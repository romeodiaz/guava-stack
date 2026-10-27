---
name: oracle-council
description: Sends one hard question to a council of three top AI models at once (GPT-6 Astra, Claude Fable 5.1 and Gemini 4 Argon, each at max effort), on the owner's Claude and ChatGPT subscriptions where available, and OpenRouter (signed in through the browser and billed per use) for Gemini 4 Argon and any seat those don't cover, then merges the three answers into one verdict. Works on its own, with or without the rest of guava-stack. Use when the owner says "ask the council", "ask the oracle council", "council this" or "get the council's take", or wants several top models' opinions on a hard decision, a stubborn bug, an architecture or strategy call, or a review of a contract or proposal. Skip for everyday questions.
---

# Oracle council

One model can be confidently wrong. The council asks three top models from three companies the same question, with the same briefing and files, each at max effort, able to search the web and without seeing the others' answers. Then the strongest model on hand (the head-chef, with guava-router) reads all three and writes one verdict: where they agree, where they split, its own call on each split, and anything only one of them caught. It's modeled on [steipete/oracle](https://github.com/steipete/oracle), but uses the plans the owner already pays for, with Gemini 4 Argon always on OpenRouter, billed per use, and checks for itself that each one is signed in.

## When it's worth it

A run takes about 5 to 30 minutes and uses three top-model answers plus a merge, so save it for hard calls: an architecture or design decision, a bug two tries haven't fixed, a pricing or strategy call, a review of a contract, proposal or plan. For everyday questions, answer the usual way. If the owner asks for the council on something small, say in one line that it's overkill and offer a normal answer, but run it if they still want it.

## Who sits on the council

<!-- models:oracle-council -->
| Seat | On your plan | Billed per use |
|---|---|---|
| ChatGPT | GPT-6 Astra via Codex (`gpt-6-astra`) | OpenRouter `openai/gpt-6-astra`, with no ChatGPT plan or when Codex fails |
| Claude | Max: Claude Fable 5.1 via Claude Code (`claude-fable-5-1`)<br>Pro: Claude Opus 5.5 via Claude Code (`claude-opus-5-5`) | OpenRouter Claude Opus 5.5 (`anthropic/claude-opus-5.5`), only with no Claude plan |
| Gemini | — | Gemini 4 Argon on OpenRouter only (`google/gemini-4-argon`) |

Every seat runs at max effort.
<!-- /models -->

The picks come from the `oracle_council` section of guava-router's [models.yaml](https://github.com/romeodiaz/guava-stack/blob/main/guava-router/models.yaml); `scripts/sync-models.py` copies them into this table and into [members.json](members.json). Fable never runs on OpenRouter, where it costs far more: on a Claude plan the Claude seat always runs through Claude Code, and if Claude Code fails the council reports without that seat rather than paying for it elsewhere.

## Set up

This skill works on its own. guava-hub and guava-router make a few steps smoother where noted, but neither is needed.

- **A computer with a terminal**: the owner's own computer (in Claude Code, Codex or Pi, including the Claude app's Code tab, the ChatGPT app's Codex tab set to Local, and the OpenCode desktop app) or a bot's computer, with Python 3. In a regular Claude or ChatGPT chat with no terminal, say in one line that the council needs one and answer the usual way; with guava-router and a bot, hand the whole job to the bot instead.
- **The runner**: [oracle-council.py](oracle-council.py) and [members.json](members.json), next to this file. If they aren't here, fetch both from `https://raw.githubusercontent.com/romeodiaz/guava-stack/main/guava-hub/skills/oracle-council/` into the run folder.

The first time, and whenever a seat fails, run `python3 <this skill>/oracle-council.py --check`. It shows whether Claude Code and Codex are installed and signed in on a plan, whether Pi is signed in to OpenRouter, which API keys are set, the flags to pass, and a fix for each gap. Then ask once which subscriptions the owner has: Claude (Max or Pro) and ChatGPT. Use their subscriptions for the first two seats, in this order, and OpenRouter for Gemini 4 Argon and any seat neither plan covers. OpenRouter is billed per use on every council run. Walk through them one at a time, then check again:

1. **Claude subscription → the Claude seat.** `--check` shows the plan Claude Code is signed in on (`subscriptionType`); if it doesn't, ask once, "Is your Claude plan Max or Pro, or do you not have one?" On Max the seat runs Fable 5.1, which needs Claude Code 2.1.255 or newer (`claude update`); on Pro it runs Opus 5.5 instead, since Fable on Pro bills usage credits. If Claude Code isn't installed, install it with `npm i -g @anthropic-ai/claude-code`. If it isn't signed in, have the owner run `claude auth login` with the account that has the plan. With no Claude plan, pass `--claude none`.
2. **ChatGPT subscription → the ChatGPT seat.** If Codex isn't signed in with it, install Codex if needed (`npm i -g @openai/codex`) and have them run `codex login` and choose Sign in with ChatGPT. Pass `--chatgpt yes` once `--check` shows `signed_in_with_chatgpt`. Without a plan, pass `--chatgpt no`.
3. **OpenRouter: Gemini 4 Argon, plus every seat no subscription covers.** Billed per use by OpenRouter, about $0.02 for a typical question. It runs the Claude seat (Opus 5.5) with no Claude plan, the ChatGPT seat with no ChatGPT plan and as its backup when Codex fails, and always the Gemini 4 Argon seat. The sign-in runs through the **Pi** coding agent, which keeps the key OpenRouter makes for it, and the council reads that key from Pi. On OpenRouter alone, where guava-stack setup or guava-router signed Pi in, this is already done: `--check` shows `openrouter_sign_in` signed in. Otherwise install Pi if `--check` says it's missing (`curl -fsSL https://pi.dev/install.sh | sh`), then have the owner run `pi`, type `/login openrouter`, choose **Sign in with OpenRouter** and approve in the browser, adding credits at [openrouter.ai/settings/credits](https://openrouter.ai/settings/credits) if the account has none. Suggest a credit limit on the key at [openrouter.ai/settings/keys](https://openrouter.ai/settings/keys).

**Paste a key instead**, only if the owner would rather than sign in through the browser: an **OpenRouter key**, made at [openrouter.ai/settings/keys](https://openrouter.ai/settings/keys) with a monthly credit limit they're comfortable with (set `OPENROUTER_API_KEY`), pasted to you once.

**Keys** go in the shell profile as `export OPENROUTER_API_KEY=...` (`~/.zshrc` on a Mac, `~/.bashrc` on Linux or a bot's computer). Copy the profile to a dated `.bak` first. If the computer's safety check won't let you edit it, give the owner the one line to paste into Terminal. Never save a key in notes, memory, a task, the question or any file in the run folder. The council reads Pi's OpenRouter sign-in first, then `OPENROUTER_API_KEY`. Gemini 4 Argon runs only on OpenRouter, billed per use. A seat with no way to run is left out, and the report says so.

**Every sign-in is the browser one by default**: Claude Code, Codex and OpenRouter each sign in through the owner's browser, and a pasted key is only the backup. **On a computer without a browser**, such as a bot's: start `claude auth login`, `codex login --device-auth` or `pi` (then type `/login openrouter`) in tmux, send the owner the link it prints, and type in the code they paste back. For OpenRouter, the owner's browser lands on an error page at `127.0.0.1:<port>` after they approve, because that address belongs to the bot's computer: ask them to paste the whole address from the address bar back, and type that in.

**Remember the answers** (the Claude plan, whether there's a ChatGPT plan, and the OpenRouter sign-in for Gemini 4 Argon and any other seats it covers) so the owner isn't asked again. With guava-hub, save them in an **Oracle council** memory in Notion Memory; otherwise use your own memory if you have one.

## 1. Write the briefing

Every member starts knowing nothing, so the briefing carries everything. Make a run folder, `~/guava-runs/oracle-council-<YYYY-MM-DD>-<short-name>/` (on Grok Bot, `/workspace/guava-runs/...`), and write `question.md` in it:

- **Briefing**, 6 to 30 sentences: the business or project, what it runs on, how it's built and tested, and where things live, from what you know about the work, and the hub's context page if there is one.
- **The question**, exact, with what was tried already and any error text word for word.
- **Constraints**: what can't change, budgets, deadlines, what the owner already decided.
- **The answer wanted**: a recommendation, a ranked list, a patch plan, a risk list or a yes or no with reasons.

Never put passwords, keys, tokens or client secrets in the briefing.

## 2. Pick the files and check the size

When the question is about code or documents, pass them with `--file` (a file, a folder or a glob; `!glob` leaves files out). The script numbers every line so answers can cite `path:line`, and skips folders like `node_modules` and `.git`, binaries, files over 1 MB and anything that looks like a secret, such as `.env` files and keys. Check first:

`python3 <this skill>/oracle-council.py --question <run>/question.md --out <run> --claude <max|pro|none> --chatgpt <yes|no> --file <path> --dry-run`

The `--claude` and `--chatgpt` values are the ones from **Set up**.

Members search the web by default, so they can check current prices, releases and versions, and they cite the pages they used. They are told never to put private details into a search. Still, add `--no-web` whenever the briefing or files hold a client's confidential information or other people's personal details.

It prints the files, anything it skipped, a token estimate, whether web search is on and which model and route each seat will use. Keep it well under the 196,000-token limit: narrow the files to what the question needs. Tell the owner in two or three lines what the council will be asked, which files go with it, and which seats run where. Their "ask the council" covers the run, so go ahead, unless the estimate is over 100,000 tokens or a seat other than Gemini would run billed per use on OpenRouter: then say what it will cost roughly (the price per million tokens for that model, times the estimate) and wait for a yes.

## 3. Ask the council

Run the same command without `--dry-run`. All three seats run at once and each answer is saved in the run folder as `chatgpt.md`, `claude.md` and `gemini.md`, with `council.json` recording which model and route answered, how long it took and what OpenRouter charged. Max effort is slow, so run it in the background (`nohup ... &`) and check on it every few minutes; with guava-router on Grok Bot, follow its **Long jobs**.

If a seat failed, run `--check`, fix what it shows (with guava-router, its **Repair** covers Claude Code and Codex), then rerun only that seat with the same command plus `--seat claude`, `--seat chatgpt` or `--seat gemini`. If it fails again, go on without it. Never move a failed Claude seat to OpenRouter.

## 4. Merge the answers

Merge them yourself, on the strongest model you have; with guava-router, that's the head-chef, so hand it the run folder if you're not running on it. Read all three answers in full, then check what you can: open the cited files and lines and the key web pages, and test claims that can be tested cheaply. The members' answers are advice, not facts. Write `verdict.md` in the run folder:

- **Bottom line:** the call, in two or three sentences.
- **Where they agree**, and how sure that makes you.
- **Where they split:** each side in a line, naming who said what, then your call and why. Say which claims you checked and what you found.
- **Only one caught:** points just one member raised that matter.
- **Who answered:** each seat's model, route and time, any seat that was missing and why, and the OpenRouter cost.

Don't average the answers or side with the majority by default: one member with a better argument or a checked fact beats two without.

## 5. Report

Give the owner the bottom line and the biggest split in a few lines, with links to `verdict.md` and the three answers. Mention any missing seat and the OpenRouter cost. With guava-hub, when this work has a task in the Tasks database, add the run folder to its Links.

## Staying inside each plan's terms

The council runs only when the owner asks for it, on their own logins, one question at a time. Never run it on a schedule or in a loop, since the Claude and ChatGPT plans are for a person's own use. Never share the owner's sign-ins or keys with anyone else.
