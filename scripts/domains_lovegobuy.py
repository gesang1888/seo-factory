"""Lovegobuy cluster — 8 domains (2026-06 Semrush)."""

from __future__ import annotations

HREFLANG_LOVEGOBUY = {
    "es-ES": "https://lovegobuyspreadsheet.es",
    "it-IT": "https://lovegobuyspreadsheet.it",
    "nl-NL": "https://lovegobuyspreadsheet.nl",
    "en-CA": "https://lovegobuyspreadsheet.ca",
    "en": "https://lovegobuyguide.com",
    "x-default": "https://lovegobuyguide.com",
}

LOVEGOBUY_DOMAINS = {
    "lovegobuyspreadsheet.es": {
        "locale": "es-ES",
        "lang": "es",
        "region": "ES",
        "region_label": "España",
        "priority": "P0",
        "role": "spreadsheet",
        "brand_volume": 2900,
        "spreadsheet_volume": 140,
    },
    "lovegobuyspreadsheet.it": {
        "locale": "it-IT",
        "lang": "it",
        "region": "IT",
        "region_label": "Italia",
        "priority": "P0",
        "role": "spreadsheet",
        "brand_volume": 480,
        "spreadsheet_volume": 20,
    },
    "lovegobuy.it": {
        "locale": "it-IT",
        "lang": "it",
        "region": "IT",
        "region_label": "Italia",
        "priority": "P1",
        "role": "brand",
        "brand_volume": 480,
        "spreadsheet_volume": 20,
    },
    "lovegobuyspreadsheet.nl": {
        "locale": "nl-NL",
        "lang": "nl",
        "region": "NL",
        "region_label": "Nederland",
        "priority": "P1",
        "role": "spreadsheet",
        "brand_volume": 140,
        "spreadsheet_volume": 30,
    },
    "lovegobuy.nl": {
        "locale": "nl-NL",
        "lang": "nl",
        "region": "NL",
        "region_label": "Nederland",
        "priority": "P1",
        "role": "brand",
        "brand_volume": 140,
        "spreadsheet_volume": 30,
    },
    "lovegobuyspreadsheet.ca": {
        "locale": "en-CA",
        "lang": "en",
        "region": "CA",
        "region_label": "Canada",
        "priority": "P1",
        "role": "spreadsheet",
        "brand_volume": 260,
        "spreadsheet_volume": 30,
    },
    "lovegobuyspreadsheet.eu": {
        "locale": "en",
        "lang": "en",
        "region": "EU",
        "region_label": "Europe",
        "priority": "P2",
        "role": "spreadsheet_eu",
        "brand_volume": None,
        "spreadsheet_volume": None,
    },
    "lovegobuyguide.com": {
        "locale": "en",
        "lang": "en",
        "region": "INT",
        "region_label": "International",
        "priority": "P0",
        "role": "guide",
        "brand_volume": None,
        "spreadsheet_volume": None,
        "x_default": True,
    },
}

COMMON_SLUGS = [
    "",
    "lovegobuy-spreadsheet",
    "lovegobuy-spreadsheets",
    "best-lovegobuy-spreadsheet",
    "lovegobuy-finds",
    "lovegobuy-coupon",
    "lovegobuy-coupons",
    "lovegobuy-shipping",
    "lovegobuy-qc",
    "is-lovegobuy-legit",
    "is-lovegobuy-safe",
    "how-to-use-lovegobuy",
    "lovegobuy-discord",
    "lovegobuy-review",
]

REGION_EXCLUSIVE_SLUGS: dict[str, list[str]] = {
    "ES": [
        "lovegobuy-opiniones",
        "es-lovegobuy-confiable",
        "envio-lovegobuy-espana",
        "como-comprar-en-lovegobuy",
    ],
    "IT": [
        "lovegobuy-recensioni",
        "spedizione-lovegobuy",
        "lovegobuy-italia",
    ],
    "NL": [
        "lovegobuy-ervaringen",
        "lovegobuy-verzending",
    ],
    "CA": [
        "lovegobuy-canada",
        "lovegobuy-shipping-to-canada",
        "lovegobuy-shipping-calculator",
    ],
    "EU": [
        "lovegobuy-europe",
        "lovegobuy-shipping-eu",
    ],
    "INT": [
        "lovegobuy-guide",
        "lovegobuy-spreadsheet-guide",
    ],
}

REGION_EXTRA_SLUGS: dict[str, list[str]] = {
    "ES": [],
    "IT": [],
    "NL": ["best-lovegobuy-spreadsheet"],
    "CA": ["lovegobuy-tracking", "lovegobuy-warehouse"],
    "EU": [],
    "INT": [],
}

# Brand domains: slimmer page set (homepage + core commercial pages)
BRAND_DOMAIN_SLUGS = [
    "",
    "lovegobuy-spreadsheet",
    "lovegobuy-coupon",
    "lovegobuy-shipping",
    "is-lovegobuy-legit",
    "how-to-use-lovegobuy",
]

PLURAL_REDIRECTS: dict[str, str] = {}

SLUG_KEYWORDS: dict[str, dict[str, list[str]]] = {
    "": {
        "en": ["lovegobuy"],
        "es": ["lovegobuy"],
        "it": ["lovegobuy"],
        "nl": ["lovegobuy"],
    },
    "lovegobuy-spreadsheet": {
        "en": ["lovegobuy spreadsheet", "spreadsheet lovegobuy"],
        "es": ["lovegobuy spreadsheet", "spreadsheet lovegobuy"],
        "it": ["lovegobuy spreadsheet", "spreadsheet lovegobuy"],
        "nl": ["lovegobuy spreadsheet"],
    },
    "lovegobuy-coupon": {
        "en": ["lovegobuy coupon", "lovegobuy coupon codes"],
        "es": ["cupon lovegobuy"],
        "it": ["lovegobuy coupon"],
        "nl": ["lovegobuy coupon"],
    },
    "is-lovegobuy-legit": {
        "en": ["is lovegobuy legit", "lovegobuy legit"],
        "es": ["lovegobuy es fiable", "lovegobuy opiniones"],
        "it": ["lovegobuy recensioni"],
        "nl": ["lovegobuy reviews"],
    },
    "lovegobuy-opiniones": {"es": ["lovegobuy opiniones"]},
    "lovegobuy-recensioni": {"it": ["lovegobuy recensioni"]},
    "lovegobuy-ervaringen": {"nl": ["lovegobuy reviews"]},
}


def slug_to_path(slug: str) -> str:
    if not slug:
        return "/"
    return f"/{slug}/"


def domain_slugs(region: str, role: str = "spreadsheet") -> list[str]:
    if role == "brand":
        slugs = list(BRAND_DOMAIN_SLUGS)
        slugs.extend(REGION_EXCLUSIVE_SLUGS.get(region, []))
    else:
        slugs = list(COMMON_SLUGS)
        slugs.extend(REGION_EXCLUSIVE_SLUGS.get(region, []))
        slugs.extend(REGION_EXTRA_SLUGS.get(region, []))
    seen: set[str] = set()
    out: list[str] = []
    for s in slugs:
        if s not in seen:
            seen.add(s)
            out.append(s)
    return out


def exclusive_slug_regions(slug: str) -> list[str] | None:
    for region, slugs in REGION_EXCLUSIVE_SLUGS.items():
        if slug in slugs:
            return [region]
    return None
