#!/usr/bin/env python3
"""PantherBuy desks: restore unique 65KB .net hub; surgical #local.

Gates:
1. Hub #local has the HUB fingerprint, no dest-country fingerprints.
2. Estimator country ≠ TLD; .net must say it is not a customs territory.
   GSC is 1 DEU click + mixed CAN/ESP/GBR/ITA/NLD impressions — still a hub
   because the TLD is .net, not a customs dest.
3. Homepage title has no invite token (unique title “— Coupons” stays; no
   frozen invite on home). Body has no customs coaching / 58-line snapshot.
   Coupon stacking stays on /pantherbuy-coupon-tracker-2026.html.
4. Canonical is www.pantherbuy.net. Apex/http 301 to www $request_uri.
   No same-agent country 301. Single origin host.
5. spam-p0 turned apex/http 301s and www location / into 410. Restore
   bak-spam-p0 so ranked inners 200. Deep paths must not 404. Keep existing
   gsc-redirects slash aliases.
6. Unique 65KB dark CMS stays. Surgical #local insert only — do not PUT a
   5KB dest template over 15–65KB HTML.

Official SPA shell 200s /estimation and /help-center. Do not invent a
free-day count; Help is a SPA and the JS does not state warehouse days.
"""
from __future__ import annotations

import os
import re
import sys
import time
from html import escape
from pathlib import Path

_TOOLS = Path(__file__).resolve().parent
if str(_TOOLS) not in sys.path:
    sys.path.insert(0, str(_TOOLS))
from desk_template import (
    SKIP_CSS,
    _check_local_section,
    assert_dest_packs_unique,
    dest_local_pack,
    local_cta,
    local_guide_html,
    skip_label,
    skip_link,
)

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "sites"
EST = "https://pantherbuy.com/estimation"
OFFICIAL = "https://pantherbuy.com/"
HELP = "https://pantherbuy.com/help-center"
DATE = "2 Oct 2026"
# Homepage has no frozen invite token. Sentinel so an empty string cannot match.
INVITE = "___no_frozen_pantherbuy_invite___"
HUB_MIN = 60000
LIVE_HUB_MIN = 62000
STORAGE = (
    "Official PantherBuy Help is the live site "
    f"({HELP}); that URL is a SPA shell. "
    "Confirm the live copy the morning you ship. "
    "This desk does not invent a free-day count."
)

HUBS = {
    "net": {
        "host": "pantherbuy.net",
        "public": "www.pantherbuy.net",
        "lang": "en",
        "loc": "en",
        "dest": None,
        "dest_label": "a country in the estimator",
        "ccy": "USD",
        "title": None,
        "h1": None,
        "keep": [
            ("/pantherbuy-coupon-tracker-2026.html", "Coupon tracker"),
            ("/pantherbuy-shipping-lines-2026.html", "Shipping lines"),
            ("/pantherbuy-real-shipping-bills-2026.html", "Shipping bills"),
            ("/pantherbuy-user-reports-2026.html", "User reports"),
        ],
    },
}

EST_NOTE = {
    "net": (
        "This .net hub is not a customs territory. One DE click and mixed "
        "CA/ES/GB/IT/NL impressions do not make .net a customs dest. Pick the "
        "real ship-to country in the official estimator, not this hostname, "
        "not “EU” as one country."
    ),
}

STORE_NOTE = {
    "en": (
        "Warehouse: official PantherBuy Help. That URL is a SPA — confirm "
        "the live copy the morning you ship. Do not invent a free-day count "
        "on this hub."
    ),
}

TRAIL = {"en": ("Live money is in", "this HTML is not checkout.")}

HUB_LOCAL_CSS = (
    ".sg-sec#local{max-width:1100px;margin:1.5rem auto;padding:0 24px;color:#e5e7eb}"
    ".sg-sec#local h2{margin-top:0;color:#fff}"
    ".ssub{color:#a3a3a3;font-size:.95rem;margin:0 0 12px}"
    ".local-steps{margin:12px 0 0;padding:0;list-style:none;display:grid;gap:12px}"
    ".local-steps li{border:1px solid rgba(255,255,255,.12);border-radius:12px;"
    "padding:14px 16px;background:#111}"
    ".local-steps strong{display:block;margin:0 0 6px;font-size:15px;color:#fff}"
    ".local-steps span{display:block;color:#d4d4d4;line-height:1.7;font-size:15px}"
    ".local-src{font-size:14px;color:#d4d4d4;line-height:1.7;margin:14px 0 0}"
    ".local-src a{color:#93c5fd;text-decoration:underline}"
    "#local{scroll-margin-top:96px}"
)

ALIENS = (
    "1010 Wien",
    "Packstation",
    "form A1A 1A1",
    "Poste Italiane",
    "00-001 Warszawa",
    "00100 Helsinki",
    "no copiamos un recuento de líneas",
    "pas un code postal belge",
    "Nederlandse postcode",
    "does not invent a de-minimis dollar",
    "Northern Ireland is often another",
    "do not copy a GST rate",
)

RANKED_CMS = (
    ("/pantherbuy-coupon-tracker-2026.html", 8000),
    ("/pantherbuy-shipping-lines-2026.html", 8000),
    ("/pantherbuy-real-shipping-bills-2026.html", 8000),
    ("/pantherbuy-user-reports-2026.html", 8000),
    ("/hoodies-sweaters/", 4000),
    ("/shoes381/", 4000),
    ("/jackets839/", 4000),
    ("/t-shirts/", 4000),
    ("/accessories/", 4000),
)

KEEP_REDIRECTS: tuple[tuple[str, str], ...] = ()

HERO_END = "    </section>\n\n    <section class=\"overview-strip\">"
NAV_DESK = '<nav class="desktop-nav" aria-label="Main navigation">\n        <a href="/">Home</a>'
NAV_MOB = '<nav class="mobile-menu" id="mobileMenu" aria-label="Mobile navigation">\n        <a href="/">Home</a>'
CHROME = (
    'id="siteHeader"',
    "desktop-nav",
    "hero-panel",
    'id="deeper-guides"',
    "PantherBuy Spreadsheet 2026",
)
HOST = "pantherbuy.net"
PUBLIC = "www.pantherbuy.net"


def _facts(spec: dict) -> dict:
    return {
        "agent": "PantherBuy",
        "host": spec["host"],
        "lang": spec["lang"],
        "loc": spec["loc"],
        "dest": spec.get("dest"),
        "dest_label": spec.get("dest_label") or "a country in the estimator",
        "ccy": spec["ccy"],
        "storage": STORAGE,
        "estimator": EST,
        "official": OFFICIAL,
        "date": DATE,
        "keep": spec.get("keep") or [],
        "codes_off_title": [INVITE],
        "strict_html_codes": True,
    }


def _local_block(key: str, spec: dict) -> str:
    facts = _facts(spec)
    loc = spec["loc"]
    fp = dest_local_pack(facts.get("dest"))["fingerprint"]
    store = STORE_NOTE.get(loc) or STORE_NOTE["en"]
    live, not_co = TRAIL.get(loc) or TRAIL["en"]
    extra = (
        f'<p class="local-src">{escape(fp)}. {escape(EST_NOTE[key])} {escape(store)} '
        f"{escape(live)} <a href=\"{escape(facts['estimator'])}\">{escape(facts['estimator'])}</a> "
        f"— {escape(not_co)}</p>"
    )
    html = local_guide_html(facts).strip()
    if not html.endswith("</section>"):
        raise RuntimeError(f"{key}: missing section")
    html = html[: -len("</section>")] + extra + "\n</section>"
    err: list[str] = []
    _check_local_section(html, facts, err)
    if err:
        raise RuntimeError(f"{key} #local: {'; '.join(err)}")
    return html


def patch_static(html: str, key: str, spec: dict) -> str:
    facts = _facts(spec)
    block = _local_block(key, spec)
    loc = spec["loc"]
    if 'class="skip"' not in html:
        html = re.sub(
            r"(<body[^>]*>)",
            r"\1\n" + skip_link(skip_label(loc)).rstrip(),
            html,
            count=1,
        )
    if 'id="main"' not in html:
        html = html.replace(
            '<section class="hero">',
            '<section class="hero" id="main">',
            1,
        )
    cta = escape(local_cta(facts))
    if 'href="#local"' not in html:
        if NAV_DESK not in html:
            raise RuntimeError("hub desktop nav missing")
        html = html.replace(
            NAV_DESK,
            NAV_DESK + f'\n        <a href="#local">{cta}</a>',
            1,
        )
        if NAV_MOB in html:
            html = html.replace(
                NAV_MOB,
                NAV_MOB + f'\n        <a href="#local">{cta}</a>',
                1,
            )
    if "#local{scroll-margin-top" not in html:
        if "</style>" in html:
            html = html.replace("</style>", SKIP_CSS + HUB_LOCAL_CSS + "\n</style>", 1)
        else:
            html = html.replace("</head>", "<style>" + SKIP_CSS + HUB_LOCAL_CSS + "</style>\n</head>", 1)
    if 'id="local"' in html:
        html = re.sub(
            r'<section class="sg-sec" id="local".*?</section>',
            block,
            html,
            count=1,
            flags=re.S,
        )
    else:
        if HERO_END not in html:
            raise RuntimeError("hub hero marker missing")
        html = html.replace(HERO_END, "    </section>\n" + block + "\n    <section class=\"overview-strip\">", 1)
    err: list[str] = []
    _check_local_section(html, facts, err)
    title_m = re.search(r"<title>(.*?)</title>", html, flags=re.S)
    title = title_m.group(1) if title_m else ""
    if re.search(r"invite\s*(code)?\s*[A-Z0-9]{5,}", title, flags=re.I):
        err.append("invite in title")
    if INVITE in html:
        err.append("sentinel invite leaked onto homepage")
    if re.search(r"58 l[ií]neas para Espa|23[,.]81\s*USD|how to under-?declar", html, flags=re.I):
        err.append("spain snapshot / coaching")
    if "not a customs territory" not in html:
        err.append("hub missing fingerprint")
    if len(html.encode("utf-8")) < HUB_MIN:
        err.append(f"hub collapsed to {len(html.encode('utf-8'))} bytes")
    for marker in CHROME:
        if marker not in html:
            err.append(f"hub chrome missing {marker}")
    if err:
        raise RuntimeError(f"{key}: {'; '.join(err)}")
    return html


def generate() -> None:
    assert_dest_packs_unique()
    blobs = {}
    specs = {**HUBS}
    for key, spec in specs.items():
        src = OUT / spec["host"] / "live-base" / "index.html"
        html = patch_static(src.read_text(encoding="utf-8"), key, spec)
        dest = OUT / spec["host"] / "overlay" / "index.html"
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(html, encoding="utf-8")
        inner = re.search(r'<section class="sg-sec" id="local".*?</section>', html, flags=re.S)
        blobs[key] = inner.group(0) if inner else ""
        print("hub", key, spec["host"], "bytes", len(html.encode("utf-8")))
    fps = {k: dest_local_pack(specs[k].get("dest"))["fingerprint"] for k in blobs}
    for key, inner in blobs.items():
        fp = fps[key]
        if fp not in inner:
            raise SystemExit(f"{key} missing fingerprint {fp!r}")
        for alien in ALIENS:
            if alien in inner:
                raise SystemExit(f"{key} leaked dest {alien!r}")
        if EST not in inner:
            raise SystemExit(f"{key} missing estimator")
        if "not a customs territory" not in inner:
            raise SystemExit(f"{key} hub missing customs-territory line")
        if INVITE in inner:
            raise SystemExit(f"{key} #local still has invite token")
        if re.search(r"90\s*dagen|90\s*days|60\s*-?\s*day", inner, flags=re.I):
            raise SystemExit(f"{key} invented free-day count in #local")
    print("generate ok", len(blobs), "desks")


def _connect():
    try:
        import paramiko
    except ImportError:
        import subprocess

        subprocess.check_call([sys.executable, "-m", "pip", "install", "paramiko", "-q"])
        import paramiko

    password = os.environ.get("ORIGIN_SSH_PASS")
    if not password:
        raise SystemExit("Set ORIGIN_SSH_PASS")
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect("31.97.41.31", username="root", password=password, timeout=30)
    return client


def _run(client, cmd: str, timeout: int = 90) -> str:
    _, stdout, stderr = client.exec_command(cmd, timeout=timeout)
    return (stdout.read() + stderr.read()).decode(errors="replace").strip()


def put() -> None:
    generate()
    client = _connect()
    stamp = time.strftime("%Y%m%d-%H%M%S")
    bak = f"/www/backup/pantherbuy-desks-{stamp}"
    _run(client, f"mkdir -p '{bak}'")
    sftp = client.open_sftp()
    for spec in HUBS.values():
        local = OUT / spec["host"] / "overlay" / "index.html"
        remote = f"/www/wwwroot/{spec['host']}/index.html"
        raw = local.read_text(encoding="utf-8")
        if 'id="local"' not in raw or "not a customs territory" not in raw:
            raise SystemExit(f"refusing to PUT {spec['host']} without hub #local")
        if INVITE in raw:
            raise SystemExit(f"refusing to PUT {spec['host']} with invite sentinel")
        if local.stat().st_size < HUB_MIN:
            raise SystemExit(f"refusing to PUT collapsed hub {local.stat().st_size} B")
        for marker in CHROME:
            if marker not in raw:
                raise SystemExit(f"refusing to PUT hub missing chrome {marker}")
        live = _run(client, f"wc -c < '{remote}'")
        try:
            live_n = int(live.strip().split()[0])
        except ValueError:
            live_n = 0
        if live_n and live_n < 20000:
            raise SystemExit(f"refusing to PUT over unexpected thin home {live_n} B")
        if live_n and live_n >= 50000 and 'id="siteHeader"' in _run(client, f"head -c 20000 '{remote}'"):
            pass
        _run(client, f"cp -a '{remote}' '{bak}/{spec['host']}.index.html'")
        sftp.put(str(local), remote)
        print("PUT", remote, "bytes", local.stat().st_size)

        vhost = f"/www/server/panel/vhost/nginx/{spec['host']}.conf"
        _run(client, f"cp -a '{vhost}' '{bak}/{spec['host']}.conf'")
        bak_p0 = f"{vhost}.bak-spam-p0"
        exists = _run(client, f"test -f '{bak_p0}' && echo yes || echo no")
        if exists.strip() == "yes":
            _run(client, f"cp -a '{bak_p0}' '{vhost}'")
            print("restored vhost from bak-spam-p0 (410 → www 301 + try_files)")
        else:
            vraw = _run(client, f"cat '{vhost}'")
            new = vraw.replace(
                "    location / { return 410; }",
                "    location / { try_files $uri $uri/ $uri/index.html =404; }",
            )
            if new == vraw:
                raise SystemExit("hub nginx 410 restore did not match and no bak-spam-p0")
            with sftp.file(vhost, "w") as fh:
                fh.write(new)
            print("restored vhost try_files (was 410)")
        vnow = _run(client, f"cat '{vhost}'")
        if "return 410" in vnow:
            raise SystemExit("hub nginx still has return 410 after restore")
        if "try_files $uri $uri/ $uri/index.html =404" not in vnow:
            raise SystemExit("hub nginx missing try_files after restore")
        if "https://www.pantherbuy.net$request_uri" not in vnow:
            raise SystemExit("apex/http missing 301 to www $request_uri")

        for rel, min_b in RANKED_CMS:
            if rel.endswith("/"):
                inner = f"/www/wwwroot/{spec['host']}{rel}index.html"
            else:
                inner = f"/www/wwwroot/{spec['host']}{rel}"
            n = _run(client, f"wc -c < '{inner}' 2>/dev/null || echo 0")
            try:
                inner_n = int(n.strip().split()[0])
            except ValueError:
                inner_n = 0
            if inner_n and inner_n < min_b:
                raise SystemExit(f"unique CMS shrank {rel} {inner_n}")
            print("keep unique", rel, inner_n)

    nginx_t = _run(client, "nginx -t 2>&1")
    print(nginx_t)
    if "successful" not in nginx_t.lower() and "ok" not in nginx_t.lower():
        raise SystemExit("nginx -t failed; not reloading")
    print(_run(client, "nginx -s reload 2>&1"))
    sftp.close()
    print("backup", bak)
    print("unique 65KB CMS kept; 410 restored; no dest overlay")
    client.close()


def live_check() -> None:
    import urllib.request

    class NR(urllib.request.HTTPRedirectHandler):
        def redirect_request(self, req, fp, code, msg, headers, newurl):
            return None

    def fetch(url, follow=True):
        req = urllib.request.Request(
            url,
            headers={
                "User-Agent": "pantherbuy-desk-check/1.0",
                "Cache-Control": "no-cache",
                "Pragma": "no-cache",
            },
        )
        opener = urllib.request.build_opener() if follow else urllib.request.build_opener(NR)
        try:
            with opener.open(req, timeout=25) as resp:
                return resp.status, resp.geturl(), resp.headers.get("Location") or "", resp.read()
        except urllib.error.HTTPError as e:
            return e.code, url, e.headers.get("Location") or "", e.read() if e.fp else b""

    fail = 0
    url = f"https://{PUBLIC}/"
    code, _, loc, body = fetch(url, follow=True)
    html = body.decode("utf-8", "replace")
    title_m = re.search(r"<title>(.*?)</title>", html, flags=re.S)
    title = title_m.group(1) if title_m else ""
    inner_m = re.search(r'<section class="sg-sec" id="local".*?</section>', html, flags=re.S)
    inner = inner_m.group(0) if inner_m else ""
    fp = "not a customs territory"
    print(f"net {code} bytes={len(body)} local={bool(inner)} fp={fp in html}")
    if code == 410:
        print("  FAIL homepage still 410")
        fail += 1
    elif code != 200 or not inner or fp not in inner:
        print("  FAIL status/local/fp")
        fail += 1
    else:
        for alien in ALIENS:
            if alien in inner:
                print("  FAIL sister", alien)
                fail += 1
        if re.search(r"invite\s*(code)?\s*[A-Z0-9]{5,}", title, flags=re.I):
            print("  FAIL invite in title")
            fail += 1
        if re.search(r"58 l[ií]neas para Espa|23[,.]81\s*USD|how to under-?declar", html, flags=re.I):
            print("  FAIL snapshot/coaching")
            fail += 1
        if re.search(r"90\s*dagen|90\s*days|60\s*-?\s*day", inner, flags=re.I):
            print("  FAIL invented free-day copy")
            fail += 1
        if EST not in inner:
            print("  FAIL estimator")
            fail += 1
        if len(body) < LIVE_HUB_MIN:
            print("  FAIL hub collapsed", len(body))
            fail += 1
        for marker in CHROME:
            if marker not in html:
                print("  FAIL hub chrome gone", marker)
                fail += 1

    code, _, loc, _ = fetch(url, follow=False)
    if code in (301, 302, 303, 307, 308):
        print("FAIL www hub 301", loc)
        fail += 1
    else:
        print("indep www hub", code)

    code, _, loc, _ = fetch(f"https://{HOST}/", follow=False)
    if code in (301, 302, 303, 307, 308) and PUBLIC in (loc or "") and "pantherbuy.net" in (loc or ""):
        print("apex www", code, loc)
        if "$request" not in loc and not loc.rstrip("/").endswith("pantherbuy.net") and "/http" in loc:
            pass
    else:
        print("FAIL apex not 301 www", code, loc)
        fail += 1

    deep = "/pantherbuy-coupon-tracker-2026.html"
    code, _, loc, _ = fetch(f"https://{HOST}{deep}", follow=False)
    if code in (301, 302, 303, 307, 308) and PUBLIC in (loc or "") and deep in (loc or ""):
        print("apex deep $request_uri", code, loc)
    else:
        print("FAIL apex deep", code, loc)
        fail += 1

    for path, min_bytes in RANKED_CMS:
        inner_url = f"https://{PUBLIC}{path}"
        code, _, loc, _ = fetch(inner_url, follow=False)
        if code in (301, 302, 303, 307, 308) and loc:
            if path.rstrip("/") not in loc and not loc.rstrip("/").endswith(path.rstrip("/")):
                print("FAIL 301 inner", inner_url, "->", loc)
                fail += 1
                continue
        code, final, _, body = fetch(inner_url, follow=True)
        if code == 404 or code == 410 or len(body) < min_bytes:
            print("FAIL inner", inner_url, code, len(body), final)
            fail += 1
        else:
            print("inner", code, len(body), final)

    if fail:
        raise SystemExit(f"live_check failures: {fail}")
    print("live_check ok")


def main() -> None:
    if "--put" in sys.argv:
        put()
        return
    if "--check" in sys.argv:
        live_check()
        return
    generate()


if __name__ == "__main__":
    main()
