# Changelog

What changed in the kit. The next version's changes are collected here; each released version's notes, including manual steps for existing vaults, are on its GitHub release, linked below. To see what an update would change in a vault, run `agd status` there.

Version numbers: **major** when something is renamed or removed and existing vaults need manual changes, **minor** for new agents, skills, templates, commands or rules, **patch** for wording and fixes. Before 1.0, a minor version may also need manual changes; its notes list them under "Manual steps". Each release is a git tag (`v0.1.0`), and the first line of a vault's `AGENTS.md` shows which version its copy came from.

## 0.6.0 (unreleased)

- Needs pkm 0.11.0 (`pkm version --require 0.11`), for `pkm new --set/--folder/--url`, `pkm set` (which moves a project's folder along), `pkm mv` with several notes, `pkm config <key> <value>`, the `part_of_folders` setting and `pkm check`'s notices for doubled addresses and archived parents. The agreement's too-old message also gives `brew upgrade pkm`.
- New core skill `organizing`: making, connecting, moving and tidying notes as one numbered table of pkm commands, run after a yes, with names, clashes (`<name>-repo`), `part_of` and project folders spelled out. The chief of staff uses it.
- The `projects` skill now sets up a project and connects its repositories: it lists them with `gh repo list` or `az repos list` by prefix, and proposes `pkm new repo --url <address> --set part_of=<project>` for each. Rounds, what's new, updates and cycle summaries moved to a new `rounds` skill in the same pack.
- The working agreement: a request such as "set up X" is not the approval of what it proposes; notes are made, changed and moved only with pkm, never by editing frontmatter by hand; `summary` is written with `pkm set`; it names `.claude/skills/organizing/SKILL.md` before making or moving several notes, and says where skills are, for assistants that don't load them. The line pointing to `pkm help` went, for the words.
- A note moved into a project's folder also gets `part_of` (the `organizing` and `projects` skills), so `--under` and `pkm overview` find it.
- Drills (`scripts/drill.py`, `tests/drills/`): the kit tried by a real assistant on a made-up vault, with a fake `gh`, and graded: connecting repositories, project folders, tidying a mess and finishing a project. The rules above came from Haiku's runs of them.
- From those runs: a yes covers only the rows it answers; a line no longer true is struck with `pkm strike`, never by editing it; a person, team, application or area is never `part_of` a project; and the agreement names `ls`, `cat`, `find` and `grep` as never run on notes. `pkm check` runs as part of "Done means".
- `organizing` also covers which notes belong under a project (never people, teams, applications or areas), moving a project under an application, finishing one (each note archived or moved to what outlives it, the project last), and a fuller tidy-up driven by `pkm check`'s notices. It looks with pkm only, never `ls`, `cat` or `find`, and reports from pkm's output.
- Settings are set with `pkm config <key> <value>`, never by hand: in `organizing`, `projects` and `pkms-init`. `pkms-init` now also sets `shared=yes` for a shared vault, which it only implied before.
- The guard, `.claude/settings.json` in the core pack: Claude Code asks the owner before an agent runs `rm`, `mv`, `cp`, `sed -i`, `find` (which can delete) or `xargs`, or edits a day page or a note in `archive/`, even when edits are accepted automatically. pkm's own commands, such as `pkm mv`, don't start with those words, so they run as before; so do edits of `## Now` and close pages. rtk's rewrites keep the rules: Claude Code checks the command as written. Copilot and other assistants don't read the file. A vault that already has its own `.claude/settings.json` keeps it: agd reports it as taken, and its rules can be copied in by hand. In a drill's non-interactive run, an asked command is refused. It is a seatbelt, not a sandbox: a model set on deleting can still find another way.
- `pkms-init` asks whether a project's notes should sit in a folder of their own (`part_of_folders=yes`). The ledger, study, coaching and writing skills fill and change frontmatter with `--set` and `pkm set`.

## Released

- [0.5.0](https://github.com/Zejnilovic/agentic-pkms/releases/tag/v0.5.0) (2026-11-23)
- [0.4.2](https://github.com/Zejnilovic/agentic-pkms/releases/tag/v0.4.2) (2026-11-22)
- [0.4.1](https://github.com/Zejnilovic/agentic-pkms/releases/tag/v0.4.1) (2026-11-20)
- [0.4.0](https://github.com/Zejnilovic/agentic-pkms/releases/tag/v0.4.0) (2026-11-20)
- [0.3.0](https://github.com/Zejnilovic/agentic-pkms/releases/tag/v0.3.0) (2026-11-20)
- [0.2.0](https://github.com/Zejnilovic/agentic-pkms/releases/tag/v0.2.0) (2026-11-19)
- [0.1.0](https://github.com/Zejnilovic/agentic-pkms/releases/tag/v0.1.0) (2026-11-18)
