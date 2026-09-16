"""Build kakospreadsheet.nl as a CZ-style local catalog site (EUR, Netherlands UX)."""

from __future__ import annotations

import json
import shutil
import sys
from datetime import date
from html import escape as esc
from pathlib import Path
from urllib.parse import quote
from xml.sax.saxutils import escape as xml_esc

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.kakobuy_fi_local import fetch_w2c_products, kakobuy_url  # noqa: E402

CATALOG_PATH = ROOT / "data" / "kakobuy-nl-catalog.json"
TEMPLATE_ASSETS = ROOT / "templates" / "kakobuy-fi" / "assets"
NL_ASSETS = ROOT / "templates" / "kakobuy-nl" / "assets"
API_PHP = ROOT / "templates" / "api" / "products.php"
DOMAIN = "kakospreadsheet.nl"
BASE = f"https://{DOMAIN}"
TODAY = date.today().isoformat()
ASSET_V = "20260916a"
RUNTIME: dict = {}

NAV = [
    ("", "Home"),
    ("kakobuy-spreadsheet", "Spreadsheet"),
    ("kakobuy-finds", "Finds"),
    ("how-to-use-kakobuy", "Hoe kopen"),
    ("kakobuy-verzending", "Verzending"),
    ("kakobuy-coupon", "Coupons"),
]

PRIMARY_SLUGS = [
    "",
    "kakobuy-spreadsheet",
    "kakobuy-finds",
    "how-to-use-kakobuy",
    "kakobuy-verzending",
    "kakobuy-shipping",
    "kakobuy-coupon",
    "kakobuy-qc",
    "kakobuy-ervaringen",
    "is-kakobuy-legit",
    "is-kakobuy-safe",
    "kakobuy-discord",
    "kako-buy",
    "kako-spreadsheet",
    "about",
    "privacy-policy",
    "affiliate-disclosure",
    "partner-disclosure",
    "contact",
    "terms",
]

REDIRECTS = {
    "kakobuy-spreadsheets": "/kakobuy-spreadsheet/",
    "kakobuy-coupons": "/kakobuy-coupon/",
    "best-kakobuy-spreadsheet": "/kakobuy-spreadsheet/",
    "kakobuy-review": "/is-kakobuy-legit/",
    "kakobuy-shipping-calculator": "/kakobuy-shipping/",
    "kako-buy-spreadsheet": "/kako-spreadsheet/",
    "kako-buy-spreadsheets": "/kako-spreadsheet/",
    "kako-spreadsheets": "/kako-spreadsheet/",
    "kakobuy-spread-sheet": "/kakobuy-spreadsheet/",
    "kako-buys": "/kako-buy/",
}

HREFLANG_COMMON = {
    "es-ES": "https://kakospreadsheet.es",
    "fr-FR": "https://kakospreadsheet.fr",
    "nl-NL": "https://kakospreadsheet.nl",
    "en-CA": "https://kakospreadsheet.ca",
    "fi-FI": "https://kakobuy.fi",
    "x-default": "https://kakospreadsheet.ca",
}

I18N = {
    "locale": "nl-NL",
    "product": "Product",
    "productOne": "1 product",
    "products": "producten",
    "other": "Overig",
    "priceOnKakobuy": "Prijs op Kakobuy",
    "openOnKakobuy": "Openen op Kakobuy ↗",
    "openAria": "{title} openen op Kakobuy (nieuw tabblad)",
    "openAriaCard": "{title} — openen op Kakobuy",
    "prev": "Vorige",
    "next": "Volgende",
    "pageOf": "Pagina {current} / {pages}",
    "loadError": "Producten laden lukte niet. Probeer het zo opnieuw.",
    "emptyCount": "0 producten",
}


def load_catalog() -> dict:
    return json.loads(CATALOG_PATH.read_text(encoding="utf-8"))


def cat_map(catalog: dict) -> dict[str, dict]:
    return {c["id"]: c for c in catalog["categories"]}


def eur_amount(cny: float | int | None, rate: float) -> int | None:
    try:
        return int(round(float(cny) / rate))  # type: ignore[arg-type]
    except (TypeError, ValueError):
        return None


def format_eur(cny: float | int | None, rate: float) -> str:
    amount = eur_amount(cny, rate)
    return "Prijs op Kakobuy" if amount is None else f"≈ {amount} €"


def format_cny(cny: float | int | None) -> str:
    try:
        value = float(cny)  # type: ignore[arg-type]
    except (TypeError, ValueError):
        return ""
    if value.is_integer():
        return f"{int(value)} CNY"
    return f"{str(value).replace('.', ',')} CNY"


def format_count(n: int) -> str:
    return f"{n:,}".replace(",", ".")


def asset(path: str) -> str:
    href = f"/{path.lstrip('/')}"
    if path.endswith((".js", ".css", ".webp", ".png", ".ico")):
        return f"{href}?v={ASSET_V}"
    return href


def image_src(path: str) -> str:
    if path.startswith(("http://", "https://", "/")):
        return path
    return asset(path)


def category_options_html(catalog: dict) -> str:
    groups: dict[str, list[dict]] = {}
    for cat in catalog["categories"]:
        groups.setdefault(str(cat.get("group") or "Overig"), []).append(cat)
    parts = []
    for group, items in groups.items():
        inner = "".join(
            f'<option value="{esc(c["id"])}">{esc(c["label"])}</option>' for c in items
        )
        parts.append(f'<optgroup label="{esc(group)}">{inner}</optgroup>')
    return "".join(parts)


def catalog_boot_script() -> str:
    catalog = RUNTIME.get("catalog") or {}
    payload = {
        "affcode": catalog.get("affcode", "yze69"),
        "currency": "EUR",
        "cnyPerEur": catalog.get("cny_per_eur", 7.7762),
        "api": "/api/products.php",
        "categories": [{"id": c["id"], "label": c["label"]} for c in catalog.get("categories", [])],
        "i18n": I18N,
    }
    blob = json.dumps(payload, ensure_ascii=False, separators=(",", ":"))
    return f"<script>window.KAKOBUY_CATALOG={blob};window.KAKOBUY_FI=window.KAKOBUY_CATALOG;</script>"


def page_href(slug: str) -> str:
    return "/" if not slug else f"/{slug}/"


def canonical(slug: str) -> str:
    return f"{BASE}/" if not slug else f"{BASE}/{slug}/"


def hreflang_tags(slug: str) -> str:
    exclusive = {
        "kakobuy-ervaringen",
        "kakobuy-verzending",
        "kako-buy",
        "kako-spreadsheet",
        "partner-disclosure",
        "terms",
    }
    path = "/" if not slug else f"/{slug}/"
    if slug in exclusive:
        loc = canonical(slug)
        return (
            f'<link rel="alternate" hreflang="nl-NL" href="{esc(loc)}">\n'
            f'<link rel="alternate" hreflang="x-default" href="{esc(HREFLANG_COMMON["x-default"] + path)}">'
        )
    tags = []
    for code, origin in HREFLANG_COMMON.items():
        tags.append(f'<link rel="alternate" hreflang="{esc(code)}" href="{esc(origin + path)}">')
    return "\n".join(tags)


def head(
    *,
    title: str,
    description: str,
    canonical_url: str,
    slug: str = "",
    extra_css: list[str] | None = None,
    extra_js: list[str] | None = None,
    og_type: str = "website",
    json_ld: list[str] | None = None,
) -> str:
    css = [
        asset("assets/styles.css"),
        asset("assets/layout.css"),
        asset("assets/fi.css"),
        *(extra_css or []),
    ]
    css_tags = "".join(f'<link rel="stylesheet" href="{esc(href)}">' for href in css)
    js_tags = catalog_boot_script() + "".join(
        f'<script src="{esc(href)}" defer></script>' for href in (extra_js or [])
    )
    ld = "".join(
        f'<script type="application/ld+json">{block}</script>' for block in (json_ld or [])
    )
    return f"""<!doctype html>
<html lang="nl-NL">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(description)}">
<link rel="canonical" href="{esc(canonical_url)}">
{hreflang_tags(slug)}
<meta property="og:site_name" content="Kakobuy Spreadsheet Nederland">
<meta property="og:type" content="{esc(og_type)}">
<meta property="og:locale" content="nl_NL">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(description)}">
<meta property="og:url" content="{esc(canonical_url)}">
<meta property="og:image" content="{BASE}/assets/hero.webp">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{esc(title)}">
<meta name="twitter:description" content="{esc(description)}">
<link rel="icon" href="/assets/favicon.ico" sizes="any">
<link rel="icon" href="/assets/favicon-v2-32.png" type="image/png" sizes="32x32">
<link rel="icon" href="/assets/favicon-v2-16.png" type="image/png" sizes="16x16">
<link rel="apple-touch-icon" href="/assets/apple-touch-icon-v2.png">
<link rel="manifest" href="/site.webmanifest">
<meta name="theme-color" content="#ff5722">
{css_tags}
{ld}
{js_tags}
</head>"""


def header(current: str) -> str:
    links = []
    for slug, label in NAV:
        href = page_href(slug)
        current_attr = ' aria-current="page"' if slug == current else ""
        links.append(f'<a href="{esc(href)}"{current_attr}>{esc(label)}</a>')
    return f"""<body>
<a class="skip-link" href="#inhoud">Naar de inhoud</a>
<div class="kb-promo"><div class="container">KAKOSEP tot 30.9: pack 1300 CNY + 10 % verzending · nieuw 3000 CNY · <a href="https://ikako.vip/r/yze69" target="_blank" rel="sponsored noopener noreferrer">Registreren op Kakobuy</a></div></div>
<header class="site-header"><div class="container nav">
<a class="brand" href="/" aria-label="Kakobuy Spreadsheet Nederland – home"><span class="brand-mark">K</span><span>Kakobuy <small>Nederland</small></span></a>
<form class="kb-head-search" action="/kakobuy-spreadsheet/" method="get" role="search">
<label class="sr-only" for="kb-q">Zoek een product</label>
<input id="kb-q" type="search" name="q" placeholder="Product, kako buy, of plak een link" autocomplete="off">
<button type="submit">Zoeken</button>
</form>
<div class="nav-actions">
<a class="button small" href="https://ikako.vip/r/yze69" target="_blank" rel="sponsored noopener noreferrer">Registreren</a>
<button class="menu-button" type="button" aria-label="Menu openen" aria-expanded="false">☰</button>
</div>
</div></header>
<nav class="kb-subnav" aria-label="Hoofdmenu"><div class="container nav-links">{"".join(links)}</div></nav>
<main id="inhoud">"""


def footer() -> str:
    return f"""</main>
<footer class="site-footer"><div class="container">
<div class="footer-grid">
<div><a class="brand" href="/"><span class="brand-mark">K</span><span>Kakobuy Nederland</span></a>
<p class="footer-copy">Onafhankelijke Nederlandstalige catalogus en Kakobuy spreadsheet-gids. Ook voor zoekopdrachten kako buy en kako-spreadsheet.</p></div>
<div class="footer-col"><strong>Gids</strong>
<a href="/how-to-use-kakobuy/">Hoe kopen</a>
<a href="/kakobuy-verzending/">Verzending Nederland</a>
<a href="/kakobuy-ervaringen/">Kakobuy ervaringen</a>
<a href="/is-kakobuy-legit/">Betrouwbaar?</a></div>
<div class="footer-col"><strong>Producten</strong>
<a href="/kakobuy-spreadsheet/">Kakobuy spreadsheet</a>
<a href="/kakobuy-finds/">Finds</a>
<a href="/kakobuy-coupon/">Coupons</a>
<a href="/kako-buy/">Kako buy</a>
<a href="/kako-spreadsheet/">Kako spreadsheet</a></div>
<div class="footer-col"><strong>Info</strong>
<a href="/about/">Over</a>
<a href="/privacy-policy/">Privacy</a>
<a href="/affiliate-disclosure/">Affiliate</a></div>
</div>
<div class="footer-bottom"><span>© <span data-year></span> kakospreadsheet.nl</span>
<span>Dit is niet de officiële website van Kakobuy.</span></div>
</div></footer>
<script src="{esc(asset("assets/site.js"))}" defer></script>
</body></html>"""


def wrap(slug: str, title: str, description: str, body: str, **head_kw) -> str:
    return (
        head(
            title=title,
            description=description,
            canonical_url=canonical(slug),
            slug=slug,
            **head_kw,
        )
        + header(slug)
        + body
        + footer()
    )


def faq_list_html(items: list[tuple[str, str]]) -> str:
    blocks = []
    for q, a in items:
        blocks.append(
            f'<div class="faq-item"><button class="faq-question" type="button" aria-expanded="false">{esc(q)}</button>'
            f'<div class="faq-answer"><p>{esc(a)}</p></div></div>'
        )
    return f'<div class="faq-list">{"".join(blocks)}</div>'


def json_ld_website() -> str:
    return json.dumps(
        {
            "@context": "https://schema.org",
            "@type": "WebSite",
            "name": "Kakobuy Spreadsheet Nederland",
            "url": f"{BASE}/",
            "inLanguage": "nl-NL",
            "description": "Kakobuy spreadsheet voor Nederland: productlinks, prijzen in euro, QC en verzending. Ook voor kako buy en kako-spreadsheet.",
        },
        ensure_ascii=False,
    )


def json_ld_itemlist(name: str, products: list[dict], catalog: dict) -> str:
    aff = catalog["affcode"]
    elements = []
    for i, p in enumerate(products, 1):
        elements.append(
            {
                "@type": "ListItem",
                "position": i,
                "name": p["title"],
                "url": kakobuy_url(p["item_id"], aff, p.get("shop") or "weidian"),
            }
        )
    return json.dumps(
        {
            "@context": "https://schema.org",
            "@type": "ItemList",
            "name": name,
            "numberOfItems": len(products),
            "dateModified": catalog["checked"],
            "itemListElement": elements,
        },
        ensure_ascii=False,
    )


def json_ld_faq(name: str, url: str, items: list[tuple[str, str]]) -> str:
    return json.dumps(
        {
            "@context": "https://schema.org",
            "@type": "FAQPage",
            "name": name,
            "url": url,
            "inLanguage": "nl-NL",
            "dateModified": TODAY,
            "mainEntity": [
                {
                    "@type": "Question",
                    "name": q,
                    "acceptedAnswer": {"@type": "Answer", "text": a},
                }
                for q, a in items
            ],
        },
        ensure_ascii=False,
    )


def sheet_card(p: dict, catalog: dict, cats: dict) -> str:
    label = (cats.get(p["category"]) or {}).get("label") or p["category"] or "Overig"
    rate = catalog["cny_per_eur"]
    href = kakobuy_url(p["item_id"], catalog["affcode"], p.get("shop") or "weidian")
    cny = format_cny(p.get("price_cny"))
    return (
        f'<li class="sheet-product" data-product-id="{esc(p["id"])}" data-category="{esc(p["category"])}">'
        f'<img src="{esc(image_src(p["image"]))}" width="750" height="750" alt="{esc(p["title"])}" loading="lazy" decoding="async">'
        f'<div class="sheet-product-info"><span>{esc(label)}</span><h2>{esc(p["title"])}</h2></div>'
        f'<div class="sheet-price"><strong>{esc(format_eur(p.get("price_cny"), rate))}</strong>'
        f'<small>{esc(cny)}</small></div>'
        f'<a class="sheet-buy" href="{esc(href)}" target="_blank" rel="sponsored noopener noreferrer" '
        f'aria-label="{esc(p["title"])} openen op Kakobuy (nieuw tabblad)">Openen op Kakobuy ↗</a></li>'
    )


def finds_card(p: dict, catalog: dict, cats: dict) -> str:
    label = (cats.get(p["category"]) or {}).get("label") or p["category"] or "Overig"
    rate = catalog["cny_per_eur"]
    href = kakobuy_url(p["item_id"], catalog["affcode"], p.get("shop") or "weidian")
    brand = f'<p class="catalog-advice">{esc(p["brand"])}</p>' if p.get("brand") else ""
    cny = format_cny(p.get("price_cny"))
    return f"""<article class="catalog-card" data-product-id="{esc(p["id"])}">
<a class="catalog-image" href="{esc(href)}" target="_blank" rel="sponsored noopener noreferrer" aria-label="{esc(p["title"])} — openen op Kakobuy">
<img src="{esc(image_src(p["image"]))}" width="750" height="750" alt="{esc(p["title"])}" loading="lazy" decoding="async"><span>{esc(label)}</span></a>
<div class="catalog-body">
<h3>{esc(p["title"])}</h3>
<div class="catalog-meta"><strong>{esc(format_eur(p.get("price_cny"), rate))}</strong><small>{esc(cny)}</small></div>
{brand}
<a class="text-link" href="{esc(href)}" target="_blank" rel="sponsored noopener noreferrer">Openen op Kakobuy ↗</a>
</div></article>"""


def rate_note(catalog: dict) -> str:
    return (
        f'Prijzen en links gecontroleerd op <time datetime="{esc(catalog["checked"])}">{esc(catalog["checked"])}</time>. '
        f'ECB-koers van <time datetime="{esc(catalog["ecb_date"])}">{esc(catalog["ecb_date"])}</time>: '
        f'1 EUR ≈ {str(catalog["cny_per_eur"]).replace(".", ",")} CNY, afgerond op de euro. '
        "Dit is de catalogusprijs van het product, zonder internationale verzending, heffingen en invoer-btw. "
        "Bevestig de variant op Kakobuy voordat je betaalt."
    )


FAQ: list[tuple[str, str]] = [
    (
        "Wat is Kakobuy?",
        "Kakobuy is een inkoop- en verzendagent. Hij bestelt op compatibele Chinese marketplaces, ontvangt in het warehouse, maakt QC-foto’s en biedt internationale lijnen naar Nederland.",
    ),
    (
        "Verkoopt kakospreadsheet.nl producten?",
        "Nee. Deze site is een onafhankelijke catalogus en affiliate-gids. Aankoop, betaling en verzending gebeuren op Kakobuy en bij de verkopers.",
    ),
    (
        "Kako buy, kako-buy of kako spreadsheet: is dat hetzelfde?",
        "Ja. Veel mensen typen kako buy, kako-buy, kako spreadsheet of kako-spreadsheet. De officiële naam is Kakobuy. De Kakobuy spreadsheet is de linkcatalogus op deze site.",
    ),
    (
        "Hoeveel kost verzending naar Nederland?",
        "Dat hangt af van werkelijk of volumetrisch gewicht, afmetingen, lijn en inhoud. De live-offerte verschijnt in je Kakobuy-account zodra de items in het warehouse liggen.",
    ),
    (
        "BTW en douane in Nederland?",
        "Ja, bij zendingen van buiten de EU. Het algemene btw-tarief in Nederland is 21 %. Sinds 1.7.2026 dragen veel afstandsverkopen tot 150 € ook 3 € recht per tariefpost. Kakobuy kan duty-free lijnen bieden: check bij checkout. Zie belastingdienst.nl.",
    ),
    (
        "Is Kakobuy betrouwbaar?",
        "Kakobuy is een werkend agentplatform. Deze site is Kakobuy niet en garandeert geen prijs, kwaliteit of inklaring. Betaal met kopersbescherming, lees de QC-foto’s en check lijnrestricties.",
    ),
]

def page_home(catalog: dict) -> str:
    cats = cat_map(catalog)
    found, live = RUNTIME.get("live") or (0, [])
    featured = live[:8]
    rate = catalog["cny_per_eur"]
    count_label = f"{format_count(found)}+" if found else "Duizenden"
    cat_count = len(catalog["categories"])
    cards = []
    for p in featured:
        href = kakobuy_url(p["item_id"], catalog["affcode"], p.get("shop") or "weidian")
        label = (cats.get(p["category"]) or {}).get("label") or p["category"] or "Overig"
        cards.append(
            f'<a class="card catalog-card" href="{esc(href)}" target="_blank" rel="sponsored noopener noreferrer">'
            f'<div class="catalog-image"><img src="{esc(image_src(p["image"]))}" alt="{esc(p["title"])}" width="640" height="640" loading="lazy">'
            f"<span>{esc(label)}</span></div>"
            f'<div class="catalog-body"><h3>{esc(p["title"])}</h3>'
            f'<div class="catalog-meta"><strong>{esc(format_eur(p.get("price_cny"), rate))}</strong>'
            f'<small>{esc(format_cny(p.get("price_cny")))}</small></div></div></a>'
        )
    body = f"""
<section class="hero"><div class="container hero-grid">
<div class="hero-copy">
<span class="eyebrow">Productlinks · prijzen in euro</span>
<h1>Kakobuy Spreadsheet<br><span class="gradient-text">voor Nederland</span></h1>
<p>Bekijk de catalogus op één plek. Zoek op naam, filter een categorie en vergelijk indicatieve prijzen in euro. Het product opent op Kakobuy — ook als je kako buy of kako spreadsheet hebt getypt.</p>
<form class="kb-hero-search" action="/kakobuy-spreadsheet/" method="get" role="search">
<label class="sr-only" for="hero-q">Zoeken in de spreadsheet</label>
<input id="hero-q" type="search" name="q" placeholder="Product, kako buy, of plak een Weidian-link" autocomplete="off">
<button type="submit">Zoeken</button>
</form>
<div class="hero-actions">
<a class="button" href="/kakobuy-spreadsheet/">Spreadsheet openen <span aria-hidden="true">→</span></a>
<a class="button secondary" href="/how-to-use-kakobuy/">Hoe de aankoop werkt</a>
</div>
<div class="trust-row" aria-label="Voordelen">
<span><i class="check">✓</i> Geen account op deze site</span>
<span><i class="check">✓</i> Prijzen in euro</span>
<span><i class="check">✓</i> Verzendnotities Nederland</span>
</div>
</div>
<div class="hero-visual hero-art">
<img class="hero-art-image" src="{esc(asset('assets/hero.webp'))}" width="1152" height="864" alt="Kakobuy-verzending naar Nederland: warehouse, QC en pakket" fetchpriority="high">
</div>
</div></section>
<section class="kb-offers"><div class="container">
<div class="section-heading"><p class="kicker">Kakobuy.com · september 2026</p>
<h2>Huidige aanbiedingen</h2>
<p>Officiële Kakobuy-campagnes. Voorwaarden, korting en data bevestig je in het account vóór je betaalt.</p></div>
<div class="kb-offer-grid">
<a class="kb-offer" href="https://www.kakobuy.com/tipdetail?id=55" target="_blank" rel="noopener noreferrer">
<span class="kb-offer-tag">Code KAKOSEP</span>
<strong>Septemberpack 1300 CNY ≈ 167 € + 10 % extra verzending</strong>
<p>Inwisselbaar van 8 tot 30.9.2026 (Peking-tijd). Op Kakobuy: User Center → Coupons → Redeem, code <strong>KAKOSEP</strong>.</p>
<span class="text-link">Campagne openen op Kakobuy ↗</span></a>
<a class="kb-offer" href="https://ikako.vip/r/yze69" target="_blank" rel="sponsored noopener noreferrer">
<span class="kb-offer-tag">Nieuwe gebruiker</span>
<strong>Couponpack 3000 CNY ≈ 386 €</strong>
<p>Registreer via de invitielink. Coupons verschijnen in de wallet; de spreadsheet past ze niet zelf toe.</p>
<span class="text-link">Registreren ↗</span></a>
<a class="kb-offer" href="https://www.kakobuy.com/tipdetail?id=55" target="_blank" rel="noopener noreferrer">
<span class="kb-offer-tag">Subsidie 10 %</span>
<strong>Verzendkrediet 8–14.9, te gebruiken tot 31.10.2026</strong>
<p>Het venster om de sitewide-subsidie te krijgen is dicht. Als je die al had, geeft Kakobuy aan dat die tot 31.10.2026 geldig is.</p>
<span class="text-link">Regels op Kakobuy ↗</span></a>
<a class="kb-offer" href="/kakobuy-verzending/">
<span class="kb-offer-tag">EU / Nederland</span>
<strong>3 € recht / zending en duty-free lijnen</strong>
<p>Kakobuy biedt EU-lijnen met ongeveer 3 € recht per zending op in aanmerking komende tariefposten. BTW 21 % in Nederland volgt bij invoer.</p>
<span class="text-link">Verzending Nederland →</span></a>
</div>
</div></section>
<section class="stats"><div class="container stats-grid">
<div class="stat"><strong>{esc(count_label)} producten</strong><span>Doorzoekbare catalogus op deze site</span></div>
<div class="stat"><strong>{cat_count} categorieën</strong><span>Van sneakers tot accessoires</span></div>
<div class="stat"><strong>Prijzen in euro</strong><span>Indicatief, zonder verzending</span></div>
</div></section>
<section class="section"><div class="container">
<div class="section-heading"><p class="kicker">Laatste finds</p>
<h2>Sneakers, kleding en accessoires met Kakobuy-links</h2>
<p>Je kunt de volledige lijst op naam zoeken of tot één categorie beperken.</p></div>
<div class="catalog-grid">{"".join(cards)}</div>
<p class="catalog-note">Wij zijn niet de verkoper · check prijs en voorraad vóór je bestelt
<a class="text-link" href="/kakobuy-spreadsheet/">Kakobuy Spreadsheet · zoek in de hele catalogus →</a></p>
<p class="catalog-price-note">{rate_note(catalog)}</p>
</div></section>
<section class="section soft"><div class="container">
<div class="section-heading"><h2>Catalogus, bestelling en verzending</h2>
<p>Meer catalogus, de aankoopstappen en de kosten tot Nederland.</p></div>
<div class="card-grid">
<a class="card" href="/kakobuy-spreadsheet/"><div class="card-icon">▦</div><h3>Beste spreadsheet</h3>
<p>Categorieën en links als je geen uur op Chinese marketplaces wilt zoeken. De term best kakobuy spreadsheet landt hier.</p>
<span class="text-link">Catalogus openen ↗</span></a>
<a class="card" href="/how-to-use-kakobuy/"><div class="card-icon">1</div><h3>Eerste bestelling</h3>
<p>Wat je nu betaalt, wat je in het warehouse betaalt, en waarom je QC niet blind moet goedkeuren.</p></a>
<a class="card" href="/kakobuy-verzending/"><div class="card-icon">→</div><h3>Verzending Nederland</h3>
<p>Werkelijk vs volumetrisch gewicht, consolidatie, tracking, BTW 21 % en 3 € recht.</p></a>
</div></div></section>
<section class="section"><div class="container">
<div class="section-heading"><h2>Kopen in zes stappen</h2>
<p>Het artikel komt eerst in het warehouse. De lijn naar Nederland kies je na de foto’s.</p></div>
<div class="steps">
<div class="step"><h3>Vind het product</h3><p>Kies een spreadsheet-link of een marketplace-URL.</p></div>
<div class="step"><h3>Plak de link</h3><p>Kies variant, maat, kleur en aantal.</p></div>
<div class="step"><h3>Betaal het artikel</h3><p>Na betaling stuurt de verkoper naar het Kakobuy-warehouse.</p></div>
<div class="step"><h3>Sla QC niet over</h3><p>Vergelijk kleur, labels, aantal en zichtbare gebreken.</p></div>
<div class="step"><h3>Verstuur het pakket</h3><p>Consolideer items en kies een lijn naar Nederland.</p></div>
<div class="step"><h3>Volg de zending</h3><p>Gebruik het trackingnummer zodra het pakket vertrekt.</p></div>
</div></div></section>
<section class="section soft"><div class="container split">
<div><h2>De spreadsheet is een kaart, geen kwaliteitsstempel</h2>
<p>De catalogus staat op deze site. Bij elk aanbod kies je Kakobuy nog steeds als agent.</p>
<ul class="check-list"><li>Minder handmatig zoeken</li><li>Link naar de oorspronkelijke listing</li><li>Geen garantie op prijs of kwaliteit</li></ul>
<p>Typte je <a href="/kako-buy/">kako buy</a> of <a href="/kako-spreadsheet/">kako spreadsheet</a>? Dat is dezelfde Kakobuy, met de catalogus hier.</p></div>
<div>{faq_list_html(FAQ[:4])}</div>
</div></section>
<section class="cta"><div class="container"><div class="cta-box">
<h2>Heb je al een productlink?</h2>
<p>Plak die in de Kakobuy-zoekbalk. Zoek je nog ideeën, begin bij de spreadsheet.</p>
<a class="button" href="/kakobuy-spreadsheet/">Catalogus bekijken</a>
</div></div></section>
"""
    json_ld_blocks = [json_ld_website()]
    if featured:
        json_ld_blocks.append(json_ld_itemlist("Productcatalogus", featured, catalog))
    return wrap(
        "",
        "Kakobuy Spreadsheet Nederland – producten, prijzen in euro en QC",
        "Kakobuy spreadsheet voor Nederland: zoek op naam, filter categorieën, indicatieve prijzen in euro en links die op Kakobuy openen. Ook voor kako buy en best kakobuy spreadsheet. Onafhankelijke gids.",
        body,
        extra_css=[asset("assets/catalog.css")],
        json_ld=json_ld_blocks,
    )


def page_spreadsheet(catalog: dict) -> str:
    cats = cat_map(catalog)
    found, live = RUNTIME.get("live") or (0, [])
    options = category_options_html(catalog)
    items = "".join(sheet_card(p, catalog, cats) for p in live[:24])
    extra_ids = [
        "SNEAKERS",
        "T-SHIRT",
        "HOODIE",
        "JACKET",
        "TROUSERS",
        "SHORTS",
        "Jersey",
        "BAG",
        "HAT",
        "Electronics",
        "CHILD",
        "JEWELRY",
    ]
    extra = "".join(
        f'<a href="/kakobuy-spreadsheet/?category={quote(c["id"])}" data-sheet-category="{esc(c["id"])}">{esc(c["label"])}</a>'
        for c in catalog["categories"]
        if c["id"] in extra_ids
    )
    count_label = f"{format_count(found)} producten" if found else "Laden…"
    body = f"""
<section class="container sheet-intro"><p class="kicker">Catalogus Nederland · doorzoekbaar</p>
<h1>Kakobuy Spreadsheet voor Nederland</h1>
<p>Dit is de spreadsheet die je écht kunt doorzoeken: live links, prijzen in euro en checkout op Kakobuy, geen screenshot van een Google Sheet. Zoekopdrachten kakobuy spreadsheet, best kakobuy spreadsheet, kako spreadsheet en kako-buy spreadsheet komen hier uit.</p></section>
<section class="container sheet-content" aria-label="Productlijst">
<div class="sheet-controls">
<div class="sheet-field"><label for="sheet-search">Producten zoeken</label>
<input type="search" id="sheet-search" placeholder="bijv. hoodie, tas, Jordan" autocomplete="off" aria-controls="sheet-products"></div>
<div class="sheet-field"><label for="sheet-category">Categorie</label>
<select id="sheet-category" aria-controls="sheet-products"><option value="all">Alle categorieën</option>{options}</select></div>
<button type="button" class="sheet-reset">Filters wissen</button>
<output id="sheet-count" aria-live="polite">{esc(count_label)}</output>
</div>
<p class="sheet-disclosure">Prijzen zijn indicatief, zonder verzending en andere heffingen. Links zijn affiliate; we kunnen commissie ontvangen.</p>
<ul id="sheet-products" class="sheet-products">{items}</ul>
<nav id="sheet-pager" class="sheet-pager" aria-label="Paginering" hidden></nav>
<p class="sheet-empty" role="status" hidden>Geen producten. Probeer een kortere naam of een andere categorie.</p>
<details class="sheet-method"><summary>Prijzen en controledatum</summary>
<p>{rate_note(catalog)}</p>
<p>Foto’s en namen komen uit de listings. We hebben de items niet fysiek getest; authenticiteit en warehouse-voorraad bevestig je hier niet. <a href="/affiliate-disclosure/">Affiliate-vermelding</a></p>
</details>
</section>
<section class="section soft" id="beste"><div class="container">
<div class="section-heading"><h2>Beste Kakobuy spreadsheet (2026)</h2>
<p>De nuttige spreadsheet is degene die je hier kunt zoeken — niet een bevroren lijst van 24 Weidian-SKU’s. <code>/best-kakobuy-spreadsheet/</code> verwijst naar deze pagina, in lijn met de bestaande redirect.</p></div>
</div></section>
<section class="section soft" id="categorieen"><div class="container">
<div class="section-heading"><h2>Verkennen per categorie</h2>
<p>Kies een categorie om deze pagina te filteren. Het product opent op Kakobuy.</p></div>
<div class="sheet-categories">{extra}</div>
</div></section>
<section class="section"><div class="container sheet-help">
<div><h2>Wat is een Kakobuy spreadsheet?</h2>
<p>Een lijst productlinks om via Kakobuy te kopen. Je bladert deze catalogus in de browser; elke rij heeft een categorie en een prijs in euro.</p>
<p>Liever kaarten? Zie <a href="/kakobuy-finds/">Kakobuy Finds</a>.</p></div>
<div><h2>Wat daarna</h2>
<p>Open op Kakobuy, check variant en live prijs. In het warehouse: QC-foto’s, daarna verzending naar Nederland.</p>
<p><a href="/how-to-use-kakobuy/">Gids eerste bestelling</a> · <a href="/kakobuy-verzending/">Verzending Nederland</a></p></div>
</div></section>
"""
    json_ld_blocks = []
    if live:
        json_ld_blocks.append(
            json_ld_itemlist("Kakobuy Spreadsheet – producten met prijzen in euro", live[:24], catalog)
        )
    return wrap(
        "kakobuy-spreadsheet",
        "Beste Kakobuy Spreadsheet – producten met prijzen in euro",
        "Beste Kakobuy spreadsheet voor Nederland: zoek op naam, filter categorie, vergelijk prijzen in euro en open het product op Kakobuy. Ook voor kako spreadsheet.",
        body,
        extra_css=[asset("assets/spreadsheet.css")],
        extra_js=[asset("assets/catalog-live.js"), asset("assets/spreadsheet.js")],
        json_ld=json_ld_blocks,
    )


def page_finds(catalog: dict) -> str:
    cats = cat_map(catalog)
    _found, live = RUNTIME.get("live") or (0, [])
    options = category_options_html(catalog)
    cards = "".join(finds_card(p, catalog, cats) for p in live[:24])
    body = f"""
<section class="article-hero finds-hero"><div class="container">
<span class="eyebrow">Laatste finds · prijzen in euro</span>
<h1>Kakobuy Finds</h1>
<p>Kaartweergave van de catalogus. Sneller zoeken? Open de <a class="text-link" href="/kakobuy-spreadsheet/">Kakobuy Spreadsheet</a>.</p>
</div></section>
<section class="section finds-catalog"><div class="container">
<div class="catalog-context">
<p>Schattingen zonder verzending en andere heffingen. Links zijn affiliate; we kunnen commissie ontvangen.</p>
<details><summary>Prijzen, datum en notities</summary>
<p>{rate_note(catalog)}</p></details>
</div>
<div class="catalog-filter" hidden>
<label for="catalog-category">Categorie tonen</label>
<select id="catalog-category"><option value="all">Alle categorieën</option>{options}</select>
<output id="catalog-count">{esc(format_count(_found) + " producten") if _found else "Laden…"}</output>
</div>
<div id="finds-grid" class="catalog-grid">{cards}</div>
<p class="finds-empty sheet-empty" role="status" hidden>Geen producten in deze categorie.</p>
<p class="catalog-price-note">{rate_note(catalog)}</p>
</div></section>
"""
    json_ld_blocks = []
    if live:
        json_ld_blocks.append(
            json_ld_itemlist("Kakobuy Finds – producten met prijzen in euro", live[:24], catalog)
        )
    return wrap(
        "kakobuy-finds",
        "Kakobuy Finds – producten met prijzen in euro",
        "Kakobuy Finds voor Nederland: laatste finds met prijzen in euro en directe Kakobuy-links.",
        body,
        extra_css=[asset("assets/catalog.css")],
        extra_js=[asset("assets/catalog-live.js"), asset("assets/finds.js")],
        json_ld=json_ld_blocks,
    )


def page_guide() -> str:
    body = """
<section class="article-hero"><div class="container">
<span class="eyebrow">6 stappen voor Nederland</span>
<h1>Hoe je via Kakobuy koopt vanuit Nederland</h1>
<p>Van account tot verzending. Op kakospreadsheet.nl maak je geen account en plaats je geen bestelling.</p>
</div></section>
<div class="container article-layout"><article class="article">
<p>Kakobuy zit tussen jou en de verkoper. De goederen gaan niet rechtstreeks naar huis: je betaalt het artikel, het komt in het warehouse, je bekijkt foto’s, daarna betaal je internationale verzending naar Nederland.</p>
<div class="article-callout"><strong>Voor je op Betalen klikt</strong>Houd de originallink bij, check de variant, en zorg dat de lijn het artikel accepteert en dat je het legaal in Nederland kunt invoeren.</div>
<h2 id="stap-1">1. Maak een Kakobuy-account</h2>
<p>Ga naar <a class="text-link" href="https://ikako.vip/r/yze69" target="_blank" rel="noopener noreferrer">Kakobuy-registratie</a> en kies Sign Up. Vul e-mail, wachtwoord en eventuele verificatie in.</p>
<p>Registratie kan een couponpack bevatten. Check waarde en voorwaarden in het account; het geldt niet automatisch voor elke aankoop.</p>
<h2 id="stap-2">2. Vind het product of plak een link</h2>
<p>Plak een gekopieerde link of zoek op trefwoord. Heb je een Taobao-, 1688- of Weidian-URL, plak die in Kakobuy en bevestig dat het juiste product laadt.</p>
<p>Je kunt ook starten bij <a class="text-link" href="/kakobuy-finds/">Finds</a> of de <a class="text-link" href="/kakobuy-spreadsheet/">spreadsheet</a>. Een link bevestigt geen kwaliteit of voorraad.</p>
<h2 id="stap-3">3. Kies variant en betaal de order</h2>
<p>Kies kleur, maat en aantal. Bij kleding volg je de matentabel van de verkoper, niet alleen een Nederlandse lettermaat. De eerste betaling is niet de eindprijs tot de deur. Internationale verzending betaal je later, als het warehouse gewicht en maten kent.</p>
<h2 id="stap-4">4. Lees de QC-foto’s in het warehouse</h2>
<p>Als het item is opgeslagen, open Warehouse en QC Picture. Vergelijk kleur, maattag, aantal en zichtbare details. QC toont zichtbare fouten; het bewijst authenticiteit niet alleen.</p>
<div class="article-callout"><strong>Klopt er iets niet?</strong>Open een ticket bij support vóór internationale verzending.</div>
<h2 id="stap-5">5. Voeg een Nederlands adres toe en kies de lijn</h2>
<p>Selecteer de items om te versturen en voeg het juiste adres toe. Land moet <strong>Netherlands / Nederland</strong> zijn. Check naam, straat, postcode, plaats en telefoon; gebruik landcode <strong>+31</strong>.</p>
<p>Vergelijk de lijnen die écht worden aangeboden voor dit adres en deze goederen. Kies op prijs, restricties, formaat, gewicht en voorwaarden. Meer: <a class="text-link" href="/kakobuy-verzending/">verzendgids Nederland</a>.</p>
<h2 id="stap-6">6. Bevestig verzending en volg het pakket</h2>
<p>Voor je bevestigt, check adres, inhoud, lijn en prijs. Vul douanegegevens juist in. Na verzending volg je het nummer in het Kakobuy-account. De eerste scan is niet altijd meteen.</p>
<h2 id="fouten">Veelgemaakte fouten</h2>
<ul><li>Verkeerde maat zonder de maattabel te bekijken.</li><li>QC-foto’s overslaan.</li><li>Alleen werkelijk gewicht begroten en volumetrisch vergeten.</li><li>Items met verzend- of invoerbeperking kopen.</li><li>Onjuiste douaneaangifte.</li></ul>
<p class="legal-note">Dit is algemene informatie. Bevestig prijs, voorraad, verzendvoorwaarden en invoerverplichtingen op Kakobuy en bij de Nederlandse autoriteiten vóór je betaalt.</p>
<p style="margin-top:30px"><a class="button" href="/kakobuy-finds/">Finds bekijken →</a></p>
</article>
<aside class="toc"><strong>Gids</strong>
<a href="#stap-1">1. Account</a>
<a href="#stap-2">2. Product vinden</a>
<a href="#stap-3">3. Variant en betaling</a>
<a href="#stap-4">4. QC lezen</a>
<a href="#stap-5">5. Adres in Nederland</a>
<a href="#stap-6">6. Verzenden en volgen</a>
<a href="#fouten">Veelgemaakte fouten</a></aside></div>
"""
    return wrap(
        "how-to-use-kakobuy",
        "Hoe Kakobuy gebruiken vanuit Nederland – stap voor stap",
        "Nederlandse gids om met Kakobuy te kopen: link, order, warehouse, QC-foto’s en verzending naar Nederland.",
        body,
        og_type="article",
    )


def page_shipping_nl() -> str:
    body = """
<section class="article-hero"><div class="container">
<span class="eyebrow">Verzending Nederland · bijgewerkt 16.9.2026</span>
<h1>De goedkoopste lijn is niet altijd het goedkoopste pakket</h1>
<p>Facturabel gewicht, afmetingen, inhoud en wat de offerte omvat bepalen de echte kosten. Gebruik deze lijst om aanbiedingen te vergelijken.</p>
</div></section>
<div class="container article-layout"><article class="article">
<h2 id="stroom">Hoe verzending werkt</h2>
<p>Items van verschillende verkopers komen eerst in het Kakobuy-warehouse. Als ze klaar zijn, kies je wat samen gaat, pas je de verpakking aan en vergelijk je internationale lijnen naar Nederland.</p>
<h2 id="gewicht">Werkelijk en volumetrisch gewicht</h2>
<p>De vervoerder kan werkelijk of volumetrisch gewicht factureren. Een licht maar omvangrijk item kan duurder zijn door volume. De deler en regels verschillen per lijn.</p>
<div class="article-callout"><strong>Praktische tip</strong>Bij omvangrijke producten: extra dozen eraf of vacuümzak, als dat het artikel niet beschadigt.</div>
<h2 id="lijnen">Lijnen vergelijken</h2>
<ul>
<li>Prijs: vergelijk het totaal, niet alleen de eerste gewichtsstap.</li>
<li>Geschatte tijd: een schatting, geen gegarandeerde dag. PostNL of DHL last-mile wisselt per lijn.</li>
<li>Inhoudsbeperkingen: sommige lijnen weigeren batterijen, vloeistoffen, cosmetica of bepaalde materialen.</li>
<li>Tracking en verzekering: check hoever tracking gaat en wat de verzekering dekt.</li>
<li>Factuurmethode: bevestig werkelijk vs volumetrisch gewicht.</li>
</ul>
<h2 id="consolideren">Consolidatie en verpakking</h2>
<p>Meerdere items in één zending kan vaste kosten drukken, maar een grotere doos is niet altijd goedkoper. Breekbaar heeft bescherming nodig; sneakers of kleding kunnen vaak zonder originele doos als je dat vraagt.</p>
<h2 id="btw">BTW en douane in Nederland 2026</h2>
<p>Zendingen van buiten de EU vragen een aangifte en btw wordt geheven. Het algemene tarief in Nederland is <strong>21 %</strong>. Sinds 1.7.2026 dragen veel afstandsverkopen tot 150 € ook een tijdelijk recht van <strong>3 € per tariefpost</strong>. Eén post kan meerdere stuks van hetzelfde type bevatten; het is niet automatisch 3 € per stuk. Boven 150 € geldt het gebruikelijke recht.</p>
<p>PostNL of een andere vervoerder kan btw en afhandelingskosten innen vóór levering, tenzij de lijn vooraf is betaald (IOSS / tax-paid). Als btw al via IOSS is betaald, zou die niet opnieuw moeten worden geïnd, maar de IOSS-gegevens moeten goed worden doorgegeven.</p>
<p>Geldende regels: <a href="https://www.belastingdienst.nl/" target="_blank" rel="noopener noreferrer">belastingdienst.nl ↗</a> · <a href="https://www.belastingdienst.nl/wps/wcm/connect/nl/douane/douane" target="_blank" rel="noopener noreferrer">Douane ↗</a></p>
<h2 id="tracking">Tracking</h2>
<p>Na aanmaken van de zending verschijnt vaak een trackingnummer. Het gat tussen label en eerste fysieke scan is normaal. Op sommige routes wordt tracking duidelijker bij aankomst in Europa of bij de last-mile (PostNL/DHL).</p>
<h2 id="check">Check vóór je vracht betaalt</h2>
<ul>
<li>Ik heb QC-foto’s van alle items gezien.</li>
<li>Ik ken het eindgewicht en de afmetingen.</li>
<li>Ik heb de restricties van de lijn gelezen.</li>
<li>Ik begrijp verzekering en tracking.</li>
<li>Ik heb juiste gegevens voor transport en douane gegeven.</li>
</ul>
</article>
<aside class="toc"><strong>Inhoud</strong>
<a href="#stroom">Hoe het werkt</a>
<a href="#gewicht">Gewicht</a>
<a href="#lijnen">Lijn kiezen</a>
<a href="#consolideren">Consolidatie</a>
<a href="#btw">BTW en douane</a>
<a href="#tracking">Tracking</a>
<a href="#check">Checklist</a></aside></div>
"""
    return wrap(
        "kakobuy-verzending",
        "Kakobuy verzending Nederland – gewicht, BTW 21 % en douane",
        "Hoe Kakobuy-verzending naar Nederland werkt: consolidatie, werkelijk vs volumetrisch gewicht, BTW 21 %, 3 € recht, PostNL en IOSS.",
        body,
        og_type="article",
    )


def page_shipping_generic() -> str:
    body = """
<section class="article-hero"><div class="container">
<h1>Kakobuy shipping</h1>
<p>Algemene verzendgids. Bestel je naar Nederland, gebruik de pagina over BTW en douane. Deze pagina dekt ook zoekopdrachten kakobuy shipping calculator.</p>
</div></section>
<div class="container article-layout"><article class="article">
<p>Vracht betaal je op Kakobuy als de items in het warehouse liggen. Vergelijk facturabel gewicht, restricties en of de lijn btw of recht vooruit aangeeft.</p>
<p>Er is geen losse rekenmachine op deze site: de live calculator zit in het Kakobuy-account na QC. Voor Nederlandse kopers: <a class="text-link" href="/kakobuy-verzending/">Kakobuy verzending naar Nederland</a> (BTW 21 %, recht en tracking).</p>
</article></div>
"""
    return wrap(
        "kakobuy-shipping",
        "Kakobuy shipping — verzendgids en calculator-notities",
        "Kakobuy shipping en shipping calculator: gewicht, consolidatie en link naar de Nederlandse gids (BTW 21 %).",
        body,
        og_type="article",
    )


def page_coupon() -> str:
    body = """
<section class="article-hero"><div class="container">
<h1>Kakobuy coupon en campagnes</h1>
<p>Officieel op kakobuy.com op 16.9.2026: code <strong>KAKOSEP</strong> (pack 1300 CNY + 10 % extra verzending tot 30.9), nieuw-gebruikerspack 3000 CNY, en 10 % subsidiekrediet tot 31.10 als je dat al had. Bevestig altijd in het account.</p>
</div></section>
<div class="container article-layout"><article class="article">
<h2>KAKOSEP — pack 1300 CNY ≈ 167 € + 10 % extra verzending</h2>
<p>Campagne 2 van <a href="https://www.kakobuy.com/tipdetail?id=55" target="_blank" rel="noopener noreferrer">kakobuy.com/tipdetail?id=55</a>. Duur: <strong>8–30.9.2026</strong> (Peking-tijd). Op 16.9 kun je nog inwisselen.</p>
<p>Code: <strong>KAKOSEP</strong>. Pad: User Center → Coupons → Redeem. De spreadsheet past de code niet toe.</p>
<p>Het pack bevat (drempels in CNY vracht, volgens Kakobuy):</p>
<ul>
<li>1 × 10 % verzending, zonder minimum</li>
<li>1 × 300 CNY als verzending boven 2000 CNY is</li>
<li>1 × 200 CNY boven 1500 CNY</li>
<li>1 × 150 CNY boven 1000 CNY</li>
<li>2 × 100 CNY boven 800 CNY</li>
<li>3 × 80 CNY boven 500 CNY</li>
<li>3 × 50 CNY boven 300 CNY</li>
<li>2 × 30 CNY boven 21 CNY</li>
</ul>
<p>Percentages stapelen niet: wissel het pack in en kies bij checkout de coupon die het meest scheelt. Meerdere coupons combineren kan Kakobuy beperken — check de wallet.</p>
<h2>Nieuwe gebruiker 3000 CNY ≈ 386 €</h2>
<p>Officieel op Kakobuy.com: registreer en ontvang een couponpack (ongeveer 3000 CNY / 410 USD). Ze verschijnen in de wallet, vaak voor verzending.</p>
<p>Registreer via <a class="text-link" href="https://ikako.vip/r/yze69" target="_blank" rel="sponsored noopener noreferrer">ikako.vip/r/yze69</a>. Bron: <a href="https://www.kakobuy.com/tipdetail?id=1" target="_blank" rel="noopener noreferrer">kakobuy.com/tipdetail?id=1</a>.</p>
<h2>Sitewide-subsidie 10 % — krediet tot 31.10.2026</h2>
<p>Campagne 1 op dezelfde pagina: venster om de subsidie te <em>krijgen</em> 8–14.9.2026 (Peking-tijd). Kakobuy zegt dat al toegekend krediet tot <strong>31.10.2026</strong> kan. 16.9 is niet meer het inschrijfvenster; check wallet en productpagina.</p>
<h2>EU-lijnen</h2>
<p>Kakobuy adverteert duty-free lijnen naar de EU en <strong>3 € recht per zending</strong> op in aanmerking komende posten. De algemene btw in Nederland blijft 21 %. Zie de <a href="/kakobuy-verzending/">verzendgids</a>.</p>
<h2>Vrienden uitnodigen / Share &amp; earn</h2>
<p>Cashprijzen en invites zijn Kakobuy-accountcampagnes. Ze wissel je niet in op deze site.</p>
<p><a class="button" href="https://www.kakobuy.com/tipdetail?id=55" target="_blank" rel="noopener noreferrer">September Savings / KAKOSEP openen</a>
<a class="button secondary" href="https://ikako.vip/r/yze69" target="_blank" rel="sponsored noopener noreferrer">Registreren</a></p>
</article></div>
"""
    return wrap(
        "kakobuy-coupon",
        "Kakobuy coupon 2026 – KAKOSEP 1300 CNY en pack 3000 CNY",
        "Kakobuy coupons voor Nederland: code KAKOSEP (pack 1300 CNY + 10 % verzending tot 30.9) en pack 3000 CNY voor nieuwe gebruikers. Bevestig op Kakobuy.",
        body,
        og_type="article",
    )


def page_qc() -> str:
    body = """
<section class="article-hero"><div class="container">
<h1>Kakobuy QC-foto’s</h1>
<p>Controlefoto’s worden gemaakt als het product in het warehouse is, vóór internationale verzending.</p>
</div></section>
<div class="container article-layout"><article class="article">
<p>Vergelijk kleur, maattag, aantal, naden en zichtbare gebreken. Keur foto’s niet blind goed. Klopt er iets niet, open een ticket vóór je de lijn betaalt.</p>
<p>QC bewijst geen authenticiteit. Het helpt te voorkomen dat je een verkeerde kleur, maat of beschadigd stuk naar Nederland stuurt.</p>
<p><a class="text-link" href="/how-to-use-kakobuy/#stap-4">QC in de koopgids</a></p>
</article></div>
"""
    return wrap(
        "kakobuy-qc",
        "Kakobuy QC – warehousefoto’s lezen",
        "Kakobuy QC-foto’s: waar je op let in warehousebeelden vóór verzending naar Nederland.",
        body,
        og_type="article",
    )


def page_ervaringen() -> str:
    body = f"""
<section class="article-hero"><div class="container">
<h1>Kakobuy ervaringen — is Kakobuy betrouwbaar?</h1>
<p>Deze pagina verzint geen sterren. Betrouwbaarheid beslis je in het account, op QC-foto’s en op de verzendlijn.</p>
</div></section>
<div class="container article-layout"><article class="article">
<p>Kakobuy is een werkende inkoopagent: kopen, opslaan, fotograferen, verzenden. kakospreadsheet.nl is Kakobuy niet en vervangt de support niet.</p>
<ul>
<li>Betaal met een methode met kopersbescherming.</li>
<li>Lees QC vóór internationale verzending.</li>
<li>Neem community-hype niet als kwaliteitscertificaat.</li>
<li>BTW 21 % en Nederlandse douane zijn invoerregels, geen «Kakobuy-bug».</li>
</ul>
{faq_list_html(FAQ)}
<p><a class="button" href="/is-kakobuy-legit/">Is Kakobuy legit?</a>
<a class="button secondary" href="/how-to-use-kakobuy/">Aankoopstappen</a></p>
</article></div>
"""
    return wrap(
        "kakobuy-ervaringen",
        "Kakobuy ervaringen (2026) — betrouwbaar of niet?",
        "Kakobuy reviews en ervaringen voor Nederland: is Kakobuy betrouwbaar? Geen verzonnen scores. Check QC, betaling en douane zelf.",
        body,
        og_type="article",
        json_ld=[json_ld_faq("Kakobuy ervaringen", f"{BASE}/kakobuy-ervaringen/", FAQ)],
    )


def page_legit() -> str:
    body = f"""
<section class="article-hero"><div class="container">
<h1>Is Kakobuy legit?</h1>
<p>Engelse zoekvraag. Voor Nederlands detail: ervaringen en betrouwbaar.</p>
</div></section>
<div class="container article-layout"><article class="article">
<p>Kakobuy is a working purchasing agent. kakospreadsheet.nl is not Kakobuy support. Pay with buyer protection, read QC photos, and budget Dutch import VAT at 21 %.</p>
<p>Kakobuy is een werkende inkoopagent. Betaal met kopersbescherming, lees QC, en reken op invoer-btw van 21 %.</p>
{faq_list_html(FAQ[-2:])}
<p><a class="button" href="/kakobuy-ervaringen/">Kakobuy ervaringen</a>
<a class="button secondary" href="/kakobuy-verzending/">Verzending en BTW</a></p>
</article></div>
"""
    return wrap(
        "is-kakobuy-legit",
        "Is Kakobuy legit? — notities voor Nederland",
        "Is Kakobuy legit voor kopers in Nederland? Onafhankelijke notities: QC, betalingsbescherming en BTW 21 %.",
        body,
        og_type="article",
    )


def page_safe() -> str:
    body = """
<section class="article-hero"><div class="container">
<h1>Is Kakobuy safe?</h1>
<p>Praktische veiligheid zit in de betaalmethode, QC-foto’s en lijnrestricties niet negeren.</p>
</div></section>
<div class="container article-layout"><article class="article">
<p>Deze site verwerkt geen betalingen. Gebruik kopersbescherming op Kakobuy en keur QC niet blind goed.</p>
<p><a class="text-link" href="/kakobuy-ervaringen/">Betrouwbaarheidsgids in het Nederlands</a></p>
</article></div>
"""
    return wrap(
        "is-kakobuy-safe",
        "Is Kakobuy safe? — Nederland",
        "Is Kakobuy safe: betaal met bescherming, lees QC en check verzendrestricties naar Nederland.",
        body,
        og_type="article",
    )


def page_discord() -> str:
    body = """
<section class="article-hero"><div class="container">
<h1>Kakobuy Discord en chats</h1>
<p>Communityservers zijn niet officieel. Behandel QC-screenshots als anekdotes, geen certificaat. Hetzelfde voor Telegram.</p>
</div></section>
<div class="container article-layout"><article class="article">
<p>Gebruik de spreadsheet en Kakobuy QC-foto’s als aankoopdossier. Discord-, Telegram- of Reddit-threads kunnen verouderd of promocontent zijn.</p>
<p><a class="button" href="/kakobuy-ervaringen/">Betrouwbaarheidsnotities</a></p>
</article></div>
"""
    return wrap(
        "kakobuy-discord",
        "Kakobuy Discord — onofficiële chats",
        "Kakobuy Discord en Telegram: onofficiële communities. Beslissingen komen uit warehouse-QC en Kakobuy-support.",
        body,
        og_type="article",
    )


SPELL_FAQ: list[tuple[str, str]] = [
    (
        "Wat is het verschil tussen kako buy en Kakobuy?",
        "Alleen de spelling. Kakobuy is één woord. Veel mensen typen kako buy, kako-buy of kako buy spreadsheet.",
    ),
    (
        "Waar is de kako spreadsheet?",
        "De live catalogus is /kakobuy-spreadsheet/. URL’s kako-spreadsheet en kako-buy-spreadsheet leiden naar deze spellinghub, daarna naar de catalogus.",
    ),
    (
        "Heb ik een account nodig op kakospreadsheet.nl?",
        "Nee. Account, betaling en vracht gaan via Kakobuy. Deze site list links en legt BTW 21 % en Nederlandse douane uit.",
    ),
]


def page_kako_buy() -> str:
    body = f"""
<section class="article-hero"><div class="container">
<span class="eyebrow">Spelling · kako buy / kako-buy</span>
<h1>Kako buy, dat is Kakobuy</h1>
<p>Zocht je kako buy, kako-buy of kako buy spreadsheet, dan ben je goed: de agent heet <strong>Kakobuy</strong>. De Nederlandse catalogus staat op deze site.</p>
</div></section>
<div class="container article-layout"><article class="article">
<p>Spaties en koppeltekens breken de merknaam. Kakobuy is een inkoopagent: je plakt een Weidian-/Taobao-/1688-link, het warehouse ontvangt, je leest QC, daarna betaal je een lijn naar Nederland.</p>
<ul class="check-list">
<li><strong>kako buy</strong> en <strong>kako-buy</strong> → hetzelfde platform als Kakobuy.</li>
<li><strong>kako buy spreadsheet</strong> en <strong>kako-buy spreadsheet</strong> → de linkcatalogus, geen bevroren Google Sheet.</li>
<li>Registratie en betaling alleen op Kakobuy, niet hier.</li>
</ul>
<p>Producttabel: <a href="/kakobuy-spreadsheet/">Kakobuy spreadsheet</a>. Catalogusspelling: <a href="/kako-spreadsheet/">kako spreadsheet</a>.</p>
{faq_list_html(SPELL_FAQ)}
<p><a class="button" href="https://ikako.vip/r/yze69" target="_blank" rel="sponsored noopener noreferrer">Registreren op Kakobuy</a>
<a class="button secondary" href="/how-to-use-kakobuy/">Hoe kopen</a></p>
</article></div>
"""
    return wrap(
        "kako-buy",
        "Kako buy / kako-buy — dat is Kakobuy (Nederland)",
        "Kako buy en kako-buy betekenen Kakobuy. Gids Nederland: registratie, spreadsheet, QC en verzending. Ook voor kako buy spreadsheet.",
        body,
        og_type="article",
        json_ld=[json_ld_faq("Kako buy", f"{BASE}/kako-buy/", SPELL_FAQ)],
    )


def page_kako_spreadsheet() -> str:
    body = f"""
<section class="article-hero"><div class="container">
<span class="eyebrow">Spelling · kako spreadsheet</span>
<h1>Kako spreadsheet, kako-spreadsheet, kako-buy spreadsheet</h1>
<p>Deze zoekopdrachten bedoelen de <strong>Kakobuy spreadsheet</strong>: een catalogus productlinks, met indicatieve prijzen in euro, die op Kakobuy opent.</p>
</div></section>
<div class="container article-layout"><article class="article">
<p>Een Kakobuy-«spreadsheet» is geen Excel-bestand om hier te downloaden. Het is een doorzoekbare lijst: naam, categorie, euro-schatting, knop naar Kakobuy. Varianten <strong>kako spreadsheet</strong>, <strong>kako-spreadsheet</strong> en <strong>kako-buy spreadsheet</strong> wijzen naar dezelfde flow.</p>
<ul class="check-list">
<li>Zoek op naam of plak een Weidian-link in de catalogus.</li>
<li>Prijzen zijn van CNY omgerekend (ECB), zonder vracht en BTW 21 %.</li>
<li>QC, KAKOSEP-coupons en de NL-lijn regel je in het Kakobuy-account.</li>
</ul>
<p>URL’s <code>/kako-buy-spreadsheet/</code> en <code>/kako-spreadsheets/</code> verwijzen naar deze pagina om spelling te bundelen; daarna open je de live catalogus.</p>
{faq_list_html(SPELL_FAQ)}
<p><a class="button" href="/kakobuy-spreadsheet/">Kakobuy spreadsheet openen</a>
<a class="button secondary" href="/kako-buy/">Kako buy = Kakobuy</a></p>
</article></div>
"""
    return wrap(
        "kako-spreadsheet",
        "Kako spreadsheet / kako-spreadsheet — Kakobuy-catalogus Nederland",
        "Kako spreadsheet, kako-spreadsheet en kako-buy spreadsheet: de Kakobuy spreadsheet Nederland, doorzoekbaar, prijzen in euro.",
        body,
        og_type="article",
        json_ld=[json_ld_faq("Kako spreadsheet", f"{BASE}/kako-spreadsheet/", SPELL_FAQ)],
    )


def page_about() -> str:
    body = """
<section class="article-hero"><div class="container">
<h1>Praktische gids voor kopers in Nederland</h1>
<p>Hoe Kakobuy gebruiken, hoe verzending werkt, en productlinks. Bijgewerkt 16 september 2026.</p>
</div></section>
<div class="container article-layout"><article class="article">
<h2>Wat hier staat</h2>
<p>kakospreadsheet.nl is een onafhankelijke Nederlandstalige gids om Kakobuy te gebruiken. We leggen aankoopstappen, warehousefoto’s en het kiezen van een lijn naar Nederland uit. We listen ook productvoorbeelden en links. De site vangt ook zoekopdrachten kako buy, kako spreadsheet en best kakobuy spreadsheet.</p>
<h2>Hoe de links werken</h2>
<p>Productlinks openen de fiche op Kakobuy. Check variant, prijs en voorraad daar vóór je bestelt.</p>
<p>Op kakospreadsheet.nl koop of betaal je niet. We hebben geen klantdossiers en runnen geen warehouse of transport.</p>
<h2>Onafhankelijkheid en affiliate</h2>
<p>Wij zijn niet de officiële site of de support van Kakobuy. Sommige links bevatten een affiliatecode. Als de voorwaarden kloppen, kan deze site commissie ontvangen. Details: <a href="/affiliate-disclosure/">affiliate-vermelding</a>.</p>
<h2>Prijzen lezen</h2>
<p>Bedragen in euro zijn schattingen, geen verkoopaanbod op deze site. Een product kiezen betekent niet dat we het hebben getest of authenticiteit hebben geverifieerd.</p>
</article></div>
"""
    return wrap(
        "about",
        "Over kakospreadsheet.nl",
        "kakospreadsheet.nl is een onafhankelijke gids voor Nederland over Kakobuy: kopen, QC en verzending.",
        body,
        og_type="article",
    )


def page_privacy() -> str:
    body = """
<section class="article-hero"><div class="container"><h1>Privacy</h1>
<p>Deze site is een statische gids. We openen geen klantdossiers en nemen geen bestellingen aan.</p></div></section>
<div class="container article-layout"><article class="article">
<p>Technische cookies of serverlogs kunnen nodig zijn om te werken. Aankoop en betaling gebeuren op Kakobuy, onder hun voorwaarden.</p>
<p>Mail je ons, dan gebruiken we het bericht alleen om te antwoorden.</p>
</article></div>
"""
    return wrap(
        "privacy-policy",
        "Privacy – Kakobuy Spreadsheet Nederland",
        "Privacybeleid van kakospreadsheet.nl: statische gids, geen accounts op deze site.",
        body,
        og_type="article",
    )


def page_affiliate() -> str:
    body = """
<section class="article-hero"><div class="container"><h1>Affiliate-vermelding</h1>
<p>Productlinks naar Kakobuy kunnen een affiliatecode bevatten.</p></div></section>
<div class="container article-layout"><article class="article">
<p>Als je via een link bestelt en de voorwaarden kloppen, kunnen we commissie ontvangen. Jouw prijs stijgt daardoor niet. Wij zijn niet de officiële Kakobuy-site.</p>
<p>De catalogus is geen kwaliteitscertificaat. Check prijs, variant, voorraad en invoerregels vóór je betaalt.</p>
</article></div>
"""
    return wrap(
        "affiliate-disclosure",
        "Affiliate-vermelding – Kakobuy Spreadsheet Nederland",
        "kakospreadsheet.nl gebruikt affiliatelinks. Commissie verhoogt jouw prijs niet.",
        body,
        og_type="article",
    )


def page_partner() -> str:
    body = """
<section class="article-hero"><div class="container"><h1>Partner disclosure</h1>
<p>Zelfde affiliatevoorwaarden als de Nederlandse vermelding.</p></div></section>
<div class="container article-layout"><article class="article">
<p>Zie de <a href="/affiliate-disclosure/">affiliate-vermelding</a>.</p>
</article></div>
"""
    return wrap(
        "partner-disclosure",
        "Partner disclosure – Kakobuy Spreadsheet Nederland",
        "Partner disclosure voor kakospreadsheet.nl. Zie de Nederlandse affiliatepagina.",
        body,
        og_type="article",
    )


def page_contact() -> str:
    body = """
<section class="article-hero"><div class="container">
<h1>Contact</h1>
<p>Deze site beheert geen Kakobuy-bestellingen. Orderproblemen horen bij Kakobuy-support.</p>
</div></section>
<div class="container article-layout"><article class="article">
<p>Vragen over deze site: <a href="mailto:support@kakobuytips.com">support@kakobuytips.com</a></p>
<p>Kakobuy helpcentrum: <a href="https://www.kakobuy.com/help" target="_blank" rel="noopener noreferrer">kakobuy.com/help</a></p>
</article></div>
"""
    return wrap(
        "contact",
        "Contact – Kakobuy Spreadsheet Nederland",
        "Contact van kakospreadsheet.nl. Bestellingen lopen via Kakobuy.",
        body,
        og_type="article",
    )


def page_terms() -> str:
    body = """
<section class="article-hero"><div class="container"><h1>Voorwaarden</h1>
<p>Deze site publiceert een onafhankelijke catalogus en gids. Het is geen winkel.</p></div></section>
<div class="container article-layout"><article class="article">
<p>De inhoud is algemene informatie. Kakobuy-voorwaarden gelden voor accounts, betalingen, warehouse en vracht. Invoerregels zijn die van de Nederlandse autoriteiten.</p>
<p>Zie ook de <a href="/affiliate-disclosure/">affiliate-vermelding</a> en <a href="/privacy-policy/">privacy</a>.</p>
</article></div>
"""
    return wrap(
        "terms",
        "Voorwaarden – Kakobuy Spreadsheet Nederland",
        "Voorwaarden van kakospreadsheet.nl: onafhankelijke gids, geen winkel.",
        body,
        og_type="article",
    )


def page_404() -> str:
    return f"""<!doctype html>
<html lang="nl-NL"><head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Pagina niet gevonden – Kakobuy Spreadsheet Nederland</title>
<meta name="robots" content="noindex">
<link rel="stylesheet" href="{esc(asset("assets/styles.css"))}">
<link rel="stylesheet" href="{esc(asset("assets/layout.css"))}">
<link rel="stylesheet" href="{esc(asset("assets/fi.css"))}">
</head><body>
<main class="article-hero"><div class="container">
<h1>Pagina niet gevonden</h1>
<p>Open de spreadsheet of ga terug naar home.</p>
<p><a class="button" href="/kakobuy-spreadsheet/">Spreadsheet</a>
<a class="button secondary" href="/">Home</a></p>
</div></main>
</body></html>
"""


def redirect_html(target: str) -> str:
    return f"""<!doctype html>
<html lang="nl-NL"><head>
<meta charset="utf-8">
<title>Doorverwijzen…</title>
<link rel="canonical" href="{esc(BASE + target)}">
<meta http-equiv="refresh" content="0;url={esc(target)}">
<script>location.replace({json.dumps(target)});</script>
</head><body><p><a href="{esc(target)}">Doorgaan</a></p></body></html>
"""


def write_page(out_dir: Path, slug: str, html: str) -> None:
    if slug.endswith(".html"):
        (out_dir / slug).write_text(html, encoding="utf-8")
        return
    if not slug:
        (out_dir / "index.html").write_text(html, encoding="utf-8")
        return
    dest = out_dir / slug
    dest.mkdir(parents=True, exist_ok=True)
    (dest / "index.html").write_text(html, encoding="utf-8")


def write_sitemap(out_dir: Path) -> None:
    urls = []
    for slug in PRIMARY_SLUGS:
        loc = canonical(slug)
        urls.append(
            f"  <url>\n    <loc>{xml_esc(loc)}</loc>\n    <lastmod>{TODAY}</lastmod>\n    <changefreq>weekly</changefreq>\n  </url>"
        )
    xml = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "\n".join(urls)
        + "\n</urlset>\n"
    )
    (out_dir / "sitemap.xml").write_text(xml, encoding="utf-8")


def write_robots(out_dir: Path) -> None:
    (out_dir / "robots.txt").write_text(
        "User-agent: *\nAllow: /\n\n" f"Sitemap: {BASE}/sitemap.xml\n",
        encoding="utf-8",
    )


def write_manifest(out_dir: Path) -> None:
    data = {
        "name": "Kakobuy Spreadsheet Nederland",
        "short_name": "Kakobuy.nl",
        "start_url": "/",
        "display": "browser",
        "lang": "nl-NL",
        "icons": [
            {"src": "/assets/favicon-v2-32.png", "sizes": "32x32", "type": "image/png"},
            {"src": "/assets/apple-touch-icon-v2.png", "sizes": "180x180", "type": "image/png"},
        ],
    }
    (out_dir / "site.webmanifest").write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def assert_quality(out_dir: Path) -> None:
    home = (out_dir / "index.html").read_text(encoding="utf-8")
    sheet = (out_dir / "kakobuy-spreadsheet" / "index.html").read_text(encoding="utf-8")
    ship = (out_dir / "kakobuy-verzending" / "index.html").read_text(encoding="utf-8")
    kako = (out_dir / "kako-buy" / "index.html").read_text(encoding="utf-8")
    kako_sheet = (out_dir / "kako-spreadsheet" / "index.html").read_text(encoding="utf-8")
    php = (out_dir / "api" / "products.php").read_text(encoding="utf-8")
    for bad in (
        "Search intent",
        "W2CLinks",
        "fansheets.com",
        "kakobuydocs.com",
        "ALV 24%",
        "CBSA",
        "Agencia Tributaria",
        "España",
        "pour la France",
        "TVA 20",
        "20 %",
        "Abrir en Kakobuy",
        "Ouvrir sur Kakobuy",
        "como-comprar-en-kakobuy",
        "livraison-kakobuy",
        "avis-kakobuy",
    ):
        blob = home + sheet + ship + kako + kako_sheet
        if bad in blob:
            raise SystemExit(f"NL local site still contains {bad!r}")
    if 'lang="nl-NL"' not in home:
        raise SystemExit("home missing lang=nl-NL")
    if "/api/products.php" not in sheet:
        raise SystemExit("spreadsheet missing products API config")
    if "$_GET['q']" not in php or "item_id" not in php:
        raise SystemExit("products.php missing live search fields")
    if "Openen op Kakobuy" not in sheet:
        raise SystemExit("spreadsheet missing Kakobuy CTA")
    if "21 %" not in ship and "21%" not in ship:
        raise SystemExit("shipping page missing 21% VAT")
    if "belastingdienst.nl" not in ship:
        raise SystemExit("shipping page missing belastingdienst.nl")
    if "Spreadsheet" not in home or "Verzending" not in home:
        raise SystemExit("Netherlands nav missing")
    if "betrouwbaar" not in (out_dir / "kakobuy-ervaringen" / "index.html").read_text(encoding="utf-8"):
        raise SystemExit("ervaringen page missing betrouwbaar")
    if "kb-promo" not in home or "kakobuy-logo.png" not in (out_dir / "assets" / "fi.css").read_text(
        encoding="utf-8"
    ):
        raise SystemExit("NL site missing Kakobuy promo strip or official logo")
    if "3000 CNY" not in home or "KAKOSEP" not in home:
        raise SystemExit("home missing latest Kakobuy coupon promo")
    if "w2clinks.com/spreadsheet" in home:
        raise SystemExit("NL home still sends catalog traffic to W2CLinks spreadsheet")
    if "kako buy" not in kako.lower() or "kako-buy" not in kako:
        raise SystemExit("kako-buy lander missing misspelling copy")
    if "kako spreadsheet" not in kako_sheet.lower():
        raise SystemExit("kako-spreadsheet lander missing misspelling copy")
    redir = (out_dir / "best-kakobuy-spreadsheet" / "index.html").read_text(encoding="utf-8")
    if "/kakobuy-spreadsheet/" not in redir:
        raise SystemExit("best-kakobuy-spreadsheet should redirect to spreadsheet")
    if "Beste Kakobuy" not in sheet:
        raise SystemExit("spreadsheet missing beste kakobuy targeting")


def build_kakobuy_nl(out_dir: Path) -> int:
    catalog = load_catalog()
    RUNTIME["catalog"] = catalog
    RUNTIME["live"] = fetch_w2c_products(page=1, per_page=24)
    if out_dir.exists():
        shutil.rmtree(out_dir)
    out_dir.mkdir(parents=True)
    shutil.copytree(TEMPLATE_ASSETS, out_dir / "assets", ignore=shutil.ignore_patterns("products"))
    hero_src = NL_ASSETS / "hero.webp"
    if hero_src.is_file():
        shutil.copyfile(hero_src, out_dir / "assets" / "hero.webp")
    api_dir = out_dir / "api"
    api_dir.mkdir(parents=True)
    shutil.copyfile(API_PHP, api_dir / "products.php")

    pages = {
        "": page_home(catalog),
        "kakobuy-spreadsheet": page_spreadsheet(catalog),
        "kakobuy-finds": page_finds(catalog),
        "how-to-use-kakobuy": page_guide(),
        "kakobuy-verzending": page_shipping_nl(),
        "kakobuy-shipping": page_shipping_generic(),
        "kakobuy-coupon": page_coupon(),
        "kakobuy-qc": page_qc(),
        "kakobuy-ervaringen": page_ervaringen(),
        "is-kakobuy-legit": page_legit(),
        "is-kakobuy-safe": page_safe(),
        "kakobuy-discord": page_discord(),
        "kako-buy": page_kako_buy(),
        "kako-spreadsheet": page_kako_spreadsheet(),
        "about": page_about(),
        "privacy-policy": page_privacy(),
        "affiliate-disclosure": page_affiliate(),
        "partner-disclosure": page_partner(),
        "contact": page_contact(),
        "terms": page_terms(),
    }
    for slug, html in pages.items():
        write_page(out_dir, slug, html)

    for src, target in REDIRECTS.items():
        write_page(out_dir, src, redirect_html(target))

    (out_dir / "404.html").write_text(page_404(), encoding="utf-8")
    write_sitemap(out_dir)
    write_robots(out_dir)
    write_manifest(out_dir)
    assert_quality(out_dir)
    return len(pages) + len(REDIRECTS) + 1


if __name__ == "__main__":
    dest = ROOT / "dist" / DOMAIN
    n = build_kakobuy_nl(dest)
    print(f"Built {n} kakospreadsheet.nl files → {dest}")
