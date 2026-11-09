"""Shared release machinery (OV-63): build, check independently, record and sign a Python release.

Owner decisions (2026-11-09):
- a dedicated Ed25519 release key, kept outside every repository, signs in the SSH signature format
  (`ssh-keygen -Y sign`, namespace `outer-void-release`); the public key is `releases/allowed_signers`;
- the DAT pilot is local: no tag and no GitHub release while CI cannot run (D-01);
- F113: the signed receipt carries the BLUX System evidence-store head, so a consistent rewrite of that store
  is detected (`verify --store`).

`pilot` never trusts the tool it releases to judge itself:
1. Two fresh clones from the spec's URL at the spec's full commit, each built with the pinned toolchain and
   SOURCE_DATE_EPOCH = the commit time. sdists are normalized (setuptools writes checkout mtimes and the local
   user into the tar); the two builds must be byte-identical.
2. Counted checks: the test suite and lint in a fresh environment, install of the wheel and of the sdist into
   empty environments with the spec's smoke commands, and independent scanners (bandit, detect-secrets,
   pip-audit) whose accepted results are listed with reasons in the spec. Anything not accepted fails.
3. The tool's own verdict on itself (`self_checks`) is recorded but never counted.
4. SHA256SUMS and receipt.json are written; the artifacts and an operation receipt go into a BLUX System store,
   whose head is written into receipt.json; both files are signed.

    python3 tools/release_pipeline.py pilot --spec releases/dat/4.0.0-pilot.1/spec.json --work DIR \
        --key ~/.config/outer-void/release-keys/release_ed25519 --store DIR [--record]
    python3 tools/release_pipeline.py verify --release releases/dat/4.0.0-pilot.1 [--artifacts DIR] [--store DIR]
        [--rebuild SOURCE_DIR]

`pilot` exits 0 only when every counted check passed. `verify` exits 0 only when every requested check passed.
"""

from __future__ import annotations

import argparse
import gzip
import hashlib
import io
import json
import os
import re
import shutil
import subprocess
import sys
import tarfile
import tempfile
import time
import tomllib
import xml.etree.ElementTree as ET  # parses only JUnit files this tool just wrote
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
ALLOWED_SIGNERS = ROOT / "releases" / "allowed_signers"
NAMESPACE = "outer-void-release"
PRINCIPAL = "outer-void-release"
SHA_RE = re.compile(r"^[0-9a-f]{40}$")
PIN_RE = re.compile(r"^[A-Za-z0-9_.\-]+(\[[a-z0-9,]+\])?==[A-Za-z0-9_.+\-]+$")
RECEIPT_KIND = "outer-void.release-receipt"


class ReleaseError(Exception):
    pass


# -- spec --------------------------------------------------------------------------------------------------------


def load_spec(path: Path) -> dict[str, Any]:
    spec = json.loads(path.read_text())
    problems = []
    for key in ("repo", "url", "commit", "version", "channel", "build_requirements", "scanner_requirements"):
        if key not in spec:
            problems.append(f"missing {key}")
    if not SHA_RE.match(spec.get("commit", "")):
        problems.append("commit must be a full 40-character SHA")
    for req in spec.get("build_requirements", []) + spec.get("scanner_requirements", []):
        if not PIN_RE.match(req):
            problems.append(f"requirement {req!r} is not pinned with ==")
    if problems:
        raise ReleaseError("invalid spec: " + "; ".join(problems))
    return spec


# -- reproducible sdist --------------------------------------------------------------------------------------------


def normalize_sdist(path: Path, epoch: int) -> None:
    """Rewrite a .tar.gz so its bytes depend only on the file contents: sorted members, fixed mtime, owner and
    modes, and a gzip header without a timestamp or file name."""
    with tarfile.open(path, "r:gz") as src:
        members = []
        for m in src.getmembers():
            if not (m.isfile() or m.isdir()):
                raise ReleaseError(f"{path.name}: unexpected member type for {m.name}")
            data = src.extractfile(m).read() if m.isfile() else None  # type: ignore[union-attr]
            members.append((m, data))
    raw = io.BytesIO()
    with tarfile.open(fileobj=raw, mode="w", format=tarfile.PAX_FORMAT) as out:
        for m, data in sorted(members, key=lambda pair: pair[0].name):
            info = tarfile.TarInfo(m.name)
            info.mtime = epoch
            info.uid = info.gid = 0
            info.uname = info.gname = ""
            if m.isdir():
                info.type = tarfile.DIRTYPE
                info.mode = 0o755
                out.addfile(info)
            else:
                info.mode = 0o755 if m.mode & 0o111 else 0o644
                info.size = len(data or b"")
                out.addfile(info, io.BytesIO(data or b""))
    packed = io.BytesIO()
    with gzip.GzipFile(filename="", mode="wb", fileobj=packed, mtime=0, compresslevel=9) as gz:
        gz.write(raw.getvalue())
    path.write_bytes(packed.getvalue())


# -- helpers ---------------------------------------------------------------------------------------------------------


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def run(argv: list[str], *, cwd: Path | None = None, env: dict[str, str] | None = None, timeout: int = 3600) -> Any:
    return subprocess.run(argv, cwd=cwd, env=env, capture_output=True, text=True, timeout=timeout, check=False)


def must(argv: list[str], **kw: Any) -> str:
    proc = run(argv, **kw)
    if proc.returncode != 0:
        raise ReleaseError(f"{' '.join(argv[:3])}… exited {proc.returncode}: {proc.stderr.strip()[-400:]}")
    return proc.stdout


def venv(path: Path, requirements: list[str], *, with_pip: bool = True) -> Path:
    must([sys.executable, "-m", "venv", *([] if with_pip else ["--without-pip"]), str(path)])
    if requirements:
        must([str(path / "bin" / "python"), "-m", "pip", "install", "-q", *requirements])
    return path / "bin"


def clone(url: str, commit: str, dest: Path) -> None:
    must(["git", "clone", "-q", url, str(dest)])
    must(["git", "-C", str(dest), "checkout", "-q", commit])
    head = must(["git", "-C", str(dest), "rev-parse", "HEAD"]).strip()
    if head != commit:
        raise ReleaseError(f"clone is at {head}, not {commit}")
    if must(["git", "-C", str(dest), "status", "--porcelain"]).strip():
        raise ReleaseError("fresh clone is not clean")


def tracked_files(source: Path) -> list[str]:
    """The files a release is made from: what git tracks at the checked-out commit."""
    return [f for f in must(["git", "-C", str(source), "ls-files", "-z"]).split("\0") if f]


def build(source: Path, bin_dir: Path, out: Path, epoch: int) -> dict[str, str]:
    env = {**os.environ, "SOURCE_DATE_EPOCH": str(epoch), "PYTHONHASHSEED": "0"}
    must([str(bin_dir / "python"), "-m", "build", "--no-isolation", "--outdir", str(out), str(source)], env=env)
    hashes = {}
    for f in sorted(out.iterdir()):
        if f.name.endswith(".tar.gz"):
            normalize_sdist(f, epoch)
        hashes[f.name] = sha256_file(f)
    return hashes


def junit_counts(path: Path) -> dict[str, int]:
    root = ET.parse(path).getroot()
    suites = [root] if root.tag == "testsuite" else list(root)
    total = {k: sum(int(s.get(k, 0)) for s in suites) for k in ("tests", "failures", "errors", "skipped")}
    total["passed"] = total["tests"] - total["failures"] - total["errors"] - total["skipped"]
    return total


def check(name: str, argv: list[str], proc: Any, ok: bool, **extra: Any) -> dict[str, Any]:
    return {"name": name, "argv": argv, "exit": proc.returncode, "passed": ok, **extra}


# -- independent scanners ----------------------------------------------------------------------------------------


def judge_bandit(report: dict[str, Any], accepted: list[dict[str, str]]) -> dict[str, Any]:
    """Every MEDIUM or HIGH result must be accepted in the spec by test id and file; LOW results are counted."""
    allow = {(a["test_id"], a["filename"]) for a in accepted}
    blocking, accepted_hits, low = [], [], 0
    for r in report.get("results", []):
        key = (r["test_id"], r["filename"])
        if r["issue_severity"] == "LOW":
            low += 1
        elif key in allow:
            accepted_hits.append({"test_id": key[0], "filename": key[1], "line": r["line_number"]})
        else:
            blocking.append({"test_id": key[0], "filename": key[1], "line": r["line_number"], "severity": r["issue_severity"]})
    errors = report.get("errors", [])
    return {"blocking": blocking, "accepted": accepted_hits, "low": low, "errors": len(errors),
            "passed": not blocking and not errors}


def judge_detect_secrets(report: dict[str, Any], accepted: list[dict[str, str]]) -> dict[str, Any]:
    """Every hit must be accepted by file, type and detect-secrets' SHA-1 of the value (never the value)."""
    # The spec stores detect-secrets' hashed_secret as value_sha1, so the spec itself never looks like a credential.
    allow = {(a["filename"], a["type"], a["value_sha1"]) for a in accepted}
    blocking, hits = [], 0
    for filename, results in sorted(report.get("results", {}).items()):
        for r in results:
            hits += 1
            if (filename, r["type"], r["hashed_secret"]) not in allow:
                blocking.append({"filename": filename, "type": r["type"], "line": r["line_number"]})
    return {"hits": hits, "blocking": blocking, "passed": not blocking}


def judge_pip_audit(report: dict[str, Any]) -> dict[str, Any]:
    deps = report.get("dependencies", [])
    vulns = [{"name": d["name"], "id": v["id"]} for d in deps for v in d.get("vulns", [])]
    skipped = [d["name"] for d in deps if "skip_reason" in d]
    return {"dependencies": len(deps), "vulnerabilities": vulns, "not_on_index": skipped, "passed": not vulns}


# -- fixtures for smoke commands ---------------------------------------------------------------------------------

# Generated at run time so no credential-shaped literal is ever committed.
TOKENS = {"github_token": "ghp_" + "A1b2C3d4E5f6G7h8I9j0" + "K1l2M3n4O5p6Q7r8"}


def make_fixture(base: Path, name: str, spec: dict[str, Any]) -> Path:
    root = base / name
    root.mkdir(parents=True)
    for rel, text in spec.get("files", {}).items():
        p = root / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text.format(**TOKENS))
    if spec.get("git"):
        must(["git", "init", "-q", str(root)])
        must(["git", "-C", str(root), "add", "-A"])
        must(["git", "-C", str(root), "-c", "user.name=release", "-c", "user.email=release@invalid", "commit", "-qm", "f"])
    return root


def smoke(bin_dir: Path, cwd: Path, fixtures: dict[str, Path], cases: list[dict[str, Any]]) -> list[dict[str, Any]]:
    results = []
    for case in cases:
        argv = [a.format(bin=str(bin_dir), **{f"fixture_{k}": str(v) for k, v in fixtures.items()}) for a in case["argv"]]
        proc = run(argv, cwd=cwd, timeout=600)
        ok = proc.returncode == case.get("exit", 0) and case.get("stdout_contains", "") in proc.stdout
        results.append({"argv": case["argv"], "exit": proc.returncode, "expected_exit": case.get("exit", 0), "passed": ok})
    return results


# -- signing -----------------------------------------------------------------------------------------------------


def sign(path: Path, key: Path) -> Path:
    sig = path.with_name(path.name + ".sig")
    sig.unlink(missing_ok=True)
    must(["ssh-keygen", "-q", "-Y", "sign", "-f", str(key), "-n", NAMESPACE, str(path)])
    return sig


def verify_signature(path: Path, allowed: Path) -> bool:
    sig = path.with_name(path.name + ".sig")
    if not sig.is_file():
        return False
    with path.open("rb") as data:
        proc = subprocess.run(
            ["ssh-keygen", "-Y", "verify", "-f", str(allowed), "-I", PRINCIPAL, "-n", NAMESPACE, "-s", str(sig)],
            stdin=data, capture_output=True, check=False,
        )
    return proc.returncode == 0


def key_fingerprint(key: Path) -> str:
    pub = key.with_name(key.name + ".pub")
    return must(["ssh-keygen", "-l", "-E", "sha256", "-f", str(pub)]).split()[1]


# -- BLUX System evidence ----------------------------------------------------------------------------------------


def record_evidence(store: Path, spec: dict[str, Any], artifacts: Path, sums: bytes, passed: bool) -> dict[str, Any]:
    """Store the artifacts and one operation receipt in a BLUX System store; return the anchor for receipt.json."""
    from blux_sdk import envelopes, ids  # the BLUX SDK, installed with blux-system
    from blux_sdk.serialization import sha256_of
    from blux_sdk.timeutil import utc_now

    exe = shutil.which("blux-system") or str(Path(sys.executable).with_name("blux-system"))
    if not (store / "head.json").exists() and not any(store.glob("*")):
        must([exe, "init", "--store", str(store)])
    op = ids.new_operation_id()
    started = utc_now()
    artifact_ids = []
    for f in sorted(artifacts.iterdir()):
        doc = envelopes.artifact_from_bytes(
            operation_id=op, name=f.name, media_type="application/octet-stream", data=f.read_bytes()
        )
        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as tmp:
            json.dump(doc, tmp)
        try:
            must([exe, "ingest", "--store", str(store), "--kind", "artifact", "--data", str(f), tmp.name])
        finally:
            os.unlink(tmp.name)
        artifact_ids.append(doc["artifact_id"])
    receipt = envelopes.receipt(
        receipt_id=ids.new_receipt_id(), operation_id=op, parent_operation_id=None, session_id=None, project_id=None,
        capability_id="release.pilot", capability_version=None, actor={"type": "service", "id": "release-pipeline"},
        status="succeeded" if passed else "failed", error_code=None if passed else "EXECUTION_FAILED",
        policy_decision={"effect": "not_evaluated", "policy_id": None, "rule_id": None,
                         "reason": "release pipeline run by the owner (OV-63)"},
        input_sha256=sha256_of({k: spec[k] for k in ("repo", "url", "commit", "version", "channel")}),
        output_sha256=hashlib.sha256(sums).hexdigest(), artifact_ids=artifact_ids, started_at=started,
        finished_at=utc_now(), issuer={"component": "outer-void.release-pipeline", "version": "1.0.0"},
    )
    proc = subprocess.run([exe, "ingest", "--store", str(store), "-"], input=json.dumps(receipt), capture_output=True,
                          text=True, check=False)
    if proc.returncode != 0:
        raise ReleaseError(f"blux-system ingest failed: {proc.stdout.strip()[-400:]}")
    verify = json.loads(run([exe, "verify", "--store", str(store)]).stdout)
    if not verify.get("ok"):
        raise ReleaseError(f"evidence store does not verify: {verify.get('problems')}")
    return {"operation_id": op, "receipt_id": receipt["receipt_id"], "artifact_ids": artifact_ids,
            "head": verify["head"], "records": verify["records"]}


# -- pilot ---------------------------------------------------------------------------------------------------------


def pilot(spec_path: Path, work: Path, key: Path, store: Path, record: bool) -> int:
    spec = load_spec(spec_path)
    if work.exists() and any(work.iterdir()):
        raise ReleaseError(f"{work} must be empty")
    work.mkdir(parents=True, exist_ok=True)
    t0 = time.time()
    build_bin = venv(work / "build-venv", spec["build_requirements"])
    for side in ("a", "b"):
        clone(spec["url"], spec["commit"], work / side)
    version = tomllib.loads((work / "a" / "pyproject.toml").read_text())["project"]["version"]
    if version != spec["version"]:
        raise ReleaseError(f"pyproject version {version} != spec version {spec['version']}")
    epoch = int(must(["git", "-C", str(work / "a"), "log", "-1", "--format=%ct"]).strip())
    builds = {side: build(work / side, build_bin, work / f"dist-{side}", epoch) for side in ("a", "b")}
    reproducible = builds["a"] == builds["b"]
    checks: list[dict[str, Any]] = [{"name": "reproducible-build", "passed": reproducible, "builds": builds}]
    src = work / "a"

    # Test suite and lint in a fresh environment.
    t = spec["tests"]
    test_bin = venv(work / "test-venv", [])
    must([str(test_bin / "python"), "-m", "pip", "install", "-q", "-e", f"{src}[{t['extras']}]" if t.get("extras") else str(src)])
    if t.get("extra_pip"):
        must([str(test_bin / "python"), "-m", "pip", "install", "-q", *t["extra_pip"]])
    junit = work / "junit.xml"
    argv = [str(test_bin / "python"), "-m", "pytest", "-q", "-p", "no:cacheprovider", f"--junitxml={junit}"]
    proc = run(argv, cwd=src, env={**os.environ, **t.get("env", {})})
    counts = junit_counts(junit) if junit.exists() else {}
    checks.append(check("test-suite", ["pytest"], proc, proc.returncode == 0 and counts.get("passed", 0) > 0, counts=counts))
    for cmd in t.get("lint", []):
        proc = run([str(test_bin / cmd[0]), *cmd[1:]], cwd=src)
        checks.append(check(f"lint:{cmd[0]} {' '.join(cmd[1:])}".strip(), cmd, proc, proc.returncode == 0))

    # Install each artifact into an empty environment and run the smoke commands outside the source tree.
    fixtures_dir = work / "fixtures"
    fixtures = {name: make_fixture(fixtures_dir, name, f) for name, f in spec.get("fixtures", {}).items()}
    wheel = next((work / "dist-a").glob("*.whl"))
    sdist = next((work / "dist-a").glob("*.tar.gz"))
    wheel_bin = venv(work / "wheel-venv", [], with_pip=False)
    proc = run([str(build_bin / "python"), "-m", "pip", "--python", str(wheel_bin / "python"), "install", "-q",
                "--no-index", "--no-deps", str(wheel)])
    results = smoke(wheel_bin, fixtures_dir, fixtures, spec["smoke"]) if proc.returncode == 0 else []
    checks.append(check("install-wheel", ["pip install --no-index --no-deps", wheel.name], proc,
                        proc.returncode == 0 and bool(results) and all(r["passed"] for r in results), smoke=results))
    sdist_bin = venv(work / "sdist-venv", [r for r in spec["build_requirements"] if r.startswith(("setuptools", "wheel"))])
    proc = run([str(sdist_bin / "python"), "-m", "pip", "install", "-q", "--no-index", "--no-deps",
                "--no-build-isolation", str(sdist)])
    results = smoke(sdist_bin, fixtures_dir, fixtures, spec["smoke"]) if proc.returncode == 0 else []
    checks.append(check("install-sdist", ["pip install --no-index --no-deps", sdist.name], proc,
                        proc.returncode == 0 and bool(results) and all(r["passed"] for r in results), smoke=results))

    # Independent scanners.
    scan_bin = venv(work / "scan-venv", spec["scanner_requirements"])
    sc = spec.get("scanners", {})
    out = work / "bandit.json"
    proc = run([str(scan_bin / "bandit"), "-q", "-r", *sc.get("bandit_paths", ["src"]), "-f", "json", "-o", str(out)], cwd=src)
    verdict = judge_bandit(json.loads(out.read_text()), sc.get("bandit_accepted", [])) if out.exists() else {"passed": False}
    checks.append(check("independent:bandit", ["bandit", "-r", *sc.get("bandit_paths", ["src"])], proc, verdict["passed"], **verdict))
    # Only the files git tracks: the tests and linters above leave caches in the clone (OV-63 pilot run 1 failed on
    # .mypy_cache/CACHEDIR.TAG).
    proc = run([str(scan_bin / "detect-secrets"), "scan", *tracked_files(src)], cwd=src)
    verdict = judge_detect_secrets(json.loads(proc.stdout), sc.get("detect_secrets_accepted", [])) if proc.returncode == 0 else {"passed": False}
    checks.append(check("independent:detect-secrets", ["detect-secrets", "scan", "<git ls-files>"], proc, verdict["passed"], **verdict))
    site = next((work / "wheel-venv" / "lib").glob("python*/site-packages"))
    proc = run([str(scan_bin / "pip-audit"), "--path", str(site), "-f", "json", "--progress-spinner", "off"])
    verdict = judge_pip_audit(json.loads(proc.stdout)) if proc.stdout.strip().startswith("{") else {"passed": False}
    checks.append(check("independent:pip-audit", ["pip-audit", "--path", "<wheel-venv site-packages>"], proc, verdict["passed"], **verdict))

    # The tool judging itself: recorded, never counted.
    self_checks = []
    for case in spec.get("self_checks", []):
        argv = [a.format(bin=str(wheel_bin), source=str(src)) for a in case["argv"]]
        proc = run(argv, cwd=src)
        self_checks.append({"argv": case["argv"], "exit": proc.returncode, "counted": False})

    passed = all(c["passed"] for c in checks)
    artifacts = work / "artifacts"
    shutil.copytree(work / "dist-a", artifacts)
    sums = "".join(f"{builds['a'][n]}  {n}\n" for n in sorted(builds["a"])).encode()
    (work / "SHA256SUMS").write_bytes(sums)
    anchor = record_evidence(store, spec, artifacts, sums, passed)
    freeze = must([str(build_bin / "python"), "-m", "pip", "freeze", "--all"]).split()
    receipt = {
        "kind": RECEIPT_KIND,
        "version": "1",
        "repo": spec["repo"],
        "url": spec["url"],
        "commit": spec["commit"],
        "package_version": spec["version"],
        "channel": spec["channel"],
        "result": "PASS" if passed else "FAIL",
        "release_status": "NOT_RELEASED",
        "ci": spec.get("ci", {"status": "BLOCKED", "decision": "D-01"}),
        "created_at": datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "duration_s": int(time.time() - t0),
        "source_date_epoch": epoch,
        "toolchain": {"python": sys.version.split()[0], "build": freeze},
        "artifacts": [{"name": n, "size": (artifacts / n).stat().st_size, "sha256": h} for n, h in sorted(builds["a"].items())],
        "checks": checks,
        "self_checks": self_checks,
        "signer": {"fingerprint": key_fingerprint(key), "namespace": NAMESPACE, "principal": PRINCIPAL},
        "evidence_store": anchor,
    }
    (work / "receipt.json").write_text(json.dumps(receipt, indent=1, sort_keys=True) + "\n")
    sign(work / "SHA256SUMS", key)
    sign(work / "receipt.json", key)
    if record:
        dest = spec_path.parent
        for name in ("SHA256SUMS", "SHA256SUMS.sig", "receipt.json", "receipt.json.sig"):
            shutil.copy2(work / name, dest / name)
    print(json.dumps({"result": receipt["result"], "artifacts": receipt["artifacts"], "head": anchor["head"],
                      "failed": [c["name"] for c in checks if not c["passed"]]}, indent=1))
    return 0 if passed else 1


# -- verify ------------------------------------------------------------------------------------------------------


def verify(release: Path, artifacts: Path | None, store: Path | None, rebuild: Path | None, allowed: Path) -> int:
    results: dict[str, Any] = {}
    receipt_path, sums_path = release / "receipt.json", release / "SHA256SUMS"
    results["receipt_signature"] = verify_signature(receipt_path, allowed)
    results["sums_signature"] = verify_signature(sums_path, allowed)
    receipt = json.loads(receipt_path.read_text())
    listed = {}
    for line in sums_path.read_text().splitlines():
        digest, name = line.split("  ", 1)
        listed[name] = digest
    results["sums_match_receipt"] = listed == {a["name"]: a["sha256"] for a in receipt["artifacts"]}
    results["receipt_result"] = receipt.get("result") == "PASS"
    if artifacts is not None:
        results["artifacts_match"] = all(
            (artifacts / n).is_file() and sha256_file(artifacts / n) == d for n, d in listed.items()
        )
    if store is not None:
        exe = shutil.which("blux-system") or str(Path(sys.executable).with_name("blux-system"))
        head = receipt["evidence_store"]["head"]
        proc = run([exe, "verify", "--store", str(store), "--expect-head", head])
        results["store_anchor"] = proc.returncode == 0
    if rebuild is not None:
        with tempfile.TemporaryDirectory() as tmp:
            reqs = [r for r in receipt["toolchain"]["build"] if r.split("==")[0] in ("build", "setuptools", "wheel")]
            bin_dir = venv(Path(tmp) / "venv", reqs)
            got = build(rebuild, bin_dir, Path(tmp) / "dist", receipt["source_date_epoch"])
        results["rebuild_matches"] = got == listed
    ok = all(results.values())
    print(json.dumps({"ok": ok, **results}, indent=1, sort_keys=True))
    return 0 if ok else 1


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("pilot")
    p.add_argument("--spec", type=Path, required=True)
    p.add_argument("--work", type=Path, required=True)
    p.add_argument("--key", type=Path, required=True)
    p.add_argument("--store", type=Path, required=True)
    p.add_argument("--record", action="store_true", help="copy the signed receipt and sums next to the spec")
    v = sub.add_parser("verify")
    v.add_argument("--release", type=Path, required=True)
    v.add_argument("--artifacts", type=Path)
    v.add_argument("--store", type=Path)
    v.add_argument("--rebuild", type=Path, help="a checkout of the receipt's commit to rebuild and compare")
    v.add_argument("--allowed-signers", type=Path, default=ALLOWED_SIGNERS)
    args = ap.parse_args(argv)
    try:
        if args.cmd == "pilot":
            return pilot(args.spec, args.work, args.key.expanduser(), args.store.expanduser(), args.record)
        return verify(args.release, args.artifacts, args.store, args.rebuild, args.allowed_signers)
    except ReleaseError as exc:
        print(f"release_pipeline: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
