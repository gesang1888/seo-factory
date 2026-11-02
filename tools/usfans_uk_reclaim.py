#!/usr/bin/env python3
"""Reclaim usfansspreadsheet.uk as an independent GB-collect dest.

Unique vs .co.uk “for UK Buyers”. Fingerprint: estimator GB ≠ this .uk TLD,
Royal Mail collect, NI BT, IM / JE / GY. Hub spreadsheet stays on .net.
No dest-to-dest 301. No invite in titles. No declared-value coaching.
"""
from __future__ import annotations

import json
import os
import re
import shutil
import sys
import time
from html import escape
from pathlib import Path
from urllib.error import HTTPError
from urllib.request import HTTPRedirectHandler, HTTPSHandler, Request, build_opener, urlopen

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT / "tools"), "/tmp/usfans-dest-trio"]

import desk_template as _dt  # noqa: E402

if not hasattr(_dt, "website_ld"):
    def website_ld(*, url, name, lang, brand, host, keywords=None):
        return {
            "@context": "https://schema.org",
            "@type": "WebSite",
            "name": name,
            "url": url,
            "inLanguage": lang,
            "keywords": keywords or [],
            "publisher": {"@type": "Organization", "name": brand, "url": f"https://{host}/"},
        }

    def cluster_title(agent, dest, loc, dest_label=None):
        return f"{agent} Spreadsheet for {dest_label or dest}"

    def cluster_keywords(agent, dest, loc, dest_label=None):
        return [f"{agent} spreadsheet", str(dest or loc or "")]

    _dt.website_ld = website_ld
    _dt.cluster_title = cluster_title
    _dt.cluster_keywords = cluster_keywords

import usfans_dest as dest  # noqa: E402
import usfans_dest_copy as copy  # noqa: E402
import usfans_dest_skin as skin  # noqa: E402

HOST = "usfansspreadsheet.uk"
SIBLING = "usfansspreadsheet.co.uk"
HUB = "https://usfansspreadsheet.net"
STAMP = "20261103"
TODAY = "2026-11-03"
MARKER = f'data-usfans-dest="{STAMP}" data-uk-reclaim="{STAMP}"'
OFF = "https://usfans.com/"
EST = "https://usfans.com/estimation"
W2C = "https://w2clinks.com/spreadsheet/"
SA = "/tmp/hipobuy-creds/sa.json"
REMOTE = f"/www/wwwroot/{HOST}"
OVERLAY = ROOT / "sites" / HOST / "overlay"

HOME_TITLE = "USFans Spreadsheet — GB collect, NI & IM postcodes"
HOME_H1 = "USFans for GB collect, Northern Ireland and Crown posts"
HOME_DESC = (
    "USFans spreadsheet for GB collect, Northern Ireland (BT) and Crown posts "
    "(IM, JE, GY) on usfansspreadsheet.uk. GBP display. Estimator country is GB, "
    "not this TLD. Register on usfans.com."
)

INNER_TITLE = {
    "spreadsheet": "USFans spreadsheet for GB collect and NI postcodes",
    "finds": "USFans finds for GB collect, NI and IM doors",
    "qc": "USFans QC before a GB collect or NI parcel",
    "shipping": "USFans to Royal Mail collect, NI (BT) and IM",
    "legal": "Is USFans legal for GB collect, NI and Crown posts?",
    "guide": "How to use USFans with a GB collect address",
    "faq": "USFans FAQ — GB collect, NI, IM",
}
INNER_H1 = {
    "spreadsheet": "USFans spreadsheet for GB collect and NI postcodes",
    "finds": "USFans finds for GB collect, NI and IM doors",
    "qc": "USFans QC before a GB collect or NI parcel",
    "shipping": "USFans shipping with Royal Mail collect, NI and IM",
    "legal": "Is USFans legal for GB collect, NI and Crown posts?",
    "guide": "How to use USFans with a GB collect address",
    "faq": "USFans FAQ for GB collect, NI and IM",
}

PAGES = {
    "spreadsheet": "usfans-spreadsheet",
    "finds": "usfans-finds",
    "qc": "usfans-qc",
    "shipping": "usfans-shipping-guide",
    "legal": "is-usfans-legal-uk",
    "guide": "usfans-guide",
    "faq": "usfans-faq",
}

D = {
    "key": "uk",
    "host": HOST,
    "dest": "GB",
    "loc": "en",
    "lang": "en-GB",
    "label": "a GB collect, NI or Crown-post address",
    "ccy": "GBP",
    "customs": "HMRC",
    "customs_url": "https://www.gov.uk/goods-sent-from-abroad",
    "post": "Royal Mail collect",
    "city": "UK postcode — BT = NI, IM = Isle of Man, JE/GY = Crown",
    "pages": PAGES,
    "skip": set(),
    "canon": [],
}

LEFTOVER = ("start", "catalog", "help", "news", "about")
UNIQUE_KEEP = dest.UNIQUE_PUT

NGINX = r"""server {
    listen 80;
    listen [::]:80;
    server_name usfansspreadsheet.uk www.usfansspreadsheet.uk;
    include /www/server/panel/vhost/nginx/well-known/usfansspreadsheet.uk.conf;
    return 301 https://usfansspreadsheet.uk$request_uri;
}

server {
    listen 443 ssl;
    http2 on;
    server_name www.usfansspreadsheet.uk;
    ssl_certificate    /www/server/panel/vhost/cert/usfansspreadsheet.uk/fullchain.pem;
    ssl_certificate_key    /www/server/panel/vhost/cert/usfansspreadsheet.uk/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    return 301 https://usfansspreadsheet.uk$request_uri;
}

server
{
    listen 443 ssl;
    http2 on;
    ssl_certificate    /www/server/panel/vhost/cert/usfansspreadsheet.uk/fullchain.pem;
    ssl_certificate_key    /www/server/panel/vhost/cert/usfansspreadsheet.uk/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_prefer_server_ciphers on;
    ssl_session_cache shared:SSL:10m;
    ssl_session_timeout 10m;
    add_header Strict-Transport-Security "max-age=31536000" always;
    server_name usfansspreadsheet.uk;
    index index.html index.htm index.php;
    root /www/wwwroot/usfansspreadsheet.uk;
    charset utf-8;

    if ($request_uri ~* "^/index\.html?(\?|$)") {
        return 301 /;
    }
    if ($request_uri ~* "^/(.+)/index\.html?(\?|$)") {
        return 301 /$1/;
    }

    include /www/server/panel/vhost/nginx/extension/usfansspreadsheet.uk/*.conf;
    include /www/server/panel/vhost/nginx/well-known/usfansspreadsheet.uk.conf;
    include enable-php-74.conf;
    include /www/server/panel/vhost/rewrite/usfansspreadsheet.uk.conf;

    error_page 404 /404.html;
    location = /404.html {
        internal;
        add_header X-Robots-Tag "noindex, nofollow" always;
    }

    location = /favicon.ico {
        root /www/wwwroot/usfansspreadsheet.uk;
        try_files /favicon.ico /assets/images/favicon.ico =404;
        access_log off;
        expires 30d;
    }

    location /api/ {
        rewrite ^/api/([^/]+)/?$ /api/$1/index.php last;
        add_header X-Robots-Tag "noindex, nofollow" always;
    }

    location / { try_files $uri $uri/ $uri/index.html =404; }

    location ~ \.well-known {
        allow all;
    }

    location ~* (\.user\.ini|\.htaccess|\.htpasswd|\.env.*|\.git|\.bak(up)?|\.old|\.tmp|\.temp|\.log|\.sql(\.gz)?|DEPLOY_README\.txt|_nginx\.conf)$ {
        return 404;
    }

    location ~ .*\.(gif|jpg|jpeg|png|bmp|swf|ico|svg|webp)$ {
        expires 30d;
        access_log off;
    }
    location ~ .*\.(js|css)?$ {
        expires 12h;
        access_log off;
    }

    access_log /www/wwwlogs/usfansspreadsheet.uk.log;
    error_log /www/wwwlogs/usfansspreadsheet.uk.error.log;
}
"""

GSC_REDIRECTS = """location = /guides/how-to-buy { return 301 https://usfansspreadsheet.uk/how-to-use-usfans/; }
location = /guides/how-to-buy/ { return 301 https://usfansspreadsheet.uk/how-to-use-usfans/; }
location = /guides/qc-photos { return 301 https://usfansspreadsheet.uk/usfans-qc/; }
location = /guides/qc-photos/ { return 301 https://usfansspreadsheet.uk/usfans-qc/; }
location = /guides/dead-links { return 301 https://usfansspreadsheet.uk/catalog/; }
location = /guides/dead-links/ { return 301 https://usfansspreadsheet.uk/catalog/; }
location = /guides/shipping { return 301 https://usfansspreadsheet.uk/usfans-shipping-guide/; }
location = /guides/shipping/ { return 301 https://usfansspreadsheet.uk/usfans-shipping-guide/; }
location = /guide/shipping { return 301 https://usfansspreadsheet.uk/usfans-shipping-guide/; }
location = /guide/shipping/ { return 301 https://usfansspreadsheet.uk/usfans-shipping-guide/; }
location = /guides { return 301 https://usfansspreadsheet.uk/how-to-use-usfans/; }
location = /guides/ { return 301 https://usfansspreadsheet.uk/how-to-use-usfans/; }
"""


def _patch_copy() -> None:
    orig_title = copy.inner_serp_title
    orig_h1 = copy.inner_h1
    orig_extra = copy.extra_local
    orig_faq = copy.extra_faq

    def inner_serp_title(kind, d):
        if d.get("host") == HOST:
            return INNER_TITLE[kind]
        return orig_title(kind, d)

    def inner_h1(kind, d):
        if d.get("host") == HOST:
            return INNER_H1[kind]
        return orig_h1(kind, d)

    def extra_local(d, host):
        if host != HOST:
            return orig_extra(d, host)
        return [
            ("Estimator country is GB, not this .uk TLD", [
                f"Open {EST} and set destination United Kingdom. The hostname {HOST} is a GB-collect dest, not a customs territory, and not a copy of {SIBLING}.",
                "Ireland and EU codes are other estimator countries.",
            ]),
            ("Postcodes: BT, IM, JE, GY", [
                "Mainland GB uses a standard UK postcode. BT is Northern Ireland — often another carrier product than mainland Royal Mail.",
                "IM is Isle of Man. JE and GY are Crown dependencies. Confirm the live SKU; do not assume the same collect product as a London postcode.",
            ]),
            ("Prepaid vs collect", [
                "The booked SKU decides who pays import charges. Royal Mail can add a collect fee on the doorstep. Read https://www.gov.uk/goods-sent-from-abroad (HMRC) the morning you ship. This page does not invent a rate or a declared value.",
            ]),
            ("Sibling desks stay separate", [
                f"{SIBLING} is another UK dest (UK buyers / Royal Mail last-mile). This host is the GB-collect / NI / Crown-post desk. No dest-to-dest 301. Brand spreadsheet: {HUB}.",
                f"Register and pay on {OFF}. This hostname never takes a card.",
            ]),
        ]

    def extra_faq(d, host):
        if host != HOST:
            return orig_faq(d, host)
        return [
            ("Is usfansspreadsheet.uk the same site as .co.uk?", [
                f"No. {HOST} is the GB-collect / NI / Crown-post desk. {SIBLING} stays a separate UK dest. Neither 301s to the other. The brand catalog is {HUB}.",
            ]),
            ("Which country do I pick in the estimator?", [
                f"United Kingdom (GB). Not this .uk TLD, not EU, not Ireland. Live freight: {EST}.",
            ]),
            ("What if my postcode starts with BT, IM, JE or GY?", [
                "BT is Northern Ireland — often another carrier product. IM is Isle of Man. JE and GY are Crown dependencies. Pick the live line in the app instead of reusing a mainland GB Royal Mail assumption.",
            ]),
            ("Who pays import charges?", [
                "The booked SKU decides prepaid vs collect. Royal Mail can add a collect fee. Source: HMRC. This page does not coach a declared value.",
            ]),
            ("Where do I register?", [
                f"Only on {OFF}. Coupons attach in the official wallet. This desk does not checkout.",
            ]),
        ]

    copy.inner_serp_title = inner_serp_title
    copy.inner_h1 = inner_h1
    copy.extra_local = extra_local
    copy.extra_faq = extra_faq
    dest.inner_serp_title = inner_serp_title
    dest.inner_h1 = inner_h1

    orig_chrome = skin.chrome

    def chrome(d):
        L = orig_chrome(d)
        if d.get("host") == HOST:
            L["local_h2"] = "GB collect, NI and Crown posts"
            L["loc1t"] = "Estimator country"
            L["loc1"] = "United Kingdom (GB) in the official calculator — not this .uk TLD, not EU, not IE."
            L["loc2t"] = "Postcode"
            L["loc2"] = "UK street and postcode. BT = Northern Ireland (often another SKU). IM = Isle of Man. JE/GY = Crown dependencies."
            L["loc3t"] = "Prepaid vs collect"
            L["loc3"] = "The booked SKU decides. Royal Mail can add a collect fee. Source: HMRC. This page does not invent a rate."
            L["loc4t"] = "Last mile"
            L["loc4"] = "Often Royal Mail on mainland GB after warehouse QC. NI/IM/JE/GY: pick the live line."
            L["sub"] = "Shop from China toward a GB collect, NI or Crown-post address. Prices on this page are shown in GBP. Register on usfans.com."
            L["s3"] = "Choose a line with destination United Kingdom. Last mile is often Royal Mail collect on mainland GB; NI and Crown posts are other products."
        return L

    skin.chrome = chrome


def _connect():
    return dest._connect()


def _run(client, cmd: str, timeout: int = 120) -> str:
    return dest._run(client, cmd, timeout=timeout)


def pull_seeds() -> None:
    client = _connect()
    sftp = client.open_sftp()
    OVERLAY.mkdir(parents=True, exist_ok=True)
    slugs = ["index.html"] + list(PAGES.values()) + list(LEFTOVER)
    for name in slugs:
        if name == "index.html":
            remote = f"/www/wwwroot/{SIBLING}/index.html"
            local = OVERLAY / "index.html"
        else:
            remote = f"/www/wwwroot/{SIBLING}/{name}/index.html"
            local = OVERLAY / name / "index.html"
        local.parent.mkdir(parents=True, exist_ok=True)
        try:
            sftp.get(remote, str(local))
            html = local.read_text(encoding="utf-8", errors="replace")
            html = html.replace(SIBLING, HOST)
            html = html.replace("for UK Buyers", "for GB collect and NI posts")
            local.write_text(html, encoding="utf-8")
            print("SEED", name, local.stat().st_size)
        except Exception as exc:  # noqa: BLE001
            print("SEED_SKIP", name, type(exc).__name__, str(exc)[:120])
    sftp.close()
    client.close()


def _cleanup_public(html: str) -> str:
    html = html.replace("usfansspreadsheet.uk is an .", "usfansspreadsheet.uk is a country dest.")
    html = html.replace("is an . Orders", "is a country dest. Orders")
    html = html.replace('"name": ""', '"name": "USFans GB collect dest"')
    html = html.replace(" for the United Kingdom on", " GB-collect dest on")
    html = re.sub(r"is of usfansspreadsheet\.co\.uk", "is a separate dest from usfansspreadsheet.co.uk", html)
    html = html.replace("We will not invent a declared value", "This page does not invent a declared value")
    html = html.replace("This desk does not invent a declared value", "This page does not invent a declared value")
    return html


def _hub_uplink() -> str:
    return (
        f'<p class="hub-uplink" data-uk-reclaim="{STAMP}">Brand spreadsheet → '
        f'<a href="{HUB}/">usfansspreadsheet.net</a> · '
        f'<a href="{HUB}/finds-dataset/">dataset</a> · '
        f'<a href="{HUB}/usfans-coupons/">coupons</a>. '
        f"This host = GB collect / NI / IM. Sibling "
        f'<a href="https://{SIBLING}/">{SIBLING}</a> stays independent — no 301.</p>'
    )


def patch_home() -> Path:
    path = OVERLAY / "index.html"
    html = path.read_text(encoding="utf-8")
    html = re.sub(r'(<html\b[^>]*\blang=")[^"]*', rf'\1{D["lang"]}', html, count=1, flags=re.I)
    html = dest.patch_cluster_nav(html, D)
    html = re.sub(r"<title>[\s\S]*?</title>", f"<title>{escape(HOME_TITLE)}</title>", html, count=1, flags=re.I)
    html = dest.upsert_meta(html, "description", HOME_DESC)
    html = re.sub(r"<h1>[\s\S]*?</h1>", f"<h1>{escape(HOME_H1)}</h1>", html, count=1, flags=re.I)
    html = re.sub(
        r'(<meta\s+property="og:title"\s+content=")[^"]*(")',
        rf"\1{escape(HOME_TITLE)}\2",
        html,
        count=1,
        flags=re.I,
    )
    try:
        html = dest.inject_jsonld(
            html,
            dest.website_ld(
                url=f"https://{HOST}/",
                name=HOME_TITLE,
                lang=D["lang"],
                brand="USFans",
                host=HOST,
                keywords=["usfans spreadsheet", "gb collect", "northern ireland", "isle of man"],
            ),
        )
    except Exception:
        pass
    html = html.replace("<body", f"<body {MARKER}", 1)
    html = skin.rebuild_home(html, HOST, D)
    html = skin.strip_ops(html)
    html = html.replace("for UK Buyers", "for GB collect and NI posts")
    html = _cleanup_public(html)
    if 'class="hub-uplink"' not in html:
        html = html.replace('id="local">', 'id="local">' + _hub_uplink(), 1)
        if 'class="hub-uplink"' not in html:
            html = html.replace("</h1>", "</h1>\n" + _hub_uplink(), 1)
    path.write_text(html, encoding="utf-8")
    print("HOME", path.stat().st_size, HOME_TITLE)
    return path


def generate() -> list[Path]:
    _patch_copy()
    dest.ROOT = ROOT
    skin.ROOT = ROOT
    skin.MEDIA_SRC = ROOT / "sites" / "shared" / "usfans-media"
    dest.HOSTS[HOST] = D
    dest.TODAY = TODAY
    dest.STAMP = STAMP
    dest.MARKER = MARKER
    dest.pull_official_media()
    pull_seeds()
    skin.UNIQUE_DIR[HOST] = set(skin.UNIQUE_DIR.get(SIBLING, set()))
    written: list[Path] = []
    written.extend(skin.install_media(HOST))
    written.append(patch_home())
    for kind in PAGES:
        p = dest.deepen_inner(HOST, kind, D)
        if p:
            html = p.read_text(encoding="utf-8")
            html = html.replace("<body", f"<body {MARKER}", 1) if MARKER.split("=")[0] not in html else html
            html = skin.skin_chrome(html, HOST, D)
            html = skin.strip_ops(html)
            html = _cleanup_public(html)
            if 'class="hub-uplink"' not in html:
                html = html.replace("</h1>", "</h1>\n" + _hub_uplink(), 1)
            p.write_text(html, encoding="utf-8")
            written.append(p)
            print("INNER", kind, p.stat().st_size)
    for slug in LEFTOVER:
        path = OVERLAY / slug / "index.html"
        if not path.is_file() or dest._is_unique(slug):
            continue
        html = path.read_text(encoding="utf-8", errors="replace")
        html = html.replace(SIBLING, HOST)
        html = skin.skin_chrome(html, HOST, D)
        html = skin.strip_ops(html)
        title = f"USFans {slug} — GB collect, NI & IM"
        html = re.sub(r"<title>[\s\S]*?</title>", f"<title>{escape(title)}</title>", html, count=1, flags=re.I)
        html = _cleanup_public(html)
        if 'class="hub-uplink"' not in html:
            html = html.replace("</h1>", "</h1>\n" + _hub_uplink(), 1)
        path.write_text(html, encoding="utf-8")
        written.append(path)
        print("LEFTOVER", slug, path.stat().st_size)
    dest.bump_sitemap(HOST, D)
    sm = OVERLAY / "sitemap.xml"
    if sm.is_file():
        written.append(sm)
    written.extend(dest.write_api_overlay(HOST))
    robots = OVERLAY / "robots.txt"
    robots.write_text(
        "User-agent: *\nAllow: /\nSitemap: https://usfansspreadsheet.uk/sitemap.xml\n",
        encoding="utf-8",
    )
    written.append(robots)
    conf = OVERLAY / "_deploy" / "dest-vhost.conf"
    conf.parent.mkdir(parents=True, exist_ok=True)
    conf.write_text(NGINX, encoding="utf-8")
    written.append(conf)
    (OVERLAY / "_deploy" / "gsc-redirects.conf").write_text(GSC_REDIRECTS, encoding="utf-8")
    written.append(OVERLAY / "_deploy" / "gsc-redirects.conf")
    return written


def deploy(files: list[Path]) -> str:
    client = _connect()
    stamp = time.strftime("%Y%m%d-%H%M%S")
    bak = f"/www/backup/usfans-uk-reclaim-{stamp}"
    print(_run(client, f"mkdir -p '{bak}' '{bak}/wwwroot' '{bak}/nginx'"))
    print(_run(client, f"cp -a /www/server/panel/vhost/nginx/{HOST}.conf '{bak}/nginx/' || true"))
    print(_run(
        client,
        f"cp -a /www/server/panel/vhost/nginx/extension/{HOST}/gsc-redirects.conf '{bak}/nginx/' || true",
    ))
    print(_run(client, f"cp -a {REMOTE}/index.html '{bak}/wwwroot/' || true"))

    # rsync assets from sibling (not HTML)
    rsync = (
        f"rsync -a --delete --exclude '*.html' --exclude 'blog/' --exclude 'indexnow-key.txt' "
        f"/www/wwwroot/{SIBLING}/assets/ {REMOTE}/assets/ && "
        f"rsync -a --exclude '*.html' /www/wwwroot/{SIBLING}/img/ {REMOTE}/img/ && "
        f"rsync -a --exclude '*.html' /www/wwwroot/{SIBLING}/media/ {REMOTE}/media/ && "
        f"mkdir -p {REMOTE}/api && "
        f"rsync -a --exclude 'config.local.php' /www/wwwroot/{SIBLING}/api/ {REMOTE}/api/"
    )
    print(_run(client, rsync, timeout=180))

    sftp = client.open_sftp()
    nginx_path = f"/www/server/panel/vhost/nginx/{HOST}.conf"
    with sftp.open(nginx_path, "w") as fh:
        fh.write(NGINX)
    print("PUT nginx", nginx_path)
    gsc_path = f"/www/server/panel/vhost/nginx/extension/{HOST}/gsc-redirects.conf"
    with sftp.open(gsc_path, "w") as fh:
        fh.write(GSC_REDIRECTS)
    print("PUT gsc-redirects", gsc_path)

    n = 0
    for path in files:
        if path.name.endswith(".conf"):
            continue
        rest = path.relative_to(OVERLAY).as_posix()
        if rest.startswith("_deploy"):
            continue
        if dest._is_unique(rest):
            print("PUT_SKIP unique", rest)
            continue
        remote = f"{REMOTE}/{rest}"
        _run(client, f"mkdir -p '{str(Path(remote).parent)}'")
        sftp.put(str(path), remote)
        _run(client, f"chown www:www '{remote}'")
        n += 1
        print("PUT", remote)
    sftp.close()

    dest.ORDER = [HOST]
    dest.put_api_secrets(client)

    test = _run(client, "nginx -t && nginx -s reload")
    print(test)
    if "failed" in test.lower() or "error" in test.lower() and "error_log" not in test.lower()[:20]:
        # restore on hard fail
        print("NGINX_FAIL restoring", bak)
        _run(client, f"cp -a '{bak}/nginx/{HOST}.conf' /www/server/panel/vhost/nginx/{HOST}.conf && nginx -t && nginx -s reload")
        raise SystemExit("nginx -t failed")
    print("DEPLOY", n, "backup", bak)
    client.close()
    return bak


def verify() -> dict:
    class NoRedir(HTTPRedirectHandler):
        def redirect_request(self, *a, **k):
            return None

    opener = build_opener(NoRedir(), HTTPSHandler())
    rows = []

    def hit(url: str, follow: bool = False):
        req = Request(url, headers={"User-Agent": "usfans-uk-reclaim/1.0"})
        try:
            handler = urlopen if follow else opener.open
            with handler(req, timeout=25) as resp:
                body = resp.read().decode("utf-8", "replace")
                return resp.status, resp.headers.get("Location"), body
        except HTTPError as exc:
            loc = exc.headers.get("Location") if exc.headers else ""
            try:
                body = exc.read().decode("utf-8", "replace")
            except Exception:
                body = ""
            return exc.code, loc, body

    checks = [
        (f"https://{HOST}/", HOME_H1, "GB collect"),
        (f"https://{HOST}/", 'name="q"', W2C),
        (f"https://{HOST}/", "Northern Ireland", "usfans.com/estimation"),
        (f"https://{HOST}/usfans-spreadsheet/", INNER_H1["spreadsheet"], "BT"),
        (f"https://{HOST}/usfans-shipping-guide/", "Royal Mail collect", "Isle of Man"),
        (f"https://{HOST}/is-usfans-legal-uk/", "Crown", "HMRC"),
        (f"https://{SIBLING}/", "UK Buyers", None),
        ("https://usfansspreadsheet.net/", "searchable QC catalog", "10,601"),
    ]
    for url, *needles in checks:
        code, loc, body = hit(url)
        miss = [n for n in needles if n and n not in (body or "")]
        row = {"url": url, "http": code, "location": loc, "miss": miss, "ok": code == 200 and not miss}
        print("VERIFY", code, url, "OK" if row["ok"] else f"MISS {miss} loc={loc}")
        rows.append(row)

    code, loc, _ = hit(f"https://{HOST}/")
    if code in (301, 302, 308) and SIBLING in (loc or ""):
        print("FAIL still 301 to sibling", loc)
        rows.append({"url": f"https://{HOST}/", "http": code, "fail": "still_301_sibling"})
    www_code, www_loc, _ = hit("https://www.usfansspreadsheet.uk/")
    print("VERIFY_WWW", www_code, www_loc)
    rows.append({"www": www_code, "location": www_loc})

    # API
    req = Request(
        f"https://{HOST}/api/products/?q=sneakers&limit=2&page=1",
        headers={"User-Agent": "usfans-uk-reclaim/1.0", "Accept": "application/json"},
    )
    try:
        with urlopen(req, timeout=22) as resp:
            data = json.loads(resp.read().decode())
            items = data.get("items") or data.get("products") or []
            print("VERIFY_API", resp.status, "n=", len(items), "found=", data.get("found"))
            rows.append({"api": resp.status, "n": len(items)})
    except Exception as exc:  # noqa: BLE001
        print("VERIFY_API_ERR", type(exc).__name__, str(exc)[:160])
        rows.append({"api_err": str(exc)[:160]})
    return {"at": time.strftime("%Y-%m-%dT%H:%M:%SZ"), "rows": rows}


def gsc_submit() -> None:
    if not Path(SA).is_file():
        print("GSC_SKIP no sa.json")
        return
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

    creds = service_account.Credentials.from_service_account_file(
        SA, scopes=["https://www.googleapis.com/auth/webmasters"]
    )
    gsc = build("searchconsole", "v1", credentials=creds, cache_discovery=False)
    listed = {row["siteUrl"] for row in gsc.sites().list().execute().get("siteEntry", [])}
    site = f"sc-domain:{HOST}" if f"sc-domain:{HOST}" in listed else f"https://{HOST}/"
    feed = f"https://{HOST}/sitemap.xml"
    try:
        gsc.sitemaps().submit(siteUrl=site if site in listed else f"https://{HOST}/", feedpath=feed).execute()
        print("SITEMAP", HOST, site, feed)
    except Exception as exc:  # noqa: BLE001
        print("SITEMAP_FAIL", type(exc).__name__, str(exc)[:200])
    # hub sitemap too
    hub = "usfansspreadsheet.net"
    hsite = f"sc-domain:{hub}" if f"sc-domain:{hub}" in listed else f"https://{hub}/"
    try:
        gsc.sitemaps().submit(siteUrl=hsite if hsite in listed else f"https://{hub}/", feedpath=f"https://{hub}/sitemap.xml").execute()
        print("SITEMAP", hub, hsite)
    except Exception as exc:  # noqa: BLE001
        print("SITEMAP_FAIL", hub, type(exc).__name__, str(exc)[:200])


def main() -> None:
    os.environ.setdefault("ORIGIN_SSH_PASS", Path("/tmp/hipobuy-creds/origin.pass").read_text().strip())
    cmd = sys.argv[1] if len(sys.argv) > 1 else "all"
    if cmd == "generate":
        generate()
    elif cmd == "put":
        files = generate()
        deploy(files)
    elif cmd == "verify":
        verify()
    elif cmd == "gsc":
        gsc_submit()
    elif cmd == "all":
        files = generate()
        deploy(files)
        verify()
        gsc_submit()
    else:
        raise SystemExit(f"unknown {cmd}")


if __name__ == "__main__":
    main()
