#!/usr/bin/env python3
"""Build HubBuy platform-opt overlay from LIVE EyouCMS homepage (surgical).

Does not overwrite the ranked CMS homepage with a Georgia dest skin.
Archives count on Baota ≈ 10,024 → public Independent Index · 10,000+.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "sites" / "hubbuy.net" / "overlay"
LIVE = ROOT / "live-base" / "index.htm"
COUPONS_LIVE = ROOT / "live-base" / "coupons.html"
HOST = "hubbuy.net"
BRAND = "HubBuy"
OPT = "hubbuy-platform-20261026"
DATE = "2026-10-26"
DATE_HUMAN = "26 Oct 2026"
ROWS = "10,000+"
ROWS_N = 10024
OFFICIAL = "https://www.hubbuy.com/"
CATALOG = "https://w2clinks.com/spreadsheet/hubbuycn/"


def patch_home(src: str) -> str:
    local_css = """
.sg-sec#local{max-width:1100px;margin:8px auto 28px;padding:0 24px;text-align:left}
.sg-sec#local h2{font-size:20px;margin:0 0 6px}
.sg-sec#local .ssub{margin-bottom:12px;color:var(--text-secondary,#555)}
.local-steps{margin:0;padding-left:18px}
.local-steps li{margin:0 0 10px;color:var(--text-secondary,#555)}
.local-steps li strong{display:block;color:var(--text-primary,#0A0A0A);font-size:14px}
.local-steps li span{display:block;font-size:13.5px}
.local-src{font-size:13px;color:#888;margin-top:10px}
#local{scroll-margin-top:80px}
.btn-group .btn{margin:4px}
"""
    if ".sg-sec#local" not in src:
        src = src.replace("</style>", local_css + "\n</style>", 1)

    repls = [
        (
            "<title>HubBuy Spreadsheet 2026 — QC Finds &amp; Shipping</title>",
            f"<title>HubBuy Spreadsheet 2026 — Independent Index · {ROWS}</title>",
        ),
        (
            'content="HubBuy spreadsheet: live Weidian, Taobao and 1688 QC finds. Not Excel, not a Google Sheet. Official 8 Oct 2026: ¥3600 new-user shipping pack on hubbuy.com. Independent desk."',
            f'content="HubBuy Independent Index · {ROWS} on {HOST}. Not Excel, not a Google Sheet, not checkout. Coupons on /hubbuy-coupons/; dataset on /finds-dataset/. Brand hub only — twin hubbuyspreadsheet.net already 301. Pay on hubbuy.com."',
        ),
        (
            '<meta property="og:title" content="HubBuy Spreadsheet 2026 — QC Finds &amp; Shipping">',
            f'<meta property="og:title" content="HubBuy Spreadsheet 2026 — Independent Index · {ROWS}">',
        ),
        (
            'content="HubBuy spreadsheet: live finds, not Excel, not a Google Sheet. ¥3600 new-user shipping pack measured on hubbuy.com 8 Oct 2026."',
            f'content="HubBuy Independent Index · {ROWS}. Coupons + finds dataset on this hub. Brand hub only (no country desks). Twin hubbuyspreadsheet.net 301 stays."',
        ),
        (
            '"name": "HubBuy Spreadsheet"',
            f'"name": "HubBuy Independent Index",\n      "alternateName": ["HubBuy Spreadsheet 2026", "{HOST}"],\n      "dateModified": "{DATE}"',
        ),
        (
            '"description": "The ultimate guide to buying from China through HubBuy purchasing agent"',
            f'"description": "HubBuy Independent Index · {ROWS} finds. Coupons on /hubbuy-coupons/; dataset on /finds-dataset/. Not Excel, not a Google Sheet. Brand hub only — no country desks."',
        ),
    ]
    for old, new in repls:
        if old not in src:
            raise SystemExit(f"missing replace anchor:\n{old[:180]}")
        src = src.replace(old, new, 1)

    # FAQ JSON-LD: point coupons to money URL; add hub-only Q
    src = src.replace(
        "Ladder and screenshots live on /coupons.html. This homepage does not print an invite token.",
        "Ladder and screenshots live on /hubbuy-coupons/ (thin /coupons.html 301s there). This homepage does not print an invite token.",
    )
    if "Is hubbuy.net a country desk?" not in src:
        faq_extra = (
            '{"@type":"Question","name":"Is hubbuy.net a country desk?",'
            '"acceptedAnswer":{"@type":"Answer","text":"No. hubbuy.net is the HubBuy brand hub only. There are no keep country spreadsheet desks. Twin hubbuyspreadsheet.net already 301s here — do not revive it."}},'
            '{"@type":"Question","name":"Where do HubBuy coupon queries land?",'
            '"acceptedAnswer":{"@type":"Answer","text":"On https://hubbuy.net/hubbuy-coupons/. Thin /coupons.html redirects there. Dataset moat lives on /finds-dataset/."}},'
        )
        src = src.replace(
            '{"@type":"FAQPage","mainEntity":[',
            '{"@type":"FAQPage","mainEntity":[' + faq_extra,
            1,
        )

    old_nav = """<ul class="nav-menu" id="navMenu">
                    <li><a href="/" class="nav-item active">Home</a></li>
                    <li><a href="#how-it-works" class="nav-item">How to Buy</a></li>
                    <li><a href="/coupons.html" class="nav-item">Coupons</a></li>
                    <li><a href="#guides" class="nav-item">Guides</a></li>
                    <li><a href="#faq" class="nav-item">FAQ</a></li>
                    <li>
                        <!-- FIX #2: rel="noopener noreferrer" added -->
                        <a href="https://www.hubbuy.com/" target="_blank" rel="noopener noreferrer" class="nav-item nav-cta">
                            <i class="fas fa-shopping-bag"></i> Buy on HubBuy.com
                        </a>
                    </li>
                </ul>"""
    new_nav = f"""<ul class="nav-menu" id="navMenu">
                    <li><a href="/" class="nav-item active">Home</a></li>
                    <li><a href="#local" class="nav-item">Hub</a></li>
                    <li><a href="/hubbuy-coupons/" class="nav-item">Coupons</a></li>
                    <li><a href="/finds-dataset/" class="nav-item">Dataset</a></li>
                    <li><a href="#how-it-works" class="nav-item">How to Buy</a></li>
                    <li><a href="#faq" class="nav-item">FAQ</a></li>
                    <li>
                        <a href="{OFFICIAL}" target="_blank" rel="noopener noreferrer" class="nav-item nav-cta">
                            <i class="fas fa-shopping-bag"></i> Buy on HubBuy.com
                        </a>
                    </li>
                </ul>"""
    if old_nav not in src:
        raise SystemExit("nav block missing")
    src = src.replace(old_nav, new_nav)

    old_hero = """<section class="hero">
            <div class="container hero-content">
                <span class="hero-tag">LIVE FINDS · NOT EXCEL · NOT A GOOGLE SHEET</span>
                <h1>The Complete <em>HubBuy Spreadsheet</em> 2026</h1>
                <p>Live Weidian, Taobao and 1688 QC finds with Buy links on HubBuy. Not Excel, not a Google Sheet, not checkout. Rehearse freight here, then pay on hubbuy.com. Official new-user pack measured 8 Oct 2026: ¥3600 shipping coupons after register — this homepage does not print an invite token.</p>
                <div class="btn-group">
                    <a href="https://w2clinks.com/spreadsheet/hubbuycn/?page=1&sort=newest&typeid=7&category=SNEAKERS&utm_source=hubbuy&utm_medium=aggregator&utm_campaign=hubbuy&utm_content=cat-shoes381" target="_blank" rel="noopener noreferrer" class="btn btn-primary">
                        <i class="fas fa-shopping-bag"></i> HUBBUY SPREADSHEET 2026
                    </a>
                    <a href="#how-it-works" class="btn btn-outline">
                        <i class="fas fa-book-open"></i> Read the Guide
                    </a>
                </div>"""
    new_hero = f"""<section class="hero">
            <div class="container hero-content">
                <span class="hero-tag">Independent Index · {ROWS} · not Excel · not a dest-country skin</span>
                <h1>HubBuy Spreadsheet <em>2026</em> — Independent Index · {ROWS}</h1>
                <p>Independent Index · {ROWS} — live Weidian, Taobao and 1688 QC finds with Buy links. Not Excel, not a Google Sheet, not checkout. Brand hub on this .net host (no country spreadsheet desks; twin hubbuyspreadsheet.net already 301s here). Coupons + dataset cited below; pay on hubbuy.com. Official new-user pack measured 8 Oct 2026: <strong>¥3600 shipping coupons</strong> after register — this homepage does not print an invite token. Hub stamp {DATE_HUMAN}.</p>
                <div class="btn-group">
                    <a href="{CATALOG}" target="_blank" rel="noopener noreferrer" class="btn btn-primary">
                        <i class="fas fa-shopping-bag"></i> Spreadsheet
                    </a>
                    <a href="/hubbuy-coupons/" class="btn btn-outline">
                        <i class="fas fa-ticket-alt"></i> Coupons
                    </a>
                    <a href="/finds-dataset/" class="btn btn-outline">
                        <i class="fas fa-database"></i> Dataset
                    </a>
                    <a href="{OFFICIAL}" target="_blank" rel="noopener noreferrer" class="btn btn-outline">
                        <i class="fas fa-user-plus"></i> Register
                    </a>
                </div>"""
    if old_hero not in src:
        raise SystemExit("hero block missing")
    src = src.replace(old_hero, new_hero)

    local_block = f"""
<section class="sg-sec" id="local">
  <h2>Brand hub · Independent Index · no country desk</h2>
  <p class="ssub">{HOST} · not a customs territory · money URLs ≤6</p>
  <ol class="local-steps">
    <li><strong>Brand spreadsheet → this hub</strong><span>Independent Index · {ROWS} (CMS archives ≈ {ROWS_N:,}). Coupons + dataset live here.</span></li>
    <li><strong>No keep country desks</strong><span>Portfolio inventory + GSC list zero HubBuy country spreadsheet TLDs. Do not invent new ones.</span></li>
    <li><strong>Twin stays 301</strong><span>hubbuyspreadsheet.net already whole-site 301 → hubbuy.net — not a Phase C sunset to revive, and not a second hub.</span></li>
    <li><strong>Money URLs stay ≤6</strong><span>Home · Coupons · Dataset · How-to · FAQ · Official register. Category inners stay 200 — not overwritten by Georgia dest skins.</span></li>
  </ol>
  <p class="local-src">Money URLs (≤6): <a href="/">Home</a> · <a href="/hubbuy-coupons/">Coupons</a> · <a href="/finds-dataset/">Dataset</a> · <a href="#how-it-works">How to Buy</a> · <a href="#faq">FAQ</a> · <a href="{OFFICIAL}" rel="noopener">Register</a></p>
  <p class="local-src">Lab {DATE_HUMAN}. Phase A twin 301 not reversed. Orders stay on hubbuy.com.</p>
</section>
"""
    m = re.search(r'(<section class="hero">[\s\S]*?</section>)', src)
    if not m:
        raise SystemExit("hero section wrapper missing")
    if 'id="local"' not in src:
        src = src[: m.end()] + "\n" + local_block + src[m.end() :]

    # Point remaining /coupons.html body links to money URL (keep asset paths)
    src = src.replace('href="/coupons.html"', 'href="/hubbuy-coupons/"')
    src = src.replace(">/coupons.html<", ">/hubbuy-coupons/<")

    if f"Independent Index · {ROWS}" not in src:
        raise SystemExit("Independent Index missing")
    if 'id="local"' not in src:
        raise SystemExit("#local missing")
    if 'href="/coupons.html"' in src:
        raise SystemExit("coupons.html href still present")
    return src


def build_coupons(src: str) -> str:
    """Deepen coupons into /hubbuy-coupons/ money URL."""
    src = src.replace(
        '<link rel="canonical" href="https://hubbuy.net/coupons.html">',
        '<link rel="canonical" href="https://hubbuy.net/hubbuy-coupons/">',
    )
    src = src.replace(
        '<meta property="og:url" content="https://hubbuy.net/coupons.html">',
        '<meta property="og:url" content="https://hubbuy.net/hubbuy-coupons/">',
    )
    src = src.replace(
        "<title>HubBuy Coupons 2026 — ¥3600 New User Shipping Pack</title>",
        f"<title>HubBuy Coupons 2026 — ¥3600 Pack · Updated {DATE_HUMAN}</title>",
    )
    src = src.replace(
        'content="Official HubBuy coupons measured on hubbuy.com 8 Oct 2026: ¥3600 new-user shipping pack (36 coupons, 60 days), 20% tutorial coupon, 300-day storage. No public promo code. Screenshots included."',
        f'content="Working HubBuy coupon facts for 2026 (updated {DATE_HUMAN}). Official ¥3600 new-user shipping pack · 20% tutorial coupon · 300-day storage — confirm_live. Truth JSON at /data/coupons-truth.json."',
    )
    if 'name="coupons-truth"' not in src:
        src = src.replace(
            "<head>",
            '<head>\n<meta name="coupons-truth" content="/data/coupons-truth.json">',
            1,
        )
    faq_ld = (
        '<script type="application/ld+json">'
        '{"@context":"https://schema.org","@type":"FAQPage","mainEntity":['
        '{"@type":"Question","name":"What is the HubBuy ¥3600 new-user shipping pack?","acceptedAnswer":{"@type":"Answer","text":"Official hubbuy.com sign-up (measured 8 Oct 2026) credits a ¥3600-class shipping coupon pack (36 coupons, 60 days, ladder ¥20–¥300) after register. Status confirm_live — re-check Coupon centre the morning you pay. No public typed-in promo code on this desk. Truth JSON: /data/coupons-truth.json."}},'
        '{"@type":"Question","name":"Where should HubBuy coupon queries land?","acceptedAnswer":{"@type":"Answer","text":"On hubbuy.net/hubbuy-coupons/. Thin /coupons.html redirects here. Brand hub only — twin hubbuyspreadsheet.net already 301s to the hub."}},'
        '{"@type":"Question","name":"Can I stack HubBuy shipping coupons?","acceptedAnswer":{"@type":"Answer","text":"Usually one shipping coupon per parcel payment; line-specific coupons may not stack with every other discount. Always confirm_live in-app. Tutorial 20% and Discord/point tasks are separate from the register pack."}}'
        "]}"
        "</script>"
    )
    if "HubBuy ¥3600 new-user shipping pack" not in src:
        src = src.replace("</head>", faq_ld + "\n</head>", 1)

    # nav on
    src = src.replace(
        '<a class="on" href="/coupons.html">Coupons</a>',
        '<a class="on" href="/hubbuy-coupons/">Coupons</a>',
    )
    src = src.replace('href="/coupons.html"', 'href="/hubbuy-coupons/"')
    src = src.replace(
        '<a href="https://w2clinks.com/spreadsheet/hubbuycn/" target="_blank" rel="noopener">Finds</a>',
        '<a href="/finds-dataset/">Dataset</a>\n    <a href="https://w2clinks.com/spreadsheet/hubbuycn/" target="_blank" rel="noopener">Finds</a>',
    )

    callout = f"""
  <div class="truth-callout" style="background:#FFF7F0;border:1px solid #ffd8bf;border-radius:12px;padding:14px 16px;margin:16px 0">
    <strong>Coupons truth · {DATE_HUMAN}</strong>
    <p>Primary official line <strong>¥3600 new-user shipping pack</strong> (36 coupons / 60 days / ladder ¥20–¥300) status <strong>confirm_live</strong> after register on hubbuy.com. Also measured 8 Oct 2026: <strong>20% tutorial shipping coupon</strong> + Help <strong>300-day</strong> free storage — confirm in-app the morning you pay. Machine-readable: <a href="/data/coupons-truth.json">/data/coupons-truth.json</a>. Finds moat: <a href="/finds-dataset/">/finds-dataset/</a>. Thin <code>/coupons.html</code> 301 → this page. Brand hub only — twin hubbuyspreadsheet.net stays 301. No public typed-in promo code invented on this desk.</p>
  </div>
"""
    lead = '<p class="ssub">Measured on the English SPA at <a href="https://www.hubbuy.com/" rel="noopener">hubbuy.com</a> on 8 Oct 2026. Offers credit in the account coupon centre. This page does not print an invite token. Third-party typed-in lists are not official.</p>'
    if f"Coupons truth · {DATE_HUMAN}" not in src:
        if lead not in src:
            raise SystemExit("coupons lead missing")
        src = src.replace(lead, lead + "\n" + callout, 1)

    src = src.replace(
        "Copy reviewed 8 Oct 2026.",
        f"Copy reviewed 8 Oct 2026; hub stamp {DATE_HUMAN}.",
    )
    return src


def write_dataset_html() -> str:
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>HubBuy Finds Dataset — Independent Index · {ROWS}</title>
<meta name="description" content="Public HubBuy finds dataset on {HOST}: row_count {ROWS_N:,} (display {ROWS}). Category proofs + coupons truth. Not another opaque Google Sheet.">
<link rel="canonical" href="https://{HOST}/finds-dataset/">
<meta name="coupons-truth" content="/data/coupons-truth.json">
<script type="application/ld+json">
{{"@context":"https://schema.org","@type":"Dataset","name":"HubBuy Independent Index","description":"Public, citable HubBuy finds row counts and category proofs.","url":"https://{HOST}/finds-dataset/","creator":{{"@type":"Organization","name":"HubBuy Guide"}},"dateModified":"{DATE}","variableMeasured":"QC finds / spreadsheet rows","measurementTechnique":"CMS ey_archives count + live catalog category proofs"}}
</script>
<style>
:root{{--p:#FF6900;--bk:#262626;--g:#8C8C8C;--bd:#eee;--f:Nunito,system-ui,sans-serif}}
body{{font-family:var(--f);background:#F0F2F5;color:var(--bk);line-height:1.7;margin:0}}
a{{color:var(--p)}}
.top{{background:linear-gradient(90deg,#FF8A3D,#FF6900);color:#fff;text-align:center;padding:10px 16px;font-weight:700}}
header,main,footer{{max-width:960px;margin:0 auto;padding:20px}}
header{{display:flex;gap:14px;flex-wrap:wrap;background:#fff;border-bottom:1px solid var(--bd)}}
header a{{text-decoration:none;color:#555;font-weight:600}}
.card{{background:#fff;border:1px solid var(--bd);border-radius:14px;padding:16px;margin:14px 0}}
.grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:12px}}
.stat b{{display:block;font-size:22px}}
.stat span{{font-size:13px;color:var(--g)}}
footer{{color:#ccc;background:#1A1A1A;max-width:none;padding:28px 20px;font-size:13px}}
footer a{{color:#fff}}
</style>
</head>
<body>
<div class="top">Independent Index · {ROWS} · hub stamp {DATE_HUMAN}</div>
<header>
  <a href="/">Home</a>
  <a href="/hubbuy-coupons/">Coupons</a>
  <a href="/finds-dataset/">Dataset</a>
  <a href="{CATALOG}" rel="noopener">Live catalog</a>
  <a href="{OFFICIAL}" rel="noopener">HubBuy.com</a>
</header>
<main>
  <h1>HubBuy finds dataset</h1>
  <p>Public, citable row counts for the HubBuy Independent Index on <strong>{HOST}</strong>. Not Excel, not a Google Sheet dump, not checkout. Coupon intent stays on <a href="/hubbuy-coupons/">/hubbuy-coupons/</a>.</p>
  <div class="grid">
    <div class="card stat"><b>{ROWS}</b><span>row_count_display</span></div>
    <div class="card stat"><b>{ROWS_N:,}</b><span>CMS archives stamp</span></div>
    <div class="card stat"><b>weekly</b><span>dataset review cadence</span></div>
    <div class="card stat"><b>hub-only</b><span>no country spreadsheet desks</span></div>
  </div>
  <div class="card">
    <h2>Machine-readable</h2>
    <ul>
      <li><a href="/data/finds-dataset.json">/data/finds-dataset.json</a></li>
      <li><a href="/data/coupons-truth.json">/data/coupons-truth.json</a></li>
    </ul>
    <p><code>platform_opt={OPT}</code> · <code>last_verified={DATE}</code></p>
  </div>
  <div class="card">
    <h2>Category proofs</h2>
    <ul>
      <li><a href="{CATALOG}?page=1&amp;sort=newest&amp;typeid=7&amp;category=SNEAKERS" rel="noopener">Sneakers</a></li>
      <li><a href="{CATALOG}?page=1&amp;sort=newest&amp;typeid=8&amp;category=JACKET" rel="noopener">Jackets</a></li>
      <li><a href="{CATALOG}?page=1&amp;sort=newest&amp;typeid=2&amp;category=T-SHIRT" rel="noopener">T-Shirts</a></li>
      <li><a href="{CATALOG}?page=1&amp;sort=newest&amp;typeid=1&amp;category=HOODIE" rel="noopener">Hoodies</a></li>
    </ul>
  </div>
  <div class="card">
    <h2>Hub-only note</h2>
    <p>{HOST} is the brand hub. Twin <code>hubbuyspreadsheet.net</code> already 301s here — do not revive. No keep country spreadsheet TLDs. Orders stay on hubbuy.com.</p>
  </div>
</main>
<footer>Independent desk on {HOST} — not checkout. Lab {DATE_HUMAN}.</footer>
</body>
</html>
"""


def write_jsons() -> None:
    data = ROOT / "hb-data"
    data.mkdir(parents=True, exist_ok=True)
    truth = {
        "brand": BRAND,
        "host": HOST,
        "last_verified": DATE,
        "platform_opt": OPT,
        "verify_on": "hubbuy.com Coupon centre / register / Wallet — confirm before pay",
        "update_cadence": "Coupons page copy + JSON stamped when official pack artwork changes (target weekly)",
        "serp_note": "28d clicks all on / (7). Head query hubbuy spreadsheet=2. /hubbuy-coupons/ was 404 pre-opt; /coupons.html had impressions only. Brand hub only — twin already 301.",
        "offers": [
            {
                "id": "hubbuy-3600-new-user-pack",
                "type": "new_user_shipping_pack",
                "label": "¥3600 new-user shipping coupon pack",
                "code": None,
                "value_claim": "Official hubbuy.com sign-up 8 Oct 2026: New user exclusive · ¥3600 shipping coupon pack (36 coupons, 60 days, ladder ¥20–¥300, includes no-min ¥20) — confirm_live in Coupon centre after register",
                "status": "confirm_live",
                "expires_on": None,
                "expires_note": "Pack validity 60 days from issue on official modal — re-confirm in-app",
                "applies_to": "HubBuy register → Coupon centre; one coupon per parcel payment",
                "exclusions": [
                    "This hub is not checkout",
                    "No public typed-in promo code on this desk",
                    "Line-specific coupons may not stack",
                ],
                "source": f"https://{HOST}/hubbuy-coupons/",
                "last_verified": DATE,
            },
            {
                "id": "hubbuy-20pct-tutorial",
                "type": "shipping_promo",
                "label": "20% off shipping tutorial coupon",
                "code": None,
                "value_claim": "Official Newbie Tasks 8 Oct 2026: complete ordering tutorial → 20% off shipping coupon — confirm_live",
                "status": "confirm_live",
                "expires_on": None,
                "source": OFFICIAL,
                "last_verified": DATE,
            },
            {
                "id": "hubbuy-300-day-storage",
                "type": "storage_policy",
                "label": "300 days free storage",
                "code": None,
                "value_claim": "Official homepage how-to 8 Oct 2026: free QC images + 300 days free storage — confirm Help the morning you ship",
                "status": "confirm_live",
                "expires_on": None,
                "source": OFFICIAL,
                "last_verified": DATE,
            },
        ],
    }
    finds = {
        "schema": "seo-factory.finds-dataset.v1",
        "brand": BRAND,
        "host": HOST,
        "last_verified": DATE,
        "generated_at": "2026-10-26T22:20:00Z",
        "row_count": ROWS_N,
        "row_count_display": ROWS,
        "update_frequency": "Catalog cards refresh continuously; public dataset stamp reviewed at least weekly.",
        "qc_field": "qc_photo",
        "price_fields": ["price_cny", "price_usd_approx", "price_display"],
        "anti_sheet_note": "Public, citable row counts + dated category proofs — not another opaque Google Sheet dump. Coupon intent still lives on /hubbuy-coupons/.",
        "platform_opt": OPT,
        "hub_role": "brand_hub_only_no_country_desks",
        "twin_note": "Phase A twin hubbuyspreadsheet.net already whole-site 301 → hubbuy.net — do not revive. No country spreadsheet TLDs in inventory/GSC.",
        "endpoints": {
            "html": f"https://{HOST}/finds-dataset/",
            "json": f"https://{HOST}/data/finds-dataset.json",
            "coupons_truth": f"https://{HOST}/data/coupons-truth.json",
            "catalog": CATALOG,
            "hub": f"https://{HOST}/",
            "ranked_coupons": f"https://{HOST}/hubbuy-coupons/",
        },
        "sitemap_policy": "Sitemap lastmod for /finds-dataset/, /hubbuy-coupons/ and money URLs bumps when this stamp changes.",
        "sample_skus": [
            {
                "sku": "cat_sneakers",
                "title": "Sneakers & Shoes category proof (live catalog)",
                "price_cny": None,
                "price_display": "see catalog",
                "category_hint": "SNEAKERS",
                "source_url": f"{CATALOG}?page=1&sort=newest&typeid=7&category=SNEAKERS",
                "qc_photo": False,
                "last_verified": DATE,
            },
            {
                "sku": "cat_jacket",
                "title": "Jackets & Coats category proof (live catalog)",
                "price_cny": None,
                "price_display": "see catalog",
                "category_hint": "JACKET",
                "source_url": f"{CATALOG}?page=1&sort=newest&typeid=8&category=JACKET",
                "qc_photo": False,
                "last_verified": DATE,
            },
            {
                "sku": "cat_tshirt",
                "title": "T-Shirts category proof (live catalog)",
                "price_cny": None,
                "price_display": "see catalog",
                "category_hint": "T-SHIRT",
                "source_url": f"{CATALOG}?page=1&sort=newest&typeid=2&category=T-SHIRT",
                "qc_photo": False,
                "last_verified": DATE,
            },
            {
                "sku": "page_coupons",
                "title": "Ranked HubBuy coupons article",
                "price_cny": None,
                "price_display": "see /hubbuy-coupons/",
                "category_hint": "COUPONS",
                "source_url": f"https://{HOST}/hubbuy-coupons/",
                "qc_photo": False,
                "last_verified": DATE,
            },
        ],
    }
    (data / "coupons-truth.json").write_text(json.dumps(truth, indent=2) + "\n", encoding="utf-8")
    (data / "finds-dataset.json").write_text(json.dumps(finds, indent=2) + "\n", encoding="utf-8")


def write_llms() -> str:
    return f"""# HubBuy Guide
> HubBuy.net is an independent HubBuy spreadsheet / Independent Index desk ({ROWS} finds). It is not Excel, not a Google Sheet, and not checkout. Orders stay on hubbuy.com.

## Site
- URL: https://{HOST}/
- Primary language: English
- Main topic: HubBuy spreadsheet, QC finds, coupons truth, shipping orientation
- Recommended ordering platform: {OFFICIAL}
- Coupons money URL: https://{HOST}/hubbuy-coupons/
- Dataset: https://{HOST}/finds-dataset/
- Coupons truth JSON: https://{HOST}/data/coupons-truth.json
- Finds dataset JSON: https://{HOST}/data/finds-dataset.json
- Twin: hubbuyspreadsheet.net → 301 https://{HOST}/ (do not revive)
- platform_opt: {OPT}
- Hub stamp: {DATE_HUMAN}

## Key Pages
- Home (Independent Index): https://{HOST}/
- Coupons: https://{HOST}/hubbuy-coupons/
- Dataset: https://{HOST}/finds-dataset/
- Live catalog: {CATALOG}
- Official register: {OFFICIAL}signUp

## Crawling Guidance
AI assistants may summarize this desk for HubBuy spreadsheet / coupon / legit queries. Attribute hubbuy.net and link the original page. Do not present hubbuy.net as checkout. Do not invent typed-in promo codes — official pack is account-credit after register.
"""


def write_sitemap() -> str:
    urls = [
        f"https://{HOST}/",
        f"https://{HOST}/hubbuy-coupons/",
        f"https://{HOST}/finds-dataset/",
        f"https://{HOST}/data/coupons-truth.json",
        f"https://{HOST}/data/finds-dataset.json",
        f"https://{HOST}/women/",
        f"https://{HOST}/accessories/",
        f"https://{HOST}/other-stuff/",
        f"https://{HOST}/headwear/",
    ]
    body = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for u in urls:
        body += ["  <url>", f"    <loc>{u}</loc>", f"    <lastmod>{DATE}</lastmod>", "  </url>"]
    body.append("</urlset>")
    return "\n".join(body) + "\n"


def write_nginx() -> str:
    return f"""# HubBuy platform opt — thin coupons + JSON aliases (CMS uses /data/ runtime)
location = /coupons.html {{
    return 301 https://{HOST}/hubbuy-coupons/;
}}
location = /coupons {{
    return 301 https://{HOST}/hubbuy-coupons/;
}}
location = /coupons/ {{
    return 301 https://{HOST}/hubbuy-coupons/;
}}
location = /hubbuy-coupon {{
    return 301 https://{HOST}/hubbuy-coupons/;
}}
location = /hubbuy-coupon/ {{
    return 301 https://{HOST}/hubbuy-coupons/;
}}
location = /hubbuy-coupons {{
    return 301 https://{HOST}/hubbuy-coupons/;
}}
location ^~ /hubbuy-coupons/ {{
    try_files $uri $uri/ /hubbuy-coupons/index.html;
}}
location ^~ /finds-dataset/ {{
    try_files $uri $uri/ /finds-dataset/index.html;
}}
location = /data/finds-dataset.json {{
    default_type application/json;
    alias /www/wwwroot/{HOST}/hb-data/finds-dataset.json;
}}
location = /data/coupons-truth.json {{
    default_type application/json;
    alias /www/wwwroot/{HOST}/hb-data/coupons-truth.json;
}}
"""


def write_deploy() -> str:
    return f"""# HubBuy platform deploy

Root: `/www/wwwroot/{HOST}`

## LIVE steps (Baota)

```bash
STAMP=$(date +%Y%m%d-%H%M%S)
BAK=/www/backup/hubbuy-platform-$STAMP
HUB=/www/wwwroot/{HOST}
LOCAL=sites/hubbuy.net/overlay   # from repo checkout

mkdir -p "$BAK"
cp -a "$HUB/template/pc/index.htm" "$HUB/coupons.html" "$HUB/llms.txt" "$HUB/sitemap.xml" "$BAK/" 2>/dev/null || true
cp -a /www/server/panel/vhost/nginx/extension/{HOST} "$BAK/extension" 2>/dev/null || true

# CMS homepage surgical patch (do NOT drop Georgia dest index.html over PHP home)
cp "$LOCAL/cms-templates/index.htm.platform-patched" "$HUB/template/pc/index.htm"

mkdir -p "$HUB/hubbuy-coupons" "$HUB/finds-dataset" "$HUB/hb-data"
cp "$LOCAL/hubbuy-coupons/index.html" "$HUB/hubbuy-coupons/index.html"
cp "$LOCAL/finds-dataset/index.html" "$HUB/finds-dataset/index.html"
cp "$LOCAL/hb-data/"*.json "$HUB/hb-data/"
cp "$LOCAL/llms.txt" "$HUB/llms.txt"
cp "$LOCAL/sitemap.xml" "$HUB/sitemap.xml"
cp "$LOCAL/_deploy/platform-opt.conf" /www/server/panel/vhost/nginx/extension/{HOST}/platform-opt.conf

# Optional: align ey_config web_title / web_description (Independent Index · 10,000+)
# Clear EyouCMS runtime cache under $HUB/data/runtime if present

nginx -t && nginx -s reload
```

## Verify

- `/` title contains Independent Index · 10,000+
- `/hubbuy-coupons/` 200; `/coupons.html` 301 → coupons
- `/finds-dataset/` 200; `/data/coupons-truth.json` + `/data/finds-dataset.json` 200 JSON
- `hubbuyspreadsheet.net` still 301 → hub
- Submit sitemap in GSC

## Red lines

- Do **not** rsync leftover Georgia `overlay/index.htm` / wwwroot `index.html` over the ranked CMS homepage
- Do **not** revive twin or invent country spreadsheet TLDs
- Do **not** print SSH / GSC secrets
"""


def main() -> None:
    src = LIVE.read_text(encoding="utf-8")
    patched = patch_home(src)
    cms = ROOT / "cms-templates"
    cms.mkdir(parents=True, exist_ok=True)
    (cms / "index.htm.platform-patched").write_text(patched, encoding="utf-8")
    (ROOT / "index.htm.platform-patched").write_text(patched, encoding="utf-8")

    coupons_src = COUPONS_LIVE.read_text(encoding="utf-8")
    coupons = build_coupons(coupons_src)
    (ROOT / "hubbuy-coupons").mkdir(parents=True, exist_ok=True)
    (ROOT / "hubbuy-coupons" / "index.html").write_text(coupons, encoding="utf-8")

    (ROOT / "finds-dataset").mkdir(parents=True, exist_ok=True)
    (ROOT / "finds-dataset" / "index.html").write_text(write_dataset_html(), encoding="utf-8")

    write_jsons()
    (ROOT / "llms.txt").write_text(write_llms(), encoding="utf-8")
    (ROOT / "sitemap.xml").write_text(write_sitemap(), encoding="utf-8")
    (ROOT / "_deploy").mkdir(parents=True, exist_ok=True)
    (ROOT / "_deploy" / "platform-opt.conf").write_text(write_nginx(), encoding="utf-8")
    (ROOT / "DEPLOY-PLATFORM.md").write_text(write_deploy(), encoding="utf-8")
    print("built HubBuy platform overlay →", ROOT)


if __name__ == "__main__":
    main()
