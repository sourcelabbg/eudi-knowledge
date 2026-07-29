# EUDI Knowledge Base

Python tool that fetches official EUDI/eIDAS2 specifications and splits them
into SKILL.md files, distributed as a single plugin that both Claude Code and
Codex install.

## Project Structure

```
scripts/
  common.py            # Shared utilities (fetch, HTML convert, token count, skill write)
  split_arf.py         # ARF main document → 14 skills
  split_oid4vp.py      # OpenID4VP spec → 11 skills
  split_arf_annexes.py # ARF annexes + tech specs → ~39 skills (auto-split)
  split_arf_topics.py  # ARF discussion topics → ~34 skills (auto-split)
  split_oid4vci.py     # OpenID4VCI spec → 8 skills
  split_external.py    # HAIP, SD-JWT, W3C specs → ~41 skills
  split_mattr_mdoc.py  # MATTR Learn mDocs (ISO 18013-5) → 3 skills
  split_sd_jwt_quickstart.py # SD-JWT implementation quickstart → 1 skill
  generate_all.py      # Single entry point for all generators
  update.py            # Check for new ARF release, re-run generators if newer version found
  release.py           # Sync the plugin version across both host manifests
plugins/eudi/          # THE PLUGIN — one directory, two host manifests
  .claude-plugin/plugin.json   # Claude Code manifest
  .codex-plugin/plugin.json    # Codex manifest
  skills/              # CANONICAL skill files (158 generated + 4 role skills)
  agents/              # 4 thin Claude Code subagents (Codex ignores these)
  README.md            # Install/update instructions for consumers
.claude-plugin/marketplace.json    # Claude Code marketplace catalogue
.agents/plugins/marketplace.json   # Codex marketplace catalogue
.claude/skills         # Symlink → ../plugins/eudi/skills (in-repo discovery)
.claude/commands/      # Repo maintenance procedures (e.g. ADD_OPENID4VP.md)
.agents/skills         # Symlink → ../plugins/eudi/skills (in-repo discovery)
.arf-version           # Last-processed ARF release tag
.plugin-version.json   # Plugin version state (ARF base, revision, content hash)
requirements.txt       # Pinned Python dependencies
docs/plugin-distribution.md  # Host compatibility + packaging validation log
```

**The canonical skill location is `plugins/eudi/skills/`.** Generators write
real files there because both hosts copy a plugin into a cache and *skip*
symlinks whose target resolves outside the plugin — a symlinked `skills/` would
silently ship empty. The two `skills` symlinks point the other way, so this
repository loads its own skills while you work on it; they are never part of a
published package. See [docs/plugin-distribution.md](docs/plugin-distribution.md).

The plugin lives in a `plugins/<name>/` subdirectory rather than at the
repository root so the published package contains only skills and manifests —
not `scripts/`, `docs/`, or `requirements.txt`. This also matches the dominant
convention in Anthropic's official marketplace.

## Specialist roles (skills + Claude subagents)

Four hand-authored specialist roles ship with the plugin. Claude Code plugins
support subagents; Codex plugins do not — so each role is authored **once as a
skill** (both hosts) with a thin Claude subagent that loads it.

| Role | Skill (both hosts) | Claude subagent | Purpose |
|---|---|---|---|
| Standards generalist | `eudi-expert` | `@eudi:eudi-expert` | General EUDI specialist across ARF, OID4VP, and OID4VCI. |
| OID4VP audit | `oid4vp-security-auditor` | `@eudi:oid4vp-security-auditor` | Security/privacy audit of OpenID4VP requests, responses, and verifier checks. |
| Trust architecture | `arf-trust-architect` | `@eudi:arf-trust-architect` | Trust model and actor lifecycle guidance based on ARF. |
| Issuer review | `oid4vci-issuer-reviewer` | `@eudi:oid4vci-issuer-reviewer` | Issuer-side OpenID4VCI flow review and hardening checklist. |

The role text lives only in `plugins/eudi/skills/<role>/SKILL.md`; the matching
file in `plugins/eudi/agents/` just carries frontmatter plus "load that skill and
follow it". Use a role by invoking the skill, or on Claude Code by delegating:

```text
@eudi:eudi-expert What skills apply to this wallet presentation flow?
@eudi:oid4vp-security-auditor Audit this direct_post response handling.
```

**These four skills are hand-authored, not generated.** They live alongside the
generated corpus, so `clean_old_skills()` skips the names listed in
`HAND_WRITTEN_SKILLS` in `scripts/common.py`. Adding a role means adding its
name to that set, or the next regeneration deletes it. Do not declare
`"agents"` in `plugin.json` — a bare directory string fails validation, and
`agents/` at the plugin root is discovered automatically.

## Build & Run Commands

```bash
# Setup
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# Generate all skills (primary command)
python scripts/generate_all.py

# Generate only ARF main document skills
python scripts/split_arf.py

# Check for updates and regenerate if new ARF version available
python scripts/update.py

# Force regenerate regardless of version
python scripts/update.py --force
```

No test suite exists. No linter or formatter is configured.
Validate changes by running `python scripts/generate_all.py` and checking that
skills are written to `plugins/eudi/skills/*/SKILL.md` without errors.

## CI / GitHub Actions

- **Workflow**: `.github/workflows/update-arf.yml`
- **Schedule**: Every Monday 08:00 UTC (also manual dispatch)
- **Python version**: 3.12
- **What it does**: `pip install -r requirements.txt` → `python scripts/update.py` → auto-commit if skills changed

## Available Skills

### ARF Main Document

| Skill | Trigger |
|---|---|
| `arf-glossary` | Term or acronym definitions (PID, QEAA, WSCD, LoTE...) |
| `arf-ecosystem-roles` | Who does what: Wallet Provider, PID Provider, Relying Party... |
| `arf-architecture` | Design principles, reference architecture, components, interfaces |
| `arf-wscd-states` | WSCD architecture types, state lifecycles, pseudonym types |
| `arf-presentation-flows` | Remote/proximity presentation flows, OID4VP, DC API |
| `arf-data-model` | Credential formats (mdoc, SD-JWT VC), attestation categories, rulebooks |
| `arf-trust-model` | Trust framework, provider registration, Wallet/PID/RP lifecycle |
| `arf-wallet-lifecycle-install` | Wallet Unit lifecycle overview, installation, activation |
| `arf-wallet-lifecycle-mgmt` | Wallet Unit management, revocation, migration, uninstallation |
| `arf-issuance-reqs` | PID/attestation issuance, batch issuance, key binding |
| `arf-presentation-reqs` | Wallet-side presentation trust: RP auth, disclosure, user approval |
| `arf-rp-verification` | RP-side verification: authenticity, revocation, device/user binding |
| `arf-attestation-mgmt` | Wallet-to-wallet presentation, attestation management, deletion |
| `arf-wallet-reqs` | Wallet Solution certification, conformity assessment, risk management |

### ARF Annexes & Technical Specifications

| Skill | Trigger |
|---|---|
| `arf-hlr-intro` | HLR structure overview, key words (SHALL/SHOULD/MAY) |
| `hlr-NN-*` (~33 skills) | Specific high-level requirements by topic number (auto-split if large) |
| `arf-annex3-pid-rulebook` | PID Rulebook — attribute schemas, mdoc/SD-JWT VC encoding, trust anchors (from Annex 3.01) |
| `arf-annex3-mdl-rulebook` | mDL Rulebook — attribute schema, ISO 18013-5 encoding (from Annex 3.02) |
| `arf-design-guide` | EUDI Wallet UI/UX design principles, visual identity |
| `arf-design-data-sharing` | Data sharing user flow scenarios |
| `arf-standards-matrix-*` | Standards matrix mapped to CIR articles by actor (auto-split) |

### ARF Discussion Topics

| Skill | Trigger |
|---|---|
| `arf-topic-a-*` | Privacy risks and mitigations |
| `arf-topic-b-*` | Re-issuance and batch issuance |
| `arf-topic-c-*` | Wallet Unit Attestation (WUA/WIA) |
| `arf-topic-d-*` | Embedded disclosure policies |
| `arf-topic-e-*` | Pseudonyms and user authentication |
| `arf-topic-f-*` | Digital Credential API integration |
| `arf-topic-g-*` | Zero Knowledge Proof |
| `arf-topic-h-*` | Transaction logs |
| `arf-topic-i-*` | Person representing another person |
| `arf-topic-j-*` | Wallet-to-wallet interactions |
| `arf-topic-k-*` | Combined presentation of attestations |
| `arf-topic-lm-*` | Data deletion and WRP reporting to DPA |
| `arf-topic-n-*` | Export and data portability |
| `arf-topic-o-*` | Catalogues for attestations |
| `arf-topic-p-*` | Secure cryptographic interface (Wallet-WSCA) |
| `arf-topic-q-*` | User-Wallet Instance interface |
| `arf-topic-r-*` | User-to-device authentication |
| `arf-topic-s-*` | Certificate transparency |
| `arf-topic-t-*` | Support and maintenance by Wallet Provider |
| `arf-topic-u-*` | EUDI Wallet trust mark |
| `arf-topic-v-*` | PID Rulebook discussion |
| `arf-topic-w-*` | Transactional data for payments |
| `arf-topic-x-*` | Relying Party registration |
| `arf-topic-aa-*` | Electronic payments SCA with Wallet |

Large topics are automatically split into `-part-N` suffixed skills.

### OpenID4VP

| Skill | Trigger |
|---|---|
| `oid4vp-overview` | OID4VP terminology, same/cross device flow overview |
| `oid4vp-authorization-request` | Authorization request params, client_id prefixes |
| `oid4vp-request-uri-jar` | request_uri, JWT-Secured Authorization Requests (JAR) |
| `oid4vp-dcql` | DCQL queries, claims path pointers, credential selection |
| `oid4vp-response` | vp_token, direct_post, encrypted responses, VP token validation |
| `oid4vp-metadata` | Wallet/verifier metadata, wallet invocation, Verifier Attestation JWT |
| `oid4vp-security` | Security, privacy, replay prevention, conformance |
| `oid4vp-dc-api` | OpenID4VP over W3C Digital Credentials API (browser) |
| `oid4vp-format-w3c-vc` | W3C VC format params, claims matching |
| `oid4vp-format-mdoc` | ISO mdoc (18013/23220) Handover, SessionTranscript |
| `oid4vp-format-sd-jwt-vc` | SD-JWT VC format, key binding JWT |

### OpenID4VCI

| Skill | Trigger |
|---|---|
| `oid4vci-overview` | OID4VCI terminology, issuance flow overview |
| `oid4vci-issuer-metadata` | Credential Issuer metadata, discovery |
| `oid4vci-credential-offer` | Credential offer (issuer-initiated issuance) |
| `oid4vci-authorization` | Authorization flow, token endpoint extensions |
| `oid4vci-credential-endpoint` | Credential request/response, proof of possession |
| `oid4vci-batch-issuance` | Batch credential issuance |
| `oid4vci-deferred-notification` | Deferred retrieval, notifications |
| `oid4vci-security` | Security and privacy considerations |

### HAIP, SD-JWT, and Other Specs

| Skill | Trigger |
|---|---|
| `haip-overview` | High Assurance Interop Profile overview |
| `haip-protocol-profile` | OID4VP/OID4VCI profile, credential format requirements |
| `haip-security` | HAIP security and privacy requirements |
| `sd-jwt-intro` | SD-JWT concepts, terminology |
| `sd-jwt-quickstart` | End-to-end SD-JWT path: issuer, holder, verifier, SD-JWT VC, OID4VP |
| `sd-jwt-format` | SD-JWT data formats, disclosures, salt/hash |
| `sd-jwt-examples` | SD-JWT issuance and presentation examples |
| `sd-jwt-examples-nested` | Nested data: flat, structured, recursive disclosures |
| `sd-jwt-verification` | SD-JWT verification, JWS JSON serialization |
| `sd-jwt-security` | SD-JWT security and privacy considerations |
| `sd-jwt-vc-intro` | SD-JWT VC introduction, terminology, vct claim |
| `sd-jwt-vc-metadata` | SD-JWT VC issuer/type metadata |
| `sd-jwt-vc-presentation-security` | SD-JWT VC presentation, security, privacy |
| `token-status-list-core` | Token Status List fundamentals, representation |
| `token-status-list-usage` | Referenced tokens, verification, status types |
| `token-status-list-aggregation-x509` | Status list aggregation, X.509 extensions |
| `token-status-list-verification-details` | Detailed verification rules |

### W3C Verifiable Credentials Data Model 2.0

| Skill | Trigger |
|---|---|
| `w3c-vcdm-intro` | W3C VCDM 2.0 introduction, ecosystem overview |
| `w3c-vcdm-terminology` | W3C VCDM terminology, key definitions |
| `w3c-vcdm-data-model-concepts` | Core data model: claims, credentials, presentations |
| `w3c-vcdm-getting-started` | Getting started, verifiable credentials, contexts |
| `w3c-vcdm-identifiers-types` | Identifier modeling, URI usage |
| `w3c-vcdm-types` | Type processing and requirements |
| `w3c-vcdm-names-descriptions` | Human-readable labeling |
| `w3c-vcdm-issuer` | Issuer property requirements |
| `w3c-vcdm-subject-validity` | Credential subject structure |
| `w3c-vcdm-validity-period` | Temporal validity semantics |
| `w3c-vcdm-status-schemas-securing` | Status, data schemas, securing mechanisms |
| `w3c-vcdm-presentations` | Verifiable presentations structure |
| `w3c-vcdm-trust-extensibility` | Trust model, extensibility |
| `w3c-vcdm-integrity` | Integrity of related resources |
| `w3c-vcdm-refreshing-evidence` | Refreshing, terms of use, evidence |
| `w3c-vcdm-zkp-advanced` | ZKP, time, authorization, reserved extensions |
| `w3c-vcdm-ecosystem-graphs` | Ecosystem compatibility, VC graphs |
| `w3c-vcdm-syntaxes-algorithms` | JSON-LD, media types, verification algorithms |
| `w3c-vcdm-privacy-correlation` | Privacy: correlation risks and mitigations |
| `w3c-vcdm-privacy-minimization` | Privacy: data minimization approaches |
| `w3c-vcdm-privacy-minimization-continued` | Privacy: additional minimization patterns |
| `w3c-vcdm-privacy-threats` | Privacy: threats and residual risks |
| `w3c-vcdm-security` | W3C VCDM security considerations |

### W3C Digital Credentials API

| Skill | Trigger |
|---|---|
| `w3c-dc-api-core` | DC API purpose, usage examples, scope, terminology |
| `w3c-dc-api-interface` | DigitalCredential interface, protocol registry, CM Level 1, Permissions Policy |
| `w3c-dc-api-coordinator` | Credential Request Coordinator, interaction states, request algorithms |
| `w3c-dc-api-security` | DC API security, accessibility, internationalization |
| `w3c-dc-api-privacy` | DC API privacy design and protocol/format privacy properties |
| `w3c-dc-api-privacy-risks` | DC API privacy risks: unnecessary requests, fingerprinting, transparency |

### MATTR Learn mDocs (ISO/IEC 18013-5)

| Skill | Trigger |
|---|---|
| `mdoc-core-capabilities` | mDoc core capabilities: device/issuer/holder auth, session encryption, selective disclosure |
| `mdoc-standards-tech` | mDoc standards: ISO 18013-5, 18013-7, 23220, CBOR, COSE, X.509 (IACA, DSC) |
| `mdoc-structure-function` | mDoc data structures: MSO, COSE_sign1, namespaces, digests, device auth methods, signed payload |

## Skill Usage Rules

- Before answering any ARF-specific question, load the relevant skill.
- Never cite normative requirements (SHALL/MUST) from memory — always load the skill first.
- When a question spans multiple skills, load all relevant ones before answering.
- Always note the ARF version when citing a requirement.
- For any OpenID4VP question, load the relevant `oid4vp-*` skill before answering.
- For any OpenID4VCI question, load the relevant `oid4vci-*` skill before answering.
- For flows that involve both ARF and OID4VP (e.g. wallet presentation),
  load both `arf-presentation-flows` and `oid4vp-authorization-request`.
- For credential format questions, load `arf-data-model` plus the relevant format skill
  (`sd-jwt-*`, `oid4vp-format-*`, etc.).
- For implementation walkthroughs of SD-JWT/SD-JWT VC, start with
  `sd-jwt-quickstart`, then load specific `sd-jwt-*` and `sd-jwt-vc-*` skills.
- For ISO/IEC 18013-5 (mdoc) questions, load the relevant `mdoc-*` skill.
  Combine with `arf-data-model` for credential format context.
- For high-level requirements, use `hlr-NN-*` skills to find specific topic requirements.
- For discussion topic deep dives, use `arf-topic-*` skills.

## Code Style Guidelines

### Python Version

Target Python 3.12+. Use modern syntax:
- `str | None` not `Optional[str]`
- `list[str]` not `List[str]`
- No `from __future__ import annotations`

### Imports

Order: stdlib -> third-party -> local. Scripts use `sys.path.insert` to import
from sibling `common.py`. Example:

```python
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import re
import requests
from common import OUTPUT_BASE, fetch_markdown, write_skill
```

### Type Hints

Use return type annotations on all functions. Annotate parameters when non-obvious:

```python
def get_cached_version() -> str | None:
def extract_section(text: str, patterns: list) -> str:
def write_skill(skill_dir: Path, name: str, description: str, content: str, version: str) -> None:
```

### Naming

- Functions: `snake_case` -- verb-first (`get_latest_version`, `fetch_arf`, `count_tokens`)
- Constants: `UPPER_SNAKE_CASE` (`ARF_MAIN_URL`, `TOKEN_WARN`, `SKILLS`)
- Variables: `snake_case`, short and contextual (`r` for response, `m` for match)
- Files: `snake_case.py`

### Docstrings

Module-level docstrings with usage instructions. No per-function docstrings (code is self-documenting given small script size). Example:

```python
"""
split_arf.py -- Fetch the latest ARF and split it into OpenCode SKILL.md files.
Usage: python scripts/split_arf.py
"""
```

### Error Handling

- Use bare `try/except Exception: pass` only for non-critical fallbacks (e.g. version fetch).
- Use `r.raise_for_status()` for HTTP calls that must succeed.
- Let critical failures propagate -- no defensive try/except wrapping.

### String Formatting

Use f-strings exclusively. Multi-line strings via implicit concatenation for URLs:

```python
ARF_MAIN_URL = (
    "https://raw.githubusercontent.com/eu-digital-identity-wallet/"
    "eudi-doc-architecture-and-reference-framework/main/docs/"
    "architecture-and-reference-framework-main.md"
)
```

### Output Style

Use `print()` with emoji prefixes for status output:
- `✓` for success
- `✗` for failure/skip
- `⚠` for warnings
- `→` for actions in progress

### Script Structure

Each script follows: constants -> helper functions -> `main()` -> `if __name__ == "__main__"` guard.
Shared code lives in `common.py` -- imported via `sys.path.insert` for sibling imports.
Import heavy stdlib modules (`subprocess`) inside functions when only needed conditionally.

### File I/O

Use `pathlib.Path` throughout. Never `os.path`. Use `encoding="utf-8"` explicitly on `.write_text()`.

### Dependencies

Pinned in `requirements.txt` with exact versions (`==`), except `tiktoken` (`>=`).
No `pyproject.toml` or `setup.py` -- this is not a distributable package.

## Generated Skill Format

Each skill is a Markdown file at `plugins/eudi/skills/<name>/SKILL.md` with YAML frontmatter. The `sections` field lists top-level + one sub-level headings so models can locate content across skills:

```markdown
---
name: "arf-architecture"
description: "Use when designing wallet components..."
sections:
  - "4.1 Introduction"
  - "4.2 Design principles"
  - "4.2.1 User-centricity"
---

<!-- ARF version: v1.5.0 -->
<!-- Tokens: ~4200 -->

[extracted ARF content]
```

Token counts use `cl100k_base` encoding. Skills exceeding 8,000 tokens are flagged
with `(LARGE)` in the token comment.

## Key Design Decisions

- Skills are **generated, not hand-written** -- edit the relevant `split_*.py` script, not SKILL.md files directly.
- `common.py` provides shared utilities (fetch, HTML->markdown, token counting, skill writing).
- `generate_all.py` is the single entry point that cleans old skills and runs all generators.
- The `SKILLS` dict in each splitter maps skill names -> regex patterns or section numbers.
- Skills with `"join": True` extract each pattern individually and merge with `---` separators.
- Skills with `"url"` fetch content from a separate file (e.g. `arf-glossary` from Annex 1).
- The ARF main document is **assembled from chapter files** under `docs/main/` (`01-introduction.md` ... `11-annexes.md`); upstream retired the single `architecture-and-reference-framework-main.md`. `list_main_chapters()` discovers them via the GitHub contents API and sorts by filename, so a renumbering upstream cannot silently drop a chapter. Filename order matches chapter order, so the joined text keeps the heading numbering the `SKILLS` patterns match.
- Figure links arrive at varying relative depths (`media/`, `../media/`, `../../media/`) depending on where the source file sits under `docs/`; `enrich_arf_diagrams()` rewrites all of them to absolute raw URLs.
- Annex 2.02 (HLRs by topic) is dynamically split at `####` headings -- each topic becomes its own skill.
- Annex 3 rulebooks (PID, mDL) are fetched from a separate repo (`eudi-doc-attestation-rulebooks-catalog`) since they were moved out of the main ARF repo.
- Large topics and HLR skills are **automatically split** at heading boundaries into `-part-N` suffixed skills when they exceed the token budget.
- Discussion topics are each a standalone markdown file -- auto-split if they exceed the token budget.
- HTML specs (OID4VP, OID4VCI, HAIP, SD-JWT, etc.) are converted from HTML to markdown, then split by section numbers.
- W3C VCDM 2.0 is split at subsection level (`### 4.N`) due to massive document size (~140K tokens total).
- Old skill directories are cleaned before regeneration to remove stale skills.
- `.arf-version` file caches the last-processed release tag to avoid redundant regeneration.
- Every skill includes a `sections:` list in frontmatter for cross-skill reference lookup.
