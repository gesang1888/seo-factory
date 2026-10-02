#!/usr/bin/env python3
"""DGoBuy desks: restore unique 37KB .com catalog; surgical #local.

Gates:
1. Hub #local has the HUB fingerprint, no dest-country fingerprints.
2. Estimator country ≠ TLD; .com must say it is not a customs territory.
   GSC is 0 clicks, mixed USA/GBR/GRC/JPN/TWN/ZAF impressions — still a hub.
3. Homepage title has no invite token; no frozen code. Body has no customs
   coaching / 58-line snapshot. Coupon stacking stays on /dgobuy-coupons/.
4. Single public dest host on origin — no same-agent country 301. www already
   301s to apex. No extra twins.
5. spam-p0 `return 410` hid unique 23–61KB CMS. Restore try_files so ranked
   URLs 200. No gsc-redirects — do not invent 301s. Deep paths must not 404.
6. Unique 37KB catalog stays. Surgical #local insert only — do not PUT a 5KB
   country template over 23–61KB CMS.

Official /en_US/freight-estimation and /en_US/help-center 200. Do not invent
a free-day count in #local.
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
EST = "https://dgobuy.com/en_US/freight-estimation"
OFFICIAL = "https://dgobuy.com/en_US"
HELP = "https://dgobuy.com/en_US/help-center"
DATE = "2 Oct 2026"
INVITE = "___no_frozen_dgobuy_invite___"
HUB_MIN = 30000
LIVE_HUB_MIN = 32000
STORAGE = (
    "Official DGoBuy Help is the live site "
    f"({HELP}); confirm that live copy the morning you ship. "
    "This desk does not invent a free-day count."
)

HUBS = {
    "com": {
        "host": "dgobuyspreadsheet.com",
        "lang": "en",
        "loc": "en",
        "dest": None,
        "dest_label": "a country in the estimator",
        "ccy": "USD",
        "title": None,
        "h1": None,
        "keep": [
            ("/dgobuy-coupons/", "Coupons"),
            ("/dgobuy-shipping-guide/", "Shipping"),
            ("/is-dgobuy-legit/", "Legit"),
            ("/dgobuy-spreadsheet/", "Spreadsheet"),
            ("/how-to-use-dgobuy/", "How to use"),
            ("/blog/", "Blog"),
        ],
    },
}

EST_NOTE = {
    "com": (
        "This .com hub is not a customs territory. Mixed US/GB/GR impressions "
        "do not make .com a customs dest. Pick the real ship-to country in the "
        "official estimator, not this hostname, not “EU” as one country."
    ),
}

STORE_NOTE = {
    "en": (
        "Warehouse: official DGoBuy Help. Confirm that live copy the morning "
        "you ship. Do not invent a free-day count on this hub."
    ),
}

TRAIL = {"en": ("Live money is in", "this HTML is not checkout.")}

HUB_LOCAL_CSS = (
    ".sg-sec#local{max-width:1100px;margin:1.5rem auto;padding:0 24px}"
    ".sg-sec#local h2{margin-top:0}"
    ".ssub{color:var(--g3,#555);font-size:.95rem;margin:0 0 12px}"
    ".local-steps{margin:12px 0 0;padding:0;list-style:none;display:grid;gap:12px}"
    ".local-steps li{border:1px solid #e5e7eb;border-radius:12px;padding:14px 16px;background:#fff}"
    ".local-steps strong{display:block;margin:0 0 6px;font-size:15px}"
    ".local-steps span{display:block;color:#334155;line-height:1.7;font-size:15px}"
    ".local-src{font-size:14px;color:#334155;line-height:1.7;margin:14px 0 0}"
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
    ("/dgobuy-coupons/", 20000),
    ("/dgobuy-shipping-guide/", 20000),
    ("/is-dgobuy-legit/", 20000),
    ("/dgobuy-spreadsheet/", 20000),
    ("/dgobuy-spreadsheet-2026/", 8000),
    ("/dgobuy-shoes-spreadsheet/", 8000),
    ("/how-to-use-dgobuy/", 8000),
    ("/blog/", 8000),
    ("/dgobuy-qc-guide/", 8000),
    ("/dgobuy-refund-guide/", 8000),
    ("/dgobuy-invite-code/", 8000),
    ("/dgobuy-community/", 8000),
)

KEEP_REDIRECTS: tuple[tuple[str, str], ...] = ()

HERO_END = "</section>\n\n<div class=\"trust\">"
NAV_UL = '<ul class="nl">'
CHROME = ('class="nav"', "hero fade-in", "nbrand", "DgoBuy", "ccard")
HOST = "dgobuyspreadsheet.com"


def _facts(spec: dict) -> dict:
    return {
        "agent": "DGoBuy",
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
        html = html.replace("<body>", "<body>\n" + skip_link(skip_label(loc)).rstrip(), 1)
    if 'id="main"' not in html:
        html = html.replace(
            '<section class="hero fade-in">',
            '<section class="hero fade-in" id="main">',
            1,
        )
    if 'href="#local"' not in html:
        if NAV_UL not in html:
            raise RuntimeError("hub nav missing")
        html = html.replace(
            NAV_UL,
            NAV_UL + f'<li><a href="#local">{escape(local_cta(facts))}</a></li>',
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
        html = html.replace(HERO_END, "</section>\n" + block + "\n<div class=\"trust\">", 1)
    err: list[str] = []
    _check_local_section(html, facts, err)
    title_m = re.search(r"<title>(.*?)</title>", html, flags=re.S)
    title = title_m.group(1) if title_m else ""
    if re.search(r"invite\s*(code)?\s*[A-Z0-9]{5,}", title, flags=re.I) or INVITE in title:
        err.append("invite in title")
    if INVITE in html:
        err.append("frozen invite token still on homepage")
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
        if re.search(r"90\s*dagen|90\s*days", inner, flags=re.I):
            raise SystemExit(f"{key} invented 90-day copy in #local")
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
    bak = f"/www/backup/dgobuy-desks-{stamp}"
    _run(client, f"mkdir -p '{bak}'")
    sftp = client.open_sftp()
    for spec in HUBS.values():
        local = OUT / spec["host"] / "overlay" / "index.html"
        remote = f"/www/wwwroot/{spec['host']}/index.html"
        raw = local.read_text(encoding="utf-8")
        if 'id="local"' not in raw or "not a customs territory" not in raw:
            raise SystemExit(f"refusing to PUT {spec['host']} without hub #local")
        if INVITE in raw:
            raise SystemExit(f"refusing to PUT {spec['host']} with frozen invite token")
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
        vraw = _run(client, f"cat '{vhost}'")
        new = vraw.replace(
            "    location / { return 410; }",
            "    location / { try_files $uri $uri/ $uri/index.html =404; }",
        )
        if new == vraw:
            new = vraw.replace(
                "    location / {\n        return 410;\n    }",
                "    location / {\n        try_files $uri $uri/ $uri/index.html =404;\n    }",
            )
        if "return 410" in new and "try_files $uri $uri/ $uri/index.html =404" not in new:
            raise SystemExit("hub nginx still 410 and restore did not match")
        if new != vraw:
            with sftp.file(vhost, "w") as fh:
                fh.write(new)
            print("restored vhost try_files (was 410)")
        else:
            print("hub nginx already serving")

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

    nginx_t = _run(client, "nginx -t 2>&1")
    print(nginx_t)
    if "successful" not in nginx_t.lower() and "ok" not in nginx_t.lower():
        raise SystemExit("nginx -t failed; not reloading")
    print(_run(client, "nginx -s reload 2>&1"))
    sftp.close()
    print("backup", bak)
    print("unique 37KB catalog kept; 410 restored; no dest overlay")
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
                "User-Agent": "dgobuy-desk-check/1.0",
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
    url = f"https://{HOST}/"
    code, _, loc, body = fetch(url, follow=True)
    html = body.decode("utf-8", "replace")
    title_m = re.search(r"<title>(.*?)</title>", html, flags=re.S)
    title = title_m.group(1) if title_m else ""
    inner_m = re.search(r'<section class="sg-sec" id="local".*?</section>', html, flags=re.S)
    inner = inner_m.group(0) if inner_m else ""
    fp = "not a customs territory"
    print(f"com {code} bytes={len(body)} local={bool(inner)} fp={fp in html}")
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
        if INVITE in title or INVITE in html:
            print("  FAIL invite on homepage")
            fail += 1
        if re.search(r"invite\s*(code)?\s*[A-Z0-9]{5,}", title, flags=re.I):
            print("  FAIL invite in title")
            fail += 1
        if re.search(r"58 l[ií]neas para Espa|23[,.]81\s*USD|how to under-?declar", html, flags=re.I):
            print("  FAIL snapshot/coaching")
            fail += 1
        if re.search(r"90\s*dagen|90\s*days", inner, flags=re.I):
            print("  FAIL invented 90-day copy")
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

    for path, min_bytes in RANKED_CMS:
        inner_url = f"https://{HOST}{path}"
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

    code, _, loc, _ = fetch(f"https://www.{HOST}/", follow=False)
    if code in (301, 302, 303, 307, 308) and HOST in (loc or ""):
        print("www apex", code, loc)
    else:
        print("www", code, loc)
        if code not in (301, 302, 308):
            fail += 1

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
