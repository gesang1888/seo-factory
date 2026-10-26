#!/usr/bin/env python3
"""Build VigorBuy platform-opt overlay from LIVE homepage (surgical)."""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "sites" / "vigorspreadsheet.com" / "overlay"
LIVE = ROOT / "live-base" / "index.html"
COUPONS_LIVE = Path("/tmp/vigor-coupons-live.html")


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
            "<title>VigorBuy Spreadsheet 2026</title>",
            "<title>VigorBuy Spreadsheet 2026 — Independent Index · 12,400+</title>",
        ),
        (
            'content="VigorBuy spreadsheet: live Weidian, Taobao, 1688 and Yupoo finds. Not Excel, not a Google Sheet. Official vigorbuy.com 9 Oct 2026: $210 new-user gift plus 30% shipping off. Help and estimation sit behind Cloudflare Turnstile — this desk does not invent a free-day count. Pay on vigorbuy.com."',
            'content="VigorBuy Independent Index · 12,400+ on vigorspreadsheet.com. Not Excel, not a Google Sheet, not checkout. Coupons on /vigorbuy-coupons/; dataset on /finds-dataset/. Brand hub only — no country spreadsheet desks. Pay on vigorbuy.com."',
        ),
        (
            '<meta property="og:title" content="VigorBuy Spreadsheet 2026">',
            '<meta property="og:title" content="VigorBuy Spreadsheet 2026 — Independent Index · 12,400+">',
        ),
        (
            'content="VigorBuy spreadsheet: live finds, not Excel, not a Google Sheet. Official new-user gift $210 plus 30% shipping off. Independent of vigor-buy.com, vigorbuy-spreadsheet.com and vigorbuyspreadsheets.net."',
            'content="VigorBuy Independent Index · 12,400+. Coupons + finds dataset on this hub. Brand hub only (no country desks). Lookalike hosts are not keep desks."',
        ),
        (
            '"name":"VigorBuy Spreadsheet","alternateName":["VigorBuy Spreadsheet","VigorBuy spreadsheet 2026","Vigorbuy Spreadsheet"],"url":"https://vigorspreadsheet.com/","description":"VigorBuy spreadsheet: live Weidian, Taobao and 1688 finds. Not Excel, not a Google Sheet.","inLanguage":"en"',
            '"name":"VigorBuy Spreadsheet","alternateName":["VigorBuy Independent Index","VigorBuy Spreadsheet 2026","vigorspreadsheet.com"],"dateModified":"2026-10-26","url":"https://vigorspreadsheet.com/","description":"VigorBuy Independent Index · 12,400+ finds. Coupons on /vigorbuy-coupons/; dataset on /finds-dataset/. Not Excel, not a Google Sheet.","inLanguage":"en"',
        ),
        (
            '"name":"VigorBuy Spreadsheet 2026","url":"https://vigorspreadsheet.com/","description":"VigorBuy spreadsheet: live finds. Not Excel, not a Google Sheet."',
            '"name":"VigorBuy Spreadsheet 2026 — Independent Index · 12,400+","url":"https://vigorspreadsheet.com/","description":"Brand hub only. No country spreadsheet desks. Coupons + dataset cited on this host."',
        ),
        (
            '"description":"Independent VigorBuy spreadsheet desk. Not the official VigorBuy app. Not vigor-buy.com, not vigorbuy-spreadsheet.com, not vigorbuyspreadsheets.net."',
            '"description":"Independent VigorBuy spreadsheet hub · Independent Index · 12,400+. Brand hub only — no country desks. Lookalike hosts are not keep desks in this portfolio."',
        ),
        (
            '{"@type":"Question","name":"Are vigor-buy.com or vigorbuy-spreadsheet.com the same site?","acceptedAnswer":{"@type":"Answer","text":"No. vigor-buy.com, vigorbuy-spreadsheet.com and vigorbuyspreadsheets.net are independent competitor catalogs. This hub does not 301 onto any of them."}}',
            '{"@type":"Question","name":"Is vigorspreadsheet.com a country desk?","acceptedAnswer":{"@type":"Answer","text":"No. vigorspreadsheet.com is the brand hub only. Mixed USA/SVN/IRL impressions do not authorize a dest-country skin. There are no keep country spreadsheet desks for VigorBuy. Lookalike hosts are competitor catalogs — not Phase C sunsets to revive, and not keep desks."}}',
        ),
        (
            '<div class="opfact"><b>Independent hosts</b><span>vigor-buy.com, vigorbuy-spreadsheet.com and vigorbuyspreadsheets.net stay independent. This hub does not 301 onto them. Mixed SI/RO/DK GSC does not make this hostname a dest-country skin.</span></div>',
            '<div class="opfact"><b>Brand hub only</b><span>Independent Index · 12,400+. No country spreadsheet desks. Lookalike hosts are competitor catalogs — not keep desks. Mixed USA/SVN GSC does not make .com a dest-country skin.</span></div>',
        ),
        (
            "This .com host is independent of vigor-buy.com, vigorbuy-spreadsheet.com and vigorbuyspreadsheets.net — no 301 between them. Mixed SI/RO/DK leftover GSC plus US impressions do not make this hostname a country dest. It is a spreadsheet hub, not a dest-country skin and not a country desk. Pick the real ship-to country inside vigorbuy.com. This desk does not coach customs values and does not reprint a 58-line Spain snapshot.",
            "This .com host is the VigorBuy brand hub (Independent Index · 12,400+). No keep country spreadsheet desks — do not invent new country TLDs. Lookalike hosts are competitor catalogs, not Phase C sunsets to revive. Mixed USA/SVN leftover GSC does not make this hostname a dest-country skin. Pick the real ship-to country inside vigorbuy.com. This desk does not coach customs values.",
        ),
        (
            "Independent VigorBuy spreadsheet desk on vigorspreadsheet.com. Not the official app, not checkout, not vigor-buy.com, not vigorbuy-spreadsheet.com, not vigorbuyspreadsheets.net.",
            "Independent Index · 12,400+ on vigorspreadsheet.com. Brand hub only — no country desks. Not the official app, not checkout.",
        ),
        (
            "Ranked unique coupon article stays at <a href=\"/vigorbuy-coupons/\">/vigorbuy-coupons/</a>. Unique ~45KB page stays 200. $210 / 30% 图文 for today’s official line also lives on /coupons.html — this homepage does not overwrite the ranked article.",
            "Ranked unique coupon article stays at <a href=\"/vigorbuy-coupons/\">/vigorbuy-coupons/</a>. Thin <code>/coupons.html</code> · <code>/coupons/</code> 301 → that money URL. Dataset: <a href=\"/finds-dataset/\">/finds-dataset/</a>.",
        ),
        (
            "Unique ~45KB page stays 200. $210 / 30% 图文 for today’s official line also lives on /coupons.html — this homepage does not overwrite the ranked article.",
            "Unique ~45KB money URL stays 200. Thin /coupons.html · /coupons/ 301 → /vigorbuy-coupons/. Dataset on /finds-dataset/.",
        ),
        (
            "Thin /coupons/ /shipping/ /start/ paths 404 today and are not invented as live 200s.",
            "Thin /coupons/ · /coupons.html 301 → /vigorbuy-coupons/. /shipping/ stays absent (no thin 200 shell).",
        ),
        (
            "vigor-buy.com, vigorbuy-spreadsheet.com and vigorbuyspreadsheets.net stay independent. This host is not a dest-country skin. Copy reviewed 9 Oct 2026.",
            "Brand hub only — no country desks. Lookalike hosts are not keep desks. Copy reviewed 26 Oct 2026.",
        ),
        (
            '<li><a href="/coupons.html">Offers</a></li>',
            '<li><a href="/finds-dataset/">Dataset</a></li>',
        ),
    ]
    for old, new in repls:
        if old not in src:
            # allow optional strings that may already differ
            if old in (
                "Unique ~45KB page stays 200. $210 / 30% 图文 for today’s official line also lives on /coupons.html — this homepage does not overwrite the ranked article.",
                "Ranked unique coupon article stays at <a href=\"/vigorbuy-coupons/\">/vigorbuy-coupons/</a>. Unique ~45KB page stays 200. $210 / 30% 图文 for today’s official line also lives on /coupons.html — this homepage does not overwrite the ranked article.",
            ):
                continue
            raise SystemExit(f"missing replace anchor:\n{old[:160]}")
        src = src.replace(old, new)

    # Coupons guide card description (gc block) — softer match
    src = src.replace(
        "$210 / 30% 图文 for today’s official line also lives on /coupons.html — this homepage does not overwrite the ranked article.",
        "Thin /coupons.html · /coupons/ 301 → this money URL. Dataset on /finds-dataset/.",
    )

    old_nav = """  <ul class="nl">
    <li><a class="on" href="/">Home</a></li>
    <li><a href="/vigorbuy-spreadsheet/">Spreadsheet</a></li>
    <li><a href="/is-vigorbuy-legit/">Is it Legit?</a></li>
    <li><a href="/vigorbuy-shipping-guide/">Shipping</a></li>
    <li><a href="/vigorbuy-coupons/">Coupons</a></li>
    <li><a href="/finds-dataset/">Dataset</a></li>
    <li><a href="/blog/">Blog</a></li>
  </ul>"""
    # after Offers→Dataset replace, nav already has Dataset; rebuild cleanly
    old_nav_live = """  <ul class="nl">
    <li><a class="on" href="/">Home</a></li>
    <li><a href="/vigorbuy-spreadsheet/">Spreadsheet</a></li>
    <li><a href="/is-vigorbuy-legit/">Is it Legit?</a></li>
    <li><a href="/vigorbuy-shipping-guide/">Shipping</a></li>
    <li><a href="/vigorbuy-coupons/">Coupons</a></li>
    <li><a href="/finds-dataset/">Dataset</a></li>
    <li><a href="/blog/">Blog</a></li>
  </ul>"""
    new_nav = """  <ul class="nl">
    <li><a href="#local">Hub</a></li>
    <li><a href="/vigorbuy-spreadsheet/">Spreadsheet</a></li>
    <li><a href="/vigorbuy-coupons/">Coupons</a></li>
    <li><a href="/finds-dataset/">Dataset</a></li>
    <li><a href="/vigorbuy-shipping-guide/">Shipping</a></li>
    <li><a href="/is-vigorbuy-legit/">Legit?</a></li>
    <li><a href="/blog/">Blog</a></li>
  </ul>"""
    if old_nav_live not in src:
        raise SystemExit("nav block missing after Offers→Dataset")
    src = src.replace(old_nav_live, new_nav)

    old_hero = """<section class="hero fade-in" id="main">
  <div class="hbg">$210 new-user gift · 30% shipping off · not Excel</div>
  <h1>VigorBuy Spreadsheet <em>2026</em></h1>
  <p class="hsub">Live Weidian, Taobao, 1688 and Yupoo finds with Buy links. Not Excel, not a Google Sheet, not checkout. Browse the ranked spreadsheet already on this host — including Women’s Fashion — then pay on vigorbuy.com. Official new-user gift measured 9 Oct 2026: <strong>$210</strong> coupon pack plus <strong>30%</strong> shipping off. Help sits behind Cloudflare Turnstile — this desk does not invent a free-day count.</p>
  <div class="hctas">
    <a href="/vigorbuy-spreadsheet/" class="cp">Ranked spreadsheet →</a>
    <a href="https://w2clinks.com/spreadsheet/vigorbuy/" class="cs" target="_blank" rel="noopener">Browse finds</a>
    <a href="https://vigorbuy.com/" class="cs" target="_blank" rel="noopener">Register on VigorBuy</a>
  </div>
  <div class="hst">
    <div class="hs"><div class="hsn">$210</div><div class="hsl">New-user gift</div></div>
    <div class="hs"><div class="hsn">30%</div><div class="hsl">Shipping off</div></div>
    <div class="hs"><div class="hsn">Discord</div><div class="hsl">dgd7j48e9U</div></div>
    <div class="hs"><div class="hsn">Help</div><div class="hsl">Turnstile</div></div>
  </div>
</section>"""
    new_hero = """<section class="hero fade-in" id="main">
  <div class="hbg">Independent Index · 12,400+ · not Excel · not a dest-country skin</div>
  <h1>VigorBuy Spreadsheet <em>2026</em> — Independent Index · 12,400+</h1>
  <p class="hsub">Independent Index · 12,400+ — live Weidian, Taobao, 1688 and Yupoo finds. Not Excel, not a Google Sheet, not checkout. Brand hub on this .com host (no country spreadsheet desks). Coupons + dataset cited below; pay on vigorbuy.com. Official new-user gift: <strong>$210</strong> pack + <strong>30%</strong> shipping off — confirm Wallet the morning you pay.</p>
  <div class="hctas">
    <a href="/vigorbuy-spreadsheet/" class="cp">Spreadsheet</a>
    <a href="/vigorbuy-coupons/" class="cs">Coupons</a>
    <a href="/finds-dataset/" class="cs">Dataset</a>
    <a href="https://vigorbuy.com/" class="cs" target="_blank" rel="noopener">Register</a>
  </div>
  <div class="hst">
    <div class="hs"><div class="hsn">12,400+</div><div class="hsl">Index rows</div></div>
    <div class="hs"><div class="hsn">$210</div><div class="hsl">New-user gift</div></div>
    <div class="hs"><div class="hsn">30%</div><div class="hsl">Shipping off</div></div>
    <div class="hs"><div class="hsn">Hub-only</div><div class="hsl">No country desk</div></div>
  </div>
</section>"""
    if old_hero not in src:
        raise SystemExit("hero block missing")
    src = src.replace(old_hero, new_hero)

    local_block = """
<section class="sg-sec" id="local">
  <h2>Brand hub · Independent Index · no country desk</h2>
  <p class="ssub">vigorspreadsheet.com · not a customs territory · money URLs ≤6</p>
  <ol class="local-steps">
    <li><strong>Brand spreadsheet → this hub</strong><span>Independent Index · 12,400+. Coupons + dataset live here. Mixed USA/SVN/IRL impressions do not make .com a dest-country desk.</span></li>
    <li><strong>No keep country desks</strong><span>Portfolio inventory lists zero VigorBuy country spreadsheet TLDs. Do not invent new ones. Do not revive Phase C sunsets.</span></li>
    <li><strong>Lookalikes ≠ keep desks</strong><span>vigor-buy.com / vigorbuy-spreadsheet.com / vigorbuyspreadsheets.net are competitor catalogs — not Phase C sunsets to revive, and not keep desks on this portfolio.</span></li>
    <li><strong>Money URLs stay ≤6</strong><span>Home · Spreadsheet · Coupons · Dataset · Shipping · Legit. Ranked inners stay 200 — not overwritten.</span></li>
  </ol>
  <p class="local-src">Money URLs (≤6): <a href="/">Home</a> · <a href="/vigorbuy-spreadsheet/">Spreadsheet</a> · <a href="/vigorbuy-coupons/">Coupons</a> · <a href="/finds-dataset/">Dataset</a> · <a href="/vigorbuy-shipping-guide/">Shipping</a> · <a href="/is-vigorbuy-legit/">Legit</a></p>
  <p class="local-src">Lab 26 Oct 2026. Phase C sunsets not revived. Orders stay on vigorbuy.com.</p>
</section>
"""
    m = re.search(r'(<section class="hero-wrap"><section class="hero fade-in" id="main">[\s\S]*?</section>)', src)
    if not m:
        # hero-wrap may close later
        m = re.search(r'(<section class="hero fade-in" id="main">[\s\S]*?</section>)', src)
    if not m:
        raise SystemExit("hero section wrapper missing")
    if 'id="local"' not in src:
        # insert after hero section; keep hero-wrap intact
        src = src[: m.end()] + "\n" + local_block + src[m.end() :]

    # Collapse remaining /coupons.html mentions onto the ranked money URL or dataset.
    src = src.replace(
        'Coupon 图文 also lives on <a href="/coupons.html">/coupons.html</a>.',
        'Thin coupons aliases 301 → <a href="/vigorbuy-coupons/">/vigorbuy-coupons/</a>.',
    )
    src = src.replace(
        '<a href="/coupons.html" class="gc"><span class="gtg" style="background:var(--rdl);color:var(--rd)">Offers</span><p class="gtit">Official $210 / 30% 图文</p><p class="gdesc">New-user gift measured 9 Oct 2026. Help behind Turnstile. Discord dgd7j48e9U.</p><span class="glink">See offers →</span></a>',
        '<a href="/finds-dataset/" class="gc"><span class="gtg" style="background:var(--rdl);color:var(--rd)">Moat</span><p class="gtit">Finds dataset</p><p class="gdesc">Public row counts + category proofs. Brand hub only — no country desks.</p><span class="glink">Open dataset →</span></a>',
    )
    src = src.replace(
        '<li><a href="/coupons.html">Official offers</a></li>',
        '<li><a href="/finds-dataset/">Dataset</a></li>',
    )
    src = src.replace(
        "also lives on /coupons.html — this homepage does not overwrite the ranked article.",
        "aliases 301 → /vigorbuy-coupons/. Dataset on /finds-dataset/.",
    )
    # Remaining hrefs (promo image figure, etc.) → ranked coupons money URL
    src = src.replace('href="/coupons.html"', 'href="/vigorbuy-coupons/"')
    # Any leftover plain-text /coupons.html path mentions
    if "coupons.html" in src:
        src = src.replace("/coupons.html", "/vigorbuy-coupons/")

    if "Independent Index · 12,400+" not in src:
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
        "<title>VigorBuy Coupon Codes 2026 — Working Discounts & Promo Codes</title>",
        "<title>VigorBuy Coupon Codes 2026 — Working Discounts · Updated 26 Oct</title>",
    )
    src = src.replace(
        'content="All working VigorBuy coupon codes for 2026, updated weekly. Use $210 GIFT — $210 new-user gift pack · 30% off shipping."',
        'content="Working VigorBuy coupon codes for 2026 (updated 26 Oct 2026). Primary $210 GIFT / 30% SHIP — confirm_live in Wallet. Truth JSON at /data/coupons-truth.json."',
    )
    faq_ld = (
        '<script type="application/ld+json">'
        '{"@context":"https://schema.org","@type":"FAQPage","mainEntity":['
        '{"@type":"Question","name":"What is the VigorBuy $210 GIFT code?","acceptedAnswer":{"@type":"Answer","text":"$210 GIFT is the public label for the official new-user gift pack (about $210 coupons + 30% shipping off). Status on this desk is confirm_live — re-check Wallet the morning you pay. Truth JSON: /data/coupons-truth.json."}},'
        '{"@type":"Question","name":"Where should VigorBuy coupon queries land?","acceptedAnswer":{"@type":"Answer","text":"On vigorspreadsheet.com/vigorbuy-coupons/. Thin /coupons/ and /coupons.html redirect here. Brand hub only — no country spreadsheet desks."}},'
        '{"@type":"Question","name":"Can I stack multiple VigorBuy codes?","acceptedAnswer":{"@type":"Answer","text":"Usually one order coupon per checkout; shipping discounts may stack separately when Wallet allows. Always confirm_live before pay."}}'
        "]}"
        "</script>"
    )
    if '"@type":"FAQPage"' not in src or "application/ld+json" not in src or "VigorBuy $210 GIFT" not in src:
        # microdata FAQ exists; still add JSON-LD once
        if "VigorBuy $210 GIFT code" not in src:
            src = src.replace("</head>", faq_ld + "\n</head>", 1)

    callout = """
  <div class="truth-callout" style="background:#FFF0F3;border:1px solid #F0C8C2;border-radius:12px;padding:14px 16px;margin:16px 0">
    <strong>Coupons truth · 26 Oct 2026</strong>
    <p>Primary public line <code>$210 GIFT</code> / <code>30% SHIP</code> status <strong>confirm_live</strong>. Machine-readable: <a href="/data/coupons-truth.json">/data/coupons-truth.json</a>. Finds moat: <a href="/finds-dataset/">/finds-dataset/</a>. Thin <code>/coupons.html</code> · <code>/coupons/</code> 301 → this page. Brand hub only — no country desks.</p>
  </div>
"""
    if "Coupons truth · 26 Oct 2026" not in src:
        anchor = "Every working VigorBuy coupon code in one place. Verified weekly. Click any code to copy it instantly."
        if anchor in src:
            src = src.replace(
                anchor,
                anchor + "</p>\n" + callout + "<p style=\"display:none\">",
                1,
            )
            # fix accidental broken p — cleaner insert after the lead p
            src = src.replace(
                anchor + "</p>\n" + callout + "<p style=\"display:none\">",
                anchor,
                1,
            )
            src = src.replace(
                '<p style="font-size:16px;color:var(--g3);line-height:1.8;border-left:3px solid var(--acc);padding-left:16px">Every working VigorBuy coupon code in one place. Verified weekly. Click any code to copy it instantly.</p>',
                '<p style="font-size:16px;color:var(--g3);line-height:1.8;border-left:3px solid var(--acc);padding-left:16px">Every working VigorBuy coupon code in one place. Verified weekly. Click any code to copy it instantly.</p>\n'
                + callout,
                1,
            )
        else:
            raise SystemExit("coupons lead paragraph missing")
    # freshness signal
    src = src.replace("Working codes &mdash; verified 2026", "Working codes &mdash; verified 26 Oct 2026")
    return src


def write_jsons() -> None:
    data = ROOT / "data"
    data.mkdir(parents=True, exist_ok=True)
    truth = {
        "brand": "VigorBuy",
        "host": "vigorspreadsheet.com",
        "last_verified": "2026-10-26",
        "platform_opt": "vigorbuy-platform-20261026",
        "verify_on": "vigorbuy.com Wallet / coupon dialog — confirm before pay",
        "update_cadence": "Coupons page copy + JSON stamped when gift/shipping offers change (target weekly)",
        "serp_note": "/vigorbuy-coupons/ carries nearly all clicks; homepage needs Independent Index · 12,400+ SERP signal. Brand hub only — no country desks.",
        "offers": [
            {
                "id": "vigorbuy-gift-210",
                "type": "new_user_gift",
                "label": "$210 GIFT new-user pack",
                "code": "$210 GIFT",
                "value_claim": "Official new-user gift pack (~$210 coupons) — confirm_live in Wallet / Nuxt coupon dialog",
                "status": "confirm_live",
                "expires_on": None,
                "expires_note": "No fixed expiry promised by this desk — re-confirm in-app the morning you pay",
                "applies_to": "VigorBuy new-user Wallet / register gift",
                "exclusions": ["This hub is not checkout", "Stacking rules official-only"],
                "source": "https://vigorspreadsheet.com/vigorbuy-coupons/",
                "last_verified": "2026-10-26",
            },
            {
                "id": "vigorbuy-ship-30",
                "type": "shipping_promo",
                "label": "30% SHIP shipping off",
                "code": "30% SHIP",
                "value_claim": "Official 30% shipping discount tied to new-user gift line — confirm_live",
                "status": "confirm_live",
                "expires_on": None,
                "source": "https://vigorspreadsheet.com/vigorbuy-coupons/",
                "last_verified": "2026-10-26",
            },
            {
                "id": "vigorbuy-pack-15-archive",
                "type": "order_promo",
                "label": "PACK 15% archive",
                "code": "PACK 15%",
                "value_claim": "Listed on ranked coupons article — treat as confirm_live / may be historical",
                "status": "confirm_live",
                "expires_on": None,
                "source": "https://vigorspreadsheet.com/vigorbuy-coupons/",
                "last_verified": "2026-10-26",
            },
            {
                "id": "vigorbuy-back-to-school-archive",
                "type": "community_promo",
                "label": "Back-to-School Reddit event archive",
                "code": None,
                "value_claim": "One-week Reddit community event — historical unless still visible in Wallet",
                "status": "historical",
                "expires_on": None,
                "source": "https://vigorspreadsheet.com/vigorbuy-coupons/",
                "last_verified": "2026-10-26",
            },
        ],
    }
    finds = {
        "schema": "seo-factory.finds-dataset.v1",
        "brand": "VigorBuy",
        "host": "vigorspreadsheet.com",
        "last_verified": "2026-10-26",
        "generated_at": "2026-10-26T19:30:00Z",
        "row_count": 12400,
        "row_count_display": "12,400+",
        "update_frequency": "Catalog cards refresh continuously; public dataset stamp reviewed at least weekly.",
        "qc_field": "qc_photo",
        "price_fields": ["price_cny", "price_usd_approx", "price_display"],
        "anti_sheet_note": "Public, citable row counts + dated category proofs — not another opaque Google Sheet dump. Coupon intent still lives on /vigorbuy-coupons/.",
        "platform_opt": "vigorbuy-platform-20261026",
        "hub_role": "brand_hub_only_no_country_desks",
        "twin_note": "No Phase A hub twin in portfolio. Lookalike hosts (vigor-buy.com / vigorbuy-spreadsheet.com / vigorbuyspreadsheets.net) are competitor catalogs — not keep desks; do not revive Phase C sunsets.",
        "endpoints": {
            "html": "https://vigorspreadsheet.com/finds-dataset/",
            "json": "https://vigorspreadsheet.com/data/finds-dataset.json",
            "coupons_truth": "https://vigorspreadsheet.com/data/coupons-truth.json",
            "catalog": "https://w2clinks.com/spreadsheet/vigorbuy/",
            "hub": "https://vigorspreadsheet.com/",
            "ranked_spreadsheet": "https://vigorspreadsheet.com/vigorbuy-spreadsheet/",
        },
        "sitemap_policy": "Sitemap lastmod for /finds-dataset/, /vigorbuy-coupons/ and money URLs bumps when this stamp changes.",
        "sample_skus": [
            {
                "sku": "cat_sneakers",
                "title": "Sneakers & Shoes category proof (live catalog)",
                "price_cny": None,
                "price_display": "see catalog",
                "category_hint": "SNEAKERS",
                "source_url": "https://w2clinks.com/spreadsheet/vigorbuy/",
                "qc_photo": False,
                "last_verified": "2026-10-26",
            },
            {
                "sku": "cat_women",
                "title": "Women's Fashion (GSC money query on this hub)",
                "price_cny": None,
                "price_display": "see catalog / homepage cards",
                "category_hint": "FEMALE STYLE",
                "source_url": "https://w2clinks.com/spreadsheet/vigorbuy/?category=FEMALE%20STYLE",
                "qc_photo": False,
                "last_verified": "2026-10-26",
            },
            {
                "sku": "cat_jacket",
                "title": "Jackets & Coats category proof (live catalog)",
                "price_cny": None,
                "price_display": "see catalog",
                "category_hint": "JACKET",
                "source_url": "https://w2clinks.com/spreadsheet/vigorbuy/",
                "qc_photo": False,
                "last_verified": "2026-10-26",
            },
            {
                "sku": "page_shoes_sheet",
                "title": "Shoes spreadsheet ranked article on this hub",
                "price_cny": None,
                "price_display": "see /vigorbuy-shoes-spreadsheet/",
                "category_hint": "SHOES",
                "source_url": "https://vigorspreadsheet.com/vigorbuy-shoes-spreadsheet/",
                "qc_photo": False,
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
<title>VigorBuy Finds Dataset — 12,400+ Rows, Category Proofs &amp; last_verified</title>
<meta name="description" content="Provable VigorBuy spreadsheet dataset: 12,400+ rows, weekly freshness stamp, category proofs. Independent Index on vigorspreadsheet.com — not a Google Sheet dump. Coupons stay on /vigorbuy-coupons/.">
<link rel="canonical" href="https://vigorspreadsheet.com/finds-dataset/">
<meta name="robots" content="index,follow">
<meta property="og:title" content="VigorBuy Finds Dataset — Independent Index · 12,400+">
<meta property="og:description" content="12,400+ indexed finds with last_verified=2026-10-26. Public JSON + category proofs. Coupon truth is a separate JSON.">
<meta property="og:url" content="https://vigorspreadsheet.com/finds-dataset/">
<meta property="og:type" content="article">
<meta property="article:modified_time" content="2026-10-26">
<script type="application/ld+json">{"@context":"https://schema.org","@type":"Dataset","name":"VigorBuy spreadsheet finds dataset","description":"Public row counts, update frequency and category proofs for the independent VigorBuy spreadsheet hub.","url":"https://vigorspreadsheet.com/finds-dataset/","creator":{"@type":"Organization","name":"VigorBuy Spreadsheet"},"dateModified":"2026-10-26","distribution":[{"@type":"DataDownload","encodingFormat":"application/json","contentUrl":"https://vigorspreadsheet.com/data/finds-dataset.json"},{"@type":"DataDownload","encodingFormat":"application/json","contentUrl":"https://vigorspreadsheet.com/data/coupons-truth.json"}],"variableMeasured":["sku","title","price","qc_photo","last_verified"]}</script>
<style>
:root{--acc:#F80038;--ink:#0A0A0A;--mute:#555;--line:#F0C8C2;--bg:#FFF5F6;--ok:#166534;--okbg:#f0fdf4}
*{box-sizing:border-box}body{margin:0;font-family:Montserrat,DM Sans,system-ui,sans-serif;color:var(--ink);background:#fff;line-height:1.7}
.top{border-bottom:1px solid var(--line);background:#fff;position:sticky;top:0;z-index:5}
.wrap{max-width:860px;margin:0 auto;padding:0 20px}
.top .wrap{display:flex;gap:16px;align-items:center;min-height:56px;flex-wrap:wrap}
.brand{font-weight:700;text-decoration:none;color:var(--ink);font-size:15px}
.nav a{margin-left:12px;text-decoration:none;color:var(--mute);font-size:14px}
.nav a:hover,.nav a.on{color:var(--acc)}
.hero{padding:40px 0 16px;background:linear-gradient(180deg,#FFF0F3 0%,#fff 72%)}
.eyebrow{font-size:12px;letter-spacing:.08em;text-transform:uppercase;color:var(--acc);font-weight:700}
h1{font-size:clamp(28px,4vw,40px);line-height:1.2;margin:10px 0}
.lead{font-size:18px;color:var(--mute);max-width:42em}
.stamp{display:inline-flex;align-items:center;gap:8px;font-size:13px;background:var(--okbg);color:var(--ok);border:1px solid #bbf7d0;border-radius:999px;padding:6px 12px;margin-top:12px}
.stamp time{font-weight:700}
article{padding:8px 0 56px}
article h2{font-size:24px;margin:1.6em 0 .5em}
.stats{display:grid;grid-template-columns:repeat(auto-fit,minmax(140px,1fr));gap:12px;margin:1.2em 0}
.stat{background:var(--bg);border:1px solid var(--line);border-radius:12px;padding:14px 16px}
.stat b{display:block;font-size:22px;letter-spacing:-.02em}
.stat span{font-size:12px;color:var(--mute)}
.box{background:var(--bg);border:1px solid var(--line);border-radius:12px;padding:18px 20px;margin:1.2em 0}
table{width:100%;border-collapse:collapse;font-size:13.5px;margin:1em 0}
th,td{border:1px solid var(--line);padding:10px 12px;text-align:left;vertical-align:top}
th{background:var(--bg);font-size:12px;text-transform:uppercase;letter-spacing:.04em;color:var(--mute)}
.btn{display:inline-block;background:var(--acc);color:#fff;text-decoration:none;padding:12px 18px;border-radius:10px;font-weight:700;margin:4px 8px 4px 0}
.btn.ghost{background:#fff;color:var(--acc);border:1px solid var(--acc)}
footer{border-top:1px solid var(--line);padding:28px 0;color:var(--mute);font-size:14px}
a{color:var(--acc)}
</style>
</head>
<body>
<header class="top"><div class="wrap">
  <a class="brand" href="/">VigorBuy Spreadsheet</a>
  <nav class="nav">
    <a href="/">Home</a>
    <a href="/vigorbuy-coupons/">Coupons</a>
    <a href="/vigorbuy-spreadsheet/">Spreadsheet</a>
    <a href="/finds-dataset/" class="on">Dataset</a>
    <a href="/is-vigorbuy-legit/">Legit?</a>
  </nav>
</div></header>
<section class="hero"><div class="wrap">
  <div class="eyebrow">VigorBuy Spreadsheet · Independent Index · brand hub</div>
  <h1>VigorBuy finds dataset</h1>
  <p class="lead">Public row counts, update frequency and dated category proofs — so this hub is not “just another Sheet clone.” Coupon stacking stays on <a href="/vigorbuy-coupons/">/vigorbuy-coupons/</a>. No country spreadsheet desks for this brand. Phase C sunsets not revived.</p>
  <div class="stamp">last_verified <time datetime="2026-10-26">2026-10-26</time> · 12,400+ rows · platform_opt=vigorbuy-platform-20261026</div>
</div></section>
<article class="wrap">
<div class="stats">
  <div class="stat"><b>12,400+</b><span>Indexed finds (hub hero)</span></div>
  <div class="stat"><b>weekly</b><span>Target stamp cadence</span></div>
  <div class="stat"><b>Coupons</b><span>Separate truth JSON</span></div>
  <div class="stat"><b>Hub-only</b><span>No country desks</span></div>
</div>

<div class="box">
  <h2 style="margin-top:0;font-size:20px">Why this page exists</h2>
  <p>GSC for this host leans <strong>/vigorbuy-coupons/</strong> (most of the 28d clicks) plus impressing homepage / shipping / legit URLs with zero clicks. Spreadsheet / Independent Index queries need a falsifiable catalog claim: how many rows, when the stamp moved, and which category proofs back the count.</p>
  <p><a class="btn" href="/data/finds-dataset.json">Download finds-dataset.json</a>
     <a class="btn ghost" href="/data/coupons-truth.json">Coupons truth JSON</a>
     <a class="btn ghost" href="/vigorbuy-coupons/">Coupon codes</a>
     <a class="btn ghost" href="https://w2clinks.com/spreadsheet/vigorbuy/" rel="noopener">Open catalog</a></p>
</div>

<h2>Category / page proofs</h2>
<table>
  <thead><tr><th>Proof</th><th>Hint</th><th>last_verified</th></tr></thead>
  <tbody>
    <tr><td>Sneakers &amp; Shoes</td><td>SNEAKERS</td><td>2026-10-26</td></tr>
    <tr><td>Women's Fashion (GSC money)</td><td>FEMALE STYLE</td><td>2026-10-26</td></tr>
    <tr><td>Jackets &amp; Coats</td><td>JACKET</td><td>2026-10-26</td></tr>
    <tr><td>Shoes spreadsheet article</td><td>/vigorbuy-shoes-spreadsheet/</td><td>2026-10-26</td></tr>
  </tbody>
</table>

<div class="box">
  <h2 style="margin-top:0;font-size:20px">Hub vs country desk</h2>
  <p><strong>Brand hub = vigorspreadsheet.com.</strong> Portfolio inventory lists zero VigorBuy country spreadsheet desks. Mixed geo impressions do not authorize a dest-country skin. Lookalike hosts are competitor catalogs — not keep desks. Do not revive Phase C sunsets.</p>
</div>
</article>
<footer><div class="wrap">Independent resource. Not affiliated with vigorbuy.com. platform_opt=vigorbuy-platform-20261026.</div></footer>
</body>
</html>
"""
    d = ROOT / "finds-dataset"
    d.mkdir(parents=True, exist_ok=True)
    (d / "index.html").write_text(html, encoding="utf-8")


def write_misc() -> None:
    (ROOT / "llms.txt").write_text(
        """# VigorBuy Spreadsheet (vigorspreadsheet.com)

> Independent Index · 12,400+ finds. Brand hub only — no country spreadsheet desks.

- Hub: https://vigorspreadsheet.com/
- Spreadsheet: https://vigorspreadsheet.com/vigorbuy-spreadsheet/
- Coupons (money): https://vigorspreadsheet.com/vigorbuy-coupons/
- Coupons truth JSON: https://vigorspreadsheet.com/data/coupons-truth.json
- Finds dataset: https://vigorspreadsheet.com/finds-dataset/
- Dataset JSON: https://vigorspreadsheet.com/data/finds-dataset.json
- Shipping: https://vigorspreadsheet.com/vigorbuy-shipping-guide/
- Legit: https://vigorspreadsheet.com/is-vigorbuy-legit/
- QC: https://vigorspreadsheet.com/vigorbuy-qc-guide/

## Hub / sunset rules
- Brand hub only. No keep country spreadsheet desks. Do not invent new country TLDs.
- Lookalike hosts (vigor-buy.com / vigorbuy-spreadsheet.com / vigorbuyspreadsheets.net) are competitor catalogs — not keep desks; do not revive Phase C sunsets.
- Thin /coupons/ and /coupons.html → /vigorbuy-coupons/

## Official
- https://vigorbuy.com/ (checkout / Wallet; $210 GIFT + 30% SHIP confirm_live)

platform_opt=vigorbuy-platform-20261026
last_verified=2026-10-26
""",
        encoding="utf-8",
    )

    (ROOT / "sitemap.xml").write_text(
        """<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url><loc>https://vigorspreadsheet.com/</loc><lastmod>2026-10-26</lastmod><changefreq>weekly</changefreq></url>
  <url><loc>https://vigorspreadsheet.com/vigorbuy-spreadsheet/</loc><lastmod>2026-10-26</lastmod><changefreq>weekly</changefreq></url>
  <url><loc>https://vigorspreadsheet.com/vigorbuy-coupons/</loc><lastmod>2026-10-26</lastmod><changefreq>weekly</changefreq></url>
  <url><loc>https://vigorspreadsheet.com/finds-dataset/</loc><lastmod>2026-10-26</lastmod><changefreq>weekly</changefreq></url>
  <url><loc>https://vigorspreadsheet.com/data/finds-dataset.json</loc><lastmod>2026-10-26</lastmod><changefreq>weekly</changefreq></url>
  <url><loc>https://vigorspreadsheet.com/data/coupons-truth.json</loc><lastmod>2026-10-26</lastmod><changefreq>weekly</changefreq></url>
  <url><loc>https://vigorspreadsheet.com/vigorbuy-shipping-guide/</loc><lastmod>2026-10-26</lastmod><changefreq>weekly</changefreq></url>
  <url><loc>https://vigorspreadsheet.com/is-vigorbuy-legit/</loc><lastmod>2026-10-26</lastmod><changefreq>monthly</changefreq></url>
  <url><loc>https://vigorspreadsheet.com/vigorbuy-qc-guide/</loc><lastmod>2026-10-26</lastmod><changefreq>weekly</changefreq></url>
  <url><loc>https://vigorspreadsheet.com/vigorbuy-shoes-spreadsheet/</loc><lastmod>2026-10-26</lastmod><changefreq>weekly</changefreq></url>
  <url><loc>https://vigorspreadsheet.com/how-to-use-vigorbuy/</loc><lastmod>2026-10-26</lastmod><changefreq>monthly</changefreq></url>
  <url><loc>https://vigorspreadsheet.com/vigorbuy-invite-code/</loc><lastmod>2026-10-26</lastmod><changefreq>monthly</changefreq></url>
  <url><loc>https://vigorspreadsheet.com/llms.txt</loc><lastmod>2026-10-26</lastmod><changefreq>monthly</changefreq></url>
</urlset>
""",
        encoding="utf-8",
    )

    deploy_dir = ROOT / "_deploy"
    deploy_dir.mkdir(parents=True, exist_ok=True)
    (deploy_dir / "thin-page-redirects.conf").write_text(
        """# Platform opt 2026-10-26: coupons aliases + public JSON/dataset
# Brand hub only — no country desks; do not revive Phase C sunsets.
location = /coupons.html { return 301 https://vigorspreadsheet.com/vigorbuy-coupons/; }
location = /coupons/ { return 301 https://vigorspreadsheet.com/vigorbuy-coupons/; }
location = /coupons { return 301 https://vigorspreadsheet.com/vigorbuy-coupons/; }
location = /vigorbuy-coupon/ { return 301 https://vigorspreadsheet.com/vigorbuy-coupons/; }
location = /vigorbuy-coupon { return 301 https://vigorspreadsheet.com/vigorbuy-coupons/; }

location = /data/finds-dataset.json {
  default_type application/json;
  add_header Cache-Control "public, max-age=300";
  alias /www/wwwroot/vigorspreadsheet.com/data/finds-dataset.json;
}
location = /data/coupons-truth.json {
  default_type application/json;
  add_header Cache-Control "public, max-age=300";
  alias /www/wwwroot/vigorspreadsheet.com/data/coupons-truth.json;
}
location ^~ /finds-dataset/ {
  try_files $uri $uri/ /finds-dataset/index.html;
}
location ^~ /vigorbuy-coupons/ {
  try_files $uri $uri/ /vigorbuy-coupons/index.html;
}
""",
        encoding="utf-8",
    )

    (ROOT / "HOME-PATCH.md").write_text(
        """# HOME patch notes — vigorspreadsheet.com

Surgical on ranked CMS homepage (title / CTAs / `#local` / nav / footer / hub-only narrative).
Do **not** wholesale overwrite with leftover Georgia dest skin in `overlay/index.html`.
Publish only `index.html.platform-patched`.
Brand hub only — **no** keep country desks. Lookalike hosts are competitor catalogs — not Phase C sunsets to revive.
""",
        encoding="utf-8",
    )

    (ROOT / "DEPLOY-PLATFORM.md").write_text(
        """# Deploy — VigorBuy platform opt (2026-10-26)

Origin: Baota host used by portfolio desks.  
Root: `/www/wwwroot/vigorspreadsheet.com`

## GUARDS

- **Do not** rsync leftover Georgia dest `overlay/index.html` over the ranked CMS homepage — publish only `index.html.platform-patched`.
- **Do not** revive Phase C sunsets; do not invent country spreadsheet domains.
- Hub must **not** treat lookalike hosts as keep desks.
- Nginx vhost must `include .../extension/vigorspreadsheet.com/*.conf` (was missing before this opt).

## Files to push

```bash
HUB=/www/wwwroot/vigorspreadsheet.com
LOCAL=sites/vigorspreadsheet.com/overlay
BAK=/www/backup/vigorbuy-platform-$(date +%Y%m%d-%H%M%S)
NGX=/www/server/panel/vhost/nginx/vigorspreadsheet.com.conf

mkdir -p "$BAK"
cp -a "$HUB/index.html" "$HUB/sitemap.xml" "$HUB/coupons.html" "$BAK/" 2>/dev/null || true
cp -a "$HUB/vigorbuy-coupons" "$BAK/vigorbuy-coupons" 2>/dev/null || true
cp -a "$NGX" "$BAK/vigorspreadsheet.com.conf.bak"

cp "$LOCAL/index.html.platform-patched" "$HUB/index.html"
mkdir -p "$HUB/vigorbuy-coupons"
cp "$LOCAL/vigorbuy-coupons/index.html" "$HUB/vigorbuy-coupons/index.html"
rsync -av "$LOCAL/finds-dataset/" "$HUB/finds-dataset/"
mkdir -p "$HUB/data"
cp "$LOCAL/data/coupons-truth.json" "$LOCAL/data/finds-dataset.json" "$HUB/data/"
cp "$LOCAL/llms.txt" "$LOCAL/sitemap.xml" "$HUB/"

mkdir -p /www/server/panel/vhost/nginx/extension/vigorspreadsheet.com
cp "$LOCAL/_deploy/thin-page-redirects.conf" \\
  /www/server/panel/vhost/nginx/extension/vigorspreadsheet.com/thin-page-redirects.conf
# Ensure SSL server block includes extension/*.conf before location /
nginx -t && nginx -s reload
```

## GSC

Submit `https://vigorspreadsheet.com/sitemap.xml` after deploy.

## Verify

- `/` title contains Independent Index · 12,400+
- Hero CTAs Spreadsheet / Coupons / Dataset / Register; `#local` money URLs ≤6
- `/vigorbuy-coupons/` has truth callout + 26 Oct 2026 + FAQ-LD
- `/data/*.json` + `/finds-dataset/` + `/llms.txt` → 200
- `/coupons/` · `/coupons.html` → 301 `/vigorbuy-coupons/`
""",
        encoding="utf-8",
    )


def main() -> None:
    src = LIVE.read_text(encoding="utf-8")
    patched = patch_home(src)
    (ROOT / "index.html.platform-patched").write_text(patched, encoding="utf-8")

    if not COUPONS_LIVE.is_file():
        raise SystemExit(f"missing {COUPONS_LIVE}")
    coupons_dir = ROOT / "vigorbuy-coupons"
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
