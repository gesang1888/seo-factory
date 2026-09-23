#!/usr/bin/env python3
"""PUT remaining leftover dests; 301 two empty same-family aliases.

PUTs (homepage only; inner CMS/html stays):
  ootdbuyspreadsheet.org / .net, sugargoospreadsheetnow.com,
  sugargoospreadsheets.nl, wemimispreadsheet.com, oopbuyspreadsheets.it,
  hubbuyspreadsheet.net

Path-mapped aliases (dest unique; alias inner 404):
  fansspreadsheets.net → https://fansbuysheets.net
  orientdigspreadsheets.fr → https://orientdig.fr
    /orientdig-spreadsheets/ → /orientdig-spreadsheet/
    unknown → dest /

Never PUT hubbuy.net (11c / 103 KB), hipobuyspreadsheet.net, mulebuy.fr,
sugargoo.es/.nl, wemimi.net (500), orientdig.us, spanbuy/piko/itaobuy indie,
ootd.org onto .net, hubbuyspreadsheet.net onto hubbuy.net (slug mismatch).

  export BT_KEY='...'
  python3 scripts/evasion_remaining_leftovers_apply.py --apply
"""

from __future__ import annotations

import argparse
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from spam_update_p0 import Baota  # noqa: E402

PUTS = {
    "ootdbuyspreadsheet.org": ROOT / "sites/ootdbuyspreadsheet.org/overlay/index.html",
    "ootdbuyspreadsheet.net": ROOT / "sites/ootdbuyspreadsheet.net/overlay/index.html",
    "sugargoospreadsheetnow.com": ROOT
    / "sites/sugargoospreadsheetnow.com/overlay/index.html",
    "sugargoospreadsheets.nl": ROOT / "sites/sugargoospreadsheets.nl/overlay/index.html",
    "wemimispreadsheet.com": ROOT / "sites/wemimispreadsheet.com/overlay/index.html",
    "oopbuyspreadsheets.it": ROOT / "sites/oopbuyspreadsheets.it/overlay/index.html",
    "hubbuyspreadsheet.net": ROOT / "sites/hubbuyspreadsheet.net/overlay/index.html",
}

FANS_PATHS = [
    "blog",
    "fansbuy-community",
    "fansbuy-coupons",
    "fansbuy-invite-code",
    "fansbuy-qc-guide",
    "fansbuy-refund-guide",
    "fansbuy-shipping-guide",
    "fansbuy-shoes-spreadsheet",
    "fansbuy-spreadsheet",
    "fansbuy-spreadsheet-2026",
    "how-to-use-fansbuy",
    "is-fansbuy-legit",
]

OD_FR_PATHS = [
    "how-to-use-orientdig",
    "is-orientdig-legit",
    "is-orientdig-safe",
    "orientdig-shipping",
    "orientdig-spreadsheet",
    "orientdig-coupons",
    "orientdig-finds",
    "orientdig-qc",
    "avis-orientdig",
    "orientdig-discord",
    "orientdig-review",
    "contact",
    "privacy-policy",
    "affiliate-disclosure",
    "partner-disclosure",
    "about",
    "terms",
]
OD_FR_REMAPS = {
    "orientdig-spreadsheets": "orientdig-spreadsheet",
}

ALIASES = {
    "fansspreadsheets.net": ("https://fansbuysheets.net", FANS_PATHS, {}),
    "orientdigspreadsheets.fr": (
        "https://orientdig.fr",
        OD_FR_PATHS,
        OD_FR_REMAPS,
    ),
}


def mapped_locations(
    target_origin: str, slugs: list[str], remaps: dict[str, str] | None = None
) -> str:
    origin = target_origin.rstrip("/")
    lines = []
    seen: set[str] = set()
    for src, dst in (remaps or {}).items():
        dest = dst.strip("/")
        lines.append(f"    location = /{src} {{ return 301 {origin}/{dest}/; }}")
        lines.append(f"    location = /{src}/ {{ return 301 {origin}/{dest}/; }}")
        seen.add(src)
    for slug in slugs:
        if slug in seen:
            continue
        lines.append(f"    location = /{slug} {{ return 301 {origin}/{slug}/; }}")
        lines.append(f"    location = /{slug}/ {{ return 301 {origin}/{slug}/; }}")
    lines.append(f"    location / {{ return 301 {origin}/; }}")
    return "\n".join(lines)


def redirect_conf(
    domain: str,
    target_origin: str,
    slugs: list[str],
    original: str,
    remaps: dict[str, str] | None = None,
) -> str:
    cert = f"/www/server/panel/vhost/cert/{domain}/fullchain.pem"
    key = f"/www/server/panel/vhost/cert/{domain}/privkey.pem"
    m_cert = re.search(r"ssl_certificate\s+(\S+);", original)
    m_key = re.search(r"ssl_certificate_key\s+(\S+);", original)
    if m_cert:
        cert = m_cert.group(1)
    if m_key:
        key = m_key.group(1)
    maps = mapped_locations(target_origin, slugs, remaps)
    return f"""server
{{
    listen 80;
    listen [::]:80;
    listen 443 ssl;
    http2 on;
    server_name {domain} www.{domain};
    include /www/server/panel/vhost/nginx/well-known/{domain}.conf;
    ssl_certificate    {cert};
    ssl_certificate_key    {key};
    ssl_protocols TLSv1.2 TLSv1.3;
    add_header Strict-Transport-Security "max-age=31536000" always;
{maps}
    access_log  /www/wwwlogs/{domain}.log;
    error_log  /www/wwwlogs/{domain}.error.log;
}}
"""


def apply(bt: Baota, dry_run: bool = False) -> None:
    for host, html_path in PUTS.items():
        html = html_path.read_text(encoding="utf-8")
        dest = f"/www/wwwroot/{host}/index.html"
        if dry_run:
            print("dry-run put", dest, "bytes", len(html))
            continue
        print("put", dest, bt.put(dest, html).get("msg", "")[:80])

    for host, (target, slugs, remaps) in ALIASES.items():
        nginx = f"/www/server/panel/vhost/nginx/{host}.conf"
        original = bt.get(nginx) or ""
        backup = nginx + ".bak-evasion-alias"
        new = redirect_conf(host, target, slugs, original, remaps)
        rewrite = f"/www/server/panel/vhost/rewrite/{host}.conf"
        if dry_run:
            print("dry-run 301", host, "→", target, "bytes", len(new))
            continue
        if original and bt.get(backup) is None:
            print("backup", backup, bt.put(backup, original).get("msg", "")[:60])
        print("nginx", host, bt.put(nginx, new).get("msg", "")[:60])
        print(
            "rewrite",
            host,
            bt.put(rewrite, "# evasion: same-country alias 301, path-mapped\n").get(
                "msg", ""
            )[:60],
        )

    if not dry_run:
        print("reload", bt.reload_nginx())


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()
    if not (args.apply or args.dry_run):
        print("Pass --dry-run or --apply (BT_KEY required)")
        return 1
    key = os.environ.get("BT_KEY", "")
    if not key:
        raise SystemExit("BT_KEY required")
    apply(Baota(key), dry_run=args.dry_run)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
