#!/usr/bin/env python3
"""Read Google Search Console with the gitignored service account.

Credentials: data/gsc/service_account.json  (never commit)

Usage:
  python3 scripts/gsc_service_account.py --list
  python3 scripts/gsc_service_account.py --inspect https://cssbuy.nl/
  python3 scripts/gsc_service_account.py --analytics sc-domain:cssbuy.nl --days 28
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import date, timedelta
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
SA_PATH = ROOT / "data" / "gsc" / "service_account.json"
# Full webmaster scope: analytics is readonly-capable, URL Inspection is not.
SCOPES = ["https://www.googleapis.com/auth/webmasters"]


def _service():
    try:
        from google.oauth2 import service_account
        from googleapiclient.discovery import build
    except ImportError:
        import subprocess

        subprocess.check_call(
            [
                sys.executable,
                "-m",
                "pip",
                "install",
                "google-api-python-client",
                "google-auth",
                "-q",
            ]
        )
        from google.oauth2 import service_account
        from googleapiclient.discovery import build

    if not SA_PATH.is_file():
        print(f"Missing {SA_PATH}", file=sys.stderr)
        sys.exit(1)
    creds = service_account.Credentials.from_service_account_file(
        str(SA_PATH), scopes=SCOPES
    )
    return build("searchconsole", "v1", credentials=creds, cache_discovery=False)


def list_sites(service) -> list[dict]:
    res = service.sites().list().execute()
    return res.get("siteEntry", [])


def inspect_url(service, url: str, site_url: str | None = None) -> dict:
    if not site_url:
        host = urlparse(url).netloc
        site_url = f"https://{host}/"
    body = {"inspectionUrl": url, "siteUrl": site_url}
    return service.urlInspection().index().inspect(body=body).execute()


def query_analytics(service, site_url: str, days: int = 28) -> dict:
    end = date.today() - timedelta(days=1)
    start = end - timedelta(days=days - 1)
    body = {
        "startDate": start.isoformat(),
        "endDate": end.isoformat(),
        "dimensions": ["page"],
        "rowLimit": 25,
    }
    return service.searchanalytics().query(siteUrl=site_url, body=body).execute()


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--list", action="store_true")
    p.add_argument("--inspect", metavar="URL")
    p.add_argument("--site-url", help="GSC property, e.g. sc-domain:cssbuy.nl or https://cssbuy.nl/")
    p.add_argument("--analytics", metavar="SITE_URL")
    p.add_argument("--days", type=int, default=28)
    args = p.parse_args()
    if not (args.list or args.inspect or args.analytics):
        p.print_help()
        return 1

    svc = _service()
    if args.list:
        sites = list_sites(svc)
        print(json.dumps(sites, indent=2))
        print(f"# {len(sites)} properties", file=sys.stderr)
    if args.inspect:
        try:
            res = inspect_url(svc, args.inspect, args.site_url)
            print(json.dumps(res, indent=2))
        except Exception as exc:
            print(f"FAIL inspect {args.inspect}: {exc}", file=sys.stderr)
            return 2
    if args.analytics:
        try:
            res = query_analytics(svc, args.analytics, args.days)
            print(json.dumps(res, indent=2))
        except Exception as exc:
            print(f"FAIL analytics {args.analytics}: {exc}", file=sys.stderr)
            return 3
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
