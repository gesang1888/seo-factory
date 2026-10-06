#!/usr/bin/env python3
"""BBDBuy country dests: CA, UK, US, DE, IT.

Gold IA: hipobuy.es. Gold brand: bbdbuy.com (official orange tag #F0700C).
Same-agent country hosts stay independent. Same-country twins 301 into the
dest with $request_uri. Hub bbdbuyeu.net is not overwritten.

bbdbuy.com and bbdbuyeu.com are the same official product. The public
estimator URL redirected to login on 6 Oct 2026; this desk does not invent
a line, a transit-day count or a declared value.
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
ASSETS = Path("/tmp/bbdbuy-assets")
DATE = "6 Oct 2026"
OFFICIAL = "https://www.bbdbuy.com/"
EST = "https://www.bbdbuy.com/estimation"
HELP = "https://www.bbdbuy.com/help"
ACC = "#F0700C"
ACC_DARK = "#C45A0A"
MAIL = "cnfd85269032661@gmail.com"
HUB = "bbdbuyeu.net"
DEST_MIN = 22000
CSS_V = "20261006e"
INVITES = ("1QodRw", "BBD5OFF")

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

RANKED = (
    ("/is-bbdbuy-legit/", 8000),
    ("/bbdbuy-shipping/", 8000),
    ("/bbdbuy-coupons/", 8000),
    ("/bbdbuy-spreadsheet/", 8000),
    ("/how-to-use-bbdbuy/", 4000),
    ("/ist-bbdbuy-serioes/", 4000),
)

TWINS = {
    "bbdbuyspreadsheet.ca": "bbdbuy.ca",
    "bbdbuyspreadsheet.uk": "bbdbuy.uk",
    "bbdbuyspreadsheet.us": "bbdbuy.us",
    "bbdbuyeuspreadsheet.com": HUB,
}

TWIN_EXTRA = {
    "bbdbuyspreadsheet.ca": [
        ("/bbdbuy-canada", "/"),
        ("/bbdbuy-shipping-to-canada", "/bbdbuy-shipping/"),
        ("/is-bbdbuy-safe", "/is-bbdbuy-legit/"),
        ("/contact", "/contact/"),
    ],
    "bbdbuyspreadsheet.uk": [
        ("/is-bbdbuy-safe", "/is-bbdbuy-legit/"),
    ],
    "bbdbuyspreadsheet.us": [
        ("/best-bbdbuy-spreadsheet", "/best-bbdbuy-spreadsheet/"),
    ],
    "bbdbuyeuspreadsheet.com": [
        ("/bbd-invite-code", "/bbdbuyeu-invite-code/"),
        ("/bbd-community", "/bbdbuyeu-community/"),
        ("/bbd-shoes-spreadsheet", "/bbdbuyeu-shoes-spreadsheet/"),
        ("/bbd-spreadsheet-2026", "/bbdbuyeu-spreadsheet-2026/"),
        ("/bbd-refund-guide", "/bbdbuyeu-refund-guide/"),
        ("/is-bbd-legit", "/is-bbdbuyeu-legit/"),
        ("/how-to-use-bbd", "/how-to-use-bbdbuyeu/"),
        ("/bbd-shipping-guide", "/bbdbuyeu-shipping-guide/"),
    ],
}

CMS_PAGE_LOCS = (
    "about", "about/", "help", "help/", "news", "news/", "catalog", "catalog/",
    "start", "start/", "aiuto", "aiuto/", "catalogo", "catalogo/", "notizie", "notizie/",
    "chi-siamo", "chi-siamo/", "hilfe", "hilfe/", "katalog", "katalog/",
    "neuigkeiten", "neuigkeiten/", "ueber-uns", "ueber-uns/",
)

WRAP_SKIP_PREFIXES = (
    "help/", "news/", "about/", "catalog/", "start/", "aiuto/", "catalogo/",
    "notizie/", "chi-siamo/", "hilfe/", "katalog/", "neuigkeiten/", "ueber-uns/",
    "api/", "assets/", "img/",
    "bbdbuy-shipping/", "how-to-use-bbdbuy/", "is-bbdbuy-legit/",
    "bbdbuy-coupons/", "bbdbuy-spreadsheet/", "ist-bbdbuy-serioes/",
)
WRAP_POISON = ("orientdig", "orient dig", "1qodrw", "bbd5off")

EXTRA_CSS = """
.hero .eyebrow{color:#ffd8b0}
.hero p.lead{color:#fff4ea}
:root{--primary-soft:#fff1e6}
"""


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
        "guide": "/how-to-use-bbdbuy/",
        "ship": "/bbdbuy-shipping/",
        "nav": [
            ("/start/", "Start"),
            ("/how-to-use-bbdbuy/", "Guide"),
            ("/catalog/", "Catalog"),
            ("/bbdbuy-shipping/", "Shipping"),
            ("/help/", "Help"),
            ("/news/", "News"),
        ],
        "footer_sections": [
            ("/how-to-use-bbdbuy/", "BBDBuy guide"),
            ("/catalog/", "The spreadsheet and the categories"),
            ("/bbdbuy-shipping/", "Shipping and customs"),
            ("/help/", "Help and questions"),
            ("/news/", "News"),
            ("/about/", "About us"),
        ],
        "aliens": aliens,
        "not_found_tab": "Page not found",
        "login": "Log in to BBDBuy",
        "menu": "Open menu",
        "home_cta": "Back to the homepage",
        "skip": "en",
        "desk_css": css,
        "css_id": css_id,
    }


PACKS = {
    "ca": _en_pack(
        "bbdbuy.ca", "CA", "Canada", "Canada — 加拿大", "en-CA", "CAD",
        "buy in China from Canada, safely",
        "BBDBuy Spreadsheet: the guide to buying in China from Canada",
        "How you paste a product link into the agent, how the w2clinks catalogue works, how a parcel travels to Canada, and what you check before CBSA.",
        "Canadian postal code (form A1A 1A1)", "CBSA", "https://www.cbsa-asfc.gc.ca/",
        ("Packstation", "Poste Italiane", "Northern Ireland is often another", "does not invent a de-minimis dollar"),
        "bbdbuy-ca-desk.css", "bbdbuy-ca",
    ),
    "uk": _en_pack(
        "bbdbuy.uk", "GB", "the United Kingdom", "United Kingdom — 英国", "en-GB", "GBP",
        "buy in China from the United Kingdom, safely",
        "BBDBuy Spreadsheet: the guide to buying in China from the United Kingdom",
        "How you paste a product link into the agent, how the w2clinks catalogue works, how a parcel travels to the United Kingdom, and what you check before HMRC.",
        "UK postcode. Northern Ireland is often another carrier product", "HMRC",
        "https://www.gov.uk/goods-sent-from-abroad",
        ("Packstation", "Poste Italiane", "form A1A 1A1", "does not invent a de-minimis dollar"),
        "bbdbuy-uk-desk.css", "bbdbuy-uk",
    ),
    "us": _en_pack(
        "bbdbuy.us", "US", "the United States", "United States — 美国", "en-US", "USD",
        "buy in China from the United States, safely",
        "BBDBuy Spreadsheet: the guide to buying in China from the United States",
        "How you paste a product link into the agent, how the w2clinks catalogue works, how a parcel travels to the United States, and what you check before CBP.",
        "US street + ZIP. This desk does not invent a de-minimis dollar", "CBP",
        "https://www.cbp.gov/",
        ("Packstation", "Poste Italiane", "form A1A 1A1", "Northern Ireland is often another"),
        "bbdbuy-us-desk.css", "bbdbuy-us",
    ),
    "de": {
        "host": "bbdbuyspreadsheet.de",
        "dest": "DE",
        "dest_label": "Deutschland",
        "dest_zh": "Germany — 德国",
        "lang": "de-DE",
        "loc": "de",
        "in_language": "auf Deutsch",
        "ccy": "EUR",
        "home_topic": "in China kaufen aus Deutschland, sicher",
        "hero_h1": "BBDBuy Spreadsheet: die Anleitung, um in China von Deutschland aus zu kaufen",
        "eyebrow": "Unabhängiger Leitfaden, auf Deutsch",
        "lead": "Wie du einen Produktlink in den Agenten einfügst, wie der w2clinks-Katalog funktioniert, wie ein Paket nach Deutschland reist und was du vor dem Zoll prüfst.",
        "fingerprint": dest_local_pack("DE")["fingerprint"],
        "customs": "Zoll",
        "customs_url": "https://www.zoll.de/",
        "postal": "deutsche PLZ. Packstation-Nummern sind ein DE-Muster",
        "catalog": "/katalog/",
        "help": "/hilfe/",
        "news": "/neuigkeiten/",
        "about": "/ueber-uns/",
        "guide": "/how-to-use-bbdbuy/",
        "ship": "/bbdbuy-shipping/",
        "nav": [
            ("/start/", "Start"),
            ("/how-to-use-bbdbuy/", "Anleitung"),
            ("/katalog/", "Katalog"),
            ("/bbdbuy-shipping/", "Versand"),
            ("/hilfe/", "Hilfe"),
            ("/neuigkeiten/", "News"),
        ],
        "footer_sections": [
            ("/how-to-use-bbdbuy/", "BBDBuy-Anleitung"),
            ("/katalog/", "Spreadsheet und Kategorien"),
            ("/bbdbuy-shipping/", "Versand und Zoll"),
            ("/hilfe/", "Hilfe und Fragen"),
            ("/neuigkeiten/", "News"),
            ("/ueber-uns/", "Über uns"),
        ],
        "aliens": ("form A1A 1A1", "Poste Italiane", "Northern Ireland is often another", "does not invent a de-minimis dollar"),
        "not_found_tab": "Seite nicht gefunden",
        "login": "Bei BBDBuy anmelden",
        "menu": "Menü öffnen",
        "home_cta": "Zurück zur Startseite",
        "skip": "de",
        "desk_css": "bbdbuy-de-desk.css",
        "css_id": "bbdbuy-de",
    },
    "it": {
        "host": "bbdbuy.it",
        "dest": "IT",
        "dest_label": "l’Italia",
        "dest_zh": "Italy — 意大利",
        "lang": "it-IT",
        "loc": "it",
        "in_language": "in italiano",
        "ccy": "EUR",
        "home_topic": "comprare in Cina dall’Italia, in sicurezza",
        "hero_h1": "BBDBuy Spreadsheet: la guida per comprare in Cina dall’Italia",
        "eyebrow": "Guida indipendente, in italiano",
        "lead": "Come incolli un link prodotto nell’agente, come funziona il catalogo w2clinks, come un pacco arriva in Italia e cosa controlli prima dell’Agenzia delle Dogane.",
        "fingerprint": dest_local_pack("IT")["fingerprint"],
        "customs": "Agenzia delle Dogane e dei Monopoli",
        "customs_url": "https://www.adm.gov.it/portale/",
        "postal": "via italiana e CAP a cinque cifre. Poste Italiane è il corriere locale di riferimento",
        "catalog": "/catalogo/",
        "help": "/aiuto/",
        "news": "/notizie/",
        "about": "/chi-siamo/",
        "guide": "/how-to-use-bbdbuy/",
        "ship": "/bbdbuy-shipping/",
        "nav": [
            ("/start/", "Start"),
            ("/how-to-use-bbdbuy/", "Guida"),
            ("/catalogo/", "Catalogo"),
            ("/bbdbuy-shipping/", "Spedizione"),
            ("/aiuto/", "Aiuto"),
            ("/notizie/", "Notizie"),
        ],
        "footer_sections": [
            ("/how-to-use-bbdbuy/", "Guida BBDBuy"),
            ("/catalogo/", "Lo spreadsheet e le categorie"),
            ("/bbdbuy-shipping/", "Spedizione e dogana"),
            ("/aiuto/", "Aiuto e domande"),
            ("/notizie/", "Notizie"),
            ("/chi-siamo/", "Chi siamo"),
        ],
        "aliens": ("Packstation", "form A1A 1A1", "Northern Ireland is often another", "does not invent a de-minimis dollar"),
        "not_found_tab": "Pagina non trovata",
        "login": "Accedi a BBDBuy",
        "menu": "Apri il menu",
        "home_cta": "Torna alla homepage",
        "skip": "it",
        "desk_css": "bbdbuy-it-desk.css",
        "css_id": "bbdbuy-it",
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
            "Unabhängiger deutschsprachiger Leitfaden zu BBDBuy und dazu, wie du den "
            "Katalog von w2clinks nutzt, um von Deutschland aus in China zu kaufen."
        )
        independence = (
            "BBDBuy Spreadsheet ist eine unabhängige Informationsseite. Wir sind nicht "
            "BBDBuy, wir nehmen keine Bestellungen an, wir kassieren kein Porto und wir "
            "sehen dein Konto nicht. Bestellung, Zahlung und Reklamation laufen über die offizielle Site."
        )
        copyright = "&copy; 2026 BBDBuy Spreadsheet. Deutscher Text, vor der Veröffentlichung gegengelesen."
        sections_h, official_h, independence_h, nav_aria = (
            "Bereiche", "Offizielle Links", "Unabhängigkeitshinweis.", "Hauptmenü",
        )
        nf_h1, nf_lead = "Diese Seite gibt es nicht", "Der Link ist vielleicht alt. Das sind die Bereiche, die existieren:"
        official_links = [
            (_off(p["host"]), "BBDBuy (offizielle Site)"),
            (_off(p["host"], "/register"), "BBDBuy-Konto"),
            (_off(p["host"], "/estimation"), "Fracht-Schätzer (Login am 6 Oct 2026)"),
        ]
    elif loc == "it":
        intro = (
            "Guida indipendente in italiano su BBDBuy e su come usi il catalogo w2clinks "
            "per comprare in Cina dall’Italia."
        )
        independence = (
            "BBDBuy Spreadsheet è un sito informativo indipendente. Non siamo BBDBuy, "
            "non elaboriamo ordini, non incassiamo il trasporto e non vediamo il tuo account. "
            "Ogni ordine, pagamento e reclamo passa dal sito ufficiale."
        )
        copyright = "&copy; 2026 BBDBuy Spreadsheet. Testo italiano, riletto prima della pubblicazione."
        sections_h, official_h, independence_h, nav_aria = (
            "Sezioni", "Link ufficiali", "Nota di indipendenza.", "Menu principale",
        )
        nf_h1, nf_lead = "Questa pagina non esiste", "Il link forse è vecchio. Queste sezioni invece ci sono:"
        official_links = [
            (_off(p["host"]), "BBDBuy (sito ufficiale)"),
            (_off(p["host"], "/register"), "Account BBDBuy"),
            (_off(p["host"], "/estimation"), "Preventivo (login il 6 Oct 2026)"),
        ]
    else:
        intro = (
            f"Independent English-language guide to BBDBuy and to how you use the w2clinks "
            f"catalogue to buy in China from {p['dest_label']}."
        )
        independence = (
            "BBDBuy Spreadsheet is an independent information site. We are not BBDBuy, "
            "we do not process orders, we do not collect shipping fees and we cannot see "
            "your account. Every order, payment and claim runs through the official site."
        )
        copyright = "&copy; 2026 BBDBuy Spreadsheet. English copy, edited and checked by people before publication."
        sections_h, official_h, independence_h, nav_aria = (
            "Sections", "Official links", "Independence notice.", "Main menu",
        )
        nf_h1, nf_lead = "This page does not exist", "The link may be old. These are the sections that do exist:"
        official_links = [
            (_off(p["host"]), "BBDBuy (official site)"),
            (_off(p["host"], "/register"), "Create a BBDBuy account"),
            (_off(p["host"], "/estimation"), "Official estimator (login wall on 6 Oct 2026)"),
        ]
    return CountryDesk(
        host=p["host"],
        agent="BBDBuy",
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
        logo_src="/assets/images/bbdbuy-logo.png",
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
        theme_css="bbdbuy-theme.css",
        desk_css=p["desk_css"],
        inner_marker=inner,
        register_path="/register",
        sheet_slug="bbdbuy",
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
        "agent": "BBDBuy",
        "host": p["host"],
        "lang": p["lang"],
        "loc": p["loc"],
        "dest": p["dest"],
        "dest_label": p["dest_label"],
        "ccy": p["ccy"],
        "storage": (
            f"Official BBDBuy estimator URL redirected to login on {DATE}; "
            "confirm live Help the morning you ship. This desk does not invent a free-day count."
        ),
        "estimator": EST,
        "official": OFFICIAL,
        "date": DATE,
        "keep": [
            ("/bbdbuy-shipping/", "Shipping"),
            ("/is-bbdbuy-legit/", "Review"),
            ("/bbdbuy-spreadsheet/", "Spreadsheet"),
            ("/how-to-use-bbdbuy/", "Guide"),
        ],
        "codes_off_title": list(INVITES),
        "strict_html_codes": True,
    }


def _faqs(key: str) -> list[tuple[str, str]]:
    p = PACKS[key]
    pairs = []
    for q, a in long_faqs(_facts(key)):
        a = a.replace("/api/products/", "w2clinks")
        pairs.append((q, a))
    extra = f"The delivery address uses a {p['postal']}."
    if p["loc"] == "de":
        extra = f"Die Lieferadresse ist eine {p['postal']}."
    elif p["loc"] == "it":
        extra = f"L’indirizzo di consegna è una {p['postal']}."
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


def _cats(key: str):
    loc = PACKS[key]["loc"]
    if loc == "de":
        return cats_for(DE_LABELS)
    if loc == "it":
        return cats_for(IT_LABELS)
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
    if loc == "de":
        off_alt, off_cap = (
            "Offizielle BBDBuy-Startseite: orangeres BBD-Tag, Suche, Forwarding und Estimation in der Navigation",
            f"Offizielle bbdbuy.com, {DATE}. Estimation in der Navigation öffnete an dem Morgen ein Login. Dieser Desk erfindet keine Linie und keinen Betrag.",
        )
        sheet_alt, sheet_cap = (
            "BBDBuy-Katalog auf w2clinks: Produktkarten mit Foto, Marke und Referenzpreis",
            "Karten, keine Excel-Zellen. Yuan-Preise ändern sich täglich. Aufnahme 6 Oct 2026, Kategorie SNEAKERS.",
        )
        vol_alt, vol_cap = (
            "Rechenbeispiel Volumengewicht: 40×40×3 cm und 200 g Waage werden 600 g Volumen",
            "Ein Rechenbeispiel, kein Lagerfoto. Viele Linien rechnen das Maximum aus Waage und Volumen, oft L×B×H (cm) / 8000.",
        )
        zoek_alt, zoek_cap = (
            "Hoodie-Suche im BBDBuy-Katalog auf w2clinks",
            "Ergebnisse mit Filterspalte. Aufnahme 6 Oct 2026.",
        )
    elif loc == "it":
        off_alt, off_cap = (
            "Homepage ufficiale BBDBuy: tag BBD arancione, ricerca, forwarding e estimation nel menu",
            f"Sito ufficiale bbdbuy.com, {DATE}. Estimation nel menu quella mattina apriva un login. Questa guida non inventa una linea né un importo.",
        )
        sheet_alt, sheet_cap = (
            "Catalogo BBDBuy su w2clinks: schede con foto, marca e prezzo di riferimento",
            "Schede, non celle Excel. I prezzi in yuan cambiano ogni giorno. Scatto 6 Oct 2026, categoria SNEAKERS.",
        )
        vol_alt, vol_cap = (
            "Esempio di peso volumetrico: 40×40×3 cm e 200 g in bilancia diventano 600 g di volume",
            "Un esempio calcolato, non una foto di magazzino. Molte linee fatturano il massimo tra bilancia e volume, spesso L×W×H (cm) / 8000.",
        )
        zoek_alt, zoek_cap = (
            "Ricerca hoodie nel catalogo BBDBuy su w2clinks",
            "Risultati con colonna filtri. Scatto 6 Oct 2026.",
        )
    else:
        off_alt, off_cap = (
            "Official BBDBuy homepage: orange BBD tag, search bar, forwarding and estimation in the nav",
            f"Official bbdbuy.com, {DATE}. Estimation in the nav still opened a login wall that morning. This desk does not invent a line or a dollar amount.",
        )
        sheet_alt, sheet_cap = (
            "BBDBuy catalogue on w2clinks: product cards with photo, brand and reference price",
            "Cards, not Excel cells. Yuan prices change by the day. Capture 6 Oct 2026, category SNEAKERS.",
        )
        vol_alt, vol_cap = (
            "Worked example of volume weight: 40×40×3 cm and 200 g scale becomes 600 g volume",
            "A worked example, not a warehouse photo. Many lines bill the greater of scale and volume, often L×W×H (cm) / 8000.",
        )
        zoek_alt, zoek_cap = (
            "Hoodie search in the BBDBuy catalogue on w2clinks",
            "Results with the filter column. Capture 6 Oct 2026.",
        )
    fig_off = _fig("/img/shots/oficial.jpg", off_alt, off_cap)
    fig_sheet = _fig("/img/shots/catalogus.jpg", sheet_alt, sheet_cap, 1200, 900)
    fig_vol = _fig("/img/shots/volume-voorbeeld.jpg", vol_alt, vol_cap, 1200, 640)
    fig_zoek = _fig("/img/shots/catalogus-zoek.jpg", zoek_alt, zoek_cap, 1200, 900)
    return fig_off, fig_sheet, fig_vol, fig_zoek


def _sec_shots(key: str, fig) -> str:
    p = PACKS[key]
    loc, dest = p["loc"], p["dest_label"]
    if loc == "de":
        return f"""
<section class="sec" id="shots">
  <div class="wrap"><div class="split split--rev"><div>
    <h2>Einen chinesischen Link einfügen, oder in der App suchen</h2>
    <p class="lead">BBDBuy beginnt so: einen Link von Taobao, 1688 oder Weidian einfügen, oder den Namen tippen. Der chinesische Shop sieht BBDBuy; du siehst danach Lagerfotos und eine Linie nach Deutschland.</p>
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
    <p class="lead">BBDBuy parte così: incolli un link di Taobao, 1688 o Weidian, o digiti il nome. Il negozio cinese vede BBDBuy; tu poi vedi le foto di magazzino e una linea verso l’Italia.</p>
    <p>Se la ricerca non legge il link, il passo successivo è il modulo manuale: nome, taglia, colore e prezzo in yuan. L’internazionale lo paghi dopo, dal magazzino.</p>
    <p><a class="btn" href="{escape(p["guide"])}">Guida passo passo</a>
       <a class="btn btn--ghost" href="{escape(OFFICIAL)}" rel="noopener">Sito ufficiale</a></p>
  </div>{fig}</div></div>
</section>
"""
    return f"""
<section class="sec" id="shots">
  <div class="wrap"><div class="split split--rev"><div>
    <h2>Paste a Chinese link, or search in the app</h2>
    <p class="lead">BBDBuy starts the same way: paste a Taobao, 1688 or Weidian link, or type the name. The Chinese shop sees BBDBuy; you later see warehouse photos and a line to {escape(dest)}.</p>
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
    <p class="lead">Zuerst zahlst du das Produkt plus den Inlandsweg in China bis zum Lager. International kommt später, wenn du eine Linie nach Deutschland wählst. «Warum steht es still?» heißt fast immer: du schaust auf den falschen Bildschirm.</p>
    <p>Die ersten Schritte liegen unter Bestellungen, danach Lager, danach das Paket, das du absendest. Am {escape(DATE)} öffnete der öffentliche Schätzer ein Login: dieser Desk erfindet keine Lagerfrist.</p>
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
    <p>I primi passi stanno sotto gli ordini, poi il magazzino, poi il pacco che invii. Il {escape(DATE)} il preventivo pubblico apriva un login: questa guida non inventa giorni di giacenza.</p>
    <p><a class="btn" href="{escape(p["guide"])}">Guida con il percorso</a></p>
  </div>{fig}</div></div>
</section>
"""
    return f"""
<section class="sec" id="states">
  <div class="wrap"><div class="split"><div>
    <h2>Nine statuses, three screens</h2>
    <p class="lead">You first pay the product plus domestic China freight to the warehouse. International comes later, when you pick a line to {escape(dest)}. “Why is it stuck?” is almost always: you are looking at the wrong screen.</p>
    <p>The first stretch lives under orders, then warehouse, then the parcel you submit. On {escape(DATE)} the public estimator opened a login wall: this desk does not invent a free-storage day count.</p>
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
    <p>Regel: ohne echten Preis und Varianten nicht bestellen. Tabak, Alkohol und Arzneimittel reisen nicht. Restricted ist eine Kaufsperre, kein Bescheid vom {escape(customs)}. BBDBuy verkauft keine eigene Ware.</p>
  </div>{fig}</div></div>
</section>
"""
    if loc == "it":
        return f"""
<section class="sec sec--tint" id="restricted">
  <div class="wrap"><div class="split split--rev"><div>
    <h2>Molti prodotti non si possono comprare anche se compaiono</h2>
    <p class="lead">Sul sito ufficiale vedi schede senza prezzo, o un modulo manuale al posto di una scheda negozio. Non è un bug di questa homepage: il link sorgente non è acquistabile tramite l’agente, o il prezzo non si è letto.</p>
    <p>Regola: senza prezzo vero e varianti non ordinare. Tabacco, alcol e farmaci non viaggiano. Restricted è un blocco d’acquisto, non un avviso della {escape(customs)}. BBDBuy non vende merce propria.</p>
  </div>{fig}</div></div>
</section>
"""
    return f"""
<section class="sec sec--tint" id="restricted">
  <div class="wrap"><div class="split split--rev"><div>
    <h2>Many products you cannot buy even if they appear</h2>
    <p class="lead">On the official site you will see cards without a price, or a manual form instead of a shop card. That is not a bug of this homepage: the source link is not buyable through the agent, or the price could not be read.</p>
    <p>Rule: without a real price and variants, do not order. Tobacco, alcohol and medicines do not travel. Restricted is a purchase block, not a {escape(customs)} seizure notice. BBDBuy does not sell its own stock.</p>
  </div>{fig}</div></div>
</section>
"""


def build_home(key: str) -> str:
    p = PACKS[key]
    desk = desk_for(key)
    sheet = _sheet(desk)
    wall = _wall(key)
    chips = _chips(key)
    fig_off, fig_sheet, fig_vol, fig_zoek = _shots(key)
    dest = p["dest_label"]
    loc = p["loc"]
    shots = _sec_shots(key, fig_zoek)
    states = _sec_states(key, fig_off)
    restricted = _sec_restricted(key, fig_sheet)
    if loc == "de":
        body = f"""
<section class="hero">
  <div class="hero__bg" role="img" aria-label="Offizielle BBDBuy-Startseite"></div>
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
    <p class="lead">BBDBuy verkauft keine eigene Ware. Er kauft für dich in chinesischen Shops, die nicht ins Ausland senden, nimmt das Paket im Lager an, fotografiert es, lagert es und schickt es nach Deutschland, wenn du das entscheidest.</p>
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
    <h2>Deutschland hat Linien, aber nicht jede Linie ist offen</h2>
    <p class="lead">Im Schätzer Ziel <strong>{escape(p["dest_zh"])}</strong> wählen, nicht EU und nicht AT. Die Lieferadresse ist eine {escape(p["postal"])}.</p>
    <p>Am {escape(DATE)} öffnete die öffentliche Estimator-URL ein Login, keinen Live-Preis. Dieser Desk erfindet keine Linie, keine Transitzeit und keinen Eurobetrag. Quelle: <a href="{escape(p["customs_url"])}" rel="noopener">{escape(p["customs"])}</a>.</p>
    <p><a class="btn" href="{escape(EST)}">Offizielle BBDBuy-Site</a>
       <a class="btn btn--ghost" href="{escape(p["ship"])}">Versandplan</a></p>
  </div>{fig_off}</div></div>
</section>
<section class="sec" id="volume">
  <div class="wrap"><div class="split split--rev"><div>
    <h2>Das Gewicht, das du zahlst, ist fast nie nur die Waage</h2>
    <p class="lead">Viele Linien rechnen das Maximum aus Waage und Volumen. Ein üblicher Teiler ist L×B×H (cm) / 8000. Eine Daunenjacke ist leicht und voluminös: dort entscheidet das Volumen.</p>
    <p>Beispiel: 40×40×3 cm sind 4800 cm³, geteilt durch 8000 sind 600 g Volumen bei 200 g Echtgewicht. Deine Maße trägst du im offiziellen Schätzer ein, Ziel Deutschland, sobald du eingeloggt bist.</p>
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
        desc = "Unabhängiger Leitfaden auf Deutsch: wie du über BBDBuy in China kaufst, wie der w2clinks-Katalog funktioniert, wie ein Paket nach Deutschland reist."
    elif loc == "it":
        body = f"""
<section class="hero">
  <div class="hero__bg" role="img" aria-label="Homepage ufficiale BBDBuy"></div>
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
    <p class="lead">BBDBuy non vende merce propria. Compra per te nei negozi cinesi che non spediscono all’estero, riceve il pacco in magazzino, lo fotografa, lo conserva e lo spedisce in Italia quando decidi tu.</p>
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
    <p>Il {escape(DATE)} l’URL pubblico del preventivo apriva un login, non un prezzo live. Questa guida non inventa una linea, un transito né un importo. Fonte: <a href="{escape(p["customs_url"])}" rel="noopener">{escape(p["customs"])}</a>.</p>
    <p><a class="btn" href="{escape(EST)}">Sito ufficiale BBDBuy</a>
       <a class="btn btn--ghost" href="{escape(p["ship"])}">Piano spedizione</a></p>
  </div>{fig_off}</div></div>
</section>
<section class="sec" id="volume">
  <div class="wrap"><div class="split split--rev"><div>
    <h2>Il peso che paghi quasi mai è solo la bilancia</h2>
    <p class="lead">Molte linee fatturano il massimo tra bilancia e volume. Un divisore comune è L×W×H (cm) / 8000. Un piumino è leggero e ingombrante: lì decide il volume.</p>
    <p>Esempio: 40×40×3 cm sono 4800 cm³, divisi per 8000 sono 600 g di volume a 200 g reali. Le tue misure le inserisci nel preventivo ufficiale, destinazione Italia, quando sei loggato.</p>
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
        desc = "Guida indipendente in italiano: come compri in Cina con BBDBuy, come funziona il catalogo w2clinks, come un pacco arriva in Italia."
    else:
        body = f"""
<section class="hero">
  <div class="hero__bg" role="img" aria-label="Official BBDBuy homepage"></div>
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
    <p class="lead">BBDBuy does not sell its own goods. It buys for you in Chinese shops that do not ship abroad, receives the parcel in the warehouse, photographs it, stores it, and ships to {escape(dest)} when you decide.</p>
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
    <p>What you see on w2clinks are cards, not cells. Each fiche has the link BBDBuy needs.</p>
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
    <p class="lead">Pick destination <strong>{escape(p["dest_zh"])}</strong> in the official estimator when you are logged in. The delivery address is a {escape(p["postal"])}.</p>
    <p>On {escape(DATE)} the public estimator URL opened a login wall, not a live rate. This desk does not invent a line, a transit-day count or a money amount. Open {escape(OFFICIAL)} the morning you ship. Import: <a href="{escape(p["customs_url"])}" rel="noopener">{escape(p["customs"])}</a>.</p>
    <p><a class="btn" href="{escape(EST)}">Official BBDBuy site</a>
       <a class="btn btn--ghost" href="{escape(p["ship"])}">Shipping plan</a></p>
  </div>{fig_off}</div></div>
</section>
<section class="sec" id="volume">
  <div class="wrap"><div class="split split--rev"><div>
    <h2>The weight you pay is almost never the scale alone</h2>
    <p class="lead">Many lines bill the greater of scale and volume. A common divisor is L×W×H (cm) / 8000. A down jacket is light and bulky: volume decides.</p>
    <p>Example: 40×40×3 cm is 4800 cm³, divided by 8000 is 600 g volume at 200 g real weight. You enter your measurements in the official estimator when you are logged in, destination {escape(p["dest_zh"].split("—")[0].strip())}.</p>
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
            f"Independent English guide: how you buy in China through BBDBuy, how the w2clinks catalogue works, how a parcel travels to {dest}."
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
    notes = {"de": CAT_NOTES_DE, "it": CAT_NOTES_IT}.get(loc, CAT_NOTES_EN)
    wall = _wall(key, notes)
    _fig_off, fig_sheet, _fig_vol, fig_zoek = _shots(key)
    dest = p["dest_label"]
    if loc == "de":
        topic = "was es ist und welche Kategorien du findest"
        body = f"""
<section class="sec sec--first"><div class="wrap"><div class="split"><div>
<span class="eyebrow" style="color:var(--acc)">Der Katalog</span>
<h1>Was BBDBuy Spreadsheet ist, und was du darin findest</h1>
<p class="lead">Ein Katalog aus Produktkarten, keine Excel-Datei. Dreiunddreißig Kategorien, Filter, Foto, Marke und der Link für den Agenten.</p>
</div>{fig_sheet}</div></div></section>
<section class="sec sec--tint"><div class="wrap"><div class="split split--rev"><div>
<h2>Warum ein eigener Katalog</h2>
<p>Die Suche eines Agenten gibt den ganzen chinesischen Bestand, riesig und oft auf Chinesisch. Ein Katalog hat die Hausaufgaben schon gemacht: jemand hat gewählt, welche Karten sich lohnen, sie in Kategorien gelegt und den Shop-Link bereitgelegt.</p>
<p>In der Praxis: du findest die Karte auf w2clinks, kopierst den Quellenlink und fügst ihn in die Suche von BBDBuy oder ins manuelle Formular ein. Der Katalog kassiert nichts und verkauft nichts.</p>
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
<p>Drei Kategorien mit Extra-Bedingungen: Elektronik (oft Lithium), Brillen (zerbrechlich) und alles mit Akku oder Magnet. Nicht jede Linie nach Deutschland nimmt das. Schätzer prüfen, bevor sie im Lager liegen bleiben.</p>
</div></section>
<section class="sec"><div class="wrap">
<h2>Unbequemes Faktum: der Katalog sucht auf Englisch</h2>
<p>Wir haben es Wort für Wort am {escape(DATE)} nachgeprüft. Deutsche Schreibweisen wie Turnschuhe, Pullover oder Brille liefern oft null. Die englischen Keys sneakers, hoodie, jacket, trousers, bag, glasses oder watch liefern Seiten.</p>
</div></section>
<section class="sec sec--tint"><div class="wrap">
<h2>Vom Katalog zur Bestellung, ohne den Link zu verlieren</h2>
<p class="lead">Die Karte ist der Anfang, nicht die Kasse. Der Schritt, der am häufigsten schiefläuft: du kopierst die Katalog-URL statt des Shop-Links. BBDBuy braucht den Taobao-, 1688- oder Weidian-Link.</p>
<p>Liest die Suche den Link nicht, bleibt das manuelle Formular. Karten ohne Preis überspringen — der Quellenlink ist in China oft schon tot.</p>
</div></section>
"""
    elif loc == "it":
        topic = "cos’è e quali categorie trovi"
        body = f"""
<section class="sec sec--first"><div class="wrap"><div class="split"><div>
<span class="eyebrow" style="color:var(--acc)">Il catalogo</span>
<h1>Che cos’è BBDBuy Spreadsheet, e cosa ci trovi</h1>
<p class="lead">Un catalogo di schede prodotto, non un file Excel. Trentatré categorie, filtri, foto, marca e il link per l’agente.</p>
</div>{fig_sheet}</div></div></section>
<section class="sec sec--tint"><div class="wrap"><div class="split split--rev"><div>
<h2>Perché un catalogo a parte</h2>
<p>La ricerca dell’agente restituisce tutto lo stock cinese, enorme e spesso in cinese. Un catalogo ha già fatto il lavoro: qualcuno ha scelto quali schede valgono, le ha messe in categoria e ha pronto il link del negozio.</p>
<p>In pratica: trovi la scheda su w2clinks, copi il link sorgente e lo incolli nella ricerca di BBDBuy o nel modulo manuale. Il catalogo non incassa e non vende.</p>
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
<section class="sec"><div class="wrap">
<h2>Dato scomodo: il catalogo cerca in inglese</h2>
<p>L’abbiamo verificato termine per termine il {escape(DATE)}. Grafie locali come scarpe, felpa o occhiali danno spesso zero. Le key inglesi sneakers, hoodie, jacket, trousers, bag, glasses o watch danno pagine.</p>
</div></section>
<section class="sec sec--tint"><div class="wrap">
<h2>Dal catalogo all’ordine, senza perdere il link</h2>
<p class="lead">La scheda è l’inizio, non la cassa. Il passo che fallisce più spesso: copi l’URL della scheda catalogo invece del link negozio. A BBDBuy serve il link Taobao, 1688 o Weidian.</p>
<p>Se la ricerca non legge il link, resta il modulo manuale. Schede senza prezzo: saltale — il link sorgente in Cina è spesso già morto.</p>
</div></section>
"""
    else:
        topic = "what it is and which categories you will find"
        body = f"""
<section class="sec sec--first"><div class="wrap"><div class="split"><div>
<span class="eyebrow" style="color:var(--acc)">The catalogue</span>
<h1>What BBDBuy Spreadsheet is, and what you find in it</h1>
<p class="lead">It is a catalogue of product cards, not an Excel file. Thirty-three categories, filters, and cards with a photo, a brand and the link for the agent.</p>
</div>{fig_sheet}</div></div></section>
<section class="sec sec--tint"><div class="wrap"><div class="split split--rev"><div>
<h2>Why a separate catalogue</h2>
<p>An agent search bar returns the whole stock of Chinese shops, huge and often in Chinese. A catalogue does the homework: someone already picked which fiches are worth it, put them in a category and left the shop link ready.</p>
<p>In practice: you find the fiche on w2clinks, copy the source link and paste it into BBDBuy search or the manual form. The catalogue collects no money and sells nothing.</p>
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
<section class="sec"><div class="wrap">
<h2>Uncomfortable fact: the catalogue searches in English</h2>
<p>We checked it term by term on {escape(DATE)}. Local spellings often returned zero. The English keys sneakers, hoodie, jacket, trousers, bag, glasses or watch returned pages of fiches. That is why the homepage search bar still sends English keys to w2clinks.</p>
</div></section>
<section class="sec sec--tint"><div class="wrap">
<h2>From catalogue to order, without losing the link</h2>
<p class="lead">The fiche is the start, not checkout. The step that fails most often is copying the catalogue URL instead of the shop link. BBDBuy needs the Taobao, 1688 or Weidian link.</p>
<p>If search does not read the link, the manual form remains. Skip cards without a price — that source link is often already dead in China.</p>
</div></section>
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
    html_f = _faq_html(pairs, open_first=True)
    fig_off, *_ = _shots(key)
    loc = p["loc"]
    if loc == "de":
        topic = "Hilfe und häufige Fragen"
        body = f"""
<article class="pw">
  <span class="eyebrow" style="color:var(--acd)">Hilfe</span>
  <h1>Hilfe und Fragen zu BBDBuy in Deutschland</h1>
  <p class="lead">Fragen erster Bestellungen. Die Lieferadresse ist eine {escape(p["postal"])}.</p>
  {fig_off}{html_f}
  <p><a class="btn" href="{escape(EST)}">Offizielle BBDBuy-Site</a>
     <a class="btn btn--ghost" href="{escape(p["ship"])}">Versandplan</a></p>
</article>
"""
    elif loc == "it":
        topic = "aiuto e domande frequenti"
        body = f"""
<article class="pw">
  <span class="eyebrow" style="color:var(--acd)">Aiuto</span>
  <h1>Aiuto e domande su BBDBuy in Italia</h1>
  <p class="lead">Domande dei primi ordini. L’indirizzo è una {escape(p["postal"])}.</p>
  {fig_off}{html_f}
  <p><a class="btn" href="{escape(EST)}">Sito ufficiale BBDBuy</a>
     <a class="btn btn--ghost" href="{escape(p["ship"])}">Piano spedizione</a></p>
</article>
"""
    else:
        topic = "help and frequently asked questions"
        body = f"""
<article class="pw">
  <span class="eyebrow" style="color:var(--acd)">Help</span>
  <h1>Help and questions about BBDBuy in {escape(p["dest_label"])}</h1>
  <p class="lead">Questions that come back on first orders. The delivery address uses a {escape(p["postal"])}.</p>
  {fig_off}{html_f}
  <p><a class="btn" href="{escape(EST)}">Official BBDBuy site</a>
     <a class="btn btn--ghost" href="{escape(p["ship"])}">Shipping plan</a></p>
</article>
"""
    return cms_shell(
        desk, page_title(desk, topic),
        f"FAQ about BBDBuy from {p['dest_label']}.",
        f"https://{p['host']}{p['help']}", [faq_ld(p["lang"], pairs)], body, p["help"],
    )


def build_news(key: str) -> str:
    p = PACKS[key]
    desk = desk_for(key)
    loc = p["loc"]
    if loc == "de":
        items = [
            ("Erste Runde: Estimator hinter Login",
             f"Am {DATE} öffnete https://www.bbdbuy.com/estimation ein Login, keinen Live-Preis. Keine erfundene Linie.",
             "Am Versandmorgen die offizielle Site öffnen, Ziel Germany — 德国, deutsche PLZ / Packstation."),
            ("w2clinks sucht auf Englisch",
             "sneakers, hoodie, jacket liefern Seiten; Turnschuhe oft null. Gemessen 6 Oct 2026.",
             "Englischen Key tippen oder einen Chip auf der Homepage antippen."),
            ("Volumengewicht",
             "Viele Linien nehmen das Maximum aus Waage und L×B×H/8000. Kein SKU-Preis in diesem HTML.",
             "Deine Box im offiziellen Schätzer rechnen, sobald du eingeloggt bist."),
            ("Schwester-Hosts bleiben getrennt",
             "CA, UK, US, DE und IT sind eigene Dateien. Kein 301 untereinander, kein 301 auf bbdbuyeu.net.",
             "Der Hub bbdbuyeu.net ist kein Zollgebiet."),
        ]
        h1, topic, brow = "Was wir auf der Plattform geprüft haben, mit Datum", "was wir auf der Plattform geprüft haben", "News"
        lead = "Das ist kein Firmennewsletter. Eigene Checks, mit Datum."
    elif loc == "it":
        items = [
            ("Primo giro: preventivo dietro login",
             f"Il {DATE} https://www.bbdbuy.com/estimation apriva un login, non un prezzo live. Nessuna linea inventata.",
             "La mattina della spedizione apri il sito ufficiale, destinazione Italy — 意大利, CAP italiano / Poste Italiane."),
            ("w2clinks cerca in inglese",
             "sneakers, hoodie, jacket danno pagine; grafie locali spesso zero. Misurato 6 Oct 2026.",
             "Scrivi la key inglese, o tocca un chip in homepage."),
            ("Peso volumetrico",
             "Molte linee prendono il massimo tra bilancia e L×W×H/8000. Nessun prezzo SKU in questo HTML.",
             "Calcola la tua scatola nel preventivo ufficiale quando sei loggato."),
            ("Gli host sorella restano separati",
             "CA, UK, US, DE e IT sono file distinti. Nessun 301 fra loro, nessun 301 verso bbdbuyeu.net.",
             "Il hub bbdbuyeu.net non è un territorio doganale."),
        ]
        h1, topic, brow = "Cosa abbiamo verificato sulla piattaforma, con data", "cosa abbiamo verificato sulla piattaforma", "Notizie"
        lead = "Non è una newsletter aziendale. Check nostri, con data."
    else:
        items = [
            (f"First round: official estimator opened a login wall",
             f"On {DATE} {EST} redirected to login, not a live rate. This guide does not invent a line or an amount.",
             f"Open the official site the morning you ship. Destination {p['dest_zh']}. {p['postal']}."),
            ("The w2clinks catalogue searches in English",
             "sneakers, hoodie and jacket returned pages; local spellings often returned zero. Measured 6 Oct 2026.",
             "Type the English key, or tap a chip on the homepage."),
            ("Volume weight",
             "Many lines bill the greater of scale and L×W×H/8000. No SKU price in this HTML.",
             "Run your box on the official estimator when you are logged in."),
            ("Sister country hosts stay separate",
             "Canada, UK, US, Germany and Italy on BBDBuy stay on their own hosts. None of them 301 into bbdbuyeu.net.",
             "The .net hub is not a customs territory."),
        ]
        h1, topic, brow = "What we checked on the platform, with a date", "what we checked on the platform", "News"
        lead = "This is not a company newsletter. These are our own checks, with a date."
    ld = itemlist_ld(
        url=f"https://{p['host']}{p['news']}",
        name="BBDBuy dest checks",
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
        desk, page_title(desk, topic), "Dated checks on BBDBuy.",
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
  <h1>Eine unabhängige Site über BBDBuy, auf Deutsch</h1>
  <p class="lead">BBDBuy Spreadsheet ist nicht BBDBuy. Es ist ein redaktioneller Leitfaden. bbdbuy.com und bbdbuyeu.com sind dasselbe offizielle Produkt; bbdbuyeu.net ist unser Hub, kein Zollgebiet.</p>
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
  <h1>Un sito indipendente su BBDBuy, in italiano</h1>
  <p class="lead">BBDBuy Spreadsheet non è BBDBuy. È una guida editoriale. bbdbuy.com e bbdbuyeu.com sono lo stesso prodotto ufficiale; bbdbuyeu.net è il nostro hub, non un territorio doganale.</p>
  {fig_off}
  <h2>Contatto</h2>
  <p>Ordini: sito ufficiale. Questa guida: <a href="mailto:{escape(MAIL)}">{escape(MAIL)}</a>.</p>
</article>
"""
    else:
        topic = "who we are and how to reach us"
        body = f"""
<article class="pw">
  <span class="eyebrow" style="color:var(--acd)">About us</span>
  <h1>An independent site about BBDBuy, in English</h1>
  <p class="lead">BBDBuy Spreadsheet is not BBDBuy. It is an editorial guide. bbdbuy.com and bbdbuyeu.com are the same official product; bbdbuyeu.net is our hub, not a customs territory.</p>
  {fig_off}
  <h2>How we work</h2>
  <p>Shipping figures would come from the public estimator. On {escape(DATE)} that URL opened a login wall, so this desk published no invented rate. Import points to <a href="{escape(p["customs_url"])}" rel="noopener">{escape(p["customs"])}</a>.</p>
  <h2>Contact</h2>
  <p>Orders: official BBDBuy chat. This guide: <a href="mailto:{escape(MAIL)}">{escape(MAIL)}</a>.</p>
</article>
"""
    return cms_shell(
        desk, page_title(desk, topic),
        "Independent BBDBuy guide: how we check facts.",
        f"https://{p['host']}{p['about']}", [], body, p["about"],
    )


def _inner_pages(key: str) -> dict[str, tuple[str, str, str]]:
    """href, topic, html-body for dest-local ranked inners (not OrientDig leftovers)."""
    p = PACKS[key]
    dest = p["dest_label"]
    loc = p["loc"]
    fig_off, fig_sheet, fig_vol, _fig_zoek = _shots(key)
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

    if loc == "de":
        guide_topic = "wie du die erste Bestellung aus Deutschland aufgibst"
        guide_body = f"""
<article class="pw">
  <span class="eyebrow" style="color:var(--acd)">Anleitung</span>
  <h1>Erste Bestellung bei BBDBuy, von Deutschland aus</h1>
  <p class="lead">Link kopieren, in den Agenten einfügen, Lagerfoto prüfen, bündeln, Ziel {dest_zh} wählen. Die Lieferadresse ist eine {fp}.</p>
  {fig_off}
  <h2>1. Karte auf w2clinks öffnen</h2>
  <p>Eine der dreiunddreißig Kategorien, Foto und Shop-Link. Das ist der Katalog, keine Excel-Datei.</p>
  {fig_sheet}
  <h2>2. Auf der offiziellen Site einfügen</h2>
  <p>Zahlung und Tickets bleiben auf {official}. Dieser Desk sieht dein Konto nicht.</p>
  <h2>3. Foto, dann bündeln, dann senden</h2>
  <p>Am {escape(DATE)} öffnete der öffentliche Schätzer ein Login, keinen Live-Preis. Keine erfundene Lagerfrist, keine erfundene Linie.</p>
  <h2>Neun Status, drei Bildschirme</h2>
  <p>Zuerst Produkt plus Inlandsweg bis zum Lager. International später. «Warum steht es still?» heißt fast immer: falscher Bildschirm — Bestellungen, dann Lager, dann Paket.</p>
  <h2>Erste Haul: flach zuerst</h2>
  <p>T-Shirts, Shorts, Schmuck für die erste Runde. Daune, Taschen, Mützen für die zweite. Elektronik oft Lithium: Linie auf der offiziellen Site prüfen.</p>
  <p><a class="btn" href="{guide}">Anleitung</a> <a class="btn btn--ghost" href="{ship}">Versandplan</a></p>
</article>
"""
        ship_topic = "Versand und Zoll aus Deutschland"
        ship_body = f"""
<article class="pw">
  <span class="eyebrow" style="color:var(--acd)">Versand</span>
  <h1>Versand nach Deutschland: Schätzer, Volumen, Zoll</h1>
  <p class="lead">Ziel {dest_zh}, nicht EU und nicht AT. Die Lieferadresse ist eine {fp}.</p>
  {fig_off}
  <h2>Der öffentliche Schätzer war hinter Login</h2>
  <p>Am {escape(DATE)} öffnete {est} ein Login, keinen Live-Preis. Dieser Desk erfindet keine Linie, keine Transitzeit und keinen Eurobetrag. Quelle: <a href="{customs_url}" rel="noopener">{customs}</a>.</p>
  <h2>Waage gegen Volumen</h2>
  <p>Viele Linien rechnen das Maximum aus Waage und L×B×H (cm) / 8000. Beispiel: 40×40×3 cm sind 4800 cm³, geteilt durch 8000 sind 600 g Volumen bei 200 g Echtgewicht. Kein SKU-Preis in diesem HTML.</p>
  {fig_vol}
  <h2>Bündeln ist kein Zolltrick auf dieser Seite</h2>
  <p>Mehrere Lagerpositionen in einem Karton können Gebühren sparen. Was du dem Zoll angibst, steht in der offiziellen Sendung, nicht auf dieser Seite.</p>
  <h2>Restricted ist keine Zollnachricht</h2>
  <p>Karten ohne Preis oder ein manuelles Formular heißen: der Quellenlink ist über den Agenten nicht kaufbar. Tabak, Alkohol und Arzneimittel reisen nicht.</p>
  <p><a class="btn" href="{est}">Offizielle BBDBuy-Site</a> <a class="btn btn--ghost" href="{help_h}">Hilfe</a></p>
</article>
"""
        legit_topic = "ist BBDBuy ein echter Agent aus Deutschland"
        legit_body = f"""
<article class="pw">
  <span class="eyebrow" style="color:var(--acd)">Check</span>
  <h1>Ist BBDBuy ein echter Einkaufsagent?</h1>
  <p class="lead">bbdbuy.com und bbdbuyeu.com sind dasselbe offizielle Produkt. bbdbuyeu.net ist unser Hub, kein Zollgebiet. Dieser Desk ist nicht BBDBuy.</p>
  {fig_off}
  <p>Am {escape(DATE)} war der öffentliche Schätzer hinter Login. Wir erfinden deshalb keine Lagerfrist und keinen Tarif. Bestellungen nur über {official}.</p>
  <p>Die Lieferadresse auf diesem Dest ist eine {fp}.</p>
  <p><a class="btn" href="{guide}">Anleitung</a> <a class="btn btn--ghost" href="{help_h}">Hilfe</a></p>
</article>
"""
        coup_topic = "Gutscheine stehen auf der offiziellen Site"
        coup_body = f"""
<article class="pw">
  <span class="eyebrow" style="color:var(--acd)">Codes</span>
  <h1>Gutscheine: nicht im Titel dieses Dest</h1>
  <p class="lead">Dieser Dest druckt keine Einladungscodes in Titel oder Homepage. Wenn BBDBuy einen Code veröffentlicht, steht er nach dem Login auf {official}.</p>
  {fig_off}
  <p>Die Lieferadresse bleibt eine {fp}. Ziel im Schätzer: {dest_zh}.</p>
  <p><a class="btn" href="{official}">Offizielle Site</a> <a class="btn btn--ghost" href="{catalog}">Katalog</a></p>
</article>
"""
        sheet_topic = "der Katalog und wie du ihn von Deutschland aus nutzt"
        sheet_body = f"""
<article class="pw">
  <span class="eyebrow" style="color:var(--acd)">Spreadsheet</span>
  <h1>BBDBuy Spreadsheet ist ein Katalog, keine Tabelle</h1>
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
  <h1>Primo ordine BBDBuy, dall’Italia</h1>
  <p class="lead">Copi il link, lo incolli nell’agente, controlli la foto di magazzino, consolidi, scegli destinazione {dest_zh}. L’indirizzo è una {fp}.</p>
  {fig_off}
  <h2>1. Apri una scheda su w2clinks</h2>
  <p>Una delle trentatré categorie, foto e link del negozio. È un catalogo, non un file Excel.</p>
  {fig_sheet}
  <h2>2. Incolla sul sito ufficiale</h2>
  <p>Pagamenti e ticket restano su {official}. Questa guida non vede il tuo account.</p>
  <h2>3. Foto, poi consolida, poi spedisci</h2>
  <p>Il {escape(DATE)} il preventivo pubblico apriva un login, non un prezzo live. Nessuna giacenza inventata, nessuna linea inventata.</p>
  <h2>Nove stati, tre schermate</h2>
  <p>Prima il prodotto più il trasporto interno fino al magazzino. L’internazionale dopo. «Perché è fermo?» quasi sempre: schermata sbagliata — ordini, poi magazzino, poi pacco.</p>
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
  <h2>Il preventivo pubblico era dietro login</h2>
  <p>Il {escape(DATE)} {est} apriva un login, non un prezzo live. Questa guida non inventa una linea, un transito né un importo. Fonte: <a href="{customs_url}" rel="noopener">{customs}</a>.</p>
  <h2>Bilancia contro volume</h2>
  <p>Molte linee fatturano il massimo tra bilancia e L×W×H (cm) / 8000. Esempio: 40×40×3 cm sono 4800 cm³, divisi per 8000 sono 600 g di volume a 200 g reali. Nessun prezzo SKU in questo HTML.</p>
  {fig_vol}
  <h2>Consolidare non è una guida doganale</h2>
  <p>Più pezzi in un cartone possono ridurre le riga di nolo. Cosa dichiari in dogana sta sulla spedizione ufficiale, non in questa pagina.</p>
  <h2>Restricted non è un avviso di dogana</h2>
  <p>Schede senza prezzo o un modulo manuale significano: il link sorgente non è acquistabile tramite l’agente. Tabacco, alcol e farmaci non viaggiano.</p>
  <p><a class="btn" href="{est}">Sito ufficiale BBDBuy</a> <a class="btn btn--ghost" href="{help_h}">Aiuto</a></p>
</article>
"""
        legit_topic = "BBDBuy è un agente vero dall’Italia"
        legit_body = f"""
<article class="pw">
  <span class="eyebrow" style="color:var(--acd)">Check</span>
  <h1>BBDBuy è un agente d’acquisto vero?</h1>
  <p class="lead">bbdbuy.com e bbdbuyeu.com sono lo stesso prodotto ufficiale. bbdbuyeu.net è il nostro hub, non un territorio doganale. Questo dest non è BBDBuy.</p>
  {fig_off}
  <p>Il {escape(DATE)} il preventivo pubblico era dietro login. Per questo non inventiamo giacenza né tariffa. Ordini solo su {official}.</p>
  <p>L’indirizzo su questo dest è una {fp}.</p>
  <p><a class="btn" href="{guide}">Guida</a> <a class="btn btn--ghost" href="{help_h}">Aiuto</a></p>
</article>
"""
        coup_topic = "i coupon stanno sul sito ufficiale"
        coup_body = f"""
<article class="pw">
  <span class="eyebrow" style="color:var(--acd)">Codici</span>
  <h1>Coupon: non nel titolo di questo dest</h1>
  <p class="lead">Questo dest non stampa codici invito nel titolo o in homepage. Se BBDBuy pubblica un codice, sta dopo il login su {official}.</p>
  {fig_off}
  <p>L’indirizzo resta una {fp}. Destinazione nel preventivo: {dest_zh}.</p>
  <p><a class="btn" href="{official}">Sito ufficiale</a> <a class="btn btn--ghost" href="{catalog}">Catalogo</a></p>
</article>
"""
        sheet_topic = "il catalogo e come lo usi dall’Italia"
        sheet_body = f"""
<article class="pw">
  <span class="eyebrow" style="color:var(--acd)">Spreadsheet</span>
  <h1>BBDBuy Spreadsheet è un catalogo, non una griglia</h1>
  <p class="lead">Schede con foto, marca e link negozio. Trentatré categorie come su w2clinks.</p>
  {fig_sheet}
  <p>Cerca in inglese (sneakers, hoodie, jacket). L’indirizzo su questo dest è una {fp}.</p>
  <p><a class="btn" href="{catalog}">Apri il catalogo</a> <a class="btn btn--ghost" href="{guide}">Guida</a></p>
</article>
"""
    else:
        guide_topic = f"how you place the first order from {dest}"
        guide_body = f"""
<article class="pw">
  <span class="eyebrow" style="color:var(--acd)">Guide</span>
  <h1>First BBDBuy order, from {dest_e}</h1>
  <p class="lead">Copy the shop link, paste it into the agent, check the warehouse photo, consolidate, then pick destination {dest_zh}. The delivery address uses a {fp}.</p>
  {fig_off}
  <h2>1. Open a card on w2clinks</h2>
  <p>One of the thirty-three categories, a photo and the shop link. That is the catalogue, not an Excel file.</p>
  {fig_sheet}
  <h2>2. Paste it on the official site</h2>
  <p>Payment and tickets stay on {official}. This desk cannot see your account.</p>
  <h2>3. Photo, then consolidate, then ship</h2>
  <p>On {escape(DATE)} the public estimator opened a login wall, not a live rate. This desk does not invent a free-storage day count or a line.</p>
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
  <p class="lead">Pick destination {dest_zh} in the official estimator when you are logged in. The delivery address uses a {fp}.</p>
  {fig_off}
  <h2>The public estimator was behind a login wall</h2>
  <p>On {escape(DATE)} {est} opened a login, not a live rate. This desk does not invent a line, a transit-day count or a money amount. Import: <a href="{customs_url}" rel="noopener">{customs}</a>.</p>
  <h2>Scale versus volume</h2>
  <p>Many lines bill the greater of scale and L×W×H (cm) / 8000. Example: 40×40×3 cm is 4800 cm³, divided by 8000 is 600 g volume at 200 g real weight. No SKU price in this HTML.</p>
  {fig_vol}
  <h2>Consolidation is not a customs tutorial</h2>
  <p>Several warehouse items in one box can cut the number of international lines. What you declare to customs is on the official shipment, not on this page.</p>
  <h2>Restricted is not a customs notice</h2>
  <p>Cards without a price, or a manual form, mean the source link is not buyable through the agent. Tobacco, alcohol and medicines do not travel.</p>
  <p><a class="btn" href="{est}">Official BBDBuy site</a> <a class="btn btn--ghost" href="{help_h}">Help</a></p>
</article>
"""
        legit_topic = f"is BBDBuy a real agent from {dest}"
        legit_body = f"""
<article class="pw">
  <span class="eyebrow" style="color:var(--acd)">Check</span>
  <h1>Is BBDBuy a real purchasing agent?</h1>
  <p class="lead">bbdbuy.com and bbdbuyeu.com are the same official product. bbdbuyeu.net is our hub, not a customs territory. This dest is not BBDBuy.</p>
  {fig_off}
  <p>On {escape(DATE)} the public estimator was behind login. That is why this desk publishes no invented storage window and no invented tariff. Orders only through {official}.</p>
  <p>The delivery address on this dest uses a {fp}.</p>
  <p><a class="btn" href="{guide}">Guide</a> <a class="btn btn--ghost" href="{help_h}">Help</a></p>
</article>
"""
        coup_topic = "coupons live on the official site"
        coup_body = f"""
<article class="pw">
  <span class="eyebrow" style="color:var(--acd)">Codes</span>
  <h1>Coupons: not in this dest title</h1>
  <p class="lead">This dest does not print invite codes in the title or on the homepage. If BBDBuy publishes a code, it lives on {official} after you log in.</p>
  {fig_off}
  <p>The delivery address still uses a {fp}. Estimator destination: {dest_zh}.</p>
  <p><a class="btn" href="{official}">Official site</a> <a class="btn btn--ghost" href="{catalog}">Catalogue</a></p>
</article>
"""
        sheet_topic = f"the catalogue and how you use it from {dest}"
        sheet_body = f"""
<article class="pw">
  <span class="eyebrow" style="color:var(--acd)">Spreadsheet</span>
  <h1>BBDBuy Spreadsheet is a catalogue, not a grid</h1>
  <p class="lead">Cards with a photo, a brand and the shop link. Thirty-three categories, the same wall as w2clinks.</p>
  {fig_sheet}
  <p>Search in English (sneakers, hoodie, jacket). The delivery address on this dest uses a {fp}.</p>
  <p><a class="btn" href="{catalog}">Open the catalogue</a> <a class="btn btn--ghost" href="{guide}">Guide</a></p>
</article>
"""
    return {
        "guide": (p["guide"], guide_topic, guide_body),
        "ship": (p["ship"], ship_topic, ship_body),
        "legit": ("/is-bbdbuy-legit/", legit_topic, legit_body),
        "coupons": ("/bbdbuy-coupons/", coup_topic, coup_body),
        "spreadsheet": ("/bbdbuy-spreadsheet/", sheet_topic, sheet_body),
        **(
            {"serioes": ("/ist-bbdbuy-serioes/", legit_topic, legit_body)}
            if loc == "de"
            else {}
        ),
    }


def build_inner(key: str, name: str) -> str:
    p = PACKS[key]
    desk = desk_for(key)
    href, topic, body = _inner_pages(key)[name]
    return cms_shell(
        desk, page_title(desk, topic),
        f"Independent BBDBuy {name} for {p['dest_label']}.",
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
    }
    err = [e for e in validate_desk(html, _facts(key), page=page) if e not in skip]
    if page == "home":
        err = [e for e in err if not e.startswith("faq count")]
        if page_title(desk, p["home_topic"]) not in html:
            err.append("home title")
        if p["fingerprint"] not in html:
            err.append("fingerprint")
        if "not an Excel file" not in html and "keine Excel-Datei" not in html and "non è un file Excel" not in html:
            err.append("sheet-explain")
        if "cat-30-shoes.png" not in html or "w2clinks.com/spreadsheet/bbdbuy" not in html:
            err.append("W2C cats")
        if MAIL not in html:
            err.append("footer mail")
        if 'id="local"' in html or "/api/products/" in html:
            err.append("ops dump")
        if 'class="fig"' not in html:
            err.append("photos")
        for sid in ("shots", "states", "restricted"):
            if f'id="{sid}"' not in html:
                err.append(f"missing #{sid}")
        if p["loc"] != "en" and "Official bbdbuy.com, 6 Oct" in html:
            err.append("english fig caption")
        for alien in p["aliens"]:
            if alien in html:
                err.append(f"alien {alien}")
        for tok in INVITES:
            if tok in html:
                err.append(f"invite {tok}")
    if page == "help" and p["fingerprint"] not in html:
        err.append("help fingerprint")
    if page in ("guide", "ship", "legit", "coupons", "spreadsheet", "serioes"):
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


def _copy_assets(dest: Path) -> None:
    img = dest / "img"
    (img / "shots").mkdir(parents=True, exist_ok=True)
    (dest / "assets" / "images").mkdir(parents=True, exist_ok=True)
    (dest / "assets" / "css").mkdir(parents=True, exist_ok=True)
    shutil.copy(ASSETS / "bbdbuy-logo.png", dest / "assets" / "images" / "bbdbuy-logo.png")
    shutil.copy(ASSETS / "hero.jpg", img / "hero.jpg")
    shutil.copy(ASSETS / "favicon.ico", dest / "favicon.ico")
    shutil.copy(ASSETS / "favicon1.ico", dest / "favicon1.ico")
    for name in ("oficial.jpg", "catalogus.jpg", "catalogus-zoek.jpg", "volume-voorbeeld.jpg"):
        shutil.copy(ASSETS / "shots" / name, img / "shots" / name)


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
    theme = OUT / "shared" / "themes" / "bbdbuy-theme.css"
    theme.parent.mkdir(parents=True, exist_ok=True)
    theme.write_text(
        "/* BBDBuy country dest — official orange from bbdbuy.com wordmark */\n"
        ":root { --primary: #F0700C; --primary-dark: #C45A0A; --primary-soft: #fff1e6; --nav-dark: #111111; }\n",
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
    out: dict[str, Path] = {"css": css_path, "logo": dest / "assets" / "images" / "bbdbuy-logo.png"}
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
    _run(client, f"cp -a '{gsc}' '/www/backup/bbdbuy-{key}-gsc-about-{stamp}.conf'")
    Path(f"/tmp/bbdbuy-{key}-gsc.conf").write_text("".join(keep), encoding="utf-8")
    sftp.put(f"/tmp/bbdbuy-{key}-gsc.conf", gsc)
    print(key, "stripped", stripped, "CMS-page home 301s")
    _reload_nginx(client)


def _map_legacy_english_cms(client, sftp, key: str) -> None:
    """DE/IT: 301 leftover English CMS slugs to dest slugs; drop OrientDig /about/ files."""
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
    seen: set[str] = set()
    out: list[str] = []
    loc_re = re.compile(r"^\s*location\s+=\s+(\S+)\s*\{")
    for ln in (raw or "").splitlines(True):
        m = loc_re.match(ln)
        if m and m.group(1) in wanted:
            path = m.group(1)
            if path in seen:
                continue
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
    _run(client, f"mkdir -p /www/backup; cp -a '{gsc}' '/www/backup/bbdbuy-{key}-gsc-legacy-{stamp}.conf' 2>/dev/null || true")
    Path(f"/tmp/bbdbuy-{key}-gsc-legacy.conf").write_text(new, encoding="utf-8")
    sftp.put(f"/tmp/bbdbuy-{key}-gsc-legacy.conf", gsc)
    print(key, "legacy CMS 301s", " ".join(f"{a}->{b}" for a, b in wanted.items()))
    _reload_nginx(client)
    if dropped:
        print(key, "dropped leftover English CMS dirs", dropped)


def _harden_catchall(client, sftp, key: str) -> None:
    host = PACKS[key]["host"]
    vhost = f"/www/server/panel/vhost/nginx/{host}.conf"
    with sftp.open(vhost, "r") as fh:
        text = fh.read().decode()
    marker = f'X-Desk "bbdbuy-{key}-independent"'
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
        add_header X-Desk "bbdbuy-{key}-independent" always;
    }}
"""
    if old not in text:
        print(key, "catch-all needle not the plain try_files; skip harden")
        return
    stamp = time.strftime("%Y%m%d-%H%M%S")
    _run(client, f"cp -a '{vhost}' '/www/backup/bbdbuy-{key}-nginx-{stamp}.conf'")
    text = text.replace(old, new, 1)
    tmp = Path(f"/tmp/bbdbuy-{key}.conf")
    tmp.write_text(text, encoding="utf-8")
    sftp.put(str(tmp), vhost)
    print(key, "hardened HTTPS catch-all")
    _reload_nginx(client)


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
            _run(client, f"cp -a '{vhost}' '/www/backup/bbdbuy-twin-{twin}-{stamp}.conf'")
            raw = raw.replace(old, want).replace(old2, want)
            Path(f"/tmp/bbdbuy-twin-{twin}.conf").write_text(raw, encoding="utf-8")
            sftp.put(f"/tmp/bbdbuy-twin-{twin}.conf", vhost)
            print("twin catch-all now $request_uri", twin)
        else:
            print("WARN twin catch-all needle missing", twin)
        gsc = f"/www/server/panel/vhost/nginx/extension/{twin}/gsc-redirects.conf"
        graw = _run(client, f"cat '{gsc}' 2>/dev/null || true")
        if graw and f"https://{twin}" in graw:
            _run(client, f"cp -a '{gsc}' '/www/backup/bbdbuy-twin-gsc-{twin}-{stamp}.conf'")
            graw = graw.replace(f"https://{twin}", f"https://{target}")
            Path(f"/tmp/bbdbuy-twin-gsc-{twin}.conf").write_text(graw, encoding="utf-8")
            sftp.put(f"/tmp/bbdbuy-twin-gsc-{twin}.conf", gsc)
            print("retargeted twin gsc host", twin, "->", target)
            graw = _run(client, f"cat '{gsc}'")
        extra = TWIN_EXTRA.get(twin) or []
        add = []
        for src, dest in extra:
            line = f"location = {src} {{ return 301 https://{target}{dest}; }}"
            line2 = f"location = {src}/ {{ return 301 https://{target}{dest}; }}"
            if line not in graw:
                add.append(line + "\n" + line2 + "\n")
        if add:
            _run(client, f"cp -a '{gsc}' '/www/backup/bbdbuy-twin-gsc-extra-{twin}-{stamp}.conf'")
            Path(f"/tmp/bbdbuy-twin-gsc-{twin}.conf").write_text(graw + "\n" + "".join(add), encoding="utf-8")
            sftp.put(f"/tmp/bbdbuy-twin-gsc-{twin}.conf", gsc)
            print("appended", len(add), "twin path maps", twin)
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
  <p class="lead">Die alte Fassung gehörte nicht zu BBDBuy. Die aktuelle Anleitung steht auf Start. Die Lieferadresse ist eine {fp}.</p>
  <p><a class="btn" href="/start/">Start</a> <a class="btn btn--ghost" href="{escape(p['guide'])}">Anleitung</a></p>
</article>
"""
    elif loc == "it":
        topic = "questo articolo è stato sostituito"
        body = f"""
<article class="pw">
  <h1>Questo articolo è stato sostituito</h1>
  <p class="lead">La versione precedente non era di BBDBuy. La guida attuale sta su Start. L’indirizzo è una {fp}.</p>
  <p><a class="btn" href="/start/">Start</a> <a class="btn btn--ghost" href="{escape(p['guide'])}">Guida</a></p>
</article>
"""
    else:
        topic = "this article was replaced"
        body = f"""
<article class="pw">
  <h1>This article was replaced</h1>
  <p class="lead">The previous version was not a BBDBuy dest page. The current guide is on Start. The delivery address uses a {fp}.</p>
  <p><a class="btn" href="/start/">Start</a> <a class="btn btn--ghost" href="{escape(p['guide'])}">Guide</a></p>
</article>
"""
    return cms_shell(
        desk, page_title(desk, topic),
        f"Replaced leftover article on {p['host']}.",
        f"https://{p['host']}{href}", [], body, href,
    )


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
        if any(tok in raw.lower() for tok in WRAP_POISON):
            out = _retire_poison(key, href)
            why = "retire-poison"
            print("retire poison", rel)
        else:
            out, why = cms_wrap_inner(desk, raw, href)
            if out is None:
                print("inner", rel, why)
                continue
        min_b = 4000
        for prefix, floor in mins.items():
            if rel.startswith(prefix.lstrip("/")):
                min_b = floor
                break
        if why != "retire-poison" and len(out.encode("utf-8")) < min_b:
            print("WARN skip thin wrap", rel, len(out.encode("utf-8")))
            continue
        rel_dir = str(Path(rel).parent)
        _run(client, f"mkdir -p '{bak}/{rel_dir}'")
        _run(client, f"cp -a '{remote}' '{bak}/{rel}'")
        local_tmp = Path("/tmp") / f"bbd-wrap-{key}-{rel.replace('/', '_')}"
        local_tmp.write_text(out, encoding="utf-8")
        sftp.put(str(local_tmp), remote)
        print("WRAP", rel, "in", len(raw), "out", len(out.encode("utf-8")))


def put(key: str) -> None:
    if PACKS[key]["host"] == HUB:
        raise SystemExit("refusing to PUT hub bbdbuyeu.net")
    files = generate(key)
    p = PACKS[key]
    host = p["host"]
    client = _connect()
    stamp = time.strftime("%Y%m%d-%H%M%S")
    bak = f"/www/backup/bbdbuy-{key}-cms-{stamp}"
    root = f"/www/wwwroot/{host}"
    overlay = _overlay(key)
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
    theme = OUT / "shared" / "themes" / "bbdbuy-theme.css"
    sftp.put(str(theme), f"{root}/assets/css/bbdbuy-theme.css")
    sftp.put(str(files["css"]), f"{root}/assets/css/{p['desk_css']}")
    sftp.put(str(overlay / "assets" / "images" / "bbdbuy-logo.png"), f"{root}/assets/images/bbdbuy-logo.png")
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
            url, headers={"User-Agent": "bbdbuy-cms/1.0", "Cache-Control": "no-cache"},
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
            (f"https://{host}/is-bbdbuy-legit/", "legit", False),
            (f"https://{host}/bbdbuy-coupons/", "coupons", False),
        ]
        for url, kind, need_fp in checks:
            follow = kind in ("home", "start", "guide", "ship", "legit", "coupons")
            code, final, loc, body = fetch(url, follow=follow)
            html = body.decode("utf-8", "replace")
            print(k, kind, code, "bytes", len(body), "loc", loc or final)
            if HUB in (final or "") or HUB in (loc or ""):
                if host != HUB:
                    print(" FAIL 301 into hub"); fail += 1
            sisters = [h for h in dest_hosts if h != host]
            if any(s in (final or "") or s in (loc or "") for s in sisters):
                print(" FAIL 301 into sister dest"); fail += 1
            if kind not in ("404",) and code != 200:
                print(" FAIL status"); fail += 1
            if "orientdig" in html.lower() or "warum sollte ich lieferungen" in html.lower():
                print(" FAIL orientdig leftover"); fail += 1
            for tok in INVITES:
                if tok in html:
                    print(" FAIL invite"); fail += 1
            if "bbdbuy-logo.png" not in html:
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
                for sid in ("shots", "states", "restricted"):
                    if f'id="{sid}"' not in html:
                        print(" FAIL missing #", sid, sep=""); fail += 1
                if p["loc"] != "en" and "Official bbdbuy.com, 6 Oct" in html:
                    print(" FAIL english fig caption"); fail += 1
            if kind in ("guide", "ship"):
                mark = {
                    "de": ("Erste Bestellung bei BBDBuy" if kind == "guide" else "Versand nach Deutschland"),
                    "it": ("Primo ordine BBDBuy" if kind == "guide" else "Spedire in Italia"),
                }.get(p["loc"], ("First BBDBuy order" if kind == "guide" else "Shipping to"))
                if mark not in html:
                    print(" FAIL", kind, "copy"); fail += 1
            if kind == "catalog" and html.count('class="cat"') < 30:
                print(" FAIL catalog wall"); fail += 1
            if kind == "news" and "ItemList" not in html:
                print(" FAIL news ItemList"); fail += 1
            if kind == "about":
                mark = {
                    "de": "Eine unabhängige Site über BBDBuy",
                    "it": "Un sito indipendente su BBDBuy",
                }.get(p["loc"], "An independent site about BBDBuy")
                if mark not in html:
                    print(" FAIL about copy"); fail += 1
                if (loc or "").rstrip("/") == f"https://{host}":
                    print(" FAIL about 301 home"); fail += 1
            if kind == "help" and "FAQPage" not in html:
                print(" FAIL help FAQPage"); fail += 1
        if p["about"] != "/about/":
            code_ab, _, loc_ab, body_ab = fetch(f"https://{host}/about/", follow=False)
            print(k, "legacy about", code_ab, loc_ab)
            if code_ab not in (301, 302, 308) or p["about"].rstrip("/") not in (loc_ab or ""):
                print(" FAIL leftover /about/ not 301 to dest about"); fail += 1
            code_ab2, _, _, body_ab2 = fetch(f"https://{host}/about/", follow=True)
            html_ab = body_ab2.decode("utf-8", "replace")
            if "orientdig" in html_ab.lower() or any(tok in html_ab for tok in INVITES):
                print(" FAIL leftover /about/ still OrientDig/invite"); fail += 1
        code, _, _, nf = fetch(f"https://{host}/this-page-does-not-exist-cms/", follow=True)
        nhtml = nf.decode("utf-8", "replace")
        print(k, "404", code)
        if code != 404:
            print(" FAIL 404"); fail += 1
        if f"{p['not_found_tab']} | BBDBuy Spreadsheet" not in nhtml:
            print(" FAIL 404 title"); fail += 1
    for twin, target in TWINS.items():
        code, _, loc, _ = fetch(f"https://{twin}/", follow=False)
        print("twin", twin, code, loc)
        if code not in (301, 302, 308) or target not in (loc or ""):
            print(" FAIL twin 301"); fail += 1
        deep = f"https://{twin}/bbdbuy-shipping/" if target != HUB else f"https://{twin}/bbdbuyeu-shipping-guide/"
        code2, _, loc2, _ = fetch(deep, follow=False)
        print(" twin deep", code2, loc2)
        if code2 not in (301, 302, 308) or target not in (loc2 or ""):
            print(" FAIL twin deep"); fail += 1
        elif target != HUB and "/bbdbuy-shipping" not in (loc2 or "") and loc2.rstrip("/") == f"https://{target}":
            print(" FAIL twin deep collapsed to home"); fail += 1
    code, _, loc, _ = fetch(f"https://{HUB}/", follow=False)
    print("hub", code, loc or HUB)
    if code != 200:
        print(" FAIL hub"); fail += 1
    if any(h in (loc or "") for h in dest_hosts):
        print(" FAIL hub collapsed into dest"); fail += 1
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
        _cf_bust([PACKS[k]["host"] for k in rest] + list(TWINS))
    elif cmd == "live":
        live_check(rest[0] if len(rest) == 1 else None)
    elif cmd == "twins":
        client = _connect()
        _fix_twins(client, client.open_sftp())
        client.close()
    elif cmd == "all":
        for k in rest:
            put(k)
        client = _connect()
        _fix_twins(client, client.open_sftp())
        client.close()
        _cf_bust([PACKS[k]["host"] for k in rest] + list(TWINS))
        live_check()
    else:
        for k in rest:
            generate(k)
