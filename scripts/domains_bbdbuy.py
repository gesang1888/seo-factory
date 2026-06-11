"""BBDBuy cluster: bbdbuy.uk / bbdbuy.us / bbdbuy.ca / bbdbuy.it"""

from __future__ import annotations

HREFLANG_BBDBUY = {
    "en-GB": "https://bbdbuy.uk",
    "en-US": "https://bbdbuy.us",
    "en-CA": "https://bbdbuy.ca",
    "it-IT": "https://bbdbuy.it",
    "x-default": "https://bbdbuy.us",
}

BBDBUY_DOMAINS = {
    "bbdbuy.uk": {
        "locale": "en-GB",
        "lang": "en",
        "region": "UK",
        "region_label": "United Kingdom",
        "priority": "P0",
    },
    "bbdbuy.us": {
        "locale": "en-US",
        "lang": "en",
        "region": "US",
        "region_label": "United States",
        "priority": "P0",
    },
    "bbdbuy.ca": {
        "locale": "en-CA",
        "lang": "en",
        "region": "CA",
        "region_label": "Canada",
        "priority": "P1",
    },
    "bbdbuy.it": {
        "locale": "it-IT",
        "lang": "it",
        "region": "IT",
        "region_label": "Italy",
        "priority": "P1",
    },
}

COMMON_SLUGS = [
    "",
    "bbdbuy-spreadsheet",
    "bbdbuy-discord",
    "bbdbuy-coupon",
    "bbdbuy-coupons",
    "bbdbuy-review",
    "is-bbdbuy-legit",
    "is-bbdbuy-safe",
    "bbdbuy-link",
    "bbdbuy-app",
    "how-to-use-bbdbuy",
    "bbdbuy-shipping",
    "bbdbuy-qc",
    "bbdbuy-finds",
]

REGION_EXTRA_SLUGS: dict[str, list[str]] = {
    "UK": ["what-is-bbdbuy", "bbdbuy-spreadsheet-reddit", "bbdbuy-telegram"],
    "US": [
        "best-bbdbuy-spreadsheet",
        "bbdbuy-spreadsheet-2026",
        "bbdbuy-tracking",
        "bbdbuy-payment-methods",
        "bbdbuy-link-converter",
    ],
    "CA": ["bbdbuy-canada", "bbdbuy-shipping-to-canada"],
    "IT": ["spreadsheet-bbdbuy", "recensioni-bbdbuy", "bbdbuy-affidabile"],
}


def slug_to_path(slug: str) -> str:
    if not slug:
        return "/"
    return f"/{slug}/"


def domain_slugs(region: str) -> list[str]:
    return COMMON_SLUGS + REGION_EXTRA_SLUGS.get(region, [])
