---
name: organizing
description: Makes and arranges notes with pkm: notes with their frontmatter filled, part_of trees, project folders, moves, renames and clean-ups, as one numbered proposal. Use to set up, connect, group, move, rename or tidy notes.
---

<!-- From agentic-pkms. Kit updates replace this file except a "## This project" section at the end, which belongs to the vault. Edit nothing else. Vault rules go in AGENTS.md "This project". -->

Needs pkm; see the agreement.

# Organizing notes

pkm makes, changes and moves notes. You decide what to propose, the owner says yes, and pkm writes. Never create a note file, edit frontmatter or move a file yourself: a command that refuses is the answer, not something to work around.

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
| See the settings | `pkm config`: `folder_<type>` and `part_of_folders` |
| See the types | `pkm templates` |

## Names, types and trees

- **One note per thing.** Before proposing a note, run `pkm path <name>`. If it exists, propose `pkm set` for what is missing instead.
- **Names** are lowercase words joined by hyphens, from the title. A thing from a tool keeps its own name: the repository `project-v9-api` is the note `project-v9-api`.
- **A clash** (pkm says the name is taken): qualify the new name by its type, `--name <name>-<type>`, such as `project-v9-repo` next to the project `project-v9`. Never rename the existing note to make room.
- **The type** is the first word of `pkm new`. Use a type `pkm templates` lists. A new type of the owner's goes in AGENTS.md "This project" first.
- **part_of** names the one note a note belongs to. The owner's words decide it: "connect them to project-v9" is `part_of=project-v9`. Make the parent first; pkm refuses a `part_of` that names no note.
- **Values** come from the owner or from an address they gave. Write "unknown" nowhere in frontmatter: leave a key empty instead. A tool's own text, such as a repository's description, is not copied.

## Folders

- **Default**: notes sit in `notes/`, or in a type's `folder_<type>`. Links name the note, so a folder never matters to pkm.
- **Project folders**: when `pkm config` shows `part_of_folders=yes`, pkm puts each note in a folder named after its parent: the hub stays at `notes/project-v9.md`, and its notes go in `notes/project-v9/`. Don't pass `--folder` then; pkm places them.
- **The owner asks for that layout** and the setting is `no`: propose the line `part_of_folders=yes` for `.pkm/config`, append it after a yes, then run `pkm check`. Its notices list each note outside its parent's folder with the `pkm mv` that moves it; propose those moves as rows.
- **A folder the owner names**, such as `notes/clients/`: `--folder <folder>` on `pkm new`, `pkm mv` for existing notes.

## Steps

1. **The ask in one line**: the top note, the notes under it, the layout. Example: "project-v9, its 6 repositories, in notes/project-v9/".
2. **Look** before proposing: `pkm config`, `pkm path <top>`, `pkm list --under <top>`, and `pkm names --type <type>` for the kinds involved. Things from a tool, such as repositories, are listed with the tool, read only (the `projects` skill has the commands).
3. **Propose** one numbered table, parents first, at most 30 rows. Each row is one pkm command and the path it gives:

   ```text
   | # | Action | Note | Command | Path |
   |---|---|---|---|---|
   | 1 | new | project-v9 | pkm new project "project-v9" --set status=active | notes/project-v9.md |
   | 2 | new | project-v9-api | pkm new repo --url https://github.com/acme-example/project-v9-api --set part_of=project-v9 | notes/project-v9/project-v9-api.md |
   | 3 | set | kickoff-notes | pkm set kickoff-notes part_of=project-v9 | notes/project-v9/kickoff-notes.md |
   ```

   Below it, say what you leave out and why, such as archived repositories or notes that already exist.
4. **Wait** for the owner's yes, or for the numbers they accept.
5. **Run** the accepted rows in order, one command each. If one fails, stop: give its message, and propose a fixed row.
6. **Check**: run `pkm check`. Fix what you caused, with the commands above, after a yes. Report the other problems.
7. **Report**: each file created, changed or moved, by path, then `pkm list --under <top>`.

## Tidying a mess

When notes are scattered, doubled or of the wrong type, run `pkm check`, `pkm overview` and `pkm names --type <type>`, then propose a table as in step 3:

- A wrong type: `pkm set <note> type=<type>`. A wrong or missing parent: `pkm set <note> part_of=<name>`.
- A misplaced file: `pkm mv`. A bad name: `pkm rename`.
- Two notes for one thing: show both, and ask which stays. The owner moves or merges the text, or asks you to; the other goes to `archive/` with `pkm mv` after a yes. Never delete.

## Rules

- At most 30 rows per proposal. For more, propose the first 30 and say how many are left.
- Never edit frontmatter or move files by hand, and never write a note with a shell command.
- Every new note is linked: a `part_of`, or a line in a note or on today's page.
