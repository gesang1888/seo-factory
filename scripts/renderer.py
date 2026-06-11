"""HTML renderer for OrientDig Spreadsheet static pages."""

from __future__ import annotations

import html
import json
from pathlib import Path

from scripts.deep_content import merge_deep_sections
from scripts.domains import CANONICAL_DOMAINS, slug_to_path
from scripts.domains_partner import HREFLANG_PARTNER, PARTNER_DOMAINS
from scripts.hub_icons import brand_flag_markup
from scripts.hub_sections import render_home_hub
from scripts.i18n_ui import t as ui_t
from scripts.keyword_articles import country_guide_html
from scripts.shipping_data import shipping_section_html
from scripts.link_helpers import (
    AGENT_PLATFORM,
    external_attrs,
    main_spreadsheet_url,
    whatsapp_number,
    whatsapp_url,
)
from scripts.promo_banners import render_promo_banners
from scripts.reddit_insights import pain_points_section

ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = ROOT / "site.config.json"
TEMPLATE_ROOT = ROOT / "templates"


def asset_query() -> str:
    """Cache-bust static assets when theme files change."""
    css = TEMPLATE_ROOT / "orientdig-theme.css"
    js = TEMPLATE_ROOT / "site.js"
    stamp = max(int(css.stat().st_mtime), int(js.stat().st_mtime))
    return f"?v={stamp}"

FAVICON = AGENT_PLATFORM["faviconUrl"]
LOGO_ASSET = AGENT_PLATFORM["logoAsset"]
PLATFORM = AGENT_PLATFORM["baseUrl"]
REGISTER_URL = AGENT_PLATFORM["registerUrl"]
SPREADSHEET = main_spreadsheet_url()
FOOTER_DISCLAIMER = (
    "OrientDig is the shopping agent brand referenced by this guide. "
    "Spreadsheet and product-find links are provided through W2CLinks."
)

WHATSAPP_FLOAT_SVG = (
    '<svg viewBox="0 0 24 24" width="28" height="28" aria-hidden="true" focusable="false">'
    '<path fill="currentColor" d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-'
    ".273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-"
    ".297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-"
    ".606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-"
    ".075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-"
    ".198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 "
    "2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 "
    "1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 "
    "7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 "
    "9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 "
    "9.825 0 012.893 6.994c-.003 5.45-4.435 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 "
    "0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 "
    '11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413z"/>'
    "</svg>"
)

PRODUCT_SLUGS = {
    "orientdig-spreadsheet",
    "orientdig-spreadsheets",
    "orientdig-finds",
    "spreadsheet-orientdig",
    "best-orientdig-spreadsheet",
    "orientdig-spreadsheet-2026",
}

SHIPPING_SLUGS = {
    "orientdig-shipping",
    "orientdig-shipping-calculator",
    "how-long-does-orientdig-take-to-ship",
    "livraison-orientdig",
    "orientdig-tracking",
}

COUPON_SLUGS = {
    "orientdig-coupons",
    "orientdig-coupon",
    "orientdig-coupon-code",
    "orientdig-codes",
    "orientdig-coupon-codes",
    "orientdig-shipping-coupons",
}

LOCALE_TO_DOMAIN = {
    "en-GB": "orientdigspreadsheet.uk",
    "en-US": "orientdigspreadsheet.us",
    "nl-NL": "orientdigspreadsheet.nl",
    "it-IT": "orientdigspreadsheet.it",
    "de-DE": "orientdigspreadsheet.de",
    "fr-FR": "orientdigspreadsheet.fr",
    "x-default": "orientdigspreadsheet.us",
}


def load_site_config() -> dict:
    if CONFIG_PATH.is_file():
        return json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
    return {}


def _ui_lang(lang: str) -> str:
    return lang if lang in ("nl", "de", "it", "fr", "es") else "en"


def esc(text: str) -> str:
    return html.escape(str(text), quote=True)


def render_hreflang(slug: str, slug_exists: dict[str, set[str]], domain: str = "") -> str:
    lines = []
    path = slug_to_path(slug)
    locale_map = HREFLANG_PARTNER if domain in PARTNER_DOMAINS else LOCALE_TO_DOMAIN
    for hreflang, target_domain in locale_map.items():
        target = target_domain.replace("https://", "")
        if slug not in slug_exists.get(target, set()):
            continue
        url = f"https://{target}{path if path != '/' else '/'}"
        lines.append(
            f'<link rel="alternate" hreflang="{esc(hreflang)}" href="{esc(url)}">'
        )
    return "\n".join(lines)


def json_ld_faq(faq_items: list[dict[str, str]]) -> str:
    if not faq_items:
        return ""
    data = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {
                "@type": "Question",
                "name": item["question"],
                "acceptedAnswer": {"@type": "Answer", "text": item["answer"]},
            }
            for item in faq_items
        ],
    }
    return json.dumps(data, ensure_ascii=False)


def json_ld_breadcrumb(domain: str, slug: str, h1: str) -> str:
    base = f"https://{domain}"
    items = [
        {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{base}/"},
    ]
    if slug:
        items.append(
            {
                "@type": "ListItem",
                "position": 2,
                "name": h1,
                "item": f"{base}/{slug}/",
            }
        )
    data = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": items,
    }
    return json.dumps(data, ensure_ascii=False)


def json_ld_organization(site_config: dict, domain: str, logo_url: str) -> str:
    contact = site_config.get("contact", {})
    data = {
        "@context": "https://schema.org",
        "@type": "Organization",
        "name": f"{site_config.get('brand', 'OrientDig')} Spreadsheet Guide",
        "url": f"https://{domain}/",
        "logo": logo_url,
        "contactPoint": {
            "@type": "ContactPoint",
            "contactType": "customer support",
            "telephone": whatsapp_number().replace(" ", ""),
            "availableLanguage": ["English", "German", "French", "Dutch", "Italian"],
        },
    }
    email = contact.get("email")
    if email:
        data["email"] = email
    return json.dumps(data, ensure_ascii=False)


def json_ld_webpage(title: str, description: str, canonical: str, site_config: dict) -> str:
    data = {
        "@context": "https://schema.org",
        "@type": "WebPage",
        "name": title,
        "description": description,
        "url": canonical,
        "publisher": {
            "@type": "Organization",
            "name": f"{site_config.get('brand', 'OrientDig')} Spreadsheet Guide",
        },
    }
    return json.dumps(data, ensure_ascii=False)


def trust_footer_links(home_prefix: str, lang: str) -> str:
    ui = _ui_lang(lang)
    items = [
        ("footer_about", "about/"),
        ("footer_contact", "contact/"),
        ("footer_privacy", "privacy-policy/"),
        ("footer_terms", "terms/"),
        ("footer_affiliate", "affiliate-disclosure/"),
        ("footer_partner", "partner-disclosure/"),
    ]
    lines = ""
    for key, path in items:
        lines += f'<p><a href="{home_prefix}{path}">{esc(ui_t(ui, key))}</a></p>'
    return lines


def header_actions(lang: str) -> str:
    ui = _ui_lang(lang)
    ext = external_attrs()
    return f"""<div class="header-actions">
  <a class="btn btn-ghost btn-sm" href="{esc(REGISTER_URL)}" {ext}>{esc(ui_t(ui, "nav_register"))}</a>
  <a class="btn btn-primary btn-sm" href="{esc(SPREADSHEET)}" {ext}>{esc(ui_t(ui, "nav_spreadsheet"))}</a>
</div>"""


def hero_block(
    *,
    h1: str,
    intro: str,
    cta: str,
    cta_href: str,
    lang: str,
    site_config: dict,
    is_home: bool,
) -> str:
    ui = _ui_lang(lang)
    ext = external_attrs()
    badge = esc(site_config.get("trustMessaging", {}).get("badge", "Independent Spreadsheet Guide"))
    platform_link = (
        f'<a href="{esc(REGISTER_URL)}" class="btn btn-secondary" {ext}>'
        f"{esc(ui_t(ui, 'nav_register'))}</a>"
    )
    side = ""
    if is_home:
        side = f"""<div class="card hub-side-card">
  <h2>{esc(ui_t(ui, "hero_side_title"))}</h2>
  <p>{esc(ui_t(ui, "hero_side_body"))}</p>
</div>"""
        inner = f"""<div class="hero-main">
  <span class="od-badge">{badge}</span>
  <h1>{esc(h1)}</h1>
  <p class="lead">{esc(intro)}</p>
  <p class="hero-ctas">
    <a href="{esc(cta_href)}" class="btn btn-primary" {ext}>{esc(cta)}</a>
    {platform_link}
  </p>
</div>{side}"""
        return f"""<section class="hero">
  <div class="container hero-grid">{inner}</div>
</section>"""
    return f"""<section class="hero">
  <div class="container">
    <span class="od-badge">{badge}</span>
    <h1>{esc(h1)}</h1>
    <p class="lead">{esc(intro)}</p>
    <p class="hero-ctas">
      <a href="{esc(cta_href)}" class="btn btn-primary" {ext}>{esc(cta)}</a>
      {platform_link}
    </p>
  </div>
</section>"""


def nav_links(slugs: list[str], current: str, home_prefix: str, lang: str) -> str:
    labels = {
        "": "Home",
        "orientdig-spreadsheet": "Spreadsheet",
        "orientdig-spreadsheets": "Spreadsheets",
        "orientdig-finds": "Finds",
        "orientdig-coupons": "Coupons",
        "is-orientdig-legit": "Legit?",
        "orientdig-shipping": "Shipping",
        "how-to-use-orientdig": "How To",
    }
    if lang == "es":
        labels.update(
            {
                "orientdig-spreadsheet": "Spreadsheet",
                "orientdig-coupons": "Cupones",
                "orientdig-shipping": "Envíos",
                "how-to-use-orientdig": "Guía",
            }
        )
    elif lang == "nl":
        labels.update(
            {
                "orientdig-spreadsheets": "Spreadsheets",
                "orientdig-coupons": "Coupons",
                "orientdig-shipping": "Verzending",
                "how-to-use-orientdig": "Handleiding",
            }
        )
    elif lang == "de":
        labels.update(
            {
                "orientdig-coupons": "Gutscheine",
                "orientdig-shipping": "Versand",
                "how-to-use-orientdig": "Anleitung",
            }
        )
    elif lang == "it":
        labels.update(
            {
                "orientdig-coupons": "Coupon",
                "orientdig-shipping": "Spedizione",
                "how-to-use-orientdig": "Guida",
            }
        )
    elif lang == "fr":
        labels.update(
            {
                "orientdig-coupons": "Coupons",
                "orientdig-shipping": "Livraison",
                "how-to-use-orientdig": "Guide",
            }
        )

    slug_set = set(slugs)
    sheet_slug = (
        "orientdig-spreadsheet"
        if "orientdig-spreadsheet" in slug_set
        else "orientdig-spreadsheets"
    )
    nav_order = [
        "",
        sheet_slug,
        "orientdig-finds",
        "orientdig-shipping",
        "orientdig-coupons",
        "how-to-use-orientdig",
        "is-orientdig-legit",
    ]

    parts = []
    for slug in nav_order:
        if slug not in slug_set or slug not in labels:
            continue
        href = f"{home_prefix}{slug}/" if slug else (home_prefix or "/")
        active = " active" if slug == current else ""
        parts.append(f'<a href="{href}" class="nav-link{active}">{esc(labels[slug])}</a>')
    return "".join(parts)


def lang_switcher(
    slug: str,
    current_domain: str,
    slug_exists: dict[str, set[str]],
    config: dict,
    ui_lang: str,
) -> str:
    path = slug_to_path(slug)
    options = []
    for entry in config.get("languages", []):
        code = entry.get("code", "")
        dom = entry.get("domain", "")
        if slug not in slug_exists.get(dom, set()):
            continue
        url = f"https://{dom}{path if path != '/' else '/'}"
        selected = " selected" if dom == current_domain else ""
        options.append(
            f'<option value="{esc(code)}" data-url="{esc(url)}"{selected}>{esc(entry.get("label", code))}</option>'
        )
    if not options:
        return ""
    return (
        f'<label class="header-select"><span>{esc(ui_t(ui_lang, "lang_label"))}</span> '
        f'<select id="od-lang-select" aria-label="Language">{"".join(options)}</select></label>'
    )


def currency_switcher(config: dict, default_code: str, ui_lang: str) -> str:
    opts = []
    for c in config.get("currencies", []):
        code = c.get("code", "")
        sym = c.get("symbol", code)
        sel = " selected" if code == default_code else ""
        opts.append(f'<option value="{esc(code)}"{sel}>{esc(sym)} {esc(code)}</option>')
    return (
        f'<label class="header-select"><span>{esc(ui_t(ui_lang, "currency_label"))}</span> '
        f'<select id="od-currency-select" aria-label="Currency">{"".join(opts)}</select></label>'
    )


def render_product_card(p: dict) -> str:
    url = str(p.get("url") or SPREADSHEET)
    if url.startswith("/"):
        url = "https://w2clinks.com" + url
    title = esc(p.get("title") or "Find")
    img = p.get("image") or ""
    thumb = (
        f'<img src="{esc(img)}" alt="{title}" loading="lazy" decoding="async">'
        if img
        else '<div class="od-no-img">Find</div>'
    )
    price = p.get("price_cny")
    price_html = (
        f'<span class="od-price" data-price-cny="{esc(price)}"></span>'
        if price is not None
        else ""
    )
    cat = esc(p.get("category") or "")
    return f"""<a class="od-product-card" href="{esc(url)}" target="_blank" rel="noopener">
  <div class="od-product-thumb">{thumb}</div>
  <div class="od-product-body"><h3>{title}</h3><p class="od-product-meta">{cat}</p>{price_html}</div>
</a>"""


def products_section(products: list[dict], lang: str) -> str:
    if not products:
        return ""
    cards = "".join(render_product_card(p) for p in products[:12])
    return f"""<div class="card" id="spreadsheet-products">
  <h2>{esc(ui_t(lang, "products_title"))}</h2>
  <p>{esc(ui_t(lang, "products_sub"))} <a href="{esc(SPREADSHEET)}" target="_blank" rel="noopener">{esc(ui_t(lang, "products_open"))}</a>.</p>
  <p class="od-live-meta"><span>{esc(ui_t(lang, "products_updated"))}</span></p>
  <div class="od-product-grid" id="od-product-grid">{cards}</div>
</div>"""


def render_help_article(a: dict) -> str:
    imgs = ""
    for src in (a.get("images") or [])[:2]:
        if not src.startswith("http"):
            src = "https://orientdig.com" + src if src.startswith("/") else src
        imgs += (
            f'<img src="{esc(src)}" alt="" loading="lazy" class="od-policy-img" '
            f'onerror="this.style.display=\'none\'">'
        )
    img_block = f'<div class="od-policy-imgs">{imgs}</div>' if imgs else ""
    return f"""<article class="od-policy-article">
  <h3>{esc(a.get("title") or "")}</h3>
  {img_block}
  <div class="od-policy-html">{a.get("html") or ""}</div>
  <p class="od-policy-src"><a href="{esc(a.get("source") or PLATFORM)}" target="_blank" rel="noopener">Read on OrientDig Help Center</a></p>
</article>"""


def live_help_section(articles: list[dict], topic: str, lang: str) -> str:
    title = ui_t(lang, "live_shipping_title" if topic == "shipping" else "live_coupon_title")
    body = "".join(render_help_article(a) for a in articles)
    return f"""<div class="card od-live-panel" id="od-live-help-wrap">
  <h2>{esc(title)}</h2>
  <div class="od-live-meta">
    <span>{esc(ui_t(lang, "live_source"))}</span>
    <span id="od-live-ts"></span>
    <button type="button" class="btn-ghost" id="od-refresh-help" data-topic="{esc(topic)}">{esc(ui_t(lang, "live_refresh"))}</button>
  </div>
  <div id="od-live-help" data-topic="{esc(topic)}">{body}</div>
</div>"""


def country_guide_section(region: str, lang: str, home_prefix: str = "") -> str:
    return country_guide_html(region, lang, home_prefix)


def site_config_script(config: dict, region: str) -> str:
    defaults = config.get("defaultCurrencyByRegion", {})
    payload = {
        "spreadsheetUrl": SPREADSHEET,
        "registerUrl": REGISTER_URL,
        "whatsappUrl": whatsapp_url(),
        "defaultCurrency": defaults.get(region, "USD"),
        "currencies": config.get("currencies", []),
    }
    return f"<script>window.OD_SITE_CONFIG={json.dumps(payload, ensure_ascii=False)};</script>"


def render_page(
    *,
    domain: str,
    locale: str,
    lang: str,
    region: str,
    region_label: str,
    slug: str,
    page_data: dict,
    locale_content: dict,
    all_slugs: list[str],
    slug_exists: dict[str, set[str]],
    live_cache: dict,
    site_config: dict,
    depth: int = 0,
) -> str:
    path = slug_to_path(slug)
    canonical = f"https://{domain}{path if path != '/' else '/'}"
    title = locale_content["title"]
    if region_label and lang == "en" and slug == "":
        title = title.replace("Guide:", f"{region_label} Guide:")

    desc = locale_content["description"]
    h1 = locale_content["h1"]
    intro = locale_content["intro"]
    sections = merge_deep_sections(
        slug, region, lang, locale_content.get("sections", [])
    )
    faq = locale_content.get("faq", [])
    cta = page_data["cta"]
    cta_href = page_data["cta_href"]

    home_prefix = "../" * depth if depth else ""
    asset_q = asset_query()
    css_href = f"{home_prefix}assets/css/orientdig-theme.css{asset_q}"
    js_href = f"{home_prefix}assets/js/site.js{asset_q}"

    hreflang_html = render_hreflang(slug, slug_exists, domain)
    faq_ld = json_ld_faq(faq)
    crumb_ld = json_ld_breadcrumb(domain, slug, h1)

    default_currency = site_config.get("defaultCurrencyByRegion", {}).get(region, "USD")
    lang_ui = _ui_lang(lang)

    section_html = ""
    for heading, body in sections:
        section_html += f"""
    <div class="card">
      <h2>{esc(heading)}</h2>
      <p>{body}</p>
    </div>"""

    extra_html = country_guide_section(region, lang, home_prefix)
    extra_html += pain_points_section(region, lang, slug, home_prefix)

    if slug in PRODUCT_SLUGS:
        extra_html += products_section(live_cache.get("products", []), lang_ui)

    if slug in SHIPPING_SLUGS:
        extra_html += live_help_section(live_cache.get("shipping_help", []), "shipping", lang_ui)
        extra_html += shipping_section_html(region, lang)
    elif slug in COUPON_SLUGS:
        extra_html += live_help_section(live_cache.get("coupon_help", []), "coupons", lang_ui)
    elif slug == "":
        products = live_cache.get("products", [])
        extra_html += render_home_hub(
            products=products,
            lang=lang_ui,
            region=region,
            home_prefix=home_prefix,
            site_config=site_config,
            domain=domain,
            default_currency=default_currency,
        )

    faq_html = ""
    for item in faq:
        faq_html += f"""
      <details>
        <summary>{esc(item['question'])}</summary>
        <p>{esc(item['answer'])}</p>
      </details>"""

    logo_href = f"{home_prefix}{LOGO_ASSET.lstrip('/')}"
    favicon_href = logo_href
    logo_abs = f"https://{domain}/{LOGO_ASSET.lstrip('/')}"
    org_ld = json_ld_organization(site_config, domain, logo_abs)
    page_ld = json_ld_webpage(title, desc, canonical, site_config)
    contact = site_config.get("contact", {})
    wa_display = esc(contact.get("whatsappDisplay", whatsapp_number()))
    footer_note = esc(
        site_config.get("trustMessaging", {}).get("footerNote", FOOTER_DISCLAIMER)
    )
    contact_note = esc(
        contact.get("siteNote") or ui_t(lang_ui, "contact_note")
    )
    ext = external_attrs()

    return f"""<!DOCTYPE html>
<html lang="{esc(locale)}" data-default-currency="{esc(default_currency)}">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{esc(canonical)}">
<meta name="robots" content="index, follow">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{esc(canonical)}">
<meta property="og:type" content="website">
<link rel="icon" href="{esc(favicon_href)}" type="image/png">
{hreflang_html}
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{css_href}">
{site_config_script(site_config, region)}
<script type="application/ld+json">{org_ld}</script>
<script type="application/ld+json">{page_ld}</script>
<script type="application/ld+json">{faq_ld}</script>
<script type="application/ld+json">{crumb_ld}</script>
</head>
<body>
<header class="site-header">
  <div class="container header-inner">
    <div class="header-top">
      <a href="{home_prefix or '/'}" class="brand">
        <span class="brand-mark">
          <img class="brand-logo" src="{esc(logo_href)}" width="160" height="36" alt="OrientDig">
          {brand_flag_markup(region)}
        </span>
      </a>
      <div class="header-end">
        <div class="header-tools">
          {lang_switcher(slug, domain, slug_exists, site_config, lang_ui)}
          {currency_switcher(site_config, default_currency, lang_ui)}
        </div>
        {header_actions(lang_ui)}
      </div>
    </div>
    <nav class="header-nav" aria-label="Main navigation">{nav_links(all_slugs, slug, home_prefix, lang_ui)}</nav>
  </div>
</header>
{hero_block(h1=h1, intro=intro, cta=cta, cta_href=cta_href, lang=lang_ui, site_config=site_config, is_home=(slug == ""))}
{render_promo_banners(home_prefix, lang, region)}
<main class="content">
  <div class="container">
    {extra_html}
    {section_html}
    <div class="card faq">
      <h2>{esc(ui_t(lang_ui, "faq"))}</h2>
      {faq_html}
    </div>
  </div>
</main>
<footer class="site-footer">
  <div class="container">
    <div class="footer-grid">
      <div>
        <strong>OrientDig Spreadsheet Guide</strong>
        <p>{contact_note}</p>
        <p>{wa_display}</p>
        <p>{esc(contact.get("w2cSupportNote", ""))}</p>
      </div>
      <div>
        <strong>Guides</strong>
        <p><a href="{home_prefix}orientdig-finds/">Finds</a></p>
        <p><a href="{home_prefix}orientdig-coupons/">Coupons</a></p>
        <p><a href="{home_prefix}is-orientdig-legit/">Legit?</a></p>
      </div>
      <div>
        <strong>{esc(ui_t(lang_ui, "footer_trust"))}</strong>
        {trust_footer_links(home_prefix, lang_ui)}
        <p><a href="{esc(SPREADSHEET)}" {ext}>W2CLinks Spreadsheet</a></p>
        <p><a href="{esc(REGISTER_URL)}" {ext}>OrientDig Register</a></p>
      </div>
    </div>
    <p class="footer-note">{footer_note}</p>
  </div>
</footer>
<a class="float-wa" href="{esc(whatsapp_url())}" {ext} aria-label="Contact on WhatsApp">{WHATSAPP_FLOAT_SVG}</a>
<script src="{js_href}" defer></script>
</body>
</html>
"""


def write_404_page(
    *,
    domain: str,
    locale: str,
    lang: str,
    region: str,
    site_config: dict,
    slug_index: dict[str, set[str]],
    live_cache: dict,
) -> str:
    ui = _ui_lang(lang)
    return render_page(
        domain=domain,
        locale=locale,
        lang=lang,
        region=region,
        region_label="",
        slug="__404__",
        page_data={"cta": "Open OrientDig Spreadsheet", "cta_href": SPREADSHEET},
        locale_content={
            "title": "404 — Page Not Found | OrientDig Spreadsheet Guide",
            "description": "Page not found. Open the W2CLinks spreadsheet or contact us on WhatsApp.",
            "h1": "Page not found",
            "intro": "Try the homepage, spreadsheet CTA, or WhatsApp for guide help.",
            "sections": [],
            "faq": [
                {
                    "question": "Where does the spreadsheet open?",
                    "answer": "Use Open Spreadsheet — it opens W2CLinks in a new tab.",
                },
                {
                    "question": "How can I contact support?",
                    "answer": f"Use WhatsApp at {whatsapp_number()}.",
                },
            ],
        },
        all_slugs=list(slug_index.get(domain, set())),
        slug_exists=slug_index,
        live_cache=live_cache,
        site_config=site_config,
        depth=0,
    )


def write_redirect_page(target: str) -> str:
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta http-equiv="refresh" content="0;url={esc(target)}">
<link rel="canonical" href="{esc(target)}">
<title>Redirecting…</title>
</head>
<body>
<p>Redirecting to <a href="{esc(target)}">{esc(target)}</a></p>
</body>
</html>
"""


def copy_assets(dist_domain_dir: Path, template_root: Path) -> None:
    css_dir = dist_domain_dir / "assets" / "css"
    js_dir = dist_domain_dir / "assets" / "js"
    api_dir = dist_domain_dir / "api"
    css_dir.mkdir(parents=True, exist_ok=True)
    js_dir.mkdir(parents=True, exist_ok=True)
    api_dir.mkdir(parents=True, exist_ok=True)
    (css_dir / "orientdig-theme.css").write_text(
        (template_root / "orientdig-theme.css").read_text(encoding="utf-8"),
        encoding="utf-8",
    )
    (js_dir / "site.js").write_text(
        (template_root / "site.js").read_text(encoding="utf-8"),
        encoding="utf-8",
    )
    for name in ("products.php", "orientdig-help.php"):
        src = template_root / "api" / name
        if src.is_file():
            (api_dir / name).write_text(src.read_text(encoding="utf-8"), encoding="utf-8")
    img_dir = dist_domain_dir / "assets" / "images"
    img_dir.mkdir(parents=True, exist_ok=True)
    src_img = template_root / "assets" / "images"
    if src_img.is_dir():
        for img in src_img.glob("*.png"):
            (img_dir / img.name).write_bytes(img.read_bytes())
