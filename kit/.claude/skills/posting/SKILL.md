---
name: posting
description: Files the owner's entries into notes with pkm: a numbered list, answers by number, each entry copied word for word with its day, then summaries and checks. Use to file a day's entries.
---

<!-- From agentic-pkms. Kit updates replace this file except a "## This project" section at the end, which belongs to the vault. Edit nothing else. Vault rules go in AGENTS.md "This project". -->

Needs pkm; see the agreement.

# Posting

You propose; the owner answers by number; pkm copies. Entries reach notes only through pkm, so the owner's words cannot change on the way.

## Steps

1. **Read the entries.** Use `pkm since <date>` for a range, or `pkm get <page>` for one day page.
2. **Propose a numbered list**, one line per entry, in this format:
   - `1. Line 9, "! They may cancel the contract if the demo slips again": Risks in [[apollo]]`
   - `2. Line 11, "Their new contact is Marta Kovac": a new note, marta-kovac, because a new contact at a customer is worth keeping`
   - `3. Line 12, "I'll send them the revised timeline by Thursday": nothing, you sent it on Thursday`
   - `4. Now of [[marta-kovac]]: Marta Kovac is Acme's project lead ([[2026-11-16]])`

   Quote each entry as the owner wrote it. Give a reason for every "nothing". Put questions last, one per line, as `Question for 2: who is Marta Kovac at Acme?`. Propose at most 10 entries at a time.
3. **Stop and wait** for the owner's answers by number. Post nothing for a number that is not answered.
4. **Log the answers that add a fact** on today's page with `pkm add`, in the owner's words, with links added and nothing else changed: `pkm add "[[marta-kovac|Marta Kovac]] is [[acme|Acme]]'s project lead"`. Never log a bare answer such as "1 yes".
5. **File each entry.** Create each new note with `pkm new <type> "<title>"`, then post each entry once: `pkm post <path:line> <note>#<Section>`. pkm refuses an open task, an event or a heading as the source, a day page or a close page as the target, and a repeat (exit 1, with the existing `path:line`). A refusal is an answer, not a failure to work around.
6. **Update `## Now`** when a numbered proposal says so. It is its own line in the list. After a yes, edit the Now section directly, in your own words, with a source on every line such as `([[2026-11-10]])`. Then run `pkm evidence --verify <note>`.
7. **Run `pkm check`.** Fix what you caused; report the rest.
8. **Report** each change, note by note: the lines posted, the new notes, the `## Now` lines changed.

## Person facts

- Facts only: role, how to reach them, what helps the relationship. Feelings and doubts stay on the day page, and are not carried into the person's note.
- No secrets, such as passwords, keys or card numbers.
- A birthday goes in the frontmatter as `birthday: 1985-03-14`; `pkm upcoming` lists it.
- Health and other private matters about someone: only what the owner needs to act on, word for word, with who said it. Never infer one. When the vault has no folder off limits for them, ask the owner where they belong before posting.
- A post to a person without a section lands at the note's end. A new person note ends with `## Next time` and `## Notes`, so it lands in Notes. For an older note without them, propose adding both before its first Next time post.

## Source notes

A book, article or talk gets `type: source` in its frontmatter, with a link to where it came from. Summaries of it link its page or line.

## Hubs

After about 10 notes on one topic, propose a hub note that links them. Create it only after a yes.

## New notes

A name mentioned three times, or a new contact who matters, gets a note. Propose it as "a new note, <name>, because ...". `pkm close` lists names linked three times or more with no note under `== names`.

## Renames

Rename with `pkm rename <old> <new>`. It rewrites every link and keeps the old name as an alias; `--dry-run` shows the changes first. When two notes would share a name, add a qualifier: `<name>-<word>`. Run it only after a yes.

## Next time

What the owner wants to raise at the next meeting is posted to `<note>#Next time`, in a person's, project's or area's note: `pkm post <path:line> "<note>#Next time"`. Once it was raised, propose `pkm strike <path:line>` for its line.

## Strikes

After a yes, `pkm strike <path:line>` strikes a line that is no longer true, and links today's page. Never delete the line.

## What you may change without asking

Only links: put `[[ ]]` around a name in the owner's text, such as `[[apollo]]`. Any other change to the owner's text waits for a yes.
