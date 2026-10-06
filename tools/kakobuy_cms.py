#!/usr/bin/env python3
"""Kakobuy country dests: CA, FI, ES, FR, NL.

Gold IA: hipobuy.es. Gold brand: kakobuy.com (official coral #F04A4F / #D13A3F).
Same-agent country hosts stay independent (no 301). No Origin twins: the plural
kakospreadsheets.* names are off-origin or have no DNS.
Hubs kakobuydocs.com and kakobuytips.com are not overwritten.

Official estimator is https://www.kakobuy.com/tools/estimate.
Warehouse: official Help copies quote both 100 days from in-storage and 180 days;
the desks name both and pick neither. Confirm live Help the morning you ship.
Invite yze69 / KAKOSEP stay off titles and dest homepages.
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
    build_404 as _cms_build_404,
    cats_for,
    fig as cms_fig,
    page_title,
    render_css,
    shell as _cms_shell,
    w2c_sheet,
    wrap_inner as _cms_wrap_inner,
)
from desk_template import dest_local_pack, faq_ld, itemlist_ld, long_faqs, skip_label, validate_desk

# desk_template.skip_label has no Finnish entry; its English fallback is swapped here.
SKIP_LABELS = {"fi": "Siirry sisältöön"}


def _localize_skip(desk: CountryDesk, html: str) -> str:
    label = SKIP_LABELS.get(desk.skip_lang)
    if not label:
        return html
    stock = f'<a class="skip" href="#main">{escape(skip_label(desk.skip_lang))}</a>'
    return html.replace(stock, f'<a class="skip" href="#main">{escape(label)}</a>', 1)


def cms_shell(desk: CountryDesk, *args, **kwargs) -> str:
    return _localize_skip(desk, _cms_shell(desk, *args, **kwargs))


def build_404(desk: CountryDesk) -> str:
    return _localize_skip(desk, _cms_build_404(desk))


def cms_wrap_inner(desk: CountryDesk, html: str, page_href: str):
    out, why = _cms_wrap_inner(desk, html, page_href)
    return (_localize_skip(desk, out) if out is not None else None), why

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "sites"
ASSETS = Path("/tmp/kakobuy-assets")
DATE = "6 Oct 2026"
OFFICIAL = "https://www.kakobuy.com/"
EST = "https://www.kakobuy.com/tools/estimate"
HELP = "https://www.kakobuy.com/"
ACC = "#F04A4F"
ACC_DARK = "#D13A3F"
SOFT = "#FEE2E2"
LOGIN_FG = "#fff"
MAIL = "cnfd85269032661@gmail.com"
HUB = "kakobuydocs.com"
TIPS = "kakobuytips.com"
PHP_HOSTS = ()
PHP_KEYS = ()
SKIP_PUT_HOSTS = {HUB, TIPS}
PHP_OVERLAY = OUT / "kakobuy-shared" / "php" / "overlay"
DEST_MIN = 22000
CSS_V = "20261006k"
INVITES = ("yze69", "KAKOSEP")
LOGO = "kakobuy-logo.png"
SHOTS = ("oficial.jpg", "oficial-diy.jpg", "catalogus.jpg", "catalogus-zoek.jpg", "volume-voorbeeld.jpg")

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

FI_LABELS = {
    **EN_LABELS,
    "SNEAKERS": "Lenkkarit",
    "SLIPPERS": "Tossut",
    "T-SHIRT": "T-paita",
    "POLO": "Pikeepaita",
    "SHIRT": "Kauluspaita",
    "SHORTS": "Shortsit",
    "VEST": "Liivi",
    "LONG SLEEVED": "Pitkähihainen",
    "HOODIE": "Huppari",
    "SWEATER": "Neule",
    "SHAWL": "Huivi",
    "JACKET": "Takki",
    "SHELL JACKET": "Kuoritakki",
    "FLEECE JACKET": "Fleecetakki",
    "DOWN JACKETS": "Untuvatakki",
    "TROUSERS": "Housut",
    "Jersey": "Pelipaita",
    "FEMALE STYLE": "Naisten",
    "Electronics": "Elektroniikka",
    "GLOVES": "Hanskat",
    "BAG": "Laukku",
    "HAT": "Hattu",
    "JEWELRY": "Korut",
    "UNDERWEAR": "Alusvaatteet",
    "BELT": "Vyö",
    "KNEEPAD": "Polvisuojat",
    "SOCKS": "Sukat",
    "HEADGEAR": "Päähine",
    "EARMUFF": "Korvaläpät",
    "SCARF": "Kaulahuivi",
    "GLASSES": "Lasit",
    "WATCH": "Kello",
    "CHILD": "Lapset",
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

FR_LABELS = {
    **EN_LABELS,
    "SNEAKERS": "Baskets",
    "T-SHIRT": "T-shirt",
    "SHIRT": "Chemise",
    "VEST": "Veste sans manches",
    "LONG SLEEVED": "Manches longues",
    "SWEATER": "Pull",
    "SHAWL": "Châle",
    "JACKET": "Veste",
    "SHELL JACKET": "Veste shell",
    "FLEECE JACKET": "Polaire",
    "DOWN JACKETS": "Doudoune",
    "TROUSERS": "Pantalon",
    "FEMALE STYLE": "Femme",
    "Electronics": "Électronique",
    "GLOVES": "Gants",
    "BAG": "Sac",
    "HAT": "Casquette",
    "JEWELRY": "Bijoux",
    "UNDERWEAR": "Sous-vêtements",
    "BELT": "Ceinture",
    "KNEEPAD": "Genouillère",
    "SOCKS": "Chaussettes",
    "HEADGEAR": "Couvre-chef",
    "EARMUFF": "Cache-oreilles",
    "SCARF": "Écharpe",
    "GLASSES": "Lunettes",
    "WATCH": "Montre",
    "CHILD": "Enfants",
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

CAT_NOTES_FI = {
    "SNEAKERS": "Tarkista pohja ja lesti QC-kuvista ennen kuin varaat kansainvälisen linjan.",
    "SLIPPERS": "Kevyet ja litteät. Täyttävät laatikkoa nostamatta laskutettavaa painoa paljon.",
    "T-SHIRT": "Aasialaiset mitoitukset ovat usein kapeampia. Mittaa rinnanympärys senteissä.",
    "POLO": "Katso kaulus ja pikeekudos QC-kuvasta. Ne poikkeavat katalogikuvasta useimmin.",
    "SHIRT": "Hihan pituus ja olkasauma mittanauhakuvasta, ei kirjainkoosta.",
    "SHORTS": "Kevyet ja litteät: helpoin tapa täyttää paketti ilman että paino räjähtää.",
    "VEST": "Liivit ovat paksumpia kuin painavat. Laske tilavuus ennen kuin lisäät takin.",
    "LONG SLEEVED": "Hihan pituus ja resori QC-kuvasta. Aasialaiset pituudet ovat usein lyhyempiä.",
    "HOODIE": "Painava tilavuuteensa nähden. Yksi huppari voi ratkaista koko laatikon painoluokan.",
    "SWEATER": "Grammapaino ja kutistuminen. Mittaa rinta, älä luota pelkkään lappuun.",
    "SHAWL": "Kevyt mutta tilaa vievä, jos sitä ei pakata litteäksi. Pyydä litteä pakkaus.",
    "JACKET": "Untuvatakit vievät valtavasti tilaa. Tilavuuspaino voittaa vaa’an lähes aina.",
    "SHELL JACKET": "Katso saumat ja vetoketju QC-kuvasta läheltä. Pinnoitteen repeämä näkyy vain lähikuvassa.",
    "FLEECE JACKET": "Kevyt vaa’alla, paksu tilavuudeltaan. Laske uudelleen kuten untuvassa.",
    "DOWN JACKETS": "Tilavuus voittaa. Yksi untuvatakki voi yksin pakottaa kalliimpaan luokkaan.",
    "TROUSERS": "Pyydä kuvat vyötärön korkeudesta ja sisälahkeesta. W/L ei aina vastaa senttejä.",
    "Jersey": "Tarkista numero, merkit ja kausi kuvista: ne menevät useimmin pieleen.",
    "FEMALE STYLE": "Istuvuus on harvoin unisex. Mittaa rinta ja pituus, älä oleta eurooppalaista kokoa.",
    "Electronics": "Usein litiumia. Moni lentolinja ei ota niitä: tarkista virallinen sivusto ennen tilausta.",
    "GLOVES": "Pyydä kuva parista. Yksi hanska katalogikuvassa ei kerro toisesta mitään.",
    "BAG": "Täyttää laatikon melkein yksin. Laske tilavuus ennen kuin lisäät vaatteita.",
    "HAT": "Litistyy ja vie tilaa. Pyydä täyte, muuten lippa saapuu taittuneena.",
    "JEWELRY": "Pieni ja halpa lähettää. Hyvä tapa täydentää lähes täysi laatikko.",
    "UNDERWEAR": "Vähemmän kortteja kuin muissa. Jos mitään ei löydy, hae merkillä eikä sanalla.",
    "BELT": "Litteä ja kevyt. Lisätään helposti muuttamatta painoluokkaa.",
    "KNEEPAD": "Pari QC-kuvaan. Yksi suoja katalogikuvassa ei ole pari.",
    "SOCKS": "Kevyt täyte. Tarkista pari ja kokomerkintä kuvasta.",
    "HEADGEAR": "Kysy, miten se pakataan. Lierit taittuvat tiukassa laatikossa.",
    "EARMUFF": "Kevyet, mutta kaari tarvitsee tilaa. Älä litistä hupparin alle.",
    "SCARF": "Pyydä litteä pakkaus, muuten se saapuu tilaa vievänä myttynä.",
    "GLASSES": "Pyydä kova kotelo varastokuvaan ennen kuin varaat linjan.",
    "WATCH": "Pieni ja halpa lähettää. Varmista lukko QC-kuvasta.",
    "CHILD": "Aasialaiset lastenkoot ovat pienempiä. Mittaa, älä arvaa lapun iästä.",
}

CAT_NOTES_ES = {k: v for k, v in CAT_NOTES_EN.items()}
CAT_NOTES_ES.update({
    "SNEAKERS": "Suela y horma en las fotos QC antes de reservar el internacional.",
    "T-SHIRT": "Los cortes asiáticos suelen ser más estrechos. Mide el pecho en centímetros.",
    "HOODIE": "Pesada para su volumen. Una sudadera puede fijar la franja de peso de toda la caja.",
    "Electronics": "A menudo litio. Muchas líneas aéreas las rechazan: mira el sitio oficial antes.",
    "BAG": "Llena una caja casi sola. Cuenta el volumen antes de añadir ropa.",
})
CAT_NOTES_FR = {k: v for k, v in CAT_NOTES_EN.items()}
CAT_NOTES_FR.update({
    "SNEAKERS": "Semelle et forme sur les photos QC avant de réserver l’international.",
    "T-SHIRT": "Les coupes asiatiques sont souvent plus étroites. Mesure le tour de poitrine.",
    "HOODIE": "Lourd pour son volume. Un hoodie peut fixer la tranche de poids de toute la boîte.",
    "Electronics": "Souvent du lithium. Beaucoup de lignes aériennes refusent : vérifier le site officiel.",
    "BAG": "Remplit presque une boîte à elle seule. Compter le volume avant d’ajouter des vêtements.",
})
CAT_NOTES_NL = {k: v for k, v in CAT_NOTES_EN.items()}
CAT_NOTES_NL.update({
    "SNEAKERS": "Zool en leest op de QC-foto’s voor je internationaal boekt.",
    "T-SHIRT": "Aziatische snits lopen vaak smaller. Meet de borst in centimeters.",
    "HOODIE": "Zwaar voor het volume. Eén hoodie kan de gewichtsklasse van de hele doos zetten.",
    "Electronics": "Vaak lithium. Veel luchtlijnen weigeren: check de officiële site eerst.",
    "BAG": "Vult bijna in z’n eentje een doos. Tel het volume voor je kleding toevoegt.",
})

RANKED = (
    ("/how-to-use-kakobuy/", 4000),
    ("/is-kakobuy-legit/", 8000),
    ("/kakobuy-spreadsheet/", 8000),
    ("/kakobuy-coupons/", 8000),
    ("/kakobuy-coupon/", 8000),
    ("/best-kakobuy-spreadsheet/", 8000),
    ("/kakobuy-qc/", 4000),
    ("/kakobuy-shipping-to-canada/", 8000),
    ("/kakobuy-canada/", 8000),
    ("/kakobuy-toimitus/", 8000),
    ("/kakobuy-kokemuksia/", 8000),
    ("/kakobuy-suomi/", 8000),
    ("/envio-kakobuy-espana/", 8000),
    ("/kakobuy-opiniones/", 8000),
    ("/es-kakobuy-confiable/", 8000),
    ("/livraison-kakobuy/", 8000),
    ("/kakobuy-france/", 8000),
    ("/avis-kakobuy/", 8000),
    ("/kakobuy-verzending/", 8000),
    ("/kakobuy-ervaringen/", 8000),
)

TWINS = {}

TWIN_EXTRA = {}

CMS_PAGE_LOCS = (
    "about", "about/", "who-we-are", "who-we-are/", "help", "help/", "news", "news/", "catalog", "catalog/",
    "start", "start/",
    "ohje", "ohje/", "katalogi", "katalogi/", "uutiset", "uutiset/", "meista", "meista/",
    "ayuda", "ayuda/", "catalogo", "catalogo/", "noticias", "noticias/", "novedades", "novedades/",
    "sobre-nosotros", "sobre-nosotros/",
    "aide", "aide/", "catalogue", "catalogue/", "actualites", "actualites/", "a-propos", "a-propos/",
    "hulp", "hulp/", "catalogus", "catalogus/", "nieuws", "nieuws/", "over-ons", "over-ons/",
)

WRAP_SKIP_PREFIXES = (
    "help/", "news/", "about/", "who-we-are/", "catalog/", "start/",
    "ohje/", "katalogi/", "uutiset/", "meista/",
    "ayuda/", "novedades/", "sobre-nosotros/", "catalogo/",
    "aide/", "catalogue/", "actualites/", "a-propos/",
    "hulp/", "catalogus/", "nieuws/", "over-ons/",
    "api/", "assets/", "img/",
    "how-to-use-kakobuy/", "kakobuy-shipping/", "is-kakobuy-legit/",
    "kakobuy-coupons/", "kakobuy-spreadsheet/",
    "faq/", "guide/",
)
WRAP_POISON = ("orientdig", "orient dig", "1yi9", "cssb.uy", "1qodrw", "bbd5off", "cruisezhang")

EXTRA_CSS = """
:root{--primary-soft:#fee2e2;--login-fg:#fff}
.hero .eyebrow{color:#fecaca}
.sbox button{color:#fff}
"""

STORAGE = {
    "en": (
        "Official Kakobuy Help copies quote both 100 days from in-storage and 180 days. "
        f"This desk does not pick a number: confirm live Help the morning you ship ({DATE})."
    ),
    "fi": (
        "Kakobuyn virallisissa ohjeissa mainitaan sekä 100 päivää varastoon kirjaamisesta että 180 päivää. "
        f"Tämä desk ei valitse lukua: tarkista virallinen ohje lähetysaamuna ({DATE})."
    ),
    "es": (
        "Las copias oficiales de la Ayuda de Kakobuy citan tanto 100 días desde la entrada en almacén como 180 días. "
        f"Esta guía no elige una cifra: confirma la Ayuda en vivo la mañana del envío ({DATE})."
    ),
    "fr": (
        "Les pages d’aide officielles de Kakobuy citent à la fois 100 jours depuis l’entrée en entrepôt et 180 jours. "
        f"Ce guide ne choisit pas de chiffre : vérifie l’aide en direct le matin de l’envoi ({DATE})."
    ),
    "nl": (
        "Officiële Kakobuy-hulpteksten noemen zowel 100 dagen vanaf inslag als 180 dagen. "
        f"Deze gids kiest geen getal: check de live Help op de ochtend dat je verzendt ({DATE})."
    ),
}


def _storage(loc: str) -> str:
    return STORAGE.get(loc, STORAGE["en"])


def _en_pack(host, dest, dest_label, dest_zh, lang, ccy, topic, hero, lead, postal, customs, customs_url, aliens, css, css_id):
    return {
        "host": host,
        "dest": dest,
        "dest_label": dest_label,
        "dest_zh": dest_zh,
        "lang": lang,
        "loc": "en",
        "in_language": "in English",
        "ccy": ccy,
        "home_topic": topic,
        "hero_h1": hero,
        "eyebrow": "Independent guide, in English",
        "lead": lead,
        "fingerprint": dest_local_pack(dest)["fingerprint"],
        "customs": customs,
        "customs_url": customs_url,
        "postal": postal,
        "catalog": "/catalog/",
        "help": "/help/",
        "news": "/news/",
        "about": "/about/",
        "guide": "/how-to-use-kakobuy/",
        "ship": "/kakobuy-shipping/",
        "nav": [
            ("/start/", "Start"),
            ("/how-to-use-kakobuy/", "Guide"),
            ("/catalog/", "Catalog"),
            ("/kakobuy-shipping/", "Shipping"),
            ("/help/", "Help"),
            ("/news/", "News"),
        ],
        "footer_sections": [
            ("/how-to-use-kakobuy/", "Kakobuy guide"),
            ("/catalog/", "The spreadsheet and the categories"),
            ("/kakobuy-shipping/", "Shipping and customs"),
            ("/help/", "Help and questions"),
            ("/news/", "News"),
            ("/about/", "About us"),
        ],
        "aliens": aliens,
        "not_found_tab": "Page not found",
        "login": "Log in to Kakobuy",
        "menu": "Open menu",
        "home_cta": "Back to the homepage",
        "skip": "en",
        "desk_css": css,
        "css_id": css_id,
    }


PACKS = {
    "ca": _en_pack(
        "kakospreadsheet.ca", "CA", "Canada", "Canada — 加拿大", "en-CA", "CAD",
        "buy in China from Canada, safely",
        "Kakobuy Spreadsheet: the guide to buying in China from Canada",
        "How you paste a product link into the agent, how the w2clinks catalogue works, how a parcel travels to Canada, and what you check before CBSA.",
        "Canadian postal code (form A1A 1A1)", "CBSA", "https://www.cbsa-asfc.gc.ca/",
        ("Packstation", "Poste Italiane", "Northern Ireland is often another", "00100 Helsinki"),
        "kakobuy-ca-desk.css", "kakobuy-ca",
    ),
    "fi": {
        "host": "kakobuy.fi",
        "dest": "FI",
        "dest_label": "Suomi",
        "dest_zh": "Finland — 芬兰",
        "lang": "fi-FI",
        "loc": "fi",
        "in_language": "suomeksi",
        "ccy": "EUR",
        "home_topic": "osta Kiinasta Suomeen turvallisesti",
        "hero_h1": "Kakobuy Spreadsheet: opas Kiinasta ostamiseen Suomesta",
        "eyebrow": "Riippumaton opas, suomeksi",
        "lead": "Miten liität tuotelinkin agenttiin, miten w2clinks-katalogi toimii, miten paketti kulkee Suomeen ja mitä tarkistat ennen Tullia.",
        "fingerprint": dest_local_pack("FI")["fingerprint"],
        "customs": "Tulli",
        "customs_url": "https://tulli.fi/",
        "postal": "suomalainen postinumero (esim. 00100 Helsinki)",
        "catalog": "/katalogi/",
        "help": "/ohje/",
        "news": "/uutiset/",
        "about": "/meista/",
        "guide": "/how-to-use-kakobuy/",
        "ship": "/kakobuy-shipping/",
        "nav": [
            ("/start/", "Start"),
            ("/how-to-use-kakobuy/", "Opas"),
            ("/katalogi/", "Katalogi"),
            ("/kakobuy-shipping/", "Toimitus"),
            ("/ohje/", "Ohje"),
            ("/uutiset/", "Uutiset"),
        ],
        "footer_sections": [
            ("/how-to-use-kakobuy/", "Kakobuy-opas"),
            ("/katalogi/", "Spreadsheet ja kategoriat"),
            ("/kakobuy-shipping/", "Toimitus ja tulli"),
            ("/ohje/", "Ohje ja kysymykset"),
            ("/uutiset/", "Uutiset"),
            ("/meista/", "Meistä"),
        ],
        "aliens": ("Packstation", "form A1A 1A1", "Poste Italiane", "pas un code postal belge"),
        "not_found_tab": "Sivua ei löytynyt",
        "login": "Kirjaudu Kakobuyhin",
        "menu": "Avaa valikko",
        "home_cta": "Takaisin etusivulle",
        "skip": "fi",
        "desk_css": "kakobuy-fi-desk.css",
        "css_id": "kakobuy-fi",
        "lab_not": "ei EU eikä SE",
    },
    "es": {
        "host": "kakospreadsheet.es",
        "dest": "ES",
        "dest_label": "España",
        "dest_zh": "Spain — 西班牙",
        "lang": "es-ES",
        "loc": "es",
        "in_language": "en español",
        "ccy": "EUR",
        "home_topic": "comprar en China desde España, con seguridad",
        "hero_h1": "Kakobuy Spreadsheet: la guía para comprar en China desde España",
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
        "guide": "/how-to-use-kakobuy/",
        "ship": "/kakobuy-shipping/",
        "nav": [
            ("/start/", "Start"),
            ("/how-to-use-kakobuy/", "Guía"),
            ("/catalogo/", "Catálogo"),
            ("/kakobuy-shipping/", "Envío"),
            ("/ayuda/", "Ayuda"),
            ("/novedades/", "Novedades"),
        ],
        "footer_sections": [
            ("/how-to-use-kakobuy/", "Guía Kakobuy"),
            ("/catalogo/", "Spreadsheet y categorías"),
            ("/kakobuy-shipping/", "Envío y aduanas"),
            ("/ayuda/", "Ayuda y preguntas"),
            ("/novedades/", "Novedades"),
            ("/sobre-nosotros/", "Sobre nosotros"),
        ],
        "aliens": ("Packstation", "00100 Helsinki", "pas un code postal belge", "Poste Italiane"),
        "not_found_tab": "Página no encontrada",
        "login": "Entrar en Kakobuy",
        "menu": "Abrir menú",
        "home_cta": "Volver al inicio",
        "skip": "es",
        "desk_css": "kakobuy-es-desk.css",
        "css_id": "kakobuy-es",
    },
    "fr": {
        "host": "kakospreadsheet.fr",
        "dest": "FR",
        "dest_label": "la France",
        "dest_zh": "France — 法国",
        "lang": "fr-FR",
        "loc": "fr",
        "in_language": "en français",
        "ccy": "EUR",
        "home_topic": "acheter en Chine depuis la France, en sécurité",
        "hero_h1": "Kakobuy Spreadsheet : le guide pour acheter en Chine depuis la France",
        "eyebrow": "Guide indépendant, en français",
        "lead": "Comment tu colles un lien produit dans l’agent, comment le catalogue w2clinks fonctionne, comment un colis voyage vers la France, et ce que tu vérifies avant la douane.",
        "fingerprint": dest_local_pack("FR")["fingerprint"],
        "customs": "douane.gouv.fr",
        "customs_url": "https://www.douane.gouv.fr/",
        "postal": "rue française, code postal à cinq chiffres, pas un code postal belge",
        "catalog": "/catalogue/",
        "help": "/aide/",
        "news": "/actualites/",
        "about": "/a-propos/",
        "guide": "/how-to-use-kakobuy/",
        "ship": "/kakobuy-shipping/",
        "nav": [
            ("/start/", "Start"),
            ("/how-to-use-kakobuy/", "Guide"),
            ("/catalogue/", "Catalogue"),
            ("/kakobuy-shipping/", "Livraison"),
            ("/aide/", "Aide"),
            ("/actualites/", "Actus"),
        ],
        "footer_sections": [
            ("/how-to-use-kakobuy/", "Guide Kakobuy"),
            ("/catalogue/", "Spreadsheet et catégories"),
            ("/kakobuy-shipping/", "Livraison et douane"),
            ("/aide/", "Aide et questions"),
            ("/actualites/", "Actus"),
            ("/a-propos/", "À propos"),
        ],
        "aliens": ("Packstation", "00100 Helsinki", "Poste Italiane", "form A1A 1A1"),
        "not_found_tab": "Page introuvable",
        "login": "Se connecter à Kakobuy",
        "menu": "Ouvrir le menu",
        "home_cta": "Retour à l’accueil",
        "skip": "fr",
        "desk_css": "kakobuy-fr-desk.css",
        "css_id": "kakobuy-fr",
    },
    "nl": {
        "host": "kakospreadsheet.nl",
        "dest": "NL",
        "dest_label": "Nederland",
        "dest_zh": "Netherlands — 荷兰",
        "lang": "nl-NL",
        "loc": "nl",
        "in_language": "in het Nederlands",
        "ccy": "EUR",
        "home_topic": "kopen in China vanaf Nederland, veilig",
        "hero_h1": "Kakobuy Spreadsheet: de gids om in China te kopen vanuit Nederland",
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
        "guide": "/how-to-use-kakobuy/",
        "ship": "/kakobuy-shipping/",
        "nav": [
            ("/start/", "Start"),
            ("/how-to-use-kakobuy/", "Handleiding"),
            ("/catalogus/", "Catalogus"),
            ("/kakobuy-shipping/", "Verzending"),
            ("/hulp/", "Hulp"),
            ("/nieuws/", "Nieuws"),
        ],
        "footer_sections": [
            ("/how-to-use-kakobuy/", "Kakobuy-handleiding"),
            ("/catalogus/", "Spreadsheet en categorieën"),
            ("/kakobuy-shipping/", "Verzending en douane"),
            ("/hulp/", "Hulp en vragen"),
            ("/nieuws/", "Nieuws"),
            ("/over-ons/", "Over ons"),
        ],
        "aliens": ("Packstation", "00100 Helsinki", "Poste Italiane", "form A1A 1A1"),
        "not_found_tab": "Pagina niet gevonden",
        "login": "Inloggen bij Kakobuy",
        "menu": "Menu openen",
        "home_cta": "Terug naar de homepage",
        "skip": "nl",
        "desk_css": "kakobuy-nl-desk.css",
        "css_id": "kakobuy-nl",
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
    if loc == "fi":
        intro = (
            "Riippumaton suomenkielinen opas Kakobuysta ja siitä, miten käytät "
            "w2clinks-katalogia, kun ostat Kiinasta Suomeen."
        )
        independence = (
            "Kakobuy Spreadsheet on riippumaton tietosivusto. Emme ole Kakobuy, emme käsittele "
            "tilauksia, emme peri rahtia emmekä näe tiliäsi. Tilaus, maksu ja reklamaatio "
            "kulkevat virallisen sivuston kautta."
        )
        copyright = "&copy; 2026 Kakobuy Spreadsheet. Suomenkielinen teksti, luettu ennen julkaisua."
        sections_h, official_h, independence_h, nav_aria = (
            "Osiot", "Viralliset linkit", "Riippumattomuusilmoitus.", "Päävalikko",
        )
        nf_h1, nf_lead = "Tätä sivua ei ole", "Linkki voi olla vanha. Nämä osiot ovat olemassa:"
        official_links = [
            (_off(p["host"]), "Kakobuy (virallinen sivusto)"),
            (_off(p["host"], "/tools/estimate"), f"Rahtiarvioija (virallinen, {DATE})"),
        ]
    elif loc == "es":
        intro = (
            "Guía independiente en español sobre Kakobuy y sobre cómo usas el catálogo "
            f"w2clinks para comprar en China desde {p['dest_label']}."
        )
        independence = (
            "Kakobuy Spreadsheet es un sitio informativo independiente. No somos Kakobuy, "
            "no tramitamos pedidos, no cobramos el envío y no vemos tu cuenta. "
            "Cada pedido, pago y reclamación pasa por el sitio oficial."
        )
        copyright = "&copy; 2026 Kakobuy Spreadsheet. Texto en español, releído antes de publicar."
        sections_h, official_h, independence_h, nav_aria = (
            "Secciones", "Enlaces oficiales", "Aviso de independencia.", "Menú principal",
        )
        nf_h1, nf_lead = "Esta página no existe", "El enlace quizá sea antiguo. Estas secciones sí existen:"
        official_links = [
            (_off(p["host"]), "Kakobuy (sitio oficial)"),
            (_off(p["host"], "/tools/estimate"), f"Estimador oficial ({DATE})"),
        ]
    elif loc == "fr":
        intro = (
            "Guide indépendant en français sur Kakobuy et sur la façon d’utiliser le catalogue "
            f"w2clinks pour acheter en Chine depuis {p['dest_label']}."
        )
        independence = (
            "Kakobuy Spreadsheet est un site d’information indépendant. Nous ne sommes pas Kakobuy, "
            "nous ne traitons pas les commandes, nous n’encaissons pas le port et nous ne voyons "
            "pas ton compte. Chaque commande, paiement et réclamation passe par le site officiel."
        )
        copyright = "&copy; 2026 Kakobuy Spreadsheet. Texte français, relu avant publication."
        sections_h, official_h, independence_h, nav_aria = (
            "Rubriques", "Liens officiels", "Mention d’indépendance.", "Menu principal",
        )
        nf_h1, nf_lead = "Cette page n’existe pas", "Le lien est peut-être ancien. Voici les rubriques qui existent :"
        official_links = [
            (_off(p["host"]), "Kakobuy (site officiel)"),
            (_off(p["host"], "/tools/estimate"), f"Estimateur officiel ({DATE})"),
        ]
    elif loc == "nl":
        intro = (
            "Onafhankelijke Nederlandstalige gids over Kakobuy en hoe je de w2clinks-catalogus "
            f"gebruikt om vanuit {p['dest_label']} in China te kopen."
        )
        independence = (
            "Kakobuy Spreadsheet is een onafhankelijke infosite. Wij zijn Kakobuy niet, "
            "we verwerken geen bestellingen, we innen geen porto en we zien je account niet. "
            "Elke bestelling, betaling en klacht loopt via de officiële site."
        )
        copyright = "&copy; 2026 Kakobuy Spreadsheet. Nederlandse tekst, nagelezen voor publicatie."
        sections_h, official_h, independence_h, nav_aria = (
            "Onderdelen", "Officiële links", "Onafhankelijkheidsnotitie.", "Hoofdmenu",
        )
        nf_h1, nf_lead = "Deze pagina bestaat niet", "De link is misschien oud. Dit zijn de onderdelen die wel bestaan:"
        official_links = [
            (_off(p["host"]), "Kakobuy (officiële site)"),
            (_off(p["host"], "/tools/estimate"), f"Officiële schatter ({DATE})"),
        ]
    else:
        intro = (
            f"Independent English-language guide to Kakobuy and to how you use the w2clinks "
            f"catalogue to buy in China from {p['dest_label']}."
        )
        independence = (
            "Kakobuy Spreadsheet is an independent information site. We are not Kakobuy, "
            "we do not process orders, we do not collect shipping fees and we cannot see "
            "your account. Every order, payment and claim runs through the official site."
        )
        copyright = "&copy; 2026 Kakobuy Spreadsheet. English copy, edited and checked by people before publication."
        sections_h, official_h, independence_h, nav_aria = (
            "Sections", "Official links", "Independence notice.", "Main menu",
        )
        nf_h1, nf_lead = "This page does not exist", "The link may be old. These are the sections that do exist:"
        official_links = [
            (_off(p["host"]), "Kakobuy (official site)"),
            (_off(p["host"], "/tools/estimate"), f"Official estimator ({DATE})"),
        ]
    return CountryDesk(
        host=p["host"],
        agent="Kakobuy",
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
        theme_css="kakobuy-theme.css",
        desk_css=p["desk_css"],
        inner_marker=inner,
        register_path="/",
        sheet_slug="kakobuy",
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
        "agent": "Kakobuy",
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
        "keep": [
            ("/kakobuy-shipping/", "Shipping"),
            ("/is-kakobuy-legit/", "Review"),
            ("/kakobuy-spreadsheet/", "Spreadsheet"),
            ("/how-to-use-kakobuy/", "Guide"),
        ],
        "codes_off_title": list(INVITES),
        "strict_html_codes": True,
    }


def _fi_long_faqs(facts: dict) -> list[tuple[str, str]]:
    """Fifteen Finnish Help FAQs in the same order as desk_template.long_faqs."""
    host, store = facts["host"], facts["storage"]
    pack = dest_local_pack("FI")
    pairs = [
        ("Mikä Kakobuy on?",
         f"Kakobuy on ostoagentti. Se ostaa puolestasi kiinalaisista kaupoista, kuten Taobaosta, 1688:sta ja Weidianista, jotka eivät itse lähetä ulkomaille. Tuote saapuu agentin varastoon Kiinassa, siitä otetaan QC-kuvat ja vasta sen jälkeen valitset kansainvälisen linjan Suomeen. {host} on riippumaton opas, ei kauppa eikä kassa, eikä se näe tiliäsi."),
        ("Millä kielellä Kakobuy toimii?",
         "Virallinen sivusto ja sovellus ovat pääosin englanniksi, ja osa tuotekorteista on kiinaksi. Tämä opas kirjoittaa suomeksi, mutta tilaus, maksu ja reklamaatio tehdään aina virallisella sivustolla. Jos jokin näkymä on epäselvä, ota kuvakaappaus ja kysy virallisesta chatista samana päivänä, ennen kuin maksat mitään. Selaimen käännöstoiminto auttaa, mutta tarkista summat aina alkuperäisestä näkymästä."),
        ("Mikä spreadsheet on?",
         "Spreadsheet ei ole Excel-taulukko. Se on katalogi tuotekortteja, joissa on kuva, merkki, viitehinta ja kaupan linkki. Löydät kortin w2clinksistä, kopioit kaupan linkin ja liität sen Kakobuyn hakuun. Katalogi ei myy mitään eikä peri maksuja, ja hinnat juanissa muuttuvat päivittäin, joten tarkista hinta aina agentilta."),
        ("Kuinka monta kertaa maksan?",
         "Maksat kahdesti. Ensin tuote ja Kiinan sisäinen rahti varastoon. Myöhemmin, kun tuotteet ovat varastossa ja QC-kuvat on hyväksytty, maksat kansainvälisen rahdin Suomeen. Välissä voit vielä peruuttaa, yhdistää paketteja tai vaihtaa linjaa. Tämä sivu ei näytä lopullista summaa, koska se lasketaan virallisessa arvioijassa."),
        ("Mistä rahtihinta muodostuu?",
         f"Moni linja laskuttaa suuremman painoista: vaa’an painon tai tilavuuspainon, usein P×L×K (cm) / 8000. Untuvatakki on kevyt mutta tilaa vievä, joten tilavuus ratkaisee. Syötä omat mittasi viralliseen arvioijaan osoitteessa {EST} ja valitse kohteeksi Suomi. Tämä desk ei keksi linjaa, kuljetusaikaa eikä euromäärää."),
        ("Kuinka kauan tuotteet saavat olla varastossa?",
         f"{store} Jos aiot yhdistää useita tilauksia samaan pakettiin, suunnittele aikataulu niin, ettei ensimmäinen tuote odota liian kauan. Varastointiehdot voivat muuttua, joten tämä opas ei lupaa yhtään päivämäärää puolestasi."),
        ("Voinko yhdistää useita tilauksia yhteen pakettiin?",
         "Kyllä, se on tavallisin tapa säästää. Tuotteet odottavat varastossa, kunnes lähetät paketin. Yhdistäminen ei ole tullikikka: se mitä ilmoitat Tullille, lukee virallisessa lähetyksessä, ei tällä sivulla. Jos QC jakaa tuotteet useampaan laatikkoon, arvioi jokainen laatikko erikseen samaan kohteeseen Suomeen. Pyydä tarvittaessa poistamaan ylimääräiset kenkälaatikot, koska ne kasvattavat tilavuuspainoa."),
        ("Kuka maksaa tullin ja ALV:n Suomeen?",
         "Se lukee valitun linjan SKU:ssa. Joissain linjoissa maksut on laskettu mukaan, toisissa vastaanottaja maksaa. Tarkista ehdot ennen lähetystä ja säilytä kuitit."),
        ("Mitkä kynnysarvot pätevät?",
         "ALV, IOSS ja kynnysarvot muuttuvat. Tarkista ajantasainen tieto Tullilta lähetyspäivänä. Älä ilmoita todellista pienempää arvoa: se on riski sinulle, ei agentille."),
        ("Mitä QC-kuvat ovat?",
         "QC-kuvat ovat varaston ottamia valokuvia tuotteestasi ennen kansainvälistä lähetystä. Tarkista koko, väri, ompeleet ja mittanauhakuva. Lisäkulmat maksavat usein erikseen. Reklamointi on helpointa silloin, kun tuote on vielä varastossa, joten älä varaa linjaa Suomeen ennen kuin kuvat täsmäävät tilaukseen. Vertaa mittoja aina tuotekortin kokotaulukkoon, ei pelkkään kirjainkokoon."),
        ("Mitä teen, jos kuva ei vastaa tilausta?",
         "Avaa tiketti virallisella sivustolla heti, kun kuvat tulevat, ja liitä mukaan kuvakaappaus tuotekortista. Pyydä vaihtoa, palautusta myyjälle tai hyvitystä. Tämä opas ei voi avata tikettiä puolestasi eikä nähdä tilausnumeroasi. Säilytä kaikki viestit, koska ne ovat ainoa todisteesi myöhemmin. Kun tuote on jo lähtenyt Suomeen, vaihtoehtoja on selvästi vähemmän."),
        ("Miksi tuotteella ei ole hintaa?",
         "Kortti ilman hintaa tai manuaalinen lomake tarkoittaa yleensä, että lähdelinkki ei ole ostettavissa agentin kautta tai hintaa ei voitu lukea. Restricted on ostoesto, ei Tullin päätös. Tupakka, alkoholi ja lääkkeet eivät matkusta. Älä tilaa ilman oikeaa hintaa ja variantteja. Etsi mieluummin toinen myyjä samalle tuotteelle w2clinksistä tai suoraan Kakobuyn haulla."),
        ("Voiko elektroniikkaa lähettää Suomeen?",
         "Elektroniikassa on usein litiumakku, eikä jokainen lentolinja hyväksy niitä. Tarkista virallisesta arvioijasta, mitkä linjat Suomeen ottavat akun tai magneetin, ennen kuin ostat. Muuten tuote voi jäädä varastoon odottamaan. Sama koskee nesteitä, aerosoleja ja kaikkea, jossa on paristo. Tilaa tällaiset tuotteet erikseen, jotta ne eivät pysäytä koko pakettia."),
        ("Mitä teen, jos paketti on jumissa?",
         "Katso ensin oikea näkymä: tilaukset, sitten varasto, sitten lähetetty paketti. Useimmiten kysymys miksi se seisoo tarkoittaa, että katsot väärää näyttöä. Kun paketti on lähtenyt, seuraa virallista seurantakoodia. Jos koodi ei päivity useaan päivään, avaa tiketti virallisella sivustolla ja liitä seurantanumero. Suomessa viimeisen kilometrin hoitaa usein Posti, joten tarkista myös sen seuranta."),
        ("Miten otan yhteyttä Kakobuyhin?",
         f"Virallisen sivuston chatin tai tiketin kautta osoitteessa {OFFICIAL}. Tämä opas ({host}) ei voi hakea tilausnumeroa eikä muuttaa tiliäsi. Säilytä sovelluksen tilausnumero. Oppaan omat korjaukset ja palautteen voit lähettää osoitteeseen {MAIL}, mutta tilauksiin liittyvät asiat hoidetaan aina Kakobuyn kanssa."),
    ]
    out = list(pairs)
    if pack.get("duty"):
        out[7] = (out[7][0], f"{pack['duty']} {out[7][1]}".strip())
    if pack.get("threshold"):
        out[8] = (out[8][0], f"{pack['threshold']} {out[8][1]}".strip())
    return out


def _faqs(key: str) -> list[tuple[str, str]]:
    p = PACKS[key]
    pairs = []
    facts = _facts(key)
    raw = _fi_long_faqs(facts) if p["loc"] == "fi" else long_faqs(facts)
    for q, a in raw:
        a = a.replace("/api/products/", "w2clinks")
        a = re.sub(r"ni copia un snapshot de 58 l[ií]neas ajenas\.?", "", a, flags=re.I)
        a = re.sub(r"58 l[ií]neas(?: para Espa\w*)?", "", a, flags=re.I)
        a = re.sub(r"23[,.]81\s*USD", "", a, flags=re.I)
        pairs.append((q, a))
    extra = f"The delivery address uses a {p['postal']}."
    if p["loc"] == "fi":
        extra = f"Toimitusosoitteessa on {p['postal']}."
    elif p["loc"] == "es":
        extra = f"La dirección de entrega es una {p['postal']}."
    elif p["loc"] == "fr":
        extra = f"L’adresse de livraison est une {p['postal']}."
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
    if loc == "fi":
        return [
            "Mikä Kakobuy on ja millä kielellä se toimii",
            "Mitä maksat",
            "Tuonti Suomeen",
            "Varasto, kuvat ja mikä saa matkustaa",
            "Jos jokin ei täsmää",
        ]
    if loc == "es":
        return [
            "Qué es Kakobuy y en qué idioma funciona",
            "Qué vas a pagar",
            f"Importación a {dest}",
            "Almacén, fotos y qué puede viajar",
            "Si algo no cuadra",
        ]
    if loc == "fr":
        return [
            "Ce qu’est Kakobuy et dans quelle langue ça tourne",
            "Ce que tu vas payer",
            f"Import vers {dest}",
            "Entrepôt, photos et ce qui peut voyager",
            "Si quelque chose cloche",
        ]
    if loc == "nl":
        return [
            "Wat Kakobuy is en in welke taal het draait",
            "Wat je gaat betalen",
            f"Invoer naar {dest}",
            "Magazijn, foto’s en wat mag reizen",
            "Als iets niet klopt",
        ]
    return [
        "What Kakobuy is, and which language it uses",
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
    if loc == "fi":
        head = ("Jos ajattelet", "Kirjoita")
        rows = (
            ("lenkkarit", "sneakers"),
            ("huppari", "hoodie"),
            ("takki", "jacket"),
            ("housut", "trousers"),
            ("laukku", "bag"),
            ("lasit", "glasses"),
            ("kello", "watch"),
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
    elif loc == "fr":
        head = ("Si tu penses à", "Tape")
        rows = (
            ("baskets", "sneakers"),
            ("hoodie", "hoodie"),
            ("veste", "jacket"),
            ("pantalon", "trousers"),
            ("sac", "bag"),
            ("lunettes", "glasses"),
            ("montre", "watch"),
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
    if loc == "fi":
        return cats_for(FI_LABELS)
    if loc == "es":
        return cats_for(ES_LABELS)
    if loc == "fr":
        return cats_for(FR_LABELS)
    if loc == "nl":
        return cats_for(NL_LABELS)
    return cats_for(EN_LABELS)


def _sheet(desk: CountryDesk) -> str:
    return w2c_sheet(desk)


def _fig(src: str, alt: str, cap: str, w: int = 1200, h: int = 750) -> str:
    return cms_fig(src, alt, cap, w, h)


def _wall(key: str, notes: dict[str, str] | None = None) -> str:
    p = PACKS[key]
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
    if loc == "fi":
        off_alt, off_cap = (
            "Kakobuyn virallinen etusivu: hakupalkki, valikko ja rahtiarvioija",
            f"Virallinen kakobuy.com, {DATE}. Arvioija on osoitteessa /tools/estimate. Tämä desk ei keksi linjaa eikä summaa.",
        )
        sheet_alt, sheet_cap = (
            "Kakobuy-katalogi w2clinksissä: tuotekortit, joissa kuva, merkki ja viitehinta",
            "Kortteja, ei Excel-soluja. Juanihinnat muuttuvat päivittäin. Kuvattu 6 Oct 2026, kategoria SNEAKERS.",
        )
        vol_alt, vol_cap = (
            "Esimerkki tilavuuspainosta: 40×40×3 cm ja 200 g vaa’alla on 600 g tilavuutta",
            "Laskuesimerkki, ei varastokuva. Moni linja laskuttaa suuremman painon vaa’asta ja tilavuudesta, usein P×L×K (cm) / 8000.",
        )
        zoek_alt, zoek_cap = (
            "Huppari-haku Kakobuy-katalogissa w2clinksissä",
            "Tulokset ja suodatinsarake. Kuvattu 6 Oct 2026.",
        )
        diy_alt, diy_cap = (
            "Kakobuyn haku: liitä Taobao-, 1688- tai Weidian-linkki",
            f"Julkinen liitospalkki kakobuy.comissa, {DATE}. Tämä desk ei keksi täytettyä tilauslomaketta.",
        )
    elif loc == "es":
        off_alt, off_cap = (
            "Portada oficial de Kakobuy: búsqueda, menú y estimador de envío",
            f"Sitio oficial kakobuy.com, {DATE}. El estimador está en /tools/estimate. Esta guía no inventa una línea ni un importe.",
        )
        sheet_alt, sheet_cap = (
            "Catálogo Kakobuy en w2clinks: fichas con foto, marca y precio de referencia",
            "Fichas, no celdas de Excel. Los precios en yuan cambian cada día. Captura 6 Oct 2026, categoría SNEAKERS.",
        )
        vol_alt, vol_cap = (
            "Ejemplo de peso volumétrico: 40×40×3 cm y 200 g en báscula son 600 g de volumen",
            "Un ejemplo calculado, no una foto de almacén. Muchas líneas facturan el máximo entre báscula y volumen, a menudo L×W×H (cm) / 8000.",
        )
        zoek_alt, zoek_cap = (
            "Búsqueda de hoodie en el catálogo Kakobuy de w2clinks",
            "Resultados con columna de filtros. Captura 6 Oct 2026.",
        )
        diy_alt, diy_cap = (
            "Búsqueda Kakobuy: pegar un enlace Taobao, 1688 o Weidian",
            f"Barra pública en kakobuy.com, {DATE}. Esta guía no inventa un pedido relleno.",
        )
    elif loc == "fr":
        off_alt, off_cap = (
            "Page d’accueil officielle Kakobuy : recherche, menu et estimateur de livraison",
            f"Site officiel kakobuy.com, {DATE}. L’estimateur est sur /tools/estimate. Ce guide n’invente ni ligne ni montant.",
        )
        sheet_alt, sheet_cap = (
            "Catalogue Kakobuy sur w2clinks : fiches avec photo, marque et prix de référence",
            "Des fiches, pas des cellules Excel. Les prix en yuan changent chaque jour. Capture 6 Oct 2026, catégorie SNEAKERS.",
        )
        vol_alt, vol_cap = (
            "Exemple de poids volumétrique : 40×40×3 cm et 200 g à la balance deviennent 600 g de volume",
            "Un exemple calculé, pas une photo d’entrepôt. Beaucoup de lignes facturent le max entre balance et volume, souvent L×W×H (cm) / 8000.",
        )
        zoek_alt, zoek_cap = (
            "Recherche hoodie dans le catalogue Kakobuy sur w2clinks",
            "Résultats avec colonne de filtres. Capture 6 Oct 2026.",
        )
        diy_alt, diy_cap = (
            "Recherche Kakobuy : coller un lien Taobao, 1688 ou Weidian",
            f"Barre publique sur kakobuy.com, {DATE}. Ce guide n’invente pas une commande remplie.",
        )
    elif loc == "nl":
        off_alt, off_cap = (
            "Officiële Kakobuy-homepage: zoekbalk, menu en verzendschatter",
            f"Officiële kakobuy.com, {DATE}. De schatter staat op /tools/estimate. Deze gids verzint geen lijn en geen bedrag.",
        )
        sheet_alt, sheet_cap = (
            "Kakobuy-catalogus op w2clinks: kaarten met foto, merk en referentieprijs",
            "Kaarten, geen Excel-cellen. Yuan-prijzen veranderen per dag. Opname 6 Oct 2026, categorie SNEAKERS.",
        )
        vol_alt, vol_cap = (
            "Voorbeeld volumegewicht: 40×40×3 cm en 200 g op de weegschaal wordt 600 g volume",
            "Een rekenvoorbeeld, geen magazijnfoto. Veel lijnen factureren het maximum van weegschaal en volume, vaak L×W×H (cm) / 8000.",
        )
        zoek_alt, zoek_cap = (
            "Hoodie-zoekopdracht in de Kakobuy-catalogus op w2clinks",
            "Resultaten met filterkolom. Opname 6 Oct 2026.",
        )
        diy_alt, diy_cap = (
            "Kakobuy-zoekbalk: een Taobao-, 1688- of Weidian-link plakken",
            f"Publieke plakbalk op kakobuy.com, {DATE}. Deze gids verzint geen ingevulde bestelling.",
        )
    else:
        off_alt, off_cap = (
            "Official Kakobuy homepage: search bar, navigation and the shipping estimator",
            f"Official kakobuy.com, {DATE}. The estimator lives at /tools/estimate. This desk does not invent a line or a dollar amount.",
        )
        sheet_alt, sheet_cap = (
            "Kakobuy catalogue on w2clinks: product cards with photo, brand and reference price",
            "Cards, not Excel cells. Yuan prices change by the day. Capture 6 Oct 2026, category SNEAKERS.",
        )
        vol_alt, vol_cap = (
            "Worked example of volume weight: 40×40×3 cm and 200 g scale becomes 600 g volume",
            "A worked example, not a warehouse photo. Many lines bill the greater of scale and volume, often L×W×H (cm) / 8000.",
        )
        zoek_alt, zoek_cap = (
            "Hoodie search in the Kakobuy catalogue on w2clinks",
            "Results with the filter column. Capture 6 Oct 2026.",
        )
        diy_alt, diy_cap = (
            "Kakobuy search: paste a Taobao, 1688 or Weidian link",
            f"Public paste bar on kakobuy.com, {DATE}. This desk does not invent a filled order total.",
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
    if loc == "fi":
        return f"""
<section class="sec" id="shots">
  <div class="wrap"><div class="split split--rev"><div>
    <h2>Liitä kiinalainen linkki tai hae sovelluksessa</h2>
    <p class="lead">Kakobuy alkaa näin: liität Taobao-, 1688- tai Weidian-linkin tai kirjoitat tuotteen nimen. Kiinalainen kauppa näkee Kakobuyn; sinä näet myöhemmin varastokuvat ja linjan Suomeen.</p>
    <p>Jos haku ei lue linkkiä, seuraava askel on manuaalinen lomake: nimi, koko, väri ja hinta juaneina. Kansainvälisen rahdin maksat vasta myöhemmin, varastosta.</p>
    <p><a class="btn" href="{escape(p["guide"])}">Opas vaihe vaiheelta</a>
       <a class="btn btn--ghost" href="{escape(OFFICIAL)}" rel="noopener">Virallinen sivusto</a></p>
  </div>{fig}</div></div>
</section>
"""
    if loc == "es":
        return f"""
<section class="sec" id="shots">
  <div class="wrap"><div class="split split--rev"><div>
    <h2>Pega un enlace chino, o busca en la app</h2>
    <p class="lead">Kakobuy empieza así: pegas un enlace de Taobao, 1688 o Weidian, o escribes el nombre. La tienda china ve Kakobuy; tú luego ves fotos de almacén y una línea hacia {escape(dest)}.</p>
    <p>Si la búsqueda no lee el enlace, el siguiente paso es el formulario manual: nombre, talla, color y precio en yuan. El internacional lo pagas después, desde el almacén.</p>
    <p><a class="btn" href="{escape(p["guide"])}">Guía paso a paso</a>
       <a class="btn btn--ghost" href="{escape(OFFICIAL)}" rel="noopener">Sitio oficial</a></p>
  </div>{fig}</div></div>
</section>
"""
    if loc == "fr":
        return f"""
<section class="sec" id="shots">
  <div class="wrap"><div class="split split--rev"><div>
    <h2>Colle un lien chinois, ou cherche dans l’app</h2>
    <p class="lead">Kakobuy commence ainsi : tu colles un lien Taobao, 1688 ou Weidian, ou tu tapes le nom. La boutique chinoise voit Kakobuy ; toi, tu vois ensuite les photos d’entrepôt et une ligne vers {escape(dest)}.</p>
    <p>Si la recherche ne lit pas le lien, l’étape suivante est le formulaire manuel : nom, taille, couleur et prix en yuan. L’international se paie plus tard, depuis l’entrepôt.</p>
    <p><a class="btn" href="{escape(p["guide"])}">Guide pas à pas</a>
       <a class="btn btn--ghost" href="{escape(OFFICIAL)}" rel="noopener">Site officiel</a></p>
  </div>{fig}</div></div>
</section>
"""
    if loc == "nl":
        return f"""
<section class="sec" id="shots">
  <div class="wrap"><div class="split split--rev"><div>
    <h2>Plak een Chinese link, of zoek in de app</h2>
    <p class="lead">Kakobuy start zo: je plakt een Taobao-, 1688- of Weidian-link, of typt de naam. De Chinese shop ziet Kakobuy; jij ziet daarna magazijnfoto’s en een lijn naar {escape(dest)}.</p>
    <p>Leest de zoekbalk de link niet, is het handmatige formulier de volgende stap: naam, maat, kleur en prijs in yuan. Internationaal betaal je later, vanuit het magazijn.</p>
    <p><a class="btn" href="{escape(p["guide"])}">Handleiding stap voor stap</a>
       <a class="btn btn--ghost" href="{escape(OFFICIAL)}" rel="noopener">Officiële site</a></p>
  </div>{fig}</div></div>
</section>
"""
    return f"""
<section class="sec" id="shots">
  <div class="wrap"><div class="split split--rev"><div>
    <h2>Paste a Chinese link, or search in the app</h2>
    <p class="lead">Kakobuy starts the same way: paste a Taobao, 1688 or Weidian link, or type the name. The Chinese shop sees Kakobuy; you later see warehouse photos and a line to {escape(dest)}.</p>
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
    if loc == "fi":
        return f"""
<section class="sec" id="states">
  <div class="wrap"><div class="split"><div>
    <h2>Yhdeksän tilaa, kolme näkymää</h2>
    <p class="lead">Ensin maksat tuotteen ja Kiinan sisäisen rahdin varastoon. Kansainvälinen rahti tulee myöhemmin, kun valitset linjan Suomeen. ”Miksi se seisoo?” tarkoittaa lähes aina: katsot väärää näkymää.</p>
    <p>Ensimmäiset vaiheet ovat tilausten alla, sitten varasto, sitten paketti, jonka lähetät. {store}</p>
    <p><a class="btn" href="{escape(p["guide"])}">Opas koko polusta</a></p>
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
    if loc == "fr":
        return f"""
<section class="sec" id="states">
  <div class="wrap"><div class="split"><div>
    <h2>Neuf statuts, trois écrans</h2>
    <p class="lead">Tu paies d’abord le produit plus le trajet intérieur en Chine jusqu’à l’entrepôt. L’international vient ensuite, quand tu choisis une ligne vers {escape(dest)}. « Pourquoi c’est bloqué ? » veut presque toujours dire : tu regardes le mauvais écran.</p>
    <p>Les premiers pas sont sous les commandes, puis l’entrepôt, puis le colis que tu envoies. {store}</p>
    <p><a class="btn" href="{escape(p["guide"])}">Guide avec le parcours</a></p>
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
    <p><a class="btn" href="{escape(p["guide"])}">Handleiding met het pad</a></p>
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
    if loc == "fi":
        return f"""
<section class="sec sec--tint" id="restricted">
  <div class="wrap"><div class="split split--rev"><div>
    <h2>Monia tuotteita ei voi ostaa, vaikka ne näkyvät</h2>
    <p class="lead">Virallisella sivustolla näet kortteja ilman hintaa tai manuaalisen lomakkeen kauppakortin sijaan. Se ei ole tämän etusivun vika: lähdelinkki ei ole ostettavissa agentin kautta, tai hintaa ei voitu lukea.</p>
    <p>Sääntö: ilman oikeaa hintaa ja variantteja älä tilaa. Tupakka, alkoholi ja lääkkeet eivät matkusta. Restricted on ostoesto, ei {escape(customs)}n päätös. Kakobuy ei myy omaa varastoa.</p>
  </div>{fig}</div></div>
</section>
"""
    if loc == "es":
        return f"""
<section class="sec sec--tint" id="restricted">
  <div class="wrap"><div class="split split--rev"><div>
    <h2>Muchos productos no se pueden comprar aunque aparezcan</h2>
    <p class="lead">En el sitio oficial ves fichas sin precio, o un formulario manual en lugar de una ficha de tienda. No es un fallo de esta portada: el enlace de origen no se puede comprar por el agente, o el precio no se leyó.</p>
    <p>Regla: sin precio real y variantes, no pidas. Tabaco, alcohol y medicamentos no viajan. Restricted es un bloqueo de compra, no un aviso de {escape(customs)}. Kakobuy no vende mercancía propia.</p>
  </div>{fig}</div></div>
</section>
"""
    if loc == "fr":
        return f"""
<section class="sec sec--tint" id="restricted">
  <div class="wrap"><div class="split split--rev"><div>
    <h2>Beaucoup de produits ne s’achètent pas même s’ils s’affichent</h2>
    <p class="lead">Sur le site officiel tu vois des fiches sans prix, ou un formulaire manuel à la place d’une fiche boutique. Ce n’est pas un bug de cette page d’accueil : le lien source n’est pas achetable via l’agent, ou le prix n’a pas pu être lu.</p>
    <p>Règle : sans vrai prix et variantes, n’ordonne pas. Tabac, alcool et médicaments ne voyagent pas. Restricted est un blocage d’achat, pas un avis de {escape(customs)}. Kakobuy ne vend pas de stock propre.</p>
  </div>{fig}</div></div>
</section>
"""
    if loc == "nl":
        return f"""
<section class="sec sec--tint" id="restricted">
  <div class="wrap"><div class="split split--rev"><div>
    <h2>Veel producten kun je niet kopen, ook al staan ze er</h2>
    <p class="lead">Op de officiële site zie je kaarten zonder prijs, of een handmatig formulier in plaats van een shopkaart. Dat is geen bug van deze homepage: de bronlink is via de agent niet te koop, of de prijs liet zich niet lezen.</p>
    <p>Regel: zonder echte prijs en varianten niet bestellen. Tabak, alcohol en geneesmiddelen reizen niet. Restricted is een koopblokkade, geen bericht van {escape(customs)}. Kakobuy verkoopt geen eigen voorraad.</p>
  </div>{fig}</div></div>
</section>
"""
    return f"""
<section class="sec sec--tint" id="restricted">
  <div class="wrap"><div class="split split--rev"><div>
    <h2>Many products you cannot buy even if they appear</h2>
    <p class="lead">On the official site you will see cards without a price, or a manual form instead of a shop card. That is not a bug of this homepage: the source link is not buyable through the agent, or the price could not be read.</p>
    <p>Rule: without a real price and variants, do not order. Tobacco, alcohol and medicines do not travel. Restricted is a purchase block, not a {escape(customs)} seizure notice. Kakobuy does not sell its own stock.</p>
  </div>{fig}</div></div>
</section>
"""


def build_home(key: str) -> str:
    p = PACKS[key]
    desk = desk_for(key)
    sheet = _sheet(desk)
    wall = _wall(key)
    chips = _chips(key)
    fig_off, fig_sheet, fig_vol, fig_zoek, _fig_diy = _shots(key)
    dest = p["dest_label"]
    loc = p["loc"]
    shots = _sec_shots(key, fig_zoek)
    states = _sec_states(key, fig_off)
    restricted = _sec_restricted(key, fig_sheet)
    if loc == "fi":
        body = f"""
<section class="hero">
  <div class="hero__bg" role="img" aria-label="Kakobuyn virallinen etusivu"></div>
  <div class="hero__scrim"></div>
  <div class="wrap">
    <span class="eyebrow">{escape(p["eyebrow"])}</span>
    <h1>{escape(p["hero_h1"])}</h1>
    <p class="lead">{escape(p["lead"])}</p>
    <div class="sbox">
      <form id="w2c-search" action="{escape(sheet)}" method="get" target="_blank" rel="nofollow noopener" role="search">
        <label class="skip" for="q">Hae tuotteita w2clinksistä</label>
        <input id="q" name="q" type="search" autocomplete="off" placeholder="Hae sneakers, hoodie, jacket…">
        <input type="hidden" name="utm_source" value="{escape(p["host"])}">
        <input type="hidden" name="utm_medium" value="referral">
        <input type="hidden" name="utm_campaign" value="hero-buscador">
        <button type="submit">Hae</button>
      </form>
      <div class="chips">{chips}</div>
    </div>
  </div>
</section>
<section class="sec sec--first" id="agent">
  <div class="wrap"><div class="split"><div>
    <h2>Ostoagentti on välikäsi, ei kauppa</h2>
    <p class="lead">Kakobuy ei myy omia tuotteita. Se ostaa puolestasi kiinalaisista kaupoista, jotka eivät lähetä ulkomaille, vastaanottaa paketin varastoon, kuvaa sen, säilyttää sen ja lähettää Suomeen, kun sinä päätät.</p>
    <p>Maksat kahdesti (ensin tuote, myöhemmin kansainvälinen rahti) ja odotat kahdesti. Välissä voit vielä peruuttaa, yhdistää tai vaihtaa linjaa. Maksut ja tiketit pysyvät osoitteessa {escape(OFFICIAL)}.</p>
    <p><a class="btn" href="{escape(p["guide"])}">Opas vaihe vaiheelta</a></p>
  </div>{fig_off}</div></div>
</section>
{shots}
<section class="sec sec--tint" id="sheet-explain">
  <div class="wrap"><div class="split split--rev"><div>
    <span class="eyebrow" style="color:var(--acd)">Harhaanjohtava nimi</span>
    <h2>Spreadsheet ei ole Excel-tiedosto</h2>
    <p class="lead">Sana «spreadsheet» kuulostaa riveiltä ja sarakkeilta. Tässä se tarkoittaa tuotekorttien katalogia: kuva, merkki, viitehinta ja linkki, jonka liität agenttiin.</p>
    <p>w2clinksissä näet kortteja, et soluja.</p>
    <p><a class="btn btn--ghost" href="{escape(p["catalog"])}">Näin katalogi toimii</a></p>
  </div>{fig_sheet}</div></div>
</section>
<section class="sec" id="cat-wall">
  <div class="wrap">
    <h2>Kolmekymmentäkolme kategoriaa ensimmäiseen päivään</h2>
    <p class="lead">Jokainen kortti avaa kategorian katalogissa. Aloita yhdellä: viisi kategoriaa ensimmäisessä haulissa on nopein tie kalliiseen ja hankalaan laatikkoon.</p>
    <div class="cat-grid">{wall}</div>
  </div>
</section>
{states}
<section class="sec sec--tint" id="lab">
  <div class="wrap"><div class="split"><div>
    <h2>Suomeen on linjoja, mutta kaikki eivät ole auki</h2>
    <p class="lead">Valitse arvioijassa kohde <strong>{escape(p["dest_zh"])}</strong>, {escape(p.get("lab_not", "ei EU"))}. Toimitusosoitteessa on {escape(p["postal"])}.</p>
    <p>Virallinen arvioija on osoitteessa {escape(EST)}: valitse maa, älä tätä hostnamea. Tämä desk ei keksi linjaa, kuljetusaikaa eikä euromäärää. Lähde: <a href="{escape(p["customs_url"])}" rel="noopener">{escape(p["customs"])}</a>.</p>
    <p><a class="btn" href="{escape(EST)}">Kakobuyn virallinen arvioija</a>
       <a class="btn btn--ghost" href="{escape(p["ship"])}">Toimitussuunnitelma</a></p>
  </div>{fig_off}</div></div>
</section>
<section class="sec" id="volume">
  <div class="wrap"><div class="split split--rev"><div>
    <h2>Maksamasi paino on harvoin pelkkä vaaka</h2>
    <p class="lead">Moni linja laskuttaa suuremman painon vaa’asta ja tilavuudesta. Tavallinen jakaja on P×L×K (cm) / 8000. Untuvatakki on kevyt ja tilaa vievä: siinä tilavuus ratkaisee.</p>
    <p>Esimerkki: 40×40×3 cm on 4800 cm³, jaettuna 8000:lla se on 600 g tilavuutta, kun todellinen paino on 200 g. Omat mittasi syötät viralliseen arvioijaan, kohteena Suomi.</p>
  </div>{fig_vol}</div></div>
</section>
{restricted}
<section class="sec" id="faq">
  <div class="wrap">
    <h2>Ohje, uutiset ja mistä kysyä</h2>
    <p class="lead">Ensimmäisten tilausten kysymykset toistuvat. Ne ovat Ohje-sivulla — omassa osoitteessaan, ei tämän etusivun liitteenä.</p>
    <p><a class="btn" href="{escape(p["help"])}">Kaikki kysymykset Ohjeessa</a>
       <a class="btn btn--ghost" href="{escape(p["news"])}">Päivätyt tarkistukset Uutisissa</a>
       <a class="btn btn--ghost" href="{escape(p["about"])}">Meistä</a></p>
  </div>
</section>
"""
        desc = "Riippumaton opas suomeksi: miten ostat Kiinasta Kakobuyn kautta, miten w2clinks-katalogi toimii ja miten paketti kulkee Suomeen."
    elif loc == "es":
        body = f"""
<section class="hero">
  <div class="hero__bg" role="img" aria-label="Portada oficial de Kakobuy"></div>
  <div class="hero__scrim"></div>
  <div class="wrap">
    <span class="eyebrow">{escape(p["eyebrow"])}</span>
    <h1>{escape(p["hero_h1"])}</h1>
    <p class="lead">{escape(p["lead"])}</p>
    <div class="sbox">
      <form id="w2c-search" action="{escape(sheet)}" method="get" target="_blank" rel="nofollow noopener" role="search">
        <label class="skip" for="q">Buscar productos en w2clinks</label>
        <input id="q" name="q" type="search" autocomplete="off" placeholder="Busca zapatillas, hoodie, chaqueta…">
        <input type="hidden" name="utm_source" value="{escape(p["host"])}">
        <input type="hidden" name="utm_medium" value="referral">
        <input type="hidden" name="utm_campaign" value="hero-buscador">
        <button type="submit">Buscar</button>
      </form>
      <div class="chips">{chips}</div>
    </div>
  </div>
</section>
<section class="sec sec--first" id="agent">
  <div class="wrap"><div class="split"><div>
    <h2>Un agente de compras es un intermediario, no una tienda</h2>
    <p class="lead">Kakobuy no vende mercancía propia. Compra por ti en tiendas chinas que no envían al extranjero, recibe el paquete en el almacén, lo fotografía, lo guarda y lo envía a {escape(dest)} cuando tú lo decides.</p>
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
    <p><a class="btn" href="{escape(EST)}">Sitio oficial Kakobuy</a>
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
    <h2>Ayuda, noticias y dónde preguntar</h2>
    <p class="lead">Las dudas de los primeros pedidos se repiten. Están en Ayuda — una URL propia, no un apéndice de esta portada.</p>
    <p><a class="btn" href="{escape(p["help"])}">Todas las preguntas en Ayuda</a>
       <a class="btn btn--ghost" href="{escape(p["news"])}">Checks con fecha en Noticias</a>
       <a class="btn btn--ghost" href="{escape(p["about"])}">Sobre nosotros</a></p>
  </div>
</section>
"""
        desc = f"Guía independiente en español: cómo compras en China con Kakobuy, cómo funciona el catálogo w2clinks, cómo viaja un paquete a {dest}."
    elif loc == "fr":
        body = f"""
<section class="hero">
  <div class="hero__bg" role="img" aria-label="Page d’accueil officielle Kakobuy"></div>
  <div class="hero__scrim"></div>
  <div class="wrap">
    <span class="eyebrow">{escape(p["eyebrow"])}</span>
    <h1>{escape(p["hero_h1"])}</h1>
    <p class="lead">{escape(p["lead"])}</p>
    <div class="sbox">
      <form id="w2c-search" action="{escape(sheet)}" method="get" target="_blank" rel="nofollow noopener" role="search">
        <label class="skip" for="q">Chercher des produits sur w2clinks</label>
        <input id="q" name="q" type="search" autocomplete="off" placeholder="Cherche baskets, hoodie, veste…">
        <input type="hidden" name="utm_source" value="{escape(p["host"])}">
        <input type="hidden" name="utm_medium" value="referral">
        <input type="hidden" name="utm_campaign" value="hero-buscador">
        <button type="submit">Chercher</button>
      </form>
      <div class="chips">{chips}</div>
    </div>
  </div>
</section>
<section class="sec sec--first" id="agent">
  <div class="wrap"><div class="split"><div>
    <h2>Un agent d’achat est un intermédiaire, pas une boutique</h2>
    <p class="lead">Kakobuy ne vend pas de stock propre. Il achète pour toi dans des boutiques chinoises qui n’expédient pas à l’étranger, reçoit le colis en entrepôt, le photographie, le stocke et l’envoie vers {escape(dest)} quand tu le décides.</p>
    <p>Tu paies deux fois (d’abord le produit, plus tard l’international) et tu attends deux fois. Entre les deux tu peux encore annuler, regrouper ou changer de ligne. Paiements et tickets restent sur {escape(OFFICIAL)}.</p>
    <p><a class="btn" href="{escape(p["guide"])}">Guide pas à pas</a></p>
  </div>{fig_off}</div></div>
</section>
{shots}
<section class="sec sec--tint" id="sheet-explain">
  <div class="wrap"><div class="split split--rev"><div>
    <span class="eyebrow" style="color:var(--acd)">Un nom qui trompe</span>
    <h2>Un spreadsheet n’est pas un fichier Excel</h2>
    <p class="lead">En français, « spreadsheet » sonne encore comme une grille. Ici c’est un catalogue de fiches produit avec photo, marque, prix de référence et le lien à coller dans l’agent.</p>
    <p>Sur w2clinks tu vois des fiches, pas des cellules.</p>
    <p><a class="btn btn--ghost" href="{escape(p["catalog"])}">Comment marche le catalogue</a></p>
  </div>{fig_sheet}</div></div>
</section>
<section class="sec" id="cat-wall">
  <div class="wrap">
    <h2>Trente-trois catégories pour le premier jour</h2>
    <p class="lead">Chaque fiche ouvre cette catégorie dans le catalogue. Commence par une : cinq catégories dans le premier haul, c’est le plus court chemin vers une boîte chère et malcommode.</p>
    <div class="cat-grid">{wall}</div>
  </div>
</section>
{states}
<section class="sec sec--tint" id="lab">
  <div class="wrap"><div class="split"><div>
    <h2>{escape(dest[0].upper() + dest[1:])} a des lignes, mais pas toutes sont ouvertes</h2>
    <p class="lead">Dans l’estimateur, choisis destination <strong>{escape(p["dest_zh"])}</strong>, pas EU. L’adresse est une {escape(p["postal"])}.</p>
    <p>L’estimateur officiel est sur {escape(EST)} : choisis le pays, pas ce nom d’hôte. Ce guide n’invente ni ligne, ni transit, ni montant. Source : <a href="{escape(p["customs_url"])}" rel="noopener">{escape(p["customs"])}</a>.</p>
    <p><a class="btn" href="{escape(EST)}">Site officiel Kakobuy</a>
       <a class="btn btn--ghost" href="{escape(p["ship"])}">Plan de livraison</a></p>
  </div>{fig_off}</div></div>
</section>
<section class="sec" id="volume">
  <div class="wrap"><div class="split split--rev"><div>
    <h2>Le poids que tu paies n’est presque jamais la balance seule</h2>
    <p class="lead">Beaucoup de lignes facturent le maximum entre balance et volume. Un diviseur courant est L×W×H (cm) / 8000. Une doudoune est légère et volumineuse : c’est le volume qui décide.</p>
    <p>Exemple : 40×40×3 cm font 4800 cm³, divisés par 8000 font 600 g de volume pour 200 g réels. Tes mesures, tu les saisis dans l’estimateur officiel, destination {escape(dest)}.</p>
  </div>{fig_vol}</div></div>
</section>
{restricted}
<section class="sec" id="faq">
  <div class="wrap">
    <h2>Aide, actus et où demander</h2>
    <p class="lead">Les doutes des premières commandes se répètent. Ils sont sur Aide — une URL à part, pas un appendice de cette page d’accueil.</p>
    <p><a class="btn" href="{escape(p["help"])}">Toutes les questions sur Aide</a>
       <a class="btn btn--ghost" href="{escape(p["news"])}">Checks datés sur Actus</a>
       <a class="btn btn--ghost" href="{escape(p["about"])}">À propos</a></p>
  </div>
</section>
"""
        desc = f"Guide indépendant en français : comment tu achètes en Chine via Kakobuy, comment marche le catalogue w2clinks, comment un colis voyage vers {dest}."
    elif loc == "nl":
        body = f"""
<section class="hero">
  <div class="hero__bg" role="img" aria-label="Officiële Kakobuy-homepage"></div>
  <div class="hero__scrim"></div>
  <div class="wrap">
    <span class="eyebrow">{escape(p["eyebrow"])}</span>
    <h1>{escape(p["hero_h1"])}</h1>
    <p class="lead">{escape(p["lead"])}</p>
    <div class="sbox">
      <form id="w2c-search" action="{escape(sheet)}" method="get" target="_blank" rel="nofollow noopener" role="search">
        <label class="skip" for="q">Producten zoeken op w2clinks</label>
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
  <div class="wrap"><div class="split"><div>
    <h2>Een inkoopagent is een tussenpersoon, geen shop</h2>
    <p class="lead">Kakobuy verkoopt geen eigen voorraad. Hij koopt voor jou in Chinese shops die niet naar het buitenland sturen, neemt het pakket in het magazijn aan, fotografeert het, slaat het op en stuurt het naar {escape(dest)} als jij dat besluit.</p>
    <p>Je betaalt twee keer (eerst het product, later internationaal) en wacht twee keer. Daartussen kun je nog annuleren, bundelen of van lijn wisselen. Betaling en tickets blijven op {escape(OFFICIAL)}.</p>
    <p><a class="btn" href="{escape(p["guide"])}">Handleiding stap voor stap</a></p>
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
    <p><a class="btn" href="{escape(EST)}">Officiële Kakobuy-site</a>
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
        desc = f"Onafhankelijke gids in het Nederlands: hoe je via Kakobuy in China koopt, hoe de w2clinks-catalogus werkt, hoe een pakket naar {dest} reist."
    else:
        body = f"""
<section class="hero">
  <div class="hero__bg" role="img" aria-label="Official Kakobuy homepage"></div>
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
  <div class="wrap"><div class="split"><div>
    <h2>A purchasing agent is a middleman, not a shop</h2>
    <p class="lead">Kakobuy does not sell its own goods. It buys for you in Chinese shops that do not ship abroad, receives the parcel in the warehouse, photographs it, stores it, and ships to {escape(dest)} when you decide.</p>
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
    <p>What you see on w2clinks are cards, not cells. Each fiche has the link Kakobuy needs.</p>
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
    <p>The official estimator lives at kakobuy.com/tools/estimate — pick the dest country, not this hostname. This desk does not invent a line, a transit-day count or a money amount. Open {escape(OFFICIAL)} the morning you ship. Import: <a href="{escape(p["customs_url"])}" rel="noopener">{escape(p["customs"])}</a>.</p>
    <p><a class="btn" href="{escape(EST)}">Official Kakobuy site</a>
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
            f"Independent English guide: how you buy in China through Kakobuy, how the w2clinks catalogue works, how a parcel travels to {dest}."
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
    notes = {"fi": CAT_NOTES_FI, "es": CAT_NOTES_ES, "fr": CAT_NOTES_FR, "nl": CAT_NOTES_NL}.get(loc, CAT_NOTES_EN)
    wall = _wall(key, notes)
    _fig_off, fig_sheet, _fig_vol, fig_zoek, fig_diy = _shots(key)
    dest = p["dest_label"]
    sheet = _sheet(desk)
    keys = _keys_table(key)
    if loc == "fi":
        topic = "mikä se on ja mitä kategorioita löydät"
        body = f"""
<section class="sec sec--first"><div class="wrap"><div class="split"><div>
<span class="eyebrow" style="color:var(--acc)">Katalogi</span>
<h1>Mikä Kakobuy Spreadsheet on ja mitä siitä löydät</h1>
<p class="lead">Tuotekorttien katalogi, ei Excel-tiedosto. Kolmekymmentäkolme kategoriaa, suodattimet, kuva, merkki ja linkki agenttia varten.</p>
</div>{fig_sheet}</div></div></section>
<section class="sec sec--tint"><div class="wrap"><div class="split split--rev"><div>
<h2>Miksi erillinen katalogi</h2>
<p>Agentin haku palauttaa koko kiinalaisen valikoiman, valtavan ja usein kiinaksi. Katalogi on tehnyt kotiläksyt valmiiksi: joku on valinnut kannattavat kortit, laittanut ne kategorioihin ja jättänyt kaupan linkin valmiiksi.</p>
<p>Käytännössä: löydät kortin w2clinksistä, kopioit lähdelinkin ja liität sen Kakobuyn hakuun tai manuaaliseen lomakkeeseen. Katalogi ei peri rahaa eikä myy mitään.</p>
</div>{fig_zoek}</div></div></section>
<section class="sec" id="categorias"><div class="wrap">
<h2>Kolmekymmentäkolme kategoriaa ja mitä tarkistat kussakin</h2>
<p class="lead">Lause jokaisen kortin alla ei ole täytettä: se on virhe, joka toistuu kategoriassa useimmin, kun ostat kaukaa.</p>
<div class="cat-grid cat-grid--rich">{wall}</div>
</div></section>
<section class="sec sec--tint" id="first-category"><div class="wrap">
<h2>Miten valitset ensimmäisen kategorian</h2>
<p class="lead">Ensimmäinen tilaus: jotain litteää ja kevyttä — T-paitoja, shortseja, koruja. Ne saapuvat nopeammin, rahti on halvempi, ja testaat koko ketjun ilman suurta riskiä.</p>
<p>Tilaa vievät toiseen tilaukseen: untuvatakit, laukut, hatut. Ei siksi, että ne olisivat huonompia, vaan koska niiden rahti riippuu tilavuudesta — ja sen lasket hyvin vasta yhden kierroksen jälkeen.</p>
<p>Kolme kategoriaa lisäehdoilla: elektroniikka (usein litiumia), lasit (särkyviä) ja kaikki, missä on akku tai magneetti. Kaikki linjat Suomeen eivät ota niitä. Tarkista arvioija ennen kuin ne jäävät varastoon.</p>
</div></section>
<section class="sec" id="keys"><div class="wrap">
<h2>Epämukava tosiasia: katalogi hakee englanniksi</h2>
<p class="lead">Tarkistimme sen sana sanalta {escape(DATE)}. Se kannattaa tietää ennen kuin kirjoitat ensimmäisen haun suomeksi.</p>
<p>Suomenkieliset sanat kuten lenkkarit, huppari tai lasit antavat usein nolla tulosta. Englanninkieliset avainsanat sneakers, hoodie, jacket, trousers, bag, glasses tai watch antavat sivukaupalla kortteja. Siksi etusivun haku lähettää englanninkielisiä avainsanoja w2clinksiin.</p>
{keys}
</div></section>
<section class="sec sec--tint"><div class="wrap"><div class="split"><div>
<h2>Katalogista tilaukseen hukkaamatta linkkiä</h2>
<p class="lead">Kortti on alku, ei kassa. Useimmin epäonnistuva vaihe: kopioit katalogin URL-osoitteen kaupan linkin sijaan. Kakobuy tarvitsee Taobao-, 1688- tai Weidian-linkin.</p>
<p>Jos liität katalogikortin oman osoitteen, agentti ei tiedä, mitä ostaa. Kopioi kaupan linkki, liitä se Kakobuyn hakuun, tarkista hinta ja variantti, ja maksa kansainvälinen rahti vasta kun varastokuvat täsmäävät.</p>
<p>Jos haku ei lue linkkiä, jäljelle jää manuaalinen tilauslomake virallisella sivustolla. Ohita kortit ilman hintaa — lähdelinkki on Kiinassa usein jo kuollut.</p>
<p><a class="btn" href="{escape(sheet)}">Avaa katalogi w2clinksissä</a>
   <a class="btn btn--ghost" href="{escape(p["guide"])}">Opas vaihe vaiheelta</a></p>
</div>{fig_diy}</div></div></section>
"""
    elif loc == "es":
        topic = "qué es y qué categorías encuentras"
        body = f"""
<section class="sec sec--first"><div class="wrap"><div class="split"><div>
<span class="eyebrow" style="color:var(--acc)">El catálogo</span>
<h1>Qué es Kakobuy Spreadsheet, y qué encuentras dentro</h1>
<p class="lead">Un catálogo de fichas de producto, no un archivo Excel. Treinta y tres categorías, filtros, foto, marca y el enlace para el agente.</p>
</div>{fig_sheet}</div></div></section>
<section class="sec sec--tint"><div class="wrap"><div class="split split--rev"><div>
<h2>Por qué un catálogo aparte</h2>
<p>La búsqueda del agente devuelve todo el stock chino, enorme y a menudo en chino. Un catálogo ya hizo el trabajo: alguien eligió qué fichas merecen, las puso en categoría y dejó listo el enlace de la tienda.</p>
<p>En la práctica: encuentras la ficha en w2clinks, copias el enlace de origen y lo pegas en la búsqueda de Kakobuy o en el formulario manual. El catálogo no cobra y no vende.</p>
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
<p class="lead">La ficha es el principio, no la caja. El paso que más falla: copias la URL de la ficha del catálogo en vez del enlace de la tienda. Kakobuy necesita el enlace Taobao, 1688 o Weidian.</p>
<p>Si pegas la URL de la ficha del catálogo, el agente no sabe qué comprar. Copia el enlace de la tienda, pégalo en la búsqueda de Kakobuy, revisa precio y variante, y paga el internacional solo cuando las fotos de almacén cuadran.</p>
<p>Si la búsqueda no lee el enlace, queda el formulario manual del sitio oficial. Fichas sin precio: sáltalas — el enlace de origen en China a menudo ya está muerto.</p>
<p><a class="btn" href="{escape(sheet)}">Abrir el catálogo en w2clinks</a>
   <a class="btn btn--ghost" href="{escape(p["guide"])}">Guía paso a paso</a></p>
</div>{fig_diy}</div></div></section>
"""
    elif loc == "fr":
        topic = "ce que c’est et quelles catégories tu trouves"
        body = f"""
<section class="sec sec--first"><div class="wrap"><div class="split"><div>
<span class="eyebrow" style="color:var(--acc)">Le catalogue</span>
<h1>Ce qu’est Kakobuy Spreadsheet, et ce que tu y trouves</h1>
<p class="lead">Un catalogue de fiches produit, pas un fichier Excel. Trente-trois catégories, filtres, photo, marque et le lien pour l’agent.</p>
</div>{fig_sheet}</div></div></section>
<section class="sec sec--tint"><div class="wrap"><div class="split split--rev"><div>
<h2>Pourquoi un catalogue à part</h2>
<p>La recherche de l’agent renvoie tout le stock chinois, énorme et souvent en chinois. Un catalogue a déjà fait le travail : quelqu’un a choisi quelles fiches valent, les a mises en catégorie et a préparé le lien boutique.</p>
<p>En pratique : tu trouves la fiche sur w2clinks, tu copies le lien source et tu le colles dans la recherche Kakobuy ou le formulaire manuel. Le catalogue n’encaisse rien et ne vend rien.</p>
</div>{fig_zoek}</div></div></section>
<section class="sec" id="categorias"><div class="wrap">
<h2>Les trente-trois catégories, et ce que tu vérifies dans chacune</h2>
<p class="lead">La phrase sous chaque fiche n’est pas du remplissage : c’est l’erreur qui revient le plus dans cette catégorie quand tu achètes de loin.</p>
<div class="cat-grid cat-grid--rich">{wall}</div>
</div></section>
<section class="sec sec--tint" id="first-category"><div class="wrap">
<h2>Comment tu choisis la première catégorie</h2>
<p class="lead">Première commande : quelque chose de plat et léger — t-shirts, shorts, bijoux. Ça arrive plus tôt, ça coûte moins cher à envoyer, et tu vérifies tout le circuit sans trop risquer.</p>
<p>Le volumineux pour la deuxième commande : doudounes, sacs, casquettes. Pas parce qu’ils sont moins bons, mais parce que le port dépend du volume — et ça, tu le calcules bien après un tour.</p>
<p>Trois catégories avec extra : électronique (souvent du lithium), lunettes (fragiles) et tout avec batterie ou aimant. Toutes les lignes vers {escape(dest)} ne les acceptent pas. Vérifie l’estimateur avant de les laisser en entrepôt.</p>
</div></section>
<section class="sec" id="keys"><div class="wrap">
<h2>Fait gênant : le catalogue cherche en anglais</h2>
<p class="lead">On l’a vérifié mot pour mot le {escape(DATE)}. Tu veux le savoir avant de taper la première recherche en français.</p>
<p>Les graphies locales comme baskets, pull ou lunettes donnent souvent zéro. Les keys anglaises sneakers, hoodie, jacket, trousers, bag, glasses ou watch donnent des pages. C’est pour ça que la recherche de la page d’accueil envoie des keys anglaises à w2clinks.</p>
{keys}
</div></section>
<section class="sec sec--tint"><div class="wrap"><div class="split"><div>
<h2>Du catalogue à la commande, sans perdre le lien</h2>
<p class="lead">La fiche est le début, pas la caisse. L’étape qui rate le plus : tu copies l’URL de la fiche catalogue au lieu du lien boutique. Kakobuy a besoin du lien Taobao, 1688 ou Weidian.</p>
<p>Si tu colles l’URL de la fiche catalogue, l’agent ne sait pas quoi acheter. Copie le lien boutique, colle-le dans la recherche Kakobuy, vérifie prix et variante, et paie l’international seulement quand les photos d’entrepôt collent.</p>
<p>Si la recherche ne lit pas le lien, reste le formulaire manuel du site officiel. Fiches sans prix : saute-les — le lien source en Chine est souvent déjà mort.</p>
<p><a class="btn" href="{escape(sheet)}">Ouvrir le catalogue sur w2clinks</a>
   <a class="btn btn--ghost" href="{escape(p["guide"])}">Guide pas à pas</a></p>
</div>{fig_diy}</div></div></section>
"""
    elif loc == "nl":
        topic = "wat het is en welke categorieën je vindt"
        body = f"""
<section class="sec sec--first"><div class="wrap"><div class="split"><div>
<span class="eyebrow" style="color:var(--acc)">De catalogus</span>
<h1>Wat Kakobuy Spreadsheet is, en wat je erin vindt</h1>
<p class="lead">Een catalogus van productkaarten, geen Excel-bestand. Drieëndertig categorieën, filters, foto, merk en de link voor de agent.</p>
</div>{fig_sheet}</div></div></section>
<section class="sec sec--tint"><div class="wrap"><div class="split split--rev"><div>
<h2>Waarom een aparte catalogus</h2>
<p>De zoekbalk van een agent geeft de hele Chinese voorraad, enorm en vaak in het Chinees. Een catalogus heeft het huiswerk al gedaan: iemand koos welke kaarten de moeite waard zijn, zette ze in een categorie en legde de shoplink klaar.</p>
<p>In de praktijk: je vindt de kaart op w2clinks, kopieert de bronlink en plakt die in de Kakobuy-zoekbalk of het handmatige formulier. De catalogus int niets en verkoopt niets.</p>
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
<p class="lead">De kaart is het begin, niet de kassa. De stap die het vaakst misgaat: je kopieert de catalogus-URL in plaats van de shoplink. Kakobuy heeft de Taobao-, 1688- of Weidian-link nodig.</p>
<p>Plak je de URL van de cataloguskaart zelf, dan weet de agent niet wat hij moet kopen. Kopieer de shoplink, plak hem in de Kakobuy-zoekbalk, check prijs en variant, en betaal internationaal pas als de magazijnfoto’s kloppen.</p>
<p>Leest de zoekbalk de link niet, blijft het handmatige formulier op de officiële site. Kaarten zonder prijs overslaan — de bronlink is in China vaak al dood.</p>
<p><a class="btn" href="{escape(sheet)}">Catalogus op w2clinks openen</a>
   <a class="btn btn--ghost" href="{escape(p["guide"])}">Handleiding stap voor stap</a></p>
</div>{fig_diy}</div></div></section>
"""
    else:
        topic = "what it is and which categories you will find"
        body = f"""
<section class="sec sec--first"><div class="wrap"><div class="split"><div>
<span class="eyebrow" style="color:var(--acc)">The catalogue</span>
<h1>What Kakobuy Spreadsheet is, and what you find in it</h1>
<p class="lead">It is a catalogue of product cards, not an Excel file. Thirty-three categories, filters, and cards with a photo, a brand and the link for the agent.</p>
</div>{fig_sheet}</div></div></section>
<section class="sec sec--tint"><div class="wrap"><div class="split split--rev"><div>
<h2>Why a separate catalogue</h2>
<p>An agent search bar returns the whole stock of Chinese shops, huge and often in Chinese. A catalogue does the homework: someone already picked which fiches are worth it, put them in a category and left the shop link ready.</p>
<p>In practice: you find the fiche on w2clinks, copy the source link and paste it into Kakobuy search or the manual form. The catalogue collects no money and sells nothing.</p>
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
<p class="lead">The fiche is the start, not checkout. The step that fails most often is copying the catalogue URL instead of the shop link. Kakobuy needs the Taobao, 1688 or Weidian link.</p>
<p>If you paste the catalogue-card URL itself, the agent does not know what to buy. Copy the shop link, paste it into Kakobuy search, check price and variant, and pay international only after the warehouse photos match.</p>
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
    if loc == "fi":
        topic = "ohje ja usein kysytyt kysymykset"
        body = f"""
<article class="pw">
  <span class="eyebrow" style="color:var(--acd)">Ohje</span>
  <h1>Ohje ja kysymykset Kakobuysta — kohde {escape(p["dest_label"])}</h1>
  <p class="lead">Ensimmäisten tilausten kysymykset. Toimitusosoitteessa on {escape(p["postal"])}.</p>
  {fig_off}{html_f}
  <p><a class="btn" href="{escape(EST)}">Kakobuyn virallinen arvioija</a>
     <a class="btn btn--ghost" href="{escape(p["ship"])}">Toimitussuunnitelma</a></p>
</article>
"""
    elif loc == "es":
        topic = "ayuda y preguntas frecuentes"
        body = f"""
<article class="pw">
  <span class="eyebrow" style="color:var(--acd)">Ayuda</span>
  <h1>Ayuda y preguntas sobre Kakobuy en {escape(p["dest_label"])}</h1>
  <p class="lead">Preguntas de los primeros pedidos. La dirección es una {escape(p["postal"])}.</p>
  {fig_off}{html_f}
  <p><a class="btn" href="{escape(EST)}">Sitio oficial Kakobuy</a>
     <a class="btn btn--ghost" href="{escape(p["ship"])}">Plan de envío</a></p>
</article>
"""
    elif loc == "fr":
        topic = "aide et questions fréquentes"
        body = f"""
<article class="pw">
  <span class="eyebrow" style="color:var(--acd)">Aide</span>
  <h1>Aide et questions sur Kakobuy depuis {escape(p["dest_label"])}</h1>
  <p class="lead">Questions des premières commandes. L’adresse est une {escape(p["postal"])}.</p>
  {fig_off}{html_f}
  <p><a class="btn" href="{escape(EST)}">Site officiel Kakobuy</a>
     <a class="btn btn--ghost" href="{escape(p["ship"])}">Plan de livraison</a></p>
</article>
"""
    elif loc == "nl":
        topic = "hulp en veelgestelde vragen"
        body = f"""
<article class="pw">
  <span class="eyebrow" style="color:var(--acd)">Hulp</span>
  <h1>Hulp en vragen over Kakobuy in {escape(p["dest_label"])}</h1>
  <p class="lead">Vragen van eerste bestellingen. Het afleveradres is een {escape(p["postal"])}.</p>
  {fig_off}{html_f}
  <p><a class="btn" href="{escape(EST)}">Officiële Kakobuy-site</a>
     <a class="btn btn--ghost" href="{escape(p["ship"])}">Verzendplan</a></p>
</article>
"""
    else:
        topic = "help and frequently asked questions"
        body = f"""
<article class="pw">
  <span class="eyebrow" style="color:var(--acd)">Help</span>
  <h1>Help and questions about Kakobuy in {escape(p["dest_label"])}</h1>
  <p class="lead">Questions that come back on first orders. The delivery address uses a {escape(p["postal"])}.</p>
  {fig_off}{html_f}
  <p><a class="btn" href="{escape(EST)}">Official Kakobuy site</a>
     <a class="btn btn--ghost" href="{escape(p["ship"])}">Shipping plan</a></p>
</article>
"""
    return cms_shell(
        desk, page_title(desk, topic),
        f"FAQ about Kakobuy from {p['dest_label']}.",
        f"https://{p['host']}{p['help']}", [faq_ld(p["lang"], pairs)], body, p["help"],
    )


def build_news(key: str) -> str:
    p = PACKS[key]
    desk = desk_for(key)
    loc = p["loc"]
    if loc == "fi":
        items = [
            ("Ensimmäinen kierros: virallinen arvioija",
             f"{DATE}: rahtiluvut tulevat vain osoitteesta {EST}. Ei keksittyä linjaa eikä summaa.",
             f"Avaa virallinen sivusto lähetysaamuna, kohde {p['dest_zh']}. {p['postal']}."),
            ("w2clinks hakee englanniksi",
             "sneakers, hoodie, jacket antavat sivuja; suomenkieliset sanat usein nolla. Mitattu 6 Oct 2026.",
             "Kirjoita englanninkielinen avainsana tai napauta etusivun sirua."),
            ("Varastointi: kaksi lukua virallisissa ohjeissa",
             _storage("fi"),
             "Suunnittele yhdistäminen niin, ettei ensimmäinen tuote odota viimeiseen päivään."),
            ("Sisarhostit pysyvät erillään",
             "CA, FI, ES, FR ja NL ovat omia tiedostojaan. Ei 301-ohjausta niiden välillä eikä kakobuydocs.comiin.",
             "Hub kakobuydocs.com ei ole tullialue."),
        ]
        h1, topic, brow = "Mitä tarkistimme alustalta, päivämäärän kera", "mitä tarkistimme alustalta", "Uutiset"
        lead = "Tämä ei ole yrityksen uutiskirje. Omia tarkistuksia, päivämäärän kera."
    elif loc == "es":
        items = [
            ("Primera ronda: el estimador oficial",
             f"El {DATE} las cifras de flete solo salen de {EST}: elige el país, no este hostname. Ninguna línea inventada.",
             f"La mañana del envío abre el sitio oficial, destino {p['dest_zh']}. {p['postal']}."),
            ("w2clinks busca en inglés",
             "sneakers, hoodie, jacket dan páginas; grafías locales a menudo cero. Medido 6 Oct 2026.",
             "Escribe la key inglesa, o toca un chip en la portada."),
            ("Almacén: dos cifras en la Ayuda oficial",
             _storage("es"),
             "Planifica la consolidación para que la primera pieza no espere hasta el último día."),
            ("Los hosts hermanos siguen separados",
             "CA, FI, ES, FR y NL son archivos distintos. Ningún 301 entre ellos, ningún 301 hacia kakobuydocs.com.",
             "El hub kakobuydocs.com no es un territorio aduanero."),
        ]
        h1, topic, brow = "Qué hemos comprobado en la plataforma, con fecha", "qué hemos comprobado en la plataforma", "Noticias"
        lead = "No es un boletín de empresa. Checks nuestros, con fecha."
    elif loc == "fr":
        items = [
            ("Premier tour : l’estimateur officiel",
             f"Le {DATE} les chiffres de fret viennent seulement de {EST}. Aucune ligne inventée.",
             f"Le matin de l’envoi, ouvre le site officiel, destination {p['dest_zh']}. {p['postal']}."),
            ("w2clinks cherche en anglais",
             "sneakers, hoodie, jacket donnent des pages ; les graphies locales souvent zéro. Mesuré 6 Oct 2026.",
             "Tape la key anglaise, ou touche un chip sur la page d’accueil."),
            ("Entrepôt : deux chiffres dans l’aide officielle",
             _storage("fr"),
             "Planifie le regroupement pour que la première pièce n’attende pas jusqu’au dernier jour."),
            ("Les hôtes sœurs restent séparés",
             "CA, FI, ES, FR et NL sont des fichiers distincts. Aucun 301 entre eux, aucun 301 vers kakobuydocs.com.",
             "Le hub kakobuydocs.com n’est pas un territoire douanier."),
        ]
        h1, topic, brow = "Ce que nous avons vérifié sur la plateforme, avec une date", "ce que nous avons vérifié sur la plateforme", "Actus"
        lead = "Ce n’est pas une newsletter d’entreprise. Des checks à nous, avec une date."
    elif loc == "nl":
        items = [
            ("Eerste ronde: de officiële schatter",
             f"Op {DATE} komen vrachtcijfers alleen uit {EST}. Geen verzonnen lijn.",
             f"Open de officiële site de ochtend dat je verzendt, bestemming {p['dest_zh']}. {p['postal']}."),
            ("w2clinks zoekt in het Engels",
             "sneakers, hoodie, jacket geven pagina’s; lokale spellingen vaak nul. Gemeten 6 Oct 2026.",
             "Typ de Engelse key, of tik een chip op de homepage."),
            ("Magazijn: twee getallen in de officiële Help",
             _storage("nl"),
             "Plan het bundelen zo dat het eerste stuk niet tot de laatste dag wacht."),
            ("Zusterhosts blijven apart",
             "CA, FI, ES, FR en NL zijn eigen bestanden. Geen 301 onderling, geen 301 naar kakobuydocs.com.",
             "De hub kakobuydocs.com is geen douanegebied."),
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
            ("Warehouse: two numbers in the official Help",
             _storage("en"),
             "Plan consolidation so the first piece does not wait until the last day."),
            ("Sister country hosts stay separate",
             "Canada, Finland, Spain, France and the Netherlands on Kakobuy stay on their own hosts. None of them 301 into kakobuydocs.com.",
             "The kakobuydocs.com hub is not a customs territory."),
        ]
        h1, topic, brow = "What we checked on the platform, with a date", "what we checked on the platform", "News"
        lead = "This is not a company newsletter. These are our own checks, with a date."
    ld = itemlist_ld(
        url=f"https://{p['host']}{p['news']}",
        name="Kakobuy dest checks",
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
        desk, page_title(desk, topic), "Dated checks on Kakobuy.",
        f"https://{p['host']}{p['news']}", [ld], body, p["news"],
    )


def build_about(key: str) -> str:
    p = PACKS[key]
    desk = desk_for(key)
    fig_off, *_ = _shots(key)
    loc = p["loc"]
    if loc == "fi":
        topic = "keitä olemme ja miten tavoitat meidät"
        body = f"""
<article class="pw">
  <span class="eyebrow" style="color:var(--acd)">Meistä</span>
  <h1>Riippumaton sivusto Kakobuysta, suomeksi</h1>
  <p class="lead">Kakobuy Spreadsheet ei ole Kakobuy. Se on toimituksellinen opas. kakobuy.com on virallinen sivusto; kakobuydocs.com on meidän hubimme, ei tullialue.</p>
  {fig_off}
  <h2>Miten työskentelemme</h2>
  <p>Rahtiluvut tulevat vain viralliselta arvioijalta, joten tämä desk ei julkaise keksittyä hintaa. Tuonti: <a href="{escape(p["customs_url"])}" rel="noopener">{escape(p["customs"])}</a>.</p>
  <h2>Yhteystiedot</h2>
  <p>Tilaukset: virallinen sivusto. Tämä opas: <a href="mailto:{escape(MAIL)}">{escape(MAIL)}</a>.</p>
</article>
"""
    elif loc == "es":
        topic = "quiénes somos y cómo contactarnos"
        body = f"""
<article class="pw">
  <span class="eyebrow" style="color:var(--acd)">Sobre nosotros</span>
  <h1>Un sitio independiente sobre Kakobuy, en español</h1>
  <p class="lead">Kakobuy Spreadsheet no es Kakobuy. Es una guía editorial. kakobuy.com es el sitio oficial; kakobuydocs.com es nuestro hub, no un territorio aduanero.</p>
  {fig_off}
  <h2>Contacto</h2>
  <p>Pedidos: sitio oficial. Esta guía: <a href="mailto:{escape(MAIL)}">{escape(MAIL)}</a>.</p>
</article>
"""
    elif loc == "fr":
        topic = "qui nous sommes et comment nous joindre"
        body = f"""
<article class="pw">
  <span class="eyebrow" style="color:var(--acd)">À propos</span>
  <h1>Un site indépendant sur Kakobuy, en français</h1>
  <p class="lead">Kakobuy Spreadsheet n’est pas Kakobuy. C’est un guide éditorial. kakobuy.com est le site officiel ; kakobuydocs.com est notre hub, pas un territoire douanier.</p>
  {fig_off}
  <h2>Contact</h2>
  <p>Commandes : site officiel. Ce guide : <a href="mailto:{escape(MAIL)}">{escape(MAIL)}</a>.</p>
</article>
"""
    elif loc == "nl":
        topic = "wie we zijn en hoe je ons bereikt"
        body = f"""
<article class="pw">
  <span class="eyebrow" style="color:var(--acd)">Over ons</span>
  <h1>Een onafhankelijke site over Kakobuy, in het Nederlands</h1>
  <p class="lead">Kakobuy Spreadsheet is Kakobuy niet. Het is een redactionele gids. kakobuy.com is de officiële site; kakobuydocs.com is onze hub, geen douanegebied.</p>
  {fig_off}
  <h2>Contact</h2>
  <p>Bestellingen: officiële site. Deze gids: <a href="mailto:{escape(MAIL)}">{escape(MAIL)}</a>.</p>
</article>
"""
    else:
        topic = "who we are and how to reach us"
        body = f"""
<article class="pw">
  <span class="eyebrow" style="color:var(--acd)">About us</span>
  <h1>An independent site about Kakobuy, in English</h1>
  <p class="lead">Kakobuy Spreadsheet is not Kakobuy. It is an editorial guide. kakobuy.com is the official site; kakobuydocs.com is our hub, not a customs territory.</p>
  {fig_off}
  <h2>How we work</h2>
  <p>Shipping figures come only from the official estimator at {escape(EST)}, so this desk publishes no invented rate. Import points to <a href="{escape(p["customs_url"])}" rel="noopener">{escape(p["customs"])}</a>.</p>
  <h2>Contact</h2>
  <p>Orders: official Kakobuy chat. This guide: <a href="mailto:{escape(MAIL)}">{escape(MAIL)}</a>.</p>
</article>
"""
    return cms_shell(
        desk, page_title(desk, topic),
        "Independent Kakobuy guide: how we check facts.",
        f"https://{p['host']}{p['about']}", [], body, p["about"],
    )


def _inner_pages(key: str) -> dict[str, tuple[str, str, str]]:
    """href, topic, html-body for dest-local ranked inners (not OrientDig leftovers)."""
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
    catalog = escape(p["catalog"])
    help_h = escape(p["help"])
    dest_e = escape(dest)
    lab_not = escape(p.get("lab_not", "not EU"))

    if loc == "fi":
        guide_topic = "miten teet ensimmäisen tilauksen Suomeen"
        guide_body = f"""
<article class="pw">
  <span class="eyebrow" style="color:var(--acd)">Opas</span>
  <h1>Ensimmäinen Kakobuy-tilaus Suomesta</h1>
  <p class="lead">Kopioi linkki, liitä se agenttiin, tarkista varastokuva, yhdistä, valitse kohde {dest_zh}. Toimitusosoitteessa on {fp}.</p>
  {fig_off}
  <h2>1. Avaa kortti w2clinksissä</h2>
  <p>Yksi kolmestakymmenestäkolmesta kategoriasta, kuva ja kaupan linkki. Se on katalogi, ei Excel-tiedosto.</p>
  {fig_sheet}
  <h2>2. Liitä linkki viralliselle sivustolle</h2>
  <p>Maksut ja tiketit pysyvät osoitteessa {official}. Tämä desk ei näe tiliäsi. Jos haku ei lue linkkiä, virallisella sivustolla on manuaalinen tilauslomake.</p>
  {fig_diy}
  <h2>3. Kuva, sitten yhdistäminen, sitten lähetys</h2>
  <p>Rahtiluvut tulevat vain osoitteesta {est}: valitse maa, älä tätä hostnamea. {escape(_storage("fi"))}</p>
  <h2>Yhdeksän tilaa, kolme näkymää</h2>
  <p>Ensin tuote ja sisäinen rahti varastoon. Kansainvälinen myöhemmin. ”Miksi se seisoo?” tarkoittaa lähes aina väärää näkymää — tilaukset, sitten varasto, sitten paketti.</p>
  <h2>Ensimmäinen haul: litteät ensin</h2>
  <p>T-paidat, shortsit ja korut ensimmäiselle kierrokselle. Untuva, laukut ja hatut toiselle. Elektroniikassa on usein litiumia: tarkista linja virallisella sivustolla.</p>
  <p><a class="btn" href="{guide}">Opas</a> <a class="btn btn--ghost" href="{ship}">Toimitussuunnitelma</a></p>
</article>
"""
        ship_topic = "toimitus ja tulli Suomeen"
        ship_body = f"""
<article class="pw">
  <span class="eyebrow" style="color:var(--acd)">Toimitus</span>
  <h1>Toimitus Suomeen: arvioija, tilavuus, tulli</h1>
  <p class="lead">Kohde {dest_zh}, {lab_not}. Toimitusosoitteessa on {fp}.</p>
  {fig_off}
  <h2>Virallinen arvioija ratkaisee</h2>
  <p>{escape(DATE)}: rahtiluvut tulevat vain osoitteesta {est}. Tämä desk ei keksi linjaa, kuljetusaikaa eikä euromäärää. Lähde: <a href="{customs_url}" rel="noopener">{customs}</a>.</p>
  <h2>Vaaka vastaan tilavuus</h2>
  <p>Moni linja laskuttaa suuremman painon vaa’asta ja P×L×K (cm) / 8000 -kaavasta. Esimerkki: 40×40×3 cm on 4800 cm³, jaettuna 8000:lla 600 g tilavuutta, kun todellinen paino on 200 g. Tässä HTML:ssä ei ole SKU-hintaa.</p>
  {fig_vol}
  <h2>Yhdistäminen ei ole tullikikka</h2>
  <p>Useampi varastotuote samassa laatikossa voi säästää maksuja. Se mitä ilmoitat Tullille, lukee virallisessa lähetyksessä, ei tällä sivulla.</p>
  <h2>Restricted ei ole tullin ilmoitus</h2>
  <p>Kortti ilman hintaa tai manuaalinen lomake tarkoittaa: lähdelinkki ei ole ostettavissa agentin kautta. Tupakka, alkoholi ja lääkkeet eivät matkusta.</p>
  <h2>Varastokuvat ennen linjaa</h2>
  <p>QC-kuvat tulevat sovellukseen, kun tuote on varastossa. Lisäkulmat maksavat usein. Reklamointi on helpompaa, kun tuote on vielä varastossa. {escape(_storage("fi"))}</p>
  <h2>Osoite tällä destillä</h2>
  <p>Toimitusosoitteessa on {fp}. Viisinumeroinen postinumero kuuluu viralliseen lähetykseen, ei kikaksi tälle sivulle. Ruotsalainen postinumero on väärä maa.</p>
  <p><a class="btn" href="{est}">Kakobuyn virallinen arvioija</a> <a class="btn btn--ghost" href="{help_h}">Ohje</a></p>
</article>
"""
        legit_topic = "onko Kakobuy oikea agentti Suomeen"
        legit_body = f"""
<article class="pw">
  <span class="eyebrow" style="color:var(--acd)">Tarkistus</span>
  <h1>Onko Kakobuy oikea ostoagentti?</h1>
  <p class="lead">kakobuy.com on virallinen sivusto. kakobuydocs.com on meidän hubimme, ei tullialue. Tämä desk ei ole Kakobuy.</p>
  {fig_off}
  <p>Emme keksi varastointiaikaa emmekä tariffia. {escape(_storage("fi"))} Tilaukset vain osoitteessa {official}.</p>
  <p>Toimitusosoitteessa tällä destillä on {fp}.</p>
  <p><a class="btn" href="{guide}">Opas</a> <a class="btn btn--ghost" href="{help_h}">Ohje</a></p>
</article>
"""
        coup_topic = "kupongit ovat virallisella sivustolla"
        coup_body = f"""
<article class="pw">
  <span class="eyebrow" style="color:var(--acd)">Koodit</span>
  <h1>Kupongit: ei tämän destin otsikossa</h1>
  <p class="lead">Tämä desk ei tulosta kutsukoodeja otsikkoon eikä etusivulle. Jos Kakobuy julkaisee koodin, se on kirjautumisen jälkeen osoitteessa {official}.</p>
  {fig_off}
  <p>Toimitusosoitteessa on edelleen {fp}. Kohde arvioijassa: {dest_zh}.</p>
  <p><a class="btn" href="{official}">Virallinen sivusto</a> <a class="btn btn--ghost" href="{catalog}">Katalogi</a></p>
</article>
"""
        sheet_topic = "katalogi ja miten käytät sitä Suomesta"
        sheet_body = f"""
<article class="pw">
  <span class="eyebrow" style="color:var(--acd)">Spreadsheet</span>
  <h1>Kakobuy Spreadsheet on katalogi, ei taulukko</h1>
  <p class="lead">Kortteja, joissa on kuva, merkki ja kaupan linkki. Kolmekymmentäkolme kategoriaa kuten w2clinksissä.</p>
  {fig_sheet}
  <p>Hae englanniksi (sneakers, hoodie, jacket). Toimitusosoitteessa tällä destillä on {fp}.</p>
  <p><a class="btn" href="{catalog}">Avaa katalogi</a> <a class="btn btn--ghost" href="{guide}">Opas</a></p>
</article>
"""
    elif loc == "es":
        guide_topic = f"cómo haces el primer pedido desde {dest}"
        guide_body = f"""
<article class="pw">
  <span class="eyebrow" style="color:var(--acd)">Guía</span>
  <h1>Primer pedido Kakobuy, desde {dest_e}</h1>
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
        ship_topic = f"envío y aduanas desde {dest}"
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
  <p>Las fotos QC llegan a la app cuando la pieza está en almacén. Ángulos extra a menudo de pago. Reclamar es más fácil mientras sigue ahí.</p>
  <h2>La dirección en este dest</h2>
  <p>La dirección es una {fp}. Ese formato va en el envío oficial, no como truco en esta página.</p>
  <p><a class="btn" href="{est}">Sitio oficial Kakobuy</a> <a class="btn btn--ghost" href="{help_h}">Ayuda</a></p>
</article>
"""
        legit_topic = f"Kakobuy es un agente de verdad desde {dest}"
        legit_body = f"""
<article class="pw">
  <span class="eyebrow" style="color:var(--acd)">Check</span>
  <h1>¿Kakobuy es un agente de compras de verdad?</h1>
  <p class="lead">kakobuy.com es el sitio oficial. kakobuydocs.com es nuestro hub, no un territorio aduanero. Este dest no es Kakobuy.</p>
  {fig_off}
  <p>No inventamos plazo de almacén ni tarifa. {escape(_storage("es"))} Pedidos solo en {official}.</p>
  <p>La dirección en este dest es una {fp}.</p>
  <p><a class="btn" href="{guide}">Guía</a> <a class="btn btn--ghost" href="{help_h}">Ayuda</a></p>
</article>
"""
        coup_topic = "los cupones están en el sitio oficial"
        coup_body = f"""
<article class="pw">
  <span class="eyebrow" style="color:var(--acd)">Códigos</span>
  <h1>Cupones: no en el título de este dest</h1>
  <p class="lead">Este dest no imprime códigos de invitación en el título ni en la portada. Si Kakobuy publica un código, está después del login en {official}.</p>
  {fig_off}
  <p>La dirección sigue siendo una {fp}. Destino en el estimador: {dest_zh}.</p>
  <p><a class="btn" href="{official}">Sitio oficial</a> <a class="btn btn--ghost" href="{catalog}">Catálogo</a></p>
</article>
"""
        sheet_topic = f"el catálogo y cómo lo usas desde {dest}"
        sheet_body = f"""
<article class="pw">
  <span class="eyebrow" style="color:var(--acd)">Spreadsheet</span>
  <h1>Kakobuy Spreadsheet es un catálogo, no una tabla</h1>
  <p class="lead">Fichas con foto, marca y enlace de tienda. Treinta y tres categorías como en w2clinks.</p>
  {fig_sheet}
  <p>Busca en inglés (sneakers, hoodie, jacket). La dirección en este dest es una {fp}.</p>
  <p><a class="btn" href="{catalog}">Abrir el catálogo</a> <a class="btn btn--ghost" href="{guide}">Guía</a></p>
</article>
"""
    elif loc == "fr":
        guide_topic = f"comment tu passes la première commande depuis {dest}"
        guide_body = f"""
<article class="pw">
  <span class="eyebrow" style="color:var(--acd)">Guide</span>
  <h1>Première commande Kakobuy, depuis {dest_e}</h1>
  <p class="lead">Tu copies le lien, tu le colles dans l’agent, tu vérifies la photo d’entrepôt, tu regroupes, tu choisis destination {dest_zh}. L’adresse est une {fp}.</p>
  {fig_off}
  <h2>1. Ouvre une fiche sur w2clinks</h2>
  <p>Une des trente-trois catégories, photo et lien boutique. C’est un catalogue, pas un fichier Excel.</p>
  {fig_sheet}
  <h2>2. Colle-le sur le site officiel</h2>
  <p>Paiements et tickets restent sur {official}. Ce guide ne voit pas ton compte. Si la recherche ne lit pas le lien, le site officiel a un formulaire manuel.</p>
  {fig_diy}
  <h2>3. Photo, puis regrouper, puis envoyer</h2>
  <p>Les chiffres de fret viennent seulement de {est} : choisis le pays, pas ce nom d’hôte. {escape(_storage("fr"))}</p>
  <h2>Neuf statuts, trois écrans</h2>
  <p>D’abord le produit plus le trajet intérieur jusqu’à l’entrepôt. L’international après. « Pourquoi c’est bloqué ? » presque toujours : mauvais écran — commandes, puis entrepôt, puis colis.</p>
  <h2>Premier haul : plat d’abord</h2>
  <p>T-shirts, shorts, bijoux pour le premier tour. Doudounes, sacs, casquettes pour le second. Électronique souvent lithium : vérifie la ligne sur le site officiel.</p>
  <p><a class="btn" href="{guide}">Guide</a> <a class="btn btn--ghost" href="{ship}">Plan de livraison</a></p>
</article>
"""
        ship_topic = f"livraison et douane depuis {dest}"
        ship_body = f"""
<article class="pw">
  <span class="eyebrow" style="color:var(--acd)">Livraison</span>
  <h1>Expédier vers {dest_e} : estimateur, volume, douane</h1>
  <p class="lead">Destination {dest_zh}, pas EU. L’adresse est une {fp}.</p>
  {fig_off}
  <h2>L’estimateur officiel fait foi</h2>
  <p>Le {escape(DATE)} les chiffres de fret viennent seulement de {est}. Ce guide n’invente ni ligne, ni transit, ni montant. Source : <a href="{customs_url}" rel="noopener">{customs}</a>.</p>
  <h2>Balance contre volume</h2>
  <p>Beaucoup de lignes facturent le max entre balance et L×W×H (cm) / 8000. Exemple : 40×40×3 cm font 4800 cm³, divisés par 8000 font 600 g de volume pour 200 g réels. Aucun prix SKU dans cet HTML.</p>
  {fig_vol}
  <h2>Regrouper n’est pas un tutoriel douane</h2>
  <p>Plusieurs pièces d’entrepôt dans un carton peuvent réduire les lignes internationales. Ce que tu déclares en douane est sur l’envoi officiel, pas sur cette page.</p>
  <h2>Restricted n’est pas un avis de douane</h2>
  <p>Fiches sans prix ou un formulaire manuel signifient : le lien source n’est pas achetable via l’agent. Tabac, alcool et médicaments ne voyagent pas.</p>
  <h2>Photos d’entrepôt avant la ligne</h2>
  <p>Les photos QC arrivent dans l’app quand la pièce est en entrepôt. Angles extra souvent payants. Réclamer est plus simple tant qu’elle y est encore.</p>
  <h2>L’adresse sur ce dest</h2>
  <p>L’adresse est une {fp}. Ce format va sur l’envoi officiel, pas comme astuce sur cette page.</p>
  <p><a class="btn" href="{est}">Site officiel Kakobuy</a> <a class="btn btn--ghost" href="{help_h}">Aide</a></p>
</article>
"""
        legit_topic = f"Kakobuy est un vrai agent depuis {dest}"
        legit_body = f"""
<article class="pw">
  <span class="eyebrow" style="color:var(--acd)">Check</span>
  <h1>Kakobuy est-il un vrai agent d’achat ?</h1>
  <p class="lead">kakobuy.com est le site officiel. kakobuydocs.com est notre hub, pas un territoire douanier. Ce dest n’est pas Kakobuy.</p>
  {fig_off}
  <p>On n’invente ni délai de stockage ni tarif. {escape(_storage("fr"))} Commandes seulement sur {official}.</p>
  <p>L’adresse sur ce dest est une {fp}.</p>
  <p><a class="btn" href="{guide}">Guide</a> <a class="btn btn--ghost" href="{help_h}">Aide</a></p>
</article>
"""
        coup_topic = "les codes sont sur le site officiel"
        coup_body = f"""
<article class="pw">
  <span class="eyebrow" style="color:var(--acd)">Codes</span>
  <h1>Codes : pas dans le titre de ce dest</h1>
  <p class="lead">Ce dest n’imprime pas de codes d’invitation dans le titre ni sur la page d’accueil. Si Kakobuy publie un code, il est après le login sur {official}.</p>
  {fig_off}
  <p>L’adresse reste une {fp}. Destination dans l’estimateur : {dest_zh}.</p>
  <p><a class="btn" href="{official}">Site officiel</a> <a class="btn btn--ghost" href="{catalog}">Catalogue</a></p>
</article>
"""
        sheet_topic = f"le catalogue et comment tu l’utilises depuis {dest}"
        sheet_body = f"""
<article class="pw">
  <span class="eyebrow" style="color:var(--acd)">Spreadsheet</span>
  <h1>Kakobuy Spreadsheet est un catalogue, pas une grille</h1>
  <p class="lead">Fiches avec photo, marque et lien boutique. Trente-trois catégories comme sur w2clinks.</p>
  {fig_sheet}
  <p>Cherche en anglais (sneakers, hoodie, jacket). L’adresse sur ce dest est une {fp}.</p>
  <p><a class="btn" href="{catalog}">Ouvrir le catalogue</a> <a class="btn btn--ghost" href="{guide}">Guide</a></p>
</article>
"""
    elif loc == "nl":
        guide_topic = f"hoe je de eerste bestelling vanuit {dest} plaatst"
        guide_body = f"""
<article class="pw">
  <span class="eyebrow" style="color:var(--acd)">Handleiding</span>
  <h1>Eerste Kakobuy-bestelling, vanuit {dest_e}</h1>
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
  <p><a class="btn" href="{guide}">Handleiding</a> <a class="btn btn--ghost" href="{ship}">Verzendplan</a></p>
</article>
"""
        ship_topic = f"verzending en douane vanuit {dest}"
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
  <p>QC-foto’s landen in de app zodra het stuk in het magazijn is. Extra hoeken zijn vaak betaald. Reclame is makkelijker zolang het er nog ligt.</p>
  <h2>Het adres op dit dest</h2>
  <p>Het afleveradres is een {fp}. Dat formaat hoort op de officiële zending, niet als truc op deze pagina.</p>
  <p><a class="btn" href="{est}">Officiële Kakobuy-site</a> <a class="btn btn--ghost" href="{help_h}">Hulp</a></p>
</article>
"""
        legit_topic = f"is Kakobuy een echte agent vanuit {dest}"
        legit_body = f"""
<article class="pw">
  <span class="eyebrow" style="color:var(--acd)">Check</span>
  <h1>Is Kakobuy een echte inkoopagent?</h1>
  <p class="lead">kakobuy.com is de officiële site. kakobuydocs.com is onze hub, geen douanegebied. Dit dest is Kakobuy niet.</p>
  {fig_off}
  <p>We verzinnen geen opslagvenster en geen tarief. {escape(_storage("nl"))} Bestellingen alleen via {official}.</p>
  <p>Het afleveradres op dit dest is een {fp}.</p>
  <p><a class="btn" href="{guide}">Handleiding</a> <a class="btn btn--ghost" href="{help_h}">Hulp</a></p>
</article>
"""
        coup_topic = "kortingscodes staan op de officiële site"
        coup_body = f"""
<article class="pw">
  <span class="eyebrow" style="color:var(--acd)">Codes</span>
  <h1>Kortingscodes: niet in de titel van dit dest</h1>
  <p class="lead">Dit dest drukt geen uitnodigingscodes in de titel of op de homepage. Als Kakobuy een code publiceert, staat die na het inloggen op {official}.</p>
  {fig_off}
  <p>Het afleveradres blijft een {fp}. Bestemming in de schatter: {dest_zh}.</p>
  <p><a class="btn" href="{official}">Officiële site</a> <a class="btn btn--ghost" href="{catalog}">Catalogus</a></p>
</article>
"""
        sheet_topic = f"de catalogus en hoe je hem vanuit {dest} gebruikt"
        sheet_body = f"""
<article class="pw">
  <span class="eyebrow" style="color:var(--acd)">Spreadsheet</span>
  <h1>Kakobuy Spreadsheet is een catalogus, geen raster</h1>
  <p class="lead">Kaarten met foto, merk en shoplink. Drieëndertig categorieën zoals op w2clinks.</p>
  {fig_sheet}
  <p>Zoek in het Engels (sneakers, hoodie, jacket). Het afleveradres op dit dest is een {fp}.</p>
  <p><a class="btn" href="{catalog}">Catalogus openen</a> <a class="btn btn--ghost" href="{guide}">Handleiding</a></p>
</article>
"""
    else:
        guide_topic = f"how you place the first order from {dest}"
        guide_body = f"""
<article class="pw">
  <span class="eyebrow" style="color:var(--acd)">Guide</span>
  <h1>First Kakobuy order, from {dest_e}</h1>
  <p class="lead">Copy the shop link, paste it into the agent, check the warehouse photo, consolidate, then pick destination {dest_zh}. The delivery address uses a {fp}.</p>
  {fig_off}
  <h2>1. Open a card on w2clinks</h2>
  <p>One of the thirty-three categories, a photo and the shop link. That is the catalogue, not an Excel file.</p>
  {fig_sheet}
  <h2>2. Paste it on the official site</h2>
  <p>Payment and tickets stay on {official}. This desk cannot see your account. If search does not read the link, the official site has a manual order form.</p>
  {fig_diy}
  <h2>3. Photo, then consolidate, then ship</h2>
  <p>Freight figures come only from kakobuy.com/tools/estimate — pick the dest country, not this hostname. {escape(_storage("en"))}</p>
  <h2>Nine statuses, three screens</h2>
  <p>First the product plus domestic freight to the warehouse. International later. “Why is it stuck?” is almost always the wrong screen — orders, then warehouse, then the parcel.</p>
  <h2>First haul: flat first</h2>
  <p>T-shirts, shorts, jewelry for the first round. Down, bags, hats for the second. Electronics often mean lithium: check the line on the official site.</p>
  <p><a class="btn" href="{guide}">Guide</a> <a class="btn btn--ghost" href="{ship}">Shipping plan</a></p>
</article>
"""
        ship_topic = f"shipping and customs from {dest}"
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
  <p>QC photos land in the app once the piece is in the warehouse. Extra angles are often paid. Disputes are easier while it is still there.</p>
  <h2>The address on this dest</h2>
  <p>The delivery address uses a {fp}. That format belongs on the official shipment, not as a trick on this page.</p>
  <p><a class="btn" href="{est}">Official Kakobuy site</a> <a class="btn btn--ghost" href="{help_h}">Help</a></p>
</article>
"""
        legit_topic = f"is Kakobuy a real agent from {dest}"
        legit_body = f"""
<article class="pw">
  <span class="eyebrow" style="color:var(--acd)">Check</span>
  <h1>Is Kakobuy a real purchasing agent?</h1>
  <p class="lead">kakobuy.com is the official site. kakobuydocs.com is our hub, not a customs territory. This dest is not Kakobuy.</p>
  {fig_off}
  <p>This desk publishes no invented storage window and no invented tariff. {escape(_storage("en"))} Orders only through {official}.</p>
  <p>The delivery address on this dest uses a {fp}.</p>
  <p><a class="btn" href="{guide}">Guide</a> <a class="btn btn--ghost" href="{help_h}">Help</a></p>
</article>
"""
        coup_topic = "coupons live on the official site"
        coup_body = f"""
<article class="pw">
  <span class="eyebrow" style="color:var(--acd)">Codes</span>
  <h1>Coupons: not in this dest title</h1>
  <p class="lead">This dest does not print invite codes in the title or on the homepage. If Kakobuy publishes a code, it lives on {official} after you log in.</p>
  {fig_off}
  <p>The delivery address still uses a {fp}. Estimator destination: {dest_zh}.</p>
  <p><a class="btn" href="{official}">Official site</a> <a class="btn btn--ghost" href="{catalog}">Catalogue</a></p>
</article>
"""
        sheet_topic = f"the catalogue and how you use it from {dest}"
        sheet_body = f"""
<article class="pw">
  <span class="eyebrow" style="color:var(--acd)">Spreadsheet</span>
  <h1>Kakobuy Spreadsheet is a catalogue, not a grid</h1>
  <p class="lead">Cards with a photo, a brand and the shop link. Thirty-three categories, the same wall as w2clinks.</p>
  {fig_sheet}
  <p>Search in English (sneakers, hoodie, jacket). The delivery address on this dest uses a {fp}.</p>
  <p><a class="btn" href="{catalog}">Open the catalogue</a> <a class="btn btn--ghost" href="{guide}">Guide</a></p>
</article>
"""
    return {
        "guide": (p["guide"], guide_topic, guide_body),
        "ship": (p["ship"], ship_topic, ship_body),
        "legit": ("/is-kakobuy-legit/", legit_topic, legit_body),
        "coupons": ("/kakobuy-coupons/", coup_topic, coup_body),
        "spreadsheet": ("/kakobuy-spreadsheet/", sheet_topic, sheet_body),
    }


def build_inner(key: str, name: str) -> str:
    p = PACKS[key]
    desk = desk_for(key)
    href, topic, body = _inner_pages(key)[name]
    return cms_shell(
        desk, page_title(desk, topic),
        f"Independent Kakobuy {name} for {p['dest_label']}.",
        f"https://{p['host']}{href}", [], body, href,
    )


SHEET_EXPLAIN = (
    "not an Excel file",
    "ei ole Excel-tiedosto",
    "no es un archivo Excel",
    "n’est pas un fichier Excel",
    "geen Excel-bestand",
)


def _assert_ok(html: str, page: str, key: str) -> None:
    p = PACKS[key]
    desk = desk_for(key)
    if page == "nf":
        if p["not_found_tab"] not in html or MAIL not in html:
            raise SystemExit(f"{key} nf chrome")
        if f"{p['not_found_tab']} | Kakobuy Spreadsheet" not in html:
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
    if page == "home":
        err = [e for e in err if not e.startswith("faq count")]
        if page_title(desk, p["home_topic"]) not in html:
            err.append("home title")
        if p["fingerprint"] not in html:
            err.append("fingerprint")
        if not any(tok in html for tok in SHEET_EXPLAIN):
            err.append("sheet-explain")
        if "cat-30-shoes.png" not in html or "w2clinks.com/spreadsheet/kakobuy" not in html:
            err.append("W2C cats")
        if html.count('class="cat"') < 33:
            err.append("W2C cat wall < 33")
        if MAIL not in html:
            err.append("footer mail")
        if 'id="local"' in html or "/api/products/" in html:
            err.append("ops dump")
        if html.count('class="sg-faq"') >= 8:
            err.append("home faq dump")
        if 'class="fig"' not in html:
            err.append("photos")
        for sid in ("shots", "states", "restricted"):
            if f'id="{sid}"' not in html:
                err.append(f"missing #{sid}")
        if p["loc"] != "en" and "Official kakobuy.com, 6 Oct" in html:
            err.append("english fig caption")
        for alien in p["aliens"]:
            if alien in html:
                err.append(f"alien {alien}")
        for tok in INVITES:
            if tok in html:
                err.append(f"invite {tok}")
        if re.search(r"58 l[ií]neas", html, re.I) or re.search(r"23[,.]81\s*USD", html, re.I):
            err.append("58-line / 23.81 leak")
    if page == "help" and p["fingerprint"] not in html:
        err.append("help fingerprint")
    if page == "help":
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
    if page in ("guide", "ship", "legit", "coupons", "spreadsheet"):
        if "orientdig" in html.lower():
            err.append("orientdig leftover")
        for tok in INVITES:
            if tok in html:
                err.append(f"invite {tok}")
        if page in ("guide", "ship") and p["fingerprint"] not in html:
            err.append(f"{page} fingerprint")
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
    theme = OUT / "shared" / "themes" / "kakobuy-theme.css"
    theme.parent.mkdir(parents=True, exist_ok=True)
    theme.write_text(
        "/* Kakobuy country dest — official coral from kakobuy.com */\n"
        f":root {{ --primary: {ACC}; --primary-dark: {ACC_DARK}; --primary-soft: {SOFT}; --nav-dark: #0f172a; }}\n",
        encoding="utf-8",
    )
    return theme


def generate(key: str) -> dict[str, Path]:
    p = PACKS[key]
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
    _run(client, f"cp -a '{gsc}' '/www/backup/kakobuy-{key}-gsc-about-{stamp}.conf'")
    Path(f"/tmp/kakobuy-{key}-gsc.conf").write_text("".join(keep), encoding="utf-8")
    sftp.put(f"/tmp/kakobuy-{key}-gsc.conf", gsc)
    print(key, "stripped", stripped, "CMS-page home 301s")
    _reload_nginx(client)


def _map_legacy_english_cms(client, sftp, key: str) -> None:
    """301 leftover English CMS slugs onto dest slugs; drop leftover OrientDig dirs."""
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
    _run(client, f"mkdir -p /www/backup; cp -a '{gsc}' '/www/backup/kakobuy-{key}-gsc-legacy-{stamp}.conf' 2>/dev/null || true")
    Path(f"/tmp/kakobuy-{key}-gsc-legacy.conf").write_text(new, encoding="utf-8")
    sftp.put(f"/tmp/kakobuy-{key}-gsc-legacy.conf", gsc)
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
    listing = _run(client, f"find '{ext}' -maxdepth 1 -name '*.conf' -print")
    files = [ln.strip() for ln in listing.splitlines() if ln.strip().endswith(".conf")]
    # kakobuy-coupons is left out on purpose: origin 301s it onto the ranked /kakobuy-coupon/.
    unstick = {
        "start",
        p["help"].strip("/"),
        p["news"].strip("/"),
        p["about"].strip("/"),
        p["catalog"].strip("/"),
        "how-to-use-kakobuy",
        "kakobuy-shipping",
        "is-kakobuy-legit",
        "kakobuy-spreadsheet",
    }
    if key in PHP_KEYS:
        unstick.update({"guide", "spreadsheet"})
    faq_src = {
        "/faq", "/faq/",
        "/kakobuy-invite-code", "/kakobuy-invite-code/",
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
            _run(client, f"cp -a '{remote}' '/www/backup/kakobuy-{key}-{Path(remote).name}-{stamp}.conf'")
            tmp = Path(f"/tmp/kakobuy-{key}-{Path(remote).name}")
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
        Path(f"/tmp/kakobuy-{key}-gsc-faq.conf").write_text(body + add, encoding="utf-8")
        sftp.put(f"/tmp/kakobuy-{key}-gsc-faq.conf", gsc)
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
    marker = f'X-Desk "kakobuy-{key}-independent"'
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
        add_header X-Desk "kakobuy-{key}-independent" always;
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
    _run(client, f"cp -a '{vhost}' '/www/backup/kakobuy-{key}-nginx-{stamp}.conf'")
    tmp = Path(f"/tmp/kakobuy-{key}.conf")
    tmp.write_text(text, encoding="utf-8")
    sftp.put(str(tmp), vhost)
    _reload_nginx(client)


def _php_legacy_maps(key: str) -> list[tuple[str, str]]:
    p = PACKS[key]
    cat, help_h, guide, ship = p["catalog"], p["help"], p["guide"], p["ship"]
    legit, coup = "/is-kakobuy-legit/", "/kakobuy-coupons/"
    return [
        ("/guides/customs", ship),
        ("/guides/costs", ship),
        ("/guides/payment", guide),
        ("/guides/tracking", ship),
        ("/guides/coupon", coup),
        ("/guides/is-safe", legit),
        ("/guides/first-order", guide),
        ("/guides/vs-pandabuy", legit),
        ("/guides/shipping", ship),
        ("/guide/shipping", ship),
        ("/guide/first-order", guide),
        ("/guide/customs", ship),
        ("/guide/coupon", coup),
        ("/guide/is-safe", legit),
        ("/guide", guide),
        ("/spreadsheet", cat),
        ("/faq", help_h),
    ]


def _cutover_php_vhost(client, sftp, key: str) -> None:
    """Move the five PHP ccTLDs off kakobuy-hub-skip onto a static dest wwwroot."""
    if key not in PHP_KEYS:
        return
    host = PACKS[key]["host"]
    if host not in PHP_HOSTS:
        raise SystemExit(f"cutover host mismatch {host}")
    dest_root = f"/www/wwwroot/{host}"
    vhost = f"/www/server/panel/vhost/nginx/{host}.conf"
    rewrite = f"/www/server/panel/vhost/rewrite/{host}.conf"
    with sftp.open(vhost, "r") as fh:
        text = fh.read().decode()
    stamp = time.strftime("%Y%m%d-%H%M%S")
    _run(client, f"mkdir -p /www/backup '{dest_root}'; cp -a '{vhost}' '/www/backup/kakobuy-{key}-php-cutover-{stamp}.conf'")
    _run(client, f"cp -a '{rewrite}' '/www/backup/kakobuy-{key}-php-rewrite-{stamp}.conf' 2>/dev/null || true")
    text = text.replace("/www/wwwroot/kakobuy-hub-skip", dest_root)
    text = text.replace("index index.php;", "index index.html;")
    text = re.sub(r"\n[ \t]*include enable-php-74\.conf;\s*", "\n", text)
    text = re.sub(r"\n[ \t]*location = /index\.html\s*\{[^}]*\}\s*", "\n", text)
    text = re.sub(r"\n[ \t]*location = /index\.htm\s*\{[^}]*\}\s*", "\n", text)
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
        else:
            raise SystemExit(f"{host} missing error_page 497 needle for 404 inject")
    if "/www/wwwroot/kakobuy-hub-skip" in text or "kakobuy-hub-skip" in text:
        raise SystemExit(f"refusing {host} vhost still on lite/public")
    if "enable-php-74.conf" in text:
        raise SystemExit(f"refusing {host} still includes php74")
    Path(f"/tmp/kakobuy-{key}-cutover.conf").write_text(text, encoding="utf-8")
    sftp.put(f"/tmp/kakobuy-{key}-cutover.conf", vhost)
    catch = (
        "location / {\n"
        "    try_files $uri $uri/ $uri/index.html =404;\n"
        '    add_header Strict-Transport-Security "max-age=31536000" always;\n'
        '    add_header Cache-Control "private, no-cache, must-revalidate" always;\n'
        f'    add_header X-Desk "kakobuy-{key}-independent" always;\n'
        "}\n"
    )
    Path(f"/tmp/kakobuy-{key}-rewrite.conf").write_text(catch, encoding="utf-8")
    sftp.put(f"/tmp/kakobuy-{key}-rewrite.conf", rewrite)
    _run(client, f"mkdir -p '{dest_root}'")
    chk = _run(client, "nginx -t")
    print(key, "php cutover nginx -t", chk)
    if "successful" not in chk.lower() and "ok" not in chk.lower():
        raise SystemExit(f"nginx -t failed after {host} cutover")
    print(key, "cut over vhost root to", dest_root)
    _reload_nginx(client)


def _map_php_legacy(client, sftp, key: str) -> None:
    """301 leftover PHP /guide /spreadsheet /faq onto dest slugs."""
    if key not in PHP_KEYS:
        return
    p = PACKS[key]
    host = p["host"]
    root = f"/www/wwwroot/{host}"
    wanted: dict[str, str] = {}
    for src, dest in _php_legacy_maps(key):
        wanted[src] = dest
        if not src.endswith("/"):
            wanted[src + "/"] = dest
        _run(client, f"rm -rf '{root}{src}'")
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
    stamp = time.strftime("%Y%m%d-%H%M%S")
    _run(client, f"mkdir -p /www/backup '{Path(gsc).parent}'; touch '{gsc}'")
    if new != (raw or ""):
        _run(client, f"cp -a '{gsc}' '/www/backup/kakobuy-{key}-gsc-php-legacy-{stamp}.conf' 2>/dev/null || true")
        Path(f"/tmp/kakobuy-{key}-gsc-php-legacy.conf").write_text(new, encoding="utf-8")
        sftp.put(f"/tmp/kakobuy-{key}-gsc-php-legacy.conf", gsc)
        print(key, "php leftover 301s", len(wanted))
        _reload_nginx(client)
    else:
        print(key, "php leftover 301s already mapped")


def _fix_twins(client, sftp) -> None:
    stamp = time.strftime("%Y%m%d-%H%M%S")
    for twin, target in TWINS.items():
        vhost = f"/www/server/panel/vhost/nginx/{twin}.conf"
        raw = _run(client, f"cat '{vhost}' 2>/dev/null || true")
        if not raw:
            print("skip missing twin vhost", twin)
            continue
        want = f"    location / {{ return 301 https://{target}$request_uri; }}"
        old = f"    location / {{ return 301 https://{target}/; }}"
        old2 = f"    location / {{ return 301 https://{target}; }}"
        if want in raw:
            print("twin catch-all already $request_uri", twin)
        elif old in raw or old2 in raw:
            _run(client, f"cp -a '{vhost}' '/www/backup/kakobuy-twin-{twin}-{stamp}.conf'")
            raw = raw.replace(old, want).replace(old2, want)
            Path(f"/tmp/kakobuy-twin-{twin}.conf").write_text(raw, encoding="utf-8")
            sftp.put(f"/tmp/kakobuy-twin-{twin}.conf", vhost)
            print("twin catch-all now $request_uri", twin)
        else:
            print("WARN twin catch-all needle missing", twin)
        extra = TWIN_EXTRA.get(twin) or []
        pdest = next(p for p in PACKS.values() if p["host"] == target)
        wanted: dict[str, str] = {}
        for src, dest in extra:
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
        vhost_new = raw
        vhost_changed = False
        for path, dest in wanted.items():
            pat = re.compile(
                rf"(location = {re.escape(path)} \{{ return 301 )https://{re.escape(target)}[^\s;]*"
            )
            vhost_new, n = pat.subn(rf"\g<1>https://{target}{dest}", vhost_new)
            if n:
                vhost_changed = True
        if vhost_changed:
            _run(client, f"cp -a '{vhost}' '/www/backup/kakobuy-twin-vhost-maps-{twin}-{stamp}.conf'")
            Path(f"/tmp/kakobuy-twin-{twin}.conf").write_text(vhost_new, encoding="utf-8")
            sftp.put(f"/tmp/kakobuy-twin-{twin}.conf", vhost)
            print("rewrote twin vhost exact maps", twin)
            raw = vhost_new
        gsc = f"/www/server/panel/vhost/nginx/extension/{twin}/gsc-redirects.conf"
        graw = _run(client, f"cat '{gsc}' 2>/dev/null || true")
        if graw and f"https://{twin}" in graw:
            _run(client, f"cp -a '{gsc}' '/www/backup/kakobuy-twin-gsc-{twin}-{stamp}.conf'")
            graw = graw.replace(f"https://{twin}", f"https://{target}")
            Path(f"/tmp/kakobuy-twin-gsc-{twin}.conf").write_text(graw, encoding="utf-8")
            sftp.put(f"/tmp/kakobuy-twin-gsc-{twin}.conf", gsc)
            print("retargeted twin gsc host", twin, "->", target)
            graw = _run(client, f"cat '{gsc}'")
        graw = re.sub(r"\}(\s*)location\s+=", "}\nlocation =", graw or "")
        if graw and not graw.endswith("\n"):
            graw += "\n"
        seen: set[str] = set()
        out: list[str] = []
        loc_re = re.compile(r"location\s+=\s+(\S+)\s*\{")
        file_changed = False
        for ln in graw.splitlines(True):
            m = loc_re.search(ln)
            if m and m.group(1) in wanted:
                path = m.group(1)
                if path in seen:
                    file_changed = True
                    continue
                want = f"location = {path} {{ return 301 https://{target}{wanted[path]}; }}\n"
                prefix = ln[: m.start()] if m.start() else ""
                if prefix.strip() and not prefix.endswith("\n"):
                    out.append(prefix.rstrip() + "\n")
                out.append(want)
                seen.add(path)
                if ln.strip() != want.strip():
                    file_changed = True
                continue
            out.append(ln)
        for path, dest in wanted.items():
            if path not in seen:
                out.append(f"location = {path} {{ return 301 https://{target}{dest}; }}\n")
                seen.add(path)
                file_changed = True
        if file_changed:
            _run(client, f"mkdir -p '{Path(gsc).parent}'; cp -a '{gsc}' '/www/backup/kakobuy-twin-gsc-extra-{twin}-{stamp}.conf' 2>/dev/null || true")
            Path(f"/tmp/kakobuy-twin-gsc-{twin}.conf").write_text("".join(out), encoding="utf-8")
            sftp.put(f"/tmp/kakobuy-twin-gsc-{twin}.conf", gsc)
            print("rewrote twin path maps", twin, len(wanted))
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
    if loc == "fi":
        topic = "tämä artikkeli on korvattu"
        body = f"""
<article class="pw">
  <h1>Tämä artikkeli on korvattu</h1>
  <p class="lead">Aiempi versio ei kuulunut Kakobuylle. Ajantasainen opas on Start-sivulla. Toimitusosoitteessa on {fp}.</p>
  <p><a class="btn" href="/start/">Start</a> <a class="btn btn--ghost" href="{escape(p['guide'])}">Opas</a></p>
</article>
"""
    elif loc == "es":
        topic = "este artículo fue sustituido"
        body = f"""
<article class="pw">
  <h1>Este artículo fue sustituido</h1>
  <p class="lead">La versión anterior no era de Kakobuy. La guía actual está en Start. La dirección es una {fp}.</p>
  <p><a class="btn" href="/start/">Start</a> <a class="btn btn--ghost" href="{escape(p['guide'])}">Guía</a></p>
</article>
"""
    elif loc == "fr":
        topic = "cet article a été remplacé"
        body = f"""
<article class="pw">
  <h1>Cet article a été remplacé</h1>
  <p class="lead">La version précédente n’était pas Kakobuy. Le guide actuel est sur Start. L’adresse est une {fp}.</p>
  <p><a class="btn" href="/start/">Start</a> <a class="btn btn--ghost" href="{escape(p['guide'])}">Guide</a></p>
</article>
"""
    elif loc == "nl":
        topic = "dit artikel is vervangen"
        body = f"""
<article class="pw">
  <h1>Dit artikel is vervangen</h1>
  <p class="lead">De vorige versie hoorde niet bij Kakobuy. De huidige gids staat op Start. Het afleveradres is een {fp}.</p>
  <p><a class="btn" href="/start/">Start</a> <a class="btn btn--ghost" href="{escape(p['guide'])}">Handleiding</a></p>
</article>
"""
    else:
        topic = "this article was replaced"
        body = f"""
<article class="pw">
  <h1>This article was replaced</h1>
  <p class="lead">The previous version was not a Kakobuy dest page. The current guide is on Start. The delivery address uses a {fp}.</p>
  <p><a class="btn" href="/start/">Start</a> <a class="btn btn--ghost" href="{escape(p['guide'])}">Guide</a></p>
</article>
"""
    return cms_shell(
        desk, page_title(desk, topic),
        f"Replaced leftover article on {p['host']}.",
        f"https://{p['host']}{href}", [], body, href,
    )


def _ranked_floor(rel: str) -> int | None:
    for prefix, floor in RANKED:
        if rel.startswith(prefix.lstrip("/")):
            return floor
    return None


def _wrap_ranked(client, sftp, bak: str, root: str, key: str) -> None:
    """Wrap ranked inners in dest chrome; retire poisoned leftovers; leave the rest untouched."""
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
    seen: set[str] = set()
    for rel in rels:
        if rel in seen:
            continue
        seen.add(rel)
        if rel in skip or any(rel == p.rstrip("/") or rel.startswith(p) for p in WRAP_SKIP_PREFIXES):
            continue
        floor = _ranked_floor(rel)
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
        if any(tok in raw.lower() for tok in WRAP_POISON):
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
        local_tmp = Path("/tmp") / f"kakobuy-wrap-{key}-{rel.replace('/', '_')}"
        local_tmp.write_text(out, encoding="utf-8")
        sftp.put(str(local_tmp), remote)
        print("WRAP", rel, "in", len(raw), "out", len(out.encode("utf-8")))


def _put_if(sftp, local: Path, remote: str) -> None:
    if local.is_file():
        sftp.put(str(local), remote)
        print("PUT", remote, local.stat().st_size)
    else:
        print("WARN skip missing local asset", local)


def put(key: str) -> None:
    host = PACKS[key]["host"]
    if host in SKIP_PUT_HOSTS:
        raise SystemExit(f"refusing to PUT {host}")
    files = generate(key)
    p = PACKS[key]
    host = p["host"]
    client = _connect()
    stamp = time.strftime("%Y%m%d-%H%M%S")
    bak = f"/www/backup/kakobuy-{key}-cms-{stamp}"
    root = f"/www/wwwroot/{host}"
    overlay = _overlay(key)
    if host in SKIP_PUT_HOSTS or any(h in root for h in SKIP_PUT_HOSTS):
        raise SystemExit(f"refusing hub PUT {root}")
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
    if key in PHP_KEYS:
        _cutover_php_vhost(client, sftp, key)
    _harden_catchall(client, sftp, key)
    _strip_cms_home_301s(client, sftp, key)
    _map_legacy_english_cms(client, sftp, key)
    _map_faq_to_help(client, sftp, key)
    if key in PHP_KEYS:
        _map_php_legacy(client, sftp, key)
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
        sftp.put(str(local), remote)
        print("PUT", remote, local.stat().st_size)
    theme = _write_theme()
    sftp.put(str(theme), f"{root}/assets/css/kakobuy-theme.css")
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


GUIDE_MARK = {
    "fi": "Ensimmäinen Kakobuy-tilaus",
    "es": "Primer pedido Kakobuy",
    "fr": "Première commande Kakobuy",
    "nl": "Eerste Kakobuy-bestelling",
    "en": "First Kakobuy order",
}
ABOUT_MARK = {
    "fi": "Riippumaton sivusto Kakobuysta",
    "es": "Un sitio independiente sobre Kakobuy",
    "fr": "Un site indépendant sur Kakobuy",
    "nl": "Een onafhankelijke site over Kakobuy",
    "en": "An independent site about Kakobuy",
}


def _ship_mark(p: dict) -> str:
    return {
        "fi": "Toimitus Suomeen",
        "es": f"Enviar a {p['dest_label']}",
        "fr": f"Expédier vers {p['dest_label']}",
        "nl": f"Verzenden naar {p['dest_label']}",
    }.get(p["loc"], "Shipping to")


SISTER_PAIRS = (
    ("https://kakospreadsheet.ca/", "kakobuy.fi"),
    ("https://kakobuy.fi/", "kakospreadsheet.ca"),
    ("https://kakospreadsheet.es/", "kakospreadsheet.fr"),
    ("https://kakospreadsheet.fr/", "kakospreadsheet.es"),
    ("https://kakospreadsheet.nl/", "kakospreadsheet.fr"),
    ("https://kakospreadsheet.fr/", "kakospreadsheet.nl"),
)


def live_check(key: str | None = None) -> None:
    import ssl
    import urllib.error
    import urllib.request

    keys = [key] if key else list(PACKS)
    ctx = ssl.create_default_context()
    https = urllib.request.HTTPSHandler(context=ctx)

    class NR(urllib.request.HTTPRedirectHandler):
        def redirect_request(self, req, fp, code, msg, headers, newurl):
            return None

    def fetch(url, follow=True):
        req = urllib.request.Request(
            url, headers={"User-Agent": "kakobuy-cms/1.0", "Cache-Control": "no-cache"},
        )
        opener = urllib.request.build_opener(*([https] if follow else [https, NR()]))
        try:
            with opener.open(req, timeout=25) as resp:
                return resp.status, resp.geturl(), resp.headers.get("Location") or "", resp.read()
        except urllib.error.HTTPError as e:
            return e.code, url, e.headers.get("Location") or "", e.read() if e.fp else b""
        except (urllib.error.URLError, OSError) as e:
            return 0, url, "", str(e).encode()

    fail = 0
    dest_hosts = [PACKS[k]["host"] for k in PACKS]
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
            (f"https://{host}{p['guide']}", "guide", True),
            (f"https://{host}{p['ship']}", "ship", True),
            (f"https://{host}/is-kakobuy-legit/", "legit", False),
            (f"https://{host}/kakobuy-coupons/", "coupons", False),
        ]
        for url, kind, need_fp in checks:
            follow = kind in ("home", "start", "guide", "ship", "legit", "coupons")
            code, final, loc, body = fetch(url, follow=follow)
            html = body.decode("utf-8", "replace")
            print(k, kind, code, "bytes", len(body), "loc", loc or final)
            if any(h in (final or "") or h in (loc or "") for h in SKIP_PUT_HOSTS):
                print(" FAIL 301 into hub"); fail += 1
            sisters = [h for h in dest_hosts if h != host]
            if any(s in (final or "") or s in (loc or "") for s in sisters):
                print(" FAIL 301 into sister dest"); fail += 1
            if code != 200:
                print(" FAIL status"); fail += 1
            if "orientdig" in html.lower() or "warum sollte ich lieferungen" in html.lower():
                print(" FAIL orientdig leftover"); fail += 1
            for tok in INVITES:
                if tok in html:
                    print(" FAIL invite"); fail += 1
            if re.search(r"58 l[ií]neas", html, re.I) or re.search(r"23[,.]81\s*USD", html, re.I):
                print(" FAIL 58-line / 23.81"); fail += 1
            if LOGO not in html:
                print(" FAIL logo"); fail += 1
            if f'lang="{p["lang"]}"' not in html:
                print(" FAIL lang"); fail += 1
            if 'href="/start/"' not in html or 'href="/">Start' in html:
                print(" FAIL Start href"); fail += 1
            if need_fp and p["fingerprint"] not in html:
                print(" FAIL fingerprint"); fail += 1
            if kind in ("home", "start"):
                if page_title(desk, p["home_topic"]) not in html:
                    print(" FAIL title"); fail += 1
                if p["dest_zh"] not in html:
                    print(" FAIL dest zh"); fail += 1
                if "cat-30-shoes.png" not in html:
                    print(" FAIL cats"); fail += 1
                if html.count('class="sg-faq"') >= 8:
                    print(" FAIL faq dump"); fail += 1
                if "/api/products/" in html:
                    print(" FAIL api dump"); fail += 1
                for sid in ("shots", "states", "restricted"):
                    if f'id="{sid}"' not in html:
                        print(" FAIL missing #", sid, sep=""); fail += 1
                if p["loc"] != "en" and "Official kakobuy.com, 6 Oct" in html:
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
            if kind == "catalog" and html.count('class="cat"') < 30:
                print(" FAIL catalog wall"); fail += 1
            if kind == "news" and "ItemList" not in html:
                print(" FAIL news ItemList"); fail += 1
            if kind == "about":
                if ABOUT_MARK.get(p["loc"], ABOUT_MARK["en"]) not in html:
                    print(" FAIL about copy"); fail += 1
                if (loc or "").rstrip("/") == f"https://{host}":
                    print(" FAIL about 301 home"); fail += 1
            if kind == "help":
                if "FAQPage" not in html:
                    print(" FAIL help FAQPage"); fail += 1
                if html.count("<h2>") < 5:
                    print(" FAIL help groups"); fail += 1
                if html.count('class="sg-faq"') < 12:
                    print(" FAIL help faq count"); fail += 1
            if kind == "catalog" and 'class="eq"' not in html:
                print(" FAIL catalog keys table"); fail += 1
            if kind == "catalog" and "oficial-diy.jpg" not in html:
                print(" FAIL catalog diy"); fail += 1
            if kind == "catalog" and html.count('class="fig"') < 3:
                print(" FAIL catalog figs"); fail += 1
        for old, want in (("/about/", p["about"]), ("/help/", p["help"]), ("/faq/", p["help"])):
            if want == old:
                continue
            code_ab, _, loc_ab, _ = fetch(f"https://{host}{old}", follow=False)
            print(k, "legacy", old, code_ab, loc_ab)
            if code_ab not in (301, 302, 308) or want.rstrip("/") not in (loc_ab or ""):
                print(f" FAIL leftover {old} not 301 to {want}"); fail += 1
            if old == "/about/":
                _, _, _, body_ab2 = fetch(f"https://{host}{old}", follow=True)
                html_ab = body_ab2.decode("utf-8", "replace")
                if "orientdig" in html_ab.lower() or any(tok in html_ab for tok in INVITES):
                    print(" FAIL leftover /about/ still OrientDig/invite"); fail += 1
        code, _, _, nf = fetch(f"https://{host}/this-page-does-not-exist-cms/", follow=True)
        nhtml = nf.decode("utf-8", "replace")
        print(k, "404", code)
        if code != 404:
            print(" FAIL 404"); fail += 1
        if f"{p['not_found_tab']} | Kakobuy Spreadsheet" not in nhtml:
            print(" FAIL 404 title"); fail += 1
        if k in PHP_KEYS:
            code_g, _, loc_g, _ = fetch(f"https://{host}/guide/shipping", follow=False)
            print(k, "legacy guide/shipping", code_g, loc_g)
            if code_g not in (301, 302, 308) or "/kakobuy-shipping" not in (loc_g or ""):
                print(" FAIL leftover /guide/shipping"); fail += 1
    if key is None:
        for a, b in SISTER_PAIRS:
            code, final, loc, _ = fetch(a, follow=False)
            if code in (301, 302, 308) and ((loc or "") and (b in (loc or "") or b in (final or ""))):
                print(" FAIL sister 301", a, loc); fail += 1
            else:
                print("sister indep", a, code)
    for twin, target in TWINS.items():
        code, _, loc, _ = fetch(f"https://{twin}/", follow=False)
        print("twin", twin, code, loc)
        if code not in (301, 302, 308) or target not in (loc or ""):
            print(" FAIL twin 301"); fail += 1
    code, _, loc, _ = fetch(f"https://{HUB}/", follow=False)
    print("hub", HUB, code, loc or HUB)
    if code != 200:
        print(" FAIL hub"); fail += 1
    if any(h in (loc or "") for h in dest_hosts):
        print(" FAIL hub collapsed into dest"); fail += 1
    code_t, _, loc_t, _ = fetch(f"https://{TIPS}/", follow=False)
    print("tips", TIPS, code_t, loc_t or TIPS)
    if any(h in (loc_t or "") for h in dest_hosts):
        print(" FAIL tips collapsed into dest"); fail += 1
    elif code_t in (301, 302, 308) and HUB not in (loc_t or ""):
        print(" WARN tips redirects somewhere other than", HUB)
    elif code_t not in (200, 301, 302, 308):
        print(" WARN tips status", code_t)
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
        z = req("GET", f"/zones?name={host}")
        zid = ((z.get("result") or [{}])[0] or {}).get("id")
        if not zid:
            print("CF zone missing", host, z.get("errors"))
            continue
        d = req("PATCH", f"/zones/{zid}/settings/development_mode", {"value": "on"})
        print("CF development_mode", host, d.get("success"))
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
        live_check(rest[0] if len(rest) == 1 and rest[0] in PACKS else None)
    elif cmd == "all":
        for k in rest:
            put(k)
        _cf_bust([PACKS[k]["host"] for k in rest])
        live_check()
    else:
        for k in rest:
            generate(k)
