# AI setups

The planner does the thinking and reviews important results; the builder does the doing. Each setup fills those two slots with a model and the command-line tool that runs it. Install and sign in only the tools the owner's setup uses.

The models come from [models.yaml](../../models.yaml); don't edit the tables here by hand, since `scripts/sync-models.py` rewrites them. Commands below are templates for CLI routing. Add `< /dev/null` so neither CLI waits for input. The **In the apps** line under each setup is for app routing, when the owner works in the Claude or ChatGPT app without Grok Bot or Muse.

## Claude + ChatGPT (default)
For owners who pay for both. Each job goes to the model that's best at it, and the work is spread across two plans.

<!-- models:setup name=claude-chatgpt -->
| Slot | Model | Tool | Run it |
|---|---|---|---|
| Planner | Claude Opus 5.5, effort high (`claude-opus-5-5`) | Claude Code | `claude -p --model claude-opus-5-5 "<task>" < /dev/null` |
| Builder | GPT-6.1 Sol, effort high (`gpt-6.1-sol`) | Codex | `codex exec -m gpt-6.1-sol -c model_reasoning_effort=high --skip-git-repo-check "<task>" < /dev/null` |

**In the apps:** plan in the Claude app on Claude Opus 5.5; execute in the ChatGPT app on GPT-6.1 Sol. The hand-off moves the plan from one app to the other.
<!-- /models -->

## ChatGPT only
For owners who only pay for ChatGPT. Both slots run through Codex; skip Claude Code.

<!-- models:setup name=chatgpt-only -->
| Slot | Model | Tool | Run it |
|---|---|---|---|
| Planner | GPT-6 Astra, effort high (`gpt-6-astra`) | Codex | `codex exec -m gpt-6-astra -c model_reasoning_effort=high --skip-git-repo-check "<task>" < /dev/null` |
| Builder | GPT-6.1 Sol, effort high (`gpt-6.1-sol`) | Codex | `codex exec -m gpt-6.1-sol -c model_reasoning_effort=high --skip-git-repo-check "<task>" < /dev/null` |

**In the apps:** both in the ChatGPT app. Plan on GPT-6 Astra and execute on GPT-6.1 Sol, each in its own new chat.
<!-- /models -->

## Claude only
For owners who only pay for Claude. Both slots run through Claude Code; skip Codex.

<!-- models:setup name=claude-only -->
| Slot | Model | Tool | Run it |
|---|---|---|---|
| Planner | Claude Opus 5.5, effort high (`claude-opus-5-5`) | Claude Code | `claude -p --model claude-opus-5-5 "<task>" < /dev/null` |
| Builder | Claude Sonnet 5.5, effort high (`claude-sonnet-5-5`) | Claude Code | `claude -p --model claude-sonnet-5-5 "<task>" < /dev/null` |

**In the apps:** both in the Claude app. Plan on Claude Opus 5.5 and execute on Claude Sonnet 5.5, each in its own new chat.
<!-- /models -->

**In the Claude desktop app's Code tab:** routing is built in. Set the model to `opusplan` (type `/model opusplan`, or set `"model": "opusplan"` in `~/.claude/settings.json`): Claude uses Opus while in Plan mode and switches to Sonnet on its own once the owner approves the plan. `opusplan` always uses Anthropic's current Opus and Sonnet, so it fits as long as the Claude-only picks in models.yaml are an Opus and a Sonnet. Teach the owner one habit: start real work in Plan mode. It works in Local and Remote Control sessions; in Cloud sessions, type `/model opusplan` at the start, since they don't read the computer's settings. Anthropic's docs don't say whether `opusplan` shows in the Code tab's model menu, so set it by command if it doesn't.

Both slots share one Claude plan, so it hits usage limits sooner. There's no non-Claude builder for unattended or always-on jobs: those need an Anthropic API key or get done by hand (see the terms step in the skill).

## Your own picks
Owners can put any model in either slot that a tool in their setup can run: any Claude model through Claude Code, any OpenAI model through Codex. Use the same commands as above with that model's ID and effort, and mark it "(own pick)" in Stack settings so "check for newer models" leaves it alone. For app routing, pick a model the app offers.

## Third-party tools (coming soon)
Support for Cursor, Devin, Factory's Droid, Amp and other tools, as planner, builder or day-to-day assistant, is coming soon. Until then, set up the closest of the three setups above.

## Local models (coming soon)
Support for models that run on the owner's own hardware (through tools like Ollama or LM Studio), so nothing leaves the computer, is coming soon. It pairs with a local Markdown or Obsidian hub for clients that need to stay offline. Until then, say so plainly, and set up the closest of the three setups above if the owner still wants routing.
