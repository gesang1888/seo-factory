#!/usr/bin/env python3
"""Allow AI search crawlers on every Cloudflare zone in this account.

Cloudflare has no "allow" enum for these fields. 放行 means:

  ai_bots_protection = disabled   # dashboard: Block AI bots = Off
  ai_search           = disabled   # ChatGPT / Perplexity / Claude search
  ai_user             = disabled   # ChatGPT-User / Claude-User fetches
  ai_training         = disabled   # GPTBot / ClaudeBot training crawlers
  is_robots_txt_managed = false    # keep origin robots.txt

Auth:
  export CLOUDFLARE_API_TOKEN='...'          # Account token with Bot Management Write
  export CLOUDFLARE_ACCOUNT_ID='...'         # optional; used to verify account tokens

Usage:
  python3 scripts/cloudflare_allow_ai_search.py --dry-run
  python3 scripts/cloudflare_allow_ai_search.py
  python3 scripts/cloudflare_allow_ai_search.py --zone bbdbuyeu.net
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed

API = "https://api.cloudflare.com/client/v4"
ALLOW_BODY = {
    "ai_bots_protection": "disabled",
    "ai_search": "disabled",
    "ai_user": "disabled",
    "ai_training": "disabled",
    "is_robots_txt_managed": False,
}


def _headers() -> dict[str, str]:
    token = os.environ.get("CLOUDFLARE_API_TOKEN", "").strip()
    if not token:
        print("Set CLOUDFLARE_API_TOKEN", file=sys.stderr)
        sys.exit(1)
    return {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}


def _request(method: str, path: str, body: dict | None = None, attempt: int = 0) -> dict:
    data = None if body is None else json.dumps(body).encode()
    req = urllib.request.Request(f"{API}{path}", data=data, headers=_headers(), method=method)
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as exc:
        if exc.code in (429, 500, 502, 503) and attempt < 4:
            time.sleep(2**attempt)
            return _request(method, path, body, attempt + 1)
        payload = exc.read().decode(errors="replace")
        try:
            return json.loads(payload)
        except json.JSONDecodeError:
            return {"success": False, "errors": [{"message": payload[:300]}]}


def verify_token() -> None:
    account = os.environ.get("CLOUDFLARE_ACCOUNT_ID", "").strip()
    if account:
        res = _request("GET", f"/accounts/{account}/tokens/verify")
        if res.get("success"):
            return
    res = _request("GET", "/user/tokens/verify")
    if res.get("success"):
        return
    err = (res.get("errors") or [{}])[0].get("message", "auth failed")
    print(f"Cloudflare auth failed: {err}", file=sys.stderr)
    sys.exit(1)


def list_zones() -> list[dict]:
    zones: list[dict] = []
    page = 1
    while True:
        res = _request("GET", f"/zones?per_page=50&page={page}")
        if not res.get("success"):
            err = (res.get("errors") or [{}])[0].get("message", "list zones failed")
            print(err, file=sys.stderr)
            sys.exit(1)
        batch = res.get("result") or []
        zones.extend(batch)
        info = res.get("result_info") or {}
        total = int(info.get("total_count") or len(zones))
        if len(zones) >= total or not batch:
            break
        page += 1
    return zones


def already_allowed(bot: dict) -> bool:
    return (
        bot.get("ai_bots_protection") == "disabled"
        and bot.get("ai_search") == "disabled"
        and bot.get("ai_user") == "disabled"
        and bot.get("ai_training") == "disabled"
        and bot.get("is_robots_txt_managed") is False
    )


def apply_zone(zone: dict, dry_run: bool) -> dict:
    name = zone["name"]
    zid = zone["id"]
    current = _request("GET", f"/zones/{zid}/bot_management")
    bot = current.get("result") or {}
    if already_allowed(bot):
        return {"name": name, "status": "already", "bots": bot.get("ai_bots_protection")}
    if dry_run:
        return {
            "name": name,
            "status": "would-update",
            "bots": bot.get("ai_bots_protection"),
            "search": bot.get("ai_search"),
            "training": bot.get("ai_training"),
            "robots_managed": bot.get("is_robots_txt_managed"),
        }
    res = _request("PUT", f"/zones/{zid}/bot_management", ALLOW_BODY)
    updated = res.get("result") or {}
    ok = bool(res.get("success") and already_allowed(updated))
    return {
        "name": name,
        "status": "updated" if ok else "fail",
        "bots": updated.get("ai_bots_protection"),
        "err": res.get("errors"),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--zone", help="Only this zone name")
    parser.add_argument("--workers", type=int, default=6)
    args = parser.parse_args()
    verify_token()
    zones = list_zones()
    if args.zone:
        zones = [z for z in zones if z.get("name") == args.zone]
        if not zones:
            print(f"zone not found: {args.zone}", file=sys.stderr)
            sys.exit(1)
    print(f"zones {len(zones)} dry_run={args.dry_run}")
    rows: list[dict] = []
    with ThreadPoolExecutor(max_workers=max(1, args.workers)) as pool:
        futs = [pool.submit(apply_zone, z, args.dry_run) for z in zones]
        for i, fut in enumerate(as_completed(futs), 1):
            row = fut.result()
            rows.append(row)
            print(f"{row['status']}\t{row['name']}\tbots={row.get('bots')}")
            if i % 40 == 0:
                print(f"# progress {i}/{len(zones)}", file=sys.stderr)
    counts: dict[str, int] = {}
    for row in rows:
        counts[row["status"]] = counts.get(row["status"], 0) + 1
    print(json.dumps(counts))
    if any(r["status"] == "fail" for r in rows):
        sys.exit(1)


if __name__ == "__main__":
    main()
