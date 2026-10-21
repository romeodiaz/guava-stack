---
name: design-cook-off
description: Before any AI tool builds a page or screen people will judge by its look, such as a landing page, marketing site, one-pager, offer or product page, portfolio, hero section, or a new app screen like a dashboard, makes two versions at the same time on the head-chef model, one with the impeccable design skill and one with taste-skill, and lets the owner pick. Use when the owner asks for any of these, says something looks generic, templated or AI-made, or says "cook-off" or "taste-test". Skip for emails, posts, Notion pages, docs, slides, charts, reports with a fixed template, and small changes inside a page that already has a design.
---

# Design cook-off

AI-built pages look alike: a centered headline, a small label above it, three icon cards, a soft purple gradient. Two design skills fix this in different ways. **impeccable** ([pbakaus/impeccable](https://github.com/pbakaus/impeccable)) works like a design director with a rule book: it builds from what the product is, bans the common AI tells, and its engine checks the result against 61 detector rules. **taste-skill** ([leonxlnx/taste-skill](https://github.com/leonxlnx/taste-skill), installed as `design-taste-frontend`) works like an art director with a library: a script deals researched directions from 247 gallery sites, and the run picks one and screenshots its way to a finished page. This skill runs both on the same brief at once and shows the owner both.

## When it's worth it

Each run costs two head-chef runs, so use it only where a designed look changes the result.

- **Use:** a page someone outside the business sees and judges by its look first: landing pages, offer and pricing pages, marketing sites, one-pagers, portfolios, hero sections, event or launch pages. Also new app screens (dashboards, settings, inboxes) when the look matters to a client. This is where plain AI output is most generic and both skills help most.
- **Skip:** writing (emails, posts, Notion pages, docs), slides, charts (use a chart skill), reports built from a fixed template such as the free AI assessment, and small edits inside a page that already has its own design. There the design is already decided, and the skills add little beyond plain Claude.
- If unsure, ask the owner in one line: "This is a page people will judge by its look. Want two designed versions to pick from? It takes about 20 minutes."

## Needs

- Both skills installed in Claude Code, straight from their GitHub repos: copy the `impeccable` folder from impeccable's `.claude/skills/` to `~/.claude/skills/impeccable`, and the `skills/taste-skill` folder from taste-skill to `~/.claude/skills/design-taste-frontend`. Both are third-party and their skills.sh audits show warnings (low to medium), so install them only after showing the owner what the audits found and getting a yes, as founder-mode says. Don't turn on impeccable's hooks.
- Node (taste-skill's scripts) and Chrome or Brave (both skills look at the page in a headless browser).
- If you're not in Claude Code (the Claude or ChatGPT app, Grok Bot, Muse), hand the whole job to the head-chef in Claude Code, as guava-router says, and pass the brief from step 1. With no Claude Code to hand it to, say so in one line and build the page the usual way.

## 1. Write one brief

Both runs get the same brief, word for word, so the only difference is the skill. Save it as `brief.md` in a new folder, `~/Downloads/design-cook-off-<YYYY-MM-DD>-<name>/`:

- What it is, who it's for, and the one or two things they should do (with the real links).
- Every fact, number and claim the page may use, from the hub, Notion Memory or the owner. Say plainly what doesn't exist yet (logos, testimonials, photos), and that nothing may be invented.
- The voice from the context page.
- What to deliver: one self-contained `index.html` unless the project says otherwise, the widths it must work at (1440px and 390px), and any brand assets to use.
- "Don't ask questions: this brief is complete." Ask the owner anything missing before the runs, not during them.

## 2. Run both at once

Re-read the head-chef's model line first. Start two agents in the same step, each on the head-chef's model and effort, each writing only to its own subfolder (`impeccable/` and `taste/`):

- **A:** "Use the impeccable skill for new work. Build the page in brief.md." Its engine downloads on first run from the project's GitHub releases and checks its checksum. Don't use its `live` mode.
- **B:** "Use the design-taste-frontend skill and follow its run. Build the page in brief.md." It may use the photos its library deals. Don't run its `assets.mjs` image search unless the owner asked for found imagery: it pulls search results from public archives into the run.

Tell each agent to answer its skill's own questions from the brief, to use no other design skill, and to finish only after looking at the page at both widths and fixing what it sees. impeccable starts a reviewer of its own near the end, and the review can reach you instead of A: if A says it's waiting on a reviewer that already reported to you, send A the review.

## 3. Check facts and links

Check each page for mistakes only, never for looks:

- Every fact matches the brief, with nothing invented: no numbers, quotes, clients, logos or people that the brief doesn't hold. Numbers a run worked out itself, such as a price after a credit, count as new claims: list them for the owner.
- Links go where the brief says, and the page opens with no console errors at 1440px and 390px.
- Fix a wrong fact or a broken link in place and say what you fixed. If a page doesn't open at all, rerun that side.

## 4. Show the owner both files

Which one looks better is the owner's call alone. Don't compare, describe, score or rank the two pages, don't run either skill's checker against the other's page, and don't recommend one. Open both in the owner's browser (or send both files), labeled **A · impeccable** and **B · taste-skill**, with any facts from step 3 for them to confirm, and ask: "Which one do you want to build on?"

## 5. Build on the pick

Keep improving the page they pick with the skill that made it, as they ask: impeccable's commands (such as polish, bolder, quieter or typeset), or another taste-skill run on that page. Leave the other file as it is.

## 6. Note the pick

When the owner picks, save one line to Notion Memory, under a **Design cook-off** memory (update it, don't add a new one): the date, the kind of page and which skill they picked, plus their reason if they gave one.
