#!/usr/bin/env python3
"""Deepen BBDBuy dest desks to UK-cluster inner depth.

Independent country hosts (UK/US/CA/IT/DE/FR). Does not touch bbdbuyeu.net or
bbdbuyeuspreadsheet.com hubs. Does not smash unique coupons/telegram/contact.
No declared-value coaching. GSC: sitemap submit only.
"""
from __future__ import annotations

import json
import os
import re
import shutil
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
from bbdbuy_dest_copy import inner_h1, inner_keywords, inner_serp_title, sections_for, wrap_copy
import bbdbuy_dest_skin as odskin

ROOT = Path(__file__).resolve().parents[1]
STAMP = "20261102"
TODAY = "2026-11-02"
MARKER = f'data-bbdbuy-dest="{STAMP}"'
_SA_CANDIDATES = [
    os.environ.get("GSC_SA_JSON", ""),
    "/tmp/hipobuy-creds/sa.json",
    "/cursor/stores/self/internal/gsc-sa.json",
]
SA = next((p for p in _SA_CANDIDATES if p and Path(p).is_file()), "/tmp/hipobuy-creds/sa.json")
BAK_DE = "/www/backup/portfolio-step5-phaseb-20261026-150339"
BAK_NL = BAK_DE
BAK_IT = "/www/backup/portfolio-step5-phasec-20261026-151213"
OFFICIAL = "https://www.bbdbuy.com/"
EST = "https://www.bbdbuy.com/estimation"
A = "BBDBuy"
W2C_SHEET = "https://w2clinks.com/spreadsheet/bbdbuy/"
PRODUCTS_PHP = (ROOT / "templates" / "api" / "products_w2c.php").read_text(encoding="utf-8")
PRODUCTS_INDEX = (ROOT / "templates" / "api" / "products_index.php").read_text(encoding="utf-8")



HOSTS = {
    "bbdbuy.uk": {
        "key": "uk",
        "dest": "GB",
        "loc": "en",
        "lang": "en-GB",
        "label": "the United Kingdom",
        "ccy": "GBP",
        "customs": "HMRC",
        "customs_url": "https://www.gov.uk/goods-sent-from-abroad",
        "post": "Royal Mail",
        "city": "UK postcode",
        "pages": {
            "spreadsheet": "bbdbuy-spreadsheet",
            "finds": "bbdbuy-finds",
            "qc": "bbdbuy-qc",
            "shipping": "bbdbuy-shipping",
            "legal": "is-bbdbuy-legit",
            "guide": "how-to-use-bbdbuy",
            "faq": "bbdbuy-faq",
        },
        "skip": set(),
        "canon": [],
        "nav_extra": [],
    },
    "bbdbuy.us": {
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
            "spreadsheet": "bbdbuy-spreadsheet",
            "finds": "bbdbuy-finds",
            "qc": "bbdbuy-qc",
            "shipping": "bbdbuy-shipping",
            "legal": "is-bbdbuy-legal-us",
            "guide": "how-to-use-bbdbuy",
            "faq": "bbdbuy-faq",
        },
        "skip": set(),
        "canon": [],
        "nav_extra": [],
    },
    "bbdbuy.ca": {
        "key": "ca",
        "dest": "CA",
        "loc": "en",
        "lang": "en-CA",
        "label": "Canada",
        "ccy": "CAD",
        "customs": "CBSA",
        "customs_url": "https://www.cbsa-asfc.gc.ca/",
        "post": "Canada Post",
        "city": "Canadian postal code A1A 1A1",
        "pages": {
            "spreadsheet": "bbdbuy-spreadsheet",
            "finds": "bbdbuy-finds",
            "qc": "bbdbuy-qc",
            "shipping": "bbdbuy-shipping",
            "legal": "is-bbdbuy-legit",
            "guide": "bbdbuy-guide",
            "faq": "bbdbuy-faq",
        },
        "skip": set(),
        "canon": [],
        "nav_extra": [],
    },
    "bbdbuy.it": {
        "key": "it",
        "dest": "IT",
        "loc": "it",
        "lang": "it-IT",
        "label": "l’Italia",
        "ccy": "EUR",
        "customs": "ADM",
        "customs_url": "https://www.adm.gov.it/",
        "post": "Poste Italiane",
        "city": "CAP italiano di cinque cifre",
        "pages": {
            "spreadsheet": "bbdbuy-spreadsheet",
            "finds": "bbdbuy-finds",
            "qc": "bbdbuy-qc",
            "shipping": "bbdbuy-shipping",
            "legal": "is-bbdbuy-legit",
            "guide": "how-to-use-bbdbuy",
            "faq": "bbdbuy-faq",
        },
        "skip": set(),
        "canon": [],
        "nav_extra": [],
    },
    "bbdbuyspreadsheet.de": {
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
            "spreadsheet": "bbdbuy-spreadsheet",
            "finds": "bbdbuy-finds",
            "qc": "bbdbuy-qc",
            "shipping": "bbdbuy-shipping",
            "legal": "ist-bbdbuy-serioes",
            "guide": "how-to-use-bbdbuy",
            "faq": "bbdbuy-faq",
        },
        "skip": set(),
        "canon": [("is-bbdbuy-legit", "ist-bbdbuy-serioes")],
        "nav_extra": [],
    },
    "bbdbuy.fr": {
        "key": "fr",
        "dest": "FR",
        "loc": "fr",
        "lang": "fr-FR",
        "label": "la France",
        "ccy": "EUR",
        "customs": "douane.gouv.fr",
        "customs_url": "https://www.douane.gouv.fr/",
        "post": "Colissimo / La Poste",
        "city": "code postal français à cinq chiffres",
        "pages": {
            "spreadsheet": "bbdbuy-spreadsheet",
            "finds": "bbdbuy-finds",
            "qc": "bbdbuy-qc",
            "shipping": "bbdbuy-shipping",
            "legal": "is-bbdbuy-legit",
            "guide": "how-to-use-bbdbuy",
            "faq": "bbdbuy-faq",
        },
        "skip": set(),
        "canon": [],
        "nav_extra": [],
    },
}

ORDER = [
    "bbdbuy.uk",
    "bbdbuy.us",
    "bbdbuy.ca",
    "bbdbuy.it",
    "bbdbuyspreadsheet.de",
    "bbdbuy.fr",
]

# Unique country-desk leftover pages: official chrome only, keep ranked body.
LEFTOVER_SKIN = {
    "bbdbuy.uk": ["start", "catalog", "about", "help", "news"],
    "bbdbuy.us": ["start", "catalog", "about", "help", "news"],
    "bbdbuy.ca": ["start", "catalog", "about", "help", "news"],
    "bbdbuy.it": ["start", "catalogo", "chi-siamo", "aiuto", "notizie"],
    "bbdbuyspreadsheet.de": ["start", "katalog", "ueber-uns", "hilfe", "neuigkeiten"],
    "bbdbuy.fr": [],
}


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
    "de": "Bestellen und zahlen auf www.bbdbuy.com. Anzeige auf dieser Seite in lokaler Währung.",
    "es": "Pide y paga en www.bbdbuy.com. Los precios de esta página se muestran en moneda local.",
    "fr": "Commande et paiement sur www.bbdbuy.com. Les prix de cette page sont affichés en monnaie locale.",
    "it": "Ordina e paga su www.bbdbuy.com. I prezzi di questa pagina sono in valuta locale.",
    "nl": "Bestellen en betalen op www.bbdbuy.com. Prijzen op deze pagina staan in lokale valuta.",
    "en": "Shop and pay on www.bbdbuy.com. Prices on this page are shown in local currency.",
    "pl": "Zamawiaj i płać na www.bbdbuy.com. Ceny na tej stronie są w walucie lokalnej.",
}


UNIQUE_PUT = {
    "bbdbuy-coupons",
    "bbdbuy-coupon",
    "bbdbuy-telegram",
    "contact",
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
    """Restore dest vhost for DE (undo Phase B catch-all 301 to bbdbuyeu.net)."""
    client = _connect()
    stamp = time.strftime("%Y%m%d-%H%M%S")
    bak = f"/www/backup/bbdbuy-dest-reclaim-{stamp}"
    print(_run(client, f"mkdir -p '{bak}'"))
    host = "bbdbuyspreadsheet.de"
    live = f"/www/server/panel/vhost/nginx/{host}.conf"
    src_bak = f"{BAK_NL}/{host}.conf.bak"
    head = _run(client, f"head -c 1200 '{live}'")
    sunset = "bbdbuyeu.net" in head and "return 301" in head
    if not sunset:
        print("SKIP_RESTORE", host, "already dest vhost")
        client.close()
        print("RECLAIM_NGINX skip")
        return
    print(_run(client, f"cp -a '{live}' '{bak}/{host}.conf.before'"))
    print(_run(client, f"cp -a '{src_bak}' '{live}'"))
    print("RESTORE", host)
    print(_run(client, "nginx -t && nginx -s reload"))
    client.close()
    print("RECLAIM_NGINX", bak)
    return


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


def ensure_cluster_shell(host: str, path: Path) -> str:
    """Georgia QC stubs have no <main>. Borrow the cluster spreadsheet shell."""
    html = path.read_text(encoding="utf-8")
    if MAIN_RE.search(html):
        return html
    for kind in ("spreadsheet", "finds", "faq", "shipping"):
        slug = HOSTS[host]["pages"].get(kind)
        if not slug:
            continue
        src = overlay(host) / slug / "index.html"
        if src.is_file() and src != path:
            shell = src.read_text(encoding="utf-8")
            if MAIN_RE.search(shell):
                print("SHELL", host, path.parent.name, "from", slug)
                return shell
    raise ValueError(f"missing <main> and no cluster shell on {host} {path}")


def upsert_meta(html: str, name: str, content: str) -> str:
    tag = f'<meta name="{name}" content="{escape(content)}">'
    if re.search(rf'<meta\s+name="{name}"', html, re.I):
        return re.sub(rf'<meta\s+name="{name}"[^>]*>', tag, html, count=1, flags=re.I)
    return html.replace("</head>", tag + "\n</head>", 1)


def patch_cluster_nav(html: str, d: dict) -> str:
    inner = _nav_links(d)
    return re.sub(
        r'<nav class="cluster-nav"[^>]*>.*?</nav>',
        f'<nav class="cluster-nav" data-spreadsheet-cluster="20261030" aria-label="BBDBuy">{inner}</nav>',
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
    html = ensure_cluster_shell(host, path)
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
        "bbdbuy-coupons/index.html",
        "bbdbuy-telegram/index.html",
        "contact/index.html",
    ):
        p = overlay(host) / rel
        if p.is_file():
            out[rel] = p.read_bytes()
    return out


def seed_keep_pages(host: str, d: dict) -> None:
    """Copy overlay HTML from a wrap slug onto a missing keep slug.

    Only seeds keep URLs that this run will deepen. Unique skipped CMS
    Unique skipped CMS (coupons/telegram/contact) is never invented from a wrap.
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


def seed_new_overlay(host: str, template: str = "bbdbuy.uk") -> None:
    """Copy cluster shells from an existing dest so generate() can swap <main>."""
    dest = overlay(host)
    if (dest / "index.html").is_file() and MAIN_RE.search((dest / "index.html").read_text(encoding="utf-8", errors="replace")):
        return
    src = overlay(template)
    if not src.is_dir():
        raise SystemExit(f"missing template overlay {template}")
    dest.mkdir(parents=True, exist_ok=True)
    skip = {
        "bbdbuy-coupons",
        "bbdbuy-coupon",
        "bbdbuy-telegram",
        "contact",
        "DEPLOY-PLATFORM.md",
        "DEPLOY-IT-DEEPEN.md",
        "index.html.platform-patched",
    }
    for child in src.iterdir():
        if child.name in skip:
            continue
        target = dest / child.name
        if child.is_dir():
            if target.exists():
                continue
            shutil.copytree(child, target, dirs_exist_ok=True)
        elif not target.exists():
            shutil.copy2(child, target)
    print("SEED_OVERLAY", host, "from", template)


def leftover_skin() -> list[Path]:
    """Official chrome on leftover country-desk pages. Ranked body stays."""
    written: list[Path] = []
    client = None
    sftp = None
    try:
        for host, slugs in LEFTOVER_SKIN.items():
            d = HOSTS[host]
            for slug in slugs:
                path = overlay(host) / slug / "index.html"
                if not path.is_file():
                    if sftp is None:
                        client = _connect()
                        sftp = client.open_sftp()
                    remote = f"/www/wwwroot/{host}/{slug}/index.html"
                    try:
                        path.parent.mkdir(parents=True, exist_ok=True)
                        sftp.get(remote, str(path))
                    except Exception as exc:  # noqa: BLE001
                        print("SKIP leftover", host, slug, type(exc).__name__)
                        continue
                html = path.read_text(encoding="utf-8")
                before = html
                html = odskin.skin_chrome(html, host, d)
                if html == before:
                    print("LEFTOVER_SKIN_NOOP", host, slug)
                path.write_text(html, encoding="utf-8")
                written.append(path)
                print("LEFTOVER_SKIN", host, slug, path.stat().st_size)
    finally:
        if sftp is not None:
            sftp.close()
        if client is not None:
            client.close()
    return written


def provision_origin_host(host: str, template: str = "bbdbuy.uk") -> None:
    """Create wwwroot + nginx vhost from a live dest template. SSL if DNS already points here."""
    client = _connect()
    live = f"/www/wwwroot/{host}"
    conf = f"/www/server/panel/vhost/nginx/{host}.conf"
    src_conf = f"/www/server/panel/vhost/nginx/{template}.conf"
    stamp = time.strftime("%Y%m%d-%H%M%S")
    bak = f"/www/backup/bbdbuy-dest-provision-{stamp}"
    print(_run(client, f"mkdir -p '{bak}' '{live}'"))
    exists = _run(client, f"test -f '{conf}' && echo yes || echo no")
    if exists.strip() == "yes":
        print("PROVISION_SKIP nginx exists", host)
        client.close()
        return
    print(_run(client, f"cp -a '{src_conf}' '{bak}/{template}.conf'"))
    raw = _run(client, f"cat '{src_conf}'")
    raw = raw.replace(template, host)
    raw = raw.replace(f"/www/wwwroot/{template}", live)
    sftp = client.open_sftp()
    with sftp.open(conf, "w") as fh:
        fh.write(raw)
    sftp.close()
    print("PROVISION_NGINX", conf)
    for sub in (
        f"/www/server/panel/vhost/nginx/well-known/{host}.conf",
        f"/www/server/panel/vhost/rewrite/{host}.conf",
    ):
        src = sub.replace(host, template)
        print(_run(client, f"test -f '{src}' && cp -a '{src}' '{sub}' && sed -i 's/{template}/{host}/g' '{sub}' || true"))
    print(_run(client, f"mkdir -p '/www/server/panel/vhost/nginx/extension/{host}'"))
    cert_dir = f"/www/server/panel/vhost/cert/{host}"
    print(_run(client, f"mkdir -p '{cert_dir}'"))
    src_cert = f"/www/server/panel/vhost/cert/{template}"
    # Copy template certs only as a placeholder so nginx -t can parse; replace if certbot works.
    print(_run(client, f"cp -a '{src_cert}/.' '{cert_dir}/' 2>/dev/null || true"))
    test = _run(client, "nginx -t 2>&1")
    print(test)
    if "syntax is ok" in test or "successful" in test:
        print(_run(client, "nginx -s reload"))
    client.close()
    print("PROVISION", host, bak)


def generate() -> list[Path]:
    written: list[Path] = []
    seed_new_overlay("bbdbuy.fr")
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
    written.extend(leftover_skin())
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
    olds = [
        """    location /api/ {
        try_files $uri =404;
        add_header X-Robots-Tag "noindex, nofollow" always;
    }
""",
        """    location /api/ {
        try_files $uri =404;
    }
""",
    ]
    new = """    location /api/ {
        rewrite ^/api/([^/]+)/?$ /api/$1/index.php last;
        add_header X-Robots-Tag "noindex, nofollow" always;
    }
"""
    changed = 0
    sftp = client.open_sftp()
    stamp = time.strftime("%Y%m%d-%H%M%S")
    bak_root = f"/www/backup/bbdbuy-api-nginx-{stamp}"
    _run(client, f"mkdir -p '{bak_root}'")
    for host in ORDER:
        path = f"/www/server/panel/vhost/nginx/{host}.conf"
        raw = _run(client, f"cat '{path}'")
        if "rewrite ^/api/([^/]+)/?$ /api/$1/index.php last" in raw:
            print("ok", host, "api rewrite")
            continue
        matched = next((blk for blk in olds if blk in raw), None)
        if not matched:
            print("skip", host, "api block mismatch")
            continue
        _run(client, f"cp -a '{path}' '{bak_root}/{host}.conf'")
        with sftp.open(path, "w") as fh:
            fh.write(raw.replace(matched, new, 1))
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
    bak = f"/www/backup/bbdbuy-dest-{stamp}"
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
        ("https://bbdbuy.uk/", "BBDBuy Spreadsheet for UK Buyers"),
        ("https://bbdbuy.uk/", 'action="https://w2clinks.com/spreadsheet/"'),
        ("https://bbdbuy.uk/bbdbuy-coupons/", "Citable checklist"),
        ("https://bbdbuy.us/", "BBDBuy Spreadsheet for US Buyers"),
        ("https://bbdbuy.us/", 'action="https://w2clinks.com/spreadsheet/"'),
        ("https://bbdbuy.us/bbdbuy-spreadsheet/", "CBP"),
        ("https://bbdbuy.us/how-to-use-bbdbuy/", "US ZIP"),
        ("https://bbdbuy.ca/", "BBDBuy Spreadsheet for Canadian Buyers"),
        ("https://bbdbuy.ca/bbdbuy-spreadsheet/", "A1A 1A1"),
        ("https://bbdbuy.ca/bbdbuy-faq/", "CBSA"),
        ("https://bbdbuy.ca/bbdbuy-coupons/", "wallet checklist"),
        ("https://bbdbuy.it/", "Migliori finds e QC"),
        ("https://bbdbuy.it/bbdbuy-spreadsheet/", "Poste"),
        ("https://bbdbuy.it/bbdbuy-faq/", "CAP"),
        ("https://bbdbuy.it/bbdbuy-coupons/", "Coupon"),
        ("https://bbdbuyspreadsheet.de/", "Beste Finds"),
        ("https://bbdbuyspreadsheet.de/bbdbuy-spreadsheet/", "Packstation"),
        ("https://bbdbuyspreadsheet.de/bbdbuy-faq/", "Einfuhrumsatzsteuer"),
        ("https://bbdbuy.fr/", "acheteurs en France"),
        ("https://bbdbuy.fr/", 'action="https://w2clinks.com/spreadsheet/"'),
        ("https://bbdbuy.fr/bbdbuy-spreadsheet/", "code postal"),
        ("https://bbdbuy.uk/start/", "od-head"),
        ("https://bbdbuy.uk/catalog/", "od-head"),
        ("https://bbdbuy.it/start/", "od-head"),
        ("https://bbdbuyspreadsheet.de/start/", "od-head"),
        ("https://bbdbuyeu.net/", "Independent Index"),
        ("https://bbdbuyspreadsheet.uk/", None),
        ("https://bbdbuyspreadsheet.ca/", None),
        ("https://bbdbuyspreadsheet.us/", None),
    ]
    for url, needle in checks:
        req = Request(url, headers={"User-Agent": "bbdbuy-dest/1.0"})
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
                    "User-Agent": "Mozilla/5.0 (compatible; BBDBuyDestVerify/1.0)",
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
    elif cmd == "leftover":
        files = leftover_skin()
        put(files)
        verify()
    elif cmd == "provision":
        provision_origin_host("bbdbuy.fr")
    elif cmd == "all":
        reclaim_nginx()
        provision_origin_host("bbdbuy.fr")
        files = generate()
        put(files)
        verify()
        gsc_submit()
    else:
        raise SystemExit(f"unknown {cmd}")


if __name__ == "__main__":
    main()
