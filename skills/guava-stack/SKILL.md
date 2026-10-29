---
name: guava-stack
description: Makes Notion the owner's shared memory and workspace in Claude and ChatGPT, in their desktop apps and in Claude Code and Codex, by running Notion's official setup guide for agents and adding only the steps it leaves to each app. Use when the owner says "set me up", "Follow the Start here steps in github.com/romeodiaz/guava-stack", "update guava-stack" or "uninstall guava-stack".
---

# guava-stack

guava-stack is a small add-on to Notion's official setup guide for agents, [Set up Notion for your agent](https://developers.notion.com/prompts/setup.md). Notion's guide does the setup. This skill adds only what the guide leaves to each app: how Claude Code and Codex connect to Notion, where they keep the custom instructions, and how the owner's other apps join.

It supports four apps on two plans: the Claude desktop app and Claude Code on a Claude plan, and the ChatGPT desktop app and Codex on a ChatGPT plan. The desktop app's **Code** tab (Claude) or **Codex** tab (ChatGPT), set to **Local**, is Claude Code or Codex running on the owner's computer. For anything else, say it isn't supported yet.

## Set up
1. **Run Notion's guide.** Read it in full, then run its steps in order, following its rules for talking with the user. Where these steps and Notion's guide cover the same thing, follow Notion's guide. This guava-stack is tested with Notion's version 0.0.5: if the guide shows a newer version, run 0.0.5 from the guide's [changelog](https://developers.notion.com/prompts/setup/changelog.md), which links every version, and tell the owner once that Notion has a newer one.
2. **Connect Notion** (Notion's step 1), in the app you're running in:
   - Claude desktop app: "Open https://claude.ai/customize/connectors?q=notion and click **Connect** next to Notion," then start a new chat if Notion's tools don't show up.
   - ChatGPT desktop app: "Open https://chatgpt.com/plugins?search=notion and click **+** next to Notion," then start a new chat if Notion doesn't show up.
   - Claude Code: `claude mcp list` shows `claude.ai Notion` when Claude Code is signed in with the same Claude account. Only if it doesn't, run `claude mcp add --transport http --scope user notion https://mcp.notion.com/mcp`, and have the owner type `/mcp` and approve Notion's sign-in page.
   - Codex: unless `codex mcp list` already shows Notion, run `codex mcp add notion --url https://mcp.notion.com/mcp`, then `codex mcp login notion`, and the owner approves Notion's sign-in page.
3. **Save the custom instructions** (Notion's step 2). Every app gets the same text, with the link to the owner's Agent Operating Guide:
   - Claude and ChatGPT desktop apps: the click paths in Notion's guide.
   - Claude Code: the end of `~/.claude/CLAUDE.md`, the file every Claude Code session loads.
   - Codex: the end of `~/.codex/AGENTS.md` (or `AGENTS.md` in `$CODEX_HOME` when it's set), the file every Codex session loads.

   In Claude Code and Codex, show the owner the exact text and the file, and save it yourself after their yes, as Notion's guide offers. Add to what's there and keep the owner's other lines. Never put it in a project's `CLAUDE.md` or `AGENTS.md`: those live in code repositories, and Notion's guide keeps personal guidance out of them. Then have the owner start a new session and ask "Where does my Agent Operating Guide live?": it passes if the answer gives the guide's link without searching.
4. **Finish Notion's guide** (its steps 3 to 6), then add the owner's other apps below.

## Add the owner's other apps
Each desktop app pairs with the tool on the same computer: Claude with Claude Code, ChatGPT with Codex. After setup in one, offer the other. In it, the owner pastes the same Start here line. There, Notion's guide finds the Agent Operating Guide the owner already has and keeps it, so only steps 2 and 3 above are new: connect Notion and save the same custom instructions. An owner with both plans does the same in the other plan's apps.

To reach Claude Code or Codex from the desktop app, the owner opens its **Code** or **Codex** tab, sets it to **Local**, picks their home folder and pastes the Start here line there. If the `claude` or `codex` command is missing on the computer, say so and point to the install steps at https://code.claude.com/docs or https://developers.openai.com/codex, rather than guessing.

## Update
When the owner says "update guava-stack": read this skill and Notion's guide again, run the version check from Notion's daily check now, and compare the custom instructions saved in each app with the approved version. Show what differs, old and then new, and change nothing without a yes.

## Uninstall
When the owner says "uninstall guava-stack": show the exact text to remove, then, on a yes, take the custom instructions out of `~/.claude/CLAUDE.md` and `~/.codex/AGENTS.md`, leaving the owner's other lines. Offer to remove the Notion connections steps 2 added to Claude Code and Codex, as their own items, since other work may use them. Everything in Notion stays, since it's the owner's: the Agent Operating Guide, memories, skills and documents. So do the custom instructions in the desktop apps, which are Notion's setup; tell the owner where they are in case they want them gone too.
