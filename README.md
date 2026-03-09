# eudi-knowledge

OpenCode skills derived from official EUDI Wallet / eIDAS2 specifications.

## What's in here

Structured [OpenCode skills](https://opencode.ai/docs/skills/) split from the
[EUDI Wallet Architecture and Reference Framework (ARF)](https://github.com/eu-digital-identity-wallet/eudi-doc-architecture-and-reference-framework)
and related specs. Load them in any project where you're building on the EUDI ecosystem.

## Custom Subagents (`@` mentions)

The project includes custom OpenCode subagents in `.ai/agents/` (exposed at
`.opencode/agents/` via symlink). The
filename maps directly to the `@` handle.

| Handle | File | Purpose |
|---|---|---|
| `@eudi-expert` | `.ai/agents/eudi-expert.md` | General EUDI standards specialist across ARF, OID4VP, and OID4VCI. |
| `@oid4vp-security-auditor` | `.ai/agents/oid4vp-security-auditor.md` | Security/privacy audit for OpenID4VP requests, responses, and verifier checks. |
| `@arf-trust-architect` | `.ai/agents/arf-trust-architect.md` | Trust model and actor lifecycle architecture guidance based on ARF. |
| `@oid4vci-issuer-reviewer` | `.ai/agents/oid4vci-issuer-reviewer.md` | Issuer-side OpenID4VCI flow review and hardening checklist. |

Use them by mentioning the handle in chat, for example:

```text
@eudi-expert What skills apply to this wallet presentation flow?
@oid4vp-security-auditor Audit this direct_post response handling.
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
| `hlr-03-pid-rulebook` | Annex 3.01 | PID Rulebook — attribute schemas, mdoc/SD-JWT VC encoding, trust anchors |
| `hlr-04-mdl-rulebook` | Annex 3.02 | mDL Rulebook — attribute schema, ISO 18013-5 encoding |
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
| `w3c-dc-api-core` | W3C DC API §1–7 | DigitalCredential interface, credential management |
| `w3c-dc-api-security` | W3C DC API §8–10 | Security, privacy, accessibility |

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
.ai/
  skills/              # Canonical generated skill files (~150 skills)
  agents/              # Canonical custom OpenCode subagents
  commands/            # Canonical OpenCode command docs
.opencode/skills/      # Compatibility symlink to .ai/skills
.opencode/agents/      # Compatibility symlink to .ai/agents
.opencode/commands/    # Compatibility symlink to .ai/commands
```

## Setup

```bash
git clone https://github.com/sourcelabbg/eudi-knowledge
cd eudi-knowledge
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# Generate all skills
python scripts/generate_all.py
```

## Use in your project

### Option A — Symlink globally (single developer)

```bash
ln -s $(pwd)/.ai/skills/* ~/.config/opencode/skills/
```

### Option B — Reference in your project's opencode.json

```json
{
  "instructions": [
    "https://raw.githubusercontent.com/sourcelabbg/eudi-knowledge/main/AGENTS.md"
  ]
}
```

### Option C — Git submodule in your monorepo

```bash
git submodule add https://github.com/sourcelabbg/eudi-knowledge packages/eudi-knowledge
```

## Updating

Skills are auto-updated every Monday via GitHub Actions.
To update manually:

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
