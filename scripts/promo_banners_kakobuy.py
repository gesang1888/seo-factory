"""Kakobuy home promos: synced official activities + local guide cards (shipping, guide)."""

from __future__ import annotations

from html import escape as esc

from scripts.fetch_kakobuy_activities import load_activities
from scripts.i18n_ui_kakobuy import t as ui_t
from scripts.link_helpers_kakobuy import AGENT_PLATFORM

REGISTER = AGENT_PLATFORM["registerUrl"]

#图二/图三对换：Shipping 在前，Guide 在后（已删除原 1300CNY Coupon 图一）
LOCAL_GUIDE_ITEMS = [
    {
        "id": "shipping",
        "image": "assets/images/promo-shipping.png",
        "slugs": {
            "en": "/kakobuy-shipping/",
            "nl": "/kakobuy-shipping/",
            "fr": "/livraison-kakobuy/",
            "es": "/envio-kakobuy-espana/",
            "fi": "/kakobuy-toimitus/",
        },
        "region_slugs": {"CA": "/kakobuy-shipping-to-canada/"},
        "title_key": "promo_shipping_title",
        "desc_key": "promo_shipping_desc",
    },
    {
        "id": "guide",
        "image": "assets/images/promo-guide.png",
        "slugs": {lang: "/how-to-use-kakobuy/" for lang in ("en", "nl", "fr", "es", "fi")},
        "title_key": "promo_guide_title",
        "desc_key": "promo_guide_desc",
    },
]


def _lang_ui(lang: str) -> str:
    return lang if lang in ("nl", "fr", "es", "fi") else "en"


def promo_href(item: dict, lang: str, region: str) -> str:
    region_map = item.get("region_slugs") or {}
    if region in region_map:
        return region_map[region]
    return item.get("slugs", {}).get(lang, item.get("slugs", {}).get("en", "/"))


def render_top_promo_strip(lang: str) -> str:
    """Yellow strip synced with kakobuy.com new-user 3000 CNY message."""
    ui = _lang_ui(lang)
    text = ui_t(ui, "promo_strip_text")
    cta = ui_t(ui, "promo_strip_cta")
    return f"""<div class="kb-promo"><div class="container"><span>{esc(text)}</span> · <a href="{esc(REGISTER)}" target="_blank" rel="sponsored noopener">{esc(cta)}</a></div></div>"""


def render_official_activities(home_prefix: str, lang: str, region: str) -> str:
    """3 banners synced from kakobuy.com homepage carousel."""
    ui = _lang_ui(lang)
    cards = []
    for act in load_activities():
        if act.get("kind") == "notice" and region not in ("CA", "US"):
            continue
        title = act.get(f"title_{ui}") or act.get("title_en") or act.get("title_zh", "")
        href = act.get("url") or REGISTER
        if act.get("id") == "1":
            href = REGISTER
        img = act.get("image") or ""
        if not img:
            continue
        cards.append(
            f"""<a class="od-promo-card od-promo-official" href="{esc(href)}" target="_blank" rel="sponsored noopener" aria-label="{esc(title)}">
  <img src="{esc(img)}" alt="{esc(title)}" width="341" height="283" loading="lazy" decoding="async" referrerpolicy="no-referrer">
</a>"""
        )
    if not cards:
        return ""
    return f"""<section class="od-promo-strip od-promo-official-strip">
  <div class="container">
    <h2 class="od-promo-heading">{esc(ui_t(ui, "promo_official_heading"))}</h2>
    <div class="od-promo-grid od-promo-grid-official">{''.join(cards)}</div>
  </div>
</section>"""


def render_guide_cards(home_prefix: str, lang: str, region: str) -> str:
    ui = _lang_ui(lang)
    cards = []
    for item in LOCAL_GUIDE_ITEMS:
        path = promo_href(item, ui, region).lstrip("/")
        href = f"{home_prefix}{path}"
        img = f"{home_prefix}{item['image']}"
        title = ui_t(ui, item["title_key"])
        desc = ui_t(ui, item["desc_key"])
        cards.append(
            f"""<a class="od-promo-card od-promo-{item['id']}" href="{esc(href)}" aria-label="{esc(title)} — {esc(desc)}">
  <img src="{esc(img)}" alt="{esc(title)}" width="341" height="283" loading="lazy" decoding="async">
</a>"""
        )
    return f"""<section class="od-promo-strip">
  <div class="container">
    <h2 class="od-promo-heading">{esc(ui_t(ui, "promo_heading"))}</h2>
    <div class="od-promo-grid od-promo-grid-duo">{''.join(cards)}</div>
  </div>
</section>"""


def render_promo_banners(home_prefix: str, lang: str, region: str) -> str:
    return (
        render_top_promo_strip(lang)
        + render_official_activities(home_prefix, lang, region)
        + render_guide_cards(home_prefix, lang, region)
    )
