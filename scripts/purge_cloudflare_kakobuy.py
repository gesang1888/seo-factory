#!/usr/bin/env python3
"""Purge Cloudflare cache for all Kakobuy cluster domains.

Auth:
  export CLOUDFLARE_API_TOKEN='...'   # account (cfat_) or user token
  export CLOUDFLARE_ACCOUNT_ID='...'  # optional; needed to verify account tokens

Usage:
  python3 scripts/purge_cloudflare_kakobuy.py
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from cloudflare_account import request, verify_token, zone_id  # noqa: E402

DOMAINS = [
    "kakospreadsheet.es",
    "kakospreadsheet.fr",
    "kakospreadsheet.ca",
    "kakospreadsheet.nl",
    "kakobuy.fi",
    "kakospreadsheets.es",
    "kakospreadsheets.fr",
    "kakospreadsheets.nl",
    "kakospreadsheets.ca",
]

def purge_domain(domain: str) -> tuple[bool, str]:
    zid = zone_id(domain)
    if not zid:
        return False, "zone not found in this Cloudflare account"
    res = request("POST", f"/zones/{zid}/purge_cache", {"purge_everything": True})
    if res.get("success"):
        return True, "purged"
    err = (res.get("errors") or [{}])[0].get("message", "unknown error")
    return False, err


def main() -> None:
    verify_token()

    ok = 0
    for domain in DOMAINS:
        success, msg = purge_domain(domain)
        status = "OK" if success else "FAIL"
        print(f"{status}\t{domain}\t{msg}")
        if success:
            ok += 1
    print(f"\nPurged {ok}/{len(DOMAINS)} zones")
    sys.exit(0 if ok == len(DOMAINS) else 1)


if __name__ == "__main__":
    main()
