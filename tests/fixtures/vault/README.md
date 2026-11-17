# Acceptance fixture vault

A small, made-up Daybook vault (Apollo, Acme, Jane Doe and John Roe) for the manual acceptance run of agentic-pkms (plan step 22). It is a starting state, not a test run: always copy it first and work in the copy.

What it holds:

- Ten day pages, 2026-11-03 to 2026-11-16, and one from 2026-08-18.
- `notes/apollo.md`, a project with Now, Decisions and Links; `notes/jane-doe.md` and `notes/john-roe.md`, people.
- A waiting task: "waiting for [[john-roe]] on the budget" (2026-11-09).
- An old decision, 2026-08-18 ("Decided: Apollo's backend stays on Postgres ...").
- A fresh decision, 2026-11-16 ("Decided: we ship Apollo in two phases ..."), not yet posted to Apollo.

Run pkm with `PKM_NOW=20261116090000` to make 2026-11-16 today. This folder has no cache; `pkm` builds one in `.pkm/cache`, which `.pkm/.gitignore` leaves out of git.
