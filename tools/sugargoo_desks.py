#!/usr/bin/env python3
"""Restore SugarGoo country-desk homepages in original CMS chrome.

Puts catalogue on /, Inter + existing sugargoo-theme.css (not Georgia, not HipoBuy green).
Does not overwrite coupons / GST / CBSA / de-minimis / now.com html articles.
Does not 301 country TLDs together or onto sugargoo.ca / sugargoo.es.
Invite/coupon codes stay off titles.
No declared-value coaching.
"""
from __future__ import annotations

import json
import os
import re
import sys
import time
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "sites"
EST = "https://www.sugargoo.com/freight-estimate"
OFFICIAL = "https://www.sugargoo.com/"
REG = "https://www.sugargoo.com/register?inviteCode=O4K87NHKR"
INVITE = "O4K87NHKR"
COUPON = "2026SG50"
W2C = "https://w2clinks.com/spreadsheet/sugargoo/"
DATE = "30 Sep 2026"

HOSTS = {
    "us": {
        "host": "sugargoospreadsheets.us",
        "lang": "en-US",
        "theme": "sugargoo-theme-us",
        "locale": "USA",
        "dest": "US",
        "dest_label": "the United States",
        "badge": "United States · USD · USPS",
        "mail": "support@sugargoospreadsheets.us",
        "utm": "sugargoospreadsheets_us",
        "keep": [
            ("/sugargoo-coupons/", "Coupons (¥800 / 2026SG50 in the article)"),
            ("/de-minimis-us-sugargoo/", "CBP / de minimis — educational"),
            ("/cbp-declared-value-us/", "CBP declared value — educational"),
            ("/sugargoo-shipping-times-us/", "USPS times"),
            ("/sugargoo-spreadsheet/", "Spreadsheet guide"),
            ("/sugargoo-review/", "Review"),
        ],
    },
    "au": {
        "host": "sugargoospreadsheet.au",
        "lang": "en-AU",
        "theme": "sugargoo-theme-global",
        "locale": "Australia",
        "dest": "AU",
        "dest_label": "Australia",
        "badge": "Australia · AUD · GST",
        "mail": "support@sugargoospreadsheet.au",
        "utm": "sugargoospreadsheet_au",
        "keep": [
            ("/gst-import-australia/", "GST / ABF — educational"),
            ("/sugargoo-spreadsheet/", "Spreadsheet guide"),
            ("/sugargoo-coupons/", "Coupons"),
            ("/sugargoo-review/", "Review"),
        ],
    },
    "fr": {
        "host": "sugargoospreadsheets.fr",
        "lang": "fr-FR",
        "theme": "sugargoo-theme-fr",
        "locale": "France",
        "dest": "FR",
        "dest_label": "la France",
        "badge": "France · EUR · douane FR",
        "mail": "support@sugargoospreadsheets.fr",
        "utm": "sugargoospreadsheets_fr",
        "keep": [
            ("/sugargoo-coupons/", "Coupons"),
            ("/sugargoo-review/", "Avis"),
            ("/sugargoo-spreadsheet/", "Guide spreadsheet"),
        ],
    },
    "ca": {
        "host": "sugargoospreadsheets2026.ca",
        "lang": "en-CA",
        "theme": "sugargoo-theme-ca",
        "locale": "Canada",
        "dest": "CA",
        "dest_label": "Canada",
        "badge": "Canada · CAD · CBSA",
        "mail": "support@sugargoospreadsheets2026.ca",
        "utm": "sugargoospreadsheets2026_ca",
        "keep": [
            ("/cbsa-import-canada/", "CBSA import guide (ranked URL)"),
            ("/sugargoo-shipping-canada/", "Shipping to Canada"),
            ("/sugargoo-spreadsheet/", "Spreadsheet guide"),
            ("/sugargoo-coupons/", "Coupons"),
        ],
    },
    "now": {
        "host": "sugargoospreadsheetnow.com",
        "lang": "en",
        "theme": "sugargoo-theme-global",
        "locale": "Global",
        "dest": None,
        "dest_label": "a country in the estimator",
        "badge": "Coupon / spreadsheet hub · pick a country in-app",
        "mail": "support@sugargoospreadsheetnow.com",
        "utm": "sugargoospreadsheetnow",
        "keep": [
            ("/sugargoo-coupon-2026.html", "Coupons 2026 html"),
            ("/sugargoo-reddit-2026.html", "Reddit html"),
            ("/best-sugargoo-spreadsheet-2026.html", "Spreadsheet html"),
            ("/is-sugargoo-legit-2026.html", "Legit html"),
            ("/how-does-sugargoo-work-2026.html", "How it works html"),
        ],
    },
    "uk": {
        "host": "sugargoospreadsheets.uk",
        "lang": "en-GB",
        "theme": "sugargoo-theme-uk",
        "locale": "UK",
        "dest": "GB",
        "dest_label": "the United Kingdom",
        "badge": "United Kingdom · GBP · HMRC",
        "mail": "support@sugargoospreadsheets.uk",
        "utm": "sugargoospreadsheets_uk",
        "keep": [
            ("/vat-on-imports-uk-2026/", "UK import VAT"),
            ("/sugargoo-spreadsheet/", "Spreadsheet guide"),
            ("/sugargoo-coupons/", "Coupons"),
        ],
    },
    "es": {
        "host": "sugargoospreadsheet.es",
        "lang": "es-ES",
        "theme": "sugargoo-theme-es",
        "locale": "España",
        "dest": "ES",
        "dest_label": "España",
        "badge": "España · EUR · aduana",
        "mail": "support@sugargoospreadsheet.es",
        "utm": "sugargoospreadsheet_es",
        "keep": [
            ("/aduana-iva-espana/", "Aduana / IVA"),
            ("/guias-comprador-es/", "Guías"),
            ("/sugargoo-coupons/", "Cupones"),
            ("/sugargoo-spreadsheet/", "Spreadsheet"),
        ],
    },
    "de": {
        "host": "sugargoospreadsheets.de",
        "lang": "de-DE",
        "theme": "sugargoo-theme-de",
        "locale": "Deutschland",
        "dest": "DE",
        "dest_label": "Deutschland",
        "badge": "Deutschland · EUR · Zoll",
        "mail": "support@sugargoospreadsheets.de",
        "utm": "sugargoospreadsheets_de",
        "keep": [
            ("/sugargoo-coupons/", "Coupons"),
            ("/sugargoo-spreadsheet/", "Spreadsheet"),
            ("/sugargoo-review/", "Review"),
        ],
    },
    "at": {
        "host": "sugargoo.at",
        "lang": "de-AT",
        "theme": "sugargoo-theme-at",
        "locale": "Österreich",
        "dest": "AT",
        "dest_label": "Österreich",
        "badge": "Österreich · EUR · BMF Zoll",
        "mail": "support@sugargoo.at",
        "utm": "sugargoo_at",
        "keep": [
            ("/sugargoo-coupons/", "Coupons"),
            ("/sugargoo-spreadsheet/", "Spreadsheet"),
            ("/kaeuferguides-at/", "Käuferguides"),
        ],
    },
    "nl": {
        "host": "sugargoospreadsheets.nl",
        "lang": "nl-NL",
        "theme": "sugargoo-theme-nl",
        "locale": "Nederland",
        "dest": "NL",
        "dest_label": "Nederland",
        "badge": "Nederland · EUR · douane",
        "mail": "support@sugargoospreadsheets.nl",
        "utm": "sugargoospreadsheets_nl",
        "keep": [
            ("/btw-import-nederland/", "BTW / douane"),
            ("/sugargoo-coupons/", "Coupons"),
            ("/sugargoo-spreadsheet/", "Spreadsheet"),
        ],
    },
}

HOME_META = {
    "us": {
        "title": "Buy from China to the United States with SugarGoo",
        "desc": "Independent US desk: catalogue on this homepage, USPS/CBP sources, official freight estimate. Lab 30 Sep 2026. No under-declaration tips.",
        "h1": "Using SugarGoo to ship from China to the <em>US</em>",
        "hsub": "Purchasing agent to a US street: warehouse photos, then an international SKU. Catalogue, FAQ and the freight lab sit on this homepage. Coupons stay on the coupon article.",
    },
    "au": {
        "title": "Buy from China to Australia with SugarGoo",
        "desc": "Independent AU desk: catalogue on this homepage, GST/ABF article kept, official freight estimate. Lab 30 Sep 2026.",
        "h1": "Using SugarGoo to ship from China to <em>Australia</em>",
        "hsub": "GST notes stay on the GST article. This homepage is the catalogue and the AU estimator reminder.",
    },
    "fr": {
        "title": "Acheter en Chine et envoyer en France avec SugarGoo",
        "desc": "Desk FR indépendant : catalogue sur cette accueil, coupons et avis déjà classés. Destination France dans l’estimateur. Pas la Belgique.",
        "h1": "Envoyer de Chine en <em>France</em> avec SugarGoo",
        "hsub": "Les clics Google sont sur les coupons et l’avis — on les garde. Cette accueil est le catalogue. La destination dans l’estimateur est la France, pas la Belgique.",
    },
    "ca": {
        "title": "Buy from China to Canada with SugarGoo",
        "desc": "Independent CA desk on this host. Ranked CBSA article stays. Catalogue on the homepage. Lab 30 Sep 2026.",
        "h1": "Using SugarGoo to ship from China to <em>Canada</em>",
        "hsub": "The ranked URL is still /cbsa-import-canada/. This homepage is the CA destination desk, not a 2026 gimmick and not sugargoo.ca.",
    },
    "now": {
        "title": "SugarGoo coupon desk — pick a country in the estimator",
        "desc": "Independent English hub. Destination is a country code in the official estimator, not this hostname. Existing html articles stay.",
        "h1": "SugarGoo coupons and spreadsheet hub",
        "hsub": "This host is not a destination. Open the official estimator with US, CA, FR… The dated html files already on this host stay put.",
    },
    "uk": {
        "title": "Buy from China to the UK with SugarGoo",
        "desc": "Independent UK haul log: catalogue on this homepage, HMRC VAT article kept. Lab 30 Sep 2026.",
        "h1": "Using SugarGoo to ship a <em>UK haul</em> from China",
        "hsub": "GBP haul log. Destination in the estimator is a GB address. Northern Ireland is often another SKU.",
    },
    "es": {
        "title": "Comprar en China y enviar a España con SugarGoo",
        "desc": "Desk ES independiente. Catálogo en esta portada. Aduana/IVA se queda en su URL. No es sugargoo.es.",
        "h1": "Enviar de China a <em>España</em> con SugarGoo",
        "hsub": "El artículo de aduana sigue en /aduana-iva-espana/. Esta portada es el catálogo. No copiamos sugargoo.es.",
    },
    "de": {
        "title": "Mit SugarGoo nach Deutschland bestellen — aus China auf eine DE-Adresse",
        "desc": "Unabhängiger DE-Desk: Katalog auf dieser Startseite, Zollquellen. Lab 30 Sep 2026.",
        "h1": "Mit <em>SugarGoo</em> nach Deutschland bestellen",
        "hsub": "Aus China auf eine deutsche Straße. Katalog und FAQ auf dieser Startseite. Coupons bleiben im Coupon-Artikel.",
    },
    "at": {
        "title": "Mit SugarGoo nach Österreich bestellen — aus China auf eine AT-Adresse",
        "desc": "Unabhängiger AT-Desk: Katalog auf dieser Startseite. Lab 30 Sep 2026. Keine Unterdeklaration.",
        "h1": "Mit <em>SugarGoo</em> nach Österreich bestellen",
        "hsub": "Aus China auf eine österreichische Straße. Katalog, FAQ und Schätzer-Hinweis auf dieser Startseite.",
    },
    "nl": {
        "title": "Met SugarGoo naar Nederland verzenden — kopen in China op een NL-adres",
        "desc": "Onafhankelijke NL-desk: catalogus op deze homepage. Lab 30 sep 2026. Geen onderwaardering.",
        "h1": "Met <em>SugarGoo</em> naar Nederland verzenden",
        "hsub": "Uit China naar een Nederlands huisadres. Catalogus en FAQ op deze homepage.",
    },
}

CATS = [
    ("all", "All", ""),
    ("sneakers", "Sneakers", "sneakers"),
    ("hoodie", "Hoodies", "hoodie"),
    ("t-shirt", "T-shirts", "t-shirt"),
    ("jacket", "Jackets", "jacket"),
    ("bag", "Bags", "bag"),
    ("watch", "Watches", "watch"),
]

EXTRA_CSS = """
.sg-hero{max-width:1100px;margin:0 auto;padding:28px 24px 8px;text-align:left}
.sg-hero h1{font-size:clamp(28px,4.4vw,42px);font-weight:800;letter-spacing:-1.1px;line-height:1.15;margin:0 0 12px}
.sg-hero h1 em{font-style:normal;color:var(--primary,#ff7103)}
.sg-hero .hsub{color:#475569;font-size:16px;line-height:1.6;max-width:720px}
.sg-hero .hbg{display:inline-block;font-size:12px;font-weight:700;background:var(--primary-soft,#fff5eb);color:var(--primary,#ff7103);padding:4px 10px;border-radius:999px;margin-bottom:12px}
.sg-ctas{display:flex;gap:10px;flex-wrap:wrap;margin:18px 0 8px}
.sg-mw{max-width:1200px;margin:0 auto;padding:8px 24px 48px}
.sg-fbar{display:flex;gap:8px;align-items:center;margin:12px 0 16px;flex-wrap:wrap}
.sg-fbar input,.sg-fbar select{height:38px;border:1.5px solid #e5e7eb;border-radius:9px;padding:0 12px;font:inherit}
.sg-fbar input{flex:1;min-width:180px}
.sg-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(180px,1fr));gap:13px}
.sg-card{border:1px solid #e5e7eb;border-radius:12px;overflow:hidden;background:#fff;display:flex;flex-direction:column}
.sg-card img{width:100%;aspect-ratio:1;object-fit:cover;background:#f8fafc}
.sg-card .b{padding:10px;display:flex;flex-direction:column;gap:6px;flex:1}
.sg-card .t{font-size:13px;font-weight:600;line-height:1.4;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden}
.sg-card .pr{font-weight:800;color:var(--primary,#ff7103)}
.sg-card a.buy{margin:0 10px 10px;text-align:center;padding:8px;border-radius:8px;background:var(--primary,#ff7103);color:#fff;font-size:12.5px;font-weight:600;text-decoration:none}
.sg-chips{display:flex;gap:8px;flex-wrap:wrap;margin:8px 0 4px}
.sg-chips button{border:1px solid #e5e7eb;background:#fff;border-radius:999px;padding:6px 12px;font:inherit;cursor:pointer}
.sg-chips button.on{background:var(--primary-soft,#fff5eb);border-color:var(--primary,#ff7103);color:var(--primary,#ff7103);font-weight:600}
.sg-sec{max-width:1100px;margin:0 auto;padding:12px 24px 28px}
.sg-sec h2{font-size:22px;margin:0 0 8px}
.sg-sec .ssub{color:#64748b;margin:0 0 14px}
.tw{overflow-x:auto;border:1px solid #e5e7eb;border-radius:12px}
.tw table{width:100%;border-collapse:collapse;font-size:14px}
.tw th,.tw td{padding:10px 12px;border-bottom:1px solid #e5e7eb;text-align:left;vertical-align:top}
.tw th{background:#f8fafc;font-size:11px;letter-spacing:.4px;text-transform:uppercase;color:#64748b}
details.sg-faq{border:1px solid #e5e7eb;border-radius:10px;padding:10px 14px;margin:0 0 8px;background:#fff}
details.sg-faq summary{cursor:pointer;font-weight:600}
.keep{display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:10px}
.keep a{display:block;border:1px solid #e5e7eb;border-radius:10px;padding:12px;text-decoration:none;color:inherit;background:#fff}
.keep a:hover{border-color:var(--primary,#ff7103)}
.vol{border:1px solid #e5e7eb;border-radius:16px;padding:16px 18px;margin:16px 0;background:#fff}
.vol input,.vol select{width:100%;height:36px;border:1.5px solid #e5e7eb;border-radius:8px;padding:0 8px}
figure.shot{margin:16px 0}
figure.shot img{width:100%;max-width:920px;height:auto;border:1px solid #e5e7eb;border-radius:12px;background:#f8fafc}
figure.shot figcaption{font-size:13px;color:#64748b;margin-top:6px}
"""


HREFLANG = [
    ("en", "sugargoospreadsheetnow.com"),
    ("en-US", "sugargoospreadsheets.us"),
    ("en-AU", "sugargoospreadsheet.au"),
    ("en-CA", "sugargoospreadsheets2026.ca"),
    ("en-GB", "sugargoospreadsheets.uk"),
    ("fr-FR", "sugargoospreadsheets.fr"),
    ("es", "sugargoospreadsheet.es"),
    ("de-DE", "sugargoospreadsheets.de"),
    ("de-AT", "sugargoo.at"),
    ("nl-NL", "sugargoospreadsheets.nl"),
]


def _hreflang() -> str:
    bits = [
        f'<link rel="alternate" hreflang="{escape(code)}" href="https://{escape(host)}/">'
        for code, host in HREFLANG
    ]
    bits.append('<link rel="alternate" hreflang="x-default" href="https://sugargoospreadsheetnow.com/">')
    return "\n".join(bits)


def _locale_switcher(key: str, d: dict) -> str:
    rows = [
        ("English", [
            ("now", "sugargoospreadsheetnow.com", "English (Global)"),
            ("us", "sugargoospreadsheets.us", "English (USA)"),
            ("uk", "sugargoospreadsheets.uk", "English (UK)"),
            ("ca", "sugargoospreadsheets2026.ca", "English (Canada)"),
            ("au", "sugargoospreadsheet.au", "English (Australia)"),
        ]),
        ("Local editions", [
            ("fr", "sugargoospreadsheets.fr", "Français (France)"),
            ("es", "sugargoospreadsheet.es", "Español (España)"),
            ("nl", "sugargoospreadsheets.nl", "Nederlands"),
            ("de", "sugargoospreadsheets.de", "Deutsch (Deutschland)"),
            ("at", "sugargoo.at", "Deutsch (Österreich)"),
        ]),
    ]
    parts = ['<div class="locale-switcher" data-locale-switcher>']
    parts.append(
        '<button type="button" class="locale-switcher-btn" data-locale-toggle '
        'aria-haspopup="listbox" aria-expanded="false" aria-label="Choose language or region">'
        '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true">'
        '<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3a15 15 0 0 1 0 18M12 3a15 15 0 0 0 0 18"/></svg>'
        f'<span>{escape(d["locale"])}</span>'
        '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true">'
        '<path d="M6 9l6 6 6-6"/></svg></button>'
    )
    parts.append('<div class="locale-switcher-panel" role="listbox" hidden>')
    for heading, items in rows:
        parts.append(f'<div class="locale-switcher-heading">{escape(heading)}</div>')
        for k, host, lab in items:
            cur = ' class="is-current"' if k == key else ""
            parts.append(
                f'<a href="https://{escape(host)}/" hreflang="alternate" rel="alternate"{cur}>{escape(lab)}</a>'
            )
    parts.append(
        f'<div class="locale-switcher-register"><a href="{REG}" target="_blank" rel="noopener sponsored">'
        "Register on Sugargoo →</a></div>"
    )
    parts.append("</div></div>")
    return "".join(parts)


def _nav(key: str, d: dict) -> str:
    if key == "fr":
        items = [
            ("/", "Accueil", True),
            ("/sugargoo-finds/", "Trouvailles", False),
            ("/sugargoo-spreadsheet/", "Spreadsheet", False),
            ("/sugargoo-review/", "Avis", False),
            ("/sugargoo-coupons/", "Coupons", False),
            ("/#faq", "FAQ", False),
        ]
        cta, browse = "Voir le catalogue", "Spreadsheet complète"
    elif key == "es":
        items = [
            ("/", "Inicio", True),
            ("/sugargoo-finds/", "Finds", False),
            ("/sugargoo-spreadsheet/", "Spreadsheet", False),
            ("/sugargoo-review/", "Opinión", False),
            ("/sugargoo-coupons/", "Cupones", False),
            ("/#faq", "FAQ", False),
        ]
        cta, browse = "Ver catálogo", "Spreadsheet completa"
    elif key in ("de", "at"):
        items = [
            ("/", "Start", True),
            ("/sugargoo-finds/", "Finds", False),
            ("/sugargoo-spreadsheet/", "Spreadsheet", False),
            ("/sugargoo-review/", "Review", False),
            ("/sugargoo-coupons/", "Coupons", False),
            ("/#faq", "FAQ", False),
        ]
        cta, browse = "Katalog", "Ganzes Spreadsheet"
    elif key == "nl":
        items = [
            ("/", "Home", True),
            ("/sugargoo-finds/", "Finds", False),
            ("/sugargoo-spreadsheet/", "Spreadsheet", False),
            ("/sugargoo-review/", "Review", False),
            ("/sugargoo-coupons/", "Coupons", False),
            ("/#faq", "FAQ", False),
        ]
        cta, browse = "Catalogus", "Volledige spreadsheet"
    elif key == "now":
        items = [
            ("/", "Home", True),
            ("/sugargoo-coupon-2026.html", "Coupons", False),
            ("/best-sugargoo-spreadsheet-2026.html", "Spreadsheet", False),
            ("/is-sugargoo-legit-2026.html", "Legit", False),
            ("/sugargoo-reddit-2026.html", "Reddit", False),
            ("/#faq", "FAQ", False),
        ]
        cta, browse = "Browse catalogue", "Full spreadsheet"
    else:
        items = [
            ("/", "Home", True),
            ("/sugargoo-finds/", "Finds", False),
            ("/sugargoo-spreadsheet/", "Spreadsheet", False),
            ("/sugargoo-review/", "Review", False),
            ("/sugargoo-coupons/", "Coupons", False),
            ("/#faq", "FAQ", False),
        ]
        cta, browse = "Browse catalogue", "Full spreadsheet"
    nav = "".join(
        f'<a href="{escape(href)}"' + (' class="active"' if on else "") + f">{escape(lab)}</a>"
        for href, lab, on in items
    )
    w2c = f"{W2C}?utm_source={d['utm']}&utm_medium=desk&utm_campaign=sugargoo"
    return nav, cta, browse, w2c


def _chrome_head(key: str, d: dict, title: str, desc: str) -> str:
    host = d["host"]
    canonical = f"https://{host}/"
    return f"""<!DOCTYPE html>
<html lang="{escape(d['lang'])}">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{escape(title)}</title>
<meta name="description" content="{escape(desc)}">
<link rel="canonical" href="{canonical}">
<meta name="robots" content="index, follow, max-image-preview:large">
<meta property="og:type" content="website">
<meta property="og:title" content="{escape(title)}">
<meta property="og:description" content="{escape(desc)}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="https://{host}/assets/images/sugargoo-logo.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/css/country-flags.css?v=20260531-flags">
<link rel="stylesheet" href="/assets/css/sugargoo-theme.css?v=20260531-sugargoo">
<link rel="stylesheet" href="/assets/css/sugargoo-regional-themes.css?v=20260601-regional">
<link rel="stylesheet" href="/assets/css/style.css?v=20260930-home">
<link rel="icon" href="/assets/images/sugargoo-favicon.ico" type="image/x-icon">
{_hreflang()}
<style>{EXTRA_CSS}</style>
<script type="application/ld+json">{json.dumps({"@context":"https://schema.org","@type":"WebPage","name":title,"url":canonical,"description":desc,"inLanguage":d["lang"]}, ensure_ascii=False)}</script>
</head>
<body class="{escape(d['theme'])}">
"""


def _header(key: str, d: dict) -> str:
    nav, cta, browse, w2c = _nav(key, d)
    top = {
        "fr": f"Conçu pour la France · estimateur officiel · <a href=\"{w2c}\" target=\"_blank\" rel=\"noopener\">{browse} →</a>",
        "es": f"Escritorio ES independiente · no es sugargoo.es · <a href=\"{w2c}\" target=\"_blank\" rel=\"noopener\">{browse} →</a>",
        "de": f"Für eine DE-Adresse · kein Kakobuy · <a href=\"{w2c}\" target=\"_blank\" rel=\"noopener\">{browse} →</a>",
        "at": f"Für eine AT-Adresse · BMF Zoll · <a href=\"{w2c}\" target=\"_blank\" rel=\"noopener\">{browse} →</a>",
        "nl": f"Voor een NL-adres · <a href=\"{w2c}\" target=\"_blank\" rel=\"noopener\">{browse} →</a>",
        "now": f"Coupon hub · destination is a country in the estimator · <a href=\"{w2c}\" target=\"_blank\" rel=\"noopener\">{browse} →</a>",
    }.get(key, f"Independent desk · {escape(d['badge'])} · <a href=\"{w2c}\" target=\"_blank\" rel=\"noopener\">{browse} →</a>")
    return f"""<div class="topbar"><div class="container">{top}</div></div>
<header class="site-header">
  <div class="container header-inner">
    <a href="/" class="brand sugargoo-brand"><img class="brand-logo sugargoo-logo" src="/assets/images/sugargoo-logo.png" alt="Sugargoo" width="160" height="36"></a>
    <nav class="nav" id="site-nav">{nav}</nav>
    <div class="header-actions">
      <a href="#catalog" class="btn btn-primary">{escape(cta)}</a>
      <a href="{REG}" target="_blank" rel="noopener sponsored" class="btn btn-outline">{escape({"fr":"S’inscrire","es":"Registrarse","de":"Registrieren","at":"Registrieren","nl":"Registreren"}.get(key,"Register"))}</a>
      {_locale_switcher(key, d)}
      <button class="mobile-toggle" data-mobile-toggle aria-label="Menu"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="3" y1="6" x2="21" y2="6"/><line x1="3" y1="12" x2="21" y2="12"/><line x1="3" y1="18" x2="21" y2="18"/></svg></button>
    </div>
  </div>
</header>
"""


def _footer(key: str, d: dict) -> str:
    return f"""<footer class="site-footer">
  <div class="container">
    <div class="footer-grid">
      <div class="footer-brand"><a href="/" class="brand sugargoo-brand"><img class="brand-logo sugargoo-logo" src="/assets/images/sugargoo-logo.png" alt="Sugargoo"></a>
      <p>Independent information desk on {escape(d['host'])}. Not the official SugarGoo site. Sister country hosts stay separate files — no 301.</p></div>
      <div class="footer-col"><h5>On this host</h5><ul>
        {''.join(f'<li><a href="{escape(h)}">{escape(l)}</a></li>' for h,l in d['keep'])}
      </ul></div>
      <div class="footer-col"><h5>Official</h5><ul>
        <li><a href="{EST}">Freight estimate</a></li>
        <li><a href="{REG}" rel="noopener sponsored">Register</a></li>
        <li><a href="{OFFICIAL}">sugargoo.com</a></li>
      </ul></div>
      <div class="footer-col"><h5>Contact</h5><ul>
        <li><a href="mailto:{escape(d['mail'])}">{escape(d['mail'])}</a></li>
        <li><a href="/privacy-policy/">Privacy</a></li>
        <li><a href="/cookie-policy/">Cookies</a></li>
      </ul></div>
    </div>
    <p class="footer-locale-cluster" style="margin:12px 0;font-size:13px;color:#94A3B8">Independent desks:
      <a href="https://sugargoospreadsheetnow.com/">Global</a> ·
      <a href="https://sugargoospreadsheets.us/">USA</a> ·
      <a href="https://sugargoospreadsheet.au/">Australia</a> ·
      <a href="https://sugargoospreadsheets.fr/">France</a> ·
      <a href="https://sugargoospreadsheets2026.ca/">Canada</a> ·
      <a href="https://sugargoospreadsheets.uk/">UK</a> ·
      <a href="https://sugargoospreadsheet.es/">España</a> ·
      <a href="https://sugargoospreadsheets.de/">Deutschland</a> ·
      <a href="https://sugargoo.at/">Österreich</a> ·
      <a href="https://sugargoospreadsheets.nl/">Nederland</a>
    </p>
    <div class="footer-bottom"><div>© 2026 {escape(d['host'])} · independent desk</div></div>
  </div>
</footer>
<script src="/assets/js/main.js?v=20260930-home"></script>
</body></html>
"""


def _catalog(key: str) -> str:
    chips = "".join(
        f'<button type="button" data-q="{escape(q)}" class="{"on" if slug=="all" else ""}">{escape(lab)}</button>'
        for slug, lab, q in CATS
    )
    ph = {
        "fr": ("Rechercher sneakers, hoodie…", "Le catalogue anglais est sur cette accueil via /api/products/."),
        "es": ("Buscar sneakers, hoodie…", "El catálogo en inglés está en esta portada via /api/products/."),
        "de": ("Sneakers, Hoodie suchen…", "Der englische Katalog liegt auf dieser Startseite über /api/products/."),
        "at": ("Sneakers, Hoodie suchen…", "Der englische Katalog liegt auf dieser Startseite über /api/products/."),
        "nl": ("Zoek sneakers, hoodie…", "De Engelse catalogus staat op deze homepage via /api/products/."),
    }.get(key, ("Search sneakers, hoodie…", "The English catalogue renders on this homepage from /api/products/."))
    return f"""
<section class="sg-mw" id="catalog">
  <p class="ssub">{escape(ph[1])} Local words often return zero — type the English key.</p>
  <div class="sg-chips">{chips}</div>
  <div class="sg-fbar">
    <input id="sg-q" type="search" placeholder="{escape(ph[0])}">
    <span id="sg-count"></span>
  </div>
  <div class="sg-grid" id="sg-grid"></div>
</section>
<script>
(function(){{
  var PAPI='/api/products/';
  var q='';
  function render(data){{
    var items=data.items||data.products||[];
    var g=document.getElementById('sg-grid');
    var c=document.getElementById('sg-count');
    if(c) c.textContent=items.length+' on this page';
    g.innerHTML='';
    items.forEach(function(it){{
      var el=document.createElement('article');
      el.className='sg-card';
      var img=document.createElement('img');
      img.src=it.image||''; img.alt=it.title||''; img.loading='lazy';
      var b=document.createElement('div'); b.className='b';
      var t=document.createElement('div'); t.className='t'; t.textContent=it.title||'';
      var p=document.createElement('div'); p.className='pr'; p.textContent=(it.currency||'')+' '+(it.price||'');
      b.appendChild(t); b.appendChild(p);
      var a=document.createElement('a'); a.className='buy'; a.target='_blank'; a.rel='noopener sponsored';
      a.href=it.href||it.target||'{REG}'; a.textContent='Open';
      el.appendChild(img); el.appendChild(b); el.appendChild(a);
      g.appendChild(el);
    }});
    if(!items.length) g.innerHTML='<p>No cards for that English key. Try sneakers or hoodie.</p>';
  }}
  function load(){{
    var u=new URL(PAPI, location.origin);
    if(q) u.searchParams.set('q', q);
    u.searchParams.set('limit','24');
    u.searchParams.set('page','1');
    fetch(u, {{headers:{{'Accept':'application/json'}}}}).then(function(r){{return r.json();}}).then(render).catch(function(){{
      document.getElementById('sg-grid').innerHTML='<p>Catalogue API not reachable on this host yet.</p>';
    }});
  }}
  document.querySelectorAll('.sg-chips button').forEach(function(b){{
    b.addEventListener('click', function(){{
      document.querySelectorAll('.sg-chips button').forEach(function(x){{x.classList.remove('on');}});
      b.classList.add('on');
      q=b.getAttribute('data-q')||'';
      document.getElementById('sg-q').value=q;
      load();
    }});
  }});
  var inp=document.getElementById('sg-q');
  var t=null;
  inp.addEventListener('input', function(){{
    clearTimeout(t); t=setTimeout(function(){{ q=inp.value.trim(); load(); }}, 250);
  }});
  load();
}})();
</script>
"""


def _nine(key: str) -> str:
    rows_en = [
        ("Submitted", "You paid the goods plus China domestic."),
        ("Purchasing", "SugarGoo buys in the third-party shop."),
        ("Purchased", "The agent completed the China-side order."),
        ("Seller shipped", "The Chinese seller dispatched."),
        ("To warehouse", "In transit to the SugarGoo warehouse."),
        ("QC / photos", "Warehouse inspection photos."),
        ("Packing center", "Stored. Official blog: 100 free days on purchasing orders, counted from this status."),
        ("Parcel shipped", "International SKU left China."),
        ("Delivered", "Last-mile delivered; confirm in-app."),
    ]
    if key in ("de", "at"):
        h, n = "Neun Zustände (Packing Center)", "Offizielle Lagerfrist für Kaufaufträge: 100 Tage ab Packing Center — nicht 90. Labels der App bleiben oft englisch."
        rows = [
            ("Submitted", "Ware plus Inlandversand in China bezahlt."),
            ("Purchasing", "SugarGoo kauft im Drittshop."),
            ("Purchased", "China-Bestellung abgeschlossen."),
            ("Seller shipped", "Der Shop hat abgeschickt."),
            ("To warehouse", "Unterwegs ins Lager."),
            ("QC / photos", "Lagerfotos."),
            ("Packing center", "Eingelagert. Offiziell 100 Tage gratis ab diesem Status."),
            ("Parcel shipped", "Internationale Linie gestartet."),
            ("Delivered", "Zugestellt."),
        ]
    elif key == "nl":
        h, n = "Negen statussen (Packing Center)", "Officieel: 100 dagen gratis opslag voor kooporders vanaf Packing Center."
        rows = [
            ("Submitted", "Product plus binnenlands China betaald."),
            ("Purchasing", "SugarGoo koopt in de Chinese shop."),
            ("Purchased", "China-order geplaatst."),
            ("Seller shipped", "Verkoper heeft verzonden."),
            ("To warehouse", "Onderweg naar het magazijn."),
            ("QC / photos", "Magazijnfoto’s."),
            ("Packing center", "Opgeslagen. 100 dagen gratis vanaf deze status."),
            ("Parcel shipped", "Internationale lijn vertrokken."),
            ("Delivered", "Bezorgd."),
        ]
    elif key == "fr":
        h, n = "Neuf états (Packing Center)", "Blog officiel : 100 jours gratuits pour les ordres d’achat, à partir du statut Packing Center."
        rows = [
            ("Submitted", "Marchandise + domestique Chine payés."),
            ("Purchasing", "SugarGoo achète chez le vendeur."),
            ("Purchased", "Commande Chine passée."),
            ("Seller shipped", "Le vendeur a expédié."),
            ("To warehouse", "Vers l’entrepôt."),
            ("QC / photos", "Photos d’entrepôt."),
            ("Packing center", "Stocké. 100 jours gratuits à partir de ce statut."),
            ("Parcel shipped", "Ligne internationale partie."),
            ("Delivered", "Livré."),
        ]
    elif key == "es":
        h, n = "Nueve estados (Packing Center)", "Blog oficial: 100 días gratis en pedidos de compra desde Packing Center."
        rows = [
            ("Submitted", "Producto + envío doméstico en China pagados."),
            ("Purchasing", "SugarGoo compra en la tienda."),
            ("Purchased", "Pedido en China hecho."),
            ("Seller shipped", "El vendedor envió."),
            ("To warehouse", "Hacia el almacén."),
            ("QC / photos", "Fotos de almacén."),
            ("Packing center", "Almacenado. 100 días gratis desde este estado."),
            ("Parcel shipped", "Línea internacional salió."),
            ("Delivered", "Entregado."),
        ]
    else:
        h, n = "Nine states, packing center", "Official blog: 100 free days on purchasing orders from Packing Center — not a 90-day HipoBuy figure. App labels stay English."
        rows = rows_en
    body = "".join(f"<tr><td><code>{escape(a)}</code></td><td>{escape(b)}</td></tr>" for a, b in rows)
    return f"""<section class="sg-sec" id="states"><h2>{escape(h)}</h2><p class="ssub">{escape(n)}</p>
<div class="tw"><table><thead><tr><th>State</th><th></th></tr></thead><tbody>{body}</tbody></table></div></section>"""


def _vol(key: str) -> str:
    title = {
        "fr": "Poids volumétrique (pas un prix)",
        "es": "Peso volumétrico (no es un precio)",
        "de": "Volumengewicht (kein Preis)",
        "at": "Volumengewicht (kein Preis)",
        "nl": "Volumgewicht (geen prijs)",
    }.get(key, "Volumetric weight (not a price)")
    note = {
        "fr": "Géométrie seule. Les dollars sont dans l’estimateur officiel. Souvent L×W×H/8000 en kg.",
        "es": "Solo geometría. El precio está en el estimador oficial. Casi siempre L×W×H/8000 en kg.",
        "de": "Nur Geometrie. Den Preis kennt der offizielle Schätzer. Meist L×W×H/8000 in kg.",
        "at": "Nur Geometrie. Den Preis kennt der offizielle Schätzer. Meist L×W×H/8000 in kg.",
        "nl": "Alleen meetkunde. De prijs staat in de officiële estimator. Meestal L×W×H/8000 in kg.",
    }.get(key, "Geometry only. Live dollars sit in the official estimator. Most air SKUs divide by 8000 (result in kg).")
    return f"""
<div class="vol" id="vol-calc">
  <strong>{escape(title)}</strong>
  <p>{escape(note)}</p>
  <div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(120px,1fr));gap:10px">
    <label>L cm<br><input id="vol-l" type="number" min="1" value="35"></label>
    <label>W cm<br><input id="vol-w" type="number" min="1" value="25"></label>
    <label>H cm<br><input id="vol-h" type="number" min="1" value="10"></label>
    <label>g<br><input id="vol-g" type="number" min="1" value="1000"></label>
    <label>÷<br>
      <select id="vol-d"><option value="8000" selected>/8000</option><option value="6000">/6000</option><option value="5000">/5000</option></select>
    </label>
  </div>
  <p id="vol-out" style="margin-top:12px;background:#fff5eb;padding:12px 14px;border-radius:10px"></p>
</div>
<script>
(function(){{
  function sgVol(){{
    var L=+document.getElementById('vol-l').value||0;
    var W=+document.getElementById('vol-w').value||0;
    var H=+document.getElementById('vol-h').value||0;
    var G=+document.getElementById('vol-g').value||0;
    var D=+document.getElementById('vol-d').value||8000;
    var vol=Math.round(L*W*H/D*1000);
    var billed=Math.ceil(Math.max(G,vol)/100)*100;
    var el=document.getElementById('vol-out');
    if(el) el.innerHTML='Volumetric <b>'+vol+' g</b> · billed <b>'+billed+' g</b> · not checkout.';
  }}
  ['vol-l','vol-w','vol-h','vol-g','vol-d'].forEach(function(id){{
    var n=document.getElementById(id); if(n) n.addEventListener(id==='vol-d'?'change':'input', sgVol);
  }});
  sgVol();
}})();
</script>
"""


def _faqs(key: str, d: dict) -> list[tuple[str, str]]:
    dest = d["dest_label"]
    if key == "fr":
        return [
            ("SugarGoo vend-il la marchandise ?", "Non. C’est un agent : il achète en Chine, photographie, tu paies la ligne internationale ensuite."),
            ("Où est le catalogue ?", "Sur cette accueil, via /api/products/ de ce host. Les 8 000 finds restent sur w2clinks."),
            ("La destination est-elle « EU » ?", "Non. L’estimateur veut un pays. Ici : France. Les dossiers Belgique de ce host ne définissent pas la France."),
            ("Les coupons ?", "L’article /sugargoo-coupons/ liste le pack ¥800 et 2026SG50. Vérifie dans My Coupons."),
            ("Invite dans le title ?", "Non. Le code d’affiliation est sur le bouton Register, pas dans <title>."),
            ("Stockage ?", "Blog officiel : 100 jours gratuits pour les ordres d’achat à partir de Packing Center."),
            ("Poids volumétrique ?", "L×W×H/8000 (kg) sur beaucoup de lignes aériennes. Le widget ci-dessus n’est pas un devis."),
            ("Douane ?", "Suit la SKU. Pas de conseil de sous-déclaration. Sources officielles le matin de l’envoi."),
            ("Ce host est-il sugargoo.com ?", "Non. Desk indépendant."),
            ("301 vers now.com ?", "Non. Les TLD du même agent restent séparés."),
            ("Photos QC ?", "Dans l’app, après arrivée entrepôt."),
            ("Deux paiements ?", "Oui : marchandise + domestique Chine, puis fret international."),
            ("USD vs EUR ?", "L’affichage officiel peut rester en USD. Lis le montant, pas seulement le symbole."),
            ("Avis déjà classé ?", "Oui — /sugargoo-review/ n’est pas écrasé."),
            ("Espagne 58 lignes ?", "Non. Les lignes ES restent un autre desk."),
        ]
    if key == "es":
        return [
            ("¿SugarGoo vende el producto?", "No. Es un agente de compras."),
            ("¿Dónde está el catálogo?", "En esta portada, /api/products/ de este host."),
            ("¿Es este sitio sugargoo.es?", "No. sugargoo.es es otro host. No hay 301."),
            ("¿Cupones en el title?", "No. 2026SG50 vive en /sugargoo-coupons/."),
            ("¿Aduana?", "Sigue la SKU. Sin infradeclaración. El artículo /aduana-iva-espana/ se conserva."),
            ("¿Almacén?", "100 días gratis en pedidos de compra desde Packing Center (blog oficial)."),
            ("¿Volumétrico?", "L×W×H/8000 en kg en muchas líneas."),
            ("¿Destino EU?", "El estimador pide un país. Aquí España."),
            ("¿QC?", "Fotos de almacén en la app."),
            ("¿Dos pagos?", "Sí: mercancía + doméstico China, luego internacional."),
            ("¿Invite?", "Solo en el enlace Register."),
            ("¿now.com?", "Hub de cupones en inglés, no un 301."),
            ("¿Catálogo en inglés?", "Sí. zapatillas suele dar 0; sneakers llena la rejilla."),
            ("¿IVA?", "Lee la SKU y la fuente de la Comisión / AEAT. No inventamos tipos."),
            ("¿Este Desk opera tu cuenta?", "No."),
        ]
    if key in ("de", "at"):
        land = "Österreich" if key == "at" else "Deutschland"
        return [
            ("Verkauft SugarGoo die Ware?", "Nein. Einkaufsagent."),
            ("Wo ist der Katalog?", "Auf dieser Startseite über /api/products/."),
            ("Invite im Title?", "Nein. Nur am Register-Button."),
            ("Lager?", "Offiziell 100 Tage gratis ab Packing Center bei Kaufaufträgen."),
            ("Zoll?", "Folgt der SKU. Keine Unterdeklaration."),
            ("Volumen?", "L×W×H/8000 in kg auf vielen Luftlinien."),
            ("Ziel EU?", f"Der Schätzer will ein Land. Hier: {land}."),
            ("Coupons?", "Im Coupon-Artikel, nicht in diesem Title."),
            ("QC?", "Lagerfotos in der App."),
            ("Zwei Zahlungen?", "Ja: Ware plus Inland, später Porto."),
            ("USD-Ziffern?", "Der Schalter ändert oft nur das Symbol."),
            ("301 auf now.com?", "Nein."),
            ("Turnschuhe?", "Oft 0 Treffer. Englisch sneakers."),
            ("Ist das sugargoo.com?", "Nein. Unabhängiger Desk."),
            ("Kakobuy?", "Anderer Agent, kein 301."),
        ]
    if key == "nl":
        return [
            ("Verkoopt SugarGoo de ware?", "Nee. Inkoopagent."),
            ("Waar is de catalogus?", "Op deze homepage via /api/products/."),
            ("Invite in de title?", "Nee. Alleen op Register."),
            ("Opslag?", "Officieel 100 dagen gratis vanaf Packing Center."),
            ("Douane?", "Volgt de SKU. Geen onderwaardering."),
            ("Volume?", "L×W×H/8000 in kg op veel luchtlijnen."),
            ("Bestemming EU?", "De estimator wil een land. Hier: Nederland."),
            ("Coupons?", "In het coupon-artikel, niet in deze title."),
            ("QC?", "Magazijnfoto’s in de app."),
            ("Twee betalingen?", "Ja."),
            ("USD-cijfers?", "De schakelaar verandert vaak alleen het symbool."),
            ("301 naar now.com?", "Nee."),
            ("Turnschuhe / sneakers?", "Lokale woorden geven vaak 0. Engels filtert."),
            ("Is dit sugargoo.com?", "Nee."),
            ("Kakobuy?", "Andere agent."),
        ]
    dest_q = dest
    extra = []
    if key == "now":
        extra = [
            ("Is this hostname a destination?", "No. Pick a member country or US/CA/AU/GB in the official estimator."),
            ("Will you overwrite the html articles?", "No. Coupon, Reddit, legit and spreadsheet html files stay."),
        ]
    elif key == "us":
        extra = [
            ("Where is CBP detail?", "Kept on /de-minimis-us-sugargoo/ and /cbp-declared-value-us/. This homepage does not invent a dollar de-minimis."),
            ("USPS times?", "Kept on /sugargoo-shipping-times-us/."),
        ]
    elif key == "au":
        extra = [
            ("GST?", "The ranked GST article stays at /gst-import-australia/. We do not copy a rate into this title."),
            ("Australia Post?", "Read the live SKU. This desk does not invent a last-mile."),
        ]
    elif key == "ca":
        extra = [
            ("Why does GSC rank CBSA?", "Because /cbsa-import-canada/ already has the click. That file stays. This homepage is the catalogue."),
            ("Is this sugargoo.ca?", "No. Different host. No 301."),
        ]
    elif key == "uk":
        extra = [
            ("HMRC?", "VAT article stays if present. No declared-value coaching."),
            ("Northern Ireland?", "Often another carrier product."),
        ]
    base = [
        ("Does SugarGoo sell the goods?", "No. It is a purchasing agent: two payments, warehouse photos, then an international SKU."),
        ("Where is the catalogue?", "On this homepage from this host’s /api/products/. Thousands of finds stay on w2clinks."),
        ("Invite in the title?", "No. The affiliate URL is the Register button only."),
        (f"Is destination {dest_q} a TLD?", "The estimator wants a country code. This hostname is a desk, not a customs territory."),
        ("Free storage?", "Official blog: 100 days on purchasing orders from Packing Center."),
        ("Volumetric weight?", "Most air SKUs: L×W×H/8000 in kilograms. The widget is geometry, not a quote."),
        ("Customs?", "Follows the booked SKU. No under-declaration tips. Use the official destination source the morning you ship."),
        ("Coupons in this title?", "No. 2026SG50 and the ¥800 pack live on the coupon URL."),
        ("QC photos?", "In-app after warehouse arrival."),
        ("USD digits?", "The official currency switcher has been observed to change the symbol without converting the number."),
        ("301 to another SugarGoo TLD?", "No. Same-agent country hosts stay independent."),
        ("Is this sugargoo.com?", "No. Independent desk."),
        ("Local search words?", "The index is English. Local words often return zero cards."),
    ]
    out = (extra + base)[:15]
    while len(out) < 15:
        out.append((f"Independent desk {len(out)+1}?", f"Yes. {d['host']} does not run your SugarGoo account."))
    return out[:15]


def _faq_block(key: str, d: dict) -> str:
    h = {"fr": "Questions", "es": "Preguntas", "de": "Fragen", "at": "Fragen", "nl": "Vragen"}.get(key, "FAQ")
    items = []
    for i, (q, a) in enumerate(_faqs(key, d)):
        op = " open" if i == 0 else ""
        items.append(f'<details class="sg-faq"{op}><summary>{escape(q)}</summary><p>{escape(a)}</p></details>')
    return f'<section class="sg-sec" id="faq"><h2>{h}</h2>{"".join(items)}</section>'


def _keep(d: dict) -> str:
    links = "".join(f'<a href="{escape(h)}"><strong>{escape(l)}</strong><span> kept · not overwritten</span></a>' for h, l in d["keep"])
    return f'<section class="sg-sec" id="kept"><h2>Already ranking on this host</h2><div class="keep">{links}</div></section>'


def _lab(key: str, d: dict) -> str:
    if not d.get("dest"):
        p = (
            f"The official estimator needs a <strong>country</strong>, not this hostname. "
            f'Open <a href="{EST}">{EST}</a> and pick US, CA, FR, ES… Spain-only copy stays off this hub.'
        )
    else:
        p = (
            f"Open the official SugarGoo freight estimate with destination <strong>{escape(d['dest_label'])}</strong> "
            f"before you pay international freight. Snapshot habit: 1000 g / 35×25×10 cm, clothing. "
            f"Lab note {DATE}. USD digits may stay dollars when only the symbol changes."
        )
    return f"""<section class="sg-sec" id="lab"><h2>Freight lab</h2>
<p class="ssub">{p}</p>
<p><a class="btn btn-primary" href="{EST}">Official freight estimate →</a></p>
{_vol(key)}
</section>"""


def build_home(key: str) -> str:
    d = HOSTS[key]
    m = HOME_META[key]
    if INVITE in m["title"] or COUPON in m["title"]:
        raise RuntimeError(f"{key}: invite/coupon in title")
    html = _chrome_head(key, d, m["title"], m["desc"])
    html += _header(key, d)
    html += f"""<section class="sg-hero">
  <div class="hbg">Lab {DATE}</div>
  <h1>{m["h1"]}</h1>
  <p class="hsub">{m["hsub"]}</p>
  <p class="eu-badge">{escape(d["badge"])}</p>
  <div class="sg-ctas">
    <a class="btn btn-primary" href="#catalog">{escape({"fr":"Catalogue","es":"Catálogo","de":"Katalog","at":"Katalog","nl":"Catalogus"}.get(key,"Catalogue"))}</a>
    <a class="btn btn-outline" href="{EST}">{escape({"fr":"Estimateur","es":"Estimador","de":"Schätzer","at":"Schätzer","nl":"Estimator"}.get(key,"Estimator"))}</a>
    <a class="btn btn-outline" href="{REG}" target="_blank" rel="noopener sponsored">{escape({"fr":"S’inscrire","es":"Registrarse","de":"Registrieren","at":"Registrieren","nl":"Registreren"}.get(key,"Register"))}</a>
  </div>
</section>
"""
    html += _catalog(key)
    html += _nine(key)
    html += _lab(key, d)
    html += _keep(d)
    html += _faq_block(key, d)
    html += _footer(key, d)
    return html


def _wc(html: str) -> int:
    return len(re.findall(r"[A-Za-zÀ-ÿ]{3,}", html))


def _validate() -> None:
    for key, d in HOSTS.items():
        html = build_home(key)
        title = re.search(r"<title>(.*?)</title>", html, flags=re.S).group(1)
        if INVITE in title or COUPON in title:
            raise SystemExit(f"{key}: code in title")
        if "Georgia" in html or "gsc-editor-notes" in html or "impressions on a template" in html:
            raise SystemExit(f"{key}: junk/Georgia leftover")
        if "#00C853" in html:
            raise SystemExit(f"{key}: HipoBuy green leaked")
        for tok in ('id="catalog"', 'id="states"', 'id="vol-calc"', 'id="faq"', "sugargoo-theme.css", "/api/products/"):
            if tok not in html:
                raise SystemExit(f"{key}: missing {tok}")
        nfaq = len(re.findall(r"class=\"sg-faq\"", html))
        if nfaq < 15:
            raise SystemExit(f"{key}: faq {nfaq}")
        if key == "now" and ("58 líneas" in html or "ES AIR" in html):
            raise SystemExit("now.com copied Spain lines")
        if key == "fr" and ("Belgique" in title or "Belgium" in title or "France / BE" in html):
            raise SystemExit("fr title became Belgium")
        if "locale-switcher" not in html:
            raise SystemExit(f"{key}: missing locale-switcher")
        n = _wc(html)
        print(f"{'OK' if n>=600 else 'SHORT':5} {key}/home words={n} faq={nfaq} {title[:56]}")
        if n < 500:
            raise SystemExit(f"{key} too short")


def _connect():
    try:
        import paramiko
    except ImportError:
        import subprocess

        subprocess.check_call([sys.executable, "-m", "pip", "install", "paramiko", "-q"])
        import paramiko

    password = os.environ.get("ORIGIN_SSH_PASS")
    if not password:
        raise SystemExit("Set ORIGIN_SSH_PASS")
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect("31.97.41.31", username="root", password=password, timeout=30)
    return client


def _run(client, cmd: str, timeout: int = 60) -> str:
    _, stdout, stderr = client.exec_command(cmd, timeout=timeout)
    return (stdout.read() + stderr.read()).decode(errors="replace").strip()


ORDER = ["us", "au", "fr", "ca", "now", "uk", "es", "de", "at", "nl"]


def _only() -> list[str]:
    if "--only" not in sys.argv:
        return list(ORDER)
    i = sys.argv.index("--only")
    if i + 1 >= len(sys.argv):
        raise SystemExit("usage: --only us,au,fr")
    keys = [k.strip() for k in sys.argv[i + 1].split(",") if k.strip()]
    bad = [k for k in keys if k not in HOSTS]
    if bad:
        raise SystemExit(f"unknown --only {bad}")
    return keys


def main() -> None:
    _validate()
    put_keys = _only()
    for key in ORDER:
        d = HOSTS[key]
        html = build_home(key)
        dest = ROOT / "sites" / d["host"] / "overlay" / "index.html"
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(html, encoding="utf-8")
        print("wrote", dest, dest.stat().st_size)
    if "--dry" in sys.argv:
        print("dry-run ok")
        return
    client = _connect()
    sftp = client.open_sftp()
    stamp = time.strftime("%Y%m%d-%H%M%S")
    bak = f"/www/backup/sugargoo-home-{stamp}"
    print(_run(client, f"mkdir -p '{bak}'"))
    uploaded = []
    for key in put_keys:
        d = HOSTS[key]
        local = ROOT / "sites" / d["host"] / "overlay" / "index.html"
        remote = f"/www/wwwroot/{d['host']}/index.html"
        _run(client, f"cp -a '{remote}' '{bak}/{d['host']}-index.html'")
        sftp.put(str(local), remote)
        uploaded.append(remote)
        print("PUT", remote, "bytes", local.stat().st_size)
    if uploaded:
        _run(client, "chown www:www " + " ".join(f"'{p}'" for p in uploaded) + " && chmod 644 " + " ".join(f"'{p}'" for p in uploaded))
    print("backup", bak, "put", ",".join(put_keys))
    sftp.close()
    client.close()


if __name__ == "__main__":
    main()
