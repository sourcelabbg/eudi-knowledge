"""
split_oid4vp.py — Fetch OpenID4VP 1.0 Final spec and split into OpenCode SKILL.md files.
Usage: python scripts/split_oid4vp.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import re
from common import OUTPUT_BASE, fetch_html_as_markdown, extract_section, write_skill

OID4VP_URL = "https://openid.net/specs/openid-4-verifiable-presentations-1_0.html"
OID4VP_VERSION = "1.0-final-2025-07-09"

OID4VP_SKILLS = {
    "oid4vp-overview": {
        "section_numbers": ["1", "2", "3"],
        "description": (
            "Use when needing an overview of OpenID4VP, its terminology, or the "
            "difference between same-device and cross-device presentation flows. "
            "Covers: Verifier, Wallet, VP Token, vp_token response type, nonce, "
            "authorization request/response model."
        ),
    },
    "oid4vp-authorization-request": {
        "section_numbers": ["4"],
        "description": (
            "Use when constructing or validating an OpenID4VP authorization request. "
            "Covers: request parameters (presentation_definition, dcql_query, nonce, "
            "response_type, response_mode, response_uri, client_id), client_id prefixes "
            "(pre-registered, redirect_uri, did, verifier_attestation, x509_san_dns, "
            "x509_san_uri), request_uri with GET and POST methods, JAR (RFC9101), "
            "Verifier Info and Proof of Possession."
        ),
    },
    "oid4vp-request-uri-jar": {
        "section_numbers": ["5.7", "5.8", "5.9", "5.10", "5.11"],
        "description": (
            "Use when implementing request_uri or JWT-Secured Authorization Requests "
            "(JAR) for OpenID4VP. Covers: request_uri parameter, request_uri methods "
            "(GET and POST), signed request objects, and request parameter passing."
        ),
    },
    "oid4vp-dcql": {
        "section_numbers": ["6", "7"],
        "description": (
            "Use when writing or parsing DCQL (Digital Credentials Query Language) queries. "
            "Covers: credential queries, credential set queries, claims queries, "
            "trusted_authorities, claims path pointers for JSON and mdoc credentials, "
            "credential selection logic, and DCQL examples."
        ),
    },
    "oid4vp-response": {
        "section_numbers": ["8"],
        "description": (
            "Use when handling or validating an OpenID4VP response. Covers: vp_token "
            "structure, presentation_submission, response modes (fragment, direct_post, "
            "direct_post.jwt), encrypted responses, transaction data, error responses, "
            "and VP Token validation rules."
        ),
    },
    "oid4vp-metadata": {
        "section_numbers": ["9", "10", "11", "12"],
        "description": (
            "Use when configuring wallet or verifier metadata, wallet invocation schemes "
            "(openid4vp://, universal links, DC API), or implementing Verifier Attestation JWTs. "
            "Covers: authorization_server metadata, vp_formats_supported, "
            "client_metadata parameters, and verifier_attestation JWT format."
        ),
    },
    "oid4vp-security": {
        "section_numbers": ["13", "14", "15"],
        "description": (
            "Use when reviewing security or privacy requirements for an OpenID4VP "
            "implementation. Covers: replay prevention, nonce binding, session fixation, "
            "direct_post response URI validation, TLS requirements, selective disclosure "
            "privacy, verifier-to-verifier unlinkability, and conformance testing guidance."
        ),
    },
    "oid4vp-dc-api": {
        "section_numbers": ["appendix-A", "Appendix A"],
        "description": (
            "Use when implementing OpenID4VP over the W3C Digital Credentials API (DC API) "
            "in a browser context. Covers: DC API protocol flow, request/response format, "
            "signed and unsigned requests, security and privacy considerations specific "
            "to the browser-based flow."
        ),
    },
    "oid4vp-format-w3c-vc": {
        "section_numbers": ["appendix-B.1", "Appendix B.1", "B.1"],
        "description": (
            "Use when implementing W3C Verifiable Credentials format in OpenID4VP. "
            "Covers: W3C VC format params, claims matching, presentation response "
            "structure, and transaction data for W3C VCs."
        ),
    },
    "oid4vp-format-mdoc": {
        "section_numbers": ["appendix-B.2", "Appendix B.2", "B.2"],
        "description": (
            "Use when implementing ISO mdoc (ISO 18013/23220) format in OpenID4VP. "
            "Covers: mdoc DeviceResponse, Handover, SessionTranscript computation, "
            "and mdoc-specific presentation rules."
        ),
    },
    "oid4vp-format-sd-jwt-vc": {
        "section_numbers": ["appendix-B.3", "Appendix B.3", "B.3"],
        "description": (
            "Use when implementing IETF SD-JWT VC format in OpenID4VP. "
            "Covers: SD-JWT VC format identifier, presentation response structure, "
            "key binding JWT, and transaction data for SD-JWT VCs."
        ),
    },
}


def main() -> None:
    print("\n── EUDI Knowledge: OpenID4VP ──────────────────────────────────")
    print("  Fetching OpenID4VP 1.0 spec...")
    raw = fetch_html_as_markdown(OID4VP_URL)
    output_base = OUTPUT_BASE

    for skill_name, config in OID4VP_SKILLS.items():
        sections = config["section_numbers"]
        parts = []

        for section_num in sections:
            patterns = [
                rf"^## {re.escape(section_num)}[\.\s]",
                rf"^## {re.escape(section_num)}\.",
                rf"^### {re.escape(section_num)}[\.\s]",
                rf"^### {re.escape(section_num)}\.",
                rf"^# {re.escape(section_num)}[\.\s]",
            ]
            content = extract_section(raw, patterns)
            if content.strip():
                parts.append(content)

        if not parts:
            print(
                f"  ✗  {skill_name}: no content matched — may need to adjust patterns"
            )
            continue

        combined = "\n\n---\n\n".join(parts)
        write_skill(
            skill_dir=output_base / skill_name,
            name=skill_name,
            description=config["description"],
            content=combined,
            version=OID4VP_VERSION,
        )

    skills_written = list(output_base.glob("oid4vp-*/SKILL.md"))
    print(f"\n  Done: {len(skills_written)} OID4VP skills written")


if __name__ == "__main__":
    main()
