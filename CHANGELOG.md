# Changelog

What changed in the kit. The next version's changes are collected here; each released version's notes, including manual steps for existing vaults, are on its GitHub release, linked below. To see what an update would change in a vault, run `agd status` there.

Version numbers: **major** when something is renamed or removed and existing vaults need manual changes, **minor** for new agents, skills, templates, commands or rules, **patch** for wording and fixes. Before 1.0, a minor version may also need manual changes; its notes list them under "Manual steps". Each release is a git tag (`v0.1.0`), and the first line of a vault's `AGENTS.md` shows which version its copy came from.

## 0.3.0 (unreleased)

- **Money tied to notes** (ledger pack): a transaction names the note it belongs to with `; note: <name>` (a project, an area, an item or a person), so hledger answers what the bathroom cost: `register 'tag:note=^bathroom$'`. A new Invoices section: an invoice is a waiting task until it is paid, then the task is done and the income recorded with its note. Older `; project:` and `; item:` tags still read. pkm gets no amount marker: money stays in the journal, where hledger adds up.
- **Methodology**: the digest excerpt's names match what `pkm since last` prints on the work example.

## Released

- [0.2.0](https://github.com/Zejnilovic/agentic-pkms/releases/tag/v0.2.0) (2026-11-19)
- [0.1.0](https://github.com/Zejnilovic/agentic-pkms/releases/tag/v0.1.0) (2026-11-18)
