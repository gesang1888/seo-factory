"""Domain cluster configuration for OrientDig Spreadsheet SEO sites."""

from __future__ import annotations

HREFLANG_CLUSTER = {
    "en-GB": "https://orientdigspreadsheet.uk",
    "en-US": "https://orientdigspreadsheet.us",
    "nl-NL": "https://orientdigspreadsheet.nl",
    "it-IT": "https://orientdigspreadsheet.it",
    "de-DE": "https://orientdigspreadsheet.de",
    "fr-FR": "https://orientdigspreadsheet.fr",
    "x-default": "https://orientdigspreadsheet.us",
}

CANONICAL_DOMAINS = {
    "orientdigspreadsheet.uk": {
        "locale": "en-GB",
        "lang": "en",
        "region": "UK",
        "region_label": "United Kingdom",
        "priority": "P0",
    },
    "orientdigspreadsheet.us": {
        "locale": "en-US",
        "lang": "en",
        "region": "US",
        "region_label": "United States",
        "priority": "P0",
    },
    "orientdigspreadsheet.nl": {
        "locale": "nl-NL",
        "lang": "nl",
        "region": "NL",
        "region_label": "Netherlands",
        "priority": "P0",
    },
    "orientdigspreadsheet.it": {
        "locale": "it-IT",
        "lang": "it",
        "region": "IT",
        "region_label": "Italy",
        "priority": "P1",
    },
    "orientdigspreadsheet.de": {
        "locale": "de-DE",
        "lang": "de",
        "region": "DE",
        "region_label": "Germany",
        "priority": "P1",
    },
    "orientdigspreadsheet.fr": {
        "locale": "fr-FR",
        "lang": "fr",
        "region": "FR",
        "region_label": "France",
        "priority": "P2",
    },
}

PLURAL_REDIRECTS = {
    "orientdigspreadsheets.uk": "https://orientdigspreadsheet.uk/orientdig-spreadsheets/",
    "orientdigspreadsheets.nl": "https://orientdigspreadsheet.nl/orientdig-spreadsheets/",
    "orientdigspreadsheets.de": "https://orientdigspreadsheet.de/orientdig-spreadsheets/",
    "orientdigspreadsheets.fr": "https://orientdigspreadsheet.fr/orientdig-spreadsheets/",
}

COMMON_SLUGS = [
    "",
    "orientdig-spreadsheets",
    "orientdig-finds",
    "orientdig-coupons",
    "is-orientdig-legit",
    "is-orientdig-safe",
    "orientdig-shipping",
    "orientdig-qc",
    "how-to-use-orientdig",
    "orientdig-review",
]

REGION_EXTRA_SLUGS: dict[str, list[str]] = {
    "UK": [
        "what-is-orientdig",
        "how-long-does-orientdig-take-to-ship",
        "orientdig-spreadsheet-reddit",
    ],
    "US": [
        "best-orientdig-spreadsheet",
        "orientdig-spreadsheet-2026",
        "orientdig-shipping-calculator",
        "orientdig-customer-service",
        "orientdig-payment-methods",
        "orientdig-tracking",
    ],
    "NL": [
        "orientdig-coupon-code",
        "orientdig-trustpilot",
        "cnfans-to-orientdig",
    ],
    "DE": [
        "orientdig-erfahrungen",
        "orientdig-trustpilot",
        "orientdig-codes",
        "qc-orientdig",
    ],
    "IT": [
        "spreadsheet-orientdig",
        "orientdig-coupon-codes",
        "orientdig-reddit",
    ],
    "FR": [
        "spreadsheet-orientdig",
        "orientdig-discord",
        "orientdig-coupon",
        "avis-orientdig",
        "orientdig-fiable",
        "livraison-orientdig",
        "guide-orientdig",
    ],
}


def slug_to_path(slug: str) -> str:
    if not slug:
        return "/"
    return f"/{slug}/"


def domain_slugs(region: str) -> list[str]:
    return COMMON_SLUGS + REGION_EXTRA_SLUGS.get(region, [])
