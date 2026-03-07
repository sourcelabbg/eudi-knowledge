# eudi-knowledge

OpenCode skills derived from official EUDI Wallet / eIDAS2 specifications.

## What's in here

Structured [OpenCode skills](https://opencode.ai/docs/skills/) split from the
[EUDI Wallet Architecture and Reference Framework (ARF)](https://github.com/eu-digital-identity-wallet/eudi-doc-architecture-and-reference-framework)
and related specs. Load them in any project where you're building on the EUDI ecosystem.

## Skills

| Skill | Source | Content |
|---|---|---|
| `arf-glossary` | ARF Annex 1 | Term definitions |
| `arf-ecosystem-roles` | ARF §3 | All ecosystem roles |
| `arf-architecture` | ARF §4.1–4.3 | Design principles, reference architecture, components |
| `arf-wscd-states` | ARF §4.5–4.7 | WSCD types, state lifecycles, pseudonyms |
| `arf-presentation-flows` | ARF §4.4 + §5.6 | Remote/proximity flows, OID4VP |
| `arf-data-model` | ARF §5 | Credential formats, attestation categories |
| `arf-trust-model` | ARF §6.1–6.4 | Trust framework, provider registration |
| `arf-wallet-lifecycle` | ARF §6.5 | Wallet Unit install, activation, management |
| `arf-issuance-reqs` | ARF §6.6.1–6.6.2 | PID/attestation issuance, batch issuance |
| `arf-presentation-reqs` | ARF §6.6.3.1–5 | Wallet-side presentation trust, RP auth |
| `arf-rp-verification` | ARF §6.6.3.6–13 | RP-side verification, revocation, binding |
| `arf-attestation-mgmt` | ARF §6.6.4–7 | Attestation management, refresh, deletion |
| `arf-wallet-reqs` | ARF §7 | Wallet certification, conformity assessment |
| `oid4vp-*` (8 skills) | OID4VP 1.0 Final | Authorization requests, DCQL, responses, metadata, security, DC API, credential formats |

## Setup

```bash
git clone https://github.com/your-org/eudi-knowledge
cd eudi-knowledge
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# Generate skills from latest ARF
python scripts/split_arf.py
```

## Use in your project

### Option A — Symlink globally (single developer)

```bash
ln -s $(pwd)/.opencode/skills/* ~/.config/opencode/skills/
```

### Option B — Reference in your project's opencode.json

```json
{
  "instructions": [
    "https://raw.githubusercontent.com/your-org/eudi-knowledge/main/AGENTS.md"
  ],
  "mcp": {
    "eudi-skills": {
      "type": "local",
      "command": "..."
    }
  }
}
```

### Option C — Git submodule in your monorepo

```bash
git submodule add https://github.com/your-org/eudi-knowledge packages/eudi-knowledge
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
- [OpenID4VCI](https://openid.net/specs/openid-4-verifiable-credential-issuance-1_0.html)
