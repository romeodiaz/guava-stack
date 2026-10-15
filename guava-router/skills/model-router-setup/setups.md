# AI setups

The planner does the thinking; the worker does the doing. Each setup fills those two slots with a model and the command-line tool that runs it. Install and sign in only the tools the owner's setup uses.

Commands below are templates for CLI routing. Add `< /dev/null` so neither CLI waits for input. The **In the apps** line under each setup is for app routing, when the owner works in the Claude or ChatGPT app without Grok Bot or Muse.

## Claude + ChatGPT (default)
For owners who pay for both. Each job goes to the model that's best at it, and the work is spread across two plans.

| Slot | Model | Tool | Run it |
|---|---|---|---|
| Planner | Claude Opus 5.5, effort high (`claude-opus-5-5`) | Claude Code | `claude -p --model claude-opus-5-5 "<task>" < /dev/null` |
| Worker | GPT-6.1 Sol, reasoning effort high (`gpt-6.1-sol`) | Codex | `codex exec -m gpt-6.1-sol -c model_reasoning_effort=high --skip-git-repo-check "<task>" < /dev/null` |

**In the apps:** plan in the Claude app on Claude Opus 5.5; execute in the ChatGPT app on GPT-6.1 Sol. The hand-off moves the plan from one app to the other.

## ChatGPT only
For owners who only pay for ChatGPT. Both slots run through Codex; skip Claude Code.

| Slot | Model | Tool | Run it |
|---|---|---|---|
| Planner | Astra, reasoning effort high | Codex | `codex exec -m <Astra model ID> -c model_reasoning_effort=high --skip-git-repo-check "<task>" < /dev/null` |
| Worker | GPT-6.1 Sol, reasoning effort high (`gpt-6.1-sol`) | Codex | as in the default setup |

Find Astra's exact model ID in Codex's `/model` menu and use what it shows. Don't guess it.

**In the apps:** both in the ChatGPT app. Plan on Astra and execute on GPT-6.1 Sol, each in its own new chat.

## Claude only
For owners who only pay for Claude. Both slots run through Claude Code; skip Codex.

| Slot | Model | Tool | Run it |
|---|---|---|---|
| Planner | Claude Opus 5.5, effort high (`claude-opus-5-5`) | Claude Code | as in the default setup |
| Worker | Claude Sonnet 5.5, effort high (`claude-sonnet-5-5`) | Claude Code | `claude -p --model claude-sonnet-5-5 "<task>" < /dev/null` |

**In the apps:** both in the Claude app. Plan on Claude Opus 5.5 and execute on Claude Sonnet 5.5, each in its own new chat.

Both slots share one Claude plan, so it hits usage limits sooner. There's no non-Claude worker for unattended or always-on jobs: those need an Anthropic API key or get done by hand (see the terms step in the skill).

## Other tools or a custom mix
For owners who use Cursor, Devin, Factory's Droid, Amp or another AI tool, or who want any other pairing (for example Opus as planner and Cursor as worker). Any tool can fill either slot.

1. Ask which tools they pay for. Suggest the strongest reasoning model they have as planner and the fastest capable one as worker, and let them pick.
2. For each slot, record four things in Stack settings: the tool, the model, its effort setting, and how to hand it a job.
3. **Tools with a CLI:** find the non-interactive command in the tool's docs or its `--help`, then test it. Examples to confirm on the owner's machine: Cursor's `cursor-agent -p`, Droid's `droid exec`, Amp's `amp -x`. Install only what's missing, with a yes, and sign in with the owner's own account.
4. **Tools that run in the cloud** (such as Devin) take jobs through their own app, Slack or API, not a local command. Record how the owner hands them work, and check their results like any worker's.
5. Connect each tool to the hub if it supports the hub's connector or MCP server. Most of these tools also read an `AGENTS.md` file for standing instructions; check the tool's docs. If a tool can't reach the hub, the planner passes it what it needs (see the hand-off rule in the skill).
6. Follow each tool's own terms of service.

**In the apps:** use whichever apps hold the owner's planner and worker, the same way as the setups above.
