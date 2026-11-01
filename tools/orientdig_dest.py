#!/usr/bin/env python3
"""Deepen OrientDig dest desks to UK-cluster inner depth.

Independent country hosts (AT/ES/FR/US/DE/IT/NL/UK). Reclaims IT/NL from
Phase B/C 301 to orientdig.es. Does not revive same-country twins.
Does not smash unique ES CMS or FR avis/freight. No declared-value coaching.
GSC: sitemap submit only.
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
    base = cluster_title(agent, dest, loc, dest_label)
    suffix = {
        "de": " – Beste Finds & QC",
        "es": " – Mejores finds y QC",
        "fr": " – Meilleurs finds et QC",
        "it": " – Migliori finds e QC",
        "nl": " – Beste finds en QC",
        "fi": " – Finds ja QC",
    }.get(loc, " – Best Finds & QC")
    return base + suffix
from orientdig_dest_copy import inner_h1, inner_keywords, inner_serp_title, sections_for, wrap_copy

ROOT = Path(__file__).resolve().parents[1]
STAMP = "20261101"
TODAY = "2026-11-01"
MARKER = f'data-orientdig-dest="{STAMP}"'
_SA_CANDIDATES = [
    os.environ.get("GSC_SA_JSON", ""),
    "/tmp/hipobuy-creds/sa.json",
    "/cursor/stores/self/internal/gsc-sa.json",
]
SA = next((p for p in _SA_CANDIDATES if p and Path(p).is_file()), "/tmp/hipobuy-creds/sa.json")
BAK_NL = "/www/backup/portfolio-step5-phaseb-20261026-150339"
BAK_IT = "/www/backup/portfolio-step5-phasec-20261026-151213"
OFFICIAL = "https://orientdig.com/"
EST = "https://orientdig.com/estimation/"
A = "OrientDig"

HOSTS = {
    "orientdig.at": {
        "key": "at",
        "dest": "AT",
        "loc": "de",
        "lang": "de-AT",
        "label": "Österreich",
        "ccy": "EUR",
        "customs": "BMF Zoll",
        "customs_url": "https://www.bmf.gv.at/themen/zoll.html",
        "post": "Österreichische Post",
        "city": "1010 Wien",
        "pages": {
            "spreadsheet": "orientdig-spreadsheet",
            "finds": "orientdig-finds",
            "qc": "orientdig-qc",
            "shipping": "orientdig-shipping",
            "legal": "is-orientdig-legit",
            "guide": "how-to-use-orientdig",
            "faq": "orientdig-faq",
        },
        "skip": set(),
        "canon": [],
        "nav_extra": [],
    },
    "orientdig.es": {
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
            "spreadsheet": "orientdig-spreadsheet",
            "finds": "finds-dataset",
            "qc": "orientdig-qc",
            "shipping": "orientdig-shipping-to-espana",
            "legal": "is-orientdig-legit",
            "guide": "como-comprar-en-orientdig",
            "faq": "orientdig-faq",
        },
        "skip": {"spreadsheet", "finds", "guide"},
        "canon": [],
        "nav_extra": [],
    },
    "orientdig.fr": {
        "key": "fr",
        "dest": "FR",
        "loc": "fr",
        "lang": "fr-FR",
        "label": "France",
        "ccy": "EUR",
        "customs": "douane.gouv.fr",
        "customs_url": "https://www.douane.gouv.fr/",
        "post": "Colissimo",
        "city": "code postal à cinq chiffres, pas un code belge",
        "pages": {
            "spreadsheet": "orientdig-spreadsheet",
            "finds": "orientdig-finds",
            "qc": "orientdig-qc",
            "shipping": "orientdig-shipping",
            "legal": "avis-orientdig",
            "guide": "how-to-use-orientdig",
            "faq": "orientdig-faq",
        },
        "skip": {"legal"},
        "canon": [("is-orientdig-legit", "avis-orientdig")],
        "nav_extra": [],
    },
    "orientdig.us": {
        "key": "us",
        "dest": "US",
        "loc": "en",
        "lang": "en-US",
        "label": "the United States",
        "ccy": "USD",
        "customs": "CBP",
        "customs_url": "https://www.cbp.gov/",
        "post": "USPS",
        "city": "US ZIP",
        "pages": {
            "spreadsheet": "orientdig-spreadsheet",
            "finds": "orientdig-finds",
            "qc": "orientdig-qc",
            "shipping": "orientdig-shipping",
            "legal": "is-orientdig-legit",
            "guide": "how-to-use-orientdig",
            "faq": "orientdig-faq",
        },
        "skip": set(),
        "canon": [],
        "nav_extra": [],
    },
    "orientdigspreadsheet.de": {
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
            "spreadsheet": "orientdig-spreadsheets",
            "finds": "orientdig-finds",
            "qc": "orientdig-qc",
            "shipping": "orientdig-shipping",
            "legal": "is-orientdig-legit",
            "guide": "how-to-use-orientdig",
            "faq": "orientdig-faq",
        },
        "skip": set(),
        "canon": [("orientdig-spreadsheet", "orientdig-spreadsheets")],
        "nav_extra": [],
    },
    "orientdigspreadsheet.it": {
        "key": "it",
        "dest": "IT",
        "loc": "it",
        "lang": "it-IT",
        "label": "Italia",
        "ccy": "EUR",
        "customs": "Agenzia delle Dogane e dei Monopoli",
        "customs_url": "https://www.adm.gov.it/portale/",
        "post": "Poste Italiane",
        "city": "CAP a cinque cifre",
        "pages": {
            "spreadsheet": "orientdig-spreadsheets",
            "finds": "orientdig-finds",
            "qc": "orientdig-qc",
            "shipping": "orientdig-shipping",
            "legal": "is-orientdig-legit",
            "guide": "how-to-use-orientdig",
            "faq": "orientdig-faq",
        },
        "skip": set(),
        "canon": [],
        "nav_extra": [],
    },
    "orientdigspreadsheet.nl": {
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
            "spreadsheet": "orientdig-spreadsheets",
            "finds": "orientdig-finds",
            "qc": "orientdig-qc",
            "shipping": "orientdig-shipping",
            "legal": "is-orientdig-legit",
            "guide": "how-to-use-orientdig",
            "faq": "orientdig-faq",
        },
        "skip": set(),
        "canon": [],
        "nav_extra": [],
    },
    "orientdigspreadsheet.uk": {
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
            "spreadsheet": "orientdig-spreadsheets",
            "finds": "orientdig-finds",
            "qc": "orientdig-qc",
            "shipping": "orientdig-shipping",
            "legal": "is-orientdig-legit",
            "guide": "how-to-use-orientdig",
            "faq": "orientdig-faq",
        },
        "skip": set(),
        "canon": [],
        "nav_extra": [],
    },
}

ORDER = [
    "orientdig.at",
    "orientdig.es",
    "orientdig.fr",
    "orientdig.us",
    "orientdigspreadsheet.de",
    "orientdigspreadsheet.it",
    "orientdigspreadsheet.nl",
    "orientdigspreadsheet.uk",
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
}

H2NAV = {
    "de": "Spreadsheet / Finds / QC / Versand",
    "es": "Spreadsheet / finds / QC / Envío",
    "fr": "Spreadsheet / finds / QC / Livraison",
    "it": "Spreadsheet / finds / QC / Spedizione",
    "nl": "Spreadsheet / finds / QC / Verzending",
    "en": "Spreadsheet / finds / QC / Shipping",
}

CTA = {
    "de": "Bestellen und zahlen auf orientdig.com. Anzeige auf dieser Seite in lokaler Währung.",
    "es": "Pide y paga en orientdig.com. Los precios de esta página se muestran en moneda local.",
    "fr": "Commande et paiement sur orientdig.com. Les prix de cette page sont affichés en monnaie locale.",
    "it": "Ordina e paga su orientdig.com. I prezzi di questa pagina sono in valuta locale.",
    "nl": "Bestellen en betalen op orientdig.com. Prijzen op deze pagina staan in lokale valuta.",
    "en": "Shop and pay on orientdig.com. Prices on this page are shown in local currency.",
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
    """Restore dest vhosts for IT/NL (undo Phase B/C catch-all 301 to orientdig.es)."""
    client = _connect()
    stamp = time.strftime("%Y%m%d-%H%M%S")
    bak = f"/www/backup/orientdig-dest-reclaim-{stamp}"
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
    chunks = [
        f'<article class="cluster-page" data-spreadsheet-cluster="20261030" {MARKER} data-kind="{escape(kind)}">',
        f"<h1>{escape(h1)}</h1>",
        f'<p class="lead">{escape(lead)}</p>',
    ]
    for h2, paras in secs:
        chunks.append(f"<h2>{escape(h2)}</h2>")
        for p in paras:
            chunks.append(f"<p>{escape(p)}</p>")
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
        f'<nav class="cluster-nav" data-spreadsheet-cluster="20261030" aria-label="OrientDig">{inner}</nav>',
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
    # Keep H1 unsuffixed (kakobuy.co.uk pattern): strip a trailing " (2026)" only if SERP suffix leaked.
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
        "como-comprar-en-orientdig/index.html",
        "finds-dataset/index.html",
        "orientdig-coupons/index.html",
        "orientdig-shipping-coupons/index.html",
        "avis-orientdig/index.html",
        "avis-orientdig/live-base.index.html",
        "orientdig-freight/index.html",
        "orientdig-freight/live-base.index.html",
    ):
        p = overlay(host) / rel
        if p.is_file():
            out[rel] = p.read_bytes()
    # ES unique spreadsheet body must survive skip
    if host == "orientdig.es":
        p = overlay(host) / "orientdig-spreadsheet" / "index.html"
        if p.is_file():
            out["orientdig-spreadsheet/index.html"] = p.read_bytes()
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


def generate() -> list[Path]:
    written: list[Path] = []
    for host in ORDER:
        d = HOSTS[host]
        snap = _unique_snapshot(host)
        seed_keep_pages(host, d)
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
        bump_sitemap(host, d)
        sm = overlay(host) / "sitemap.xml"
        if sm.is_file():
            written.append(sm)
        for rel, blob in snap.items():
            now = overlay(host) / rel
            if now.is_file() and now.read_bytes() != blob:
                raise SystemExit(f"refused to smash unique {rel} on {host}")
    return written


def put(files: list[Path] | None = None) -> None:
    if files is None:
        files = generate()
    client = _connect()
    stamp = time.strftime("%Y%m%d-%H%M%S")
    bak = f"/www/backup/orientdig-dest-{stamp}"
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
        sftp.put(str(path), remote)
        _run(client, f"chown www:www '{remote}'")
        n += 1
        print("PUT", remote)
    sftp.close()
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
        ("https://orientdigspreadsheet.it/", "OrientDig Spreadsheet per acquirenti in Italia"),
        ("https://orientdigspreadsheet.nl/", "OrientDig Spreadsheet voor kopers in Nederland"),
        ("https://orientdig.at/", "Finds"),
        ("https://orientdig.es/", "Mejores finds y QC"),
        ("https://orientdig.fr/", "Meilleurs finds et QC"),
        ("https://orientdig.us/", "Best Finds"),
        ("https://orientdigspreadsheet.de/", "Beste Finds"),
        ("https://orientdigspreadsheet.uk/", "Best Finds"),
        ("https://orientdig.at/orientdig-spreadsheet/", "1010 Wien"),
        ("https://orientdigspreadsheet.de/orientdig-spreadsheets/", "Packstation"),
        ("https://orientdigspreadsheet.de/orientdig-spreadsheet/", None),  # GSC 301 → plural keep
        ("https://orientdig.es/como-comprar-en-orientdig/", "Guía OrientDig para España"),
        ("https://orientdig.es/orientdig-spreadsheet/", "compradores en España"),
        ("https://orientdig.fr/avis-orientdig/", "Avis OrientDig"),
        ("https://orientdig.fr/is-orientdig-legit/", "avis-orientdig"),
        ("https://orientdigspreadsheet.nl/orientdig-shipping/", "Nederlandse postcode"),
        ("https://orientdigspreadsheet.it/how-to-use-orientdig/", "Poste Italiane"),
        ("https://orientdigspreadsheet.uk/orientdig-spreadsheets/", "Northern Ireland"),
        ("https://orientdig.us/orientdig-shipping/", "USPS"),
        ("https://orientdigspreadsheet.fr/", None),  # twin must stay 301
        ("https://orientdigspreadsheet.us/", None),
    ]
    for url, needle in checks:
        req = Request(url, headers={"User-Agent": "orientdig-dest/1.0"})
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
    elif cmd == "gsc":
        gsc_submit()
    elif cmd == "all":
        reclaim_nginx()
        files = generate()
        put(files)
        verify()
        gsc_submit()
    else:
        raise SystemExit(f"unknown {cmd}")


if __name__ == "__main__":
    main()
