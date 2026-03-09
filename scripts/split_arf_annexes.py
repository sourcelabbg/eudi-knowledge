"""
split_arf_annexes.py — Fetch ARF annexes and technical specifications, split into skills.

Covers:
  - Annex 2.01 (HLR intro)
  - Annex 2.02 (HLRs by topic — dynamically split per topic)
  - Annex 5.01 (Design guide)
  - Annex 5.02 (Design guide — data sharing scenarios)
  - Technical Specifications README (standards matrix)

Usage: python scripts/split_arf_annexes.py
"""

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import (
    ARF_REPO_RAW,
    OUTPUT_BASE,
    TOKEN_WARN,
    count_tokens,
    extract_all_sections_at_level,
    fetch_markdown,
    get_arf_version,
    slugify,
    write_skill,
)

# ── URLs ───────────────────────────────────────────────────────────────────

ANNEX_2_01_URL = f"{ARF_REPO_RAW}/annexes/annex-2/annex-2.01-high-level-requirements.md"
ANNEX_2_02_URL = (
    f"{ARF_REPO_RAW}/annexes/annex-2/annex-2.02-high-level-requirements-by-topic.md"
)
ANNEX_5_01_URL = f"{ARF_REPO_RAW}/annexes/annex-5/annex-5.01-design-guide.md"
ANNEX_5_02_URL = (
    f"{ARF_REPO_RAW}/annexes/annex-5/annex-5.02-design-guide-data-sharing-scenarios.md"
)
TS_README_URL = f"{ARF_REPO_RAW}/technical-specifications/README.md"
RULEBOOK_REPO_RAW = (
    "https://raw.githubusercontent.com/eu-digital-identity-wallet/"
    "eudi-doc-attestation-rulebooks-catalog/main/rulebooks"
)
ANNEX_3_01_URL = f"{RULEBOOK_REPO_RAW}/pid/pid-rulebook.md"
ANNEX_3_02_URL = f"{RULEBOOK_REPO_RAW}/mdl/mdl-rulebook.md"

# ── Static skills (whole-file, single skill each) ─────────────────────────

STATIC_SKILLS = {
    "arf-hlr-intro": {
        "url": ANNEX_2_01_URL,
        "description": (
            "Use when needing an overview of ARF high-level requirements "
            "structure, key words (SHALL/SHOULD/MAY), and how HLRs are "
            "organized by topic and category."
        ),
    },
    "arf-design-guide": {
        "url": ANNEX_5_01_URL,
        "description": (
            "Use when implementing EUDI Wallet UI/UX. Covers design "
            "principles, visual identity, accessibility requirements, and "
            "user interface guidelines for Wallet Solutions."
        ),
    },
    "arf-design-data-sharing": {
        "url": ANNEX_5_02_URL,
        "description": (
            "Use when designing data sharing user flows in EUDI Wallet "
            "applications. Covers scenarios for sharing PID and attestation "
            "data with Relying Parties."
        ),
    },
    "arf-annex3-pid-rulebook": {
        "url": ANNEX_3_01_URL,
        "description": (
            "Use when working with the PID Rulebook. Covers PID attribute "
            "schemas, mdoc and SD-JWT VC encoding, trust anchors, revocation, "
            "and compliance requirements."
        ),
        "no_split": True,
    },
    "arf-annex3-mdl-rulebook": {
        "url": ANNEX_3_02_URL,
        "description": (
            "Use when working with the mDL Rulebook. Covers mDL attribute "
            "schema and ISO 18013-5 encoding for mobile driving licences."
        ),
    },
    "arf-standards-matrix": {
        "url": TS_README_URL,
        "description": (
            "Use when looking up which technical standards apply to EUDI "
            "ecosystem actors. Contains the complete matrix of ~40 essential "
            "standards mapped to CIR articles, organized by actor (Wallet "
            "Providers, Member States, Attestation Providers, Relying Parties)."
        ),
        "split_at_heading": "## Technical Specifications",
        "description_part1": (
            "Use when looking up which technical standards apply to EUDI "
            "ecosystem actors. Contains the matrix of essential standards "
            "mapped to CIR articles, organized by actor (Wallet Providers, "
            "Member States, Attestation Providers, Relying Parties)."
        ),
        "description_part2": (
            "Use when looking up EUDI technical specification details. "
            "Contains the list of technical specifications referenced by "
            "the standards matrix with descriptions and status."
        ),
    },
}


def generate_static_skills(version: str) -> int:
    """Generate skills from whole-file annex sources. Returns count."""
    count = 0
    for skill_name, config in STATIC_SKILLS.items():
        try:
            content = fetch_markdown(config["url"])
        except Exception as e:
            print(f"  ✗  {skill_name}: fetch failed — {e}")
            continue
        if not content.strip():
            print(f"  ✗  {skill_name}: empty content")
            continue

        split_at_heading = config.get("split_at_heading")
        if split_at_heading:
            heading_pattern = re.compile(
                rf"^{re.escape(split_at_heading)}$", re.MULTILINE
            )
            match = heading_pattern.search(content)
            if match:
                part1_content = content[: match.start()].strip()
                part2_content = content[match.start() :].strip()
                if part1_content and part2_content:
                    write_skill(
                        OUTPUT_BASE / f"{skill_name}-part-1",
                        f"{skill_name}-part-1",
                        config.get("description_part1", config["description"]),
                        part1_content,
                        version,
                    )
                    write_skill(
                        OUTPUT_BASE / f"{skill_name}-part-2",
                        f"{skill_name}-part-2",
                        config.get("description_part2", config["description"]),
                        part2_content,
                        version,
                    )
                    count += 2
                    continue

        tokens = count_tokens(content)
        if tokens <= TOKEN_WARN or config.get("no_split"):
            write_skill(
                OUTPUT_BASE / skill_name,
                skill_name,
                config["description"],
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
                config["description"],
                content,
                version,
            )
            count += 1
            continue

        groups: list[list[tuple[str, str]]] = []
        current_group: list[tuple[str, str]] = []
        current_tokens = 0

        first_heading_match = re.search(r"^## ", content, re.MULTILINE)
        preamble = (
            content[: first_heading_match.start()].strip()
            if first_heading_match
            else ""
        )

        for heading, section_content in sections:
            section_tokens = count_tokens(section_content)
            if current_group and current_tokens + section_tokens > 7500:
                groups.append(current_group)
                current_group = [(heading, section_content)]
                current_tokens = section_tokens
            else:
                current_group.append((heading, section_content))
                current_tokens += section_tokens

        if current_group:
            groups.append(current_group)

        for part_num, group in enumerate(groups, 1):
            part_content = "\n\n".join(section_content for _, section_content in group)
            if part_num == 1 and preamble:
                part_content = preamble + "\n\n" + part_content

            part_skill_name = f"{skill_name}-part-{part_num}"
            section_titles = [heading for heading, _ in group]
            part_desc = (
                f"{config['description']} Part {part_num}: "
                f"covers {', '.join(section_titles[:3])}."
            )

            write_skill(
                OUTPUT_BASE / part_skill_name,
                part_skill_name,
                part_desc,
                part_content,
                version,
            )
            count += 1
    return count


def generate_hlr_topic_skills(version: str) -> int:
    """Fetch Annex 2.02 and split each topic into its own skill. Returns count."""
    print("  Fetching Annex 2.02 (HLRs by topic)...")
    try:
        raw = fetch_markdown(ANNEX_2_02_URL)
    except Exception as e:
        print(f"  ✗  Annex 2.02: fetch failed — {e}")
        return 0

    # Find all topic headings: #### A.2.3.N Topic M - Title
    topic_pattern = re.compile(
        r"^(####) (A\.2\.3\.\d+ )(Topic \d+) - (.+)",
        re.MULTILINE,
    )
    matches = list(topic_pattern.finditer(raw))
    if not matches:
        print("  ✗  Annex 2.02: no topic headings found")
        return 0

    count = 0
    for i, m in enumerate(matches):
        start = m.start()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(raw)
        content = raw[start:end].strip()

        topic_num = m.group(3)  # "Topic 1"
        title = m.group(4).strip()  # "Accessing Online Services with a Wallet Unit"

        # Extract topic number for skill name: "Topic 1" → "01"
        num_match = re.search(r"\d+", topic_num)
        num_str = num_match.group().zfill(2) if num_match else "00"
        title_slug = slugify(title)[:40]  # Truncate long titles
        skill_name = f"hlr-{num_str}-{title_slug}"

        description = (
            f"Use when working with EUDI high-level requirements for "
            f"'{title}'. Contains normative SHALL/SHOULD/MAY requirements "
            f"from ARF Annex 2."
        )

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

        sections = extract_all_sections_at_level(content, 5)
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

        first_section_start = content.find("\n#####")
        preamble = (
            content[:first_section_start].strip() if first_section_start > 0 else ""
        )

        for heading, section_content in sections:
            section_tokens = count_tokens(section_content)
            if current_group and current_tokens + section_tokens > 7500:
                groups.append(current_group)
                current_group = [(heading, section_content)]
                current_tokens = section_tokens
            else:
                current_group.append((heading, section_content))
                current_tokens += section_tokens

        if current_group:
            groups.append(current_group)

        for part_num, group in enumerate(groups, 1):
            part_content = "\n\n".join(section_content for _, section_content in group)
            if part_num == 1 and preamble:
                part_content = preamble + "\n\n" + part_content

            part_skill_name = f"{skill_name}-part-{part_num}"
            part_desc = (
                f"Use when working with EUDI high-level requirements for "
                f"'{title}' (Part {part_num}). Contains normative requirements "
                f"from ARF Annex 2."
            )

            write_skill(
                OUTPUT_BASE / part_skill_name,
                part_skill_name,
                part_desc,
                part_content,
                version,
            )
            count += 1

    return count


def main() -> None:
    print("\n── EUDI Knowledge: ARF Annexes & Tech Specs ──────────────────")
    version = get_arf_version()
    print(f"  Latest ARF release: {version}")

    print("\n── Generating annex skills ────────────────────────────────────")
    static_count = generate_static_skills(version)
    hlr_count = generate_hlr_topic_skills(version)

    total = static_count + hlr_count
    print(f"\n  Done: {total} annex/TS skills written")


if __name__ == "__main__":
    main()
