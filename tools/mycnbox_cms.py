#!/usr/bin/env python3
"""MyCNBox country dests: UK, DE, ES, FR, NL, PL.

Gold IA: hipobuy.es. Gold brand: www.mycnbox.com (official orange #ff5501 / #e04c00).
Same-agent country hosts stay independent (no 301 between them). No Origin twins.
Hubs mycnbox.eu / mycnboxhaul.com are not overwritten: they keep their own CMS
and say "not a customs territory". Empty typo wwwroot mycnboxhual.com is skip-only.
Never PUT those hubs. Never put
dest hostnames like mycnbox.es in SKIP_PUT (substring trap on wwwroot path).

Official estimator is https://www.mycnbox.com/estimation/.
Warehouse: official Help FAQDetail?id=83 says 90 free warehouse days; name that
article and confirm it the morning you ship. Do not invent a second number.
Invite AABZKT stays off titles and dest homepages.

Usage:
    python3 tools/mycnbox_cms.py generate [uk de es fr nl pl]
    python3 tools/mycnbox_cms.py put [uk de es fr nl pl]     # dests in PACKS order
    python3 tools/mycnbox_cms.py twins                 # no-op while TWINS is empty
    python3 tools/mycnbox_cms.py live [uk|de|es|fr|nl|pl]
    python3 tools/mycnbox_cms.py all
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
from urllib.parse import quote_plus, urlparse

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
ASSETS = Path("/tmp/mycnbox-assets")
DATE = "6 Oct 2026"
AGENT = "MyCNBox"
OFFICIAL = "https://www.mycnbox.com/"
EST_PATH = "/estimation/"
EST = "https://www.mycnbox.com/estimation/"
HELP = "https://mycnbox.com/FAQDetail?id=83"
ACC = "#ff5501"
ACC_DARK = "#e04c00"
SOFT = "#fff4ed"
LOGIN_FG = "#fff"
MAIL = "cnfd85269032661@gmail.com"
HUBS = ("mycnbox.eu", "mycnboxhaul.com")
# Exact hub hostnames only. Never put dest TLDs like mycnbox.es in SKIP_PUT:
# that substring would skip a dest wwwroot path.
# mycnboxhual.com is an empty typo wwwroot (no nginx/DNS) — skip PUT, do not live-check.
SKIP_PUT_HOSTS = {"mycnbox.eu", "mycnboxhaul.com", "mycnboxhual.com"}
OFF_ORIGIN = ()  # none on Origin
DEST_MIN = 22000
CSS_V = "20261006q"
INVITES = ("AABZKT",)
LOGO = "mycnbox-logo.png"
THEME_CSS = "mycnbox-theme.css"
SHEET_SLUG = "mycnbox"
SHOTS = ("oficial.jpg", "oficial-diy.jpg", "catalogus.jpg", "catalogus-zoek.jpg", "volume-voorbeeld.jpg")
GUIDE_HREF = "/how-to-use-mycnbox/"
SHIP_HREF = "/mycnbox-shipping/"

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


DE_LABELS = {
    **EN_LABELS,
    "SNEAKERS": "Turnschuhe",
    "T-SHIRT": "T-Shirt",
    "SHIRT": "Hemd",
    "SHORTS": "Shorts",
    "VEST": "Weste",
    "LONG SLEEVED": "Langarm",
    "SWEATER": "Pullover",
    "SHAWL": "Schal / Tuch",
    "JACKET": "Jacke",
    "SHELL JACKET": "Shelljacke",
    "FLEECE JACKET": "Fleecejacke",
    "DOWN JACKETS": "Daunenjacke",
    "TROUSERS": "Hose",
    "FEMALE STYLE": "Damen",
    "Electronics": "Elektronik",
    "GLOVES": "Handschuhe",
    "BAG": "Tasche",
    "HAT": "Mütze",
    "JEWELRY": "Schmuck",
    "UNDERWEAR": "Unterwäsche",
    "BELT": "Gürtel",
    "KNEEPAD": "Knieschützer",
    "SOCKS": "Socken",
    "HEADGEAR": "Kopfbedeckung",
    "EARMUFF": "Ohrenschützer",
    "SCARF": "Schal",
    "GLASSES": "Brille",
    "WATCH": "Uhr",
    "CHILD": "Kinder",
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

PL_LABELS = {
    **EN_LABELS,
    "SNEAKERS": "Buty",
    "T-SHIRT": "T-shirt",
    "SHIRT": "Koszula",
    "SHORTS": "Szorty",
    "VEST": "Kamizelka",
    "LONG SLEEVED": "Długi rękaw",
    "SWEATER": "Sweter",
    "SHAWL": "Chusta",
    "JACKET": "Kurtka",
    "SHELL JACKET": "Kurtka shell",
    "FLEECE JACKET": "Polar",
    "DOWN JACKETS": "Kurtka puchowa",
    "TROUSERS": "Spodnie",
    "FEMALE STYLE": "Damskie",
    "Electronics": "Elektronika",
    "GLOVES": "Rękawiczki",
    "BAG": "Torba",
    "HAT": "Czapka",
    "JEWELRY": "Biżuteria",
    "UNDERWEAR": "Bielizna",
    "BELT": "Pasek",
    "KNEEPAD": "Ochraniacz kolana",
    "SOCKS": "Skarpety",
    "HEADGEAR": "Nakrycie głowy",
    "EARMUFF": "Nauszniki",
    "SCARF": "Szalik",
    "GLASSES": "Okulary",
    "WATCH": "Zegarek",
    "CHILD": "Dzieci",
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

CAT_NOTES_DE = {
    "SNEAKERS": "Sohle und Leisten auf den QC-Fotos prüfen, bevor du international buchst.",
    "SLIPPERS": "Leicht und flach. Füllt die Box, ohne das tarifierte Gewicht hart zu drücken.",
    "T-SHIRT": "Asiatische Schnitte sind oft schmaler. Brustweite in Zentimetern, nicht nur die Buchstabengröße.",
    "POLO": "Kragen und Piqué auf dem QC-Foto. Die weichen am häufigsten vom Katalogshot ab.",
    "SHIRT": "Ärmellänge und Schulternaht am Maßbandfoto, nicht am Buchstaben.",
    "SHORTS": "Leicht und flach: der einfachste Weg, ein Paket zu füllen.",
    "VEST": "Westen sind dicker, als sie wiegen. Volumen zählen, bevor eine Jacke dazu kommt.",
    "LONG SLEEVED": "Ärmellänge und Bündchen auf dem QC-Foto. Asiatische Längen laufen oft kürzer.",
    "HOODIE": "Schwer für ihr Volumen. Ein Hoodie kann die Gewichtsklasse der ganzen Box setzen.",
    "SWEATER": "GSM und Einlaufen. Brust messen, nicht nur das Etikett.",
    "SHAWL": "Leicht, aber voluminös wenn nicht flach gepackt.",
    "JACKET": "Daune braucht enorm Platz. Volumengewicht schlägt hier fast immer die Waage.",
    "SHELL JACKET": "Nähte und Reißverschluss nah auf dem QC-Foto.",
    "FLEECE JACKET": "Leicht auf der Waage, dick im Volumen. Wie Daune nachrechnen.",
    "DOWN JACKETS": "Volumen gewinnt. Eine Daunenjacke allein kann eine teurere Klasse erzwingen.",
    "TROUSERS": "Bundhöhe und Innenbeinlänge fotografieren. W/L stimmt nicht immer mit Zentimetern.",
    "Jersey": "Nummer, Patches und Saison auf den Fotos prüfen.",
    "FEMALE STYLE": "Passform ist selten Unisex. Brust und Länge messen.",
    "Electronics": "Oft Lithium. Viele Luftlinien lehnen ab: offizielle Site prüfen, bevor du bestellst.",
    "GLOVES": "Paar auf dem QC-Foto. Ein Handschuh auf dem Katalogshot sagt nichts über den zweiten.",
    "BAG": "Füllt eine Box fast allein. Volumen zählen, bevor Kleidung dazu kommt.",
    "HAT": "Druckempfindlich und voluminös. Füllung verlangen, sonst knickt die Krempe.",
    "JEWELRY": "Klein und billig zu senden. Gut, um eine fast volle Box zu runden.",
    "UNDERWEAR": "Weniger Listings. Wenn nichts kommt, nach Marke suchen, nicht nach dem Wort.",
    "BELT": "Flach und leicht. Ändert die Gewichtsklasse kaum.",
    "KNEEPAD": "Paar auf dem QC-Foto. Ein Pad auf dem Shot ist kein Paar.",
    "SOCKS": "Leichtes Füllmaterial. Paar und Größenaufdruck prüfen.",
    "HEADGEAR": "Fragen, wie es gepackt wird. Krempen knicken in engen Kartons.",
    "EARMUFF": "Leicht, aber der Bügel braucht Platz. Nicht unter einem Hoodie zerdrücken.",
    "SCARF": "Flach packen lassen, sonst kommt ein Volumenball.",
    "GLASSES": "Hartschale auf dem Lagerfoto verlangen, bevor du die Linie buchst.",
    "WATCH": "Klein und billig zu senden. Schließe auf dem QC-Foto.",
    "CHILD": "Asiatische Kindergrößen laufen kleiner. Messen, nicht vom Alter auf dem Etikett raten.",
}
CAT_NOTES_NL = {k: v for k, v in CAT_NOTES_EN.items()}
CAT_NOTES_NL.update({
    "SNEAKERS": "Zool en leest op de QC-foto’s voor je internationaal boekt.",
    "T-SHIRT": "Aziatische snits lopen vaak smaller. Meet de borst in centimeters.",
    "HOODIE": "Zwaar voor het volume. Eén hoodie kan de gewichtsklasse van de hele doos zetten.",
    "Electronics": "Vaak lithium. Veel luchtlijnen weigeren: check de officiële site eerst.",
    "BAG": "Vult bijna in z’n eentje een doos. Tel het volume voor je kleding toevoegt.",
})
CAT_NOTES_PL = {k: v for k, v in CAT_NOTES_EN.items()}
CAT_NOTES_PL.update({
    "SNEAKERS": "Podeszwa i kopyto na zdjęciach QC zanim zarezerwujesz międzynarodowy.",
    "T-SHIRT": "Azjatyckie kroje są często węższe. Mierz klatkę w centymetrach.",
    "HOODIE": "Ciężka jak na objętość. Jedna bluza może ustawić próg wagi całej paczki.",
    "Electronics": "Często lit. Wiele linii lotniczych odmawia: sprawdź oficjalną stronę wcześniej.",
    "BAG": "Prawie sama wypełnia karton. Policz objętość zanim dodasz ubrania.",
})

# Ranked inners per dest: wrapped in dest chrome, never regenerated. Paths that are
# also a CMS slug (guide/ship/help/…) are generated instead — see _wrap_targets().
# how-to-use-mycnbox and mycnbox-shipping ARE generated CMS. Ranked shipping-guide stays wrap.
_RANKED_SHARED = (
    ("/mycnbox-spreadsheet/", 8000),
    ("/is-mycnbox-legit/", 8000),
    ("/mycnbox-shipping-guide/", 8000),
    ("/mycnbox-coupons/", 8000),
)
RANKED = {k: _RANKED_SHARED for k in ("uk", "de", "es", "fr", "nl", "pl")}

# Copied from tools/mycnbox_desks.py DESTS[*]["keep"], plus ranked wrap URLs.
KEEP = {
    "uk": [
        ("/is-mycnbox-legit/", "Is it legit?"),
        ("/mycnbox-coupons/", "Coupons article"),
        ("/mycnbox-shipping-guide/", "UK shipping"),
        ("/mycnbox-spreadsheet/", "Spreadsheet"),
    ],
    "de": [
        ("/mycnbox-spreadsheet/", "Spreadsheet DE"),
        ("/mycnbox-shipping-guide/", "Versand DE"),
        ("/how-to-use-mycnbox/", "Anleitung"),
        ("/is-mycnbox-legit/", "Seriös?"),
        ("/mycnbox-coupons/", "Coupons"),
    ],
    "es": [
        ("/mycnbox-invite-code/", "Código (artículo)"),
        ("/mycnbox-community/", "Comunidad"),
        ("/mycnbox-shipping-guide/", "Envío"),
        ("/how-to-use-mycnbox/", "Cómo usar"),
        ("/mycnbox-spreadsheet/", "Spreadsheet"),
        ("/is-mycnbox-legit/", "¿Confiable?"),
        ("/mycnbox-coupons/", "Cupones"),
    ],
    "fr": [
        ("/mycnbox-shipping-guide/", "Livraison"),
        ("/mycnbox-community/", "Communauté"),
        ("/mycnbox-spreadsheet/", "Spreadsheet"),
        ("/how-to-use-mycnbox/", "Tutoriel"),
        ("/is-mycnbox-legit/", "Avis"),
        ("/mycnbox-coupons/", "Coupons"),
    ],
    "nl": [
        ("/mycnbox-shoes-spreadsheet/", "Shoes sheet"),
        ("/mycnbox-shipping-guide/", "Verzending"),
        ("/is-mycnbox-legit/", "Legit?"),
        ("/mycnbox-spreadsheet/", "Spreadsheet"),
        ("/mycnbox-coupons/", "Coupons"),
    ],
    "pl": [
        ("/mycnbox-qc-guide/", "QC"),
        ("/mycnbox-spreadsheet/", "Spreadsheet PL"),
        ("/how-to-use-mycnbox/", "Poradnik"),
        ("/mycnbox-shipping-guide/", "Wysyłka"),
        ("/is-mycnbox-legit/", "Czy to legalne?"),
        ("/mycnbox-coupons/", "Kupony"),
    ],
}

TWINS = {}
TWIN_EXTRA = {}
TWIN_DEEP_PROBES = {}

CMS_PAGE_LOCS = (
    "about", "about/", "who-we-are", "who-we-are/", "help", "help/", "news", "news/", "catalog", "catalog/",
    "start", "start/",
    "ayuda", "ayuda/", "novedades", "novedades/", "sobre-nosotros", "sobre-nosotros/",
    "catalogo", "catalogo/",
    "aide", "aide/", "catalogue", "catalogue/", "actualites", "actualites/", "a-propos", "a-propos/",
    "hilfe", "hilfe/", "aktuelles", "aktuelles/", "ueber-uns", "ueber-uns/", "katalog", "katalog/",
    "hulp", "hulp/", "nieuws", "nieuws/", "over-ons", "over-ons/", "catalogus", "catalogus/",
    "pomoc", "pomoc/", "aktualnosci", "aktualnosci/", "o-nas", "o-nas/",
    "how-to-use-mycnbox", "how-to-use-mycnbox/", "mycnbox-shipping", "mycnbox-shipping/",
)

WRAP_SKIP_PREFIXES = (
    "help/", "news/", "about/", "who-we-are/", "catalog/", "start/",
    "ayuda/", "novedades/", "sobre-nosotros/", "catalogo/",
    "aide/", "catalogue/", "actualites/", "a-propos/",
    "hilfe/", "aktuelles/", "ueber-uns/", "katalog/",
    "hulp/", "nieuws/", "over-ons/", "catalogus/",
    "pomoc/", "aktualnosci/", "o-nas/",
    "api/", "assets/", "img/",
    "how-to-use-mycnbox/", "mycnbox-shipping/",
    "faq/", "guide/",
)
WRAP_POISON = ("orientdig", "orient dig", "1yi9", "cssb.uy", "1qodrw", "bbd5off", "cruisezhang", "200345875")

EXTRA_CSS = """
:root{--primary-soft:#fff4ed;--login-fg:#fff}
.hero .eyebrow{color:#ffb088}
header.top .hdr-login,.hdr-login{background:#ff5501;color:#fff}
header.top .hdr-login:hover,.hdr-login:hover{background:#e04c00;color:#fff}
.sbox button{color:#fff}
"""

STORAGE = {
    "en": (
        "Official Help: 90 free warehouse days "
        f"({HELP}). Confirm that article the morning you ship ({DATE})."
    ),
    "de": (
        "Offizielles Help: 90 Tage Lager gratis "
        f"({HELP}). Denselben Artikel am Versandmorgen prüfen ({DATE})."
    ),
    "es": (
        "Help oficial: 90 días gratis de almacén "
        f"({HELP}). Confirma el artículo la mañana del envío ({DATE})."
    ),
    "fr": (
        "Help officiel : 90 jours d’entrepôt gratuits "
        f"({HELP}). Relire l’article le matin de l’envoi ({DATE})."
    ),
    "nl": (
        "Officiële Help: 90 dagen magazijn gratis "
        f"({HELP}). Bevestig het artikel op de verzendochtend ({DATE})."
    ),
    "pl": (
        "Oficjalny Help: 90 dni magazynu gratis "
        f"({HELP}). Potwierdź artykuł rano w dniu nadania ({DATE})."
    ),
}


def _storage(loc: str) -> str:
    return STORAGE.get(loc, STORAGE["en"])


def _en_pack(host, dest, dest_label, dest_zh, lang, ccy, topic, hero, lead, postal, customs, customs_url, aliens, css, css_id, login="Log in to MyCNBox"):
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
            (GUIDE_HREF, "MyCNBox guide"),
            ("/catalog/", "The spreadsheet and the categories"),
            (SHIP_HREF, "Shipping and customs"),
            ("/help/", "Help and questions"),
            ("/news/", "News"),
            ("/about/", "About us"),
        ],
        "aliens": aliens,
        "not_found_tab": "Page not found",
        "login": login,
        "menu": "Open menu",
        "home_cta": "Back to the homepage",
        "skip": "en",
        "desk_css": css,
        "css_id": css_id,
    }


PACKS = {
    "uk": _en_pack(
        "mycnbox.co.uk", "GB", "the United Kingdom", "United Kingdom — 英国",
        "en-GB", "GBP",
        "buy in China from the United Kingdom, safely",
        "MyCNBox Spreadsheet: the guide to buying in China from the United Kingdom",
        "How you paste a product link into the agent, how the w2clinks catalogue works, how a parcel travels to the United Kingdom, and what you check before HMRC.",
        "UK postcode. Northern Ireland is often another carrier product",
        "HMRC", "https://www.gov.uk/goods-sent-from-abroad",
        ("Packstation", "form A1A 1A1", "Poste Italiane", "no copiamos", "pas un code postal belge", "00-001 Warszawa", "Nederlandse postcode"),
        "mycnbox-uk-desk.css", "mycnbox-uk",
        "Log in to MyCNBox",
    ),
    "de": {
        "host": "mycnbox.de",
        "dest": "DE",
        "dest_label": "Deutschland",
        "dest_zh": "Germany — 德国",
        "lang": "de-DE",
        "loc": "de",
        "in_language": "auf Deutsch",
        "ccy": "EUR",
        "home_topic": "in China kaufen aus Deutschland, sicher",
        "hero_h1": "MyCNBox Spreadsheet: die Anleitung, um in China von Deutschland aus zu kaufen",
        "eyebrow": "Unabhängiger Leitfaden, auf Deutsch",
        "lead": "Wie du einen Produktlink in den Agenten einfügst, wie der w2clinks-Katalog funktioniert, wie ein Paket nach Deutschland reist und was du vor dem Zoll prüfst.",
        "fingerprint": dest_local_pack("DE")["fingerprint"],
        "customs": "Zoll",
        "customs_url": "https://www.zoll.de/",
        "postal": "deutsche PLZ. Packstation-Nummern sind ein DE-Muster",
        "catalog": "/katalog/",
        "help": "/hilfe/",
        "news": "/aktuelles/",
        "about": "/ueber-uns/",
        "guide": GUIDE_HREF,
        "ship": SHIP_HREF,
        "nav": [
            ("/start/", "Start"),
            (GUIDE_HREF, "Anleitung"),
            ("/katalog/", "Katalog"),
            (SHIP_HREF, "Versand"),
            ("/hilfe/", "Hilfe"),
            ("/aktuelles/", "Aktuelles"),
        ],
        "footer_sections": [
            (GUIDE_HREF, "MyCNBox-Anleitung"),
            ("/katalog/", "Spreadsheet und Kategorien"),
            (SHIP_HREF, "Versand und Zoll"),
            ("/hilfe/", "Hilfe und Fragen"),
            ("/aktuelles/", "Aktuelles"),
            ("/ueber-uns/", "Über uns"),
        ],
        "aliens": ("form A1A 1A1", "Poste Italiane", "Northern Ireland is often another", "no copiamos", "pas un code postal belge", "00-001 Warszawa", "Nederlandse postcode"),
        "not_found_tab": "Seite nicht gefunden",
        "login": "Bei MyCNBox anmelden",
        "menu": "Menü öffnen",
        "home_cta": "Zurück zur Startseite",
        "skip": "de",
        "desk_css": "mycnbox-de-desk.css",
        "css_id": "mycnbox-de",
        "lab_not": "nicht EU und nicht AT",
    },
    "es": {
        "host": "mycnbox.es",
        "dest": "ES",
        "dest_label": "España",
        "dest_zh": "Spain — 西班牙",
        "lang": "es-ES",
        "loc": "es",
        "in_language": "en español",
        "ccy": "EUR",
        "home_topic": "comprar en China desde España, con seguridad",
        "hero_h1": "MyCNBox Spreadsheet: la guía para comprar en China desde España",
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
            (GUIDE_HREF, "Guía MyCNBox"),
            ("/catalogo/", "Spreadsheet y categorías"),
            (SHIP_HREF, "Envío y aduanas"),
            ("/ayuda/", "Ayuda y preguntas"),
            ("/novedades/", "Novedades"),
            ("/sobre-nosotros/", "Sobre nosotros"),
        ],
        "aliens": ("Packstation", "1010 Wien", "Poste Italiane", "form A1A 1A1", "00-001 Warszawa", "pas un code postal belge", "Nederlandse postcode", "Northern Ireland is often another"),
        "not_found_tab": "Página no encontrada",
        "login": "Entrar en MyCNBox",
        "menu": "Abrir menú",
        "home_cta": "Volver al inicio",
        "skip": "es",
        "desk_css": "mycnbox-es-desk.css",
        "css_id": "mycnbox-es",
    },
    "fr": {
        "host": "mycnbox.fr",
        "dest": "FR",
        "dest_label": "la France",
        "dest_zh": "France — 法国",
        "lang": "fr-FR",
        "loc": "fr",
        "in_language": "en français",
        "ccy": "EUR",
        "home_topic": "acheter en Chine depuis la France, en sécurité",
        "hero_h1": "MyCNBox Spreadsheet : le guide pour acheter en Chine depuis la France",
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
        "guide": GUIDE_HREF,
        "ship": SHIP_HREF,
        "nav": [
            ("/start/", "Start"),
            (GUIDE_HREF, "Guide"),
            ("/catalogue/", "Catalogue"),
            (SHIP_HREF, "Livraison"),
            ("/aide/", "Aide"),
            ("/actualites/", "Actus"),
        ],
        "footer_sections": [
            (GUIDE_HREF, "Guide MyCNBox"),
            ("/catalogue/", "Spreadsheet et catégories"),
            (SHIP_HREF, "Livraison et douane"),
            ("/aide/", "Aide et questions"),
            ("/actualites/", "Actus"),
            ("/a-propos/", "À propos"),
        ],
        "aliens": ("Packstation", "Poste Italiane", "00-001 Warszawa", "form A1A 1A1", "no copiamos", "Nederlandse postcode", "Northern Ireland is often another"),
        "not_found_tab": "Page introuvable",
        "login": "Se connecter à MyCNBox",
        "menu": "Ouvrir le menu",
        "home_cta": "Retour à l’accueil",
        "skip": "fr",
        "desk_css": "mycnbox-fr-desk.css",
        "css_id": "mycnbox-fr",
    },
    "nl": {
        "host": "mycnbox.nl",
        "dest": "NL",
        "dest_label": "Nederland",
        "dest_zh": "Netherlands — 荷兰",
        "lang": "nl-NL",
        "loc": "nl",
        "in_language": "in het Nederlands",
        "ccy": "EUR",
        "home_topic": "kopen in China vanaf Nederland, veilig",
        "hero_h1": "MyCNBox Spreadsheet: de gids om in China te kopen vanuit Nederland",
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
            (GUIDE_HREF, "Handleiding"),
            ("/catalogus/", "Catalogus"),
            (SHIP_HREF, "Verzending"),
            ("/hulp/", "Hulp"),
            ("/nieuws/", "Nieuws"),
        ],
        "footer_sections": [
            (GUIDE_HREF, "MyCNBox-handleiding"),
            ("/catalogus/", "Spreadsheet en categorieën"),
            (SHIP_HREF, "Verzending en douane"),
            ("/hulp/", "Hulp en vragen"),
            ("/nieuws/", "Nieuws"),
            ("/over-ons/", "Over ons"),
        ],
        "aliens": ("Packstation", "1010 Wien", "Poste Italiane", "form A1A 1A1", "00-001 Warszawa", "no copiamos", "pas un code postal belge", "Northern Ireland is often another"),
        "not_found_tab": "Pagina niet gevonden",
        "login": "Inloggen bij MyCNBox",
        "menu": "Menu openen",
        "home_cta": "Terug naar de homepage",
        "skip": "nl",
        "desk_css": "mycnbox-nl-desk.css",
        "css_id": "mycnbox-nl",
    },
    "pl": {
        "host": "mycnbox.pl",
        "dest": "PL",
        "dest_label": "Polska",
        "dest_zh": "Poland — 波兰",
        "lang": "pl-PL",
        "loc": "pl",
        "in_language": "po polsku",
        "ccy": "PLN",
        "home_topic": "kupować w Chinach z Polski, bezpiecznie",
        "hero_h1": "MyCNBox Spreadsheet: poradnik, jak kupować w Chinach z Polski",
        "eyebrow": "Niezależny przewodnik, po polsku",
        "lead": "Jak wklejasz link produktu do agenta, jak działa katalog w2clinks, jak paczka jedzie do Polski i co sprawdzasz przed cłem.",
        "fingerprint": dest_local_pack("PL")["fingerprint"],
        "customs": "Krajowa Administracja Skarbowa",
        "customs_url": "https://www.podatki.gov.pl/",
        "postal": "polski kod pocztowy, np. 00-001 Warszawa",
        "catalog": "/katalog/",
        "help": "/pomoc/",
        "news": "/aktualnosci/",
        "about": "/o-nas/",
        "guide": GUIDE_HREF,
        "ship": SHIP_HREF,
        "nav": [
            ("/start/", "Start"),
            (GUIDE_HREF, "Poradnik"),
            ("/katalog/", "Katalog"),
            (SHIP_HREF, "Wysyłka"),
            ("/pomoc/", "Pomoc"),
            ("/aktualnosci/", "Aktualności"),
        ],
        "footer_sections": [
            (GUIDE_HREF, "Poradnik MyCNBox"),
            ("/katalog/", "Spreadsheet i kategorie"),
            (SHIP_HREF, "Wysyłka i cło"),
            ("/pomoc/", "Pomoc i pytania"),
            ("/aktualnosci/", "Aktualności"),
            ("/o-nas/", "O nas"),
        ],
        "aliens": ("Packstation", "form A1A 1A1", "Poste Italiane", "no copiamos", "pas un code postal belge", "Northern Ireland is often another", "Nederlandse postcode"),
        "not_found_tab": "Strona nie znaleziona",
        "login": "Zaloguj się do MyCNBox",
        "menu": "Otwórz menu",
        "home_cta": "Wróć na stronę główną",
        "skip": "en",
        "desk_css": "mycnbox-pl-desk.css",
        "css_id": "mycnbox-pl",
        "lab_not": "nie EU i nie DE",
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
    if loc == "de":
        intro = (
            "Unabhängiger deutschsprachiger Leitfaden zu MyCNBox und dazu, wie du den "
            f"Katalog von w2clinks nutzt, um von {p['dest_label']} aus in China zu kaufen."
        )
        independence = (
            "MyCNBox Spreadsheet ist eine unabhängige Informationsseite. Wir sind nicht "
            "MyCNBox, wir nehmen keine Bestellungen an, wir kassieren kein Porto und wir "
            "sehen dein Konto nicht. Bestellung, Zahlung und Reklamation laufen über die offizielle Site."
        )
        copyright = "&copy; 2026 MyCNBox Spreadsheet. Deutscher Text, vor der Veröffentlichung gegengelesen."
        sections_h, official_h, independence_h, nav_aria = (
            "Bereiche", "Offizielle Links", "Unabhängigkeitshinweis.", "Hauptmenü",
        )
        nf_h1, nf_lead = "Diese Seite gibt es nicht", "Der Link ist vielleicht alt. Das sind die Bereiche, die existieren:"
        official_links = [
            (_off(p["host"]), "MyCNBox (offizielle Site)"),
            (_off(p["host"], EST_PATH), f"Offizieller Schätzer ({DATE})"),
        ]
    elif loc == "nl":
        intro = (
            "Onafhankelijke Nederlandstalige gids over MyCNBox en hoe je de w2clinks-catalogus "
            f"gebruikt om vanuit {p['dest_label']} in China te kopen."
        )
        independence = (
            "MyCNBox Spreadsheet is een onafhankelijke infosite. Wij zijn MyCNBox niet, "
            "we verwerken geen bestellingen, we innen geen porto en we zien je account niet. "
            "Elke bestelling, betaling en klacht loopt via de officiële site."
        )
        copyright = "&copy; 2026 MyCNBox Spreadsheet. Nederlandse tekst, nagelezen voor publicatie."
        sections_h, official_h, independence_h, nav_aria = (
            "Onderdelen", "Officiële links", "Onafhankelijkheidsnotitie.", "Hoofdmenu",
        )
        nf_h1, nf_lead = "Deze pagina bestaat niet", "De link is misschien oud. Dit zijn de onderdelen die wel bestaan:"
        official_links = [
            (_off(p["host"]), "MyCNBox (officiële site)"),
            (_off(p["host"], EST_PATH), f"Officiële schatter ({DATE})"),
        ]
    elif loc == "pl":
        intro = (
            "Niezależny polski przewodnik po MyCNBox i po tym, jak używasz katalogu w2clinks, "
            f"żeby kupować w Chinach z {p['dest_label']}."
        )
        independence = (
            "MyCNBox Spreadsheet to niezależna strona informacyjna. Nie jesteśmy MyCNBox, "
            "nie przyjmujemy zamówień, nie pobieramy porto i nie widzimy Twojego konta. "
            "Zamówienie, płatność i reklamacja idą przez oficjalną stronę."
        )
        copyright = "&copy; 2026 MyCNBox Spreadsheet. Tekst polski, przeczytany przed publikacją."
        sections_h, official_h, independence_h, nav_aria = (
            "Działy", "Oficjalne linki", "Informacja o niezależności.", "Menu główne",
        )
        nf_h1, nf_lead = "Tej strony nie ma", "Link może być stary. Oto działy, które istnieją:"
        official_links = [
            (_off(p["host"]), "MyCNBox (strona oficjalna)"),
            (_off(p["host"], EST_PATH), f"Oficjalny estymator ({DATE})"),
        ]
    elif loc == "es":
        intro = (
            "Guía independiente en español sobre MyCNBox y sobre cómo usas el catálogo "
            f"w2clinks para comprar en China desde {p['dest_label']}."
        )
        independence = (
            "MyCNBox Spreadsheet es un sitio informativo independiente. No somos MyCNBox, "
            "no tramitamos pedidos, no cobramos el envío y no vemos tu cuenta. "
            "Cada pedido, pago y reclamación pasa por el sitio oficial."
        )
        copyright = "&copy; 2026 MyCNBox Spreadsheet. Texto en español, releído antes de publicar."
        sections_h, official_h, independence_h, nav_aria = (
            "Secciones", "Enlaces oficiales", "Aviso de independencia.", "Menú principal",
        )
        nf_h1, nf_lead = "Esta página no existe", "El enlace quizá sea antiguo. Estas secciones sí existen:"
        official_links = [
            (_off(p["host"]), "MyCNBox (sitio oficial)"),
            (_off(p["host"], EST_PATH), f"Estimador oficial ({DATE})"),
        ]
    elif loc == "fr":
        intro = (
            "Guide indépendant en français sur MyCNBox et sur la façon d’utiliser le catalogue "
            f"w2clinks pour acheter en Chine depuis {p['dest_label']}."
        )
        independence = (
            "MyCNBox Spreadsheet est un site d’information indépendant. Nous ne sommes pas MyCNBox, "
            "nous ne traitons pas les commandes, nous n’encaissons pas le port et nous ne voyons "
            "pas ton compte. Chaque commande, paiement et réclamation passe par le site officiel."
        )
        copyright = "&copy; 2026 MyCNBox Spreadsheet. Texte français, relu avant publication."
        sections_h, official_h, independence_h, nav_aria = (
            "Rubriques", "Liens officiels", "Mention d’indépendance.", "Menu principal",
        )
        nf_h1, nf_lead = "Cette page n’existe pas", "Le lien est peut-être ancien. Voici les rubriques qui existent :"
        official_links = [
            (_off(p["host"]), "MyCNBox (site officiel)"),
            (_off(p["host"], EST_PATH), f"Estimateur officiel ({DATE})"),
        ]
    else:
        intro = (
            f"Independent English-language guide to MyCNBox and to how you use the w2clinks "
            f"catalogue to buy in China from {p['dest_label']}."
        )
        independence = (
            "MyCNBox Spreadsheet is an independent information site. We are not MyCNBox, "
            "we do not process orders, we do not collect shipping fees and we cannot see "
            "your account. Every order, payment and claim runs through the official site."
        )
        copyright = "&copy; 2026 MyCNBox Spreadsheet. English copy, edited and checked by people before publication."
        sections_h, official_h, independence_h, nav_aria = (
            "Sections", "Official links", "Independence notice.", "Main menu",
        )
        nf_h1, nf_lead = "This page does not exist", "The link may be old. These are the sections that do exist:"
        official_links = [
            (_off(p["host"]), "MyCNBox (official site)"),
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
        "customs": p["customs"],
        "customs_url": p["customs_url"],
        "storage": _storage(p["loc"]),
        "estimator": EST,
        "official": OFFICIAL,
        "date": DATE,
        "keep": list(KEEP.get(key) or []),
        "codes_off_title": list(INVITES),
        "strict_html_codes": True,
    }


def _pl_faqs(p: dict) -> list[tuple[str, str]]:
    dest, host, store = p["dest_label"], p["host"], _storage("pl")
    fp = p["fingerprint"]
    est, official, customs = EST, OFFICIAL, p["customs"]
    pad = (
        f" Estimator country is PL, not this TLD and not EU as one destination. "
        f"Live freight is {est}. Warehouse days: official Help FAQDetail id 83, 90 free days; "
        f"confirm that article the morning you ship ({DATE}). SKU, QC photos, volume vs scale, "
        f"prepaid vs collect, IOSS and VAT stay on the official app. This HTML is not checkout. "
        f"Delivery address on this dest: {fp}."
    )
    return [
        ("Czy MyCNBox sprzedaje towar z tej strony?",
         f"Nie. MyCNBox to agent zakupowy: kupuje w chińskich sklepach na Twoje nazwisko, fotografuje w magazynie, potem rezerwujesz SKU do {dest}. {host} to niezależny desk redakcyjny, nie kasa. Zamówienia, płatność i reklamacja tylko na {official}. Adres dostawy na tym deście to {fp}. Cel estymatora to kraj, nie ten TLD." + pad),
        ("Czy mogę mieć MyCNBox po polsku?",
         f"Selektor języka aplikacji jest niezależny od tego desku. Zmierzono {DATE}. Pola estymatora często zostają po angielsku albo chińsku. Adres dostawy i tak musi być w formacie {dest} — {fp}. Zmiana języka na {host} nie zmienia języka oficjalnej aplikacji." + pad),
        ("Dlaczego katalog nic nie znajduje po polsku?",
         f"Indeks na w2clinks jest angielski (sneakers, hoodie, jacket). «Buty» albo «bluza» często dają zero kart. To nie pusty sklep i nie błąd tego desku. Pomiar {DATE}. Wpisz angielski key albo stuknij chip kategorii na stronie głównej {host}." + pad),
        ("Ile razy płacę?",
         f"Dwa razy: najpierw towar plus krajowy transport do magazynu w Chinach, potem linia międzynarodowa do {dest}. Pomiędzy możesz łączyć, anulować albo zmienić linię. Ten desk nie kasuje i nie widzi salda. Żywe kwoty czytasz na {official} w dniu płatności." + pad),
        ("Dlaczego dolary na oficjalnej stronie, a tu PLN?",
         f"Przełącznik waluty często zmienia symbol, nie cyfrę. Ten desk pokazuje {p['ccy']} jako podgląd, nie kasę. Kwotę czytasz w aplikacji w dniu płatności. Żywe pieniądze frachtu: {est} z celem {dest}, nie ten hostname." + pad),
        ("Jak płacę?",
         f"Tylko na {official}. Karta, PayPal, saldo — FAQ oficjalne tego dnia, nie ten HTML. {host} nie zbiera numerów kart, nie zapisuje metody i nie wystawia faktury. Po płatności ticket zostaje w aplikacji agenta." + pad),
        ("Co to waga objętościowa?",
         f"Wiele linii lotniczych liczy max(waga, L×W×H w cm / dzielnik, często 8000). Kurtka puchowa jest lekka i puchata: tam wygrywa objętość. Tylko geometria — cena wychodzi z {est} z celem {dest}, nie z tego HTML. Wpisujesz wymiary po zdjęciach magazynu." + pad),
        (f"Kto płaci cło do {dest}?",
         f"Decyduje SKU. Kurier przy Collect może doliczyć opłatę. Źródło: {customs}, rano w dniu nadania. Cel estymatora: PL z kodem {fp}, nie niemiecki automat paczkowy i nie EU jako jeden kraj. Ten desk nie uczy zaniżania wartości zgłoszeniowej." + pad),
        ("Czy jest próg do obejścia?",
         f"Nie. VAT, IOSS i progi się zmieniają. Czytaj {customs} i SKU rano w dniu nadania. Ten desk nie wymyśla kwoty zgłoszeniowej dla adresu w Polsce i nie wkleja niemieckiego progu Zoll na {host}. Adres: {fp}." + pad),
        ("Czy mogę łączyć zamówienia?",
         f"Tak, zwykła oszczędność międzynarodowych linii. Części czekają w magazynie. {store}. Jeśli QC rozbije kartony, każdy karton osobno szacuj do {dest} w {est}. Łączenie to nie poradnik celny." + pad),
        ("Są zdjęcia QC?",
         f"Tak, zdjęcia magazynowe lądują w aplikacji, gdy sztuka jest w Chinach. Dodatkowe kąty często płatne. Reklamacja jest łatwiejsza, dopóki leży w magazynie, nie po cłe do {dest}. Nie rezerwuj linii międzynarodowej zanim zaakceptujesz QC." + pad),
        ("Czego nie wolno wysyłać?",
         f"Tytoń, alkohol, leki, zakazane. Płyny i proszki mogą być towarem niebezpiecznym. To reguła platformy na {official}, nie {customs}. Restricted albo cena 0 na karcie znaczy: nie zamawiaj. MyCNBox nie sprzedaje własnego towaru." + pad),
        ("Dlaczego restricted albo cena 0?",
         f"Link źródłowy nie da się kupić przez agenta, albo cena się nie odczytała. Nie buduj haulu na zerze. Sprawdź żywą kartę MyCNBox na {official} zanim wkleisz ten sam link drugi raz. Restricted to blokada zakupu, nie zawiadomienie {customs}." + pad),
        ("Paczka lżejsza niż szacunek?",
         f"Oficjalne FAQ pokrywa szacunek vs waga rzeczywista i zwrot porto. Ten HTML nie jest wyceną. Policz {est} do {dest} po zdjęciach magazynowych, z rzeczywistymi wymiarami kartonu. {store}" + pad),
        ("Gdzie reklamuję?",
         f"Tylko na {official}, nigdy tutaj. {host} nie widzi konta, nie otwiera ticketu i nie zwraca porto. Czat w aplikacji albo oficjalny Help. Cel estymatora to {dest}, nie TLD. Adres dostawy: {fp}." + pad),
    ]


def _faqs(key: str) -> list[tuple[str, str]]:
    p = PACKS[key]
    if p["loc"] == "pl":
        return _pl_faqs(p)
    facts = _facts(key)
    pairs = []
    for q, a in long_faqs(facts):
        a = a.replace("/api/products/", "w2clinks")
        a = re.sub(r"ni copia un snapshot de 58 l[ií]neas ajenas\.?", "", a, flags=re.I)
        a = re.sub(r"58 l[ií]neas(?: para Espa\w*)?", "", a, flags=re.I)
        a = re.sub(r"23[,.]81\s*USD", "", a, flags=re.I)
        pairs.append((q, a))
    extra = f"The delivery address uses a {p['postal']}."
    if p["loc"] == "es":
        extra = f"La dirección de entrega es una {p['postal']}."
    elif p["loc"] == "fr":
        extra = f"L’adresse de livraison est une {p['postal']}."
    elif p["loc"] == "de":
        extra = f"Die Lieferadresse ist eine {p['postal']}."
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
    if loc == "de":
        return [
            "Was MyCNBox ist und in welcher Sprache es läuft",
            "Was du zahlen wirst",
            f"Einfuhr nach {dest}",
            "Lager, Fotos und was reisen darf",
            "Wenn etwas nicht stimmt",
        ]
    if loc == "nl":
        return [
            "Wat MyCNBox is en in welke taal het draait",
            "Wat je gaat betalen",
            f"Invoer naar {dest}",
            "Magazijn, foto’s en wat mag reizen",
            "Als iets niet klopt",
        ]
    if loc == "pl":
        return [
            "Czym jest MyCNBox i w jakim języku działa",
            "Co zapłacisz",
            f"Import do {dest}",
            "Magazyn, zdjęcia i co może jechać",
            "Gdy coś nie gra",
        ]
    if loc == "es":
        return [
            "Qué es MyCNBox y en qué idioma funciona",
            "Qué vas a pagar",
            f"Importación a {dest}",
            "Almacén, fotos y qué puede viajar",
            "Si algo no cuadra",
        ]
    if loc == "fr":
        return [
            "Ce qu’est MyCNBox et dans quelle langue ça tourne",
            "Ce que tu vas payer",
            f"Import vers {dest}",
            "Entrepôt, photos et ce qui peut voyager",
            "Si quelque chose cloche",
        ]
    return [
        "What MyCNBox is, and which language it uses",
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
    if loc == "de":
        head = ("Wenn du denkst an", "Tippe")
        rows = (
            ("Turnschuhe", "sneakers"),
            ("Kapuzenpullover / Hoodie", "hoodie"),
            ("Jacke", "jacket"),
            ("Hose", "trousers"),
            ("Tasche", "bag"),
            ("Brille", "glasses"),
            ("Uhr", "watch"),
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
    elif loc == "pl":
        head = ("Jeśli myślisz o", "Wpisz")
        rows = (
            ("buty", "sneakers"),
            ("bluza", "hoodie"),
            ("kurtka", "jacket"),
            ("spodnie", "trousers"),
            ("torba", "bag"),
            ("okulary", "glasses"),
            ("zegarek", "watch"),
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
    elif key == "uk":
        head = ("If you think of", "Type")
        rows = (
            ("trainers", "sneakers"),
            ("jumper", "sweater"),
            ("hoodie", "hoodie"),
            ("trousers", "trousers"),
            ("bag", "bag"),
            ("glasses", "glasses"),
            ("watch", "watch"),
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
    if loc == "de":
        return cats_for(DE_LABELS)
    if loc == "nl":
        return cats_for(NL_LABELS)
    if loc == "pl":
        return cats_for(PL_LABELS)
    if loc == "es":
        return cats_for(ES_LABELS)
    if loc == "fr":
        return cats_for(FR_LABELS)
    return cats_for(EN_LABELS)


def _sheet(desk: CountryDesk) -> str:
    return w2c_sheet(desk)


def _fig(src: str, alt: str, cap: str, w: int = 1200, h: int = 750) -> str:
    sep = "&" if "?" in src else "?"
    return cms_fig(f"{src}{sep}v={CSS_V}", alt, cap, w, h)


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
    if loc == "de":
        off_alt, off_cap = (
            "Offizielle MyCNBox-Startseite: Suche, Coupon-Banner und Anmeldung",
            f"www.mycnbox.com, {DATE}. Der Schätzer liegt unter {EST_PATH}. Dieser Desk erfindet keine Linie und keinen Betrag.",
        )
        sheet_alt, sheet_cap = (
            "MyCNBox-Katalog auf w2clinks: Produktkarten mit Foto, Marke und Referenzpreis",
            "Karten, keine Excel-Zellen. Yuan-Preise ändern sich täglich. Aufnahme 6 Oct 2026, Kategorie SNEAKERS.",
        )
        vol_alt, vol_cap = (
            "Rechenbeispiel Volumengewicht: 40×40×3 cm und 200 g Waage werden 600 g Volumen",
            "Ein Rechenbeispiel, kein Lagerfoto. Viele Linien rechnen das Maximum aus Waage und Volumen, oft L×B×H (cm) / 8000.",
        )
        zoek_alt, zoek_cap = (
            "Hoodie-Suche im MyCNBox-Katalog auf w2clinks",
            "Ergebnisse mit Filterspalte. Aufnahme 6 Oct 2026.",
        )
        diy_alt, diy_cap = (
            "MyCNBox-Suche: einen Taobao-, 1688- oder Weidian-Link einfügen",
            f"Öffentliche Paste-Leiste auf www.mycnbox.com, {DATE}. Dieser Desk erfindet keine ausgefüllte Bestellung.",
        )
    elif loc == "nl":
        off_alt, off_cap = (
            "Officiële MyCNBox-homepage: zoeken, couponbanner en inloggen",
            f"www.mycnbox.com, {DATE}. De schatter staat op {EST_PATH}. Deze gids verzint geen lijn en geen bedrag.",
        )
        sheet_alt, sheet_cap = (
            "MyCNBox-catalogus op w2clinks: kaarten met foto, merk en referentieprijs",
            "Kaarten, geen Excel-cellen. Yuan-prijzen veranderen per dag. Opname 6 Oct 2026, categorie SNEAKERS.",
        )
        vol_alt, vol_cap = (
            "Voorbeeld volumgewicht: 40×40×3 cm en 200 g op de weegschaal wordt 600 g volume",
            "Een rekenvoorbeeld, geen magazijnfoto. Veel lijnen factureren het maximum van weegschaal en volume, vaak L×W×H (cm) / 8000.",
        )
        zoek_alt, zoek_cap = (
            "Hoodie-zoekopdracht in de MyCNBox-catalogus op w2clinks",
            "Resultaten met filterkolom. Opname 6 Oct 2026.",
        )
        diy_alt, diy_cap = (
            "MyCNBox-zoekbalk: een Taobao-, 1688- of Weidian-link plakken",
            f"Publieke plakbalk op www.mycnbox.com, {DATE}. Deze gids verzint geen ingevulde bestelling.",
        )
    elif loc == "pl":
        off_alt, off_cap = (
            "Oficjalna strona MyCNBox: wyszukiwarka, baner kuponów i logowanie",
            f"www.mycnbox.com, {DATE}. Estymator jest pod {EST_PATH}. Ten desk nie wymyśla linii ani kwoty.",
        )
        sheet_alt, sheet_cap = (
            "Katalog MyCNBox na w2clinks: karty z zdjęciem, marką i ceną orientacyjną",
            "Karty, nie komórki Excela. Ceny w juanach zmieniają się co dzień. Zdjęcie 6 Oct 2026, kategoria SNEAKERS.",
        )
        vol_alt, vol_cap = (
            "Przykład wagi objętościowej: 40×40×3 cm i 200 g na wadze to 600 g objętości",
            "Przykład liczony, nie zdjęcie magazynu. Wiele linii liczy maksimum wagi i objętości, często L×W×H (cm) / 8000.",
        )
        zoek_alt, zoek_cap = (
            "Wyszukiwanie hoodie w katalogu MyCNBox na w2clinks",
            "Wyniki z kolumną filtrów. Zdjęcie 6 Oct 2026.",
        )
        diy_alt, diy_cap = (
            "Wyszukiwanie MyCNBox: wklej link Taobao, 1688 lub Weidian",
            f"Publiczny pasek na www.mycnbox.com, {DATE}. Ten desk nie wymyśla wypełnionego zamówienia.",
        )
    elif loc == "es":
        off_alt, off_cap = (
            "Portada oficial de MyCNBox: búsqueda, cupón y acceso",
            f"www.mycnbox.com, {DATE}. El estimador está en {EST_PATH}. Esta guía no inventa una línea ni un importe.",
        )
        sheet_alt, sheet_cap = (
            "Catálogo MyCNBox en w2clinks: fichas con foto, marca y precio de referencia",
            "Fichas, no celdas de Excel. Los precios en yuan cambian cada día. Captura 6 Oct 2026, categoría SNEAKERS.",
        )
        vol_alt, vol_cap = (
            "Ejemplo de peso volumétrico: 40×40×3 cm y 200 g en báscula son 600 g de volumen",
            "Un ejemplo calculado, no una foto de almacén. Muchas líneas facturan el máximo entre báscula y volumen, a menudo L×W×H (cm) / 8000.",
        )
        zoek_alt, zoek_cap = (
            "Búsqueda de hoodie en el catálogo MyCNBox de w2clinks",
            "Resultados con columna de filtros. Captura 6 Oct 2026.",
        )
        diy_alt, diy_cap = (
            "Búsqueda MyCNBox: pegar un enlace Taobao, 1688 o Weidian",
            f"Barra pública en www.mycnbox.com, {DATE}. Esta guía no inventa un pedido relleno.",
        )
    elif loc == "fr":
        off_alt, off_cap = (
            "Page d’accueil officielle MyCNBox : recherche, bannière coupon et connexion",
            f"www.mycnbox.com, {DATE}. L’estimateur est sur {EST_PATH}. Ce guide n’invente ni ligne ni montant.",
        )
        sheet_alt, sheet_cap = (
            "Catalogue MyCNBox sur w2clinks : fiches avec photo, marque et prix de référence",
            "Des fiches, pas des cellules Excel. Les prix en yuan changent chaque jour. Capture 6 Oct 2026, catégorie SNEAKERS.",
        )
        vol_alt, vol_cap = (
            "Exemple de poids volumétrique : 40×40×3 cm et 200 g à la balance deviennent 600 g de volume",
            "Un exemple calculé, pas une photo d’entrepôt. Beaucoup de lignes facturent le max entre balance et volume, souvent L×W×H (cm) / 8000.",
        )
        zoek_alt, zoek_cap = (
            "Recherche hoodie dans le catalogue MyCNBox sur w2clinks",
            "Résultats avec colonne de filtres. Capture 6 Oct 2026.",
        )
        diy_alt, diy_cap = (
            "Recherche MyCNBox : coller un lien Taobao, 1688 ou Weidian",
            f"Barre publique sur www.mycnbox.com, {DATE}. Ce guide n’invente pas une commande remplie.",
        )
    else:
        off_alt, off_cap = (
            "Official MyCNBox homepage: search, coupon banner and sign-in",
            f"www.mycnbox.com, {DATE}. The estimator lives at {EST_PATH}. This desk does not invent a line or a dollar amount.",
        )
        sheet_alt, sheet_cap = (
            "MyCNBox catalogue on w2clinks: product cards with photo, brand and reference price",
            "Cards, not Excel cells. Yuan prices change by the day. Capture 6 Oct 2026, category SNEAKERS.",
        )
        vol_alt, vol_cap = (
            "Worked example of volume weight: 40×40×3 cm and 200 g scale becomes 600 g volume",
            "A worked example, not a warehouse photo. Many lines bill the greater of scale and volume, often L×W×H (cm) / 8000.",
        )
        zoek_alt, zoek_cap = (
            "Hoodie search in the MyCNBox catalogue on w2clinks",
            "Results with the filter column. Capture 6 Oct 2026.",
        )
        diy_alt, diy_cap = (
            "MyCNBox search: paste a Taobao, 1688 or Weidian link",
            f"Public paste bar on www.mycnbox.com, {DATE}. This desk does not invent a filled order total.",
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
    if loc == "de":
        return f"""
<section class="sec" id="shots">
  <div class="wrap"><div class="split split--rev"><div>
    <h2>Einen chinesischen Link einfügen, oder in der App suchen</h2>
    <p class="lead">MyCNBox beginnt so: einen Link von Taobao, 1688 oder Weidian einfügen, oder den Namen tippen. Der chinesische Shop sieht MyCNBox; du siehst danach Lagerfotos und eine Linie nach {escape(dest)}.</p>
    <p>Liest die Suche den Link nicht, ist das manuelle Formular der nächste Schritt: Name, Größe, Farbe und Preis in Yuan. International zahlst du erst später, aus dem Lager.</p>
    <p><a class="btn" href="{escape(p["guide"])}">Anleitung Schritt für Schritt</a>
       <a class="btn btn--ghost" href="{escape(OFFICIAL)}" rel="noopener">Offizielle Site</a></p>
  </div>{fig}</div></div>
</section>
"""
    if loc == "nl":
        return f"""
<section class="sec" id="shots">
  <div class="wrap"><div class="split split--rev"><div>
    <h2>Plak een Chinese link, of zoek in de app</h2>
    <p class="lead">MyCNBox start zo: je plakt een Taobao-, 1688- of Weidian-link, of typt de naam. De Chinese shop ziet MyCNBox; jij ziet daarna magazijnfoto’s en een lijn naar {escape(dest)}.</p>
    <p>Leest de zoekbalk de link niet, is het handmatige formulier de volgende stap: naam, maat, kleur en prijs in yuan. Internationaal betaal je later, vanuit het magazijn.</p>
    <p><a class="btn" href="{escape(p["guide"])}">Handleiding stap voor stap</a>
       <a class="btn btn--ghost" href="{escape(OFFICIAL)}" rel="noopener">Officiële site</a></p>
  </div>{fig}</div></div>
</section>
"""
    if loc == "pl":
        return f"""
<section class="sec" id="shots">
  <div class="wrap"><div class="split split--rev"><div>
    <h2>Wklej chiński link albo szukaj w aplikacji</h2>
    <p class="lead">MyCNBox zaczyna się tak: wklejasz link Taobao, 1688 albo Weidian, albo wpisujesz nazwę. Chiński sklep widzi MyCNBox; Ty potem widzisz zdjęcia magazynu i linię do {escape(dest)}.</p>
    <p>Jeśli wyszukiwarka nie czyta linku, następny krok to formularz ręczny: nazwa, rozmiar, kolor i cena w juanach. Międzynarodowy płacisz później, z magazynu.</p>
    <p><a class="btn" href="{escape(p["guide"])}">Poradnik krok po kroku</a>
       <a class="btn btn--ghost" href="{escape(OFFICIAL)}" rel="noopener">Strona oficjalna</a></p>
  </div>{fig}</div></div>
</section>
"""
    if loc == "es":
        return f"""
<section class="sec" id="shots">
  <div class="wrap"><div class="split split--rev"><div>
    <h2>Pega un enlace chino, o busca en la app</h2>
    <p class="lead">MyCNBox empieza así: pegas un enlace de Taobao, 1688 o Weidian, o escribes el nombre. La tienda china ve MyCNBox; tú luego ves fotos de almacén y una línea hacia {escape(dest)}.</p>
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
    <p class="lead">MyCNBox commence ainsi : tu colles un lien Taobao, 1688 ou Weidian, ou tu tapes le nom. La boutique chinoise voit MyCNBox ; toi, tu vois ensuite les photos d’entrepôt et une ligne vers {escape(dest)}.</p>
    <p>Si la recherche ne lit pas le lien, l’étape suivante est le formulaire manuel : nom, taille, couleur et prix en yuan. L’international se paie plus tard, depuis l’entrepôt.</p>
    <p><a class="btn" href="{escape(p["guide"])}">Guide pas à pas</a>
       <a class="btn btn--ghost" href="{escape(OFFICIAL)}" rel="noopener">Site officiel</a></p>
  </div>{fig}</div></div>
</section>
"""
    return f"""
<section class="sec" id="shots">
  <div class="wrap"><div class="split split--rev"><div>
    <h2>Paste a Chinese link, or search in the app</h2>
    <p class="lead">MyCNBox starts the same way: paste a Taobao, 1688 or Weidian link, or type the name. The Chinese shop sees MyCNBox; you later see warehouse photos and a line to {escape(dest)}.</p>
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
    if loc == "de":
        store = escape(_storage(loc))
        return f"""
<section class="sec" id="states">
  <div class="wrap"><div class="split"><div>
    <h2>Neun Status, drei Bildschirme</h2>
    <p class="lead">Zuerst zahlst du das Produkt plus den Inlandsweg in China bis zum Lager. International kommt später, wenn du eine Linie nach {escape(dest)} wählst. «Warum steht es still?» heißt fast immer: du schaust auf den falschen Bildschirm.</p>
    <p>Die ersten Schritte liegen unter Bestellungen, danach Lager, danach das Paket, das du absendest. {store}</p>
    <p><a class="btn" href="{escape(p["guide"])}">Anleitung mit dem Verlauf</a></p>
  </div>{fig}</div></div>
</section>
"""
    if loc == "nl":
        store = escape(_storage(loc))
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
    if loc == "pl":
        store = escape(_storage(loc))
        return f"""
<section class="sec" id="states">
  <div class="wrap"><div class="split"><div>
    <h2>Dziewięć statusów, trzy ekrany</h2>
    <p class="lead">Najpierw płacisz produkt plus krajowy transport w Chinach do magazynu. Międzynarodowy przychodzi później, gdy wybierasz linię do {escape(dest)}. «Dlaczego stoi?» prawie zawsze znaczy: patrzysz na zły ekran.</p>
    <p>Pierwsze kroki są pod zamówieniami, potem magazyn, potem paczka, którą nadajesz. {store}</p>
    <p><a class="btn" href="{escape(p["guide"])}">Poradnik z przebiegiem</a></p>
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
    if loc == "de":
        return f"""
<section class="sec sec--tint" id="restricted">
  <div class="wrap"><div class="split split--rev"><div>
    <h2>Viele Produkte kannst du nicht kaufen, auch wenn sie da stehen</h2>
    <p class="lead">Auf der offiziellen Site siehst du Karten ohne Preis, oder ein manuelles Formular statt einer Shopkarte. Das ist kein Fehler dieser Homepage: der Quellenlink ist über den Agenten nicht kaufbar, oder der Preis ließ sich nicht lesen.</p>
    <p>Regel: ohne echten Preis und Varianten nicht bestellen. Tabak, Alkohol und Arzneimittel reisen nicht. Restricted ist eine Kaufsperre, kein Bescheid vom {escape(customs)}. MyCNBox verkauft keine eigene Ware.</p>
  </div>{fig}</div></div>
</section>
"""
    if loc == "nl":
        return f"""
<section class="sec sec--tint" id="restricted">
  <div class="wrap"><div class="split split--rev"><div>
    <h2>Veel producten kun je niet kopen, ook al staan ze er</h2>
    <p class="lead">Op de officiële site zie je kaarten zonder prijs, of een handmatig formulier in plaats van een shopkaart. Dat is geen bug van deze homepage: de bronlink is via de agent niet te koop, of de prijs liet zich niet lezen.</p>
    <p>Regel: zonder echte prijs en varianten niet bestellen. Tabak, alcohol en geneesmiddelen reizen niet. Restricted is een koopblokkade, geen bericht van {escape(customs)}. MyCNBox verkoopt geen eigen voorraad.</p>
  </div>{fig}</div></div>
</section>
"""
    if loc == "pl":
        return f"""
<section class="sec sec--tint" id="restricted">
  <div class="wrap"><div class="split split--rev"><div>
    <h2>Wielu produktów nie kupisz, choć się wyświetlają</h2>
    <p class="lead">Na stronie oficjalnej widzisz karty bez ceny albo formularz ręczny zamiast karty sklepu. To nie błąd tej strony: link źródłowy nie da się kupić przez agenta, albo cena się nie odczytała.</p>
    <p>Zasada: bez prawdziwej ceny i wariantów nie zamawiaj. Tytoń, alkohol i leki nie jadą. Restricted to blokada zakupu, nie zawiadomienie {escape(customs)}. MyCNBox nie sprzedaje własnego towaru.</p>
  </div>{fig}</div></div>
</section>
"""
    if loc == "es":
        return f"""
<section class="sec sec--tint" id="restricted">
  <div class="wrap"><div class="split split--rev"><div>
    <h2>Muchos productos no se pueden comprar aunque aparezcan</h2>
    <p class="lead">En el sitio oficial ves fichas sin precio, o un formulario manual en lugar de una ficha de tienda. No es un fallo de esta portada: el enlace de origen no se puede comprar por el agente, o el precio no se leyó.</p>
    <p>Regla: sin precio real y variantes, no pidas. Tabaco, alcohol y medicamentos no viajan. Restricted es un bloqueo de compra, no un aviso de {escape(customs)}. MyCNBox no vende mercancía propia.</p>
  </div>{fig}</div></div>
</section>
"""
    if loc == "fr":
        return f"""
<section class="sec sec--tint" id="restricted">
  <div class="wrap"><div class="split split--rev"><div>
    <h2>Beaucoup de produits ne s’achètent pas même s’ils s’affichent</h2>
    <p class="lead">Sur le site officiel tu vois des fiches sans prix, ou un formulaire manuel à la place d’une fiche boutique. Ce n’est pas un bug de cette page d’accueil : le lien source n’est pas achetable via l’agent, ou le prix n’a pas pu être lu.</p>
    <p>Règle : sans vrai prix et variantes, n’ordonne pas. Tabac, alcool et médicaments ne voyagent pas. Restricted est un blocage d’achat, pas un avis de {escape(customs)}. MyCNBox ne vend pas de stock propre.</p>
  </div>{fig}</div></div>
</section>
"""
    return f"""
<section class="sec sec--tint" id="restricted">
  <div class="wrap"><div class="split split--rev"><div>
    <h2>Many products you cannot buy even if they appear</h2>
    <p class="lead">On the official site you will see cards without a price, or a manual form instead of a shop card. That is not a bug of this homepage: the source link is not buyable through the agent, or the price could not be read.</p>
    <p>Rule: without a real price and variants, do not order. Tobacco, alcohol and medicines do not travel. Restricted is a purchase block, not a {escape(customs)} seizure notice. MyCNBox does not sell its own stock.</p>
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
    if loc == "de":
        hero = _hero(key, "Offizielle MyCNBox-Startseite", "Produkte auf w2clinks suchen", "Suche Turnschuhe, Hoodie, Jacke…", "Suchen")
        body = f"""{hero}
<section class="sec sec--first" id="agent">
  <div class="wrap"><div class="split"><div>
    <h2>Ein Einkaufsagent ist ein Zwischenhändler, kein Shop</h2>
    <p class="lead">MyCNBox verkauft keine eigene Ware. Er kauft für dich in chinesischen Shops, die nicht ins Ausland senden, nimmt das Paket im Lager an, fotografiert es, lagert es und schickt es nach {escape(dest)}, wenn du das entscheidest.</p>
    <p>Du zahlst zweimal (zuerst das Produkt, später international) und wartest zweimal. Dazwischen kannst du noch stornieren, bündeln oder die Linie wechseln. Zahlung und Tickets bleiben auf {escape(OFFICIAL)}.</p>
    <p><a class="btn" href="{escape(p["guide"])}">Anleitung Schritt für Schritt</a></p>
  </div>{fig_off}</div></div>
</section>
{shots}
<section class="sec sec--tint" id="sheet-explain">
  <div class="wrap"><div class="split split--rev"><div>
    <span class="eyebrow" style="color:var(--acd)">Ein irreführender Name</span>
    <h2>Ein Spreadsheet ist keine Excel-Datei</h2>
    <p class="lead">«Spreadsheet» klingt nach Zeilen und Spalten. Hier meint es einen Katalog aus Produktkarten mit Foto, Marke, Referenzpreis und dem Link, den du in den Agenten einfügst.</p>
    <p>Was du auf w2clinks siehst, sind Karten, keine Zellen.</p>
    <p><a class="btn btn--ghost" href="{escape(p["catalog"])}">So funktioniert der Katalog</a></p>
  </div>{fig_sheet}</div></div>
</section>
<section class="sec" id="cat-wall">
  <div class="wrap">
    <h2>Dreiunddreißig Kategorien für den ersten Tag</h2>
    <p class="lead">Jede Karte öffnet die Kategorie im Katalog. Fang mit einer an: fünf Kategorien in der ersten Haul sind der schnellste Weg zu einer teuren, unbequemen Box.</p>
    <div class="cat-grid">{wall}</div>
  </div>
</section>
{states}
<section class="sec sec--tint" id="lab">
  <div class="wrap"><div class="split"><div>
    <h2>{escape(dest)} hat Linien, aber nicht jede Linie ist offen</h2>
    <p class="lead">Im Schätzer Ziel <strong>{escape(p["dest_zh"])}</strong> wählen, nicht EU, nicht AT. Die Lieferadresse ist eine {escape(p["postal"])}.</p>
    <p>Der offizielle Schätzer steht auf {escape(EST)}: das Land wählen, nicht diesen Hostnamen. Dieser Desk erfindet keine Linie, keine Transitzeit und keinen Betrag. Quelle: <a href="{escape(p["customs_url"])}" rel="noopener">{escape(p["customs"])}</a>.</p>
    <p><a class="btn" href="{escape(EST)}">Offizieller MyCNBox-Schätzer</a>
       <a class="btn btn--ghost" href="{escape(p["ship"])}">Versandplan</a></p>
  </div>{fig_off}</div></div>
</section>
<section class="sec" id="volume">
  <div class="wrap"><div class="split split--rev"><div>
    <h2>Das Gewicht, das du zahlst, ist fast nie nur die Waage</h2>
    <p class="lead">Viele Linien rechnen das Maximum aus Waage und Volumen. Ein üblicher Teiler ist L×B×H (cm) / 8000. Eine Daunenjacke ist leicht und voluminös: dort entscheidet das Volumen.</p>
    <p>Beispiel: 40×40×3 cm sind 4800 cm³, geteilt durch 8000 sind 600 g Volumen bei 200 g Echtgewicht. Deine Maße trägst du im offiziellen Schätzer ein, Ziel {escape(p["dest_zh"].split("—")[0].strip())}.</p>
  </div>{fig_vol}</div></div>
</section>
{restricted}
<section class="sec" id="faq">
  <div class="wrap">
    <h2>Hilfe, News und wo du fragst</h2>
    <p class="lead">Die meisten Zweifel der ersten Bestellung wiederholen sich. Sie stehen auf Hilfe — eine eigene URL, kein Anhang dieser Homepage.</p>
    <p><a class="btn" href="{escape(p["help"])}">Alle Fragen auf Hilfe</a>
       <a class="btn btn--ghost" href="{escape(p["news"])}">Datierte Checks auf News</a>
       <a class="btn btn--ghost" href="{escape(p["about"])}">Über uns</a></p>
  </div>
</section>
"""
        desc = f"Unabhängiger Leitfaden auf Deutsch: wie du über MyCNBox in China kaufst, wie der w2clinks-Katalog funktioniert, wie ein Paket nach {dest} reist."
    elif loc == "nl":
        hero = _hero(key, "Officiële MyCNBox-homepage", "Producten zoeken op w2clinks", "Zoek sneakers, hoodie, jas…", "Zoeken")
        body = f"""{hero}
<section class="sec sec--first" id="agent">
  <div class="wrap"><div class="split"><div>
    <h2>Een inkoopagent is een tussenpersoon, geen shop</h2>
    <p class="lead">MyCNBox verkoopt geen eigen voorraad. Hij koopt voor jou in Chinese shops die niet naar het buitenland sturen, neemt het pakket in het magazijn aan, fotografeert het, slaat het op en stuurt het naar {escape(dest)} wanneer jij dat beslist.</p>
    <p>Je betaalt twee keer (eerst het product, later internationaal) en wacht twee keer. Daartussen kun je nog annuleren, bundelen of van lijn wisselen. Betaling en tickets blijven op {escape(OFFICIAL)}.</p>
    <p><a class="btn" href="{escape(p["guide"])}">Handleiding stap voor stap</a></p>
  </div>{fig_off}</div></div>
</section>
{shots}
<section class="sec sec--tint" id="sheet-explain">
  <div class="wrap"><div class="split split--rev"><div>
    <span class="eyebrow" style="color:var(--acd)">Een misleidende naam</span>
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
    <p class="lead">In de schatter bestemming <strong>{escape(p["dest_zh"])}</strong> kiezen, niet EU. Het afleveradres is een {escape(p["postal"])}.</p>
    <p>De officiële schatter staat op {escape(EST)}: kies het land, niet deze hostname. Deze gids verzint geen lijn, transittijd of bedrag. Bron: <a href="{escape(p["customs_url"])}" rel="noopener">{escape(p["customs"])}</a>.</p>
    <p><a class="btn" href="{escape(EST)}">Officiële MyCNBox-schatter</a>
       <a class="btn btn--ghost" href="{escape(p["ship"])}">Verzendplan</a></p>
  </div>{fig_off}</div></div>
</section>
<section class="sec" id="volume">
  <div class="wrap"><div class="split split--rev"><div>
    <h2>Het gewicht dat je betaalt is bijna nooit alleen de weegschaal</h2>
    <p class="lead">Veel lijnen factureren het maximum van weegschaal en volume. Een gangbare deler is L×W×H (cm) / 8000. Een donsjas is licht en volumineus: daar beslist het volume.</p>
    <p>Voorbeeld: 40×40×3 cm is 4800 cm³, gedeeld door 8000 is 600 g volume bij 200 g echt gewicht. Jouw maten voer je in de officiële schatter in, bestemming {escape(p["dest_zh"].split("—")[0].strip())}.</p>
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
        desc = f"Onafhankelijke gids in het Nederlands: hoe je via MyCNBox in China koopt, hoe de w2clinks-catalogus werkt, hoe een pakket naar {dest} reist."
    elif loc == "pl":
        hero = _hero(key, "Oficjalna strona MyCNBox", "Szukaj produktów na w2clinks", "Szukaj buty, hoodie, kurtka…", "Szukaj")
        body = f"""{hero}
<section class="sec sec--first" id="agent">
  <div class="wrap"><div class="split"><div>
    <h2>Agent zakupowy to pośrednik, nie sklep</h2>
    <p class="lead">MyCNBox nie sprzedaje własnego towaru. Kupuje za Ciebie w chińskich sklepach, które nie wysyłają za granicę, przyjmuje paczkę w magazynie, fotografuje, przechowuje i wysyła do {escape(dest)}, kiedy Ty zdecydujesz.</p>
    <p>Płacisz dwa razy (najpierw produkt, później międzynarodowy) i czekasz dwa razy. Pomiędzy możesz jeszcze anulować, łączyć albo zmienić linię. Płatności i zgłoszenia zostają na {escape(OFFICIAL)}.</p>
    <p><a class="btn" href="{escape(p["guide"])}">Poradnik krok po kroku</a></p>
  </div>{fig_off}</div></div>
</section>
{shots}
<section class="sec sec--tint" id="sheet-explain">
  <div class="wrap"><div class="split split--rev"><div>
    <span class="eyebrow" style="color:var(--acd)">Nazwa, która myli</span>
    <h2>Spreadsheet nie jest plikiem Excel</h2>
    <p class="lead">Po polsku «spreadsheet» brzmi jak siatka wierszy. Tu to katalog kart produktów ze zdjęciem, marką, ceną orientacyjną i linkiem, który wklejasz do agenta.</p>
    <p>Na w2clinks widzisz karty, nie komórki.</p>
    <p><a class="btn btn--ghost" href="{escape(p["catalog"])}">Jak działa katalog</a></p>
  </div>{fig_sheet}</div></div>
</section>
<section class="sec" id="cat-wall">
  <div class="wrap">
    <h2>Trzydzieści trzy kategorie na pierwszy dzień</h2>
    <p class="lead">Każda karta otwiera tę kategorię w katalogu. Zacznij od jednej: pięć kategorii w pierwszym haulu to najszybsza droga do drogiej, niewygodnej paczki.</p>
    <div class="cat-grid">{wall}</div>
  </div>
</section>
{states}
<section class="sec sec--tint" id="lab">
  <div class="wrap"><div class="split"><div>
    <h2>{escape(dest)} ma linie, ale nie każda jest otwarta</h2>
    <p class="lead">W estymatorze wybierz cel <strong>{escape(p["dest_zh"])}</strong>, nie EU, nie DE. Adres to {escape(p["postal"])}.</p>
    <p>Oficjalny estymator jest na {escape(EST)}: wybierz kraj, nie ten hostname. Ten desk nie wymyśla linii, czasu tranzytu ani kwoty. Źródło: <a href="{escape(p["customs_url"])}" rel="noopener">{escape(p["customs"])}</a>.</p>
    <p><a class="btn" href="{escape(EST)}">Oficjalny estymator MyCNBox</a>
       <a class="btn btn--ghost" href="{escape(p["ship"])}">Plan wysyłki</a></p>
  </div>{fig_off}</div></div>
</section>
<section class="sec" id="volume">
  <div class="wrap"><div class="split split--rev"><div>
    <h2>Waga, którą płacisz, prawie nigdy nie jest samą wagą</h2>
    <p class="lead">Wiele linii liczy maksimum wagi i objętości. Częsty dzielnik to L×W×H (cm) / 8000. Kurtka puchowa jest lekka i puchata: tam decyduje objętość.</p>
    <p>Przykład: 40×40×3 cm to 4800 cm³, podzielone przez 8000 to 600 g objętości przy 200 g rzeczywistych. Swoje wymiary wpisujesz w oficjalnym estymatorze, cel {escape(p["dest_zh"].split("—")[0].strip())}.</p>
  </div>{fig_vol}</div></div>
</section>
{restricted}
<section class="sec" id="faq">
  <div class="wrap">
    <h2>Pomoc, aktualności i gdzie pytać</h2>
    <p class="lead">Wątpliwości pierwszych zamówień się powtarzają. Są na Pomocy — własny URL, nie dodatek tej strony.</p>
    <p><a class="btn" href="{escape(p["help"])}">Wszystkie pytania na Pomocy</a>
       <a class="btn btn--ghost" href="{escape(p["news"])}">Sprawdzenia z datą w Aktualnościach</a>
       <a class="btn btn--ghost" href="{escape(p["about"])}">O nas</a></p>
  </div>
</section>
"""
        desc = f"Niezależny przewodnik po polsku: jak kupujesz w Chinach przez MyCNBox, jak działa katalog w2clinks, jak paczka jedzie do {dest}."
    elif loc == "fr":
        hero = _hero(key, "Page d’accueil officielle MyCNBox", "Chercher des produits sur w2clinks", "Cherche baskets, hoodie, veste…", "Chercher")
        body = f"""{hero}
<section class="sec sec--first" id="agent">
  <div class="wrap"><div class="split"><div>
    <h2>Un agent d’achat est un intermédiaire, pas une boutique</h2>
    <p class="lead">MyCNBox ne vend pas de stock propre. Il achète pour toi dans des boutiques chinoises qui n’expédient pas à l’étranger, reçoit le colis en entrepôt, le photographie, le stocke et l’envoie vers {escape(dest)} quand tu le décides.</p>
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
    <p><a class="btn" href="{escape(EST)}">Estimateur officiel MyCNBox</a>
       <a class="btn btn--ghost" href="{escape(p["ship"])}">Plan de livraison</a></p>
  </div>{fig_off}</div></div>
</section>
<section class="sec" id="volume">
  <div class="wrap"><div class="split split--rev"><div>
    <h2>Le poids que tu paies n’est presque jamais la balance seule</h2>
    <p class="lead">Beaucoup de lignes facturent le maximum entre balance et volume. Un diviseur courant est L×W×H (cm) / 8000. Une doudoune est légère et volumineuse : c’est le volume qui décide.</p>
    <p>Exemple : 40×40×3 cm font 4800 cm³, divisés par 8000 font 600 g de volume pour 200 g réels. Tes mesures, tu les saisis dans l’estimateur officiel, destination {escape(p["dest_zh"].split("—")[0].strip())}.</p>
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
        desc = f"Guide indépendant en français : comment tu achètes en Chine via MyCNBox, comment marche le catalogue w2clinks, comment un colis voyage vers {dest}."
    elif loc == "es":
        hero = _hero(key, "Portada oficial de MyCNBox", "Buscar productos en w2clinks", "Busca zapatillas, hoodie, chaqueta…", "Buscar")
        body = f"""{hero}
<section class="sec sec--first" id="agent">
  <div class="wrap"><div class="split"><div>
    <h2>Un agente de compras es un intermediario, no una tienda</h2>
    <p class="lead">MyCNBox no vende mercancía propia. Compra por ti en tiendas chinas que no envían al extranjero, recibe el paquete en el almacén, lo fotografía, lo guarda y lo envía a {escape(dest)} cuando tú lo decides.</p>
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
    <p><a class="btn" href="{escape(EST)}">Estimador oficial MyCNBox</a>
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
        desc = f"Guía independiente en español: cómo compras en China con MyCNBox, cómo funciona el catálogo w2clinks, cómo viaja un paquete a {dest}."
    else:
        hero = _hero(key, "Official MyCNBox homepage", "Search products on w2clinks", "Search sneakers, hoodie, jacket…", "Search")
        body = f"""{hero}
<section class="sec sec--first" id="agent">
  <div class="wrap"><div class="split"><div>
    <h2>A purchasing agent is a middleman, not a shop</h2>
    <p class="lead">MyCNBox does not sell its own goods. It buys for you in Chinese shops that do not ship abroad, receives the parcel in the warehouse, photographs it, stores it, and ships to {escape(dest)} when you decide.</p>
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
    <p>What you see on w2clinks are cards, not cells. Each fiche has the link MyCNBox needs.</p>
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
    <p>The official estimator lives at www.mycnbox.com{escape(EST_PATH)} — pick the dest country, not this hostname. This desk does not invent a line, a transit-day count or a money amount. Open {escape(OFFICIAL)} the morning you ship. Import: <a href="{escape(p["customs_url"])}" rel="noopener">{escape(p["customs"])}</a>.</p>
    <p><a class="btn" href="{escape(EST)}">Official MyCNBox estimator</a>
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
            f"Independent English guide: how you buy in China through MyCNBox, how the w2clinks catalogue works, how a parcel travels to {dest}."
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
    notes = {"de": CAT_NOTES_DE, "es": CAT_NOTES_ES, "fr": CAT_NOTES_FR, "nl": CAT_NOTES_NL, "pl": CAT_NOTES_PL}.get(loc, CAT_NOTES_EN)
    wall = _wall(key, notes)
    _fig_off, fig_sheet, _fig_vol, fig_zoek, fig_diy = _shots(key)
    dest = p["dest_label"]
    sheet = _sheet(desk)
    keys = _keys_table(key)
    if loc == "de":
        topic = "was es ist und welche Kategorien du findest"
        body = f"""
<section class="sec sec--first"><div class="wrap"><div class="split"><div>
<span class="eyebrow" style="color:var(--acc)">Der Katalog</span>
<h1>Was MyCNBox Spreadsheet ist, und was du darin findest</h1>
<p class="lead">Ein Katalog aus Produktkarten, keine Excel-Datei. Dreiunddreißig Kategorien, Filter, Foto, Marke und der Link für den Agenten.</p>
</div>{fig_sheet}</div></div></section>
<section class="sec sec--tint"><div class="wrap"><div class="split split--rev"><div>
<h2>Warum ein eigener Katalog</h2>
<p>Die Suche eines Agenten gibt den ganzen chinesischen Bestand, riesig und oft auf Chinesisch. Ein Katalog hat die Hausaufgaben schon gemacht: jemand hat gewählt, welche Karten sich lohnen, sie in Kategorien gelegt und den Shop-Link bereitgelegt.</p>
<p>In der Praxis: du findest die Karte auf w2clinks, kopierst den Quellenlink und fügst ihn in die Suche von MyCNBox oder ins manuelle Formular ein. Der Katalog kassiert nichts und verkauft nichts.</p>
</div>{fig_zoek}</div></div></section>
<section class="sec" id="categorias"><div class="wrap">
<h2>Die dreiunddreißig Kategorien, und was du in jeder prüfst</h2>
<p class="lead">Der Satz unter jeder Karte ist kein Fülltext: es ist der Fehler, der in der Kategorie am häufigsten passiert, wenn du aus der Ferne kaufst.</p>
<div class="cat-grid cat-grid--rich">{wall}</div>
</div></section>
<section class="sec sec--tint" id="first-category"><div class="wrap">
<h2>Wie du die erste Kategorie wählst</h2>
<p class="lead">Erste Bestellung: etwas Flaches und Leichtes — T-Shirts, Shorts, Schmuck. Die kommen früher an, kosten weniger Porto, und du prüfst den ganzen Kreislauf ohne viel Geld.</p>
<p>Voluminöses für die zweite Order: Daunenjacken, Taschen, Mützen. Nicht weil sie schlechter sind, sondern weil ihr Porto vom Volumen abhängt — und das rechnest du erst gut, wenn du eine Runde gesehen hast.</p>
<p>Drei Kategorien mit Extra-Bedingungen: Elektronik (oft Lithium), Brillen (zerbrechlich) und alles mit Akku oder Magnet. Nicht jede Linie nach {escape(dest)} nimmt das. Schätzer prüfen, bevor sie im Lager liegen bleiben.</p>
</div></section>
<section class="sec" id="keys"><div class="wrap">
<h2>Unbequemes Faktum: der Katalog sucht auf Englisch</h2>
<p class="lead">Wir haben es Wort für Wort am {escape(DATE)} nachgeprüft. Das willst du wissen, bevor du die erste Suche auf Deutsch tippst.</p>
<p>Deutsche Schreibweisen wie Turnschuhe, Pullover oder Brille liefern oft null. Die englischen Keys sneakers, hoodie, jacket, trousers, bag, glasses oder watch liefern Seiten. Deshalb schickt die Homepage-Suche englische Keys zu w2clinks.</p>
{keys}
</div></section>
<section class="sec sec--tint"><div class="wrap"><div class="split"><div>
<h2>Vom Katalog zur Bestellung, ohne den Link zu verlieren</h2>
<p class="lead">Die Karte ist der Anfang, nicht die Kasse. Der Schritt, der am häufigsten schiefläuft: du kopierst die Katalog-URL statt des Shop-Links. MyCNBox braucht den Taobao-, 1688- oder Weidian-Link.</p>
<p>Klebst du die URL der Katalogkarte selbst, weiß der Agent nicht, was er kaufen soll. Kopiere den Shop-Link, füge ihn in die MyCNBox-Suche ein, prüfe Preis und Variante, und zahle international erst, wenn die Lagerfotos stimmen.</p>
<p>Liest die Suche den Link nicht, bleibt das manuelle Formular auf der offiziellen Site. Karten ohne Preis überspringen — der Quellenlink ist in China oft schon tot.</p>
<p><a class="btn" href="{escape(sheet)}">Katalog auf w2clinks öffnen</a>
   <a class="btn btn--ghost" href="{escape(p["guide"])}">Anleitung Schritt für Schritt</a></p>
</div>{fig_diy}</div></div></section>
"""
    elif loc == "nl":
        topic = "wat het is en welke categorieën je vindt"
        body = f"""
<section class="sec sec--first"><div class="wrap"><div class="split"><div>
<span class="eyebrow" style="color:var(--acc)">De catalogus</span>
<h1>Wat MyCNBox Spreadsheet is, en wat je erin vindt</h1>
<p class="lead">Een catalogus van productkaarten, geen Excel-bestand. Drieëndertig categorieën, filters, foto, merk en de link voor de agent.</p>
</div>{fig_sheet}</div></div></section>
<section class="sec sec--tint"><div class="wrap"><div class="split split--rev"><div>
<h2>Waarom een aparte catalogus</h2>
<p>De zoekbalk van een agent geeft de hele Chinese voorraad, enorm en vaak in het Chinees. Een catalogus heeft het huiswerk al gedaan: iemand koos welke kaarten de moeite waard zijn, zette ze in een categorie en legde de shoplink klaar.</p>
<p>In de praktijk: je vindt de kaart op w2clinks, kopieert de bronlink en plakt die in de MyCNBox-zoekbalk of het handmatige formulier. De catalogus int niets en verkoopt niets.</p>
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
<p class="lead">De kaart is het begin, niet de kassa. De stap die het vaakst misgaat: je kopieert de catalogus-URL in plaats van de shoplink. MyCNBox heeft de Taobao-, 1688- of Weidian-link nodig.</p>
<p>Plak je de URL van de cataloguskaart zelf, dan weet de agent niet wat hij moet kopen. Kopieer de shoplink, plak hem in de MyCNBox-zoekbalk, check prijs en variant, en betaal internationaal pas als de magazijnfoto’s kloppen.</p>
<p>Leest de zoekbalk de link niet, blijft het handmatige formulier op de officiële site. Kaarten zonder prijs overslaan — de bronlink is in China vaak al dood.</p>
<p><a class="btn" href="{escape(sheet)}">Catalogus op w2clinks openen</a>
   <a class="btn btn--ghost" href="{escape(p["guide"])}">Handleiding stap voor stap</a></p>
</div>{fig_diy}</div></div></section>
"""
    elif loc == "pl":
        topic = "czym jest i jakie kategorie znajdziesz"
        body = f"""
<section class="sec sec--first"><div class="wrap"><div class="split"><div>
<span class="eyebrow" style="color:var(--acc)">Katalog</span>
<h1>Czym jest MyCNBox Spreadsheet i co w nim znajdziesz</h1>
<p class="lead">Katalog kart produktów, nie plik Excel. Trzydzieści trzy kategorie, filtry, zdjęcie, marka i link dla agenta.</p>
</div>{fig_sheet}</div></div></section>
<section class="sec sec--tint"><div class="wrap"><div class="split split--rev"><div>
<h2>Dlaczego osobny katalog</h2>
<p>Wyszukiwarka agenta zwraca cały chiński stan, ogromny i często po chińsku. Katalog zrobił robotę: ktoś wybrał, które karty warto, włożył je w kategorię i zostawił link sklepu.</p>
<p>W praktyce: znajdujesz kartę na w2clinks, kopiujesz link źródłowy i wklejasz go w wyszukiwarkę MyCNBox albo formularz ręczny. Katalog nic nie kasuje i nic nie sprzedaje.</p>
</div>{fig_zoek}</div></div></section>
<section class="sec" id="categorias"><div class="wrap">
<h2>Trzydzieści trzy kategorie i co sprawdzasz w każdej</h2>
<p class="lead">Zdanie pod każdą kartą to nie wypełniacz: to błąd, który w tej kategorii wraca najczęściej, gdy kupujesz z daleka.</p>
<div class="cat-grid cat-grid--rich">{wall}</div>
</div></section>
<section class="sec sec--tint" id="first-category"><div class="wrap">
<h2>Jak wybierasz pierwszą kategorię</h2>
<p class="lead">Pierwsze zamówienie: coś płaskiego i lekkiego — t-shirty, szorty, biżuteria. Przychodzą wcześniej, kosztują mniej porto, i sprawdzasz cały obieg bez dużego ryzyka.</p>
<p>Objętościowe na drugie zamówienie: kurtki puchowe, torby, czapki. Nie dlatego, że gorsze, tylko dlatego, że porto zależy od objętości — a to liczysz dobrze po jednej rundzie.</p>
<p>Trzy kategorie z dodatkowymi warunkami: elektronika (często lit), okulary (kruche) i wszystko z baterią albo magnesem. Nie każda linia do {escape(dest)} to bierze. Sprawdź estymator zanim zostaną w magazynie.</p>
</div></section>
<section class="sec" id="keys"><div class="wrap">
<h2>Niewygodny fakt: katalog szuka po angielsku</h2>
<p class="lead">Sprawdziliśmy to słowo po słowie {escape(DATE)}. Chcesz to wiedzieć zanim wpiszesz pierwsze wyszukiwanie po polsku.</p>
<p>Lokalne zapisy jak buty, bluza albo okulary często dają zero. Angielskie keys sneakers, hoodie, jacket, trousers, bag, glasses albo watch dają strony. Dlatego wyszukiwarka na stronie głównej wysyła angielskie keys do w2clinks.</p>
{keys}
</div></section>
<section class="sec sec--tint"><div class="wrap"><div class="split"><div>
<h2>Z katalogu do zamówienia, bez zgubienia linku</h2>
<p class="lead">Karta to początek, nie kasa. Krok, który najczęściej pada: kopiujesz URL karty katalogu zamiast linku sklepu. MyCNBox potrzebuje linku Taobao, 1688 albo Weidian.</p>
<p>Jeśli wkleisz URL samej karty katalogu, agent nie wie, co kupić. Skopiuj link sklepu, wklej w wyszukiwarkę MyCNBox, sprawdź cenę i wariant, i zapłać międzynarodowy dopiero gdy zdjęcia magazynu się zgadzają.</p>
<p>Jeśli wyszukiwarka nie czyta linku, zostaje formularz ręczny na stronie oficjalnej. Karty bez ceny pomiń — link źródłowy w Chinach często już nie żyje.</p>
<p><a class="btn" href="{escape(sheet)}">Otwórz katalog na w2clinks</a>
   <a class="btn btn--ghost" href="{escape(p["guide"])}">Poradnik krok po kroku</a></p>
</div>{fig_diy}</div></div></section>
"""
    elif loc == "fr":
        topic = "ce que c’est et quelles catégories tu trouves"
        body = f"""
<section class="sec sec--first"><div class="wrap"><div class="split"><div>
<span class="eyebrow" style="color:var(--acc)">Le catalogue</span>
<h1>Ce qu’est MyCNBox Spreadsheet, et ce que tu y trouves</h1>
<p class="lead">Un catalogue de fiches produit, pas un fichier Excel. Trente-trois catégories, filtres, photo, marque et le lien pour l’agent.</p>
</div>{fig_sheet}</div></div></section>
<section class="sec sec--tint"><div class="wrap"><div class="split split--rev"><div>
<h2>Pourquoi un catalogue à part</h2>
<p>La recherche de l’agent renvoie tout le stock chinois, énorme et souvent en chinois. Un catalogue a déjà fait le travail : quelqu’un a choisi quelles fiches valent, les a mises en catégorie et a préparé le lien boutique.</p>
<p>En pratique : tu trouves la fiche sur w2clinks, tu copies le lien source et tu le colles dans la recherche MyCNBox ou le formulaire manuel. Le catalogue n’encaisse rien et ne vend rien.</p>
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
<p class="lead">La fiche est le début, pas la caisse. L’étape qui rate le plus : tu copies l’URL de la fiche catalogue au lieu du lien boutique. MyCNBox a besoin du lien Taobao, 1688 ou Weidian.</p>
<p>Si tu colles l’URL de la fiche catalogue, l’agent ne sait pas quoi acheter. Copie le lien boutique, colle-le dans la recherche MyCNBox, vérifie prix et variante, et paie l’international seulement quand les photos d’entrepôt collent.</p>
<p>Si la recherche ne lit pas le lien, reste le formulaire manuel du site officiel. Fiches sans prix : saute-les — le lien source en Chine est souvent déjà mort.</p>
<p><a class="btn" href="{escape(sheet)}">Ouvrir le catalogue sur w2clinks</a>
   <a class="btn btn--ghost" href="{escape(p["guide"])}">Guide pas à pas</a></p>
</div>{fig_diy}</div></div></section>
"""
    elif loc == "es":
        topic = "qué es y qué categorías encuentras"
        body = f"""
<section class="sec sec--first"><div class="wrap"><div class="split"><div>
<span class="eyebrow" style="color:var(--acc)">El catálogo</span>
<h1>Qué es MyCNBox Spreadsheet, y qué encuentras dentro</h1>
<p class="lead">Un catálogo de fichas de producto, no un archivo Excel. Treinta y tres categorías, filtros, foto, marca y el enlace para el agente.</p>
</div>{fig_sheet}</div></div></section>
<section class="sec sec--tint"><div class="wrap"><div class="split split--rev"><div>
<h2>Por qué un catálogo aparte</h2>
<p>La búsqueda del agente devuelve todo el stock chino, enorme y a menudo en chino. Un catálogo ya hizo el trabajo: alguien eligió qué fichas merecen, las puso en categoría y dejó listo el enlace de la tienda.</p>
<p>En la práctica: encuentras la ficha en w2clinks, copias el enlace de origen y lo pegas en la búsqueda de MyCNBox o en el formulario manual. El catálogo no cobra y no vende.</p>
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
<p class="lead">La ficha es el principio, no la caja. El paso que más falla: copias la URL de la ficha del catálogo en vez del enlace de la tienda. MyCNBox necesita el enlace Taobao, 1688 o Weidian.</p>
<p>Si pegas la URL de la ficha del catálogo, el agente no sabe qué comprar. Copia el enlace de la tienda, pégalo en la búsqueda de MyCNBox, revisa precio y variante, y paga el internacional solo cuando las fotos de almacén cuadran.</p>
<p>Si la búsqueda no lee el enlace, queda el formulario manual del sitio oficial. Fichas sin precio: sáltalas — el enlace de origen en China a menudo ya está muerto.</p>
<p><a class="btn" href="{escape(sheet)}">Abrir el catálogo en w2clinks</a>
   <a class="btn btn--ghost" href="{escape(p["guide"])}">Guía paso a paso</a></p>
</div>{fig_diy}</div></div></section>
"""
    else:
        topic = "what it is and which categories you will find"
        body = f"""
<section class="sec sec--first"><div class="wrap"><div class="split"><div>
<span class="eyebrow" style="color:var(--acc)">The catalogue</span>
<h1>What MyCNBox Spreadsheet is, and what you find in it</h1>
<p class="lead">It is a catalogue of product cards, not an Excel file. Thirty-three categories, filters, and cards with a photo, a brand and the link for the agent.</p>
</div>{fig_sheet}</div></div></section>
<section class="sec sec--tint"><div class="wrap"><div class="split split--rev"><div>
<h2>Why a separate catalogue</h2>
<p>An agent search bar returns the whole stock of Chinese shops, huge and often in Chinese. A catalogue does the homework: someone already picked which fiches are worth it, put them in a category and left the shop link ready.</p>
<p>In practice: you find the fiche on w2clinks, copy the source link and paste it into MyCNBox search or the manual form. The catalogue collects no money and sells nothing.</p>
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
<p class="lead">The fiche is the start, not checkout. The step that fails most often is copying the catalogue URL instead of the shop link. MyCNBox needs the Taobao, 1688 or Weidian link.</p>
<p>If you paste the catalogue-card URL itself, the agent does not know what to buy. Copy the shop link, paste it into MyCNBox search, check price and variant, and pay international only after the warehouse photos match.</p>
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
    if loc == "de":
        topic = "Hilfe und häufige Fragen"
        body = f"""
<article class="pw">
  <span class="eyebrow" style="color:var(--acd)">Hilfe</span>
  <h1>Hilfe und Fragen zu MyCNBox in {escape(p["dest_label"])}</h1>
  <p class="lead">Fragen erster Bestellungen. Die Lieferadresse ist eine {escape(p["postal"])}.</p>
  {fig_off}{html_f}
  <p><a class="btn" href="{escape(EST)}">Offizieller MyCNBox-Schätzer</a>
     <a class="btn btn--ghost" href="{escape(p["ship"])}">Versandplan</a></p>
</article>
"""
    elif loc == "nl":
        topic = "hulp en veelgestelde vragen"
        body = f"""
<article class="pw">
  <span class="eyebrow" style="color:var(--acd)">Hulp</span>
  <h1>Hulp en vragen over MyCNBox in {escape(p["dest_label"])}</h1>
  <p class="lead">Vragen van eerste bestellingen. Het afleveradres is een {escape(p["postal"])}.</p>
  {fig_off}{html_f}
  <p><a class="btn" href="{escape(EST)}">Officiële MyCNBox-schatter</a>
     <a class="btn btn--ghost" href="{escape(p["ship"])}">Verzendplan</a></p>
</article>
"""
    elif loc == "pl":
        topic = "pomoc i częste pytania"
        body = f"""
<article class="pw">
  <span class="eyebrow" style="color:var(--acd)">Pomoc</span>
  <h1>Pomoc i pytania o MyCNBox w {escape(p["dest_label"])}</h1>
  <p class="lead">Pytania pierwszych zamówień. Adres dostawy to {escape(p["postal"])}.</p>
  {fig_off}{html_f}
  <p><a class="btn" href="{escape(EST)}">Oficjalny estymator MyCNBox</a>
     <a class="btn btn--ghost" href="{escape(p["ship"])}">Plan wysyłki</a></p>
</article>
"""
    elif loc == "es":
        topic = "ayuda y preguntas frecuentes"
        body = f"""
<article class="pw">
  <span class="eyebrow" style="color:var(--acd)">Ayuda</span>
  <h1>Ayuda y preguntas sobre MyCNBox en {escape(p["dest_label"])}</h1>
  <p class="lead">Preguntas de los primeros pedidos. La dirección es una {escape(p["postal"])}.</p>
  {fig_off}{html_f}
  <p><a class="btn" href="{escape(EST)}">Estimador oficial MyCNBox</a>
     <a class="btn btn--ghost" href="{escape(p["ship"])}">Plan de envío</a></p>
</article>
"""
    elif loc == "fr":
        topic = "aide et questions fréquentes"
        body = f"""
<article class="pw">
  <span class="eyebrow" style="color:var(--acd)">Aide</span>
  <h1>Aide et questions sur MyCNBox depuis {escape(p["dest_label"])}</h1>
  <p class="lead">Questions des premières commandes. L’adresse est une {escape(p["postal"])}.</p>
  {fig_off}{html_f}
  <p><a class="btn" href="{escape(EST)}">Estimateur officiel MyCNBox</a>
     <a class="btn btn--ghost" href="{escape(p["ship"])}">Plan de livraison</a></p>
</article>
"""
    else:
        topic = "help and frequently asked questions"
        body = f"""
<article class="pw">
  <span class="eyebrow" style="color:var(--acd)">Help</span>
  <h1>Help and questions about MyCNBox in {escape(p["dest_label"])}</h1>
  <p class="lead">Questions that come back on first orders. The delivery address uses a {escape(p["postal"])}.</p>
  {fig_off}{html_f}
  <p><a class="btn" href="{escape(EST)}">Official MyCNBox estimator</a>
     <a class="btn btn--ghost" href="{escape(p["ship"])}">Shipping plan</a></p>
</article>
"""
    return cms_shell(
        desk, page_title(desk, topic),
        f"FAQ about MyCNBox from {p['dest_label']}.",
        f"https://{p['host']}{p['help']}", [faq_ld(p["lang"], pairs)], body, p["help"],
    )


def build_news(key: str) -> str:
    p = PACKS[key]
    desk = desk_for(key)
    loc = p["loc"]
    if loc == "de":
        items = [
            ("Erste Runde: der offizielle Schätzer",
             f"Am {DATE} kommen Frachtzahlen nur aus {EST}: das Land wählen, nicht diesen Hostnamen. Keine erfundene Linie.",
             f"Am Versandmorgen die offizielle Site öffnen, Ziel {p['dest_zh']}. {p['postal']}."),
            ("w2clinks sucht auf Englisch",
             "sneakers, hoodie, jacket liefern Seiten; Turnschuhe oft null. Gemessen 6 Oct 2026.",
             "Englischen Key tippen oder einen Chip auf der Homepage antippen."),
            ("Lager: 90 Tage im offiziellen Help",
             _storage("de"),
             "Die Konsolidierung so planen, dass das erste Stück nicht bis zum letzten Tag wartet."),
            ("Schwester-Hosts bleiben getrennt",
             "UK, DE, ES, FR, NL und PL sind eigene Dateien. Kein 301 untereinander, kein 301 auf mycnbox.eu, mycnboxhaul.com oder mycnboxhual.com.",
             "Die Hubs mycnbox.eu / mycnboxhaul.com / mycnboxhual.com sind kein Zollgebiet."),
        ]
        h1, topic, brow = "Was wir auf der Plattform geprüft haben, mit Datum", "was wir auf der Plattform geprüft haben", "News"
        lead = "Das ist kein Firmennewsletter. Eigene Checks, mit Datum."
    elif loc == "nl":
        items = [
            ("Eerste ronde: de officiële schatter",
             f"Op {DATE} komen vrachtcijfers alleen uit {EST}: kies het land, niet deze hostname. Geen verzonnen lijn.",
             f"Open de officiële site de ochtend dat je verzendt, bestemming {p['dest_zh']}. {p['postal']}."),
            ("w2clinks zoekt in het Engels",
             "sneakers, hoodie, jacket geven pagina’s; lokale spellingen vaak nul. Gemeten 6 Oct 2026.",
             "Typ de Engelse key, of tik een chip op de homepage."),
            ("Magazijn: 90 dagen in de officiële Help",
             _storage("nl"),
             "Plan de consolidatie zodat het eerste stuk niet tot de laatste dag wacht."),
            ("Zusthosts blijven apart",
             "UK, DE, ES, FR, NL en PL zijn eigen bestanden. Geen 301 onderling, geen 301 naar mycnbox.eu, mycnboxhaul.com of mycnboxhual.com.",
             "De hubs mycnbox.eu / mycnboxhaul.com / mycnboxhual.com zijn geen douanegebied."),
        ]
        h1, topic, brow = "Wat we op het platform hebben nagekeken, met datum", "wat we op het platform hebben nagekeken", "Nieuws"
        lead = "Dit is geen bedrijfsnieuwsbrief. Eigen checks, met datum."
    elif loc == "pl":
        items = [
            ("Pierwsza runda: oficjalny estymator",
             f"{DATE} liczby frachtu wychodzą tylko z {EST}: wybierz kraj, nie ten hostname. Żadnej wymyślonej linii.",
             f"Rano w dniu nadania otwórz stronę oficjalną, cel {p['dest_zh']}. {p['postal']}."),
            ("w2clinks szuka po angielsku",
             "sneakers, hoodie, jacket dają strony; lokalne zapisy często zero. Zmierzono 6 Oct 2026.",
             "Wpisz angielski key albo stuknij chip na stronie głównej."),
            ("Magazyn: 90 dni w oficjalnym Help",
             _storage("pl"),
             "Zaplanuj konsolidację, żeby pierwsza sztuka nie czekała do ostatniego dnia."),
            ("Hosty siostrzane zostają osobno",
             "UK, DE, ES, FR, NL i PL to osobne pliki. Żadnego 301 między nimi, żadnego 301 na mycnbox.eu, mycnboxhaul.com ani mycnboxhual.com.",
             "Huby mycnbox.eu / mycnboxhaul.com / mycnboxhual.com to nie terytorium celne."),
        ]
        h1, topic, brow = "Co sprawdziliśmy na platformie, z datą", "co sprawdziliśmy na platformie", "Aktualności"
        lead = "To nie newsletter firmy. Nasze sprawdzenia, z datą."
    elif loc == "es":
        items = [
            ("Primera ronda: el estimador oficial",
             f"El {DATE} las cifras de flete solo salen de {EST}: elige el país, no este hostname. Ninguna línea inventada.",
             f"La mañana del envío abre el sitio oficial, destino {p['dest_zh']}. {p['postal']}."),
            ("w2clinks busca en inglés",
             "sneakers, hoodie, jacket dan páginas; grafías locales a menudo cero. Medido 6 Oct 2026.",
             "Escribe la key inglesa, o toca un chip en la portada."),
            ("Almacén: 90 días en el Help oficial",
             _storage("es"),
             "Planifica la consolidación para que la primera pieza no espere hasta el último día."),
            ("Los hosts hermanos siguen separados",
             "UK, DE, ES, FR, NL y PL son archivos distintos. Ningún 301 entre ellos, ningún 301 hacia mycnbox.eu, mycnboxhaul.com o mycnboxhual.com.",
             "Los hubs mycnbox.eu / mycnboxhaul.com / mycnboxhual.com no son un territorio aduanero."),
        ]
        h1, topic, brow = "Qué hemos comprobado en la plataforma, con fecha", "qué hemos comprobado en la plataforma", "Novedades"
        lead = "No es un boletín de empresa. Checks nuestros, con fecha."
    elif loc == "fr":
        items = [
            ("Premier tour : l’estimateur officiel",
             f"Le {DATE} les chiffres de nolo sortent seulement de {EST} : choisis le pays, pas ce nom d’hôte. Aucune ligne inventée.",
             f"Le matin de l’envoi, ouvre le site officiel, destination {p['dest_zh']}. {p['postal']}."),
            ("w2clinks cherche en anglais",
             "sneakers, hoodie, jacket donnent des pages ; les graphies locales souvent zéro. Mesuré 6 Oct 2026.",
             "Tape la key anglaise, ou touche un chip sur la page d’accueil."),
            ("Entrepôt : 90 jours dans le Help officiel",
             _storage("fr"),
             "Planifie le regroupement pour que la première pièce n’attende pas jusqu’au dernier jour."),
            ("Les hôtes sœurs restent séparés",
             "UK, DE, ES, FR, NL et PL sont des fichiers distincts. Aucun 301 entre eux, aucun 301 vers mycnbox.eu, mycnboxhaul.com ou mycnboxhual.com.",
             "Les hubs mycnbox.eu / mycnboxhaul.com / mycnboxhual.com ne sont pas un territoire douanier."),
        ]
        h1, topic, brow = "Ce que nous avons vérifié sur la plateforme, avec une date", "ce que nous avons vérifié sur la plateforme", "Actus"
        lead = "Ce n’est pas une newsletter d’entreprise. Des checks à nous, avec une date."
    else:
        items = [
            ("First round: the official estimator",
             f"On {DATE} freight figures come only from {EST}. This guide does not invent a line or an amount.",
             f"Open the official site the morning you ship. Destination {p['dest_zh']}. {p['postal']}."),
            ("The w2clinks catalogue searches in English",
             "sneakers, hoodie and jacket returned pages; local spellings often returned zero. Measured 6 Oct 2026.",
             "Type the English key, or tap a chip on the homepage."),
            ("Warehouse: 90 free days in official Help",
             _storage("en"),
             "Plan consolidation so the first piece does not wait until the last day."),
            ("Sister country hosts stay separate",
             "The United Kingdom, Germany, Spain, France, the Netherlands and Poland on MyCNBox stay on their own hosts. None of them 301 into mycnbox.eu, mycnboxhaul.com or mycnboxhual.com.",
             "The mycnbox.eu / mycnboxhaul.com / mycnboxhual.com hubs are not a customs territory."),
        ]
        h1, topic, brow = "What we checked on the platform, with a date", "what we checked on the platform", "News"
        lead = "This is not a company newsletter. These are our own checks, with a date."
    ld = itemlist_ld(
        url=f"https://{p['host']}{p['news']}",
        name="MyCNBox dest checks",
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
        desk, page_title(desk, topic), "Dated checks on MyCNBox.",
        f"https://{p['host']}{p['news']}", [ld], body, p["news"],
    )


def build_about(key: str) -> str:
    p = PACKS[key]
    desk = desk_for(key)
    fig_off, *_ = _shots(key)
    loc = p["loc"]
    if loc == "de":
        topic = "wer wir sind und wie du uns erreichst"
        body = f"""
<article class="pw">
  <span class="eyebrow" style="color:var(--acd)">Über uns</span>
  <h1>Eine unabhängige Site über MyCNBox, auf Deutsch</h1>
  <p class="lead">MyCNBox Spreadsheet ist nicht MyCNBox. Es ist ein redaktioneller Leitfaden. www.mycnbox.com ist die offizielle Site; mycnbox.eu, mycnboxhaul.com und mycnboxhual.com sind Hubs, kein Zollgebiet.</p>
  {fig_off}
  <h2>Wie wir arbeiten</h2>
  <p>Frachtzahlen kommen nur aus dem offiziellen Schätzer auf {escape(EST)}, deshalb veröffentlicht dieser Desk keinen erfundenen Tarif. Import: <a href="{escape(p["customs_url"])}" rel="noopener">{escape(p["customs"])}</a>.</p>
  <h2>Kontakt</h2>
  <p>Bestellungen: offizielle Site. Dieser Leitfaden: <a href="mailto:{escape(MAIL)}">{escape(MAIL)}</a>.</p>
</article>
"""
    elif loc == "nl":
        topic = "wie we zijn en hoe je ons bereikt"
        body = f"""
<article class="pw">
  <span class="eyebrow" style="color:var(--acd)">Over ons</span>
  <h1>Een onafhankelijke site over MyCNBox, in het Nederlands</h1>
  <p class="lead">MyCNBox Spreadsheet is MyCNBox niet. Het is een redactionele gids. www.mycnbox.com is de officiële site; mycnbox.eu, mycnboxhaul.com en mycnboxhual.com zijn hubs, geen douanegebied.</p>
  {fig_off}
  <h2>Hoe we werken</h2>
  <p>Vrachtcijfers komen alleen uit de officiële schatter op {escape(EST)}, dus deze gids publiceert geen verzonnen tarief. Import: <a href="{escape(p["customs_url"])}" rel="noopener">{escape(p["customs"])}</a>.</p>
  <h2>Contact</h2>
  <p>Bestellingen: officiële site. Deze gids: <a href="mailto:{escape(MAIL)}">{escape(MAIL)}</a>.</p>
</article>
"""
    elif loc == "pl":
        topic = "kim jesteśmy i jak się z nami skontaktować"
        body = f"""
<article class="pw">
  <span class="eyebrow" style="color:var(--acd)">O nas</span>
  <h1>Niezależna strona o MyCNBox, po polsku</h1>
  <p class="lead">MyCNBox Spreadsheet to nie MyCNBox. To przewodnik redakcyjny. www.mycnbox.com to strona oficjalna; mycnbox.eu, mycnboxhaul.com i mycnboxhual.com to huby, nie terytorium celne.</p>
  {fig_off}
  <h2>Jak pracujemy</h2>
  <p>Liczby frachtu wychodzą tylko z oficjalnego estymatora na {escape(EST)}, więc ten desk nie publikuje wymyślonej stawki. Import: <a href="{escape(p["customs_url"])}" rel="noopener">{escape(p["customs"])}</a>.</p>
  <h2>Kontakt</h2>
  <p>Zamówienia: strona oficjalna. Ten przewodnik: <a href="mailto:{escape(MAIL)}">{escape(MAIL)}</a>.</p>
</article>
"""
    elif loc == "es":
        topic = "quiénes somos y cómo contactarnos"
        body = f"""
<article class="pw">
  <span class="eyebrow" style="color:var(--acd)">Sobre nosotros</span>
  <h1>Un sitio independiente sobre MyCNBox, en español</h1>
  <p class="lead">MyCNBox Spreadsheet no es MyCNBox. Es una guía editorial. www.mycnbox.com es el sitio oficial; mycnbox.eu, mycnboxhaul.com y mycnboxhual.com son hubs, no un territorio aduanero.</p>
  {fig_off}
  <h2>Cómo trabajamos</h2>
  <p>Las cifras de flete solo salen del estimador oficial en {escape(EST)}, así que esta guía no publica tarifas inventadas. Importación: <a href="{escape(p["customs_url"])}" rel="noopener">{escape(p["customs"])}</a>.</p>
  <h2>Contacto</h2>
  <p>Pedidos: sitio oficial. Esta guía: <a href="mailto:{escape(MAIL)}">{escape(MAIL)}</a>.</p>
</article>
"""
    elif loc == "fr":
        topic = "qui nous sommes et comment nous joindre"
        body = f"""
<article class="pw">
  <span class="eyebrow" style="color:var(--acd)">À propos</span>
  <h1>Un site indépendant sur MyCNBox, en français</h1>
  <p class="lead">MyCNBox Spreadsheet n’est pas MyCNBox. C’est un guide éditorial. www.mycnbox.com est le site officiel ; mycnbox.eu, mycnboxhaul.com et mycnboxhual.com sont des hubs, pas un territoire douanier.</p>
  {fig_off}
  <h2>Comment on travaille</h2>
  <p>Les chiffres de nolo sortent seulement de l’estimateur officiel sur {escape(EST)}, donc ce guide ne publie pas de tarif inventé. Import : <a href="{escape(p["customs_url"])}" rel="noopener">{escape(p["customs"])}</a>.</p>
  <h2>Contact</h2>
  <p>Commandes : site officiel. Ce guide : <a href="mailto:{escape(MAIL)}">{escape(MAIL)}</a>.</p>
</article>
"""
    else:
        topic = "who we are and how to reach us"
        body = f"""
<article class="pw">
  <span class="eyebrow" style="color:var(--acd)">About us</span>
  <h1>An independent site about MyCNBox, in English</h1>
  <p class="lead">MyCNBox Spreadsheet is not MyCNBox. It is an editorial guide. www.mycnbox.com is the official site; mycnbox.eu, mycnboxhaul.com and mycnboxhual.com are hubs, not a customs territory.</p>
  {fig_off}
  <h2>How we work</h2>
  <p>Shipping figures come only from the official estimator at {escape(EST)}, so this desk publishes no invented rate. Import points to <a href="{escape(p["customs_url"])}" rel="noopener">{escape(p["customs"])}</a>.</p>
  <h2>Contact</h2>
  <p>Orders: official MyCNBox chat. This guide: <a href="mailto:{escape(MAIL)}">{escape(MAIL)}</a>.</p>
</article>
"""
    return cms_shell(
        desk, page_title(desk, topic),
        "Independent MyCNBox guide: how we check facts.",
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

    if loc == "de":
        guide_topic = f"wie du die erste Bestellung aus {dest} aufgibst"
        guide_body = f"""
<article class="pw">
  <span class="eyebrow" style="color:var(--acd)">Anleitung</span>
  <h1>Erste Bestellung bei MyCNBox, von {dest_e} aus</h1>
  <p class="lead">Link kopieren, in den Agenten einfügen, Lagerfoto prüfen, bündeln, Ziel {dest_zh} wählen. Die Lieferadresse ist eine {fp}.</p>
  {fig_off}
  <h2>1. Karte auf w2clinks öffnen</h2>
  <p>Eine der dreiunddreißig Kategorien, Foto und Shop-Link. Das ist der Katalog, keine Excel-Datei.</p>
  {fig_sheet}
  <h2>2. Auf der offiziellen Site einfügen</h2>
  <p>Zahlung und Tickets bleiben auf {official}. Dieser Desk sieht dein Konto nicht. Liest die Suche den Link nicht, hat die offizielle Site ein manuelles Formular.</p>
  {fig_diy}
  <h2>3. Foto, dann bündeln, dann senden</h2>
  <p>Frachtzahlen kommen nur von {est}: das Land wählen, nicht diesen Hostnamen. {escape(_storage("de"))}</p>
  <h2>Neun Status, drei Bildschirme</h2>
  <p>Zuerst Produkt plus Inlandsweg bis zum Lager. International später. «Warum steht es still?» heißt fast immer: falscher Bildschirm — Bestellungen, dann Lager, dann Paket.</p>
  <h2>Erste Haul: flach zuerst</h2>
  <p>T-Shirts, Shorts, Schmuck für die erste Runde. Daune, Taschen, Mützen für die zweite. Elektronik oft Lithium: Linie auf der offiziellen Site prüfen.</p>
  <p><a class="btn" href="{guide}">Anleitung</a> <a class="btn btn--ghost" href="{ship}">Versandplan</a></p>
</article>
"""
        ship_topic = f"Versand und Zoll nach {dest}"
        ship_body = f"""
<article class="pw">
  <span class="eyebrow" style="color:var(--acd)">Versand</span>
  <h1>Versand nach {dest_e}: Schätzer, Volumen, Zoll</h1>
  <p class="lead">Ziel {dest_zh}, nicht EU. Die Lieferadresse ist eine {fp}.</p>
  {fig_off}
  <h2>Der offizielle Schätzer entscheidet</h2>
  <p>Am {escape(DATE)} kommen Frachtzahlen nur aus {est}: das Land wählen, nicht diesen Hostnamen. Dieser Desk erfindet keine Linie, keine Transitzeit und keinen Betrag. Quelle: <a href="{customs_url}" rel="noopener">{customs}</a>.</p>
  <h2>Waage gegen Volumen</h2>
  <p>Viele Linien rechnen das Maximum aus Waage und L×B×H (cm) / 8000. Beispiel: 40×40×3 cm sind 4800 cm³, geteilt durch 8000 sind 600 g Volumen bei 200 g Echtgewicht. Kein SKU-Preis in diesem HTML.</p>
  {fig_vol}
  <h2>Bündeln ist kein Zolltrick auf dieser Seite</h2>
  <p>Mehrere Lagerpositionen in einem Karton können internationale Linien sparen. Was du dem Zoll angibst, steht in der offiziellen Sendung, nicht auf dieser Seite.</p>
  <h2>Restricted ist keine Zollnachricht</h2>
  <p>Karten ohne Preis oder ein manuelles Formular heißen: der Quellenlink ist über den Agenten nicht kaufbar. Tabak, Alkohol und Arzneimittel reisen nicht.</p>
  <h2>Lagerfotos vor der Linie</h2>
  <p>QC-Fotos landen in der App, sobald das Stück im Lager ist. Extra-Winkel sind oft kostenpflichtig. Reklamieren ist einfacher, solange es noch im Lager liegt. {escape(_storage("de"))}</p>
  <h2>Die Adresse auf diesem Dest</h2>
  <p>Die Lieferadresse ist eine {fp}. Packstation zählt, wenn die gewählte Linie sie akzeptiert — das steht auf der offiziellen Sendung, nicht hier.</p>
  <p><a class="btn" href="{est}">Offizieller MyCNBox-Schätzer</a> <a class="btn btn--ghost" href="{help_h}">Hilfe</a></p>
</article>
"""
    elif loc == "nl":
        guide_topic = f"hoe je de eerste bestelling vanuit {dest} plaatst"
        guide_body = f"""
<article class="pw">
  <span class="eyebrow" style="color:var(--acd)">Handleiding</span>
  <h1>Eerste MyCNBox-bestelling, vanuit {dest_e}</h1>
  <p class="lead">Link kopiëren, in de agent plakken, magazijnfoto checken, bundelen, bestemming {dest_zh} kiezen. Het afleveradres is een {fp}.</p>
  {fig_off}
  <h2>1. Open een kaart op w2clinks</h2>
  <p>Eén van de drieëndertig categorieën, foto en shoplink. Dat is de catalogus, geen Excel-bestand.</p>
  {fig_sheet}
  <h2>2. Plak op de officiële site</h2>
  <p>Betaling en tickets blijven op {official}. Deze gids ziet je account niet. Leest de zoekbalk de link niet, heeft de officiële site een handmatig formulier.</p>
  {fig_diy}
  <h2>3. Foto, dan bundelen, dan verzenden</h2>
  <p>Vrachtcijfers komen alleen van {est}: kies het land, niet deze hostname. {escape(_storage("nl"))}</p>
  <h2>Negen statussen, drie schermen</h2>
  <p>Eerst product plus binnenlands traject tot het magazijn. Internationaal later. «Waarom staat het stil?» bijna altijd: verkeerd scherm — bestellingen, dan magazijn, dan pakket.</p>
  <h2>Eerste haul: plat eerst</h2>
  <p>T-shirts, shorts, sieraden voor de eerste ronde. Dons, tassen, petten voor de tweede. Elektronica vaak lithium: check de lijn op de officiële site.</p>
  <p><a class="btn" href="{guide}">Handleiding</a> <a class="btn btn--ghost" href="{ship}">Verzendplan</a></p>
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
  <p>Op {escape(DATE)} komen vrachtcijfers alleen uit {est}: kies het land, niet deze hostname. Deze gids verzint geen lijn, transittijd of bedrag. Bron: <a href="{customs_url}" rel="noopener">{customs}</a>.</p>
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
  <p><a class="btn" href="{est}">Officiële MyCNBox-schatter</a> <a class="btn btn--ghost" href="{help_h}">Hulp</a></p>
</article>
"""
    elif loc == "pl":
        guide_topic = f"jak składasz pierwsze zamówienie z {dest}"
        guide_body = f"""
<article class="pw">
  <span class="eyebrow" style="color:var(--acd)">Poradnik</span>
  <h1>Pierwsze zamówienie MyCNBox, z {dest_e}</h1>
  <p class="lead">Kopiujesz link, wklejasz do agenta, sprawdzasz zdjęcie magazynu, łączysz, wybierasz cel {dest_zh}. Adres dostawy to {fp}.</p>
  {fig_off}
  <h2>1. Otwórz kartę na w2clinks</h2>
  <p>Jedna z trzydziestu trzech kategorii, zdjęcie i link sklepu. To katalog, nie plik Excel.</p>
  {fig_sheet}
  <h2>2. Wklej na stronie oficjalnej</h2>
  <p>Płatności i zgłoszenia zostają na {official}. Ten desk nie widzi Twojego konta. Jeśli wyszukiwarka nie czyta linku, strona oficjalna ma formularz ręczny.</p>
  {fig_diy}
  <h2>3. Zdjęcie, potem łącz, potem wyślij</h2>
  <p>Liczby frachtu wychodzą tylko z {est}: wybierz kraj, nie ten hostname. {escape(_storage("pl"))}</p>
  <h2>Dziewięć statusów, trzy ekrany</h2>
  <p>Najpierw produkt plus krajowy transport do magazynu. Międzynarodowy później. «Dlaczego stoi?» prawie zawsze: zły ekran — zamówienia, potem magazyn, potem paczka.</p>
  <h2>Pierwszy haul: płaskie najpierw</h2>
  <p>T-shirty, szorty, biżuteria na pierwszą rundę. Puch, torby, czapki na drugą. Elektronika często lit: sprawdź linię na stronie oficjalnej.</p>
  <p><a class="btn" href="{guide}">Poradnik</a> <a class="btn btn--ghost" href="{ship}">Plan wysyłki</a></p>
</article>
"""
        ship_topic = f"wysyłka i cło do {dest}"
        ship_body = f"""
<article class="pw">
  <span class="eyebrow" style="color:var(--acd)">Wysyłka</span>
  <h1>Wysyłka do {dest_e}: estymator, objętość, cło</h1>
  <p class="lead">Cel {dest_zh}, nie EU. Adres dostawy to {fp}.</p>
  {fig_off}
  <h2>Oficjalny estymator decyduje</h2>
  <p>{escape(DATE)} liczby frachtu wychodzą tylko z {est}: wybierz kraj, nie ten hostname. Ten desk nie wymyśla linii, czasu tranzytu ani kwoty. Źródło: <a href="{customs_url}" rel="noopener">{customs}</a>.</p>
  <h2>Waga kontra objętość</h2>
  <p>Wiele linii liczy maksimum wagi i L×W×H (cm) / 8000. Przykład: 40×40×3 cm to 4800 cm³, podzielone przez 8000 to 600 g objętości przy 200 g rzeczywistych. Żadnej ceny SKU w tym HTML.</p>
  {fig_vol}
  <h2>Łączenie to nie poradnik celny</h2>
  <p>Kilka sztuk z magazynu w jednym kartonie może obciąć linie międzynarodowe. Co zgłaszasz na cło, jest na oficjalnej przesyłce, nie na tej stronie.</p>
  <h2>Restricted to nie zawiadomienie celne</h2>
  <p>Karty bez ceny albo formularz ręczny znaczą: link źródłowy nie da się kupić przez agenta. Tytoń, alkohol i leki nie jadą.</p>
  <h2>Zdjęcia magazynu przed linią</h2>
  <p>Zdjęcia QC lądują w aplikacji, gdy sztuka jest w magazynie. Dodatkowe kąty często płatne. Reklamacja jest łatwiejsza, dopóki jeszcze tam leży. {escape(_storage("pl"))}</p>
  <h2>Adres na tym deście</h2>
  <p>Adres dostawy to {fp}. Ten format należy na oficjalną przesyłkę, nie jako fortel na tej stronie.</p>
  <p><a class="btn" href="{est}">Oficjalny estymator MyCNBox</a> <a class="btn btn--ghost" href="{help_h}">Pomoc</a></p>
</article>
"""
    elif loc == "fr":
        guide_topic = f"comment tu passes la première commande depuis {dest}"
        guide_body = f"""
<article class="pw">
  <span class="eyebrow" style="color:var(--acd)">Guide</span>
  <h1>Première commande MyCNBox, depuis {dest_e}</h1>
  <p class="lead">Tu copies le lien, tu le colles dans l’agent, tu vérifies la photo d’entrepôt, tu regroupes, tu choisis destination {dest_zh}. L’adresse est une {fp}.</p>
  {fig_off}
  <h2>1. Ouvre une fiche sur w2clinks</h2>
  <p>Une des trente-trois catégories, photo et lien boutique. C’est un catalogue, pas un fichier Excel.</p>
  {fig_sheet}
  <h2>2. Colle-le sur le site officiel</h2>
  <p>Paiements et tickets restent sur {official}. Ce guide ne voit pas ton compte. Si la recherche ne lit pas le lien, le site officiel a un formulaire d’ordre manuel.</p>
  {fig_diy}
  <h2>3. Photo, puis regrouper, puis envoyer</h2>
  <p>Les chiffres de nolo sortent seulement de {est} : choisis le pays, pas ce nom d’hôte. {escape(_storage("fr"))}</p>
  <h2>Neuf statuts, trois écrans</h2>
  <p>D’abord le produit plus le trajet intérieur jusqu’à l’entrepôt. L’international après. « Pourquoi c’est bloqué ? » presque toujours : mauvais écran — commandes, puis entrepôt, puis colis.</p>
  <h2>Premier haul : plat d’abord</h2>
  <p>T-shirts, shorts, bijoux pour le premier tour. Doudounes, sacs, casquettes pour le second. Électronique souvent lithium : vérifie la ligne sur le site officiel.</p>
  <p><a class="btn" href="{guide}">Guide</a> <a class="btn btn--ghost" href="{ship}">Plan de livraison</a></p>
</article>
"""
        ship_topic = f"livraison et douane vers {dest}"
        ship_body = f"""
<article class="pw">
  <span class="eyebrow" style="color:var(--acd)">Livraison</span>
  <h1>Expédier vers {dest_e} : estimateur, volume, douane</h1>
  <p class="lead">Destination {dest_zh}, pas EU. L’adresse est une {fp}.</p>
  {fig_off}
  <h2>L’estimateur officiel décide</h2>
  <p>Le {escape(DATE)} les chiffres de nolo sortent seulement de {est} : choisis le pays, pas ce nom d’hôte. Ce guide n’invente ni ligne, ni transit, ni montant. Source : <a href="{customs_url}" rel="noopener">{customs}</a>.</p>
  <h2>Balance contre volume</h2>
  <p>Beaucoup de lignes facturent le max entre balance et L×W×H (cm) / 8000. Exemple : 40×40×3 cm font 4800 cm³, divisés par 8000 font 600 g de volume pour 200 g réels. Aucun prix SKU dans cet HTML.</p>
  {fig_vol}
  <h2>Regrouper n’est pas un tutoriel douane</h2>
  <p>Plusieurs pièces d’entrepôt dans un carton peuvent réduire les lignes internationales. Ce que tu déclares en douane est sur l’envoi officiel, pas sur cette page.</p>
  <h2>Restricted n’est pas un avis de douane</h2>
  <p>Fiches sans prix ou un formulaire manuel signifient : le lien source n’est pas achetable via l’agent. Tabac, alcool et médicaments ne voyagent pas.</p>
  <h2>Photos d’entrepôt avant la ligne</h2>
  <p>Les photos QC arrivent dans l’app quand la pièce est en entrepôt. Angles extra souvent payants. Réclamer est plus simple tant qu’elle y est encore. {escape(_storage("fr"))}</p>
  <h2>L’adresse sur ce dest</h2>
  <p>L’adresse est une {fp}. Ce format va sur l’envoi officiel, pas comme astuce sur cette page.</p>
  <p><a class="btn" href="{est}">Estimateur officiel MyCNBox</a> <a class="btn btn--ghost" href="{help_h}">Aide</a></p>
</article>
"""
    elif loc == "es":
        guide_topic = f"cómo haces el primer pedido desde {dest}"
        guide_body = f"""
<article class="pw">
  <span class="eyebrow" style="color:var(--acd)">Guía</span>
  <h1>Primer pedido MyCNBox, desde {dest_e}</h1>
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
  <p><a class="btn" href="{est}">Estimador oficial MyCNBox</a> <a class="btn btn--ghost" href="{help_h}">Ayuda</a></p>
</article>
"""
    else:
        guide_topic = f"how you place the first order from {dest}"
        guide_body = f"""
<article class="pw">
  <span class="eyebrow" style="color:var(--acd)">Guide</span>
  <h1>First MyCNBox order, from {dest_e}</h1>
  <p class="lead">Copy the shop link, paste it into the agent, check the warehouse photo, consolidate, then pick destination {dest_zh}. The delivery address uses a {fp}.</p>
  {fig_off}
  <h2>1. Open a card on w2clinks</h2>
  <p>One of the thirty-three categories, a photo and the shop link. That is the catalogue, not an Excel file.</p>
  {fig_sheet}
  <h2>2. Paste it on the official site</h2>
  <p>Payment and tickets stay on {official}. This desk cannot see your account. If search does not read the link, the official site has a manual order form.</p>
  {fig_diy}
  <h2>3. Photo, then consolidate, then ship</h2>
  <p>Freight figures come only from www.mycnbox.com{escape(EST_PATH)} — pick the dest country, not this hostname. {escape(_storage("en"))}</p>
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
  <p><a class="btn" href="{est}">Official MyCNBox estimator</a> <a class="btn btn--ghost" href="{help_h}">Help</a></p>
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
        f"Independent MyCNBox {name} for {p['dest_label']}.",
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
    "no es un archivo Excel",
    "pas un fichier Excel",
    "keine Excel-Datei",
    "geen Excel-bestand",
    "nie jest plikiem Excel",
)

GUIDE_MARK = {
    "es": "Primer pedido MyCNBox",
    "fr": "Première commande MyCNBox",
    "de": "Erste Bestellung bei MyCNBox",
    "nl": "Eerste MyCNBox-bestelling",
    "pl": "Pierwsze zamówienie MyCNBox",
    "en": "First MyCNBox order",
}
ABOUT_MARK = {
    "es": "Un sitio independiente sobre MyCNBox",
    "fr": "Un site indépendant sur MyCNBox",
    "de": "Eine unabhängige Site über MyCNBox",
    "nl": "Een onafhankelijke site over MyCNBox",
    "pl": "Niezależna strona o MyCNBox",
    "en": "An independent site about MyCNBox",
}


def _ship_mark(p: dict) -> str:
    return {
        "es": f"Enviar a {p['dest_label']}",
        "fr": f"Expédier vers {p['dest_label']}",
        "de": f"Versand nach {p['dest_label']}",
        "nl": f"Verzenden naar {p['dest_label']}",
        "pl": f"Wysyłka do {p['dest_label']}",
    }.get(p["loc"], "Shipping to")


def _assert_ok(html: str, page: str, key: str) -> None:
    p = PACKS[key]
    desk = desk_for(key)
    if page == "nf":
        if p["not_found_tab"] not in html or MAIL not in html:
            raise SystemExit(f"{key} nf chrome")
        if f"{p['not_found_tab']} | MyCNBox Spreadsheet" not in html:
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
        if p["loc"] != "en" and "Official www.mycnbox.com, 6 Oct" in html:
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
        "/* MyCNBox country dest — official orange from www.mycnbox.com */\n"
        f":root {{ --primary: {ACC}; --primary-dark: {ACC_DARK}; --primary-soft: {SOFT}; --nav-dark: #111111; }}\n",
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
    _run(client, f"cp -a '{gsc}' '/www/backup/mycnbox-{key}-gsc-about-{stamp}.conf'")
    Path(f"/tmp/mycnbox-{key}-gsc.conf").write_text("".join(keep), encoding="utf-8")
    sftp.put(f"/tmp/mycnbox-{key}-gsc.conf", gsc)
    print(key, "stripped", stripped, "CMS-page home 301s")
    _reload_nginx(client)


def _map_legacy_english_cms(client, sftp, key: str) -> None:
    """301 leftover English CMS slugs onto dest slugs; drop the leftover dirs.

    Rewrite in every extension conf (FR already has `location = /about` in
    00-gsc-redirects.conf). Appending a second copy into gsc-redirects.conf
    duplicates the location and breaks nginx -t.
    """
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
    ext = f"/www/server/panel/vhost/nginx/extension/{host}"
    listing = _run(client, f"find '{ext}' -maxdepth 1 -name '*.conf' -print 2>/dev/null || true")
    files = [ln.strip() for ln in listing.splitlines() if ln.strip().endswith(".conf")]
    loc_re = re.compile(r"location\s+=\s+(\S+)\s*\{")
    seen: set[str] = set()
    stamp = time.strftime("%Y%m%d-%H%M%S")
    changed = 0
    for remote in files:
        raw = _run(client, f"cat '{remote}' 2>/dev/null || true")
        if not raw:
            continue
        out: list[str] = []
        file_changed = False
        for ln in raw.splitlines(True):
            m = loc_re.search(ln)
            if not m or m.group(1) not in wanted:
                out.append(ln)
                continue
            path = m.group(1)
            want = f"location = {path} {{ return 301 https://{host}{wanted[path]}; }}\n"
            if path in seen:
                file_changed = True
                continue
            prefix = ln[: m.start()] if m.start() else ""
            if prefix.strip() and not prefix.endswith("\n"):
                out.append(prefix.rstrip() + "\n")
            elif prefix and prefix.endswith("\n"):
                out.append(prefix)
            out.append(want)
            seen.add(path)
            if ln.strip() != want.strip():
                file_changed = True
        if file_changed:
            _run(client, f"cp -a '{remote}' '/www/backup/mycnbox-{key}-legacy-{Path(remote).name}-{stamp}.conf'")
            tmp = Path(f"/tmp/mycnbox-{key}-legacy-{Path(remote).name}")
            tmp.write_text("".join(out), encoding="utf-8")
            sftp.put(str(tmp), remote)
            changed += 1
            print(key, "legacy CMS 301s", Path(remote).name)
    gsc = f"{ext}/gsc-redirects.conf"
    missing = [path for path in wanted if path not in seen]
    if missing:
        raw = _run(client, f"cat '{gsc}' 2>/dev/null || true")
        add = "".join(f"location = {path} {{ return 301 https://{host}{wanted[path]}; }}\n" for path in missing)
        _run(client, f"mkdir -p '{ext}'; touch '{gsc}'")
        body = raw or ""
        if body and not body.endswith("\n"):
            body += "\n"
        Path(f"/tmp/mycnbox-{key}-gsc-legacy.conf").write_text(body + add, encoding="utf-8")
        sftp.put(f"/tmp/mycnbox-{key}-gsc-legacy.conf", gsc)
        changed += 1
        print(key, "appended leftover CMS 301s", " ".join(missing))
    if changed:
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
    # mycnbox-coupon (singular) is left out on purpose: origin may 301 it onto ranked /mycnbox-coupons/.
    unstick = {h.strip("/") for h in _cms_hrefs(key)}
    faq_src = {
        "/faq", "/faq/",
        "/mycnbox-invite-code", "/mycnbox-invite-code/",
    }
    loc_re = re.compile(r"location\s+(?:=|\^~)\s+(\S+)\s*\{")
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
            _run(client, f"cp -a '{remote}' '/www/backup/mycnbox-{key}-{Path(remote).name}-{stamp}.conf'")
            tmp = Path(f"/tmp/mycnbox-{key}-{Path(remote).name}")
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
        Path(f"/tmp/mycnbox-{key}-gsc-faq.conf").write_text(body + add, encoding="utf-8")
        sftp.put(f"/tmp/mycnbox-{key}-gsc-faq.conf", gsc)
        changed += 1
        print(key, "appended", " ".join(missing), "->", help_href)
    if changed:
        _reload_nginx(client)
    else:
        print(key, "faq/CMS redirects already mapped")


_LOC_LINE = re.compile(
    r"location\s+(?P<mod>=|\^~)\s+(?P<path>\S+)\s*\{(?P<body>[^{}]*)\}"
)


def _unstick_shadows(client, sftp, key: str) -> None:
    """Drop locations that steal CMS slugs or ranked wrap URLs.

    Drops CMS-slug 301s including `location =` and `location ^~` so generated
    ship/guide/help are 200. Leftover `/mycnbox-shipping/` 301s unstick because
    `/mycnbox-shipping/` is the CMS ship slug; ranked `/mycnbox-shipping-guide/`
    stays wrap. Trailing-slash canonicalization onto the same wrap href is kept.
    """
    p = PACKS[key]
    host = p["host"]
    cms = {h.strip("/") for h in _cms_hrefs(key)}
    ranked = {href.strip("/") for href, _ in _wrap_targets(key)}
    ext = f"/www/server/panel/vhost/nginx/extension/{host}"
    listing = _run(client, f"find '{ext}' -maxdepth 1 -name '*.conf' -print 2>/dev/null || true")
    files = [ln.strip() for ln in listing.splitlines() if ln.strip().endswith(".conf")]
    stamp = time.strftime("%Y%m%d-%H%M%S")
    changed = 0
    for remote in files:
        raw = _run(client, f"cat '{remote}' 2>/dev/null || true")
        if not raw:
            continue
        out: list[str] = []
        file_changed = False
        for ln in raw.splitlines(True):
            m = _LOC_LINE.search(ln)
            if not m:
                out.append(ln)
                continue
            path = m.group("path")
            slug = path.strip("/")
            body = m.group("body")
            tm = re.search(r"return\s+30[1278]\s+https?://[^/\s]+(\S*?);", body)
            tgt = (tm.group(1) or "/") if tm else None
            if slug in cms:
                print(key, "unstick cms", path, "->", tgt, Path(remote).name)
                file_changed = True
                continue
            if slug in ranked:
                self_href = "/" + slug + "/"
                if tgt is None or tgt.rstrip("/") != self_href.rstrip("/"):
                    print(key, "unstick ranked", path, "->", tgt, Path(remote).name)
                    file_changed = True
                    continue
            out.append(ln)
        if not file_changed:
            continue
        _run(client, f"cp -a '{remote}' '/www/backup/mycnbox-{key}-unstick-{Path(remote).name}-{stamp}.conf'")
        tmp = Path(f"/tmp/mycnbox-{key}-unstick-{Path(remote).name}")
        tmp.write_text("".join(out), encoding="utf-8")
        sftp.put(str(tmp), remote)
        changed += 1
    if changed:
        _reload_nginx(client)
    else:
        print(key, "no cms/ranked shadow 301s")


def _harden_catchall(client, sftp, key: str) -> None:
    host = PACKS[key]["host"]
    vhost = f"/www/server/panel/vhost/nginx/{host}.conf"
    with sftp.open(vhost, "r") as fh:
        text = fh.read().decode()
    marker = f'X-Desk "mycnbox-{key}-independent"'
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
        add_header X-Desk "mycnbox-{key}-independent" always;
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
    _run(client, f"cp -a '{vhost}' '/www/backup/mycnbox-{key}-nginx-{stamp}.conf'")
    tmp = Path(f"/tmp/mycnbox-{key}.conf")
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
    if loc == "de":
        topic = "dieser Artikel wurde ersetzt"
        body = f"""
<article class="pw">
  <h1>Dieser Artikel wurde ersetzt</h1>
  <p class="lead">Die alte Fassung gehörte nicht zu MyCNBox. Die aktuelle Anleitung steht auf Start. Die Lieferadresse ist eine {fp}.</p>
  <p><a class="btn" href="/start/">Start</a> <a class="btn btn--ghost" href="{escape(p['guide'])}">Anleitung</a></p>
</article>
"""
    elif loc == "nl":
        topic = "dit artikel is vervangen"
        body = f"""
<article class="pw">
  <h1>Dit artikel is vervangen</h1>
  <p class="lead">De vorige versie hoorde niet bij MyCNBox. De huidige gids staat op Start. Het afleveradres is een {fp}.</p>
  <p><a class="btn" href="/start/">Start</a> <a class="btn btn--ghost" href="{escape(p['guide'])}">Handleiding</a></p>
</article>
"""
    elif loc == "pl":
        topic = "ten artykuł został zastąpiony"
        body = f"""
<article class="pw">
  <h1>Ten artykuł został zastąpiony</h1>
  <p class="lead">Poprzednia wersja nie była destem MyCNBox. Aktualny poradnik jest na Start. Adres dostawy to {fp}.</p>
  <p><a class="btn" href="/start/">Start</a> <a class="btn btn--ghost" href="{escape(p['guide'])}">Poradnik</a></p>
</article>
"""
    elif loc == "es":
        topic = "este artículo fue sustituido"
        body = f"""
<article class="pw">
  <h1>Este artículo fue sustituido</h1>
  <p class="lead">La versión anterior no era de MyCNBox. La guía actual está en Start. La dirección es una {fp}.</p>
  <p><a class="btn" href="/start/">Start</a> <a class="btn btn--ghost" href="{escape(p['guide'])}">Guía</a></p>
</article>
"""
    elif loc == "fr":
        topic = "cet article a été remplacé"
        body = f"""
<article class="pw">
  <h1>Cet article a été remplacé</h1>
  <p class="lead">La version précédente n’était pas MyCNBox. Le guide actuel est sur Start. L’adresse est une {fp}.</p>
  <p><a class="btn" href="/start/">Start</a> <a class="btn btn--ghost" href="{escape(p['guide'])}">Guide</a></p>
</article>
"""
    else:
        topic = "this article was replaced"
        body = f"""
<article class="pw">
  <h1>This article was replaced</h1>
  <p class="lead">The previous version was not a MyCNBox dest page. The current guide is on Start. The delivery address uses a {fp}.</p>
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
        elif "data-inner-chrome=" in raw and p["css_id"] in raw:
            # Marker includes CSS_V; a cache-bust bump must not re-wrap and shrink.
            print("skip already wrapped", rel)
            continue
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
        local_tmp = Path("/tmp") / f"mycnbox-wrap-{key}-{rel.replace('/', '_')}"
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
    bak = f"/www/backup/mycnbox-{key}-cms-{stamp}"
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
    _unstick_shadows(client, sftp, key)
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
        url, headers={"User-Agent": "mycnbox-cms/1.0", "Cache-Control": "no-cache"},
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
    if not TWINS:
        return []
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
            bak = f"/www/backup/mycnbox-twin-{twin}-{Path(remote).name}-{stamp}"
            if _run(client, f"test -f '{remote}' && cp -a '{remote}' '{bak}' && echo ok || true") == "ok":
                backups.append((remote, bak))
            else:
                backups.append((remote, ""))
            tmp = Path(f"/tmp/mycnbox-twin-{twin}-{Path(remote).name}")
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
    if not TWINS:
        print("no Origin twins; skip")
        return
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
                if p["loc"] != "en" and "Official www.mycnbox.com, 6 Oct" in html:
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
            elif code in (301, 302, 308):
                loc_path = urlparse(loc).path if loc else ""
                if loc_path.rstrip("/") != href.rstrip("/"):
                    print(" FAIL ranked 301 away", href, "->", loc); fail += 1
            else:
                print(" FAIL ranked status", code); fail += 1
        code_c, _, loc_c, _ = _fetch(f"https://{host}/mycnbox-coupon/", follow=False)
        print(k, "coupon", code_c, loc_c)
        if code_c in (301, 302, 308) and "/mycnbox-coupon" in (loc_c or "") and host in (loc_c or host):
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
        if f"{p['not_found_tab']} | MyCNBox Spreadsheet" not in nhtml:
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
    """Accept pack keys or hosts; return dests in PACKS order (uk de es fr nl pl)."""
    if not args:
        return list(PACKS)
    host_to_key = {p["host"]: k for k, p in PACKS.items()}
    mapped: list[str] = []
    bad: list[str] = []
    for a in args:
        if a in PACKS:
            mapped.append(a)
        elif a in host_to_key:
            mapped.append(host_to_key[a])
        else:
            bad.append(a)
    if bad:
        raise SystemExit(
            f"unknown dest {bad}; dests are {list(PACKS)}. "
            f"Hubs/twins {sorted(SKIP_PUT_HOSTS | set(TWINS))} are never PUT as dests."
        )
    wanted = set(mapped)
    return [k for k in PACKS if k in wanted]


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
