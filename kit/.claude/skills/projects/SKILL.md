---
name: projects
description: Project, application, repository and team notes: setting up a project, connecting its repositories from GitHub or Azure DevOps, a project's tasks, and the portfolio. Use to set up or connect a project, app, repo or team, to make a repo note, or for the active projects.
---

<!-- From agentic-pkms. Kit updates replace this file except a "## This project" section at the end, which belongs to the vault. Edit nothing else. Vault rules go in AGENTS.md "This project". -->

Needs pkm; see the agreement. Proposals, folders and clean-ups follow the `organizing` skill; the rounds and "what's new" are the `rounds` skill.

# Projects

The owner's notes hold their overview: what a thing is, its Now, decisions and links. The work lives in its tools. The notes link them and never copy their items. Facts only: no health, status colours or scores.

## The notes

Make each with `pkm new <type> "<name>" --set key=value ...`, after a yes. Change one with `pkm set <note> key=value`. Never edit the frontmatter by hand.

- **Project** (`project`): anything with an end. `status` (`idea`, `active`, `paused`, `done` or `dropped`), `target`, `summary`, `part_of` (its application or area). Sections: **Now**, five to ten lines on the current milestone, the next decision, what it waits for and the owner's next actions; **Next time**, what to raise at its next meeting, struck once raised; **Goals**, with dates; **People**, who does what; **Risks** and **Decisions**, entries posted from their day with `pkm post` (the posting skill); **Later**, ideas; **Links**, one line per address where the work lives, such as `- Board: https://dev.azure.com/acme-example/apollo/_boards`.
- **Application** (`app`): software the owner builds or runs, which outlasts its projects. Now, Links (where it runs, who owns it, its runbook), Decisions, Notes. Its projects and repositories are `part_of` it. Its IDs in other systems go in `aliases`, so `[[APP-1001]]` links it.
- **Repository** (`repo`): made from its address, `pkm new repo --url <address> --set part_of=<name>`, which fills `url`, `items` and the title for GitHub, Azure DevOps and GitLab. `part_of` is the note the owner named; without one, its application, or its project when there is no application note. Now, Decisions, Notes.
- **Team** (`team`): People, Links (its team on GitHub or Azure DevOps, its board, its wiki), Next time.

Keys of the vault's own, such as an ID that several notes carry, are named in AGENTS.md "This project". Set them with `--set` as written there; `pkm list <key>=<value>` finds the notes with a value.

## Items

`[[apollo-web]]#42` is item 42 of that note: its `items` value with the number added. `pkm url "[[apollo-web]]#42"` prints the address; pkm never goes online. Write an item from a tool this way when its note has an `items` line, and as its full address otherwise. `pkm check` reports an item whose note has no `items` line.

## Set up a project

For "set up project-v9":

1. Run `pkm path project-v9`. If the note exists, show its frontmatter with `pkm get project-v9 --lines 1-12` and propose only `pkm set` rows for what is missing.
2. Ask at most three questions, each with an example, and accept "skip": its status (`active`), its target date, and the application or area it is `part_of`, if any. The summary is the owner's words, or left empty.
3. Propose the row: `pkm new project "project-v9" --set status=active --set target=2027-03-31`. A parent must exist first: propose it as an earlier row.
4. After a yes, run it, then offer to connect its repositories and its board (below).

## Connect repositories

For "connect project-v9 to every repository that starts with project-v9":

1. **What to match**, from the owner's words: the owner or organization, and a prefix, a topic or a list of names. If the organization is missing, ask for it, with an example (`acme-example`).
2. **List them**, read only:
   - GitHub: `gh repo list <owner> --limit 1000 --json name,url,isArchived --jq '.[] | select(.name | startswith("<prefix>")) | [.name, .url, .isArchived] | @tsv'`
   - Azure DevOps: `az repos list --organization https://dev.azure.com/<org> --project <project> --query "[?starts_with(name, '<prefix>')].[name, webUrl]" -o tsv`
   - If the tool is missing or not signed in, say which, give the command, and ask the owner for the list of addresses instead.
3. **Already there**: run `pkm list type=repo --show url,part_of`. A repository whose `url` is listed has a note: propose `pkm set <note> part_of=<project>` for it instead of a new note.
4. **Propose** the `organizing` table, one row per repository: `pkm new repo --url <url> --set part_of=<project>`. A repository named like its project, or like another note, gets `--name <repo>-repo`. List archived repositories below the table, not as rows, unless the owner asks for them.
5. **After a yes**, run the rows, then `pkm check` and `pkm list --under <project>`. Report each path.

Copy nothing else from the tool: no descriptions, topics or READMEs. The note's **Now** is written later, from the owner's entries.

## A board or a team

- A project's board: propose a **Links** line with its address, and `pkm set <project> items=<address of an item without its number>` when its items are numbered, such as `https://acme.atlassian.net/browse/APOLLO-`.
- A team: `pkm new team "<name>" --set url=<its team page>`, and its people as `[[name]]` links under **People**, after a yes.

## Tasks of a note

Run `pkm tasks --under <name>`: the tasks of the note, of every note under it by `part_of`, and of the day lines about one of them. For an application, that includes its projects and repositories. `pkm tasks someday --under <name>` lists its catch-up tasks.

## Portfolio

Run `pkm list type=project status=active`. Give one line per project: its name, the first line of its Now, and its `path:line`, ordered by target date. `pkm overview` shows each application with its projects and repositories under it.

## Rules

- Nothing from a tool is copied into the vault. An accepted task names the item and links it.
- One proposal at a time, at most 30 rows, as the `organizing` skill sets out.
- A status report is the `rounds` skill's.
