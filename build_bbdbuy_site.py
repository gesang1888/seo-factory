#!/usr/bin/env python3
"""Build BBDBuy cluster: bbdbuy.uk / bbdbuy.us / bbdbuy.ca / bbdbuy.it"""

from __future__ import annotations

import json
import shutil
import sys
from datetime import date
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from scripts.domains_bbdbuy import BBDBUY_DOMAINS, domain_slugs, slug_to_path  # noqa: E402
from scripts.fetch_live_data import refresh_cache  # noqa: E402
from scripts.pages_bbdbuy import get_page, page_allowed  # noqa: E402
from scripts.renderer_bbdbuy import (  # noqa: E402
    copy_assets,
    render_page,
    write_404_page,
)
from scripts.trust_pages_bbdbuy import TRUST_SLUGS, get_trust_page  # noqa: E402

DIST = ROOT / "dist"
TEMPLATE_ROOT = ROOT / "templates"
BBDBUY_CONFIG = ROOT / "site.bbdbuy.config.json"
TODAY = date.today().isoformat()


def load_bbdbuy_config() -> dict:
    return json.loads(BBDBUY_CONFIG.read_text(encoding="utf-8"))


def build_slug_index() -> dict[str, set[str]]:
    index: dict[str, set[str]] = {}
    for domain, meta in BBDBUY_DOMAINS.items():
        region = meta["region"]
        slugs = set()
        for slug in domain_slugs(region):
            page = get_page(slug)
            if page and page_allowed(page, region):
                slugs.add(slug)
        for trust_slug in TRUST_SLUGS:
            slugs.add(trust_slug)
        index[domain] = slugs
    return index


def write_sitemap(domain: str, slugs: set[str]) -> None:
    base = f"https://{domain}"
    urls = []
    for slug in sorted(slugs, key=lambda s: (s != "", s)):
        path = slug_to_path(slug)
        loc = f"{base}{path if path != '/' else '/'}"
        urls.append(
            f"  <url>\n    <loc>{escape(loc)}</loc>\n    <lastmod>{TODAY}</lastmod>\n  </url>"
        )
    xml = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "\n".join(urls)
        + "\n</urlset>\n"
    )
    (DIST / domain / "sitemap.xml").write_text(xml, encoding="utf-8")


def write_robots(domain: str) -> None:
    content = (
        "User-agent: *\nAllow: /\n\n"
        f"Sitemap: https://{domain}/sitemap.xml\n"
    )
    (DIST / domain / "robots.txt").write_text(content, encoding="utf-8")


def build_domain(
    domain: str,
    meta: dict,
    slug_index: dict[str, set[str]],
    live_cache: dict,
    site_config: dict,
) -> int:
    region = meta["region"]
    lang = meta["lang"]
    locale = meta["locale"]
    region_label = meta["region_label"]
    slugs = slug_index[domain]
    out_dir = DIST / domain
    if out_dir.exists():
        shutil.rmtree(out_dir)
    out_dir.mkdir(parents=True)
    copy_assets(out_dir, TEMPLATE_ROOT)
    count = 0

    for slug in domain_slugs(region):
        page = get_page(slug)
        if not page or not page_allowed(page, region):
            continue
        locale_content = page[lang]
        html = render_page(
            domain=domain,
            locale=locale,
            lang=lang,
            region=region,
            region_label=region_label,
            slug=slug,
            page_data=page,
            locale_content=locale_content,
            all_slugs=list(slugs),
            slug_exists=slug_index,
            live_cache=live_cache,
            site_config=site_config,
            depth=0 if not slug else 1,
        )
        if slug:
            page_dir = out_dir / slug
            page_dir.mkdir(parents=True, exist_ok=True)
            (page_dir / "index.html").write_text(html, encoding="utf-8")
        else:
            (out_dir / "index.html").write_text(html, encoding="utf-8")
        count += 1

    for trust_slug in TRUST_SLUGS:
        trust = get_trust_page(trust_slug, lang)
        if not trust:
            trust = get_trust_page(trust_slug, "en")
        if not trust:
            continue
        html = render_page(
            domain=domain,
            locale=locale,
            lang=lang,
            region=region,
            region_label=region_label,
            slug=trust_slug,
            page_data={"cta": trust["cta"], "cta_href": trust["cta_href"]},
            locale_content=trust,
            all_slugs=list(slugs),
            slug_exists=slug_index,
            live_cache=live_cache,
            site_config=site_config,
            depth=1,
        )
        page_dir = out_dir / trust_slug
        page_dir.mkdir(parents=True, exist_ok=True)
        (page_dir / "index.html").write_text(html, encoding="utf-8")
        count += 1

    (out_dir / "404.html").write_text(
        write_404_page(
            domain=domain,
            locale=locale,
            lang=lang,
            region=region,
            site_config=site_config,
            slug_index=slug_index,
            live_cache=live_cache,
        ),
        encoding="utf-8",
    )

    write_sitemap(domain, slugs)
    write_robots(domain)
    return count


def main() -> None:
    if not BBDBUY_CONFIG.is_file():
        print("Missing site.bbdbuy.config.json", file=sys.stderr)
        sys.exit(1)

    print("Fetching live W2CLinks products + OrientDig help data...")
    live_cache = refresh_cache()
    site_config = load_bbdbuy_config()
    slug_index = build_slug_index()
    total_pages = 0
    domain_stats: dict[str, int] = {}

    for domain, meta in BBDBUY_DOMAINS.items():
        n = build_domain(domain, meta, slug_index, live_cache, site_config)
        domain_stats[domain] = n
        total_pages += n
        print(f"  {domain}: {n} pages")

    manifest = {
        "built": TODAY,
        "cluster": "bbdbuy",
        "domains": list(BBDBUY_DOMAINS.keys()),
        "pages_per_domain": domain_stats,
        "total_pages": total_pages,
        "live_products": len(live_cache.get("products", [])),
    }
    (DIST / "build-bbdbuy-manifest.json").write_text(
        json.dumps(manifest, indent=2), encoding="utf-8"
    )

    print(f"\nBuilt {total_pages} pages across {len(BBDBUY_DOMAINS)} BBDBuy domains")
    print(f"Output: {DIST}")


if __name__ == "__main__":
    main()
