#!/usr/bin/env python3
"""Build the usfansspreadsheet.net SEO overlay.

Priority work this overlay ships:
1. Collapse satellite domains onto .net (301 + noindex stubs)
2. 301 thin brand/dupe spreadsheet URLs; shrink sitemap to keep URLs
3. Homepage is the live sheet, with product cards in HTML
4. sitemap lastmod = build date
5. Remove Official hub / fansbuy-hreflang-cluster
"""

from __future__ import annotations

import argparse
import html
import json
import re
import shutil
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.usfans_config import (  # noqa: E402
    CANONICAL_HOST,
    CANONICAL_ORIGIN,
    CNY_TO_USD,
    INDEPENDENT_BANNER,
    INDEPENDENT_FOOTER_BLURB,
    KEEP_PATHS,
    REGISTER_URL,
    SATELLITE_DOMAINS,
    hreflang_html,
    overlay_file_for_keep,
    overlay_file_for_redirect,
    path_variants,
    thin_redirects,
)

SITE_DIR = ROOT / "sites" / "usfansspreadsheet.net"
OVERLAY = SITE_DIR / "overlay"
SAT_DIR = SITE_DIR / "satellites"
TEMPLATE = ROOT / "templates" / "usfans" / "index.html"
CSS_SRC = ROOT / "templates" / "usfans" / "usfans-seo.css"
PRODUCTS_JSON = ROOT / "data" / "usfans" / "homepage-products.json"
KEEP_SNAPSHOT = Path("/tmp/usfans-keep")

HREFLANG_RE = re.compile(
    r"\s*<!--\s*fansbuy-hreflang-cluster\s*-->\s*(?:<link\s+rel=\"alternate\"[^>]*>\s*)+",
    re.I,
)
ALT_HREFLANG_RE = re.compile(r"\s*<link\s+rel=\"alternate\"\s+hreflang=\"[^\"]+\"[^>]*>\s*", re.I)
ORG_BANNER_RE = re.compile(
    r'<div class="org-banner"[^>]*>[\s\S]*?</div>\s*',
    re.I,
)
INDEPENDENT_BANNER_RE = re.compile(
    r'<div class="independent-banner"[^>]*>[\s\S]*?</div>\s*',
    re.I,
)


def esc(text: str) -> str:
    return html.escape(str(text), quote=True)


def load_products() -> tuple[int, list[dict]]:
    data = json.loads(PRODUCTS_JSON.read_text(encoding="utf-8"))
    items = data.get("items") or data.get("products") or []
    total = int(data.get("total") or len(items))
    return total, items


def usd_from_cny(price: str) -> str:
    try:
        n = float(re.sub(r"[^\d.]", "", str(price)))
    except ValueError:
        return ""
    if not n:
        return ""
    return f"≈ ${n * CNY_TO_USD:.2f}"


def abs_img(src: str) -> str:
    if not src:
        return ""
    if src.startswith("http"):
        return src
    return CANONICAL_ORIGIN + src


def render_product_grid(items: list[dict]) -> str:
    cards = []
    for item in items:
        title = esc(item.get("title") or "Find")
        href = esc(item.get("href") or item.get("target") or "/usfans-spreadsheet/")
        image = abs_img(item.get("image") or "")
        bg = (
            f"background:#f0f0ee center/cover url('{esc(image)}')"
            if image
            else "background:var(--bg-alt)"
        )
        price = item.get("price") or ""
        cny = f"¥{esc(price)}" if price else ""
        usd = usd_from_cny(str(price))
        usd_html = f" <small>{esc(usd)}</small>" if usd else ""
        cards.append(
            "    "
            f'<a href="{href}" target="_blank" rel="noopener" class="prod">'
            f'<div class="prod-img" style="{bg}"><span class="qc">📷 QC</span></div>'
            f'<div class="prod-body"><h4>{title}</h4>'
            f'<div class="price">{cny}{usd_html}</div></div></a>'
        )
    return "\n".join(cards)


def website_jsonld(item_count: int) -> str:
    return json.dumps(
        {
            "@context": "https://schema.org",
            "@type": "WebSite",
            "name": "USFans Spreadsheet",
            "url": f"{CANONICAL_ORIGIN}/",
            "description": (
                f"Independent USFans spreadsheet with {item_count}+ QC finds "
                "from Taobao, Weidian and 1688. Not affiliated with USFans.com."
            ),
            "potentialAction": {
                "@type": "SearchAction",
                "target": f"{CANONICAL_ORIGIN}/usfans-spreadsheet/?q={{search_term_string}}",
                "query-input": "required name=search_term_string",
            },
        },
        ensure_ascii=False,
        indent=2,
    )


def faq_jsonld() -> str:
    faqs = [
        (
            "Where is the USFans spreadsheet?",
            "The live sheet is https://usfansspreadsheet.net/usfans-spreadsheet/. This homepage is the hub; that search page is the catalog.",
        ),
        (
            "Is this the official USFans website?",
            "No. This is an independent fan-curated index. Orders, payments, warehouse QC and shipping happen on usfans.com.",
        ),
        (
            "Do I need to sign up to browse?",
            "No. Search and category pages are public. You only need a USFans account to place an order.",
        ),
        (
            "How long does USFans take to ship?",
            "Domestic seller-to-warehouse is often 2-5 days. International shipping is commonly 10-20 days for budget air. Confirm current lines at checkout.",
        ),
    ]
    return json.dumps(
        {
            "@context": "https://schema.org",
            "@type": "FAQPage",
            "mainEntity": [
                {
                    "@type": "Question",
                    "name": q,
                    "acceptedAnswer": {"@type": "Answer", "text": a},
                }
                for q, a in faqs
            ],
        },
        ensure_ascii=False,
        indent=2,
    )


def itemlist_jsonld(items: list[dict]) -> str:
    elements = []
    for i, item in enumerate(items, start=1):
        elements.append(
            {
                "@type": "ListItem",
                "position": i,
                "name": item.get("title") or "Find",
                "url": item.get("href") or item.get("target") or f"{CANONICAL_ORIGIN}/usfans-spreadsheet/",
            }
        )
    return json.dumps(
        {
            "@context": "https://schema.org",
            "@type": "ItemList",
            "name": "Latest USFans spreadsheet finds",
            "itemListElement": elements,
        },
        ensure_ascii=False,
        indent=2,
    )


def write_homepage(item_count: int, items: list[dict]) -> None:
    tpl = TEMPLATE.read_text(encoding="utf-8")
    html_out = (
        tpl.replace("{{HREFLANG}}", hreflang_html("/"))
        .replace("{{WEBSITE_JSONLD}}", website_jsonld(item_count))
        .replace("{{FAQ_JSONLD}}", faq_jsonld())
        .replace("{{ITEMLIST_JSONLD}}", itemlist_jsonld(items))
        .replace("{{INDEPENDENT_BANNER}}", INDEPENDENT_BANNER)
        .replace("{{INDEPENDENT_FOOTER}}", INDEPENDENT_FOOTER_BLURB)
        .replace("{{ITEM_COUNT}}", f"{item_count:,}")
        .replace("{{PRODUCT_GRID}}", render_product_grid(items))
        .replace("{{REGISTER_URL}}", REGISTER_URL)
    )
    (OVERLAY / "index.html").write_text(html_out, encoding="utf-8")


def write_sitemap(today: str) -> None:
    urls = []
    for path in KEEP_PATHS:
        loc = CANONICAL_ORIGIN + (path if path != "/" else "/")
        urls.append(
            "  <url>\n"
            f"    <loc>{html.escape(loc)}</loc>\n"
            f"    <lastmod>{today}</lastmod>\n"
            "    <changefreq>weekly</changefreq>\n"
            "  </url>"
        )
    xml = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "\n".join(urls)
        + "\n</urlset>\n"
    )
    (OVERLAY / "sitemap.xml").write_text(xml, encoding="utf-8")


def write_robots() -> None:
    (OVERLAY / "robots.txt").write_text(
        "User-agent: *\n"
        "Allow: /\n"
        "Disallow: /api/\n"
        "Disallow: /admin/\n"
        "Disallow: /.env\n"
        "Disallow: /.bak\n"
        "\n"
        "User-agent: SemrushBot\n"
        "Disallow: /\n"
        "\n"
        "User-agent: AhrefsBot\n"
        "Disallow: /\n"
        "\n"
        f"Sitemap: {CANONICAL_ORIGIN}/sitemap.xml\n",
        encoding="utf-8",
    )


def redirect_html(target: str) -> str:
    abs_target = target if target.startswith("http") else CANONICAL_ORIGIN + target
    return (
        "<!DOCTYPE html>\n<html lang=\"en\">\n<head>\n"
        "<meta charset=\"UTF-8\">\n"
        f'<meta http-equiv="refresh" content="0;url={esc(abs_target)}">\n'
        '<meta name="robots" content="noindex, follow">\n'
        f'<link rel="canonical" href="{esc(abs_target)}">\n'
        "<title>Redirecting…</title>\n"
        "</head>\n<body>\n"
        f'<p>This URL moved. Continue at <a href="{esc(abs_target)}">{esc(abs_target)}</a>.</p>\n'
        "</body>\n</html>\n"
    )


def write_thin_redirect_pages() -> None:
    for src, dest in thin_redirects().items():
        rel = overlay_file_for_redirect(src)
        path = OVERLAY / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(redirect_html(dest), encoding="utf-8")


def write_nginx() -> None:
    nginx_dir = OVERLAY / "nginx"
    nginx_dir.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Thin-page 301s for usfansspreadsheet.net — include inside the HTTPS server block.",
        "# include /www/server/nginx/conf/usfans-thin-redirects.conf;",
        "",
    ]
    for src, dest in sorted(thin_redirects().items()):
        abs_dest = dest if dest.startswith("http") else dest
        for variant in path_variants(src):
            if variant == "/":
                continue
            lines.append(f"location = {variant} {{")
            lines.append(f"    return 301 {abs_dest};")
            lines.append("}")
            lines.append("")
    (nginx_dir / "usfans-thin-redirects.conf").write_text("\n".join(lines), encoding="utf-8")

    sat_lines = [
        "# 301 every satellite host onto the canonical .net host, preserving path + query.",
        "",
    ]
    for domain in SATELLITE_DOMAINS:
        sat_lines.append("server {")
        sat_lines.append("    listen 80;")
        sat_lines.append("    listen 443 ssl;")
        sat_lines.append(f"    server_name {domain} www.{domain};")
        sat_lines.append(f"    return 301 {CANONICAL_ORIGIN}$request_uri;")
        sat_lines.append("}")
        sat_lines.append("")
    (nginx_dir / "usfans-satellite-301.conf").write_text("\n".join(sat_lines), encoding="utf-8")


def write_cloudflare() -> None:
    cf_dir = OVERLAY / "cloudflare"
    cf_dir.mkdir(parents=True, exist_ok=True)
    rows = ["source,destination,status,preserve_query"]
    for src, dest in sorted(thin_redirects().items()):
        abs_dest = dest if dest.startswith("http") else CANONICAL_ORIGIN + dest
        for variant in path_variants(src):
            rows.append(f"{CANONICAL_ORIGIN}{variant},{abs_dest},301,TRUE")
    (cf_dir / "thin-redirects.csv").write_text("\n".join(rows) + "\n", encoding="utf-8")

    hosts = []
    for domain in SATELLITE_DOMAINS:
        hosts.append(f'"{domain}"')
        hosts.append(f'"www.{domain}"')
    expression = (
        "http.host in {" + " ".join(hosts) + "}\n\n"
        "Then: Dynamic 301\n"
        f'concat("{CANONICAL_ORIGIN}", http.request.uri.path)\n'
        "Preserve query string: on\n"
    )
    (cf_dir / "satellite-dynamic-rule.txt").write_text(expression, encoding="utf-8")

    pages = []
    for src, dest in sorted(thin_redirects().items()):
        for variant in path_variants(src):
            pages.append(f"{variant} {dest} 301")
    (OVERLAY / "_redirects").write_text("\n".join(pages) + "\n", encoding="utf-8")


def write_redirect_manifest() -> None:
    payload = {
        "canonical": CANONICAL_ORIGIN,
        "satellites_301_to": CANONICAL_ORIGIN,
        "satellite_domains": SATELLITE_DOMAINS,
        "keep_paths": KEEP_PATHS,
        "thin_redirects": thin_redirects(),
        "keep_count": len(KEEP_PATHS),
        "thin_count": len(thin_redirects()),
    }
    (SITE_DIR / "redirect-map.json").write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def write_satellites() -> None:
    if SAT_DIR.exists():
        shutil.rmtree(SAT_DIR)
    for domain in SATELLITE_DOMAINS:
        d = SAT_DIR / domain
        d.mkdir(parents=True)
        target = CANONICAL_ORIGIN + "/"
        (d / "index.html").write_text(redirect_html(target), encoding="utf-8")
        (d / "robots.txt").write_text(
            "User-agent: *\nDisallow: /\n",
            encoding="utf-8",
        )
        (d / ".htaccess").write_text(
            f"RewriteEngine On\nRewriteRule ^(.*)$ {CANONICAL_ORIGIN}/$1 [R=301,L,QSA]\n",
            encoding="utf-8",
        )


def snapshot_path_to_file(path: str) -> Path | None:
    if path == "/":
        return None
    if path.endswith(".html"):
        candidate = KEEP_SNAPSHOT / path.lstrip("/")
        return candidate if candidate.is_file() else None
    slug = path.strip("/")
    for name in (f"{slug}.html", slug, f"{slug}/index.html"):
        candidate = KEEP_SNAPSHOT / name
        if candidate.is_file():
            return candidate
    # nested: es/como-comprar-usfans.html style from wget
    nested = KEEP_SNAPSHOT / f"{slug}.html"
    if nested.is_file():
        return nested
    return None


def inject_stylesheet(text: str) -> str:
    if "usfans-seo.css" in text:
        return text
    link = '<link rel="stylesheet" href="/usfans-seo.css">\n'
    if re.search(r'<link rel="stylesheet" href="[^"]*styles\.css[^"]*">', text):
        return re.sub(
            r'(<link rel="stylesheet" href="[^"]*styles\.css[^"]*">)',
            r"\1\n" + link,
            text,
            count=1,
        )
    return text.replace("</head>", link + "</head>", 1)


def inject_hreflang(text: str, path: str) -> str:
    text = HREFLANG_RE.sub("\n", text)
    # leftover alternate links that pointed at sibling ccTLDs
    def drop_cluster_alt(match: re.Match[str]) -> str:
        chunk = match.group(0)
        if "usfansspreadsheet.uk" in chunk or "usfansspreadsheet.nl" in chunk:
            return "\n"
        if "fansbuy" in chunk:
            return "\n"
        return chunk

    text = ALT_HREFLANG_RE.sub(drop_cluster_alt, text)
    block = hreflang_html(path) + "\n"
    if "usfans-hreflang: same-host language versions only" in text:
        return text
    return text.replace("</head>", block + "</head>", 1)


def inject_banner(text: str) -> str:
    text = ORG_BANNER_RE.sub("", text)
    text = INDEPENDENT_BANNER_RE.sub("", text)
    if re.search(r"<body[^>]*>", text):
        return re.sub(r"(<body[^>]*>)", r"\1\n" + INDEPENDENT_BANNER, text, count=1)
    return INDEPENDENT_BANNER + text


def patch_keep_html(text: str, path: str) -> str:
    text = inject_hreflang(text, path)
    text = inject_stylesheet(text)
    text = inject_banner(text)
    text = text.replace('href="index.html"', 'href="/"')
    text = re.sub(
        r'(<a href="/usfans-spreadsheet/" class="nav-cta"[^>]*>)[\s\S]*?</a>',
        r'\1Open spreadsheet</a>',
        text,
    )
    text = text.replace(
        'href="https://usfans.com/register?ref=7BJBAJ" class="nav-cta"',
        'href="/usfans-spreadsheet/" class="nav-cta"',
    )
    text = re.sub(
        r'<a href="/usfans-spreadsheet/" class="nav-cta"[^>]*>',
        '<a href="/usfans-spreadsheet/" class="nav-cta">',
        text,
    )
    text = re.sub(
        r'(class="nav-cta"[^>]*>)\s*Sign up — Save 15%\s*</a>',
        r"\1Open spreadsheet</a>",
        text,
    )
    text = text.replace(
        "The official-style USFans Spreadsheet hub — 8,000+ curated finds with QC photos and USD pricing. Updated weekly.",
        INDEPENDENT_FOOTER_BLURB,
    )
    text = text.replace("Official hub:", "Independent index:")
    text = text.replace("official-style USFans Spreadsheet hub", "independent USFans spreadsheet index")
    text = text.replace("Updated 9 August 2026", "Updated 21 September 2026")
    # search page still said 8,000+
    text = text.replace("8,000+", "10,000+")
    return text


def write_keep_pages() -> int:
    written = 0
    for path in KEEP_PATHS:
        if path == "/":
            continue
        src = snapshot_path_to_file(path)
        dest = OVERLAY / overlay_file_for_keep(path)
        dest.parent.mkdir(parents=True, exist_ok=True)
        if src and src.is_file():
            patched = patch_keep_html(src.read_text(encoding="utf-8", errors="replace"), path)
            dest.write_text(patched, encoding="utf-8")
            written += 1
        else:
            print(f"warn: no snapshot for {path}", file=sys.stderr)
    return written


def copy_css() -> None:
    shutil.copyfile(CSS_SRC, OVERLAY / "usfans-seo.css")


def self_check(item_count: int) -> None:
    home = (OVERLAY / "index.html").read_text(encoding="utf-8")
    sitemap = (OVERLAY / "sitemap.xml").read_text(encoding="utf-8")
    assert "Official hub" not in home
    assert "fansbuy-hreflang-cluster" not in home
    assert "usfansspreadsheet.uk" not in home
    assert 'class="prod"' in home
    assert "Loading trending finds" not in home
    assert "independent" in home.lower()
    assert f"{item_count:,}+" in home or str(item_count) in home
    loc_count = sitemap.count("<loc>")
    assert loc_count == len(KEEP_PATHS), (loc_count, len(KEEP_PATHS))
    today = date.today().isoformat()
    assert today in sitemap
    for path in KEEP_PATHS:
        if path == "/":
            continue
        sample = OVERLAY / overlay_file_for_keep(path)
        if sample.is_file():
            text = sample.read_text(encoding="utf-8", errors="replace")
            assert "fansbuy-hreflang-cluster" not in text, path
            assert "usfansspreadsheet.uk" not in text, path
            assert "Official hub" not in text, path
            assert 'class="nav-cta" target="_blank"' not in text, path
    thin = thin_redirects()
    for src in thin:
        html_path = OVERLAY / overlay_file_for_redirect(src)
        assert html_path.is_file(), src
        body = html_path.read_text(encoding="utf-8")
        assert "noindex" in body
        assert "canonical" in body
    print(
        f"check ok: homepage products={home.count('class=\"prod\"')} "
        f"sitemap={loc_count} thin={len(thin)} satellites={len(SATELLITE_DOMAINS)}"
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="rebuild then assert invariants")
    args = parser.parse_args()

    if OVERLAY.exists():
        shutil.rmtree(OVERLAY)
    OVERLAY.mkdir(parents=True)

    today = date.today().isoformat()
    item_count, items = load_products()
    write_homepage(item_count, items)
    write_sitemap(today)
    write_robots()
    copy_css()
    write_thin_redirect_pages()
    write_nginx()
    write_cloudflare()
    write_redirect_manifest()
    write_satellites()
    keep_n = write_keep_pages()
    self_check(item_count)
    print(
        f"Built overlay at {OVERLAY} | keep snapshots patched={keep_n} "
        f"| keep URLs={len(KEEP_PATHS)} | 301s={len(thin_redirects())} | lastmod={today}"
    )
    if args.check:
        return


if __name__ == "__main__":
    main()
