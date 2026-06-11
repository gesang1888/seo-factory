#!/usr/bin/env python3
"""Purge Cloudflare cache for all Kakobuy cluster domains.

Auth (pick one):
  export CLOUDFLARE_API_TOKEN='...'   # recommended (Zone.Cache Purge)
  # or
  export CLOUDFLARE_EMAIL='...'
  export CLOUDFLARE_API_KEY='...'

Usage:
  python3 scripts/purge_cloudflare_kakobuy.py
"""

from __future__ import annotations

import json
import os
import sys
import urllib.error
import urllib.request

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

API = "https://api.cloudflare.com/client/v4"


def _headers() -> dict[str, str]:
    token = os.environ.get("CLOUDFLARE_API_TOKEN", "").strip()
    if token:
        return {"Authorization": f"Bearer {token}"}
    email = os.environ.get("CLOUDFLARE_EMAIL", "").strip()
    key = os.environ.get("CLOUDFLARE_API_KEY", "").strip()
    if email and key:
        return {"X-Auth-Email": email, "X-Auth-Key": key}
    print(
        "Set CLOUDFLARE_API_TOKEN or CLOUDFLARE_EMAIL + CLOUDFLARE_API_KEY",
        file=sys.stderr,
    )
    sys.exit(1)


def _request(method: str, path: str, body: dict | None = None) -> dict:
    data = None
    headers = _headers()
    headers["Content-Type"] = "application/json"
    if body is not None:
        data = json.dumps(body).encode()
    req = urllib.request.Request(f"{API}{path}", data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as exc:
        payload = exc.read().decode(errors="replace")
        try:
            return json.loads(payload)
        except json.JSONDecodeError:
            return {"success": False, "errors": [{"message": payload[:300]}]}


def zone_id(domain: str) -> str | None:
    res = _request("GET", f"/zones?name={domain}")
    if not res.get("success"):
        return None
    zones = res.get("result") or []
    return zones[0]["id"] if zones else None


def purge_domain(domain: str) -> tuple[bool, str]:
    zid = zone_id(domain)
    if not zid:
        return False, "zone not found in this Cloudflare account"
    res = _request("POST", f"/zones/{zid}/purge_cache", {"purge_everything": True})
    if res.get("success"):
        return True, "purged"
    err = (res.get("errors") or [{}])[0].get("message", "unknown error")
    return False, err


def main() -> None:
    verify = _request("GET", "/user/tokens/verify")
    if not verify.get("success"):
        verify = _request("GET", "/user")
    if not verify.get("success"):
        err = (verify.get("errors") or [{}])[0].get("message", "auth failed")
        print(f"Cloudflare auth failed: {err}", file=sys.stderr)
        sys.exit(1)

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
