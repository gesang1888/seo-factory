#!/usr/bin/env python3
"""Purge Cloudflare cache. Account tokens (cfat_) are supported.

  export CLOUDFLARE_API_TOKEN='...'
  python3 scripts/purge_cloudflare.py cssbuy.nl bbdbuy.uk
  python3 scripts/purge_cloudflare.py --p0b
"""

from __future__ import annotations

import argparse
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed

sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parent))
from cloudflare_account import request, verify_token, zone_id  # noqa: E402

P0B = [
    "cssbuyspreadsheet.nl",
    "cssbuyspreadsheet.es",
    "cssbuyspreadsheet.fr",
    "cssbuyspreadsheet.it",
    "cssbuy.nl",
    "cssbuy.es",
    "cssbuy.fr",
    "cssbuy.it",
    "cssbuy.at",
    "cssbuyspreadsheets.de",
    "cssbuyspreadsheets.us",
    "cssbuyspreadsheet.ca",
    "cssbuyspreadsheet.uk",
    "cssbuyspreadsheet.eu",
    "bbdbuy.uk",
    "bbdbuy.us",
    "bbdbuy.ca",
    "bbdbuyspreadsheet.uk",
    "bbdbuyspreadsheet.us",
    "bbdbuyspreadsheet.ca",
    "usfansspreadsheet.co.uk",
    "usfansspreadsheet.nl",
    "usfansspreadsheet.uk",
    "usfansspreadsheet.net",
    "fashionrepsfind.com",
    "fashionrepsspreadsheet.com",
    "hipobuyreview.com",
    "hipobuyspreadsheet.net",
]


def purge_domain(domain: str) -> tuple[str, bool, str]:
    zid = zone_id(domain)
    if not zid:
        return domain, False, "zone not found"
    res = request("POST", f"/zones/{zid}/purge_cache", {"purge_everything": True})
    if res.get("success"):
        return domain, True, "purged"
    err = (res.get("errors") or [{}])[0].get("message", "unknown error")
    return domain, False, err


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("domains", nargs="*")
    parser.add_argument("--p0b", action="store_true", help="Purge evasion P0/P0b hosts")
    parser.add_argument("--workers", type=int, default=6)
    args = parser.parse_args()
    domains = list(args.domains)
    if args.p0b:
        domains.extend(P0B)
    domains = list(dict.fromkeys(domains))
    if not domains:
        parser.print_help()
        return 1
    verify_token()
    ok = 0
    with ThreadPoolExecutor(max_workers=max(1, args.workers)) as pool:
        futs = [pool.submit(purge_domain, d) for d in domains]
        for fut in as_completed(futs):
            domain, success, msg = fut.result()
            print(f"{'OK' if success else 'FAIL'}\t{domain}\t{msg}")
            if success:
                ok += 1
    print(f"\nPurged {ok}/{len(domains)} zones")
    return 0 if ok == len(domains) else 1


if __name__ == "__main__":
    raise SystemExit(main())
