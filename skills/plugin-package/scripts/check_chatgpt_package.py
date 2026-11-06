#!/usr/bin/env python3
"""Check a ChatGPT plugin package (a .zip or a folder) for the mistakes the OpenAI upload and
review reject, before you upload it.

  python3 check_chatgpt_package.py my-plugin.zip
  python3 check_chatgpt_package.py dist/chatgpt --server https://api.example.com

Prints every problem; exit code 1 if there are any. With --server it also fetches
<server>/.well-known/oauth-authorization-server and checks the OAuth URLs in mcp.json match.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.request
import zipfile
from pathlib import Path

LIMITS = {"displayName": 30, "shortDescription": 30, "longDescription": 4000, "developerName": 80}
GROUNDS = {"brandColor": "#FFFFFF", "brandColorDark": "#212121"}


def contrast(a: str, b: str) -> float:
    def lum(h: str) -> float:
        c = [int(h.lstrip("#")[i:i + 2], 16) / 255 for i in (0, 2, 4)]
        c = [x / 12.92 if x <= 0.03928 else ((x + 0.055) / 1.055) ** 2.4 for x in c]
        return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]
    hi, lo = sorted((lum(a), lum(b)), reverse=True)
    return (hi + 0.05) / (lo + 0.05)


class Package:
    def __init__(self, path: Path):
        self.path = path
        self.zip = zipfile.ZipFile(path) if path.suffix == ".zip" else None

    def names(self) -> list[str]:
        if self.zip:
            return self.zip.namelist()
        return [str(p.relative_to(self.path)) for p in self.path.rglob("*") if p.is_file()]

    def read(self, name: str) -> str | None:
        name = name.lstrip("./")
        try:
            return (self.zip.read(name).decode("utf-8") if self.zip else (self.path / name).read_text(encoding="utf-8"))
        except (KeyError, FileNotFoundError):
            return None


def check(pkg: Package, server: str | None) -> list[str]:
    bad: list[str] = []
    names = pkg.names()
    if "plugin.json" not in names and any(n.endswith("/plugin.json") for n in names):
        bad.append("plugin.json is not at the ZIP's root: zip the folder's contents, not the folder")
    raw = pkg.read("plugin.json")
    if raw is None:
        return bad + ["no plugin.json"]
    manifest = json.loads(raw)
    oa = manifest.get("extensions", {}).get("com.openai", {})
    face = oa.get("interface", {})
    for k, n in LIMITS.items():
        if not face.get(k):
            bad.append(f"interface.{k} is missing")
        elif len(face[k]) > n:
            bad.append(f"interface.{k} is {len(face[k])} characters, over {n}")
    prompts = face.get("defaultPrompt") or []
    prompts = [prompts] if isinstance(prompts, str) else prompts
    if len(prompts) > 3 or any(len(p) > 128 for p in prompts):
        bad.append("defaultPrompt: at most 3 prompts of at most 128 characters")
    for k in ("websiteURL", "supportURL", "privacyPolicyURL", "termsOfServiceURL"):
        if not str(face.get(k, "")).startswith("https://"):
            bad.append(f"interface.{k} must be an https URL")
    for k, ground in GROUNDS.items():
        c = face.get(k)
        if c and re.fullmatch(r"#[0-9A-Fa-f]{6}", c) and contrast(c, ground) < 2:
            bad.append(f"interface.{k} {c} has {contrast(c, ground):.2f}:1 against {ground}; needs at least 2:1")
    for k in ("composerIcon", "composerIconDark", "logo"):
        if face.get(k) and face[k].lstrip("./") not in names:
            bad.append(f"interface.{k} points at {face[k]}, which isn't in the package")
    skill = oa.get("onboardingSkill")
    if skill:
        body = pkg.read(skill)
        folder = skill.lstrip("./").split("/")[-2] if "/" in skill else ""
        if body is None:
            bad.append(f"onboardingSkill {skill} isn't in the package")
        elif not re.match(rf"---\s*\nname:\s*{re.escape(folder)}\s*\ndescription:", body):
            bad.append(f"{skill}: front matter must start with name: {folder} then description:")
    review = oa.get("review", {})
    cases = review.get("test_cases", {})
    pos, neg = cases.get("positive", []), cases.get("negative", [])
    if len(pos) != 5 or len(neg) != 3:
        bad.append(f"test cases: {len(pos)} positive and {len(neg)} negative; submission needs 5 and 3")
    for i, c in enumerate(pos):
        tt = c.get("tools_triggered")
        if not isinstance(tt, str):
            bad.append(f"positive[{i}].tools_triggered must be one string like \"tool_a, tool_b\", not {type(tt).__name__}")
        elif not re.fullmatch(r"[A-Za-z0-9_.-]+(, [A-Za-z0-9_.-]+)*", tt):
            bad.append(f"positive[{i}].tools_triggered should be names joined by ', ': {tt!r}")
        for k in ("description", "prompt", "expected_behavior"):
            if not isinstance(c.get(k), str) or not c.get(k):
                bad.append(f"positive[{i}].{k} must be a non-empty string")
    for i, c in enumerate(neg):
        if not all(isinstance(c.get(k), str) and c.get(k) for k in ("description", "prompt")):
            bad.append(f"negative[{i}] needs a description and a prompt")
    demo = review.get("demo_recording_url")
    if demo is not None and not str(demo).startswith("https://"):
        bad.append("review.demo_recording_url is empty or not https: leave it out until you have the link")
    if review.get("commerce") not in (False, None):
        bad.append("review.commerce should be false: purchases stay on your website")
    countries = oa.get("publication", {}).get("countries", [])
    if not isinstance(countries, list) or any(not re.fullmatch(r"[A-Z]{2}", c) for c in countries):
        bad.append("publication.countries must be a list of two-letter uppercase codes (or empty)")

    raw_mcp = pkg.read("mcp.json")
    if raw_mcp is None:
        return bad + ["no mcp.json"]
    servers = json.loads(raw_mcp).get("mcpServers", {})
    if not servers:
        bad.append("mcp.json has no mcpServers")
    for name, s in servers.items():
        if s.get("type") != "streamable-http":
            bad.append(f"mcp.json {name}: type should be streamable-http")
        if not str(s.get("url", "")).startswith("https://"):
            bad.append(f"mcp.json {name}: url must be https")
        auth = s.get("extensions", {}).get("com.openai", {}).get("auth", {})
        if auth.get("type") in ("oauth", "mixed"):
            for k in ("authorizationUrl", "tokenUrl"):
                if not str(auth.get(k, "")).startswith("https://"):
                    bad.append(f"mcp.json {name}: auth.{k} is required next to the client mode")
            if server:
                url = server.rstrip("/") + "/.well-known/oauth-authorization-server"
                try:   # a named agent: some bot protection refuses Python's default one
                    req = urllib.request.Request(url, headers={"User-Agent": "ship-mcp-apps-checker/0.1", "Accept": "application/json"})
                    meta = json.load(urllib.request.urlopen(req, timeout=20))
                except Exception as exc:
                    bad.append(f"could not read {url}: {exc}")
                    meta = {}
                for k, mk in (("authorizationUrl", "authorization_endpoint"), ("tokenUrl", "token_endpoint")):
                    if meta and auth.get(k) and auth[k] != meta.get(mk):
                        bad.append(f"mcp.json {name}: auth.{k} {auth[k]} differs from the server's {mk} {meta.get(mk)}")
    if any(n.endswith((".app.json",)) or "/hooks/" in n for n in names):
        bad.append("the package holds apps or hooks, which can't be submitted")
    return bad


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("package", type=Path)
    ap.add_argument("--server", default=None, help="the OAuth issuer, e.g. https://api.example.com")
    a = ap.parse_args()
    bad = check(Package(a.package), a.server)
    for b in bad:
        print("FAIL", b)
    print("OK: no problems found" if not bad else f"{len(bad)} problem(s)")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
