#!/usr/bin/env python3
"""Local chrome, homepage guides, catalog translator, figures for HipoBuy desks.

Same editorial inbox as hipobuy.es. Does not touch hipobuyspreadsheet.net.
"""
from __future__ import annotations

import json
import re
from html import escape

MAIL = "Cruisezhang0202@gmail.com"
EST = "https://hipobuy.com/estimation"
REG = "https://hipobuy.com/register?inviteCode=VGEICZNX0"
OFFICIAL = "https://hipobuy.com/"
NET = "https://hipobuyspreadsheet.net/"
INVITE = "VGEICZNX0"
SHOT_OFF = "/media/official-home-20260930.png"
SHOT_EST = "/media/estimator-20260930.png"
SHOT_CAT = "/media/at-spreadsheet-20260930.png"

THEMES = {
    "at": ("#7c2d12", "#9a3412", "#f6efe6", "#fed7aa", "#ffedd5"),
    "nl": ("#115e59", "#0d9488", "#f0fdfa", "#99f6e4", "#ccfbf1"),
    "uk": ("#1e293b", "#1d4ed8", "#e8edf4", "#bfdbfe", "#dbeafe"),
    "eu": ("#1c1917", "#0e7490", "#eef7f8", "#a5f3fc", "#cffafe"),
    "us": ("#312e81", "#4f46e5", "#f5f3ff", "#c4b5fd", "#ede9fe"),
    "ukhaul": ("#134e4a", "#0f766e", "#eef6f3", "#99f6e4", "#ccfbf1"),
}

# local, english-index
GLOSS = {
    "at": [
        ("Turnschuhe", "sneakers"),
        ("Kapuzenpullover", "hoodie"),
        ("Jacke", "jacket"),
        ("Jeans", "jeans"),
        ("Tasche", "bag"),
        ("Sonnenbrille", "sunglasses"),
        ("Uhr", "watch"),
        ("Mantel", "coat"),
        ("Hose", "pants"),
    ],
    "nl": [
        ("Turnschoenen", "sneakers"),
        ("Hoodie", "hoodie"),
        ("Jas", "jacket"),
        ("Spijkerbroek", "jeans"),
        ("Tas", "bag"),
        ("Zonnebril", "sunglasses"),
        ("Horloge", "watch"),
        ("Broek", "pants"),
    ],
    "uk": [
        ("trainers", "sneakers"),
        ("jumper", "hoodie"),
        ("trousers", "pants"),
        ("trainers uk", "sneakers"),
    ],
    "eu": [
        ("zapatillas", "sneakers"),
        ("sudadera", "hoodie"),
        ("chaqueta", "jacket"),
        ("vaqueros", "jeans"),
        ("Turnschuhe", "sneakers"),
        ("Kapuzenpullover", "hoodie"),
        ("baskets", "sneakers"),
        ("sweat", "hoodie"),
    ],
    "us": [
        ("sneakers", "sneakers"),
        ("hoodie", "hoodie"),
        ("jacket", "jacket"),
    ],
    "ukhaul": [
        ("trainers", "sneakers"),
        ("jumper", "hoodie"),
        ("trousers", "pants"),
    ],
}


def labels(key: str) -> dict[str, str]:
    if key == "at":
        return {
            "home": "Start",
            "ship": "Versand",
            "howto": "Ablauf",
            "help": "Hilfe",
            "news": "Neuigkeiten",
            "about": "Über uns",
            "sheet": "Katalog",
            "coupons": "Coupons",
            "reg": "Registrieren",
            "est": "Offizieller Schätzer",
            "note": "Unabhängiger AT-Desk, nicht HipoBuy und nicht der Finds-Hub",
            "contact": "Redaktion (kein Bestellticket)",
            "translate": "Katalogsuche: Deutsch tippen, Englisch senden",
            "go": "Auf dem Katalog suchen",
        }
    if key == "nl":
        return {
            "home": "Home",
            "ship": "Verzending",
            "howto": "Stappen",
            "help": "Hulp",
            "news": "Nieuws",
            "about": "Over ons",
            "sheet": "Catalogus",
            "coupons": "Coupons",
            "reg": "Registreren",
            "est": "Officiële estimator",
            "note": "Onafhankelijke NL-desk, niet HipoBuy en niet de finds-hub",
            "contact": "Redactie (geen bestelticket)",
            "translate": "Cataloguszoek: Nederlands typen, Engels versturen",
            "go": "Zoek in de catalogus",
        }
    job = {
        "uk": "Independent .co.uk coupon desk, not the .uk haul log",
        "eu": "Independent EU coupon desk — TLD is not a destination",
        "us": "Independent US freight desk, not the .net finds hub",
        "ukhaul": "Independent Nominet haul log, not the .co.uk coupon desk",
    }[key]
    return {
        "home": "Home",
        "ship": "Shipping",
        "howto": "How to",
        "help": "Help",
        "news": "News",
        "about": "Who we are",
        "sheet": "Spreadsheet",
        "coupons": "Coupons",
        "reg": "Register",
        "est": "Official estimator",
        "note": job,
        "contact": "Editorial (not an order ticket)",
        "translate": "Catalogue search: local word in, English query out",
        "go": "Search the catalogue",
    }


def nav_links(key: str, d: dict) -> list[tuple[str, str]]:
    s = d["slugs"]
    L = labels(key)
    links = [("/", L["home"])]
    if key in ("uk", "eu"):
        links.append(("/hipobuy-coupons/", L["coupons"]))
    if key == "uk":
        links.append(("/blog/posts/hipobuy-sizing-guide/", "UK sizing"))
    if key == "us":
        links.append(("/guides/shipping/", L["ship"]))
    else:
        links.append(("/hipobuy-shipping-guide/", L["ship"]))
    if key not in ("uk", "eu"):
        links.append(("/how-to-use-hipobuy/", L["howto"]))
    if key in ("ukhaul", "us", "at", "nl"):
        links.append(("/hipobuy-spreadsheet/", L["sheet"]))
    links.extend(
        [
            (f"/{s['help']}/", L["help"]),
            (f"/{s['news']}/", L["news"]),
            (f"/{s['about']}/", L["about"]),
        ]
    )
    # unique by href
    seen = set()
    out = []
    for href, lab in links:
        if href not in seen:
            seen.add(href)
            out.append((href, lab))
    return out


def fig(src: str, cap: str) -> str:
    return (
        f'<figure class="shot"><img src="{src}" alt="{escape(cap)}" loading="lazy">'
        f"<figcaption>{cap}</figcaption></figure>"
    )


def translator_widget(key: str) -> str:
    pairs = GLOSS.get(key) or []
    if not pairs:
        return ""
    L = labels(key)
    mapping = {a.lower(): b for a, b in pairs}
    chips = " · ".join(f"<code>{escape(a)}</code>→<code>{escape(b)}</code>" for a, b in pairs[:7])
    dest = "/hipobuy-spreadsheet/"
    return f"""
<div class="box" id="katalog">
  <p><strong>{escape(L["translate"])}</strong></p>
  <p class="note">{chips}</p>
  <form id="hipo-trans" action="{dest}" method="get">
    <input type="search" name="q" id="hipo-q" required placeholder="{escape(pairs[0][0])}">
    <button type="submit">{escape(L["go"])}</button>
  </form>
  <p class="note" id="hipo-hint"></p>
</div>
<script>
(function(){{
  var map = {json.dumps(mapping, ensure_ascii=False)};
  var form = document.getElementById('hipo-trans');
  if (!form) return;
  form.addEventListener('submit', function(ev) {{
    var raw = (document.getElementById('hipo-q').value || '').trim();
    var key = raw.toLowerCase();
    var en = map[key] || raw;
    var hint = document.getElementById('hipo-hint');
    if (hint) hint.textContent = raw + ' → ' + en;
    if (en !== raw) {{
      ev.preventDefault();
      location.href = {json.dumps(dest)} + '?q=' + encodeURIComponent(en);
    }}
  }});
}})();
</script>
"""


def contact_block(key: str) -> str:
    L = labels(key)
    if key == "at":
        body = (
            f'{L["contact"]}: <a href="mailto:{MAIL}">{MAIL}</a> — dieselbe Redaktionsadresse wie hipobuy.es. '
            "Bestellungen, Zahlungen und Reklamationen nur auf hipobuy.com."
        )
    elif key == "nl":
        body = (
            f'{L["contact"]}: <a href="mailto:{MAIL}">{MAIL}</a> — hetzelfde redactionele adres als hipobuy.es. '
            "Bestellingen alleen via hipobuy.com."
        )
    else:
        body = (
            f'{L["contact"]}: <a href="mailto:{MAIL}">{MAIL}</a> — same editorial inbox as hipobuy.es. '
            "Order tickets stay on hipobuy.com."
        )
    return f'<p class="note">{body}</p>'


def css(key: str) -> str:
    ink, accent, bg, border, head = THEMES[key]
    return f"""
:root {{ --ink:{ink}; --muted:{accent}; --bg:{bg}; --card:#fff; --accent:{accent}; --border:{border}; --head:{head}; }}
body {{ margin:0; font-family: Georgia, ui-serif, serif; background:var(--bg); color:var(--ink); line-height:1.55; }}
header, main, footer {{ max-width:46rem; margin:0 auto; padding:1.25rem; }}
.note {{ color:var(--muted); font-size:.92rem; }}
h1 {{ font-size:clamp(1.55rem,4vw,2.15rem); }}
h2 {{ font-size:1.18rem; margin-top:1.8rem; }}
h3 {{ font-size:1.02rem; margin-top:1.15rem; }}
table {{ width:100%; border-collapse:collapse; background:var(--card); }}
th, td {{ border:1px solid var(--border); padding:.55rem .65rem; text-align:left; font-size:.95rem; }}
th {{ background:var(--head); }}
a.cta {{ display:inline-block; background:var(--accent); color:#fff; text-decoration:none; padding:.7rem 1rem; border-radius:.5rem; margin:.25rem .5rem .25rem 0; }}
.box {{ background:var(--card); padding:1rem 1.1rem; border-radius:.5rem; }}
nav.local a {{ margin-right:1rem; display:inline-block; }}
code {{ background:var(--head); padding:.05rem .3rem; }}
figure.shot {{ margin:1.1rem 0; }}
figure.shot img {{ width:100%; height:auto; border:1px solid var(--border); background:var(--card); }}
figcaption {{ font-size:.88rem; color:var(--muted); margin-top:.4rem; }}
form#hipo-trans {{ display:flex; gap:.4rem; flex-wrap:wrap; margin:.6rem 0; }}
form#hipo-trans input {{ flex:1; min-width:12rem; padding:.5rem .6rem; }}
form#hipo-trans button {{ background:var(--accent); color:#fff; border:0; padding:.5rem .8rem; border-radius:.4rem; }}
.pp {{ margin:0.7rem 0; }}
.ph {{ margin-top:1.4rem; }}
article.hipo-howto {{ max-width:none; margin:0; padding:0; text-align:left; }}
"""


def shell_page(
    key: str,
    d: dict,
    *,
    title: str,
    desc: str,
    canonical: str,
    crumb: str,
    inner: str,
) -> str:
    L = labels(key)
    ink, accent, bg, border, head = THEMES[key]
    nav = "\n    ".join(
        f'<a href="{escape(href)}">{escape(lab)}</a>' for href, lab in nav_links(key, d)
    )
    jsonld = json.dumps(
        {
            "@context": "https://schema.org",
            "@type": "WebPage",
            "name": title,
            "inLanguage": d["lang"],
            "url": canonical,
            "isPartOf": {"@type": "WebSite", "name": d["host"], "url": f"https://{d['host']}/"},
        },
        ensure_ascii=False,
    )
    return f"""<!doctype html>
<html lang="{escape(d['lang'])}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{escape(title)}</title>
<meta name="description" content="{escape(desc)}">
<link rel="canonical" href="{escape(canonical)}">
<meta name="robots" content="index,follow">
<style>{css(key)}</style>
<script type="application/ld+json">{jsonld}</script>
</head>
<body>
<header>
  <p class="note">HipoBuy · {escape(d['host'])} · {escape(L['note'])}</p>
  <nav class="local">
    {nav}
  </nav>
</header>
<main>
  <p class="note">{escape(L['home'])} · {escape(crumb)}</p>
  {inner}
  {contact_block(key)}
</main>
<footer>
  <p class="note">{escape(L['note'])}. <a href="mailto:{MAIL}">{MAIL}</a></p>
</footer>
</body>
</html>
"""


def cms_nav_html(key: str, d: dict) -> str:
    items = "".join(
        f'<li><a href="{escape(href)}">{escape(lab)}</a></li>'
        for href, lab in nav_links(key, d)
        if href != "/"
    )
    L = labels(key)
    return f'<ul class="nl">{items}</ul>'


def localize_cms_nav(html: str, key: str, d: dict) -> str:
    html = re.sub(r'<ul class="nl">.*?</ul>', cms_nav_html(key, d), html, count=1, flags=re.S)
    L = labels(key)
    html = re.sub(r">Register</a>", f">{L['reg']}</a>", html, count=1)
    html = re.sub(r">Home</a>", f">{L['home']}</a>", html, count=1)
    return html


def nine_states(key: str) -> str:
    if key == "at":
        rows = [
            ("Order Submitted", "Bestellung abgeschickt, Ware in China bezahlt."),
            ("Order Placed", "HipoBuy kauft in der Drittshop, oft innerhalb von 6 Arbeitsstunden."),
            ("Seller Shipped", "Der chinesische Shop hat abgeschickt."),
            ("Arrived at Warehouse", "Im Lager angekommen."),
            ("Inspection & Storage", "Prüfung und Einlagerung, oft 24 Stunden."),
            ("Shipping Requested", "Du bündelst und buchst die internationale Linie."),
            ("Parcel Packed", "Karton wird gepackt."),
            ("Shipped", "Start aus China."),
            ("Delivered & Confirmed", "Zugestellt, Empfang bestätigen."),
        ]
        h = "Neun Zustände, drei Bildschirme"
        n = "Die ersten vier leben unter Order, die nächsten unter Warehouse, die letzten unter Parcel. Offizielles Tutorial, hier auf Deutsch erklärt — die Screenshots der Plattform bleiben englisch."
    elif key == "nl":
        rows = [
            ("Order Submitted", "Bestelling verstuurd, product in China betaald."),
            ("Order Placed", "HipoBuy koopt in de Chinese shop, vaak binnen 6 werkuren."),
            ("Seller Shipped", "De Chinese verkoper heeft verzonden."),
            ("Arrived at Warehouse", "Aangekomen in het magazijn."),
            ("Inspection & Storage", "Controle en opslag, vaak 24 uur."),
            ("Shipping Requested", "Jij bundelt en boekt de internationale lijn."),
            ("Parcel Packed", "Doos wordt ingepakt."),
            ("Shipped", "Vertrek uit China."),
            ("Delivered & Confirmed", "Bezorgd; ontvangst bevestigen."),
        ]
        h = "Negen statussen, drie schermen"
        n = "De eerste vier staan onder Order, daarna Warehouse, daarna Parcel. Officiële tutorial, hier in het Nederlands; de platform-screenshots blijven Engels."
    else:
        rows = [
            ("Order Submitted", "You paid for the goods plus China domestic."),
            ("Order Placed", "HipoBuy buys in the third-party shop, often within 6 working hours."),
            ("Seller Shipped", "The Chinese seller dispatched."),
            ("Arrived at Warehouse", "At the warehouse."),
            ("Inspection & Storage", "QC and storage, often 24 hours."),
            ("Shipping Requested", "You consolidate and book the international line."),
            ("Parcel Packed", "Carton packed."),
            ("Shipped", "Left China."),
            ("Delivered & Confirmed", "Delivered; confirm receipt."),
        ]
        h = "Nine states, three screens"
        n = "The first four live under Order, then Warehouse, then Parcel. Official tutorial explained here; platform screenshots stay English."
    body = "".join(f"<tr><td><code>{a}</code></td><td>{b}</td></tr>" for a, b in rows)
    return f"<h2>{h}</h2><p>{n}</p><table><thead><tr><th>State</th><th></th></tr></thead><tbody>{body}</tbody></table>"


def homepage_html(key: str, d: dict) -> str:
    """Long ES-style local guide. Overlay file + origin index."""
    L = labels(key)
    host = d["host"]
    s = d["slugs"]
    if key == "at":
        title = "HipoBuy Österreich: so kaufst du in China auf eine AT-Adresse"
        desc = (
            "Unabhängiger AT-Desk: was ein Einkaufsagent ist, warum der Katalog Englisch ist, "
            "Volumengewicht, Zollquellen, Lab 29 Sep 2026. Ohne Unterdeklaration."
        )
        h1 = "So kommt ein HipoBuy-Paket nach Österreich"
        inner = f"""
  <h1>{h1}</h1>
  <p>HipoBuy <strong>verkauft die Ware nicht</strong>. Es ist ein Einkaufsagent: er kauft in chinesischen Drittshops in deinem Namen, fotografiert im Lager und schickt erst, wenn du eine internationale Linie buchst. Deshalb zahlst du zweimal — zuerst Ware plus Inlandversand in China, später Porto nach den QC-Fotos. Dazwischen kannst du stornieren, bündeln oder die Linie wechseln. Das steht so in der Plattform-Hilfe; dieser Desk wiederholt es auf Deutsch für eine österreichische Straße.</p>
  {fig(SHOT_OFF, "Offizielle Startseite hipobuy.com, eigene Aufnahme 30 Sep 2026. Englisch/USD ist die Voreinstellung — nicht dieser AT-Desk.")}
  <p>
    <a class="cta" href="/hipobuy-shipping-guide/">AT-Versandtabelle und Rechner</a>
    <a class="cta" href="{EST}">Offiziellen Schätzer öffnen</a>
    <a class="cta" href="/{s['help']}/">Fünfzehn Fragen</a>
  </p>

  <h2>Ein Spreadsheet ist hier kein Excel</h2>
  <p>Auf diesem Desk meint „Spreadsheet“ einen <strong>Katalog von Produktkarten</strong> (Foto, Marke, Referenzpreis, Link für den Agenten) — keine Tabelle mit Zellen. Die 8&nbsp;600 Zeilen Finds bleiben auf <a href="{NET}">hipobuyspreadsheet.net</a>. hipobuy.at hält Versandlabor, Ablauf, Hilfe und Neuigkeiten. LitBuy.at ist ein anderer Agent, kein 301.</p>
  {fig(SHOT_CAT, "Katalog auf diesem Host, eigene Aufnahme 30 Sep 2026. Die Karten kommen aus w2clinks; deutsche Wörter in der Suche liefern oft 0 Treffer.")}

  <h2>Der Katalog versteht Deutsch nicht — die Suche hier schon</h2>
  <p>Am 29.&nbsp;Aug.&nbsp;2026 hat die spanische Schwesterdesk gemessen: zapatillas, sudadera, chaqueta → 0 Karten; sneakers, hoodie, jacket → volle Seiten. Dasselbe Muster gilt für Turnschuhe, Kapuzenpullover, Jacke. Du tippst Deutsch, wir senden das englische Indexwort an <a href="/hipobuy-spreadsheet/">/hipobuy-spreadsheet/</a>.</p>
  {translator_widget(key)}

  {nine_states(key)}

  <h2>Österreich hat Linien, aber nicht alle tragen</h2>
  <p>Der öffentliche Schätzer braucht kein Konto. Am {escape('29 Sep 2026')} , Paket 1000&nbsp;g / 35×25×10&nbsp;cm, Kleidung/gewöhnliche Ware, Ziel AT: <strong>{d['lines']} Linien</strong>. Günstigste carriable Zeile <code>{d['cheap']}</code> etwa ${d['usd']:.2f} ({d['days']} Tage, oft 1100&nbsp;g Volumen). Das ist ein Snapshot, kein Checkout. Filtere auf verfügbare Linien, bevor du Tage vergleichst.</p>
  {fig(SHOT_EST, "Offizielles Formular hipobuy.com/estimation, eigene Aufnahme 30 Sep 2026. Ziel, Gewicht, Maße, Warentyp — dann Inquire. Anzeige bleibt USD.")}
  <p>Volumengewicht: L×B×H/8000 (manchmal /6000). Unser Laborkarton 35×25×10&nbsp;cm = 8750&nbsp;cm³ → 1,094&nbsp;kg, gerundet 1100&nbsp;g auf den meisten Luftlinien. Eine Daunenjacke wiegt wenig und kostet trotzdem Volumen.</p>

  <h2>Zoll — nur Erklärung</h2>
  <div class="box">
    <p>Drei Labels auf der Live-SKU: Tax free, Prepaid Duty, Duties Payable by Recipient. „Tax free“ löscht nicht die Prüfbefugnis der Zollstelle. Quellen, die wir nicht selbst messen: <a href="{d['customs']}">BMF Zoll</a> · <a href="{d['ioss']}">IOSS / Kommission</a> (Orientierung oft 150&nbsp;€). <strong>Keine Tipps zur Unterdeklaration.</strong></p>
  </div>
  <p>USD-Ziffern: der Währungsschalter ändert oft nur das Symbol. Laborsätze hier in Dollar. Invite {INVITE} steht im Coupon-Artikel, nicht in diesem Title.</p>
  <p>Tabak, Alkohol, Arzneimittel und verbotene Artikel reisen nicht. Restricted-Karten ohne Preis nicht bestellen.</p>
  <p><a href="/{s['help']}/">Hilfe</a> · <a href="/{s['news']}/">Neuigkeiten mit Datum</a> · <a href="/{s['about']}/">Über uns</a> · <a href="/how-to-use-hipobuy/">Ablauf</a></p>
  <p><a class="cta" href="{OFFICIAL}">HipoBuy öffnen, dann AT-Adresse in der App</a></p>
"""
    elif key == "nl":
        title = "HipoBuy Nederland: kopen in China naar een NL-adres"
        desc = (
            "Onafhankelijke NL-desk: wat een inkoopagent is, waarom de catalogus Engels is, "
            "volumgewicht, douanebronnen, lab 29 sep 2026. Geen onderwaardering."
        )
        h1 = "Verzendkosten naar Nederland narekenen na de magazijnfoto’s"
        inner = f"""
  <h1>{h1}</h1>
  <p>HipoBuy <strong>verkoopt de spullen niet</strong>. Het is een inkoopagent: hij koopt in Chinese shops op jouw naam, fotografeert in het magazijn en stuurt pas als jij een internationale lijn boekt. Je betaalt twee keer — eerst product plus binnenlands China-vervoer, later internationaal na QC. Daartussen kun je bundelen of de lijn wisselen.</p>
  {fig(SHOT_OFF, "Officiële homepage hipobuy.com, eigen opname 30 sep 2026. English/USD is de default — niet deze NL-desk.")}
  <p>
    <a class="cta" href="/hipobuy-shipping-guide/">NL-lijntabel</a>
    <a class="cta" href="{EST}">Officiële estimator</a>
    <a class="cta" href="/{s['help']}/">Vijftien vragen</a>
  </p>
  <h2>Spreadsheet is hier geen Excel</h2>
  <p>Het is een catalogus van kaarten. De 8&nbsp;600 finds blijven op <a href="{NET}">hipobuyspreadsheet.net</a>. ootdbuy.nl is een andere agent.</p>
  {fig(SHOT_CAT, "Catalogusgrid (zelfde index als AT), eigen opname 30 sep 2026. Nederlandse zoektermen geven vaak 0 hits.")}
  <h2>De catalogus spreekt geen Nederlands — dit zoekveld wel</h2>
  <p>Zelfde meting als op hipobuy.es: lokale woorden → lege grid; sneakers/hoodie → kaarten. Typ Nederlands, wij sturen het Engelse indexwoord.</p>
  {translator_widget(key)}
  {nine_states(key)}
  <h2>Nederland heeft lijnen, niet allemaal beschikbaar</h2>
  <p>Op 29&nbsp;sep&nbsp;2026, 1000&nbsp;g / 35×25×10&nbsp;cm, bestemming NL: <strong>{d['lines']} lijnen</strong>. Goedkoopste carriable <code>{d['cheap']}</code> ± ${d['usd']:.2f} ({d['days']} dagen, vaak 1100&nbsp;g volume). Snapshot, geen checkout. SURFACE 60–90 werkdagen is een andere beslissing dan DHL-EUCR.</p>
  {fig(SHOT_EST, "Officieel schattingsformulier, eigen opname 30 sep 2026. Kies Netherlands, niet EU.")}
  <p>Volumgewicht L×B×H/8000. 35×25×10 cm = 8750 cm³ → 1100&nbsp;g op de meeste luchtlijnen.</p>
  <h2>Invoer — alleen uitleg</h2>
  <div class="box">
    <p>Tax free / Prepaid Duty / Duties Payable by Recipient. Bronnen: <a href="{d['customs']}">Belastingdienst Douane</a> · <a href="{d['ioss']}">IOSS</a>. <strong>Geen onderwaardering.</strong></p>
  </div>
  <p>USD-cijfers, euro-symbool. Invite {INVITE} op de coupon-URL, niet in deze title. Tabak, alcohol, geneesmiddelen reizen niet. Restricted-kaarten zonder prijs niet bestellen. Als de schatting lichter uitvalt dan de factuur, staat de officiële FAQ over portoteruggave — niet dit HTML-bestand.</p>
  <p>Hulp voor de eerste bestelling: vijftien vragen, nieuws met datum, en de labtabel. Discord en Reddit zijn kanalen van de platform, niet van deze desk. {contact_block('nl')}</p>
  <p><a href="/{s['help']}/">Hulp</a> · <a href="/{s['news']}/">Nieuws</a> · <a href="/{s['about']}/">Over ons</a></p>
  <p><a class="cta" href="{OFFICIAL}">HipoBuy openen, daarna een NL-adres</a></p>
"""
    else:
        flavour = {"uk": "uk", "eu": "eu", "us": "us", "ukhaul": "haul"}[key]
        if flavour == "uk":
            title = "HipoBuy UK spreadsheet: coupons, UK sizing, then the estimator"
            desc = (
                "Independent .co.uk desk: what a purchasing agent is, English catalogue index, "
                "HMRC sources, coupons. No declared-value coaching."
            )
            h1 = "Working coupons and UK sizing before you submit"
            job_p = (
                f"This host ranks <a href=\"/hipobuy-coupons/\">coupons</a> and "
                f"<a href=\"/blog/posts/hipobuy-sizing-guide/\">UK sizing</a>. "
                f"Haul-log freight dollars live on hipobuyspreadsheets.uk — not a 301. "
                f"On 29 Sep 2026 the exclusive invite card still showed <code>{INVITE}</code>."
            )
            tax_box = (
                f'UK import VAT/duty follow the booked SKU. <a href="{d["customs"]}">GOV.UK goods sent from abroad</a>. '
                "Northern Ireland is often another product. <strong>No declared-value coaching.</strong>"
            )
            lab_p = (
                f"GB lab carton 29 Sep 2026 lives on the haul-log shipping URL: "
                f"<code>{d['cheap']}</code> about ${d['usd']:.2f}. Re-run <a href=\"{EST}\">the estimator</a> with destination United Kingdom."
            )
        elif flavour == "eu":
            title = "HipoBuy EU coupon desk: member-state address, then the invite"
            desc = (
                "Independent .eu coupon desk. IOSS is a SKU. Catalogue search maps ES/FR/DE words to English. "
                "Not a clone of hipobuy.es."
            )
            h1 = "Put a member-state address in HipoBuy, then re-type the invite"
            job_p = (
                f"The TLD is not a destination. Open the coupon article, copy <code>{INVITE}</code>, "
                "enter it in-app. Spain freight copy stays on hipobuy.es. AT/NL keep their own labs."
            )
            tax_box = (
                f'Pick a country in the estimator. <a href="{d["ioss"]}">Commission VAT e-commerce / IOSS</a> '
                "(often discussed around €150). <strong>No declared-value coaching.</strong>"
            )
            lab_p = (
                f"There is no “EU” line table. On 29 Sep 2026 we measured AT/NL/GB/US as country codes. "
                f'Open <a href="{EST}">{EST}</a> with ES, IE, IT…'
            )
        elif flavour == "us":
            title = "HipoBuy US: warehouse photos, then a United States estimate"
            desc = (
                "Independent US desk: purchasing-agent flow, USPS/integrator lab 29 Sep 2026, CBP sources. "
                "No under-declaration tips."
            )
            h1 = "Shipping to the United States after warehouse photos"
            job_p = (
                f"Wait for QC photos, then estimate a US street — not an AT Post article. "
                f"Lab carton 29 Sep 2026: <code>{d['cheap']}</code> about ${d['usd']:.2f} "
                f"({d['days']} workdays, billed actual 1000&nbsp;g). Integrator SKUs billed volumetric 1100–2000&nbsp;g on the same carton."
            )
            tax_box = (
                f'US treatment follows the booked product. <a href="{d["customs"]}">CBP duty basics</a>. '
                "This desk does not invent a de-minimis dollar figure. <strong>No under-declaration tips.</strong>"
            )
            lab_p = f'Open <a href="{EST}">the estimator</a> with destination United States after photos.'
        else:
            title = "HipoBuy UK haul log: Royal Mail, Evri, then the spreadsheet"
            desc = (
                "Independent Nominet haul log. GB estimator snapshot 29 Sep 2026, GOV.UK sources. "
                "Not an alias of hipobuyspreadsheet.co.uk."
            )
            h1 = "UK haul log: shipping lines and the spreadsheet"
            job_p = (
                f"Line codes after warehouse photos, then the spreadsheet of what shipped. "
                f"Lab: <code>{d['cheap']}</code> about ${d['usd']:.2f}; Evri-AF1 about $33.88. "
                "Not a 301 onto .co.uk."
            )
            tax_box = (
                f'<a href="{d["customs"]}">GOV.UK goods sent from abroad</a>. Northern Ireland is often another SKU. '
                "<strong>No declared-value coaching.</strong>"
            )
            lab_p = f'Open <a href="{EST}">the estimator</a> with destination United Kingdom.'
        inner = f"""
  <h1>{h1}</h1>
  <p>HipoBuy <strong>does not sell the items</strong>. It is a purchasing agent: it buys from third-party Chinese shops in your name, photographs in the warehouse, and books an international line after you confirm QC. Two payments. {job_p}</p>
  {fig(SHOT_OFF, "Official hipobuy.com home, own capture 30 Sep 2026. English/USD is the platform default — not this desk’s job.")}
  <p>
    <a class="cta" href="{EST}">{L['est']}</a>
    <a class="cta" href="/{s['help']}/">Fifteen questions</a>
  </p>
  <h2>A spreadsheet here is a catalogue of cards</h2>
  <p>Not Excel. Finds with thousands of rows stay on <a href="{NET}">hipobuyspreadsheet.net</a>. Sister desks keep their own files; no 301.</p>
  {fig(SHOT_CAT, "Catalogue grid on a country desk, own capture 30 Sep 2026. English index words fill the cards.")}
  <h2>Catalogue language</h2>
  <p>The index is English. Local words (zapatillas, Turnschuhe, trainers) often return zero. Type the local word; we send the English key to <a href="/hipobuy-spreadsheet/">/hipobuy-spreadsheet/</a> where that host has a grid.</p>
  {translator_widget(key)}
  {nine_states(key)}
  <h2>Lines, volumetric weight, USD digits</h2>
  <p>{lab_p} Volumetric L×W×H/8000 on most air SKUs. Lab carton 35×25×10 cm billed 1100&nbsp;g on many lines. Switching the official currency selector has been observed to change the symbol without converting the number.</p>
  {fig(SHOT_EST, "Official estimator form, own capture 30 Sep 2026. Destination must be a country, not a TLD.")}
  <h2>Customs — educational</h2>
  <div class="box"><p>{tax_box}</p></div>
  <p>Tobacco, alcohol, medicines, banned goods do not travel. Restricted or zero-price cards are not buyable. If billed weight is lighter than estimated, official FAQ covers excess postage — not this HTML file. Discord and Reddit belong to the platform.</p>
  <p>USD digits stay dollars when the official selector only changes the symbol. Invite {INVITE} lives on the coupon URL, not in this title.</p>
  <p><a href="/{s['help']}/">Help</a> · <a href="/{s['news']}/">Dated news</a> · <a href="/{s['about']}/">Who we are</a></p>
  <p><a class="cta" href="{OFFICIAL}">Open HipoBuy, then a real address in-app</a></p>
"""
    return shell_page(
        key,
        d,
        title=title,
        desc=desc,
        canonical=f"https://{host}/",
        crumb=L["home"],
        inner=inner,
    )


def shipping_essay(key: str, d: dict) -> str:
    """ES /envios-style customs essay inserted before the calculator."""
    from hipobuy_desk_copy import DATE, lab_block

    extra_lab = ""
    if key == "uk" and d.get("dest") == "GB":
        extra_lab = lab_block(
            "GB",
            "United Kingdom",
            "Cheapest carriable on the lab day: HIPO-RoyalMail-GB-1 about $23.83. This .co.uk host still ranks coupons; the table is here so GBP landed cost is not a surprise.",
        )
    shot = fig(
        SHOT_EST,
        {
            "at": "Offizieller Schätzer, eigene Aufnahme 30 Sep 2026. Ziel Austria wählen — nicht Germany, nicht EU.",
            "nl": "Officiële estimator, eigen opname 30 sep 2026. Bestemming Netherlands, niet EU.",
            "uk": "Official estimator, own capture 30 Sep 2026. Destination United Kingdom.",
            "eu": "Official estimator, own capture 30 Sep 2026. Pick a member-state country code, not EU.",
            "us": "Official estimator, own capture 30 Sep 2026. Destination United States.",
            "ukhaul": "Official estimator, own capture 30 Sep 2026. Destination United Kingdom; NI may differ.",
        }[key],
    )
    if key == "at":
        body = f"""
<h2 class="ph" id="zoll">Zoll und MwSt — drei Modi, nur Erklärung</h2>
<p class="pp">Wer Abgaben zahlt, steht auf der Live-SKU. Der Schätzer markiert Linien auf Englisch:</p>
<h3 class="ph">Tax free</h3>
<p class="pp">Die Linie wird als ohne Abgaben für den Empfänger verkauft. Die Zollstelle darf trotzdem prüfen. Es verschwindet nicht das Verfahren, nur wer es trägt.</p>
<h3 class="ph">Prepaid Duty</h3>
<p class="pp">Du zahlst die Abgaben mit dem Porto. Der Betrag steht vor dem Versand, nicht an der Haustür.</p>
<h3 class="ph">Duties Payable by Recipient</h3>
<p class="pp">Günstigerer Listenpreis, weil Abgaben fehlen. Der Zusteller kann vor der Übergabe kassieren, oft plus Bearbeitungsgebühr, die der Schätzer nicht zeigt. Vergleiche nur Linien desselben Modus.</p>
<p class="pp">EU-Orientierung oft 150&nbsp;€ IOSS für bestimmte Fernverkäufe. Darüber können Zölle greifen. Konkrete Sätze stehen nicht in dieser HTML. <a href="{d["customs"]}">BMF Zoll</a> · <a href="{d["ioss"]}">IOSS / Kommission</a>. HipoBuy veröffentlicht zusätzlich eine eigene Schwellen-Tabelle und kennzeichnet sie als aus dem Internet gesammelt und nur orientierend — wir kopieren daraus keine erfundenen Euro-Beträge. <strong>Keine Unterdeklaration.</strong></p>
<h2 class="ph">Volumengewicht am Laborkarton</h2>
<p class="pp">35×25×10&nbsp;cm = 8750&nbsp;cm³. Durch 8000 = 1,094&nbsp;kg, auf den meisten AT-Luftlinien 1100&nbsp;g. Istgewicht war 1000&nbsp;g. Es zählt das Maximum. Der Rechner darunter macht nur die Volumen-Rechnung; den Preis kennt nur der offizielle Schätzer am Büchertag.</p>
<h2 class="ph">Verpackung und Bündeln</h2>
<p class="pp">Schuhkarton entfernen, Folie, Vakuumbeutel: die App listet kostenlose und kostenpflichtige Optionen. Einmal gepackt sind Materialkosten oft nicht erstattbar. Mehrere Bestellungen in einem Karton sparen das Anfangsgewicht — solange nichts als Einzelsendung markiert ist. Ab etwa 10&nbsp;kg wirkt ein Karton kommerzieller; das ist Erklärung, kein Trick.</p>
<p class="pp">USD-Ziffern: Währungsschalter ändert oft nur das Symbol. {shot}</p>
<p class="pp"><a href="/hilfe/">Hilfe</a> · <a href="/neuigkeiten/">Neuigkeiten</a> · <a href="/ueber-uns/">Über uns</a> · <a href="mailto:{MAIL}">{MAIL}</a></p>
"""
    elif key == "nl":
        body = f"""
<h2 class="ph" id="douane">Btw en douane — drie modi, alleen uitleg</h2>
<p class="pp">Invoer volgt de geboekte lijn. Labels in de estimator:</p>
<h3 class="ph">Tax free</h3>
<p class="pp">Verkocht als zonder invoer voor de ontvanger. De douane mag nog controleren.</p>
<h3 class="ph">Prepaid Duty</h3>
<p class="pp">Je betaalt invoer bij het porto. Totaal vóór vertrek.</p>
<h3 class="ph">Duties Payable by Recipient</h3>
<p class="pp">Lagere lijstprijs omdat invoer ontbreekt. Last-mile kan innen plus behandelingsfee. Vergelijk alleen hetzelfde modus.</p>
<p class="pp"><a href="{d["customs"]}">Belastingdienst Douane</a> · <a href="{d["ioss"]}">IOSS</a>. HipoBuy heeft zelf een drempeltabel die het als internet-compilatie en slechts indicatief labelt — wij verzinnen daar geen eurobedragen bij. <strong>Geen onderwaardering.</strong></p>
<h2 class="ph">Volumgewicht</h2>
<p class="pp">35×25×10 cm = 8750 cm³ / 8000 ≈ 1,094 kg, op de meeste NL-luchtlijnen 1100&nbsp;g tegen 1000&nbsp;g echt. De rekenmachine hieronder doet alleen die som; de prijs staat in de officiële estimator.</p>
<h2 class="ph">Verpakking en bundelen</h2>
<p class="pp">Schoenendoos eraf, folie, vacuüm: de app scheidt gratis en betaalde opties. Eenmaal ingepakt zijn materiaalkosten vaak niet terug. Bundelen spaart het startgewicht. Vanaf ongeveer 10 kg oogt een doos commerciëler voor de douane — uitleg, geen truc. PostNL of DHL moet op de live-SKU staan, niet alleen „goedkope lijn“. {shot}</p>
<p class="pp"><a href="/hulp/">Hulp</a> · <a href="/nieuws/">Nieuws</a> · <a href="mailto:{MAIL}">{MAIL}</a></p>
"""
    elif key == "us":
        body = f"""
<h2 class="ph" id="cbp">CBP — three SKU labels, educational</h2>
<p class="pp">US treatment follows the booked product. Read Tax free / Prepaid Duty / Duties Payable by Recipient the morning you book. This desk does not invent a de-minimis dollar figure — HipoBuy’s own threshold table is labelled indicative.</p>
<h3 class="ph">Tax free</h3>
<p class="pp">Marketed as no duty for the recipient. CBP can still inspect.</p>
<h3 class="ph">Prepaid Duty</h3>
<p class="pp">Duties collected with freight.</p>
<h3 class="ph">Duties Payable by Recipient</h3>
<p class="pp">Last-mile may collect before delivery, plus a handling fee the estimator omits.</p>
<p class="pp"><a href="{d["customs"]}">CBP duty overview</a>. HipoBuy’s own destination-threshold table is labelled as gathered from the internet and indicative — we do not copy a dollar de-minimis into this HTML. <strong>No under-declaration tips.</strong></p>
<h2 class="ph">Volumetric weight</h2>
<p class="pp">Lab carton 1000&nbsp;g / 35×25×10&nbsp;cm: USPS-ZF1 billed actual 1000&nbsp;g; some integrator SKUs billed 1100–2000&nbsp;g volumetric on the same carton. The calculator below only does L×W×H/8000; live dollars sit in the official estimator.</p>
<h2 class="ph">Packing and consolidation</h2>
<p class="pp">Shoe-box removal and wrap options are in-app, some free with limits. After pack, material fees often do not refund. Consolidation saves the first-weight band. Around 10 kg a carton starts to look commercial. {shot}</p>
<p class="pp"><a href="/help/">Help</a> · <a href="/news/">News</a> · <a href="mailto:{MAIL}">{MAIL}</a></p>
"""
    elif key == "eu":
        body = f"""
<h2 class="ph" id="ioss">VAT / IOSS — educational, not a TLD</h2>
<p class="pp">The estimator needs a member-state country code. IOSS is a SKU. The Commission explains the import one-stop shop for certain low-value distance sales (often around €150). Above that, customs duty can apply. Spain-only line copy belongs on hipobuy.es.</p>
<h3 class="ph">Tax free</h3>
<p class="pp">Does not delete the right of customs to inspect.</p>
<h3 class="ph">Prepaid Duty</h3>
<p class="pp">Paid with freight.</p>
<h3 class="ph">Duties Payable by Recipient</h3>
<p class="pp">Last-mile may collect, plus fees the estimator hides.</p>
<p class="pp"><a href="{d["ioss"]}">European Commission VAT e-commerce</a>. HipoBuy’s own EU row in its threshold table is labelled indicative. We do not invent rates. <strong>No declared-value coaching.</strong></p>
<h2 class="ph">Volumetric weight</h2>
<p class="pp">Same lab carton as AT/NL/GB: 35×25×10 cm often bills 1100&nbsp;g at /8000. There is no EU destination code — pick ES, IE, IT… Spain-only line counts stay on hipobuy.es.</p>
<h2 class="ph">Packing and consolidation</h2>
<p class="pp">Packing options and warehouse storage limits are official-help facts and can change. Consolidation saves first-weight; a 10 kg carton can look commercial. IOSS/fiscal treatment is still a SKU you read the morning you book, not a reason to clone hipobuy.es here. {shot}</p>
<p class="pp"><a href="/help/">Help</a> · <a href="/news/">News</a> · <a href="mailto:{MAIL}">{MAIL}</a></p>
"""
    else:
        ni = " Northern Ireland is often another carrier product." if key == "ukhaul" else " This .co.uk host still ranks coupons; haul-log dollars live on hipobuyspreadsheets.uk."
        body = f"""
<h2 class="ph" id="hmrc">HMRC — three SKU labels, educational</h2>
<p class="pp">UK import VAT/duty follow the carrier SKU.{ni}</p>
<h3 class="ph">Tax free</h3>
<p class="pp">Marketed as no extra collection at the door. HMRC can still inspect.</p>
<h3 class="ph">Prepaid Duty</h3>
<p class="pp">Duties with freight.</p>
<h3 class="ph">Duties Payable by Recipient</h3>
<p class="pp">A cheaper list price is not a cheaper landed cost if last-mile collects.</p>
<p class="pp"><a href="{d["customs"]}">GOV.UK goods sent from abroad</a>. HipoBuy’s own UK threshold row is labelled indicative. <strong>No declared-value coaching.</strong></p>
<h2 class="ph">Volumetric weight</h2>
<p class="pp">Lab carton 35×25×10 cm often billed 1100&nbsp;g on Royal Mail / Evri air SKUs. 1000&nbsp;g actual still loses to volume on many lines. The calculator below is geometry, not a checkout quote.</p>
<h2 class="ph">Packing and consolidation</h2>
<p class="pp">Shoe-box removal can drop billed weight when volume leads; it does nothing when actual weight already wins. After pack, material fees often stay. Evri versus Royal Mail is a last-mile reading on the live SKU, not a homepage slogan. {shot}</p>
<p class="pp"><a href="/help/">Help</a> · <a href="/news/">News</a> · <a href="mailto:{MAIL}">{MAIL}</a></p>
"""
    est_p = (
        f'<p class="pp"><a href="{EST}">Open the official HipoBuy estimator</a> with this country selected '
        f"before you pay international freight. The table above is a snapshot from {DATE}, not checkout. "
        "USD digits stay dollars when the official selector only changes the symbol.</p>"
        if d.get("dest")
        else (
            f'<p class="pp">The estimator needs a <strong>member-state country code</strong>, not “EU”. '
            f'Open <a href="{EST}">{EST}</a>.</p>'
        )
    )
    return extra_lab + est_p + body
