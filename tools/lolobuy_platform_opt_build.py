#!/usr/bin/env python3
"""Build LoloBuy platform-opt overlay from LIVE homepage (surgical)."""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "sites" / "bestlolobuyspreadsheet.com" / "overlay"
LIVE = ROOT / "live-base" / "index.html"
COUPONS_LIVE = Path("/tmp/lolobuy-live/coupons.html")


def patch_home(src: str) -> str:
    local_css = """
.sg-sec#local{max-width:820px;margin:8px auto 28px;padding:0 22px;text-align:left}
.sg-sec#local h2{font-size:20px;margin:0 0 6px}
.sg-sec#local .ssub{margin-bottom:12px}
.local-steps{margin:0;padding-left:18px}
.local-steps li{margin:0 0 10px;color:var(--muted)}
.local-steps li strong{display:block;color:var(--ink);font-size:14px}
.local-steps li span{display:block;font-size:13.5px}
.local-src{font-size:13px;color:#888;margin-top:10px}
#local{scroll-margin-top:80px}
"""
    if ".sg-sec#local" not in src:
        src = src.replace("</style>", local_css + "\n</style>", 1)

    repls = [
        (
            "<title>LoLoBuy QC Spreadsheet 2026</title>",
            "<title>LoLoBuy Spreadsheet 2026 — Independent Index · 9,200+</title>",
        ),
        (
            'content="LoLoBuy QC spreadsheet 2026 — warehouse inspection photos and reject notes. Live finds, not Excel and not a Google Sheet. Official lolobuy.com 9 Oct 2026: free quality inspection pictures, 180 days free of storage charge. lolospreadsheet.com stays the parcel SOP hub."',
            'content="LoLoBuy Independent Index · 9,200+ QC finds on bestlolobuyspreadsheet.com. Not Excel, not a Google Sheet, not checkout. Coupons on /guides/coupons/; dataset on /finds-dataset/. Twin lolospreadsheet.com already 301→this hub. Pay on lolobuy.com."',
        ),
        (
            '<meta property="og:title" content="LoLoBuy QC Spreadsheet 2026">',
            '<meta property="og:title" content="LoLoBuy Spreadsheet 2026 — Independent Index · 9,200+">',
        ),
        (
            'content="Warehouse QC photos for LoLoBuy finds. Not Excel, not a Google Sheet, not checkout. Independent of lolospreadsheet.com."',
            'content="LoLoBuy Independent Index · 9,200+. Coupons + finds dataset on this hub. Twin lolospreadsheet.com already 301→here. Not a dest-country skin."',
        ),
        (
            '"name":"LoLoBuy QC Spreadsheet","alternateName":["LoLoBuy QC Spreadsheet 2026","bestlolobuyspreadsheet.com"],"url":"https://bestlolobuyspreadsheet.com/","description":"Warehouse QC photos and reject notes for LoLoBuy finds. Not Excel, not a Google Sheet.","inLanguage":"en"',
            '"name":"LoLoBuy Spreadsheet","alternateName":["LoLoBuy Independent Index","LoLoBuy QC Spreadsheet 2026","bestlolobuyspreadsheet.com"],"dateModified":"2026-10-26","url":"https://bestlolobuyspreadsheet.com/","description":"LoLoBuy Independent Index · 9,200+ QC finds. Coupons on /guides/coupons/; dataset on /finds-dataset/. Not Excel, not a Google Sheet.","inLanguage":"en"',
        ),
        (
            '"name":"LoLoBuy QC Spreadsheet 2026","url":"https://bestlolobuyspreadsheet.com/","description":"Independent LoLoBuy QC desk. Warehouse inspection stays on lolobuy.com. lolospreadsheet.com stays the SOP hub."',
            '"name":"LoLoBuy Spreadsheet 2026 — Independent Index · 9,200+","url":"https://bestlolobuyspreadsheet.com/","description":"Brand hub only. Twin lolospreadsheet.com already 301→this host. No country spreadsheet desks."',
        ),
        (
            '{"@type":"Question","name":"Is this the same host as lolospreadsheet.com?","acceptedAnswer":{"@type":"Answer","text":"No. lolospreadsheet.com is a separate parcel SOP hub. bestlolobuyspreadsheet.com is the QC hub. Both stay independent — there is no 301 between them."}}',
            '{"@type":"Question","name":"What happened to lolospreadsheet.com?","acceptedAnswer":{"@type":"Answer","text":"lolospreadsheet.com is a Phase A hub twin. It already 301s to bestlolobuyspreadsheet.com (including deep paths). Do not treat it as a live SOP desk. Brand spreadsheet + coupons + dataset live on this hub only. There are no keep country spreadsheet desks for LoloBuy."}}',
        ),
        (
            '<div class="st"><b>No 301</b><span>SOP twin</span></div>',
            '<div class="st"><b>9,200+</b><span>index rows</span></div>',
        ),
        (
            "lolospreadsheet.com is a separate parcel-SOP hub. Both stay independent under the August 2026 duplicate-site rule — there is no 301 either way, and this HTML is not a clone of that SOP homepage (different title, Open Sans / official orange QC chrome, warehouse-inspection IA).",
            "Former twin <code>lolospreadsheet.com</code> already <strong>301s to this hub</strong> (Phase A). Do not list it as a live SOP desk. This HTML keeps the ranked QC/brand IA — Open Sans / official orange chrome — and does not invent country spreadsheet domains.",
        ),
        (
            "What this QC hostname is not: it is not lolospreadsheet.com (parcel SOP, booking a line, 180-day storage as a shipping clock).",
            "What this hub is not: it is not a live twin of lolospreadsheet.com (that host already 301s here). It is not a customs territory.",
        ),
        (
            "It is not LoloBuy warehouse SOP and it is not the parcel-SOP copy on lolospreadsheet.com.",
            "It is not LoloBuy warehouse SOP and it does not revive the sunset twin.",
        ),
        (
            "bestlolobuyspreadsheet.com — Independent LoLoBuy QC spreadsheet. Not Excel. Not a Google Sheet. Not a dest-country skin. lolospreadsheet.com stays independent.",
            "bestlolobuyspreadsheet.com — Independent Index · 9,200+. Brand hub only (no country desks). Twin lolospreadsheet.com already 301→here.",
        ),
        (
            '<p><a href="/guides/qc/">QC photos</a><br><a href="/guides/coupons/">Coupons</a><br><a href="/guides/shipping/">Shipping</a><br><a href="/spreadsheet/">Spreadsheet</a></p>',
            '<p><a href="/spreadsheet/">Spreadsheet</a><br><a href="/guides/coupons/">Coupons</a><br><a href="/finds-dataset/">Dataset</a><br><a href="/guides/qc/">QC photos</a><br><a href="/guides/shipping/">Shipping</a></p>',
        ),
        (
            "© 2026 bestlolobuyspreadsheet.com — warehouse QC index. Copy reviewed 9 Oct 2026 against the live LoloBuy homepage. Invite token off this page. No 301 onto lolospreadsheet.com.",
            "© 2026 bestlolobuyspreadsheet.com — Independent Index · 9,200+. Updated 26 Oct 2026. Invite stacking on /guides/coupons/. Twin lolospreadsheet.com already 301→this hub.",
        ),
        (
            'Extra 图文: <a href="/coupons.html">/coupons.html</a>.',
            'Thin <code>/coupons/</code> · <code>/coupons.html</code> 301 → <a href="/guides/coupons/">/guides/coupons/</a>.',
        ),
    ]
    for old, new in repls:
        if old not in src:
            raise SystemExit(f"missing replace anchor:\n{old[:120]}")
        src = src.replace(old, new)

    old_nav = """  <ul class=\"nl\">
    <li><a href=\"/\">Home</a></li>
    <li><a href=\"/guides/qc/\">QC photos</a></li>
    <li><a href=\"/spreadsheet/\">Spreadsheet</a></li>
    <li><a href=\"/guides/shipping/\">Shipping</a></li>
    <li><a href=\"/guides/coupons/\">Coupons</a></li>
    <li><a href=\"/guides/is-lolobuy-legit/\">Is it legit?</a></li>
  </ul>"""
    new_nav = """  <ul class=\"nl\">
    <li><a href=\"#local\">Hub</a></li>
    <li><a href=\"/spreadsheet/\">Spreadsheet</a></li>
    <li><a href=\"/guides/coupons/\">Coupons</a></li>
    <li><a href=\"/finds-dataset/\">Dataset</a></li>
    <li><a href=\"/guides/qc/\">QC photos</a></li>
    <li><a href=\"/guides/shipping/\">Shipping</a></li>
    <li><a href=\"/guides/is-lolobuy-legit/\">Legit?</a></li>
  </ul>"""
    if old_nav not in src:
        raise SystemExit("nav block missing")
    src = src.replace(old_nav, new_nav)

    old_hero = """  <h1>LoLoBuy QC Spreadsheet <em>2026</em></h1>
  <p class=\"hsub\">This desk is the warehouse-inspection index — pass / reject photos for Weidian, Taobao and 1688 rows. It is not Excel and not a Google Sheet. Parcel booking stays on <a href=\"https://lolospreadsheet.com/\">lolospreadsheet.com</a> (independent SOP hub, no 301). Payment stays on lolobuy.com. This host is not a dest-country skin.</p>
  <div class=\"cta-row\">
    <a class=\"btn btn-primary\" href=\"/guides/qc/\">Open QC photos →</a>
    <a class=\"btn btn-dark\" href=\"https://www.lolobuy.com/\" rel=\"noopener\">Register on LoloBuy</a>
    <a class=\"btn btn-ghost\" href=\"#official-promo\">Official QC 图文</a>
  </div>"""
    new_hero = """  <h1>LoLoBuy Spreadsheet <em>2026</em> — Independent Index · 9,200+</h1>
  <p class=\"hsub\">Independent Index · 9,200+ — warehouse QC finds, brand rows and W2C. Not Excel, not a Google Sheet, not checkout. Brand hub on this .com host (no country spreadsheet desks). Twin <code>lolospreadsheet.com</code> already <strong>301 → here</strong>. Coupons + dataset cited below; pay on lolobuy.com.</p>
  <div class=\"cta-row\">
    <a class=\"btn btn-primary\" href=\"/spreadsheet/\">Spreadsheet</a>
    <a class=\"btn btn-dark\" href=\"/guides/coupons/\">Coupons</a>
    <a class=\"btn btn-ghost\" href=\"/finds-dataset/\">Dataset</a>
    <a class=\"btn btn-ghost\" href=\"https://www.lolobuy.com/\" rel=\"noopener\">Register</a>
  </div>"""
    if old_hero not in src:
        raise SystemExit("hero block missing")
    src = src.replace(old_hero, new_hero)

    old_sister = """    <a class=\"gc\" href=\"https://lolospreadsheet.com/\" rel=\"noopener\"><span class=\"gtg\">Sister SOP</span><p class=\"gtit\">lolospreadsheet.com</p><p class=\"gdesc\">Parcel SOP hub. Independent. No 301 onto this QC hostname.</p><span>Independent →</span></a>"""
    new_sister = """    <a class=\"gc\" href=\"/finds-dataset/\"><span class=\"gtg\">Moat</span><p class=\"gtit\">Finds dataset</p><p class=\"gdesc\">Public row counts + category proofs. Twin lolospreadsheet.com already 301→this hub.</p><span>Open dataset →</span></a>"""
    if old_sister not in src:
        raise SystemExit("sister card missing")
    src = src.replace(old_sister, new_sister)

    local_block = """
<section class="sg-sec" id="local">
  <h2>Brand hub · Independent Index · no country desk</h2>
  <p class="ssub">bestlolobuyspreadsheet.com · not a customs territory · money URLs ≤6</p>
  <ol class="local-steps">
    <li><strong>Brand spreadsheet → this hub</strong><span>Independent Index · 9,200+. Coupons + dataset live here. Mixed CAN/SRB/USA impressions do not make .com a dest-country desk.</span></li>
    <li><strong>Twin already 301</strong><span><code>lolospreadsheet.com</code> → this hub (Phase A). Do not revive as a live SOP desk. Do not invent new country spreadsheet TLDs.</span></li>
    <li><strong>Money URLs stay ≤6</strong><span>Home · Spreadsheet · Coupons · Dataset · Shipping · Legit. Brand folders (Nike / LV / Moncler) stay 200 — not overwritten.</span></li>
    <li><strong>Orders stay on lolobuy.com</strong><span>This hub never takes payment. Invite stacking documented on /guides/coupons/ (code 2pgzy — confirm_live).</span></li>
  </ol>
  <p class="local-src">Money URLs (≤6): <a href="/">Home</a> · <a href="/spreadsheet/">Spreadsheet</a> · <a href="/guides/coupons/">Coupons</a> · <a href="/finds-dataset/">Dataset</a> · <a href="/guides/shipping/">Shipping</a> · <a href="/guides/is-lolobuy-legit/">Legit</a></p>
  <p class="local-src">Lab 26 Oct 2026. Twin sunset kept. Phase C sunsets not revived.</p>
</section>
"""
    m = re.search(r'(<section class="hero fade-in">[\s\S]*?</section>)', src)
    if not m:
        raise SystemExit("hero section wrapper missing")
    if 'id="local"' not in src:
        src = src[: m.end()] + "\n" + local_block + src[m.end() :]

    if "https://lolospreadsheet.com/" in src:
        raise SystemExit("live twin href still present")
    if "Independent Index · 9,200+" not in src:
        raise SystemExit("Independent Index missing")
    if 'id="local"' not in src:
        raise SystemExit("#local missing")
    return src


def patch_coupons(src: str) -> str:
    if 'name="coupons-truth"' not in src:
        src = src.replace(
            "<head>",
            '<head>\n<meta name="coupons-truth" content="/data/coupons-truth.json">',
            1,
        )
    # bump title date signal
    src = src.replace(
        "<title>LoLoBuy Coupons 2026 &amp; Working Codes</title>",
        "<title>LoLoBuy Coupons 2026 — Working Codes · Updated 26 Oct</title>",
    )
    src = src.replace(
        'content="Working LoLoBuy coupon codes for 2026 plus invite 2pgzy. Register at lolobuy.com with inviteCode=2pgzy."',
        'content="Working LoLoBuy coupon codes for 2026 (updated 26 Oct 2026) plus invite 2pgzy. Truth JSON at /data/coupons-truth.json. Register at lolobuy.com with inviteCode=2pgzy."',
    )
    faq_ld = (
        '<script type="application/ld+json">'
        '{"@context":"https://schema.org","@type":"FAQPage","mainEntity":['
        '{"@type":"Question","name":"What is the LoLoBuy invite code 2pgzy?","acceptedAnswer":{"@type":"Answer","text":"2pgzy is the LoLoBuy inviteCode used on lolobuy.com register. Status on this desk is confirm_live — re-check in-app the morning you pay. Truth JSON: /data/coupons-truth.json."}},'
        '{"@type":"Question","name":"Where should LoLoBuy coupon queries land?","acceptedAnswer":{"@type":"Answer","text":"On bestlolobuyspreadsheet.com/guides/coupons/. Thin /coupons/ and /coupons.html redirect here. Twin lolospreadsheet.com already 301s to this hub."}},'
        '{"@type":"Question","name":"Are World Cup / CenturyPay promos still live?","acceptedAnswer":{"@type":"Answer","text":"Those announcement windows were June–July 2026. Treat as historical unless still visible in your LoLoBuy wallet. Always confirm_live before checkout."}}'
        "]}"
        "</script>"
    )
    if '"@type":"FAQPage"' not in src:
        src = src.replace("</head>", faq_ld + "\n</head>", 1)

    callout = """
  <div class="truth-callout" style="background:#fff6e8;border:1px solid #f3d7a3;border-radius:12px;padding:14px 16px;margin:16px 0">
    <strong>Coupons truth · 26 Oct 2026</strong>
    <p>Primary invite <code>2pgzy</code> status <strong>confirm_live</strong>. Machine-readable: <a href="/data/coupons-truth.json">/data/coupons-truth.json</a>. Finds moat: <a href="/finds-dataset/">/finds-dataset/</a>. Twin <code>lolospreadsheet.com</code> already 301 → this hub — do not chase coupons there.</p>
  </div>
"""
    if "Coupons truth · 26 Oct 2026" not in src:
        src = src.replace(
            "<h2>Lolobuy Coupons &amp; Invite Code</h2>",
            "<h2>Lolobuy Coupons &amp; Invite Code</h2>\n" + callout,
            1,
        )
    src = src.replace(
        "Sister country hosts stay separate files — no 301. Copy reviewed 2 Oct 2026.",
        "Twin lolospreadsheet.com already 301→this hub. No country spreadsheet desks. Copy reviewed 26 Oct 2026.",
    )
    return src


def write_jsons() -> None:
    data = ROOT / "data"
    data.mkdir(parents=True, exist_ok=True)
    truth = {
        "brand": "LoloBuy",
        "host": "bestlolobuyspreadsheet.com",
        "last_verified": "2026-10-26",
        "platform_opt": "lolobuy-platform-20261026",
        "verify_on": "lolobuy.com register / wallet — confirm before pay",
        "update_cadence": "Coupons page copy + JSON stamped when invite/offer changes (target weekly)",
        "serp_note": "Brand folder URLs + /guides/coupons/ carry clicks; homepage needs Independent Index · 9,200+ SERP signal. Twin lolospreadsheet.com already 301→hub.",
        "offers": [
            {
                "id": "lolobuy-invite-2pgzy",
                "type": "invite_ref",
                "label": "Invite code 2pgzy",
                "code": "2pgzy",
                "value_claim": "Register inviteCode on lolobuy.com — gifts/wallet vary; confirm_live after register",
                "status": "confirm_live",
                "expires_on": None,
                "expires_note": "No fixed expiry promised by this desk — re-confirm in-app the morning you pay",
                "applies_to": "LoLoBuy register / invite field",
                "exclusions": ["This hub is not checkout", "Stacking rules official-only"],
                "source": "https://bestlolobuyspreadsheet.com/guides/coupons/",
                "last_verified": "2026-10-26",
            },
            {
                "id": "lolobuy-centurypay-fee-archive",
                "type": "payment_promo",
                "label": "CenturyPay fee discount archive",
                "code": None,
                "value_claim": "Credit-card fee 4% → 3.5% (Jun 30–Jul 30 2026 window) — historical unless still in wallet",
                "status": "historical",
                "expires_on": "2026-07-30",
                "source": "https://bestlolobuyspreadsheet.com/guides/coupons/",
                "last_verified": "2026-10-26",
            },
            {
                "id": "lolobuy-worldcup-ship10-archive",
                "type": "shipping_promo",
                "label": "World Cup Carnival 10% shipping (US/CA/MX) archive",
                "code": None,
                "value_claim": "Automatic 10% shipping discount US/CA/MX Jun 22–Jul 21 2026 — historical unless still in wallet",
                "status": "historical",
                "expires_on": "2026-07-21",
                "source": "https://bestlolobuyspreadsheet.com/guides/coupons/",
                "last_verified": "2026-10-26",
            },
        ],
    }
    finds = {
        "schema": "seo-factory.finds-dataset.v1",
        "brand": "LoloBuy",
        "host": "bestlolobuyspreadsheet.com",
        "last_verified": "2026-10-26",
        "generated_at": "2026-10-26T19:05:00Z",
        "row_count": 9200,
        "row_count_display": "9,200+",
        "update_frequency": "Catalog cards refresh continuously; public dataset stamp reviewed at least weekly.",
        "qc_field": "qc_photo",
        "price_fields": ["price_cny", "price_usd_approx", "price_display"],
        "anti_sheet_note": "Public, citable row counts + dated category proofs — not another opaque Google Sheet dump. Coupon intent still lives on /guides/coupons/.",
        "platform_opt": "lolobuy-platform-20261026",
        "hub_role": "brand_hub_only_no_country_desks",
        "twin_note": "lolospreadsheet.com already 301→bestlolobuyspreadsheet.com (Phase A); do not revive",
        "endpoints": {
            "html": "https://bestlolobuyspreadsheet.com/finds-dataset/",
            "json": "https://bestlolobuyspreadsheet.com/data/finds-dataset.json",
            "coupons_truth": "https://bestlolobuyspreadsheet.com/data/coupons-truth.json",
            "catalog": "https://w2clinks.com/spreadsheet/lolobuy/",
            "hub": "https://bestlolobuyspreadsheet.com/",
        },
        "sitemap_policy": "Sitemap lastmod for /finds-dataset/, /guides/coupons/ and money URLs bumps when this stamp changes.",
        "sample_skus": [
            {
                "sku": "cat_sneakers",
                "title": "Sneakers & Shoes category proof (live catalog)",
                "price_cny": None,
                "price_display": "see catalog",
                "category_hint": "SNEAKERS",
                "source_url": "https://w2clinks.com/spreadsheet/lolobuy/",
                "qc_photo": False,
                "last_verified": "2026-10-26",
            },
            {
                "sku": "brand_nike",
                "title": "Nike brand QC rows (ranked on this hub)",
                "price_cny": None,
                "price_display": "see /brand/nike/",
                "category_hint": "NIKE",
                "source_url": "https://bestlolobuyspreadsheet.com/brand/nike/",
                "qc_photo": True,
                "last_verified": "2026-10-26",
            },
            {
                "sku": "cat_jacket",
                "title": "Jackets & Coats category proof (live catalog)",
                "price_cny": None,
                "price_display": "see catalog",
                "category_hint": "JACKET",
                "source_url": "https://w2clinks.com/spreadsheet/lolobuy/",
                "qc_photo": False,
                "last_verified": "2026-10-26",
            },
            {
                "sku": "brand_moncler",
                "title": "Moncler brand QC rows (ranked on this hub)",
                "price_cny": None,
                "price_display": "see /brand/moncler/",
                "category_hint": "MONCLER",
                "source_url": "https://bestlolobuyspreadsheet.com/brand/moncler/",
                "qc_photo": True,
                "last_verified": "2026-10-26",
            },
        ],
    }
    (data / "coupons-truth.json").write_text(json.dumps(truth, indent=2) + "\n", encoding="utf-8")
    (data / "finds-dataset.json").write_text(json.dumps(finds, indent=2) + "\n", encoding="utf-8")


def write_dataset_html() -> None:
    html = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>LoLoBuy Finds Dataset — 9,200+ Rows, Category Proofs &amp; last_verified</title>
<meta name="description" content="Provable LoLoBuy spreadsheet dataset: 9,200+ rows, weekly freshness stamp, category proofs. Independent Index on bestlolobuyspreadsheet.com — not a Google Sheet dump. Coupons stay on /guides/coupons/.">
<link rel="canonical" href="https://bestlolobuyspreadsheet.com/finds-dataset/">
<meta name="robots" content="index,follow">
<meta property="og:title" content="LoLoBuy Finds Dataset — Independent Index · 9,200+">
<meta property="og:description" content="9,200+ indexed finds with last_verified=2026-10-26. Public JSON + category proofs. Coupon truth is a separate JSON.">
<meta property="og:url" content="https://bestlolobuyspreadsheet.com/finds-dataset/">
<meta property="og:type" content="article">
<meta property="article:modified_time" content="2026-10-26">
<script type="application/ld+json">{"@context":"https://schema.org","@type":"Dataset","name":"LoLoBuy spreadsheet finds dataset","description":"Public row counts, update frequency and category proofs for the independent LoLoBuy spreadsheet hub.","url":"https://bestlolobuyspreadsheet.com/finds-dataset/","creator":{"@type":"Organization","name":"LoLoBuy Spreadsheet"},"dateModified":"2026-10-26","distribution":[{"@type":"DataDownload","encodingFormat":"application/json","contentUrl":"https://bestlolobuyspreadsheet.com/data/finds-dataset.json"},{"@type":"DataDownload","encodingFormat":"application/json","contentUrl":"https://bestlolobuyspreadsheet.com/data/coupons-truth.json"}],"variableMeasured":["sku","title","price","qc_photo","last_verified"]}</script>
<style>
:root{--acc:#FF9F00;--ink:#0a0a0a;--mute:#57534e;--line:#e7e5e4;--bg:#fafaf9;--ok:#166534;--okbg:#f0fdf4}
*{box-sizing:border-box}body{margin:0;font-family:Georgia,"Times New Roman",serif;color:var(--ink);background:#fff;line-height:1.7}
.top{border-bottom:1px solid var(--line);background:#fff;position:sticky;top:0;z-index:5}
.wrap{max-width:860px;margin:0 auto;padding:0 20px}
.top .wrap{display:flex;gap:16px;align-items:center;min-height:56px;flex-wrap:wrap}
.brand{font-weight:700;text-decoration:none;color:var(--ink);font-family:system-ui,sans-serif;font-size:15px}
.nav a{margin-left:12px;text-decoration:none;color:var(--mute);font-family:system-ui,sans-serif;font-size:14px}
.nav a:hover,.nav a.on{color:var(--acc)}
.hero{padding:40px 0 16px;background:linear-gradient(180deg,#fff6e8 0%,#fff 72%)}
.eyebrow{font-family:system-ui,sans-serif;font-size:12px;letter-spacing:.08em;text-transform:uppercase;color:var(--acc);font-weight:700}
h1{font-size:clamp(28px,4vw,40px);line-height:1.2;margin:10px 0}
.lead{font-size:18px;color:var(--mute);max-width:42em}
.stamp{display:inline-flex;align-items:center;gap:8px;font-family:system-ui,sans-serif;font-size:13px;background:var(--okbg);color:var(--ok);border:1px solid #bbf7d0;border-radius:999px;padding:6px 12px;margin-top:12px}
.stamp time{font-weight:700}
article{padding:8px 0 56px}
article h2{font-size:24px;margin:1.6em 0 .5em}
.stats{display:grid;grid-template-columns:repeat(auto-fit,minmax(140px,1fr));gap:12px;margin:1.2em 0}
.stat{background:var(--bg);border:1px solid var(--line);border-radius:12px;padding:14px 16px}
.stat b{display:block;font-family:system-ui,sans-serif;font-size:22px;letter-spacing:-.02em}
.stat span{font-family:system-ui,sans-serif;font-size:12px;color:var(--mute)}
.box{background:var(--bg);border:1px solid var(--line);border-radius:12px;padding:18px 20px;margin:1.2em 0}
table{width:100%;border-collapse:collapse;font-family:system-ui,sans-serif;font-size:13.5px;margin:1em 0}
th,td{border:1px solid var(--line);padding:10px 12px;text-align:left;vertical-align:top}
th{background:var(--bg);font-size:12px;text-transform:uppercase;letter-spacing:.04em;color:var(--mute)}
.btn{display:inline-block;background:var(--acc);color:#fff;text-decoration:none;padding:12px 18px;border-radius:10px;font-family:system-ui,sans-serif;font-weight:700;margin:4px 8px 4px 0}
.btn.ghost{background:#fff;color:var(--acc);border:1px solid var(--acc)}
footer{border-top:1px solid var(--line);padding:28px 0;color:var(--mute);font-size:14px;font-family:system-ui,sans-serif}
a{color:var(--acc)}
</style>
</head>
<body>
<header class="top"><div class="wrap">
  <a class="brand" href="/">LoLoBuy Spreadsheet</a>
  <nav class="nav">
    <a href="/">Home</a>
    <a href="/guides/coupons/">Coupons</a>
    <a href="/guides/qc/">QC</a>
    <a href="/finds-dataset/" class="on">Dataset</a>
    <a href="/guides/is-lolobuy-legit/">Legit?</a>
  </nav>
</div></header>
<section class="hero"><div class="wrap">
  <div class="eyebrow">LoLoBuy Spreadsheet · Independent Index · brand hub</div>
  <h1>LoLoBuy finds dataset</h1>
  <p class="lead">Public row counts, update frequency and dated category proofs — so this hub is not “just another Sheet clone.” Coupon stacking stays on <a href="/guides/coupons/">/guides/coupons/</a>. No country spreadsheet desks for this brand. Twin <code>lolospreadsheet.com</code> already 301 → here.</p>
  <div class="stamp">last_verified <time datetime="2026-10-26">2026-10-26</time> · 9,200+ rows · platform_opt=lolobuy-platform-20261026</div>
</div></section>
<article class="wrap">
<div class="stats">
  <div class="stat"><b>9,200+</b><span>Indexed finds (hub hero)</span></div>
  <div class="stat"><b>weekly</b><span>Target stamp cadence</span></div>
  <div class="stat"><b>Coupons</b><span>Separate truth JSON</span></div>
  <div class="stat"><b>Hub-only</b><span>No country desks</span></div>
</div>

<div class="box">
  <h2 style="margin-top:0;font-size:20px">Why this page exists</h2>
  <p>GSC for this host leans <strong>brand folders</strong> (Nike / LV / Moncler) plus <code>/guides/coupons/</code> and shipping. Spreadsheet / Independent Index queries still need a falsifiable catalog claim: how many rows, when the stamp moved, and which category proofs back the count.</p>
  <p><a class="btn" href="/data/finds-dataset.json">Download finds-dataset.json</a>
     <a class="btn ghost" href="/data/coupons-truth.json">Coupons truth JSON</a>
     <a class="btn ghost" href="/guides/coupons/">Coupon codes</a>
     <a class="btn ghost" href="https://w2clinks.com/spreadsheet/lolobuy/" rel="noopener">Open catalog</a></p>
</div>

<h2>Category / brand proofs</h2>
<table>
  <thead><tr><th>Proof</th><th>Hint</th><th>last_verified</th></tr></thead>
  <tbody>
    <tr><td>Sneakers &amp; Shoes</td><td>SNEAKERS</td><td>2026-10-26</td></tr>
    <tr><td>Nike brand QC rows</td><td>NIKE · /brand/nike/</td><td>2026-10-26</td></tr>
    <tr><td>Jackets &amp; Coats</td><td>JACKET</td><td>2026-10-26</td></tr>
    <tr><td>Moncler brand QC rows</td><td>MONCLER · /brand/moncler/</td><td>2026-10-26</td></tr>
  </tbody>
</table>

<div class="box">
  <h2 style="margin-top:0;font-size:20px">Hub vs country desk</h2>
  <p><strong>Brand hub = bestlolobuyspreadsheet.com.</strong> Portfolio inventory lists zero LoloBuy country spreadsheet desks. Mixed geo impressions do not authorize a dest-country skin. Twin <code>lolospreadsheet.com</code> already 301 → this hub (Phase A) — do not revive.</p>
</div>
</article>
<footer><div class="wrap">Independent resource. Not affiliated with lolobuy.com. platform_opt=lolobuy-platform-20261026.</div></footer>
</body>
</html>
"""
    d = ROOT / "finds-dataset"
    d.mkdir(parents=True, exist_ok=True)
    (d / "index.html").write_text(html, encoding="utf-8")


def write_misc() -> None:
    (ROOT / "llms.txt").write_text(
        """# LoLoBuy Spreadsheet (bestlolobuyspreadsheet.com)

> Independent Index · 9,200+ QC finds. Brand hub only — no country spreadsheet desks.

- Hub: https://bestlolobuyspreadsheet.com/
- Spreadsheet: https://bestlolobuyspreadsheet.com/spreadsheet/
- Coupons (money): https://bestlolobuyspreadsheet.com/guides/coupons/
- Coupons truth JSON: https://bestlolobuyspreadsheet.com/data/coupons-truth.json
- Finds dataset: https://bestlolobuyspreadsheet.com/finds-dataset/
- Dataset JSON: https://bestlolobuyspreadsheet.com/data/finds-dataset.json
- QC guide: https://bestlolobuyspreadsheet.com/guides/qc/
- Shipping: https://bestlolobuyspreadsheet.com/guides/shipping/
- Legit: https://bestlolobuyspreadsheet.com/guides/is-lolobuy-legit/

## Twin / sunset
- lolospreadsheet.com → already 301 to this hub (Phase A). Do not revive.
- No keep country desks. Do not invent new country spreadsheet TLDs.
- Thin /coupons/ and /coupons.html → /guides/coupons/

## Official
- https://www.lolobuy.com/ (checkout / register; invite 2pgzy confirm_live)

platform_opt=lolobuy-platform-20261026
last_verified=2026-10-26
""",
        encoding="utf-8",
    )

    (ROOT / "sitemap.xml").write_text(
        """<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url><loc>https://bestlolobuyspreadsheet.com/</loc><lastmod>2026-10-26</lastmod><changefreq>weekly</changefreq></url>
  <url><loc>https://bestlolobuyspreadsheet.com/spreadsheet/</loc><lastmod>2026-10-26</lastmod><changefreq>weekly</changefreq></url>
  <url><loc>https://bestlolobuyspreadsheet.com/guides/coupons/</loc><lastmod>2026-10-26</lastmod><changefreq>weekly</changefreq></url>
  <url><loc>https://bestlolobuyspreadsheet.com/finds-dataset/</loc><lastmod>2026-10-26</lastmod><changefreq>weekly</changefreq></url>
  <url><loc>https://bestlolobuyspreadsheet.com/data/finds-dataset.json</loc><lastmod>2026-10-26</lastmod><changefreq>weekly</changefreq></url>
  <url><loc>https://bestlolobuyspreadsheet.com/data/coupons-truth.json</loc><lastmod>2026-10-26</lastmod><changefreq>weekly</changefreq></url>
  <url><loc>https://bestlolobuyspreadsheet.com/guides/qc/</loc><lastmod>2026-10-26</lastmod><changefreq>weekly</changefreq></url>
  <url><loc>https://bestlolobuyspreadsheet.com/guides/shipping/</loc><lastmod>2026-10-26</lastmod><changefreq>weekly</changefreq></url>
  <url><loc>https://bestlolobuyspreadsheet.com/guides/is-lolobuy-legit/</loc><lastmod>2026-10-26</lastmod><changefreq>monthly</changefreq></url>
  <url><loc>https://bestlolobuyspreadsheet.com/brand/nike/</loc><lastmod>2026-10-26</lastmod><changefreq>weekly</changefreq></url>
  <url><loc>https://bestlolobuyspreadsheet.com/brand/louis-vuitton/</loc><lastmod>2026-10-26</lastmod><changefreq>weekly</changefreq></url>
  <url><loc>https://bestlolobuyspreadsheet.com/brand/moncler/</loc><lastmod>2026-10-26</lastmod><changefreq>weekly</changefreq></url>
  <url><loc>https://bestlolobuyspreadsheet.com/llms.txt</loc><lastmod>2026-10-26</lastmod><changefreq>monthly</changefreq></url>
</urlset>
""",
        encoding="utf-8",
    )

    deploy_dir = ROOT / "_deploy"
    deploy_dir.mkdir(parents=True, exist_ok=True)
    (deploy_dir / "thin-page-redirects.conf").write_text(
        """# Platform opt 2026-10-26: coupons aliases + public JSON/dataset
# Keep Step 3 /shipping/ noindex behavior on the HTML itself; do not revive Phase A twin.
location = /coupons.html { return 301 https://bestlolobuyspreadsheet.com/guides/coupons/; }
location = /coupons/ { return 301 https://bestlolobuyspreadsheet.com/guides/coupons/; }
location = /coupons { return 301 https://bestlolobuyspreadsheet.com/guides/coupons/; }
location = /lolobuy-coupons/ { return 301 https://bestlolobuyspreadsheet.com/guides/coupons/; }
location = /lolobuy-coupon/ { return 301 https://bestlolobuyspreadsheet.com/guides/coupons/; }

location = /data/finds-dataset.json {
  default_type application/json;
  add_header Cache-Control "public, max-age=300";
  alias /www/wwwroot/bestlolobuyspreadsheet.com/data/finds-dataset.json;
}
location = /data/coupons-truth.json {
  default_type application/json;
  add_header Cache-Control "public, max-age=300";
  alias /www/wwwroot/bestlolobuyspreadsheet.com/data/coupons-truth.json;
}
location ^~ /finds-dataset/ {
  try_files $uri $uri/ /finds-dataset/index.html;
}
""",
        encoding="utf-8",
    )

    (ROOT / "HOME-PATCH.md").write_text(
        """# HOME patch notes — bestlolobuyspreadsheet.com

Surgical on ranked CMS homepage (title / CTAs / `#local` / nav / footer / twin narrative).
Do **not** wholesale overwrite with leftover Georgia dest skin in `overlay/index.html`.
Publish only `index.html.platform-patched`.
Brand hub only — **no** keep country desks. Twin `lolospreadsheet.com` already 301 → hub (Phase A) — do not revive.
""",
        encoding="utf-8",
    )

    (ROOT / "DEPLOY-PLATFORM.md").write_text(
        """# Deploy — LoloBuy platform opt (2026-10-26)

Origin: Baota host used by portfolio desks.  
Root: `/www/wwwroot/bestlolobuyspreadsheet.com`

## GUARDS

- **Do not** rsync leftover Georgia dest `overlay/index.html` over the ranked CMS homepage — publish only `index.html.platform-patched`.
- **Do not** revive Phase A twin `lolospreadsheet.com` (already 301 → hub).
- Do not invent new country spreadsheet domains.
- Hub must **not** link the sunset twin as a live SOP desk.

## Files to push

```bash
HUB=/www/wwwroot/bestlolobuyspreadsheet.com
LOCAL=sites/bestlolobuyspreadsheet.com/overlay
BAK=/www/backup/lolobuy-platform-$(date +%Y%m%d-%H%M%S)

mkdir -p "$BAK"
cp -a "$HUB/index.html" "$HUB/sitemap.xml" "$HUB/llms.txt" "$BAK/" 2>/dev/null || true
cp -a "$HUB/guides/coupons" "$BAK/guides-coupons" 2>/dev/null || true

cp "$LOCAL/index.html.platform-patched" "$HUB/index.html"
mkdir -p "$HUB/guides/coupons"
cp "$LOCAL/guides/coupons/index.html" "$HUB/guides/coupons/index.html"
rsync -av "$LOCAL/finds-dataset/" "$HUB/finds-dataset/"
mkdir -p "$HUB/data"
cp "$LOCAL/data/coupons-truth.json" "$LOCAL/data/finds-dataset.json" "$HUB/data/"
cp "$LOCAL/llms.txt" "$LOCAL/sitemap.xml" "$HUB/"

mkdir -p /www/server/panel/vhost/nginx/extension/bestlolobuyspreadsheet.com
cp "$LOCAL/_deploy/thin-page-redirects.conf" \\
  /www/server/panel/vhost/nginx/extension/bestlolobuyspreadsheet.com/thin-page-redirects.conf
nginx -t && nginx -s reload
```

## GSC

Submit `https://bestlolobuyspreadsheet.com/sitemap.xml` after deploy.

## Verify

- `/` title contains Independent Index · 9,200+
- Hero CTAs Spreadsheet / Coupons / Dataset / Register; `#local` money URLs ≤6; no live twin href to lolospreadsheet.com
- `/guides/coupons/` has truth callout + 26 Oct 2026 + FAQ-LD
- `/data/*.json` + `/finds-dataset/` + `/llms.txt` → 200
- `/coupons/` · `/coupons.html` → 301 `/guides/coupons/`
- `lolospreadsheet.com/` still 301 → hub
""",
        encoding="utf-8",
    )


def main() -> None:
    src = LIVE.read_text(encoding="utf-8")
    patched = patch_home(src)
    (ROOT / "index.html.platform-patched").write_text(patched, encoding="utf-8")

    if not COUPONS_LIVE.is_file():
        raise SystemExit(f"missing {COUPONS_LIVE}")
    coupons_dir = ROOT / "guides" / "coupons"
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
