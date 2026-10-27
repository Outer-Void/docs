"""Stage 42 hard gate: contract-breaking changes are detected automatically.

A small, self-contained fixture workspace stands in for the organization (no clones, no network). The real
`.blux/` fixture is JADIS Toolbox's. Each test applies one change and checks the verdict. Needs blux-sdk.
"""

from __future__ import annotations

import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
pytest.importorskip("blux_sdk")
import check_contracts as cc  # noqa: E402

FIX = Path(__file__).resolve().parent / "fixtures" / "dot-blux"
VF = {"protocol": "voidforge-integration/1", "capabilities": [{"capability_id": "device.list"}]}


def write(root: Path, rel: str, text: str) -> None:
    p = root / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text)


def git(root: Path, *args: str) -> str:
    return subprocess.run(["git", "-C", str(root), *args], check=True, capture_output=True, text=True,
                          env={"GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@example.com", "GIT_COMMITTER_NAME": "t",
                               "GIT_COMMITTER_EMAIL": "t@example.com", "PATH": "/usr/bin:/bin", "HOME": str(root)}).stdout.strip()


@pytest.fixture
def ws(tmp_path, monkeypatch):
    w = tmp_path / "ws"
    b = w / "blux"
    write(b, "sdk/python/src/blux_sdk/versions.py", 'CONTRACT_VERSION = "1.0"\nSUPPORTED_CONTRACT_VERSIONS: tuple[str, ...] = ("1.0",)\n')
    write(b, "sdk/python/src/blux_sdk/model_api.py", 'MODEL_API_VERSION = "1.0"\n')
    write(b, "runtime/blux_runtime/hooks/catalog.py", 'HOOKS_VERSION = "1.0"\n')
    write(b, "sdk/python/pyproject.toml", '[project]\nname = "blux-sdk"\nversion = "0.2.0"\n')
    write(b, "pyproject.toml", '[project]\nname = "outervoid-blux"\nversion = "0.4.0"\ndependencies = ["blux-sdk==0.2.0"]\n'
          '[project.scripts]\nblux = "blux_cli.main:main"\n')
    write(b, "contracts/v1/CHECKSUMS.sha256", "aaaa  receipt.schema.json\n")
    write(b, "runtime/blux_runtime/devices/voidforge_capabilities.json", json.dumps(VF))
    write(b, "cli/blux_cli/main.py", 'sub.add_parser("capabilities")\n')
    write(b, "cli/blux_cli/direct.py", 'sub.add_parser(\n    "ask",\n)\n')
    write(b, "cli/blux_cli/agent_cmd.py", 'sub.add_parser("agent")\n')
    for repo in cc.ENGINES:
        for f in FIX.iterdir():
            write(w / repo, f".blux/{f.name}", f.read_text())
    (w / "blux-system").mkdir(parents=True)
    git(b, "init", "-q")
    git(b, "add", "-A")
    git(b, "commit", "-q", "-m", "fixture")
    sha = git(b, "rev-parse", "HEAD")
    write(w / "blux-system", "pyproject.toml", f'[project]\nname = "blux-system"\nversion = "2.0.0"\ndependencies = ["blux-sdk @ git+https://github.com/Outer-Void/blux.git@{sha}#subdirectory=sdk/python"]\n'
          '[project.scripts]\nblux-system = "blux_system.cli:main"\n')
    write(w / "blux-system", "src/blux_system/cli.py", "")
    write(w / "god", "pyproject.toml", '[project]\nname = "god"\nversion = "2.0.0"\ndependencies = ["blux-sdk>=0.1.0,<0.3"]\n[project.scripts]\ngod = "god.cli:main"\n')
    write(w / "god", "src/god/cli.py", 'sub.add_parser("commands")\nsub.add_parser("index")\nsub.add_parser("capabilities")\n')
    for repo, exe in (("blux-coga", "coga"), ("blux-ca", "ca"), ("lrc", "lrc"), ("dat", "dat")):
        write(w / repo, "pyproject.toml", f'[project]\nname = "{repo}"\nversion = "1.0.0"\n[project.scripts]\n{exe} = "x:main"\n')
    write(w / "blux10k", "bin/blux10k", "#!/bin/sh\n")
    write(w / "voidforge", "integration/protocol/v1/capabilities.json", json.dumps(VF))
    write(w / "voidforge", "integration/client/voidforge", 'sub.add_parser("devices")\n')
    write(w / "axiom", "cockpit/ax/router.py", "\n".join([
        'Route("env", "blux10k", "blux10k", default=("report",)),', 'Route("ask", "BLUX", "blux", prefix=("ask",)),',
        'Route("agent", "BLUX Runtime", "blux", prefix=("agent",)),', 'Route("reason", "CogA", "coga"),', 'Route("build", "cA", "ca"),',
        'Route("create", "LRC", "lrc"),', 'Route("audit", "DAT", "dat"),', 'Route("projects", "GOD", "god", prefix=("index",)),',
        'Route("inspect", "BLUX System", "blux-system"),', 'Route("devices", "VoidForge", "voidforge", default=("devices",)),']))
    monkeypatch.setattr(cc, "LEDGER", tmp_path / "ledger.json")
    (tmp_path / "ledger.json").write_text(json.dumps({"releases": []}))
    lock = tmp_path / "lock.json"
    assert cc.main(["--workspace", str(w), "--lock", str(lock), "--write-lock"]) == 0
    return w, lock


def run(ws_lock, capsys):
    w, lock = ws_lock
    code = cc.main(["--workspace", str(w), "--lock", str(lock)])
    return code, json.loads(capsys.readouterr().out)


def edit(path: Path, old: str, new: str) -> None:
    text = path.read_text()
    assert old in text, (path, old)
    path.write_text(text.replace(old, new, 1))


def test_unchanged_ecosystem_passes(ws, capsys):
    code, report = run(ws, capsys)
    assert code == 0 and report["ok"] and report["invariant_failures"] == []


def test_removed_capability_is_breaking(ws, capsys):
    caps = ws[0] / "dat" / ".blux" / "capabilities.yaml"
    text = caps.read_text()
    blocks = text.split("\n  - contract: blux.capability\n")
    caps.write_text("\n  - contract: blux.capability\n".join(blocks[:-1]) + "\n")  # drop the last capability
    code, report = run(ws, capsys)
    assert code == 1 and any("removed" in c["change"] and c["where"] == "dat" for c in report["breaking"])


def test_changed_capability_schema_is_breaking(ws, capsys):
    edit(ws[0] / "blux-ca" / ".blux" / "capabilities.yaml", '"required": ["format", "classification", "architecture"]',
         '"required": ["format"]')
    code, report = run(ws, capsys)
    assert code == 1 and any("schema" in c["change"] and c["where"] == "blux-ca" for c in report["breaking"])


def test_added_capability_is_additive_not_breaking(ws, capsys):
    caps = ws[0] / "lrc" / ".blux" / "capabilities.yaml"
    text = caps.read_text()
    first = text[text.index("  - contract: blux.capability"):].split("\n  - contract: blux.capability")[0]
    caps.write_text(text + "\n" + first.replace("environment.inspect", "environment.extra") + "\n")
    code, report = run(ws, capsys)
    assert code == 0 and any(c["class"] == "ADDITIVE" and "environment.extra" in c["change"] for c in report["changes"])


def test_contract_schemas_changed_without_version_bump(ws, capsys):
    edit(ws[0] / "blux" / "contracts" / "v1" / "CHECKSUMS.sha256", "aaaa", "bbbb")
    code, report = run(ws, capsys)
    assert code == 1 and any("without a contract version change" in c["change"] for c in report["breaking"])


def test_new_contract_version_breaks_engines_and_pins(ws, capsys):
    edit(ws[0] / "blux" / "sdk" / "python" / "src" / "blux_sdk" / "versions.py", '"1.0",)', '"2.0",)')
    edit(ws[0] / "blux" / "sdk" / "python" / "src" / "blux_sdk" / "versions.py", 'CONTRACT_VERSION = "1.0"', 'CONTRACT_VERSION = "2.0"')
    code, report = run(ws, capsys)
    assert code == 1
    assert any(f.startswith("dot-blux:") for f in report["invariant_failures"])
    assert any(f.startswith("blux-system-pin:") for f in report["invariant_failures"])


@pytest.mark.parametrize("mutate,prefix", [
    (lambda w: (w / "voidforge" / "integration/protocol/v1/capabilities.json").write_text(json.dumps({**VF, "capabilities": []})), "voidforge:"),
    (lambda w: edit(w / "blux-coga" / "pyproject.toml", "coga = ", "blux-coga = "), "ax-routes:"),
    (lambda w: edit(w / "god" / "src/god/cli.py", 'sub.add_parser("index")', ""), "ax-routes:"),
    (lambda w: edit(w / "god" / "pyproject.toml", "<0.3", "<0.2"), "god-sdk-range:"),
    (lambda w: edit(w / "blux" / "pyproject.toml", "blux-sdk==0.2.0", "blux-sdk==0.1.0"), "blux-sdk:"),
])
def test_invariant_breaks_are_detected(ws, capsys, mutate, prefix):
    mutate(ws[0])
    code, report = run(ws, capsys)
    assert code == 1 and any(f.startswith(prefix) for f in report["invariant_failures"]), report["invariant_failures"]


def test_unrecorded_release_tag_is_detected(ws, capsys):
    git(ws[0] / "blux", "tag", "v9.9.9")
    code, report = run(ws, capsys)
    assert code == 1 and any("v9.9.9" in f for f in report["invariant_failures"])


def test_lock_refuses_to_record_a_broken_state(ws):
    edit(ws[0] / "god" / "pyproject.toml", "<0.3", "<0.2")
    assert cc.main(["--workspace", str(ws[0]), "--lock", str(ws[1]), "--write-lock"]) == 1
