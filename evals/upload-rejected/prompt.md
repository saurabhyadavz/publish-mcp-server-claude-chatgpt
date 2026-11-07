---
tags: [package]
max_turns: 25
timeout_seconds: 900
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit, Bash]
---

OpenAI's plugin upload keeps rejecting my package. First it said "Invalid plugin package: tools_triggered: Input should be a valid string", and I think there will be more errors after that. My package is in the chatgpt/ folder. Fix everything that would get it rejected so I only upload once more.

Input files: chatgpt/plugin.json, chatgpt/mcp.json
