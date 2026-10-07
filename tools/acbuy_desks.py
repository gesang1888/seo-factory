#!/usr/bin/env python3
"""ACBuy CA/NL desks: surgical NL dest #local; twin catch-all $request_uri.

Gates:
1. NL #local has Nederlandse postcode, no sister dest fingerprints.
   ACBuy CA dest is acbuyspreadsheets.ca (independent). AllChinaBuy CA
   dest allchinabuyspreadsheet.ca stays its own host — different agent.
2. Estimator country ≠ TLD. NL picks NL, not EU, not BE, not the .com hub.
   Official Help is a 2KB SPA shell — do not invent a free-day count.
3. Titles have no invite token. Homepage strips frozen 5F2RRA. Body has no
   customs coaching / 58-line snapshot. Coupon stacking stays on
   /acbuy-coupons/ and /acbuy-invite-code/ (do not TITLE_SCRUB those).
4. CA dest and NL dest stay independent (no 301 between countries).
   Skip acbuy.cheap (no DNS, no vhost).
5. AllChinaBuy is a different agent: do not 301 allchinabuyspreadsheet.nl
   into acbuyspreadsheets.nl, or acbuyspreadsheets.ca into AllChinaBuy CA.
6. Unique 25–58KB CMS stays. Georgia NL home (~6.5KB) gets surgical #local
   only — never PUT a 5KB overlay over unique inners, CA extra, or the
   AllChinaBuy .com hub.

Official /estimation/ and /help 200 as SPA shells. Confirm Help live; do not
invent 90 warehouse days.
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
EST = "https://www.acbuy.com/estimation/"
OFFICIAL = "https://www.acbuy.com/"
HELP = "https://www.acbuy.com/help"
DATE = "2 Oct 2026"
INVITE = "5F2RRA"
INVITE2 = "EwjrSk"
DEST_MIN = 6000
LIVE_DEST_MIN = 6500
STORAGE = (
    "Official ACBuy Help is the live site "
    f"({HELP}); confirm that live copy the morning you ship. "
    "This desk does not invent a free-day count."
)

DESTS = {
    "nl": {
        "host": "acbuyspreadsheets.nl",
        "lang": "nl-NL",
        "loc": "nl",
        "dest": "NL",
        "dest_label": "Nederland",
        "ccy": "EUR",
        "title": "ACBuy Nederland — Nederlandse postcode, geen Duitse automaat",
        "h1": "ACBuy voor een Nederlands adres (EUR, Nederlandse postcode)",
        "chrome": (
            "niet AllChinaBuy",
            "Nederlandse postcode",
            "ACBuy",
        ),
        "keep": [
            ("/is-acbuy-legit/", "Review NL"),
            ("/acbuy-shipping-guide/", "Verzending"),
            ("/acbuy-coupons/", "Coupons"),
            ("/how-to-use-acbuy/", "Handleiding"),
        ],
        "ranked": (
            ("/is-acbuy-legit/", 20000),
            ("/acbuy-shipping-guide/", 20000),
            ("/acbuy-coupons/", 20000),
            ("/acbuy-spreadsheet/", 20000),
            ("/acbuy-invite-code/", 8000),
            ("/how-to-use-acbuy/", 8000),
            ("/blog/", 8000),
        ),
    },
    "ca": {
        "host": "allchinabuyspreadsheet.ca",
        "lang": "en-CA",
        "loc": "en",
        "dest": "CA",
        "dest_label": "Canada",
        "ccy": "CAD",
        "title": "AllChinaBuy Canada — Canada Post, CAD, CBSA notes",
        "h1": "AllChinaBuy for a Canadian delivery address (CAD, form A1A 1A1)",
        "chrome": (
            "form A1A 1A1",
            "CBSA",
            "AllChinaBuy",
        ),
        "keep": [
            ("/allchinabuy-shipping-guide/", "Shipping CA"),
            ("/is-allchinabuy-legit/", "Is it legit?"),
            ("/allchinabuy-spreadsheet/", "Spreadsheet"),
            ("/allchinabuy-coupons/", "Coupons article"),
        ],
        "ranked": (
            ("/allchinabuy-shipping-guide/", 20000),
            ("/is-allchinabuy-legit/", 20000),
            ("/allchinabuy-spreadsheet/", 20000),
            ("/allchinabuy-coupons/", 20000),
            ("/how-to-use-allchinabuy/", 8000),
        ),
    },
}

# AllChinaBuy and ACBuy are different agents. Never 301 their hosts together.
CONVERT_TWINS = {}

CA_TARGET = "allchinabuyspreadsheet.ca"
NL_HOST = "acbuyspreadsheets.nl"

EST_NOTE = {
    "nl": (
        "Estimator-land is NL, niet deze TLD, niet EU, niet BE, niet het .com-hub."
    ),
    "ca": (
        "Estimator country is CA, not this TLD, not US, not the .com hub."
    ),
}

STORE_NOTE = {
    "nl": (
        "Magazijn: officiële ACBuy Help. Bevestig die live-tekst op de verzenddag. "
        "Deze desk verzint geen gratis-dagen-aantal."
    ),
    "en": (
        "Warehouse: official ACBuy Help. Confirm that live copy the morning you ship. "
        "This desk does not invent a free-day count."
    ),
}

TRAIL = {
    "nl": ("Live-geld staat in", "deze HTML is geen kassa."),
    "en": ("Live money is in", "this HTML is not checkout."),
}

DEST_LOCAL_CSS = (
    ".sg-sec#local{margin:1.25rem 0 0}"
    ".sg-sec#local h2{margin-top:0}"
    ".ssub{color:var(--muted,#57534e);font-size:.95rem;margin:0 0 12px}"
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
    "does not invent a de-minimis dollar",
    "Northern Ireland is often another",
    "do not copy a GST rate",
    "not a customs territory",
)

NAV_END = "</nav>"


def _facts(spec: dict) -> dict:
    return {
        "agent": "ACBuy",
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
        "codes_off_title": [INVITE, INVITE2],
        "strict_html_codes": True,
    }


def _local_block(key: str, spec: dict) -> str:
    facts = _facts(spec)
    loc = spec["loc"]
    fp = dest_local_pack(facts.get("dest"))["fingerprint"]
    store = STORE_NOTE.get(loc) or STORE_NOTE.get("en", "")
    live, not_co = TRAIL.get(loc) or TRAIL.get("en", ("Live money is in", "this HTML is not checkout."))
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


def _scrub_token_from_home(html: str) -> str:
    html = html.replace(
        '<p class="note">ACBuy · haul-log Nederland · code 5F2RRA · niet AllChinaBuy</p>',
        '<p class="note">ACBuy · haul-log Nederland · niet AllChinaBuy</p>',
    )
    html = html.replace(
        '<a href="/acbuy-coupons/">5F2RRA</a>',
        '<a href="/acbuy-coupons/">Coupons</a>',
    )
    html = html.replace(
        "Coupon 5F2RRA op /acbuy-coupons/.",
        "Coupons op /acbuy-coupons/.",
    )
    html = html.replace(
        '<a href="/acbuy-coupons/">/acbuy-coupons/</a> publiceert <code>5F2RRA</code>.',
        '<a href="/acbuy-coupons/">/acbuy-coupons/</a> houdt de coupon-stacking (niet op deze homepage).',
    )
    html = html.replace(
        "<td>Invite</td><td><code>5F2RRA</code> uit het coupon-CMS, daarna in de wallet checken.</td>",
        "<td>Coupons</td><td>Stacking blijft op /acbuy-coupons/ — deze homepage drukt geen token.</td>",
    )
    html = html.replace(
        "Couponartikel — <code>5F2RRA</code> zoals de pagina hem nu toont.",
        "Couponartikel — stacking blijft op /acbuy-coupons/, niet op deze homepage.",
    )
    html = html.replace(
        'Partner code <code>EwjrSk</code> when <a href="/allchinabuy-coupons/">/allchinabuy-coupons/</a> still shows it.',
        'Coupon stacking stays on <a href="/allchinabuy-coupons/">/allchinabuy-coupons/</a> (not on this homepage).',
    )
    html = html.replace(
        'hreflang="nl-NL" href="https://allchinabuyspreadsheet.nl/"',
        'hreflang="nl-NL" href="https://acbuyspreadsheets.nl/"',
    )
    html = html.replace(INVITE, "")
    html = html.replace(INVITE2, "")
    html = re.sub(r"90 dagen gratis", "Help-tekst (geen verzonnen dagen)", html, flags=re.I)
    html = re.sub(r"90 free (warehouse )?days", "Help live copy (no invented days)", html, flags=re.I)
    return html


def _strip_invite_title(html: str, new_title: str | None = None) -> str:
    def scrub(s: str) -> str:
        s = re.sub(re.escape(INVITE) + r"[,]?\s*", "", s, flags=re.I)
        s = re.sub(r"(?i)\s*[—\-–:,]*\s*invite\b", "", s)
        s = re.sub(r"\s{2,}", " ", s).strip(" —–-,;")
        return s

    def title_sub(m):
        if new_title:
            return f"<title>{escape(new_title)}</title>"
        return f"<title>{scrub(m.group(1))}</title>"

    html = re.sub(r"<title>(.*?)</title>", title_sub, html, count=1, flags=re.S)
    html = re.sub(
        r'(<meta property="og:title" content=")([^"]+)(")',
        lambda m: m.group(1) + (new_title or scrub(m.group(2))) + m.group(3),
        html,
        count=1,
    )
    return html


def patch_static(html: str, key: str, spec: dict) -> str:
    facts = _facts(spec)
    block = _local_block(key, spec)
    loc = spec["loc"]
    html = _scrub_token_from_home(html)
    html = _strip_invite_title(html, spec.get("title"))
    if spec.get("h1"):
        html = re.sub(r"<h1>.*?</h1>", f"<h1>{escape(spec['h1'])}</h1>", html, count=1, flags=re.S)
    if 'class="skip"' not in html:
        html = html.replace("<body>", "<body>\n" + skip_link(skip_label(loc)).rstrip(), 1)
    if 'id="main"' not in html:
        html = html.replace("<main>", '<main id="main">', 1)
    if 'href="#local"' not in html and NAV_END in html:
        html = html.replace(
            NAV_END,
            f'    <a href="#local">{escape(local_cta(facts))}</a>\n  </nav>',
            1,
        )
    if "#local{scroll-margin-top" not in html:
        if "</style>" in html:
            html = html.replace("</style>", SKIP_CSS + DEST_LOCAL_CSS + "\n</style>", 1)
        else:
            html = html.replace("</head>", "<style>" + SKIP_CSS + DEST_LOCAL_CSS + "</style>\n</head>", 1)
    if 'id="local"' in html:
        html = re.sub(
            r'<section class="sg-sec" id="local".*?</section>',
            block,
            html,
            count=1,
            flags=re.S,
        )
    else:
        html = re.sub(r"(<h1>.*?</h1>)", r"\1\n" + block, html, count=1, flags=re.S)
    err: list[str] = []
    _check_local_section(html, facts, err)
    title_m = re.search(r"<title>(.*?)</title>", html, flags=re.S)
    title = title_m.group(1) if title_m else ""
    if INVITE in title or INVITE in html or INVITE2 in title or INVITE2 in html:
        err.append("frozen invite token still on homepage")
    if re.search(r"90\s*dagen|90\s*days", html, flags=re.I):
        err.append("invented 90-day warehouse copy")
    if re.search(r"58 l[ií]neas para Espa|23[,.]81\s*USD|how to under-?declar", html, flags=re.I):
        err.append("spain snapshot / coaching")
    if re.search(r"impressions on a template", html, flags=re.I):
        err.append("template-impressions copy")
    if len(html.encode("utf-8")) < DEST_MIN:
        err.append(f"dest collapsed to {len(html.encode('utf-8'))} bytes")
    for marker in spec.get("chrome") or ():
        if marker not in html:
            err.append(f"chrome missing {marker}")
    if err:
        raise RuntimeError(f"{key}: {'; '.join(err)}")
    return html


def generate() -> None:
    assert_dest_packs_unique()
    blobs = {}
    for key, spec in DESTS.items():
        src = OUT / spec["host"] / "live-base" / "index.html"
        html = patch_static(src.read_text(encoding="utf-8"), key, spec)
        dest = OUT / spec["host"] / "overlay" / "index.html"
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(html, encoding="utf-8")
        inner = re.search(r'<section class="sg-sec" id="local".*?</section>', html, flags=re.S)
        blobs[key] = inner.group(0) if inner else ""
        print("dest", key, spec["host"], "bytes", len(html.encode("utf-8")))
    fps = {k: dest_local_pack(DESTS[k]["dest"])["fingerprint"] for k in blobs}
    for key, inner in blobs.items():
        fp = fps[key]
        if fp not in inner:
            raise SystemExit(f"{key} missing fingerprint {fp!r}")
        for alien in ALIENS:
            if alien == fp:
                continue
            if alien in inner:
                raise SystemExit(f"{key} leaked sister {alien!r}")
        if EST not in inner:
            raise SystemExit(f"{key} missing estimator")
        if INVITE in inner or INVITE2 in inner:
            raise SystemExit(f"{key} invite in #local")
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


def patch_twins(client) -> None:
    changed = 0
    sftp = client.open_sftp()
    for twin, target in CONVERT_TWINS.items():
        path = f"/www/server/panel/vhost/nginx/{twin}.conf"
        raw = _run(client, f"cat '{path}'")
        if not raw:
            print("skip missing", twin)
            continue
        needle = f"    location / {{ return 301 https://{target}/; }}"
        want = f"    location / {{ return 301 https://{target}$request_uri; }}"
        if want in raw:
            print("twin catch-all already $request_uri", twin)
            continue
        if needle not in raw:
            print("skip no catch-all needle", twin)
            continue
        _run(client, f"cp -a '{path}' '/www/backup/acbuy-twin-{twin}.conf'")
        raw = raw.replace(needle, want)
        with sftp.open(path, "w") as fh:
            fh.write(raw)
        changed += 1
        print("PATCH nginx", twin, "catch-all $request_uri →", target)
    sftp.close()
    if changed:
        nginx_t = _run(client, "nginx -t 2>&1")
        print(nginx_t)
        if "successful" not in nginx_t.lower() and "ok" not in nginx_t.lower():
            raise SystemExit("nginx -t failed after twin patch; not reloading")
        print(_run(client, "nginx -s reload 2>&1"))


def put() -> None:
    generate()
    client = _connect()
    stamp = time.strftime("%Y%m%d-%H%M%S")
    bak = f"/www/backup/acbuy-desks-{stamp}"
    _run(client, f"mkdir -p '{bak}'")
    sftp = client.open_sftp()
    for spec in DESTS.values():
        local = OUT / spec["host"] / "overlay" / "index.html"
        remote = f"/www/wwwroot/{spec['host']}/index.html"
        raw = local.read_text(encoding="utf-8")
        if 'id="local"' not in raw:
            raise SystemExit(f"refusing to PUT {spec['host']} without #local")
        fp = dest_local_pack(spec["dest"])["fingerprint"]
        if fp not in raw:
            raise SystemExit(f"refusing to PUT {spec['host']} without dest fingerprint")
        if INVITE in raw or INVITE2 in raw:
            raise SystemExit(f"refusing to PUT {spec['host']} with frozen invite token")
        if re.search(r"90\s*dagen|90\s*days", raw, flags=re.I):
            raise SystemExit(f"refusing to PUT {spec['host']} with invented 90-day copy")
        if local.stat().st_size < DEST_MIN:
            raise SystemExit(f"refusing to PUT collapsed dest {local.stat().st_size} B")
        live = _run(client, f"wc -c < '{remote}'")
        try:
            live_n = int(live.strip().split()[0])
        except ValueError:
            live_n = 0
        if live_n > 15000:
            raise SystemExit(f"refusing to PUT over unique CMS home {live_n} B")
        for marker in spec.get("chrome") or ():
            if marker not in raw:
                raise SystemExit(f"refusing to PUT dest missing chrome {marker}")
        _run(client, f"cp -a '{remote}' '{bak}/{spec['host']}.index.html'")
        sftp.put(str(local), remote)
        print("PUT", remote, "bytes", local.stat().st_size)
        for rel, min_b in spec.get("ranked") or ():
            inner = f"/www/wwwroot/{spec['host']}{rel}index.html"
            n = _run(client, f"wc -c < '{inner}' 2>/dev/null || echo 0")
            try:
                inner_n = int(n.strip().split()[0])
            except ValueError:
                inner_n = 0
            if inner_n and inner_n < min_b:
                raise SystemExit(f"unique CMS shrank {rel} {inner_n}")
            print("keep unique", rel, inner_n)
    sftp.close()
    patch_twins(client)
    print("backup", bak)
    print("NL dest surgical; unique CMS kept; CA extra not overwritten; cheap skipped")
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
                "User-Agent": "acbuy-desk-check/1.0",
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
    for key, spec in DESTS.items():
        url = f"https://{spec['host']}/"
        code, _, loc, body = fetch(url, follow=True)
        html = body.decode("utf-8", "replace")
        title_m = re.search(r"<title>(.*?)</title>", html, flags=re.S)
        title = title_m.group(1) if title_m else ""
        inner_m = re.search(r'<section class="sg-sec" id="local".*?</section>', html, flags=re.S)
        inner = inner_m.group(0) if inner_m else ""
        fp = dest_local_pack(spec["dest"])["fingerprint"]
        print(f"{key} {code} bytes={len(body)} local={bool(inner)} fp={fp in html}")
        if code != 200 or not inner or fp not in inner:
            print("  FAIL status/local/fp")
            fail += 1
        else:
            for alien in ALIENS:
                if alien == fp:
                    continue
                if alien in inner:
                    print("  FAIL sister", alien)
                    fail += 1
            if INVITE in title or INVITE in html or INVITE2 in title or INVITE2 in html:
                print("  FAIL invite on homepage")
                fail += 1
            if re.search(r"90\s*dagen|90\s*days", html, flags=re.I):
                print("  FAIL invented 90-day copy")
                fail += 1
            if re.search(r"58 l[ií]neas para Espa|23[,.]81\s*USD|how to under-?declar", html, flags=re.I):
                print("  FAIL snapshot/coaching")
                fail += 1
            if EST not in inner:
                print("  FAIL estimator")
                fail += 1
            if len(body) < LIVE_DEST_MIN:
                print("  FAIL dest collapsed", len(body))
                fail += 1
            for marker in spec.get("chrome") or ():
                if marker not in html:
                    print("  FAIL chrome gone", marker)
                    fail += 1

        code, _, loc, _ = fetch(url, follow=False)
        if code in (301, 302, 303, 307, 308):
            print("FAIL dest 301", spec["host"], loc)
            fail += 1
        else:
            print("indep", key, code)

        for path, min_bytes in spec.get("ranked") or ():
            inner_url = f"https://{spec['host']}{path}"
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

    for twin, target in CONVERT_TWINS.items():
        code, _, loc, _ = fetch(f"https://{twin}/", follow=False)
        print("twin", twin, code, loc)
        if code not in (301, 302, 308) or target not in (loc or ""):
            print("  FAIL twin 301")
            fail += 1
        if twin.endswith(".ca"):
            deep = f"https://{twin}/acbuy-coupons/"
        else:
            deep = f"https://{twin}/acbuy-coupons/"
        code2, final2, loc2, body2 = fetch(deep, follow=False)
        print("  deep-nofollow", twin, code2, loc2)
        if code2 not in (301, 302, 308):
            print("  FAIL deep not 301")
            fail += 1
        elif twin.endswith(".nl") and "/acbuy-coupons" not in (loc2 or ""):
            print("  FAIL extra /acbuy-coupons/ dropped path", loc2)
            fail += 1
        elif twin.endswith(".ca") and "allchinabuy-coupons" not in (loc2 or "") and "/acbuy-coupons" not in (loc2 or ""):
            print("  FAIL CA extra coupons lost path", loc2)
            fail += 1
        code3, final3, _, body3 = fetch(deep, follow=True)
        if code3 == 404 or len(body3) < 8000:
            print("  FAIL deep 404", twin, code3, len(body3), final3)
            fail += 1
        else:
            print("  deep", twin, code3, "bytes", len(body3), final3)

        if twin.endswith(".nl"):
            mapped = f"https://{twin}/allchinabuy-coupons/"
            code4, final4, _, body4 = fetch(mapped, follow=True)
            if code4 == 404 or len(body4) < 8000:
                print("  FAIL mapped coupons", mapped, code4, len(body4), final4)
                fail += 1
            else:
                print("  mapped", mapped, code4, len(body4), final4)

    code, _, loc, _ = fetch(f"https://www.{NL_HOST}/", follow=False)
    if code in (301, 302, 308) and NL_HOST in (loc or ""):
        print("www apex nl", code, loc)
    else:
        print("www nl", code, loc)
        if code not in (301, 302, 308):
            fail += 1

    code, _, loc, _ = fetch(f"https://www.{CA_TARGET}/", follow=False)
    if code in (301, 302, 308) and CA_TARGET in (loc or ""):
        print("www apex ca", code, loc)
    else:
        print("www ca", code, loc)

    ca_inner = f"https://{CA_TARGET}/allchinabuy-coupons/"
    code, final, _, body = fetch(ca_inner, follow=True)
    if code == 404 or len(body) < 8000:
        print("FAIL CA dest coupons", code, len(body), final)
        fail += 1
    else:
        print("ca dest coupons", code, len(body), final)

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
