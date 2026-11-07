---
name: plugin-package
description: Build the two store packages for one MCP server from a single listing source - the ChatGPT plugin ZIP (plugin.json with the com.openai interface, review test cases and publication blocks, mcp.json with the OAuth settings, an onboarding skill, icons) and Claude's plugin bundle and connector-portal text - and check the ZIP for the mistakes the OpenAI upload rejects. Use when preparing a ChatGPT plugin ZIP or a Claude plugin, when the OpenAI portal says "Invalid plugin package" or "Update the MCP authentication settings", when a brand-colour or contrast finding appears, or when listing text needs to fit each store's limits.
license: MIT
metadata:
  author: Saurabh Yadav
  version: "0.1.0"
---

# Two packages from one listing source

Keep every word of the listing (names, descriptions, prompts, test cases, URLs, colours) in one
file, for example `plugin/listing.json`, and generate both packages from it with a script. Put
the store's name in the shared description as a placeholder (`{app}` → "ChatGPT" or "Claude").
Re-run the generator in CI with a `--check` flag that fails when a package is out of date.

## The ChatGPT ZIP

Upload at platform.openai.com/plugins. The ZIP's root holds:

```
plugin.json                 $schema https://agent-plugins.org/schemas/1.0.0/plugin.schema.json
mcp.json                    the server and its auth
skills/get-started/SKILL.md an onboarding skill (name must match the folder)
assets/icon.png icon-dark.png logo.png
```

Shapes and limits are in `references/chatgpt-package.md`. The checks that the upload enforces
and that bit us, all caught by `scripts/check_chatgpt_package.py`:

- `review.test_cases.positive[].tools_triggered` is **one string**, names joined by `", "`,
  not a list ("Input should be a valid string").
- `mcp.json` `auth` needs **`authorizationUrl` and `tokenUrl`** beside `client: {mode: "cimd"}`
  ("Declare both authorizationUrl and tokenUrl for OAuth"), even though discovery gives them.
- **Brand colours need contrast**: dark vs `#212121` at least 2:1 ("Dark brand color must have at
  least 2:1 contrast against #212121"); check the light one against white too.
- **The demo video is required to submit for review.** Leave an empty `demo_recording_url` out
  (the upload rejects it), and tell the user they still need the video link before submitting:
  in `plugin.json`, or pasted in the portal's Supporting content step.
- Exactly five positive and three negative test cases for submission; `developerName` equal to
  your verified identity; `displayName` and `shortDescription` at most 30 characters; up to three
  `defaultPrompt`s of at most 128.
- No `commerce` in the plugin: purchases stay on your website.

```
python3 scripts/check_chatgpt_package.py upsc-grade-chatgpt.zip           # or a folder
python3 scripts/check_chatgpt_package.py dist/chatgpt --server https://api.example.com
```

`--server` also fetches your authorization-server metadata and checks the ZIP's
`authorizationUrl` and `tokenUrl` match it.

## Claude

Claude has two listings that can point at the same server:

- **The connector** (claude.ai/directory/manage → Submit → MCP connector): typed into the
  portal. Generate its text (one-liner, description, use cases, test steps) from the listing
  source into a markdown file you copy from; see `submit-to-claude`.
- **A plugin bundle** (optional): a public GitHub repo with `.claude-plugin/plugin.json`,
  `.mcp.json` (`{"mcpServers": {"<name>": {"type": "http", "url": "https://…/mcp"}}}`), a skill,
  a README of at least 40 words that says what it does, how to use it and what data it sends,
  and a LICENSE. No symlinks, no secrets.

## Words that fit both

- ChatGPT: `shortDescription` 30 characters ("Your exam second brain"), `longDescription` up to
  4,000, capabilities up to 20 lines of 120.
- Claude: one-liner up to 200, but the directory card shows about 90 before cutting it;
  description up to 2,000.
- Claims must match what the tools do: reviewers compare them. Count things on real data (a
  "20,000 answers" claim that counts empty rows is wrong), and say where data comes from
  ("from the official key wherever one is published").
- Leave affiliation disclaimers and marketing superlatives out of the one-liner; keep facts.
