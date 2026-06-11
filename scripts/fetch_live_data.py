"""Fetch live product and OrientDig help data at build time."""

from __future__ import annotations

import json
import re
import ssl
import urllib.parse
import urllib.request
from html import unescape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CACHE_PATH = ROOT / "data" / "live-cache.json"

W2C_PRODUCTS = "https://w2clinks.com/public/typesense-search.php"
W2C_BASE = "https://w2clinks.com"
OD_HELP = "https://orientdig.com/wp-json/wp/v2/help-center"

SHIPPING_SLUGS = [
    "the-duration-for-which-parcel-can-be-stored-in-the-orientdig-warehouse-for-free-is-30-days",
    "why-should-i-combine-delivery",
    "compensation-standard-for-insured-parcel",
    "about-orientdig-2",
]

COUPON_SLUGS = [
    "affiliate-system-rules",
    "about-orientdig-2",
]

SSL_CTX = ssl.create_default_context()
SSL_CTX.check_hostname = False
SSL_CTX.verify_mode = ssl.CERT_NONE


def http_get(url: str, timeout: int = 20) -> str | None:
    try:
        req = urllib.request.Request(
            url,
            headers={"User-Agent": "OrientDigSpreadsheetBuilder/1.0", "Accept": "application/json"},
        )
        with urllib.request.urlopen(req, context=SSL_CTX, timeout=timeout) as resp:
            return resp.read().decode("utf-8", errors="replace")
    except Exception:
        return None


def fetch_products(per_page: int = 12, sort: str = "newest") -> list[dict]:
    qs = urllib.parse.urlencode({"page": 1, "per_page": per_page, "sort": sort})
    raw = http_get(f"{W2C_PRODUCTS}?{qs}")
    if not raw:
        return []
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        return []
    hits = data.get("hits") or []
    items = []
    for h in hits:
        url = str(h.get("url") or "")
        if url.startswith("/"):
            url = W2C_BASE + url
        img = str(h.get("image") or "")
        items.append(
            {
                "title": str(h.get("title") or ""),
                "url": url,
                "image": img,
                "price_cny": h.get("price"),
                "category": str(h.get("category") or ""),
                "brand": str(h.get("brand") or ""),
            }
        )
    return items


def pick_english_post(posts: list[dict]) -> dict | None:
    for p in posts:
        title = unescape(str(p.get("title", {}).get("rendered", "")))
        if title and title.isascii() and "&#" not in title:
            return p
    return posts[0] if posts else None


def strip_html(html: str) -> str:
    text = re.sub(r"<script[^>]*>.*?</script>", " ", html, flags=re.S | re.I)
    text = re.sub(r"<style[^>]*>.*?</style>", " ", text, flags=re.S | re.I)
    text = re.sub(r"<[^>]+>", " ", text)
    return re.sub(r"\s+", " ", unescape(text)).strip()


def extract_images(html: str) -> list[str]:
    imgs = []
    for src in re.findall(r'src=["\']([^"\']+)["\']', html, re.I):
        if src.startswith("/"):
            src = "https://orientdig.com" + src
        if any(ext in src.lower() for ext in (".png", ".jpg", ".jpeg", ".webp", ".gif")):
            imgs.append(src)
    return imgs[:6]


def sanitize_help_html(html: str) -> str:
    html = re.sub(r"<script[^>]*>.*?</script>", "", html, flags=re.S | re.I)
    html = re.sub(r'src="/', 'src="https://orientdig.com/', html)
    html = re.sub(r"src='/", "src='https://orientdig.com/", html)
    html = re.sub(r'href="/', 'href="https://orientdig.com/', html)
    html = re.sub(r"href='/", "href='https://orientdig.com/", html)
    html = re.sub(
        r'src="(https://orientdig\.com/wp-content/[^"]+)"',
        lambda m: m.group(0),
        html,
    )
    return html


def fetch_help_topic(slugs: list[str]) -> list[dict]:
    articles = []
    seen = set()
    for slug in slugs:
        raw = http_get(f"{OD_HELP}?slug={urllib.parse.quote(slug)}")
        if not raw:
            continue
        try:
            posts = json.loads(raw)
        except json.JSONDecodeError:
            continue
        post = pick_english_post(posts if isinstance(posts, list) else [])
        if not post or post.get("id") in seen:
            continue
        seen.add(post.get("id"))
        content_html = post.get("content", {}).get("rendered", "")
        articles.append(
            {
                "slug": slug,
                "title": strip_html(post.get("title", {}).get("rendered", "")),
                "html": sanitize_help_html(content_html),
                "excerpt": strip_html(content_html)[:320],
                "images": extract_images(content_html),
                "source": f"https://orientdig.com/help-center-detail?slug={slug}",
            }
        )
    return articles


def build_cache() -> dict:
    return {
        "products": fetch_products(12, "newest"),
        "shipping_help": fetch_help_topic(SHIPPING_SLUGS),
        "coupon_help": fetch_help_topic(COUPON_SLUGS),
    }


def load_cache() -> dict:
    if CACHE_PATH.is_file():
        return json.loads(CACHE_PATH.read_text(encoding="utf-8"))
    return build_cache()


def refresh_cache() -> dict:
    data = build_cache()
    CACHE_PATH.parent.mkdir(parents=True, exist_ok=True)
    CACHE_PATH.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    return data


if __name__ == "__main__":
    data = refresh_cache()
    print(f"products: {len(data.get('products', []))}")
    print(f"shipping articles: {len(data.get('shipping_help', []))}")
    print(f"coupon articles: {len(data.get('coupon_help', []))}")
    print(f"written {CACHE_PATH}")
