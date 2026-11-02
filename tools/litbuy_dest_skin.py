"""Official LitBuy chrome for dest country sites.

Public pages: no ops notes. Images from litbuy.com shots. Local language + currency.
White sticky header + official yellow #FFC800 CTAs (litbuy.com). Does not smash
unique coupons/legit/invite CMS.
"""
from __future__ import annotations

import json
import re
import shutil
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MEDIA_SRC = ROOT / "sites" / "shared" / "litbuy-media"
OFF = "https://litbuy.com/"
EST = "https://litbuy.com/shipping-estimate"
HELP = "https://litbuy.com/"
W2C_SHEET = "https://w2clinks.com/spreadsheet/litbuy/"
W2C_SEARCH = "https://w2clinks.com/spreadsheet/"

SHOT_HOME = "/media/oficial-inicio.jpg"
SHOT_EST = "/media/estimator-uk.jpg"
SHOT_DIY = "/media/oficial-diy.jpg"
SHOT_GIF = "/media/official-home.jpg"


def shot_est(d: dict) -> str:
    key = d.get("key") or ""
    return {
        "uk": "/media/estimator-uk.jpg",
        "nl": "/media/estimator-nl.jpg",
        "us": "/media/estimator-us.jpg",
        "at": "/media/estimator-at.jpg",
        "au": "/media/estimator-au.jpg",
        "ca": "/media/estimator-ca.jpg",
        "fr": "/media/estimator-fr.jpg",
        "es": "/media/estimator-es.jpg",
        "de": "/media/estimator-de.jpg",
        "it": "/media/estimator-it.jpg",
    }.get(key, SHOT_EST)

CATS = [
    ("sneakers", "sneakers.png"),
    ("hoodie", "hoodie.png"),
    ("jacket", "jacket.png"),
    ("t-shirt", "t-shirt.png"),
    ("pants", "pants.png"),
    ("bag", "bag.png"),
    ("watch", "watch.png"),
    ("hat", "hat.png"),
    ("glasses", "glasses.png"),
    ("jewelry", "jewelry.png"),
    ("shirt", "shirt.png"),
    ("electronics", "electronics.png"),
]
CAT_SRC = {
    "sneakers.png": "cat-30-shoes.png",
    "hoodie.png": "cat-06-hoodie.png",
    "jacket.png": "cat-18-jacket.png",
    "t-shirt.png": "cat-03-t-shirt.png",
    "pants.png": "cat-19-trousers.png",
    "bag.png": "cat-00-bag.png",
    "watch.png": "cat-32-watch.png",
    "hat.png": "cat-01-hat.png",
    "glasses.png": "cat-31-glasses.png",
    "jewelry.png": "cat-02-jewelry.png",
    "shirt.png": "cat-05-shirt.png",
    "electronics.png": "cat-electronics.png",
}

UNIQUE_DIR = {
    h: {
        "litbuy-coupon", "litbuy-coupons",
        "is-litbuy-legit", "is-litbuy-safe",
        "litbuy-qc-guide", "litbuy-refund-guide",
        "litbuy-shoes-spreadsheet", "litbuy-spreadsheet-2026",
        "litbuy-community", "litbuy-invite-code",
        "litbuy-freight", "litbuy-haul", "litbuy-announcements",
        "best-litbuy-spreadsheet", "litbuy-spreadsheets",
        "gst-import-australia", "litbuy-shipping-australia",
        "de-minimis-us-litbuy", "cbp-declared-value-us", "litbuy-shipping-times-us",
        "vat-on-imports-uk-2026", "royal-mail-customs-uk",
        "cbsa-import-canada", "gst-landed-cost-canada", "litbuy-shipping-canada",
        "aduana-iva-espana", "guias-comprador-es",
        "btw-import-nederland", "kaeuferguides-at", "zoll-einfuhr-oesterreich",
        "ioss-import-vat-eu", "ecommerce-vat-reform-eu",
        "litbuy-review",
        "affiliate-disclosure", "partner-disclosure",
        "privacy-policy", "cookie-policy", "refund-policy", "contact", "terms",
        "category", "blog",
    }
    for h in ("litbuy.at", "litbuyspreadsheet.it", "litbuyspreadsheets.ca", "litbuyspreadsheets.us", "litbuyspreadsheet.me.uk", "litspreadsheet.fr", "litbuyspreadsheets.es", "litbuyspreadsheets.nl")
}
_EXTRA_UNIQUE = {
    "post-at-sendungsverfolgung", "zoll-ust-oesterreich", "ratgeber-oesterreich",
    "dsgvo-litbuy-oesterreich", "ist-litbuy-serioes",
    "gst-hst-import-canada", "canada-post-customs", "ca-buyer-guides",
    "dogana-poste-italiane", "iva-importazione-italia", "guide-italia",
    "duties-taxes-usps-fedex", "us-customs-declaration-guide",
    "hmrc-import-charges-uk", "litbuy-shipping-uk",
    "livraison-litbuy-france", "tva-import-france", "colissimo-douane-france",
    "aduana-correos-espana", "iva-importacion-espana", "guias-espana",
    "douane-nederland-dhl", "litbuy-verzendkosten-nederland", "ideal-betalen-litbuy",
    "what-is-litbuy", "how-to-use-litbuy", "spreadsheet", "guides",
}
for _h in UNIQUE_DIR:
    UNIQUE_DIR[_h].update(_EXTRA_UNIQUE)

CSS = """
<style id="litbuy-official-skin">
:root{--acc:#FFC800;--acd:#C49200;--link:#C49200;--primary:#FFC800;--primary-dark:#C49200;--primary-soft:#fff8e1;--ink:#303133;--mute:#8492b2;--dark:#181818;--line:#eaecf0}
body{background:#fff;font-family:"Microsoft Yahei","PingFang SC",Avenir,"Segoe UI","Hiragino Sans GB",Inter,ui-sans-serif,system-ui,sans-serif;color:var(--ink)}
.cb-promo{background:#181818;color:#fff;text-align:center;padding:8px 14px;font-weight:600;font-size:13px}
.cb-promo a{color:#fff;text-decoration:none}
.hdr-login,.btn-primary,.cb-login{display:inline-flex;align-items:center;min-height:36px;padding:0 16px;border-radius:999px;background:#FFC800;color:#181818;font-size:14px;font-weight:700;text-decoration:none;border:0}
.hdr-login:hover,.btn-primary:hover{background:#C49200;color:#181818}
.btn-outline,.btn-cart{display:inline-flex;align-items:center;min-height:36px;padding:0 16px;border-radius:999px;background:#fff;color:#C49200;border:1px solid #eaecf0;text-decoration:none;font-weight:700;font-size:14px}
header.top,header.cb-head{position:sticky;top:0;z-index:50;background:#fff;border-bottom:1px solid #eaecf0}
.cluster-nav{display:flex;flex-wrap:wrap;gap:8px 14px;align-items:center;margin:12px 0 8px;font-size:14px;font-weight:600}
.cb-head-inner,.top .wrap{width:min(1120px,calc(100% - 28px));margin:0 auto;display:flex;align-items:center;gap:12px;min-height:72px;flex-wrap:wrap}
.cb-head-left,.nav{display:flex;align-items:center;gap:4px;flex-wrap:wrap;margin-left:auto}
.cb-head-left a,.nav a{color:#333;text-decoration:none;padding:0 12px;min-height:44px;display:inline-flex;align-items:center;border-radius:12px;font-size:15px;font-weight:600}
.cb-head-left a:hover,.nav a:hover,.cb-head-left a.on,.nav a[aria-current]{color:#C49200}
.cb-logo img,.brand img{height:32px;width:auto;display:block}
.cb-ccy{color:#8492b2;font-size:13px;font-weight:600}
.cb-head-search{display:flex;gap:8px;margin:0 auto 14px;background:#fff;border:2px solid #FFC800;border-radius:999px;padding:6px 6px 6px 18px;align-items:center;width:min(1100px,calc(100% - 28px))}
.cb-head-search input{flex:1;border:0;outline:none;font-size:15px;background:transparent}
.cb-head-search .btn{background:#FFC800;color:#181818;border-radius:999px;min-width:96px;border:0;font-weight:700;cursor:pointer;padding:8px 16px}
.cb-hero{position:relative;border-radius:0;overflow:hidden;min-height:420px;margin:0 0 8px;background:#181818}
.cb-hero-bg{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;filter:brightness(.42);object-position:center top}
.cb-hero::after{content:"";position:absolute;inset:0;background:linear-gradient(100deg,rgba(24,24,24,.72) 0%,rgba(17,17,17,.38) 100%);z-index:0}
.cb-hero-copy{position:relative;z-index:1;padding:74px 36px 78px;color:#fff;max-width:760px;width:min(1120px,calc(100% - 28px));margin:0 auto}
.cb-hero-copy h1{color:#fff;font-size:clamp(28px,4.4vw,45px);letter-spacing:-.02em;margin:0 0 12px}
.cb-hero-copy .hsub{color:#f4f4f4;font-size:19px;max-width:640px}
.cb-search{display:flex;gap:8px;margin:22px 0 10px;background:#fff;border-radius:999px;padding:8px 8px 8px 18px;align-items:center;max-width:660px}
.cb-search input{flex:1;border:0;outline:none;font-size:17px;background:transparent}
.cb-search .btn{border-radius:999px;min-width:110px;border:0;cursor:pointer;font:inherit;background:#FFC800;color:#181818;font-weight:700;min-height:44px;padding:0 24px}
.cb-hero .cluster-nav a{color:#fff}
.cb-hero .eu-badge{background:#FFC800;color:#181818;display:inline-block;border-radius:999px;padding:4px 10px;font-size:12px;font-weight:700}
.cb-steps{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;margin:18px auto;width:min(1120px,calc(100% - 28px))}
@media(max-width:800px){.cb-head-inner{text-align:center}.cb-steps{grid-template-columns:1fr}.cb-hero-copy{padding:36px 18px}}
.cb-step{background:#fff;border-radius:16px;padding:18px;border:1px solid #eaecf0}
.cb-step strong{display:block;color:#C49200;font-size:13px;margin-bottom:6px}
.sg-split{display:grid;grid-template-columns:1.05fr .95fr;gap:22px;align-items:start}
@media(max-width:860px){.sg-split{grid-template-columns:1fr}}
figure.shot{margin:0}
figure.shot img{width:100%;border-radius:14px;border:1px solid #eaecf0;display:block;background:#fff}
figure.shot figcaption{font-size:13px;color:#8492b2;margin-top:8px}
.sg-cats{display:grid;grid-template-columns:repeat(auto-fill,minmax(150px,1fr));gap:12px}
.sg-cat{padding:0;overflow:hidden;border:1px solid #eaecf0;border-radius:18px;text-decoration:none;color:inherit;background:#fff}
.sg-cat img{width:100%;aspect-ratio:1;object-fit:cover;display:block;background:#f5f6f7}
.sg-cat .b{padding:10px 12px}
.cluster-page{max-width:820px}
.cluster-nav a{color:#C49200}
.site-footer,.cb-foot,.site-ft{background:#111;color:#ccc;margin-top:36px;padding:52px 0 30px;font-size:15.5px}
.cb-foot a,.site-ft a{color:#c2c2c2;text-decoration:none}
.cb-foot-grid,.ft-grid{width:min(1120px,calc(100% - 28px));margin:0 auto;display:grid;grid-template-columns:repeat(3,1fr);gap:34px}
@media(max-width:800px){.cb-foot-grid,.ft-grid{grid-template-columns:1fr 1fr}}
.cb-foot h3,.site-ft h3{color:#fff;font-size:15.5px;margin:0 0 12px}
.cb-foot ul{margin:0;padding:0;list-style:none}
.cb-pay{display:flex;flex-wrap:wrap;gap:8px;margin-top:10px}
.cb-pay span{background:#fff;color:#111;border-radius:6px;padding:4px 8px;font-size:11px;font-weight:800}
.local-steps{display:grid;gap:14px;padding:0;margin:16px 0 0;list-style:none}
.local-steps li{display:grid;gap:4px}
.local-steps strong{display:block}
#lang-modal,.lmo,.lbk,.waf,.lmi,.lmh,.lgr,.lcf,#lang-grid,#curr-grid{display:none!important}
</style>
"""

OPS_RX = [
    r"Lab \d+ Sep 2026\.?\s*",
    r"Lab \d+ Oct 2026\.?\s*",
    r"Copy reviewed \d+ Oct 2026\.?\s*",
    r"Measured \d+ Oct 2026[^.]*\.\s*",
    r"Gemeten \d+ Oct 2026[^.]*\.\s*",
    r"Gemessen \d+ Oct 2026[^.]*\.\s*",
    r"Medido \d+ Oct 2026[^.]*\.\s*",
    r"Lo medimos el \d+ Oct 2026\.?\s*",
    r"Sister country hosts stay separate files — no 301\.?\s*",
    r"Schwesterdesks bleiben eigene Dateien — kein 301\.?\s*",
    r"Independent desk — not the official app, not checkout\.?\s*",
    r"Independent information desk[^.]*\.\s*",
    r"escritorio informativo independiente[^.<]{0,80}",
    r"this HTML is not checkout\.?\s*",
    r"Not checkout\.?\s*",
    r"No declared-value coaching\.?\s*",
    r"Sin infradeclaración\.?\s*",
    r"not a location-name swap\.?\s*",
    r"not a second brand hub\.?\s*",
    r"local-intent desk[^.<]{0,80}",
    r"Freight lab — not checkout",
    r"Already ranking on this host",
    r"<!--\s*/?portfolio-step4[^>]*-->",
    r"<!-- DEPLOY GUARD:[^>]*-->",
    r"DEPLOY GUARD:[^<]*",
    r"Official LitBuy estimator URL redirected to login[^.]*\.\s*",
    r"This desk does not invent a free-day count\.?\s*",
    r'<p[^>]*class="[^"]*hub-uplink[^"]*"[^>]*>[\s\S]*?</p>',
    r"pas un simple changement de nom\.?\s*",
    r"on ne le remplace pas par un texte[^.<]{0,80}",
    r"not a simple name swap\.?\s*",
    r"this HTML is not a till\.?\s*",
    r"Coupon desk on \.co\.uk[^.]*\.\s*",
    r"Independent \.co\.uk coupon desk[^.]*\.\s*",
    r"Geen onderwaardering\.?\s*",
    r"Keine Unterdeklaration\.?\s*",
    r"Independent SEO guide[^.<]{0,120}",
    r"kein Ortsnamen-Tausch\.?\s*",
    r"Labor 2 Oct 2026\.?\s*",
    r"O4K87NHKR",
    r"Independent SEO guide[^.<]{0,80}",
    r"kein Ortsnamen-Tausch\.?\s*",
    r"Labor 2 Oct 2026\.?\s*",
    r"Copy reviewed 2 Oct 2026\.?\s*",
    r"O4K87NHKR",
    r"this HTML is not checkout[^.]*\.\s*",
    r"Live money is in[^.<]{0,120}",
    r"VGEICZNX0",
    r"inviteCode=[A-Za-z0-9]+",
]


def chrome(d: dict) -> dict:
    key = d["key"]
    ccy = d["ccy"]
    label = d["label"]
    en = {
        "home": "Home",
        "sheet": "Spreadsheet",
        "ship": "Shipping",
        "help": "Help",
        "reg": "Log in to LitBuy",
        "login": "Login",
        "cart": "Cart",
        "promo": "Shop from China on litbuy.com — register before you paste a link.",
        "est": "Shipping Calculator",
        "custom": "How To Buy",
        "lang": "English",
        "search": "Enter the product name/link",
        "submit": "Search",
        "sub": f"Shop from China's e-commerce with a delivery address in {label}. Prices on this page are shown in {ccy}.",
        "s1t": "Place orders",
        "s1": "Paste a Taobao, 1688 or Weidian link on litbuy.com.",
        "s2t": "QC in the warehouse",
        "s2": "Warehouse photos before you book international freight.",
        "s3t": "Ship to your door",
        "s3": f"Choose a line with destination {label}. Last mile is often {d['post']}.",
        "shots": "How LitBuy works",
        "cap_home": "LitBuy home — paste a product link to start.",
        "cap_est": f"Shipping calculator. Set destination to {label} before you pay freight.",
        "cap_diy": "Register or log in on litbuy.com to pay in the official app.",
        "local": f"Delivery to {label}",
        "faq": "Questions",
        "cs": "Customer Service",
        "pay": "Payment",
        "guide": "Shopping Agent Guidance",
        "copy": f"LitBuy spreadsheet for {label}. Display currency {ccy}. Orders on litbuy.com.",
        "local_h2": f"Delivery to {label}",
        "loc1t": "Estimator country",
        "loc1": f"Open the calculator and set destination {label} before you pay freight. {d['city']}.",
        "loc2t": "Address",
        "loc2": f"Use a street and {d['city']}. Register and pay on litbuy.com.",
        "loc3t": "Import charges",
        "loc3": f"The booked SKU decides prepaid vs collect. Source: {d['customs']} — {d['customs_url']}.",
        "loc4t": "Last mile",
        "loc4": f"Often {d['post']} after you accept warehouse photos.",
    }
    packs = {k: dict(en) for k in ("uk", "us", "ca", "au")}
    packs["au"]["sub"] = f"Shop from China's e-commerce with an Australian postcode. Prices on this page are shown in {ccy}."
    packs["au"]["lang"] = "English"
    packs["us"]["sub"] = f"Shop from China's e-commerce with a US ZIP. Prices on this page are shown in {ccy}."
    packs["ca"]["sub"] = f"Shop from China's e-commerce with a Canadian postal code. Prices on this page are shown in {ccy}."
    packs["de"] = {
        **en,
        "home": "Start",
        "ship": "Versand",
        "help": "Hilfe",
        "reg": "Bei LitBuy anmelden",
        "cart": "Warenkorb",
        "promo": "Bestellen auf litbuy.com — zuerst registrieren, dann den Link einfügen.",
        "est": "Fracht schätzen",
        "custom": "So kaufen",
        "lang": "Deutsch",
        "search": "Produktname oder Link",
        "submit": "Suchen",
        "sub": f"Aus Chinas Shops nach {label} bestellen. Preise auf dieser Seite in {ccy}.",
        "s1t": "Bestellen",
        "s1": "Taobao-, 1688- oder Weidian-Link auf litbuy.com einfügen.",
        "s2t": "QC im Lager",
        "s2": "Lagerfotos, bevor du die internationale Fracht buchst.",
        "s3t": "Zur Haustür",
        "s3": f"Linie mit Ziel {label}. Letzte Meile oft {d['post']}.",
        "shots": "So sieht LitBuy aus",
        "cap_home": "LitBuy-Startseite — Link einfügen und bestellen.",
        "cap_est": f"Fracht-Rechner. Ziel {label} wählen, bevor du Porto zahlst.",
        "cap_diy": "Auf litbuy.com registrieren oder anmelden.",
        "local": f"Lieferung nach {label}",
        "faq": "Fragen",
        "cs": "Kundenservice",
        "pay": "Zahlung",
        "guide": "Einkaufsagent",
        "copy": f"LitBuy-Spreadsheet für {label}. Anzeige in {ccy}. Bestellen auf litbuy.com.",
        "local_h2": f"Lieferung nach {label}",
        "loc1t": "Land im Rechner",
        "loc1": f"Öffne den Rechner und setze Ziel {label}, bevor du Fracht zahlst. {d['city']}.",
        "loc2t": "Adresse",
        "loc2": f"Straße und {d['city']}. Packstation-Nummern sind ein DE-Muster. Registrieren und zahlen auf litbuy.com.",
        "loc3t": "Abgaben",
        "loc3": f"Die gebuchte SKU entscheidet prepaid oder Nachnahme. Quelle: {d['customs']} — {d['customs_url']}.",
        "loc4t": "Letzte Meile",
        "loc4": f"Oft {d['post']} nach akzeptierten Lagerfotos.",
    }
    packs["at"] = dict(packs["de"])
    packs["nl"] = {
        **en,
        "home": "Home",
        "ship": "Verzending",
        "help": "Helpcentrum",
        "reg": "Inloggen bij LitBuy",
        "cart": "Winkelwagen",
        "promo": "Bestellen op litbuy.com — eerst registreren, dan de link plakken.",
        "est": "Vrachtcalculator",
        "lang": "Nederlands",
        "search": "Productnaam of link",
        "submit": "Zoeken",
        "sub": f"Shop in China met bezorging in {label}. Prijzen op deze pagina in {ccy}.",
        "s1t": "Bestellen",
        "s1": "Plak een Taobao-, 1688- of Weidian-link op litbuy.com.",
        "s2t": "QC in het magazijn",
        "s2": "Magazijnfoto’s vóór internationale vracht.",
        "s3t": "Naar je deur",
        "s3": f"Kies een lijn met bestemming {label}. Last-mile vaak {d['post']}.",
        "shots": "Zo werkt LitBuy",
        "cap_home": "LitBuy-home — plak de link om te starten.",
        "cap_est": f"Vrachtcalculator. Bestemming {label} vóór je porto betaalt.",
        "cap_diy": "Registreer of log in op litbuy.com.",
        "local": f"Bezorging in {label}",
        "faq": "Vragen",
        "cs": "Klantenservice",
        "pay": "Betaling",
        "guide": "Inkoopagent",
        "copy": f"LitBuy-spreadsheet voor {label}. Weergave in {ccy}. Bestellen op litbuy.com.",
        "local_h2": f"Bezorging in {label}",
        "loc1t": "Land in de calculator",
        "loc1": f"Open de calculator en kies bestemming {label} vóór je vracht betaalt. {d['city']}.",
        "loc2t": "Adres",
        "loc2": f"Gebruik een straat en {d['city']}. Registreren en betalen op litbuy.com.",
        "loc3t": "Invoerrechten",
        "loc3": f"De geboekte SKU bepaalt prepaid of collect. Bron: {d['customs']} — {d['customs_url']}.",
        "loc4t": "Last-mile",
        "loc4": f"Vaak {d['post']} na geaccepteerde magazijnfoto’s.",
    }
    packs["es"] = {
        **en,
        "home": "Inicio",
        "ship": "Envío",
        "help": "Ayuda",
        "reg": "Entrar en LitBuy",
        "cart": "Carrito",
        "promo": "Compra en litbuy.com — regístrate antes de pegar el enlace.",
        "est": "Calculadora de envío",
        "custom": "Cómo comprar",
        "lang": "Español",
        "search": "Nombre del producto o enlace",
        "submit": "Buscar",
        "sub": f"Compra en China con entrega en {label}. Precios en esta página en {ccy}.",
        "s1t": "Pedir",
        "s1": "Pega un enlace de Taobao, 1688 o Weidian en litbuy.com.",
        "s2t": "QC en almacén",
        "s2": "Fotos de almacén antes del flete internacional.",
        "s3t": "A tu puerta",
        "s3": f"Elige una línea con destino {label}. Last-mile a menudo {d['post']}.",
        "shots": "Así funciona LitBuy",
        "cap_home": "Inicio LitBuy — pega el enlace para empezar.",
        "cap_est": f"Calculadora. Destino {label} antes de pagar el flete.",
        "cap_diy": "Regístrate o entra en litbuy.com.",
        "local": f"Entrega en {label}",
        "faq": "Preguntas",
        "cs": "Atención al cliente",
        "pay": "Pago",
        "guide": "Agente de compras",
        "copy": f"Spreadsheet LitBuy para {label}. Visualización en {ccy}. Pedidos en litbuy.com.",
        "local_h2": f"Entrega en {label}",
        "loc1t": "País en el calculador",
        "loc1": f"Abre el calculador y elige {label} antes de pagar el flete. {d['city']}.",
        "loc2t": "Dirección",
        "loc2": f"Calle y {d['city']}. Pago en litbuy.com.",
        "loc3t": "Aduana",
        "loc3": f"La SKU decide prepaid o destinatario. Fuente: {d['customs']} — {d['customs_url']}.",
        "loc4t": "Last-mile",
        "loc4": f"A menudo {d['post']} después de aceptar las fotos de almacén.",
    }
    packs["fr"] = {
        **en,
        "home": "Accueil",
        "ship": "Livraison",
        "help": "Aide",
        "reg": "Connexion LitBuy",
        "cart": "Panier",
        "promo": "Achetez sur litbuy.com — inscrivez-vous avant de coller le lien.",
        "est": "Calculateur de fret",
        "custom": "Comment acheter",
        "lang": "Français",
        "search": "Nom du produit ou lien",
        "submit": "Rechercher",
        "sub": f"Achetez en Chine avec livraison en {label}. Prix affichés en {ccy}.",
        "s1t": "Commander",
        "s1": "Collez un lien Taobao, 1688 ou Weidian sur litbuy.com.",
        "s2t": "QC en entrepôt",
        "s2": "Photos d’entrepôt avant le fret international.",
        "s3t": "À votre porte",
        "s3": f"Choisissez une ligne vers {label}. Last-mile souvent {d['post']}.",
        "shots": "Comment LitBuy fonctionne",
        "cap_home": "Accueil LitBuy — collez le lien pour commencer.",
        "cap_est": f"Calculateur. Destination {label} avant de payer le fret.",
        "cap_diy": "Inscrivez-vous sur litbuy.com.",
        "local": f"Livraison en {label}",
        "faq": "Questions",
        "cs": "Service client",
        "pay": "Paiement",
        "guide": "Agent d’achat",
        "copy": f"Spreadsheet LitBuy pour {label}. Affichage {ccy}. Commandes sur litbuy.com.",
        "local_h2": f"Livraison en {label}",
        "loc1t": "Pays dans le calculateur",
        "loc1": f"Ouvrez le calculateur et choisissez {label} avant de payer le fret. {d['city']}.",
        "loc2t": "Adresse",
        "loc2": f"Rue et {d['city']}. Paiement sur litbuy.com.",
        "loc3t": "Douane",
        "loc3": f"La SKU décide prepaid ou destinataire. Source : {d['customs']} — {d['customs_url']}.",
        "loc4t": "Last-mile",
        "loc4": f"Souvent {d['post']} après les photos d’entrepôt.",
    }
    packs["it"] = {
        **en,
        "home": "Home",
        "ship": "Spedizione",
        "help": "Aiuto",
        "reg": "Accedi a LitBuy",
        "cart": "Carrello",
        "promo": "Acquista su litbuy.com — registrati prima di incollare il link.",
        "est": "Calcolatore spedizione",
        "custom": "Come comprare",
        "lang": "Italiano",
        "search": "Nome prodotto o link",
        "submit": "Cerca",
        "sub": f"Acquista in Cina con consegna in {label}. Prezzi in {ccy}.",
        "s1t": "Ordina",
        "s1": "Incolla un link Taobao, 1688 o Weidian su litbuy.com.",
        "s2t": "QC in magazzino",
        "s2": "Foto di magazzino prima del nolo internazionale.",
        "s3t": "Alla porta",
        "s3": f"Scegli una linea verso {label}. Last-mile spesso {d['post']}.",
        "shots": "Come funziona LitBuy",
        "cap_home": "Home LitBuy — incolla il link per iniziare.",
        "cap_est": f"Calcolatore. Destinazione {label} prima di pagare il nolo.",
        "cap_diy": "Registrati su litbuy.com.",
        "local": f"Consegna in {label}",
        "faq": "Domande",
        "cs": "Assistenza",
        "pay": "Pagamento",
        "guide": "Agente d’acquisto",
        "copy": f"Spreadsheet LitBuy per {label}. Visualizzazione {ccy}. Ordini su litbuy.com.",
    }
    return packs.get(key) or packs["uk"]


def fig(src: str, cap: str) -> str:
    return (
        f'<figure class="shot"><img src="{escape(src)}" alt="{escape(cap)}" width="1400" height="900" loading="lazy" decoding="async">'
        f"<figcaption>{escape(cap)}</figcaption></figure>"
    )


def header_html(host: str, d: dict) -> str:
    L = chrome(d)
    p = d["pages"]
    return (
        f'<div class="cb-promo"><a href="{OFF}" rel="noopener">{escape(L["promo"])}</a></div>'
        '<header class="cb-head top" role="banner">'
        '<div class="cb-head-inner wrap">'
        f'<a class="cb-logo brand" href="/"><img src="/assets/images/litbuy-logo.png" alt="LitBuy" width="118" height="39"></a>'
        '<nav class="cb-head-left nav">'
        f'<a class="on" href="/">{escape(L["home"])}</a>'
        f'<a href="/{p["spreadsheet"]}/">{escape(L["sheet"])}</a>'
        f'<a href="{EST}" rel="noopener">{escape(L["est"])}</a>'
        f'<a href="/{p["shipping"]}/">{escape(L["ship"])}</a>'
        f'<a href="/{p["guide"]}/">{escape(L["help"])}</a>'
        f'<a href="{OFF}" rel="noopener">{escape(L["custom"])}</a>'
        "</nav>"
        '<div class="cb-head-right" style="display:flex;align-items:center;gap:12px">'
        f'<span class="cb-ccy">{escape(L["lang"])} / {escape(d["ccy"])}</span>'
        f'<a class="hdr-login" href="{OFF}" rel="noopener">{escape(L["reg"])}</a>'
        "</div></div>"
        f'<form class="cb-head-search" action="{W2C_SEARCH}" method="get" target="_blank" rel="noopener">'
        f'<input name="q" placeholder="{escape(L["search"])}" aria-label="{escape(L["search"])}">'
        f'<button class="btn" type="submit">{escape(L["submit"])}</button>'
        "</form>"
        "</header>"
    )


def footer_html(host: str, d: dict) -> str:
    L = chrome(d)
    p = d["pages"]
    return (
        '<footer class="cb-foot site-ft"><div class="cb-foot-grid ft-grid">'
        f"<div><h3>{escape(L['cs'])}</h3><ul>"
        f'<li><a href="{HELP}">{escape(L["help"])}</a></li>'
        f'<li><a href="/{p["faq"]}/">{escape(L["faq"])}</a></li>'
        "</ul></div>"
        f"<div><h3>{escape(L['pay'])}</h3><ul>"
        f'<li><a href="{OFF}">litbuy.com</a></li>'
        f"<li>{escape(d['ccy'])}</li></ul>"
        '<p class="cb-pay"><span>VISA</span><span>Mastercard</span><span>PayPal</span></p></div>'
        f"<div><h3>{escape(L['guide'])}</h3><ul>"
        f'<li><a href="/{p["guide"]}/">{escape(L["help"])}</a></li>'
        f'<li><a href="{EST}">{escape(L["est"])}</a></li>'
        f'<li><a href="/{p["qc"]}/">QC</a></li>'
        "</ul></div>"
        f"<div><h3>LitBuy</h3><p>{escape(L['copy'])}</p>"
        f'<p><a href="{OFF}">litbuy.com</a></p></div>'
        "</div></footer>"
    )


def strip_ops(html: str) -> str:
    html = re.sub(r"<!--\s*DEPLOY GUARD:[^>]*-->\s*", "", html, flags=re.I)
    phrases = (
        r"\s*Not checkout\. No declared-value coaching\.",
        r"\s*No declared-value coaching\.",
        r"\s*Not checkout\.",
        r"\s*Keine Unterdeklaration\.",
        r"\s*Geen onderwaardering\.",
        r"\s*Sin infradeclaración\.",
        r"\s*Pas de sous-déclaration\.",
        r"\s*Niente sottofatturazione\.",
        r"LitBuy independent desk",
        r"[a-z0-9.-]+ independent desk",
        r"independent information desk",
    )
    for rx in phrases:
        html = re.sub(rx, "", html, flags=re.I)

    def _body(m: re.Match) -> str:
        body = m.group(0)
        for rx in OPS_RX:
            body = re.sub(rx, "", body, flags=re.I)
        return body

    if re.search(r"<body\b", html, re.I):
        return re.sub(r"<body\b[\s\S]*</body>", _body, html, count=1, flags=re.I)
    for rx in OPS_RX:
        html = re.sub(rx, "", html, flags=re.I)
    return html


def _drop_el(html: str, open_re: str, tag: str = "div") -> str:
    m = re.search(open_re, html, flags=re.I)
    if not m:
        return html
    start = m.start()
    i = m.end()
    depth = 1
    open_pat = re.compile(rf"<{tag}\b", re.I)
    close_pat = re.compile(rf"</{tag}>", re.I)
    while i < len(html) and depth:
        nxt_open = open_pat.search(html, i)
        nxt_close = close_pat.search(html, i)
        if not nxt_close:
            break
        if nxt_open and nxt_open.start() < nxt_close.start():
            depth += 1
            i = nxt_open.end()
        else:
            depth -= 1
            i = nxt_close.end()
    return html[:start] + html[i:]


def _drop_all(html: str, open_re: str, tag: str = "div") -> str:
    for _ in range(8):
        nxt = _drop_el(html, open_re, tag)
        if nxt == html:
            break
        html = nxt
    return html


def kill_lang_modal(html: str) -> str:
    """Remove leftover Language & Currency chrome that is not official dest UI."""
    html = _drop_all(html, r'<div\b[^>]*\bid=["\']lang-backdrop["\'][^>]*>')
    html = _drop_all(html, r'<div\b[^>]*\bid=["\']lang-modal["\'][^>]*>')
    html = _drop_all(html, r'<div\b[^>]*\bclass=["\'][^"\']*\blmo\b[^"\']*["\'][^>]*>')
    html = _drop_all(html, r'<div\b[^>]*\bclass=["\'][^"\']*\blbk\b[^"\']*["\'][^>]*>')
    html = _drop_all(html, r'<div\b[^>]*\bclass=["\'][^"\']*\blmi\b[^"\']*["\'][^>]*>')
    html = _drop_all(html, r'<div\b[^>]*\bclass=["\']waf["\'][^>]*>')
    html = re.sub(r"(</header>)\s*</div>\s*", r"\1\n", html, count=1)
    html = html.replace(
        "document.addEventListener('DOMContentLoaded',()=>{buildG();setBadge();applyT();if(typeof lp==='function')lp(true);});",
        "document.addEventListener('DOMContentLoaded',()=>{if(typeof lp==='function')lp(true);});",
    )
    html = re.sub(r"function toggleLM\(\)\{[^}]*\}", "function toggleLM(){}", html)
    html = re.sub(r"function openLM\(\)\{[^}]*\}", "function openLM(){}", html)
    html = re.sub(r"function closeLM\(\)\{[^}]*\}", "function closeLM(){}", html)
    html = re.sub(
        r"function buildG\(\)\{[\s\S]*?document\.getElementById\('curr-grid'\)[\s\S]*?\n\}",
        "function buildG(){}",
        html,
        count=1,
    )
    return html


def _replace_nested(html: str, open_re: str, new: str) -> str:
    m = re.search(open_re, html, flags=re.I)
    if not m:
        return html
    start = m.start()
    i = m.end()
    depth = 1
    open_pat = re.compile(r"<section\b", re.I)
    close_pat = re.compile(r"</section>", re.I)
    while i < len(html) and depth:
        nxt_open = open_pat.search(html, i)
        nxt_close = close_pat.search(html, i)
        if not nxt_close:
            break
        if nxt_open and nxt_open.start() < nxt_close.start():
            depth += 1
            i = nxt_open.end()
        else:
            depth -= 1
            i = nxt_close.end()
    return html[:start] + new + html[i:]


def _replace_section(html: str, sid: str, new: str) -> str:
    return _replace_nested(html, rf'<section\b[^>]*\bid=["\']{sid}["\'][^>]*>', new)


def ensure_section(html: str, sid: str, new: str) -> str:
    if re.search(rf'\bid=["\']{sid}["\']', html, flags=re.I):
        return _replace_section(html, sid, new)
    html = re.sub(r"(<footer\b)", new + "\n\\1", html, count=1, flags=re.I)
    return html


def inject_css(html: str) -> str:
    if 'id="litbuy-official-skin"' in html:
        html = re.sub(r'<style id="litbuy-official-skin">[\s\S]*?</style>', CSS, html, count=1)
    else:
        html = html.replace("</head>", CSS + "\n</head>", 1)
    return html


def skin_chrome(html: str, host: str, d: dict) -> str:
    html = inject_css(html)
    html = re.sub(r'<div class="(?:cb-promo|od-promo|ann)">[\s\S]*?</div>\s*', "", html, count=1)
    html = re.sub(
        r"<header class=\"(?:site-header|cb-head|lg-head|top|cssbuy-header|litbuy-header|w2c-header)[^\"]*\"[^>]*>[\s\S]*?</header>",
        header_html(host, d),
        html,
        count=1,
    )
    if not re.search(r"<header\b[^>]*class=\"[^\"]*cb-head", html, flags=re.I):
        html = re.sub(
            r"<nav class=\"(?:nav|w2c-nav)\"[^>]*>[\s\S]*?</nav>",
            header_html(host, d),
            html,
            count=1,
        )
    html = kill_lang_modal(html)
    html = _drop_all(html, r'<div class="locale-switcher"[^>]*>')
    html = re.sub(r'<div class="header-actions">[\s\S]*?</div>\s*', "", html, count=1)
    html = re.sub(r'<div class="topbar">[\s\S]*?</div>\s*', "", html, count=1)
    html = re.sub(r'<style id="au-deepen-[^"]*">[\s\S]*?</style>\s*', "", html, count=1)
    html = re.sub(
        r"<footer class=\"(?:site-footer|cb-foot|site-ft|od-foot|ft|w2c-footer)[^\"]*\"[^>]*>[\s\S]*?</footer>",
        footer_html(host, d),
        html,
        count=1,
    )
    html = re.sub(
        r'<form id="w2c-search"[^>]*>[\s\S]*?</form>',
        "",
        html,
        count=1,
        flags=re.I,
    )
    html = re.sub(r"\?inviteCode=[A-Za-z0-9]+", "", html)
    html = html.replace("https://litbuy.com/register", "https://litbuy.com/register")
    html = re.sub(r"\?ref=O4K87NHKR", "", html)
    html = patch_catalog_w2c(html)
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
        f"{fig(shot_est(d), L['cap_est'])}"
        f"{fig(SHOT_DIY, L['cap_diy'])}"
        "</div></div></section>"
    )


def process_html(d: dict) -> str:
    L = chrome(d)
    return (
        '<section class="cb-steps" id="how">'
        f'<article class="cb-step"><strong>01</strong><h3>{escape(L["s1t"])}</h3><p>{escape(L["s1"])}</p></article>'
        f'<article class="cb-step"><strong>02</strong><h3>{escape(L["s2t"])}</h3><p>{escape(L["s2"])}</p></article>'
        f'<article class="cb-step"><strong>03</strong><h3>{escape(L["s3t"])}</h3><p>{escape(L["s3"])}</p></article>'
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
        '<section class="cb-hero" id="hero">'
        f'<img class="cb-hero-bg" src="{SHOT_GIF}" alt="LitBuy">'
        '<div class="cb-hero-copy">'
        f"<h1>{h1}</h1>"
        f'<p class="hsub">{escape(L["sub"])}</p>'
        f'<form class="cb-search" action="{W2C_SEARCH}" method="get" target="_blank" rel="noopener">'
        f'<input name="q" placeholder="{escape(L["search"])}" aria-label="{escape(L["search"])}">'
        f'<button class="btn btn-primary" type="submit">{escape(L["submit"])}</button>'
        "</form>"
        f"{nav_html}"
        f'<p class="eu-badge">{escape(d["dest"] or "")} · {escape(d["ccy"])} · {escape(d["post"])}</p>'
        "</div></section>"
    )
    html = _replace_nested(html, r'<section class="[^"]*(?:sg-hero|hero|cb-hero|od-hero)[^"]*"[^>]*>', hero)
    return html


def rebuild_home(html: str, host: str, d: dict) -> str:
    L = chrome(d)
    html = skin_chrome(html, host, d)
    html = rebuild_hero(html, host, d)
    local_html = (
        f'<section class="sg-sec" id="local">{fig(shot_est(d), L["cap_est"])}'
        f"<h2>{escape(L['local_h2'])}</h2>"
        f"<ol class=\"local-steps\">"
        f"<li><strong>{escape(L['loc1t'])}</strong><span>{escape(L['loc1'])}</span></li>"
        f"<li><strong>{escape(L['loc2t'])}</strong><span>{escape(L['loc2'])}</span></li>"
        f"<li><strong>{escape(L['loc3t'])}</strong><span>{escape(L['loc3'])}</span></li>"
        f"<li><strong>{escape(L['loc4t'])}</strong><span>{escape(L['loc4'])}</span></li>"
        f"</ol></section>"
    )
    html = ensure_section(html, "local", local_html)
    html = _replace_section(html, "lab", "")
    html = _replace_section(html, "kept", "")
    html = _replace_section(html, "news", "")
    html = re.sub(r'<div class="waband">[\s\S]*?</div>\s*', "", html, count=1)
    html = re.sub(r'<section class="sec act-sec">[\s\S]*?</section>', "", html, count=1)
    html = ensure_section(
        html,
        "agent",
        f'<section class="sg-sec" id="agent"><div class="sg-split"><div class="sg-prose">'
        f"<h2>LitBuy</h2><p>{escape(L['sub'])}</p>"
        f'<p><a class="btn btn-primary" href="{OFF}">{escape(L["reg"])}</a> '
        f'<a class="btn btn-outline" href="{EST}">{escape(L["est"])}</a> '
        f'<a class="btn btn-outline" href="{W2C_SHEET}" target="_blank" rel="noopener">w2clinks</a></p>'
        f'</div>{fig(SHOT_DIY, L["cap_diy"])}</div></section>',
    )
    html = ensure_section(html, "shots", shots_html(d))
    html = ensure_section(
        html,
        "restricted",
        f'<section class="sg-sec" id="restricted"><h2>QC</h2>'
        f"<p>{escape(L['s2'])}</p>{fig(shot_est(d), L['s2'])}</section>",
    )
    html = ensure_section(html, "cat-wall", cat_wall(d))
    html = _replace_section(html, "states", "")
    html = ensure_section(html, "how", process_html(d))
    html = re.sub(
        r"</main>\s*<section class=\"cb-steps\" id=\"how\">[\s\S]*?</section>",
        "</main>",
        html,
        count=1,
        flags=re.I,
    )
    from litbuy_dest_copy import extra_faq

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
    html = re.sub(r'<p class="local-src">[\s\S]*?</p>', "", html)
    html = re.sub(r'<p class="hub-uplink">[\s\S]*?</p>', "", html)
    html = strip_ops(html)
    html = patch_catalog_w2c(html)
    return html


def patch_catalog_w2c(html: str) -> str:
    html = html.replace(
        'action="https://w2clinks.com/spreadsheet/litbuy/"',
        f'action="{W2C_SEARCH}"',
    )
    html = html.replace(
        "https://w2clinks.com/spreadsheet/litbuy/?q=",
        "https://w2clinks.com/spreadsheet/?q=",
    )
    return html


def article_figures(kind: str, d: dict) -> list[str]:
    L = chrome(d)
    if kind == "shipping":
        return [fig(shot_est(d), L["cap_est"]), fig(SHOT_HOME, L["cap_home"])]
    if kind == "guide":
        return [fig(SHOT_DIY, L["cap_diy"]), fig(SHOT_GIF, L["s1"])]
    if kind == "qc":
        return [fig(shot_est(d), L["s2"]), fig(shot_est(d), L["cap_est"])]
    if kind == "legal":
        return [fig(SHOT_DIY, L["cap_diy"]), fig(SHOT_HOME, L["cap_home"])]
    return [fig(SHOT_HOME, L["cap_home"]), fig(shot_est(d), L["cap_est"])]


def install_media(host: str) -> list[Path]:
    dest = ROOT / "sites" / host / "overlay"
    media = dest / "media"
    cats = dest / "img" / "cat"
    media.mkdir(parents=True, exist_ok=True)
    cats.mkdir(parents=True, exist_ok=True)
    written = []
    mapping = {
        "official-home.jpg": MEDIA_SRC / "official-home.jpg",
        "catalogus.jpg": MEDIA_SRC / "shots" / "catalogus.jpg",
        "catalogus-zoek.jpg": MEDIA_SRC / "shots" / "catalogus-zoek.jpg",
        "volume-voorbeeld.jpg": MEDIA_SRC / "shots" / "volume-voorbeeld.jpg",
        "oficial-inicio.jpg": MEDIA_SRC / "shots" / "oficial-inicio.jpg",
        "oficial-diy.jpg": MEDIA_SRC / "shots" / "oficial-diy.jpg",
        "estimator-nl.jpg": MEDIA_SRC / "shots" / "estimator-nl.jpg",
        "estimator-ca.jpg": MEDIA_SRC / "shots" / "estimator-ca.jpg",
        "estimator-uk.jpg": MEDIA_SRC / "shots" / "estimator-uk.jpg",
        "estimator-us.jpg": MEDIA_SRC / "shots" / "estimator-us.jpg",
        "estimator-at.jpg": MEDIA_SRC / "shots" / "estimator-at.jpg",
        "estimator-de.jpg": MEDIA_SRC / "shots" / "estimator-de.jpg",
        "hero.jpg": MEDIA_SRC / "hero.jpg",
        "litbuy-logo.png": MEDIA_SRC / "litbuy-logo.png",
        "litbuy-logo-eu.png": MEDIA_SRC / "litbuy-logo-eu.png",
    }
    home = MEDIA_SRC / "official-home.jpg"
    if not home.is_file() or home.stat().st_size < 200:
        for cand in (
            MEDIA_SRC / "shots" / "oficial-inicio.jpg",
            MEDIA_SRC / "hero.jpg",
            MEDIA_SRC / "shots" / "catalogus.jpg",
            MEDIA_SRC / "shots" / "volume-voorbeeld.jpg",
        ):
            if cand.is_file() and cand.stat().st_size > 200:
                shutil.copy2(cand, home)
                break
    logo = MEDIA_SRC / "litbuy-logo.png"
    word = MEDIA_SRC / "litbuy-logo-eu.png"
    if (not logo.is_file() or logo.stat().st_size < 200) and word.is_file():
        shutil.copy2(word, logo)
    for name, src in mapping.items():
        if src.is_file():
            out = media / name
            shutil.copy2(src, out)
            written.append(out)
        elif name == "official-home.jpg" and (media / "oficial-inicio.jpg").is_file():
            out = media / name
            shutil.copy2(media / "oficial-inicio.jpg", out)
            written.append(out)
    assets = dest / "assets" / "images"
    assets.mkdir(parents=True, exist_ok=True)
    for logo_name in ("litbuy-logo.png", "litbuy-logo-eu.png"):
        logo = MEDIA_SRC / logo_name
        if logo.is_file():
            out = assets / logo_name
            shutil.copy2(logo, out)
            written.append(out)
            if logo_name == "litbuy-logo-eu.png":
                shutil.copy2(logo, assets / "litbuy-logo.png")
                written.append(assets / "litbuy-logo.png")
    est = media / "estimator-de.jpg"
    if not est.is_file() or est.stat().st_size < 200:
        for cand in (
            media / "estimator-at.jpg",
            media / "oficial-inicio.jpg",
            media / "official-home.jpg",
            media / "hero.jpg",
        ):
            if cand.is_file() and cand.stat().st_size > 200:
                shutil.copy2(cand, est)
                written.append(est)
                break
    for alias in ("oficial-inicio.jpg", "oficial-diy.jpg", "official-home.jpg", "estimator-uk.jpg", "estimator-at.jpg"):
        dest_alias = media / alias
        if (not dest_alias.is_file() or dest_alias.stat().st_size < 200) and est.is_file() and est.stat().st_size > 200:
            shutil.copy2(est, dest_alias)
            written.append(dest_alias)
    src_cats = MEDIA_SRC / "cats"
    if src_cats.is_dir():
        for dest_name, src_name in CAT_SRC.items():
            srcp = src_cats / src_name
            if not srcp.is_file():
                srcp = src_cats / dest_name
            if srcp.is_file():
                out = cats / dest_name
                shutil.copy2(srcp, out)
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
        if any(part.startswith("litbuy-announcement") for part in path.parts):
            continue
        html = path.read_text(encoding="utf-8")
        if path.name == "index.html" and path.parent.name == "overlay":
            continue
        html = skin_chrome(html, host, d)
        path.write_text(html, encoding="utf-8")
