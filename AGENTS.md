# EUDI Knowledge Base

Python tool that fetches the official EUDI Architecture and Reference Framework (ARF)
and splits it into OpenCode SKILL.md files for use in any EUDI-related project.

## Project Structure

```
scripts/
  split_arf.py      # Fetch ARF markdown from GitHub, extract sections, write SKILL.md files
  update.py          # Check for new ARF release, re-run splitter if newer version found
.opencode/skills/    # Generated skill files (arf-architecture/, arf-data-model/, etc.)
docs/raw/            # Gitignored raw downloads
requirements.txt     # Pinned Python dependencies
```

## Build & Run Commands

```bash
# Setup
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# Generate skills from latest ARF (primary command)
python scripts/split_arf.py

# Check for updates and regenerate if new ARF version available
python scripts/update.py

# Force regenerate regardless of version
python scripts/update.py --force
```

No test suite exists. No linter or formatter is configured.
Validate changes by running `python scripts/split_arf.py` and checking that
skills are written to `.opencode/skills/*/SKILL.md` without errors.

## CI / GitHub Actions

- **Workflow**: `.github/workflows/update-arf.yml`
- **Schedule**: Every Monday 08:00 UTC (also manual dispatch)
- **Python version**: 3.12
- **What it does**: `pip install -r requirements.txt` → `python scripts/update.py` → auto-commit if skills changed

## Available Skills

| Skill | Trigger |
|---|---|
| `arf-glossary` | Term or acronym definitions (PID, QEAA, WSCD, LoTE…) |
| `arf-ecosystem-roles` | Who does what: Wallet Provider, PID Provider, Relying Party… |
| `arf-architecture` | Design principles, reference architecture, components, interfaces |
| `arf-wscd-states` | WSCD architecture types, state lifecycles, pseudonym types |
| `arf-presentation-flows` | Remote/proximity presentation flows, OID4VP, DC API |
| `arf-data-model` | Credential formats (mdoc, SD-JWT VC), attestation categories, rulebooks |
| `arf-trust-model` | Trust framework, provider registration, Wallet/PID/RP lifecycle |
| `arf-wallet-lifecycle` | Wallet Unit installation, activation, management, uninstallation |
| `arf-issuance-reqs` | PID/attestation issuance, batch issuance, key binding |
| `arf-presentation-reqs` | Wallet-side presentation trust: RP auth, disclosure, user approval |
| `arf-rp-verification` | RP-side verification: authenticity, revocation, device/user binding |
| `arf-attestation-mgmt` | Wallet-to-wallet presentation, attestation management, deletion |
| `arf-wallet-reqs` | Wallet Solution certification, conformity assessment, risk management |
| `oid4vp-overview` | OID4VP terminology, same/cross device flow overview |
| `oid4vp-authorization-request` | Authorization request params, client_id prefixes, request_uri, JAR |
| `oid4vp-dcql` | DCQL queries, claims path pointers, credential selection |
| `oid4vp-response` | vp_token, direct_post, encrypted responses, VP token validation |
| `oid4vp-metadata` | Wallet/verifier metadata, wallet invocation, Verifier Attestation JWT |
| `oid4vp-security` | Security, privacy, replay prevention, conformance |
| `oid4vp-dc-api` | OpenID4VP over W3C Digital Credentials API (browser) |
| `oid4vp-credential-formats` | Format-specific params: W3C VC, mdoc, SD-JWT VC |

## Skill Usage Rules

- Before answering any ARF-specific question, load the relevant skill.
- Never cite normative requirements (SHALL/MUST) from memory — always load the skill first.
- When a question spans multiple skills, load all relevant ones before answering.
- Always note the ARF version when citing a requirement.
- For any OpenID4VP question, load the relevant `oid4vp-*` skill before answering.
- For flows that involve both ARF and OID4VP (e.g. wallet presentation),
  load both `arf-presentation-flows` and `oid4vp-authorization-request`.

## Code Style Guidelines

### Python Version

Target Python 3.12+. Use modern syntax:
- `str | None` not `Optional[str]`
- `list[str]` not `List[str]`
- No `from __future__ import annotations`

### Imports

Order: stdlib → third-party → local. No blank line separators between groups
(current codebase omits them). Example from `split_arf.py`:

```python
import re
import tiktoken
import requests
from pathlib import Path
```

### Type Hints

Use return type annotations on all functions. Annotate parameters when non-obvious:

```python
def get_cached_version() -> str | None:
def extract_section(text: str, patterns: list) -> str:
def write_skill(skill_dir: Path, name: str, description: str, content: str, version: str) -> None:
```

### Naming

- Functions: `snake_case` — verb-first (`get_latest_version`, `fetch_arf`, `count_tokens`)
- Constants: `UPPER_SNAKE_CASE` (`ARF_MAIN_URL`, `TOKEN_WARN`, `SKILLS`)
- Variables: `snake_case`, short and contextual (`r` for response, `m` for match)
- Files: `snake_case.py`

### Docstrings

Module-level docstrings with usage instructions. No per-function docstrings (code is self-documenting given small script size). Example:

```python
"""
split_arf.py — Fetch the latest ARF and split it into OpenCode SKILL.md files.
Usage: python scripts/split_arf.py
"""
```

### Error Handling

- Use bare `try/except Exception: pass` only for non-critical fallbacks (e.g. version fetch).
- Use `r.raise_for_status()` for HTTP calls that must succeed.
- Let critical failures propagate — no defensive try/except wrapping.

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

Each script follows: constants → helper functions → `main()` → `if __name__ == "__main__"` guard.
Keep scripts standalone — no shared module or `__init__.py`. Import heavy stdlib
modules (`subprocess`) inside functions when only needed conditionally.

### File I/O

Use `pathlib.Path` throughout. Never `os.path`. Use `encoding="utf-8"` explicitly on `.write_text()`.

### Dependencies

Pinned in `requirements.txt` with exact versions (`==`), except `tiktoken` (`>=`).
No `pyproject.toml` or `setup.py` — this is not a distributable package.

## Generated Skill Format

Each skill is a Markdown file at `.opencode/skills/<name>/SKILL.md` with YAML frontmatter:

```markdown
---
name: "arf-architecture"
description: "Use when designing wallet components..."
---

<!-- ARF version: v1.5.0 -->
<!-- Tokens: ~4200 -->

[extracted ARF content]
```

Token counts use `cl100k_base` encoding. Skills exceeding 8,000 tokens are flagged
with `(LARGE)` and should be considered for splitting.

## Key Design Decisions

- Skills are **generated, not hand-written** — edit `split_arf.py` section patterns, not SKILL.md files directly.
- The `SKILLS` dict in `split_arf.py` maps skill names → regex patterns matching ARF section headers.
- Skills with `"join": True` extract each pattern individually and merge with `---` separators (used for non-consecutive sections like `arf-presentation-flows`).
- Skills with `"url"` fetch content from a separate file (used for `arf-glossary` which lives in Annex 1).
- Old skill directories are cleaned before regeneration to remove stale skills.
- `.arf-version` file caches the last-processed release tag to avoid redundant regeneration.
