"""Build kakobuy.fi as a CZ-style local catalog site (on-site finds, EUR, Finnish UX)."""

from __future__ import annotations

import json
import os
import re
import shutil
import ssl
import urllib.parse
import urllib.request
from datetime import date
from html import escape as esc
from pathlib import Path
from urllib.parse import quote
from xml.sax.saxutils import escape as xml_esc

ROOT = Path(__file__).resolve().parents[1]
CATALOG_PATH = ROOT / "data" / "kakobuy-fi-catalog.json"
TEMPLATE_ASSETS = ROOT / "templates" / "kakobuy-fi" / "assets"
API_PHP = ROOT / "templates" / "api" / "products.php"
DOMAIN = "kakobuy.fi"
BASE = f"https://{DOMAIN}"
TODAY = date.today().isoformat()
W2C_SEARCH = "https://w2clinks.com/public/typesense-search.php"
ITEM_RE = re.compile(r"(wd|tb|ali|1688)_(\d+)", re.I)
SSL_CTX = ssl.create_default_context()
SSL_CTX.check_hostname = False
SSL_CTX.verify_mode = ssl.CERT_NONE
RUNTIME: dict = {}

NAV = [
    ("", "Etusivu"),
    ("kakobuy-spreadsheet", "Spreadsheet"),
    ("kakobuy-finds", "Valitut tuotteet"),
    ("kuinka-kayttaa-kakobuyta", "Ostaminen"),
    ("kakobuy-toimitus", "Toimitus"),
    ("faq", "FAQ"),
]

PRIMARY_SLUGS = [
    "",
    "kakobuy-spreadsheet",
    "kakobuy-finds",
    "kuinka-kayttaa-kakobuyta",
    "kakobuy-toimitus",
    "faq",
    "about",
    "privacy-policy",
    "affiliate-disclosure",
    "kakobuy-coupon",
    "kakobuy-qc",
    "kakobuy-kokemuksia",
    "kakobuy-suomi",
    "contact",
]

REDIRECTS = {
    "spreadsheet.html": "/kakobuy-spreadsheet/",
    "finds.html": "/kakobuy-finds/",
    "guide.html": "/kuinka-kayttaa-kakobuyta/",
    "shipping.html": "/kakobuy-toimitus/",
    "faq.html": "/faq/",
    "about.html": "/about/",
    "privacy.html": "/privacy-policy/",
    "disclaimer.html": "/affiliate-disclosure/",
    "how-to-use-kakobuy": "/kuinka-kayttaa-kakobuyta/",
    "kakobuy-spreadsheets": "/kakobuy-spreadsheet/",
    "best-kakobuy-spreadsheet": "/kakobuy-spreadsheet/",
    "kakobuy-shipping": "/kakobuy-toimitus/",
    "kakobuy-coupons": "/kakobuy-coupon/",
    "is-kakobuy-legit": "/kakobuy-kokemuksia/",
    "is-kakobuy-safe": "/kakobuy-kokemuksia/",
    "kakobuy-review": "/kakobuy-kokemuksia/",
    "kakobuy-discord": "/faq/",
    "terms": "/affiliate-disclosure/",
    "partner-disclosure": "/affiliate-disclosure/",
    "kakobuy-shipping-calculator": "/kakobuy-toimitus/",
    "how-long-does-kakobuy-take-to-ship": "/kakobuy-toimitus/",
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
    return "Hinta Kakobuyssa" if amount is None else f"≈ {amount} €"


def format_cny(cny: float | int | None) -> str:
    try:
        value = float(cny)  # type: ignore[arg-type]
    except (TypeError, ValueError):
        return ""
    if value.is_integer():
        return f"{int(value)} CNY"
    return f"{str(value).replace('.', ',')} CNY"


def format_count(n: int) -> str:
    return f"{n:,}".replace(",", "\u00a0")


def parse_shop_item(url: str) -> tuple[str, str]:
    match = ITEM_RE.search(url or "")
    if not match:
        return "", ""
    prefix = match.group(1).lower()
    shop = "weidian" if prefix == "wd" else "taobao" if prefix == "tb" else "1688"
    return shop, match.group(2)


def source_url(shop: str, item_id: str) -> str:
    if not item_id:
        return ""
    if shop == "taobao":
        return f"https://item.taobao.com/item.htm?id={item_id}"
    if shop == "1688":
        return f"https://detail.1688.com/offer/{item_id}.html"
    return f"https://weidian.com/item.html?itemID={item_id}"


def kakobuy_url(item_id: str, affcode: str, shop: str = "weidian") -> str:
    src = source_url(shop, item_id)
    if not src:
        return "/kakobuy-spreadsheet/"
    return (
        "https://kakobuy.com/item/details?url="
        + quote(src, safe="")
        + f"&affcode={quote(affcode)}"
    )


def http_json(url: str, timeout: int = 20) -> dict | None:
    try:
        req = urllib.request.Request(
            url,
            headers={"User-Agent": "KakobuyFiBuilder/1.0", "Accept": "application/json"},
        )
        with urllib.request.urlopen(req, context=SSL_CTX, timeout=timeout) as resp:
            return json.loads(resp.read().decode("utf-8", errors="replace"))
    except Exception:
        return None


def normalize_hit(raw: dict) -> dict | None:
    shop, item_id = parse_shop_item(str(raw.get("url") or ""))
    if not item_id:
        return None
    title = str(raw.get("title") or "").strip()
    if not title:
        return None
    price = raw.get("price")
    if price is None:
        price = raw.get("price_cny")
    try:
        price_cny: float | None = float(price)
    except (TypeError, ValueError):
        price_cny = None
    return {
        "id": f"{shop}-{item_id}",
        "title": title,
        "item_id": item_id,
        "shop": shop,
        "image": str(raw.get("image") or ""),
        "price_cny": price_cny,
        "category": str(raw.get("category") or ""),
        "brand": str(raw.get("brand") or ""),
    }


def fetch_w2c_products(*, page: int = 1, per_page: int = 24, category: str = "", q: str = "") -> tuple[int, list[dict]]:
    params: dict[str, str | int] = {"page": page, "per_page": per_page, "sort": "newest"}
    if q:
        params["q"] = q
    if category:
        params["category"] = category
    key = os.environ.get("W2CLINKS_API_KEY", "").strip()
    if key:
        params["api_key"] = key
    data = http_json(W2C_SEARCH + "?" + urllib.parse.urlencode(params))
    if not data:
        return 0, []
    hits = []
    for row in data.get("hits") or []:
        if isinstance(row, dict):
            item = normalize_hit(row)
            if item:
                hits.append(item)
    return int(data.get("found") or len(hits)), hits


ASSET_V = "20260914c"


def asset(path: str) -> str:
    href = f"/{path.lstrip('/')}"
    if path.endswith((".js", ".css")):
        return f"{href}?v={ASSET_V}"
    return href


def image_src(path: str) -> str:
    if path.startswith(("http://", "https://", "/")):
        return path
    return asset(path)


def category_options_html(catalog: dict) -> str:
    groups: dict[str, list[dict]] = {}
    for cat in catalog["categories"]:
        groups.setdefault(str(cat.get("group") or "Muut"), []).append(cat)
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
        "cnyPerEur": catalog.get("cny_per_eur", 7.7762),
        "api": "/api/products.php",
        "categories": [{"id": c["id"], "label": c["label"]} for c in catalog.get("categories", [])],
    }
    return (
        "<script>window.KAKOBUY_FI="
        + json.dumps(payload, ensure_ascii=False, separators=(",", ":"))
        + ";</script>"
    )


def page_href(slug: str) -> str:
    return "/" if not slug else f"/{slug}/"


def canonical(slug: str) -> str:
    return f"{BASE}/" if not slug else f"{BASE}/{slug}/"


def head(
    *,
    title: str,
    description: str,
    canonical_url: str,
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
<html lang="fi">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(description)}">
<link rel="canonical" href="{esc(canonical_url)}">
<meta property="og:site_name" content="Kakobuy Suomi">
<meta property="og:type" content="{esc(og_type)}">
<meta property="og:locale" content="fi_FI">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(description)}">
<meta property="og:url" content="{esc(canonical_url)}">
<meta property="og:image" content="{BASE}/assets/hero.webp">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{esc(title)}">
<meta name="twitter:description" content="{esc(description)}">
<link rel="icon" href="/assets/favicon-v2-32.png" type="image/png" sizes="32x32">
<link rel="icon" href="/assets/favicon-v2-16.png" type="image/png" sizes="16x16">
<link rel="apple-touch-icon" href="/assets/apple-touch-icon-v2.png">
<link rel="manifest" href="/site.webmanifest">
<meta name="theme-color" content="#6548e8">
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
<a class="skip-link" href="#sisalto">Siirry sisältöön</a>
<div class="announcement">Riippumaton opas suomalaisille ostajille · <a href="/affiliate-disclosure/">Miten tämä sivusto toimii</a></div>
<header class="site-header"><div class="container nav">
<a class="brand" href="/" aria-label="Kakobuy Suomi – etusivu"><span class="brand-mark">K</span><span>Kakobuy <small>Suomi</small></span></a>
<nav class="nav-links" aria-label="Päävalikko">{"".join(links)}</nav>
<div class="nav-actions"><button class="menu-button" type="button" aria-label="Avaa valikko" aria-expanded="false">☰</button></div>
</div></header>
<main id="sisalto">"""


def footer() -> str:
    return f"""</main>
<footer class="site-footer"><div class="container">
<div class="footer-grid">
<div><a class="brand" href="/"><span class="brand-mark">K</span><span>Kakobuy Suomi</span></a>
<p class="footer-copy">Riippumaton suomenkielinen tuotevalikoima ja ohjeet Kakobuyn käyttöön.</p></div>
<div class="footer-col"><strong>Opas</strong>
<a href="/kuinka-kayttaa-kakobuyta/">Ostaminen</a>
<a href="/kakobuy-toimitus/">Toimitus</a>
<a href="/faq/">FAQ</a></div>
<div class="footer-col"><strong>Tuotteet</strong>
<a href="/kakobuy-spreadsheet/">Spreadsheet</a>
<a href="/kakobuy-finds/">Valitut tuotteet</a></div>
<div class="footer-col"><strong>Tiedot</strong>
<a href="/about/">Tietoa</a>
<a href="/privacy-policy/">Tietosuoja</a>
<a href="/affiliate-disclosure/">Kumppanuus</a></div>
</div>
<div class="footer-bottom"><span>© <span data-year></span> kakobuy.fi</span>
<span>Kakobuy.fi ei ole Kakobuyn virallinen sivusto.</span></div>
</div></footer>
<script src="{esc(asset("assets/site.js"))}" defer></script>
</body></html>"""


def wrap(slug: str, title: str, description: str, body: str, **head_kw) -> str:
    return (
        head(title=title, description=description, canonical_url=canonical(slug), **head_kw)
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
            "name": "Kakobuy Suomi",
            "url": f"{BASE}/",
            "inLanguage": "fi-FI",
            "description": "Kakobuy Spreadsheet Suomelle: tuotelinkit, suuntaa-antavat hinnat euroina ja suomenkieliset ostohjeet.",
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


def json_ld_faq(items: list[tuple[str, str]]) -> str:
    return json.dumps(
        {
            "@context": "https://schema.org",
            "@type": "FAQPage",
            "name": "Kakobuy FAQ suomalaisille",
            "url": f"{BASE}/faq/",
            "inLanguage": "fi-FI",
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
    label = (cats.get(p["category"]) or {}).get("label") or p["category"] or "Muut"
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
        f'aria-label="Avaa {esc(p["title"])} Kakobuyssa (uusi välilehti)">Avaa Kakobuyssa ↗</a></li>'
    )


def finds_card(p: dict, catalog: dict, cats: dict) -> str:
    label = (cats.get(p["category"]) or {}).get("label") or p["category"] or "Muut"
    rate = catalog["cny_per_eur"]
    href = kakobuy_url(p["item_id"], catalog["affcode"], p.get("shop") or "weidian")
    brand = f'<p class="catalog-advice">{esc(p["brand"])}</p>' if p.get("brand") else ""
    cny = format_cny(p.get("price_cny"))
    return f"""<article class="catalog-card" data-product-id="{esc(p["id"])}">
<a class="catalog-image" href="{esc(href)}" target="_blank" rel="sponsored noopener noreferrer" aria-label="{esc(p["title"])} – avaa Kakobuyssa">
<img src="{esc(image_src(p["image"]))}" width="750" height="750" alt="{esc(p["title"])}" loading="lazy" decoding="async"><span>{esc(label)}</span></a>
<div class="catalog-body">
<h3>{esc(p["title"])}</h3>
<div class="catalog-meta"><strong>{esc(format_eur(p.get("price_cny"), rate))}</strong><small>{esc(cny)}</small></div>
{brand}
<a class="text-link" href="{esc(href)}" target="_blank" rel="sponsored noopener noreferrer">Avaa Kakobuyssa ↗</a>
</div></article>"""


def format_fi_date(iso: str) -> str:
    try:
        y, m, d = iso.split("-")
        return f"{int(d)}.{int(m)}.{y}"
    except ValueError:
        return iso


def rate_note(catalog: dict) -> str:
    checked = format_fi_date(str(catalog.get("checked") or TODAY))
    ecb = format_fi_date(str(catalog.get("ecb_date") or TODAY))
    return (
        f'Hinnat ja linkit tarkistettu <time datetime="{esc(catalog["checked"])}">{esc(checked)}</time>. '
        f'Kurssi ECB:n mukaan <time datetime="{esc(catalog["ecb_date"])}">{esc(ecb)}</time>: '
        f'1 EUR ≈ {str(catalog["cny_per_eur"]).replace(".", ",")} CNY, pyöristetty euroon. '
        "Kyse on tuotteen katalogihinnasta ilman toimitusta, kuluja tai tuontimaksuja. "
        "Valitun variantin hinta kannattaa varmistaa Kakobuyssa."
    )


FAQ: list[tuple[str, str]] = [
    (
        "Mikä Kakobuy on?",
        "Kakobuy on osto- ja toimitusagentti. Se tilaa tuotteen tuetulta kiinalaiselta kauppapaikalta, vastaanottaa sen varastoon, ottaa tarkistuskuvat ja tarjoaa toimitusvaihtoehtoja kohdemaahan.",
    ),
    (
        "Myykö kakobuy.fi tuotteita?",
        "Ei. Tämä sivusto on riippumaton opas ja kumppanuuslinkkien keskittymä. Osto, maksu ja toimitus tapahtuvat Kakobuyssa ja myyjillä.",
    ),
    (
        "Mitä toimitus Suomeen maksaa?",
        "Hinta muuttuu todellisen tai tilavuuspainon, mittojen, linjan ja sisällön mukaan. Tarkka tarjous näkyy Kakobuy-tilillä, kun tuotteet ovat varastossa.",
    ),
    (
        "Mitä QC-kuvat tarkoittavat?",
        "Ne ovat varastossa otettuja tarkistuskuvia. Niistä näkee värin, koon, kappalemäärän ja näkyvät viat ennen kansainvälistä lähetystä.",
    ),
    (
        "Pitääkö ALV ja tulli hoitaa?",
        "Kyllä. EU:n ulkopuolelta tulevista lähetyksistä tehdään tulli-ilmoitus ja ALV 25,5 % ratkaistaan. 1.7.2026 alkaen useimpiin enintään 150 euron lähetyksiin tulee myös 3 euron tulli tulli nimikettä kohti. Katso ajantasaiset tiedot Tullilta.",
    ),
    (
        "Onko Kakobuy luotettava?",
        "Kakobuy on toimiva agenttialusta, ei tämä sivusto. Emme takaa hintaa, laatua emmekä tulliselvitystä. Maksa suojatulla tavalla, lue QC-kuvat ja tarkista linjan rajoitukset.",
    ),
]


def page_home(catalog: dict) -> str:
    cats = cat_map(catalog)
    found, live = RUNTIME.get("live") or (0, [])
    featured = live[:8]
    rate = catalog["cny_per_eur"]
    count_label = f"{format_count(found)}+" if found else "Tuhansia"
    cat_count = len(catalog["categories"])
    cards = []
    for p in featured:
        href = kakobuy_url(p["item_id"], catalog["affcode"], p.get("shop") or "weidian")
        label = (cats.get(p["category"]) or {}).get("label") or p["category"] or "Muut"
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
<span class="eyebrow">Tuotelinkit · hinnat euroina</span>
<h1>Kakobuy Spreadsheet<br><span class="gradient-text">Suomelle</span></h1>
<p>Selaa tuotevalikoimaa yhdessä paikassa. Hae nimellä, valitse kategoria ja vertaa suuntaa-antavia hintoja euroina. Valittu tuote avautuu suoraan Kakobuyssa.</p>
<div class="hero-actions">
<a class="button" href="/kakobuy-spreadsheet/">Avaa spreadsheet <span aria-hidden="true">→</span></a>
<a class="button secondary" href="/kuinka-kayttaa-kakobuyta/">Miten osto toimii</a>
</div>
<div class="trust-row" aria-label="Hyödyt">
<span><i class="check">✓</i> Ei rekisteröitymistä tällä sivustolla</span>
<span><i class="check">✓</i> Hinnat euroina</span>
<span><i class="check">✓</i> Suomenkieliset ohjeet</span>
</div>
</div>
<div class="hero-visual hero-art">
<img class="hero-art-image" src="/assets/hero.webp" width="1280" height="853" alt="Paketti, varaston QC-tarkistus ja toimitus Suomeen" fetchpriority="high">
<div class="hero-proof hero-proof-qc"><span class="hero-proof-icon">✓</span><span><strong>QC varastossa</strong><small>Kuvat ennen lähetystä</small></span></div>
<div class="hero-proof hero-proof-cz hero-proof-fi"><span class="hero-proof-icon">🇫🇮</span><span><strong>Toimitus Suomeen</strong><small>Valitset vasta tarkistuksen jälkeen</small></span></div>
</div>
</div></section>
<section class="stats"><div class="container stats-grid">
<div class="stat"><strong>{esc(count_label)} tuotetta</strong><span>Haettava katalogi tällä sivustolla</span></div>
<div class="stat"><strong>{cat_count} kategoriaa</strong><span>Kengistä asusteisiin</span></div>
<div class="stat"><strong>Hinnat euroina</strong><span>Suuntaa-antavasti, ilman toimitusta</span></div>
</div></section>
<section class="section"><div class="container">
<div class="section-heading"><p class="kicker">Uusimmat löydöt</p>
<h2>Kengät, vaatteet ja asusteet Kakobuy-linkeillä</h2>
<p>Koko listaa voi hakea nimen perusteella tai rajata yhteen kategoriaan.</p></div>
<div class="catalog-grid">{"".join(cards)}</div>
<p class="catalog-note">Emme ole myyjä · hinta ja saatavuus kannattaa tarkistaa ennen tilausta
<a class="text-link" href="/kakobuy-spreadsheet/">Kakobuy Spreadsheet · hae koko katalogista →</a></p>
<p class="catalog-price-note">{rate_note(catalog)}</p>
</div></section>
<section class="section soft"><div class="container">
<div class="section-heading"><h2>Katalogi, tilaus ja toimitus</h2>
<p>Laajempi valikoima, ostamisen vaiheet ja kustannukset Suomeen.</p></div>
<div class="card-grid">
<a class="card" href="/kakobuy-spreadsheet/"><div class="card-icon">▦</div><h3>Spreadsheet</h3>
<p>Kategoriat ja tuotelinkit, kun et halua selailla kiinalaisia kauppapaikkoja tunnin ajan.</p>
<span class="text-link">Avaa katalogi ↗</span></a>
<a class="card" href="/kuinka-kayttaa-kakobuyta/"><div class="card-icon">1</div><h3>Ensimmäinen tilaus</h3>
<p>Mitä maksetaan heti, mitä vasta varastossa, ja miksi QC-kuvia ei kannata kuitata sokeasti.</p></a>
<a class="card" href="/kakobuy-toimitus/"><div class="card-icon">→</div><h3>Toimitus Suomeen</h3>
<p>Todellinen vs. tilavuuspaino, yhdistäminen, seuranta sekä tulli ja ALV.</p></a>
</div></div></section>
<section class="section"><div class="container">
<div class="section-heading"><h2>Osto kuudessa vaiheessa</h2>
<p>Tuote saapuu ensin varastoon. Toimituksen Suomeen valitset vasta kuvien jälkeen.</p></div>
<div class="steps">
<div class="step"><h3>Löydä tuote</h3><p>Valitse linkki spreadsheetistä tai suoraan kauppapaikalta.</p></div>
<div class="step"><h3>Liitä linkki</h3><p>Valitse variantti, koko, väri ja määrä.</p></div>
<div class="step"><h3>Maksa tuote</h3><p>Maksun jälkeen myyjä lähettää tavaran Kakobuyn varastoon.</p></div>
<div class="step"><h3>Älä kuittaa QC:tä</h3><p>Vertaa väri, lappu, kappalemäärä ja näkyvät viat.</p></div>
<div class="step"><h3>Lähetä paketti</h3><p>Yhdistä tuotteet ja valitse sopiva linja Suomeen.</p></div>
<div class="step"><h3>Seuraa lähetystä</h3><p>Lähetyksen jälkeen seuraa pakettia seurantanumerolla.</p></div>
</div></div></section>
<section class="section soft"><div class="container split">
<div><h2>Spreadsheet on opaste, ei laatuleima</h2>
<p>Katalogi on tällä sivustolla. Yksittäisessä tarjouksessa valitset Kakobuyn ostoalustaksi.</p>
<ul class="check-list"><li>Vähemmän manuaalista etsintää</li><li>Linkki alkuperäiseen tarjoukseen</li><li>Ei hinta- tai laatutakuuta</li></ul></div>
<div>{faq_list_html(FAQ[:4])}</div>
</div></section>
<section class="cta"><div class="container"><div class="cta-box">
<h2>Onko sinulla tuotelinkki?</h2>
<p>Liitä se Kakobuyn hakuun. Jos etsit vielä ideoita, aloita spreadsheetistä.</p>
<a class="button" href="/kakobuy-spreadsheet/">Selaa katalogia</a>
</div></div></section>
"""
    json_ld_blocks = [json_ld_website()]
    if featured:
        json_ld_blocks.append(json_ld_itemlist("Tuotevalikoima", featured, catalog))
    return wrap(
        "",
        "Kakobuy Spreadsheet Suomi – tuotteet, hinnat ja ohjeet",
        "Kakobuy Spreadsheet Suomelle: tuotekatsaus, haku nimen mukaan, kategoriat ja hinnat euroina. Linkit Kakobuysyn ja suomenkielinen ohje ensimmäiseen tilaukseen.",
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
    count_label = f"{format_count(found)} tuotetta" if found else "Ladataan…"
    body = f"""
<section class="container sheet-intro"><p class="kicker">Suomalainen valikoima · haettava katalogi</p>
<h1>Kakobuy Spreadsheet Suomelle</h1>
<p>Tuotelinkit, kategoriat ja suuntaa-antavat hinnat euroina. Etsi tuote ja avaa tarjous suoraan Kakobuyssa.</p></section>
<section class="container sheet-content" aria-label="Tuotelista">
<div class="sheet-controls">
<div class="sheet-field"><label for="sheet-search">Hae tuotetta</label>
<input type="search" id="sheet-search" placeholder="Esim. paita, reppu, Jordan" autocomplete="off" aria-controls="sheet-products"></div>
<div class="sheet-field"><label for="sheet-category">Kategoria</label>
<select id="sheet-category" aria-controls="sheet-products"><option value="all">Kaikki kategoriat</option>{options}</select></div>
<button type="button" class="sheet-reset">Tyhjennä suodattimet</button>
<output id="sheet-count" aria-live="polite">{esc(count_label)}</output>
</div>
<p class="sheet-disclosure">Hinnat ovat suuntaa-antavia, ilman toimitusta ja muita kuluja. Tuotelinkit ovat kumppanuuslinkkejä; voimme saada provision.</p>
<ul id="sheet-products" class="sheet-products">{items}</ul>
<nav id="sheet-pager" class="sheet-pager" aria-label="Sivutus" hidden></nav>
<p class="sheet-empty" role="status" hidden>Tuotetta ei löytynyt. Kokeile lyhyempää nimeä tai toista kategoriaa.</p>
<details class="sheet-method"><summary>Hinnat ja tarkistuspäivä</summary>
<p>{rate_note(catalog)}</p>
<p>Kuvat ja nimet perustuvat tarjouksiin. Emme ole testanneet tuotteita fyysisesti; aitoutta tai varastosaatavuutta ei vahvisteta tällä. <a href="/affiliate-disclosure/">Kumppanuusilmoitus</a></p>
</details>
</section>
<section class="section soft" id="kategoriat"><div class="container">
<div class="section-heading"><h2>Selaa kategorioittain</h2>
<p>Valitse kategoria, niin lista suodattuu tällä sivulla. Tuote avautuu Kakobuyssa.</p></div>
<div class="sheet-categories">{extra}</div>
</div></section>
<section class="section"><div class="container sheet-help">
<div><h2>Mikä on Kakobuy spreadsheet?</h2>
<p>Tuotelinkkien lista, joka auttaa valitsemaan tavaraa Kakobuyn kautta. Tätä valikoimaa selaat selaimessa; kuvan vieressä on kategoria ja euromääräinen hinta.</p>
<p>Haluatko korttinäkymän? Katso <a href="/kakobuy-finds/">Kakobuy Finds</a>.</p></div>
<div><h2>Miten jatkaa valinnan jälkeen?</h2>
<p>Avaa tuote Kakobuyssa, tarkista variantti ja ajantasainen hinta. Kun tavara on varastossa, käy QC-kuvat läpi ja vasta sitten valitse toimitus Suomeen.</p>
<p><a href="/kuinka-kayttaa-kakobuyta/">Suomenkielinen ohje ensimmäiseen tilaukseen</a> · <a href="/kakobuy-toimitus/">Toimitus Suomeen</a></p></div>
</div></section>
"""
    json_ld_blocks = []
    if live:
        json_ld_blocks.append(
            json_ld_itemlist("Kakobuy Spreadsheet – tuotteet hinnoilla euroina", live[:24], catalog)
        )
    return wrap(
        "kakobuy-spreadsheet",
        "Kakobuy Spreadsheet – tuotteet hinnoilla euroina",
        "Kakobuy Spreadsheet Suomelle: hae nimen mukaan, suodata kategoriasta, vertaa hintoja euroina ja avaa tuote Kakobuyssa.",
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
<span class="eyebrow">Uusimmat löydöt · hinnat euroina</span>
<h1>Kakobuy Finds</h1>
<p>Korttinäkymä katalogista. Nopeaan hakuun avaa <a class="text-link" href="/kakobuy-spreadsheet/">Kakobuy Spreadsheet</a>.</p>
</div></section>
<section class="section finds-catalog"><div class="container">
<div class="catalog-context">
<p>Suuntaa-antavat hinnat ilman toimitusta ja muita kuluja. Linkit ovat kumppanuuslinkkejä; voimme saada provision.</p>
<details><summary>Hinnat, tarkistuspäivä ja tiedot</summary>
<p>{rate_note(catalog)}</p></details>
</div>
<div class="catalog-filter" hidden>
<label for="catalog-category">Näytä kategoria</label>
<select id="catalog-category"><option value="all">Kaikki kategoriat</option>{options}</select>
<output id="catalog-count">{esc(format_count(_found) + " tuotetta") if _found else "Ladataan…"}</output>
</div>
<div id="finds-grid" class="catalog-grid">{cards}</div>
<p class="finds-empty sheet-empty" role="status" hidden>Tuotetta ei löytynyt tähän kategoriaan.</p>
<p class="catalog-price-note">{rate_note(catalog)}</p>
</div></section>
"""
    json_ld_blocks = []
    if live:
        json_ld_blocks.append(
            json_ld_itemlist("Kakobuy Finds – tuotteet hinnoilla euroina", live[:24], catalog)
        )
    return wrap(
        "kakobuy-finds",
        "Kakobuy Finds – tuotteet hinnoilla euroina",
        "Kakobuy Finds Suomelle: uusimmat tuotelöydöt hinnoilla euroina ja suorilla Kakobuy-linkeillä.",
        body,
        extra_css=[asset("assets/catalog.css")],
        extra_js=[asset("assets/catalog-live.js"), asset("assets/finds.js")],
        json_ld=json_ld_blocks,
    )


def page_guide() -> str:
    body = """
<section class="article-hero"><div class="container">
<span class="eyebrow">6 vaihetta Suomelle</span>
<h1>Miten ostaa Kakobuyn kautta Suomesta</h1>
<p>Tilin luomisesta paketin lähetykseen. Kakobuy.fi:ssä et luo tiliä etkä tilausta.</p>
</div></section>
<div class="container article-layout"><article class="article">
<p>Kakobuy toimii välikätenä sinun ja myyjän välillä. Tavara ei tule suoraan kotiin: maksat sen ensin, se saapuu varastoon, tarkistat kuvat ja vasta sitten hoidat kansainvälisen toimituksen Suomeen.</p>
<div class="article-callout"><strong>Ennen kuin klikkaat Maksa</strong>Pidä alkuperäinen linkki valmiina, tarkista variantti ja varmista, että linja hyväksyy tavaran ja sen saa tuoda Suomeen laillisesti.</div>
<h2 id="vaihe-1">1. Luo tili Kakobuyssa</h2>
<p>Siirry <a class="text-link" href="https://ikako.vip/r/yze69" target="_blank" rel="noopener noreferrer">Kakobuyn rekisteröintiin</a> ja valitse Sign Up. Täytä sähköposti, valitse salasana ja viimeistele vahvistus, jos palvelu sitä pyytää.</p>
<p>Rekisteröinti voi sisältää kuponkitarjouksen. Sen arvo ja ehdot kannattaa tarkistaa tilillä; se ei ole automaattisesti käytettävissä mihin tahansa ostokseen.</p>
<h2 id="vaihe-2">2. Löydä tuote tai liitä linkki</h2>
<p>Voit liittää kopioidun tuotelinkin tai hakea avainsanoilla. Jos sinulla on Taobao-, 1688- tai Weidian-linkki, liitä se Kakobuyn hakuun ja varmista, että oikea tuote latautui.</p>
<p>Voit aloittaa myös <a class="text-link" href="/kakobuy-finds/">valituista tuotteista</a> tai <a class="text-link" href="/kakobuy-spreadsheet/">kategorioista</a>. Linkki ei ole laadun tai saatavuuden vahvistus.</p>
<h2 id="vaihe-3">3. Valitse variantti ja maksa tilaus</h2>
<p>Valitse väri, koko ja määrä. Vaatteissa noudata myyjän mittoja, ei pelkkää suomalaista kokokirjainta. Ensimmäinen maksu ei ole lopullinen hinta kotiintoimitukselle Suomeen. Kansainvälinen toimitus hoidetaan myöhemmin, kun varasto tietää painon ja mitat.</p>
<h2 id="vaihe-4">4. Tarkista QC-kuvat varastossa</h2>
<p>Kun tavara on varastossa, avaa Warehouse ja tuotteen QC Picture. Vertaa väri, kokolappu, kappalemäärä ja näkyvät yksityiskohdat tilaukseen. QC paljastaa näkyviä virheitä; se ei yksin todista aitoutta.</p>
<div class="article-callout"><strong>Jokin ei täsmää?</strong>Hoida asia palvelun kanssa ennen kansainvälistä lähetystä.</div>
<h2 id="vaihe-5">5. Lisää suomalainen osoite ja valitse toimitus</h2>
<p>Valitse lähetettävät tuotteet ja lisää oikea toimitusosoite. Maan on oltava <strong>Suomi / Finland</strong>. Tarkista nimi, katu, postinumero, kaupunki ja puhelin; suomalaiselle numerolle käytä suuntanumeroa <strong>+358</strong>.</p>
<p>Vertaa linjoja, jotka oikeasti tarjotaan tälle osoitteelle ja tälle tavaralle. Päätä hinnan, rajoitusten, mittojen, painon ja ehtojen perusteella. Lisätiedot: <a class="text-link" href="/kakobuy-toimitus/">toimitusopas Suomeen</a>.</p>
<h2 id="vaihe-6">6. Vahvista lähetys ja seuraa pakettia</h2>
<p>Ennen vahvistusta tarkista osoite, sisältö, linja ja hinta. Täytä tullitiedot totuudenmukaisesti. Lähetyksen jälkeen seuraa seurantanumeroa Kakobuy-tilillä. Ensimmäinen päivitys ei välttämättä tule heti.</p>
<h2 id="virheet">Yleisimmät virheet</h2>
<ul><li>Väärä koko ilman mittataulukon tarkistusta.</li><li>QC-kuvien ohittaminen.</li><li>Vain todellisen painon laskeminen ja tilavuuspainon unohtaminen.</li><li>Tavaran ostaminen, jolla on toimitus- tai tuontirajoitus.</li><li>Epätodet tiedot tulli-ilmoituksessa.</li></ul>
<p class="legal-note">Tiedot ovat yleisluontoisia. Ajantasainen hinta, saatavuus, toimitusehdot ja tuontivelvoitteet kannattaa varmistaa ennen maksua Kakobuyssa ja viranomaisilta.</p>
<p style="margin-top:30px"><a class="button" href="/kakobuy-finds/">Selaa valittuja tuotteita →</a></p>
</article>
<aside class="toc"><strong>Ohjeen sisältö</strong>
<a href="#vaihe-1">1. Luo tili</a>
<a href="#vaihe-2">2. Löydä tuote</a>
<a href="#vaihe-3">3. Variantti ja maksu</a>
<a href="#vaihe-4">4. Tarkista QC</a>
<a href="#vaihe-5">5. Suomalainen osoite</a>
<a href="#vaihe-6">6. Lähetys ja seuranta</a>
<a href="#virheet">Yleisimmät virheet</a></aside></div>
"""
    return wrap(
        "kuinka-kayttaa-kakobuyta",
        "Miten ostaa Kakobuyn kautta – suomenkielinen ohje vaiheittain",
        "Täydellinen suomenkielinen ohje Kakobuy-ostoon: tuotelinkki, tilaus, varasto, QC-kuvat ja toimitus Suomeen.",
        body,
        og_type="article",
    )


def page_shipping() -> str:
    body = """
<section class="article-hero"><div class="container">
<span class="eyebrow">Toimitus Suomeen · päivitetty 14.9.2026</span>
<h1>Halvin linja ei välttämättä ole halvin paketti</h1>
<p>Ratkaisee laskutettava paino, mitat, sisältö ja se, mitä hintaan sisältyy. Tässä tarkistuslista tarjousten vertailuun.</p>
</div></section>
<div class="container article-layout"><article class="article">
<h2 id="lahetys">Miten lähetys etenee</h2>
<p>Eri myyjien tuotteet saapuvat ensin Kakobuyn varastoon. Kun ne ovat valmiina, valitset yhdessä lähetettävät tuotteet, säädät pakkausta ja vertaat tarjottuja kansainvälisiä linjoja.</p>
<h2 id="paino">Todellinen ja tilavuuspaino</h2>
<p>Kuljettaja voi laskuttaa todellisen painon tai mitoista lasketun tilavuuspainon. Kevyt mutta kookas tavara voi tulla kalliimmaksi tilavuuden takia. Jakaja ja säännöt vaihtelevat linjoittain.</p>
<div class="article-callout"><strong>Käytännön vinkki</strong>Kookkaissa tuotteissa harkitse turhien laatikoiden poistoa tai tyhjiöpakkausta, jos se ei vahingoita tuotetta.</div>
<h2 id="linjat">Miten vertaat linjoja</h2>
<ul>
<li>Hinta: vertaa kokonaishintaa, ei vain ensimmäisen painoyksikön hintaa.</li>
<li>Arvioitu aika: kyse on arviosta, ei taatusta päivästä.</li>
<li>Sisältörajoitukset: osa linjoista ei ota akkuja, nesteitä, kosmetiikkaa tai tiettyjä materiaaleja.</li>
<li>Seuranta ja vakuutus: tarkista seurannan laajuus ja korvausehdot.</li>
<li>Laskentatapa: varmista, laskuttaako linja todellisen vai tilavuuspainon.</li>
</ul>
<h2 id="yhdistaminen">Yhdistäminen ja pakkauksen muokkaus</h2>
<p>Useiden tuotteiden yhdistäminen yhteen pakettiin voi laskea kiinteitä kuluja, mutta isompi paketti ei aina ole halvin. Särkyvä tarvitsee suojaa; kengissä tai vaatteissa voi pyytää alkuperäispakkauksen poistoa.</p>
<h2 id="alv">ALV ja tulli Suomessa 2026</h2>
<p>EU:n ulkopuolelta tulevista lähetyksistä tarvitaan tulli-ilmoitus, ja ALV ratkaistaan. Suomen yleinen ALV-kanta on <strong>25,5 %</strong>. 1.7.2026 alkaen useimpiin enintään 150 euron etämyyntilähetyksiin tulee myös väliaikainen <strong>3 euron tulli tulli nimikettä kohti</strong>. Yksi nimike voi sisältää useita kappaleita samaa lajia; kyse ei ole automaattisesti 3 eurosta jokaista kappaletta kohti. Yli 150 euron lähetyksissä käytetään tavanomaista tullinimikkeistöä.</p>
<p>Posti tai muu kuljettaja voi periä ALVin ja käsittelymaksun ennen luovutusta, ellei linja ole ennakkoon maksettu (IOSS / tax-paid). Jos ALV on jo maksettu IOSS:n kautta, sitä ei pidä periä toiseen kertaan, mutta IOSS-tietojen oikea välitys on kriittistä.</p>
<p>Ajantasaiset säännöt: <a href="https://tulli.fi/yksityishenkiloille" target="_blank" rel="noopener noreferrer">Tulli.fi – yksityishenkilöt ↗</a> · <a href="https://www.vero.fi/henkiloasiakkaat/" target="_blank" rel="noopener noreferrer">Vero.fi ↗</a></p>
<h2 id="seuranta">Lähetyksen seuranta</h2>
<p>Kun lähetys on luotu, näkyy yleensä seurantanumero. Viive tarran luonnin ja ensimmäisen fyysisen skannauksen välillä on tavallinen. Joillain reiteillä seuranta päivittyy selvemmin vasta Euroopan saapumisen tai viimeisen kuljettajan luovutuksen jälkeen.</p>
<h2 id="tarkistus">Tarkistus ennen toimituksen maksua</h2>
<ul>
<li>Olen nähnyt QC-kuvat kaikista tuotteista.</li>
<li>Tiedän paketin lopullisen painon ja mitat.</li>
<li>Olen tarkistanut valitun linjan rajoitukset.</li>
<li>Ymmärrän vakuutuksen ja seurannan laajuuden.</li>
<li>Olen antanut totuudenmukaiset tiedot kuljetusta ja tullausta varten.</li>
</ul>
</article>
<aside class="toc"><strong>Sisältö</strong>
<a href="#lahetys">Miten lähetys etenee</a>
<a href="#paino">Paino</a>
<a href="#linjat">Linjan valinta</a>
<a href="#yhdistaminen">Yhdistäminen</a>
<a href="#alv">ALV ja tulli</a>
<a href="#seuranta">Seuranta</a>
<a href="#tarkistus">Tarkistuslista</a></aside></div>
"""
    return wrap(
        "kakobuy-toimitus",
        "Kakobuy toimitus Suomeen – paino, hinta ja tulli",
        "Miten Kakobuy-toimitus Suomeen toimii: yhdistäminen, todellinen ja tilavuuspaino, linjan valinta, ALV 25,5 %, tulli ja seuranta.",
        body,
        og_type="article",
    )


def page_faq() -> str:
    body = f"""
<section class="article-hero"><div class="container">
<span class="eyebrow">FAQ Suomelle · tiedot 14.9.2026</span>
<h1>Kakobuy ilman kiertelyä</h1>
<p>Mitä maksetaan, mitä varasto osaa, paljonko toimitus maksaa ja mitä 1.7.2026 muuttui tullissa ja ALVissa.</p>
</div></section>
<section class="section"><div class="container">{faq_list_html(FAQ)}
<p class="catalog-price-note">Lähteet: <a href="https://tulli.fi/yksityishenkiloille" target="_blank" rel="noopener noreferrer">Tulli</a>, <a href="https://www.vero.fi/henkiloasiakkaat/" target="_blank" rel="noopener noreferrer">Vero</a>. Tarkista aina Kakobuy-tilin ajantasainen tarjous.</p>
</div></section>
"""
    return wrap(
        "faq",
        "Kakobuy FAQ Suomelle (2026) – toimitus, QC, tulli ja ALV",
        "Lyhyet ja tarkistetut vastaukset suomalaisille Kakobuy-käyttäjille. Miten varasto ja QC toimivat, mitä toimitus maksaa ja mitä 1.7.2026 muuttui tullissa ja ALVissa.",
        body,
        json_ld=[json_ld_faq(FAQ)],
    )


def page_about() -> str:
    body = """
<section class="article-hero"><div class="container">
<h1>Käytännön opas suomalaisille ostajille</h1>
<p>Ohjeet Kakobuyn käyttöön, toimituksen selitys ja linkit valittuihin tuotteisiin. Päivitetty 14. syyskuuta 2026.</p>
</div></section>
<div class="container article-layout"><article class="article">
<h2>Mitä täältä löytyy</h2>
<p>Kakobuy.fi on riippumaton suomenkielinen opas Kakobuy-palvelun käyttöön. Selitämme ostamisen vaiheet, varaston tarkistuskuvat ja toimituksen valinnan Suomeen. Lisäämme tuote-esimerkkejä ja linkkejä.</p>
<h2>Miten tuotelinkit toimivat</h2>
<p>Yksittäisten tuotteiden linkit vievät Kakobuyn tuotesivulle. Ennen tilausta tarkista kohdesivulla variantti, hinta ja saatavuus.</p>
<p>Kakobuy.fi:ssä et osta etkä maksa mitään. Meillä ei ole asiakastilejä, emme ota tilauksia emmekä tarjoa varasto- tai kuljetuspalvelua.</p>
<h2>Riippumattomuus ja kumppanuuslinkit</h2>
<p>Kakobuy.fi ei ole Kakobuyn virallinen sivusto eikä asiakastuki. Osa linkeistä sisältää kumppanuuskoodin. Ehdot täyttyessä tämä sivusto voi saada provision. Tiedot: <a href="/affiliate-disclosure/">kumppanuusilmoitus</a>.</p>
<h2>Miten lukea hintoja</h2>
<p>Eurohinnat ovat suuntaa-antavia muunnoksia, eivät myyntitarjous tällä sivustolla. Tuotteen valinta ei tarkoita, että olisimme testanneet sen tai varmistaneet aitouden.</p>
</article></div>
"""
    return wrap("about", "Tietoa Kakobuy.fi:stä", "Kakobuy.fi on riippumaton suomalainen opas Kakobuyn käyttöön: ostaminen, QC ja toimitus Suomeen.", body, og_type="article")


def page_privacy() -> str:
    body = """
<section class="article-hero"><div class="container"><h1>Tietosuoja</h1>
<p>Tämä sivusto on staattinen opas. Emme avaa asiakastilejä emmekä ota tilauksia.</p></div></section>
<div class="container article-layout"><article class="article">
<p>Sivusto voi käyttää teknisiä evästeitä tai palvelinlokitietoja toiminnan varmistamiseksi. Osto ja maksu tapahtuvat Kakobuyssa, jonka ehtoja noudatat siellä.</p>
<p>Jos otat yhteyttä sähköpostitse, käytämme viestiä vain vastaukseen.</p>
</article></div>
"""
    return wrap("privacy-policy", "Tietosuoja – Kakobuy Suomi", "Kakobuy.fi:n tietosuojakäytäntö: staattinen opas, ei asiakastilejä tällä sivustolla.", body, og_type="article")


def page_affiliate() -> str:
    body = """
<section class="article-hero"><div class="container"><h1>Kumppanuusilmoitus</h1>
<p>Tuotelinkit Kakobuysyn voivat sisältää kumppanuuskoodin.</p></div></section>
<div class="container article-layout"><article class="article">
<p>Jos teet tilauksen linkin kautta ja ehdot täyttyvät, voimme saada provision. Hinta sinulle ei nouse tästä syystä. Emme ole Kakobuyn virallinen sivusto.</p>
<p>Katalogi ei ole laatutodistus. Hinta, variantti, saatavuus ja tuontisäännöt kannattaa tarkistaa ennen maksua.</p>
</article></div>
"""
    return wrap("affiliate-disclosure", "Kumppanuusilmoitus – Kakobuy Suomi", "Kakobuy.fi käyttää kumppanuuslinkkejä. Provision saaminen ei nosta hintaasi.", body, og_type="article")


def page_coupon() -> str:
    body = """
<section class="article-hero"><div class="container">
<h1>Kakobuy-kuponki</h1>
<p>Uuden käyttäjän tarjoukset näkyvät Kakobuy-tilillä. Niitä ei sovelleta automaattisesti spreadsheet-selailuun.</p>
</div></section>
<div class="container article-layout"><article class="article">
<p>Rekisteröidy kutsulinkillä <a class="text-link" href="https://ikako.vip/r/yze69" target="_blank" rel="noopener noreferrer">ikako.vip/r/yze69</a>. Kampanjat (esim. uuden käyttäjän CNY-kuponki) muuttuvat; vahvista aina omalla tililläsi.</p>
<p>Spreadsheet-selailu ei valitse toimituslinjaa eikä lisää kupongin automaattisesti. Hyvä sessio päättyy pakettisuunnitelmaan, ei satunnaiseen raskaaseen koriin.</p>
<p><a class="button" href="/kakobuy-spreadsheet/">Siirry spreadsheetiin</a></p>
</article></div>
"""
    return wrap("kakobuy-coupon", "Kakobuy-kuponki ja alennuskoodit", "Kakobuy-kupongit suomalaisille ostajille: tarkista tarjous tilillä, spreadsheet ei lisää koodia automaattisesti.", body, og_type="article")


def page_qc() -> str:
    body = """
<section class="article-hero"><div class="container">
<h1>Kakobuy QC-kuvat</h1>
<p>Tarkistuskuvat otetaan, kun tuote on saapunut varastoon – ennen kansainvälistä lähetystä.</p>
</div></section>
<div class="container article-layout"><article class="article">
<p>Vertaa väri, kokolappu, kappalemäärä, saumat ja näkyvät viat. Älä kuittaa kuvia sokeasti. Jos jokin ei täsmää, avaa tiketti ennen linjan maksua.</p>
<p>QC ei todista aitoutta. Se auttaa välttämään väärän värin, väärän koon tai rikkinäisen kappaleen lähettämisen Suomeen.</p>
<p><a class="text-link" href="/kuinka-kayttaa-kakobuyta/#vaihe-4">Katso QC osana ostohjetta</a></p>
</article></div>
"""
    return wrap("kakobuy-qc", "Kakobuy QC – miten luet tarkistuskuvat", "Kakobuy QC-kuvat: mitä katsoa varastokuvista ennen lähettämistä Suomeen.", body, og_type="article")


def page_kokemuksia() -> str:
    body = """
<section class="article-hero"><div class="container">
<h1>Kakobuy kokemuksia – onko luotettava?</h1>
<p>Tämä sivu ei keksi tähtiarvioita. Luotettavuus ratkaistaan tilillä, QC-kuvissa ja toimituslinjassa.</p>
</div></section>
<div class="container article-layout"><article class="article">
<p>Kakobuy on toimiva ostoagentti: se ostaa, varastoi, kuvaa ja lähettää. kakobuy.fi ei ole Kakobuy eikä korvaa sen tukea.</p>
<ul>
<li>Maksa tavalla, jossa on ostajan suoja.</li>
<li>Lue QC ennen kansainvälistä lähetystä.</li>
<li>Älä usko yhteisön hypetystä laatutodisteeksi.</li>
<li>Tulli ja ALV 25,5 % Suomessa eivät ole Kakobuyn “virhe”, vaan tuontisääntöjä.</li>
</ul>
<p><a class="button" href="/faq/">Avaa FAQ</a> <a class="button secondary" href="/kuinka-kayttaa-kakobuyta/">Ostamisen vaiheet</a></p>
</article></div>
"""
    return wrap("kakobuy-kokemuksia", "Kakobuy kokemuksia (2026) — Luotettava?", "Kakobuy kokemuksia suomalaisille: ei tekoarvioita. Tarkista QC, maksutapa ja tulli itse.", body, og_type="article")


def page_suomi() -> str:
    body = """
<section class="article-hero"><div class="container">
<h1>Kakobuy Suomi</h1>
<p>Tämä .fi-hubi keskittyy eurohintoihin, Posti/DHL-toimitukseen Suomeen ja spreadsheet-työnkulkuun ennen paketin lähettämistä.</p>
</div></section>
<div class="container article-layout"><article class="article">
<ul class="check-list">
<li>Aloita spreadsheetistä, valitse 3–5 riviä, pyydä QC varastossa.</li>
<li>Lue toimitus- ja tulliohjeet ennen isoa haulia.</li>
<li>Rekisteröidy vain Kakobuyn linkillä, älä tähän sivustoon.</li>
</ul>
<p><a class="button" href="/kakobuy-spreadsheet/">Avaa spreadsheet</a>
<a class="button secondary" href="/kakobuy-toimitus/">Toimitus ja tulli</a></p>
</article></div>
"""
    return wrap("kakobuy-suomi", "Kakobuy Suomi — opas ostajille", "Kakobuy Suomi: spreadsheet eurohinnoilla, QC ja toimitus Suomeen.", body, og_type="article")


def page_contact() -> str:
    body = """
<section class="article-hero"><div class="container">
<h1>Yhteystiedot</h1>
<p>Tämä sivusto ei hoida Kakobuy-tilauksia. Tilausongelmat kuuluvat Kakobuyn tukeen.</p>
</div></section>
<div class="container article-layout"><article class="article">
<p>Sivustoa koskevat kysymykset: <a href="mailto:support@kakobuytips.com">support@kakobuytips.com</a></p>
<p>Kakobuyn ohjekeskus: <a href="https://www.kakobuy.com/help" target="_blank" rel="noopener noreferrer">kakobuy.com/help</a></p>
</article></div>
"""
    return wrap("contact", "Yhteystiedot – Kakobuy Suomi", "Kakobuy.fi yhteystiedot. Tilaukset hoidetaan Kakobuyssa.", body, og_type="article")


def page_404() -> str:
    return f"""<!doctype html>
<html lang="fi"><head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Sivua ei löytynyt – Kakobuy Suomi</title>
<meta name="robots" content="noindex">
<link rel="stylesheet" href="{esc(asset("assets/styles.css"))}">
<link rel="stylesheet" href="{esc(asset("assets/layout.css"))}">
<link rel="stylesheet" href="{esc(asset("assets/fi.css"))}">
</head><body>
<main class="article-hero"><div class="container">
<h1>Sivua ei löytynyt</h1>
<p>Avaa spreadsheet tai palaa etusivulle.</p>
<p><a class="button" href="/kakobuy-spreadsheet/">Spreadsheet</a>
<a class="button secondary" href="/">Etusivu</a></p>
</div></main>
</body></html>
"""


def redirect_html(target: str) -> str:
    return f"""<!doctype html>
<html lang="fi"><head>
<meta charset="utf-8">
<title>Siirretään…</title>
<link rel="canonical" href="{esc(BASE + target)}">
<meta http-equiv="refresh" content="0;url={esc(target)}">
<script>location.replace({json.dumps(target)});</script>
</head><body><p><a href="{esc(target)}">Jatka</a></p></body></html>
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
        "name": "Kakobuy Suomi",
        "short_name": "Kakobuy.fi",
        "start_url": "/",
        "display": "browser",
        "lang": "fi-FI",
        "icons": [
            {"src": "/assets/favicon-v2-32.png", "sizes": "32x32", "type": "image/png"},
            {"src": "/assets/apple-touch-icon-v2.png", "sizes": "180x180", "type": "image/png"},
        ],
    }
    (out_dir / "site.webmanifest").write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def assert_quality(out_dir: Path) -> None:
    home = (out_dir / "index.html").read_text(encoding="utf-8")
    sheet = (out_dir / "kakobuy-spreadsheet" / "index.html").read_text(encoding="utf-8")
    ship = (out_dir / "kakobuy-toimitus" / "index.html").read_text(encoding="utf-8")
    js = (out_dir / "assets" / "spreadsheet.js").read_text(encoding="utf-8")
    php = (out_dir / "api" / "products.php").read_text(encoding="utf-8")
    for bad in ("Search intent", "Country guide", "ALV 24%", "kakobuydocs.com", "W2CLinks", "fansheets.com"):
        if bad in home or bad in sheet or bad in ship:
            raise SystemExit(f"FI local site still contains {bad!r}")
    if 'lang="fi"' not in home:
        raise SystemExit("home missing lang=fi")
    if "/api/products.php" not in sheet:
        raise SystemExit("spreadsheet missing products API config")
    if "$_GET['q']" not in php or "item_id" not in php:
        raise SystemExit("products.php missing live search fields")
    if "Avaa Kakobuyssa" not in js and "Avaa Kakobuyssa" not in sheet:
        raise SystemExit("spreadsheet missing Kakobuy CTA")
    if "25,5" not in ship:
        raise SystemExit("shipping page missing 25.5% VAT")
    if "tulli.fi" not in ship:
        raise SystemExit("shipping page missing tulli.fi")
    if "Etusivu" not in home or "Toimitus" not in home:
        raise SystemExit("Finnish nav missing")
    if "24 tuotetta" in home or "24 tuotetta" in sheet:
        raise SystemExit("FI site still hardcodes the 24-product CZ catalog")


def build_kakobuy_fi(out_dir: Path) -> int:
    catalog = load_catalog()
    RUNTIME["catalog"] = catalog
    RUNTIME["live"] = fetch_w2c_products(page=1, per_page=24)
    if out_dir.exists():
        shutil.rmtree(out_dir)
    out_dir.mkdir(parents=True)
    shutil.copytree(TEMPLATE_ASSETS, out_dir / "assets", ignore=shutil.ignore_patterns("products"))
    api_dir = out_dir / "api"
    api_dir.mkdir(parents=True)
    shutil.copyfile(API_PHP, api_dir / "products.php")

    pages = {
        "": page_home(catalog),
        "kakobuy-spreadsheet": page_spreadsheet(catalog),
        "kakobuy-finds": page_finds(catalog),
        "kuinka-kayttaa-kakobuyta": page_guide(),
        "kakobuy-toimitus": page_shipping(),
        "faq": page_faq(),
        "about": page_about(),
        "privacy-policy": page_privacy(),
        "affiliate-disclosure": page_affiliate(),
        "kakobuy-coupon": page_coupon(),
        "kakobuy-qc": page_qc(),
        "kakobuy-kokemuksia": page_kokemuksia(),
        "kakobuy-suomi": page_suomi(),
        "contact": page_contact(),
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
    n = build_kakobuy_fi(dest)
    print(f"Built {n} kakobuy.fi files → {dest}")
