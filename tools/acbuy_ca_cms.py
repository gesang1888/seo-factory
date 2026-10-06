#!/usr/bin/env python3
"""ACBuy Canada pack of the country-dest CMS template.

Chrome / IA / wrap live in tools/country_cms.py (gold IA: hipobuy.es, gold
brand: acbuy.com). English copy, CAD, Canadian postal-code fingerprint.
Does not PUT 5KB overlays over ranked unique inners. Does not 301 this host
into allchinabuyspreadsheet.ca or into the NL dest. Twin
allchinabuyspreadsheet.nl still 301s into acbuyspreadsheets.nl.
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
HOST = "acbuyspreadsheets.ca"
DATE = "6 Oct 2026"
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
NL_HOST = "acbuyspreadsheets.nl"
ACB_CA = "allchinabuyspreadsheet.ca"
STORAGE = (
    "Official ACBuy Help is the live SPA "
    f"({HELP}); confirm that copy the morning you ship. "
    "This desk does not invent a free-day count."
)
DEST_MIN = 22000
CSS_V = "20261006a"
INNER_MARKER = f'data-inner-chrome="{CSS_V}-acbuy-ca"'
ALIENS = (
    "1010 Wien",
    "Packstation",
    "Nederlandse postcode",
    "Poste Italiane",
    "00-001 Warszawa",
    "00100 Helsinki",
    "pas un code postal belge",
    "does not invent a de-minimis dollar",
    "Northern Ireland is often another",
    "do not copy a GST rate",
    "not a customs territory",
    "1234 AB",
)

KEEP = [
    ("/is-acbuy-legit/", "Review"),
    ("/acbuy-shipping-guide/", "Shipping"),
    ("/acbuy-coupons/", "Coupons"),
    ("/how-to-use-acbuy/", "Guide"),
]
CMS_PAGES = [
    ("/", "Start"),
    ("/how-to-use-acbuy/", "Guide"),
    ("/catalog/", "Catalog"),
    ("/acbuy-shipping-guide/", "Shipping"),
    ("/help/", "Help"),
    ("/news/", "News"),
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
    "lang": "en-CA",
    "loc": "en",
    "dest": "CA",
    "dest_label": "Canada",
    "ccy": "CAD",
    "storage": STORAGE,
    "estimator": EST,
    "official": OFFICIAL,
    "date": DATE,
    "keep": KEEP,
    "codes_off_title": [INVITE, INVITE2, INVITE3],
    "strict_html_codes": True,
}

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
W2C_CATS = cats_for(EN_LABELS)


def _ca_faqs() -> list[tuple[str, str]]:
    """Help answers follow homepage: catalog is w2clinks, never /api/products/."""
    pairs = []
    for q, a in long_faqs(FACTS):
        a = a.replace(
            f"The finds index this desk reads is English (sneakers, hoodie, jacket). Local words often return zero cards — that is an English index, not an empty shop. Type the English key. Measured {DATE} via /api/products/ on {HOST}.",
            f"The w2clinks catalogue indexes in English (sneakers, hoodie, jacket). «Sneakers» works; French or local spellings often return zero cards. That is not an empty shop. Measured {DATE}.",
        )
        a = a.replace("/api/products/", "w2clinks")
        pairs.append((q, a))
    return pairs


CAT_NOTES = {
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
    "Electronics": "Often lithium. Many air lines refuse them: check the estimator before you order.",
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
    dest="CA",
    dest_label="Canada",
    lang="en-CA",
    in_language="in English",
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
        "Independent English-language guide to ACBuy and to how you use the w2clinks "
        "catalogue to buy in China from Canada."
    ),
    footer_sections=[
        ("/how-to-use-acbuy/", "ACBuy guide"),
        ("/catalog/", "The spreadsheet and the categories"),
        ("/acbuy-shipping-guide/", "Shipping and customs"),
        ("/help/", "Help and questions"),
        ("/news/", "News"),
        ("/about/", "About us"),
    ],
    footer_official=[
        (_off("/"), "ACBuy (official site)"),
        (_off("/register"), "Create an ACBuy account"),
        (_off("/estimation/"), "Shipping estimator"),
        (_off("/help"), "Help centre"),
        (_off("/issueView"), "Official FAQ"),
        ("https://www.reddit.com/r/Acbuyofficial/", "Official Reddit"),
    ],
    independence=(
        "ACBuy Spreadsheet is an independent information site. We are not ACBuy, "
        "we do not process orders, we do not collect shipping fees and we cannot see "
        "your account. Every order, payment and claim runs through the official site."
    ),
    copyright="&copy; 2026 ACBuy Spreadsheet. English copy, edited and checked by people before publication.",
    login_label="Log in to ACBuy",
    menu_label="Open menu",
    skip_lang="en",
    not_found_h1="This page does not exist",
    not_found_lead="The link may be old. These are the sections that do exist:",
    home_cta="Back to the homepage",
    theme_css="acbuy-theme.css",
    desk_css="acbuy-ca-desk.css",
    inner_marker=INNER_MARKER,
    reddit="https://www.reddit.com/r/Acbuyofficial/",
    register_path="/register",
    sheet_slug="acbuy",
    invites=(INVITE, INVITE2, INVITE3),
    factory_pats=(
        r"Step-by-step guide to using ACBuy:[^.<]{0,240}\.",
        r"This page is part of\s*(?:<strong>)?ACBuy(?: Canada| Nederland)?(?:</strong>)?\s*\.[\s./<code>]*",
        r"Browse ACBuy Spreadsheet\s*(?:&rarr;|→)?",
    ),
    extra_subs=(
        (
            r'(?is)(<div style="max-width:720px;[^"]*">)\s*(<h1[\s\S]*?</h1>)\s*<p\b[^>]*>[\s\S]*?</p>\s*',
            r"\1\n  \2\n  ",
        ),
    ),
    strip_home_crumb="Start",
    not_found_tab="Page not found",
    sections_h="Sections",
    official_h="Official links",
    independence_h="Independence notice.",
    nav_aria="Main menu",
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
        "Official ACBuy homepage with search bar, plane banner and four steps: Place orders, QC&storage, Submit parcels, INTL ship",
        "The official homepage of acbuy.com, 6 Oct 2026. The four steps under the search bar are the whole path: order in China, QC in the warehouse, consolidate, ship internationally.",
    )
    fig_guide = _fig(
        "/img/shots/oficial-guidebook.jpg",
        "Official ACBuy GuideBook, step 1: pick a product via a Taobao link or the search bar",
        "ACBuy GuideBook, step 1. Left: paste a Taobao / 1688 link. Right: search in the app. Capture 6 Oct 2026.",
    )
    fig_sheet = _fig(
        "/img/shots/catalogus.jpg",
        "ACBuy catalogue on w2clinks: product cards with photo, brand and reference price",
        "What you see on w2clinks are cards, not Excel cells. Yuan prices change by the day. Capture 6 Oct 2026, category SNEAKERS.",
        1200,
        900,
    )
    fig_pay = _fig(
        "/img/shots/oficial-guidebook-3.jpg",
        "Official ACBuy GuideBook, step 3: first payment of product plus China domestic, Checkout button",
        "Step 3 of the official GuideBook: you first pay the product and China-domestic freight into the warehouse. International is not in that total. Capture 6 Oct 2026.",
    )
    fig_est = _fig(
        "/img/shots/estimator-ca.jpg",
        "Official ACBuy estimator with destination Canada 加拿大, 1000 g, 35×25×10 cm, Canada Post-M line",
        "Public estimator, destination Canada — 加拿大, 1000 g and 35×25×10 cm. 6 Oct 2026 showed among others Canada Post-M, 10–20 working days. Those figures change; open the estimator again.",
    )
    fig_vol = _fig(
        "/img/shots/volume-voorbeeld.jpg",
        "Volume-weight example: 40×40×3 cm and 200 g on the scale becomes 600 g volume",
        "A worked example, not a warehouse photo. The same divisor 8000 is in the Canada Post-M rule in the estimator. You run your box there, destination Canada.",
        1200,
        640,
    )
    fig_diy = _fig(
        "/img/shots/oficial-diy.jpg",
        "ACBuy DIY form: link, name, specs, price in CNY, and a disclaimer that ACBuy does not sell its own stock",
        "DIY Order on acbuy.com. If the search bar cannot read the link, fill the form by hand. The green disclaimer says it: goods come from third parties. Capture 6 Oct 2026.",
    )
    body = f"""
<section class="hero">
  <div class="hero__bg" role="img" aria-label="Official ACBuy banner: plane and a search bar to paste a Chinese product link"></div>
  <div class="hero__scrim"></div>
  <div class="wrap">
    <span class="eyebrow">Independent guide, in English</span>
    <h1>ACBuy Spreadsheet: the guide to buying in China from Canada</h1>
    <p class="lead">How you paste a product link into the agent, how the w2clinks catalogue works, how a parcel travels to Canada, and what you check before CBSA.</p>
    <div class="sbox">
      <form id="w2c-search" action="{escape(W2C_ACBUY_SHEET)}" method="get" target="_blank" rel="nofollow noopener" role="search">
        <label class="skip" for="q">Search products on w2clinks</label>
        <input id="q" name="q" type="search" autocomplete="off" placeholder="Search sneakers, hoodie, jacket…">
        <input type="hidden" name="utm_source" value="{escape(HOST)}">
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
        <p class="lead">ACBuy does not sell its own goods. It buys for you in Chinese shops that do not ship abroad, receives the parcel in the warehouse, photographs it, stores it, and ships to Canada when you decide.</p>
        <p>That changes everything: you pay twice (first the product, later international), you wait twice, and in between you can still cancel, consolidate or switch lines. Payment and tickets stay on {escape(OFFICIAL)}.</p>
        <p><a class="btn" href="/how-to-use-acbuy/">Step-by-step guide</a></p>
      </div>
      {fig_home}
    </div>
  </div>
</section>
<section class="sec sec--tint" id="shots">
  <div class="wrap">
    <div class="split split--rev">
      <div>
        <span class="eyebrow" style="color:var(--acd)">How you buy</span>
        <h2>Paste a Chinese link, or search in the app</h2>
        <p class="lead">The official GuideBook starts here: paste a Taobao, 1688 or Weidian link, or type the name in the search bar. That is the whole trick of a purchasing agent — the Chinese shop sees ACBuy, you later see QC photos and a line to Canada.</p>
        <p>If the search bar cannot read the link, the DIY form is the next step: name, size, colour and price in yuan. International you pay later, from the warehouse.</p>
        <p><a class="btn" href="/how-to-use-acbuy/">Canadian step-by-step</a>
           <a class="btn btn--ghost" href="{escape(OFFICIAL)}shopping-guide">Official GuideBook</a></p>
      </div>
      {fig_guide}
    </div>
  </div>
</section>
<section class="sec" id="sheet-explain">
  <div class="wrap">
    <div class="split">
      <div>
        <span class="eyebrow" style="color:var(--acd)">A name that misleads</span>
        <h2>A spreadsheet is not an Excel file</h2>
        <p class="lead">In English the word still sounds like a grid of rows and columns. Here «spreadsheet» means a catalogue of product cards with a photo, a brand, a reference price and the link you paste into the agent.</p>
        <p>What you see on <a href="{escape(W2C)}/?{utm}" rel="nofollow noopener" target="_blank">w2clinks</a> are cards, not cells. You browse by category, filter by brand, gender, colour or material, and every fiche has the link the agent needs. That is the whole trick: turning a Taobao, 1688 or Weidian link into something you can order from Canada.</p>
        <p><a class="btn btn--ghost" href="/catalog/">How the catalogue works</a></p>
      </div>
      {fig_sheet}
    </div>
  </div>
</section>
<section class="sec sec--tint" id="cat-wall">
  <div class="wrap">
    <h2>Thirty-three categories for the first day</h2>
    <p class="lead">Each card opens that category in the catalogue. Start with one: five categories in the first haul is the fastest way to an expensive, awkward box.</p>
    <div class="cat-grid">{wall}</div>
    <p style="margin-top:26px"><a class="btn" href="/catalog/#categorias">What to check in each category</a></p>
  </div>
</section>
<section class="sec" id="states">
  <div class="wrap">
    <div class="split split--rev">
      <div>
        <span class="eyebrow" style="color:var(--acd)">Two payments</span>
        <h2>Nine statuses, three screens</h2>
        <p class="lead">First you pay the product plus China-domestic freight into the warehouse. International comes later, when you pick a line to Canada. The question «why is it stuck?» is almost always: you are looking at the wrong screen.</p>
        <ul class="tl">
          <li><b>Order Submitted</b><span>Order sent, product paid in China.</span></li>
          <li><b>Order Placed</b><span>ACBuy buys in the Chinese shop in your name.</span></li>
          <li><b>Seller Shipped</b><span>The Chinese seller has shipped.</span></li>
          <li><b>Arrived at Warehouse</b><span>Arrived at the warehouse.</span></li>
          <li><b>Inspection &amp; Storage</b><span>Check, photos and storage. Live labels are in the app.</span></li>
          <li><b>Shipping Requested</b><span>You consolidate and book the international line to Canada.</span></li>
          <li><b>Parcel Packed</b><span>The box is packed.</span></li>
          <li><b>Shipped</b><span>Left China.</span></li>
          <li><b>Delivered</b><span>Delivered; confirm receipt in the app.</span></li>
        </ul>
        <p>The first four sit under Order, then Warehouse, then Parcel. <a href="/how-to-use-acbuy/">Guide with the full path →</a></p>
      </div>
      {fig_pay}
    </div>
  </div>
</section>
<section class="sec sec--tint" id="lab">
  <div class="wrap">
    <div class="split">
      <div>
        <h2>Canada has lines, but not every line is open</h2>
        <p class="lead">The official estimator is public. Pick destination <strong>Canada — 加拿大</strong>, not the United States and not “North America”. The delivery address is a Canadian postal code (form A1A 1A1).</p>
        <p>On 6 Oct 2026, with 1000 g and 35×25×10 cm, the estimator showed among others Canada Post-M, 10–20 working days. Those amounts change by the week; treat them as a photo of that day and open the estimator before you buy. Import: <a href="https://www.cbsa-asfc.gc.ca/" rel="noopener">CBSA</a>.</p>
        <p><a class="btn" href="{escape(EST)}">Official estimator, destination Canada</a>
           <a class="btn btn--ghost" href="/acbuy-shipping-guide/">Shipping plan</a></p>
      </div>
      {fig_est}
    </div>
  </div>
</section>
<section class="sec" id="volume">
  <div class="wrap">
    <div class="split split--rev">
      <div>
        <span class="eyebrow" style="color:var(--acd)">The expensive mistake</span>
        <h2>The weight you pay is almost never the scale alone</h2>
        <p class="lead">The Canada Post-M rule in the estimator itself says it: volume weight = L×W×H (cm) / 8000, and they bill the greater of scale and volume. A down jacket is light and bulky: volume decides.</p>
        <p>Example: 40×40×3 cm is 4800 cm³, divided by 8000 is 600 g volume at 200 g real weight. If only that jacket travels, you pay 600 g. You enter your measurements in the estimator, destination Canada.</p>
        <p><a class="btn btn--ghost" href="/acbuy-shipping-guide/">Shipping plan with volume weight</a></p>
      </div>
      {fig_vol}
    </div>
  </div>
</section>
<section class="sec sec--tint" id="restricted">
  <div class="wrap">
    <div class="split">
      <div>
        <h2>Many products you cannot buy, even when they are listed</h2>
        <p class="lead">On the official site you will see cards without a price, or a DIY form instead of a shop card. That is not a bug of this homepage: the source link is not buyable through the agent, or the price could not be read.</p>
        <p>Rule: do not order without a real price and variants. Tobacco, alcohol and medicines do not travel. Restricted is a buying block, not a message from CBSA. The green disclaimer on the DIY screen says the same: ACBuy does not sell its own stock.</p>
      </div>
      {fig_diy}
    </div>
  </div>
</section>
<section class="sec" id="faq">
  <div class="wrap">
    <h2>Help, news and where to ask</h2>
    <p class="lead">Most first-order doubts repeat: two payments, English catalogue on w2clinks, volume weight, CBSA. They are answered in English on Help — its own URL, not an appendix of this homepage.</p>
    <p>On News we date what we ourselves checked on the platform. About us explains that this host is editorially independent. If you need to talk to ACBuy, the channel is in-app chat: we cannot see your account.</p>
    <p><a class="btn" href="/help/">All questions on Help</a>
       <a class="btn btn--ghost" href="/news/">Dated checks on News</a>
       <a class="btn btn--ghost" href="/about/">About us</a></p>
  </div>
</section>
"""
    return _shell(
        page_title(DESK, "buy in China from Canada, safely"),
        "Independent English guide: how you buy in China through ACBuy, how the w2clinks catalogue works, how a parcel travels to Canada.",
        f"https://{HOST}/",
        [faq_ld("en-CA", _ca_faqs())],
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
        "ACBuy catalogue on w2clinks: product cards with photo, brand and reference price",
        "A catalogue category: cards with image, brand and a reference price in yuan. Those prices change by the day. Capture 6 Oct 2026.",
        1200,
        900,
    )
    fig_zoek = _fig(
        "/img/shots/catalogus-zoek.jpg",
        "Hoodie search results in the ACBuy catalogue on w2clinks, with filters on the left",
        "Results with the filter column. Visible prices are platform samples and change daily. Capture 6 Oct 2026.",
        1200,
        900,
    )
    fig_diy = _fig(
        "/img/shots/oficial-diy.jpg",
        "ACBuy DIY form: paste the source link when the search bar cannot read the card",
        "The manual form accepts the source link and specs as text. Capture 6 Oct 2026; the total shown is from that example.",
    )
    body = f"""
<section class="sec sec--first">
  <div class="wrap">
    <div class="split">
      <div>
        <span class="eyebrow" style="color:var(--acc)">The catalogue</span>
        <h1>What ACBuy Spreadsheet is, and what you find in it</h1>
        <p class="lead">It is a catalogue of product cards, not an Excel file. You browse as in a shop: thirty-three categories, filters, and cards with a photo, a brand and the link for the agent. Below are those categories, with what you check in each.</p>
        <p>The name still misleads in English, because «spreadsheet» literally means a grid. There are no rows, cells or tabs here: there are fiches. Each fiche is a concrete product from a Chinese shop, with an image, a category and the link you then paste into ACBuy.</p>
      </div>
      {fig_sheet}
    </div>
  </div>
</section>
<section class="sec sec--tint">
  <div class="wrap">
    <div class="split split--rev">
      <div>
        <h2>Why a separate catalogue</h2>
        <p>An agent search bar returns the whole stock of Chinese shops, huge and in Chinese. A catalogue does the homework: someone already picked which fiches are worth it, put them in a category and staged the link.</p>
        <p>In practice: you find the fiche in the w2clinks catalogue, copy the source link and paste it into ACBuy’s search bar or the manual order form. The catalogue charges nothing and sells nothing: it saves the search work.</p>
        <p>The filters on the left are the most underestimated. Brand, gender, season, colour, material and price band turn thousands of fiches into something you can scan in two clicks.</p>
      </div>
      {fig_zoek}
    </div>
  </div>
</section>
<section class="sec" id="categorias">
  <div class="wrap">
    <h2>The thirty-three categories, and what you check in each</h2>
    <p class="lead">This is the catalogue. Each card opens that category on w2clinks. The line under it is not filler: it is the mistake that comes back most often in that category when you buy at a distance.</p>
    <div class="cat-grid cat-grid--rich">{wall}</div>
  </div>
</section>
<section class="sec sec--tint" id="first-category">
  <div class="wrap">
    <h2>How you pick the first category</h2>
    <p class="lead">If it is your first order, pick something flat and light: T-shirts, shorts, jewelry. Those arrive sooner, cost less to send, and let you check the whole circuit without risking much money.</p>
    <p>Leave bulky for the second order: down jackets, bags, hats. Not because they are worse, but because their shipping price depends on volume — and you only count that well after you have seen one round.</p>
    <p>Three categories with extra conditions: electronics (often lithium), glasses (fragile) and anything with a battery or magnet. Not every line to Canada accepts those. Check the estimator before you leave them in the warehouse.</p>
  </div>
</section>
<section class="sec">
  <div class="wrap">
    <h2>Uncomfortable fact: the catalogue searches in English</h2>
    <p class="lead">We checked it term by term on {escape(DATE)}. You want to know that before you type your first query in French.</p>
    <p>French or local words such as «souliers», «chandail» or «lunettes» often returned zero results. The English keys sneakers, hoodie, jacket, trousers, bag, glasses or watch returned pages of fiches. That is why the homepage search bar sends you to w2clinks with that English term.</p>
    <table class="eq">
      <thead><tr><th>If you are thinking of</th><th>Type</th></tr></thead>
      <tbody>
        <tr><td>running shoes</td><td>sneakers</td></tr>
        <tr><td>hoodie / sweatshirt</td><td>hoodie</td></tr>
        <tr><td>jacket</td><td>jacket</td></tr>
        <tr><td>pants</td><td>trousers</td></tr>
        <tr><td>bag</td><td>bag</td></tr>
        <tr><td>glasses</td><td>glasses</td></tr>
        <tr><td>watch</td><td>watch</td></tr>
      </tbody>
    </table>
  </div>
</section>
<section class="sec sec--tint">
  <div class="wrap">
    <div class="split">
      <div>
        <h2>From catalogue to order, without losing the link</h2>
        <p class="lead">The fiche is the start, not the till. The step that goes wrong most often is copying the wrong URL: the catalogue fiche has the source link of the Chinese shop; that is what ACBuy needs.</p>
        <p>If you paste the URL of the catalogue fiche itself, the agent does not know what to buy. Copy the Taobao, 1688 or Weidian link, paste it into ACBuy’s search bar, check price and variant, and pay international only after the QC photos match.</p>
        <p>If the search bar does not recognise the link, the manual order form remains: address, colour and size as text, plus a note. Skip fiches without a price — that source link is already dead in China.</p>
        <p><a class="btn" href="{escape(W2C_ACBUY_SHEET)}">Open the ACBuy catalogue on w2clinks</a>
           <a class="btn btn--ghost" href="/how-to-use-acbuy/">Step-by-step guide</a></p>
      </div>
      {fig_diy}
    </div>
  </div>
</section>
"""
    return _shell(
        page_title(DESK, "what it is and which categories you will find"),
        "Independent catalogue guide: thirty-three w2clinks categories, English search keys, and how you go from a fiche to an ACBuy order.",
        f"https://{HOST}/catalog/",
        [],
        body,
        "/catalog/",
    )


def build_help() -> str:
    pairs = _ca_faqs()
    g1 = _faq_html(pairs[0:3], open_first=True)
    g2 = _faq_html(pairs[3:7], open_first=False)
    g3 = _faq_html(pairs[7:9], open_first=False)
    g4 = _faq_html(pairs[9:13], open_first=False)
    g5 = _faq_html(pairs[13:15], open_first=False)
    fig_help = _fig(
        "/img/shots/oficial-guidebook-3.jpg",
        "Official ACBuy GuideBook: first payment in Checkout",
        "Questions about a concrete parcel belong in official chat, not on this guide. Capture 6 Oct 2026.",
    )
    body = f"""
<article class="pw">
  <span class="eyebrow" style="color:var(--acd)">Help</span>
  <h1>Help and questions about ACBuy in Canada</h1>
  <p class="lead">Fifteen questions that come back on first orders, answered with what we checked ourselves and with a link to the official source when the figure is not ours.</p>
  <p>The estimator destination is Canada, not the United States. The delivery address uses a Canadian postal code (form A1A 1A1).</p>
  <p>If your doubt is about a concrete parcel: the right counter is official support. We cannot see your account. This page explains the system before and after you order.</p>
  {fig_help}
  <h2>What ACBuy is and which language it uses</h2>
  {g1}
  <h2>What you will pay</h2>
  {g2}
  <h2>Import into Canada</h2>
  {g3}
  <h2>Warehouse, photos and what may travel</h2>
  {g4}
  <h2>If something is wrong</h2>
  {g5}
  <p><a class="btn" href="{escape(EST)}">Official estimator, destination Canada</a>
     <a class="btn btn--ghost" href="/acbuy-shipping-guide/">Shipping plan</a>
     <a class="btn btn--ghost" href="/news/">News</a></p>
</article>
"""
    return _shell(
        page_title(DESK, "help and frequently asked questions"),
        "Fifteen frequently asked questions about ACBuy, in English: payments, volume weight, CBSA in Canada, w2clinks catalogue.",
        f"https://{HOST}/help/",
        [faq_ld("en-CA", pairs)],
        body,
        "/help/",
    )


def build_news() -> str:
    items = [
        (
            "First round: estimator destination is Canada, not the United States",
            "We opened the official estimator with destination Canada. A US ZIP is the wrong country. A Canadian postal code has the form A1A 1A1. Live money sits in that estimator, not in this HTML.",
            "What that means for you: always filter on Canada before you compare lines. A US choice is not a Canadian home address.",
        ),
        (
            "Checked: the currency switch often only changes the symbol",
            "On the official site the digits often stay USD digits when you pick CAD; only the symbol swaps. This host shows CAD as a display of the China card (X-Rates 6 Oct 2026). Checkout stays the official estimator.",
            "What that means for you: read the amount in the app on the day you pay. A dollar sign on an unchanged figure is not a rate.",
        ),
        (
            "The w2clinks catalogue searches in English",
            "We searched the ACBuy catalogue on w2clinks. sneakers, hoodie and jacket returned pages of results; souliers, chandail or lunettes often returned zero. That is the index, not an empty shop. Measured {date}.".format(date=DATE),
            "What that means for you: type the English key, or tap a chip on the homepage. The search bar there sends you to w2clinks.",
        ),
        (
            "Official Help does not load without JavaScript",
            "https://www.acbuy.com/help is an app shell. Without JavaScript you do not see a warehouse rule. This guide does not copy an invented free-day count from there; the live text is in the app the morning you ship.",
            "What that means for you: storage length and extra angles you read in official Help that day, not as a frozen number on this site.",
        ),
        (
            "How we check this",
            "Shipping figures come from the public estimator, always with the same habit (destination Canada, 1000 g, 35×25×10 cm) and the date of the round. The catalogue we write about is w2clinks, not a product grid on this homepage. Ranked guides (shipping, review, how-to) stay their own URLs; this page does not overwrite them.",
            "We do not publish a SKU price in running copy. That changes by the week; that is what the official estimator is for, and it is public.",
        ),
    ]
    ld = itemlist_ld(
        url=f"https://{HOST}/news/",
        name="ACBuy CA desk checks",
        items=[(h, f"{p} {m}") for h, p, m in items],
    )
    cards = "".join(
        f'<article class="ncard"><h2>{escape(h)}</h2><p>{escape(p)}</p><p>{escape(m)}</p></article>'
        for h, p, m in items
    )
    body = f"""
<article class="pw">
  <span class="eyebrow" style="color:var(--acd)">News</span>
  <h1>What we checked on the platform, with a date</h1>
  <p class="lead">This is not a company newsletter. These are our own checks, with a date, so you know which information is recent and which has not been re-checked for months.</p>
  <p>First round: {escape(DATE)}. The checks below come from the same session, while we built this guide. They are not five separate posts from different days, and we do not present them that way. Later rounds go on top, with their own date.</p>
  <p>If a fact on this site changes, it will be listed here with the date of the new check, instead of being rewritten in silence.</p>
  {cards}
</article>
"""
    return _shell(
        page_title(DESK, "what we checked on the platform"),
        "Dated checks on ACBuy: shipping lines to Canada, currency, and how the catalogue searches.",
        f"https://{HOST}/news/",
        [ld],
        body,
        "/news/",
    )


def build_about() -> str:
    fig_about = _fig(
        "/img/shots/oficial-inicio.jpg",
        "Official ACBuy homepage, different from this guide",
        "The official site is a different URL from this guide. Capture 6 Oct 2026.",
    )
    body = f"""
<article class="pw">
  <span class="eyebrow" style="color:var(--acd)">About us</span>
  <h1>An independent site about ACBuy, in English</h1>
  <p class="lead">ACBuy Spreadsheet is not ACBuy. It is an editorial guide: how that agent works, and how you use the w2clinks catalogue from Canada.</p>
  <p>We do not take orders, we do not charge postage, we do not store goods and we cannot see an account. A problem with an order belongs on {escape(OFFICIAL)}.</p>
  {fig_about}
  <h2>How we work</h2>
  <h3>Where each fact comes from</h3>
  <p>Shipping figures come from the public estimator, always with destination, weight, dimensions and the date of the check. Import points to <a href="https://www.cbsa-asfc.gc.ca/" rel="noopener">CBSA</a>. What we have not checked, we do not publish.</p>
  <h3>Why you see few rates here</h3>
  <p>SKU prices change by the week. A frozen amount on this page would be misleading within days. We explain the mechanism and send you to <a href="{escape(EST)}">{escape(EST)}</a> for that day’s figure.</p>
  <h3>What the screenshots show</h3>
  <p>Captures of acbuy.com are from {escape(DATE)}. Product cards next to «spreadsheet» come from w2clinks, not from a product grid on this homepage. Amounts in a tutorial are examples of that day, not a till price for your box.</p>
  <h2>Contact</h2>
  <p>Write if a fact, a link or a translation breaks. We put the correction with a date on <a href="/news/">News</a>. Orders: in-app chat on ACBuy. This guide: <a href="mailto:{escape(MAIL)}">{escape(MAIL)}</a>.</p>
</article>
"""
    return _shell(
        page_title(DESK, "who we are and how to reach us"),
        "Independent English-language site about ACBuy: how we check facts, why we publish few rates, and how you write to us.",
        f"https://{HOST}/about/",
        [],
        body,
        "/about/",
    )


def _assert_ok(html: str, page: str) -> None:
    if page == "nf":
        err = []
        if "Page not found | ACBuy Spreadsheet" not in html:
            err.append("404 title not aligned with hipobuy.es")
        if "This page does not exist" not in html:
            err.append("404 h1")
        if "noindex" not in html:
            err.append("404 robots")
        if MAIL not in html or "acbuy-logo.svg" not in html:
            err.append("404 chrome")
        if "Catalog" not in html or "Guide" not in html:
            err.append("404 nav")
        if ".waf,.wabu,.wafb" not in html:
            err.append("404 missing waf hide")
        if 'lang="en-CA"' not in html:
            err.append("404 lang")
        if err:
            raise SystemExit(f"{page}: {'; '.join(err)}")
        return
    skip = {
        "missing #local dest briefing",
        "missing #local",
        "missing #catalog",
        "missing catalogue API",
        "missing FX_CCY CAD",
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
    if "Independence notice" not in html or "independent information site" not in html:
        err.append("missing independence disclaimer")
    fp = dest_local_pack("CA")["fingerprint"]
    if page in ("home", "help") and fp not in html:
        err.append("missing CA fingerprint")
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
    if page == "home":
        if html.count('class="sg-faq"') >= 8:
            err.append("faq dump on homepage")
        if ACB_CA in html or "Novedades" in html:
            err.append("planning dump on homepage")
        if "cat-30-shoes.png" not in html or "w2clinks.com/spreadsheet/acbuy" not in html:
            err.append("missing W2C Links categories")
        if 'class="fig"' not in html:
            err.append("missing illustrated figures")
        if "not an Excel file" not in html or "w2clinks" not in html:
            err.append("sheet-explain not aligned with hipobuy.es / w2clinks")
        if "Dezelfde indeling" in html:
            err.append("categories meta dump")
        if 'id="local"' in html or 'id="catalog"' in html:
            err.append("ops ids leftover on home")
        if 'href="/catalog/"' not in html:
            err.append("catalog nav missing")
        if page_title(DESK, "buy in China from Canada, safely") not in html:
            err.append("home title not aligned with hipobuy.es")
        if 'lang="en-CA"' not in html:
            err.append("home lang")
        if ".waf,.wabu,.wafb" not in html:
            err.append("home missing waf hide")
        if "Canada — 加拿大" not in html:
            err.append("missing estimator dest Canada")
    if page == "catalog":
        if "cat-30-shoes.png" not in html or 'id="categorias"' not in html:
            err.append("catalog page missing category wall")
        if "not an Excel file" not in html:
            err.append("catalog missing spreadsheet-not-excel copy")
        if "How you pick the first category" not in html:
            err.append("catalog missing first-category section")
        if "source link" not in html:
            err.append("catalog missing source-link copy")
    if page == "news":
        if "Novedades" in html:
            err.append("news meta leftover")
        if page_title(DESK, "what we checked on the platform") not in html:
            err.append("news title not aligned with hipobuy.es home formula")
    if err:
        raise SystemExit(f"{page}: {'; '.join(err)}")


def _desk_css_path() -> Path:
    return OUT / HOST / "overlay" / "assets" / "css" / "acbuy-ca-desk.css"


def _wordmark_path() -> Path:
    return OUT / HOST / "overlay" / "assets" / "images" / "acbuy-wordmark.png"


def write_wordmark(path: Path) -> Path:
    from PIL import Image, ImageDraw, ImageFont

    path.parent.mkdir(parents=True, exist_ok=True)
    w, h = 324, 70
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, 70, 70), 16, fill=(49, 179, 140, 255))
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
    for name in ("help", "news", "about", "catalog"):
        (dest / name).mkdir(exist_ok=True)
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
        "estimator-ca.jpg",
        "catalogus.jpg",
        "catalogus-zoek.jpg",
        "volume-voorbeeld.jpg",
    )
    missing += [n for n in shots if not (img_root / "shots" / n).is_file()]
    if not (img_root / "hero.jpg").is_file():
        missing.append("hero.jpg")
    if missing:
        raise SystemExit(f"missing images {missing}")
    pages = {
        "home": (dest / "index.html", build_home(), "home"),
        "help": (dest / "help" / "index.html", build_help(), "help"),
        "news": (dest / "news" / "index.html", build_news(), "news"),
        "about": (dest / "about" / "index.html", build_about(), "about"),
        "catalog": (dest / "catalog" / "index.html", build_catalog(), "catalog"),
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
CATCH_OLD = "    location / { return 301 https://allchinabuyspreadsheet.ca$request_uri; }\n"
CATCH_PLAIN = """    location / {
        try_files $uri $uri/ $uri/index.html =404;
    }
"""
CATCH_NEW = """    location / {
        try_files $uri $uri/ $uri/index.html =404;
        add_header Strict-Transport-Security "max-age=31536000" always;
        add_header Cache-Control "private, no-cache, must-revalidate" always;
        add_header X-Desk "acbuy-ca-independent" always;
    }
"""


def _reload_nginx(client) -> None:
    chk = _run(client, "nginx -t")
    print(chk)
    if "successful" not in chk.lower() and "ok" not in chk.lower():
        raise SystemExit("nginx -t failed")
    print(_run(client, "nginx -s reload"))


def _lift_ca_301(client, sftp) -> None:
    """Stop 301 into AllChinaBuy CA; serve this dest locally."""
    vhost = f"/www/server/panel/vhost/nginx/{HOST}.conf"
    stamp = time.strftime("%Y%m%d-%H%M%S")
    _run(client, f"cp -a '{vhost}' '/www/backup/acbuy-ca-nginx-{stamp}.conf'")
    with sftp.open(vhost, "r") as fh:
        text = fh.read().decode()
    changed = False
    if CATCH_OLD in text:
        text = text.replace(CATCH_OLD, CATCH_NEW, 1)
        changed = True
        print("lifted catch-all 301")
    elif CATCH_PLAIN in text:
        text = text.replace(CATCH_PLAIN, CATCH_NEW, 1)
        changed = True
        print("patched try_files with no-cache + X-Desk")
    elif 'X-Desk "acbuy-ca-independent"' in text:
        print("catch-all already independent no-cache")
    elif "try_files $uri $uri/ $uri/index.html =404" in text:
        print("catch-all already try_files")
    else:
        raise SystemExit("catch-all 301 needle not found")
    if OLD_API in text:
        text = text.replace(OLD_API, NEW_API, 1)
        changed = True
        print("patched /api/")
    if changed:
        tmp = Path("/tmp/acbuy-ca.conf")
        tmp.write_text(text, encoding="utf-8")
        sftp.put(str(tmp), vhost)

    gsc = f"/www/server/panel/vhost/nginx/extension/{HOST}/gsc-redirects.conf"
    raw = _run(client, f"cat '{gsc}'")
    if ACB_CA in raw:
        _run(client, f"cp -a '{gsc}' '/www/backup/acbuy-ca-gsc-{stamp}.conf'")
        keep = []
        for line in raw.splitlines(True):
            if ACB_CA in line and "return 301" in line:
                continue
            keep.append(line)
        new = "".join(keep)
        tmp = Path("/tmp/acbuy-ca-gsc.conf")
        tmp.write_text(new, encoding="utf-8")
        sftp.put(str(tmp), gsc)
        print("stripped AllChinaBuy 301s from gsc-redirects", raw.count("return 301"), "->", new.count("return 301"))
    _reload_nginx(client)


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
        local_tmp = Path("/tmp") / f"acbuy-ca-wrap-{rel.replace('/', '_')}"
        local_tmp.write_text(out, encoding="utf-8")
        sftp.put(str(local_tmp), remote)
        print("WRAP", rel, "in", len(raw), "out", len(out.encode("utf-8")))
        local_tmp.unlink(missing_ok=True)


def put() -> None:
    files = generate()
    client = _connect()
    stamp = time.strftime("%Y%m%d-%H%M%S")
    bak = f"/www/backup/acbuy-ca-cms-{stamp}"
    root = f"/www/wwwroot/{HOST}"
    _run(
        client,
        f"mkdir -p '{bak}' '{root}/help' '{root}/news' '{root}/about' '{root}/catalog' "
        f"'{root}/assets/css' '{root}/assets/images' '{root}/img/cat' '{root}/img/shots'",
    )
    sftp = client.open_sftp()
    _lift_ca_301(client, sftp)
    mapping = {
        "home": f"{root}/index.html",
        "help": f"{root}/help/index.html",
        "news": f"{root}/news/index.html",
        "about": f"{root}/about/index.html",
        "catalog": f"{root}/catalog/index.html",
        "nf": f"{root}/404.html",
    }
    for key, remote in mapping.items():
        local = files[key]
        raw = local.read_text(encoding="utf-8")
        if key in ("home", "help") and dest_local_pack("CA")["fingerprint"] not in raw:
            raise SystemExit(f"refusing {key} without fingerprint")
        if key == "home" and (INVITE in raw or "90 days" in raw.lower()):
            raise SystemExit("refusing home with invite or 90-day copy")
        _run(client, f"test -f '{remote}' && cp -a '{remote}' '{bak}/{key}.html' || true")
        sftp.put(str(local), remote)
        print("PUT", remote, local.stat().st_size)
    theme = OUT / "shared" / "themes" / "acbuy-theme.css"
    sftp.put(str(theme), f"{root}/assets/css/acbuy-theme.css")
    sftp.put(str(files["css"]), f"{root}/assets/css/acbuy-ca-desk.css")
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
        f"chown -R www:www '{root}/index.html' '{root}/404.html' '{root}/help' '{root}/news' '{root}/about' '{root}/catalog' '{root}/favicon.ico' '{root}/favicon1.ico' '{root}/assets/css' "
        f"'{root}/img' '{root}/acbuy-shipping-guide' '{root}/is-acbuy-legit' '{root}/how-to-use-acbuy' '{root}/acbuy-coupons' "
        f"'{root}/acbuy-spreadsheet' '{root}/blog' 2>/dev/null || true",
    )
    sftp.close()
    print("backup", bak)
    client.close()


def live_check() -> None:
    import ssl
    import urllib.request

    ctx = ssl.create_default_context()
    https = urllib.request.HTTPSHandler(context=ctx)

    class NR(urllib.request.HTTPRedirectHandler):
        def redirect_request(self, req, fp, code, msg, headers, newurl):
            return None

    def fetch(url, follow=True):
        req = urllib.request.Request(
            url,
            headers={"User-Agent": "acbuy-ca-cms/1.0", "Cache-Control": "no-cache"},
        )
        handlers = [https] if follow else [https, NR()]
        opener = urllib.request.build_opener(*handlers)
        try:
            with opener.open(req, timeout=25) as resp:
                return resp.status, resp.geturl(), resp.headers.get("Location") or "", resp.read()
        except urllib.error.HTTPError as e:
            return e.code, url, e.headers.get("Location") or "", e.read() if e.fp else b""

    fail = 0
    fp = dest_local_pack("CA")["fingerprint"]
    checks = [
        (f"https://{HOST}/", "home", True),
        (f"https://{HOST}/help/", "help", True),
        (f"https://{HOST}/news/", "news", False),
        (f"https://{HOST}/about/", "about", False),
        (f"https://{HOST}/catalog/", "catalog", False),
        (f"https://{HOST}/acbuy-shipping-guide/", "ranked", False),
        (f"https://{HOST}/is-acbuy-legit/", "ranked", False),
        (f"https://{HOST}/how-to-use-acbuy/", "ranked", False),
    ]
    for url, kind, need_fp in checks:
        code, final, loc, body = fetch(url, follow=True)
        html = body.decode("utf-8", "replace")
        print(kind, code, "bytes", len(body), "cms", "acbuy-logo.svg" in html or "acbuy-wordmark" in html)
        if ACB_CA in (final or "") or ACB_CA in (loc or ""):
            print(" FAIL still 301 into AllChinaBuy CA"); fail += 1
        if code != 200:
            print(" FAIL status"); fail += 1
        if "acbuy-logo.svg" not in html:
            print(" FAIL official logo"); fail += 1
        if 'lang="en-CA"' not in html:
            print(" FAIL lang en-CA"); fail += 1
        if ".waf,.wabu,.wafb" not in html:
            print(" FAIL waf hide"); fail += 1
        if need_fp and fp not in html:
            print(" FAIL fingerprint"); fail += 1
        if kind in ("home", "help", "news", "about", "catalog"):
            if "/api/products/" in html or "Voor een huisadres in Nederland" in html:
                print(" FAIL api/huisadres leftover"); fail += 1
            if "w2cspreadsheet" in html.lower() or "W2C Spreadsheet" in html:
                print(" FAIL w2cspreadsheet leftover"); fail += 1
        if kind == "home":
            if INVITE in html or re.search(r"90\s*days", html, re.I):
                print(" FAIL invite/90"); fail += 1
            if page_title(DESK, "buy in China from Canada, safely") not in html:
                print(" FAIL home title"); fail += 1
            if ACB_CA in html or "Novedades" in html:
                print(" FAIL planning dump on home"); fail += 1
            if html.count('class="sg-faq"') >= 8:
                print(" FAIL faq dump on home"); fail += 1
            if "FAQPage" not in html:
                print(" FAIL home FAQPage"); fail += 1
            if "cat-30-shoes.png" not in html or "w2clinks.com/spreadsheet/acbuy" not in html:
                print(" FAIL missing W2C categories"); fail += 1
            if 'class="fig"' not in html:
                print(" FAIL missing photos"); fail += 1
            if MAIL not in html or "Independence notice" not in html:
                print(" FAIL footer independence/mail"); fail += 1
            if "not an Excel file" not in html:
                print(" FAIL sheet-explain"); fail += 1
            if 'id="local"' in html or 'id="catalog"' in html:
                print(" FAIL ops ids on home"); fail += 1
            if "/catalog/" not in html:
                print(" FAIL catalog nav"); fail += 1
            if "Canada — 加拿大" not in html:
                print(" FAIL estimator dest"); fail += 1
            for alien in ("Packstation", "Nederlandse postcode"):
                if alien in html:
                    print(" FAIL alien", alien); fail += 1
        if kind == "catalog":
            if html.count('class="cat"') < 30 or "not an Excel file" not in html:
                print(" FAIL catalog page"); fail += 1
            if "How you pick the first category" not in html or "source link" not in html:
                print(" FAIL catalog hipobuy.es sections"); fail += 1
            if f"acbuy-ca-desk.css?v={CSS_V}" not in html:
                print(" FAIL catalog css bust"); fail += 1
        if kind == "news" and page_title(DESK, "what we checked on the platform") not in html:
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
            if 'id="lang-modal"' in html or re.search(r">\s*p>", html):
                print(" FAIL ranked english chrome"); fail += 1
            if f"acbuy-ca-desk.css?v={CSS_V}" not in html or "allchinabuy-theme.css" in html:
                print(" FAIL ranked mint css"); fail += 1
            if "country-desk-chrome" not in html:
                print(" FAIL ranked chrome lock id"); fail += 1
    code, _, _, nf_body = fetch(f"https://{HOST}/this-page-does-not-exist-cms/", follow=True)
    nf = nf_body.decode("utf-8", "replace")
    print("404", code, "bytes", len(nf_body), "title", "Page not found" in nf)
    if code != 404:
        print(" FAIL 404 status"); fail += 1
    if "Page not found | ACBuy Spreadsheet" not in nf:
        print(" FAIL 404 title"); fail += 1
    if "This page does not exist" not in nf or "Catalog" not in nf:
        print(" FAIL 404 chrome/nav"); fail += 1
    if "acbuy-logo.svg" not in nf or MAIL not in nf:
        print(" FAIL 404 logo/mail"); fail += 1
    if "noindex" not in nf:
        print(" FAIL 404 robots"); fail += 1
    # Same-agent NL dest stays independent. AllChinaBuy CA stays independent.
    code, _, loc, _ = fetch(f"https://allchinabuyspreadsheet.nl/", follow=False)
    print("twin NL extra", code, loc)
    if code not in (301, 302, 308) or NL_HOST not in (loc or ""):
        print(" FAIL NL extra twin"); fail += 1
    code, final, loc, _ = fetch(f"https://{NL_HOST}/", follow=False)
    print("nl dest", code, final or loc)
    if code not in (200,):
        print(" FAIL NL dest"); fail += 1
    code, final, loc, _ = fetch(f"https://{ACB_CA}/", follow=False)
    print("allchinabuy ca", code, final or loc)
    if code != 200 or HOST in (final or "") or HOST in (loc or ""):
        print(" FAIL AllChinaBuy CA collapsed"); fail += 1
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
