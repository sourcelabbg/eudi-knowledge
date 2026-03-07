"""
split_arf_topics.py — Fetch ARF discussion topic papers and generate one skill per topic.

Each discussion topic (A through X, plus AA) is a standalone markdown file
in the ARF repository. Skills are named arf-topic-<letter>-<slug>.

Usage: python scripts/split_arf_topics.py
"""

# pyright: reportImplicitStringConcatenation=false

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import (  # pyright: ignore[reportImplicitRelativeImport]
    ARF_REPO_RAW,
    OUTPUT_BASE,
    TOKEN_WARN,
    clean_skills_with_prefix,
    count_tokens,
    extract_all_sections_at_level,
    fetch_markdown,
    get_arf_version,
    slugify,
    write_skill,
)

TOPICS_BASE = f"{ARF_REPO_RAW}/discussion-topics"

# Each entry: (filename, letter, short_title, description)
DISCUSSION_TOPICS = [
    (
        "a-privacy-risks-and-mitigations.md",
        "a",
        "Privacy Risks and Mitigations",
        "Use when assessing privacy risks in the EUDI Wallet ecosystem. "
        "Covers privacy risk analysis, tracking risks, profiling risks, "
        "and mitigation strategies.",
    ),
    (
        "b-re-issuance-and-batch-issuance-of-pids-and-attestations.md",
        "b",
        "Re-issuance and Batch Issuance",
        "Use when implementing PID/attestation re-issuance or batch "
        "issuance. Covers issuance triggers, batch strategies, and "
        "validity management.",
    ),
    (
        "c-wallet-unit-attestation.md",
        "c",
        "Wallet Unit Attestation",
        "Use when implementing Wallet Unit Attestation (WUA) or Wallet "
        "Instance Attestation (WIA). Covers WUA lifecycle, formats, "
        "key attestation, and WSCD binding.",
    ),
    (
        "d-embedded-disclosure-policies.md",
        "d",
        "Embedded Disclosure Policies",
        "Use when implementing embedded disclosure policies for "
        "attestations. Covers policy formats, enforcement, and "
        "attribute-level disclosure control.",
    ),
    (
        "e-pseudonyms-including-user-authentication-mechanism.md",
        "e",
        "Pseudonyms and User Authentication",
        "Use when implementing pseudonyms or user authentication "
        "mechanisms. Covers verifiable pseudonyms, attested pseudonyms, "
        "scope-rate-limited pseudonyms, and ZKP-based approaches.",
    ),
    (
        "f-digital-credential-api.md",
        "f",
        "Digital Credential API",
        "Use when integrating EUDI Wallet with the W3C Digital "
        "Credentials API. Covers browser integration, DC API flow, "
        "CTAP-Hybrid, and security considerations.",
    ),
    (
        "g-zero-knowledge-proof.md",
        "g",
        "Zero Knowledge Proof",
        "Use when evaluating ZKP technologies for EUDI Wallet. Covers "
        "ZKP use cases (selective disclosure, predicate proofs, "
        "unlinkability), candidate schemes, and integration approaches.",
    ),
    (
        "h-transaction-logs-kept-by-the-wallet.md",
        "h",
        "Transaction Logs",
        "Use when implementing transaction logging in the Wallet Unit. "
        "Covers log content, retention, access control, and privacy "
        "requirements for wallet transaction records.",
    ),
    (
        "i-natural-person-representing-another-natural-person.md",
        "i",
        "Person Representing Another Person",
        "Use when implementing delegation or representation scenarios "
        "where a natural person acts on behalf of another natural person "
        "using the EUDI Wallet.",
    ),
    (
        "j-wallet-to-wallet-interactions.md",
        "j",
        "Wallet-to-Wallet Interactions",
        "Use when implementing peer-to-peer attestation exchange between "
        "Wallet Units. Covers wallet-to-wallet flows, trust models, "
        "and protocol requirements.",
    ),
    (
        "k-combined-presentation-of-attestations.md",
        "k",
        "Combined Presentation of Attestations",
        "Use when implementing combined presentation of multiple "
        "attestations in a single transaction. Covers binding mechanisms, "
        "session linking, and multi-attestation verification.",
    ),
    (
        "l+m-data-deletion-and-reporting-of-wrp-to-dpa.md",
        "lm",
        "Data Deletion and WRP Reporting to DPA",
        "Use when implementing data deletion requests or wrongful request "
        "of personal data (WRP) reporting. Covers deletion interfaces, "
        "DPA reporting mechanisms, and compliance requirements.",
    ),
    (
        "n-export-and-data-portability.md",
        "n",
        "Export and Data Portability",
        "Use when implementing data export or portability features in "
        "the Wallet. Covers export formats, portability rights, and "
        "wallet migration scenarios.",
    ),
    (
        "o-catalogues-for-attestations.md",
        "o",
        "Catalogues for Attestations",
        "Use when implementing attestation catalogues. Covers catalogue "
        "structure, attribute schemas, attestation type discovery, and "
        "provider information.",
    ),
    (
        "p-secure-cryptographic-interface-between-the-Wallet-Instance-and-WSCA.md",
        "p",
        "Secure Cryptographic Interface (Wallet-WSCA)",
        "Use when implementing the interface between Wallet Instance and "
        "WSCA. Covers cryptographic operations, key management, and "
        "secure communication channel requirements.",
    ),
    (
        "q-interface-user-wallet-instance.md",
        "q",
        "User-Wallet Instance Interface",
        "Use when designing the user interface layer of the Wallet "
        "Instance. Covers interaction patterns, user consent flows, "
        "and accessibility requirements.",
    ),
    (
        "r-authentication-of-user-to-device.md",
        "r",
        "User-to-Device Authentication",
        "Use when implementing user authentication to the device and "
        "Wallet. Covers biometrics, PIN, device binding, and WSCD "
        "authentication mechanisms.",
    ),
    (
        "s-certificate-transparancy.md",
        "s",
        "Certificate Transparency",
        "Use when implementing or evaluating certificate transparency "
        "for the EUDI ecosystem. Covers CT logs, monitoring, and "
        "compliance requirements for access certificates.",
    ),
    (
        "t-support-and-maintenance-by-the-wallet-provider.md",
        "t",
        "Support and Maintenance by Wallet Provider",
        "Use when defining Wallet Provider support obligations. Covers "
        "maintenance requirements, update mechanisms, incident response, "
        "and User support channels.",
    ),
    (
        "u-eudi-wallet-trust-mark.md",
        "u",
        "EUDI Wallet Trust Mark",
        "Use when implementing the EUDI Wallet trust mark. Covers trust "
        "mark design, usage requirements, verification, and display "
        "guidelines.",
    ),
    (
        "v-pid-rulebook.md",
        "v",
        "PID Rulebook Discussion",
        "Use when working with PID Rulebook design decisions. Covers "
        "PID attribute selection, encoding choices, namespace design, "
        "and format-specific considerations.",
    ),
    (
        "w-transactional-data-for-payments-and-other-use-cases.md",
        "w",
        "Transactional Data for Payments",
        "Use when implementing transaction data signing or payment SCA "
        "with the EUDI Wallet. Covers transaction data binding, payment "
        "flows, and PSD2/PSD3 integration.",
    ),
    (
        "x-relying-party-registration.md",
        "x",
        "Relying Party Registration",
        "Use when implementing RP registration and access certificate "
        "management. Covers registration workflows, certificate issuance, "
        "attribute disclosure policies, and RP trust framework.",
    ),
    (
        "aa-support-of-electronic-payments-SCA-with-wallet.md",
        "aa",
        "Electronic Payments SCA with Wallet",
        "Use when implementing Strong Customer Authentication (SCA) for "
        "electronic payments using the EUDI Wallet. Covers PSD2/PSD3 "
        "compliance, payment attestation flows, and PSP integration.",
    ),
]


def main() -> None:
    print("\n── EUDI Knowledge: ARF Discussion Topics ─────────────────────")
    version = get_arf_version()
    print(f"  Latest ARF release: {version}")

    print("\n── Generating discussion topic skills ────────────────────────")
    count = 0
    for filename, letter, title, description in DISCUSSION_TOPICS:
        url = f"{TOPICS_BASE}/{filename}"
        skill_name = f"arf-topic-{letter}-{slugify(title)[:30]}"

        try:
            content = fetch_markdown(url)
        except Exception as e:
            print(f"  ✗  {skill_name}: fetch failed — {e}")
            continue

        if not content.strip():
            print(f"  ✗  {skill_name}: empty content")
            continue

        clean_skills_with_prefix(skill_name)

        tokens = count_tokens(content)
        if tokens <= TOKEN_WARN:
            write_skill(
                OUTPUT_BASE / skill_name,
                skill_name,
                description,
                content,
                version,
            )
            count += 1
            continue

        sections = extract_all_sections_at_level(content, 2)
        if not sections:
            write_skill(
                OUTPUT_BASE / skill_name,
                skill_name,
                description,
                content,
                version,
            )
            count += 1
            continue

        groups: list[list[tuple[str, str]]] = []
        current_group: list[tuple[str, str]] = []
        current_tokens = 0
        split_budget = 7_500

        for heading, section_content in sections:
            section_tokens = count_tokens(section_content)
            if current_group and current_tokens + section_tokens > split_budget:
                groups.append(current_group)
                current_group = [(heading, section_content)]
                current_tokens = section_tokens
            else:
                current_group.append((heading, section_content))
                current_tokens += section_tokens

        if current_group:
            groups.append(current_group)

        first_heading_match = re.search(r"^## ", content, flags=re.MULTILINE)
        preamble = ""
        if first_heading_match:
            preamble = content[: first_heading_match.start()].strip()

        for part_num, group in enumerate(groups, 1):
            part_content = "\n\n".join(section_content for _, section_content in group)
            if part_num == 1 and preamble:
                part_content = f"{preamble}\n\n{part_content}"

            section_titles = [heading for heading, _ in group]
            listed_titles = ", ".join(section_titles[:3])
            suffix = " ..." if len(section_titles) > 3 else ""
            part_description = (
                f"{description} Part {part_num}: covers {listed_titles}{suffix}."
            )
            part_skill_name = f"{skill_name}-part-{part_num}"

            write_skill(
                OUTPUT_BASE / part_skill_name,
                part_skill_name,
                part_description,
                part_content,
                version,
            )
            count += 1

    print(f"\n  Done: {count} discussion topic skills written")


if __name__ == "__main__":
    main()
