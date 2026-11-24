# Drills

A drill tries the kit with a real assistant on a made-up vault and grades what it did. Tests of `check.py` show the kit is consistent; a drill shows a model can follow it. Each drill is a request an owner makes, in turns, with the answers an owner would give.

| Drill | What the owner asks |
|---|---|
| `connect-repos` | Connect the project `apollo` to every `acme-example` repository whose name starts with `apollo`: one name clashes with the project, one repository already has a note, one is archived |
| `project-folders` | Set up the project `hermes`, connect its repositories, and keep `hermes.md` in `notes/` and its other notes, an existing kickoff note included, in `notes/hermes/` |
| `tidy-mess` | Tidy what another assistant left: two notes for one repository, a repository note typed `note` with a trailing `/` on its address, notes without `part_of`, and a person filed under the project |
| `finish-project` | Finish `hermes`: its kickoff note goes to the archive with it, and its repository moves to the application that outlives it |

## Running one

```bash
python3 scripts/drill.py run connect-repos --model haiku
```

It builds a vault in a temporary folder from `tests/fixtures/vault`, the drill's `vault/` files and `kit/`, puts pkm (from `SCRIPTS_PKMS`, or `../scripts-pkms`) and a fake `gh` first on `PATH`, and sends each turn to `claude -p` in that vault. The fake `gh` serves the repositories in `drill.json` and logs each call to `gh.log`. After the first turn it records what changed; after the others it stops once the grade passes. It prints each turn's tool calls and answer, the cost, and one line per check. A run with Haiku costs a few cents.

The assistant may run pkm, `gh`, `jq` and `ls`, read and edit files, and run the file commands that `acceptEdits` allows; anything else is refused. User settings and MCP servers are left out (`--setting-sources project,local`, `--strict-mcp-config`).

## Trying one by hand, as with Copilot

```bash
python3 scripts/drill.py setup project-folders /tmp/drill-hermes
```

It prints the vault, the `PATH` to set in its terminal, and the turns. Open the vault in the assistant, give it the first turn, then run `python3 scripts/drill.py mark /tmp/drill-hermes`. Give it the other turns, then run `python3 scripts/drill.py check project-folders /tmp/drill-hermes`.

## What is graded

- **Proposal first**: nothing in the vault changed after the first turn, before the owner's yes.
- **The notes**: each expected note exists once, at its path, with its type and its frontmatter values.
- **Nothing extra**: no note for what the owner left out, such as an archived repository, and one note per repository address.
- **The owner's words**: day pages and the listed notes are unchanged; a note's text below its frontmatter is unchanged.
- **Nothing from the tool**: no repository description in any note.
- **Moves through pkm**: a note that moved is in `.pkm/moves.tsv`.
- **`pkm check`** finds no problems, and none of the notices a drill names (`notices_absent`), such as two notes with one address.
- **pkm only**, a warning rather than a failure (in a `run`, from its tool calls): the vault was read with pkm, never with `ls`, `cat`, `find`, `grep` or the assistant's own file tools; the kit's files and `.pkm/` don't count.

`tests/test_drill.py` checks the grader without a model: each drill's `solution` (the pkm commands that solve it) passes, and the usual messes fail.

## Adding one

Make `tests/drills/<name>/drill.json` with `title`, `base`, `now` (pkm's clock), `gh_repos` (the fake `gh`'s organizations and repositories), `turns`, `expect` (`notes`, each with one `path` or a list of allowed ones, `absent`, `unchanged` paths, `body_unchanged` names and `notices_absent`) and `solution`, and put any extra vault files in `tests/drills/<name>/vault/`. Use made-up names only. Keep the kit's examples different from a drill's names, so a skill never hands a model the answer.
