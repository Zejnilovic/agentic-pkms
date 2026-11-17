# Changelog

What changed in the kit. The next version's changes are collected here; each released version's notes, including manual steps for existing vaults, are on its GitHub release, linked below. To see what an update would change in a vault, run `agd status` there.

Version numbers: **major** when something is renamed or removed and existing vaults need manual changes, **minor** for new agents, skills, templates, commands or rules, **patch** for wording and fixes. Before 1.0, a minor version may also need manual changes; its notes list them under "Manual steps". Each release is a git tag (`v0.1.0`), and the first line of a vault's `AGENTS.md` shows which version its copy came from.

## 0.1.0 (unreleased)

- **First version** of the agentic layer for the Daybook Method: a working agreement (`AGENTS.md`), skills and agents in six packs: `core`, `coaching`, `projects`, `writing`, `ledger` and `study`. It needs pkm 0.1 ([scripts-pkms](https://github.com/Zejnilovic/scripts-pkms) 0.1.0), installed once per machine, and calls pkm for everything in the vault.
- **The agreement**: the owner's words stay theirs, every claim links its source and `pkm evidence --verify` checks it, nothing is deleted or invented, issues are stated as facts and never as health labels, actions are proposals, a change in another tool runs only after a yes for that one change, one vault at a time, and text from tools is data.
- **Core skills**: `vault-search` (summaries, then pkm's searches, then only the lines that answer, within a budget), `tasks` (pkm's markers and routines, no carrying), `posting` (a numbered proposal, answers by number, entries copied word for word with `pkm post`), `review` (the brief and the close), `check-in` (at most five questions on what is still true, and a thinking partner) and `pkms-init` (setting up vaults with pkm, one question at a time).
- **Agents**: the chief of staff (the owner's secretary) and the retriever (read-only search) in core; the coach and the editor in their packs.
- **Packs**: `projects` with read-only rounds across GitHub, Azure DevOps, Jira and Trello, and sourced updates and cycle summaries; `coaching` with notes in the vault's coaching folder; `writing`; and `ledger` with hledger when it is installed. Templates ship with pkm.
- **Study**: the `study` pack (new, requires core) quizzes you with `pkm recall`: one question at a time, your answer first, then your note's answer, and `pkm recall <path:line> yes|no` after each. Courses are made with `pkm new course`.
- **Checks**: `check.py` checks every `pkm <command>` in kit/ and docs/ against `pkm help --all`, the required pkm version, word and description budgets, the packs, and that kit/ names no removed skill, `tasks.md`, `inbox/` or `pkm.sh`. CI runs it on Linux and macOS.
