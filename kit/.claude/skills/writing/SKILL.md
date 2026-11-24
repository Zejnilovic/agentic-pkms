---
name: writing
description: Articles, guides, newsletters, posts and talks, from idea through outline and draft to published, built from the owner's notes and sources, in their voice and language. Use when starting, outlining, drafting or publishing a piece.
---

<!-- From agentic-pkms. Kit updates replace this file except a "## This project" section at the end, which belongs to the vault. Edit nothing else. Vault rules go in AGENTS.md "This project". -->

Needs pkm; see the agreement.

# Writing

A piece is assembled from notes the owner already has, not written from nothing. The owner is the author. You find the material, propose the structure, draft when asked, and check. The voice and the opinions are theirs.

## The piece

Create it with `pkm new writing "<working title>" --set key=value ...`; move it on with `pkm set <name> status=<status>`. It is one note for the piece's whole life, in the folder that `folder_writing` names (`notes/` by default). Frontmatter: `form` (`article`, `guide`, `newsletter`, `post` or `talk`), `status` (`idea`, `outline`, `draft`, `review`, `published` or `dropped`), `audience`, `venue`, `language`, `due`, `url`, and `sources` (links to the notes it uses). Sections: Idea, Outline, Draft. A translation or another form of the piece is its own note, linked from the original.

## From idea to outline

1. Write the idea first: the one thing the reader should take away. Ask the owner if it is unclear.
2. Find material with `pkm find` and `pkm backlinks`, starting from hub notes. At most 15 candidates, each with one line on what it adds.
3. Propose an outline: one heading per section, its point, and the notes it draws on, each linked. Name the gaps: claims that need a source the vault does not have.
4. After a yes, set `sources` and `status=outline` with `pkm set`, and wait for the owner's comments.

## Draft

- Only when asked, and in the piece's language.
- In the owner's voice. Follow the writing-style note if the owner kept one, named by `folder_writing`; otherwise follow two or three of their published pieces (`pkm list type=writing status=published`). Offer to write that note from them. It is the owner's file.
- Use the wording of their notes where it fits.
- Mark every claim that needs a source or a number with `[source?]`.
- Add no opinions, examples or stories the owner did not give you. Ask for them.
- Never invent quotes, figures, studies or experiences.

## Review and publish

- The `editor` agent reviews a draft. It does not rewrite it.
- When published, after a yes: `pkm set <name> status=published url=<address>`, and add the date. Notes the piece used can link back to it.
- Changes after publishing go into the same note.

## Rules

- Summarize sources in your own words. Quote briefly, with attribution, only what the piece needs.
- You never send or publish anything.
