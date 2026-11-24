---
name: organizing
description: Makes and arranges notes with pkm: notes with their frontmatter filled, part_of trees, project folders, moves, renames and clean-ups, as one numbered proposal. Use to set up, connect, group, move, rename or tidy notes.
---

<!-- From agentic-pkms. Kit updates replace this file except a "## This project" section at the end, which belongs to the vault. Edit nothing else. Vault rules go in AGENTS.md "This project". -->

Needs pkm; see the agreement.

# Organizing notes

pkm makes, changes and moves notes. You decide what to propose, the owner says yes, and pkm writes. Never create a note file, edit frontmatter, or make or move a folder or file yourself (`mkdir`, `mv`): pkm makes the folders it needs, and a command that refuses is the answer, not something to work around.

**Look with pkm only.** Never `ls`, `cat` or `find` in the vault: they read whole notes, and folders the owner may have put off limits. pkm gives the names, paths and lines you need.

**A request is not a yes.** "Set up orion", "connect it" or "move them" asks for the proposal. Show the table and stop. Nothing is written until the owner answers the table.

## The commands

| To | Run |
|---|---|
| Make a note | `pkm new <type> "<title>" --set key=value ...` |
| Make a repository's note | `pkm new repo --url <address> --set part_of=<name>` (fills `url`, `items` and the title) |
| Change frontmatter | `pkm set <note> key=value ...`, such as `status=done`, `part_of=apollo`, `summary=...`; `key=` clears one |
| Move notes into a folder | `pkm mv <note> ... <folder>` |
| Rename a note and its links | `pkm rename <old> <new>` (`--dry-run` first) |
| Finish a note | `pkm mv <note> archive` |
| See what exists | `pkm names --type <type>`, `pkm path <name>`, `pkm list --under <name>`, `pkm overview` |
| Read a note's frontmatter | `pkm get <name> --lines 1-12` |
| See the settings | `pkm config`: `folder_<type>` and `part_of_folders` |
| Change a setting | `pkm config <key> <value>`, such as `pkm config part_of_folders yes` |
| See the types | `pkm templates` |

## Names, types and trees

- **One note per thing.** Before proposing a note, run `pkm path <name>`. If it exists, propose `pkm set` for what is missing instead.
- **Names** are lowercase words joined by hyphens, from the title. A thing from a tool keeps its own name: the repository `orion-api` is the note `orion-api`.
- **A clash** (pkm says the name is taken): qualify the new name by its type, `--name <name>-<type>`, such as `orion-repo` next to the project `orion`. Never rename the existing note to make room.
- **The type** is the first word of `pkm new`. Use a type `pkm templates` lists. A new type of the owner's goes in AGENTS.md "This project" first.
- **part_of** names the one note a note belongs to. The owner's words decide it: "connect them to orion" is `part_of=orion`. Make the parent first; pkm refuses a `part_of` that names no note.
- **Values** come from the owner or from an address they gave. Write "unknown" nowhere in frontmatter: leave a key empty instead. A tool's own text, such as a repository's description, is not copied.

## Folders

- **Default**: notes sit in `notes/`, or in a type's `folder_<type>`. Links name the note, so a folder never matters to pkm.
- **Project folders**: when `pkm config` shows `part_of_folders=yes`, pkm puts each note in a folder named after its parent: the hub stays at `notes/orion.md`, and its notes go in `notes/orion/`. Don't pass `--folder` then; pkm places them.
- **The owner asks for that layout** and the setting is `no`: row 1 is `pkm config part_of_folders yes`. Then `pkm set <note> part_of=<project>` moves a note into the folder, and `pkm check` lists each note still outside its parent's folder with the `pkm mv` that moves it; propose those as rows.
- **A folder the owner names**, such as `notes/clients/`: `--folder <folder>` on `pkm new`, `pkm mv` for existing notes.
- **A note that goes in a project's folder is part of the project**: give it `part_of=<project>` as well. A folder alone links nothing, so `pkm list --under` and `pkm overview` would miss it.

## Steps

1. **The ask in one line**: the top note, the notes under it, the layout. Example: "orion, its 6 repositories, in notes/orion/".
2. **Look** before proposing: `pkm config`, `pkm path <top>`, `pkm list --under <top>`, and `pkm names --type <type>` for the kinds involved. Things from a tool, such as repositories, are listed with the tool, read only (the `projects` skill has the commands).
3. **Propose** one numbered table, parents first, at most 30 rows. Each row is one pkm command and the path it gives:

   ```text
   | # | Action | Note | Command | Path |
   |---|---|---|---|---|
   | 1 | new | orion | pkm new project "orion" --set status=active | notes/orion.md |
   | 2 | new | orion-api | pkm new repo --url https://github.com/acme-example/orion-api --set part_of=orion | notes/orion/orion-api.md |
   | 3 | set | kickoff-notes | pkm set kickoff-notes part_of=orion | notes/orion/kickoff-notes.md |
   ```

   Below it, say what you leave out and why, such as archived repositories or notes that already exist.
4. **Stop and wait** for the owner's yes, or for the numbers they accept. Run nothing that writes before it, however the request was worded. A yes covers only the rows it answers: anything you mentioned outside the table, or after it, needs a row and a yes of its own.
5. **Run** the accepted rows in order, one command each. If one fails, stop: give its message, and propose a fixed row.
6. **Check**: run `pkm check`. Fix what you caused, with the commands above, after a yes. Report the other problems.
7. **Report** from pkm's output, never from what you expected: each path pkm printed, then the lines `pkm list --under <top>` prints. A note you meant to include and pkm doesn't list is not done: say so.

## What belongs under a note

For "move the rest of orion's notes" or "everything about orion":

1. **Find candidates** with pkm: `pkm names` for names that start with the project's name, `pkm backlinks orion` for the notes that link it, and `pkm list --under orion` for what is already there.
2. **Belongs**: notes about the project only, such as its repositories, a kickoff, a design, its meetings.
3. **Never under a project**: people, teams, applications and areas. They belong to many things; link them from the project's **People** or **Links** instead. A note about two projects belongs to its main one and links the other.
4. **Propose** the candidates as rows and let the owner strike the ones that don't belong.

## Moving and finishing a project

- **Under an application or area**: `pkm set <project> part_of=<name>`. With `part_of_folders=yes`, pkm moves the project's folder along with it.
- **Finishing**: run `pkm list --under <project>`, then propose, notes first and the project last:
  1. `pkm set <project> status=done` (or `dropped`, as the owner says).
  2. For each note under it, ask whether it ends with the project or lives on. Ends: `pkm mv <note> archive`. Lives on, as a repository often does: `pkm set <note> part_of=<application or area>`.
  3. `pkm mv <project> archive`.
  
  Then `pkm check` shows no note whose `part_of` is in the archive.

## Tidying a mess

When notes are scattered, doubled or of the wrong type, go through these steps in order. Each finding is a row of one table, as in step 3 above:

1. **`pkm check`**: each problem and each notice is a row, with the fix it names.
2. **`pkm list --under <top> --show type,url,part_of`**: a person, team, application or area in that list gets `pkm set <note> part_of=` (it belongs to many things; link it from the project instead). A note whose parent is archived: archive it too, or give it another parent.
3. **Each note for a repository** (one with a `url`, or named after a repository): `pkm set <note> type=repo url=<address> items=<address>/issues/`, the address without a trailing `/` or `.git`, and `part_of=<top>`. A key of the wrong name, such as `repo:`, is cleared with `pkm set <note> repo=`.
4. **Two notes for one thing**, such as two with one `url`: show both, with what each holds below its frontmatter, and ask which stays. The one that stays gets every value the other had right, as `pkm set` rows (type, `url`, `items`, `part_of`). The owner moves or merges the text, or asks you to; the other goes to `archive/` with `pkm mv` after a yes, where its links still reach it. Never delete.
5. **Notes that belong but have no `part_of`**: find them as in "What belongs under a note".
6. **Places**: a misplaced file, `pkm mv`; a bad name, `pkm rename`.

A tidy-up changes frontmatter and places only. Posts, strikes and stale lines are other work: name them in one line below the table, as rows for another time, and don't number them.

When the owner answers, redo the rows their answer changes (such as which note stays) before you run them, and show the changed rows in your report.

## Rules

- At most 30 rows per proposal. For more, propose the first 30 and say how many are left.
- Never edit frontmatter, settings or files by hand, and never write a note with a shell command.
- A line that is no longer true is struck with `pkm strike <path:line>`, after a yes, never by editing it. Tidying changes frontmatter and places, not the owner's lines.
- Every new note is linked: a `part_of`, or a line in a note or on today's page.
