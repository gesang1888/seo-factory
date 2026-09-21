#!/usr/bin/env python3
"""Evasion P0 apply: recover 5xx aliases, deepen USFans UK/NL desks.

Secrets stay in BT_KEY. HipoBuy CMS DB restore is an ops step on the VPS
(dump already imported); this script does not store MySQL passwords.
"""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from spam_update_p0 import Baota  # noqa: E402

REDIRECTS = {
    # Dead EyouCMS (empty DB) → working same-agent hub.
    "fashionrepsfind.com": "https://fashionrepsspreadsheet.com",
    # Thin template overlay → restored HipoBuy CMS hub.
    "hipobuyreview.com": "https://hipobuyspreadsheet.net",
    # Same-country UK alias → the GB desk we just deepened.
    "usfansspreadsheet.uk": "https://usfansspreadsheet.co.uk",
}

PUTS = {
    "usfansspreadsheet.co.uk": ROOT / "sites/usfansspreadsheet.co.uk/overlay/index.html",
    "usfansspreadsheet.nl": ROOT / "sites/usfansspreadsheet.nl/overlay/index.html",
}


def redirect_conf(domain: str, target: str, original: str) -> str:
    cert = f"/www/server/panel/vhost/cert/{domain}/fullchain.pem"
    key = f"/www/server/panel/vhost/cert/{domain}/privkey.pem"
    import re

    m_cert = re.search(r"ssl_certificate\s+(\S+);", original)
    m_key = re.search(r"ssl_certificate_key\s+(\S+);", original)
    if m_cert:
        cert = m_cert.group(1)
    if m_key:
        key = m_key.group(1)
    dest = target.rstrip("/")
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
    location / {{
        return 301 {dest}$request_uri;
    }}
    access_log  /www/wwwlogs/{domain}.log;
    error_log  /www/wwwlogs/{domain}.error.log;
}}
"""


def apply(bt: Baota, dry_run: bool = False) -> None:
    for host, html_path in PUTS.items():
        html = html_path.read_text()
        dest = f"/www/wwwroot/{host}/index.html"
        if dry_run:
            print("dry-run put", dest, "bytes", len(html))
            continue
        print("put", dest, bt.put(dest, html).get("msg", "")[:80])

    for host, target in REDIRECTS.items():
        nginx = f"/www/server/panel/vhost/nginx/{host}.conf"
        original = bt.get(nginx) or ""
        backup = nginx + ".bak-evasion-p0"
        new = redirect_conf(host, target, original)
        rewrite = f"/www/server/panel/vhost/rewrite/{host}.conf"
        if dry_run:
            print("dry-run 301", host, "→", target, "changed", new != original)
            continue
        if original and bt.get(backup) is None:
            print("backup", backup, bt.put(backup, original).get("msg", "")[:60])
        print("nginx", host, bt.put(nginx, new).get("msg", "")[:60])
        print("rewrite", host, bt.put(rewrite, "# evasion-p0: same-agent alias 301\n").get("msg", "")[:60])

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
