# Working in this repo

This repo is a set of agent skills, not an app. Rules that keep it installable in both Claude Code
and Codex and listable in both stores' directories:

- One folder per skill under `skills/`, with `SKILL.md` whose `name` equals the folder name.
- Front matter uses only the Agent Skills fields: `name`, `description`, `license`,
  `compatibility`, `metadata` (and the experimental `allowed-tools`). Claude-Code-only fields
  break uploads to claude.ai and the API.
- Keep `SKILL.md` under 500 lines; put detail in the skill's own `references/` and tools in its
  `scripts/`. Don't share files across skills: per-skill installs copy only the skill's folder.
- No hooks (they rule a plugin out of OpenAI's directory), no symlinks, no secrets, no
  submodules.
- Bump `version` in `.claude-plugin/plugin.json`, `.codex-plugin/plugin.json` and the
  marketplace together.
- Every factual claim about a store should be something a store page or a real submission
  showed. Note the month it was checked.
- Run `python3 scripts/validate_skills.py` before committing.
