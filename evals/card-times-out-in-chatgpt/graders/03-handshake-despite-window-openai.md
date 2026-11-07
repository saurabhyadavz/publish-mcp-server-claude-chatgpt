---
type: llm
focus: {source: file, path: card.html}
weight: 1
---

This card runs the ui/initialize handshake even when window.openai.toolOutput is already set when it starts; window.openai is only used to draw early
