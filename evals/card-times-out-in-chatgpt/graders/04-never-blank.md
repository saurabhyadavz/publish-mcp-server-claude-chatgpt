---
type: llm
focus: {source: file, path: card.html}
weight: 1
---

This card picks up data that arrives late (it listens for openai:set_globals or keeps checking window.openai.toolOutput for some seconds) and, if no data ever comes, replaces the Loading text with a message instead of staying on Loading forever
