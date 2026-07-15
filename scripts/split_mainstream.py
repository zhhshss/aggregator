#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Split mainstream-airport nodes from collect clash output and upload to Gist."""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import urllib.error
import urllib.request

import yaml

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DATA = os.path.join(ROOT, "data")


def load_keywords(path: str) -> list[str]:
    items: list[str] = []
    if not path or not os.path.isfile(path):
        return items
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            items.append(line)
    return items


def compile_pattern(keywords: list[str]) -> re.Pattern | None:
    parts = [re.escape(k) for k in keywords if k]
    if not parts:
        return None
    return re.compile("|".join(parts), flags=re.I)


def load_proxies(path: str) -> list[dict]:
    if not path or not os.path.isfile(path):
        return []
    with open(path, "r", encoding="utf-8") as f:
        raw = f.read()
    if not raw.strip():
        return []
    data = yaml.safe_load(raw) or {}
    if not isinstance(data, dict):
        return []
    proxies = data.get("proxies") or []
    return [p for p in proxies if isinstance(p, dict)]


def domain_of(url: str) -> str:
    m = re.search(r"https?://([^/:\s]+)", url or "", flags=re.I)
    return (m.group(1) if m else "").lower()


def is_mainstream(proxy: dict, pat: re.Pattern | None, domains: set[str]) -> bool:
    name = str(proxy.get("name") or "")
    sub = str(proxy.get("sub") or "")
    server = str(proxy.get("server") or "")
    hay = f"{name} {sub} {server}"
    if pat and pat.search(hay):
        return True
    if domains:
        d = domain_of(sub)
        if d and any(d == x or d.endswith("." + x) for x in domains):
            return True
    return False


def dump_clash(path: str, proxies: list[dict]) -> str:
    cleaned = []
    for p in proxies:
        item = dict(p)
        for k in ("sub", "liveness", "chatgpt"):
            item.pop(k, None)
        cleaned.append(item)
    content = yaml.safe_dump({"proxies": cleaned}, allow_unicode=True, sort_keys=False)
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    return content


def gist_patch(token: str, gist_id: str, files: dict[str, str]) -> bool:
    payload = json.dumps({"files": {n: {"content": c if c else " "} for n, c in files.items()}}).encode("utf-8")
    req = urllib.request.Request(
        url=f"https://api.github.com/gists/{gist_id}",
        data=payload,
        method="PATCH",
        headers={
            "Authorization": f"token {token}",
            "Accept": "application/vnd.github+json",
            "Content-Type": "application/json",
            "User-Agent": "aggregator-mainstream-split",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=90) as resp:
            return 200 <= getattr(resp, "status", 200) < 300
    except urllib.error.HTTPError as e:
        print(f"[gist] HTTP {e.code}: {e.read().decode('utf-8', 'replace')[:500]}", file=sys.stderr)
        return False
    except Exception as e:
        print(f"[gist] error: {e}", file=sys.stderr)
        return False


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--input", default=os.path.join(DATA, "clash.yaml"))
    ap.add_argument("-b", "--brands", default=os.path.join(DATA, "mainstream_brands.txt"))
    ap.add_argument("-d", "--domains", default="")
    ap.add_argument("-g", "--gist", default=os.environ.get("GIST_LINK", ""))
    ap.add_argument("-k", "--key", default=os.environ.get("GIST_PAT", ""))
    ap.add_argument("-o", "--outdir", default=DATA)
    args = ap.parse_args()

    link = (args.gist or "").strip()
    token = (args.key or "").strip()
    if not link or "/" not in link:
        print("need -g username/gist_id or env GIST_LINK", file=sys.stderr)
        return 2
    if not token:
        print("need -k token or env GIST_PAT", file=sys.stderr)
        return 2
    gist_id = link.split("/", 1)[1].strip()

    keywords = load_keywords(args.brands)
    pat = compile_pattern(keywords)
    domains: set[str] = set()
    if args.domains and os.path.isfile(args.domains):
        with open(args.domains, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip().lower()
                if line and not line.startswith("#"):
                    domains.add(line)

    candidates = [
        args.input,
        os.path.join(DATA, "clash.yaml"),
        os.path.join(ROOT, "subconverter", "proxies.yaml"),
    ]
    proxies: list[dict] = []
    used = ""
    for p in candidates:
        proxies = load_proxies(p)
        if proxies:
            used = p
            break
    if not proxies:
        print("no proxies found; skip mainstream split", file=sys.stderr)
        return 0

    main_nodes = [p for p in proxies if is_mainstream(p, pat, domains)]
    print(f"source={used} total={len(proxies)} mainstream={len(main_nodes)} keywords={len(keywords)}")

    out_path = os.path.join(args.outdir, "mainstream-clash.yaml")
    content = dump_clash(out_path, main_nodes)
    names = "\n".join(str(p.get("name") or "") for p in main_nodes)
    files = {
        "mainstream-clash.yaml": content or "proxies: []\n",
        "mainstream-list.txt": (names + "\n") if names else "# empty\n",
    }
    ok = gist_patch(token, gist_id, files)
    print("gist mainstream upload:", "ok" if ok else "failed")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
