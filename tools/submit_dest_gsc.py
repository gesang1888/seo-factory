#!/usr/bin/env python3
"""Submit GSC sitemaps + Indexing API URL_UPDATED for the 48 dest CMS desks.

Homepages first, then HOSTS keep inners, then remaining ranked HTML.
Requires the GSC service account to be siteOwner. Does not print secrets.
"""
from __future__ import annotations

import json
import os
import sys
import time
from pathlib import Path

_TOOLS = Path(__file__).resolve().parent
if str(_TOOLS) not in sys.path:
    sys.path.insert(0, str(_TOOLS))
from hub_skin_desks import HOSTS

SA = os.environ.get("GSC_SA_JSON", "/tmp/hipobuy-creds/sa.json")
SCOPES = [
    "https://www.googleapis.com/auth/webmasters",
    "https://www.googleapis.com/auth/indexing",
]
OUT = Path("/tmp/dest-gsc-submit.json")
INNERS = Path("/tmp/dest-inners.json")


def _build():
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

    creds = service_account.Credentials.from_service_account_file(SA, scopes=SCOPES)
    gsc = build("searchconsole", "v1", credentials=creds, cache_discovery=False)
    idx = build("indexing", "v3", credentials=creds, cache_discovery=False)
    return gsc, idx


def _property(listed: dict, host: str) -> str | None:
    for cand in (f"sc-domain:{host}", f"https://{host}/", f"http://{host}/"):
        if cand in listed:
            return cand
    return None


def _inner_url(host: str, rel: str) -> str:
    rel = rel.lstrip("/")
    if rel.endswith("/index.html"):
        rel = rel[: -len("index.html")]
    elif rel == "index.html":
        rel = ""
    return f"https://{host}/{rel}"


def _priority_urls(host: str, files: list[dict]) -> list[str]:
    seen: set[str] = set()
    out: list[str] = []

    def add(url: str) -> None:
        if url not in seen:
            seen.add(url)
            out.append(url)

    add(f"https://{host}/")
    for path, _lab in HOSTS.get(host, {}).get("keep") or []:
        if path.startswith("http"):
            add(path)
        else:
            add(f"https://{host}{path if path.startswith('/') else '/' + path}")
    for item in files:
        add(_inner_url(host, item["rel"]))
    return out


def main() -> None:
    gsc, idx = _build()
    listed = {
        row["siteUrl"]: row.get("permissionLevel")
        for row in gsc.sites().list().execute().get("siteEntry", [])
    }
    inventory = {row["host"]: row.get("files") or [] for row in json.loads(INNERS.read_text())}
    results = {
        "sitemap_ok": [],
        "sitemap_fail": [],
        "index_ok": [],
        "index_fail": [],
        "missing": [],
        "quota_stopped": False,
    }
    quota_hit = False
    print("GSC properties", len(listed), "dests", len(HOSTS))
    for host in HOSTS:
        use = _property(listed, host)
        perm = listed.get(use) if use else None
        if not use:
            print("MISSING", host)
            results["missing"].append(host)
            continue
        if perm and perm not in ("siteOwner", "siteFullUser"):
            print("NOT_OWNER", host, perm)
            results["missing"].append(host)
            continue
        feed = f"https://{host}/sitemap.xml"
        try:
            gsc.sitemaps().submit(siteUrl=use, feedpath=feed).execute()
            print("SITEMAP", host)
            results["sitemap_ok"].append(host)
        except Exception as exc:  # noqa: BLE001
            print("SITEMAP_FAIL", host, type(exc).__name__, str(exc)[:180])
            results["sitemap_fail"].append({"host": host, "error": str(exc)[:240]})

    waves: list[str] = []
    extras: list[str] = []
    for host in HOSTS:
        urls = _priority_urls(host, inventory.get(host) or [])
        waves.extend(urls[:5])  # homepage + four keep slots
        extras.extend(urls[5:])

    def ping(url: str) -> bool:
        nonlocal quota_hit
        if quota_hit:
            return False
        try:
            idx.urlNotifications().publish(body={"url": url, "type": "URL_UPDATED"}).execute()
            print("INDEX", url)
            results["index_ok"].append(url)
        except Exception as exc:  # noqa: BLE001
            msg = str(exc)
            print("INDEX_FAIL", url, type(exc).__name__, msg[:180])
            results["index_fail"].append({"url": url, "error": msg[:240]})
            if "Quota" in msg or "quota" in msg or "rateLimitExceeded" in msg or "429" in msg:
                quota_hit = True
                results["quota_stopped"] = True
                print("QUOTA stop remaining Indexing API calls")
                return False
        time.sleep(0.12)
        return True

    for url in waves + extras:
        if not ping(url):
            if quota_hit:
                break
    OUT.write_text(json.dumps(results, indent=2), encoding="utf-8")
    print(
        "done sitemap_ok",
        len(results["sitemap_ok"]),
        "sitemap_fail",
        len(results["sitemap_fail"]),
        "index_ok",
        len(results["index_ok"]),
        "index_fail",
        len(results["index_fail"]),
        "missing",
        len(results["missing"]),
        "quota_stopped",
        results["quota_stopped"],
    )
    print("wrote", OUT)


if __name__ == "__main__":
    main()
