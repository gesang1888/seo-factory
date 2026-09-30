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

from hipobuy_trust_chrome import GLOSS, MAIL, labels  # noqa: E402

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


def _nav(key: str, d: dict) -> str:
    L = labels(key)
    s = d["slugs"]
    items = [('<a href="/" class="on">' + escape(L["sheet"]) + "</a>")]
    if key in ("uk", "eu"):
        items.append(f'<a href="/hipobuy-coupons/">{escape(L["coupons"])}</a>')
    if key == "uk":
        items.append('<a href="/blog/posts/hipobuy-sizing-guide/">UK sizing</a>')
    ship = "/guides/shipping/" if key == "us" else "/hipobuy-shipping-guide/"
    items.append(f'<a href="{ship}">{escape(L["ship"])}</a>')
    if key not in ("uk", "eu"):
        items.append(f'<a href="/how-to-use-hipobuy/">{escape(L["howto"])}</a>')
    items.extend(
        [
            f'<a href="/{s["help"]}/">{escape(L["help"])}</a>',
            f'<a href="/{s["news"]}/">{escape(L["news"])}</a>',
            f'<a href="/{s["about"]}/">{escape(L["about"])}</a>',
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
    html = re.sub(
        r"(</section>\s*)(<article class=\"w2c-prose)",
        r"\1" + block + r"\2",
        html,
        count=1,
    )
    if 'id="catalog"' not in html:
        html = re.sub(
            r"(</section>)",
            r"\1\n" + block,
            html,
            count=1,
        )
    # editorial inbox in footer copyright strip
    html = re.sub(
        r'(<div class="fb">)',
        rf'\1<p>Editorial: <a href="mailto:{MAIL}">{MAIL}</a></p>',
        html,
        count=1,
    )
    html = html.replace("Cruisezhang0202@gmail.com", MAIL)
    return html
