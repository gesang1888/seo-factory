"""OrientDig-style home activity promo banners (coupon / guide / shipping)."""

from __future__ import annotations

from html import escape as esc

from scripts.i18n_ui import t as ui_t

# Local guide paths — coupons/shipping content stays on our SEO pages
PROMO_ITEMS = [
    {
        "id": "coupon",
        "image": "assets/images/promo-coupon.png",
        "slugs": {
            "en": "/orientdig-coupons/",
            "nl": "/orientdig-coupons/",
            "de": "/orientdig-coupons/",
            "it": "/orientdig-coupons/",
            "fr": "/orientdig-coupon/",
        },
        "title_key": "promo_coupon_title",
        "desc_key": "promo_coupon_desc",
    },
    {
        "id": "guide",
        "image": "assets/images/promo-guide.png",
        "slugs": {lang: "/how-to-use-orientdig/" for lang in ("en", "nl", "de", "it", "fr")},
        "title_key": "promo_guide_title",
        "desc_key": "promo_guide_desc",
    },
    {
        "id": "shipping",
        "image": "assets/images/promo-shipping.png",
        "slugs": {
            "en": "/orientdig-shipping/",
            "nl": "/orientdig-shipping/",
            "de": "/orientdig-shipping/",
            "it": "/orientdig-shipping/",
            "fr": "/livraison-orientdig/",
        },
        "region_slugs": {
            "US": "/orientdig-shipping-calculator/",
            "UK": "/how-long-does-orientdig-take-to-ship/",
        },
        "title_key": "promo_shipping_title",
        "desc_key": "promo_shipping_desc",
    },
]


def promo_href(item: dict, lang: str, region: str) -> str:
    region_map = item.get("region_slugs") or {}
    if region in region_map:
        return region_map[region]
    return item.get("slugs", {}).get(lang, item.get("slugs", {}).get("en", "/"))


def render_promo_banners(home_prefix: str, lang: str, region: str) -> str:
    lang_ui = lang if lang in ("nl", "de", "it", "fr") else "en"
    cards = []
    for item in PROMO_ITEMS:
        path = promo_href(item, lang_ui, region).lstrip("/")
        href = f"{home_prefix}{path}"
        img = f"{home_prefix}{item['image']}"
        title = ui_t(lang_ui, item["title_key"])
        desc = ui_t(lang_ui, item["desc_key"])
        cards.append(
            f"""<a class="od-promo-card od-promo-{item['id']}" href="{esc(href)}" aria-label="{esc(title)} — {esc(desc)}">
  <img src="{esc(img)}" alt="{esc(title)}" width="341" height="283" loading="lazy" decoding="async">
</a>"""
        )
    return f"""<section class="od-promo-strip">
  <div class="container">
    <h2 class="od-promo-heading">{esc(ui_t(lang_ui, "promo_heading"))}</h2>
    <div class="od-promo-grid">{''.join(cards)}</div>
  </div>
</section>"""
