"""
release.py — Sync the plugin version across both host manifests.

Both Claude Code and Codex only hand users a new plugin version when the
`version` string in the manifest changes, so the generated corpus needs a
version that moves whenever skill content moves.

Version scheme: <ARF major>.<ARF minor>.<revision>
  - <ARF major>.<ARF minor> tracks the ARF release the corpus was built from.
  - <revision> increments whenever generated skill content changes, and resets
    to 0 when the ARF major/minor changes.

Usage:
    python scripts/release.py            # bump if content changed, write manifests
    python scripts/release.py --check    # report only, exit 1 if out of sync
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import re
import json
import hashlib
import argparse
from common import OUTPUT_BASE, get_arf_version

STATE_FILE = Path(".plugin-version.json")
AGENTS_DIR = Path("plugins/eudi/agents")
ARF_VERSION_CACHE = Path(".arf-version")
CLAUDE_MANIFEST = Path("plugins/eudi/.claude-plugin/plugin.json")
CODEX_MANIFEST = Path("plugins/eudi/.codex-plugin/plugin.json")
CLAUDE_MARKETPLACE = Path(".claude-plugin/marketplace.json")
CODEX_MARKETPLACE = Path(".agents/plugins/marketplace.json")


def content_hash() -> str:
    """Hash every shipped skill and subagent so any change moves the digest."""
    h = hashlib.sha256()
    for path in sorted(OUTPUT_BASE.glob("*/SKILL.md")):
        h.update(path.parent.name.encode("utf-8"))
        h.update(path.read_bytes())
    for path in sorted(AGENTS_DIR.glob("*.md")):
        h.update(path.name.encode("utf-8"))
        h.update(path.read_bytes())
    return h.hexdigest()


def arf_base() -> str:
    """Return the <major>.<minor> prefix of the ARF release being tracked."""
    version = None
    if ARF_VERSION_CACHE.exists():
        version = ARF_VERSION_CACHE.read_text().strip()
    if not version or version == "unknown":
        version = get_arf_version()
    m = re.search(r"(\d+)\.(\d+)", version or "")
    if not m:
        return "0.0"
    return f"{m.group(1)}.{m.group(2)}"


def read_state() -> dict:
    if STATE_FILE.exists():
        return json.loads(STATE_FILE.read_text(encoding="utf-8"))
    return {}


def manifest_versions() -> list[str]:
    versions = []
    for path in (CLAUDE_MANIFEST, CODEX_MANIFEST):
        versions.append(json.loads(path.read_text(encoding="utf-8")).get("version", ""))
    return versions


def write_version(version: str) -> None:
    for path in (CLAUDE_MANIFEST, CODEX_MANIFEST):
        data = json.loads(path.read_text(encoding="utf-8"))
        data["version"] = version
        path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
        print(f"  ✓  {path} → {version}")


def check_marketplaces() -> bool:
    """Both host catalogues must agree on marketplace and plugin identity."""
    claude = json.loads(CLAUDE_MARKETPLACE.read_text(encoding="utf-8"))
    codex = json.loads(CODEX_MARKETPLACE.read_text(encoding="utf-8"))
    ok = True
    if claude["name"] != codex["name"]:
        print(f"  ✗  marketplace name differs: {claude['name']} vs {codex['name']}")
        ok = False
    claude_plugins = sorted(p["name"] for p in claude["plugins"])
    codex_plugins = sorted(p["name"] for p in codex["plugins"])
    if claude_plugins != codex_plugins:
        print(f"  ✗  plugin list differs: {claude_plugins} vs {codex_plugins}")
        ok = False
    # A marketplace entry carrying its own version would shadow plugin.json on
    # one host and not the other; plugin.json is the single source of truth.
    for name, data in (("claude", claude), ("codex", codex)):
        for plugin in data["plugins"]:
            if "version" in plugin:
                print(f"  ✗  {name} marketplace entry '{plugin['name']}' pins a version")
                ok = False
    if ok:
        print("  ✓  marketplace catalogues agree")
    return ok


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--check", action="store_true", help="Report only; exit 1 if out of sync"
    )
    args = parser.parse_args()

    if not OUTPUT_BASE.exists():
        print(f"✗  {OUTPUT_BASE} not found — run scripts/generate_all.py first")
        sys.exit(1)

    consistent = check_marketplaces()

    state = read_state()
    digest = content_hash()
    base = arf_base()

    if state.get("arf_base") != base:
        revision = 0
    elif state.get("content_hash") != digest:
        revision = int(state.get("revision", 0)) + 1
    else:
        revision = int(state.get("revision", 0))

    version = f"{base}.{revision}"
    current = manifest_versions()
    in_sync = all(v == version for v in current)

    print(f"  ARF base : {base}")
    print(f"  Revision : {revision}")
    print(f"  Version  : {version} (manifests: {', '.join(current)})")

    if args.check:
        if not in_sync:
            print("  ✗  manifests are out of sync — run python scripts/release.py")
        if not in_sync or not consistent:
            sys.exit(1)
        print("  ✓  in sync")
        return

    if not consistent:
        sys.exit(1)

    if in_sync and state.get("content_hash") == digest:
        print("  ✓  already up to date")
        return

    write_version(version)
    STATE_FILE.write_text(
        json.dumps(
            {"arf_base": base, "revision": revision, "content_hash": digest}, indent=2
        )
        + "\n",
        encoding="utf-8",
    )
    print(f"  ✓  released {version}")


if __name__ == "__main__":
    main()
