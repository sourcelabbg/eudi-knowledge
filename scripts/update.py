"""
update.py — Check if a newer ARF release is available and regenerate all skills.

Usage:
    python scripts/update.py [--force]
"""

import sys
import json
import argparse
import requests
from pathlib import Path

RELEASES_API = (
    "https://api.github.com/repos/eu-digital-identity-wallet/"
    "eudi-doc-architecture-and-reference-framework/releases/latest"
)
VERSION_CACHE = Path(".arf-version")


def get_latest_version() -> str:
    r = requests.get(RELEASES_API, timeout=10)
    r.raise_for_status()
    return r.json()["tag_name"]


def get_cached_version() -> str | None:
    if VERSION_CACHE.exists():
        return VERSION_CACHE.read_text().strip()
    return None


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--force", action="store_true", help="Re-run even if version unchanged")
    args = parser.parse_args()

    print("Checking for ARF updates...")
    latest = get_latest_version()
    cached = get_cached_version()

    print(f"  Latest : {latest}")
    print(f"  Current: {cached or 'none'}")

    if not args.force and latest == cached:
        print("  ✓  Already up to date. Use --force to regenerate anyway.")
        sys.exit(0)

    print("  → New version detected, regenerating skills...")

    import subprocess
    subprocess.run(
        [sys.executable, "scripts/generate_all.py"],
        check=True
    )

    VERSION_CACHE.write_text(latest)

    # Bump the plugin version so both hosts hand the new corpus to users.
    subprocess.run([sys.executable, "scripts/release.py"], check=True)

    print(f"  ✓  Updated to {latest}")


if __name__ == "__main__":
    main()
