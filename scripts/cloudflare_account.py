#!/usr/bin/env python3
"""Cloudflare account-token client.

Account API tokens (cfat_…) verify at /accounts/{id}/tokens/verify.
User tokens verify at /user/tokens/verify. Try account first.

Auth:
  export CLOUDFLARE_API_TOKEN='...'
  export CLOUDFLARE_ACCOUNT_ID='f90658e3c565e505018e02367be592a4'  # optional
"""

from __future__ import annotations

import json
import os
import time
import urllib.error
import urllib.request

API = "https://api.cloudflare.com/client/v4"
DEFAULT_ACCOUNT_ID = "f90658e3c565e505018e02367be592a4"


def headers() -> dict[str, str]:
    token = os.environ.get("CLOUDFLARE_API_TOKEN", "").strip()
    if not token:
        raise SystemExit("Set CLOUDFLARE_API_TOKEN")
    return {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}


def request(method: str, path: str, body: dict | None = None, attempt: int = 0) -> dict:
    data = None if body is None else json.dumps(body).encode()
    req = urllib.request.Request(f"{API}{path}", data=data, headers=headers(), method=method)
    try:
        with urllib.request.urlopen(req, timeout=45) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as exc:
        if exc.code in (429, 500, 502, 503) and attempt < 4:
            time.sleep(2**attempt)
            return request(method, path, body, attempt + 1)
        payload = exc.read().decode(errors="replace")
        try:
            return json.loads(payload)
        except json.JSONDecodeError:
            return {"success": False, "errors": [{"message": payload[:300]}]}


def verify_token() -> dict:
    account = os.environ.get("CLOUDFLARE_ACCOUNT_ID", "").strip() or DEFAULT_ACCOUNT_ID
    res = request("GET", f"/accounts/{account}/tokens/verify")
    if res.get("success"):
        return res
    res = request("GET", "/user/tokens/verify")
    if res.get("success"):
        return res
    err = (res.get("errors") or [{}])[0].get("message", "auth failed")
    raise SystemExit(f"Cloudflare auth failed: {err}")


def list_zones() -> list[dict]:
    zones: list[dict] = []
    page = 1
    while True:
        res = request("GET", f"/zones?per_page=50&page={page}")
        if not res.get("success"):
            err = (res.get("errors") or [{}])[0].get("message", "list zones failed")
            raise SystemExit(err)
        batch = res.get("result") or []
        zones.extend(batch)
        info = res.get("result_info") or {}
        total = int(info.get("total_count") or len(zones))
        if len(zones) >= total or not batch:
            break
        page += 1
    return zones


def zone_id(domain: str) -> str | None:
    res = request("GET", f"/zones?name={domain}")
    if not res.get("success"):
        return None
    zones = res.get("result") or []
    return zones[0]["id"] if zones else None
