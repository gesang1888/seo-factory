#!/usr/bin/env python3
"""Build FishGoo platform-opt overlay from LIVE homepage (surgical).

Does not overwrite the ranked ~45KB homepage with leftover Georgia dest
overlay/index.html. API /api/products/ total ≈ 11,365 → Independent Index · 11,300+.
Brand hub only — no keep country spreadsheet desks; do not revive Phase C sunsets.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "sites" / "fishgoospreadsheet.net" / "overlay"
LIVE = ROOT / "live-base" / "index.html"
COUPONS_LIVE = ROOT / "live-base" / "coupons.html"
HOST = "fishgoospreadsheet.net"
BRAND = "FishGoo"
OPT = "fishgoo-platform-20261026"
DATE = "2026-10-26"
DATE_HUMAN = "26 Oct 2026"
ROWS = "11,300+"
ROWS_N = 11365
OFFICIAL = "https://www.fishgoo.com/"
CATALOG = "https://w2clinks.com/spreadsheet/fishgoo/"
EST = "https://www.fishgoo.com/estimation"


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
.hero-cta-row{display:flex;flex-wrap:wrap;gap:10px;margin:14px 0 6px}
.hero-cta-row a{display:inline-block;padding:10px 16px;border-radius:10px;font-weight:700;text-decoration:none;font-size:14px}
.hero-cta-row .cta-p{background:var(--acc,#FF7A45);color:#fff}
.hero-cta-row .cta-o{background:#fff;color:var(--acd,#c2410c);border:1px solid color-mix(in srgb,var(--acc,#FF7A45) 45%,#ddd)}
"""
    if ".sg-sec#local" not in src:
        src = src.replace("</style>", local_css + "\n</style>", 1)

    repls = [
        (
            "<title>FishGoo Spreadsheet 2026 — QC Finds &amp; Shipping</title>",
            f"<title>FishGoo Spreadsheet 2026 — Independent Index · {ROWS}</title>",
        ),
        (
            'content="FishGoo spreadsheet: live Weidian, Taobao and 1688 QC finds. Not Excel, not a Google Sheet. Use the shipping calculator, then pay on fishgoo.com."',
            f'content="FishGoo Independent Index · {ROWS} on {HOST}. Not Excel, not a Google Sheet, not checkout. Coupons on /fishgoo-coupons/; dataset on /finds-dataset/. Brand hub only — no country spreadsheet desks. Pay on fishgoo.com."',
        ),
        (
            '<meta property="og:title" content="FishGoo Spreadsheet 2026 — QC Finds & Shipping">',
            f'<meta property="og:title" content="FishGoo Spreadsheet 2026 — Independent Index · {ROWS}">',
        ),
        (
            'content="FishGoo spreadsheet: live Weidian, Taobao and 1688 QC finds. Not Excel, not a Google Sheet. Use the shipping calculator, then pay on fishgoo.com."',
            f'content="FishGoo Independent Index · {ROWS}. Coupons + finds dataset on this hub. Brand hub only (no country desks). Spam-cliff recovery candidate — deepen SERP truth, do not invent desks."',
        ),
    ]
    for old, new in repls:
        if old not in src:
            raise SystemExit(f"missing replace anchor:\n{old[:180]}")
        src = src.replace(old, new, 1)

    # Force remaining og:description duplicates
    src = src.replace(
        'content="FishGoo spreadsheet: live Weidian, Taobao and 1688 QC finds. Not Excel, not a Google Sheet. Use the shipping calculator, then pay on fishgoo.com."',
        f'content="FishGoo Independent Index · {ROWS}. Coupons + finds dataset on this hub. Brand hub only (no country desks)."',
    )

    src = src.replace(
        '"@type":"WebSite","name":"FishGoo Spreadsheet","alternateName":["FishGoo Spreadsheet","FishGoo spreadsheet 2026"]',
        f'"@type":"WebSite","name":"FishGoo Independent Index","alternateName":["FishGoo Spreadsheet 2026","{HOST}"],"dateModified":"{DATE}"',
    )
    src = src.replace(
        '"description":"FishGoo spreadsheet: live Weidian, Taobao and 1688 QC finds. Not Excel, not a Google Sheet. Use the shipping calculator, then pay on fishgoo.com."',
        f'"description":"FishGoo Independent Index · {ROWS} finds. Coupons on /fishgoo-coupons/; dataset on /finds-dataset/. Not Excel, not a Google Sheet. Brand hub only — no country desks."',
        1,
    )

    if "Is fishgoospreadsheet.net a country desk?" not in src:
        faq_extra = (
            '{"@type":"Question","name":"Is fishgoospreadsheet.net a country desk?",'
            '"acceptedAnswer":{"@type":"Answer","text":"No. fishgoospreadsheet.net is the FishGoo brand hub only. There are no keep country spreadsheet desks. Do not invent new country TLDs. Do not revive Phase C sunsets."}},'
            '{"@type":"Question","name":"Where do FishGoo coupon queries land?",'
            '"acceptedAnswer":{"@type":"Answer","text":"On https://fishgoospreadsheet.net/fishgoo-coupons/. Thin /coupons.html and /coupons/ redirect there. Dataset moat lives on /finds-dataset/. Official offers are account-based ($500 new-user / ¥100 app) — no typed-in FISHGOO10."}},'
        )
        src = src.replace(
            '{"@type":"FAQPage","mainEntity":[',
            '{"@type":"FAQPage","mainEntity":[' + faq_extra,
            1,
        )

    old_nav = """<ul class="nl">
    <li><a class="on" href="/">Home</a></li>
    <li><a href="https://w2clinks.com/spreadsheet/fishgoo/" target="_blank" rel="noopener">Bestpicks</a></li>
    <li><a href="/finds.html">Forwarding</a></li>
    <li><a href="/shipping-guide.html">Freight Calculator</a></li>
    <li><a href="/beginner-guide.html">How to buy?</a></li>
    <li><a href="/coupons.html">Coupons</a></li>
    <li><a href="https://www.fishgoo.com/" rel="noopener">APP Download</a></li>
  </ul>"""
    new_nav = """<ul class="nl">
    <li><a class="on" href="/">Home</a></li>
    <li><a href="#local">Hub</a></li>
    <li><a href="https://w2clinks.com/spreadsheet/fishgoo/" target="_blank" rel="noopener">Spreadsheet</a></li>
    <li><a href="/fishgoo-coupons/">Coupons</a></li>
    <li><a href="/finds-dataset/">Dataset</a></li>
    <li><a href="/shipping-guide.html">Shipping</a></li>
    <li><a href="/beginner-guide.html">How to buy?</a></li>
    <li><a href="https://www.fishgoo.com/" rel="noopener">Register</a></li>
  </ul>"""
    if old_nav not in src:
        raise SystemExit("nav block missing")
    src = src.replace(old_nav, new_nav)

    old_hero_head = """<section class="hero-wrap"><section class="hero fade-in">
  <p class="hero-kicker">Shop China. Ship Worldwide.</p>
  <h1>The Complete <em>FishGoo Spreadsheet</em> 2026</h1>
  <p class="hsub">Live Weidian, Taobao and 1688 QC finds. Not Excel, not a Google Sheet, not checkout. Paste a product link, then pay on fishgoo.com.</p>"""
    new_hero_head = f"""<section class="hero-wrap"><section class="hero fade-in">
  <p class="hero-kicker">Independent Index · {ROWS} · not Excel · not a dest-country skin</p>
  <h1>FishGoo Spreadsheet <em>2026</em> — Independent Index · {ROWS}</h1>
  <p class="hsub">Independent Index · {ROWS} — live Weidian, Taobao and 1688 QC finds. Not Excel, not a Google Sheet, not checkout. Brand hub on this .net host (no country spreadsheet desks). Coupons + dataset cited below; pay on fishgoo.com. Official SPA measured 8 Oct 2026: <strong>up to $500 new-user shipping coupons</strong> + <strong>¥100 app exclusive</strong> — this homepage does not print an invite token. Hub stamp {DATE_HUMAN}.</p>
  <div class="hero-cta-row">
    <a class="cta-p" href="{CATALOG}" target="_blank" rel="noopener">Spreadsheet</a>
    <a class="cta-o" href="/fishgoo-coupons/">Coupons</a>
    <a class="cta-o" href="/finds-dataset/">Dataset</a>
    <a class="cta-o" href="{OFFICIAL}" rel="noopener">Register</a>
  </div>"""
    if old_hero_head not in src:
        raise SystemExit("hero head missing")
    src = src.replace(old_hero_head, new_hero_head)

    local_block = f"""
<section class="sg-sec" id="local">
  <h2>Brand hub · Independent Index · no country desk</h2>
  <p class="ssub">{HOST} · not a customs territory · money URLs ≤6</p>
  <ol class="local-steps">
    <li><strong>Brand spreadsheet → this hub</strong><span>Independent Index · {ROWS} (API total {ROWS_N}). Coupons + dataset live here. Spam cliff (90d 63 → 28d 5) is recovery work on this host — not a reason to invent desks.</span></li>
    <li><strong>No keep country desks</strong><span>GSC lists only sc-domain:{HOST}. Do not invent country spreadsheet TLDs. Do not revive Phase C sunsets.</span></li>
    <li><strong>Coupons money URL</strong><span>/fishgoo-coupons/ holds $500 / ¥100 truth (confirm_live). Thin /coupons.html · /coupons/ 301 here. No typed-in FISHGOO10.</span></li>
    <li><strong>Money URLs stay ≤6</strong><span>Home · Spreadsheet · Coupons · Dataset · Shipping · Beginner. Ranked ~12–45KB inners stay 200 — not overwritten by Georgia dest skins.</span></li>
  </ol>
  <p class="local-src">Money URLs (≤6): <a href="/">Home</a> · <a href="{CATALOG}">Spreadsheet</a> · <a href="/fishgoo-coupons/">Coupons</a> · <a href="/finds-dataset/">Dataset</a> · <a href="/shipping-guide.html">Shipping</a> · <a href="/beginner-guide.html">Beginner</a></p>
  <p class="local-src">Lab {DATE_HUMAN}. Estimator: <a href="{EST}">{EST}</a>. Phase C sunsets not revived. Orders stay on fishgoo.com.</p>
</section>
"""
    marker = "</section></section>\n<section id=\"official-promo\">"
    if marker not in src:
        raise SystemExit("hero close / official-promo marker missing")
    if 'id="local"' not in src:
        src = src.replace(marker, "</section></section>\n" + local_block + "\n<section id=\"official-promo\">", 1)

    # Guides card: coupons.html → fishgoo-coupons; add dataset framing on Trust Review optional
    old_coupon_card = (
        '<a href="/coupons.html" class="gc"><span class="gtg" style="background:#FEF3C7;color:#92400E">Coupons</span>'
        '<p class="gtit">FishGoo Coupons 2026</p>'
        '<p class="gdesc">Official 8 Oct 2026: up to $500 new-user shipping coupons + ¥100 app exclusive, with screenshots. This homepage does not print a token.</p>'
        '<span class="glink">See offers &rarr;</span></a>'
    )
    new_coupon_card = (
        '<a href="/fishgoo-coupons/" class="gc"><span class="gtg" style="background:#FEF3C7;color:#92400E">Coupons</span>'
        f'<p class="gtit">FishGoo Coupons · truth · {DATE_HUMAN}</p>'
        '<p class="gdesc">Money URL + /data/coupons-truth.json. Official $500 new-user + ¥100 app exclusive (confirm_live). Thin /coupons.html 301 here. No typed-in FISHGOO10.</p>'
        '<span class="glink">Open coupons &rarr;</span></a>'
    )
    if old_coupon_card not in src:
        raise SystemExit("coupons guide card missing")
    src = src.replace(old_coupon_card, new_coupon_card)

    old_sheet_card = (
        '<a href="/fishgoo-spreadsheet.html" class="gc"><span class="gtg" style="background:var(--acl);color:var(--acd)">On this host</span>'
        '<p class="gtit">FishGoo Spreadsheet — how to use W2C links 2026</p>'
        '<p class="gdesc">Twelve W2C category lists already on this host. Live photos stay on the w2clinks FishGoo sheet.</p>'
        '<span class="glink">Open &rarr;</span></a>'
    )
    new_sheet_card = (
        '<a href="/finds-dataset/" class="gc"><span class="gtg" style="background:var(--pul);color:var(--pu)">Moat</span>'
        f'<p class="gtit">Finds dataset · {ROWS}</p>'
        '<p class="gdesc">Public row counts + category proofs. Brand hub only — no country desks. Coupon truth stays on /fishgoo-coupons/.</p>'
        '<span class="glink">Open dataset &rarr;</span></a>'
    )
    if old_sheet_card not in src:
        raise SystemExit("spreadsheet guide card missing")
    src = src.replace(old_sheet_card, new_sheet_card)

    src = src.replace('href="/coupons.html"', 'href="/fishgoo-coupons/"')

    guides_ssub = "Guides already ranking on this host — coupon, legit, shipping lines, FAQ. Not leftover dest copy."
    if guides_ssub in src:
        src = src.replace(
            guides_ssub,
            f"Independent Index · {ROWS}. Money URLs deepened on this hub — not leftover dest copy. Brand hub only — no country desks.",
        )

    if f"Independent Index · {ROWS}" not in src:
        raise SystemExit("Independent Index missing")
    if 'id="local"' not in src:
        raise SystemExit("#local missing")
    if 'href="/coupons.html"' in src:
        raise SystemExit("coupons.html href still present")
    return src


def patch_coupons(src: str) -> str:
    if 'name="coupons-truth"' not in src:
        src = src.replace(
            "<head>",
            '<head>\n<meta name="coupons-truth" content="/data/coupons-truth.json">',
            1,
        )
    src = src.replace(
        "<title>FishGoo Coupons 2026 — $500 New User &amp; ¥100 App</title>",
        f"<title>FishGoo Coupons 2026 — $500 New User &amp; ¥100 App · Updated {DATE_HUMAN}</title>",
    )
    src = src.replace(
        'content="Official FishGoo coupons measured on fishgoo.com 8 Oct 2026: up to $500 new-user shipping coupons and ¥100 app-exclusive. No public promo code. Screenshots included."',
        f'content="Working FishGoo coupon truth for 2026 (updated {DATE_HUMAN}). Official $500 new-user + ¥100 app exclusive — confirm_live. No typed-in FISHGOO10. Truth JSON: /data/coupons-truth.json."',
    )
    # og title may use non-escaped &
    src = src.replace(
        'content="FishGoo Coupons 2026 — $500 New User & ¥100 App"',
        f'content="FishGoo Coupons 2026 — $500 / ¥100 · Updated {DATE_HUMAN}"',
    )
    src = src.replace(
        'href="https://fishgoospreadsheet.net/coupons.html"',
        f'href="https://{HOST}/fishgoo-coupons/"',
    )
    src = src.replace(
        'content="https://fishgoospreadsheet.net/coupons.html"',
        f'content="https://{HOST}/fishgoo-coupons/"',
    )
    src = src.replace(
        'rel="canonical" href="https://fishgoospreadsheet.net/coupons.html"',
        f'rel="canonical" href="https://{HOST}/fishgoo-coupons/"',
    )

    old_nav = """<ul class="nl">
    <li><a href="/">Home</a></li>
    <li><a href="https://w2clinks.com/spreadsheet/fishgoo/" target="_blank" rel="noopener">Bestpicks</a></li>
    <li><a href="/finds.html">Forwarding</a></li>
    <li><a href="/shipping-guide.html">Freight Calculator</a></li>
    <li><a href="/beginner-guide.html">How to buy?</a></li>
    <li><a class="on" href="/coupons.html">Coupons</a></li>
    <li><a href="https://www.fishgoo.com/" rel="noopener">APP Download</a></li>
  </ul>"""
    new_nav = """<ul class="nl">
    <li><a href="/">Home</a></li>
    <li><a href="/#local">Hub</a></li>
    <li><a href="https://w2clinks.com/spreadsheet/fishgoo/" target="_blank" rel="noopener">Spreadsheet</a></li>
    <li><a class="on" href="/fishgoo-coupons/">Coupons</a></li>
    <li><a href="/finds-dataset/">Dataset</a></li>
    <li><a href="/shipping-guide.html">Shipping</a></li>
    <li><a href="https://www.fishgoo.com/" rel="noopener">Register</a></li>
  </ul>"""
    if old_nav in src:
        src = src.replace(old_nav, new_nav)

    faq_ld = (
        '<script type="application/ld+json">'
        '{"@context":"https://schema.org","@type":"FAQPage","mainEntity":['
        '{"@type":"Question","name":"What FishGoo coupons are confirm_live right now?",'
        '"acceptedAnswer":{"@type":"Answer","text":"Official fishgoo.com homepage measured 8 Oct 2026 shows up to $500 new-user shipping coupons and a ¥100 app-exclusive voucher after login. Offers credit in the account coupon centre — there is no public typed-in promo code. Status confirm_live; re-check the morning you pay. Truth JSON: /data/coupons-truth.json."}},'
        '{"@type":"Question","name":"Where should FishGoo coupon queries land?",'
        '"acceptedAnswer":{"@type":"Answer","text":"On fishgoospreadsheet.net/fishgoo-coupons/. Thin /coupons.html and /coupons/ redirect here. Brand hub only — no country spreadsheet desks."}},'
        '{"@type":"Question","name":"Is FISHGOO10 a real FishGoo code?",'
        '"acceptedAnswer":{"@type":"Answer","text":"No. Third-party FISHGOO10 / SHIP15 lists are not official. FishGoo uses account-based coupon centre credit after register / app login."}}'
        "]}"
        "</script>"
    )
    if "What FishGoo coupons are confirm_live" not in src:
        src = src.replace("</head>", faq_ld + "\n</head>", 1)

    callout = f"""
  <div class="truth-callout" style="background:#FFF7F0;border:1px solid #fed7aa;border-radius:12px;padding:14px 16px;margin:16px 0">
    <strong>Coupons truth · {DATE_HUMAN}</strong>
    <p>Primary public lines: <strong>up to $500 new-user shipping</strong> + <strong>¥100 app exclusive</strong> status <strong>confirm_live</strong> (measured fishgoo.com 8 Oct 2026). No typed-in FISHGOO10. Machine-readable: <a href="/data/coupons-truth.json">/data/coupons-truth.json</a>. Finds moat: <a href="/finds-dataset/">/finds-dataset/</a>. Thin <code>/coupons.html</code> · <code>/coupons/</code> 301 → this page. Brand hub only — no country desks. Hub stamp {DATE_HUMAN} · platform_opt={OPT}.</p>
  </div>
"""
    lead = (
        '<p class="ssub">Measured on the English SPA at <a href="https://www.fishgoo.com/" rel="noopener">fishgoo.com</a> on 8 Oct 2026. '
        "Offers credit in the account coupon centre. This page does not print an invite token. "
        "Third-party “FISHGOO10” lists are not official.</p>"
    )
    if lead not in src:
        # try curly/straight quote variants
        lead2 = lead.replace("“", '"').replace("”", '"')
        if lead2 in src:
            lead = lead2
        else:
            raise SystemExit("coupons lead paragraph missing")
    if f"Coupons truth · {DATE_HUMAN}" not in src:
        src = src.replace(lead, lead + "\n" + callout, 1)

    src = src.replace('href="/coupons.html"', 'href="/fishgoo-coupons/"')
    src = src.replace(">Coupon Codes</a>", ">Coupons truth</a>")
    return src


def write_jsons() -> None:
    data = ROOT / "data"
    data.mkdir(parents=True, exist_ok=True)
    truth = {
        "brand": BRAND,
        "host": HOST,
        "last_verified": DATE,
        "platform_opt": OPT,
        "verify_on": "fishgoo.com coupon centre / register / app login — confirm before pay",
        "update_cadence": "Coupons page copy + JSON stamped when official offers change (target weekly)",
        "serp_note": "28d clicks exclusive on /. Head terms fish go / fishgo spreadsheet. Spam cliff recovery: deepen Independent Index + coupons money URL + dataset.",
        "offers": [
            {
                "id": "fishgoo-new-user-500",
                "type": "new_user_gift",
                "label": "Up to $500 new-user shipping coupons",
                "code": None,
                "value_claim": "Official homepage 8 Oct 2026: $500 Shipping Coupons For New Users — account coupon centre credit after register; confirm_live",
                "status": "confirm_live",
                "expires_on": None,
                "expires_note": "No fixed expiry promised by this desk — re-confirm in-app the morning you pay",
                "applies_to": "FishGoo register / new-user coupon centre",
                "exclusions": [
                    "This hub is not checkout",
                    "Not a typed-in promo code",
                    "Third-party FISHGOO10 lists are not official",
                ],
                "source": f"https://{HOST}/fishgoo-coupons/",
                "last_verified": DATE,
            },
            {
                "id": "fishgoo-app-100",
                "type": "app_exclusive",
                "label": "¥100 app-exclusive voucher",
                "code": None,
                "value_claim": "Official login/home artwork ¥100 app exclusive; blog lists ¥50×2 no-minimum shipping after app download — confirm_live",
                "status": "confirm_live",
                "expires_on": None,
                "source": f"https://{HOST}/fishgoo-coupons/",
                "last_verified": DATE,
            },
            {
                "id": "fishgoo-zero-service-fee",
                "type": "fee_policy",
                "label": "0% purchasing fee",
                "code": None,
                "value_claim": "Evergreen official: service fee 0%. You still pay item + international freight — confirm_live",
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
        "generated_at": "2026-10-26T22:30:00Z",
        "row_count": ROWS_N,
        "row_count_display": ROWS,
        "update_frequency": "Catalog cards refresh via /api/products/; public dataset stamp reviewed at least weekly.",
        "qc_field": "qc_photo",
        "price_fields": ["price_cny", "price_usd_approx", "price_display"],
        "anti_sheet_note": "Public, citable row counts + dated category proofs — not another opaque Google Sheet dump. Coupon intent still lives on /fishgoo-coupons/.",
        "platform_opt": OPT,
        "hub_role": "brand_hub_only_no_country_desks",
        "twin_note": "GSC lists only fishgoospreadsheet.net. No keep country spreadsheet desks. Do not invent new country TLDs. Do not revive Phase C sunsets.",
        "endpoints": {
            "html": f"https://{HOST}/finds-dataset/",
            "json": f"https://{HOST}/data/finds-dataset.json",
            "coupons_truth": f"https://{HOST}/data/coupons-truth.json",
            "catalog": CATALOG,
            "api": f"https://{HOST}/api/products/",
            "hub": f"https://{HOST}/",
            "ranked_spreadsheet": f"https://{HOST}/fishgoo-spreadsheet.html",
        },
        "sitemap_policy": "Sitemap lastmod for /finds-dataset/, /fishgoo-coupons/ and money URLs bumps when this stamp changes.",
        "sample_skus": [
            {
                "sku": "cat_shoes",
                "title": "Shoes category proof (host HTML)",
                "price_cny": None,
                "price_display": "see /category-shoes.html",
                "category_hint": "SHOES",
                "source_url": f"https://{HOST}/category-shoes.html",
                "qc_photo": False,
                "last_verified": DATE,
            },
            {
                "sku": "cat_jersey",
                "title": "Jersey category proof (host HTML)",
                "price_cny": None,
                "price_display": "see /category-jersey.html",
                "category_hint": "JERSEY",
                "source_url": f"https://{HOST}/category-jersey.html",
                "qc_photo": False,
                "last_verified": DATE,
            },
            {
                "sku": "page_rimowa",
                "title": "Rimowa spreadsheet ranked article",
                "price_cny": None,
                "price_display": "see /fishgoo-rimowa-spreadsheet/",
                "category_hint": "RIMOWA",
                "source_url": f"https://{HOST}/fishgoo-rimowa-spreadsheet/",
                "qc_photo": False,
                "last_verified": DATE,
            },
            {
                "sku": "api_total",
                "title": f"/api/products/ total={ROWS_N}",
                "price_cny": None,
                "price_display": ROWS,
                "category_hint": "INDEX",
                "source_url": f"https://{HOST}/api/products/",
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
<title>FishGoo Finds Dataset — {ROWS} Rows, Category Proofs &amp; last_verified</title>
<meta name="description" content="Provable FishGoo spreadsheet dataset: {ROWS} rows, weekly freshness stamp, category proofs. Independent Index on {HOST} — not a Google Sheet dump. Coupons stay on /fishgoo-coupons/.">
<link rel="canonical" href="https://{HOST}/finds-dataset/">
<meta name="robots" content="index,follow">
<meta property="og:title" content="FishGoo Finds Dataset — Independent Index · {ROWS}">
<meta property="og:description" content="{ROWS} indexed finds with last_verified={DATE}. Public JSON + category proofs. Coupon truth is a separate JSON.">
<meta property="og:url" content="https://{HOST}/finds-dataset/">
<meta property="og:type" content="article">
<meta property="article:modified_time" content="{DATE}">
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"Dataset","name":"FishGoo spreadsheet finds dataset","description":"Public row counts, update frequency and category proofs for the independent FishGoo spreadsheet hub.","url":"https://{HOST}/finds-dataset/","creator":{{"@type":"Organization","name":"FishGoo Spreadsheet"}},"dateModified":"{DATE}","distribution":[{{"@type":"DataDownload","encodingFormat":"application/json","contentUrl":"https://{HOST}/data/finds-dataset.json"}},{{"@type":"DataDownload","encodingFormat":"application/json","contentUrl":"https://{HOST}/data/coupons-truth.json"}}],"variableMeasured":["sku","title","price","qc_photo","last_verified"]}}</script>
<style>
:root{{--acc:#FF7A45;--ink:#0A0A0A;--mute:#555;--line:#fed7aa;--bg:#FFF7F0;--ok:#166534;--okbg:#f0fdf4}}
*{{box-sizing:border-box}}body{{margin:0;font-family:DM Sans,Montserrat,system-ui,sans-serif;color:var(--ink);background:#fff;line-height:1.7}}
.top{{border-bottom:1px solid var(--line);background:#fff;position:sticky;top:0;z-index:5}}
.wrap{{max-width:860px;margin:0 auto;padding:0 20px}}
.top .wrap{{display:flex;gap:16px;align-items:center;min-height:56px;flex-wrap:wrap}}
.brand{{font-weight:700;text-decoration:none;color:var(--ink);font-size:15px}}
.nav a{{margin-left:12px;text-decoration:none;color:var(--mute);font-size:14px}}
.nav a:hover,.nav a.on{{color:var(--acc)}}
.hero{{padding:40px 0 16px;background:linear-gradient(180deg,#FFF7F0 0%,#fff 72%)}}
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
  <a class="brand" href="/">FishGoo Spreadsheet</a>
  <nav class="nav">
    <a href="/">Home</a>
    <a href="/fishgoo-coupons/">Coupons</a>
    <a href="/fishgoo-spreadsheet.html">Spreadsheet</a>
    <a href="/finds-dataset/" class="on">Dataset</a>
    <a href="/shipping-guide.html">Shipping</a>
  </nav>
</div></header>
<section class="hero"><div class="wrap">
  <div class="eyebrow">FishGoo Spreadsheet · Independent Index · brand hub</div>
  <h1>FishGoo finds dataset</h1>
  <p class="lead">Public row counts, update frequency and dated category proofs — so this hub is not “just another Sheet clone.” Coupon stacking stays on <a href="/fishgoo-coupons/">/fishgoo-coupons/</a>. No country spreadsheet desks for this brand. Phase C sunsets not revived.</p>
  <div class="stamp">last_verified <time datetime="{DATE}">{DATE}</time> · {ROWS} rows · platform_opt={OPT}</div>
</div></section>
<article class="wrap">
<div class="stats">
  <div class="stat"><b>{ROWS}</b><span>Indexed finds (API {ROWS_N})</span></div>
  <div class="stat"><b>weekly</b><span>Target stamp cadence</span></div>
  <div class="stat"><b>Coupons</b><span>Separate truth JSON</span></div>
  <div class="stat"><b>Hub-only</b><span>No country desks</span></div>
</div>

<div class="box">
  <h2 style="margin-top:0;font-size:20px">Why this page exists</h2>
  <p>GSC for this host concentrates 28d clicks on <strong>home</strong> after a spam cliff (90d residual → thin 28d). Spreadsheet / Independent Index queries need a falsifiable catalog claim: how many rows, when the stamp moved, and which category proofs back the count.</p>
  <p><a class="btn" href="/data/finds-dataset.json">Download finds-dataset.json</a>
     <a class="btn ghost" href="/data/coupons-truth.json">Coupons truth JSON</a>
     <a class="btn ghost" href="/fishgoo-coupons/">Coupon codes</a>
     <a class="btn ghost" href="{CATALOG}" rel="noopener">Open catalog</a></p>
</div>

<h2>Category / page proofs</h2>
<table>
  <thead><tr><th>Proof</th><th>Hint</th><th>last_verified</th></tr></thead>
  <tbody>
    <tr><td>Shoes category HTML</td><td>/category-shoes.html</td><td>{DATE}</td></tr>
    <tr><td>Jersey category HTML</td><td>/category-jersey.html</td><td>{DATE}</td></tr>
    <tr><td>Rimowa spreadsheet article</td><td>/fishgoo-rimowa-spreadsheet/</td><td>{DATE}</td></tr>
    <tr><td>API products total</td><td>/api/products/ = {ROWS_N}</td><td>{DATE}</td></tr>
  </tbody>
</table>

<div class="box">
  <h2 style="margin-top:0;font-size:20px">Hub vs country desk</h2>
  <p><strong>Brand hub = {HOST}.</strong> GSC lists only this property for FishGoo. Mixed geo impressions do not authorize a dest-country skin. Do not invent country spreadsheet TLDs. Do not revive Phase C sunsets. Ranked ~12–45KB inners stay 200 — not overwritten by Georgia dest skins.</p>
</div>
</article>
<footer><div class="wrap">Independent resource. Not affiliated with fishgoo.com. platform_opt={OPT}.</div></footer>
</body>
</html>
"""
    d = ROOT / "finds-dataset"
    d.mkdir(parents=True, exist_ok=True)
    (d / "index.html").write_text(html, encoding="utf-8")


def write_misc() -> None:
    (ROOT / "llms.txt").write_text(
        f"""# FishGoo Spreadsheet ({HOST})

> Independent Index · {ROWS} finds. Brand hub only — no country spreadsheet desks.

- Hub: https://{HOST}/
- Spreadsheet article: https://{HOST}/fishgoo-spreadsheet.html
- Live catalog: {CATALOG}
- Coupons (money): https://{HOST}/fishgoo-coupons/
- Coupons truth JSON: https://{HOST}/data/coupons-truth.json
- Finds dataset: https://{HOST}/finds-dataset/
- Dataset JSON: https://{HOST}/data/finds-dataset.json
- Shipping guide: https://{HOST}/shipping-guide.html
- Beginner / QC: https://{HOST}/beginner-guide.html
- API: https://{HOST}/api/products/

## Hub / sunset rules
- Brand hub only. No keep country spreadsheet desks. Do not invent new country TLDs.
- Do not revive Phase C sunsets. Do not drop leftover Georgia dest overlay over the ranked homepage.
- Thin /coupons/ and /coupons.html → /fishgoo-coupons/
- Official offers are account-based ($500 new-user / ¥100 app) — no typed-in FISHGOO10.

## Official
- {OFFICIAL} (checkout; confirm_live coupon centre)
- {EST} (freight estimator — pick a real country, not this hostname)

platform_opt={OPT}
last_verified={DATE}
""",
        encoding="utf-8",
    )

    (ROOT / "sitemap.xml").write_text(
        f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url><loc>https://{HOST}/</loc><lastmod>{DATE}</lastmod><changefreq>weekly</changefreq></url>
  <url><loc>https://{HOST}/fishgoo-spreadsheet.html</loc><lastmod>{DATE}</lastmod><changefreq>weekly</changefreq></url>
  <url><loc>https://{HOST}/fishgoo-coupons/</loc><lastmod>{DATE}</lastmod><changefreq>weekly</changefreq></url>
  <url><loc>https://{HOST}/finds-dataset/</loc><lastmod>{DATE}</lastmod><changefreq>weekly</changefreq></url>
  <url><loc>https://{HOST}/data/finds-dataset.json</loc><lastmod>{DATE}</lastmod><changefreq>weekly</changefreq></url>
  <url><loc>https://{HOST}/data/coupons-truth.json</loc><lastmod>{DATE}</lastmod><changefreq>weekly</changefreq></url>
  <url><loc>https://{HOST}/shipping-guide.html</loc><lastmod>{DATE}</lastmod><changefreq>weekly</changefreq></url>
  <url><loc>https://{HOST}/beginner-guide.html</loc><lastmod>{DATE}</lastmod><changefreq>monthly</changefreq></url>
  <url><loc>https://{HOST}/finds.html</loc><lastmod>{DATE}</lastmod><changefreq>weekly</changefreq></url>
  <url><loc>https://{HOST}/comparisons.html</loc><lastmod>{DATE}</lastmod><changefreq>monthly</changefreq></url>
  <url><loc>https://{HOST}/fishgoo-rimowa-spreadsheet/</loc><lastmod>{DATE}</lastmod><changefreq>weekly</changefreq></url>
  <url><loc>https://{HOST}/llms.txt</loc><lastmod>{DATE}</lastmod><changefreq>monthly</changefreq></url>
</urlset>
""",
        encoding="utf-8",
    )

    deploy_dir = ROOT / "_deploy"
    deploy_dir.mkdir(parents=True, exist_ok=True)
    (deploy_dir / "platform-opt.conf").write_text(
        f"""# FishGoo platform opt {DATE} — coupons money URL + JSON/dataset
# Brand hub only — no country desks; do not revive Phase C sunsets.
# NOTE: also patch ia-collapse.conf (drop fishgoo-coupons→/coupons/ rewrite)
# and retarget gsc-redirects /coupons → /fishgoo-coupons/ (exact locations win first-match).

location = /coupons.html {{ return 301 https://{HOST}/fishgoo-coupons/; }}
location = /fishgoo-coupon {{ return 301 https://{HOST}/fishgoo-coupons/; }}
location = /fishgoo-coupon/ {{ return 301 https://{HOST}/fishgoo-coupons/; }}
location = /fishgoo-coupons {{ return 301 https://{HOST}/fishgoo-coupons/; }}
location = /fishgoo-invite-code {{ return 301 https://{HOST}/fishgoo-coupons/; }}
location = /fishgoo-invite-code/ {{ return 301 https://{HOST}/fishgoo-coupons/; }}

location ^~ /fishgoo-coupons/ {{
  try_files $uri $uri/ /fishgoo-coupons/index.html;
}}
location ^~ /finds-dataset/ {{
  try_files $uri $uri/ /finds-dataset/index.html;
}}
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
""",
        encoding="utf-8",
    )

    (deploy_dir / "ia-collapse.conf").write_text(
        f"""# indie-agent-redesign: collapse cookie-cutter variants on {HOST}
# platform-opt {DATE}: fishgoo-coupons + invite-code now money-URL 200 (not → /coupons/)
rewrite ^/fishgoo-spreadsheet(?:-2026)?/?$ / permanent;
rewrite ^/fishgoo-shoes-spreadsheet/?$ / permanent;
rewrite ^/fishgoo-community/?$ / permanent;
rewrite ^/fishgoo-shipping-guide/?$ /shipping/ permanent;
rewrite ^/fishgoo-qc-guide/?$ /shipping/ permanent;
rewrite ^/fishgoo-refund-guide/?$ /shipping/ permanent;
rewrite ^/how-to-use-fishgoo/?$ /start/ permanent;
rewrite ^/is-fishgoo-legit/?$ /start/ permanent;
rewrite ^/blog/?$ / permanent;
location ~ ^/fishgoo-[a-z0-9-]+-spreadsheet {{ add_header X-Robots-Tag "noindex, follow" always; try_files $uri $uri/ $uri/index.html =404; }}
""",
        encoding="utf-8",
    )

    (deploy_dir / "gsc-redirects-coupons-snippet.txt").write_text(
        f"""# Replace these two lines inside gsc-redirects.conf:
# location = /coupons {{ return 301 https://{HOST}/coupons.html; }}
# location = /coupons/ {{ return 301 https://{HOST}/coupons.html; }}
# with:
location = /coupons {{ return 301 https://{HOST}/fishgoo-coupons/; }}
location = /coupons/ {{ return 301 https://{HOST}/fishgoo-coupons/; }}
""",
        encoding="utf-8",
    )

    (ROOT / "HOME-PATCH.md").write_text(
        f"""# HOME patch notes — {HOST}

Surgical on ranked homepage (title / CTAs / `#local` / nav / FAQ / hub-only narrative).
Do **not** wholesale overwrite with leftover Georgia dest skin in `overlay/index.html`.
Publish only `index.html.platform-patched`.
Brand hub only — **no** keep country desks. Do not revive Phase C sunsets.
API total {ROWS_N} → Independent Index · {ROWS}.
""",
        encoding="utf-8",
    )

    (ROOT / "DEPLOY-PLATFORM.md").write_text(
        f"""# Deploy — FishGoo platform opt ({DATE})

Origin: Baota host used by portfolio desks.  
Root: `/www/wwwroot/{HOST}`

## GUARDS

- **Do not** rsync leftover Georgia dest `overlay/index.html` over the ranked homepage — publish only `index.html.platform-patched`.
- **Do not** revive Phase C sunsets; do not invent country spreadsheet domains.
- Patch **ia-collapse.conf** so `/fishgoo-coupons/` is not rewritten to `/coupons/`.
- Retarget **gsc-redirects** `/coupons` · `/coupons/` → `/fishgoo-coupons/` (exact locations are first-match).
- Nginx vhost already `include .../extension/{HOST}/*.conf` (keep it).

## Files to push

```bash
HUB=/www/wwwroot/{HOST}
LOCAL=sites/{HOST}/overlay
BAK=/www/backup/fishgoo-platform-$(date +%Y%m%d-%H%M%S)
EXT=/www/server/panel/vhost/nginx/extension/{HOST}

mkdir -p "$BAK"
cp -a "$HUB/index.html" "$HUB/sitemap.xml" "$HUB/coupons.html" "$HUB/llms.txt" "$BAK/" 2>/dev/null || true
cp -a "$EXT" "$BAK/extension" 2>/dev/null || true

cp "$LOCAL/index.html.platform-patched" "$HUB/index.html"
mkdir -p "$HUB/fishgoo-coupons" "$HUB/finds-dataset" "$HUB/data"
cp "$LOCAL/fishgoo-coupons/index.html" "$HUB/fishgoo-coupons/index.html"
cp "$LOCAL/finds-dataset/index.html" "$HUB/finds-dataset/index.html"
cp "$LOCAL/data/"*.json "$HUB/data/"
cp "$LOCAL/llms.txt" "$LOCAL/sitemap.xml" "$HUB/"

cp "$LOCAL/_deploy/platform-opt.conf" "$EXT/platform-opt.conf"
cp "$LOCAL/_deploy/ia-collapse.conf" "$EXT/ia-collapse.conf"
# Retarget coupons aliases in gsc-redirects (exact location first-match)
sed -i 's#return 301 https://{HOST}/coupons.html;#return 301 https://{HOST}/fishgoo-coupons/;#g' \\
  "$EXT/gsc-redirects.conf"

nginx -t && nginx -s reload
```

## GSC

Submit `https://{HOST}/sitemap.xml` after deploy.

## Verify

- `/` title contains Independent Index · {ROWS}
- Hero CTAs Spreadsheet / Coupons / Dataset / Register; `#local` money URLs ≤6
- `/fishgoo-coupons/` has truth callout + {DATE_HUMAN} + FAQ-LD
- `/data/*.json` + `/finds-dataset/` + `/llms.txt` → 200
- `/coupons/` · `/coupons.html` → 301 `/fishgoo-coupons/`
""",
        encoding="utf-8",
    )


def main() -> None:
    src = LIVE.read_text(encoding="utf-8")
    patched = patch_home(src)
    (ROOT / "index.html.platform-patched").write_text(patched, encoding="utf-8")

    if not COUPONS_LIVE.is_file():
        raise SystemExit(f"missing {COUPONS_LIVE}")
    coupons_dir = ROOT / "fishgoo-coupons"
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
