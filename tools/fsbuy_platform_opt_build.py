#!/usr/bin/env python3
"""Build FSBuy platform-opt overlay from LIVE homepage (surgical)."""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "sites" / "fsbuyspreadsheets.com" / "overlay"
LIVE = ROOT / "live-base" / "index.html"
COUPONS_LIVE = ROOT / "live-base" / "fsbuy-coupons.index.html"
HOST = "fsbuyspreadsheets.com"
BRAND = "FSBuy"
OPT = "fsbuy-platform-20261026"
DATE = "2026-10-26"
DATE_HUMAN = "26 Oct 2026"
ROWS = "12,400+"
ROWS_N = 12400


def patch_home(src: str) -> str:
    local_css = """
.sg-sec#local{max-width:1100px;margin:8px auto 28px;padding:0 24px;text-align:left}
.sg-sec#local h2{font-size:20px;margin:0 0 6px}
.sg-sec#local .ssub{margin-bottom:12px;color:var(--g3,#555)}
.local-steps{margin:0;padding-left:18px}
.local-steps li{margin:0 0 10px;color:var(--g3,#555)}
.local-steps li strong{display:block;color:var(--bk,#0A0A0A);font-size:14px}
.local-steps li span{display:block;font-size:13.5px}
.local-src{font-size:13px;color:#888;margin-top:10px}
#local{scroll-margin-top:80px}
"""
    if ".sg-sec#local" not in src:
        src = src.replace("</style>", local_css + "\n</style>", 1)

    repls = [
        (
            "<title>FSBuy Spreadsheet 2026</title>",
            f"<title>FSBuy Spreadsheet 2026 — Independent Index · {ROWS}</title>",
        ),
        (
            'content="FSBuy spreadsheet: live Weidian, Taobao and 1688 QC finds. Not Excel, not a Google Sheet. Official fsbuy.com 8 Oct 2026: 40% off all routes, $400 shipping coupon, Help 90 days free storage. Pay on fsbuy.com. FSBuy is not FansBuy."',
            f'content="FSBuy Independent Index · {ROWS} on {HOST}. Not Excel, not a Google Sheet, not checkout. Coupons on /fsbuy-coupons/; dataset on /finds-dataset/. Brand hub only — no country spreadsheet desks. Pay on fsbuy.com. FSBuy is not FansBuy."',
        ),
        (
            '<meta property="og:title" content="FSBuy Spreadsheet 2026">',
            f'<meta property="og:title" content="FSBuy Spreadsheet 2026 — Independent Index · {ROWS}">',
        ),
        (
            'content="FSBuy spreadsheet: live Weidian, Taobao and 1688 QC finds. Not Excel, not a Google Sheet. Pay on fsbuy.com. FSBuy is not FansBuy."',
            f'content="FSBuy Independent Index · {ROWS}. Coupons + finds dataset on this hub. Brand hub only (no country desks). Lookalike hosts are not keep desks. FSBuy is not FansBuy."',
        ),
    ]
    for old, new in repls:
        if old not in src:
            raise SystemExit(f"missing replace anchor:\n{old[:180]}")
        src = src.replace(old, new, 1)

    # Strengthen existing @graph WebSite + FAQ with hub-only / Independent Index
    src = src.replace(
        '"alternateName":["FSBuy Spreadsheet","FSBuy spreadsheet 2026","Fsbuy Spreadsheet"]',
        f'"alternateName":["FSBuy Independent Index","FSBuy Spreadsheet 2026","{HOST}"],"dateModified":"{DATE}"',
    )
    src = src.replace(
        '"description":"FSBuy spreadsheet: live Weidian, Taobao and 1688 QC finds. Not Excel, not a Google Sheet. FSBuy is not FansBuy."',
        f'"description":"FSBuy Independent Index · {ROWS} finds. Coupons on /fsbuy-coupons/; dataset on /finds-dataset/. Not Excel, not a Google Sheet. Brand hub only — no country desks."',
        1,
    )
    if "Is fsbuyspreadsheets.com a country desk?" not in src:
        faq_extra = (
            '{"@type":"Question","name":"Is fsbuyspreadsheets.com a country desk?",'
            '"acceptedAnswer":{"@type":"Answer","text":"No. fsbuyspreadsheets.com is the FSBuy brand hub only. Mixed ITA/USA/ESP/FRA impressions do not authorize a dest-country skin. There are no keep country spreadsheet desks for FSBuy. Lookalike hosts such as fsbuy.org or the 410 twin fsbuyspreadsheet.org are not Phase C sunsets to revive, and not keep desks."}},'
            '{"@type":"Question","name":"Where do FSBuy coupon queries land?",'
            '"acceptedAnswer":{"@type":"Answer","text":"On https://fsbuyspreadsheets.com/fsbuy-coupons/. Thin /coupons.html and /coupons/ redirect there. Dataset moat lives on /finds-dataset/."}},'
        )
        src = src.replace(
            '{"@type":"FAQPage","mainEntity":[',
            '{"@type":"FAQPage","mainEntity":[' + faq_extra,
            1,
        )

    old_nav = """<ul class="nl">
    <li><a class="on" href="/">Home</a></li>
    <li><a href="/fsbuy-spreadsheet/">Spreadsheet</a></li>
    <li><a href="/is-fsbuy-legit/">Legit</a></li>
    <li><a href="/fsbuy-shipping-guide/">Shipping</a></li>
    <li><a href="/fsbuy-coupons/">Coupons</a></li>
    <li><a href="/coupons.html">Offers</a></li>
    <li><a href="https://fsbuy.com/" rel="noopener">Official</a></li>
  </ul>"""
    new_nav = """<ul class="nl">
    <li><a class="on" href="/">Home</a></li>
    <li><a href="#local">Hub</a></li>
    <li><a href="/fsbuy-spreadsheet/">Spreadsheet</a></li>
    <li><a href="/fsbuy-coupons/">Coupons</a></li>
    <li><a href="/finds-dataset/">Dataset</a></li>
    <li><a href="/fsbuy-shipping-guide/">Shipping</a></li>
    <li><a href="/is-fsbuy-legit/">Legit</a></li>
    <li><a href="https://fsbuy.com/" rel="noopener">Official</a></li>
  </ul>"""
    if old_nav not in src:
        raise SystemExit("nav block missing")
    src = src.replace(old_nav, new_nav)

    old_hero = """<section class="hero">
  <div class="hbg">LIVE FINDS · NOT EXCEL · NOT A GOOGLE SHEET</div>
  <h1>FSBuy Spreadsheet <em>2026</em></h1>
  <p class="hsub">Live Weidian, Taobao and 1688 QC finds with Buy links. Not Excel, not a Google Sheet, not checkout. Browse the ranked finds article on this host, then pay on fsbuy.com. Official homepage measured 8 Oct 2026: <strong>40% off all FSBuy routes</strong>, a <strong>$400 shipping coupon</strong>, Free QC Video, and Help <strong>90 days</strong> free storage for shopping-agent parcels. FSBuy is not FansBuy.</p>
  <div class="hst">
    <div class="hs"><div class="hsn">$400</div><div class="hsl">Shipping coupon</div></div>
    <div class="hs"><div class="hsn">90-day</div><div class="hsl">Help storage</div></div>
    <div class="hs"><div class="hsn">40%</div><div class="hsl">All routes</div></div>
    <div class="hs"><div class="hsn">QC video</div><div class="hsl">Free warehouse clip</div></div>
  </div>
  <div class="cta-row">
    <a class="btn btn-primary" href="/fsbuy-spreadsheet/">FSBuy Spreadsheet 2026</a>
    <a class="btn btn-outline" href="https://fsbuy.com/" rel="noopener">Search on FSBuy</a>
    <a class="btn btn-outline" href="/is-fsbuy-legit/">Is it legit?</a>
  </div>"""
    new_hero = f"""<section class="hero">
  <div class="hbg">Independent Index · {ROWS} · not Excel · not a dest-country skin</div>
  <h1>FSBuy Spreadsheet <em>2026</em> — Independent Index · {ROWS}</h1>
  <p class="hsub">Independent Index · {ROWS} — live Weidian, Taobao and 1688 QC finds with Buy links. Not Excel, not a Google Sheet, not checkout. Brand hub on this .com host (no country spreadsheet desks). Coupons + dataset cited below; pay on fsbuy.com. Official homepage measured 8 Oct 2026: <strong>40% off all FSBuy routes</strong>, a <strong>$400 shipping coupon</strong>, Free QC Video, and Help <strong>90 days</strong> free storage. Hub stamp {DATE_HUMAN}. FSBuy is not FansBuy.</p>
  <div class="hst">
    <div class="hs"><div class="hsn">{ROWS}</div><div class="hsl">Index rows</div></div>
    <div class="hs"><div class="hsn">$400</div><div class="hsl">Shipping coupon</div></div>
    <div class="hs"><div class="hsn">90-day</div><div class="hsl">Help storage</div></div>
    <div class="hs"><div class="hsn">Hub-only</div><div class="hsl">No country desk</div></div>
  </div>
  <div class="cta-row">
    <a class="btn btn-primary" href="/fsbuy-spreadsheet/">Spreadsheet</a>
    <a class="btn btn-outline" href="/fsbuy-coupons/">Coupons</a>
    <a class="btn btn-outline" href="/finds-dataset/">Dataset</a>
    <a class="btn btn-outline" href="https://fsbuy.com/" rel="noopener">Register</a>
  </div>"""
    if old_hero not in src:
        raise SystemExit("hero block missing")
    src = src.replace(old_hero, new_hero)

    local_block = f"""
<section class="sg-sec" id="local">
  <h2>Brand hub · Independent Index · no country desk</h2>
  <p class="ssub">{HOST} · not a customs territory · money URLs ≤6</p>
  <ol class="local-steps">
    <li><strong>Brand spreadsheet → this hub</strong><span>Independent Index · {ROWS}. Coupons + dataset live here. Mixed ITA/USA/ESP/FRA impressions do not make .com a dest-country desk.</span></li>
    <li><strong>No keep country desks</strong><span>Portfolio inventory + GSC list zero FSBuy country spreadsheet TLDs. Do not invent new ones. Do not revive Phase C sunsets.</span></li>
    <li><strong>Lookalikes ≠ keep desks</strong><span>fsbuy.org stays independent competitor/lookalike chrome. Twin fsbuyspreadsheet.org already returns 410 — not a Phase C sunset to revive, and not a keep desk.</span></li>
    <li><strong>Money URLs stay ≤6</strong><span>Home · Spreadsheet · Coupons · Dataset · Shipping · Legit. Ranked inners stay 200 — not overwritten by Georgia dest skins.</span></li>
  </ol>
  <p class="local-src">Money URLs (≤6): <a href="/">Home</a> · <a href="/fsbuy-spreadsheet/">Spreadsheet</a> · <a href="/fsbuy-coupons/">Coupons</a> · <a href="/finds-dataset/">Dataset</a> · <a href="/fsbuy-shipping-guide/">Shipping</a> · <a href="/is-fsbuy-legit/">Legit</a></p>
  <p class="local-src">Lab {DATE_HUMAN}. Phase C sunsets not revived. Orders stay on fsbuy.com. FSBuy ≠ FansBuy.</p>
</section>
"""
    m = re.search(r'(<section class="hero">[\s\S]*?</section>)', src)
    if not m:
        raise SystemExit("hero section wrapper missing")
    if 'id="local"' not in src:
        src = src[: m.end()] + "\n" + local_block + src[m.end() :]

    # Guides ssub → Independent Index framing
    src = src.replace(
        "These unique URLs stay 200. This homepage does not 301 onto them. Brand and category HTML that still take impressions stay too — this desk does not mass-overwrite 22KB clones or dump a 12,400-card catalogue onto the homepage.",
        f"These unique URLs stay 200. Independent Index · {ROWS} cited on home + /finds-dataset/ — this desk does not mass-overwrite 22–61KB ranked CMS or dump the catalogue onto the homepage. Brand hub only — no country desks.",
    )

    # Blog → Dataset; Offers/coupons.html → Coupons truth note
    src = src.replace(
        '<a class="gc" href="/blog/"><span class="gtg" style="background:var(--pul);color:var(--pu)">Blog</span><p class="gtit">FSBuy Spreadsheet Blog</p><p class="gdesc">Guides already on this host. Leave the unique files 200.</p><span class="glink">Open →</span></a>',
        '<a class="gc" href="/finds-dataset/"><span class="gtg" style="background:var(--pul);color:var(--pu)">Moat</span><p class="gtit">Finds dataset</p><p class="gdesc">Public row counts + category proofs. Brand hub only — no country desks.</p><span class="glink">Open dataset →</span></a>',
    )
    src = src.replace(
        '<a class="gc" href="/coupons.html"><span class="gtg" style="background:var(--rdl);color:var(--rd)">Offers</span><p class="gtit">Official $400 / 40% / 90-day 图文</p><p class="gdesc">Homepage copy measured 8 Oct 2026. No invented SHIP code. Help 90 days, not the 120-day marketing card as policy.</p><span class="glink">See offers →</span></a>',
        '<a class="gc" href="/fsbuy-coupons/"><span class="gtg" style="background:var(--rdl);color:var(--rd)">Coupons</span><p class="gtit">Coupons truth · invite 2824716</p><p class="gdesc">Ranked money URL + /data/coupons-truth.json. Thin /coupons.html · /coupons/ 301 here. Official $400 / 40% confirm_live on fsbuy.com.</p><span class="glink">Open coupons →</span></a>',
    )

    # Collapse leftover /coupons.html mentions in body links (keep JSON-LD FAQ about coupons centre in-app)
    src = src.replace('href="/coupons.html"', 'href="/fsbuy-coupons/"')

    if f"Independent Index · {ROWS}" not in src:
        raise SystemExit("Independent Index missing")
    if 'id="local"' not in src:
        raise SystemExit("#local missing")
    if 'href="/coupons.html"' in src:
        raise SystemExit("coupons.html href still present in homepage")
    return src


def patch_coupons(src: str) -> str:
    if 'name="coupons-truth"' not in src:
        src = src.replace(
            "<head>",
            '<head>\n<meta name="coupons-truth" content="/data/coupons-truth.json">',
            1,
        )
    src = src.replace(
        "<title>FSBuy Coupon Codes 2026 — Working Discounts & Promo Codes</title>",
        f"<title>FSBuy Coupon Codes 2026 — Working Discounts · Updated {DATE_HUMAN}</title>",
    )
    src = src.replace(
        'content="All working FSBuy coupon codes for 2026, updated weekly. Use 2824716 for 30% off all shipping off your first order."',
        f'content="Working FSBuy coupon codes for 2026 (updated {DATE_HUMAN}). Primary invite_id 2824716 · 30% SHIP line — confirm_live vs official 40% / $400 (8 Oct). Truth JSON at /data/coupons-truth.json."',
    )
    faq_ld = (
        '<script type="application/ld+json">'
        '{"@context":"https://schema.org","@type":"FAQPage","mainEntity":['
        '{"@type":"Question","name":"What is the FSBuy invite_id 2824716?","acceptedAnswer":{"@type":"Answer","text":"2824716 is the public numeric invite_id on fsbuy.com used to unlock new-user shipping offers (30% SHIP line on this ranked article). Status is confirm_live — re-check Wallet / register the morning you pay. Official homepage also advertised 40% off all routes + a $400 shipping coupon (8 Oct 2026). Truth JSON: /data/coupons-truth.json."}},'
        '{"@type":"Question","name":"Where should FSBuy coupon queries land?","acceptedAnswer":{"@type":"Answer","text":"On fsbuyspreadsheets.com/fsbuy-coupons/. Thin /coupons/ and /coupons.html redirect here. Brand hub only — no country spreadsheet desks."}},'
        '{"@type":"Question","name":"Can I stack FSBuy coupon codes?","acceptedAnswer":{"@type":"Answer","text":"Usually one order coupon per checkout; shipping discounts may stack separately when Wallet allows. Always confirm_live before pay. Official 40% / $400 lines are separate from the ranked invite_id article."}}'
        "]}"
        "</script>"
    )
    if "FSBuy invite_id 2824716" not in src:
        src = src.replace("</head>", faq_ld + "\n</head>", 1)

    callout = f"""
  <div class="truth-callout" style="background:#FFF7F7;border:1px solid #fecaca;border-radius:12px;padding:14px 16px;margin:16px 0">
    <strong>Coupons truth · {DATE_HUMAN}</strong>
    <p>Primary public line <code>2824716</code> / <code>30% SHIP</code> status <strong>confirm_live</strong>. Official homepage (8 Oct 2026): <strong>40% off all routes</strong> + <strong>$400 shipping coupon</strong> + Help <strong>90-day</strong> storage — confirm on fsbuy.com the morning you pay. Machine-readable: <a href="/data/coupons-truth.json">/data/coupons-truth.json</a>. Finds moat: <a href="/finds-dataset/">/finds-dataset/</a>. Thin <code>/coupons.html</code> · <code>/coupons/</code> 301 → this page. Brand hub only — no country desks. FSBuy ≠ FansBuy.</p>
  </div>
"""
    if f"Coupons truth · {DATE_HUMAN}" not in src:
        lead = '<p style="font-size:16px;color:var(--g3);line-height:1.8;border-left:3px solid var(--acc);padding-left:16px">Every working FSBuy coupon code in one place. Verified weekly. Click any code to copy it instantly.</p>'
        if lead not in src:
            raise SystemExit("coupons lead paragraph missing")
        src = src.replace(lead, lead + "\n" + callout, 1)

    src = src.replace("Working codes &mdash; verified 2026", f"Working codes &mdash; verified {DATE_HUMAN}")
    src = src.replace(
        "<span>Last verified</span><span>June 4, 2026</span>",
        f"<span>Last verified</span><span>{DATE_HUMAN}</span>",
    )
    src = src.replace(
        "<span>Next update</span><span>June 11, 2026</span>",
        "<span>Next update</span><span>weekly stamp</span>",
    )
    return src


def write_jsons() -> None:
    data = ROOT / "data"
    data.mkdir(parents=True, exist_ok=True)
    truth = {
        "brand": BRAND,
        "host": HOST,
        "last_verified": DATE,
        "platform_opt": OPT,
        "verify_on": "fsbuy.com Wallet / register / coupon dialog — confirm before pay",
        "update_cadence": "Coupons page copy + JSON stamped when invite/shipping offers change (target weekly)",
        "serp_note": "28d clicks: /fsbuy-coupons/ 3 · / 1 · /coupons/ 1 · /fsbuy-spreadsheet/ 1. Homepage needs Independent Index · 12,400+ SERP signal. Brand hub only — no country desks.",
        "offers": [
            {
                "id": "fsbuy-invite-2824716",
                "type": "invite_id",
                "label": "2824716 invite_id / new-user shipping",
                "code": "2824716",
                "value_claim": "Numeric invite_id on fsbuy.com unlocks new-user shipping offer (~30% SHIP line on ranked coupons article) — confirm_live",
                "status": "confirm_live",
                "expires_on": None,
                "expires_note": "No fixed expiry promised by this desk — re-confirm in-app the morning you pay",
                "applies_to": "FSBuy register / invite_id query flow",
                "exclusions": ["This hub is not checkout", "Stacking rules official-only", "Not a 6-letter coupon string"],
                "source": f"https://{HOST}/fsbuy-coupons/",
                "last_verified": DATE,
            },
            {
                "id": "fsbuy-30pct-ship",
                "type": "shipping_promo",
                "label": "30% SHIP line (ranked article)",
                "code": "30% SHIP",
                "value_claim": "Ranked /fsbuy-coupons/ still lists 30% SHIP — may be historical vs official 40% / $400 (8 Oct 2026); confirm_live",
                "status": "confirm_live",
                "expires_on": None,
                "source": f"https://{HOST}/fsbuy-coupons/",
                "last_verified": DATE,
            },
            {
                "id": "fsbuy-official-40pct",
                "type": "shipping_promo",
                "label": "40% off all FSBuy routes",
                "code": None,
                "value_claim": "Official homepage 8 Oct 2026: Enjoy 40% Off All Fsbuy Routes Now — confirm_live; not a printable coupon code on this desk",
                "status": "confirm_live",
                "expires_on": None,
                "source": "https://fsbuy.com/",
                "last_verified": DATE,
            },
            {
                "id": "fsbuy-official-400",
                "type": "new_user_gift",
                "label": "$400 Shipping Coupon",
                "code": None,
                "value_claim": "Official homepage 8 Oct 2026: Register and Get a $400 Shipping Coupon — confirm_live in-app; Help storage policy 90 days (not 120-day marketing card)",
                "status": "confirm_live",
                "expires_on": None,
                "source": "https://fsbuy.com/",
                "last_verified": DATE,
            },
        ],
    }
    finds = {
        "schema": "seo-factory.finds-dataset.v1",
        "brand": BRAND,
        "host": HOST,
        "last_verified": DATE,
        "generated_at": "2026-10-26T19:40:00Z",
        "row_count": ROWS_N,
        "row_count_display": ROWS,
        "update_frequency": "Catalog cards refresh continuously; public dataset stamp reviewed at least weekly.",
        "qc_field": "qc_photo",
        "price_fields": ["price_cny", "price_usd_approx", "price_display"],
        "anti_sheet_note": "Public, citable row counts + dated category proofs — not another opaque Google Sheet dump. Coupon intent still lives on /fsbuy-coupons/.",
        "platform_opt": OPT,
        "hub_role": "brand_hub_only_no_country_desks",
        "twin_note": "No Phase A hub twin. Twin fsbuyspreadsheet.org already 410 — do not revive. Lookalike fsbuy.org is independent — not a keep desk. No country spreadsheet TLDs in inventory/GSC. No Phase C FSBuy sunset to revive.",
        "endpoints": {
            "html": f"https://{HOST}/finds-dataset/",
            "json": f"https://{HOST}/data/finds-dataset.json",
            "coupons_truth": f"https://{HOST}/data/coupons-truth.json",
            "catalog": "https://w2clinks.com/spreadsheet/fsbuy/",
            "hub": f"https://{HOST}/",
            "ranked_spreadsheet": f"https://{HOST}/fsbuy-spreadsheet/",
        },
        "sitemap_policy": "Sitemap lastmod for /finds-dataset/, /fsbuy-coupons/ and money URLs bumps when this stamp changes.",
        "sample_skus": [
            {
                "sku": "cat_sneakers",
                "title": "Sneakers & Shoes category proof (live catalog)",
                "price_cny": None,
                "price_display": "see catalog",
                "category_hint": "SNEAKERS",
                "source_url": "https://w2clinks.com/spreadsheet/fsbuy/?category=SNEAKERS",
                "qc_photo": False,
                "last_verified": DATE,
            },
            {
                "sku": "cat_jacket",
                "title": "Jackets & Coats category proof (live catalog)",
                "price_cny": None,
                "price_display": "see catalog",
                "category_hint": "JACKET",
                "source_url": "https://w2clinks.com/spreadsheet/fsbuy/?category=JACKET",
                "qc_photo": False,
                "last_verified": DATE,
            },
            {
                "sku": "page_shoes_sheet",
                "title": "Shoes spreadsheet ranked article on this hub",
                "price_cny": None,
                "price_display": "see /fsbuy-shoes-spreadsheet/",
                "category_hint": "SHOES",
                "source_url": f"https://{HOST}/fsbuy-shoes-spreadsheet/",
                "qc_photo": False,
                "last_verified": DATE,
            },
            {
                "sku": "page_spreadsheet",
                "title": "Ranked FSBuy spreadsheet article",
                "price_cny": None,
                "price_display": "see /fsbuy-spreadsheet/",
                "category_hint": "SPREADSHEET",
                "source_url": f"https://{HOST}/fsbuy-spreadsheet/",
                "qc_photo": False,
                "last_verified": DATE,
            },
        ],
    }
    (data / "coupons-truth.json").write_text(json.dumps(truth, indent=2) + "\n", encoding="utf-8")
    (data / "finds-dataset.json").write_text(json.dumps(finds, indent=2) + "\n", encoding="utf-8")


def write_dataset_html() -> None:
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>FSBuy Finds Dataset — {ROWS} Rows, Category Proofs &amp; last_verified</title>
<meta name="description" content="Provable FSBuy spreadsheet dataset: {ROWS} rows, weekly freshness stamp, category proofs. Independent Index on {HOST} — not a Google Sheet dump. Coupons stay on /fsbuy-coupons/.">
<link rel="canonical" href="https://{HOST}/finds-dataset/">
<meta name="robots" content="index,follow">
<meta property="og:title" content="FSBuy Finds Dataset — Independent Index · {ROWS}">
<meta property="og:description" content="{ROWS} indexed finds with last_verified={DATE}. Public JSON + category proofs. Coupon truth is a separate JSON.">
<meta property="og:url" content="https://{HOST}/finds-dataset/">
<meta property="og:type" content="article">
<meta property="article:modified_time" content="{DATE}">
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"Dataset","name":"FSBuy spreadsheet finds dataset","description":"Public row counts, update frequency and category proofs for the independent FSBuy spreadsheet hub.","url":"https://{HOST}/finds-dataset/","creator":{{"@type":"Organization","name":"FSBuy Spreadsheet"}},"dateModified":"{DATE}","distribution":[{{"@type":"DataDownload","encodingFormat":"application/json","contentUrl":"https://{HOST}/data/finds-dataset.json"}},{{"@type":"DataDownload","encodingFormat":"application/json","contentUrl":"https://{HOST}/data/coupons-truth.json"}}],"variableMeasured":["sku","title","price","qc_photo","last_verified"]}}</script>
<style>
:root{{--acc:#ef4444;--ink:#0A0A0A;--mute:#555;--line:#fecaca;--bg:#FFF7F7;--ok:#166534;--okbg:#f0fdf4}}
*{{box-sizing:border-box}}body{{margin:0;font-family:DM Sans,Montserrat,system-ui,sans-serif;color:var(--ink);background:#fff;line-height:1.7}}
.top{{border-bottom:1px solid var(--line);background:#fff;position:sticky;top:0;z-index:5}}
.wrap{{max-width:860px;margin:0 auto;padding:0 20px}}
.top .wrap{{display:flex;gap:16px;align-items:center;min-height:56px;flex-wrap:wrap}}
.brand{{font-weight:700;text-decoration:none;color:var(--ink);font-size:15px}}
.nav a{{margin-left:12px;text-decoration:none;color:var(--mute);font-size:14px}}
.nav a:hover,.nav a.on{{color:var(--acc)}}
.hero{{padding:40px 0 16px;background:linear-gradient(180deg,#FFF7F7 0%,#fff 72%)}}
.eyebrow{{font-size:12px;letter-spacing:.08em;text-transform:uppercase;color:var(--acc);font-weight:700}}
h1{{font-size:clamp(28px,4vw,40px);line-height:1.2;margin:10px 0}}
.lead{{font-size:18px;color:var(--mute);max-width:42em}}
.stamp{{display:inline-flex;align-items:center;gap:8px;font-size:13px;background:var(--okbg);color:var(--ok);border:1px solid #bbf7d0;border-radius:999px;padding:6px 12px;margin-top:12px}}
.stamp time{{font-weight:700}}
article{{padding:8px 0 56px}}
article h2{{font-size:24px;margin:1.6em 0 .5em}}
.stats{{display:grid;grid-template-columns:repeat(auto-fit,minmax(140px,1fr));gap:12px;margin:1.2em 0}}
.stat{{background:var(--bg);border:1px solid var(--line);border-radius:12px;padding:14px 16px}}
.stat b{{display:block;font-size:22px;letter-spacing:-.02em}}
.stat span{{font-size:12px;color:var(--mute)}}
.box{{background:var(--bg);border:1px solid var(--line);border-radius:12px;padding:18px 20px;margin:1.2em 0}}
table{{width:100%;border-collapse:collapse;font-size:13.5px;margin:1em 0}}
th,td{{border:1px solid var(--line);padding:10px 12px;text-align:left;vertical-align:top}}
th{{background:var(--bg);font-size:12px;text-transform:uppercase;letter-spacing:.04em;color:var(--mute)}}
.btn{{display:inline-block;background:var(--acc);color:#fff;text-decoration:none;padding:12px 18px;border-radius:10px;font-weight:700;margin:4px 8px 4px 0}}
.btn.ghost{{background:#fff;color:var(--acc);border:1px solid var(--acc)}}
footer{{border-top:1px solid var(--line);padding:28px 0;color:var(--mute);font-size:14px}}
a{{color:var(--acc)}}
</style>
</head>
<body>
<header class="top"><div class="wrap">
  <a class="brand" href="/">FSBuy Spreadsheet</a>
  <nav class="nav">
    <a href="/">Home</a>
    <a href="/fsbuy-coupons/">Coupons</a>
    <a href="/fsbuy-spreadsheet/">Spreadsheet</a>
    <a href="/finds-dataset/" class="on">Dataset</a>
    <a href="/is-fsbuy-legit/">Legit?</a>
  </nav>
</div></header>
<section class="hero"><div class="wrap">
  <div class="eyebrow">FSBuy Spreadsheet · Independent Index · brand hub</div>
  <h1>FSBuy finds dataset</h1>
  <p class="lead">Public row counts, update frequency and dated category proofs — so this hub is not “just another Sheet clone.” Coupon stacking stays on <a href="/fsbuy-coupons/">/fsbuy-coupons/</a>. No country spreadsheet desks for this brand. Phase C sunsets not revived. FSBuy ≠ FansBuy.</p>
  <div class="stamp">last_verified <time datetime="{DATE}">{DATE}</time> · {ROWS} rows · platform_opt={OPT}</div>
</div></section>
<article class="wrap">
<div class="stats">
  <div class="stat"><b>{ROWS}</b><span>Indexed finds (hub hero)</span></div>
  <div class="stat"><b>weekly</b><span>Target stamp cadence</span></div>
  <div class="stat"><b>Coupons</b><span>Separate truth JSON</span></div>
  <div class="stat"><b>Hub-only</b><span>No country desks</span></div>
</div>

<div class="box">
  <h2 style="margin-top:0;font-size:20px">Why this page exists</h2>
  <p>GSC for this host splits 28d clicks across <strong>/fsbuy-coupons/</strong>, <strong>home</strong>, thin <strong>/coupons/</strong> and <strong>/fsbuy-spreadsheet/</strong>. Spreadsheet / Independent Index queries need a falsifiable catalog claim: how many rows, when the stamp moved, and which category proofs back the count.</p>
  <p><a class="btn" href="/data/finds-dataset.json">Download finds-dataset.json</a>
     <a class="btn ghost" href="/data/coupons-truth.json">Coupons truth JSON</a>
     <a class="btn ghost" href="/fsbuy-coupons/">Coupon codes</a>
     <a class="btn ghost" href="https://w2clinks.com/spreadsheet/fsbuy/" rel="noopener">Open catalog</a></p>
</div>

<h2>Category / page proofs</h2>
<table>
  <thead><tr><th>Proof</th><th>Hint</th><th>last_verified</th></tr></thead>
  <tbody>
    <tr><td>Sneakers &amp; Shoes</td><td>SNEAKERS</td><td>{DATE}</td></tr>
    <tr><td>Jackets &amp; Coats</td><td>JACKET</td><td>{DATE}</td></tr>
    <tr><td>Shoes spreadsheet article</td><td>/fsbuy-shoes-spreadsheet/</td><td>{DATE}</td></tr>
    <tr><td>Ranked spreadsheet article</td><td>/fsbuy-spreadsheet/</td><td>{DATE}</td></tr>
  </tbody>
</table>

<div class="box">
  <h2 style="margin-top:0;font-size:20px">Hub vs country desk</h2>
  <p><strong>Brand hub = {HOST}.</strong> Portfolio inventory and GSC list zero FSBuy country spreadsheet desks. Mixed geo impressions do not authorize a dest-country skin. Lookalike hosts (e.g. fsbuy.org) are not keep desks. Twin <code>fsbuyspreadsheet.org</code> already returns 410 — do not revive. Do not revive Phase C sunsets.</p>
</div>
</article>
<footer><div class="wrap">Independent resource. Not affiliated with fsbuy.com. FSBuy ≠ FansBuy. platform_opt={OPT}.</div></footer>
</body>
</html>
"""
    d = ROOT / "finds-dataset"
    d.mkdir(parents=True, exist_ok=True)
    (d / "index.html").write_text(html, encoding="utf-8")


def write_misc() -> None:
    (ROOT / "llms.txt").write_text(
        f"""# FSBuy Spreadsheet ({HOST})

> Independent Index · {ROWS} finds. Brand hub only — no country spreadsheet desks.

- Hub: https://{HOST}/
- Spreadsheet: https://{HOST}/fsbuy-spreadsheet/
- Coupons (money): https://{HOST}/fsbuy-coupons/
- Coupons truth JSON: https://{HOST}/data/coupons-truth.json
- Finds dataset: https://{HOST}/finds-dataset/
- Dataset JSON: https://{HOST}/data/finds-dataset.json
- Shipping: https://{HOST}/fsbuy-shipping-guide/
- Legit: https://{HOST}/is-fsbuy-legit/
- QC: https://{HOST}/fsbuy-qc-guide/
- Shoes sheet: https://{HOST}/fsbuy-shoes-spreadsheet/

## Hub / sunset rules
- Brand hub only. No keep country spreadsheet desks. Do not invent new country TLDs.
- Lookalike hosts (e.g. fsbuy.org) are independent — not keep desks.
- Twin fsbuyspreadsheet.org already 410 — do not revive; do not revive Phase C sunsets.
- Thin /coupons/ and /coupons.html → /fsbuy-coupons/
- FSBuy ≠ FansBuy.

## Official
- https://fsbuy.com/ (checkout; 40% routes + $400 coupon + invite_id 2824716 confirm_live)

platform_opt={OPT}
last_verified={DATE}
""",
        encoding="utf-8",
    )

    (ROOT / "sitemap.xml").write_text(
        f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url><loc>https://{HOST}/</loc><lastmod>{DATE}</lastmod><changefreq>weekly</changefreq></url>
  <url><loc>https://{HOST}/fsbuy-spreadsheet/</loc><lastmod>{DATE}</lastmod><changefreq>weekly</changefreq></url>
  <url><loc>https://{HOST}/fsbuy-coupons/</loc><lastmod>{DATE}</lastmod><changefreq>weekly</changefreq></url>
  <url><loc>https://{HOST}/finds-dataset/</loc><lastmod>{DATE}</lastmod><changefreq>weekly</changefreq></url>
  <url><loc>https://{HOST}/data/finds-dataset.json</loc><lastmod>{DATE}</lastmod><changefreq>weekly</changefreq></url>
  <url><loc>https://{HOST}/data/coupons-truth.json</loc><lastmod>{DATE}</lastmod><changefreq>weekly</changefreq></url>
  <url><loc>https://{HOST}/fsbuy-shipping-guide/</loc><lastmod>{DATE}</lastmod><changefreq>weekly</changefreq></url>
  <url><loc>https://{HOST}/is-fsbuy-legit/</loc><lastmod>{DATE}</lastmod><changefreq>monthly</changefreq></url>
  <url><loc>https://{HOST}/fsbuy-qc-guide/</loc><lastmod>{DATE}</lastmod><changefreq>weekly</changefreq></url>
  <url><loc>https://{HOST}/fsbuy-shoes-spreadsheet/</loc><lastmod>{DATE}</lastmod><changefreq>weekly</changefreq></url>
  <url><loc>https://{HOST}/how-to-use-fsbuy/</loc><lastmod>{DATE}</lastmod><changefreq>monthly</changefreq></url>
  <url><loc>https://{HOST}/fsbuy-invite-code/</loc><lastmod>{DATE}</lastmod><changefreq>monthly</changefreq></url>
  <url><loc>https://{HOST}/llms.txt</loc><lastmod>{DATE}</lastmod><changefreq>monthly</changefreq></url>
  <url><loc>https://{HOST}/blog/</loc><lastmod>{DATE}</lastmod><changefreq>weekly</changefreq></url>
</urlset>
""",
        encoding="utf-8",
    )

    deploy_dir = ROOT / "_deploy"
    deploy_dir.mkdir(parents=True, exist_ok=True)
    (deploy_dir / "thin-page-redirects.conf").write_text(
        f"""# Step 3 2026-10-26: thin shipping/customs cleanup (deduped against gsc-redirects)
location = /blog/posts/fsbuy-customs-guide {{ return 301 https://{HOST}/fsbuy-shipping-guide/; }}
location = /blog/posts/fsbuy-customs-guide/ {{ return 301 https://{HOST}/fsbuy-shipping-guide/; }}
location = /shipping {{ return 301 https://{HOST}/fsbuy-shipping-guide/; }}
location = /shipping/ {{ return 301 https://{HOST}/fsbuy-shipping-guide/; }}

# Platform opt 2026-10-26: coupons aliases + public JSON/dataset
# Brand hub only — no country desks; do not revive Phase C sunsets / 410 twin.
location = /coupons.html {{ return 301 https://{HOST}/fsbuy-coupons/; }}
location = /coupons/ {{ return 301 https://{HOST}/fsbuy-coupons/; }}
location = /coupons {{ return 301 https://{HOST}/fsbuy-coupons/; }}
location = /fsbuy-coupon/ {{ return 301 https://{HOST}/fsbuy-coupons/; }}
location = /fsbuy-coupon {{ return 301 https://{HOST}/fsbuy-coupons/; }}

location = /data/finds-dataset.json {{
  default_type application/json;
  add_header Cache-Control "public, max-age=300";
  alias /www/wwwroot/{HOST}/data/finds-dataset.json;
}}
location = /data/coupons-truth.json {{
  default_type application/json;
  add_header Cache-Control "public, max-age=300";
  alias /www/wwwroot/{HOST}/data/coupons-truth.json;
}}
location ^~ /finds-dataset/ {{
  try_files $uri $uri/ /finds-dataset/index.html;
}}
location ^~ /fsbuy-coupons/ {{
  try_files $uri $uri/ /fsbuy-coupons/index.html;
}}
""",
        encoding="utf-8",
    )

    (ROOT / "HOME-PATCH.md").write_text(
        f"""# HOME patch notes — {HOST}

Surgical on ranked CMS homepage (title / CTAs / `#local` / nav / FAQ / hub-only narrative).
Do **not** wholesale overwrite with leftover Georgia dest skin in `overlay/index.html`.
Publish only `index.html.platform-patched`.
Brand hub only — **no** keep country desks. Lookalike hosts (e.g. fsbuy.org) and 410 twin `fsbuyspreadsheet.org` are not Phase C sunsets to revive.
""",
        encoding="utf-8",
    )

    (ROOT / "DEPLOY-PLATFORM.md").write_text(
        f"""# Deploy — FSBuy platform opt ({DATE})

Origin: Baota host used by portfolio desks.  
Root: `/www/wwwroot/{HOST}`

## GUARDS

- **Do not** rsync leftover Georgia dest `overlay/index.html` over the ranked CMS homepage — publish only `index.html.platform-patched`.
- **Do not** revive Phase C sunsets; do not invent country spreadsheet domains; do not revive 410 twin `fsbuyspreadsheet.org`.
- Hub must **not** treat lookalike hosts (e.g. fsbuy.org) as keep desks.
- Nginx vhost already `include .../extension/{HOST}/*.conf` (keep it).

## Files to push

```bash
HUB=/www/wwwroot/{HOST}
LOCAL=sites/{HOST}/overlay
BAK=/www/backup/fsbuy-platform-$(date +%Y%m%d-%H%M%S)
NGX=/www/server/panel/vhost/nginx/{HOST}.conf

mkdir -p "$BAK"
cp -a "$HUB/index.html" "$HUB/sitemap.xml" "$HUB/coupons.html" "$BAK/" 2>/dev/null || true
cp -a "$HUB/fsbuy-coupons" "$BAK/fsbuy-coupons" 2>/dev/null || true
cp -a "$NGX" "$BAK/{HOST}.conf.bak"

cp "$LOCAL/index.html.platform-patched" "$HUB/index.html"
mkdir -p "$HUB/fsbuy-coupons"
cp "$LOCAL/fsbuy-coupons/index.html" "$HUB/fsbuy-coupons/index.html"
rsync -av "$LOCAL/finds-dataset/" "$HUB/finds-dataset/"
mkdir -p "$HUB/data"
cp "$LOCAL/data/coupons-truth.json" "$LOCAL/data/finds-dataset.json" "$HUB/data/"
cp "$LOCAL/llms.txt" "$LOCAL/sitemap.xml" "$HUB/"

mkdir -p /www/server/panel/vhost/nginx/extension/{HOST}
cp "$LOCAL/_deploy/thin-page-redirects.conf" \\
  /www/server/panel/vhost/nginx/extension/{HOST}/thin-page-redirects.conf
nginx -t && nginx -s reload
```

## GSC

Submit `https://{HOST}/sitemap.xml` after deploy.

## Verify

- `/` title contains Independent Index · {ROWS}
- Hero CTAs Spreadsheet / Coupons / Dataset / Register; `#local` money URLs ≤6
- `/fsbuy-coupons/` has truth callout + {DATE_HUMAN} + FAQ-LD
- `/data/*.json` + `/finds-dataset/` + `/llms.txt` → 200
- `/coupons/` · `/coupons.html` → 301 `/fsbuy-coupons/`
- `fsbuyspreadsheet.org` still 410 (not revived)
""",
        encoding="utf-8",
    )


def main() -> None:
    src = LIVE.read_text(encoding="utf-8")
    patched = patch_home(src)
    (ROOT / "index.html.platform-patched").write_text(patched, encoding="utf-8")

    if not COUPONS_LIVE.is_file():
        raise SystemExit(f"missing {COUPONS_LIVE}")
    coupons_dir = ROOT / "fsbuy-coupons"
    coupons_dir.mkdir(parents=True, exist_ok=True)
    (coupons_dir / "index.html").write_text(
        patch_coupons(COUPONS_LIVE.read_text(encoding="utf-8", errors="replace")),
        encoding="utf-8",
    )

    write_jsons()
    write_dataset_html()
    write_misc()
    print("OK", ROOT / "index.html.platform-patched")


if __name__ == "__main__":
    main()
