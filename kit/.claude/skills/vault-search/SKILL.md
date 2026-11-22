---
name: vault-search
description: Finds things in a vault too big to read: summaries first, then pkm searches, then only the lines that answer, within a fixed budget. Use before answering any question from the vault or looking for notes to link.
---

<!-- From agentic-pkms. Kit updates replace this file except a "## This project" section at the end, which belongs to the vault. Edit nothing else. Vault rules go in AGENTS.md "This project". -->

Needs pkm; see the agreement.

# Searching the vault

Find first, then read the smallest part that answers. Reading more makes answers worse.

## Steps

1. **Summaries first.** Read a note's `summary:` and its `## Now` with `pkm get <name>#Now`. For the latest period, run `pkm list type=close` and read the newest close page with `pkm get`. If no close exists yet, go on to the search.
2. **Search by place, link and time.** Use the first that fits:
   - `pkm find <word> [<word>...]`: lines that hold every word, `path:line: text`.
   - `pkm backlinks <name> [--since YYYY-MM-DD]`: every line that links a note, and the lines under a `###` heading that links it.
   - `pkm names [--type <type>]` or `pkm path <name>`: which note a name means.
   - `pkm overview`: the vault's shape, each area with the notes `part_of` it, then projects and resources. Use it when you don't know which note a question is about.
   - `pkm list <field>=<value>`: notes whose frontmatter matches.
   - `pkm since <date|N|cycle> --about <name>`: what happened about a name since a date.
   - `--under <note>` on `tasks`, `since`, `list` and `backlinks`: only a project's or an area's notes (by `part_of`), and the day lines about them.
3. **Read only the lines that answer.** Use `pkm get <name> --lines a-b` with the line numbers the search gave, and a line or two around it. pkm stops at the file's end, so stay within the file.
4. **Stop at the budget.** About three searches and twenty lines per question. Then answer with what you have, say what you did not search, and ask before going further.

Search with pkm only. Never write your own shell search over the vault.

## Answer format

- One line per point, each ending in its source as `path:line`.
- If nothing matches, say `not found`, and name what you searched.
- Mark what you inferred rather than read: `(inferred)`.
- Say when you read only a summary: `(from path, source not read)`.

## Other vaults and broad searches

- Another vault is searched only with `pkm -V <name>`, or `pkm --vaults <names>`, and only where its `.pkm/config` has `cross_vault=yes` (`pkm -V <name> config` shows it).
- A question across years or the whole vault goes to the `retriever` agent, which returns the answer with its sources. Its output stays out of the conversation.
