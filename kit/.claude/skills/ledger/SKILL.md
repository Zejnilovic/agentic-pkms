---
name: ledger
description: Money and possessions: recording spending and income in a plain-text hledger journal when hledger is installed, each tied to its note, and item notes for things the owner owns, with warranty dates. Use when recording a purchase or income, asking what something cost or whether an invoice was paid, or adding or finding an item.
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
    expenses:home:appliances        49.90 EUR  ; note: kettle
    assets:bank:checking

2026-11-02 Joe Bloggs | Deposit for the bathroom
    expenses:home:repairs          500.00 EUR  ; note: bathroom, source: 2026-11-02-sam
    assets:bank:checking
```

- A transaction is a date, a payee, and two or more postings that add up to zero. One amount may be left out.
- Accounts: `expenses:<area>:<what>`, `income:<source>`, `assets:bank:<nickname>`, `liabilities:card:<nickname>`. Reuse existing ones (`hledger -f ledger/<year>.journal accounts`).
- `; note: <name>` ties a posting to the note it belongs to: a project, an area, an item or a person, by the note's name, as in a link. `; source: <day page>` names the page where the owner wrote it. Older entries may use `; project:` or `; item:`; read them the same way.
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
- What a note cost, such as the bathroom: `hledger -f ledger/2026.journal register 'tag:note=^bathroom$'`, and its total with `balance` in place of `register`. Add the years it spans with one `-f` per journal. For older entries, run it again with `tag:project=` or `tag:item=`.

## Invoices

1. The hours to bill come from `pkm since <first day> --under <client> --sum`, as pkm prints them: the client's note and the projects under it. The rate and the amount come from the owner; never work out an amount they didn't give.
2. Sending an invoice is a task with a wait: `- [ ] Invoice [[acme]] for October (waiting 2026-11-03)`, through the `tasks` skill.
3. When the owner says it was paid, propose two things: `pkm done <words>` for the task, and the income, `income:clients:<name>` with `; note: <the client or project>`, dated the day it arrived.
4. "Is it paid?" is answered from the task (`pkm tasks waiting`) and the journal (`register 'tag:note=^acme$' income`), each with its source. Never assume a payment that neither shows.

## Items

Create one with `pkm new item "<name>"`, in the folder that `folder_item` names, `notes/` by default. Frontmatter: `status` (`owned`, `lent`, `broken`, `sold` or `gone`), `bought`, `price` (with its currency), `shop`, `warranty` (the date it ends), `serial`, and `location`. `pkm upcoming` lists warranty dates in the next two weeks.

- Details: the model, a link to the manual, and the receipt, if the owner keeps one in the vault.
- Log: repairs, who it was lent to and when, changes.
- When sold or gone: set the status, add a log line, and ask before moving it to `archive/`.

## Rules

- Record only what the owner gives you, with its source line.
- Never write account numbers, card numbers or passwords.
