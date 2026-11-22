---
template: home.html
title: The agentic Daybook
description: An AI agent for a Daybook vault. It reads your week, asks and drafts the brief, the posting and the close. Every line links its source, nothing is deleted or sent, and nothing happens without your yes.
hide:
  - navigation
  - toc
---

## Set it up

The kit is a set of instructions, skills and agents copied into your vault. It is written for Claude Code, its working agreement is a plain `AGENTS.md` that other assistants read too, and it needs [pkm](https://zejnilovic.github.io/scripts-pkms/), installed once per machine.

1. **Install pkm:** `brew install zejnilovic/tap/pkm`, which brings ripgrep, jq and tab completion. Without Homebrew, see [pkm's install](https://github.com/Zejnilovic/scripts-pkms#install). Then run `pkm doctor`. Exit 0 means it is ready.
2. **Make a vault and install the kit** with [agd](https://zejnilovic.github.io/agd/). Git is recommended, so every change an agent makes is a diff you can review.

    ```bash
    mkdir ~/vault && cd ~/vault && git init
    pkm init
    agd init Zejnilovic/agentic-pkms
    ```

3. **Or let the agent do it.** Ask it to run the `pkms-init` skill. It checks pkm, asks which vaults you want, and writes each setting only after you say yes.
4. **Describe the vault.** Fill in "This project" at the end of `AGENTS.md`: who keeps it, the languages you write in, and any folder agents must not read.
5. **Ask for a brief.** "What's new? What needs me?"

Or hand [For your AI agent](agent.md) to your assistant: it lists the files and links it needs to do these steps with you.

Optional packs add coaching, projects, writing, a ledger and studying. The [README](https://github.com/Zejnilovic/agentic-pkms#packs) lists every skill, agent and pack.

[How it works](methodology.md){ .md-button .md-button--primary } [For your AI agent](agent.md){ .md-button } [The Daybook Method](https://zejnilovic.github.io/scripts-pkms/){ .md-button }
