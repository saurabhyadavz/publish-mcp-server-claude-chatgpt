#!/usr/bin/env python3
"""Run an MCP Apps card inside a stand-in host in headless Chrome and check the start-up the
2026-01-26 spec asks for, three ways:

  plain    a plain MCP Apps host: answers ui/initialize after 300 ms, then sends tool-result
  chatgpt  like ChatGPT: window.openai.toolOutput is already set when the card's script runs
  late     like ChatGPT, later: window.openai is empty at first, filled 1.5 s later with an
           openai:set_globals event, and no tool-result message is ever sent

Checks: ui/initialize carries appInfo (not clientInfo); ui/notifications/initialized comes only
after the host answered; the card drew text from the data.

Usage:
  python3 card_host_test.py card.html [card2.html ...] --data sample.json --expect "some text"
  python3 card_host_test.py card.html --chrome "/path/to/chrome"     # if Chrome isn't found
Exit code 0 when every card passes every mode.
"""
from __future__ import annotations

import argparse
import html
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HOST = """<!doctype html><html><body><iframe id="f" srcdoc="__CARD__"></iframe><pre id="out">pending</pre>
<script>
var log=[], f=document.getElementById('f'), answered=false;
function send(m){f.contentWindow.postMessage(m,'*');}
window.addEventListener('message',function(ev){
  var m=ev.data; if(!m||m.jsonrpc!=='2.0')return;
  log.push({method:m.method||null, answered:answered,
            hasAppInfo:!!(m.params&&m.params.appInfo), hasClientInfo:!!(m.params&&m.params.clientInfo)});
  if(m.method==='ui/initialize'){
    setTimeout(function(){answered=true; send({jsonrpc:'2.0',id:m.id,result:{protocolVersion:'2026-01-26',
      hostInfo:{name:'stand-in',version:'1'},hostCapabilities:{},hostContext:{theme:'light'}}});},300);
  }
  if(m.method==='ui/notifications/initialized'&&__SEND_RESULT__){
    setTimeout(function(){send({jsonrpc:'2.0',method:'ui/notifications/tool-result',params:{structuredContent:__DATA__}});},100);
  }
});
setTimeout(function(){
  var root=f.contentDocument&&f.contentDocument.getElementById('root');
  var text=(root||f.contentDocument.body).textContent.trim();
  document.getElementById('out').textContent=JSON.stringify({log:log, text:text.slice(0,400)});
},3000);
</script></body></html>"""

CHROME_GUESSES = [
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Chromium.app/Contents/MacOS/Chromium",
    "google-chrome", "google-chrome-stable", "chromium", "chromium-browser",
]


def find_chrome(given: str | None) -> str:
    for c in ([given] if given else []) + CHROME_GUESSES:
        if c and (os.path.exists(c) or shutil.which(c)):
            return c
    sys.exit("Chrome not found: pass --chrome /path/to/chrome")


def js(data: dict) -> str:
    """The data as a JavaScript literal that is safe inside <script> (no "</script>" break-out)."""
    return json.dumps(data).replace("<", "\\u003c")


def run(chrome: str, card: Path, data: dict, mode: str) -> dict:
    body = card.read_text(encoding="utf-8")
    inject = ""
    if mode == "chatgpt":
        inject = "<script>window.openai={toolOutput:" + js(data) + ",theme:'light'};</script>"
    elif mode == "late":
        inject = ("<script>window.openai={theme:'light'};setTimeout(function(){window.openai.toolOutput="
                  + js(data) + ";window.dispatchEvent(new CustomEvent('openai:set_globals',"
                  "{detail:{globals:{toolOutput:window.openai.toolOutput}}}));},1500);</script>")
    if inject:
        body = re.sub(r"<head[^>]*>", lambda m: m.group(0) + inject, body, count=1) if "<head" in body else inject + body
    page = (HOST.replace("__CARD__", html.escape(body, quote=True)).replace("__DATA__", js(data))
            .replace("__SEND_RESULT__", "false" if mode == "late" else "true"))
    with tempfile.TemporaryDirectory() as d:
        host = Path(d) / "host.html"
        host.write_text(page, encoding="utf-8")
        try:
            out = subprocess.run([chrome, "--headless=new", "--disable-gpu", "--no-first-run", f"--user-data-dir={d}/u",
                                  "--virtual-time-budget=7000", "--dump-dom", host.as_uri()],
                                 capture_output=True, text=True, timeout=90).stdout
        except subprocess.TimeoutExpired:
            return {"error": "Chrome timed out (run again; if it repeats, the card may loop forever)"}
    got = re.search(r'<pre id="out">(.*?)</pre>', out, re.S)
    if not got or got.group(1) == "pending":
        return {"error": "no result from Chrome"}
    return json.loads(html.unescape(got.group(1)))


def verdict(r: dict, expect: str) -> list[str]:
    if "error" in r:
        return [r["error"]]
    bad = []
    init = [e for e in r["log"] if e["method"] == "ui/initialize"]
    done = [e for e in r["log"] if e["method"] == "ui/notifications/initialized"]
    if not init:
        bad.append("never sent ui/initialize")
    else:
        if not init[0]["hasAppInfo"]:
            bad.append("ui/initialize has no appInfo")
        if init[0]["hasClientInfo"]:
            bad.append("ui/initialize sends clientInfo")
    if not done:
        bad.append("never sent initialized")
    elif not done[0]["answered"]:
        bad.append("sent initialized before the host answered")
    if expect not in r.get("text", ""):
        bad.append(f"did not draw the data (no {expect!r})")
    return bad


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("cards", nargs="+", type=Path)
    ap.add_argument("--data", type=Path, help="JSON file: the tool's structuredContent")
    ap.add_argument("--expect", default=None, help="text that must appear once the card drew the data")
    ap.add_argument("--chrome", default=None)
    a = ap.parse_args()
    data = json.loads(a.data.read_text()) if a.data else {"title": "Stand-in result", "summary": "Drawn from the data."}
    expect = a.expect or str(data.get("title") or next(iter(data.values())))
    chrome = find_chrome(a.chrome)
    failed = False
    for card in a.cards:
        for mode in ("plain", "chatgpt", "late"):
            bad = verdict(run(chrome, card, data, mode), expect)
            failed |= bool(bad)
            print(("PASS" if not bad else "FAIL"), f"{card.name} [{mode}]", "|", "; ".join(bad) or "ok")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
