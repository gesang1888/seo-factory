#!/usr/bin/env python3
"""AllChinaBuy country dests: CA, NL, UK.

Gold IA: hipobuy.es. Gold brand: allchinabuy.com (forest green, official
wordmark). AllChinaBuy is a different agent from ACBuy — these hosts never
301 into acbuyspreadsheets.ca / .nl. Same-agent CA / NL / UK stay independent
of each other. Hub allchina-buy.com is not overwritten.

Official allchinabuy.com showed a maintenance notice on 6 Oct 2026; this
desk does not invent estimator lines, transit days or a declared value.
"""
from __future__ import annotations

import json
import os
import re
import shutil
import sys
import time
from html import escape
from pathlib import Path
from urllib.parse import quote_plus

_TOOLS = Path(__file__).resolve().parent
if str(_TOOLS) not in sys.path:
    sys.path.insert(0, str(_TOOLS))

from country_cms import (
    CountryDesk,
    W2C,
    W2C_CATS as W2C_CATS_NL,
    build_404,
    cats_for,
    fig as cms_fig,
    official_url,
    page_title,
    render_css,
    shell as cms_shell,
    w2c_sheet,
    wrap_inner as cms_wrap_inner,
)
from desk_template import dest_local_pack, faq_ld, itemlist_ld, long_faqs, validate_desk

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "sites"
DATE = "6 Oct 2026"
OFFICIAL = "https://www.allchinabuy.com/"
EST = "https://www.allchinabuy.com/"
HELP = "https://www.allchinabuy.com/"
ACC = "#18753C"
ACC_DARK = "#0F5A2E"
MAIL = "cnfd85269032661@gmail.com"
ACBUY_CA = "acbuyspreadsheets.ca"
ACBUY_NL = "acbuyspreadsheets.nl"
HUB = "allchina-buy.com"
DEST_MIN = 22000
CSS_V = "20261006c"
FORBIDDEN_ACBUY = ("5F2RRA", "EwjrSk", "ACBUY5", "acbuy.com/estimation", "www.acbuy.com/help")

EN_LABELS = {
    "SNEAKERS": "Sneakers",
    "SLIPPERS": "Slippers",
    "T-SHIRT": "T-shirt",
    "POLO": "Polo",
    "SHIRT": "Shirt",
    "SHORTS": "Shorts",
    "VEST": "Vest",
    "LONG SLEEVED": "Long sleeve",
    "HOODIE": "Hoodie",
    "SWEATER": "Sweater",
    "SHAWL": "Shawl",
    "JACKET": "Jacket",
    "SHELL JACKET": "Shell jacket",
    "FLEECE JACKET": "Fleece jacket",
    "DOWN JACKETS": "Down jacket",
    "TROUSERS": "Trousers",
    "Jersey": "Jersey",
    "FEMALE STYLE": "Womenswear",
    "Electronics": "Electronics",
    "GLOVES": "Gloves",
    "BAG": "Bag",
    "HAT": "Hat",
    "JEWELRY": "Jewelry",
    "UNDERWEAR": "Underwear",
    "BELT": "Belt",
    "KNEEPAD": "Knee pad",
    "SOCKS": "Socks",
    "HEADGEAR": "Headgear",
    "EARMUFF": "Earmuffs",
    "SCARF": "Scarf",
    "GLASSES": "Glasses",
    "WATCH": "Watch",
    "CHILD": "Kids",
}

CAT_NOTES_EN = {
    "SNEAKERS": "Check the sole and last on the QC photos before you book international: that is where most returns start.",
    "SLIPPERS": "Light and flat. A cheap way to fill a box without pushing billed weight up hard.",
    "T-SHIRT": "Asian cuts often run narrower. Compare chest width in centimetres, not only the letter size.",
    "POLO": "Look at collar and piqué on the QC photo. Those two details drift from the catalogue shot most often.",
    "SHIRT": "Sleeve length and shoulder seam on the tape-measure photo, not on the letter size.",
    "SHORTS": "Light and flat: the easiest way to fill a parcel without exploding billed weight.",
    "VEST": "Vests are thicker than they weigh. Count the volume before you add a jacket.",
    "LONG SLEEVED": "Sleeve length and cuff on the QC photo. Asian lengths often run shorter.",
    "HOODIE": "Heavy for their volume. One hoodie can set the weight band for the whole box.",
    "SWEATER": "GSM and shrink. Measure the chest, not only the label size.",
    "SHAWL": "Light, but bulky if it is not packed flat. Ask for flat packing.",
    "JACKET": "Down jackets take enormous space. Volume weight almost always beats the scale here.",
    "SHELL JACKET": "Look at seams and zip on the QC photo. A coating tear only shows up close.",
    "FLEECE JACKET": "Light on the scale, thick in volume. Same recount as down.",
    "DOWN JACKETS": "Volume wins. One down jacket alone can force a dearer weight class.",
    "TROUSERS": "Ask for photos of rise and inseam. The W/L label does not always match the centimetre.",
    "Jersey": "Check number, patches and season on the photos: those are the details that go wrong most often.",
    "FEMALE STYLE": "Fit is rarely unisex. Measure bust and length; do not assume North-American women’s sizes.",
    "Electronics": "Often lithium. Many air lines refuse them: check the official site before you order.",
    "GLOVES": "Ask for a photo of the pair. One glove on the catalogue shot says nothing about the second.",
    "BAG": "Fills a box almost by itself. Count the volume before you add a bag to clothing.",
    "HAT": "Crushable and bulky. Ask for stuffing, or the brim arrives folded.",
    "JEWELRY": "Small and cheap to send. A good way to round out a nearly full box.",
    "UNDERWEAR": "Fewer listings than the rest. If you find nothing, search by brand instead of the word underwear.",
    "BELT": "Buckle and length on the QC photo. The catalogue shot is often a different buckle colour.",
    "KNEEPAD": "Thick and bulky. Count L×W×H, not only the scale.",
    "SOCKS": "Light. Good filler, almost no extra kilo.",
    "HEADGEAR": "Pack to hold shape, or it arrives flattened.",
    "EARMUFF": "Light on the scale, round in volume. Same recount as hats.",
    "SCARF": "Light and flat if folded. Ask for flat packing.",
    "GLASSES": "Fragile and small. Reinforced packing is worth it, even if it is a few grams.",
    "WATCH": "Ask for photos of the movement and clasp. The catalogue shot looks least like what arrives here.",
    "CHILD": "Kids’ sizes are not scaled-down adult sizes. Measure; do not guess at ‘small’.",
}

RANKED = (
    ("/is-allchinabuy-legit/", 8000),
    ("/allchinabuy-shipping-guide/", 8000),
    ("/allchinabuy-coupons/", 8000),
    ("/allchinabuy-spreadsheet/", 8000),
    ("/allchinabuy-invite-code/", 4000),
    ("/how-to-use-allchinabuy/", 4000),
    ("/blog/", 4000),
)

PACKS = {
    "ca": {
        "host": "allchinabuyspreadsheet.ca",
        "dest": "CA",
        "dest_label": "Canada",
        "dest_zh": "Canada — 加拿大",
        "lang": "en-CA",
        "loc": "en",
        "in_language": "in English",
        "ccy": "CAD",
        "home_topic": "buy in China from Canada, safely",
        "hero_h1": "AllChinaBuy Spreadsheet: the guide to buying in China from Canada",
        "eyebrow": "Independent guide, in English",
        "lead": "How you paste a product link into the agent, how the w2clinks catalogue works, how a parcel travels to Canada, and what you check before CBSA.",
        "fingerprint": dest_local_pack("CA")["fingerprint"],
        "customs": "CBSA",
        "customs_url": "https://www.cbsa-asfc.gc.ca/",
        "postal": "Canadian postal code (form A1A 1A1)",
        "catalog": "/catalog/",
        "help": "/help/",
        "news": "/news/",
        "about": "/about/",
        "guide": "/how-to-use-allchinabuy/",
        "ship": "/allchinabuy-shipping-guide/",
        "nav": [
            ("/start/", "Start"),
            ("/how-to-use-allchinabuy/", "Guide"),
            ("/catalog/", "Catalog"),
            ("/allchinabuy-shipping-guide/", "Shipping"),
            ("/help/", "Help"),
            ("/news/", "News"),
        ],
        "footer_sections": [
            ("/how-to-use-allchinabuy/", "AllChinaBuy guide"),
            ("/catalog/", "The spreadsheet and the categories"),
            ("/allchinabuy-shipping-guide/", "Shipping and customs"),
            ("/help/", "Help and questions"),
            ("/news/", "News"),
            ("/about/", "About us"),
        ],
        "aliens": (
            "Packstation",
            "Nederlandse postcode",
            "Northern Ireland is often another",
            "1234 AB",
            "www.acbuy.com",
        ),
        "not_found_tab": "Page not found",
        "login": "Log in to AllChinaBuy",
        "menu": "Open menu",
        "home_cta": "Back to the homepage",
        "skip": "en",
        "desk_css": "allchinabuy-ca-desk.css",
        "css_id": "allchinabuy-ca",
    },
    "uk": {
        "host": "allchinabuyspreadsheets.co.uk",
        "dest": "GB",
        "dest_label": "the United Kingdom",
        "dest_zh": "United Kingdom — 英国",
        "lang": "en-GB",
        "loc": "en",
        "in_language": "in English",
        "ccy": "GBP",
        "home_topic": "buy in China from the United Kingdom, safely",
        "hero_h1": "AllChinaBuy Spreadsheet: the guide to buying in China from the United Kingdom",
        "eyebrow": "Independent guide, in English",
        "lead": "How you paste a product link into the agent, how the w2clinks catalogue works, how a parcel travels to the United Kingdom, and what you check before HMRC.",
        "fingerprint": dest_local_pack("GB")["fingerprint"],
        "customs": "HMRC",
        "customs_url": "https://www.gov.uk/goods-sent-from-abroad",
        "postal": "UK postcode. Northern Ireland is often another carrier product",
        "catalog": "/catalog/",
        "help": "/help/",
        "news": "/news/",
        "about": "/about/",
        "guide": "/how-to-use-allchinabuy/",
        "ship": "/allchinabuy-shipping-guide/",
        "nav": [
            ("/start/", "Start"),
            ("/how-to-use-allchinabuy/", "Guide"),
            ("/catalog/", "Catalog"),
            ("/allchinabuy-shipping-guide/", "Shipping"),
            ("/help/", "Help"),
            ("/news/", "News"),
        ],
        "footer_sections": [
            ("/how-to-use-allchinabuy/", "AllChinaBuy guide"),
            ("/catalog/", "The spreadsheet and the categories"),
            ("/allchinabuy-shipping-guide/", "Shipping and customs"),
            ("/help/", "Help and questions"),
            ("/news/", "News"),
            ("/about/", "About us"),
        ],
        "aliens": (
            "Packstation",
            "Nederlandse postcode",
            "form A1A 1A1",
            "1234 AB",
            "www.acbuy.com",
        ),
        "not_found_tab": "Page not found",
        "login": "Log in to AllChinaBuy",
        "menu": "Open menu",
        "home_cta": "Back to the homepage",
        "skip": "en",
        "desk_css": "allchinabuy-uk-desk.css",
        "css_id": "allchinabuy-uk",
    },
    "nl": {
        "host": "allchinabuyspreadsheet.nl",
        "dest": "NL",
        "dest_label": "Nederland",
        "dest_zh": "Netherlands — 荷兰",
        "lang": "nl-NL",
        "loc": "nl",
        "in_language": "in het Nederlands",
        "ccy": "EUR",
        "home_topic": "kopen in China vanaf Nederland, veilig",
        "hero_h1": "AllChinaBuy Spreadsheet: de gids om in China te kopen vanaf Nederland",
        "eyebrow": "Onafhankelijke gids, in het Nederlands",
        "lead": "Hoe je een productlink in de agent plakt, hoe de catalogus van w2clinks werkt, hoe een pakket naar Nederland reist en wat je nagaat vóór de Douane.",
        "fingerprint": dest_local_pack("NL")["fingerprint"],
        "customs": "Belastingdienst Douane",
        "customs_url": "https://www.belastingdienst.nl/wps/wcm/connect/nl/douane/",
        "postal": "Nederlandse postcode (vorm 1234 AB)",
        "catalog": "/catalogus/",
        "help": "/hulp/",
        "news": "/nieuws/",
        "about": "/over-ons/",
        "guide": "/how-to-use-allchinabuy/",
        "ship": "/allchinabuy-shipping-guide/",
        "nav": [
            ("/start/", "Start"),
            ("/how-to-use-allchinabuy/", "Handleiding"),
            ("/catalogus/", "Catalogus"),
            ("/allchinabuy-shipping-guide/", "Verzending"),
            ("/hulp/", "Hulp"),
            ("/nieuws/", "Nieuws"),
        ],
        "footer_sections": [
            ("/how-to-use-allchinabuy/", "AllChinaBuy-gids"),
            ("/catalogus/", "De spreadsheet en de categorieën"),
            ("/allchinabuy-shipping-guide/", "Verzending en douane"),
            ("/hulp/", "Hulp en vragen"),
            ("/nieuws/", "Nieuws"),
            ("/over-ons/", "Over ons"),
        ],
        "aliens": (
            "form A1A 1A1",
            "Packstation",
            "Northern Ireland is often another",
            "www.acbuy.com",
        ),
        "not_found_tab": "Pagina niet gevonden",
        "login": "Inloggen bij AllChinaBuy",
        "menu": "Menu openen",
        "home_cta": "Terug naar de homepage",
        "skip": "nl",
        "desk_css": "allchinabuy-nl-desk.css",
        "css_id": "allchinabuy-nl",
    },
}


def _off(host: str, path: str = "") -> str:
    url = OFFICIAL.rstrip("/") + path
    sep = "&" if "?" in url else "?"
    return f"{url}{sep}utm_source={host}&utm_medium=referral&utm_campaign=portada"


def desk_for(key: str) -> CountryDesk:
    p = PACKS[key]
    inner = f'data-inner-chrome="{CSS_V}-{p["css_id"]}"'
    if key == "nl":
        intro = (
            "Onafhankelijke Nederlandstalige gids over AllChinaBuy en over hoe je de "
            "catalogus van w2clinks gebruikt om vanuit Nederland in China te kopen."
        )
        independence = (
            "AllChinaBuy Spreadsheet is een onafhankelijke informatiesite. Wij zijn niet "
            "AllChinaBuy, we verwerken geen bestellingen, we innen geen verzendkosten en we "
            "zien je account niet. Elke order, betaling en claim loopt via de officiële site. "
            "AllChinaBuy is een andere agent dan ACBuy — deze host 301’t niet naar acbuyspreadsheets.nl."
        )
        copyright = "&copy; 2026 AllChinaBuy Spreadsheet. Nederlandse tekst, nagekeken vóór publicatie."
        sections_h, official_h, independence_h, nav_aria = (
            "Secties",
            "Officiële links",
            "Onafhankelijkheidsverklaring.",
            "Hoofdmenu",
        )
        nf_h1, nf_lead = "Deze pagina bestaat niet", "De link is misschien oud. Dit zijn de onderdelen die wél bestaan:"
        official_links = [
            (_off(p["host"]), "AllChinaBuy (officiële site)"),
            (_off(p["host"]), "AllChinaBuy-account"),
            (_off(p["host"]), "Officiële site / schatter (nu onderhoud)"),
        ]
        not_found_tab = p["not_found_tab"]
    else:
        intro = (
            f"Independent English-language guide to AllChinaBuy and to how you use the w2clinks "
            f"catalogue to buy in China from {p['dest_label']}."
        )
        independence = (
            "AllChinaBuy Spreadsheet is an independent information site. We are not AllChinaBuy, "
            "we do not process orders, we do not collect shipping fees and we cannot see "
            "your account. Every order, payment and claim runs through the official site. "
            "AllChinaBuy is a different purchasing agent from ACBuy — this host does not 301 "
            "into an ACBuy country dest."
        )
        copyright = "&copy; 2026 AllChinaBuy Spreadsheet. English copy, edited and checked by people before publication."
        sections_h, official_h, independence_h, nav_aria = (
            "Sections",
            "Official links",
            "Independence notice.",
            "Main menu",
        )
        nf_h1, nf_lead = "This page does not exist", "The link may be old. These are the sections that do exist:"
        official_links = [
            (_off(p["host"]), "AllChinaBuy (official site)"),
            (_off(p["host"]), "Create an AllChinaBuy account"),
            (_off(p["host"]), "Official site / estimator (maintenance on 6 Oct 2026)"),
        ]
        not_found_tab = p["not_found_tab"]
    return CountryDesk(
        host=p["host"],
        agent="AllChinaBuy",
        dest=p["dest"],
        dest_label=p["dest_label"],
        lang=p["lang"],
        in_language=p["in_language"],
        official=OFFICIAL,
        estimator=EST,
        help_url=HELP,
        mail=MAIL,
        acc=ACC,
        acc_dark=ACC_DARK,
        date=DATE,
        css_v=CSS_V,
        logo_src="/assets/images/allchinabuy-logo.png",
        nav=list(p["nav"]),
        home_href="/start/",
        footer_intro=intro,
        footer_sections=list(p["footer_sections"]),
        footer_official=official_links,
        independence=independence,
        copyright=copyright,
        login_label=p["login"],
        menu_label=p["menu"],
        skip_lang=p["skip"],
        not_found_h1=nf_h1,
        not_found_lead=nf_lead,
        home_cta=p["home_cta"],
        theme_css="allchinabuy-theme.css",
        desk_css=p["desk_css"],
        inner_marker=inner,
        register_path="/",
        sheet_slug="allchinabuy",
        invites=FORBIDDEN_ACBUY,
        factory_pats=(
            r"ACBuy is the current AllChinaBuy brand name[^.<]{0,200}",
            r"acbuyspreadsheets\.ca 301s here\.",
            r"Step-by-step guide to using ACBuy:[^.<]{0,240}\.",
        ),
        extra_subs=(),
        strip_home_crumb="Start",
        sections_h=sections_h,
        official_h=official_h,
        independence_h=independence_h,
        nav_aria=nav_aria,
        not_found_tab=not_found_tab,
    )


def _facts(key: str) -> dict:
    p = PACKS[key]
    return {
        "agent": "AllChinaBuy",
        "host": p["host"],
        "lang": p["lang"],
        "loc": p["loc"],
        "dest": p["dest"],
        "dest_label": p["dest_label"],
        "ccy": p["ccy"],
        "storage": (
            "Official AllChinaBuy (allchinabuy.com) showed a maintenance notice on "
            f"{DATE}; confirm live Help the morning you ship. This desk does not invent a free-day count."
        ),
        "estimator": EST,
        "official": OFFICIAL,
        "date": DATE,
        "keep": [
            ("/allchinabuy-shipping-guide/", "Shipping"),
            ("/is-allchinabuy-legit/", "Review"),
            ("/allchinabuy-spreadsheet/", "Spreadsheet"),
            ("/how-to-use-allchinabuy/", "Guide"),
        ],
        "codes_off_title": list(FORBIDDEN_ACBUY),
        "strict_html_codes": True,
    }


def _faqs(key: str) -> list[tuple[str, str]]:
    facts = _facts(key)
    p = PACKS[key]
    pairs = []
    for q, a in long_faqs(facts):
        a = a.replace("/api/products/", "w2clinks")
        a = a.replace("www.acbuy.com", "www.allchinabuy.com")
        if p["fingerprint"] not in a and "help" in q.lower():
            pass
        pairs.append((q, a))
    extra_en = (
        f"The delivery address uses a {p['postal']}. AllChinaBuy is not ACBuy; this hostname does not 301 into an ACBuy dest."
    )
    extra_nl = (
        f"Het afleveradres is een {p['postal']}. AllChinaBuy is niet ACBuy; deze host 301’t niet naar acbuyspreadsheets.nl."
    )
    extra = extra_nl if key == "nl" else extra_en
    if pairs:
        q0, a0 = pairs[0]
        if p["fingerprint"] not in a0:
            pairs[0] = (q0, a0 + " " + extra)
    else:
        pairs.append(("Postal / postcode?", extra))
    # Guarantee fingerprint on help.
    blob = " ".join(a for _, a in pairs)
    if p["fingerprint"] not in blob:
        pairs.append(
            (
                "Which postcode belongs on this dest?" if key != "nl" else "Welke postcode hoort bij dit dest?",
                extra,
            )
        )
    return pairs


def _faq_html(pairs: list[tuple[str, str]], *, open_first: bool = True) -> str:
    items = []
    for i, (q, a) in enumerate(pairs):
        op = " open" if open_first and i == 0 else ""
        items.append(
            f'<details class="sg-faq"{op}><summary>{escape(q)}</summary><p>{escape(a)}</p></details>'
        )
    return "\n".join(items)


def _cats(key: str):
    return list(W2C_CATS_NL) if key == "nl" else cats_for(EN_LABELS)


def _sheet(desk: CountryDesk) -> str:
    return w2c_sheet(desk)


def _fig(src: str, alt: str, cap: str, w: int = 1200, h: int = 750) -> str:
    return cms_fig(src, alt, cap, w, h)



def _status_ul(key: str) -> str:
    loc = PACKS[key]["loc"]
    rows = {
        "de": [
            ("Order Submitted", "Bestellung gesendet, Produkt in China bezahlt."),
            ("Order Placed", "AllChinaBuy kauft im chinesischen Shop auf deinen Namen."),
            ("Seller Shipped", "Der chinesische Verkäufer hat versandt."),
            ("Arrived at Warehouse", "Im Lager angekommen."),
            ("Inspection & Storage", "Prüfung, Fotos und Lager. Live-Labels stehen in der App."),
            ("Shipping Requested", "Du bündelst und buchst die internationale Linie."),
            ("Parcel Packed", "Die Box wird gepackt."),
            ("Shipped", "Abfahrt aus China."),
            ("Delivered", "Zugestellt; Empfang in der App bestätigen."),
        ],
        "it": [
            ("Order Submitted", "Ordine inviato, prodotto pagato in Cina."),
            ("Order Placed", "AllChinaBuy compra nel negozio cinese a tuo nome."),
            ("Seller Shipped", "Il venditore cinese ha spedito."),
            ("Arrived at Warehouse", "Arrivato in magazzino."),
            ("Inspection & Storage", "Controllo, foto e stoccaggio. Le etichette live stanno in app."),
            ("Shipping Requested", "Tu consolidi e prenoti la linea internazionale."),
            ("Parcel Packed", "La scatola viene imballata."),
            ("Shipped", "Partenza dalla Cina."),
            ("Delivered", "Consegnato; conferma in app."),
        ],
        "es": [
            ("Order Submitted", "Pedido enviado, producto pagado en China."),
            ("Order Placed", "AllChinaBuy compra en la tienda china a tu nombre."),
            ("Seller Shipped", "El vendedor chino ha enviado."),
            ("Arrived at Warehouse", "Llegó al almacén."),
            ("Inspection & Storage", "Control, fotos y almacenamiento. Las etiquetas en vivo están en la app."),
            ("Shipping Requested", "Tú consolidas y reservas la línea internacional."),
            ("Parcel Packed", "La caja se empaca."),
            ("Shipped", "Salida de China."),
            ("Delivered", "Entregado; confirma en la app."),
        ],
        "fr": [
            ("Order Submitted", "Commande envoyée, produit payé en Chine."),
            ("Order Placed", "AllChinaBuy achète dans la boutique chinoise à ton nom."),
            ("Seller Shipped", "Le vendeur chinois a expédié."),
            ("Arrived at Warehouse", "Arrivé à l’entrepôt."),
            ("Inspection & Storage", "Contrôle, photos et stockage. Les libellés live sont dans l’app."),
            ("Shipping Requested", "Tu regroupes et réserves la ligne internationale."),
            ("Parcel Packed", "La boîte est emballée."),
            ("Shipped", "Départ de Chine."),
            ("Delivered", "Livré ; confirme dans l’app."),
        ],
        "nl": [
            ("Order Submitted", "Bestelling verstuurd, product in China betaald."),
            ("Order Placed", "AllChinaBuy koopt in de Chinese shop op jouw naam."),
            ("Seller Shipped", "De Chinese verkoper heeft verzonden."),
            ("Arrived at Warehouse", "Aangekomen in het magazijn."),
            ("Inspection & Storage", "Controle, foto’s en opslag. Live labels staan in de app."),
            ("Shipping Requested", "Jij bundelt en boekt de internationale lijn."),
            ("Parcel Packed", "De doos wordt ingepakt."),
            ("Shipped", "Vertrek uit China."),
            ("Delivered", "Bezorgd; ontvangst bevestigen in de app."),
        ],
        "en": [
            ("Order Submitted", "Order sent, product paid in China."),
            ("Order Placed", "AllChinaBuy buys in the Chinese shop in your name."),
            ("Seller Shipped", "The Chinese seller has shipped."),
            ("Arrived at Warehouse", "Arrived at the warehouse."),
            ("Inspection & Storage", "Check, photos and storage. Live labels sit in the app."),
            ("Shipping Requested", "You consolidate and book the international line."),
            ("Parcel Packed", "The box is packed."),
            ("Shipped", "Departure from China."),
            ("Delivered", "Delivered; confirm receipt in the app."),
        ],
    }[loc if loc in ("de", "it", "es", "fr", "nl") else "en"]
    return '<ul class="tl">' + "".join(
        f"<li><b>{escape(a)}</b><span>{escape(b)}</span></li>" for a, b in rows
    ) + "</ul>"


def _sec_states(key: str, fig) -> str:
    p = PACKS[key]
    loc, dest = p["loc"], p["dest_label"]
    if loc == "nl":
        return f"""
<section class="sec" id="states">
  <div class="wrap"><div class="split"><div>
    <h2>Negen statussen, drie schermen</h2>
    <p class="lead">Eerst betaal je het product plus het binnenlandse traject in China tot het magazijn. Internationaal komt later, als je een lijn naar {escape(dest)} kiest. «Waarom staat het stil?» betekent bijna altijd: je kijkt naar het verkeerde scherm.</p>
    {_status_ul(key)}
    <p>De eerste stappen staan onder bestellingen, daarna magazijn, daarna het pakket dat je verzendt. Op {escape(DATE)} toonde allchinabuy.com onderhoud: deze gids verzint geen gratis-opslagdagen.</p>
    <p><a class="btn" href="{escape(p["guide"])}">Handleiding met het pad</a></p>
  </div>{fig}</div></div>
</section>
"""
    return f"""
<section class="sec" id="states">
  <div class="wrap"><div class="split"><div>
    <h2>Nine statuses, three screens</h2>
    <p class="lead">You first pay the product plus domestic China freight to the warehouse. International comes later, when you pick a line to {escape(dest)}. “Why is it stuck?” is almost always: you are looking at the wrong screen.</p>
    {_status_ul(key)}
    <p>The first stretch lives under orders, then warehouse, then the parcel you submit. On {escape(DATE)} the official site showed maintenance: this desk does not invent a free-storage day count.</p>
    <p><a class="btn" href="{escape(p["guide"])}">Guide with the path</a></p>
  </div>{fig}</div></div>
</section>
"""


def build_home(key: str) -> str:
    p = PACKS[key]
    desk = desk_for(key)
    sheet = _sheet(desk)
    cats = _cats(key)
    wall = "".join(
        f'<a class="cat" href="{escape(sheet)}?category={quote_plus(ckey)}&amp;page=1&amp;sort=newest" '
        f'rel="noopener" target="_blank">'
        f'<img src="{escape(W2C)}/public/static/w2c/categories/{escape(fn)}" alt="{escape(ckey)}" '
        f'loading="lazy" decoding="async" width="96" height="96">'
        f'<div class="cat__b"><strong>{escape(labn)}</strong><span>{escape(ckey)}</span></div></a>'
        for ckey, labn, fn in cats
    )
    chips = "".join(
        f'<a href="{escape(sheet)}?q={quote_plus(ckey.lower())}&amp;utm_source={escape(p["host"])}&amp;utm_medium=referral&amp;utm_campaign=hero-chips" '
        f'rel="nofollow noopener" target="_blank">{escape(ckey.lower() if ckey.isupper() else ckey)}</a>'
        for ckey, _lab, _fn in cats[:8]
    )
    fig_off = _fig(
        "/img/shots/oficial-maintenance.jpg",
        "Official AllChinaBuy homepage on 6 Oct 2026: maintenance notice, not a live estimator",
        f"Official allchinabuy.com, {DATE}. The public site showed a maintenance notice after an attack. This desk does not invent a line or a dollar amount from that day.",
    )
    fig_sheet = _fig(
        "/img/shots/catalogus.jpg",
        "AllChinaBuy catalogue on w2clinks: product cards with photo, brand and reference price",
        "Cards, not Excel cells. Yuan prices change by the day. Capture 6 Oct 2026, category SNEAKERS.",
        1200,
        900,
    )
    fig_vol = _fig(
        "/img/shots/volume-voorbeeld.jpg",
        "Worked example of volume weight: 40×40×3 cm and 200 g scale becomes 600 g volume",
        "A worked example, not a warehouse photo. Many lines bill the greater of scale and volume, often L×W×H (cm) / 8000. Run your box on the official estimator when it is back.",
        1200,
        640,
    )
    dest = p["dest_label"]
    states = _sec_states(key, fig_off)
    if key == "nl":
        body = f"""
<section class="hero">
  <div class="hero__bg" role="img" aria-label="AllChinaBuy-woordmerk op groene achtergrond"></div>
  <div class="hero__scrim"></div>
  <div class="wrap">
    <span class="eyebrow">{escape(p["eyebrow"])}</span>
    <h1>{escape(p["hero_h1"])}</h1>
    <p class="lead">{escape(p["lead"])}</p>
    <div class="sbox">
      <form id="w2c-search" action="{escape(sheet)}" method="get" target="_blank" rel="nofollow noopener" role="search">
        <label class="skip" for="q">Zoek producten op w2clinks</label>
        <input id="q" name="q" type="search" autocomplete="off" placeholder="Zoek sneakers, hoodie, jas…">
        <input type="hidden" name="utm_source" value="{escape(p["host"])}">
        <input type="hidden" name="utm_medium" value="referral">
        <input type="hidden" name="utm_campaign" value="hero-buscador">
        <button type="submit">Zoeken</button>
      </form>
      <div class="chips">{chips}</div>
    </div>
  </div>
</section>
<section class="sec sec--first" id="agent">
  <div class="wrap">
    <div class="split">
      <div>
        <h2>Een inkoopagent is een tussenpersoon, geen winkel</h2>
        <p class="lead">AllChinaBuy verkoopt zelf niets. Hij koopt voor jou in Chinese shops die niet naar het buitenland sturen, ontvangt het pakket in het magazijn, fotografeert het, bewaart het, en stuurt het naar Nederland wanneer jij dat besluit.</p>
        <p>Dat verandert alles: je betaalt twee keer (eerst het product, daarna internationaal), je wacht twee keer, en ertussen kun je nog annuleren, bundelen of van lijn wisselen. Betalen en tickets blijven op {escape(OFFICIAL)}. AllChinaBuy is een andere agent dan ACBuy.</p>
        <p><a class="btn" href="{escape(p["guide"])}">Handleiding stap voor stap</a></p>
      </div>
      {fig_off}
    </div>
  </div>
</section>
<section class="sec sec--tint" id="sheet-explain">
  <div class="wrap">
    <div class="split split--rev">
      <div>
        <span class="eyebrow" style="color:var(--acd)">Naam die misleidt</span>
        <h2>Een spreadsheet is geen Excel-bestand</h2>
        <p class="lead">In het Nederlands leidt het woord af. Hier betekent «spreadsheet» geen tabel van rijen en kolommen: het is een catalogus van productkaarten met foto, merk, referentieprijs en de link om in de agent te plakken.</p>
        <p>Wat je op w2clinks ziet zijn kaarten, geen cellen. Elke fiche heeft de link die AllChinaBuy nodig heeft.</p>
        <p><a class="btn btn--ghost" href="{escape(p["catalog"])}">Hoe de catalogus werkt</a></p>
      </div>
      {fig_sheet}
    </div>
  </div>
</section>
<section class="sec" id="cat-wall">
  <div class="wrap">
    <h2>Drieëndertig categorieën voor de eerste dag</h2>
    <p class="lead">Elke kaart opent de bijbehorende categorie in de catalogus. Begin met één.</p>
    <div class="cat-grid">{wall}</div>
  </div>
</section>
<section class="sec sec--tint" id="lab">
  <div class="wrap">
    <div class="split">
      <div>
        <h2>Nederland heeft lijnen, maar niet elke lijn is open</h2>
        <p class="lead">Kies destination <strong>{escape(p["dest_zh"])}</strong>, niet EU en niet Netherlands Antilles. Het afleveradres is een {escape(p["postal"])}.</p>
        <p>Op {escape(DATE)} toonde allchinabuy.com een onderhoudsmelding, geen live schatter. Deze gids verzint geen lijn, geen transittijd en geen eurobedrag. Open de officiële site op de verzenddag. Invoer: <a href="{escape(p["customs_url"])}" rel="noopener">{escape(p["customs"])}</a>.</p>
        <p><a class="btn" href="{escape(EST)}">Officiële AllChinaBuy-site</a>
           <a class="btn btn--ghost" href="{escape(p["ship"])}">Verzendplan</a></p>
      </div>
      {fig_off}
    </div>
  </div>
</section>
<section class="sec" id="volume">
  <div class="wrap">
    <div class="split split--rev">
      <div>
        <h2>Het gewicht dat je betaalt is bijna nooit alleen de weegschaal</h2>
        <p class="lead">Veel lijnen factureren het maximum van weegschaal en volume. Een veelgebruikte deler is L×W×H (cm) / 8000. Een donsjas is licht en volumineus: daar beslist het volume.</p>
        <p>Voorbeeld: 40×40×3 cm is 4800 cm³, gedeeld door 8000 is 600 g volume bij 200 g echt gewicht. Jouw maten vul je in de officiële schatter wanneer die weer live is, bestemming Nederland.</p>
      </div>
      {fig_vol}
    </div>
  </div>
</section>
{states}
<section class="sec" id="faq">
  <div class="wrap">
    <h2>Hulp, nieuws en waar je vraagt</h2>
    <p class="lead">De meeste twijfels van de eerste orders herhalen zich. Ze staan beantwoord in het Nederlands op Hulp — een eigen URL, geen bijlage van deze homepage.</p>
    <p><a class="btn" href="{escape(p["help"])}">Alle vragen op Hulp</a>
       <a class="btn btn--ghost" href="{escape(p["news"])}">Gedateerde checks op Nieuws</a>
       <a class="btn btn--ghost" href="{escape(p["about"])}">Over ons</a></p>
  </div>
</section>
"""
        desc = "Onafhankelijke gids in het Nederlands: hoe je via AllChinaBuy in China koopt, hoe de catalogus van w2clinks werkt, hoe een pakket naar Nederland reist."
    else:
        body = f"""
<section class="hero">
  <div class="hero__bg" role="img" aria-label="AllChinaBuy wordmark on a green field"></div>
  <div class="hero__scrim"></div>
  <div class="wrap">
    <span class="eyebrow">{escape(p["eyebrow"])}</span>
    <h1>{escape(p["hero_h1"])}</h1>
    <p class="lead">{escape(p["lead"])}</p>
    <div class="sbox">
      <form id="w2c-search" action="{escape(sheet)}" method="get" target="_blank" rel="nofollow noopener" role="search">
        <label class="skip" for="q">Search products on w2clinks</label>
        <input id="q" name="q" type="search" autocomplete="off" placeholder="Search sneakers, hoodie, jacket…">
        <input type="hidden" name="utm_source" value="{escape(p["host"])}">
        <input type="hidden" name="utm_medium" value="referral">
        <input type="hidden" name="utm_campaign" value="hero-buscador">
        <button type="submit">Search</button>
      </form>
      <div class="chips">{chips}</div>
    </div>
  </div>
</section>
<section class="sec sec--first" id="agent">
  <div class="wrap">
    <div class="split">
      <div>
        <h2>A purchasing agent is a middleman, not a shop</h2>
        <p class="lead">AllChinaBuy does not sell its own goods. It buys for you in Chinese shops that do not ship abroad, receives the parcel in the warehouse, photographs it, stores it, and ships to {escape(dest)} when you decide.</p>
        <p>That changes everything: you pay twice (first the product, later international), you wait twice, and in between you can still cancel, consolidate or switch lines. Payment and tickets stay on {escape(OFFICIAL)}. AllChinaBuy is a different purchasing agent from ACBuy.</p>
        <p><a class="btn" href="{escape(p["guide"])}">Step-by-step guide</a></p>
      </div>
      {fig_off}
    </div>
  </div>
</section>
<section class="sec sec--tint" id="sheet-explain">
  <div class="wrap">
    <div class="split split--rev">
      <div>
        <span class="eyebrow" style="color:var(--acd)">A name that misleads</span>
        <h2>A spreadsheet is not an Excel file</h2>
        <p class="lead">In English the word still sounds like a grid of rows and columns. Here «spreadsheet» means a catalogue of product cards with a photo, a brand, a reference price and the link you paste into the agent.</p>
        <p>What you see on w2clinks are cards, not cells. Each fiche has the link AllChinaBuy needs.</p>
        <p><a class="btn btn--ghost" href="{escape(p["catalog"])}">How the catalogue works</a></p>
      </div>
      {fig_sheet}
    </div>
  </div>
</section>
<section class="sec" id="cat-wall">
  <div class="wrap">
    <h2>Thirty-three categories for the first day</h2>
    <p class="lead">Each card opens that category in the catalogue. Start with one.</p>
    <div class="cat-grid">{wall}</div>
  </div>
</section>
<section class="sec sec--tint" id="lab">
  <div class="wrap">
    <div class="split">
      <div>
        <h2>{escape(dest).capitalize() if dest[0].islower() else dest} has lines, but not every line is open</h2>
        <p class="lead">Pick destination <strong>{escape(p["dest_zh"])}</strong> in the official estimator when it is live. The delivery address is a {escape(p["postal"])}.</p>
        <p>On {escape(DATE)} the official AllChinaBuy site showed a maintenance notice, not a live estimator. This desk does not invent a line, a transit-day count or a money amount. Open {escape(OFFICIAL)} the morning you ship. Import: <a href="{escape(p["customs_url"])}" rel="noopener">{escape(p["customs"])}</a>.</p>
        <p><a class="btn" href="{escape(EST)}">Official AllChinaBuy site</a>
           <a class="btn btn--ghost" href="{escape(p["ship"])}">Shipping plan</a></p>
      </div>
      {fig_off}
    </div>
  </div>
</section>
<section class="sec" id="volume">
  <div class="wrap">
    <div class="split split--rev">
      <div>
        <h2>The weight you pay is almost never the scale alone</h2>
        <p class="lead">Many lines bill the greater of scale and volume. A common divisor is L×W×H (cm) / 8000. A down jacket is light and bulky: volume decides.</p>
        <p>Example: 40×40×3 cm is 4800 cm³, divided by 8000 is 600 g volume at 200 g real weight. You enter your measurements in the official estimator when it is back, destination {escape(p["dest_zh"].split("—")[0].strip())}.</p>
      </div>
      {fig_vol}
    </div>
  </div>
</section>
{states}
<section class="sec" id="faq">
  <div class="wrap">
    <h2>Help, news and where to ask</h2>
    <p class="lead">Most first-order doubts repeat. They are answered on Help — its own URL, not an appendix of this homepage.</p>
    <p><a class="btn" href="{escape(p["help"])}">All questions on Help</a>
       <a class="btn btn--ghost" href="{escape(p["news"])}">Dated checks on News</a>
       <a class="btn btn--ghost" href="{escape(p["about"])}">About us</a></p>
  </div>
</section>
"""
        desc = (
            f"Independent English guide: how you buy in China through AllChinaBuy, how the w2clinks catalogue works, how a parcel travels to {dest}."
        )
    return cms_shell(
        desk,
        page_title(desk, p["home_topic"]),
        desc,
        f"https://{p['host']}/",
        [faq_ld(p["lang"], _faqs(key))],
        body,
        "/start/",
    )


def build_catalog(key: str) -> str:
    p = PACKS[key]
    desk = desk_for(key)
    sheet = _sheet(desk)
    notes = CAT_NOTES_EN
    cats = _cats(key)
    wall = "".join(
        f'<a class="cat" href="{escape(sheet)}?category={quote_plus(ckey)}&amp;page=1&amp;sort=newest" '
        f'rel="noopener" target="_blank">'
        f'<img src="{escape(W2C)}/public/static/w2c/categories/{escape(fn)}" alt="{escape(ckey)}" '
        f'loading="lazy" decoding="async" width="96" height="96">'
        f'<div class="cat__b"><strong>{escape(labn)}</strong><span>{escape(ckey)}</span>'
        f"<em>{escape(notes.get(ckey, ""))}</em></div></a>"
        for ckey, labn, fn in cats
    )
    fig_sheet = _fig(
        "/img/shots/catalogus.jpg",
        "AllChinaBuy catalogue on w2clinks",
        "A catalogue category: cards with image, brand and a reference price in yuan. Capture 6 Oct 2026.",
        1200,
        900,
    )
    fig_zoek = _fig(
        "/img/shots/catalogus-zoek.jpg",
        "Hoodie search in the AllChinaBuy catalogue on w2clinks",
        "Results with the filter column. Capture 6 Oct 2026.",
        1200,
        900,
    )
    if key == "nl":
        h1 = "Wat AllChinaBuy Spreadsheet is, en wat je erin vindt"
        lead = "Het is een catalogus van productkaarten, geen Excel-bestand. Je bladert zoals in een shop: drieëndertig categorieën."
        pick = "Hoe je de eerste categorie kiest"
        source = "source link"
        title_topic = "wat het is en welke categorieën je vindt"
        body = f"""
<section class="sec sec--first"><div class="wrap"><div class="split"><div>
<span class="eyebrow" style="color:var(--acc)">De catalogus</span>
<h1>{h1}</h1>
<p class="lead">{lead}</p>
<p>Het woord misleidt nog: «spreadsheet» klinkt als een raster. Hier zijn het fiches. Elke fiche is een product uit een Chinese shop, met de {source} die je in AllChinaBuy plakt.</p>
</div>{fig_sheet}</div></div></section>
<section class="sec sec--tint"><div class="wrap"><div class="split split--rev"><div>
<h2>Waarom een aparte catalogus</h2>
<p>De zoekbalk van een agent geeft de hele Chinese voorraad. Een catalogus doet het huiswerk: iemand koos al welke fiches de moeite waard zijn.</p>
</div>{fig_zoek}</div></div></section>
<section class="sec" id="categorias"><div class="wrap">
<h2>De drieëndertig categorieën</h2>
<div class="cat-grid cat-grid--rich">{wall}</div>
</div></section>
<section class="sec sec--tint" id="first-category"><div class="wrap">
<h2>{pick}</h2>
<p class="lead">Eerste order: kies iets plats en lichts. Dons en tassen bewaren voor de tweede ronde, omdat volume daar de prijs maakt.</p>
</div></section>
"""
    else:
        h1 = "What AllChinaBuy Spreadsheet is, and what you find in it"
        title_topic = "what it is and which categories you will find"
        body = f"""
<section class="sec sec--first"><div class="wrap"><div class="split"><div>
<span class="eyebrow" style="color:var(--acc)">The catalogue</span>
<h1>{h1}</h1>
<p class="lead">It is a catalogue of product cards, not an Excel file. You browse as in a shop: thirty-three categories, filters, and cards with a photo, a brand and the link for the agent. Below are those categories, with what you check in each.</p>
<p>The name still misleads in English, because «spreadsheet» literally means a grid. There are no rows, cells or tabs here: there are fiches. Each fiche is a concrete product from a Chinese shop, with an image, a category and the source link you then paste into AllChinaBuy.</p>
</div>{fig_sheet}</div></div></section>
<section class="sec sec--tint"><div class="wrap"><div class="split split--rev"><div>
<h2>Why a separate catalogue</h2>
<p>An agent search bar returns the whole stock of Chinese shops. A catalogue does the homework: someone already picked which fiches are worth it.</p>
</div>{fig_zoek}</div></div></section>
<section class="sec" id="categorias"><div class="wrap">
<h2>The thirty-three categories, and what you check in each</h2>
<div class="cat-grid cat-grid--rich">{wall}</div>
</div></section>
<section class="sec sec--tint" id="first-category"><div class="wrap">
<h2>How you pick the first category</h2>
<p class="lead">If it is your first order, pick something flat and light: T-shirts, shorts, jewelry. Leave bulky for the second order: down jackets, bags, hats.</p>
<p>The source link on the fiche is what AllChinaBuy needs — not the URL of the catalogue card itself.</p>
</div></section>
"""
    return cms_shell(
        desk,
        page_title(desk, title_topic),
        "Independent catalogue guide: thirty-three w2clinks categories.",
        f"https://{p['host']}{p['catalog']}",
        [],
        body,
        p["catalog"],
    )


def build_help(key: str) -> str:
    p = PACKS[key]
    desk = desk_for(key)
    pairs = _faqs(key)
    html_f = _faq_html(pairs, open_first=True)
    fig = _fig(
        "/img/shots/oficial-maintenance.jpg",
        "Official AllChinaBuy site on 6 Oct 2026",
        "Parcel questions belong in official chat when the site is back. Capture 6 Oct 2026.",
    )
    if key == "nl":
        body = f"""
<article class="pw">
  <span class="eyebrow" style="color:var(--acd)">Hulp</span>
  <h1>Hulp en vragen over AllChinaBuy in Nederland</h1>
  <p class="lead">Vragen van eerste orders, beantwoord met wat we zelf nakeken. Het afleveradres is een {escape(p["postal"])}.</p>
  {fig}
  {html_f}
  <p><a class="btn" href="{escape(EST)}">Officiële AllChinaBuy-site</a>
     <a class="btn btn--ghost" href="{escape(p["ship"])}">Verzendplan</a></p>
</article>
"""
        topic = "hulp en veelgestelde vragen"
    else:
        body = f"""
<article class="pw">
  <span class="eyebrow" style="color:var(--acd)">Help</span>
  <h1>Help and questions about AllChinaBuy in {escape(p["dest_label"])}</h1>
  <p class="lead">Questions that come back on first orders. The delivery address uses a {escape(p["postal"])}.</p>
  {fig}
  {html_f}
  <p><a class="btn" href="{escape(EST)}">Official AllChinaBuy site</a>
     <a class="btn btn--ghost" href="{escape(p["ship"])}">Shipping plan</a></p>
</article>
"""
        topic = "help and frequently asked questions"
    return cms_shell(
        desk,
        page_title(desk, topic),
        f"FAQ about AllChinaBuy from {p['dest_label']}.",
        f"https://{p['host']}{p['help']}",
        [faq_ld(p["lang"], pairs)],
        body,
        p["help"],
    )


def build_news(key: str) -> str:
    p = PACKS[key]
    desk = desk_for(key)
    if key == "nl":
        items = [
            (
                "Eerste ronde: allchinabuy.com stond in onderhoud",
                f"Op {DATE} toonde de officiële site een onderhoudsmelding, geen live schatter. Deze gids verzint geen lijn en geen bedrag.",
                "Wat dat voor jou betekent: open de officiële site op de verzenddag, bestemming Netherlands — 荷兰, Nederlandse postcode.",
            ),
            (
                "De catalogus van w2clinks zoekt in het Engels",
                "sneakers, hoodie en jacket gaven pagina’s; turnschoenen vaak nul. Gemeten 6 Oct 2026.",
                "Typ de Engelse key, of tik een chip op de homepage.",
            ),
            (
                "AllChinaBuy is niet ACBuy",
                "Dit is een andere inkoopagent. allchinabuyspreadsheet.nl 301’t niet naar acbuyspreadsheets.nl.",
                "Twee land-URL’s van dezelfde agent blijven ook uit elkaar: CA, NL en UK elk hun eigen host.",
            ),
            (
                "Volumgewicht",
                "Veel lijnen nemen het maximum van weegschaal en L×W×H/8000. Geen SKU-prijs in deze HTML.",
                "Reken jouw doos in de officiële schatter wanneer die weer live is.",
            ),
            (
                "Hoe we dit checken",
                "Geen verzonnen transittijden. Rankende gidsen (verzending, review, handleiding) blijven eigen URL’s.",
                "Feiten die veranderen, komen met datum op deze pagina.",
            ),
        ]
        h1 = "Wat we op het platform hebben nagekeken, met datum"
        topic = "wat we op het platform hebben nagekeken"
    else:
        items = [
            (
                f"First round: official AllChinaBuy site was in maintenance",
                f"On {DATE} allchinabuy.com showed a maintenance notice, not a live estimator. This guide does not invent a line or an amount.",
                f"What that means for you: open the official site the morning you ship. Destination {p['dest_zh']}. {p['postal']}.",
            ),
            (
                "The w2clinks catalogue searches in English",
                "sneakers, hoodie and jacket returned pages; local spellings often returned zero. Measured 6 Oct 2026.",
                "Type the English key, or tap a chip on the homepage.",
            ),
            (
                "AllChinaBuy is not ACBuy",
                "This is a different purchasing agent. This hostname does not 301 into an ACBuy country dest.",
                "Canada, the Netherlands and the UK on AllChinaBuy also stay on their own hosts.",
            ),
            (
                "Volume weight",
                "Many lines bill the greater of scale and L×W×H/8000. No SKU price in this HTML.",
                "Run your box on the official estimator when it is back.",
            ),
            (
                "How we check this",
                "No invented transit days. Ranked guides stay their own URLs.",
                "If a fact changes, it is listed here with the date of the new check.",
            ),
        ]
        h1 = "What we checked on the platform, with a date"
        topic = "what we checked on the platform"
    ld = itemlist_ld(
        url=f"https://{p['host']}{p['news']}",
        name="AllChinaBuy dest checks",
        items=[(h, f"{x} {y}") for h, x, y in items],
    )
    cards = "".join(
        f'<article class="ncard"><h2>{escape(h)}</h2><p>{escape(x)}</p><p>{escape(y)}</p></article>'
        for h, x, y in items
    )
    body = f"""
<article class="pw">
  <span class="eyebrow" style="color:var(--acd)">{"Nieuws" if key == "nl" else "News"}</span>
  <h1>{escape(h1)}</h1>
  <p class="lead">{"Dit is geen bedrijfsnieuwsbrief. Het zijn eigen checks, met datum." if key == "nl" else "This is not a company newsletter. These are our own checks, with a date."}</p>
  <p>{"Eerste ronde" if key == "nl" else "First round"}: {escape(DATE)}.</p>
  {cards}
</article>
"""
    return cms_shell(
        desk,
        page_title(desk, topic),
        "Dated checks on AllChinaBuy.",
        f"https://{p['host']}{p['news']}",
        [ld],
        body,
        p["news"],
    )


def build_about(key: str) -> str:
    p = PACKS[key]
    desk = desk_for(key)
    fig = _fig(
        "/img/shots/oficial-maintenance.jpg",
        "Official AllChinaBuy site, a different URL from this guide",
        f"Official allchinabuy.com on {DATE}.",
    )
    if key == "nl":
        body = f"""
<article class="pw">
  <span class="eyebrow" style="color:var(--acd)">Over ons</span>
  <h1>Een onafhankelijke site over AllChinaBuy, in het Nederlands</h1>
  <p class="lead">AllChinaBuy Spreadsheet is niet AllChinaBuy. Het is een redactionele gids. AllChinaBuy is ook niet ACBuy.</p>
  {fig}
  <h2>Contact</h2>
  <p>Orders: officiële site. Deze gids: <a href="mailto:{escape(MAIL)}">{escape(MAIL)}</a>.</p>
</article>
"""
        topic = "wie we zijn en hoe je ons bereikt"
    else:
        body = f"""
<article class="pw">
  <span class="eyebrow" style="color:var(--acd)">About us</span>
  <h1>An independent site about AllChinaBuy, in English</h1>
  <p class="lead">AllChinaBuy Spreadsheet is not AllChinaBuy. It is an editorial guide. AllChinaBuy is a different purchasing agent from ACBuy.</p>
  {fig}
  <h2>How we work</h2>
  <p>Shipping figures would come from the public estimator. On {escape(DATE)} that site was in maintenance, so this desk published no invented rate. Import points to <a href="{escape(p["customs_url"])}" rel="noopener">{escape(p["customs"])}</a>.</p>
  <h2>Contact</h2>
  <p>Orders: official AllChinaBuy chat when the site is back. This guide: <a href="mailto:{escape(MAIL)}">{escape(MAIL)}</a>.</p>
</article>
"""
        topic = "who we are and how to reach us"
    return cms_shell(
        desk,
        page_title(desk, topic),
        "Independent AllChinaBuy guide: how we check facts.",
        f"https://{p['host']}{p['about']}",
        [],
        body,
        p["about"],
    )


def _assert_ok(html: str, page: str, key: str) -> None:
    p = PACKS[key]
    desk = desk_for(key)
    if page == "nf":
        if p["not_found_tab"] not in html or MAIL not in html:
            raise SystemExit(f"{key} nf chrome")
        if 'href="/start/"' not in html:
            raise SystemExit(f"{key} nf Start")
        return
    skip = {
        "missing #local dest briefing",
        "missing #local",
        "missing #catalog",
        "missing catalogue API",
        f"missing FX_CCY {p['ccy']}",
                "missing #restricted",
        "missing #shots",
        "faq count 0",
    }
    err = [e for e in validate_desk(html, _facts(key), page=page) if e not in skip]
    if page == "home":
        err = [e for e in err if not e.startswith("faq count")]
    if page == "home":
        if page_title(desk, p["home_topic"]) not in html:
            err.append("home title")
        if p["fingerprint"] not in html:
            err.append("fingerprint")
        if "not an Excel file" not in html and "geen Excel-bestand" not in html:
            err.append("sheet-explain")
        if "cat-30-shoes.png" not in html or "w2clinks.com/spreadsheet/allchinabuy" not in html:
            err.append("W2C cats")
        if MAIL not in html or ("Independence notice" not in html and "Onafhankelijkheidsverklaring" not in html):
            err.append("footer")
        if 'id="local"' in html or "/api/products/" in html:
            err.append("ops leftover")
        if p["dest_zh"] not in html:
            err.append("estimator dest")
        if "www.acbuy.com" in html:
            err.append("acbuy.com leak")
        if html.count('class="sg-faq"') >= 8:
            err.append("faq dump")
        if 'class="fig"' not in html:
            err.append("photos")
        if 'class="tl"' not in html:
            err.append("status timeline")
        for alien in p["aliens"]:
            if alien in html:
                err.append(f"alien {alien}")
        for tok in FORBIDDEN_ACBUY:
            if tok in html:
                err.append(f"invite {tok}")
    if page == "help" and p["fingerprint"] not in html:
        err.append("help fingerprint")
    if err:
        raise SystemExit(f"{key}/{page}: {'; '.join(err)}")


def _overlay(key: str) -> Path:
    return OUT / PACKS[key]["host"] / "overlay"


def _copy_assets(dest: Path) -> None:
    img = dest / "img"
    (img / "shots").mkdir(parents=True, exist_ok=True)
    (img / "cat").mkdir(exist_ok=True)
    (dest / "assets" / "images").mkdir(parents=True, exist_ok=True)
    (dest / "assets" / "css").mkdir(parents=True, exist_ok=True)
    shutil.copy("/tmp/acb-official-logo.png", dest / "assets" / "images" / "allchinabuy-logo.png")
    shutil.copy("/tmp/acb-hero.jpg", img / "hero.jpg")
    shutil.copy("/tmp/acb-favicon.png", dest / "favicon.ico")
    shutil.copy("/tmp/acb-hub-favicon.ico", dest / "favicon1.ico")
    for name in (
        "oficial-maintenance.jpg",
        "catalogus.jpg",
        "catalogus-zoek.jpg",
        "volume-voorbeeld.jpg",
    ):
        shutil.copy(f"/tmp/acb-shots/{name}", img / "shots" / name)


def generate(key: str) -> dict[str, Path]:
    p = PACKS[key]
    desk = desk_for(key)
    dest = _overlay(key)
    dest.mkdir(parents=True, exist_ok=True)
    for name in ("help", "news", "about", "catalog", "catalogus", "hulp", "nieuws", "over-ons", "start"):
        (dest / name).mkdir(exist_ok=True)
    _copy_assets(dest)
    css_path = dest / "assets" / "css" / p["desk_css"]
    css_path.write_text(render_css(desk), encoding="utf-8")
    theme = OUT / "shared" / "themes" / "allchinabuy-theme.css"
    theme.parent.mkdir(parents=True, exist_ok=True)
    theme.write_text(
        "/* AllChinaBuy country dest — official forest green from allchinabuy.com wordmark */\n"
        ":root { --primary: #18753C; --primary-dark: #0F5A2E; --primary-soft: #e8f5ee; --nav-dark: #111111; }\n",
        encoding="utf-8",
    )
    home = build_home(key)
    pages = {
        "home": (dest / "index.html", home, "home"),
        "start": (dest / "start" / "index.html", home, "home"),
        "help": (dest / p["help"].strip("/").split("/")[0] / "index.html", build_help(key), "help"),
        "news": (dest / p["news"].strip("/").split("/")[0] / "index.html", build_news(key), "news"),
        "about": (dest / p["about"].strip("/").split("/")[0] / "index.html", build_about(key), "about"),
        "catalog": (dest / p["catalog"].strip("/").split("/")[0] / "index.html", build_catalog(key), "catalog"),
        "nf": (dest / "404.html", build_404(desk), "nf"),
    }
    out: dict[str, Path] = {"css": css_path, "logo": dest / "assets" / "images" / "allchinabuy-logo.png"}
    for name, (path, html, page) in pages.items():
        _assert_ok(html, page, key)
        n = len(html.encode("utf-8"))
        if name in ("home", "start") and n < DEST_MIN:
            raise SystemExit(f"{key} {name} too small {n}")
        path.write_text(html, encoding="utf-8")
        print("wrote", path, n)
        out[name] = path
    return out


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


def _reload_nginx(client) -> None:
    chk = _run(client, "nginx -t")
    print(chk)
    if "successful" not in chk.lower() and "ok" not in chk.lower():
        raise SystemExit("nginx -t failed")
    print(_run(client, "nginx -s reload"))


CMS_PAGE_LOCS = (
    "about",
    "about/",
    "help",
    "help/",
    "news",
    "news/",
    "catalog",
    "catalog/",
    "catalogus",
    "catalogus/",
    "hulp",
    "hulp/",
    "nieuws",
    "nieuws/",
    "over-ons",
    "over-ons/",
    "start",
    "start/",
)

WRAP_SKIP_PREFIXES = (
    "help/",
    "news/",
    "about/",
    "catalog/",
    "catalogus/",
    "hulp/",
    "nieuws/",
    "over-ons/",
    "start/",
    "api/",
    "assets/",
    "img/",
)


def _strip_cms_home_301s(client, sftp, key: str) -> None:
    host = PACKS[key]["host"]
    gsc = f"/www/server/panel/vhost/nginx/extension/{host}/gsc-redirects.conf"
    raw = _run(client, f"cat '{gsc}' 2>/dev/null || true")
    if not raw:
        return
    drop = {f"location = /{loc} {{ return 301 https://{host}/; }}" for loc in CMS_PAGE_LOCS}
    keep = []
    stripped = 0
    for ln in raw.splitlines(True):
        if ln.strip() in drop:
            stripped += 1
            continue
        keep.append(ln)
    if not stripped:
        print(key, "no CMS-page home 301s")
        return
    stamp = time.strftime("%Y%m%d-%H%M%S")
    _run(client, f"cp -a '{gsc}' '/www/backup/allchinabuy-{key}-gsc-about-{stamp}.conf'")
    Path(f"/tmp/allchinabuy-{key}-gsc.conf").write_text("".join(keep), encoding="utf-8")
    sftp.put(f"/tmp/allchinabuy-{key}-gsc.conf", gsc)
    print(key, "stripped", stripped, "CMS-page home 301s")
    _reload_nginx(client)


def _harden_catchall(client, sftp, key: str) -> None:
    host = PACKS[key]["host"]
    vhost = f"/www/server/panel/vhost/nginx/{host}.conf"
    with sftp.open(vhost, "r") as fh:
        text = fh.read().decode()
    marker = f'X-Desk "allchinabuy-{key}-independent"'
    if marker in text:
        print(key, "catch-all already independent")
        return
    old = """    location / {
        try_files $uri $uri/ $uri/index.html =404;
    }
"""
    new = f"""    location / {{
        try_files $uri $uri/ $uri/index.html =404;
        add_header Strict-Transport-Security "max-age=31536000" always;
        add_header Cache-Control "private, no-cache, must-revalidate" always;
        add_header X-Desk "allchinabuy-{key}-independent" always;
    }}
"""
    if old not in text:
        print(key, "catch-all needle not the plain try_files; skip harden")
        return
    stamp = time.strftime("%Y%m%d-%H%M%S")
    _run(client, f"cp -a '{vhost}' '/www/backup/allchinabuy-{key}-nginx-{stamp}.conf'")
    text = text.replace(old, new, 1)
    tmp = Path(f"/tmp/allchinabuy-{key}.conf")
    tmp.write_text(text, encoding="utf-8")
    sftp.put(str(tmp), vhost)
    print(key, "hardened HTTPS catch-all")
    _reload_nginx(client)


def _origin_inners(client, root: str) -> list[str]:
    raw = _run(client, f"find '{root}' -name index.html | sed 's|^{root}/||'")
    rels = []
    for rel in raw.splitlines():
        rel = rel.strip().lstrip("/")
        if not rel or rel == "index.html":
            continue
        if any(rel == p.rstrip("/") or rel.startswith(p) for p in WRAP_SKIP_PREFIXES):
            continue
        rels.append(rel)
    return rels


def _lift_nl_acbuy_301(client, sftp) -> None:
    host = PACKS["nl"]["host"]
    vhost = f"/www/server/panel/vhost/nginx/{host}.conf"
    stamp = time.strftime("%Y%m%d-%H%M%S")
    _run(client, f"cp -a '{vhost}' '/www/backup/allchinabuy-nl-nginx-{stamp}.conf'")
    with sftp.open(vhost, "r") as fh:
        text = fh.read().decode()
    old = "    location / { return 301 https://acbuyspreadsheets.nl$request_uri; }\n"
    new = """    location / {
        try_files $uri $uri/ $uri/index.html =404;
        add_header Strict-Transport-Security "max-age=31536000" always;
        add_header Cache-Control "private, no-cache, must-revalidate" always;
        add_header X-Desk "allchinabuy-nl-independent" always;
    }
"""
    if old in text:
        text = text.replace(old, new, 1)
        tmp = Path("/tmp/allchinabuy-nl.conf")
        tmp.write_text(text, encoding="utf-8")
        sftp.put(str(tmp), vhost)
        print("lifted NL 301 into ACBuy NL")
    elif "allchinabuy-nl-independent" in text:
        print("NL catch-all already independent")
    elif "try_files $uri $uri/ $uri/index.html =404" in text and "acbuyspreadsheets.nl$request_uri" not in text:
        print("NL catch-all already try_files")
    else:
        raise SystemExit("NL catch-all 301 needle not found")
    gsc = f"/www/server/panel/vhost/nginx/extension/{host}/gsc-redirects.conf"
    raw = _run(client, f"cat '{gsc}'")
    if "acbuyspreadsheets.nl" in raw:
        _run(client, f"cp -a '{gsc}' '/www/backup/allchinabuy-nl-gsc-{stamp}.conf'")
        keep = [ln for ln in raw.splitlines(True) if "acbuyspreadsheets.nl" not in ln]
        Path("/tmp/allchinabuy-nl-gsc.conf").write_text("".join(keep), encoding="utf-8")
        sftp.put("/tmp/allchinabuy-nl-gsc.conf", gsc)
        print("stripped ACBuy 301s from NL gsc-redirects")
    _reload_nginx(client)


def _wrap_ranked(client, sftp, bak: str, root: str, key: str) -> None:
    desk = desk_for(key)
    skip = {"index.html", "404.html", "404/index.html"}
    inventory = Path("/tmp/dest-inners.json")
    rels: list[str] = []
    if inventory.is_file():
        for row in json.loads(inventory.read_text()):
            if row.get("host") == PACKS[key]["host"]:
                rels = [item["rel"].lstrip("/") for item in row.get("files") or []]
                break
    if not rels:
        rels = _origin_inners(client, root)
        print(key, "wrap inventory miss; origin inners", len(rels))
    if not rels:
        rels = [f"{rel.lstrip('/')}index.html" for rel, _ in RANKED]
    mins = {rel.lstrip("/"): min_b for rel, min_b in RANKED}
    for rel in rels:
        if rel in skip or any(rel == p.rstrip("/") or rel.startswith(p) for p in WRAP_SKIP_PREFIXES):
            continue
        remote = f"{root}/{rel}"
        try:
            with sftp.open(remote, "r") as fh:
                raw = fh.read().decode("utf-8", "replace")
        except OSError as exc:
            print("skip missing", rel, exc)
            continue
        href = "/" + str(Path(rel).parent).replace("\\", "/").rstrip("/") + "/"
        if href == "/./":
            href = "/"
        out, why = cms_wrap_inner(desk, raw, href)
        if out is None:
            print("inner", rel, why)
            continue
        min_b = 4000
        for prefix, floor in mins.items():
            if rel.startswith(prefix.lstrip("/")):
                min_b = floor
                break
        if len(out.encode("utf-8")) < min_b:
            print("WARN skip thin wrap", rel, len(out.encode("utf-8")))
            continue
        rel_dir = str(Path(rel).parent)
        _run(client, f"mkdir -p '{bak}/{rel_dir}'")
        _run(client, f"cp -a '{remote}' '{bak}/{rel}'")
        local_tmp = Path("/tmp") / f"acb-wrap-{key}-{rel.replace('/', '_')}"
        local_tmp.write_text(out, encoding="utf-8")
        sftp.put(str(local_tmp), remote)
        print("WRAP", rel, "in", len(raw), "out", len(out.encode("utf-8")))


def put(key: str) -> None:
    files = generate(key)
    p = PACKS[key]
    host = p["host"]
    client = _connect()
    stamp = time.strftime("%Y%m%d-%H%M%S")
    bak = f"/www/backup/allchinabuy-{key}-cms-{stamp}"
    root = f"/www/wwwroot/{host}"
    overlay = _overlay(key)
    _run(
        client,
        f"mkdir -p '{bak}' '{root}/help' '{root}/news' '{root}/about' '{root}/catalog' "
        f"'{root}/catalogus' '{root}/hulp' '{root}/nieuws' '{root}/over-ons' '{root}/start' "
        f"'{root}/assets/css' '{root}/assets/images' '{root}/img/shots'",
    )
    sftp = client.open_sftp()
    if key == "nl":
        _lift_nl_acbuy_301(client, sftp)
    else:
        _harden_catchall(client, sftp, key)
    _strip_cms_home_301s(client, sftp, key)
    mapping = {
        "home": f"{root}/index.html",
        "start": f"{root}/start/index.html",
        "help": f"{root}{p['help']}index.html",
        "news": f"{root}{p['news']}index.html",
        "about": f"{root}{p['about']}index.html",
        "catalog": f"{root}{p['catalog']}index.html",
        "nf": f"{root}/404.html",
    }
    for name, remote in mapping.items():
        local = files[name]
        raw = local.read_text(encoding="utf-8")
        if name in ("home", "start", "help") and p["fingerprint"] not in raw:
            raise SystemExit(f"refusing {key} {name} without fingerprint")
        if "www.acbuy.com" in raw:
            raise SystemExit(f"refusing {key} {name} with acbuy.com")
        _run(client, f"mkdir -p '{Path(remote).parent}'")
        sftp.put(str(local), remote)
        print("PUT", remote, local.stat().st_size)
    theme = OUT / "shared" / "themes" / "allchinabuy-theme.css"
    sftp.put(str(theme), f"{root}/assets/css/allchinabuy-theme.css")
    sftp.put(str(files["css"]), f"{root}/assets/css/{p['desk_css']}")
    sftp.put(str(overlay / "assets" / "images" / "allchinabuy-logo.png"), f"{root}/assets/images/allchinabuy-logo.png")
    sftp.put(str(overlay / "favicon.ico"), f"{root}/favicon.ico")
    sftp.put(str(overlay / "favicon1.ico"), f"{root}/favicon1.ico")
    sftp.put(str(overlay / "img" / "hero.jpg"), f"{root}/img/hero.jpg")
    for src in sorted((overlay / "img" / "shots").glob("*.jpg")):
        sftp.put(str(src), f"{root}/img/shots/{src.name}")
        print("PUT", src.name)
    _wrap_ranked(client, sftp, bak, root, key)
    _run(client, f"chown -R www:www '{root}' 2>/dev/null || true")
    sftp.close()
    print("backup", bak)
    client.close()


def live_check(key: str | None = None) -> None:
    import ssl
    import urllib.request

    keys = [key] if key else list(PACKS)
    ctx = ssl.create_default_context()
    https = urllib.request.HTTPSHandler(context=ctx)

    class NR(urllib.request.HTTPRedirectHandler):
        def redirect_request(self, req, fp, code, msg, headers, newurl):
            return None

    def fetch(url, follow=True):
        req = urllib.request.Request(
            url,
            headers={"User-Agent": "allchinabuy-cms/1.0", "Cache-Control": "no-cache"},
        )
        opener = urllib.request.build_opener(*([https] if follow else [https, NR()]))
        try:
            with opener.open(req, timeout=25) as resp:
                return resp.status, resp.geturl(), resp.headers.get("Location") or "", resp.read()
        except urllib.error.HTTPError as e:
            return e.code, url, e.headers.get("Location") or "", e.read() if e.fp else b""

    fail = 0
    acbuy = (ACBUY_CA, ACBUY_NL, "acbuy.com/estimation", "www.acbuy.com/help")
    for k in keys:
        p = PACKS[k]
        host = p["host"]
        desk = desk_for(k)
        checks = [
            (f"https://{host}/", "home", True),
            (f"https://{host}/start/", "start", True),
            (f"https://{host}{p['help']}", "help", True),
            (f"https://{host}{p['news']}", "news", False),
            (f"https://{host}{p['about']}", "about", False),
            (f"https://{host}{p['catalog']}", "catalog", False),
            (f"https://{host}{p['guide']}", "ranked", False),
            (f"https://{host}{p['ship']}", "ranked", False),
        ]
        for url, kind, need_fp in checks:
            follow = kind in ("home", "start", "ranked")
            code, final, loc, body = fetch(url, follow=follow)
            html = body.decode("utf-8", "replace")
            print(k, kind, code, "bytes", len(body), "loc", loc or final)
            if any(a in (final or "") or a in (loc or "") for a in (ACBUY_CA, ACBUY_NL)):
                print(" FAIL 301 into ACBuy"); fail += 1
            if kind != "ranked" and code != 200:
                print(" FAIL status"); fail += 1
            if kind == "ranked" and code != 200:
                print(" FAIL ranked"); fail += 1
            if "allchinabuy-logo.png" not in html:
                print(" FAIL logo"); fail += 1
            if f'lang="{p["lang"]}"' not in html:
                print(" FAIL lang"); fail += 1
            if 'href="/start/"' not in html or 'href="/">Start' in html:
                print(" FAIL Start href"); fail += 1
            if need_fp and p["fingerprint"] not in html:
                print(" FAIL fingerprint"); fail += 1
            if kind in ("home", "start", "help", "news", "about", "catalog") and "www.acbuy.com" in html:
                print(" FAIL acbuy.com leak"); fail += 1
            if kind in ("home", "start"):
                if page_title(desk, p["home_topic"]) not in html:
                    print(" FAIL title"); fail += 1
                if p["dest_zh"] not in html:
                    print(" FAIL dest zh"); fail += 1
                if "cat-30-shoes.png" not in html:
                    print(" FAIL cats"); fail += 1
                if html.count('class="sg-faq"') >= 8:
                    print(" FAIL faq dump"); fail += 1
                if 'class="tl"' not in html:
                    print(" FAIL status timeline"); fail += 1
            if kind == "catalog" and html.count('class="cat"') < 30:
                print(" FAIL catalog wall"); fail += 1
            if kind == "news" and "ItemList" not in html:
                print(" FAIL news ItemList"); fail += 1
            if kind == "about":
                mark = (
                    "Een onafhankelijke site over AllChinaBuy"
                    if k == "nl"
                    else "An independent site about AllChinaBuy"
                )
                if mark not in html:
                    print(" FAIL about copy"); fail += 1
                if (loc or "").rstrip("/") == f"https://{host}":
                    print(" FAIL about 301 home"); fail += 1
            if kind == "help" and "FAQPage" not in html:
                print(" FAIL help FAQPage"); fail += 1
        code, _, _, nf = fetch(f"https://{host}/this-page-does-not-exist-cms/", follow=True)
        nhtml = nf.decode("utf-8", "replace")
        print(k, "404", code)
        if code != 404:
            print(" FAIL 404"); fail += 1
        if f"{p['not_found_tab']} | AllChinaBuy Spreadsheet" not in nhtml:
            print(" FAIL 404 title"); fail += 1
    # ACBuy dests stay independent; hub not collapsed.
    for url, lab in (
        (f"https://{ACBUY_CA}/", "acbuy ca"),
        (f"https://{ACBUY_NL}/", "acbuy nl"),
        (f"https://{HUB}/", "hub"),
    ):
        code, final, loc, _ = fetch(url, follow=False)
        print(lab, code, final or loc)
        if code != 200:
            print(" FAIL", lab); fail += 1
        if any(PACKS[k]["host"] in (loc or "") for k in PACKS):
            print(" FAIL collapsed into AllChinaBuy dest"); fail += 1
    if fail:
        raise SystemExit(f"live_check fail {fail}")
    print("live_check ok")


def _cf_bust(hosts: list[str]) -> None:
    import json
    import urllib.error
    import urllib.request

    token = os.environ.get("CLOUDFLARE_API_TOKEN", "").strip()
    if not token:
        print("skip CF purge: no token")
        return
    api = "https://api.cloudflare.com/client/v4"

    def req(method: str, path: str, body: dict | None = None) -> dict:
        data = json.dumps(body).encode() if body is not None else None
        r = urllib.request.Request(
            f"{api}{path}",
            data=data,
            method=method,
            headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
        )
        try:
            with urllib.request.urlopen(r, timeout=30) as resp:
                return json.loads(resp.read().decode())
        except urllib.error.HTTPError as e:
            raw = e.read().decode(errors="replace")
            try:
                return json.loads(raw)
            except json.JSONDecodeError:
                return {"success": False, "errors": [{"message": raw[:300]}]}

    for host in hosts:
        z = req("GET", f"/zones?name={host}")
        zid = ((z.get("result") or [{}])[0] or {}).get("id")
        if not zid:
            print("CF zone missing", host, z.get("errors"))
            continue
        d = req("PATCH", f"/zones/{zid}/settings/development_mode", {"value": "on"})
        print("CF development_mode", host, d.get("success"), (d.get("errors") or d.get("result") or ""))
        p = req("POST", f"/zones/{zid}/purge_cache", {"purge_everything": True})
        print("CF purge", host, p.get("success"), p.get("errors") or "")


if __name__ == "__main__":
    args = sys.argv[1:]
    cmd = args[0] if args else "generate"
    rest = args[1:] or list(PACKS)
    if cmd == "put":
        for k in rest:
            put(k)
        _cf_bust([PACKS[k]["host"] for k in rest])
    elif cmd == "live":
        live_check(rest[0] if len(rest) == 1 else None)
    elif cmd == "all":
        for k in rest:
            put(k)
        _cf_bust([PACKS[k]["host"] for k in rest])
        live_check()
    else:
        for k in rest:
            generate(k)
