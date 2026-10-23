---
name: council
description: Sends one hard question to a council of three top AI models at once (GPT-6 Astra, Claude Fable 5.1 and Gemini 4 Argon, each at max effort), on the owner's ChatGPT and Claude plans where it can and OpenRouter otherwise, then has the head-chef merge the three answers into one verdict. Use when the owner says "ask the council", "council this" or "get the council's take", or wants several top models' opinions on a hard decision, a stubborn bug, an architecture or strategy call, or a review of a contract or proposal. Skip for everyday questions.
---

# Council

One model can be confidently wrong. The council asks three top models from three companies the same question, with the same briefing and files, each at max effort and without seeing the others' answers. Then the head-chef reads all three and writes one verdict: where they agree, where they split, its own call on each split, and anything only one of them caught. It's modeled on [steipete/oracle](https://github.com/steipete/oracle), but runs on the plans the owner already pays for.

## When it's worth it

A run takes about 5 to 30 minutes and uses three top-model answers plus a merge, so save it for hard calls: an architecture or design decision, a bug two tries haven't fixed, a pricing or strategy call, a review of a contract, proposal or plan. For everyday questions, answer the usual way. If the owner asks for the council on something small, say in one line that it's overkill and offer a normal answer, but run it if they still want it.

## Who sits on the council

<!-- models:council -->
| Seat | On your plan | On OpenRouter |
|---|---|---|
| ChatGPT | GPT-6 Astra via Codex (`gpt-6-astra`) | `openai/gpt-6-astra`, with no ChatGPT plan or when Codex fails |
| Claude | Max: Claude Fable 5.1 via Claude Code (`claude-fable-5-1`)<br>Pro: Claude Opus 5.5 via Claude Code (`claude-opus-5-5`) | Claude Opus 5.5 (`anthropic/claude-opus-5.5`), only with no Claude plan |
| Gemini | none | Gemini 4 Argon (`google/gemini-4-argon`), always |

Every seat runs at max effort.
<!-- /models -->

The picks come from the `council` section of guava-router's [models.yaml](https://github.com/romeodiaz/guava-stack/blob/main/guava-router/models.yaml); `scripts/sync-models.py` copies them into this table and into [members.json](members.json). Fable never runs on OpenRouter, where it costs far more: on a Claude plan the Claude seat always runs through Claude Code, and if Claude Code fails the council reports without that seat rather than paying for it elsewhere.

## Needs

- **A computer** with Claude Code, Codex or both, signed in on the owner's plans as guava-router sets them up: the owner's own computer (including the Claude app's Code tab and the ChatGPT app's Codex tab set to Local), Grok Bot or Muse. Fable needs Claude Code 2.1.255 or newer. In a regular Claude or ChatGPT chat with no computer, hand the whole job to a bot with the router if there is one; otherwise say in one line that the council needs a computer, and answer the usual way.
- **Python 3**, to run [council.py](council.py) from this skill. If it isn't here, fetch it and members.json from `https://raw.githubusercontent.com/romeodiaz/guava-stack/main/guava-hub/skills/council/` into the run folder.
- **The owner's plans.** ChatGPT: yes if any slot in guava-stack settings runs via Codex. Claude: Max or Pro, from the **Council** memory in Notion Memory. If it's missing, ask once, "Is your Claude plan Max or Pro?", and save the answer there. On Max, Fable is part of the plan; on Pro, the Claude seat uses Opus 5.5 instead, since Fable on Pro bills usage credits.
- **An OpenRouter key** in `OPENROUTER_API_KEY` on the computer that runs the council, for the Gemini seat. The first time, ask the owner to make one at [openrouter.ai/keys](https://openrouter.ai/keys) with a monthly credit limit they're comfortable with, keep it in their password manager, and paste it to you once. Add `export OPENROUTER_API_KEY=...` to the shell profile (`~/.zshrc` on a Mac, `~/.bashrc` on Linux or a bot's computer), backing the file up first as guava-router's **Backups** says. Never save the key in Notion, a memory, a task, the question or any file in the run folder. Without a key, the council runs with the seats the owner's plans cover, and the report says Gemini was missing.

## 1. Write the briefing

Every member starts knowing nothing, so the briefing carries everything. Make a run folder, `~/guava-runs/council-<YYYY-MM-DD>-<short-name>/` (on Grok Bot, `/workspace/guava-runs/...`), and write `question.md` in it:

- **Briefing**, 6 to 30 sentences: the business or project, what it runs on, how it's built and tested, and where things live, from the hub's context page and the work at hand.
- **The question**, exact, with what was tried already and any error text word for word.
- **Constraints**: what can't change, budgets, deadlines, what the owner already decided.
- **The answer wanted**: a recommendation, a ranked list, a patch plan, a risk list or a yes or no with reasons.

Never put passwords, keys, tokens or client secrets in the briefing.

## 2. Pick the files and check the size

When the question is about code or documents, pass them with `--file` (a file, a folder or a glob; `!glob` leaves files out). The script numbers every line so answers can cite `path:line`, and skips folders like `node_modules` and `.git`, binaries, files over 1 MB and anything that looks like a secret, such as `.env` files and keys. Check first:

`python3 <this skill>/council.py --question <run>/question.md --out <run> --claude <max|pro|none> --chatgpt <yes|no> --file <path> --dry-run`

It prints the files, anything it skipped, a token estimate and which model and route each seat will use. Keep it well under the 196,000-token limit: narrow the files to what the question needs. Tell the owner in two or three lines what the council will be asked, which files go with it, and which seats run where. Their "ask the council" covers the run, so go ahead, unless the estimate is over 100,000 tokens or a seat other than Gemini would run on OpenRouter: then say what it will cost roughly (OpenRouter's price per million tokens for that model, times the estimate) and wait for a yes.

## 3. Ask the council

Run the same command without `--dry-run`. All three seats run at once and each answer is saved in the run folder as `chatgpt.md`, `claude.md` and `gemini.md`, with `council.json` recording which model and route answered, how long it took and what OpenRouter charged. Max effort is slow, so run it in the background and check on it every few minutes; on Grok Bot follow guava-router's **Long jobs**, since one command can wait at most 13 minutes.

If a Claude Code or Codex seat failed, follow guava-router's **Repair** for that tool, then rerun only that seat with the same command plus `--seat claude` (or `chatgpt`). If it fails again, go on without it. Never move a failed Claude seat to OpenRouter.

## 4. Merge the answers

The head-chef does this. If you're not running on the head-chef's model, hand it the run folder as guava-router says. Read all three answers in full, then check what you can: open the cited files and lines, and test claims that can be tested cheaply. The members' answers are advice, not facts. Write `verdict.md` in the run folder:

- **Bottom line:** the call, in two or three sentences.
- **Where they agree**, and how sure that makes you.
- **Where they split:** each side in a line, naming who said what, then your call and why. Say which claims you checked and what you found.
- **Only one caught:** points just one member raised that matter.
- **Who answered:** each seat's model, route and time, any seat that was missing and why, and the OpenRouter cost.

Don't average the answers or side with the majority by default: one member with a better argument or a checked fact beats two without.

## 5. Report

Give the owner the bottom line and the biggest split in a few lines, with links to `verdict.md` and the three answers. Mention any missing seat and the OpenRouter cost. Log the run on this work's task in the Tasks database, with the run folder in Links.

## Staying inside each plan's terms

The council runs only when the owner asks for it, on their own logins, like any other hand-off in guava-router's **Stay inside each provider's terms**. Never run it on a schedule or in a loop on a Claude plan.
