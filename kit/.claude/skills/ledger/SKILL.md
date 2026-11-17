---
name: ledger
description: Money and possessions: recording spending and income in a plain-text hledger journal when hledger is installed, and item notes for things the owner owns, with warranty dates. Use when recording a purchase or income, asking what was spent, or adding or finding an item.
---

<!-- From agentic-pkms. Kit updates replace this file except a "## This project" section at the end, which belongs to the vault. Edit nothing else. Vault rules go in AGENTS.md "This project". -->

Needs pkm; see the agreement.

# Ledger and items

Money goes into a plain-text journal in hledger's format. Things the owner owns get an item note. This skill edits notes directly: it appends transactions to the journal file, after a yes. Day-page entries still reach notes only through `pkm post`. Report facts only: never give financial or investment advice, and never move money.

## Tools

Check for hledger with `command -v hledger`. If it is missing, say so and give the install line (`brew install hledger`, or the system's package manager). Do not install it yourself. Without hledger, you may still record entries and items, but you cannot report totals.

## The journal

Keep one file per year: `ledger/YYYY.journal`, in the `ledger/` folder of the vault.

```journal
2026-10-25 Electronics shop | Kettle
    expenses:home:appliances        49.90 EUR  ; item: kettle
    assets:bank:checking

2026-10-26 Lunch with the team
    expenses:food:eating-out        62.00 EUR  ; project: apollo
    liabilities:card:personal
```

- A transaction is a date, a payee, and two or more postings that add up to zero. One amount may be left out.
- Accounts: `expenses:<area>:<what>`, `income:<source>`, `assets:bank:<nickname>`, `liabilities:card:<nickname>`. Reuse existing ones (`hledger -f ledger/<year>.journal accounts`).
- Comments can link the vault: `; item: <name>`, `; project: <name>`, `; source: <capture>`.
- Every amount has its currency. Convert only with a rate the owner gives.
- Use nicknames for accounts. Never write an account, card or IBAN number.

## Record

1. From what the owner gives (a receipt, a statement line, "I paid 50 for dinner"), take the date, payee, amount, currency and account. Ask for what is missing. Never guess an amount or a date.
2. After a yes, add the transaction at the end of `ledger/<year>.journal`, creating the file for the year's first entry.
3. If hledger is installed, run `hledger -f ledger/<year>.journal check` and fix the entry if it fails.
4. Report the entry in one line.

## Reports

hledger adds up. Never add up by hand. Report the numbers as hledger prints them, with the command you ran:

- Spending by category this month: `hledger -f ledger/2026.journal balance expenses -p thismonth`
- Spending per month: `hledger -f ledger/2026.journal balance expenses --monthly --depth 2`
- Everything for a project: `hledger -f ledger/2026.journal register tag:project=apollo`

## Items

Create one with `pkm new item "<name>"`, in the folder that `folder_item` names, `notes/` by default. Frontmatter: `status` (`owned`, `lent`, `broken`, `sold` or `gone`), `bought`, `price` (with its currency), `shop`, `warranty` (the date it ends), `serial`, and `location`. `pkm upcoming` lists warranty dates in the next two weeks.

- Details: the model, a link to the manual, and the receipt, if the owner keeps one in the vault.
- Log: repairs, who it was lent to and when, changes.
- When sold or gone: set the status, add a log line, and ask before moving it to `archive/`.

## Rules

- Record only what the owner gives you, with its source line.
- Never write account numbers, card numbers or passwords.
