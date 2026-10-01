#!/usr/bin/env python3
"""Kakobuy country desks: dest-unique #local, catalogue on /, teal Inter chrome.

Order: CA → FI → ES → docs (surgical hub) → FR → NL.
Not HipoBuy green, not LitBuy yellow, not SugarGoo orange, not Georgia memos.
Does not overwrite ranked inner URLs. Invite/coupon codes stay off titles.
Storage: confirm official Help; do not invent 100 vs 180.
US stays on kakobuytips.com — this cluster does not take US, no tips 301.
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
    dest_local_pack,
    faq_ld,
    independence_copy,
    inject_jsonld,
    itemlist_ld,
    keep_copy,
    lab_copy,
    local_cta,
    local_guide_html,
    long_faqs,
    og_locale,
    organization_ld,
    skip_label,
    skip_link,
    validate_desk,
    vol_js_labels,
    webpage_ld,
)
from kakobuy_desk_trust import CAT_LABELS, CAT_WALL, loc as _loc, pack as _trust_pack

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "sites"
SHARED = ROOT / "sites" / "kakobuy-shared"
EST = "https://www.kakobuy.com/tools/estimate"
OFFICIAL = "https://www.kakobuy.com/"
REG = "https://www.kakobuy.com/"
W2C = "https://w2clinks.com/spreadsheet/kakobuy/"
DATE = "1 Oct 2026"
INVITE = "yze69"
COUPON = "KAKOSEP"
IKAKO = "ikako.vip"
STORAGE = (
    "Confirm the live Kakobuy Help Center the morning you ship. "
    "Public copies of the storage article have quoted both 100 days from in-storage and 180 days; "
    "this desk does not pick a number."
)

PRIMARY = "#0284c7"
SOFT = "#e0f2fe"

HOSTS = {
    "ca": {
        "host": "kakospreadsheet.ca",
        "lang": "en-CA",
        "locale": "Canada",
        "dest": "CA",
        "dest_label": "Canada",
        "badge": "Canada · CAD · CBSA",
        "mail": "support@kakospreadsheet.ca",
        "utm": "kakospreadsheet_ca",
        "logo": "/assets/kakobuy-logo.png",
        "keep": [
            ("/kakobuy-shipping-to-canada/", "Shipping to Canada (ranked URL)"),
            ("/kakobuy-canada/", "Kakobuy Canada"),
            ("/is-kakobuy-legit/", "Is Kakobuy legit"),
            ("/kakobuy-spreadsheet/", "Spreadsheet guide"),
            ("/kakobuy-coupon/", "Coupons (article kept; codes off this title)"),
            ("/about/", "Existing about (kept)"),
        ],
    },
    "fi": {
        "host": "kakobuy.fi",
        "lang": "fi-FI",
        "locale": "Suomi",
        "dest": "FI",
        "dest_label": "Suomi",
        "badge": "Suomi · EUR · Tulli",
        "mail": "support@kakobuy.fi",
        "utm": "kakobuy_fi",
        "logo": "/assets/kakobuy-logo.png",
        "keep": [
            ("/kakobuy-toimitus/", "Toimitus Suomeen (rankkaava URL)"),
            ("/kakobuy-kokemuksia/", "Kakobuy kokemuksia"),
            ("/kakobuy-suomi/", "Kakobuy Suomi"),
            ("/kakobuy-spreadsheet/", "Spreadsheet"),
            ("/kakobuy-coupon/", "Kuponki (artikkeli säilyy)"),
            ("/faq/", "Vanha faq-stub (säilytetään)"),
        ],
    },
    "es": {
        "host": "kakospreadsheet.es",
        "lang": "es-ES",
        "locale": "España",
        "dest": "ES",
        "dest_label": "España",
        "badge": "España · EUR · aduana",
        "mail": "support@kakospreadsheet.es",
        "utm": "kakospreadsheet_es",
        "logo": "/assets/kakobuy-logo.png",
        "keep": [
            ("/envio-kakobuy-espana/", "Envío Kakobuy España"),
            ("/kakobuy-opiniones/", "Opiniones"),
            ("/es-kakobuy-confiable/", "¿Es confiable?"),
            ("/kakobuy-spreadsheet/", "Spreadsheet"),
            ("/kakobuy-coupon/", "Cupones (artículo; códigos fuera de este título)"),
            ("/about/", "About existente (se conserva)"),
        ],
    },
    "fr": {
        "host": "kakospreadsheet.fr",
        "lang": "fr-FR",
        "locale": "France",
        "dest": "FR",
        "dest_label": "la France",
        "badge": "France · EUR · douane FR",
        "mail": "support@kakospreadsheet.fr",
        "utm": "kakospreadsheet_fr",
        "logo": "/assets/kakobuy-logo.png",
        "keep": [
            ("/livraison-kakobuy/", "Livraison France"),
            ("/kakobuy-france/", "Kakobuy France"),
            ("/avis-kakobuy/", "Avis Kakobuy"),
            ("/kakobuy-spreadsheet/", "Spreadsheet"),
            ("/kakobuy-coupon/", "Coupons"),
            ("/about/", "About existant (conservé)"),
        ],
    },
    "nl": {
        "host": "kakospreadsheet.nl",
        "lang": "nl-NL",
        "locale": "Nederland",
        "dest": "NL",
        "dest_label": "Nederland",
        "badge": "Nederland · EUR · douane",
        "mail": "support@kakospreadsheet.nl",
        "utm": "kakospreadsheet_nl",
        "logo": "/assets/kakobuy-logo.png",
        "keep": [
            ("/kakobuy-verzending/", "Verzending Nederland"),
            ("/kakobuy-ervaringen/", "Ervaringen"),
            ("/kakobuy-spreadsheet/", "Spreadsheet"),
            ("/kakobuy-coupon/", "Coupons"),
            ("/is-kakobuy-legit/", "Is Kakobuy legit"),
            ("/about/", "Bestaande about (behouden)"),
        ],
    },
}

HOME_META = {
    "ca": {
        "title": "Buy from China to Canada with Kakobuy",
        "desc": "Independent CA desk: catalogue on this homepage, CBSA source, official freight estimate. Lab 1 Oct 2026. Ranked shipping-to-Canada URL stays.",
        "h1": "Using Kakobuy to ship from China to <em>Canada</em>",
        "hsub": "Canadian postal code (form A1A 1A1) in the estimator, not a US ZIP. Ranked /kakobuy-shipping-to-canada/ stays. Catalogue, FAQ and the freight lab sit on this homepage.",
    },
    "fi": {
        "title": "Tilaa Kiinasta Suomeen Kakobuylla — suomalainen osoite",
        "desc": "Riippumaton FI-desk: katalogi tällä etusivulla. Tulli (tulli.fi). Rankkaava /kakobuy-toimitus/ säilyy. Lab 1. loka 2026.",
        "h1": "Kakobuylla Kiinasta <em>Suomeen</em>",
        "hsub": "Arvioijan kohde FI, viisinumeroinen postinumero kuten 00100 Helsinki — ei Ruotsi, ei EU. /kakobuy-toimitus/ ja /kakobuy-kokemuksia/ säilyvät.",
    },
    "es": {
        "title": "Comprar en China y enviar a España con Kakobuy",
        "desc": "Desk ES independiente. Catálogo en esta portada. /envio-kakobuy-espana/ se conserva. Lab 1 oct 2026. No copiamos un recuento de líneas ajeno.",
        "h1": "Enviar de China a <em>España</em> con Kakobuy",
        "hsub": "El artículo de envío sigue en /envio-kakobuy-espana/. Esta portada es el catálogo. No copiamos un recuento de líneas de otro agente.",
    },
    "fr": {
        "title": "Acheter en Chine et envoyer en France avec Kakobuy",
        "desc": "Desk FR indépendant : catalogue sur cette accueil. Destination France dans l’estimateur. Pas la Belgique. Lab 1 oct. 2026.",
        "h1": "Envoyer de Chine en <em>France</em> avec Kakobuy",
        "hsub": "Les articles /livraison-kakobuy/ et /kakobuy-france/ restent. La destination dans l’estimateur est la France, pas la Belgique.",
    },
    "nl": {
        "title": "Met Kakobuy naar Nederland verzenden — kopen in China op een NL-adres",
        "desc": "Onafhankelijke NL-desk: catalogus op deze homepage. Nederlandse postcode. Lab 1 okt 2026.",
        "h1": "Met <em>Kakobuy</em> naar Nederland verzenden",
        "hsub": "Estimator-bestemming NL met Nederlandse postcode, geen Duits afhaalautomaat-nummer. /kakobuy-verzending/ blijft.",
    },
}

THEME_CSS = f"""
:root{{--primary:{PRIMARY};--primary-soft:{SOFT};--ink:#0f172a;--muted:#475569;--line:#e5e7eb;--bg:#f8fafc}}
*{{box-sizing:border-box}}
html,body{{margin:0;padding:0}}
body{{font-family:Inter,system-ui,-apple-system,sans-serif;color:var(--ink);background:#fff;line-height:1.55}}
a{{color:var(--primary)}}
.topbar{{background:#0c4a6e;color:#e0f2fe;font-size:13px}}
.topbar .container{{max-width:1100px;margin:0 auto;padding:8px 24px}}
.topbar a{{color:#fff}}
.site-header{{position:sticky;top:0;z-index:10;background:#fff;border-bottom:1px solid var(--line)}}
.container{{max-width:1100px;margin:0 auto;padding:0 24px}}
.header-inner{{display:flex;align-items:center;gap:16px;min-height:64px}}
.brand-logo{{height:32px;width:auto;display:block}}
.nav{{display:flex;flex-wrap:wrap;gap:12px;font-size:14px;font-weight:600}}
.nav a{{color:#334155;text-decoration:none}}
.nav a.active,.nav a:hover{{color:var(--primary)}}
.header-actions{{margin-left:auto;display:flex;align-items:center;gap:8px}}
.btn{{display:inline-block;border-radius:9px;padding:8px 12px;font-size:13px;font-weight:600;text-decoration:none;border:1px solid transparent}}
.btn-primary{{background:var(--primary);color:#fff}}
.btn-outline{{border-color:var(--primary);color:var(--primary);background:#fff}}
.mobile-toggle{{display:none;background:none;border:0;padding:6px}}
.mobile-toggle svg{{width:22px;height:22px}}
.eu-badge{{display:inline-block;font-size:12px;font-weight:700;background:var(--primary-soft);color:var(--primary);padding:4px 10px;border-radius:999px}}
.site-footer{{background:#0f172a;color:#cbd5e1;margin-top:24px;padding:36px 0 20px;font-size:14px}}
.site-footer a{{color:#e0f2fe}}
.footer-grid{{display:grid;grid-template-columns:1.4fr repeat(3,1fr);gap:24px}}
.footer-brand p{{color:#94a3b8}}
.footer-col h5{{margin:0 0 8px;color:#fff}}
.footer-col ul{{list-style:none;margin:0;padding:0;display:grid;gap:6px}}
.footer-bottom{{margin-top:20px;border-top:1px solid #1e293b;padding-top:12px;color:#64748b}}
.locale-switcher{{position:relative}}
.locale-switcher-btn{{display:flex;align-items:center;gap:6px;background:#fff;border:1px solid var(--line);border-radius:9px;padding:6px 10px;font:inherit;cursor:pointer}}
.locale-switcher-btn svg{{width:16px;height:16px}}
.locale-switcher-panel{{position:absolute;right:0;top:110%;background:#fff;border:1px solid var(--line);border-radius:12px;min-width:220px;padding:8px;box-shadow:0 8px 24px rgba(15,23,42,.12);z-index:20}}
.locale-switcher-heading{{font-size:11px;letter-spacing:.4px;text-transform:uppercase;color:#64748b;padding:6px 8px}}
.locale-switcher-panel a{{display:block;padding:6px 8px;border-radius:8px;text-decoration:none;color:#0f172a}}
.locale-switcher-panel a.is-current,.locale-switcher-panel a:hover{{background:var(--primary-soft);color:var(--primary)}}
.locale-switcher-register{{padding:8px}}
@media(max-width:860px){{
  .nav{{display:none}}.nav.is-open{{display:flex;flex-direction:column;position:absolute;left:0;right:0;top:64px;background:#fff;padding:12px 24px;border-bottom:1px solid var(--line)}}
  .mobile-toggle{{display:block}}
  .footer-grid{{grid-template-columns:1fr 1fr}}
}}
.sg-hero{{max-width:1100px;margin:0 auto;padding:28px 24px 8px;text-align:left}}
.sg-hero h1{{font-size:clamp(28px,4.4vw,42px);font-weight:800;letter-spacing:-1.1px;line-height:1.15;margin:0 0 12px}}
.sg-hero h1 em{{font-style:normal;color:var(--primary)}}
.sg-hero .hsub{{color:#475569;font-size:16px;line-height:1.6;max-width:720px}}
.sg-hero .hbg{{display:inline-block;font-size:12px;font-weight:700;background:var(--primary-soft);color:var(--primary);padding:4px 10px;border-radius:999px;margin-bottom:12px}}
.sg-ctas{{display:flex;gap:10px;flex-wrap:wrap;margin:18px 0 8px}}
.sg-mw{{max-width:1200px;margin:0 auto;padding:8px 24px 48px}}
.sg-fbar{{display:flex;gap:8px;align-items:center;margin:12px 0 16px;flex-wrap:wrap}}
.sg-fbar input,.sg-fbar select{{height:38px;border:1.5px solid #e5e7eb;border-radius:9px;padding:0 12px;font:inherit}}
.sg-fbar input{{flex:1;min-width:180px}}
.sg-grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(180px,1fr));gap:13px}}
.sg-card{{border:1px solid #e5e7eb;border-radius:12px;overflow:hidden;background:#fff;display:flex;flex-direction:column}}
.sg-card img{{width:100%;aspect-ratio:1;object-fit:cover;background:#f8fafc}}
.sg-card .b{{padding:10px;display:flex;flex-direction:column;gap:6px;flex:1}}
.sg-card .t{{font-size:13px;font-weight:600;line-height:1.4;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden}}
.sg-card .pr{{font-weight:800;color:var(--primary)}}
.sg-card a.buy{{margin:0 10px 10px;text-align:center;padding:8px;border-radius:8px;background:var(--primary);color:#fff;font-size:12.5px;font-weight:600;text-decoration:none}}
.sg-chips{{display:flex;gap:8px;flex-wrap:wrap;margin:8px 0 4px}}
.sg-chips button{{border:1px solid #e5e7eb;background:#fff;border-radius:999px;padding:6px 12px;font:inherit;cursor:pointer}}
.sg-chips button.on{{background:var(--primary-soft);border-color:var(--primary);color:var(--primary);font-weight:600}}
.sg-sec{{max-width:1100px;margin:0 auto;padding:12px 24px 28px}}
.sg-sec h2{{font-size:22px;margin:0 0 8px}}
.sg-sec .ssub{{color:#64748b;margin:0 0 14px}}
.tw{{overflow-x:auto;border:1px solid #e5e7eb;border-radius:12px}}
.tw table{{width:100%;border-collapse:collapse;font-size:14px}}
.tw th,.tw td{{padding:10px 12px;border-bottom:1px solid #e5e7eb;text-align:left;vertical-align:top}}
.tw th{{background:#f8fafc;font-size:11px;letter-spacing:.4px;text-transform:uppercase;color:#64748b}}
details.sg-faq{{border:1px solid #e5e7eb;border-radius:10px;padding:10px 14px;margin:0 0 8px;background:#fff}}
details.sg-faq summary{{cursor:pointer;font-weight:600}}
.keep{{display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:10px}}
.keep a{{display:block;border:1px solid #e5e7eb;border-radius:10px;padding:12px;text-decoration:none;color:inherit;background:#fff}}
.keep a:hover{{border-color:var(--primary)}}
.vol{{border:1px solid #e5e7eb;border-radius:16px;padding:16px 18px;margin:16px 0;background:#fff}}
.vol input,.vol select{{width:100%;height:36px;border:1.5px solid #e5e7eb;border-radius:8px;padding:0 8px}}
figure.shot{{margin:16px 0}}
figure.shot img{{width:100%;max-width:920px;height:auto;border:1px solid #e5e7eb;border-radius:12px;background:#f8fafc}}
figure.shot figcaption{{font-size:13px;color:#64748b;margin-top:6px}}
.sg-split{{display:grid;grid-template-columns:1.05fr .95fr;gap:28px;align-items:start;margin:8px 0 4px}}
@media(max-width:860px){{.sg-split{{grid-template-columns:1fr}}}}
.sg-prose p{{color:#334155;line-height:1.75;margin:0 0 12px}}
.sg-prose .lead{{font-size:17px;color:#1e293b}}
.sg-cats{{display:grid;grid-template-columns:repeat(auto-fill,minmax(148px,1fr));gap:12px}}
a.sg-cat{{position:relative;display:block;border-radius:12px;overflow:hidden;color:#fff;text-decoration:none;background:#0f172a}}
a.sg-cat img{{width:100%;aspect-ratio:1;object-fit:cover;display:block}}
a.sg-cat .b{{position:absolute;left:0;right:0;bottom:0;padding:10px 12px;background:linear-gradient(transparent,rgba(15,23,42,.78))}}
a.sg-cat strong{{display:block;font-size:14px}}
a.sg-cat span{{font-size:11px;opacity:.85;letter-spacing:.2px}}
.sg-about h2{{font-size:22px;margin:28px 0 8px}}
.sg-about h3{{font-size:16px;margin:18px 0 6px}}
.sg-about p{{color:#334155;line-height:1.75;margin:0 0 12px}}
""" + EXTRA_CSS_FX + SKIP_CSS

PRODUCTS_PHP = r"""<?php
declare(strict_types=1);
/**
 * Adapter so the homepage catalogue can call /api/products/?q=&limit=
 * without deleting the live /api/products.php (hits / price_cny) proxy.
 */
$_GET['per_page'] = (string) max(1, min(48, (int)($_GET['limit'] ?? $_GET['per_page'] ?? 24)));
$upstream = dirname(__DIR__) . '/products.php';
if (!is_file($upstream)) {
    header('Content-Type: application/json; charset=utf-8');
    http_response_code(502);
    echo json_encode(['ok' => false, 'items' => []]);
    exit;
}
ob_start();
require $upstream;
$raw = ob_get_clean();
$data = json_decode((string) $raw, true);
if (!is_array($data)) {
    header('Content-Type: application/json; charset=utf-8');
    http_response_code(502);
    echo json_encode(['ok' => false, 'items' => []]);
    exit;
}
$items = [];
foreach (($data['hits'] ?? $data['items'] ?? []) as $h) {
    if (!is_array($h)) {
        continue;
    }
    $items[] = [
        'title' => (string) ($h['title'] ?? ''),
        'image' => (string) ($h['image'] ?? ''),
        'price' => $h['price_cny'] ?? $h['price'] ?? '',
        'currency' => (string) ($h['currency'] ?? 'CNY'),
        'href' => (string) ($h['url'] ?? $h['href'] ?? $h['target'] ?? ''),
    ];
}
header('Content-Type: application/json; charset=utf-8');
echo json_encode(
    [
        'ok' => true,
        'items' => $items,
        'found' => $data['found'] ?? count($items),
        'page' => $data['page'] ?? 1,
    ],
    JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE
);
"""

HREFLANG = [
    ("en-CA", "kakospreadsheet.ca"),
    ("fi-FI", "kakobuy.fi"),
    ("es-ES", "kakospreadsheet.es"),
    ("fr-FR", "kakospreadsheet.fr"),
    ("nl-NL", "kakospreadsheet.nl"),
]


def _hreflang() -> str:
    bits = [
        f'<link rel="alternate" hreflang="{escape(code)}" href="https://{escape(host)}/">'
        for code, host in HREFLANG
    ]
    bits.append('<link rel="alternate" hreflang="x-default" href="https://kakospreadsheet.ca/">')
    return "\n".join(bits)


def _trust_paths(key: str) -> dict:
    table = {
        "es": {
            "help": "ayuda",
            "news": "novedades",
            "about": "sobre-nosotros",
            "help_lab": "Ayuda",
            "news_lab": "Novedades",
            "about_lab": "Sobre",
        },
        "fr": {
            "help": "aide",
            "news": "actualites",
            "about": "a-propos",
            "help_lab": "Aide",
            "news_lab": "Actualités",
            "about_lab": "À propos",
        },
        "nl": {
            "help": "hulp",
            "news": "nieuws",
            "about": "over-ons",
            "help_lab": "Hulp",
            "news_lab": "Nieuws",
            "about_lab": "Over ons",
        },
        "fi": {
            "help": "ohje",
            "news": "uutiset",
            "about": "meista",
            "help_lab": "Ohje",
            "news_lab": "Uutiset",
            "about_lab": "Meistä",
        },
    }
    return table.get(
        key,
        {
            "help": "help",
            "news": "news",
            "about": "who-we-are",
            "help_lab": "Help",
            "news_lab": "News",
            "about_lab": "About",
        },
    )


def _facts(key: str) -> dict:
    d = HOSTS[key]
    dest = d.get("dest")
    cname, curl = customs_for(dest)
    return {
        "agent": "Kakobuy",
        "host": d["host"],
        "lang": d["lang"],
        "loc": _loc(key),
        "dest": dest,
        "dest_label": d["dest_label"],
        "ccy": currency_for(key, d),
        "customs": cname,
        "customs_url": curl,
        "storage": STORAGE,
        "estimator": EST,
        "official": OFFICIAL,
        "date": DATE,
        "email": d["mail"],
        "keep": d["keep"],
        "codes_off_title": [INVITE, COUPON, IKAKO],
        "strict_html_codes": True,
    }


def _locale_switcher(key: str, d: dict) -> str:
    u = ui_copy(_loc(key))
    rows = [
        (u["en_group"], [("ca", "kakospreadsheet.ca", "English (Canada)")]),
        (
            u["local_group"],
            [
                ("fi", "kakobuy.fi", "Suomi"),
                ("es", "kakospreadsheet.es", "Español (España)"),
                ("fr", "kakospreadsheet.fr", "Français (France)"),
                ("nl", "kakospreadsheet.nl", "Nederlands"),
            ],
        ),
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
        f"{escape(u['register_on'].format(brand='Kakobuy'))}</a></div>"
    )
    parts.append("</div></div>")
    return "".join(parts)


def _reg_lab(key: str) -> str:
    return {"fr": "S’inscrire", "es": "Registrarse", "nl": "Registreren", "fi": "Rekisteröidy"}.get(key, "Register")


def _nav(key: str, d: dict, page: str = "home") -> tuple[str, str, str, str]:
    t = _trust_paths(key)
    hp, np, ap = f"/{t['help']}/", f"/{t['news']}/", f"/{t['about']}/"
    sheet = "/kakobuy-spreadsheet/"
    coup = "/kakobuy-coupon/"
    home_lab = {"fr": "Accueil", "es": "Inicio", "nl": "Home", "fi": "Etusivu"}.get(key, "Home")
    items = [
        ("/", home_lab, page == "home"),
        (sheet, "Spreadsheet", page == "sheet"),
        (coup, {"es": "Cupones", "fi": "Kuponki"}.get(key, "Coupons"), page == "coupons"),
        (hp, t["help_lab"], page == "help"),
        (np, t["news_lab"], page == "news"),
        (ap, t["about_lab"], page == "about"),
        ("/#lab", {"fr": "Livraison", "es": "Envíos", "nl": "Verzending", "fi": "Toimitus"}.get(key, "Shipping"), page == "lab"),
    ]
    cta = {"fr": "Catalogue", "es": "Catálogo", "nl": "Catalogus", "fi": "Katalogi"}.get(key, "Catalogue")
    browse = {"fr": "Spreadsheet complète", "es": "Spreadsheet completa", "nl": "Volledige spreadsheet", "fi": "Koko spreadsheet"}.get(
        key, "Full spreadsheet"
    )
    nav = "".join(
        f'<a href="{escape(href)}"' + (' class="active"' if on else "") + f">{escape(lab)}</a>"
        for href, lab, on in items
    )
    w2c = f"{W2C}?utm_source={d['utm']}&utm_medium=desk&utm_campaign=kakobuy"
    return nav, cta, browse, w2c


def _chrome_head(key: str, d: dict, title: str, desc: str, path: str = "/") -> str:
    host = d["host"]
    if not path.startswith("/"):
        path = "/" + path
    canonical = f"https://{host}{path}"
    logo = d.get("logo") or "/assets/kakobuy-logo.png"
    ld = webpage_ld(url=canonical, name=title, desc=desc, lang=d["lang"], brand="Kakobuy", host=host)
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
<link rel="stylesheet" href="/assets/css/kakobuy-theme.css?v=20261001-home">
<link rel="icon" href="/assets/favicon.ico" type="image/x-icon">
{_hreflang()}
<style>{THEME_CSS}</style>
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
</head>
<body class="kakobuy-desk">
{skip_link(skip_label(loc))}
"""


def _header(key: str, d: dict, page: str = "home") -> str:
    nav, cta, browse, w2c = _nav(key, d, page=page)
    top = {
        "fr": f"Conçu pour la France · estimateur officiel · pas la Belgique · <a href=\"{w2c}\" target=\"_blank\" rel=\"noopener\">{browse} →</a>",
        "es": f"Escritorio ES independiente · no copiamos un recuento de líneas ajeno · <a href=\"{w2c}\" target=\"_blank\" rel=\"noopener\">{browse} →</a>",
        "nl": f"Voor een NL-adres · Nederlandse postcode · <a href=\"{w2c}\" target=\"_blank\" rel=\"noopener\">{browse} →</a>",
        "fi": f"Suomalainen osoite · Tulli · 00100 Helsinki · <a href=\"{w2c}\" target=\"_blank\" rel=\"noopener\">{browse} →</a>",
        "ca": f"Independent CA desk · CAD · CBSA · <a href=\"{w2c}\" target=\"_blank\" rel=\"noopener\">{browse} →</a>",
    }.get(key, f"Independent desk · {escape(d['badge'])} · <a href=\"{w2c}\" target=\"_blank\" rel=\"noopener\">{browse} →</a>")
    logo = d.get("logo") or "/assets/kakobuy-logo.png"
    return f"""<div class="topbar"><div class="container">{top}</div></div>
<header class="site-header">
  <div class="container header-inner">
    <a href="/" class="brand"><img class="brand-logo" src="{escape(logo)}" alt="Kakobuy" width="160" height="36"></a>
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
      <div class="footer-brand"><a href="/" class="brand"><img class="brand-logo" src="{escape(d.get('logo') or '/assets/kakobuy-logo.png')}" alt="Kakobuy"></a>
      <p>{escape(u['foot'].format(host=d['host'], brand='Kakobuy'))}</p>
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
        <li><a href="{OFFICIAL}">kakobuy.com</a></li>
      </ul></div>
      <div class="footer-col"><h5>{escape(u['contact'])}</h5><ul>
        <li><a href="mailto:{escape(d['mail'])}">{escape(d['mail'])}</a></li>
        <li><a href="/privacy-policy/">{escape(u['privacy'])}</a></li>
      </ul></div>
    </div>
    <p class="footer-locale-cluster" style="margin:12px 0;font-size:13px;color:#94A3B8">{escape(u['desks'])}:
      <a href="https://kakospreadsheet.ca/">Canada</a> ·
      <a href="https://kakobuy.fi/">Suomi</a> ·
      <a href="https://kakospreadsheet.es/">España</a> ·
      <a href="https://kakospreadsheet.fr/">France</a> ·
      <a href="https://kakospreadsheet.nl/">Nederland</a>
    </p>
    <div class="footer-bottom"><div>© 2026 {escape(d['host'])} · {escape(u['indep'])}</div></div>
  </div>
</footer>
<script>
(function(){{
  var b=document.querySelector('[data-mobile-toggle]');
  var n=document.getElementById('site-nav');
  if(b&&n) b.addEventListener('click', function(){{ n.classList.toggle('is-open'); }});
  var t=document.querySelector('[data-locale-toggle]');
  var p=document.querySelector('.locale-switcher-panel');
  if(t&&p) t.addEventListener('click', function(){{
    var hid=p.hasAttribute('hidden');
    if(hid) p.removeAttribute('hidden'); else p.setAttribute('hidden','');
    t.setAttribute('aria-expanded', hid?'true':'false');
  }});
}})();
</script>
</body></html>
"""


def _catalog(key: str) -> str:
    return catalog_block(key, HOSTS[key], register_url=REG, loc_fn=_loc, cat_labels=CAT_LABELS)


def _nine(key: str) -> str:
    rows_en = [
        ("Submitted", "You paid the goods plus China domestic."),
        ("Purchasing", "Kakobuy buys in the third-party shop."),
        ("Purchased", "The agent completed the China-side order."),
        ("Seller shipped", "The Chinese seller dispatched."),
        ("To warehouse / in storage", "Arrived at the Kakobuy warehouse."),
        ("QC / photos", "Warehouse inspection photos."),
        ("Can submit waybill", "Ready to book an international SKU. Storage clock: confirm official Help (copies quote 100 or 180 days)."),
        ("Parcel shipped", "International SKU left China."),
        ("Delivered", "Last-mile delivered; confirm in-app."),
    ]
    heads = {
        "es": ("Nueve estados (almacén)", "Help Center oficial 1 oct 2026: el reloj de almacén se confirma allí. Copias públicas citan 100 o 180 días — este desk no elige."),
        "fr": ("Neuf états (entrepôt)", "Help Center officiel 1 oct. 2026 : horloge d’entrepôt à confirmer. Copies publiques 100 ou 180 jours."),
        "nl": ("Negen statussen (magazijn)", "Officieel Help Center 1 okt 2026: opslagklok daar bevestigen. Kopieën noemen 100 of 180 dagen."),
        "fi": ("Yhdeksän tilaa (varasto)", "Virallinen Help Center 1. loka 2026: varastokello vahvistetaan siellä. Julkiset kopiot: 100 tai 180 päivää."),
    }
    h, n = heads.get(key, ("Nine states, warehouse", "Official Help Center 1 Oct 2026: confirm the live storage clock there. Public copies quote 100 or 180 days."))
    if key == "es":
        rows = [
            ("Submitted", "Producto + envío doméstico en China pagados."),
            ("Purchasing", "Kakobuy compra en la tienda."),
            ("Purchased", "Pedido en China hecho."),
            ("Seller shipped", "El vendedor envió."),
            ("To warehouse / in storage", "Llegó al almacén Kakobuy."),
            ("QC / photos", "Fotos de almacén."),
            ("Can submit waybill", "Listo para la SKU internacional. Reloj: ayuda oficial (copias 100 o 180 días)."),
            ("Parcel shipped", "Línea internacional salió."),
            ("Delivered", "Entregado."),
        ]
    elif key == "fr":
        rows = [
            ("Submitted", "Marchandise + domestique Chine payés."),
            ("Purchasing", "Kakobuy achète chez le vendeur."),
            ("Purchased", "Commande Chine passée."),
            ("Seller shipped", "Le vendeur a expédié."),
            ("To warehouse / in storage", "Arrivé à l’entrepôt Kakobuy."),
            ("QC / photos", "Photos d’entrepôt."),
            ("Can submit waybill", "Prêt pour la SKU internationale. Horloge: aide officielle (copies 100 ou 180 jours)."),
            ("Parcel shipped", "Ligne internationale partie."),
            ("Delivered", "Livré."),
        ]
    elif key == "nl":
        rows = [
            ("Submitted", "Product plus binnenlands China betaald."),
            ("Purchasing", "Kakobuy koopt in de Chinese shop."),
            ("Purchased", "China-order geplaatst."),
            ("Seller shipped", "Verkoper heeft verzonden."),
            ("To warehouse / in storage", "Aangekomen in het Kakobuy-magazijn."),
            ("QC / photos", "Magazijnfoto’s."),
            ("Can submit waybill", "Klaar voor de internationale SKU. Klok: officiële help (kopieën 100 of 180 dagen)."),
            ("Parcel shipped", "Internationale lijn vertrokken."),
            ("Delivered", "Bezorgd."),
        ]
    elif key == "fi":
        rows = [
            ("Submitted", "Tavara plus Kiinan kotimaan rahti maksettu."),
            ("Purchasing", "Kakobuy ostaa kaupasta."),
            ("Purchased", "Kiina-tilaus tehty."),
            ("Seller shipped", "Myyjä lähetti."),
            ("To warehouse / in storage", "Saapui Kakobuy-varastoon."),
            ("QC / photos", "Varastokuvat."),
            ("Can submit waybill", "Valmis kansainväliseen SKU:hun. Kello: virallinen ohje (kopiot 100 tai 180 päivää)."),
            ("Parcel shipped", "Kansainvälinen linja lähti."),
            ("Delivered", "Toimitettu."),
        ]
    else:
        rows = rows_en
    body = "".join(f"<tr><td><code>{escape(a)}</code></td><td>{escape(b)}</td></tr>" for a, b in rows)
    return f"""<section class="sg-sec" id="states"><h2>{escape(h)}</h2><p class="ssub">{escape(n)}</p>
<div class="tw"><table><thead><tr><th>State</th><th></th></tr></thead><tbody>{body}</tbody></table></div></section>"""


def _vol(key: str) -> str:
    title = {
        "fr": "Poids volumétrique (pas un prix)",
        "es": "Peso volumétrico (no es un precio)",
        "nl": "Volumgewicht (geen prijs)",
        "fi": "Tilavuuspaino (ei hinta)",
    }.get(key, "Volumetric weight (not a price)")
    note = {
        "fr": "Géométrie seule. L’argent est dans l’estimateur officiel. Souvent L×W×H/8000 en kg.",
        "es": "Solo geometría. El precio está en el estimador oficial. Casi siempre L×W×H/8000 en kg.",
        "nl": "Alleen meetkunde. De prijs staat in de officiële estimator. Meestal L×W×H/8000 in kg.",
        "fi": "Vain geometria. Raha on virallisessa arvioijassa. Usein P×L×K/8000 kilogrammoina.",
    }.get(key, "Geometry only. Live dollars sit in the official estimator. Most air SKUs divide by 8000 (result in kg).")
    vlab, blab = vol_js_labels(_loc(key))
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
  <p id="vol-out" style="margin-top:12px;background:{SOFT};padding:12px 14px;border-radius:10px"></p>
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
    if(el) el.innerHTML={json.dumps(vlab)}+' <b>'+vol+' g</b> · '+{json.dumps(blab)}+' <b>'+billed+' g</b> · not checkout.';
  }}
  ['vol-l','vol-w','vol-h','vol-g','vol-d'].forEach(function(id){{
    var n=document.getElementById(id); if(n) n.addEventListener(id==='vol-d'?'change':'input', sgVol);
  }});
  sgVol();
}})();
</script>
"""


def _faq_block(key: str, d: dict) -> str:
    h = {"fr": "Questions", "es": "Preguntas", "nl": "Vragen", "fi": "Kysymyksiä"}.get(key, "FAQ")
    items = []
    for i, (q, a) in enumerate(long_faqs(_facts(key))):
        op = " open" if i == 0 else ""
        items.append(f'<details class="sg-faq"{op}><summary>{escape(q)}</summary><p>{escape(a)}</p></details>')
    return f'<section class="sg-sec" id="faq"><h2>{h}</h2>{"".join(items)}</section>'


def _keep(key: str, d: dict) -> str:
    h, note = keep_copy(_loc(key))
    links = "".join(
        f'<a href="{escape(href)}"><strong>{escape(lab)}</strong><span> {escape(note)}</span></a>'
        for href, lab in d["keep"]
    )
    return f'<section class="sg-sec" id="kept"><h2>{escape(h)}</h2><div class="keep">{links}</div></section>'


def _lab(key: str, d: dict) -> str:
    c = lab_copy(_facts(key))
    return f"""<section class="sg-sec" id="lab"><h2>{escape(c["h2"])}</h2>
<p class="ssub">{c["ssub"]}</p>
<p><a class="btn btn-primary" href="{EST}">{escape(c["cta"])} →</a></p>
{_vol(key)}
</section>"""


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
    <img src="/media/official-home-20261001.jpg" alt="{escape(p['agent_cap'])}" width="1400" height="900" loading="lazy" decoding="async">
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
    <img src="/media/help-restricted-20261001.jpg" alt="{escape(p['rest_cap'])}" width="1400" height="900" loading="lazy" decoding="async">
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
    <img src="/media/estimator-20261001.jpg" alt="{escape(p['shot_est_cap'])}" width="1400" height="900" loading="lazy" decoding="async">
    <figcaption>{escape(p['shot_est_cap'])}</figcaption>
  </figure>
</section>
"""


def _help_meta(key: str, d: dict) -> dict:
    loc = d["locale"]
    dest = d["dest_label"]
    if key == "es":
        return {
            "title": "Ayuda: quince preguntas sobre Kakobuy en España",
            "desc": "Desk ES independiente: catálogo en inglés, almacén según Help oficial, estimador con destino España. Lab 1 oct 2026.",
            "h1": "Ayuda y preguntas frecuentes sobre Kakobuy en <em>español</em>",
            "lead": "Esta página vale para una calle española en este host. Pedidos solo en kakobuy.com.",
            "h2": "Las quince preguntas que más se repiten",
            "ask_h": "Dónde preguntar cuando esto no basta",
            "ask": "El chat de la app oficial. Los cupones siguen en /kakobuy-coupon/; el envío en /envio-kakobuy-espana/.",
        }
    if key == "fr":
        return {
            "title": "Aide : quinze questions sur Kakobuy en France",
            "desc": "Desk FR indépendant : catalogue anglais, estimateur vers la France. Lab 1 oct. 2026. Pas la Belgique.",
            "h1": "Aide et questions fréquentes sur Kakobuy en <em>France</em>",
            "lead": "Cette page vaut pour une adresse en France. Commandes seulement sur kakobuy.com.",
            "h2": "Les quinze questions qui reviennent",
            "ask_h": "Où demander si cela ne suffit pas",
            "ask": "Le chat de l’app officielle. /livraison-kakobuy/ et /avis-kakobuy/ restent.",
        }
    if key == "nl":
        return {
            "title": "Hulp: vijftien vragen over Kakobuy in Nederland",
            "desc": "Onafhankelijke NL-desk: Engelse catalogus, estimator naar Nederland. Lab 1 okt 2026.",
            "h1": "Hulp: vijftien vragen over Kakobuy in <em>Nederland</em>",
            "lead": "Deze pagina geldt voor een Nederlands adres. Orders alleen op kakobuy.com.",
            "h2": "De vijftien vragen die het vaakst terugkomen",
            "ask_h": "Waar vragen als dit niet volstaat",
            "ask": "De chat in de officiële app. /kakobuy-verzending/ blijft.",
        }
    if key == "fi":
        return {
            "title": "Ohje: viisitoista kysymystä Kakobuysta Suomessa",
            "desc": "Riippumaton FI-desk: englanninkielinen katalogi, arvioija kohti Suomea. Lab 1. loka 2026. Tulli.",
            "h1": "Ohje: viisitoista kysymystä Kakobuysta <em>Suomessa</em>",
            "lead": "Tämä sivu koskee suomalaista osoitetta tällä hostilla. Tilaukset vain kakobuy.comissa.",
            "h2": "Viisitoista kysymystä, jotka palaavat",
            "ask_h": "Mihin kysyä, jos tämä ei riitä",
            "ask": "Virallisen sovelluksen chat. /kakobuy-toimitus/ säilyy.",
        }
    return {
        "title": f"Help: fifteen questions about Kakobuy in {loc}",
        "desc": f"Independent desk: English catalogue, official estimator to {dest}. Lab 1 Oct 2026.",
        "h1": f"Help: fifteen questions about Kakobuy in <em>{escape(loc)}</em>",
        "lead": f"This page is for a {dest} address on this host. Orders and claims run only on kakobuy.com.",
        "h2": "The fifteen questions that come back most",
        "ask_h": "Where to ask when this is not enough",
        "ask": "Official in-app chat. Ranked coupon and customs URLs stay on this host.",
    }


def _news_meta(key: str, d: dict) -> dict:
    loc = d["locale"]
    dest = d["dest_label"]
    if key == "es":
        return {
            "title": "Novedades: lo que hemos comprobado en Kakobuy para España",
            "desc": "Notas con fecha de este desk ES. No copiamos un recuento de líneas ajeno. Lab 1 oct 2026.",
            "h1": "Qué hemos comprobado en la plataforma, <em>con fecha</em>",
            "lead": "Cada bloque es una medición de este host, no un recorte de hipobuy.es.",
            "how_h": "Cómo comprobamos las cosas",
            "how": "Homepage y /api/products/ de este host, el estimador oficial con destino España, y las URL que ya posicionan.",
        }
    if key == "fr":
        return {
            "title": "Actualités : ce que nous avons vérifié sur Kakobuy pour la France",
            "desc": "Notes datées du desk FR. Destination France, pas la Belgique. Lab 1 oct. 2026.",
            "h1": "Ce que nous avons vérifié sur la plateforme, <em>avec date</em>",
            "lead": "Chaque bloc est une mesure sur ce host.",
            "how_h": "Comment on vérifie",
            "how": "Accueil et /api/products/ de ce host, estimateur officiel vers la France.",
        }
    if key == "nl":
        return {
            "title": "Nieuws: wat we op Kakobuy voor Nederland hebben nagemeten",
            "desc": "Gedateerde notities van deze NL-desk. Lab 1 okt 2026.",
            "h1": "Wat we op het platform hebben nagemeten, <em>met datum</em>",
            "lead": "Elk blok is een meting op deze host.",
            "how_h": "Hoe we meten",
            "how": "Homepage en /api/products/ van deze host, officiële estimator naar Nederland.",
        }
    if key == "fi":
        return {
            "title": "Uutiset: mitä mittasimme Kakobuysta Suomelle",
            "desc": "Päivättyjä muistiinpanoja tältä FI-deskiltä. Lab 1. loka 2026. Tulli.",
            "h1": "Mitä mittasimme alustalta, <em>päivämäärällä</em>",
            "lead": "Jokainen lohko on mittaus tällä hostilla, ei toisen agentin rivimäärä.",
            "how_h": "Miten mittaamme",
            "how": "Etusivu ja /api/products/ tällä hostilla, virallinen arvioija kohti Suomea, rankkaavat URL:t paikallaan.",
        }
    return {
        "title": f"News: what we checked on Kakobuy for {loc}",
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
             "En el sitio oficial el símbolo puede pasar a EUR y las cifras seguir en dólares. Lee el número."),
            ("Check 3 · el estimador pide España, no este TLD",
             "Abrimos tools/estimate con destino España. No copiamos un recuento de líneas de otro agente."),
            ("Check 4 · reloj de almacén",
             "Help Center oficial 1 oct 2026: copias públicas citan 100 o 180 días. Este desk no elige un número."),
            ("Check 5 · URLs que ya posicionan",
             "/envio-kakobuy-espana/ y /kakobuy-opiniones/ se conservan."),
            ("Check 6 · 1 oct 2026 · SPA del estimador y página Sobre",
             "El HTML crudo de tools/estimate era una cáscara SPA. El navegador del 1 oct 2026 sí renderizó el formulario; captura en /media/."),
        ]
    if key == "fr":
        return [
            ("Check 1 · 1 oct. 2026 · catalogue sur cette accueil",
             f"Catalogue restauré sur / via {api}. La clé sneakers remplit la grille."),
            ("Check 2 · le sélecteur de devise ne convertit pas",
             "Le symbole peut passer en EUR et le chiffre rester en dollars."),
            ("Check 3 · l’estimateur veut la France",
             "Destination France, pas la Belgique, pas un TLD."),
            ("Check 4 · horloge d’entrepôt",
             "Aide officielle 1 oct. 2026 : copies publiques 100 ou 180 jours. Ce desk ne choisit pas."),
            ("Check 5 · URL déjà classées",
             "/livraison-kakobuy/ et /avis-kakobuy/ restent."),
            ("Check 6 · 1 oct. 2026 · SPA estimateur",
             "tools/estimate est un SPA. Capture du formulaire dans /media/."),
        ]
    if key == "nl":
        return [
            ("Check 1 · 1 okt 2026 · catalogus op deze homepage",
             f"Catalogus terug op / via {api}. Engels sneakers vult het raster."),
            ("Check 2 · valutaswitcher rekent niet om",
             "Het symbool kan EUR worden terwijl het cijfer dollar blijft."),
            ("Check 3 · estimator naar Nederland",
             "Officiële estimator met bestemming Nederland. Nederlandse postcode."),
            ("Check 4 · opslagklok",
             "Officiële help 1 okt 2026: kopieën noemen 100 of 180 dagen."),
            ("Check 5 · URL’s die al ranken",
             "/kakobuy-verzending/ en /kakobuy-ervaringen/ blijven."),
            ("Check 6 · 1 okt 2026 · SPA-estimator",
             "tools/estimate is een SPA. Opname in /media/."),
        ]
    if key == "fi":
        return [
            ("Check 1 · 1. loka 2026 · katalogi tällä etusivulla",
             f"Katalogi takaisin / kautta {api}. Englanti sneakers täyttää ruudukon; lenkkarit usein 0."),
            ("Check 2 · valuuttakytkin ei muunna",
             "Merkki voi vaihtua EUR:ksi ja numero jäädä dollareiksi. Lue luku."),
            ("Check 3 · arvioija kohti Suomea",
             "Virallinen arvioija kohteella FI, postinumero kuten 00100 Helsinki. Ei Ruotsi, ei EU."),
            ("Check 4 · varastokello",
             "Virallinen Help 1. loka 2026: julkiset kopiot 100 tai 180 päivää. Tämä desk ei valitse."),
            ("Check 5 · jo rankkaavat URL:t",
             "/kakobuy-toimitus/, /kakobuy-kokemuksia/ ja /kakobuy-suomi/ säilyvät."),
            ("Check 6 · 1. loka 2026 · SPA-arvioija",
             "tools/estimate on SPA. Lomakkeen kuvakaappaus /media/-kansiossa."),
        ]
    extra = "The ranked CBSA article at /kakobuy-shipping-to-canada/ stays. US notes stay on kakobuytips.com."
    return [
        ("Check 1 · 1 Oct 2026 · catalogue on this homepage",
         f"Catalogue restored on / via {api}. English key sneakers fills the grid; local words often return zero."),
        ("Check 2 · currency switcher does not convert",
         "On the official site the symbol can change while the digits stay dollars. Read the number."),
        (f"Check 3 · estimator destination {dest}",
         f"Open kakobuy.com/tools/estimate with {dest}. A US ZIP is the wrong country. We do not paste another agent’s line count."),
        ("Check 4 · warehouse clock",
         "Official Help Center 1 Oct 2026: public copies quote 100 days from in-storage and 180 days. This desk does not pick a number."),
        ("Check 5 · ranked URLs kept", extra),
        ("Check 6 · 1 Oct 2026 · SPA estimator and About page",
         "Raw HTML of tools/estimate was a SPA shell. The 1 Oct 2026 browser rendered the form; capture lives under /media/. /who-we-are/ is its own page."),
    ]


def build_help(key: str) -> str:
    d = HOSTS[key]
    t = _trust_paths(key)
    m = _help_meta(key, d)
    faqs = long_faqs(_facts(key))
    html = _chrome_head(key, d, m["title"], m["desc"], path=f"/{t['help']}/")
    html = inject_jsonld(
        html,
        faq_ld(d["lang"], faqs),
        breadcrumb_ld([("Home", f"https://{d['host']}/"), (t["help_lab"], f"https://{d['host']}/{t['help']}/")]),
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
  <p><a class="btn btn-outline" href="#local">{escape(local_cta(_facts(key)))}</a></p>
</section>
"""
    html += local_guide_html(_facts(key))
    html += f"""<section class="sg-sec" id="faq"><h2>{escape(m['h2'])}</h2>{''.join(items)}</section>
<section class="sg-sec"><h2>{escape(m['ask_h'])}</h2><p class="ssub">{escape(m['ask'])}</p>
<p><a class="btn btn-primary" href="{REG}" target="_blank" rel="noopener sponsored">{escape(_reg_lab(key))}</a>
<a class="btn btn-outline" href="/">← /</a></p></section>
"""
    html += _footer(key, d)
    return html


def build_news(key: str) -> str:
    d = HOSTS[key]
    t = _trust_paths(key)
    m = _news_meta(key, d)
    news_items = _news_items(key, d)
    html = _chrome_head(key, d, m["title"], m["desc"], path=f"/{t['news']}/")
    html = inject_jsonld(
        html,
        itemlist_ld(url=f"https://{d['host']}/{t['news']}/", name=m["title"], items=news_items),
        breadcrumb_ld([("Home", f"https://{d['host']}/"), (t["news_lab"], f"https://{d['host']}/{t['news']}/")]),
    )
    html += _header(key, d, page="news")
    blocks = [f'<article class="sg-sec"><h2>{escape(h)}</h2><p class="ssub">{escape(p)}</p></article>' for h, p in news_items]
    html += f"""<section class="sg-hero">
  <div class="hbg">Lab {DATE} · {escape(t['news_lab'])}</div>
  <h1>{m['h1']}</h1>
  <p class="hsub">{escape(m['lead'])}</p>
  <p class="eu-badge">{escape(d['badge'])}</p>
</section>
{''.join(blocks)}
<section class="sg-sec"><h2>{escape(m['how_h'])}</h2><p class="ssub">{escape(m['how'])}</p>
<p><a class="btn btn-outline" href="/{t['help']}/">{escape(t['help_lab'])}</a>
<a class="btn btn-outline" href="/">← /</a></p></section>
"""
    html += _footer(key, d)
    return html


def build_about(key: str) -> str:
    d = HOSTS[key]
    t = _trust_paths(key)
    p = _trust_pack(key, d)
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
        breadcrumb_ld([("Home", f"https://{d['host']}/"), (t["about_lab"], f"https://{d['host']}/{t['about']}/")]),
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
  <a class="btn btn-primary" href="{REG}" target="_blank" rel="noopener sponsored">{escape(_reg_lab(key))}</a></p>
</article>
"""
    html += _footer(key, d)
    return html


def build_home(key: str) -> str:
    d = HOSTS[key]
    m = HOME_META[key]
    html = _chrome_head(key, d, m["title"], m["desc"])
    html += _header(key, d)
    cat_lab = {"fr": "Catalogue", "es": "Catálogo", "nl": "Catalogus", "fi": "Katalogi"}.get(key, "Catalogue")
    est_lab = {"fr": "Estimateur", "es": "Estimador", "nl": "Estimator", "fi": "Arvioija"}.get(key, "Estimator")
    html += f"""<section class="sg-hero">
  <div class="hbg">Lab {DATE}</div>
  <h1>{m["h1"]}</h1>
  <p class="hsub">{m["hsub"]}</p>
  <p class="eu-badge">{escape(d["badge"])}</p>
  <div class="sg-ctas">
    <a class="btn btn-primary" href="#catalog">{escape(cat_lab)}</a>
    <a class="btn btn-outline" href="#local">{escape(local_cta(_facts(key)))}</a>
    <a class="btn btn-outline" href="{EST}">{escape(est_lab)}</a>
    <a class="btn btn-outline" href="{REG}" target="_blank" rel="noopener sponsored">{escape(_reg_lab(key))}</a>
  </div>
</section>
"""
    html += local_guide_html(_facts(key))
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
    return len(re.findall(r"[A-Za-zÀ-ÿÄÖäöÅå]{3,}", html))


def _codes_in(html: str) -> bool:
    return INVITE in html or COUPON in html or IKAKO in html


def _validate() -> None:
    for key, d in HOSTS.items():
        html = build_home(key)
        title = re.search(r"<title>(.*?)</title>", html, flags=re.S).group(1)
        if _codes_in(html):
            raise SystemExit(f"{key}: invite/coupon leaked into generated HTML")
        if "Georgia" in html or "gsc-editor-notes" in html:
            raise SystemExit(f"{key}: junk/Georgia leftover")
        if "#00C853" in html or "#ffc400" in html:
            raise SystemExit(f"{key}: HipoBuy green / LitBuy yellow leaked")
        if "Packing Center" in html:
            raise SystemExit(f"{key}: SugarGoo packing-center leaked")
        for tok in (
            'id="local"',
            'id="catalog"',
            'id="states"',
            'id="vol-calc"',
            'id="faq"',
            'id="agent"',
            'id="sheet-explain"',
            'id="restricted"',
            'id="cat-wall"',
            'id="shots"',
            "kakobuy-theme.css",
            "/api/products/",
            "/img/cat/sneakers.jpg",
            "/media/estimator-20261001.jpg",
            "/media/official-home-20261001.jpg",
            EST,
        ):
            if tok not in html:
                raise SystemExit(f"{key}: missing {tok}")
        ccy = currency_for(key, d)
        if f'var FX_CCY="{ccy}"' not in html:
            raise SystemExit(f"{key}: missing local FX {ccy}")
        for e in validate_desk(html, _facts(key), page="home"):
            raise SystemExit(f"{key}/home template: {e}")
        ncat = len(re.findall(r'class="sg-cat"', html))
        if ncat != 16:
            raise SystemExit(f"{key}: cat wall {ncat}")
        pack = dest_local_pack(d["dest"])
        if pack["fingerprint"] not in html:
            raise SystemExit(f"{key}: missing fingerprint {pack['fingerprint']}")
        t = _trust_paths(key)
        help_html = build_help(key)
        news_html = build_news(key)
        about_html = build_about(key)
        for label, page in (("help", help_html), ("news", news_html), ("about", about_html)):
            if _codes_in(page):
                raise SystemExit(f"{key} {label}: code leaked")
            if "Georgia" in page or "#00C853" in page or "#ffc400" in page:
                raise SystemExit(f"{key} {label}: junk chrome")
        for e in validate_desk(help_html, _facts(key), page="help"):
            raise SystemExit(f"{key}/help template: {e}")
        for e in validate_desk(news_html, _facts(key), page="news"):
            raise SystemExit(f"{key}/news template: {e}")
        for e in validate_desk(about_html, _facts(key), page="about"):
            raise SystemExit(f"{key}/about template: {e}")
        if key == "fr" and ("Belgique" in title or "Belgium" in title):
            raise SystemExit("fr title became Belgium")
        if key == "fi" and "00100 Helsinki" not in html:
            raise SystemExit("fi missing Helsinki fingerprint")
        if key == "ca" and "form A1A 1A1" not in html:
            raise SystemExit("ca missing postal fingerprint")
        n = _wc(html)
        print(f"{'OK' if n>=600 else 'SHORT':5} {key}/home words={n} cats={ncat} {title[:56]}")
        print(f"OK    {key}/help words={_wc(help_html)}")
        print(f"OK    {key}/news words={_wc(news_html)}")
        print(f"OK    {key}/about words={_wc(about_html)}")
        if n < 500:
            raise SystemExit(f"{key} too short")
        if f"/{t['help']}/" not in html:
            raise SystemExit(f"{key}: home missing help nav")


def _overlay_files(key: str) -> list[tuple[Path, str]]:
    d = HOSTS[key]
    t = _trust_paths(key)
    host_root = OUT / d["host"] / "overlay"
    return [
        (host_root / "index.html", build_home(key)),
        (host_root / t["help"] / "index.html", build_help(key)),
        (host_root / t["news"] / "index.html", build_news(key)),
        (host_root / t["about"] / "index.html", build_about(key)),
    ]


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


ORDER = ["ca", "fi", "es", "fr", "nl"]
DOCS_HOST = "kakobuydocs.com"


def _only() -> list[str]:
    if "--only" not in sys.argv:
        return list(ORDER)
    i = sys.argv.index("--only")
    if i + 1 >= len(sys.argv):
        raise SystemExit("usage: --only ca,fi")
    keys = [k.strip() for k in sys.argv[i + 1].split(",") if k.strip()]
    bad = [k for k in keys if k not in HOSTS]
    if bad:
        raise SystemExit(f"unknown --only {bad}")
    return keys


def _sitemap_insert(client, host: str, slugs: list[str]) -> None:
    path = f"/www/wwwroot/{host}/sitemap.xml"
    raw = _run(client, f"python3 -c \"print(open({path!r}).read() if __import__('os').path.isfile({path!r}) else '')\"")
    if "</urlset>" not in raw:
        print("skip sitemap", host)
        return
    chunk = raw
    added = 0
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
    with sftp.open(path, "w") as fh:
        fh.write(chunk)
    sftp.close()
    print("sitemap +", added, host)


def _put_assets(client, sftp, host: str) -> None:
    media_local = SHARED / "media"
    cat_local = SHARED / "img" / "cat"
    theme_local = SHARED / "kakobuy-theme.css"
    _run(client, f"mkdir -p '/www/wwwroot/{host}/media' '/www/wwwroot/{host}/img/cat' '/www/wwwroot/{host}/assets/css' '/www/wwwroot/{host}/api/products'")
    if theme_local.is_file():
        sftp.put(str(theme_local), f"/www/wwwroot/{host}/assets/css/kakobuy-theme.css")
        print("PUT theme", host)
    for src in sorted(media_local.glob("*.jpg")):
        remote = f"/www/wwwroot/{host}/media/{src.name}"
        sftp.put(str(src), remote)
        print("PUT", remote, "bytes", src.stat().st_size)
    for src in sorted(cat_local.glob("*.jpg")):
        remote = f"/www/wwwroot/{host}/img/cat/{src.name}"
        sftp.put(str(src), remote)
    php_remote = f"/www/wwwroot/{host}/api/products/index.php"
    with sftp.open(php_remote, "w") as fh:
        fh.write(PRODUCTS_PHP)
    print("PUT", php_remote)
    _run(
        client,
        f"chown -R www:www '/www/wwwroot/{host}/media' '/www/wwwroot/{host}/img' "
        f"'/www/wwwroot/{host}/assets/css' '/www/wwwroot/{host}/api/products' "
        f"&& find '/www/wwwroot/{host}/media' '/www/wwwroot/{host}/img' "
        f"'/www/wwwroot/{host}/assets/css' '/www/wwwroot/{host}/api/products' -type f -exec chmod 644 {{}} +",
    )


def _fix_api_nginx(client, hosts: list[str]) -> None:
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
    for host in hosts:
        path = f"/www/server/panel/vhost/nginx/{host}.conf"
        raw = _run(client, f"cat '{path}'")
        if "rewrite ^/api/([^/]+)/?$ /api/$1/index.php last" in raw:
            print("ok", host, "api rewrite")
            continue
        if old not in raw:
            print("skip", host, "api block mismatch")
            continue
        bak = f"/www/backup/kakobuy-nginx-{host}.conf"
        _run(client, f"cp -a '{path}' '{bak}'")
        sftp = client.open_sftp()
        with sftp.open(path, "w") as fh:
            fh.write(raw.replace(old, new, 1))
        sftp.close()
        print("PATCH", path)
        changed += 1
    if changed:
        print(_run(client, "nginx -t && nginx -s reload"))


def _docs_facts() -> dict:
    cname, curl = customs_for(None)
    return {
        "agent": "Kakobuy",
        "host": DOCS_HOST,
        "lang": "en",
        "loc": "en",
        "dest": None,
        "dest_label": "a country in the estimator",
        "ccy": "USD",
        "customs": cname,
        "customs_url": curl,
        "storage": STORAGE,
        "estimator": EST,
        "official": OFFICIAL,
        "date": DATE,
        "keep": [
            ("/kakobuy-shoes-spreadsheet/", "Shoes spreadsheet (ranked)"),
            ("/how-to-use-kakobuy/", "How-to (ranked)"),
            ("/kakobuy-spreadsheet/", "Full spreadsheet"),
            ("/kakobuy-coupons/", "Coupons article"),
        ],
    }


def _patch_docs_home(html: str) -> str:
    """Surgical hub #local. Keep ranked inner copy and existing Georgia chrome."""
    facts = _docs_facts()
    block = local_guide_html(facts)
    if 'id="local"' in html:
        html = re.sub(r'<section class="sg-sec" id="local".*?</section>', block, html, count=1, flags=re.S)
        return html
    if "<main>" in html:
        html = html.replace("<main>", "<main>\n" + block, 1)
    else:
        html = html.replace("<body>", "<body>\n" + skip_link(skip_label("en")) + block, 1)
    if "#local{scroll-margin-top" not in html:
        html = html.replace("</style>", SKIP_CSS + "</style>", 1)
    if 'href="#main"' not in html and "href='#main'" not in html:
        html = html.replace("<body>", "<body>\n" + skip_link(skip_label("en")), 1)
        if 'id="main"' not in html:
            html = html.replace("<main>", '<main id="main">', 1)
    return html


def _put_docs(client, sftp, bak: str) -> None:
    remote = f"/www/wwwroot/{DOCS_HOST}/index.html"
    raw = _run(client, f"cat '{remote}'")
    if not raw:
        print("skip docs: empty")
        return
    patched = _patch_docs_home(raw)
    pack = dest_local_pack(None)
    if pack["fingerprint"] not in patched:
        raise SystemExit("docs surgical missing hub fingerprint")
    if 'id="local"' not in patched:
        raise SystemExit("docs surgical missing #local")
    _run(client, f"cp -a '{remote}' '{bak}/{DOCS_HOST}-index.html'")
    with sftp.open(remote, "w") as fh:
        fh.write(patched)
    _run(client, f"chown www:www '{remote}' && chmod 644 '{remote}'")
    print("PUT surgical", remote, "bytes", len(patched.encode()))


def main() -> None:
    _validate()
    SHARED.mkdir(parents=True, exist_ok=True)
    (SHARED / "kakobuy-theme.css").write_text(THEME_CSS, encoding="utf-8")
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
    bak = f"/www/backup/kakobuy-desks-{stamp}"
    print(_run(client, f"mkdir -p '{bak}'"))
    uploaded = []
    for key in put_keys:
        d = HOSTS[key]
        t = _trust_paths(key)
        mapping = [
            (OUT / d["host"] / "overlay" / "index.html", f"/www/wwwroot/{d['host']}/index.html"),
            (OUT / d["host"] / "overlay" / t["help"] / "index.html", f"/www/wwwroot/{d['host']}/{t['help']}/index.html"),
            (OUT / d["host"] / "overlay" / t["news"] / "index.html", f"/www/wwwroot/{d['host']}/{t['news']}/index.html"),
            (OUT / d["host"] / "overlay" / t["about"] / "index.html", f"/www/wwwroot/{d['host']}/{t['about']}/index.html"),
        ]
        for local, remote in mapping:
            rdir = remote.rsplit("/", 1)[0]
            _run(client, f"mkdir -p '{rdir}'")
            _run(client, f"test -f '{remote}' && cp -a '{remote}' '{bak}/{d['host']}-{remote.strip('/').replace('/', '_')}' || true")
            sftp.put(str(local), remote)
            uploaded.append(remote)
            print("PUT", remote, "bytes", local.stat().st_size)
        _put_assets(client, sftp, d["host"])
        _sitemap_insert(client, d["host"], [t["help"], t["news"], t["about"]])
    if "--skip-docs" not in sys.argv:
        _put_docs(client, sftp, bak)
    if uploaded:
        _run(
            client,
            "chown www:www "
            + " ".join(f"'{p}'" for p in uploaded)
            + " && chmod 644 "
            + " ".join(f"'{p}'" for p in uploaded),
        )
    print("backup", bak, "put", ",".join(put_keys))
    _fix_api_nginx(client, [HOSTS[k]["host"] for k in put_keys])
    sftp.close()
    client.close()


if __name__ == "__main__":
    main()
