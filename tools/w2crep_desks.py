#!/usr/bin/env python3
"""W2CREP hub: surgical #local on unique 44KB catalog. No 5KB overlay.

Gates:
1. Hub #local has the HUB fingerprint, no dest-country fingerprints.
2. Estimator country ≠ TLD; .org must say it is not a customs territory.
   GSC is mixed CAN/ESP/FRA/NZL 1 click each — still a hub because the TLD
   is .org, not a customs dest. W2CREP is not an agent and has no freight
   form; cite the ranked shipping guide. Do not invent a free-day count.
3. Homepage title has no invite token. Body has no customs coaching /
   58-line snapshot. Coupon stacking stays on /w2crep-coupons/.
4. w2clinks.com is a unique PHP search CMS with a different job — stay
   independent, no 301 either way. Skip dest overlay of w2clinks.
5. Same-agent extras w2cclothes.com / w2cshoes.com already 301 $request_uri
   into this hub. Target must have #local first (this change). Deep extra
   paths must not 404 (they follow $request_uri onto ranked inners).
6. Unique 44KB catalog stays. Surgical #local insert only — do not PUT a
   5KB dest template over 25–73KB HTML.

Skip repsicon.com (thin Baota/Eyou leftover). Skip unique dest overwrite
of sugargoo.ca/.es. Do not invent warehouse days.
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
EST = "https://w2crep.org/w2crep-shipping-guide/"
OFFICIAL = "https://w2crep.org/"
HELP = "https://w2crep.org/how-to-use-w2crep/"
DATE = "2 Oct 2026"
INVITE = "___no_frozen_w2crep_invite___"
HUB_MIN = 40000
LIVE_HUB_MIN = 42000
STORAGE = (
    "W2CREP is not an agent warehouse. Storage days belong to the agent "
    f"you book. Ranked how-to on this host: {HELP}. "
    "Confirm that agent’s Help the morning you ship. "
    "This desk does not invent a free-day count."
)

HUBS = {
    "org": {
        "host": "w2crep.org",
        "public": "w2crep.org",
        "lang": "en",
        "loc": "en",
        "dest": None,
        "dest_label": "a country in the estimator",
        "ccy": "USD",
        "title": None,
        "h1": None,
        "keep": [
            ("/w2crep-spreadsheet/", "Spreadsheet"),
            ("/w2crep-coupons/", "Agent coupons"),
            ("/is-w2crep-legit/", "Is it legit?"),
            ("/w2crep-shipping-guide/", "Shipping"),
            ("/how-to-use-w2crep/", "How-to"),
        ],
    },
}

EST_NOTE = {
    "org": (
        "This .org hub is not a customs territory. Mixed CA/ES/FR/NZ clicks "
        "do not make .org a customs dest. W2CREP has no freight form. Pick "
        "the real ship-to country in the estimator of the agent you actually "
        "pay, not this hostname, not “EU” as one country."
    ),
}

STORE_NOTE = {
    "en": (
        "Warehouse: W2CREP is not an agent. Confirm storage on the agent you "
        "book. Do not invent a free-day count on this hub."
    ),
}

TRAIL = {"en": ("Live money is in", "this HTML is not checkout.")}

HUB_LOCAL_CSS = (
    ".sg-sec#local{max-width:1100px;margin:1.5rem auto;padding:0 24px;color:#111}"
    ".sg-sec#local h2{margin-top:0}"
    ".ssub{color:#555;font-size:.95rem;margin:0 0 12px}"
    ".local-src{font-size:14px;color:#2D2D2D;line-height:1.7;margin:14px 0 0}"
    ".local-src a{color:#1A56DB;text-decoration:underline}"
    "#local{scroll-margin-top:72px}"
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
    ("/w2crep-spreadsheet/", 20000),
    ("/w2crep-shipping-guide/", 20000),
    ("/w2crep-coupons/", 20000),
    ("/is-w2crep-legit/", 20000),
    ("/how-to-use-w2crep/", 8000),
    ("/blog/", 8000),
)

EXTRAS = (
    "w2cclothes.com",
    "w2cshoes.com",
)

HERO_END = (
    "</section>\n\n"
    '<section class="w2c-prose">\n'
    "  <h2>What does W2C mean on Reddit?</h2>"
)
NAV = '<ul class="nl">'
CHROME = (
    "Where to Cop Reps",
    "W2C Spreadsheet 2026",
    'class="hero fade-in"',
    "w2c-prose",
    'class="nl"',
)
HOST = "w2crep.org"
PUBLIC = "w2crep.org"
LINKS_HOST = "w2clinks.com"


def _facts(spec: dict) -> dict:
    return {
        "agent": "W2CREP",
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
            r"(<body>)",
            r"\1\n" + skip_link(skip_label(loc)).rstrip(),
            html,
            count=1,
        )
    if 'id="main"' not in html:
        html = html.replace(
            '<section class="hero fade-in">',
            '<section class="hero fade-in" id="main">',
            1,
        )
    cta = escape(local_cta(facts))
    if 'href="#local"' not in html:
        if NAV not in html:
            raise RuntimeError("hub nav missing")
        html = html.replace(
            NAV,
            NAV + f'<li><a href="#local">{cta}</a></li>',
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
        html = html.replace(
            HERO_END,
            "</section>\n" + block + "\n"
            '<section class="w2c-prose">\n'
            "  <h2>What does W2C mean on Reddit?</h2>",
            1,
        )
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
    bak = f"/www/backup/w2crep-desks-{stamp}"
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
        _run(client, f"cp -a '{remote}' '{bak}/{spec['host']}.index.html'")
        sftp.put(str(local), remote)
        print("PUT", remote, "bytes", local.stat().st_size)

        vhost = f"/www/server/panel/vhost/nginx/{spec['host']}.conf"
        _run(client, f"cp -a '{vhost}' '{bak}/{spec['host']}.conf'")
        vnow = _run(client, f"cat '{vhost}'")
        if "https://w2crep.org$request_uri" not in vnow:
            raise SystemExit("www/http missing 301 to apex $request_uri")
        if "return 410" in vnow:
            raise SystemExit("hub nginx has return 410")
        if "try_files $uri $uri/ $uri/index.html =404" not in vnow:
            raise SystemExit("hub nginx missing try_files")

        for extra in EXTRAS:
            extra_conf = f"/www/server/panel/vhost/nginx/{extra}.conf"
            eraw = _run(client, f"cat '{extra_conf}'")
            if "https://w2crep.org$request_uri" not in eraw:
                raise SystemExit(f"{extra} missing 301 $request_uri into hub")
            print("keep extra 301", extra)

        for rel, min_b in RANKED_CMS:
            inner = f"/www/wwwroot/{spec['host']}{rel}index.html"
            n = _run(client, f"wc -c < '{inner}' 2>/dev/null || echo 0")
            try:
                inner_n = int(n.strip().split()[0])
            except ValueError:
                inner_n = 0
            if inner_n and inner_n < min_b:
                raise SystemExit(f"unique CMS shrank {rel} {inner_n}")
            print("keep unique", rel, inner_n)

        links_php = _run(client, f"wc -c < /www/wwwroot/{LINKS_HOST}/index.php 2>/dev/null || echo 0")
        print("keep unique PHP", LINKS_HOST, links_php)

    nginx_t = _run(client, "nginx -t 2>&1")
    print(nginx_t)
    if "successful" not in nginx_t.lower() and "ok" not in nginx_t.lower():
        raise SystemExit("nginx -t failed; not reloading")
    print(_run(client, "nginx -s reload 2>&1"))
    sftp.close()
    print("backup", bak)
    print("unique 44KB CMS kept; extras still 301 $request_uri; w2clinks not overwritten")
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
                "User-Agent": "w2crep-desk-check/1.0",
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
        except Exception as e:
            return 0, url, "", str(e).encode()

    fail = 0
    url = f"https://{PUBLIC}/"
    code, _, loc, body = fetch(url, follow=True)
    html = body.decode("utf-8", "replace")
    title_m = re.search(r"<title>(.*?)</title>", html, flags=re.S)
    title = title_m.group(1) if title_m else ""
    inner_m = re.search(r'<section class="sg-sec" id="local".*?</section>', html, flags=re.S)
    inner = inner_m.group(0) if inner_m else ""
    fp = "not a customs territory"
    print(f"org {code} bytes={len(body)} local={bool(inner)} fp={fp in html}")
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
        print("FAIL hub 301", loc)
        fail += 1
    else:
        print("indep hub", code)

    for extra in EXTRAS:
        code, _, loc, _ = fetch(f"https://{extra}/", follow=False)
        if code in (301, 302, 303, 307, 308) and PUBLIC in (loc or "") and "w2clinks" not in (loc or "").lower():
            print("extra apex 301 hub", extra, code, loc)
        else:
            print("FAIL extra", extra, code, loc)
            fail += 1
        deep = "/w2crep-spreadsheet/"
        code, _, loc, _ = fetch(f"https://{extra}{deep}", follow=False)
        if code in (301, 302, 303, 307, 308) and PUBLIC in (loc or "") and deep.rstrip("/") in (loc or ""):
            print("extra deep $request_uri", extra, code, loc)
        else:
            print("FAIL extra deep", extra, code, loc)
            fail += 1

    code, _, loc, body = fetch(f"https://{LINKS_HOST}/", follow=False)
    if code in (301, 302, 303, 307, 308):
        print("FAIL unique PHP 301", loc)
        fail += 1
    elif code != 200 or len(body) < 15000:
        print("FAIL unique PHP", code, len(body))
        fail += 1
    else:
        print("indep unique PHP", LINKS_HOST, code, len(body))

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
