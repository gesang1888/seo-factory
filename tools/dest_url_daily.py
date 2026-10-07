#!/usr/bin/env python3
"""Daily Indexing API URL_UPDATED for the 84 dest sitemaps, importance order.

Order: unpinged homepages, /start/, desk IA (catalog → guide → shipping →
help → news → about), ranked keep, other, blog, legal.
Skips already-ok URLs, joyagoospreadsheets.de (no GSC SA), hubs, .cheap.
Stops at ~200 publishes or first 429. Does not PUT pages.
"""
from __future__ import annotations

import json
import os
import re
import sys
import time
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
SM_DIR = ROOT / "data" / "dest-sitemaps"
QUEUE = ROOT / "data" / "dest-url-daily-queue.json"
LOG = ROOT / "data" / "dest-url-daily-log.json"
DAILY_LIMIT = int(os.environ.get("DEST_URL_DAILY_LIMIT", "200"))
SKIP_HOSTS = {
    "joyagoospreadsheets.de",  # SA not siteOwner
    "repsicon.com",
    "sugargoo.ca",
    "sugargoo.es",
    "hipobuy.us",
    "hipobuy.es",
    "cssbuy.co.uk",
    "cssbuyspreadsheet.de",
    "bbdbuyeu.net",
}
PRIOR_OK = [
    Path("/tmp/dest-gsc-remain.json"),
    Path("/tmp/dest-gsc-submit.json"),
    Path("/tmp/dest-gsc-submit-day2.json"),
    Path("/tmp/dest-gsc-submit-day3.json"),
    Path("/tmp/dest-gsc-submit-day4.json"),
    Path("/tmp/dest-gsc-submit-day5.json"),
]

DESK_SUB = [
    ("catalog", ("/catalog/", "/catalogus/", "/katalog/", "/catalogo/", "/catalogue/")),
    ("guide", ("/how-to-use-", "/handleiding/", "/anleitung/", "/guia/", "/guide/")),
    ("shipping", ("/shipping", "/verzending/", "/versand/", "/envio", "/envoi", "/spedizione", "/freight")),
    ("help", ("/help/", "/hulp/", "/hilfe/", "/ayuda/", "/aide/", "/aiuto/")),
    ("news", ("/news/", "/nieuws/", "/aktuelles/", "/noticias/", "/actualites/", "/notizie/", "/neuigkeiten/")),
    ("about", ("/about/", "/over-ons/", "/ueber-uns/", "/sobre-nosotros/", "/a-propos/", "/chi-siamo/")),
]


def _norm(url: str) -> str:
    url = url.strip()
    if not url.endswith("/") and "?" not in url and "#" not in url:
        path = urlparse(url).path or "/"
        if path != "/" and "." not in path.rsplit("/", 1)[-1]:
            url += "/"
    return url


def _load_ok() -> set[str]:
    ok: set[str] = set()
    for path in PRIOR_OK:
        if not path.exists():
            continue
        data = json.loads(path.read_text())
        if isinstance(data, dict):
            for key in ("already_ok", "index_ok"):
                for url in data.get(key) or []:
                    if isinstance(url, str):
                        ok.add(_norm(url))
                        ok.add(url.rstrip("/"))
    if LOG.exists():
        log = json.loads(LOG.read_text())
        for day in log.get("days") or []:
            for url in day.get("index_ok") or []:
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


def build_queue() -> dict:
    ok = _load_ok()
    rows: list[dict] = []
    for xml in sorted(SM_DIR.glob("*.xml")):
        host = xml.name[: -len(".xml")]
        if host in SKIP_HOSTS or host.endswith(".cheap"):
            continue
        for loc in re.findall(r"<loc>([^<]+)</loc>", xml.read_text()):
            loc = _norm(loc)
            host_loc = urlparse(loc).netloc.lower().removeprefix("www.")
            if host_loc != host.lower().removeprefix("www."):
                continue
            if loc in ok or loc.rstrip("/") in ok:
                continue
            path = urlparse(loc).path or "/"
            band_i, band, sub = _band(path)
            rows.append({"url": loc, "host": host, "band": band, "band_i": band_i, "sub": sub, "path": path})
    rows.sort(key=lambda r: (r["band_i"], r["sub"], r["host"], r["path"]))
    payload = {
        "built": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "remaining_n": len(rows),
        "by_band": dict(Counter(r["band"] for r in rows)),
        "remaining": rows,
    }
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


def run() -> dict:
    if not QUEUE.exists() or not json.loads(QUEUE.read_text()).get("remaining"):
        build_queue()
    payload = json.loads(QUEUE.read_text())
    remaining: list[dict] = payload.get("remaining") or []
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
    elif cmd == "run":
        run()
    else:
        raise SystemExit("usage: dest_url_daily.py [build|run]")


if __name__ == "__main__":
    main()
