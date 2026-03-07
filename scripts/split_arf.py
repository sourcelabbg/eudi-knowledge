"""
split_arf.py — Fetch the latest ARF main document and split it into OpenCode SKILL.md files.
Usage: python scripts/split_arf.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import requests
from common import (
    ARF_REPO_RAW,
    OUTPUT_BASE,
    fetch_markdown,
    extract_section,
    get_arf_version,
    write_skill,
    clean_old_skills,
)

ARF_MAIN_URL = f"{ARF_REPO_RAW}/architecture-and-reference-framework-main.md"
ARF_ANNEX1_URL = f"{ARF_REPO_RAW}/annexes/annex-1/annex-1-definitions.md"

SKILLS = {
    "arf-glossary": {
        "url": ARF_ANNEX1_URL,
        "description": (
            "Use when the meaning of a specific EUDI/ARF term or acronym is "
            "unclear. Contains all ARF definitions: PID, QEAA, PuB-EAA, WUA, "
            "WSCD, WSCA, LoTE, CAB, Relying Party, Wallet Unit."
        ),
    },
    "arf-ecosystem-roles": {
        "patterns": [r"^## 3[\. ]"],
        "description": (
            "Use when discussing who does what in the EUDI ecosystem: Wallet "
            "Provider, PID Provider, QEAA Provider, PuB-EAA Provider, EAA "
            "Provider, Relying Party, CAB, Trust List Provider, Access "
            "Certificate Authority."
        ),
    },
    "arf-architecture": {
        "patterns": [r"^### 4\.1 ", r"^### 4\.2 ", r"^### 4\.3 "],
        "description": (
            "Use when designing wallet components, understanding EUDI design "
            "principles (user-centricity, interoperability, privacy/security "
            "by design), or working with the reference architecture, its "
            "components, and interfaces."
        ),
    },
    "arf-wscd-states": {
        "patterns": [r"^### 4\.5 ", r"^### 4\.6 ", r"^### 4\.7 "],
        "description": (
            "Use when selecting WSCD architecture types "
            "(remote/local-external/local-internal/local-native/hybrid), "
            "working with state lifecycles for Wallet Providers/Solutions/"
            "Units/Providers/Attestations, or implementing pseudonym types "
            "(verifiable, attested, scope rate-limited)."
        ),
    },
    "arf-presentation-flows": {
        "patterns": [r"^### 4\.4 ", r"^### 5\.6 "],
        "join": True,
        "description": (
            "Use when implementing presentation flows, OpenID4VP integration, "
            "verifier endpoints, or proximity flows. Covers same-device/"
            "cross-device remote presentation, BLE/NFC proximity, OID4VP "
            "profiling, DC API."
        ),
    },
    "arf-data-model": {
        "patterns": [r"^## 5[\. ]"],
        "description": (
            "Use when working with credential formats (ISO/IEC 18013-5 mdoc, "
            "SD-JWT VC, W3C VCDM), attestation categories (PID, QEAA, "
            "PuB-EAA, EAA), attestation rulebooks, or attribute schemas."
        ),
    },
    "arf-trust-model": {
        "patterns": [r"^### 6\.1 ", r"^### 6\.2 ", r"^### 6\.3 ", r"^### 6\.4 "],
        "description": (
            "Use when understanding the EUDI trust framework, provider "
            "registration, and lifecycle management for Wallet Providers, PID "
            "Providers, Attestation Providers, and Relying Parties."
        ),
    },
    "arf-wallet-lifecycle-install": {
        "patterns": [r"^#### 6\.5\.1 ", r"^#### 6\.5\.2 ", r"^#### 6\.5\.3 "],
        "join": True,
        "description": (
            "Use when implementing Wallet Unit lifecycle: overview, "
            "installation (trust relationships, authenticity verification, "
            "Wallet Solution validation), and activation (device data "
            "collection, user authentication setup, WUA/WIA issuance)."
        ),
    },
    "arf-wallet-lifecycle-mgmt": {
        "patterns": [r"^#### 6\.5\.4 ", r"^#### 6\.5\.5 "],
        "join": True,
        "description": (
            "Use when implementing Wallet Unit management and uninstallation. "
            "Covers: Wallet Unit revocation, migrating PIDs and attestations "
            "to a different Wallet Solution, and Wallet Instance uninstallation."
        ),
    },
    "arf-issuance-reqs": {
        "patterns": [r"^#### 6\.6\.1 ", r"^#### 6\.6\.2 "],
        "description": (
            "Use when implementing PID or attestation issuance, including "
            "lifecycle states, batch issuance, key binding, and trust "
            "requirements between issuers and wallet units."
        ),
    },
    "arf-presentation-reqs": {
        "patterns": [
            r"^##### 6\.6\.3\.1 ",
            r"^##### 6\.6\.3\.2 ",
            r"^##### 6\.6\.3\.3 ",
            r"^##### 6\.6\.3\.4 ",
            r"^##### 6\.6\.3\.5 ",
        ],
        "description": (
            "Use when implementing wallet-side presentation trust: Relying "
            "Party authentication, attribute request verification, embedded "
            "disclosure policy evaluation, and user approval flows."
        ),
    },
    "arf-rp-verification": {
        "patterns": [r"^##### 6\.6\.3\.([6-9]|1[0-3]) "],
        "description": (
            "Use when implementing RP-side verification during attestation "
            "presentation: authenticity checks, revocation verification, "
            "device binding, user binding, combined presentation, and "
            "suspicious request reporting."
        ),
    },
    "arf-attestation-mgmt": {
        "patterns": [
            r"^#### 6\.6\.4 ",
            r"^#### 6\.6\.5 ",
            r"^#### 6\.6\.6 ",
            r"^#### 6\.6\.7 ",
        ],
        "description": (
            "Use when implementing attestation presentation to other Wallet "
            "Units or intermediaries, attestation management (refresh, status "
            "checks), and attestation deletion."
        ),
    },
    "arf-wallet-reqs": {
        "patterns": [r"^## 7[\. ]"],
        "description": (
            "Use when reviewing Wallet Solution certification requirements, "
            "conformity assessment, CSA-based certification schemes, or risk "
            "management for Wallet Solutions."
        ),
    },
}


def fetch_arf() -> str:
    print("  Fetching ARF from GitHub...")
    r = requests.get(ARF_MAIN_URL, timeout=30)
    r.raise_for_status()
    return r.text


def main() -> None:
    print("\n── EUDI Knowledge: ARF Main Document ────────────────────────")
    version = get_arf_version()
    print(f"  Latest ARF release: {version}")
    raw = fetch_arf()
    output_base = OUTPUT_BASE

    print("\n── Generating ARF skills ──────────────────────────────────────")
    for skill_name, config in SKILLS.items():
        if "url" in config:
            try:
                content = fetch_markdown(config["url"])
            except Exception as e:
                print(f"  ✗  {skill_name}: fetch failed — {e}")
                continue
        elif config.get("join"):
            parts = [extract_section(raw, [p]) for p in config["patterns"]]
            content = "\n\n---\n\n".join(p for p in parts if p.strip())
        else:
            content = extract_section(raw, config["patterns"])

        if not content.strip():
            print(f"  ✗  {skill_name}: no content matched")
            continue
        write_skill(
            output_base / skill_name,
            skill_name,
            config["description"],
            content,
            version,
        )

    skills_written = list(output_base.glob("arf-*/SKILL.md"))
    print(f"\n  Done: {len(skills_written)} ARF skills written")


if __name__ == "__main__":
    main()
