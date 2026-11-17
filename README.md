# agentic-pkms

An AI agent for a personal knowledge vault: plain Markdown that you write and decide on. [pkm](https://github.com/Zejnilovic/scripts-pkms) finds and copies; the agent reads, asks and drafts. This kit gives it the rules, skills and agents. [Working with a knowledge agent](docs/methodology.md) explains why.

## Start

1. **Install pkm once per machine.** It needs bash, [ripgrep](https://github.com/BurntSushi/ripgrep) and [jq](https://jqlang.org). From a clone of [scripts-pkms](https://github.com/Zejnilovic/scripts-pkms), run `make install`; or unpack its release tarball and run `sh install.sh`. Then run `pkm doctor`. Exit 0 means it is ready.
2. **Make a vault** in a new folder, then install the kit. Git is recommended, so every change an agent makes is a diff you can review.

   ```bash
   mkdir ~/vault && cd ~/vault && git init
   pkm init
   agd init Zejnilovic/agentic-pkms
   ```

   [agd](https://zejnilovic.github.io/agd) copies the kit into the vault.
3. **Or let the agent do it.** Ask it to run the `pkms-init` skill. It checks pkm, asks which vaults you want, and writes each setting only after you say yes.
4. **Describe the vault.** Fill in "This project" at the end of `AGENTS.md`: who keeps the vault, the languages you write in, and any folder agents must not read.
5. **Capture and find.** Write an entry with `pkm add "Called Jane Doe about the offer"`, and search with `pkm find offer`. Or just ask the agent: "remember that Jane Doe called".

   `agd init` installs the kit from its first release (0.1.0), so it needs that release to be out; until then, copy the kit from this repository.

## What the agent does

- **Brief**: what is new, important and needs attention, from what you wrote since the last brief.
- **Posting**: proposes where each entry belongs; you answer by number; pkm copies it word for word.
- **Close**: asks about each open task and question, and records what you decide.
- **Check-in**: asks at most five questions about whether your notes are still true.
- **Rounds**: reads your project tools for what changed for you, read only.
- **Recall**: asks your own questions back on a schedule with `pkm recall`. The `study` pack uses it.
- **Find**: answers from your notes, with sources.

## The rules

1. Your words stay yours: entries are copied, never rewritten.
2. Every claim links its source. Nothing is deleted, and nothing is invented.
3. Nothing happens in your name. The agent proposes and drafts; it never sends, posts or commits unless you ask.

## Skills

| Skill | Pack | Use it for |
|---|---|---|
| [`vault-search`](kit/.claude/skills/vault-search/SKILL.md) | core | Finding things in a vault too big to read: summaries first, then pkm searches. |
| [`tasks`](kit/.claude/skills/tasks/SKILL.md) | core | Adding, finishing and planning your tasks with pkm. |
| [`posting`](kit/.claude/skills/posting/SKILL.md) | core | Filing entries into notes, on your answers by number. |
| [`review`](kit/.claude/skills/review/SKILL.md) | core | The brief and the close. Runs only when you ask. |
| [`check-in`](kit/.claude/skills/check-in/SKILL.md) | core | Asking whether your notes are still true, and talking a decision through. |
| [`pkms-init`](kit/.claude/skills/pkms-init/SKILL.md) | core | Setting up a vault with you, one question at a time. |
| [`coaching`](kit/.claude/skills/coaching/SKILL.md) | coaching | Coaching notes, 1:1 preparation and records, feedback drafts. |
| [`projects`](kit/.claude/skills/projects/SKILL.md) | projects | Project overviews, rounds over your project tools, and updates. |
| [`writing`](kit/.claude/skills/writing/SKILL.md) | writing | Articles, guides and posts, from idea to published. |
| [`ledger`](kit/.claude/skills/ledger/SKILL.md) | ledger | Spending in an hledger journal, and notes on things you own. |
| [`study`](kit/.claude/skills/study/SKILL.md) | study | Quizzing you on your own notes with `pkm recall`, and proposing questions for a course. |

## Agents

| Agent | Pack | Role |
|---|---|---|
| [`chief-of-staff`](kit/.claude/agents/chief-of-staff.md) | core | The secretary: brief, close, filing and check-ins, on request. |
| [`retriever`](kit/.claude/agents/retriever.md) | core | Answers questions across the vault in its own context. Read only. |
| [`coach`](kit/.claude/agents/coach.md) | coaching | Prepares and records 1:1s and drafts feedback. Drafts only. |
| [`editor`](kit/.claude/agents/editor.md) | writing | Reviews a draft for its point, structure and claims. Does not rewrite it. |

## Packs

| Pack | Contents | Requires |
|---|---|---|
| `core` | The working agreement, the core skills and agents above | nothing: pkm is installed once per machine |
| `coaching` | Coaching skill and coach agent | `core` |
| `projects` | Projects skill | `core` |
| `writing` | Writing skill and editor agent | `core` |
| `ledger` | Ledger skill | `core` |
| `study` | Study skill: courses, questions and the quiz | `core` |

Rounds need the `gh`, `az` or `acli` command of each place you use, signed in by you. The ledger's totals need hledger. The agent says when a tool is missing.

## Working on this repo

Maintainers: see [AGENTS.md](AGENTS.md). Run `python3 scripts/check.py` before committing.

## License

[MIT](LICENSE) © Sasa Zejnilovic
