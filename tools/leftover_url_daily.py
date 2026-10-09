#!/usr/bin/env python3
"""Daily Indexing API URL_UPDATED for unique leftover hub homepages.

Mirrors tools/dest_url_daily.py (PR #78) but only unique leftover apex `/`
URLs — never a sitemap dump (ootdbuyspreadsheet.net sitemap is 316 locs).

Pacific midnight quota is shared with dest (~200 Publish/day). Default
limit 30 so dest remaining (PR #78, remaining_n 636 as of 2026-10-09)
still gets the rest of the day. Timer should fire at 07:00 UTC, 15
minutes before dest-url-daily (15 7 * * *).

Does not PUT pages. Does not 301 twins. Skips hipobuy.es (not ours),
repsicon.com, cssbuy.co.uk, cssbuyspreadsheet.de.
"""
from __future__ import annotations

import json
import os
import sys
import time
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
QUEUE = ROOT / "data" / "leftover-url-daily-queue.json"
LOG = ROOT / "data" / "leftover-url-daily-log.json"
DAILY_LIMIT = int(os.environ.get("LEFTOVER_URL_DAILY_LIMIT", "30"))

# Unique leftover CMS homes (SKIP_UNIQUE after PRs #102–#108) plus the
# HipoBuy unique PHP twin. Newest unique PUT first so a tiny daily cap
# still recrawls today's unique homes.
UNIQUE_HOSTS = (
    "cssbuyspreadsheet.eu",
    "fansbuy.eu",
    "kakobuydocs.com",
    "lovegobuyspreadsheet.eu",
    "lovegobuyguide.com",
    "ootdbuyspreadsheet.net",
    "mycnboxhaul.com",
    "hipobuyreview.com",
    "fansbuysheets.net",
    "mycnbox.eu",
    "bestlolobuyspreadsheet.com",
    "ossbuyspreadsheets.org",
    "hipobuyspreadsheet.net",
    "basetaospreadsheet.com",
    "boonspreadsheet.com",
    "cnshopper.net",
    "fishgoospreadsheet.net",
    "goatedspreadsheet.com",
    "pikospreadsheets.net",
    "lolospreadsheet.com",
    "eastmallspreadsheet.com",
    "fsbuyspreadsheets.com",
    "gtspreadsheet.com",
    "itaobuyspreadsheet.net",
    "pingubuyspreadsheet.net",
    "spanbuyspreadsheets.com",
)

SKIP_HOSTS = {
    "hipobuy.es",
    "repsicon.com",
    "cssbuy.co.uk",
    "cssbuyspreadsheet.de",
    "sugargoo.ca",
    "sugargoo.es",
    "hipobuy.us",
}


def _norm(url: str) -> str:
    url = url.strip()
    if not url.endswith("/") and "?" not in url and "#" not in url:
        path = urlparse(url).path or "/"
        if path != "/" and "." not in path.rsplit("/", 1)[-1]:
            url += "/"
    return url


def _load_ok() -> set[str]:
    ok: set[str] = set()
    if not LOG.exists():
        return ok
    log = json.loads(LOG.read_text())
    for day in log.get("days") or []:
        for url in day.get("index_ok") or []:
            if isinstance(url, str):
                ok.add(_norm(url))
                ok.add(url.rstrip("/"))
    return ok


def _home(host: str) -> str:
    return f"https://{host}/"


def build_queue() -> dict:
    ok = _load_ok()
    rows: list[dict] = []
    for host in UNIQUE_HOSTS:
        if host in SKIP_HOSTS or host.endswith(".cheap"):
            continue
        loc = _norm(_home(host))
        if loc in ok or loc.rstrip("/") in ok:
            continue
        rows.append(
            {
                "url": loc,
                "host": host,
                "band": "home",
                "band_i": 0,
                "sub": 0,
                "path": "/",
            }
        )
    payload = {
        "built": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "note": "unique leftover apex homes only; not a sitemap dump",
        "remaining_n": len(rows),
        "by_band": dict(Counter(r["band"] for r in rows)),
        "remaining": rows,
    }
    QUEUE.parent.mkdir(parents=True, exist_ok=True)
    QUEUE.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print("queue", payload["remaining_n"], payload["by_band"])
    return payload


def _idx():
    try:
        from google.oauth2 import service_account
        from googleapiclient.discovery import build
    except ImportError:
        import subprocess

        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "google-api-python-client", "google-auth", "-q"]
        )
        from google.oauth2 import service_account
        from googleapiclient.discovery import build

    sa = os.environ.get("GSC_SA_JSON", "/tmp/hipobuy-creds/sa.json")
    creds = service_account.Credentials.from_service_account_file(
        sa, scopes=["https://www.googleapis.com/auth/indexing"]
    )
    return build("indexing", "v3", credentials=creds, cache_discovery=False)


def status() -> dict:
    if not QUEUE.exists():
        payload = build_queue()
    else:
        payload = json.loads(QUEUE.read_text())
    remaining = payload.get("remaining") or []
    preview = [r.get("url") for r in remaining[: DAILY_LIMIT]]
    out = {
        "remaining_n": payload.get("remaining_n", len(remaining)),
        "by_band": payload.get("by_band") or {},
        "daily_limit": DAILY_LIMIT,
        "would_submit": preview,
        "would_submit_n": len(preview),
    }
    print(
        "status remaining",
        out["remaining_n"],
        out["by_band"],
        "limit",
        DAILY_LIMIT,
        "next",
        out["would_submit_n"],
    )
    for url in preview:
        print("NEXT", url)
    return out


def run() -> dict:
    if not QUEUE.exists() or not json.loads(QUEUE.read_text()).get("remaining"):
        build_queue()
    payload = json.loads(QUEUE.read_text())
    remaining: list[dict] = payload.get("remaining") or []
    if not remaining:
        print("empty leftover unique-home queue")
        return {
            "day": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
            "index_ok": [],
            "index_fail": [],
            "quota_stopped": False,
            "by_band": {},
            "remaining_n": 0,
        }

    idx = _idx()
    day = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    result = {
        "day": day,
        "index_ok": [],
        "index_fail": [],
        "quota_stopped": False,
        "by_band": Counter(),
    }

    def ping(url: str) -> bool:
        try:
            idx.urlNotifications().publish(body={"url": url, "type": "URL_UPDATED"}).execute()
            print("INDEX", url)
            result["index_ok"].append(url)
            return True
        except Exception as exc:  # noqa: BLE001
            msg = str(exc)
            print("INDEX_FAIL", url, type(exc).__name__, msg[:180])
            result["index_fail"].append({"url": url, "error": msg[:240]})
            if "Quota" in msg or "quota" in msg or "rateLimitExceeded" in msg or "429" in msg:
                result["quota_stopped"] = True
                return False
            return True

    kept: list[dict] = []
    for i, row in enumerate(remaining):
        if result["quota_stopped"] or len(result["index_ok"]) >= DAILY_LIMIT:
            kept.extend(remaining[i:])
            break
        if not ping(row["url"]):
            kept.extend(remaining[i:])
            break
        result["by_band"][row["band"]] += 1
        time.sleep(0.12)
    else:
        kept = []

    payload["remaining"] = kept
    payload["remaining_n"] = len(kept)
    payload["by_band"] = dict(Counter(r["band"] for r in kept))
    payload["updated"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    QUEUE.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")

    log = {"days": []}
    if LOG.exists():
        log = json.loads(LOG.read_text())
    entry = {
        "day": day,
        "index_ok_n": len(result["index_ok"]),
        "index_fail_n": len(result["index_fail"]),
        "quota_stopped": result["quota_stopped"],
        "by_band": dict(result["by_band"]),
        "index_ok": result["index_ok"],
        "index_fail": result["index_fail"],
        "remaining_n": payload["remaining_n"],
        "remaining_by_band": payload["by_band"],
    }
    log.setdefault("days", []).append(entry)
    LOG.write_text(json.dumps(log, indent=2) + "\n", encoding="utf-8")
    print(
        "day",
        day,
        "ok",
        len(result["index_ok"]),
        "fail",
        len(result["index_fail"]),
        "quota",
        result["quota_stopped"],
        "remaining",
        payload["remaining_n"],
        payload["by_band"],
    )
    return result


def main() -> None:
    cmd = sys.argv[1] if len(sys.argv) > 1 else "run"
    if cmd == "build":
        build_queue()
    elif cmd == "status":
        status()
    elif cmd == "run":
        run()
    else:
        raise SystemExit("usage: leftover_url_daily.py [build|status|run]")


if __name__ == "__main__":
    main()
