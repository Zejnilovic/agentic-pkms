# Changelog

What changed in the kit. The next version's changes are collected here; each released version's notes, including manual steps for existing vaults, are on its GitHub release, linked below. To see what an update would change in a vault, run `agd status` there.

Version numbers: **major** when something is renamed or removed and existing vaults need manual changes, **minor** for new agents, skills, templates, commands or rules, **patch** for wording and fixes. Before 1.0, a minor version may also need manual changes; its notes list them under "Manual steps". Each release is a git tag (`v0.1.0`), and the first line of a vault's `AGENTS.md` shows which version its copy came from.

## 0.5.0 (unreleased)

- The kit needs pkm 0.9 ([v0.9.0](https://github.com/Zejnilovic/scripts-pkms/releases/tag/v0.9.0)): `pkm version --require 0.9`. Update pkm first, for example with `brew upgrade pkm`.
- The projects skill covers applications (`pkm new app`), repositories (`pkm new repo`) and teams (`pkm new team`) as well as projects. An application's projects and repositories are `part_of` it, and its IDs in other systems are its aliases.
- Items: the projects skill writes an item from a tool as `[[apollo-web]]#42`, its note's link and number, when the note has an `items` line, and `pkm url` prints its address.
- Rounds cover the applications and repositories too.
- What's new: "what's new on apollo-web since last week?" gives at most 15 lines from the vault and the tools, each with its source, and proposes tasks: what waits on you, and someday tasks starting "Catch up on" for what you only need to read.
- "This project" names keys of your own, such as an ID that several notes carry, under "Own types and conventions", and `pkms-init` writes them there when you name them. Manual step: in an existing vault, add your own keys there by hand, since kit updates never change "This project".

## Released

- [0.4.2](https://github.com/Zejnilovic/agentic-pkms/releases/tag/v0.4.2) (2026-11-22)
- [0.4.1](https://github.com/Zejnilovic/agentic-pkms/releases/tag/v0.4.1) (2026-11-20)
- [0.4.0](https://github.com/Zejnilovic/agentic-pkms/releases/tag/v0.4.0) (2026-11-20)
- [0.3.0](https://github.com/Zejnilovic/agentic-pkms/releases/tag/v0.3.0) (2026-11-20)
- [0.2.0](https://github.com/Zejnilovic/agentic-pkms/releases/tag/v0.2.0) (2026-11-19)
- [0.1.0](https://github.com/Zejnilovic/agentic-pkms/releases/tag/v0.1.0) (2026-11-18)
