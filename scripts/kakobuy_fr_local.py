"""Build kakospreadsheet.fr as a CZ-style local catalog site (EUR, France UX)."""

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

CATALOG_PATH = ROOT / "data" / "kakobuy-fr-catalog.json"
TEMPLATE_ASSETS = ROOT / "templates" / "kakobuy-fi" / "assets"
FR_ASSETS = ROOT / "templates" / "kakobuy-fr" / "assets"
API_PHP = ROOT / "templates" / "api" / "products.php"
DOMAIN = "kakospreadsheet.fr"
BASE = f"https://{DOMAIN}"
TODAY = date.today().isoformat()
ASSET_V = "20260916a"
RUNTIME: dict = {}

NAV = [
    ("", "Accueil"),
    ("kakobuy-spreadsheet", "Spreadsheet"),
    ("kakobuy-finds", "Finds"),
    ("how-to-use-kakobuy", "Comment acheter"),
    ("livraison-kakobuy", "Livraison"),
    ("kakobuy-coupon", "Coupons"),
]

PRIMARY_SLUGS = [
    "",
    "kakobuy-spreadsheet",
    "kakobuy-finds",
    "how-to-use-kakobuy",
    "livraison-kakobuy",
    "kakobuy-shipping",
    "kakobuy-coupon",
    "kakobuy-qc",
    "avis-kakobuy",
    "kakobuy-france",
    "kakobuy-lululemon",
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
    "meilleur-kakobuy-spreadsheet": "/kakobuy-spreadsheet/",
    "kakobuy-review": "/avis-kakobuy/",
    "kakobuy-avis": "/avis-kakobuy/",
    "kakobuy-shipping-calculator": "/livraison-kakobuy/",
    "comment-utiliser-kakobuy": "/how-to-use-kakobuy/",
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
    "locale": "fr-FR",
    "product": "Produit",
    "productOne": "1 produit",
    "products": "produits",
    "other": "Autres",
    "priceOnKakobuy": "Prix sur Kakobuy",
    "openOnKakobuy": "Ouvrir sur Kakobuy ↗",
    "openAria": "Ouvrir {title} sur Kakobuy (nouvel onglet)",
    "openAriaCard": "{title} — ouvrir sur Kakobuy",
    "prev": "Précédent",
    "next": "Suivant",
    "pageOf": "Page {current} / {pages}",
    "loadError": "Impossible de charger les produits. Réessayez dans un instant.",
    "emptyCount": "0 produit",
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
    return "Prix sur Kakobuy" if amount is None else f"≈ {amount} €"


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
        groups.setdefault(str(cat.get("group") or "Autres"), []).append(cat)
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
        "avis-kakobuy",
        "livraison-kakobuy",
        "kakobuy-france",
        "kakobuy-lululemon",
        "kako-buy",
        "kako-spreadsheet",
        "partner-disclosure",
        "terms",
    }
    path = "/" if not slug else f"/{slug}/"
    if slug in exclusive:
        loc = canonical(slug)
        return (
            f'<link rel="alternate" hreflang="fr-FR" href="{esc(loc)}">\n'
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
<html lang="fr-FR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(description)}">
<link rel="canonical" href="{esc(canonical_url)}">
{hreflang_tags(slug)}
<meta property="og:site_name" content="Kakobuy Spreadsheet France">
<meta property="og:type" content="{esc(og_type)}">
<meta property="og:locale" content="fr_FR">
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
<a class="skip-link" href="#contenu">Aller au contenu</a>
<div class="kb-promo"><div class="container">KAKOSEP jusqu’au 30.9 : pack 1300 CNY + 10 % livraison · nouveaux 3000 CNY · <a href="https://ikako.vip/r/yze69" target="_blank" rel="sponsored noopener noreferrer">S’inscrire sur Kakobuy</a></div></div>
<header class="site-header"><div class="container nav">
<a class="brand" href="/" aria-label="Kakobuy Spreadsheet France – accueil"><span class="brand-mark">K</span><span>Kakobuy <small>France</small></span></a>
<form class="kb-head-search" action="/kakobuy-spreadsheet/" method="get" role="search">
<label class="sr-only" for="kb-q">Rechercher un produit</label>
<input id="kb-q" type="search" name="q" placeholder="Produit, kako buy, ou collez un lien" autocomplete="off">
<button type="submit">Rechercher</button>
</form>
<div class="nav-actions">
<a class="button small" href="https://ikako.vip/r/yze69" target="_blank" rel="sponsored noopener noreferrer">S’inscrire</a>
<button class="menu-button" type="button" aria-label="Ouvrir le menu" aria-expanded="false">☰</button>
</div>
</div></header>
<nav class="kb-subnav" aria-label="Principal"><div class="container nav-links">{"".join(links)}</div></nav>
<main id="contenu">"""


def footer() -> str:
    return f"""</main>
<footer class="site-footer"><div class="container">
<div class="footer-grid">
<div><a class="brand" href="/"><span class="brand-mark">K</span><span>Kakobuy France</span></a>
<p class="footer-copy">Catalogue indépendant en français et guide Kakobuy spreadsheet pour la France. Aussi pour les recherches kako buy et kako-spreadsheet.</p></div>
<div class="footer-col"><strong>Guide</strong>
<a href="/how-to-use-kakobuy/">Comment acheter</a>
<a href="/livraison-kakobuy/">Livraison France</a>
<a href="/avis-kakobuy/">Avis Kakobuy</a>
<a href="/kakobuy-france/">Kakobuy France</a></div>
<div class="footer-col"><strong>Produits</strong>
<a href="/kakobuy-spreadsheet/">Kakobuy spreadsheet</a>
<a href="/kakobuy-finds/">Finds</a>
<a href="/kakobuy-coupon/">Coupons</a>
<a href="/kako-buy/">Kako buy</a>
<a href="/kako-spreadsheet/">Kako spreadsheet</a></div>
<div class="footer-col"><strong>Info</strong>
<a href="/about/">À propos</a>
<a href="/privacy-policy/">Confidentialité</a>
<a href="/affiliate-disclosure/">Affiliation</a></div>
</div>
<div class="footer-bottom"><span>© <span data-year></span> kakospreadsheet.fr</span>
<span>Ce n’est pas le site officiel de Kakobuy.</span></div>
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
            "name": "Kakobuy Spreadsheet France",
            "url": f"{BASE}/",
            "inLanguage": "fr-FR",
            "description": "Kakobuy spreadsheet pour la France : liens produits, prix en euros, QC et livraison. Aussi pour kako buy et kako-spreadsheet.",
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
            "inLanguage": "fr-FR",
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
    label = (cats.get(p["category"]) or {}).get("label") or p["category"] or "Autres"
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
        f'aria-label="Ouvrir {esc(p["title"])} sur Kakobuy (nouvel onglet)">Ouvrir sur Kakobuy ↗</a></li>'
    )


def finds_card(p: dict, catalog: dict, cats: dict) -> str:
    label = (cats.get(p["category"]) or {}).get("label") or p["category"] or "Autres"
    rate = catalog["cny_per_eur"]
    href = kakobuy_url(p["item_id"], catalog["affcode"], p.get("shop") or "weidian")
    brand = f'<p class="catalog-advice">{esc(p["brand"])}</p>' if p.get("brand") else ""
    cny = format_cny(p.get("price_cny"))
    return f"""<article class="catalog-card" data-product-id="{esc(p["id"])}">
<a class="catalog-image" href="{esc(href)}" target="_blank" rel="sponsored noopener noreferrer" aria-label="{esc(p["title"])} — ouvrir sur Kakobuy">
<img src="{esc(image_src(p["image"]))}" width="750" height="750" alt="{esc(p["title"])}" loading="lazy" decoding="async"><span>{esc(label)}</span></a>
<div class="catalog-body">
<h3>{esc(p["title"])}</h3>
<div class="catalog-meta"><strong>{esc(format_eur(p.get("price_cny"), rate))}</strong><small>{esc(cny)}</small></div>
{brand}
<a class="text-link" href="{esc(href)}" target="_blank" rel="sponsored noopener noreferrer">Ouvrir sur Kakobuy ↗</a>
</div></article>"""


def rate_note(catalog: dict) -> str:
    return (
        f'Prix et liens vérifiés le <time datetime="{esc(catalog["checked"])}">{esc(catalog["checked"])}</time>. '
        f'Taux BCE du <time datetime="{esc(catalog["ecb_date"])}">{esc(catalog["ecb_date"])}</time> : '
        f'1 EUR ≈ {str(catalog["cny_per_eur"]).replace(".", ",")} CNY, arrondi à l’euro. '
        "C’est le prix catalogue du produit, hors livraison internationale, taxes et TVA d’importation. "
        "Confirme la variante sur Kakobuy avant de payer."
    )


FAQ: list[tuple[str, str]] = [
    (
        "Qu’est-ce que Kakobuy ?",
        "Kakobuy est un agent d’achat et d’expédition. Il commande sur les marketplaces chinoises compatibles, réceptionne en entrepôt, prend des photos QC et propose des lignes internationales vers la France.",
    ),
    (
        "kakospreadsheet.fr vend-il des produits ?",
        "Non. Ce site est un catalogue et un guide d’affiliation indépendants. Achat, paiement et livraison se font sur Kakobuy et chez les vendeurs.",
    ),
    (
        "Kako buy, kako-buy ou kako spreadsheet : c’est la même chose ?",
        "Oui. Beaucoup tapent kako buy, kako-buy, kako spreadsheet ou kako-spreadsheet. Le nom officiel est Kakobuy. Le Kakobuy spreadsheet est le catalogue de liens de ce site.",
    ),
    (
        "Combien coûte la livraison en France ?",
        "Cela dépend du poids réel ou volumétrique, des dimensions, de la ligne et du contenu. Le devis live apparaît dans le compte Kakobuy une fois les articles en entrepôt.",
    ),
    (
        "TVA et douane en France ?",
        "Oui, pour les envois hors UE. La TVA générale en France est de 20 %. Depuis le 1.7.2026, beaucoup d’envois de vente à distance jusqu’à 150 € portent aussi 3 € de droit par position tarifaire. Kakobuy peut proposer des lignes duty-free : à confirmer en caisse. Voir douane.gouv.fr.",
    ),
    (
        "Kakobuy est-il fiable ?",
        "Kakobuy est une plateforme d’agent opérationnelle. Ce site n’est pas Kakobuy et ne garantit ni prix, ni qualité, ni dédouanement. Paie avec une protection acheteur, lis les photos QC et vérifie les restrictions de ligne.",
    ),
]


def page_home(catalog: dict) -> str:
    cats = cat_map(catalog)
    found, live = RUNTIME.get("live") or (0, [])
    featured = live[:8]
    rate = catalog["cny_per_eur"]
    count_label = f"{format_count(found)}+" if found else "Des milliers de"
    cat_count = len(catalog["categories"])
    cards = []
    for p in featured:
        href = kakobuy_url(p["item_id"], catalog["affcode"], p.get("shop") or "weidian")
        label = (cats.get(p["category"]) or {}).get("label") or p["category"] or "Autres"
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
<span class="eyebrow">Liens produits · prix en euros</span>
<h1>Kakobuy Spreadsheet<br><span class="gradient-text">pour la France</span></h1>
<p>Consulte le catalogue au même endroit. Cherche par nom, filtre une catégorie et compare les prix indicatifs en euros. Le produit s’ouvre sur Kakobuy — aussi si tu as tapé kako buy ou kako spreadsheet.</p>
<form class="kb-hero-search" action="/kakobuy-spreadsheet/" method="get" role="search">
<label class="sr-only" for="hero-q">Rechercher dans le spreadsheet</label>
<input id="hero-q" type="search" name="q" placeholder="Produit, kako buy, ou colle un lien Weidian" autocomplete="off">
<button type="submit">Rechercher</button>
</form>
<div class="hero-actions">
<a class="button" href="/kakobuy-spreadsheet/">Ouvrir le spreadsheet <span aria-hidden="true">→</span></a>
<a class="button secondary" href="/how-to-use-kakobuy/">Comment fonctionne l’achat</a>
</div>
<div class="trust-row" aria-label="Avantages">
<span><i class="check">✓</i> Pas de compte sur ce site</span>
<span><i class="check">✓</i> Prix en euros</span>
<span><i class="check">✓</i> Notes de livraison France</span>
</div>
</div>
<div class="hero-visual hero-art">
<img class="hero-art-image" src="{esc(asset('assets/hero.webp'))}" width="1152" height="864" alt="Livraison Kakobuy en France : entrepôt, QC et colis" fetchpriority="high">
</div>
</div></section>
<section class="kb-offers"><div class="container">
<div class="section-heading"><p class="kicker">Kakobuy.com · septembre 2026</p>
<h2>Offres actuelles</h2>
<p>Campagnes officielles Kakobuy. Conditions, réduction et dates se confirment dans le compte avant de payer.</p></div>
<div class="kb-offer-grid">
<a class="kb-offer" href="https://www.kakobuy.com/tipdetail?id=55" target="_blank" rel="noopener noreferrer">
<span class="kb-offer-tag">Code KAKOSEP</span>
<strong>Pack septembre 1300 CNY ≈ 167 € + 10 % extra livraison</strong>
<p>Échangeable du 8 au 30.9.2026 (heure de Pékin). Sur Kakobuy : Centre utilisateur → Coupons → Échanger, code <strong>KAKOSEP</strong>.</p>
<span class="text-link">Ouvrir la campagne sur Kakobuy ↗</span></a>
<a class="kb-offer" href="https://ikako.vip/r/yze69" target="_blank" rel="sponsored noopener noreferrer">
<span class="kb-offer-tag">Nouvel utilisateur</span>
<strong>Pack de coupons 3000 CNY ≈ 386 €</strong>
<p>Inscris-toi avec le lien d’invitation. Les coupons apparaissent dans le portefeuille ; le spreadsheet ne les applique pas tout seul.</p>
<span class="text-link">S’inscrire ↗</span></a>
<a class="kb-offer" href="https://www.kakobuy.com/tipdetail?id=55" target="_blank" rel="noopener noreferrer">
<span class="kb-offer-tag">Subvention 10 %</span>
<strong>Crédit livraison du 8–14.9, utilisable jusqu’au 31.10.2026</strong>
<p>La fenêtre pour obtenir la subvention sitewide est close. Si elle t’a été accordée, Kakobuy indique qu’elle vaut jusqu’au 31.10.2026.</p>
<span class="text-link">Voir les règles sur Kakobuy ↗</span></a>
<a class="kb-offer" href="/livraison-kakobuy/">
<span class="kb-offer-tag">UE / France</span>
<strong>3 € de droit / colis et lignes duty-free</strong>
<p>Kakobuy propose des lignes UE avec un droit d’environ 3 € par colis sur les positions éligibles. La TVA 20 % en France se règle à l’importation.</p>
<span class="text-link">Livraison France →</span></a>
</div>
</div></section>
<section class="stats"><div class="container stats-grid">
<div class="stat"><strong>{esc(count_label)} produits</strong><span>Catalogue recherchable sur ce site</span></div>
<div class="stat"><strong>{cat_count} catégories</strong><span>Des baskets aux accessoires</span></div>
<div class="stat"><strong>Prix en euros</strong><span>Indicatifs, hors livraison</span></div>
</div></section>
<section class="section"><div class="container">
<div class="section-heading"><p class="kicker">Derniers finds</p>
<h2>Baskets, vêtements et accessoires avec liens Kakobuy</h2>
<p>Tu peux chercher la liste complète par nom ou la limiter à une catégorie.</p></div>
<div class="catalog-grid">{"".join(cards)}</div>
<p class="catalog-note">Nous ne sommes pas le vendeur · vérifie prix et stock avant de commander
<a class="text-link" href="/kakobuy-spreadsheet/">Kakobuy Spreadsheet · chercher dans tout le catalogue →</a></p>
<p class="catalog-price-note">{rate_note(catalog)}</p>
</div></section>
<section class="section soft"><div class="container">
<div class="section-heading"><h2>Catalogue, commande et livraison</h2>
<p>Plus de catalogue, les étapes d’achat et le coût jusqu’en France.</p></div>
<div class="card-grid">
<a class="card" href="/kakobuy-spreadsheet/"><div class="card-icon">▦</div><h3>Spreadsheet</h3>
<p>Catégories et liens quand tu ne veux pas passer une heure sur les marketplaces chinoises.</p>
<span class="text-link">Ouvrir le catalogue ↗</span></a>
<a class="card" href="/how-to-use-kakobuy/"><div class="card-icon">1</div><h3>Première commande</h3>
<p>Ce que tu paies maintenant, ce que tu paies à l’entrepôt, et pourquoi il ne faut pas valider le QC à l’aveugle.</p></a>
<a class="card" href="/livraison-kakobuy/"><div class="card-icon">→</div><h3>Livraison France</h3>
<p>Poids réel vs volumétrique, consolidation, suivi, TVA 20 % et droit de 3 €.</p></a>
</div></div></section>
<section class="section"><div class="container">
<div class="section-heading"><h2>Achat en six étapes</h2>
<p>L’article arrive d’abord à l’entrepôt. La ligne vers la France se choisit après les photos.</p></div>
<div class="steps">
<div class="step"><h3>Trouve le produit</h3><p>Choisis un lien du spreadsheet ou une URL de marketplace.</p></div>
<div class="step"><h3>Colle le lien</h3><p>Choisis variante, taille, couleur et quantité.</p></div>
<div class="step"><h3>Paie l’article</h3><p>Après le paiement, le vendeur envoie à l’entrepôt Kakobuy.</p></div>
<div class="step"><h3>Ne saute pas le QC</h3><p>Compare couleur, étiquettes, quantité et défauts visibles.</p></div>
<div class="step"><h3>Expédie le colis</h3><p>Consolide les articles et choisis une ligne vers la France.</p></div>
<div class="step"><h3>Suis l’envoi</h3><p>Utilise le numéro de suivi quand le colis part.</p></div>
</div></div></section>
<section class="section soft"><div class="container split">
<div><h2>Le spreadsheet est une carte, pas un tampon qualité</h2>
<p>Le catalogue est sur ce site. Sur chaque offre, tu continues de choisir Kakobuy comme agent.</p>
<ul class="check-list"><li>Moins de recherche manuelle</li><li>Lien vers l’offre d’origine</li><li>Sans garantie de prix ni de qualité</li></ul>
<p>Tu as tapé <a href="/kako-buy/">kako buy</a> ou <a href="/kako-spreadsheet/">kako spreadsheet</a> ? C’est le même Kakobuy, avec le catalogue ici.</p></div>
<div>{faq_list_html(FAQ[:4])}</div>
</div></section>
<section class="cta"><div class="container"><div class="cta-box">
<h2>Tu as déjà un lien produit ?</h2>
<p>Colle-le dans la recherche Kakobuy. Si tu cherches encore des idées, commence par le spreadsheet.</p>
<a class="button" href="/kakobuy-spreadsheet/">Voir le catalogue</a>
</div></div></section>
"""
    json_ld_blocks = [json_ld_website()]
    if featured:
        json_ld_blocks.append(json_ld_itemlist("Catalogue de produits", featured, catalog))
    return wrap(
        "",
        "Kakobuy Spreadsheet France – produits, prix en euros et QC",
        "Kakobuy spreadsheet pour la France : cherche par nom, filtre les catégories, prix indicatifs en euros et liens qui s’ouvrent sur Kakobuy. Aussi pour kako buy et kako-spreadsheet. Guide indépendant.",
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
    count_label = f"{format_count(found)} produits" if found else "Chargement…"
    body = f"""
<section class="container sheet-intro"><p class="kicker">Catalogue France · recherchable</p>
<h1>Kakobuy Spreadsheet pour la France</h1>
<p>Voici le spreadsheet que tu peux vraiment chercher : liens en direct, prix en euros et paiement sur Kakobuy, pas une capture d’un Google Sheet. Les recherches kakobuy spreadsheet, kako spreadsheet et kako-buy spreadsheet aboutissent ici.</p></section>
<section class="container sheet-content" aria-label="Liste de produits">
<div class="sheet-controls">
<div class="sheet-field"><label for="sheet-search">Rechercher des produits</label>
<input type="search" id="sheet-search" placeholder="ex. sweat, sac, Jordan" autocomplete="off" aria-controls="sheet-products"></div>
<div class="sheet-field"><label for="sheet-category">Catégorie</label>
<select id="sheet-category" aria-controls="sheet-products"><option value="all">Toutes les catégories</option>{options}</select></div>
<button type="button" class="sheet-reset">Retirer les filtres</button>
<output id="sheet-count" aria-live="polite">{esc(count_label)}</output>
</div>
<p class="sheet-disclosure">Les prix sont indicatifs, hors livraison et autres taxes. Les liens sont d’affiliation ; nous pouvons recevoir une commission.</p>
<ul id="sheet-products" class="sheet-products">{items}</ul>
<nav id="sheet-pager" class="sheet-pager" aria-label="Pagination" hidden></nav>
<p class="sheet-empty" role="status" hidden>Aucun produit. Essaie un nom plus court ou une autre catégorie.</p>
<details class="sheet-method"><summary>Prix et date de vérification</summary>
<p>{rate_note(catalog)}</p>
<p>Photos et noms viennent des offres. Nous n’avons pas testé les articles en physique ; authenticité et stock d’entrepôt ne se confirment pas ici. <a href="/affiliate-disclosure/">Avis d’affiliation</a></p>
</details>
</section>
<section class="section soft" id="categories"><div class="container">
<div class="section-heading"><h2>Explorer par catégorie</h2>
<p>Choisis une catégorie pour filtrer cette page. Le produit s’ouvre sur Kakobuy.</p></div>
<div class="sheet-categories">{extra}</div>
</div></section>
<section class="section"><div class="container sheet-help">
<div><h2>Qu’est-ce qu’un Kakobuy spreadsheet ?</h2>
<p>Une liste de liens produits pour acheter via Kakobuy. Tu parcours ce catalogue dans le navigateur ; chaque ligne a une catégorie et un prix en euros.</p>
<p>Tu préfères les cartes ? Voir <a href="/kakobuy-finds/">Kakobuy Finds</a>.</p></div>
<div><h2>Que faire après avoir choisi</h2>
<p>Ouvre-le sur Kakobuy, vérifie variante et prix en direct. Une fois en entrepôt, lis les photos QC puis choisis la livraison vers la France.</p>
<p><a href="/how-to-use-kakobuy/">Guide de la première commande</a> · <a href="/livraison-kakobuy/">Livraison France</a></p></div>
</div></section>
"""
    json_ld_blocks = []
    if live:
        json_ld_blocks.append(
            json_ld_itemlist("Kakobuy Spreadsheet – produits avec prix en euros", live[:24], catalog)
        )
    return wrap(
        "kakobuy-spreadsheet",
        "Kakobuy Spreadsheet – produits avec prix en euros",
        "Kakobuy spreadsheet pour la France : cherche par nom, filtre une catégorie, compare les prix en euros et ouvre le produit sur Kakobuy. Aussi pour kako spreadsheet.",
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
<span class="eyebrow">Derniers finds · prix en euros</span>
<h1>Kakobuy Finds</h1>
<p>Vue en cartes du catalogue. Pour chercher plus vite, ouvre le <a class="text-link" href="/kakobuy-spreadsheet/">Kakobuy Spreadsheet</a>.</p>
</div></section>
<section class="section finds-catalog"><div class="container">
<div class="catalog-context">
<p>Estimations hors livraison et autres taxes. Les liens sont d’affiliation ; nous pouvons recevoir une commission.</p>
<details><summary>Prix, date et notes</summary>
<p>{rate_note(catalog)}</p></details>
</div>
<div class="catalog-filter" hidden>
<label for="catalog-category">Afficher la catégorie</label>
<select id="catalog-category"><option value="all">Toutes les catégories</option>{options}</select>
<output id="catalog-count">{esc(format_count(_found) + " produits") if _found else "Chargement…"}</output>
</div>
<div id="finds-grid" class="catalog-grid">{cards}</div>
<p class="finds-empty sheet-empty" role="status" hidden>Aucun produit dans cette catégorie.</p>
<p class="catalog-price-note">{rate_note(catalog)}</p>
</div></section>
"""
    json_ld_blocks = []
    if live:
        json_ld_blocks.append(
            json_ld_itemlist("Kakobuy Finds – produits avec prix en euros", live[:24], catalog)
        )
    return wrap(
        "kakobuy-finds",
        "Kakobuy Finds – produits avec prix en euros",
        "Kakobuy Finds pour la France : derniers finds avec prix en euros et liens directs vers Kakobuy.",
        body,
        extra_css=[asset("assets/catalog.css")],
        extra_js=[asset("assets/catalog-live.js"), asset("assets/finds.js")],
        json_ld=json_ld_blocks,
    )


def page_guide() -> str:
    body = """
<section class="article-hero"><div class="container">
<span class="eyebrow">6 étapes pour la France</span>
<h1>Comment acheter sur Kakobuy depuis la France</h1>
<p>De la création du compte jusqu’à l’expédition du colis. Sur kakospreadsheet.fr tu ne crées pas de compte et tu ne passes pas commande.</p>
</div></section>
<div class="container article-layout"><article class="article">
<p>Kakobuy se place entre toi et le vendeur. La marchandise n’arrive pas directe à domicile : tu paies l’article, il entre en entrepôt, tu regardes les photos, puis tu paies la livraison internationale vers la France.</p>
<div class="article-callout"><strong>Avant de cliquer sur Payer</strong>Garde le lien d’origine, vérifie la variante, et assure-toi que la ligne accepte l’article et que tu peux l’importer en France légalement.</div>
<h2 id="etape-1">1. Crée un compte sur Kakobuy</h2>
<p>Va sur l’<a class="text-link" href="https://ikako.vip/r/yze69" target="_blank" rel="noopener noreferrer">inscription Kakobuy</a> et choisis Sign Up. Renseigne l’e-mail, un mot de passe et toute vérification demandée par le service.</p>
<p>L’inscription peut inclure un pack de coupons. Vérifie valeur et conditions dans le compte ; il ne s’applique pas tout seul à n’importe quel achat.</p>
<h2 id="etape-2">2. Trouve le produit ou colle un lien</h2>
<p>Colle un lien copié ou cherche par mot-clé. Si tu as une URL Taobao, 1688 ou Weidian, colle-la dans Kakobuy et confirme que le bon produit s’affiche.</p>
<p>Tu peux aussi commencer par les <a class="text-link" href="/kakobuy-finds/">Finds</a> ou le <a class="text-link" href="/kakobuy-spreadsheet/">spreadsheet</a>. Un lien ne confirme ni qualité ni stock.</p>
<h2 id="etape-3">3. Choisis la variante et paie la commande</h2>
<p>Choisis couleur, taille et quantité. Pour les vêtements, suis les mesures du vendeur, pas seulement une taille lettre française. Le premier paiement n’est pas le prix final à domicile. La livraison internationale se paie ensuite, quand l’entrepôt connaît poids et dimensions.</p>
<h2 id="etape-4">4. Lis les photos QC à l’entrepôt</h2>
<p>Quand l’article est stocké, ouvre Warehouse et QC Picture. Compare couleur, étiquette de taille, quantité et détails visibles. Le QC montre des défauts visibles ; il ne prouve pas l’authenticité à lui seul.</p>
<div class="article-callout"><strong>Quelque chose ne correspond pas ?</strong>Ouvre un ticket au support avant la livraison internationale.</div>
<h2 id="etape-5">5. Ajoute une adresse en France et choisis la ligne</h2>
<p>Sélectionne les articles à expédier et ajoute la bonne adresse. Le pays doit être <strong>France</strong>. Vérifie nom, rue, code postal, ville et téléphone ; utilise l’indicatif <strong>+33</strong>.</p>
<p>Compare les lignes réellement proposées pour cette adresse et cette marchandise. Décide selon le prix, les restrictions, la taille, le poids et les conditions. Plus de détail : <a class="text-link" href="/livraison-kakobuy/">guide de livraison France</a>.</p>
<h2 id="etape-6">6. Confirme l’envoi et suis le colis</h2>
<p>Avant de confirmer, relis adresse, contenu, ligne et prix. Remplis les données douane avec exactitude. Après l’expédition, suis le numéro dans le compte Kakobuy. Le premier scan n’est pas toujours immédiat.</p>
<h2 id="erreurs">Erreurs fréquentes</h2>
<ul><li>Mauvaise taille sans regarder le tableau des mesures.</li><li>Sauter les photos QC.</li><li>Budgéter seulement le poids réel et oublier le volumétrique.</li><li>Acheter des articles avec restriction d’envoi ou d’importation.</li><li>Déclaration douanière inexacte.</li></ul>
<p class="legal-note">Ceci est une information générale. Confirme prix, stock, conditions de livraison et obligations d’importation sur Kakobuy et auprès des autorités françaises avant de payer.</p>
<p style="margin-top:30px"><a class="button" href="/kakobuy-finds/">Voir les finds →</a></p>
</article>
<aside class="toc"><strong>Guide</strong>
<a href="#etape-1">1. Créer un compte</a>
<a href="#etape-2">2. Trouver le produit</a>
<a href="#etape-3">3. Variante et paiement</a>
<a href="#etape-4">4. Lire le QC</a>
<a href="#etape-5">5. Adresse en France</a>
<a href="#etape-6">6. Envoi et suivi</a>
<a href="#erreurs">Erreurs fréquentes</a></aside></div>
"""
    return wrap(
        "how-to-use-kakobuy",
        "Comment acheter sur Kakobuy depuis la France – étape par étape",
        "Guide en français pour acheter avec Kakobuy : lien, commande, entrepôt, photos QC et livraison en France.",
        body,
        og_type="article",
    )


def page_shipping_fr() -> str:
    body = """
<section class="article-hero"><div class="container">
<span class="eyebrow">Livraison France · mise à jour 16.9.2026</span>
<h1>La ligne la moins chère n’est pas toujours le colis le moins cher</h1>
<p>Le poids facturable, les dimensions, le contenu et ce que le devis inclut décident du coût réel. Utilise cette liste pour comparer les offres.</p>
</div></section>
<div class="container article-layout"><article class="article">
<h2 id="flux">Comment fonctionne la livraison</h2>
<p>Les articles de différents vendeurs arrivent d’abord à l’entrepôt Kakobuy. Quand ils sont prêts, tu choisis ce qu’il faut envoyer ensemble, ajustes l’emballage et compares les lignes internationales vers la France.</p>
<h2 id="poids">Poids réel et volumétrique</h2>
<p>Le transporteur peut facturer le poids réel ou le volumétrique selon les dimensions. Un article léger mais volumineux peut coûter plus cher à cause du volume. Le diviseur et les règles varient selon la ligne.</p>
<div class="article-callout"><strong>Conseil pratique</strong>Sur les produits volumineux, envisage de retirer les cartons superflus ou d’utiliser un sac sous vide si cela n’abîme pas l’article.</div>
<h2 id="lignes">Comment comparer les lignes</h2>
<ul>
<li>Prix : compare le total, pas seulement le premier palier de poids.</li>
<li>Délai estimé : c’est une estimation, pas un jour garanti.</li>
<li>Limites de contenu : certaines lignes n’acceptent pas batteries, liquides, cosmétique ou certains matériaux.</li>
<li>Suivi et assurance : vérifie jusqu’où va le tracking et ce que couvre l’assurance.</li>
<li>Méthode de facturation : confirme poids réel vs volumétrique.</li>
</ul>
<h2 id="consolider">Consolidation et emballage</h2>
<p>Regrouper plusieurs articles dans un colis peut baisser les frais fixes, mais un carton plus grand n’est pas toujours moins cher. Le fragile a besoin de protection ; baskets ou vêtements peuvent souvent partir sans boîte d’origine si tu le demandes.</p>
<h2 id="tva">TVA et douane en France 2026</h2>
<p>Les envois hors UE nécessitent une déclaration et la TVA se liquide. Le taux général en France est de <strong>20 %</strong>. Depuis le 1.7.2026, beaucoup d’envois de vente à distance jusqu’à 150 € portent aussi un droit temporaire de <strong>3 € par position tarifaire</strong>. Une position peut regrouper plusieurs unités du même type ; ce n’est pas 3 € par pièce automatiquement. Au-dessus de 150 € s’applique le droit habituel.</p>
<p>La Poste ou un autre transporteur peut encaisser la TVA et des frais de gestion avant la livraison, sauf si la ligne est prépayée (IOSS / tax-paid). Si la TVA a déjà été payée via IOSS, elle ne devrait pas être recouvrée une seconde fois, mais les données IOSS doivent être transmises correctement.</p>
<p>Règles en vigueur : <a href="https://www.douane.gouv.fr/" target="_blank" rel="noopener noreferrer">douane.gouv.fr ↗</a> · <a href="https://www.economie.gouv.fr/particuliers/tva" target="_blank" rel="noopener noreferrer">TVA – economie.gouv.fr ↗</a></p>
<h2 id="suivi">Suivi</h2>
<p>Quand l’envoi est créé, un numéro de suivi apparaît souvent. Le trou entre l’étiquette et le premier scan physique est habituel. Sur certaines routes, le tracking s’éclaircit davantage à l’arrivée en Europe ou chez le dernier transporteur.</p>
<h2 id="check">Vérifie avant de payer le fret</h2>
<ul>
<li>J’ai vu les photos QC de tous les articles.</li>
<li>Je connais le poids et les dimensions finales.</li>
<li>J’ai relu les restrictions de la ligne.</li>
<li>Je comprends l’assurance et le suivi.</li>
<li>J’ai donné des données exactes pour le transport et la douane.</li>
</ul>
</article>
<aside class="toc"><strong>Sommaire</strong>
<a href="#flux">Comment ça marche</a>
<a href="#poids">Poids</a>
<a href="#lignes">Choisir une ligne</a>
<a href="#consolider">Consolidation</a>
<a href="#tva">TVA et douane</a>
<a href="#suivi">Suivi</a>
<a href="#check">Liste</a></aside></div>
"""
    return wrap(
        "livraison-kakobuy",
        "Livraison Kakobuy en France – poids, TVA 20 % et douane",
        "Comment fonctionne la livraison Kakobuy en France : consolidation, poids réel et volumétrique, TVA 20 %, droit de 3 € et IOSS.",
        body,
        og_type="article",
    )


def page_shipping_generic() -> str:
    body = """
<section class="article-hero"><div class="container">
<h1>Kakobuy shipping</h1>
<p>Guide général de livraison. Si tu commandes en France, utilise la page spécifique TVA et douane.</p>
</div></section>
<div class="container article-layout"><article class="article">
<p>Le fret se paie sur Kakobuy quand les articles sont en entrepôt. Compare le poids facturable, les restrictions et si la ligne déclare TVA ou droit prépayé.</p>
<p>Pour les acheteurs en France : <a class="text-link" href="/livraison-kakobuy/">livraison Kakobuy en France</a> (TVA 20 %, droit et suivi).</p>
</article></div>
"""
    return wrap(
        "kakobuy-shipping",
        "Kakobuy shipping — guide de livraison",
        "Kakobuy shipping : poids, consolidation et lien vers le guide de livraison France (TVA 20 %).",
        body,
        og_type="article",
    )


def page_coupon() -> str:
    body = """
<section class="article-hero"><div class="container">
<h1>Coupon Kakobuy et campagnes</h1>
<p>Officiel sur kakobuy.com le 16.9.2026 : code <strong>KAKOSEP</strong> (pack 1300 CNY + 10 % extra livraison jusqu’au 30.9), pack nouvel utilisateur 3000 CNY, et crédit de subvention 10 % utilisable jusqu’au 31.10 s’il t’a déjà été accordé. Confirme toujours dans le compte.</p>
</div></section>
<div class="container article-layout"><article class="article">
<h2>KAKOSEP — pack 1300 CNY ≈ 167 € + 10 % extra livraison</h2>
<p>Campagne 2 de <a href="https://www.kakobuy.com/tipdetail?id=55" target="_blank" rel="noopener noreferrer">kakobuy.com/tipdetail?id=55</a>. Durée : <strong>8–30.9.2026</strong> (heure de Pékin). Le 16.9, on peut encore l’échanger.</p>
<p>Code : <strong>KAKOSEP</strong>. Chemin : Centre utilisateur → Coupons → Échanger. Le spreadsheet n’applique pas le code.</p>
<p>Le pack comprend (seuils en CNY de fret, selon Kakobuy) :</p>
<ul>
<li>1 × 10 % de livraison, sans minimum</li>
<li>1 × 300 CNY si la livraison dépasse 2000 CNY</li>
<li>1 × 200 CNY si elle dépasse 1500 CNY</li>
<li>1 × 150 CNY si elle dépasse 1000 CNY</li>
<li>2 × 100 CNY si elle dépasse 800 CNY</li>
<li>3 × 80 CNY si elle dépasse 500 CNY</li>
<li>3 × 50 CNY si elle dépasse 300 CNY</li>
<li>2 × 30 CNY si elle dépasse 21 CNY</li>
</ul>
<p>Les pourcentages ne se combinent pas entre eux : échange le pack et en caisse choisis le coupon qui réduit le plus.</p>
<h2>Nouvel utilisateur 3000 CNY ≈ 386 €</h2>
<p>Offre officielle sur Kakobuy.com : inscris-toi et reçois un pack de coupons (environ 3000 CNY / 410 USD). Ils apparaissent dans le portefeuille, souvent pour la livraison.</p>
<p>Inscris-toi avec le lien <a class="text-link" href="https://ikako.vip/r/yze69" target="_blank" rel="sponsored noopener noreferrer">ikako.vip/r/yze69</a>. Source : <a href="https://www.kakobuy.com/tipdetail?id=1" target="_blank" rel="noopener noreferrer">kakobuy.com/tipdetail?id=1</a>.</p>
<h2>Subvention sitewide 10 % — crédit jusqu’au 31.10.2026</h2>
<p>Campagne 1 de la même page : fenêtre pour <em>obtenir</em> la subvention 8–14.9.2026 (heure de Pékin). Kakobuy indique que le crédit déjà accordé peut servir jusqu’au <strong>31.10.2026</strong>. Le 16.9 n’est plus la fenêtre d’inscription ; vérifie le portefeuille et la fiche produit.</p>
<h2>Lignes UE</h2>
<p>Kakobuy annonce des lignes duty-free vers l’UE et un <strong>droit de 3 € par colis</strong> sur les positions éligibles. La TVA générale en France reste de 20 %. Voir le <a href="/livraison-kakobuy/">guide de livraison</a>.</p>
<h2>Inviter des amis / Share &amp; earn</h2>
<p>Prix en cash et invitations sont des campagnes du compte Kakobuy. Ils ne s’échangent pas sur ce site.</p>
<p><a class="button" href="https://www.kakobuy.com/tipdetail?id=55" target="_blank" rel="noopener noreferrer">Ouvrir September Savings / KAKOSEP</a>
<a class="button secondary" href="https://ikako.vip/r/yze69" target="_blank" rel="sponsored noopener noreferrer">S’inscrire</a></p>
</article></div>
"""
    return wrap(
        "kakobuy-coupon",
        "Coupon Kakobuy 2026 – KAKOSEP 1300 CNY et pack 3000 CNY",
        "Coupons Kakobuy pour la France : code KAKOSEP (pack 1300 CNY + 10 % livraison jusqu’au 30.9) et pack 3000 CNY pour les nouveaux. Confirme sur Kakobuy.",
        body,
        og_type="article",
    )


def page_qc() -> str:
    body = """
<section class="article-hero"><div class="container">
<h1>Photos QC Kakobuy</h1>
<p>Les photos de contrôle se font quand le produit est arrivé à l’entrepôt, avant la livraison internationale.</p>
</div></section>
<div class="container article-layout"><article class="article">
<p>Compare couleur, étiquette de taille, quantité, coutures et défauts visibles. Ne valide pas les photos à l’aveugle. Si quelque chose cloche, ouvre un ticket avant de payer la ligne.</p>
<p>Le QC ne prouve pas l’authenticité. Il aide à ne pas envoyer en France une couleur, une taille ou une pièce abîmée incorrectes.</p>
<p><a class="text-link" href="/how-to-use-kakobuy/#etape-4">Voir le QC dans le guide d’achat</a></p>
</article></div>
"""
    return wrap(
        "kakobuy-qc",
        "Kakobuy QC – comment lire les photos d’entrepôt",
        "Photos QC Kakobuy : quoi regarder sur les images d’entrepôt avant d’expédier en France.",
        body,
        og_type="article",
    )


def page_avis() -> str:
    body = f"""
<section class="article-hero"><div class="container">
<h1>Avis Kakobuy</h1>
<p>Cette page n’invente pas d’étoiles. La fiabilité se décide dans le compte, sur les photos QC et sur la ligne de livraison.</p>
</div></section>
<div class="container article-layout"><article class="article">
<p>Kakobuy est un agent d’achat qui opère : il achète, stocke, photographie et expédie. kakospreadsheet.fr n’est pas Kakobuy et ne remplace pas son support.</p>
<ul>
<li>Paie avec un moyen qui a une protection acheteur.</li>
<li>Lis le QC avant la livraison internationale.</li>
<li>Ne prends pas le hype des communautés pour un certificat de qualité.</li>
<li>La TVA 20 % et la douane en France sont des règles d’importation, pas un « bug Kakobuy ».</li>
</ul>
{faq_list_html(FAQ)}
<p><a class="button" href="/is-kakobuy-legit/">Kakobuy est-il fiable ?</a>
<a class="button secondary" href="/how-to-use-kakobuy/">Étapes d’achat</a></p>
</article></div>
"""
    return wrap(
        "avis-kakobuy",
        "Avis Kakobuy (2026) — est-il fiable ?",
        "Avis Kakobuy pour la France : sans notes inventées. Vérifie QC, paiement et douane toi-même.",
        body,
        og_type="article",
        json_ld=[json_ld_faq("Avis Kakobuy", f"{BASE}/avis-kakobuy/", FAQ)],
    )


def page_france() -> str:
    body = """
<section class="article-hero"><div class="container">
<h1>Kakobuy France</h1>
<p>Ce hub .fr se concentre sur les prix en euros, la livraison vers la France, le QC en entrepôt et le workflow spreadsheet avant d’expédier.</p>
</div></section>
<div class="container article-layout"><article class="article">
<ul class="check-list">
<li>Commence dans le spreadsheet, choisis 3–5 lignes, demande le QC à l’entrepôt.</li>
<li>Lis les notes TVA 20 % et douane avant un gros haul.</li>
<li>Inscris-toi seulement sur Kakobuy, pas sur ce site.</li>
</ul>
<p>Les recherches kako buy, kako-buy et kako spreadsheet pointent vers le même agent : Kakobuy. Le catalogue reste sur kakospreadsheet.fr.</p>
<p><a class="button" href="/kakobuy-spreadsheet/">Ouvrir le spreadsheet</a>
<a class="button secondary" href="/livraison-kakobuy/">Livraison et douane</a></p>
</article></div>
"""
    return wrap(
        "kakobuy-france",
        "Kakobuy France — guide pour acheteurs français",
        "Kakobuy France : spreadsheet avec prix en euros, QC et livraison vers la France. TVA 20 %.",
        body,
        og_type="article",
    )


def page_lululemon() -> str:
    body = """
<section class="article-hero"><div class="container">
<h1>Kakobuy Lululemon</h1>
<p>Les recherches kakobuy lululemon en France aboutissent au même catalogue live, filtré sur le mot Lululemon. Ce n’est pas une boutique Lululemon officielle.</p>
</div></section>
<div class="container article-layout"><article class="article">
<p>Ouvre le spreadsheet avec la requête <strong>lululemon</strong>, compare le prix indicatif en euros, puis ouvre l’offre sur Kakobuy. Vérifie taille, tissu et photos QC comme pour n’importe quel article.</p>
<p>Les finds Lululemon sont des listings marketplace. Authenticité, stock et restrictions d’envoi se confirment sur Kakobuy, pas ici.</p>
<p><a class="button" href="/kakobuy-spreadsheet/?q=lululemon">Chercher Lululemon dans le spreadsheet</a>
<a class="button secondary" href="/kakobuy-finds/">Vue cartes</a></p>
</article></div>
"""
    return wrap(
        "kakobuy-lululemon",
        "Kakobuy Lululemon — finds dans le spreadsheet France",
        "Kakobuy Lululemon : cherche les finds dans le spreadsheet France, prix en euros, ouverture sur Kakobuy.",
        body,
        og_type="article",
    )


def page_legit() -> str:
    body = f"""
<section class="article-hero"><div class="container">
<h1>Is Kakobuy legit ?</h1>
<p>Version anglaise de la question de confiance. Pour le détail en français, lis les avis.</p>
</div></section>
<div class="container article-layout"><article class="article">
<p>Kakobuy is a working purchasing agent. kakospreadsheet.fr is not Kakobuy support. Pay with buyer protection, read QC photos, and budget French import VAT at 20 %.</p>
<p>Kakobuy est un agent d’achat opérationnel. Paie avec une protection acheteur, lis les photos QC, et prévois la TVA d’importation à 20 %.</p>
{faq_list_html(FAQ[-2:])}
<p><a class="button" href="/avis-kakobuy/">Avis Kakobuy</a>
<a class="button secondary" href="/livraison-kakobuy/">Livraison et TVA</a></p>
</article></div>
"""
    return wrap(
        "is-kakobuy-legit",
        "Is Kakobuy legit ? — notes pour la France",
        "Is Kakobuy legit pour les acheteurs en France ? Notes indépendantes : QC, protection de paiement et TVA 20 %.",
        body,
        og_type="article",
    )


def page_safe() -> str:
    body = """
<section class="article-hero"><div class="container">
<h1>Is Kakobuy safe ?</h1>
<p>La sécurité pratique tient au moyen de paiement, aux photos QC et à ne pas ignorer les restrictions de ligne.</p>
</div></section>
<div class="container article-layout"><article class="article">
<p>Ce site ne traite pas les paiements. Utilise une protection acheteur sur Kakobuy et ne valide pas le QC à l’aveugle.</p>
<p><a class="text-link" href="/avis-kakobuy/">Guide de confiance en français</a></p>
</article></div>
"""
    return wrap(
        "is-kakobuy-safe",
        "Is Kakobuy safe ? — France",
        "Is Kakobuy safe : paie avec protection, lis le QC et vérifie les restrictions d’envoi vers la France.",
        body,
        og_type="article",
    )


def page_discord() -> str:
    body = """
<section class="article-hero"><div class="container">
<h1>Kakobuy Discord et chats</h1>
<p>Les serveurs communautaires ne sont pas officiels. Traite les captures QC comme des anecdotes, pas comme un certificat.</p>
</div></section>
<div class="container article-layout"><article class="article">
<p>Utilise le spreadsheet et les photos QC Kakobuy comme journal d’achat. Les fils Discord, Telegram ou Reddit peuvent être datés ou promotionnels.</p>
<p><a class="button" href="/avis-kakobuy/">Notes de confiance</a></p>
</article></div>
"""
    return wrap(
        "kakobuy-discord",
        "Kakobuy Discord — chats non officiels",
        "Kakobuy Discord et communautés non officielles. Les décisions viennent du QC d’entrepôt et du support Kakobuy.",
        body,
        og_type="article",
    )


SPELL_FAQ: list[tuple[str, str]] = [
    (
        "Kako buy et Kakobuy, c’est quoi la différence ?",
        "Aucune, à part l’orthographe. Kakobuy s’écrit en un mot. Beaucoup tapent kako buy, kako-buy ou kako buy spreadsheet.",
    ),
    (
        "Où est le kako spreadsheet ?",
        "Le catalogue live est /kakobuy-spreadsheet/. Les URL kako-spreadsheet et kako-buy-spreadsheet redirigent vers ce hub d’orthographe, puis vers le catalogue.",
    ),
    (
        "Faut-il un compte sur kakospreadsheet.fr ?",
        "Non. Le compte, le paiement et le fret se font sur Kakobuy. Ce site liste des liens et explique TVA 20 % et douane France.",
    ),
]


def page_kako_buy() -> str:
    body = f"""
<section class="article-hero"><div class="container">
<span class="eyebrow">Orthographe · kako buy / kako-buy</span>
<h1>Kako buy, c’est Kakobuy</h1>
<p>Si tu as cherché kako buy, kako-buy ou kako buy spreadsheet, tu es au bon endroit : l’agent s’écrit <strong>Kakobuy</strong>. Le catalogue France est sur ce site.</p>
</div></section>
<div class="container article-layout"><article class="article">
<p>Les espaces et les traits d’union cassent souvent le nom de marque. Kakobuy est un agent d’achat : tu colles un lien Weidian / Taobao / 1688, l’entrepôt réceptionne, tu lis le QC, puis tu paies une ligne vers la France.</p>
<ul class="check-list">
<li><strong>kako buy</strong> et <strong>kako-buy</strong> → même plateforme que Kakobuy.</li>
<li><strong>kako buy spreadsheet</strong> et <strong>kako-buy spreadsheet</strong> → le catalogue de liens, pas un Google Sheet figé.</li>
<li>Inscription et paiement uniquement sur Kakobuy, pas ici.</li>
</ul>
<p>Pour le tableau de produits : <a href="/kakobuy-spreadsheet/">Kakobuy spreadsheet</a>. Pour l’orthographe catalogue : <a href="/kako-spreadsheet/">kako spreadsheet</a>.</p>
{faq_list_html(SPELL_FAQ)}
<p><a class="button" href="https://ikako.vip/r/yze69" target="_blank" rel="sponsored noopener noreferrer">S’inscrire sur Kakobuy</a>
<a class="button secondary" href="/how-to-use-kakobuy/">Comment acheter</a></p>
</article></div>
"""
    return wrap(
        "kako-buy",
        "Kako buy / kako-buy — c’est Kakobuy (France)",
        "Kako buy et kako-buy désignent Kakobuy. Guide France : inscription, spreadsheet, QC et livraison. Aussi pour kako buy spreadsheet.",
        body,
        og_type="article",
        json_ld=[json_ld_faq("Kako buy", f"{BASE}/kako-buy/", SPELL_FAQ)],
    )


def page_kako_spreadsheet() -> str:
    body = f"""
<section class="article-hero"><div class="container">
<span class="eyebrow">Orthographe · kako spreadsheet</span>
<h1>Kako spreadsheet, kako-spreadsheet, kako-buy spreadsheet</h1>
<p>Ces recherches visent le <strong>Kakobuy spreadsheet</strong> : un catalogue de liens produits, avec prix indicatifs en euros, qui s’ouvre sur Kakobuy.</p>
</div></section>
<div class="container article-layout"><article class="article">
<p>Un « spreadsheet » Kakobuy n’est pas un fichier Excel à télécharger ici. C’est une liste cherchable : nom, catégorie, estimation en euros, bouton vers Kakobuy. Les variantes <strong>kako spreadsheet</strong>, <strong>kako-spreadsheet</strong> et <strong>kako-buy spreadsheet</strong> pointent vers le même flux.</p>
<ul class="check-list">
<li>Cherche par nom ou colle un lien Weidian dans le catalogue.</li>
<li>Les prix sont convertis depuis le CNY (BCE), hors fret et TVA 20 %.</li>
<li>QC, coupons KAKOSEP et ligne France se gèrent dans le compte Kakobuy.</li>
</ul>
<p>Les URL <code>/kako-buy-spreadsheet/</code> et <code>/kako-spreadsheets/</code> redirigent vers cette page pour regrouper l’orthographe, puis tu ouvres le catalogue live.</p>
{faq_list_html(SPELL_FAQ)}
<p><a class="button" href="/kakobuy-spreadsheet/">Ouvrir le Kakobuy spreadsheet</a>
<a class="button secondary" href="/kako-buy/">Kako buy = Kakobuy</a></p>
</article></div>
"""
    return wrap(
        "kako-spreadsheet",
        "Kako spreadsheet / kako-spreadsheet — catalogue Kakobuy France",
        "Kako spreadsheet, kako-spreadsheet et kako-buy spreadsheet : le Kakobuy spreadsheet France, recherchable, prix en euros.",
        body,
        og_type="article",
        json_ld=[json_ld_faq("Kako spreadsheet", f"{BASE}/kako-spreadsheet/", SPELL_FAQ)],
    )


def page_about() -> str:
    body = """
<section class="article-hero"><div class="container">
<h1>Guide pratique pour acheteurs en France</h1>
<p>Comment utiliser Kakobuy, comment marche la livraison, et des liens produits. Mis à jour le 16 septembre 2026.</p>
</div></section>
<div class="container article-layout"><article class="article">
<h2>Ce qu’il y a ici</h2>
<p>kakospreadsheet.fr est un guide indépendant en français pour utiliser Kakobuy. Nous expliquons les étapes d’achat, les photos d’entrepôt et comment choisir une ligne vers la France. Nous listons aussi des exemples de produits et des liens. Le site capte aussi les recherches kako buy et kako spreadsheet.</p>
<h2>Comment fonctionnent les liens</h2>
<p>Les liens produits ouvrent la fiche sur Kakobuy. Vérifie variante, prix et stock là-bas avant de commander.</p>
<p>Sur kakospreadsheet.fr tu n’achètes pas et tu ne paies pas. Nous n’avons pas de comptes client et nous n’opérons ni entrepôt ni transport.</p>
<h2>Indépendance et affiliation</h2>
<p>Nous ne sommes pas le site officiel ni le support de Kakobuy. Certains liens incluent un code d’affilié. Si les conditions sont remplies, ce site peut recevoir une commission. Détails : <a href="/affiliate-disclosure/">avis d’affiliation</a>.</p>
<h2>Comment lire les prix</h2>
<p>Les montants en euros sont des estimations, pas une offre de vente sur ce site. Choisir un produit ne signifie pas que nous l’avons testé ni vérifié l’authenticité.</p>
</article></div>
"""
    return wrap(
        "about",
        "À propos de kakospreadsheet.fr",
        "kakospreadsheet.fr est un guide indépendant pour la France sur Kakobuy : achat, QC et livraison.",
        body,
        og_type="article",
    )


def page_privacy() -> str:
    body = """
<section class="article-hero"><div class="container"><h1>Confidentialité</h1>
<p>Ce site est un guide statique. Nous n’ouvrons pas de comptes client et ne prenons pas de commandes.</p></div></section>
<div class="container article-layout"><article class="article">
<p>Il peut utiliser des cookies techniques ou des journaux serveur pour fonctionner. Achat et paiement se font sur Kakobuy, selon ses conditions.</p>
<p>Si tu nous écris par e-mail, nous utilisons le message seulement pour répondre.</p>
</article></div>
"""
    return wrap(
        "privacy-policy",
        "Confidentialité – Kakobuy Spreadsheet France",
        "Politique de confidentialité de kakospreadsheet.fr : guide statique, sans comptes sur ce site.",
        body,
        og_type="article",
    )


def page_affiliate() -> str:
    body = """
<section class="article-hero"><div class="container"><h1>Avis d’affiliation</h1>
<p>Les liens produits vers Kakobuy peuvent inclure un code d’affilié.</p></div></section>
<div class="container article-layout"><article class="article">
<p>Si tu commandes via un lien et que les conditions sont remplies, nous pouvons recevoir une commission. Ton prix n’augmente pas pour autant. Nous ne sommes pas le site officiel de Kakobuy.</p>
<p>Le catalogue n’est pas un certificat de qualité. Vérifie prix, variante, stock et règles d’importation avant de payer.</p>
</article></div>
"""
    return wrap(
        "affiliate-disclosure",
        "Avis d’affiliation – Kakobuy Spreadsheet France",
        "kakospreadsheet.fr utilise des liens d’affiliation. Une commission n’augmente pas ton prix.",
        body,
        og_type="article",
    )


def page_partner() -> str:
    body = """
<section class="article-hero"><div class="container"><h1>Partner disclosure</h1>
<p>Mêmes conditions d’affiliation que la page française.</p></div></section>
<div class="container article-layout"><article class="article">
<p>Voir l’<a href="/affiliate-disclosure/">avis d’affiliation</a>.</p>
</article></div>
"""
    return wrap(
        "partner-disclosure",
        "Partner disclosure – Kakobuy Spreadsheet France",
        "Partner disclosure pour kakospreadsheet.fr. Voir la page d’affiliation française.",
        body,
        og_type="article",
    )


def page_contact() -> str:
    body = """
<section class="article-hero"><div class="container">
<h1>Contact</h1>
<p>Ce site ne gère pas les commandes Kakobuy. Les problèmes de commande relèvent du support Kakobuy.</p>
</div></section>
<div class="container article-layout"><article class="article">
<p>Questions sur ce site : <a href="mailto:support@kakobuytips.com">support@kakobuytips.com</a></p>
<p>Centre d’aide Kakobuy : <a href="https://www.kakobuy.com/help" target="_blank" rel="noopener noreferrer">kakobuy.com/help</a></p>
</article></div>
"""
    return wrap(
        "contact",
        "Contact – Kakobuy Spreadsheet France",
        "Contact de kakospreadsheet.fr. Les commandes se gèrent sur Kakobuy.",
        body,
        og_type="article",
    )


def page_terms() -> str:
    body = """
<section class="article-hero"><div class="container"><h1>Conditions</h1>
<p>Ce site publie un catalogue et un guide indépendants. Ce n’est pas une boutique.</p></div></section>
<div class="container article-layout"><article class="article">
<p>Le contenu est une information générale. Les conditions Kakobuy régissent comptes, paiements, entrepôt et fret. Les règles d’importation sont celles des autorités françaises.</p>
<p>Voir aussi l’<a href="/affiliate-disclosure/">avis d’affiliation</a> et la <a href="/privacy-policy/">confidentialité</a>.</p>
</article></div>
"""
    return wrap(
        "terms",
        "Conditions – Kakobuy Spreadsheet France",
        "Conditions de kakospreadsheet.fr : guide indépendant, ce n’est pas une boutique.",
        body,
        og_type="article",
    )


def page_404() -> str:
    return f"""<!doctype html>
<html lang="fr-FR"><head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Page introuvable – Kakobuy Spreadsheet France</title>
<meta name="robots" content="noindex">
<link rel="stylesheet" href="{esc(asset("assets/styles.css"))}">
<link rel="stylesheet" href="{esc(asset("assets/layout.css"))}">
<link rel="stylesheet" href="{esc(asset("assets/fi.css"))}">
</head><body>
<main class="article-hero"><div class="container">
<h1>Page introuvable</h1>
<p>Ouvre le spreadsheet ou reviens à l’accueil.</p>
<p><a class="button" href="/kakobuy-spreadsheet/">Spreadsheet</a>
<a class="button secondary" href="/">Accueil</a></p>
</div></main>
</body></html>
"""


def redirect_html(target: str) -> str:
    return f"""<!doctype html>
<html lang="fr-FR"><head>
<meta charset="utf-8">
<title>Redirection…</title>
<link rel="canonical" href="{esc(BASE + target)}">
<meta http-equiv="refresh" content="0;url={esc(target)}">
<script>location.replace({json.dumps(target)});</script>
</head><body><p><a href="{esc(target)}">Continuer</a></p></body></html>
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
        "name": "Kakobuy Spreadsheet France",
        "short_name": "Kakobuy.fr",
        "start_url": "/",
        "display": "browser",
        "lang": "fr-FR",
        "icons": [
            {"src": "/assets/favicon-v2-32.png", "sizes": "32x32", "type": "image/png"},
            {"src": "/assets/apple-touch-icon-v2.png", "sizes": "180x180", "type": "image/png"},
        ],
    }
    (out_dir / "site.webmanifest").write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def assert_quality(out_dir: Path) -> None:
    home = (out_dir / "index.html").read_text(encoding="utf-8")
    sheet = (out_dir / "kakobuy-spreadsheet" / "index.html").read_text(encoding="utf-8")
    ship = (out_dir / "livraison-kakobuy" / "index.html").read_text(encoding="utf-8")
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
        "para España",
        "21 %",
        "Abrir en Kakobuy",
        "como-comprar-en-kakobuy",
        "envio-kakobuy-espana",
    ):
        blob = home + sheet + ship + kako + kako_sheet
        if bad in blob:
            raise SystemExit(f"FR local site still contains {bad!r}")
    if 'lang="fr-FR"' not in home:
        raise SystemExit("home missing lang=fr-FR")
    if "/api/products.php" not in sheet:
        raise SystemExit("spreadsheet missing products API config")
    if "$_GET['q']" not in php or "item_id" not in php:
        raise SystemExit("products.php missing live search fields")
    if "Ouvrir sur Kakobuy" not in sheet:
        raise SystemExit("spreadsheet missing Kakobuy CTA")
    if "20 %" not in ship and "20%" not in ship:
        raise SystemExit("shipping page missing 20% VAT")
    if "douane.gouv.fr" not in ship:
        raise SystemExit("shipping page missing douane.gouv.fr")
    if "Spreadsheet" not in home or "Livraison" not in home:
        raise SystemExit("France nav missing")
    if "kb-promo" not in home or "kakobuy-logo.png" not in (out_dir / "assets" / "fi.css").read_text(
        encoding="utf-8"
    ):
        raise SystemExit("FR site missing Kakobuy promo strip or official logo")
    if "3000 CNY" not in home or "KAKOSEP" not in home:
        raise SystemExit("home missing latest Kakobuy coupon promo")
    if "w2clinks.com/spreadsheet" in home:
        raise SystemExit("FR home still sends catalog traffic to W2CLinks spreadsheet")
    if "kako buy" not in kako.lower() or "kako-buy" not in kako:
        raise SystemExit("kako-buy lander missing misspelling copy")
    if "kako spreadsheet" not in kako_sheet.lower():
        raise SystemExit("kako-spreadsheet lander missing misspelling copy")
    redir = (out_dir / "kako-buy-spreadsheet" / "index.html").read_text(encoding="utf-8")
    if "/kako-spreadsheet/" not in redir:
        raise SystemExit("kako-buy-spreadsheet should redirect to kako-spreadsheet")


def build_kakobuy_fr(out_dir: Path) -> int:
    catalog = load_catalog()
    RUNTIME["catalog"] = catalog
    RUNTIME["live"] = fetch_w2c_products(page=1, per_page=24)
    if out_dir.exists():
        shutil.rmtree(out_dir)
    out_dir.mkdir(parents=True)
    shutil.copytree(TEMPLATE_ASSETS, out_dir / "assets", ignore=shutil.ignore_patterns("products"))
    hero_src = FR_ASSETS / "hero.webp"
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
        "livraison-kakobuy": page_shipping_fr(),
        "kakobuy-shipping": page_shipping_generic(),
        "kakobuy-coupon": page_coupon(),
        "kakobuy-qc": page_qc(),
        "avis-kakobuy": page_avis(),
        "kakobuy-france": page_france(),
        "kakobuy-lululemon": page_lululemon(),
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
    n = build_kakobuy_fr(dest)
    print(f"Built {n} kakospreadsheet.fr files → {dest}")
