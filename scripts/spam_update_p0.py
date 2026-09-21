#!/usr/bin/env python3
"""August 2026 spam-update P0: collapse doorways, noindex cloned SKUs.

Live changes go through the Baota panel API (BT_KEY). This script does not
store secrets. Inventory: scripts/spam_update_p0_inventory.json
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import ssl
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INV = json.loads((ROOT / "scripts" / "spam_update_p0_inventory.json").read_text())
OVERLAY = {
    "allchina-buy.com": ROOT / "sites" / "allchina-buy.com" / "overlay",
    "bbdbuyeu.net": ROOT / "sites" / "bbdbuyeu.net" / "overlay",
}
EMPTY_SITEMAP = """<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
</urlset>
"""
PRODUCT_NOINDEX = """# spam-update-p0: cloned SKU pages stay crawlable so Google sees noindex.
location ^~ /product/ {
    add_header X-Robots-Tag "noindex, follow" always;
    try_files $uri $uri/ $uri/index.html =404;
}
"""
USFANS_REWRITE = """# spam-update-p0: identical clone — collapse HTTPS apex onto .net
return 301 https://usfansspreadsheet.net$request_uri;
"""
W2C_REWRITE = """# spam-update-p0: identical w2cReps clone
location / {
    return 301 https://w2crep.org$request_uri;
}
"""


def md5(s: str) -> str:
    return hashlib.md5(s.encode()).hexdigest()


class Baota:
    def __init__(self, key: str, base: str = "https://31.97.41.31:18888"):
        self.key = key
        self.base = base.rstrip("/")
        self.ctx = ssl._create_unverified_context()

    def api(self, path: str, extra: dict, timeout: int = 90):
        now = str(int(time.time()))
        data = {"request_time": now, "request_token": md5(now + md5(self.key))}
        data.update(extra)
        body = urllib.parse.urlencode(data).encode()
        req = urllib.request.Request(
            self.base + path,
            data=body,
            method="POST",
            headers={
                "Content-Type": "application/x-www-form-urlencoded",
                "User-Agent": "BT-API/1.0",
            },
        )
        try:
            with urllib.request.urlopen(req, timeout=timeout, context=self.ctx) as r:
                raw = r.read().decode(errors="replace")
                try:
                    return json.loads(raw)
                except json.JSONDecodeError:
                    return {"_raw": raw[:2000]}
        except urllib.error.HTTPError as e:
            return {"_http": e.code, "_raw": e.read()[:400].decode(errors="replace")}

    def get(self, path: str) -> str | None:
        r = self.api("/files?action=GetFileBody", {"path": path})
        if r.get("status") is False:
            return None
        data = r.get("data")
        return data if isinstance(data, str) else None

    def put(self, path: str, data: str) -> dict:
        existed = self.get(path)
        if existed is None:
            self.api("/files?action=CreateFile", {"path": path})
        return self.api(
            "/files?action=SaveFileBody",
            {"path": path, "data": data, "encoding": "utf-8"},
        )

    def reload_nginx(self) -> dict:
        return self.api("/system?action=ServiceAdmin", {"name": "nginx", "type": "reload"})


def patch_indie_conf(conf: str, action: str) -> str:
    if action == "301":
        new = "location / { return 301 https://w2clinks.com/; }"
    else:
        new = "location / { return 410; }"
    pattern = r"location\s+/\s*\{\s*try_files \$uri \$uri/ \$uri/index\.html =404;\s*\}"
    out, n = re.subn(pattern, new, conf, count=1)
    if n != 1:
        raise ValueError(f"try_files location / not uniquely found (n={n})")
    return out


def w2c_redirect_conf(domain: str, original: str) -> str:
    cert = f"/www/server/panel/vhost/cert/{domain}/fullchain.pem"
    key = f"/www/server/panel/vhost/cert/{domain}/privkey.pem"
    # Keep original cert paths if present.
    m_cert = re.search(r"ssl_certificate\s+(\S+);", original)
    m_key = re.search(r"ssl_certificate_key\s+(\S+);", original)
    if m_cert:
        cert = m_cert.group(1)
    if m_key:
        key = m_key.group(1)
    return f"""server
{{
    listen 80;
    listen 443 ssl;
    http2 on;
    server_name {domain} www.{domain};
    include /www/server/panel/vhost/nginx/well-known/{domain}.conf;
    include /www/server/panel/vhost/nginx/extension/{domain}/*.conf;
    ssl_certificate    {cert};
    ssl_certificate_key    {key};
    ssl_protocols TLSv1.2 TLSv1.3;
    add_header Strict-Transport-Security "max-age=31536000" always;
    location / {{
        return 301 https://w2crep.org$request_uri;
    }}
    access_log  /www/wwwlogs/{domain}.log;
    error_log  /www/wwwlogs/{domain}.error.log;
}}
"""


def apply(bt: Baota, dry_run: bool = False) -> dict:
    report: dict = {"ok": True, "steps": []}

    def step(name: str, result):
        report["steps"].append({"name": name, "result": result})
        print(name, result if isinstance(result, str) else json.dumps(result, ensure_ascii=False)[:240])

    # 1) USFans HTTPS apex → .net via rewrite include (HTTP/www already 301).
    for host in INV["usfans"]["redirect_301"]:
        path = f"/www/server/panel/vhost/rewrite/{host}.conf"
        if dry_run:
            step(f"usfans rewrite {host}", "dry-run")
            continue
        step(f"usfans rewrite {host}", bt.put(path, USFANS_REWRITE))

    # 2) w2cclothes / w2cshoes → w2crep.org
    for host in INV["w2c"]["redirect_301"]:
        nginx = f"/www/server/panel/vhost/nginx/{host}.conf"
        original = bt.get(nginx) or ""
        backup = nginx + ".bak-spam-p0"
        new = w2c_redirect_conf(host, original)
        if dry_run:
            step(f"w2c {host}", f"dry-run backup={backup} new_len={len(new)}")
            continue
        if original and bt.get(backup) is None:
            bt.put(backup, original)
        step(f"w2c {host}", bt.put(nginx, new))

    # 3) Product noindex + empty sitemaps
    for host in INV["product_noindex"]["hosts"]:
        overlay = OVERLAY[host]
        mapping = {
            f"/www/wwwroot/{host}/robots.txt": (overlay / "robots.txt").read_text(),
            f"/www/wwwroot/{host}/sitemap.xml": (overlay / "sitemap.xml").read_text(),
            f"/www/wwwroot/{host}/sitemap-products.xml": EMPTY_SITEMAP,
            f"/www/server/panel/vhost/nginx/extension/{host}/product-noindex.conf": PRODUCT_NOINDEX,
        }
        for path, data in mapping.items():
            if dry_run:
                step(f"put {path}", f"dry-run bytes={len(data)}")
                continue
            step(f"put {path}", bt.put(path, data))

    # 4) Indie clones
    for host in INV["indie"]["redirect_301"]:
        nginx = f"/www/server/panel/vhost/nginx/{host}.conf"
        original = bt.get(nginx)
        if original is None:
            step(f"indie 301 {host}", "missing nginx conf")
            continue
        try:
            new = patch_indie_conf(original, "301")
        except ValueError as e:
            step(f"indie 301 {host}", str(e))
            continue
        if dry_run:
            step(f"indie 301 {host}", "dry-run patched")
            continue
        bt.put(nginx + ".bak-spam-p0", original)
        step(f"indie 301 {host}", bt.put(nginx, new))

    for host in INV["indie"]["gone_410"]:
        nginx = f"/www/server/panel/vhost/nginx/{host}.conf"
        original = bt.get(nginx)
        if original is None:
            step(f"indie 410 {host}", "missing nginx conf")
            continue
        try:
            new = patch_indie_conf(original, "410")
        except ValueError as e:
            step(f"indie 410 {host}", str(e))
            continue
        if dry_run:
            step(f"indie 410 {host}", "dry-run patched")
            continue
        bt.put(nginx + ".bak-spam-p0", original)
        step(f"indie 410 {host}", bt.put(nginx, new))

    if not dry_run:
        step("nginx reload", bt.reload_nginx())
    return report


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()
    key = os.environ.get("BT_KEY", "")
    if args.apply or args.dry_run:
        if not key:
            raise SystemExit("BT_KEY is required for --apply/--dry-run")
        bt = Baota(key)
        apply(bt, dry_run=args.dry_run)
        return 0
    print("Pass --dry-run or --apply with BT_KEY set.")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
