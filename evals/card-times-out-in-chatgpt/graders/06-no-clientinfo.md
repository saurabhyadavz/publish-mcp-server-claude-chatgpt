---
type: regex
pattern: 'clientInfo"?\s*:'
match: not_contains
target: {source: file, path: card.html}
weight: 1
---

card.html no longer sends a clientInfo key (the MCP Apps spec names it appInfo)
