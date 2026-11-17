---
name: tasks
description: The owner's tasks: markers for due dates, priority, waiting, start, someday and routines; adding, finishing and dropping them with pkm; planning the day; nothing carried over. Use to add, finish, find or plan tasks, or when asked what to do today.
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

## Commands

- `pkm todo <text> [--due <day>] [--high | --low] [--waiting | --someday | --start <day> | --every <N>d|w|m|y or cycle]`: adds a task for today. `--every` writes to the `routines` note.
- `pkm done <words | path:line> [--drop]`: marks the one open task that matches as done, or as dropped with `--drop`. A routine moves on by its interval or cycle.
- `pkm tasks [open | waiting | someday | done [YYYY-MM-DD]] [--link <name>] [--stale <days>] [--all]`: open tasks in groups: overdue, due soon, waiting, the rest.
- `pkm upcoming [<days>]`: due tasks, routines, birthdays and target dates ahead.

A day is `YYYY-MM-DD`, `today`, `tomorrow`, `+3d`, `+2w` or a weekday name.

## Add a task

1. Make it one task that starts with a verb: "Send Jane the signed offer", not "offer".
2. Turn a deadline into `--due` ("by Friday" is `--due friday`). Never invent a due date.
3. Run `pkm todo` once per task, after the owner's yes, and report each line it added.

## Finish and drop

- **Done**: `pkm done <a few words>`. If several tasks match, pkm changes nothing: add words or use `path:line`.
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
