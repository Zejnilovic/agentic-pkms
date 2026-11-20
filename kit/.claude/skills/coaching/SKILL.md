---
name: coaching
description: Coaching notes for the people the owner manages or mentors: goals, agreed actions, 1:1 prep and records, feedback drafts and review evidence. Facts only, drafts only. Use for a 1:1, feedback, goals, a review period or a check on the team.
---

<!-- From agentic-pkms. Kit updates replace this file except a "## This project" section at the end, which belongs to the vault. Edit nothing else. Vault rules go in AGENTS.md "This project". -->

Needs pkm; see the agreement.

# Coaching

A coaching note is the owner's working file for one person they manage, mentor or coach. It holds what that person is working toward, what the two of them agreed, and the evidence for fair feedback and reviews. Contact details stay in the person's own note. This skill edits notes directly: it writes its own sections in the coaching note (1:1s, Feedback, Actions, Goals, Now), after a yes. Day-page entries still reach notes only through `pkm post`.

## The note

Create it with `pkm new coaching "<name>"`. It is made in the folder that `folder_coaching` names in `.pkm/config`, such as `team/` in the work example. Its frontmatter: `relation` (`report`, `mentee` or `coachee`), `role`, `since`, `cadence` (`weekly`, `biweekly` or `monthly`), `status` (`active` or `ended`), and a link to the person. Sections: Now, Goals, Strengths, Growth areas, Actions, 1:1s, Feedback.

The first time a coaching note is written, ask the owner what may be recorded and what stays out.

## Write it so it holds up

- Observed facts, dated and linked: "shipped the migration two days early", not "reliable".
- Behavior and its impact, never personality, and no guesses about causes.
- Feelings and doubts stay on the day page. They are not carried into the note.
- Leave out health, family matters, beliefs and protected characteristics, unless the owner shared them and they affect the work.
- The note stays in the vault. Draft text for the owner to paste, with only what is needed.

## Prepare a 1:1

1. Read Now, Goals, Actions and the last two 1:1 entries. Run `pkm tasks --link <person>-coaching` for the owner's open actions, and `pkm tasks --for <person>` for the tasks and questions that are theirs to do or decide.
2. Run `pkm since <date of the last 1:1> --about <person>` for what happened since, and `pkm get "<person>#Next time"` for what the owner set aside to raise; its struck lines were raised already.
3. Write an agenda of at most six points: the person's topics first, the open lines of Next time, open actions on both sides, goal progress, what the owner noticed with its evidence, and one open question about how they are doing.
4. Put it on today's page under `### HH:MM 1:1 [[<person>]]` after a yes, or reply with it.

## Record a 1:1

1. After a yes, add a `### YYYY-MM-DD` entry under 1:1s: topics, what they raised in their own words, decisions and agreed actions.
2. Update Actions: mark what was done, and add what was agreed as waiting tasks with a due date. Update Goals and Now. Propose `pkm strike <path:line>` for each Next time line that was raised.
3. The owner's own actions become tasks with `pkm todo`, linked to the coaching note.
4. Ask before writing down anything said in confidence.
5. If the date of the 1:1 is unknown, ask. If it stays unknown, use the date it was written down and say so in the entry.

## Feedback

- Record each piece as situation, behavior and impact, dated, with a link to where it happened.
- Draft feedback from the facts the owner gives you. Keep it specific and short. The owner gives it. You never send it.

## Review periods

1. Collect the period's goals and their state, the feedback and 1:1 entries, and `pkm backlinks <person> --since <start of the period>`.
2. Summarize by goal, then by strength and growth area. Link every claim to its evidence, and name the gaps: "nothing in the notes about ...".
3. Draft only. Ratings, wording on pay or promotion, and performance judgments belong to the owner, and their company's process may apply.

## Stop and ask before

- Writing anything about a performance problem, a complaint, a conflict, pay, promotion or someone leaving. Draft only, mark it sensitive, and suggest the owner checks their company's process or HR.
- Recording something said in confidence.
- Ending a note: set `status: ended`, add a closing Now line, and ask first.

## Check on the team

Run `pkm list type=coaching status=active --show cadence`. For each person, compare the last 1:1 entry with the cadence, and list actions open for more than two weeks. Give one line per person who needs something, and nothing about the others.
