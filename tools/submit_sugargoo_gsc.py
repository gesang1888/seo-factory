#!/usr/bin/env python3
"""Submit SugarGoo country-desk sitemaps via Search Console.

Uses the existing GSC service account. Does not enable Indexing API.
Does not submit sugargoo.ca / sugargoo.es / .pt / .cheap.
"""
from __future__ import annotations

import os
import sys

SA = os.environ.get("GSC_SA_JSON", "/tmp/hipobuy-creds/sa.json")
SCOPES = ["https://www.googleapis.com/auth/webmasters"]

HOSTS = [
    "sugargoospreadsheets.us",
    "sugargoospreadsheet.au",
    "sugargoospreadsheets.fr",
    "sugargoospreadsheets2026.ca",
    "sugargoospreadsheetnow.com",
    "sugargoospreadsheets.uk",
    "sugargoospreadsheet.es",
    "sugargoospreadsheets.de",
    "sugargoo.at",
    "sugargoospreadsheets.nl",
]


def _svc():
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
    return build("searchconsole", "v1", credentials=creds, cache_discovery=False)


def _site_url(host: str) -> str:
    return f"sc-domain:{host}"


def main() -> None:
    svc = _svc()
    listed = {row["siteUrl"] for row in svc.sites().list().execute().get("siteEntry", [])}
    for host in HOSTS:
        site = _site_url(host)
        prefix = f"https://{host}/"
        if site not in listed and prefix not in listed:
            print("MISSING", host, "not in this SA property list")
            continue
        use = site if site in listed else prefix
        for feed in (f"https://{host}/sitemap.xml", f"https://{host}/sitemap_index.xml"):
            try:
                svc.sitemaps().submit(siteUrl=use, feedpath=feed).execute()
                print("SUBMIT", use, feed)
            except Exception as exc:  # noqa: BLE001
                print("FAIL", use, feed, type(exc).__name__, exc)


if __name__ == "__main__":
    main()
