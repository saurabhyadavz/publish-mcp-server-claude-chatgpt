---
type: regex
pattern: '"authorizationUrl"[\s\S]*"tokenUrl"|"tokenUrl"[\s\S]*"authorizationUrl"'
match: contains
target: {source: file, path: chatgpt/mcp.json}
weight: 1
---

chatgpt/mcp.json declares both authorizationUrl and tokenUrl
