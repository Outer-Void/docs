"""Ecosystem contract verification (Stage 42), without cloning the organization.

It reads only the few files that define each boundary: from sibling checkouts (`--workspace ~/ov`) or by
fetching single files from GitHub at a ref (`--fetch`, public repositories, no clones). It then checks:

Invariants (must always hold):
  blux-sdk          the runtime's blux-sdk pin equals the SDK version shipped in the same repository (BLUX <-> Runtime)
  dot-blux          every engine's .blux/ loads with the current SDK and declares a supported contract version
                    (BLUX <-> CogA, cA, DAT, LRC, GOD, jadis)
  blux-system-pin   the SDK commit BLUX System pins supports BLUX's current contract version (BLUX <-> BLUX System)
  god-sdk-range     GOD's blux-sdk version range includes the current SDK version (BLUX <-> GOD)
  voidforge         BLUX's copy of the VoidForge capability catalogue equals VoidForge's (BLUX <-> VoidForge adapter)
  ax-routes         every `ax` route's executable is provided by its engine, and its subcommand exists (ax <-> engines)
  release-ledger    every release tag in the checked repositories is recorded in ecosystem/release-ledger.json

Against the lock (ecosystem/compatibility.json), changes are classified:
  BREAKING  a capability removed or its input/output schema changed; Contract v1 schemas changed without a contract
            version change; contract, Model API or Hook System version changed
  ADDITIVE  a capability added
  INFO      a commit or package version moved

    python3 tools/check_contracts.py --workspace ~/ov            # check; exit 1 on a breaking change or invariant failure
    python3 tools/check_contracts.py --fetch                     # same, reading main from GitHub
    python3 tools/check_contracts.py --workspace ~/ov --write-lock   # accept the current state (a reviewed decision)
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
import tempfile
import tomllib
import urllib.request
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
LOCK = ROOT / "ecosystem" / "compatibility.json"
LEDGER = ROOT / "ecosystem" / "release-ledger.json"
ORG = "Outer-Void"
ENGINES = ("blux-coga", "blux-ca", "dat", "lrc", "god", "jadis.toolbox", "blux")
REPOS = ("blux", "blux-system", "blux-coga", "blux-ca", "dat", "lrc", "god", "jadis.toolbox", "axiom", "voidforge", "blux10k")


def sha256(data: str | bytes) -> str:
    return hashlib.sha256(data.encode() if isinstance(data, str) else data).hexdigest()


def canonical(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


class Source:
    """Reads files from a repository at a ref: a local checkout, or single-file fetches from GitHub."""

    def __init__(self, workspace: Path | None, ref: str = "main"):
        self.workspace, self.ref = workspace, ref

    def read(self, repo: str, path: str, ref: str | None = None) -> str | None:
        if self.workspace is not None and ref is None:
            p = self.workspace / repo / path
            return p.read_text(encoding="utf-8") if p.is_file() else None
        if self.workspace is not None:  # a historical ref of a local checkout
            out = subprocess.run(["git", "-C", str(self.workspace / repo), "show", f"{ref}:{path}"], capture_output=True, text=True)
            return out.stdout if out.returncode == 0 else None
        url = f"https://raw.githubusercontent.com/{ORG}/{repo}/{ref or self.ref}/{path}"
        try:
            with urllib.request.urlopen(url, timeout=30) as resp:  # noqa: S310 - fixed https host
                return resp.read().decode("utf-8")
        except OSError:
            return None

    def head(self, repo: str) -> str | None:
        if self.workspace is not None:
            out = subprocess.run(["git", "-C", str(self.workspace / repo), "rev-parse", "--short=12", "HEAD"], capture_output=True, text=True)
            return out.stdout.strip() or None
        out = subprocess.run(["git", "ls-remote", f"https://github.com/{ORG}/{repo}.git", self.ref], capture_output=True, text=True)
        return out.stdout.split()[0][:12] if out.stdout.strip() else None

    def tags(self, repo: str) -> list[str]:
        target = str(self.workspace / repo) if self.workspace is not None else f"https://github.com/{ORG}/{repo}.git"
        out = subprocess.run(["git", "ls-remote", "--tags", target] if self.workspace is None else ["git", "-C", target, "tag"],
                             capture_output=True, text=True)
        if self.workspace is None:
            return sorted({line.split("refs/tags/")[1].removesuffix("^{}") for line in out.stdout.splitlines() if "refs/tags/" in line})
        return sorted(t for t in out.stdout.split() if t)


def _const(text: str | None, name: str) -> str | None:
    m = re.search(rf'^{name}\s*(?::[^=]*)?=\s*["(]([^")]+)', text or "", re.M)
    return m.group(1).strip().strip('",') if m else None


def _scripts(pyproject: str | None) -> set[str]:
    if not pyproject:
        return set()
    return set((tomllib.loads(pyproject).get("project", {}).get("scripts") or {}).keys())


def _version_tuple(v: str) -> tuple[int, ...]:
    return tuple(int(x) for x in re.findall(r"\d+", v)[:3])


def _in_range(version: str, spec: str) -> bool:
    for part in [p.strip() for p in spec.split(",") if p.strip()]:
        m = re.match(r"(>=|<=|==|<|>)\s*([\d.]+)", part)
        if not m:
            return False
        op, bound = m.group(1), _version_tuple(m.group(2))
        v = _version_tuple(version)
        if not {">=": v >= bound, "<=": v <= bound, "==": v == bound, "<": v < bound, ">": v > bound}[op]:
            return False
    return True


def snapshot(src: Source) -> dict[str, Any]:
    """Everything the checks compare, read from the sources."""
    versions_py = src.read("blux", "sdk/python/src/blux_sdk/versions.py")
    snap: dict[str, Any] = {
        "commits": {r: src.head(r) for r in REPOS},
        "blux": {
            "contract_version": _const(versions_py, "CONTRACT_VERSION"),
            "supported_contract_versions": re.findall(r'"([\d.]+)"', (re.search(r"SUPPORTED_CONTRACT_VERSIONS[^=]*=\s*\(([^)]*)\)", versions_py or "") or [None, ""])[1]),
            "model_api_version": _const(src.read("blux", "sdk/python/src/blux_sdk/model_api.py"), "MODEL_API_VERSION"),
            "hooks_version": _const(src.read("blux", "runtime/blux_runtime/hooks/catalog.py"), "HOOKS_VERSION"),
            "sdk_version": (tomllib.loads(src.read("blux", "sdk/python/pyproject.toml") or "").get("project") or {}).get("version"),
            "runtime_sdk_pin": next((d for d in (tomllib.loads(src.read("blux", "pyproject.toml") or "").get("project") or {}).get("dependencies", [])
                                     if d.startswith("blux-sdk")), None),
            "contracts_sha256": sha256(src.read("blux", "contracts/v1/CHECKSUMS.sha256") or ""),
            "voidforge_copy_sha256": sha256(canonical(json.loads(src.read("blux", "runtime/blux_runtime/devices/voidforge_capabilities.json") or "{}"))),
        },
        "voidforge_catalogue_sha256": sha256(canonical(json.loads(src.read("voidforge", "integration/protocol/v1/capabilities.json") or "{}"))),
        "capabilities": {},
    }
    for repo in ENGINES:
        caps = src.read(repo, ".blux/capabilities.yaml")
        if caps is None:
            continue
        snap["capabilities"][repo] = _capability_digests(caps)
    return snap


def _capability_digests(capabilities_yaml: str) -> dict[str, str]:
    from blux_sdk.serialization import loads_yaml

    doc = loads_yaml(capabilities_yaml)
    return {c["capability_id"]: sha256(canonical({"input": c.get("input_schema"), "output": c.get("output_schema")}))
            for c in doc.get("capabilities", [])}


def invariants(src: Source, snap: dict[str, Any]) -> list[str]:
    from blux_sdk import dot_blux
    from blux_sdk.errors import BluxError

    out: list[str] = []
    b = snap["blux"]
    if b["runtime_sdk_pin"] != f"blux-sdk=={b['sdk_version']}":
        out.append(f"blux-sdk: the runtime pins {b['runtime_sdk_pin']!r} but the repository ships blux-sdk {b['sdk_version']}")
    for repo in ENGINES:
        files = {n: src.read(repo, f".blux/{n}") for n in ("manifest.yaml", "capabilities.yaml", "policy.yaml")}
        if files["manifest.yaml"] is None:
            out.append(f"dot-blux: {repo} has no .blux/manifest.yaml")
            continue
        with tempfile.TemporaryDirectory() as tmp:
            (Path(tmp) / ".blux").mkdir()
            for name, text in files.items():
                if text is not None:
                    (Path(tmp) / ".blux" / name).write_text(text)
            try:
                loaded = dot_blux.load(tmp)
            except BluxError as exc:
                out.append(f"dot-blux: {repo}/.blux does not validate with blux-sdk {b['sdk_version']}: {exc}")
                continue
        if str(loaded.manifest.get("contract_version")) not in b["supported_contract_versions"]:
            out.append(f"dot-blux: {repo} declares contract {loaded.manifest.get('contract_version')}, SDK supports {b['supported_contract_versions']}")
    pin = re.search(r"blux\.git@([0-9a-f]{7,40})#subdirectory=sdk/python", src.read("blux-system", "pyproject.toml") or "")
    if not pin:
        out.append("blux-system-pin: blux-system does not pin blux-sdk to a commit")
    else:
        pinned = src.read("blux", "sdk/python/src/blux_sdk/versions.py", ref=pin.group(1))
        supported = re.findall(r'"([\d.]+)"', (re.search(r"SUPPORTED_CONTRACT_VERSIONS[^=]*=\s*\(([^)]*)\)", pinned or "") or [None, ""])[1])
        if b["contract_version"] not in supported:
            out.append(f"blux-system-pin: blux-sdk at {pin.group(1)[:12]} supports {supported or 'nothing readable'}, BLUX speaks {b['contract_version']}")
    god_dep = next((d for d in (tomllib.loads(src.read("god", "pyproject.toml") or "").get("project") or {}).get("dependencies", [])
                    if d.startswith("blux-sdk")), "")
    spec = god_dep.removeprefix("blux-sdk").strip()
    if not spec or not _in_range(b["sdk_version"] or "0", spec):
        out.append(f"god-sdk-range: GOD requires {god_dep or 'no blux-sdk'}, current blux-sdk is {b['sdk_version']}")
    if b["voidforge_copy_sha256"] != snap["voidforge_catalogue_sha256"]:
        out.append("voidforge: BLUX's voidforge_capabilities.json differs from voidforge integration/protocol/v1/capabilities.json")
    out += _ax_routes(src)
    out += _release_ledger(src)
    return out


def _ax_routes(src: Source) -> list[str]:
    router = src.read("axiom", "cockpit/ax/router.py") or ""
    routes = re.findall(r'Route\("([a-z-]+)",\s*"[^"]+",\s*"([a-z0-9-]+)"(?:,\s*prefix=\(([^)]*)\))?', router)
    if not routes:
        return ["ax-routes: no routes found in axiom cockpit/ax/router.py"]
    providers = {
        "blux": (_scripts(src.read("blux", "pyproject.toml")),
                 "\n".join(src.read("blux", f"cli/blux_cli/{m}.py") or "" for m in ("main", "direct", "agent_cmd", "migrate"))),
        "blux-system": (_scripts(src.read("blux-system", "pyproject.toml")), src.read("blux-system", "src/blux_system/cli.py")),
        "god": (_scripts(src.read("god", "pyproject.toml")), src.read("god", "src/god/cli.py")),
        "coga": (_scripts(src.read("blux-coga", "pyproject.toml")), None),
        "ca": (_scripts(src.read("blux-ca", "pyproject.toml")), None),
        "lrc": (_scripts(src.read("lrc", "pyproject.toml")), None),
        "dat": (_scripts(src.read("dat", "pyproject.toml")), None),
        "blux10k": ({"blux10k"} if src.read("blux10k", "bin/blux10k") is not None else set(), None),
        "voidforge": ({"voidforge"} if src.read("voidforge", "integration/client/voidforge") is not None else set(),
                      src.read("voidforge", "integration/client/voidforge")),
    }
    out = []
    for command, exe, prefix in routes:
        if exe not in providers:
            out.append(f"ax-routes: `ax {command}` routes to {exe!r}, which no checked repository provides")
            continue
        scripts, cli = providers[exe]
        if exe not in scripts:
            out.append(f"ax-routes: `ax {command}` needs the executable {exe!r}, which its repository does not declare")
        sub = re.findall(r'"([a-z-]+)"', prefix or "")
        if sub and cli is not None and not re.search(rf'add_parser\(\s*"{sub[0]}"', cli):
            out.append(f"ax-routes: `ax {command}` calls `{exe} {sub[0]}`, which {exe} does not define")
    return out


def _release_ledger(src: Source) -> list[str]:
    ledger = json.loads(LEDGER.read_text()) if LEDGER.exists() else {"releases": []}
    recorded = {(r["repo"], r["tag"]) for r in ledger["releases"]}
    out = []
    for repo in REPOS:
        for tag in src.tags(repo):
            if (repo, tag) not in recorded:
                out.append(f"release-ledger: {repo} tag {tag!r} is not recorded in ecosystem/release-ledger.json")
    return out


def compare(lock: dict[str, Any], snap: dict[str, Any]) -> list[dict[str, str]]:
    changes = []

    def add(kind: str, where: str, what: str) -> None:
        changes.append({"class": kind, "where": where, "change": what})

    lb, sb = lock["blux"], snap["blux"]
    for key in ("contract_version", "model_api_version", "hooks_version"):
        if lb.get(key) != sb.get(key):
            add("BREAKING", "blux", f"{key} {lb.get(key)} -> {sb.get(key)}")
    if lb["contracts_sha256"] != sb["contracts_sha256"] and lb["contract_version"] == sb["contract_version"]:
        add("BREAKING", "blux", "Contract v1 schemas changed without a contract version change")
    if lb.get("sdk_version") != sb.get("sdk_version"):
        add("INFO", "blux", f"blux-sdk {lb.get('sdk_version')} -> {sb.get('sdk_version')}")
    for repo, caps in lock["capabilities"].items():
        now = snap["capabilities"].get(repo, {})
        for cid, digest in caps.items():
            if cid not in now:
                add("BREAKING", repo, f"capability {cid} removed")
            elif now[cid] != digest:
                add("BREAKING", repo, f"capability {cid} changed its input/output schema")
        for cid in sorted(set(now) - set(caps)):
            add("ADDITIVE", repo, f"capability {cid} added")
    for repo in sorted(set(snap["capabilities"]) - set(lock["capabilities"])):
        add("ADDITIVE", repo, "new .blux/ provider")
    for repo, sha in snap["commits"].items():
        if lock["commits"].get(repo) != sha:
            add("INFO", repo, f"commit {lock['commits'].get(repo)} -> {sha}")
    return changes


def render(lock: dict[str, Any]) -> str:
    b = lock["blux"]
    lines = ["<!-- GENERATED by tools/check_contracts.py from ecosystem/compatibility.json; do not edit. -->",
             "# Compatibility matrix", "",
             f"Accepted baseline for contract verification. Contract {b['contract_version']} (SDK supports "
             f"{', '.join(b['supported_contract_versions'])}), Model API {b['model_api_version']}, Hook System {b['hooks_version']}, "
             f"blux-sdk {b['sdk_version']}. Check: `python3 tools/check_contracts.py --fetch` (CI) or `--workspace ~/ov`.", "",
             "| Repository | Commit | Declared capabilities |", "|---|---|---|"]
    for repo, sha in sorted(lock["commits"].items()):
        caps = lock["capabilities"].get(repo)
        lines.append(f"| `{repo}` | `{sha}` | {len(caps) if caps is not None else '—'} |")
    lines += ["", "Boundaries verified on every check: BLUX ↔ Runtime (SDK pin), BLUX ↔ CogA, cA, DAT, LRC, GOD and jadis (`.blux/` with the",
              "current SDK), BLUX ↔ BLUX System (pinned SDK supports the contract), BLUX ↔ GOD (SDK range), BLUX ↔ VoidForge adapter",
              "(capability catalogue copy), ax ↔ engines (executables and subcommands), and the release ledger.", ""]
    return "\n".join(lines)


COMPAT_MD = ROOT / "ecosystem" / "compatibility.md"


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="check_contracts")
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument("--workspace", type=Path, help="directory with sibling checkouts (e.g. ~/ov)")
    g.add_argument("--fetch", action="store_true", help="read single files from GitHub (public repositories)")
    p.add_argument("--ref", default="main")
    p.add_argument("--lock", type=Path, default=LOCK)
    p.add_argument("--write-lock", action="store_true", help="record the current state as the accepted baseline")
    args = p.parse_args(argv)
    src = Source(args.workspace.expanduser() if args.workspace else None, args.ref)
    snap = snapshot(src)
    problems = invariants(src, snap)
    if args.write_lock:
        if problems:
            print("refusing to write a lock while invariants fail:", *problems, sep="\n  ", file=sys.stderr)
            return 1
        args.lock.write_text(json.dumps(snap, indent=1, sort_keys=True) + "\n")
        if args.lock == LOCK:
            COMPAT_MD.write_text(render(snap))
        print(f"wrote {args.lock}")
        return 0
    changes = compare(json.loads(args.lock.read_text()), snap) if args.lock.exists() else [{"class": "BREAKING", "where": "lock", "change": "no lock"}]
    if args.lock == LOCK and args.lock.exists() and (not COMPAT_MD.exists() or COMPAT_MD.read_text() != render(json.loads(args.lock.read_text()))):
        problems.append("ecosystem/compatibility.md does not match the lock: re-run with --write-lock")
    report = {"invariant_failures": problems, "changes": changes,
              "breaking": [c for c in changes if c["class"] == "BREAKING"], "ok": not problems and not any(c["class"] == "BREAKING" for c in changes)}
    print(json.dumps(report, indent=1, sort_keys=True))
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
