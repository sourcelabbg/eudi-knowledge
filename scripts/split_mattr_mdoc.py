"""
split_mattr_mdoc.py — Fetch MATTR Learn mDocs pages and generate skills.

Covers freely available ISO/IEC 18013-5 (mdoc) documentation from MATTR Learn:
  - Core capabilities (security features, UX, revocation)
  - Standards and technologies (ISO standards, CBOR, COSE, hashing, X.509)
  - Structure to function (data model, MSO, selective disclosure, device auth)

Source: https://learn.mattr.global/docs/concepts/mdocs

Usage: python scripts/split_mattr_mdoc.py
"""

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import (
    OUTPUT_BASE,
    clean_skills_with_prefix,
    fetch_html_as_markdown,
    write_skill,
)

MATTR_BASE = "https://learn.mattr.global/docs/concepts/mdocs"
VERSION = "MATTR-Learn-2025"

PAGES = {
    "mdoc-core-capabilities": {
        "path": "/core-capabilities",
        "title": "Core Capabilities",
        "description": (
            "Use when understanding mDoc/ISO 18013-5 core capabilities. "
            "Covers: issuer data authentication, device authentication, "
            "holder authentication, session encryption, remote and in-person "
            "verification workflows, selective disclosure, and revocation."
        ),
    },
    "mdoc-standards-tech": {
        "path": "/standards-and-technologies",
        "title": "Standards and technology",
        "description": (
            "Use when understanding the standards and technologies behind mDocs. "
            "Covers: ISO/IEC 18013-5, 18013-7, 23220 standards overview, CBOR "
            "encoding, COSE signing, salted hashed claims, and X.509 certificate "
            "chains (IACA, DSC)."
        ),
    },
    "mdoc-structure-function": {
        "path": "/structure-to-function",
        "title": "Structure to Function",
        "description": (
            "Use when working with mDoc/ISO 18013-5 data structures. "
            "Covers: MSO (Mobile Security Object) structure, COSE_sign1, "
            "namespaces, element digests, presentation construction, "
            "selective disclosure mechanics, device auth methods "
            "(signature vs ECDH MAC), issuer auth, offline verification, "
            "and signed mDoc payload examples with decoded JSON."
        ),
    },
}


def extract_article(raw: str, title: str) -> str:
    """Extract article content from MATTR Learn page markdown.

    Strips navigation sidebar, page chrome, UI button text,
    and truncates large base64 payloads.
    """
    # Find the page title heading — may be mid-line after nav chrome
    idx = raw.find(f"# {title}")
    if idx >= 0:
        raw = raw[idx :]

    # Ensure the title heading has a newline after it
    raw = raw.replace(f"# {title}", f"# {title}\n\n", 1)

    # Strip trailing page chrome
    for marker in [
        "How would you rate this page?",
        "Last updated on",
        "### On this page",
    ]:
        cut = raw.find(marker)
        if cut > 0:
            raw = raw[:cut]

    # Remove "Copy MarkdownOpen" UI button text
    raw = raw.replace("Copy MarkdownOpen", "")

    # Truncate any long base64/encoded string values in JSON examples
    # Matches: "key": "<200+ base64 chars>" regardless of key name
    raw = re.sub(
        r'("\w+":\s*")'
        r"([A-Za-z0-9+/=]{200})[A-Za-z0-9+/=]+",
        r"\1\2... [truncated]",
        raw,
    )

    # Also truncate bare long base64 lines (not in JSON key-value format)
    raw = re.sub(
        r"^([A-Za-z0-9+/=]{200})[A-Za-z0-9+/=]+",
        r"\1... [truncated]",
        raw,
        flags=re.MULTILINE,
    )

    # Collapse excessive blank lines
    raw = re.sub(r"\n{4,}", "\n\n\n", raw)

    return raw.strip()

def main() -> None:
    print("\n── EUDI Knowledge: MATTR mDocs ────────────────────────────────")

    clean_skills_with_prefix("mdoc-")
    count = 0

    for skill_name, config in PAGES.items():
        url = MATTR_BASE + config["path"]
        print(f"  Fetching {skill_name}...")

        try:
            raw = fetch_html_as_markdown(url, source_url=url)
        except Exception as e:
            print(f"  ✗  {skill_name}: fetch failed — {e}")
            continue

        content = extract_article(raw, config["title"])
        if not content.strip():
            print(f"  ✗  {skill_name}: no content extracted")
            continue

        write_skill(
            skill_dir=OUTPUT_BASE / skill_name,
            name=skill_name,
            description=config["description"],
            content=content,
            version=VERSION,
        )
        count += 1

    print(f"\n  Done: {count} MATTR mDocs skills written")


if __name__ == "__main__":
    main()
