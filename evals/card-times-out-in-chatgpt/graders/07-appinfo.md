---
type: regex
pattern: 'appInfo'
match: contains
target: {source: file, path: card.html}
weight: 1
---

card.html sends appInfo in ui/initialize
