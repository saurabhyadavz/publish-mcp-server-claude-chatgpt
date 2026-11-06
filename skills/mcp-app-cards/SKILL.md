---
name: mcp-app-cards
description: Build MCP Apps cards (ui:// HTML resources rendered inside the chat) that work in both ChatGPT and Claude - the MCP Apps start-up handshake done in the right order, window.openai treated as an extra and never a reason to skip the handshake, data picked up however the host delivers it so a card never stays blank, the card-domain conflict (Claude's hashed ui.domain vs ChatGPT's openai/widgetDomain), CSP and link targets, and a stand-in host test that runs in headless Chrome. Use when adding a card or widget to an MCP server, porting an OpenAI Apps SDK widget, or when a card shows "timed out", "Couldn't open", renders blank, or works in one host and not the other.
license: MIT
metadata:
  author: Saurabh Yadav
  version: "0.1.0"
---

# MCP Apps cards that render in both hosts

A card is an HTML document served as an MCP resource (`ui://…`, mime type
`text/html;profile=mcp-app`) and linked from a tool with `_meta.ui.resourceUri`. The host runs it
in a sandboxed iframe and talks to it with JSON-RPC over `postMessage`. Both ChatGPT and Claude
implement this standard; they differ in strictness and in a few keys. Start from
`assets/card-template.html`, which already does everything below.

## 1. The start-up, in this order

1. The card sends a request: `{"jsonrpc":"2.0","id":1,"method":"ui/initialize","params":{"protocolVersion":"2026-01-26","appInfo":{"name":"…","version":"…"},"appCapabilities":{…}}}`.
   It's `appInfo`, not `clientInfo`.
2. It waits for the host's answer to id 1.
3. Only then it sends `{"jsonrpc":"2.0","method":"ui/notifications/initialized"}`.
4. The host sends the data in `ui/notifications/tool-result` (`params.structuredContent`), and may
   also include it in the initialize answer (`result.toolResult`).

Claude tolerates a card that sends `initialized` early or names itself wrongly. ChatGPT doesn't:
it waits for a correct start-up and, after about 5 seconds, removes the card ("<card> timed out",
then "Couldn't open <card>").

## 2. window.openai is an extra, never a shortcut

ChatGPT also injects `window.openai` (with `toolOutput`, `theme`, `openExternal`). A card that
sees `window.openai.toolOutput` and skips the handshake draws its data, and ChatGPT still times
it out because the start-up never happened. Always run the handshake. Use `window.openai` only
to draw sooner or to open links.

## 3. Never stay blank

The host may hand data over at different moments, and not always by message. A card that looks
once and then waits can sit on its loading skeleton forever ("Opened <card>" with an empty box).
So: render on `tool-result`, on the initialize answer, on `window.openai.toolOutput` at start,
on the `openai:set_globals` event, and keep checking for about 10 seconds. If nothing arrives,
replace the skeleton with a sentence ("This card could not load here. Ask again.").

## 4. Keys that differ between hosts

| Need | Standard key (Claude reads) | ChatGPT key |
|---|---|---|
| A dedicated origin | `_meta.ui.domain` | `openai/widgetDomain` (alias) |
| Network / assets allowed | `_meta.ui.csp.connectDomains`, `resourceDomains` | `openai/widgetCSP.connect_domains`, `resource_domains` |
| Sites the card may open | (open-link request) | `openai/widgetCSP.redirect_domains` |
| Tool → card link | `_meta.ui.resourceUri` | `openai/outputTemplate` (alias) |

**The conflict:** Claude shows a card only if `ui.domain` is absent or exactly
`<first 32 hex of sha256(full MCP URL)>.claudemcpcontent.com`; anything else gives "Invalid
ui.domain format". ChatGPT requires a domain for a submitted plugin. Leave `ui.domain` out and
put your origin in `openai/widgetDomain`; ChatGPT then serves the card from
`<your-domain-with-dashes>.web-sandbox.oaiusercontent.com`. Use origins with the scheme
(`https://example.com`) in every domain list. ChatGPT appends `?redirectUrl=…` to links it
opens, so make sure no page of your site follows a redirect parameter blindly.

## 5. Test it before either host sees it

`scripts/card_host_test.py` runs a card inside a stand-in host in headless Chrome, three ways:
a plain MCP Apps host; ChatGPT-like, with `window.openai.toolOutput` present at start; and
ChatGPT-late, with `window.openai` filled 1.5 s later and no tool-result message. It checks the
start-up order (appInfo, initialized only after the answer) and that the card drew your data.

```
python3 scripts/card_host_test.py path/to/card.html --data sample.json --expect "text that must appear"
```

Run it on the old card and the new one when fixing a bug; the old should fail the way the host
did, and the new should pass all three.

## 6. Then in the real hosts

- Claude: add the server as a custom connector, ask for the tool, and check that the card draws.
- ChatGPT: chatgpt.com/plugins → your plugin → **Refresh** after every deploy (it caches card
  HTML), then a new chat with the plugin @-mentioned.
- If a host fails, reproduce in the stand-in before changing anything: watch the page for the
  card's frame appearing and disappearing, and the host's own "Opening… / Couldn't open" text.
