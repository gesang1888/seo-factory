#!/usr/bin/env python3
"""BBDBuy country desks: dest-unique #local, keep the 54KB .net hub.

Gates:
1. Each host #local has that dest fingerprint, no sister fingerprints.
2. Estimator country ≠ TLD; .net must say it is not a customs territory.
3. Titles have no invite code; body has no customs coaching / 58-line snapshot.
4. Same-agent country URLs stay independent (no 301).
5. Same-country twins: target #local first, then keep 301; deep paths must not 404.
6. Hub stays the original 54KB CMS homepage — never PUT a 5KB country template over it.
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
# Official Next.js freight form (login-gated). The old ThinkPHP estimate.html 404s.
EST = "https://www.bbdbuy.com/estimation"
EST_HUB = "https://www.bbdbuyeu.com/estimation"
OFFICIAL = "https://www.bbdbuy.com/"
HUB_OFFICIAL = "https://www.bbdbuyeu.com/"
DATE = "2 Oct 2026"
INVITE = "1QodRw"
COUPON = "BBD5OFF"
STORAGE = (
    "90 free warehouse days on BBDBuy warehouse copy; "
    "confirm live Help the morning you ship (do not treat a second public figure as official)"
)

DESTS = {
    "ca": {
        "host": "bbdbuy.ca",
        "lang": "en-CA",
        "loc": "en",
        "dest": "CA",
        "dest_label": "Canada",
        "ccy": "CAD",
        "title": "BBDBuy Canada — Canada Post, CAD, CBSA notes",
        "keep": [
            ("/bbdbuy-shipping/", "Canada shipping"),
            ("/is-bbdbuy-legit/", "Is it legit?"),
            ("/contact/", "Contact"),
            ("/bbdbuy-coupons/", "Coupons article"),
        ],
    },
    "it": {
        "host": "bbdbuy.it",
        "lang": "it-IT",
        "loc": "it",
        "dest": "IT",
        "dest_label": "Italia",
        "ccy": "EUR",
        "title": "BBDBuy Italia — Poste, IVA, QC già in classifica",
        "keep": [
            ("/bbdbuy-qc/", "QC"),
            ("/bbdbuy-shipping/", "Spedizione / IVA"),
            ("/bbdbuy-spreadsheet/", "Spreadsheet"),
            ("/how-to-use-bbdbuy/", "Come funziona"),
        ],
    },
    "uk": {
        "host": "bbdbuy.uk",
        "lang": "en-GB",
        "loc": "en",
        "dest": "GB",
        "dest_label": "the United Kingdom",
        "ccy": "GBP",
        "title": "BBDBuy UK desk — Royal Mail, GBP, HMRC notes",
        "keep": [
            ("/bbdbuy-shipping/", "UK shipping"),
            ("/how-to-use-bbdbuy/", "How to use"),
            ("/bbdbuy-telegram/", "Telegram"),
            ("/bbdbuy-coupons/", "Coupons article"),
        ],
    },
    "us": {
        "host": "bbdbuy.us",
        "lang": "en-US",
        "loc": "en",
        "dest": "US",
        "dest_label": "the United States",
        "ccy": "USD",
        "title": "BBDBuy United States — USPS lines, USD, shipping times",
        "keep": [
            ("/bbdbuy-shipping/", "Shipping times"),
            ("/how-to-use-bbdbuy/", "How to use"),
            ("/bbdbuy-qc/", "QC"),
            ("/bbdbuy-spreadsheet/", "Spreadsheet"),
        ],
    },
    "de": {
        "host": "bbdbuyspreadsheet.de",
        "lang": "de-DE",
        "loc": "de",
        "dest": "DE",
        "dest_label": "Deutschland",
        "ccy": "EUR",
        "title": "BBDBuy Deutschland — Zoll und MwSt auf einer DE-Adresse",
        "keep": [
            ("/bbdbuy-shipping/", "Versand DE (Zoll)"),
            ("/ist-bbdbuy-serioes/", "Seriös?"),
            ("/how-to-use-bbdbuy/", "Anleitung"),
            ("/bbdbuy-spreadsheet/", "Spreadsheet DE"),
        ],
    },
}

HUB = {
    "host": "bbdbuyeu.net",
    "lang": "en",
    "loc": "en",
    "dest": None,
    "dest_label": "a country in the estimator",
    "ccy": "USD",
    "title": "BBDBuyEU spreadsheet hub — pick a country in the estimator",
    "keep": [
        ("/bbdbuyeu-spreadsheet/", "On-site spreadsheet"),
        ("/bbdbuyeu-shipping-guide/", "Shipping guide"),
        ("/is-bbdbuyeu-legit/", "Is it legit?"),
        ("/customs-calculator/", "Customs calculator"),
    ],
}

TWINS = {
    "bbdbuyspreadsheet.ca": "bbdbuy.ca",
    "bbdbuyspreadsheet.uk": "bbdbuy.uk",
    "bbdbuyspreadsheet.us": "bbdbuy.us",
    "bbdbuyeuspreadsheet.com": "bbdbuyeu.net",
}

_DEST_TWIN_COMMON = [
    ("/bbdbuy-shipping", "/bbdbuy-shipping/"),
    ("/is-bbdbuy-legit", "/is-bbdbuy-legit/"),
    ("/how-to-use-bbdbuy", "/how-to-use-bbdbuy/"),
    ("/bbdbuy-qc", "/bbdbuy-qc/"),
    ("/bbdbuy-spreadsheet", "/bbdbuy-spreadsheet/"),
    ("/bbdbuy-coupons", "/bbdbuy-coupons/"),
]

TWIN_EXTRA = {
    "bbdbuyspreadsheet.ca": _DEST_TWIN_COMMON
    + [
        ("/bbdbuy-canada", "/"),
        ("/bbdbuy-shipping-to-canada", "/bbdbuy-shipping/"),
        ("/is-bbdbuy-safe", "/is-bbdbuy-legit/"),
        ("/contact", "/contact/"),
    ],
    "bbdbuyspreadsheet.uk": _DEST_TWIN_COMMON
    + [
        ("/bbdbuy-telegram", "/bbdbuy-telegram/"),
        ("/bbdbuy-spreadsheet-reddit", "/bbdbuy-spreadsheet-reddit/"),
        ("/is-bbdbuy-safe", "/is-bbdbuy-legit/"),
    ],
    "bbdbuyspreadsheet.us": _DEST_TWIN_COMMON
    + [
        ("/bbdbuy-link-converter", "/bbdbuy-link-converter/"),
        ("/bbdbuy-payment-methods", "/bbdbuy-payment-methods/"),
        ("/bbdbuy-tracking", "/bbdbuy-tracking/"),
        ("/bbdbuy-spreadsheet-2026", "/bbdbuy-spreadsheet-2026/"),
        ("/best-bbdbuy-spreadsheet", "/best-bbdbuy-spreadsheet/"),
    ],
    "bbdbuyeuspreadsheet.com": [
        ("/bbd-invite-code", "/bbdbuyeu-invite-code/"),
        ("/bbd-community", "/bbdbuyeu-community/"),
        ("/bbd-shoes-spreadsheet", "/bbdbuyeu-shoes-spreadsheet/"),
        ("/bbd-spreadsheet-2026", "/bbdbuyeu-spreadsheet-2026/"),
        ("/bbd-refund-guide", "/bbdbuyeu-refund-guide/"),
        ("/is-bbd-legit", "/is-bbdbuyeu-legit/"),
        ("/how-to-use-bbd", "/how-to-use-bbdbuyeu/"),
        ("/customs-calculator", "/customs-calculator/"),
        ("/bbd-shipping-guide", "/bbdbuyeu-shipping-guide/"),
        ("/bbdbuyeu-shipping-guide", "/bbdbuyeu-shipping-guide/"),
        ("/bbdbuyeu-spreadsheet", "/bbdbuyeu-spreadsheet/"),
        ("/is-bbdbuyeu-legit", "/is-bbdbuyeu-legit/"),
    ],
}

DEST_LOCAL_CSS = (
    ".sg-sec#local{margin:1.25rem 0 0}"
    ".sg-sec#local h2{margin-top:0}"
    ".ssub{color:var(--muted,#57534e);font-size:.95rem;margin:0 0 12px}"
)
HUB_LOCAL_CSS = """
#local.sg-sec{max-width:860px;margin:0 auto;padding:8px 24px 40px;text-align:left}
#local.sg-sec h2{font-size:22px;letter-spacing:-.4px;margin:0 0 8px}
#local.sg-sec .ssub{margin-bottom:14px}
#local.sg-sec .local-steps li{border-color:var(--g5,#e5e7eb)}
"""

EST_NOTE = {
    "ca": "Estimator country is CA, not this TLD, not a US ZIP.",
    "it": "Il paese dell’estimator è IT, non questo TLD, non EU.",
    "uk": "Estimator country is GB, not this TLD, not EU.",
    "us": "Estimator country is US, not this TLD, not EU.",
    "de": "Schätzer-Land ist DE, nicht diese TLD, nicht AT, nicht „EU“.",
    "net": "This hostname is not a customs territory. Open the estimator with a real country, not .net.",
}

STORE_NOTE = {
    "de": "Lager: 90 freie Tage laut BBDBuy-Warehouse-Text; am Versandmorgen in Help prüfen. Keine zweite Zahl als offiziell ausgeben.",
    "it": "Magazzino: 90 giorni gratis sulla copia warehouse BBDBuy; conferma Help il giorno della spedizione. Non trattare una seconda cifra come ufficiale.",
    "en": "Warehouse: 90 free days on BBDBuy warehouse copy; confirm live Help the morning you ship. Do not treat a second public figure as official.",
}

TRAIL = {
    "de": ("Live-Preis steht in", "dieses HTML ist keine Kasse."),
    "it": ("I soldi veri stanno in", "questo HTML non è cassa."),
    "en": ("Live money is in", "this HTML is not checkout."),
}


def _facts(spec: dict) -> dict:
    dest = spec.get("dest")
    official = HUB_OFFICIAL if dest is None else OFFICIAL
    est = EST_HUB if dest is None else EST
    return {
        "agent": "BBDBuyEU" if dest is None else "BBDBuy",
        "host": spec["host"],
        "lang": spec["lang"],
        "loc": spec["loc"],
        "dest": dest,
        "dest_label": spec.get("dest_label") or "a country in the estimator",
        "ccy": spec["ccy"],
        "storage": STORAGE,
        "estimator": est,
        "official": official,
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
        s = re.sub(r"\s*[—\-–:,]*\s*Invite\s+1QodRw", "", s, flags=re.I)
        s = s.replace(INVITE, "").replace(COUPON, "")
        s = re.sub(r"\s{2,}", " ", s).strip(" —–-,")
        return s

    def title_sub(m):
        inner = m.group(1)
        if new_title:
            return f"<title>{escape(new_title)}</title>"
        return f"<title>{scrub(inner)}</title>"

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
        html = html.replace("</style>", SKIP_CSS + DEST_LOCAL_CSS + "\n</style>", 1)
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
        err.append("invite/coupon in title")
    if re.search(r"58 l[ií]neas para Espa|23[,.]81\s*USD|how to under-?declar", html, flags=re.I):
        err.append("spain snapshot / coaching")
    if err:
        raise RuntimeError(f"{key}: {'; '.join(err)}")
    return html


def patch_hub(html: str) -> str:
    facts = _facts(HUB)
    block = _local_block("net", HUB)
    html = _strip_invite_title(html, HUB["title"])
    html = html.replace(
        "<h1>The Complete <em>BBDBuyEU Spreadsheet</em> — Invite 1QodRw</h1>",
        "<h1>The Complete <em>BBDBuyEU Spreadsheet</em> hub</h1>",
        1,
    )
    if 'class="skip"' not in html:
        html = html.replace("<body>", "<body>\n" + skip_link("Skip to content").rstrip(), 1)
    if 'id="main"' not in html:
        html = html.replace(
            '<section class="hero fade-in">',
            '<section class="hero fade-in" id="main">',
            1,
        )
    if 'href="#local"' not in html:
        html = html.replace(
            '<li><a href="/bbdbuyeu-spreadsheet/">Spreadsheet</a></li>',
            '<li><a href="/bbdbuyeu-spreadsheet/">Spreadsheet</a></li>'
            '<li><a href="#local">Pick a country</a></li>',
            1,
        )
    if "#local{scroll-margin-top" not in html:
        html = html.replace("</style>", SKIP_CSS + HUB_LOCAL_CSS + "\n</style>", 1)
    if 'id="local"' in html:
        html = re.sub(
            r'<section class="sg-sec" id="local".*?</section>',
            block,
            html,
            count=1,
            flags=re.S,
        )
    else:
        marker = "</section>\n<section class=\"phwrap fade-in\">"
        if marker not in html:
            raise RuntimeError("hub hero marker missing")
        html = html.replace(marker, "</section>\n" + block + "\n<section class=\"phwrap fade-in\">", 1)
    err: list[str] = []
    _check_local_section(html, facts, err)
    title_m = re.search(r"<title>(.*?)</title>", html, flags=re.S)
    title = title_m.group(1) if title_m else ""
    if INVITE in title or COUPON in title:
        err.append("invite in hub title")
    if "not a customs territory" not in html:
        err.append("hub missing fingerprint")
    if len(html) < 40000:
        err.append(f"hub collapsed to {len(html)} bytes")
    if 'class="hero' not in html or "hot-products-grid" not in html:
        err.append("hub chrome missing")
    if err:
        raise RuntimeError(f"hub: {'; '.join(err)}")
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
        print("dest", key, spec["host"], "bytes", len(html))
    hub_src = OUT / "bbdbuyeu.net" / "live-base" / "index.html"
    hub_html = patch_hub(hub_src.read_text(encoding="utf-8"))
    hub_dest = OUT / "bbdbuyeu.net" / "overlay" / "index.html"
    hub_dest.parent.mkdir(parents=True, exist_ok=True)
    hub_dest.write_text(hub_html, encoding="utf-8")
    inner = re.search(r'<section class="sg-sec" id="local".*?</section>', hub_html, flags=re.S)
    blobs["net"] = inner.group(0) if inner else ""
    print("hub bbdbuyeu.net bytes", len(hub_html), "was", hub_src.stat().st_size)

    fps = {
        k: dest_local_pack(DESTS[k]["dest"] if k in DESTS else None)["fingerprint"]
        for k in blobs
    }
    for key, inner in blobs.items():
        fp = fps[key]
        if fp not in inner:
            raise SystemExit(f"{key} missing fingerprint {fp!r}")
        for other, ofp in fps.items():
            if other == key:
                continue
            if ofp in inner:
                raise SystemExit(f"{key} leaked {other} {ofp!r}")
        if INVITE in inner:
            raise SystemExit(f"{key} invite in #local")
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
    bak = f"/www/backup/bbdbuy-desks-{stamp}"
    _run(client, f"mkdir -p '{bak}'")
    sftp = client.open_sftp()
    puts = [(spec["host"], OUT / spec["host"] / "overlay" / "index.html") for spec in DESTS.values()]
    puts.append(("bbdbuyeu.net", OUT / "bbdbuyeu.net" / "overlay" / "index.html"))
    for host, local in puts:
        remote = f"/www/wwwroot/{host}/index.html"
        if host == "bbdbuyeu.net" and local.stat().st_size < 40000:
            raise SystemExit("refusing to PUT thin template over .net hub")
        _run(client, f"cp -a '{remote}' '{bak}/{host}.index.html'")
        sftp.put(str(local), remote)
        print("PUT", remote, "bytes", local.stat().st_size)
    sftp.close()
    patch_twins(client)
    print("backup", bak)
    client.close()


def patch_twins(client) -> None:
    changed = 0
    for twin, target in TWINS.items():
        path = f"/www/server/panel/vhost/nginx/{twin}.conf"
        raw = _run(client, f"cat '{path}'")
        if not raw:
            print("skip missing", twin)
            continue
        extra = []
        for src, dest in TWIN_EXTRA.get(twin, []):
            if f"location = {src} " in raw or f"location = {src}{{" in raw:
                continue
            extra.append(f"    location = {src} {{ return 301 https://{target}{dest}; }}")
            extra.append(f"    location = {src}/ {{ return 301 https://{target}{dest}; }}")
        if extra:
            marker = "    location / { return 301"
            if marker not in raw:
                print("skip", twin, "no catch-all")
                continue
            raw = raw.replace(marker, "\n".join(extra) + "\n" + marker, 1)
            _run(client, f"cp -a '{path}' '/www/backup/bbdbuy-twin-{twin}.conf'")
            sftp = client.open_sftp()
            with sftp.open(path, "w") as fh:
                fh.write(raw)
            sftp.close()
            changed += 1
            print("PATCH nginx", twin, "extra", len(extra) // 2)
        else:
            print("ok nginx", twin)
    if changed:
        print(_run(client, "nginx -t && nginx -s reload"))


def live_check() -> None:
    import urllib.request

    pairs = [
        ("ca", "https://bbdbuy.ca/", "form A1A 1A1", ("Packstation", "Poste Italiane", "1010 Wien")),
        ("it", "https://bbdbuy.it/", "Poste Italiane", ("Packstation", "form A1A 1A1", "1010 Wien")),
        ("uk", "https://bbdbuy.uk/", "Northern Ireland is often another", ("Packstation", "form A1A 1A1", "Poste Italiane")),
        ("us", "https://bbdbuy.us/", "does not invent a de-minimis dollar", ("Packstation", "form A1A 1A1", "1010 Wien")),
        ("de", "https://bbdbuyspreadsheet.de/", "Packstation", ("1010 Wien", "form A1A 1A1", "Poste Italiane")),
        ("net", "https://bbdbuyeu.net/", "not a customs territory", ("1010 Wien", "Packstation", "form A1A 1A1")),
    ]

    class NR(urllib.request.HTTPRedirectHandler):
        def redirect_request(self, req, fp, code, msg, headers, newurl):
            return None

    def fetch(url, follow=True):
        req = urllib.request.Request(url, headers={"User-Agent": "bbd-desk-check/1.0"})
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
        print(f"{key:3} {code} bytes={len(body)} local={bool(inner)} fp={fp in html}")
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
        if key == "net" and len(body) < 40000:
            print("  FAIL hub collapsed", len(body))
            fail += 1
        if key == "net" and ("hot-products-grid" not in html or 'class="hero' not in html):
            print("  FAIL hub chrome gone")
            fail += 1
        est_need = EST_HUB if key == "net" else EST
        if est_need not in inner:
            print("  FAIL estimator url missing")
            fail += 1
        notes = {
            "ca": "Estimator country is CA",
            "it": "estimator è IT",
            "uk": "Estimator country is GB",
            "us": "Estimator country is US",
            "de": "Schätzer-Land ist DE",
            "net": "not a customs territory",
        }
        if notes[key] not in inner:
            print("  FAIL estimator country note")
            fail += 1

    inners = [
        "https://bbdbuy.ca/is-bbdbuy-legit/",
        "https://bbdbuy.ca/bbdbuy-shipping/",
        "https://bbdbuy.it/bbdbuy-qc/",
        "https://bbdbuy.uk/bbdbuy-shipping/",
        "https://bbdbuy.us/bbdbuy-shipping/",
        "https://bbdbuyspreadsheet.de/bbdbuy-shipping/",
        "https://bbdbuyspreadsheet.de/ist-bbdbuy-serioes/",
        "https://bbdbuyeu.net/bbdbuyeu-spreadsheet/",
        "https://bbdbuyeu.net/is-bbdbuyeu-legit/",
    ]
    for url in inners:
        code, final, _, body = fetch(url, follow=True)
        if code == 404 or len(body) < 8000:
            print("FAIL inner", url, code, len(body))
            fail += 1
        else:
            print("inner", code, len(body), final)

    for a in (
        "https://bbdbuy.ca/",
        "https://bbdbuy.it/",
        "https://bbdbuy.uk/",
        "https://bbdbuy.us/",
        "https://bbdbuyspreadsheet.de/",
        "https://bbdbuyeu.net/",
    ):
        code, _, loc, _ = fetch(a, follow=False)
        if code in (301, 302, 303, 307, 308) and loc:
            print("FAIL 301", a, "->", loc)
            fail += 1
        else:
            print("indep", a, code)

    for twin, target in TWINS.items():
        code, _, loc, _ = fetch(f"https://{twin}/", follow=False)
        print("twin", twin, code, loc)
        if code not in (301, 302, 308) or target not in (loc or ""):
            print("  FAIL twin 301")
            fail += 1
        deep = f"https://{twin}/bbdbuy-shipping" if twin != "bbdbuyeuspreadsheet.com" else f"https://{twin}/bbd-shipping-guide"
        code2, _, _, body2 = fetch(deep, follow=True)
        if code2 == 404:
            print("  FAIL deep 404", twin)
            fail += 1
        else:
            print("  deep", twin, code2, "bytes", len(body2))

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
