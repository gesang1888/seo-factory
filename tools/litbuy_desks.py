#!/usr/bin/env python3
"""Restore LitBuy country-desk homepages in original CMS chrome.

Puts catalogue on /, Inter + existing style.css (yellow #ffc400 / dach red / US blue).
Not HipoBuy green, not Georgia memos, not SugarGoo orange.
Does not overwrite coupons / Zoll / CBSA / IOSS / now.com html articles.
Adds independent Help/News/About pages (local slugs, same CMS chrome).
Homepage editorial: agent is not a shop, spreadsheet is not Excel, Restricted items, 16-cat wall.
Dated official SPA screenshots under /media/ (litbuy.com + shipping-estimate).
Warehouse: 90 free days from stocked/listed, 120-day max.
Does not 301 country TLDs together or onto .net / now.com / unique dests.
Invite/coupon codes stay off titles (do not copy O4K87NHKR).
No declared-value coaching. FR is France, not Belgium. .eu and now.com are hubs.
"""
from __future__ import annotations

import json
import os
import re
import sys
import time
from html import escape
from pathlib import Path

_TOOLS = Path(__file__).resolve().parent
if str(_TOOLS) not in sys.path:
    sys.path.insert(0, str(_TOOLS))
from desk_fx import EXTRA_CSS_FX, catalog_block, currency_for, ui_copy
from desk_template import (
    SKIP_CSS,
    breadcrumb_ld,
    customs_for,
    faq_ld,
    independence_copy,
    inject_jsonld,
    itemlist_ld,
    keep_copy,
    lab_copy,
    long_faqs,
    og_locale,
    organization_ld,
    skip_label,
    skip_link,
    validate_desk,
    vol_js_labels,
    webpage_ld,
)
from litbuy_desk_trust import CAT_LABELS, CAT_WALL, loc as _loc, pack as _trust_pack

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "sites"
EST = "https://litbuy.com/shipping-estimate"
OFFICIAL = "https://litbuy.com/"
REG = "https://litbuy.com/register"
INVITE = "O4K87NHKR"
COUPON = "2026SG50"
W2C = "https://w2clinks.com/spreadsheet/litbuy/"
DATE = "1 Oct 2026"
SHOT_HOME = "/media/official-home-20261001.jpg"
SHOT_EST = "/media/estimator-20261001.jpg"
SHOT_HELP = "/media/help-restricted-20261001.jpg"
SHOT_STORE = "/media/storage-period-20261001.jpg"

HOSTS = {
    "at": {
        "host": "litbuy.at",
        "lang": "de-AT",
        "theme": "litbuy-theme-dach",
        "css": ["style.css?v=20261001-home", "theme-dach.css?v=20260531-theme"],
        "locale": "Österreich",
        "dest": "AT",
        "dest_label": "Österreich",
        "badge": "Österreich · EUR · BMF Zoll",
        "mail": "support@litbuy.at",
        "utm": "litbuy_at",
        "logo": "/assets/images/litbuy-logo-eu.png",
        "keep": [
            ("/post-at-sendungsverfolgung/", "Post AT tracking (ranked URL)"),
            ("/zoll-ust-oesterreich/", "Zoll / USt"),
            ("/ratgeber-oesterreich/", "Ratgeber Österreich"),
            ("/litbuy-spreadsheet/", "Spreadsheet guide"),
            ("/litbuy-coupons/", "Coupons (article kept; codes off this title)"),
        ],
    },
    "ca": {
        "host": "litbuyspreadsheets.ca",
        "lang": "en-CA",
        "theme": "litbuy-theme-uk-ca",
        "css": ["style.css?v=20261001-home", "theme-uk-ca.css?v=20260531-theme"],
        "locale": "Canada",
        "dest": "CA",
        "dest_label": "Canada",
        "badge": "Canada · CAD · CBSA",
        "mail": "support@litbuyspreadsheets.ca",
        "utm": "litbuyspreadsheets_ca",
        "logo": "/assets/images/litbuy-logo.png",
        "keep": [
            ("/litbuy-shipping-canada/", "Shipping to Canada (ranked URL)"),
            ("/cbsa-import-canada/", "CBSA import"),
            ("/gst-hst-import-canada/", "GST / HST"),
            ("/litbuy-spreadsheet/", "Spreadsheet guide"),
            ("/litbuy-coupons/", "Coupons"),
        ],
    },
    "it": {
        "host": "litbuyspreadsheet.it",
        "lang": "it-IT",
        "theme": "litbuy-theme-south",
        "css": ["style.css?v=20261001-home", "theme-south.css?v=20260531-theme"],
        "locale": "Italia",
        "dest": "IT",
        "dest_label": "l’Italia",
        "badge": "Italia · EUR · dogana",
        "mail": "support@litbuyspreadsheet.it",
        "utm": "litbuyspreadsheet_it",
        "logo": "/assets/images/litbuy-logo.png",
        "keep": [
            ("/dogana-poste-italiane/", "Dogana Poste Italiane"),
            ("/iva-importazione-italia/", "IVA importazione"),
            ("/guide-italia/", "Guide Italia"),
            ("/litbuy-spreadsheet/", "Spreadsheet"),
            ("/litbuy-coupons/", "Coupon"),
        ],
    },
    "eu": {
        "host": "litbuyspreadsheet.eu",
        "lang": "en",
        "theme": "",
        "css": ["style.css?v=20261001-home"],
        "locale": "Europe",
        "dest": None,
        "dest_label": "a country in the estimator",
        "badge": "English Europe hub · pick a country in-app",
        "mail": "support@litbuyspreadsheet.eu",
        "utm": "litbuyspreadsheet_eu",
        "logo": "/assets/images/litbuy-logo-eu.png",
        "keep": [
            ("/ioss-import-vat-eu/", "IOSS / import VAT"),
            ("/ecommerce-vat-reform-eu/", "e-commerce VAT reform"),
            ("/eu-parcel-thresholds-guide/", "Parcel thresholds"),
            ("/what-is-litbuy/", "What is LitBuy"),
            ("/litbuy-spreadsheet/", "Spreadsheet"),
            ("/litbuy-coupons/", "Coupons"),
        ],
    },
    "es": {
        "host": "litbuyspreadsheets.es",
        "lang": "es-ES",
        "theme": "litbuy-theme-south",
        "css": ["style.css?v=20261001-home", "theme-south.css?v=20260531-theme"],
        "locale": "España",
        "dest": "ES",
        "dest_label": "España",
        "badge": "España · EUR · aduana",
        "mail": "support@litbuyspreadsheets.es",
        "utm": "litbuyspreadsheets_es",
        "logo": "/assets/images/litbuy-logo.png",
        "keep": [
            ("/aduana-correos-espana/", "Aduana Correos"),
            ("/iva-importacion-espana/", "IVA importación"),
            ("/guias-espana/", "Guías"),
            ("/litbuy-spreadsheet/", "Spreadsheet"),
            ("/litbuy-coupons/", "Cupones"),
        ],
    },
    "fr": {
        "host": "litspreadsheet.fr",
        "lang": "fr-FR",
        "theme": "litbuy-theme-fr",
        "css": ["style.css?v=20261001-home", "theme-fr-editorial.css?v=20260531-theme"],
        "locale": "France",
        "dest": "FR",
        "dest_label": "la France",
        "badge": "France · EUR · douane FR",
        "mail": "support@litspreadsheet.fr",
        "utm": "litspreadsheet_fr",
        "logo": "/assets/images/litbuy-logo.png",
        "keep": [
            ("/livraison-litbuy-france/", "Livraison France"),
            ("/tva-import-france/", "TVA import"),
            ("/colissimo-douane-france/", "Colissimo / douane"),
            ("/litbuy-spreadsheet/", "Spreadsheet"),
            ("/litbuy-coupons/", "Coupons"),
        ],
    },
    "us": {
        "host": "litbuyspreadsheets.us",
        "lang": "en-US",
        "theme": "litbuy-theme-us",
        "css": ["style.css?v=20261001-home", "theme-us.css?v=20260531-theme"],
        "locale": "USA",
        "dest": "US",
        "dest_label": "the United States",
        "badge": "United States · USD · USPS",
        "mail": "support@litbuyspreadsheets.us",
        "utm": "litbuyspreadsheets_us",
        "logo": "/assets/images/litbuy-logo.png",
        "keep": [
            ("/de-minimis-us-litbuy/", "CBP / de minimis — educational"),
            ("/duties-taxes-usps-fedex/", "USPS / FedEx duties"),
            ("/litbuy-shipping-times-us/", "US shipping times"),
            ("/us-customs-declaration-guide/", "Customs declaration guide"),
            ("/litbuy-spreadsheet/", "Spreadsheet"),
            ("/litbuy-coupons/", "Coupons"),
        ],
    },
    "nl": {
        "host": "litbuyspreadsheets.nl",
        "lang": "nl-NL",
        "theme": "litbuy-theme-benelux",
        "css": ["style.css?v=20261001-home", "theme-benelux.css?v=20260531-theme"],
        "locale": "Nederland",
        "dest": "NL",
        "dest_label": "Nederland",
        "badge": "Nederland · EUR · douane",
        "mail": "support@litbuyspreadsheets.nl",
        "utm": "litbuyspreadsheets_nl",
        "logo": "/assets/images/litbuy-logo.png",
        "keep": [
            ("/douane-nederland-dhl/", "Douane / DHL"),
            ("/btw-import-nederland/", "BTW import"),
            ("/litbuy-verzendkosten-nederland/", "Verzendkosten"),
            ("/ideal-betalen-litbuy/", "iDEAL"),
            ("/litbuy-spreadsheet/", "Spreadsheet"),
            ("/litbuy-coupons/", "Coupons"),
        ],
    },
    "uk": {
        "host": "litbuyspreadsheet.me.uk",
        "lang": "en-GB",
        "theme": "litbuy-theme-uk-ca",
        "css": ["style.css?v=20261001-home", "theme-uk-ca.css?v=20260531-theme"],
        "locale": "UK",
        "dest": "GB",
        "dest_label": "the United Kingdom",
        "badge": "United Kingdom · GBP · HMRC",
        "mail": "support@litbuyspreadsheet.me.uk",
        "utm": "litbuyspreadsheet_meuk",
        "logo": "/assets/images/litbuy-logo.png",
        "keep": [
            ("/vat-on-imports-uk-2026/", "UK import VAT"),
            ("/hmrc-import-charges-uk/", "HMRC charges"),
            ("/litbuy-shipping-uk/", "Shipping to the UK"),
            ("/royal-mail-customs-uk/", "Royal Mail customs"),
            ("/litbuy-spreadsheet/", "Spreadsheet"),
            ("/litbuy-coupons/", "Coupons (article kept; codes off this title)"),
        ],
    },
    "now": {
        "host": "litbuyspreadsheetnow.com",
        "lang": "en",
        "theme": "",
        "css": ["style.css?v=20261001-home", "now-hub.css?v=20260531-theme"],
        "locale": "Global",
        "dest": None,
        "dest_label": "a country in the estimator",
        "badge": "Coupon / spreadsheet hub · pick a country in-app",
        "mail": "support@litbuyspreadsheetnow.com",
        "utm": "litbuyspreadsheetnow",
        "logo": "/assets/images/litbuy-logo.png",
        "keep": [
            ("/litbuy-coupon-2026.html", "Coupons 2026 html"),
            ("/litbuy-reddit-2026.html", "Reddit html"),
            ("/best-litbuy-spreadsheet-2026.html", "Spreadsheet html"),
            ("/is-litbuy-legit-2026.html", "Legit html"),
            ("/how-does-litbuy-work-2026.html", "How it works html"),
        ],
    },
}

HOME_META = {
    "at": {
        "title": "Mit LitBuy nach Österreich bestellen — aus China auf eine AT-Adresse",
        "desc": "Unabhängiger AT-Desk: Katalog auf dieser Startseite. Post-AT- und Zoll-URLs bleiben. Lab 1 Oct 2026. Keine Unterdeklaration.",
        "h1": "Mit <em>LitBuy</em> nach Österreich bestellen",
        "hsub": "Aus China auf eine österreichische Straße. Katalog, FAQ und Schätzer-Hinweis auf dieser Startseite. Ranked URLs /post-at-sendungsverfolgung/ und /zoll-ust-oesterreich/ bleiben.",
    },
    "ca": {
        "title": "Buy from China to Canada with LitBuy",
        "desc": "Independent CA desk on this host. Ranked shipping-Canada article stays. Catalogue on the homepage. Lab 1 Oct 2026.",
        "h1": "Using LitBuy to ship from China to <em>Canada</em>",
        "hsub": "The ranked URL is still /litbuy-shipping-canada/. This homepage is the CA destination desk, not litbuy.ca.",
    },
    "it": {
        "title": "Comprare in Cina e spedire in Italia con LitBuy",
        "desc": "Desk IT indipendente: catalogo su questa home. Dogana e IVA restano sulle loro URL. Lab 1 ott 2026.",
        "h1": "Spedire dalla Cina in <em>Italia</em> con LitBuy",
        "hsub": "I clic Google sono sulla home — la teniamo come catalogo. Le guide dogana/IVA restano. Destinazione Italia nell’estimator.",
    },
    "eu": {
        "title": "LitBuy English Europe hub — pick a country in the estimator",
        "desc": "Independent English EU hub. Destination is a country code in the official estimator, not this TLD. Lab 1 Oct 2026.",
        "h1": "LitBuy spreadsheet hub for <em>Europe</em>",
        "hsub": "This host is not a destination. Open shipping-estimate with AT, IT, ES, FR, NL… IOSS and VAT articles stay. No Spain line-count copy.",
    },
    "es": {
        "title": "Comprar en China y enviar a España con LitBuy",
        "desc": "Desk ES independiente. Catálogo en esta portada. Aduana Correos se queda en su URL. Lab 1 oct 2026.",
        "h1": "Enviar de China a <em>España</em> con LitBuy",
        "hsub": "El artículo de aduana sigue en /aduana-correos-espana/. Esta portada es el catálogo. No copiamos las 58 líneas de otro agente.",
    },
    "fr": {
        "title": "Acheter en Chine et envoyer en France avec LitBuy",
        "desc": "Desk FR indépendant : catalogue sur cette accueil. Destination France dans l’estimateur. Pas la Belgique. Lab 1 oct. 2026.",
        "h1": "Envoyer de Chine en <em>France</em> avec LitBuy",
        "hsub": "Les articles Colissimo et TVA restent. Cette accueil est le catalogue. La destination dans l’estimateur est la France, pas la Belgique.",
    },
    "us": {
        "title": "Buy from China to the United States with LitBuy",
        "desc": "Independent US desk: catalogue on this homepage, USPS/CBP sources, official freight estimate. Lab 1 Oct 2026. No under-declaration tips.",
        "h1": "Using LitBuy to ship from China to the <em>US</em>",
        "hsub": "Purchasing agent to a US street: warehouse photos, then an international SKU. Catalogue, FAQ and the freight lab sit on this homepage.",
    },
    "nl": {
        "title": "Met LitBuy naar Nederland verzenden — kopen in China op een NL-adres",
        "desc": "Onafhankelijke NL-desk: catalogus op deze homepage. Lab 1 okt 2026. Geen onderwaardering.",
        "h1": "Met <em>LitBuy</em> naar Nederland verzenden",
        "hsub": "Uit China naar een Nederlands huisadres. Catalogus en FAQ op deze homepage. Douane/BTW-artikelen blijven.",
    },
    "uk": {
        "title": "Buy from China to the UK with LitBuy",
        "desc": "Independent UK desk on .me.uk: catalogue on this homepage, HMRC VAT article kept. Lab 1 Oct 2026.",
        "h1": "Using LitBuy to ship a <em>UK haul</em> from China",
        "hsub": "GBP haul log on this host. Destination in the estimator is a GB address. Unique .uk dests are not 301’d here.",
    },
    "now": {
        "title": "LitBuy coupon desk — pick a country in the estimator",
        "desc": "Independent English hub. Destination is a country code in the official estimator, not this hostname. Existing html articles stay.",
        "h1": "LitBuy coupons and spreadsheet hub",
        "hsub": "This host is not a destination. Open the official estimator with US, CA, FR… The dated html files already on this host stay put.",
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
.sg-hero h1 em{font-style:normal;color:var(--primary,#ffc400)}
.sg-hero .hsub{color:#475569;font-size:16px;line-height:1.6;max-width:720px}
.sg-hero .hbg{display:inline-block;font-size:12px;font-weight:700;background:var(--primary-soft,#fff8df);color:var(--primary,#ffc400);padding:4px 10px;border-radius:999px;margin-bottom:12px}
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
.sg-card .pr{font-weight:800;color:var(--primary,#ffc400)}
.sg-card a.buy{margin:0 10px 10px;text-align:center;padding:8px;border-radius:8px;background:var(--primary,#ffc400);color:#fff;font-size:12.5px;font-weight:600;text-decoration:none}
.sg-chips{display:flex;gap:8px;flex-wrap:wrap;margin:8px 0 4px}
.sg-chips button{border:1px solid #e5e7eb;background:#fff;border-radius:999px;padding:6px 12px;font:inherit;cursor:pointer}
.sg-chips button.on{background:var(--primary-soft,#fff8df);border-color:var(--primary,#ffc400);color:var(--primary,#ffc400);font-weight:600}
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
.keep a:hover{border-color:var(--primary,#ffc400)}
.vol{border:1px solid #e5e7eb;border-radius:16px;padding:16px 18px;margin:16px 0;background:#fff}
.vol input,.vol select{width:100%;height:36px;border:1.5px solid #e5e7eb;border-radius:8px;padding:0 8px}
figure.shot{margin:16px 0}
figure.shot img{width:100%;max-width:920px;height:auto;border:1px solid #e5e7eb;border-radius:12px;background:#f8fafc}
figure.shot figcaption{font-size:13px;color:#64748b;margin-top:6px}
.sg-split{display:grid;grid-template-columns:1.05fr .95fr;gap:28px;align-items:start;margin:8px 0 4px}
@media(max-width:860px){.sg-split{grid-template-columns:1fr}}
.sg-prose p{color:#334155;line-height:1.75;margin:0 0 12px}
.sg-prose .lead{font-size:17px;color:#1e293b}
.sg-cats{display:grid;grid-template-columns:repeat(auto-fill,minmax(148px,1fr));gap:12px}
a.sg-cat{position:relative;display:block;border-radius:12px;overflow:hidden;color:#fff;text-decoration:none;background:#0f172a}
a.sg-cat img{width:100%;aspect-ratio:1;object-fit:cover;display:block}
a.sg-cat .b{position:absolute;left:0;right:0;bottom:0;padding:10px 12px;background:linear-gradient(transparent,rgba(15,23,42,.78))}
a.sg-cat strong{display:block;font-size:14px}
a.sg-cat span{font-size:11px;opacity:.85;letter-spacing:.2px}
.sg-about h2{font-size:22px;margin:28px 0 8px}
.sg-about h3{font-size:16px;margin:18px 0 6px}
.sg-about p{color:#334155;line-height:1.75;margin:0 0 12px}
""" + EXTRA_CSS_FX + SKIP_CSS


HREFLANG = [
    ("en", "litbuyspreadsheetnow.com"),
    ("en-US", "litbuyspreadsheets.us"),
    ("en-CA", "litbuyspreadsheets.ca"),
    ("en-GB", "litbuyspreadsheet.me.uk"),
    ("en-150", "litbuyspreadsheet.eu"),
    ("fr-FR", "litspreadsheet.fr"),
    ("es", "litbuyspreadsheets.es"),
    ("de-AT", "litbuy.at"),
    ("it-IT", "litbuyspreadsheet.it"),
    ("nl-NL", "litbuyspreadsheets.nl"),
]


def _hreflang() -> str:
    bits = [
        f'<link rel="alternate" hreflang="{escape(code)}" href="https://{escape(host)}/">'
        for code, host in HREFLANG
    ]
    bits.append('<link rel="alternate" hreflang="x-default" href="https://litbuyspreadsheetnow.com/">')
    return "\n".join(bits)


def _locale_switcher(key: str, d: dict) -> str:
    u = ui_copy(_loc(key))
    rows = [
        (u["en_group"], [
            ("now", "litbuyspreadsheetnow.com", "English (Global)"),
            ("eu", "litbuyspreadsheet.eu", "English (Europe)"),
            ("uk", "litbuyspreadsheet.me.uk", "English (UK)"),
            ("ca", "litbuyspreadsheets.ca", "English (Canada)"),
            ("us", "litbuyspreadsheets.us", "English (USA)"),
        ]),
        (u["local_group"], [
            ("fr", "litspreadsheet.fr", "Français (France)"),
            ("es", "litbuyspreadsheets.es", "Español (España)"),
            ("it", "litbuyspreadsheet.it", "Italiano"),
            ("nl", "litbuyspreadsheets.nl", "Nederlands"),
            ("at", "litbuy.at", "Deutsch (Österreich)"),
        ]),
    ]
    parts = ['<div class="locale-switcher" data-locale-switcher>']
    parts.append(
        '<button type="button" class="locale-switcher-btn" data-locale-toggle '
        f'aria-haspopup="listbox" aria-expanded="false" aria-label="{escape(u["choose_lang"])}">'
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
        f"{escape(u['register_on'].format(brand='LitBuy'))}</a></div>"
    )
    parts.append("</div></div>")
    return "".join(parts)


def _trust_paths(key: str) -> dict:
    """Local Help/News/About slugs, HipoBuy-country style."""
    if key == "es":
        return {
            "help": "ayuda",
            "news": "novedades",
            "about": "sobre-nosotros",
            "help_lab": "Ayuda",
            "news_lab": "Novedades",
            "about_lab": "Sobre",
        }
    if key == "fr":
        return {
            "help": "aide",
            "news": "actualites",
            "about": "a-propos",
            "help_lab": "Aide",
            "news_lab": "Actualités",
            "about_lab": "À propos",
        }
    if key == "at":
        return {
            "help": "hilfe",
            "news": "neuigkeiten",
            "about": "ueber-uns",
            "help_lab": "Hilfe",
            "news_lab": "Neuigkeiten",
            "about_lab": "Über uns",
        }
    if key == "nl":
        return {
            "help": "hulp",
            "news": "nieuws",
            "about": "over-ons",
            "help_lab": "Hulp",
            "news_lab": "Nieuws",
            "about_lab": "Over ons",
        }
    if key == "it":
        return {
            "help": "aiuto",
            "news": "novita",
            "about": "chi-siamo",
            "help_lab": "Aiuto",
            "news_lab": "Novità",
            "about_lab": "Chi siamo",
        }
    return {
        "help": "help",
        "news": "news",
        "about": "who-we-are",
        "help_lab": "Help",
        "news_lab": "News",
        "about_lab": "About",
    }


def _nav(key: str, d: dict, page: str = "home") -> str:
    t = _trust_paths(key)
    hp, np, ap = f"/{t['help']}/", f"/{t['news']}/", f"/{t['about']}/"
    if key == "fr":
        items = [
            ("/", "Accueil", page == "home"),
            ("/litbuy-spreadsheet/", "Spreadsheet", page == "sheet"),
            ("/litbuy-coupons/", "Coupons", page == "coupons"),
            (hp, t["help_lab"], page == "help"),
            (np, t["news_lab"], page == "news"),
            (ap, t["about_lab"], page == "about"),
            ("/#lab", "Livraison", page == "lab"),
        ]
        cta, browse = "Voir le catalogue", "Spreadsheet complète"
    elif key == "es":
        items = [
            ("/", "Inicio", page == "home"),
            ("/litbuy-spreadsheet/", "Spreadsheet", page == "sheet"),
            ("/litbuy-coupons/", "Cupones", page == "coupons"),
            (hp, t["help_lab"], page == "help"),
            (np, t["news_lab"], page == "news"),
            (ap, t["about_lab"], page == "about"),
            ("/#lab", "Envíos", page == "lab"),
        ]
        cta, browse = "Ver catálogo", "Spreadsheet completa"
    elif key == "at":
        items = [
            ("/", "Start", page == "home"),
            ("/litbuy-spreadsheet/", "Spreadsheet", page == "sheet"),
            ("/litbuy-coupons/", "Coupons", page == "coupons"),
            (hp, t["help_lab"], page == "help"),
            (np, t["news_lab"], page == "news"),
            (ap, t["about_lab"], page == "about"),
            ("/#lab", "Versand", page == "lab"),
        ]
        cta, browse = "Katalog", "Ganzes Spreadsheet"
    elif key == "nl":
        items = [
            ("/", "Home", page == "home"),
            ("/litbuy-spreadsheet/", "Spreadsheet", page == "sheet"),
            ("/litbuy-coupons/", "Coupons", page == "coupons"),
            (hp, t["help_lab"], page == "help"),
            (np, t["news_lab"], page == "news"),
            (ap, t["about_lab"], page == "about"),
            ("/#lab", "Verzending", page == "lab"),
        ]
        cta, browse = "Catalogus", "Volledige spreadsheet"
    elif key == "it":
        items = [
            ("/", "Home", page == "home"),
            ("/litbuy-spreadsheet/", "Spreadsheet", page == "sheet"),
            ("/litbuy-coupons/", "Coupon", page == "coupons"),
            (hp, t["help_lab"], page == "help"),
            (np, t["news_lab"], page == "news"),
            (ap, t["about_lab"], page == "about"),
            ("/#lab", "Spedizione", page == "lab"),
        ]
        cta, browse = "Catalogo", "Spreadsheet completa"
    elif key == "now":
        items = [
            ("/", "Home", page == "home"),
            ("/litbuy-coupon-2026.html", "Coupons", page == "coupons"),
            ("/best-litbuy-spreadsheet-2026.html", "Spreadsheet", page == "sheet"),
            (hp, t["help_lab"], page == "help"),
            (np, t["news_lab"], page == "news"),
            (ap, t["about_lab"], page == "about"),
            ("/#lab", "Shipping", page == "lab"),
        ]
        cta, browse = "Browse catalogue", "Full spreadsheet"
    else:
        items = [
            ("/", "Home", page == "home"),
            ("/litbuy-spreadsheet/", "Spreadsheet", page == "sheet"),
            ("/litbuy-coupons/", "Coupons", page == "coupons"),
            (hp, t["help_lab"], page == "help"),
            (np, t["news_lab"], page == "news"),
            (ap, t["about_lab"], page == "about"),
            ("/#lab", "Shipping", page == "lab"),
        ]
        cta, browse = "Browse catalogue", "Full spreadsheet"
    nav = "".join(
        f'<a href="{escape(href)}"' + (' class="active"' if on else "") + f">{escape(lab)}</a>"
        for href, lab, on in items
    )
    w2c = f"{W2C}?utm_source={d['utm']}&utm_medium=desk&utm_campaign=litbuy"
    return nav, cta, browse, w2c


def _css_links(d: dict) -> str:
    return "\n".join(
        f'<link rel="stylesheet" href="/assets/css/{escape(href)}">' for href in d.get("css") or ["style.css?v=20261001-home"]
    )


def _facts(key: str) -> dict:
    d = HOSTS[key]
    dest = d.get("dest")
    cname, curl = customs_for(dest)
    return {
        "agent": "LitBuy",
        "host": d["host"],
        "lang": d["lang"],
        "loc": _loc(key),
        "dest": dest,
        "dest_label": d["dest_label"],
        "ccy": currency_for(key, d),
        "customs": cname,
        "customs_url": curl,
        "storage": "90 free days from stocked/listed, 120-day max",
        "estimator": EST,
        "official": OFFICIAL,
        "date": DATE,
        "email": d["mail"],
        "codes_off_title": [INVITE, COUPON],
        "strict_html_codes": True,
    }


def _reg_lab(key: str) -> str:
    return {"fr": "S’inscrire", "es": "Registrarse", "at": "Registrieren", "nl": "Registreren", "it": "Registrati"}.get(key, "Register")


def _chrome_head(key: str, d: dict, title: str, desc: str, path: str = "/") -> str:
    host = d["host"]
    if not path.startswith("/"):
        path = "/" + path
    canonical = f"https://{host}{path}"
    logo = d.get("logo") or "/assets/images/litbuy-logo.png"
    ld = webpage_ld(url=canonical, name=title, desc=desc, lang=d["lang"], brand="LitBuy", host=host)
    loc = _loc(key)
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
<meta property="og:locale" content="{escape(og_locale(d['lang']))}">
<meta property="og:title" content="{escape(title)}">
<meta property="og:description" content="{escape(desc)}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="https://{host}{logo}">
<meta name="twitter:card" content="summary_large_image">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
{_css_links(d)}
<link rel="icon" href="/assets/images/favicon-new.ico" type="image/x-icon">
{_hreflang()}
<style>{EXTRA_CSS}</style>
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
</head>
<body class="{escape(d['theme'])}">
{skip_link(skip_label(loc))}
"""


def _header(key: str, d: dict, page: str = "home") -> str:
    nav, cta, browse, w2c = _nav(key, d, page=page)
    top = {
        "fr": f"Conçu pour la France · estimateur officiel · pas la Belgique · <a href=\"{w2c}\" target=\"_blank\" rel=\"noopener\">{browse} →</a>",
        "es": f"Escritorio ES independiente · no copiamos 58 líneas ajenas · <a href=\"{w2c}\" target=\"_blank\" rel=\"noopener\">{browse} →</a>",
        "at": f"Für eine AT-Adresse · BMF Zoll · <a href=\"{w2c}\" target=\"_blank\" rel=\"noopener\">{browse} →</a>",
        "nl": f"Voor een NL-adres · <a href=\"{w2c}\" target=\"_blank\" rel=\"noopener\">{browse} →</a>",
        "it": f"Per un indirizzo IT · dogana · <a href=\"{w2c}\" target=\"_blank\" rel=\"noopener\">{browse} →</a>",
        "eu": f"English Europe hub · destination is a country in the estimator · <a href=\"{w2c}\" target=\"_blank\" rel=\"noopener\">{browse} →</a>",
        "now": f"Coupon hub · destination is a country in the estimator · <a href=\"{w2c}\" target=\"_blank\" rel=\"noopener\">{browse} →</a>",
    }.get(key, f"Independent desk · {escape(d['badge'])} · <a href=\"{w2c}\" target=\"_blank\" rel=\"noopener\">{browse} →</a>")
    logo = d.get("logo") or "/assets/images/litbuy-logo.png"
    return f"""<div class="topbar"><div class="container">{top}</div></div>
<header class="site-header">
  <div class="container header-inner">
    <a href="/" class="brand"><img class="brand-logo" src="{escape(logo)}" alt="LitBuy" width="160" height="36"></a>
    <nav class="nav" id="site-nav">{nav}</nav>
    <div class="header-actions">
      <a href="#catalog" class="btn btn-primary">{escape(cta)}</a>
      <a href="{REG}" target="_blank" rel="noopener sponsored" class="btn btn-outline">{escape(_reg_lab(key))}</a>
      {_locale_switcher(key, d)}
      <button class="mobile-toggle" data-mobile-toggle aria-label="{escape(ui_copy(_loc(key))['menu'])}"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="3" y1="6" x2="21" y2="6"/><line x1="3" y1="12" x2="21" y2="12"/><line x1="3" y1="18" x2="21" y2="18"/></svg></button>
    </div>
  </div>
</header>
<main id="main">
"""


def _footer(key: str, d: dict) -> str:
    u = ui_copy(_loc(key))
    t = _trust_paths(key)
    note = independence_copy(_facts(key))
    return f"""</main>
<footer class="site-footer">
  <div class="container">
    <div class="footer-grid">
      <div class="footer-brand"><a href="/" class="brand"><img class="brand-logo" src="{escape(d.get('logo') or '/assets/images/litbuy-logo.png')}" alt="LitBuy"></a>
      <p>{escape(u['foot'].format(host=d['host'], brand='LitBuy'))}</p>
      <p class="legal-note">{escape(note)}</p></div>
      <div class="footer-col"><h5>{escape(u['on_host'])}</h5><ul>
        <li><a href="/{t['help']}/">{escape(t['help_lab'])}</a></li>
        <li><a href="/{t['news']}/">{escape(t['news_lab'])}</a></li>
        <li><a href="/{t['about']}/">{escape(t['about_lab'])}</a></li>
        {''.join(f'<li><a href="{escape(h)}">{escape(l)}</a></li>' for h,l in d['keep'])}
      </ul></div>
      <div class="footer-col"><h5>{escape(u['official'])}</h5><ul>
        <li><a href="{EST}">{escape(u['freight'])}</a></li>
        <li><a href="{REG}" rel="noopener sponsored">{escape(u['register'])}</a></li>
        <li><a href="{OFFICIAL}">litbuy.com</a></li>
      </ul></div>
      <div class="footer-col"><h5>{escape(u['contact'])}</h5><ul>
        <li><a href="mailto:{escape(d['mail'])}">{escape(d['mail'])}</a></li>
        <li><a href="/privacy-policy/">{escape(u['privacy'])}</a></li>
        <li><a href="/cookie-policy/">{escape(u['cookies'])}</a></li>
      </ul></div>
    </div>
    <p class="footer-locale-cluster" style="margin:12px 0;font-size:13px;color:#94A3B8">{escape(u['desks'])}:
      <a href="https://litbuyspreadsheetnow.com/">Global</a> ·
      <a href="https://litbuyspreadsheet.eu/">Europe</a> ·
      <a href="https://litbuyspreadsheets.us/">USA</a> ·
      <a href="https://litbuyspreadsheets.ca/">Canada</a> ·
      <a href="https://litbuyspreadsheet.me.uk/">UK</a> ·
      <a href="https://litspreadsheet.fr/">France</a> ·
      <a href="https://litbuyspreadsheets.es/">España</a> ·
      <a href="https://litbuyspreadsheet.it/">Italia</a> ·
      <a href="https://litbuy.at/">Österreich</a> ·
      <a href="https://litbuyspreadsheets.nl/">Nederland</a>
    </p>
    <div class="footer-bottom"><div>© 2026 {escape(d['host'])} · {escape(u['indep'])}</div></div>
  </div>
</footer>
<script src="/assets/js/main.js?v=20261001-home"></script>
</body></html>
"""


def _catalog(key: str) -> str:
    return catalog_block(key, HOSTS[key], register_url=REG, loc_fn=_loc, cat_labels=CAT_LABELS)


def _nine(key: str) -> str:
    rows_en = [
        ("Submitted", "You paid the goods plus China domestic."),
        ("Purchasing", "LitBuy buys in the third-party shop."),
        ("Purchased", "The agent completed the China-side order."),
        ("Seller shipped", "The Chinese seller dispatched."),
        ("To warehouse", "In transit to the LitBuy warehouse."),
        ("QC / photos", "Warehouse inspection photos."),
        ("Stocked / listed", "Stored. Official Help: 90 free calendar days from stocked/listed, 120-day max."),
        ("Parcel shipped", "International SKU left China."),
        ("Delivered", "Last-mile delivered; confirm in-app."),
    ]
    if key == "at":
        h, n = "Neun Zustände (Lager)", "Offizielles Help Center 1. Okt 2026: 90 Tage gratis ab stocked/listed, höchstens 120. Labels der App bleiben oft englisch."
        rows = [
            ("Submitted", "Ware plus Inlandversand in China bezahlt."),
            ("Purchasing", "LitBuy kauft im Drittshop."),
            ("Purchased", "China-Bestellung abgeschlossen."),
            ("Seller shipped", "Der Shop hat abgeschickt."),
            ("To warehouse", "Unterwegs ins Lager."),
            ("QC / photos", "Lagerfotos."),
            ("Stocked / listed", "Eingelagert. 90 Tage gratis ab diesem Status, Höchstfrist 120."),
            ("Parcel shipped", "Internationale Linie gestartet."),
            ("Delivered", "Zugestellt."),
        ]
    elif key == "it":
        h, n = "Nove stati (magazzino)", "Help Center ufficiale 1 ott 2026: 90 giorni gratis da stocked/listed, tetto 120. Le etichette in-app restano spesso in inglese."
        rows = [
            ("Submitted", "Merce più domestico Cina pagati."),
            ("Purchasing", "LitBuy compra nello shop."),
            ("Purchased", "Ordine Cina fatto."),
            ("Seller shipped", "Lo shop ha spedito."),
            ("To warehouse", "Verso il magazzino."),
            ("QC / photos", "Foto di magazzino."),
            ("Stocked / listed", "Stoccato. 90 giorni gratis da questo stato, tetto 120."),
            ("Parcel shipped", "Linea internazionale partita."),
            ("Delivered", "Consegnato."),
        ]
    elif key == "nl":
        h, n = "Negen statussen (magazijn)", "Officieel Help Center 1 okt 2026: 90 dagen gratis vanaf stocked/listed, max 120."
        rows = [
            ("Submitted", "Product plus binnenlands China betaald."),
            ("Purchasing", "LitBuy koopt in de Chinese shop."),
            ("Purchased", "China-order geplaatst."),
            ("Seller shipped", "Verkoper heeft verzonden."),
            ("To warehouse", "Onderweg naar het magazijn."),
            ("QC / photos", "Magazijnfoto’s."),
            ("Stocked / listed", "Opgeslagen. 90 dagen gratis vanaf deze status, max 120."),
            ("Parcel shipped", "Internationale lijn vertrokken."),
            ("Delivered", "Bezorgd."),
        ]
    elif key == "fr":
        h, n = "Neuf états (entrepôt)", "Help Center officiel 1 oct. 2026 : 90 jours gratuits depuis stocked/listed, plafond 120."
        rows = [
            ("Submitted", "Marchandise + domestique Chine payés."),
            ("Purchasing", "LitBuy achète chez le vendeur."),
            ("Purchased", "Commande Chine passée."),
            ("Seller shipped", "Le vendeur a expédié."),
            ("To warehouse", "Vers l’entrepôt."),
            ("QC / photos", "Photos d’entrepôt."),
            ("Stocked / listed", "Stocké. 90 jours gratuits à partir de ce statut, plafond 120."),
            ("Parcel shipped", "Ligne internationale partie."),
            ("Delivered", "Livré."),
        ]
    elif key == "es":
        h, n = "Nueve estados (almacén)", "Help Center oficial 1 oct 2026: 90 días gratis desde stocked/listed, tope 120."
        rows = [
            ("Submitted", "Producto + envío doméstico en China pagados."),
            ("Purchasing", "LitBuy compra en la tienda."),
            ("Purchased", "Pedido en China hecho."),
            ("Seller shipped", "El vendedor envió."),
            ("To warehouse", "Hacia el almacén."),
            ("QC / photos", "Fotos de almacén."),
            ("Stocked / listed", "Almacenado. 90 días gratis desde este estado, tope 120."),
            ("Parcel shipped", "Línea internacional salió."),
            ("Delivered", "Entregado."),
        ]
    else:
        h, n = "Nine states, warehouse", "Official Help Center 1 Oct 2026: 90 free calendar days from stocked/listed, 120-day max. App labels stay English."
        rows = rows_en
    body = "".join(f"<tr><td><code>{escape(a)}</code></td><td>{escape(b)}</td></tr>" for a, b in rows)
    return f"""<section class="sg-sec" id="states"><h2>{escape(h)}</h2><p class="ssub">{escape(n)}</p>
<div class="tw"><table><thead><tr><th>State</th><th></th></tr></thead><tbody>{body}</tbody></table></div></section>"""


def _vol(key: str) -> str:
    title = {
        "fr": "Poids volumétrique (pas un prix)",
        "es": "Peso volumétrico (no es un precio)",
        "at": "Volumengewicht (kein Preis)",
        "it": "Peso volumetrico (non è un prezzo)",
        "at": "Volumengewicht (kein Preis)",
        "nl": "Volumgewicht (geen prijs)",
    }.get(key, "Volumetric weight (not a price)")
    note = {
        "fr": "Géométrie seule. Les dollars sont dans l’estimateur officiel. Souvent L×W×H/8000 en kg.",
        "es": "Solo geometría. El precio está en el estimador oficial. Casi siempre L×W×H/8000 en kg.",
        "at": "Nur Geometrie. Den Preis kennt der offizielle Schätzer. Meist L×W×H/8000 in kg.",
        "it": "Solo geometria. Il prezzo sta nell’estimator ufficiale. Spesso L×W×H/8000 in kg.",
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
  <p id="vol-out" style="margin-top:12px;background:#fff8df;padding:12px 14px;border-radius:10px"></p>
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
    if(el) el.innerHTML={json.dumps(vol_js_labels(_loc(key))[0])}+' <b>'+vol+' g</b> · '+{json.dumps(vol_js_labels(_loc(key))[1])}+' <b>'+billed+' g</b> · not checkout.';
  }}
  ['vol-l','vol-w','vol-h','vol-g','vol-d'].forEach(function(id){{
    var n=document.getElementById(id); if(n) n.addEventListener(id==='vol-d'?'change':'input', sgVol);
  }});
  sgVol();
}})();
</script>
"""


def _faqs(key: str, d: dict) -> list[tuple[str, str]]:
    return long_faqs(_facts(key))


def _faq_block(key: str, d: dict) -> str:
    h = {"fr": "Questions", "es": "Preguntas", "at": "Fragen", "nl": "Vragen", "it": "Domande"}.get(key, "FAQ")
    items = []
    for i, (q, a) in enumerate(_faqs(key, d)):
        op = " open" if i == 0 else ""
        items.append(f'<details class="sg-faq"{op}><summary>{escape(q)}</summary><p>{escape(a)}</p></details>')
    return f'<section class="sg-sec" id="faq"><h2>{h}</h2>{"".join(items)}</section>'


def _keep(key: str, d: dict) -> str:
    h, note = keep_copy(_loc(key))
    links = "".join(f'<a href="{escape(href)}"><strong>{escape(lab)}</strong><span> {escape(note)}</span></a>' for href, lab in d["keep"])
    return f'<section class="sg-sec" id="kept"><h2>{escape(h)}</h2><div class="keep">{links}</div></section>'


def _lab(key: str, d: dict) -> str:
    c = lab_copy(_facts(key))
    return f"""<section class="sg-sec" id="lab"><h2>{escape(c["h2"])}</h2>
<p class="ssub">{c["ssub"]}</p>
<p><a class="btn btn-primary" href="{EST}">{escape(c["cta"])} →</a></p>
{_vol(key)}
</section>"""

def _help_meta(key: str, d: dict) -> dict:
    loc = d["locale"]
    dest = d["dest_label"]
    if key == "es":
        return {
            "title": "Ayuda: quince preguntas sobre LitBuy en España",
            "desc": "Desk ES independiente: catálogo en inglés, almacén 90/120, estimador con destino España. Lab 1 oct 2026.",
            "h1": "Ayuda y preguntas frecuentes sobre LitBuy en <em>español</em>",
            "lead": "Esta página vale para una calle española en este host. No vemos tu cuenta. Pedidos, pagos y reclamaciones solo en litbuy.com.",
            "h2": "Las quince preguntas que más se repiten",
            "ask_h": "Dónde preguntar cuando esto no basta",
            "ask": "El chat de la app oficial. Este desk no opera tu cuenta. Los cupones siguen en /litbuy-coupons/; la aduana en /aduana-correos-espana/.",
        }
    if key == "fr":
        return {
            "title": "Aide : quinze questions sur LitBuy en France",
            "desc": "Desk FR indépendant : catalogue anglais, entrepôt 90/120, estimateur vers la France. Lab 1 oct. 2026. Pas la Belgique.",
            "h1": "Aide et questions fréquentes sur LitBuy en <em>France</em>",
            "lead": "Cette page vaut pour une adresse en France sur ce host. On ne voit pas ton compte. Commandes et litiges seulement sur litbuy.com.",
            "h2": "Les quinze questions qui reviennent",
            "ask_h": "Où demander si cela ne suffit pas",
            "ask": "Le chat de l’app officielle. Ce desk n’opère pas ton compte. Coupons et avis restent sur leurs URL classées.",
        }
    if key == "it":
        return {
            "title": "Aiuto: quindici domande su LitBuy in Italia",
            "desc": "Desk IT indipendente: catalogo inglese, magazzino 90/120, estimator verso l’Italia. Lab 1 ott 2026.",
            "h1": "Aiuto: quindici domande su LitBuy in <em>Italia</em>",
            "lead": "Questa pagina vale per un indirizzo italiano su questo host. Non vediamo il tuo conto. Ordini solo su litbuy.com.",
            "h2": "Le quindici domande che tornano di più",
            "ask_h": "Dove chiedere se non basta",
            "ask": "Chat in-app ufficiale. Questo desk non opera il tuo conto. Coupon e dogana restano sulle URL già in ranking.",
        }
    if key == "at":
        land = "Österreich" if key == "at" else "Deutschland"
        return {
            "title": f"Hilfe: fünfzehn Fragen zu LitBuy in {land}",
            "desc": f"Unabhängiger Desk: englischer Katalog, Lager 90/120, Schätzer nach {land}. Lab 1. Okt 2026.",
            "h1": f"Hilfe: fünfzehn Fragen zu LitBuy in <em>{land}</em>",
            "lead": f"Diese Seite gilt für eine Straße in {land} auf diesem Host. Wir sehen dein Konto nicht. Bestellungen nur auf litbuy.com.",
            "h2": "Die fünfzehn häufigsten Fragen",
            "ask_h": "Wohin, wenn das nicht reicht",
            "ask": "Offizieller App-Chat. Dieser Desk führt dein Konto nicht. Coupons bleiben im Coupon-Artikel.",
        }
    if key == "nl":
        return {
            "title": "Hulp: vijftien vragen over LitBuy in Nederland",
            "desc": "Onafhankelijke NL-desk: Engelse catalogus, magazijn 90/120, estimator naar Nederland. Lab 1 okt 2026.",
            "h1": "Hulp: vijftien vragen over LitBuy in <em>Nederland</em>",
            "lead": "Deze pagina geldt voor een Nederlands adres op deze host. We zien je account niet. Orders alleen op litbuy.com.",
            "h2": "De vijftien vragen die het vaakst terugkomen",
            "ask_h": "Waar vragen als dit niet volstaat",
            "ask": "De chat in de officiële app. Deze desk voert je account niet. Coupons blijven op de coupon-URL.",
        }
    if key == "now":
        return {
            "title": "Help: fifteen questions on this LitBuy coupon hub",
            "desc": "Independent English hub. Destination is a country in the official estimator, not this hostname. Lab 1 Oct 2026.",
            "h1": "Help: fifteen questions on this <em>coupon hub</em>",
            "lead": "This hostname is not a destination. Dated html articles stay. Orders run only on litbuy.com.",
            "h2": "The fifteen questions that come back most",
            "ask_h": "Where to ask when this is not enough",
            "ask": "Official in-app chat. This desk does not run your account. Coupon html files on this host stay put.",
        }
    return {
        "title": f"Help: fifteen questions about LitBuy in {loc}",
        "desc": f"Independent desk: English catalogue, 90/120 warehouse, estimator to {dest}. Lab 1 Oct 2026.",
        "h1": f"Help: fifteen questions about LitBuy in <em>{escape(loc)}</em>",
        "lead": f"This page is for a {dest} address on this host. We cannot see your account. Orders and claims run only on litbuy.com.",
        "h2": "The fifteen questions that come back most",
        "ask_h": "Where to ask when this is not enough",
        "ask": "Official in-app chat. This desk does not operate your LitBuy account. Ranked coupon and customs URLs stay on this host.",
    }


def _news_meta(key: str, d: dict) -> dict:
    loc = d["locale"]
    dest = d["dest_label"]
    if key == "es":
        return {
            "title": "Novedades: lo que hemos comprobado en LitBuy para España",
            "desc": "Notas con fecha de este desk ES. No copiamos las 58 líneas de otro agente. Lab 1 oct 2026.",
            "h1": "Qué hemos comprobado en la plataforma, <em>con fecha</em>",
            "lead": "Cada bloque es una medición o una captura de este host, no un recorte de hipobuy.es.",
            "how_h": "Cómo comprobamos las cosas",
            "how": "Homepage y /api/products/ de este host, el estimador oficial con destino España, y las URL que ya posicionan. No inventamos un recuento de líneas ajenas.",
        }
    if key == "fr":
        return {
            "title": "Actualités : ce que nous avons vérifié sur LitBuy pour la France",
            "desc": "Notes datées du desk FR. Destination France, pas la Belgique. Lab 1 oct. 2026.",
            "h1": "Ce que nous avons vérifié sur la plateforme, <em>avec date</em>",
            "lead": "Chaque bloc est une mesure sur ce host, pas une copie d’un autre agent.",
            "how_h": "Comment on vérifie",
            "how": "Accueil et /api/products/ de ce host, estimateur officiel vers la France, URL déjà classées. Pas de copie des lignes ES d’un autre agent.",
        }
    if key == "at":
        land = "Österreich" if key == "at" else "Deutschland"
        return {
            "title": f"Neuigkeiten: was wir an LitBuy für {land} geprüft haben",
            "desc": f"Datierte Notizen dieses Desks. Schätzer nach {land}. Lab 1. Okt 2026.",
            "h1": "Was wir auf der Plattform geprüft haben, <em>mit Datum</em>",
            "lead": "Jeder Block ist eine Messung auf diesem Host, kein fremder Linien-Schnappschuss.",
            "how_h": "Wie wir messen",
            "how": f"Startseite und /api/products/ dieses Hosts, offizieller Schätzer nach {land}, bereits rankende URLs.",
        }
    if key == "nl":
        return {
            "title": "Nieuws: wat we op LitBuy voor Nederland hebben nagemeten",
            "desc": "Gedateerde notities van deze NL-desk. Lab 1 oct 2026.",
            "h1": "Wat we op het platform hebben nagemeten, <em>met datum</em>",
            "lead": "Elk blok is een meting op deze host, geen kopie van een andere agent.",
            "how_h": "Hoe we meten",
            "how": "Homepage en /api/products/ van deze host, officiële estimator naar Nederland, URL’s die al ranken.",
        }
    if key == "now":
        return {
            "title": "News: what we checked on this LitBuy coupon hub",
            "desc": "Dated notes. This hostname is not a destination. Html articles stay. Lab 1 Oct 2026.",
            "h1": "What we checked on this hub, <em>with dates</em>",
            "lead": "Each block is a measurement on this host. Spain-only line counts stay off this page.",
            "how_h": "How we measure",
            "how": "Homepage and /api/products/ on this host, official estimator with a country code, existing html articles left in place.",
        }
    return {
        "title": f"News: what we checked on LitBuy for {loc}",
        "desc": f"Dated notes on this independent desk. Estimator destination {dest}. Lab 1 Oct 2026.",
        "h1": "What we checked on the platform, <em>with dates</em>",
        "lead": "Each block is a measurement on this host, not another agent’s freight snapshot.",
        "how_h": "How we measure",
        "how": f"Homepage and /api/products/ on this host, official estimator to {dest}, ranked URLs left in place.",
    }


def _news_items(key: str, d: dict) -> list[tuple[str, str]]:
    dest = d["dest_label"]
    api = f"https://{d['host']}/api/products/"
    if key == "es":
        return [
            ("Check 1 · 1 oct 2026 · catálogo en esta portada",
             f"Restauramos el catálogo en / vía {api}. Clave inglesa sneakers devuelve fichas; zapatillas suele dar 0."),
            ("Check 2 · el conmutador de moneda no convierte",
             "En el sitio oficial el símbolo puede pasar a EUR y las cifras seguir en dólares. Lee el número, no solo el símbolo."),
            ("Check 3 · el estimador pide España, no este TLD",
             "Abrimos shipping-estimate con destino España. No copiamos las 58 líneas de hipobuy.es ni un precio de otro agente."),
            ("Check 4 · almacén 90/120",
             "Help Center oficial 1 oct 2026: 90 días gratis desde stocked/listed, tope 120."),
            ("Check 5 · URLs que ya posicionan",
             " /aduana-correos-espana/ y /litbuy-coupons/ se conservan. Esta novedad no las pisa."),
            ("Check 6 · 1 oct 2026 · SPA del estimador y página Sobre",
             "El HTML crudo de shipping-estimate era ~2 KB. El navegador del 1 oct 2026 sí renderizó el formulario; la captura está en /media/. Sobre nosotros es página propia, no un ancla."),
        ]
    if key == "fr":
        return [
            ("Check 1 · 1 oct. 2026 · catalogue sur cette accueil",
             f"Catalogue restauré sur / via {api}. La clé sneakers remplit la grille ; baskets donne souvent 0."),
            ("Check 2 · le sélecteur de devise ne convertit pas",
             "Le symbole peut passer en EUR et le chiffre rester en dollars. Lis le nombre."),
            ("Check 3 · l’estimateur veut la France",
             "Destination France, pas la Belgique, pas un TLD. Pas de copie des lignes ES d’un autre agent."),
            ("Check 4 · entrepôt 90/120",
             "Help Center officiel 1 oct. 2026 : 90 jours gratuits depuis stocked/listed, plafond 120."),
            ("Check 5 · URL déjà classées",
             "/litbuy-coupons/ et /litbuy-review/ restent. Cette page actualités ne les écrase pas."),
            ("Check 6 · 1 oct. 2026 · SPA estimateur et page À propos",
             "Le HTML brut de shipping-estimate faisait ~2 ko. Le navigateur du 1 oct. 2026 a rendu le formulaire ; capture dans /media/. À propos est une page, pas une ancre."),
        ]
    if key == "at":
        land = "Österreich" if key == "at" else "Deutschland"
        return [
            (f"Check 1 · 1. Okt 2026 · Katalog auf dieser Startseite",
             f"Katalog wieder auf / über {api}. Englisch sneakers füllt das Raster; Turnschuhe oft 0."),
            ("Check 2 · Währungsschalter rechnet nicht um",
             "Das Symbol kann auf EUR springen, die Ziffer Dollar bleiben. Die Zahl lesen."),
            (f"Check 3 · Schätzer nach {land}",
             f"Offizieller Schätzer mit Ziel {land}. Keine 58 ES-Linien eines anderen Agenten."),
            ("Check 4 · Lager 90/120",
             "Offizielles Help Center 1. Okt 2026: 90 Tage gratis ab stocked/listed, höchstens 120."),
            ("Check 5 · bereits rankende URLs",
             "Coupon- und Spreadsheet-Artikel bleiben. Diese Neuigkeiten-Seite überschreibt sie nicht."),
            ("Check 6 · 1. Okt 2026 · SPA-Schätzer und Über uns",
             "Roh-HTML von shipping-estimate war ~2 KB. Der Browser am 1 Oct 2026 hat das Formular gerendert; Aufnahme unter /media/. Über uns ist eine eigene Seite."),
        ]
    if key == "nl":
        return [
            ("Check 1 · 1 oct 2026 · catalogus op deze homepage",
             f"Catalogus terug op / via {api}. Engels sneakers vult het raster; lokale woorden vaak 0."),
            ("Check 2 · valutaswitcher rekent niet om",
             "Het symbool kan EUR worden terwijl het cijfer dollar blijft. Lees het getal."),
            ("Check 3 · estimator naar Nederland",
             "Officiële estimator met bestemming Nederland. Geen ES-lijnen van een andere agent."),
            ("Check 4 · magazijn 90/120",
             "Officieel Help Center 1 okt 2026: 90 dagen gratis vanaf stocked/listed, max 120."),
            ("Check 5 · URL’s die al ranken",
             "Coupon- en BTW-artikelen blijven. Deze nieuwspagina overschrijft ze niet."),
            ("Check 6 · 1 oct 2026 · SPA-estimator en Over ons",
             "Ruwe HTML van shipping-estimate was ~2 KB. De browser op 1 oct 2026 renderde het formulier; opname in /media/. Over ons is een eigen pagina."),
        ]
    if key == "now":
        return [
            ("Check 1 · 1 Oct 2026 · catalogue on this hub homepage",
             f"Catalogue restored on / via {api}. English keys fill the grid. Dated html files stay."),
            ("Check 2 · currency switcher does not convert",
             "Official site: the symbol can change while the digits stay dollars."),
            ("Check 3 · this hostname is not a destination",
             "Open the official estimator with a country code. Spain-only line counts stay off this hub."),
            ("Check 4 · warehouse 90/120",
             "Official Help Center 1 Oct 2026: 90 free days from stocked/listed, 120-day max. Not a Packing Center 100-day figure."),
            ("Check 5 · html articles kept",
             "Coupon, Reddit, legit and spreadsheet html files were not overwritten."),
            ("Check 6 · 1 Oct 2026 · SPA estimator and About page",
             "Raw HTML of shipping-estimate was ~2 KB. The 1 Oct 2026 browser rendered the form; capture in /media/. /who-we-are/ is its own page, not an anchor."),
        ]
    extra = {
        "us": "Ranked de-minimis, USPS times and coupons URLs stay.",
        "au": "The ranked GST article at /gst-hst-import-canada/ stays.",
        "ca": "The ranked CBSA article at /cbsa-import-canada/ stays.",
        "uk": "The UK VAT article stays.",
    }.get(key, "Ranked coupon and guide URLs stay.")
    return [
        ("Check 1 · 1 Oct 2026 · catalogue on this homepage",
         f"Catalogue restored on / via {api}. English key sneakers fills the grid; local words often return zero."),
        ("Check 2 · currency switcher does not convert",
         "On the official site the symbol can change to a local currency while the digits stay dollars. Read the number."),
        (f"Check 3 · estimator destination {dest}",
         f"Open the official freight estimate with {dest}. We do not paste another agent’s line count onto this desk."),
        ("Check 4 · warehouse 90/120",
         "Official Help Center 1 Oct 2026: 90 free days from stocked/listed, 120-day max. Not a Packing Center 100-day figure."),
        ("Check 5 · ranked URLs kept", extra),
        ("Check 6 · 1 Oct 2026 · SPA estimator and About page",
         "Raw HTML of shipping-estimate was ~2 KB. The 1 Oct 2026 browser rendered the form; capture lives under /media/. /who-we-are/ is its own page."),
    ]


def build_help(key: str) -> str:
    d = HOSTS[key]
    t = _trust_paths(key)
    m = _help_meta(key, d)
    if INVITE in m["title"] or COUPON in m["title"]:
        raise RuntimeError(f"{key} help: code in title")
    faqs = _faqs(key, d)
    html = _chrome_head(key, d, m["title"], m["desc"], path=f"/{t['help']}/")
    html = inject_jsonld(
        html,
        faq_ld(d["lang"], faqs),
        breadcrumb_ld(
            [
                ("Home", f"https://{d['host']}/"),
                (t["help_lab"], f"https://{d['host']}/{t['help']}/"),
            ]
        ),
    )
    html += _header(key, d, page="help")
    items = []
    for i, (q, a) in enumerate(faqs):
        op = " open" if i == 0 else ""
        items.append(f'<details class="sg-faq"{op}><summary>{escape(q)}</summary><p>{escape(a)}</p></details>')
    html += f"""<section class="sg-hero">
  <div class="hbg">Lab {DATE} · {escape(t['help_lab'])}</div>
  <h1>{m['h1']}</h1>
  <p class="hsub">{escape(m['lead'])}</p>
  <p class="eu-badge">{escape(d['badge'])}</p>
</section>
<section class="sg-sec" id="faq"><h2>{escape(m['h2'])}</h2>{''.join(items)}</section>
<section class="sg-sec"><h2>{escape(m['ask_h'])}</h2><p class="ssub">{escape(m['ask'])}</p>
<p><a class="btn btn-primary" href="{REG}" target="_blank" rel="noopener sponsored">{escape({"fr":"S’inscrire","es":"Registrarse","at":"Registrieren","nl":"Registreren","it":"Registrati"}.get(key,"Register"))}</a>
<a class="btn btn-outline" href="/">← /</a></p></section>
"""
    html += _footer(key, d)
    return html


def build_news(key: str) -> str:
    d = HOSTS[key]
    t = _trust_paths(key)
    m = _news_meta(key, d)
    if INVITE in m["title"] or COUPON in m["title"]:
        raise RuntimeError(f"{key} news: code in title")
    news_items = _news_items(key, d)
    html = _chrome_head(key, d, m["title"], m["desc"], path=f"/{t['news']}/")
    html = inject_jsonld(
        html,
        itemlist_ld(url=f"https://{d['host']}/{t['news']}/", name=m["title"], items=news_items),
        breadcrumb_ld(
            [
                ("Home", f"https://{d['host']}/"),
                (t["news_lab"], f"https://{d['host']}/{t['news']}/"),
            ]
        ),
    )
    html += _header(key, d, page="news")
    blocks = []
    for h, p in news_items:
        blocks.append(f'<article class="sg-sec"><h2>{escape(h)}</h2><p class="ssub">{escape(p)}</p></article>')
    html += f"""<section class="sg-hero">
  <div class="hbg">Lab {DATE} · {escape(t['news_lab'])}</div>
  <h1>{m['h1']}</h1>
  <p class="hsub">{escape(m['lead'])}</p>
  <p class="eu-badge">{escape(d['badge'])}</p>
</section>
{''.join(blocks)}
<section class="sg-sec"><h2>{escape(m['how_h'])}</h2><p class="ssub">{escape(m['how'])}</p>
<p><a class="btn btn-outline" href="/{_trust_paths(key)['help']}/">{escape(t['help_lab'])}</a>
<a class="btn btn-outline" href="/">← /</a></p></section>
"""
    html += _footer(key, d)
    return html


def _prose_agent(key: str, d: dict) -> str:
    p = _trust_pack(key, d)
    t = _trust_paths(key)
    return f"""<section class="sg-sec" id="agent"><div class="sg-split">
  <div class="sg-prose">
    <h2>{escape(p['agent_h'])}</h2>
    <p class="lead">{escape(p['agent_lead'])}</p>
    <p>{escape(p['agent_p'])}</p>
    <p><a class="btn btn-primary" href="#catalog">{escape(p['agent_btn'])}</a>
    <a class="btn btn-outline" href="/{t['about']}/">{escape(t['about_lab'])}</a></p>
  </div>
  <figure class="shot">
    <img src="/media/official-home-20261001.jpg" alt="{escape(p['agent_cap'])}" width="1400" height="1069" loading="lazy" decoding="async">
    <figcaption>{escape(p['agent_cap'])}</figcaption>
  </figure>
</div></section>
"""


def _prose_sheet(key: str, d: dict) -> str:
    p = _trust_pack(key, d)
    return f"""<section class="sg-sec" id="sheet-explain"><div class="sg-prose">
  <h2>{escape(p['sheet_h'])}</h2>
  <p class="lead">{escape(p['sheet_lead'])}</p>
  <p>{escape(p['sheet_p'])}</p>
  <p><a class="btn btn-outline" href="#catalog">{escape(p['sheet_btn'])}</a>
  <a class="btn btn-outline" href="{W2C}" target="_blank" rel="noopener">w2clinks</a></p>
</div></section>
"""


def _cat_wall(key: str, d: dict) -> str:
    p = _trust_pack(key, d)
    labels = CAT_LABELS[_loc(key)]
    tiles = []
    for slug, fn in CAT_WALL:
        lab = labels[slug]
        tiles.append(
            f'<a class="sg-cat" href="#catalog" data-q="{escape(slug)}">'
            f'<img src="/img/cat/{escape(fn)}" alt="{escape(lab)} · {escape(slug)}" width="560" height="560" loading="lazy" decoding="async">'
            f'<div class="b"><strong>{escape(lab)}</strong><span>{escape(slug)}</span></div></a>'
        )
    return f"""<section class="sg-sec" id="cat-wall">
  <h2>{escape(p['wall_h'])}</h2>
  <p class="ssub">{escape(p['wall_lead'])}</p>
  <div class="sg-cats">{''.join(tiles)}</div>
</section>
"""


def _prose_restricted(key: str, d: dict) -> str:
    p = _trust_pack(key, d)
    t = _trust_paths(key)
    return f"""<section class="sg-sec" id="restricted"><div class="sg-split">
  <div class="sg-prose">
    <h2>{escape(p['rest_h'])}</h2>
    <p class="lead">{escape(p['rest_lead'])}</p>
    <p>{escape(p['rest_p'])}</p>
    <p><a class="btn btn-outline" href="/{t['help']}/">{escape(p['rest_btn'])}</a></p>
  </div>
  <figure class="shot">
    <img src="/media/help-restricted-20261001.jpg" alt="{escape(p['rest_cap'])}" width="1400" height="1166" loading="lazy" decoding="async">
    <figcaption>{escape(p['rest_cap'])}</figcaption>
  </figure>
</div></section>
"""


def _shots(key: str, d: dict) -> str:
    p = _trust_pack(key, d)
    return f"""<section class="sg-sec" id="shots">
  <h2>{escape(p['shots_h'])}</h2>
  <p class="ssub">{escape(p['shots_lead'])}</p>
  <figure class="shot">
    <img src="/media/estimator-20261001.jpg" alt="{escape(p['shot_est_cap'])}" width="1400" height="1069" loading="lazy" decoding="async">
    <figcaption>{escape(p['shot_est_cap'])}</figcaption>
  </figure>
</section>
"""


def build_about(key: str) -> str:
    d = HOSTS[key]
    t = _trust_paths(key)
    p = _trust_pack(key, d)
    if INVITE in p["about_title"] or COUPON in p["about_title"]:
        raise RuntimeError(f"{key} about: code in title")
    html = _chrome_head(key, d, p["about_title"], p["about_desc"], path=f"/{t['about']}/")
    html = inject_jsonld(
        html,
        organization_ld(
            name=f"{d['host']} independent desk",
            url=f"https://{d['host']}/",
            email=d["mail"],
            lang=d["lang"],
            desc=p["about_desc"],
        ),
        breadcrumb_ld(
            [
                ("Home", f"https://{d['host']}/"),
                (t["about_lab"], f"https://{d['host']}/{t['about']}/"),
            ]
        ),
    )
    html += _header(key, d, page="about")
    html += f"""<section class="sg-hero">
  <div class="hbg">Lab {DATE} · {escape(t['about_lab'])}</div>
  <h1>{p['about_h1']}</h1>
  <p class="hsub">{p['about_lead']}</p>
  <p class="eu-badge">{escape(d['badge'])}</p>
</section>
<article class="sg-sec sg-about">
  <h2>{escape(p['how_h'])}</h2>
  <h3>{escape(p['src_h'])}</h3>
  <p>{escape(p['src_p'])}</p>
  <h3>{escape(p['why_h'])}</h3>
  <p>{escape(p['why_p'])}</p>
  <h3>{escape(p['inv_h'])}</h3>
  <p>{escape(p['inv_p'])}</p>
  <h2>{escape(p['not_h'])}</h2>
  <p>{escape(p['not_p'])}</p>
  <h2>{escape(p['co_h'])}</h2>
  <p>{escape(p['co_p'])}</p>
  <p>{escape(p['legal'])}</p>
  <p><a class="btn btn-outline" href="/{t['help']}/">{escape(t['help_lab'])}</a>
  <a class="btn btn-outline" href="/{t['news']}/">{escape(t['news_lab'])}</a>
  <a class="btn btn-outline" href="/">← /</a>
  <a class="btn btn-primary" href="{REG}" target="_blank" rel="noopener sponsored">{escape({"fr":"S’inscrire","es":"Registrarse","at":"Registrieren","nl":"Registreren","it":"Registrati"}.get(key,"Register"))}</a></p>
</article>
"""
    html += _footer(key, d)
    return html


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
    <a class="btn btn-primary" href="#catalog">{escape({"fr":"Catalogue","es":"Catálogo","at":"Katalog","nl":"Catalogus","it":"Catalogo"}.get(key,"Catalogue"))}</a>
    <a class="btn btn-outline" href="{EST}">{escape({"fr":"Estimateur","es":"Estimador","at":"Schätzer","nl":"Estimator","it":"Estimatore"}.get(key,"Estimator"))}</a>
    <a class="btn btn-outline" href="{REG}" target="_blank" rel="noopener sponsored">{escape({"fr":"S’inscrire","es":"Registrarse","at":"Registrieren","nl":"Registreren","it":"Registrati"}.get(key,"Register"))}</a>
  </div>
</section>
"""
    html += _prose_agent(key, d)
    html += _prose_sheet(key, d)
    html += _cat_wall(key, d)
    html += _catalog(key)
    html += _nine(key)
    html += _prose_restricted(key, d)
    html += _shots(key, d)
    html += _lab(key, d)
    html += _keep(key, d)
    html += _faq_block(key, d)
    html += _footer(key, d)
    return html


def _wc(html: str) -> int:
    return len(re.findall(r"[A-Za-zÀ-ÿ]{3,}", html))


def _validate() -> None:
    for key, d in HOSTS.items():
        html = build_home(key)
        title = re.search(r"<title>(.*?)</title>", html, flags=re.S).group(1)
        if INVITE in html or COUPON in html:
            raise SystemExit(f"{key}: invite/coupon leaked into generated HTML")
        if "Georgia" in html or "gsc-editor-notes" in html or "impressions on a template" in html:
            raise SystemExit(f"{key}: junk/Georgia leftover")
        if "#00C853" in html:
            raise SystemExit(f"{key}: HipoBuy green leaked")
        if "90" not in html or "120" not in html:
            raise SystemExit(f"{key}: missing 90/120 storage")
        if "Packing Center" in html:
            raise SystemExit(f"{key}: SugarGoo packing-center leaked")
        for tok in (
            'id="catalog"',
            'id="states"',
            'id="vol-calc"',
            'id="faq"',
            'id="agent"',
            'id="sheet-explain"',
            'id="restricted"',
            'id="cat-wall"',
            'id="shots"',
            "style.css",
            "/api/products/",
            "/img/cat/sneakers.jpg",
            "/media/estimator-20261001.jpg",
            "/media/official-home-20261001.jpg",
            "/media/help-restricted-20261001.jpg",
        ):
            if tok not in html:
                raise SystemExit(f"{key}: missing {tok}")
        ccy = currency_for(key, d)
        if f'var FX_CCY="{ccy}"' not in html or "FX_RATE" not in html:
            raise SystemExit(f"{key}: missing local FX {ccy}")
        if "p.textContent=(it.currency||'')+' '+(it.price" in html:
            raise SystemExit(f"{key}: raw CNY catalogue concat")
        for e in validate_desk(html, _facts(key), page="home"):
            raise SystemExit(f"{key}/home template: {e}")
        ncat = len(re.findall(r"class=\"sg-cat\"", html))
        if ncat != 16:
            raise SystemExit(f"{key}: cat wall {ncat}")
        nfaq = len(re.findall(r"class=\"sg-faq\"", html))
        if nfaq < 15:
            raise SystemExit(f"{key}: faq {nfaq}")
        if key == "now" and ("58 líneas" in html or "ES AIR" in html):
            raise SystemExit("now.com copied Spain lines")
        if key == "fr" and ("Belgique" in title or "Belgium" in title or "France / BE" in html):
            raise SystemExit("fr title became Belgium")
        if "locale-switcher" not in html:
            raise SystemExit(f"{key}: missing locale-switcher")
        t = _trust_paths(key)
        if f"/{t['help']}/" not in html or f"/{t['news']}/" not in html or f"/{t['about']}/" not in html:
            raise SystemExit(f"{key}: home missing help/news/about nav")
        n = _wc(html)
        print(f"{'OK' if n>=600 else 'SHORT':5} {key}/home words={n} faq={nfaq} cats={ncat} {title[:56]}")
        if n < 500:
            raise SystemExit(f"{key} too short")

        help_html = build_help(key)
        news_html = build_news(key)
        for label, page in (("help", help_html), ("news", news_html)):
            pt = re.search(r"<title>(.*?)</title>", page, flags=re.S).group(1)
            if INVITE in pt or COUPON in pt:
                raise SystemExit(f"{key} {label}: code in title")
            if "Georgia" in page or "#00C853" in page or "gsc-editor-notes" in page:
                raise SystemExit(f"{key} {label}: junk")
            if "style.css" not in page or "locale-switcher" not in page:
                raise SystemExit(f"{key} {label}: chrome")
            if key == "now" and ("58 líneas" in page or "ES AIR" in page):
                raise SystemExit("now.com help/news copied Spain lines")
            if key == "fr" and ("Belgique" in pt or "Belgium" in pt or "France / BE" in page):
                raise SystemExit("fr help/news became Belgium")
        for e in validate_desk(help_html, _facts(key), page="help"):
            raise SystemExit(f"{key}/help template: {e}")
        hf = len(re.findall(r"class=\"sg-faq\"", help_html))
        if hf < 15:
            raise SystemExit(f"{key} help faq {hf}")
        hn = len(re.findall(r"<h2>", news_html))
        if hn < 6:
            raise SystemExit(f"{key} news h2 {hn}")
        for e in validate_desk(news_html, _facts(key), page="news"):
            raise SystemExit(f"{key}/news template: {e}")
        print(f"OK    {key}/help words={_wc(help_html)} faq={hf}")
        print(f"OK    {key}/news words={_wc(news_html)} h2={hn}")

        about_html = build_about(key)
        at = re.search(r"<title>(.*?)</title>", about_html, flags=re.S).group(1)
        if INVITE in at or COUPON in at:
            raise SystemExit(f"{key} about: code in title")
        if "Georgia" in about_html or "#00C853" in about_html or "gsc-editor-notes" in about_html:
            raise SystemExit(f"{key} about: junk")
        if "style.css" not in about_html or "locale-switcher" not in about_html:
            raise SystemExit(f"{key} about: chrome")
        if f"/{t['about']}/" not in about_html:
            raise SystemExit(f"{key} about: canonical slug")
        if key == "now" and ("58 líneas" in about_html or "ES AIR" in about_html):
            raise SystemExit("now.com about copied Spain lines")
        if key == "fr" and ("Belgique" in at or "Belgium" in at or "France / BE" in about_html):
            raise SystemExit("fr about became Belgium")
        if _wc(about_html) < 280:
            raise SystemExit(f"{key} about too short")
        for e in validate_desk(about_html, _facts(key), page="about"):
            raise SystemExit(f"{key}/about template: {e}")
        print(f"OK    {key}/about words={_wc(about_html)} {at[:56]}")


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


ORDER = ["at", "ca", "it", "eu", "es", "fr", "us", "nl", "uk", "now"]


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


def _overlay_files(key: str) -> list[tuple[Path, str]]:
    d = HOSTS[key]
    t = _trust_paths(key)
    host_root = ROOT / "sites" / d["host"] / "overlay"
    return [
        (host_root / "index.html", build_home(key)),
        (host_root / t["help"] / "index.html", build_help(key)),
        (host_root / t["news"] / "index.html", build_news(key)),
        (host_root / t["about"] / "index.html", build_about(key)),
    ]


def _sitemap_insert(client, host: str, slugs: list[str]) -> None:
    path = f"/www/wwwroot/{host}/sitemap.xml"
    raw = _run(client, f"python3 -c \"print(open({path!r}).read() if __import__('os').path.isfile({path!r}) else '')\"")
    if "</urlset>" not in raw:
        print("skip sitemap", host)
        return
    added = 0
    chunk = raw
    for slug in slugs:
        loc = f"https://{host}/{slug.strip('/')}/"
        if loc in chunk:
            continue
        block = (
            "  <url>\n"
            f"    <loc>{loc}</loc>\n"
            "    <lastmod>2026-10-01</lastmod>\n"
            "    <changefreq>weekly</changefreq>\n"
            "    <priority>0.7</priority>\n"
            "  </url>\n"
        )
        chunk = chunk.replace("</urlset>", block + "</urlset>", 1)
        added += 1
    if not added:
        print("sitemap ok", host)
        return
    sftp = client.open_sftp()
    bak = f"/www/backup/litbuy-sitemap-{host}-20260930.xml"
    _run(client, f"cp -a '{path}' '{bak}'")
    with sftp.open(path, "w") as fh:
        fh.write(chunk)
    sftp.close()
    print("sitemap +", added, host)


def _fix_api_nginx(client, keys: list[str]) -> None:
    """Route /api/{name}/ to index.php so the homepage catalogue works."""
    old = """    location /api/ {
        try_files $uri =404;
        add_header X-Robots-Tag "noindex, nofollow" always;
    }
"""
    new = """    location /api/ {
        rewrite ^/api/([^/]+)/?$ /api/$1/index.php last;
        add_header X-Robots-Tag "noindex, nofollow" always;
    }
"""
    changed = 0
    basedir = 0
    for key in keys:
        host = HOSTS[key]["host"]
        path = f"/www/server/panel/vhost/nginx/{host}.conf"
        raw = _run(client, f"cat '{path}'")
        if "rewrite ^/api/([^/]+)/?$ /api/$1/index.php last" in raw:
            print("ok", host, "api rewrite")
        elif old not in raw:
            print("skip", host, "api block mismatch")
        else:
            bak = f"/www/backup/litbuy-nginx-{host}.conf"
            _run(client, f"cp -a '{path}' '{bak}'")
            sftp = client.open_sftp()
            with sftp.open(path, "w") as fh:
                fh.write(raw.replace(old, new, 1))
            sftp.close()
            print("PATCH", path)
            changed += 1
        ini = f"/www/wwwroot/{host}/.user.ini"
        want = f"open_basedir=/www/wwwroot/{host}/:/tmp/\n"
        cur = _run(client, f"python3 -c \"import os; p={ini!r}; print(open(p).read() if os.path.isfile(p) else '')\"")
        if f"/www/wwwroot/{host}/" in cur and "open_basedir" in cur:
            print("ok", host, "open_basedir")
        else:
            sftp = client.open_sftp()
            with sftp.open(ini, "w") as fh:
                fh.write(want)
            sftp.close()
            print("PATCH", ini)
            basedir += 1
    if changed:
        print(_run(client, "nginx -t && nginx -s reload"))
    if basedir:
        print(_run(client, "/etc/init.d/php-fpm-74 reload || true"))


SHARED = ROOT / "sites" / "litbuy-shared"


def _put_assets(client, sftp, host: str) -> None:
    """Copy dated official shots + 16-category wall onto this wwwroot only (new dirs)."""
    media_local = SHARED / "media"
    cat_local = SHARED / "img" / "cat"
    _run(client, f"mkdir -p '/www/wwwroot/{host}/media' '/www/wwwroot/{host}/img/cat'")
    for src in sorted(media_local.glob("*.jpg")):
        remote = f"/www/wwwroot/{host}/media/{src.name}"
        sftp.put(str(src), remote)
        print("PUT", remote, "bytes", src.stat().st_size)
    for src in sorted(cat_local.glob("*.jpg")):
        remote = f"/www/wwwroot/{host}/img/cat/{src.name}"
        sftp.put(str(src), remote)
        print("PUT", remote, "bytes", src.stat().st_size)
    _run(
        client,
        f"chown -R www:www '/www/wwwroot/{host}/media' '/www/wwwroot/{host}/img' "
        f"&& find '/www/wwwroot/{host}/media' '/www/wwwroot/{host}/img' -type f -exec chmod 644 {{}} +",
    )


def main() -> None:
    _validate()
    put_keys = _only()
    for key in ORDER:
        for dest, html in _overlay_files(key):
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_text(html, encoding="utf-8")
            print("wrote", dest, dest.stat().st_size)
    if "--dry" in sys.argv:
        print("dry-run ok")
        return
    client = _connect()
    sftp = client.open_sftp()
    stamp = time.strftime("%Y%m%d-%H%M%S")
    bak = f"/www/backup/litbuy-trust-{stamp}"
    print(_run(client, f"mkdir -p '{bak}'"))
    uploaded = []
    for key in put_keys:
        d = HOSTS[key]
        t = _trust_paths(key)
        mapping = [
            (ROOT / "sites" / d["host"] / "overlay" / "index.html", f"/www/wwwroot/{d['host']}/index.html"),
            (
                ROOT / "sites" / d["host"] / "overlay" / t["help"] / "index.html",
                f"/www/wwwroot/{d['host']}/{t['help']}/index.html",
            ),
            (
                ROOT / "sites" / d["host"] / "overlay" / t["news"] / "index.html",
                f"/www/wwwroot/{d['host']}/{t['news']}/index.html",
            ),
            (
                ROOT / "sites" / d["host"] / "overlay" / t["about"] / "index.html",
                f"/www/wwwroot/{d['host']}/{t['about']}/index.html",
            ),
        ]
        for local, remote in mapping:
            rdir = remote.rsplit("/", 1)[0]
            _run(client, f"mkdir -p '{rdir}'")
            # never clobber a pre-existing unique dest directory's other files; only write index.html
            _run(client, f"test -f '{remote}' && cp -a '{remote}' '{bak}/{d['host']}-{remote.strip('/').replace('/', '_')}' || true")
            sftp.put(str(local), remote)
            uploaded.append(remote)
            print("PUT", remote, "bytes", local.stat().st_size)
        _put_assets(client, sftp, d["host"])
        _sitemap_insert(client, d["host"], [t["help"], t["news"], t["about"]])
    if uploaded:
        _run(
            client,
            "chown www:www "
            + " ".join(f"'{p}'" for p in uploaded)
            + " && chmod 644 "
            + " ".join(f"'{p}'" for p in uploaded),
        )
    print("backup", bak, "put", ",".join(put_keys))
    _fix_api_nginx(client, put_keys)
    sftp.close()
    client.close()


if __name__ == "__main__":
    main()
