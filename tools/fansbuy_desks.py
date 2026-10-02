#!/usr/bin/env python3
"""FansBuy country desks: dest-unique #local, keep ranked CMS inners.

Gates:
1. Each host #local has that dest fingerprint, no sister fingerprints.
2. Estimator country ≠ TLD; .eu / .net must say they are not a customs territory.
3. Titles have no invite code; body has no customs coaching / 58-line snapshot.
4. Same-agent country URLs stay independent (no 301). UK ≠ DE ≠ NL; none 301 to USFans.
5. Same-country twins: target #local first, then 301; deep paths must not 404.
6. Georgia homes get #local; ranked 24–60KB inners stay. Do not PUT over unique CMS.
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
EST = "https://fansbuy.com/estimates"
OFFICIAL = "https://fansbuy.com/"
HELP = "https://fansbuy.com/help-283.html"
DATE = "2 Oct 2026"
INVITE = "Fans-pys5Zt48"
COUPON = "FANS26"
STORAGE = (
    "Official Help: 90 free warehouse days "
    f"({HELP}); confirm that article the morning you ship"
)

DESTS = {
    "uk": {
        "host": "fansbuy.co.uk",
        "lang": "en-GB",
        "loc": "en",
        "dest": "GB",
        "dest_label": "the United Kingdom",
        "ccy": "GBP",
        "title": "FansBuy UK — Royal Mail lines, GBP, HMRC notes",
        "h1": "FansBuy for a UK delivery address (GBP, Royal Mail last-mile)",
        "keep": [
            ("/fansbuy-shipping-guide/", "UK shipping"),
            ("/fansbuy-coupons/", "Coupons article"),
            ("/fansbuy-spreadsheet/", "Spreadsheet"),
            ("/fansbuy-refund-guide/", "Refunds"),
        ],
    },
    "de": {
        "host": "fansbuyspreadsheet.de",
        "lang": "de-DE",
        "loc": "de",
        "dest": "DE",
        "dest_label": "Deutschland",
        "ccy": "EUR",
        "title": "FansBuy Deutschland — Zoll, DHL und Packstation",
        "h1": "FansBuy für eine deutsche Adresse (EUR, Packstation möglich)",
        "keep": [
            ("/fansbuy-coupons/", "Coupons DE"),
            ("/fansbuy-shipping-guide/", "Versand DE"),
            ("/fansbuy-spreadsheet/", "Spreadsheet DE"),
            ("/is-fansbuy-legit/", "Seriös?"),
        ],
    },
    "nl": {
        "host": "fansbuy.nl",
        "lang": "nl-NL",
        "loc": "nl",
        "dest": "NL",
        "dest_label": "Nederland",
        "ccy": "EUR",
        "title": "FansBuy Nederland — Nederlandse postcode, geen Duitse automaat",
        "h1": "FansBuy voor een Nederlands adres (EUR, Nederlandse postcode)",
        "keep": [
            ("/fansbuy-shipping-guide/", "Verzending"),
            ("/fansbuy-spreadsheet/", "Spreadsheet"),
            ("/is-fansbuy-legit/", "Legit?"),
            ("/fansbuy-coupons/", "Coupons"),
        ],
    },
}

HUBS = {
    "eu": {
        "host": "fansbuy.eu",
        "lang": "en",
        "loc": "en",
        "dest": None,
        "dest_label": "a country in the estimator",
        "ccy": "EUR",
        "title": "FansBuy.eu — not a customs territory; pick a member-state",
        "h1": "FansBuy.eu is not a customs territory — pick a real country",
        "keep": [
            ("/fansbuy-shipping-guide/", "Shipping / fiscal notes"),
            ("/fansbuy-spreadsheet/", "Spreadsheet"),
            ("/how-to-use-fansbuy/", "How to use"),
            ("/is-fansbuy-legit/", "Legit?"),
        ],
    },
    "net": {
        "host": "fansbuysheets.net",
        "lang": "en",
        "loc": "en",
        "dest": None,
        "dest_label": "a country in the estimator",
        "ccy": "USD",
        "title": "FansBuy sheets hub — not a customs territory",
        "h1": "This .net hostname is not a customs territory",
        "keep": [
            ("/fansbuy-coupons/", "Coupons (ranked)"),
            ("/fansbuy-shipping-guide/", "Shipping"),
            ("/fansbuy-invite-code/", "Invite article"),
            ("/fansbuy-spreadsheet/", "Spreadsheet"),
        ],
    },
}

# Already 301; after dest #local, keep catch-all $request_uri so deep paths land.
CONVERT_TWINS = {
    "fansbuyspreadsheet.uk": "fansbuy.co.uk",
    "fansbuyspreadsheet.eu": "fansbuy.eu",
    "fansspreadsheet.net": "fansbuysheets.net",
    "fansspreadsheets.net": "fansbuysheets.net",
}

PATH_MAP = {
    "fansbuyspreadsheet.uk": [
        ("/fansbuy-spreadsheet-2026/", "/fansbuy-spreadsheet/"),
        ("/blog/posts/is-fansbuy-legit/", "/is-fansbuy-legit/"),
    ],
    "fansbuyspreadsheet.eu": [
        ("/fansbuy-spreadsheet-2026/", "/fansbuy-spreadsheet/"),
        ("/blog/posts/is-fansbuy-legit/", "/is-fansbuy-legit/"),
    ],
    "fansspreadsheet.net": [
        ("/blog/posts/is-fansbuy-legit/", "/is-fansbuy-legit/"),
        ("/blog/posts/best-acbuy-spreadsheet/", "/fansbuy-spreadsheet/"),
    ],
}

EST_NOTE = {
    "uk": "Estimator country is GB, not this TLD, not EU, not the .eu hub.",
    "de": "Schätzer-Land ist DE, nicht diese TLD, nicht AT, nicht „EU“.",
    "nl": "Estimator-land is NL, niet deze TLD, niet EU, niet BE.",
    "eu": "This .eu hub is not a customs territory. Pick DE, NL or GB in the estimator — not this hostname, not “EU” as one country.",
    "net": "This .net hub is not a customs territory. Pick the real ship-to country in the estimator, not this hostname.",
}

STORE_NOTE = {
    "de": "Lager: offizielles Help 90 Tage gratis; am Versandmorgen denselben Artikel prüfen.",
    "nl": "Magazijn: officiële Help 90 dagen gratis; bevestig het artikel op de verzenddag.",
    "en": "Warehouse: official Help 90 free days; confirm that article the morning you ship.",
}

TRAIL = {
    "de": ("Live-Preis steht in", "dieses HTML ist keine Kasse."),
    "nl": ("Live-geld staat in", "deze HTML is geen kassa."),
    "en": ("Live money is in", "this HTML is not checkout."),
}

DEST_LOCAL_CSS = (
    ".sg-sec#local{margin:1.25rem 0 0}"
    ".sg-sec#local h2{margin-top:0}"
    ".ssub{color:var(--muted,#57534e);font-size:.95rem;margin:0 0 12px}"
)


def _facts(spec: dict) -> dict:
    return {
        "agent": "FansBuy",
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
        "codes_off_title": [INVITE, COUPON],
        "strict_html_codes": False,
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


def _strip_invite_title(html: str, new_title: str | None = None) -> str:
    def scrub(s: str) -> str:
        s = re.sub(r"\s*[—\-–:,]*\s*(invite|ref|code|coupon)?\s*Fans-pys5Zt48", "", s, flags=re.I)
        s = s.replace(INVITE, "").replace(COUPON, "")
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
    html = _strip_invite_title(html, spec.get("title"))
    if spec.get("h1"):
        html = re.sub(r"<h1>.*?</h1>", f"<h1>{escape(spec['h1'])}</h1>", html, count=1, flags=re.S)
    html = re.sub(r"impressions on a template", "impressions on this dest desk", html, flags=re.I)
    if 'class="skip"' not in html:
        html = html.replace("<body>", "<body>\n" + skip_link(skip_label(loc)).rstrip(), 1)
    if 'id="main"' not in html:
        html = html.replace("<main>", '<main id="main">', 1)
    if 'href="#local"' not in html and "</nav>" in html:
        html = html.replace(
            "</nav>",
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
    if INVITE in title or COUPON in title:
        err.append("invite in title")
    if re.search(r"58 l[ií]neas para Espa|23[,.]81\s*USD|how to under-?declar", html, flags=re.I):
        err.append("spain snapshot / coaching")
    if err:
        raise RuntimeError(f"{key}: {'; '.join(err)}")
    return html


def generate() -> None:
    assert_dest_packs_unique()
    blobs = {}
    specs = {**DESTS, **HUBS}
    for key, spec in specs.items():
        src = OUT / spec["host"] / "live-base" / "index.html"
        html = patch_static(src.read_text(encoding="utf-8"), key, spec)
        dest = OUT / spec["host"] / "overlay" / "index.html"
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(html, encoding="utf-8")
        inner = re.search(r'<section class="sg-sec" id="local".*?</section>', html, flags=re.S)
        blobs[key] = inner.group(0) if inner else ""
        kind = "hub" if spec.get("dest") is None else "dest"
        print(kind, key, spec["host"], "bytes", len(html))
    fps = {k: dest_local_pack(specs[k].get("dest"))["fingerprint"] for k in blobs}
    for key, inner in blobs.items():
        fp = fps[key]
        if fp not in inner:
            raise SystemExit(f"{key} missing fingerprint {fp!r}")
        for other, ofp in fps.items():
            if other == key or ofp == fp:
                continue
            if ofp in inner:
                raise SystemExit(f"{key} leaked {other} {ofp!r}")
        if INVITE in inner:
            raise SystemExit(f"{key} invite in #local")
        if EST.split("://", 1)[-1].rstrip("/") not in inner and EST not in inner:
            raise SystemExit(f"{key} missing estimator")
        if specs[key].get("dest") is None and "not a customs territory" not in inner:
            raise SystemExit(f"{key} hub missing customs-territory line")
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


def _rewrite_gsc(graw: str, twin: str, target: str) -> str:
    old_host = f"https://{twin}/"
    new_host = f"https://{target}/"
    graw = graw.replace(old_host, new_host)
    existing = set(re.findall(r"location = (/[^\s{]+)", graw))
    extras = []
    for src, dest in PATH_MAP.get(twin, []):
        graw = graw.replace(f"{new_host}{src.lstrip('/')}", f"{new_host}{dest.lstrip('/')}")
        graw = graw.replace(f"{new_host}{src}", f"{new_host}{dest}")
        slash = src if src.endswith("/") else src + "/"
        if slash not in existing:
            extras.append(f"location = {slash} {{ return 301 {new_host}{dest.lstrip('/')}; }}")
    if extras:
        graw = graw.rstrip() + "\n" + "\n".join(extras) + "\n"
    return graw


def _ensure_catch_all(raw: str, target: str) -> str:
    needle_try = "    location / {\n        try_files $uri $uri/ $uri/index.html =404;\n    }"
    if needle_try in raw:
        return raw.replace(needle_try, f"    location / {{ return 301 https://{target}$request_uri; }}", 1)
    home_only = f"location / {{ return 301 https://{target}/; }}"
    keep_uri = f"location / {{ return 301 https://{target}$request_uri; }}"
    if home_only in raw:
        return raw.replace(home_only, keep_uri, 1)
    home_only2 = f"return 301 https://{target}/;"
    # only rewrite a location / catch-all, not exact maps
    raw2 = re.sub(
        rf"(location\s+/\s*\{{\s*return\s+301\s+https://{re.escape(target)})/;(\s*\}})",
        rf"\1$request_uri;\2",
        raw,
        count=1,
    )
    return raw2


def patch_twins(client) -> None:
    changed = 0
    for twin, target in CONVERT_TWINS.items():
        path = f"/www/server/panel/vhost/nginx/{twin}.conf"
        raw = _run(client, f"cat '{path}'")
        if not raw:
            print("skip missing", twin)
            continue
        new = _ensure_catch_all(raw, target)
        if new != raw:
            _run(client, f"cp -a '{path}' '/www/backup/fansbuy-twin-{twin}.conf'")
            sftp = client.open_sftp()
            with sftp.open(path, "w") as fh:
                fh.write(new)
            sftp.close()
            changed += 1
            print("PATCH nginx", twin, "catch-all $request_uri →", target)
        else:
            print("twin already 301", twin, "→", target)
        gsc = f"/www/server/panel/vhost/nginx/extension/{twin}/gsc-redirects.conf"
        graw = _run(client, f"cat '{gsc}'")
        if graw and f"https://{twin}/" in graw:
            _run(client, f"cp -a '{gsc}' '/www/backup/fansbuy-gsc-{twin}.conf'")
            graw = _rewrite_gsc(graw, twin, target)
            sftp = client.open_sftp()
            with sftp.open(gsc, "w") as fh:
                fh.write(graw)
            sftp.close()
            changed += 1
            print("PATCH nginx GSC redirects", twin, "→", target)
        elif graw:
            print("GSC already dest-host or unused", twin)
    if changed:
        print(_run(client, "nginx -t && nginx -s reload"))


def put() -> None:
    generate()
    client = _connect()
    stamp = time.strftime("%Y%m%d-%H%M%S")
    bak = f"/www/backup/fansbuy-desks-{stamp}"
    _run(client, f"mkdir -p '{bak}'")
    sftp = client.open_sftp()
    specs = list(DESTS.values()) + list(HUBS.values())
    for spec in specs:
        local = OUT / spec["host"] / "overlay" / "index.html"
        remote = f"/www/wwwroot/{spec['host']}/index.html"
        raw = local.read_text(encoding="utf-8")
        if 'id="local"' not in raw:
            raise SystemExit(f"refusing to PUT {spec['host']} without #local")
        _run(client, f"cp -a '{remote}' '{bak}/{spec['host']}.index.html'")
        sftp.put(str(local), remote)
        print("PUT", remote, "bytes", local.stat().st_size)
    sftp.close()
    patch_twins(client)
    print("backup", bak)
    client.close()


def live_check() -> None:
    import urllib.request

    pairs = [
        ("uk", "https://fansbuy.co.uk/", "Northern Ireland is often another", ("Packstation", "form A1A 1A1", "00-001 Warszawa")),
        ("de", "https://fansbuyspreadsheet.de/", "Packstation", ("1010 Wien", "form A1A 1A1", "00-001 Warszawa")),
        ("nl", "https://fansbuy.nl/", "Nederlandse postcode", ("Packstation", "form A1A 1A1", "00-001 Warszawa")),
        ("eu", "https://fansbuy.eu/", "not a customs territory", ("1010 Wien", "Packstation", "00-001 Warszawa")),
        ("net", "https://fansbuysheets.net/", "not a customs territory", ("1010 Wien", "Packstation", "00-001 Warszawa")),
    ]

    class NR(urllib.request.HTTPRedirectHandler):
        def redirect_request(self, req, fp, code, msg, headers, newurl):
            return None

    def fetch(url, follow=True):
        req = urllib.request.Request(url, headers={"User-Agent": "fb-desk-check/1.0"})
        opener = urllib.request.build_opener() if follow else urllib.request.build_opener(NR)
        try:
            with opener.open(req, timeout=25) as resp:
                return resp.status, resp.geturl(), resp.headers.get("Location") or "", resp.read()
        except urllib.error.HTTPError as e:
            return e.code, url, e.headers.get("Location") or "", e.read() if e.fp else b""

    fail = 0
    for key, url, fp, aliens in pairs:
        code, _, loc, body = fetch(url, follow=True)
        html = body.decode("utf-8", "replace")
        title_m = re.search(r"<title>(.*?)</title>", html, flags=re.S)
        title = title_m.group(1) if title_m else ""
        inner_m = re.search(r'<section class="sg-sec" id="local".*?</section>', html, flags=re.S)
        inner = inner_m.group(0) if inner_m else ""
        print(f"{key:4} {code} bytes={len(body)} local={bool(inner)} fp={fp in html}")
        if code != 200 or not inner or fp not in inner:
            print("  FAIL status/local/fp")
            fail += 1
            continue
        for alien in aliens:
            if alien in inner:
                print("  FAIL sister", alien)
                fail += 1
        if INVITE in title or COUPON in title:
            print("  FAIL invite in title")
            fail += 1
        if re.search(r"58 l[ií]neas para Espa|23[,.]81\s*USD|how to under-?declar", html, flags=re.I):
            print("  FAIL snapshot/coaching")
            fail += 1
        if EST not in inner:
            print("  FAIL estimator url missing")
            fail += 1

    inners = [
        "https://fansbuy.co.uk/fansbuy-shipping-guide/",
        "https://fansbuy.co.uk/fansbuy-coupons/",
        "https://fansbuyspreadsheet.de/fansbuy-spreadsheet/",
        "https://fansbuy.nl/fansbuy-shipping-guide/",
        "https://fansbuy.eu/fansbuy-shipping-guide/",
        "https://fansbuysheets.net/fansbuy-coupons/",
    ]
    for url in inners:
        code, final, _, body = fetch(url, follow=True)
        if code == 404 or len(body) < 8000:
            print("FAIL inner", url, code, len(body))
            fail += 1
        else:
            print("inner", code, len(body), final)

    dest_urls = [f"https://{spec['host']}/" for spec in list(DESTS.values()) + list(HUBS.values())]
    dest_urls.append("https://usfansspreadsheet.co.uk/")
    dest_urls.append("https://usfansspreadsheet.nl/")
    for a in dest_urls:
        code, _, loc, _ = fetch(a, follow=False)
        if code in (301, 302, 303, 307, 308) and loc:
            print("FAIL 301", a, "->", loc)
            fail += 1
        else:
            print("indep", a, code)

    twins = [
        ("https://fansbuyspreadsheet.uk/", "https://fansbuy.co.uk/"),
        ("https://fansbuyspreadsheet.uk/fansbuy-shipping-guide/", "https://fansbuy.co.uk/fansbuy-shipping-guide/"),
        ("https://fansbuyspreadsheet.eu/", "https://fansbuy.eu/"),
        ("https://fansbuyspreadsheet.eu/fansbuy-coupons/", "https://fansbuy.eu/fansbuy-coupons/"),
        ("https://fansspreadsheet.net/", "https://fansbuysheets.net/"),
        ("https://fansspreadsheets.net/fansbuy-coupons/", "https://fansbuysheets.net/fansbuy-coupons/"),
    ]
    for src, dest in twins:
        code, final, loc, body = fetch(src, follow=True)
        dest_host = dest.split("/")[2]
        if dest_host not in final or code == 404 or (src.rstrip("/").count("/") > 2 and len(body) < 8000):
            print("FAIL twin", src, code, final, len(body))
            fail += 1
        else:
            print("twin", src, "→", final, code, len(body))

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
