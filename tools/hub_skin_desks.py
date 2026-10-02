#!/usr/bin/env python3
"""Rebuild 48 Georgia one-pager dests as agent-branded CMS homepages.

Uses each agent's logo + primary color (and leftover theme CSS on disk).
Does not PUT 5KB Georgia overlays. Does not overwrite ranked inner HTML.
"""
from __future__ import annotations

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
    CUSTOMS,
    breadcrumb_ld,
    faq_ld,
    independence_copy,
    inject_jsonld,
    itemlist_ld,
    lab_copy,
    local_cta,
    local_guide_html,
    long_faqs,
    organization_ld,
    skip_link,
    skip_label,
    validate_desk,
    webpage_ld,
)

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "sites"
DATE = "2 Oct 2026"
CMS_CSS = OUT / "shared" / "desk-cms.css"

AGENTS = {
    "AllChinaBuy": {
        "primary": "#E87000",
        "soft": "#FFF3E0",
        "nav": "#111111",
        "logo": "/assets/images/allchinabuy-wordmark.png",
        "official": "https://www.acbuy.com/",
        "estimator": "https://www.acbuy.com/estimation/",
        "register": "https://www.acbuy.com/",
        "storage": "Official ACBuy Help: 90 free warehouse days; confirm that article the morning you ship",
        "codes": ["5F2RRA", "EwjrSk", "ACBUY5"],
        "css": ["/assets/css/desk-cms.css", "/assets/css/allchinabuy-theme.css"],
    },
    "ACBuy": {
        "primary": "#E87000",
        "soft": "#FFF3E0",
        "nav": "#111111",
        "logo": "/assets/images/acbuy-wordmark.png",
        "official": "https://www.acbuy.com/",
        "estimator": "https://www.acbuy.com/estimation/",
        "register": "https://www.acbuy.com/",
        "storage": "Official ACBuy Help: 90 free warehouse days; confirm that article the morning you ship",
        "codes": ["5F2RRA", "EwjrSk", "ACBUY5"],
        "css": ["/assets/css/desk-cms.css", "/assets/css/allchinabuy-theme.css"],
    },
    "BBDBuy": {
        "primary": "#2563eb",
        "soft": "#eff6ff",
        "nav": "#0f172a",
        "logo": "/assets/images/bbdbuy-logo.png",
        "official": "https://www.bbdbuy.com/",
        "estimator": "https://www.bbdbuy.com/estimation",
        "register": "https://www.bbdbuy.com/",
        "storage": "Confirm live BBDBuy Help the morning you ship; do not treat a second public figure as official",
        "codes": [],
        "css": ["/assets/css/desk-cms.css", "/assets/css/bbdbuy-theme.css"],
    },
    "CSSBuy": {
        "primary": "#E85D1A",
        "soft": "#fff4ed",
        "nav": "#1a1a1a",
        "logo": "/assets/images/cssbuy-logo.png",
        "official": "https://www.cssbuy.com/",
        "estimator": "https://www.cssbuy.com/?action=estimates&go=page",
        "register": "https://www.cssbuy.com/",
        "storage": "Official CSSBuy warehouse FAQ: 90 free days from In Warehouse, then ¥15/order/month; confirm Help the morning you ship",
        "codes": ["1Yi9"],
        "css": ["/assets/css/desk-cms.css", "/assets/css/cssbuy-site.css"],
    },
    "FansBuy": {
        "primary": "#7c3aed",
        "soft": "#f5f3ff",
        "nav": "#1e1b4b",
        "logo": "/assets/images/fansbuy-wordmark.png",
        "official": "https://fansbuy.com/",
        "estimator": "https://fansbuy.com/estimates",
        "register": "https://fansbuy.com/",
        "storage": "Official Help: 90 free warehouse days; confirm that article the morning you ship",
        "codes": [],
        "css": ["/assets/css/desk-cms.css", "/assets/css/fansbuy-theme.css"],
    },
    "LoveGoBuy": {
        "primary": "#e91e12",
        "soft": "#fff0ee",
        "nav": "#131926",
        "logo": "/assets/images/lovegobuy-logo.png",
        "official": "https://www.lovegobuy.com/",
        "estimator": "https://www.lovegobuy.com/shipping/estimation/index",
        "register": "https://www.lovegobuy.com/",
        "storage": "Public copies disagree on free warehouse days; confirm live LoveGoBuy Help the morning you ship",
        "codes": [],
        "css": ["/assets/css/desk-cms.css", "/assets/css/lovegobuy-theme.css"],
    },
    "MuleBuy": {
        "primary": "#9456ff",
        "soft": "#f5f0ff",
        "nav": "#191a1f",
        "logo": "/assets/images/mulebuy-wordmark.png",
        "official": "https://mulebuy.com/",
        "estimator": "https://mulebuy.com/estimation/",
        "register": "https://mulebuy.com/",
        "storage": "Official blog: 90 free warehouse days; confirm live Help the morning you ship",
        "codes": [],
        "css": ["/assets/css/desk-cms.css", "/assets/css/mulebuy-theme.css"],
    },
    "MyCNBox": {
        "primary": "#0f766e",
        "soft": "#f0fdfa",
        "nav": "#134e4a",
        "logo": "/assets/images/mycnbox-logo.png",
        "official": "https://www.mycnbox.com/",
        "estimator": "https://www.mycnbox.com/estimation/",
        "register": "https://www.mycnbox.com/",
        "storage": "Official Help: 90 free warehouse days; confirm that article the morning you ship",
        "codes": [],
        "css": ["/assets/css/desk-cms.css", "/assets/css/mycnbox-theme.css"],
    },
    "OOPBuy": {
        "primary": "#2563eb",
        "soft": "#eff6ff",
        "nav": "#1e3a8a",
        "logo": "/assets/images/oopbuy-wordmark.png",
        "official": "https://oopbuy.com/",
        "estimator": "https://oopbuy.com/estimation",
        "register": "https://oopbuy.com/",
        "storage": "Official OOPBuy Help is the live site; confirm storage there the morning you ship",
        "codes": [],
        "css": ["/assets/css/desk-cms.css", "/assets/css/oopbuy-theme.css"],
    },
    "OOTDBuy": {
        "primary": "#111111",
        "soft": "#f5f5f4",
        "nav": "#0a0a0a",
        "logo": "/assets/images/ootdbuy-logo.png",
        "official": "https://ootdbuy.com/",
        "estimator": "https://ootdbuy.com/estimation/",
        "register": "https://ootdbuy.com/",
        "storage": "Official Help Center warehouse notice; confirm it the morning you ship",
        "codes": [],
        "css": ["/assets/css/desk-cms.css", "/assets/css/ootdbuy-theme.css"],
    },
    "OrientDig": {
        "primary": "#f7931e",
        "soft": "#fff4e8",
        "nav": "#272121",
        "logo": "/assets/images/orientdig-logo.png",
        "official": "https://orientdig.com/",
        "estimator": "https://orientdig.com/estimation/",
        "register": "https://orientdig.com/",
        "storage": "Official Help: 90 days from stored in warehouse; confirm that article the morning you ship",
        "codes": ["100246065"],
        "css": ["/assets/css/desk-cms.css", "/assets/css/orientdig-theme.css"],
    },
    "Superbuy": {
        "primary": "#ff1733",
        "soft": "#fff6f7",
        "nav": "#1b1b1b",
        "logo": "/assets/images/superbuy-logo.png",
        "official": "https://www.superbuy.com/",
        "estimator": "https://www.superbuy.com/en/page/query/freight/",
        "register": "https://www.superbuy.com/",
        "storage": "Official fee-composition guide: 90 free warehouse days; confirm Help the morning you ship",
        "codes": [],
        "css": ["/assets/css/desk-cms.css", "/assets/css/superbuy-theme.css"],
    },
    "USFans": {
        "primary": "#ff4800",
        "soft": "#fff4ed",
        "nav": "#202b40",
        "logo": "/assets/images/usfans-wordmark.png",
        "official": "https://usfans.com/",
        "estimator": "https://usfans.com/estimation",
        "register": "https://usfans.com/",
        "storage": "Official Help Center → goods storage period; confirm that article the morning you ship",
        "codes": [],
        "css": ["/assets/css/desk-cms.css", "/assets/css/usfans-theme.css"],
    },
}

CATS = [
    ("sneakers", "Sneakers"),
    ("hoodie", "Hoodie"),
    ("jacket", "Jacket"),
    ("t-shirt", "T-shirt"),
    ("pants", "Pants"),
    ("bag", "Bags"),
    ("watch", "Watches"),
    ("accessories", "Accessories"),
    ("shoes", "Shoes"),
    ("boots", "Boots"),
    ("hat", "Hats"),
    ("glasses", "Glasses"),
    ("jewelry", "Jewelry"),
    ("electronics", "Electronics"),
    ("perfume", "Fragrance"),
    ("sports", "Sports"),
]


def D(**kw):
    return kw


HOSTS = {
    "allchinabuyspreadsheet.ca": D(agent="AllChinaBuy", dest="CA", loc="en", lang="en-CA", ccy="CAD", dest_label="Canada",
        title="AllChinaBuy Canada — CAD, Canada Post, CBSA notes",
        h1="AllChinaBuy for a Canadian delivery address",
        keep=[("/allchinabuy-shipping-guide/", "Shipping"), ("/is-allchinabuy-legit/", "Is it legit?"), ("/allchinabuy-spreadsheet/", "Spreadsheet"), ("/allchinabuy-coupons/", "Coupons")]),
    "allchinabuyspreadsheets.co.uk": D(agent="AllChinaBuy", dest="GB", loc="en", lang="en-GB", ccy="GBP", dest_label="the United Kingdom",
        title="AllChinaBuy UK — GBP, Royal Mail, HMRC notes",
        h1="AllChinaBuy for a UK delivery address",
        keep=[("/allchinabuy-shipping-guide/", "Shipping"), ("/is-allchinabuy-legit/", "Is it legit?"), ("/allchinabuy-spreadsheet/", "Spreadsheet"), ("/allchinabuy-coupons/", "Coupons")]),
    "acbuyspreadsheets.nl": D(agent="ACBuy", dest="NL", loc="nl", lang="nl-NL", ccy="EUR", dest_label="Nederland",
        title="ACBuy Nederland — Nederlandse postcode, geen Duitse automaat",
        h1="ACBuy voor een Nederlands adres",
        keep=[("/is-acbuy-legit/", "Review"), ("/acbuy-shipping-guide/", "Verzending"), ("/acbuy-coupons/", "Coupons"), ("/how-to-use-acbuy/", "Handleiding")]),
    "bbdbuy.ca": D(agent="BBDBuy", dest="CA", loc="en", lang="en-CA", ccy="CAD", dest_label="Canada",
        title="BBDBuy Canada — CAD, Canada Post, CBSA notes",
        h1="BBDBuy for a Canadian delivery address",
        keep=[("/bbdbuy-shipping/", "Shipping"), ("/is-bbdbuy-legit/", "Is it legit?"), ("/bbdbuy-coupons/", "Coupons"), ("/bbdbuy-spreadsheet/", "Spreadsheet")]),
    "bbdbuy.it": D(agent="BBDBuy", dest="IT", loc="it", lang="it-IT", ccy="EUR", dest_label="l’Italia",
        title="BBDBuy Italia — Poste Italiane, IVA, QC",
        h1="BBDBuy per un indirizzo in Italia",
        keep=[("/bbdbuy-qc/", "QC"), ("/bbdbuy-shipping/", "Spedizione"), ("/bbdbuy-spreadsheet/", "Spreadsheet"), ("/how-to-use-bbdbuy/", "Come funziona")]),
    "bbdbuy.uk": D(agent="BBDBuy", dest="GB", loc="en", lang="en-GB", ccy="GBP", dest_label="the United Kingdom",
        title="BBDBuy UK — GBP, Royal Mail, HMRC notes",
        h1="BBDBuy for a UK delivery address",
        keep=[("/bbdbuy-shipping/", "Shipping"), ("/how-to-use-bbdbuy/", "How to use"), ("/bbdbuy-coupons/", "Coupons"), ("/is-bbdbuy-legit/", "Is it legit?")]),
    "bbdbuy.us": D(agent="BBDBuy", dest="US", loc="en", lang="en-US", ccy="USD", dest_label="the United States",
        title="BBDBuy United States — USD, USPS, CBP notes",
        h1="BBDBuy for a US delivery address",
        keep=[("/bbdbuy-shipping/", "Shipping"), ("/how-to-use-bbdbuy/", "How to use"), ("/bbdbuy-qc/", "QC"), ("/bbdbuy-spreadsheet/", "Spreadsheet")]),
    "bbdbuyspreadsheet.de": D(agent="BBDBuy", dest="DE", loc="de", lang="de-DE", ccy="EUR", dest_label="Deutschland",
        title="BBDBuy Deutschland — Packstation, DHL, Zoll",
        h1="BBDBuy für eine deutsche Lieferadresse",
        keep=[("/bbdbuy-shipping/", "Versand"), ("/how-to-use-bbdbuy/", "Anleitung"), ("/bbdbuy-spreadsheet/", "Spreadsheet"), ("/is-bbdbuy-legit/", "Seriös?")]),
    "cssbuyspreadsheet.ca": D(agent="CSSBuy", dest="CA", loc="en", lang="en-CA", ccy="CAD", dest_label="Canada",
        title="CSSBuy Canada — CAD, Canada Post, CBSA notes",
        h1="CSSBuy for a Canadian delivery address",
        keep=[("/spreadsheet/", "Spreadsheet"), ("/faq/", "FAQ"), ("/guides/", "Guides"), ("/guides/shipping/", "Shipping")]),
    "cssbuyspreadsheet.uk": D(agent="CSSBuy", dest="GB", loc="en", lang="en-GB", ccy="GBP", dest_label="the United Kingdom",
        title="CSSBuy UK — GBP, Royal Mail, HMRC notes",
        h1="CSSBuy for a UK delivery address",
        keep=[("/spreadsheet/", "Spreadsheet"), ("/faq/", "FAQ"), ("/guides/", "Guides"), ("/guides/shipping/", "Shipping")]),
    "cssbuyspreadsheets.de": D(agent="CSSBuy", dest="DE", loc="de", lang="de-DE", ccy="EUR", dest_label="Deutschland",
        title="CSSBuy Deutschland — Packstation, DHL, Zoll",
        h1="CSSBuy für eine deutsche Lieferadresse",
        keep=[("/spreadsheet/", "Spreadsheet"), ("/faq/", "Zoll-FAQ"), ("/guides/", "Ratgeber"), ("/guides/shipping/", "Versand")]),
    "cssbuyspreadsheets.us": D(agent="CSSBuy", dest="US", loc="en", lang="en-US", ccy="USD", dest_label="the United States",
        title="CSSBuy United States — USD, USPS, CBP notes",
        h1="CSSBuy for a US delivery address",
        keep=[("/spreadsheet/", "Spreadsheet"), ("/faq/", "FAQ"), ("/guides/", "Guides"), ("/guides/shipping/", "Shipping")]),
    "fansbuy.co.uk": D(agent="FansBuy", dest="GB", loc="en", lang="en-GB", ccy="GBP", dest_label="the United Kingdom",
        title="FansBuy UK — GBP, Royal Mail, HMRC notes",
        h1="FansBuy for a UK delivery address",
        keep=[("/how-to-use-fansbuy/", "How to use"), ("/is-fansbuy-legit/", "Is it legit?"), ("/fansbuy-coupons/", "Coupons"), ("/fansbuy-spreadsheet/", "Spreadsheet")]),
    "fansbuy.nl": D(agent="FansBuy", dest="NL", loc="nl", lang="nl-NL", ccy="EUR", dest_label="Nederland",
        title="FansBuy Nederland — Nederlandse postcode",
        h1="FansBuy voor een Nederlands adres",
        keep=[("/how-to-use-fansbuy/", "Handleiding"), ("/is-fansbuy-legit/", "Review"), ("/fansbuy-coupons/", "Coupons"), ("/fansbuy-spreadsheet/", "Spreadsheet")]),
    "fansbuyspreadsheet.de": D(agent="FansBuy", dest="DE", loc="de", lang="de-DE", ccy="EUR", dest_label="Deutschland",
        title="FansBuy Deutschland — Packstation, DHL, Zoll",
        h1="FansBuy für eine deutsche Adresse",
        keep=[("/how-to-use-fansbuy/", "Anleitung"), ("/is-fansbuy-legit/", "Seriös?"), ("/fansbuy-coupons/", "Coupons"), ("/fansbuy-spreadsheet/", "Spreadsheet")]),
    "lovegobuy.it": D(agent="LoveGoBuy", dest="IT", loc="it", lang="it-IT", ccy="EUR", dest_label="l’Italia",
        title="LoveGoBuy Italia — Poste Italiane e spedizione",
        h1="LoveGoBuy per un indirizzo in Italia",
        keep=[("/lovegobuy-spreadsheet/", "Spreadsheet"), ("/is-lovegobuy-legit/", "È affidabile?"), ("/how-to-use-lovegobuy/", "Come usare"), ("/lovegobuy-coupons/", "Coupon")]),
    "lovegobuy.nl": D(agent="LoveGoBuy", dest="NL", loc="nl", lang="nl-NL", ccy="EUR", dest_label="Nederland",
        title="LoveGoBuy Nederland — PostNL-lijnen en verzending",
        h1="LoveGoBuy voor een Nederlands adres",
        keep=[("/lovegobuy-shipping/", "Verzending"), ("/lovegobuy-ervaringen/", "Ervaringen"), ("/lovegobuy-coupon/", "Coupons"), ("/lovegobuy-spreadsheet/", "Spreadsheet")]),
    "lovegobuyspreadsheet.ca": D(agent="LoveGoBuy", dest="CA", loc="en", lang="en-CA", ccy="CAD", dest_label="Canada",
        title="LoveGoBuy Canada — CAD, Canada Post, CBSA notes",
        h1="LoveGoBuy for a Canadian delivery address",
        keep=[("/lovegobuy-spreadsheet/", "Spreadsheet"), ("/is-lovegobuy-legit/", "Is it legit?"), ("/lovegobuy-coupon/", "Coupons"), ("/how-to-use-lovegobuy/", "How to use")]),
    "lovegobuyspreadsheet.es": D(agent="LoveGoBuy", dest="ES", loc="es", lang="es-ES", ccy="EUR", dest_label="España",
        title="LoveGoBuy España — Correos, opiniones y envío",
        h1="LoveGoBuy para una dirección en España",
        keep=[("/lovegobuy-opiniones/", "Opiniones"), ("/es-lovegobuy-confiable/", "¿Es fiable?"), ("/envio-lovegobuy-espana/", "Envío"), ("/lovegobuy-spreadsheet/", "Spreadsheet")]),
    "mulebuy.fr": D(agent="MuleBuy", dest="FR", loc="fr", lang="fr-FR", ccy="EUR", dest_label="la France",
        title="MuleBuy France — Colissimo, pas un code postal belge",
        h1="MuleBuy pour une adresse en France",
        keep=[("/how-to-use-mulebuy/", "Mode d’emploi"), ("/is-mulebuy-legit/", "Avis"), ("/mulebuy-coupons/", "Coupons"), ("/mulebuy-spreadsheet/", "Spreadsheet")]),
    "mulebuyspreadsheets.co.uk": D(agent="MuleBuy", dest="GB", loc="en", lang="en-GB", ccy="GBP", dest_label="the United Kingdom",
        title="MuleBuy UK — GBP, Royal Mail, HMRC notes",
        h1="MuleBuy for a UK delivery address",
        keep=[("/how-to-use-mulebuy/", "How to use"), ("/is-mulebuy-legit/", "Is it legit?"), ("/mulebuy-coupons/", "Coupons"), ("/mulebuy-spreadsheet/", "Spreadsheet")]),
    "mulebuyspreadsheets.es": D(agent="MuleBuy", dest="ES", loc="es", lang="es-ES", ccy="EUR", dest_label="España",
        title="MuleBuy España — Correos y envío",
        h1="MuleBuy para una dirección en España",
        keep=[("/how-to-use-mulebuy/", "Cómo usar"), ("/is-mulebuy-legit/", "¿Legit?"), ("/mulebuy-coupons/", "Cupones"), ("/mulebuy-spreadsheet/", "Spreadsheet")]),
    "mulebuyspreadsheets.us": D(agent="MuleBuy", dest="US", loc="en", lang="en-US", ccy="USD", dest_label="the United States",
        title="MuleBuy United States — USD, USPS, CBP notes",
        h1="MuleBuy for a US delivery address",
        keep=[("/how-to-use-mulebuy/", "How to use"), ("/is-mulebuy-legit/", "Is it legit?"), ("/mulebuy-coupons/", "Coupons"), ("/mulebuy-spreadsheet/", "Spreadsheet")]),
    "mycnbox.co.uk": D(agent="MyCNBox", dest="GB", loc="en", lang="en-GB", ccy="GBP", dest_label="the United Kingdom",
        title="MyCNBox UK — GBP, Royal Mail, HMRC notes",
        h1="MyCNBox for a UK delivery address",
        keep=[("/is-mycnbox-legit/", "Is it legit?"), ("/mycnbox-coupons/", "Coupons"), ("/mycnbox-shipping-guide/", "Shipping"), ("/mycnbox-spreadsheet/", "Spreadsheet")]),
    "mycnbox.de": D(agent="MyCNBox", dest="DE", loc="de", lang="de-DE", ccy="EUR", dest_label="Deutschland",
        title="MyCNBox Deutschland — Packstation, DHL, Zoll",
        h1="MyCNBox für eine deutsche Adresse",
        keep=[("/mycnbox-spreadsheet/", "Spreadsheet"), ("/mycnbox-shipping-guide/", "Versand"), ("/how-to-use-mycnbox/", "Anleitung"), ("/is-mycnbox-legit/", "Seriös?")]),
    "mycnbox.es": D(agent="MyCNBox", dest="ES", loc="es", lang="es-ES", ccy="EUR", dest_label="España",
        title="MyCNBox España — Correos y spreadsheet",
        h1="MyCNBox para una dirección en España",
        keep=[("/mycnbox-spreadsheet/", "Spreadsheet"), ("/mycnbox-shipping-guide/", "Envío"), ("/how-to-use-mycnbox/", "Cómo usar"), ("/is-mycnbox-legit/", "¿Legit?")]),
    "mycnbox.fr": D(agent="MyCNBox", dest="FR", loc="fr", lang="fr-FR", ccy="EUR", dest_label="la France",
        title="MyCNBox France — Colissimo, pas un code postal belge",
        h1="MyCNBox pour une adresse en France",
        keep=[("/mycnbox-spreadsheet/", "Spreadsheet"), ("/mycnbox-shipping-guide/", "Livraison"), ("/how-to-use-mycnbox/", "Mode d’emploi"), ("/is-mycnbox-legit/", "Avis")]),
    "mycnbox.nl": D(agent="MyCNBox", dest="NL", loc="nl", lang="nl-NL", ccy="EUR", dest_label="Nederland",
        title="MyCNBox Nederland — Nederlandse postcode",
        h1="MyCNBox voor een Nederlands adres",
        keep=[("/mycnbox-spreadsheet/", "Spreadsheet"), ("/mycnbox-shipping-guide/", "Verzending"), ("/how-to-use-mycnbox/", "Handleiding"), ("/is-mycnbox-legit/", "Review")]),
    "mycnbox.pl": D(agent="MyCNBox", dest="PL", loc="en", lang="pl-PL", ccy="PLN", dest_label="Poland",
        title="MyCNBox Poland — PLN, 00-001 Warszawa, KAS notes",
        h1="MyCNBox for a Polish delivery address",
        keep=[("/mycnbox-spreadsheet/", "Spreadsheet"), ("/mycnbox-shipping-guide/", "Shipping"), ("/how-to-use-mycnbox/", "How to use"), ("/is-mycnbox-legit/", "Is it legit?")]),
    "oopbuyspreadsheets.it": D(agent="OOPBuy", dest="IT", loc="it", lang="it-IT", ccy="EUR", dest_label="l’Italia",
        title="OOPBuy Italia — Poste Italiane e spedizione",
        h1="OOPBuy per un indirizzo di consegna in Italia",
        keep=[("/oopbuy-spreadsheet/", "Spreadsheet"), ("/how-to-use-oopbuy/", "Come usare"), ("/is-oopbuy-legit/", "È affidabile?"), ("/oopbuy-coupons/", "Coupon")]),
    "ootdbuy.nl": D(agent="OOTDBuy", dest="NL", loc="nl", lang="nl-NL", ccy="EUR", dest_label="Nederland",
        title="OOTDBuy Nederland — Nederlandse postcode",
        h1="OOTDBuy voor een Nederlands adres",
        keep=[("/ootdbuy-spreadsheet/", "Spreadsheet"), ("/how-to-use-ootdbuy/", "Handleiding"), ("/is-ootdbuy-legit/", "Review"), ("/ootdbuy-coupons/", "Coupons")]),
    "ootdbuyspreadsheet.ca": D(agent="OOTDBuy", dest="CA", loc="en", lang="en-CA", ccy="CAD", dest_label="Canada",
        title="OOTDBuy Canada — CAD, form A1A 1A1, CBSA notes",
        h1="OOTDBuy for a Canadian delivery address",
        keep=[("/ootdbuy-spreadsheet/", "Spreadsheet"), ("/how-to-use-ootdbuy/", "How to use"), ("/is-ootdbuy-legit/", "Is it legit?"), ("/ootdbuy-coupons/", "Coupons")]),
    "ootdbuyspreadsheet.co.uk": D(agent="OOTDBuy", dest="GB", loc="en", lang="en-GB", ccy="GBP", dest_label="the United Kingdom",
        title="OOTDBuy UK — GBP, Royal Mail, HMRC notes",
        h1="OOTDBuy for a UK delivery address",
        keep=[("/ootdbuy-spreadsheet/", "Spreadsheet"), ("/how-to-use-ootdbuy/", "How to use"), ("/is-ootdbuy-legit/", "Is it legit?"), ("/ootdbuy-coupons/", "Coupons")]),
    "ootdbuyspreadsheet.de": D(agent="OOTDBuy", dest="DE", loc="de", lang="de-DE", ccy="EUR", dest_label="Deutschland",
        title="OOTDBuy Deutschland — Packstation, DHL, Zoll",
        h1="OOTDBuy für eine deutsche Adresse",
        keep=[("/ootdbuy-spreadsheet/", "Spreadsheet"), ("/how-to-use-ootdbuy/", "Anleitung"), ("/is-ootdbuy-legit/", "Seriös?"), ("/ootdbuy-coupons/", "Coupons")]),
    "ootdbuyspreadsheet.us": D(agent="OOTDBuy", dest="US", loc="en", lang="en-US", ccy="USD", dest_label="the United States",
        title="OOTDBuy United States — USD, USPS, CBP notes",
        h1="OOTDBuy for a US delivery address",
        keep=[("/ootdbuy-spreadsheet/", "Spreadsheet"), ("/how-to-use-ootdbuy/", "How to use"), ("/is-ootdbuy-legit/", "Is it legit?"), ("/ootdbuy-coupons/", "Coupons")]),
    "orientdig.at": D(agent="OrientDig", dest="AT", loc="de", lang="de-AT", ccy="EUR", dest_label="Österreich",
        title="OrientDig Österreich — Österreichische Post, nicht DHL DE",
        h1="OrientDig für eine österreichische Adresse",
        keep=[("/orientdig-shipping/", "Versand"), ("/orientdig-coupons/", "Gutscheine"), ("/how-to-use-orientdig/", "Anleitung"), ("/is-orientdig-legit/", "Seriös?")]),
    "orientdig.es": D(agent="OrientDig", dest="ES", loc="es", lang="es-ES", ccy="EUR", dest_label="España",
        title="OrientDig España — Correos, envío y spreadsheet",
        h1="OrientDig para una dirección en España",
        keep=[("/orientdig-shipping-coupons/", "Cupones"), ("/como-comprar-en-orientdig/", "Cómo comprar"), ("/orientdig-spreadsheet/", "Spreadsheet"), ("/is-orientdig-legit/", "¿Legit?")]),
    "orientdig.fr": D(agent="OrientDig", dest="FR", loc="fr", lang="fr-FR", ccy="EUR", dest_label="la France",
        title="OrientDig France — Colissimo, pas un code postal belge",
        h1="OrientDig pour une adresse en France",
        keep=[("/orientdig-shipping/", "Livraison"), ("/how-to-use-orientdig/", "Mode d’emploi"), ("/orientdig-coupons/", "Coupons"), ("/is-orientdig-legit/", "Avis")]),
    "orientdig.us": D(agent="OrientDig", dest="US", loc="en", lang="en-US", ccy="USD", dest_label="the United States",
        title="OrientDig United States — USD, USPS, CBP notes",
        h1="OrientDig for a US delivery address",
        keep=[("/orientdig-shipping/", "Shipping"), ("/how-to-use-orientdig/", "How to use"), ("/orientdig-coupons/", "Coupons"), ("/is-orientdig-legit/", "Is it legit?")]),
    "orientdigspreadsheet.de": D(agent="OrientDig", dest="DE", loc="de", lang="de-DE", ccy="EUR", dest_label="Deutschland",
        title="OrientDig Deutschland — Packstation, DHL, Zoll",
        h1="OrientDig für eine deutsche Adresse",
        keep=[("/orientdig-shipping/", "Versand"), ("/how-to-use-orientdig/", "Anleitung"), ("/orientdig-coupons/", "Gutscheine"), ("/is-orientdig-legit/", "Seriös?")]),
    "orientdigspreadsheet.it": D(agent="OrientDig", dest="IT", loc="it", lang="it-IT", ccy="EUR", dest_label="l’Italia",
        title="OrientDig Italia — Poste Italiane e spedizione",
        h1="OrientDig per un indirizzo in Italia",
        keep=[("/orientdig-shipping/", "Spedizione"), ("/how-to-use-orientdig/", "Come usare"), ("/orientdig-coupons/", "Coupon"), ("/is-orientdig-legit/", "È affidabile?")]),
    "orientdigspreadsheet.nl": D(agent="OrientDig", dest="NL", loc="nl", lang="nl-NL", ccy="EUR", dest_label="Nederland",
        title="OrientDig Nederland — Nederlandse postcode",
        h1="OrientDig voor een Nederlands adres",
        keep=[("/orientdig-shipping/", "Verzending"), ("/how-to-use-orientdig/", "Handleiding"), ("/orientdig-coupons/", "Coupons"), ("/is-orientdig-legit/", "Review")]),
    "orientdigspreadsheet.uk": D(agent="OrientDig", dest="GB", loc="en", lang="en-GB", ccy="GBP", dest_label="the United Kingdom",
        title="OrientDig UK — GBP, Royal Mail, HMRC notes",
        h1="OrientDig for a UK delivery address",
        keep=[("/orientdig-shipping/", "Shipping"), ("/how-to-use-orientdig/", "How to use"), ("/orientdig-coupons/", "Coupons"), ("/is-orientdig-legit/", "Is it legit?")]),
    "superbuyspreadsheets.ca": D(agent="Superbuy", dest="CA", loc="en", lang="en-CA", ccy="CAD", dest_label="Canada",
        title="Superbuy Canada — CAD, form A1A 1A1, CBSA notes",
        h1="Superbuy for a Canadian delivery address",
        keep=[("/superbuy-spreadsheet/", "Spreadsheet"), ("/how-to-use-superbuy/", "How to use"), ("/is-superbuy-legit/", "Is it legit?"), ("/superbuy-coupons/", "Coupons")]),
    "superbuyspreadsheets.it": D(agent="Superbuy", dest="IT", loc="it", lang="it-IT", ccy="EUR", dest_label="l’Italia",
        title="Superbuy Italia — Poste Italiane e spedizione",
        h1="Superbuy per un indirizzo in Italia",
        keep=[("/superbuy-spreadsheet/", "Spreadsheet"), ("/how-to-use-superbuy/", "Come usare"), ("/is-superbuy-legit/", "È affidabile?"), ("/superbuy-coupons/", "Coupon")]),
    "superbuyspreadsheets.us": D(agent="Superbuy", dest="US", loc="en", lang="en-US", ccy="USD", dest_label="the United States",
        title="Superbuy United States — USD, USPS, CBP notes",
        h1="Superbuy for a US delivery address",
        keep=[("/superbuy-spreadsheet/", "Spreadsheet"), ("/how-to-use-superbuy/", "How to use"), ("/is-superbuy-legit/", "Is it legit?"), ("/superbuy-coupons/", "Coupons")]),
    "usfansspreadsheet.co.uk": D(agent="USFans", dest="GB", loc="en", lang="en-GB", ccy="GBP", dest_label="the United Kingdom",
        title="USFans UK — GBP, Royal Mail, HMRC notes",
        h1="USFans for a UK delivery address",
        keep=[("/usfans-spreadsheet/", "Spreadsheet"), ("/guide.html", "Guide"), ("/faq.html", "FAQ"), ("/blog/", "Blog")]),
    "usfansspreadsheet.nl": D(agent="USFans", dest="NL", loc="nl", lang="nl-NL", ccy="EUR", dest_label="Nederland",
        title="USFans Nederland — Nederlandse postcode",
        h1="USFans voor een Nederlands adres",
        keep=[("/usfans-spreadsheet/", "Spreadsheet"), ("/guide.html", "Gids"), ("/faq.html", "FAQ"), ("/blog/", "Blog")]),
}

NAV = {
    "en": [("Spreadsheet", "sheet"), ("Shipping", "ship"), ("Is it legit?", "legit"), ("Coupons", "coup"), ("How to use", "how"), ("Local checks", "#local")],
    "de": [("Spreadsheet", "sheet"), ("Versand", "ship"), ("Seriös?", "legit"), ("Coupons", "coup"), ("Anleitung", "how"), ("Lokal", "#local")],
    "es": [("Spreadsheet", "sheet"), ("Envío", "ship"), ("¿Legit?", "legit"), ("Cupones", "coup"), ("Cómo usar", "how"), ("Check local", "#local")],
    "fr": [("Spreadsheet", "sheet"), ("Livraison", "ship"), ("Avis", "legit"), ("Coupons", "coup"), ("Mode d’emploi", "how"), ("Local", "#local")],
    "it": [("Spreadsheet", "sheet"), ("Spedizione", "ship"), ("È affidabile?", "legit"), ("Coupon", "coup"), ("Come usare", "how"), ("Locale", "#local")],
    "nl": [("Spreadsheet", "sheet"), ("Verzending", "ship"), ("Review", "legit"), ("Coupons", "coup"), ("Handleiding", "how"), ("Lokaal", "#local")],
}


def _facts(host: str) -> dict:
    d = HOSTS[host]
    ag = AGENTS[d["agent"]]
    cname, curl = CUSTOMS.get(d["dest"], ("the destination customs site", ""))
    return {
        "agent": d["agent"],
        "host": host,
        "lang": d["lang"],
        "loc": d["loc"],
        "dest": d["dest"],
        "dest_label": d["dest_label"],
        "ccy": d["ccy"],
        "storage": ag["storage"],
        "estimator": ag["estimator"],
        "official": ag["official"],
        "date": DATE,
        "email": f"support@{host}",
        "keep": d["keep"],
        "customs": cname,
        "customs_url": curl,
        "codes_off_title": ag["codes"],
        "strict_html_codes": False,
    }


def theme_css(agent: str) -> str:
    a = AGENTS[agent]
    return f"""/* {agent} country dest — matches official palette, Inter not serif. */
:root {{
  --primary: {a['primary']};
  --primary-dark: {a['primary']};
  --primary-soft: {a['soft']};
  --nav-dark: {a['nav']};
}}
body {{ background: var(--bg, #f7f8fa); }}
"""


def _nav(host: str) -> str:
    d = HOSTS[host]
    loc = d["loc"]
    keep = {k: v for v, k in [("sheet", 0), ("coup", 2), ("legit", 1), ("how", 3)]}
    links = []
    items = NAV.get(loc, NAV["en"])
    mapping = {"sheet": 2, "ship": 0, "legit": 1, "coup": 2, "how": 3}
    for lab, kind in items:
        if kind == "#local":
            href = "#local"
        else:
            idx = mapping.get(kind, 0)
            href = d["keep"][idx][0] if idx < len(d["keep"]) else "#catalog"
        links.append(f'<a href="{escape(href)}">{escape(lab)}</a>')
    return "".join(links)


def _prose(host: str) -> str:
    f = _facts(host)
    ag, dest, h = f["agent"], f["dest_label"], host
    loc = f["loc"]
    packs = {
        "de": (
            f"{ag} ist ein Einkaufsagent, kein Shop. {h} ist ein Infodesk für {dest}.",
            f"Das Spreadsheet auf {h} ist ein Index, keine Excel-Datei und keine Kasse.",
            f"Restricted ist eine Plattform-Sperre, kein Zollbescheid für {dest}.",
        ),
        "es": (
            f"{ag} es un agente de compras, no una tienda. {h} es un desk informativo para {dest}.",
            f"El spreadsheet de {h} es un índice, no Excel ni caja.",
            f"Restricted es un bloqueo de plataforma, no un embargo de aduana para {dest}.",
        ),
        "fr": (
            f"{ag} est un agent d’achat, pas une boutique. {h} est un desk d’information pour {dest}.",
            f"Le spreadsheet de {h} est un index, pas Excel ni une caisse.",
            f"Restricted est un blocage plateforme, pas une saisie douane pour {dest}.",
        ),
        "it": (
            f"{ag} è un agente d’acquisto, non un negozio. {h} è un desk informativo per {dest}.",
            f"Lo spreadsheet su {h} è un indice, non Excel né cassa.",
            f"Restricted è un blocco piattaforma, non un sequestro doganale per {dest}.",
        ),
        "nl": (
            f"{ag} is een inkoopagent, geen winkel. {h} is een infodesk voor {dest}.",
            f"De spreadsheet op {h} is een index, geen Excel en geen kassa.",
            f"Restricted is een platformblokkade, geen douane-inbeslagname voor {dest}.",
        ),
        "en": (
            f"{ag} is a purchasing agent, not a shop. {h} is an information desk for {dest}.",
            f"The spreadsheet on {h} is an index, not Excel and not checkout.",
            f"Restricted is a platform purchase block, not a customs seizure notice for {dest}.",
        ),
    }
    a_h, s_h, r_h = packs.get(loc, packs["en"])
    return f"""
<section class="sg-sec" id="agent"><h2>{escape(ag)}</h2><p>{escape(a_h)}</p>
<p>Orders, payment and warehouse photos stay on {escape(f['official'])}. This hostname never takes a card.</p></section>
<section class="sg-sec" id="sheet-explain"><h2>Spreadsheet</h2><p>{escape(s_h)}</p>
<p>English keys (sneakers, hoodie, jacket) still feed /api/products/ on this host. Lab {DATE}.</p></section>
<section class="sg-sec" id="restricted"><h2>Restricted</h2><p>{escape(r_h)}</p>
<p>Price-0 cards are dead Weidian/Taobao links, not a checkout you can force toward {escape(dest)}.</p></section>
"""


def _wall(host: str) -> str:
    tiles = "".join(
        f'<a class="sg-cat" href="#catalog" data-q="{escape(slug)}"><strong>{escape(lab)}</strong><span>{escape(slug)}</span></a>'
        for slug, lab in CATS
    )
    return f'<section class="sg-sec" id="cat-wall"><h2>Catalogue wall</h2><p class="ssub">Sixteen English index keys. Local words often return zero cards.</p><div class="sg-cats">{tiles}</div></section>'


def _states(host: str) -> str:
    f = _facts(host)
    return f"""<section class="sg-sec" id="states"><h2>{escape(f['dest_label'])}</h2>
<p class="ssub">Estimator country is {escape(f['dest'])}, not this TLD. Sister country hosts stay separate files — no 301.</p>
<p>{escape(independence_copy(f))}</p></section>"""


def _shots(host: str) -> str:
    f = _facts(host)
    return f"""<section class="sg-sec" id="shots"><h2>Official app</h2>
<p class="ssub">Screenshots and live money stay on the official {escape(f['agent'])} site, dated {DATE}.</p>
<p><a class="btn btn-outline" href="{escape(f['official'])}" rel="noopener">Open {escape(f['agent'])}</a>
<a class="btn btn-primary" href="{escape(f['estimator'])}" rel="noopener">Freight estimate</a></p></section>"""


def _lab(host: str) -> str:
    lab = lab_copy(_facts(host))
    return f"""<section class="sg-sec" id="lab"><h2>{escape(lab['h2'])}</h2>
<p class="ssub">{lab['ssub']}</p>
<p><a class="btn btn-primary" href="{escape(_facts(host)['estimator'])}">{escape(lab['cta'])}</a></p></section>"""


def _keep(host: str) -> str:
    d = HOSTS[host]
    links = "".join(f'<a href="{escape(h)}">{escape(l)}</a>' for h, l in d["keep"])
    return f'<section class="sg-sec" id="kept"><h2>Already ranking on this host</h2><div class="keep">{links}</div></section>'


def _faq(host: str) -> str:
    pairs = long_faqs(_facts(host))
    items = []
    for i, (q, a) in enumerate(pairs):
        op = " open" if i == 0 else ""
        items.append(f'<details class="sg-faq"{op}><summary>{escape(q)}</summary><p>{escape(a)}</p></details>')
    return f'<section class="sg-sec" id="faq"><h2>FAQ</h2>{"".join(items)}</section>'


def build_home(host: str) -> str:
    d = HOSTS[host]
    ag = AGENTS[d["agent"]]
    f = _facts(host)
    u = ui_copy(d["loc"])
    css = "\n".join(f'<link rel="stylesheet" href="{escape(href)}?v=20261002-cms">' for href in ag["css"])
    desc = f"{d['agent']} independent desk for {d['dest_label']} on {host}. Catalogue, freight estimate, local last-mile. Not checkout."
    html = f"""<!DOCTYPE html>
<html lang="{escape(d['lang'])}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{escape(d['title'])}</title>
<meta name="description" content="{escape(desc)}">
<link rel="canonical" href="https://{escape(host)}/">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap" rel="stylesheet">
{css}
<style>{EXTRA_CSS_FX}</style>
</head>
<body>
{skip_link(skip_label(d['loc']))}
<header class="site-header">
  <div class="container header-inner">
    <a class="brand" href="/"><img class="brand-logo" src="{escape(ag['logo'])}" alt="{escape(d['agent'])}"></a>
    <nav class="header-nav">{_nav(host)}</nav>
    <div class="header-actions">
      <a class="btn btn-outline" href="#catalog">{escape(u.get('open') or 'Catalogue')}</a>
      <a class="btn btn-primary" href="{escape(ag['register'])}" rel="noopener sponsored">{escape(u['register'])}</a>
    </div>
  </div>
</header>
<main id="main" class="container">
<section class="sg-hero">
  <h1>{escape(d['h1'])}</h1>
  <p class="hsub">{escape(d['agent'])} · {escape(host)} · {escape(d['ccy'])} display · {escape(d['dest_label'])}. Independent desk — not the official app, not checkout.</p>
  <p class="eu-badge">{escape(d['dest'])} · {escape(d['ccy'])} · {escape(f['customs'])}</p>
  <div class="sg-ctas">
    <a class="btn btn-primary" href="#catalog">Catalogue</a>
    <a class="btn btn-outline" href="#local">{escape(local_cta(f))}</a>
    <a class="btn btn-outline" href="{escape(ag['estimator'])}">{escape(u['freight'])}</a>
  </div>
</section>
"""
    html = inject_jsonld(
        html,
        webpage_ld(url=f"https://{host}/", name=d["title"], desc=desc, lang=d["lang"], brand=d["agent"], host=host),
        organization_ld(name=f"{host} independent desk", url=f"https://{host}/", email=f"support@{host}", lang=d["lang"], desc=desc),
        breadcrumb_ld([("Home", f"https://{host}/")]),
        faq_ld(d["lang"], long_faqs(f)[:8]),
        itemlist_ld(url=f"https://{host}/", name=f"{d['agent']} catalogue keys", items=[(lab, slug) for slug, lab in CATS]),
    )
    html += local_guide_html(f)
    html += _prose(host)
    html += _wall(host)
    html += catalog_block(host, d, register_url=ag["register"], loc_fn=lambda k: HOSTS[k]["loc"], cat_labels={})
    html += _states(host)
    html += _shots(host)
    html += _lab(host)
    html += _keep(host)
    html += _faq(host)
    html += f"""
</main>
<footer class="site-footer">
  <div class="container footer-grid">
    <div><strong>{escape(d['agent'])} · {escape(host)}</strong>
      <p class="footer-note">{escape(u['foot'].format(host=host, brand=d['agent']))}</p>
      <p class="legal-note">{escape(independence_copy(f))}</p></div>
    <div><strong>{escape(u['on_host'])}</strong>
      <p>{''.join(f'<a href="{escape(h)}">{escape(l)}</a><br>' for h,l in d['keep'])}</p></div>
    <div><strong>{escape(u['official'])}</strong>
      <p><a href="{escape(ag['official'])}">{escape(d['agent'])}</a><br>
      <a href="{escape(ag['estimator'])}">{escape(u['freight'])}</a></p></div>
  </div>
</footer>
</body></html>
"""
    return html


def generate() -> None:
    if not CMS_CSS.is_file():
        raise SystemExit("missing desk-cms.css")
    for host, d in HOSTS.items():
        html = build_home(host)
        if "Georgia" in html or "#00C853" in html:
            raise SystemExit(f"{host}: Georgia/HipoBuy leak")
        for e in validate_desk(html, _facts(host), page="home"):
            raise SystemExit(f"{host}: {e}")
        if len(html) < 18000:
            raise SystemExit(f"{host}: too small {len(html)}")
        dest = OUT / host / "overlay"
        dest.mkdir(parents=True, exist_ok=True)
        (dest / "index.html").write_text(html, encoding="utf-8")
        themed = OUT / "shared" / "themes" / f"{d['agent'].lower()}-theme.css"
        themed.parent.mkdir(parents=True, exist_ok=True)
        if not themed.is_file():
            themed.write_text(theme_css(d["agent"]), encoding="utf-8")
        print("OK", host, len(html), d["agent"], d["dest"])


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


def _run(client, cmd: str, timeout: int = 90) -> str:
    _, stdout, stderr = client.exec_command(cmd, timeout=timeout)
    return (stdout.read() + stderr.read()).decode(errors="replace").strip()


def put() -> None:
    generate()
    client = _connect()
    stamp = time.strftime("%Y%m%d-%H%M%S")
    bak = f"/www/backup/dest-hub-skins-{stamp}"
    print(_run(client, f"mkdir -p '{bak}'"))
    sftp = client.open_sftp()
    theme_map = {
        "AllChinaBuy": "allchinabuy-theme.css",
        "ACBuy": "allchinabuy-theme.css",
        "BBDBuy": "bbdbuy-theme.css",
        "CSSBuy": "cssbuy-theme.css",
        "FansBuy": "fansbuy-theme.css",
        "LoveGoBuy": "lovegobuy-theme.css",
        "MuleBuy": "mulebuy-theme.css",
        "MyCNBox": "mycnbox-theme.css",
        "OOPBuy": "oopbuy-theme.css",
        "OOTDBuy": "ootdbuy-theme.css",
        "OrientDig": "orientdig-theme.css",
        "Superbuy": "superbuy-theme.css",
        "USFans": "usfans-theme.css",
    }
    for host, d in HOSTS.items():
        remote_root = f"/www/wwwroot/{host}"
        _run(client, f"mkdir -p '{remote_root}/assets/css' '{bak}/{host}' && cp -a '{remote_root}/index.html' '{bak}/{host}/index.html'")
        local = OUT / host / "overlay" / "index.html"
        sftp.put(str(local), f"{remote_root}/index.html")
        sftp.put(str(CMS_CSS), f"{remote_root}/assets/css/desk-cms.css")
        theme_name = theme_map[d["agent"]]
        theme_local = OUT / "shared" / "themes" / f"{d['agent'].lower()}-theme.css"
        if not theme_local.is_file():
            theme_local.write_text(theme_css(d["agent"]), encoding="utf-8")
        remote_theme = f"{remote_root}/assets/css/{theme_name}"
        existed = _run(client, f"wc -c < '{remote_theme}' 2>/dev/null || echo 0")
        try:
            existed_n = int(re.sub(r"\D", "", existed) or "0")
        except ValueError:
            existed_n = 0
        if existed_n < 2000:
            sftp.put(str(theme_local), remote_theme)
            _run(client, f"chown www:www '{remote_theme}'")
        _run(client, f"chown www:www '{remote_root}/index.html' '{remote_root}/assets/css/desk-cms.css'")
        print("PUT", host, local.stat().st_size)
    sftp.close()
    print("backup", bak)
    client.close()


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "generate"
    if cmd == "put":
        put()
    else:
        generate()
