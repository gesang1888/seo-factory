#!/usr/bin/env python3
"""Submit Kakobuy cluster sitemaps to Google Search Console API.

Requires OAuth desktop client JSON (Search Console scope):
  data/gsc/oauth_client.json
  data/gsc/token.json   (created on first run)

Usage:
  python3 scripts/submit_gsc_kakobuy.py --sitemaps
  python3 scripts/submit_gsc_kakobuy.py --inspect-p1
  python3 scripts/submit_gsc_kakobuy.py --sitemaps --inspect-p1
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from urllib.parse import quote, urlparse

ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "sites" / "kakobuy-cluster" / "cluster-config.json"
GSC_DIR = ROOT / "data" / "gsc"
OAUTH_CLIENT = GSC_DIR / "oauth_client.json"
TOKEN_PATH = GSC_DIR / "token.json"
SCOPES = ["https://www.googleapis.com/auth/webmasters"]


def _load_config() -> dict:
    return json.loads(CONFIG.read_text(encoding="utf-8"))


def _site_url(domain: str) -> str:
    return f"https://{domain}/"


def _get_service():
    try:
        from google.auth.transport.requests import Request
        from google.oauth2.credentials import Credentials
        from google_auth_oauthlib.flow import InstalledAppFlow
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
                "google-auth-oauthlib",
                "-q",
            ]
        )
        from google.auth.transport.requests import Request
        from google.oauth2.credentials import Credentials
        from google_auth_oauthlib.flow import InstalledAppFlow
        from googleapiclient.discovery import build

    if not OAUTH_CLIENT.is_file():
        print(f"Missing {OAUTH_CLIENT}", file=sys.stderr)
        print(
            "Create OAuth client (Desktop) in Google Cloud Console, "
            "enable Search Console API, save JSON as data/gsc/oauth_client.json",
            file=sys.stderr,
        )
        sys.exit(1)

    GSC_DIR.mkdir(parents=True, exist_ok=True)
    creds = None
    if TOKEN_PATH.is_file():
        creds = Credentials.from_authorized_user_file(str(TOKEN_PATH), SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(str(OAUTH_CLIENT), SCOPES)
            creds = flow.run_local_server(port=0)
        TOKEN_PATH.write_text(creds.to_json(), encoding="utf-8")
    return build("searchconsole", "v1", credentials=creds)


def submit_sitemaps(service) -> int:
    cfg = _load_config()
    ok = 0
    for sm in cfg.get("gsc_sitemaps", []):
        domain = urlparse(sm).netloc
        site = quote(_site_url(domain), safe="")
        feed = quote(sm.replace(f"https://{domain}/", ""), safe="")
        try:
            service.sitemaps().submit(siteUrl=_site_url(domain), feedpath=feed).execute()
            print(f"OK\tsitemap\t{sm}")
            ok += 1
        except Exception as exc:
            print(f"FAIL\tsitemap\t{sm}\t{exc}")
    return ok


def inspect_p1(service) -> int:
    cfg = _load_config()
    ok = 0
    for url in cfg.get("gsc_p1_urls", []):
        domain = urlparse(url).netloc
        body = {
            "inspectionUrl": url,
            "siteUrl": _site_url(domain),
        }
        try:
            res = service.urlInspection().index().inspect(body=body).execute()
            verdict = (
                res.get("inspectionResult", {})
                .get("indexStatusResult", {})
                .get("verdict", "UNKNOWN")
            )
            print(f"OK\tinspect\t{url}\t{verdict}")
            ok += 1
        except Exception as exc:
            print(f"FAIL\tinspect\t{url}\t{exc}")
    return ok


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--sitemaps", action="store_true", help="Submit all cluster sitemaps")
    parser.add_argument(
        "--inspect-p1",
        action="store_true",
        help="Run URL Inspection API on P1 URLs (does not request indexing)",
    )
    args = parser.parse_args()
    if not args.sitemaps and not args.inspect_p1:
        parser.print_help()
        sys.exit(1)

    service = _get_service()
    if args.sitemaps:
        n = submit_sitemaps(service)
        print(f"\nSitemaps submitted: {n}")
    if args.inspect_p1:
        n = inspect_p1(service)
        print(f"\nP1 URLs inspected: {n}")


if __name__ == "__main__":
    main()
