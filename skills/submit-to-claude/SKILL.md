---
name: submit-to-claude
description: Walk through listing a remote MCP server in Claude's connector directory at claude.ai/directory/manage - testing it first as a custom connector, letting Anthropic's servers through bot protection, the portal's ten steps (connection, tools, listing copy that fits the directory card, use cases, company, authentication, data handling, test account, compliance, review), card link permissions and screenshots, and pairing an optional Claude plugin bundle. Use when someone wants their MCP server, app or ChatGPT plugin in Claude's directory, is filling in the Claude connector portal, needs listing copy or categories, or their connector fails to link in claude.ai.
license: MIT
metadata:
  author: Saurabh Yadav
  version: "0.1.0"
---

# Submitting to Claude's connector directory

Submit from an account on a paid Claude plan. Anthropic's review checks the listing against
what the tools do and runs your test steps with the reviewer account. Every field, in the
portal's order: `references/portal.md`.

## 0. Test as a custom connector first

claude.ai → Settings → Connectors → **Add custom connector** → paste the MCP URL exactly
(`https://…/mcp`, no trailing character) → sign in on your page → Allow. Then in a new chat with
the connector on, run each use case and check the cards draw.

If linking bounces you back to the sign-in page or Allow vanishes, see the debugging list in
`plugin-oauth` (another open tab signing you out, bot protection, a stale tab after a deploy).
If you use bot protection, let Anthropic's published egress ranges through for `/mcp` and the
OAuth endpoints.

## 1. The ten steps (claude.ai/directory/manage → Submit new → MCP connector)

1. **Connection**: the universal MCP URL.
2. **Tools**: read from your server automatically; each needs a title and all four hints.
3. **Listing**: name; **one-liner** (limit 200, but the directory card shows about 90
   characters, so put the whole hook in the first 90); categories; documentation URL; privacy
   URL; support; icon; URL slug (permanent once published); **description** (≤2,000).
4. **Use cases**: at least three, each a title, a prompt, and what Claude does with it; also
   "what someone needs before connecting" and whether the connector reads, writes or both.
5. **Company**: name and website; a contact for review updates.
6. **Authentication**: OAuth. Claude registers by Client ID Metadata Document (or DCR), so
   there's no client secret to share. Its return address is
   `https://claude.ai/api/mcp/auth_callback`.
7. **Data handling**: whose API it is, health data, sponsored content, and a plain statement of
   what you read and keep.
8. **Test & launch**: the reviewer account's email (the password goes only in the credentials
   field) and numbered steps a stranger can follow; confirm you tested every tool in Claude.
9. **Compliance**: seven acknowledgements; read each.
10. **Review and submit.**

Cards that open links need those origins listed as allowed link URIs (scheme and host only, your
own domains). Screenshots: 3–5 PNGs at least 1000 px wide, cropped to the card, with the prompt
given separately.

## 2. Copy that passes review

- Lead the one-liner with what the user gets, not the technology.
- Every claim in the description must be something a tool returns today. If the listing promises
  a feature, check the connector actually exposes it, not just your website.
- Numbers counted on real data. Wording like "from the official source wherever one is published"
  when some data is unofficial.
- After submitting, keep the generated portal text in your repo so a later edit starts from what
  was submitted.

## 3. The optional plugin bundle

A Claude plugin (public GitHub repo) can bundle a skill that teaches Claude to use your tools
well, with `.mcp.json` pointing at the **same** MCP URL. Submit it separately and pair it with the
connector; see `plugin-package` for the files and the directory's checklist (README ≥40 words,
LICENSE, no symlinks or secrets).
