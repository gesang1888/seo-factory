#!/usr/bin/env python3
"""Submit LitBuy desk sitemaps and request Indexing API URL_UPDATED.

Requires the GSC service account to be siteOwner on each sc-domain property.
Does not index unique dests we do not control, parked TLDs, or CH/BE.
"""
from __future__ import annotations

import os
import sys
import time

SA = os.environ.get("GSC_SA_JSON", "/tmp/hipobuy-creds/sa.json")
SCOPES = [
    "https://www.googleapis.com/auth/webmasters",
    "https://www.googleapis.com/auth/indexing",
]

# Same order as tools/litbuy_desks.py ORDER
HOSTS = [
    ("at", "litbuy.at", ["hilfe", "neuigkeiten", "ueber-uns"]),
    ("ca", "litbuyspreadsheets.ca", ["help", "news", "who-we-are"]),
    ("it", "litbuyspreadsheet.it", ["aiuto", "novita", "chi-siamo"]),
    ("eu", "litbuyspreadsheet.eu", ["help", "news", "who-we-are"]),
    ("es", "litbuyspreadsheets.es", ["ayuda", "novedades", "sobre-nosotros"]),
    ("fr", "litspreadsheet.fr", ["aide", "actualites", "a-propos"]),
    ("us", "litbuyspreadsheets.us", ["help", "news", "who-we-are"]),
    ("nl", "litbuyspreadsheets.nl", ["hulp", "nieuws", "over-ons"]),
    ("uk", "litbuyspreadsheet.me.uk", ["help", "news", "who-we-are"]),
    ("now", "litbuyspreadsheetnow.com", ["help", "news", "who-we-are"]),
]


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


def _urls(host: str, slugs: list[str]) -> list[str]:
    out = [f"https://{host}/"]
    for slug in slugs:
        out.append(f"https://{host}/{slug.strip('/')}/")
    return out


def main() -> None:
    gsc, idx = _build()
    listed = {row["siteUrl"]: row.get("permissionLevel") for row in gsc.sites().list().execute().get("siteEntry", [])}
    ok = fail = skip = 0
    for key, host, slugs in HOSTS:
        site = f"sc-domain:{host}"
        perm = listed.get(site) or listed.get(f"https://{host}/")
        use = site if site in listed else (f"https://{host}/" if f"https://{host}/" in listed else None)
        if not use:
            print("MISSING", host)
            skip += 1
            continue
        if perm and perm != "siteOwner":
            print("NOT_OWNER", host, perm)
            skip += 1
            continue
        for feed in (f"https://{host}/sitemap.xml",):
            try:
                gsc.sitemaps().submit(siteUrl=use, feedpath=feed).execute()
                print("SITEMAP", host, feed)
            except Exception as exc:  # noqa: BLE001
                print("SITEMAP_FAIL", host, feed, type(exc).__name__, exc)
        for url in _urls(host, slugs):
            try:
                idx.urlNotifications().publish(body={"url": url, "type": "URL_UPDATED"}).execute()
                print("OK", url)
                ok += 1
            except Exception as exc:  # noqa: BLE001
                print("FAIL", url, type(exc).__name__, exc)
                fail += 1
            time.sleep(0.15)
    print("done ok", ok, "fail", fail, "skip", skip)


if __name__ == "__main__":
    main()
