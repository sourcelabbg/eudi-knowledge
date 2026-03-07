# Instructions: Add OpenID4VP 1.0 Spec to the Knowledge Base

Follow these steps exactly to add OpenID for Verifiable Presentations 1.0 as skills.

---

## Context

The OpenID4VP 1.0 spec is a single HTML page at:
https://openid.net/specs/openid-4-verifiable-presentations-1_0.html

Published: 9 July 2025 — Final standard.

The spec has these top-level sections to split into skills:

| Section | Content |
|---|---|
| §1–3 | Introduction, Terminology, Overview (same/cross device flows) |
| §4–5 | Scope, Authorization Request (params, client IDs, request_uri) |
| §6–7 | DCQL — credential queries, claims queries, path pointers |
| §8 | Response (vp_token, direct_post, encryption, VP token validation) |
| §9–11 | Wallet invocation, Wallet metadata, Verifier metadata |
| §12 | Verifier Attestation JWT |
| §13–15 | Implementation, Security, Privacy considerations |
| Appendix A | OpenID4VP over the Digital Credentials API (DC API) |
| Appendix B | Credential format specifics (W3C VC, mdoc, SD-JWT VC) |
| Appendix C | Combining with SIOPv2 |

---

## Step 1 — Add the fetch function to `scripts/split_arf.py`

The existing `fetch_arf()` function fetches a single markdown file. The OpenID4VP spec
is an HTML page and needs to be fetched and converted to plain text differently.

Add this function to `scripts/split_arf.py`:

```python
OID4VP_URL = "https://openid.net/specs/openid-4-verifiable-presentations-1_0.html"
OID4VP_VERSION = "1.0-final-2025-07-09"

def fetch_oid4vp() -> str:
    """Fetch OpenID4VP spec HTML and convert to plain text for splitting."""
    print("  Fetching OpenID4VP 1.0 spec...")
    r = requests.get(OID4VP_URL, timeout=30)
    r.raise_for_status()

    # Strip HTML tags to get clean text while preserving structure.
    # The spec uses <h2>/<h3> for sections — convert them to markdown headings.
    text = r.text

    # Convert headings before stripping tags
    import re as _re
    text = _re.sub(r'<h1[^>]*>(.*?)</h1>', r'# \1', text, flags=_re.DOTALL)
    text = _re.sub(r'<h2[^>]*>(.*?)</h2>', r'## \1', text, flags=_re.DOTALL)
    text = _re.sub(r'<h3[^>]*>(.*?)</h3>', r'### \1', text, flags=_re.DOTALL)
    text = _re.sub(r'<h4[^>]*>(.*?)</h4>', r'#### \1', text, flags=_re.DOTALL)

    # Preserve code blocks
    text = _re.sub(r'<pre[^>]*>(.*?)</pre>', r'```\n\1\n```', text, flags=_re.DOTALL)

    # Strip remaining tags
    text = _re.sub(r'<[^>]+>', '', text)

    # Decode HTML entities
    import html as _html
    text = _html.unescape(text)

    # Collapse excessive blank lines
    text = _re.sub(r'\n{4,}', '\n\n\n', text)

    return text.strip()
```

---

## Step 2 — Define the OpenID4VP skills

Add this dict to `scripts/split_arf.py` alongside `SKILLS`:

```python
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
```

---

## Step 3 — Add a `generate_oid4vp_skills()` function

Add this function to `scripts/split_arf.py`:

```python
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
```

---

## Step 4 — Call it from `main()`

In the `main()` function of `scripts/split_arf.py`, add after the ARF skills block:

```python
    print("\n── Generating OpenID4VP skills ────────────────────────────")
    generate_oid4vp_skills()
```

---

## Step 5 — Update `AGENTS.md`

Add the new skills to the table in `AGENTS.md`:

```markdown
| `oid4vp-overview` | OID4VP terminology, same/cross device flow overview |
| `oid4vp-authorization-request` | Authorization request params, client_id prefixes, request_uri, JAR |
| `oid4vp-dcql` | DCQL queries, claims path pointers, credential selection |
| `oid4vp-response` | vp_token, direct_post, encrypted responses, VP token validation |
| `oid4vp-metadata` | Wallet/verifier metadata, wallet invocation, Verifier Attestation JWT |
| `oid4vp-security` | Security, privacy, replay prevention, conformance |
| `oid4vp-dc-api` | OpenID4VP over W3C Digital Credentials API (browser) |
| `oid4vp-credential-formats` | Format-specific params: W3C VC, mdoc, SD-JWT VC |
```

Also add to the Rules section:

```markdown
- For any OpenID4VP question, load the relevant `oid4vp-*` skill before answering.
- For flows that involve both ARF and OID4VP (e.g. wallet presentation), 
  load both `arf-presentation-flows` and `oid4vp-authorization-request`.
```

---

## Step 6 — Update `README.md`

Add a new row to the Skills table:

```markdown
| `oid4vp-*` (8 skills) | OID4VP 1.0 Final | Authorization requests, DCQL, responses, metadata, security, DC API, credential formats |
```

And add to the Sources section:

```markdown
- [OpenID4VP 1.0 Final](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html)
```

---

## Step 7 — Verify

After making the changes, run:

```bash
python scripts/split_arf.py
```

Expected output — 8 new `oid4vp-*` skills written under `.opencode/skills/`.
Check token counts: each should ideally be under 8,000 tokens.
If any skill exceeds 8,000 tokens, split it further by narrowing its section numbers.

Then commit:

```bash
git add .opencode/skills/ scripts/split_arf.py AGENTS.md README.md
git commit -m "feat: add OpenID4VP 1.0 skills"
```
