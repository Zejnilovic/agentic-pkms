---
name: tasks
description: The owner's tasks: due dates, priority, waiting, routines and whose move it is; adding, finishing, moving and dropping them with pkm; planning the day. Use to add, finish, find or plan tasks, or for what to do today.
---

<!-- From agentic-pkms. Kit updates replace this file except a "## This project" section at the end, which belongs to the vault. Edit nothing else. Vault rules go in AGENTS.md "This project". -->

Needs pkm; see the agreement.

# Tasks

A task is a `- [ ]` line outside code. It stays on the page where it was written; nothing carries over.

## Markers

Put markers at the end of the task line, in parentheses.

| Marker | Means |
|---|---|
| `(due 2026-11-20)` | The deadline. On a day page, a relative date such as `(due friday)` or `(due +3d)` resolves against that page's day |
| `(high)`, `(low)` | Priority; no marker is normal |
| `(waiting 2026-11-10)` | Someone else must act; the owner follows up. The date is when the wait began |
| `(start 2026-11-15)` | Hidden until that day |
| `(someday)` | Not committed to; shown only by `pkm tasks someday` |
| `(every 1m)` or `(every <cycle>)` | A routine. It lives in the `routines` note and moves on when done |
| `(at 2026-11-20 14:00-15:00)` or `(@ …)` | A time. On a task, it is due that day unless it has a `(due …)` |
| `(for [[jane-doe]])` or `(for sam)` | Whose move it is: they do the task, or decide the question. A link, or the name of a writer of a shared vault. A writer's tasks without one are theirs |

What needs doing every day, such as a parent's pills, is never `(every 1d)`: each missed day would be overdue at every close. Propose a list note (`type: list`) with its boxes, ticked as the day goes and unticked for the next; those boxes are not tasks.

## Events

An event is a line without a box that ends with `(at <when>)` or `(@ <when>)`: `- Parents' evening (at 2026-11-19 17:30-19:00)`. `<when>` is a date, a date and `HH:MM`, a date and `HH:MM-HH:MM`, or `<date> to <date>`; on a day page the date may be relative. An event is never a task and never overdue; `pkm upcoming` lists it on its days. Write one only for what no calendar holds already, and give it a box only when there is something to do.

- **Comes back**: in a note, add `(every 1w)` and, when needed, `(until <date>)` and `(skip <date>)`.
- **Changes**: never edit the time. Propose `pkm moved <path:line> <when>`, which strikes it and writes it again with the new time, and run it after a yes. For one time of an event that comes back, add `(skip <date>)` and write that time as an event of its own.
- **Stays put**: `pkm post` refuses an event, as it refuses an open task.

## Commands

- `pkm todo <text> [--due <day>] [--high | --low] [--waiting | --someday | --start <day> | --every <N>d|w|m|y or cycle]`: adds a task for today. `--every` writes to the `routines` note.
- `pkm done <words | path:line> [--drop | --next <day>]`: marks the one open task that matches as done, or as dropped with `--drop`. A routine moves on by its interval or cycle; done early or late, `--next <day>` sets its next due date.
- `pkm moved <path:line> <when>`: a task or an event whose date changed: strikes it and writes it again with the new date, linking the day it came from.
- `pkm tasks [open | waiting | someday | done [YYYY-MM-DD]] [--link <name>] [--for <who>] [--under <note>] [--stale <days>] [--all]`: open tasks in groups: overdue, due soon, waiting, the rest. `--for` lists someone's tasks and questions; `--under` those of a project or area and every note in it.
- `pkm upcoming [<days>]`: due tasks, routines, events, birthdays and target dates ahead. `pkm upcoming --ics > daybook.ics` writes the events, tasks with a time and birthdays as a calendar file, only when the owner asks for one.

A day is `YYYY-MM-DD`, `today`, `tomorrow`, `+3d`, `+2w` or a weekday name.

## Add a task

1. Make it one task that starts with a verb: "Send Jane the signed offer", not "offer".
2. Turn a deadline into `--due` ("by Friday" is `--due friday`). Never invent a due date.
3. Run `pkm todo` once per task, after the owner's yes, and report each line it added.

## Finish, move and drop

- **Done**: `pkm done <a few words>`. If several tasks match, pkm changes nothing: add words or use `path:line`.
- **Moved**: a deadline that changed is `pkm moved <path:line> <new day>`, never an edit of the date, so the old date stays on record.
- **Dropped**: `pkm done <words> --drop`, only when the owner said so.

## Plan the day

1. Run `pkm tasks` and `pkm upcoming 7`.
2. Propose at most 7 lines, each ending in `path:line`: overdue first, then due soon, then waiting tasks to chase.
3. Write nothing without the owner's yes.

## Promises and the close

- A promise in an entry, such as "I'll send the draft", becomes a task on today's page, quoting the entry, only after a yes.
- A task open for three weeks or more is raised at the close (`pkm close`): the owner chooses do, date, someday or drop.

## Rules

- Only the owner's tasks. Never mark one done or dropped unless the owner said so.
- A `(for …)` records whose move it is. It never sends anything: chasing someone is a draft the owner sends.
