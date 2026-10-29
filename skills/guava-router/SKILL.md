---
name: guava-router
description: Hands each job from Claude Code or Codex to the owner's head-chef or line-cook, the two models named in the guava-stack settings of their Agent Operating Guide in Notion, with the head-chef for thinking work and the line-cook for doing work. Use on every task in Claude Code or Codex once guava-stack settings names both slots, and when the owner says "set up the router" or wants a different model in a slot.
---

# guava-router

Two slots, kept in the **guava-stack settings** section of the owner's Agent Operating Guide, so the owner swaps a model by editing one line. The owner can add a third line, `computer-use`, such as `GPT-6.1 Sol (Low) via Codex`, to run computer use on its own model and effort:

```
## guava-stack settings
### guava-router
head-chef
- Claude Opus 5.5 (High) via Claude Code
  - Orchestration, research, planning, brainstorming, copywriting, validation, review, verification, and fuzzy and hard problems. On important work, checks the line-cook's result before it's called done.
line-cook
- GPT-6.1 Sol (High) via Codex
  - Bulk execution, coding, computer use, sub-agent tasks, worker threads and long-running jobs.
```

## Route work
Routing runs only in Claude Code or Codex on the owner's computer. In the desktop apps' chat, do the work yourself.
- Re-read the model lines right before each hand-off. Quick replies and lookups stay with you.
- If this session already runs on that slot's model at its effort, do the work yourself. Otherwise hand it off with the slot's tool, model ID and effort, passing both, since each tool otherwise falls back to its own default. Run it in the folder it should work in, and give it only the access the job needs:
  - Claude Code: `claude -p --model <ID> --effort <effort> --permission-mode acceptEdits "<task>" < /dev/null` for work that writes files, or `--permission-mode plan` for reading and reviewing. Add any commands the job must run with `--allowedTools`, such as `--allowedTools "Bash(npm test:*)"`.
  - Codex: `codex exec -m <ID> -c model_reasoning_effort=<effort> -s workspace-write --skip-git-repo-check "<task>" < /dev/null` for work that writes files in this folder, or `-s read-only` for reading and reviewing.

  Without `< /dev/null`, either tool can wait for input and hang.
- Give each hand-off the goal, what's done, what to check and where to write the result. When the job reads Notion databases, tell it to use `notion-fetch` or a saved view (`notion-query-data-sources` in view mode), not SQL: on Free and Plus plans Notion meters SQL per workspace, and views have no limit.
- On important work, the head-chef checks the line-cook's result before it's called done.
- Computer use goes to the computer-use line when guava-stack settings has one, and otherwise to the line-cook: browser tools first, in the browser where the owner is already signed in.
- If a hand-off fails, find out why first: the tool's error, whether it's signed in (`claude auth status`, `codex login status`) and whether it had the access the job needed. Fix what the evidence points to and retry once. If it still fails, do the task yourself and say so. Updating a tool changes software on the owner's computer, so show the command (`claude update`, or `npm i -g @openai/codex@latest` for an npm install) and run it only on a yes.
- When a skill says how it runs, follow the skill and route only the work it leaves open.

## Set it up
1. Check, without asking, that `claude` and `codex` are installed and signed in on the owner's plans. Point to the install steps at https://code.claude.com/docs or https://developers.openai.com/codex for a missing one.
2. Pick the slots:
   - Claude and ChatGPT plans: Claude Opus 5.5 (`claude-opus-5-5`) via Claude Code, and GPT-6.1 Sol (`gpt-6.1-sol`) via Codex, both at High.
   - Claude only: Claude Sonnet 5.5 (`claude-sonnet-5-5`) via Claude Code as line-cook.
   - ChatGPT only: GPT-6 Astra (`gpt-6-astra`) via Codex as head-chef.

   The owner can pick any Claude model through Claude Code or OpenAI model through Codex, at Low, Medium, High, xhigh or Max.
3. Test each slot twice in a new empty folder: a tiny prompt, such as `claude -p --model claude-opus-5-5 --effort high "Reply OK" < /dev/null`, then a hand-off with the write access above that creates a file named `ok.txt`, which you check for and then delete. An old tool rejects new models, so if a model is rejected, check the tool's version and offer the update as above.
4. On a yes, add the guava-router part of the section above to the end of the Agent Operating Guide, under a `## guava-stack settings` heading (adding the heading if it isn't there yet), with the slots that passed. Keep Notion's own sections as they are.
