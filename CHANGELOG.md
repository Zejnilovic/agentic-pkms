# Changelog

What changed in the kit. The next version's changes are collected here; each released version's notes, including manual steps for existing vaults, are on its GitHub release, linked below. To see what an update would change in a vault, run `agd status` there.

Version numbers: **major** when something is renamed or removed and existing vaults need manual changes, **minor** for new agents, skills, templates, commands or rules, **patch** for wording and fixes. Before 1.0, a minor version may also need manual changes; its notes list them under "Manual steps". Each release is a git tag (`v0.1.0`), and the first line of a vault's `AGENTS.md` shows which version its copy came from.

## 0.2.0 (unreleased)

- **Events** (pkm 0.3.0): the brief opens with a Today list of today's events, and its Needs attention list includes the events of the coming days. The close lists the events in `== due` with the other dates. The `tasks` skill writes events (`(at …)` or `(@ …)`, and `(every …)` for one that comes back), changes one by striking and rewriting it, and writes a calendar file with `pkm upcoming --ics` when asked. `check-in`, `posting` and the chief of staff follow suit.
- **pkm 0.3**: the kit needs pkm 0.3 ([scripts-pkms](https://github.com/Zejnilovic/scripts-pkms) 0.3.0); its checks run against that release.
- **Manual steps**: upgrade pkm to 0.3 on each machine (`brew upgrade pkm`), then `pkm version --require 0.3` confirms it.

## Released

- [0.1.0](https://github.com/Zejnilovic/agentic-pkms/releases/tag/v0.1.0) (2026-11-18)
