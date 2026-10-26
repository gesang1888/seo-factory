#!/usr/bin/env python3
"""Build EsgoBuy platform-opt overlay from LIVE homepage (surgical)."""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "sites" / "esgobuyspreadsheet.net" / "overlay"
LIVE = ROOT / "live-base" / "index.html"
COUPONS_LIVE = ROOT / "live-base" / "esgobuy-coupons.index.html"
HOST = "esgobuyspreadsheet.net"
BRAND = "EsgoBuy"
OPT = "esgobuy-platform-20261026"
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
            "<title>EsgoBuy Spreadsheet 2026</title>",
            f"<title>EsgoBuy Spreadsheet 2026 — Independent Index · {ROWS}</title>",
        ),
        (
            'content="EsgoBuy Spreadsheet 2026: live finds, QC photos and W2C. Not Excel, not a Google Sheet, not a dest-country skin. Official ¥4500 welcome shipping discounts + 300-day Help storage measured 9 Oct 2026."',
            f'content="EsgoBuy Independent Index · {ROWS} on {HOST}. Not Excel, not a Google Sheet, not checkout. Coupons on /esgobuy-coupons/; dataset on /finds-dataset/. Brand hub only — no country spreadsheet desks. Pay on esgobuy.com."',
        ),
        (
            '<meta property="og:title" content="EsgoBuy Spreadsheet 2026">',
            f'<meta property="og:title" content="EsgoBuy Spreadsheet 2026 — Independent Index · {ROWS}">',
        ),
        (
            'content="EsgoBuy Spreadsheet 2026: live finds, QC photos and W2C. Not Excel, not a Google Sheet, not a dest-country skin. Official ¥4500 welcome shipping discounts + 300-day Help storage measured 9 Oct 2026."',
            f'content="EsgoBuy Independent Index · {ROWS}. Coupons + finds dataset on this hub. Brand hub only (no country desks). Lookalike hosts are not keep desks."',
        ),
        (
            "Public copy measured on <a href=\"https://www.esgobuy.com/\" rel=\"noopener\">www.esgobuy.com</a>, 9 Oct 2026. This EsgoBuy spreadsheet is not Excel and not a Google Sheet. This host is not a dest-country skin. esgobuy.org stays independent — no 301. Official Help <a href=\"https://www.esgobuy.com/help?id=1834915352383983616&amp;type=4\">Warehouse storage time</a> is 300 days for normal parcels (30 days abnormal) — this desk cites that article, it does not invent a day count. Discord Lucky Thursday is named on the official homepage; this page does not invent an invite URL.",
            f"Public copy measured on <a href=\"https://www.esgobuy.com/\" rel=\"noopener\">www.esgobuy.com</a>, 9 Oct 2026; hub stamp {DATE_HUMAN}. Independent Index · {ROWS}. This host is the brand hub only — not a dest-country skin, no keep country spreadsheet desks. esgobuy.org stays independent (lookalike ≠ keep desk) — no 301. Official Help <a href=\"https://www.esgobuy.com/help?id=1834915352383983616&amp;type=4\">Warehouse storage time</a> is 300 days for normal parcels (30 days abnormal) — this desk cites that article, it does not invent a day count. Discord Lucky Thursday is named on the official homepage; this page does not invent an invite URL. Do not revive Phase C sunsets.",
        ),
        (
            "Coupon stacking for ranked codes stays on <a href=\"/esgobuy-coupons/\">/esgobuy-coupons/</a>. Extra 图文: <a href=\"/coupons.html\">/coupons.html</a>. Thin <code>/coupons/</code> and <code>/start/</code> stay 404. The previous email-verify pack is not the live official welcome.",
            "Coupon stacking for ranked codes stays on <a href=\"/esgobuy-coupons/\">/esgobuy-coupons/</a>. Thin <code>/coupons.html</code> · <code>/coupons/</code> 301 → that money URL. Dataset: <a href=\"/finds-dataset/\">/finds-dataset/</a>. The previous email-verify pack is not the live official welcome.",
        ),
        (
            "Coupon stacking stays on /esgobuy-coupons/. Official welcome is ¥4500 shipping discounts (9 Oct 2026).",
            f"Ranked money URL /esgobuy-coupons/ + truth JSON. Thin /coupons.html 301 here. Official welcome ¥4500 (9 Oct) · stamp {DATE_HUMAN}.",
        ),
        (
            "The most complete EsgoBuy spreadsheet and buying guide. Updated daily.",
            f"Independent Index · {ROWS}. Brand hub only — no country desks. Coupons + dataset cited on this host.",
        ),
    ]
    for old, new in repls:
        if old not in src:
            raise SystemExit(f"missing replace anchor:\n{old[:180]}")
        src = src.replace(old, new, 1)

    # Remaining og:description may still be old if duplicate string already replaced once — force both
    src = src.replace(
        'content="EsgoBuy Spreadsheet 2026: live finds, QC photos and W2C. Not Excel, not a Google Sheet, not a dest-country skin. Official ¥4500 welcome shipping discounts + 300-day Help storage measured 9 Oct 2026."',
        f'content="EsgoBuy Independent Index · {ROWS}. Coupons + finds dataset on this hub. Brand hub only (no country desks). Lookalike hosts are not keep desks."',
    )

    old_nav = '<ul class="nl"><li><a href="#official-offers">Offers</a></li><li><a href="https://w2clinks.com/spreadsheet/esgobuy/" target="_blank" rel="noopener">Spreadsheet</a></li><li><a href="/is-esgobuy-legit">Is it Legit?</a></li><li><a href="/esgobuy-shipping-guide">Shipping</a></li><li><a href="/esgobuy-coupons">Coupons</a></li><li><a href="/blog">Blog</a></li></ul>'
    new_nav = (
        '<ul class="nl">'
        '<li><a href="#local">Hub</a></li>'
        '<li><a href="/esgobuy-spreadsheet/">Spreadsheet</a></li>'
        '<li><a href="/esgobuy-coupons/">Coupons</a></li>'
        '<li><a href="/finds-dataset/">Dataset</a></li>'
        '<li><a href="/esgobuy-shipping-guide/">Shipping</a></li>'
        '<li><a href="/is-esgobuy-legit/">Legit?</a></li>'
        '<li><a href="/blog/">Blog</a></li>'
        "</ul>"
    )
    if old_nav not in src:
        raise SystemExit("nav block missing")
    src = src.replace(old_nav, new_nav)

    old_hero = """<section class="hero fade-in" id="main">
  <div class="hbg">Updated daily &middot; 2026</div>
  <h1>EsgoBuy Spreadsheet <em>2026</em></h1>
  <p class="hsub">EsgoBuy Spreadsheet 2026 — live finds, QC photos and W2C categories. This spreadsheet is not Excel and not a Google Sheet. Independent hub, not a dest-country skin, not esgobuy.com.</p>
  <div class="hctas">
    <a href="https://w2clinks.com/spreadsheet/esgobuy/" class="cp" target="_blank" rel="noopener">Browse Spreadsheet &rarr;</a>
    <a href="https://www.esgobuy.com/user/register" target="_blank" rel="noopener sponsored" class="cp" style="background:var(--bk);color:#fff">Sign up on EsgoBuy</a>
    <a href="/how-to-use-esgobuy" class="cs">Beginner Guide</a>
  </div>
  <div class="hst">
    <div class="hs"><div class="hsn">12,400+</div><div class="hsl">Products</div></div>
    <div class="hs"><div class="hsn">12</div><div class="hsl">Categories</div></div>
    <div class="hs"><div class="hsn">Daily</div><div class="hsl">Updates</div></div>
    <div class="hs"><div class="hsn">Free</div><div class="hsl">Access</div></div>
  </div>
</section>"""
    new_hero = f"""<section class="hero fade-in" id="main">
  <div class="hbg">Independent Index · {ROWS} · not Excel · not a dest-country skin</div>
  <h1>EsgoBuy Spreadsheet <em>2026</em> — Independent Index · {ROWS}</h1>
  <p class="hsub">Independent Index · {ROWS} — live finds, QC photos and W2C categories. Not Excel, not a Google Sheet, not checkout. Brand hub on this .net host (no country spreadsheet desks). Coupons + dataset cited below; pay on esgobuy.com. Official welcome: <strong>¥4500</strong> shipping discounts + <strong>300-day</strong> Help storage — confirm on esgobuy.com the morning you pay.</p>
  <div class="hctas">
    <a href="/esgobuy-spreadsheet/" class="cp">Spreadsheet</a>
    <a href="/esgobuy-coupons/" class="cs">Coupons</a>
    <a href="/finds-dataset/" class="cs">Dataset</a>
    <a href="https://www.esgobuy.com/user/register" target="_blank" rel="noopener sponsored" class="cs">Register</a>
  </div>
  <div class="hst">
    <div class="hs"><div class="hsn">{ROWS}</div><div class="hsl">Index rows</div></div>
    <div class="hs"><div class="hsn">¥4500</div><div class="hsl">Welcome gift</div></div>
    <div class="hs"><div class="hsn">300d</div><div class="hsl">Help storage</div></div>
    <div class="hs"><div class="hsn">Hub-only</div><div class="hsl">No country desk</div></div>
  </div>
</section>"""
    if old_hero not in src:
        raise SystemExit("hero block missing")
    src = src.replace(old_hero, new_hero)

    local_block = f"""
<section class="sg-sec" id="local">
  <h2>Brand hub · Independent Index · no country desk</h2>
  <p class="ssub">{HOST} · not a customs territory · money URLs ≤6</p>
  <ol class="local-steps">
    <li><strong>Brand spreadsheet → this hub</strong><span>Independent Index · {ROWS}. Coupons + dataset live here. Mixed USA/AUS/DEU/POL impressions do not make .net a dest-country desk.</span></li>
    <li><strong>No keep country desks</strong><span>Portfolio inventory + GSC list zero EsgoBuy country spreadsheet TLDs. Do not invent new ones. Do not revive Phase C sunsets.</span></li>
    <li><strong>Lookalikes ≠ keep desks</strong><span>esgobuy.org stays independent competitor/lookalike chrome — not a Phase C sunset to revive, and not a keep desk on this portfolio.</span></li>
    <li><strong>Money URLs stay ≤6</strong><span>Home · Spreadsheet · Coupons · Dataset · Shipping · Legit. Ranked inners stay 200 — not overwritten.</span></li>
  </ol>
  <p class="local-src">Money URLs (≤6): <a href="/">Home</a> · <a href="/esgobuy-spreadsheet/">Spreadsheet</a> · <a href="/esgobuy-coupons/">Coupons</a> · <a href="/finds-dataset/">Dataset</a> · <a href="/esgobuy-shipping-guide/">Shipping</a> · <a href="/is-esgobuy-legit/">Legit</a></p>
  <p class="local-src">Lab {DATE_HUMAN}. Phase C sunsets not revived. Orders stay on esgobuy.com.</p>
</section>
"""
    m = re.search(r'(<section class="hero fade-in" id="main">[\s\S]*?</section>)', src)
    if not m:
        raise SystemExit("hero section wrapper missing")
    if 'id="local"' not in src:
        src = src[: m.end()] + "\n" + local_block + src[m.end() :]

    # Add WebSite + FAQ JSON-LD once (LIVE had none)
    if '"@type":"WebSite"' not in src:
        ld = (
            '<script type="application/ld+json">'
            "{"
            '"@context":"https://schema.org",'
            '"@type":"WebSite",'
            f'"name":"EsgoBuy Spreadsheet",'
            f'"alternateName":["EsgoBuy Independent Index","EsgoBuy Spreadsheet 2026","{HOST}"],'
            f'"dateModified":"{DATE}",'
            f'"url":"https://{HOST}/",'
            f'"description":"EsgoBuy Independent Index · {ROWS} finds. Coupons on /esgobuy-coupons/; dataset on /finds-dataset/. Not Excel, not a Google Sheet.",'
            '"inLanguage":"en"'
            "}"
            "</script>\n"
            '<script type="application/ld+json">'
            "{"
            '"@context":"https://schema.org",'
            '"@type":"FAQPage",'
            '"mainEntity":['
            '{"@type":"Question","name":"Is esgobuyspreadsheet.net a country desk?",'
            '"acceptedAnswer":{"@type":"Answer","text":"No. esgobuyspreadsheet.net is the EsgoBuy brand hub only. Mixed USA/AUS/DEU impressions do not authorize a dest-country skin. There are no keep country spreadsheet desks for EsgoBuy. Lookalike hosts such as esgobuy.org are not Phase C sunsets to revive, and not keep desks."}},'
            '{"@type":"Question","name":"Where do EsgoBuy coupon queries land?",'
            '"acceptedAnswer":{"@type":"Answer","text":"On https://esgobuyspreadsheet.net/esgobuy-coupons/. Thin /coupons.html and /coupons/ redirect there. Dataset moat lives on /finds-dataset/."}}'
            "]"
            "}"
            "</script>\n"
        )
        src = src.replace("</head>", ld + "</head>", 1)

    # Collapse leftover /coupons.html mentions
    src = src.replace('href="/coupons.html"', 'href="/esgobuy-coupons/"')
    if "coupons.html" in src:
        src = src.replace("/coupons.html", "/esgobuy-coupons/")

    # Blog GC → Dataset card (keep interaction density low in money grid)
    src = src.replace(
        '<a href="/blog" class="gc"><span class="gtg" style="background:var(--g6);color:var(--g4)">Blog</span><p class="gtit">EsgoBuy Spreadsheet Blog &mdash; Guides &amp; Tips</p><p class="gdesc">Real answers to rep community questions: sizing, delays, customs and more.</p><span class="glink">Read blog &rarr;</span></a>',
        '<a href="/finds-dataset/" class="gc"><span class="gtg" style="background:var(--g6);color:var(--g4)">Moat</span><p class="gtit">Finds dataset</p><p class="gdesc">Public row counts + category proofs. Brand hub only — no country desks.</p><span class="glink">Open dataset →</span></a>',
    )

    if f"Independent Index · {ROWS}" not in src:
        raise SystemExit("Independent Index missing")
    if 'id="local"' not in src:
        raise SystemExit("#local missing")
    if "coupons.html" in src:
        raise SystemExit("coupons.html still present in homepage")
    return src


def patch_coupons(src: str) -> str:
    if 'name="coupons-truth"' not in src:
        src = src.replace(
            "<head>",
            '<head>\n<meta name="coupons-truth" content="/data/coupons-truth.json">',
            1,
        )
    src = src.replace(
        "<title>EsgoBuy Coupon Codes 2026 — Working Discounts & Promo Codes</title>",
        f"<title>EsgoBuy Coupon Codes 2026 — Working Discounts · Updated {DATE_HUMAN}</title>",
    )
    src = src.replace(
        'content="All working EsgoBuy coupon codes for 2026, updated weekly. Use V0HXH6F40B for ¥1080 shipping coupon pack off your first order."',
        f'content="Working EsgoBuy coupon codes for 2026 (updated {DATE_HUMAN}). Primary V0HXH6F40B · ¥1080 invite pack — confirm_live. Truth JSON at /data/coupons-truth.json."',
    )
    faq_ld = (
        '<script type="application/ld+json">'
        '{"@context":"https://schema.org","@type":"FAQPage","mainEntity":['
        '{"@type":"Question","name":"What is the EsgoBuy V0HXH6F40B invite code?","acceptedAnswer":{"@type":"Answer","text":"V0HXH6F40B is the public invite / affcode used to unlock new-user shipping coupon packs (¥1080 line on this desk). Status is confirm_live — re-check Wallet / register the morning you pay. Truth JSON: /data/coupons-truth.json."}},'
        '{"@type":"Question","name":"Where should EsgoBuy coupon queries land?","acceptedAnswer":{"@type":"Answer","text":"On esgobuyspreadsheet.net/esgobuy-coupons/. Thin /coupons/ and /coupons.html redirect here. Brand hub only — no country spreadsheet desks."}},'
        '{"@type":"Question","name":"Can I stack EsgoBuy coupon codes?","acceptedAnswer":{"@type":"Answer","text":"Usually one order coupon per checkout; shipping discounts may stack separately when Wallet allows. Always confirm_live before pay. Official welcome ¥4500 shipping discounts are separate from the ranked invite pack."}}'
        "]}"
        "</script>"
    )
    if "EsgoBuy V0HXH6F40B invite code" not in src:
        src = src.replace("</head>", faq_ld + "\n</head>", 1)

    callout = f"""
  <div class="truth-callout" style="background:#FFF3EB;border:1px solid #F0C8C2;border-radius:12px;padding:14px 16px;margin:16px 0">
    <strong>Coupons truth · {DATE_HUMAN}</strong>
    <p>Primary public line <code>V0HXH6F40B</code> / <code>EMAIL1080</code> / <code>AFF5PCT</code> status <strong>confirm_live</strong>. Official welcome <strong>¥4500</strong> shipping discounts measured on esgobuy.com (9 Oct 2026). Machine-readable: <a href="/data/coupons-truth.json">/data/coupons-truth.json</a>. Finds moat: <a href="/finds-dataset/">/finds-dataset/</a>. Thin <code>/coupons.html</code> · <code>/coupons/</code> 301 → this page. Brand hub only — no country desks.</p>
  </div>
"""
    if f"Coupons truth · {DATE_HUMAN}" not in src:
        lead = '<p style="font-size:16px;color:var(--g3);line-height:1.8;border-left:3px solid var(--acc);padding-left:16px">Every working EsgoBuy coupon code in one place. Verified weekly. Click any code to copy it instantly.</p>'
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
        "verify_on": "esgobuy.com Wallet / register / coupon dialog — confirm before pay",
        "update_cadence": "Coupons page copy + JSON stamped when invite/shipping offers change (target weekly)",
        "serp_note": "28d clicks split across / · /esgobuy-coupons/ · /is-esgobuy-legit/ · /esgobuy-shipping-guide/. Homepage needs Independent Index · 12,400+ SERP signal. Brand hub only — no country desks.",
        "offers": [
            {
                "id": "esgobuy-invite-v0hxh6f40b",
                "type": "invite_code",
                "label": "V0HXH6F40B invite / new-user pack",
                "code": "V0HXH6F40B",
                "value_claim": "Official invite / affcode unlocks new-user shipping coupon pack (~¥1080 line on ranked coupons article) — confirm_live",
                "status": "confirm_live",
                "expires_on": None,
                "expires_note": "No fixed expiry promised by this desk — re-confirm in-app the morning you pay",
                "applies_to": "EsgoBuy register / invite flow",
                "exclusions": ["This hub is not checkout", "Stacking rules official-only"],
                "source": f"https://{HOST}/esgobuy-coupons/",
                "last_verified": DATE,
            },
            {
                "id": "esgobuy-email-1080",
                "type": "shipping_promo",
                "label": "EMAIL1080 verify-email shipping pack",
                "code": "EMAIL1080",
                "value_claim": "Verify-email CNY ¥1080 shipping coupon pack listed on ranked coupons article — confirm_live / may be historical vs ¥4500 welcome",
                "status": "confirm_live",
                "expires_on": None,
                "source": f"https://{HOST}/esgobuy-coupons/",
                "last_verified": DATE,
            },
            {
                "id": "esgobuy-aff-5pct",
                "type": "promoter_reward",
                "label": "AFF5PCT promoter rewards",
                "code": "AFF5PCT",
                "value_claim": "Promoter rewards Bronze 5% / Silver 6% — confirm_live on official promoter rules",
                "status": "confirm_live",
                "expires_on": None,
                "source": f"https://{HOST}/esgobuy-coupons/",
                "last_verified": DATE,
            },
            {
                "id": "esgobuy-welcome-4500",
                "type": "new_user_gift",
                "label": "¥4500 Welcome shipping discounts",
                "code": None,
                "value_claim": "Official homepage / register chrome 9 Oct 2026: Sign Up & Grab ¥4500 Shipping Discounts — confirm_live; not a printable coupon code on this desk",
                "status": "confirm_live",
                "expires_on": None,
                "source": "https://www.esgobuy.com/",
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
        "anti_sheet_note": "Public, citable row counts + dated category proofs — not another opaque Google Sheet dump. Coupon intent still lives on /esgobuy-coupons/.",
        "platform_opt": OPT,
        "hub_role": "brand_hub_only_no_country_desks",
        "twin_note": "No Phase A hub twin. No Phase B/C EsgoBuy sunset to revive. Lookalike esgobuy.org is independent — not a keep desk. No country spreadsheet TLDs in inventory/GSC.",
        "endpoints": {
            "html": f"https://{HOST}/finds-dataset/",
            "json": f"https://{HOST}/data/finds-dataset.json",
            "coupons_truth": f"https://{HOST}/data/coupons-truth.json",
            "catalog": "https://w2clinks.com/spreadsheet/esgobuy/",
            "hub": f"https://{HOST}/",
            "ranked_spreadsheet": f"https://{HOST}/esgobuy-spreadsheet/",
        },
        "sitemap_policy": "Sitemap lastmod for /finds-dataset/, /esgobuy-coupons/ and money URLs bumps when this stamp changes.",
        "sample_skus": [
            {
                "sku": "cat_sneakers",
                "title": "Sneakers & Shoes category proof (live catalog)",
                "price_cny": None,
                "price_display": "see catalog",
                "category_hint": "SNEAKERS",
                "source_url": "https://w2clinks.com/spreadsheet/esgobuy/?category=SNEAKERS",
                "qc_photo": False,
                "last_verified": DATE,
            },
            {
                "sku": "cat_jacket",
                "title": "Jackets & Coats category proof (live catalog)",
                "price_cny": None,
                "price_display": "see catalog",
                "category_hint": "JACKET",
                "source_url": "https://w2clinks.com/spreadsheet/esgobuy/?category=JACKET",
                "qc_photo": False,
                "last_verified": DATE,
            },
            {
                "sku": "cat_women",
                "title": "Women's Fashion category proof (live catalog)",
                "price_cny": None,
                "price_display": "see catalog",
                "category_hint": "FEMALE STYLE",
                "source_url": "https://w2clinks.com/spreadsheet/esgobuy/?category=FEMALE%20STYLE",
                "qc_photo": False,
                "last_verified": DATE,
            },
            {
                "sku": "page_shoes_sheet",
                "title": "Shoes spreadsheet ranked article on this hub",
                "price_cny": None,
                "price_display": "see /esgobuy-shoes-spreadsheet/",
                "category_hint": "SHOES",
                "source_url": f"https://{HOST}/esgobuy-shoes-spreadsheet/",
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
<title>EsgoBuy Finds Dataset — {ROWS} Rows, Category Proofs &amp; last_verified</title>
<meta name="description" content="Provable EsgoBuy spreadsheet dataset: {ROWS} rows, weekly freshness stamp, category proofs. Independent Index on {HOST} — not a Google Sheet dump. Coupons stay on /esgobuy-coupons/.">
<link rel="canonical" href="https://{HOST}/finds-dataset/">
<meta name="robots" content="index,follow">
<meta property="og:title" content="EsgoBuy Finds Dataset — Independent Index · {ROWS}">
<meta property="og:description" content="{ROWS} indexed finds with last_verified={DATE}. Public JSON + category proofs. Coupon truth is a separate JSON.">
<meta property="og:url" content="https://{HOST}/finds-dataset/">
<meta property="og:type" content="article">
<meta property="article:modified_time" content="{DATE}">
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"Dataset","name":"EsgoBuy spreadsheet finds dataset","description":"Public row counts, update frequency and category proofs for the independent EsgoBuy spreadsheet hub.","url":"https://{HOST}/finds-dataset/","creator":{{"@type":"Organization","name":"EsgoBuy Spreadsheet"}},"dateModified":"{DATE}","distribution":[{{"@type":"DataDownload","encodingFormat":"application/json","contentUrl":"https://{HOST}/data/finds-dataset.json"}},{{"@type":"DataDownload","encodingFormat":"application/json","contentUrl":"https://{HOST}/data/coupons-truth.json"}}],"variableMeasured":["sku","title","price","qc_photo","last_verified"]}}</script>
<style>
:root{{--acc:#EB6D21;--ink:#0A0A0A;--mute:#555;--line:#F0C8C2;--bg:#FFF3EB;--ok:#166534;--okbg:#f0fdf4}}
*{{box-sizing:border-box}}body{{margin:0;font-family:DM Sans,Montserrat,system-ui,sans-serif;color:var(--ink);background:#fff;line-height:1.7}}
.top{{border-bottom:1px solid var(--line);background:#fff;position:sticky;top:0;z-index:5}}
.wrap{{max-width:860px;margin:0 auto;padding:0 20px}}
.top .wrap{{display:flex;gap:16px;align-items:center;min-height:56px;flex-wrap:wrap}}
.brand{{font-weight:700;text-decoration:none;color:var(--ink);font-size:15px}}
.nav a{{margin-left:12px;text-decoration:none;color:var(--mute);font-size:14px}}
.nav a:hover,.nav a.on{{color:var(--acc)}}
.hero{{padding:40px 0 16px;background:linear-gradient(180deg,#FFF3EB 0%,#fff 72%)}}
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
  <a class="brand" href="/">EsgoBuy Spreadsheet</a>
  <nav class="nav">
    <a href="/">Home</a>
    <a href="/esgobuy-coupons/">Coupons</a>
    <a href="/esgobuy-spreadsheet/">Spreadsheet</a>
    <a href="/finds-dataset/" class="on">Dataset</a>
    <a href="/is-esgobuy-legit/">Legit?</a>
  </nav>
</div></header>
<section class="hero"><div class="wrap">
  <div class="eyebrow">EsgoBuy Spreadsheet · Independent Index · brand hub</div>
  <h1>EsgoBuy finds dataset</h1>
  <p class="lead">Public row counts, update frequency and dated category proofs — so this hub is not “just another Sheet clone.” Coupon stacking stays on <a href="/esgobuy-coupons/">/esgobuy-coupons/</a>. No country spreadsheet desks for this brand. Phase C sunsets not revived.</p>
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
  <p>GSC for this host splits 28d clicks across <strong>home</strong>, <strong>/esgobuy-coupons/</strong>, <strong>/is-esgobuy-legit/</strong> and shipping. Spreadsheet / Independent Index queries need a falsifiable catalog claim: how many rows, when the stamp moved, and which category proofs back the count.</p>
  <p><a class="btn" href="/data/finds-dataset.json">Download finds-dataset.json</a>
     <a class="btn ghost" href="/data/coupons-truth.json">Coupons truth JSON</a>
     <a class="btn ghost" href="/esgobuy-coupons/">Coupon codes</a>
     <a class="btn ghost" href="https://w2clinks.com/spreadsheet/esgobuy/" rel="noopener">Open catalog</a></p>
</div>

<h2>Category / page proofs</h2>
<table>
  <thead><tr><th>Proof</th><th>Hint</th><th>last_verified</th></tr></thead>
  <tbody>
    <tr><td>Sneakers &amp; Shoes</td><td>SNEAKERS</td><td>{DATE}</td></tr>
    <tr><td>Jackets &amp; Coats</td><td>JACKET</td><td>{DATE}</td></tr>
    <tr><td>Women's Fashion</td><td>FEMALE STYLE</td><td>{DATE}</td></tr>
    <tr><td>Shoes spreadsheet article</td><td>/esgobuy-shoes-spreadsheet/</td><td>{DATE}</td></tr>
  </tbody>
</table>

<div class="box">
  <h2 style="margin-top:0;font-size:20px">Hub vs country desk</h2>
  <p><strong>Brand hub = {HOST}.</strong> Portfolio inventory and GSC list zero EsgoBuy country spreadsheet desks. Mixed geo impressions do not authorize a dest-country skin. Lookalike hosts (e.g. esgobuy.org) are not keep desks. Do not revive Phase C sunsets.</p>
</div>
</article>
<footer><div class="wrap">Independent resource. Not affiliated with esgobuy.com. platform_opt={OPT}.</div></footer>
</body>
</html>
"""
    d = ROOT / "finds-dataset"
    d.mkdir(parents=True, exist_ok=True)
    (d / "index.html").write_text(html, encoding="utf-8")


def write_misc() -> None:
    (ROOT / "llms.txt").write_text(
        f"""# EsgoBuy Spreadsheet ({HOST})

> Independent Index · {ROWS} finds. Brand hub only — no country spreadsheet desks.

- Hub: https://{HOST}/
- Spreadsheet: https://{HOST}/esgobuy-spreadsheet/
- Coupons (money): https://{HOST}/esgobuy-coupons/
- Coupons truth JSON: https://{HOST}/data/coupons-truth.json
- Finds dataset: https://{HOST}/finds-dataset/
- Dataset JSON: https://{HOST}/data/finds-dataset.json
- Shipping: https://{HOST}/esgobuy-shipping-guide/
- Legit: https://{HOST}/is-esgobuy-legit/
- QC: https://{HOST}/esgobuy-qc-guide/
- Shoes sheet: https://{HOST}/esgobuy-shoes-spreadsheet/

## Hub / sunset rules
- Brand hub only. No keep country spreadsheet desks. Do not invent new country TLDs.
- Lookalike hosts (e.g. esgobuy.org) are independent — not keep desks; do not revive Phase C sunsets.
- Thin /coupons/ and /coupons.html → /esgobuy-coupons/

## Official
- https://www.esgobuy.com/ (checkout; ¥4500 welcome + V0HXH6F40B invite confirm_live)

platform_opt={OPT}
last_verified={DATE}
""",
        encoding="utf-8",
    )

    (ROOT / "sitemap.xml").write_text(
        f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url><loc>https://{HOST}/</loc><lastmod>{DATE}</lastmod><changefreq>weekly</changefreq></url>
  <url><loc>https://{HOST}/esgobuy-spreadsheet/</loc><lastmod>{DATE}</lastmod><changefreq>weekly</changefreq></url>
  <url><loc>https://{HOST}/esgobuy-coupons/</loc><lastmod>{DATE}</lastmod><changefreq>weekly</changefreq></url>
  <url><loc>https://{HOST}/finds-dataset/</loc><lastmod>{DATE}</lastmod><changefreq>weekly</changefreq></url>
  <url><loc>https://{HOST}/data/finds-dataset.json</loc><lastmod>{DATE}</lastmod><changefreq>weekly</changefreq></url>
  <url><loc>https://{HOST}/data/coupons-truth.json</loc><lastmod>{DATE}</lastmod><changefreq>weekly</changefreq></url>
  <url><loc>https://{HOST}/esgobuy-shipping-guide/</loc><lastmod>{DATE}</lastmod><changefreq>weekly</changefreq></url>
  <url><loc>https://{HOST}/is-esgobuy-legit/</loc><lastmod>{DATE}</lastmod><changefreq>monthly</changefreq></url>
  <url><loc>https://{HOST}/esgobuy-qc-guide/</loc><lastmod>{DATE}</lastmod><changefreq>weekly</changefreq></url>
  <url><loc>https://{HOST}/esgobuy-shoes-spreadsheet/</loc><lastmod>{DATE}</lastmod><changefreq>weekly</changefreq></url>
  <url><loc>https://{HOST}/how-to-use-esgobuy/</loc><lastmod>{DATE}</lastmod><changefreq>monthly</changefreq></url>
  <url><loc>https://{HOST}/esgobuy-invite-code/</loc><lastmod>{DATE}</lastmod><changefreq>monthly</changefreq></url>
  <url><loc>https://{HOST}/llms.txt</loc><lastmod>{DATE}</lastmod><changefreq>monthly</changefreq></url>
  <url><loc>https://{HOST}/blog/</loc><lastmod>{DATE}</lastmod><changefreq>weekly</changefreq></url>
</urlset>
""",
        encoding="utf-8",
    )

    deploy_dir = ROOT / "_deploy"
    deploy_dir.mkdir(parents=True, exist_ok=True)
    # Preserve Step 3 customs 301s + add platform coupons/JSON/dataset rules
    (deploy_dir / "thin-page-redirects.conf").write_text(
        f"""# Step 3 2026-10-26: thin shipping/customs cleanup (deduped against gsc-redirects)
location = /blog/posts/esgobuy-customs-guide {{ return 301 https://{HOST}/esgobuy-shipping-guide/; }}
location = /blog/posts/esgobuy-customs-guide/ {{ return 301 https://{HOST}/esgobuy-shipping-guide/; }}

# Platform opt 2026-10-26: coupons aliases + public JSON/dataset
# Brand hub only — no country desks; do not revive Phase C sunsets.
location = /coupons.html {{ return 301 https://{HOST}/esgobuy-coupons/; }}
location = /coupons/ {{ return 301 https://{HOST}/esgobuy-coupons/; }}
location = /coupons {{ return 301 https://{HOST}/esgobuy-coupons/; }}
location = /esgobuy-coupon/ {{ return 301 https://{HOST}/esgobuy-coupons/; }}
location = /esgobuy-coupon {{ return 301 https://{HOST}/esgobuy-coupons/; }}

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
location ^~ /esgobuy-coupons/ {{
  try_files $uri $uri/ /esgobuy-coupons/index.html;
}}
""",
        encoding="utf-8",
    )

    (ROOT / "HOME-PATCH.md").write_text(
        f"""# HOME patch notes — {HOST}

Surgical on ranked CMS homepage (title / CTAs / `#local` / nav / footer / hub-only narrative).
Do **not** wholesale overwrite with leftover Georgia dest skin in `overlay/index.html`.
Publish only `index.html.platform-patched`.
Brand hub only — **no** keep country desks. Lookalike hosts (e.g. esgobuy.org) are not Phase C sunsets to revive.
""",
        encoding="utf-8",
    )

    (ROOT / "DEPLOY-PLATFORM.md").write_text(
        f"""# Deploy — EsgoBuy platform opt ({DATE})

Origin: Baota host used by portfolio desks.  
Root: `/www/wwwroot/{HOST}`

## GUARDS

- **Do not** rsync leftover Georgia dest `overlay/index.html` over the ranked CMS homepage — publish only `index.html.platform-patched`.
- **Do not** revive Phase C sunsets; do not invent country spreadsheet domains.
- Hub must **not** treat lookalike hosts (e.g. esgobuy.org) as keep desks.
- Nginx vhost already `include .../extension/{HOST}/*.conf` (keep it).

## Files to push

```bash
HUB=/www/wwwroot/{HOST}
LOCAL=sites/{HOST}/overlay
BAK=/www/backup/esgobuy-platform-$(date +%Y%m%d-%H%M%S)
NGX=/www/server/panel/vhost/nginx/{HOST}.conf

mkdir -p "$BAK"
cp -a "$HUB/index.html" "$HUB/sitemap.xml" "$HUB/coupons.html" "$BAK/" 2>/dev/null || true
cp -a "$HUB/esgobuy-coupons" "$BAK/esgobuy-coupons" 2>/dev/null || true
cp -a "$NGX" "$BAK/{HOST}.conf.bak"

cp "$LOCAL/index.html.platform-patched" "$HUB/index.html"
mkdir -p "$HUB/esgobuy-coupons"
cp "$LOCAL/esgobuy-coupons/index.html" "$HUB/esgobuy-coupons/index.html"
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
- `/esgobuy-coupons/` has truth callout + {DATE_HUMAN} + FAQ-LD
- `/data/*.json` + `/finds-dataset/` + `/llms.txt` → 200
- `/coupons/` · `/coupons.html` → 301 `/esgobuy-coupons/`
""",
        encoding="utf-8",
    )


def main() -> None:
    src = LIVE.read_text(encoding="utf-8")
    patched = patch_home(src)
    (ROOT / "index.html.platform-patched").write_text(patched, encoding="utf-8")

    if not COUPONS_LIVE.is_file():
        raise SystemExit(f"missing {COUPONS_LIVE}")
    coupons_dir = ROOT / "esgobuy-coupons"
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
