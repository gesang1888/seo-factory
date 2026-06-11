"""Render Reddit-derived pain-point blocks for SEO/GEO pages."""

from __future__ import annotations

import json
from html import escape as esc
from pathlib import Path

from scripts.i18n_ui_bbdbuy import t as ui_t

ROOT = Path(__file__).resolve().parents[1]
PAIN_JSON = ROOT / "data" / "reddit" / "bbdbuy_pain_points.json"

# Which themes matter most per region
REGION_THEMES: dict[str, list[str]] = {
    "UK": ["shipping_time", "trust_scam", "tracking", "coupons", "website_ux"],
    "US": ["shipping_time", "payment", "tracking", "agent_compare", "website_ux"],
    "NL": ["shipping_time", "trust_scam", "qc_photos", "coupons"],
    "DE": ["trust_scam", "agent_compare", "shipping_time", "payment"],
    "IT": ["shipping_time", "qc_photos", "coupons", "website_ux"],
    "FR": ["shipping_time", "trust_scam", "coupons", "agent_compare"],
    "ES": ["shipping_time", "website_ux", "coupons", "trust_scam"],
    "AT": ["trust_scam", "agent_compare", "shipping_time", "payment"],
}

REDDIT_SLUGS = {
    "bbdbuy-spreadsheet-reddit",
    "bbdbuy-reddit",
    "is-bbdbuy-legit",
    "is-bbdbuy-safe",
    "bbdbuy-shipping",
    "how-long-does-bbdbuy-take-to-ship",
    "bbdbuy-shipping-calculator",
    "livraison-bbdbuy",
    "bbdbuy-erfahrungen",
    "avis-bbdbuy",
    "bbdbuy-fiable",
}


def clean_snippet(text: str) -> str:
    import html as html_mod
    import re

    text = html_mod.unescape(text or "")
    text = re.sub(r"&#x200B;|\u200b", "", text, flags=re.I)
    text = re.sub(r"\|[^|\n]+\|", " ", text)
    text = re.sub(r"\*+", "", text)
    text = re.sub(r"https?://\S+", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text[:180]


def pick_thread(threads: list[dict]) -> dict | None:
    for thread in threads:
        snip = clean_snippet(thread.get("snippet") or thread.get("title") or "")
        if len(snip) < 20:
            continue
        if "trusted agents" in snip.lower() and "|" in (thread.get("snippet") or ""):
            continue
        thread = dict(thread)
        thread["snippet"] = snip
        return thread
    return threads[0] if threads else None


def load_pain_report() -> dict | None:
    if not PAIN_JSON.is_file():
        return None
    try:
        return json.loads(PAIN_JSON.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return None


def pain_points_section(region: str, lang: str, slug: str, home_prefix: str) -> str:
    if slug not in REDDIT_SLUGS:
        return ""
    report = load_pain_report()
    if not report:
        return ""

    lang_ui = lang if lang in ("nl", "de", "it", "fr") else "en"
    themes_wanted = REGION_THEMES.get(region, REGION_THEMES["US"])
    by_theme = {t["theme"]: t for t in report.get("themes", [])}

    items_html = ""
    for theme in themes_wanted:
        block = by_theme.get(theme)
        if not block:
            continue
        top = block.get("top_threads") or []
        thread = pick_thread(top)
        if not thread:
            continue
        angle = block.get("seo_angle", "")
        pages = block.get("suggested_pages") or []
        page_links = ""
        for p in pages[:2]:
            rel = p.strip("/") + "/"
            page_links += f'<a href="{esc(home_prefix + rel)}">{esc(rel.rstrip("/"))}</a> · '
        items_html += f"""<li class="od-pain-item">
  <strong>{esc(ui_t(lang_ui, f"pain_{theme}"))}</strong>
  <p>{esc(angle)}</p>
  <p class="od-pain-quote">“{esc(thread.get('snippet', ''))}” — r/{esc(thread.get('subreddit', ''))}</p>
  <p class="od-pain-links">{page_links.rstrip(' · ')}</p>
</li>"""

    if not items_html:
        return ""

    return f"""<div class="card od-pain-card">
  <h2>{esc(ui_t(lang_ui, "pain_heading"))}</h2>
  <p>{esc(ui_t(lang_ui, "pain_intro"))}</p>
  <ul class="od-pain-list">{items_html}</ul>
  <p class="od-muted"><small>{esc(ui_t(lang_ui, "pain_source"))}</small></p>
</div>"""
