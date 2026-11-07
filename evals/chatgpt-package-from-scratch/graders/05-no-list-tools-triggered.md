---
type: regex
pattern: '"tools_triggered"\s*:\s*\['
match: not_contains
target: {source: file, path: chatgpt/plugin.json}
weight: 1
---

No tools_triggered in chatgpt/plugin.json is a list
