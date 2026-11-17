# Maintaining this repository

This repo publishes a reusable setup for personal knowledge vaults: a working agreement, skills, agents and the templates of its optional packs. Everything under `kit/` is copied into vaults, so it must work there on its own. The vault's commands come from [scripts-pkms](https://github.com/Zejnilovic/scripts-pkms) (pkm), installed once per machine. The kit needs the pkm version named in the `pkm version --require` line of `kit/AGENTS.md`.

**`kit/` is the product, not your instructions.** When you read files under `kit/`, Claude Code also loads `kit/CLAUDE.md`, which imports the vault's working agreement, and it may offer the kit's skills. Treat them as content you are editing. The rules in this file are the ones that apply to work on this repo.

## Before committing

- Run `python3 scripts/check.py`, with a clone of scripts-pkms next to this repo (or its path in `SCRIPTS_PKMS`). It checks every `pkm <command>` in kit/ and docs/ against `pkm help --all`. Without a clone it warns and skips; CI fails instead. CI runs it on Linux and macOS.
- A skill that needs a new pkm command waits for it: release the command in scripts-pkms first, by its rules, then raise the `pkm version --require` line in `kit/AGENTS.md` and use it here. Name the pkm release in the `CHANGELOG.md` entry.

## Versions and releases

- **Every change to `kit/` or `packs.txt` belongs to a version.** If the current version is already released (tagged), start a new one before or with the change: `bash scripts/bump.sh <version>`. It updates `VERSION`, the marker on the first line of `kit/AGENTS.md`, and adds an "(unreleased)" `CHANGELOG.md` heading with a TODO. Replace the TODO with what changed.
- **Pick the number by impact on vaults:** patch for wording and fixes, minor for new agents, skills, templates, commands or rules, major for renames or removals that need manual changes in vaults. A change to note names, link syntax, frontmatter fields or folders is major: vaults are full of notes that follow the old one.
- **Several changes can share one unreleased version.** Add a bullet to its `CHANGELOG.md` entry for each.
- **To release:** commit and push everything to the default branch, then run the **Release** workflow (Actions tab, or `gh workflow run release.yml`; `-f dry_run=true` pushes nothing). It runs the checks, moves the entry's text into a GitHub release, leaves a link under "## Released" in `CHANGELOG.md`, commits, and tags the commit `v<version>`. Don't release by hand.
- **agd** (github.com/Zejnilovic/agd) installs the kit from this repo's tags and `packs.txt`. A release whose `packs.txt` raises `min-agd` waits for that agd release.
- **`check.py` enforces this**, as in agentic-defaults.

## Compatibility

- **Editors**: vaults are plain Markdown with `[[name]]` links and YAML frontmatter, readable in any editor. Never require an editor or plugin; the script is the shared logic, and editors call it.
- **Assistants**: as in agentic-defaults. Agents need `name` and `description`; `model` and `skills` are read by Claude Code only. Don't set `tools`. Skills follow the Agent Skills format. Bodies describe actions, not one product's tools.
- **`kit/AGENTS.md`** is the single source of instructions; `kit/CLAUDE.md` only imports it.

## Write for everyday models

The rules of agentic-defaults apply: numbered steps, an explicit output format and stop conditions; concrete limits ("at most 10 findings"); short files. `kit/AGENTS.md` is loaded into every conversation, and `check.py` enforces a 700-word budget on the part above "This project". `model: sonnet` only for roles that mainly judge (chief of staff, coach, editor), `model: haiku` for roles that mainly read or file (retriever).

## Content rules

- [docs/methodology.md](docs/methodology.md) is the why, written for people. Keep the kit and it consistent, and update its last table when kit files are added or renamed.
- **The vault is the owner's.** The kit's rules protect the owner's words (agents capture and organize; they rewrite only when asked), never delete, and never invent. Keep every new skill and agent inside those rules.
- **Scripts move the owner's words; agents decide where.** Anything that files text works like `pkm post`: the agent proposes, the owner approves, the script copies, and a check proves nothing was lost.
- **Evidence on every summary.** Anything an agent summarizes links its source on every line, and the skill runs `pkm evidence` on it. A day page is never rewritten, so the source survives.
- **Nothing in the owner's name.** Nothing in the kit sends email, arranges meetings, posts, or commits and pushes unless the owner asks. People data and money get the strictest rules: facts only, no secrets, drafts instead of sending.
- **Generic only.** No real names, places, employers or other personal facts in the kit, its tests or its docs: use made-up examples such as Jane Doe, Apollo and Acme.
- **Context is the budget.** Every skill that writes notes keeps them findable (links, `## Now`, newest-first logs, reviews), and every skill that reads follows `vault-search`: summaries first, search, then lines.
- Agents are roles; skills are practices. An agent names the skills it uses and keeps a short version of their key rules. Roles don't hand work to each other.
- When adding, renaming or removing anything in `kit/`, update the tables in `README.md` and `packs.txt`. `check.py` fails when a skill, agent or pack has no row there.
- `docs/methodology.md` ends with a table of where each kit part lives; update it with the kit.
