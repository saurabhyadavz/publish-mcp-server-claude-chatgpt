# Test results

Run on 7 November 2026 with `claude plugin eval` (Claude Code 2.1.319, Claude Opus 5.5). Each
case ran with the plugin and without it. The judge for written answers is Claude Haiku. Files
the runs produced were also checked with this repo's own scripts (`card_host_test.py`,
`check_chatgpt_package.py`).

| Case | With the skills | Without | What the difference was |
|---|---|---|---|
| `chatgpt-package-from-scratch` | 100% (3 runs) | 3% | Without the skills the agent wrote the old `.codex-plugin` layout and no `mcp.json`. All three packages made with them pass the checker. |
| `domain-token-missing` | 100% (2 runs) | 25% | Without the skills the agent didn't know the token sits in the Connect MCP server panel. |
| `where-do-i-start` | 100% (2 runs) | 33% | Without the skills: no reviewer account without codes, no CIMD, and "ChatGPT plugins were retired in 2024". |
| `upload-rejected` | 100% (2 runs) | 43% | Without the skills the agent fixed only the error it was shown. The checker found four problems left in each of its packages. |
| `card-times-out-in-chatgpt` | all checks pass | all but one | Both versions fixed the start-up, and all six cards pass the stand-in host in all three modes. With the skills, every card also shows a message when no data ever arrives. Without them, two of three stay on "Loading…". |

## What the runs changed

- `plugin-package` now says plainly that the demo video is required before submitting. One run
  had left that out of its reply. After the change, both re-runs passed.
- `check_chatgpt_package.py` reports a `plugin.json` or `mcp.json` that isn't valid JSON instead of
  crashing.
- The graders now read the one file or the final reply they judge, not the whole transcript. A
  text check that flagged `clientInfo` inside a comment now looks only for a real key.

## Not tested yet

Codex: the skills follow the Agent Skills format and the Codex plugin layout, but no run has been
made in Codex itself.
