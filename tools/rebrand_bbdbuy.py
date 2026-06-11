#!/usr/bin/env python3
"""One-shot rebrand script for cloned *_bbdbuy.py modules."""

from __future__ import annotations

import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]

PROTECT = [
    "orientdig.com/wp-json/wp/v2/help-center",
    "orientdig.com/register?ref=100246065",
    "orientdig.com/help-center",
    "orientdig.com",
    "w2clinks.com/public/typesense-search.php",
    "w2clinks.com",
    "service@orientdig.com",
    "wa.me/447856544534",
    "orientdig-theme.css",
    "orientdig-help.php",
    "orientdig-logo.png",
    "assets/images/orientdig-logo.png",
]


def rebrand(text: str) -> str:
    holders: dict[str, str] = {}
    for i, s in enumerate(PROTECT):
        key = f"__PROTECT_{i}__"
        holders[key] = s
        text = text.replace(s, key)
    text = text.replace("OrientDigSpreadsheetBuilder", "BBDBuySpreadsheetBuilder")
    text = text.replace("OrientDig", "BBDBuy")
    text = text.replace("orientdig", "bbdbuy")
    for key, s in holders.items():
        text = text.replace(key, s)
    return text


TARGETS = [
    "scripts/pages_bbdbuy.py",
    "scripts/trust_pages_bbdbuy.py",
    "scripts/i18n_ui_bbdbuy.py",
    "scripts/keyword_articles_bbdbuy.py",
    "scripts/deep_content_bbdbuy.py",
    "scripts/hub_sections_bbdbuy.py",
    "scripts/country_seo_bbdbuy.py",
    "scripts/promo_banners_bbdbuy.py",
    "scripts/reddit_insights_bbdbuy.py",
    "scripts/shipping_data_bbdbuy.py",
    "scripts/renderer_bbdbuy.py",
]


def main() -> None:
    for rel in TARGETS:
        p = ROOT / rel
        if not p.exists():
            print(f"skip (missing): {rel}")
            continue
        p.write_text(rebrand(p.read_text(encoding="utf-8")), encoding="utf-8")
        print("rebranded", rel)


if __name__ == "__main__":
    main()
