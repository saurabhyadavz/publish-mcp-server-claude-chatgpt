---
name: submit-to-chatgpt
description: Walk through publishing an MCP server as a ChatGPT plugin at platform.openai.com/plugins, step by step - testing it first as a custom MCP server in ChatGPT, uploading the ZIP, connecting the server, the domain-verification token at /.well-known/openai-apps-challenge, reviewer credentials, test cases, the demo video, reading the findings, and submitting. Use when someone is on the OpenAI plugins portal, asks where to find the domain token or the Submit button, gets a portal finding or "needs further review" message, needs a demo video for review, or wants to know if they can submit yet.
license: MIT
metadata:
  author: Saurabh Yadav
  version: "0.1.0"
---

# Submitting to the ChatGPT plugin directory

Two different sites: **chatgpt.com/plugins** is where you *use and test* plugins;
**platform.openai.com/plugins** is where you *submit* one. "Upload plugin archive" on chatgpt.com
only installs it for yourself. Full portal walkthrough: `references/portal.md`.

## 0. Test in ChatGPT first

chatgpt.com/plugins → **Add** → **Add custom MCP server** → name, the MCP URL (ending in `/mcp`,
nothing after it), OAuth → "I understand and want to continue" → **Create as a plugin** → sign in
on your page as the reviewer → **Install**. In a new chat type `@` and pick the plugin.

- After every deploy: open the plugin and click **Refresh** (ChatGPT caches tools and card HTML).
- Run every review test case. If ChatGPT answers without calling your tool, fix the server
  instructions (see `mcp-server-for-plugins`), not the prompt.
- Watch cards: "Opened <card>" with an empty box, or "timed out", means the card's start-up or
  data pickup is wrong (see `mcp-app-cards`).

## 1. Upload the ZIP

platform.openai.com/plugins → **Upload new or existing plugin** → the ZIP from `plugin-package`
(run its checker first). Fixing the package later: **Upload new version** on the plugin's page.
A deleted test plugin in ChatGPT doesn't touch the draft here.

## 2. Connect the server and verify the domain

MCPs tab → **Connect** (or Reconnect). The panel shows the URL, OAuth, the redirect URI
(`https://chatgpt.com/connector/oauth/<id>`) and, further down, the **domain-verification
token**. The status badge itself isn't clickable.

- Serve the token as plain text, nothing else, at
  `https://<your MCP host>/.well-known/openai-apps-challenge` (a route that reads it from an
  environment variable is simplest). A new draft can get a new token.
- Check it with `curl` before clicking Connect/Verify. Paste the real token, not a placeholder:
  the endpoint will happily serve the word "TOKEN".
- Sign in as the reviewer when asked. "Authorized" and a green domain badge mean this step is done.

## 3. Review information (five steps in a side panel)

1. **Countries and translations**: from the ZIP.
2. **Reviewer credentials**: username and password; Login URL = the sign-in page your OAuth flow
   opens; no tenant unless you have workspaces; notes with the exact steps a stranger follows.
   You type the password; never paste it anywhere an agent or a log can read it.
3. **Test cases** and 4. **Negative test cases**: from the ZIP (read-only here).
5. **Supporting content**: the demo video URL (unlisted YouTube or a Drive link anyone can view)
   and the release notes.

## 4. Read the findings, then submit

- "This new tool definition needs further review before it can be published": not an error. A
  person will look at that tool (often tools that serve news or third-party content). Be ready to
  say where the content comes from. Check the **Blocking** tab; if it's empty you can submit.
- Contrast, auth-settings or schema findings: fix the package and upload a new version.
- Click **Rescan** after a deploy so the checks run against the current server.
- **Submit for review** becomes usable when nothing says "incomplete". Publish only after approval.

## The demo video

Show exactly what reviewers will do: connect and sign in, all five test prompts in a fresh chat
with each card fully drawn, one refused prompt. Before recording, copy the password first and
close the password manager, notes and terminal. If they appear, cut them; the `video` tooling in
your agent or any editor can trim. A test case that visibly fails in the video invites a
rejection: re-record that clip instead of shipping it.
