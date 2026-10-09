#!/usr/bin/env python3
"""Daily Indexing API URL_UPDATED for unique leftover hubs.

Phase 1 (from 2026-10-10, before dest remaining drains): unique leftover
apex `/` only. Cap 30 so dest remaining (PR #78) still gets the rest of
the Pacific midnight ~200 Publish/day quota.

Phase 2 (from INNER_START 2026-10-15, after 2026-10-14): remaining
sitemap inners in dest-style importance order. Cap 200. Dest remaining
should already be 0; dest-url-daily expires 2026-10-14T02:52Z.

Does not PUT pages. Does not 301 twins. Skips hipobuy.es (not ours),
repsicon.com, cssbuy.co.uk, cssbuyspreadsheet.de.
"""
from __future__ import annotations

import json
import os
import re
import ssl
import sys
import time
import urllib.request
from collections import Counter
from datetime import date, datetime, timezone
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
SM_DIR = ROOT / "data" / "leftover-sitemaps"
QUEUE = ROOT / "data" / "leftover-url-daily-queue.json"
LOG = ROOT / "data" / "leftover-url-daily-log.json"
INNER_START = date.fromisoformat(os.environ.get("LEFTOVER_INNER_START", "2026-10-15"))
HOME_LIMIT = int(os.environ.get("LEFTOVER_URL_DAILY_LIMIT", "30"))
INNER_LIMIT = int(os.environ.get("LEFTOVER_URL_INNER_LIMIT", "200"))

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
HOST_I = {host: i for i, host in enumerate(UNIQUE_HOSTS)}

SKIP_HOSTS = {
    "hipobuy.es",
    "repsicon.com",
    "cssbuy.co.uk",
    "cssbuyspreadsheet.de",
    "sugargoo.ca",
    "sugargoo.es",
    "hipobuy.us",
}

DESK_SUB = [
    ("catalog", ("/catalog/", "/catalogus/", "/katalog/", "/catalogo/", "/catalogue/", "/category/", "/categories/")),
    ("guide", ("/how-to-use-", "/handleiding/", "/anleitung/", "/guia/", "/guide/", "/guides/")),
    ("shipping", ("/shipping", "/verzending/", "/versand/", "/envio", "/envoi", "/spedizione", "/freight")),
    ("help", ("/help/", "/hulp/", "/hilfe/", "/ayuda/", "/aide/", "/aiuto/")),
    ("news", ("/news/", "/nieuws/", "/aktuelles/", "/noticias/", "/actualites/", "/notizie/", "/neuigkeiten/")),
    ("about", ("/about/", "/over-ons/", "/ueber-uns/", "/sobre-nosotros/", "/a-propos/", "/chi-siamo/")),
]


def _today() -> date:
    return datetime.now(timezone.utc).date()


def _inners_open(day: date | None = None) -> bool:
    return (day or _today()) >= INNER_START


def _daily_limit(day: date | None = None) -> int:
    return INNER_LIMIT if _inners_open(day) else HOME_LIMIT


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


def _band(path: str) -> tuple[int, str, int]:
    p = path.lower() or "/"
    if p in ("/", ""):
        return 0, "home", 0
    if p.rstrip("/") == "/start":
        return 1, "start", 0
    for i, (name, needles) in enumerate(DESK_SUB):
        if any(n in p for n in needles) and "/blog/" not in p:
            return 2, "desk", i
    if "/blog/" in p or p.rstrip("/") == "/blog":
        return 5, "blog", 0
    legal = ("/terms", "/privacy", "/affiliate", "/contact", "/cookie", "/dsgvo", "/partner-disclosure")
    if any(n in p for n in legal):
        return 6, "legal", 0
    keep = ("legit", "spreadsheet", "coupon", "/qc", "refund", "community", "invite")
    if any(n in p for n in keep):
        return 3, "keep", 0
    return 4, "other", 0


def fetch_sitemaps() -> None:
    SM_DIR.mkdir(parents=True, exist_ok=True)
    ctx = ssl.create_default_context()
    headers = {"User-Agent": "Mozilla/5.0 leftover-url-daily/1.0"}
    for host in UNIQUE_HOSTS:
        if host in SKIP_HOSTS:
            continue
        url = f"https://{host}/sitemap.xml"
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=25, context=ctx) as resp:
            body = resp.read()
        (SM_DIR / f"{host}.xml").write_bytes(body)
        print("sitemap", host, len(body))


def build_queue() -> dict:
    ok = _load_ok()
    rows: list[dict] = []
    seen: set[str] = set()
    for host in UNIQUE_HOSTS:
        if host in SKIP_HOSTS or host.endswith(".cheap"):
            continue
        xml = SM_DIR / f"{host}.xml"
        locs: list[str] = []
        if xml.exists():
            locs = re.findall(r"<loc>([^<]+)</loc>", xml.read_text(encoding="utf-8", errors="replace"))
        if not locs:
            locs = [f"https://{host}/"]
        for loc in locs:
            loc = _norm(loc)
            host_loc = urlparse(loc).netloc.lower().removeprefix("www.")
            if host_loc != host.lower().removeprefix("www."):
                continue
            if loc in ok or loc.rstrip("/") in ok or loc in seen:
                continue
            seen.add(loc)
            path = urlparse(loc).path or "/"
            band_i, band, sub = _band(path)
            rows.append(
                {
                    "url": loc,
                    "host": host,
                    "band": band,
                    "band_i": band_i,
                    "sub": sub,
                    "path": path,
                    "host_i": HOST_I.get(host, 999),
                }
            )
    rows.sort(key=lambda r: (r["band_i"], r["sub"], r["host_i"], r["path"]))
    by_band = dict(Counter(r["band"] for r in rows))
    payload = {
        "built": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "note": "unique leftover sitemap locs; homes before 2026-10-14, inners from 2026-10-15",
        "inner_start": INNER_START.isoformat(),
        "remaining_n": len(rows),
        "by_band": by_band,
        "remaining": rows,
    }
    QUEUE.parent.mkdir(parents=True, exist_ok=True)
    QUEUE.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print("queue", payload["remaining_n"], payload["by_band"], "inner_start", INNER_START.isoformat())
    return payload


def _eligible(remaining: list[dict], day: date) -> list[dict]:
    if _inners_open(day):
        return remaining
    return [r for r in remaining if r.get("band") == "home"]


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
    day = _today()
    eligible = _eligible(remaining, day)
    limit = _daily_limit(day)
    preview = [r.get("url") for r in eligible[:limit]]
    out = {
        "day": day.isoformat(),
        "inner_start": INNER_START.isoformat(),
        "inners_open": _inners_open(day),
        "remaining_n": payload.get("remaining_n", len(remaining)),
        "eligible_n": len(eligible),
        "by_band": payload.get("by_band") or {},
        "daily_limit": limit,
        "would_submit": preview,
        "would_submit_n": len(preview),
        "waiting": bool(remaining) and not eligible,
    }
    print(
        "status day",
        out["day"],
        "inners_open",
        out["inners_open"],
        "remaining",
        out["remaining_n"],
        out["by_band"],
        "eligible",
        out["eligible_n"],
        "limit",
        limit,
        "waiting",
        out["waiting"],
    )
    for url in preview:
        print("NEXT", url)
    if out["waiting"]:
        print("WAIT leftover inners start", INNER_START.isoformat(), "after 2026-10-14; do not ping")
    return out


def run() -> dict:
    if not QUEUE.exists() or not json.loads(QUEUE.read_text()).get("remaining"):
        build_queue()
    payload = json.loads(QUEUE.read_text())
    remaining: list[dict] = payload.get("remaining") or []
    day = _today()
    day_s = day.isoformat()
    eligible = _eligible(remaining, day)
    limit = _daily_limit(day)

    if not remaining:
        print("empty leftover unique queue")
        return {
            "day": day_s,
            "index_ok": [],
            "index_fail": [],
            "quota_stopped": False,
            "by_band": {},
            "remaining_n": 0,
            "waiting": False,
        }

    if not eligible:
        print(
            "WAIT leftover inners start",
            INNER_START.isoformat(),
            "after 2026-10-14; remaining",
            len(remaining),
            "do not ping, dest keeps the 200",
        )
        log = {"days": []}
        if LOG.exists():
            log = json.loads(LOG.read_text())
        log.setdefault("days", []).append(
            {
                "day": day_s,
                "waiting": True,
                "inner_start": INNER_START.isoformat(),
                "index_ok_n": 0,
                "index_fail_n": 0,
                "quota_stopped": False,
                "by_band": {},
                "index_ok": [],
                "index_fail": [],
                "remaining_n": len(remaining),
                "remaining_by_band": payload.get("by_band") or dict(Counter(r["band"] for r in remaining)),
            }
        )
        LOG.write_text(json.dumps(log, indent=2) + "\n", encoding="utf-8")
        return {
            "day": day_s,
            "waiting": True,
            "index_ok": [],
            "index_fail": [],
            "quota_stopped": False,
            "remaining_n": len(remaining),
        }

    idx = _idx()
    result = {
        "day": day_s,
        "index_ok": [],
        "index_fail": [],
        "quota_stopped": False,
        "by_band": Counter(),
        "waiting": False,
    }
    eligible_urls = {r["url"] for r in eligible}

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
    pinged = 0
    stopped = False
    for row in remaining:
        if row["url"] not in eligible_urls:
            kept.append(row)
            continue
        if stopped or result["quota_stopped"] or pinged >= limit:
            kept.append(row)
            continue
        if not ping(row["url"]):
            kept.append(row)
            stopped = True
            continue
        result["by_band"][row["band"]] += 1
        pinged += 1
        time.sleep(0.12)

    payload["remaining"] = kept
    payload["remaining_n"] = len(kept)
    payload["by_band"] = dict(Counter(r["band"] for r in kept))
    payload["updated"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    QUEUE.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")

    log = {"days": []}
    if LOG.exists():
        log = json.loads(LOG.read_text())
    entry = {
        "day": day_s,
        "index_ok_n": len(result["index_ok"]),
        "index_fail_n": len(result["index_fail"]),
        "quota_stopped": result["quota_stopped"],
        "by_band": dict(result["by_band"]),
        "index_ok": result["index_ok"],
        "index_fail": result["index_fail"],
        "remaining_n": payload["remaining_n"],
        "remaining_by_band": payload["by_band"],
        "waiting": False,
        "inner_start": INNER_START.isoformat(),
    }
    log.setdefault("days", []).append(entry)
    LOG.write_text(json.dumps(log, indent=2) + "\n", encoding="utf-8")
    print(
        "day",
        day_s,
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
    if cmd == "fetch":
        fetch_sitemaps()
    elif cmd == "build":
        build_queue()
    elif cmd == "status":
        status()
    elif cmd == "run":
        run()
    else:
        raise SystemExit("usage: leftover_url_daily.py [fetch|build|status|run]")


if __name__ == "__main__":
    main()
