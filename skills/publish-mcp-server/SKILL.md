---
name: publish-mcp-server
description: Start here to take one MCP server into both the ChatGPT plugin directory (platform.openai.com/plugins) and Claude's connector directory (claude.ai/directory) end to end. Use whenever someone wants to publish, list, submit or "ship" an MCP server, ChatGPT app, ChatGPT plugin, Claude connector or MCP Apps UI, asks what is left before submitting, or is stuck at any step from first setup to a reviewer's findings, even if they only name one of the two stores.
license: MIT
metadata:
  author: Saurabh Yadav
  version: "0.1.0"
---

# Publish one MCP server to ChatGPT and Claude

Both stores now run on the same thing: a remote MCP server over Streamable HTTP, OAuth sign-in,
and (optionally) MCP Apps cards. So one server can be listed in both. What differs is a handful
of rules that conflict, two packaging formats and two review portals. This skill finds where the
person is and runs the right next skill, in this order:

| Stage | Skill | Done when |
|---|---|---|
| 1 | `plugin-prerequisites` | accounts, domain, legal pages, support mailbox, reviewer account exist |
| 2 | `mcp-server-for-plugins` | every tool has a verb_first name, a title, all four hints and an output schema; results fit the size budget |
| 3 | `plugin-oauth` | discovery documents, PKCE, CIMD and DCR work; a reviewer can sign in with no codes |
| 4 | `mcp-app-cards` (skip if no cards) | the stand-in host test passes in all three modes; a card renders in both hosts |
| 5 | `plugin-package` | one listing source writes both packages; the package checker passes |
| 6 | `submit-to-chatgpt` | the portal shows no blocking findings; review submitted |
| 7 | `submit-to-claude` | the connector portal's ten steps are filled; review submitted |

Stages 6 and 7 are independent once 1–5 are done; most people submit to Claude first because it
needs fewer assets (no demo video).

## How to run it

1. **Find the stage.** Ask only what you cannot see. If you are in the server's repo, look: is
   there an `/mcp` route, `/.well-known/oauth-authorization-server`, `ui://` resources, a
   `plugin.json` or `.claude-plugin/`? Each answers a stage without a question.
2. **Run the stage's skill**, then come back here and tick it off.
3. **Keep one listing source.** Names, descriptions, prompts and test cases live in one file and
   both packages are generated from it (stage 5). Writing two by hand is how listings drift.
4. **Ask before anything leaves the machine**: a push that deploys, a portal submission, a
   public repo. Each store review takes days to weeks, so a rejection costs far more than a check.

## The conflicts to know up front

These are the places where doing the right thing for one store breaks the other. Each skill
covers its own in detail; know they exist before starting.

- **Card domain.** Claude shows a card only if `_meta.ui.domain` is its own hash of your URL or
  is absent; ChatGPT wants a domain declared. Leave `ui.domain` out and give ChatGPT its alias,
  `openai/widgetDomain` (`mcp-app-cards`).
- **Card start-up.** ChatGPT also injects `window.openai`. A card that skips the MCP Apps
  handshake when it sees `window.openai` works in Claude and times out in ChatGPT after about
  5 seconds (`mcp-app-cards`).
- **Tool choice.** ChatGPT has its own features (quizzes, web search). Without server
  instructions that say when to use your tool, it may answer a test prompt without calling you
  (`mcp-server-for-plugins`).
- **Sign-in.** Both register as OAuth clients by Client ID Metadata Document (CIMD) from their
  own domains; other apps use Dynamic Client Registration (DCR). Support both (`plugin-oauth`).
- **Listing words.** ChatGPT allows 30 characters for a short description; Claude's card shows
  about 90 characters of a one-liner. Write per store from one source (`plugin-package`).

## When something fails

Read the failure literally before theorising. A portal finding, a card that says "timed out",
a sign-in that bounces: each skill lists the messages it has seen and what fixed them. If the
message is new, reproduce it against a stand-in (the cards skill ships a stand-in host) before
changing code that already works in the other store.
