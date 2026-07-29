# eudi-knowledge

Agent skills derived from official EUDI Wallet / eIDAS2 specifications,
distributed as a single plugin that both **Claude Code** and **Codex** install.

## What's in here

162 individually loadable skills split from the
[EUDI Wallet Architecture and Reference Framework (ARF)](https://github.com/eu-digital-identity-wallet/eudi-doc-architecture-and-reference-framework)
and related specs. Nothing is bundled into one giant skill — each stays
separately selectable so the model loads only what a question needs.

## Install

```bash
# Claude Code
claude plugin marketplace add sourcelabbg/eudi-knowledge
claude plugin install eudi@eudi-knowledge

# Codex
codex plugin marketplace add sourcelabbg/eudi-knowledge
codex plugin add eudi@eudi-knowledge
```

Then run `/reload-plugins` in Claude Code, or start a new Codex session.

Plugin skills are namespaced, so explicit invocation is `/eudi:arf-glossary`.
All 162 descriptions stay in context so the model can choose between them —
about 14.6k tokens per session.

**[docs/installing.md](docs/installing.md)** covers updating, team-wide setup,
pinning to a release, install scopes, disabling the plugin per project,
uninstalling, and troubleshooting.
[docs/plugin-distribution.md](docs/plugin-distribution.md) covers packaging and
host compatibility.

## Specialist roles

Four skills are specialist roles rather than reference material — they tell the
model which corpus skills to load, what to check, and how to report.

| Role | Skill (both hosts) | Claude subagent |
|---|---|---|
| General EUDI standards specialist | `eudi-expert` | `@eudi:eudi-expert` |
| OpenID4VP security/privacy audit | `oid4vp-security-auditor` | `@eudi:oid4vp-security-auditor` |
| ARF trust model and actor lifecycle | `arf-trust-architect` | `@eudi:arf-trust-architect` |
| OpenID4VCI issuer review | `oid4vci-issuer-reviewer` | `@eudi:oid4vci-issuer-reviewer` |

Claude Code plugins support subagents, so there each role also runs in its own
context window. Codex plugins have no agent component, so there the roles are
skills only.

```text
@eudi:oid4vp-security-auditor Audit this direct_post response handling.
```

## Skills

### ARF Main Document (14 skills)

| Skill | Source | Content |
|---|---|---|
| `arf-glossary` | ARF Annex 1 | Term definitions |
| `arf-ecosystem-roles` | ARF §3 | All ecosystem roles |
| `arf-architecture` | ARF §4.1–4.3 | Design principles, reference architecture, components |
| `arf-wscd-states` | ARF §4.5–4.7 | WSCD types, state lifecycles, pseudonyms |
| `arf-presentation-flows` | ARF §4.4 + §5.6 | Remote/proximity flows, OID4VP |
| `arf-data-model` | ARF §5 | Credential formats, attestation categories |
| `arf-trust-model` | ARF §6.1–6.4 | Trust framework, provider registration |
| `arf-wallet-lifecycle-install` | ARF §6.5.1–6.5.3 | Wallet Unit lifecycle, installation, activation |
| `arf-wallet-lifecycle-mgmt` | ARF §6.5.4–6.5.5 | Wallet Unit management, revocation, uninstallation |
| `arf-issuance-reqs` | ARF §6.6.1–6.6.2 | PID/attestation issuance, batch issuance |
| `arf-presentation-reqs` | ARF §6.6.3.1–5 | Wallet-side presentation trust, RP auth |
| `arf-rp-verification` | ARF §6.6.3.6–13 | RP-side verification, revocation, binding |
| `arf-attestation-mgmt` | ARF §6.6.4–7 | Attestation management, refresh, deletion |
| `arf-wallet-reqs` | ARF §7 | Wallet certification, conformity assessment |

### ARF Annexes & Technical Specifications (~39 skills)

| Skill | Source | Content |
|---|---|---|
| `arf-hlr-intro` | Annex 2.01 | HLR structure overview, key words |
| `hlr-NN-*` (~33 skills) | Annex 2.02 | High-level requirements by topic (auto-split if large) |
| `arf-annex3-pid-rulebook` | Annex 3.01 | PID Rulebook — attribute schemas, mdoc/SD-JWT VC encoding, trust anchors |
| `arf-annex3-mdl-rulebook` | Annex 3.02 | mDL Rulebook — attribute schema, ISO 18013-5 encoding |
| `arf-design-guide` | Annex 5.01 | UI/UX design principles, visual identity |
| `arf-design-data-sharing` | Annex 5.02 | Data sharing user flow scenarios |
| `arf-standards-matrix-*` | TS README | Standards matrix mapped to CIR articles by actor (auto-split) |

### ARF Discussion Topics (~34 skills)

| Skill | Source | Content |
|---|---|---|
| `arf-topic-a-*` | Topic A | Privacy risks and mitigations |
| `arf-topic-b-*` | Topic B | Re-issuance and batch issuance |
| `arf-topic-c-*` | Topic C | Wallet Unit Attestation (WUA/WIA) |
| `arf-topic-d-*` | Topic D | Embedded disclosure policies |
| `arf-topic-e-*` | Topic E | Pseudonyms and user authentication |
| `arf-topic-f-*` | Topic F | Digital Credential API integration |
| `arf-topic-g-*` | Topic G | Zero Knowledge Proof |
| `arf-topic-h-*` | Topic H | Transaction logs |
| `arf-topic-i-*` | Topic I | Person representing another person |
| `arf-topic-j-*` | Topic J | Wallet-to-wallet interactions |
| `arf-topic-k-*` | Topic K | Combined presentation of attestations |
| `arf-topic-lm-*` | Topic L+M | Data deletion and WRP reporting to DPA |
| `arf-topic-n-*` | Topic N | Export and data portability |
| `arf-topic-o-*` | Topic O | Catalogues for attestations |
| `arf-topic-p-*` | Topic P | Secure cryptographic interface (Wallet-WSCA) |
| `arf-topic-q-*` | Topic Q | User-Wallet Instance interface |
| `arf-topic-r-*` | Topic R | User-to-device authentication |
| `arf-topic-s-*` | Topic S | Certificate transparency |
| `arf-topic-t-*` | Topic T | Support and maintenance by Wallet Provider |
| `arf-topic-u-*` | Topic U | EUDI Wallet trust mark |
| `arf-topic-v-*` | Topic V | PID Rulebook discussion |
| `arf-topic-w-*` | Topic W | Transactional data for payments |
| `arf-topic-x-*` | Topic X | Relying Party registration |
| `arf-topic-aa-*` | Topic AA | Electronic payments SCA with Wallet |

Large topics are automatically split into `-part-N` suffixed skills.

### OpenID4VP (11 skills)

| Skill | Source | Content |
|---|---|---|
| `oid4vp-overview` | OID4VP §1–3 | Terminology, same/cross device flows |
| `oid4vp-authorization-request` | OID4VP §4 | Request params, client_id prefixes |
| `oid4vp-request-uri-jar` | OID4VP §5 | request_uri, JWT-Secured Authorization Requests |
| `oid4vp-dcql` | OID4VP §6–7 | DCQL queries, claims path pointers |
| `oid4vp-response` | OID4VP §8 | vp_token, direct_post, validation |
| `oid4vp-metadata` | OID4VP §9–12 | Wallet/verifier metadata, invocation |
| `oid4vp-security` | OID4VP §13–15 | Security, privacy, replay prevention |
| `oid4vp-dc-api` | OID4VP App. A | OpenID4VP over W3C DC API |
| `oid4vp-format-w3c-vc` | OID4VP App. B.1 | W3C VC format params and claims matching |
| `oid4vp-format-mdoc` | OID4VP App. B.2 | ISO mdoc Handover and SessionTranscript |
| `oid4vp-format-sd-jwt-vc` | OID4VP App. B.3 | SD-JWT VC format and key binding |

### OpenID4VCI (8 skills)

| Skill | Source | Content |
|---|---|---|
| `oid4vci-overview` | OID4VCI §1–3 | Terminology, issuance flow overview |
| `oid4vci-issuer-metadata` | OID4VCI §4–5 | Issuer metadata, discovery |
| `oid4vci-credential-offer` | OID4VCI §6 | Credential offer (issuer-initiated) |
| `oid4vci-authorization` | OID4VCI §7–8 | Authorization flow, token endpoint |
| `oid4vci-credential-endpoint` | OID4VCI §9–10 | Credential request/response, nonce |
| `oid4vci-batch-issuance` | OID4VCI §11 | Batch credential issuance |
| `oid4vci-deferred-notification` | OID4VCI §12–13 | Deferred retrieval, notifications |
| `oid4vci-security` | OID4VCI §14–15 | Security, privacy considerations |

### HAIP (3 skills)

| Skill | Source | Content |
|---|---|---|
| `haip-overview` | HAIP §1–4 | High Assurance Interop Profile overview |
| `haip-protocol-profile` | HAIP §5–6 | OID4VP/OID4VCI profile, credential formats |
| `haip-security` | HAIP §7–8 | Security and privacy requirements |

### SD-JWT (6 skills)

| Skill | Source | Content |
|---|---|---|
| `sd-jwt-intro` | RFC 9901 §1–2 | SD-JWT concepts, terminology |
| `sd-jwt-quickstart` | Curated implementation path | End-to-end SD-JWT/SD-JWT VC implementation flow |
| `sd-jwt-format` | RFC 9901 §3–4 | SD-JWT data formats, disclosures, salt/hash |
| `sd-jwt-examples` | RFC 9901 §5 | Issuance and presentation examples |
| `sd-jwt-examples-nested` | RFC 9901 §6 | Nested data: flat, structured, recursive disclosures |
| `sd-jwt-verification` | RFC 9901 §7–8 | Verification, JWS JSON serialization |
| `sd-jwt-security` | RFC 9901 §9–11 | Security and privacy considerations |

### SD-JWT VC (3 skills)

| Skill | Source | Content |
|---|---|---|
| `sd-jwt-vc-intro` | SD-JWT VC §1–3 | Introduction, terminology, vct claim |
| `sd-jwt-vc-metadata` | SD-JWT VC §4–5 | Issuer/type metadata, header params |
| `sd-jwt-vc-presentation-security` | SD-JWT VC §6–10 | Presentation, security, privacy |

### Token Status List (4 skills)

| Skill | Source | Content |
|---|---|---|
| `token-status-list-core` | Draft §1–5 | Status list representation, JWT/CWT tokens |
| `token-status-list-usage` | Draft §6–8 | Referenced tokens, verification, status types |
| `token-status-list-aggregation-x509` | Draft §9–10 | Status list aggregation, X.509 extensions |
| `token-status-list-verification-details` | Draft | Detailed verification rules |

### W3C Verifiable Credentials Data Model 2.0 (~19 skills)

| Skill | Source | Content |
|---|---|---|
| `w3c-vcdm-intro` | W3C VCDM §1 | Introduction, ecosystem overview, conformance |
| `w3c-vcdm-terminology` | W3C VCDM §2 | Terminology and key definitions |
| `w3c-vcdm-data-model-concepts` | W3C VCDM §3 | Core data model: claims, credentials, presentations |
| `w3c-vcdm-getting-started` | W3C VCDM §4.1–4.3 | Getting started, verifiable credentials, contexts |
| `w3c-vcdm-identifiers-types` | W3C VCDM §4.4 | Identifier modeling and URI usage |
| `w3c-vcdm-types` | W3C VCDM §4.5 | Type processing and requirements |
| `w3c-vcdm-names-descriptions` | W3C VCDM §4.6 | Human-readable labeling |
| `w3c-vcdm-issuer` | W3C VCDM §4.7 | Issuer property requirements |
| `w3c-vcdm-subject-validity` | W3C VCDM §4.8 | Credential subject structure |
| `w3c-vcdm-validity-period` | W3C VCDM §4.9 | Temporal validity semantics |
| `w3c-vcdm-status-schemas-securing` | W3C VCDM §4.10–4.12 | Status, data schemas, securing mechanisms |
| `w3c-vcdm-presentations` | W3C VCDM §4.13 | Verifiable presentations |
| `w3c-vcdm-trust-extensibility` | W3C VCDM §5.1–5.2 | Trust model, extensibility |
| `w3c-vcdm-integrity` | W3C VCDM §5.3 | Integrity of related resources |
| `w3c-vcdm-refreshing-evidence` | W3C VCDM §5.4–5.6 | Refreshing, terms of use, evidence |
| `w3c-vcdm-zkp-advanced` | W3C VCDM §5.7–5.10 | ZKP, time, authorization, reserved extensions |
| `w3c-vcdm-ecosystem-graphs` | W3C VCDM §5.11–5.13 | Ecosystem compatibility, VC graphs, securing specs |
| `w3c-vcdm-syntaxes-algorithms` | W3C VCDM §6–7 | JSON-LD, media types, verification algorithms |
| `w3c-vcdm-privacy-correlation` | W3C VCDM §8.1–8.7 | Privacy: correlation risks and mitigations |
| `w3c-vcdm-privacy-minimization` | W3C VCDM §8.8–8.12 | Privacy: data minimization approaches |
| `w3c-vcdm-privacy-minimization-continued` | W3C VCDM §8.13–8.14 | Privacy: additional minimization patterns |
| `w3c-vcdm-privacy-threats` | W3C VCDM §8.15–8.21 | Privacy: threats and residual risks |
| `w3c-vcdm-security` | W3C VCDM §9 | Security considerations |

### W3C Digital Credentials API (2 skills)

| Skill | Source | Content |
|---|---|---|
| `w3c-dc-api-core` | W3C DC API §1–4 | Purpose, usage examples, scope, terminology |
| `w3c-dc-api-interface` | W3C DC API §5, §7–9 | DigitalCredential interface, protocol registry, CM Level 1, Permissions Policy |
| `w3c-dc-api-coordinator` | W3C DC API §6 | Credential Request Coordinator, interaction states, request algorithms |
| `w3c-dc-api-security` | W3C DC API §10, §12–13 | Security, accessibility, internationalization |
| `w3c-dc-api-privacy` | W3C DC API §11.1–11.3 | Privacy design, spectrum of privacy, protocol/format properties |
| `w3c-dc-api-privacy-risks` | W3C DC API §11.4–11.6 | Unnecessary requests, fingerprinting, permission and transparency |

## Project Structure

```
scripts/
  common.py            # Shared utilities (fetch, HTML convert, skill write)
  split_arf.py         # ARF main document → 14 skills
  split_oid4vp.py      # OpenID4VP spec → 11 skills
  split_arf_annexes.py # ARF annexes + tech specs → ~39 skills
  split_arf_topics.py  # ARF discussion topics → ~34 skills (auto-split)
  split_oid4vci.py     # OpenID4VCI spec → 8 skills
  split_external.py    # HAIP, SD-JWT, W3C specs → ~41 skills
  split_mattr_mdoc.py  # MATTR Learn mDocs (ISO 18013-5) → 3 skills
  split_sd_jwt_quickstart.py # SD-JWT implementation quickstart → 1 skill
  generate_all.py      # Single entry point for all generators
  update.py            # Check for updates and regenerate
  release.py           # Sync the plugin version across both host manifests
plugins/eudi/          # THE PLUGIN — one directory, two host manifests
  .claude-plugin/plugin.json   # Claude Code manifest
  .codex-plugin/plugin.json    # Codex manifest
  skills/              # Canonical skill files (158 generated + 4 role skills)
  agents/              # 4 thin Claude Code subagents (Codex ignores these)
.claude-plugin/marketplace.json    # Claude Code marketplace catalogue
.agents/plugins/marketplace.json   # Codex marketplace catalogue
.claude/skills         # Symlink → ../plugins/eudi/skills (in-repo discovery)
.agents/skills         # Symlink → ../plugins/eudi/skills (in-repo discovery)
```

The canonical skill location is `plugins/eudi/skills/`. Both hosts copy a plugin
into a cache and skip symlinks pointing outside it, so `skills/` must be real
files — the two `skills` symlinks point the other way and exist only for
in-repo discovery.

## Use in your project

Install the plugin — see [Install](#install) above. No submodule, no vendored
copy, and no symlink into this repository: each host fetches the plugin from the
marketplace and caches its own copy.

If your project also installs skills with `gh skill`, keep `.agents/skills/` a
real, writable directory that your project owns. Pointing it at a shared corpus
would direct `gh skill install` writes into that other repository.

## Local development

```bash
git clone https://github.com/sourcelabbg/eudi-knowledge
cd eudi-knowledge
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# Regenerate all skills
python scripts/generate_all.py

# Bump the plugin version if generated content changed
python scripts/release.py
```

To try the plugin from a local checkout, register the repository as a
marketplace instead of publishing:

```bash
claude plugin marketplace add "$(pwd)" && claude plugin install eudi@eudi-knowledge
codex plugin marketplace add "$(pwd)" && codex plugin add eudi@eudi-knowledge
```

Local-path marketplaces read live from disk, so edits appear without
reinstalling. Both hosts require an absolute path or one starting with `./` —
a bare `.` is rejected.

## Updating

Skills are regenerated every Monday via GitHub Actions, which bumps the plugin
version when content changed. Consumers then run:

```bash
claude plugin marketplace update eudi-knowledge && claude plugin update eudi
codex plugin marketplace upgrade eudi-knowledge && codex plugin add eudi@eudi-knowledge
```

To regenerate manually in this repository:

```bash
python scripts/update.py          # only if new ARF version available
python scripts/update.py --force  # always regenerate
```

## Sources

- [ARF on GitHub](https://github.com/eu-digital-identity-wallet/eudi-doc-architecture-and-reference-framework)
- [EUDI Dev Hub](https://eu-digital-identity-wallet.github.io/eudi-doc-architecture-and-reference-framework/latest/)
- [OpenID4VP 1.0 Final](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html)
- [OpenID4VCI 1.0](https://openid.net/specs/openid-4-verifiable-credential-issuance-1_0.html)
- [HAIP 1.0](https://openid.net/specs/openid4vc-high-assurance-interoperability-profile-1_0.html)
- [SD-JWT (RFC 9901)](https://www.rfc-editor.org/rfc/rfc9901.html)
- [SD-JWT VC](https://www.ietf.org/archive/id/draft-ietf-oauth-sd-jwt-vc-08.html)
- [Token Status List](https://www.ietf.org/archive/id/draft-ietf-oauth-status-list-10.html)
- [W3C VC Data Model 2.0](https://www.w3.org/TR/vc-data-model-2.0/)
- [W3C Digital Credentials API](https://w3c-fedid.github.io/digital-credentials/)
