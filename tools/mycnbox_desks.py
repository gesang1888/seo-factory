#!/usr/bin/env python3
"""MyCNBox country desks: dest-unique #local, keep ranked CMS inners.

Gates:
1. Each host #local has that dest fingerprint, no sister fingerprints.
2. Estimator country ≠ TLD; .eu / haul.com must say they are not a customs territory.
3. Titles have no invite code; body has no customs coaching / 58-line snapshot.
4. Same-agent country URLs stay independent (no 301).
5. No same-country twins on this cluster to convert.
6. Do not PUT a 5KB template over unique CMS — surgical insert on Georgia homes;
   ranked 24–58KB inners stay.
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
EST = "https://www.mycnbox.com/estimation/"
OFFICIAL = "https://www.mycnbox.com/"
HELP = "https://mycnbox.com/FAQDetail?id=83"
DATE = "2 Oct 2026"
INVITE = "AABZKT"
STORAGE = (
    "Official Help: 90 free warehouse days "
    f"({HELP}); confirm that article the morning you ship"
)

DESTS = {
    "uk": {
        "host": "mycnbox.co.uk",
        "lang": "en-GB",
        "loc": "en",
        "dest": "GB",
        "dest_label": "the United Kingdom",
        "ccy": "GBP",
        "title": "MyCNBox UK — Royal Mail lines, GBP, HMRC notes",
        "h1": "MyCNBox for a UK delivery address (GBP, Royal Mail last-mile)",
        "keep": [
            ("/is-mycnbox-legit/", "Is it legit?"),
            ("/mycnbox-coupons/", "Coupons article"),
            ("/mycnbox-shipping-guide/", "UK shipping"),
            ("/mycnbox-spreadsheet/", "Spreadsheet"),
        ],
    },
    "de": {
        "host": "mycnbox.de",
        "lang": "de-DE",
        "loc": "de",
        "dest": "DE",
        "dest_label": "Deutschland",
        "ccy": "EUR",
        "title": "MyCNBox Deutschland — Zoll, DHL und Packstation",
        "h1": "MyCNBox für eine deutsche Adresse (EUR, Packstation möglich)",
        "keep": [
            ("/mycnbox-spreadsheet/", "Spreadsheet DE"),
            ("/mycnbox-shipping-guide/", "Versand DE"),
            ("/how-to-use-mycnbox/", "Anleitung"),
            ("/is-mycnbox-legit/", "Seriös?"),
        ],
    },
    "es": {
        "host": "mycnbox.es",
        "lang": "es-ES",
        "loc": "es",
        "dest": "ES",
        "dest_label": "España",
        "ccy": "EUR",
        "title": "MyCNBox España — Correos, envío CMS y spreadsheet",
        "h1": "MyCNBox para una dirección en España (EUR, Correos)",
        "keep": [
            ("/mycnbox-invite-code/", "Código (artículo)"),
            ("/mycnbox-community/", "Comunidad"),
            ("/mycnbox-shipping-guide/", "Envío"),
            ("/how-to-use-mycnbox/", "Cómo usar"),
        ],
    },
    "fr": {
        "host": "mycnbox.fr",
        "lang": "fr-FR",
        "loc": "fr",
        "dest": "FR",
        "dest_label": "la France",
        "ccy": "EUR",
        "title": "MyCNBox France — Colissimo, avis et livraison déjà classés",
        "h1": "MyCNBox pour une adresse en France (EUR, pas un code postal belge)",
        "keep": [
            ("/mycnbox-shipping-guide/", "Livraison"),
            ("/mycnbox-community/", "Communauté"),
            ("/mycnbox-spreadsheet/", "Spreadsheet"),
            ("/how-to-use-mycnbox/", "Tutoriel"),
        ],
    },
    "nl": {
        "host": "mycnbox.nl",
        "lang": "nl-NL",
        "loc": "nl",
        "dest": "NL",
        "dest_label": "Nederland",
        "ccy": "EUR",
        "title": "MyCNBox Nederland — Nederlandse postcode, geen Duitse automaat",
        "h1": "MyCNBox voor een Nederlands adres (EUR, Nederlandse postcode)",
        "keep": [
            ("/mycnbox-shoes-spreadsheet/", "Shoes sheet"),
            ("/mycnbox-shipping-guide/", "Verzending"),
            ("/is-mycnbox-legit/", "Legit?"),
            ("/mycnbox-spreadsheet/", "Spreadsheet"),
        ],
    },
    "pl": {
        "host": "mycnbox.pl",
        "lang": "pl-PL",
        "loc": "pl",
        "dest": "PL",
        "dest_label": "Polska",
        "ccy": "PLN",
        "title": "MyCNBox Polska — InPost / Poczta, PLN, kod 00-001 Warszawa",
        "h1": "MyCNBox na adres w Polsce (PLN, 00-001 Warszawa)",
        "keep": [
            ("/mycnbox-qc-guide/", "QC"),
            ("/mycnbox-spreadsheet/", "Spreadsheet PL"),
            ("/how-to-use-mycnbox/", "Poradnik"),
            ("/mycnbox-shipping-guide/", "Wysyłka"),
        ],
    },
}

HUBS = {
    "eu": {
        "host": "mycnbox.eu",
        "lang": "en",
        "loc": "en",
        "dest": None,
        "dest_label": "a country in the estimator",
        "ccy": "EUR",
        "title": "MyCNBox.eu — not a customs territory; pick a member-state",
        "h1": "MyCNBox.eu is not a customs territory — pick a real country",
        "keep": [
            ("/mycnbox-refund-guide/", "Refund guide"),
            ("/mycnbox-shipping-guide/", "Shipping / fiscal notes"),
            ("/how-to-use-mycnbox/", "How to use"),
            ("/mycnbox-spreadsheet/", "Spreadsheet"),
        ],
    },
    "haul": {
        "host": "mycnboxhaul.com",
        "lang": "en",
        "loc": "en",
        "dest": None,
        "dest_label": "a country in the estimator",
        "ccy": "USD",
        "title": "MyCNBox haul SOP — not a customs territory",
        "h1": "This haul hostname is not a customs territory",
        "keep": [
            ("/spreadsheet-finds/", "Spreadsheet finds"),
            ("/shipping-calculator/", "Shipping / rehearsal"),
            ("/help/", "Help"),
            ("/reviews/", "Reviews"),
        ],
    },
}

EST_NOTE = {
    "uk": "Estimator country is GB, not this TLD, not EU, not the .eu hub.",
    "de": "Schätzer-Land ist DE, nicht diese TLD, nicht AT, nicht „EU“.",
    "es": "El país del estimador es ES, no este TLD, no EU.",
    "fr": "Le pays de l’estimateur est FR, pas ce TLD, pas BE, pas EU.",
    "nl": "Estimator-land is NL, niet deze TLD, niet EU, niet BE.",
    "pl": "Kraj estimatora to PL, nie ta TLD, nie DE, nie „EU”.",
    "eu": "This .eu hub is not a customs territory. Pick DE, ES, FR, NL or PL in the estimator — not this hostname, not “EU” as one country.",
    "haul": "This .com haul host is not a customs territory. Pick the real ship-to country in the estimator, not this hostname.",
}

STORE_NOTE = {
    "de": "Lager: offizielles Help 90 Tage gratis; am Versandmorgen denselben Artikel prüfen.",
    "es": "Almacén: Help oficial 90 días gratis; confirma el artículo el día del envío.",
    "fr": "Entrepôt : Help officiel 90 jours gratuits ; relire l’article le matin de l’envoi.",
    "nl": "Magazijn: officiële Help 90 dagen gratis; bevestig het artikel op de verzenddag.",
    "pl": "Magazyn: oficjalny Help 90 dni gratis; potwierdź artykuł rano w dniu nadania.",
    "en": "Warehouse: official Help 90 free days; confirm that article the morning you ship.",
}

TRAIL = {
    "de": ("Live-Preis steht in", "dieses HTML ist keine Kasse."),
    "es": ("El dinero real está en", "este HTML no es caja."),
    "fr": ("L’argent réel est dans", "cet HTML n’est pas une caisse."),
    "nl": ("Live-geld staat in", "deze HTML is geen kassa."),
    "pl": ("Prawdziwe pieniądze są w", "ten HTML nie jest kasą."),
    "en": ("Live money is in", "this HTML is not checkout."),
}

DEST_LOCAL_CSS = (
    ".sg-sec#local{margin:1.25rem 0 0}"
    ".sg-sec#local h2{margin-top:0}"
    ".ssub{color:var(--muted,#57534e);font-size:.95rem;margin:0 0 12px}"
)


def _facts(spec: dict) -> dict:
    return {
        "agent": "MyCNBox",
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
        s = re.sub(r"\s*[—\-–:,]*\s*(invite|ref|code)?\s*AABZKT", "", s, flags=re.I)
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
    fps = {
        k: dest_local_pack(specs[k].get("dest"))["fingerprint"]
        for k in blobs
    }
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


def put() -> None:
    generate()
    client = _connect()
    stamp = time.strftime("%Y%m%d-%H%M%S")
    bak = f"/www/backup/mycnbox-desks-{stamp}"
    _, out, err = client.exec_command(f"mkdir -p '{bak}'", timeout=30)
    out.read()
    sftp = client.open_sftp()
    specs = list(DESTS.values()) + list(HUBS.values())
    for spec in specs:
        local = OUT / spec["host"] / "overlay" / "index.html"
        remote = f"/www/wwwroot/{spec['host']}/index.html"
        raw = local.read_text(encoding="utf-8")
        if 'id="local"' not in raw:
            raise SystemExit(f"refusing to PUT {spec['host']} without #local")
        _, o, e = client.exec_command(f"cp -a '{remote}' '{bak}/{spec['host']}.index.html'", timeout=30)
        o.read()
        sftp.put(str(local), remote)
        print("PUT", remote, "bytes", local.stat().st_size)
    sftp.close()
    print("backup", bak)
    print("no same-country twins to convert")
    client.close()


def live_check() -> None:
    import urllib.request

    pairs = [
        ("uk", "https://mycnbox.co.uk/", "Northern Ireland is often another", ("Packstation", "form A1A 1A1", "00-001 Warszawa")),
        ("de", "https://mycnbox.de/", "Packstation", ("1010 Wien", "form A1A 1A1", "00-001 Warszawa")),
        ("es", "https://mycnbox.es/", "no copiamos un recuento de líneas", ("Packstation", "1010 Wien", "00-001 Warszawa")),
        ("fr", "https://mycnbox.fr/", "pas un code postal belge", ("Packstation", "Poste Italiane", "00-001 Warszawa")),
        ("nl", "https://mycnbox.nl/", "Nederlandse postcode", ("Packstation", "form A1A 1A1", "00-001 Warszawa")),
        ("pl", "https://mycnbox.pl/", "00-001 Warszawa", ("Packstation", "form A1A 1A1", "1010 Wien")),
        ("eu", "https://mycnbox.eu/", "not a customs territory", ("1010 Wien", "Packstation", "00-001 Warszawa")),
        ("haul", "https://mycnboxhaul.com/", "not a customs territory", ("1010 Wien", "Packstation", "00-001 Warszawa")),
    ]

    class NR(urllib.request.HTTPRedirectHandler):
        def redirect_request(self, req, fp, code, msg, headers, newurl):
            return None

    def fetch(url, follow=True):
        req = urllib.request.Request(url, headers={"User-Agent": "mcb-desk-check/1.0"})
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
        "https://mycnbox.co.uk/is-mycnbox-legit/",
        "https://mycnbox.de/mycnbox-spreadsheet/",
        "https://mycnbox.es/mycnbox-shipping-guide/",
        "https://mycnbox.fr/mycnbox-shipping-guide/",
        "https://mycnbox.nl/mycnbox-shipping-guide/",
        "https://mycnbox.pl/mycnbox-spreadsheet/",
        "https://mycnbox.eu/mycnbox-refund-guide/",
        "https://mycnboxhaul.com/spreadsheet-finds/",
    ]
    for url in inners:
        code, final, _, body = fetch(url, follow=True)
        if code == 404 or len(body) < 8000:
            print("FAIL inner", url, code, len(body))
            fail += 1
        else:
            print("inner", code, len(body), final)

    dest_urls = [f"https://{spec['host']}/" for spec in list(DESTS.values()) + list(HUBS.values())]
    for a in dest_urls:
        code, _, loc, _ = fetch(a, follow=False)
        if code in (301, 302, 303, 307, 308) and loc:
            print("FAIL 301", a, "->", loc)
            fail += 1
        else:
            print("indep", a, code)

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
