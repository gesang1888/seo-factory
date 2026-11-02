#!/usr/bin/env python3
"""Deepen MyCNBox dest desks to UK-cluster inner depth.

Independent country hosts (UK/DE/ES/FR/NL/PL). Does not touch mycnbox.eu or
mycnboxhaul.com hubs. Does not smash unique coupons/community/invite/shoes/qc-guide.
No declared-value coaching. GSC: sitemap submit only.
"""
from __future__ import annotations

import json
import os
import re
import sys
import time
from html import escape
from pathlib import Path

_TOOLS = Path(__file__).resolve().parent
if str(_TOOLS) not in sys.path:
    sys.path.insert(0, str(_TOOLS))
from desk_template import cluster_keywords, cluster_title, faq_ld, inject_jsonld, website_ld


def cluster_title_serp(agent: str, dest: str | None, loc: str, dest_label: str | None = None) -> str:
    """SERP title: cluster title plus Finds & QC, matching kakobuy.co.uk. H1 stays unsuffixed."""
    if loc == "pl":
        base = f"{agent} Spreadsheet dla kupujących w Polsce"
    else:
        base = cluster_title(agent, dest, loc, dest_label)
    suffix = {
        "de": " – Beste Finds & QC",
        "es": " – Mejores finds y QC",
        "fr": " – Meilleurs finds et QC",
        "it": " – Migliori finds e QC",
        "nl": " – Beste finds en QC",
        "fi": " – Finds ja QC",
        "pl": " – Finds i QC",
    }.get(loc, " – Best Finds & QC")
    return base + suffix
from mycnbox_dest_copy import inner_h1, inner_keywords, inner_serp_title, sections_for, wrap_copy
import mycnbox_dest_skin as odskin

ROOT = Path(__file__).resolve().parents[1]
STAMP = "20261102"
TODAY = "2026-11-02"
MARKER = f'data-mycnbox-dest="{STAMP}"'
_SA_CANDIDATES = [
    os.environ.get("GSC_SA_JSON", ""),
    "/tmp/hipobuy-creds/sa.json",
    "/cursor/stores/self/internal/gsc-sa.json",
]
SA = next((p for p in _SA_CANDIDATES if p and Path(p).is_file()), "/tmp/hipobuy-creds/sa.json")
BAK_NL = "/www/backup/portfolio-step5-phaseb-20261026-150339"
BAK_IT = "/www/backup/portfolio-step5-phasec-20261026-151213"
OFFICIAL = "https://www.mycnbox.com/"
EST = "https://www.mycnbox.com/"
A = "MyCNBox"
W2C_SHEET = "https://w2clinks.com/spreadsheet/mycnbox/"
PRODUCTS_PHP = (ROOT / "templates" / "api" / "products_w2c.php").read_text(encoding="utf-8")
PRODUCTS_INDEX = (ROOT / "templates" / "api" / "products_index.php").read_text(encoding="utf-8")


HOSTS = {
    "mycnbox.co.uk": {
        "key": "uk",
        "dest": "GB",
        "loc": "en",
        "lang": "en-GB",
        "label": "the United Kingdom",
        "ccy": "GBP",
        "customs": "HMRC",
        "customs_url": "https://www.gov.uk/goods-sent-from-abroad",
        "post": "Royal Mail",
        "city": "UK postcode; Northern Ireland is often another carrier product",
        "pages": {
            "spreadsheet": "mycnbox-spreadsheet",
            "finds": "mycnbox-finds",
            "qc": "mycnbox-qc",
            "shipping": "mycnbox-shipping-guide",
            "legal": "is-mycnbox-legit",
            "guide": "mycnbox-guide",
            "faq": "mycnbox-faq",
        },
        "skip": set(),
        "canon": [("mycnbox-shipping", "mycnbox-shipping-guide")],
        "nav_extra": [],
    },
    "mycnbox.de": {
        "key": "de",
        "dest": "DE",
        "loc": "de",
        "lang": "de-DE",
        "label": "Deutschland",
        "ccy": "EUR",
        "customs": "Zoll",
        "customs_url": "https://www.zoll.de/",
        "post": "DHL / Deutsche Post",
        "city": "fünfstellige PLZ, Packstation möglich",
        "pages": {
            "spreadsheet": "mycnbox-spreadsheet",
            "finds": "mycnbox-finds",
            "qc": "mycnbox-qc",
            "shipping": "mycnbox-shipping-guide",
            "legal": "is-mycnbox-legit",
            "guide": "how-to-use-mycnbox",
            "faq": "mycnbox-faq",
        },
        "skip": set(),
        "canon": [],
        "nav_extra": [],
    },
    "mycnbox.es": {
        "key": "es",
        "dest": "ES",
        "loc": "es",
        "lang": "es-ES",
        "label": "España",
        "ccy": "EUR",
        "customs": "Agencia Tributaria",
        "customs_url": "https://sede.agenciatributaria.gob.es/",
        "post": "Correos",
        "city": "código postal de cinco dígitos",
        "pages": {
            "spreadsheet": "mycnbox-spreadsheet",
            "finds": "mycnbox-finds",
            "qc": "mycnbox-qc",
            "shipping": "mycnbox-shipping-guide",
            "legal": "is-mycnbox-legit",
            "guide": "how-to-use-mycnbox",
            "faq": "mycnbox-faq",
        },
        "skip": set(),
        "canon": [],
        "nav_extra": [],
    },
    "mycnbox.fr": {
        "key": "fr",
        "dest": "FR",
        "loc": "fr",
        "lang": "fr-FR",
        "label": "la France",
        "ccy": "EUR",
        "customs": "douane.gouv.fr",
        "customs_url": "https://www.douane.gouv.fr/",
        "post": "Colissimo",
        "city": "code postal à cinq chiffres, pas un code belge",
        "pages": {
            "spreadsheet": "mycnbox-spreadsheet",
            "finds": "mycnbox-finds",
            "qc": "mycnbox-qc",
            "shipping": "mycnbox-shipping-guide",
            "legal": "is-mycnbox-legit",
            "guide": "how-to-use-mycnbox",
            "faq": "mycnbox-faq",
        },
        "skip": set(),
        "canon": [],
        "nav_extra": [],
    },
    "mycnbox.nl": {
        "key": "nl",
        "dest": "NL",
        "loc": "nl",
        "lang": "nl-NL",
        "label": "Nederland",
        "ccy": "EUR",
        "customs": "Belastingdienst Douane",
        "customs_url": "https://www.belastingdienst.nl/wps/wcm/connect/nl/douane/",
        "post": "DHL / PostNL",
        "city": "Nederlandse postcode 1234 AB",
        "pages": {
            "spreadsheet": "mycnbox-spreadsheet",
            "finds": "mycnbox-finds",
            "qc": "mycnbox-qc",
            "shipping": "mycnbox-shipping-guide",
            "legal": "is-mycnbox-legit",
            "guide": "how-to-use-mycnbox",
            "faq": "mycnbox-faq",
        },
        "skip": set(),
        "canon": [("mycnbox-shipping", "mycnbox-shipping-guide")],
        "nav_extra": [],
    },
    "mycnbox.pl": {
        "key": "pl",
        "dest": "PL",
        "loc": "pl",
        "lang": "pl-PL",
        "label": "Polska",
        "ccy": "PLN",
        "customs": "Krajowa Administracja Skarbowa",
        "customs_url": "https://www.podatki.gov.pl/",
        "post": "InPost / Poczta Polska",
        "city": "kod 00-001 Warszawa",
        "pages": {
            "spreadsheet": "mycnbox-spreadsheet",
            "finds": "mycnbox-finds",
            "qc": "mycnbox-qc",
            "shipping": "mycnbox-shipping-guide",
            "legal": "is-mycnbox-legit",
            "guide": "how-to-use-mycnbox",
            "faq": "mycnbox-faq",
        },
        "skip": set(),
        "canon": [("mycnbox-shipping", "mycnbox-shipping-guide")],
        "nav_extra": [],
    },
}

ORDER = [
    "mycnbox.co.uk",
    "mycnbox.de",
    "mycnbox.es",
    "mycnbox.fr",
    "mycnbox.nl",
    "mycnbox.pl",
]


NAV_LAB = {
    "de": {
        "spreadsheet": "Spreadsheet",
        "finds": "Finds",
        "qc": "QC",
        "shipping": "Versand",
        "legal": "Legal?",
        "guide": "Anleitung",
        "faq": "FAQ",
    },
    "es": {
        "spreadsheet": "Spreadsheet",
        "finds": "Finds",
        "qc": "QC",
        "shipping": "Envío",
        "legal": "¿Es legal?",
        "guide": "Guía",
        "faq": "FAQ",
    },
    "fr": {
        "spreadsheet": "Spreadsheet",
        "finds": "Finds",
        "qc": "QC",
        "shipping": "Livraison",
        "legal": "Avis",
        "guide": "Guide",
        "faq": "FAQ",
    },
    "it": {
        "spreadsheet": "Spreadsheet",
        "finds": "Finds",
        "qc": "QC",
        "shipping": "Spedizione",
        "legal": "È legale?",
        "guide": "Guida",
        "faq": "FAQ",
    },
    "nl": {
        "spreadsheet": "Spreadsheet",
        "finds": "Finds",
        "qc": "QC",
        "shipping": "Verzending",
        "legal": "Legaal?",
        "guide": "Handleiding",
        "faq": "FAQ",
    },
    "en": {
        "spreadsheet": "Spreadsheet",
        "finds": "Finds",
        "qc": "QC",
        "shipping": "Shipping",
        "legal": "Is it legal?",
        "guide": "Guide",
        "faq": "FAQ",
    },
    "pl": {
        "spreadsheet": "Spreadsheet",
        "finds": "Finds",
        "qc": "QC",
        "shipping": "Wysyłka",
        "legal": "Legalne?",
        "guide": "Poradnik",
        "faq": "FAQ",
    },
}

H2NAV = {
    "de": "Spreadsheet / Finds / QC / Versand",
    "es": "Spreadsheet / finds / QC / Envío",
    "fr": "Spreadsheet / finds / QC / Livraison",
    "it": "Spreadsheet / finds / QC / Spedizione",
    "nl": "Spreadsheet / finds / QC / Verzending",
    "en": "Spreadsheet / finds / QC / Shipping",
    "pl": "Spreadsheet / finds / QC / Wysyłka",
}

CTA = {
    "de": "Bestellen und zahlen auf www.mycnbox.com. Anzeige auf dieser Seite in lokaler Währung.",
    "es": "Pide y paga en www.mycnbox.com. Los precios de esta página se muestran en moneda local.",
    "fr": "Commande et paiement sur www.mycnbox.com. Les prix de cette page sont affichés en monnaie locale.",
    "it": "Ordina e paga su www.mycnbox.com. I prezzi di questa pagina sono in valuta locale.",
    "nl": "Bestellen en betalen op www.mycnbox.com. Prijzen op deze pagina staan in lokale valuta.",
    "en": "Shop and pay on www.mycnbox.com. Prices on this page are shown in local currency.",
    "pl": "Zamawiaj i płać na www.mycnbox.com. Ceny na tej stronie są w walucie lokalnej.",
}


UNIQUE_PUT = {
    "mycnbox-coupons",
    "mycnbox-invite-code",
    "mycnbox-community",
    "mycnbox-shoes-spreadsheet",
    "mycnbox-qc-guide",
    "mycnbox-customs-guide",
}


def overlay(host: str) -> Path:
    return ROOT / "sites" / host / "overlay"


def _connect():
    try:
        import paramiko
    except ImportError:
        import subprocess

        subprocess.check_call([sys.executable, "-m", "pip", "install", "paramiko", "-q"])
        import paramiko

    password = os.environ.get("ORIGIN_SSH_PASS")
    if not password:
        cred = Path("/tmp/hipobuy-creds/origin.pass")
        if cred.is_file():
            password = cred.read_text().strip()
    if not password:
        raise SystemExit("Set ORIGIN_SSH_PASS")
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect("31.97.41.31", username="root", password=password, timeout=30)
    return client


def _run(client, cmd: str, timeout: int = 90) -> str:
    _, stdout, stderr = client.exec_command(cmd, timeout=timeout)
    return (stdout.read() + stderr.read()).decode(errors="replace").strip()


def reclaim_nginx() -> None:
    print("RECLAIM_SKIP mycnbox dests already independent")
    return


def _unused_reclaim() -> None:
    """Restore dest vhosts for IT/NL (undo Phase B/C catch-all 301 to orientdig.es)."""
    client = _connect()
    stamp = time.strftime("%Y%m%d-%H%M%S")
    bak = f"/www/backup/mycnbox-dest-reclaim-{stamp}"
    print(_run(client, f"mkdir -p '{bak}'"))
    jobs = (
        ("orientdigspreadsheet.nl", f"{BAK_NL}/orientdigspreadsheet.nl.conf.bak"),
        ("orientdigspreadsheet.it", f"{BAK_IT}/orientdigspreadsheet.it.conf.bak"),
    )
    for host, src in jobs:
        live = f"/www/server/panel/vhost/nginx/{host}.conf"
        head = _run(client, f"head -c 900 '{live}'")
        sunset = "orientdig.es" in head and "return 301" in head
        if not sunset:
            print("SKIP_RESTORE", host, "already dest vhost")
            continue
        print(_run(client, f"cp -a '{live}' '{bak}/{host}.conf.before'"))
        print(_run(client, f"cp -a '{src}' '{live}'"))
        print("RESTORE", host)
    noindex = "/www/server/panel/vhost/nginx/extension/orientdigspreadsheet.nl/phaseb-noindex.conf"
    exists = _run(client, f"test -f '{noindex}' && echo YES || echo NO")
    if exists.strip() == "YES":
        print(_run(client, f"cp -a '{noindex}' '{bak}/phaseb-noindex.conf'"))
        print(_run(client, f"mv '{noindex}' '{noindex}.disabled-{stamp}'"))
        print("DISABLE NL noindex")
    print(_run(client, "nginx -t && nginx -s reload"))
    client.close()
    print("RECLAIM_NGINX", bak)


def _nav(d: dict) -> str:
    labels = NAV_LAB[d["loc"]]
    items = []
    for kind, slug in d["pages"].items():
        items.append(f'<li><a href="/{slug}/">{escape(labels.get(kind, kind))}</a></li>')
    return '<ul class="cluster-links">' + "".join(items) + "</ul>"


def _nav_links(d: dict) -> str:
    labels = NAV_LAB[d["loc"]]
    return "".join(
        f'<a href="/{slug}/">{escape(labels.get(kind, kind))}</a>' for kind, slug in d["pages"].items()
    )


def render_article(host: str, kind: str, d: dict) -> str:
    h1, lead, secs = sections_for(kind, d, host)
    loc = d["loc"]
    figs = odskin.article_figures(kind, d)
    chunks = [
        f'<article class="cluster-page" data-spreadsheet-cluster="20261030" {MARKER} data-kind="{escape(kind)}">',
        f"<h1>{escape(h1)}</h1>",
        f'<p class="lead">{escape(lead)}</p>',
    ]
    if figs:
        chunks.append(figs[0])
    for i, (h2, paras) in enumerate(secs):
        chunks.append(f"<h2>{escape(h2)}</h2>")
        for p in paras:
            chunks.append(f"<p>{escape(p)}</p>")
        if i == 1 and len(figs) > 1:
            chunks.append(figs[1])
    chunks.append(f"<h2>{escape(H2NAV[loc])}</h2>")
    chunks.append(_nav(d))
    chunks.append(f'<p class="kb-cta">{escape(CTA[loc])}</p>')
    chunks.append("</article>")
    return "\n".join(chunks) + "\n"


MAIN_RE = re.compile(r"(<main\b[^>]*>)(.*?)(</main>)", re.I | re.S)


def swap_main(html: str, inner: str) -> str:
    if not MAIN_RE.search(html):
        raise ValueError("missing <main>")
    return MAIN_RE.sub(lambda m: m.group(1) + "\n" + inner + m.group(3), html, count=1)


def upsert_meta(html: str, name: str, content: str) -> str:
    tag = f'<meta name="{name}" content="{escape(content)}">'
    if re.search(rf'<meta\s+name="{name}"', html, re.I):
        return re.sub(rf'<meta\s+name="{name}"[^>]*>', tag, html, count=1, flags=re.I)
    return html.replace("</head>", tag + "\n</head>", 1)


def patch_cluster_nav(html: str, d: dict) -> str:
    inner = _nav_links(d)
    return re.sub(
        r'<nav class="cluster-nav"[^>]*>.*?</nav>',
        f'<nav class="cluster-nav" data-spreadsheet-cluster="20261030" aria-label="MyCNBox">{inner}</nav>',
        html,
        count=1,
        flags=re.I | re.S,
    )


def _home_ld_replacer(host, serp, kws, d):
    def repl(m: re.Match) -> str:
        raw = m.group(1).strip()
        try:
            data = json.loads(raw)
        except json.JSONDecodeError:
            return m.group(0)
        if not isinstance(data, dict):
            return m.group(0)
        if data.get("@type") == "WebPage":
            data["name"] = serp
            part = data.get("isPartOf")
            if isinstance(part, dict):
                part["@type"] = "WebSite"
                part["name"] = serp
                part["url"] = f"https://{host}/"
                part["keywords"] = kws
                data["isPartOf"] = part
        if data.get("@type") == "WebSite":
            data["name"] = serp
            data["keywords"] = kws
            data["url"] = f"https://{host}/"
        return f'<script type="application/ld+json">{json.dumps(data, ensure_ascii=False)}</script>'

    return repl


def patch_home(host: str, d: dict) -> Path:
    path = overlay(host) / "index.html"
    html = path.read_text(encoding="utf-8")
    serp = cluster_title_serp(A, d["dest"], d["loc"], d["label"])
    kws = cluster_keywords(A, d["dest"], d["loc"], d["label"])
    html = patch_cluster_nav(html, d)
    html = re.sub(r"<title>[\s\S]*?</title>", f"<title>{escape(serp)}</title>", html, count=1, flags=re.I)
    h1 = cluster_title_serp(A, d["dest"], d["loc"], d["label"]).split(" – ")[0].split(" - ")[0]
    html = re.sub(r"<h1>[\s\S]*?</h1>", f"<h1>{escape(h1)}</h1>", html, count=1, flags=re.I)
    html = re.sub(
        r'(<meta\s+property="og:title"\s+content=")[^"]*(")',
        rf"\1{escape(serp)}\2",
        html,
        count=1,
        flags=re.I,
    )
    html = re.sub(
        r'<script type="application/ld\+json">([\s\S]*?)</script>',
        _home_ld_replacer(host, serp, kws, d),
        html,
        count=1,
        flags=re.I,
    )
    if MARKER.split("=")[0] not in html:
        html = inject_jsonld(
            html,
            website_ld(
                url=f"https://{host}/",
                name=serp,
                lang=d["lang"],
                brand=A,
                host=host,
                keywords=kws,
            ),
        )
        html = html.replace("<body", f"<body {MARKER}", 1)
    html = odskin.rebuild_home(html, host, d)
    path.write_text(html, encoding="utf-8")
    return path


def _inner_ld_replacer(page_url: str, name: str, kws: list[str], desc: str):
    def repl(m: re.Match) -> str:
        raw = m.group(1).strip()
        try:
            data = json.loads(raw)
        except json.JSONDecodeError:
            return m.group(0)
        if isinstance(data, dict) and data.get("@type") == "WebPage":
            data["@id"] = page_url
            data["url"] = page_url
            data["name"] = name
            data["description"] = desc[:220]
            data["keywords"] = kws
        return f'<script type="application/ld+json">{json.dumps(data, ensure_ascii=False)}</script>'

    return repl


def deepen_inner(host: str, kind: str, d: dict) -> Path | None:
    slug = d["pages"].get(kind)
    if not slug or kind in d.get("skip", set()):
        return None
    path = overlay(host) / slug / "index.html"
    if not path.is_file():
        print("MISSING", host, slug)
        return None
    html = path.read_text(encoding="utf-8")
    inner = render_article(host, kind, d)
    html = swap_main(html, inner)
    h1, lead, secs = sections_for(kind, d, host)
    serp = inner_serp_title(kind, d)
    kws = inner_keywords(kind, d)
    page_url = f"https://{host}/{slug}/"
    html = re.sub(r"<title>[\s\S]*?</title>", f"<title>{escape(serp)}</title>", html, flags=re.I)
    html = re.sub(
        r'(<meta\s+property="og:title"\s+content=")[^"]*(")',
        rf"\1{escape(serp)}\2",
        html,
        count=1,
        flags=re.I,
    )
    html = re.sub(
        r'(<meta\s+property="og:url"\s+content=")[^"]*(")',
        rf"\1{page_url}\2",
        html,
        count=1,
        flags=re.I,
    )
    html = re.sub(
        r'(<link\s+rel="canonical"\s+href=")[^"]*(")',
        rf"\1{page_url}\2",
        html,
        count=1,
        flags=re.I,
    )
    html = re.sub(
        r'<script type="application/ld\+json">([\s\S]*?)</script>',
        _inner_ld_replacer(page_url, serp, kws, lead),
        html,
        count=1,
        flags=re.I,
    )
    html = upsert_meta(html, "keywords", ", ".join(kws))
    html = upsert_meta(html, "description", lead[:220])
    html = re.sub(
        r'(<meta\s+property="og:description"\s+content=")[^"]*(")',
        rf"\1{escape(lead[:220])}\2",
        html,
        count=1,
        flags=re.I,
    )
    html = patch_cluster_nav(html, d)
    if kind == "faq":
        pairs = [(h2, " ".join(paras)) for h2, paras in secs]
        block = faq_ld(d["lang"], pairs)
        dumped = json.dumps(block, ensure_ascii=False)
        if '"FAQPage"' in html:
            html = re.sub(
                r'<script type="application/ld\+json">\s*\{[^{}]*"@type"\s*:\s*"FAQPage"[\s\S]*?</script>',
                f'<script type="application/ld+json">{dumped}</script>',
                html,
                count=1,
            )
        else:
            html = inject_jsonld(html, block)
    path.write_text(html, encoding="utf-8")
    return path


def wrap_old_slug(host: str, d: dict, old: str, keep: str) -> Path | None:
    src = overlay(host) / keep / "index.html"
    if not src.is_file():
        src = overlay(host) / old / "index.html"
    if not src.is_file():
        return None
    dest_dir = overlay(host) / old
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest = dest_dir / "index.html"
    html = src.read_text(encoding="utf-8")
    h1, lead, secs = wrap_copy(host, d, keep)
    chunks = [
        f'<article class="cluster-page" {MARKER} data-kind="wrap">',
        f"<h1>{escape(h1)}</h1>",
        f'<p class="lead">{escape(lead)}</p>',
    ]
    for h2, paras in secs:
        chunks.append(f"<h2>{escape(h2)}</h2>")
        for p in paras:
            chunks.append(f"<p>{escape(p)}</p>")
    chunks.append(_nav(d))
    chunks.append("</article>\n")
    html = swap_main(html, "\n".join(chunks))
    keep_url = f"https://{host}/{keep}/"
    wrap_url = f"https://{host}/{old}/"
    html = re.sub(r"<title>[\s\S]*?</title>", f"<title>{escape(h1)}</title>", html, flags=re.I)
    html = re.sub(
        r'(<link\s+rel="canonical"\s+href=")[^"]*(")',
        rf"\1{keep_url}\2",
        html,
        count=1,
        flags=re.I,
    )
    html = re.sub(
        r'(<meta\s+property="og:url"\s+content=")[^"]*(")',
        rf"\1{wrap_url}\2",
        html,
        count=1,
        flags=re.I,
    )
    html = upsert_meta(html, "description", lead[:220])
    html = odskin.skin_chrome(html, host, d)
    dest.write_text(html, encoding="utf-8")
    print("WRAP", host, old, "->", keep)
    return dest


def bump_sitemap(host: str, d: dict) -> None:
    path = overlay(host) / "sitemap.xml"
    if not path.is_file():
        return
    sm = path.read_text(encoding="utf-8")
    locs = [f"https://{host}/"] + [f"https://{host}/{slug}/" for slug in d["pages"].values()]
    for old, keep in d.get("canon") or []:
        locs.append(f"https://{host}/{old}/")
        locs.append(f"https://{host}/{keep}/")
    for loc in locs:
        sm = re.sub(
            rf"(<loc>\s*{re.escape(loc)}\s*</loc>\s*<lastmod>)[^<]+",
            rf"\g<1>{TODAY}",
            sm,
        )
        if loc not in sm and "</urlset>" in sm:
            sm = sm.replace(
                "</urlset>",
                "  <url>\n"
                f"    <loc>{loc}</loc>\n"
                f"    <lastmod>{TODAY}</lastmod>\n"
                "    <changefreq>weekly</changefreq>\n"
                "    <priority>0.8</priority>\n"
                "  </url>\n</urlset>",
                1,
            )
    path.write_text(sm, encoding="utf-8")


def _unique_snapshot(host: str) -> dict[str, bytes]:
    out = {}
    for rel in (
        "mycnbox-coupons/index.html",
        "mycnbox-invite-code/index.html",
        "mycnbox-community/index.html",
        "mycnbox-shoes-spreadsheet/index.html",
        "mycnbox-qc-guide/index.html",
        "blog/posts/mycnbox-customs-guide/index.html",
    ):
        p = overlay(host) / rel
        if p.is_file():
            out[rel] = p.read_bytes()
    return out


def seed_keep_pages(host: str, d: dict) -> None:
    """Copy overlay HTML from a wrap slug onto a missing keep slug.

    Only seeds keep URLs that this run will deepen. Unique skipped CMS
    (FR avis-orientdig, ES spreadsheet) is never invented from a wrap.
    """
    page_slugs = set(d["pages"].values())
    skip_slugs = {d["pages"][k] for k in d.get("skip", set()) if k in d["pages"]}
    for old, keep in d.get("canon") or []:
        if keep not in page_slugs or keep in skip_slugs:
            continue
        keep_p = overlay(host) / keep / "index.html"
        old_p = overlay(host) / old / "index.html"
        if not keep_p.is_file() and old_p.is_file():
            keep_p.parent.mkdir(parents=True, exist_ok=True)
            keep_p.write_bytes(old_p.read_bytes())
            print("SEED", host, keep, "from", old)


def append_es_finds_buyer() -> Path | None:
    """Buyer-facing Spanish depth after unique Dataset CMS. Does not rewrite the article."""
    path = overlay("orientdig.es") / "finds-dataset" / "index.html"
    if not path.is_file():
        return None
    html = path.read_text(encoding="utf-8")
    section = """
<section id="es-finds-buyer" class="wrap" lang="es">
  <h2>Finds OrientDig para una puerta en España</h2>
  <p>El dataset de arriba cuenta filas y categorías. Esta sección explica el camino de compra hacia una dirección española: fotos de almacén en China, luego flete. No es Excel ni caja. Los pedidos siguen en <a href="https://orientdig.com/">orientdig.com</a>.</p>
  <p>La etiqueta quiere calle española y código postal de cinco dígitos. Un code postal francés o un CAP italiano es el país equivocado, aunque la app esté en español. Canarias, Ceuta o Melilla pueden ser otro producto de transportista — elige la línea viva en el estimador, no copies la SKU de Madrid.</p>
  <h2>Cómo elegir un find</h2>
  <p>Un find útil tiene enlace de Taobao, 1688 o Weidian vivo, al menos una foto de almacén, y destino España en <a href="https://orientdig.com/estimation/">el estimador oficial</a>. Precio 0 o restricted es fuente muerta, no un descuento. Zapatillas, sudaderas, cazadoras y bolsos suelen tener ángulos QC; electrónica, perfume y líquidos se quedan fuera hasta que la app los permita el día del envío.</p>
  <p>Las claves del muro (sneakers, hoodie, jacket) están en inglés porque el índice está en inglés. Buscar «zapatillas» suele devolver cero fichas. Eso no convierte el paquete en un envío US. El país del estimador sigue siendo España. Pagas en euros de visualización aquí; la caja real está en orientdig.com.</p>
  <h2>QC, Correos y Agencia Tributaria</h2>
  <p>Las fotos QC se hacen en China. Extra ángulos se piden en la app mientras la SKU está en almacén. Cuando Correos ya tiene el cartón, la Agencia Tributaria no reabre un ticket de almacén. Tras aceptar el QC, reserva la línea internacional. Última milla a menudo Correos.</p>
  <p>Hay dos pagos: mercancía a China, luego flete. Los días de almacén están en la Help oficial. Quién paga aranceles, IVA de importación y Collect lo decide la SKU reservada. Fuente el día del envío: <a href="https://sede.agenciatributaria.gob.es/">Agencia Tributaria</a>. Esta página no inventa un tipo ni un valor declarado.</p>
  <h2>Primera compra y consolidación</h2>
  <p>Para la primera puerta en España basta una SKU de ropa con fotos. Consolidar varias piezas sin QC en la primera factura mezcla aduana y Collect. Restricted se queda fuera aunque un foro lo nombre.</p>
  <p>Fail-QC se resuelve en la app mientras la pieza está en China. Correos no rehace la foto de almacén a cartón ya en España. Si la app cobra una sola vez, vale la app — dos recibos (mercancía, luego flete) son el caso habitual.</p>
  <h2>Qué no es este hostname</h2>
  <p>orientdig.es es índice y guía hacia una puerta en España. No cobra tarjeta, no es atención de Correos y no sustituye el estimador. Registro y tickets solo en orientdig.com.</p>
  <p>Un artículo de aduana que rankea aquí no es un arancel vivo: los umbrales cambian. Confirma destino España en el estimador y lee la Agencia Tributaria la mañana que envías. El JSON de arriba sigue siendo la prueba de filas; esta sección es la guía de comprador en español.</p>
</section>
"""
    if 'id="es-finds-buyer"' in html:
        html = re.sub(
            r'\n?<section id="es-finds-buyer"[\s\S]*?</section>\n?',
            "\n" + section + "\n",
            html,
            count=1,
        )
        print("ES_FINDS_BUYER replaced")
    elif "</article>" in html:
        html = html.replace("</article>", "</article>\n" + section, 1)
        print("ES_FINDS_BUYER appended")
    else:
        html = html.replace("</body>", section + "\n</body>", 1)
        print("ES_FINDS_BUYER appended")
    path.write_text(html, encoding="utf-8")
    return path


def generate() -> list[Path]:
    written: list[Path] = []
    for host in ORDER:
        d = HOSTS[host]
        snap = _unique_snapshot(host)
        seed_keep_pages(host, d)
        written.extend(odskin.install_media(host))
        written.append(patch_home(host, d))
        print("HOME", host, cluster_title_serp(A, d["dest"], d["loc"], d["label"]))
        for kind in d["pages"]:
            p = deepen_inner(host, kind, d)
            if p:
                written.append(p)
                print("INNER", host, kind, p.relative_to(ROOT))
        for old, keep in d.get("canon") or []:
            wrap = wrap_old_slug(host, d, old, keep)
            if wrap:
                written.append(wrap)
        odskin.skin_overlay_files(host, d, [p for p in written if str(p).startswith(str(overlay(host)))])
        bump_sitemap(host, d)
        sm = overlay(host) / "sitemap.xml"
        if sm.is_file():
            written.append(sm)
        for rel, blob in snap.items():
            now = overlay(host) / rel
            if now.is_file() and now.read_bytes() != blob:
                raise SystemExit(f"refused to smash unique {rel} on {host}")
        written.extend(write_api_overlay(host))
    return written


def write_api_overlay(host: str) -> list[Path]:
    """Same-host /api/products/ adapter → w2clinks.com typesense."""
    api_dir = overlay(host) / "api"
    prod_dir = api_dir / "products"
    prod_dir.mkdir(parents=True, exist_ok=True)
    upstream = api_dir / "products.php"
    index = prod_dir / "index.php"
    upstream.write_text(PRODUCTS_PHP, encoding="utf-8")
    index.write_text(PRODUCTS_INDEX, encoding="utf-8")
    print("API", host, "products.php + products/index.php")
    return [upstream, index]


def _w2c_api_key() -> str:
    for name in ("W2CLINKS_API_KEY", "W2C_PRODUCTS_API_KEY"):
        val = (os.environ.get(name) or "").strip()
        if val:
            return val
    for path in (
        Path("/cursor/stores/self/w2c-api-key"),
        Path("/tmp/hipobuy-creds/w2c-api-key"),
    ):
        if path.is_file():
            val = path.read_text(encoding="utf-8").strip()
            if val:
                return val
    return ""


def put_api_secrets(client) -> None:
    """Origin-only config.local.php — not written into git overlay."""
    key = _w2c_api_key()
    if not key:
        print("API_KEY_SKIP no key file")
        return
    body = (
        "<?php\ndeclare(strict_types=1);\n"
        "return ['api_key' => " + json.dumps(key) + "];\n"
    )
    sftp = client.open_sftp()
    n = 0
    for host in ORDER:
        remote = f"/www/wwwroot/{host}/api/config.local.php"
        _run(client, f"mkdir -p '/www/wwwroot/{host}/api'")
        bak = remote + ".bak"
        _run(client, f"test -f '{remote}' && cp -a '{remote}' '{bak}' || true")
        with sftp.open(remote, "w") as fh:
            fh.write(body)
        _run(client, f"chown www:www '{remote}' && chmod 640 '{remote}'")
        n += 1
    sftp.close()
    print("API_KEY_PUT", n, "hosts")


def fix_api_nginx(client) -> None:
    """Route /api/products/ to PHP the way kakobuy dests do."""
    old = """    location /api/ {
        try_files $uri =404;
        add_header X-Robots-Tag "noindex, nofollow" always;
    }
"""
    new = """    location /api/ {
        rewrite ^/api/([^/]+)/?$ /api/$1/index.php last;
        add_header X-Robots-Tag "noindex, nofollow" always;
    }
"""
    changed = 0
    sftp = client.open_sftp()
    stamp = time.strftime("%Y%m%d-%H%M%S")
    bak_root = f"/www/backup/mycnbox-api-nginx-{stamp}"
    _run(client, f"mkdir -p '{bak_root}'")
    for host in ORDER:
        path = f"/www/server/panel/vhost/nginx/{host}.conf"
        raw = _run(client, f"cat '{path}'")
        if "rewrite ^/api/([^/]+)/?$ /api/$1/index.php last" in raw:
            print("ok", host, "api rewrite")
            continue
        if old not in raw:
            print("skip", host, "api block mismatch")
            continue
        _run(client, f"cp -a '{path}' '{bak_root}/{host}.conf'")
        with sftp.open(path, "w") as fh:
            fh.write(raw.replace(old, new, 1))
        print("PATCH", path)
        changed += 1
    sftp.close()
    if changed:
        print(_run(client, "nginx -t && nginx -s reload"))
    print("NGINX_API", changed)


def put(files: list[Path] | None = None) -> None:
    if files is None:
        files = generate()
    client = _connect()
    stamp = time.strftime("%Y%m%d-%H%M%S")
    bak = f"/www/backup/mycnbox-dest-{stamp}"
    print(_run(client, f"mkdir -p '{bak}'"))
    sftp = client.open_sftp()
    n = 0
    for path in files:
        rel = path.relative_to(ROOT / "sites").as_posix()
        host = rel.split("/", 1)[0]
        rest = path.relative_to(overlay(host)).as_posix()
        remote = f"/www/wwwroot/{host}/{rest}"
        _run(client, f"mkdir -p '{str(Path(remote).parent)}'")
        _run(
            client,
            f"test -f '{remote}' && mkdir -p '{bak}/{host}' && cp -a '{remote}' '{bak}/{host}/{rest.replace('/', '_')}' || true",
        )
        if any(part in UNIQUE_PUT for part in Path(rest).parts):
            print("PUT_SKIP unique", host, rest)
            continue
        sftp.put(str(path), remote)
        _run(client, f"chown www:www '{remote}'")
        n += 1
        print("PUT", remote)
    sftp.close()
    put_api_secrets(client)
    fix_api_nginx(client)
    client.close()
    print("PUT_DONE", n, "backup", bak)


def verify() -> None:
    from urllib.error import HTTPError
    from urllib.request import HTTPRedirectHandler, HTTPSHandler, Request, build_opener

    class NoRedir(HTTPRedirectHandler):
        def redirect_request(self, *a, **k):
            return None

    opener = build_opener(NoRedir(), HTTPSHandler())
    checks = [
        ("https://mycnbox.co.uk/", "MyCNBox Spreadsheet for UK Buyers"),
        ("https://mycnbox.co.uk/", 'action="https://w2clinks.com/spreadsheet/"'),
        ("https://mycnbox.de/", "Beste Finds"),
        ("https://mycnbox.de/mycnbox-spreadsheet/", "Packstation"),
        ("https://mycnbox.de/mycnbox-faq/", "Einfuhrumsatzsteuer"),
        ("https://mycnbox.es/", "Mejores finds y QC"),
        ("https://mycnbox.es/", 'action="https://w2clinks.com/spreadsheet/"'),
        ("https://mycnbox.es/mycnbox-faq/", "Canarias, Ceuta o Melilla"),
        ("https://mycnbox.es/mycnbox-invite-code/", "Código"),
        ("https://mycnbox.fr/", "Meilleurs finds et QC"),
        ("https://mycnbox.fr/mycnbox-community/", "Commun"),
        ("https://mycnbox.nl/", "Beste finds en QC"),
        ("https://mycnbox.nl/mycnbox-spreadsheet/", "1234 AB"),
        ("https://mycnbox.nl/mycnbox-shoes-spreadsheet/", "Shoes"),
        ("https://mycnbox.pl/", "Finds i QC"),
        ("https://mycnbox.pl/mycnbox-spreadsheet/", "00-001"),
        ("https://mycnbox.pl/mycnbox-qc-guide/", "QC"),
        ("https://mycnbox.co.uk/mycnbox-coupons/", "Coupon"),
        ("https://mycnbox.eu/", "Independent Index"),
    ]
    for url, needle in checks:
        req = Request(url, headers={"User-Agent": "mycnbox-dest/1.0"})
        try:
            with opener.open(req, timeout=22) as resp:
                raw = resp.read().decode("utf-8", "replace")
                ok = True if needle is None else needle in raw
                print("VERIFY", resp.status, url, "OK" if ok else "MISS " + (needle or ""))
                if needle is None:
                    print("VERIFY_UNEXP_200", url)
        except HTTPError as exc:
            loc = exc.headers.get("Location") if exc.headers else ""
            print("VERIFY", exc.code, url, loc)
        except Exception as exc:  # noqa: BLE001
            print("VERIFY_ERR", url, type(exc).__name__, str(exc)[:120])
    verify_api()


def verify_api() -> None:
    from urllib.request import Request, urlopen

    for host in ORDER:
        for path, needle_q in (
            (f"https://{host}/api/products/?limit=2&page=1", None),
            (f"https://{host}/api/products/?q=sneakers&limit=2&page=1", "sneakers"),
        ):
            req = Request(
                path,
                headers={
                    "User-Agent": "Mozilla/5.0 (compatible; MyCNBoxDestVerify/1.0)",
                    "Accept": "application/json",
                },
            )
            try:
                with urlopen(req, timeout=22) as resp:
                    raw = resp.read().decode("utf-8", "replace")
                    data = json.loads(raw)
                    items = data.get("items") or data.get("products") or []
                    hrefs = [str(it.get("href") or it.get("target") or "") for it in items if isinstance(it, dict)]
                    w2c = sum(1 for h in hrefs if h.startswith("https://w2clinks.com/"))
                    print(
                        "VERIFY_API",
                        resp.status,
                        host,
                        "q=" + (needle_q or "-"),
                        "n=" + str(len(items)),
                        "w2c=" + str(w2c),
                        "found=" + str(data.get("found", "")),
                    )
                    if resp.status != 200 or not items or w2c == 0:
                        print("VERIFY_API_FAIL", host, path.split("?")[0])
            except Exception as exc:  # noqa: BLE001
                print("VERIFY_API_ERR", host, type(exc).__name__, str(exc)[:120])


def wire_api() -> list[Path]:
    """Homepage + /api/products/ only. Does not deepen inner CMS."""
    written: list[Path] = []
    for host in ORDER:
        snap = _unique_snapshot(host)
        written.append(patch_home(host, HOSTS[host]))
        written.extend(write_api_overlay(host))
        for rel, blob in snap.items():
            now = overlay(host) / rel
            if now.is_file() and now.read_bytes() != blob:
                raise SystemExit(f"refused to smash unique {rel} on {host}")
        print("WIRE", host)
    return written


def gsc_submit() -> None:
    if not Path(SA).is_file():
        print("GSC_SKIP no sa.json")
        return
    try:
        from google.oauth2 import service_account
        from googleapiclient.discovery import build
    except ImportError:
        import subprocess

        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "google-api-python-client", "google-auth", "-q"]
        )
        from google.oauth2 import service_account
        from googleapiclient.discovery import build

    creds = service_account.Credentials.from_service_account_file(
        SA, scopes=["https://www.googleapis.com/auth/webmasters"]
    )
    gsc = build("searchconsole", "v1", credentials=creds, cache_discovery=False)
    listed = {row["siteUrl"] for row in gsc.sites().list().execute().get("siteEntry", [])}
    for host in ORDER:
        site = f"sc-domain:{host}" if f"sc-domain:{host}" in listed else f"https://{host}/"
        feed = f"https://{host}/sitemap.xml"
        try:
            gsc.sitemaps().submit(siteUrl=site if site in listed else f"https://{host}/", feedpath=feed).execute()
            print("SITEMAP", host, site)
        except Exception as exc:  # noqa: BLE001
            print("SITEMAP_FAIL", host, type(exc).__name__, str(exc)[:180])
        time.sleep(0.35)


def main() -> None:
    cmd = sys.argv[1] if len(sys.argv) > 1 else "all"
    if cmd == "reclaim":
        reclaim_nginx()
    elif cmd == "generate":
        generate()
    elif cmd == "put":
        put()
    elif cmd == "verify":
        verify()
    elif cmd == "api":
        files = wire_api()
        put(files)
        verify()
    elif cmd == "gsc":
        gsc_submit()
    elif cmd == "all":
        files = generate()
        put(files)
        verify()
        gsc_submit()
    else:
        raise SystemExit(f"unknown {cmd}")


if __name__ == "__main__":
    main()
