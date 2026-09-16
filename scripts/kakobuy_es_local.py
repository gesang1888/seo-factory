"""Build kakospreadsheet.es as a CZ-style local catalog site (EUR, Spain UX)."""

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

CATALOG_PATH = ROOT / "data" / "kakobuy-es-catalog.json"
TEMPLATE_ASSETS = ROOT / "templates" / "kakobuy-fi" / "assets"
ES_ASSETS = ROOT / "templates" / "kakobuy-es" / "assets"
API_PHP = ROOT / "templates" / "api" / "products.php"
DOMAIN = "kakospreadsheet.es"
BASE = f"https://{DOMAIN}"
TODAY = date.today().isoformat()
ASSET_V = "20260915b"
RUNTIME: dict = {}

NAV = [
    ("", "Inicio"),
    ("kakobuy-spreadsheet", "Spreadsheet"),
    ("kakobuy-finds", "Hallazgos"),
    ("como-comprar-en-kakobuy", "Cómo comprar"),
    ("envio-kakobuy-espana", "Envío"),
    ("kakobuy-coupon", "Cupones"),
]

PRIMARY_SLUGS = [
    "",
    "kakobuy-spreadsheet",
    "kakobuy-finds",
    "como-comprar-en-kakobuy",
    "envio-kakobuy-espana",
    "kakobuy-shipping",
    "kakobuy-coupon",
    "kakobuy-qc",
    "kakobuy-opiniones",
    "es-kakobuy-confiable",
    "kakobuy-app",
    "is-kakobuy-legit",
    "is-kakobuy-safe",
    "kakobuy-review",
    "kakobuy-discord",
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
    "how-to-use-kakobuy": "/como-comprar-en-kakobuy/",
    "kakobuy-shipping-calculator": "/envio-kakobuy-espana/",
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
    "locale": "es-ES",
    "product": "Producto",
    "productOne": "1 producto",
    "products": "productos",
    "other": "Otros",
    "priceOnKakobuy": "Precio en Kakobuy",
    "openOnKakobuy": "Abrir en Kakobuy ↗",
    "openAria": "Abrir {title} en Kakobuy (nueva pestaña)",
    "openAriaCard": "{title} — abrir en Kakobuy",
    "prev": "Anterior",
    "next": "Siguiente",
    "pageOf": "Página {current} / {pages}",
    "loadError": "No se pudieron cargar los productos. Inténtalo de nuevo en un momento.",
    "emptyCount": "0 productos",
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
    return "Precio en Kakobuy" if amount is None else f"≈ {amount} €"


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
        groups.setdefault(str(cat.get("group") or "Otros"), []).append(cat)
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
        "kakobuy-opiniones",
        "es-kakobuy-confiable",
        "envio-kakobuy-espana",
        "kakobuy-app",
        "como-comprar-en-kakobuy",
        "kakobuy-shipping",
        "kakobuy-discord",
        "is-kakobuy-safe",
        "kakobuy-review",
        "partner-disclosure",
        "terms",
    }
    path = "/" if not slug else f"/{slug}/"
    if slug in exclusive:
        loc = canonical(slug)
        return (
            f'<link rel="alternate" hreflang="es-ES" href="{esc(loc)}">\n'
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
<html lang="es-ES">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(description)}">
<link rel="canonical" href="{esc(canonical_url)}">
{hreflang_tags(slug)}
<meta property="og:site_name" content="Kakobuy Spreadsheet España">
<meta property="og:type" content="{esc(og_type)}">
<meta property="og:locale" content="es_ES">
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
<a class="skip-link" href="#contenido">Saltar al contenido</a>
<div class="kb-promo"><div class="container">KAKOSEP hasta el 30.9: pack 1300 CNY + 10 % envío · nuevos usuarios 3000 CNY · <a href="https://ikako.vip/r/yze69" target="_blank" rel="sponsored noopener noreferrer">Regístrate en Kakobuy</a></div></div>
<header class="site-header"><div class="container nav">
<a class="brand" href="/" aria-label="Kakobuy Spreadsheet España – inicio"><span class="brand-mark">K</span><span>Kakobuy <small>España</small></span></a>
<form class="kb-head-search" action="/kakobuy-spreadsheet/" method="get" role="search">
<label class="sr-only" for="kb-q">Buscar producto</label>
<input id="kb-q" type="search" name="q" placeholder="Busca un producto o pega un enlace" autocomplete="off">
<button type="submit">Buscar</button>
</form>
<div class="nav-actions">
<a class="button small" href="https://ikako.vip/r/yze69" target="_blank" rel="sponsored noopener noreferrer">Registrarse</a>
<button class="menu-button" type="button" aria-label="Abrir menú" aria-expanded="false">☰</button>
</div>
</div></header>
<nav class="kb-subnav" aria-label="Principal"><div class="container nav-links">{"".join(links)}</div></nav>
<main id="contenido">"""


def footer() -> str:
    return f"""</main>
<footer class="site-footer"><div class="container">
<div class="footer-grid">
<div><a class="brand" href="/"><span class="brand-mark">K</span><span>Kakobuy España</span></a>
<p class="footer-copy">Catálogo independiente en español y guía para comprar con Kakobuy desde España.</p></div>
<div class="footer-col"><strong>Guía</strong>
<a href="/como-comprar-en-kakobuy/">Cómo comprar</a>
<a href="/envio-kakobuy-espana/">Envío a España</a>
<a href="/kakobuy-opiniones/">Opiniones</a>
<a href="/es-kakobuy-confiable/">¿Es confiable?</a></div>
<div class="footer-col"><strong>Productos</strong>
<a href="/kakobuy-spreadsheet/">Spreadsheet</a>
<a href="/kakobuy-finds/">Hallazgos</a>
<a href="/kakobuy-coupon/">Cupones</a></div>
<div class="footer-col"><strong>Info</strong>
<a href="/about/">Acerca de</a>
<a href="/privacy-policy/">Privacidad</a>
<a href="/affiliate-disclosure/">Afiliados</a></div>
</div>
<div class="footer-bottom"><span>© <span data-year></span> kakospreadsheet.es</span>
<span>No es el sitio oficial de Kakobuy.</span></div>
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
            "name": "Kakobuy Spreadsheet España",
            "url": f"{BASE}/",
            "inLanguage": "es-ES",
            "description": "Kakobuy spreadsheet para España: enlaces de productos, precios orientativos en euros, QC y envío.",
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
            "inLanguage": "es-ES",
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
    label = (cats.get(p["category"]) or {}).get("label") or p["category"] or "Otros"
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
        f'aria-label="Abrir {esc(p["title"])} en Kakobuy (nueva pestaña)">Abrir en Kakobuy ↗</a></li>'
    )


def finds_card(p: dict, catalog: dict, cats: dict) -> str:
    label = (cats.get(p["category"]) or {}).get("label") or p["category"] or "Otros"
    rate = catalog["cny_per_eur"]
    href = kakobuy_url(p["item_id"], catalog["affcode"], p.get("shop") or "weidian")
    brand = f'<p class="catalog-advice">{esc(p["brand"])}</p>' if p.get("brand") else ""
    cny = format_cny(p.get("price_cny"))
    return f"""<article class="catalog-card" data-product-id="{esc(p["id"])}">
<a class="catalog-image" href="{esc(href)}" target="_blank" rel="sponsored noopener noreferrer" aria-label="{esc(p["title"])} — abrir en Kakobuy">
<img src="{esc(image_src(p["image"]))}" width="750" height="750" alt="{esc(p["title"])}" loading="lazy" decoding="async"><span>{esc(label)}</span></a>
<div class="catalog-body">
<h3>{esc(p["title"])}</h3>
<div class="catalog-meta"><strong>{esc(format_eur(p.get("price_cny"), rate))}</strong><small>{esc(cny)}</small></div>
{brand}
<a class="text-link" href="{esc(href)}" target="_blank" rel="sponsored noopener noreferrer">Abrir en Kakobuy ↗</a>
</div></article>"""


def rate_note(catalog: dict) -> str:
    return (
        f'Precios y enlaces comprobados el <time datetime="{esc(catalog["checked"])}">{esc(catalog["checked"])}</time>. '
        f'Tipo BCE del <time datetime="{esc(catalog["ecb_date"])}">{esc(catalog["ecb_date"])}</time>: '
        f'1 EUR ≈ {str(catalog["cny_per_eur"]).replace(".", ",")} CNY, redondeado al euro. '
        "Es el precio de catálogo del producto, sin envío internacional, tasas ni IVA de importación. "
        "Confirma la variante en Kakobuy antes de pagar."
    )


FAQ: list[tuple[str, str]] = [
    (
        "¿Qué es Kakobuy?",
        "Kakobuy es un agente de compra y envío. Pide el producto en marketplaces chinos compatibles, lo recibe en almacén, hace fotos QC y ofrece líneas internacionales a España.",
    ),
    (
        "¿kakospreadsheet.es vende productos?",
        "No. Este sitio es un catálogo y guía de afiliación independientes. La compra, el pago y el envío ocurren en Kakobuy y con los vendedores.",
    ),
    (
        "¿Cuánto cuesta el envío a España?",
        "Depende del peso real o volumétrico, las medidas, la línea y el contenido. El presupuesto en vivo aparece en tu cuenta de Kakobuy cuando los artículos están en almacén.",
    ),
    (
        "¿Qué son las fotos QC?",
        "Fotos de almacén tomadas antes del envío internacional. Sirven para comprobar color, talla, cantidad y defectos visibles.",
    ),
    (
        "¿Hay que pagar IVA y aduana en España?",
        "Sí, en envíos desde fuera de la UE. El IVA general en España es el 21 %. Desde el 1.7.2026, muchos envíos de hasta 150 € también llevan 3 € de arancel por partida arancelaria. Kakobuy puede ofrecer líneas duty-free: confírmalo en caja. Consulta la Agencia Tributaria.",
    ),
    (
        "¿Kakobuy es confiable?",
        "Kakobuy es una plataforma de agente operativa. Este sitio no es Kakobuy y no garantiza precio, calidad ni despacho. Paga con protección al comprador, lee las fotos QC y revisa las restricciones de la línea.",
    ),
]


def page_home(catalog: dict) -> str:
    cats = cat_map(catalog)
    found, live = RUNTIME.get("live") or (0, [])
    featured = live[:8]
    rate = catalog["cny_per_eur"]
    count_label = f"{format_count(found)}+" if found else "Miles de"
    cat_count = len(catalog["categories"])
    cards = []
    for p in featured:
        href = kakobuy_url(p["item_id"], catalog["affcode"], p.get("shop") or "weidian")
        label = (cats.get(p["category"]) or {}).get("label") or p["category"] or "Otros"
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
<span class="eyebrow">Enlaces de producto · precios en euros</span>
<h1>Kakobuy Spreadsheet<br><span class="gradient-text">para España</span></h1>
<p>Consulta el catálogo en un solo sitio. Busca por nombre, filtra categoría y compara precios orientativos en euros. El producto se abre en Kakobuy.</p>
<form class="kb-hero-search" action="/kakobuy-spreadsheet/" method="get" role="search">
<label class="sr-only" for="hero-q">Buscar en el spreadsheet</label>
<input id="hero-q" type="search" name="q" placeholder="Busca un producto, marca o pega un enlace de Weidian" autocomplete="off">
<button type="submit">Buscar</button>
</form>
<div class="hero-actions">
<a class="button" href="/kakobuy-spreadsheet/">Abrir spreadsheet <span aria-hidden="true">→</span></a>
<a class="button secondary" href="/como-comprar-en-kakobuy/">Cómo funciona la compra</a>
</div>
<div class="trust-row" aria-label="Ventajas">
<span><i class="check">✓</i> Sin cuenta en este sitio</span>
<span><i class="check">✓</i> Precios en euros</span>
<span><i class="check">✓</i> Notas de envío a España</span>
</div>
</div>
<div class="hero-visual hero-art">
<img class="hero-art-image" src="{esc(asset('assets/hero.webp'))}" width="1152" height="864" alt="Envío Kakobuy a España: almacén, QC y paquete" fetchpriority="high">
</div>
</div></section>
<section class="kb-offers"><div class="container">
<div class="section-heading"><p class="kicker">Kakobuy.com · septiembre 2026</p>
<h2>Ofertas actuales</h2>
<p>Campañas oficiales de Kakobuy. Condiciones, descuento y fechas se confirman en la cuenta antes de pagar.</p></div>
<div class="kb-offer-grid">
<a class="kb-offer" href="https://www.kakobuy.com/tipdetail?id=55" target="_blank" rel="noopener noreferrer">
<span class="kb-offer-tag">Código KAKOSEP</span>
<strong>Pack septiembre 1300 CNY ≈ 167 € + 10 % extra de envío</strong>
<p>Canjeable del 8 al 30.9.2026 (hora de Pekín). En Kakobuy: Centro de usuario → Cupones → Canjear, código <strong>KAKOSEP</strong>.</p>
<span class="text-link">Abrir campaña en Kakobuy ↗</span></a>
<a class="kb-offer" href="https://ikako.vip/r/yze69" target="_blank" rel="sponsored noopener noreferrer">
<span class="kb-offer-tag">Usuario nuevo</span>
<strong>Pack de cupones 3000 CNY ≈ 386 €</strong>
<p>Regístrate con el enlace de invitación. Los cupones aparecen en el monedero; el spreadsheet no los aplica solo.</p>
<span class="text-link">Registrarse ↗</span></a>
<a class="kb-offer" href="https://www.kakobuy.com/tipdetail?id=55" target="_blank" rel="noopener noreferrer">
<span class="kb-offer-tag">Subvención 10 %</span>
<strong>Crédito de envío del 8–14.9, usable hasta el 31.10.2026</strong>
<p>La ventana para obtener la subvención sitewide ya cerró. Si te la concedieron, Kakobuy indica que vale hasta el 31.10.2026.</p>
<span class="text-link">Ver reglas en Kakobuy ↗</span></a>
<a class="kb-offer" href="/envio-kakobuy-espana/">
<span class="kb-offer-tag">UE / España</span>
<strong>3 € de arancel / paquete y líneas duty-free</strong>
<p>Kakobuy ofrece líneas a la UE con arancel de unos 3 € por paquete en partidas elegibles. El IVA 21 % en España se resuelve en la importación.</p>
<span class="text-link">Envío a España →</span></a>
</div>
</div></section>
<section class="stats"><div class="container stats-grid">
<div class="stat"><strong>{esc(count_label)} productos</strong><span>Catálogo buscable en este sitio</span></div>
<div class="stat"><strong>{cat_count} categorías</strong><span>De zapatillas a accesorios</span></div>
<div class="stat"><strong>Precios en euros</strong><span>Orientativos, sin envío</span></div>
</div></section>
<section class="section"><div class="container">
<div class="section-heading"><p class="kicker">Últimos hallazgos</p>
<h2>Zapatillas, ropa y accesorios con enlaces Kakobuy</h2>
<p>Puedes buscar la lista completa por nombre o limitarla a una categoría.</p></div>
<div class="catalog-grid">{"".join(cards)}</div>
<p class="catalog-note">No somos el vendedor · comprueba precio y stock antes de pedir
<a class="text-link" href="/kakobuy-spreadsheet/">Kakobuy Spreadsheet · busca en todo el catálogo →</a></p>
<p class="catalog-price-note">{rate_note(catalog)}</p>
</div></section>
<section class="section soft"><div class="container">
<div class="section-heading"><h2>Catálogo, pedido y envío</h2>
<p>Más catálogo, los pasos de compra y el coste hasta España.</p></div>
<div class="card-grid">
<a class="card" href="/kakobuy-spreadsheet/"><div class="card-icon">▦</div><h3>Spreadsheet</h3>
<p>Categorías y enlaces cuando no quieres pasar una hora en marketplaces chinos.</p>
<span class="text-link">Abrir catálogo ↗</span></a>
<a class="card" href="/como-comprar-en-kakobuy/"><div class="card-icon">1</div><h3>Primer pedido</h3>
<p>Qué pagas ahora, qué pagas en almacén y por qué no conviene aprobar el QC a ciegas.</p></a>
<a class="card" href="/envio-kakobuy-espana/"><div class="card-icon">→</div><h3>Envío a España</h3>
<p>Peso real vs volumétrico, consolidación, seguimiento, IVA 21 % y arancel.</p></a>
</div></div></section>
<section class="section"><div class="container">
<div class="section-heading"><h2>Compra en seis pasos</h2>
<p>El artículo llega primero al almacén. La línea a España se elige después de las fotos.</p></div>
<div class="steps">
<div class="step"><h3>Encuentra el producto</h3><p>Elige un enlace del spreadsheet o una URL del marketplace.</p></div>
<div class="step"><h3>Pega el enlace</h3><p>Elige variante, talla, color y cantidad.</p></div>
<div class="step"><h3>Paga el artículo</h3><p>Tras el pago, el vendedor envía al almacén de Kakobuy.</p></div>
<div class="step"><h3>No te saltes el QC</h3><p>Compara color, etiquetas, cantidad y defectos visibles.</p></div>
<div class="step"><h3>Envía el paquete</h3><p>Consolida artículos y elige una línea a España.</p></div>
<div class="step"><h3>Sigue el envío</h3><p>Usa el número de seguimiento cuando el paquete salga.</p></div>
</div></div></section>
<section class="section soft"><div class="container split">
<div><h2>El spreadsheet es un mapa, no un sello de calidad</h2>
<p>El catálogo está en este sitio. En cada oferta sigues eligiendo Kakobuy como agente.</p>
<ul class="check-list"><li>Menos búsqueda manual</li><li>Enlace a la oferta original</li><li>Sin garantía de precio ni calidad</li></ul></div>
<div>{faq_list_html(FAQ[:4])}</div>
</div></section>
<section class="cta"><div class="container"><div class="cta-box">
<h2>¿Ya tienes un enlace de producto?</h2>
<p>Pégalo en el buscador de Kakobuy. Si aún buscas ideas, empieza por el spreadsheet.</p>
<a class="button" href="/kakobuy-spreadsheet/">Ver el catálogo</a>
</div></div></section>
"""
    json_ld_blocks = [json_ld_website()]
    if featured:
        json_ld_blocks.append(json_ld_itemlist("Catálogo de productos", featured, catalog))
    return wrap(
        "",
        "Kakobuy Spreadsheet España – productos, precios en euros y QC",
        "Kakobuy spreadsheet para España: busca por nombre, filtra categorías, precios orientativos en euros y enlaces que abren en Kakobuy. Guía independiente.",
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
    count_label = f"{format_count(found)} productos" if found else "Cargando…"
    body = f"""
<section class="container sheet-intro"><p class="kicker">Catálogo para España · buscable</p>
<h1>Kakobuy Spreadsheet para España</h1>
<p>Este es el spreadsheet que puedes buscar de verdad: enlaces en vivo, precios en euros y checkout en Kakobuy, no una captura de un Google Sheet ajeno.</p></section>
<section class="container sheet-content" aria-label="Lista de productos">
<div class="sheet-controls">
<div class="sheet-field"><label for="sheet-search">Buscar productos</label>
<input type="search" id="sheet-search" placeholder="p. ej. sudadera, mochila, Jordan" autocomplete="off" aria-controls="sheet-products"></div>
<div class="sheet-field"><label for="sheet-category">Categoría</label>
<select id="sheet-category" aria-controls="sheet-products"><option value="all">Todas las categorías</option>{options}</select></div>
<button type="button" class="sheet-reset">Quitar filtros</button>
<output id="sheet-count" aria-live="polite">{esc(count_label)}</output>
</div>
<p class="sheet-disclosure">Los precios son orientativos, sin envío ni otras tasas. Los enlaces son de afiliación; podemos recibir comisión.</p>
<ul id="sheet-products" class="sheet-products">{items}</ul>
<nav id="sheet-pager" class="sheet-pager" aria-label="Paginación" hidden></nav>
<p class="sheet-empty" role="status" hidden>No hay productos. Prueba un nombre más corto u otra categoría.</p>
<details class="sheet-method"><summary>Precios y fecha de comprobación</summary>
<p>{rate_note(catalog)}</p>
<p>Fotos y nombres salen de las ofertas. No hemos probado los artículos en físico; no se confirma autenticidad ni stock de almacén aquí. <a href="/affiliate-disclosure/">Aviso de afiliación</a></p>
</details>
</section>
<section class="section soft" id="categorias"><div class="container">
<div class="section-heading"><h2>Explorar por categoría</h2>
<p>Elige una categoría para filtrar esta página. El producto se abre en Kakobuy.</p></div>
<div class="sheet-categories">{extra}</div>
</div></section>
<section class="section"><div class="container sheet-help">
<div><h2>¿Qué es un Kakobuy spreadsheet?</h2>
<p>Una lista de enlaces de producto para comprar a través de Kakobuy. Navegas este catálogo en el navegador; cada fila tiene categoría y un precio en euros.</p>
<p>¿Prefieres tarjetas? Mira <a href="/kakobuy-finds/">Kakobuy Finds</a>.</p></div>
<div><h2>Qué hacer después de elegir</h2>
<p>Ábrelo en Kakobuy, comprueba variante y precio en vivo. Cuando esté en almacén, revisa las fotos QC y luego elige el envío a España.</p>
<p><a href="/como-comprar-en-kakobuy/">Guía del primer pedido</a> · <a href="/envio-kakobuy-espana/">Envío a España</a></p></div>
</div></section>
"""
    json_ld_blocks = []
    if live:
        json_ld_blocks.append(
            json_ld_itemlist("Kakobuy Spreadsheet – productos con precios en euros", live[:24], catalog)
        )
    return wrap(
        "kakobuy-spreadsheet",
        "Kakobuy Spreadsheet – productos con precios en euros",
        "Kakobuy spreadsheet para España: busca por nombre, filtra categoría, compara precios en euros y abre el producto en Kakobuy.",
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
<span class="eyebrow">Últimos hallazgos · precios en euros</span>
<h1>Kakobuy Finds</h1>
<p>Vista en tarjetas del catálogo. Para buscar más rápido abre el <a class="text-link" href="/kakobuy-spreadsheet/">Kakobuy Spreadsheet</a>.</p>
</div></section>
<section class="section finds-catalog"><div class="container">
<div class="catalog-context">
<p>Estimaciones sin envío ni otras tasas. Los enlaces son de afiliación; podemos recibir comisión.</p>
<details><summary>Precios, fecha y notas</summary>
<p>{rate_note(catalog)}</p></details>
</div>
<div class="catalog-filter" hidden>
<label for="catalog-category">Mostrar categoría</label>
<select id="catalog-category"><option value="all">Todas las categorías</option>{options}</select>
<output id="catalog-count">{esc(format_count(_found) + " productos") if _found else "Cargando…"}</output>
</div>
<div id="finds-grid" class="catalog-grid">{cards}</div>
<p class="finds-empty sheet-empty" role="status" hidden>No hay productos en esta categoría.</p>
<p class="catalog-price-note">{rate_note(catalog)}</p>
</div></section>
"""
    json_ld_blocks = []
    if live:
        json_ld_blocks.append(
            json_ld_itemlist("Kakobuy Finds – productos con precios en euros", live[:24], catalog)
        )
    return wrap(
        "kakobuy-finds",
        "Kakobuy Finds – productos con precios en euros",
        "Kakobuy Finds para España: últimos hallazgos con precios en euros y enlaces directos a Kakobuy.",
        body,
        extra_css=[asset("assets/catalog.css")],
        extra_js=[asset("assets/catalog-live.js"), asset("assets/finds.js")],
        json_ld=json_ld_blocks,
    )


def page_guide() -> str:
    body = """
<section class="article-hero"><div class="container">
<span class="eyebrow">6 pasos para España</span>
<h1>Cómo comprar en Kakobuy desde España</h1>
<p>Desde crear la cuenta hasta enviar el paquete. En kakospreadsheet.es no creas cuenta ni haces pedidos.</p>
</div></section>
<div class="container article-layout"><article class="article">
<p>Kakobuy se sitúa entre tú y el vendedor. La mercancía no llega directa a casa: pagas el artículo, entra en almacén, revisas fotos y luego pagas el envío internacional a España.</p>
<div class="article-callout"><strong>Antes de pulsar Pagar</strong>Ten el enlace original, comprueba la variante y asegúrate de que la línea acepta el artículo y de que puedes importarlo a España de forma legal.</div>
<h2 id="paso-1">1. Crea una cuenta en Kakobuy</h2>
<p>Ve al <a class="text-link" href="https://ikako.vip/r/yze69" target="_blank" rel="noopener noreferrer">registro de Kakobuy</a> y elige Sign Up. Completa el correo, una contraseña y cualquier verificación que pida el servicio.</p>
<p>El registro puede incluir un pack de cupones. Revisa valor y condiciones en la cuenta; no se aplica solo a cualquier compra.</p>
<h2 id="paso-2">2. Encuentra el producto o pega un enlace</h2>
<p>Pega un enlace copiado o busca por palabra clave. Si tienes una URL de Taobao, 1688 o Weidian, pégala en Kakobuy y confirma que carga el producto correcto.</p>
<p>También puedes empezar por <a class="text-link" href="/kakobuy-finds/">Hallazgos</a> o el <a class="text-link" href="/kakobuy-spreadsheet/">spreadsheet</a>. Un enlace no confirma calidad ni stock.</p>
<h2 id="paso-3">3. Elige variante y paga el pedido</h2>
<p>Elige color, talla y cantidad. En ropa, sigue las medidas del vendedor, no solo una talla de letra española. El primer pago no es el precio final a domicilio. El envío internacional se paga después, cuando el almacén conoce peso y medidas.</p>
<h2 id="paso-4">4. Revisa las fotos QC en el almacén</h2>
<p>Cuando el artículo está almacenado, abre Warehouse y QC Picture. Compara color, etiqueta de talla, cantidad y detalles visibles. El QC muestra fallos visibles; no demuestra autenticidad por sí solo.</p>
<div class="article-callout"><strong>¿Algo no coincide?</strong>Ábrelo con soporte antes del envío internacional.</div>
<h2 id="paso-5">5. Añade una dirección en España y elige línea</h2>
<p>Selecciona los artículos a enviar y añade la dirección correcta. El país debe ser <strong>España / Spain</strong>. Revisa nombre, calle, código postal, ciudad y teléfono; usa el prefijo <strong>+34</strong>.</p>
<p>Compara las líneas que realmente se ofrecen para esta dirección y esta mercancía. Decide por precio, restricciones, tamaño, peso y condiciones. Más detalle: <a class="text-link" href="/envio-kakobuy-espana/">guía de envío a España</a>.</p>
<h2 id="paso-6">6. Confirma el envío y haz seguimiento</h2>
<p>Antes de confirmar, revisa dirección, contenido, línea y precio. Rellena los datos de aduana con veracidad. Después del despacho, sigue el número en la cuenta de Kakobuy. El primer escaneo no siempre es inmediato.</p>
<h2 id="errores">Errores frecuentes</h2>
<ul><li>Talla incorrecta sin mirar la tabla de medidas.</li><li>Saltar las fotos QC.</li><li>Presupuestar solo el peso real y olvidar el volumétrico.</li><li>Comprar artículos con restricción de envío o importación.</li><li>Declaración aduanera inexacta.</li></ul>
<p class="legal-note">Esto es información general. Confirma precio, stock, condiciones de envío y obligaciones de importación en Kakobuy y en las autoridades españolas antes de pagar.</p>
<p style="margin-top:30px"><a class="button" href="/kakobuy-finds/">Ver hallazgos →</a></p>
</article>
<aside class="toc"><strong>Guía</strong>
<a href="#paso-1">1. Crear cuenta</a>
<a href="#paso-2">2. Encontrar producto</a>
<a href="#paso-3">3. Variante y pago</a>
<a href="#paso-4">4. Revisar QC</a>
<a href="#paso-5">5. Dirección en España</a>
<a href="#paso-6">6. Envío y seguimiento</a>
<a href="#errores">Errores frecuentes</a></aside></div>
"""
    return wrap(
        "como-comprar-en-kakobuy",
        "Cómo comprar en Kakobuy desde España – paso a paso",
        "Guía en español para comprar con Kakobuy: enlace, pedido, almacén, fotos QC y envío a España.",
        body,
        og_type="article",
    )


def page_shipping_es() -> str:
    body = """
<section class="article-hero"><div class="container">
<span class="eyebrow">Envío a España · actualizado 15.9.2026</span>
<h1>La línea más barata no siempre es el paquete más barato</h1>
<p>El peso facturable, las medidas, el contenido y lo que incluye el presupuesto deciden el coste real. Usa esta lista al comparar ofertas.</p>
</div></section>
<div class="container article-layout"><article class="article">
<h2 id="flujo">Cómo funciona el envío</h2>
<p>Los artículos de distintos vendedores llegan primero al almacén de Kakobuy. Cuando están listos, eliges qué enviar juntos, ajustas el embalaje y comparas las líneas internacionales a España.</p>
<h2 id="peso">Peso real y volumétrico</h2>
<p>El transportista puede facturar el peso real o el volumétrico según las medidas. Un artículo ligero pero voluminoso puede salir más caro por el volumen. El divisor y las reglas varían por línea.</p>
<div class="article-callout"><strong>Consejo práctico</strong>En productos voluminosos, valora quitar cajas extra o usar bolsa de vacío si no daña el artículo.</div>
<h2 id="lineas">Cómo comparar líneas</h2>
<ul>
<li>Precio: compara el total, no solo el primer tramo de peso.</li>
<li>Plazo estimado: es una estimación, no un día garantizado.</li>
<li>Límites de contenido: algunas líneas no aceptan baterías, líquidos, cosmética o ciertos materiales.</li>
<li>Seguimiento y seguro: comprueba hasta dónde llega el tracking y qué cubre el seguro.</li>
<li>Método de facturación: confirma peso real vs volumétrico.</li>
</ul>
<h2 id="consolidar">Consolidación y embalaje</h2>
<p>Juntar varios artículos en un paquete puede bajar tasas fijas, pero una caja más grande no siempre es más barata. Lo frágil necesita protección; zapatillas o ropa a menudo pueden ir sin caja original si lo pides.</p>
<h2 id="iva">IVA y aduana en España 2026</h2>
<p>Los envíos desde fuera de la UE necesitan declaración y se liquida el IVA. El tipo general en España es el <strong>21 %</strong>. Desde el 1.7.2026, muchos envíos de venta a distancia de hasta 150 € también llevan un arancel temporal de <strong>3 € por partida arancelaria</strong>. Una partida puede incluir varias unidades del mismo tipo; no son 3 € por cada pieza de forma automática. Por encima de 150 € se aplica el arancel habitual.</p>
<p>Correos u otro transportista puede cobrar el IVA y una tasa de gestión antes de entregar, salvo que la línea esté prepagada (IOSS / tax-paid). Si el IVA ya se pagó por IOSS, no debería cobrarse otra vez, pero los datos IOSS tienen que transmitirse bien.</p>
<p>Normas vigentes: <a href="https://sede.agenciatributaria.gob.es/" target="_blank" rel="noopener noreferrer">Agencia Tributaria ↗</a> · <a href="https://www.agenciatributaria.es/AEAT.internet/Inicio/La_Agencia_Tributaria/Aduanas_e_Impuestos_Especiales/_Presentacion/Aduanas_e_Impuestos_Especiales.shtml" target="_blank" rel="noopener noreferrer">Aduanas ↗</a></p>
<h2 id="seguimiento">Seguimiento</h2>
<p>Cuando se crea el envío suele aparecer un número de seguimiento. El hueco entre la etiqueta y el primer escaneo físico es habitual. En algunas rutas el tracking se aclara más al llegar a Europa o al último transportista.</p>
<h2 id="check">Comprueba antes de pagar el flete</h2>
<ul>
<li>He visto fotos QC de todos los artículos.</li>
<li>Conozco el peso y las medidas finales.</li>
<li>He revisado las restricciones de la línea.</li>
<li>Entiendo el seguro y el seguimiento.</li>
<li>He dado datos veraces para transporte y aduana.</li>
</ul>
</article>
<aside class="toc"><strong>Contenido</strong>
<a href="#flujo">Cómo funciona</a>
<a href="#peso">Peso</a>
<a href="#lineas">Elegir línea</a>
<a href="#consolidar">Consolidación</a>
<a href="#iva">IVA y aduana</a>
<a href="#seguimiento">Seguimiento</a>
<a href="#check">Lista</a></aside></div>
"""
    return wrap(
        "envio-kakobuy-espana",
        "Envío Kakobuy a España – peso, IVA 21 % y aduana",
        "Cómo funciona el envío Kakobuy a España: consolidación, peso real y volumétrico, IVA 21 %, arancel de 3 € e IOSS.",
        body,
        og_type="article",
    )


def page_shipping_generic() -> str:
    body = """
<section class="article-hero"><div class="container">
<h1>Kakobuy shipping</h1>
<p>Guía general de envío. Si pides a España, usa la página específica de aduana e IVA.</p>
</div></section>
<div class="container article-layout"><article class="article">
<p>El flete se paga en Kakobuy cuando los artículos están en almacén. Compara peso facturable, restricciones y si la línea declara IVA o arancel prepagado.</p>
<p>Para compradores en España: <a class="text-link" href="/envio-kakobuy-espana/">envío Kakobuy a España</a> (IVA 21 %, arancel y seguimiento).</p>
</article></div>
"""
    return wrap(
        "kakobuy-shipping",
        "Kakobuy shipping — guía de envío",
        "Kakobuy shipping: peso, consolidación y enlace a la guía de envío a España (IVA 21 %).",
        body,
        og_type="article",
    )


def page_coupon() -> str:
    body = """
<section class="article-hero"><div class="container">
<h1>Cupón Kakobuy y campañas</h1>
<p>Oficial en kakobuy.com el 15.9.2026: código <strong>KAKOSEP</strong> (pack 1300 CNY + 10 % extra de envío hasta el 30.9), pack nuevo usuario 3000 CNY, y crédito de subvención 10 % usable hasta el 31.10 si ya te lo concedieron. Confirma siempre en la cuenta.</p>
</div></section>
<div class="container article-layout"><article class="article">
<h2>KAKOSEP — pack 1300 CNY ≈ 167 € + 10 % extra de envío</h2>
<p>Campaña 2 de <a href="https://www.kakobuy.com/tipdetail?id=55" target="_blank" rel="noopener noreferrer">kakobuy.com/tipdetail?id=55</a>. Duración: <strong>8–30.9.2026</strong> (hora de Pekín). Hoy 15.9 todavía se puede canjear.</p>
<p>Código: <strong>KAKOSEP</strong>. Ruta: Centro de usuario → Cupones → Canjear. El spreadsheet no aplica el código.</p>
<p>El pack incluye (umbrales en CNY de flete, según Kakobuy):</p>
<ul>
<li>1 × 10 % de envío, sin mínimo</li>
<li>1 × 300 CNY si el envío supera 2000 CNY</li>
<li>1 × 200 CNY si supera 1500 CNY</li>
<li>1 × 150 CNY si supera 1000 CNY</li>
<li>2 × 100 CNY si supera 800 CNY</li>
<li>3 × 80 CNY si supera 500 CNY</li>
<li>3 × 50 CNY si supera 300 CNY</li>
<li>2 × 30 CNY si supera 21 CNY</li>
</ul>
<p>Los porcentajes no se combinan entre sí: canjea el pack y en caja elige el cupón que más descuente.</p>
<h2>Usuario nuevo 3000 CNY ≈ 386 €</h2>
<p>Oferta oficial en Kakobuy.com: regístrate y recibe un pack de cupones (unos 3000 CNY / 410 USD). Aparecen en el monedero, suele ser para envío.</p>
<p>Regístrate con el enlace <a class="text-link" href="https://ikako.vip/r/yze69" target="_blank" rel="sponsored noopener noreferrer">ikako.vip/r/yze69</a>. Fuente: <a href="https://www.kakobuy.com/tipdetail?id=1" target="_blank" rel="noopener noreferrer">kakobuy.com/tipdetail?id=1</a>.</p>
<h2>Subvención sitewide 10 % — crédito hasta el 31.10.2026</h2>
<p>Campaña 1 de la misma página: ventana para <em>obtener</em> la subvención 8–14.9.2026 (hora de Pekín). Kakobuy indica que el crédito ya concedido se puede usar hasta el <strong>31.10.2026</strong>. El 15.9 ya no es la ventana de alta; comprueba el monedero y la ficha del producto.</p>
<h2>Líneas UE</h2>
<p>Kakobuy anuncia líneas duty-free a la UE y un <strong>arancel de 3 € por paquete</strong> en partidas elegibles. El IVA general en España sigue siendo el 21 %. Ver <a href="/envio-kakobuy-espana/">guía de envío</a>.</p>
<h2>Invita amigos / Share &amp; earn</h2>
<p>Premios en efectivo e invitaciones son campañas de la cuenta Kakobuy. No se canjean en este sitio.</p>
<p><a class="button" href="https://www.kakobuy.com/tipdetail?id=55" target="_blank" rel="noopener noreferrer">Abrir September Savings / KAKOSEP</a>
<a class="button secondary" href="https://ikako.vip/r/yze69" target="_blank" rel="sponsored noopener noreferrer">Regístrate</a></p>
</article></div>
"""
    return wrap(
        "kakobuy-coupon",
        "Cupón Kakobuy 2026 – KAKOSEP 1300 CNY y pack 3000 CNY",
        "Cupones Kakobuy para España: código KAKOSEP (pack 1300 CNY + 10 % envío hasta el 30.9) y pack de 3000 CNY para nuevos usuarios. Confirma en Kakobuy.",
        body,
        og_type="article",
    )


def page_qc() -> str:
    body = """
<section class="article-hero"><div class="container">
<h1>Fotos QC de Kakobuy</h1>
<p>Las fotos de control se hacen cuando el producto ha llegado al almacén, antes del envío internacional.</p>
</div></section>
<div class="container article-layout"><article class="article">
<p>Compara color, etiqueta de talla, cantidad, costuras y defectos visibles. No apruebes las fotos a ciegas. Si algo no cuadra, abre un ticket antes de pagar la línea.</p>
<p>El QC no demuestra autenticidad. Ayuda a no enviar a España un color, talla o pieza dañada incorrectos.</p>
<p><a class="text-link" href="/como-comprar-en-kakobuy/#paso-4">Ver el QC en la guía de compra</a></p>
</article></div>
"""
    return wrap(
        "kakobuy-qc",
        "Kakobuy QC – cómo leer las fotos de almacén",
        "Fotos QC de Kakobuy: qué mirar en las imágenes de almacén antes de enviar a España.",
        body,
        og_type="article",
    )


def page_opiniones() -> str:
    body = f"""
<section class="article-hero"><div class="container">
<h1>Kakobuy opiniones</h1>
<p>Esta página no inventa estrellas. La fiabilidad se decide en la cuenta, en las fotos QC y en la línea de envío.</p>
</div></section>
<div class="container article-layout"><article class="article">
<p>Kakobuy es un agente de compra que opera: compra, almacena, fotografía y envía. kakospreadsheet.es no es Kakobuy ni sustituye su soporte.</p>
<ul>
<li>Paga con un método que tenga protección al comprador.</li>
<li>Lee el QC antes del envío internacional.</li>
<li>No tomes el hype de comunidades como certificado de calidad.</li>
<li>El IVA 21 % y la aduana en España son normas de importación, no un «fallo de Kakobuy».</li>
</ul>
<p><a class="button" href="/es-kakobuy-confiable/">¿Es Kakobuy confiable?</a>
<a class="button secondary" href="/como-comprar-en-kakobuy/">Pasos de compra</a></p>
</article></div>
"""
    return wrap(
        "kakobuy-opiniones",
        "Kakobuy opiniones (2026) — ¿es fiable?",
        "Opiniones Kakobuy para España: sin valoraciones inventadas. Revisa QC, pago y aduana tú mismo.",
        body,
        og_type="article",
    )


def page_confiable() -> str:
    body = f"""
<section class="article-hero"><div class="container">
<h1>¿Kakobuy es confiable?</h1>
<p>Sí es una plataforma de agente que funciona. Este sitio no es Kakobuy y no sustituye su atención al cliente.</p>
</div></section>
<div class="container article-layout"><article class="article">
{faq_list_html(FAQ)}
<p><a class="button" href="/como-comprar-en-kakobuy/">Cómo comprar</a>
<a class="button secondary" href="/envio-kakobuy-espana/">Envío e IVA</a></p>
</article></div>
"""
    return wrap(
        "es-kakobuy-confiable",
        "¿Kakobuy es confiable? (2026)",
        "¿Kakobuy es confiable en España? Sin notas inventadas. Revisa QC, método de pago e IVA 21 %.",
        body,
        og_type="article",
        json_ld=[json_ld_faq("¿Kakobuy es confiable?", f"{BASE}/es-kakobuy-confiable/", FAQ)],
    )


def page_legit() -> str:
    body = """
<section class="article-hero"><div class="container">
<h1>Is Kakobuy legit?</h1>
<p>Versión en inglés de la pregunta de confianza. Para el detalle en español, usa la página de opiniones.</p>
</div></section>
<div class="container article-layout"><article class="article">
<p>Kakobuy is a working purchasing agent. kakospreadsheet.es is not Kakobuy support. Pay with buyer protection, read QC photos, and budget Spanish import VAT at 21 %.</p>
<p><a class="button" href="/es-kakobuy-confiable/">¿Es confiable?</a>
<a class="button secondary" href="/kakobuy-opiniones/">Opiniones</a></p>
</article></div>
"""
    return wrap(
        "is-kakobuy-legit",
        "Is Kakobuy legit? — notas para España",
        "Is Kakobuy legit for buyers in Spain? Independent notes: QC, payment protection and 21% VAT.",
        body,
        og_type="article",
    )


def page_safe() -> str:
    body = """
<section class="article-hero"><div class="container">
<h1>Is Kakobuy safe?</h1>
<p>La seguridad práctica está en el método de pago, las fotos QC y no saltarse restricciones de línea.</p>
</div></section>
<div class="container article-layout"><article class="article">
<p>Este sitio no procesa pagos. Usa protección al comprador en Kakobuy y no apruebes el QC a ciegas.</p>
<p><a class="text-link" href="/es-kakobuy-confiable/">Guía de confianza en español</a></p>
</article></div>
"""
    return wrap(
        "is-kakobuy-safe",
        "Is Kakobuy safe? — España",
        "Is Kakobuy safe: paga con protección, revisa QC y comprueba restricciones de envío a España.",
        body,
        og_type="article",
    )


def page_review() -> str:
    body = """
<section class="article-hero"><div class="container">
<h1>Kakobuy review</h1>
<p>Reseña independiente: el agente compra, almacena y envía. La calidad del artículo es del vendedor, no de este spreadsheet.</p>
</div></section>
<div class="container article-layout"><article class="article">
<p>No publicamos una nota media inventada. Lee <a href="/kakobuy-opiniones/">opiniones</a> y la <a href="/como-comprar-en-kakobuy/">guía de compra</a>.</p>
</article></div>
"""
    return wrap(
        "kakobuy-review",
        "Kakobuy review (2026) — España",
        "Kakobuy review para España: sin estrellas inventadas. QC, envío e IVA 21 %.",
        body,
        og_type="article",
    )


def page_app() -> str:
    body = """
<section class="article-hero"><div class="container">
<h1>Kakobuy app</h1>
<p>El pedido, el QC y el flete se gestionan en la cuenta de Kakobuy (web o app oficial). Este sitio no tiene app propia.</p>
</div></section>
<div class="container article-layout"><article class="article">
<p>Descarga solo desde los canales que Kakobuy indique en <a href="https://www.kakobuy.com/" target="_blank" rel="noopener noreferrer">kakobuy.com</a>. El catálogo de este spreadsheet se usa en el navegador y abre el producto en Kakobuy.</p>
<p><a class="button" href="/kakobuy-spreadsheet/">Abrir spreadsheet</a>
<a class="button secondary" href="https://ikako.vip/r/yze69" target="_blank" rel="sponsored noopener noreferrer">Crear cuenta</a></p>
</article></div>
"""
    return wrap(
        "kakobuy-app",
        "Kakobuy app — cuenta oficial, no este sitio",
        "Kakobuy app: el pedido se hace en Kakobuy. kakospreadsheet.es es un catálogo web independiente.",
        body,
        og_type="article",
    )


def page_discord() -> str:
    body = """
<section class="article-hero"><div class="container">
<h1>Kakobuy Discord y chats</h1>
<p>Los servidores de comunidad no son oficiales. Trata las capturas de QC allí como anécdotas, no como certificado.</p>
</div></section>
<div class="container article-layout"><article class="article">
<p>Usa el spreadsheet y las fotos QC de Kakobuy como registro de compra. Hilos de Discord, Telegram o Reddit pueden estar desfasados o ser promocionales.</p>
<p><a class="button" href="/es-kakobuy-confiable/">Notas de confianza</a></p>
</article></div>
"""
    return wrap(
        "kakobuy-discord",
        "Kakobuy Discord — chats no oficiales",
        "Kakobuy Discord y comunidades no oficiales. Las decisiones salen del QC de almacén y del soporte de Kakobuy.",
        body,
        og_type="article",
    )


def page_about() -> str:
    body = """
<section class="article-hero"><div class="container">
<h1>Guía práctica para compradores en España</h1>
<p>Cómo usar Kakobuy, cómo funciona el envío y enlaces a productos. Actualizado el 15 de septiembre de 2026.</p>
</div></section>
<div class="container article-layout"><article class="article">
<h2>Qué hay aquí</h2>
<p>kakospreadsheet.es es una guía independiente en español para usar Kakobuy. Explicamos los pasos de compra, las fotos de almacén y cómo elegir una línea a España. También listamos ejemplos de producto y enlaces.</p>
<h2>Cómo funcionan los enlaces</h2>
<p>Los enlaces de producto abren la ficha en Kakobuy. Comprueba variante, precio y stock allí antes de pedir.</p>
<p>En kakospreadsheet.es no compras ni pagas. No tenemos cuentas de cliente ni operamos almacén ni transporte.</p>
<h2>Independencia y afiliación</h2>
<p>No somos el sitio oficial ni el soporte de Kakobuy. Algunos enlaces incluyen código de afiliado. Si se cumplen las condiciones, este sitio puede recibir comisión. Detalles: <a href="/affiliate-disclosure/">aviso de afiliación</a>.</p>
<h2>Cómo leer los precios</h2>
<p>Las cifras en euros son estimaciones, no una oferta de venta en este sitio. Elegir un producto no significa que lo hayamos probado ni verificado autenticidad.</p>
</article></div>
"""
    return wrap(
        "about",
        "Acerca de kakospreadsheet.es",
        "kakospreadsheet.es es una guía independiente para España sobre Kakobuy: compra, QC y envío.",
        body,
        og_type="article",
    )


def page_privacy() -> str:
    body = """
<section class="article-hero"><div class="container"><h1>Privacidad</h1>
<p>Este sitio es una guía estática. No abrimos cuentas de cliente ni tomamos pedidos.</p></div></section>
<div class="container article-layout"><article class="article">
<p>Puede usar cookies técnicas o registros del servidor para funcionar. La compra y el pago ocurren en Kakobuy, bajo sus términos.</p>
<p>Si nos escribes por correo, usamos el mensaje solo para responder.</p>
</article></div>
"""
    return wrap(
        "privacy-policy",
        "Privacidad – Kakobuy Spreadsheet España",
        "Política de privacidad de kakospreadsheet.es: guía estática, sin cuentas en este sitio.",
        body,
        og_type="article",
    )


def page_affiliate() -> str:
    body = """
<section class="article-hero"><div class="container"><h1>Aviso de afiliación</h1>
<p>Los enlaces de producto a Kakobuy pueden incluir un código de afiliado.</p></div></section>
<div class="container article-layout"><article class="article">
<p>Si pides a través de un enlace y se cumplen las condiciones, podemos recibir comisión. Tu precio no sube por ello. No somos el sitio oficial de Kakobuy.</p>
<p>El catálogo no es un certificado de calidad. Comprueba precio, variante, stock y normas de importación antes de pagar.</p>
</article></div>
"""
    return wrap(
        "affiliate-disclosure",
        "Aviso de afiliación – Kakobuy Spreadsheet España",
        "kakospreadsheet.es usa enlaces de afiliado. Una comisión no sube tu precio.",
        body,
        og_type="article",
    )


def page_partner() -> str:
    body = """
<section class="article-hero"><div class="container"><h1>Partner disclosure</h1>
<p>Same affiliate terms as the Spanish disclosure page.</p></div></section>
<div class="container article-layout"><article class="article">
<p>See <a href="/affiliate-disclosure/">aviso de afiliación</a>.</p>
</article></div>
"""
    return wrap(
        "partner-disclosure",
        "Partner disclosure – Kakobuy Spreadsheet España",
        "Partner disclosure for kakospreadsheet.es. See the Spanish affiliate page.",
        body,
        og_type="article",
    )


def page_contact() -> str:
    body = """
<section class="article-hero"><div class="container">
<h1>Contacto</h1>
<p>Este sitio no gestiona pedidos de Kakobuy. Los problemas de pedido corresponden al soporte de Kakobuy.</p>
</div></section>
<div class="container article-layout"><article class="article">
<p>Preguntas sobre esta web: <a href="mailto:support@kakobuytips.com">support@kakobuytips.com</a></p>
<p>Centro de ayuda de Kakobuy: <a href="https://www.kakobuy.com/help" target="_blank" rel="noopener noreferrer">kakobuy.com/help</a></p>
</article></div>
"""
    return wrap(
        "contact",
        "Contacto – Kakobuy Spreadsheet España",
        "Contacto de kakospreadsheet.es. Los pedidos se gestionan en Kakobuy.",
        body,
        og_type="article",
    )


def page_terms() -> str:
    body = """
<section class="article-hero"><div class="container"><h1>Términos</h1>
<p>Este sitio publica un catálogo y una guía independientes. No es una tienda.</p></div></section>
<div class="container article-layout"><article class="article">
<p>El contenido es información general. Los términos de Kakobuy rigen cuentas, pagos, almacén y flete. Las normas de importación las marcan las autoridades españolas.</p>
<p>Ver también el <a href="/affiliate-disclosure/">aviso de afiliación</a> y la <a href="/privacy-policy/">privacidad</a>.</p>
</article></div>
"""
    return wrap(
        "terms",
        "Términos – Kakobuy Spreadsheet España",
        "Términos de kakospreadsheet.es: guía independiente, no es una tienda.",
        body,
        og_type="article",
    )


def page_404() -> str:
    return f"""<!doctype html>
<html lang="es-ES"><head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Página no encontrada – Kakobuy Spreadsheet España</title>
<meta name="robots" content="noindex">
<link rel="stylesheet" href="{esc(asset("assets/styles.css"))}">
<link rel="stylesheet" href="{esc(asset("assets/layout.css"))}">
<link rel="stylesheet" href="{esc(asset("assets/fi.css"))}">
</head><body>
<main class="article-hero"><div class="container">
<h1>Página no encontrada</h1>
<p>Abre el spreadsheet o vuelve al inicio.</p>
<p><a class="button" href="/kakobuy-spreadsheet/">Spreadsheet</a>
<a class="button secondary" href="/">Inicio</a></p>
</div></main>
</body></html>
"""


def redirect_html(target: str) -> str:
    return f"""<!doctype html>
<html lang="es-ES"><head>
<meta charset="utf-8">
<title>Redirigiendo…</title>
<link rel="canonical" href="{esc(BASE + target)}">
<meta http-equiv="refresh" content="0;url={esc(target)}">
<script>location.replace({json.dumps(target)});</script>
</head><body><p><a href="{esc(target)}">Continuar</a></p></body></html>
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
        "name": "Kakobuy Spreadsheet España",
        "short_name": "Kakobuy.es",
        "start_url": "/",
        "display": "browser",
        "lang": "es-ES",
        "icons": [
            {"src": "/assets/favicon-v2-32.png", "sizes": "32x32", "type": "image/png"},
            {"src": "/assets/apple-touch-icon-v2.png", "sizes": "180x180", "type": "image/png"},
        ],
    }
    (out_dir / "site.webmanifest").write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def assert_quality(out_dir: Path) -> None:
    home = (out_dir / "index.html").read_text(encoding="utf-8")
    sheet = (out_dir / "kakobuy-spreadsheet" / "index.html").read_text(encoding="utf-8")
    ship = (out_dir / "envio-kakobuy-espana" / "index.html").read_text(encoding="utf-8")
    js = (out_dir / "assets" / "spreadsheet.js").read_text(encoding="utf-8")
    php = (out_dir / "api" / "products.php").read_text(encoding="utf-8")
    for bad in ("Search intent", "W2CLinks", "fansheets.com", "kakobuydocs.com", "ALV 24%", "CBSA"):
        if bad in home or bad in sheet or bad in ship:
            raise SystemExit(f"ES local site still contains {bad!r}")
    if 'lang="es-ES"' not in home:
        raise SystemExit("home missing lang=es-ES")
    if "/api/products.php" not in sheet:
        raise SystemExit("spreadsheet missing products API config")
    if "$_GET['q']" not in php or "item_id" not in php:
        raise SystemExit("products.php missing live search fields")
    if "Abrir en Kakobuy" not in js and "Abrir en Kakobuy" not in sheet:
        raise SystemExit("spreadsheet missing Kakobuy CTA")
    if "21 %" not in ship and "21%" not in ship:
        raise SystemExit("shipping page missing 21% VAT")
    if "Agencia Tributaria" not in ship:
        raise SystemExit("shipping page missing Agencia Tributaria")
    if "Spreadsheet" not in home or "Envío" not in home:
        raise SystemExit("Spain nav missing")
    if "kb-promo" not in home or "kakobuy-logo.png" not in (out_dir / "assets" / "fi.css").read_text(encoding="utf-8"):
        raise SystemExit("ES site missing Kakobuy promo strip or official logo")
    if "3000 CNY" not in home or "KAKOSEP" not in home:
        raise SystemExit("home missing latest Kakobuy coupon promo")
    if "w2clinks.com/spreadsheet" in home:
        raise SystemExit("ES home still sends catalog traffic to W2CLinks spreadsheet")


def build_kakobuy_es(out_dir: Path) -> int:
    catalog = load_catalog()
    RUNTIME["catalog"] = catalog
    RUNTIME["live"] = fetch_w2c_products(page=1, per_page=24)
    if out_dir.exists():
        shutil.rmtree(out_dir)
    out_dir.mkdir(parents=True)
    shutil.copytree(TEMPLATE_ASSETS, out_dir / "assets", ignore=shutil.ignore_patterns("products"))
    hero_src = ES_ASSETS / "hero.webp"
    if hero_src.is_file():
        shutil.copyfile(hero_src, out_dir / "assets" / "hero.webp")
    api_dir = out_dir / "api"
    api_dir.mkdir(parents=True)
    shutil.copyfile(API_PHP, api_dir / "products.php")

    pages = {
        "": page_home(catalog),
        "kakobuy-spreadsheet": page_spreadsheet(catalog),
        "kakobuy-finds": page_finds(catalog),
        "como-comprar-en-kakobuy": page_guide(),
        "envio-kakobuy-espana": page_shipping_es(),
        "kakobuy-shipping": page_shipping_generic(),
        "kakobuy-coupon": page_coupon(),
        "kakobuy-qc": page_qc(),
        "kakobuy-opiniones": page_opiniones(),
        "es-kakobuy-confiable": page_confiable(),
        "kakobuy-app": page_app(),
        "is-kakobuy-legit": page_legit(),
        "is-kakobuy-safe": page_safe(),
        "kakobuy-review": page_review(),
        "kakobuy-discord": page_discord(),
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
    n = build_kakobuy_es(dest)
    print(f"Built {n} kakospreadsheet.es files → {dest}")
