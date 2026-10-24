# ChatGPT adapter: ChatGPT desktop app and Codex

- For owners on a ChatGPT plan (Plus or higher works best; if Notion won't connect on Free, setup needs a paid plan). Daily chat happens in the **ChatGPT desktop app**, which syncs with chatgpt.com on the web and the ChatGPT app on their phone. **Codex** runs on their computer for the skills that run programs, and becomes the line-cook's tool once they add a bot. Setup starts in the desktop app's chat, with nothing to install for that part. Do the setup clicks on a computer; the phone app lays settings out differently.
- **Get the app:** if the owner only uses chatgpt.com in a browser, have them install the desktop app from https://chatgpt.com/download, sign in with the account that has their plan, and paste the Start here line there.
- **Before you start:** setup reads these steps from GitHub, so web search must be on for this chat. If you can't open github.com/romeodiaz/guava-stack, ask the owner to turn it on and try again.
- **Show the screenshots:** for each click below, give the owner the link and the screenshot, so they see exactly where to click.
- **Connect your hub:** "Open https://chatgpt.com/plugins?search=notion and click **+** next to Notion." "Sign in to Notion and approve access to the workspace you'll use for your guava-hub." Then start a new chat if Notion doesn't show up in this one.

  ![ChatGPT Plugins with Notion and its + button](https://raw.githubusercontent.com/romeodiaz/guava-stack/main/assets/setup/chatgpt-plugins.png)
- **Add the standing instructions:** "Open https://chatgpt.com/settings/personalization and, under **Custom instructions**, click **ChatGPT**." "Paste these lines at the end of the instructions box, then save." "Now click **Codex** in the same list and paste the same lines there too, then save, so Codex follows them as well." "In both, add to what's there; never replace or delete anything." Give them the short version from setup step 2. Uninstalling removes the lines from both rows.

  ![ChatGPT Personalization with Custom instructions, ChatGPT](https://raw.githubusercontent.com/romeodiaz/guava-stack/main/assets/setup/chatgpt-custom-instructions.png)
- **Connect your computer** (setup step 6): "In the ChatGPT desktop app, open the **Codex** tab, set it to **Local**, pick your home folder, and paste: `Connect Codex to my guava-hub, following Connect your computer in github.com/romeodiaz/guava-stack`." The Codex tab is Codex running on their computer, so it does these itself, with one yes for the plan:
  - Check first, without asking: `codex --version` in a terminal, `codex plugin list` and `codex mcp list`. Skip whatever is already there.
  - Put the `codex` command in their terminal too, if it's missing: `npm i -g @openai/codex`, or `brew install --cask codex` on a Mac without Node. Check `codex login status`, and if it isn't signed in, run `codex login` and choose Sign in with ChatGPT, on the same account.
  - Install the guava-hub plugin, whose start-up hook gives every Codex session the standing instructions: `codex plugin marketplace add romeodiaz/guava-stack`, then `codex plugin add guava-hub@guava`, and the owner trusts its hooks in a new Codex chat.
  - Notion, unless `codex mcp list` already shows it: `codex mcp add notion --url https://mcp.notion.com/mcp`, then `codex mcp login notion`, and the owner approves Notion's sign-in page.
  - Check it in a new Codex chat: "What's in my guava-hub?" passes if it answers from the hub.
- ChatGPT's chat keeps no skill files: keep skills in the hub and read the matching one from there when a task needs it. Codex reads them from the hub too, and runs the ones that need a computer.
- The Model Router and last30days-research come with adding Grok Bot or Muse (**Add a bot** in the setup skill).
- **Workflow review:** make the report as a downloadable `.html` file the owner saves, never a shared link.
