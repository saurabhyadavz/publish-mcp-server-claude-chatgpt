---
type: llm
focus: trace
weight: 1
---

The fixed card.html picks up data that arrives late (listens for openai:set_globals or keeps checking window.openai.toolOutput for some seconds) and shows a message instead of staying on "Loading…" forever
