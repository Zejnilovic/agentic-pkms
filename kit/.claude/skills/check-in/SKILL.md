---
name: check-in
description: Asks the owner at most five short questions about whether their notes are still true, proposes entries and strikes for the answers, and talks a decision through without deciding it. Use when asked to check in or to think something through.
---

<!-- From agentic-pkms. Kit updates replace this file except a "## This project" section at the end, which belongs to the vault. Edit nothing else. Vault rules go in AGENTS.md "This project". -->

Needs pkm; see the agreement.

# Check-in

A check-in is the agent asking rather than telling. Run it only when the owner asks. Facts only: never a health label, a score or praise. Write nothing without a yes.

## Steps

1. **Read, with pkm only.**
   - `pkm list type=project status=active` for the active projects.
   - Each project's `## Now`, with `pkm get <name>#Now`.
   - `pkm tasks waiting` for open waits.
   - `pkm upcoming 14` for dates and events in the next two weeks.
2. **Ask at most five questions, one at a time, most useful first.** Each quotes its source line and asks whether it is still true, for example: "Is the demo still on 2026-11-20? (notes/apollo.md:13)". Accept a one-word answer.
3. **For each answer, propose the exact change and wait for a yes.** Use one of:
   - an entry on today's page, `pkm add "<text>"`, in the owner's words;
   - a strike for what is no longer true, `pkm strike <path:line>`;
   - a task, `pkm todo "<text>"`, with its marker.
4. **Stop when the owner says stop.** Ask nothing further after that.
5. **Report what changed**: each entry, strike or task, with its `path:line`. Name what you left alone.

## Thinking partner

When the owner wants to think a decision through:

1. Ask before you answer: what they are choosing between, what they need to be true, and what they are afraid of losing.
2. Offer the facts the vault holds about it, each with its source. Mark what is not in the vault as unknown.
3. Never decide for them. Give the options they name, and say what each one depends on.
4. End with a proposed line in their words, `Decided: <their choice, in their words>`. Add it with `pkm add` only after a yes, and change it when they ask.

## Rules

- Questions are at most five per check-in, each with its source.
- No advice unless asked, and no health labels or scores.
- Keep the owner's wording in every entry, and link names without changing them.
