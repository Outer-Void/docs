# Release records

Signed records of release builds made with [`tools/release_pipeline.py`](../tools/release_pipeline.py) (OV-63).
A record is evidence about one build. It is not a release: every receipt here says `release_status:
NOT_RELEASED` until the release policy in [constitution/lifecycle.md](../constitution/lifecycle.md) is met, and
that needs green CI, which cannot run today (D-01).

| Path | Content |
|---|---|
| `allowed_signers` | The Outer-Void release public key (Ed25519, SSH signature format), namespace `outer-void-release` |
| `<repo>/<version>[-<channel>]/spec.json` | What was built: repository URL, full commit, pinned toolchain and scanners, smoke commands, and every accepted scanner result with its reason |
| `.../SHA256SUMS`, `.../SHA256SUMS.sig` | Artifact hashes and their signature |
| `.../receipt.json`, `.../receipt.json.sig` | Every check with its result, the reproducibility result, the toolchain, the signer and the BLUX System evidence-store head |

## Key

- Owner decision 2026-11-09 (OV-63): a dedicated release key generated for this purpose. The private key is kept
  outside every repository on the owner's machine; it has no passphrase, so the machine is its custody boundary.
- Fingerprint `SHA256:Puur0bR6kbQK+12BgzoUQ7gnoa1z972W966bRqumEyc`, comment `outer-void-release-2026-11-09`.
- The termux-background key exposed in public history (F81) is permanently untrusted and never signs anything.
- Rotation: add the new key to `allowed_signers` with a dated note in this file, sign new records with it, and
  keep the old line only for records it signed.

## Verify a record

```sh
python3 tools/release_pipeline.py verify --release releases/dat/4.0.0-pilot.1
# with the artifacts, the evidence store, or a rebuild from a checkout of the recorded commit:
python3 tools/release_pipeline.py verify --release releases/dat/4.0.0-pilot.1 \
    --artifacts DIR --store ~/.local/share/outer-void/release-evidence --rebuild DAT_CHECKOUT
```

The signature check alone is:

```sh
ssh-keygen -Y verify -f releases/allowed_signers -I outer-void-release -n outer-void-release \
    -s releases/dat/4.0.0-pilot.1/receipt.json.sig < releases/dat/4.0.0-pilot.1/receipt.json
```

`--rebuild` is the strongest check because it needs nothing from the owner's machine: the builds are
reproducible, so a fresh build of the recorded commit with the recorded toolchain must give the signed hashes.
