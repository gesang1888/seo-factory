"""W2CLinks CDN icons for category and brand hub cards."""

from __future__ import annotations

W2C_BASE = "https://w2clinks.com"

CATEGORY_ICONS: dict[str, str] = {
    "SNEAKERS": "/public/static/w2c/categories/cat-30-shoes.png",
    "SLIPPERS": "/public/static/w2c/categories/cat-27-slippers.png",
    "BOOTS": "/public/static/w2c/categories/cat-30-shoes.png",
    "BAGS": "/public/static/w2c/categories/cat-00-bag.png",
    "CLOTHING": "/public/static/w2c/categories/cat-14-cotton-ciothes.png",
    "HOODIES": "/public/static/w2c/categories/cat-06-hoodie.png",
    "JACKETS": "/public/static/w2c/categories/cat-13-jacket.png",
    "PANTS": "/public/static/w2c/categories/cat-19-trousers.png",
    "TSHIRTS": "/public/static/w2c/categories/cat-03-t-shirt.png",
    "ACCESSORIES": "/public/static/w2c/categories/cat-02-jewelry.png",
    "WATCHES": "/public/static/w2c/categories/cat-02-jewelry.png",
    "ELECTRONICS": "/public/static/w2c/categories/cat-15-giove.png",
}

BRAND_ICONS: dict[str, str] = {
    "NIKE": "/public/static/w2c/brands/brand-011-nk.png",
    "ADIDAS": "/public/static/w2c/brands/brand-031-aias.png",
    "JORDAN": "/public/static/w2c/brands/brand-030-ar-jran.png",
    "NEW BALANCE": "/public/static/w2c/brands/brand-168-nw-daane.png",
    "ASICS": "/public/static/w2c/brands/brand-267-asics.png",
    "PUMA": "/public/static/w2c/brands/brand-215-puma.png",
    "SUPREME": "/public/static/w2c/brands/brand-022-sre.png",
    "STONE ISLAND": "/public/static/w2c/brands/brand-028-s-id.png",
    "BALENCIAGA": "/public/static/w2c/brands/brand-074-bliaa.png",
    "LOUIS VUITTON": "/public/static/w2c/brands/brand-068-l.png",
}

REGION_FLAGS: dict[str, dict[str, str]] = {
    "US": {"code": "us", "emoji": "🇺🇸", "label": "United States"},
    "ES": {"code": "es", "emoji": "🇪🇸", "label": "Spain"},
    "FR": {"code": "fr", "emoji": "🇫🇷", "label": "France"},
    "AT": {"code": "at", "emoji": "🇦🇹", "label": "Austria"},
    "UK": {"code": "gb", "emoji": "🇬🇧", "label": "United Kingdom"},
    "NL": {"code": "nl", "emoji": "🇳🇱", "label": "Netherlands"},
    "DE": {"code": "de", "emoji": "🇩🇪", "label": "Germany"},
    "IT": {"code": "it", "emoji": "🇮🇹", "label": "Italy"},
}


def icon_url(path: str) -> str:
    if path.startswith("http"):
        return path
    return W2C_BASE + path


def category_icon(category: str) -> str:
    return icon_url(CATEGORY_ICONS.get(category.upper(), CATEGORY_ICONS["CLOTHING"]))


def brand_icon(brand: str) -> str:
    return icon_url(BRAND_ICONS.get(brand.upper(), BRAND_ICONS["NIKE"]))


def flag_img(region: str, size: int = 24) -> str:
    meta = REGION_FLAGS.get(region, {"code": "us", "emoji": "🌐", "label": region})
    code = meta["code"]
    return f"https://flagcdn.com/w{size}/{code}.png"


def flag_emoji(region: str) -> str:
    return REGION_FLAGS.get(region, {}).get("emoji", "🌐")


def region_label(region: str) -> str:
    return REGION_FLAGS.get(region, {}).get("label", region)


def brand_flag_markup(region: str) -> str:
    """Small flag shown under the header logo for the site region."""
    if region not in REGION_FLAGS:
        return ""
    emoji = flag_emoji(region)
    label = region_label(region)
    img = flag_img(region, 40)
    return (
        f'<span class="brand-flag" title="{label}">'
        f'<img class="brand-flag-img" src="{img}" alt="{label}" width="28" height="21" loading="lazy" '
        f'onerror="this.hidden=true;this.nextElementSibling.hidden=false">'
        f'<span class="brand-flag-emoji" hidden>{emoji}</span>'
        f"</span>"
    )

