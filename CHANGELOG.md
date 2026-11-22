# Changelog

What changed in the kit. The next version's changes are collected here; each released version's notes, including manual steps for existing vaults, are on its GitHub release, linked below. To see what an update would change in a vault, run `agd status` there.

Version numbers: **major** when something is renamed or removed and existing vaults need manual changes, **minor** for new agents, skills, templates, commands or rules, **patch** for wording and fixes. Before 1.0, a minor version may also need manual changes; its notes list them under "Manual steps". Each release is a git tag (`v0.1.0`), and the first line of a vault's `AGENTS.md` shows which version its copy came from.

## 0.4.2 (unreleased)

- Requires [pkm 0.8.0](https://github.com/Zejnilovic/scripts-pkms/releases/tag/v0.8.0): a `###` block now ends at a blank line followed by an entry, so `backlinks`, `since --about` and `--under` no longer count the entries after a block as about its heading.
- The tasks skill: what needs doing every day, such as pills, is a list note with boxes, never a routine with `(every 1d)`, as pkm 0.8.0's method says.
- The agreement and the methodology name `pkm mv` for moving a finished note to `archive/`, so the move keeps its name and links.
- vault-search and the methodology name `pkm overview`, the tree of areas, projects and resources by `part_of`, for a question whose note is unknown.
- Repo: the tests of `check.py` follow the agreement's `pkm version --require` line, and CI and the release workflow run them.
- **Manual steps**: upgrade pkm to 0.8 on each machine (`brew upgrade pkm`), then `pkm version --require 0.8` confirms it. Pages written before keep an entry glued to the end of a block in it; add a blank line before the entry to take it out.

## Released

- [0.4.1](https://github.com/Zejnilovic/agentic-pkms/releases/tag/v0.4.1) (2026-11-20)
- [0.4.0](https://github.com/Zejnilovic/agentic-pkms/releases/tag/v0.4.0) (2026-11-20)
- [0.3.0](https://github.com/Zejnilovic/agentic-pkms/releases/tag/v0.3.0) (2026-11-20)
- [0.2.0](https://github.com/Zejnilovic/agentic-pkms/releases/tag/v0.2.0) (2026-11-19)
- [0.1.0](https://github.com/Zejnilovic/agentic-pkms/releases/tag/v0.1.0) (2026-11-18)
