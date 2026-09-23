#!/usr/bin/env python3
"""Evasion P0b: CSSBuy same-country alias 301 (path-mapped) + deepen homepages.

Do not PUT cssbuy.at/es/fr/it/nl (shared PHP app). Inner CMS/tool URLs on
BBDBuy and CSSBuy spreadsheet country hosts stay on disk; only index.html
is replaced. Secrets stay in BT_KEY.
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

# Thin generated homepages sitting in front of unique inner pages.
PUTS = {
    "cssbuyspreadsheets.de": ROOT / "sites/cssbuyspreadsheets.de/overlay/index.html",
    "cssbuyspreadsheet.ca": ROOT / "sites/cssbuyspreadsheet.ca/overlay/index.html",
    "cssbuyspreadsheet.uk": ROOT / "sites/cssbuyspreadsheet.uk/overlay/index.html",
    "cssbuyspreadsheet.eu": ROOT / "sites/cssbuyspreadsheet.eu/overlay/index.html",
    "cssbuyspreadsheets.us": ROOT / "sites/cssbuyspreadsheets.us/overlay/index.html",
    "bbdbuy.uk": ROOT / "sites/bbdbuy.uk/overlay/index.html",
    "bbdbuy.us": ROOT / "sites/bbdbuy.us/overlay/index.html",
    "bbdbuy.ca": ROOT / "sites/bbdbuy.ca/overlay/index.html",
}

# Spreadsheet-template paths → Host-aware PHP country app.
PHP_PATH_MAP = [
    ("=", "/spreadsheet", "/spreadsheet"),
    ("=", "/spreadsheet/", "/spreadsheet"),
    ("=", "/guides", "/"),
    ("=", "/guides/", "/"),
    ("=", "/guides/how-to-buy", "/guide/first-order"),
    ("=", "/guides/how-to-buy/", "/guide/first-order"),
    ("=", "/guides/qc-photos", "/guide/qc-photos"),
    ("=", "/guides/qc-photos/", "/guide/qc-photos"),
    ("=", "/guides/shipping", "/guide/shipping"),
    ("=", "/guides/shipping/", "/guide/shipping"),
    ("=", "/guides/dead-links", "/"),
    ("=", "/guides/dead-links/", "/"),
    ("=", "/faq", "/"),
    ("=", "/faq/", "/"),
    ("^~", "/category/", "/spreadsheet"),
]

CSSBUY_ALIASES = {
    "cssbuyspreadsheet.nl": "https://cssbuy.nl",
    "cssbuyspreadsheet.es": "https://cssbuy.es",
    "cssbuyspreadsheet.fr": "https://cssbuy.fr",
    "cssbuyspreadsheet.it": "https://cssbuy.it",
}


def mapped_locations(target_origin: str) -> str:
    origin = target_origin.rstrip("/")
    lines = []
    for kind, src, dest in PHP_PATH_MAP:
        url = origin + dest
        if kind == "=":
            lines.append(f"    location = {src} {{ return 301 {url}; }}")
        else:
            lines.append(f"    location ^~ {src} {{ return 301 {url}; }}")
    lines.append(f"    location / {{ return 301 {origin}/; }}")
    return "\n".join(lines)


def redirect_conf(domain: str, target_origin: str, original: str) -> str:
    cert = f"/www/server/panel/vhost/cert/{domain}/fullchain.pem"
    key = f"/www/server/panel/vhost/cert/{domain}/privkey.pem"
    m_cert = re.search(r"ssl_certificate\s+(\S+);", original)
    m_key = re.search(r"ssl_certificate_key\s+(\S+);", original)
    if m_cert:
        cert = m_cert.group(1)
    if m_key:
        key = m_key.group(1)
    maps = mapped_locations(target_origin)
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

    for host, target in CSSBUY_ALIASES.items():
        nginx = f"/www/server/panel/vhost/nginx/{host}.conf"
        original = bt.get(nginx) or ""
        backup = nginx + ".bak-evasion-p0b"
        new = redirect_conf(host, target, original)
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
            bt.put(rewrite, "# evasion-p0b: CSSBuy same-country alias, path-mapped\n").get(
                "msg", ""
            )[:60],
        )

    if not dry_run:
        print("reload", bt.reload_nginx())


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--print-map", action="store_true")
    args = parser.parse_args()
    if args.print_map:
        print(mapped_locations("https://cssbuy.nl"))
        return 0
    if not (args.apply or args.dry_run):
        print("Pass --dry-run, --apply, or --print-map (BT_KEY required for apply)")
        return 1
    key = os.environ.get("BT_KEY", "")
    if not key:
        raise SystemExit("BT_KEY required")
    apply(Baota(key), dry_run=args.dry_run)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
