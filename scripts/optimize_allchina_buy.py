#!/usr/bin/env python3
"""Apply lit-buy-spreadsheet.com-style SEO to allchina-buy.com.

The competitor ranks on spaced/misspelled queries plus AI crawlers. This
script mirrors that playbook for AllChinaBuy / ACBuy:

  - WebSite.alternateName for all china buy / ac buy / acbuy
  - FAQ + visible copy that maps those spellings to this hub
  - SoftwareApplication / ItemList / Breadcrumb schema
  - llms.txt + AI-bot robots.txt
  - Dedicated /tools/, /customs-calculator/, /sizing-guide/,
    /compare-shopping-agents/ landings
  - Crawlable /product/{slug}-{aid}/ long-tail pages from W2C

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
Allow: /tools/
Allow: /customs-calculator
Allow: /sizing-guide
Allow: /compare-shopping-agents
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
Sitemap: https://allchina-buy.com/sitemap-products.xml
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
- Shopping agent comparison: https://allchina-buy.com/compare-shopping-agents/
- ACBuy vs AllChinaBuy: https://allchina-buy.com/acbuy-vs-allchinabuy/
- Tools: https://allchina-buy.com/tools/
- Product long-tail pages: https://allchina-buy.com/product/
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
<link rel="stylesheet" href="/assets/css/main.css?v=seo20260917">
<style>main table{{width:100%;border-collapse:collapse;margin:16px 0}}main th,main td{{border-bottom:1px solid #e5e5e5;padding:8px 10px;text-align:left}}main label{{display:flex;flex-direction:column;gap:6px;font-size:.9rem}}main select,main input[type=number]{{padding:10px;border:1px solid #ddd;border-radius:8px}}</style>
<meta property="og:title" content="{title_e}">
<meta property="og:description" content="{desc_e}">
<meta property="og:url" content="{canonical}">
<meta property="og:type" content="website">
{extra_head}
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
    <p><a href="/">Home</a> · <a href="/allchinabuy-spreadsheet/">Spreadsheet</a> · <a href="/tools/">Tools</a> · <a href="/customs-calculator/">Duty calculator</a> · <a href="/sizing-guide/">Size chart</a> · <a href="/compare-shopping-agents/">Agent comparison</a></p>
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
    <h1>Free Tools for AllChinaBuy / ACBuy Shopping</h1>
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
        <p class="feature-card__desc">ACBuy / AllChinaBuy vs Kakobuy, CNFans, Superbuy, LitBuy and Pandabuy — fees, QC, storage and shipping.</p>
      </a>
      <a class="feature-card" href="/allchinabuy-shipping-guide/">
        <h2 class="feature-card__title">Shipping &amp; customs guides</h2>
        <p class="feature-card__desc">Lines, times, QC rejection and the country customs write-up on this hub.</p>
      </a>
    </div>
  </div>
</section>
"""
    return _shell(
        "Free AllChinaBuy Tools 2026 — Duty Calculator, Size Chart, Agent Comparison",
        "Free AllChinaBuy / ACBuy tools: import duty calculator, Chinese size chart and shopping agent comparison. No signup.",
        f"{BASE}/tools/",
        body,
    )


def customs_page() -> str:
    body = """
<section class="hero">
  <div class="container">
    <p class="hero__eyebrow">AllChinaBuy customs</p>
    <h1>Import Duty Calculator 2026</h1>
    <p class="hero__sub">Estimate VAT/GST and customs duty for AllChinaBuy / ACBuy parcels. Educational calculator using published destination thresholds — not legal advice. Confirm current rules with your customs authority before you ship.</p>
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
    <h2>How this AllChinaBuy calculator works</h2>
    <p>Built for searches such as <strong>all china buy customs</strong>, <strong>acbuy duty</strong> and <strong>allchinabuy import tax</strong>. Thresholds change; treat the numbers as a starting point:</p>
    <ul>
      <li><strong>United States</strong> — de minimis treatment has been changing; verify CBP before you ship.</li>
      <li><strong>United Kingdom</strong> — VAT commonly 20%; customs duty often starts above £135 and depends on HS code.</li>
      <li><strong>EU</strong> — VAT is usually due at the destination rate; customs duty commonly starts above €150.</li>
      <li><strong>Canada</strong> — general goods de minimis is low; GST/HST may still apply.</li>
      <li><strong>Australia</strong> — GST often 10%, with a high-value threshold around AUD $1,000.</li>
      <li><strong>New Zealand</strong> — GST commonly 15% on imported goods.</li>
    </ul>
    <p>Declare the accurate transaction value. Undervaluing a parcel to avoid tax is illegal. Country write-ups: <a href="/blog/posts/allchinabuy-customs-guide/">customs guide</a> and <a href="/allchinabuy-shipping-guide/">shipping guide</a>.</p>
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
        "Import Duty Calculator 2026 — AllChinaBuy / ACBuy Customs Estimator",
        "Estimate AllChinaBuy import VAT and duty for US, UK, EU, Canada, Australia and New Zealand. Educational calculator, not legal advice.",
        f"{BASE}/customs-calculator/",
        body,
    )


def sizing_page() -> str:
    body = """
<section class="hero">
  <div class="container">
    <p class="hero__eyebrow">AllChinaBuy sizing</p>
    <h1>Chinese Size Chart 2026</h1>
    <p class="hero__sub">Convert CN sizes to US, EU, UK and AU for clothes and shoes before you order from the AllChinaBuy / ACBuy spreadsheet. Chinese letter sizes usually run small.</p>
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
    <p>Always prefer the seller's centimetre chart over a generic letter size. Longer write-up: <a href="/blog/posts/allchinabuy-sizing-guide/">AllChinaBuy sizing guide</a>.</p>
  </div>
</section>
"""
    return _shell(
        "Chinese Size Chart 2026 — CN to US / EU / UK for AllChinaBuy",
        "Chinese size conversion for the AllChinaBuy spreadsheet: men's and women's clothing and shoes, with foot length in centimetres.",
        f"{BASE}/sizing-guide/",
        body,
    )


def compare_page() -> str:
    body = """
<section class="hero">
  <div class="container">
    <p class="hero__eyebrow">Updated 2026</p>
    <h1>Which Chinese Shopping Agent is Best in 2026?</h1>
    <p class="hero__sub">Side-by-side look at ACBuy / AllChinaBuy, Kakobuy, CNFans, Superbuy, LitBuy and Pandabuy — fees, QC photos, storage and shipping. This hub's spreadsheet is built for AllChinaBuy / ACBuy checkout.</p>
  </div>
</section>
<section class="section">
  <div class="container">
    <table>
      <thead>
        <tr><th>Agent</th><th>Service fee</th><th>QC photos</th><th>Free storage</th><th>Best for</th></tr>
      </thead>
      <tbody>
        <tr><td>ACBuy / AllChinaBuy</td><td>0%</td><td>Free, unlimited</td><td>Often 90–180 days</td><td>This spreadsheet</td></tr>
        <tr><td>Kakobuy</td><td>Varies</td><td>Warehouse QC</td><td>Agent policy</td><td>EU / invite-code users</td></tr>
        <tr><td>CNFans</td><td>Often 0%</td><td>Free QC</td><td>Long storage on many plans</td><td>Community threads</td></tr>
        <tr><td>Superbuy</td><td>Often 0%</td><td>Limited free photos</td><td>~90 days</td><td>Beginners</td></tr>
        <tr><td>LitBuy</td><td>About 5–10%</td><td>Free QC</td><td>~90 days</td><td>Shipping-line choice</td></tr>
        <tr><td>Pandabuy</td><td>Often 0%</td><td>Free QC</td><td>~90 days</td><td>Legacy rep users</td></tr>
      </tbody>
    </table>
    <h2>What 0% fees actually mean</h2>
    <p>ACBuy, CNFans, Superbuy and Pandabuy often advertise 0% item fees. Revenue still has to come from somewhere — usually shipping markups. LitBuy states a service fee and may price freight closer to cost. Always compare <strong>item + fee + freight</strong> for your haul weight, not the headline percentage.</p>
    <h2>ACBuy vs AllChinaBuy</h2>
    <p>They are the same agent after a rebrand. Use this site's <a href="/acbuy-vs-allchinabuy/">ACBuy vs AllChinaBuy</a> page for the name change, then browse the <a href="/acbuy-spreadsheet/">ACBuy spreadsheet</a> or <a href="/allchinabuy-spreadsheet/">AllChinaBuy spreadsheet</a> — same catalog.</p>
    <h2>FAQ</h2>
    <h3>Which agent is cheapest?</h3>
    <p>The cheapest checkout is the lowest landed cost after shipping, not the lowest advertised fee. Weigh a 2–5 kg haul on two agents before you standardise.</p>
    <h3>Which agent has the best QC?</h3>
    <p>Unlimited warehouse photos matter more than branding. ACBuy / AllChinaBuy, CNFans and LitBuy typically allow free QC on each item; some 0% agents cap free photos.</p>
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
                "name": "Is ACBuy the same as AllChinaBuy?",
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": "Yes. ACBuy rebranded from AllChinaBuy. This spreadsheet hub is built for that agent.",
                },
            },
        ],
    }
    extra = f'<script type="application/ld+json">{json.dumps(faq, ensure_ascii=False, separators=(",", ":"))}</script>'
    return _shell(
        "Shopping Agent Comparison 2026: ACBuy vs Kakobuy vs CNFans vs Superbuy",
        "Compare ACBuy / AllChinaBuy with Kakobuy, CNFans, Superbuy, LitBuy and Pandabuy — fees, QC photos, storage and shipping for spreadsheet users.",
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
        '<li><a href="/compare-shopping-agents/">Agent comparison</a></li>'
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


def _products_mod():
    try:
        import allchina_products
        return allchina_products
    except ImportError:
        import importlib.util

        spec = importlib.util.spec_from_file_location(
            "allchina_products", Path(__file__).with_name("allchina_products.py")
        )
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        return mod


def write_overlay(index_html: str, products: bool = True, product_limit: int = 0) -> None:
    OVERLAY.mkdir(parents=True, exist_ok=True)
    (OVERLAY / "robots.txt").write_text(ROBOTS_TXT, encoding="utf-8")
    (OVERLAY / "llms.txt").write_text(LLMS_TXT, encoding="utf-8")
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
    sitemap_extra = """  <url><loc>https://allchina-buy.com/tools/</loc><lastmod>{today}</lastmod><changefreq>monthly</changefreq><priority>0.8</priority></url>
  <url><loc>https://allchina-buy.com/customs-calculator/</loc><lastmod>{today}</lastmod><changefreq>monthly</changefreq><priority>0.85</priority></url>
  <url><loc>https://allchina-buy.com/sizing-guide/</loc><lastmod>{today}</lastmod><changefreq>monthly</changefreq><priority>0.85</priority></url>
  <url><loc>https://allchina-buy.com/compare-shopping-agents/</loc><lastmod>{today}</lastmod><changefreq>monthly</changefreq><priority>0.85</priority></url>
  <url><loc>https://allchina-buy.com/product/</loc><lastmod>{today}</lastmod><changefreq>daily</changefreq><priority>0.7</priority></url>
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
    assert "/compare-shopping-agents/" in patched
    for page in (tools_page(), customs_page(), sizing_page(), compare_page()):
        assert "<h1>" in page and "AllChinaBuy" in page
    compare_html = compare_page()
    assert "Kakobuy" in compare_html and "application/ld+json" in compare_html
    _products_mod().self_test()
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
        str(OVERLAY / "compare-shopping-agents" / "index.html"): f"{WEBROOT}/compare-shopping-agents/index.html",
        str(OVERLAY / "sitemap-products.xml"): f"{WEBROOT}/sitemap-products.xml",
        str(OVERLAY / "api" / "products.php"): f"{WEBROOT}/api/products.php",
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

        tar_path = Path(tempfile.gettempdir()) / "allchina-product-pages.tar.gz"
        with tarfile.open(tar_path, "w:gz") as tar:
            tar.add(product_dir, arcname="product")
        remote_tar = "/tmp/allchina-product-pages.tar.gz"
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
                    f"{WEBROOT}/compare-shopping-agents {WEBROOT}/product {WEBROOT}/api/products.php"
                ),
            ]
        ),
    )
    sftp.close()
    client.close()
    print("allchina-buy seo deploy done")


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
        deploy()
        return
    source = args.file.read_text(encoding="utf-8") if args.file else fetch_homepage()
    write_overlay(source, products=not args.skip_products, product_limit=args.product_limit)
    types = validate_jsonld((OVERLAY / "index.html").read_text(encoding="utf-8"))
    print(f"wrote {OVERLAY} json-ld={types}")


if __name__ == "__main__":
    main()
