---
name: pkms-init
description: Sets up a Daybook with the owner: checks pkm, asks which vaults, runs pkm init, writes settings after a yes, installs the kit and records a first entry. Use to set up or add a vault.
---

<!-- From agentic-pkms. Kit updates replace this file except a "## This project" section at the end, which belongs to the vault. Edit nothing else. Vault rules go in AGENTS.md "This project". -->

Needs pkm; see the agreement. Step 1 runs without pkm, so it starts from the shell.

# Setting up the Daybook

Ask one question at a time, with an example answer. Accept "skip". Show every line before you write it, and write it only after a yes.

## Steps

1. **Check the tools.** Run `pkm version --require <x.y>` with the version the agreement names, then `pkm doctor`. If pkm is missing (exit 127) or too old (exit 1), stop and give the install line: `brew install zejnilovic/tap/pkm`, or without Homebrew, `make install` in a clone of scripts-pkms (its README). If doctor names a missing tool, stop and name it. Go on only when both pass.
2. **Ask which vaults.** "Which vaults do you want, for example work, personal or family? Give a name for each." For each name, ask where it lives: "Which folder is work in, for example `~/vaults/work`?"
3. **For each vault, in order:**
   1. **Existing setup.** If the folder has `.pkm/`, say so, read `.pkm/config`, and offer only the missing settings. Never work around `pkm init`.
   2. **Create it.** After a yes: `mkdir -p <folder>`, then `cd <folder> && pkm init`. It writes `.pkm/config`, `.pkm/.gitignore` and `.pkmignore`.
   3. **Shared?** "Do others write here, as in a family vault?" If yes, ask the owner's writer name, for example `sam`. Show `writer=sam` for the user config, and append it there.
   4. **Close cycle.** "Do you close each week? Say week, or a cycle such as `sprint 2w from 2026-11-02` (a cycle longer than a week starts from a date) or `payday 1m from 25`." Show `close=<name>` and each `cycle_<name>=...` line for `.pkm/config`, and append after a yes.
   5. **Ignored files.** "What should pkm not see, for example `scans/` or `*.pdf`?" Show the lines and append them to `.pkmignore` after a yes.
   6. **Project folders.** "Should a project's notes sit together in a folder, such as `notes/apollo/` next to `notes/apollo.md`?" Default no: links work either way. If yes, append `part_of_folders=yes` to `.pkm/config`.
   7. **Cross-vault read.** "May an agent read this vault from another vault, for a brief across them?" Default no; a work vault usually stays no. If yes, append `cross_vault=yes` to `.pkm/config`.
   8. **Vault name.** Show `vault_<name>=<folder>` for `~/.config/pkm/config` (or `$XDG_CONFIG_HOME/pkm/config`), and append it after a yes.
   9. **Routines.** "Is there anything you do again and again, such as a weekly status?" For each, offer `pkm todo "<text>" --every <rule> --due <date>`, where the rule is `1w`, `1m` or a cycle name. Run it only after a yes; it writes the routines note.
4. **Install the kit.** For each vault, after a yes, run `agd init Zejnilovic/agentic-pkms` in its folder.
5. **Fill "This project".** Ask the owner three questions: who keeps this vault and in what role; which languages notes are written in; which folders agents must never read. Write the owner's answers in their own words into "This project" in `AGENTS.md`, after a yes. Types and keys of their own, such as an ID that several notes carry, go under "Own types and conventions" when the owner names them.
6. **Finish.** Run `pkm -V <name> config`, `pkm -V <name> doctor` and `pkm vaults` for each vault. Ask for a first line, and record it with `pkm -V <name> add "<text>"` after a yes.
7. **Report.** List each file created or changed, by path.

## Rules

- Never overwrite a file. Create files only with `pkm init`; add settings by appending.
- Write nothing without a yes, and show each line first.
- Put no secrets in any file: no passwords, keys, tokens, or card or account numbers. If the owner offers one, refuse it and say why.
- The user config holds `writer=` and `vault_<name>=`. A vault's `.pkm/config` never holds `writer=`.
