#!/usr/bin/env python3
"""Restore SugarGoo country-desk homepages in original CMS chrome.

Puts catalogue on /, Inter + existing sugargoo-theme.css (not Georgia, not HipoBuy green).
Does not overwrite coupons / GST / CBSA / de-minimis / now.com html articles.
Adds independent Help/News/About pages (local slugs, same CMS chrome).
Homepage editorial: agent is not a shop, spreadsheet is not Excel, Restricted items, 16-cat wall.
Dated official SPA screenshots under /media/ (freight-estimate is no longer a 2 KB shell).
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

_TOOLS = Path(__file__).resolve().parent
if str(_TOOLS) not in sys.path:
    sys.path.insert(0, str(_TOOLS))
from desk_fx import EXTRA_CSS_FX, catalog_block, currency_for, ui_copy
from sugargoo_desk_trust import CAT_LABELS, CAT_WALL, loc as _loc, pack as _trust_pack

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
""" + EXTRA_CSS_FX


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
    u = ui_copy(_loc(key))
    rows = [
        (u["en_group"], [
            ("now", "sugargoospreadsheetnow.com", "English (Global)"),
            ("us", "sugargoospreadsheets.us", "English (USA)"),
            ("uk", "sugargoospreadsheets.uk", "English (UK)"),
            ("ca", "sugargoospreadsheets2026.ca", "English (Canada)"),
            ("au", "sugargoospreadsheet.au", "English (Australia)"),
        ]),
        (u["local_group"], [
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
        f"{escape(u['register_on'].format(brand='Sugargoo'))}</a></div>"
    )
    parts.append("</div></div>")
    return "".join(parts)


def _trust_paths(key: str) -> dict:
    """Local Help/News/About slugs, HipoBuy-country style (ES gold uses Ayuda/Novedades labels)."""
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
    if key in ("de", "at"):
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
            ("/sugargoo-spreadsheet/", "Spreadsheet", page == "sheet"),
            ("/sugargoo-coupons/", "Coupons", page == "coupons"),
            (hp, t["help_lab"], page == "help"),
            (np, t["news_lab"], page == "news"),
            (ap, t["about_lab"], page == "about"),
            ("/#lab", "Livraison", page == "lab"),
        ]
        cta, browse = "Voir le catalogue", "Spreadsheet complète"
    elif key == "es":
        items = [
            ("/", "Inicio", page == "home"),
            ("/sugargoo-spreadsheet/", "Spreadsheet", page == "sheet"),
            ("/sugargoo-coupons/", "Cupones", page == "coupons"),
            (hp, t["help_lab"], page == "help"),
            (np, t["news_lab"], page == "news"),
            (ap, t["about_lab"], page == "about"),
            ("/#lab", "Envíos", page == "lab"),
        ]
        cta, browse = "Ver catálogo", "Spreadsheet completa"
    elif key in ("de", "at"):
        items = [
            ("/", "Start", page == "home"),
            ("/sugargoo-spreadsheet/", "Spreadsheet", page == "sheet"),
            ("/sugargoo-coupons/", "Coupons", page == "coupons"),
            (hp, t["help_lab"], page == "help"),
            (np, t["news_lab"], page == "news"),
            (ap, t["about_lab"], page == "about"),
            ("/#lab", "Versand", page == "lab"),
        ]
        cta, browse = "Katalog", "Ganzes Spreadsheet"
    elif key == "nl":
        items = [
            ("/", "Home", page == "home"),
            ("/sugargoo-spreadsheet/", "Spreadsheet", page == "sheet"),
            ("/sugargoo-coupons/", "Coupons", page == "coupons"),
            (hp, t["help_lab"], page == "help"),
            (np, t["news_lab"], page == "news"),
            (ap, t["about_lab"], page == "about"),
            ("/#lab", "Verzending", page == "lab"),
        ]
        cta, browse = "Catalogus", "Volledige spreadsheet"
    elif key == "now":
        items = [
            ("/", "Home", page == "home"),
            ("/sugargoo-coupon-2026.html", "Coupons", page == "coupons"),
            ("/best-sugargoo-spreadsheet-2026.html", "Spreadsheet", page == "sheet"),
            (hp, t["help_lab"], page == "help"),
            (np, t["news_lab"], page == "news"),
            (ap, t["about_lab"], page == "about"),
            ("/#lab", "Shipping", page == "lab"),
        ]
        cta, browse = "Browse catalogue", "Full spreadsheet"
    else:
        items = [
            ("/", "Home", page == "home"),
            ("/sugargoo-spreadsheet/", "Spreadsheet", page == "sheet"),
            ("/sugargoo-coupons/", "Coupons", page == "coupons"),
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
    w2c = f"{W2C}?utm_source={d['utm']}&utm_medium=desk&utm_campaign=sugargoo"
    return nav, cta, browse, w2c


def _chrome_head(key: str, d: dict, title: str, desc: str, path: str = "/") -> str:
    host = d["host"]
    if not path.startswith("/"):
        path = "/" + path
    canonical = f"https://{host}{path}"
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


def _header(key: str, d: dict, page: str = "home") -> str:
    nav, cta, browse, w2c = _nav(key, d, page=page)
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
      <button class="mobile-toggle" data-mobile-toggle aria-label="{escape(ui_copy(_loc(key))['menu'])}"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="3" y1="6" x2="21" y2="6"/><line x1="3" y1="12" x2="21" y2="12"/><line x1="3" y1="18" x2="21" y2="18"/></svg></button>
    </div>
  </div>
</header>
"""


def _footer(key: str, d: dict) -> str:
    u = ui_copy(_loc(key))
    t = _trust_paths(key)
    return f"""<footer class="site-footer">
  <div class="container">
    <div class="footer-grid">
      <div class="footer-brand"><a href="/" class="brand sugargoo-brand"><img class="brand-logo sugargoo-logo" src="/assets/images/sugargoo-logo.png" alt="Sugargoo"></a>
      <p>{escape(u['foot'].format(host=d['host'], brand='SugarGoo'))}</p></div>
      <div class="footer-col"><h5>{escape(u['on_host'])}</h5><ul>
        <li><a href="/{t['help']}/">{escape(t['help_lab'])}</a></li>
        <li><a href="/{t['news']}/">{escape(t['news_lab'])}</a></li>
        <li><a href="/{t['about']}/">{escape(t['about_lab'])}</a></li>
        {''.join(f'<li><a href="{escape(h)}">{escape(l)}</a></li>' for h,l in d['keep'])}
      </ul></div>
      <div class="footer-col"><h5>{escape(u['official'])}</h5><ul>
        <li><a href="{EST}">{escape(u['freight'])}</a></li>
        <li><a href="{REG}" rel="noopener sponsored">{escape(u['register'])}</a></li>
        <li><a href="{OFFICIAL}">sugargoo.com</a></li>
      </ul></div>
      <div class="footer-col"><h5>{escape(u['contact'])}</h5><ul>
        <li><a href="mailto:{escape(d['mail'])}">{escape(d['mail'])}</a></li>
        <li><a href="/privacy-policy/">{escape(u['privacy'])}</a></li>
        <li><a href="/cookie-policy/">{escape(u['cookies'])}</a></li>
      </ul></div>
    </div>
    <p class="footer-locale-cluster" style="margin:12px 0;font-size:13px;color:#94A3B8">{escape(u['desks'])}:
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
    <div class="footer-bottom"><div>© 2026 {escape(d['host'])} · {escape(u['indep'])}</div></div>
  </div>
</footer>
<script src="/assets/js/main.js?v=20260930-home"></script>
</body></html>
"""


def _catalog(key: str) -> str:
    return catalog_block(key, HOSTS[key], register_url=REG, loc_fn=_loc, cat_labels=CAT_LABELS)


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


def _help_meta(key: str, d: dict) -> dict:
    loc = d["locale"]
    dest = d["dest_label"]
    if key == "es":
        return {
            "title": "Ayuda: quince preguntas sobre SugarGoo en España",
            "desc": "Desk ES independiente: catálogo en inglés, Packing Center 100 días, estimador con destino España. Lab 30 sep 2026.",
            "h1": "Ayuda y preguntas frecuentes sobre SugarGoo en <em>español</em>",
            "lead": "Esta página vale para una calle española en este host. No vemos tu cuenta. Pedidos, pagos y reclamaciones solo en sugargoo.com.",
            "h2": "Las quince preguntas que más se repiten",
            "ask_h": "Dónde preguntar cuando esto no basta",
            "ask": "El chat de la app oficial. Este desk no opera tu cuenta. Los cupones siguen en /sugargoo-coupons/; la aduana en /aduana-iva-espana/.",
        }
    if key == "fr":
        return {
            "title": "Aide : quinze questions sur SugarGoo en France",
            "desc": "Desk FR indépendant : catalogue anglais, Packing Center 100 jours, estimateur vers la France. Lab 30 sept. 2026. Pas la Belgique.",
            "h1": "Aide et questions fréquentes sur SugarGoo en <em>France</em>",
            "lead": "Cette page vaut pour une adresse en France sur ce host. On ne voit pas ton compte. Commandes et litiges seulement sur sugargoo.com.",
            "h2": "Les quinze questions qui reviennent",
            "ask_h": "Où demander si cela ne suffit pas",
            "ask": "Le chat de l’app officielle. Ce desk n’opère pas ton compte. Coupons et avis restent sur leurs URL classées.",
        }
    if key in ("de", "at"):
        land = "Österreich" if key == "at" else "Deutschland"
        return {
            "title": f"Hilfe: fünfzehn Fragen zu SugarGoo in {land}",
            "desc": f"Unabhängiger Desk: englischer Katalog, 100 Tage Packing Center, Schätzer nach {land}. Lab 30. Sep 2026.",
            "h1": f"Hilfe: fünfzehn Fragen zu SugarGoo in <em>{land}</em>",
            "lead": f"Diese Seite gilt für eine Straße in {land} auf diesem Host. Wir sehen dein Konto nicht. Bestellungen nur auf sugargoo.com.",
            "h2": "Die fünfzehn häufigsten Fragen",
            "ask_h": "Wohin, wenn das nicht reicht",
            "ask": "Offizieller App-Chat. Dieser Desk führt dein Konto nicht. Coupons bleiben im Coupon-Artikel.",
        }
    if key == "nl":
        return {
            "title": "Hulp: vijftien vragen over SugarGoo in Nederland",
            "desc": "Onafhankelijke NL-desk: Engelse catalogus, 100 dagen Packing Center, estimator naar Nederland. Lab 30 sep 2026.",
            "h1": "Hulp: vijftien vragen over SugarGoo in <em>Nederland</em>",
            "lead": "Deze pagina geldt voor een Nederlands adres op deze host. We zien je account niet. Orders alleen op sugargoo.com.",
            "h2": "De vijftien vragen die het vaakst terugkomen",
            "ask_h": "Waar vragen als dit niet volstaat",
            "ask": "De chat in de officiële app. Deze desk voert je account niet. Coupons blijven op de coupon-URL.",
        }
    if key == "now":
        return {
            "title": "Help: fifteen questions on this SugarGoo coupon hub",
            "desc": "Independent English hub. Destination is a country in the official estimator, not this hostname. Lab 30 Sep 2026.",
            "h1": "Help: fifteen questions on this <em>coupon hub</em>",
            "lead": "This hostname is not a destination. Dated html articles stay. Orders run only on sugargoo.com.",
            "h2": "The fifteen questions that come back most",
            "ask_h": "Where to ask when this is not enough",
            "ask": "Official in-app chat. This desk does not run your account. Coupon html files on this host stay put.",
        }
    return {
        "title": f"Help: fifteen questions about SugarGoo in {loc}",
        "desc": f"Independent desk: English catalogue, 100-day packing center, estimator to {dest}. Lab 30 Sep 2026.",
        "h1": f"Help: fifteen questions about SugarGoo in <em>{escape(loc)}</em>",
        "lead": f"This page is for a {dest} address on this host. We cannot see your account. Orders and claims run only on sugargoo.com.",
        "h2": "The fifteen questions that come back most",
        "ask_h": "Where to ask when this is not enough",
        "ask": "Official in-app chat. This desk does not operate your SugarGoo account. Ranked coupon and customs URLs stay on this host.",
    }


def _news_meta(key: str, d: dict) -> dict:
    loc = d["locale"]
    dest = d["dest_label"]
    if key == "es":
        return {
            "title": "Novedades: lo que hemos comprobado en SugarGoo para España",
            "desc": "Notas con fecha de este desk ES. No copiamos las 58 líneas de otro agente. Lab 30 sep 2026.",
            "h1": "Qué hemos comprobado en la plataforma, <em>con fecha</em>",
            "lead": "Cada bloque es una medición o una captura de este host, no un recorte de hipobuy.es.",
            "how_h": "Cómo comprobamos las cosas",
            "how": "Homepage y /api/products/ de este host, el estimador oficial con destino España, y las URL que ya posicionan. No inventamos un recuento de líneas ajenas.",
        }
    if key == "fr":
        return {
            "title": "Actualités : ce que nous avons vérifié sur SugarGoo pour la France",
            "desc": "Notes datées du desk FR. Destination France, pas la Belgique. Lab 30 sept. 2026.",
            "h1": "Ce que nous avons vérifié sur la plateforme, <em>avec date</em>",
            "lead": "Chaque bloc est une mesure sur ce host, pas une copie d’un autre agent.",
            "how_h": "Comment on vérifie",
            "how": "Accueil et /api/products/ de ce host, estimateur officiel vers la France, URL déjà classées. Pas de copie des lignes ES d’un autre agent.",
        }
    if key in ("de", "at"):
        land = "Österreich" if key == "at" else "Deutschland"
        return {
            "title": f"Neuigkeiten: was wir an SugarGoo für {land} geprüft haben",
            "desc": f"Datierte Notizen dieses Desks. Schätzer nach {land}. Lab 30. Sep 2026.",
            "h1": "Was wir auf der Plattform geprüft haben, <em>mit Datum</em>",
            "lead": "Jeder Block ist eine Messung auf diesem Host, kein fremder Linien-Schnappschuss.",
            "how_h": "Wie wir messen",
            "how": f"Startseite und /api/products/ dieses Hosts, offizieller Schätzer nach {land}, bereits rankende URLs.",
        }
    if key == "nl":
        return {
            "title": "Nieuws: wat we op SugarGoo voor Nederland hebben nagemeten",
            "desc": "Gedateerde notities van deze NL-desk. Lab 30 sep 2026.",
            "h1": "Wat we op het platform hebben nagemeten, <em>met datum</em>",
            "lead": "Elk blok is een meting op deze host, geen kopie van een andere agent.",
            "how_h": "Hoe we meten",
            "how": "Homepage en /api/products/ van deze host, officiële estimator naar Nederland, URL’s die al ranken.",
        }
    if key == "now":
        return {
            "title": "News: what we checked on this SugarGoo coupon hub",
            "desc": "Dated notes. This hostname is not a destination. Html articles stay. Lab 30 Sep 2026.",
            "h1": "What we checked on this hub, <em>with dates</em>",
            "lead": "Each block is a measurement on this host. Spain-only line counts stay off this page.",
            "how_h": "How we measure",
            "how": "Homepage and /api/products/ on this host, official estimator with a country code, existing html articles left in place.",
        }
    return {
        "title": f"News: what we checked on SugarGoo for {loc}",
        "desc": f"Dated notes on this independent desk. Estimator destination {dest}. Lab 30 Sep 2026.",
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
            ("Check 1 · 30 sep 2026 · catálogo en esta portada",
             f"Restauramos el catálogo en / vía {api}. Clave inglesa sneakers devuelve fichas; zapatillas suele dar 0."),
            ("Check 2 · el conmutador de moneda no convierte",
             "En el sitio oficial el símbolo puede pasar a EUR y las cifras seguir en dólares. Lee el número, no solo el símbolo."),
            ("Check 3 · el estimador pide España, no este TLD",
             "Abrimos freight-estimate con destino España. No copiamos las 58 líneas de hipobuy.es ni un precio de otro agente."),
            ("Check 4 · Packing Center 100 días",
             "El blog oficial de SugarGoo: 100 días gratis en pedidos de compra desde Packing Center — no la cifra 90 de otro agente."),
            ("Check 5 · URLs que ya posicionan",
             " /aduana-iva-espana/ y /sugargoo-coupons/ se conservan. Esta novedad no las pisa."),
            ("Check 6 · 30 sep 2026 · SPA del estimador y página Sobre",
             "El HTML crudo de freight-estimate era ~2 KB. El navegador del 30 sep 2026 sí renderizó el formulario; la captura está en /media/. Sobre nosotros es página propia, no un ancla."),
        ]
    if key == "fr":
        return [
            ("Check 1 · 30 sept. 2026 · catalogue sur cette accueil",
             f"Catalogue restauré sur / via {api}. La clé sneakers remplit la grille ; baskets donne souvent 0."),
            ("Check 2 · le sélecteur de devise ne convertit pas",
             "Le symbole peut passer en EUR et le chiffre rester en dollars. Lis le nombre."),
            ("Check 3 · l’estimateur veut la France",
             "Destination France, pas la Belgique, pas un TLD. Pas de copie des lignes ES d’un autre agent."),
            ("Check 4 · Packing Center 100 jours",
             "Blog officiel SugarGoo : 100 jours gratuits à partir du Packing Center pour les ordres d’achat."),
            ("Check 5 · URL déjà classées",
             "/sugargoo-coupons/ et /sugargoo-review/ restent. Cette page actualités ne les écrase pas."),
            ("Check 6 · 30 sept. 2026 · SPA estimateur et page À propos",
             "Le HTML brut de freight-estimate faisait ~2 ko. Le navigateur du 30 sept. 2026 a rendu le formulaire ; capture dans /media/. À propos est une page, pas une ancre."),
        ]
    if key in ("de", "at"):
        land = "Österreich" if key == "at" else "Deutschland"
        return [
            (f"Check 1 · 30. Sep 2026 · Katalog auf dieser Startseite",
             f"Katalog wieder auf / über {api}. Englisch sneakers füllt das Raster; Turnschuhe oft 0."),
            ("Check 2 · Währungsschalter rechnet nicht um",
             "Das Symbol kann auf EUR springen, die Ziffer Dollar bleiben. Die Zahl lesen."),
            (f"Check 3 · Schätzer nach {land}",
             f"Offizieller Schätzer mit Ziel {land}. Keine 58 ES-Linien eines anderen Agenten."),
            ("Check 4 · Packing Center 100 Tage",
             "Offizieller SugarGoo-Blog: 100 Tage gratis ab Packing Center bei Kaufaufträgen."),
            ("Check 5 · bereits rankende URLs",
             "Coupon- und Spreadsheet-Artikel bleiben. Diese Neuigkeiten-Seite überschreibt sie nicht."),
            ("Check 6 · 30. Sep 2026 · SPA-Schätzer und Über uns",
             "Roh-HTML von freight-estimate war ~2 KB. Der Browser am 30 Sep 2026 hat das Formular gerendert; Aufnahme unter /media/. Über uns ist eine eigene Seite."),
        ]
    if key == "nl":
        return [
            ("Check 1 · 30 sep 2026 · catalogus op deze homepage",
             f"Catalogus terug op / via {api}. Engels sneakers vult het raster; lokale woorden vaak 0."),
            ("Check 2 · valutaswitcher rekent niet om",
             "Het symbool kan EUR worden terwijl het cijfer dollar blijft. Lees het getal."),
            ("Check 3 · estimator naar Nederland",
             "Officiële estimator met bestemming Nederland. Geen ES-lijnen van een andere agent."),
            ("Check 4 · Packing Center 100 dagen",
             "Officiële SugarGoo-blog: 100 dagen gratis vanaf Packing Center voor kooporders."),
            ("Check 5 · URL’s die al ranken",
             "Coupon- en BTW-artikelen blijven. Deze nieuwspagina overschrijft ze niet."),
            ("Check 6 · 30 sep 2026 · SPA-estimator en Over ons",
             "Ruwe HTML van freight-estimate was ~2 KB. De browser op 30 sep 2026 renderde het formulier; opname in /media/. Over ons is een eigen pagina."),
        ]
    if key == "now":
        return [
            ("Check 1 · 30 Sep 2026 · catalogue on this hub homepage",
             f"Catalogue restored on / via {api}. English keys fill the grid. Dated html files stay."),
            ("Check 2 · currency switcher does not convert",
             "Official site: the symbol can change while the digits stay dollars."),
            ("Check 3 · this hostname is not a destination",
             "Open the official estimator with a country code. Spain-only line counts stay off this hub."),
            ("Check 4 · packing center 100 days",
             "Official SugarGoo blog: 100 free days on purchasing orders from Packing Center."),
            ("Check 5 · html articles kept",
             "Coupon, Reddit, legit and spreadsheet html files were not overwritten."),
            ("Check 6 · 30 Sep 2026 · SPA estimator and About page",
             "Raw HTML of freight-estimate was ~2 KB. The 30 Sep 2026 browser rendered the form; capture in /media/. /who-we-are/ is its own page, not an anchor."),
        ]
    extra = {
        "us": "Ranked de-minimis, USPS times and coupons URLs stay.",
        "au": "The ranked GST article at /gst-import-australia/ stays.",
        "ca": "The ranked CBSA article at /cbsa-import-canada/ stays.",
        "uk": "The UK VAT article stays.",
    }.get(key, "Ranked coupon and guide URLs stay.")
    return [
        ("Check 1 · 30 Sep 2026 · catalogue on this homepage",
         f"Catalogue restored on / via {api}. English key sneakers fills the grid; local words often return zero."),
        ("Check 2 · currency switcher does not convert",
         "On the official site the symbol can change to a local currency while the digits stay dollars. Read the number."),
        (f"Check 3 · estimator destination {dest}",
         f"Open the official freight estimate with {dest}. We do not paste another agent’s line count onto this desk."),
        ("Check 4 · packing center 100 days",
         "Official SugarGoo blog: 100 free days on purchasing orders from Packing Center — not a 90-day figure from another agent."),
        ("Check 5 · ranked URLs kept", extra),
        ("Check 6 · 30 Sep 2026 · SPA estimator and About page",
         "Raw HTML of freight-estimate was ~2 KB. The 30 Sep 2026 browser rendered the form; capture lives under /media/. /who-we-are/ is its own page."),
    ]


def build_help(key: str) -> str:
    d = HOSTS[key]
    t = _trust_paths(key)
    m = _help_meta(key, d)
    if INVITE in m["title"] or COUPON in m["title"]:
        raise RuntimeError(f"{key} help: code in title")
    faqs = _faqs(key, d)
    faq_ld = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "inLanguage": d["lang"],
        "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
            for q, a in faqs
        ],
    }
    html = _chrome_head(key, d, m["title"], m["desc"], path=f"/{t['help']}/")
    # extra FAQ JSON-LD
    html = html.replace("</head>", f'<script type="application/ld+json">{json.dumps(faq_ld, ensure_ascii=False)}</script>\n</head>', 1)
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
<p><a class="btn btn-primary" href="{REG}" target="_blank" rel="noopener sponsored">{escape({"fr":"S’inscrire","es":"Registrarse","de":"Registrieren","at":"Registrieren","nl":"Registreren"}.get(key,"Register"))}</a>
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
    html = _chrome_head(key, d, m["title"], m["desc"], path=f"/{t['news']}/")
    html += _header(key, d, page="news")
    blocks = []
    for h, p in _news_items(key, d):
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
    <img src="/media/official-home-20260930.jpg" alt="{escape(p['agent_cap'])}" width="1400" height="1069" loading="lazy" decoding="async">
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
    <img src="/media/help-restricted-20260930.jpg" alt="{escape(p['rest_cap'])}" width="1400" height="1166" loading="lazy" decoding="async">
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
    <img src="/media/estimator-20260930.jpg" alt="{escape(p['shot_est_cap'])}" width="1400" height="1069" loading="lazy" decoding="async">
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
  <a class="btn btn-primary" href="{REG}" target="_blank" rel="noopener sponsored">{escape({"fr":"S’inscrire","es":"Registrarse","de":"Registrieren","at":"Registrieren","nl":"Registreren"}.get(key,"Register"))}</a></p>
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
    <a class="btn btn-primary" href="#catalog">{escape({"fr":"Catalogue","es":"Catálogo","de":"Katalog","at":"Katalog","nl":"Catalogus"}.get(key,"Catalogue"))}</a>
    <a class="btn btn-outline" href="{EST}">{escape({"fr":"Estimateur","es":"Estimador","de":"Schätzer","at":"Schätzer","nl":"Estimator"}.get(key,"Estimator"))}</a>
    <a class="btn btn-outline" href="{REG}" target="_blank" rel="noopener sponsored">{escape({"fr":"S’inscrire","es":"Registrarse","de":"Registrieren","at":"Registrieren","nl":"Registreren"}.get(key,"Register"))}</a>
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
            "sugargoo-theme.css",
            "/api/products/",
            "/img/cat/sneakers.jpg",
            "/media/estimator-20260930.jpg",
            "/media/official-home-20260930.jpg",
            "/media/help-restricted-20260930.jpg",
        ):
            if tok not in html:
                raise SystemExit(f"{key}: missing {tok}")
        ccy = currency_for(key, d)
        if f'var FX_CCY="{ccy}"' not in html or "FX_RATE" not in html:
            raise SystemExit(f"{key}: missing local FX {ccy}")
        if "p.textContent=(it.currency||'')+' '+(it.price" in html:
            raise SystemExit(f"{key}: raw CNY catalogue concat")
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
            if "sugargoo-theme.css" not in page or "locale-switcher" not in page:
                raise SystemExit(f"{key} {label}: chrome")
            if key == "now" and ("58 líneas" in page or "ES AIR" in page):
                raise SystemExit("now.com help/news copied Spain lines")
            if key == "fr" and ("Belgique" in pt or "Belgium" in pt or "France / BE" in page):
                raise SystemExit("fr help/news became Belgium")
        hf = len(re.findall(r"class=\"sg-faq\"", help_html))
        if hf < 15:
            raise SystemExit(f"{key} help faq {hf}")
        hn = len(re.findall(r"<h2>", news_html))
        if hn < 6:
            raise SystemExit(f"{key} news h2 {hn}")
        print(f"OK    {key}/help words={_wc(help_html)} faq={hf}")
        print(f"OK    {key}/news words={_wc(news_html)} h2={hn}")

        about_html = build_about(key)
        at = re.search(r"<title>(.*?)</title>", about_html, flags=re.S).group(1)
        if INVITE in at or COUPON in at:
            raise SystemExit(f"{key} about: code in title")
        if "Georgia" in about_html or "#00C853" in about_html or "gsc-editor-notes" in about_html:
            raise SystemExit(f"{key} about: junk")
        if "sugargoo-theme.css" not in about_html or "locale-switcher" not in about_html:
            raise SystemExit(f"{key} about: chrome")
        if f"/{t['about']}/" not in about_html:
            raise SystemExit(f"{key} about: canonical slug")
        if key == "now" and ("58 líneas" in about_html or "ES AIR" in about_html):
            raise SystemExit("now.com about copied Spain lines")
        if key == "fr" and ("Belgique" in at or "Belgium" in at or "France / BE" in about_html):
            raise SystemExit("fr about became Belgium")
        if _wc(about_html) < 280:
            raise SystemExit(f"{key} about too short")
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
            "    <lastmod>2026-09-30</lastmod>\n"
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
    bak = f"/www/backup/sugargoo-sitemap-{host}-20260930.xml"
    _run(client, f"cp -a '{path}' '{bak}'")
    with sftp.open(path, "w") as fh:
        fh.write(chunk)
    sftp.close()
    print("sitemap +", added, host)


SHARED = ROOT / "sites" / "sugargoo-shared"


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
    bak = f"/www/backup/sugargoo-trust-{stamp}"
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
    sftp.close()
    client.close()


if __name__ == "__main__":
    main()
