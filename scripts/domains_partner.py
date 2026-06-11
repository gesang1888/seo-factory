"""Partner cluster: orientdig.us / orientdig.es / orientdig.fr / orientdig.at"""

from __future__ import annotations

HREFLANG_PARTNER = {
    "en-US": "https://orientdig.us",
    "es-ES": "https://orientdig.es",
    "fr-FR": "https://orientdig.fr",
    "de-AT": "https://orientdig.at",
    "x-default": "https://orientdig.us",
}

PARTNER_DOMAINS = {
    "orientdig.us": {
        "locale": "en-US",
        "lang": "en",
        "region": "US",
        "region_label": "United States",
        "priority": "P0",
    },
    "orientdig.es": {
        "locale": "es-ES",
        "lang": "es",
        "region": "ES",
        "region_label": "Spain",
        "priority": "P1",
    },
    "orientdig.fr": {
        "locale": "fr-FR",
        "lang": "fr",
        "region": "FR",
        "region_label": "France",
        "priority": "P1",
    },
    "orientdig.at": {
        "locale": "de-AT",
        "lang": "de",
        "region": "AT",
        "region_label": "Austria",
        "priority": "P2",
    },
}

COMMON_SLUGS = [
    "",
    "orientdig-spreadsheet",
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
    "US": [
        "best-orientdig-spreadsheet",
        "orientdig-shipping-calculator",
        "orientdig-payment-methods",
        "orientdig-tracking",
    ],
    "ES": [
        "como-comprar-en-orientdig",
        "orientdig-discord",
        "orientdig-shipping-coupons",
    ],
    "FR": [
        "spreadsheet-orientdig",
        "orientdig-discord",
        "orientdig-coupon",
        "avis-orientdig",
    ],
    "AT": [
        "orientdig-erfahrungen",
        "orientdig-trustpilot",
        "orientdig-codes",
        "qc-orientdig",
    ],
}


def slug_to_path(slug: str) -> str:
    if not slug:
        return "/"
    return f"/{slug}/"


def domain_slugs(region: str) -> list[str]:
    return COMMON_SLUGS + REGION_EXTRA_SLUGS.get(region, [])
