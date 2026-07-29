# Plugin distribution: host compatibility and packaging validation

Validated 2026-07-29 against Claude Code 2.1.211 and `codex-cli` 0.146.0.

This note records what was actually tested on this machine, not only what the
documentation claims. Re-run the checks in [Validation log](#validation-log)
after a host upgrade before trusting them again.

## Topology

One plugin directory carries two host manifests. Both hosts read the same
`skills/` tree, so there is no per-host copy of the corpus and no generated
staging step.

```text
eudi-knowledge/
  .claude-plugin/marketplace.json     # Claude Code catalogue (repo root)
  .agents/plugins/marketplace.json    # Codex catalogue (repo root)
  plugins/eudi/
    .claude-plugin/plugin.json        # Claude Code manifest
    .codex-plugin/plugin.json         # Codex manifest
    skills/<skill-name>/SKILL.md      # canonical generated content, real files
  .claude/skills -> ../plugins/eudi/skills   # in-repo discovery only
  .agents/skills -> ../plugins/eudi/skills   # in-repo discovery only
```

Both hosts require the manifest to be the only thing inside its
`.<host>-plugin/` directory; `skills/` stays at the plugin root. Each host
ignores the other's manifest directory, and both preserve it verbatim when
caching the plugin.

### Why `skills/` must be real files, not a symlink

Claude Code copies a marketplace plugin into `~/.claude/plugins/cache` rather
than running it in place, and its symlink handling depends on where the target
resolves:

| Symlink target | Behaviour on install |
|---|---|
| Inside the plugin's own directory | Preserved as a relative symlink |
| Elsewhere in the same marketplace | Dereferenced, content copied |
| Outside the marketplace | **Skipped for security** |

For `--plugin-dir` and local-path installs the rule is stricter: only symlinks
resolving inside the plugin's own directory survive, everything else is skipped.

A `plugins/eudi/skills -> ../../<elsewhere>` link would therefore be dropped in
exactly the case developers test with first. So the generators write the real
tree into `plugins/eudi/skills/`, and the two in-repo `skills` entries are the
symlinks pointing the other way. They exist only so this repository can load its
own skills while you work on it; neither is part of a published package.

### Why the plugin is not the repository root

Both layouts appear in the wild. Anthropic's official marketplace (276 entries)
resolves 55 plugins through in-repo `./plugins/<name>` paths and another 79
through `git-subdir` with `path: plugins/<name>`, while 142 point at a whole
repository. `nrwl/nx-ai-agents-config` takes the whole-repo route.

This repository uses `plugins/eudi/` because it is a *generator* repository: a
whole-repo package would copy `scripts/`, `docs/`, `requirements.txt`, and the
test tooling into every user's plugin cache alongside the skills. The
subdirectory keeps the published payload to manifests, `skills/`, and a README.

Relative supporting files inside a skill (`references/`, `scripts/`, `assets/`)
survive caching on both hosts — verified below.

## Skill naming

Plugin skills are namespaced by plugin name on Claude Code, so every skill
gains an `eudi:` prefix:

| Context | Invocation |
|---|---|
| This repository, via `.claude/skills` | `/arf-glossary` |
| Installed as a plugin | `/eudi:arf-glossary` |

Model-invoked use is unaffected — Claude and Codex still select skills from
their `description` frontmatter. Only the explicit slash-command form changes.
Because namespacing is what prevents collisions between plugins, this is not
something to work around.

## Subagents: Claude only, so roles ship as skills

Claude Code plugins support an `agents/` component. Codex plugins do not — its
manifest only points at `skills`, `mcpServers`, `hooks`, and the compatibility
`apps` field, and the component list in its authoring docs has no agent entry.

So the portable primitive for a specialist role is a **skill**, and each role is
authored once as a skill that both hosts load:

| Role | Skill (both hosts) | Subagent (Claude only) |
|---|---|---|
| EUDI standards generalist | `eudi-expert` | `@eudi:eudi-expert` |
| OpenID4VP security audit | `oid4vp-security-auditor` | `@eudi:oid4vp-security-auditor` |
| ARF trust architecture | `arf-trust-architect` | `@eudi:arf-trust-architect` |
| OpenID4VCI issuer review | `oid4vci-issuer-reviewer` | `@eudi:oid4vci-issuer-reviewer` |

The four files in `plugins/eudi/agents/` are deliberately thin: each carries
`name`, `description`, and `disallowedTools: Write, Edit, Bash`, and its body
tells the subagent to load the matching role skill and follow it. The role text
therefore lives in exactly one place. Claude users get real context isolation
(the corpus lookup happens in a separate window); Codex users invoke the same
role as a skill in the main conversation.

These four role skills are **hand-authored** and live alongside the generated
corpus, so `clean_old_skills()` in `scripts/common.py` skips the names in
`HAND_WRITTEN_SKILLS`. Adding a role means adding it to that set, or the next
regeneration deletes it.

`agents` is not a valid manifest field value as a bare directory string —
`claude plugin validate` rejects `"agents": "./agents"` with
`agents: Invalid input`. Leave it undeclared; `agents/` at the plugin root is a
default location and is discovered automatically. Codex ships the directory in
its cache and ignores it.

## Two catalogues, one identity

Codex documents its repo marketplace at `.agents/plugins/marketplace.json` and
accepts `.claude-plugin/marketplace.json` as a legacy-compatible fallback. That
fallback is real, not just documented: the `nx-claude-plugins` marketplace
installed on this machine ships only `.claude-plugin/marketplace.json`, uses
Claude's `{"source": "github", ...}` entry shape, and Codex consumes it.

The dual-manifest shape is also what a real multi-host plugin does:
`nrwl/nx-ai-agents-config` ships `.claude-plugin/` and `.cursor-plugin/` side by
side in one plugin directory, each with its own `plugin.json` describing the same
`skills/` tree.

This repository still ships both catalogue files, each in its host's native
form, because the entry schemas differ:

```jsonc
// .claude-plugin/marketplace.json — string relative path
{ "name": "eudi", "source": "./plugins/eudi" }

// .agents/plugins/marketplace.json — object source
{ "name": "eudi", "source": { "source": "local", "path": "./plugins/eudi" } }
```

Two catalogues can drift. `python scripts/release.py --check` fails if the
marketplace name or plugin list disagree, or if either entry pins its own
`version` — `plugin.json` is the single source of truth for the version, and a
marketplace-level pin would shadow it on one host but not the other. CI runs
this check on every regeneration.

## Versioning

Both hosts hand users a new version only when the manifest `version` string
changes, and Codex requires `version` (so omitting it to fall back to the git
SHA, which Claude Code supports, is not an option).

`scripts/release.py` computes `<ARF major>.<ARF minor>.<revision>`:

- `<ARF major>.<ARF minor>` comes from `.arf-version`, the tracked ARF release.
- `<revision>` increments when the SHA-256 over every generated `SKILL.md`
  changes, and resets to 0 when the ARF major/minor moves.

State lives in `.plugin-version.json`. The script writes the resulting version
into both manifests, so a regeneration that changes no content produces no
version churn and no spurious update for users.

## Validation log

Performed with a scratch marketplace holding a 2-skill plugin, then a third
skill added for the upgrade step.

| # | Check | Claude Code | Codex |
|---|---|---|---|
| 1 | Manifest/marketplace validates | ✓ `claude plugin validate <root> --strict` → passed | n/a (no validate subcommand) |
| 2 | Marketplace registers from local path | ✓ `claude plugin marketplace add` | ✓ `codex plugin marketplace add`, resolved via `.agents/plugins/marketplace.json` |
| 3 | Plugin installs | ✓ `claude plugin install eudi@eudi-knowledge` | ✓ `codex plugin add eudi@eudi-knowledge` |
| 4 | Skills listed **separately** | ✓ `claude plugin details eudi` → `Skills (2) proto-one, proto-two` | ✓ `codex plugin list` → installed, enabled |
| 5 | Other host's manifest survives caching | ✓ `.codex-plugin/plugin.json` present in cache | ✓ `.claude-plugin/plugin.json` present in cache |
| 6 | Relative supporting file survives caching | ✓ `skills/proto-two/references/extra.md` | ✓ same |
| 7 | Adding a skill + version bump is picked up | ✓ `details` → `Skills (3)`, version `0.0.2` | ✓ re-`add` → cache `.../eudi/0.0.2` |

Then repeated against the real 162-skill corpus at version `3.0.2`:

| # | Check | Claude Code | Codex |
|---|---|---|---|
| 8 | Full corpus validates | ✓ `claude plugin validate . --strict` → passed | n/a |
| 9 | Every skill listed separately | ✓ `Skills (162)` | ✓ 162 directories in cache |
| 10 | Subagents discovered | ✓ `Agents (4)` | n/a — `agents/` shipped but ignored |
| 11 | No symlinks leaked into the cache | ✓ `find <cache> -type l` → 0 | ✓ same |
| 12 | Always-on context cost | ~14,585 tok per session | not reported by the CLI |

Cache layout is identical in shape on both hosts:
`~/.claude/plugins/cache/<marketplace>/<plugin>/<version>/` and
`~/.codex/plugins/cache/<marketplace>/<plugin>/<version>/`.

### Known limits found during validation

- **Local-path marketplaces are live, not snapshotted, on Claude Code.**
  After bumping the source to `0.0.2`, `claude plugin details eudi` reported
  `0.0.2` with 3 skills while `~/.claude/plugins/cache/.../0.0.1` was still the
  only cached version. `claude plugin update eudi` fails with
  `Plugin "eudi" not found` for a local-path marketplace. This is a development
  convenience, not a bug to route around: local paths reload as you edit.
- **`codex plugin marketplace upgrade` requires a git marketplace.** Against a
  local path it errors with `marketplace ... is not configured as a Git
  marketplace`. Re-running `codex plugin add` picks up the new version.
- **`file://` git URLs are rejected by both hosts.** Claude Code wants
  `owner/repo`, `https://...`, or `./path`; Codex wants `owner/repo`, a git
  URL, or a local path. A local bare repository therefore cannot stand in for
  GitHub, which is why step 7 was validated by version bump rather than by
  `git`-sourced `update`/`upgrade`.
- **Not yet validated: the `git`-sourced install and upgrade.** This needs the
  marketplace pushed to `github.com/sourcelabbg/eudi-knowledge`. Until then the
  team flow below is documentation-derived for the fetch/pin step, while
  everything about package layout, discovery, and caching is verified.

## Team install and update flow

Once the marketplace is on the default branch of the GitHub repository:

```bash
# Claude Code
claude plugin marketplace add sourcelabbg/eudi-knowledge
claude plugin install eudi@eudi-knowledge

# Codex
codex plugin marketplace add sourcelabbg/eudi-knowledge
codex plugin add eudi@eudi-knowledge
```

Updating:

```bash
# Claude Code — refresh the catalogue, then the plugin
claude plugin marketplace update eudi-knowledge
claude plugin update eudi

# Codex — refresh the git snapshot, then re-add
codex plugin marketplace upgrade eudi-knowledge
codex plugin add eudi@eudi-knowledge
```

Because `plugin.json` pins an explicit `version`, neither host offers an update
until `scripts/release.py` bumps it. The weekly CI job regenerates the corpus,
bumps the revision when content changed, and pushes — so a normal update lands
within a week of an upstream ARF release, or immediately on a manual dispatch.

To pin a team to an exact release, add the marketplace at a tag. `claude plugin
marketplace add` has no `--ref` flag — Claude Code takes a `#<ref>` suffix on a
full git URL, while Codex takes `owner/repo@<ref>` or `--ref`:

```bash
claude plugin marketplace add https://github.com/sourcelabbg/eudi-knowledge.git#eudi--v3.0.2
codex plugin marketplace add sourcelabbg/eudi-knowledge@eudi--v3.0.2
```

`claude plugin tag plugins/eudi` creates the matching `eudi--v<version>` tag and
validates that `plugin.json` and the marketplace entry agree before tagging.

Full install, update, team-setup, and troubleshooting instructions live in
[installing.md](installing.md).

## Consuming from another repository (replacing a submodule)

A consumer such as Panacea does not need this repository vendored at all:

- Remove the `eudi-knowledge` submodule and any `.claude/skills` or
  `.agents/skills` symlink pointing into it.
- Install the plugin per host as above. Skills arrive namespaced (`/eudi:*`).
- Keep `.agents/skills/` as a **real, writable directory** owned by the
  consumer. `gh skill install` writes there, and pointing it at a shared corpus
  would direct those writes into this repository. Vendor skills such as
  `github/gh-stack` stay independently installed and updated with `gh skill`;
  the plugin is not a delivery mechanism for them.

`claude --add-dir` also exposes a directory's `.claude/skills`, but it applies
per launch and has no Codex equivalent, so it is a local convenience rather
than a distribution mechanism.

## Sources

- [Claude Code: create plugins](https://code.claude.com/docs/en/plugins)
- [Claude Code: plugins reference](https://code.claude.com/docs/en/plugins-reference)
- [Claude Code: plugin marketplaces](https://code.claude.com/docs/en/plugin-marketplaces)
- [Codex: build plugins](https://developers.openai.com/plugins/build/plugins)
- [Codex: build skills](https://developers.openai.com/plugins/build/skills)
- [Agent Skills specification](https://agentskills.io/specification)
- [GitHub CLI: `gh skill install`](https://cli.github.com/manual/gh_skill_install)
