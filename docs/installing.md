# Installing and updating the EUDI Knowledge plugin

The plugin ships 162 skills and 4 subagents from one directory that both Claude
Code and Codex install. Commands below were exercised against Claude Code
2.1.211 and `codex-cli` 0.146.0; see [plugin-distribution.md](plugin-distribution.md)
for the full validation log and the packaging rationale.

- [Install](#install)
- [Verify](#verify)
- [Use it](#use-it)
- [Update](#update)
- [Install for a whole team](#install-for-a-whole-team)
- [Pin to a specific release](#pin-to-a-specific-release)
- [Turn it off where you don't need it](#turn-it-off-where-you-dont-need-it)
- [Uninstall](#uninstall)
- [Install from a local clone](#install-from-a-local-clone)
- [Troubleshooting](#troubleshooting)

## Install

Adding a marketplace only registers the catalogue; you then install the plugin
from it. Both steps are needed.

### Claude Code

```bash
claude plugin marketplace add sourcelabbg/eudi-knowledge
claude plugin install eudi@eudi-knowledge
```

Then, inside a session, activate it without restarting:

```text
/reload-plugins
```

`claude plugin install` writes to **user** scope by default — available in all
your projects. Pass `--scope` to change that:

| Scope | Flag | Written to | Who gets it |
|---|---|---|---|
| User | `--scope user` (default) | `~/.claude/settings.json` | You, in every project |
| Project | `--scope project` | `.claude/settings.json` | Everyone on the repository (commit it) |
| Local | `--scope local` | `.claude/settings.local.json` | You, in this repository only |

The same flag exists on `marketplace add`, `update`, `uninstall`, `enable`, and
`disable`. Keep the marketplace and the plugin in the same scope.

### Codex

```bash
codex plugin marketplace add sourcelabbg/eudi-knowledge
codex plugin add eudi@eudi-knowledge
```

Codex has no scope flag — installs are per user, recorded in
`~/.codex/config.toml`. Start a new session to pick the plugin up.

## Verify

```bash
# Claude Code — component inventory and context cost
claude plugin details eudi
claude plugin list

# Codex — install state and resolved path
codex plugin list | grep eudi
```

A healthy Claude Code install reports:

```text
EUDI Knowledge (eudi) 3.0.2
  Skills (162)  arf-annex3-mdl-rulebook, arf-annex3-pid-rulebook, ...
  Agents (4)  arf-trust-architect, oid4vp-security-auditor, ...
  Always-on:   ~14,585 tok   added to every session
```

If the skill count is far lower, or `Skills (0)`, see
[Troubleshooting](#troubleshooting).

## Use it

Plugin skills are **namespaced by plugin name**, so explicit invocation gains an
`eudi:` prefix:

```text
/eudi:arf-glossary
/eudi:oid4vp-security
```

You rarely need to type them. Both hosts select skills automatically from their
`description` frontmatter, which is why all 162 descriptions stay in context.

The four specialist roles are the intended entry points:

| Role | Skill (both hosts) | Claude subagent |
|---|---|---|
| General EUDI standards specialist | `eudi-expert` | `@eudi:eudi-expert` |
| OpenID4VP security/privacy audit | `oid4vp-security-auditor` | `@eudi:oid4vp-security-auditor` |
| ARF trust model and actor lifecycle | `arf-trust-architect` | `@eudi:arf-trust-architect` |
| OpenID4VCI issuer review | `oid4vci-issuer-reviewer` | `@eudi:oid4vci-issuer-reviewer` |

On Claude Code, delegating to the subagent keeps the corpus lookup in its own
context window and returns only conclusions:

```text
@eudi:oid4vp-security-auditor Audit this direct_post response handling.
```

Codex plugins have no agent component, so there the roles are skills only.

## Update

Refresh the catalogue first, then the plugin — one step is not enough.

```bash
# Claude Code
claude plugin marketplace update eudi-knowledge
claude plugin update eudi@eudi-knowledge

# Codex
codex plugin marketplace upgrade eudi-knowledge
codex plugin add eudi@eudi-knowledge
```

Claude Code needs a restart, or `/reload-plugins`, to apply the new version.
Codex re-runs `plugin add` to install over the previous version.

Note the `eudi@eudi-knowledge` form: `update` is the one command that rejects the
bare plugin name, failing with `Plugin "eudi" not found` even though the plugin
is installed. `install`, `details`, `enable`, and `disable` all accept `eudi`.

**Nothing will appear until the version string changes.** `plugin.json` pins an
explicit `version`, so both hosts consider you current until it moves.
`scripts/release.py` bumps it only when generated content actually changed, so a
regeneration that produces identical skills causes no update churn. The weekly
CI job regenerates, bumps, and pushes — so an upstream ARF release normally
reaches you within a week.

Version numbers track the ARF release they were built from:
`<ARF major>.<ARF minor>.<revision>`. `3.0.2` means "built from ARF v3.0.0,
third revision".

### Automatic updates (Claude Code)

Third-party marketplaces have auto-update **disabled** by default. To enable it
for this one: run `/plugin`, open **Marketplaces**, select `eudi-knowledge`, and
choose **Enable auto-update**. Claude Code then refreshes it in the background
shortly after startup and prompts you to `/reload-plugins` when a new version
lands.

## Install for a whole team

### Claude Code — commit it to the repository

Add both keys to your project's `.claude/settings.json` and commit. Teammates
are prompted to install when they trust the folder.

```json
{
  "extraKnownMarketplaces": {
    "eudi-knowledge": {
      "source": {
        "source": "github",
        "repo": "sourcelabbg/eudi-knowledge"
      }
    }
  },
  "enabledPlugins": {
    "eudi@eudi-knowledge": true
  }
}
```

`enabledPlugins` alone is not sufficient for a plugin from an external source —
it stays listed as not installed until the teammate runs the install. Running
`claude plugin install eudi@eudi-knowledge --scope project` writes both keys for
you.

### Codex — document the two commands

Codex does **not** auto-discover a marketplace committed to a repository. A
`.agents/plugins/marketplace.json` in your project is ignored until someone runs
`codex plugin marketplace add`, which was verified by probing a repository
containing one. So for Codex, put the two install commands in your project's
README or setup script:

```bash
codex plugin marketplace add sourcelabbg/eudi-knowledge
codex plugin add eudi@eudi-knowledge
```

State is recorded per user in `~/.codex/config.toml`:

```toml
[marketplaces.eudi-knowledge]
source_type = "git"
source = "https://github.com/sourcelabbg/eudi-knowledge.git"

[plugins."eudi@eudi-knowledge"]
enabled = true
```

## Pin to a specific release

Useful when you want every engineer on an identical corpus.

```bash
# Claude Code — append #<ref> to a full git URL
claude plugin marketplace add https://github.com/sourcelabbg/eudi-knowledge.git#eudi--v3.0.2

# Codex — owner/repo@<ref>, or the --ref flag
codex plugin marketplace add sourcelabbg/eudi-knowledge@eudi--v3.0.2
codex plugin marketplace add sourcelabbg/eudi-knowledge --ref eudi--v3.0.2
```

`claude plugin marketplace add` has **no** `--ref` flag — the `#<ref>` suffix on a
git URL is the documented mechanism. Use the full `https://...git` form: the
`owner/repo` shorthand accepts a `#<ref>` suffix without erroring but is not
documented to honour it, and it resolves to the same cache directory as the
unpinned shorthand.

Pinning is the one part of this guide not exercised end to end here — it needs
the marketplace published with tags. Everything else was run against a live
install.

Release tags are created with `claude plugin tag plugins/eudi`, which validates
that `plugin.json` and the marketplace entry agree before tagging and produces
`eudi--v<version>`.

## Turn it off where you don't need it

All 162 skill descriptions are always-on so the model can choose between them —
roughly 14,600 tokens in every session. That is worth paying on EUDI work and
not otherwise, so disable it elsewhere rather than uninstalling:

```bash
# Claude Code — disable for this repository only
claude plugin disable eudi --scope local
claude plugin enable eudi --scope local

# Codex
codex plugin remove eudi@eudi-knowledge
```

Codex has no disable command, only removal. Alternatively edit
`~/.codex/config.toml` and set `enabled = false` under
`[plugins."eudi@eudi-knowledge"]`.

## Uninstall

```bash
# Claude Code
claude plugin uninstall eudi
claude plugin marketplace remove eudi-knowledge

# Codex
codex plugin remove eudi@eudi-knowledge
codex plugin marketplace remove eudi-knowledge
```

On Claude Code, removing a marketplace also uninstalls the plugins installed
from it, so the second command alone is enough. Add `--scope` to target a
non-user scope. Pass `--keep-data` to preserve
`~/.claude/plugins/data/{id}/`.

## Install from a local clone

For working on the corpus itself, register the checkout as a marketplace instead
of publishing:

```bash
git clone https://github.com/sourcelabbg/eudi-knowledge
cd eudi-knowledge

claude plugin marketplace add "$(pwd)" && claude plugin install eudi@eudi-knowledge
codex plugin marketplace add "$(pwd)" && codex plugin add eudi@eudi-knowledge
```

Both hosts need an absolute path or one starting with `./` — a bare `.` is
rejected with `Invalid marketplace source format`.

Local-path marketplaces are read live rather than snapshotted on Claude Code, so
edits to `plugins/eudi/skills/` show up without reinstalling. Two consequences:

- Nothing to update: the plugin is already live, so `claude plugin update` has
  no work to do.
- `codex plugin marketplace upgrade` errors with `not configured as a Git
  marketplace`. Re-run `codex plugin add` to pick up a version bump.

## Troubleshooting

| Symptom | Cause and fix |
|---|---|
| `Invalid marketplace source format` | A bare `.` is rejected. Use `"$(pwd)"` or `./path`. For non-GitHub hosts include `https://` and the `.git` suffix. |
| `Plugin "eudi" not found in marketplace` | Local catalogue is stale. `claude plugin marketplace update eudi-knowledge`, then retry. |
| Skills don't appear after installing | Run `/reload-plugins`. Note its summary counts only `commands/`, so it can report `0 skills` even when the 162 loaded — confirm with `claude plugin details eudi`. |
| Still no skills | Stale cache. `rm -rf ~/.claude/plugins/cache`, restart, reinstall. |
| `/arf-glossary` not recognised | Plugin skills are namespaced: `/eudi:arf-glossary`. |
| `claude plugin update eudi` → `Plugin "eudi" not found` | `update` is the one command that needs the fully-qualified id: `claude plugin update eudi@eudi-knowledge`. |
| `marketplace ... is not configured as a Git marketplace` | `codex plugin marketplace upgrade` only works on git sources. Re-run `codex plugin add`. |
| Context feels heavy on unrelated work | Expected — ~14,600 always-on tokens. [Disable it](#turn-it-off-where-you-dont-need-it) outside EUDI projects. |
| `@eudi:eudi-expert` does nothing in Codex | Codex plugins have no agent component. Use the `eudi-expert` skill instead. |

## A note for repositories that also use `gh skill`

Keep `.agents/skills/` a real, writable directory owned by your project. If you
point it at a shared corpus, `gh skill install` writes land in that other
repository. This plugin is installed through the host's own plugin cache and
never needs a symlink in your project, so the two mechanisms don't collide.
