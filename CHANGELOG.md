# Changelog

What changed in the kit. The next version's changes are collected here; each released version's notes, including manual steps for existing vaults, are on its GitHub release, linked below. To see what an update would change in a vault, run `agd status` there.

Version numbers: **major** when something is renamed or removed and existing vaults need manual changes, **minor** for new agents, skills, templates, commands or rules, **patch** for wording and fixes. Before 1.0, a minor version may also need manual changes; its notes list them under "Manual steps". Each release is a git tag (`v0.1.0`), and the first line of a vault's `AGENTS.md` shows which version its copy came from.

## 0.6.0 (unreleased)

- Needs pkm 0.10.0 (`pkm version --require 0.10`), for `pkm new --set/--folder/--url`, `pkm set`, `pkm mv` with several notes and the `part_of_folders` setting.
- New core skill `organizing`: making, connecting, moving and tidying notes as one numbered table of pkm commands, run after a yes, with names, clashes (`<name>-repo`), `part_of` and project folders spelled out. The chief of staff uses it.
- The `projects` skill now sets up a project and connects its repositories: it lists them with `gh repo list` or `az repos list` by prefix, and proposes `pkm new repo --url <address> --set part_of=<project>` for each. Rounds, what's new, updates and cycle summaries moved to a new `rounds` skill in the same pack.
- The working agreement: a request such as "set up X" is not the approval of what it proposes; notes are made, changed and moved only with pkm, never by editing frontmatter by hand; `summary` is written with `pkm set`; it names `.claude/skills/organizing/SKILL.md` before making or moving several notes, and says where skills are, for assistants that don't load them. The line pointing to `pkm help` went, for the words.
- A note moved into a project's folder also gets `part_of` (the `organizing` and `projects` skills), so `--under` and `pkm overview` find it.
- Drills (`scripts/drill.py`, `tests/drills/`): the kit tried by a real assistant on a made-up vault, with a fake `gh`, and graded. The rules above came from Haiku's runs of them.
- `pkms-init` asks whether a project's notes should sit in a folder of their own (`part_of_folders=yes`). The ledger, study, coaching and writing skills fill and change frontmatter with `--set` and `pkm set`.

## Released

- [0.5.0](https://github.com/Zejnilovic/agentic-pkms/releases/tag/v0.5.0) (2026-11-23)
- [0.4.2](https://github.com/Zejnilovic/agentic-pkms/releases/tag/v0.4.2) (2026-11-22)
- [0.4.1](https://github.com/Zejnilovic/agentic-pkms/releases/tag/v0.4.1) (2026-11-20)
- [0.4.0](https://github.com/Zejnilovic/agentic-pkms/releases/tag/v0.4.0) (2026-11-20)
- [0.3.0](https://github.com/Zejnilovic/agentic-pkms/releases/tag/v0.3.0) (2026-11-20)
- [0.2.0](https://github.com/Zejnilovic/agentic-pkms/releases/tag/v0.2.0) (2026-11-19)
- [0.1.0](https://github.com/Zejnilovic/agentic-pkms/releases/tag/v0.1.0) (2026-11-18)
