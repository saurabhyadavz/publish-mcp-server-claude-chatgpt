---
type: regex
pattern: '"demo_recording_url"\s*:\s*""'
match: not_contains
target: {source: file, path: chatgpt/plugin.json}
weight: 1
---

chatgpt/plugin.json no longer has an empty demo_recording_url
