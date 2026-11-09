"""OV-63: the shared release machinery (tools/release_pipeline.py)."""

from __future__ import annotations

import io
import json
import shutil
import subprocess
import sys
import tarfile
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))

import release_pipeline as rp

ROOT = Path(__file__).resolve().parent.parent
HAVE_SSH_KEYGEN = shutil.which("ssh-keygen") is not None


def _tar(path: Path, mtime: int, uname: str, order: list[str]) -> None:
    files = {"pkg-1.0/PKG-INFO": b"Name: pkg\n", "pkg-1.0/src/a.py": b"print(1)\n", "pkg-1.0/run.sh": b"#!/bin/sh\n"}
    with tarfile.open(path, "w:gz") as tf:
        for name in order:
            info = tarfile.TarInfo(name)
            info.mtime, info.uname, info.uid = mtime, uname, 1000
            if name in files:
                info.size = len(files[name])
                info.mode = 0o775 if name.endswith(".sh") else 0o664
                tf.addfile(info, io.BytesIO(files[name]))
            else:
                info.type, info.mode = tarfile.DIRTYPE, 0o775
                tf.addfile(info)


def test_normalized_sdists_depend_only_on_their_contents(tmp_path: Path) -> None:
    """setuptools writes checkout mtimes and the local user into sdists, so two clean builds differ (OV-63)."""
    names = ["pkg-1.0", "pkg-1.0/PKG-INFO", "pkg-1.0/src", "pkg-1.0/src/a.py", "pkg-1.0/run.sh"]
    a, b = tmp_path / "a.tar.gz", tmp_path / "b.tar.gz"
    _tar(a, 1_700_000_000, "alice", names)
    _tar(b, 1_800_000_000, "bob", list(reversed(names)))
    assert a.read_bytes() != b.read_bytes()
    rp.normalize_sdist(a, 1_794_235_396)
    rp.normalize_sdist(b, 1_794_235_396)
    assert a.read_bytes() == b.read_bytes()
    with tarfile.open(a) as tf:
        members = {m.name: m for m in tf.getmembers()}
        assert tf.extractfile("pkg-1.0/src/a.py").read() == b"print(1)\n"  # type: ignore[union-attr]
    assert members["pkg-1.0/run.sh"].mode == 0o755 and members["pkg-1.0/PKG-INFO"].mode == 0o644
    assert {m.uname for m in members.values()} == {""} and {m.mtime for m in members.values()} == {1_794_235_396}


def test_specs_must_pin_everything(tmp_path: Path) -> None:
    spec = {"repo": "x", "url": "u", "commit": "abc123", "version": "1", "channel": "pilot.1",
            "build_requirements": ["build>=1"], "scanner_requirements": ["bandit==1.8.6"]}
    (tmp_path / "s.json").write_text(json.dumps(spec))
    with pytest.raises(rp.ReleaseError) as err:
        rp.load_spec(tmp_path / "s.json")
    assert "full 40-character SHA" in str(err.value) and "'build>=1' is not pinned" in str(err.value)


def test_scanner_verdicts_fail_on_anything_not_accepted() -> None:
    bandit = {"results": [
        {"test_id": "B603", "filename": "src/x.py", "line_number": 1, "issue_severity": "LOW"},
        {"test_id": "B314", "filename": "src/a.py", "line_number": 2, "issue_severity": "MEDIUM"},
    ], "errors": []}
    assert not rp.judge_bandit(bandit, [])["passed"]
    ok = rp.judge_bandit(bandit, [{"test_id": "B314", "filename": "src/a.py", "reason": "r"}])
    assert ok["passed"] and ok["low"] == 1
    assert not rp.judge_bandit({**bandit, "errors": [{"filename": "x"}]},
                               [{"test_id": "B314", "filename": "src/a.py"}])["passed"]
    ds = {"results": {"t.py": [{"type": "Secret Keyword", "hashed_secret": "h1", "line_number": 3}]}}
    assert not rp.judge_detect_secrets(ds, [])["passed"]
    assert rp.judge_detect_secrets(ds, [{"filename": "t.py", "type": "Secret Keyword", "value_sha1": "h1"}])["passed"]
    assert not rp.judge_detect_secrets(ds, [{"filename": "t.py", "type": "Secret Keyword", "value_sha1": "h2"}])["passed"]
    audit = {"dependencies": [{"name": "a", "version": "1", "vulns": [{"id": "GHSA-x"}]}]}
    assert not rp.judge_pip_audit(audit)["passed"]
    assert rp.judge_pip_audit({"dependencies": [{"name": "pkg", "skip_reason": "not on PyPI"}]})["passed"]


@pytest.fixture
def signed_release(tmp_path: Path) -> tuple[Path, Path, Path, Path]:
    if not HAVE_SSH_KEYGEN:
        pytest.skip("no ssh-keygen")
    key = tmp_path / "k"
    subprocess.run(["ssh-keygen", "-q", "-t", "ed25519", "-N", "", "-f", str(key)], check=True)
    pub = key.with_name("k.pub").read_text().split()
    allowed = tmp_path / "allowed_signers"
    allowed.write_text(f'{rp.PRINCIPAL} namespaces="{rp.NAMESPACE}" {pub[0]} {pub[1]}\n')
    arts = tmp_path / "artifacts"
    arts.mkdir()
    (arts / "pkg-1.0-py3-none-any.whl").write_bytes(b"wheel")
    rel = tmp_path / "release"
    rel.mkdir()
    digest = rp.sha256_file(arts / "pkg-1.0-py3-none-any.whl")
    (rel / "SHA256SUMS").write_text(f"{digest}  pkg-1.0-py3-none-any.whl\n")
    receipt = {"kind": rp.RECEIPT_KIND, "result": "PASS",
               "artifacts": [{"name": "pkg-1.0-py3-none-any.whl", "sha256": digest, "size": 5}],
               "evidence_store": {"head": "0" * 64}}
    (rel / "receipt.json").write_text(json.dumps(receipt))
    rp.sign(rel / "SHA256SUMS", key)
    rp.sign(rel / "receipt.json", key)
    return rel, arts, allowed, key


def test_a_signed_release_verifies(signed_release: tuple[Path, Path, Path, Path]) -> None:
    rel, arts, allowed, _ = signed_release
    assert rp.verify(rel, arts, None, None, allowed) == 0


def test_a_changed_artifact_fails(signed_release: tuple[Path, Path, Path, Path]) -> None:
    rel, arts, allowed, _ = signed_release
    (arts / "pkg-1.0-py3-none-any.whl").write_bytes(b"other")
    assert rp.verify(rel, arts, None, None, allowed) == 1


def test_an_edited_receipt_fails(signed_release: tuple[Path, Path, Path, Path]) -> None:
    rel, arts, allowed, _ = signed_release
    (rel / "receipt.json").write_text((rel / "receipt.json").read_text().replace("PASS", "PASS "))
    assert rp.verify(rel, arts, None, None, allowed) == 1


def test_a_failed_run_never_verifies_even_when_signed(signed_release: tuple[Path, Path, Path, Path]) -> None:
    rel, arts, allowed, key = signed_release
    (rel / "receipt.json").write_text((rel / "receipt.json").read_text().replace('"PASS"', '"FAIL"'))
    rp.sign(rel / "receipt.json", key)
    assert rp.verify(rel, arts, None, None, allowed) == 1


def test_another_key_is_not_trusted(signed_release: tuple[Path, Path, Path, Path], tmp_path: Path) -> None:
    rel, arts, _, _ = signed_release
    other = tmp_path / "o"
    subprocess.run(["ssh-keygen", "-q", "-t", "ed25519", "-N", "", "-f", str(other)], check=True)
    pub = other.with_name("o.pub").read_text().split()
    allowed = tmp_path / "other_signers"
    allowed.write_text(f'{rp.PRINCIPAL} namespaces="{rp.NAMESPACE}" {pub[0]} {pub[1]}\n')
    assert rp.verify(rel, arts, None, None, allowed) == 1


def _blux_system() -> str | None:
    local = Path(sys.executable).with_name("blux-system")
    return str(local) if local.exists() else shutil.which("blux-system")


@pytest.mark.skipif(_blux_system() is None, reason="needs blux-system and the BLUX SDK")
def test_f113_a_consistently_rewritten_evidence_store_is_detected(
    signed_release: tuple[Path, Path, Path, Path], tmp_path: Path
) -> None:
    """F113 (owner decision 2026-11-09): the signed receipt carries the store head. Rebuilding the whole store, so
    that its own chain still verifies, no longer goes unnoticed."""
    rel, arts, allowed, key = signed_release
    spec = {"repo": "pkg", "url": "u", "commit": "c" * 40, "version": "1.0", "channel": "pilot.1"}
    store = tmp_path / "store"
    anchor = rp.record_evidence(store, spec, arts, (rel / "SHA256SUMS").read_bytes(), True)
    receipt = json.loads((rel / "receipt.json").read_text())
    receipt["evidence_store"] = anchor
    (rel / "receipt.json").write_text(json.dumps(receipt))
    rp.sign(rel / "receipt.json", key)
    assert rp.verify(rel, arts, store, None, allowed) == 0

    forged = tmp_path / "forged"
    rp.record_evidence(forged, {**spec, "commit": "d" * 40}, arts, b"forged sums\n", True)
    exe = _blux_system()
    assert subprocess.run([exe, "verify", "--store", str(forged)], capture_output=True).returncode == 0
    shutil.rmtree(store)
    shutil.copytree(forged, store)
    assert rp.verify(rel, arts, store, None, allowed) == 1


def test_recorded_releases_verify_against_the_published_key() -> None:
    """Every recorded release in releases/ is signed by the key in releases/allowed_signers, and its sums match."""
    if not HAVE_SSH_KEYGEN:
        pytest.skip("no ssh-keygen")
    keys = [line for line in (ROOT / "releases" / "allowed_signers").read_text().splitlines() if line.strip()]
    assert len(keys) == 1 and f'namespaces="{rp.NAMESPACE}" ssh-ed25519 ' in keys[0]
    receipts = sorted((ROOT / "releases").glob("*/*/receipt.json"))
    assert receipts, "no recorded release"
    for receipt in receipts:
        assert rp.verify(receipt.parent, None, None, None, rp.ALLOWED_SIGNERS) == 0, receipt
        doc = json.loads(receipt.read_text())
        assert doc["release_status"] == "NOT_RELEASED" and doc["ci"]["status"] == "BLOCKED"
        assert all(c["passed"] for c in doc["checks"])
        assert all(not s["counted"] for s in doc["self_checks"])


def test_scanners_see_only_tracked_files(tmp_path: Path) -> None:
    """Pilot run 1 (OV-63) failed: detect-secrets scanned the caches mypy and ruff had just written into the clone."""
    subprocess.run(["git", "init", "-q", str(tmp_path)], check=True)
    (tmp_path / "a.py").write_text("x = 1\n")
    (tmp_path / ".mypy_cache").mkdir()
    (tmp_path / ".mypy_cache" / "CACHEDIR.TAG").write_text("Signature: 8a477f597d28d172789f06886806bc55\n")
    subprocess.run(["git", "-C", str(tmp_path), "add", "a.py"], check=True)
    assert rp.tracked_files(tmp_path) == ["a.py"]
