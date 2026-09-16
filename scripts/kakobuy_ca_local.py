"""Build kakospreadsheet.ca as a CZ-style local catalog site (CAD, Canada UX)."""

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

CATALOG_PATH = ROOT / "data" / "kakobuy-ca-catalog.json"
TEMPLATE_ASSETS = ROOT / "templates" / "kakobuy-fi" / "assets"
CA_ASSETS = ROOT / "templates" / "kakobuy-ca" / "assets"
API_PHP = ROOT / "templates" / "api" / "products.php"
DOMAIN = "kakospreadsheet.ca"
BASE = f"https://{DOMAIN}"
TODAY = date.today().isoformat()
ASSET_V = "20260915b"
RUNTIME: dict = {}

NAV = [
    ("", "Home"),
    ("kakobuy-spreadsheet", "Spreadsheet"),
    ("kakobuy-finds", "Finds"),
    ("how-to-use-kakobuy", "How to buy"),
    ("kakobuy-shipping-to-canada", "Shipping"),
    ("kakobuy-coupons", "Coupons"),
]

PRIMARY_SLUGS = [
    "",
    "kakobuy-spreadsheet",
    "kakobuy-finds",
    "how-to-use-kakobuy",
    "kakobuy-shipping-to-canada",
    "kakobuy-coupons",
    "kakobuy-qc",
    "is-kakobuy-legit",
    "kakobuy-canada",
    "kakobuy-warehouse",
    "kakobuy-payment-methods",
    "kakobuy-tracking",
    "kakobuy-discord",
    "about",
    "privacy-policy",
    "affiliate-disclosure",
    "contact",
    "terms",
]

REDIRECTS = {
    "kakobuy-spreadsheets": "/kakobuy-spreadsheet/",
    "kakobuy-coupon": "/kakobuy-coupons/",
    "kakobuy-shipping": "/kakobuy-shipping-to-canada/",
    "kakobuy-shipping-calculator": "/kakobuy-shipping-to-canada/",
    "is-kakobuy-safe": "/is-kakobuy-legit/",
    "kakobuy-review": "/is-kakobuy-legit/",
    "partner-disclosure": "/affiliate-disclosure/",
    "how-long-does-kakobuy-take-to-ship": "/kakobuy-shipping-to-canada/",
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
    "locale": "en-CA",
    "product": "Product",
    "productOne": "1 product",
    "products": "products",
    "other": "Other",
    "priceOnKakobuy": "Price on Kakobuy",
    "openOnKakobuy": "Open on Kakobuy ↗",
    "openAria": "Open {title} on Kakobuy (new tab)",
    "openAriaCard": "{title} — open on Kakobuy",
    "prev": "Previous",
    "next": "Next",
    "pageOf": "Page {current} / {pages}",
    "loadError": "Products could not be loaded. Try again in a moment.",
    "emptyCount": "0 products",
}


def load_catalog() -> dict:
    return json.loads(CATALOG_PATH.read_text(encoding="utf-8"))


def cat_map(catalog: dict) -> dict[str, dict]:
    return {c["id"]: c for c in catalog["categories"]}


def cad_amount(cny: float | int | None, cad_per_cny: float) -> int | None:
    try:
        return int(round(float(cny) * cad_per_cny))  # type: ignore[arg-type]
    except (TypeError, ValueError):
        return None


def format_cad(cny: float | int | None, cad_per_cny: float) -> str:
    amount = cad_amount(cny, cad_per_cny)
    return "Price on Kakobuy" if amount is None else f"≈ C${amount}"


def format_cny(cny: float | int | None) -> str:
    try:
        value = float(cny)  # type: ignore[arg-type]
    except (TypeError, ValueError):
        return ""
    if value.is_integer():
        return f"{int(value)} CNY"
    return f"{value} CNY"


def format_count(n: int) -> str:
    return f"{n:,}"


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
        groups.setdefault(str(cat.get("group") or "Other"), []).append(cat)
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
        "currency": "CAD",
        "cadPerCny": catalog.get("cad_per_cny", 0.2067),
        "cnyPerCad": catalog.get("cny_per_cad", 4.838),
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
        "kakobuy-canada",
        "kakobuy-shipping-to-canada",
        "kakobuy-warehouse",
        "kakobuy-payment-methods",
        "kakobuy-tracking",
        "kakobuy-discord",
        "terms",
    }
    path = "/" if not slug else f"/{slug}/"
    if slug in exclusive:
        loc = canonical(slug)
        return (
            f'<link rel="alternate" hreflang="en-CA" href="{esc(loc)}">\n'
            f'<link rel="alternate" hreflang="x-default" href="{esc(loc)}">'
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
<html lang="en-CA">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(description)}">
<link rel="canonical" href="{esc(canonical_url)}">
{hreflang_tags(slug)}
<meta property="og:site_name" content="Kakobuy Spreadsheet Canada">
<meta property="og:type" content="{esc(og_type)}">
<meta property="og:locale" content="en_CA">
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
<a class="skip-link" href="#content">Skip to content</a>
<div class="kb-promo"><div class="container">KAKOSEP until 30 Sep: ¥1300 pack + extra 10% off shipping · new users 3000 CNY · <a href="https://ikako.vip/r/yze69" target="_blank" rel="sponsored noopener noreferrer">Register on Kakobuy</a></div></div>
<header class="site-header"><div class="container nav">
<a class="brand" href="/" aria-label="Kakobuy Spreadsheet Canada – home"><span class="brand-mark">K</span><span>Kakobuy <small>Canada</small></span></a>
<form class="kb-head-search" action="/kakobuy-spreadsheet/" method="get" role="search">
<label class="sr-only" for="kb-q">Search products</label>
<input id="kb-q" type="search" name="q" placeholder="Search a product or paste a link" autocomplete="off">
<button type="submit">Search</button>
</form>
<div class="nav-actions">
<a class="button small" href="https://ikako.vip/r/yze69" target="_blank" rel="sponsored noopener noreferrer">Register</a>
<button class="menu-button" type="button" aria-label="Open menu" aria-expanded="false">☰</button>
</div>
</div></header>
<nav class="kb-subnav" aria-label="Main"><div class="container nav-links">{"".join(links)}</div></nav>
<main id="content">"""


def footer() -> str:
    return f"""</main>
<footer class="site-footer"><div class="container">
<div class="footer-grid">
<div><a class="brand" href="/"><span class="brand-mark">K</span><span>Kakobuy Canada</span></a>
<p class="footer-copy">Independent English-Canada product catalog and buying guide for Kakobuy.</p></div>
<div class="footer-col"><strong>Guide</strong>
<a href="/how-to-use-kakobuy/">How to buy</a>
<a href="/kakobuy-shipping-to-canada/">Shipping to Canada</a>
<a href="/is-kakobuy-legit/">Is Kakobuy legit?</a></div>
<div class="footer-col"><strong>Products</strong>
<a href="/kakobuy-spreadsheet/">Spreadsheet</a>
<a href="/kakobuy-finds/">Finds</a>
<a href="/kakobuy-coupons/">Coupons</a></div>
<div class="footer-col"><strong>Info</strong>
<a href="/about/">About</a>
<a href="/privacy-policy/">Privacy</a>
<a href="/affiliate-disclosure/">Affiliate disclosure</a></div>
</div>
<div class="footer-bottom"><span>© <span data-year></span> kakospreadsheet.ca</span>
<span>Not the official Kakobuy website.</span></div>
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
            "name": "Kakobuy Spreadsheet Canada",
            "url": f"{BASE}/",
            "inLanguage": "en-CA",
            "description": "Kakobuy spreadsheet for Canada: product links, CAD estimates, QC and shipping notes.",
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
            "inLanguage": "en-CA",
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
    label = (cats.get(p["category"]) or {}).get("label") or p["category"] or "Other"
    rate = catalog["cad_per_cny"]
    href = kakobuy_url(p["item_id"], catalog["affcode"], p.get("shop") or "weidian")
    cny = format_cny(p.get("price_cny"))
    return (
        f'<li class="sheet-product" data-product-id="{esc(p["id"])}" data-category="{esc(p["category"])}">'
        f'<img src="{esc(image_src(p["image"]))}" width="750" height="750" alt="{esc(p["title"])}" loading="lazy" decoding="async">'
        f'<div class="sheet-product-info"><span>{esc(label)}</span><h2>{esc(p["title"])}</h2></div>'
        f'<div class="sheet-price"><strong>{esc(format_cad(p.get("price_cny"), rate))}</strong>'
        f'<small>{esc(cny)}</small></div>'
        f'<a class="sheet-buy" href="{esc(href)}" target="_blank" rel="sponsored noopener noreferrer" '
        f'aria-label="Open {esc(p["title"])} on Kakobuy (new tab)">Open on Kakobuy ↗</a></li>'
    )


def finds_card(p: dict, catalog: dict, cats: dict) -> str:
    label = (cats.get(p["category"]) or {}).get("label") or p["category"] or "Other"
    rate = catalog["cad_per_cny"]
    href = kakobuy_url(p["item_id"], catalog["affcode"], p.get("shop") or "weidian")
    brand = f'<p class="catalog-advice">{esc(p["brand"])}</p>' if p.get("brand") else ""
    cny = format_cny(p.get("price_cny"))
    return f"""<article class="catalog-card" data-product-id="{esc(p["id"])}">
<a class="catalog-image" href="{esc(href)}" target="_blank" rel="sponsored noopener noreferrer" aria-label="{esc(p["title"])} — open on Kakobuy">
<img src="{esc(image_src(p["image"]))}" width="750" height="750" alt="{esc(p["title"])}" loading="lazy" decoding="async"><span>{esc(label)}</span></a>
<div class="catalog-body">
<h3>{esc(p["title"])}</h3>
<div class="catalog-meta"><strong>{esc(format_cad(p.get("price_cny"), rate))}</strong><small>{esc(cny)}</small></div>
{brand}
<a class="text-link" href="{esc(href)}" target="_blank" rel="sponsored noopener noreferrer">Open on Kakobuy ↗</a>
</div></article>"""


def rate_note(catalog: dict) -> str:
    return (
        f'Prices and links checked <time datetime="{esc(catalog["checked"])}">{esc(catalog["checked"])}</time>. '
        f'Bank of Canada rate <time datetime="{esc(catalog["boc_date"])}">{esc(catalog["boc_date"])}</time>: '
        f'1 CNY ≈ {catalog["cad_per_cny"]} CAD, rounded to the nearest dollar. '
        "That is the catalog product price without international shipping, fees, GST, duty or brokerage. "
        "Confirm the selected variant on Kakobuy before you pay."
    )


FAQ: list[tuple[str, str]] = [
    (
        "What is Kakobuy?",
        "Kakobuy is a buying and shipping agent. It orders from supported Chinese marketplaces, receives the item in a warehouse, takes QC photos, then offers international lines to Canada.",
    ),
    (
        "Does kakospreadsheet.ca sell products?",
        "No. This site is an independent catalog and affiliate guide. Purchase, payment and shipping happen on Kakobuy and with the sellers.",
    ),
    (
        "How much is shipping to Canada?",
        "It depends on actual or volumetric weight, dimensions, line and contents. The live quote appears on your Kakobuy account after items are in the warehouse.",
    ),
    (
        "What do QC photos mean?",
        "Warehouse photos taken before international shipping. Use them to check colour, size tags, quantity and visible defects.",
    ),
    (
        "Will I pay GST and duty in Canada?",
        "Usually yes on commercial parcels from China. Plan for GST (5%) plus possible duty, provincial tax and courier brokerage. Kakobuy may offer tax-prepaid lines — confirm at checkout. See CBSA for current rules.",
    ),
    (
        "Is Kakobuy legit?",
        "Kakobuy is a working agent platform. This site is not Kakobuy and does not guarantee price, quality or clearance. Pay with buyer protection, read QC photos and check line restrictions.",
    ),
]


def page_home(catalog: dict) -> str:
    cats = cat_map(catalog)
    found, live = RUNTIME.get("live") or (0, [])
    featured = live[:8]
    rate = catalog["cad_per_cny"]
    count_label = f"{format_count(found)}+" if found else "Thousands of"
    cat_count = len(catalog["categories"])
    cards = []
    for p in featured:
        href = kakobuy_url(p["item_id"], catalog["affcode"], p.get("shop") or "weidian")
        label = (cats.get(p["category"]) or {}).get("label") or p["category"] or "Other"
        cards.append(
            f'<a class="card catalog-card" href="{esc(href)}" target="_blank" rel="sponsored noopener noreferrer">'
            f'<div class="catalog-image"><img src="{esc(image_src(p["image"]))}" alt="{esc(p["title"])}" width="640" height="640" loading="lazy">'
            f"<span>{esc(label)}</span></div>"
            f'<div class="catalog-body"><h3>{esc(p["title"])}</h3>'
            f'<div class="catalog-meta"><strong>{esc(format_cad(p.get("price_cny"), rate))}</strong>'
            f'<small>{esc(format_cny(p.get("price_cny")))}</small></div></div></a>'
        )
    body = f"""
<section class="hero"><div class="container hero-grid">
<div class="hero-copy">
<span class="eyebrow">Product links · prices in CAD</span>
<h1>Kakobuy Spreadsheet<br><span class="gradient-text">for Canada</span></h1>
<p>Browse the catalog in one place. Search by name, filter a category and compare CAD estimates. The product you pick opens on Kakobuy.</p>
<form class="kb-hero-search" action="/kakobuy-spreadsheet/" method="get" role="search">
<label class="sr-only" for="hero-q">Search the spreadsheet</label>
<input id="hero-q" type="search" name="q" placeholder="Search a product, brand or paste a Weidian link" autocomplete="off">
<button type="submit">Search</button>
</form>
<div class="hero-actions">
<a class="button" href="/kakobuy-spreadsheet/">Open spreadsheet <span aria-hidden="true">→</span></a>
<a class="button secondary" href="/how-to-use-kakobuy/">How buying works</a>
</div>
<div class="trust-row" aria-label="Benefits">
<span><i class="check">✓</i> No account on this site</span>
<span><i class="check">✓</i> Prices in CAD</span>
<span><i class="check">✓</i> Canada shipping notes</span>
</div>
</div>
<div class="hero-visual hero-art">
<img class="hero-art-image" src="{esc(asset('assets/hero.webp'))}" width="1152" height="864" alt="Kakobuy shipping to Canada: warehouse, QC and parcel" fetchpriority="high">
</div>
</div></section>
<section class="kb-offers"><div class="container">
<div class="section-heading"><p class="kicker">Kakobuy.com · September 2026</p>
<h2>Current offers</h2>
<p>Official Kakobuy campaigns. Terms, discount and dates are confirmed on your account before payment.</p></div>
<div class="kb-offer-grid">
<a class="kb-offer" href="https://www.kakobuy.com/tipdetail?id=55" target="_blank" rel="noopener noreferrer">
<span class="kb-offer-tag">Code KAKOSEP</span>
<strong>September pack 1300 CNY ≈ C$269 + extra 10% off shipping</strong>
<p>Redeem 8–30 Sep 2026 (Beijing time). On Kakobuy: User Center → Coupons → Redeem, code <strong>KAKOSEP</strong>.</p>
<span class="text-link">Open campaign on Kakobuy ↗</span></a>
<a class="kb-offer" href="https://ikako.vip/r/yze69" target="_blank" rel="sponsored noopener noreferrer">
<span class="kb-offer-tag">New user</span>
<strong>3000 CNY coupon bundle ≈ C$620</strong>
<p>Register with the invite link. Coupons appear in the wallet; browsing the spreadsheet does not apply them automatically.</p>
<span class="text-link">Register ↗</span></a>
<a class="kb-offer" href="https://www.kakobuy.com/tipdetail?id=55" target="_blank" rel="noopener noreferrer">
<span class="kb-offer-tag">10% subsidy</span>
<strong>Credit from 8–14 Sep, usable until 31 Oct 2026</strong>
<p>The window to earn the sitewide subsidy has closed. If Kakobuy already granted it, they say it can be used until 31 Oct 2026.</p>
<span class="text-link">See rules on Kakobuy ↗</span></a>
<a class="kb-offer" href="/kakobuy-shipping-to-canada/">
<span class="kb-offer-tag">Canada</span>
<strong>CBSA, GST and duty-aware lines</strong>
<p>Most China parcels to Canada are assessed for GST and may face duty or brokerage. Compare tax-prepaid lines on Kakobuy.</p>
<span class="text-link">Shipping to Canada →</span></a>
</div>
</div></section>
<section class="stats"><div class="container stats-grid">
<div class="stat"><strong>{esc(count_label)} products</strong><span>Searchable catalog on this site</span></div>
<div class="stat"><strong>{cat_count} categories</strong><span>From sneakers to accessories</span></div>
<div class="stat"><strong>Prices in CAD</strong><span>Estimates, without shipping</span></div>
</div></section>
<section class="section"><div class="container">
<div class="section-heading"><p class="kicker">Latest finds</p>
<h2>Shoes, clothing and accessories with Kakobuy links</h2>
<p>Search the full list by name or limit it to one category.</p></div>
<div class="catalog-grid">{"".join(cards)}</div>
<p class="catalog-note">We are not the seller · check price and stock before ordering
<a class="text-link" href="/kakobuy-spreadsheet/">Kakobuy Spreadsheet · search the full catalog →</a></p>
<p class="catalog-price-note">{rate_note(catalog)}</p>
</div></section>
<section class="section soft"><div class="container">
<div class="section-heading"><h2>Catalog, order and shipping</h2>
<p>Wider catalog, the buying steps and costs into Canada.</p></div>
<div class="card-grid">
<a class="card" href="/kakobuy-spreadsheet/"><div class="card-icon">▦</div><h3>Spreadsheet</h3>
<p>Categories and product links when you do not want to browse Chinese marketplaces for an hour.</p>
<span class="text-link">Open catalog ↗</span></a>
<a class="card" href="/how-to-use-kakobuy/"><div class="card-icon">1</div><h3>First order</h3>
<p>What you pay now, what you pay in the warehouse, and why QC photos should not be approved blindly.</p></a>
<a class="card" href="/kakobuy-shipping-to-canada/"><div class="card-icon">→</div><h3>Shipping to Canada</h3>
<p>Actual vs volumetric weight, consolidation, tracking, GST, duty and CBSA.</p></a>
</div></div></section>
<section class="section"><div class="container">
<div class="section-heading"><h2>Buying in six steps</h2>
<p>The item reaches the warehouse first. You choose the Canada line only after photos.</p></div>
<div class="steps">
<div class="step"><h3>Find a product</h3><p>Pick a spreadsheet link or a marketplace URL.</p></div>
<div class="step"><h3>Paste the link</h3><p>Choose variant, size, colour and quantity.</p></div>
<div class="step"><h3>Pay for the item</h3><p>After payment the seller ships to Kakobuy’s warehouse.</p></div>
<div class="step"><h3>Do not skip QC</h3><p>Compare colour, tags, quantity and visible defects.</p></div>
<div class="step"><h3>Ship the parcel</h3><p>Consolidate items and pick a line to Canada.</p></div>
<div class="step"><h3>Track the shipment</h3><p>Follow the tracking number after the parcel is handed off.</p></div>
</div></div></section>
<section class="section soft"><div class="container split">
<div><h2>The spreadsheet is a map, not a quality stamp</h2>
<p>The catalog lives on this site. On each offer you still choose Kakobuy as the buying agent.</p>
<ul class="check-list"><li>Less manual hunting</li><li>Link to the original offer</li><li>No price or quality guarantee</li></ul></div>
<div>{faq_list_html(FAQ[:4])}</div>
</div></section>
<section class="cta"><div class="container"><div class="cta-box">
<h2>Already have a product link?</h2>
<p>Paste it into Kakobuy search. If you still need ideas, start with the spreadsheet.</p>
<a class="button" href="/kakobuy-spreadsheet/">Browse the catalog</a>
</div></div></section>
"""
    json_ld_blocks = [json_ld_website()]
    if featured:
        json_ld_blocks.append(json_ld_itemlist("Product catalog", featured, catalog))
    return wrap(
        "",
        "Kakobuy Spreadsheet Canada – products, CAD prices and QC",
        "Kakobuy spreadsheet for Canada: search by name, filter categories, CAD estimates and links that open on Kakobuy. Independent buying guide.",
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
    count_label = f"{format_count(found)} products" if found else "Loading…"
    body = f"""
<section class="container sheet-intro"><p class="kicker">Canadian catalog · searchable</p>
<h1>Kakobuy Spreadsheet for Canada</h1>
<p>This is the Kakobuy spreadsheet Canadian buyers can actually search: live product links, CAD estimates and a Kakobuy checkout — not a frozen screenshot of someone else’s Google Sheet.</p></section>
<section class="container sheet-content" aria-label="Product list">
<div class="sheet-controls">
<div class="sheet-field"><label for="sheet-search">Search products</label>
<input type="search" id="sheet-search" placeholder="e.g. hoodie, backpack, Jordan" autocomplete="off" aria-controls="sheet-products"></div>
<div class="sheet-field"><label for="sheet-category">Category</label>
<select id="sheet-category" aria-controls="sheet-products"><option value="all">All categories</option>{options}</select></div>
<button type="button" class="sheet-reset">Clear filters</button>
<output id="sheet-count" aria-live="polite">{esc(count_label)}</output>
</div>
<p class="sheet-disclosure">Prices are estimates without shipping and other fees. Product links are affiliate links; we may earn a commission.</p>
<ul id="sheet-products" class="sheet-products">{items}</ul>
<nav id="sheet-pager" class="sheet-pager" aria-label="Pagination" hidden></nav>
<p class="sheet-empty" role="status" hidden>No product found. Try a shorter name or another category.</p>
<details class="sheet-method"><summary>Prices and check date</summary>
<p>{rate_note(catalog)}</p>
<p>Photos and names come from the offers. We have not physically tested the items; authenticity and warehouse stock are not confirmed here. <a href="/affiliate-disclosure/">Affiliate disclosure</a></p>
</details>
</section>
<section class="section soft" id="categories"><div class="container">
<div class="section-heading"><h2>Browse by category</h2>
<p>Pick a category to filter this page. The product still opens on Kakobuy.</p></div>
<div class="sheet-categories">{extra}</div>
</div></section>
<section class="section"><div class="container sheet-help">
<div><h2>What is a Kakobuy spreadsheet?</h2>
<p>A product-link list that helps you shop through Kakobuy. You browse this catalog in the browser; each row has a category and a CAD estimate.</p>
<p>Want cards instead of a list? See <a href="/kakobuy-finds/">Kakobuy Finds</a>.</p></div>
<div><h2>What to do after you pick an item</h2>
<p>Open it on Kakobuy, check the variant and live price. When it is in the warehouse, review QC photos, then choose shipping to Canada.</p>
<p><a href="/how-to-use-kakobuy/">Step-by-step first-order guide</a> · <a href="/kakobuy-shipping-to-canada/">Shipping to Canada</a></p></div>
</div></section>
"""
    json_ld_blocks = []
    if live:
        json_ld_blocks.append(
            json_ld_itemlist("Kakobuy Spreadsheet – products with CAD prices", live[:24], catalog)
        )
    return wrap(
        "kakobuy-spreadsheet",
        "Kakobuy Spreadsheet – products with CAD prices",
        "Kakobuy spreadsheet for Canada: search by name, filter a category, compare CAD estimates and open the product on Kakobuy.",
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
<span class="eyebrow">Latest finds · CAD prices</span>
<h1>Kakobuy Finds</h1>
<p>Card view of the catalog. For faster search open the <a class="text-link" href="/kakobuy-spreadsheet/">Kakobuy Spreadsheet</a>.</p>
</div></section>
<section class="section finds-catalog"><div class="container">
<div class="catalog-context">
<p>Estimates without shipping and other fees. Links are affiliate links; we may earn a commission.</p>
<details><summary>Prices, check date and notes</summary>
<p>{rate_note(catalog)}</p></details>
</div>
<div class="catalog-filter" hidden>
<label for="catalog-category">Show category</label>
<select id="catalog-category"><option value="all">All categories</option>{options}</select>
<output id="catalog-count">{esc(format_count(_found) + " products") if _found else "Loading…"}</output>
</div>
<div id="finds-grid" class="catalog-grid">{cards}</div>
<p class="finds-empty sheet-empty" role="status" hidden>No product found in this category.</p>
<p class="catalog-price-note">{rate_note(catalog)}</p>
</div></section>
"""
    json_ld_blocks = []
    if live:
        json_ld_blocks.append(
            json_ld_itemlist("Kakobuy Finds – products with CAD prices", live[:24], catalog)
        )
    return wrap(
        "kakobuy-finds",
        "Kakobuy Finds – products with CAD prices",
        "Kakobuy Finds for Canada: latest product finds with CAD estimates and direct Kakobuy links.",
        body,
        extra_css=[asset("assets/catalog.css")],
        extra_js=[asset("assets/catalog-live.js"), asset("assets/finds.js")],
        json_ld=json_ld_blocks,
    )


def page_guide() -> str:
    body = """
<section class="article-hero"><div class="container">
<span class="eyebrow">6 steps for Canada</span>
<h1>How to buy through Kakobuy from Canada</h1>
<p>From creating an account to shipping the parcel. You do not create an account or place an order on kakospreadsheet.ca.</p>
</div></section>
<div class="container article-layout"><article class="article">
<p>Kakobuy sits between you and the seller. Goods do not come straight to your door: you pay for the item first, it arrives at the warehouse, you check photos, then you pay international shipping to Canada.</p>
<div class="article-callout"><strong>Before you click Pay</strong>Keep the original link ready, check the variant, and make sure the line accepts the goods and that you can legally import them into Canada.</div>
<h2 id="step-1">1. Create an account on Kakobuy</h2>
<p>Go to <a class="text-link" href="https://ikako.vip/r/yze69" target="_blank" rel="noopener noreferrer">Kakobuy registration</a> and choose Sign Up. Fill in email, pick a password and finish any verification the service asks for.</p>
<p>Registration can include a coupon offer. Check value and rules on the account; it is not automatically usable on every purchase.</p>
<h2 id="step-2">2. Find a product or paste a link</h2>
<p>Paste a copied product link or search by keyword. If you have a Taobao, 1688 or Weidian URL, paste it into Kakobuy search and confirm the right product loaded.</p>
<p>You can also start from <a class="text-link" href="/kakobuy-finds/">Finds</a> or the <a class="text-link" href="/kakobuy-spreadsheet/">spreadsheet</a>. A link is not a quality or stock confirmation.</p>
<h2 id="step-3">3. Choose the variant and pay for the order</h2>
<p>Pick colour, size and quantity. For clothing, follow the seller’s measurements, not just a Canadian letter size. The first payment is not the final door-to-door price. International shipping is paid later, once the warehouse knows weight and dimensions.</p>
<h2 id="step-4">4. Check QC photos in the warehouse</h2>
<p>When the item is in storage, open Warehouse and QC Picture. Compare colour, size tag, quantity and visible details with the order. QC shows visible issues; it does not prove authenticity by itself.</p>
<div class="article-callout"><strong>Something does not match?</strong>Raise it with support before international shipping.</div>
<h2 id="step-5">5. Add a Canadian address and choose a line</h2>
<p>Select the items to ship and add the correct address. Country must be <strong>Canada</strong>. Check name, street, city, province, postal code and phone; use country code <strong>+1</strong>.</p>
<p>Compare lines actually offered for this address and these goods. Decide on price, restrictions, size, weight and terms. More detail: <a class="text-link" href="/kakobuy-shipping-to-canada/">shipping guide for Canada</a>.</p>
<h2 id="step-6">6. Confirm shipment and track the parcel</h2>
<p>Before confirming, check address, contents, line and price. Fill customs details truthfully. After handoff, track the number on the Kakobuy account. The first scan is not always immediate.</p>
<h2 id="mistakes">Common mistakes</h2>
<ul><li>Wrong size without checking the measurement chart.</li><li>Skipping QC photos.</li><li>Budgeting only actual weight and forgetting volumetric weight.</li><li>Buying goods with a shipping or import restriction.</li><li>Inaccurate customs declarations.</li></ul>
<p class="legal-note">This is general information. Confirm live price, stock, shipping terms and import obligations on Kakobuy and with Canadian authorities before you pay.</p>
<p style="margin-top:30px"><a class="button" href="/kakobuy-finds/">Browse finds →</a></p>
</article>
<aside class="toc"><strong>Guide</strong>
<a href="#step-1">1. Create an account</a>
<a href="#step-2">2. Find a product</a>
<a href="#step-3">3. Variant and payment</a>
<a href="#step-4">4. Check QC</a>
<a href="#step-5">5. Canadian address</a>
<a href="#step-6">6. Ship and track</a>
<a href="#mistakes">Common mistakes</a></aside></div>
"""
    return wrap(
        "how-to-use-kakobuy",
        "How to use Kakobuy from Canada – step-by-step",
        "Complete English-Canada guide to buying with Kakobuy: product link, order, warehouse, QC photos and shipping to Canada.",
        body,
        og_type="article",
    )


def page_shipping() -> str:
    body = """
<section class="article-hero"><div class="container">
<span class="eyebrow">Shipping to Canada · updated 14 Sep 2026</span>
<h1>The cheapest line is not always the cheapest parcel</h1>
<p>Billable weight, dimensions, contents and what is included in the quote decide the real cost. Use this checklist when you compare offers.</p>
</div></section>
<div class="container article-layout"><article class="article">
<h2 id="flow">How shipping works</h2>
<p>Items from different sellers arrive at Kakobuy’s warehouse first. When they are ready, you choose what to send together, adjust packing, then compare the international lines offered to Canada.</p>
<h2 id="weight">Actual vs volumetric weight</h2>
<p>Carriers may bill actual weight or volumetric weight from dimensions. A light but bulky item can cost more because of volume. The divisor and rules vary by line.</p>
<div class="article-callout"><strong>Practical tip</strong>On bulky goods, consider removing extra boxes or vacuum bags if that will not damage the product.</div>
<h2 id="lines">How to compare lines</h2>
<ul>
<li>Price: compare the total, not only the first weight step.</li>
<li>Estimated time: an estimate, not a guaranteed day.</li>
<li>Content limits: some lines refuse batteries, liquids, cosmetics or certain materials.</li>
<li>Tracking and insurance: check how far tracking goes and what insurance covers.</li>
<li>Billing method: confirm actual vs volumetric weight.</li>
</ul>
<h2 id="bundle">Consolidation and packing</h2>
<p>Combining several items into one parcel can cut fixed fees, but a bigger box is not always cheaper. Fragile goods need protection; shoes or clothing can often ship without the original box if you ask.</p>
<h2 id="cbsa">GST, duty and CBSA in 2026</h2>
<p>Commercial parcels from China to Canada are usually assessed by the <strong>Canada Border Services Agency (CBSA)</strong>. Plan for federal <strong>GST at 5%</strong> on the dutiable value, plus possible <strong>customs duty</strong> depending on tariff classification, and provincial tax or HST if the courier collects it.</p>
<p>Low-value mail can be treated differently, but most Kakobuy hauls are above casual gift thresholds. Courier deliveries often add a <strong>brokerage fee</strong> on top of tax. Some Kakobuy lines advertise tax-prepaid or DDP-style delivery — read the line notes and still keep a buffer.</p>
<p>Current rules: <a href="https://www.cbsa-asfc.gc.ca/travel-voyage/declare-eng.html" target="_blank" rel="noopener noreferrer">CBSA – declaring goods ↗</a> · <a href="https://www.canada.ca/en/revenue-agency/services/tax/businesses/topics/gst-hst-businesses.html" target="_blank" rel="noopener noreferrer">CRA GST/HST ↗</a></p>
<h2 id="tracking">Tracking</h2>
<p>After the shipment is created you usually get a tracking number. A gap between label creation and the first physical scan is normal. Some routes update more clearly after arrival in Canada or handover to the last-mile carrier.</p>
<h2 id="check">Check before you pay freight</h2>
<ul>
<li>I have seen QC photos for every item.</li>
<li>I know the final weight and dimensions.</li>
<li>I have checked restrictions on the chosen line.</li>
<li>I understand insurance and tracking coverage.</li>
<li>I gave truthful details for transport and customs.</li>
</ul>
</article>
<aside class="toc"><strong>Contents</strong>
<a href="#flow">How shipping works</a>
<a href="#weight">Weight</a>
<a href="#lines">Choosing a line</a>
<a href="#bundle">Consolidation</a>
<a href="#cbsa">GST and duty</a>
<a href="#tracking">Tracking</a>
<a href="#check">Checklist</a></aside></div>
"""
    return wrap(
        "kakobuy-shipping-to-canada",
        "Kakobuy shipping to Canada – weight, GST and CBSA",
        "How Kakobuy shipping to Canada works: consolidation, actual vs volumetric weight, line choice, GST, duty, brokerage and tracking.",
        body,
        og_type="article",
    )


def page_coupon() -> str:
    body = """
<section class="article-hero"><div class="container">
<h1>Kakobuy coupons and campaigns</h1>
<p>Official on kakobuy.com on 15 Sep 2026: code <strong>KAKOSEP</strong> (¥1300 pack + extra 10% off shipping until 30 Sep), new-user 3000 CNY pack, and 10% subsidy credit usable until 31 Oct if already granted. Always confirm in the Kakobuy account.</p>
</div></section>
<div class="container article-layout"><article class="article">
<h2>KAKOSEP — ¥1300 pack ≈ C$269 + extra 10% off shipping</h2>
<p>Campaign 2 on <a href="https://www.kakobuy.com/tipdetail?id=55" target="_blank" rel="noopener noreferrer">kakobuy.com/tipdetail?id=55</a>. Duration: <strong>8–30 Sep 2026</strong> (Beijing time). It is still redeemable on 15 Sep.</p>
<p>Code: <strong>KAKOSEP</strong>. Path: User Center → Coupons → Redeem. This spreadsheet does not apply the code.</p>
<p>The pack includes (shipping thresholds in CNY, per Kakobuy):</p>
<ul>
<li>1 × 10% off shipping, no minimum</li>
<li>1 × ¥300 when shipping is over ¥2000</li>
<li>1 × ¥200 over ¥1500</li>
<li>1 × ¥150 over ¥1000</li>
<li>2 × ¥100 over ¥800</li>
<li>3 × ¥80 over ¥500</li>
<li>3 × ¥50 over ¥300</li>
<li>2 × ¥30 over ¥21</li>
</ul>
<p>Percentage coupons do not stack with each other: redeem the pack, then pick the coupon that saves more at checkout.</p>
<h2>New-user 3000 CNY ≈ C$620</h2>
<p>Official offer on Kakobuy.com: register and receive a coupon bundle (about 3000 CNY / 410 USD). Coupons show in the wallet, usually for shipping.</p>
<p>Register with invite link <a class="text-link" href="https://ikako.vip/r/yze69" target="_blank" rel="sponsored noopener noreferrer">ikako.vip/r/yze69</a>. Source: <a href="https://www.kakobuy.com/tipdetail?id=1" target="_blank" rel="noopener noreferrer">kakobuy.com/tipdetail?id=1</a>.</p>
<h2>10% sitewide subsidy — credit until 31 Oct 2026</h2>
<p>Campaign 1 on the same page: the window to <em>earn</em> the subsidy was 8–14 Sep 2026 (Beijing time). Kakobuy says granted credit can be used until <strong>31 Oct 2026</strong>. 15 Sep is after that signup window; check the wallet and the product page.</p>
<h2>Canada lines</h2>
<p>EU €3-per-parcel customs does not apply in Canada. Budget for GST, possible duty and brokerage, unless you pick a Kakobuy line that states tax is prepaid. See the <a href="/kakobuy-shipping-to-canada/">Canada shipping guide</a>.</p>
<h2>Invite friends / Share &amp; earn</h2>
<p>Cash prizes and friend invites are Kakobuy-account campaigns. They are not redeemed on this site.</p>
<p><a class="button" href="https://www.kakobuy.com/tipdetail?id=55" target="_blank" rel="noopener noreferrer">Open September Savings / KAKOSEP</a>
<a class="button secondary" href="https://ikako.vip/r/yze69" target="_blank" rel="sponsored noopener noreferrer">Register</a></p>
</article></div>
"""
    return wrap(
        "kakobuy-coupons",
        "Kakobuy coupon 2026 – KAKOSEP ¥1300 and 3000 CNY pack",
        "Kakobuy coupons for Canadian buyers: code KAKOSEP (¥1300 pack + extra 10% off shipping until 30 Sep) and new-user 3000 CNY bundle. Confirm the offer on Kakobuy.",
        body,
        og_type="article",
    )


def page_qc() -> str:
    body = """
<section class="article-hero"><div class="container">
<h1>Kakobuy QC photos</h1>
<p>Check photos are taken when the product has arrived at the warehouse — before international shipping.</p>
</div></section>
<div class="container article-layout"><article class="article">
<p>Compare colour, size tag, quantity, seams and visible defects. Do not approve photos blindly. If something is off, open a ticket before you pay the line.</p>
<p>QC does not prove authenticity. It helps you avoid shipping the wrong colour, wrong size or a damaged piece to Canada.</p>
<p><a class="text-link" href="/how-to-use-kakobuy/#step-4">See QC as part of the buying guide</a></p>
</article></div>
"""
    return wrap(
        "kakobuy-qc",
        "Kakobuy QC – how to read warehouse photos",
        "Kakobuy QC photos: what to look at in warehouse pictures before shipping to Canada.",
        body,
        og_type="article",
    )


def page_legit() -> str:
    body = f"""
<section class="article-hero"><div class="container">
<h1>Is Kakobuy legit?</h1>
<p>This page does not invent star ratings. Trust is decided on the account, in QC photos and on the shipping line.</p>
</div></section>
<div class="container article-layout"><article class="article">
<p>Kakobuy is a working purchasing agent: it buys, stores, photographs and ships. kakospreadsheet.ca is not Kakobuy and does not replace its support.</p>
<ul>
<li>Pay with a method that has buyer protection.</li>
<li>Read QC before international shipping.</li>
<li>Do not treat community hype as a quality certificate.</li>
<li>GST and CBSA charges in Canada are import rules, not a “Kakobuy bug”.</li>
</ul>
{faq_list_html(FAQ)}
<p><a class="button" href="/how-to-use-kakobuy/">Buying steps</a> <a class="button secondary" href="/kakobuy-shipping-to-canada/">Shipping and CBSA</a></p>
</article></div>
"""
    return wrap(
        "is-kakobuy-legit",
        "Is Kakobuy legit? (2026) — Canadian buyer notes",
        "Is Kakobuy legit for Canadian buyers? No fake ratings. Check QC, payment method and CBSA yourself.",
        body,
        og_type="article",
        json_ld=[json_ld_faq("Is Kakobuy legit?", f"{BASE}/is-kakobuy-legit/", FAQ)],
    )


def page_canada() -> str:
    body = """
<section class="article-hero"><div class="container">
<h1>Kakobuy Canada</h1>
<p>This .ca hub focuses on CAD estimates, Canada Post / courier delivery, QC in the warehouse, and the spreadsheet workflow before you ship.</p>
</div></section>
<div class="container article-layout"><article class="article">
<ul class="check-list">
<li>Start in the spreadsheet, pick 3–5 rows, request QC in the warehouse.</li>
<li>Read shipping and CBSA notes before a large haul.</li>
<li>Register only on Kakobuy, not on this site.</li>
</ul>
<p><a class="button" href="/kakobuy-spreadsheet/">Open spreadsheet</a>
<a class="button secondary" href="/kakobuy-shipping-to-canada/">Shipping and duty</a></p>
</article></div>
"""
    return wrap(
        "kakobuy-canada",
        "Kakobuy Canada — guide for Canadian buyers",
        "Kakobuy Canada: spreadsheet with CAD prices, QC and shipping to Canada.",
        body,
        og_type="article",
    )


def page_best() -> str:
    body = """
<section class="article-hero"><div class="container">
<h1>Best Kakobuy spreadsheet for Canada</h1>
<p>The useful spreadsheet is the one you can search here, with CAD estimates and links that open on Kakobuy — not a screenshot of someone else’s Google Sheet.</p>
</div></section>
<div class="container article-layout"><article class="article">
<p>Canadian shoppers searching “best kakobuy spreadsheet” usually want three things: live product links, a price they can compare in CAD, and a clear next step (QC, then a Canada line).</p>
<p>This site keeps the catalog on-page. You search by name or category, then open the offer on Kakobuy with the affiliate code already on the URL. We do not host 24 frozen Weidian SKUs as “the” list.</p>
<ul class="check-list">
<li>Search and category filters stay on kakospreadsheet.ca.</li>
<li>Prices are Bank of Canada conversions, labelled as estimates.</li>
<li>Checkout, coupons and freight still happen on Kakobuy.</li>
</ul>
<p><a class="button" href="/kakobuy-spreadsheet/">Open the live spreadsheet</a>
<a class="button secondary" href="/kakobuy-finds/">Card view</a></p>
</article></div>
"""
    return wrap(
        "best-kakobuy-spreadsheet",
        "Best Kakobuy spreadsheet (2026) — Canada catalog",
        "Best Kakobuy spreadsheet for Canada: searchable on-site catalog, CAD estimates and Kakobuy product links.",
        body,
        og_type="article",
    )


def page_warehouse() -> str:
    body = """
<section class="article-hero"><div class="container">
<h1>Kakobuy warehouse</h1>
<p>Items wait in storage until you submit an international parcel. That pause is where QC happens.</p>
</div></section>
<div class="container article-layout"><article class="article">
<p>“Storing” means the seller has delivered to Kakobuy and the item is available for photos, returns or consolidation. Storage windows and extra fees are set on Kakobuy — check the account, not this page, for the live clock.</p>
<p>Do not pay freight until you have reviewed QC for every piece you plan to include.</p>
<p><a class="text-link" href="/kakobuy-qc/">QC photo checklist</a> · <a class="text-link" href="/how-to-use-kakobuy/#step-4">Warehouse step in the guide</a></p>
</article></div>
"""
    return wrap(
        "kakobuy-warehouse",
        "Kakobuy warehouse — storage, QC and parcel submit",
        "What Kakobuy warehouse storage means: QC photos, consolidation, then shipping to Canada.",
        body,
        og_type="article",
    )


def page_payment() -> str:
    body = """
<section class="article-hero"><div class="container">
<h1>Kakobuy payment methods</h1>
<p>Pay on Kakobuy, not on this website. Prefer a method with buyer protection.</p>
</div></section>
<div class="container article-layout"><article class="article">
<p>Available cards, wallets and local methods change. Open the Kakobuy checkout to see what is offered on your account. This site never takes card details.</p>
<p>Coupons from the new-user pack usually apply in the Kakobuy wallet, often to shipping. They are not promo codes you type into this spreadsheet.</p>
<p><a class="button" href="https://ikako.vip/r/yze69" target="_blank" rel="sponsored noopener noreferrer">Register on Kakobuy</a></p>
</article></div>
"""
    return wrap(
        "kakobuy-payment-methods",
        "Kakobuy payment methods — pay on Kakobuy",
        "Kakobuy payment methods for Canadian buyers. Checkout stays on Kakobuy; this site does not take payments.",
        body,
        og_type="article",
    )


def page_tracking() -> str:
    body = """
<section class="article-hero"><div class="container">
<h1>Kakobuy tracking</h1>
<p>You get a tracking number after the international parcel is created — not when the seller ships to the warehouse.</p>
</div></section>
<div class="container article-layout"><article class="article">
<p>Warehouse inbound tracking and last-mile tracking are different numbers. Gaps of a few days after label creation are common on Canada routes.</p>
<p>If CBSA holds a parcel, the carrier notice or Kakobuy ticket is the source of truth, not a spreadsheet row.</p>
<p><a class="text-link" href="/kakobuy-shipping-to-canada/#tracking">Tracking notes in the shipping guide</a></p>
</article></div>
"""
    return wrap(
        "kakobuy-tracking",
        "Kakobuy tracking to Canada",
        "Kakobuy tracking for Canada: warehouse vs international number, scan gaps and CBSA holds.",
        body,
        og_type="article",
    )


def page_discord() -> str:
    body = """
<section class="article-hero"><div class="container">
<h1>Kakobuy Discord and community chats</h1>
<p>Community servers are unofficial. Treat QC screenshots there as anecdotes, not a certificate.</p>
</div></section>
<div class="container article-layout"><article class="article">
<p>Use the spreadsheet and Kakobuy QC photos as the buying record. Discord, Telegram or Reddit threads can be outdated or promotional.</p>
<p><a class="button" href="/is-kakobuy-legit/">Read the legit notes</a></p>
</article></div>
"""
    return wrap(
        "kakobuy-discord",
        "Kakobuy Discord — unofficial chats",
        "Kakobuy Discord and community chats are unofficial. Use warehouse QC and Kakobuy support for decisions.",
        body,
        og_type="article",
    )


def page_about() -> str:
    body = """
<section class="article-hero"><div class="container">
<h1>A practical guide for Canadian buyers</h1>
<p>How to use Kakobuy, how shipping works, and links to selected products. Updated 14 September 2026.</p>
</div></section>
<div class="container article-layout"><article class="article">
<h2>What you find here</h2>
<p>kakospreadsheet.ca is an independent English-Canada guide to Kakobuy. We explain the buying steps, warehouse photos and choosing a line to Canada. We also list product examples and links.</p>
<h2>How product links work</h2>
<p>Individual product links open Kakobuy’s item page. Check variant, price and stock there before you order.</p>
<p>You do not buy or pay on kakospreadsheet.ca. We have no customer accounts and we do not run warehouse or freight service.</p>
<h2>Independence and affiliate links</h2>
<p>This is not Kakobuy’s official site or support. Some links include an affiliate code. When terms are met, this site may earn a commission. Details: <a href="/affiliate-disclosure/">affiliate disclosure</a>.</p>
<h2>How to read prices</h2>
<p>CAD figures are estimates, not an offer for sale on this site. Picking a product does not mean we tested it or verified authenticity.</p>
</article></div>
"""
    return wrap(
        "about",
        "About kakospreadsheet.ca",
        "kakospreadsheet.ca is an independent Canadian guide to Kakobuy: buying, QC and shipping to Canada.",
        body,
        og_type="article",
    )


def page_privacy() -> str:
    body = """
<section class="article-hero"><div class="container"><h1>Privacy</h1>
<p>This site is a static guide. We do not open customer accounts or take orders.</p></div></section>
<div class="container article-layout"><article class="article">
<p>The site may use technical cookies or server logs to keep it running. Purchase and payment happen on Kakobuy, under Kakobuy’s terms.</p>
<p>If you email us, we use the message only to reply.</p>
</article></div>
"""
    return wrap(
        "privacy-policy",
        "Privacy – Kakobuy Spreadsheet Canada",
        "Privacy policy for kakospreadsheet.ca: static guide, no customer accounts on this site.",
        body,
        og_type="article",
    )


def page_affiliate() -> str:
    body = """
<section class="article-hero"><div class="container"><h1>Affiliate disclosure</h1>
<p>Product links to Kakobuy may include an affiliate code.</p></div></section>
<div class="container article-layout"><article class="article">
<p>If you order through a link and the terms are met, we may earn a commission. Your price does not increase because of that. We are not Kakobuy’s official site.</p>
<p>The catalog is not a quality certificate. Check price, variant, stock and import rules before you pay.</p>
</article></div>
"""
    return wrap(
        "affiliate-disclosure",
        "Affiliate disclosure – Kakobuy Spreadsheet Canada",
        "kakospreadsheet.ca uses affiliate links. A commission does not raise your price.",
        body,
        og_type="article",
    )


def page_contact() -> str:
    body = """
<section class="article-hero"><div class="container">
<h1>Contact</h1>
<p>This site does not handle Kakobuy orders. Order issues belong with Kakobuy support.</p>
</div></section>
<div class="container article-layout"><article class="article">
<p>Questions about this website: <a href="mailto:support@kakobuytips.com">support@kakobuytips.com</a></p>
<p>Kakobuy help centre: <a href="https://www.kakobuy.com/help" target="_blank" rel="noopener noreferrer">kakobuy.com/help</a></p>
</article></div>
"""
    return wrap(
        "contact",
        "Contact – Kakobuy Spreadsheet Canada",
        "kakospreadsheet.ca contact. Orders are handled on Kakobuy.",
        body,
        og_type="article",
    )


def page_terms() -> str:
    body = """
<section class="article-hero"><div class="container"><h1>Terms</h1>
<p>This website publishes an independent catalog and guide. It is not a store.</p></div></section>
<div class="container article-layout"><article class="article">
<p>Content is general information. Kakobuy’s own terms govern accounts, payments, warehouse storage and freight. Import rules are set by Canadian authorities.</p>
<p>See also the <a href="/affiliate-disclosure/">affiliate disclosure</a> and <a href="/privacy-policy/">privacy policy</a>.</p>
</article></div>
"""
    return wrap("terms", "Terms – Kakobuy Spreadsheet Canada", "Terms for kakospreadsheet.ca: independent guide, not a store.", body, og_type="article")


def page_404() -> str:
    return f"""<!doctype html>
<html lang="en-CA"><head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Page not found – Kakobuy Spreadsheet Canada</title>
<meta name="robots" content="noindex">
<link rel="stylesheet" href="{esc(asset("assets/styles.css"))}">
<link rel="stylesheet" href="{esc(asset("assets/layout.css"))}">
<link rel="stylesheet" href="{esc(asset("assets/fi.css"))}">
</head><body>
<main class="article-hero"><div class="container">
<h1>Page not found</h1>
<p>Open the spreadsheet or go back home.</p>
<p><a class="button" href="/kakobuy-spreadsheet/">Spreadsheet</a>
<a class="button secondary" href="/">Home</a></p>
</div></main>
</body></html>
"""


def redirect_html(target: str) -> str:
    return f"""<!doctype html>
<html lang="en-CA"><head>
<meta charset="utf-8">
<title>Redirecting…</title>
<link rel="canonical" href="{esc(BASE + target)}">
<meta http-equiv="refresh" content="0;url={esc(target)}">
<script>location.replace({json.dumps(target)});</script>
</head><body><p><a href="{esc(target)}">Continue</a></p></body></html>
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
        "name": "Kakobuy Spreadsheet Canada",
        "short_name": "Kakobuy.ca",
        "start_url": "/",
        "display": "browser",
        "lang": "en-CA",
        "icons": [
            {"src": "/assets/favicon-v2-32.png", "sizes": "32x32", "type": "image/png"},
            {"src": "/assets/apple-touch-icon-v2.png", "sizes": "180x180", "type": "image/png"},
        ],
    }
    (out_dir / "site.webmanifest").write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def assert_quality(out_dir: Path) -> None:
    home = (out_dir / "index.html").read_text(encoding="utf-8")
    sheet = (out_dir / "kakobuy-spreadsheet" / "index.html").read_text(encoding="utf-8")
    ship = (out_dir / "kakobuy-shipping-to-canada" / "index.html").read_text(encoding="utf-8")
    js = (out_dir / "assets" / "spreadsheet.js").read_text(encoding="utf-8")
    php = (out_dir / "api" / "products.php").read_text(encoding="utf-8")
    for bad in ("Search intent", "W2CLinks", "fansheets.com", "kakobuydocs.com", "ALV 24%", "24 tuotte"):
        if bad in home or bad in sheet or bad in ship:
            raise SystemExit(f"CA local site still contains {bad!r}")
    if 'lang="en-CA"' not in home:
        raise SystemExit("home missing lang=en-CA")
    if "/api/products.php" not in sheet:
        raise SystemExit("spreadsheet missing products API config")
    if "$_GET['q']" not in php or "item_id" not in php:
        raise SystemExit("products.php missing live search fields")
    if "Open on Kakobuy" not in js and "Open on Kakobuy" not in sheet:
        raise SystemExit("spreadsheet missing Kakobuy CTA")
    if "CBSA" not in ship:
        raise SystemExit("shipping page missing CBSA")
    if "GST" not in ship:
        raise SystemExit("shipping page missing GST")
    if "Spreadsheet" not in home or "Shipping" not in home:
        raise SystemExit("Canada nav missing")
    if "kb-promo" not in home or "kakobuy-logo.png" not in (out_dir / "assets" / "fi.css").read_text(encoding="utf-8"):
        raise SystemExit("CA site missing Kakobuy promo strip or official logo")
    if "3000 CNY" not in home or "KAKOSEP" not in home:
        raise SystemExit("home missing latest Kakobuy coupon promo")
    if "w2clinks.com/spreadsheet" in home:
        raise SystemExit("CA home still sends catalog traffic to W2CLinks spreadsheet")


def build_kakobuy_ca(out_dir: Path) -> int:
    catalog = load_catalog()
    RUNTIME["catalog"] = catalog
    RUNTIME["live"] = fetch_w2c_products(page=1, per_page=24)
    if out_dir.exists():
        shutil.rmtree(out_dir)
    out_dir.mkdir(parents=True)
    shutil.copytree(TEMPLATE_ASSETS, out_dir / "assets", ignore=shutil.ignore_patterns("products"))
    hero_src = CA_ASSETS / "hero.webp"
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
        "kakobuy-shipping-to-canada": page_shipping(),
        "kakobuy-coupons": page_coupon(),
        "kakobuy-qc": page_qc(),
        "is-kakobuy-legit": page_legit(),
        "kakobuy-canada": page_canada(),
        "best-kakobuy-spreadsheet": page_best(),
        "kakobuy-warehouse": page_warehouse(),
        "kakobuy-payment-methods": page_payment(),
        "kakobuy-tracking": page_tracking(),
        "kakobuy-discord": page_discord(),
        "about": page_about(),
        "privacy-policy": page_privacy(),
        "affiliate-disclosure": page_affiliate(),
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
    n = build_kakobuy_ca(dest)
    print(f"Built {n} kakospreadsheet.ca files → {dest}")
