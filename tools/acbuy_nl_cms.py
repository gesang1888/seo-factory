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
CMS_PAGES = [
    ("/", "Catalogus"),
    ("/acbuy-shipping-guide/", "Verzending"),
    ("/how-to-use-acbuy/", "Handleiding"),
    ("/hulp/", "Hulp"),
    ("/nieuws/", "Nieuws"),
    ("/over-ons/", "Over ons"),
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
    html = local_guide_html(FACTS).strip()
    extra = (
        f'<p class="local-src">Nederlandse postcode (vorm 1234 AB). Estimator-land is NL, '
        f"niet EU, niet BE, niet het .com-hub. {escape(STORAGE)} "
        f"Live-geld staat in <a href=\"{escape(EST)}\">{escape(EST)}</a> — deze HTML is geen kassa.</p>"
    )
    if not html.endswith("</section>"):
        raise RuntimeError("missing #local section")
    return html[: -len("</section>")] + extra + "\n</section>"


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
        on = ' class="on"' if href == page else ""
        bits.append(f'<li><a href="{escape(href)}"{on}>{escape(lab)}</a></li>')
    local = "/#local" if page != "/" else "#local"
    bits.append(f'<li><a href="{escape(local)}">Lokaal</a></li>')
    return "".join(bits)


def _header(page: str) -> str:
    return f"""{skip_link(skip_label("nl"))}<div class="ann">Onafhankelijke ACBuy Nederland-desk · oranje chrome · geen kassa op deze host</div>
<header class="nav" role="banner">
  <div class="nbrand">
    <a href="/" class="nlo">
      <img src="/assets/images/acbuy-wordmark.png?v=20261005-nl" alt="ACBuy" class="nlo-logo"
           onerror="this.style.display='none';this.nextElementSibling.style.display='flex'">
      <span class="nfb" style="display:none">A</span>
    </a>
    <div class="nregion" title="Nederland"><span class="nregion-flag">🇳🇱</span></div>
  </div>
  <ul class="nl">{_nav(page)}</ul>
  <div class="nact">
    <span class="blc" aria-label="Taal en valuta van deze desk">🇳🇱 NL · EUR</span>
    <a class="bwa" href="{escape(REG)}" rel="noopener sponsored">Registreren</a>
  </div>
</header>
"""


def _footer() -> str:
    keep = "".join(f'<li><a href="{escape(h)}">{escape(l)}</a></li>' for h, l in KEEP)
    cms = "".join(f'<li><a href="{escape(h)}">{escape(l)}</a></li>' for h, l in CMS_PAGES[3:])
    return f"""<footer class="ft">
  <div class="fti">
    <div>
      <div class="flo"><img src="/assets/images/acbuy-wordmark.png?v=20261005-nl" alt="ACBuy" class="flo-logo"><span>ACBuy Nederland</span></div>
      <p class="ftg">Onafhankelijke infodesk op {escape(HOST)}. Niet de officiële ACBuy-app. Geen bestellingen, geen kassa. AllChinaBuy Canada blijft een aparte host — geen 301 tussen landen.</p>
    </div>
    <div class="fc"><h4>Op deze host</h4><ul>{keep}</ul></div>
    <div class="fc"><h4>Desk</h4><ul>{cms}<li><a href="{escape(EST)}">Vracht-schatter</a></li></ul></div>
  </div>
  <div class="fb">
    <p>Redactie: <a href="mailto:support@{escape(HOST)}">support@{escape(HOST)}</a></p>
    <p>© 2026 {escape(HOST)} — onafhankelijk. Checkout alleen op {escape(OFFICIAL)}.</p>
  </div>
</footer>
"""


CSS = f"""
:root{{
  --acc:{ACC};--acd:#c45f00;--acl:#FFF3E0;
  --bk:#0A0A0A;--g1:#1A1A1A;--g2:#2D2D2D;--g3:#555;--g4:#888;--g5:#E5E5E5;--g6:#F6F6F6;--wh:#fff;
  --f:'DM Sans',Inter,system-ui,sans-serif;--m:ui-monospace,monospace;--r:10px;--rl:16px;
}}
*,*::before,*::after{{box-sizing:border-box;margin:0;padding:0}}
html{{scroll-behavior:smooth}}
body{{font-family:var(--f);background:var(--wh);color:var(--bk);font-size:15px;line-height:1.7;-webkit-font-smoothing:antialiased}}
a{{color:var(--acc);text-decoration:none}}
a:hover{{text-decoration:underline;text-underline-offset:3px}}
img{{max-width:100%;display:block}}
.skip{{position:absolute;left:-999px;top:8px;background:#fff;padding:8px 12px;z-index:20;border-radius:8px}}
.skip:focus{{left:12px}}
.ann{{background:var(--acc);color:#fff;text-align:center;padding:9px 16px;font-size:13px;font-weight:500}}
.nav{{position:sticky;top:0;z-index:100;background:var(--wh);border-bottom:1px solid var(--g5);padding:0 24px;min-height:60px;display:flex;align-items:center;justify-content:space-between;gap:16px;flex-wrap:wrap}}
.nbrand{{display:flex;align-items:center;gap:12px}}
.nlo{{display:flex;align-items:center}}
.nlo-logo{{display:block;width:162px;height:35px;object-fit:contain;object-position:left center}}
.nfb{{width:28px;height:28px;background:var(--acc);border-radius:6px;display:flex;align-items:center;justify-content:center;color:#fff;font-weight:700}}
.nregion-flag{{font-size:22px;line-height:1}}
.nl{{display:flex;align-items:center;gap:4px;list-style:none;flex-wrap:wrap}}
.nl a{{font-size:13px;padding:6px 10px;border-radius:6px;color:var(--g4)}}
.nl a:hover,.nl a.on{{background:var(--g6);color:var(--bk);text-decoration:none;font-weight:500}}
.nact{{display:flex;align-items:center;gap:8px}}
.blc{{display:inline-flex;align-items:center;gap:5px;padding:6px 10px;border:1px solid var(--g5);border-radius:8px;font-size:13px;font-weight:500}}
.bwa{{display:inline-flex;align-items:center;padding:7px 14px;background:var(--acc);color:#fff;border-radius:8px;font-size:13px;font-weight:600}}
.bwa:hover{{background:var(--acd);text-decoration:none}}
.hero{{max-width:860px;margin:0 auto;padding:56px 24px 36px;text-align:center}}
.hbg{{display:inline-flex;align-items:center;gap:6px;background:var(--acl);color:var(--acd);font-size:12px;font-weight:600;padding:5px 14px;border-radius:20px;margin-bottom:18px}}
.hero h1{{font-size:clamp(30px,5vw,48px);font-weight:700;letter-spacing:-1.5px;line-height:1.12;margin-bottom:16px}}
.hero h1 em{{font-style:normal;color:var(--acc)}}
.hsub{{font-size:17px;color:var(--g3);max-width:640px;margin:0 auto 28px;line-height:1.75}}
.hctas{{display:flex;justify-content:center;gap:12px;flex-wrap:wrap;margin-bottom:36px}}
.cp{{padding:13px 24px;background:var(--acc);color:#fff;border-radius:10px;font-weight:600}}
.cp:hover{{background:var(--acd);text-decoration:none}}
.cs{{padding:12px 22px;border:1.5px solid var(--g5);color:var(--bk);border-radius:10px;font-weight:500}}
.hst{{display:flex;justify-content:center;border:1px solid var(--g5);border-radius:var(--rl);overflow:hidden;max-width:640px;margin:0 auto}}
.hs{{flex:1;padding:14px 8px;text-align:center;border-right:1px solid var(--g5)}}
.hs:last-child{{border-right:none}}
.hsn{{font-size:18px;font-weight:700}}
.hsl{{font-size:11px;color:var(--g4);text-transform:uppercase;letter-spacing:.4px}}
.sg-sec{{max-width:1100px;margin:0 auto;padding:28px 24px 8px}}
.sg-sec h2,.stit{{font-size:clamp(22px,3vw,30px);font-weight:700;letter-spacing:-.5px;margin:0 0 8px}}
.ssub{{color:var(--g3);margin:0 0 14px;font-size:15px}}
.local-steps{{margin:12px 0 0;padding:0;list-style:none;display:grid;gap:12px}}
.local-steps li{{border:1px solid var(--g5);border-radius:12px;padding:14px 16px;background:#fff}}
.local-steps strong{{display:block;margin:0 0 6px}}
.local-src{{font-size:14px;color:#334155;line-height:1.7;margin:14px 0 0}}
#local{{scroll-margin-top:88px}}
.prose{{max-width:820px;margin:0 auto;padding:8px 24px 12px}}
.prose p,.prose li{{font-size:15px;color:var(--g2);line-height:1.8;margin-bottom:12px}}
.prose h2,.prose h3{{margin:28px 0 10px;font-size:22px;color:var(--bk)}}
.sg-cats{{display:grid;grid-template-columns:repeat(auto-fill,minmax(140px,1fr));gap:10px}}
.sg-cat{{display:block;border:1px solid var(--g5);border-radius:12px;padding:14px;text-decoration:none;color:inherit;background:#fff}}
.sg-cat span{{display:block;color:var(--g4);font-size:12px;margin-top:4px}}
.sg-mw{{max-width:1100px;margin:0 auto;padding:12px 24px 40px}}
.sg-chips{{display:flex;flex-wrap:wrap;gap:8px;margin:10px 0}}
.sg-chips button{{border:1px solid var(--g5);background:#fff;border-radius:999px;padding:6px 12px;cursor:pointer}}
.sg-chips button.on{{background:var(--acl);border-color:var(--acc);color:var(--acd);font-weight:700}}
.sg-fbar{{display:flex;gap:10px;align-items:center;margin:8px 0 14px}}
.sg-fbar input{{flex:1;padding:10px 12px;border-radius:8px;border:1px solid var(--g5)}}
.sg-grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(180px,1fr));gap:12px}}
.sg-card{{border:1px solid var(--g5);border-radius:12px;overflow:hidden;background:#fff;display:flex;flex-direction:column}}
.sg-card img{{width:100%;aspect-ratio:1;object-fit:cover;background:#f1f5f9}}
.sg-card .b{{padding:10px}}
.sg-card .t{{font-size:13px;font-weight:600;min-height:2.4em}}
.sg-card .pr{{font-weight:800;color:var(--acc)}}
.sg-card .pr-src{{font-size:11px;color:#94a3b8}}
.sg-card a.buy{{margin:0 10px 10px;text-align:center;padding:8px;border-radius:8px;background:var(--acc);color:#fff;font-size:12.5px;font-weight:600;text-decoration:none}}
.sg-fx{{color:#64748b;font-size:13px;line-height:1.55;margin:4px 0 10px}}
.sg-faq{{border:1px solid var(--g5);border-radius:10px;padding:12px 14px;margin:8px 0;background:#fff}}
.sg-faq summary{{cursor:pointer;font-weight:700}}
.ncard{{border:1px solid var(--g5);border-radius:var(--rl);padding:16px 18px;margin-bottom:12px}}
.ncard h3{{font-size:15px;font-weight:600;margin-bottom:6px}}
.guides{{display:grid;grid-template-columns:repeat(auto-fill,minmax(240px,1fr));gap:14px;padding:8px 24px 40px;max-width:1100px;margin:0 auto}}
.gc{{border:1px solid var(--g5);border-radius:var(--rl);padding:18px;display:flex;flex-direction:column;gap:8px;text-decoration:none;color:inherit}}
.gc:hover{{border-color:var(--acc);text-decoration:none}}
.gtg{{font-size:10px;font-weight:700;text-transform:uppercase;letter-spacing:.5px;padding:3px 8px;border-radius:4px;background:var(--acl);color:var(--acd);width:fit-content}}
.tw{{overflow:auto;border:1px solid var(--g5);border-radius:12px;margin:12px 0 18px}}
.tw table{{width:100%;border-collapse:collapse;font-size:14px}}
.tw th,.tw td{{text-align:left;padding:10px 12px;border-bottom:1px solid var(--g5);vertical-align:top}}
.tw th{{background:var(--g6);font-size:12px;letter-spacing:.4px;text-transform:uppercase;color:var(--g3)}}
.tw code{{font-family:var(--m);font-size:12px}}
.ft{{background:#111;color:#ccc;padding:40px 24px;margin-top:24px}}
.fti{{max-width:1100px;margin:0 auto;display:grid;grid-template-columns:1.5fr 1fr 1fr;gap:32px}}
.flo{{display:flex;align-items:center;gap:8px;color:#fff;font-weight:600;margin-bottom:10px}}
.flo-logo{{height:26px;width:auto}}
.ftg{{font-size:13px;color:#888;line-height:1.65}}
.fc h4{{font-size:12px;letter-spacing:.6px;color:#888;margin-bottom:12px;text-transform:uppercase}}
.fc ul{{list-style:none}}
.fc li{{margin-bottom:8px}}
.fc a{{color:#888}}
.fc a:hover{{color:#fff}}
.fb{{max-width:1100px;margin:24px auto 0;padding-top:16px;border-top:1px solid #2D2D2D;display:flex;justify-content:space-between;gap:12px;flex-wrap:wrap;font-size:12px;color:#666}}
.fb a{{color:#888}}
.pw{{max-width:820px;margin:0 auto;padding:28px 24px 48px}}
.pw h1{{font-size:clamp(26px,4vw,36px);letter-spacing:-.8px;margin:0 0 12px}}
.pw h2{{font-size:20px;margin:28px 0 10px}}
.pw p{{margin:0 0 12px;color:var(--g2)}}
.inner-article{{max-width:860px;margin:0 auto;padding:28px 24px 48px}}
.inner-article h1{{font-size:clamp(26px,4vw,36px);letter-spacing:-.8px;margin:0 0 12px}}
.trust{{background:var(--acl);border-top:1px solid #f3d5a8;border-bottom:1px solid #f3d5a8;padding:18px 24px;margin:12px 0}}
.ti{{max-width:1100px;margin:0 auto;display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:12px;font-size:13px;font-weight:600;color:var(--acd)}}
@media(max-width:860px){{.nl{{width:100%}}.fti{{grid-template-columns:1fr}}.nlo-logo{{width:132px}}}}
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
<link rel="stylesheet" href="/assets/css/acbuy-theme.css?v=20261005-nl">
<link rel="stylesheet" href="/assets/css/acbuy-nl-desk.css?v=20261005-nl">
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
        ("sneakers", "Sneakers"),
        ("hoodie", "Hoodie"),
        ("jacket", "Jas"),
        ("t-shirt", "T-shirt"),
        ("pants", "Broek"),
        ("bag", "Tassen"),
        ("watch", "Horloges"),
        ("shoes", "Schoenen"),
        ("hat", "Petten"),
        ("glasses", "Brillen"),
        ("jewelry", "Sieraden"),
        ("electronics", "Electronica"),
    ]
    wall = "".join(
        f'<a class="sg-cat" href="#catalog" data-q="{escape(q)}"><strong>{escape(labn)}</strong><span>{escape(q)}</span></a>'
        for q, labn in cats
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
  <div class="hbg">Lab {escape(DATE)} · NL-adres · EUR-weergave</div>
  <h1>Met <em>ACBuy</em> naar Nederland verzenden</h1>
  <p class="hsub">Uit China naar een Nederlands huisadres: ACBuy koopt en slaat op, jij boekt de lijn. Deze host is de oranje Nederland-desk — catalogus, lokale checks, Hulp, Nieuws en Over ons — geen kassa.</p>
  <div class="hctas">
    <a class="cs" href="#local">Check NL</a>
    <a class="cp" href="{escape(REG)}" rel="noopener sponsored">Registreren op ACBuy</a>
    <a class="cs" href="/how-to-use-acbuy/">Handleiding</a>
  </div>
  <div class="hst">
    <div class="hs"><div class="hsn">EUR</div><div class="hsl">Weergave</div></div>
    <div class="hs"><div class="hsn">NL</div><div class="hsl">Estimator</div></div>
    <div class="hs"><div class="hsn">DHL</div><div class="hsl">Vaak last-mile</div></div>
    <div class="hs"><div class="hsn">Geen kassa</div><div class="hsl">Deze host</div></div>
  </div>
</section>
{_local_block()}
<section class="sg-sec" id="agent">
  <h2>ACBuy is de inkoopagent, deze host is de NL-desk</h2>
  <p class="ssub">acbuyspreadsheets.nl is geen shop en geen AllChinaBuy-Canada-kloon.</p>
  <div class="prose">
    <p>ACBuy koopt in Chinese derdewinkels op jouw naam, maakt magazijnfoto’s, en jij kiest daarna een internationale SKU naar Nederland. Betalen, tickets en QC blijven op {escape(OFFICIAL)}. Deze hostname int geen kaart, opent geen order-ID en is geen 301 vanaf een ander land.</p>
    <p>De oranje balk, het woordmerk en de EUR-weergave horen bij deze ACBuy-desk. De officiële app kan nog USD-cijfers tonen als alleen het valutateken wisselt — vertrouw de estimator, niet een HTML-tabel. Labdatum {escape(DATE)}.</p>
    <p>AllChinaBuy is dezelfde officiële winkel op acbuy.com, met een Canadese dest op allchinabuyspreadsheet.ca. Nederland blijft ACBuy: {escape(HOST)}. Zusterhost allchinabuyspreadsheet.nl 301’t naar hier; Canada blijft Canada. Geen land-wissel in de title.</p>
    <p>Eerste haul in het kort: plak een Weidian- of Taobao-link in de app, betaal product plus China-vervoer, wacht op QC-foto’s, bundel wat je houdt, en boek pas dan een lijn met bestemming Nederland — niet EU, niet België. Tokens horen op de coupon-URL, niet in de title van deze homepage.</p>
  </div>
  <ol class="local-steps">
    <li><strong>1. Kopen in China</strong>Open de live fiche op ACBuy. Restricted of prijs 0 overslaan.</li>
    <li><strong>2. QC in het magazijn</strong>Keur of weiger op de foto’s. Extra hoeken koop je in de app, niet hier.</li>
    <li><strong>3. Lijn naar Nederland</strong>Estimator-land NL, Nederlandse postcode 1234 AB. Live geld: {escape(EST)}.</li>
    <li><strong>4. Last-mile</strong>Vaak DHL. Collect kan extra innen. Bron: Belastingdienst Douane, geen verzonnen aangegeven waarde.</li>
  </ol>
</section>
<section class="sg-sec" id="sheet-explain">
  <h2>Spreadsheet op deze host</h2>
  <p class="ssub">Een index van finds, geen Excel-bestand en geen voorraad van ACBuy.</p>
  <div class="prose">
    <p>De kaarten onderaan komen van /api/products/ op {escape(HOST)}. Engelse keys (sneakers, hoodie, jacket) vullen de grid. Nederlandse woorden zoals «turnschoenen» geven vaak nul hits — dat is de index, geen lege winkel. Gemeten {escape(DATE)}.</p>
    <p>Restricted of prijs 0 is een platformblokkade of een dode Weidian/Taobao-link, geen douane-inbeslagname voor Nederland. Open dezelfde dag de fiche op {escape(OFFICIAL)} voordat je een haul plant op deze HTML.</p>
    <p>De rankende spreadsheet-URL /acbuy-spreadsheet/ blijft staan. Deze homepage overschrijft hem niet met een 5KB-sjabloon. Coupons en invite-tokens blijven op /acbuy-coupons/ en /acbuy-invite-code/.</p>
  </div>
</section>
<section class="sg-sec" id="restricted">
  <h2>Restricted</h2>
  <p class="ssub">Geen checkout forceren naar Nederland op een nulprijs.</p>
  <div class="prose">
    <p>Bouw de haul niet op een kaart zonder live fiche. Restricted is een inkoopblokkade van het platform, geen bericht van de Douane. Tabak, alcohol, medicijnen en verboden spullen reizen niet — dat is de regel van ACBuy, niet een drempel die deze desk verzint.</p>
    <p>Vloeistoffen en poeders kunnen extra papier vragen. Check de live fiche dezelfde ochtend. Deze desk opent geen ticket.</p>
  </div>
</section>
<section class="sg-sec" id="cat-wall">
  <h2>Categorieën</h2>
  <p class="ssub">Twaalf Engelse index-keys. Lokale woorden geven vaak 0 kaarten.</p>
  <div class="sg-cats">{wall}</div>
</section>
{catalog}
<section class="sg-sec" id="states">
  <h2>Negen statussen, live labels in de app</h2>
  <p class="ssub">Estimator-land is NL, niet deze TLD. Deze tabel is een Nederlandse leeshulp, geen SLA en geen magazijn-dagentelling.</p>
  <div class="tw"><table>
    <thead><tr><th>State in de app</th><th>Wat het hier betekent</th></tr></thead>
    <tbody>
      <tr><td><code>Order Submitted</code></td><td>Bestelling verstuurd; product in China betaald.</td></tr>
      <tr><td><code>Order Placed</code></td><td>ACBuy koopt in de Chinese shop op jouw naam.</td></tr>
      <tr><td><code>Seller Shipped</code></td><td>De Chinese verkoper heeft verzonden.</td></tr>
      <tr><td><code>Arrived at Warehouse</code></td><td>Aangekomen in het magazijn in China.</td></tr>
      <tr><td><code>Inspection &amp; Storage</code></td><td>QC en opslag. Gratis-dagen: alleen de live Help-SPA, niet dit HTML.</td></tr>
      <tr><td><code>Shipping Requested</code></td><td>Jij bundelt en boekt de internationale lijn naar Nederland.</td></tr>
      <tr><td><code>Parcel Packed</code></td><td>Doos wordt ingepakt na jouw SKU-keuze.</td></tr>
      <tr><td><code>Shipped</code></td><td>Vertrek uit China. Tracking staat in de app.</td></tr>
      <tr><td><code>Delivered</code></td><td>Last-mile (vaak DHL) heeft bezorgd; ontvangst bevestigen in de app.</td></tr>
    </tbody>
  </table></div>
  <p>Onafhankelijkheid: {escape(HOST)} is een infodesk, niet ACBuy. Geen bestellingen, geen accounttoegang, geen porto. AllChinaBuy Canada ({escape("allchinabuyspreadsheet.ca")}) blijft een Canadese dest.</p>
</section>
<section class="sg-sec" id="shots">
  <h2>Officiële app, geen stockfoto’s</h2>
  <p class="ssub">Live schermen en live geld staan op ACBuy, gedateerd {escape(DATE)}. Deze desk plakt geen verzonnen screenshots.</p>
  <div class="prose">
    <p>Open de estimator met bestemming Netherlands, niet EU. Help laadt als JavaScript-shell: zonder script zie je geen magazijnartikel, dus deze desk kopieert daar geen dagen-aantal uit. QC-foto’s, tickets en iDEAL zitten in de app.</p>
  </div>
  <p><a class="cp" href="{escape(OFFICIAL)}" rel="noopener">Open ACBuy</a>
     <a class="cs" href="{escape(EST)}" rel="noopener">Vracht-schatter</a>
     <a class="cs" href="{escape(HELP)}" rel="noopener">Officiële Help</a></p>
</section>
<section class="sg-sec" id="lab">
  <h2>{escape(lab["h2"])}</h2>
  <p class="ssub">{lab["ssub"]}</p>
  <div class="prose">
    <p>Labgewoonte: 1000 g / 35×25×10 cm, kleding. Volumgewicht op veel luchtlijnen is L×B×H/8000 (hier 1,094 kg, vaak 1100 g gefactureerd). Factuur = max(werkelijk, volume). Jouw doos wijkt af — daarom geen SKU-prijzen op deze homepage.</p>
    <p>Weergaveconversie van de China-kaart: X-Rates 1 Oct 2026, 1 CNY ≈ 0,132940 EUR. Dat is geen kassakoers. Als de officiële SPA na een eurosymbool nog USD-cijfers toont, vertrouw de cijfers in de app.</p>
    <p>Bron invoer: Douane. Geen 58-lijnen-snapshot, geen verzonnen aangegeven waarde. <a href="{escape(EST)}">{escape(lab["cta"])}</a> met bestemming Nederland, daarna de rankende <a href="/acbuy-shipping-guide/">verzendgids</a>.</p>
  </div>
</section>
<section class="sg-sec" id="faq">
  <h2>Veelgestelde vragen</h2>
  <p class="ssub">Vijftien vragen voor een Nederlands huisadres. Volledige antwoorden ook op /hulp/.</p>
  {faqs}
  <p class="ssub"><a href="/hulp/">Alle vragen op de hulppagina →</a></p>
</section>
<section class="sg-sec" id="news">
  <h2>Wat we hebben nagekeken</h2>
  <p class="ssub">Gedateerde desk-checks, geen bedrijfsblog.</p>
  <article class="ncard"><h3>Check 1 · {escape(DATE)} · NL-adres</h3><p>Estimator-bestemming moet NL zijn, niet EU. Belgische of Duitse postcode is het verkeerde land. Nederlandse postcodevorm 1234 AB, geen Duits afhaalautomaat-nummer.</p></article>
  <article class="ncard"><h3>Check 2 · Help is een SPA</h3><p>https://www.acbuy.com/help laadt als JavaScript-shell. Deze desk kopieert daar geen gratis-dagen-aantal uit.</p></article>
  <article class="ncard"><h3>Check 3 · EUR hier, dollars in de app</h3><p>Weergaveconversie van de China-kaart (X-Rates 1 Oct 2026). Kassacijfers alleen in de officiële estimator.</p></article>
  <p><a href="/nieuws/">Alle checks →</a></p>
</section>
<div class="trust"><div class="ti">
  <div>Geen kassa op deze host</div>
  <div>EUR-weergave, NL in de estimator</div>
  <div>Douane als invoerbron</div>
  <div>Rankende gidsen blijven</div>
</div></div>
<section>
  <h2 class="stit" style="max-width:1100px;margin:24px auto 8px;padding:0 24px">Gidsen op deze host</h2>
  <div class="guides">
    <a class="gc" href="/acbuy-shipping-guide/"><span class="gtg">Verzending</span><p><strong>Verzendgids NL</strong></p><p>Rankende URL. SKU en Douane op de verzenddag, niet deze homepage.</p></a>
    <a class="gc" href="/how-to-use-acbuy/"><span class="gtg">Stappen</span><p><strong>Handleiding</strong></p><p>Eerste order: kopen, QC, dan pas internationale lijn naar Nederland.</p></a>
    <a class="gc" href="/is-acbuy-legit/"><span class="gtg">Review</span><p><strong>Is ACBuy betrouwbaar?</strong></p><p>Bestaande review-URL blijft; deze desk overschrijft hem niet met 5KB.</p></a>
    <a class="gc" href="/acbuy-coupons/"><span class="gtg">Coupons</span><p><strong>Coupon-stacking</strong></p><p>Tokens blijven op de coupon-URL, niet in de title van deze homepage.</p></a>
    <a class="gc" href="/acbuy-spreadsheet/"><span class="gtg">Index</span><p><strong>Spreadsheet</strong></p><p>Rankende finds-URL. Homepage-catalogus is dezelfde index, EUR-weergave.</p></a>
    <a class="gc" href="/hulp/"><span class="gtg">Hulp</span><p><strong>Vijftien vragen</strong></p><p>Zelfde FAQ als hier, met langere antwoorden en JSON-LD FAQPage.</p></a>
  </div>
</section>
"""
    return _shell(
        "Met ACBuy naar Nederland verzenden — NL-adres, EUR-weergave, geen kassa",
        "ACBuy Nederland-desk: inkoopagent, catalogus, volumgewicht, Douane-bronnen. Lab 5 Oct 2026. Geen onderwaardering, geen invite in de title.",
        f"https://{HOST}/",
        [faq_ld("nl-NL", long_faqs(FACTS))],
        body,
        "/",
    )


def build_help() -> str:
    faqs = _faq_html()
    body = f"""
<div class="pw">
  <h1>Hulp: vijftien vragen over ACBuy in Nederland</h1>
  <p class="ssub">FAQ voor een Nederlands huisadres. Lab {escape(DATE)}. Geen onderwaardering. Deze pagina is de hulpbalk, niet de officiële ACBuy-SPA.</p>
  {_local_block()}
  <p>Deze pagina hoort bij een <strong>Nederlands huisadres</strong> op {escape(HOST)}. Wij zien je account niet. Bestellen, betalen en claims gaan alleen via <a href="{escape(OFFICIAL)}">{escape(OFFICIAL)}</a>.</p>
  <h2>Wat ACBuy is</h2>
  <p>ACBuy is een inkoopagent: hij koopt in Chinese shops op jouw naam en houdt de goederen in het magazijn tot jij een internationale lijn boekt. {escape(HOST)} is de Nederland-desk — oranje chrome, EUR-weergave, lokale checks — geen shop.</p>
  {faqs}
  <h2>Estimator en tickets</h2>
  <p>Open <a href="{escape(EST)}">{escape(EST)}</a> met bestemming Netherlands nadat de QC-foto’s er zijn. In een supportticket schrijf je Netherlands, niet Belgium of EU, ook als DHL last-mile lijkt. Twee dozen na een QC-split zijn twee schattingen.</p>
  <p>Officiële Help is een JavaScript-shell. Deze desk kopieert daar geen magazijn-dagentelling uit. Tokens staan op <a href="/acbuy-coupons/">/acbuy-coupons/</a>, niet in de title van de homepage.</p>
  <p><a href="/nieuws/">Nieuws met datum</a> · <a href="/over-ons/">Over ons</a> · <a href="/acbuy-shipping-guide/">Verzendgids</a> · <a href="{escape(EST)}">Officiële estimator</a></p>
</div>
"""
    return _shell(
        "Hulp: vijftien vragen over ACBuy in Nederland",
        "FAQ voor een Nederlands huisadres: twee betalingen, EUR-weergave, volumgewicht, Douane zonder onderwaardering. Stand 5 Oct 2026.",
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
         "https://www.acbuy.com/help geeft zonder JavaScript een SPA-fout. Daarom staat hier geen verzonnen magazijn-dagentelling."),
        ("Check 3 · EUR-weergave versus USD-cijfers in de app",
         "Deze desk toont EUR als weergave van de China-kaart (X-Rates 1 Oct 2026). Live quote blijft de officiële estimator."),
        ("Check 4 · Catalogus-index is Engels",
         "/api/products/ op deze host blijft Engels. sneakers werkt; turnschoenen vaak niet. Gemeten 5 Oct 2026."),
        ("Check 5 · AllChinaBuy Canada blijft een andere dest",
         "allchinabuyspreadsheet.ca is AllChinaBuy Canada. acbuyspreadsheets.nl blijft ACBuy Nederland. Geen 301 tussen landen."),
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
<div class="pw">
  <h1>Nieuws: gedateerde checks op de ACBuy NL-desk</h1>
  <p class="ssub">Geen bedrijfsblog. Alleen wat we op {escape(HOST)} konden narekenen. Lab {escape(DATE)}.</p>
  {cards}
  <p>Rankende gidsen op deze host blijven: <a href="/acbuy-shipping-guide/">verzending</a>, <a href="/is-acbuy-legit/">review</a>, <a href="/how-to-use-acbuy/">handleiding</a>. Deze nieuws-URL is de gedateerde checklist, geen overwrite van die artikelen.</p>
</div>
"""
    return _shell(
        "Nieuws: gedateerde ACBuy Nederland checks",
        "Vijf gedateerde checks op acbuyspreadsheets.nl: estimator NL, Help-SPA, EUR-weergave, Engelse catalogus, geen 301 naar Canada.",
        f"https://{HOST}/nieuws/",
        [ld],
        body,
        "/nieuws/",
    )


def build_about() -> str:
    body = f"""
<div class="pw">
  <h1>Over ons: onafhankelijke ACBuy-desk voor Nederland</h1>
  <p>{escape(HOST)} is redactioneel onafhankelijk. We nemen geen bestellingen aan, zien je account niet, en rekenen geen porto. De oranje balk en het woordmerk vertellen welk platform deze desk bespreekt — ACBuy — niet dat wij de app zijn.</p>
  <h2>Wat we wel zijn</h2>
  <p>Een Nederland-desk: lokale checks (Nederlandse postcode, estimator-land NL), catalogus met EUR-weergave, vijftien hulpvragen, gedateerde checks, en de rankende gidsen die al op deze host stonden.</p>
  <h2>Wat we niet zijn</h2>
  <p>Geen shop, geen magazijn, geen ticketsysteem. Claims alleen op {escape(OFFICIAL)}. We 301’en niet naar Canada en niet naar een .com-hub. allchinabuyspreadsheet.nl 301’t naar deze dest; allchinabuyspreadsheet.ca blijft AllChinaBuy Canada.</p>
  <h2>Bronnen</h2>
  <p>Invoer: <a href="https://www.belastingdienst.nl/wps/wcm/connect/nl/douane/" rel="noopener">Belastingdienst Douane</a>. Live geld: <a href="{escape(EST)}">{escape(EST)}</a>. Help: <a href="{escape(HELP)}">{escape(HELP)}</a> (SPA — geen verzonnen dagen-aantal). Valuta-weergave: X-Rates 1 Oct 2026. Labgewoonte 1000 g / 35×25×10 cm, geen SKU-prijzen op de homepage.</p>
  <h2>Invite</h2>
  <p>Registratiecodes horen op de coupon-URL. Ze staan niet in de title van de homepage en niet in deze Over-ons-kop. Zonder code kan ook.</p>
  <h2>Contact</h2>
  <p>ACBuy zelf zit op {escape(OFFICIAL)}. Contact voor orders: de in-app chat daar. Contact voor deze desk: <a href="mailto:support@{escape(HOST)}">support@{escape(HOST)}</a>. Als een labkolom of een link stukgaat, zetten we dat met datum in Nieuws. We herschrijven niet stiekem.</p>
</div>
"""
    return _shell(
        "Over ons: onafhankelijke ACBuy-desk voor Nederland",
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
        '<link rel="stylesheet" href="/assets/css/acbuy-theme.css?v=20261005-nl">\n'
        '<link rel="stylesheet" href="/assets/css/acbuy-nl-desk.css?v=20261005-nl">\n'
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
            if "Catalogus" not in html or "Met" not in html:
                print(" FAIL dutch hero"); fail += 1
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
