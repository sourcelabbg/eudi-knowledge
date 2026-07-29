# EUDI Knowledge plugin

162 individually loadable skills derived from official EUDI Wallet / eIDAS2
specifications: the ARF (main document, annexes, high-level requirements,
discussion topics), OpenID4VP, OpenID4VCI, HAIP, SD-JWT and SD-JWT VC, Token
Status List, ISO/IEC 18013-5 mdoc, W3C Verifiable Credentials Data Model 2.0,
and the W3C Digital Credentials API.

One directory, two host manifests — Claude Code reads `.claude-plugin/`, Codex
reads `.codex-plugin/`, and both load the same `skills/` tree.

## Install

```bash
# Claude Code
claude plugin marketplace add sourcelabbg/eudi-knowledge
claude plugin install eudi@eudi-knowledge
# then, in a session: /reload-plugins

# Codex
codex plugin marketplace add sourcelabbg/eudi-knowledge
codex plugin add eudi@eudi-knowledge
# then start a new session
```

## Update

Refresh the catalogue *and* the plugin — one step is not enough:

```bash
# Claude Code
claude plugin marketplace update eudi-knowledge && claude plugin update eudi

# Codex
codex plugin marketplace upgrade eudi-knowledge && codex plugin add eudi@eudi-knowledge
```

Nothing updates until the manifest `version` changes, which happens only when
generated content actually changed.

Full instructions — team-wide setup, install scopes, pinning to a release,
disabling per project, uninstalling, troubleshooting — are in
[docs/installing.md](../../docs/installing.md).

## Specialist roles

Four of the skills are specialist roles rather than reference material. Each
tells the model which corpus skills to load, what to check, and how to format
its findings:

| Skill | Use for |
|---|---|
| `eudi-expert` | General or cross-specification EUDI questions |
| `oid4vp-security-auditor` | Auditing OpenID4VP request/response handling |
| `arf-trust-architect` | Trust model and actor lifecycle decisions |
| `oid4vci-issuer-reviewer` | Reviewing an OpenID4VCI issuer implementation |

On Claude Code each role is also a subagent, so the corpus lookup runs in its
own context window and returns only conclusions:

```text
@eudi:oid4vp-security-auditor Audit this direct_post response handling.
```

Codex plugins have no agent component, so there the roles are skills only.

## Skill names are namespaced

Plugin skills carry the plugin name as a prefix, so explicit invocation is
`/eudi:arf-glossary`, not `/arf-glossary`. Model-invoked selection is unchanged —
Claude and Codex still pick skills from their `description` frontmatter.

## Context cost

All 162 skill descriptions are always-on so the model can select among them:
roughly **14,600 tokens added to every session** (`claude plugin details eudi`
reports the current figure). Skill bodies load only when a skill fires. Disable
the plugin in projects unrelated to EUDI work:

```bash
claude plugin disable eudi
```

## Versioning

The version tracks the ARF release the corpus was built from —
`<ARF major>.<ARF minor>.<revision>`, where `revision` increments when
generated content changes within the same ARF release. So `3.0.0` means "built
from ARF v3.0.0, first revision".

## Editing

Don't edit `skills/*/SKILL.md` — every file is generated. Change the relevant
`scripts/split_*.py` generator in the repository root and re-run
`python scripts/generate_all.py`. See the repository
[README](../../README.md) and [AGENTS.md](../../AGENTS.md).

Packaging details, host-compatibility findings, and the validation log live in
[docs/plugin-distribution.md](../../docs/plugin-distribution.md).
