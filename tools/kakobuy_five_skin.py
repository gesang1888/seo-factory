#!/usr/bin/env python3
"""Public-facing Kakobuy dest skin: no ops notes, official orange, local money, photos.

Applies to the five independent country hosts. Does not smash unique /ohje/
article body beyond ops-phrase scrub. Does not coach a declared value.
"""
from __future__ import annotations

import os
import re
import sys
import time
from pathlib import Path

_TOOLS = Path(__file__).resolve().parent
if str(_TOOLS) not in sys.path:
    sys.path.insert(0, str(_TOOLS))
from kakobuy_five_dest import HOSTS, ORDER, overlay, _connect, _run  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
STAMP = "20261101"
SKIN = f'data-kakobuy-skin="{STAMP}"'
SHARED = ROOT / "sites" / "kakobuy-shared"
OFFICIAL_CSS = SHARED / "kakobuy-official.css"
THEME_CSS = SHARED / "kakobuy-theme.css"
LOGO = SHARED / "official" / "logo.png"
XD = SHARED / "official" / "xd.webp"
OFFICIAL_MP4 = "https://nstatic.kakobuy.com/www/kakobuy.mp4"

SKIP_FILE = re.compile(
    r"live-base|/DEPLOY|\.platform-patched|\.step4-patched|\.fi-deepen|\.ops-scrub"
)

TOPBAR = {
    "kakobuy.fi": "Suomi · EUR · Posti / Tulli",
    "kakospreadsheet.ca": "Canada · CAD · Canada Post / CBSA",
    "kakospreadsheet.es": "España · EUR · Correos",
    "kakospreadsheet.fr": "France · EUR · Colissimo",
    "kakospreadsheet.nl": "Nederland · EUR · PostNL / DHL",
}
CCY = {
    "kakobuy.fi": "EUR",
    "kakospreadsheet.ca": "CAD",
    "kakospreadsheet.es": "EUR",
    "kakospreadsheet.fr": "EUR",
    "kakospreadsheet.nl": "EUR",
}
HSUB = {
    "kakobuy.fi": "Kakobuy Suomelle: spreadsheet, finds, QC ja toimitus euroissa. Tilaukset kakobuy.comissa.",
    "kakospreadsheet.ca": "Kakobuy for Canada: spreadsheet, finds, QC and shipping in CAD. Order on kakobuy.com.",
    "kakospreadsheet.es": "Kakobuy para España: spreadsheet, finds, QC y envío en EUR. Pedidos en kakobuy.com.",
    "kakospreadsheet.fr": "Kakobuy pour la France : spreadsheet, finds, QC et livraison en EUR. Commandes sur kakobuy.com.",
    "kakospreadsheet.nl": "Kakobuy voor Nederland: spreadsheet, finds, QC en verzending in EUR. Bestellen op kakobuy.com.",
}
FOOTER_BLURB = {
    "kakobuy.fi": "Kakobuy Suomi — spreadsheet, finds ja QC. Tilaa osoitteessa kakobuy.com.",
    "kakospreadsheet.ca": "Kakobuy Canada — spreadsheet, finds and QC. Order on kakobuy.com.",
    "kakospreadsheet.es": "Kakobuy España — spreadsheet, finds y QC. Pedidos en kakobuy.com.",
    "kakospreadsheet.fr": "Kakobuy France — spreadsheet, finds et QC. Commandes sur kakobuy.com.",
    "kakospreadsheet.nl": "Kakobuy Nederland — spreadsheet, finds en QC. Bestellen op kakobuy.com.",
}
GUIDES_H2 = {
    "fi": "Oppaat",
    "en": "Guides",
    "es": "Guías",
    "fr": "Guides",
    "nl": "Gidsen",
}
SITE_COL = {
    "fi": "Sivusto",
    "en": "This site",
    "es": "Este sitio",
    "fr": "Ce site",
    "nl": "Deze site",
}
LANGS_H = {
    "fi": "Kieli / alue",
    "en": "Language / region",
    "es": "Idioma / región",
    "fr": "Langue / région",
    "nl": "Taal / regio",
}
INNER_IMG = {
    "spreadsheet": "/media/official-home-20261001.jpg",
    "finds": "/img/cat/sneakers.jpg",
    "qc": "/media/help-restricted-20261001.jpg",
    "shipping": "/media/estimator-20261001.jpg",
    "legal": "/media/official-home-20261001.jpg",
    "guide": "/media/official-home-20261001.jpg",
    "faq": "/img/cat/hoodie.jpg",
}
CAT_GRID = [
    ("/img/cat/sneakers.jpg", "Sneakers"),
    ("/img/cat/hoodie.jpg", "Hoodie"),
    ("/img/cat/bags.jpg", "Bags"),
]


def _host_loc(host: str) -> str:
    return HOSTS[host]["loc"]


def scrub_ops(html: str, host: str) -> str:
    loc = _host_loc(host)
    html = re.sub(r'<div class="hbg">[^<]*</div>\s*', "", html)
    html = re.sub(
        r"Confirm the live Kakobuy Help Center[\s\S]{0,320}?this desk does not pick a number\.?",
        "",
        html,
        flags=re.I,
    )

    def kept_repl(m: re.Match) -> str:
        block = m.group(0)
        block = re.sub(r"<span>[^<]*</span>", "", block)
        block = re.sub(
            r"\s*\((?:rankkaava URL|ranked URL|artículo;[^)]*|artikkeli säilyy)\)",
            "",
            block,
            flags=re.I,
        )
        block = block.replace("Vanha faq-stub (säilytetään)", "FAQ")
        block = block.replace("About existant (conservé)", "À propos")
        block = block.replace("Bestaande about (behouden)", "Over ons")
        block = block.replace("About existente (se conserva)", "Sobre nosotros")
        block = block.replace("About existant (conservé)", "À propos")
        block = re.sub(r"<h2>[^<]*</h2>", f"<h2>{GUIDES_H2[loc]}</h2>", block, count=1)
        return block.replace('id="kept"', 'id="guides"')

    html = re.sub(
        r'<section class="sg-sec" id="kept">[\s\S]*?</section>',
        kept_repl,
        html,
        count=1,
        flags=re.I,
    )
    html = re.sub(r'<p class="legal-note">[\s\S]*?</p>\s*', "", html)
    html = re.sub(
        r"<strong>\s*(?:Spreadsheet(?:-)?klusteri|Spreadsheet cluster|Cluster spreadsheet)\s*</strong>\s*",
        "",
        html,
        flags=re.I,
    )
    phrases = [
        r"Sister country hosts stay separate files\s*—\s*no 301\.?",
        r"Los hosts hermanos siguen en archivos separados\s*—\s*sin 301\.?",
        r"Hôtes sœurs(?: en fichiers séparés)?\s*—\s*pas de 301\.?",
        r"Les hôtes sœurs restent des fichiers séparés\s*—\s*pas de 301\.?",
        r"Zusterhosts blijven aparte bestanden\s*—\s*geen 301\.?",
        r"Zushosts blijven aparte bestanden\s*—\s*geen 301\.?",
        r"Sisarhostit(?: pysyvät erillisinä tiedostoina| erillisinä tiedostoina)\s*—\s*ei 301\.?",
        r"Sisarhostit pysyvät erillisinä tiedostoina\s*—\s*ei 301\.?",
        r"Copy reviewed [^.<]{0,40}\.?",
        r"Teksti tarkistettu [^.<]{0,40}\.?",
        r"Texto revisado [^.<]{0,40}\.?",
        r"Relu [^.<]{0,40}\.?",
        r"Tekst nagekeken [^.<]{0,40}\.?",
        r"Tekst [^.<]{0,20}2026-11-01\.?",
        r"Texto 2026-11-01\.?",
        r"Teksti 2026-11-01\.?",
        r"this HTML is not checkout\.?",
        r"cet HTML n’est pas une caisse\.?",
        r"cet HTML n'est pas une caisse\.?",
        r"este HTML no es caja\.?",
        r"deze HTML is geen kassa\.?",
        r"tämä HTML ei ole kassa\.?",
        r"not a location-name swap\.?",
        r"ei pelkkä maan nimen vaihto\.?",
        r"Lab(?:o|oratorio)?(?:\s*fret)?\s*1\s*Oct(?:obre)?\s*2026\.?",
        r"Lab 1 oct 2026\.?",
        r"1\. loka 2026\.?",
        r"Mitattu 1 Oct 2026\.?",
        r"Measured 1 Oct 2026\.?",
        r"this hostname is not a \.ca 301 from another agent\.?",
        r"Ce desk n’est pas la Belgique\.?",
        r"Ce desk n'est pas la Belgique\.?",
        r"Tällä hostilla jo rankkaava toimitus-URL säilyy[^.<]{0,80}\.?",
        r"Ranked shipping-to-Canada URL on this host stays\.?",
        r"Ranked /kakobuy-shipping-to-canada/ stays\.?",
        r"/kakobuy-toimitus/ ja /kakobuy-kokemuksia/ säilyvät\.?",
        r"GST/HST articles already ranking on this host stay[^.<]{0,80}\.?",
        r"we do not copy a rate into this title\.?",
        r"Paikalliset laitokset",
        r"Local editions",
        r"Éditions locales",
        r"Ediciones locales",
        r"Lokale edities",
        r"Independent CA desk · ",
        r"Escritorio ES independiente · no copiamos un recuento de líneas ajeno · ",
        r"Onafhankelijke desks:",
        r"Riippumattomat deskit:",
        r"Independent desks:",
        r"Desks indépendants:",
        r"Desks independientes:",
        r" · riippumaton desk",
        r" · independent desk",
        r" · desk indépendant",
        r" · escritorio independiente",
        r" · onafhankelijke desk",
        r"\(rankkaava URL\)",
        r"\(ranked URL\)",
        r"artikkeli säilyy",
        r"article remains",
        r"not overwritten",
        r"ei ylikirjoiteta",
        r"niet overschreven",
        r"non écrasé",
        r"no se pisa",
    ]
    for pat in phrases:
        html = re.sub(pat, "", html, flags=re.I)
    # “desk” as ops noun — keep “desktop” out of scope
    html = re.sub(r"\binfodeck\b", "", html, flags=re.I)
    html = re.sub(r"\binfodesk\b", "site", html, flags=re.I)
    html = re.sub(r"riippumaton infodesk", "Kakobuy Suomi", html, flags=re.I)
    html = re.sub(r"riippumaton desk", "Kakobuy Suomi", html, flags=re.I)
    html = re.sub(r"tämän deskin", "tämän sivuston", html, flags=re.I)
    html = re.sub(r"tällä deskillä", "tällä sivustolla", html, flags=re.I)
    html = re.sub(r"tämä desk", "tämä sivusto", html, flags=re.I)
    html = re.sub(r"Tämä desk", "Tämä sivusto", html)
    html = re.sub(r"this desk", "this site", html, flags=re.I)
    html = re.sub(r"this Desk", "this site", html)
    html = re.sub(r"Independent CA desk", "Kakobuy Canada", html, flags=re.I)
    html = re.sub(r"independent desk", "Kakobuy", html, flags=re.I)
    html = re.sub(r"information desk", "site", html, flags=re.I)
    html = re.sub(r"escritorio informativo", "sitio", html, flags=re.I)
    html = re.sub(r"desk d’information", "site", html, flags=re.I)
    html = re.sub(r"desk d'information", "site", html, flags=re.I)
    html = re.sub(r"desk indépendant", "site Kakobuy", html, flags=re.I)
    html = re.sub(r"ce desk", "ce site", html, flags=re.I)
    html = re.sub(r"onafhankelijke infodesk", "Kakobuy Nederland", html, flags=re.I)
    html = re.sub(r"onafhankelijke desk", "Kakobuy Nederland", html, flags=re.I)
    html = re.sub(r"deze desk", "deze site", html, flags=re.I)
    html = re.sub(r"Kakobuy independent desk", "Kakobuy", html)
    html = re.sub(r'"Kakobuy desk"', '"Kakobuy"', html)
    html = html.replace("Kakobuy Kakobuy", "Kakobuy")
    html = re.sub(
        r"Sisarhostit \([^)]*\) pysyvät erillisinä tiedostoina — ei 301\.?",
        "",
        html,
        flags=re.I,
    )
    html = re.sub(
        r"Sister hosts \([^)]*\) stay separate files — no 301\.?",
        "",
        html,
        flags=re.I,
    )
    html = re.sub(r"Sister hosts are not 301s of this page\.?", "", html, flags=re.I)
    html = re.sub(r"Zusterhosts zijn geen 301\.?", "", html, flags=re.I)
    html = re.sub(r"Los hosts hermanos siguen en archivos separados — no 301\.?", "", html, flags=re.I)
    html = html.replace("riippumaton site", "Kakobuy-sivusto")
    html = html.replace("Vanha faq-stub (säilytetään)", "FAQ")
    html = html.replace("Kuponki ()", "Kuponki")
    html = html.replace("Coupons ()", "Coupons")
    html = re.sub(r"Jo tällä hostilla \(säilytetään\):", "", html)
    html = re.sub(r"Already on this host \(kept\):", "", html)
    html = re.sub(r"Ya en este host \(se conserva\):", "", html)
    html = re.sub(r"Déjà sur cet hôte \(conservé\):", "", html)
    html = re.sub(r"Al op deze host \(behouden\):", "", html)
    html = html.replace("tästä deskistä", "tästä sivustosta")
    html = html.replace("FI-deskiltä", "tältä sivustolta")
    html = html.replace("NL-desk", "site")
    html = html.replace("Kakobuy-desk", "Kakobuy")
    html = html.replace("Spreadsheet-klusteri", "Spreadsheet")
    html = re.sub(r'aria-label="Spreadsheet cluster"', 'aria-label="Kakobuy"', html)
    html = re.sub(r'<div class="locale-switcher-heading"></div>', "", html)
    html = html.replace("Tällä isäntänimellä ei kassata.", "")
    html = html.replace("ei tätä isäntänimeä.", "")
    html = html.replace("not this TLD, not US.", "not the US.")
    html = re.sub(r"redactionele desk", "site", html)
    html = re.sub(r"toimituksellinen desk", "sivusto", html)
    html = re.sub(r"Desk FR indépendant :", "", html)
    html = html.replace("tältä deskiltä", "tältä sivustolta")
    html = re.sub(r"si le desk est la France", "pour la France", html, flags=re.I)
    html = re.sub(r"Mesur[ée] 1 Oct(?:obre|\.)? 2026\.?", "", html, flags=re.I)
    html = re.sub(r"Mesure 1 Oct(?:obre|\.)? 2026\.?", "", html, flags=re.I)
    html = re.sub(r"Varasto:\s*\.\s*", "", html)
    html = re.sub(r"Varastokello:\s*\.\s*", "", html)
    html = re.sub(r"Stockage\s*:\s*\.\s*", "", html)
    html = re.sub(r"Horloge de stockage\s*:\s*\.\s*", "", html)
    html = re.sub(r"Storage:\s*\.\s*", "", html)
    html = html.replace("tältä deskiltä", "tältä sivustolta")
    html = html.replace("ei tilata tältä deskiltä", "ei tilata täältä")
    html = re.sub(r"Ei virallinen Kakobuy-sivusto\.?\s*", "", html)
    html = re.sub(r"Niet de officiële Kakobuy-site\.?\s*", "", html)
    html = re.sub(r"Pas le site officiel Kakobuy\.?\s*", "", html)
    html = re.sub(r"No es el sitio oficial de Kakobuy\.?\s*", "", html)
    html = re.sub(r"Not the official Kakobuy site\.?\s*", "", html)
    html = re.sub(r" · \s*·", " ·", html)
    return html


def patch_theme_vars(html: str) -> str:
    html = html.replace(
        ":root{--primary:#0284c7;--primary-soft:#e0f2fe;--ink:#0f172a;--muted:#475569;--line:#e5e7eb;--bg:#f8fafc}",
        ":root{--primary:#ff5000;--primary-soft:#fff1eb;--ink:#333;--muted:#666;--line:#f0f0f0;--bg:#f5f5f5}",
    )
    html = html.replace(".topbar{background:#0c4a6e;color:#e0f2fe;font-size:13px}", ".topbar{background:#ff5000;color:#fff;font-size:13px}")
    html = html.replace("border-radius:9px", "border-radius:4px")
    if "kakobuy-official.css" not in html:
        html = html.replace(
            "</head>",
            '<link rel="stylesheet" href="/assets/css/kakobuy-official.css?v=20261101-skin">\n</head>',
            1,
        )
    html = re.sub(
        r'src="/assets/kakobuy-logo\.png"',
        'src="/assets/kakobuy-official-logo.png"',
        html,
    )
    html = html.replace('kakobuy-theme.css?v=20261001-home', "kakobuy-theme.css?v=20261101-skin")
    return html


def patch_topbar(html: str, host: str) -> str:
    bar = TOPBAR[host]
    html = re.sub(
        r'(<div class="topbar"><div class="container">)[\s\S]*?(</div></div>)',
        rf"\1{bar}\2",
        html,
        count=1,
    )
    ccy = CCY[host]
    if 'class="kb-ccy"' not in html:
        html = html.replace(
            '<div class="header-actions">',
            f'<div class="header-actions"><span class="kb-ccy" aria-label="currency">{ccy}</span>',
            1,
        )
    return html


def patch_hero(html: str, host: str, is_home: bool) -> str:
    html = re.sub(
        r'(<p class="hsub">)[\s\S]*?(</p>)',
        rf"\1{HSUB[host]}\2",
        html,
        count=1,
    )
    if is_home and "kb-hero-visual" not in html and 'class="sg-hero"' in html:
        visual = (
            '<div class="kb-hero-visual">'
            f'<video autoplay muted loop playsinline poster="/media/official-home-20261001.jpg" aria-label="Kakobuy">'
            f'<source src="{OFFICIAL_MP4}" type="video/mp4">'
            "</video>"
            "</div>"
        )
        html = re.sub(
            r'(<section class="sg-hero">)',
            rf"\1{visual}",
            html,
            count=1,
        )
    return html


def patch_footer(html: str, host: str) -> str:
    loc = _host_loc(host)
    html = re.sub(
        r'(<div class="footer-brand">[\s\S]*?<p>)[\s\S]*?(</p>)',
        rf"\1{FOOTER_BLURB[host]}\2",
        html,
        count=1,
    )
    html = re.sub(
        r"<h5>Tällä hostilla</h5>|<h5>On this host</h5>|<h5>En este host</h5>|<h5>Sur cet hôte</h5>|<h5>Op deze host</h5>",
        f"<h5>{SITE_COL[loc]}</h5>",
        html,
        count=1,
    )
    html = re.sub(
        r'(<p class="footer-locale-cluster"[^>]*>)[^<]*',
        rf"\1{LANGS_H[loc]}: ",
        html,
        count=1,
    )
    html = re.sub(
        r'(<div class="footer-bottom"><div>)[^<]*(</div></div>)',
        rf"\1© 2026 {host} · {CCY[host]}\2",
        html,
        count=1,
    )
    return html


def patch_figcaptions(html: str) -> str:
    # Drop lab/ops captions; keep the photo.
    html = re.sub(
        r"<figcaption>[\s\S]*?(?:Lab|loka 2026|desk|SPA render|este desk|tämä desk)[\s\S]*?</figcaption>",
        "",
        html,
        flags=re.I,
    )
    return html


def ensure_inner_images(html: str, path: Path) -> str:
    if "<article" not in html or "kb-illust" in html:
        return html
    kind = "spreadsheet"
    m = re.search(r'data-kind="([^"]+)"', html)
    if m:
        kind = m.group(1)
    slug = path.parent.name
    if slug in ("kakobuy-finds",):
        kind = "finds"
    elif slug in ("kakobuy-qc",):
        kind = "qc"
    elif "shipping" in slug or "toimitus" in slug or "envio" in slug or "livraison" in slug or "verzending" in slug:
        kind = "shipping"
    src = INNER_IMG.get(kind, "/media/official-home-20261001.jpg")
    fig = (
        f'<figure class="kb-illust"><img src="{src}" alt="Kakobuy" width="1400" height="900" '
        'loading="lazy" decoding="async"></figure>'
    )
    if kind == "finds":
        cells = "".join(
            f'<img src="{u}" alt="{a}" width="560" height="560" loading="lazy">'
            for u, a in CAT_GRID
        )
        fig += f'<div class="kb-illust-grid">{cells}</div>'
    if re.search(r'<p class="lead">[\s\S]*?</p>', html):
        html = re.sub(
            r'(<p class="lead">[\s\S]*?</p>)',
            rf"\1\n{fig}",
            html,
            count=1,
        )
    return html


def mark_body(html: str) -> str:
    if "data-kakobuy-skin=" in html:
        html = re.sub(r'data-kakobuy-skin="[^"]*"', SKIN, html, count=1)
        return html
    html = re.sub(r"<body\b", f"<body {SKIN}", html, count=1)
    return html


def process_file(host: str, path: Path) -> bool:
    html = path.read_text(encoding="utf-8")
    orig = html
    is_home = path.name == "index.html" and path.parent.name == "overlay"
    html = scrub_ops(html, host)
    html = patch_theme_vars(html)
    html = patch_topbar(html, host)
    html = patch_hero(html, host, is_home)
    html = patch_footer(html, host)
    html = patch_figcaptions(html)
    if not is_home:
        html = ensure_inner_images(html, path)
    html = mark_body(html)
    if html != orig:
        path.write_text(html, encoding="utf-8")
        return True
    return False


def generate() -> list[Path]:
    written: list[Path] = []
    for host in ORDER:
        root = overlay(host)
        for path in sorted(root.rglob("index.html")):
            if SKIP_FILE.search(str(path)):
                continue
            if process_file(host, path):
                written.append(path)
                print("SKIN", path.relative_to(ROOT))
        # shared assets copied into overlay so PUT can send them
        asset_css = root / "assets" / "css"
        asset_css.mkdir(parents=True, exist_ok=True)
        dest_off = asset_css / "kakobuy-official.css"
        dest_off.write_bytes(OFFICIAL_CSS.read_bytes())
        dest_theme = asset_css / "kakobuy-theme.css"
        dest_theme.write_bytes(THEME_CSS.read_bytes())
        logo_dir = root / "assets"
        logo_dir.mkdir(parents=True, exist_ok=True)
        (logo_dir / "kakobuy-official-logo.png").write_bytes(LOGO.read_bytes())
        (logo_dir / "kakobuy-xd.webp").write_bytes(XD.read_bytes())
        written.extend([dest_off, dest_theme, logo_dir / "kakobuy-official-logo.png", logo_dir / "kakobuy-xd.webp"])
    return written


def put(files: list[Path] | None = None) -> None:
    if files is None:
        files = generate()
    client = _connect()
    stamp = time.strftime("%Y%m%d-%H%M%S")
    bak = f"/www/backup/kakobuy-five-skin-{stamp}"
    print(_run(client, f"mkdir -p '{bak}'"))
    sftp = client.open_sftp()
    n = 0
    seen_remote = set()
    for path in files:
        host = path.relative_to(ROOT / "sites").as_posix().split("/", 1)[0]
        rest = path.relative_to(overlay(host)).as_posix()
        remote = f"/www/wwwroot/{host}/{rest}"
        if remote in seen_remote:
            continue
        seen_remote.add(remote)
        _run(client, f"mkdir -p '{str(Path(remote).parent)}'")
        _run(
            client,
            f"test -f '{remote}' && mkdir -p '{bak}/{host}' && cp -a '{remote}' '{bak}/{host}/{rest.replace('/', '_')}' || true",
        )
        sftp.put(str(path), remote)
        _run(client, f"chown www:www '{remote}'")
        n += 1
        print("PUT", remote)
    sftp.close()
    client.close()
    print("PUT_DONE", n, "backup", bak)


def verify() -> None:
    from urllib.request import Request, build_opener, HTTPSHandler, HTTPRedirectHandler

    class NoRedir(HTTPRedirectHandler):
        def redirect_request(self, *a, **k):
            return None

    opener = build_opener(NoRedir(), HTTPSHandler())
    checks = [
        ("https://kakobuy.fi/", ["#ff5000", "EUR", "data-kakobuy-skin", "kakobuy.mp4"], True),
        ("https://kakospreadsheet.ca/", ["CAD", "#ff5000", "kakobuy.com"], True),
        ("https://kakospreadsheet.es/", ["EUR", "Mejores finds"], True),
        ("https://kakospreadsheet.fr/", ["EUR", "Meilleurs finds", "kakobuy-fr-independent"], True),
        ("https://kakospreadsheet.nl/", ["EUR", "Beste finds"], True),
        ("https://kakobuy.fi/kakobuy-spreadsheet/", ["kb-illust", "EUR"], True),
        ("https://kakobuy.fi/ohje/", ["Ohje"], True),
    ]
    forbid = ["no 301", "independent desk", "infodesk", "Lab 1 Oct 2026", "ei ylikirjoiteta", "not overwritten"]
    for url, needles, _ in checks:
        try:
            r = opener.open(Request(url, headers={"User-Agent": "kakobuy-skin/1.0"}), timeout=20)
            body = r.read().decode("utf-8", "replace")
            hits = [n for n in needles if n.lower() in body.lower()]
            bad = [f for f in forbid if f.lower() in body.lower()]
            print("VERIFY", r.status, url, "hits", hits, "ops", bad or "clean", "desk", r.headers.get("X-Desk"))
        except Exception as exc:  # noqa: BLE001
            print("VERIFY_ERR", url, type(exc).__name__, str(exc)[:120])


def main() -> None:
    cmd = sys.argv[1] if len(sys.argv) > 1 else "all"
    if cmd == "generate":
        generate()
    elif cmd == "put":
        put()
    elif cmd == "verify":
        verify()
    elif cmd == "all":
        files = generate()
        put(files)
        verify()
    else:
        raise SystemExit(f"unknown {cmd}")


if __name__ == "__main__":
    main()
