#!/usr/bin/env python3
"""Apply lit-buy-spreadsheet.com-style SEO to allchina-buy.com.

The competitor ranks on spaced/misspelled queries plus AI crawlers. This
script mirrors that playbook for AllChinaBuy / ACBuy:

  - WebSite.alternateName for all china buy / ac buy / acbuy
  - FAQ + visible copy that maps those spellings to this hub
  - SoftwareApplication / ItemList / Breadcrumb schema
  - llms.txt + AI-bot robots.txt
  - Dedicated /customs-calculator/ and /sizing-guide/ landings

Usage:
  python3 scripts/optimize_allchina_buy.py --self-test
  python3 scripts/optimize_allchina_buy.py --build
  ALLCHINA_DEPLOY_PASS='...' python3 scripts/optimize_allchina_buy.py --deploy
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
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
OVERLAY = ROOT / "sites" / "allchina-buy.com" / "overlay"
DOMAIN = "allchina-buy.com"
BASE = f"https://{DOMAIN}"
TODAY = date.today().isoformat()
HOST = os.environ.get(
    "ALLCHINA_DEPLOY_HOST",
    os.environ.get("ORIENTDIG_DEPLOY_HOST", "31.97.41.31"),
)
USER = os.environ.get(
    "ALLCHINA_DEPLOY_USER",
    os.environ.get("ORIENTDIG_DEPLOY_USER", "root"),
)
WEBROOT = f"/www/wwwroot/{DOMAIN}"

ALTERNATE_NAMES = [
    "AllChinaBuy Sheet",
    "AllChinaBuy Spreadsheets",
    "ACBuy Spreadsheet",
    "AC Buy Spreadsheet",
    "All China Buy Spreadsheet",
    "Allchinabuy Spreadsheet",
    "Best AllChinaBuy Spreadsheet 2026",
    "ACBuy Sheet",
]

CATEGORIES = [
    ("Sneakers", "/allchinabuy-spreadsheet-shoes/", "3,800+"),
    ("Slippers", "/allchinabuy-spreadsheet-other-goods/", "420+"),
    ("T-Shirts", "/allchinabuy-spreadsheet-t-shirts/", "2,100+"),
    ("Polo", "/allchinabuy-spreadsheet-womens-fashion/", "890+"),
    ("Shorts", "/allchinabuy-spreadsheet-pants/", "980+"),
    ("Hoodies", "/allchinabuy-spreadsheet-hoodies/", "760+"),
    ("Jackets", "/allchinabuy-spreadsheet-jackets/", "1,200+"),
    ("Trousers", "/allchinabuy-spreadsheet-headwear/", "650+"),
    ("Jerseys", "/allchinabuy-spreadsheet-jerseys/", "290+"),
    ("Electronics", "/allchinabuy-spreadsheet-electronics/", "150+"),
    ("Bags", "/allchinabuy-spreadsheet-bags/", "540+"),
    ("Jewelry", "/allchinabuy-spreadsheet-accessories/", "480+"),
]

FAQ_EXTRA = [
    {
        "name": "Is this the same as \"all china buy spreadsheet\" or \"ac buy spreadsheet\"?",
        "text": (
            "Yes — \"all china buy\", \"ac buy\", \"acbuy\" and \"allchinabuy\" are "
            "common spellings for the same shopping agent. This is the same "
            "AllChinaBuy spreadsheet regardless of how it is spelled. ACBuy is "
            "the current brand name; AllChinaBuy is the older name."
        ),
    },
    {
        "name": "Is ACBuy the same as AllChinaBuy?",
        "text": (
            "Yes. ACBuy rebranded from AllChinaBuy. The spreadsheet, QC photos "
            "and live product links on this site work for both names. Browse "
            "the ACBuy spreadsheet or the AllChinaBuy spreadsheet — they are "
            "the same catalog."
        ),
    },
]


def _jsonld_graph() -> dict:
    faq_entities = [
        {
            "@type": "Question",
            "name": "What is the AllChinaBuy Spreadsheet?",
            "acceptedAnswer": {
                "@type": "Answer",
                "text": "A curated database of 8,600+ products from Taobao, Weidian and 1688 with live product links, USD pricing and QC photos.",
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
            "name": "Is the AllChinaBuy Spreadsheet free?",
            "acceptedAnswer": {
                "@type": "Answer",
                "text": "Yes — browsing is completely free. No signup required until you place an order on AllChinaBuy / ACBuy.",
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
            "name": "Is AllChinaBuy safe to use?",
            "acceptedAnswer": {
                "@type": "Answer",
                "text": "AllChinaBuy / ACBuy uses escrow payments and warehouse QC photos. See the Is AllChinaBuy Legit? guide on this site.",
            },
        },
        {
            "@type": "Question",
            "name": "Does AllChinaBuy have coupon codes?",
            "acceptedAnswer": {
                "@type": "Answer",
                "text": "Yes — use ACBUY5 for 5% off. See the coupons page.",
            },
        },
    ]
    return {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "WebSite",
                "@id": f"{BASE}/#website",
                "name": "AllChinaBuy Spreadsheet 2026",
                "alternateName": ALTERNATE_NAMES,
                "description": "The #1 free AllChinaBuy / ACBuy spreadsheet with 8,600+ verified products from Taobao, 1688 and Weidian.",
                "url": f"{BASE}/",
                "inLanguage": "en",
                "dateModified": TODAY,
                "potentialAction": {
                    "@type": "SearchAction",
                    "target": f"{BASE}/allchinabuy-spreadsheet/?q={{search_term_string}}",
                    "query-input": "required name=search_term_string",
                },
            },
            {
                "@type": "Organization",
                "@id": f"{BASE}/#org",
                "name": "AllChinaBuy Spreadsheet",
                "legalName": "AllChinaBuy Spreadsheet (Independent)",
                "url": f"{BASE}/",
                "logo": f"{BASE}/allchinabuy-LOGO.png",
                "description": "Independent AllChinaBuy / ACBuy spreadsheet hub. Not affiliated with allchinabuy.com.",
            },
            {
                "@type": "SoftwareApplication",
                "name": "AllChinaBuy Spreadsheet",
                "applicationCategory": "ShoppingApplication",
                "operatingSystem": "Web",
                "url": f"{BASE}/allchinabuy-spreadsheet/",
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
                "name": "AllChinaBuy Spreadsheet 2026",
                "url": f"{BASE}/",
                "about": "AllChinaBuy spreadsheet and ACBuy spreadsheet product catalog",
            },
            {
                "@type": "ItemList",
                "name": "AllChinaBuy Spreadsheet Categories",
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
                        "name": "AllChinaBuy Spreadsheet",
                        "item": f"{BASE}/allchinabuy-spreadsheet/",
                    },
                ],
            },
            {
                "@type": "Service",
                "name": "AllChinaBuy Spreadsheet Guide",
                "serviceType": "Product discovery spreadsheet",
                "provider": {"@id": f"{BASE}/#org"},
                "areaServed": ["US", "UK", "CA", "AU", "EU"],
                "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"},
            },
            {"@type": "FAQPage", "mainEntity": faq_entities},
            {
                "@type": "HowTo",
                "name": "How to Use the AllChinaBuy Spreadsheet",
                "step": [
                    {
                        "@type": "HowToStep",
                        "position": 1,
                        "name": "Browse or search",
                        "text": "Open the AllChinaBuy spreadsheet and filter by category or brand.",
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
                        "name": "Paste into ACBuy / AllChinaBuy",
                        "text": "Register on AllChinaBuy (now ACBuy) and paste the link.",
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


ROBOTS_TXT = """User-Agent: *
Allow: /
Disallow: /api/
Disallow: /.bak
Disallow: /admin/

User-Agent: Googlebot
Allow: /
Allow: /allchinabuy-spreadsheet
Allow: /acbuy-spreadsheet
Allow: /blog/
Allow: /product/
Disallow: /api/

User-Agent: Bingbot
Allow: /
Disallow: /api/
Disallow: /admin/

User-Agent: GPTBot
Allow: /
Allow: /allchinabuy-spreadsheet
Allow: /acbuy-spreadsheet
Allow: /blog/
Disallow: /api/
Disallow: /admin/

User-Agent: ChatGPT-User
Allow: /
Disallow: /api/
Disallow: /admin/

User-Agent: PerplexityBot
Allow: /
Allow: /blog/
Allow: /allchinabuy-spreadsheet
Disallow: /api/

User-Agent: Anthropic-AI
Allow: /
Disallow: /api/

User-Agent: Google-Extended
Allow: /

User-Agent: OAI-SearchBot
Allow: /
Disallow: /api/

User-Agent: ClaudeBot
Allow: /
Disallow: /api/

Sitemap: https://allchina-buy.com/sitemap.xml
"""

LLMS_TXT = """# AllChinaBuy Spreadsheet (ACBuy Spreadsheet)

> Independent AllChinaBuy / ACBuy spreadsheet for Chinese e-commerce. Browse 8,600+ live products from Taobao, 1688 and Weidian with QC photos, working links and USD pricing. Not a store — discovery only. Checkout happens on AllChinaBuy (now branded ACBuy).

## Also searched as

- all china buy spreadsheet
- ac buy spreadsheet
- acbuy spreadsheet
- allchinabuy spreadsheet
- all china buy sheet
- acbuy sheet

These spellings all refer to the same catalog on https://allchina-buy.com/

## Key facts

- 8,600+ live product listings refreshed from W2C
- Categories: sneakers, slippers, t-shirts, polo, shorts, hoodies, jackets, trousers, jerseys, electronics, bags, jewelry
- Platforms: Taobao, 1688, Weidian
- Free to browse — no account required
- Independent of allchinabuy.com / acbuy.com

## Key pages

- Homepage: https://allchina-buy.com/
- AllChinaBuy spreadsheet: https://allchina-buy.com/allchinabuy-spreadsheet/
- ACBuy spreadsheet: https://allchina-buy.com/acbuy-spreadsheet/
- Coupons: https://allchina-buy.com/allchinabuy-coupons/
- Is AllChinaBuy legit?: https://allchina-buy.com/is-allchinabuy-legit/
- How to use AllChinaBuy: https://allchina-buy.com/how-to-use-allchinabuy/
- Shipping guide: https://allchina-buy.com/allchinabuy-shipping-guide/
- Customs / duty calculator: https://allchina-buy.com/customs-calculator/
- Chinese size chart: https://allchina-buy.com/sizing-guide/
- ACBuy vs AllChinaBuy: https://allchina-buy.com/acbuy-vs-allchinabuy/
- Tools: https://allchina-buy.com/tools/
- Blog: https://allchina-buy.com/blog/

## Common questions

Q: Is ACBuy the same as AllChinaBuy?
A: Yes. ACBuy is the current brand; AllChinaBuy is the previous name. This spreadsheet works for both.

Q: Is the AllChinaBuy spreadsheet free?
A: Yes. You only pay when you order through the agent.

Q: Where do product links come from?
A: Live W2C catalog rows pointing at Taobao, Weidian and 1688 listings.

Q: Is this the official AllChinaBuy website?
A: No. allchina-buy.com is an independent English guide hub.
"""


def _shell(title: str, description: str, canonical: str, body: str) -> str:
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
<link rel="stylesheet" href="/assets/css/main.css?v=seo20260917">
<style>main table{{width:100%;border-collapse:collapse;margin:16px 0}}main th,main td{{border-bottom:1px solid #e5e5e5;padding:8px 10px;text-align:left}}main label{{display:flex;flex-direction:column;gap:6px;font-size:.9rem}}main select,main input[type=number]{{padding:10px;border:1px solid #ddd;border-radius:8px}}</style>
<meta property="og:title" content="{title_e}">
<meta property="og:description" content="{desc_e}">
<meta property="og:url" content="{canonical}">
<meta property="og:type" content="website">
</head>
<body>
<div class="topbar">2026 Update: Code <strong>ACBUY5</strong> — 5% off · <a href="/allchinabuy-coupons/">Get code →</a></div>
<nav class="nav" aria-label="Main navigation">
  <div class="container nav__inner">
    <a href="/" class="nav__logo">AllChinaBuy Spreadsheet</a>
    <ul class="nav__links" role="list">
      <li><a href="/">Home</a></li>
      <li><a href="/allchinabuy-spreadsheet/">Spreadsheet</a></li>
      <li><a href="/acbuy-spreadsheet/">ACBuy Spreadsheet</a></li>
      <li><a href="/tools/">Tools</a></li>
      <li><a href="/blog/">Blog</a></li>
      <li><a href="/allchinabuy-coupons/">Coupons</a></li>
    </ul>
  </div>
</nav>
<main>
{body}
</main>
<footer class="footer" role="contentinfo">
  <div class="container">
    <p>Independent AllChinaBuy / ACBuy spreadsheet resource — not affiliated with allchinabuy.com.</p>
    <p><a href="/">Home</a> · <a href="/allchinabuy-spreadsheet/">Spreadsheet</a> · <a href="/customs-calculator/">Duty calculator</a> · <a href="/sizing-guide/">Size chart</a></p>
  </div>
</footer>
</body>
</html>
"""


def tools_page() -> str:
    body = """
<section class="hero">
  <div class="container">
    <p class="hero__eyebrow">AllChinaBuy tools</p>
    <h1>Free AllChinaBuy Spreadsheet Tools</h1>
    <p class="hero__sub">Duty estimates and Chinese size conversion for AllChinaBuy / ACBuy hauls — same hub as the live spreadsheet.</p>
  </div>
</section>
<section class="section">
  <div class="container">
    <div class="feature-grid">
      <a class="feature-card" href="/customs-calculator/">
        <h2 class="feature-card__title">Import duty calculator</h2>
        <p class="feature-card__desc">Published de minimis and VAT/GST thresholds for US, UK, EU, Canada and Australia. Check official rules before you ship.</p>
      </a>
      <a class="feature-card" href="/sizing-guide/">
        <h2 class="feature-card__title">Chinese size chart</h2>
        <p class="feature-card__desc">CN to US / EU / UK clothing and shoe conversions for AllChinaBuy spreadsheet orders.</p>
      </a>
      <a class="feature-card" href="/allchinabuy-shipping-guide/">
        <h2 class="feature-card__title">Shipping guide</h2>
        <p class="feature-card__desc">Lines, times and what to expect after warehouse QC.</p>
      </a>
      <a class="feature-card" href="/acbuy-vs-allchinabuy/">
        <h2 class="feature-card__title">ACBuy vs AllChinaBuy</h2>
        <p class="feature-card__desc">Same agent, new name — how the spreadsheet still applies.</p>
      </a>
    </div>
  </div>
</section>
"""
    return _shell(
        "AllChinaBuy Spreadsheet Tools — Duty Calculator & Size Chart",
        "Free AllChinaBuy / ACBuy tools: import duty calculator and Chinese size conversion for spreadsheet hauls.",
        f"{BASE}/tools/",
        body,
    )


def customs_page() -> str:
    body = """
<section class="hero">
  <div class="container">
    <p class="hero__eyebrow">AllChinaBuy customs</p>
    <h1>AllChinaBuy Import Duty Calculator</h1>
    <p class="hero__sub">Estimate VAT/GST and customs duty using published destination thresholds. This is an educational calculator, not legal advice — confirm current rules with your customs authority before shipping an AllChinaBuy / ACBuy parcel.</p>
  </div>
</section>
<section class="section">
  <div class="container" style="max-width:820px">
    <form id="duty-form" class="hero__search" style="display:grid;gap:12px;grid-template-columns:1fr 1fr;max-width:640px">
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
        </select>
      </label>
      <button type="submit" class="btn btn-primary" style="grid-column:1/-1">Estimate</button>
    </form>
    <p id="duty-out" class="section-sub" style="margin-top:20px"></p>
    <h2>How this AllChinaBuy calculator works</h2>
    <p>Shoppers searching <strong>all china buy customs</strong>, <strong>acbuy duty</strong> or <strong>allchinabuy import tax</strong> land here. Thresholds below are public de minimis / VAT starting points and change over time:</p>
    <ul>
      <li><strong>United States</strong> — de minimis treatment has been changing; treat sub-$800 figures as historical and verify CBP before you ship.</li>
      <li><strong>United Kingdom</strong> — VAT typically applies on imported goods; customs duty often starts above £135.</li>
      <li><strong>EU</strong> — VAT is usually due; customs duty commonly starts above €150.</li>
      <li><strong>Canada</strong> — general goods de minimis is low (often CAD $20); GST/HST may still apply.</li>
      <li><strong>Australia</strong> — GST often applies above AUD $1,000.</li>
    </ul>
    <p>Declare the accurate transaction value. Undervaluing a parcel to avoid tax is illegal. For country write-ups see the <a href="/blog/posts/allchinabuy-customs-guide/">AllChinaBuy customs guide</a> and <a href="/allchinabuy-shipping-guide/">shipping guide</a>.</p>
    <p><a class="btn btn-primary" href="/allchinabuy-spreadsheet/">Back to the spreadsheet</a></p>
  </div>
</section>
<script>
const RULES = {
  US: {vat: 0, duty: 0, note: "US import rules are in flux. Confirm current CBP de minimis before shipping."},
  UK: {vat: 0.20, duty: 0, note: "UK VAT is commonly 20%. Customs duty depends on HS code above the duty-free threshold."},
  EU: {vat: 0.19, duty: 0, note: "Illustrative 19% VAT. Actual VAT is the destination country rate; duty depends on HS code."},
  CA: {vat: 0.05, duty: 0, note: "Illustrative 5% GST. Provincial HST/PST may add more; de minimis is low for most goods."},
  AU: {vat: 0.10, duty: 0, note: "Illustrative 10% GST. Low-value import rules still apply below AUD $1,000."}
};
document.getElementById("duty-form").addEventListener("submit", function (e) {
  e.preventDefault();
  const value = Number(document.getElementById("declared").value || 0);
  const dest = document.getElementById("dest").value;
  const rule = RULES[dest];
  const vat = value * rule.vat;
  const total = value + vat + value * rule.duty;
  document.getElementById("duty-out").textContent =
    "Estimated landed cost about USD " + total.toFixed(2) +
    " (goods USD " + value.toFixed(2) + " + tax USD " + vat.toFixed(2) + "). " + rule.note;
});
</script>
"""
    return _shell(
        "AllChinaBuy Import Duty Calculator 2026 — US, UK, EU, CA, AU",
        "Estimate AllChinaBuy / ACBuy import VAT and duty with published destination thresholds. Educational calculator, not legal advice.",
        f"{BASE}/customs-calculator/",
        body,
    )


def sizing_page() -> str:
    body = """
<section class="hero">
  <div class="container">
    <p class="hero__eyebrow">AllChinaBuy sizing</p>
    <h1>AllChinaBuy Spreadsheet Size Chart</h1>
    <p class="hero__sub">Chinese (CN) sizes on Taobao, Weidian and 1688 usually run small. Convert before you order from the AllChinaBuy / ACBuy spreadsheet.</p>
  </div>
</section>
<section class="section">
  <div class="container" style="max-width:820px">
    <h2>Men's clothing (tops)</h2>
    <table>
      <thead><tr><th>CN</th><th>US</th><th>UK</th><th>EU</th></tr></thead>
      <tbody>
        <tr><td>165 / S</td><td>XS</td><td>34</td><td>44</td></tr>
        <tr><td>170 / M</td><td>S</td><td>36</td><td>46</td></tr>
        <tr><td>175 / L</td><td>M</td><td>38</td><td>48</td></tr>
        <tr><td>180 / XL</td><td>L</td><td>40</td><td>50</td></tr>
        <tr><td>185 / XXL</td><td>XL</td><td>42</td><td>52</td></tr>
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
      </tbody>
    </table>
    <p>Always prefer the seller's centimetre chart on the listing over a generic letter size. More detail: <a href="/blog/posts/allchinabuy-sizing-guide/">AllChinaBuy sizing guide</a>.</p>
    <p><a class="btn btn-primary" href="/allchinabuy-spreadsheet/">Browse the spreadsheet</a></p>
  </div>
</section>
"""
    return _shell(
        "AllChinaBuy Size Chart 2026 — CN to US / EU / UK",
        "Chinese size conversion for the AllChinaBuy spreadsheet and ACBuy spreadsheet. Clothing and shoe charts plus seller measurement tips.",
        f"{BASE}/sizing-guide/",
        body,
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

    html = html.replace(
        'content="Browse 8,600+ live AllChinaBuy spreadsheet links with product images, USD prices and categories. Independent directory, refreshed from W2C data."',
        'content="The free AllChinaBuy spreadsheet (also searched as all china buy spreadsheet, ac buy spreadsheet or acbuy spreadsheet) — 8,600+ Taobao, 1688 and Weidian links with QC photos."',
    )
    html = html.replace(
        'content="AllChinaBuy Spreadsheet, AllChinaBuy Sheet, best allchinabuy spreadsheet 2026"',
        'content="AllChinaBuy Spreadsheet, all china buy spreadsheet, acbuy spreadsheet, ac buy spreadsheet, ACBuy spreadsheet, AllChinaBuy Sheet, best allchinabuy spreadsheet 2026"',
    )

    misspell = (
        '<p class="hero__sub">Also searched as <strong>all china buy spreadsheet</strong>, '
        "<strong>ac buy spreadsheet</strong> or <strong>acbuy spreadsheet</strong> — "
        "same AllChinaBuy spreadsheet, however you spell it. ACBuy is the current agent name.</p>"
    )
    if "Also searched as" not in html:
        html = html.replace(
            '<p class="hero__sub">8,600+ products from Taobao, Weidian &amp; 1688 — live product links, real QC photos, USD pricing. Free to browse. Updated daily.</p>',
            '<p class="hero__sub">8,600+ products from Taobao, Weidian &amp; 1688 — live product links, real QC photos, USD pricing. Free to browse. Updated daily.</p>\n      '
            + misspell,
            1,
        )

    about_extra = (
        "<p>People also search <strong>all china buy spreadsheet</strong>, "
        "<strong>acbuy spreadsheet</strong> and <strong>ac buy spreadsheet</strong>. "
        "Those queries point here: the live catalog is on this domain, with a dedicated "
        '<a href="/acbuy-spreadsheet/">ACBuy spreadsheet</a> alias.</p>'
    )
    if "People also search" not in html:
        html = html.replace(
            '<p>Not affiliated with <a href="https://allchinabuy.com" rel="nofollow">https://allchinabuy.com</a> — we curate the best spreadsheet experience for r/FashionReps.</p>',
            '<p>Not affiliated with <a href="https://allchinabuy.com" rel="nofollow">https://allchinabuy.com</a> — we curate the best spreadsheet experience for r/FashionReps.</p>'
            + about_extra,
            1,
        )

    extra_faq = "".join(
        (
            '<div class="faq-item" role="listitem">'
            f'<div class="faq-question" tabindex="0">{escape(item["name"])}</div>'
            f'<div class="faq-answer">{escape(item["text"])}</div></div>'
        )
        for item in FAQ_EXTRA
    )
    faq_marker = f'<div class="faq-question" tabindex="0">{escape(FAQ_EXTRA[0]["name"])}'
    if faq_marker not in html:
        html = html.replace(
            '<div class="faq-item" role="listitem"><div class="faq-question" tabindex="0">What is the AllChinaBuy Spreadsheet?</div>',
            extra_faq
            + '<div class="faq-item" role="listitem"><div class="faq-question" tabindex="0">What is the AllChinaBuy Spreadsheet?</div>',
            1,
        )

    tool_links = (
        '<li><a href="/customs-calculator/">Duty calculator</a></li>'
        '<li><a href="/sizing-guide/">Size chart</a></li>'
        '<li><a href="/tools/">Buyer tools</a></li>'
    )
    if "/customs-calculator/" not in html:
        html = html.replace(
            '<li><a href="/allchinabuy-shipping-guide/">Shipping Guide</a></li>',
            '<li><a href="/allchinabuy-shipping-guide/">Shipping Guide</a></li>\n        ' + tool_links,
            1,
        )
    return html


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
    req = Request(f"{BASE}/", headers={"User-Agent": "AllChinaBuySEO/1.0"})
    with urlopen(req, timeout=30) as resp:
        return resp.read().decode("utf-8", "replace")


def write_overlay(index_html: str) -> None:
    OVERLAY.mkdir(parents=True, exist_ok=True)
    (OVERLAY / "robots.txt").write_text(ROBOTS_TXT, encoding="utf-8")
    (OVERLAY / "llms.txt").write_text(LLMS_TXT, encoding="utf-8")
    (OVERLAY / "index.html").write_text(patch_homepage(index_html), encoding="utf-8")
    (OVERLAY / "tools").mkdir(exist_ok=True)
    (OVERLAY / "tools" / "index.html").write_text(tools_page(), encoding="utf-8")
    (OVERLAY / "customs-calculator").mkdir(exist_ok=True)
    (OVERLAY / "customs-calculator" / "index.html").write_text(customs_page(), encoding="utf-8")
    (OVERLAY / "sizing-guide").mkdir(exist_ok=True)
    (OVERLAY / "sizing-guide" / "index.html").write_text(sizing_page(), encoding="utf-8")
    sitemap_extra = """  <url><loc>https://allchina-buy.com/tools/</loc><lastmod>{today}</lastmod><changefreq>monthly</changefreq><priority>0.8</priority></url>
  <url><loc>https://allchina-buy.com/customs-calculator/</loc><lastmod>{today}</lastmod><changefreq>monthly</changefreq><priority>0.85</priority></url>
  <url><loc>https://allchina-buy.com/sizing-guide/</loc><lastmod>{today}</lastmod><changefreq>monthly</changefreq><priority>0.85</priority></url>
""".format(today=TODAY)
    (OVERLAY / "sitemap-extra.xml").write_text(sitemap_extra, encoding="utf-8")


def merge_sitemap(existing: str) -> str:
    extra_locs = [
        f"{BASE}/tools/",
        f"{BASE}/customs-calculator/",
        f"{BASE}/sizing-guide/",
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
    fixture = """<!DOCTYPE html><html><head>
<meta name="description" content="Browse 8,600+ live AllChinaBuy spreadsheet links with product images, USD prices and categories. Independent directory, refreshed from W2C data.">
<meta name="keywords" content="AllChinaBuy Spreadsheet, AllChinaBuy Sheet, best allchinabuy spreadsheet 2026">
<script type="application/ld+json">{"@context":"https://schema.org","@graph":[{"@type":"WebSite","name":"old"}]}</script>
</head><body>
<p class="hero__sub">8,600+ products from Taobao, Weidian &amp; 1688 — live product links, real QC photos, USD pricing. Free to browse. Updated daily.</p>
<p>Not affiliated with <a href="https://allchinabuy.com" rel="nofollow">https://allchinabuy.com</a> — we curate the best spreadsheet experience for r/FashionReps.</p>
<div class="faq-item" role="listitem"><div class="faq-question" tabindex="0">What is the AllChinaBuy Spreadsheet?</div><div class="faq-answer">A curated database.</div></div>
<li><a href="/allchinabuy-shipping-guide/">Shipping Guide</a></li>
</body></html>"""
    patched = patch_homepage(fixture)
    types = validate_jsonld(patched)
    assert "WebSite" in types and "FAQPage" in types and "SoftwareApplication" in types, types
    graph = json.loads(JSONLD_RE.search(patched).group(0).split(">", 1)[1].rsplit("</", 1)[0])
    website = next(n for n in graph["@graph"] if n["@type"] == "WebSite")
    assert "All China Buy Spreadsheet" in website["alternateName"]
    assert "all china buy spreadsheet" in patched.lower()
    assert "/customs-calculator/" in patched
    for page in (tools_page(), customs_page(), sizing_page()):
        assert "<h1>" in page and "AllChinaBuy" in page
    print("self-test OK", types)


def _connect():
    try:
        import paramiko
    except ImportError:
        import subprocess

        subprocess.check_call([sys.executable, "-m", "pip", "install", "paramiko", "-q"])
        import paramiko

    password = (
        os.environ.get("ALLCHINA_DEPLOY_PASS")
        or os.environ.get("ORIENTDIG_DEPLOY_PASS")
        or os.environ.get("KAKOBUY_DEPLOY_PASS")
        or os.environ.get("LITBUY_DEPLOY_PASS")
    )
    if not password:
        print("Set ALLCHINA_DEPLOY_PASS (or ORIENTDIG_DEPLOY_PASS)", file=sys.stderr)
        sys.exit(1)
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(HOST, username=USER, password=password, timeout=30)
    return client


def _run(client, cmd: str, timeout: int = 60) -> str:
    _, stdout, stderr = client.exec_command(cmd, timeout=timeout)
    return (stdout.read() + stderr.read()).decode(errors="replace").strip()


def deploy() -> None:
    html = fetch_homepage()
    write_overlay(html)
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

    uploads = {
        str(OVERLAY / "index.html"): f"{WEBROOT}/index.html",
        str(OVERLAY / "robots.txt"): f"{WEBROOT}/robots.txt",
        str(OVERLAY / "llms.txt"): f"{WEBROOT}/llms.txt",
        str(OVERLAY / "tools" / "index.html"): f"{WEBROOT}/tools/index.html",
        str(OVERLAY / "customs-calculator" / "index.html"): f"{WEBROOT}/customs-calculator/index.html",
        str(OVERLAY / "sizing-guide" / "index.html"): f"{WEBROOT}/sizing-guide/index.html",
    }
    for local, remote in uploads.items():
        parent = remote.rsplit("/", 1)[0]
        _run(client, f"mkdir -p {parent}")
        sftp.put(local, remote)
        print("uploaded", remote)

    with sftp.open(f"{WEBROOT}/sitemap.xml", "r") as fh:
        existing = fh.read().decode("utf-8")
    merged = merge_sitemap(existing)
    tmp = f"{WEBROOT}/sitemap.xml.new"
    with sftp.open(tmp, "w") as fh:
        fh.write(merged)
    _run(client, f"mv {tmp} {WEBROOT}/sitemap.xml && chown -R www:www {WEBROOT}/index.html {WEBROOT}/robots.txt {WEBROOT}/llms.txt {WEBROOT}/sitemap.xml {WEBROOT}/tools {WEBROOT}/customs-calculator {WEBROOT}/sizing-guide")
    sftp.close()
    client.close()
    print("allchina-buy seo deploy done")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--build", action="store_true")
    parser.add_argument("--file", type=Path)
    parser.add_argument("--deploy", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        self_test()
        return
    if args.deploy:
        deploy()
        return
    source = args.file.read_text(encoding="utf-8") if args.file else fetch_homepage()
    write_overlay(source)
    types = validate_jsonld((OVERLAY / "index.html").read_text(encoding="utf-8"))
    print(f"wrote {OVERLAY} json-ld={types}")


if __name__ == "__main__":
    main()
