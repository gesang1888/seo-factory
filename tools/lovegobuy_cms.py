#!/usr/bin/env python3
"""LoveGoBuy country dests: CA, NL, IT, ES.

Gold IA: hipobuy.es. Gold brand: lovegobuy.com (official red #e91e12 / #c8160c).
Same-agent country hosts stay independent (no 301 between them).
Same-country twins lovegobuyspreadsheet.it / .nl 301 into lovegobuy.it / lovegobuy.nl
only after the target dest is live; their wwwroot is never PUT as a dest.
Hubs lovegobuyspreadsheet.eu and lovegobuyguide.com (and lovegobuy.cheap) are not
overwritten: they keep their own PHP/CMS and say "not a customs territory".

Official estimator is https://www.lovegobuy.com/shipping/estimation/index.
Warehouse: public copies disagree (60 vs 90 free warehouse days); the desks name
both and pick neither. Confirm live Help the morning you ship.
Invite W5RJX3 stays off titles and dest homepages.

Usage:
    python3 tools/lovegobuy_cms.py generate [ca nl it es]
    python3 tools/lovegobuy_cms.py put [ca nl it es]     # dests first, then twins
    python3 tools/lovegobuy_cms.py twins                 # twins only (target must be live)
    python3 tools/lovegobuy_cms.py live [ca|nl|it|es]
    python3 tools/lovegobuy_cms.py all
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
    build_404,
    cats_for,
    fig as cms_fig,
    page_title,
    render_css,
    shell as cms_shell,
    w2c_sheet,
    wrap_inner as cms_wrap_inner,
)
from desk_template import dest_local_pack, faq_ld, itemlist_ld, long_faqs, validate_desk

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "sites"
ASSETS = Path("/tmp/lovegobuy-assets")
DATE = "6 Oct 2026"
AGENT = "LoveGoBuy"
OFFICIAL = "https://www.lovegobuy.com/"
EST_PATH = "/shipping/estimation/index"
EST = "https://www.lovegobuy.com/shipping/estimation/index"
HELP = "https://www.lovegobuy.com/"
ACC = "#e91e12"
ACC_DARK = "#c8160c"
SOFT = "#fff0ee"
LOGIN_FG = "#fff"
MAIL = "cnfd85269032661@gmail.com"
HUB = "lovegobuyspreadsheet.eu"
GUIDE_HUB = "lovegobuyguide.com"
HUBS = (HUB, GUIDE_HUB)
SKIP_PUT_HOSTS = {HUB, GUIDE_HUB, "lovegobuy.cheap"}
DEST_MIN = 22000
CSS_V = "20261006g"
INVITES = ("W5RJX3",)
LOGO = "lovegobuy-logo.png"
THEME_CSS = "lovegobuy-theme.css"
SHEET_SLUG = "lovegobuy"
SHOTS = ("oficial.jpg", "oficial-diy.jpg", "catalogus.jpg", "catalogus-zoek.jpg", "volume-voorbeeld.jpg")
GUIDE_HREF = "/how-to-use-lovegobuy/"
SHIP_HREF = "/lovegobuy-shipping/"

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

NL_LABELS = {
    **EN_LABELS,
    "SNEAKERS": "Sneakers",
    "T-SHIRT": "T-shirt",
    "SHIRT": "Overhemd",
    "VEST": "Bodywarmer",
    "LONG SLEEVED": "Lange mouw",
    "SWEATER": "Trui",
    "SHAWL": "Omslagdoek",
    "JACKET": "Jas",
    "SHELL JACKET": "Shelljas",
    "FLEECE JACKET": "Fleecejas",
    "DOWN JACKETS": "Donsjas",
    "TROUSERS": "Broek",
    "FEMALE STYLE": "Dames",
    "Electronics": "Elektronica",
    "GLOVES": "Handschoenen",
    "BAG": "Tas",
    "HAT": "Pet",
    "JEWELRY": "Sieraden",
    "UNDERWEAR": "Ondergoed",
    "BELT": "Riem",
    "KNEEPAD": "Kniebeschermer",
    "SOCKS": "Sokken",
    "HEADGEAR": "Hoofddeksel",
    "EARMUFF": "Oorwarmers",
    "SCARF": "Sjaal",
    "GLASSES": "Bril",
    "WATCH": "Horloge",
    "CHILD": "Kinderen",
}

IT_LABELS = {
    **EN_LABELS,
    "SNEAKERS": "Sneakers",
    "T-SHIRT": "T-shirt",
    "SHIRT": "Camicia",
    "SHORTS": "Shorts",
    "VEST": "Gilet",
    "LONG SLEEVED": "Manica lunga",
    "SWEATER": "Maglione",
    "SHAWL": "Scialle",
    "JACKET": "Giacca",
    "SHELL JACKET": "Giacca shell",
    "FLEECE JACKET": "Pile",
    "DOWN JACKETS": "Piumino",
    "TROUSERS": "Pantaloni",
    "FEMALE STYLE": "Donna",
    "Electronics": "Elettronica",
    "GLOVES": "Guanti",
    "BAG": "Borsa",
    "HAT": "Cappello",
    "JEWELRY": "Gioielli",
    "UNDERWEAR": "Intimo",
    "BELT": "Cintura",
    "KNEEPAD": "Ginocchiere",
    "SOCKS": "Calze",
    "HEADGEAR": "Copricapo",
    "EARMUFF": "Paraorecchie",
    "SCARF": "Sciarpa",
    "GLASSES": "Occhiali",
    "WATCH": "Orologio",
    "CHILD": "Bambini",
}

ES_LABELS = {
    **EN_LABELS,
    "SNEAKERS": "Zapatillas",
    "T-SHIRT": "Camiseta",
    "SHIRT": "Camisa",
    "VEST": "Chaleco",
    "LONG SLEEVED": "Manga larga",
    "SWEATER": "Jersey",
    "SHAWL": "Chal",
    "JACKET": "Chaqueta",
    "SHELL JACKET": "Chaqueta shell",
    "FLEECE JACKET": "Forro polar",
    "DOWN JACKETS": "Plumífero",
    "TROUSERS": "Pantalón",
    "FEMALE STYLE": "Mujer",
    "Electronics": "Electrónica",
    "GLOVES": "Guantes",
    "BAG": "Bolso",
    "HAT": "Gorra",
    "JEWELRY": "Joyería",
    "UNDERWEAR": "Ropa interior",
    "BELT": "Cinturón",
    "KNEEPAD": "Rodillera",
    "SOCKS": "Calcetines",
    "HEADGEAR": "Sombrero",
    "EARMUFF": "Orejeras",
    "SCARF": "Bufanda",
    "GLASSES": "Gafas",
    "WATCH": "Reloj",
    "CHILD": "Niños",
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
    "BELT": "Flat and light. Easy to add without changing the weight band.",
    "KNEEPAD": "Pair them in the QC photo. One pad on the catalogue shot is not a pair.",
    "SOCKS": "Light filler. Check the pair and the size print on the photo.",
    "HEADGEAR": "Ask how it is packed. Brims fold in a tight box.",
    "EARMUFF": "Light, but the headband needs space. Do not crush it under a hoodie.",
    "SCARF": "Ask for flat packing or it arrives as a ball of volume.",
    "GLASSES": "Ask for a rigid case in the warehouse photo before you book the line.",
    "WATCH": "Small and cheap to send. Confirm the clasp on the QC photo.",
    "CHILD": "Asian kids’ sizes run smaller. Measure, do not guess from the age on the label.",
}

CAT_NOTES_IT = {
    "SNEAKERS": "Suola e forma sulle foto QC prima di prenotare l’internazionale.",
    "SLIPPERS": "Leggere e piatte. Riempiono la scatola senza alzare troppo il peso fatturato.",
    "T-SHIRT": "I tagli asiatici sono spesso più stretti. Misura il petto in centimetri, non solo la lettera.",
    "POLO": "Colletto e piqué sulla foto QC. Sono i due dettagli che divergono di più.",
    "SHIRT": "Lunghezza manica e spalla sulla foto con metro, non sulla lettera.",
    "SHORTS": "Leggeri e piatti: il modo più semplice per riempire un pacco.",
    "VEST": "I gilet sono più spessi di quanto pesino. Conta il volume prima di una giacca.",
    "LONG SLEEVED": "Lunghezza manica e polsino sulla foto QC. Le lunghezze asiatiche corrono più corte.",
    "HOODIE": "Pesante per il volume. Una felpa può fissare la fascia di peso di tutta la scatola.",
    "SWEATER": "GSM e restringimento. Misura il petto, non solo l’etichetta.",
    "SHAWL": "Leggero, ma ingombrante se non è piegato piatto.",
    "JACKET": "Il piumino occupa enormemente. Il volume batte quasi sempre la bilancia.",
    "SHELL JACKET": "Cuciture e zip da vicino sulla foto QC.",
    "FLEECE JACKET": "Leggero in bilancia, spesso in volume. Stesso ricalcolo del piumino.",
    "DOWN JACKETS": "Vince il volume. Un piumino da solo può forzare una classe più cara.",
    "TROUSERS": "Foto di cavallo e interno gamba. La W/L non sempre coincide coi centimetri.",
    "Jersey": "Numero, patch e stagione sulle foto.",
    "FEMALE STYLE": "La vestibilità è di rado unisex. Misura busto e lunghezza.",
    "Electronics": "Spesso litio. Molte linee aeree rifiutano: controlla il sito ufficiale prima.",
    "GLOVES": "La coppia sulla foto QC. Un guanto sullo scatto del catalogo non dice il secondo.",
    "BAG": "Riempie quasi da sola una scatola. Conta il volume prima di aggiungere vestiti.",
    "HAT": "Si schiaccia e ingombra. Chiedi imbottitura, o la tesa arriva piegata.",
    "JEWELRY": "Piccoli e economici da spedire. Buoni per chiudere una scatola quasi piena.",
    "UNDERWEAR": "Meno schede. Se non trovi nulla, cerca per marca, non per la parola.",
    "BELT": "Piatta e leggera. Quasi non cambia la fascia di peso.",
    "KNEEPAD": "In coppia sulla foto QC. Una ginocchiera sullo scatto non è un paio.",
    "SOCKS": "Riempitivo leggero. Controlla il paio e la taglia stampata.",
    "HEADGEAR": "Chiedi come viene imballato. Le tese si piegano in una scatola stretta.",
    "EARMUFF": "Leggeri, ma l’archetto vuole spazio. Non schiacciarli sotto una felpa.",
    "SCARF": "Chiedi piegatura piatta, o arriva come una palla di volume.",
    "GLASSES": "Astuccio rigido sulla foto di magazzino prima di prenotare la linea.",
    "WATCH": "Piccolo e economico da spedire. Conferma la chiusura sulla foto QC.",
    "CHILD": "Le taglie kids asiatiche corrono più piccole. Misura, non indovinare dall’età.",
}

CAT_NOTES_ES = {k: v for k, v in CAT_NOTES_EN.items()}
CAT_NOTES_ES.update({
    "SNEAKERS": "Suela y horma en las fotos QC antes de reservar el internacional.",
    "T-SHIRT": "Los cortes asiáticos suelen ser más estrechos. Mide el pecho en centímetros.",
    "HOODIE": "Pesada para su volumen. Una sudadera puede fijar la franja de peso de toda la caja.",
    "Electronics": "A menudo litio. Muchas líneas aéreas las rechazan: mira el sitio oficial antes.",
    "BAG": "Llena una caja casi sola. Cuenta el volumen antes de añadir ropa.",
})
CAT_NOTES_NL = {k: v for k, v in CAT_NOTES_EN.items()}
CAT_NOTES_NL.update({
    "SNEAKERS": "Zool en leest op de QC-foto’s voor je internationaal boekt.",
    "T-SHIRT": "Aziatische snits lopen vaak smaller. Meet de borst in centimeters.",
    "HOODIE": "Zwaar voor het volume. Eén hoodie kan de gewichtsklasse van de hele doos zetten.",
    "Electronics": "Vaak lithium. Veel luchtlijnen weigeren: check de officiële site eerst.",
    "BAG": "Vult bijna in z’n eentje een doos. Tel het volume voor je kleding toevoegt.",
})

# Ranked inners per dest: wrapped in dest chrome, never regenerated. Paths that are
# also a CMS slug (guide/ship/help/…) are generated instead — see _wrap_targets().
RANKED = {
    "ca": (
        ("/lovegobuy-spreadsheet/", 8000),
        ("/is-lovegobuy-legit/", 8000),
        ("/how-to-use-lovegobuy/", 4000),
        ("/lovegobuy-coupon/", 8000),
    ),
    "nl": (
        ("/lovegobuy-ervaringen/", 8000),
        ("/lovegobuy-coupon/", 8000),
        ("/lovegobuy-spreadsheet/", 8000),
        ("/lovegobuy-verzending/", 8000),
    ),
    "it": (
        ("/lovegobuy-recensioni/", 8000),
        ("/spedizione-lovegobuy/", 8000),
        ("/lovegobuy-spreadsheet/", 8000),
        ("/is-lovegobuy-legit/", 8000),
    ),
    "es": (
        ("/lovegobuy-opiniones/", 8000),
        ("/es-lovegobuy-confiable/", 8000),
        ("/envio-lovegobuy-espana/", 8000),
        ("/lovegobuy-spreadsheet/", 8000),
    ),
}

# Copied from tools/lovegobuy_desks.py DESTS[*]["keep"].
KEEP = {
    "es": [
        ("/lovegobuy-opiniones/", "Opiniones"),
        ("/es-lovegobuy-confiable/", "¿Es fiable?"),
        ("/envio-lovegobuy-espana/", "Envío a España"),
        ("/lovegobuy-spreadsheet/", "Spreadsheet"),
    ],
    "it": [
        ("/lovegobuy-recensioni/", "Recensioni"),
        ("/spedizione-lovegobuy/", "Spedizione"),
        ("/lovegobuy-spreadsheet/", "Spreadsheet"),
        ("/is-lovegobuy-legit/", "È affidabile?"),
    ],
    "nl": [
        ("/lovegobuy-shipping/", "Verzending NL"),
        ("/lovegobuy-ervaringen/", "Ervaringen"),
        ("/lovegobuy-coupon/", "Coupons"),
        ("/lovegobuy-spreadsheet/", "Spreadsheet"),
    ],
    "ca": [
        ("/lovegobuy-spreadsheet/", "Canada spreadsheet"),
        ("/is-lovegobuy-legit/", "Is it legit?"),
        ("/lovegobuy-shipping/", "Shipping CA"),
        ("/how-to-use-lovegobuy/", "How to use"),
    ],
}

TWINS = {
    "lovegobuyspreadsheet.it": "lovegobuy.it",
    "lovegobuyspreadsheet.nl": "lovegobuy.nl",
}

# Copied from tools/lovegobuy_desks.py.
TWIN_EXTRA = {
    "lovegobuyspreadsheet.it": [
        ("/lovegobuy-shipping", "/spedizione-lovegobuy/"),
        ("/is-lovegobuy-safe", "/is-lovegobuy-legit/"),
        ("/best-lovegobuy-spreadsheet", "/lovegobuy-spreadsheet/"),
        ("/lovegobuy-review", "/lovegobuy-recensioni/"),
        ("/lovegobuy-spreadsheets", "/lovegobuy-spreadsheet/"),
        ("/lovegobuy-coupons", "/lovegobuy-coupon/"),
        ("/lovegobuy-qc", "/lovegobuy-recensioni/"),
        ("/lovegobuy-finds", "/lovegobuy-spreadsheet/"),
        ("/lovegobuy-discord", "/how-to-use-lovegobuy/"),
    ],
    "lovegobuyspreadsheet.nl": [
        ("/lovegobuy-coupons", "/lovegobuy-coupon/"),
        ("/lovegobuy-verzending", "/lovegobuy-verzending/"),
        ("/best-lovegobuy-spreadsheet", "/lovegobuy-spreadsheet/"),
        ("/lovegobuy-spreadsheet", "/lovegobuy-spreadsheet/"),
        ("/lovegobuy-ervaringen", "/lovegobuy-ervaringen/"),
        ("/how-to-use-lovegobuy", "/how-to-use-lovegobuy/"),
        ("/is-lovegobuy-legit", "/is-lovegobuy-legit/"),
        ("/lovegobuy-shipping", "/lovegobuy-shipping/"),
        ("/lovegobuy-coupon", "/lovegobuy-coupon/"),
        ("/lovegobuy-finds", "/lovegobuy-spreadsheet/"),
        ("/lovegobuy-qc", "/lovegobuy-ervaringen/"),
        ("/lovegobuy-discord", "/how-to-use-lovegobuy/"),
    ],
}

# Deep twin URLs that must land on the same path on the target (not the target home).
TWIN_DEEP_PROBES = {
    "lovegobuyspreadsheet.nl": ("/lovegobuy-ervaringen/", "/lovegobuy-coupons", "/lovegobuy-qc"),
    "lovegobuyspreadsheet.it": ("/lovegobuy-recensioni/", "/lovegobuy-review", "/lovegobuy-coupons"),
}

CMS_PAGE_LOCS = (
    "about", "about/", "who-we-are", "who-we-are/", "help", "help/", "news", "news/", "catalog", "catalog/",
    "start", "start/",
    "hulp", "hulp/", "catalogus", "catalogus/", "nieuws", "nieuws/", "over-ons", "over-ons/",
    "aiuto", "aiuto/", "catalogo", "catalogo/", "novita", "novita/", "chi-siamo", "chi-siamo/",
    "ayuda", "ayuda/", "novedades", "novedades/", "sobre-nosotros", "sobre-nosotros/",
)

WRAP_SKIP_PREFIXES = (
    "help/", "news/", "about/", "who-we-are/", "catalog/", "start/",
    "hulp/", "catalogus/", "nieuws/", "over-ons/",
    "aiuto/", "catalogo/", "novita/", "chi-siamo/",
    "ayuda/", "novedades/", "sobre-nosotros/",
    "api/", "assets/", "img/",
    "how-to-use-lovegobuy/", "lovegobuy-shipping/",
    "faq/", "guide/",
)
WRAP_POISON = ("orientdig", "orient dig", "1yi9", "cssb.uy", "1qodrw", "bbd5off", "cruisezhang")

EXTRA_CSS = """
:root{--primary-soft:#fff0ee;--login-fg:#fff}
.hero .eyebrow{color:#ffc9c5}
header.top .hdr-login,.hdr-login{background:#e91e12;color:#fff}
header.top .hdr-login:hover,.hdr-login:hover{background:#c8160c;color:#fff}
.sbox button{color:#fff}
"""

STORAGE = {
    "en": (
        "Public LoveGoBuy copies disagree: some say 60 free warehouse days, others 90. "
        f"This desk does not pick a number: confirm live Help the morning you ship ({DATE})."
    ),
    "nl": (
        "Publieke LoveGoBuy-teksten verschillen: de ene noemt 60 gratis magazijndagen, de andere 90. "
        f"Deze gids kiest geen getal: check de live Help op de ochtend dat je verzendt ({DATE})."
    ),
    "it": (
        "Le copie pubbliche di LoveGoBuy non coincidono: alcune dicono 60 giorni gratuiti di magazzino, altre 90. "
        f"Questa guida non sceglie un numero: controlla l’Help ufficiale dal vivo la mattina della spedizione ({DATE})."
    ),
    "es": (
        "Las copias públicas de LoveGoBuy no coinciden: unas dicen 60 días gratis de almacén, otras 90. "
        f"Esta guía no elige una cifra: confirma la Ayuda en vivo la mañana del envío ({DATE})."
    ),
}


def _storage(loc: str) -> str:
    return STORAGE.get(loc, STORAGE["en"])


PACKS = {
    "ca": {
        "host": "lovegobuyspreadsheet.ca",
        "dest": "CA",
        "dest_label": "Canada",
        "dest_zh": "Canada — 加拿大",
        "lang": "en-CA",
        "loc": "en",
        "in_language": "in English",
        "ccy": "CAD",
        "home_topic": "buy in China from Canada, safely",
        "hero_h1": "LoveGoBuy Spreadsheet: the guide to buying in China from Canada",
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
        "guide": GUIDE_HREF,
        "ship": SHIP_HREF,
        "nav": [
            ("/start/", "Start"),
            (GUIDE_HREF, "Guide"),
            ("/catalog/", "Catalog"),
            (SHIP_HREF, "Shipping"),
            ("/help/", "Help"),
            ("/news/", "News"),
        ],
        "footer_sections": [
            (GUIDE_HREF, "LoveGoBuy guide"),
            ("/catalog/", "The spreadsheet and the categories"),
            (SHIP_HREF, "Shipping and customs"),
            ("/help/", "Help and questions"),
            ("/news/", "News"),
            ("/about/", "About us"),
        ],
        "aliens": ("Packstation", "Poste Italiane", "Nederlandse postcode", "no copiamos un recuento de líneas"),
        "not_found_tab": "Page not found",
        "login": "Log in to LoveGoBuy",
        "menu": "Open menu",
        "home_cta": "Back to the homepage",
        "skip": "en",
        "desk_css": "lovegobuy-ca-desk.css",
        "css_id": "lovegobuy-ca",
    },
    "nl": {
        "host": "lovegobuy.nl",
        "dest": "NL",
        "dest_label": "Nederland",
        "dest_zh": "Netherlands — 荷兰",
        "lang": "nl-NL",
        "loc": "nl",
        "in_language": "in het Nederlands",
        "ccy": "EUR",
        "home_topic": "kopen in China vanaf Nederland, veilig",
        "hero_h1": "LoveGoBuy Spreadsheet: de gids om in China te kopen vanuit Nederland",
        "eyebrow": "Onafhankelijke gids, in het Nederlands",
        "lead": "Hoe je een productlink in de agent plakt, hoe de w2clinks-catalogus werkt, hoe een pakket naar Nederland reist en wat je checkt voor de Douane.",
        "fingerprint": dest_local_pack("NL")["fingerprint"],
        "customs": "Douane",
        "customs_url": "https://www.belastingdienst.nl/wps/wcm/connect/nl/douane/",
        "postal": "Nederlandse postcode (vorm 1234 AB), geen Duits afhaalautomaat-nummer",
        "catalog": "/catalogus/",
        "help": "/hulp/",
        "news": "/nieuws/",
        "about": "/over-ons/",
        "guide": GUIDE_HREF,
        "ship": SHIP_HREF,
        "nav": [
            ("/start/", "Start"),
            (GUIDE_HREF, "Gids"),
            ("/catalogus/", "Catalogus"),
            (SHIP_HREF, "Verzending"),
            ("/hulp/", "Hulp"),
            ("/nieuws/", "Nieuws"),
        ],
        "footer_sections": [
            (GUIDE_HREF, "LoveGoBuy-gids"),
            ("/catalogus/", "Spreadsheet en categorieën"),
            (SHIP_HREF, "Verzending en douane"),
            ("/hulp/", "Hulp en vragen"),
            ("/nieuws/", "Nieuws"),
            ("/over-ons/", "Over ons"),
        ],
        "aliens": ("Packstation", "form A1A 1A1", "Poste Italiane", "no copiamos un recuento de líneas"),
        "not_found_tab": "Pagina niet gevonden",
        "login": "Inloggen bij LoveGoBuy",
        "menu": "Menu openen",
        "home_cta": "Terug naar de homepage",
        "skip": "nl",
        "desk_css": "lovegobuy-nl-desk.css",
        "css_id": "lovegobuy-nl",
    },
    "it": {
        "host": "lovegobuy.it",
        "dest": "IT",
        "dest_label": "Italia",
        "dest_zh": "Italy — 意大利",
        "lang": "it-IT",
        "loc": "it",
        "in_language": "in italiano",
        "ccy": "EUR",
        "home_topic": "comprare in Cina dall’Italia, in sicurezza",
        "hero_h1": "LoveGoBuy Spreadsheet: la guida per comprare in Cina dall’Italia",
        "eyebrow": "Guida indipendente, in italiano",
        "lead": "Come incolli un link prodotto nell’agente, come funziona il catalogo w2clinks, come un pacco arriva in Italia e cosa controlli prima della dogana.",
        "fingerprint": dest_local_pack("IT")["fingerprint"],
        "customs": "ADM",
        "customs_url": "https://www.adm.gov.it/portale/",
        "postal": "via italiana e CAP a cinque cifre. Poste Italiane può aggiungere un fee",
        "catalog": "/catalogo/",
        "help": "/aiuto/",
        "news": "/novita/",
        "about": "/chi-siamo/",
        "guide": GUIDE_HREF,
        "ship": SHIP_HREF,
        "nav": [
            ("/start/", "Start"),
            (GUIDE_HREF, "Guida"),
            ("/catalogo/", "Catalogo"),
            (SHIP_HREF, "Spedizione"),
            ("/aiuto/", "Aiuto"),
            ("/novita/", "Novità"),
        ],
        "footer_sections": [
            (GUIDE_HREF, "Guida LoveGoBuy"),
            ("/catalogo/", "Spreadsheet e categorie"),
            (SHIP_HREF, "Spedizione e dogana"),
            ("/aiuto/", "Aiuto e domande"),
            ("/novita/", "Novità"),
            ("/chi-siamo/", "Chi siamo"),
        ],
        "aliens": ("Packstation", "form A1A 1A1", "Nederlandse postcode", "no copiamos un recuento de líneas"),
        "not_found_tab": "Pagina non trovata",
        "login": "Accedi a LoveGoBuy",
        "menu": "Apri menu",
        "home_cta": "Torna alla homepage",
        "skip": "it",
        "desk_css": "lovegobuy-it-desk.css",
        "css_id": "lovegobuy-it",
    },
    "es": {
        "host": "lovegobuyspreadsheet.es",
        "dest": "ES",
        "dest_label": "España",
        "dest_zh": "Spain — 西班牙",
        "lang": "es-ES",
        "loc": "es",
        "in_language": "en español",
        "ccy": "EUR",
        "home_topic": "comprar en China desde España, con seguridad",
        "hero_h1": "LoveGoBuy Spreadsheet: la guía para comprar en China desde España",
        "eyebrow": "Guía independiente, en español",
        "lead": "Cómo pegas un enlace de producto en el agente, cómo funciona el catálogo de w2clinks, cómo viaja un paquete a España y qué miras antes de aduanas.",
        "fingerprint": dest_local_pack("ES")["fingerprint"],
        "customs": "Agencia Tributaria",
        "customs_url": "https://sede.agenciatributaria.gob.es/",
        "postal": "calle española y código postal de cinco dígitos. no copiamos un recuento de líneas",
        "catalog": "/catalogo/",
        "help": "/ayuda/",
        "news": "/novedades/",
        "about": "/sobre-nosotros/",
        "guide": GUIDE_HREF,
        "ship": SHIP_HREF,
        "nav": [
            ("/start/", "Start"),
            (GUIDE_HREF, "Guía"),
            ("/catalogo/", "Catálogo"),
            (SHIP_HREF, "Envío"),
            ("/ayuda/", "Ayuda"),
            ("/novedades/", "Novedades"),
        ],
        "footer_sections": [
            (GUIDE_HREF, "Guía LoveGoBuy"),
            ("/catalogo/", "Spreadsheet y categorías"),
            (SHIP_HREF, "Envío y aduanas"),
            ("/ayuda/", "Ayuda y preguntas"),
            ("/novedades/", "Novedades"),
            ("/sobre-nosotros/", "Sobre nosotros"),
        ],
        "aliens": ("Packstation", "form A1A 1A1", "Poste Italiane", "Nederlandse postcode"),
        "not_found_tab": "Página no encontrada",
        "login": "Entrar en LoveGoBuy",
        "menu": "Abrir menú",
        "home_cta": "Volver al inicio",
        "skip": "es",
        "desk_css": "lovegobuy-es-desk.css",
        "css_id": "lovegobuy-es",
    },
}


def _off(host: str, path: str = "") -> str:
    url = OFFICIAL.rstrip("/") + path
    sep = "&" if "?" in url else "?"
    return f"{url}{sep}utm_source={host}&utm_medium=referral&utm_campaign=portada"


def desk_for(key: str) -> CountryDesk:
    p = PACKS[key]
    inner = f'data-inner-chrome="{CSS_V}-{p["css_id"]}"'
    loc = p["loc"]
    if loc == "nl":
        intro = (
            "Onafhankelijke Nederlandstalige gids over LoveGoBuy en hoe je de w2clinks-catalogus "
            f"gebruikt om vanuit {p['dest_label']} in China te kopen."
        )
        independence = (
            "LoveGoBuy Spreadsheet is een onafhankelijke infosite. Wij zijn LoveGoBuy niet, "
            "we verwerken geen bestellingen, we innen geen porto en we zien je account niet. "
            "Elke bestelling, betaling en klacht loopt via de officiële site."
        )
        copyright = "&copy; 2026 LoveGoBuy Spreadsheet. Nederlandse tekst, nagelezen voor publicatie."
        sections_h, official_h, independence_h, nav_aria = (
            "Onderdelen", "Officiële links", "Onafhankelijkheidsnotitie.", "Hoofdmenu",
        )
        nf_h1, nf_lead = "Deze pagina bestaat niet", "De link is misschien oud. Dit zijn de onderdelen die wel bestaan:"
        official_links = [
            (_off(p["host"]), "LoveGoBuy (officiële site)"),
            (_off(p["host"], EST_PATH), f"Officiële schatter ({DATE})"),
        ]
    elif loc == "it":
        intro = (
            "Guida indipendente in italiano su LoveGoBuy e su come usi il catalogo w2clinks "
            "per comprare in Cina dall’Italia."
        )
        independence = (
            "LoveGoBuy Spreadsheet è un sito informativo indipendente. Non siamo LoveGoBuy, "
            "non elaboriamo ordini, non incassiamo il trasporto e non vediamo il tuo account. "
            "Ogni ordine, pagamento e reclamo passa dal sito ufficiale."
        )
        copyright = "&copy; 2026 LoveGoBuy Spreadsheet. Testo italiano, riletto prima della pubblicazione."
        sections_h, official_h, independence_h, nav_aria = (
            "Sezioni", "Link ufficiali", "Nota di indipendenza.", "Menu principale",
        )
        nf_h1, nf_lead = "Questa pagina non esiste", "Il link forse è vecchio. Queste sezioni invece ci sono:"
        official_links = [
            (_off(p["host"]), "LoveGoBuy (sito ufficiale)"),
            (_off(p["host"], EST_PATH), f"Estimator ufficiale ({DATE})"),
        ]
    elif loc == "es":
        intro = (
            "Guía independiente en español sobre LoveGoBuy y sobre cómo usas el catálogo "
            f"w2clinks para comprar en China desde {p['dest_label']}."
        )
        independence = (
            "LoveGoBuy Spreadsheet es un sitio informativo independiente. No somos LoveGoBuy, "
            "no tramitamos pedidos, no cobramos el envío y no vemos tu cuenta. "
            "Cada pedido, pago y reclamación pasa por el sitio oficial."
        )
        copyright = "&copy; 2026 LoveGoBuy Spreadsheet. Texto en español, releído antes de publicar."
        sections_h, official_h, independence_h, nav_aria = (
            "Secciones", "Enlaces oficiales", "Aviso de independencia.", "Menú principal",
        )
        nf_h1, nf_lead = "Esta página no existe", "El enlace quizá sea antiguo. Estas secciones sí existen:"
        official_links = [
            (_off(p["host"]), "LoveGoBuy (sitio oficial)"),
            (_off(p["host"], EST_PATH), f"Estimador oficial ({DATE})"),
        ]
    else:
        intro = (
            f"Independent English-language guide to LoveGoBuy and to how you use the w2clinks "
            f"catalogue to buy in China from {p['dest_label']}."
        )
        independence = (
            "LoveGoBuy Spreadsheet is an independent information site. We are not LoveGoBuy, "
            "we do not process orders, we do not collect shipping fees and we cannot see "
            "your account. Every order, payment and claim runs through the official site."
        )
        copyright = "&copy; 2026 LoveGoBuy Spreadsheet. English copy, edited and checked by people before publication."
        sections_h, official_h, independence_h, nav_aria = (
            "Sections", "Official links", "Independence notice.", "Main menu",
        )
        nf_h1, nf_lead = "This page does not exist", "The link may be old. These are the sections that do exist:"
        official_links = [
            (_off(p["host"]), "LoveGoBuy (official site)"),
            (_off(p["host"], EST_PATH), f"Official estimator ({DATE})"),
        ]
    return CountryDesk(
        host=p["host"],
        agent=AGENT,
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
        logo_src=f"/assets/images/{LOGO}",
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
        theme_css=THEME_CSS,
        desk_css=p["desk_css"],
        inner_marker=inner,
        register_path="/",
        sheet_slug=SHEET_SLUG,
        invites=INVITES,
        extra_css=EXTRA_CSS,
        soft=SOFT,
        login_fg=LOGIN_FG,
        sections_h=sections_h,
        official_h=official_h,
        independence_h=independence_h,
        nav_aria=nav_aria,
        not_found_tab=p["not_found_tab"],
    )


def _facts(key: str) -> dict:
    p = PACKS[key]
    return {
        "agent": AGENT,
        "host": p["host"],
        "lang": p["lang"],
        "loc": p["loc"],
        "dest": p["dest"],
        "dest_label": p["dest_label"],
        "ccy": p["ccy"],
        "storage": _storage(p["loc"]),
        "estimator": EST,
        "official": OFFICIAL,
        "date": DATE,
        "keep": list(KEEP.get(key) or []),
        "codes_off_title": list(INVITES),
        "strict_html_codes": True,
    }


def _faqs(key: str) -> list[tuple[str, str]]:
    p = PACKS[key]
    pairs = []
    for q, a in long_faqs(_facts(key)):
        a = a.replace("/api/products/", "w2clinks")
        a = re.sub(r"ni copia un snapshot de 58 l[ií]neas ajenas\.?", "", a, flags=re.I)
        a = re.sub(r"58 l[ií]neas(?: para Espa\w*)?", "", a, flags=re.I)
        a = re.sub(r"23[,.]81\s*USD", "", a, flags=re.I)
        pairs.append((q, a))
    extra = f"The delivery address uses a {p['postal']}."
    if p["loc"] == "it":
        extra = f"L’indirizzo di consegna è una {p['postal']}."
    elif p["loc"] == "es":
        extra = f"La dirección de entrega es una {p['postal']}."
    elif p["loc"] == "nl":
        extra = f"Het afleveradres is een {p['postal']}."
    if pairs:
        q0, a0 = pairs[0]
        if p["fingerprint"] not in a0:
            pairs[0] = (q0, a0 + " " + extra)
    blob = " ".join(a for _, a in pairs)
    if p["fingerprint"] not in blob:
        pairs.append(("Which address belongs on this dest?", extra))
    return pairs


def _faq_html(pairs: list[tuple[str, str]], *, open_first: bool = True) -> str:
    items = []
    for i, (q, a) in enumerate(pairs):
        op = " open" if open_first and i == 0 else ""
        items.append(
            f'<details class="sg-faq"{op}><summary>{escape(q)}</summary><p>{escape(a)}</p></details>'
        )
    return "\n".join(items)


def _faq_group_titles(key: str) -> list[str]:
    p = PACKS[key]
    dest = p["dest_label"]
    loc = p["loc"]
    if loc == "it":
        return [
            "Che cos’è LoveGoBuy e in quale lingua funziona",
            "Cosa paghi",
            "Importazione in Italia",
            "Magazzino, foto e cosa può viaggiare",
            "Se qualcosa non torna",
        ]
    if loc == "es":
        return [
            "Qué es LoveGoBuy y en qué idioma funciona",
            "Qué vas a pagar",
            f"Importación a {dest}",
            "Almacén, fotos y qué puede viajar",
            "Si algo no cuadra",
        ]
    if loc == "nl":
        return [
            "Wat LoveGoBuy is en in welke taal het draait",
            "Wat je gaat betalen",
            f"Invoer naar {dest}",
            "Magazijn, foto’s en wat mag reizen",
            "Als iets niet klopt",
        ]
    return [
        "What LoveGoBuy is, and which language it uses",
        "What you will pay",
        f"Import into {dest}",
        "Warehouse, photos and what may travel",
        "If something is wrong",
    ]


def _faq_grouped_html(key: str) -> str:
    pairs = _faqs(key)
    titles = _faq_group_titles(key)
    slices = ((0, 3), (3, 7), (7, 9), (9, 13), (13, None))
    bits = []
    open_first = True
    for title, (a, b) in zip(titles, slices):
        chunk = pairs[a:b]
        bits.append(f"<h2>{escape(title)}</h2>")
        bits.append(_faq_html(chunk, open_first=open_first))
        open_first = False
    return "\n".join(bits)


def _keys_table(key: str) -> str:
    loc = PACKS[key]["loc"]
    if loc == "it":
        head = ("Se pensi a", "Scrivi")
        rows = (
            ("scarpe", "sneakers"),
            ("felpa", "hoodie"),
            ("giacca", "jacket"),
            ("pantaloni", "trousers"),
            ("borsa", "bag"),
            ("occhiali", "glasses"),
            ("orologio", "watch"),
        )
    elif loc == "es":
        head = ("Si piensas en", "Escribe")
        rows = (
            ("zapatillas", "sneakers"),
            ("sudadera", "hoodie"),
            ("chaqueta", "jacket"),
            ("pantalón", "trousers"),
            ("bolso", "bag"),
            ("gafas", "glasses"),
            ("reloj", "watch"),
        )
    elif loc == "nl":
        head = ("Als je denkt aan", "Typ")
        rows = (
            ("sneakers", "sneakers"),
            ("hoodie", "hoodie"),
            ("jas", "jacket"),
            ("broek", "trousers"),
            ("tas", "bag"),
            ("bril", "glasses"),
            ("horloge", "watch"),
        )
    else:
        head = ("If you think of", "Type")
        rows = (
            ("sneakers / trainers", "sneakers"),
            ("hoodie", "hoodie"),
            ("jacket", "jacket"),
            ("trousers / pants", "trousers"),
            ("bag", "bag"),
            ("glasses", "glasses"),
            ("watch", "watch"),
        )
    body = "".join(f"<tr><td>{escape(a)}</td><td>{escape(b)}</td></tr>" for a, b in rows)
    return (
        f'<table class="eq"><thead><tr><th>{escape(head[0])}</th><th>{escape(head[1])}</th></tr></thead>'
        f"<tbody>{body}</tbody></table>"
    )


def _cats(key: str):
    loc = PACKS[key]["loc"]
    if loc == "it":
        return cats_for(IT_LABELS)
    if loc == "es":
        return cats_for(ES_LABELS)
    if loc == "nl":
        return cats_for(NL_LABELS)
    return cats_for(EN_LABELS)


def _sheet(desk: CountryDesk) -> str:
    return w2c_sheet(desk)


def _fig(src: str, alt: str, cap: str, w: int = 1200, h: int = 750) -> str:
    return cms_fig(src, alt, cap, w, h)


def _wall(key: str, notes: dict[str, str] | None = None) -> str:
    desk = desk_for(key)
    sheet = _sheet(desk)
    bits = []
    for ckey, labn, fn in _cats(key):
        em = f"<em>{escape(notes[ckey])}</em>" if notes and ckey in notes else ""
        bits.append(
            f'<a class="cat" href="{escape(sheet)}?category={quote_plus(ckey)}&amp;page=1&amp;sort=newest" '
            f'rel="noopener" target="_blank">'
            f'<img src="{escape(W2C)}/public/static/w2c/categories/{escape(fn)}" alt="{escape(ckey)}" '
            f'loading="lazy" decoding="async" width="96" height="96">'
            f'<div class="cat__b"><strong>{escape(labn)}</strong><span>{escape(ckey)}</span>{em}</div></a>'
        )
    return "".join(bits)


def _chips(key: str) -> str:
    p = PACKS[key]
    desk = desk_for(key)
    sheet = _sheet(desk)
    return "".join(
        f'<a href="{escape(sheet)}?q={quote_plus(ckey.lower())}&amp;utm_source={escape(p["host"])}&amp;utm_medium=referral&amp;utm_campaign=hero-chips" '
        f'rel="nofollow noopener" target="_blank">{escape(ckey.lower() if ckey.isupper() else ckey)}</a>'
        for ckey, _lab, _fn in _cats(key)[:8]
    )


def _shots(key: str):
    loc = PACKS[key]["loc"]
    if loc == "it":
        off_alt, off_cap = (
            "Homepage ufficiale LoveGoBuy: ricerca, menu ed estimator di spedizione",
            f"Sito ufficiale lovegobuy.com, {DATE}. L’estimator sta su {EST_PATH}. Questa guida non inventa una linea né un importo.",
        )
        sheet_alt, sheet_cap = (
            "Catalogo LoveGoBuy su w2clinks: schede con foto, marca e prezzo di riferimento",
            "Schede, non celle Excel. I prezzi in yuan cambiano ogni giorno. Scatto 6 Oct 2026, categoria SNEAKERS.",
        )
        vol_alt, vol_cap = (
            "Esempio di peso volumetrico: 40×40×3 cm e 200 g in bilancia diventano 600 g di volume",
            "Un esempio calcolato, non una foto di magazzino. Molte linee fatturano il massimo tra bilancia e volume, spesso L×W×H (cm) / 8000.",
        )
        zoek_alt, zoek_cap = (
            "Ricerca hoodie nel catalogo LoveGoBuy su w2clinks",
            "Risultati con colonna filtri. Scatto 6 Oct 2026.",
        )
        diy_alt, diy_cap = (
            "Ricerca LoveGoBuy: incollare un link Taobao, 1688 o Weidian",
            f"Barra pubblica su lovegobuy.com, {DATE}. Questa guida non inventa un ordine compilato.",
        )
    elif loc == "es":
        off_alt, off_cap = (
            "Portada oficial de LoveGoBuy: búsqueda, menú y estimador de envío",
            f"Sitio oficial lovegobuy.com, {DATE}. El estimador está en {EST_PATH}. Esta guía no inventa una línea ni un importe.",
        )
        sheet_alt, sheet_cap = (
            "Catálogo LoveGoBuy en w2clinks: fichas con foto, marca y precio de referencia",
            "Fichas, no celdas de Excel. Los precios en yuan cambian cada día. Captura 6 Oct 2026, categoría SNEAKERS.",
        )
        vol_alt, vol_cap = (
            "Ejemplo de peso volumétrico: 40×40×3 cm y 200 g en báscula son 600 g de volumen",
            "Un ejemplo calculado, no una foto de almacén. Muchas líneas facturan el máximo entre báscula y volumen, a menudo L×W×H (cm) / 8000.",
        )
        zoek_alt, zoek_cap = (
            "Búsqueda de hoodie en el catálogo LoveGoBuy de w2clinks",
            "Resultados con columna de filtros. Captura 6 Oct 2026.",
        )
        diy_alt, diy_cap = (
            "Búsqueda LoveGoBuy: pegar un enlace Taobao, 1688 o Weidian",
            f"Barra pública en lovegobuy.com, {DATE}. Esta guía no inventa un pedido relleno.",
        )
    elif loc == "nl":
        off_alt, off_cap = (
            "Officiële LoveGoBuy-homepage: zoekbalk, menu en verzendschatter",
            f"Officiële lovegobuy.com, {DATE}. De schatter staat op {EST_PATH}. Deze gids verzint geen lijn en geen bedrag.",
        )
        sheet_alt, sheet_cap = (
            "LoveGoBuy-catalogus op w2clinks: kaarten met foto, merk en referentieprijs",
            "Kaarten, geen Excel-cellen. Yuan-prijzen veranderen per dag. Opname 6 Oct 2026, categorie SNEAKERS.",
        )
        vol_alt, vol_cap = (
            "Voorbeeld volumegewicht: 40×40×3 cm en 200 g op de weegschaal wordt 600 g volume",
            "Een rekenvoorbeeld, geen magazijnfoto. Veel lijnen factureren het maximum van weegschaal en volume, vaak L×W×H (cm) / 8000.",
        )
        zoek_alt, zoek_cap = (
            "Hoodie-zoekopdracht in de LoveGoBuy-catalogus op w2clinks",
            "Resultaten met filterkolom. Opname 6 Oct 2026.",
        )
        diy_alt, diy_cap = (
            "LoveGoBuy-zoekbalk: een Taobao-, 1688- of Weidian-link plakken",
            f"Publieke plakbalk op lovegobuy.com, {DATE}. Deze gids verzint geen ingevulde bestelling.",
        )
    else:
        off_alt, off_cap = (
            "Official LoveGoBuy homepage: search bar, navigation and the shipping estimator",
            f"Official lovegobuy.com, {DATE}. The estimator lives at {EST_PATH}. This desk does not invent a line or a dollar amount.",
        )
        sheet_alt, sheet_cap = (
            "LoveGoBuy catalogue on w2clinks: product cards with photo, brand and reference price",
            "Cards, not Excel cells. Yuan prices change by the day. Capture 6 Oct 2026, category SNEAKERS.",
        )
        vol_alt, vol_cap = (
            "Worked example of volume weight: 40×40×3 cm and 200 g scale becomes 600 g volume",
            "A worked example, not a warehouse photo. Many lines bill the greater of scale and volume, often L×W×H (cm) / 8000.",
        )
        zoek_alt, zoek_cap = (
            "Hoodie search in the LoveGoBuy catalogue on w2clinks",
            "Results with the filter column. Capture 6 Oct 2026.",
        )
        diy_alt, diy_cap = (
            "LoveGoBuy search: paste a Taobao, 1688 or Weidian link",
            f"Public paste bar on lovegobuy.com, {DATE}. This desk does not invent a filled order total.",
        )
    fig_off = _fig("/img/shots/oficial.jpg", off_alt, off_cap)
    fig_sheet = _fig("/img/shots/catalogus.jpg", sheet_alt, sheet_cap, 1200, 900)
    fig_vol = _fig("/img/shots/volume-voorbeeld.jpg", vol_alt, vol_cap, 1200, 640)
    fig_zoek = _fig("/img/shots/catalogus-zoek.jpg", zoek_alt, zoek_cap, 1200, 900)
    fig_diy = _fig("/img/shots/oficial-diy.jpg", diy_alt, diy_cap, 1200, 280)
    return fig_off, fig_sheet, fig_vol, fig_zoek, fig_diy


def _sec_shots(key: str, fig) -> str:
    p = PACKS[key]
    loc, dest = p["loc"], p["dest_label"]
    if loc == "it":
        return f"""
<section class="sec" id="shots">
  <div class="wrap"><div class="split split--rev"><div>
    <h2>Incolla un link cinese, o cerca nell’app</h2>
    <p class="lead">LoveGoBuy parte così: incolli un link di Taobao, 1688 o Weidian, o digiti il nome. Il negozio cinese vede LoveGoBuy; tu poi vedi le foto di magazzino e una linea verso l’Italia.</p>
    <p>Se la ricerca non legge il link, il passo successivo è il modulo manuale: nome, taglia, colore e prezzo in yuan. L’internazionale lo paghi dopo, dal magazzino.</p>
    <p><a class="btn" href="{escape(p["guide"])}">Guida passo passo</a>
       <a class="btn btn--ghost" href="{escape(OFFICIAL)}" rel="noopener">Sito ufficiale</a></p>
  </div>{fig}</div></div>
</section>
"""
    if loc == "es":
        return f"""
<section class="sec" id="shots">
  <div class="wrap"><div class="split split--rev"><div>
    <h2>Pega un enlace chino, o busca en la app</h2>
    <p class="lead">LoveGoBuy empieza así: pegas un enlace de Taobao, 1688 o Weidian, o escribes el nombre. La tienda china ve LoveGoBuy; tú luego ves fotos de almacén y una línea hacia {escape(dest)}.</p>
    <p>Si la búsqueda no lee el enlace, el siguiente paso es el formulario manual: nombre, talla, color y precio en yuan. El internacional lo pagas después, desde el almacén.</p>
    <p><a class="btn" href="{escape(p["guide"])}">Guía paso a paso</a>
       <a class="btn btn--ghost" href="{escape(OFFICIAL)}" rel="noopener">Sitio oficial</a></p>
  </div>{fig}</div></div>
</section>
"""
    if loc == "nl":
        return f"""
<section class="sec" id="shots">
  <div class="wrap"><div class="split split--rev"><div>
    <h2>Plak een Chinese link, of zoek in de app</h2>
    <p class="lead">LoveGoBuy start zo: je plakt een Taobao-, 1688- of Weidian-link, of typt de naam. De Chinese shop ziet LoveGoBuy; jij ziet daarna magazijnfoto’s en een lijn naar {escape(dest)}.</p>
    <p>Leest de zoekbalk de link niet, is het handmatige formulier de volgende stap: naam, maat, kleur en prijs in yuan. Internationaal betaal je later, vanuit het magazijn.</p>
    <p><a class="btn" href="{escape(p["guide"])}">Gids stap voor stap</a>
       <a class="btn btn--ghost" href="{escape(OFFICIAL)}" rel="noopener">Officiële site</a></p>
  </div>{fig}</div></div>
</section>
"""
    return f"""
<section class="sec" id="shots">
  <div class="wrap"><div class="split split--rev"><div>
    <h2>Paste a Chinese link, or search in the app</h2>
    <p class="lead">LoveGoBuy starts the same way: paste a Taobao, 1688 or Weidian link, or type the name. The Chinese shop sees LoveGoBuy; you later see warehouse photos and a line to {escape(dest)}.</p>
    <p>If the search bar does not read the link, the next step is a manual form: name, size, colour and price in yuan. International freight is paid later, from the warehouse.</p>
    <p><a class="btn" href="{escape(p["guide"])}">Step-by-step guide</a>
       <a class="btn btn--ghost" href="{escape(OFFICIAL)}" rel="noopener">Official site</a></p>
  </div>{fig}</div></div>
</section>
"""


def _sec_states(key: str, fig) -> str:
    p = PACKS[key]
    loc, dest = p["loc"], p["dest_label"]
    store = escape(_storage(loc))
    if loc == "it":
        return f"""
<section class="sec" id="states">
  <div class="wrap"><div class="split"><div>
    <h2>Nove stati, tre schermate</h2>
    <p class="lead">Prima paghi il prodotto più il trasporto interno in Cina fino al magazzino. L’internazionale arriva dopo, quando scegli una linea verso l’Italia. «Perché è fermo?» quasi sempre significa: stai guardando la schermata sbagliata.</p>
    <p>I primi passi stanno sotto gli ordini, poi il magazzino, poi il pacco che invii. {store}</p>
    <p><a class="btn" href="{escape(p["guide"])}">Guida con il percorso</a></p>
  </div>{fig}</div></div>
</section>
"""
    if loc == "es":
        return f"""
<section class="sec" id="states">
  <div class="wrap"><div class="split"><div>
    <h2>Nueve estados, tres pantallas</h2>
    <p class="lead">Primero pagas el producto más el tramo interno en China hasta el almacén. El internacional llega después, cuando eliges una línea hacia {escape(dest)}. «¿Por qué está parado?» casi siempre significa: estás mirando la pantalla equivocada.</p>
    <p>Los primeros pasos están bajo pedidos, luego almacén, luego el paquete que envías. {store}</p>
    <p><a class="btn" href="{escape(p["guide"])}">Guía con el recorrido</a></p>
  </div>{fig}</div></div>
</section>
"""
    if loc == "nl":
        return f"""
<section class="sec" id="states">
  <div class="wrap"><div class="split"><div>
    <h2>Negen statussen, drie schermen</h2>
    <p class="lead">Eerst betaal je het product plus het binnenlandse traject in China tot het magazijn. Internationaal komt later, als je een lijn naar {escape(dest)} kiest. «Waarom staat het stil?» betekent bijna altijd: je kijkt naar het verkeerde scherm.</p>
    <p>De eerste stappen staan onder bestellingen, daarna magazijn, daarna het pakket dat je verzendt. {store}</p>
    <p><a class="btn" href="{escape(p["guide"])}">Gids met het pad</a></p>
  </div>{fig}</div></div>
</section>
"""
    return f"""
<section class="sec" id="states">
  <div class="wrap"><div class="split"><div>
    <h2>Nine statuses, three screens</h2>
    <p class="lead">You first pay the product plus domestic China freight to the warehouse. International comes later, when you pick a line to {escape(dest)}. “Why is it stuck?” is almost always: you are looking at the wrong screen.</p>
    <p>The first stretch lives under orders, then warehouse, then the parcel you submit. {store}</p>
    <p><a class="btn" href="{escape(p["guide"])}">Guide with the path</a></p>
  </div>{fig}</div></div>
</section>
"""


def _sec_restricted(key: str, fig) -> str:
    p = PACKS[key]
    loc = p["loc"]
    customs = p["customs"]
    if loc == "it":
        return f"""
<section class="sec sec--tint" id="restricted">
  <div class="wrap"><div class="split split--rev"><div>
    <h2>Molti prodotti non si possono comprare anche se compaiono</h2>
    <p class="lead">Sul sito ufficiale vedi schede senza prezzo, o un modulo manuale al posto di una scheda negozio. Non è un bug di questa homepage: il link sorgente non è acquistabile tramite l’agente, o il prezzo non si è letto.</p>
    <p>Regola: senza prezzo vero e varianti non ordinare. Tabacco, alcol e farmaci non viaggiano. Restricted è un blocco d’acquisto, non un avviso della {escape(customs)}. LoveGoBuy non vende merce propria.</p>
  </div>{fig}</div></div>
</section>
"""
    if loc == "es":
        return f"""
<section class="sec sec--tint" id="restricted">
  <div class="wrap"><div class="split split--rev"><div>
    <h2>Muchos productos no se pueden comprar aunque aparezcan</h2>
    <p class="lead">En el sitio oficial ves fichas sin precio, o un formulario manual en lugar de una ficha de tienda. No es un fallo de esta portada: el enlace de origen no se puede comprar por el agente, o el precio no se leyó.</p>
    <p>Regla: sin precio real y variantes, no pidas. Tabaco, alcohol y medicamentos no viajan. Restricted es un bloqueo de compra, no un aviso de {escape(customs)}. LoveGoBuy no vende mercancía propia.</p>
  </div>{fig}</div></div>
</section>
"""
    if loc == "nl":
        return f"""
<section class="sec sec--tint" id="restricted">
  <div class="wrap"><div class="split split--rev"><div>
    <h2>Veel producten kun je niet kopen, ook al staan ze er</h2>
    <p class="lead">Op de officiële site zie je kaarten zonder prijs, of een handmatig formulier in plaats van een shopkaart. Dat is geen bug van deze homepage: de bronlink is via de agent niet te koop, of de prijs liet zich niet lezen.</p>
    <p>Regel: zonder echte prijs en varianten niet bestellen. Tabak, alcohol en geneesmiddelen reizen niet. Restricted is een koopblokkade, geen bericht van {escape(customs)}. LoveGoBuy verkoopt geen eigen voorraad.</p>
  </div>{fig}</div></div>
</section>
"""
    return f"""
<section class="sec sec--tint" id="restricted">
  <div class="wrap"><div class="split split--rev"><div>
    <h2>Many products you cannot buy even if they appear</h2>
    <p class="lead">On the official site you will see cards without a price, or a manual form instead of a shop card. That is not a bug of this homepage: the source link is not buyable through the agent, or the price could not be read.</p>
    <p>Rule: without a real price and variants, do not order. Tobacco, alcohol and medicines do not travel. Restricted is a purchase block, not a {escape(customs)} seizure notice. LoveGoBuy does not sell its own stock.</p>
  </div>{fig}</div></div>
</section>
"""


def _hero(key: str, aria: str, label: str, placeholder: str, button: str) -> str:
    p = PACKS[key]
    sheet = _sheet(desk_for(key))
    return f"""
<section class="hero">
  <div class="hero__bg" role="img" aria-label="{escape(aria)}"></div>
  <div class="hero__scrim"></div>
  <div class="wrap">
    <span class="eyebrow">{escape(p["eyebrow"])}</span>
    <h1>{escape(p["hero_h1"])}</h1>
    <p class="lead">{escape(p["lead"])}</p>
    <div class="sbox">
      <form id="w2c-search" action="{escape(sheet)}" method="get" target="_blank" rel="nofollow noopener" role="search">
        <label class="skip" for="q">{escape(label)}</label>
        <input id="q" name="q" type="search" autocomplete="off" placeholder="{escape(placeholder)}">
        <input type="hidden" name="utm_source" value="{escape(p["host"])}">
        <input type="hidden" name="utm_medium" value="referral">
        <input type="hidden" name="utm_campaign" value="hero-buscador">
        <button type="submit">{escape(button)}</button>
      </form>
      <div class="chips">{_chips(key)}</div>
    </div>
  </div>
</section>"""


def build_home(key: str) -> str:
    p = PACKS[key]
    desk = desk_for(key)
    wall = _wall(key)
    fig_off, fig_sheet, fig_vol, fig_zoek, _fig_diy = _shots(key)
    dest = p["dest_label"]
    loc = p["loc"]
    shots = _sec_shots(key, fig_zoek)
    states = _sec_states(key, fig_off)
    restricted = _sec_restricted(key, fig_sheet)
    if loc == "it":
        hero = _hero(key, "Homepage ufficiale LoveGoBuy", "Cerca prodotti su w2clinks", "Cerca sneakers, hoodie, giacca…", "Cerca")
        body = f"""{hero}
<section class="sec sec--first" id="agent">
  <div class="wrap"><div class="split"><div>
    <h2>Un agente d’acquisto è un intermediario, non un negozio</h2>
    <p class="lead">LoveGoBuy non vende merce propria. Compra per te nei negozi cinesi che non spediscono all’estero, riceve il pacco in magazzino, lo fotografa, lo conserva e lo spedisce in Italia quando decidi tu.</p>
    <p>Paghi due volte (prima il prodotto, poi l’internazionale) e aspetti due volte. In mezzo puoi ancora annullare, consolidare o cambiare linea. Pagamenti e ticket restano su {escape(OFFICIAL)}.</p>
    <p><a class="btn" href="{escape(p["guide"])}">Guida passo passo</a></p>
  </div>{fig_off}</div></div>
</section>
{shots}
<section class="sec sec--tint" id="sheet-explain">
  <div class="wrap"><div class="split split--rev"><div>
    <span class="eyebrow" style="color:var(--acd)">Un nome che inganna</span>
    <h2>Uno spreadsheet non è un file Excel</h2>
    <p class="lead">In italiano «spreadsheet» suona come una griglia. Qui è un catalogo di schede prodotto con foto, marca, prezzo di riferimento e il link da incollare nell’agente.</p>
    <p>Su w2clinks vedi schede, non celle.</p>
    <p><a class="btn btn--ghost" href="{escape(p["catalog"])}">Come funziona il catalogo</a></p>
  </div>{fig_sheet}</div></div>
</section>
<section class="sec" id="cat-wall">
  <div class="wrap">
    <h2>Trentatré categorie per il primo giorno</h2>
    <p class="lead">Ogni scheda apre quella categoria nel catalogo. Parti da una: cinque categorie nel primo haul sono la via più rapida verso una scatola cara e scomoda.</p>
    <div class="cat-grid">{wall}</div>
  </div>
</section>
{states}
<section class="sec sec--tint" id="lab">
  <div class="wrap"><div class="split"><div>
    <h2>L’Italia ha linee, ma non ogni linea è aperta</h2>
    <p class="lead">Nell’estimator scegli destinazione <strong>{escape(p["dest_zh"])}</strong>, non EU. L’indirizzo è una {escape(p["postal"])}.</p>
    <p>L’estimator ufficiale sta su {escape(EST)}: scegli il paese, non questo hostname. Questa guida non inventa una linea, un transito né un importo. Fonte: <a href="{escape(p["customs_url"])}" rel="noopener">{escape(p["customs"])}</a>.</p>
    <p><a class="btn" href="{escape(EST)}">Estimator ufficiale LoveGoBuy</a>
       <a class="btn btn--ghost" href="{escape(p["ship"])}">Piano spedizione</a></p>
  </div>{fig_off}</div></div>
</section>
<section class="sec" id="volume">
  <div class="wrap"><div class="split split--rev"><div>
    <h2>Il peso che paghi quasi mai è solo la bilancia</h2>
    <p class="lead">Molte linee fatturano il massimo tra bilancia e volume. Un divisore comune è L×W×H (cm) / 8000. Un piumino è leggero e ingombrante: lì decide il volume.</p>
    <p>Esempio: 40×40×3 cm sono 4800 cm³, divisi per 8000 sono 600 g di volume a 200 g reali. Le tue misure le inserisci nell’estimator ufficiale, destinazione Italia.</p>
  </div>{fig_vol}</div></div>
</section>
{restricted}
<section class="sec" id="faq">
  <div class="wrap">
    <h2>Aiuto, novità e dove chiedere</h2>
    <p class="lead">I dubbi dei primi ordini si ripetono. Stanno su Aiuto — un URL proprio, non un’appendice di questa homepage.</p>
    <p><a class="btn" href="{escape(p["help"])}">Tutte le domande su Aiuto</a>
       <a class="btn btn--ghost" href="{escape(p["news"])}">Check datati su Novità</a>
       <a class="btn btn--ghost" href="{escape(p["about"])}">Chi siamo</a></p>
  </div>
</section>
"""
        desc = "Guida indipendente in italiano: come compri in Cina con LoveGoBuy, come funziona il catalogo w2clinks, come un pacco arriva in Italia."
    elif loc == "es":
        hero = _hero(key, "Portada oficial de LoveGoBuy", "Buscar productos en w2clinks", "Busca zapatillas, hoodie, chaqueta…", "Buscar")
        body = f"""{hero}
<section class="sec sec--first" id="agent">
  <div class="wrap"><div class="split"><div>
    <h2>Un agente de compras es un intermediario, no una tienda</h2>
    <p class="lead">LoveGoBuy no vende mercancía propia. Compra por ti en tiendas chinas que no envían al extranjero, recibe el paquete en el almacén, lo fotografía, lo guarda y lo envía a {escape(dest)} cuando tú lo decides.</p>
    <p>Pagas dos veces (primero el producto, luego el internacional) y esperas dos veces. En medio aún puedes cancelar, consolidar o cambiar de línea. Pagos y tickets siguen en {escape(OFFICIAL)}.</p>
    <p><a class="btn" href="{escape(p["guide"])}">Guía paso a paso</a></p>
  </div>{fig_off}</div></div>
</section>
{shots}
<section class="sec sec--tint" id="sheet-explain">
  <div class="wrap"><div class="split split--rev"><div>
    <span class="eyebrow" style="color:var(--acd)">Un nombre que engaña</span>
    <h2>Un spreadsheet no es un archivo Excel</h2>
    <p class="lead">En español «spreadsheet» suena a filas y columnas. Aquí es un catálogo de fichas de producto con foto, marca, precio de referencia y el enlace que pegas en el agente.</p>
    <p>En w2clinks ves fichas, no celdas.</p>
    <p><a class="btn btn--ghost" href="{escape(p["catalog"])}">Cómo funciona el catálogo</a></p>
  </div>{fig_sheet}</div></div>
</section>
<section class="sec" id="cat-wall">
  <div class="wrap">
    <h2>Treinta y tres categorías para el primer día</h2>
    <p class="lead">Cada ficha abre esa categoría en el catálogo. Empieza con una: cinco categorías en el primer haul es el camino más rápido a una caja cara e incómoda.</p>
    <div class="cat-grid">{wall}</div>
  </div>
</section>
{states}
<section class="sec sec--tint" id="lab">
  <div class="wrap"><div class="split"><div>
    <h2>{escape(dest)} tiene líneas, pero no todas están abiertas</h2>
    <p class="lead">En el estimador elige destino <strong>{escape(p["dest_zh"])}</strong>, no EU. La dirección es una {escape(p["postal"])}.</p>
    <p>El estimador oficial está en {escape(EST)}: elige el país, no este hostname. Esta guía no inventa una línea, un tránsito ni un importe. Fuente: <a href="{escape(p["customs_url"])}" rel="noopener">{escape(p["customs"])}</a>.</p>
    <p><a class="btn" href="{escape(EST)}">Estimador oficial LoveGoBuy</a>
       <a class="btn btn--ghost" href="{escape(p["ship"])}">Plan de envío</a></p>
  </div>{fig_off}</div></div>
</section>
<section class="sec" id="volume">
  <div class="wrap"><div class="split split--rev"><div>
    <h2>El peso que pagas casi nunca es solo la báscula</h2>
    <p class="lead">Muchas líneas facturan el máximo entre báscula y volumen. Un divisor habitual es L×W×H (cm) / 8000. Un plumífero es ligero y voluminoso: ahí decide el volumen.</p>
    <p>Ejemplo: 40×40×3 cm son 4800 cm³, divididos por 8000 son 600 g de volumen con 200 g reales. Tus medidas las metes en el estimador oficial, destino {escape(dest)}.</p>
  </div>{fig_vol}</div></div>
</section>
{restricted}
<section class="sec" id="faq">
  <div class="wrap">
    <h2>Ayuda, novedades y dónde preguntar</h2>
    <p class="lead">Las dudas de los primeros pedidos se repiten. Están en Ayuda — una URL propia, no un apéndice de esta portada.</p>
    <p><a class="btn" href="{escape(p["help"])}">Todas las preguntas en Ayuda</a>
       <a class="btn btn--ghost" href="{escape(p["news"])}">Checks con fecha en Novedades</a>
       <a class="btn btn--ghost" href="{escape(p["about"])}">Sobre nosotros</a></p>
  </div>
</section>
"""
        desc = f"Guía independiente en español: cómo compras en China con LoveGoBuy, cómo funciona el catálogo w2clinks, cómo viaja un paquete a {dest}."
    elif loc == "nl":
        hero = _hero(key, "Officiële LoveGoBuy-homepage", "Producten zoeken op w2clinks", "Zoek sneakers, hoodie, jas…", "Zoeken")
        body = f"""{hero}
<section class="sec sec--first" id="agent">
  <div class="wrap"><div class="split"><div>
    <h2>Een inkoopagent is een tussenpersoon, geen shop</h2>
    <p class="lead">LoveGoBuy verkoopt geen eigen voorraad. Hij koopt voor jou in Chinese shops die niet naar het buitenland sturen, neemt het pakket in het magazijn aan, fotografeert het, slaat het op en stuurt het naar {escape(dest)} als jij dat besluit.</p>
    <p>Je betaalt twee keer (eerst het product, later internationaal) en wacht twee keer. Daartussen kun je nog annuleren, bundelen of van lijn wisselen. Betaling en tickets blijven op {escape(OFFICIAL)}.</p>
    <p><a class="btn" href="{escape(p["guide"])}">Gids stap voor stap</a></p>
  </div>{fig_off}</div></div>
</section>
{shots}
<section class="sec sec--tint" id="sheet-explain">
  <div class="wrap"><div class="split split--rev"><div>
    <span class="eyebrow" style="color:var(--acd)">Een naam die misleidt</span>
    <h2>Een spreadsheet is geen Excel-bestand</h2>
    <p class="lead">«Spreadsheet» klinkt naar rijen en kolommen. Hier is het een catalogus van productkaarten met foto, merk, referentieprijs en de link die je in de agent plakt.</p>
    <p>Op w2clinks zie je kaarten, geen cellen.</p>
    <p><a class="btn btn--ghost" href="{escape(p["catalog"])}">Zo werkt de catalogus</a></p>
  </div>{fig_sheet}</div></div>
</section>
<section class="sec" id="cat-wall">
  <div class="wrap">
    <h2>Drieëndertig categorieën voor de eerste dag</h2>
    <p class="lead">Elke kaart opent die categorie in de catalogus. Begin met één: vijf categorieën in de eerste haul is de snelste weg naar een dure, onhandige doos.</p>
    <div class="cat-grid">{wall}</div>
  </div>
</section>
{states}
<section class="sec sec--tint" id="lab">
  <div class="wrap"><div class="split"><div>
    <h2>{escape(dest)} heeft lijnen, maar niet elke lijn is open</h2>
    <p class="lead">Kies in de schatter bestemming <strong>{escape(p["dest_zh"])}</strong>, niet EU. Het afleveradres is een {escape(p["postal"])}.</p>
    <p>De officiële schatter staat op {escape(EST)}: kies het land, niet deze hostnaam. Deze gids verzint geen lijn, transittijd of bedrag. Bron: <a href="{escape(p["customs_url"])}" rel="noopener">{escape(p["customs"])}</a>.</p>
    <p><a class="btn" href="{escape(EST)}">Officiële LoveGoBuy-schatter</a>
       <a class="btn btn--ghost" href="{escape(p["ship"])}">Verzendplan</a></p>
  </div>{fig_off}</div></div>
</section>
<section class="sec" id="volume">
  <div class="wrap"><div class="split split--rev"><div>
    <h2>Het gewicht dat je betaalt is bijna nooit alleen de weegschaal</h2>
    <p class="lead">Veel lijnen factureren het maximum van weegschaal en volume. Een gebruikelijke deler is L×W×H (cm) / 8000. Een donsjas is licht en volumineus: daar beslist het volume.</p>
    <p>Voorbeeld: 40×40×3 cm is 4800 cm³, gedeeld door 8000 is 600 g volume bij 200 g echt gewicht. Jouw maten vul je in de officiële schatter in, bestemming {escape(dest)}.</p>
  </div>{fig_vol}</div></div>
</section>
{restricted}
<section class="sec" id="faq">
  <div class="wrap">
    <h2>Hulp, nieuws en waar je vraagt</h2>
    <p class="lead">De twijfels van de eerste bestelling herhalen zich. Ze staan op Hulp — een eigen URL, geen bijlage van deze homepage.</p>
    <p><a class="btn" href="{escape(p["help"])}">Alle vragen op Hulp</a>
       <a class="btn btn--ghost" href="{escape(p["news"])}">Gedateerde checks op Nieuws</a>
       <a class="btn btn--ghost" href="{escape(p["about"])}">Over ons</a></p>
  </div>
</section>
"""
        desc = f"Onafhankelijke gids in het Nederlands: hoe je via LoveGoBuy in China koopt, hoe de w2clinks-catalogus werkt, hoe een pakket naar {dest} reist."
    else:
        hero = _hero(key, "Official LoveGoBuy homepage", "Search products on w2clinks", "Search sneakers, hoodie, jacket…", "Search")
        body = f"""{hero}
<section class="sec sec--first" id="agent">
  <div class="wrap"><div class="split"><div>
    <h2>A purchasing agent is a middleman, not a shop</h2>
    <p class="lead">LoveGoBuy does not sell its own goods. It buys for you in Chinese shops that do not ship abroad, receives the parcel in the warehouse, photographs it, stores it, and ships to {escape(dest)} when you decide.</p>
    <p>That changes everything: you pay twice (first the product, later international), you wait twice, and in between you can still cancel, consolidate or switch lines. Payment and tickets stay on {escape(OFFICIAL)}.</p>
    <p><a class="btn" href="{escape(p["guide"])}">Step-by-step guide</a></p>
  </div>{fig_off}</div></div>
</section>
{shots}
<section class="sec sec--tint" id="sheet-explain">
  <div class="wrap"><div class="split split--rev"><div>
    <span class="eyebrow" style="color:var(--acd)">A name that misleads</span>
    <h2>A spreadsheet is not an Excel file</h2>
    <p class="lead">In English the word still sounds like a grid of rows and columns. Here «spreadsheet» means a catalogue of product cards with a photo, a brand, a reference price and the link you paste into the agent.</p>
    <p>What you see on w2clinks are cards, not cells. Each fiche has the link LoveGoBuy needs.</p>
    <p><a class="btn btn--ghost" href="{escape(p["catalog"])}">How the catalogue works</a></p>
  </div>{fig_sheet}</div></div>
</section>
<section class="sec" id="cat-wall">
  <div class="wrap">
    <h2>Thirty-three categories for the first day</h2>
    <p class="lead">Each card opens that category in the catalogue. Start with one: five categories in the first haul is the fastest way to an expensive, awkward box.</p>
    <div class="cat-grid">{wall}</div>
  </div>
</section>
{states}
<section class="sec sec--tint" id="lab">
  <div class="wrap"><div class="split"><div>
    <h2>{escape(dest[0].upper() + dest[1:])} has lines, but not every line is open</h2>
    <p class="lead">Pick destination <strong>{escape(p["dest_zh"])}</strong> in the official estimator. The delivery address is a {escape(p["postal"])}.</p>
    <p>The official estimator lives at lovegobuy.com{escape(EST_PATH)} — pick the dest country, not this hostname. This desk does not invent a line, a transit-day count or a money amount. Open {escape(OFFICIAL)} the morning you ship. Import: <a href="{escape(p["customs_url"])}" rel="noopener">{escape(p["customs"])}</a>.</p>
    <p><a class="btn" href="{escape(EST)}">Official LoveGoBuy estimator</a>
       <a class="btn btn--ghost" href="{escape(p["ship"])}">Shipping plan</a></p>
  </div>{fig_off}</div></div>
</section>
<section class="sec" id="volume">
  <div class="wrap"><div class="split split--rev"><div>
    <h2>The weight you pay is almost never the scale alone</h2>
    <p class="lead">Many lines bill the greater of scale and volume. A common divisor is L×W×H (cm) / 8000. A down jacket is light and bulky: volume decides.</p>
    <p>Example: 40×40×3 cm is 4800 cm³, divided by 8000 is 600 g volume at 200 g real weight. You enter your measurements in the official estimator, destination {escape(p["dest_zh"].split("—")[0].strip())}.</p>
  </div>{fig_vol}</div></div>
</section>
{restricted}
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
            f"Independent English guide: how you buy in China through LoveGoBuy, how the w2clinks catalogue works, how a parcel travels to {dest}."
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
    loc = p["loc"]
    notes = {"it": CAT_NOTES_IT, "es": CAT_NOTES_ES, "nl": CAT_NOTES_NL}.get(loc, CAT_NOTES_EN)
    wall = _wall(key, notes)
    _fig_off, fig_sheet, _fig_vol, fig_zoek, fig_diy = _shots(key)
    dest = p["dest_label"]
    sheet = _sheet(desk)
    keys = _keys_table(key)
    if loc == "it":
        topic = "cos’è e quali categorie trovi"
        body = f"""
<section class="sec sec--first"><div class="wrap"><div class="split"><div>
<span class="eyebrow" style="color:var(--acc)">Il catalogo</span>
<h1>Che cos’è LoveGoBuy Spreadsheet, e cosa ci trovi</h1>
<p class="lead">Un catalogo di schede prodotto, non un file Excel. Trentatré categorie, filtri, foto, marca e il link per l’agente.</p>
</div>{fig_sheet}</div></div></section>
<section class="sec sec--tint"><div class="wrap"><div class="split split--rev"><div>
<h2>Perché un catalogo a parte</h2>
<p>La ricerca dell’agente restituisce tutto lo stock cinese, enorme e spesso in cinese. Un catalogo ha già fatto il lavoro: qualcuno ha scelto quali schede valgono, le ha messe in categoria e ha pronto il link del negozio.</p>
<p>In pratica: trovi la scheda su w2clinks, copi il link sorgente e lo incolli nella ricerca di LoveGoBuy o nel modulo manuale. Il catalogo non incassa e non vende.</p>
</div>{fig_zoek}</div></div></section>
<section class="sec" id="categorias"><div class="wrap">
<h2>Le trentatré categorie, e cosa controlli in ciascuna</h2>
<p class="lead">La frase sotto ogni scheda non è riempitivo: è l’errore che in quella categoria torna più spesso quando compri da lontano.</p>
<div class="cat-grid cat-grid--rich">{wall}</div>
</div></section>
<section class="sec sec--tint" id="first-category"><div class="wrap">
<h2>Come scegli la prima categoria</h2>
<p class="lead">Primo ordine: qualcosa di piatto e leggero — t-shirt, shorts, gioielli. Arrivano prima, costano meno di nolo, e controlli tutto il circuito senza rischiare troppo.</p>
<p>Il voluminoso per il secondo ordine: piumini, borse, cappelli. Non perché siano peggiori, ma perché il nolo dipende dal volume — e quello lo calcoli bene solo dopo un giro.</p>
<p>Tre categorie con extra: elettronica (spesso litio), occhiali (fragili) e tutto con batteria o magnete. Non ogni linea verso l’Italia li accetta. Controlla l’estimator prima di lasciarli in magazzino.</p>
</div></section>
<section class="sec" id="keys"><div class="wrap">
<h2>Dato scomodo: il catalogo cerca in inglese</h2>
<p class="lead">L’abbiamo verificato termine per termine il {escape(DATE)}. Conviene saperlo prima di digitare la prima ricerca in italiano.</p>
<p>Grafie locali come scarpe, felpa o occhiali danno spesso zero. Le key inglesi sneakers, hoodie, jacket, trousers, bag, glasses o watch danno pagine. Per questo la ricerca in homepage manda key inglesi a w2clinks.</p>
{keys}
</div></section>
<section class="sec sec--tint"><div class="wrap"><div class="split"><div>
<h2>Dal catalogo all’ordine, senza perdere il link</h2>
<p class="lead">La scheda è l’inizio, non la cassa. Il passo che fallisce più spesso: copi l’URL della scheda catalogo invece del link negozio. A LoveGoBuy serve il link Taobao, 1688 o Weidian.</p>
<p>Se incolli l’URL della scheda catalogo, l’agente non sa cosa comprare. Copia il link del negozio, incollalo nella ricerca di LoveGoBuy, controlla prezzo e variante, e paga l’internazionale solo quando le foto di magazzino tornano.</p>
<p>Se la ricerca non legge il link, resta il modulo manuale del sito ufficiale. Schede senza prezzo: saltale — il link sorgente in Cina è spesso già morto.</p>
<p><a class="btn" href="{escape(sheet)}">Apri il catalogo su w2clinks</a>
   <a class="btn btn--ghost" href="{escape(p["guide"])}">Guida passo passo</a></p>
</div>{fig_diy}</div></div></section>
"""
    elif loc == "es":
        topic = "qué es y qué categorías encuentras"
        body = f"""
<section class="sec sec--first"><div class="wrap"><div class="split"><div>
<span class="eyebrow" style="color:var(--acc)">El catálogo</span>
<h1>Qué es LoveGoBuy Spreadsheet, y qué encuentras dentro</h1>
<p class="lead">Un catálogo de fichas de producto, no un archivo Excel. Treinta y tres categorías, filtros, foto, marca y el enlace para el agente.</p>
</div>{fig_sheet}</div></div></section>
<section class="sec sec--tint"><div class="wrap"><div class="split split--rev"><div>
<h2>Por qué un catálogo aparte</h2>
<p>La búsqueda del agente devuelve todo el stock chino, enorme y a menudo en chino. Un catálogo ya hizo el trabajo: alguien eligió qué fichas merecen, las puso en categoría y dejó listo el enlace de la tienda.</p>
<p>En la práctica: encuentras la ficha en w2clinks, copias el enlace de origen y lo pegas en la búsqueda de LoveGoBuy o en el formulario manual. El catálogo no cobra y no vende.</p>
</div>{fig_zoek}</div></div></section>
<section class="sec" id="categorias"><div class="wrap">
<h2>Las treinta y tres categorías, y qué miras en cada una</h2>
<p class="lead">La frase bajo cada ficha no es relleno: es el error que más se repite en esa categoría cuando compras a distancia.</p>
<div class="cat-grid cat-grid--rich">{wall}</div>
</div></section>
<section class="sec sec--tint" id="first-category"><div class="wrap">
<h2>Cómo eliges la primera categoría</h2>
<p class="lead">Primer pedido: algo plano y ligero — camisetas, shorts, joyería. Llegan antes, cuestan menos de envío, y compruebas todo el circuito sin arriesgar mucho.</p>
<p>Lo voluminoso para el segundo pedido: plumíferos, bolsos, gorras. No porque sean peores, sino porque el porte depende del volumen — y eso lo calculas bien después de una ronda.</p>
<p>Tres categorías con extra: electrónica (a menudo litio), gafas (frágiles) y todo con batería o imán. No todas las líneas hacia {escape(dest)} lo aceptan. Mira el estimador antes de dejarlos en el almacén.</p>
</div></section>
<section class="sec" id="keys"><div class="wrap">
<h2>Dato incómodo: el catálogo busca en inglés</h2>
<p class="lead">Lo comprobamos término a término el {escape(DATE)}. Conviene saberlo antes de escribir la primera búsqueda en español.</p>
<p>Grafías locales como zapatillas, sudadera o gafas suelen dar cero. Las keys inglesas sneakers, hoodie, jacket, trousers, bag, glasses o watch dan páginas. Por eso la búsqueda de la portada manda keys inglesas a w2clinks.</p>
{keys}
</div></section>
<section class="sec sec--tint"><div class="wrap"><div class="split"><div>
<h2>Del catálogo al pedido, sin perder el enlace</h2>
<p class="lead">La ficha es el principio, no la caja. El paso que más falla: copias la URL de la ficha del catálogo en vez del enlace de la tienda. LoveGoBuy necesita el enlace Taobao, 1688 o Weidian.</p>
<p>Si pegas la URL de la ficha del catálogo, el agente no sabe qué comprar. Copia el enlace de la tienda, pégalo en la búsqueda de LoveGoBuy, revisa precio y variante, y paga el internacional solo cuando las fotos de almacén cuadran.</p>
<p>Si la búsqueda no lee el enlace, queda el formulario manual del sitio oficial. Fichas sin precio: sáltalas — el enlace de origen en China a menudo ya está muerto.</p>
<p><a class="btn" href="{escape(sheet)}">Abrir el catálogo en w2clinks</a>
   <a class="btn btn--ghost" href="{escape(p["guide"])}">Guía paso a paso</a></p>
</div>{fig_diy}</div></div></section>
"""
    elif loc == "nl":
        topic = "wat het is en welke categorieën je vindt"
        body = f"""
<section class="sec sec--first"><div class="wrap"><div class="split"><div>
<span class="eyebrow" style="color:var(--acc)">De catalogus</span>
<h1>Wat LoveGoBuy Spreadsheet is, en wat je erin vindt</h1>
<p class="lead">Een catalogus van productkaarten, geen Excel-bestand. Drieëndertig categorieën, filters, foto, merk en de link voor de agent.</p>
</div>{fig_sheet}</div></div></section>
<section class="sec sec--tint"><div class="wrap"><div class="split split--rev"><div>
<h2>Waarom een aparte catalogus</h2>
<p>De zoekbalk van een agent geeft de hele Chinese voorraad, enorm en vaak in het Chinees. Een catalogus heeft het huiswerk al gedaan: iemand koos welke kaarten de moeite waard zijn, zette ze in een categorie en legde de shoplink klaar.</p>
<p>In de praktijk: je vindt de kaart op w2clinks, kopieert de bronlink en plakt die in de LoveGoBuy-zoekbalk of het handmatige formulier. De catalogus int niets en verkoopt niets.</p>
</div>{fig_zoek}</div></div></section>
<section class="sec" id="categorias"><div class="wrap">
<h2>De drieëndertig categorieën, en wat je in elk checkt</h2>
<p class="lead">De zin onder elke kaart is geen vulling: het is de fout die in die categorie het vaakst terugkomt als je van ver koopt.</p>
<div class="cat-grid cat-grid--rich">{wall}</div>
</div></section>
<section class="sec sec--tint" id="first-category"><div class="wrap">
<h2>Hoe je de eerste categorie kiest</h2>
<p class="lead">Eerste bestelling: iets flats en lichts — T-shirts, shorts, sieraden. Die komen eerder aan, kosten minder porto, en je checkt de hele ronde zonder veel geld.</p>
<p>Volumineus voor de tweede order: donsjassen, tassen, petten. Niet omdat ze slechter zijn, maar omdat hun porto van volume afhangt — en dat reken je pas goed als je één ronde hebt gezien.</p>
<p>Drie categorieën met extra voorwaarden: elektronica (vaak lithium), brillen (breekbaar) en alles met accu of magneet. Niet elke lijn naar {escape(dest)} neemt dat. Check de schatter voordat ze in het magazijn blijven liggen.</p>
</div></section>
<section class="sec" id="keys"><div class="wrap">
<h2>Ongemakkelijk feit: de catalogus zoekt in het Engels</h2>
<p class="lead">We hebben het woord voor woord nagekeken op {escape(DATE)}. Dat wil je weten voordat je de eerste zoekopdracht in het Nederlands typt.</p>
<p>Lokale spellingen zoals sneakers, trui of bril geven vaak nul. De Engelse keys sneakers, hoodie, jacket, trousers, bag, glasses of watch geven pagina’s. Daarom stuurt de homepage-zoekbalk Engelse keys naar w2clinks.</p>
{keys}
</div></section>
<section class="sec sec--tint"><div class="wrap"><div class="split"><div>
<h2>Van catalogus naar bestelling, zonder de link te verliezen</h2>
<p class="lead">De kaart is het begin, niet de kassa. De stap die het vaakst misgaat: je kopieert de catalogus-URL in plaats van de shoplink. LoveGoBuy heeft de Taobao-, 1688- of Weidian-link nodig.</p>
<p>Plak je de URL van de cataloguskaart zelf, dan weet de agent niet wat hij moet kopen. Kopieer de shoplink, plak hem in de LoveGoBuy-zoekbalk, check prijs en variant, en betaal internationaal pas als de magazijnfoto’s kloppen.</p>
<p>Leest de zoekbalk de link niet, blijft het handmatige formulier op de officiële site. Kaarten zonder prijs overslaan — de bronlink is in China vaak al dood.</p>
<p><a class="btn" href="{escape(sheet)}">Catalogus op w2clinks openen</a>
   <a class="btn btn--ghost" href="{escape(p["guide"])}">Gids stap voor stap</a></p>
</div>{fig_diy}</div></div></section>
"""
    else:
        topic = "what it is and which categories you will find"
        body = f"""
<section class="sec sec--first"><div class="wrap"><div class="split"><div>
<span class="eyebrow" style="color:var(--acc)">The catalogue</span>
<h1>What LoveGoBuy Spreadsheet is, and what you find in it</h1>
<p class="lead">It is a catalogue of product cards, not an Excel file. Thirty-three categories, filters, and cards with a photo, a brand and the link for the agent.</p>
</div>{fig_sheet}</div></div></section>
<section class="sec sec--tint"><div class="wrap"><div class="split split--rev"><div>
<h2>Why a separate catalogue</h2>
<p>An agent search bar returns the whole stock of Chinese shops, huge and often in Chinese. A catalogue does the homework: someone already picked which fiches are worth it, put them in a category and left the shop link ready.</p>
<p>In practice: you find the fiche on w2clinks, copy the source link and paste it into LoveGoBuy search or the manual form. The catalogue collects no money and sells nothing.</p>
</div>{fig_zoek}</div></div></section>
<section class="sec" id="categorias"><div class="wrap">
<h2>The thirty-three categories, and what you check in each</h2>
<p class="lead">The line under each card is not filler: it is the mistake that comes back most often in that category when you buy from a distance.</p>
<div class="cat-grid cat-grid--rich">{wall}</div>
</div></section>
<section class="sec sec--tint" id="first-category"><div class="wrap">
<h2>How you pick the first category</h2>
<p class="lead">If it is your first order, pick something flat and light: T-shirts, shorts, jewelry. They arrive sooner, cost less to send, and let you check the whole circuit without risking much money.</p>
<p>Leave bulky for the second order: down jackets, bags, hats. Not because they are worse, but because their freight depends on volume — and you only calculate that well after one round.</p>
<p>Three categories with extra conditions: electronics (often lithium), glasses (fragile) and anything with a battery or a magnet. Not every line to {escape(dest)} accepts those. Check the official estimator before you leave them in the warehouse.</p>
</div></section>
<section class="sec" id="keys"><div class="wrap">
<h2>Uncomfortable fact: the catalogue searches in English</h2>
<p class="lead">We checked it term by term on {escape(DATE)}. You want that before you type the first search in a local spelling.</p>
<p>Local spellings often returned zero. The English keys sneakers, hoodie, jacket, trousers, bag, glasses or watch returned pages of fiches. That is why the homepage search bar still sends English keys to w2clinks.</p>
{keys}
</div></section>
<section class="sec sec--tint"><div class="wrap"><div class="split"><div>
<h2>From catalogue to order, without losing the link</h2>
<p class="lead">The fiche is the start, not checkout. The step that fails most often is copying the catalogue URL instead of the shop link. LoveGoBuy needs the Taobao, 1688 or Weidian link.</p>
<p>If you paste the catalogue-card URL itself, the agent does not know what to buy. Copy the shop link, paste it into LoveGoBuy search, check price and variant, and pay international only after the warehouse photos match.</p>
<p>If search does not read the link, the manual order form on the official site remains. Skip cards without a price — that source link is often already dead in China.</p>
<p><a class="btn" href="{escape(sheet)}">Open the catalogue on w2clinks</a>
   <a class="btn btn--ghost" href="{escape(p["guide"])}">Step-by-step guide</a></p>
</div>{fig_diy}</div></div></section>
"""
    return cms_shell(
        desk, page_title(desk, topic),
        "Independent catalogue guide: thirty-three w2clinks categories.",
        f"https://{p['host']}{p['catalog']}", [], body, p["catalog"],
    )


def build_help(key: str) -> str:
    p = PACKS[key]
    desk = desk_for(key)
    pairs = _faqs(key)
    html_f = _faq_grouped_html(key)
    fig_off, *_ = _shots(key)
    loc = p["loc"]
    if loc == "it":
        topic = "aiuto e domande frequenti"
        body = f"""
<article class="pw">
  <span class="eyebrow" style="color:var(--acd)">Aiuto</span>
  <h1>Aiuto e domande su LoveGoBuy in Italia</h1>
  <p class="lead">Domande dei primi ordini. L’indirizzo è una {escape(p["postal"])}.</p>
  {fig_off}{html_f}
  <p><a class="btn" href="{escape(EST)}">Estimator ufficiale LoveGoBuy</a>
     <a class="btn btn--ghost" href="{escape(p["ship"])}">Piano spedizione</a></p>
</article>
"""
    elif loc == "es":
        topic = "ayuda y preguntas frecuentes"
        body = f"""
<article class="pw">
  <span class="eyebrow" style="color:var(--acd)">Ayuda</span>
  <h1>Ayuda y preguntas sobre LoveGoBuy en {escape(p["dest_label"])}</h1>
  <p class="lead">Preguntas de los primeros pedidos. La dirección es una {escape(p["postal"])}.</p>
  {fig_off}{html_f}
  <p><a class="btn" href="{escape(EST)}">Estimador oficial LoveGoBuy</a>
     <a class="btn btn--ghost" href="{escape(p["ship"])}">Plan de envío</a></p>
</article>
"""
    elif loc == "nl":
        topic = "hulp en veelgestelde vragen"
        body = f"""
<article class="pw">
  <span class="eyebrow" style="color:var(--acd)">Hulp</span>
  <h1>Hulp en vragen over LoveGoBuy in {escape(p["dest_label"])}</h1>
  <p class="lead">Vragen van eerste bestellingen. Het afleveradres is een {escape(p["postal"])}.</p>
  {fig_off}{html_f}
  <p><a class="btn" href="{escape(EST)}">Officiële LoveGoBuy-schatter</a>
     <a class="btn btn--ghost" href="{escape(p["ship"])}">Verzendplan</a></p>
</article>
"""
    else:
        topic = "help and frequently asked questions"
        body = f"""
<article class="pw">
  <span class="eyebrow" style="color:var(--acd)">Help</span>
  <h1>Help and questions about LoveGoBuy in {escape(p["dest_label"])}</h1>
  <p class="lead">Questions that come back on first orders. The delivery address uses a {escape(p["postal"])}.</p>
  {fig_off}{html_f}
  <p><a class="btn" href="{escape(EST)}">Official LoveGoBuy estimator</a>
     <a class="btn btn--ghost" href="{escape(p["ship"])}">Shipping plan</a></p>
</article>
"""
    return cms_shell(
        desk, page_title(desk, topic),
        f"FAQ about LoveGoBuy from {p['dest_label']}.",
        f"https://{p['host']}{p['help']}", [faq_ld(p["lang"], pairs)], body, p["help"],
    )


def build_news(key: str) -> str:
    p = PACKS[key]
    desk = desk_for(key)
    loc = p["loc"]
    if loc == "it":
        items = [
            ("Primo giro: l’estimator ufficiale",
             f"Il {DATE} le cifre di nolo escono solo da {EST}: scegli il paese, non questo hostname. Nessuna linea inventata.",
             f"La mattina della spedizione apri il sito ufficiale, destinazione {p['dest_zh']}. {p['postal']}."),
            ("w2clinks cerca in inglese",
             "sneakers, hoodie, jacket danno pagine; grafie locali spesso zero. Misurato 6 Oct 2026.",
             "Scrivi la key inglese, o tocca un chip in homepage."),
            ("Magazzino: due cifre nelle copie pubbliche",
             _storage("it"),
             "Pianifica il consolidamento perché il primo pezzo non aspetti fino all’ultimo giorno."),
            ("Gli host sorella restano separati",
             "CA, NL, IT ed ES sono file distinti. Nessun 301 fra loro, nessun 301 verso lovegobuyspreadsheet.eu o lovegobuyguide.com.",
             "Gli hub lovegobuyspreadsheet.eu e lovegobuyguide.com non sono un territorio doganale."),
        ]
        h1, topic, brow = "Cosa abbiamo verificato sulla piattaforma, con data", "cosa abbiamo verificato sulla piattaforma", "Novità"
        lead = "Non è una newsletter aziendale. Check nostri, con data."
    elif loc == "es":
        items = [
            ("Primera ronda: el estimador oficial",
             f"El {DATE} las cifras de flete solo salen de {EST}: elige el país, no este hostname. Ninguna línea inventada.",
             f"La mañana del envío abre el sitio oficial, destino {p['dest_zh']}. {p['postal']}."),
            ("w2clinks busca en inglés",
             "sneakers, hoodie, jacket dan páginas; grafías locales a menudo cero. Medido 6 Oct 2026.",
             "Escribe la key inglesa, o toca un chip en la portada."),
            ("Almacén: dos cifras en las copias públicas",
             _storage("es"),
             "Planifica la consolidación para que la primera pieza no espere hasta el último día."),
            ("Los hosts hermanos siguen separados",
             "CA, NL, IT y ES son archivos distintos. Ningún 301 entre ellos, ningún 301 hacia lovegobuyspreadsheet.eu o lovegobuyguide.com.",
             "Los hubs lovegobuyspreadsheet.eu y lovegobuyguide.com no son un territorio aduanero."),
        ]
        h1, topic, brow = "Qué hemos comprobado en la plataforma, con fecha", "qué hemos comprobado en la plataforma", "Novedades"
        lead = "No es un boletín de empresa. Checks nuestros, con fecha."
    elif loc == "nl":
        items = [
            ("Eerste ronde: de officiële schatter",
             f"Op {DATE} komen vrachtcijfers alleen uit {EST}. Geen verzonnen lijn.",
             f"Open de officiële site de ochtend dat je verzendt, bestemming {p['dest_zh']}. {p['postal']}."),
            ("w2clinks zoekt in het Engels",
             "sneakers, hoodie, jacket geven pagina’s; lokale spellingen vaak nul. Gemeten 6 Oct 2026.",
             "Typ de Engelse key, of tik een chip op de homepage."),
            ("Magazijn: twee getallen in publieke teksten",
             _storage("nl"),
             "Plan het bundelen zo dat het eerste stuk niet tot de laatste dag wacht."),
            ("Zusterhosts blijven apart",
             "CA, NL, IT en ES zijn eigen bestanden. Geen 301 onderling, geen 301 naar lovegobuyspreadsheet.eu of lovegobuyguide.com.",
             "De hubs lovegobuyspreadsheet.eu en lovegobuyguide.com zijn geen douanegebied."),
        ]
        h1, topic, brow = "Wat we op het platform hebben nagekeken, met datum", "wat we op het platform hebben nagekeken", "Nieuws"
        lead = "Dit is geen bedrijfsnieuwsbrief. Eigen checks, met datum."
    else:
        items = [
            ("First round: the official estimator",
             f"On {DATE} freight figures come only from {EST}. This guide does not invent a line or an amount.",
             f"Open the official site the morning you ship. Destination {p['dest_zh']}. {p['postal']}."),
            ("The w2clinks catalogue searches in English",
             "sneakers, hoodie and jacket returned pages; local spellings often returned zero. Measured 6 Oct 2026.",
             "Type the English key, or tap a chip on the homepage."),
            ("Warehouse: two numbers in public copies",
             _storage("en"),
             "Plan consolidation so the first piece does not wait until the last day."),
            ("Sister country hosts stay separate",
             "Canada, the Netherlands, Italy and Spain on LoveGoBuy stay on their own hosts. None of them 301 into lovegobuyspreadsheet.eu or lovegobuyguide.com.",
             "The lovegobuyspreadsheet.eu and lovegobuyguide.com hubs are not a customs territory."),
        ]
        h1, topic, brow = "What we checked on the platform, with a date", "what we checked on the platform", "News"
        lead = "This is not a company newsletter. These are our own checks, with a date."
    ld = itemlist_ld(
        url=f"https://{p['host']}{p['news']}",
        name="LoveGoBuy dest checks",
        items=[(h, f"{x} {y}") for h, x, y in items],
    )
    cards = "".join(
        f'<article class="ncard"><h2>{escape(h)}</h2><p>{escape(x)}</p><p>{escape(y)}</p></article>'
        for h, x, y in items
    )
    body = f"""
<article class="pw">
  <span class="eyebrow" style="color:var(--acd)">{escape(brow)}</span>
  <h1>{escape(h1)}</h1>
  <p class="lead">{escape(lead)}</p>
  <p>{escape(DATE)}.</p>
  {cards}
</article>
"""
    return cms_shell(
        desk, page_title(desk, topic), "Dated checks on LoveGoBuy.",
        f"https://{p['host']}{p['news']}", [ld], body, p["news"],
    )


def build_about(key: str) -> str:
    p = PACKS[key]
    desk = desk_for(key)
    fig_off, *_ = _shots(key)
    loc = p["loc"]
    if loc == "it":
        topic = "chi siamo e come raggiungerci"
        body = f"""
<article class="pw">
  <span class="eyebrow" style="color:var(--acd)">Chi siamo</span>
  <h1>Un sito indipendente su LoveGoBuy, in italiano</h1>
  <p class="lead">LoveGoBuy Spreadsheet non è LoveGoBuy. È una guida editoriale. lovegobuy.com è il sito ufficiale; lovegobuyspreadsheet.eu e lovegobuyguide.com sono hub, non un territorio doganale.</p>
  {fig_off}
  <h2>Come lavoriamo</h2>
  <p>Le cifre di nolo escono solo dall’estimator ufficiale su {escape(EST)}, quindi questa guida non pubblica tariffe inventate. Importazione: <a href="{escape(p["customs_url"])}" rel="noopener">{escape(p["customs"])}</a>.</p>
  <h2>Contatto</h2>
  <p>Ordini: sito ufficiale. Questa guida: <a href="mailto:{escape(MAIL)}">{escape(MAIL)}</a>.</p>
</article>
"""
    elif loc == "es":
        topic = "quiénes somos y cómo contactarnos"
        body = f"""
<article class="pw">
  <span class="eyebrow" style="color:var(--acd)">Sobre nosotros</span>
  <h1>Un sitio independiente sobre LoveGoBuy, en español</h1>
  <p class="lead">LoveGoBuy Spreadsheet no es LoveGoBuy. Es una guía editorial. lovegobuy.com es el sitio oficial; lovegobuyspreadsheet.eu y lovegobuyguide.com son hubs, no un territorio aduanero.</p>
  {fig_off}
  <h2>Cómo trabajamos</h2>
  <p>Las cifras de flete solo salen del estimador oficial en {escape(EST)}, así que esta guía no publica tarifas inventadas. Importación: <a href="{escape(p["customs_url"])}" rel="noopener">{escape(p["customs"])}</a>.</p>
  <h2>Contacto</h2>
  <p>Pedidos: sitio oficial. Esta guía: <a href="mailto:{escape(MAIL)}">{escape(MAIL)}</a>.</p>
</article>
"""
    elif loc == "nl":
        topic = "wie we zijn en hoe je ons bereikt"
        body = f"""
<article class="pw">
  <span class="eyebrow" style="color:var(--acd)">Over ons</span>
  <h1>Een onafhankelijke site over LoveGoBuy, in het Nederlands</h1>
  <p class="lead">LoveGoBuy Spreadsheet is LoveGoBuy niet. Het is een redactionele gids. lovegobuy.com is de officiële site; lovegobuyspreadsheet.eu en lovegobuyguide.com zijn hubs, geen douanegebied.</p>
  {fig_off}
  <h2>Hoe we werken</h2>
  <p>Vrachtcijfers komen alleen uit de officiële schatter op {escape(EST)}, dus deze gids publiceert geen verzonnen tarief. Invoer: <a href="{escape(p["customs_url"])}" rel="noopener">{escape(p["customs"])}</a>.</p>
  <h2>Contact</h2>
  <p>Bestellingen: officiële site. Deze gids: <a href="mailto:{escape(MAIL)}">{escape(MAIL)}</a>.</p>
</article>
"""
    else:
        topic = "who we are and how to reach us"
        body = f"""
<article class="pw">
  <span class="eyebrow" style="color:var(--acd)">About us</span>
  <h1>An independent site about LoveGoBuy, in English</h1>
  <p class="lead">LoveGoBuy Spreadsheet is not LoveGoBuy. It is an editorial guide. lovegobuy.com is the official site; lovegobuyspreadsheet.eu and lovegobuyguide.com are hubs, not a customs territory.</p>
  {fig_off}
  <h2>How we work</h2>
  <p>Shipping figures come only from the official estimator at {escape(EST)}, so this desk publishes no invented rate. Import points to <a href="{escape(p["customs_url"])}" rel="noopener">{escape(p["customs"])}</a>.</p>
  <h2>Contact</h2>
  <p>Orders: official LoveGoBuy chat. This guide: <a href="mailto:{escape(MAIL)}">{escape(MAIL)}</a>.</p>
</article>
"""
    return cms_shell(
        desk, page_title(desk, topic),
        "Independent LoveGoBuy guide: how we check facts.",
        f"https://{p['host']}{p['about']}", [], body, p["about"],
    )


def _inner_pages(key: str) -> dict[str, tuple[str, str, str]]:
    """href, topic, html-body for the CMS guide and shipping pages.

    Legit / coupon / spreadsheet URLs are ranked articles on these hosts, so they are
    wrapped by _wrap_ranked instead of regenerated here.
    """
    p = PACKS[key]
    dest = p["dest_label"]
    loc = p["loc"]
    fig_off, fig_sheet, fig_vol, _fig_zoek, fig_diy = _shots(key)
    est = escape(EST)
    official = escape(OFFICIAL)
    fp = escape(p["postal"])
    dest_zh = escape(p["dest_zh"])
    customs = escape(p["customs"])
    customs_url = escape(p["customs_url"])
    guide = escape(p["guide"])
    ship = escape(p["ship"])
    help_h = escape(p["help"])
    dest_e = escape(dest)

    if loc == "it":
        guide_topic = "come fai il primo ordine dall’Italia"
        guide_body = f"""
<article class="pw">
  <span class="eyebrow" style="color:var(--acd)">Guida</span>
  <h1>Primo ordine LoveGoBuy, dall’Italia</h1>
  <p class="lead">Copi il link, lo incolli nell’agente, controlli la foto di magazzino, consolidi, scegli destinazione {dest_zh}. L’indirizzo è una {fp}.</p>
  {fig_off}
  <h2>1. Apri una scheda su w2clinks</h2>
  <p>Una delle trentatré categorie, foto e link del negozio. È un catalogo, non un file Excel.</p>
  {fig_sheet}
  <h2>2. Incolla sul sito ufficiale</h2>
  <p>Pagamenti e ticket restano su {official}. Questa guida non vede il tuo account. Se la ricerca non legge il link, il sito ufficiale ha un modulo d’ordine manuale.</p>
  {fig_diy}
  <h2>3. Foto, poi consolida, poi spedisci</h2>
  <p>Le cifre di nolo escono solo da {est}: scegli il paese, non questo hostname. {escape(_storage("it"))}</p>
  <h2>Nove stati, tre schermate</h2>
  <p>Prima il prodotto più il trasporto interno fino al magazzino. L’internazionale dopo. «Perché è fermo?» quasi sempre: schermata sbagliata — ordini, poi magazzino, poi pacco.</p>
  <h2>Primo haul: piatto prima</h2>
  <p>T-shirt, shorts, gioielli per il primo giro. Piumini, borse, cappelli per il secondo. Elettronica spesso litio: controlla la linea sul sito ufficiale.</p>
  <p><a class="btn" href="{guide}">Guida</a> <a class="btn btn--ghost" href="{ship}">Piano spedizione</a></p>
</article>
"""
        ship_topic = "spedizione e dogana verso l’Italia"
        ship_body = f"""
<article class="pw">
  <span class="eyebrow" style="color:var(--acd)">Spedizione</span>
  <h1>Spedire in Italia: estimator, volume, dogana</h1>
  <p class="lead">Destinazione {dest_zh}, non EU. L’indirizzo è una {fp}.</p>
  {fig_off}
  <h2>L’estimator ufficiale decide</h2>
  <p>Il {escape(DATE)} le cifre di nolo escono solo da {est}: scegli il paese, non questo hostname. Questa guida non inventa una linea, un transito né un importo. Fonte: <a href="{customs_url}" rel="noopener">{customs}</a>.</p>
  <h2>Bilancia contro volume</h2>
  <p>Molte linee fatturano il massimo tra bilancia e L×W×H (cm) / 8000. Esempio: 40×40×3 cm sono 4800 cm³, divisi per 8000 sono 600 g di volume a 200 g reali. Nessun prezzo SKU in questo HTML.</p>
  {fig_vol}
  <h2>Consolidare non è una guida doganale</h2>
  <p>Più pezzi di magazzino in un cartone possono ridurre le righe di nolo. Cosa dichiari in dogana sta sulla spedizione ufficiale, non in questa pagina.</p>
  <h2>Restricted non è un avviso di dogana</h2>
  <p>Schede senza prezzo o un modulo manuale significano: il link sorgente non è acquistabile tramite l’agente. Tabacco, alcol e farmaci non viaggiano.</p>
  <h2>Foto di magazzino prima della linea</h2>
  <p>Le foto QC arrivano in app quando il pezzo è in magazzino. Angoli extra spesso a pagamento. Reclami più facili finché sta ancora lì. {escape(_storage("it"))}</p>
  <h2>L’indirizzo su questo dest</h2>
  <p>L’indirizzo è una {fp}. Quel formato va sulla spedizione ufficiale, non come trucco in questa pagina.</p>
  <p><a class="btn" href="{est}">Estimator ufficiale LoveGoBuy</a> <a class="btn btn--ghost" href="{help_h}">Aiuto</a></p>
</article>
"""
    elif loc == "es":
        guide_topic = f"cómo haces el primer pedido desde {dest}"
        guide_body = f"""
<article class="pw">
  <span class="eyebrow" style="color:var(--acd)">Guía</span>
  <h1>Primer pedido LoveGoBuy, desde {dest_e}</h1>
  <p class="lead">Copias el enlace, lo pegas en el agente, revisas la foto de almacén, consolidas, eliges destino {dest_zh}. La dirección es una {fp}.</p>
  {fig_off}
  <h2>1. Abre una ficha en w2clinks</h2>
  <p>Una de las treinta y tres categorías, foto y enlace de tienda. Es un catálogo, no un archivo Excel.</p>
  {fig_sheet}
  <h2>2. Pégalo en el sitio oficial</h2>
  <p>Pagos y tickets siguen en {official}. Esta guía no ve tu cuenta. Si la búsqueda no lee el enlace, el sitio oficial tiene un formulario manual.</p>
  {fig_diy}
  <h2>3. Foto, luego consolida, luego envía</h2>
  <p>Las cifras de flete solo salen de {est}: elige el país, no este hostname. {escape(_storage("es"))}</p>
  <h2>Nueve estados, tres pantallas</h2>
  <p>Primero el producto más el tramo interno hasta el almacén. El internacional después. «¿Por qué está parado?» casi siempre: pantalla equivocada — pedidos, luego almacén, luego paquete.</p>
  <h2>Primer haul: plano primero</h2>
  <p>Camisetas, shorts, joyería para la primera ronda. Plumíferos, bolsos, gorras para la segunda. Electrónica a menudo litio: mira la línea en el sitio oficial.</p>
  <p><a class="btn" href="{guide}">Guía</a> <a class="btn btn--ghost" href="{ship}">Plan de envío</a></p>
</article>
"""
        ship_topic = f"envío y aduanas hacia {dest}"
        ship_body = f"""
<article class="pw">
  <span class="eyebrow" style="color:var(--acd)">Envío</span>
  <h1>Enviar a {dest_e}: estimador, volumen, aduanas</h1>
  <p class="lead">Destino {dest_zh}, no EU. La dirección es una {fp}.</p>
  {fig_off}
  <h2>El estimador oficial manda</h2>
  <p>El {escape(DATE)} las cifras de flete solo salen de {est}: elige el país, no este hostname. Esta guía no inventa una línea, un tránsito ni un importe. Fuente: <a href="{customs_url}" rel="noopener">{customs}</a>.</p>
  <h2>Báscula contra volumen</h2>
  <p>Muchas líneas facturan el máximo entre báscula y L×W×H (cm) / 8000. Ejemplo: 40×40×3 cm son 4800 cm³, divididos por 8000 son 600 g de volumen con 200 g reales. Ningún precio SKU en este HTML.</p>
  {fig_vol}
  <h2>Consolidar no es una guía de aduanas</h2>
  <p>Varias piezas de almacén en un cartón pueden recortar líneas internacionales. Lo que declaras en aduanas está en el envío oficial, no en esta página.</p>
  <h2>Restricted no es un aviso de aduanas</h2>
  <p>Fichas sin precio o un formulario manual significan: el enlace de origen no se puede comprar por el agente. Tabaco, alcohol y medicamentos no viajan.</p>
  <h2>Fotos de almacén antes de la línea</h2>
  <p>Las fotos QC llegan a la app cuando la pieza está en almacén. Ángulos extra a menudo de pago. Reclamar es más fácil mientras sigue ahí. {escape(_storage("es"))}</p>
  <h2>La dirección en este dest</h2>
  <p>La dirección es una {fp}. Ese formato va en el envío oficial, no como truco en esta página.</p>
  <p><a class="btn" href="{est}">Estimador oficial LoveGoBuy</a> <a class="btn btn--ghost" href="{help_h}">Ayuda</a></p>
</article>
"""
    elif loc == "nl":
        guide_topic = f"hoe je de eerste bestelling vanuit {dest} plaatst"
        guide_body = f"""
<article class="pw">
  <span class="eyebrow" style="color:var(--acd)">Gids</span>
  <h1>Eerste LoveGoBuy-bestelling, vanuit {dest_e}</h1>
  <p class="lead">Link kopiëren, in de agent plakken, magazijnfoto checken, bundelen, bestemming {dest_zh} kiezen. Het afleveradres is een {fp}.</p>
  {fig_off}
  <h2>1. Open een kaart op w2clinks</h2>
  <p>Eén van de drieëndertig categorieën, foto en shoplink. Dat is de catalogus, geen Excel-bestand.</p>
  {fig_sheet}
  <h2>2. Plak op de officiële site</h2>
  <p>Betaling en tickets blijven op {official}. Deze gids ziet je account niet. Leest de zoekbalk de link niet, dan heeft de officiële site een handmatig formulier.</p>
  {fig_diy}
  <h2>3. Foto, dan bundelen, dan verzenden</h2>
  <p>Vrachtcijfers komen alleen uit {est}: kies het land, niet deze hostnaam. {escape(_storage("nl"))}</p>
  <h2>Negen statussen, drie schermen</h2>
  <p>Eerst product plus binnenlands traject tot het magazijn. Internationaal later. «Waarom staat het stil?» bijna altijd: verkeerd scherm — bestellingen, dan magazijn, dan pakket.</p>
  <h2>Eerste haul: plat eerst</h2>
  <p>T-shirts, shorts, sieraden voor de eerste ronde. Dons, tassen, petten voor de tweede. Elektronica vaak lithium: check de lijn op de officiële site.</p>
  <p><a class="btn" href="{guide}">Gids</a> <a class="btn btn--ghost" href="{ship}">Verzendplan</a></p>
</article>
"""
        ship_topic = f"verzending en douane naar {dest}"
        ship_body = f"""
<article class="pw">
  <span class="eyebrow" style="color:var(--acd)">Verzending</span>
  <h1>Verzenden naar {dest_e}: schatter, volume, douane</h1>
  <p class="lead">Bestemming {dest_zh}, niet EU. Het afleveradres is een {fp}.</p>
  {fig_off}
  <h2>De officiële schatter beslist</h2>
  <p>Op {escape(DATE)} komen vrachtcijfers alleen uit {est}. Deze gids verzint geen lijn, transittijd of bedrag. Bron: <a href="{customs_url}" rel="noopener">{customs}</a>.</p>
  <h2>Weegschaal versus volume</h2>
  <p>Veel lijnen factureren het maximum van weegschaal en L×W×H (cm) / 8000. Voorbeeld: 40×40×3 cm is 4800 cm³, gedeeld door 8000 is 600 g volume bij 200 g echt gewicht. Geen SKU-prijs in deze HTML.</p>
  {fig_vol}
  <h2>Bundelen is geen douane-tutorial</h2>
  <p>Meerdere magazijnstukken in één doos kunnen internationale lijnen schelen. Wat je aan de douane opgeeft, staat op de officiële zending, niet op deze pagina.</p>
  <h2>Restricted is geen douanebericht</h2>
  <p>Kaarten zonder prijs of een handmatig formulier betekenen: de bronlink is via de agent niet te koop. Tabak, alcohol en geneesmiddelen reizen niet.</p>
  <h2>Magazijnfoto’s vóór de lijn</h2>
  <p>QC-foto’s landen in de app zodra het stuk in het magazijn is. Extra hoeken zijn vaak betaald. Reclame is makkelijker zolang het er nog ligt. {escape(_storage("nl"))}</p>
  <h2>Het adres op dit dest</h2>
  <p>Het afleveradres is een {fp}. Dat formaat hoort op de officiële zending, niet als truc op deze pagina.</p>
  <p><a class="btn" href="{est}">Officiële LoveGoBuy-schatter</a> <a class="btn btn--ghost" href="{help_h}">Hulp</a></p>
</article>
"""
    else:
        guide_topic = f"how you place the first order from {dest}"
        guide_body = f"""
<article class="pw">
  <span class="eyebrow" style="color:var(--acd)">Guide</span>
  <h1>First LoveGoBuy order, from {dest_e}</h1>
  <p class="lead">Copy the shop link, paste it into the agent, check the warehouse photo, consolidate, then pick destination {dest_zh}. The delivery address uses a {fp}.</p>
  {fig_off}
  <h2>1. Open a card on w2clinks</h2>
  <p>One of the thirty-three categories, a photo and the shop link. That is the catalogue, not an Excel file.</p>
  {fig_sheet}
  <h2>2. Paste it on the official site</h2>
  <p>Payment and tickets stay on {official}. This desk cannot see your account. If search does not read the link, the official site has a manual order form.</p>
  {fig_diy}
  <h2>3. Photo, then consolidate, then ship</h2>
  <p>Freight figures come only from lovegobuy.com{escape(EST_PATH)} — pick the dest country, not this hostname. {escape(_storage("en"))}</p>
  <h2>Nine statuses, three screens</h2>
  <p>First the product plus domestic freight to the warehouse. International later. “Why is it stuck?” is almost always the wrong screen — orders, then warehouse, then the parcel.</p>
  <h2>First haul: flat first</h2>
  <p>T-shirts, shorts, jewelry for the first round. Down, bags, hats for the second. Electronics often mean lithium: check the line on the official site.</p>
  <p><a class="btn" href="{guide}">Guide</a> <a class="btn btn--ghost" href="{ship}">Shipping plan</a></p>
</article>
"""
        ship_topic = f"shipping and customs to {dest}"
        ship_body = f"""
<article class="pw">
  <span class="eyebrow" style="color:var(--acd)">Shipping</span>
  <h1>Shipping to {dest_e}: estimator, volume, customs</h1>
  <p class="lead">Pick destination {dest_zh} in the official estimator. The delivery address uses a {fp}.</p>
  {fig_off}
  <h2>The official estimator decides</h2>
  <p>On {escape(DATE)} freight figures come only from {est} — pick the dest country, not this hostname. This desk does not invent a line, a transit-day count or a money amount. Import: <a href="{customs_url}" rel="noopener">{customs}</a>.</p>
  <h2>Scale versus volume</h2>
  <p>Many lines bill the greater of scale and L×W×H (cm) / 8000. Example: 40×40×3 cm is 4800 cm³, divided by 8000 is 600 g volume at 200 g real weight. No SKU price in this HTML.</p>
  {fig_vol}
  <h2>Consolidation is not a customs tutorial</h2>
  <p>Several warehouse items in one box can cut the number of international lines. What you declare to customs is on the official shipment, not on this page.</p>
  <h2>Restricted is not a customs notice</h2>
  <p>Cards without a price, or a manual form, mean the source link is not buyable through the agent. Tobacco, alcohol and medicines do not travel.</p>
  <h2>Warehouse photos before you book a line</h2>
  <p>QC photos land in the app once the piece is in the warehouse. Extra angles are often paid. Disputes are easier while it is still there. {escape(_storage("en"))}</p>
  <h2>The address on this dest</h2>
  <p>The delivery address uses a {fp}. That format belongs on the official shipment, not as a trick on this page.</p>
  <p><a class="btn" href="{est}">Official LoveGoBuy estimator</a> <a class="btn btn--ghost" href="{help_h}">Help</a></p>
</article>
"""
    return {
        "guide": (p["guide"], guide_topic, guide_body),
        "ship": (p["ship"], ship_topic, ship_body),
    }


def build_inner(key: str, name: str) -> str:
    p = PACKS[key]
    desk = desk_for(key)
    href, topic, body = _inner_pages(key)[name]
    return cms_shell(
        desk, page_title(desk, topic),
        f"Independent LoveGoBuy {name} for {p['dest_label']}.",
        f"https://{p['host']}{href}", [], body, href,
    )


def _cms_hrefs(key: str) -> set[str]:
    p = PACKS[key]
    return {"/start/", p["help"], p["news"], p["about"], p["catalog"], p["guide"], p["ship"]}


def _wrap_targets(key: str) -> tuple[tuple[str, int], ...]:
    """Ranked inners to wrap; a path that is also a CMS slug is generated instead."""
    cms = _cms_hrefs(key)
    return tuple((href, floor) for href, floor in RANKED.get(key, ()) if href not in cms)


SHEET_EXPLAIN = (
    "not an Excel file",
    "non è un file Excel",
    "no es un archivo Excel",
    "geen Excel-bestand",
)

GUIDE_MARK = {
    "nl": "Eerste LoveGoBuy-bestelling",
    "it": "Primo ordine LoveGoBuy",
    "es": "Primer pedido LoveGoBuy",
    "en": "First LoveGoBuy order",
}
ABOUT_MARK = {
    "nl": "Een onafhankelijke site over LoveGoBuy",
    "it": "Un sito indipendente su LoveGoBuy",
    "es": "Un sitio independiente sobre LoveGoBuy",
    "en": "An independent site about LoveGoBuy",
}


def _ship_mark(p: dict) -> str:
    return {
        "nl": f"Verzenden naar {p['dest_label']}",
        "it": "Spedire in Italia",
        "es": f"Enviar a {p['dest_label']}",
    }.get(p["loc"], "Shipping to")


def _assert_ok(html: str, page: str, key: str) -> None:
    p = PACKS[key]
    desk = desk_for(key)
    if page == "nf":
        if p["not_found_tab"] not in html or MAIL not in html:
            raise SystemExit(f"{key} nf chrome")
        if f"{p['not_found_tab']} | LoveGoBuy Spreadsheet" not in html:
            raise SystemExit(f"{key} nf title")
        if 'href="/start/"' not in html:
            raise SystemExit(f"{key} nf Start")
        return
    skip = {
        "missing #local dest briefing",
        "missing #local",
        "missing #catalog",
        "missing catalogue API",
        f"missing FX_CCY {p['ccy']}",
        "faq count 0",
    }
    err = [e for e in validate_desk(html, _facts(key), page=page) if e not in skip]
    for tok in INVITES:
        if tok in html:
            err.append(f"invite {tok}")
    if re.search(r"58 l[ií]neas", html, re.I) or re.search(r"23[,.]81\s*USD", html, re.I):
        err.append("58-line / 23.81 leak")
    if page != "help" and html.count('class="sg-faq"') >= (8 if page == "home" else 1):
        err.append(f"{page} faq outside Help")
    if page == "home":
        err = [e for e in err if not e.startswith("faq count")]
        if page_title(desk, p["home_topic"]) not in html:
            err.append("home title")
        if p["fingerprint"] not in html:
            err.append("fingerprint")
        if not any(tok in html for tok in SHEET_EXPLAIN):
            err.append("sheet-explain")
        if "cat-30-shoes.png" not in html or f"w2clinks.com/spreadsheet/{SHEET_SLUG}" not in html:
            err.append("W2C cats")
        if html.count('class="cat"') < 33:
            err.append("W2C cat wall < 33")
        if MAIL not in html:
            err.append("footer mail")
        if 'id="local"' in html or "/api/products/" in html:
            err.append("ops dump")
        if 'class="fig"' not in html:
            err.append("photos")
        for sid in ("shots", "states", "restricted"):
            if f'id="{sid}"' not in html:
                err.append(f"missing #{sid}")
        if p["loc"] != "en" and "Official lovegobuy.com, 6 Oct" in html:
            err.append("english fig caption")
        for alien in p["aliens"]:
            if alien in html:
                err.append(f"alien {alien}")
    if page == "help":
        if p["fingerprint"] not in html:
            err.append("help fingerprint")
        if html.count("<h2>") < 5:
            err.append("help groups")
        if html.count('class="sg-faq"') < 12:
            err.append("help faq count")
    if page == "catalog":
        if 'class="eq"' not in html:
            err.append("catalog keys table")
        if "oficial-diy.jpg" not in html:
            err.append("catalog diy shot")
        if html.count('class="fig"') < 3:
            err.append("catalog figs")
    if page == "about" and ABOUT_MARK.get(p["loc"], ABOUT_MARK["en"]) not in html:
        err.append("about mark")
    if page in ("guide", "ship"):
        if "orientdig" in html.lower():
            err.append("orientdig leftover")
        if p["fingerprint"] not in html:
            err.append(f"{page} fingerprint")
        mark = GUIDE_MARK.get(p["loc"], GUIDE_MARK["en"]) if page == "guide" else _ship_mark(p)
        if mark not in html:
            err.append(f"{page} mark {mark!r}")
        for alien in p["aliens"]:
            if alien in html:
                err.append(f"alien {alien}")
    if err:
        raise SystemExit(f"{key}/{page}: {'; '.join(err)}")


def _overlay(key: str) -> Path:
    return OUT / PACKS[key]["host"] / "overlay"


def _copy_asset(src: Path, dst: Path) -> bool:
    if not src.is_file():
        print("WARN missing asset", src)
        return False
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy(src, dst)
    return True


def _copy_hero(dst: Path) -> None:
    jpg, webp = ASSETS / "hero.jpg", ASSETS / "hero.webp"
    if jpg.is_file():
        _copy_asset(jpg, dst)
        return
    if not webp.is_file():
        print("WARN missing asset", jpg)
        return
    dst.parent.mkdir(parents=True, exist_ok=True)
    try:
        from PIL import Image
    except ImportError:
        shutil.copy(webp, dst)
        print("WARN hero.webp copied as hero.jpg without re-encode (no Pillow)")
        return
    with Image.open(webp) as im:
        im.convert("RGB").save(dst, "JPEG", quality=86, optimize=True, progressive=True)


def _copy_assets(dest: Path) -> None:
    img = dest / "img"
    (img / "shots").mkdir(parents=True, exist_ok=True)
    (dest / "assets" / "images").mkdir(parents=True, exist_ok=True)
    (dest / "assets" / "css").mkdir(parents=True, exist_ok=True)
    if not ASSETS.is_dir():
        print("WARN assets dir missing", ASSETS, "- writing HTML/CSS only")
        return
    _copy_asset(ASSETS / LOGO, dest / "assets" / "images" / LOGO)
    _copy_hero(img / "hero.jpg")
    _copy_asset(ASSETS / "favicon.ico", dest / "favicon.ico")
    fav1 = ASSETS / "favicon1.ico"
    _copy_asset(fav1 if fav1.is_file() else ASSETS / "favicon.ico", dest / "favicon1.ico")
    for name in SHOTS:
        _copy_asset(ASSETS / "shots" / name, img / "shots" / name)


def _write_theme() -> Path:
    theme = OUT / "shared" / "themes" / THEME_CSS
    theme.parent.mkdir(parents=True, exist_ok=True)
    theme.write_text(
        "/* LoveGoBuy country dest — official red from lovegobuy.com */\n"
        f":root {{ --primary: {ACC}; --primary-dark: {ACC_DARK}; --primary-soft: {SOFT}; --nav-dark: #0f172a; }}\n",
        encoding="utf-8",
    )
    return theme


def generate(key: str) -> dict[str, Path]:
    p = PACKS[key]
    if p["host"] in SKIP_PUT_HOSTS or p["host"] in TWINS:
        raise SystemExit(f"refusing to generate a dest for hub/twin {p['host']}")
    dest = _overlay(key)
    dest.mkdir(parents=True, exist_ok=True)
    inner_rels = [href.strip("/") for href, _t, _b in _inner_pages(key).values()]
    for rel in ("start", p["help"].strip("/"), p["news"].strip("/"), p["about"].strip("/"), p["catalog"].strip("/"), *inner_rels):
        (dest / rel).mkdir(exist_ok=True)
    _copy_assets(dest)
    css_path = dest / "assets" / "css" / p["desk_css"]
    css_path.write_text(render_css(desk_for(key)), encoding="utf-8")
    _write_theme()
    home = build_home(key)
    pages = {
        "home": (dest / "index.html", home, "home"),
        "start": (dest / "start" / "index.html", home, "home"),
        "help": (dest / p["help"].strip("/").split("/")[0] / "index.html", build_help(key), "help"),
        "news": (dest / p["news"].strip("/").split("/")[0] / "index.html", build_news(key), "news"),
        "about": (dest / p["about"].strip("/").split("/")[0] / "index.html", build_about(key), "about"),
        "catalog": (dest / p["catalog"].strip("/").split("/")[0] / "index.html", build_catalog(key), "catalog"),
        "nf": (dest / "404.html", build_404(desk_for(key)), "nf"),
    }
    for name, (href, _topic, _body) in _inner_pages(key).items():
        pages[name] = (dest / href.strip("/").split("/")[0] / "index.html", build_inner(key, name), name)
    out: dict[str, Path] = {"css": css_path, "logo": dest / "assets" / "images" / LOGO}
    for name, (path, html, page) in pages.items():
        _assert_ok(html, page, key)
        n = len(html.encode("utf-8"))
        if name in ("home", "start") and n < DEST_MIN:
            raise SystemExit(f"{key} {name} too small {n}")
        path.write_text(html, encoding="utf-8")
        print("wrote", path, n)
        out[name] = path
    wraps = ", ".join(h for h, _f in _wrap_targets(key)) or "none"
    print(key, "ranked inners to wrap on PUT:", wraps)
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


def _nginx_ok(client) -> tuple[bool, str]:
    chk = _run(client, "nginx -t")
    low = chk.lower()
    return ("successful" in low or "syntax is ok" in low) and "emerg" not in low, chk


def _reload_nginx(client) -> None:
    ok, chk = _nginx_ok(client)
    print(chk)
    if not ok:
        raise SystemExit("nginx -t failed")
    print(_run(client, "nginx -s reload"))


def _strip_cms_home_301s(client, sftp, key: str) -> None:
    host = PACKS[key]["host"]
    gsc = f"/www/server/panel/vhost/nginx/extension/{host}/gsc-redirects.conf"
    raw = _run(client, f"cat '{gsc}' 2>/dev/null || true")
    if not raw:
        return
    drop = {f"location = /{loc} {{ return 301 https://{host}/; }}" for loc in CMS_PAGE_LOCS}
    keep, stripped = [], 0
    for ln in raw.splitlines(True):
        if ln.strip() in drop:
            stripped += 1
            continue
        keep.append(ln)
    if not stripped:
        print(key, "no CMS-page home 301s")
        return
    stamp = time.strftime("%Y%m%d-%H%M%S")
    _run(client, f"cp -a '{gsc}' '/www/backup/lovegobuy-{key}-gsc-about-{stamp}.conf'")
    Path(f"/tmp/lovegobuy-{key}-gsc.conf").write_text("".join(keep), encoding="utf-8")
    sftp.put(f"/tmp/lovegobuy-{key}-gsc.conf", gsc)
    print(key, "stripped", stripped, "CMS-page home 301s")
    _reload_nginx(client)


def _map_legacy_english_cms(client, sftp, key: str) -> None:
    """301 leftover English CMS slugs onto dest slugs; drop the leftover dirs."""
    p = PACKS[key]
    host = p["host"]
    root = f"/www/wwwroot/{host}"
    wanted: dict[str, str] = {}
    dropped: list[str] = []
    for old, dest in (
        ("about", p["about"]),
        ("who-we-are", p["about"]),
        ("help", p["help"]),
        ("news", p["news"]),
        ("catalog", p["catalog"]),
        ("novedades", p["news"]),
        ("noticias", p["news"]),
        ("novita", p["news"]),
        ("notizie", p["news"]),
    ):
        if dest.strip("/") == old:
            continue
        wanted[f"/{old}"] = dest
        wanted[f"/{old}/"] = dest
        dropped.append(old)
        _run(client, f"rm -rf '{root}/{old}'")
    if not wanted:
        return
    gsc = f"/www/server/panel/vhost/nginx/extension/{host}/gsc-redirects.conf"
    raw = _run(client, f"cat '{gsc}' 2>/dev/null || true")
    raw = re.sub(r"\}(\s*)location\s+=", "}\nlocation =", raw or "")
    if raw and not raw.endswith("\n"):
        raw += "\n"
    seen: set[str] = set()
    out: list[str] = []
    loc_re = re.compile(r"location\s+=\s+(\S+)\s*\{")
    for ln in raw.splitlines(True):
        m = loc_re.search(ln)
        if m and m.group(1) in wanted:
            path = m.group(1)
            if path in seen:
                continue
            prefix = ln[: m.start()] if m.start() else ""
            if prefix.strip() and not prefix.endswith("\n"):
                out.append(prefix.rstrip() + "\n")
            out.append(f"location = {path} {{ return 301 https://{host}{wanted[path]}; }}\n")
            seen.add(path)
            continue
        out.append(ln)
    for path, dest in wanted.items():
        if path not in seen:
            out.append(f"location = {path} {{ return 301 https://{host}{dest}; }}\n")
            seen.add(path)
    new = "".join(out)
    if new == (raw or ""):
        if dropped:
            print(key, "dropped leftover English CMS dirs", dropped)
        return
    stamp = time.strftime("%Y%m%d-%H%M%S")
    _run(client, f"mkdir -p /www/backup '{Path(gsc).parent}'; cp -a '{gsc}' '/www/backup/lovegobuy-{key}-gsc-legacy-{stamp}.conf' 2>/dev/null || true")
    Path(f"/tmp/lovegobuy-{key}-gsc-legacy.conf").write_text(new, encoding="utf-8")
    sftp.put(f"/tmp/lovegobuy-{key}-gsc-legacy.conf", gsc)
    print(key, "legacy CMS 301s", " ".join(f"{a}->{b}" for a, b in wanted.items()))
    _reload_nginx(client)
    if dropped:
        print(key, "dropped leftover English CMS dirs", dropped)


def _map_faq_to_help(client, sftp, key: str) -> None:
    """Rewrite leftover /faq (and invite-code→faq) 301s in every extension conf.

    Exact `location =` in 00-gsc-exact-redirects.conf beats try_files, so appending
    a second /faq into gsc-redirects.conf duplicates the location and breaks nginx -t.
    Also drop 301s that would shadow new CMS slugs (start, help, guide, …).
    """
    p = PACKS[key]
    host = p["host"]
    help_href = p["help"]
    root = f"/www/wwwroot/{host}"
    _run(client, f"rm -rf '{root}/faq'")
    ext = f"/www/server/panel/vhost/nginx/extension/{host}"
    listing = _run(client, f"find '{ext}' -maxdepth 1 -name '*.conf' -print 2>/dev/null || true")
    files = [ln.strip() for ln in listing.splitlines() if ln.strip().endswith(".conf")]
    # lovegobuy-coupons is left out on purpose: origin may 301 it onto the ranked /lovegobuy-coupon/.
    unstick = {h.strip("/") for h in _cms_hrefs(key)}
    faq_src = {
        "/faq", "/faq/",
        "/lovegobuy-invite-code", "/lovegobuy-invite-code/",
    }
    loc_re = re.compile(r"location\s+=\s+(\S+)\s*\{")
    seen_faq: set[str] = set()
    changed = 0
    stamp = time.strftime("%Y%m%d-%H%M%S")
    for remote in files:
        raw = _run(client, f"cat '{remote}' 2>/dev/null || true")
        if not raw:
            continue
        out: list[str] = []
        file_changed = False
        for ln in raw.splitlines(True):
            m = loc_re.search(ln)
            if not m:
                out.append(ln)
                continue
            path = m.group(1)
            slug = path.strip("/")
            if path in faq_src:
                want = f"location = {path} {{ return 301 https://{host}{help_href}; }}\n"
                prefix = ln[: m.start()] if m.start() else ""
                if prefix.strip() and not prefix.endswith("\n"):
                    out.append(prefix.rstrip() + "\n")
                elif prefix and prefix.endswith("\n"):
                    out.append(prefix)
                out.append(want)
                seen_faq.add(path)
                if ln.strip() != want.strip():
                    file_changed = True
                continue
            if slug in unstick:
                file_changed = True
                continue
            out.append(ln)
        if file_changed:
            _run(client, f"cp -a '{remote}' '/www/backup/lovegobuy-{key}-{Path(remote).name}-{stamp}.conf'")
            tmp = Path(f"/tmp/lovegobuy-{key}-{Path(remote).name}")
            tmp.write_text("".join(out), encoding="utf-8")
            sftp.put(str(tmp), remote)
            changed += 1
            print(key, "rewrote redirects", remote)
    missing = [path for path in ("/faq", "/faq/") if path not in seen_faq]
    if missing:
        gsc = f"{ext}/gsc-redirects.conf"
        raw = _run(client, f"cat '{gsc}' 2>/dev/null || true")
        add = "".join(
            f"location = {path} {{ return 301 https://{host}{help_href}; }}\n"
            for path in missing
        )
        _run(client, f"mkdir -p '{ext}'; touch '{gsc}'")
        body = raw or ""
        if body and not body.endswith("\n"):
            body += "\n"
        Path(f"/tmp/lovegobuy-{key}-gsc-faq.conf").write_text(body + add, encoding="utf-8")
        sftp.put(f"/tmp/lovegobuy-{key}-gsc-faq.conf", gsc)
        changed += 1
        print(key, "appended", " ".join(missing), "->", help_href)
    if changed:
        _reload_nginx(client)
    else:
        print(key, "faq/CMS redirects already mapped")


def _harden_catchall(client, sftp, key: str) -> None:
    host = PACKS[key]["host"]
    vhost = f"/www/server/panel/vhost/nginx/{host}.conf"
    with sftp.open(vhost, "r") as fh:
        text = fh.read().decode()
    marker = f'X-Desk "lovegobuy-{key}-independent"'
    stamp = time.strftime("%Y%m%d-%H%M%S")
    changed = False
    dest_root = f"/www/wwwroot/{host}"
    if "error_page 404" not in text:
        inject = (
            f"    error_page 404 /404.html;\n"
            f"    location = /404.html {{\n"
            f"        internal;\n"
            f"        root {dest_root};\n"
            f'        add_header X-Robots-Tag "noindex, nofollow" always;\n'
            f'        add_header Cache-Control "no-store" always;\n'
            f"    }}\n"
        )
        if "error_page 497 https://$host$request_uri;" in text:
            text = text.replace(
                "error_page 497 https://$host$request_uri;",
                "error_page 497 https://$host$request_uri;\n" + inject,
                1,
            )
            changed = True
            print(key, "injected error_page 404")
        else:
            print(key, "WARN no 497 needle for 404 inject")
    if marker not in text:
        old = """    location / {
        try_files $uri $uri/ $uri/index.html =404;
    }
"""
        new = f"""    location / {{
        try_files $uri $uri/ $uri/index.html =404;
        add_header Strict-Transport-Security "max-age=31536000" always;
        add_header Cache-Control "private, no-cache, must-revalidate" always;
        add_header X-Desk "lovegobuy-{key}-independent" always;
    }}
"""
        if old in text:
            text = text.replace(old, new, 1)
            changed = True
            print(key, "hardened HTTPS catch-all")
        else:
            print(key, "catch-all needle not the plain try_files; skip harden")
    if not changed:
        print(key, "vhost already ok")
        return
    _run(client, f"cp -a '{vhost}' '/www/backup/lovegobuy-{key}-nginx-{stamp}.conf'")
    tmp = Path(f"/tmp/lovegobuy-{key}.conf")
    tmp.write_text(text, encoding="utf-8")
    sftp.put(str(tmp), vhost)
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


def _retire_poison(key: str, href: str) -> str:
    p = PACKS[key]
    desk = desk_for(key)
    fp = escape(p["postal"])
    loc = p["loc"]
    if loc == "it":
        topic = "questo articolo è stato sostituito"
        body = f"""
<article class="pw">
  <h1>Questo articolo è stato sostituito</h1>
  <p class="lead">La versione precedente non era di LoveGoBuy. La guida attuale sta su Start. L’indirizzo è una {fp}.</p>
  <p><a class="btn" href="/start/">Start</a> <a class="btn btn--ghost" href="{escape(p['guide'])}">Guida</a></p>
</article>
"""
    elif loc == "es":
        topic = "este artículo fue sustituido"
        body = f"""
<article class="pw">
  <h1>Este artículo fue sustituido</h1>
  <p class="lead">La versión anterior no era de LoveGoBuy. La guía actual está en Start. La dirección es una {fp}.</p>
  <p><a class="btn" href="/start/">Start</a> <a class="btn btn--ghost" href="{escape(p['guide'])}">Guía</a></p>
</article>
"""
    elif loc == "nl":
        topic = "dit artikel is vervangen"
        body = f"""
<article class="pw">
  <h1>Dit artikel is vervangen</h1>
  <p class="lead">De vorige versie hoorde niet bij LoveGoBuy. De huidige gids staat op Start. Het afleveradres is een {fp}.</p>
  <p><a class="btn" href="/start/">Start</a> <a class="btn btn--ghost" href="{escape(p['guide'])}">Gids</a></p>
</article>
"""
    else:
        topic = "this article was replaced"
        body = f"""
<article class="pw">
  <h1>This article was replaced</h1>
  <p class="lead">The previous version was not a LoveGoBuy dest page. The current guide is on Start. The delivery address uses a {fp}.</p>
  <p><a class="btn" href="/start/">Start</a> <a class="btn btn--ghost" href="{escape(p['guide'])}">Guide</a></p>
</article>
"""
    return cms_shell(
        desk, page_title(desk, topic),
        f"Replaced leftover article on {p['host']}.",
        f"https://{p['host']}{href}", [], body, href,
    )


def _ranked_floor(key: str, rel: str) -> int | None:
    for href, floor in _wrap_targets(key):
        if rel == href.lstrip("/") + "index.html":
            return floor
    return None


def _wrap_ranked(client, sftp, bak: str, root: str, key: str) -> None:
    """Wrap ranked inners in dest chrome; retire poisoned unranked leftovers; leave the rest."""
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
    for href, _floor in RANKED.get(key, ()):
        if href in _cms_hrefs(key):
            print(key, "CMS wins over ranked", href)
    seen: set[str] = set()
    for rel in rels:
        if rel in seen:
            continue
        seen.add(rel)
        if rel in skip or any(rel == p.rstrip("/") or rel.startswith(p) for p in WRAP_SKIP_PREFIXES):
            continue
        floor = _ranked_floor(key, rel)
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
        poisoned = any(tok in raw.lower() for tok in WRAP_POISON)
        if poisoned and floor is not None:
            print("WARN ranked inner carries sister-agent leftovers; left untouched for review", rel)
            continue
        if poisoned:
            out = _retire_poison(key, href)
            why = "retire-poison"
            print("retire poison", rel)
        elif floor is None:
            print("skip unranked inner", rel)
            continue
        else:
            out, why = cms_wrap_inner(desk, raw, href)
            if out is None:
                print("inner", rel, why)
                continue
        if why != "retire-poison" and len(out.encode("utf-8")) < (floor or 4000):
            print("WARN skip thin wrap", rel, len(out.encode("utf-8")))
            continue
        rel_dir = str(Path(rel).parent)
        _run(client, f"mkdir -p '{bak}/{rel_dir}'")
        _run(client, f"cp -a '{remote}' '{bak}/{rel}'")
        local_tmp = Path("/tmp") / f"lovegobuy-wrap-{key}-{rel.replace('/', '_')}"
        local_tmp.write_text(out, encoding="utf-8")
        sftp.put(str(local_tmp), remote)
        print("WRAP", rel, "in", len(raw), "out", len(out.encode("utf-8")))
    present = {r for r in seen}
    for href, _floor in _wrap_targets(key):
        if href.lstrip("/") + "index.html" not in present:
            print(key, "ranked inner not present on origin (nothing to wrap)", href)


def _put_if(sftp, local: Path, remote: str) -> None:
    if local.is_file():
        sftp.put(str(local), remote)
        print("PUT", remote, local.stat().st_size)
    else:
        print("WARN skip missing local asset", local)


def put(key: str) -> None:
    p = PACKS[key]
    host = p["host"]
    if host in SKIP_PUT_HOSTS:
        raise SystemExit(f"refusing to PUT hub {host}")
    if host in TWINS:
        raise SystemExit(f"refusing to PUT twin {host}; twins only get a 301")
    files = generate(key)
    client = _connect()
    stamp = time.strftime("%Y%m%d-%H%M%S")
    bak = f"/www/backup/lovegobuy-{key}-cms-{stamp}"
    root = f"/www/wwwroot/{host}"
    overlay = _overlay(key)
    if any(h in root for h in SKIP_PUT_HOSTS) or any(t in root for t in TWINS):
        raise SystemExit(f"refusing hub/twin PUT {root}")
    inner_dirs = [href.strip("/") for href, _t, _b in _inner_pages(key).values()]
    slug_dirs = " ".join(
        f"'{root}/{rel}'"
        for rel in (
            "start",
            p["help"].strip("/"),
            p["news"].strip("/"),
            p["about"].strip("/"),
            p["catalog"].strip("/"),
            *inner_dirs,
            "assets/css",
            "assets/images",
            "img/shots",
        )
    )
    _run(client, f"mkdir -p '{bak}' {slug_dirs}")
    sftp = client.open_sftp()
    _harden_catchall(client, sftp, key)
    _strip_cms_home_301s(client, sftp, key)
    _map_legacy_english_cms(client, sftp, key)
    _map_faq_to_help(client, sftp, key)
    mapping = {
        "home": f"{root}/index.html",
        "start": f"{root}/start/index.html",
        "help": f"{root}{p['help']}index.html",
        "news": f"{root}{p['news']}index.html",
        "about": f"{root}{p['about']}index.html",
        "catalog": f"{root}{p['catalog']}index.html",
        "nf": f"{root}/404.html",
    }
    for name, (href, _t, _b) in _inner_pages(key).items():
        mapping[name] = f"{root}{href}index.html"
    for name, remote in mapping.items():
        local = files[name]
        raw = local.read_text(encoding="utf-8")
        if name in ("home", "start", "help", "guide", "ship") and p["fingerprint"] not in raw:
            raise SystemExit(f"refusing {key} {name} without fingerprint")
        if "orientdig" in raw.lower():
            raise SystemExit(f"refusing {key} {name} with OrientDig leftover")
        for tok in INVITES:
            if tok in raw:
                raise SystemExit(f"refusing {key} {name} with invite {tok}")
        _run(client, f"mkdir -p '{Path(remote).parent}'")
        _run(client, f"cp -a '{remote}' '{bak}/{name}.index.html' 2>/dev/null || true")
        sftp.put(str(local), remote)
        print("PUT", remote, local.stat().st_size)
    theme = _write_theme()
    sftp.put(str(theme), f"{root}/assets/css/{THEME_CSS}")
    sftp.put(str(files["css"]), f"{root}/assets/css/{p['desk_css']}")
    _put_if(sftp, overlay / "assets" / "images" / LOGO, f"{root}/assets/images/{LOGO}")
    _put_if(sftp, overlay / "favicon.ico", f"{root}/favicon.ico")
    _put_if(sftp, overlay / "favicon1.ico", f"{root}/favicon1.ico")
    _put_if(sftp, overlay / "img" / "hero.jpg", f"{root}/img/hero.jpg")
    for src in sorted((overlay / "img" / "shots").glob("*.jpg")):
        sftp.put(str(src), f"{root}/img/shots/{src.name}")
        print("PUT", src.name)
    _wrap_ranked(client, sftp, bak, root, key)
    _run(client, f"chown -R www:www '{root}' 2>/dev/null || true")
    sftp.close()
    print("backup", bak)
    client.close()


def _fetch(url: str, follow: bool = True):
    import ssl
    import urllib.error
    import urllib.request

    https = urllib.request.HTTPSHandler(context=ssl.create_default_context())

    class NR(urllib.request.HTTPRedirectHandler):
        def redirect_request(self, req, fp, code, msg, headers, newurl):
            return None

    req = urllib.request.Request(
        url, headers={"User-Agent": "lovegobuy-cms/1.0", "Cache-Control": "no-cache"},
    )
    opener = urllib.request.build_opener(*([https] if follow else [https, NR()]))
    try:
        with opener.open(req, timeout=25) as resp:
            return resp.status, resp.geturl(), resp.headers.get("Location") or "", resp.read()
    except urllib.error.HTTPError as e:
        return e.code, url, e.headers.get("Location") or "", e.read() if e.fp else b""
    except (urllib.error.URLError, OSError) as e:
        return 0, url, "", str(e).encode()


def _dest_live(target_host: str) -> bool:
    key = next((k for k, p in PACKS.items() if p["host"] == target_host), None)
    if key is None:
        print("WARN twin target is not a dest", target_host)
        return False
    p = PACKS[key]
    code, _, loc, body = _fetch(f"https://{target_host}/", follow=False)
    html = body.decode("utf-8", "replace")
    ok = (
        code == 200
        and p["fingerprint"] in html
        and page_title(desk_for(key), p["home_topic"]) in html
    )
    print("dest live?", target_host, code, loc or "", "ok" if ok else "NOT LIVE")
    return ok


_TWIN_EXACT_RE = re.compile(r"location\s*=\s*(\S+)\s*\{[^{}]*\}")


def _twin_catchall(text: str, target: str) -> tuple[str, str]:
    want = f"location / {{ return 301 https://{target}$request_uri; }}"
    t = re.escape(target)
    if re.search(rf"location\s+/\s*\{{\s*return\s+30[1278]\s+https://{t}\$request_uri;\s*\}}", text):
        return text, "ok"
    new, n = re.subn(rf"location\s+/\s*\{{\s*return\s+30[1278]\s+https?://{t}/?;\s*\}}", want, text, count=1)
    if n:
        return new, "home-only"
    new, n = re.subn(r"location\s+/\s*\{[^{}]*?try_files[^{}]*\}", want, text, count=1)
    if n:
        return new, "try_files"
    return text, "missing"


def _twin_wanted(twin: str, target: str) -> dict[str, str]:
    pdest = next(p for p in PACKS.values() if p["host"] == target)
    wanted: dict[str, str] = {}
    for src, dest in TWIN_EXTRA.get(twin) or []:
        wanted[src] = dest
        if not src.endswith("/"):
            wanted[src + "/"] = dest
    for src, dest in (
        ("/guides/how-to-buy", pdest["guide"]),
        ("/guides/qc-photos", pdest["catalog"]),
        ("/guides/dead-links", pdest["catalog"]),
        ("/guides", pdest["guide"]),
    ):
        wanted.setdefault(src, dest)
        wanted.setdefault(src + "/", dest)
    return wanted


def _fix_twins(client, sftp, targets: set[str] | None = None) -> list[str]:
    """Twin catch-all → `return 301 https://{target}$request_uri;` plus exact TWIN_EXTRA maps.

    Runs only once the target dest is live. Exact `location =` lines beat the `/`
    prefix, so TWIN_EXTRA paths land on their ranked target article; everything else
    keeps its path on the target instead of collapsing to the target home.
    """
    stamp = time.strftime("%Y%m%d-%H%M%S")
    done: list[str] = []
    for twin, target in TWINS.items():
        if targets is not None and target not in targets:
            continue
        if twin in SKIP_PUT_HOSTS or twin in {p["host"] for p in PACKS.values()}:
            raise SystemExit(f"twin {twin} collides with a hub/dest")
        if not _dest_live(target):
            print("WARN skip twin until target is live", twin, "->", target)
            continue
        vhost = f"/www/server/panel/vhost/nginx/{twin}.conf"
        rewrite = f"/www/server/panel/vhost/rewrite/{twin}.conf"
        ext = f"/www/server/panel/vhost/nginx/extension/{twin}"
        gsc = f"{ext}/gsc-redirects.conf"
        if not _run(client, f"cat '{vhost}' 2>/dev/null || true"):
            print("skip missing twin vhost", twin)
            continue
        backups: list[tuple[str, str]] = []

        def write(remote: str, text: str) -> None:
            bak = f"/www/backup/lovegobuy-twin-{twin}-{Path(remote).name}-{stamp}"
            if _run(client, f"test -f '{remote}' && cp -a '{remote}' '{bak}' && echo ok || true") == "ok":
                backups.append((remote, bak))
            else:
                backups.append((remote, ""))
            tmp = Path(f"/tmp/lovegobuy-twin-{twin}-{Path(remote).name}")
            tmp.write_text(text, encoding="utf-8")
            _run(client, f"mkdir -p '{Path(remote).parent}'")
            sftp.put(str(tmp), remote)

        state = "missing"
        for remote in (vhost, rewrite):
            raw = _run(client, f"cat '{remote}' 2>/dev/null || true")
            if not raw:
                continue
            new, state = _twin_catchall(raw, target)
            if state in ("home-only", "try_files"):
                write(remote, new)
                print("twin catch-all", state, "-> $request_uri", twin, Path(remote).name)
            if state != "missing":
                break
        if state == "missing":
            print("WARN twin catch-all needle missing; not touching", twin)
            continue
        if state == "ok":
            print("twin catch-all already $request_uri", twin)

        wanted = _twin_wanted(twin, target)
        listing = _run(client, f"find '{ext}' -maxdepth 1 -name '*.conf' -print 2>/dev/null || true")
        ext_files = sorted(ln.strip() for ln in listing.splitlines() if ln.strip().endswith(".conf"))
        if gsc in ext_files:
            ext_files.remove(gsc)
        ext_files.append(gsc)
        seen: set[str] = set()
        for remote in (vhost, rewrite, *ext_files):
            raw = _run(client, f"cat '{remote}' 2>/dev/null || true")
            if not raw and remote != gsc:
                continue
            text = raw or ""
            if remote.startswith(ext):
                text = text.replace(f"https://{twin}", f"https://{target}")

            def sub(m: re.Match) -> str:
                path = m.group(1)
                if path not in wanted:
                    return m.group(0)
                if path in seen:
                    return ""
                seen.add(path)
                return f"location = {path} {{ return 301 https://{target}{wanted[path]}; }}"

            text = _TWIN_EXACT_RE.sub(sub, text)
            if remote == gsc:
                missing = [path for path in wanted if path not in seen]
                if missing:
                    if text and not text.endswith("\n"):
                        text += "\n"
                    text += "".join(
                        f"location = {path} {{ return 301 https://{target}{wanted[path]}; }}\n"
                        for path in missing
                    )
                    seen.update(missing)
            if text != (raw or ""):
                write(remote, text)
                print("twin exact maps", twin, Path(remote).name)
        ok, chk = _nginx_ok(client)
        if not ok:
            print(chk)
            for remote, bak in backups:
                if bak:
                    _run(client, f"cp -a '{bak}' '{remote}'")
                else:
                    _run(client, f"rm -f '{remote}'")
            raise SystemExit(f"nginx -t failed after {twin} twin patch; restored")
        print(_run(client, "nginx -s reload"))
        done.append(twin)
    return done


def put_many(keys: list[str]) -> None:
    for k in keys:
        put(k)
    _cf_bust([PACKS[k]["host"] for k in keys])
    targets = {PACKS[k]["host"] for k in keys}
    if not any(t in targets for t in TWINS.values()):
        return
    client = _connect()
    sftp = client.open_sftp()
    try:
        done = _fix_twins(client, sftp, targets)
    finally:
        sftp.close()
        client.close()
    if done:
        _cf_bust(done)


def put_twins() -> None:
    client = _connect()
    sftp = client.open_sftp()
    try:
        done = _fix_twins(client, sftp)
    finally:
        sftp.close()
        client.close()
    if done:
        _cf_bust(done)


def live_check(key: str | None = None) -> None:
    keys = [key] if key else list(PACKS)
    fail = 0
    dest_hosts = [PACKS[k]["host"] for k in PACKS]
    for k in keys:
        p = PACKS[k]
        host = p["host"]
        desk = desk_for(k)
        checks = [
            (f"https://{host}/", "home"),
            (f"https://{host}/start/", "start"),
            (f"https://{host}{p['help']}", "help"),
            (f"https://{host}{p['news']}", "news"),
            (f"https://{host}{p['about']}", "about"),
            (f"https://{host}{p['catalog']}", "catalog"),
            (f"https://{host}{p['guide']}", "guide"),
            (f"https://{host}{p['ship']}", "ship"),
        ]
        sisters = [h for h in dest_hosts if h != host]
        for url, kind in checks:
            code, final, loc, body = _fetch(url, follow=False)
            html = body.decode("utf-8", "replace")
            print(k, kind, code, "bytes", len(body), "loc", loc or final)
            if any(h in (loc or "") for h in SKIP_PUT_HOSTS):
                print(" FAIL 301 into hub"); fail += 1
            if any(s in (loc or "") for s in sisters):
                print(" FAIL 301 into sister dest"); fail += 1
            if code != 200:
                print(" FAIL status"); fail += 1
                continue
            if "orientdig" in html.lower():
                print(" FAIL orientdig leftover"); fail += 1
            for tok in INVITES:
                if tok in html:
                    print(" FAIL invite", tok); fail += 1
            if re.search(r"58 l[ií]neas", html, re.I) or re.search(r"23[,.]81\s*USD", html, re.I):
                print(" FAIL 58-line / 23.81"); fail += 1
            if LOGO not in html:
                print(" FAIL logo"); fail += 1
            if f'lang="{p["lang"]}"' not in html:
                print(" FAIL lang"); fail += 1
            if 'href="/start/"' not in html or 'href="/">Start' in html:
                print(" FAIL Start href"); fail += 1
            if kind in ("home", "start", "help", "guide", "ship") and p["fingerprint"] not in html:
                print(" FAIL fingerprint"); fail += 1
            faq_n = html.count('class="sg-faq"')
            if kind == "help":
                if faq_n < 12:
                    print(" FAIL help faq count", faq_n); fail += 1
            elif kind in ("home", "start"):
                if faq_n >= 8:
                    print(" FAIL home faq dump", faq_n); fail += 1
            elif faq_n:
                print(" FAIL faq outside Help", faq_n); fail += 1
            if kind in ("home", "start"):
                if page_title(desk, p["home_topic"]) not in html:
                    print(" FAIL title"); fail += 1
                if p["dest_zh"] not in html:
                    print(" FAIL dest zh"); fail += 1
                if "cat-30-shoes.png" not in html or html.count('class="cat"') < 33:
                    print(" FAIL 33 cats"); fail += 1
                if "/api/products/" in html:
                    print(" FAIL api dump"); fail += 1
                for sid in ("shots", "states", "restricted"):
                    if f'id="{sid}"' not in html:
                        print(" FAIL missing #", sid, sep=""); fail += 1
                if p["loc"] != "en" and "Official lovegobuy.com, 6 Oct" in html:
                    print(" FAIL english fig caption"); fail += 1
                if 'class="lite-hero"' in html:
                    print(" FAIL leftover lite-hero"); fail += 1
                for alien in p["aliens"]:
                    if alien in html:
                        print(" FAIL alien", alien); fail += 1
            if kind == "guide" and GUIDE_MARK.get(p["loc"], GUIDE_MARK["en"]) not in html:
                print(" FAIL guide copy"); fail += 1
            if kind == "ship" and _ship_mark(p) not in html:
                print(" FAIL ship copy"); fail += 1
            if kind == "catalog":
                if html.count('class="cat"') < 30:
                    print(" FAIL catalog wall"); fail += 1
                if 'class="eq"' not in html:
                    print(" FAIL catalog keys table"); fail += 1
                if "oficial-diy.jpg" not in html:
                    print(" FAIL catalog diy"); fail += 1
                if html.count('class="fig"') < 3:
                    print(" FAIL catalog figs"); fail += 1
            if kind == "news" and "ItemList" not in html:
                print(" FAIL news ItemList"); fail += 1
            if kind == "about" and ABOUT_MARK.get(p["loc"], ABOUT_MARK["en"]) not in html:
                print(" FAIL about copy"); fail += 1
            if kind == "help":
                if "FAQPage" not in html:
                    print(" FAIL help FAQPage"); fail += 1
                if html.count("<h2>") < 5:
                    print(" FAIL help groups"); fail += 1
        for href, _floor in _wrap_targets(k):
            code, _, loc, body = _fetch(f"https://{host}{href}", follow=False)
            html = body.decode("utf-8", "replace")
            print(k, "ranked", href, code, loc or "")
            if any(h in (loc or "") for h in SKIP_PUT_HOSTS) or any(s in (loc or "") for s in sisters):
                print(" FAIL ranked 301 into hub/sister"); fail += 1
            elif code == 404:
                print(" WARN ranked inner not present", href)
            elif code == 200:
                if "orientdig" in html.lower():
                    print(" FAIL ranked orientdig leftover"); fail += 1
                if re.search(r"58 l[ií]neas", html, re.I) or re.search(r"23[,.]81\s*USD", html, re.I):
                    print(" FAIL ranked 58-line / 23.81"); fail += 1
                if desk.inner_marker not in html:
                    print(" WARN ranked inner not wrapped in dest chrome", href)
            elif code not in (301, 302, 308):
                print(" FAIL ranked status", code); fail += 1
        code_c, _, loc_c, _ = _fetch(f"https://{host}/lovegobuy-coupons/", follow=False)
        print(k, "coupons", code_c, loc_c)
        if code_c in (301, 302, 308) and "/lovegobuy-coupon" in (loc_c or "") and host in (loc_c or host):
            print(k, "coupons kept ranked article")
        elif any(h in (loc_c or "") for h in SKIP_PUT_HOSTS) or any(s in (loc_c or "") for s in sisters):
            print(" FAIL coupons 301 into hub/sister"); fail += 1
        elif code_c not in (200, 404):
            print(" WARN coupons status", code_c)
        for old, want in (("/about/", p["about"]), ("/help/", p["help"]), ("/faq/", p["help"])):
            if want == old:
                continue
            code_ab, _, loc_ab, _ = _fetch(f"https://{host}{old}", follow=False)
            print(k, "legacy", old, code_ab, loc_ab)
            if code_ab not in (301, 302, 308) or want.rstrip("/") not in (loc_ab or ""):
                print(f" FAIL leftover {old} not 301 to {want}"); fail += 1
        code, _, _, nf = _fetch(f"https://{host}/this-page-does-not-exist-cms/", follow=True)
        nhtml = nf.decode("utf-8", "replace")
        print(k, "404", code)
        if code != 404:
            print(" FAIL 404"); fail += 1
        if f"{p['not_found_tab']} | LoveGoBuy Spreadsheet" not in nhtml:
            print(" FAIL 404 title"); fail += 1
    if key is None:
        for a in dest_hosts:
            code, _, loc, _ = _fetch(f"https://{a}/", follow=False)
            if code in (301, 302, 307, 308) and loc:
                print(" FAIL dest 301", a, "->", loc); fail += 1
            else:
                print("dest indep", a, code)
    for twin, target in TWINS.items():
        if key is not None and PACKS[key]["host"] != target:
            continue
        code, _, loc, _ = _fetch(f"https://{twin}/", follow=False)
        print("twin", twin, code, loc)
        if code not in (301, 302, 308) or target not in (loc or ""):
            print(" FAIL twin 301"); fail += 1
        probes = list(TWIN_DEEP_PROBES.get(twin, ())) + ["/deep-path-check/x/"]
        wanted = _twin_wanted(twin, target)
        for path in probes:
            want = f"https://{target}{wanted.get(path, path)}"
            code_d, _, loc_d, _ = _fetch(f"https://{twin}{path}", follow=False)
            print("  twin deep", path, code_d, loc_d)
            if code_d not in (301, 302, 308):
                print("  FAIL twin deep not a 301", path); fail += 1
            elif (loc_d or "").rstrip("/") == f"https://{target}":
                print("  FAIL twin deep 301s to target home only", path); fail += 1
            elif (loc_d or "") != want:
                print("  FAIL twin deep Location", loc_d, "want", want); fail += 1
    for hub in HUBS:
        code, _, loc, body = _fetch(f"https://{hub}/", follow=False)
        html = body.decode("utf-8", "replace")
        print("hub", hub, code, loc or hub)
        if code != 200:
            print(" FAIL hub status"); fail += 1
        if any(h in (loc or "") for h in dest_hosts):
            print(" FAIL hub collapsed into dest"); fail += 1
        if code == 200 and "not a customs territory" not in html:
            print(" FAIL hub missing 'not a customs territory'"); fail += 1
    if fail:
        raise SystemExit(f"live_check fail {fail}")
    print("live_check ok")


def _cf_bust(hosts: list[str]) -> None:
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
            f"{api}{path}", data=data, method=method,
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
        if host in SKIP_PUT_HOSTS:
            continue
        z = req("GET", f"/zones?name={host}")
        zid = ((z.get("result") or [{}])[0] or {}).get("id")
        if not zid:
            print("CF zone missing", host, z.get("errors"))
            continue
        d = req("PATCH", f"/zones/{zid}/settings/development_mode", {"value": "on"})
        print("CF development_mode", host, d.get("success"))
        p = req("POST", f"/zones/{zid}/purge_cache", {"purge_everything": True})
        print("CF purge", host, p.get("success"), p.get("errors") or "")


def _keys(args: list[str]) -> list[str]:
    if not args:
        return list(PACKS)
    bad = [a for a in args if a not in PACKS]
    if bad:
        raise SystemExit(
            f"unknown dest {bad}; dests are {list(PACKS)}. "
            f"Hubs/twins {sorted(SKIP_PUT_HOSTS | set(TWINS))} are never PUT as dests."
        )
    return [k for k in PACKS if k in args]


if __name__ == "__main__":
    args = sys.argv[1:]
    cmd = args[0] if args else "generate"
    rest = args[1:]
    if cmd == "put":
        put_many(_keys(rest))
    elif cmd == "twins":
        put_twins()
    elif cmd == "live":
        live_check(_keys(rest)[0] if len(rest) == 1 else None)
    elif cmd == "all":
        put_many(_keys(rest))
        live_check()
    elif cmd == "generate":
        for k in _keys(rest):
            generate(k)
    else:
        raise SystemExit(f"unknown command {cmd!r}: generate | put | twins | live | all")
