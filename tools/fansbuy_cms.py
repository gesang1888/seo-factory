#!/usr/bin/env python3
"""FansBuy country dests: UK, NL, DE, EU.

Gold IA: hipobuy.es (reference only — not ours; never clone the Spain 58-line /
23.81 USD snapshot). Gold completeness (content + shots): acbuyspreadsheets.nl
(7 unique figs, 9-status timeline, public estimator snapshot, FAQPage JSON-LD
on home with visible FAQs only on Help). Gold brand: fansbuy.com (official
coral #ff3344 / #f34). Gold dest: fansbuy.co.uk (English UK). Then NL, DE
(Packstation, not AT 1010 Wien), then .eu (not a customs territory).
Same-agent country hosts stay independent (no 301 between UK/NL/DE/.eu).
Never 301 FansBuy dests to USFans. Twin fansbuyspreadsheet.uk 301s onto
.co.uk with $request_uri; fansbuyspreadsheet.eu onto fansbuy.eu.

Skip PUT exact hosts: fansbuysheets.net (leftover extra hub, GSC 40, twins
already 301 in). Never substring-match skip. Do not PUT, 301, or GSC
USFans hosts, official fansbuy.com, cnfans.shop, or twins.
FansBuy is not USFans. HipoBuy is not FansBuy.

Official estimator is https://fansbuy.com/estimates
Warehouse: official Help https://fansbuy.com/help-283.html — 90 free warehouse
days; confirm that Help copy the morning you ship. Invite Fans-pys5Zt48 stays
off titles and dest homepages. Coupon FANS26 may stay on the unique ranked
coupons inner, not home. Register/login without the invite query.

CMS shipping slug is /fansbuy-freight/ so ranked /fansbuy-shipping-guide/ stays wrap.
WRAP_POISON must not contain the token "fansbuy".

Usage:
    python3 tools/fansbuy_cms.py generate [uk nl de eu]
    python3 tools/fansbuy_cms.py put [uk nl de eu]
    python3 tools/fansbuy_cms.py twins
    python3 tools/fansbuy_cms.py live [uk|nl|de|eu]
    python3 tools/fansbuy_cms.py all
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
ASSETS = Path("/tmp/fansbuy-assets")
DATE = "6 Oct 2026"
AGENT = "FansBuy"
OFFICIAL = "https://fansbuy.com/"
EST_PATH = "/estimates"
EST = "https://fansbuy.com/estimates"
HELP = "https://fansbuy.com/help-283.html"
ACC = "#ff3344"
ACC_DARK = "#c12233"
SOFT = "#fff1f2"
LOGIN_FG = "#fff"
MAIL = "cnfd85269032661@gmail.com"
HUBS = ("fansbuysheets.net",)
SKIP_PUT_HOSTS = {"fansbuysheets.net"}
OFF_ORIGIN = (
    "fansbuy.com",
    "fansbuyspreadsheet.uk",
    "fansbuyspreadsheet.eu",
    "fansspreadsheet.net",
    "fansspreadsheets.net",
    "cnfans.shop",
    "usfans.com",
    "usfansspreadsheet.co.uk",
    "usfansspreadsheet.nl",
    "usfansspreadsheet.net",
    "usfansspreadsheet.uk",
    "hipobuy.es",
    "hipobuy.com",
    "fansbuy.es",
    "fansbuy.de",
    "fansbuy.fr",
    "fansbuy.it",
    "fansbuy.us",
    "fansbuy.uk",
    "fansbuy.org",
    "fansbuy.ca",
)
PHP_HOSTS = ()
PHP_KEYS = ()
DEST_MIN = 40000
CSS_V = "20261006f"
INVITES = ("Fans-pys5Zt48",)
LOGO = "fansbuy-wordmark.png"
THEME_CSS = "fansbuy-theme.css"
SHEET_SLUG = "fansbuy"
SHOTS = (
    "oficial-inicio.jpg",
    "oficial-guidebook.jpg",
    "oficial-guidebook-3.jpg",
    "oficial-diy.jpg",
    "catalogus.jpg",
    "catalogus-zoek.jpg",
    "volume-voorbeeld.jpg",
)
# Public estimator, 6 Oct 2026, 1000 g × 35×25×10 cm, English/USD on fansbuy.com.
EST_SNAP = {
    "uk": {"dest": "United Kingdom", "line": "BJ-E-ETK", "price": "$16.62", "days": "10–30", "n": "11"},
    "nl": {"dest": "Netherlands", "line": "BJ-E-ETK", "price": "$19.05", "days": "10–30", "n": "17"},
    "de": {"dest": "Germany", "line": "EU-Tariffless-YJ-MG 0-5kgs", "price": "$23.93", "days": "10–15", "n": "15"},
    "eu": {"dest": "a member state (form has no EU)", "line": "TYG-EU-Tariffless Express (Ireland in form)", "price": "$27.58", "days": "7–15", "n": "12"},
}
GUIDE_HREF = "/how-to-use-fansbuy/"
SHIP_HREF = "/fansbuy-freight/"
SISTER_LEFTOVER = ("cssbuy leftover", "1yi9", "cssb.uy", "orientdig leftover", "1qodrw", "kakobuy leftover", "sugargoo leftover", "superbuy leftover", "usfans leftover", "hipobuy leftover")
WRAP_POISON = ("1yi9", "cssb.uy", "1qodrw", "bbd5off", "cruisezhang", "200345875", "orientdig leftover", "kakobuy leftover", "sugargoo leftover", "superbuy leftover", "usfans leftover", "hipobuy leftover")

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
    "KNEEPAD": "In coppia sulla foto QC. Un ginocchiera sullo scatto non è un paio.",
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

_RANKED_CORE = (
    ("/fansbuy-coupons/", 8000),
    ("/fansbuy-spreadsheet/", 8000),
    ("/is-fansbuy-legit/", 8000),
)
RANKED = {
    "uk": (
        ("/fansbuy-coupons/", 8000),
        ("/fansbuy-refund-guide/", 8000),
        ("/fansbuy-shipping-guide/", 8000),
        ("/is-fansbuy-legit/", 8000),
        ("/fansbuy-spreadsheet/", 8000),
        ("/fansbuy-qc-guide/", 8000),
        ("/fansbuy-community/", 8000),
        ("/fansbuy-shoes-spreadsheet/", 8000),
        ("/fansbuy-spreadsheet-2026/", 8000),
        ("/how-to-use-fansbuy/", 8000),
    ),
    "nl": (
        ("/fansbuy-coupons/", 8000),
        ("/fansbuy-refund-guide/", 8000),
        ("/fansbuy-shipping-guide/", 8000),
        ("/is-fansbuy-legit/", 8000),
        ("/fansbuy-spreadsheet/", 8000),
        ("/fansbuy-qc-guide/", 8000),
        ("/fansbuy-community/", 8000),
        ("/fansbuy-shoes-spreadsheet/", 8000),
        ("/fansbuy-spreadsheet-2026/", 8000),
    ),
    "de": (
        ("/fansbuy-coupons/", 8000),
        ("/fansbuy-refund-guide/", 8000),
        ("/fansbuy-shipping-guide/", 8000),
        ("/is-fansbuy-legit/", 8000),
        ("/fansbuy-spreadsheet/", 8000),
        ("/fansbuy-qc-guide/", 8000),
        ("/fansbuy-community/", 8000),
        ("/fansbuy-shoes-spreadsheet/", 8000),
        ("/fansbuy-spreadsheet-2026/", 8000),
    ),
    "eu": (
        ("/fansbuy-coupons/", 8000),
        ("/fansbuy-refund-guide/", 8000),
        ("/fansbuy-shipping-guide/", 8000),
        ("/is-fansbuy-legit/", 8000),
        ("/fansbuy-spreadsheet/", 8000),
        ("/fansbuy-qc-guide/", 8000),
        ("/how-to-use-fansbuy/", 8000),
    ),
}

KEEP = {
    "uk": [
        ("/fansbuy-coupons/", "Coupons article"),
        ("/help/", "Help"),
        ("/who-we-are/", "Who we are"),
        ("/fansbuy-shipping-guide/", "UK shipping"),
        ("/how-to-use-fansbuy/", "How to use"),
        ("/fansbuy-spreadsheet/", "Spreadsheet"),
    ],
    "nl": [
        ("/fansbuy-shipping-guide/", "Verzending"),
        ("/how-to-use-fansbuy/", "Handleiding"),
        ("/hulp/", "Hulp"),
        ("/over-ons/", "Over ons"),
        ("/fansbuy-coupons/", "Coupons"),
        ("/is-fansbuy-legit/", "Review"),
    ],
    "de": [
        ("/fansbuy-shipping-guide/", "Versandguide DE"),
        ("/how-to-use-fansbuy/", "Ablauf"),
        ("/is-fansbuy-legit/", "Legit"),
        ("/hilfe/", "Hilfe"),
        ("/fansbuy-coupons/", "Coupons"),
        ("/ueber-uns/", "Über uns"),
    ],
    "eu": [
        ("/fansbuy-coupons/", "Coupons article"),
        ("/help/", "Help"),
        ("/who-we-are/", "Who we are"),
        ("/how-to-use-fansbuy/", "How to use"),
        ("/fansbuy-shipping-guide/", "Shipping"),
    ],
}

TWINS = {
    "fansbuyspreadsheet.uk": "fansbuy.co.uk",
    "fansbuyspreadsheet.eu": "fansbuy.eu",
}

TWIN_EXTRA = {}

STORAGE = {
    "en": (
        f"Official Help ({HELP}): 90 free warehouse days from “In warehouse”, "
        "then items can be treated as abandoned if you do not submit a parcel or "
        f"pay an extension; maximum 180 days ({DATE}). This dest does not invent "
        "a storage window as a coupon. Orders stay on fansbuy.com."
    ),
    "de": (
        f"Offizielles Help ({HELP}): 90 kostenlose Lagertage ab „In warehouse“, "
        f"danach Aufgabe ohne Nachlieferung/Verlängerung, max. 180 Tage ({DATE})."
    ),
    "es": (
        f"Help oficial ({HELP}): 90 días de almacén gratis desde “In warehouse”; "
        f"máximo 180 días ({DATE})."
    ),
    "fr": (
        f"Help officiel ({HELP}) : 90 jours d’entrepôt gratuits depuis « In warehouse » ; "
        f"maximum 180 jours ({DATE})."
    ),
    "it": (
        f"Help ufficiale ({HELP}): 90 giorni di magazzino gratis da “In warehouse”; "
        f"massimo 180 giorni ({DATE})."
    ),
    "nl": (
        f"Officiële Help ({HELP}): 90 gratis magazijndagen vanaf “In warehouse”; "
        f"maximum 180 dagen ({DATE})."
    ),
}

EXTRA_CSS = """
:root{--primary-soft:#fff1f2;--login-fg:#fff}
.hero .eyebrow{color:#fb7185}
header.top .hdr-login,.hdr-login{background:#ff3344;color:#fff}
header.top .hdr-login:hover,.hdr-login:hover{background:#c12233;color:#fff}
.sbox button{color:#fff}
"""


def _storage(loc: str) -> str:
    return STORAGE.get(loc, STORAGE["en"])



def _en_pack(host, dest, dest_label, dest_zh, lang, ccy, topic, hero, lead, postal, customs, customs_url, aliens, css, css_id, login="Log in to FansBuy"):
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
            (GUIDE_HREF, "FansBuy guide"),
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
    "uk": {
        "host": "fansbuy.co.uk",
        "dest": "GB",
        "dest_label": "the United Kingdom",
        "dest_zh": "United Kingdom — 英国",
        "lang": "en-GB",
        "loc": "en",
        "in_language": "in English",
        "ccy": "GBP",
        "home_topic": "buy in China from the United Kingdom, safely",
        "hero_h1": "FansBuy Spreadsheet: the guide to buying in China from the United Kingdom",
        "eyebrow": "Independent guide, in English",
        "lead": "How you paste a product link into the agent, how the w2clinks catalogue works, how a parcel travels to the United Kingdom, and what you check before HMRC.",
        "fingerprint": dest_local_pack("GB")["fingerprint"],
        "customs": "HMRC",
        "customs_url": "https://www.gov.uk/goods-sent-from-abroad",
        "postal": "UK postcode. Northern Ireland is often another carrier product",
        "catalog": "/catalog/",
        "help": "/help/",
        "news": "/news/",
        "about": "/who-we-are/",
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
            (GUIDE_HREF, "FansBuy guide"),
            ("/catalog/", "The spreadsheet and the categories"),
            (SHIP_HREF, "Shipping and customs"),
            ("/help/", "Help and questions"),
            ("/news/", "News"),
            ("/who-we-are/", "About us"),
        ],
        "aliens": ("Packstation", "form A1A 1A1", "Poste Italiane", "no copiamos", "pas un code postal belge", "00-001 Warszawa", "Nederlandse postcode", "does not invent a de-minimis dollar", "1010 Wien", "do not copy a GST rate", "not a customs territory"),
        "not_found_tab": "Page not found",
        "login": "Log in to FansBuy",
        "menu": "Open menu",
        "home_cta": "Back to the homepage",
        "skip": "en",
        "desk_css": "fansbuy-uk-desk.css",
        "css_id": "fansbuy-uk",
    },
    "nl": {
        "host": "fansbuy.nl",
        "dest": "NL",
        "dest_label": "Nederland",
        "dest_zh": "Netherlands — 荷兰",
        "lang": "nl-NL",
        "loc": "nl",
        "in_language": "in het Nederlands",
        "ccy": "EUR",
        "home_topic": "kopen in China vanaf Nederland, veilig",
        "hero_h1": "FansBuy Spreadsheet: de gids om in China te kopen vanuit Nederland",
        "eyebrow": "Onafhankelijke gids, in het Nederlands",
        "lead": "Hoe je een productlink in de agent plakt, hoe de w2clinks-catalogus werkt, hoe een pakket naar Nederland reist en wat je checkt voor de Douane.",
        "fingerprint": dest_local_pack("NL")["fingerprint"],
        "customs": "Douane",
        "customs_url": "https://www.belastingdienst.nl/",
        "postal": "Nederlandse postcode, geen Belgische",
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
            (GUIDE_HREF, "FansBuy-handleiding"),
            ("/catalogus/", "Spreadsheet en categorieën"),
            (SHIP_HREF, "Verzending en douane"),
            ("/hulp/", "Hulp en vragen"),
            ("/nieuws/", "Nieuws"),
            ("/over-ons/", "Over ons"),
        ],
        "aliens": ("Packstation", "1010 Wien", "Poste Italiane", "form A1A 1A1", "no copiamos", "pas un code postal belge", "Northern Ireland is often another", "does not invent a de-minimis dollar", "do not copy a GST rate", "not a customs territory"),
        "not_found_tab": "Pagina niet gevonden",
        "login": "Inloggen bij FansBuy",
        "menu": "Menu openen",
        "home_cta": "Terug naar de homepage",
        "skip": "nl",
        "desk_css": "fansbuy-nl-desk.css",
        "css_id": "fansbuy-nl",
    },
    "de": {
        "host": "fansbuyspreadsheet.de",
        "dest": "DE",
        "dest_label": "Deutschland",
        "dest_zh": "Germany — 德国",
        "lang": "de-DE",
        "loc": "de",
        "in_language": "auf Deutsch",
        "ccy": "EUR",
        "home_topic": "in China kaufen aus Deutschland, sicher",
        "hero_h1": "FansBuy Spreadsheet: die Anleitung, um in China von Deutschland aus zu kaufen",
        "eyebrow": "Unabhängiger Leitfaden, auf Deutsch",
        "lead": "Wie du einen Produktlink in den Agenten einfügst, wie der w2clinks-Katalog funktioniert, wie ein Paket nach Deutschland reist und was du vor dem Zoll prüfst.",
        "fingerprint": dest_local_pack("DE")["fingerprint"],
        "customs": "Zoll",
        "customs_url": "https://www.zoll.de/",
        "postal": "deutsche PLZ, fünf Ziffern. Packstation möglich, nicht AT",
        "catalog": "/katalog/",
        "help": "/hilfe/",
        "news": "/neuigkeiten/",
        "about": "/ueber-uns/",
        "guide": GUIDE_HREF,
        "ship": SHIP_HREF,
        "nav": [
            ("/start/", "Start"),
            (GUIDE_HREF, "Anleitung"),
            ("/katalog/", "Katalog"),
            (SHIP_HREF, "Versand"),
            ("/hilfe/", "Hilfe"),
            ("/neuigkeiten/", "Neuigkeiten"),
        ],
        "footer_sections": [
            (GUIDE_HREF, "FansBuy-Anleitung"),
            ("/katalog/", "Spreadsheet und Kategorien"),
            (SHIP_HREF, "Versand und Zoll"),
            ("/hilfe/", "Hilfe und Fragen"),
            ("/neuigkeiten/", "Neuigkeiten"),
            ("/ueber-uns/", "Über uns"),
        ],
        "aliens": ("1010 Wien", "Poste Italiane", "form A1A 1A1", "pas un code postal belge", "Northern Ireland is often another", "no copiamos", "Nederlandse postcode", "does not invent a de-minimis dollar", "not a customs territory", "do not copy a GST rate"),
        "not_found_tab": "Seite nicht gefunden",
        "login": "Bei FansBuy anmelden",
        "menu": "Menü öffnen",
        "home_cta": "Zurück zur Startseite",
        "skip": "de",
        "desk_css": "fansbuy-de-desk.css",
        "css_id": "fansbuy-de",
    },
    "eu": {
        "host": "fansbuy.eu",
        "dest": None,
        "dest_label": "a member state",
        "dest_zh": "not a customs territory — pick DE/NL/IE",
        "lang": "en",
        "loc": "en",
        "in_language": "in English",
        "ccy": "EUR",
        "home_topic": "pick a member state, not this TLD",
        "hero_h1": "FansBuy Spreadsheet: this .eu hostname is not a customs territory",
        "eyebrow": "Independent guide, in English",
        "lead": "The official estimator needs a member-state country, not “EU”. How the w2clinks catalogue works, and why this TLD is not a destination.",
        "fingerprint": dest_local_pack(None)["fingerprint"],
        "customs": "taxation-customs.ec.europa.eu",
        "customs_url": "https://taxation-customs.ec.europa.eu/vat-e-commerce_en",
        "postal": "a real member-state address, not this hostname",
        "catalog": "/catalog/",
        "help": "/help/",
        "news": "/news/",
        "about": "/who-we-are/",
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
            (GUIDE_HREF, "FansBuy guide"),
            ("/catalog/", "The spreadsheet and the categories"),
            (SHIP_HREF, "Shipping and customs"),
            ("/help/", "Help and questions"),
            ("/news/", "News"),
            ("/who-we-are/", "About us"),
        ],
        "aliens": ("Packstation", "form A1A 1A1", "Poste Italiane", "no copiamos", "pas un code postal belge", "00-001 Warszawa", "Nederlandse postcode", "does not invent a de-minimis dollar", "1010 Wien", "Northern Ireland is often another", "do not copy a GST rate"),
        "not_found_tab": "Page not found",
        "login": "Log in to FansBuy",
        "menu": "Open menu",
        "home_cta": "Back to the homepage",
        "skip": "en",
        "desk_css": "fansbuy-eu-desk.css",
        "css_id": "fansbuy-eu",
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
            "Unabhängiger deutschsprachiger Leitfaden zu FansBuy und dazu, wie du den "
            f"Katalog von w2clinks nutzt, um von {p['dest_label']} aus in China zu kaufen."
        )
        independence = (
            "FansBuy Spreadsheet ist eine unabhängige Informationsseite. Wir sind nicht "
            "FansBuy, wir nehmen keine Bestellungen an, wir kassieren kein Porto und wir "
            "sehen dein Konto nicht. Bestellung, Zahlung und Reklamation laufen über die offizielle Site."
        )
        copyright = "&copy; 2026 FansBuy Spreadsheet. Deutscher Text, vor der Veröffentlichung gegengelesen."
        sections_h, official_h, independence_h, nav_aria = (
            "Bereiche", "Offizielle Links", "Unabhängigkeitshinweis.", "Hauptmenü",
        )
        nf_h1, nf_lead = "Diese Seite gibt es nicht", "Der Link ist vielleicht alt. Das sind die Bereiche, die existieren:"
        official_links = [
            (_off(p["host"]), "FansBuy (offizielle Site)"),
            (_off(p["host"], "/login"), "FansBuy-Konto"),
            (_off(p["host"], EST_PATH), f"Offizieller Schätzer ({DATE})"),
        ]
    elif loc == "it":
        intro = (
            "Guida indipendente in italiano su FansBuy e su come usi il catalogo w2clinks "
            "per comprare in Cina dall’Italia."
        )
        independence = (
            "FansBuy Spreadsheet è un sito informativo indipendente. Non siamo FansBuy, "
            "non elaboriamo ordini, non incassiamo il trasporto e non vediamo il tuo account. "
            "Ogni ordine, pagamento e reclamo passa dal sito ufficiale."
        )
        copyright = "&copy; 2026 FansBuy Spreadsheet. Testo italiano, riletto prima della pubblicazione."
        sections_h, official_h, independence_h, nav_aria = (
            "Sezioni", "Link ufficiali", "Nota di indipendenza.", "Menu principale",
        )
        nf_h1, nf_lead = "Questa pagina non esiste", "Il link forse è vecchio. Queste sezioni invece ci sono:"
        official_links = [
            (_off(p["host"]), "FansBuy (sito ufficiale)"),
            (_off(p["host"], "/login"), "Account FansBuy"),
            (_off(p["host"], EST_PATH), f"Preventivo ufficiale ({DATE})"),
        ]
    elif loc == "es":
        intro = (
            "Guía independiente en español sobre FansBuy y sobre cómo usas el catálogo "
            f"w2clinks para comprar en China desde {p['dest_label']}."
        )
        independence = (
            "FansBuy Spreadsheet es un sitio informativo independiente. No somos FansBuy, "
            "no tramitamos pedidos, no cobramos el envío y no vemos tu cuenta. "
            "Cada pedido, pago y reclamación pasa por el sitio oficial."
        )
        copyright = "&copy; 2026 FansBuy Spreadsheet. Texto en español, releído antes de publicar."
        sections_h, official_h, independence_h, nav_aria = (
            "Secciones", "Enlaces oficiales", "Aviso de independencia.", "Menú principal",
        )
        nf_h1, nf_lead = "Esta página no existe", "El enlace quizá sea antiguo. Estas secciones sí existen:"
        official_links = [
            (_off(p["host"]), "FansBuy (sitio oficial)"),
            (_off(p["host"], "/login"), "Cuenta FansBuy"),
            (_off(p["host"], EST_PATH), f"Estimador oficial ({DATE})"),
        ]
    elif loc == "fr":
        intro = (
            "Guide indépendant en français sur FansBuy et sur la façon d’utiliser le catalogue "
            f"w2clinks pour acheter en Chine depuis {p['dest_label']}."
        )
        independence = (
            "FansBuy Spreadsheet est un site d’information indépendant. Nous ne sommes pas FansBuy, "
            "nous ne traitons pas les commandes, nous n’encaissons pas le port et nous ne voyons "
            "pas ton compte. Chaque commande, paiement et réclamation passe par le site officiel."
        )
        copyright = "&copy; 2026 FansBuy Spreadsheet. Texte français, relu avant publication."
        sections_h, official_h, independence_h, nav_aria = (
            "Rubriques", "Liens officiels", "Mention d’indépendance.", "Menu principal",
        )
        nf_h1, nf_lead = "Cette page n’existe pas", "Le lien est peut-être ancien. Voici les rubriques qui existent :"
        official_links = [
            (_off(p["host"]), "FansBuy (site officiel)"),
            (_off(p["host"], "/login"), "Compte FansBuy"),
            (_off(p["host"], EST_PATH), f"Estimateur officiel ({DATE})"),
        ]
    elif loc == "nl":
        intro = (
            "Onafhankelijke Nederlandstalige gids over FansBuy en hoe je de w2clinks-catalogus "
            f"gebruikt om vanuit {p['dest_label']} in China te kopen."
        )
        independence = (
            "FansBuy Spreadsheet is een onafhankelijke infosite. Wij zijn FansBuy niet, "
            "we verwerken geen bestellingen, we innen geen porto en we zien je account niet. "
            "Elke bestelling, betaling en klacht loopt via de officiële site."
        )
        copyright = "&copy; 2026 FansBuy Spreadsheet. Nederlandse tekst, nagelezen voor publicatie."
        sections_h, official_h, independence_h, nav_aria = (
            "Onderdelen", "Officiële links", "Onafhankelijkheidsnotitie.", "Hoofdmenu",
        )
        nf_h1, nf_lead = "Deze pagina bestaat niet", "De link is misschien oud. Dit zijn de onderdelen die wel bestaan:"
        official_links = [
            (_off(p["host"]), "FansBuy (officiële site)"),
            (_off(p["host"], "/login"), "FansBuy-account"),
            (_off(p["host"], EST_PATH), f"Officiële schatter ({DATE})"),
        ]
    else:
        intro = (
            f"Independent English-language guide to FansBuy and to how you use the w2clinks "
            f"catalogue to buy in China from {p['dest_label']}."
        )
        independence = (
            "FansBuy Spreadsheet is an independent information site. We are not FansBuy, "
            "we do not process orders, we do not collect shipping fees and we cannot see "
            "your account. Every order, payment and claim runs through the official site."
        )
        copyright = "&copy; 2026 FansBuy Spreadsheet. English copy, edited and checked by people before publication."
        sections_h, official_h, independence_h, nav_aria = (
            "Sections", "Official links", "Independence notice.", "Main menu",
        )
        nf_h1, nf_lead = "This page does not exist", "The link may be old. These are the sections that do exist:"
        official_links = [
            (_off(p["host"]), "FansBuy (official site)"),
            (_off(p["host"], "/login"), "Log in to FansBuy"),
            (_off(p["host"], EST_PATH), f"Official estimator ({DATE})"),
        ]
    return CountryDesk(
        host=p["host"],
        agent="FansBuy",
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
        logo_src=f"/assets/images/fansbuy-wordmark.png?v={CSS_V}",
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
        theme_css="fansbuy-theme.css",
        desk_css=p["desk_css"],
        inner_marker=inner,
        register_path="/login",
        sheet_slug="fansbuy",
        invites=INVITES,
        extra_css=EXTRA_CSS,
        sections_h=sections_h,
        official_h=official_h,
        independence_h=independence_h,
        nav_aria=nav_aria,
        not_found_tab=p["not_found_tab"],
    )


def _facts(key: str) -> dict:
    p = PACKS[key]
    return {
        "agent": "FansBuy",
        "host": p["host"],
        "lang": p["lang"],
        "loc": p["loc"],
        "dest": p["dest"],
        "dest_label": p["dest_label"],
        "ccy": p["ccy"],
        "customs": p["customs"],
        "customs_url": p["customs_url"],
        "storage": _storage(p["loc"]),
        "keep": KEEP.get(key, KEEP["uk"]),
        "estimator": EST,
        "official": OFFICIAL,
        "date": DATE,
        "codes_off_title": list(INVITES),
        "strict_html_codes": True,
    }


def _faqs(key: str) -> list[tuple[str, str]]:
    p = PACKS[key]
    pairs = []
    for q, a in long_faqs(_facts(key)):
        a = a.replace("/api/products/", "w2clinks")
        a = re.sub(
            r"snapshot de 58 l[ií]neas ajenas",
            "recuento de líneas de otro agente",
            a,
            flags=re.I,
        )
        a = re.sub(r"58 l[ií]neas(?: ajenas)?", "líneas de otro agente", a, flags=re.I)
        pairs.append((q, a))
    extra = f"The delivery address uses a {p['postal']}."
    if p["loc"] == "de":
        extra = f"Die Lieferadresse ist eine {p['postal']}."
    elif p["loc"] == "it":
        extra = f"L’indirizzo di consegna è una {p['postal']}."
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
    if loc == "de":
        return [
            "Was FansBuy ist und in welcher Sprache es läuft",
            "Was du zahlen wirst",
            f"Einfuhr nach {dest}",
            "Lager, Fotos und was reisen darf",
            "Wenn etwas nicht stimmt",
        ]
    if loc == "it":
        return [
            "Che cos’è FansBuy e in quale lingua funziona",
            "Cosa paghi",
            "Importazione in Italia",
            "Magazzino, foto e cosa può viaggiare",
            "Se qualcosa non torna",
        ]
    if loc == "es":
        return [
            "Qué es FansBuy y en qué idioma funciona",
            "Qué vas a pagar",
            f"Importación a {dest}",
            "Almacén, fotos y qué puede viajar",
            "Si algo no cuadra",
        ]
    if loc == "fr":
        return [
            "Ce qu’est FansBuy et dans quelle langue ça tourne",
            "Ce que tu vas payer",
            f"Import vers {dest}",
            "Entrepôt, photos et ce qui peut voyager",
            "Si quelque chose cloche",
        ]
    if loc == "nl":
        return [
            "Wat FansBuy is en in welke taal het draait",
            "Wat je gaat betalen",
            f"Invoer naar {dest}",
            "Magazijn, foto’s en wat mag reizen",
            "Als iets niet klopt",
        ]
    return [
        "What FansBuy is, and which language it uses",
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
    elif loc == "it":
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
    if loc == "it":
        return cats_for(IT_LABELS)
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


def _est_note(key: str) -> str:
    s = EST_SNAP[key]
    loc = PACKS[key]["loc"]
    dest_zh = PACKS[key]["dest_zh"]
    if loc == "de":
        return (
            f"Am {DATE} zeigte der öffentliche Schätzer Ziel {s['dest']} ({dest_zh}), "
            f"1000 g und 35×25×10 cm, unter anderem {s['line']}, {s['price']}, {s['days']} Tage, {s['n']} Linien. "
            "Die Zahlen stehen in USD auf der offiziellen Site und ändern sich; öffne den Schätzer erneut."
        )
    if loc == "it":
        return (
            f"Il {DATE} lo stimatore pubblico con destinazione {s['dest']} ({dest_zh}), "
            f"1000 g e 35×25×10 cm ha mostrato tra le altre {s['line']}, {s['price']}, {s['days']} giorni, {s['n']} linee. "
            "I cifre sono in USD sul sito ufficiale e cambiano; riapri lo stimatore."
        )
    if loc == "es":
        return (
            f"El {DATE} el estimador público con destino {s['dest']} ({dest_zh}), "
            f"1000 g y 35×25×10 cm mostró entre otras {s['line']}, {s['price']}, {s['days']} días, {s['n']} líneas. "
            "Las cifras salen en USD en el sitio oficial y cambian; abre el estimador otra vez."
        )
    if loc == "fr":
        return (
            f"Le {DATE} l’estimateur public avec destination {s['dest']} ({dest_zh}), "
            f"1000 g et 35×25×10 cm a montré entre autres {s['line']}, {s['price']}, {s['days']} jours, {s['n']} lignes. "
            "Les montants sont en USD sur le site officiel et changent ; rouvre l’estimateur."
        )
    if loc == "nl":
        return (
            f"Op {DATE} toonde de publieke schatter bestemming {s['dest']} ({dest_zh}), "
            f"1000 g en 35×25×10 cm onder meer {s['line']}, {s['price']}, {s['days']} dagen, {s['n']} lijnen. "
            "De bedragen staan in USD op de officiële site en veranderen; open de schatter opnieuw."
        )
    return (
        f"On {DATE} the public estimator with destination {s['dest']} ({dest_zh}), "
        f"1000 g and 35×25×10 cm showed among others {s['line']}, {s['price']}, {s['days']} days, {s['n']} lines. "
        "Amounts are USD on the official site and they change; open the estimator again."
    )


def _status_ul(key: str) -> str:
    loc = PACKS[key]["loc"]
    rows = {
        "de": [
            ("Order Submitted", "Bestellung gesendet, Produkt in China bezahlt."),
            ("Order Placed", "FansBuy kauft im chinesischen Shop auf deinen Namen."),
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
            ("Order Placed", "FansBuy compra nel negozio cinese a tuo nome."),
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
            ("Order Placed", "FansBuy compra en la tienda china a tu nombre."),
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
            ("Order Placed", "FansBuy achète dans la boutique chinoise à ton nom."),
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
            ("Order Placed", "FansBuy koopt in de Chinese shop op jouw naam."),
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
            ("Order Placed", "FansBuy buys in the Chinese shop in your name."),
            ("Seller Shipped", "The Chinese seller has shipped."),
            ("Arrived at Warehouse", "Arrived at the warehouse."),
            ("Inspection & Storage", "Check, photos and storage. Live labels sit in the app."),
            ("Shipping Requested", "You consolidate and book the international line."),
            ("Parcel Packed", "The box is packed."),
            ("Shipped", "Departure from China."),
            ("Delivered", "Delivered; confirm receipt in the app."),
        ],
    }[loc if loc in ("de", "it", "es", "fr", "nl") else "en"]
    return "<ul class=\"tl\">" + "".join(
        f"<li><b>{escape(a)}</b><span>{escape(b)}</span></li>" for a, b in rows
    ) + "</ul>"


def _guide_extra(key: str, fig_pay: str, fig_est: str) -> str:
    loc = PACKS[key]["loc"]
    ul = _status_ul(key)
    note = escape(_est_note(key))
    store = escape(_storage(loc if loc in ("de", "it", "es", "fr", "nl") else "en"))
    if loc == "de":
        return f"""
  {ul}
  {fig_pay}
  <h2>Der Schätzer ist öffentlich; DIY Order nicht</h2>
  <p>{note} DIY Order auf fansbuy.com öffnete die Login-Wand. Dieser Desk füllt kein DIY-Formular aus.</p>
  {fig_est}
  <h2>Lagerfrist steht in Help, nicht als erfundene Zahl hier</h2>
  <p>{store} Die 90-Tage-Zeile steht auf der offiziellen Startseite unter QC & Storage, nicht als Coupon-Fenster.</p>
"""
    if loc == "it":
        return f"""
  {ul}
  {fig_pay}
  <h2>Lo stimatore è pubblico; DIY Order no</h2>
  <p>{note} DIY Order su fansbuy.com ha aperto il login. Questa guida non compila un modulo DIY.</p>
  {fig_est}
  <h2>I giorni di magazzino stanno in Help, non come cifra inventata qui</h2>
  <p>{store} La regola dei 90 giorni sta sulla homepage ufficiale sotto QC & Storage, non come finestra coupon.</p>
"""
    if loc == "es":
        return f"""
  {ul}
  {fig_pay}
  <h2>El estimador es público; DIY Order no</h2>
  <p>{note} DIY Order en fansbuy.com abrió el login. Esta guía no rellena un formulario DIY.</p>
  {fig_est}
  <h2>El plazo de almacén está en Help, no como cifra inventada aquí</h2>
  <p>{store} La regla de 90 días está en la portada oficial bajo QC & Storage, no como ventana de cupones.</p>
"""
    if loc == "fr":
        return f"""
  {ul}
  {fig_pay}
  <h2>L’estimateur est public ; DIY Order non</h2>
  <p>{note} DIY Order sur fansbuy.com a ouvert le login. Ce guide ne remplit pas un formulaire DIY.</p>
  {fig_est}
  <h2>Le délai d’entrepôt est dans Help, pas un chiffre inventé ici</h2>
  <p>{store} La règle des 90 jours est sur la page d’accueil officielle, QC & Storage, pas une fenêtre coupon.</p>
"""
    if loc == "nl":
        return f"""
  {ul}
  {fig_pay}
  <h2>De schatter is publiek; DIY Order niet</h2>
  <p>{note} DIY Order op fansbuy.com opende de loginmuur. Deze gids vult geen DIY-formulier in.</p>
  {fig_est}
  <h2>De magazijntermijn staat in Help, niet als verzonnen getal hier</h2>
  <p>{store} De 90-dagenregel staat op de officiële homepage onder QC & Storage, niet als coupon-venster.</p>
"""
    return f"""
  {ul}
  {fig_pay}
  <h2>The estimator is public; DIY Order is not</h2>
  <p>{note} DIY Order on fansbuy.com opened the login wall. This desk does not fill in a DIY form.</p>
  {fig_est}
  <h2>Warehouse days are named in Help, not invented here</h2>
  <p>{store} The 90-day line is on the official homepage under QC & Storage, not as a coupon-pack window.</p>
"""


def _shots(key: str) -> dict[str, str]:
    loc = PACKS[key]["loc"]
    snap = EST_SNAP[key]
    dest_zh = PACKS[key]["dest_zh"]
    if loc == "de":
        home_alt, home_cap = (
            "Offizielle FansBuy-Startseite: grünes Wortmark, Paste-Leiste und drei Schritte Place Orders, Submit Parcels, Sign Delivery",
            f"Offizielle Homepage von fansbuy.com, {DATE}. Die drei Schritte unter der Suche sind der Kreis: in China bestellen, im Lager bündeln, international empfangen.",
        )
        guide_alt, guide_cap = (
            "Offizielle FansBuy-Paste-Leiste: Goods/shop's link or name und die drei Schritte darunter",
            "Paste-Leiste auf fansbuy.com. Ein Taobao-, 1688- oder Weidian-Link einfügen, oder den Namen tippen. Aufnahme 6 Oct 2026.",
        )
        pay_alt, pay_cap = (
            "Offizielle FansBuy-Startseite, Schritt QC & Storage: 90 free warehouse days; CN¥ 0.1/item/day after, max 180 days",
            f"Offizielle Homepage, QC & Storage, {DATE}. Die 90-Tage-Lagerregel steht auf der Startseite, nicht als erfundene Zahl und nicht als Coupon-Fenster.",
        )
        sheet_alt, sheet_cap = (
            "FansBuy-Katalog auf w2clinks: Produktkarten mit Foto, Marke und Referenzpreis",
            "Karten, keine Excel-Zellen. Yuan-Preise ändern sich täglich. Aufnahme 6 Oct 2026, Kategorie SNEAKERS.",
        )
        vol_alt, vol_cap = (
            "Rechenbeispiel Volumengewicht: 40×40×3 cm und 200 g Waage werden 600 g Volumen",
            "Ein Rechenbeispiel, kein Lagerfoto. Viele Linien rechnen das Maximum aus Waage und Volumen, oft L×B×H (cm) / 8000.",
        )
        zoek_alt, zoek_cap = (
            "Hoodie-Suche im FansBuy-Katalog auf w2clinks",
            "Ergebnisse mit Filterspalte. Aufnahme 6 Oct 2026.",
        )
        diy_alt, diy_cap = (
            "FansBuy DIY Order öffnete Sign In / Register unter /login?redirect=/order/manual",
            "DIY Order auf fansbuy.com verlangt Login. Der öffentliche Schätzer unter /estimates ist ohne Login. Dieser Desk erfindet kein ausgefülltes DIY-Formular.",
        )
        est_alt, est_cap = (
            f"Offizieller FansBuy-Schätzer, Ziel {snap['dest']}, 1000 g, 35×25×10 cm, Linie {snap['line']}",
            f"Öffentlicher Schätzer, Ziel {snap['dest']} ({dest_zh}), 1000 g und 35×25×10 cm. {DATE} zeigte u. a. {snap['line']}, {snap['price']}, {snap['days']} Tage, {snap['n']} Linien. Die Zahlen ändern sich; öffne den Schätzer erneut.",
        )
    elif loc == "it":
        home_alt, home_cap = (
            "Homepage ufficiale FansBuy: wordmark verde, barra per incollare e tre passi Place Orders, Submit Parcels, Sign Delivery",
            f"Homepage ufficiale di fansbuy.com, {DATE}. I tre passi sotto la ricerca sono il giro: ordinare in Cina, consolidare in magazzino, ricevere all’estero.",
        )
        guide_alt, guide_cap = (
            "Barra ufficiale FansBuy: Goods/shop's link or name e i tre passi sotto",
            "Barra su fansbuy.com. Incolla un link Taobao, 1688 o Weidian, o digita il nome. Scatto 6 Oct 2026.",
        )
        pay_alt, pay_cap = (
            "Homepage ufficiale FansBuy, passo QC & Storage: 90 free warehouse days; CN¥ 0.1/item/day after, max 180 days",
            f"Homepage ufficiale, QC & Storage, {DATE}. La regola dei 90 giorni di magazzino sta in homepage, non come cifra inventata e non come finestra coupon.",
        )
        sheet_alt, sheet_cap = (
            "Catalogo FansBuy su w2clinks: schede con foto, marca e prezzo di riferimento",
            "Schede, non celle Excel. I prezzi in yuan cambiano ogni giorno. Scatto 6 Oct 2026, categoria SNEAKERS.",
        )
        vol_alt, vol_cap = (
            "Esempio di peso volumetrico: 40×40×3 cm e 200 g in bilancia diventano 600 g di volume",
            "Un esempio calcolato, non una foto di magazzino. Molte linee fatturano il massimo tra bilancia e volume, spesso L×W×H (cm) / 8000.",
        )
        zoek_alt, zoek_cap = (
            "Ricerca hoodie nel catalogo FansBuy su w2clinks",
            "Risultati con colonna filtri. Scatto 6 Oct 2026.",
        )
        diy_alt, diy_cap = (
            "FansBuy DIY Order ha aperto Sign In / Register su /login?redirect=/order/manual",
            "DIY Order su fansbuy.com chiede il login. Lo stimatore pubblico /estimates è senza login. Questa guida non inventa un modulo DIY compilato.",
        )
        est_alt, est_cap = (
            f"Stimatore ufficiale FansBuy, destinazione {snap['dest']}, 1000 g, 35×25×10 cm, linea {snap['line']}",
            f"Stimatore pubblico, destinazione {snap['dest']} ({dest_zh}), 1000 g e 35×25×10 cm. Il {DATE} ha mostrato tra le altre {snap['line']}, {snap['price']}, {snap['days']} giorni, {snap['n']} linee. I cifre cambiano; riapri lo stimatore.",
        )
    elif loc == "es":
        home_alt, home_cap = (
            "Portada oficial de FansBuy: wordmark verde, barra para pegar y tres pasos Place Orders, Submit Parcels, Sign Delivery",
            f"Portada oficial de fansbuy.com, {DATE}. Los tres pasos bajo la búsqueda son el circuito: pedir en China, consolidar en almacén, recibir fuera.",
        )
        guide_alt, guide_cap = (
            "Barra oficial FansBuy: Goods/shop's link or name y los tres pasos debajo",
            "Barra en fansbuy.com. Pega un enlace Taobao, 1688 o Weidian, o escribe el nombre. Captura 6 Oct 2026.",
        )
        pay_alt, pay_cap = (
            "Portada oficial de FansBuy, paso QC & Storage: 90 free warehouse days; CN¥ 0.1/item/day after, max 180 days",
            f"Portada oficial, QC & Storage, {DATE}. La regla de 90 días de almacén está en la portada, no como cifra inventada ni como ventana de cupones.",
        )
        sheet_alt, sheet_cap = (
            "Catálogo FansBuy en w2clinks: fichas con foto, marca y precio de referencia",
            "Fichas, no celdas de Excel. Los precios en yuan cambian cada día. Captura 6 Oct 2026, categoría SNEAKERS.",
        )
        vol_alt, vol_cap = (
            "Ejemplo de peso volumétrico: 40×40×3 cm y 200 g en báscula son 600 g de volumen",
            "Un ejemplo calculado, no una foto de almacén. Muchas líneas facturan el máximo entre báscula y volumen, a menudo L×W×H (cm) / 8000.",
        )
        zoek_alt, zoek_cap = (
            "Búsqueda de hoodie en el catálogo FansBuy de w2clinks",
            "Resultados con columna de filtros. Captura 6 Oct 2026.",
        )
        diy_alt, diy_cap = (
            "FansBuy DIY Order abrió Sign In / Register en /login?redirect=/order/manual",
            "DIY Order en fansbuy.com pide login. El estimador público /estimates no pide login. Esta guía no inventa un formulario DIY relleno.",
        )
        est_alt, est_cap = (
            f"Estimador oficial FansBuy, destino {snap['dest']}, 1000 g, 35×25×10 cm, línea {snap['line']}",
            f"Estimador público, destino {snap['dest']} ({dest_zh}), 1000 g y 35×25×10 cm. El {DATE} mostró entre otras {snap['line']}, {snap['price']}, {snap['days']} días, {snap['n']} líneas. Las cifras cambian; abre el estimador otra vez.",
        )
    elif loc == "fr":
        home_alt, home_cap = (
            "Page d’accueil officielle FansBuy : wordmark vert, barre de collage et trois étapes Place Orders, Submit Parcels, Sign Delivery",
            f"Page d’accueil officielle d’fansbuy.com, {DATE}. Les trois étapes sous la recherche sont le circuit : commander en Chine, regrouper en entrepôt, recevoir à l’étranger.",
        )
        guide_alt, guide_cap = (
            "Barre officielle FansBuy : Goods/shop's link or name et les trois étapes en dessous",
            "Barre sur fansbuy.com. Colle un lien Taobao, 1688 ou Weidian, ou tape le nom. Capture 6 Oct 2026.",
        )
        pay_alt, pay_cap = (
            "Page d’accueil officielle FansBuy, étape QC & Storage : 90 free warehouse days; CN¥ 0.1/item/day after, max 180 days",
            f"Page d’accueil officielle, QC & Storage, {DATE}. La règle des 90 jours d’entrepôt est sur la page d’accueil, pas un chiffre inventé ni une fenêtre coupon.",
        )
        sheet_alt, sheet_cap = (
            "Catalogue FansBuy sur w2clinks : fiches avec photo, marque et prix de référence",
            "Des fiches, pas des cellules Excel. Les prix en yuan changent chaque jour. Capture 6 Oct 2026, catégorie SNEAKERS.",
        )
        vol_alt, vol_cap = (
            "Exemple de poids volumétrique : 40×40×3 cm et 200 g à la balance deviennent 600 g de volume",
            "Un exemple calculé, pas une photo d’entrepôt. Beaucoup de lignes facturent le max entre balance et volume, souvent L×W×H (cm) / 8000.",
        )
        zoek_alt, zoek_cap = (
            "Recherche hoodie dans le catalogue FansBuy sur w2clinks",
            "Résultats avec colonne de filtres. Capture 6 Oct 2026.",
        )
        diy_alt, diy_cap = (
            "FansBuy DIY Order a ouvert Sign In / Register sur /login?redirect=/order/manual",
            "DIY Order sur fansbuy.com demande un login. L’estimateur public /estimates n’en demande pas. Ce guide n’invente pas un formulaire DIY rempli.",
        )
        est_alt, est_cap = (
            f"Estimateur officiel FansBuy, destination {snap['dest']}, 1000 g, 35×25×10 cm, ligne {snap['line']}",
            f"Estimateur public, destination {snap['dest']} ({dest_zh}), 1000 g et 35×25×10 cm. Le {DATE} a montré entre autres {snap['line']}, {snap['price']}, {snap['days']} jours, {snap['n']} lignes. Les montants changent ; rouvre l’estimateur.",
        )
    elif loc == "nl":
        home_alt, home_cap = (
            "Officiële FansBuy-homepage: groene wordmark, plakbalk en drie stappen Place Orders, Submit Parcels, Sign Delivery",
            f"Officiële homepage van fansbuy.com, {DATE}. De drie stappen onder de zoekbalk zijn de ronde: bestellen in China, bundelen in het magazijn, internationaal ontvangen.",
        )
        guide_alt, guide_cap = (
            "Officiële FansBuy-plakbalk: Goods/shop's link or name en de drie stappen eronder",
            "Plakbalk op fansbuy.com. Plak een Taobao-, 1688- of Weidian-link, of typ de naam. Opname 6 Oct 2026.",
        )
        pay_alt, pay_cap = (
            "Officiële FansBuy-homepage, stap QC & Storage: 90 free warehouse days; CN¥ 0.1/item/day after, max 180 days",
            f"Officiële homepage, QC & Storage, {DATE}. De 90-dagen-magazijnregel staat op de homepage, niet als verzonnen getal en niet als coupon-venster.",
        )
        sheet_alt, sheet_cap = (
            "FansBuy-catalogus op w2clinks: kaarten met foto, merk en referentieprijs",
            "Kaarten, geen Excel-cellen. Yuan-prijzen veranderen per dag. Opname 6 Oct 2026, categorie SNEAKERS.",
        )
        vol_alt, vol_cap = (
            "Voorbeeld volumgewicht: 40×40×3 cm en 200 g op de weegschaal wordt 600 g volume",
            "Een rekenvoorbeeld, geen magazijnfoto. Veel lijnen factureren het maximum van weegschaal en volume, vaak L×W×H (cm) / 8000.",
        )
        zoek_alt, zoek_cap = (
            "Hoodie-zoekopdracht in de FansBuy-catalogus op w2clinks",
            "Resultaten met filterkolom. Opname 6 Oct 2026.",
        )
        diy_alt, diy_cap = (
            "FansBuy DIY Order opende Sign In / Register op /login?redirect=/order/manual",
            "DIY Order op fansbuy.com vraagt login (`/order/manual`). De publieke schatter onder /estimates niet. Deze gids verzint geen ingevuld DIY-formulier.",
        )
        est_alt, est_cap = (
            f"Officiële FansBuy-schatter, bestemming {snap['dest']}, 1000 g, 35×25×10 cm, lijn {snap['line']}",
            f"Publieke schatter, bestemming {snap['dest']} ({dest_zh}), 1000 g en 35×25×10 cm. {DATE} toonde o.a. {snap['line']}, {snap['price']}, {snap['days']} dagen, {snap['n']} lijnen. Die cijfers veranderen; open de schatter opnieuw.",
        )
    else:
        home_alt, home_cap = (
            "Official FansBuy homepage: green wordmark, paste bar and three steps Place Orders, Submit Parcels, Sign Delivery",
            f"Official homepage of fansbuy.com, {DATE}. The three steps under the search bar are the loop: order in China, consolidate in the warehouse, receive abroad.",
        )
        guide_alt, guide_cap = (
            "Official FansBuy paste bar: Goods/shop's link or name and the three steps below",
            "Paste bar on fansbuy.com. Paste a Taobao, 1688 or Weidian link, or type the name. Capture 6 Oct 2026.",
        )
        pay_alt, pay_cap = (
            "Official FansBuy homepage, QC & Storage step: 90 free warehouse days; CN¥ 0.1/item/day after, max 180 days",
            f"Official homepage, QC & Storage, {DATE}. The 90-day warehouse line is named on the homepage, not as an invented number and not as a coupon-pack window.",
        )
        sheet_alt, sheet_cap = (
            "FansBuy catalogue on w2clinks: product cards with photo, brand and reference price",
            "Cards, not Excel cells. Yuan prices change by the day. Capture 6 Oct 2026, category SNEAKERS.",
        )
        vol_alt, vol_cap = (
            "Worked example of volume weight: 40×40×3 cm and 200 g scale becomes 600 g volume",
            "A worked example, not a warehouse photo. Many lines bill the greater of scale and volume, often L×W×H (cm) / 8000.",
        )
        zoek_alt, zoek_cap = (
            "Hoodie search in the FansBuy catalogue on w2clinks",
            "Results with the filter column. Capture 6 Oct 2026.",
        )
        diy_alt, diy_cap = (
            "FansBuy DIY Order opened Sign In / Register at /login?redirect=/order/manual",
            "DIY Order on fansbuy.com asks for login (`/order/manual`). The public estimator at /estimates does not. This desk does not invent a filled DIY total.",
        )
        est_alt, est_cap = (
            f"Official FansBuy estimator, destination {snap['dest']}, 1000 g, 35×25×10 cm, line {snap['line']}",
            f"Public estimator, destination {snap['dest']} ({dest_zh}), 1000 g and 35×25×10 cm. {DATE} showed among others {snap['line']}, {snap['price']}, {snap['days']} days, {snap['n']} lines. Those figures change; open the estimator again.",
        )
    return {
        "home": _fig("/img/shots/oficial-inicio.jpg", home_alt, home_cap),
        "guide": _fig("/img/shots/oficial-guidebook.jpg", guide_alt, guide_cap, 1200, 450),
        "pay": _fig("/img/shots/oficial-guidebook-3.jpg", pay_alt, pay_cap),
        "sheet": _fig("/img/shots/catalogus.jpg", sheet_alt, sheet_cap, 1200, 900),
        "est": _fig(f"/img/shots/estimator-{key}.jpg", est_alt, est_cap),
        "vol": _fig("/img/shots/volume-voorbeeld.jpg", vol_alt, vol_cap, 1200, 640),
        "diy": _fig("/img/shots/oficial-diy.jpg", diy_alt, diy_cap),
        "zoek": _fig("/img/shots/catalogus-zoek.jpg", zoek_alt, zoek_cap, 1200, 900),
    }


def _sec_shots(key: str, fig) -> str:
    p = PACKS[key]
    loc, dest = p["loc"], p["dest_label"]
    if loc == "de":
        return f"""
<section class="sec" id="shots">
  <div class="wrap"><div class="split split--rev"><div>
    <h2>Einen chinesischen Link einfügen, oder in der App suchen</h2>
    <p class="lead">FansBuy beginnt so: einen Link von Taobao, 1688 oder Weidian einfügen, oder den Namen tippen. Der chinesische Shop sieht FansBuy; du siehst danach Lagerfotos und eine Linie nach {escape(dest)}.</p>
    <p>Liest die Suche den Link nicht, ist das manuelle Formular der nächste Schritt: Name, Größe, Farbe und Preis in Yuan. International zahlst du erst später, aus dem Lager.</p>
    <p><a class="btn" href="{escape(p["guide"])}">Anleitung Schritt für Schritt</a>
       <a class="btn btn--ghost" href="{escape(OFFICIAL)}" rel="noopener">Offizielle Site</a></p>
  </div>{fig}</div></div>
</section>
"""
    if loc == "it":
        return f"""
<section class="sec" id="shots">
  <div class="wrap"><div class="split split--rev"><div>
    <h2>Incolla un link cinese, o cerca nell’app</h2>
    <p class="lead">FansBuy parte così: incolli un link di Taobao, 1688 o Weidian, o digiti il nome. Il negozio cinese vede FansBuy; tu poi vedi le foto di magazzino e una linea verso l’Italia.</p>
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
    <p class="lead">FansBuy empieza así: pegas un enlace de Taobao, 1688 o Weidian, o escribes el nombre. La tienda china ve FansBuy; tú luego ves fotos de almacén y una línea hacia {escape(dest)}.</p>
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
    <p class="lead">FansBuy commence ainsi : tu colles un lien Taobao, 1688 ou Weidian, ou tu tapes le nom. La boutique chinoise voit FansBuy ; toi, tu vois ensuite les photos d’entrepôt et une ligne vers {escape(dest)}.</p>
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
    <p class="lead">FansBuy start zo: je plakt een Taobao-, 1688- of Weidian-link, of typt de naam. De Chinese shop ziet FansBuy; jij ziet daarna magazijnfoto’s en een lijn naar {escape(dest)}.</p>
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
    <p class="lead">FansBuy starts the same way: paste a Taobao, 1688 or Weidian link, or type the name. The Chinese shop sees FansBuy; you later see warehouse photos and a line to {escape(dest)}.</p>
    <p>If the search bar does not read the link, the next step is a manual form: name, size, colour and price in yuan. International freight is paid later, from the warehouse.</p>
    <p><a class="btn" href="{escape(p["guide"])}">Step-by-step guide</a>
       <a class="btn btn--ghost" href="{escape(OFFICIAL)}" rel="noopener">Official site</a></p>
  </div>{fig}</div></div>
</section>
"""


def _sec_states(key: str, fig) -> str:
    p = PACKS[key]
    loc, dest = p["loc"], p["dest_label"]
    if loc == "de":
        return f"""
<section class="sec" id="states">
  <div class="wrap"><div class="split"><div>
    <h2>Neun Status, drei Bildschirme</h2>
    <p class="lead">Zuerst zahlst du das Produkt plus den Inlandsweg in China bis zum Lager. International kommt später, wenn du eine Linie nach {escape(dest)} wählst. «Warum steht es still?» heißt fast immer: du schaust auf den falschen Bildschirm.</p>
    {_status_ul(key)}
    <p>Die ersten Schritte liegen unter Bestellungen, danach Lager, danach das Paket, das du absendest. {escape(_est_note(key))} {escape(_storage(loc))}</p>
    <p><a class="btn" href="{escape(p["guide"])}">Anleitung mit dem Verlauf</a></p>
  </div>{fig}</div></div>
</section>
"""
    if loc == "it":
        return f"""
<section class="sec" id="states">
  <div class="wrap"><div class="split"><div>
    <h2>Nove stati, tre schermate</h2>
    <p class="lead">Prima paghi il prodotto più il trasporto interno in Cina fino al magazzino. L’internazionale arriva dopo, quando scegli una linea verso l’Italia. «Perché è fermo?» quasi sempre significa: stai guardando la schermata sbagliata.</p>
    {_status_ul(key)}
    <p>I primi passi stanno sotto gli ordini, poi il magazzino, poi il pacco che invii. {escape(_est_note(key))} {escape(_storage(loc))}</p>
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
    {_status_ul(key)}
    <p>Los primeros pasos están bajo pedidos, luego almacén, luego el paquete que envías. {escape(_est_note(key))} {escape(_storage(loc))}</p>
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
    {_status_ul(key)}
    <p>Les premiers pas sont sous les commandes, puis l’entrepôt, puis le colis que tu envoies. {escape(_est_note(key))} {escape(_storage(loc))}</p>
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
    {_status_ul(key)}
    <p>De eerste stappen staan onder bestellingen, daarna magazijn, daarna het pakket dat je verzendt. {escape(_est_note(key))} {escape(_storage(loc))}</p>
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
    <p>The first stretch lives under orders, then warehouse, then the parcel you submit. {escape(_est_note(key))} {escape(_storage("en"))}</p>
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
    <p>Regel: ohne echten Preis und Varianten nicht bestellen. Tabak, Alkohol und Arzneimittel reisen nicht. Restricted ist eine Kaufsperre, kein Bescheid vom {escape(customs)}. FansBuy verkauft keine eigene Ware.</p>
  </div>{fig}</div></div>
</section>
"""
    if loc == "it":
        return f"""
<section class="sec sec--tint" id="restricted">
  <div class="wrap"><div class="split split--rev"><div>
    <h2>Molti prodotti non si possono comprare anche se compaiono</h2>
    <p class="lead">Sul sito ufficiale vedi schede senza prezzo, o un modulo manuale al posto di una scheda negozio. Non è un bug di questa homepage: il link sorgente non è acquistabile tramite l’agente, o il prezzo non si è letto.</p>
    <p>Regola: senza prezzo vero e varianti non ordinare. Tabacco, alcol e farmaci non viaggiano. Restricted è un blocco d’acquisto, non un avviso della {escape(customs)}. FansBuy non vende merce propria.</p>
  </div>{fig}</div></div>
</section>
"""
    if loc == "es":
        return f"""
<section class="sec sec--tint" id="restricted">
  <div class="wrap"><div class="split split--rev"><div>
    <h2>Muchos productos no se pueden comprar aunque aparezcan</h2>
    <p class="lead">En el sitio oficial ves fichas sin precio, o un formulario manual en lugar de una ficha de tienda. No es un fallo de esta portada: el enlace de origen no se puede comprar por el agente, o el precio no se leyó.</p>
    <p>Regla: sin precio real y variantes, no pidas. Tabaco, alcohol y medicamentos no viajan. Restricted es un bloqueo de compra, no un aviso de {escape(customs)}. FansBuy no vende mercancía propia.</p>
  </div>{fig}</div></div>
</section>
"""
    if loc == "fr":
        return f"""
<section class="sec sec--tint" id="restricted">
  <div class="wrap"><div class="split split--rev"><div>
    <h2>Beaucoup de produits ne s’achètent pas même s’ils s’affichent</h2>
    <p class="lead">Sur le site officiel tu vois des fiches sans prix, ou un formulaire manuel à la place d’une fiche boutique. Ce n’est pas un bug de cette page d’accueil : le lien source n’est pas achetable via l’agent, ou le prix n’a pas pu être lu.</p>
    <p>Règle : sans vrai prix et variantes, n’ordonne pas. Tabac, alcool et médicaments ne voyagent pas. Restricted est un blocage d’achat, pas un avis de {escape(customs)}. FansBuy ne vend pas de stock propre.</p>
  </div>{fig}</div></div>
</section>
"""
    if loc == "nl":
        return f"""
<section class="sec sec--tint" id="restricted">
  <div class="wrap"><div class="split split--rev"><div>
    <h2>Veel producten kun je niet kopen, ook al staan ze er</h2>
    <p class="lead">Op de officiële site zie je kaarten zonder prijs, of een handmatig formulier in plaats van een shopkaart. Dat is geen bug van deze homepage: de bronlink is via de agent niet te koop, of de prijs liet zich niet lezen.</p>
    <p>Regel: zonder echte prijs en varianten niet bestellen. Tabak, alcohol en geneesmiddelen reizen niet. Restricted is een koopblokkade, geen bericht van {escape(customs)}. FansBuy verkoopt geen eigen voorraad.</p>
  </div>{fig}</div></div>
</section>
"""
    return f"""
<section class="sec sec--tint" id="restricted">
  <div class="wrap"><div class="split split--rev"><div>
    <h2>Many products you cannot buy even if they appear</h2>
    <p class="lead">On the official site you will see cards without a price, or a manual form instead of a shop card. That is not a bug of this homepage: the source link is not buyable through the agent, or the price could not be read.</p>
    <p>Rule: without a real price and variants, do not order. Tobacco, alcohol and medicines do not travel. Restricted is a purchase block, not a {escape(customs)} seizure notice. FansBuy does not sell its own stock.</p>
  </div>{fig}</div></div>
</section>
"""


def build_home(key: str) -> str:
    p = PACKS[key]
    desk = desk_for(key)
    sheet = _sheet(desk)
    wall = _wall(key)
    chips = _chips(key)
    s = _shots(key)
    fig_off, fig_sheet, fig_vol = s["home"], s["sheet"], s["vol"]
    fig_est, fig_diy = s["est"], s["diy"]
    dest = p["dest_label"]
    loc = p["loc"]
    shots = _sec_shots(key, s["guide"])
    states = _sec_states(key, s["pay"])
    restricted = _sec_restricted(key, fig_diy)
    if loc == "de":
        body = f"""
<section class="hero">
  <div class="hero__bg" role="img" aria-label="Offizielle FansBuy-Startseite"></div>
  <div class="hero__scrim"></div>
  <div class="wrap">
    <span class="eyebrow">{escape(p["eyebrow"])}</span>
    <h1>{escape(p["hero_h1"])}</h1>
    <p class="lead">{escape(p["lead"])}</p>
    <div class="sbox">
      <form id="w2c-search" action="{escape(sheet)}" method="get" target="_blank" rel="nofollow noopener" role="search">
        <label class="skip" for="q">Produkte auf w2clinks suchen</label>
        <input id="q" name="q" type="search" autocomplete="off" placeholder="Suche Turnschuhe, Hoodie, Jacke…">
        <input type="hidden" name="utm_source" value="{escape(p["host"])}">
        <input type="hidden" name="utm_medium" value="referral">
        <input type="hidden" name="utm_campaign" value="hero-buscador">
        <button type="submit">Suchen</button>
      </form>
      <div class="chips">{chips}</div>
    </div>
  </div>
</section>
<section class="sec sec--first" id="agent">
  <div class="wrap"><div class="split"><div>
    <h2>Ein Einkaufsagent ist ein Zwischenhändler, kein Shop</h2>
    <p class="lead">FansBuy verkauft keine eigene Ware. Er kauft für dich in chinesischen Shops, die nicht ins Ausland senden, nimmt das Paket im Lager an, fotografiert es, lagert es und schickt es nach {escape(dest)}, wenn du das entscheidest.</p>
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
    <p class="lead">Im Schätzer Ziel <strong>{escape(p["dest_zh"])}</strong> wählen, {escape(p.get("lab_not", "nicht EU"))}. Die Lieferadresse ist eine {escape(p["postal"])}.</p>
    <p>{escape(_est_note(key))} Quelle: <a href="{escape(p["customs_url"])}" rel="noopener">{escape(p["customs"])}</a>.</p>
    <p><a class="btn" href="{escape(EST)}">Offizielle FansBuy-Site</a>
       <a class="btn btn--ghost" href="{escape(p["ship"])}">Versandplan</a></p>
  </div>{fig_est}</div></div>
</section>
<section class="sec" id="volume">
  <div class="wrap"><div class="split split--rev"><div>
    <h2>Das Gewicht, das du zahlst, ist fast nie nur die Waage</h2>
    <p class="lead">Viele Linien rechnen das Maximum aus Waage und Volumen. Ein üblicher Teiler ist L×B×H (cm) / 8000. Eine Daunenjacke ist leicht und voluminös: dort entscheidet das Volumen.</p>
    <p>Beispiel: 40×40×3 cm sind 4800 cm³, geteilt durch 8000 sind 600 g Volumen bei 200 g Echtgewicht. Deine Maße trägst du im öffentlichen Schätzer ein, Ziel {escape(dest)} — ohne Login.</p>
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
        desc = f"Unabhängiger Leitfaden auf Deutsch: wie du über FansBuy in China kaufst, wie der w2clinks-Katalog funktioniert, wie ein Paket nach {dest} reist."
    elif loc == "it":
        body = f"""
<section class="hero">
  <div class="hero__bg" role="img" aria-label="Homepage ufficiale FansBuy"></div>
  <div class="hero__scrim"></div>
  <div class="wrap">
    <span class="eyebrow">{escape(p["eyebrow"])}</span>
    <h1>{escape(p["hero_h1"])}</h1>
    <p class="lead">{escape(p["lead"])}</p>
    <div class="sbox">
      <form id="w2c-search" action="{escape(sheet)}" method="get" target="_blank" rel="nofollow noopener" role="search">
        <label class="skip" for="q">Cerca prodotti su w2clinks</label>
        <input id="q" name="q" type="search" autocomplete="off" placeholder="Cerca sneakers, hoodie, giacca…">
        <input type="hidden" name="utm_source" value="{escape(p["host"])}">
        <input type="hidden" name="utm_medium" value="referral">
        <input type="hidden" name="utm_campaign" value="hero-buscador">
        <button type="submit">Cerca</button>
      </form>
      <div class="chips">{chips}</div>
    </div>
  </div>
</section>
<section class="sec sec--first" id="agent">
  <div class="wrap"><div class="split"><div>
    <h2>Un agente d’acquisto è un intermediario, non un negozio</h2>
    <p class="lead">FansBuy non vende merce propria. Compra per te nei negozi cinesi che non spediscono all’estero, riceve il pacco in magazzino, lo fotografa, lo conserva e lo spedisce in Italia quando decidi tu.</p>
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
    <p>{escape(_est_note(key))} Fonte: <a href="{escape(p["customs_url"])}" rel="noopener">{escape(p["customs"])}</a>.</p>
    <p><a class="btn" href="{escape(EST)}">Sito ufficiale FansBuy</a>
       <a class="btn btn--ghost" href="{escape(p["ship"])}">Piano spedizione</a></p>
  </div>{fig_est}</div></div>
</section>
<section class="sec" id="volume">
  <div class="wrap"><div class="split split--rev"><div>
    <h2>Il peso che paghi quasi mai è solo la bilancia</h2>
    <p class="lead">Molte linee fatturano il massimo tra bilancia e volume. Un divisore comune è L×W×H (cm) / 8000. Un piumino è leggero e ingombrante: lì decide il volume.</p>
    <p>Esempio: 40×40×3 cm sono 4800 cm³, divisi per 8000 sono 600 g di volume a 200 g reali. Le tue misure le inserisci nello stimatore pubblico, destinazione Italia — senza login.</p>
  </div>{fig_vol}</div></div>
</section>
{restricted}
<section class="sec" id="faq">
  <div class="wrap">
    <h2>Aiuto, notizie e dove chiedere</h2>
    <p class="lead">I dubbi dei primi ordini si ripetono. Stanno su Aiuto — un URL proprio, non un’appendice di questa homepage.</p>
    <p><a class="btn" href="{escape(p["help"])}">Tutte le domande su Aiuto</a>
       <a class="btn btn--ghost" href="{escape(p["news"])}">Check datati su Notizie</a>
       <a class="btn btn--ghost" href="{escape(p["about"])}">Chi siamo</a></p>
  </div>
</section>
"""
        desc = "Guida indipendente in italiano: come compri in Cina con FansBuy, come funziona il catalogo w2clinks, come un pacco arriva in Italia."
    elif loc == "es":
        body = f"""
<section class="hero">
  <div class="hero__bg" role="img" aria-label="Portada oficial de FansBuy"></div>
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
    <p class="lead">FansBuy no vende mercancía propia. Compra por ti en tiendas chinas que no envían al extranjero, recibe el paquete en el almacén, lo fotografía, lo guarda y lo envía a {escape(dest)} cuando tú lo decides.</p>
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
    <p>{escape(_est_note(key))} Fuente: <a href="{escape(p["customs_url"])}" rel="noopener">{escape(p["customs"])}</a>.</p>
    <p><a class="btn" href="{escape(EST)}">Sitio oficial FansBuy</a>
       <a class="btn btn--ghost" href="{escape(p["ship"])}">Plan de envío</a></p>
  </div>{fig_est}</div></div>
</section>
<section class="sec" id="volume">
  <div class="wrap"><div class="split split--rev"><div>
    <h2>El peso que pagas casi nunca es solo la báscula</h2>
    <p class="lead">Muchas líneas facturan el máximo entre báscula y volumen. Un divisor habitual es L×W×H (cm) / 8000. Un plumífero es ligero y voluminoso: ahí decide el volumen.</p>
    <p>Ejemplo: 40×40×3 cm son 4800 cm³, divididos por 8000 son 600 g de volumen con 200 g reales. Tus medidas las metes en el estimador público, destino {escape(dest)} — sin login.</p>
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
        desc = f"Guía independiente en español: cómo compras en China con FansBuy, cómo funciona el catálogo w2clinks, cómo viaja un paquete a {dest}."
    elif loc == "fr":
        body = f"""
<section class="hero">
  <div class="hero__bg" role="img" aria-label="Page d’accueil officielle FansBuy"></div>
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
    <p class="lead">FansBuy ne vend pas de stock propre. Il achète pour toi dans des boutiques chinoises qui n’expédient pas à l’étranger, reçoit le colis en entrepôt, le photographie, le stocke et l’envoie vers {escape(dest)} quand tu le décides.</p>
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
    <p>{escape(_est_note(key))} Source : <a href="{escape(p["customs_url"])}" rel="noopener">{escape(p["customs"])}</a>.</p>
    <p><a class="btn" href="{escape(EST)}">Site officiel FansBuy</a>
       <a class="btn btn--ghost" href="{escape(p["ship"])}">Plan de livraison</a></p>
  </div>{fig_est}</div></div>
</section>
<section class="sec" id="volume">
  <div class="wrap"><div class="split split--rev"><div>
    <h2>Le poids que tu paies n’est presque jamais la balance seule</h2>
    <p class="lead">Beaucoup de lignes facturent le maximum entre balance et volume. Un diviseur courant est L×W×H (cm) / 8000. Une doudoune est légère et volumineuse : c’est le volume qui décide.</p>
    <p>Exemple : 40×40×3 cm font 4800 cm³, divisés par 8000 font 600 g de volume pour 200 g réels. Tes mesures, tu les saisis dans l’estimateur public, destination {escape(dest)} — sans login.</p>
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
        desc = f"Guide indépendant en français : comment tu achètes en Chine via FansBuy, comment marche le catalogue w2clinks, comment un colis voyage vers {dest}."
    elif loc == "nl":
        body = f"""
<section class="hero">
  <div class="hero__bg" role="img" aria-label="Officiële FansBuy-homepage"></div>
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
    <p class="lead">FansBuy verkoopt geen eigen voorraad. Hij koopt voor jou in Chinese shops die niet naar het buitenland sturen, neemt het pakket in het magazijn aan, fotografeert het, slaat het op en stuurt het naar {escape(dest)} als jij dat besluit.</p>
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
    <p>{escape(_est_note(key))} Bron: <a href="{escape(p["customs_url"])}" rel="noopener">{escape(p["customs"])}</a>.</p>
    <p><a class="btn" href="{escape(EST)}">Officiële FansBuy-site</a>
       <a class="btn btn--ghost" href="{escape(p["ship"])}">Verzendplan</a></p>
  </div>{fig_est}</div></div>
</section>
<section class="sec" id="volume">
  <div class="wrap"><div class="split split--rev"><div>
    <h2>Het gewicht dat je betaalt is bijna nooit alleen de weegschaal</h2>
    <p class="lead">Veel lijnen factureren het maximum van weegschaal en volume. Een gebruikelijke deler is L×W×H (cm) / 8000. Een donsjas is licht en volumineus: daar beslist het volume.</p>
    <p>Voorbeeld: 40×40×3 cm is 4800 cm³, gedeeld door 8000 is 600 g volume bij 200 g echt gewicht. Jouw maten vul je in de publieke schatter in, bestemming {escape(dest)} — zonder login.</p>
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
        desc = f"Onafhankelijke gids in het Nederlands: hoe je via FansBuy in China koopt, hoe de w2clinks-catalogus werkt, hoe een pakket naar {dest} reist."
    else:
        body = f"""
<section class="hero">
  <div class="hero__bg" role="img" aria-label="Official FansBuy homepage"></div>
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
    <p class="lead">FansBuy does not sell its own goods. It buys for you in Chinese shops that do not ship abroad, receives the parcel in the warehouse, photographs it, stores it, and ships to {escape(dest)} when you decide.</p>
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
    <p>What you see on w2clinks are cards, not cells. Each fiche has the link FansBuy needs.</p>
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
    <p class="lead">Pick destination <strong>{escape(p["dest_zh"])}</strong> in the public estimator — no login. The delivery address is a {escape(p["postal"])}.</p>
    <p>{escape(_est_note(key))} Import: <a href="{escape(p["customs_url"])}" rel="noopener">{escape(p["customs"])}</a>.</p>
    <p><a class="btn" href="{escape(EST)}">Official FansBuy site</a>
       <a class="btn btn--ghost" href="{escape(p["ship"])}">Shipping plan</a></p>
  </div>{fig_est}</div></div>
</section>
<section class="sec" id="volume">
  <div class="wrap"><div class="split split--rev"><div>
    <h2>The weight you pay is almost never the scale alone</h2>
    <p class="lead">Many lines bill the greater of scale and volume. A common divisor is L×W×H (cm) / 8000. A down jacket is light and bulky: volume decides.</p>
    <p>Example: 40×40×3 cm is 4800 cm³, divided by 8000 is 600 g volume at 200 g real weight. You enter your measurements in the public estimator — no login — destination {escape(p["dest_zh"].split("—")[0].strip())}.</p>
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
            f"Independent English guide: how you buy in China through FansBuy, how the w2clinks catalogue works, how a parcel travels to {dest}."
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
    notes = {"de": CAT_NOTES_DE, "it": CAT_NOTES_IT, "es": CAT_NOTES_ES, "fr": CAT_NOTES_FR, "nl": CAT_NOTES_NL}.get(loc, CAT_NOTES_EN)
    wall = _wall(key, notes)
    s = _shots(key)
    fig_sheet, fig_zoek, fig_diy = s["sheet"], s["zoek"], s["diy"]
    dest = p["dest_label"]
    sheet = _sheet(desk)
    keys = _keys_table(key)
    if loc == "de":
        topic = "was es ist und welche Kategorien du findest"
        body = f"""
<section class="sec sec--first"><div class="wrap"><div class="split"><div>
<span class="eyebrow" style="color:var(--acc)">Der Katalog</span>
<h1>Was FansBuy Spreadsheet ist, und was du darin findest</h1>
<p class="lead">Ein Katalog aus Produktkarten, keine Excel-Datei. Dreiunddreißig Kategorien, Filter, Foto, Marke und der Link für den Agenten.</p>
</div>{fig_sheet}</div></div></section>
<section class="sec sec--tint"><div class="wrap"><div class="split split--rev"><div>
<h2>Warum ein eigener Katalog</h2>
<p>Die Suche eines Agenten gibt den ganzen chinesischen Bestand, riesig und oft auf Chinesisch. Ein Katalog hat die Hausaufgaben schon gemacht: jemand hat gewählt, welche Karten sich lohnen, sie in Kategorien gelegt und den Shop-Link bereitgelegt.</p>
<p>In der Praxis: du findest die Karte auf w2clinks, kopierst den Quellenlink und fügst ihn in die Suche von FansBuy oder ins manuelle Formular ein. Der Katalog kassiert nichts und verkauft nichts.</p>
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
<p class="lead">Die Karte ist der Anfang, nicht die Kasse. Der Schritt, der am häufigsten schiefläuft: du kopierst die Katalog-URL statt des Shop-Links. FansBuy braucht den Taobao-, 1688- oder Weidian-Link.</p>
<p>Klebst du die URL der Katalogkarte selbst, weiß der Agent nicht, was er kaufen soll. Kopiere den Shop-Link, füge ihn in «Goods/shop's link or name» ein, prüfe Preis und Variante, und zahle international erst, wenn die Lagerfotos stimmen.</p>
<p>Liest die Suche den Link nicht, hat die offizielle Site ein manuelles Formular. Karten ohne Preis überspringen — der Quellenlink ist in China oft schon tot.</p>
<p><a class="btn" href="{escape(sheet)}">Katalog auf w2clinks öffnen</a>
   <a class="btn btn--ghost" href="{escape(p["guide"])}">Anleitung Schritt für Schritt</a></p>
</div>{fig_diy}</div></div></section>
"""
    elif loc == "it":
        topic = "cos’è e quali categorie trovi"
        body = f"""
<section class="sec sec--first"><div class="wrap"><div class="split"><div>
<span class="eyebrow" style="color:var(--acc)">Il catalogo</span>
<h1>Che cos’è FansBuy Spreadsheet, e cosa ci trovi</h1>
<p class="lead">Un catalogo di schede prodotto, non un file Excel. Trentatré categorie, filtri, foto, marca e il link per l’agente.</p>
</div>{fig_sheet}</div></div></section>
<section class="sec sec--tint"><div class="wrap"><div class="split split--rev"><div>
<h2>Perché un catalogo a parte</h2>
<p>La ricerca dell’agente restituisce tutto lo stock cinese, enorme e spesso in cinese. Un catalogo ha già fatto il lavoro: qualcuno ha scelto quali schede valgono, le ha messe in categoria e ha pronto il link del negozio.</p>
<p>In pratica: trovi la scheda su w2clinks, copi il link sorgente e lo incolli nella ricerca di FansBuy o nel modulo manuale. Il catalogo non incassa e non vende.</p>
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
<p>Tre categorie con extra: elettronica (spesso litio), occhiali (fragili) e tutto con batteria o magnete. Non ogni linea verso l’Italia li accetta. Controlla il preventivo prima di lasciarli in magazzino.</p>
</div></section>
<section class="sec" id="keys"><div class="wrap">
<h2>Dato scomodo: il catalogo cerca in inglese</h2>
<p class="lead">L’abbiamo verificato termine per termine il {escape(DATE)}. Conviene saperlo prima di digitare la prima ricerca in italiano.</p>
<p>Grafie locali come scarpe, felpa o occhiali danno spesso zero. Le key inglesi sneakers, hoodie, jacket, trousers, bag, glasses o watch danno pagine. Per questo la ricerca in homepage manda key inglesi a w2clinks.</p>
{keys}
</div></section>
<section class="sec sec--tint"><div class="wrap"><div class="split"><div>
<h2>Dal catalogo all’ordine, senza perdere il link</h2>
<p class="lead">La scheda è l’inizio, non la cassa. Il passo che fallisce più spesso: copi l’URL della scheda catalogo invece del link negozio. A FansBuy serve il link Taobao, 1688 o Weidian.</p>
<p>Se incolli l’URL della scheda catalogo, l’agente non sa cosa comprare. Copia il link del negozio, incollalo in «Goods/shop's link or name», controlla prezzo e variante, e paga l’internazionale solo quando le foto di magazzino tornano.</p>
<p>Se la ricerca non legge il link, il sito ufficiale ha un modulo manuale. Schede senza prezzo: saltale — il link sorgente in Cina è spesso già morto.</p>
<p><a class="btn" href="{escape(sheet)}">Apri il catalogo su w2clinks</a>
   <a class="btn btn--ghost" href="{escape(p["guide"])}">Guida passo passo</a></p>
</div>{fig_diy}</div></div></section>
"""
    elif loc == "es":
        topic = "qué es y qué categorías encuentras"
        body = f"""
<section class="sec sec--first"><div class="wrap"><div class="split"><div>
<span class="eyebrow" style="color:var(--acc)">El catálogo</span>
<h1>Qué es FansBuy Spreadsheet, y qué encuentras dentro</h1>
<p class="lead">Un catálogo de fichas de producto, no un archivo Excel. Treinta y tres categorías, filtros, foto, marca y el enlace para el agente.</p>
</div>{fig_sheet}</div></div></section>
<section class="sec sec--tint"><div class="wrap"><div class="split split--rev"><div>
<h2>Por qué un catálogo aparte</h2>
<p>La búsqueda del agente devuelve todo el stock chino, enorme y a menudo en chino. Un catálogo ya hizo el trabajo: alguien eligió qué fichas merecen, las puso en categoría y dejó listo el enlace de la tienda.</p>
<p>En la práctica: encuentras la ficha en w2clinks, copias el enlace de origen y lo pegas en la búsqueda de FansBuy o en el formulario manual. El catálogo no cobra y no vende.</p>
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
<p class="lead">La ficha es el principio, no la caja. El paso que más falla: copias la URL de la ficha del catálogo en vez del enlace de la tienda. FansBuy necesita el enlace Taobao, 1688 o Weidian.</p>
<p>Si pegas la URL de la ficha del catálogo, el agente no sabe qué comprar. Copia el enlace de la tienda, pégalo en «Goods/shop's link or name», revisa precio y variante, y paga el internacional solo cuando las fotos de almacén cuadran.</p>
<p>Si la búsqueda no lee el enlace, el sitio oficial tiene un formulario manual. Fichas sin precio: sáltalas — el enlace de origen en China a menudo ya está muerto.</p>
<p><a class="btn" href="{escape(sheet)}">Abrir el catálogo en w2clinks</a>
   <a class="btn btn--ghost" href="{escape(p["guide"])}">Guía paso a paso</a></p>
</div>{fig_diy}</div></div></section>
"""
    elif loc == "fr":
        topic = "ce que c’est et quelles catégories tu trouves"
        body = f"""
<section class="sec sec--first"><div class="wrap"><div class="split"><div>
<span class="eyebrow" style="color:var(--acc)">Le catalogue</span>
<h1>Ce qu’est FansBuy Spreadsheet, et ce que tu y trouves</h1>
<p class="lead">Un catalogue de fiches produit, pas un fichier Excel. Trente-trois catégories, filtres, photo, marque et le lien pour l’agent.</p>
</div>{fig_sheet}</div></div></section>
<section class="sec sec--tint"><div class="wrap"><div class="split split--rev"><div>
<h2>Pourquoi un catalogue à part</h2>
<p>La recherche de l’agent renvoie tout le stock chinois, énorme et souvent en chinois. Un catalogue a déjà fait le travail : quelqu’un a choisi quelles fiches valent, les a mises en catégorie et a préparé le lien boutique.</p>
<p>En pratique : tu trouves la fiche sur w2clinks, tu copies le lien source et tu le colles dans la recherche FansBuy ou le formulaire manuel. Le catalogue n’encaisse rien et ne vend rien.</p>
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
<p class="lead">La fiche est le début, pas la caisse. L’étape qui rate le plus : tu copies l’URL de la fiche catalogue au lieu du lien boutique. FansBuy a besoin du lien Taobao, 1688 ou Weidian.</p>
<p>Si tu colles l’URL de la fiche catalogue, l’agent ne sait pas quoi acheter. Copie le lien boutique, colle-le dans « Goods/shop's link or name », vérifie prix et variante, et paie l’international seulement quand les photos d’entrepôt collent.</p>
<p>Si la recherche ne lit pas le lien, le site officiel a un formulaire manuel. Fiches sans prix : saute-les — le lien source en Chine est souvent déjà mort.</p>
<p><a class="btn" href="{escape(sheet)}">Ouvrir le catalogue sur w2clinks</a>
   <a class="btn btn--ghost" href="{escape(p["guide"])}">Guide pas à pas</a></p>
</div>{fig_diy}</div></div></section>
"""
    elif loc == "nl":
        topic = "wat het is en welke categorieën je vindt"
        body = f"""
<section class="sec sec--first"><div class="wrap"><div class="split"><div>
<span class="eyebrow" style="color:var(--acc)">De catalogus</span>
<h1>Wat FansBuy Spreadsheet is, en wat je erin vindt</h1>
<p class="lead">Een catalogus van productkaarten, geen Excel-bestand. Drieëndertig categorieën, filters, foto, merk en de link voor de agent.</p>
</div>{fig_sheet}</div></div></section>
<section class="sec sec--tint"><div class="wrap"><div class="split split--rev"><div>
<h2>Waarom een aparte catalogus</h2>
<p>De zoekbalk van een agent geeft de hele Chinese voorraad, enorm en vaak in het Chinees. Een catalogus heeft het huiswerk al gedaan: iemand koos welke kaarten de moeite waard zijn, zette ze in een categorie en legde de shoplink klaar.</p>
<p>In de praktijk: je vindt de kaart op w2clinks, kopieert de bronlink en plakt die in de FansBuy-zoekbalk of het handmatige formulier. De catalogus int niets en verkoopt niets.</p>
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
<p class="lead">De kaart is het begin, niet de kassa. De stap die het vaakst misgaat: je kopieert de catalogus-URL in plaats van de shoplink. FansBuy heeft de Taobao-, 1688- of Weidian-link nodig.</p>
<p>Plak je de URL van de cataloguskaart zelf, dan weet de agent niet wat hij moet kopen. Kopieer de shoplink, plak hem in «Goods/shop's link or name», check prijs en variant, en betaal internationaal pas als de magazijnfoto’s kloppen.</p>
<p>Leest de zoekbalk de link niet, heeft de officiële site een handmatig formulier. Kaarten zonder prijs overslaan — de bronlink is in China vaak al dood.</p>
<p><a class="btn" href="{escape(sheet)}">Catalogus op w2clinks openen</a>
   <a class="btn btn--ghost" href="{escape(p["guide"])}">Handleiding stap voor stap</a></p>
</div>{fig_diy}</div></div></section>
"""
    else:
        topic = "what it is and which categories you will find"
        body = f"""
<section class="sec sec--first"><div class="wrap"><div class="split"><div>
<span class="eyebrow" style="color:var(--acc)">The catalogue</span>
<h1>What FansBuy Spreadsheet is, and what you find in it</h1>
<p class="lead">It is a catalogue of product cards, not an Excel file. Thirty-three categories, filters, and cards with a photo, a brand and the link for the agent.</p>
</div>{fig_sheet}</div></div></section>
<section class="sec sec--tint"><div class="wrap"><div class="split split--rev"><div>
<h2>Why a separate catalogue</h2>
<p>An agent search bar returns the whole stock of Chinese shops, huge and often in Chinese. A catalogue does the homework: someone already picked which fiches are worth it, put them in a category and left the shop link ready.</p>
<p>In practice: you find the fiche on w2clinks, copy the source link and paste it into FansBuy search or the manual form. The catalogue collects no money and sells nothing.</p>
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
<p class="lead">The fiche is the start, not checkout. The step that fails most often is copying the catalogue URL instead of the shop link. FansBuy needs the Taobao, 1688 or Weidian link.</p>
<p>If you paste the catalogue-card URL itself, the agent does not know what to buy. Copy the shop link, paste it into «Goods/shop's link or name», check price and variant, and pay international only after the warehouse photos match.</p>
<p>If search does not read the link, the official site still has a manual form. Skip cards without a price — that source link is often already dead in China.</p>
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
    fig_off = _shots(key)["home"]
    loc = p["loc"]
    if loc == "de":
        topic = "Hilfe und häufige Fragen"
        body = f"""
<article class="pw">
  <span class="eyebrow" style="color:var(--acd)">Hilfe</span>
  <h1>Hilfe und Fragen zu FansBuy in {escape(p["dest_label"])}</h1>
  <p class="lead">Fragen erster Bestellungen. Die Lieferadresse ist eine {escape(p["postal"])}.</p>
  {fig_off}{html_f}
  <p><a class="btn" href="{escape(EST)}">Offizielle FansBuy-Site</a>
     <a class="btn btn--ghost" href="{escape(p["ship"])}">Versandplan</a></p>
</article>
"""
    elif loc == "it":
        topic = "aiuto e domande frequenti"
        body = f"""
<article class="pw">
  <span class="eyebrow" style="color:var(--acd)">Aiuto</span>
  <h1>Aiuto e domande su FansBuy in Italia</h1>
  <p class="lead">Domande dei primi ordini. L’indirizzo è una {escape(p["postal"])}.</p>
  {fig_off}{html_f}
  <p><a class="btn" href="{escape(EST)}">Sito ufficiale FansBuy</a>
     <a class="btn btn--ghost" href="{escape(p["ship"])}">Piano spedizione</a></p>
</article>
"""
    elif loc == "es":
        topic = "ayuda y preguntas frecuentes"
        body = f"""
<article class="pw">
  <span class="eyebrow" style="color:var(--acd)">Ayuda</span>
  <h1>Ayuda y preguntas sobre FansBuy en {escape(p["dest_label"])}</h1>
  <p class="lead">Preguntas de los primeros pedidos. La dirección es una {escape(p["postal"])}.</p>
  {fig_off}{html_f}
  <p><a class="btn" href="{escape(EST)}">Sitio oficial FansBuy</a>
     <a class="btn btn--ghost" href="{escape(p["ship"])}">Plan de envío</a></p>
</article>
"""
    elif loc == "fr":
        topic = "aide et questions fréquentes"
        body = f"""
<article class="pw">
  <span class="eyebrow" style="color:var(--acd)">Aide</span>
  <h1>Aide et questions sur FansBuy depuis {escape(p["dest_label"])}</h1>
  <p class="lead">Questions des premières commandes. L’adresse est une {escape(p["postal"])}.</p>
  {fig_off}{html_f}
  <p><a class="btn" href="{escape(EST)}">Site officiel FansBuy</a>
     <a class="btn btn--ghost" href="{escape(p["ship"])}">Plan de livraison</a></p>
</article>
"""
    elif loc == "nl":
        topic = "hulp en veelgestelde vragen"
        body = f"""
<article class="pw">
  <span class="eyebrow" style="color:var(--acd)">Hulp</span>
  <h1>Hulp en vragen over FansBuy in {escape(p["dest_label"])}</h1>
  <p class="lead">Vragen van eerste bestellingen. Het afleveradres is een {escape(p["postal"])}.</p>
  {fig_off}{html_f}
  <p><a class="btn" href="{escape(EST)}">Officiële FansBuy-site</a>
     <a class="btn btn--ghost" href="{escape(p["ship"])}">Verzendplan</a></p>
</article>
"""
    else:
        topic = "help and frequently asked questions"
        body = f"""
<article class="pw">
  <span class="eyebrow" style="color:var(--acd)">Help</span>
  <h1>Help and questions about FansBuy in {escape(p["dest_label"])}</h1>
  <p class="lead">Questions that come back on first orders. The delivery address uses a {escape(p["postal"])}.</p>
  {fig_off}{html_f}
  <p><a class="btn" href="{escape(EST)}">Official FansBuy site</a>
     <a class="btn btn--ghost" href="{escape(p["ship"])}">Shipping plan</a></p>
</article>
"""
    return cms_shell(
        desk, page_title(desk, topic),
        f"FAQ about FansBuy from {p['dest_label']}.",
        f"https://{p['host']}{p['help']}", [faq_ld(p["lang"], pairs)], body, p["help"],
    )


def build_news(key: str) -> str:
    p = PACKS[key]
    desk = desk_for(key)
    loc = p["loc"]
    if loc == "de":
        items = [
            ("Erste Runde: öffentlicher Schätzer",
             _est_note(key),
             f"Am Versandmorgen die offizielle Site öffnen, Ziel {p['dest_zh']}. {p['postal']}."),
            ("w2clinks sucht auf Englisch",
             "sneakers, hoodie, jacket liefern Seiten; Turnschuhe oft null. Gemessen 6 Oct 2026.",
             "Englischen Key tippen oder einen Chip auf der Homepage antippen."),
            ("Volumengewicht",
             "Viele Linien nehmen das Maximum aus Waage und L×B×H/8000. Kein SKU-Preis in diesem HTML.",
             "Deine Box im öffentlichen Schätzer rechnen — ohne Login."),
            ("Schwester-Hosts bleiben getrennt",
             "UK, US, DE, AT, ES, FR, IT und NL sind eigene Dateien. Kein 301 untereinander.",
             "Es gibt keinen FansBuy-Hub und kein Zollgebiet, das diese Dest-Hosts zusammenzieht."),
        ]
        h1, topic, brow = "Was wir auf der Plattform geprüft haben, mit Datum", "was wir auf der Plattform geprüft haben", "News"
        lead = "Das ist kein Firmennewsletter. Eigene Checks, mit Datum."
    elif loc == "it":
        items = [
            ("Primo giro: preventivo ufficiale",
             f"Il {DATE} https://fansbuy.com/estimates è lo strumento live. Nessuna linea inventata.",
             "La mattina della spedizione apri il sito ufficiale, destinazione Italy — 意大利, CAP italiano / Poste Italiane."),
            ("w2clinks cerca in inglese",
             "sneakers, hoodie, jacket danno pagine; grafie locali spesso zero. Misurato 6 Oct 2026.",
             "Scrivi la key inglese, o tocca un chip in homepage."),
            ("Peso volumetrico",
             "Molte linee prendono il massimo tra bilancia e L×W×H/8000. Nessun prezzo SKU in questo HTML.",
             "Calcola la tua scatola nello stimatore pubblico, senza login."),
            ("Gli host sorella restano separati",
             "UK, US, DE, AT, ES, FR, IT e NL sono file distinti. Nessun 301 fra loro.",
             "Non c’è un hub FansBuy né un territorio doganale che unisca questi host."),
        ]
        h1, topic, brow = "Cosa abbiamo verificato sulla piattaforma, con data", "cosa abbiamo verificato sulla piattaforma", "Notizie"
        lead = "Non è una newsletter aziendale. Check nostri, con data."
    elif loc == "es":
        items = [
            ("Primera ronda: estimador oficial",
             f"El {DATE} https://fansbuy.com/estimates es la tarifa en vivo. Ninguna línea inventada.",
             f"La mañana del envío abre el sitio oficial, destino {p['dest_zh']}. {p['postal']}."),
            ("w2clinks busca en inglés",
             "sneakers, hoodie, jacket dan páginas; grafías locales a menudo cero. Medido 6 Oct 2026.",
             "Escribe la key inglesa, o toca un chip en la portada."),
            ("Peso volumétrico",
             "Muchas líneas toman el máximo entre báscula y L×W×H/8000. Ningún precio SKU en este HTML.",
             "Calcula tu caja en el estimador público, sin login."),
            ("Los hosts hermanos siguen separados",
             "UK, US, DE, AT, ES, FR, IT y NL son archivos distintos. Ningún 301 entre ellos.",
             "No hay un hub FansBuy ni un territorio aduanero que una estos hosts."),
        ]
        h1, topic, brow = "Qué hemos comprobado en la plataforma, con fecha", "qué hemos comprobado en la plataforma", "Noticias"
        lead = "No es un boletín de empresa. Checks nuestros, con fecha."
    elif loc == "fr":
        items = [
            ("Premier tour : estimateur officiel",
             f"Le {DATE} https://fansbuy.com/estimates est l’outil live. Aucune ligne inventée.",
             f"Le matin de l’envoi, ouvre le site officiel, destination {p['dest_zh']}. {p['postal']}."),
            ("w2clinks cherche en anglais",
             "sneakers, hoodie, jacket donnent des pages ; les graphies locales souvent zéro. Mesuré 6 Oct 2026.",
             "Tape la key anglaise, ou touche un chip sur la page d’accueil."),
            ("Poids volumétrique",
             "Beaucoup de lignes prennent le max entre balance et L×W×H/8000. Aucun prix SKU dans cet HTML.",
             "Calcule ta boîte dans l’estimateur public, sans login."),
            ("Les hôtes sœurs restent séparés",
             "UK, US, DE, AT, ES, FR, IT et NL sont des fichiers distincts. Aucun 301 entre eux.",
             "Il n’y a pas de hub FansBuy ni de territoire douanier qui rassemble ces hôtes."),
        ]
        h1, topic, brow = "Ce que nous avons vérifié sur la plateforme, avec une date", "ce que nous avons vérifié sur la plateforme", "Actus"
        lead = "Ce n’est pas une newsletter d’entreprise. Des checks à nous, avec une date."
    elif loc == "nl":
        items = [
            ("Eerste ronde: officiële schatter",
             f"Op {DATE} levert https://fansbuy.com/estimates live cijfers. Geen verzonnen lijn.",
             f"Open de officiële site de ochtend dat je verzendt, bestemming {p['dest_zh']}. {p['postal']}."),
            ("w2clinks zoekt in het Engels",
             "sneakers, hoodie, jacket geven pagina’s; lokale spellingen vaak nul. Gemeten 6 Oct 2026.",
             "Typ de Engelse key, of tik een chip op de homepage."),
            ("Volumgewicht",
             "Veel lijnen nemen het maximum van weegschaal en L×W×H/8000. Geen SKU-prijs in deze HTML.",
             "Reken je doos in de publieke schatter, zonder login."),
            ("Zusthosts blijven apart",
             "UK, US, DE, AT, ES, FR, IT en NL zijn eigen bestanden. Geen 301 onderling.",
             "Er is geen FansBuy-hub en geen douanegebied dat deze hosts samenvoegt."),
        ]
        h1, topic, brow = "Wat we op het platform hebben nagekeken, met datum", "wat we op het platform hebben nagekeken", "Nieuws"
        lead = "Dit is geen bedrijfsnieuwsbrief. Eigen checks, met datum."
    else:
        items = [
            (f"First round: official estimator {EST_PATH}",
             f"On {DATE} {EST} is the live rate tool. This guide does not invent a line or an amount.",
             f"Open the official site the morning you ship. Destination {p['dest_zh']}. {p['postal']}."),
            ("The w2clinks catalogue searches in English",
             "sneakers, hoodie and jacket returned pages; local spellings often returned zero. Measured 6 Oct 2026.",
             "Type the English key, or tap a chip on the homepage."),
            ("Volume weight",
             "Many lines bill the greater of scale and L×W×H/8000. No SKU price in this HTML.",
             "Run your box on the public estimator — no login."),
            ("Sister country hosts stay separate",
             "UK, US, Germany, Austria, Spain, France, Italy and the Netherlands on FansBuy stay on their own hosts. None of them 301 into each other.",
             "There is no FansBuy hub and no customs territory that folds these dest hosts together."),
        ]
        h1, topic, brow = "What we checked on the platform, with a date", "what we checked on the platform", "News"
        lead = "This is not a company newsletter. These are our own checks, with a date."
    ld = itemlist_ld(
        url=f"https://{p['host']}{p['news']}",
        name="FansBuy dest checks",
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
        desk, page_title(desk, topic), "Dated checks on FansBuy.",
        f"https://{p['host']}{p['news']}", [ld], body, p["news"],
    )


def build_about(key: str) -> str:
    p = PACKS[key]
    desk = desk_for(key)
    fig_off = _shots(key)["home"]
    loc = p["loc"]
    if loc == "de":
        topic = "wer wir sind und wie du uns erreichst"
        body = f"""
<article class="pw">
  <span class="eyebrow" style="color:var(--acd)">Über uns</span>
  <h1>Eine unabhängige Site über FansBuy, auf Deutsch</h1>
  <p class="lead">FansBuy Spreadsheet ist nicht FansBuy. Es ist ein redaktioneller Leitfaden. Bestellungen nur auf fansbuy.com. Dieser Desk ist unabhängig — kein Hub, keine Zusammenlegung mit anderen Ländersites.</p>
  {fig_off}
  <h2>Kontakt</h2>
  <p>Bestellungen: offizielle Site. Dieser Leitfaden: <a href="mailto:{escape(MAIL)}">{escape(MAIL)}</a>.</p>
</article>
"""
    elif loc == "it":
        topic = "chi siamo e come raggiungerci"
        body = f"""
<article class="pw">
  <span class="eyebrow" style="color:var(--acd)">Chi siamo</span>
  <h1>Un sito indipendente su FansBuy, in italiano</h1>
  <p class="lead">FansBuy Spreadsheet non è FansBuy. È una guida editoriale. Ordini solo su fansbuy.com. Questo dest è indipendente — nessun hub, nessuna fusione con altri host di paese.</p>
  {fig_off}
  <h2>Contatto</h2>
  <p>Ordini: sito ufficiale. Questa guida: <a href="mailto:{escape(MAIL)}">{escape(MAIL)}</a>.</p>
</article>
"""
    elif loc == "es":
        topic = "quiénes somos y cómo contactarnos"
        body = f"""
<article class="pw">
  <span class="eyebrow" style="color:var(--acd)">Sobre nosotros</span>
  <h1>Un sitio independiente sobre FansBuy, en español</h1>
  <p class="lead">FansBuy Spreadsheet no es FansBuy. Es una guía editorial. Pedidos solo en fansbuy.com. Este dest es independiente — ningún hub, ninguna fusión con otros hosts de país.</p>
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
  <h1>Un site indépendant sur FansBuy, en français</h1>
  <p class="lead">FansBuy Spreadsheet n’est pas FansBuy. C’est un guide éditorial. Commandes uniquement sur fansbuy.com. Ce dest est indépendant — pas de hub, pas de fusion avec d’autres hôtes pays.</p>
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
  <h1>Een onafhankelijke site over FansBuy, in het Nederlands</h1>
  <p class="lead">FansBuy Spreadsheet is FansBuy niet. Het is een redactionele gids. Bestellingen alleen op fansbuy.com. Dit dest is onafhankelijk — geen hub, geen samenvoeging met andere landhosts.</p>
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
  <h1>An independent site about FansBuy, in English</h1>
  <p class="lead">FansBuy Spreadsheet is not FansBuy. It is an editorial guide. Orders only on fansbuy.com. This dest is independent — no hub, no merge with other country hosts.</p>
  {fig_off}
  <h2>How we work</h2>
  <p>Shipping figures come from {escape(EST)}. This desk publishes no invented rate. Import points to <a href="{escape(p["customs_url"])}" rel="noopener">{escape(p["customs"])}</a>.</p>
  <h2>Contact</h2>
  <p>Orders: official FansBuy chat. This guide: <a href="mailto:{escape(MAIL)}">{escape(MAIL)}</a>.</p>
</article>
"""
    return cms_shell(
        desk, page_title(desk, topic),
        "Independent FansBuy guide: how we check facts.",
        f"https://{p['host']}{p['about']}", [], body, p["about"],
    )


def _inner_pages(key: str) -> dict[str, tuple[str, str, str]]:
    """href, topic, html-body for dest-local ranked inners (not FansBuy leftovers)."""
    p = PACKS[key]
    dest = p["dest_label"]
    loc = p["loc"]
    s = _shots(key)
    fig_off, fig_sheet, fig_vol, fig_diy = s["home"], s["sheet"], s["vol"], s["diy"]
    fig_est, fig_pay = s["est"], s["pay"]
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
    lab_not = escape(p.get("lab_not", "nicht EU" if loc == "de" else "not EU"))

    if loc == "de":
        addr_note = (
            "Packstation zählt, wenn die gewählte Linie sie akzeptiert — das steht auf der offiziellen Sendung, nicht hier."
            if p["dest"] == "DE"
            else "Eine österreichische PLZ (z. B. 1010 Wien) ist kein deutsches Abholautomaten-Muster."
        )
        guide_topic = f"wie du die erste Bestellung aus {dest} aufgibst"
        guide_body = f"""
<article class="pw">
  <span class="eyebrow" style="color:var(--acd)">Anleitung</span>
  <h1>Erste Bestellung bei FansBuy, von {dest_e} aus</h1>
  <p class="lead">Link kopieren, in den Agenten einfügen, Lagerfoto prüfen, bündeln, Ziel {dest_zh} wählen. Die Lieferadresse ist eine {fp}.</p>
  {fig_off}
  <h2>1. Karte auf w2clinks öffnen</h2>
  <p>Eine der dreiunddreißig Kategorien, Foto und Shop-Link. Das ist der Katalog, keine Excel-Datei.</p>
  {fig_sheet}
  <h2>2. Auf der offiziellen Site einfügen</h2>
  <p>Zahlung und Tickets bleiben auf {official}. Dieser Desk sieht dein Konto nicht. Liest die Suche den Link nicht, hat die offizielle Site ein manuelles Formular.</p>
  {fig_diy}
  <h2>3. Foto, dann bündeln, dann senden</h2>
  <p>Der öffentliche Schätzer unter /estimates braucht kein Login. DIY Order schon. Keine erfundene Lagerfrist, keine erfundene Linie.</p>
  <h2>Neun Status, drei Bildschirme</h2>
  <p>Zuerst Produkt plus Inlandsweg bis zum Lager. International später. «Warum steht es still?» heißt fast immer: falscher Bildschirm — Bestellungen, dann Lager, dann Paket.</p>
  {_guide_extra(key, fig_pay, fig_est)}
  <h2>Erste Haul: flach zuerst</h2>
  <p>T-Shirts, Shorts, Schmuck für die erste Runde. Daune, Taschen, Mützen für die zweite. Elektronik oft Lithium: Linie auf der offiziellen Site prüfen.</p>
  <p><a class="btn" href="{guide}">Anleitung</a> <a class="btn btn--ghost" href="{ship}">Versandplan</a></p>
</article>
"""
        ship_topic = f"Versand und Zoll aus {dest}"
        ship_body = f"""
<article class="pw">
  <span class="eyebrow" style="color:var(--acd)">Versand</span>
  <h1>Versand nach {dest_e}: Schätzer, Volumen, Zoll</h1>
  <p class="lead">Ziel {dest_zh}, {lab_not}. Die Lieferadresse ist eine {fp}.</p>
  {fig_off}
  <h2>Der offizielle Schätzer entscheidet</h2>
  <p>{escape(_est_note(key))} Quelle: <a href="{customs_url}" rel="noopener">{customs}</a>.</p>
  {fig_est}
  <h2>Waage gegen Volumen</h2>
  <p>Viele Linien rechnen das Maximum aus Waage und L×B×H (cm) / 8000. Beispiel: 40×40×3 cm sind 4800 cm³, geteilt durch 8000 sind 600 g Volumen bei 200 g Echtgewicht. Kein SKU-Preis in diesem HTML.</p>
  {fig_vol}
  <h2>Bündeln ist kein Zolltrick auf dieser Seite</h2>
  <p>Mehrere Lagerpositionen in einem Karton können Gebühren sparen. Was du dem Zoll angibst, steht in der offiziellen Sendung, nicht auf dieser Seite.</p>
  <h2>Restricted ist keine Zollnachricht</h2>
  <p>Karten ohne Preis oder ein manuelles Formular heißen: der Quellenlink ist über den Agenten nicht kaufbar. Tabak, Alkohol und Arzneimittel reisen nicht.</p>
  <h2>Lagerfotos vor der Linie</h2>
  <p>QC-Fotos landen in der App, sobald das Stück im Lager ist. Extra-Winkel sind oft kostenpflichtig. Reklamieren ist einfacher, solange es noch im Lager liegt.</p>
  <h2>Die Adresse auf diesem Dest</h2>
  <p>Die Lieferadresse ist eine {fp}. {addr_note}</p>
  <p><a class="btn" href="{est}">Offizielle FansBuy-Site</a> <a class="btn btn--ghost" href="{help_h}">Hilfe</a></p>
</article>
"""
        legit_topic = f"ist FansBuy ein echter Agent aus {dest}"
        legit_body = f"""
<article class="pw">
  <span class="eyebrow" style="color:var(--acd)">Check</span>
  <h1>Ist FansBuy ein echter Einkaufsagent?</h1>
  <p class="lead">fansbuy.com ist das offizielle Produkt. Dieser Desk ist unabhängig — kein Hub. Dieser Dest ist nicht FansBuy.</p>
  {fig_off}
  <p>{escape(_est_note(key))} Bestellungen nur über {official}.</p>
  <p>Die Lieferadresse auf diesem Dest ist eine {fp}.</p>
  <p><a class="btn" href="{guide}">Anleitung</a> <a class="btn btn--ghost" href="{help_h}">Hilfe</a></p>
</article>
"""
        coup_topic = "Gutscheine stehen auf der offiziellen Site"
        coup_body = f"""
<article class="pw">
  <span class="eyebrow" style="color:var(--acd)">Codes</span>
  <h1>Gutscheine: nicht im Titel dieses Dest</h1>
  <p class="lead">Dieser Dest druckt keine Einladungscodes in Titel oder Homepage. Wenn FansBuy einen Code veröffentlicht, steht er nach dem Login auf {official}.</p>
  {fig_off}
  <p>Die Lieferadresse bleibt eine {fp}. Ziel im Schätzer: {dest_zh}.</p>
  <p><a class="btn" href="{official}">Offizielle Site</a> <a class="btn btn--ghost" href="{catalog}">Katalog</a></p>
</article>
"""
        sheet_topic = f"der Katalog und wie du ihn von {dest} aus nutzt"
        sheet_body = f"""
<article class="pw">
  <span class="eyebrow" style="color:var(--acd)">Spreadsheet</span>
  <h1>FansBuy Spreadsheet ist ein Katalog, keine Tabelle</h1>
  <p class="lead">Karten mit Foto, Marke und Shop-Link. Dreiunddreißig Kategorien wie auf w2clinks.</p>
  {fig_sheet}
  <p>Suche auf Englisch (sneakers, hoodie, jacket). Die Lieferadresse auf diesem Dest ist eine {fp}.</p>
  <p><a class="btn" href="{catalog}">Katalog öffnen</a> <a class="btn btn--ghost" href="{guide}">Anleitung</a></p>
</article>
"""
    elif loc == "it":
        guide_topic = "come fai il primo ordine dall’Italia"
        guide_body = f"""
<article class="pw">
  <span class="eyebrow" style="color:var(--acd)">Guida</span>
  <h1>Primo ordine FansBuy, dall’Italia</h1>
  <p class="lead">Copi il link, lo incolli nell’agente, controlli la foto di magazzino, consolidi, scegli destinazione {dest_zh}. L’indirizzo è una {fp}.</p>
  {fig_off}
  <h2>1. Apri una scheda su w2clinks</h2>
  <p>Una delle trentatré categorie, foto e link del negozio. È un catalogo, non un file Excel.</p>
  {fig_sheet}
  <h2>2. Incolla sul sito ufficiale</h2>
  <p>Pagamenti e ticket restano su {official}. Questa guida non vede il tuo account. La barra pubblica è «Goods/shop's link or name». La barra pubblica è «Goods/shop's link or name».</p>
  {fig_diy}
  <h2>3. Foto, poi consolida, poi spedisci</h2>
  <p>Il {escape(DATE)} il preventivo pubblico è lo strumento live. Nessuna giacenza inventata, nessuna linea inventata.</p>
  <h2>Nove stati, tre schermate</h2>
  <p>Prima il prodotto più il trasporto interno fino al magazzino. L’internazionale dopo. «Perché è fermo?» quasi sempre: schermata sbagliata — ordini, poi magazzino, poi pacco.</p>
  {_guide_extra(key, fig_pay, fig_est)}
  <h2>Primo haul: piatto prima</h2>
  <p>T-shirt, shorts, gioielli per il primo giro. Piumini, borse, cappelli per il secondo. Elettronica spesso litio: controlla la linea sul sito ufficiale.</p>
  <p><a class="btn" href="{guide}">Guida</a> <a class="btn btn--ghost" href="{ship}">Piano spedizione</a></p>
</article>
"""
        ship_topic = "spedizione e dogana dall’Italia"
        ship_body = f"""
<article class="pw">
  <span class="eyebrow" style="color:var(--acd)">Spedizione</span>
  <h1>Spedire in Italia: preventivo, volume, dogana</h1>
  <p class="lead">Destinazione {dest_zh}, non EU. L’indirizzo è una {fp}.</p>
  {fig_off}
  <h2>Il preventivo ufficiale decide</h2>
  <p>{escape(_est_note(key))} Fonte: <a href="{customs_url}" rel="noopener">{customs}</a>.</p>
  {fig_est}
  <h2>Bilancia contro volume</h2>
  <p>Molte linee fatturano il massimo tra bilancia e L×W×H (cm) / 8000. Esempio: 40×40×3 cm sono 4800 cm³, divisi per 8000 sono 600 g di volume a 200 g reali. Nessun prezzo SKU in questo HTML.</p>
  {fig_vol}
  <h2>Consolidare non è una guida doganale</h2>
  <p>Più pezzi in un cartone possono ridurre le riga di nolo. Cosa dichiari in dogana sta sulla spedizione ufficiale, non in questa pagina.</p>
  <h2>Restricted non è un avviso di dogana</h2>
  <p>Schede senza prezzo o un modulo manuale significano: il link sorgente non è acquistabile tramite l’agente. Tabacco, alcol e farmaci non viaggiano.</p>
  <h2>Foto di magazzino prima della linea</h2>
  <p>Le foto QC arrivano in app quando il pezzo è in magazzino. Angoli extra spesso a pagamento. Reclami più facili finché sta ancora lì.</p>
  <h2>L’indirizzo su questo dest</h2>
  <p>L’indirizzo è una {fp}. Poste Italiane conta se la linea scelta la accetta — sta sulla spedizione ufficiale, non qui.</p>
  <p><a class="btn" href="{est}">Sito ufficiale FansBuy</a> <a class="btn btn--ghost" href="{help_h}">Aiuto</a></p>
</article>
"""
        legit_topic = "FansBuy è un agente vero dall’Italia"
        legit_body = f"""
<article class="pw">
  <span class="eyebrow" style="color:var(--acd)">Check</span>
  <h1>FansBuy è un agente d’acquisto vero?</h1>
  <p class="lead">fansbuy.com è il prodotto ufficiale. Questo dest è indipendente — nessun hub. Questo dest non è FansBuy.</p>
  {fig_off}
  <p>Il {escape(DATE)} il preventivo ufficiale è lo strumento live. Per questo non inventiamo giacenza né tariffa. Ordini solo su {official}.</p>
  <p>L’indirizzo su questo dest è una {fp}.</p>
  <p><a class="btn" href="{guide}">Guida</a> <a class="btn btn--ghost" href="{help_h}">Aiuto</a></p>
</article>
"""
        coup_topic = "i coupon stanno sul sito ufficiale"
        coup_body = f"""
<article class="pw">
  <span class="eyebrow" style="color:var(--acd)">Codici</span>
  <h1>Coupon: non nel titolo di questo dest</h1>
  <p class="lead">Questo dest non stampa codici invito nel titolo o in homepage. Se FansBuy pubblica un codice, sta dopo il login su {official}.</p>
  {fig_off}
  <p>L’indirizzo resta una {fp}. Destinazione nel preventivo: {dest_zh}.</p>
  <p><a class="btn" href="{official}">Sito ufficiale</a> <a class="btn btn--ghost" href="{catalog}">Catalogo</a></p>
</article>
"""
        sheet_topic = "il catalogo e come lo usi dall’Italia"
        sheet_body = f"""
<article class="pw">
  <span class="eyebrow" style="color:var(--acd)">Spreadsheet</span>
  <h1>FansBuy Spreadsheet è un catalogo, non una griglia</h1>
  <p class="lead">Schede con foto, marca e link negozio. Trentatré categorie come su w2clinks.</p>
  {fig_sheet}
  <p>Cerca in inglese (sneakers, hoodie, jacket). L’indirizzo su questo dest è una {fp}.</p>
  <p><a class="btn" href="{catalog}">Apri il catalogo</a> <a class="btn btn--ghost" href="{guide}">Guida</a></p>
</article>
"""
    elif loc == "es":
        guide_topic = f"cómo haces el primer pedido desde {dest}"
        guide_body = f"""
<article class="pw">
  <span class="eyebrow" style="color:var(--acd)">Guía</span>
  <h1>Primer pedido FansBuy, desde {dest_e}</h1>
  <p class="lead">Copias el enlace, lo pegas en el agente, revisas la foto de almacén, consolidas, eliges destino {dest_zh}. La dirección es una {fp}.</p>
  {fig_off}
  <h2>1. Abre una ficha en w2clinks</h2>
  <p>Una de las treinta y tres categorías, foto y enlace de tienda. Es un catálogo, no un archivo Excel.</p>
  {fig_sheet}
  <h2>2. Pégalo en el sitio oficial</h2>
  <p>Pagos y tickets siguen en {official}. Esta guía no ve tu cuenta. La barra pública es «Goods/shop's link or name». La barra pública es «Goods/shop's link or name».</p>
  {fig_diy}
  <h2>3. Foto, luego consolida, luego envía</h2>
  <p>El {escape(DATE)} el estimador público es la tarifa en vivo. Ningún plazo de almacén inventado, ninguna línea inventada.</p>
  <h2>Nueve estados, tres pantallas</h2>
  <p>Primero el producto más el tramo interno hasta el almacén. El internacional después. «¿Por qué está parado?» casi siempre: pantalla equivocada — pedidos, luego almacén, luego paquete.</p>
  {_guide_extra(key, fig_pay, fig_est)}
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
  <h2>El estimador oficial decide</h2>
  <p>{escape(_est_note(key))} Fuente: <a href="{customs_url}" rel="noopener">{customs}</a>.</p>
  {fig_est}
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
  <p><a class="btn" href="{est}">Sitio oficial FansBuy</a> <a class="btn btn--ghost" href="{help_h}">Ayuda</a></p>
</article>
"""
        legit_topic = f"FansBuy es un agente de verdad desde {dest}"
        legit_body = f"""
<article class="pw">
  <span class="eyebrow" style="color:var(--acd)">Check</span>
  <h1>¿FansBuy es un agente de compras de verdad?</h1>
  <p class="lead">fansbuy.com es el producto oficial. Este dest es independiente — ningún hub. Este dest no es FansBuy.</p>
  {fig_off}
  <p>El {escape(DATE)} el estimador oficial es la tarifa en vivo. Por eso no inventamos plazo de almacén ni tarifa. Pedidos solo en {official}.</p>
  <p>La dirección en este dest es una {fp}.</p>
  <p><a class="btn" href="{guide}">Guía</a> <a class="btn btn--ghost" href="{help_h}">Ayuda</a></p>
</article>
"""
        coup_topic = "los cupones están en el sitio oficial"
        coup_body = f"""
<article class="pw">
  <span class="eyebrow" style="color:var(--acd)">Códigos</span>
  <h1>Cupones: no en el título de este dest</h1>
  <p class="lead">Este dest no imprime códigos de invitación en el título ni en la portada. Si FansBuy publica un código, está después del login en {official}.</p>
  {fig_off}
  <p>La dirección sigue siendo una {fp}. Destino en el estimador: {dest_zh}.</p>
  <p><a class="btn" href="{official}">Sitio oficial</a> <a class="btn btn--ghost" href="{catalog}">Catálogo</a></p>
</article>
"""
        sheet_topic = f"el catálogo y cómo lo usas desde {dest}"
        sheet_body = f"""
<article class="pw">
  <span class="eyebrow" style="color:var(--acd)">Spreadsheet</span>
  <h1>FansBuy Spreadsheet es un catálogo, no una tabla</h1>
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
  <h1>Première commande FansBuy, depuis {dest_e}</h1>
  <p class="lead">Tu copies le lien, tu le colles dans l’agent, tu vérifies la photo d’entrepôt, tu regroupes, tu choisis destination {dest_zh}. L’adresse est une {fp}.</p>
  {fig_off}
  <h2>1. Ouvre une fiche sur w2clinks</h2>
  <p>Une des trente-trois catégories, photo et lien boutique. C’est un catalogue, pas un fichier Excel.</p>
  {fig_sheet}
  <h2>2. Colle-le sur le site officiel</h2>
  <p>Paiements et tickets restent sur {official}. Ce guide ne voit pas ton compte. La barre publique est « Goods/shop's link or name ». La barre publique est «Goods/shop's link or name».</p>
  {fig_diy}
  <h2>3. Photo, puis regrouper, puis envoyer</h2>
  <p>Le {escape(DATE)} l’estimateur public est l’outil live. Aucun délai de stockage inventé, aucune ligne inventée.</p>
  <h2>Neuf statuts, trois écrans</h2>
  <p>D’abord le produit plus le trajet intérieur jusqu’à l’entrepôt. L’international après. « Pourquoi c’est bloqué ? » presque toujours : mauvais écran — commandes, puis entrepôt, puis colis.</p>
  {_guide_extra(key, fig_pay, fig_est)}
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
  <h2>L’estimateur officiel décide</h2>
  <p>{escape(_est_note(key))} Source : <a href="{customs_url}" rel="noopener">{customs}</a>.</p>
  {fig_est}
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
  <p><a class="btn" href="{est}">Site officiel FansBuy</a> <a class="btn btn--ghost" href="{help_h}">Aide</a></p>
</article>
"""
        legit_topic = f"FansBuy est un vrai agent depuis {dest}"
        legit_body = f"""
<article class="pw">
  <span class="eyebrow" style="color:var(--acd)">Check</span>
  <h1>FansBuy est-il un vrai agent d’achat ?</h1>
  <p class="lead">fansbuy.com est le produit officiel. Ce dest est indépendant — pas de hub. Ce dest n’est pas FansBuy.</p>
  {fig_off}
  <p>Le {escape(DATE)} l’estimateur officiel est l’outil live. C’est pour ça qu’on n’invente ni délai de stockage ni tarif. Commandes seulement sur {official}.</p>
  <p>L’adresse sur ce dest est une {fp}.</p>
  <p><a class="btn" href="{guide}">Guide</a> <a class="btn btn--ghost" href="{help_h}">Aide</a></p>
</article>
"""
        coup_topic = "les codes sont sur le site officiel"
        coup_body = f"""
<article class="pw">
  <span class="eyebrow" style="color:var(--acd)">Codes</span>
  <h1>Codes : pas dans le titre de ce dest</h1>
  <p class="lead">Ce dest n’imprime pas de codes d’invitation dans le titre ni sur la page d’accueil. Si FansBuy publie un code, il est après le login sur {official}.</p>
  {fig_off}
  <p>L’adresse reste une {fp}. Destination dans l’estimateur : {dest_zh}.</p>
  <p><a class="btn" href="{official}">Site officiel</a> <a class="btn btn--ghost" href="{catalog}">Catalogue</a></p>
</article>
"""
        sheet_topic = f"le catalogue et comment tu l’utilises depuis {dest}"
        sheet_body = f"""
<article class="pw">
  <span class="eyebrow" style="color:var(--acd)">Spreadsheet</span>
  <h1>FansBuy Spreadsheet est un catalogue, pas une grille</h1>
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
  <h1>Eerste FansBuy-bestelling, vanuit {dest_e}</h1>
  <p class="lead">Link kopiëren, in de agent plakken, magazijnfoto checken, bundelen, bestemming {dest_zh} kiezen. Het afleveradres is een {fp}.</p>
  {fig_off}
  <h2>1. Open een kaart op w2clinks</h2>
  <p>Eén van de drieëndertig categorieën, foto en shoplink. Dat is de catalogus, geen Excel-bestand.</p>
  {fig_sheet}
  <h2>2. Plak op de officiële site</h2>
  <p>Betaling en tickets blijven op {official}. Deze gids ziet je account niet. De publieke plakbalk heet «Goods/shop's link or name». De publieke plakbalk heet «Goods/shop's link or name».</p>
  {fig_diy}
  <h2>3. Foto, dan bundelen, dan verzenden</h2>
  <p>Op {escape(DATE)} komen vrachtcijfers uit de officiële schatter. Geen verzonnen opslagdagen, geen verzonnen lijn.</p>
  <h2>Negen statussen, drie schermen</h2>
  <p>Eerst product plus binnenlands traject tot het magazijn. Internationaal later. «Waarom staat het stil?» bijna altijd: verkeerd scherm — bestellingen, dan magazijn, dan pakket.</p>
  {_guide_extra(key, fig_pay, fig_est)}
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
  <p>{escape(_est_note(key))} Bron: <a href="{customs_url}" rel="noopener">{customs}</a>.</p>
  {fig_est}
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
  <p><a class="btn" href="{est}">Officiële FansBuy-site</a> <a class="btn btn--ghost" href="{help_h}">Hulp</a></p>
</article>
"""
        legit_topic = f"is FansBuy een echte agent vanuit {dest}"
        legit_body = f"""
<article class="pw">
  <span class="eyebrow" style="color:var(--acd)">Check</span>
  <h1>Is FansBuy een echte inkoopagent?</h1>
  <p class="lead">fansbuy.com is het officiële product. Dit dest is onafhankelijk — geen hub. Dit dest is FansBuy niet.</p>
  {fig_off}
  <p>Op {escape(DATE)} zat de publieke officiële schatter. Daarom verzinnen we geen opslagvenster en geen tarief. Bestellingen alleen via {official}.</p>
  <p>Het afleveradres op dit dest is een {fp}.</p>
  <p><a class="btn" href="{guide}">Handleiding</a> <a class="btn btn--ghost" href="{help_h}">Hulp</a></p>
</article>
"""
        coup_topic = "kortingscodes staan op de officiële site"
        coup_body = f"""
<article class="pw">
  <span class="eyebrow" style="color:var(--acd)">Codes</span>
  <h1>Kortingscodes: niet in de titel van dit dest</h1>
  <p class="lead">Dit dest drukt geen uitnodigingscodes in de titel of op de homepage. Als FansBuy een code publiceert, staat die na het inloggen op {official}.</p>
  {fig_off}
  <p>Het afleveradres blijft een {fp}. Bestemming in de schatter: {dest_zh}.</p>
  <p><a class="btn" href="{official}">Officiële site</a> <a class="btn btn--ghost" href="{catalog}">Catalogus</a></p>
</article>
"""
        sheet_topic = f"de catalogus en hoe je hem vanuit {dest} gebruikt"
        sheet_body = f"""
<article class="pw">
  <span class="eyebrow" style="color:var(--acd)">Spreadsheet</span>
  <h1>FansBuy Spreadsheet is een catalogus, geen raster</h1>
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
  <h1>First FansBuy order, from {dest_e}</h1>
  <p class="lead">Copy the shop link, paste it into the agent, check the warehouse photo, consolidate, then pick destination {dest_zh}. The delivery address uses a {fp}.</p>
  {fig_off}
  <h2>1. Open a card on w2clinks</h2>
  <p>One of the thirty-three categories, a photo and the shop link. That is the catalogue, not an Excel file.</p>
  {fig_sheet}
  <h2>2. Paste it on the official site</h2>
  <p>Payment and tickets stay on {official}. This desk cannot see your account. The public paste bar is «Goods/shop's link or name». {escape(_storage(loc))}</p>
  {fig_diy}
  <h2>3. Photo, then consolidate, then ship</h2>
  <p>On {escape(DATE)} freight figures come only from the official estimator: pick the country, not this hostname. This desk does not invent a line.</p>
  <h2>Nine statuses, three screens</h2>
  <p>First the product plus domestic freight to the warehouse. International later. “Why is it stuck?” is almost always the wrong screen — orders, then warehouse, then the parcel.</p>
  {_guide_extra(key, fig_pay, fig_est)}
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
  <p class="lead">Pick destination {dest_zh} in the public estimator — no login. The delivery address uses a {fp}.</p>
  {fig_off}
  <h2>The official estimator decides</h2>
  <p>{escape(_est_note(key))} Import: <a href="{customs_url}" rel="noopener">{customs}</a>.</p>
  {fig_est}
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
  <p><a class="btn" href="{est}">Official FansBuy site</a> <a class="btn btn--ghost" href="{help_h}">Help</a></p>
</article>
"""
        legit_topic = f"is FansBuy a real agent from {dest}"
        legit_body = f"""
<article class="pw">
  <span class="eyebrow" style="color:var(--acd)">Check</span>
  <h1>Is FansBuy a real purchasing agent?</h1>
  <p class="lead">fansbuy.com is the official product. This dest is independent — no hub. This dest is not FansBuy.</p>
  {fig_off}
  <p>On {escape(DATE)} the public estimator is on the official estimator. That is why this desk publishes no invented storage window and no invented tariff. Orders only through {official}.</p>
  <p>The delivery address on this dest uses a {fp}.</p>
  <p><a class="btn" href="{guide}">Guide</a> <a class="btn btn--ghost" href="{help_h}">Help</a></p>
</article>
"""
        coup_topic = "coupons live on the official site"
        coup_body = f"""
<article class="pw">
  <span class="eyebrow" style="color:var(--acd)">Codes</span>
  <h1>Coupons: not in this dest title</h1>
  <p class="lead">This dest does not print invite codes in the title or on the homepage. If FansBuy publishes a code, it lives on {official} after you log in.</p>
  {fig_off}
  <p>The delivery address still uses a {fp}. Estimator destination: {dest_zh}.</p>
  <p><a class="btn" href="{official}">Official site</a> <a class="btn btn--ghost" href="{catalog}">Catalogue</a></p>
</article>
"""
        sheet_topic = f"the catalogue and how you use it from {dest}"
        sheet_body = f"""
<article class="pw">
  <span class="eyebrow" style="color:var(--acd)">Spreadsheet</span>
  <h1>FansBuy Spreadsheet is a catalogue, not a grid</h1>
  <p class="lead">Cards with a photo, a brand and the shop link. Thirty-three categories, the same wall as w2clinks.</p>
  {fig_sheet}
  <p>Search in English (sneakers, hoodie, jacket). The delivery address on this dest uses a {fp}.</p>
  <p><a class="btn" href="{catalog}">Open the catalogue</a> <a class="btn btn--ghost" href="{guide}">Guide</a></p>
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
        f"Independent FansBuy {name} for {p['dest_label']}.",
        f"https://{p['host']}{href}", [], body, href,
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
        "faq count 0",
        # Official fansbuy.com lime is the same hex the factory uses as a FansBuy sentinel.
        "FansBuy green / Georgia leaked",
    }
    err = [e for e in validate_desk(html, _facts(key), page=page) if e not in skip]
    if page == "home":
        err = [e for e in err if not e.startswith("faq count")]
        if page_title(desk, p["home_topic"]) not in html:
            err.append("home title")
        if p["fingerprint"] not in html:
            err.append("fingerprint")
        if "not an Excel file" not in html and "keine Excel-Datei" not in html and "non è un file Excel" not in html and "no es un archivo Excel" not in html and "n’est pas un fichier Excel" not in html and "geen Excel-bestand" not in html:
            err.append("sheet-explain")
        if "cat-30-shoes.png" not in html or "w2clinks.com/spreadsheet/fansbuy" not in html:
            err.append("W2C cats")
        if MAIL not in html:
            err.append("footer mail")
        if "/api/products/" in html:
            err.append("ops dump")
        if 'class="fig"' not in html:
            err.append("photos")
        for sid in ("shots", "states", "restricted"):
            if f'id="{sid}"' not in html:
                err.append(f"missing #{sid}")
        if p["loc"] != "en" and "Official fansbuy.com, 6 Oct" in html:
            err.append("english fig caption")
        for alien in p["aliens"]:
            if alien in html:
                err.append(f"alien {alien}")
        for tok in INVITES:
            if tok in html:
                err.append(f"invite {tok}")
        if 'class="sg-faq"' in html:
            err.append("home visible faq")
        if "FAQPage" not in html:
            err.append("home FAQ JSON-LD")
        if 'class="tl"' not in html:
            err.append("status timeline")
        for shot in (
            "oficial-inicio.jpg", "oficial-guidebook.jpg", "oficial-guidebook-3.jpg",
            f"estimator-{key}.jpg", "oficial-diy.jpg", "catalogus.jpg", "volume-voorbeeld.jpg",
        ):
            if shot not in html:
                err.append(f"missing {shot}")
        if re.search(r"58 l[ií]neas|23[,.]81\s*USD", html, flags=re.I):
            err.append("58/23.81")
    if page == "help" and p["fingerprint"] not in html:
        err.append("help fingerprint")
    if page == "help":
        if html.count("<h2>") < 5:
            err.append("help groups")
        if html.count('class="sg-faq"') < 12:
            err.append("help faq count")
        if re.search(r"58 l[ií]neas|23[,.]81\s*USD", html, flags=re.I):
            err.append("58/23.81")
    if page == "catalog":
        if 'class="eq"' not in html:
            err.append("catalog keys table")
        if "oficial-diy.jpg" not in html:
            err.append("catalog diy shot")
        if html.count('class="fig"') < 3:
            err.append("catalog figs")
    if page in ("guide", "ship", "legit", "coupons", "spreadsheet", "serioes"):
        if any(tok in html.lower() for tok in SISTER_LEFTOVER):
            err.append("sister leftover")
        if page != "coupons":
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


def _copy_assets(dest: Path, key: str) -> None:
    img = dest / "img"
    (img / "shots").mkdir(parents=True, exist_ok=True)
    (dest / "assets" / "images").mkdir(parents=True, exist_ok=True)
    (dest / "assets" / "css").mkdir(parents=True, exist_ok=True)
    shutil.copy(ASSETS / LOGO, dest / "assets" / "images" / LOGO)
    shutil.copy(ASSETS / "hero.jpg", img / "hero.jpg")
    shutil.copy(ASSETS / "favicon.ico", dest / "favicon.ico")
    shutil.copy(ASSETS / "favicon1.ico", dest / "favicon1.ico")
    for name in SHOTS:
        shutil.copy(ASSETS / "shots" / name, img / "shots" / name)
    shutil.copy(ASSETS / "shots" / f"estimator-{key}.jpg", img / "shots" / f"estimator-{key}.jpg")


def generate(key: str) -> dict[str, Path]:
    p = PACKS[key]
    if p["host"] in SKIP_PUT_HOSTS or p["host"] in TWINS or p["host"] in OFF_ORIGIN:
        raise SystemExit(f"refusing to generate a dest for hub/twin/foreign {p['host']}")
    dest = _overlay(key)
    dest.mkdir(parents=True, exist_ok=True)
    inner_rels = [href.strip("/") for href, _t, _b in _inner_pages(key).values()]
    for rel in ("start", p["help"].strip("/"), p["news"].strip("/"), p["about"].strip("/"), p["catalog"].strip("/"), *inner_rels):
        (dest / rel).mkdir(exist_ok=True)
    _copy_assets(dest, key)
    css_path = dest / "assets" / "css" / p["desk_css"]
    css_path.write_text(render_css(desk_for(key)), encoding="utf-8")
    theme = OUT / "shared" / "themes" / THEME_CSS
    theme.parent.mkdir(parents=True, exist_ok=True)
    theme.write_text(
        "/* FansBuy country dest — official coral #ff3344 from fansbuy.com */\n"
        ":root { --primary: #ff3344; --primary-dark: #ff3344; --primary-soft: #fff1f2; --nav-dark: #c12233; }\n"
        "body { background: var(--bg, #f7f8fa); }\n",
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
    _run(client, f"cp -a '{gsc}' '/www/backup/fansbuy-{key}-gsc-about-{stamp}.conf'")
    Path(f"/tmp/fansbuy-{key}-gsc.conf").write_text("".join(keep), encoding="utf-8")
    sftp.put(f"/tmp/fansbuy-{key}-gsc.conf", gsc)
    print(key, "stripped", stripped, "CMS-page home 301s")
    _reload_nginx(client)


def _map_legacy_english_cms(client, sftp, key: str) -> None:
    """DE/IT: 301 leftover English CMS slugs to dest slugs; drop FansBuy /about/ files."""
    p = PACKS[key]
    host = p["host"]
    root = f"/www/wwwroot/{host}"
    wanted: dict[str, str] = {}
    dropped: list[str] = []
    for old, dest in (
        ("about", p["about"]),
        ("help", p["help"]),
        ("news", p["news"]),
        ("catalog", p["catalog"]),
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
    _run(client, f"mkdir -p /www/backup; cp -a '{gsc}' '/www/backup/fansbuy-{key}-gsc-legacy-{stamp}.conf' 2>/dev/null || true")
    Path(f"/tmp/fansbuy-{key}-gsc-legacy.conf").write_text(new, encoding="utf-8")
    sftp.put(f"/tmp/fansbuy-{key}-gsc-legacy.conf", gsc)
    print(key, "legacy CMS 301s", " ".join(f"{a}->{b}" for a, b in wanted.items()))
    _reload_nginx(client)
    if dropped:
        print(key, "dropped leftover English CMS dirs", dropped)


def _map_faq_to_help(client, sftp, key: str) -> None:
    """Rewrite leftover /faq (and invite-code→faq) 301s in every extension conf.

    Exact `location =` in 00-gsc-exact-redirects.conf beats try_files, so appending
    a second /faq into gsc-redirects.conf duplicates the location and breaks nginx -t.
    Also drop 301s that would shadow new CMS slugs (fansbuy-coupons, start, …).
    """
    p = PACKS[key]
    host = p["host"]
    help_href = p["help"]
    root = f"/www/wwwroot/{host}"
    _run(client, f"rm -rf '{root}/faq'")
    ext = f"/www/server/panel/vhost/nginx/extension/{host}"
    listing = _run(client, f"find '{ext}' -maxdepth 1 -name '*.conf' -print")
    files = [ln.strip() for ln in listing.splitlines() if ln.strip().endswith(".conf")]
    unstick = {
        "start",
        p["help"].strip("/"),
        p["news"].strip("/"),
        p["about"].strip("/"),
        p["catalog"].strip("/"),
        "how-to-use-fansbuy",
        "fansbuy-freight",
        p["guide"].strip("/"),
        p["ship"].strip("/"),
    }
    if key in PHP_KEYS:
        unstick.update({"guide", "spreadsheet"})
    faq_src = {
        "/faq", "/faq/",
        "/fansbuy-invite-code", "/fansbuy-invite-code/",
        "/fansbuy-gutschein", "/fansbuy-gutschein/",
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
            _run(client, f"cp -a '{remote}' '/www/backup/fansbuy-{key}-{Path(remote).name}-{stamp}.conf'")
            tmp = Path(f"/tmp/fansbuy-{key}-{Path(remote).name}")
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
        Path(f"/tmp/fansbuy-{key}-gsc-faq.conf").write_text(body + add, encoding="utf-8")
        sftp.put(f"/tmp/fansbuy-{key}-gsc-faq.conf", gsc)
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
    marker = f'X-Desk "fansbuy-{key}-independent"'
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
        add_header X-Desk "fansbuy-{key}-independent" always;
    }}
"""
    if old not in text:
        print(key, "catch-all needle not the plain try_files; skip harden")
        return
    stamp = time.strftime("%Y%m%d-%H%M%S")
    _run(client, f"cp -a '{vhost}' '/www/backup/fansbuy-{key}-nginx-{stamp}.conf'")
    text = text.replace(old, new, 1)
    tmp = Path(f"/tmp/fansbuy-{key}.conf")
    tmp.write_text(text, encoding="utf-8")
    sftp.put(str(tmp), vhost)
    print(key, "hardened HTTPS catch-all")
    _reload_nginx(client)


def _php_legacy_maps(key: str) -> list[tuple[str, str]]:
    p = PACKS[key]
    cat, help_h, guide, ship = p["catalog"], p["help"], p["guide"], p["ship"]
    legit, coup = "/is-fansbuy-legit/", "/fansbuy-coupons/"
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
    """Move the five PHP ccTLDs off fansbuy-lite/public onto a static dest wwwroot."""
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
    _run(client, f"mkdir -p /www/backup '{dest_root}'; cp -a '{vhost}' '/www/backup/fansbuy-{key}-php-cutover-{stamp}.conf'")
    _run(client, f"cp -a '{rewrite}' '/www/backup/fansbuy-{key}-php-rewrite-{stamp}.conf' 2>/dev/null || true")
    text = text.replace("/www/wwwroot/fansbuy-lite/public", dest_root)
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
    if "/www/wwwroot/fansbuy-lite/public" in text or "fansbuy-lite/public" in text:
        raise SystemExit(f"refusing {host} vhost still on lite/public")
    if "enable-php-74.conf" in text:
        raise SystemExit(f"refusing {host} still includes php74")
    Path(f"/tmp/fansbuy-{key}-cutover.conf").write_text(text, encoding="utf-8")
    sftp.put(f"/tmp/fansbuy-{key}-cutover.conf", vhost)
    catch = (
        "location / {\n"
        "    try_files $uri $uri/ $uri/index.html =404;\n"
        '    add_header Strict-Transport-Security "max-age=31536000" always;\n'
        '    add_header Cache-Control "private, no-cache, must-revalidate" always;\n'
        f'    add_header X-Desk "fansbuy-{key}-independent" always;\n'
        "}\n"
    )
    Path(f"/tmp/fansbuy-{key}-rewrite.conf").write_text(catch, encoding="utf-8")
    sftp.put(f"/tmp/fansbuy-{key}-rewrite.conf", rewrite)
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
        _run(client, f"cp -a '{gsc}' '/www/backup/fansbuy-{key}-gsc-php-legacy-{stamp}.conf' 2>/dev/null || true")
        Path(f"/tmp/fansbuy-{key}-gsc-php-legacy.conf").write_text(new, encoding="utf-8")
        sftp.put(f"/tmp/fansbuy-{key}-gsc-php-legacy.conf", gsc)
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
        self_catch = f"return 301 https://{twin}$request_uri;"
        if self_catch in raw or f"https://{twin}/" in raw or f"https://{twin}$" in raw:
            _run(client, f"cp -a '{vhost}' '/www/backup/fansbuy-twin-{twin}-{stamp}.conf'")
            raw = raw.replace(f"https://{twin}$request_uri", f"https://{target}$request_uri")
            raw = raw.replace(f"https://{twin}/", f"https://{target}/")
            raw = re.sub(
                rf"return 301 https://{re.escape(twin)}(?![.\w])",
                f"return 301 https://{target}",
                raw,
            )
            Path(f"/tmp/fansbuy-twin-{twin}.conf").write_text(raw, encoding="utf-8")
            sftp.put(f"/tmp/fansbuy-twin-{twin}.conf", vhost)
            print("twin vhost 301s retargeted to", target)
        if want in raw:
            print("twin catch-all already $request_uri", twin)
        elif old in raw or old2 in raw:
            _run(client, f"cp -a '{vhost}' '/www/backup/fansbuy-twin-{twin}-{stamp}.conf'")
            raw = raw.replace(old, want).replace(old2, want)
            Path(f"/tmp/fansbuy-twin-{twin}.conf").write_text(raw, encoding="utf-8")
            sftp.put(f"/tmp/fansbuy-twin-{twin}.conf", vhost)
            print("twin catch-all now $request_uri", twin)
        else:
            print("WARN twin catch-all needle missing", twin, "(rewrite may still try_files)")
        rewrite = f"/www/server/panel/vhost/rewrite/{twin}.conf"
        rraw = _run(client, f"cat '{rewrite}' 2>/dev/null || true")
        if rraw and ("try_files" in rraw or f"https://{twin}" in rraw):
            _run(client, f"cp -a '{rewrite}' '/www/backup/fansbuy-twin-rewrite-{twin}-{stamp}.conf'")
            rnew = "location / {\n    return 301 https://" + target + "$request_uri;\n}\n"
            Path(f"/tmp/fansbuy-twin-rewrite-{twin}.conf").write_text(rnew, encoding="utf-8")
            sftp.put(f"/tmp/fansbuy-twin-rewrite-{twin}.conf", rewrite)
            print("twin rewrite now $request_uri 301 to", target)
        ext_inc = f"    include /www/server/panel/vhost/nginx/extension/{twin}/*.conf;\n"
        # US already included extension/*.conf. Other twins listed exact maps in
        # the vhost; including gsc-redirects duplicates location = /about.
        if twin != "fansbuy.co.uk" and ext_inc in raw:
            raw = raw.replace(ext_inc, "")
            Path(f"/tmp/fansbuy-twin-{twin}.conf").write_text(raw, encoding="utf-8")
            sftp.put(f"/tmp/fansbuy-twin-{twin}.conf", vhost)
            print("twin dropped duplicate extension include", twin)
        has_ext = f"extension/{twin}/" in raw
        if (not has_ext) and "location = /guides/shipping " not in raw:
            ship_lines = (
                f"    location = /guides/shipping {{ return 301 https://{target}/fansbuy-shipping-guide/; }}\n"
                f"    location = /guides/shipping/ {{ return 301 https://{target}/fansbuy-shipping-guide/; }}\n"
                f"    location = /guide/shipping {{ return 301 https://{target}/fansbuy-shipping-guide/; }}\n"
                f"    location = /guide/shipping/ {{ return 301 https://{target}/fansbuy-shipping-guide/; }}\n"
            )
            needle = "    location / {"
            if needle in raw:
                raw = raw.replace(needle, ship_lines + needle, 1)
                Path(f"/tmp/fansbuy-twin-{twin}.conf").write_text(raw, encoding="utf-8")
                sftp.put(f"/tmp/fansbuy-twin-{twin}.conf", vhost)
                print("twin vhost shipping maps", twin)
            else:
                print("WARN twin missing location / for shipping maps", twin)
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
            ("/guides/shipping", "/fansbuy-shipping-guide/"),
            ("/guide/shipping", "/fansbuy-shipping-guide/"),
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
            _run(client, f"cp -a '{vhost}' '/www/backup/fansbuy-twin-vhost-maps-{twin}-{stamp}.conf'")
            Path(f"/tmp/fansbuy-twin-{twin}.conf").write_text(vhost_new, encoding="utf-8")
            sftp.put(f"/tmp/fansbuy-twin-{twin}.conf", vhost)
            print("rewrote twin vhost exact maps", twin)
            raw = vhost_new
        gsc = f"/www/server/panel/vhost/nginx/extension/{twin}/gsc-redirects.conf"
        graw = _run(client, f"cat '{gsc}' 2>/dev/null || true")
        if graw and f"https://{twin}" in graw:
            _run(client, f"cp -a '{gsc}' '/www/backup/fansbuy-twin-gsc-{twin}-{stamp}.conf'")
            graw = graw.replace(f"https://{twin}", f"https://{target}")
            Path(f"/tmp/fansbuy-twin-gsc-{twin}.conf").write_text(graw, encoding="utf-8")
            sftp.put(f"/tmp/fansbuy-twin-gsc-{twin}.conf", gsc)
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
            _run(client, f"mkdir -p '{Path(gsc).parent}'; cp -a '{gsc}' '/www/backup/fansbuy-twin-gsc-extra-{twin}-{stamp}.conf' 2>/dev/null || true")
            Path(f"/tmp/fansbuy-twin-gsc-{twin}.conf").write_text("".join(out), encoding="utf-8")
            sftp.put(f"/tmp/fansbuy-twin-gsc-{twin}.conf", gsc)
            print("rewrote twin path maps", twin, len(wanted))
    _reload_nginx(client)
    _cf_bust(list(TWINS) + [PACKS[k]["host"] for k in PACKS])


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
  <p class="lead">Die alte Fassung gehörte nicht zu FansBuy. Die aktuelle Anleitung steht auf Start. Die Lieferadresse ist eine {fp}.</p>
  <p><a class="btn" href="/start/">Start</a> <a class="btn btn--ghost" href="{escape(p['guide'])}">Anleitung</a></p>
</article>
"""
    elif loc == "it":
        topic = "questo articolo è stato sostituito"
        body = f"""
<article class="pw">
  <h1>Questo articolo è stato sostituito</h1>
  <p class="lead">La versione precedente non era di FansBuy. La guida attuale sta su Start. L’indirizzo è una {fp}.</p>
  <p><a class="btn" href="/start/">Start</a> <a class="btn btn--ghost" href="{escape(p['guide'])}">Guida</a></p>
</article>
"""
    elif loc == "es":
        topic = "este artículo fue sustituido"
        body = f"""
<article class="pw">
  <h1>Este artículo fue sustituido</h1>
  <p class="lead">La versión anterior no era de FansBuy. La guía actual está en Start. La dirección es una {fp}.</p>
  <p><a class="btn" href="/start/">Start</a> <a class="btn btn--ghost" href="{escape(p['guide'])}">Guía</a></p>
</article>
"""
    elif loc == "fr":
        topic = "cet article a été remplacé"
        body = f"""
<article class="pw">
  <h1>Cet article a été remplacé</h1>
  <p class="lead">La version précédente n’était pas FansBuy. Le guide actuel est sur Start. L’adresse est une {fp}.</p>
  <p><a class="btn" href="/start/">Start</a> <a class="btn btn--ghost" href="{escape(p['guide'])}">Guide</a></p>
</article>
"""
    elif loc == "nl":
        topic = "dit artikel is vervangen"
        body = f"""
<article class="pw">
  <h1>Dit artikel is vervangen</h1>
  <p class="lead">De vorige versie hoorde niet bij FansBuy. De huidige gids staat op Start. Het afleveradres is een {fp}.</p>
  <p><a class="btn" href="/start/">Start</a> <a class="btn btn--ghost" href="{escape(p['guide'])}">Handleiding</a></p>
</article>
"""
    else:
        topic = "this article was replaced"
        body = f"""
<article class="pw">
  <h1>This article was replaced</h1>
  <p class="lead">The previous version was not a FansBuy dest page. The current guide is on Start. The delivery address uses a {fp}.</p>
  <p><a class="btn" href="/start/">Start</a> <a class="btn btn--ghost" href="{escape(p['guide'])}">Guide</a></p>
</article>
"""
    return cms_shell(
        desk, page_title(desk, topic),
        f"Replaced leftover article on {p['host']}.",
        f"https://{p['host']}{href}", [], body, href,
    )



GUIDE_MARK = {
    "es": "Primer pedido FansBuy",
    "fr": "Première commande FansBuy",
    "de": "Erste Bestellung bei FansBuy",
    "nl": "Eerste FansBuy-bestelling",
    "it": "Primo ordine FansBuy",
    "en": "First FansBuy order",
}
ABOUT_MARK = {
    "es": "Un sitio independiente sobre FansBuy",
    "fr": "Un site indépendant sur FansBuy",
    "de": "Eine unabhängige Site über FansBuy",
    "nl": "Een onafhankelijke site over FansBuy",
    "it": "Un sito indipendente su FansBuy",
    "en": "An independent site about FansBuy",
}


def _ship_mark(p: dict) -> str:
    return {
        "es": f"Enviar a {p['dest_label']}",
        "fr": f"Expédier vers {p['dest_label']}",
        "de": f"Versand nach {p['dest_label']}",
        "nl": f"Verzenden naar {p['dest_label']}",
        "it": f"Spedire in {p['dest_label']}",
    }.get(p["loc"], "Shipping to")


def _cms_hrefs(key: str) -> set[str]:
    p = PACKS[key]
    return {"/start/", p["help"], p["news"], p["about"], p["catalog"], p["guide"], p["ship"]}


def _wrap_targets(key: str) -> tuple[tuple[str, int], ...]:
    """Ranked inners to wrap; a path that is also a CMS slug is generated instead."""
    cms = _cms_hrefs(key)
    return tuple((href, floor) for href, floor in RANKED.get(key, ()) if href not in cms)


def _ranked_floor(key: str, rel: str) -> int | None:
    for href, floor in _wrap_targets(key):
        if rel == href.lstrip("/") + "index.html":
            return floor
    return None


_LOC_LINE = re.compile(
    r"location\s+(?P<mod>=|\^~)\s+(?P<path>\S+)\s*\{(?P<body>[^{}]*)\}"
)


def _unstick_shadows(client, sftp, key: str) -> None:
    """Drop locations that steal CMS slugs or ranked wrap URLs.

    Drops CMS-slug 301s including `location =` and `location ^~` so generated
    ship/guide/help are 200. CMS ship is `/fansbuy-freight/`; ranked shipping URLs stay wrap. Trailing-slash canonicalization onto the
    same wrap href is kept.
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
        _run(client, f"cp -a '{remote}' '/www/backup/fansbuy-{key}-unstick-{Path(remote).name}-{stamp}.conf'")
        tmp = Path(f"/tmp/fansbuy-{key}-unstick-{Path(remote).name}")
        tmp.write_text("".join(out), encoding="utf-8")
        sftp.put(str(tmp), remote)
        changed += 1
    if changed:
        _reload_nginx(client)
    else:
        print(key, "no cms/ranked shadow 301s")


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
        elif "data-inner-chrome=" in raw and PACKS[key]["css_id"] in raw:
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
            for tok in INVITES:
                out = out.replace(f"?ref={tok}", "").replace(tok, "")
        if why != "retire-poison" and len(out.encode("utf-8")) < (floor or 4000):
            print("WARN skip thin wrap", rel, len(out.encode("utf-8")))
            continue
        rel_dir = str(Path(rel).parent)
        _run(client, f"mkdir -p '{bak}/{rel_dir}'")
        _run(client, f"cp -a '{remote}' '{bak}/{rel}'")
        local_tmp = Path("/tmp") / f"fansbuy-wrap-{key}-{rel.replace('/', '_')}"
        local_tmp.write_text(out, encoding="utf-8")
        sftp.put(str(local_tmp), remote)
        print("WRAP", rel, "in", len(raw), "out", len(out.encode("utf-8")))
    present = {r for r in seen}
    for href, _floor in _wrap_targets(key):
        if href.lstrip("/") + "index.html" not in present:
            print(key, "ranked inner not present on origin (nothing to wrap)", href)




def put(key: str) -> None:
    host = PACKS[key]["host"]
    if host in SKIP_PUT_HOSTS or host in OFF_ORIGIN:
        raise SystemExit(f"refusing to PUT hub/foreign {host}")
    if host in TWINS:
        raise SystemExit(f"refusing to PUT twin {host}; twins only get a 301")
    files = generate(key)
    p = PACKS[key]
    host = p["host"]
    client = _connect()
    stamp = time.strftime("%Y%m%d-%H%M%S")
    bak = f"/www/backup/fansbuy-{key}-cms-{stamp}"
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
        if any(tok in raw.lower() for tok in SISTER_LEFTOVER):
            raise SystemExit(f"refusing {key} {name} with sister leftover")
        for tok in INVITES:
            if tok in raw:
                raise SystemExit(f"refusing {key} {name} with invite {tok}")
        _run(client, f"mkdir -p '{Path(remote).parent}'")
        sftp.put(str(local), remote)
        print("PUT", remote, local.stat().st_size)
    theme = OUT / "shared" / "themes" / THEME_CSS
    sftp.put(str(theme), f"{root}/assets/css/fansbuy-theme.css")
    sftp.put(str(files["css"]), f"{root}/assets/css/{p['desk_css']}")
    sftp.put(str(overlay / "assets" / "images" / "fansbuy-wordmark.png"), f"{root}/assets/images/fansbuy-wordmark.png")
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


def put_php() -> None:
    print("no PHP hub in this cluster")
    return
    """Surgical fansbuy-lite: fansbuy titles, strip 1Yi9, official green. Never touch public/."""
    client = _connect()
    stamp = time.strftime("%Y%m%d-%H%M%S")
    bak = f"/www/backup/fansbuy-php-{stamp}"
    lite = "/www/wwwroot/fansbuy-lite"
    files = [
        ("app/Services/DestLocal.php", f"{lite}/app/Services/DestLocal.php"),
        ("bootstrap/app.php", f"{lite}/bootstrap/app.php"),
        ("app/helpers.php", f"{lite}/app/helpers.php"),
        ("resources/views/layouts/app.php", f"{lite}/resources/views/layouts/app.php"),
        ("resources/views/home.php", f"{lite}/resources/views/home.php"),
    ]
    for loc in ("de", "es", "fr", "it", "nl", "pt"):
        files.append((f"resources/lang/{loc}.json", f"{lite}/resources/lang/{loc}.json"))
    for loc in ("de", "es", "fr", "it", "nl", "en", "pt"):
        files.append((f"resources/guides/{loc}.php", f"{lite}/resources/guides/{loc}.php"))
    for _rel, remote in files:
        if "/public/" in remote or remote.endswith("/public/index.php"):
            raise SystemExit(f"refusing public gold {remote}")
    _run(
        client,
        f"mkdir -p '{bak}' && cp -a '{lite}/resources/lang' '{lite}/bootstrap/app.php' "
        f"'{lite}/app/helpers.php' '{lite}/app/Services/DestLocal.php' "
        f"'{lite}/resources/views/home.php' '{lite}/resources/views/layouts/app.php' "
        f"'{lite}/resources/guides' '{bak}/'",
    )
    sftp = client.open_sftp()
    for rel, remote in files:
        local = PHP_OVERLAY / rel
        if not local.is_file():
            raise SystemExit(f"missing {local}")
        raw = local.read_text(encoding="utf-8")
        for tok in INVITES:
            if tok in raw:
                raise SystemExit(f"refusing {rel} with invite {tok}")
        _run(client, f"mkdir -p '{Path(remote).parent}'")
        sftp.put(str(local), remote)
        print("PUT php", remote, local.stat().st_size)
    for host in PHP_HOSTS:
        print("skip PHP wwwroot home", host)
    _run(
        client,
        "chown -R www:www "
        f"'{lite}/app/Services/DestLocal.php' '{lite}/bootstrap/app.php' "
        f"'{lite}/app/helpers.php' '{lite}/resources/lang' '{lite}/resources/guides' "
        f"'{lite}/resources/views/home.php' '{lite}/resources/views/layouts/app.php'",
    )
    sftp.close()
    print("php backup", bak)
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
            url, headers={"User-Agent": "fansbuy-cms/1.0", "Cache-Control": "no-cache"},
        )
        opener = urllib.request.build_opener(*([https] if follow else [https, NR()]))
        try:
            with opener.open(req, timeout=25) as resp:
                return resp.status, resp.geturl(), resp.headers.get("Location") or "", resp.read()
        except urllib.error.HTTPError as e:
            return e.code, url, e.headers.get("Location") or "", e.read() if e.fp else b""

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
            *((f"https://{host}{href}", "ranked-wrap", False) for href, _ in RANKED.get(k, ())[:2]),
        ]
        for url, kind, need_fp in checks:
            follow = kind in ("home", "start", "guide", "ship")
            code, final, loc, body = fetch(url, follow=follow)
            html = body.decode("utf-8", "replace")
            print(k, kind, code, "bytes", len(body), "loc", loc or final)
            if any(h in (final or "") or h in (loc or "") for h in SKIP_PUT_HOSTS):
                print(" FAIL 301 into hub"); fail += 1
            sisters = [h for h in dest_hosts if h != host]
            if any(s in (final or "") or s in (loc or "") for s in sisters):
                print(" FAIL 301 into sister dest"); fail += 1
            cms_kinds = ("home", "start", "help", "news", "about", "catalog", "guide", "ship")
            if kind not in ("404", "ranked-wrap") and code != 200:
                print(" FAIL status"); fail += 1
            if kind == "ranked-wrap" and code not in (200, 301, 302, 308):
                print(" FAIL ranked wrap status"); fail += 1
            if kind == "ranked-wrap" and code == 404:
                print(" FAIL ranked wrap 404"); fail += 1
            if any(tok in html.lower() for tok in SISTER_LEFTOVER):
                print(" FAIL sister leftover"); fail += 1
            if kind in cms_kinds:
                for tok in INVITES:
                    if tok in html:
                        print(" FAIL invite"); fail += 1
            if re.search(r"58 l[ií]neas|23[,.]81\s*USD", html, flags=re.I):
                print(" FAIL 58/23.81"); fail += 1
            if kind in cms_kinds:
                if "fansbuy-wordmark.png" not in html:
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
                if "FAQPage" not in html:
                    print(" FAIL homepage FAQ JSON-LD"); fail += 1
                if 'class="tl"' not in html:
                    print(" FAIL status timeline"); fail += 1
                for shot in (
                    "oficial-inicio.jpg", "oficial-guidebook.jpg", "oficial-guidebook-3.jpg",
                    f"estimator-{k}.jpg", "oficial-diy.jpg",
                ):
                    if shot not in html:
                        print(" FAIL missing", shot); fail += 1
                for sid in ("shots", "states", "restricted"):
                    if f'id="{sid}"' not in html:
                        print(" FAIL missing #", sid, sep=""); fail += 1
                if p["loc"] != "en" and "Official fansbuy.com, 6 Oct" in html:
                    print(" FAIL english fig caption"); fail += 1
                if 'class="lite-hero"' in html:
                    print(" FAIL leftover lite-hero"); fail += 1
            if kind == "ranked-wrap":
                if code in (301, 302, 308) and "/fansbuy-freight/" in ((loc or "") + (final or "")):
                    print(" FAIL ranked wrap 301 to freight"); fail += 1
                if code == 404:
                    print(" FAIL ranked wrap 404"); fail += 1
            if kind in ("guide", "ship"):
                mark = {
                    "de": ("Erste Bestellung bei FansBuy" if kind == "guide" else f"Versand nach {p['dest_label']}"),
                    "it": ("Primo ordine FansBuy" if kind == "guide" else "Spedire in Italia"),
                    "es": ("Primer pedido FansBuy" if kind == "guide" else f"Enviar a {p['dest_label']}"),
                    "fr": ("Première commande FansBuy" if kind == "guide" else f"Expédier vers {p['dest_label']}"),
                    "nl": ("Eerste FansBuy-bestelling" if kind == "guide" else f"Verzenden naar {p['dest_label']}"),
                }.get(p["loc"], ("First FansBuy order" if kind == "guide" else "Shipping to"))
                if mark not in html:
                    print(" FAIL", kind, "copy"); fail += 1
            if kind == "catalog" and html.count('class="cat"') < 30:
                print(" FAIL catalog wall"); fail += 1
            if kind == "news" and "ItemList" not in html:
                print(" FAIL news ItemList"); fail += 1
            if kind == "about":
                mark = {
                    "de": "Eine unabhängige Site über FansBuy",
                    "it": "Un sito indipendente su FansBuy",
                    "es": "Un sitio independiente sobre FansBuy",
                    "fr": "Un site indépendant sur FansBuy",
                    "nl": "Een onafhankelijke site over FansBuy",
                }.get(p["loc"], "An independent site about FansBuy")
                if mark not in html:
                    print(" FAIL about copy"); fail += 1
                if (loc or "").rstrip("/") == f"https://{host}":
                    print(" FAIL about 301 home"); fail += 1
            if kind == "help" and "FAQPage" not in html:
                print(" FAIL help FAQPage"); fail += 1
            if kind == "help" and html.count("<h2>") < 5:
                print(" FAIL help groups"); fail += 1
            if kind == "catalog" and 'class="eq"' not in html:
                print(" FAIL catalog keys table"); fail += 1
            if kind == "catalog" and "oficial-diy.jpg" not in html:
                print(" FAIL catalog diy"); fail += 1
            if kind == "catalog" and html.count('class="fig"') < 3:
                print(" FAIL catalog figs"); fail += 1
        if p["about"] != "/about/":
            code_ab, _, loc_ab, body_ab = fetch(f"https://{host}/about/", follow=False)
            print(k, "legacy about", code_ab, loc_ab)
            if code_ab not in (301, 302, 308) or p["about"].rstrip("/") not in (loc_ab or ""):
                print(" FAIL leftover /about/ not 301 to dest about"); fail += 1
            code_ab2, _, _, body_ab2 = fetch(f"https://{host}/about/", follow=True)
            html_ab = body_ab2.decode("utf-8", "replace")
            if any(tok in html_ab.lower() for tok in SISTER_LEFTOVER) or any(tok in html_ab for tok in INVITES):
                print(" FAIL leftover /about/ still sister/invite"); fail += 1
        code, _, _, nf = fetch(f"https://{host}/this-page-does-not-exist-cms/", follow=True)
        nhtml = nf.decode("utf-8", "replace")
        print(k, "404", code)
        if code != 404:
            print(" FAIL 404"); fail += 1
        if f"{p['not_found_tab']} | FansBuy Spreadsheet" not in nhtml:
            print(" FAIL 404 title"); fail += 1
    if key is None:
        for a, b in (
            ("https://fansbuy.co.uk/", "fansbuy.nl"),
            ("https://fansbuy.nl/", "fansbuy.co.uk"),
            ("https://fansbuyspreadsheet.de/", "fansbuy.nl"),
            ("https://fansbuy.eu/", "fansbuy.nl"),
            ("https://fansbuy.co.uk/", "fansbuysheets.net"),
            ("https://fansbuy.nl/", "usfansspreadsheet.nl"),
            ("https://fansbuyspreadsheet.de/", "hipobuy.es"),
            ("https://fansbuy.co.uk/", "usfansspreadsheet.co.uk"),
        ):
            code, final, loc, _ = fetch(a, follow=False)
            if code in (301, 302, 308) and ((loc or "") and (b in (loc or "") or b in (final or ""))):
                print(" FAIL sister dest 301", a, loc); fail += 1
            else:
                print("dest indep", a, code)
    for twin, target in TWINS.items():
        code, _, loc, _ = fetch(f"https://{twin}/", follow=False)
        print("twin", twin, code, loc)
        if code not in (301, 302, 308) or target not in (loc or ""):
            print(" FAIL twin 301"); fail += 1
        deep = f"https://{twin}/fansbuy-coupons/"
        code2, final2, loc2, body2 = fetch(deep, follow=True)
        print(" twin deep", code2, final2, len(body2))
        if target not in (final2 or "") or code2 == 404 or len(body2) < 8000:
            print(" FAIL twin deep"); fail += 1
        generic = f"https://{twin}/kept-path-check"
        code3, _, loc3, _ = fetch(generic, follow=False)
        print(" twin uri", code3, loc3)
        if code3 not in (301, 302, 308) or target not in (loc3 or "") or "/kept-path-check" not in (loc3 or ""):
            print(" FAIL twin request_uri"); fail += 1
    import urllib.request as _ur
    try:
        hub_req = _ur.Request("https://fansbuysheets.net/", headers={"User-Agent": "fansbuy-cms/1.0"})
        with _ur.urlopen(hub_req, timeout=25) as hub_resp:
            hub_body = hub_resp.read()
        hub_html = hub_body.decode("utf-8", "replace")
        print("hub", len(hub_body), "customs", "not a customs territory" in hub_html)
        if len(hub_body) < 18000 or "not a customs territory" not in hub_html:
            print(" FAIL hub collapsed or overwritten"); fail += 1
        if "fansbuy-uk-desk.css" in hub_html or "catalogus.jpg" in hub_html:
            print(" FAIL hub got country template"); fail += 1
    except Exception as e:
        print(" FAIL hub fetch", e); fail += 1
    print('hub fansbuysheets.net stays leftover extra hub; skip USFans and foreign hosts')
    for foreign in OFF_ORIGIN:
        print('skip foreign', foreign)
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


def put_many(keys: list[str]) -> None:
    for k in keys:
        put(k)
    _cf_bust([PACKS[k]["host"] for k in keys])


def _keys(args: list[str]) -> list[str]:
    if not args:
        return list(PACKS)
    host_to_key = {p["host"]: k for k, p in PACKS.items()}
    wanted = set()
    bad = []
    for a in args:
        if a in PACKS:
            wanted.add(a)
        elif a in host_to_key:
            wanted.add(host_to_key[a])
        else:
            bad.append(a)
    if bad:
        raise SystemExit(f"unknown dest {bad}; dests are {list(PACKS)}")
    return [k for k in PACKS if k in wanted]


if __name__ == "__main__":
    args = sys.argv[1:]
    cmd = args[0] if args else "generate"
    rest = args[1:]
    if cmd == "put":
        put_many(_keys(rest))
    elif cmd == "twins":
        client = _connect()
        sftp = client.open_sftp()
        try:
            _fix_twins(client, sftp)
        finally:
            sftp.close()
            client.close()
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
