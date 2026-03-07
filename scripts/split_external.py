"""
split_external.py — Fetch external EUDI-related specs and generate skills.

Covers:
  - OpenID4VC High Assurance Interoperability Profile (HAIP) 1.0
  - SD-JWT (RFC 9901)
  - SD-JWT VC (draft)
  - Token Status List (draft)
  - W3C Verifiable Credentials Data Model 2.0
  - W3C Digital Credentials API

Each spec becomes one or more skills depending on size.

Usage: python scripts/split_external.py
"""

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import (
    OUTPUT_BASE,
    TOKEN_WARN,
    count_tokens,
    fetch_html_as_markdown,
    extract_section,
    extract_all_sections_at_level,
    write_skill,
    slugify,
)

# ── Spec definitions ───────────────────────────────────────────────────────

SPECS = {
    "haip": {
        "url": "https://openid.net/specs/openid4vc-high-assurance-interoperability-profile-1_0.html",
        "version": "1.0-2025-03-04",
        "skills": {
            "haip-overview": {
                "section_numbers": ["1", "2", "3", "4"],
                "description": (
                    "Use when understanding the EUDI High Assurance "
                    "Interoperability Profile for OpenID4VC. Covers: scope, "
                    "terminology, overview of profiled specs, and general "
                    "requirements for EUDI interoperability."
                ),
            },
            "haip-protocol-profile": {
                "section_numbers": ["5", "6"],
                "description": (
                    "Use when implementing HAIP protocol requirements. Covers: "
                    "OpenID4VP profile (request/response modes, client_id, "
                    "session transcript), OpenID4VCI profile (credential "
                    "offer, authorization, credential endpoint), and "
                    "credential-format-specific profiles (ISO mdocs, SD-JWT VC)."
                ),
            },
            "haip-security": {
                "section_numbers": ["7", "8"],
                "description": (
                    "Use when reviewing HAIP security or privacy requirements. "
                    "Covers: key management, token binding, attestation-based "
                    "client authentication, and privacy considerations for "
                    "high-assurance credential flows."
                ),
            },
        },
    },
    "sd-jwt": {
        "url": "https://www.rfc-editor.org/rfc/rfc9901.html",
        "version": "RFC-9901",
        "skills": {
            "sd-jwt-intro": {
                "section_numbers": ["1", "2"],
                "description": (
                    "Use when understanding SD-JWT (Selective Disclosure JWT) "
                    "concepts and terminology. Covers: introduction, use cases, "
                    "and key definitions."
                ),
            },
            "sd-jwt-format": {
                "section_numbers": ["3", "4"],
                "description": (
                    "Use when working with SD-JWT data formats. Covers: SD-JWT "
                    "and SD-JWT+KB structure, disclosures, salt/hash mechanisms, "
                    "and decoy digests."
                ),
            },
            "sd-jwt-examples": {
                "section_numbers": ["5"],
                "description": (
                    "Use when understanding SD-JWT through examples. Covers: "
                    "complete issuance and presentation examples, including "
                    "issuer-side selective disclosure construction."
                ),
            },
            "sd-jwt-examples-nested": {
                "section_numbers": ["6"],
                "description": (
                    "Use when implementing nested SD-JWT data handling. Covers: "
                    "flat, structured, and recursive disclosure examples for "
                    "complex claim sets."
                ),
            },
            "sd-jwt-verification": {
                "section_numbers": ["7", "8"],
                "description": (
                    "Use when implementing SD-JWT verification or JWS "
                    "serialization. Covers: SD-JWT verification, holder "
                    "processing, verifier verification, JWS JSON serialization "
                    "formats."
                ),
            },
            "sd-jwt-security": {
                "section_numbers": ["9", "10", "11"],
                "description": (
                    "Use when reviewing SD-JWT security considerations. "
                    "Covers: threat model, hash collision, claim name "
                    "collisions, key binding enforcement, and privacy "
                    "considerations for selective disclosure."
                ),
            },
        },
    },
    "sd-jwt-vc": {
        "url": "https://www.ietf.org/archive/id/draft-ietf-oauth-sd-jwt-vc-08.html",
        "version": "draft-08",
        "skills": {
            "sd-jwt-vc-intro": {
                "section_numbers": ["1", "2", "3"],
                "description": (
                    "Use when understanding the SD-JWT VC credential format. "
                    "Covers: introduction, terminology, and the vct (Verifiable "
                    "Credential Type) claim."
                ),
            },
            "sd-jwt-vc-metadata": {
                "section_numbers": ["4", "5"],
                "description": (
                    "Use when configuring SD-JWT VC issuer or type metadata. "
                    "Covers: header parameters, registered claims, issuer-signed "
                    "JWT, issuer metadata, and type metadata resolution."
                ),
            },
            "sd-jwt-vc-presentation-security": {
                "section_numbers": ["6", "7", "8", "9", "10"],
                "description": (
                    "Use when presenting or verifying SD-JWT VCs. Covers: "
                    "presentation in OpenID4VP, JWT claims, security "
                    "considerations, and privacy considerations."
                ),
            },
        },
    },
    "token-status-list": {
        "url": "https://www.ietf.org/archive/id/draft-ietf-oauth-status-list-10.html",
        "version": "draft-10",
        "skills": {
            "token-status-list-core": {
                "section_numbers": ["1", "2", "3", "4", "5"],
                "description": (
                    "Use when understanding Token Status List fundamentals. "
                    "Covers: introduction, terminology, status list "
                    "representation (compressed byte array, JSON, CBOR), and "
                    "status list tokens (JWT, CWT)."
                ),
            },
            "token-status-list-usage": {
                "section_numbers": ["6", "7"],
                "description": (
                    "Use when implementing Token Status List verification. "
                    "Covers: referenced tokens (JOSE/COSE), status types, "
                    "verification procedures, and validation rules."
                ),
            },
            "token-status-list-verification-details": {
                "section_numbers": ["8"],
                "description": (
                    "Use when implementing detailed Token Status List "
                    "verification behavior. Covers section-specific verification "
                    "rules and processing details."
                ),
            },
            "token-status-list-aggregation-x509": {
                "section_numbers": ["9", "10"],
                "description": (
                    "Use when implementing Token Status List aggregation and "
                    "PKI integration. Covers: status list aggregation behavior and "
                    "X.509 extensions."
                ),
            },
        },
    },
}

# W3C specs — section-based splitting for large specs
W3C_SPECS = {
    "w3c-vc-data-model": {
        "url": "https://www.w3.org/TR/vc-data-model-2.0/",
        "version": "2.0-2024-12-04",
        "skills": {
            "w3c-vcdm-intro": {
                "section_numbers": ["1"],
                "description": (
                    "Use when understanding W3C Verifiable Credentials Data Model "
                    "2.0 introduction. Covers: document overview, what is a "
                    "verifiable credential, ecosystem overview, and conformance "
                    "requirements."
                ),
            },
            "w3c-vcdm-terminology": {
                "section_numbers": ["2"],
                "description": (
                    "Use when looking up W3C VCDM 2.0 terminology or "
                    "understanding key term definitions. Covers core vocabulary "
                    "used across the specification."
                ),
            },
            "w3c-vcdm-data-model-concepts": {
                "section_numbers": ["3"],
                "description": (
                    "Use when understanding W3C VCDM core data model concepts. "
                    "Covers: claims, credentials, and presentations."
                ),
            },
            "w3c-vcdm-getting-started": {
                "section_numbers": ["4.1", "4.2", "4.3"],
                "description": (
                    "Use when getting started with the W3C VCDM core model. "
                    "Covers: getting started, verifiable credentials, and "
                    "contexts."
                ),
            },
            "w3c-vcdm-identifiers-types": {
                "section_numbers": ["4.4"],
                "description": (
                    "Use when working with identifiers and types in W3C VCDM. "
                    "Covers: identifier modeling rules and URI usage across "
                    "credentials and presentations."
                ),
            },
            "w3c-vcdm-types": {
                "section_numbers": ["4.5"],
                "description": (
                    "Use when implementing type constraints in W3C VCDM. Covers: "
                    "type processing and type requirements for credentials and "
                    "presentations."
                ),
            },
            "w3c-vcdm-names-descriptions": {
                "section_numbers": ["4.6"],
                "description": (
                    "Use when working with human-readable labeling in W3C VCDM. "
                    "Covers: names and descriptions for credentials, "
                    "presentations, and related entities."
                ),
            },
            "w3c-vcdm-issuer": {
                "section_numbers": ["4.7"],
                "description": (
                    "Use when implementing issuer representation in W3C VCDM. "
                    "Covers: issuer property requirements, syntax options, and "
                    "issuer-related processing expectations."
                ),
            },
            "w3c-vcdm-subject-validity": {
                "section_numbers": ["4.8"],
                "description": (
                    "Use when modeling credential subject data in W3C VCDM. "
                    "Covers: credentialSubject structure and semantics."
                ),
            },
            "w3c-vcdm-validity-period": {
                "section_numbers": ["4.9"],
                "description": (
                    "Use when implementing temporal validity in W3C VCDM. Covers: "
                    "validity period semantics and related processing rules."
                ),
            },
            "w3c-vcdm-status-schemas-securing": {
                "section_numbers": ["4.10", "4.11", "4.12"],
                "description": (
                    "Use when implementing status, schema, and securing features "
                    "in W3C VCDM. Covers: status information, data schemas, and "
                    "securing mechanisms."
                ),
            },
            "w3c-vcdm-presentations": {
                "section_numbers": ["4.13"],
                "description": (
                    "Use when implementing verifiable presentations in W3C VCDM. "
                    "Covers: presentation structure, semantics, and processing "
                    "considerations."
                ),
            },
            "w3c-vcdm-trust-extensibility": {
                "section_numbers": ["5.1", "5.2"],
                "description": (
                    "Use when working with W3C VCDM trust and extensibility "
                    "features. Covers: trust model and extensibility."
                ),
            },
            "w3c-vcdm-integrity": {
                "section_numbers": ["5.3"],
                "description": (
                    "Use when implementing integrity requirements in W3C VCDM. "
                    "Covers integrity-related claims and processing expectations."
                ),
            },
            "w3c-vcdm-refreshing-evidence": {
                "section_numbers": ["5.4", "5.5", "5.6"],
                "description": (
                    "Use when implementing advanced credential semantics in W3C "
                    "VCDM. Covers: refreshing, terms of use, and evidence."
                ),
            },
            "w3c-vcdm-zkp-advanced": {
                "section_numbers": ["5.7", "5.8", "5.9", "5.10"],
                "description": (
                    "Use when implementing advanced W3C VCDM features beyond "
                    "basic credential structure. Covers: zero-knowledge proofs, "
                    "time, authorization, and reserved extensions."
                ),
            },
            "w3c-vcdm-ecosystem-graphs": {
                "section_numbers": ["5.11", "5.12", "5.13"],
                "description": (
                    "Use when implementing ecosystem compatibility and VC graph "
                    "features in W3C VCDM. Covers ecosystem compatibility, VC "
                    "graphs, and securing specifications."
                ),
            },
            "w3c-vcdm-syntaxes-algorithms": {
                "section_numbers": ["6", "7"],
                "description": (
                    "Use when implementing W3C VCDM syntax handling and "
                    "algorithms. Covers: JSON-LD, media types, type-specific "
                    "processing, verification procedures, and problem details."
                ),
            },
            "w3c-vcdm-privacy-correlation": {
                "section_numbers": ["8.1", "8.2", "8.3", "8.4", "8.5", "8.6", "8.7"],
                "description": (
                    "Use when reviewing early-section W3C VCDM privacy guidance. "
                    "Covers: privacy architecture and correlation-related risks "
                    "and mitigations."
                ),
            },
            "w3c-vcdm-privacy-minimization": {
                "section_numbers": ["8.8", "8.9", "8.10", "8.11"],
                "description": (
                    "Use when implementing data-minimization and selective "
                    "disclosure privacy approaches in W3C VCDM. Covers privacy "
                    "tradeoffs and mitigation patterns in mid-section privacy "
                    "guidance."
                ),
            },
            "w3c-vcdm-privacy-minimization-continued": {
                "section_numbers": ["8.12", "8.13", "8.14"],
                "description": (
                    "Use when implementing later mid-section W3C VCDM privacy "
                    "mitigations. Covers additional selective disclosure and "
                    "privacy-preserving design patterns."
                ),
            },
            "w3c-vcdm-privacy-threats": {
                "section_numbers": [
                    "8.15",
                    "8.16",
                    "8.17",
                    "8.18",
                    "8.19",
                    "8.20",
                    "8.21",
                ],
                "description": (
                    "Use when assessing advanced W3C VCDM privacy threats and "
                    "residual risks. Covers: late-section privacy threats, "
                    "issuer/verifier cooperation impacts, and ecosystem risk "
                    "considerations."
                ),
            },
            "w3c-vcdm-security": {
                "section_numbers": ["9"],
                "description": (
                    "Use when reviewing W3C VCDM security or privacy "
                    "considerations. Covers: security concerns for verifiable "
                    "credentials and ecosystem deployments."
                ),
            },
        },
    },
    "w3c-dc-api": {
        "url": "https://w3c-fedid.github.io/digital-credentials/",
        "version": "draft-2025",
        "skills": {
            "w3c-dc-api-core": {
                "section_numbers": [
                    "Introduction",
                    "Model",
                    "Scope",
                    "The Digital Credentials API",
                    "Integration with Credential Management API",
                    "Permissions Policy integration",
                    "Registry of protocols",
                ],
                "description": (
                    "Use when implementing the W3C Digital Credentials API for "
                    "browser-based credential exchange. Covers: DigitalCredential "
                    "interface, navigator.credentials.get() extensions, "
                    "credential management integration, and permissions policy."
                ),
            },
            "w3c-dc-api-security": {
                "section_numbers": [
                    "Security Considerations",
                    "Privacy Considerations",
                    "Accessibility Considerations",
                ],
                "description": (
                    "Use when reviewing W3C Digital Credentials API security and "
                    "privacy. Covers: credential protocol security, cross-device "
                    "security, quishing, data integrity, XSS/CSRF protection, "
                    "session security, privacy considerations, and accessibility."
                ),
            },
        },
    },
}


def generate_section_based_skills() -> int:
    """Generate skills from IETF/OIDF HTML specs by section numbers."""
    count = 0
    for spec_key, spec_config in SPECS.items():
        url = spec_config["url"]
        version = spec_config["version"]
        print(f"  Fetching {spec_key} ({version})...")

        try:
            raw = fetch_html_as_markdown(url)
        except Exception as e:
            print(f"  ✗  {spec_key}: fetch failed — {e}")
            continue

        for skill_name, skill_config in spec_config["skills"].items():
            sections = skill_config["section_numbers"]
            parts = []

            for section_num in sections:
                patterns = [
                    rf"^## {re.escape(section_num)}[\.\s]",
                    rf"^## {re.escape(section_num)}\.",
                    rf"^# {re.escape(section_num)}[\.\s]",
                    rf"^### {re.escape(section_num)}[\.\s]",
                ]
                content = extract_section(raw, patterns)
                if content.strip():
                    parts.append(content)

            if not parts:
                print(f"  ✗  {skill_name}: no content matched")
                continue

            combined = "\n\n---\n\n".join(parts)
            write_skill(
                skill_dir=OUTPUT_BASE / skill_name,
                name=skill_name,
                description=skill_config["description"],
                content=combined,
                version=version,
            )
            count += 1

    return count


def generate_w3c_skills() -> int:
    """Generate skills from W3C specs using section-based splitting."""
    count = 0
    for spec_key, spec_config in W3C_SPECS.items():
        url = spec_config["url"]
        version = spec_config["version"]
        print(f"  Fetching {spec_key} ({version})...")

        try:
            raw = fetch_html_as_markdown(url)
        except Exception as e:
            print(f"  ✗  {spec_key}: fetch failed — {e}")
            continue

        for skill_name, skill_config in spec_config["skills"].items():
            sections = skill_config["section_numbers"]
            parts = []

            for section_num in sections:
                patterns = [
                    rf"^## {re.escape(section_num)}[\.\s]",
                    rf"^## {re.escape(section_num)}\s*$",
                    rf"^## {re.escape(section_num)}\.",
                    rf"^# {re.escape(section_num)}[\.\s]",
                    rf"^### {re.escape(section_num)}[\.\s]",
                ]
                content = extract_section(raw, patterns)
                if content.strip():
                    parts.append(content)

            if not parts:
                # Fall back to whole content if no sections matched
                if len(spec_config["skills"]) == 1:
                    parts = [raw]
                else:
                    print(f"  ✗  {skill_name}: no content matched")
                    continue

            combined = "\n\n---\n\n".join(parts)
            write_skill(
                skill_dir=OUTPUT_BASE / skill_name,
                name=skill_name,
                description=skill_config["description"],
                content=combined,
                version=version,
            )
            count += 1

    return count


def main() -> None:
    print("\n── EUDI Knowledge: External Specs ─────────────────────────────")

    print("\n── Generating IETF/OIDF spec skills ──────────────────────────")
    section_count = generate_section_based_skills()

    print("\n── Generating W3C spec skills ─────────────────────────────────")
    w3c_count = generate_w3c_skills()

    total = section_count + w3c_count
    print(f"\n  Done: {total} external spec skills written")


if __name__ == "__main__":
    main()
