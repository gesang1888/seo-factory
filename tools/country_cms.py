#!/usr/bin/env python3
"""Editorial country-dest CMS template.

Gold IA: https://hipobuy.es/ (Start / Guide / Catalog / Shipping / Help / News;
About in the footer). Gold brand chrome: the agent's official site (logo, ico,
primary colour, login pill) — not leftover orange/Georgia.

How to fill the next dest
-------------------------
1. Copy tools/acbuy_nl_cms.py to tools/<agent>_<cc>_cms.py.
2. Instantate a new CountryDesk (host, agent, lang, official URLs, colours,
   nav labels, footer copy). Do not share one desk across two country TLDs.
3. Rewrite the Dutch copy builders. Keep the same page set:
   home / handleiding / catalogus / verzending / hulp / nieuws + about in footer.
4. Titles use page_title(desk, topic) — hipobuy.es homepage formula:
       "{agent} Spreadsheet {in_language}: {topic}"
   matching
       "Hipobuy Spreadsheet en español: comprar en China desde España con seguridad"
5. 404 title matches hipobuy.es: "{not_found_tab} | {agent} Spreadsheet".
6. Do not PUT a 5KB overlay over ranked unique inners — wrap chrome only.
7. Do not 301 two country dests of the same agent into each other.
8. FAQ lives on Help, not the homepage. No invite tokens on titles/home.
9. Category wall is the 33 w2clinks.com/categories/ icons, not a product grid.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from html import escape
from urllib.parse import quote_plus

from desk_template import inject_jsonld, organization_ld, skip_label, skip_link, webpage_ld
from dest_inner_chrome import (
    _body_scripts_outside_article,
    _element_inner,
    _head_inner,
    _html_tag,
    _text_len,
    after_footer_keep,
    extract_article,
)

W2C = "https://w2clinks.com"
# Same 33 icons / order as https://w2clinks.com/categories/
# Third field is the Dutch label used by the first pack; override per dest.
W2C_CATS = [
    ("SNEAKERS", "Turnschoenen", "cat-30-shoes.png?v=24"),
    ("SLIPPERS", "Slippers", "cat-27-slippers.png?v=24"),
    ("T-SHIRT", "T-shirt", "cat-03-t-shirt.png?v=24"),
    ("POLO", "Polo", "cat-04-polo.png?v=24"),
    ("SHIRT", "Overhemd", "cat-05-shirt.png?v=24"),
    ("SHORTS", "Shorts", "cat-07-shorts.png?v=24"),
    ("VEST", "Bodywarmer", "cat-20-vest.png?v=24"),
    ("LONG SLEEVED", "Lange mouw", "cat-25-long-sleeved.png?v=24"),
    ("HOODIE", "Hoodie", "cat-06-hoodie.png?v=24"),
    ("SWEATER", "Trui", "cat-11-sweater.png?v=24"),
    ("SHAWL", "Omslagdoek", "cat-12-shawl.png?v=24"),
    ("JACKET", "Jas", "cat-13-jacket.png?v=24"),
    ("SHELL JACKET", "Shelljas", "cat-18-jacket.png?v=24"),
    ("FLEECE JACKET", "Fleecejas", "cat-17-fleece-jacket.png?v=24"),
    ("DOWN JACKETS", "Donsjas", "cat-08-down-jackets.png?v=24"),
    ("TROUSERS", "Broek", "cat-19-trousers.png?v=24"),
    ("Jersey", "Shirt", "cat-jersey.png?v=24"),
    ("FEMALE STYLE", "Dames", "cat-28-femaie-styie.png?v=24"),
    ("Electronics", "Elektronica", "cat-electronics.png?v=24"),
    ("GLOVES", "Handschoenen", "cat-15-giove.png?v=24"),
    ("BAG", "Tas", "cat-00-bag.png?v=24"),
    ("HAT", "Pet", "cat-01-hat.png?v=24"),
    ("JEWELRY", "Sieraden", "cat-02-jewelry.png?v=24"),
    ("UNDERWEAR", "Ondergoed", "cat-09-underwear.png?v=24"),
    ("BELT", "Riem", "cat-10-belt.png?v=24"),
    ("KNEEPAD", "Kniebeschermer", "cat-16-kneepad.png?v=24"),
    ("SOCKS", "Sokken", "cat-26-socks.png?v=24"),
    ("HEADGEAR", "Hoofddeksel", "cat-22-headgear.png?v=24"),
    ("EARMUFF", "Oorwarmers", "cat-23-earmuff.png?v=24"),
    ("SCARF", "Sjaal", "cat-24-scarf.png?v=24"),
    ("GLASSES", "Bril", "cat-31-glasses.png?v=25"),
    ("WATCH", "Horloge", "cat-32-watch.png?v=26"),
    ("CHILD", "Kinderen", "cat-29-child.png?v=24"),
]


@dataclass
class CountryDesk:
    """One independent country dest. Sister TLDs stay separate files."""

    host: str
    agent: str
    dest: str
    dest_label: str
    lang: str
    in_language: str
    official: str
    estimator: str
    help_url: str
    mail: str
    acc: str
    acc_dark: str
    date: str
    css_v: str
    logo_src: str
    nav: list[tuple[str, str]]
    footer_intro: str
    footer_sections: list[tuple[str, str]]
    footer_official: list[tuple[str, str]]
    independence: str
    copyright: str
    login_label: str
    menu_label: str
    skip_lang: str
    not_found_h1: str
    not_found_lead: str
    home_cta: str
    theme_css: str
    desk_css: str
    inner_marker: str
    home_href: str = "/"
    reddit: str = ""
    register_path: str = "/register"
    brand_suffix: str = "Spreadsheet"
    sheet_slug: str = ""
    invites: tuple[str, ...] = ()
    factory_pats: tuple[str, ...] = ()
    extra_subs: tuple[tuple[str, str], ...] = ()
    strip_home_crumb: str = "Start"
    extra_official: list[tuple[str, str]] = field(default_factory=list)
    extra_css: str = ""
    sections_h: str = "Secties"
    official_h: str = "Officiële links"
    independence_h: str = "Onafhankelijkheidsverklaring."
    nav_aria: str = "Hoofdmenu"
    not_found_tab: str = "Pagina niet gevonden"
    chrome_style_id: str = "country-desk-chrome"


def page_title(desk: CountryDesk, topic: str) -> str:
    """hipobuy.es homepage formula: Brand Spreadsheet + language + topic."""
    return f"{desk.agent} Spreadsheet {desk.in_language}: {topic}"


def not_found_title(desk: CountryDesk) -> str:
    """hipobuy.es 404 formula: '{tab} | {agent} Spreadsheet'."""
    return f"{desk.not_found_tab} | {desk.agent} Spreadsheet"


def official_url(desk: CountryDesk, path: str = "") -> str:
    url = desk.official.rstrip("/") + path
    sep = "&" if "?" in url else "?"
    return f"{url}{sep}utm_source={desk.host}&utm_medium=referral&utm_campaign=portada"


def w2c_sheet(desk: CountryDesk) -> str:
    slug = desk.sheet_slug or desk.agent.lower()
    return f"{W2C}/spreadsheet/{slug}/"


def cats_for(labels: dict[str, str] | None = None) -> list[tuple[str, str, str]]:
    if not labels:
        return list(W2C_CATS)
    return [(key, labels.get(key, lab), fn) for key, lab, fn in W2C_CATS]


def cat_cards(
    cats: list[tuple[str, str, str]],
    href_fn,
    notes: dict[str, str] | None = None,
) -> str:
    bits = []
    for key, labn, fn in cats:
        note = ""
        if notes and key in notes:
            note = f"<em>{escape(notes[key])}</em>"
        bits.append(
            f'<a class="cat" href="{escape(href_fn(key))}" rel="noopener" target="_blank">'
            f'<img src="{escape(W2C)}/public/static/w2c/categories/{escape(fn)}" alt="{escape(key)}" '
            f'loading="lazy" decoding="async" width="96" height="96">'
            f'<div class="cat__b"><strong>{escape(labn)}</strong><span>{escape(key)}</span>'
            f"{note}</div></a>"
        )
    return "".join(bits)


def sheet_href(desk: CountryDesk, category: str) -> str:
    return f"{w2c_sheet(desk)}?category={quote_plus(category)}&page=1&sort=newest"


def chrome_lock(desk: CountryDesk) -> str:
    acc, acd = desk.acc, desk.acc_dark
    return (
        f":root{{--acc:{acc}!important;--acd:{acd}!important;--link:{acd}!important;"
        f"--primary:{acc}!important;--primary-dark:{acd}!important;--primary-soft:#e8f7f2!important}}"
        "#lang-modal,#lang-backdrop,.lmo,.lbk,.bc,.waf,.wabu,.wafb{display:none!important}"
        "header.top .nav a{color:#333!important}"
        f"header.top .nav a[aria-current],header.top .nav a:hover{{color:{acc}!important;background:transparent!important}}"
        f"header.top .hdr-login{{background:{acc}!important;color:#fff!important}}"
        f"header.top .hdr-login:hover{{background:{acd}!important;color:#fff!important}}"
    )


def render_css(desk: CountryDesk) -> str:
    acc, acd, v = desk.acc, desk.acc_dark, desk.css_v
    extra = desk.extra_css.strip()
    extra_block = f"\n{extra}\n" if extra else ""
    return f"""
:root{{
  --acc:{acc};--acd:{acd};--link:{acd};
  --ink:#303133;--ink2:#495068;--mute:#8492b2;--dark:#181818;
  --panel:#f5f6f7;--line:#eaecf0;--soft:#f5f6f7;
  --r:18px;--rs:12px;--maxw:1120px;--medida:34em;
  --f:"Microsoft Yahei","PingFang SC",Avenir,"Segoe UI","Hiragino Sans GB",sans-serif;--m:ui-monospace,monospace;
}}
*{{box-sizing:border-box}}
html{{-webkit-text-size-adjust:100%;color-scheme:light;scroll-behavior:smooth}}
body{{margin:0;font-family:var(--f);font-size:17px;line-height:1.72;color:var(--ink);background:#fff}}
img{{max-width:100%;height:auto;display:block}}
a{{color:var(--link)}}
a:hover{{color:var(--acd)}}
#main,[id]{{scroll-margin-top:76px}}
h1,h2,h3{{color:var(--dark);line-height:1.25;letter-spacing:-.01em;margin:0 0 .5em}}
h1{{font-size:clamp(30px,4.4vw,45px);font-weight:800}}
h2{{font-size:clamp(24px,3vw,32px);font-weight:800}}
h3{{font-size:20px;font-weight:700}}
p{{margin:0 0 1.05em}}
main p,main li,.sg-faq p{{max-width:var(--medida)}}
.wrap{{max-width:var(--maxw);margin:0 auto;padding:0 22px}}
.skip{{position:absolute;left:-9999px}}
.skip:focus{{left:12px;top:12px;z-index:99;background:#fff;padding:8px 18px;border-radius:var(--rs)}}
.top{{position:sticky;top:0;z-index:40;background:#fff;border-bottom:1px solid var(--line)}}
.top .wrap{{display:flex;align-items:center;gap:16px;min-height:72px}}
.brand{{display:flex;align-items:center;gap:8px;min-height:44px;font-weight:700;color:var(--dark);text-decoration:none;font-size:15px;white-space:nowrap}}
.brand img{{height:32px;width:auto}}
.brand span{{color:#8492b2;font-weight:600}}
.nav{{margin-left:auto;display:flex;gap:2px;flex-wrap:nowrap}}
.nav a{{display:inline-flex;align-items:center;min-height:44px;padding:0 12px;border-radius:var(--rs);color:#333;text-decoration:none;font-size:15px;white-space:nowrap}}
.nav a:hover,.nav a[aria-current]{{color:var(--acc);background:transparent;font-weight:700}}
.hdr-login{{display:inline-flex;align-items:center;min-height:36px;padding:0 16px;border-radius:999px;background:var(--acc);color:#fff;font-size:14px;font-weight:700;text-decoration:none;white-space:nowrap}}
.hdr-login:hover{{background:var(--acd);color:#fff}}
.burger{{display:none;margin-left:auto;min-width:44px;min-height:44px;border:1px solid var(--line);background:#fff;border-radius:var(--rs);font-size:19px;cursor:pointer}}
.hero{{position:relative;background:#181818;overflow:hidden}}
.hero__bg{{position:absolute;inset:0;background:url(/img/hero.jpg?v={v}) center/cover no-repeat}}
.hero__scrim{{position:absolute;inset:0;background:linear-gradient(100deg,rgba(24,24,24,.58) 0%,color-mix(in srgb, var(--acc) 22%, transparent) 100%)}}
.hero .wrap{{position:relative;padding:74px 22px 78px}}
.eyebrow{{display:inline-block;font-size:12.5px;letter-spacing:.13em;text-transform:uppercase;font-weight:700;color:var(--acc);margin-bottom:14px}}
.hero .eyebrow{{color:#9ee8d2}}
.hero h1{{color:#fff;max-width:15.5em}}
.hero p.lead{{color:#e7f7f1;font-size:19px;max-width:34em}}
.sbox{{margin-top:26px;max-width:660px}}
.sbox form{{display:flex;gap:9px;background:#fff;border-radius:999px;padding:8px 8px 8px 18px;box-shadow:0 14px 40px rgba(24,24,24,.22)}}
.sbox input{{flex:1;min-width:0;border:0;font:inherit;font-size:17px;padding:12px 8px}}
.sbox button{{min-height:44px;padding:0 24px;border:0;border-radius:999px;background:var(--acc);color:#fff;font:inherit;font-weight:700;cursor:pointer}}
.chips{{display:flex;flex-wrap:wrap;gap:8px;margin-top:12px}}
.chips a{{display:inline-flex;align-items:center;min-height:38px;padding:0 13px;border-radius:999px;background:rgba(255,255,255,.12);border:1px solid rgba(255,255,255,.26);color:#fff8f0;text-decoration:none;font-size:14px}}
.sec{{padding:62px 0;border-top:1px solid var(--line)}}
.sec--tint{{background:linear-gradient(var(--soft) 0%,#fff 100%);border-top:0}}
.sec--first{{border-top:0}}
.split{{display:grid;grid-template-columns:1.04fr .96fr;gap:46px;align-items:center}}
.split--rev .fig{{order:-1}}
.fig{{margin:0}}
.fig img{{border-radius:var(--r);border:1px solid var(--line);background:#fff}}
.fig figcaption{{margin-top:11px;font-size:13.5px;line-height:1.55;color:var(--mute)}}
.lead{{font-size:18px;color:var(--ink2);max-width:var(--medida)}}
.btn{{display:inline-flex;align-items:center;min-height:44px;padding:0 18px;border-radius:999px;background:var(--acc);color:#fff;font-weight:700;text-decoration:none}}
.btn:hover{{background:var(--acd);color:#fff}}
.btn--ghost{{background:#fff;color:var(--acd);border:1px solid var(--line)}}
.tl{{list-style:none;margin:0;padding:0 0 0 30px;border-left:2px solid var(--line)}}
.tl li{{position:relative;padding:0 0 18px 8px}}
.tl li:last-child{{padding-bottom:0}}
.tl li::before{{content:"";position:absolute;left:-39px;top:9px;width:14px;height:14px;border-radius:50%;background:var(--acc);box-shadow:0 0 0 4px #fff}}
.tl b{{display:block;color:var(--dark);font-size:17px}}
.tl span{{color:var(--mute);font-size:14px}}
.cat-grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(128px,1fr));gap:12px;margin-top:8px}}
.cat{{display:flex;flex-direction:column;align-items:center;text-align:center;background:#fff;border:1px solid var(--line);border-radius:var(--r);padding:16px 10px 14px;text-decoration:none;color:inherit}}
.cat:hover{{transform:translateY(-3px);box-shadow:0 12px 28px color-mix(in srgb, var(--acc) 22%, transparent);border-color:color-mix(in srgb, var(--acc) 45%, #fff)}}
.cat img{{width:72px;height:72px;object-fit:contain;padding:0;background:#fff}}
.cat__b{{padding:10px 0 0}}
.cat em{{display:block;margin-top:8px;font-style:normal;font-size:13px;line-height:1.45;color:var(--mute);font-weight:400}}
.cat-grid--rich{{grid-template-columns:repeat(auto-fill,minmax(200px,1fr))}}
.cat-grid--rich .cat{{align-items:flex-start;text-align:left;padding:14px}}
.eq{{width:100%;border-collapse:collapse;max-width:36em;font-size:15px}}
.eq th,.eq td{{border-bottom:1px solid var(--line);padding:8px 10px;text-align:left}}
.eq th{{color:#8492b2;font-weight:600}}
.cat__b strong{{display:block;color:var(--dark);font-size:14.5px}}
.cat__b span{{font-size:12px;color:var(--mute);letter-spacing:.04em}}
.states{{margin:0;padding:0;list-style:none}}
.states li{{padding:10px 0;border-bottom:1px solid var(--line);max-width:40em}}
.states code{{font-family:var(--m);font-size:13px}}
.sg-faq{{border:1px solid var(--line);border-radius:10px;padding:12px 14px;margin:8px 0;background:#fff;max-width:40em}}
.sg-faq summary{{cursor:pointer;font-weight:700}}
.ncard{{border:1px solid var(--line);border-radius:var(--r);padding:22px 22px 8px;margin-bottom:18px;max-width:40em}}
.ncard h2{{font-size:22px}}
.list{{margin:0 0 1.4em;padding:0 0 0 1.15em;max-width:var(--medida)}}
.list li{{margin:0 0 .45em}}
.site-ft{{background:#111;color:#ccc;padding:52px 0 30px;margin-top:24px;font-size:15.5px}}
.ft-grid{{display:grid;grid-template-columns:1.5fr 1fr 1fr;gap:34px}}
.site-ft h3{{color:#fff;font-size:15.5px;margin:0 0 12px;letter-spacing:.02em;font-weight:700}}
.site-ft p{{margin:0 0 12px;max-width:36em}}
.site-ft a{{color:#c2c2c2;text-decoration:none}}
.site-ft a:hover{{color:#fff;text-decoration:underline}}
.site-ft ul{{list-style:none;margin:0;padding:0}}
.site-ft li{{margin-bottom:8px}}
.site-ft .legal{{grid-column:1/-1;border-top:1px solid #2D2D2D;padding-top:20px;font-size:13.5px;color:#8a8a8a}}
.site-ft .legal p{{margin:0 0 8px;max-width:none}}
.pw{{max-width:40em;margin:0 auto;padding:40px 22px 64px}}
.inner-article{{max-width:860px;margin:0 auto;padding:28px 24px 48px}}
#lang-modal,#lang-backdrop,.lmo,.lbk,.bc,.waf,.wabu,.wafb{{display:none!important}}
@media(max-width:1000px){{
  .split{{grid-template-columns:1fr;gap:30px}}
  .split--rev .fig{{order:0}}
  .ft-grid{{grid-template-columns:1fr 1fr}}
}}
@media(max-width:860px){{
  .burger{{display:inline-flex;align-items:center;justify-content:center}}
  .nav{{display:none;position:absolute;left:0;right:0;top:64px;background:#fff;border-bottom:1px solid var(--line);flex-direction:column;padding:8px 12px}}
  .nav.open{{display:flex}}
  .hdr-login{{display:none}}
  .ft-grid{{grid-template-columns:1fr}}
}}
@media(max-width:640px){{
  .cat-grid{{grid-template-columns:repeat(2,1fr)}}
  .sbox form{{flex-direction:column}}
  .sbox button{{width:100%}}
}}
{extra_block}"""


def _is_home_page(desk: CountryDesk, page: str) -> bool:
    p = (page or "").rstrip("/") or "/"
    h = (desk.home_href or "/").rstrip("/") or "/"
    return p in {"/", h}


def nav_html(desk: CountryDesk, page: str) -> str:
    bits = []
    for href, lab in desk.nav:
        on = href == page or (href == desk.home_href and _is_home_page(desk, page))
        cur = ' aria-current="page"' if on else ""
        bits.append(f'<a href="{escape(href)}"{cur}>{escape(lab)}</a>')
    return "".join(bits)


def header(desk: CountryDesk, page: str) -> str:
    return f"""{skip_link(skip_label(desk.skip_lang))}<header class="top" role="banner">
  <div class="wrap">
    <a href="{escape(desk.home_href)}" class="brand">
      <img src="{escape(desk.logo_src)}" alt="{escape(desk.agent)}" width="118" height="39">
      <span>{escape(desk.brand_suffix)}</span>
    </a>
    <button class="burger" type="button" aria-expanded="false" aria-label="{escape(desk.menu_label)}">&#9776;</button>
    <nav class="nav" aria-label="{escape(desk.nav_aria)}">{nav_html(desk, page)}</nav>
    <a class="hdr-login" href="{escape(official_url(desk, desk.register_path))}" rel="nofollow noopener" target="_blank">{escape(desk.login_label)}</a>
  </div>
</header>
"""


def footer(desk: CountryDesk) -> str:
    sec = "".join(
        f'<li><a href="{escape(href)}">{escape(lab)}</a></li>' for href, lab in desk.footer_sections
    )
    off = "".join(
        f'<li><a href="{escape(url)}" rel="nofollow noopener" target="_blank">{escape(lab)}</a></li>'
        for url, lab in desk.footer_official
    )
    return f"""<footer class="site-ft">
  <div class="wrap ft-grid">
    <div>
      <h3>{escape(desk.agent)} Spreadsheet</h3>
      <p>{desk.footer_intro}</p>
      <p><a href="mailto:{escape(desk.mail)}">{escape(desk.mail)}</a></p>
    </div>
    <div>
      <h3>{escape(desk.sections_h)}</h3>
      <ul>{sec}</ul>
    </div>
    <div>
      <h3>{escape(desk.official_h)}</h3>
      <ul>{off}</ul>
    </div>
    <div class="legal">
      <p><strong>{escape(desk.independence_h)}</strong> {desk.independence}</p>
      <p>{desk.copyright}</p>
    </div>
  </div>
</footer>
<script>
(function(){{
  var b=document.querySelector('.burger'), n=document.querySelector('nav.nav');
  if(!b||!n) return;
  b.addEventListener('click', function(){{
    var on=b.getAttribute('aria-expanded')==='true';
    b.setAttribute('aria-expanded', on?'false':'true');
    n.classList.toggle('open', !on);
  }});
}})();
</script>
"""


def shell(
    desk: CountryDesk,
    title: str,
    desc: str,
    canonical: str,
    extra_ld: list[dict],
    body: str,
    page: str,
    extra_head: str = "",
) -> str:
    css = render_css(desk)
    lock = chrome_lock(desk)
    ld = [
        webpage_ld(
            url=canonical,
            name=title,
            desc=desc,
            lang=desk.lang,
            brand=desk.agent,
            host=desk.host,
        ),
        organization_ld(
            name=f"{desk.host} independent desk",
            url=f"https://{desk.host}/",
            email=desk.mail,
            lang=desk.lang,
            desc=desc,
        ),
    ] + extra_ld
    html = f"""<!DOCTYPE html>
<html lang="{escape(desk.lang)}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{escape(title)}</title>
<meta name="description" content="{escape(desc)}">
<link rel="canonical" href="{escape(canonical)}">
<link rel="icon" href="/favicon1.ico">
<link rel="icon" href="/favicon.ico" sizes="32x32">
<link rel="stylesheet" href="/assets/css/{escape(desk.theme_css)}?v={escape(desk.css_v)}">
<link rel="stylesheet" href="/assets/css/{escape(desk.desk_css)}?v={escape(desk.css_v)}">
<style>{css}\n{lock}</style>
{extra_head}
</head>
<body>
{header(desk, page)}
<main id="main">
{body}
</main>
{footer(desk)}
</body>
</html>
"""
    return inject_jsonld(html, *ld)


def build_404(desk: CountryDesk) -> str:
    items = "".join(
        f'<li><a href="{escape(href)}">{escape(lab)}</a></li>' for href, lab in desk.footer_sections
        if href.rstrip("/") not in {"", "/over-ons", "/sobre-nosotros"}
    )
    body = f"""
<section class="sec sec--first">
  <div class="wrap">
    <h1>{escape(desk.not_found_h1)}</h1>
    <p class="lead">{escape(desk.not_found_lead)}</p>
    <ul class="list">{items}</ul>
    <p><a class="btn" href="{escape(desk.home_href)}">{escape(desk.home_cta)}</a></p>
  </div>
</section>
"""
    return shell(
        desk,
        not_found_title(desk),
        desk.not_found_lead,
        f"https://{desk.host}/404.html",
        [],
        body,
        desk.home_href,
        extra_head='<meta name="robots" content="noindex, nofollow">',
    )


def fig(src: str, alt: str, cap: str, w: int = 1200, h: int = 750) -> str:
    return (
        f'<figure class="fig"><img src="{escape(src)}" alt="{escape(alt)}" '
        f'loading="lazy" width="{w}" height="{h}">'
        f"<figcaption>{escape(cap)}</figcaption></figure>"
    )


def _clean_article(html: str) -> str | None:
    article = extract_article(html)
    if not article:
        return None
    wrapped = "<body>" + article + "</body>"
    while True:
        block = _element_inner(wrapped, "main")
        if not block:
            break
        inner, _s, _e = block
        if _text_len(inner) < max(120, int(_text_len(article) * 0.75)):
            break
        article = inner.strip()
        wrapped = "<body>" + article + "</body>"
    return article


def _strip_id_block(html: str, eid: str) -> str:
    m = re.search(rf"<(div|section|aside)\b[^>]*\bid=\"{re.escape(eid)}\"[^>]*>", html, re.I)
    if not m:
        return html
    block = _element_inner(html, m.group(1), m.start())
    if not block:
        return html
    return html[: block[1]] + html[block[2] :]


def strip_factory_chrome(article: str, desk: CountryDesk) -> str:
    out = _strip_id_block(article, "lang-modal")
    out = _strip_id_block(out, "lang-backdrop")
    out = re.sub(r'<div class="bc">[\s\S]*?</div>', " ", out, count=1, flags=re.I)
    pats = desk.factory_pats + (
        r"To add full content[\s\S]{0,120}README\.md\.?",
        r"Takes 10 minutes to learn\.",
        r"Language\s*&(?:amp;)?\s*Currency[\s\S]{0,400}?Confirm",
        r"LANGUAGE\s+CURRENCY",
        r"expand this stub[\s\S]{0,80}",
    )
    for pat in pats:
        out = re.sub(pat, " ", out, flags=re.I)
    for pat, repl in desk.extra_subs:
        out = re.sub(pat, repl, out, count=1)
    out = re.sub(r"(?is)<p\b[^>]*>\s*(?:<br\s*/?>|\s|&nbsp;)*p>\s*", " ", out)
    out = re.sub(r'(?is)<a href="/acbuy-spreadsheet/"[^>]*>\s*</a>', " ", out)
    out = out.replace("background:#fff8f0;border:1px solid #ffd8b0", "background:#e8f7f2;border:1px solid #9ee8d2")
    out = out.replace("color:#b35b00", f"color:{desk.acc_dark}")
    out = out.replace("background:#f7fbff;border:1px solid #c9dff5", "background:#f5f6f7;border:1px solid #eaecf0")
    out = out.replace("color:#0b5cab", f"color:{desk.acc_dark}")
    out = re.sub(r">Home</a>", f">{escape(desk.strip_home_crumb)}</a>", out, count=1, flags=re.I)
    return re.sub(r"\n{3,}", "\n\n", out)


def _html_lang_tag(html: str, lang: str) -> str:
    tag = _html_tag(html)
    if re.search(r"\blang=", tag, re.I):
        tag = re.sub(r'\blang="[^"]*"', f'lang="{lang}"', tag, count=1)
    else:
        tag = re.sub(r"<html\b", f'<html lang="{lang}"', tag, count=1, flags=re.I)
    return tag


def wrap_inner(desk: CountryDesk, html: str, page_href: str) -> tuple[str | None, str]:
    article = _clean_article(html)
    if not article:
        return None, "no-article"
    article = strip_factory_chrome(article, desk)
    if _text_len(article) < 120:
        return None, "thin-article"
    head = _head_inner(html)
    head = re.sub(
        r"<link[^>]+(?:allchinabuy-theme|allchinabuy-ca-desk|allchinabuy-nl-desk|allchinabuy-uk-desk|acbuy-theme|acbuy-nl-desk|acbuy-ca-desk|bbdbuy-theme|bbdbuy-ca-desk|bbdbuy-uk-desk|bbdbuy-us-desk|bbdbuy-de-desk|bbdbuy-it-desk|cssbuy-theme|cssbuy-ca-desk|cssbuy-uk-desk|cssbuy-us-desk|cssbuy-de-desk|cssbuy-at-desk|cssbuy-es-desk|cssbuy-fr-desk|cssbuy-it-desk|cssbuy-nl-desk)\.css[^>]*>\s*",
        "",
        head,
        flags=re.I,
    )
    head = re.sub(
        r'<style id="(?:acbuy-nl-chrome|country-desk-chrome)">[\s\S]*?</style>\s*',
        "",
        head,
        flags=re.I,
    )
    inject = (
        f"<!-- country desk chrome {desk.css_v} -->\n"
        '<link rel="icon" href="/favicon1.ico">\n'
        f'<link rel="stylesheet" href="/assets/css/{desk.theme_css}?v={desk.css_v}">\n'
        f'<link rel="stylesheet" href="/assets/css/{desk.desk_css}?v={desk.css_v}">\n'
        f'<style id="{desk.chrome_style_id}">{chrome_lock(desk)}</style>\n'
    )
    head = head.rstrip() + "\n" + inject + "\n"
    if "favicon1.ico" not in head:
        head = head.rstrip() + '\n<link rel="icon" href="/favicon1.ico">\n'
    trailing = after_footer_keep(html, article)
    extra_scripts = _body_scripts_outside_article(html, article + trailing)
    out = (
        "<!DOCTYPE html>\n"
        f"{_html_lang_tag(html, desk.lang)}\n"
        f"<head>\n{head.rstrip()}\n</head>\n"
        f"<body {desk.inner_marker}>\n"
        f"{header(desk, page_href)}"
        f'<main id="main" class="inner-article">\n{article}\n</main>\n'
        f"{footer(desk)}\n"
        f"{trailing}\n"
        f"{extra_scripts}\n"
        "</body></html>\n"
    )
    if "Georgia" in out and "#00C853" in out:
        return None, "georgia-leak"
    if any(tok and tok in out for tok in desk.invites) and page_href.rstrip("/") in {"", "/"}:
        return None, "invite-on-home"
    home = desk.home_href or "/"
    if home.rstrip("/") not in {"", "/"}:
        out = out.replace('href="/"', f'href="{home}"')
    return out, "ok"
