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

1. **Install pkm.** It needs bash, [ripgrep](https://github.com/BurntSushi/ripgrep) and [jq](https://jqlang.org). From a clone of [scripts-pkms](https://github.com/Zejnilovic/scripts-pkms), run `make install`, then `pkm doctor`. Exit 0 means it is ready.
2. **Make a vault and install the kit** with [agd](https://zejnilovic.github.io/agd/). Git is recommended, so every change an agent makes is a diff you can review.

    ```bash
    mkdir ~/vault && cd ~/vault && git init
    pkm init
    agd init Zejnilovic/agentic-pkms
    ```

3. **Or let the agent do it.** Ask it to run the `pkms-init` skill. It checks pkm, asks which vaults you want, and writes each setting only after you say yes.
4. **Describe the vault.** Fill in "This project" at the end of `AGENTS.md`: who keeps it, the languages you write in, and any folder agents must not read.
5. **Ask for a brief.** "What's new? What needs me?"

Optional packs add coaching, projects, writing, a ledger and studying. The [README](https://github.com/Zejnilovic/agentic-pkms#packs) lists every skill, agent and pack.

[How it works](methodology.md){ .md-button .md-button--primary } [The Daybook Method](https://zejnilovic.github.io/scripts-pkms/){ .md-button }
