#!/usr/bin/env python3
"""ACBuy Netherlands pack of the country-dest CMS template.

Chrome / IA / wrap live in tools/country_cms.py (gold IA: hipobuy.es, gold
brand: acbuy.com). This file is the first filled pack: Dutch copy, NL facts,
W2C category notes. Next dest: copy this file, swap DESK + copy builders.
Does not PUT 5KB overlays over ranked unique inners. AllChinaBuy NL
(allchinabuyspreadsheet.nl) is a different agent dest and stays independent.
"""
from __future__ import annotations

import json
import os
import re
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
    W2C_CATS,
    build_404,
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
HOST = "acbuyspreadsheets.nl"
DATE = "5 Oct 2026"
OFFICIAL = "https://www.acbuy.com/"
EST = "https://www.acbuy.com/estimation/"
HELP = "https://www.acbuy.com/help"
REG = "https://www.acbuy.com/"
ACC = "#31B38C"
ACC_DARK = "#27BA9B"
MAIL = "cnfd85269032661@gmail.com"
INVITE = "5F2RRA"
INVITE2 = "EwjrSk"
INVITE3 = "ACBUY5"
STORAGE = (
    "Officiële ACBuy Help is de live SPA "
    f"({HELP}); bevestig die tekst op de ochtend van verzenden. "
    "Deze desk verzint geen gratis-dagen-aantal."
)
DEST_MIN = 22000
CSS_V = "20261007a"
INNER_MARKER = f'data-inner-chrome="{CSS_V}-acbuy-nl"'
ALIENS = (
    "1010 Wien",
    "Packstation",
    "form A1A 1A1",
    "Poste Italiane",
    "00-001 Warszawa",
    "00100 Helsinki",
    "pas un code postal belge",
    "does not invent a de-minimis dollar",
    "Northern Ireland is often another",
    "do not copy a GST rate",
    "not a customs territory",
)

KEEP = [
    ("/is-acbuy-legit/", "Review"),
    ("/acbuy-shipping-guide/", "Verzending"),
    ("/acbuy-coupons/", "Coupons"),
    ("/how-to-use-acbuy/", "Handleiding"),
]
# hipobuy.es IA: Inicio, Guía, Spreadsheet, Envíos, Ayuda, Novedades.
# Over ons (= /sobre-nosotros) lives in the footer, not the homepage dump.
CMS_PAGES = [
    ("/start/", "Start"),
    ("/how-to-use-acbuy/", "Handleiding"),
    ("/catalogus/", "Catalogus"),
    ("/acbuy-shipping-guide/", "Verzending"),
    ("/hulp/", "Hulp"),
    ("/nieuws/", "Nieuws"),
]
RANKED = (
    ("/is-acbuy-legit/", 8000),
    ("/acbuy-shipping-guide/", 8000),
    ("/acbuy-coupons/", 8000),
    ("/acbuy-spreadsheet/", 8000),
    ("/acbuy-invite-code/", 4000),
    ("/how-to-use-acbuy/", 4000),
    ("/blog/", 4000),
)

FACTS = {
    "agent": "ACBuy",
    "host": HOST,
    "lang": "nl-NL",
    "loc": "nl",
    "dest": "NL",
    "dest_label": "Nederland",
    "ccy": "EUR",
    "storage": STORAGE,
    "estimator": EST,
    "official": OFFICIAL,
    "date": DATE,
    "keep": KEEP,
    "codes_off_title": [INVITE, INVITE2, INVITE3],
    "strict_html_codes": True,
}


def _nl_faqs() -> list[tuple[str, str]]:
    """Help answers follow homepage: catalog is w2clinks, never /api/products/."""
    pairs = []
    for q, a in long_faqs(FACTS):
        a = a.replace(
            f"De index van /api/products/ op {HOST} is Engels (sneakers, hoodie, jacket). «Sneakers» werkt; lokale woorden geven vaak 0 kaarten. Dat is geen lege shop. Gemeten {DATE}.",
            f"De catalogus van w2clinks indexeert in het Engels (sneakers, hoodie, jacket). «Sneakers» werkt; Nederlandse woorden zoals turnschoenen geven vaak 0 resultaten. Dat is geen lege winkel. Gemeten {DATE}.",
        )
        a = a.replace(
            f"De categorie-muur toont nog de Engelse keys (sneakers, hoodie, jacket) voor /api/products/ op {HOST}. Gemeten {DATE}.",
            f"De categoriekaarten op deze gids openen diezelfde Engelse keys in de ACBuy-catalogus van w2clinks. Gemeten {DATE}.",
        )
        a = a.replace(
            f"Prijs 0 op {HOST} is geen kassa.",
            "Een fiche zonder prijs in de catalogus van w2clinks of op ACBuy is geen kassa.",
        )
        a = a.replace("/api/products/", "w2clinks")
        pairs.append((q, a))
    return pairs


CAT_NOTES = {
    "SNEAKERS": "Kijk naar zool en leest op de QC-foto’s vóór je internationaal boekt: daar gaan de meeste retouren over.",
    "SLIPPERS": "Licht en plat. Goed om een doos te vullen zonder het factuurgewicht hard te laten stijgen.",
    "T-SHIRT": "De Aziatische snit valt vaak nauwer. Vergelijk de borstbreedte in centimeters, niet alleen de lettermaat.",
    "POLO": "Kijk op de QC-foto naar kraag en piqué. Die twee details wijken het vaakst af van de catalogusfoto.",
    "SHIRT": "Mouwlengte en schoudernaad op de foto met meetlint, niet op de lettermaat.",
    "SHORTS": "Licht en plat: de makkelijkste manier om een pakket te vullen zonder het factuurgewicht te laten exploderen.",
    "VEST": "Bodywarmers zijn dikker dan ze wegen. Reken het volume vóór je er een jas bijstopt.",
    "LONG SLEEVED": "Mouwlengte en manchet op de QC-foto. Aziatische lengtes vallen vaak korter.",
    "HOODIE": "Zwaar voor hun volume. Eén hoodie kan het gewichtstram van de hele doos bepalen.",
    "SWEATER": "Grammage en krimp. Meet de borst, niet alleen de labelmaat.",
    "SHAWL": "Licht, maar omvangrijk als hij niet plat gaat. Vraag plat inpakken.",
    "JACKET": "Donsjassen nemen enorm veel ruimte in. Hier wint het volumgewicht bijna altijd van de weegschaal.",
    "SHELL JACKET": "Kijk naar naden en rits op de QC-foto. Een scheurtje in de coating zie je pas dichtbij.",
    "FLEECE JACKET": "Licht van gewicht, dik van volume. Zelfde reconte als bij dons.",
    "DOWN JACKETS": "Volume wint. Eén donsjas alleen al kan een duurdere gewichtsklasse forceren.",
    "TROUSERS": "Vraag foto’s van kruishoogte en pijplengte. Het W/L-label komt niet altijd overeen met de centimeter.",
    "Jersey": "Controleer rugnummer, patches en seizoen op de foto’s: dat zijn de details die het vaakst misgaan.",
    "FEMALE STYLE": "Pasvorm is zelden unisex. Meet borst en lengte; reken niet op Europese damesmaten.",
    "Electronics": "Vaak lithium. Veel luchtlijnen weigeren ze: check de schatter vóór je bestelt.",
    "GLOVES": "Vraag een foto van het paar. Eén handschoen op de catalogusfoto zegt niets over de tweede.",
    "BAG": "Vult bijna in z’n eentje een doos. Reken het volume vóór je een tas bij kleding stopt.",
    "HAT": "Vervormbaar en volumineus. Vraag opvulling, anders komt de klep gevouwen aan.",
    "JEWELRY": "Klein en goedkoop om mee te sturen. Goed om een bijna volle doos af te ronden.",
    "UNDERWEAR": "Minder referenties dan de rest. Als je niets vindt, zoek op merk in plaats van op het woord ondergoed.",
    "BELT": "Gesp en lengte op de QC-foto. De catalogusfoto is vaak een andere kleurgesp.",
    "KNEEPAD": "Dik en volumineus. Reken L×B×H, niet alleen de weegschaal.",
    "SOCKS": "Licht. Goed vullingmateriaal, nauwelijks extra kilo.",
    "HEADGEAR": "Vormhoudend inpakken, anders komt het geplet aan.",
    "EARMUFF": "Licht van gewicht, bol van volume. Zelfde reconte als mutsen.",
    "SCARF": "Licht en plat als hij gevouwen gaat. Vraag plat inpakken.",
    "GLASSES": "Breekbaar en klein. Versterkt inpakken is de moeite, ook als het een paar gram scheelt.",
    "WATCH": "Vraag foto’s van uurwerk en sluiting. De catalogusfoto lijkt hier het minst op wat aankomt.",
    "CHILD": "Kindermaten zijn geen verkleinde volwassenenmaten. Meet, gok niet op ‘small’.",
}


def _faq_html(pairs: list[tuple[str, str]] | None = None, *, open_first: bool = True) -> str:
    items = []
    src = pairs if pairs is not None else long_faqs(FACTS)
    for i, (q, a) in enumerate(src):
        op = " open" if open_first and i == 0 else ""
        items.append(
            f'<details class="sg-faq"{op}><summary>{escape(q)}</summary><p>{escape(a)}</p></details>'
        )
    return "\n".join(items)

def _off(path: str = "") -> str:
    url = OFFICIAL.rstrip("/") + path
    sep = "&" if "?" in url else "?"
    return f"{url}{sep}utm_source={HOST}&utm_medium=referral&utm_campaign=portada"


DESK = CountryDesk(
    host=HOST,
    agent="ACBuy",
    dest="NL",
    dest_label="Nederland",
    lang="nl-NL",
    in_language="in het Nederlands",
    official=OFFICIAL,
    estimator=EST,
    help_url=HELP,
    mail=MAIL,
    acc=ACC,
    acc_dark=ACC_DARK,
    date=DATE,
    css_v=CSS_V,
    logo_src="/assets/images/acbuy-logo.svg",
    nav=list(CMS_PAGES),
    footer_intro=(
        "Onafhankelijke gids in het Nederlands over ACBuy en over hoe je de catalogus "
        "van w2clinks gebruikt om vanuit Nederland in China te kopen."
    ),
    footer_sections=[
        ("/how-to-use-acbuy/", "Handleiding van ACBuy"),
        ("/catalogus/", "Het spreadsheet en de categorieën"),
        ("/acbuy-shipping-guide/", "Verzending en douane"),
        ("/hulp/", "Hulp en vragen"),
        ("/nieuws/", "Nieuws"),
        ("/over-ons/", "Over ons"),
    ],
    footer_official=[
        (_off("/"), "ACBuy (officiële site)"),
        (_off("/register"), "Account aanmaken op ACBuy"),
        (_off("/estimation/"), "Verzendschatter"),
        (_off("/help"), "Helpcentrum"),
        (_off("/issueView"), "Officiële FAQ"),
        ("https://www.reddit.com/r/Acbuyofficial/", "Reddit officieel"),
    ],
    independence=(
        "ACBuy Spreadsheet is een onafhankelijke informatiesite. Wij zijn niet ACBuy, "
        "we verwerken geen bestellingen, we innen geen verzendkosten en we hebben geen "
        "toegang tot je account. Elke bestelling, betaling en klacht loopt via de officiële site."
    ),
    copyright="&copy; 2026 ACBuy Spreadsheet. Inhoud in het Nederlands, door mensen geredigeerd en nagekeken vóór publicatie.",
    login_label="Inloggen op ACBuy",
    menu_label="Menu openen",
    skip_lang="nl",
    not_found_h1="Deze pagina bestaat niet",
    not_found_lead="De link is misschien oud. Dit zijn de secties die wél bestaan:",
    home_cta="Terug naar de startpagina",
    theme_css="acbuy-theme.css",
    desk_css="acbuy-nl-desk.css",
    inner_marker=INNER_MARKER,
    home_href="/start/",
    reddit="https://www.reddit.com/r/Acbuyofficial/",
    register_path="/register",
    sheet_slug="acbuy",
    invites=(INVITE, INVITE2, INVITE3),
    factory_pats=(
        r"Step-by-step guide to using ACBuy:[^.<]{0,240}\.",
        r"This page is part of\s*(?:<strong>)?ACBuy Nederland(?:</strong>)?\s*\.[\s./<code>]*",
        r"Browse ACBuy Spreadsheet\s*(?:&rarr;|→)?",
    ),
    extra_subs=(
        (
            r'(?is)(<div style="max-width:720px;[^"]*">)\s*(<h1[\s\S]*?</h1>)\s*<p\b[^>]*>[\s\S]*?</p>\s*',
            r"\1\n  \2\n  ",
        ),
    ),
    strip_home_crumb="Start",
    not_found_tab="Pagina niet gevonden",
)

W2C_ACBUY_SHEET = w2c_sheet(DESK)


def _fig(src: str, alt: str, cap: str, w: int = 1200, h: int = 750) -> str:
    return cms_fig(src, alt, cap, w, h)


def _official(path: str = "") -> str:
    return official_url(DESK, path)


def _shell(title: str, desc: str, canonical: str, extra_ld: list[dict], body: str, page: str) -> str:
    return cms_shell(DESK, title, desc, canonical, extra_ld, body, page)


def wrap_inner(html: str, page_href: str) -> tuple[str | None, str]:
    return cms_wrap_inner(DESK, html, page_href)


def build_home() -> str:
    wall = "".join(
        f'<a class="cat" href="{escape(W2C_ACBUY_SHEET)}?category={quote_plus(key)}&amp;page=1&amp;sort=newest" '
        f'rel="noopener" target="_blank">'
        f'<img src="{escape(W2C)}/public/static/w2c/categories/{escape(fn)}" alt="{escape(key)}" '
        f'loading="lazy" decoding="async" width="96" height="96">'
        f'<div class="cat__b"><strong>{escape(labn)}</strong><span>{escape(key)}</span></div></a>'
        for key, labn, fn in W2C_CATS
    )
    chips = "".join(
        f'<a href="{escape(W2C_ACBUY_SHEET)}?q={quote_plus(key.lower())}&amp;utm_source={escape(HOST)}&amp;utm_medium=referral&amp;utm_campaign=hero-chips" '
        f'rel="nofollow noopener" target="_blank">{escape(key.lower() if key.isupper() else key)}</a>'
        for key, _lab, _fn in W2C_CATS[:8]
    )
    utm = f"utm_source={HOST}&amp;utm_medium=referral&amp;utm_campaign=portada-que-es"
    fig_home = _fig(
        "/img/shots/oficial-inicio.jpg",
        "Officiële ACBuy-homepage met zoekbalk, vliegtuigbanner en vier stappen: Place orders, QC&storage, Submit parcels, INTL ship",
        "De officiële homepage van acbuy.com, 5 Oct 2026. De vier stappen onder de zoekbalk zijn het hele traject: bestellen in China, QC in het magazijn, bundelen, internationaal versturen.",
    )
    fig_guide = _fig(
        "/img/shots/oficial-guidebook.jpg",
        "Officiële ACBuy GuideBook, stap 1: product kiezen via Taobao-link of via de zoekbalk",
        "GuideBook van ACBuy, stap 1. Links: link van Taobao / 1688 plakken. Rechts: zoeken in de app. Opname 5 Oct 2026.",
    )
    fig_sheet = _fig(
        "/img/shots/catalogus.jpg",
        "ACBuy-catalogus op w2clinks: productkaarten met foto, merk en referentieprijs",
        "Wat je op w2clinks ziet zijn kaarten, geen Excel-cellen. Prijzen in yuan veranderen per dag. Opname 5 Oct 2026, categorie SNEAKERS.",
        1200,
        900,
    )
    fig_pay = _fig(
        "/img/shots/oficial-guidebook-3.jpg",
        "Officiële ACBuy GuideBook, stap 3: eerste betaling van product plus binnenlands China, Checkout-knop",
        "Stap 3 van het officiële GuideBook: je betaalt eerst het product en het binnenlandse China-vervoer tot het magazijn. Internationaal zit daar niet bij. Opname 5 Oct 2026.",
    )
    fig_est = _fig(
        "/img/shots/estimator-nl.jpg",
        "Officiële ACBuy-schatter met bestemming Netherlands 荷兰, 1000 g, 35×25×10 cm, lijn Euro DHL Duty Free EC-Y",
        "Publieke schatter, bestemming Netherlands — 荷兰, 1000 g en 35×25×10 cm. 5 Oct 2026 toonde o.a. Euro DHL Duty Free EC-Y, 12–16 werkdagen. Die cijfers veranderen; open de estimator opnieuw.",
    )
    fig_vol = _fig(
        "/img/shots/volume-voorbeeld.jpg",
        "Rekenvoorbeeld volumgewicht: 40×40×3 cm en 200 g weegschaal wordt 600 g volume",
        "Rekenvoorbeeld, geen magazijnfoto. Dezelfde deler 8000 staat in de DHL-regel van de schatter. Jouw doos reken je daar, bestemming Nederland.",
        1200,
        640,
    )
    fig_diy = _fig(
        "/img/shots/oficial-diy.jpg",
        "ACBuy DIY-formulier: link, naam, specificaties, prijs in CNY, en disclaimer dat ACBuy geen eigen voorraad verkoopt",
        "DIY Order op acbuy.com. Als de zoekbalk de link niet leest, vul je het formulier handmatig. De groene disclaimer zegt het zelf: artikelen komen van derden. Opname 5 Oct 2026.",
    )
    body = f"""
<section class="hero">
  <div class="hero__bg" role="img" aria-label="Officiële ACBuy-banner: vliegtuig en zoekbalk om een Chinese productlink te plakken"></div>
  <div class="hero__scrim"></div>
  <div class="wrap">
    <span class="eyebrow">Onafhankelijke gids, in het Nederlands</span>
    <h1>ACBuy Spreadsheet: de gids om in China te kopen vanaf Nederland</h1>
    <p class="lead">Hoe je een productlink in de agent plakt, hoe de catalogus van w2clinks werkt, hoe een pakket naar Nederland reist en wat je nagaat vóór de Douane.</p>
    <div class="sbox">
      <form id="w2c-search" action="{escape(W2C_ACBUY_SHEET)}" method="get" target="_blank" rel="nofollow noopener" role="search">
        <label class="skip" for="q">Zoek producten op w2clinks</label>
        <input id="q" name="q" type="search" autocomplete="off" placeholder="Zoek sneakers, hoodie, jas…">
        <input type="hidden" name="utm_source" value="{escape(HOST)}">
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
        <p class="lead">ACBuy verkoopt zelf niets. Hij koopt voor jou in Chinese shops die niet naar het buitenland sturen, ontvangt het pakket in het magazijn, fotografeert het, bewaart het, en stuurt het naar Nederland wanneer jij dat besluit.</p>
        <p>Dat verandert alles: je betaalt twee keer (eerst het product, daarna internationaal), je wacht twee keer, en ertussen kun je nog annuleren, bundelen of van lijn wisselen. Betalen en tickets blijven op {escape(OFFICIAL)}.</p>
        <p><a class="btn" href="/how-to-use-acbuy/">Handleiding stap voor stap</a></p>
      </div>
      {fig_home}
    </div>
  </div>
</section>
<section class="sec sec--tint" id="shots">
  <div class="wrap">
    <div class="split split--rev">
      <div>
        <span class="eyebrow" style="color:var(--acd)">Zo koop je</span>
        <h2>Plak een Chinese link, of zoek in de app</h2>
        <p class="lead">Het officiële GuideBook begint hier: een link van Taobao, 1688 of Weidian plakken, of de naam in de zoekbalk typen. Dat is de hele truc van een inkoopagent — de Chinese shop ziet ACBuy, jij ziet daarna QC-foto’s en een lijn naar Nederland.</p>
        <p>Leest de zoekbalk de link niet, dan is het DIY-formulier de volgende stap: naam, maat, kleur en prijs in yuan. Internationaal betaal je pas later, vanuit het magazijn.</p>
        <p><a class="btn" href="/how-to-use-acbuy/">Nederlandse stap-voor-stap</a>
           <a class="btn btn--ghost" href="{escape(OFFICIAL)}shopping-guide">Officiële GuideBook</a></p>
      </div>
      {fig_guide}
    </div>
  </div>
</section>
<section class="sec" id="sheet-explain">
  <div class="wrap">
    <div class="split">
      <div>
        <span class="eyebrow" style="color:var(--acd)">Naam die misleidt</span>
        <h2>Een spreadsheet is geen Excel-bestand</h2>
        <p class="lead">In het Nederlands leidt het woord af. Hier betekent «spreadsheet» geen tabel van rijen en kolommen: het is een catalogus van productkaarten met foto, merk, referentieprijs en de link om in de agent te plakken.</p>
        <p>Wat je op <a href="{escape(W2C)}/?{utm}" rel="nofollow noopener" target="_blank">w2clinks</a> ziet zijn kaarten, geen cellen. Je bladert op categorie, filtert op merk, geslacht, kleur of materiaal, en elke fiche heeft de link die de agent nodig heeft. Dat is de hele truc: een link van Taobao, 1688 of Weidian omzetten in iets dat je vanuit Nederland kunt bestellen.</p>
        <p><a class="btn btn--ghost" href="/catalogus/">Hoe de catalogus werkt</a></p>
      </div>
      {fig_sheet}
    </div>
  </div>
</section>
<section class="sec sec--tint" id="cat-wall">
  <div class="wrap">
    <h2>Drieëndertig categorieën voor de eerste dag</h2>
    <p class="lead">Elke kaart opent de bijbehorende categorie in de catalogus. Begin met één: vijf categorieën in de eerste haul is de snelste weg naar een dure, lastige doos.</p>
    <div class="cat-grid">{wall}</div>
    <p style="margin-top:26px"><a class="btn" href="/catalogus/#categorias">Wat je in elke categorie nagaat</a></p>
  </div>
</section>
<section class="sec" id="states">
  <div class="wrap">
    <div class="split split--rev">
      <div>
        <span class="eyebrow" style="color:var(--acd)">Twee betalingen</span>
        <h2>Negen statussen, drie schermen</h2>
        <p class="lead">Eerst betaal je het product plus het binnenlandse China-vervoer tot het magazijn. Internationaal komt later, als jij een lijn naar Nederland kiest. De vraag «waarom staat het stil?» is bijna altijd: je kijkt op het verkeerde scherm.</p>
        <ul class="tl">
          <li><b>Order Submitted</b><span>Bestelling verstuurd, product in China betaald.</span></li>
          <li><b>Order Placed</b><span>ACBuy koopt in de Chinese shop op jouw naam.</span></li>
          <li><b>Seller Shipped</b><span>De Chinese verkoper heeft verzonden.</span></li>
          <li><b>Arrived at Warehouse</b><span>Aangekomen in het magazijn.</span></li>
          <li><b>Inspection &amp; Storage</b><span>Controle, foto’s en opslag. Live labels staan in de app.</span></li>
          <li><b>Shipping Requested</b><span>Jij bundelt en boekt de internationale lijn naar Nederland.</span></li>
          <li><b>Parcel Packed</b><span>De doos wordt ingepakt.</span></li>
          <li><b>Shipped</b><span>Vertrek uit China.</span></li>
          <li><b>Delivered</b><span>Bezorgd; ontvangst bevestigen in de app.</span></li>
        </ul>
        <p>De eerste vier zitten onder Order, daarna Warehouse, daarna Parcel. <a href="/how-to-use-acbuy/">Handleiding met het traject →</a></p>
      </div>
      {fig_pay}
    </div>
  </div>
</section>
<section class="sec sec--tint" id="lab">
  <div class="wrap">
    <div class="split">
      <div>
        <h2>Nederland heeft lijnen, maar niet elke lijn is open</h2>
        <p class="lead">De officiële schatter is publiek. Kies destination <strong>Netherlands — 荷兰</strong>, niet EU en niet Netherlands Antilles. Het afleveradres is een Nederlandse postcode (vorm 1234 AB).</p>
        <p>Op 5 Oct 2026, met 1000 g en 35×25×10 cm, toonde de schatter onder meer Euro DHL Duty Free EC-Y, 12–16 werkdagen. Die bedragen veranderen per week; behandel ze als een foto van die dag en open de estimator vóór je koopt. Invoer: <a href="https://www.belastingdienst.nl/wps/wcm/connect/nl/douane/" rel="noopener">Belastingdienst Douane</a>.</p>
        <p><a class="btn" href="{escape(EST)}">Officiële schatter, bestemming Nederland</a>
           <a class="btn btn--ghost" href="/acbuy-shipping-guide/">Verzendplan</a></p>
      </div>
      {fig_est}
    </div>
  </div>
</section>
<section class="sec" id="volume">
  <div class="wrap">
    <div class="split split--rev">
      <div>
        <span class="eyebrow" style="color:var(--acd)">De dure fout</span>
        <h2>Het gewicht dat je betaalt is bijna nooit alleen de weegschaal</h2>
        <p class="lead">De DHL-regel in de schatter zelf zegt het: volume weight = L×W×H (cm) / 8000, en ze factureren het maximum van weegschaal en volume. Een donsjas is licht en volumineus: daar beslist het volume.</p>
        <p>Voorbeeld: 40×40×3 cm is 4800 cm³, gedeeld door 8000 is 600 g volume bij 200 g echt gewicht. Alleen reist die jas, dan betaal je 600 g. Jouw maten vul je in de schatter, bestemming Nederland.</p>
        <p><a class="btn btn--ghost" href="/acbuy-shipping-guide/">Verzendplan met volumgewicht</a></p>
      </div>
      {fig_vol}
    </div>
  </div>
</section>
<section class="sec sec--tint" id="restricted">
  <div class="wrap">
    <div class="split">
      <div>
        <h2>Veel producten kun je niet kopen, ook al staan ze er</h2>
        <p class="lead">Op de officiële site zie je fiches zonder prijs, of een DIY-formulier in plaats van een winkelkaart. Dat is geen fout van deze homepage: de bronlink is niet koopbaar via de agent, of de prijs liet zich niet lezen.</p>
        <p>Regel: zonder echte prijs en varianten niet bestellen. Tabak, alcohol en geneesmiddelen reizen niet. Restricted is een inkoopblokkade, geen bericht van de Douane. De groene disclaimer op het DIY-scherm zegt hetzelfde: ACBuy verkoopt geen eigen voorraad.</p>
      </div>
      {fig_diy}
    </div>
  </div>
</section>
<section class="sec" id="faq">
  <div class="wrap">
    <h2>Hulp, nieuws en waar je vraagt</h2>
    <p class="lead">De meeste twijfels van de eerste orders herhalen zich: twee betalingen, catalogus in het Engels op w2clinks, volumgewicht, Douane. Ze staan beantwoord in het Nederlands op Hulp — een eigen URL, geen bijlage van deze homepage.</p>
    <p>Op Nieuws zetten we met datum wat we zelf op het platform hebben nagekeken. Over ons legt uit dat deze host redactioneel onafhankelijk is. Als je met ACBuy moet praten, is het kanaal de in-app-chat: wij zien je account niet.</p>
    <p><a class="btn" href="/hulp/">Alle vragen op Hulp</a>
       <a class="btn btn--ghost" href="/nieuws/">Gedateerde checks op Nieuws</a>
       <a class="btn btn--ghost" href="/over-ons/">Over ons</a></p>
  </div>
</section>
"""
    return _shell(
        page_title(DESK, "kopen in China vanaf Nederland, veilig"),
        "Onafhankelijke gids in het Nederlands: hoe je via ACBuy in China koopt, hoe de catalogus van w2clinks werkt, hoe een pakket naar Nederland reist.",
        f"https://{HOST}/",
        [faq_ld("nl-NL", _nl_faqs())],
        body,
        "/",
    )


def build_catalog() -> str:
    wall = "".join(
        f'<a class="cat" href="{escape(W2C_ACBUY_SHEET)}?category={quote_plus(key)}&amp;page=1&amp;sort=newest" '
        f'rel="noopener" target="_blank">'
        f'<img src="{escape(W2C)}/public/static/w2c/categories/{escape(fn)}" alt="{escape(key)}" '
        f'loading="lazy" decoding="async" width="96" height="96">'
        f'<div class="cat__b"><strong>{escape(labn)}</strong><span>{escape(key)}</span>'
        f"<em>{escape(CAT_NOTES[key])}</em></div></a>"
        for key, labn, fn in W2C_CATS
    )
    fig_sheet = _fig(
        "/img/shots/catalogus.jpg",
        "ACBuy-catalogus op w2clinks: productkaarten met foto, merk en referentieprijs",
        "Een categorie van de catalogus: kaarten met beeld, merk en referentieprijs in yuan. Die prijzen veranderen per dag. Opname 5 Oct 2026.",
        1200,
        900,
    )
    fig_zoek = _fig(
        "/img/shots/catalogus-zoek.jpg",
        "Zoekresultaten hoodie in de ACBuy-catalogus van w2clinks, met filters links",
        "Resultaten met de filterkolom. Zichtbare prijzen zijn steekproeven van het platform en wisselen dagelijks. Opname 5 Oct 2026.",
        1200,
        900,
    )
    fig_diy = _fig(
        "/img/shots/oficial-diy.jpg",
        "ACBuy DIY-formulier: bronlink plakken als de zoekbalk de fiche niet leest",
        "Het handmatige formulier accepteert de bronlink en specificaties in tekst. Opname 5 Oct 2026; het getoonde totaal is van dat voorbeeld.",
    )
    body = f"""
<section class="sec sec--first">
  <div class="wrap">
    <div class="split">
      <div>
        <span class="eyebrow" style="color:var(--acc)">De catalogus</span>
        <h1>Wat ACBuy Spreadsheet is, en wat je erin vindt</h1>
        <p class="lead">Het is een catalogus van productkaarten, geen Excel-bestand. Je bladert als in een winkel: drieëndertig categorieën, filters en kaarten met foto, merk en de link voor de agent. Hieronder staan die categorieën, met wat je in elk daarvan nagaat.</p>
        <p>De verwarring over de naam is normaal in het Nederlands, omdat «spreadsheet» letterlijk een rekenblad is. Hier zijn geen rijen, cellen of tabbladen: er zijn fiches. Elke fiche is een concreet product uit een Chinese shop, met beeld, categorie en de link die je daarna in ACBuy plakt.</p>
      </div>
      {fig_sheet}
    </div>
  </div>
</section>
<section class="sec sec--tint">
  <div class="wrap">
    <div class="split split--rev">
      <div>
        <h2>Waarom een aparte catalogus</h2>
        <p>De zoekbalk van een agent geeft de hele voorraad van Chinese shops, gigantisch en in het Chinees. Een catalogus doet het voorwerk: iemand heeft al gekozen welke fiches de moeite waard zijn, ze op categorie gezet en de link klaargezet.</p>
        <p>In de praktijk: je vindt de fiche in de catalogus van w2clinks, kopieert de bronlink en plakt die in de zoekbalk van ACBuy of in het handmatige bestelformulier. De catalogus int niets en verkoopt niets: hij spaart het zoekwerk.</p>
        <p>De filters links worden het meest onderschat. Merk, geslacht, seizoen, kleur, materiaal en prijsklasse maken van duizenden fiches in twee klikken iets naspeurbends.</p>
      </div>
      {fig_zoek}
    </div>
  </div>
</section>
<section class="sec" id="categorias">
  <div class="wrap">
    <h2>De drieëndertig categorieën, en wat je in elk nagaat</h2>
    <p class="lead">Dit is de catalogus. Elke kaart opent die categorie in w2clinks. De zin eronder is geen vulling: het is de fout die in die categorie het vaakst terugkomt als je op afstand koopt.</p>
    <div class="cat-grid cat-grid--rich">{wall}</div>
  </div>
</section>
<section class="sec sec--tint" id="eerste-categorie">
  <div class="wrap">
    <h2>Hoe kies je de eerste categorie</h2>
    <p class="lead">Als het je eerste bestelling is, kies iets flats en lichts: T-shirts, shorts, sieraden. Die komen eerder aan, kosten minder om te sturen, en laten je het hele circuit controleren zonder veel geld te riskeren.</p>
    <p>Laat volumineus voor de tweede order: donsjassen, tassen, petten. Niet omdat ze slechter zijn, maar omdat hun verzendprijs van het volume afhangt — en dat reken je pas goed als je één ronde hebt gezien.</p>
    <p>Drie categorieën met extra voorwaarden: elektronica (vaak lithium), brillen (breekbaar) en alles met batterij of magneet. Niet elke lijn naar Nederland accepteert die. Check de schatter vóór je ze in het magazijn laat liggen.</p>
  </div>
</section>
<section class="sec">
  <div class="wrap">
    <h2>Ongemakkelijk gegeven: de catalogus zoekt in het Engels</h2>
    <p class="lead">We hebben het term voor term nagekeken op {escape(DATE)}. Dat wil je weten vóór je je eerste zoekopdracht in het Nederlands typt.</p>
    <p>Nederlandse woorden zoals «turnschoenen», «trui», «jas» of «bril» gaven vaak nul resultaten. De Engelse keys sneakers, hoodie, jacket, trousers, bag, glasses of watch gaven pagina’s fiches. Daarom stuurt de zoekbalk op de homepage naar w2clinks met die Engelse term.</p>
    <table class="eq">
      <thead><tr><th>Als je denkt aan</th><th>Typ</th></tr></thead>
      <tbody>
        <tr><td>turnschoenen</td><td>sneakers</td></tr>
        <tr><td>hoodie / vest met capuchon</td><td>hoodie</td></tr>
        <tr><td>jas</td><td>jacket</td></tr>
        <tr><td>broek</td><td>trousers</td></tr>
        <tr><td>tas</td><td>bag</td></tr>
        <tr><td>bril</td><td>glasses</td></tr>
        <tr><td>horloge</td><td>watch</td></tr>
      </tbody>
    </table>
  </div>
</section>
<section class="sec sec--tint">
  <div class="wrap">
    <div class="split">
      <div>
        <h2>Van catalogus naar bestelling, zonder de link te verliezen</h2>
        <p class="lead">De fiche is het begin, niet de kassa. De stap die het vaakst misgaat is verkeerd kopiëren: de catalogusfiche heeft de bronlink van de Chinese shop; díé heeft ACBuy nodig.</p>
        <p>Plak je de URL van de catalogusfiche zelf, dan weet de agent niet wat hij moet kopen. Kopieer de Taobao-, 1688- of Weidian-link, plak die in de zoekbalk van ACBuy, controleer prijs en variant, en betaal pas internationaal als de QC-foto’s kloppen.</p>
        <p>Als de zoekbalk de link niet herkent, blijft het handmatige bestelformulier: adres, kleur en maat in tekst, plus een notitie. Fiches zonder prijs hoor je over te slaan — die bronlink is in China al dood.</p>
        <p><a class="btn" href="{escape(W2C_ACBUY_SHEET)}">Open de ACBuy-catalogus op w2clinks</a>
           <a class="btn btn--ghost" href="/how-to-use-acbuy/">Handleiding stap voor stap</a></p>
      </div>
      {fig_diy}
    </div>
  </div>
</section>
"""
    return _shell(
        page_title(DESK, "wat het is en welke categorieën je erin vindt"),
        "Onafhankelijke catalogusgids: drieëndertig categorieën van w2clinks, Engelse zoekkeys, en hoe je van fiche naar ACBuy-bestelling gaat.",
        f"https://{HOST}/catalogus/",
        [],
        body,
        "/catalogus/",
    )


def build_help() -> str:
    pairs = _nl_faqs()
    g1 = _faq_html(pairs[0:3], open_first=True)
    g2 = _faq_html(pairs[3:7], open_first=False)
    g3 = _faq_html(pairs[7:9], open_first=False)
    g4 = _faq_html(pairs[9:13], open_first=False)
    g5 = _faq_html(pairs[13:15], open_first=False)
    fig_help = _fig(
        "/img/shots/oficial-guidebook-3.jpg",
        "Officiële ACBuy GuideBook: eerste betaling in de Checkout",
        "Vragen over een concreet pakket horen in de officiële chat, niet op deze gids. Opname 5 Oct 2026.",
    )
    body = f"""
<article class="pw">
  <span class="eyebrow" style="color:var(--acd)">Hulp</span>
  <h1>Hulp en vragen over ACBuy in Nederland</h1>
  <p class="lead">Vijftien vragen die bij de eerste orders terugkomen, beantwoord met wat we zelf hebben nagekeken en met een link naar de officiële bron als het cijfer niet van ons is.</p>
  <p>Als je twijfel over een concreet pakket gaat: het juiste loket is de officiële support. Wij zien je account niet. Deze pagina legt het systeem uit vóór en ná het bestellen.</p>
  {fig_help}
  <h2>Wat ACBuy is en in welke taal het werkt</h2>
  {g1}
  <h2>Wat je gaat betalen</h2>
  {g2}
  <h2>Invoer naar Nederland</h2>
  {g3}
  <h2>Magazijn, foto’s en wat mag reizen</h2>
  {g4}
  <h2>Als iets niet klopt</h2>
  {g5}
  <p><a class="btn" href="{escape(EST)}">Officiële estimator, bestemming Nederland</a>
     <a class="btn btn--ghost" href="/acbuy-shipping-guide/">Verzendplan</a>
     <a class="btn btn--ghost" href="/nieuws/">Nieuws</a></p>
</article>
"""
    return _shell(
        page_title(DESK, "hulp en veelgestelde vragen"),
        "Vijftien veelgestelde vragen over ACBuy, in het Nederlands: betalingen, volumgewicht, Douane in Nederland, catalogus van w2clinks.",
        f"https://{HOST}/hulp/",
        [faq_ld("nl-NL", pairs)],
        body,
        "/hulp/",
    )


def build_news() -> str:
    items = [
        (
            "Eerste ronde: estimator-bestemming is Nederland, niet EU",
            "We openden de officiële schatter met bestemming Nederland. Belgische of Duitse postcode is het verkeerde land. Nederlandse postcode heeft de vorm 1234 AB. Live geld staat in die schatter, niet in deze HTML.",
            "Wat dat voor jou betekent: filter altijd op Nederland voordat je lijnen vergelijkt. Een EU-keuze is geen Nederlands huisadres.",
        ),
        (
            "Nagekeken: de valutaswitch zet vaak alleen het teken om",
            "Op de officiële site blijven de cijfers vaak USD-cijfers als je EUR kiest; alleen het symbool wisselt. Deze host toont EUR als weergave van de China-kaart (X-Rates 1 Oct 2026). De kassa blijft de officiële estimator.",
            "Wat dat voor jou betekent: lees het bedrag in de app op de dag van betalen. Een eurosymbool op een ongewijzigd cijfer is geen koers.",
        ),
        (
            "De catalogus van w2clinks zoekt in het Engels",
            "We zochten in de ACBuy-catalogus van w2clinks. sneakers, hoodie en jacket gaven pagina’s resultaten; turnschoenen, trui of jas gaven vaak nul. Dat is de index, geen lege winkel. Gemeten {date}.".format(date=DATE),
            "Wat dat voor jou betekent: typ de Engelse key, of tik een chip op de homepage. De zoekbalk daar stuurt je naar w2clinks.",
        ),
        (
            "Officiële Help laadt zonder JavaScript niet",
            "https://www.acbuy.com/help is een app-schil. Zonder JavaScript zie je geen magazijnregel. Deze gids kopieert daar geen verzonnen aantal gratis dagen uit; de live tekst staat in de app op de ochtend van verzenden.",
            "Wat dat voor jou betekent: bewaartermijn en extra hoeken lees je in de officiële Help die dag, niet als een vast getal op deze site.",
        ),
        (
            "Hoe we dit controleren",
            "Verzendcijfers komen uit de publieke estimator, steeds met dezelfde gewoonte (bestemming Nederland, 1000 g, 35×25×10 cm) en de datum van de ronde. De catalogus waarover we schrijven is w2clinks, niet een productgrid op deze homepage. Rankende gidsen (verzending, review, handleiding) blijven eigen URL’s; deze pagina overschrijft ze niet.",
            "We publiceren geen SKU-prijs in de lopende tekst. Die verandert per week; daarvoor is de officiële schatter, die bovendien publiek is.",
        ),
    ]
    ld = itemlist_ld(
        url=f"https://{HOST}/nieuws/",
        name="ACBuy NL desk checks",
        items=[(h, f"{p} {m}") for h, p, m in items],
    )
    cards = "".join(
        f'<article class="ncard"><h2>{escape(h)}</h2><p>{escape(p)}</p><p>{escape(m)}</p></article>'
        for h, p, m in items
    )
    body = f"""
<article class="pw">
  <span class="eyebrow" style="color:var(--acd)">Nieuws</span>
  <h1>Wat we op het platform hebben nagekeken, met datum</h1>
  <p class="lead">Dit is geen bedrijfsnieuwsbrief. Het zijn onze eigen controles, met datum, zodat je weet welke informatie recent is en welke al maanden niet nagekeken is.</p>
  <p>Eerste ronde: {escape(DATE)}. De controles hieronder komen uit dezelfde sessie, terwijl we deze gids bouwden. Het zijn geen vijf losse berichten van verschillende dagen, en we presenteren ze ook niet zo. Volgende rondes komen erboven, met hun eigen datum.</p>
  <p>Als een gegeven op deze site verandert, komt het hier te staan met de datum van de nieuwe check, in plaats van stilletjes herschreven te worden.</p>
  {cards}
</article>
"""
    return _shell(
        page_title(DESK, "wat we op het platform hebben nagekeken"),
        "Gedateerde controles over ACBuy: verzendlijnen naar Nederland, valuta, en het zoekgedrag van de catalogus.",
        f"https://{HOST}/nieuws/",
        [ld],
        body,
        "/nieuws/",
    )


def build_about() -> str:
    fig_about = _fig(
        "/img/shots/oficial-inicio.jpg",
        "Officiële ACBuy-homepage, anders dan deze gids",
        "De officiële site is een andere URL dan deze gids. Opname 5 Oct 2026.",
    )
    body = f"""
<article class="pw">
  <span class="eyebrow" style="color:var(--acd)">Over ons</span>
  <h1>Een onafhankelijke site over ACBuy, in het Nederlands</h1>
  <p class="lead">ACBuy Spreadsheet is geen ACBuy. Het is een redactionele gids: hoe die agent werkt, en hoe je de catalogus van w2clinks gebruikt vanaf Nederland.</p>
  <p>We nemen geen bestellingen aan, rekenen geen porto, bewaren geen goederen en zien geen account. Een probleem met een order hoort op {escape(OFFICIAL)}.</p>
  {fig_about}
  <h2>Hoe we werken</h2>
  <h3>Waar elk gegeven vandaan komt</h3>
  <p>Verzendcijfers komen uit de publieke estimator, steeds met bestemming, gewicht, maten en de datum van de check. Invoer wijst naar <a href="https://www.belastingdienst.nl/wps/wcm/connect/nl/douane/" rel="noopener">Belastingdienst Douane</a>. Wat we niet hebben nagekeken, publiceren we niet.</p>
  <h3>Waarom je hier weinig tarieven ziet</h3>
  <p>SKU-prijzen veranderen per week. Een vast bedrag op deze pagina zou binnen dagen misleidend zijn. We leggen het mechanisme uit en sturen je naar <a href="{escape(EST)}">{escape(EST)}</a> voor het bedrag van die dag.</p>
  <h3>Wat de screenshots tonen</h3>
  <p>Opnames van acbuy.com zijn van {escape(DATE)}. Productkaarten bij «spreadsheet» komen van w2clinks, niet van een productgrid op deze homepage. Bedragen in een tutorial zijn voorbeelden van die dag, geen kassaprijs voor jouw doos.</p>
  <h2>Contact</h2>
  <p>Schrijf als een gegeven, een link of een vertaling stukgaat. We zetten de correctie met datum op <a href="/nieuws/">Nieuws</a>. Orders: in-app chat op ACBuy. Deze gids: <a href="mailto:{escape(MAIL)}">{escape(MAIL)}</a>.</p>
</article>
"""
    return _shell(
        page_title(DESK, "wie we zijn en hoe je ons bereikt"),
        "Onafhankelijke site in het Nederlands over ACBuy: hoe we gegevens nalopen, waarom we weinig tarieven zetten, en hoe je ons schrijft.",
        f"https://{HOST}/over-ons/",
        [],
        body,
        "/over-ons/",
    )


def _assert_ok(html: str, page: str) -> None:
    if page == "nf":
        err = []
        if "Pagina niet gevonden | ACBuy Spreadsheet" not in html:
            err.append("404 title not aligned with hipobuy.es")
        if "Deze pagina bestaat niet" not in html:
            err.append("404 h1")
        if "noindex" not in html:
            err.append("404 robots")
        if MAIL not in html or "acbuy-logo.svg" not in html:
            err.append("404 chrome")
        if "Catalogus" not in html or "Handleiding" not in html:
            err.append("404 nav")
        if ".waf,.wabu,.wafb" not in html:
            err.append("404 missing waf hide")
        if 'lang="nl-NL"' not in html:
            err.append("404 lang")
        if 'href="/start/"' not in html or 'href="/">Start' in html:
            err.append("404 Start still points at /")
        if err:
            raise SystemExit(f"{page}: {'; '.join(err)}")
        return
    skip = {
        "missing #local dest briefing",
        "missing #local",
        "missing #catalog",
        "missing catalogue API",
        "missing FX_CCY EUR",
    }
    err = [e for e in validate_desk(html, FACTS, page=page) if e not in skip]
    if INVITE in html or INVITE2 in html or INVITE3 in html:
        if page == "home":
            err.append("invite token on homepage")
    if re.search(r"90\s*dagen|90\s*days", html, flags=re.I):
        err.append("invented 90-day copy")
    if "Georgia" in html or "#00C853" in html:
        err.append("Georgia / HipoBuy green")
    if MAIL not in html:
        err.append("missing editorial mailbox")
    if "cnfa85269032661" in html:
        err.append("old cnfa mailbox leftover")
    if f"support@{HOST}" in html:
        err.append("old support mailbox leftover")
    if "Jointown" in html or "EVERLINE" in html or "Cruisezhang" in html:
        err.append("operator paragraph / hipobuy mailbox")
    if "Onafhankelijkheidsverklaring" not in html or "onafhankelijke informatiesite" not in html:
        err.append("missing independence disclaimer")
    fp = dest_local_pack("NL")["fingerprint"]
    if page in ("home", "help") and fp not in html:
        err.append("missing NL fingerprint")
    for alien in ALIENS:
        if alien in html:
            err.append(f"sister leak {alien}")
    if "/api/products/" in html:
        err.append("api products dump")
    if "Voor een huisadres in Nederland" in html:
        err.append("huisadres briefing leftover")
    if "w2cspreadsheet" in html.lower() or "W2CSpreadsheet" in html or "W2C Spreadsheet" in html:
        err.append("w2cspreadsheet leftover")
    if "acbuy-logo.svg" not in html:
        err.append("missing official ACBuy logo")
    if "README.md" in html or "expand this stub" in html:
        err.append("english factory stub")
    if page == "home":
        if html.count('class="sg-faq"') >= 8:
            err.append("faq dump on homepage")
        if "allchinabuyspreadsheet.ca" in html or "Novedades" in html:
            err.append("planning dump on homepage")
        if "op de platform" in html:
            err.append("dutch grammar leftover on home")
        if "cat-30-shoes.png" not in html or "w2clinks.com/spreadsheet/acbuy" not in html:
            err.append("missing W2C Links categories")
        if 'class="fig"' not in html:
            err.append("missing illustrated figures")
        if "geen stockfoto" in html:
            err.append("empty shots panel leftover")
        if "geen Excel-bestand" not in html or "w2clinks" not in html:
            err.append("sheet-explain not aligned with hipobuy.es / w2clinks")
        if "Dezelfde indeling" in html:
            err.append("categories meta dump")
        if 'id="local"' in html or 'id="catalog"' in html:
            err.append("ops ids leftover on home")
        if 'href="/catalogus/"' not in html:
            err.append("catalogus nav missing")
        if 'href="/start/"' not in html or 'href="/" class="brand"' in html or 'href="/">Start' in html:
            err.append("Start still points at cached /")
        if page_title(DESK, "kopen in China vanaf Nederland, veilig") not in html:
            err.append("home title not aligned with hipobuy.es")
        if 'lang="nl-NL"' not in html:
            err.append("home lang")
        if ".waf,.wabu,.wafb" not in html:
            err.append("home missing waf hide")
    if page == "catalog":
        if "cat-30-shoes.png" not in html or "id=\"categorias\"" not in html:
            err.append("catalog page missing category wall")
        if "geen Excel-bestand" not in html:
            err.append("catalog missing spreadsheet-not-excel copy")
        if "Hoe kies je de eerste categorie" not in html:
            err.append("catalog missing first-category section")
        if "bronlink" not in html:
            err.append("catalog missing source-link copy")
    if page == "news":
        if "Novedades" in html or "op de platform" in html:
            err.append("news meta leftover")
        if "ACBuy Spreadsheet in het Nederlands: wat we op het platform hebben nagekeken" not in html:
            err.append("news title not aligned with hipobuy.es home formula")
        if "Nieuws van het platform |" in html or "Nieuws: wat we hebben nagekeken" in html:
            err.append("old news tab title leftover")
    if err:
        raise SystemExit(f"{page}: {'; '.join(err)}")


def _desk_css_path() -> Path:
    return OUT / HOST / "overlay" / "assets" / "css" / "acbuy-nl-desk.css"


def _wordmark_path() -> Path:
    return OUT / HOST / "overlay" / "assets" / "images" / "acbuy-wordmark.png"


def write_wordmark(path: Path) -> Path:
    """Orange ACBuy wordmark — replaces the leftover AllChinaBuy teal icon."""
    from PIL import Image, ImageDraw, ImageFont

    path.parent.mkdir(parents=True, exist_ok=True)
    w, h = 324, 70
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, 70, 70), 16, fill=(232, 112, 0, 255))
    font_a = ImageFont.truetype("/usr/share/fonts/truetype/macos/Inter-Bold.ttf", 36)
    font_w = ImageFont.truetype("/usr/share/fonts/truetype/macos/Inter-Bold.ttf", 40)
    bbox = d.textbbox((0, 0), "A", font=font_a)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    d.text(((70 - tw) / 2 - bbox[0], (70 - th) / 2 - bbox[1] - 1), "A", font=font_a, fill=(255, 255, 255, 255))
    d.text((86, 12), "ACBuy", font=font_w, fill=(17, 17, 17, 255))
    im.save(path, "PNG")
    return path


def generate() -> dict[str, Path]:
    dest = OUT / HOST / "overlay"
    dest.mkdir(parents=True, exist_ok=True)
    (dest / "hulp").mkdir(exist_ok=True)
    (dest / "nieuws").mkdir(exist_ok=True)
    (dest / "over-ons").mkdir(exist_ok=True)
    (dest / "catalogus").mkdir(exist_ok=True)
    (dest / "start").mkdir(exist_ok=True)
    css_path = _desk_css_path()
    css_path.parent.mkdir(parents=True, exist_ok=True)
    css_path.write_text(render_css(DESK), encoding="utf-8")
    logo = write_wordmark(_wordmark_path())
    logo_svg = dest / "assets" / "images" / "acbuy-logo.svg"
    if not logo_svg.is_file():
        raise SystemExit("missing official acbuy-logo.svg")
    img_root = dest / "img"
    missing: list[str] = []
    shots = (
        "oficial-inicio.jpg",
        "oficial-guidebook.jpg",
        "oficial-guidebook-3.jpg",
        "oficial-diy.jpg",
        "estimator-nl.jpg",
        "catalogus.jpg",
        "catalogus-zoek.jpg",
        "volume-voorbeeld.jpg",
    )
    missing += [n for n in shots if not (img_root / "shots" / n).is_file()]
    if not (img_root / "hero.jpg").is_file():
        missing.append("hero.jpg")
    if missing:
        raise SystemExit(f"missing images {missing}")
    home_html = build_home()
    pages = {
        "home": (dest / "index.html", home_html, "home"),
        "start": (dest / "start" / "index.html", home_html, "home"),
        "help": (dest / "hulp" / "index.html", build_help(), "help"),
        "news": (dest / "nieuws" / "index.html", build_news(), "news"),
        "about": (dest / "over-ons" / "index.html", build_about(), "about"),
        "catalog": (dest / "catalogus" / "index.html", build_catalog(), "catalog"),
        "nf": (dest / "404.html", build_404(DESK), "nf"),
    }
    out: dict[str, Path] = {"css": css_path, "logo": logo}
    floors = {"home": DEST_MIN, "nf": 3000}
    for key, (path, html, page) in pages.items():
        _assert_ok(html, page)
        n = len(html.encode("utf-8"))
        if n < floors.get(key, 4000):
            raise SystemExit(f"{key} too small {n}")
        path.write_text(html, encoding="utf-8")
        print("wrote", path, n)
        out[key] = path
    theme = OUT / "shared" / "themes" / "acbuy-theme.css"
    theme.parent.mkdir(parents=True, exist_ok=True)
    theme.write_text(
        "/* ACBuy country dest — official mint */\n:root { --primary: #31B38C; --primary-dark: #27BA9B; --primary-soft: #f5f6f7; --nav-dark: #181818; }\n",
        encoding="utf-8",
    )
    return out


def _inner_rels() -> list[str]:
    inventory = Path("/tmp/dest-inners.json")
    if inventory.is_file():
        rows = json.loads(inventory.read_text())
        for row in rows:
            if row.get("host") == HOST:
                return [item["rel"].lstrip("/") for item in row.get("files") or []]
    return [f"{rel.lstrip('/')}index.html" for rel, _ in RANKED]


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


OLD_API = """    location /api/ {
        try_files $uri =404;
        add_header X-Robots-Tag "noindex, nofollow" always;
    }
"""
NEW_API = """    location /api/ {
        rewrite ^/api/([^/]+)/?$ /api/$1/index.php last;
        add_header X-Robots-Tag "noindex, nofollow" always;
    }
"""


def _patch_api_nginx(client, sftp) -> None:
    remote = f"/www/server/panel/vhost/nginx/{HOST}.conf"
    stamp = time.strftime("%Y%m%d-%H%M%S")
    _run(client, f"cp -a '{remote}' '/www/backup/acbuy-nl-nginx-{stamp}.conf'")
    with sftp.open(remote, "r") as fh:
        text = fh.read().decode()
    if NEW_API in text:
        print("nginx api already patched")
        return
    if OLD_API not in text:
        raise SystemExit("nginx /api/ block not found")
    text = text.replace(OLD_API, NEW_API, 1)
    tmp = Path("/tmp/acbuy-nl.conf")
    tmp.write_text(text, encoding="utf-8")
    sftp.put(str(tmp), remote)
    chk = _run(client, "nginx -t")
    print(chk)
    if "successful" not in chk.lower() and "ok" not in chk.lower():
        raise SystemExit("nginx -t failed")
    print(_run(client, "nginx -s reload"))
    print("nginx api patched")


def _wrap_ranked(client, sftp, bak: str, root: str) -> None:
    skip = {"index.html", "404.html", "404/index.html"}
    mins = {rel.lstrip("/"): min_b for rel, min_b in RANKED}
    for rel in _inner_rels():
        if rel in skip:
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
        out, why = wrap_inner(raw, href)
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
        local_tmp = Path("/tmp") / f"acbuy-nl-wrap-{rel.replace('/', '_')}"
        local_tmp.write_text(out, encoding="utf-8")
        sftp.put(str(local_tmp), remote)
        print("WRAP", rel, "in", len(raw), "out", len(out.encode("utf-8")))
        local_tmp.unlink(missing_ok=True)


def put() -> None:
    files = generate()
    client = _connect()
    stamp = time.strftime("%Y%m%d-%H%M%S")
    bak = f"/www/backup/acbuy-nl-cms-{stamp}"
    root = f"/www/wwwroot/{HOST}"
    _run(
        client,
        f"mkdir -p '{bak}' '{root}/hulp' '{root}/nieuws' '{root}/over-ons' '{root}/catalogus' '{root}/start' "
        f"'{root}/assets/css' '{root}/assets/images' '{root}/img/cat' '{root}/img/shots'",
    )
    sftp = client.open_sftp()
    mapping = {
        "home": f"{root}/index.html",
        "start": f"{root}/start/index.html",
        "help": f"{root}/hulp/index.html",
        "news": f"{root}/nieuws/index.html",
        "about": f"{root}/over-ons/index.html",
        "catalog": f"{root}/catalogus/index.html",
        "nf": f"{root}/404.html",
    }
    for key, remote in mapping.items():
        local = files[key]
        raw = local.read_text(encoding="utf-8")
        if key in ("home", "start", "help") and dest_local_pack("NL")["fingerprint"] not in raw:
            raise SystemExit(f"refusing {key} without fingerprint")
        if key in ("home", "start") and (INVITE in raw or "90 days" in raw.lower()):
            raise SystemExit("refusing home with invite or 90-day copy")
        _run(client, f"test -f '{remote}' && cp -a '{remote}' '{bak}/{key}.html' || true")
        sftp.put(str(local), remote)
        print("PUT", remote, local.stat().st_size)
    theme = OUT / "shared" / "themes" / "acbuy-theme.css"
    sftp.put(str(theme), f"{root}/assets/css/acbuy-theme.css")
    sftp.put(str(files["css"]), f"{root}/assets/css/acbuy-nl-desk.css")
    sftp.put(str(files["logo"]), f"{root}/assets/images/acbuy-wordmark.png")
    overlay = OUT / HOST / "overlay"
    sftp.put(str(overlay / "assets" / "images" / "acbuy-logo.svg"), f"{root}/assets/images/acbuy-logo.svg")
    sftp.put(str(overlay / "favicon1.ico"), f"{root}/favicon1.ico")
    sftp.put(str(overlay / "favicon.ico"), f"{root}/favicon.ico")
    print("PUT official logo + favicon")
    img_local = OUT / HOST / "overlay" / "img"
    sftp.put(str(img_local / "hero.jpg"), f"{root}/img/hero.jpg")
    print("PUT", f"{root}/img/hero.jpg")
    for src in sorted((img_local / "cat").glob("*.jpg")):
        remote = f"{root}/img/cat/{src.name}"
        sftp.put(str(src), remote)
        print("PUT", remote, src.stat().st_size)
    for src in sorted((img_local / "shots").glob("*.jpg")):
        remote = f"{root}/img/shots/{src.name}"
        sftp.put(str(src), remote)
        print("PUT", remote, src.stat().st_size)
    _patch_api_nginx(client, sftp)
    _wrap_ranked(client, sftp, bak, root)
    for rel, min_b in RANKED:
        inner = f"{root}{rel}index.html"
        n = _run(client, f"wc -c < '{inner}' 2>/dev/null || echo 0")
        try:
            inner_n = int(re.sub(r"\D", "", n) or "0")
        except ValueError:
            inner_n = 0
        print("keep unique", rel, inner_n)
        if inner_n and inner_n < min_b:
            print("WARN unique small", rel, inner_n)
    _run(
        client,
        f"chown -R www:www '{root}/index.html' '{root}/404.html' '{root}/hulp' '{root}/nieuws' '{root}/over-ons' '{root}/catalogus' '{root}/start' '{root}/favicon.ico' '{root}/favicon1.ico' '{root}/assets/css' "
        f"'{root}/img' '{root}/acbuy-shipping-guide' '{root}/is-acbuy-legit' '{root}/how-to-use-acbuy' '{root}/acbuy-coupons' "
        f"'{root}/acbuy-spreadsheet' '{root}/blog' 2>/dev/null || true",
    )
    sftp.close()
    print("backup", bak)
    client.close()


def live_check() -> None:
    import urllib.request

    class NR(urllib.request.HTTPRedirectHandler):
        def redirect_request(self, req, fp, code, msg, headers, newurl):
            return None

    def fetch(url, follow=True):
        req = urllib.request.Request(
            url,
            headers={"User-Agent": "acbuy-nl-cms/1.0", "Cache-Control": "no-cache"},
        )
        opener = urllib.request.build_opener() if follow else urllib.request.build_opener(NR)
        try:
            with opener.open(req, timeout=25) as resp:
                return resp.status, resp.geturl(), resp.headers.get("Location") or "", resp.read()
        except urllib.error.HTTPError as e:
            return e.code, url, e.headers.get("Location") or "", e.read() if e.fp else b""

    fail = 0
    fp = dest_local_pack("NL")["fingerprint"]
    checks = [
        (f"https://{HOST}/", "home", True),
        (f"https://{HOST}/start/", "start", True),
        (f"https://{HOST}/hulp/", "help", True),
        (f"https://{HOST}/nieuws/", "news", False),
        (f"https://{HOST}/over-ons/", "about", False),
        (f"https://{HOST}/catalogus/", "catalog", False),
        (f"https://{HOST}/acbuy-shipping-guide/", "ranked", False),
        (f"https://{HOST}/is-acbuy-legit/", "ranked", False),
        (f"https://{HOST}/how-to-use-acbuy/", "ranked", False),
    ]
    for url, kind, need_fp in checks:
        code, final, loc, body = fetch(url, follow=True)
        html = body.decode("utf-8", "replace")
        print(kind, code, "bytes", len(body), "cms", "acbuy-logo.svg" in html or "acbuy-wordmark" in html)
        if code != 200:
            print(" FAIL status"); fail += 1
        if "acbuy-logo.svg" not in html:
            print(" FAIL official logo"); fail += 1
        if 'lang="nl-NL"' not in html:
            print(" FAIL lang nl-NL"); fail += 1
        if ".waf,.wabu,.wafb" not in html:
            print(" FAIL waf hide"); fail += 1
        if need_fp and fp not in html:
            print(" FAIL fingerprint"); fail += 1
        if 'href="/start/"' not in html or 'href="/">Start' in html:
            print(" FAIL Start still points at /"); fail += 1
        if kind in ("home", "help", "news", "about", "catalog", "start"):
            if "/api/products/" in html or "Voor een huisadres in Nederland" in html:
                print(" FAIL api/huisadres leftover"); fail += 1
            if "w2cspreadsheet" in html.lower() or "W2C Spreadsheet" in html:
                print(" FAIL w2cspreadsheet leftover"); fail += 1
        if kind in ("home", "start"):
            if INVITE in html or re.search(r"90\s*days", html, re.I):
                print(" FAIL invite/90"); fail += 1
            if "Independent desk — not the official" in html:
                print(" FAIL english leftover"); fail += 1
            if "Catalogus" not in html or "ACBuy Spreadsheet" not in html:
                print(" FAIL dutch hero"); fail += 1
            if "ACBuy Spreadsheet in het Nederlands: kopen in China vanaf Nederland, veilig" not in html:
                print(" FAIL home title"); fail += 1
            if "allchinabuyspreadsheet.ca" in html or "Novedades" in html:
                print(" FAIL planning dump on home"); fail += 1
            if html.count('class="sg-faq"') >= 8:
                print(" FAIL faq dump on home"); fail += 1
            if "FAQPage" not in html:
                print(" FAIL home FAQPage"); fail += 1
            if "op de platform" in html:
                print(" FAIL dutch grammar"); fail += 1
            if "cat-30-shoes.png" not in html or "w2clinks.com/spreadsheet/acbuy" not in html:
                print(" FAIL missing W2C categories"); fail += 1
            if 'class="fig"' not in html:
                print(" FAIL missing photos"); fail += 1
            if "geen stockfoto" in html:
                print(" FAIL empty shots"); fail += 1
            if MAIL not in html or "Onafhankelijkheidsverklaring" not in html:
                print(" FAIL footer independence/mail"); fail += 1
            if "cnfa85269032661" in html:
                print(" FAIL old cnfa mailbox"); fail += 1
            if "Jointown" in html or "EVERLINE" in html or f"support@{HOST}" in html:
                print(" FAIL operator/old mailbox"); fail += 1
            if "geen Excel-bestand" not in html or "Dezelfde indeling" in html:
                print(" FAIL sheet-explain / categories dump"); fail += 1
            if 'id="local"' in html or 'id="catalog"' in html:
                print(" FAIL ops ids on home"); fail += 1
            if "/catalogus/" not in html:
                print(" FAIL catalogus nav"); fail += 1
            for alien in ("Packstation", "form A1A 1A1"):
                if alien in html:
                    print(" FAIL alien", alien); fail += 1
        if kind == "catalog":
            if html.count('class="cat"') < 30 or "geen Excel-bestand" not in html:
                print(" FAIL catalog page"); fail += 1
            if "Hoe kies je de eerste categorie" not in html or "bronlink" not in html:
                print(" FAIL catalog hipobuy.es sections"); fail += 1
            if f"acbuy-nl-desk.css?v={CSS_V}" not in html:
                print(" FAIL catalog css bust"); fail += 1
        if kind == "news" and ("Novedades" in html or "op de platform" in html):
            print(" FAIL news meta leftover"); fail += 1
        if kind == "news" and "ACBuy Spreadsheet in het Nederlands: wat we op het platform hebben nagekeken" not in html:
            print(" FAIL news title"); fail += 1
        if kind == "help" and "FAQPage" not in html:
            print(" FAIL help FAQPage"); fail += 1
        if kind == "news" and "ItemList" not in html:
            print(" FAIL news ItemList"); fail += 1
        if kind == "about" and "ContactPoint" not in html:
            print(" FAIL about ContactPoint"); fail += 1
        if kind == "ranked":
            if len(body) < 4000:
                print(" FAIL ranked thin"); fail += 1
            if "acbuy-logo.svg" not in html:
                print(" FAIL ranked chrome"); fail += 1
            if "README.md" in html or "expand this stub" in html:
                print(" FAIL ranked english stub"); fail += 1
            if 'id="lang-modal"' in html or "This page is part of" in html or re.search(r">\s*p>", html):
                print(" FAIL ranked english chrome"); fail += 1
            if f"acbuy-nl-desk.css?v={CSS_V}" not in html or "allchinabuy-theme.css" in html:
                print(" FAIL ranked mint css"); fail += 1
            if "country-desk-chrome" not in html:
                print(" FAIL ranked chrome lock id"); fail += 1
    code, _, _, nf_body = fetch(f"https://{HOST}/this-page-does-not-exist-cms/", follow=True)
    nf = nf_body.decode("utf-8", "replace")
    print("404", code, "bytes", len(nf_body), "title", "Pagina niet gevonden" in nf)
    if code != 404:
        print(" FAIL 404 status"); fail += 1
    if "Pagina niet gevonden | ACBuy Spreadsheet" not in nf:
        print(" FAIL 404 title"); fail += 1
    if "Deze pagina bestaat niet" not in nf or "Catalogus" not in nf:
        print(" FAIL 404 chrome/nav"); fail += 1
    if "acbuy-logo.svg" not in nf or MAIL not in nf:
        print(" FAIL 404 logo/mail"); fail += 1
    if "noindex" not in nf:
        print(" FAIL 404 robots"); fail += 1
    if 'href="/start/"' not in nf or 'href="/">Start' in nf:
        print(" FAIL 404 Start still points at /"); fail += 1
    # AllChinaBuy NL is a different agent dest — never 301 into ACBuy NL.
    code, _, loc, _ = fetch("https://allchinabuyspreadsheet.nl/", follow=False)
    print("allchinabuy nl dest", code, loc)
    if code in (301, 302, 308) and HOST in (loc or ""):
        print(" FAIL AllChinaBuy NL collapsed into ACBuy NL"); fail += 1
    if code != 200:
        print(" FAIL AllChinaBuy NL dest"); fail += 1
    code, _, loc, _ = fetch("https://acbuyspreadsheets.ca/", follow=False)
    print("ca dest independent", code, loc)
    if code in (301, 302, 308) and HOST in (loc or ""):
        print(" FAIL CA dest collapsed into NL"); fail += 1
    code, final, _, _ = fetch("https://allchinabuyspreadsheet.ca/", follow=True)
    print("ca dest", code, final)
    if HOST in final:
        print(" FAIL CA collapsed into NL"); fail += 1
    if fail:
        raise SystemExit(f"live_check fail {fail}")
    print("live_check ok")


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "generate"
    if cmd == "put":
        put()
    elif cmd == "live":
        live_check()
    elif cmd == "all":
        put()
        live_check()
    else:
        generate()
