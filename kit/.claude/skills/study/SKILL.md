---
name: study
description: Quizzes the owner on what they studied, from their own notes: one question at a time, their answer first, then their note's answer, and recall marks moved by pkm. Use to quiz the owner, or to propose questions for a course.
---

<!-- From agentic-pkms. Kit updates replace this file except a "## This project" section at the end, which belongs to the vault. Edit nothing else. Vault rules go in AGENTS.md "This project". -->

Needs pkm; see the agreement.

# Study

You quiz the owner from their own notes. You never teach from general knowledge. A question is the owner's words, with the owner's answer indented below and linked to its source. pkm moves each question up or back on the ladder; you do not do the arithmetic.

## A course

Create one with `pkm new course "<title>"`. It has frontmatter (`type: course`, `status`, `summary`, `aliases`) and two sections: `## Modules`, the topics in order with a link to each source, and `## Questions`, where the accepted questions are written.

## Question format

```markdown
- When is the median better than the mean? (recall 2026-11-16 1d)
  - When a few extreme values pull the mean away ([[2026-11-10]])
```

The mark `(recall <date> <N>d)` ends the question line. Its date is when to ask. The answer is indented below, with a link to its day or source note. `pkm recall add` writes this form for you.

## Quiz

1. Run `pkm recall <course>` for the course's questions due today or earlier, or `pkm recall` for everything due. Oldest first, each as `path:line: text`.
2. Ask one question, quoting it word for word. Ask for the owner's answer from memory.
3. After they reply, show their own answer, the indented line under the question, with its source. If the question has no answer in the notes, say "your notes have no answer for this" and stop there. Do not supply one.
4. Ask: did you know it? Use the owner's answer only.
5. After the owner answers, run `pkm recall <path:line> yes` or `pkm recall <path:line> no`, with the line from step 1. pkm prints the rewritten line.
6. Go on to the next question. Stop when the due list is empty, or when the owner says stop.

## Propose questions

1. Read what the owner studied: `pkm since <date> --about <course>`, and the course's modules, with each line's source.
2. Propose at most five questions. Each quotes its source, and each is phrased in the owner's own words where they wrote them. Use a plain question in the note's language otherwise. Each has its answer and its source.
3. The owner accepts each one, changes it, or replaces it. Nothing is written until they say yes.
4. For each accepted question, after a yes, write it into the course with its answer, word for word:

   ```bash
   pkm recall add <course> "<question, word for word>" --answer "<the owner's answer, with its source link>"
   ```

   It goes at the end of the course's `## Questions`, due tomorrow. Give each answer as its own `--answer`.
5. Do not write questions on day pages, and do not post them: a day page is a record.

## Time studied

When the owner asks how long they studied, run `pkm since <date or cycle> --under <course> --sum`, or `--under learning` for every course of the area. pkm counts the entries timed as a range, `- 19:00-20:30 …`, and those ending in a duration such as `(1h30)`. Give the total as pkm prints it, with the lines it lists. Never add up time yourself.

## Rules

- Quiz only from the owner's notes. If a note has no answer, say so.
- Show the owner's answer only after they reply.
- Write question and answer text exactly as the owner accepted it. Never reword it.
- Questions live in the course note, so `pkm recall` moves their marks there.
- Never tell the owner whether they were right. Show what their note says and let them compare.
- One question at a time. No more than five proposals per round.
