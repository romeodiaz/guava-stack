---
name: guava-stack
description: Makes Notion the owner's shared memory and workspace in Claude and ChatGPT, in their desktop apps and in Claude Code and Codex, by running Notion's official setup guide for agents, adding the steps it leaves to each app, then Guava's parts (a guava-hub with the owner's context and rules, founder-mode, the head-chef and line-cook router, and starter skills in Notion's Skills library). Use when the owner says "set me up", "Follow the Start here steps in github.com/romeodiaz/guava-stack", "update guava-stack" or "uninstall guava-stack".
---

# guava-stack

guava-stack is a small add-on to Notion's official setup guide for agents, [Set up Notion for your agent](https://developers.notion.com/prompts/setup.md). Notion's guide does the setup. This skill adds what the guide leaves to each app (how Claude Code and Codex connect to Notion, where they keep the custom instructions, and how the owner's other apps join), then Guava's parts on top.

It supports four apps on two plans: the Claude desktop app and Claude Code on a Claude plan, and the ChatGPT desktop app and Codex on a ChatGPT plan. The desktop app's **Code** tab (Claude) or **Codex** tab (ChatGPT), set to **Local**, is Claude Code or Codex running on the owner's computer. For anything else, say it isn't supported yet.

## Set up
1. **Run Notion's guide.** Read it in full, then run its steps in order, following its rules for talking with the user, and use steps 2 and 3 below where it leaves the details to your app. Where these steps and Notion's guide cover the same thing, follow Notion's guide. This guava-stack is tested with Notion's version 0.0.5: if the guide shows a newer version, run 0.0.5 from the guide's [changelog](https://developers.notion.com/prompts/setup/changelog.md), which links every version, and tell the owner once that Notion has a newer one.
2. **Connect Notion** (Notion's step 1), in the app you're running in:
   - Claude desktop app: "Open https://claude.ai/customize/connectors?q=notion and click **Connect** next to Notion," then start a new chat if Notion's tools don't show up.
   - ChatGPT desktop app: "Open https://chatgpt.com/plugins?search=notion and click **+** next to Notion," then start a new chat if Notion doesn't show up.
   - Claude Code: `claude mcp list` shows `claude.ai Notion` when Claude Code is signed in with the same Claude account. Only if it doesn't, run `claude mcp add --transport http --scope user notion https://mcp.notion.com/mcp`. If Notion asks for sign-in, have the owner type `/mcp` and approve Notion's sign-in page.
   - Codex: only if `codex mcp list` doesn't show Notion, run `codex mcp add notion --url https://mcp.notion.com/mcp`. If Notion asks for sign-in, run `codex mcp login notion`, and the owner approves Notion's sign-in page.
   - In Claude Code and Codex, a connection added during a session may not reach it: if Notion's tools don't show up, have the owner start a new session and paste the Start here line again. Then finish with Notion's own check: tell the owner their name and workspace.
3. **Save the custom instructions** (Notion's step 2). Every app gets the same text, with the link to the owner's Agent Operating Guide:
   - Claude and ChatGPT desktop apps: the click paths in Notion's guide.
   - Claude Code: the end of `~/.claude/CLAUDE.md`, the file every Claude Code session loads.
   - Codex: the end of the global file every Codex session loads, in `~/.codex`, or in `$CODEX_HOME` when it's set: `AGENTS.override.md` if it's there and not empty, otherwise `AGENTS.md`.

   Guava adds one line at the end of Notion's text, inside the same block, so the owner pastes once:
   ```
   Also use my guava-hub in Notion, which my Agent Operating Guide links: read its context page before work about me or my business, follow its rules page as my own standing rules, and in Claude Code or Codex route work with my guava-router Skill.
   ```
   In Claude Code and Codex, show the owner the exact text and the file, and save it yourself after their yes, as Notion's guide offers. Add to what's there and keep the owner's other lines. Never put it in a project's `CLAUDE.md` or `AGENTS.md`: those live in code repositories, and Notion's guide keeps personal guidance out of them. Then have the owner start a new session and ask "Where does my Agent Operating Guide live?": it passes if the answer gives the guide's link without searching.
4. **Run Notion's steps 3 to 5**, then add **Guava's parts** below, then run Notion's step 6, which records them in the guide's destinations. Then add the owner's other apps.

## Guava's parts
Offer each one with one line on what it does, and do it on a yes. Save into the owner's private pages by default, as Notion's guide says.
- **guava-hub:** a page called guava-hub with two pages, and a mention of Notion's Skills library database, where skills live:
  - **context:** who the owner is and their business, in short bullets under About you, Customers, What you sell, Team, Voice, Tools, Where your time goes and Priorities. Draft it from their website and anything they share, ask a few short questions for the rest, and keep the link each fact came from. Leave out what you're unsure of and ask instead. No passwords, keys or other secrets.
  - **rules:** the owner's own rules and the rules skills they turn on, each set word for word in its own section, listed at the top of the page.
- **founder-mode:** 16 working rules, so the assistants handle safe work on their own, check the real result and ask before anything costly or permanent. Follow [founder-mode](../founder-mode/SKILL.md).
- **Router:** with Claude Code or Codex on the owner's computer, follow **Set it up** in [guava-router](../guava-router/SKILL.md), and save guava-router itself as a Notion Skill (below).
- **Starter skills:** save the ones the owner picks as real Notion Skills in the Skills library, with every file they need, as Notion's step 5 says:
  - [workflow-review](../workflow-review/SKILL.md): "Say 'review my workflows'. I'll rank which of your workflows are worth automating, as a report that stays on your computer."
  - [design-cook-off](../design-cook-off/SKILL.md): "Say 'cook-off' for a page people judge by its look. I'll build it twice with two design skills, and you pick one." It runs in Claude Code or Codex.
  - humanizer-writing, blader's [humanizer](https://github.com/blader/humanizer): "So anything I write for you doesn't sound like AI."
  - ponytail-coding, the `skills/ponytail` skill from Dietrich Gebert's [ponytail](https://github.com/DietrichGebert/ponytail): "When I write code for you, I write the least code that does the whole job."

  Take third-party skills straight from their GitHub repos. Before the yes, say in plain words what their [skills.sh](https://skills.sh) audits found, failed and warning checks included (`https://skills.sh/blader/humanizer`, `https://skills.sh/dietrichgebert/ponytail/ponytail`).

## Add the owner's other apps
Each desktop app pairs with the tool on the same computer: Claude with Claude Code, ChatGPT with Codex. After setup in one, offer the other, and the owner pastes the same Start here line there. An owner with both plans does the same in the other plan's apps. When the owner already has an Agent Operating Guide, joining is short: connect Notion (step 2), check it's the same workspace and guide, save the same custom instructions (step 3), check a new session, then stop. Offer Notion's other steps, such as the daily check or bringing in memories, only if the owner asks, so nothing runs twice.

To reach Claude Code or Codex from the desktop app, the owner opens its **Code** or **Codex** tab, sets it to **Local**, picks their home folder and pastes the Start here line there. If the `claude` or `codex` command is missing on the computer, say so and point to the install steps at https://code.claude.com/docs or https://developers.openai.com/codex, rather than guessing.

## Update
When the owner says "update guava-stack": read this skill again, run the version check from Notion's daily check now, and show any change to the custom instructions, old and then new. Then compare founder-mode's version on the rules page and each Guava skill in the Skills library with this repo's copy, and third-party skills with their GitHub repos and current audits. Change nothing without a yes.

## Uninstall
When the owner says "uninstall guava-stack": show the exact text to remove, then, on a yes, take the custom instructions out of `~/.claude/CLAUDE.md` and Codex's global file from step 3, leaving the owner's other lines, and Guava's line from the desktop apps' custom instructions. Offer to remove the Notion connections steps 2 added to Claude Code and Codex, as their own items, since other work may use them. Everything in Notion stays, since it's the owner's: the Agent Operating Guide, the guava-hub, memories, skills and documents. So do the custom instructions in the desktop apps, which are Notion's setup; tell the owner where they are in case they want them gone too.
