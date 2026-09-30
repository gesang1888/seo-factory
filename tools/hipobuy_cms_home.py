#!/usr/bin/env python3
"""Restore original CMS homepage chrome and put the live catalogue on top.

Same green / DM Sans skin as hipobuy.at before the Georgia overlay.
Catalogue (search + categories + /api/products/ cards) sits under the hero
on /, not on /#katalog and not on /hipobuy-spreadsheet/.
Does not touch hipobuyspreadsheet.net.
"""
from __future__ import annotations

import json
import re
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CMS_HOME = ROOT / "sites/hipobuy-shared/cms-home"

from hipobuy_trust_chrome import EST, GLOSS, MAIL, labels  # noqa: E402

INVITE = "VGEICZNX0"
REG = f"https://hipobuy.com/register?inviteCode={INVITE}"

CATMAP = {
    "shoes": "SNEAKERS",
    "slippers": "SLIPPERS",
    "tshirts": "T-SHIRT",
    "polo": "POLO",
    "shirt": "SHIRT",
    "pants": "SHORTS",
    "vest": "VEST",
    "long-sleeved": "LONG SLEEVED",
    "hoodies": "HOODIE",
    "sweater": "SWEATER",
    "shawl": "SHAWL",
    "bags": "BAG",
}
W2C_TO_FC = {
    "SNEAKERS": "shoes",
    "SLIPPERS": "slippers",
    "T-SHIRT": "tshirts",
    "POLO": "polo",
    "SHIRT": "shirt",
    "SHORTS": "pants",
    "VEST": "vest",
    "LONG SLEEVED": "long-sleeved",
    "LONG+SLEEVED": "long-sleeved",
    "HOODIE": "hoodies",
    "SWEATER": "sweater",
    "SHAWL": "shawl",
    "BAG": "bags",
}

CAT_CSS = """
.mw{max-width:1200px;margin:0 auto;padding:8px 24px 56px;display:grid;grid-template-columns:215px 1fr;gap:24px;align-items:start}
.sb{position:sticky;top:72px}
.sbtit{font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:.7px;color:var(--g4);margin-bottom:8px;padding-left:4px}
.sbsec{margin-bottom:22px}
.cl{list-style:none}
.cl li a{display:flex;align-items:center;justify-content:space-between;padding:6px 9px;border-radius:8px;font-size:13px;color:var(--g2);transition:background .12s,color .12s}
.cl li a:hover{background:var(--g6);color:var(--bk);text-decoration:none}
.cl li a.on{background:var(--acl);color:var(--acd);font-weight:500}
.cn{font-size:11px;color:var(--g4);font-family:var(--m)}
.cl li a.on .cn{color:var(--acc)}
.sbcard{background:var(--g6);border-radius:var(--rl);padding:13px}
.sbcard-t{font-size:13px;font-weight:500;margin-bottom:5px}
.sbcard-d{font-size:12px;color:var(--g3);line-height:1.55;margin-bottom:10px}
.sbwas{display:flex;align-items:center;justify-content:center;gap:6px;padding:8px;background:#25D366;color:#fff;border-radius:8px;font-size:13px;font-weight:500;width:100%;transition:opacity .15s}
.sbwas:hover{opacity:.88;text-decoration:none}.sbwas svg{width:14px;height:14px}
.fbar{display:flex;gap:8px;align-items:center;margin-bottom:16px;flex-wrap:wrap}
.sw{flex:1;min-width:180px;position:relative}
.sw svg{position:absolute;left:10px;top:50%;transform:translateY(-50%);width:15px;height:15px;color:var(--g4)}
.si{width:100%;height:37px;padding:0 12px 0 33px;border:1.5px solid var(--g5);border-radius:9px;font-family:var(--f);font-size:13px;background:var(--wh);outline:none;transition:border-color .15s}
.si:focus{border-color:var(--acc)}.si::placeholder{color:var(--g4)}
.ss{height:37px;padding:0 10px;border:1.5px solid var(--g5);border-radius:9px;font-family:var(--f);font-size:12.5px;background:var(--wh);outline:none;cursor:pointer}
.rc{font-size:13px;color:var(--g4);white-space:nowrap}.rc b{color:var(--bk);font-weight:500}
.pg{display:grid;grid-template-columns:repeat(auto-fill,minmax(180px,1fr));gap:13px;margin-bottom:24px}
.pcard{border:1px solid var(--g5);border-radius:var(--rl);overflow:hidden;background:var(--wh);transition:border-color .15s,transform .15s;cursor:pointer;display:flex;flex-direction:column}
.pcard:hover{border-color:var(--acc);transform:translateY(-2px)}
.pimg{aspect-ratio:1;background:var(--g6);position:relative;overflow:hidden}
.pimg img{width:100%;height:100%;object-fit:cover;display:block;transition:transform .3s}
.pcard:hover .pimg img{transform:scale(1.04)}
.pph{width:100%;height:100%;display:flex;align-items:center;justify-content:center;color:var(--g5)}
.pph svg{width:32px;height:32px}
.pbg{position:absolute;top:7px;left:7px;background:var(--acc);color:#fff;font-size:10px;font-weight:700;padding:2px 6px;border-radius:4px;text-transform:uppercase;letter-spacing:.3px}
.pbdy{padding:10px;flex:1;display:flex;flex-direction:column;gap:5px}
.pnm{font-size:13px;font-weight:500;color:var(--bk);line-height:1.4;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden}
.pmeta{display:flex;align-items:center;justify-content:space-between;margin-top:auto}
.ppr{font-size:14px;font-weight:700;color:var(--acc);font-family:var(--m)}
.ppl{font-size:10.5px;color:var(--g4);background:var(--g6);padding:2px 6px;border-radius:4px}
.plnk{display:block;margin:0 10px 10px;padding:7px;background:var(--acc);color:#fff;text-align:center;border-radius:8px;font-size:12.5px;font-weight:500;transition:background .15s}
.plnk:hover{background:var(--acd);text-decoration:none}
.pgn{display:flex;align-items:center;justify-content:center;gap:5px}
.pgb{width:32px;height:32px;display:flex;align-items:center;justify-content:center;border:1px solid var(--g5);border-radius:7px;font-size:12.5px;color:var(--g3);cursor:pointer;transition:all .12s;background:var(--wh)}
.pgb:hover{border-color:var(--acc);color:var(--acc)}.pgb.on{background:var(--acc);border-color:var(--acc);color:#fff;font-weight:500}
.sk{animation:pulse 1.5s ease-in-out infinite}.skim{background:var(--g5);aspect-ratio:1}.skl{height:11px;background:var(--g5);border-radius:4px;margin-bottom:7px}.skl.sh{width:55%}
@keyframes pulse{0%,100%{opacity:1}50%{opacity:.5}}
@media(max-width:768px){.mw{grid-template-columns:1fr}.sb{position:static}}
#home-trust{max-width:1100px;margin:0 auto;padding:8px 24px 8px}
#home-trust .sec{padding:36px 0 8px}
#home-trust .faq-item.open .faq-a{max-height:1600px}
.ncard{border:1px solid var(--g5);border-radius:var(--rl);padding:16px 18px;margin-bottom:12px;background:var(--wh)}
.ncard h3{font-size:15px;font-weight:600;margin-bottom:6px;color:var(--bk);letter-spacing:-.2px}
.ncard p{font-size:13.5px;color:var(--g3);line-height:1.7;margin:0}
.home-more{margin:4px 0 8px;font-size:13px;font-weight:600}
.tw{overflow-x:auto;margin:16px 0;border:1px solid var(--g5);border-radius:var(--rl)}
.tw table{width:100%;border-collapse:collapse;font-size:13px}
.tw th,.tw td{padding:10px 12px;text-align:left;border-bottom:1px solid var(--g5);vertical-align:top}
.tw th{background:var(--g6);font-size:11px;text-transform:uppercase;letter-spacing:.4px;color:var(--g4);font-weight:700}
.tw .mv{font-family:var(--m);font-weight:600;color:var(--acc);white-space:nowrap}
.tw tr:last-child td{border-bottom:none}
.tw code{font-family:var(--m);font-size:12px}
"""

SIDE_CATS = [
    ("all", "All Products"),
    ("shoes", "Sneakers & Shoes"),
    ("slippers", "Slippers"),
    ("tshirts", "T-Shirts"),
    ("polo", "Polo"),
    ("shirt", "Dress Shirts"),
    ("pants", "Pants / Shorts"),
    ("vest", "Vests & Outerwear"),
    ("long-sleeved", "Long Sleeved"),
    ("hoodies", "Hoodies"),
    ("sweater", "Sweaters"),
    ("shawl", "Shawls"),
    ("bags", "Bags"),
]


def _nav(key: str, d: dict, on: str = "/") -> str:
    L = labels(key)
    s = d["slugs"]
    on_n = on.rstrip("/") or "/"

    def item(href: str, lab: str) -> str:
        href_n = href.rstrip("/") or "/"
        cls = ' class="on"' if href_n == on_n else ""
        return f'<a href="{href}"{cls}>{escape(lab)}</a>'

    items = [item("/", L["sheet"])]
    if key in ("uk", "eu"):
        items.append(item("/hipobuy-coupons/", L["coupons"]))
    if key == "uk":
        items.append(item("/blog/posts/hipobuy-sizing-guide/", "UK sizing"))
    ship = "/guides/shipping/" if key == "us" else "/hipobuy-shipping-guide/"
    items.append(item(ship, L["ship"]))
    if key not in ("uk", "eu"):
        items.append(item("/how-to-use-hipobuy/", L["howto"]))
    items.extend(
        [
            item(f"/{s['help']}/", L["help"]),
            item(f"/{s['news']}/", L["news"]),
            item(f"/{s['about']}/", L["about"]),
        ]
    )
    return "<ul class=\"nl\">" + "".join(f"<li>{a}</li>" for a in items) + "</ul>"


def _catalog_block(key: str, d: dict) -> str:
    L = labels(key)
    pairs = GLOSS.get(key) or []
    placeholder = pairs[0][0] if pairs else "sneakers"
    lis = []
    for slug, name in SIDE_CATS:
        on = ' class="on"' if slug == "all" else ""
        cnt = "12,000+" if slug == "all" else "Live"
        lis.append(
            f'<li><a href="/?cat={escape(slug)}"{on} onclick="fc(\'{slug}\');return false;">'
            f"{escape(name)} <span class=\"cn\">{cnt}</span></a></li>"
        )
    mapping = {a.lower(): b for a, b in pairs}
    country = d.get("dest") or ""
    return f"""
<div class="mw" id="catalog">
  <aside class="sb">
    <div class="sbsec">
      <p class="sbtit">{escape(L["sheet"])}</p>
      <ul class="cl" id="clist">{"".join(lis)}</ul>
    </div>
  </aside>
  <main>
    <div class="fbar">
      <div class="sw">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.35-4.35"/></svg>
        <input type="search" class="si" id="search-input" name="q" placeholder="{escape(placeholder)}" oninput="hs(this.value)">
      </div>
      <select class="ss" id="sort-sel" onchange="lp()">
        <option value="d">Sort: Default</option>
        <option value="pa">Price: Low &rarr; High</option>
        <option value="pd">Price: High &rarr; Low</option>
      </select>
      <span class="rc" id="rc"><b>—</b></span>
    </div>
    <div class="pg" id="product-grid"></div>
  </main>
</div>
<script>
const DEMO=[];
const CATMAP={json.dumps(CATMAP)};
const PAPI='/api/products/';
const REG={json.dumps(REG)};
const SHEET='https://w2clinks.com/spreadsheet/hipobuy/';
const LOCALMAP={json.dumps(mapping, ensure_ascii=False)};
const COUNTRY={json.dumps(country)};
let cat='all',sq='';
function sk(n){{document.getElementById('product-grid').innerHTML=Array(n).fill(0).map(()=>'<div class="pcard sk"><div class="skim"></div><div class="pbdy"><div class="skl"></div><div class="skl sh"></div></div></div>').join('');}}
function rp(ps){{
  const t=(typeof T!=='undefined')?(T[aL]||T.en):{{}};
  const buyBtn=t.buy||'Hipobuy →';const noP=t.no||'No products found.';
  const g=document.getElementById('product-grid');
  if(!ps.length){{g.innerHTML='<div style="grid-column:1/-1;text-align:center;padding:60px 20px;color:var(--g4);font-size:14px">'+noP+'</div>';return;}}
  const fp=p=>((typeof fmtPrice==='function')?fmtPrice(p.priceCny??p.price,p.currency||'CNY'):(p.price||''));
  g.innerHTML=ps.map(p=>`<article class="pcard">
    <div class="pimg">
      ${{p.img?`<img src="${{p.img}}" alt="${{p.name}}" loading="lazy" onerror="this.style.display='none';this.nextElementSibling.style.display='flex'"><div class="pph" style="display:none"></div>`:'<div class="pph"></div>'}}
      ${{p.badge?`<span class="pbg">${{p.badge}}</span>`:''}}
    </div>
    <div class="pbdy"><p class="pnm">${{p.name}}</p>
      <div class="pmeta"><span class="ppr">${{fp(p)}}</span><span class="ppl">${{p.platform||'W2C'}}</span></div>
    </div>
    <a href="${{p.target||SHEET}}" target="_blank" rel="noopener" class="plnk">${{buyBtn}}</a>
  </article>`).join('');
}}
function fc(c){{
  cat=c;
  document.querySelectorAll('.cl a').forEach(a=>a.classList.toggle('on', a.getAttribute('onclick')&&a.getAttribute('onclick').indexOf("'"+c+"'")>=0));
  if(history.replaceState) history.replaceState(null,'', c&&c!=='all' ? '/?cat='+encodeURIComponent(c) : '/');
  lp();
}}
let st;function hs(v){{
  clearTimeout(st);
  st=setTimeout(()=>{{
    var raw=(v||'').trim();
    sq=LOCALMAP[raw.toLowerCase()]||raw;
    lp();
  }},280);
}}
async function lp(skipSkeleton){{
  if(!skipSkeleton) sk(12);
  try{{
    const u=new URL(PAPI,location.origin);
    u.searchParams.set('limit','24');
    if(COUNTRY) u.searchParams.set('country', COUNTRY);
    if(sq) u.searchParams.set('keyword', sq);
    if(cat!=='all'&&CATMAP[cat]) u.searchParams.set('category', CATMAP[cat]);
    const r=await fetch(u);
    const d=await r.json();
    let ps=(d.items||[]).map((it,i)=>({{
      id:i+1,name:it.title||'',price:it.price||'',priceCny:parseFloat(it.price)||0,
      currency:(it.currency||'CNY').toUpperCase(),platform:it.brand||'W2C',cat:cat,
      img:it.image||'',badge:i<3?'TOP':'',target:it.target||it.source||SHEET
    }}));
    const sel=document.getElementById('sort-sel');
    const s=sel?sel.value:'d';
    if(s==='pa')ps.sort((a,b)=>(a.priceCny||0)-(b.priceCny||0));
    if(s==='pd')ps.sort((a,b)=>(b.priceCny||0)-(a.priceCny||0));
    document.getElementById('rc').innerHTML='<b>'+ps.length.toLocaleString()+'</b>';
    rp(ps);
  }}catch(e){{rp([]);}}
}}
document.addEventListener('DOMContentLoaded',function(){{
  var params=new URLSearchParams(location.search);
  var q0=params.get('q'); var c0=params.get('cat');
  if(q0){{ var inp=document.getElementById('search-input'); if(inp) inp.value=q0; sq=LOCALMAP[q0.toLowerCase()]||q0; }}
  if(c0){{ cat=c0; document.querySelectorAll('.cl a').forEach(a=>a.classList.toggle('on', a.getAttribute('onclick')&&a.getAttribute('onclick').indexOf("'"+c0+"'")>=0)); }}
  lp(true);
}});
</script>
"""


_CHEV = (
    '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">'
    '<polyline points="6 9 12 15 18 9"/></svg>'
)


def _band_copy(key: str) -> dict[str, str]:
    if key == "at":
        return {
            "faq_h": "Häufige Fragen",
            "faq_sub": "Dieselben fünfzehn Fragen wie auf der Hilfeseite, hier auf der Startseite mit der grünen CMS-Leiste.",
            "faq_more": "Alle 15 Fragen auf der Hilfeseite",
            "news_h": "Was wir geprüft haben",
            "news_sub": "Datierte Checks, kein Firmenblog. Volle Texte bleiben unter Neuigkeiten.",
            "news_more": "Alle Checks mit Datum",
            "lab_h": "Versandlabor · 29 Sep 2026",
            "lab_sub": "Öffentlicher Schätzer, Karton 1000 g / 35×25×10 cm, Ziel Austria. Snapshot, kein Checkout.",
            "lab_more": "Ganzer Versandguide und Rechner",
            "lab_foot": "Die USA/UK-Vorlagetabelle steht nur auf der Versandseite. Hier gilt die Labortabelle vom 29 Sep 2026.",
        }
    if key == "nl":
        return {
            "faq_h": "Veelgestelde vragen",
            "faq_sub": "Dezelfde vijftien vragen als op de hulppagina, hier op de homepage in de groene CMS-balk.",
            "faq_more": "Alle 15 vragen op de hulppagina",
            "news_h": "Wat we hebben nagemeten",
            "news_sub": "Gedateerde checks, geen bedrijfsblog. Volledige teksten staan onder Nieuws.",
            "news_more": "Alle checks met datum",
            "lab_h": "Verzendlab · 29 sep 2026",
            "lab_sub": "Publieke estimator, doos 1000 g / 35×25×10 cm, bestemming Netherlands. Snapshot, geen checkout.",
            "lab_more": "Volledige verzendgids en rekenmachine",
            "lab_foot": "De USA/UK-sjabloontabel staat alleen op de verzendpagina. Hier geldt de labtabel van 29 sep 2026.",
        }
    job = {
        "uk": (
            "Coupon-desk FAQ — same fifteen questions as /help/, in this green bar.",
            "Dated checks. Full write-ups stay on /news/.",
            "GB estimator snapshot on this coupon host so landed cost is not a surprise. Haul-log dollars also live on hipobuyspreadsheets.uk.",
        ),
        "eu": (
            "Coupon-desk FAQ — same fifteen questions as /help/, in this green bar.",
            "Dated checks. This TLD is not a destination code.",
            "Pick a member-state country in the official estimator. Spain-only line counts stay on hipobuy.es.",
        ),
        "us": (
            "Same fifteen questions as /help/, on this homepage in the green CMS bar.",
            "Dated checks. Full write-ups stay on /news/.",
            "Public estimator, carton 1000 g / 35×25×10 cm, destination United States. Snapshot, not checkout.",
        ),
        "ukhaul": (
            "Haul-log FAQ — same fifteen questions as /help/, in this green bar.",
            "Dated checks. This host is not a 301 onto .co.uk.",
            "Public estimator, carton 1000 g / 35×25×10 cm, destination United Kingdom. Snapshot, not checkout.",
        ),
    }[key]
    return {
        "faq_h": "FAQ",
        "faq_sub": job[0],
        "faq_more": "All 15 questions on the help page",
        "news_h": "What we checked",
        "news_sub": job[1],
        "news_more": "All dated checks",
        "lab_h": "Shipping lab · 29 Sep 2026",
        "lab_sub": job[2],
        "lab_more": "Full shipping guide and calculator",
        "lab_foot": "The USA/UK/AU/CA template grid lives on the shipping page. Use the 29 Sep 2026 table here.",
    }


def _help_news_articles(key: str, d: dict) -> tuple[str, str]:
    from hipobuy_trust_pages import (  # noqa: WPS433
        help_at,
        help_en,
        help_nl,
        news_at,
        news_en,
        news_nl,
    )

    if key == "at":
        return help_at(d)[2], news_at(d)[2]
    if key == "nl":
        return help_nl(d)[2], news_nl(d)[2]
    flavour = {"uk": "uk", "eu": "eu", "us": "us", "ukhaul": "haul"}[key]
    return help_en(d, flavour)[2], news_en(d, flavour)[2]


def _faq_items(article: str) -> list[tuple[str, str]]:
    pairs = re.findall(
        r'<h3 class="ph">(.*?)</h3>\s*<p class="pp">(.*?)</p>',
        article,
        flags=re.S,
    )
    out = []
    for q, a in pairs:
        q_txt = re.sub(r"<[^>]+>", "", q).strip()
        out.append((q_txt, a.strip()))
    return out


def _news_cards(article: str, limit: int = 5) -> list[tuple[str, str]]:
    pairs = re.findall(
        r'<h2 class="ph">(.*?)</h2>\s*(?:<figure[\s\S]*?</figure>\s*)?<p class="pp">(.*?)</p>',
        article,
        flags=re.S,
    )
    checks = []
    rest = []
    for h, p in pairs:
        h_txt = re.sub(r"<[^>]+>", "", h).strip()
        if re.search(r"^Check\s+\d+", h_txt, flags=re.I):
            checks.append((h_txt, p.strip()))
        else:
            rest.append((h_txt, p.strip()))
    return (checks or rest)[:limit]


def _customs_note(key: str, d: dict, ship: str) -> str:
    customs = d.get("customs") or ""
    ioss = d.get("ioss") or ""
    if key == "at":
        return (
            f'<p class="pp">Wer Abgaben zahlt, steht auf der Live-SKU '
            f"(tax free / prepaid / Empfänger). "
            f'<a href="{customs}">BMF Zoll</a>'
            + (f' · <a href="{ioss}">IOSS / Kommission</a>' if ioss else "")
            + " (Orientierung oft 150&nbsp;€). "
            "<strong>Keine Unterdeklaration.</strong> "
            f'<a href="{EST}">Schätzer mit Ziel Austria öffnen</a> · '
            f'<a href="{ship}">Versandguide</a>.</p>'
        )
    if key == "nl":
        return (
            f'<p class="pp">Invoer volgt de geboekte lijn. '
            f'<a href="{customs}">Belastingdienst Douane</a>'
            + (f' · <a href="{ioss}">IOSS</a>' if ioss else "")
            + ". <strong>Geen onderwaardering.</strong> "
            f'<a href="{EST}">Estimator met bestemming Netherlands</a> · '
            f'<a href="{ship}">Verzendgids</a>.</p>'
        )
    if key == "us":
        return (
            f'<p class="pp">US treatment follows the booked SKU. '
            f'<a href="{customs}">CBP duty overview</a>. '
            "This desk does not invent a de-minimis dollar figure. "
            "<strong>No under-declaration tips.</strong> "
            f'<a href="{EST}">Official estimator, destination United States</a> · '
            f'<a href="{ship}">Shipping guide</a>.</p>'
        )
    if key == "eu":
        return (
            f'<p class="pp">The estimator needs a member-state country code, not “EU”. '
            f'<a href="{ioss or customs}">European Commission VAT e-commerce / IOSS</a> '
            "(often discussed around €150 for certain distance sales). "
            "Spain-only freight copy stays on hipobuy.es. "
            "<strong>No declared-value coaching.</strong> "
            f'<a href="{EST}">Open the official estimator</a> · '
            f'<a href="{ship}">Shipping guide</a>.</p>'
        )
    return (
        f'<p class="pp">UK import VAT/duty follow the carrier SKU. '
        f'<a href="{customs}">GOV.UK goods sent from abroad</a>. '
        "<strong>No declared-value coaching.</strong> "
        f'<a href="{EST}">Official estimator, destination United Kingdom</a> · '
        f'<a href="{ship}">Shipping guide</a>.</p>'
    )


def _lab_home(key: str, d: dict, foot: str) -> str:
    from hipobuy_desk_copy import SHIP_H1, lab_block

    code = d.get("dest")
    if not code:
        return f"""
<aside class="cb info hipo-lab-note" id="estimator-lab" style="display:block">
  <div>
    <strong>Official HipoBuy estimator · 29 Sep 2026</strong>
    The .eu TLD is not a destination. Pick ES, IE, IT… in-app. IOSS is a SKU you read the morning you book.
    Spain-only line counts stay on hipobuy.es. <strong>No declared-value coaching.</strong>
  </div>
</aside>
<p class="pp">{escape(foot)}</p>
"""
    if key in SHIP_H1:
        intro = SHIP_H1[key][4]
        dest_label = SHIP_H1[key][3]
        lab_code = SHIP_H1[key][2]
    else:
        lab_code = code
        dest_label = d.get("dest_label") or code
        intro = (
            "Cheapest carriable on the lab day: HIPO-RoyalMail-GB-1 about $23.83. "
            "This .co.uk host still ranks coupons; the table is here so landed cost is not a surprise."
        )
    lab = lab_block(lab_code, dest_label, intro)
    lab = re.sub(
        r'<p class="pp">The generic USA/UK/AU/CA.*?</p>\s*',
        f'<p class="pp">{foot}</p>\n',
        lab,
        count=1,
        flags=re.S,
    )
    return lab


def _trust_band(key: str, d: dict) -> str:
    L = labels(key)
    C = _band_copy(key)
    s = d["slugs"]
    ship = "/guides/shipping/" if key == "us" else "/hipobuy-shipping-guide/"
    help_html, news_html = _help_news_articles(key, d)
    faqs = _faq_items(help_html)
    if len(faqs) < 15:
        raise RuntimeError(f"{key}: homepage FAQ parsed {len(faqs)} questions, need 15")
    news = _news_cards(news_html)
    faq_blocks = []
    for i, (q, a) in enumerate(faqs):
        opened = " open" if i == 0 else ""
        faq_blocks.append(
            f'<div class="faq-item{opened}">'
            f'<div class="faq-q" onclick="toggleFaq(this)">{escape(q)}{_CHEV}</div>'
            f'<div class="faq-a">{a}</div></div>'
        )
    news_blocks = []
    for h, p in news:
        news_blocks.append(f'<article class="ncard"><h3>{escape(h)}</h3><p>{p}</p></article>')
    lab = _lab_home(key, d, C["lab_foot"])
    customs = _customs_note(key, d, ship)
    return f"""
<div id="home-trust">
  <section class="sec" id="faq" style="padding-top:28px">
    <h2 class="stit">{escape(C["faq_h"])}</h2>
    <p class="ssub">{escape(C["faq_sub"]).strip()}</p>
    {"".join(faq_blocks)}
    <p class="home-more"><a href="/{s["help"]}/">{escape(C["faq_more"])} →</a></p>
  </section>
  <section class="sec" id="news" style="padding-top:12px">
    <h2 class="stit">{escape(C["news_h"])}</h2>
    <p class="ssub">{escape(C["news_sub"])}</p>
    {"".join(news_blocks)}
    <p class="home-more"><a href="/{s["news"]}/">{escape(C["news_more"])} →</a></p>
  </section>
  <section class="sec" id="lab" style="padding-top:12px">
    <h2 class="stit">{escape(C["lab_h"])}</h2>
    <p class="ssub">{escape(C["lab_sub"])}</p>
    {lab}
    {customs}
    <p class="home-more"><a href="{ship}">{escape(C["lab_more"])} →</a>
      · <a href="{EST}">{escape(L["est"])} →</a></p>
  </section>
</div>
"""


def _rewrite_ccards(html: str) -> str:
    def repl(m: re.Match) -> str:
        href = m.group(1)
        cat = ""
        qm = re.search(r"category=([^&]+)", href)
        if qm:
            cat = re.sub(r"\+", " ", qm.group(1)).upper()
        slug = W2C_TO_FC.get(cat)
        if not slug:
            return m.group(0)
        return (
            f'<a href="/?cat={slug}" class="ccard" onclick="fc(\'{slug}\');return false;"'
        )

    return re.sub(
        r'<a href="(https://w2clinks\.com/spreadsheet/\?category=[^"]+)" class="ccard"[^>]*',
        repl,
        html,
    )


def _drop_sheet_cta(html: str) -> str:
    html = re.sub(
        r'<a href="/hipobuy-spreadsheet/?" class="cp">[^<]*</a>\s*',
        "",
        html,
        count=1,
    )
    html = html.replace('href="/hipobuy-spreadsheet"', 'href="/"')
    html = html.replace('href="/hipobuy-spreadsheet/"', 'href="/"')
    return html


INNER_CSS = """
.w2c-prose h1{font-size:clamp(28px,4.4vw,42px);font-weight:700;letter-spacing:-1.2px;line-height:1.15;margin:0 0 18px;color:var(--bk)}
.w2c-prose .faq-item.open .faq-a{max-height:1600px}
figure.shot{margin:16px 0}
figure.shot img{width:100%;height:auto;border:1px solid var(--g5);border-radius:var(--rl);background:var(--g6)}
figure.shot figcaption{font-size:13px;color:var(--g4);margin-top:6px;line-height:1.55}
"""


def _unwrap_article(inner: str) -> str:
    inner = inner.strip()
    inner = re.sub(r'^<article class="hipo-howto"[^>]*>\s*', "", inner)
    inner = re.sub(r"\s*</article>\s*$", "", inner)
    inner = re.sub(r'<h1 style="[^"]*">', "<h1>", inner, count=1)
    return inner


def _help_as_accordion(inner: str) -> str:
    n = 0

    def repl(m: re.Match) -> str:
        nonlocal n
        q = re.sub(r"<[^>]+>", "", m.group(1)).strip()
        a = m.group(2).strip()
        opened = " open" if n == 0 else ""
        n += 1
        return (
            f'<div class="faq-item{opened}">'
            f'<div class="faq-q" onclick="toggleFaq(this)">{escape(q)}{_CHEV}</div>'
            f'<div class="faq-a">{a}</div></div>'
        )

    return re.sub(
        r'<h3 class="ph">(.*?)</h3>\s*<p class="pp">(.*?)</p>',
        repl,
        inner,
        flags=re.S,
    )


def _set_meta(html: str, *, title: str, desc: str, canonical: str, lang: str) -> str:
    html = re.sub(r'<html lang="[^"]*"', f'<html lang="{escape(lang)}"', html, count=1)
    html = re.sub(
        r"<title>.*?</title>",
        f"<title>{escape(title)}</title>",
        html,
        count=1,
        flags=re.S,
    )
    html = re.sub(
        r'<meta name="description" content="[^"]*"',
        f'<meta name="description" content="{escape(desc)}"',
        html,
        count=1,
    )
    html = re.sub(
        r'<meta property="og:title" content="[^"]*"',
        f'<meta property="og:title" content="{escape(title)}"',
        html,
        count=1,
    )
    html = re.sub(
        r'<meta property="og:description" content="[^"]*"',
        f'<meta property="og:description" content="{escape(desc)}"',
        html,
        count=1,
    )
    html = re.sub(
        r'<meta property="og:url" content="[^"]*"',
        f'<meta property="og:url" content="{escape(canonical)}"',
        html,
        count=1,
    )
    html = re.sub(
        r'<link rel="canonical" href="[^"]*"',
        f'<link rel="canonical" href="{escape(canonical)}"',
        html,
        count=1,
    )
    jsonld = json.dumps(
        {
            "@context": "https://schema.org",
            "@type": "WebPage",
            "name": title,
            "url": canonical,
            "description": desc,
        },
        ensure_ascii=False,
    )
    html = re.sub(
        r'<script type="application/ld\+json">.*?</script>',
        f'<script type="application/ld+json">{jsonld}</script>',
        html,
        count=1,
        flags=re.S,
    )
    return html


def build_cms_inner(
    key: str,
    d: dict,
    *,
    title: str,
    desc: str,
    canonical: str,
    crumb: str,
    inner: str,
    on: str,
    as_faq: bool = False,
) -> str:
    """Same green CMS chrome as the homepage, article in the middle."""
    src = CMS_HOME / f"{key}.html"
    if not src.is_file():
        raise FileNotFoundError(src)
    html = src.read_text(encoding="utf-8", errors="replace")
    html = _set_meta(html, title=title, desc=desc, canonical=canonical, lang=d["lang"])
    html = html.replace("</style>", INNER_CSS + "\n</style>", 1)
    html = re.sub(r'<ul class="nl">.*?</ul>', _nav(key, d, on=on), html, count=1, flags=re.S)
    start = html.find('<section class="hero')
    if start < 0:
        start = html.find('<article class="w2c-prose')
    end = html.find("<footer")
    if start < 0 or end < 0:
        raise ValueError(f"{key}: cannot splice CMS inner chrome")
    body = _unwrap_article(inner)
    if as_faq:
        body = _help_as_accordion(body)
    L = labels(key)
    block = (
        f'<div class="bc"><a href="/">{escape(L["home"])}</a>'
        f" <span>/</span> <span>{escape(crumb)}</span></div>\n"
        f'<article class="w2c-prose" style="padding-bottom:72px">\n'
        f"{body}\n"
        f'<p class="pp">Editorial: <a href="mailto:{MAIL}">{MAIL}</a></p>\n'
        f"</article>\n"
    )
    html = html[:start] + block + html[end:]
    html = re.sub(
        r'(<div class="fb">)',
        rf'\1<p>Editorial: <a href="mailto:{MAIL}">{MAIL}</a></p>',
        html,
        count=1,
    )
    html = html.replace("Cruisezhang0202@gmail.com", MAIL)
    return html


def build_cms_home(key: str, d: dict) -> str:
    src = CMS_HOME / f"{key}.html"
    if not src.is_file():
        raise FileNotFoundError(src)
    html = src.read_text(encoding="utf-8", errors="replace")
    html = html.replace("</style>", CAT_CSS + "\n</style>", 1)
    html = re.sub(r'<ul class="nl">.*?</ul>', _nav(key, d), html, count=1, flags=re.S)
    html = _drop_sheet_cta(html)
    html = _rewrite_ccards(html)
    block = _catalog_block(key, d)
    band = _trust_band(key, d)
    needle = '<article class="w2c-prose'
    idx = html.find(needle)
    if idx >= 0:
        html = html[:idx] + block + band + html[idx:]
    elif 'id="catalog"' not in html:
        html = html.replace("</section>", "</section>\n" + block + band, 1)
    # editorial inbox in footer copyright strip
    html = re.sub(
        r'(<div class="fb">)',
        rf'\1<p>Editorial: <a href="mailto:{MAIL}">{MAIL}</a></p>',
        html,
        count=1,
    )
    html = html.replace("Cruisezhang0202@gmail.com", MAIL)
    return html
