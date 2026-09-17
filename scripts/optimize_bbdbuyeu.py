#!/usr/bin/env python3
"""Apply lit-buy-spreadsheet.com-style SEO to bbdbuyeu.net.

The competitor ranks on spaced/misspelled queries plus AI crawlers. This
script mirrors that playbook for BBDBuyEU:

  - WebSite.alternateName for bbd buy eu / bbdbuy spreadsheet / bbdbuyeu
  - FAQ + visible copy that maps those spellings to this hub
  - SoftwareApplication / ItemList / Breadcrumb schema
  - llms.txt + AI-bot robots.txt
  - Dedicated /tools/, /customs-calculator/, /sizing-guide/,
    /compare-shopping-agents/ landings
  - Crawlable /product/{slug}-{aid}/ long-tail pages from W2C

Usage:
  python3 scripts/optimize_bbdbuyeu.py --self-test
  python3 scripts/optimize_bbdbuyeu.py --build
  BBDBUYEU_DEPLOY_PASS='...' python3 scripts/optimize_bbdbuyeu.py --deploy
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from datetime import date
from html import escape
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
OVERLAY = ROOT / "sites" / "bbdbuyeu.net" / "overlay"
DOMAIN = "bbdbuyeu.net"
BASE = f"https://{DOMAIN}"
TODAY = date.today().isoformat()
HOST = os.environ.get(
    "BBDBUYEU_DEPLOY_HOST",
    os.environ.get("ORIENTDIG_DEPLOY_HOST", "31.97.41.31"),
)
USER = os.environ.get(
    "BBDBUYEU_DEPLOY_USER",
    os.environ.get("ORIENTDIG_DEPLOY_USER", "root"),
)
WEBROOT = f"/www/wwwroot/{DOMAIN}"

ALTERNATE_NAMES = [
    "BBDBuyEU Sheet",
    "BBDBuyEU Spreadsheets",
    "BBDBuy Spreadsheet",
    "BBD Buy Spreadsheet",
    "BBD Buy EU Spreadsheet",
    "BBDBuy EU Spreadsheet",
    "Best BBDBuyEU Spreadsheet 2026",
    "BBDBuy Sheet",
    "bbd buy eu spreadsheet",
    "bbd buy spreadsheet",
    "bbdbuy spreadsheet",
    "bbdbuyeu spreadsheet",
    "bbd buy eu sheet",
    "bbdbuy eu spreadsheet",
    "bbd buy eu",
]

CATEGORIES = [
    ("Sneakers & Shoes", "/bbdbuyeu-shoes-spreadsheet/", "shoes"),
    ("T-Shirts", "/bbdbuyeu-spreadsheet/", "tshirts"),
    ("Hoodies", "/bbdbuyeu-spreadsheet/", "hoodies"),
    ("Shorts", "/bbdbuyeu-spreadsheet/", "shorts"),
    ("Long Sleeved", "/bbdbuyeu-spreadsheet/", "longsleeved"),
    ("Jackets & Coats", "/bbdbuyeu-spreadsheet/", "jackets"),
    ("Trousers / Pants", "/bbdbuyeu-spreadsheet/", "pants"),
    ("Sweaters", "/bbdbuyeu-spreadsheet/", "sweaters"),
    ("Bags", "/bbdbuyeu-spreadsheet/", "bags"),
    ("Hats & Headwear", "/bbdbuyeu-spreadsheet/", "headwear"),
    ("Sports Jerseys", "/bbdbuyeu-spreadsheet/", "jersey"),
    ("Electronics", "/bbdbuyeu-spreadsheet/", "electronics"),
]

SIDEBAR_CATS = [
    ("shoes", "SNEAKERS"),
    ("tshirts", "T-SHIRT"),
    ("hoodies", "HOODIE"),
    ("shorts", "SHORTS"),
    ("longsleeved", "LONG SLEEVED"),
    ("jackets", "JACKET"),
    ("pants", "TROUSERS"),
    ("sweaters", "SWEATER"),
    ("bags", "BAG"),
    ("headwear", "HAT"),
    ("jersey", "Jersey"),
    ("electronics", "Electronics"),
]

STATS_API = "https://w2clinks.com/public/typesense-search.php"

_STATS: dict | None = None


def catalog_stats() -> dict:
    """Live catalog totals from /api/search.php. Falls back to last known counts."""
    global _STATS
    if _STATS is not None:
        return _STATS
    stats = {
        "found": 10024,
        "categories": {key: 0 for key, _api in SIDEBAR_CATS},
    }
    try:
        def found_for(params: dict) -> int:
            req = Request(
                f"{STATS_API}?{urlencode(params)}",
                headers={"User-Agent": "BBDBuyEUSEO/1.0", "Accept": "application/json"},
            )
            with urlopen(req, timeout=20) as resp:
                data = json.loads(resp.read().decode("utf-8", "replace"))
            return int(data.get("found") or 0)

        stats["found"] = found_for({"page": 1, "per_page": 1, "sort": "newest"})
        cats: dict[str, int] = {}
        for key, api_cat in SIDEBAR_CATS:
            cats[key] = found_for({"page": 1, "per_page": 1, "category": api_cat})
        stats["categories"] = cats
    except Exception:
        pass
    _STATS = stats
    return stats


def count_exact(n: int | None = None) -> str:
    return f"{int(n if n is not None else catalog_stats()['found']):,}"


def count_plus(n: int | None = None) -> str:
    found = int(n if n is not None else catalog_stats()["found"])
    return f"{(found // 1000) * 1000:,}+"


FAQ_EXTRA = [
    {
        "name": "Is this the same as \"bbd buy eu spreadsheet\" or \"bbd buy spreadsheet\"?",
        "text": (
            "Yes — \"bbd buy eu\", \"bbdbuy eu\", \"bbd buy\" and \"bbdbuyeu\" are "
            "common spellings for the same EU shopping agent. This hub is the "
            "BBDBuyEU spreadsheet regardless of how it is spelled. Invite code "
            "1QodRw and coupon BBD5OFF still apply."
        ),
    },
    {
        "name": "Is BBDBuy the same as BBDBuyEU?",
        "text": (
            "Yes for this catalog. W2C lists the sheet as bbdbuy; checkout is "
            "on bbdbuyeu.com (BBDBuyEU). Browse the on-site spreadsheet or the "
            "W2C bbdbuy sheet — same product rows, QC photos and live links."
        ),
    },
]


def _jsonld_graph() -> dict:
    faq_entities = [
        {
            "@type": "Question",
            "name": "What is the BBDBuyEU Spreadsheet?",
            "acceptedAnswer": {
                "@type": "Answer",
                "text": f"A curated database of {count_plus()} products from Taobao, Weidian and 1688 with live product links, USD pricing and QC photos.",
            },
        },
        {
            "@type": "Question",
            "name": FAQ_EXTRA[0]["name"],
            "acceptedAnswer": {"@type": "Answer", "text": FAQ_EXTRA[0]["text"]},
        },
        {
            "@type": "Question",
            "name": FAQ_EXTRA[1]["name"],
            "acceptedAnswer": {"@type": "Answer", "text": FAQ_EXTRA[1]["text"]},
        },
        {
            "@type": "Question",
            "name": "Is the BBDBuyEU Spreadsheet free?",
            "acceptedAnswer": {
                "@type": "Answer",
                "text": "Yes — browsing is completely free. No signup required until you place an order on BBDBuyEU.",
            },
        },
        {
            "@type": "Question",
            "name": "How often is it updated?",
            "acceptedAnswer": {
                "@type": "Answer",
                "text": "New products are added daily. Broken links are removed weekly.",
            },
        },
        {
            "@type": "Question",
            "name": "Is BBDBuyEU safe to use?",
            "acceptedAnswer": {
                "@type": "Answer",
                "text": "BBDBuyEU uses escrow payments and warehouse QC photos. See the Is BBDBuyEU Legit? guide on this site.",
            },
        },
        {
            "@type": "Question",
            "name": "Does BBDBuyEU have coupon codes?",
            "acceptedAnswer": {
                "@type": "Answer",
                "text": "Yes — use BBD5OFF for 5% off. See the coupons page.",
            },
        },
    ]
    return {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "WebSite",
                "@id": f"{BASE}/#website",
                "name": "BBDBuyEU Spreadsheet 2026",
                "alternateName": ALTERNATE_NAMES,
                "description": f"The #1 free BBDBuyEU spreadsheet with {count_plus()} verified products from Taobao, 1688 and Weidian.",
                "url": f"{BASE}/",
                "inLanguage": "en",
                "dateModified": TODAY,
                "potentialAction": {
                    "@type": "SearchAction",
                    "target": f"{BASE}/bbdbuyeu-spreadsheet/?q={{search_term_string}}",
                    "query-input": "required name=search_term_string",
                },
            },
            {
                "@type": "Organization",
                "@id": f"{BASE}/#org",
                "name": "BBDBuyEU Spreadsheet",
                "legalName": "BBDBuyEU Spreadsheet (Independent)",
                "url": f"{BASE}/",
                "logo": "https://www.bbdbuyeu.com/logo.png",
                "description": "Independent BBDBuyEU spreadsheet hub. Not affiliated with bbdbuyeu.com.",
            },
            {
                "@type": "SoftwareApplication",
                "name": "BBDBuyEU Spreadsheet",
                "applicationCategory": "ShoppingApplication",
                "operatingSystem": "Web",
                "url": f"{BASE}/bbdbuyeu-spreadsheet/",
                "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"},
                "featureList": [
                    "Live Taobao, Weidian and 1688 product links",
                    "QC photo references",
                    "USD pricing",
                    "Category filters",
                ],
            },
            {
                "@type": "CollectionPage",
                "@id": f"{BASE}/#collection",
                "name": "BBDBuyEU Spreadsheet 2026",
                "url": f"{BASE}/",
                "about": "BBDBuyEU spreadsheet and BBDBuy spreadsheet product catalog",
            },
            {
                "@type": "ItemList",
                "name": "BBDBuyEU Spreadsheet Categories",
                "itemListOrder": "https://schema.org/ItemListOrderAscending",
                "numberOfItems": len(CATEGORIES),
                "itemListElement": [
                    {
                        "@type": "ListItem",
                        "position": i,
                        "name": name,
                        "url": f"{BASE}{path}",
                    }
                    for i, (name, path, _count) in enumerate(CATEGORIES, 1)
                ],
            },
            {
                "@type": "BreadcrumbList",
                "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{BASE}/"},
                    {
                        "@type": "ListItem",
                        "position": 2,
                        "name": "BBDBuyEU Spreadsheet",
                        "item": f"{BASE}/bbdbuyeu-spreadsheet/",
                    },
                ],
            },
            {
                "@type": "Service",
                "name": "BBDBuyEU Spreadsheet Guide",
                "serviceType": "Product discovery spreadsheet",
                "provider": {"@id": f"{BASE}/#org"},
                "areaServed": ["US", "UK", "CA", "AU", "EU"],
                "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"},
            },
            {"@type": "FAQPage", "mainEntity": faq_entities},
            {
                "@type": "HowTo",
                "name": "How to Use the BBDBuyEU Spreadsheet",
                "step": [
                    {
                        "@type": "HowToStep",
                        "position": 1,
                        "name": "Browse or search",
                        "text": "Open the BBDBuyEU spreadsheet and filter by category or brand.",
                    },
                    {
                        "@type": "HowToStep",
                        "position": 2,
                        "name": "Check QC and prices",
                        "text": "Review USD pricing and product images before ordering.",
                    },
                    {
                        "@type": "HowToStep",
                        "position": 3,
                        "name": "Copy the product link",
                        "text": "Open the W2C product page and copy the Taobao, Weidian or 1688 URL.",
                    },
                    {
                        "@type": "HowToStep",
                        "position": 4,
                        "name": "Paste into BBDBuyEU",
                        "text": "Register on BBDBuyEU (bbdbuyeu.com) and paste the link. Invite 1QodRw.",
                    },
                    {
                        "@type": "HowToStep",
                        "position": 5,
                        "name": "Review warehouse QC",
                        "text": "Approve or reject QC photos before international shipping.",
                    },
                ],
            },
        ],
    }


def jsonld_script() -> str:
    payload = json.dumps(_jsonld_graph(), ensure_ascii=False, separators=(",", ":"))
    json.loads(payload)
    return f'<script type="application/ld+json">{payload}</script>'


# Keep in sync with lit-buy-spreadsheet.com: allow search + AI crawlers on
# HTML landings. Cloudflare "Block AI bots" still overrides this at the edge.
_AI_ALLOW = """Allow: /
Allow: /product/
Allow: /blog/
Allow: /bbdbuyeu-spreadsheet
Allow: /bbdbuyeu-spreadsheet-2026
Allow: /tools/
Allow: /customs-calculator
Allow: /sizing-guide
Allow: /compare-shopping-agents
Allow: /llms.txt
Disallow: /api/
Disallow: /admin/
"""

ROBOTS_TXT = f"""User-Agent: *
Allow: /
Disallow: /api/
Disallow: /.bak
Disallow: /admin/

User-Agent: Googlebot
{_AI_ALLOW}
User-Agent: Googlebot-Image
Allow: /
Allow: /product/
Disallow: /api/
Disallow: /admin/

User-Agent: Bingbot
{_AI_ALLOW}
User-Agent: GPTBot
{_AI_ALLOW}
User-Agent: ChatGPT-User
{_AI_ALLOW}
User-Agent: OAI-SearchBot
{_AI_ALLOW}
User-Agent: PerplexityBot
{_AI_ALLOW}
User-Agent: Anthropic-AI
{_AI_ALLOW}
User-Agent: ClaudeBot
{_AI_ALLOW}
User-Agent: Claude-SearchBot
{_AI_ALLOW}
User-Agent: Claude-User
{_AI_ALLOW}
User-Agent: Google-Extended
Allow: /
Allow: /product/
Allow: /blog/
Allow: /llms.txt

User-Agent: Applebot
Allow: /
Allow: /product/
Disallow: /api/

Sitemap: https://bbdbuyeu.net/sitemap.xml
Sitemap: https://bbdbuyeu.net/sitemap-products.xml
"""

LLMS_TXT = """# BBDBuyEU Spreadsheet (BBDBuy Spreadsheet)

> Independent BBDBuyEU spreadsheet for Chinese e-commerce. Browse 8,600+ live products from Taobao, 1688 and Weidian with QC photos, working links and USD pricing. Not a store — discovery only. Checkout happens on BBDBuyEU (bbdbuyeu.com). Invite 1QodRw. Coupon BBD5OFF.

## Also searched as

- bbd buy eu spreadsheet
- bbd buy spreadsheet
- bbdbuy spreadsheet
- bbdbuyeu spreadsheet
- bbd buy eu sheet
- bbdbuy sheet

These spellings all refer to the same catalog on https://bbdbuyeu.net/

## Key facts

- 8,600+ live product listings refreshed from W2C
- Categories: sneakers, slippers, t-shirts, polo, shorts, hoodies, jackets, trousers, jerseys, electronics, bags, jewelry
- Platforms: Taobao, 1688, Weidian
- Free to browse — no account required
- Independent of www.bbdbuyeu.com

## Key pages

- Homepage: https://bbdbuyeu.net/
- BBDBuyEU spreadsheet: https://bbdbuyeu.net/bbdbuyeu-spreadsheet/
- BBDBuy spreadsheet: https://bbdbuyeu.net/bbdbuyeu-spreadsheet-2026/
- Coupons: https://bbdbuyeu.net/bbdbuyeu-coupons/
- Is BBDBuyEU legit?: https://bbdbuyeu.net/is-bbdbuyeu-legit/
- How to use BBDBuyEU: https://bbdbuyeu.net/how-to-use-bbdbuyeu/
- Shipping guide: https://bbdbuyeu.net/bbdbuyeu-shipping-guide/
- Customs / duty calculator: https://bbdbuyeu.net/customs-calculator/
- Chinese size chart: https://bbdbuyeu.net/sizing-guide/
- Shopping agent comparison: https://bbdbuyeu.net/compare-shopping-agents/
- BBDBuy vs BBDBuyEU: https://bbdbuyeu.net/is-bbdbuyeu-legit/
- Tools: https://bbdbuyeu.net/tools/
- Product long-tail pages: https://bbdbuyeu.net/product/
- Blog: https://bbdbuyeu.net/blog/

## Common questions

Q: Is BBDBuy the same as BBDBuyEU?
A: W2C lists the sheet as bbdbuy. Checkout is on bbdbuyeu.com (BBDBuyEU). Same catalog rows, QC photos and live links.

Q: Is the BBDBuyEU spreadsheet free?
A: Yes. You only pay when you order through the agent.

Q: Where do product links come from?
A: Live W2C catalog rows pointing at Taobao, Weidian and 1688 listings.

Q: Is this the official BBDBuyEU website?
A: No. bbdbuyeu.net is an independent English guide hub.
"""


def _shell(title: str, description: str, canonical: str, body: str, extra_head: str = "") -> str:
    title_e = escape(title)
    desc_e = escape(description)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>{title_e}</title>
<meta name="description" content="{desc_e}">
<meta name="robots" content="index, follow, max-image-preview:large">
<link rel="canonical" href="{canonical}">
<link rel="icon" href="https://www.bbdbuyeu.com/favicon.ico">
<style>
:root{{--acc:#f0700c;--acd:#c45a0a;--acl:#FFF0E6;--bk:#0A0A0A;--g2:#2D2D2D;--g4:#888;--g5:#E5E5E5;--wh:#fff;--f:DM Sans,system-ui,sans-serif}}
body{{font-family:var(--f);margin:0;color:var(--bk);background:var(--wh);line-height:1.7}}
a{{color:var(--acc)}}
.topbar{{background:var(--acc);color:#fff;text-align:center;padding:9px 16px;font-size:13px}}
.topbar a{{color:#fff}}
nav.nav{{display:flex;gap:16px;align-items:center;padding:12px 24px;border-bottom:1px solid var(--g5)}}
.nav__logo{{font-weight:700;color:var(--bk);text-decoration:none}}
.nav__links{{display:flex;gap:8px;list-style:none;margin:0;padding:0;flex-wrap:wrap}}
.nav__links a{{color:var(--g4);text-decoration:none;padding:6px 10px}}
main{{max-width:960px;margin:0 auto;padding:24px}}
.hero h1,.section h1{{font-size:clamp(28px,5vw,44px)}}
.hero__sub,.section-sub{{color:var(--g2)}}
.feature-grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:16px}}
.feature-card{{border:1px solid var(--g5);border-radius:12px;padding:18px;text-decoration:none;color:var(--bk);display:block}}
.btn{{display:inline-block;padding:10px 16px;border-radius:8px;background:var(--acc);color:#fff;border:0;cursor:pointer}}
footer{{padding:28px 24px;border-top:1px solid var(--g5);color:var(--g4);font-size:13px}}
main table{{width:100%;border-collapse:collapse;margin:16px 0}}
main th,main td{{border-bottom:1px solid #e5e5e5;padding:8px 10px;text-align:left}}
main label{{display:flex;flex-direction:column;gap:6px;font-size:.9rem}}
main select,main input[type=number]{{padding:10px;border:1px solid #ddd;border-radius:8px}}
</style>
<meta property="og:title" content="{title_e}">
<meta property="og:description" content="{desc_e}">
<meta property="og:url" content="{canonical}">
<meta property="og:type" content="website">
{extra_head}
</head>
<body>
<div class="topbar">2026 Update: Code <strong>BBD5OFF</strong> — 5% off · <a href="/bbdbuyeu-coupons/">Get code →</a></div>
<nav class="nav" aria-label="Main navigation">
  <div class="container nav__inner">
    <a href="/" class="nav__logo">BBDBuyEU Spreadsheet</a>
    <ul class="nav__links" role="list">
      <li><a href="/">Home</a></li>
      <li><a href="/bbdbuyeu-spreadsheet/">Spreadsheet</a></li>
      <li><a href="/bbdbuyeu-spreadsheet-2026/">BBDBuy Spreadsheet</a></li>
      <li><a href="/tools/">Tools</a></li>
      <li><a href="/blog/">Blog</a></li>
      <li><a href="/bbdbuyeu-coupons/">Coupons</a></li>
    </ul>
  </div>
</nav>
<main>
{body}
</main>
<footer class="footer" role="contentinfo">
  <div class="container">
    <p>Independent BBDBuyEU spreadsheet resource — not affiliated with bbdbuyeu.com.</p>
    <p><a href="/">Home</a> · <a href="/bbdbuyeu-spreadsheet/">Spreadsheet</a> · <a href="/tools/">Tools</a> · <a href="/customs-calculator/">Duty calculator</a> · <a href="/sizing-guide/">Size chart</a> · <a href="/compare-shopping-agents/">Agent comparison</a></p>
  </div>
</footer>
</body>
</html>
"""


def tools_page() -> str:
    body = """
<section class="hero">
  <div class="container">
    <p class="hero__eyebrow">BBDBuyEU tools</p>
    <h1>Free Tools for BBDBuyEU Shopping</h1>
    <p class="hero__sub">Calculators, size charts, agent comparison and guides for Taobao, 1688 and Weidian — the same independent-tool setup used by spreadsheet hubs. All free, no signup.</p>
  </div>
</section>
<section class="section">
  <div class="container">
    <div class="feature-grid">
      <a class="feature-card" href="/customs-calculator/">
        <h2 class="feature-card__title">Import duty calculator</h2>
        <p class="feature-card__desc">Estimate VAT/GST and duty using published thresholds for US, UK, EU, Canada, Australia and New Zealand. Category selector included.</p>
      </a>
      <a class="feature-card" href="/sizing-guide/">
        <h2 class="feature-card__title">Chinese size chart</h2>
        <p class="feature-card__desc">CN to US / EU / UK / AU for men's and women's clothing and shoes, plus foot length in centimetres.</p>
      </a>
      <a class="feature-card" href="/compare-shopping-agents/">
        <h2 class="feature-card__title">Shopping agent comparison</h2>
        <p class="feature-card__desc">BBDBuyEU vs Kakobuy, CNFans, Superbuy, LitBuy and Pandabuy — fees, QC, storage and shipping.</p>
      </a>
      <a class="feature-card" href="/bbdbuyeu-shipping-guide/">
        <h2 class="feature-card__title">Shipping &amp; customs guides</h2>
        <p class="feature-card__desc">Lines, times, QC rejection and the country customs write-up on this hub.</p>
      </a>
    </div>
  </div>
</section>
"""
    return _shell(
        "Free BBDBuyEU Tools 2026 — Duty Calculator, Size Chart, Agent Comparison",
        "Free BBDBuyEU tools: import duty calculator, Chinese size chart and shopping agent comparison. No signup.",
        f"{BASE}/tools/",
        body,
    )


def customs_page() -> str:
    body = """
<section class="hero">
  <div class="container">
    <p class="hero__eyebrow">BBDBuyEU customs</p>
    <h1>Import Duty Calculator 2026</h1>
    <p class="hero__sub">Estimate VAT/GST and customs duty for BBDBuyEU parcels. Educational calculator using published destination thresholds — not legal advice. Confirm current rules with your customs authority before you ship.</p>
  </div>
</section>
<section class="section">
  <div class="container" style="max-width:820px">
    <form id="duty-form" style="display:grid;gap:12px;grid-template-columns:1fr 1fr;max-width:640px">
      <label>Declared value (USD)
        <input id="declared" type="number" min="1" value="120" required>
      </label>
      <label>Destination
        <select id="dest">
          <option value="US">United States</option>
          <option value="UK">United Kingdom</option>
          <option value="EU">European Union</option>
          <option value="CA">Canada</option>
          <option value="AU">Australia</option>
          <option value="NZ">New Zealand</option>
        </select>
      </label>
      <label>Category
        <select id="cat">
          <option value="clothing">Clothing / shoes</option>
          <option value="electronics">Electronics</option>
          <option value="other">Other goods</option>
        </select>
      </label>
      <button type="submit" class="btn btn-primary" style="grid-column:1/-1">Estimate</button>
    </form>
    <p id="duty-out" class="section-sub" style="margin-top:20px"></p>
    <h2>How this BBDBuyEU calculator works</h2>
    <p>Built for searches such as <strong>bbdbuyeu customs</strong>, <strong>bbdbuyeu duty</strong> and <strong>bbdbuyeu import tax</strong>. Thresholds change; treat the numbers as a starting point:</p>
    <ul>
      <li><strong>United States</strong> — de minimis treatment has been changing; verify CBP before you ship.</li>
      <li><strong>United Kingdom</strong> — VAT commonly 20%; customs duty often starts above £135 and depends on HS code.</li>
      <li><strong>EU</strong> — VAT is usually due at the destination rate; customs duty commonly starts above €150.</li>
      <li><strong>Canada</strong> — general goods de minimis is low; GST/HST may still apply.</li>
      <li><strong>Australia</strong> — GST often 10%, with a high-value threshold around AUD $1,000.</li>
      <li><strong>New Zealand</strong> — GST commonly 15% on imported goods.</li>
    </ul>
    <p>Declare the accurate transaction value. Undervaluing a parcel to avoid tax is illegal. Country write-ups: <a href="/blog/posts/bbdbuyeu-customs-guide/">customs guide</a> and <a href="/bbdbuyeu-shipping-guide/">shipping guide</a>.</p>
  </div>
</section>
<script>
const RULES = {
  US: {vat: 0, note: "US import rules are in flux. Confirm current CBP de minimis before shipping."},
  UK: {vat: 0.20, note: "UK VAT is commonly 20%. Duty depends on HS code above the duty-free threshold."},
  EU: {vat: 0.19, note: "Illustrative 19% VAT. Use the destination country rate; duty depends on HS code."},
  CA: {vat: 0.05, note: "Illustrative 5% GST. Provincial HST/PST may add more."},
  AU: {vat: 0.10, note: "Illustrative 10% GST. Confirm the live GST registration threshold."},
  NZ: {vat: 0.15, note: "Illustrative 15% GST on imported goods."}
};
const DUTY = {clothing: 0.08, electronics: 0.05, other: 0.04};
document.getElementById("duty-form").addEventListener("submit", function (e) {
  e.preventDefault();
  const value = Number(document.getElementById("declared").value || 0);
  const dest = document.getElementById("dest").value;
  const cat = document.getElementById("cat").value;
  const rule = RULES[dest];
  const dutyRate = dest === "US" ? 0 : (DUTY[cat] || 0);
  const vat = value * rule.vat;
  const duty = value * dutyRate;
  const total = value + vat + duty;
  document.getElementById("duty-out").textContent =
    "Estimated landed cost about USD " + total.toFixed(2) +
    " (goods " + value.toFixed(2) + " + tax " + vat.toFixed(2) +
    " + illustrative duty " + duty.toFixed(2) + "). " + rule.note;
});
</script>
"""
    return _shell(
        "Import Duty Calculator 2026 — BBDBuyEU Customs Estimator",
        "Estimate BBDBuyEU import VAT and duty for US, UK, EU, Canada, Australia and New Zealand. Educational calculator, not legal advice.",
        f"{BASE}/customs-calculator/",
        body,
    )


def sizing_page() -> str:
    body = """
<section class="hero">
  <div class="container">
    <p class="hero__eyebrow">BBDBuyEU sizing</p>
    <h1>Chinese Size Chart 2026</h1>
    <p class="hero__sub">Convert CN sizes to US, EU, UK and AU for clothes and shoes before you order from the BBDBuyEU spreadsheet. Chinese letter sizes usually run small.</p>
  </div>
</section>
<section class="section">
  <div class="container" style="max-width:820px">
    <h2>Men's clothing (tops)</h2>
    <table>
      <thead><tr><th>CN</th><th>US</th><th>UK</th><th>EU</th><th>AU</th></tr></thead>
      <tbody>
        <tr><td>165 / S</td><td>XS</td><td>34</td><td>44</td><td>XS</td></tr>
        <tr><td>170 / M</td><td>S</td><td>36</td><td>46</td><td>S</td></tr>
        <tr><td>175 / L</td><td>M</td><td>38</td><td>48</td><td>M</td></tr>
        <tr><td>180 / XL</td><td>L</td><td>40</td><td>50</td><td>L</td></tr>
        <tr><td>185 / XXL</td><td>XL</td><td>42</td><td>52</td><td>XL</td></tr>
      </tbody>
    </table>
    <h2>Women's clothing (tops)</h2>
    <table>
      <thead><tr><th>CN</th><th>US</th><th>UK</th><th>EU</th></tr></thead>
      <tbody>
        <tr><td>155 / S</td><td>XS / 2</td><td>6</td><td>32</td></tr>
        <tr><td>160 / M</td><td>S / 4</td><td>8</td><td>34</td></tr>
        <tr><td>165 / L</td><td>M / 6</td><td>10</td><td>36</td></tr>
        <tr><td>170 / XL</td><td>L / 8</td><td>12</td><td>38</td></tr>
        <tr><td>175 / XXL</td><td>XL / 10</td><td>14</td><td>40</td></tr>
      </tbody>
    </table>
    <h2>Men's shoes (EU last)</h2>
    <table>
      <thead><tr><th>CN / EU</th><th>US M</th><th>UK</th><th>Foot (cm)</th></tr></thead>
      <tbody>
        <tr><td>39</td><td>6.5</td><td>6</td><td>24.5</td></tr>
        <tr><td>40</td><td>7</td><td>6.5</td><td>25.0</td></tr>
        <tr><td>41</td><td>8</td><td>7</td><td>25.5</td></tr>
        <tr><td>42</td><td>8.5</td><td>8</td><td>26.0</td></tr>
        <tr><td>43</td><td>9.5</td><td>9</td><td>27.0</td></tr>
        <tr><td>44</td><td>10.5</td><td>10</td><td>27.5</td></tr>
        <tr><td>45</td><td>11.5</td><td>11</td><td>28.5</td></tr>
        <tr><td>46</td><td>12.5</td><td>12</td><td>29.0</td></tr>
      </tbody>
    </table>
    <h2>Women's shoes</h2>
    <table>
      <thead><tr><th>CN / EU</th><th>US W</th><th>UK</th><th>Foot (cm)</th></tr></thead>
      <tbody>
        <tr><td>35</td><td>5</td><td>2.5</td><td>22.0</td></tr>
        <tr><td>36</td><td>6</td><td>3.5</td><td>22.5</td></tr>
        <tr><td>37</td><td>6.5</td><td>4</td><td>23.5</td></tr>
        <tr><td>38</td><td>7.5</td><td>5</td><td>24.0</td></tr>
        <tr><td>39</td><td>8.5</td><td>6</td><td>24.5</td></tr>
        <tr><td>40</td><td>9.5</td><td>7</td><td>25.5</td></tr>
      </tbody>
    </table>
    <p>Always prefer the seller's centimetre chart over a generic letter size. Longer write-up: <a href="/blog/posts/bbdbuyeu-sizing-guide/">BBDBuyEU sizing guide</a>.</p>
  </div>
</section>
"""
    return _shell(
        "Chinese Size Chart 2026 — CN to US / EU / UK for BBDBuyEU",
        "Chinese size conversion for the BBDBuyEU spreadsheet: men's and women's clothing and shoes, with foot length in centimetres.",
        f"{BASE}/sizing-guide/",
        body,
    )


def compare_page() -> str:
    body = """
<section class="hero">
  <div class="container">
    <p class="hero__eyebrow">Updated 2026</p>
    <h1>Which Chinese Shopping Agent is Best in 2026?</h1>
    <p class="hero__sub">Side-by-side look at BBDBuyEU, Kakobuy, CNFans, Superbuy, LitBuy and Pandabuy — fees, QC photos, storage and shipping. This hub's spreadsheet is built for BBDBuyEU checkout.</p>
  </div>
</section>
<section class="section">
  <div class="container">
    <table>
      <thead>
        <tr><th>Agent</th><th>Service fee</th><th>QC photos</th><th>Free storage</th><th>Best for</th></tr>
      </thead>
      <tbody>
        <tr><td>BBDBuyEU</td><td>0%</td><td>Free, unlimited</td><td>Often 90–180 days</td><td>This spreadsheet</td></tr>
        <tr><td>Kakobuy</td><td>Varies</td><td>Warehouse QC</td><td>Agent policy</td><td>EU / invite-code users</td></tr>
        <tr><td>CNFans</td><td>Often 0%</td><td>Free QC</td><td>Long storage on many plans</td><td>Community threads</td></tr>
        <tr><td>Superbuy</td><td>Often 0%</td><td>Limited free photos</td><td>~90 days</td><td>Beginners</td></tr>
        <tr><td>LitBuy</td><td>About 5–10%</td><td>Free QC</td><td>~90 days</td><td>Shipping-line choice</td></tr>
        <tr><td>Pandabuy</td><td>Often 0%</td><td>Free QC</td><td>~90 days</td><td>Legacy rep users</td></tr>
      </tbody>
    </table>
    <h2>What 0% fees actually mean</h2>
    <p>BBDBuy, CNFans, Superbuy and Pandabuy often advertise 0% item fees. Revenue still has to come from somewhere — usually shipping markups. LitBuy states a service fee and may price freight closer to cost. Always compare <strong>item + fee + freight</strong> for your haul weight, not the headline percentage.</p>
    <h2>BBDBuy vs BBDBuyEU</h2>
    <p>W2C labels this catalog <strong>bbdbuy</strong>; checkout is <strong>BBDBuyEU</strong> on bbdbuyeu.com. That is a sheet-vs-agent naming split, not an AllChinaBuy/ACBuy-style rebrand. Browse the <a href="/bbdbuyeu-spreadsheet/">BBDBuyEU spreadsheet</a> or the W2C bbdbuy sheet — same rows.</p>
    <h2>FAQ</h2>
    <h3>Which agent is cheapest?</h3>
    <p>The cheapest checkout is the lowest landed cost after shipping, not the lowest advertised fee. Weigh a 2–5 kg haul on two agents before you standardise.</p>
    <h3>Which agent has the best QC?</h3>
    <p>Unlimited warehouse photos matter more than branding. BBDBuyEU, CNFans and LitBuy typically allow free QC on each item; some 0% agents cap free photos.</p>
    <p>Fees and storage change. Verify on the agent's own site before you pay. This comparison is independent and not sponsored.</p>
  </div>
</section>
"""
    faq = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {
                "@type": "Question",
                "name": "Which Chinese shopping agent is cheapest in 2026?",
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": "The cheapest checkout is the lowest landed cost after shipping, not the lowest advertised fee. Weigh a 2–5 kg haul on two agents before you standardise.",
                },
            },
            {
                "@type": "Question",
                "name": "Is BBDBuy the same as BBDBuyEU?",
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": "W2C lists the sheet as bbdbuy; checkout is on bbdbuyeu.com (BBDBuyEU). Same catalog, not a rebrand of the agent.",
                },
            },
        ],
    }
    extra = f'<script type="application/ld+json">{json.dumps(faq, ensure_ascii=False, separators=(",", ":"))}</script>'
    return _shell(
        "Shopping Agent Comparison 2026: BBDBuy vs Kakobuy vs CNFans vs Superbuy",
        "Compare BBDBuyEU with Kakobuy, CNFans, Superbuy, LitBuy and Pandabuy — fees, QC photos, storage and shipping for spreadsheet users.",
        f"{BASE}/compare-shopping-agents/",
        body,
        extra_head=extra,
    )


JSONLD_RE = re.compile(
    r'<script[^>]*type=["\']application/ld\+json["\'][^>]*>.*?</script>',
    re.I | re.S,
)


def patch_homepage(html: str) -> str:
    if JSONLD_RE.search(html):
        html = JSONLD_RE.sub(jsonld_script(), html, count=1)
    else:
        html = html.replace("</head>", jsonld_script() + "\n</head>", 1)

    plus = count_plus()
    html = html.replace(
        'content="Independent BBDBuyEU spreadsheet: QC finds, invite 1QodRw, Europe shipping and VAT tips. Browse lists on W2C Links."',
        f'content="The free BBDBuyEU spreadsheet (also searched as bbd buy eu spreadsheet, bbd buy spreadsheet or bbdbuy spreadsheet) — {plus} Taobao, 1688 and Weidian links, invite 1QodRw and coupon BBD5OFF."',
    )
    if 'name="keywords"' not in html:
        html = html.replace(
            '<link rel="canonical" href="https://bbdbuyeu.net/">',
            '<meta name="keywords" content="bbd buy eu spreadsheet, bbd buy spreadsheet, bbdbuy spreadsheet, bbdbuyeu spreadsheet, bbd buy eu sheet, BBD Buy EU Spreadsheet">\n<link rel="canonical" href="https://bbdbuyeu.net/">',
            1,
        )

    misspell = (
        '<p class="hsub">Also searched as <strong>bbd buy eu spreadsheet</strong>, '
        "<strong>bbd buy spreadsheet</strong>, <strong>bbdbuy spreadsheet</strong> "
        "or <strong>bbd buy eu sheet</strong> — same BBDBuyEU catalog. Invite <strong>1QodRw</strong>.</p>"
    )
    if "Also searched as" not in html:
        html = html.replace(
            '<p class="hsub">Browse 3,015+ products with direct BBDBuyEU links, free shipping calculator, coupon codes and full buying guides &mdash; all in one place.</p>',
            '<p class="hsub">Browse 3,015+ products with direct BBDBuyEU links, free shipping calculator, coupon codes and full buying guides &mdash; all in one place.</p>\n  '
            + misspell,
            1,
        )

    about_extra = (
        "<p>People also search <strong>bbd buy eu spreadsheet</strong>, "
        "<strong>bbdbuy spreadsheet</strong> and <strong>bbd buy spreadsheet</strong>. "
        "Those queries point here. Checkout is on "
        '<a href="https://www.bbdbuyeu.com/register?inviteCode=1QodRw" rel="nofollow">bbdbuyeu.com</a> '
        "with invite 1QodRw.</p>"
    )
    if "People also search" not in html:
        html = html.replace(
            '<p>This site focuses on EU/UK-friendly shipping notes, QC workflows and spreadsheet finds. Start with the spreadsheet, then QC, then shipping estimates in euros.</p>',
            '<p>This site focuses on EU/UK-friendly shipping notes, QC workflows and spreadsheet finds. Start with the spreadsheet, then QC, then shipping estimates in euros.</p>'
            + about_extra,
            1,
        )

    faq_html = '<section class="sec" id="faq"><h2 class="stit">BBDBuyEU spreadsheet FAQ</h2>'
    for item in FAQ_EXTRA:
        faq_html += (
            '<div class="faq-item"><div class="faq-q" onclick="toggleFaq(this)">'
            f'{escape(item["name"])}</div><div class="faq-a">{escape(item["text"])}</div></div>'
        )
    faq_html += "</section>"
    if 'id="faq"' not in html:
        html = html.replace('<footer class="ft">', faq_html + '\n<footer class="ft">', 1)

    if "/customs-calculator/" not in html:
        html = html.replace(
            '<ul class="nl"><li><a href="https://w2clinks.com/spreadsheet/bbdbuy/" target="_blank" rel="noopener">Spreadsheet</a></li>',
            '<ul class="nl"><li><a href="/bbdbuyeu-spreadsheet/">Spreadsheet</a></li><li><a href="/tools/">Tools</a></li><li><a href="/product/">Products</a></li>',
            1,
        )
        html = html.replace(
            '<li><a href="/bbdbuyeu-shipping-guide/">Shipping Guide</a></li>',
            '<li><a href="/bbdbuyeu-shipping-guide/">Shipping Guide</a></li>\n      '
            '<li><a href="/customs-calculator/">Duty calculator</a></li>'
            '<li><a href="/sizing-guide/">Size chart</a></li>'
            '<li><a href="/compare-shopping-agents/">Agent comparison</a></li>'
            '<li><a href="/tools/">Buyer tools</a></li>'
            '<li><a href="/product/">Product finds</a></li>',
            1,
        )
    if 'gtit">Duty calculator' not in html and "Guides &amp; Tools" in html:
        html = html.replace(
            '<a href="/blog/" class="gc">',
            '<a href="/tools/" class="gc"><span class="gtg" style="background:var(--acl);color:var(--acd)">Tools</span><p class="gtit">Buyer tools</p><p class="gdesc">Duty calculator, Chinese size chart and shopping-agent comparison.</p><span class="glink">Open tools &rarr;</span></a>\n    '
            '<a href="/blog/" class="gc">',
            1,
        )
    return apply_count_copy(html)


def apply_count_copy(html: str, exact: bool = False) -> str:
    """Replace stale 3,015+ marketing copy with the live catalog size."""
    found = catalog_stats()["found"]
    plus = count_plus(found)
    label = plus if not exact else count_exact(found)
    for stale in ("3,015+", "8,600+", "3,015"):
        html = html.replace(stale, label)
    return html


COUNT_SYNC_JS = r"""
function fmtN(n){return Number(n||0).toLocaleString('en-US');}
async function syncSidebarCounts(){
  const map = (typeof W2C_CAT!=='undefined') ? W2C_CAT : {};
  try{
    const r=await fetch(API+'?page=1&per_page=1&sort=newest',{cache:'no-store'});
    const d=await r.json();
    const n=Number(d.found||d.total||d.totalProducts||0);
    if(n){
      const allCn=document.querySelector('#clist a[onclick*="fc(\'all\')"] .cn');
      if(allCn) allCn.textContent=fmtN(n);
      document.querySelectorAll('.hsn').forEach(el=>{if(/^[0-9]/.test(el.textContent.trim())) el.textContent=fmtN(n)+'+';});
    }
  }catch(e){}
  await Promise.all(Object.entries(map).map(async ([key, apiCat])=>{
    try{
      const r=await fetch(API+'?page=1&per_page=1&category='+encodeURIComponent(apiCat),{cache:'no-store'});
      const d=await r.json();
      const n=Number(d.found||d.total||0);
      const el=document.querySelector('#clist a[onclick*="fc(\''+key+'\')"] .cn');
      if(el&&n) el.textContent=fmtN(n);
    }catch(e){}
  }));
}
"""


def patch_directory_page(html: str, stats: dict | None = None) -> str:
    stats = stats or catalog_stats()
    found = int(stats["found"])
    exact = f"{found:,}"
    plus = count_plus(found)
    if JSONLD_RE.search(html):
        html = JSONLD_RE.sub(jsonld_script(), html, count=1)
    else:
        html = html.replace("</head>", jsonld_script() + "\n</head>", 1)
    misspell = (
        '<p class="hsub">Also searched as <strong>bbd buy eu spreadsheet</strong>, '
        "<strong>bbd buy spreadsheet</strong> or <strong>bbdbuy spreadsheet</strong> — "
        "same catalog as this BBDBuyEU sheet.</p>"
    )
    if "Also searched as" not in html:
        html = html.replace(
            '<p class="hsub">Browse 3,015+ products — live data from',
            misspell + '\n  <p class="hsub">Browse 3,015+ products — live data from',
            1,
        )
        if "Also searched as" not in html:
            html = html.replace(
                "The 2026 edition of the BBDBuyEU spreadsheet. 3,015+ products, updated daily.",
                "The 2026 edition of the BBDBuyEU spreadsheet (also searched as bbd buy eu spreadsheet). 3,015+ products, updated daily.",
                1,
            )
    html = html.replace("Browse 3,015+ products", f"Browse {exact} products")
    html = html.replace("Browse 8,600+ products", f"Browse {exact} products")
    html = html.replace("Search 8,600+ rep products", f"Search {exact} rep products")
    html = html.replace(
        'All Products <span class="cn">3,015+</span>',
        f'All Products <span class="cn">{exact}</span>',
    )
    html = html.replace(
        'All Products <span class="cn">8,600+</span>',
        f'All Products <span class="cn">{exact}</span>',
    )
    html = html.replace("3,015+ products on W2C", f"{plus} products on W2C")
    html = html.replace("3,015+", plus)
    html = html.replace("8,600+", plus)
    html = html.replace("<b>8,649</b> products", f"<b>{exact}</b> products")
    html = html.replace("8,600+ live BBDBuyEU", f"{exact} live BBDBuyEU")
    html = html.replace("8,600+ rep products", f"{exact} rep products")
    html = html.replace("Free BBDBuyEU spreadsheet with 8,600+", f"Free BBDBuyEU spreadsheet with {exact}")
    for key, n in (stats.get("categories") or {}).items():
        html = re.sub(
            rf"(onclick=\"fc\('{re.escape(key)}'\);return false;\">[^<]+ <span class=\"cn\">)[^<]+",
            rf"\g<1>{int(n):,}",
            html,
        )
    marker = "document.addEventListener('DOMContentLoaded',lp);"
    if marker in html and "syncSidebarCounts" not in html:
        html = html.replace(
            marker,
            COUNT_SYNC_JS + "document.addEventListener('DOMContentLoaded',()=>{lp();syncSidebarCounts();});",
            1,
        )
    alt = "document.addEventListener('DOMContentLoaded',()=>lp(true));"
    if alt in html and "syncSidebarCounts" not in html:
        html = html.replace(
            alt,
            COUNT_SYNC_JS + "document.addEventListener('DOMContentLoaded',()=>{lp(true);syncSidebarCounts();});",
            1,
        )
    return html


def fetch_path(path: str) -> str:
    req = Request(f"{BASE}{path}", headers={"User-Agent": "BBDBuyEUSEO/1.0"})
    with urlopen(req, timeout=30) as resp:
        return resp.read().decode("utf-8", "replace")


def validate_jsonld(html: str) -> list[str]:
    types: list[str] = []
    for raw in re.findall(
        r'<script[^>]*type=["\']application/ld\+json["\'][^>]*>(.*?)</script>',
        html,
        re.I | re.S,
    ):
        obj = json.loads(raw.strip())
        if isinstance(obj, dict) and "@graph" in obj:
            types.extend(str(node.get("@type")) for node in obj["@graph"])
        elif isinstance(obj, dict):
            types.append(str(obj.get("@type")))
    return types


def fetch_homepage() -> str:
    req = Request(f"{BASE}/", headers={"User-Agent": "BBDBuyEUSEO/1.0"})
    with urlopen(req, timeout=30) as resp:
        return resp.read().decode("utf-8", "replace")


def _products_mod():
    try:
        import bbdbuyeu_products
        return bbdbuyeu_products
    except ImportError:
        import importlib.util

        spec = importlib.util.spec_from_file_location(
            "bbdbuyeu_products", Path(__file__).with_name("bbdbuyeu_products.py")
        )
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        return mod


def write_overlay(index_html: str, products: bool = True, product_limit: int = 0) -> None:
    OVERLAY.mkdir(parents=True, exist_ok=True)
    (OVERLAY / "robots.txt").write_text(ROBOTS_TXT, encoding="utf-8")
    (OVERLAY / "llms.txt").write_text(apply_count_copy(LLMS_TXT), encoding="utf-8")
    (OVERLAY / "index.html").write_text(patch_homepage(index_html), encoding="utf-8")
    pages = {
        "tools": tools_page(),
        "customs-calculator": customs_page(),
        "sizing-guide": sizing_page(),
        "compare-shopping-agents": compare_page(),
    }
    for slug, html in pages.items():
        dest = OVERLAY / slug
        dest.mkdir(exist_ok=True)
        (dest / "index.html").write_text(html, encoding="utf-8")
    php_src = OVERLAY / "api" / "products.php"
    if php_src.exists():
        api_dir = OVERLAY / "api" / "products"
        api_dir.mkdir(parents=True, exist_ok=True)
        (api_dir / "index.php").write_text(php_src.read_text(encoding="utf-8"), encoding="utf-8")
    stats = catalog_stats()
    for slug in ("bbdbuyeu-spreadsheet", "bbdbuyeu-spreadsheet-2026"):
        try:
            raw = fetch_path(f"/{slug}/")
        except Exception as exc:
            print("skip directory", slug, exc)
            continue
        dest = OVERLAY / slug
        dest.mkdir(exist_ok=True)
        (dest / "index.html").write_text(patch_directory_page(raw, stats), encoding="utf-8")
        print(f"directory {slug} found={stats['found']}")
    sitemap_extra = """  <url><loc>https://bbdbuyeu.net/tools/</loc><lastmod>{today}</lastmod><changefreq>monthly</changefreq><priority>0.8</priority></url>
  <url><loc>https://bbdbuyeu.net/customs-calculator/</loc><lastmod>{today}</lastmod><changefreq>monthly</changefreq><priority>0.85</priority></url>
  <url><loc>https://bbdbuyeu.net/sizing-guide/</loc><lastmod>{today}</lastmod><changefreq>monthly</changefreq><priority>0.85</priority></url>
  <url><loc>https://bbdbuyeu.net/compare-shopping-agents/</loc><lastmod>{today}</lastmod><changefreq>monthly</changefreq><priority>0.85</priority></url>
  <url><loc>https://bbdbuyeu.net/product/</loc><lastmod>{today}</lastmod><changefreq>daily</changefreq><priority>0.7</priority></url>
""".format(today=TODAY)
    (OVERLAY / "sitemap-extra.xml").write_text(sitemap_extra, encoding="utf-8")
    if products:
        items = _products_mod().build_product_pages(limit=product_limit)
        print(f"product pages {len(items)}")


def merge_sitemap(existing: str) -> str:
    extra_locs = [
        f"{BASE}/tools/",
        f"{BASE}/customs-calculator/",
        f"{BASE}/sizing-guide/",
        f"{BASE}/compare-shopping-agents/",
        f"{BASE}/product/",
    ]
    out = existing
    for loc in extra_locs:
        if loc not in out:
            out = out.replace(
                "</urlset>",
                f"  <url><loc>{loc}</loc><lastmod>{TODAY}</lastmod><changefreq>monthly</changefreq><priority>0.85</priority></url>\n</urlset>",
                1,
            )
    return out


def self_test() -> None:
    global _STATS
    _STATS = {"found": 10024, "categories": {"shoes": 1478}}
    fixture = """<!DOCTYPE html><html><head>
<title>BBDBuyEU Spreadsheet 2026</title>
<meta name="description" content="Independent BBDBuyEU spreadsheet: QC finds, invite 1QodRw, Europe shipping and VAT tips. Browse lists on W2C Links.">
<link rel="canonical" href="https://bbdbuyeu.net/">
</head><body>
<ul class="nl"><li><a href="https://w2clinks.com/spreadsheet/bbdbuy/" target="_blank" rel="noopener">Spreadsheet</a></li><li><a href="/is-bbdbuyeu-legit/">Is it Legit?</a></li>
<p class="hsub">Browse 3,015+ products with direct BBDBuyEU links, free shipping calculator, coupon codes and full buying guides &mdash; all in one place.</p>
<section class="eu-gsc-extra"><h2>BBDBuy EU spreadsheet hub</h2><p>This site focuses on EU/UK-friendly shipping notes, QC workflows and spreadsheet finds. Start with the spreadsheet, then QC, then shipping estimates in euros.</p></section>
<h2 class="stit">Guides &amp; Tools</h2>
<a href="/blog/" class="gc">
<li><a href="/bbdbuyeu-shipping-guide/">Shipping Guide</a></li>
<footer class="ft"></footer>
</body></html>"""
    patched = patch_homepage(fixture)
    types = validate_jsonld(patched)
    assert "WebSite" in types and "FAQPage" in types and "SoftwareApplication" in types, types
    graph = json.loads(JSONLD_RE.search(patched).group(0).split(">", 1)[1].rsplit("</", 1)[0])
    website = next(n for n in graph["@graph"] if n["@type"] == "WebSite")
    for name in (
        "BBD Buy EU Spreadsheet",
        "BBD Buy Spreadsheet",
        "bbd buy eu spreadsheet",
        "bbd buy spreadsheet",
        "bbdbuy spreadsheet",
    ):
        assert name in website["alternateName"], name
    assert "bbd buy eu spreadsheet" in patched.lower()
    assert "Also searched as" in patched
    assert "bbd buy eu sheet" in patched.lower()
    assert "/customs-calculator/" in patched
    assert "/compare-shopping-agents/" in patched
    assert "3,015+" not in patched
    for page in (tools_page(), customs_page(), sizing_page(), compare_page()):
        assert "<h1>" in page and "BBDBuyEU" in page
    compare_html = compare_page()
    assert "Kakobuy" in compare_html and "application/ld+json" in compare_html
    assert "not an AllChinaBuy/ACBuy-style rebrand" in compare_html
    _products_mod().self_test()
    directory = (
        "<html><head></head><body>"
        '<p class="hsub">Browse 3,015+ products — live data from <a href="https://w2clinks.com/spreadsheet/bbdbuy/">W2C</a>.</p>'
        '<ul class="cl" id="clist"><li><a href="#" class="on" onclick="fc(\'all\');return false;">All Products <span class="cn">3,015+</span></a></li>'
        '<li><a href="#" onclick="fc(\'shoes\');return false;">Sneakers <span class="cn">240+</span></a></li></ul>'
        '<span class="ss-count" id="rc"><b>3,015</b> products</span>'
        "const W2C_CAT={\"shoes\":\"SNEAKERS\"};const API='/api/products/';"
        "document.addEventListener('DOMContentLoaded',lp);"
        "</body></html>"
    )
    synced = patch_directory_page(directory, {"found": 10024, "categories": {"shoes": 1478}})
    assert "Browse 10,024 products" in synced
    assert 'All Products <span class="cn">10,024</span>' in synced
    assert "1,478" in synced
    assert "syncSidebarCounts" in synced
    assert "bbd buy eu spreadsheet" in synced.lower()
    assert "3,015+" not in synced
    print("self-test OK", types)


def _connect():
    try:
        import paramiko
    except ImportError:
        import subprocess

        subprocess.check_call([sys.executable, "-m", "pip", "install", "paramiko", "-q"])
        import paramiko

    password = (
        os.environ.get("BBDBUYEU_DEPLOY_PASS")
        or os.environ.get("ORIENTDIG_DEPLOY_PASS")
        or os.environ.get("KAKOBUY_DEPLOY_PASS")
        or os.environ.get("LITBUY_DEPLOY_PASS")
    )
    if not password:
        print("Set BBDBUYEU_DEPLOY_PASS (or ORIENTDIG_DEPLOY_PASS)", file=sys.stderr)
        sys.exit(1)
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(HOST, username=USER, password=password, timeout=30)
    return client


def _run(client, cmd: str, timeout: int = 60) -> str:
    _, stdout, stderr = client.exec_command(cmd, timeout=timeout)
    return (stdout.read() + stderr.read()).decode(errors="replace").strip()


def deploy(skip_products: bool = False, product_limit: int = 0) -> None:
    html = fetch_homepage()
    write_overlay(html, products=not skip_products, product_limit=product_limit)
    patched = (OVERLAY / "index.html").read_text(encoding="utf-8")
    types = validate_jsonld(patched)
    print("json-ld", types)

    client = _connect()
    sftp = client.open_sftp()
    stamp = _run(client, "date -u +%Y%m%d_%H%M%S")
    _run(client, f"cp -a {WEBROOT}/index.html {WEBROOT}/index.html.bak-seo-{stamp}")
    _run(client, f"cp -a {WEBROOT}/robots.txt {WEBROOT}/robots.txt.bak-seo-{stamp} || true")
    _run(client, f"cp -a {WEBROOT}/llms.txt {WEBROOT}/llms.txt.bak-seo-{stamp} || true")
    _run(client, f"cp -a {WEBROOT}/sitemap.xml {WEBROOT}/sitemap.xml.bak-seo-{stamp} || true")
    _run(client, f"cp -a {WEBROOT}/bbdbuyeu-spreadsheet/index.html {WEBROOT}/bbdbuyeu-spreadsheet/index.html.bak-seo-{stamp} || true")
    _run(client, f"cp -a {WEBROOT}/bbdbuyeu-spreadsheet-2026/index.html {WEBROOT}/bbdbuyeu-spreadsheet-2026/index.html.bak-seo-{stamp} || true")

    uploads = {
        str(OVERLAY / "index.html"): f"{WEBROOT}/index.html",
        str(OVERLAY / "robots.txt"): f"{WEBROOT}/robots.txt",
        str(OVERLAY / "llms.txt"): f"{WEBROOT}/llms.txt",
        str(OVERLAY / "tools" / "index.html"): f"{WEBROOT}/tools/index.html",
        str(OVERLAY / "customs-calculator" / "index.html"): f"{WEBROOT}/customs-calculator/index.html",
        str(OVERLAY / "sizing-guide" / "index.html"): f"{WEBROOT}/sizing-guide/index.html",
        str(OVERLAY / "compare-shopping-agents" / "index.html"): f"{WEBROOT}/compare-shopping-agents/index.html",
        str(OVERLAY / "sitemap-products.xml"): f"{WEBROOT}/sitemap-products.xml",
        str(OVERLAY / "api" / "products.php"): f"{WEBROOT}/api/products.php",
        str(OVERLAY / "api" / "products" / "index.php"): f"{WEBROOT}/api/products/index.php",
        str(OVERLAY / "bbdbuyeu-spreadsheet" / "index.html"): f"{WEBROOT}/bbdbuyeu-spreadsheet/index.html",
        str(OVERLAY / "bbdbuyeu-spreadsheet-2026" / "index.html"): f"{WEBROOT}/bbdbuyeu-spreadsheet-2026/index.html",
    }
    for local, remote in uploads.items():
        if not Path(local).exists():
            print("skip missing", local)
            continue
        parent = remote.rsplit("/", 1)[0]
        _run(client, f"mkdir -p {parent}")
        sftp.put(local, remote)
        print("uploaded", remote)

    product_dir = OVERLAY / "product"
    if product_dir.exists():
        import tarfile
        import tempfile

        tar_path = Path(tempfile.gettempdir()) / "bbdbuyeu-product-pages.tar.gz"
        with tarfile.open(tar_path, "w:gz") as tar:
            tar.add(product_dir, arcname="product")
        remote_tar = "/tmp/bbdbuyeu-product-pages.tar.gz"
        sftp.put(str(tar_path), remote_tar)
        _run(
            client,
            f"rm -rf {WEBROOT}/product && tar -xzf {remote_tar} -C {WEBROOT} && rm -f {remote_tar}",
            timeout=180,
        )
        print("uploaded product pages")

    with sftp.open(f"{WEBROOT}/sitemap.xml", "r") as fh:
        existing = fh.read().decode("utf-8")
    merged = merge_sitemap(existing)
    tmp = f"{WEBROOT}/sitemap.xml.new"
    with sftp.open(tmp, "w") as fh:
        fh.write(merged)
    _run(
        client,
        " && ".join(
            [
                f"mv {tmp} {WEBROOT}/sitemap.xml",
                (
                    f"chown -R www:www {WEBROOT}/index.html {WEBROOT}/robots.txt "
                    f"{WEBROOT}/llms.txt {WEBROOT}/sitemap.xml {WEBROOT}/sitemap-products.xml "
                    f"{WEBROOT}/tools {WEBROOT}/customs-calculator {WEBROOT}/sizing-guide "
                    f"{WEBROOT}/compare-shopping-agents {WEBROOT}/product {WEBROOT}/api/products.php "
                    f"{WEBROOT}/api/products {WEBROOT}/bbdbuyeu-spreadsheet {WEBROOT}/bbdbuyeu-spreadsheet-2026"
                ),
            ]
        ),
    )
    sftp.close()
    plus = count_plus()
    exact = count_exact()
    stale = _run(
        client,
        "python3 - <<'PY'\n"
        "import os\n"
        f"old_plus={json.dumps('3,015+')}\n"
        f"new_plus={json.dumps(plus)}\n"
        f"old_n={json.dumps('3,015')}\n"
        f"new_n={json.dumps(exact)}\n"
        "root='/www/wwwroot/bbdbuyeu.net'\n"
        "changed=0\n"
        "for dirpath, dirs, files in os.walk(root):\n"
        "    rel=os.path.relpath(dirpath, root)\n"
        "    if rel=='product' or rel.startswith('product'+os.sep):\n"
        "        dirs[:]=[]\n"
        "        continue\n"
        "    for name in files:\n"
        "        if not name.endswith(('.html','.txt')): continue\n"
        "        path=os.path.join(dirpath, name)\n"
        "        try:\n"
        "            text=open(path, encoding='utf-8').read()\n"
        "        except Exception:\n"
        "            continue\n"
        "        n=text.replace(old_plus, new_plus).replace(old_n, new_n)\n"
        "        if n!=text:\n"
        "            open(path,'w',encoding='utf-8').write(n)\n"
        "            changed+=1\n"
        "print('stale-count-files', changed)\n"
        "PY",
        timeout=120,
    )
    print(stale)
    client.close()
    print("bbdbuyeu.net seo deploy done")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--build", action="store_true")
    parser.add_argument("--file", type=Path)
    parser.add_argument("--deploy", action="store_true")
    parser.add_argument("--skip-products", action="store_true")
    parser.add_argument("--product-limit", type=int, default=0, help="0 = entire catalog")
    args = parser.parse_args()
    if args.self_test:
        self_test()
        return
    if args.deploy:
        deploy(skip_products=args.skip_products, product_limit=args.product_limit)
        return
    source = args.file.read_text(encoding="utf-8") if args.file else fetch_homepage()
    write_overlay(source, products=not args.skip_products, product_limit=args.product_limit)
    types = validate_jsonld((OVERLAY / "index.html").read_text(encoding="utf-8"))
    print(f"wrote {OVERLAY} json-ld={types}")


if __name__ == "__main__":
    main()
