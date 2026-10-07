#!/usr/bin/env python3
"""Deepen basetaospreadsheet.com hub without touching ranked inner HTML.

This .com host is a hub (not a customs territory). GSC money query is
“basetao spreadsheet” on /. Do not PUT a 5KB template over ranked inners.
Do not dump /api/products/ on the homepage (the endpoint 404s).

Cut: homepage title/H1/description, nav labels, 33-icon category wall,
/start/, /help/ (≥12 details.sg-faq). Ranked referral / shipping /
calculator / review bodies stay.
"""
from __future__ import annotations

import json
import os
import re
import sys
import time
from html import escape
from pathlib import Path
from urllib.parse import quote

_TOOLS = Path(__file__).resolve().parent
if str(_TOOLS) not in sys.path:
    sys.path.insert(0, str(_TOOLS))
from desk_template import (
    SKIP_CSS,
    _check_local_section,
    assert_dest_packs_unique,
    breadcrumb_ld,
    dest_local_pack,
    faq_ld,
    independence_copy,
    inject_jsonld,
    itemlist_ld,
    lab_copy,
    local_cta,
    local_guide_html,
    long_faqs,
    organization_ld,
    skip_label,
    skip_link,
    validate_desk,
    webpage_ld,
)

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "sites"
HOST = "basetaospreadsheet.com"
EST = "https://www.basetao.com/best-taobao-agent-service/how_make/cost.html"
OFFICIAL = "https://www.basetao.com/"
HELP_OFFICIAL = "https://www.basetao.com/best-taobao-agent-service/how_make/basetao_faq.html"
W2C = "https://w2clinks.com/spreadsheet/basetao/"
W2C_CATS = "https://w2clinks.com/categories/"
MAIL = "cnfd85269032661@gmail.com"
DATE = "7 Oct 2026"
STORAGE = (
    "Official FAQ: Basetao offers 120 days of free storage "
    f"({HELP_OFFICIAL}); confirm that live article the morning you ship"
)
TITLE = "BaseTao Spreadsheet: Weidian, Taobao and 1688 finds"
H1 = "BaseTao Spreadsheet — Weidian, Taobao and 1688 finds"
DESC = (
    "BaseTao spreadsheet on basetaospreadsheet.com: live Weidian, Taobao and "
    "1688 finds via w2clinks, QC notes, freight estimate. Not Excel, not checkout. "
    "Pay on basetao.com. This .com hub is not a customs territory."
)
ALIENS = ("1010 Wien", "Packstation", "form A1A 1A1", "Poste Italiane", "00-001 Warszawa")

KEEP = [
    ("/basetao-referral-code/", "Referral"),
    ("/basetao-shipping-calculator/", "Shipping calculator"),
    ("/basetao-calculator/", "Haul calculator"),
    ("/basetao-review/", "Review"),
]

# w2clinks.com/categories/ icon wall (same 33 as NL-complete dests).
# Prefer same-host ranked category hubs when they exist.
CAT_WALL = [
    ("ENFANTS RICHES DEPRIMES", "cat-21-enfants-riches-deprimes.png", None),
    ("SNEAKERS", "cat-30-shoes.png", "/shoes381/"),
    ("SLIPPERS", "cat-27-slippers.png", None),
    ("T-SHIRT", "cat-03-t-shirt.png", "/t-shirts/"),
    ("POLO", "cat-04-polo.png", None),
    ("SHIRT", "cat-05-shirt.png", None),
    ("SHORTS", "cat-07-shorts.png", "/pants-shorts/"),
    ("VEST", "cat-20-vest.png", None),
    ("LONG SLEEVED", "cat-25-long-sleeved.png", None),
    ("HOODIE", "cat-06-hoodie.png", "/hoodies-sweaters/"),
    ("SWEATER", "cat-11-sweater.png", "/hoodies-sweaters/"),
    ("SHAWL", "cat-12-shawl.png", None),
    ("JACKET", "cat-13-jacket.png", "/jackets839/"),
    ("SHELL JACKET", "cat-18-jacket.png", "/jackets839/"),
    ("FLEECE JACKET", "cat-17-fleece-jacket.png", "/jackets839/"),
    ("DOWN JACKETS", "cat-08-down-jackets.png", "/jackets839/"),
    ("TROUSERS", "cat-19-trousers.png", "/pants-shorts/"),
    ("Jersey", "cat-jersey.png", "/jersey/"),
    ("FEMALE STYLE", "cat-28-femaie-styie.png", "/women/"),
    ("Electronics", "cat-electronics.png", "/electronics/"),
    ("GLOVES", "cat-15-giove.png", "/accessories/"),
    ("BAG", "cat-00-bag.png", "/bags/"),
    ("HAT", "cat-01-hat.png", "/headwear/"),
    ("JEWELRY", "cat-02-jewelry.png", "/accessories/"),
    ("UNDERWEAR", "cat-09-underwear.png", None),
    ("BELT", "cat-10-belt.png", "/accessories/"),
    ("KNEEPAD", "cat-16-kneepad.png", None),
    ("SOCKS", "cat-26-socks.png", None),
    ("HEADGEAR", "cat-22-headgear.png", "/headwear/"),
    ("EARMUFF", "cat-23-earmuff.png", "/headwear/"),
    ("SCARF", "cat-24-scarf.png", "/accessories/"),
    ("GLASSES", "cat-31-glasses.png", "/accessories/"),
    ("WATCH", "cat-32-watch.png", "/accessories/"),
]

SITEMAP_EXTRA = [
    "/",
    "/start/",
    "/help/",
    "/about/",
    "/accessories/",
    "/bags/",
    "/basetao-agent/",
    "/basetao-avis/",
    "/basetao-calculator/",
    "/basetao-discord/",
    "/basetao-reddit/",
    "/basetao-referral-code/",
    "/basetao-review/",
    "/basetao-shipping-calculator/",
    "/basetao-vs-superbuy/",
    "/electronics/",
    "/headwear/",
    "/hoodies-sweaters/",
    "/jackets839/",
    "/jersey/",
    "/other-stuff/",
    "/pants-shorts/",
    "/shoes381/",
    "/t-shirts/",
    "/women/",
    "/basetao-coupon-tracker-2026.html",
    "/basetao-real-shipping-bills-2026.html",
    "/basetao-shipping-lines-2026.html",
    "/basetao-user-reports-2026.html",
]

EXTRA_CSS = SKIP_CSS + """
.w2c-cat-grid-icons{display:grid;grid-template-columns:repeat(auto-fill,minmax(96px,1fr));gap:10px}
.w2c-cat-icon-card{display:flex;flex-direction:column;align-items:center;gap:6px;padding:10px 6px;border:1px solid var(--border,#e5e7eb);border-radius:12px;text-align:center;text-decoration:none;color:inherit;background:#fff;font-size:11px;font-weight:600;line-height:1.25}
.w2c-cat-icon-card img{width:56px;height:56px;object-fit:contain}
.w2c-cat-icon-card:hover{border-color:var(--primary,#e11d48)}
.sg-faq{border:1px solid var(--border,#e5e7eb);border-radius:10px;padding:10px 14px;margin:8px 0;background:#fff}
.sg-faq summary{cursor:pointer;font-weight:700}
"""

HUBS = {
    "com": {
        "host": HOST,
        "lang": "en",
        "loc": "en",
        "dest": None,
        "dest_label": "a country in the estimator",
        "ccy": "USD",
        "title": TITLE,
        "h1": H1,
        "keep": KEEP,
    },
}


def _facts() -> dict:
    spec = HUBS["com"]
    return {
        "agent": "BaseTao",
        "host": HOST,
        "lang": spec["lang"],
        "loc": spec["loc"],
        "dest": spec.get("dest"),
        "dest_label": spec["dest_label"],
        "ccy": spec["ccy"],
        "storage": STORAGE,
        "estimator": EST,
        "official": OFFICIAL,
        "date": DATE,
        "email": MAIL,
        "keep": KEEP,
        "codes_off_title": [],
        "strict_html_codes": False,
        "customs": "the destination customs site named in the estimator",
        "customs_url": "",
    }


def _cat_href(name: str, local: str | None) -> str:
    if local:
        return local
    return f"{W2C}?category={quote(name)}&page=1&sort=newest"


def _wall() -> str:
    tiles = []
    for name, img, local in CAT_WALL:
        href = _cat_href(name, local)
        ext = ' target="_blank" rel="noopener"' if href.startswith("http") else ""
        src = f"https://w2clinks.com/public/static/w2c/categories/{img}?v=24"
        tiles.append(
            f'<a class="w2c-cat-icon-card" href="{escape(href)}"{ext}>'
            f'<img src="{escape(src)}" alt="{escape(name)}" width="56" height="56" '
            f'loading="lazy" decoding="async"><span>{escape(name)}</span></a>'
        )
    return (
        '<section class="sg-sec" id="cat-wall"><h2>Catalogue wall</h2>'
        '<p class="ssub">Same 33 icons as '
        f'<a href="{escape(W2C_CATS)}" rel="noopener">w2clinks.com/categories/</a>. '
        "Local hubs on this host stay; the rest open the live BaseTao sheet on w2clinks. "
        "The spreadsheet is not Excel.</p>"
        f'<div class="w2c-cat-grid-icons">{"".join(tiles)}</div></section>'
    )


def _header(page: str) -> str:
    cat = "#catalog" if page == "home" else "/#catalog"
    loc = "#local" if page in ("home", "start", "help") else "/#local"
    nav = [
        (cat, "Catalogue"),
        ("/basetao-shipping-calculator/", "Shipping"),
        ("/help/", "Help"),
        ("/about/", "About"),
        ("/basetao-review/", "Review"),
        (loc, "Local checks"),
    ]
    links = "".join(
        f'<a href="{escape(href)}"{ " class=\"active\"" if href.endswith(f"/{page}/") or (page=="help" and href=="/help/") or (page=="about" and href=="/about/") else ""}>{escape(lab)}</a>'
        for href, lab in nav
    )
    return f"""<header class="site-header">
  <div class="container header-inner">
    <a class="brand" href="/start/"><img class="brand-logo" src="/assets/images/basetao-logo.png" alt="BaseTao"></a>
    <nav class="header-nav">{links}</nav>
    <div class="header-actions">
      <a class="btn btn-outline" href="{escape(W2C)}" rel="noopener">Spreadsheet</a>
      <a class="btn btn-primary" href="{escape(OFFICIAL)}" rel="noopener sponsored">Register</a>
    </div>
  </div>
</header>"""


def _footer() -> str:
    keep = "".join(f'<a href="{escape(h)}">{escape(l)}</a><br>' for h, l in KEEP)
    return f"""<footer class="site-footer">
  <div class="container footer-grid">
    <div><strong>BaseTao · {escape(HOST)}</strong>
      <p class="footer-note">Independent information desk. Not checkout.</p>
      <p class="legal-note">{escape(independence_copy(_facts()))}</p>
      <p class="legal-note">{escape(MAIL)}</p></div>
    <div><strong>Already ranking</strong>
      <p>{keep}
      <a href="/start/">Start</a><br>
      <a href="/help/">Help</a><br>
      <a href="/about/">About</a></p></div>
    <div><strong>Official</strong>
      <p><a href="{escape(OFFICIAL)}">BaseTao</a><br>
      <a href="{escape(EST)}">Freight estimate</a><br>
      <a href="{escape(W2C)}" rel="noopener">w2clinks BaseTao sheet</a></p></div>
  </div>
</footer>"""


def _chrome_head(*, title: str, desc: str, canonical: str, crumbs: list[tuple[str, str]]) -> str:
    facts = _facts()
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{escape(title)}</title>
<meta name="description" content="{escape(desc)}">
<link rel="canonical" href="{escape(canonical)}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/css/desk-cms.css?v=20261007-basetao">
<link rel="stylesheet" href="/assets/css/basetao-theme.css?v=20261007-basetao">
<style>{EXTRA_CSS}</style>
</head>
<body>
"""
    html = inject_jsonld(
        html,
        webpage_ld(url=canonical, name=title, desc=desc, lang="en", brand="BaseTao", host=HOST),
        organization_ld(
            name=f"{HOST} independent desk",
            url=f"https://{HOST}/",
            email=MAIL,
            lang="en",
            desc=desc,
        ),
        breadcrumb_ld(crumbs),
    )
    return html


def _local_plus() -> str:
    facts = _facts()
    html = local_guide_html(facts).strip()
    extra = (
        f'<p class="local-src">{escape(dest_local_pack(None)["fingerprint"])}. '
        "This .com hub is not a customs territory. Pick US, CA, FR, ES, AT… in "
        f'<a href="{escape(EST)}">{escape(EST)}</a> — this HTML is not checkout.</p>'
    )
    if not html.endswith("</section>"):
        raise RuntimeError("missing #local section")
    return html[: -len("</section>")] + extra + "\n</section>"


def _spreadsheet_faqs() -> list[tuple[str, str]]:
    facts = _facts()
    extra = [
        (
            "What is a BaseTao spreadsheet?",
            "A BaseTao spreadsheet is a finds index: Weidian, Taobao and 1688 links you "
            "research before pasting into the agent. On this host the live catalog is "
            f"{W2C} (w2clinks). It is not a Google Sheet, not Excel, and not the BaseTao "
            f"fee table. Checkout stays on {OFFICIAL}. This hub does not dump a products API.",
        ),
        (
            "Is this Excel or a downloadable CSV?",
            "No. Files freeze; listings move. This desk points at the live w2clinks "
            "BaseTao sheet and at ranked guides already on this host. We do not host a "
            "basetao_spreadsheet_2026.csv download.",
        ),
        (
            "BaseTao spreadsheet vs BaseTao review — which URL?",
            "Google queries for “basetao spreadsheet” should land on this homepage. "
            "Trust / legit / QC verdict stays on /basetao-review/. Freight lines stay on "
            "/basetao-shipping-calculator/. Referral stacking stays on /basetao-referral-code/.",
        ),
        (
            "How do I buy from this BaseTao spreadsheet?",
            f"Open a category or {W2C}, copy the listing URL, paste it into {OFFICIAL}, "
            "pay there, check warehouse QC photos, then run the official freight estimate "
            "with a real country — not this hostname and not “EU” as one country.",
        ),
    ]
    pairs = extra + long_faqs(facts)
    cleaned: list[tuple[str, str]] = []
    for q, a in pairs:
        a = a.replace("/api/products/", "the live w2clinks BaseTao sheet")
        cleaned.append((q, a))
    return cleaned


def build_home() -> str:
    facts = _facts()
    title = TITLE
    canonical = f"https://{HOST}/"
    crumbs = [("Home", canonical)]
    lab = lab_copy(facts)
    html = _chrome_head(title=title, desc=DESC, canonical=canonical, crumbs=crumbs)
    faq_pairs = _spreadsheet_faqs()[:8]
    html = inject_jsonld(
        html,
        faq_ld("en", faq_pairs),
        itemlist_ld(
            url=canonical,
            name="BaseTao spreadsheet categories",
            items=[(name, local or W2C) for name, _img, local in CAT_WALL],
        ),
    )
    html += skip_link(skip_label("en"))
    html += _header("home")
    html += f"""<main id="main" class="container">
<section class="sg-hero">
  <h1>{escape(H1)}</h1>
  <p class="hsub">Live finds via <a href="{escape(W2C)}" rel="noopener">w2clinks</a> — not Excel, not checkout. Pay and warehouse QC stay on {escape(OFFICIAL)}. This .com hub is not a customs territory; pick a real country in the estimator.</p>
  <p class="eu-badge">Hub · USD display · not a customs territory</p>
  <div class="sg-ctas">
    <a class="btn btn-primary" href="#catalog">Catalogue</a>
    <a class="btn btn-outline" href="{escape(W2C)}" rel="noopener">Open w2clinks sheet</a>
    <a class="btn btn-outline" href="{escape(EST)}">Freight estimate</a>
  </div>
</section>
{_local_plus()}
<section class="sg-sec" id="agent"><h2>BaseTao</h2>
<p>BaseTao is a purchasing agent, not a shop. {escape(HOST)} is a hub, not a customs territory.</p>
<p>Orders, payment and warehouse photos stay on {escape(OFFICIAL)}. This hostname never takes a card.</p></section>
<section class="sg-sec" id="sheet-explain"><h2>Spreadsheet</h2>
<p>The spreadsheet on {escape(HOST)} is an index, not Excel and not checkout. The live catalog this desk names is <strong>w2clinks</strong> at <a href="{escape(W2C)}" rel="noopener">{escape(W2C)}</a>.</p>
<p>Category icons match {escape(W2C_CATS)}. Lab {escape(DATE)}.</p></section>
<section class="sg-sec" id="restricted"><h2>Restricted</h2>
<p>Restricted is a platform purchase block, not a customs seizure notice for this hostname.</p>
<p>Dead Weidian or Taobao links are not a checkout you can force toward a country in the estimator.</p></section>
{_wall()}
<section class="sg-mw" id="catalog">
  <h2>Live BaseTao finds</h2>
  <p class="ssub">The homepage does not dump a products API (that endpoint 404s here). Browse the live sheet, or open a category hub already on this host.</p>
  <p><a class="btn btn-primary" href="{escape(W2C)}" rel="noopener">Open the w2clinks BaseTao spreadsheet</a>
  <a class="btn btn-outline" href="/shoes381/">Sneakers hub</a>
  <a class="btn btn-outline" href="/jersey/">Jersey hub</a>
  <a class="btn btn-outline" href="/hoodies-sweaters/">Hoodies hub</a></p>
</section>
<section class="sg-sec" id="states"><h2>a country in the estimator</h2>
<p class="ssub">This hostname is not a customs territory. Open the official estimator with a real country code — not this TLD, not “EU” as one country.</p>
<p>{escape(independence_copy(facts))}</p></section>
<section class="sg-sec" id="shots"><h2>Official app</h2>
<p class="ssub">Screenshots and live money stay on the official BaseTao site, dated {escape(DATE)}.</p>
<p><a class="btn btn-outline" href="{escape(OFFICIAL)}" rel="noopener">Open BaseTao</a>
<a class="btn btn-primary" href="{escape(EST)}" rel="noopener">Freight estimate</a></p></section>
<section class="sg-sec" id="lab"><h2>{escape(lab["h2"])}</h2>
<p class="ssub">{lab["ssub"]}</p>
<p><a class="btn btn-primary" href="{escape(EST)}">{escape(lab["cta"])}</a></p></section>
<section class="sg-sec" id="kept"><h2>Already ranking on this host</h2>
<div class="keep">{"".join(f'<a href="{escape(h)}">{escape(l)}</a>' for h, l in KEEP)}</div></section>
<section class="sg-sec" id="faq"><h2>FAQ</h2>
<p class="ssub">Visible FAQs live on Help. This homepage keeps FAQPage JSON-LD only.</p>
<p><a class="btn btn-outline" href="/help/">Open Help</a></p></section>
</main>
{_footer()}
</body></html>
"""
    return html


def build_start() -> str:
    facts = _facts()
    title = "Start | BaseTao Spreadsheet"
    desc = (
        "Start with the BaseTao spreadsheet: open the live w2clinks finds index, "
        "paste a Weidian/Taobao/1688 URL into basetao.com, then run the freight estimate."
    )
    canonical = f"https://{HOST}/start/"
    html = _chrome_head(
        title=title,
        desc=desc,
        canonical=canonical,
        crumbs=[("Home", f"https://{HOST}/"), ("Start", canonical)],
    )
    html += skip_link(skip_label("en"))
    html += _header("start")
    html += f"""<main id="main" class="container">
<section class="sg-hero">
  <h1>Start | BaseTao Spreadsheet</h1>
  <p class="hsub">Four steps from a finds link to a warehouse photo. This desk is not Excel and not checkout.</p>
  <div class="sg-ctas">
    <a class="btn btn-primary" href="/#catalog">Catalogue</a>
    <a class="btn btn-outline" href="{escape(W2C)}" rel="noopener">Open w2clinks sheet</a>
    <a class="btn btn-outline" href="/help/">Help</a>
  </div>
</section>
{_local_plus()}
<section class="sg-sec" id="steps">
  <h2>How to start</h2>
  <ol class="local-steps">
    <li><strong>Open the spreadsheet</strong><span>Use the 33-icon wall on the homepage or the live BaseTao sheet at <a href="{escape(W2C)}" rel="noopener">{escape(W2C)}</a>. The sheet is named <strong>w2clinks</strong>, not Excel.</span></li>
    <li><strong>Paste into BaseTao</strong><span>Copy the Weidian, Taobao or 1688 URL and paste it on <a href="{escape(OFFICIAL)}">{escape(OFFICIAL)}</a>. Payment never happens on {escape(HOST)}.</span></li>
    <li><strong>Read warehouse QC</strong><span>Photos land in the official app. Extra angles are often paid. Do not book international freight until you accept the photos.</span></li>
    <li><strong>Estimate a real country</strong><span>This .com hub is not a customs territory. Open <a href="{escape(EST)}">{escape(EST)}</a> with US, CA, FR, ES, AT… not this hostname and not “EU” as one country.</span></li>
  </ol>
</section>
<section class="sg-sec" id="kept"><h2>Already ranking on this host</h2>
<div class="keep">{"".join(f'<a href="{escape(h)}">{escape(l)}</a>' for h, l in KEEP)}</div></section>
</main>
{_footer()}
</body></html>
"""
    return html


def build_help() -> str:
    facts = _facts()
    title = "Help | BaseTao Spreadsheet"
    desc = (
        "BaseTao spreadsheet help: what the sheet is, how to paste a Weidian link "
        "into basetao.com, QC, freight estimate, storage. Not Excel, not checkout."
    )
    canonical = f"https://{HOST}/help/"
    pairs = _spreadsheet_faqs()
    items = []
    for i, (q, a) in enumerate(pairs):
        op = " open" if i == 0 else ""
        items.append(
            f'<details class="sg-faq"{op}><summary>{escape(q)}</summary>'
            f"<p>{escape(a)}</p></details>"
        )
    html = _chrome_head(
        title=title,
        desc=desc,
        canonical=canonical,
        crumbs=[("Home", f"https://{HOST}/"), ("Help", canonical)],
    )
    html = inject_jsonld(html, faq_ld("en", pairs))
    html += skip_link(skip_label("en"))
    html += _header("help")
    html += f"""<main id="main" class="container">
<section class="sg-hero">
  <h1>Help | BaseTao Spreadsheet</h1>
  <p class="hsub">Fifteen long answers. Visible <code>details.sg-faq</code> live only here — not on the homepage.</p>
</section>
{_local_plus()}
<section class="sg-sec" id="faq"><h2>FAQ</h2>{"".join(items)}</section>
</main>
{_footer()}
</body></html>
"""
    return html


def build_about() -> str:
    facts = _facts()
    title = "About | BaseTao Spreadsheet"
    desc = (
        "basetaospreadsheet.com is an independent BaseTao spreadsheet desk, not "
        "basetao.com. Not a customs territory. Contact and independence."
    )
    canonical = f"https://{HOST}/about/"
    html = _chrome_head(
        title=title,
        desc=desc,
        canonical=canonical,
        crumbs=[("Home", f"https://{HOST}/"), ("About", canonical)],
    )
    html += skip_link(skip_label("en"))
    html += _header("about")
    html += f"""<main id="main" class="container">
<section class="sg-hero">
  <h1>About | BaseTao Spreadsheet</h1>
  <p class="hsub">Independent information desk. We do not run orders or take payment.</p>
</section>
{_local_plus()}
<section class="sg-sec" id="about">
  <h2>Independence</h2>
  <p>{escape(independence_copy(facts))}</p>
  <p>Email: <a href="mailto:{escape(MAIL)}">{escape(MAIL)}</a></p>
  <p>Live finds: <a href="{escape(W2C)}" rel="noopener">{escape(W2C)}</a></p>
  <p>Official agent: <a href="{escape(OFFICIAL)}">{escape(OFFICIAL)}</a></p>
</section>
</main>
{_footer()}
</body></html>
"""
    return html


def build_404() -> str:
    title = "404 | BaseTao Spreadsheet"
    desc = "Page not found on the BaseTao spreadsheet desk. Start again from /start/."
    canonical = f"https://{HOST}/404.html"
    html = _chrome_head(
        title=title,
        desc=desc,
        canonical=canonical,
        crumbs=[("Home", f"https://{HOST}/"), ("404", canonical)],
    )
    html += skip_link(skip_label("en"))
    html += _header("404")
    html += f"""<main id="main" class="container">
<section class="sg-hero">
  <h1>404 | BaseTao Spreadsheet</h1>
  <p class="hsub">That path is not a page on this hub.</p>
  <div class="sg-ctas">
    <a class="btn btn-primary" href="/start/">Start</a>
    <a class="btn btn-outline" href="/">Home</a>
    <a class="btn btn-outline" href="/help/">Help</a>
  </div>
</section>
</main>
{_footer()}
</body></html>
"""
    return html


def build_sitemap() -> str:
    rows = []
    for path in SITEMAP_EXTRA:
        loc = f"https://{HOST}{path}"
        pri = "1.0" if path == "/" else ("0.8" if path in ("/start/", "/help/") else "0.6")
        rows.append(
            "  <url>\n"
            f"    <loc>{escape(loc)}</loc>\n"
            f"    <lastmod>2026-10-07</lastmod>\n"
            "    <changefreq>weekly</changefreq>\n"
            f"    <priority>{pri}</priority>\n"
            "  </url>"
        )
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "\n".join(rows)
        + "\n</urlset>\n"
    )


def _assert_home(html: str) -> None:
    err: list[str] = []
    facts = _facts()
    if TITLE not in html or H1 not in html:
        err.append("missing spreadsheet title/h1")
    if 'id="local"' not in html or "not a customs territory" not in html:
        err.append("missing hub #local")
    if html.count("<details class=\"sg-faq\"") != 0:
        err.append("visible sg-faq leaked onto homepage")
    if "/api/products/" in html:
        err.append("homepage dumps /api/products/")
    if "/basetao-shipping-calculator/\">Shipping</a>" not in html:
        err.append("nav Shipping not wired to calculator")
    if "/basetao-referral-code/\">Shipping</a>" in html:
        err.append("nav still mislabels referral as Shipping")
    if "/shoes381/" not in html or W2C not in html:
        err.append("category wall missing local hub or w2clinks")
    if MAIL not in html:
        err.append("missing contact email")
    if re.search(r"invite\s*(code)?\s*[A-Z0-9]{5,}", html, flags=re.I):
        err.append("invite in html")
    if re.search(r"58 l[ií]neas para Espa|23[,.]81\s*USD|how to under-?declar", html, flags=re.I):
        err.append("coaching")
    if "Georgia" in html or "#00C853" in html:
        err.append("HipoBuy/Georgia leak")
    _check_local_section(html, facts, err)
    for alien in ALIENS:
        inner = re.search(r'<section class="sg-sec" id="local".*?</section>', html, flags=re.S)
        if inner and alien in inner.group(0):
            err.append(f"sister dest {alien}")
    if err:
        raise SystemExit("home: " + "; ".join(err))


def _assert_start(html: str) -> None:
    err: list[str] = []
    facts = _facts()
    if "Start | BaseTao Spreadsheet" not in html:
        err.append("missing start title")
    if TITLE in html and H1 in html and 'id="cat-wall"' in html:
        err.append("start cloned homepage")
    if 'id="local"' not in html or "not a customs territory" not in html:
        err.append("missing hub #local")
    if html.count('<details class="sg-faq"') != 0:
        err.append("visible sg-faq leaked onto start")
    if "/api/products/" in html:
        err.append("start dumps /api/products/")
    if "/basetao-shipping-calculator/\">Shipping</a>" not in html:
        err.append("nav Shipping not wired to calculator")
    if MAIL not in html:
        err.append("missing contact email")
    _check_local_section(html, facts, err)
    if err:
        raise SystemExit("start: " + "; ".join(err))


def generate() -> dict[str, Path]:
    assert_dest_packs_unique()
    overlay = OUT / HOST / "overlay"
    overlay.mkdir(parents=True, exist_ok=True)
    home = build_home()
    start = build_start()
    help_html = build_help()
    about = build_about()
    nf = build_404()
    _assert_home(home)
    _assert_start(start)
    help_err = validate_desk(help_html, _facts(), page="help")
    if help_err:
        raise SystemExit("help: " + "; ".join(help_err))
    about_err = validate_desk(about, _facts(), page="about")
    if about_err:
        raise SystemExit("about: " + "; ".join(about_err))
    n_faq = help_html.count('<details class="sg-faq"')
    if n_faq < 12:
        raise SystemExit(f"help faq {n_faq}")
    (overlay / "index.html").write_text(home, encoding="utf-8")
    start_dir = overlay / "start"
    start_dir.mkdir(parents=True, exist_ok=True)
    (start_dir / "index.html").write_text(start, encoding="utf-8")
    help_dir = overlay / "help"
    help_dir.mkdir(parents=True, exist_ok=True)
    (help_dir / "index.html").write_text(help_html, encoding="utf-8")
    about_dir = overlay / "about"
    about_dir.mkdir(parents=True, exist_ok=True)
    (about_dir / "index.html").write_text(about, encoding="utf-8")
    (overlay / "404.html").write_text(nf, encoding="utf-8")
    sm = overlay / "sitemap.xml"
    sm.write_text(build_sitemap(), encoding="utf-8")
    files = {
        "home": overlay / "index.html",
        "start": start_dir / "index.html",
        "help": help_dir / "index.html",
        "about": about_dir / "index.html",
        "nf": overlay / "404.html",
        "sitemap": sm,
    }
    print(
        "generate",
        "home",
        len(home),
        "start",
        len(start),
        "help",
        len(help_html),
        "about",
        len(about),
        "faq",
        n_faq,
    )
    return files


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
    files = generate()
    client = _connect()
    stamp = time.strftime("%Y%m%d-%H%M%S")
    bak = f"/www/backup/basetao-hub-deepen-{stamp}"
    root = f"/www/wwwroot/{HOST}"
    _run(
        client,
        f"mkdir -p '{bak}' '{root}/start' '{root}/help' '{root}/about' '{root}/assets/css'",
    )
    sftp = client.open_sftp()
    mapping = {
        "home": f"{root}/index.html",
        "start": f"{root}/start/index.html",
        "help": f"{root}/help/index.html",
        "about": f"{root}/about/index.html",
        "nf": f"{root}/404.html",
        "sitemap": f"{root}/sitemap.xml",
    }
    for name, remote in mapping.items():
        _run(client, f"if [ -f '{remote}' ]; then cp -a '{remote}' '{bak}/{name}.html'; fi")
        local = files[name]
        raw = local.read_text(encoding="utf-8")
        if name in ("home", "start", "help") and "not a customs territory" not in raw:
            raise SystemExit(f"refusing {name} without hub fingerprint")
        if name == "home" and "/api/products/" in raw:
            raise SystemExit("refusing homepage /api/products/ dump")
        sftp.put(str(local), remote)
        print("PUT", remote, local.stat().st_size)
    cms = ROOT / "sites" / "shared" / "desk-cms.css"
    theme = ROOT / "sites" / "shared" / "themes" / "basetao-theme.css"
    if cms.is_file():
        sftp.put(str(cms), f"{root}/assets/css/desk-cms.css")
    if theme.is_file():
        sftp.put(str(theme), f"{root}/assets/css/basetao-theme.css")
    _run(
        client,
        f"chown -R www:www '{root}/index.html' '{root}/start' '{root}/help' "
        f"'{root}/about' '{root}/404.html' '{root}/sitemap.xml' '{root}/assets/css'",
    )
    sftp.close()
    token = os.environ.get("CLOUDFLARE_API_TOKEN", "").strip()
    if token:
        import urllib.request

        req = urllib.request.Request(
            "https://api.cloudflare.com/client/v4/zones?name=basetaospreadsheet.com",
            headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
        )
        try:
            with urllib.request.urlopen(req, timeout=20) as resp:
                zones = json.loads(resp.read().decode())
            zid = (zones.get("result") or [{}])[0].get("id")
            if zid:
                preq = urllib.request.Request(
                    f"https://api.cloudflare.com/client/v4/zones/{zid}/purge_cache",
                    data=json.dumps({"purge_everything": True}).encode(),
                    headers={
                        "Authorization": f"Bearer {token}",
                        "Content-Type": "application/json",
                    },
                    method="POST",
                )
                with urllib.request.urlopen(preq, timeout=20) as resp:
                    print("cf_purge", resp.status, resp.read()[:120])
        except Exception as e:
            print("cf_purge skipped", e)
    print("backup", bak)
    print("ranked inners not overwritten")
    client.close()


def live_check() -> None:
    import urllib.error
    import urllib.request

    class NR(urllib.request.HTTPRedirectHandler):
        def redirect_request(self, req, fp, code, msg, headers, newurl):
            return None

    def fetch(url, follow=True):
        req = urllib.request.Request(url, headers={"User-Agent": "basetao-hub-deepen/1.0"})
        opener = urllib.request.build_opener() if follow else urllib.request.build_opener(NR)
        try:
            with opener.open(req, timeout=25) as resp:
                return resp.status, resp.geturl(), resp.headers.get("Location") or "", resp.read()
        except urllib.error.HTTPError as e:
            return e.code, url, e.headers.get("Location") or "", e.read() if e.fp else b""

    fail = 0
    code, _, _, body = fetch(f"https://{HOST}/")
    html = body.decode("utf-8", "replace")
    print("home", code, len(body), "title_ok", TITLE in html, "h1_ok", H1 in html)
    if code != 200 or TITLE not in html or H1 not in html:
        print(" FAIL home title")
        fail += 1
    if "not a customs territory" not in html or 'id="local"' not in html:
        print(" FAIL hub local")
        fail += 1
    if html.count('<details class="sg-faq"') != 0:
        print(" FAIL home visible faq")
        fail += 1
    if "/api/products/" in html:
        print(" FAIL api dump")
        fail += 1
    if "/basetao-shipping-calculator/\">Shipping</a>" not in html:
        print(" FAIL nav")
        fail += 1
    if "/shoes381/" not in html:
        print(" FAIL local cat")
        fail += 1
    for url in (
        f"https://{HOST}/start/",
        f"https://{HOST}/help/",
        f"https://{HOST}/about/",
    ):
        c, _, _, b = fetch(url)
        h = b.decode("utf-8", "replace")
        print("desk", url, c, len(b))
        if c != 200 or len(b) < 4000:
            print(" FAIL desk")
            fail += 1
        if url.endswith("/help/") and h.count('<details class="sg-faq"') < 12:
            print(" FAIL help faq", h.count('<details class="sg-faq"'))
            fail += 1
        if url.endswith("/about/") and TITLE in h and H1 in h and 'id="cat-wall"' in h:
            print(" FAIL about cloned home")
            fail += 1
    for url in (
        f"https://{HOST}/basetao-referral-code/",
        f"https://{HOST}/basetao-shipping-calculator/",
        f"https://{HOST}/basetao-calculator/",
        f"https://{HOST}/basetao-review/",
    ):
        c, final, _, b = fetch(url)
        if c == 404 or len(b) < 8000:
            print("FAIL inner", url, c, len(b))
            fail += 1
        else:
            print("inner", c, len(b), final)
    c, _, loc, _ = fetch(f"https://{HOST}/", follow=False)
    if c in (301, 302, 308):
        print("FAIL home 301", loc)
        fail += 1
    if fail:
        raise SystemExit(f"live_check failures: {fail}")
    print("live_check ok")


def main() -> None:
    if "--put" in sys.argv:
        put()
        return
    if "--check" in sys.argv:
        live_check()
        return
    generate()


if __name__ == "__main__":
    main()
