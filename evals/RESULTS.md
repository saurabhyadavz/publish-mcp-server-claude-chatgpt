# Test results

Run on 7 November 2026 with `claude plugin eval` (Claude Code 2.1.319, Claude Opus 5.5). Each
case ran with the plugin and without it. The files the runs produced were also checked with this
repo's own scripts (`card_host_test.py`, `check_chatgpt_package.py`).

| Case | With the skills | Without | What the difference was |
|---|---|---|---|
| `chatgpt-package-from-scratch` | 100% (3 runs) | 3% (3 runs) | Without the skills the agent wrote the old `.codex-plugin` layout and no `mcp.json`. All three packages made with them pass the checker. |
| `domain-token-missing` | 100% (2 runs) | 25% (2 runs) | Without the skills the agent didn't know the token sits in the Connect MCP server panel. |
| `where-do-i-start` | 100% (2 runs) | 33% (2 runs) | Without the skills: no reviewer account without codes, no CIMD, and "ChatGPT plugins were retired in 2024". |
| `upload-rejected` | 86% (2 runs), then 100% (2 runs) after a wording fix | 43% (2 runs) | Without the skills the agent fixed only the error it was shown. The checker found four problems left in each of its packages. |
| `card-times-out-in-chatgpt` | all checks pass (3 runs) | all but one (3 runs) | Both versions fixed the start-up, and all six cards pass the stand-in host in all three modes. With the skills, every card shows a message when no data ever arrives. Without them, all three stay on "Loading…". |

## Where each row comes from

- **Card and from-scratch rows:** the first batch. It used a Claude Sonnet judge and an earlier
  version of the graders, which read the whole transcript. The card row's "all checks pass" also
  discounts a text check that wrongly flagged `clientInfo` inside a code comment; that check is
  now fixed. The graders committed for these two cases haven't been run yet.
- **Domain-token, where-do-i-start and the first upload row:** the second batch, with the
  committed graders and the default Claude Haiku judge.
- **The upload row's 100%:** a re-run after the change below, with the skills only (no baseline
  arm).

## What the runs changed

- `plugin-package` now says plainly that the demo video is required before submitting. One run
  had left that out of its reply. After the change, both re-runs passed.
- `check_chatgpt_package.py` reports a `plugin.json` or `mcp.json` that isn't valid JSON instead of
  crashing.
- The graders now read the one file or the final reply they judge, not the whole transcript. A
  text check that flagged `clientInfo` inside a comment now looks only for a real key.

## Still to do

- Run the card and from-scratch cases once with the committed graders.
- Codex: the skills follow the Agent Skills format and the Codex plugin layout, but no run has
  been made in Codex itself.
