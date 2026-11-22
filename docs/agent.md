# For your AI agent

Hand this page to Claude Code, Copilot or another assistant, for example: *"Read https://zejnilovic.github.io/agentic-pkms/agent/ and help me set up a Daybook vault."* It says where everything is. The rules themselves live in the kit's files, so this page can't fall behind them.

## To the agent

You are helping someone keep a vault by the Daybook Method: a folder of plain Markdown they write, with one page a day, a close each week, and notes that grow from the days. The owner decides; you propose. Read the files below instead of relying on this page.

### Where things are

| What | Where |
|---|---|
| The working agreement: the rules every agent follows in a vault | [kit/AGENTS.md](../kit/AGENTS.md). It names the pkm version it needs in its `pkm version --require` line. |
| The skills: brief, posting, close, tasks, search, setup and the optional packs | `kit/.claude/skills/<name>/SKILL.md`, listed in [the README's Skills table](../README.md#skills) |
| The agents (roles) | `kit/.claude/agents/`, listed in [the README's Agents table](../README.md#agents) |
| Which files belong to which pack | [packs.txt](../packs.txt) |
| Why the kit works the way it does | [How it works](methodology.md) |
| The method itself, without an agent | [The Daybook Method](https://github.com/Zejnilovic/scripts-pkms/blob/main/docs/method.md) |
| pkm's commands | `pkm help`, `pkm help <command>`, and [Commands](https://github.com/Zejnilovic/scripts-pkms/blob/main/docs/commands.md) |
| What pkm prints and its exit codes | [The output contract](https://github.com/Zejnilovic/scripts-pkms/blob/main/docs/contract.md) |
| The file format of a vault | [The file format](https://github.com/Zejnilovic/scripts-pkms/blob/main/docs/format.md) |

Links to files on GitHub point to `main`, which can be ahead of the latest release. The kit in a vault comes from a release, and the first line of a vault's `AGENTS.md` says which.

### Setting up a vault

1. **pkm**, the command line that every skill calls. Run `pkm doctor`. If pkm is missing, give the owner the install from [pkm's README](https://github.com/Zejnilovic/scripts-pkms#install) and let them run it.
2. **The vault.** Ask the owner where it goes, then `git init` and `pkm init` in that folder. Git is recommended, so every change you make is a diff they can review. To show them what a vault looks like after a few weeks, `pkm example` copies one into a new folder (pkm 0.9 or later).
3. **The kit**, with [agd](https://zejnilovic.github.io/agd/): `agd init Zejnilovic/agentic-pkms` copies the kit into the vault at its latest release and asks which packs to install; `agd update` brings it up to date later. If agd is missing, give the owner [its install](https://zejnilovic.github.io/agd/install/).
4. **The vault's own facts.** With the owner, fill in "This project" at the end of the vault's `AGENTS.md`: who keeps it, the languages they write in, and any folder you must not read. The `pkms-init` skill walks through this and the vault's settings.

### Your assistant and the kit

Claude Code reads `CLAUDE.md`, which imports `AGENTS.md`, and loads the skills and agents in `.claude/`. Other assistants that read `AGENTS.md`, such as Copilot, get the working agreement; whether they load `.claude/skills` depends on the assistant. If yours doesn't, open the task's `SKILL.md` and follow it.
