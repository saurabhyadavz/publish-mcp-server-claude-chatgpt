---
name: mcp-server-for-plugins
description: Design or review the tools of a remote MCP server so both ChatGPT's plugin review and Claude's connector review accept it and both models actually call it - Streamable HTTP at /mcp, verb_first tool names, titles, all four annotation hints set explicitly, output schemas with structured content, error results that say what to do, a per-result size budget, and server instructions that make ChatGPT use your tool instead of its own built-in features. Use when building or auditing an MCP server for ChatGPT or Claude, when a test prompt gets answered without your tool being called, when a review flags annotations or descriptions, or when tool results are too large.
license: MIT
metadata:
  author: Saurabh Yadav
  version: "0.1.0"
---

# An MCP server both stores accept

Both reviews read your tool list (names, titles, descriptions, annotations, schemas) and run the
test prompts you give them. Most findings come from the tool list itself, so get it right before
packaging. Detailed rules with examples: `references/tool-design.md`.

## Transport and shape

- Streamable HTTP at one URL, for example `https://api.example.com/mcp`. Both stores connect
  server-to-server; neither needs your server to be reachable from the user's browser except
  the sign-in pages.
- Every request needs a bearer token (see `plugin-oauth`). Unauthenticated calls get 401 with a
  `WWW-Authenticate` header that points at your protected-resource metadata.
- Allow only your own public host in the `Host` check (DNS-rebinding protection) and keep a
  health endpoint that reports the deployed version.

## Each tool

Audit every tool against this list. A script that walks your registry and asserts it is cheap
and catches regressions (see the reference for one).

1. **Name**: verb first, lowercase snake_case, under 64 characters, unique: `get_marked_answer`,
   `search_questions`, `mark_pasted_answer`. No product prefix.
2. **Title**: short and human, shown in both UIs ("A marked answer").
3. **Description**: what it does and what it returns, in plain words. Don't steer ("use this
   first", "start here") - reviewers flag it and it belongs in server instructions.
4. **All four annotations, set explicitly**: `readOnlyHint`, `destructiveHint`,
   `idempotentHint`, `openWorldHint`. A missing hint is read as the cautious value. Anything that
   spends the user's money or credits is `destructiveHint: true` so hosts ask before running it.
5. **Inputs**: minimal, each with a description. A tool that takes nothing declares
   `{"type":"object","properties":{},"additionalProperties":false}`.
6. **Output schema + `structuredContent`**, plus the same data as text for clients that don't
   read structured output. Links are whole `https://` URLs, never paths.
7. **Errors**: return `isError: true` with a sentence that says what to do next ("Choose one
   option: a, b, c or d."), not a stack trace.
8. **Size**: hold every result under a budget (about 20,000 characters is a good ceiling).
   Measure on real data, not seeded tests: a list of ten real items can be several times the
   size of ten test items. When a field pushes a list over, return it only from the single-item
   tool.
9. **No generic executor** ("run_query", "call_api"); one tool per job.

## Make the model call you

ChatGPT has built-in features (quizzes, web search, canvases). A prompt like "give me 5
practice questions" can be answered by ChatGPT itself even with your plugin connected, and a
reviewer sees your test case fail. Two fixes, both needed:

- **Server instructions** (the `instructions` field at initialize): say when to use which tool
  and what never to do instead, for example "When the user asks for practice questions, start a
  quiz with start_quiz, which gives our own past questions; never write questions of your own."
- **A description that leads with the job**: "Gives the user practice questions: our own past
  questions, as a quiz..." rather than leading with mechanics.

Write test prompts that name the thing only your tool has ("5 of our past questions"), and test
them in ChatGPT without @-mentioning the plugin as well as with it.

## Before packaging

- Snapshot the tool list (names, descriptions, schemas) in a test so every change is visible.
- Run each review test prompt against the deployed server in both hosts.
- Keep a catalogue page (a docs URL) generated from the same registry; Claude asks for one.
