#!/usr/bin/env python3
"""Rebuild acbuyspreadsheets.nl as an ACBuy NL country desk (HipoBuy-NL depth).

Dutch throughout. Orange ACBuy chrome. Help / News / About as independent pages.
Does not PUT 5KB overlays over ranked inners. Does not invent warehouse-day
counts or invite tokens on titles. CA AllChinaBuy dest is the next agent.
Twin allchinabuyspreadsheet.nl stays 301 $request_uri into this dest.
"""
from __future__ import annotations

import json
import os
import re
import sys
import time
from html import escape
from pathlib import Path

_TOOLS = Path(__file__).resolve().parent
if str(_TOOLS) not in sys.path:
    sys.path.insert(0, str(_TOOLS))

from desk_fx import catalog_block
from desk_template import (
    dest_local_pack,
    faq_ld,
    inject_jsonld,
    itemlist_ld,
    lab_copy,
    local_guide_html,
    long_faqs,
    organization_ld,
    skip_label,
    skip_link,
    validate_desk,
    webpage_ld,
)
from dest_inner_chrome import (
    _body_scripts_outside_article,
    _element_inner,
    _head_inner,
    _html_tag,
    _text_len,
    after_footer_keep,
    extract_article,
)

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "sites"
HOST = "acbuyspreadsheets.nl"
DATE = "5 Oct 2026"
OFFICIAL = "https://www.acbuy.com/"
EST = "https://www.acbuy.com/estimation/"
HELP = "https://www.acbuy.com/help"
REG = "https://www.acbuy.com/"
ACC = "#E87000"
INVITE = "5F2RRA"
INVITE2 = "EwjrSk"
INVITE3 = "ACBUY5"
STORAGE = (
    "Officiële ACBuy Help is de live SPA "
    f"({HELP}); bevestig die tekst op de ochtend van verzenden. "
    "Deze desk verzint geen gratis-dagen-aantal."
)
DEST_MIN = 22000
INNER_MARKER = 'data-inner-chrome="20261005-acbuy-nl"'
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
    ("/", "Start"),
    ("/how-to-use-acbuy/", "Handleiding"),
    ("/#catalog", "Catalogus"),
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


def _local_block() -> str:
    """User-facing NL briefing only. Planning notes live on /nieuws/ and /over-ons/."""
    return local_guide_html(FACTS).strip()


def _faq_html() -> str:
    items = []
    for i, (q, a) in enumerate(long_faqs(FACTS)):
        op = " open" if i == 0 else ""
        items.append(
            f'<details class="sg-faq"{op}><summary>{escape(q)}</summary><p>{escape(a)}</p></details>'
        )
    return "\n".join(items)


def _nav(page: str) -> str:
    bits = []
    for href, lab in CMS_PAGES:
        if href == "/#catalog":
            dest = "#catalog" if page == "/" else "/#catalog"
            bits.append(f'<a href="{escape(dest)}">{escape(lab)}</a>')
            continue
        on = ' aria-current="page"' if href == page else ""
        bits.append(f'<a href="{escape(href)}"{on}>{escape(lab)}</a>')
    return "".join(bits)


def _header(page: str) -> str:
    return f"""{skip_link(skip_label("nl"))}<header class="top" role="banner">
  <div class="wrap">
    <a href="/" class="brand">
      <img src="/assets/images/acbuy-wordmark.png?v=20261005-esref" alt="" width="162" height="35">
      <span>ACBuy Spreadsheet</span>
    </a>
    <button class="burger" type="button" aria-expanded="false" aria-label="Menu openen">&#9776;</button>
    <nav class="nav" aria-label="Hoofdmenu">{_nav(page)}</nav>
  </div>
</header>
"""


def _footer() -> str:
    keep = "".join(f'<li><a href="{escape(h)}">{escape(l)}</a></li>' for h, l in KEEP)
    return f"""<footer class="site-ft">
  <div class="wrap ft-grid">
    <div>
      <p class="brand-ft"><img src="/assets/images/acbuy-wordmark.png?v=20261005-esref" alt="ACBuy" width="132" height="29"> ACBuy Spreadsheet NL</p>
      <p>Onafhankelijke gids op {escape(HOST)}. Geen shop, geen kassa. Checkout alleen op {escape(OFFICIAL)}.</p>
    </div>
    <div>
      <h4>Gidsen</h4>
      <ul>{keep}<li><a href="/hulp/">Hulp</a></li><li><a href="/nieuws/">Nieuws</a></li></ul>
    </div>
    <div>
      <h4>Deze desk</h4>
      <ul>
        <li><a href="/over-ons/">Over ons</a></li>
        <li><a href="{escape(EST)}">Vracht-schatter</a></li>
        <li><a href="mailto:support@{escape(HOST)}">support@{escape(HOST)}</a></li>
      </ul>
    </div>
  </div>
  <div class="wrap ft-copy"><p>© 2026 {escape(HOST)} — onafhankelijk.</p></div>
</footer>
<script>
(function(){{
  var b=document.querySelector('.burger'), n=document.querySelector('nav.nav');
  if(!b||!n) return;
  b.addEventListener('click', function(){{
    var on=b.getAttribute('aria-expanded')==='true';
    b.setAttribute('aria-expanded', on?'false':'true');
    n.classList.toggle('open', !on);
  }});
}})();
</script>
"""


CSS = f"""
:root{{
  --acc:{ACC};--acd:#c45f00;--link:#c45f00;
  --ink:#303133;--ink2:#626366;--mute:#666d80;--dark:#111827;
  --panel:#FFF3E0;--line:#f3d5a8;--soft:#fff8f0;
  --r:18px;--rs:12px;--maxw:1120px;--medida:34em;
  --f:'DM Sans','Helvetica Neue',Helvetica,Arial,sans-serif;--m:ui-monospace,monospace;
}}
*{{box-sizing:border-box}}
html{{-webkit-text-size-adjust:100%;color-scheme:light;scroll-behavior:smooth}}
body{{margin:0;font-family:var(--f);font-size:17px;line-height:1.72;color:var(--ink);background:#fff}}
img{{max-width:100%;height:auto;display:block}}
a{{color:var(--link)}}
a:hover{{color:var(--acd)}}
#main,[id]{{scroll-margin-top:76px}}
h1,h2,h3{{color:var(--dark);line-height:1.25;letter-spacing:-.01em;margin:0 0 .5em}}
h1{{font-size:clamp(30px,4.4vw,45px);font-weight:800}}
h2{{font-size:clamp(24px,3vw,32px);font-weight:800}}
h3{{font-size:20px;font-weight:700}}
p{{margin:0 0 1.05em}}
main p,main li,.sg-faq p{{max-width:var(--medida)}}
.wrap{{max-width:var(--maxw);margin:0 auto;padding:0 22px}}
.skip{{position:absolute;left:-9999px}}
.skip:focus{{left:12px;top:12px;z-index:99;background:#fff;padding:8px 18px;border-radius:var(--rs)}}
.top{{position:sticky;top:0;z-index:40;background:rgba(255,255,255,.96);backdrop-filter:blur(8px);border-bottom:1px solid var(--line)}}
.top .wrap{{display:flex;align-items:center;gap:18px;min-height:64px}}
.brand{{display:flex;align-items:center;gap:9px;min-height:44px;font-weight:800;color:var(--dark);text-decoration:none;font-size:17px;white-space:nowrap}}
.brand img{{height:28px;width:auto}}
.nav{{margin-left:auto;display:flex;gap:4px;flex-wrap:nowrap}}
.nav a{{display:inline-flex;align-items:center;min-height:44px;padding:0 12px;border-radius:var(--rs);color:var(--ink2);text-decoration:none;font-size:15.5px;white-space:nowrap}}
.nav a:hover,.nav a[aria-current]{{background:var(--soft);color:var(--acd);font-weight:700}}
.burger{{display:none;margin-left:auto;min-width:44px;min-height:44px;border:1px solid var(--line);background:#fff;border-radius:var(--rs);font-size:19px;cursor:pointer}}
.hero{{position:relative;background:#1a0f05;overflow:hidden}}
.hero__scrim{{position:absolute;inset:0;background:linear-gradient(100deg,rgba(26,15,5,.96) 0%,rgba(232,112,0,.28) 100%)}}
.hero .wrap{{position:relative;padding:74px 22px 78px}}
.eyebrow{{display:inline-block;font-size:12.5px;letter-spacing:.13em;text-transform:uppercase;font-weight:700;color:#ffd7a8;margin-bottom:14px}}
.hero h1{{color:#fff;max-width:15.5em}}
.hero p.lead{{color:#f3e2cc;font-size:19px;max-width:34em}}
.sbox{{margin-top:26px;max-width:660px}}
.sbox form{{display:flex;gap:9px;background:#fff;border-radius:var(--r);padding:9px}}
.sbox input{{flex:1;min-width:0;border:0;font:inherit;font-size:17px;padding:12px 14px}}
.sbox button{{min-height:44px;padding:0 24px;border:0;border-radius:999px;background:var(--acc);color:#fff;font:inherit;font-weight:700;cursor:pointer}}
.chips{{display:flex;flex-wrap:wrap;gap:8px;margin-top:12px}}
.chips a{{display:inline-flex;align-items:center;min-height:38px;padding:0 13px;border-radius:999px;background:rgba(255,255,255,.12);border:1px solid rgba(255,255,255,.26);color:#fff8f0;text-decoration:none;font-size:14px}}
.sec{{padding:62px 0;border-top:1px solid var(--line)}}
.sec--tint{{background:linear-gradient(var(--soft) 0%,#fff 100%);border-top:0}}
.sec--first{{border-top:0}}
.lead{{font-size:18px;color:var(--ink2);max-width:var(--medida)}}
.btn{{display:inline-flex;align-items:center;min-height:44px;padding:0 18px;border-radius:999px;background:var(--acc);color:#fff;font-weight:700;text-decoration:none}}
.btn:hover{{background:var(--acd);color:#fff}}
.btn--ghost{{background:#fff;color:var(--acd);border:1px solid var(--line)}}
.states{{margin:0;padding:0;list-style:none}}
.states li{{padding:10px 0;border-bottom:1px solid var(--line);max-width:40em}}
.states code{{font-family:var(--m);font-size:13px}}
.sg-sec{{max-width:var(--maxw);margin:0 auto;padding:28px 22px}}
.ssub{{color:var(--ink2);margin:0 0 14px}}
.local-steps{{margin:12px 0 0;padding:0;list-style:none;display:grid;gap:12px;max-width:40em}}
.local-steps li{{border:1px solid var(--line);border-radius:12px;padding:14px 16px;background:#fff;max-width:none}}
.local-steps strong{{display:block;margin:0 0 6px}}
.local-src{{font-size:14px;color:var(--mute);line-height:1.7;margin:14px 0 0;max-width:var(--medida)}}
.sg-cats{{display:grid;grid-template-columns:repeat(auto-fill,minmax(150px,1fr));gap:10px}}
.sg-cat{{display:block;border:1px solid var(--line);border-radius:12px;padding:16px;text-decoration:none;color:inherit;background:#fff}}
.sg-cat span{{display:block;color:var(--mute);font-size:13px;margin-top:4px}}
.sg-mw{{max-width:var(--maxw);margin:0 auto;padding:8px 22px 40px}}
.sg-chips{{display:flex;flex-wrap:wrap;gap:8px;margin:10px 0}}
.sg-chips button{{border:1px solid var(--line);background:#fff;border-radius:999px;padding:6px 12px;cursor:pointer}}
.sg-chips button.on{{background:var(--panel);border-color:var(--acc);color:var(--acd);font-weight:700}}
.sg-fbar{{display:flex;gap:10px;align-items:center;margin:8px 0 14px}}
.sg-fbar input{{flex:1;padding:10px 12px;border-radius:8px;border:1px solid var(--line)}}
.sg-grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(180px,1fr));gap:12px}}
.sg-card{{border:1px solid var(--line);border-radius:12px;overflow:hidden;background:#fff;display:flex;flex-direction:column}}
.sg-card img{{width:100%;aspect-ratio:1;object-fit:cover;background:#f1f5f9}}
.sg-card .b{{padding:10px}}
.sg-card .t{{font-size:13px;font-weight:600;min-height:2.4em}}
.sg-card .pr{{font-weight:800;color:var(--acc)}}
.sg-card .pr-src{{font-size:11px;color:#94a3b8}}
.sg-card a.buy{{margin:0 10px 10px;text-align:center;padding:8px;border-radius:8px;background:var(--acc);color:#fff;font-size:12.5px;font-weight:600;text-decoration:none}}
.sg-fx{{color:var(--mute);font-size:13px;line-height:1.55;margin:4px 0 10px;max-width:var(--medida)}}
.sg-faq{{border:1px solid var(--line);border-radius:10px;padding:12px 14px;margin:8px 0;background:#fff;max-width:40em}}
.sg-faq summary{{cursor:pointer;font-weight:700}}
.ncard{{border:1px solid var(--line);border-radius:var(--r);padding:16px 18px;margin-bottom:12px;max-width:40em}}
.shot-panel{{border:1px solid var(--line);border-radius:var(--r);padding:22px;background:var(--soft);max-width:40em}}
.site-ft{{background:#111;color:#ccc;padding:40px 0 24px;margin-top:24px}}
.ft-grid{{display:grid;grid-template-columns:1.5fr 1fr 1fr;gap:32px}}
.brand-ft{{display:flex;align-items:center;gap:8px;color:#fff;font-weight:700}}
.brand-ft img{{height:26px;width:auto}}
.site-ft h4{{font-size:12px;letter-spacing:.6px;color:#888;text-transform:uppercase}}
.site-ft ul{{list-style:none;margin:0;padding:0}}
.site-ft li{{margin-bottom:8px}}
.site-ft a{{color:#aaa}}
.ft-copy{{margin-top:24px;padding-top:16px;border-top:1px solid #2D2D2D;font-size:12px;color:#666}}
.pw{{max-width:40em;margin:0 auto;padding:40px 22px 64px}}
.inner-article{{max-width:860px;margin:0 auto;padding:28px 24px 48px}}
@media(max-width:860px){{
  .burger{{display:inline-flex;align-items:center;justify-content:center}}
  .nav{{display:none;position:absolute;left:0;right:0;top:64px;background:#fff;border-bottom:1px solid var(--line);flex-direction:column;padding:8px 12px}}
  .nav.open{{display:flex}}
  .ft-grid{{grid-template-columns:1fr}}
}}
"""


def _shell(title: str, desc: str, canonical: str, extra_ld: list[dict], body: str, page: str) -> str:
    ld = [
        webpage_ld(
            url=canonical,
            name=title,
            desc=desc,
            lang="nl-NL",
            brand="ACBuy",
            host=HOST,
        ),
        organization_ld(
            name=f"{HOST} independent desk",
            url=f"https://{HOST}/",
            email=f"support@{HOST}",
            lang="nl-NL",
            desc=desc,
        ),
    ] + extra_ld
    html = f"""<!DOCTYPE html>
<html lang="nl-NL">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{escape(title)}</title>
<meta name="description" content="{escape(desc)}">
<link rel="canonical" href="{escape(canonical)}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/css/acbuy-theme.css?v=20261005-esref">
<link rel="stylesheet" href="/assets/css/acbuy-nl-desk.css?v=20261005-esref">
<style>{CSS}</style>
</head>
<body>
{_header(page)}
<main id="main">
{body}
</main>
{_footer()}
</body>
</html>
"""
    return inject_jsonld(html, *ld)


def build_home() -> str:
    lab = lab_copy(FACTS)
    cats = [
        ("sneakers", "Turnschoenen"),
        ("t-shirt", "T-shirt"),
        ("hoodie", "Hoodie"),
        ("jacket", "Jas"),
        ("jeans", "Spijkerbroek"),
        ("shorts", "Shorts"),
        ("underwear", "Ondergoed"),
        ("jersey", "Shirt"),
        ("hat", "Petten"),
        ("bags", "Tassen"),
        ("sunglasses", "Brillen"),
        ("headphones", "Koptelefoons"),
        ("perfume", "Parfum"),
        ("watch", "Horloges"),
        ("jewelry", "Sieraden"),
        ("toy", "Speelgoed"),
    ]
    wall = "".join(
        f'<a class="sg-cat" href="#catalog" data-q="{escape(q)}"><strong>{escape(labn)}</strong><span>{escape(q)}</span></a>'
        for q, labn in cats
    )
    chips = "".join(
        f'<a href="#catalog" data-q="{escape(q)}">{escape(q)}</a>'
        for q, _lab in cats[:8]
    )
    catalog = catalog_block(
        "nl",
        {"lang": "nl-NL", "loc": "nl", "dest": "NL", "ccy": "EUR"},
        register_url=REG,
        loc_fn=lambda _k: "nl",
        cat_labels={},
    )
    faqs = _faq_html()
    body = f"""
<section class="hero">
  <div class="hero__scrim"></div>
  <div class="wrap">
    <span class="eyebrow">Onafhankelijke gids, in het Nederlands</span>
    <h1>ACBuy Spreadsheet: de gids om in China te kopen vanaf Nederland</h1>
    <p class="lead">Wat een inkoopagent doet, hoe je de catalogus zoekt, hoe een pakket naar Nederland reist en wat je nagaat vóór de Douane.</p>
    <div class="sbox">
      <form id="home-search" action="#catalog" method="get" role="search">
        <label class="skip" for="hero-q">Zoek in de catalogus op deze homepage</label>
        <input id="hero-q" name="q" type="search" autocomplete="off" placeholder="Zoek sneakers, hoodie, jas…">
        <button type="submit">Zoeken</button>
      </form>
      <div class="chips">{chips}</div>
    </div>
  </div>
</section>
<section class="sec sec--first" id="agent">
  <div class="wrap">
    <h2>Een inkoopagent is een tussenpersoon, geen winkel</h2>
    <p class="lead">ACBuy verkoopt zelf niets. Hij koopt voor jou in Chinese shops die niet naar het buitenland sturen, ontvangt het pakket in het magazijn, fotografeert het, bewaart het, en stuurt het naar Nederland wanneer jij dat besluit.</p>
    <p>Dat verandert alles: je betaalt twee keer (eerst het product, daarna internationaal), je wacht twee keer, en ertussen kun je nog annuleren, bundelen of van lijn wisselen. Betalen en tickets blijven op {escape(OFFICIAL)}.</p>
    <p><a class="btn" href="/how-to-use-acbuy/">Handleiding stap voor stap</a></p>
  </div>
</section>
<section class="sec sec--tint" id="sheet-explain">
  <div class="wrap">
    <span class="eyebrow" style="color:var(--acd)">Naam die misleidt</span>
    <h2>Een spreadsheet is geen Excel-bestand</h2>
    <p class="lead">Hier betekent «spreadsheet» een catalogus van productkaarten: foto, merk, referentieprijs en de link om in de agent te plakken. Geen rijen en kolommen.</p>
    <p>De kaarten op deze homepage komen van /api/products/ op {escape(HOST)}. Je bladert op categorie. Engelse keys (sneakers, hoodie) vullen de grid; «turnschoenen» geeft vaak nul hits — dat is de index, geen lege winkel.</p>
    <p><a class="btn btn--ghost" href="#catalog">Naar de catalogus op deze homepage</a></p>
  </div>
</section>
<section class="sec" id="cat-wall">
  <div class="wrap">
    <h2>Zestien categorieën voor de eerste dag</h2>
    <p class="lead">Elke kaart opent de bijbehorende catalogus. Begin met één: vijf categorieën in de eerste haul is de snelste weg naar een dure, lastige doos.</p>
    <div class="sg-cats">{wall}</div>
  </div>
</section>
{catalog}
{_local_block()}
<section class="sec" id="states">
  <div class="wrap">
    <h2>Negen statussen, drie schermen</h2>
    <p class="lead">Het officiële verloop past in negen staten. Ze uit je hoofd kennen voorkomt de vraag van de eerste maand: «waarom staat het stil?». Meestal staat het niet stil — het zit in een staat die je niet verwachtte.</p>
    <ol class="states">
      <li><code>Order Submitted</code> — bestelling verstuurd, product in China betaald.</li>
      <li><code>Order Placed</code> — ACBuy koopt in de Chinese shop op jouw naam.</li>
      <li><code>Seller Shipped</code> — de Chinese verkoper heeft verzonden.</li>
      <li><code>Arrived at Warehouse</code> — aangekomen in het magazijn.</li>
      <li><code>Inspection &amp; Storage</code> — controle en opslag. Live labels staan in de app.</li>
      <li><code>Shipping Requested</code> — jij bundelt en boekt de internationale lijn naar Nederland.</li>
      <li><code>Parcel Packed</code> — de doos wordt ingepakt.</li>
      <li><code>Shipped</code> — vertrek uit China.</li>
      <li><code>Delivered</code> — bezorgd; ontvangst bevestigen in de app.</li>
    </ol>
    <p>De eerste vier zitten onder Order, daarna Warehouse, daarna Parcel. <a href="/how-to-use-acbuy/">Handleiding met het traject →</a></p>
  </div>
</section>
<section class="sec sec--tint" id="lab">
  <div class="wrap">
    <h2>Nederland heeft lijnen, maar niet elke lijn is open</h2>
    <p class="lead">De officiële schatter is publiek. Kies bestemming Nederland, niet EU. Live geld staat in de estimator, niet in deze homepage.</p>
    <p>{lab["ssub"]}</p>
    <p>Het gewicht dat je betaalt is bijna nooit alleen de weegschaal. Veel luchtlijnen rekenen volumgewicht L×B×H/8000 en factureren het maximum. Een donsjas is licht en volumineus: daar beslist het volume. Die rekening, plus Douane, staat in het onafhankelijke verzendplan.</p>
    <p><a class="btn" href="/acbuy-shipping-guide/">Verzendplan: lijnen, Douane, volumgewicht</a>
       <a class="btn btn--ghost" href="{escape(EST)}">{escape(lab["cta"])}</a></p>
  </div>
</section>
<section class="sec" id="restricted">
  <div class="wrap">
    <h2>Veel producten kun je niet kopen, ook al staan ze er</h2>
    <p class="lead">Op het officiële site zie je fiches «Restricted item» en fiches met prijs nul. Dat is geen fout van deze homepage: de bronlink is niet koopbaar via de agent, of de prijs liet zich niet lezen.</p>
    <p>Regel: zonder echte prijs en varianten niet bestellen. Tabak, alcohol en geneesmiddelen reizen niet. Restricted is een inkoopblokkade, geen bericht van de Douane.</p>
  </div>
</section>
<section class="sec sec--tint" id="shots">
  <div class="wrap">
    <h2>Officiële schermen, geen stockfoto’s</h2>
    <p class="lead">Live estimator, QC-foto’s en iDEAL zitten in de ACBuy-app. Deze homepage plakt geen verzonnen screenshots.</p>
    <div class="shot-panel">
      <p>Open de schatter met bestemming Netherlands. De gids, de hulpvragen en de gedateerde checks staan op eigen URL’s — niet als bijlage onder deze hero.</p>
      <p><a class="btn" href="{escape(OFFICIAL)}">Open ACBuy</a>
         <a class="btn btn--ghost" href="{escape(EST)}">Vracht-schatter</a></p>
    </div>
  </div>
</section>
<section class="sec" id="faq">
  <div class="wrap">
    <h2>Hulp, nieuws en waar je vraagt</h2>
    <p class="lead">De meeste twijfels van de eerste orders herhalen zich. Ze staan beantwoord in het Nederlands op de hulppagina — een eigen URL, geen bijlage van deze homepage.</p>
    {faqs}
    <p><a class="btn" href="/hulp/">Alle vragen op Hulp</a>
       <a class="btn btn--ghost" href="/nieuws/">Gedateerde checks op Nieuws</a>
       <a class="btn btn--ghost" href="/over-ons/">Over ons</a></p>
  </div>
</section>
<script>
(function(){{
  var form=document.getElementById('home-search');
  if(!form) return;
  form.addEventListener('submit', function(ev){{
    ev.preventDefault();
    var q=(document.getElementById('hero-q')||{{}}).value||'';
    var inp=document.getElementById('sg-q');
    if(inp){{ inp.value=q; inp.dispatchEvent(new Event('input', {{bubbles:true}})); }}
    var cat=document.getElementById('catalog');
    if(cat) cat.scrollIntoView({{behavior:'smooth', block:'start'}});
  }});
  document.querySelectorAll('.chips a[data-q]').forEach(function(a){{
    a.addEventListener('click', function(ev){{
      ev.preventDefault();
      var inp=document.getElementById('sg-q');
      if(inp){{ inp.value=a.getAttribute('data-q')||''; inp.dispatchEvent(new Event('input', {{bubbles:true}})); }}
      var cat=document.getElementById('catalog');
      if(cat) cat.scrollIntoView({{behavior:'smooth', block:'start'}});
    }});
  }});
}})();
</script>
"""
    return _shell(
        "ACBuy Spreadsheet in het Nederlands: kopen in China vanaf Nederland",
        "Onafhankelijke gids in het Nederlands: wat ACBuy doet, hoe de catalogus werkt, hoe een pakket naar Nederland reist en wat je nagaat bij de Douane.",
        f"https://{HOST}/",
        [faq_ld("nl-NL", long_faqs(FACTS))],
        body,
        "/",
    )


def build_help() -> str:
    faqs = _faq_html()
    body = f"""
<article class="pw">
  <span class="eyebrow" style="color:var(--acd)">Hulp</span>
  <h1>Hulp en vragen over ACBuy in Nederland</h1>
  <p class="lead">De meeste twijfels van de eerste orders herhalen zich: twee betalingen, catalogus in het Engels, volumgewicht, Douane. Hier in het Nederlands, voor een huisadres in Nederland.</p>
  {_local_block()}
  <h2>Wat ACBuy is</h2>
  <p>ACBuy is een inkoopagent: hij koopt in Chinese shops op jouw naam en houdt de goederen in het magazijn tot jij een internationale lijn boekt. Bestellen, betalen en claims gaan alleen via <a href="{escape(OFFICIAL)}">{escape(OFFICIAL)}</a>.</p>
  {faqs}
  <p><a class="btn" href="{escape(EST)}">Officiële estimator, bestemming Nederland</a>
     <a class="btn btn--ghost" href="/acbuy-shipping-guide/">Verzendplan</a>
     <a class="btn btn--ghost" href="/nieuws/">Nieuws</a></p>
</article>
"""
    return _shell(
        "Hulp en vragen over ACBuy in Nederland",
        "FAQ voor een Nederlands huisadres: twee betalingen, catalogus, volumgewicht, Douane. Geen onderwaardering.",
        f"https://{HOST}/hulp/",
        [faq_ld("nl-NL", long_faqs(FACTS))],
        body,
        "/hulp/",
    )


def build_news() -> str:
    items = [
        ("Check 1 · Estimator-bestemming NL, niet EU",
         "Kies Nederland in de officiële schatter. Belgische of Duitse postcode is het verkeerde land. Nederlandse postcode 1234 AB."),
        ("Check 2 · Officiële Help is een SPA-shell",
         "https://www.acbuy.com/help geeft zonder JavaScript een SPA-fout. Deze pagina kopieert daar geen verzonnen magazijn-dagentelling uit."),
        ("Check 3 · EUR-weergave versus USD-cijfers in de app",
         "De catalogus op deze host toont EUR als weergave van de China-kaart (X-Rates 1 Oct 2026). Live quote blijft de officiële estimator."),
        ("Check 4 · Catalogus-index is Engels",
         "/api/products/ op deze host blijft Engels. sneakers werkt; turnschoenen vaak niet."),
        ("Check 5 · AllChinaBuy Canada blijft een andere dest",
         "allchinabuyspreadsheet.ca is AllChinaBuy Canada. acbuyspreadsheets.nl blijft ACBuy Nederland. Geen 301 tussen landen."),
        ("Hoe we dit controleren",
         "Gedateerde checks, geen bedrijfsblog. Rankende gidsen (verzending, review, handleiding) blijven eigen URL’s; deze Nieuws-pagina overschrijft ze niet."),
    ]
    ld = itemlist_ld(
        url=f"https://{HOST}/nieuws/",
        name="ACBuy NL desk checks",
        items=[(h, p) for h, p in items],
    )
    cards = "".join(
        f'<article class="ncard"><h3>{escape(h)}</h3><p>{escape(p)}</p></article>'
        for h, p in items
    )
    body = f"""
<article class="pw">
  <span class="eyebrow" style="color:var(--acd)">Nieuws</span>
  <h1>Wat we op de platform hebben nagekeken, met datum</h1>
  <p class="lead">Eigen URL, zoals Novedades op de Spaanse gids. Geen bijlage onder de homepage. Stand {escape(DATE)}.</p>
  {cards}
</article>
"""
    return _shell(
        "Nieuws: wat we hebben nagekeken op ACBuy voor Nederland",
        "Gedateerde checks: estimator NL, Help-SPA, EUR-weergave, Engelse catalogus, geen 301 naar Canada.",
        f"https://{HOST}/nieuws/",
        [ld],
        body,
        "/nieuws/",
    )


def build_about() -> str:
    body = f"""
<article class="pw">
  <span class="eyebrow" style="color:var(--acd)">Over ons</span>
  <h1>Een onafhankelijke site over ACBuy, in het Nederlands</h1>
  <p class="lead">{escape(HOST)} is redactioneel onafhankelijk. We nemen geen bestellingen aan, zien je account niet, en rekenen geen porto.</p>
  <h2>Wat deze host is</h2>
  <p>Een Nederland-gids in de trant van een landssite: homepage met catalogus, een verzendplan, hulp, nieuws en deze Over-ons-pagina. De oranje balk zegt welk platform we bespreken — niet dat wij de app zijn.</p>
  <h2>Wat deze host niet is</h2>
  <p>Geen shop, geen magazijn, geen ticketsysteem. Claims alleen op {escape(OFFICIAL)}. Canada blijft AllChinaBuy op allchinabuyspreadsheet.ca. allchinabuyspreadsheet.nl is een extra host van hetzelfde land en wijst naar deze dest. Geen land-wissel.</p>
  <h2>Bronnen</h2>
  <p>Invoer: <a href="https://www.belastingdienst.nl/wps/wcm/connect/nl/douane/" rel="noopener">Belastingdienst Douane</a>. Live geld: <a href="{escape(EST)}">{escape(EST)}</a>. Officiële Help is een JavaScript-shell — {escape(STORAGE)}</p>
  <h2>Registratiecodes</h2>
  <p>Codes horen op de coupon-URL. Ze staan niet in de title van de homepage en niet in deze kop. Zonder code kan ook.</p>
  <h2>Contact</h2>
  <p>Orders: in-app chat op ACBuy. Deze gids: <a href="mailto:support@{escape(HOST)}">support@{escape(HOST)}</a>. Als een kolom of een link stukgaat, zetten we dat met datum op <a href="/nieuws/">Nieuws</a>.</p>
</article>
"""
    return _shell(
        "Over ons: onafhankelijke ACBuy-gids voor Nederland",
        "acbuyspreadsheets.nl is redactioneel onafhankelijk. Geen bestellingen, geen accounttoegang.",
        f"https://{HOST}/over-ons/",
        [],
        body,
        "/over-ons/",
    )


def _assert_ok(html: str, page: str) -> None:
    err = validate_desk(html, FACTS, page=page)
    if INVITE in html or INVITE2 in html or INVITE3 in html:
        if page == "home":
            err.append("invite token on homepage")
    if re.search(r"90\s*dagen|90\s*days", html, flags=re.I):
        err.append("invented 90-day copy")
    if "Georgia" in html or "#00C853" in html:
        err.append("Georgia / HipoBuy green")
    fp = dest_local_pack("NL")["fingerprint"]
    if page in ("home", "help") and fp not in html:
        err.append("missing NL fingerprint")
    for alien in ALIENS:
        if alien in html:
            err.append(f"sister leak {alien}")
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
    css_path = _desk_css_path()
    css_path.parent.mkdir(parents=True, exist_ok=True)
    css_path.write_text(CSS, encoding="utf-8")
    logo = write_wordmark(_wordmark_path())
    pages = {
        "home": (dest / "index.html", build_home(), "home"),
        "help": (dest / "hulp" / "index.html", build_help(), "help"),
        "news": (dest / "nieuws" / "index.html", build_news(), "news"),
        "about": (dest / "over-ons" / "index.html", build_about(), "about"),
    }
    out: dict[str, Path] = {"css": css_path, "logo": logo}
    for key, (path, html, page) in pages.items():
        _assert_ok(html, page)
        n = len(html.encode("utf-8"))
        if n < (DEST_MIN if key == "home" else 4000):
            raise SystemExit(f"{key} too small {n}")
        path.write_text(html, encoding="utf-8")
        print("wrote", path, n)
        out[key] = path
    theme = OUT / "shared" / "themes" / "acbuy-theme.css"
    theme.parent.mkdir(parents=True, exist_ok=True)
    if not theme.is_file():
        theme.write_text(
            "/* ACBuy country dest */\n:root { --primary: #E87000; --primary-dark: #c45f00; --primary-soft: #FFF3E0; --nav-dark: #111111; }\n",
            encoding="utf-8",
        )
    return out


def _clean_article(html: str) -> str | None:
    article = extract_article(html)
    if not article:
        return None
    wrapped = "<body>" + article + "</body>"
    while True:
        block = _element_inner(wrapped, "main")
        if not block:
            break
        inner, _s, _e = block
        if _text_len(inner) < max(120, int(_text_len(article) * 0.75)):
            break
        article = inner.strip()
        wrapped = "<body>" + article + "</body>"
    return article


def wrap_inner(html: str, page_href: str) -> tuple[str | None, str]:
    article = _clean_article(html)
    if not article:
        return None, "no-article"
    if _text_len(article) < 120:
        return None, "thin-article"
    head = _head_inner(html)
    inject = (
        "<!-- acbuy nl desk chrome 20261005 -->\n"
        '<link rel="preconnect" href="https://fonts.googleapis.com">\n'
        '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
        '<link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&display=swap" rel="stylesheet">\n'
        '<link rel="stylesheet" href="/assets/css/acbuy-theme.css?v=20261005-esref">\n'
        '<link rel="stylesheet" href="/assets/css/acbuy-nl-desk.css?v=20261005-esref">\n'
    )
    if "acbuy-nl-desk.css" not in head:
        head = head.rstrip() + "\n" + inject + "\n"
    trailing = after_footer_keep(html, article)
    extra_scripts = _body_scripts_outside_article(html, article + trailing)
    out = (
        "<!DOCTYPE html>\n"
        f"{_html_tag(html)}\n"
        f"<head>\n{head.rstrip()}\n</head>\n"
        f"<body {INNER_MARKER}>\n"
        f"{_header(page_href)}"
        f'<main id="main" class="inner-article">\n{article}\n</main>\n'
        f"{_footer()}\n"
        f"{trailing}\n"
        f"{extra_scripts}\n"
        "</body></html>\n"
    )
    if "Georgia" in out and "#00C853" in out:
        return None, "georgia-leak"
    if INVITE in out and page_href.rstrip("/") in {"", "/"}:
        return None, "invite-on-home"
    return out, "ok"


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
        f"mkdir -p '{bak}' '{root}/hulp' '{root}/nieuws' '{root}/over-ons' '{root}/assets/css' '{root}/assets/images'",
    )
    sftp = client.open_sftp()
    mapping = {
        "home": f"{root}/index.html",
        "help": f"{root}/hulp/index.html",
        "news": f"{root}/nieuws/index.html",
        "about": f"{root}/over-ons/index.html",
    }
    for key, remote in mapping.items():
        local = files[key]
        raw = local.read_text(encoding="utf-8")
        if key in ("home", "help") and dest_local_pack("NL")["fingerprint"] not in raw:
            raise SystemExit(f"refusing {key} without fingerprint")
        if key == "home" and (INVITE in raw or "90 days" in raw.lower()):
            raise SystemExit("refusing home with invite or 90-day copy")
        _run(client, f"test -f '{remote}' && cp -a '{remote}' '{bak}/{key}.html' || true")
        sftp.put(str(local), remote)
        print("PUT", remote, local.stat().st_size)
    theme = OUT / "shared" / "themes" / "acbuy-theme.css"
    sftp.put(str(theme), f"{root}/assets/css/acbuy-theme.css")
    sftp.put(str(files["css"]), f"{root}/assets/css/acbuy-nl-desk.css")
    sftp.put(str(files["logo"]), f"{root}/assets/images/acbuy-wordmark.png")
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
        f"chown -R www:www '{root}/index.html' '{root}/hulp' '{root}/nieuws' '{root}/over-ons' '{root}/assets/css' "
        f"'{root}/acbuy-shipping-guide' '{root}/is-acbuy-legit' '{root}/how-to-use-acbuy' '{root}/acbuy-coupons' "
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
        (f"https://{HOST}/hulp/", "help", True),
        (f"https://{HOST}/nieuws/", "news", False),
        (f"https://{HOST}/over-ons/", "about", False),
        (f"https://{HOST}/acbuy-shipping-guide/", "ranked", False),
        (f"https://{HOST}/is-acbuy-legit/", "ranked", False),
    ]
    for url, kind, need_local in checks:
        code, final, loc, body = fetch(url, follow=True)
        html = body.decode("utf-8", "replace")
        print(kind, code, "bytes", len(body), "cms", "nlo-logo" in html or "acbuy-wordmark" in html)
        if code != 200:
            print(" FAIL status"); fail += 1
        if need_local and (fp not in html or 'id="local"' not in html):
            print(" FAIL local"); fail += 1
        if kind == "home":
            if INVITE in html or re.search(r"90\s*days", html, re.I):
                print(" FAIL invite/90"); fail += 1
            if "Independent desk — not the official" in html:
                print(" FAIL english leftover"); fail += 1
            if "Catalogus" not in html or "ACBuy Spreadsheet" not in html:
                print(" FAIL dutch hero"); fail += 1
            if "allchinabuyspreadsheet.ca" in html:
                print(" FAIL planning dump on home"); fail += 1
            if "FAQPage" not in html:
                print(" FAIL home FAQPage"); fail += 1
            for alien in ("Packstation", "form A1A 1A1"):
                if alien in html:
                    print(" FAIL alien", alien); fail += 1
        if kind == "help" and "FAQPage" not in html:
            print(" FAIL help FAQPage"); fail += 1
        if kind == "news" and "ItemList" not in html:
            print(" FAIL news ItemList"); fail += 1
        if kind == "about" and "ContactPoint" not in html:
            print(" FAIL about ContactPoint"); fail += 1
        if kind == "ranked":
            if len(body) < 4000:
                print(" FAIL ranked thin"); fail += 1
            if "nlo-logo" not in html and "acbuy-wordmark" not in html:
                print(" FAIL ranked chrome"); fail += 1
    for twin, target in (
        ("allchinabuyspreadsheet.nl", HOST),
        ("acbuyspreadsheets.ca", "allchinabuyspreadsheet.ca"),
    ):
        code, _, loc, _ = fetch(f"https://{twin}/", follow=False)
        print("twin", twin, code, loc)
        if code not in (301, 302, 308) or target not in (loc or ""):
            print(" FAIL twin"); fail += 1
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
