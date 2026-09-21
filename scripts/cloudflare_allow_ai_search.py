#!/usr/bin/env python3
"""Allow AI search crawlers on every Cloudflare zone in this account.

Cloudflare has no "allow" enum. 放行 means:

  ai_bots_protection = disabled
  ai_search / ai_user / ai_training = disabled
  is_robots_txt_managed = false

Auth:
  export CLOUDFLARE_API_TOKEN='...'
  export CLOUDFLARE_ACCOUNT_ID='...'   # optional; account tokens need this verify path

Usage:
  python3 scripts/cloudflare_allow_ai_search.py --dry-run
  python3 scripts/cloudflare_allow_ai_search.py
  python3 scripts/cloudflare_allow_ai_search.py --zone bbdbuyeu.net
"""

from __future__ import annotations

import argparse
import json
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from cloudflare_account import list_zones, request, verify_token  # noqa: E402

ALLOW_BODY = {
    "ai_bots_protection": "disabled",
    "ai_search": "disabled",
    "ai_user": "disabled",
    "ai_training": "disabled",
    "is_robots_txt_managed": False,
}


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
    current = request("GET", f"/zones/{zid}/bot_management")
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
    res = request("PUT", f"/zones/{zid}/bot_management", ALLOW_BODY)
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
