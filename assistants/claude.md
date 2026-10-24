# Claude adapter: Claude desktop app and Claude Code

- For owners on a Claude plan (Pro or higher works best; Free can hit its message limit partway through setup). Daily chat happens in the **Claude desktop app**, which syncs with claude.ai on the web and the Claude app on their phone. **Claude Code** runs on their computer for the skills that run programs, and becomes the head-chef's tool once they add a bot. Setup starts in the desktop app's chat, with nothing to install for that part. Do the setup clicks on a computer; the phone app lays settings out differently.
- **Get the app:** if the owner only uses claude.ai in a browser, have them install the desktop app from https://claude.ai/download, sign in with the account that has their plan, and paste the Start here line there.
- **Before you start:** setup reads these steps from GitHub, so web search and fetch must be on (Settings, then Capabilities). If you can't open github.com/romeodiaz/guava-stack, ask the owner to turn it on and start a new chat.
- **Show the screenshots:** for each click below, give the owner the link and the screenshot, so they see exactly where to click.
- **Connect your hub:** "Open https://claude.ai/customize/connectors?q=notion and click **Connect** next to Notion." "Sign in to Notion and approve access to the workspace you'll use for your guava-hub." Then start a new chat if Notion's tools don't show up in this one. The same connection reaches the phone app, and Claude Code signed in with the same account loads it too.

  ![Claude Connectors with Notion and its Connect button](https://raw.githubusercontent.com/romeodiaz/guava-stack/main/assets/setup/claude-connectors.png)
- **Add the standing instructions:** "Open https://claude.ai/new#settings/account and find **Instructions for Claude**." "Paste these lines at the end of that box. Add to what's there; never replace or delete anything." Give them the short version from setup step 2.

  ![Claude Settings, Account, with the Instructions for Claude box](https://raw.githubusercontent.com/romeodiaz/guava-stack/main/assets/setup/claude-instructions.png)
- **Connect your computer** (setup step 6): "In the Claude desktop app, open the **Code** tab, set it to **Local**, pick your home folder, and paste: `Connect Claude Code to my guava-hub, following Connect your computer in github.com/romeodiaz/guava-stack`." The Code tab is Claude Code running on their computer, so it does these itself, with one yes for the plan:
  - Check first, without asking: `claude --version` in a terminal, `claude plugin list` and `claude mcp list`. Skip whatever is already there.
  - Put the `claude` command in their terminal too, if it's missing: `curl -fsSL https://claude.ai/install.sh | bash` on a Mac or Linux, `irm https://claude.ai/install.ps1 | iex` in PowerShell on Windows. Check `claude auth status`, and sign in with `claude auth login` on the same account if it isn't.
  - Install the guava-hub plugin, whose start-up hook gives every Claude Code session the standing instructions: `claude plugin marketplace add romeodiaz/guava-stack`, then `claude plugin install guava-hub@guava`. Then follow **Claude Code with the guava-hub plugin** in the Notion backend's file for the local copy.
  - Notion: `claude mcp list` should show the account's Notion connector (`claude.ai Notion`). Only if it doesn't, run `claude mcp add --transport http --scope user notion https://mcp.notion.com/mcp`, and have the owner type `/mcp` in Claude Code and approve Notion's sign-in page.
  - Check it in a new Code tab session: "What's in my guava-hub?" passes if it answers from the hub.
- The Claude app's chat keeps no skill files: keep skills in the hub and read the matching one from there when a task needs it. Claude Code reads them from the hub too, and runs the ones that need a computer.
- The Model Router and last30days-research come with adding Grok Bot or Muse (**Add a bot** in the setup skill).
- **Workflow review:** make the report as a downloadable `.html` file the owner saves, never a published or shared artifact.
