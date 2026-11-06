#!/usr/bin/env python3
"""Check every skill and manifest the way the stores and agents read them:

- skills/<name>/SKILL.md exists, front matter has only Agent Skills fields, name == folder,
  name is a-z0-9- (1-64), description 1-1024 characters, body under 500 lines
- no symlinks anywhere in the repo, no hooks folders
- the three manifests agree on name and version; JSON parses
Exit 1 on any problem.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ALLOWED = {"name", "description", "license", "compatibility", "metadata", "allowed-tools"}


def front_matter(text: str) -> tuple[dict, str] | None:
    if not text.startswith("---\n"):
        return None
    head, _, body = text[4:].partition("\n---\n")
    fields: dict = {}
    for line in head.splitlines():
        m = re.match(r"^([A-Za-z][\w-]*):\s*(.*)$", line)
        if m:
            fields[m.group(1)] = m.group(2)
    return fields, body


def main() -> int:
    bad: list[str] = []
    skills = sorted(p for p in (ROOT / "skills").iterdir() if p.is_dir())
    for d in skills:
        f = d / "SKILL.md"
        if not f.exists():
            bad.append(f"{d.name}: no SKILL.md")
            continue
        got = front_matter(f.read_text(encoding="utf-8"))
        if got is None:
            bad.append(f"{d.name}: SKILL.md must start with --- front matter")
            continue
        fields, body = got
        extra = set(fields) - ALLOWED
        if extra:
            bad.append(f"{d.name}: front matter fields outside the Agent Skills spec: {sorted(extra)}")
        name = fields.get("name", "")
        if name != d.name:
            bad.append(f"{d.name}: name {name!r} must equal the folder name")
        if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", name) or len(name) > 64:
            bad.append(f"{d.name}: name must be lowercase a-z0-9 with single hyphens, at most 64")
        desc = fields.get("description", "")
        if not 1 <= len(desc) <= 1024:
            bad.append(f"{d.name}: description is {len(desc)} characters; must be 1-1024")
        if len(body.splitlines()) >= 500:
            bad.append(f"{d.name}: SKILL.md body is {len(body.splitlines())} lines; keep it under 500")
    for p in ROOT.rglob("*"):
        if ".git" in p.parts:
            continue
        if p.is_symlink():
            bad.append(f"symlink not allowed: {p.relative_to(ROOT)}")
        if p.is_dir() and p.name == "hooks":
            bad.append(f"hooks aren't allowed in a plugin for OpenAI's directory: {p.relative_to(ROOT)}")
    manifests = {}
    for rel in (".claude-plugin/plugin.json", ".codex-plugin/plugin.json", ".claude-plugin/marketplace.json",
                ".agents/plugins/marketplace.json"):
        try:
            manifests[rel] = json.loads((ROOT / rel).read_text(encoding="utf-8"))
        except (FileNotFoundError, json.JSONDecodeError) as exc:
            bad.append(f"{rel}: {exc}")
    a, b = manifests.get(".claude-plugin/plugin.json", {}), manifests.get(".codex-plugin/plugin.json", {})
    if a and b and (a.get("name"), a.get("version")) != (b.get("name"), b.get("version")):
        bad.append("the Claude and Codex plugin.json files disagree on name or version")
    mv = manifests.get(".claude-plugin/marketplace.json", {}).get("metadata", {}).get("version")
    if mv and a and mv != a.get("version"):
        bad.append("marketplace.json metadata.version differs from plugin.json version")
    for b_ in bad:
        print("FAIL", b_)
    print(f"{len(skills)} skills checked: " + ("all good" if not bad else f"{len(bad)} problem(s)"))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
