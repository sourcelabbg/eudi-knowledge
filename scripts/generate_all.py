"""
generate_all.py — Run all EUDI knowledge skill generators.

This is the single entry point for generating all skills. It cleans
the output directory and then runs each splitter in sequence.

Usage: python scripts/generate_all.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import OUTPUT_BASE, clean_old_skills

import split_arf
import split_oid4vp
import split_arf_annexes
import split_arf_topics
import split_oid4vci
import split_external
import split_mattr_mdoc
import split_sd_jwt_quickstart


def main() -> None:
    print("╔══════════════════════════════════════════════════════════════╗")
    print("║          EUDI Knowledge — Full Skill Generation            ║")
    print("╚══════════════════════════════════════════════════════════════╝")

    # Clean all existing skills before regeneration
    clean_old_skills(OUTPUT_BASE)

    # Run each generator
    split_arf.main()
    split_oid4vp.main()
    split_arf_annexes.main()
    split_arf_topics.main()
    split_oid4vci.main()
    split_external.main()
    split_mattr_mdoc.main()
    split_sd_jwt_quickstart.main()

    # Final summary
    all_skills = list(OUTPUT_BASE.glob("*/SKILL.md"))
    print("\n╔══════════════════════════════════════════════════════════════╗")
    print(f"║  Total: {len(all_skills)} skills written to {OUTPUT_BASE}/")
    print("╚══════════════════════════════════════════════════════════════╝\n")


if __name__ == "__main__":
    main()
