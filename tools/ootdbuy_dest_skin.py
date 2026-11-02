"""Official OOTDBuy chrome for dest country sites.

Public pages: no ops notes. Images from ootdbuy.com. Local language + currency.
Black header + official red #f03f3f CTAs. Does not smash unique coupons CMS.
"""
from __future__ import annotations

import json
import re
import shutil
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MEDIA_SRC = ROOT / "sites" / "shared" / "ootdbuy-media"
OFF = "https://ootdbuy.com/"
EST = "https://ootdbuy.com/estimation/"
HELP = "https://ootdbuy.com/help"
W2C_SHEET = "https://w2clinks.com/spreadsheet/ootdbuy/"
W2C_SEARCH = "https://w2clinks.com/spreadsheet/"

SHOT_HOME = "/media/oficial.jpg"
SHOT_EST = "/media/volume-voorbeeld.jpg"
SHOT_DIY = "/media/oficial-diy.jpg"
SHOT_GIF = "/media/official-home-20261102.png"

CATS = [
    ("sneakers", "sneakers.jpg"),
    ("hoodie", "hoodie.jpg"),
    ("jacket", "jacket.jpg"),
    ("t-shirt", "t-shirt.jpg"),
    ("pants", "jeans.jpg"),
    ("bag", "bags.jpg"),
    ("watch", "watches.jpg"),
    ("hat", "hats.jpg"),
    ("glasses", "eyewear.jpg"),
    ("jewelry", "jewelry.jpg"),
    ("perfume", "perfume.jpg"),
    ("electronics", "headphones.jpg"),
]

UNIQUE_DIR = {
    "ootdbuy.nl": {
        "ootdbuy-coupons",
        "ootdbuy-community",
        "ootdbuy-qc-guide",
        "ootdbuy-invite-code",
        "ootdbuy-refund-guide",
        "ootdbuy-shoes-spreadsheet",
        "blog",
    },
    "ootdbuyspreadsheet.us": {
        "ootdbuy-coupons",
        "ootdbuy-community",
        "ootdbuy-qc-guide",
        "ootdbuy-invite-code",
        "ootdbuy-refund-guide",
        "ootdbuy-shoes-spreadsheet",
        "blog",
    },
    "ootdbuyspreadsheet.ca": {
        "ootdbuy-coupons",
        "ootdbuy-community",
        "ootdbuy-qc-guide",
        "ootdbuy-invite-code",
        "ootdbuy-refund-guide",
        "ootdbuy-shoes-spreadsheet",
        "blog",
    },
    "ootdbuyspreadsheet.co.uk": {
        "ootdbuy-coupons",
        "ootdbuy-community",
        "ootdbuy-qc-guide",
        "ootdbuy-invite-code",
        "ootdbuy-refund-guide",
        "ootdbuy-shoes-spreadsheet",
        "blog",
    },
    "ootdbuyspreadsheet.de": {
        "ootdbuy-coupons",
        "ootdbuy-community",
        "ootdbuy-qc-guide",
        "ootdbuy-invite-code",
        "ootdbuy-refund-guide",
        "ootdbuy-shoes-spreadsheet",
        "blog",
    },
}

CSS = """
<style id="ootd-official-skin">
:root{--primary:#f03f3f;--primary-dark:#ed4014;--primary-soft:#fff1f0;--nav-dark:#111111;--od-red:#f03f3f}
body{background:#f6f7f8;font-family:Inter,ui-sans-serif,system-ui,-apple-system,"Segoe UI",sans-serif}
.od-promo{background:#111111;color:#fff;text-align:center;padding:8px 14px;font-weight:600;font-size:13px;letter-spacing:.01em}
.od-promo a{color:#fff;text-decoration:none}
.btn-outline,.od-reg{border:1px solid #f03f3f;color:#f03f3f;background:#fff;border-radius:999px;padding:8px 16px;text-decoration:none;font-weight:600;font-size:14px}
.btn-primary,.od-login{background:#f03f3f;color:#fff;border-radius:999px;padding:8px 16px;text-decoration:none;font-weight:600;font-size:14px;border:1px solid #f03f3f}
.btn-cart{border:1px solid #f03f3f;color:#f03f3f;border-radius:999px;padding:8px 16px;text-decoration:none;font-weight:600;font-size:14px}
.od-head{background:#111111;border-bottom:1px solid #1f1f1f;position:sticky;top:0;z-index:50}
.od-head-inner{width:min(1180px,calc(100% - 28px));margin:0 auto;display:flex;align-items:center;gap:12px;padding:10px 0;flex-wrap:wrap}
.od-head-search{display:flex;gap:8px;margin:0 auto 12px;background:#fff;border:2px solid #f03f3f;border-radius:999px;padding:6px 6px 6px 18px;align-items:center;width:min(1100px,calc(100% - 28px))}
.od-head-search input{flex:1;border:0;outline:none;font-size:14px;background:transparent}
.od-head-search .btn{background:#f03f3f;color:#fff;border-radius:999px;min-width:96px;border:0;font-weight:700;cursor:pointer;padding:8px 16px}
.od-head-left,.od-head-right{display:flex;align-items:center;gap:16px;flex-wrap:wrap;font-size:14px;font-weight:600}
.od-head-left a,.od-head-right a{color:#eee;text-decoration:none}
.od-head-left a:hover,.od-head-right a:hover,.od-head-left a.on{color:#f03f3f}
.od-head-right{justify-content:flex-end}
.od-logo img{height:36px;width:auto;display:block}
.od-ccy{color:#bbb;font-size:13px;font-weight:600}
.od-hero{position:relative;border-radius:18px;overflow:hidden;min-height:420px;margin:18px 0 8px;background:#111111}
.od-hero-bg{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;filter:brightness(.38);object-position:center top}
.od-hero::after{content:"";position:absolute;inset:0;background:linear-gradient(90deg,rgba(17,17,17,.78) 0%,rgba(17,17,17,.4) 55%,rgba(17,17,17,.18) 100%);z-index:0}
.od-hero-copy{position:relative;z-index:1;padding:48px 36px 36px;color:#fff;max-width:760px}
.od-hero-copy h1{color:#fff;font-size:clamp(28px,4vw,44px);letter-spacing:-.03em;margin:0 0 12px}
.od-hero-copy .hsub{color:#f3f3f3;font-size:18px;max-width:640px}
.od-search{display:flex;gap:8px;margin:22px 0 10px;background:#fff;border-radius:999px;padding:6px 6px 6px 16px;align-items:center;max-width:640px}
.od-search input{flex:1;border:0;outline:none;font-size:14px;background:transparent}
.od-search .btn{border-radius:999px;min-width:110px;border:0;cursor:pointer;font:inherit;background:#f03f3f;color:#fff;font-weight:700}
.od-hero .cluster-nav a{color:#fff}
.od-hero .eu-badge{background:#f03f3f;color:#fff}
.od-steps{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;margin:18px 0}
@media(max-width:800px){.od-head-inner{text-align:center}.od-head-left,.od-head-right{justify-content:center}.od-steps{grid-template-columns:1fr}.od-hero-copy{padding:28px 18px}}
.od-step{background:#fff;border-radius:16px;padding:18px;border:1px solid #eee}
.od-step strong{display:block;color:#f03f3f;font-size:13px;margin-bottom:6px}
.od-step h3{margin:0 0 6px;font-size:18px}
.od-step p{margin:0;color:#555;font-size:14px}
.sg-split{display:grid;grid-template-columns:1.05fr .95fr;gap:22px;align-items:start}
@media(max-width:860px){.sg-split{grid-template-columns:1fr}}
figure.shot{margin:0}
figure.shot img{width:100%;border-radius:14px;border:1px solid #eee;display:block;background:#fff}
figure.shot figcaption{font-size:13px;color:#666;margin-top:8px}
.sg-cats{display:grid;grid-template-columns:repeat(auto-fill,minmax(150px,1fr));gap:12px}
.sg-cat{padding:0;overflow:hidden}
.sg-cat img{width:100%;aspect-ratio:1;object-fit:cover;display:block;background:#f5f5f5}
.sg-cat .b{padding:10px 12px}
.cluster-page{max-width:820px}
.cluster-page figure.shot{margin:16px 0 22px}
.cluster-nav a{color:#f03f3f}
.site-footer,.od-foot{background:#111111;color:#eee;margin-top:36px;padding:36px 0 28px}
.od-foot a{color:#fff;text-decoration:none}
.od-foot-grid{width:min(1180px,calc(100% - 28px));margin:0 auto;display:grid;grid-template-columns:repeat(4,1fr);gap:18px}
@media(max-width:800px){.od-foot-grid{grid-template-columns:1fr 1fr}}
.od-foot h3{color:#f03f3f;font-size:14px;margin:0 0 10px}
.od-foot p,.od-foot li{font-size:13px;line-height:1.7;color:#d8d8d8}
.od-foot ul{margin:0;padding:0;list-style:none}
.od-pay{display:flex;flex-wrap:wrap;gap:8px;margin-top:10px}
.od-pay span{background:#fff;color:#111111;border-radius:6px;padding:4px 8px;font-size:11px;font-weight:800}
</style>
"""

OPS_RX = [
    r"Lab 2 Oct 2026\.?\s*",
    r"Copy reviewed 2 Oct 2026\.?\s*",
    r"Measured 2 Oct 2026[^.]*\.\s*",
    r"Gemeten 2 Oct 2026[^.]*\.\s*",
    r"Gemessen 2 Oct 2026[^.]*\.\s*",
    r"Sister country hosts stay separate files — no 301\.?\s*",
    r"Sister desks[^.]{0,80}no 301\.?\s*",
    r"Schwesterdesks bleiben eigene Dateien — kein 301\.?\s*",
    r"Geen 301\.?\s*",
    r"kein 301\.?\s*",
    r"Independent desk — not the official app, not checkout\.?\s*",
    r"Independent information desk on [^.]+\. Not the official OOTDBuy site\.?\s*",
    r"Independence:[^<]{0,280}",
    r"this HTML is not checkout\.?\s*",
    r"diese HTML ist keine Kasse\.?\s*",
    r"not a location-name swap\.?\s*",
    r"kein Ortsnamen-Tausch\.?\s*",
    r"geen landnaam-wissel\.?\s*",
    r"Freight lab — not checkout",
    r"Already ranking on this host",
    r"not this TLD,?\s*",
    r"nicht diesen Hostnamen",
    r"this desk names",
    r"Infodesk",
    r"NL-infodesk",
    r"DE-Infodesk",
    r"<!-- DEPLOY GUARD:[^>]*-->",
    r"DEPLOY GUARD:[^<]*",
    r"ootdbuy\.nl is een infodesk[^.]{0,80}\.?\s*",
    r"ootdbuyspreadsheet\.(?:us|ca|co\.uk|de) is an information desk[^.]{0,80}\.?\s*",
]


def chrome(d: dict) -> dict:
    key = d["key"]
    ccy = d["ccy"]
    label = d["label"]
    packs = {
        "uk": {
            "home": "Home",
            "sheet": "Spreadsheet",
            "ship": "Shipping",
            "help": "Help",
            "reg": "Log In/Register",
            "login": "Login",
            "cart": "Cart",
            "promo": "Shop from China on ootdbuy.com — register before you paste a link.",
            "fwd": "Forwarding",
            "est": "Shipping Calculator",
            "custom": "How To Buy",
            "app": "App",
            "aff": "Affiliate",
            "lang": "English",
            "search": "Enter the product name/link",
            "submit": "Search",
            "sub": f"Shop from China's e-commerce with a delivery address in {label}. Prices on this page are shown in {ccy}.",
            "s1t": "Place orders",
            "s1": "Paste a Taobao, 1688 or Weidian link on ootdbuy.com.",
            "s2t": "QC in the warehouse",
            "s2": "Free HD photos before you book international freight.",
            "s3t": "Ship to your door",
            "s3": f"Choose a line with destination {label}. Last mile is often {d['post']}.",
            "shots": "How OOTDBuy works",
            "cap_home": "OOTDBuy home — paste a product link to start.",
            "cap_est": f"Shipping calculator. Set destination to {label} before you pay freight.",
            "cap_diy": "Register or log in on ootdbuy.com to pay in the official app.",
            "local": f"Delivery to {label}",
            "faq": "Questions",
            "cs": "Customer Service",
            "pay": "Payment",
            "guide": "Shopping Agent Guidance",
            "copy": f"OOTDBuy spreadsheet for {label}. Display currency {ccy}. Orders on ootdbuy.com.",
        },
    }
    packs["us"] = dict(packs["uk"])
    packs["us"].update({
        "sub": f"Shop from China's e-commerce with a US ZIP. Prices on this page are shown in {ccy}.",
        "s3": f"Choose a line with destination {label}. Last mile is often {d['post']}.",
        "copy": f"OOTDBuy spreadsheet for {label}. Display currency {ccy}. Orders on ootdbuy.com.",
    })
    packs["ca"] = dict(packs["uk"])
    packs["ca"].update({
        "sub": f"Shop from China's e-commerce with a Canadian postal code. Prices on this page are shown in {ccy}.",
        "s3": f"Choose a line with destination {label}. Last mile is often {d['post']}.",
        "copy": f"OOTDBuy spreadsheet for {label}. Display currency {ccy}. Orders on ootdbuy.com.",
        "cap_est": f"Shipping calculator. Set destination to {label} before you pay freight.",
    })
    packs["de"] = {
        "home": "Start",
        "sheet": "Spreadsheet",
        "ship": "Versand",
        "help": "Hilfe",
        "reg": "Anmelden/Registrieren",
        "login": "Anmelden",
        "cart": "Warenkorb",
        "promo": "Bestellen auf ootdbuy.com — zuerst registrieren, dann den Link einfügen.",
        "fwd": "Forwarding",
        "est": "Fracht schätzen",
        "custom": "How To Buy",
        "app": "App",
        "aff": "Affiliate",
        "lang": "Deutsch",
        "search": "Produktname oder Link",
        "submit": "Suchen",
        "sub": f"Aus Chinas Shops nach {label} bestellen. Preise auf dieser Seite in {ccy}.",
        "s1t": "Bestellen",
        "s1": "Taobao-, 1688- oder Weidian-Link auf ootdbuy.com einfügen.",
        "s2t": "QC im Lager",
        "s2": "Kostenlose HD-Fotos, bevor du die internationale Fracht buchst.",
        "s3t": "Zur Haustür",
        "s3": f"Linie mit Ziel {label}. Letzte Meile oft {d['post']}.",
        "shots": "So sieht OOTDBuy aus",
        "cap_home": "OOTDBuy-Startseite — Link einfügen und bestellen.",
        "cap_est": f"Fracht-Rechner. Ziel {label} wählen, bevor du Porto zahlst.",
        "cap_diy": "Auf ootdbuy.com registrieren oder anmelden.",
        "local": f"Lieferung nach {label}",
        "faq": "Fragen",
        "cs": "Kundenservice",
        "pay": "Zahlung",
        "guide": "Einkaufsagent",
        "copy": f"OOTDBuy-Spreadsheet für {label}. Anzeige in {ccy}. Bestellen auf ootdbuy.com.",
    }
    packs["nl"] = {
        "home": "Home",
        "sheet": "Spreadsheet",
        "ship": "Verzending",
        "help": "Helpcentrum",
        "reg": "Inloggen/Registreren",
        "login": "Inloggen",
        "cart": "Winkelwagen",
        "promo": "Bestellen op ootdbuy.com — eerst registreren, dan de link plakken.",
        "fwd": "Forwarding",
        "est": "Vrachtcalculator",
        "custom": "How To Buy",
        "app": "App",
        "aff": "Affiliate",
        "lang": "Nederlands",
        "search": "Productnaam of link",
        "submit": "Zoeken",
        "sub": f"Shop in China met bezorging in {label}. Prijzen op deze pagina in {ccy}.",
        "s1t": "Bestellen",
        "s1": "Plak een Taobao-, 1688- of Weidian-link op ootdbuy.com.",
        "s2t": "QC in het magazijn",
        "s2": "Gratis HD-foto’s vóór internationale vracht.",
        "s3t": "Naar je deur",
        "s3": f"Kies een lijn met bestemming {label}. Last-mile vaak {d['post']}.",
        "shots": "Zo werkt OOTDBuy",
        "cap_home": "OOTDBuy-home — plak de link om te starten.",
        "cap_est": f"Vrachtcalculator. Bestemming {label} vóór je porto betaalt.",
        "cap_diy": "Registreer of log in op ootdbuy.com.",
        "local": f"Bezorging in {label}",
        "faq": "Vragen",
        "cs": "Klantenservice",
        "pay": "Betaling",
        "guide": "Inkoopagent",
        "copy": f"OOTDBuy-spreadsheet voor {label}. Weergave in {ccy}. Bestellen op ootdbuy.com.",
    }
    return packs[key]


def fig(src: str, cap: str) -> str:
    return (
        f'<figure class="shot"><img src="{escape(src)}" alt="{escape(cap)}" width="1400" height="900" loading="lazy" decoding="async">'
        f"<figcaption>{escape(cap)}</figcaption></figure>"
    )


def header_html(host: str, d: dict) -> str:
    L = chrome(d)
    p = d["pages"]
    promo = L.get("promo") or "Shop on ootdbuy.com"
    cart = L.get("cart") or "Cart"
    login = L.get("login") or "Login"
    search = L.get("search") or "Enter the product name/link"
    submit = L.get("submit") or "Search"
    return (
        f'<div class="od-promo"><a href="{OFF}" rel="noopener">{escape(promo)}</a></div>'
        '<header class="od-head">'
        '<div class="od-head-inner">'
        f'<a class="od-logo" href="/"><img src="/assets/images/ootdbuy-logo.png" alt="OOTDBuy"></a>'
        '<nav class="od-head-left">'
        f'<a class="on" href="/">{escape(L["home"])}</a>'
        f'<a href="/{p["spreadsheet"]}/">{escape(L["sheet"])}</a>'
        f'<a href="{EST}" rel="noopener">{escape(L.get("est") or "Shipping Calculator")}</a>'
        f'<a href="/{p["shipping"]}/">{escape(L["ship"])}</a>'
        f'<a href="/{p["guide"]}/">{escape(L["help"])}</a>'
        f'<a href="{OFF}" rel="noopener">{escape(L.get("custom") or "How To Buy")}</a>'
        "</nav>"
        '<div class="od-head-right">'
        f'<span class="od-ccy">{escape(L["lang"])} / {escape(d["ccy"])}</span>'
        f'<a class="btn-cart" href="{OFF}" rel="noopener">{escape(cart)}</a>'
        f'<a class="od-login" href="{OFF}" rel="noopener">{escape(L["reg"])}</a>'
        "</div></div>"
        f'<form class="od-head-search" action="{W2C_SEARCH}" method="get" target="_blank" rel="noopener">'
        f'<input name="q" placeholder="{escape(search)}" aria-label="{escape(search)}">'
        f'<button class="btn" type="submit">{escape(submit)}</button>'
        "</form>"
        "</header>"
    )


def footer_html(host: str, d: dict) -> str:
    L = chrome(d)
    p = d["pages"]
    return (
        '<footer class="od-foot"><div class="od-foot-grid">'
        f"<div><h3>{escape(L['cs'])}</h3><ul>"
        f'<li><a href="{HELP}">{escape(L["help"])}</a></li>'
        f'<li><a href="/{p["faq"]}/">{escape(L["faq"])}</a></li>'
        "</ul></div>"
        f"<div><h3>{escape(L['pay'])}</h3><ul>"
        f'<li><a href="{OFF}">ootdbuy.com</a></li>'
        f"<li>{escape(d['ccy'])}</li></ul>"
        '<p class="od-pay"><span>VISA</span><span>Mastercard</span><span>PayPal</span></p></div>'
        f"<div><h3>{escape(L['guide'])}</h3><ul>"
        f'<li><a href="/{p["guide"]}/">{escape(L["help"])}</a></li>'
        f'<li><a href="{EST}">{escape(L.get("est") or "Shipping Calculator")}</a></li>'
        f'<li><a href="/{p["qc"]}/">QC</a></li>'
        "</ul></div>"
        f"<div><h3>OOTDBuy</h3><p>{escape(L['copy'])}</p>"
        f'<p><a href="{OFF}">ootdbuy.com</a></p></div>'
        "</div></footer>"
    )


def strip_ops(html: str) -> str:
    for rx in OPS_RX:
        html = re.sub(rx, "", html, flags=re.I)
    return html


def _replace_section(html: str, sid: str, new: str) -> str:
    return re.sub(
        rf'<section\b[^>]*\bid=["\']{sid}["\'][^>]*>.*?</section>',
        new,
        html,
        count=1,
        flags=re.I | re.S,
    )


def inject_css(html: str) -> str:
    if "family=Inter" not in html:
        html = html.replace(
            "</head>",
            '<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">\n</head>',
            1,
        )
    if 'id="ootd-official-skin"' in html:
        html = re.sub(r'<style id="ootd-official-skin">[\s\S]*?</style>', CSS, html, count=1)
    else:
        html = html.replace("</head>", CSS + "\n</head>", 1)
    return html


def skin_chrome(html: str, host: str, d: dict) -> str:
    html = inject_css(html)
    html = re.sub(r'<div class="od-promo">[\s\S]*?</div>\s*', "", html, count=1)
    html = re.sub(
        r"<header class=\"(?:site-header|od-head|top)\"[^>]*>[\s\S]*?</header>",
        header_html(host, d),
        html,
        count=1,
    )
    html = re.sub(
        r"<footer class=\"(?:site-footer|od-foot|site-ft)\"[^>]*>[\s\S]*?</footer>",
        footer_html(host, d),
        html,
        count=1,
    )
    return strip_ops(html)


def cat_wall(d: dict) -> str:
    L = chrome(d)
    tiles = []
    for q, fn in CATS:
        tiles.append(
            f'<a class="sg-cat" href="{W2C_SEARCH}?q={escape(q)}" target="_blank" rel="noopener">'
            f'<img src="/img/cat/{escape(fn)}" alt="{escape(q)}" width="560" height="560" loading="lazy">'
            f'<div class="b"><strong>{escape(q.title())}</strong><span>{escape(q)}</span></div></a>'
        )
    return (
        f'<section class="sg-sec" id="cat-wall"><h2>{escape(L["sheet"])}</h2>'
        f'<div class="sg-cats">{"".join(tiles)}</div></section>'
    )


def shots_html(d: dict) -> str:
    L = chrome(d)
    return (
        f'<section class="sg-sec" id="shots"><h2>{escape(L["shots"])}</h2>'
        '<div class="sg-split"><div>'
        f"{fig(SHOT_HOME, L['cap_home'])}"
        "</div><div>"
        f"{fig(SHOT_EST, L['cap_est'])}"
        f"{fig(SHOT_DIY, L['cap_diy'])}"
        "</div></div></section>"
    )


def process_html(d: dict) -> str:
    L = chrome(d)
    return (
        '<section class="od-steps" id="how">'
        f'<article class="od-step"><strong>01</strong><h3>{escape(L["s1t"])}</h3><p>{escape(L["s1"])}</p></article>'
        f'<article class="od-step"><strong>02</strong><h3>{escape(L["s2t"])}</h3><p>{escape(L["s2"])}</p></article>'
        f'<article class="od-step"><strong>03</strong><h3>{escape(L["s3t"])}</h3><p>{escape(L["s3"])}</p></article>'
        "</section>"
    )


def rebuild_hero(html: str, host: str, d: dict) -> str:
    L = chrome(d)
    m = re.search(r"<h1>([\s\S]*?)</h1>", html)
    h1 = re.sub(
        r"\s*\((?:2026|Leitfaden 2026|guía 2026|guide 2026|guida 2026|gids 2026)\)\s*",
        "",
        m.group(1) if m else "",
    )
    nav = re.search(r'<nav class="cluster-nav"[\s\S]*?</nav>', html)
    nav_html = nav.group(0) if nav else ""
    hero = (
        '<section class="od-hero" id="hero">'
        f'<img class="od-hero-bg" src="{SHOT_GIF}" alt="OOTDBuy">'
        '<div class="od-hero-copy">'
        f"<h1>{h1}</h1>"
        f'<p class="hsub">{escape(L["sub"])}</p>'
        f'<form class="od-search" action="{W2C_SEARCH}" method="get" target="_blank" rel="noopener">'
        f'<input name="q" placeholder="{escape(L["search"])}" aria-label="{escape(L["search"])}">'
        f'<button class="btn btn-primary" type="submit">{escape(L["submit"])}</button>'
        "</form>"
        f"{nav_html}"
        f'<p class="eu-badge">{escape(d["dest"])} · {escape(d["ccy"])} · {escape(d["post"])}</p>'
        "</div></section>"
    )
    html = re.sub(
        r'<section class="sg-hero">[\s\S]*?</section>|<section class="od-hero"[\s\S]*?</section>',
        hero,
        html,
        count=1,
    )
    return html


def rebuild_home(html: str, host: str, d: dict) -> str:
    L = chrome(d)
    html = skin_chrome(html, host, d)
    html = rebuild_hero(html, host, d)
    html = _replace_section(html, "shots", "")
    html = _replace_section(html, "lab", "")
    html = _replace_section(html, "kept", "")
    html = _replace_section(
        html,
        "agent",
        f'<section class="sg-sec" id="agent"><div class="sg-split"><div class="sg-prose">'
        f"<h2>OOTDBuy</h2><p>{escape(L['sub'])}</p>"
        f'<p><a class="btn btn-primary" href="{OFF}">{escape(L["reg"])}</a> '
        f'<a class="btn btn-outline" href="{EST}">{escape(L.get("est") or "Shipping Calculator")}</a> '
        f'<a class="btn btn-outline" href="{W2C_SHEET}" target="_blank" rel="noopener">w2clinks</a></p>'
        f'</div>{fig(SHOT_DIY, L["cap_diy"])}</div></section>',
    )
    html = _replace_section(html, "sheet-explain", shots_html(d))
    html = _replace_section(
        html,
        "restricted",
        f'<section class="sg-sec" id="restricted"><h2>QC</h2>'
        f"<p>{escape(L['s2'])}</p>{fig(SHOT_EST, L['s2'])}</section>",
    )
    html = _replace_section(html, "cat-wall", cat_wall(d))
    html = _replace_section(html, "states", process_html(d))
    from ootdbuy_dest_copy import extra_faq

    faqs = extra_faq(d, host)
    blocks = []
    for i, (q, paras) in enumerate(faqs):
        op = " open" if i == 0 else ""
        blocks.append(
            f'<details class="sg-faq"{op}><summary>{escape(q)}</summary><p>{escape(" ".join(paras))}</p></details>'
        )
    html = _replace_section(
        html,
        "faq",
        f'<section class="sg-sec" id="faq"><h2>{escape(L["faq"])}</h2>{"".join(blocks)}</section>',
    )
    faq_ld = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "inLanguage": d.get("lang") or "en",
        "mainEntity": [
            {
                "@type": "Question",
                "name": q,
                "acceptedAnswer": {"@type": "Answer", "text": " ".join(paras)},
            }
            for q, paras in faqs
        ],
    }
    dumped = json.dumps(faq_ld, ensure_ascii=False)
    if '"FAQPage"' in html:
        html = re.sub(
            r'<script type="application/ld\+json">\s*\{[^{}]*"@type"\s*:\s*"FAQPage"[\s\S]*?</script>',
            f'<script type="application/ld+json">{dumped}</script>',
            html,
            count=1,
        )
    html = re.sub(r'<p class="local-src">[\s\S]*?</p>', "", html, count=2)
    html = re.sub(
        r'(<section class="sg-sec" id="local">)(?:\s*<figure class="shot">[\s\S]*?</figure>)+',
        rf'\1{fig(SHOT_EST, L["cap_est"])}',
        html,
        count=1,
    )
    html = re.sub(
        r'(<section class="sg-sec" id="local">)(?!\s*<figure)',
        rf'\1{fig(SHOT_EST, L["cap_est"])}',
        html,
        count=1,
    )
    html = strip_ops(html)
    html = re.sub(r"—\s*,\s*", "— ", html)
    html = patch_catalog_w2c(html)
    return html


def patch_catalog_w2c(html: str) -> str:
    """Homepage cards fetch /api/products/ and open on w2clinks.com."""
    for old in (
        'var REG="https://ootdbuy.com/";',
        "var REG='https://ootdbuy.com/';",
        'var REG="https://www.bbdbuy.com/";',
        "var REG='https://www.bbdbuy.com/';",
    ):
        html = html.replace(old, f'var REG="{W2C_SHEET}";')
    return html


def article_figures(kind: str, d: dict) -> list[str]:
    L = chrome(d)
    if kind == "shipping":
        return [fig(SHOT_EST, L["cap_est"]), fig(SHOT_HOME, L["cap_home"])]
    if kind == "guide":
        return [fig(SHOT_DIY, L["cap_diy"]), fig(SHOT_GIF, L["s1"])]
    if kind == "qc":
        return [fig(SHOT_EST, L["s2"]), fig(SHOT_EST, L["cap_est"])]
    if kind == "legal":
        return [fig(SHOT_DIY, L["cap_diy"]), fig(SHOT_HOME, L["cap_home"])]
    return [fig(SHOT_HOME, L["cap_home"]), fig(SHOT_EST, L["cap_est"])]


def install_media(host: str) -> list[Path]:
    dest = ROOT / "sites" / host / "overlay"
    media = dest / "media"
    cats = dest / "img" / "cat"
    media.mkdir(parents=True, exist_ok=True)
    cats.mkdir(parents=True, exist_ok=True)
    written = []
    for name in (
        "official-home-20261102.png",
        "oficial.jpg",
        "oficial-diy.jpg",
        "volume-voorbeeld.jpg",
        "catalogus.jpg",
        "catalogus-zoek.jpg",
        "hero.jpg",
        "ootdbuy-logo.png",
    ):
        src = MEDIA_SRC / name
        if src.is_file():
            out = media / name
            shutil.copy2(src, out)
            written.append(out)
    logo = MEDIA_SRC / "ootdbuy-logo.png"
    if logo.is_file():
        assets = dest / "assets" / "images"
        assets.mkdir(parents=True, exist_ok=True)
        out = assets / "ootdbuy-logo.png"
        shutil.copy2(logo, out)
        written.append(out)
    src_cats = MEDIA_SRC / "cats"
    if src_cats.is_dir():
        for p in src_cats.glob("*.jpg"):
            out = cats / p.name
            shutil.copy2(p, out)
            written.append(out)
    return written


def skin_overlay_files(host: str, d: dict, files: list[Path]) -> None:
    skip = UNIQUE_DIR.get(host, set())
    for path in files:
        if path.suffix.lower() not in {".html"}:
            continue
        rel = path.as_posix()
        if any(f"/{slug}/" in rel or rel.endswith(f"/{slug}/index.html") for slug in skip):
            continue
        html = path.read_text(encoding="utf-8")
        if path.name == "index.html" and path.parent.name == "overlay":
            continue
        html = skin_chrome(html, host, d)
        path.write_text(html, encoding="utf-8")
