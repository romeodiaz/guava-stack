---
name: oracle-council
description: Sends one hard question to a council of three top AI models at once (GPT-6 Astra and Claude Fable 5.1 at max effort, and Gemini 4 Argon at High, the most it offers), on the owner's Claude and ChatGPT subscriptions where available, and OpenRouter (signed in through the browser and billed per use) for Gemini 4 Argon and any seat those don't cover, then merges the three answers into one verdict, reading them unlabeled. In a chat app with no terminal, it runs by hand, with the owner pasting one briefing into two other companies' AI apps. Works on its own, with or without the rest of guava-stack. Use when the owner says "ask the council", "ask the oracle council", "council this" or "get the council's take", or wants several top models' opinions on a hard decision, a stubborn bug, an architecture or strategy call, or a review of a contract or proposal. Skip for everyday questions.
---

# Oracle council

One model can be confidently wrong. The council asks three top models from three companies the same question, with the same briefing and files, each at its highest effort, able to search the web and without seeing the others' answers. Then the strongest model on hand (the head-chef, with guava-router) reads all three and writes one verdict: where they agree, where they split, its own call on each split, and anything only one of them caught. It's modeled on [steipete/oracle](https://github.com/steipete/oracle), but uses the plans the owner already pays for, with Gemini 4 Argon always on OpenRouter, billed per use, and checks for itself that each one is signed in.

## When it's worth it

A run takes about 5 to 30 minutes and uses three top-model answers plus a merge, so save it for hard calls: an architecture or design decision, a bug two tries haven't fixed, a pricing or strategy call, a review of a contract, proposal or plan. For everyday questions, answer the usual way. If the owner asks for the council on something small, say in one line that it's overkill and offer a normal answer, but run it if they still want it.

## Who sits on the council

| Seat | On your plan | Billed per use |
|---|---|---|
| ChatGPT | GPT-6 Astra via Codex (`gpt-6-astra`), max effort | OpenRouter `openai/gpt-6-astra`, with no ChatGPT plan, or rerun there with the owner's yes when Codex fails |
| Claude | Max: Claude Fable 5.1 via Claude Code (`claude-fable-5-1`)<br>Pro: Claude Opus 5.5 via Claude Code (`claude-opus-5-5`)<br>Max effort | OpenRouter Claude Opus 5.5 (`anthropic/claude-opus-5.5`), only with no Claude plan |
| Gemini | — | Gemini 4 Argon on OpenRouter only (`google/gemini-4-argon`), at High, the most it offers |

The models and efforts live in `members.json`. Every OpenRouter request uses only providers that don't store or train on what they're sent. Fable never runs on OpenRouter, where it costs far more: on a Claude plan the Claude seat always runs through Claude Code, and if Claude Code fails the council reports without that seat rather than paying for it elsewhere.

## Set up

This skill works on its own. guava-stack's Notion setup and guava-router make a few steps smoother where noted, but neither is needed.

- **A computer with a terminal**: any AI agent that can run commands on the owner's computer with Python 3, such as Claude Code or Codex, including the Claude app's Code tab and the ChatGPT app's Codex tab set to Local. The plan seats need Claude Code or Codex installed; with OpenRouter alone, neither is needed. In a chat with no terminal, follow **Council by hand** below instead.
- **The runner**: `oracle-council.py` and `members.json`, next to this file. If they aren't here, fetch both from `https://raw.githubusercontent.com/romeodiaz/guava-stack/main/skills/oracle-council/` into the run folder.

The first time, and whenever a seat fails, run `python3 <this skill>/oracle-council.py --check`. It shows whether Claude Code and Codex are installed and signed in on a plan, whether there's an OpenRouter key, the flags to pass, and a fix for each gap. Then ask once which subscriptions the owner has: Claude (Max or Pro) and ChatGPT. Use their subscriptions for the first two seats, in this order, and OpenRouter for Gemini 4 Argon and any seat neither plan covers. OpenRouter is billed per use on every council run. Walk through them one at a time, then check again:

1. **Claude subscription → the Claude seat.** `--check` shows the plan Claude Code is signed in on (`subscriptionType`); if it doesn't, ask once, "Is your Claude plan Max or Pro, or do you not have one?" On Max the seat runs Fable 5.1, which needs a recent Claude Code (`claude update`); on Pro it runs Opus 5.5 instead, since Fable on Pro bills usage credits. If Claude Code isn't installed, point to the install steps at https://code.claude.com/docs. If it isn't signed in, have the owner run `claude auth login` with the account that has the plan. With no Claude plan, pass `--claude none`.
2. **ChatGPT subscription → the ChatGPT seat.** If Codex isn't signed in with it, point to the install steps at https://developers.openai.com/codex if it's missing, and have the owner run `codex login` and choose Sign in with ChatGPT. Pass `--chatgpt yes` once `--check` shows `signed_in_with_chatgpt`. Without a plan, pass `--chatgpt no`.
3. **OpenRouter: Gemini 4 Argon, plus every seat no subscription covers.** Billed per use by OpenRouter. The Gemini seat costs a few cents for a short question and about $0.20 with a few files and web search (October 2026; Gemini 4 Argon's price doubles on December 1, 2026). It runs the Claude seat (Opus 5.5) with no Claude plan, the ChatGPT seat with no ChatGPT plan, and always the Gemini 4 Argon seat. An owner with no plans at all passes `--claude none --chatgpt no` and runs all three seats there, at higher prices per million tokens for the other two (GPT-6 Astra $10 in and $50 out, Opus 5.5 $4 and $20, against Argon's $2 and $10), so step 2's cost check matters. Run `python3 <this skill>/oracle-council.py --login`: it opens OpenRouter in the owner's browser, they approve, and the key OpenRouter makes is saved in `~/.config/guava-stack/openrouter-key`, readable only by them. Have them add credits at [openrouter.ai/settings/credits](https://openrouter.ai/settings/credits) if the account has none, and suggest a monthly credit limit on the key at [openrouter.ai/settings/keys](https://openrouter.ai/settings/keys). On a computer without a browser, run `--login --headless`: it prints a link to open on any device, and the owner types the code the page shows into the terminal.

**Keys never pass through the chat.** Never ask the owner to paste a key to you, and never save one in notes, memory, a task, the question or any file in the run folder. An owner who already has an OpenRouter key can set `OPENROUTER_API_KEY` themselves instead of signing in; the council reads that first, then the saved key. A seat with no way to run is left out, and the report says so.

**Remember the answers** (the Claude plan, whether there's a ChatGPT plan, and that OpenRouter is signed in) so the owner isn't asked again: in an **Oracle council** memory in Notion Memory when Notion is set up, otherwise in your own memory if you have one.

## 1. Write the briefing

Every member starts knowing nothing, so the briefing carries everything. Make a run folder, `~/guava-runs/oracle-council-<YYYY-MM-DD>-<short-name>/`, and write `question.md` in it:

- **Briefing**, 6 to 30 sentences: the business or project, what it runs on, how it's built and tested, and where things live, from what you know about the work, and the guava-hub context page if there is one.
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

Run the same command without `--dry-run`. All three seats run at once and each answer is saved in the run folder as `chatgpt.md`, `claude.md` and `gemini.md`, with `council.json` recording which model and route answered, how long it took and what OpenRouter charged. The script also saves the answers unlabeled, in random order, as `blind/A.md`, `blind/B.md` and `blind/C.md`, and keeps which is which in `blind/key.json`. Max effort is slow, so run it in the background (`nohup ... &`) and check on it every few minutes.

If a seat failed, run `--check`, fix what it shows, then rerun only that seat with the same command plus `--seat claude`, `--seat chatgpt` or `--seat gemini`. If it fails again, go on without it. A failed ChatGPT seat can rerun on OpenRouter with `--seat chatgpt --chatgpt no`, billed per use, only after the owner says yes to its rough cost. Never move a failed Claude seat to OpenRouter.

## 4. Merge the answers

Merge them yourself, on the strongest model you have; with guava-router, that's the head-chef, so hand it the run folder if you're not running on it. Merge blind, so no answer gets extra weight for the company behind it: read `blind/A.md`, `B.md` and `C.md` in full, and don't open `chatgpt.md`, `claude.md`, `gemini.md`, `council.json` or `blind/key.json` until the verdict is written. Then check what you can: open the cited files and lines and the key web pages, and test claims that can be tested cheaply. The members' answers are advice, not facts. Write `verdict.md` in the run folder:

- **Bottom line:** the call, in two or three sentences.
- **Where they agree**, and how sure that makes you.
- **Where they split:** each side in a line, naming which answer (A, B or C) said what, then your call and why. Say which claims you checked and what you found.
- **Only one caught:** points just one member raised that matter.
- **Who answered:** written last, after you open `blind/key.json` and `council.json`: which model wrote A, B and C, each one's route and time, any seat that was missing and why, and the OpenRouter cost.

Don't average the answers or side with the majority by default: one member with a better argument or a checked fact beats two without.

## 5. Report

Give the owner the bottom line and the biggest split in a few lines, with links to `verdict.md` and the three answers. Mention any missing seat and the OpenRouter cost. When this work has a task in the owner's Tasks database, add the run folder's path to it.

## Council by hand
Use this in a chat app with no terminal, such as the Claude or ChatGPT app's regular chat. You answer as one member, and the owner brings in two more from other companies' AI apps they use, each in its own app, so the council still spans three companies.
1. **Write the briefing** as step 1 says, as one block the owner can copy. With no `--file`, paste in only the parts of any document the question needs, and leave out a client's confidential details unless the owner's company approves all three apps.
2. **Answer it yourself first**, in full, before you see any other answer, and keep it out of the chat for now so it doesn't shape the owner's next steps.
3. **Ask the owner** to paste the briefing into a new chat in two AI apps from other companies than yours (for example ChatGPT, Gemini or Grok, whichever two they have), each on its best model with its deepest thinking setting and web search on, then paste each full answer back.
4. **Merge** as step 4 says, calling the answers A, B and C. Since you wrote one of them, you can't merge blind: say which one is yours, and hold it to the strictest check.
5. **Report** as step 5 says, in the chat. Nothing is billed per use; each app runs on the owner's own plan.

## Staying inside each plan's terms

The council runs only when the owner asks for it, on their own logins, one question at a time. Never run it on a schedule or in a loop, since the Claude and ChatGPT plans are for a person's own use. Never share the owner's sign-ins or keys with anyone else.
