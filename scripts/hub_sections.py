"""Homepage hub blocks aligned with seo-factory partner resource standard."""

from __future__ import annotations

from datetime import date
from html import escape as esc

from scripts.i18n_ui import t as ui_t
from scripts.hub_icons import brand_icon, category_icon, flag_emoji, region_label
from scripts.link_helpers import (
    brand_url,
    category_url,
    main_spreadsheet_url,
    product_search_url,
)

SPREADSHEET = main_spreadsheet_url()

DEFAULT_CATEGORIES = [
    "SNEAKERS",
    "SLIPPERS",
    "BOOTS",
    "BAGS",
    "CLOTHING",
    "HOODIES",
    "JACKETS",
    "PANTS",
    "TSHIRTS",
    "ACCESSORIES",
    "WATCHES",
    "ELECTRONICS",
]

DEFAULT_BRANDS = [
    "NIKE",
    "ADIDAS",
    "JORDAN",
    "NEW BALANCE",
    "ASICS",
    "PUMA",
    "SUPREME",
    "STONE ISLAND",
    "BALENCIAGA",
    "LOUIS VUITTON",
]

GUIDE_LINKS = {
    "en": {
        "shipping": "orientdig-shipping/",
        "qc": "orientdig-qc/",
        "coupons": "orientdig-coupons/",
    },
    "nl": {
        "shipping": "orientdig-shipping/",
        "qc": "orientdig-qc/",
        "coupons": "orientdig-coupons/",
    },
    "de": {
        "shipping": "orientdig-shipping/",
        "qc": "orientdig-qc/",
        "coupons": "orientdig-coupons/",
    },
    "it": {
        "shipping": "orientdig-shipping/",
        "qc": "orientdig-qc/",
        "coupons": "orientdig-coupons/",
    },
    "fr": {
        "shipping": "livraison-orientdig/",
        "qc": "orientdig-qc/",
        "coupons": "orientdig-coupon/",
    },
    "es": {
        "shipping": "orientdig-shipping/",
        "qc": "orientdig-qc/",
        "coupons": "orientdig-coupons/",
    },
}


def _lang_ui(lang: str) -> str:
    return lang if lang in ("nl", "de", "it", "fr", "es") else "en"


def metrics_section(product_count: int, lang: str) -> str:
    ui = _lang_ui(lang)
    today = date.today().isoformat()
    return f"""<section class="hub-section">
  <div class="hub-grid hub-metrics">
    <div class="card hub-metric"><div class="metric">{product_count}</div><p>{esc(ui_t(ui, "hub_metric_finds"))}</p></div>
    <div class="card hub-metric"><div class="metric">12</div><p>{esc(ui_t(ui, "hub_metric_categories"))}</p></div>
    <div class="card hub-metric"><div class="metric">{esc(today)}</div><p>{esc(ui_t(ui, "hub_metric_updated"))}</p></div>
  </div>
</section>"""


DOMAIN_REGION = {
    "orientdig.us": "US",
    "orientdig.es": "ES",
    "orientdig.fr": "FR",
    "orientdig.at": "AT",
    "orientdigspreadsheet.us": "US",
    "orientdigspreadsheet.uk": "UK",
    "orientdigspreadsheet.nl": "NL",
    "orientdigspreadsheet.de": "DE",
    "orientdigspreadsheet.it": "IT",
    "orientdigspreadsheet.fr": "FR",
}


def category_grid(config: dict, lang: str) -> str:
    ui = _lang_ui(lang)
    cats = config.get("hub", {}).get("categories") or DEFAULT_CATEGORIES
    cards = ""
    for cat in cats:
        href = category_url(cat)
        icon = category_icon(cat)
        cards += (
            f'<a class="card hub-link-card hub-icon-card" href="{esc(href)}" target="_blank" rel="noopener">'
            f'<img class="hub-card-icon" src="{esc(icon)}" alt="{esc(cat)}" width="48" height="48" loading="lazy" decoding="async">'
            f"<strong>{esc(cat)}</strong>"
            f"<p>{esc(ui_t(ui, 'hub_open_category').format(cat=cat.title()))}</p></a>"
        )
    return f"""<section class="hub-section">
  <h2>{esc(ui_t(ui, "hub_categories"))}</h2>
  <div class="hub-grid hub-grid-4">{cards}</div>
</section>"""


def brand_grid(config: dict, lang: str) -> str:
    ui = _lang_ui(lang)
    brands = config.get("hub", {}).get("brands") or DEFAULT_BRANDS
    cards = ""
    for brand in brands:
        href = brand_url(brand)
        icon = brand_icon(brand)
        cards += (
            f'<a class="card hub-link-card hub-icon-card" href="{esc(href)}" target="_blank" rel="noopener">'
            f'<img class="hub-card-icon hub-brand-icon" src="{esc(icon)}" alt="{esc(brand)}" width="48" height="48" loading="lazy" decoding="async">'
            f"<strong>{esc(brand)}</strong>"
            f"<p>{esc(ui_t(ui, 'hub_browse_brand').format(brand=brand.title()))}</p></a>"
        )
    return f"""<section class="hub-section">
  <h2>{esc(ui_t(ui, "hub_brands"))}</h2>
  <div class="hub-grid hub-grid-4">{cards}</div>
</section>"""


def spreadsheet_table(products: list[dict], lang: str, currency_code: str) -> str:
    ui = _lang_ui(lang)
    if not products:
        return ""
    rows = ""
    for p in products[:10]:
        title = esc(p.get("title") or "Find")
        cat = esc(p.get("category") or "—")
        brand = esc(p.get("brand") or "—")
        price = p.get("price_cny")
        price_cell = (
            f'<span class="od-price" data-price-cny="{esc(str(price))}"></span>'
            if price is not None
            else "—"
        )
        kw = p.get("title") or ""
        href = product_search_url(kw) if kw else SPREADSHEET
        rows += f"""<tr>
  <td>{title}</td><td>{cat}</td><td>{brand}</td><td>{price_cell}</td>
  <td><a class="btn btn-primary btn-sm" href="{esc(href)}" target="_blank" rel="noopener">{esc(ui_t(ui, "products_open"))}</a></td>
</tr>"""
    return f"""<section class="hub-section">
  <h2>{esc(ui_t(ui, "hub_preview"))}</h2>
  <p>{esc(ui_t(ui, "hub_preview_sub"))}</p>
  <div class="table-wrap"><table class="od-table">
    <thead><tr><th>{esc(ui_t(ui, "hub_col_product"))}</th><th>{esc(ui_t(ui, "hub_col_category"))}</th>
    <th>{esc(ui_t(ui, "hub_col_brand"))}</th><th>{esc(ui_t(ui, "hub_col_price"))}</th><th>{esc(ui_t(ui, "hub_col_action"))}</th></tr></thead>
    <tbody>{rows}</tbody>
  </table></div>
</section>"""


def guide_trio(home_prefix: str, lang: str) -> str:
    ui = _lang_ui(lang)
    links = GUIDE_LINKS.get(_lang_ui(lang), GUIDE_LINKS["en"])
    items = [
        ("hub_guide_shipping", links["shipping"]),
        ("hub_guide_qc", links["qc"]),
        ("hub_guide_coupons", links["coupons"]),
    ]
    cards = ""
    for key, path in items:
        cards += (
            f'<a class="card hub-link-card" href="{esc(home_prefix + path)}">'
            f"<strong>{esc(ui_t(ui, key))}</strong><p>{esc(ui_t(ui, key + '_sub'))}</p></a>"
        )
    return f"""<section class="hub-section">
  <h2>{esc(ui_t(ui, "hub_guides"))}</h2>
  <div class="hub-grid hub-grid-3">{cards}</div>
</section>"""


def country_versions(config: dict, current_domain: str, lang: str) -> str:
    ui = _lang_ui(lang)
    cards = ""
    for entry in config.get("languages", []):
        dom = entry.get("domain", "")
        if not dom:
            continue
        label = entry.get("label", dom)
        region = DOMAIN_REGION.get(dom, "")
        flag_html = (
            f'<span class="od-flag-emoji" aria-hidden="true">{flag_emoji(region)}</span>'
            if region
            else ""
        )
        cards += (
            f'<a class="card hub-link-card hub-icon-card" href="https://{esc(dom)}/" target="_blank" rel="noopener">'
            f"{flag_html}<strong>{esc(label)}</strong><p>{esc(dom)}</p></a>"
        )
    return f"""<section class="hub-section">
  <h2>{esc(ui_t(ui, "hub_countries"))}</h2>
  <div class="hub-grid hub-grid-4">{cards}</div>
</section>"""


def render_home_hub(
    *,
    products: list[dict],
    lang: str,
    region: str,
    home_prefix: str,
    site_config: dict,
    domain: str,
    default_currency: str,
) -> str:
    return (
        category_grid(site_config, lang)
        + brand_grid(site_config, lang)
        + spreadsheet_table(products, lang, default_currency)
        + guide_trio(home_prefix, lang)
    )
