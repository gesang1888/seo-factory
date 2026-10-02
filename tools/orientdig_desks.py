#!/usr/bin/env python3
"""OrientDig country desks: dest-unique #local, keep ranked CMS inners.

Gates:
1. Each host #local has that dest fingerprint, no sister fingerprints.
2. Estimator country ≠ TLD (no .eu/.net/now.com in this cluster).
3. Titles have no invite/ref code; body has no customs coaching / 58-line snapshot.
4. Same-agent country URLs stay independent (no 301).
5. Same-country twins: target #local first, then 301; deep paths must not 404.
6. Do not PUT a 5KB template over unique CMS — surgical insert on Georgia homes.
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
EST = "https://orientdig.com/estimation/"
OFFICIAL = "https://orientdig.com/"
HELP_STORAGE = (
    "https://orientdig.com/help-center/"
    "the-duration-for-which-goods-can-be-stored-in-the-orientdig-warehouse-is-90-days/"
)
DATE = "2 Oct 2026"
INVITE = "100246065"
STORAGE = (
    "Official Help: 90 days from stored in warehouse "
    f"({HELP_STORAGE}); confirm that article the morning you ship"
)

DESTS = {
    "at": {
        "host": "orientdig.at",
        "lang": "de-AT",
        "loc": "de",
        "dest": "AT",
        "dest_label": "Österreich",
        "ccy": "EUR",
        "title": "OrientDig Österreich — Österreichische Post, nicht DHL DE",
        "h1": "OrientDig für eine österreichische Adresse (EUR, Post AT)",
        "keep": [
            ("/orientdig-shipping/", "Versand AT"),
            ("/orientdig-coupons/", "Gutscheine"),
            ("/how-to-use-orientdig/", "Anleitung"),
            ("/is-orientdig-legit/", "Seriös?"),
        ],
    },
    "es": {
        "host": "orientdig.es",
        "lang": "es-ES",
        "loc": "es",
        "dest": "ES",
        "dest_label": "España",
        "ccy": "EUR",
        "title": "OrientDig España — Correos, envío CMS y spreadsheet",
        "h1": "OrientDig para una dirección en España (EUR, Correos)",
        "keep": [
            ("/orientdig-shipping-coupons/", "Cupones de envío"),
            ("/como-comprar-en-orientdig/", "Cómo comprar"),
            ("/orientdig-spreadsheet/", "Spreadsheet"),
            ("/is-orientdig-legit/", "¿Legit?"),
        ],
    },
    "fr": {
        "host": "orientdig.fr",
        "lang": "fr-FR",
        "loc": "fr",
        "dest": "FR",
        "dest_label": "la France",
        "ccy": "EUR",
        "title": "OrientDig France — Colissimo, avis et livraison déjà classés",
        "h1": "OrientDig pour une adresse en France (EUR, pas un code postal belge)",
        "keep": [
            ("/avis-orientdig/", "Avis"),
            ("/orientdig-shipping/", "Livraison"),
            ("/orientdig-spreadsheet/", "Spreadsheet"),
            ("/how-to-use-orientdig/", "Tutoriel"),
        ],
    },
    "us": {
        "host": "orientdig.us",
        "lang": "en-US",
        "loc": "en",
        "dest": "US",
        "dest_label": "the United States",
        "ccy": "USD",
        "title": "OrientDig United States — USPS lines, USD, not a hub for other dests",
        "h1": "OrientDig for a US delivery address (USD, USPS last-mile)",
        "keep": [
            ("/orientdig-spreadsheet/", "Spreadsheet"),
            ("/orientdig-shipping/", "Shipping US"),
            ("/orientdig-coupons/", "Coupons article"),
            ("/is-orientdig-legit/", "Is it legit?"),
        ],
    },
    "de": {
        "host": "orientdigspreadsheet.de",
        "lang": "de-DE",
        "loc": "de",
        "dest": "DE",
        "dest_label": "Deutschland",
        "ccy": "EUR",
        "title": "OrientDig Deutschland — Zoll, DHL und Packstation",
        "h1": "OrientDig für eine deutsche Adresse (EUR, Packstation möglich)",
        "keep": [
            ("/orientdig-shipping/", "Versand DE"),
            ("/how-to-use-orientdig/", "Anleitung"),
            ("/is-orientdig-legit/", "Seriös?"),
            ("/orientdig-coupons/", "Gutscheine"),
        ],
    },
    "it": {
        "host": "orientdigspreadsheet.it",
        "lang": "it-IT",
        "loc": "it",
        "dest": "IT",
        "dest_label": "Italia",
        "ccy": "EUR",
        "title": "OrientDig Italia — Poste, tutorial già in classifica",
        "h1": "OrientDig per un indirizzo in Italia (EUR, Poste Italiane)",
        "keep": [
            ("/how-to-use-orientdig/", "Come funziona"),
            ("/orientdig-spreadsheets/", "Spreadsheet"),
            ("/is-orientdig-legit/", "È affidabile?"),
            ("/orientdig-shipping/", "Spedizione"),
        ],
    },
    "nl": {
        "host": "orientdigspreadsheet.nl",
        "lang": "nl-NL",
        "loc": "nl",
        "dest": "NL",
        "dest_label": "Nederland",
        "ccy": "EUR",
        "title": "OrientDig Nederland — Nederlandse postcode, geen Duitse automaat",
        "h1": "OrientDig voor een Nederlands adres (EUR, Nederlandse postcode)",
        "keep": [
            ("/orientdig-coupons/", "Coupons"),
            ("/orientdig-spreadsheets/", "Spreadsheet"),
            ("/how-to-use-orientdig/", "Handleiding"),
            ("/orientdig-shipping/", "Verzending"),
        ],
    },
    "uk": {
        "host": "orientdigspreadsheet.uk",
        "lang": "en-GB",
        "loc": "en",
        "dest": "GB",
        "dest_label": "the United Kingdom",
        "ccy": "GBP",
        "title": "OrientDig UK — Royal Mail, GBP, HMRC notes",
        "h1": "OrientDig for a UK delivery address (GBP, Royal Mail last-mile)",
        "keep": [
            ("/orientdig-spreadsheets/", "Spreadsheet"),
            ("/orientdig-shipping/", "UK shipping"),
            ("/how-to-use-orientdig/", "How to use"),
            ("/is-orientdig-legit/", "Is it legit?"),
        ],
    },
}

TWINS = {
    "orientdigspreadsheet.fr": "orientdig.fr",
    "orientdigspreadsheets.fr": "orientdig.fr",
    "orientdigspreadsheets.de": "orientdigspreadsheet.de",
    "orientdigspreadsheets.nl": "orientdigspreadsheet.nl",
    "orientdigspreadsheets.uk": "orientdigspreadsheet.uk",
    "orientdigspreadsheet.us": "orientdig.us",
}

CONVERT_TWINS = {"orientdigspreadsheet.us": "orientdig.us"}

TWIN_EXTRA = {
    "orientdigspreadsheet.fr": [
        ("/livraison-orientdig", "/orientdig-shipping/"),
        ("/orientdig-coupon", "/orientdig-coupons/"),
    ],
    "orientdigspreadsheets.fr": [
        ("/livraison-orientdig", "/orientdig-shipping/"),
    ],
    "orientdigspreadsheet.us": [
        ("/orientdig-spreadsheets", "/orientdig-spreadsheet/"),
        ("/orientdig-spreadsheet", "/orientdig-spreadsheet/"),
        ("/orientdig-coupons", "/orientdig-coupons/"),
        ("/how-to-use-orientdig", "/how-to-use-orientdig/"),
        ("/is-orientdig-legit", "/is-orientdig-legit/"),
        ("/orientdig-shipping", "/orientdig-shipping/"),
        ("/best-orientdig-spreadsheet", "/orientdig-spreadsheet/"),
        ("/orientdig-spreadsheet-2026", "/orientdig-spreadsheet/"),
    ],
}

EST_NOTE = {
    "at": "Schätzer-Land ist AT, nicht diese TLD, nicht DE, nicht EU.",
    "es": "El país del estimador es ES, no este TLD, no EU.",
    "fr": "Le pays de l’estimateur est FR, pas ce TLD, pas BE, pas EU.",
    "us": "Estimator country is US, not this TLD, not EU, not a hub for AT/ES/FR.",
    "de": "Schätzer-Land ist DE, nicht diese TLD, nicht AT, nicht „EU“.",
    "it": "Il paese dell’estimator è IT, non questo TLD, non EU.",
    "nl": "Estimator-land is NL, niet deze TLD, niet EU, niet BE.",
    "uk": "Estimator country is GB, not this TLD, not EU.",
}

STORE_NOTE = {
    "de": "Lager: offizielles Help 90 Tage ab stored in warehouse; am Versandmorgen denselben Artikel prüfen.",
    "es": "Almacén: Help oficial 90 días desde stored in warehouse; confirma el artículo el día del envío.",
    "fr": "Entrepôt : Help officiel 90 jours depuis stored in warehouse ; relire l’article le matin de l’envoi.",
    "it": "Magazzino: Help ufficiale 90 giorni da stored in warehouse; conferma l’articolo il giorno della spedizione.",
    "nl": "Magazijn: officiële Help 90 dagen vanaf stored in warehouse; bevestig het artikel op de verzenddag.",
    "en": "Warehouse: official Help 90 days from stored in warehouse; confirm that article the morning you ship.",
}

TRAIL = {
    "de": ("Live-Preis steht in", "dieses HTML ist keine Kasse."),
    "es": ("El dinero real está en", "este HTML no es caja."),
    "fr": ("L’argent réel est dans", "cet HTML n’est pas une caisse."),
    "it": ("I soldi veri stanno in", "questo HTML non è cassa."),
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
        "agent": "OrientDig",
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
        s = re.sub(r"\s*[—\-–:,]*\s*(invite|ref)?\s*100246065", "", s, flags=re.I)
        s = s.replace(INVITE, "")
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
    if INVITE in title:
        err.append("invite in title")
    if re.search(r"58 l[ií]neas para Espa|23[,.]81\s*USD|how to under-?declar", html, flags=re.I):
        err.append("spain snapshot / coaching")
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
        print("dest", key, spec["host"], "bytes", len(html))
    fps = {k: dest_local_pack(DESTS[k]["dest"])["fingerprint"] for k in blobs}
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
    bak = f"/www/backup/orientdig-desks-{stamp}"
    _run(client, f"mkdir -p '{bak}'")
    sftp = client.open_sftp()
    for spec in DESTS.values():
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


def patch_twins(client) -> None:
    changed = 0
    for twin, target in TWINS.items():
        path = f"/www/server/panel/vhost/nginx/{twin}.conf"
        raw = _run(client, f"cat '{path}'")
        if not raw:
            print("skip missing", twin)
            continue
        if twin in CONVERT_TWINS:
            needle = "    location / {\n        try_files $uri $uri/ $uri/index.html =404;\n    }"
            if needle in raw:
                raw = raw.replace(needle, f"    location / {{ return 301 https://{target}/; }}", 1)
                _run(client, f"cp -a '{path}' '/www/backup/orientdig-twin-{twin}.conf'")
                sftp = client.open_sftp()
                with sftp.open(path, "w") as fh:
                    fh.write(raw)
                sftp.close()
                changed += 1
                print("PATCH nginx", twin, "catch-all →", target)
            gsc = f"/www/server/panel/vhost/nginx/extension/{twin}/gsc-redirects.conf"
            graw = _run(client, f"cat '{gsc}'")
            old_host = f"https://{twin}/"
            new_host = f"https://{target}/"
            if graw and (old_host in graw or new_host in graw):
                _run(client, f"cp -a '{gsc}' '/www/backup/orientdig-gsc-{twin}.conf'")
                graw = graw.replace(old_host, new_host)
                graw = graw.replace(f"{new_host}orientdig-spreadsheets/", f"{new_host}orientdig-spreadsheet/")
                graw = graw.replace(f"{new_host}orientdig-customer-service/", f"{new_host}contact/")
                existing = set(re.findall(r"location = (/[^\s{]+)", graw))
                extras = []
                # Trailing-slash twins for ranked dest inners; GSC often only has the no-slash form.
                slash_maps = [
                    ("/orientdig-spreadsheets/", f"{new_host}orientdig-spreadsheet/"),
                    ("/how-to-use-orientdig/", f"{new_host}how-to-use-orientdig/"),
                    ("/is-orientdig-legit/", f"{new_host}is-orientdig-legit/"),
                    ("/orientdig-coupons/", f"{new_host}orientdig-coupons/"),
                    ("/orientdig-shipping/", f"{new_host}orientdig-shipping/"),
                    ("/orientdig-customer-service/", f"{new_host}contact/"),
                ]
                for loc, dest in slash_maps:
                    if loc not in existing:
                        extras.append(f"location = {loc} {{ return 301 {dest}; }}")
                if extras:
                    graw = graw.rstrip() + "\n" + "\n".join(extras) + "\n"
                sftp = client.open_sftp()
                with sftp.open(gsc, "w") as fh:
                    fh.write(graw)
                sftp.close()
                changed += 1
                print("PATCH nginx GSC redirects", twin, "→", target, "slash+", len(extras))
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
            _run(client, f"cp -a '{path}' '/www/backup/orientdig-twin-{twin}.conf'")
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
        ("at", "https://orientdig.at/", "1010 Wien", ("Packstation", "Poste Italiane", "form A1A 1A1")),
        ("es", "https://orientdig.es/", "no copiamos un recuento de líneas", ("Packstation", "1010 Wien", "form A1A 1A1")),
        ("fr", "https://orientdig.fr/", "pas un code postal belge", ("Packstation", "Poste Italiane", "1010 Wien")),
        ("us", "https://orientdig.us/", "does not invent a de-minimis dollar", ("Packstation", "form A1A 1A1", "1010 Wien")),
        ("de", "https://orientdigspreadsheet.de/", "Packstation", ("1010 Wien", "form A1A 1A1", "Poste Italiane")),
        ("it", "https://orientdigspreadsheet.it/", "Poste Italiane", ("Packstation", "form A1A 1A1", "1010 Wien")),
        ("nl", "https://orientdigspreadsheet.nl/", "Nederlandse postcode", ("Packstation", "Poste Italiane", "form A1A 1A1")),
        ("uk", "https://orientdigspreadsheet.uk/", "Northern Ireland is often another", ("Packstation", "form A1A 1A1", "Poste Italiane")),
    ]

    class NR(urllib.request.HTTPRedirectHandler):
        def redirect_request(self, req, fp, code, msg, headers, newurl):
            return None

    def fetch(url, follow=True):
        req = urllib.request.Request(url, headers={"User-Agent": "od-desk-check/1.0"})
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
        if INVITE in title:
            print("  FAIL invite in title")
            fail += 1
        if re.search(r"58 l[ií]neas para Espa|23[,.]81\s*USD|how to under-?declar", html, flags=re.I):
            print("  FAIL snapshot/coaching")
            fail += 1
        if EST not in inner:
            print("  FAIL estimator url missing")
            fail += 1

    inners = [
        "https://orientdig.at/orientdig-shipping/",
        "https://orientdig.es/orientdig-shipping-coupons/",
        "https://orientdig.fr/avis-orientdig/",
        "https://orientdig.us/orientdig-spreadsheet/",
        "https://orientdigspreadsheet.de/orientdig-shipping/",
        "https://orientdigspreadsheet.it/how-to-use-orientdig/",
        "https://orientdigspreadsheet.nl/orientdig-spreadsheets/",
        "https://orientdigspreadsheet.uk/orientdig-spreadsheets/",
    ]
    for url in inners:
        code, final, _, body = fetch(url, follow=True)
        if code == 404 or len(body) < 8000:
            print("FAIL inner", url, code, len(body))
            fail += 1
        else:
            print("inner", code, len(body), final)

    dest_urls = [f"https://{spec['host']}/" for spec in DESTS.values()]
    for a in dest_urls:
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
        deep = (
            f"https://{twin}/orientdig-spreadsheets"
            if twin.endswith(".us") or twin.endswith(".uk")
            else f"https://{twin}/how-to-use-orientdig"
        )
        code2, _, _, body2 = fetch(deep, follow=True)
        if code2 == 404 or len(body2) < 8000:
            print("  FAIL deep 404", twin, code2, len(body2))
            fail += 1
        else:
            print("  deep", twin, code2, "bytes", len(body2))
        if twin.endswith(".us"):
            code3, _, _, body3 = fetch(f"https://{twin}/orientdig-spreadsheets/", follow=True)
            if code3 == 404 or len(body3) < 8000:
                print("  FAIL deep slash 404", twin, code3, len(body3))
                fail += 1
            else:
                print("  deep-slash", twin, code3, "bytes", len(body3))

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
