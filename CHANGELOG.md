# Changelog

What changed in the kit. The next version's changes are collected here; each released version's notes, including manual steps for existing vaults, are on its GitHub release, linked below. To see what an update would change in a vault, run `agd status` there.

Version numbers: **major** when something is renamed or removed and existing vaults need manual changes, **minor** for new agents, skills, templates, commands or rules, **patch** for wording and fixes. Before 1.0, a minor version may also need manual changes; its notes list them under "Manual steps". Each release is a git tag (`v0.1.0`), and the first line of a vault's `AGENTS.md` shows which version its copy came from.

## 0.4.0 (unreleased)

- **Next time** (pkm 0.7.0): what to raise at the next meeting waits under `## Next time` in a person's, project's or area's note. Posting files it there, and proposes a strike once it was raised. The coaching skill puts its open lines first on a 1:1 agenda, and the brief shows them under each of today's events whose note they're in. A new person note has `## Next time` and `## Notes`; for an older one, posting proposes adding both first.
- **Other people's private matters**: health and the like are posted only as the owner wrote them, with who said it, never inferred, and never in a draft for someone else unless asked. The agreement asks about privacy when the first health note appears, as for coaching and money.
- **pkm 0.7**: the kit needs pkm 0.7 ([scripts-pkms](https://github.com/Zejnilovic/scripts-pkms) 0.7.0); its checks run against that release. Release pkm 0.7.0 first.
- **Manual steps**: upgrade pkm to 0.7 on each machine (`brew upgrade pkm`), then `pkm version --require 0.7` confirms it.

## Released

- [0.3.0](https://github.com/Zejnilovic/agentic-pkms/releases/tag/v0.3.0) (2026-11-20)
- [0.2.0](https://github.com/Zejnilovic/agentic-pkms/releases/tag/v0.2.0) (2026-11-19)
- [0.1.0](https://github.com/Zejnilovic/agentic-pkms/releases/tag/v0.1.0) (2026-11-18)
