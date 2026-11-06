# ship-mcp-apps

**Agent skills for Claude Code and Codex (and any agent that reads `SKILL.md`) that take one MCP
server into both the ChatGPT plugin directory and Claude's connector directory, end to end.**

ChatGPT plugins and Claude connectors now run on the same thing: a remote MCP server, OAuth
sign-in and MCP Apps cards. The official guides each cover one store. These skills cover both,
including the places where doing it right for one breaks the other, from a real app that went
through both reviews ([UPSC Grade](https://upscgrade.com)).

## Quick start

Ask your agent: **"Help me ship my MCP server to ChatGPT and Claude."** The `ship-mcp-plugin`
skill finds where you are and runs the rest in order.

## Install

<details open><summary><b>Claude Code</b></summary>

```
/plugin marketplace add saurabhyadavz/ship-mcp-apps
/plugin install ship-mcp-apps@ship-mcp-apps
```
</details>

<details><summary><b>Codex</b></summary>

```
codex plugin marketplace add saurabhyadavz/ship-mcp-apps
```
then `/plugins` and install **ship-mcp-apps**.
</details>

<details><summary><b>Any agent (skills CLI)</b></summary>

```
npx skills add saurabhyadavz/ship-mcp-apps -a claude-code    # or -a codex
```
</details>

<details><summary><b>By hand</b></summary>

Copy the folders under `skills/` into `~/.claude/skills/` (Claude Code) or `~/.agents/skills/`
(Codex).
</details>

## The skills

| Skill | What it does |
|---|---|
| `ship-mcp-plugin` | Start here: finds your stage, runs the others, lists the cross-store conflicts |
| `plugin-prerequisites` | Accounts, identity verification, domain, legal pages, a mailbox that receives mail, a reviewer login with no codes |
| `mcp-server-for-plugins` | Tool names, titles, all four hints, output schemas, size budgets, and server instructions that make ChatGPT call your tool |
| `plugin-oauth` | OAuth 2.1 + PKCE, CIMD and DCR, `iss`, refresh rotation, the consent page, a safe reviewer password login, and "it sends me back to sign-in" fixes |
| `mcp-app-cards` | Cards that render in both hosts: the handshake order, `window.openai` as an extra, never blank, the `ui.domain` conflict, and a headless stand-in host test |
| `plugin-package` | One listing source → the ChatGPT ZIP and Claude's text; a checker for every upload error we hit |
| `submit-to-chatgpt` | platform.openai.com/plugins step by step: test in ChatGPT, upload, domain token, reviewer details, findings, demo video |
| `submit-to-claude` | claude.ai/directory/manage's ten steps, copy that fits the card, test steps, the plugin bundle |

## Scripts you can run without an agent

```
python3 skills/mcp-app-cards/scripts/card_host_test.py card.html --data sample.json --expect "text"
python3 skills/plugin-package/scripts/check_chatgpt_package.py my-plugin.zip --server https://api.example.com
```

## Layout

```
skills/<name>/SKILL.md          one folder per skill (Agent Skills format: works in Claude Code and Codex)
skills/<name>/references/       detail the skill loads when needed
skills/<name>/scripts/          tools the skill runs
.claude-plugin/                 Claude Code plugin + marketplace
.codex-plugin/  .agents/        Codex plugin + marketplace
scripts/validate_skills.py      checks every skill's front matter and the manifests (CI runs it)
```

## Contributing

Each rule here was learned by shipping. If a store changes something, open an issue with the
message you saw and the page it came from. Run `python3 scripts/validate_skills.py` before a PR.

## Licence

MIT. Not affiliated with OpenAI or Anthropic; "ChatGPT" and "Claude" are their trademarks.
