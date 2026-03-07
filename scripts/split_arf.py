"""
split_arf.py — Fetch the latest ARF and split it into OpenCode SKILL.md files.
Usage: python scripts/split_arf.py
"""

import re
import shutil
import tiktoken
import requests
from pathlib import Path

ARF_MAIN_URL = (
    "https://raw.githubusercontent.com/eu-digital-identity-wallet/"
    "eudi-doc-architecture-and-reference-framework/main/docs/"
    "architecture-and-reference-framework-main.md"
)
ARF_ANNEX1_URL = (
    "https://raw.githubusercontent.com/eu-digital-identity-wallet/"
    "eudi-doc-architecture-and-reference-framework/main/docs/"
    "annexes/annex-1/annex-1-definitions.md"
)
ARF_RELEASES_API = (
    "https://api.github.com/repos/eu-digital-identity-wallet/"
    "eudi-doc-architecture-and-reference-framework/releases/latest"
)

OID4VP_URL = "https://openid.net/specs/openid-4-verifiable-presentations-1_0.html"
OID4VP_VERSION = "1.0-final-2025-07-09"

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
    "arf-wallet-lifecycle": {
        "patterns": [r"^### 6\.5 "],
        "description": (
            "Use when implementing Wallet Unit lifecycle: installation, "
            "activation (device data collection, user authentication setup, "
            "WUA/WIA issuance), management, and uninstallation."
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

OID4VP_SKILLS = {
    "oid4vp-overview": {
        # Covers §1 Introduction, §2 Terminology, §3 Overview (same/cross device)
        "heading_keywords": ["Introduction", "Terminology", "Overview",
                             "Same Device Flow", "Cross Device Flow"],
        "section_numbers": ["1", "2", "3"],
        "description": (
            "Use when needing an overview of OpenID4VP, its terminology, or the "
            "difference between same-device and cross-device presentation flows. "
            "Covers: Verifier, Wallet, VP Token, vp_token response type, nonce, "
            "authorization request/response model."
        ),
    },
    "oid4vp-authorization-request": {
        # Covers §4 Scope, §5 Authorization Request (all subsections)
        "section_numbers": ["4", "5"],
        "description": (
            "Use when constructing or validating an OpenID4VP authorization request. "
            "Covers: request parameters (presentation_definition, dcql_query, nonce, "
            "response_type, response_mode, response_uri, client_id), client_id prefixes "
            "(pre-registered, redirect_uri, did, verifier_attestation, x509_san_dns, "
            "x509_san_uri), request_uri with GET and POST methods, JAR (RFC9101), "
            "Verifier Info and Proof of Possession."
        ),
    },
    "oid4vp-dcql": {
        # Covers §6 DCQL, §7 Claims Path Pointer
        "section_numbers": ["6", "7"],
        "description": (
            "Use when writing or parsing DCQL (Digital Credentials Query Language) queries. "
            "Covers: credential queries, credential set queries, claims queries, "
            "trusted_authorities, claims path pointers for JSON and mdoc credentials, "
            "credential selection logic, and DCQL examples."
        ),
    },
    "oid4vp-response": {
        # Covers §8 Response
        "section_numbers": ["8"],
        "description": (
            "Use when handling or validating an OpenID4VP response. Covers: vp_token "
            "structure, presentation_submission, response modes (fragment, direct_post, "
            "direct_post.jwt), encrypted responses, transaction data, error responses, "
            "and VP Token validation rules."
        ),
    },
    "oid4vp-metadata": {
        # Covers §9 Wallet Invocation, §10 Wallet Metadata, §11 Verifier Metadata, §12 Verifier Attestation
        "section_numbers": ["9", "10", "11", "12"],
        "description": (
            "Use when configuring wallet or verifier metadata, wallet invocation schemes "
            "(openid4vp://, universal links, DC API), or implementing Verifier Attestation JWTs. "
            "Covers: authorization_server metadata, vp_formats_supported, "
            "client_metadata parameters, and verifier_attestation JWT format."
        ),
    },
    "oid4vp-security": {
        # Covers §13 Implementation Considerations, §14 Security, §15 Privacy
        "section_numbers": ["13", "14", "15"],
        "description": (
            "Use when reviewing security or privacy requirements for an OpenID4VP "
            "implementation. Covers: replay prevention, nonce binding, session fixation, "
            "direct_post response URI validation, TLS requirements, selective disclosure "
            "privacy, verifier-to-verifier unlinkability, and conformance testing guidance."
        ),
    },
    "oid4vp-dc-api": {
        # Covers Appendix A — OpenID4VP over the Digital Credentials API
        "section_numbers": ["appendix-A", "Appendix A"],
        "description": (
            "Use when implementing OpenID4VP over the W3C Digital Credentials API (DC API) "
            "in a browser context. Covers: DC API protocol flow, request/response format, "
            "signed and unsigned requests, security and privacy considerations specific "
            "to the browser-based flow."
        ),
    },
    "oid4vp-credential-formats": {
        # Covers Appendix B — format-specific params for W3C VC, mdoc, SD-JWT VC
        "section_numbers": ["appendix-B", "Appendix B"],
        "description": (
            "Use when implementing credential-format-specific OpenID4VP behaviour. "
            "Covers: W3C VC format params and claims matching, ISO mdoc (ISO 18013/23220) "
            "Handover and SessionTranscript, IETF SD-JWT VC format identifier, "
            "presentation response structures, and transaction data per format."
        ),
    },
}

ENCODER = tiktoken.get_encoding("cl100k_base")
TOKEN_WARN = 8_000


def count_tokens(text: str) -> int:
    return len(ENCODER.encode(text))


def get_arf_version() -> str:
    try:
        r = requests.get(ARF_RELEASES_API, timeout=10)
        if r.ok:
            return r.json().get("tag_name", "unknown")
    except Exception:
        pass
    return "unknown"


def fetch_arf() -> str:
    print("  Fetching ARF from GitHub...")
    r = requests.get(ARF_MAIN_URL, timeout=30)
    r.raise_for_status()
    return r.text


def fetch_annex(url: str) -> str:
    print(f"  Fetching annex from GitHub...")
    r = requests.get(url, timeout=30)
    r.raise_for_status()
    text = r.text
    # Strip YAML frontmatter (--- ... or --- ---) if present
    if text.startswith("---"):
        m = re.search(r"\n(?:---|\.\.\.) *\n", text)
        if m:
            text = text[m.end() :]
    return text.strip()


def fetch_oid4vp() -> str:
    """Fetch OpenID4VP spec HTML and convert to plain text for splitting."""
    print("  Fetching OpenID4VP 1.0 spec...")
    r = requests.get(OID4VP_URL, timeout=30)
    r.raise_for_status()
    r.encoding = 'utf-8'  # Prevent ISO-8859-1 double-encoding of UTF-8 content

    text = r.text

    # Protect <pre> blocks from link conversion
    pre_blocks = []
    def _stash_pre(m):
        pre_blocks.append(m.group(0))
        return f'__PRE_BLOCK_{len(pre_blocks) - 1}__'
    text = re.sub(r'<pre[^>]*>.*?</pre>', _stash_pre, text, flags=re.DOTALL)

    # Remove pilcrow paragraph markers entirely (tag + content)
    text = re.sub(r'<a[^>]*class="[^"]*pilcrow[^"]*"[^>]*>.*?</a>', '', text, flags=re.DOTALL)

    # Remove selfRef navigation links — keep inner HTML for heading converter
    text = re.sub(r'<a[^>]*class="[^"]*selfRef[^"]*"[^>]*>(.*?)</a>', r'\1', text, flags=re.DOTALL)

    # Convert <a href="...">text</a> to markdown [text](url)
    def _link_to_md(m):
        href = m.group(1)
        inner = re.sub(r'<[^>]+>', '', m.group(2)).strip()
        if not inner or not href:
            return inner or ''
        # Expand internal #fragment links to full spec URLs
        if href.startswith('#'):
            href = OID4VP_URL + href
        return f'[{inner}]({href})'
    text = re.sub(r'<a\s+[^>]*href="([^"]*)"[^>]*>(.*?)</a>', _link_to_md, text, flags=re.DOTALL)

    # Convert headings to markdown — strip inner tags and normalize whitespace
    import re as _re
    def _heading(level):
        prefix = '#' * level
        def replacer(m):
            content = _re.sub(r'<[^>]+>', '', m.group(1))
            content = ' '.join(content.split())
            return f'{prefix} {content}'
        return replacer

    text = _re.sub(r'<h1[^>]*>(.*?)</h1>', _heading(1), text, flags=_re.DOTALL)
    text = _re.sub(r'<h2[^>]*>(.*?)</h2>', _heading(2), text, flags=_re.DOTALL)
    text = _re.sub(r'<h3[^>]*>(.*?)</h3>', _heading(3), text, flags=_re.DOTALL)
    text = _re.sub(r'<h4[^>]*>(.*?)</h4>', _heading(4), text, flags=_re.DOTALL)
    text = _re.sub(r'<h5[^>]*>(.*?)</h5>', _heading(5), text, flags=_re.DOTALL)
    text = _re.sub(r'<h6[^>]*>(.*?)</h6>', _heading(6), text, flags=_re.DOTALL)


    # Strip remaining tags
    text = _re.sub(r'<[^>]+>', '', text)

    # Ensure headings start at the beginning of their line
    text = _re.sub(r'^ +(#{1,6} )', r'\1', text, flags=_re.MULTILINE)

    # Decode HTML entities
    import html as _html
    text = _html.unescape(text)

    # Remove any remaining pilcrow characters
    text = re.sub(r'\s*[¶\u00b6]', '', text)

    # Restore <pre> blocks as code fences
    for i, block in enumerate(pre_blocks):
        inner = re.sub(r'<[^>]+>', '', block)
        inner = _html.unescape(inner)
        text = text.replace(f'__PRE_BLOCK_{i}__', f'```\n{inner.strip()}\n```')

    # Collapse excessive blank lines
    text = _re.sub(r'\n{4,}', '\n\n\n', text)

    return text.strip()

def extract_section(text: str, patterns: list) -> str:
    lines = text.split("\n")
    result, collecting, current_depth = [], False, None
    for line in lines:
        if any(re.match(p, line) for p in patterns):
            collecting, current_depth = True, len(line) - len(line.lstrip("#"))
            result.append(line)
            continue
        if collecting:
            m = re.match(r"^(#{1,6}) ", line)
            if m and current_depth is not None and len(m.group(1)) <= current_depth:
                break
            result.append(line)
    return "\n".join(result).strip()


def extract_headings(content: str, max_depth: int = 2) -> list[str]:
    headings = []
    min_depth = None
    for line in content.split("\n"):
        m = re.match(r'^(#{1,6}) (.+)', line)
        if m:
            depth = len(m.group(1))
            if min_depth is None:
                min_depth = depth
            if depth <= (min_depth + max_depth - 1):
                headings.append(m.group(2).strip())
    return headings


def write_skill(
    skill_dir: Path, name: str, description: str, content: str, version: str
) -> None:
    tokens = count_tokens(content)
    is_large = tokens > TOKEN_WARN
    skill_dir.mkdir(parents=True, exist_ok=True)
    headings = extract_headings(content)
    if headings:
        sections_lines = "\n".join(f'  - "{h.replace(chr(34), chr(92)+chr(34))}"' for h in headings)
        sections_block = f"\nsections:\n{sections_lines}"
    else:
        sections_block = ""
    skill_md = f'---\nname: "{name}"\ndescription: "{description}"{sections_block}\n---\n\n<!-- ARF version: {version} -->\n<!-- Tokens: ~{tokens}{"(LARGE)" if is_large else ""} -->\n\n{content}\n'
    (skill_dir / "SKILL.md").write_text(skill_md, encoding="utf-8")
    flag = "⚠" if is_large else "✓"
    print(
        f"  {flag}  {name}: ~{tokens} tokens{'  ← consider splitting' if is_large else ''}"
    )


def clean_old_skills(output_base: Path) -> None:
    if not output_base.exists():
        return
    for d in output_base.iterdir():
        if d.is_dir() and (d / "SKILL.md").exists():
            shutil.rmtree(d)


def generate_oid4vp_skills() -> None:
    """Fetch OpenID4VP spec and write one SKILL.md per defined skill."""
    raw = fetch_oid4vp()
    output_base = Path(".opencode/skills")

    for skill_name, config in OID4VP_SKILLS.items():
        # Find the start of each section by searching for its heading
        # The HTML→markdown conversion produces headings like "## 5.  Authorization Request"
        sections = config["section_numbers"]
        parts = []

        for section_num in sections:
            # Try various heading patterns the spec might produce
            patterns = [
                rf"^## {re.escape(section_num)}[\.\s]",
                rf"^## {re.escape(section_num)}\.",
                rf"^# {re.escape(section_num)}[\.\s]",
            ]
            content = extract_section(raw, patterns)
            if content.strip():
                parts.append(content)

        if not parts:
            print(f"  ✗  {skill_name}: no content matched — may need to adjust patterns")
            continue

        combined = "\n\n---\n\n".join(parts)
        write_skill(
            skill_dir=output_base / skill_name,
            name=skill_name,
            description=config["description"],
            content=combined,
            version=OID4VP_VERSION,
        )


def main() -> None:
    print("\n── EUDI Knowledge: ARF Splitter ──────────────────────────")
    version = get_arf_version()
    print(f"  Latest ARF release: {version}")
    raw = fetch_arf()
    output_base = Path(".opencode/skills")
    clean_old_skills(output_base)
    print("\n── Generating skills ──────────────────────────────────────")

    for skill_name, config in SKILLS.items():
        if "url" in config:
            try:
                content = fetch_annex(config["url"])
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

    print("\n── Generating OpenID4VP skills ────────────────────────────")
    generate_oid4vp_skills()

    skills_written = list(output_base.glob("*/SKILL.md"))
    print(f"\n── Done: {len(skills_written)} skills written to {output_base}/\n")


if __name__ == "__main__":
    main()
