#!/usr/bin/env python3
"""JoyaGoo DE dest: surgical #local on unique 31KB W2C CMS. No 5KB overlay.

Gates:
1. Dest #local has Packstation; no sister fingerprints.
2. Estimator country is DE (matches .de ccTLD — not a .eu/.net/.com hub).
   Do NOT write “not a customs territory”. GSC SA is 403; dest chosen by
   ccTLD. Official joyagoo.com is Cloudflare-challenged 403 from this lab;
   cite the homepage. Do not invent a free-day count.
3. Homepage title has no invite token. Frozen ref=301011774 is stripped
   from home only; stacking stays on /guides/coupons/. No customs coaching
   / 58-line snapshot.
4. Same-agent CA dest joyagoospreadsheet.ca is a unique ~32KB host (not on
   this origin). Skip unique dest overwrite. DE and CA stay independently
   open — no 301 either way. www currently SNI-falls onto ACBuy CA — add
   www 301 apex $request_uri.
5. No twins on origin. spam-update-p0 rewrite `return 410;` restored so
   ranked inners 200. Deep www paths keep $request_uri onto this dest, not
   another agent.
6. Unique 31KB W2C CMS stays. Surgical #local insert only — do not PUT a
   5KB dest template over 9–31KB HTML.

Official Help/estimator are behind a Cloudflare challenge from this VM.
Cite https://joyagoo.com/ ; do not invent warehouse days.
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
EST = "https://joyagoo.com/"
OFFICIAL = "https://joyagoo.com/"
HELP = "https://joyagoo.com/"
DATE = "2 Oct 2026"
INVITE = "301011774"
HUB_MIN = 30000
LIVE_HUB_MIN = 32000
STORAGE = (
    "Official JoyaGoo is the live site "
    f"({HELP}); from this lab Cloudflare answers 403 challenge. "
    "Confirm the live copy the morning you ship. "
    "This desk does not invent a free-day count."
)

DESTS = {
    "de": {
        "host": "joyagoospreadsheets.de",
        "public": "joyagoospreadsheets.de",
        "lang": "de",
        "loc": "de",
        "dest": "DE",
        "dest_label": "Deutschland",
        "ccy": "EUR",
        "title": None,
        "h1": None,
        "keep": [
            ("/spreadsheet/", "Spreadsheet"),
            ("/guides/coupons/", "Coupons (Codes bleiben dort)"),
            ("/guides/is-joyagoo-legit/", "Ist Joyagoo seriös?"),
            ("/guides/shipping/", "Versand"),
            ("/guides/how-to-use/", "How-to"),
        ],
    },
}

EST_NOTE = {
    "de": (
        "Im offiziellen Formular das Land DE wählen, nicht EU als ein Land, "
        "nicht diesen Hostnamen anstelle der PLZ. Eine österreichische "
        "vierstellige Postleitzahl ist das falsche Land."
    ),
}

STORE_NOTE = {
    "de": (
        "Lager: offizielles JoyaGoo. Von diesem Labor antwortet Cloudflare "
        "mit 403. Bestätige die Live-Kopie am Versandmorgen. Keine erfundenen "
        "kostenlosen Lagertage auf diesem Desk."
    ),
}

TRAIL = {"de": ("Live-Preis steht in", "dieses HTML ist keine Kasse.")}

DEST_LOCAL_CSS = (
    ".sg-sec#local{max-width:1100px;margin:1.5rem auto;padding:0 24px;color:#111}"
    ".sg-sec#local h2{margin-top:0}"
    ".ssub{color:#6b7280;font-size:.95rem;margin:0 0 12px}"
    ".local-src{font-size:14px;color:#374151;line-height:1.7;margin:14px 0 0}"
    ".local-src a{color:#c2410c;text-decoration:underline}"
    "#local{scroll-margin-top:96px}"
)

ALIENS = (
    "1010 Wien",
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
    "not a customs territory",
)

RANKED_CMS = (
    ("/spreadsheet/", 8000),
    ("/guides/is-joyagoo-legit/", 8000),
    ("/guides/shipping/", 8000),
    ("/guides/coupons/", 8000),
    ("/guides/how-to-use/", 8000),
    ("/guides/qc/", 8000),
    ("/category/sneakers/", 8000),
    ("/brand/nike/", 8000),
)

HERO_END = (
    '    <p class="w2c-hero-tag">Live-Tabelle auf W2C Links</p>\n'
    "  </div>\n"
    "</section>\n"
    '<section class="w2c-section"><div class="w2c-wrap"><div class="w2c-cat-grid w2c-cat-grid-icons">'
)
NAV = '<nav class="w2c-nav" id="w2c-nav">'
CHROME = (
    'class="w2c-body"',
    "w2c-hero",
    "Joyagoo Spreadsheet — Deutschland 2026",
    "data-w2c-products",
    'id="w2c-nav"',
)
HOST = "joyagoospreadsheets.de"
PUBLIC = "joyagoospreadsheets.de"
CA_HOST = "joyagoospreadsheet.ca"

WWW_BLOCK = """server {
    listen 80;
    listen 443 ssl;
    http2 on;
    server_name www.joyagoospreadsheets.de;
    ssl_certificate    /www/server/panel/vhost/cert/joyagoospreadsheets.de/fullchain.pem;
    ssl_certificate_key    /www/server/panel/vhost/cert/joyagoospreadsheets.de/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    include /www/server/panel/vhost/nginx/well-known/joyagoospreadsheets.de.conf;
    return 301 https://joyagoospreadsheets.de$request_uri;
}

"""

REWRITE_RESTORE = "# restored after spam-update-p0 410; default file serving\n"


def _facts(spec: dict) -> dict:
    return {
        "agent": "JoyaGoo",
        "host": spec["host"],
        "lang": spec["lang"],
        "loc": spec["loc"],
        "dest": spec.get("dest"),
        "dest_label": spec.get("dest_label") or "Deutschland",
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
    store = STORE_NOTE.get(loc) or STORE_NOTE["de"]
    live, not_co = TRAIL.get(loc) or TRAIL["de"]
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


def _scrub_home_invite(html: str) -> str:
    html = html.replace(
        "https://joyagoo.com/register?ref=301011774",
        "https://joyagoo.com/register",
    )
    html = html.replace("?ref=301011774", "")
    html = html.replace("ref=301011774", "")
    html = html.replace(INVITE, "")
    return html


def patch_static(html: str, key: str, spec: dict) -> str:
    facts = _facts(spec)
    html = _scrub_home_invite(html)
    block = _local_block(key, spec)
    loc = spec["loc"]
    if 'class="skip"' not in html:
        html = re.sub(
            r'(<body class="w2c-body">)',
            r"\1\n" + skip_link(skip_label(loc)).rstrip(),
            html,
            count=1,
        )
    if 'id="main"' not in html:
        html = html.replace("<main>", '<main id="main">', 1)
    cta = escape(local_cta(facts))
    if 'href="#local"' not in html:
        if NAV not in html:
            raise RuntimeError("dest nav missing")
        html = html.replace(
            NAV,
            NAV + f'\n      <a href="#local">{cta}</a>',
            1,
        )
    if "#local{scroll-margin-top" not in html:
        if "</style>" in html:
            html = html.replace("</style>", SKIP_CSS + DEST_LOCAL_CSS + "\n</style>", 1)
        else:
            html = html.replace(
                "</head>",
                "<style>" + SKIP_CSS + DEST_LOCAL_CSS + "</style>\n</head>",
                1,
            )
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
            raise RuntimeError("dest hero marker missing")
        html = html.replace(
            HERO_END,
            '    <p class="w2c-hero-tag">Live-Tabelle auf W2C Links</p>\n'
            "  </div>\n"
            "</section>\n"
            + block
            + "\n"
            + '<section class="w2c-section"><div class="w2c-wrap"><div class="w2c-cat-grid w2c-cat-grid-icons">',
            1,
        )
    err: list[str] = []
    _check_local_section(html, facts, err)
    title_m = re.search(r"<title>(.*?)</title>", html, flags=re.S)
    title = title_m.group(1) if title_m else ""
    if INVITE in title or re.search(r"invite\s*(code)?\s*[A-Z0-9]{5,}", title, flags=re.I):
        err.append("invite in title")
    if re.search(r"invite\b", title, flags=re.I):
        err.append("leftover invite word in title")
    if INVITE in html:
        err.append("frozen invite token on dest homepage")
    if re.search(r"58 l[ií]neas para Espa|23[,.]81\s*USD|how to under-?declar", html, flags=re.I):
        err.append("spain snapshot / coaching")
    fp = dest_local_pack("DE")["fingerprint"]
    if fp not in html:
        err.append("missing dest fingerprint")
    if "not a customs territory" in html:
        err.append(".de dest must not claim it is not a customs territory")
    if len(html.encode("utf-8")) < HUB_MIN:
        err.append(f"unique dest collapsed to {len(html.encode('utf-8'))} bytes")
    for marker in CHROME:
        if marker not in html:
            err.append(f"dest chrome missing {marker}")
    if err:
        raise RuntimeError(f"{key}: {'; '.join(err)}")
    return html


def generate() -> None:
    assert_dest_packs_unique()
    blobs = {}
    specs = {**DESTS}
    for key, spec in specs.items():
        src = OUT / spec["host"] / "live-base" / "index.html"
        html = patch_static(src.read_text(encoding="utf-8"), key, spec)
        dest = OUT / spec["host"] / "overlay" / "index.html"
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(html, encoding="utf-8")
        inner = re.search(r'<section class="sg-sec" id="local".*?</section>', html, flags=re.S)
        blobs[key] = inner.group(0) if inner else ""
        print("dest", key, spec["host"], "bytes", len(html.encode("utf-8")))
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
        if "not a customs territory" in inner:
            raise SystemExit(f"{key} .de dest wrote hub customs-territory line")
        if INVITE in inner:
            raise SystemExit(f"{key} #local still has invite token")
        if re.search(r"90\s*dagen|90\s*days|60\s*-?\s*day|90\s*Tage", inner, flags=re.I):
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
    bak = f"/www/backup/joyagoo-desks-{stamp}"
    _run(client, f"mkdir -p '{bak}'")
    sftp = client.open_sftp()
    for spec in DESTS.values():
        local = OUT / spec["host"] / "overlay" / "index.html"
        remote = f"/www/wwwroot/{spec['host']}/index.html"
        raw = local.read_text(encoding="utf-8")
        if 'id="local"' not in raw or "Packstation" not in raw:
            raise SystemExit(f"refusing to PUT {spec['host']} without DE #local")
        if INVITE in raw:
            raise SystemExit(f"refusing to PUT {spec['host']} with invite on dest home")
        if "not a customs territory" in raw:
            raise SystemExit(f"refusing to PUT {spec['host']} with hub fingerprint")
        if local.stat().st_size < HUB_MIN:
            raise SystemExit(f"refusing to PUT collapsed dest {local.stat().st_size} B")
        for marker in CHROME:
            if marker not in raw:
                raise SystemExit(f"refusing to PUT dest missing chrome {marker}")
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
        if "server_name www.joyagoospreadsheets.de" not in vraw:
            if not vraw.startswith("server"):
                raise SystemExit("unexpected vhost prefix")
            with sftp.file(vhost, "w") as fh:
                fh.write(WWW_BLOCK + vraw)
            print("added www 301 apex $request_uri")
        else:
            print("www already mapped")

        rewrite = f"/www/server/panel/vhost/rewrite/{spec['host']}.conf"
        _run(client, f"cp -a '{rewrite}' '{bak}/{spec['host']}.rewrite.conf'")
        with sftp.file(rewrite, "w") as fh:
            fh.write(REWRITE_RESTORE)
        print("restored rewrite (was return 410)")
        rnow = _run(client, f"cat '{rewrite}'")
        if "return 410" in rnow:
            raise SystemExit("rewrite still has return 410 after restore")

        vnow = _run(client, f"cat '{vhost}'")
        if "https://joyagoospreadsheets.de$request_uri" not in vnow:
            raise SystemExit("www missing 301 apex $request_uri")
        if "server_name www.joyagoospreadsheets.de" not in vnow:
            raise SystemExit("www server_name missing after PUT")

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
    print("unique 31KB CMS kept; rewrite 410 restored; no dest overlay; CA not overwritten")
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
                "User-Agent": "joyagoo-desk-check/1.0",
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
    fp = "Packstation"
    print(f"de {code} bytes={len(body)} local={bool(inner)} fp={fp in html}")
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
        if INVITE in title or re.search(r"invite\s*(code)?\s*[A-Z0-9]{5,}", title, flags=re.I):
            print("  FAIL invite in title")
            fail += 1
        if INVITE in html:
            print("  FAIL invite on dest homepage")
            fail += 1
        if re.search(r"58 l[ií]neas para Espa|23[,.]81\s*USD|how to under-?declar", html, flags=re.I):
            print("  FAIL snapshot/coaching")
            fail += 1
        if re.search(r"90\s*dagen|90\s*days|60\s*-?\s*day|90\s*Tage", inner, flags=re.I):
            print("  FAIL invented free-day copy")
            fail += 1
        if EST not in inner:
            print("  FAIL estimator")
            fail += 1
        if "not a customs territory" in inner:
            print("  FAIL .de wrote hub customs-territory line")
            fail += 1
        if len(body) < LIVE_HUB_MIN:
            print("  FAIL unique dest collapsed", len(body))
            fail += 1
        for marker in CHROME:
            if marker not in html:
                print("  FAIL dest chrome gone", marker)
                fail += 1

    code, _, loc, _ = fetch(url, follow=False)
    if code in (301, 302, 303, 307, 308):
        print("FAIL dest 301", loc)
        fail += 1
    else:
        print("indep dest", code)

    code, _, loc, _ = fetch("https://www.joyagoospreadsheets.de/", follow=False)
    if code in (301, 302, 303, 307, 308) and PUBLIC in (loc or "") and "acbuy" not in (loc or "").lower():
        print("www apex", code, loc)
    else:
        print("FAIL www", code, loc)
        fail += 1

    deep = "/spreadsheet/"
    code, _, loc, _ = fetch(f"https://www.joyagoospreadsheets.de{deep}", follow=False)
    if (
        code in (301, 302, 303, 307, 308)
        and PUBLIC in (loc or "")
        and deep.rstrip("/") in (loc or "")
        and "acbuy" not in (loc or "").lower()
    ):
        print("www deep $request_uri", code, loc)
    else:
        print("FAIL www deep", code, loc)
        fail += 1

    code, _, loc, body = fetch(f"https://{CA_HOST}/", follow=False)
    if code in (301, 302, 303, 307, 308):
        print("FAIL CA unique dest 301", loc)
        fail += 1
    elif code != 200 or len(body) < 20000:
        print("FAIL CA unique dest", code, len(body))
        fail += 1
    else:
        print("indep CA unique dest", code, len(body), "(overwrite skipped)")

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

    coupons = f"https://{PUBLIC}/guides/coupons/"
    code, _, _, body = fetch(coupons, follow=True)
    cht = body.decode("utf-8", "replace")
    if code == 200 and INVITE in cht:
        print("coupons stacking kept", INVITE)
    elif code == 200:
        print("WARN coupons missing stacking token (left as-is)")
    else:
        print("FAIL coupons", code)
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
