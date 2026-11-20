---
name: review
description: Brings the owner a brief of what is new, important and needing attention, from pkm's digest, and runs the close with its do, date, answer and chase choices. Use only when the owner asks for the brief or the close.
---

<!-- From agentic-pkms. Kit updates replace this file except a "## This project" section at the end, which belongs to the vault. Edit nothing else. Vault rules go in AGENTS.md "This project". -->

Needs pkm; see the agreement.

# Brief and close

Run this only when the owner asks, never on a schedule of its own. You report; the owner decides. Facts only: never a health label, a score or praise. Every line ends with its source.

## The brief

1. Run `pkm since last` and `pkm upcoming 7`. If `since last` prints "Nothing since", say so, give only the Today list, and stop.
2. Read only that output, and for each of today's events that links a note, its open lines with `pkm get "<name>#Next time"`. If something you need is missing, say so instead of searching.
3. Write four lists, at most 5 lines each, in this format. Leave out Today when nothing happens today:

   **Today**
   - 17:30 parents' evening at the school (daybook/2026/11/2026-11-14-alex.md:9)

   **New**
   - Acme has a new contact, Marta Kovac, who has no note yet (daybook/2026/11/2026-11-10.md:11)

   **Important**
   - You marked it: Acme may cancel the contract if the demo slips again (daybook/2026/11/2026-11-10.md:9)

   **Needs attention**
   - Overdue since Friday: send John Roe the Apollo invoice (daybook/2026/11/2026-11-09.md:5)

   Today: the `event` lines dated today in `pkm upcoming 7`, in its order, each with its time as written, and under it, at most three open lines of the linked note's Next time, each with its source. Events can't be overdue, so a past one is never raised. New: entries and names that appeared since the last brief. Important: lines the owner marked with `!` or as `Decided:`. Needs attention: overdue or waiting tasks, open questions, and the dates and events of the coming days in `pkm upcoming 7`. Each line states what is there and why it may matter.

4. Run `pkm evidence --verify -` on the draft. Drop every line without a source, or that the check rejects.
5. Propose tasks for what needs doing, each quoting its line. Propose posts for marked entries not yet posted (`Decided:` and `!`), and hand them to the `posting` skill: "Shall I post …?". Add nothing without a yes.
6. Print the brief. Run `pkm since --seen` only after the owner has seen it and said so.

**Across vaults**, only when the owner asks: run `pkm -V <name> config` for each vault `pkm vaults` lists, and keep the ones with `cross_vault=yes`. Then run `pkm --vaults <this vault>,<those> upcoming 7` and give a Today and a Needs attention list per vault, each line with its vault's path. Copy nothing between them.

## The close

Run this when the owner asks for a close. It follows the vault's close cycle; `pkm close --cycle <name>` picks another.

1. Run `pkm close` and read its sections.
2. **Tasks**: for each task in `== tasks` (overdue, or open 21 days or more), ask the owner: do, date, someday or drop.
3. **Open items**: for each question and waiting task in `== open`, ask: answer, chase or drop.
4. **Someone's move**: `== for` lists, by person, the tasks and questions with a `(for …)`. Give each person once, with their lines, and for each line ask: chase, date or drop. A chase is a draft for the owner to send.
5. **Coming due**: list the routines, dated tasks, events, birthdays and target dates in `== due`, one line each with its source. An event comes with its day and time; it needs no answer. An event that comes back is listed on each of its days: give it once, with its days.
6. **Posts**: list the marked entries in `== marked` as proposals, and hand them to the `posting` skill. Post nothing unapproved.
7. **Quiet and names**: show `== quiet` (projects and people mentioned in the four weeks before the last two, and not since) and `== names` (names with no note), for the owner to decide.
8. **Shared vault**: name each line's writer from its day page's name: `2026-11-12-sam.md` is sam's.
9. **Quarter**: when `== ideas` appears, go through each idea and someday item: start, keep or drop.
10. **Close page**: if the owner says yes, run `pkm new close`, write 3 to 5 lines, each with a source such as `[[2026-11-12]]`, then run `pkm evidence --verify`.

Every action waits for the owner's yes, one answer per item.

## Rules

- Propose changes; make none without a yes.
- Name what the owner said only in their own words, quoted and linked.
- No advice unless asked. If something is not in the notes, say "unknown".
- Health and other private matters about someone appear only as written, with their source, never inferred, and never in a draft for someone else unless the owner asks.
