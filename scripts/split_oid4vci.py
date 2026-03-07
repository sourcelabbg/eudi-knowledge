"""
split_oid4vci.py — Fetch OpenID4VCI 1.0 spec and split into OpenCode SKILL.md files.
Usage: python scripts/split_oid4vci.py
"""

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import OUTPUT_BASE, fetch_html_as_markdown, extract_section, write_skill

OID4VCI_URL = (
    "https://openid.net/specs/openid-4-verifiable-credential-issuance-1_0.html"
)
OID4VCI_VERSION = "1.0-2025-02-03"

OID4VCI_SKILLS = {
    "oid4vci-overview": {
        "section_numbers": ["1", "2", "3"],
        "description": (
            "Use when needing an overview of OpenID4VCI, its terminology, or "
            "the credential issuance flow. Covers: Credential Issuer, Wallet, "
            "authorization code flow, pre-authorized code flow, and the "
            "relationship between OID4VCI and OAuth 2.0."
        ),
    },
    "oid4vci-issuer-metadata": {
        "section_numbers": ["4", "5"],
        "description": (
            "Use when configuring Credential Issuer metadata or discovering "
            "issuer capabilities. Covers: .well-known endpoints, "
            "credential_configurations_supported, display properties, "
            "proof types supported, and issuer discovery."
        ),
    },
    "oid4vci-credential-offer": {
        "section_numbers": ["6"],
        "description": (
            "Use when implementing credential offer flows (issuer-initiated "
            "issuance). Covers: credential_offer parameter, "
            "credential_offer_uri, grants object, authorization_code and "
            "pre-authorized_code grant types."
        ),
    },
    "oid4vci-authorization": {
        "section_numbers": ["7", "8"],
        "description": (
            "Use when implementing the authorization flow for credential "
            "issuance. Covers: authorization request with issuer_state, "
            "authorization_details, scope-based requests, pushed "
            "authorization requests (PAR), and token endpoint extensions."
        ),
    },
    "oid4vci-credential-endpoint": {
        "section_numbers": ["9", "10"],
        "description": (
            "Use when implementing the credential endpoint for issuing "
            "credentials. Covers: credential request format, proof of "
            "possession (key binding), credential response, error handling, "
            "and the nonce endpoint for fresh c_nonce values."
        ),
    },
    "oid4vci-batch-issuance": {
        "section_numbers": ["11"],
        "description": (
            "Use when implementing batch credential issuance. Covers: "
            "batch credential request format, batch credential response, "
            "and handling multiple credentials in a single issuance flow."
        ),
    },
    "oid4vci-deferred-notification": {
        "section_numbers": ["9", "11"],
        "description": (
            "Use when implementing deferred credential retrieval or "
            "notification endpoints. Covers: transaction_id for deferred "
            "issuance, deferred credential endpoint, and notification "
            "of credential acceptance or deletion."
        ),
    },
    "oid4vci-security": {
        "section_numbers": ["14", "15"],
        "description": (
            "Use when reviewing security or privacy considerations for "
            "OpenID4VCI. Covers: credential replay prevention, TLS "
            "requirements, proof of possession security, nonce management, "
            "and privacy considerations for credential issuance."
        ),
    },
}


def main() -> None:
    print("\n── EUDI Knowledge: OpenID4VCI ─────────────────────────────────")
    print("  Fetching OpenID4VCI 1.0 spec...")
    raw = fetch_html_as_markdown(OID4VCI_URL)
    output_base = OUTPUT_BASE

    for skill_name, config in OID4VCI_SKILLS.items():
        sections = config["section_numbers"]
        parts = []

        for section_num in sections:
            patterns = [
                rf"^## {re.escape(section_num)}[\.\s]",
                rf"^## {re.escape(section_num)}\.",
                rf"^# {re.escape(section_num)}[\.\s]",
            ]
            content = extract_section(raw, patterns)
            if content.strip():
                parts.append(content)

        if not parts:
            print(
                f"  ✗  {skill_name}: no content matched — may need pattern adjustment"
            )
            continue

        combined = "\n\n---\n\n".join(parts)
        write_skill(
            skill_dir=output_base / skill_name,
            name=skill_name,
            description=config["description"],
            content=combined,
            version=OID4VCI_VERSION,
        )

    skills_written = list(output_base.glob("oid4vci-*/SKILL.md"))
    print(f"\n  Done: {len(skills_written)} OID4VCI skills written")


if __name__ == "__main__":
    main()
