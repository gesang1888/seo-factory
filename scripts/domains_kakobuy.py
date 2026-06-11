"""Kakobuy cluster: kakospreadsheet.{es,fr,nl,ca} + kakobuy.fi

Slug matrix derived from Semrush keyword plans in sites/*/keyword-plan.md (2026-06).
"""

from __future__ import annotations

HREFLANG_KAKOBUY = {
    "es-ES": "https://kakospreadsheet.es",
    "fr-FR": "https://kakospreadsheet.fr",
    "nl-NL": "https://kakospreadsheet.nl",
    "en-CA": "https://kakospreadsheet.ca",
    "fi-FI": "https://kakobuy.fi",
    "x-default": "https://kakospreadsheet.ca",
}

KAKOBUY_DOMAINS = {
    "kakospreadsheet.es": {
        "locale": "es-ES",
        "lang": "es",
        "region": "ES",
        "region_label": "España",
        "priority": "P0",
        "brand_volume": 14800,
        "spreadsheet_volume": 480,
    },
    "kakospreadsheet.fr": {
        "locale": "fr-FR",
        "lang": "fr",
        "region": "FR",
        "region_label": "France",
        "priority": "P0",
        "brand_volume": 4400,
        "spreadsheet_volume": 320,
    },
    "kakospreadsheet.ca": {
        "locale": "en-CA",
        "lang": "en",
        "region": "CA",
        "region_label": "Canada",
        "priority": "P0",
        "brand_volume": 8100,
        "spreadsheet_volume": 1300,
        "x_default": True,
    },
    "kakospreadsheet.nl": {
        "locale": "nl-NL",
        "lang": "nl",
        "region": "NL",
        "region_label": "Nederland",
        "priority": "P1",
        "brand_volume": 2900,
        "spreadsheet_volume": 480,
    },
    "kakobuy.fi": {
        "locale": "fi-FI",
        "lang": "fi",
        "region": "FI",
        "region_label": "Suomi",
        "priority": "P2",
        "brand_volume": None,  # pending Semrush FI export
        "spreadsheet_volume": None,
    },
}

# Shared across all regions — maps to Semrush keyword clusters
COMMON_SLUGS = [
    "",  # kakobuy brand/nav
    "kakobuy-spreadsheet",  # kakobuy spreadsheet (core)
    "kakobuy-spreadsheets",  # plural variant → same content, canonical to singular
    "best-kakobuy-spreadsheet",  # best kakobuy spreadsheet (KD 3–12%)
    "kakobuy-finds",
    "kakobuy-coupon",  # coupon / coupon codes / cupon / kuponki
    "kakobuy-coupons",
    "kakobuy-shipping",  # shipping / ship / verzending / livraison / toimitus
    "kakobuy-qc",  # qc kakobuy
    "is-kakobuy-legit",  # legit / safe / betrouwbaar / confiable
    "is-kakobuy-safe",
    "how-to-use-kakobuy",
    "kakobuy-discord",  # discord / telegram / reddit
    "kakobuy-review",
]

# Country-exclusive slugs — canonical only on listed region(s)
REGION_EXCLUSIVE_SLUGS: dict[str, list[str]] = {
    "ES": [
        "kakobuy-opiniones",  # kakobuy opiniones 110 vol
        "es-kakobuy-confiable",  # kakobuy es confiable 40 vol
        "envio-kakobuy-espana",
        "kakobuy-app",  # kakobuy app 260 vol
    ],
    "FR": [
        "avis-kakobuy",  # kakobuy avis 70 vol
        "livraison-kakobuy",
        "kakobuy-france",
        "meilleur-kakobuy-spreadsheet",
    ],
    "NL": [
        "kakobuy-ervaringen",  # reviews + is kakobuy betrouwbaar
        "kakobuy-verzending",
        "best-kakobuy-spreadsheet",  # KD 3% — prioritize on NL (also in COMMON)
    ],
    "CA": [
        "kakobuy-canada",  # canada cluster 10 words
        "kakobuy-shipping-to-canada",
        "kakobuy-warehouse",  # warehouse cluster 10 words
        "kakobuy-shipping-calculator",
    ],
    "FI": [
        "kakobuy-kokemuksia",  # luotettava
        "kakobuy-toimitus",
        "kakobuy-suomi",
    ],
}

REGION_EXTRA_SLUGS: dict[str, list[str]] = {
    "ES": [],
    "FR": ["kakobuy-lululemon"],  # lululemon cluster 4 words
    "NL": [],
    "CA": [
        "kakobuy-payment-methods",
        "kakobuy-tracking",
    ],
    "FI": [],
}

# Primary keyword targets per slug (for title/H1 generation in pages_kakobuy.py)
SLUG_KEYWORDS: dict[str, dict[str, list[str]]] = {
    "": {
        "en": ["kakobuy"],
        "es": ["kakobuy", "kakobuy spreadsheet"],
        "fr": ["kakobuy"],
        "nl": ["kakobuy"],
        "fi": ["kakobuy"],
    },
    "kakobuy-spreadsheet": {
        "en": ["kakobuy spreadsheet", "kakobuy spreadsheets", "spreadsheet kakobuy"],
        "es": ["kakobuy spreadsheet", "kakobuy spreedsheet", "spreadsheet kakobuy"],
        "fr": ["kakobuy spreadsheet", "spreadsheet kakobuy"],
        "nl": ["kakobuy spreadsheet", "kakobuy spreadsheet 2025", "spreadsheet kakobuy"],
        "fi": ["kakobuy spreadsheet"],
    },
    "best-kakobuy-spreadsheet": {
        "en": ["best kakobuy spreadsheet", "kakobuy spreadsheet 2025"],
        "nl": ["best kakobuy spreadsheet", "beste kakobuy spreadsheet"],
        "es": ["mejor kakobuy spreadsheet"],
        "fr": ["meilleur kakobuy spreadsheet"],
        "fi": ["paras kakobuy spreadsheet"],
    },
    "kakobuy-coupon": {
        "en": ["kakobuy coupon codes", "kakobuy coupons", "how to use coupons on kakobuy"],
        "es": ["cupon kakobuy", "kakobuy codes"],
        "fr": ["coupon kakobuy", "kakobuy coupons"],
        "nl": ["kakobuy coupon code", "kakobuy coupons", "how to use coupon on kakobuy"],
        "fi": ["kakobuy kuponki"],
    },
    "kakobuy-shipping": {
        "en": [
            "kakobuy shipping",
            "how much is kakobuy shipping",
            "how long does kakobuy take to deliver",
            "kakobuy shipping calculator",
        ],
        "es": ["envio kakobuy"],
        "fr": ["livraison kakobuy"],
        "nl": [
            "kakobuy shipping calculator",
            "how long is kakobuy shipping",
            "how long does kakobuy take to ship",
        ],
        "fi": ["kakobuy toimitus", "kakobuy shipping"],
    },
    "is-kakobuy-legit": {
        "en": ["is kakobuy legit", "kakobuy legit", "is kakobuy real", "is kakobuy safe"],
        "es": ["is kakobuy legit", "kakobuy es confiable"],
        "fr": ["kakobuy avis", "kakobuy fiable"],
        "nl": ["is kakobuy legit", "is kakobuy betrouwbaar"],
        "fi": ["is kakobuy legit", "onko kakobuy luotettava"],
    },
    "kakobuy-qc": {
        "en": ["qc kakobuy", "kakobuy qc"],
        "es": ["qc kakobuy"],
        "fr": ["kakobuy qc"],
        "nl": ["kakobuy qc"],
        "fi": ["kakobuy qc"],
    },
    "kakobuy-opiniones": {"es": ["kakobuy opiniones"]},
    "avis-kakobuy": {"fr": ["kakobuy avis"]},
    "kakobuy-ervaringen": {"nl": ["kakobuy reviews", "is kakobuy betrouwbaar"]},
    "kakobuy-canada": {"en": ["kakobuy canada"]},
    "kakobuy-kokemuksia": {"fi": ["kakobuy kokemuksia", "onko kakobuy luotettava"]},
}

PLURAL_REDIRECTS = {
    "kakospreadsheets.es": "https://kakospreadsheet.es/kakobuy-spreadsheets/",
    "kakospreadsheets.fr": "https://kakospreadsheet.fr/kakobuy-spreadsheets/",
    "kakospreadsheets.nl": "https://kakospreadsheet.nl/kakobuy-spreadsheets/",
    "kakospreadsheets.ca": "https://kakospreadsheet.ca/kakobuy-spreadsheets/",
}


def slug_to_path(slug: str) -> str:
    if not slug:
        return "/"
    return f"/{slug}/"


def domain_slugs(region: str) -> list[str]:
    slugs = list(COMMON_SLUGS)
    slugs.extend(REGION_EXCLUSIVE_SLUGS.get(region, []))
    slugs.extend(REGION_EXTRA_SLUGS.get(region, []))
    # de-dup preserve order
    seen: set[str] = set()
    out: list[str] = []
    for s in slugs:
        if s not in seen:
            seen.add(s)
            out.append(s)
    return out


def exclusive_slug_regions(slug: str) -> list[str] | None:
    """Return allowed regions for an exclusive slug, or None if common."""
    for region, slugs in REGION_EXCLUSIVE_SLUGS.items():
        if slug in slugs:
            return [region]
    return None
