#!/usr/bin/env python3
"""Build crawlable AllChinaBuy product pages from the W2C typesense feed.

Mirrors lit-buy-spreadsheet.com /product/{slug}-{id} long-tail URLs so Google
can rank queries like "canada goose puffer allchinabuy" on this domain instead
of only the JS spreadsheet grid.
"""

from __future__ import annotations

import argparse
import json
import re
import ssl
import urllib.parse
import urllib.request
import shutil
from datetime import date, timedelta
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OVERLAY = ROOT / "sites" / "allchina-buy.com" / "overlay"
CACHE = ROOT / "sites" / "allchina-buy.com" / "products.json"
W2C_PRODUCTS = "https://w2clinks.com/public/typesense-search.php"
W2C_BASE = "https://w2clinks.com"
BASE = "https://allchina-buy.com"
REGISTER = "https://allchinabuy.com"
TODAY = date.today().isoformat()
USD_FROM_CNY = 0.138
# Display-only FX for product landings (same set as the LitBuy competitor page).
FX_FROM_CNY = {
    "USD": ("USD$", 0.138),
    "GBP": ("GBP£", 0.109),
    "EUR": ("EUR€", 0.127),
    "NZD": ("NZD NZ$", 0.230),
    "AUD": ("AUD A$", 0.213),
    "CAD": ("CAD C$", 0.190),
    "MXN": ("MXN$", 2.55),
    "BRL": ("BRL R$", 0.72),
    "KRW": ("KRW₩", 186.0),
    "PLN": ("PLN zł", 0.54),
}

SSL_CTX = ssl.create_default_context()
SSL_CTX.check_hostname = False
SSL_CTX.verify_mode = ssl.CERT_NONE

# Diversify beyond "newest hoodies". Caps sum to ~1600 like the competitor sitemap.
CATEGORY_QUOTAS: list[tuple[str, int]] = [
    ("SNEAKERS", 320),
    ("T-SHIRT", 220),
    ("HOODIE", 200),
    ("JACKET", 160),
    ("SHORTS", 120),
    ("BAGS", 120),
    ("TROUSERS", 100),
    ("SWEATER", 80),
    ("ELECTRONICS", 80),
    ("WATCH", 80),
    ("SHELL JACKET", 60),
    ("ACCESSORIES", 40),
]

CATEGORY_PATHS = {
    "SNEAKERS": "/allchinabuy-spreadsheet-shoes/",
    "SLIPPERS": "/allchinabuy-spreadsheet-other-goods/",
    "T-SHIRT": "/allchinabuy-spreadsheet-t-shirts/",
    "SHIRT": "/allchinabuy-spreadsheet-t-shirts/",
    "HOODIE": "/allchinabuy-spreadsheet-hoodies/",
    "SWEATER": "/allchinabuy-spreadsheet-hoodies/",
    "JACKET": "/allchinabuy-spreadsheet-jackets/",
    "SHELL JACKET": "/allchinabuy-spreadsheet-jackets/",
    "VEST": "/allchinabuy-spreadsheet-jackets/",
    "SHORTS": "/allchinabuy-spreadsheet-pants/",
    "TROUSERS": "/allchinabuy-spreadsheet-pants/",
    "BAGS": "/allchinabuy-spreadsheet-bags/",
    "BAG": "/allchinabuy-spreadsheet-bags/",
    "ACCESSORIES": "/allchinabuy-spreadsheet-accessories/",
    "WATCH": "/allchinabuy-spreadsheet-accessories/",
    "ELECTRONICS": "/allchinabuy-spreadsheet-electronics/",
    "JERSEY": "/allchinabuy-spreadsheet-jerseys/",
    "POLO": "/allchinabuy-spreadsheet-womens-fashion/",
    "LONG SLEEVED": "/allchinabuy-spreadsheet-t-shirts/",
    "FLEECE JACKET": "/allchinabuy-spreadsheet-jackets/",
    "DOWN JACKETS": "/allchinabuy-spreadsheet-jackets/",
}


def http_json(url: str) -> dict:
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "AllChinaBuySEO/1.0", "Accept": "application/json"},
    )
    with urllib.request.urlopen(req, context=SSL_CTX, timeout=30) as resp:
        return json.loads(resp.read().decode("utf-8", "replace"))


def slugify(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-")[:60].strip("-") or "find"


def infer_platform(url: str) -> str:
    u = url.lower()
    if "1688" in u:
        return "1688"
    if "taobao" in u or "/tb_" in u:
        return "Taobao"
    if "wd_" in u or "weidian" in u or "geilicdn" in u:
        return "Weidian"
    return "Chinese marketplace"


def abs_w2c(url: str) -> str:
    if not url:
        return W2C_BASE + "/spreadsheet/"
    if url.startswith("/"):
        return W2C_BASE + url
    return url


def as_float(price) -> float:
    try:
        return float(price)
    except (TypeError, ValueError):
        return 0.0


def usd(price) -> str:
    return f"{as_float(price) * USD_FROM_CNY:.2f}"


def money_row(price) -> str:
    cny = as_float(price)
    parts = [f"{label}{cny * rate:.2f}" for _code, (label, rate) in FX_FROM_CNY.items()]
    parts.append(f"CNY¥{cny:.2f}")
    return " ".join(parts)


def describe(item: dict) -> str:
    title = item["title"]
    brand = item.get("brand") or "this listing"
    cat = (item.get("category") or "product").replace("_", " ").title()
    platform = item["platform"]
    price = item.get("price") or 0
    extra = {
        "SNEAKERS": "Check insole length in centimetres against our size chart before you submit the AllChinaBuy order.",
        "HOODIE": "Compare hoodie measurements (shoulder, chest, length) with a hoodie you already own.",
        "JACKET": "Puffers and shells vary in fill and hardware — wait for warehouse QC before shipping.",
        "BAGS": "Inspect stitching, zipper pull and logo placement on QC photos.",
        "WATCH": "Ask the agent for a close-up of the dial, clasp and movement if listed.",
        "ELECTRONICS": "Confirm voltage, plug type and that the listing is the exact model you want.",
        "T-SHIRT": "Chinese letter sizes often run small; use the centimetre chart on the listing.",
        "SHORTS": "Check inseam and waist in centimetres rather than the tagged letter size.",
    }.get((item.get("category") or "").upper(), "Review warehouse QC photos before you approve international shipping.")
    return (
        f"{title} is a {cat} row in the AllChinaBuy spreadsheet, sourced from {platform} "
        f"at ¥{price} CNY (about ${usd(price)} USD at the live feed rate). "
        f"{brand} shoppers typically copy this W2C link into ACBuy / AllChinaBuy, pay the item, "
        f"then inspect QC photos in the warehouse. {extra}"
    )


def category_path(cat: str) -> str:
    return CATEGORY_PATHS.get((cat or "").upper(), "/allchinabuy-spreadsheet/")


def normalize(hit: dict) -> dict | None:
    title = str(hit.get("title") or "").strip()
    aid = hit.get("aid")
    if not title or aid is None:
        return None
    url = abs_w2c(str(hit.get("url") or ""))
    item = {
        "aid": int(aid),
        "title": title,
        "url": url,
        "image": str(hit.get("image") or ""),
        "category": str(hit.get("category") or ""),
        "brand": str(hit.get("brand") or ""),
        "price": hit.get("price") if hit.get("price") is not None else 0,
        "platform": infer_platform(url + " " + str(hit.get("image") or "")),
    }
    item["slug"] = f"{slugify(title)}-{item['aid']}"
    item["description"] = describe(item)
    return item


def fetch_products(limit: int = 1600) -> list[dict]:
    seen: set[int] = set()
    items: list[dict] = []
    for cat, quota in CATEGORY_QUOTAS:
        page = 1
        got = 0
        while got < quota and len(items) < limit:
            qs = urllib.parse.urlencode(
                {"page": page, "per_page": 60, "sort": "newest", "category": cat}
            )
            data = http_json(f"{W2C_PRODUCTS}?{qs}")
            hits = data.get("hits") or []
            if not hits:
                break
            for hit in hits:
                row = normalize(hit)
                if not row or row["aid"] in seen:
                    continue
                seen.add(row["aid"])
                items.append(row)
                got += 1
                if got >= quota or len(items) >= limit:
                    break
            page += 1
            if page > 12:
                break
    # Fill remainder from unfiltered newest.
    page = 1
    while len(items) < limit and page <= 20:
        qs = urllib.parse.urlencode({"page": page, "per_page": 60, "sort": "newest"})
        data = http_json(f"{W2C_PRODUCTS}?{qs}")
        hits = data.get("hits") or []
        if not hits:
            break
        for hit in hits:
            row = normalize(hit)
            if not row or row["aid"] in seen:
                continue
            seen.add(row["aid"])
            items.append(row)
            if len(items) >= limit:
                break
        page += 1
    return items


def attach_related(items: list[dict], k: int = 6) -> None:
    by_cat: dict[str, list[dict]] = {}
    for it in items:
        by_cat.setdefault(it.get("category") or "", []).append(it)
    for it in items:
        pool = [x for x in by_cat.get(it.get("category") or "", []) if x["aid"] != it["aid"]]
        it["related"] = pool[:k]


def product_jsonld(item: dict) -> str:
    canonical = f"{BASE}/product/{item['slug']}/"
    valid = (date.today() + timedelta(days=30)).isoformat()
    payload = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "Product",
                "@id": canonical + "#product",
                "name": item["title"],
                "image": [item["image"]] if item.get("image") else [],
                "description": item["description"],
                "brand": {"@type": "Brand", "name": item.get("brand") or item["platform"]},
                "category": item.get("category") or "Product",
                "offers": {
                    "@type": "Offer",
                    "url": canonical,
                    "priceCurrency": "CNY",
                    "price": item.get("price") or 0,
                    "availability": "https://schema.org/InStock",
                    "priceValidUntil": valid,
                    "seller": {"@type": "Organization", "name": "AllChinaBuy Spreadsheet"},
                },
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
                    {"@type": "ListItem", "position": 3, "name": item["title"], "item": canonical},
                ],
            },
            {
                "@type": "FAQPage",
                "mainEntity": [
                    {
                        "@type": "Question",
                        "name": f"How do I buy {item['title']} with AllChinaBuy?",
                        "acceptedAnswer": {
                            "@type": "Answer",
                            "text": (
                                "Copy the W2C / marketplace URL, paste it into AllChinaBuy (now ACBuy), "
                                "pay the item, then review warehouse QC photos before international shipping."
                            ),
                        },
                    },
                    {
                        "@type": "Question",
                        "name": "Is this the official AllChinaBuy product page?",
                        "acceptedAnswer": {
                            "@type": "Answer",
                            "text": (
                                "No. This is an independent AllChinaBuy spreadsheet landing for long-tail "
                                "search. Checkout happens on AllChinaBuy / ACBuy."
                            ),
                        },
                    },
                ],
            },
        ],
    }
    return json.dumps(payload, ensure_ascii=False, separators=(",", ":"))


def related_html(item: dict) -> str:
    related = item.get("related") or []
    if not related:
        return ""
    lis = "\n".join(
        f'<li><a href="/product/{escape(rel["slug"])}/">{escape(rel["title"])}</a>'
        f' · ¥{escape(str(rel.get("price") or 0))}</li>'
        for rel in related
    )
    return f"<h2>Related AllChinaBuy spreadsheet finds</h2>\n<ul>\n{lis}\n</ul>"


def render_product(item: dict) -> str:
    title = item["title"]
    slug = item["slug"]
    canonical = f"{BASE}/product/{slug}/"
    cat_path = category_path(item.get("category") or "")
    cat_label = (item.get("category") or "catalog").replace("_", " ").title()
    img = item.get("image") or ""
    img_tag = (
        f'<img src="{escape(img)}" alt="{escape(title)}" width="480" height="480" loading="lazy">'
        if img
        else ""
    )
    brand = item.get("brand") or "W2C listing"
    desc = item["description"]
    price_cny = item.get("price") or 0
    schema = product_jsonld(item)
    meta = escape(desc[:220])
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>{escape(title)} (¥{escape(str(price_cny))} CNY) — AllChinaBuy Find | AllChinaBuy Spreadsheet 2026</title>
<meta name="description" content="{meta}">
<link rel="canonical" href="{canonical}">
<meta name="robots" content="index, follow, max-image-preview:large">
<link rel="stylesheet" href="/assets/css/main.css?v=seo20260917">
<script type="application/ld+json">{schema}</script>
</head>
<body>
<nav class="nav"><div class="container nav__inner">
<a href="/" class="nav__logo">AllChinaBuy Spreadsheet</a>
<ul class="nav__links"><li><a href="/allchinabuy-spreadsheet/">Spreadsheet</a></li><li><a href="/tools/">Tools</a></li></ul>
</div></nav>
<main>
<section class="section">
<div class="container" style="max-width:860px">
<p class="hero__eyebrow"><a href="/">Home</a> · <a href="/product/">Products</a> · <a href="{cat_path}">{escape(cat_label)}</a></p>
<h1>{escape(title)}</h1>
{img_tag}
<p>{escape(desc)}</p>
<p>Listed by <strong>{escape(brand)}</strong> on {escape(item["platform"])}.</p>
<h2>Pricing</h2>
<p>{escape(money_row(price_cny))}</p>
<h2>About this product in our AllChinaBuy spreadsheet</h2>
<p>Looking to buy {escape(title)}? This crawlable row exists so searches such as “{escape(title.lower())} allchinabuy” and “{escape(brand.lower())} {escape(cat_label.lower())} spreadsheet” land on allchina-buy.com instead of a JavaScript-only grid. The live {escape(item["platform"])} link is on W2C; checkout is on AllChinaBuy / ACBuy.</p>
<h2>How to buy this AllChinaBuy spreadsheet find</h2>
<ol>
<li>Open the live listing on W2C and copy the {escape(item['platform'])} URL.</li>
<li>Paste it into <a href="{REGISTER}" rel="nofollow noopener" target="_blank">AllChinaBuy / ACBuy</a>.</li>
<li>Wait for warehouse QC photos, then ship. Use the <a href="/sizing-guide/">size chart</a> and <a href="/customs-calculator/">duty calculator</a> before you submit.</li>
</ol>
<p>
<a class="btn btn-primary" href="{REGISTER}" rel="nofollow noopener" target="_blank">Buy via AllChinaBuy</a>
<a class="btn btn-secondary" href="{escape(item['url'])}" rel="nofollow noopener" target="_blank">View on W2C</a>
<a class="btn btn-secondary" href="{cat_path}">More {escape(cat_label)}</a>
</p>
{related_html(item)}
<p>Independent AllChinaBuy spreadsheet landing — not the official store.</p>
</div>
</section>
</main>
<footer class="footer"><div class="container"><p>Independent AllChinaBuy / ACBuy spreadsheet — not affiliated with allchinabuy.com.</p></div></footer>
</body>
</html>
"""


def render_product_index(items: list[dict]) -> str:
    groups: dict[str, list[dict]] = {}
    for item in items:
        groups.setdefault((item.get("category") or "OTHER").upper(), []).append(item)
    chunks = []
    for cat in sorted(groups):
        rows = groups[cat]
        lis = "\n".join(
            f'<li><a href="/product/{escape(it["slug"])}/">{escape(it["title"])}</a> · ¥{escape(str(it.get("price") or 0))}</li>'
            for it in rows[:80]
        )
        more = f"<p>{len(rows)} finds in this category.</p>" if len(rows) > 80 else ""
        chunks.append(f"<h2>{escape(cat.title())}</h2>\n{more}<ul>\n{lis}\n</ul>")
    body = "\n".join(chunks)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>AllChinaBuy Spreadsheet Product Finds 2026</title>
<meta name="description" content="Crawlable AllChinaBuy / ACBuy spreadsheet product pages for long-tail searches — sneakers, hoodies, bags, jackets and more from Taobao, Weidian and 1688.">
<link rel="canonical" href="{BASE}/product/">
<meta name="robots" content="index, follow">
<link rel="stylesheet" href="/assets/css/main.css?v=seo20260917">
</head>
<body>
<nav class="nav"><div class="container nav__inner">
<a href="/" class="nav__logo">AllChinaBuy Spreadsheet</a>
<ul class="nav__links"><li><a href="/allchinabuy-spreadsheet/">Spreadsheet</a></li><li><a href="/tools/">Tools</a></li></ul>
</div></nav>
<main>
<section class="hero"><div class="container">
<h1>AllChinaBuy spreadsheet product finds</h1>
<p class="hero__sub">{len(items)} crawlable product pages so Google can rank individual W2C rows, not only the JavaScript catalog.</p>
</div></section>
<section class="section"><div class="container" style="max-width:860px">
{body}
</div></section>
</main>
<footer class="footer"><div class="container"><p>Independent AllChinaBuy / ACBuy spreadsheet — not affiliated with allchinabuy.com.</p></div></footer>
</body>
</html>
"""


def write_sitemap(items: list[dict]) -> str:
    urls = [
        "  <url>"
        f"<loc>{BASE}/product/{item['slug']}/</loc>"
        f"<lastmod>{TODAY}</lastmod>"
        "<changefreq>weekly</changefreq><priority>0.6</priority></url>"
        for item in items
    ]
    return (
        "<?xml version='1.0' encoding='utf-8'?>\n"
        "<urlset xmlns='http://www.sitemaps.org/schemas/sitemap/0.9'>\n"
        + "\n".join(urls)
        + "\n</urlset>\n"
    )


def build_product_pages(items: list[dict] | None = None, limit: int = 1600) -> list[dict]:
    if items is None:
        if CACHE.exists():
            items = json.loads(CACHE.read_text(encoding="utf-8"))
        else:
            items = fetch_products(limit=limit)
            CACHE.write_text(json.dumps(items, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    items = items[:limit]
    attach_related(items)
    product_root = OVERLAY / "product"
    if product_root.exists():
        shutil.rmtree(product_root)
    product_root.mkdir(parents=True, exist_ok=True)
    (product_root / "index.html").write_text(render_product_index(items), encoding="utf-8")
    for item in items:
        dest = product_root / item["slug"]
        dest.mkdir(parents=True, exist_ok=True)
        (dest / "index.html").write_text(render_product(item), encoding="utf-8")
        item.pop("related", None)
    (OVERLAY / "sitemap-products.xml").write_text(write_sitemap(items), encoding="utf-8")
    return items


def self_test() -> None:
    hit = {
        "title": "Designer Streetwear Backpack Collection",
        "url": "/yupoo-bags/wd_123.html",
        "image": "https://example.com/bag.webp",
        "category": "BAGS",
        "brand": "Street",
        "price": 78,
        "aid": 309754,
    }
    item = normalize(hit)
    assert item and item["slug"].endswith("-309754")
    sibling = normalize({**hit, "title": "Canvas Weekend Backpack", "aid": 309755})
    attach_related([item, sibling])
    html = render_product(item)
    assert "application/ld+json" in html
    assert "USD$" in html and "Related AllChinaBuy" in html
    payload = json.loads(re.search(r"application/ld\+json\">(.*?)</script>", html).group(1))
    types = [n["@type"] for n in payload["@graph"]]
    assert types == ["Product", "BreadcrumbList", "FAQPage"]
    assert "AllChinaBuy spreadsheet" in html
    sm = write_sitemap([item])
    assert item["slug"] in sm
    index_html = render_product_index([item, sibling])
    assert item["slug"] in index_html
    print("product self-test OK", item["slug"])


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--fetch", action="store_true")
    parser.add_argument("--limit", type=int, default=1600)
    args = parser.parse_args()
    if args.self_test:
        self_test()
        return
    if args.fetch or not CACHE.exists():
        items = fetch_products(limit=args.limit)
        CACHE.write_text(json.dumps(items, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
        print(f"cached {len(items)} products -> {CACHE}")
    else:
        items = json.loads(CACHE.read_text(encoding="utf-8"))[: args.limit]
    built = build_product_pages(items, limit=args.limit)
    print(f"wrote {len(built)} product pages")


if __name__ == "__main__":
    main()
