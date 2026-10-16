# AI setups

The head-chef does the thinking and reviews important results; the line-cook does the doing. Each setup fills those two slots with a model and the command-line tool that runs it. Install and sign in only the tools the owner's setup uses.

The models come from [models.yaml](https://github.com/romeodiaz/guava-stack/blob/main/guava-router/models.yaml); don't edit the tables here by hand, since `scripts/sync-models.py` rewrites them. Commands below are templates for CLI routing. Add `< /dev/null` so neither CLI waits for input. The **In the apps** line under each setup is for app routing, when the owner works in the Claude or ChatGPT app without Grok Bot or Muse.

## Claude + ChatGPT (default)
For owners who pay for both. Each job goes to the model that's best at it, and the work is spread across two plans.

<!-- models:setup name=claude-chatgpt -->
| Slot | Model | Tool | Run it |
|---|---|---|---|
| head-chef | Claude Opus 5.5, effort high (`claude-opus-5-5`) | Claude Code | `claude -p --model claude-opus-5-5 --effort high "<task>" < /dev/null` |
| line-cook | GPT-6.1 Sol, effort high (`gpt-6.1-sol`) | Codex | `codex exec -m gpt-6.1-sol -c model_reasoning_effort=high --skip-git-repo-check "<task>" < /dev/null` |

**In the apps:** plan in the Claude app on Claude Opus 5.5; execute in the ChatGPT app on GPT-6.1 Sol. The hand-off moves the plan from one app to the other.
<!-- /models -->

## ChatGPT only
For owners who only pay for ChatGPT. Both slots run through Codex; skip Claude Code.

<!-- models:setup name=chatgpt-only -->
| Slot | Model | Tool | Run it |
|---|---|---|---|
| head-chef | GPT-6 Astra, effort high (`gpt-6-astra`) | Codex | `codex exec -m gpt-6-astra -c model_reasoning_effort=high --skip-git-repo-check "<task>" < /dev/null` |
| line-cook | GPT-6.1 Sol, effort high (`gpt-6.1-sol`) | Codex | `codex exec -m gpt-6.1-sol -c model_reasoning_effort=high --skip-git-repo-check "<task>" < /dev/null` |

**In the apps:** both in the ChatGPT app. Plan on GPT-6 Astra and execute on GPT-6.1 Sol, each in its own new chat.
<!-- /models -->

## Claude only
For owners who only pay for Claude. Both slots run through Claude Code; skip Codex.

<!-- models:setup name=claude-only -->
| Slot | Model | Tool | Run it |
|---|---|---|---|
| head-chef | Claude Opus 5.5, effort high (`claude-opus-5-5`) | Claude Code | `claude -p --model claude-opus-5-5 --effort high "<task>" < /dev/null` |
| line-cook | Claude Sonnet 5.5, effort high (`claude-sonnet-5-5`) | Claude Code | `claude -p --model claude-sonnet-5-5 --effort high "<task>" < /dev/null` |

**In the apps:** both in the Claude app. Plan on Claude Opus 5.5 and execute on Claude Sonnet 5.5, each in its own new chat.
<!-- /models -->

**In the Claude desktop app's Code tab:** set the model to the head-chef (type `/model <head-chef model ID>`, or set it as `"model"` in `~/.claude/settings.json`), and hand line-cook jobs to a subagent on the line-cook's model and effort from guava-stack settings (Claude Code's subagents take both). It works the same way as every other setup, so a swap in guava-stack settings applies at the next hand-off.

Both slots share one Claude plan, so it hits usage limits sooner. There's no non-Claude line-cook for unattended or always-on jobs: those need an Anthropic API key or get done by hand (see the terms step in the skill).

## Google only
For owners who pay for Google AI Pro or Ultra. Both slots run through Google's Antigravity CLI (`agy`), which replaced Gemini CLI for Google AI plans; skip Claude Code and Codex.

<!-- models:setup name=google-only -->
| Slot | Model | Tool | Run it |
|---|---|---|---|
| head-chef | Gemini 4 Argon, effort high (`gemini-4-argon`) | Antigravity CLI | `agy -p --model gemini-4-argon-high "<task>" < /dev/null` |
| line-cook | Gemini 3.8 Flash, effort high (`gemini-3.8-flash`) | Antigravity CLI | `agy -p --model gemini-3.8-flash-high "<task>" < /dev/null` |

**In the apps:** both in the Gemini app. Plan on Gemini 4 Argon and execute on Gemini 3.8 Flash, each in its own new chat.
<!-- /models -->

Antigravity CLI names each model with its effort on the end, such as `gemini-4-argon-high`; run `agy models` to see the names the owner's plan offers. Gemini 4 Argon needs Google AI Pro or Ultra, and Gemini 3.8 Flash is on every plan. Both slots share one plan's quota, which refreshes every five hours up to a weekly limit, so long line-cook jobs use it up fastest; `/usage` in `agy` shows what's left.

The Claude desktop app's Code tab isn't an option here, since it needs a Claude plan: route from Grok Bot or Muse. App routing in the Gemini app works the same way once the hub is connected there, but guava-stack has no Gemini app guide yet, so set up CLI routing.

## Your own picks
Owners can put any model in either slot that a tool in their setup can run: any Claude model through Claude Code, any OpenAI model through Codex, any Gemini model through Antigravity CLI. Use the same commands as above with that model's ID and effort, and mark it "(own pick)" in guava-stack settings so "check for newer models" leaves it alone. For app routing, pick a model the app offers.

## Local models (*coming soon*)
Support for models that run on the owner's own hardware (through tools like Ollama or LM Studio), so nothing leaves the computer, is coming soon. It pairs with a local Markdown or Obsidian hub for clients that need to stay offline. Until then, say so plainly, and set up the closest of the four setups above if the owner still wants routing.
