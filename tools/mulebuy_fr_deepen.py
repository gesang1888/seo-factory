#!/usr/bin/env python3
"""Deepen mulebuy.fr keep desk: Colissimo / douane.gouv.fr / 5-digit CP + kill sheet hero.

LIVE only on mulebuy.fr. Does not touch hub (bestmulebuysheets.com), does not revive
twins (.co.uk/.es/.us), no Phase C. Requires ORIGIN_SSH_PASS (or --load-env usfans-ssh.env).
"""
from __future__ import annotations

import argparse
import http.client
import json
import os
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
OVERLAY = ROOT / "sites" / "mulebuy.fr" / "overlay"
HOST = "mulebuy.fr"
REMOTE = f"/www/wwwroot/{HOST}"
STAMP = "20261028"
TODAY = "2026-10-28"
TODAY_FR = "28 Oct 2026"
HUB = "https://bestmulebuysheets.com"
PAGES = (
    "mulebuy-shipping",
    "livraison-mulebuy",
    "mulebuy-spreadsheet",
    "mulebuy-coupons",
)

STYLE = (
    f'<style id="fr-deepen-{STAMP}">.hub-uplink{{margin:14px 0 0;padding:12px 14px;'
    "border-left:3px solid #0f766e;background:#f0fdfa;color:#134e4a;line-height:1.6;"
    "font-size:15px;max-width:760px}}.hub-uplink a{{color:#0f766e;font-weight:600}}"
    "#local{scroll-margin-top:88px}.local-box{margin:1.25em 0;padding:14px 16px;"
    "border:1px solid #e2e8f0;border-radius:10px;background:#f8fafc}"
    ".fr-desk-hero{margin:0 0 1.25em}.fr-desk-hero h1{font-size:clamp(1.5rem,3vw,2rem);"
    "line-height:1.25;margin:0 0 .5em}</style>"
)

HUB_UPLINK = (
    f'<p class="hub-uplink" data-fr-deepen="{STAMP}" data-step4-hub="1">'
    "Brand Spreadsheet / Coupons truth / Independent Index · 8,000+ → "
    f'<a href="{HUB}/">bestmulebuysheets.com</a> · '
    f'<a href="{HUB}/mulebuy-coupons/">coupons</a> · '
    f'<a href="{HUB}/finds-dataset/">dataset</a>. '
    "Cette URL = desk FR seulement (Colissimo / douane.gouv.fr / code postal à cinq chiffres / EUR)."
    "</p>"
)

LOCAL_SHIP = f"""
<section id="local" class="local-box" data-fr-fingerprint="colissimo-douane-cp5" data-fr-deepen="{STAMP}">
<h2>Empreinte FR avant de choisir une ligne</h2>
<ol>
<li><strong>Destination estimateur : France</strong> — FR, pas EU, pas BE (code postal belge à quatre chiffres = mauvais pays).</li>
<li><strong>Adresse</strong> — rue française, <strong>code postal à cinq chiffres</strong> (ex. <code>75001</code>).</li>
<li><strong>Dernier kilomètre</strong> — souvent <strong>Colissimo</strong> ; ce desk n’invente pas de point relais.</li>
<li><strong>Droits</strong> — la SKU décide. Source du matin : <a href="https://www.douane.gouv.fr/" rel="noopener" target="_blank">douane.gouv.fr</a>. Devis en <strong>EUR</strong>.</li>
</ol>
<p>Autre guide livraison : <a href="/livraison-mulebuy/">livraison MuleBuy</a> · coupons locaux (vérité sur hub) : <a href="/mulebuy-coupons/">coupons FR</a>.</p>
</section>
"""

LOCAL_LIVRAISON = f"""
<section id="local" class="local-box" data-fr-fingerprint="livraison-colissimo-douane" data-fr-deepen="{STAMP}">
<h2>Empreinte livraison France</h2>
<ol>
<li><strong>Colissimo</strong> — last mile fréquent ; Collect peut ajouter des frais (≠ coupon).</li>
<li><strong>douane.gouv.fr</strong> — règles d’import le matin de l’envoi ; pas de valeur déclarée inventée.</li>
<li><strong>Code postal à cinq chiffres</strong> — ex. <code>75001</code> ; jamais un CP belge à quatre chiffres.</li>
<li><strong>EUR</strong> — devis freight / droits en euros après QC.</li>
</ol>
<p>Checklist estimateur : <a href="/mulebuy-shipping/">expédier vers la France</a>.</p>
</section>
"""

LOCAL_SHEET = f"""
<section id="local" class="local-box" data-fr-fingerprint="fr-desk-not-second-hub" data-fr-deepen="{STAMP}">
<h2>Desk FR — pas un second hub Spreadsheet</h2>
<ol>
<li><strong>Intention Brand Spreadsheet</strong> → <a href="{HUB}/">bestmulebuysheets.com</a> (Independent Index · 8,000+).</li>
<li><strong>Cette URL .fr</strong> aide l’atterrissage FR : Colissimo, douane.gouv.fr, code postal à cinq chiffres, EUR — pas un héros finds concurrent.</li>
<li><strong>Table coupons vérité</strong> → <a href="{HUB}/mulebuy-coupons/">hub coupons</a> ; landing FR peut rester locale.</li>
<li><strong>Dataset / lignes W2C</strong> → <a href="{HUB}/finds-dataset/">hub finds-dataset</a>.</li>
</ol>
<p>Suite sur ce desk : <a href="/mulebuy-shipping/">shipping FR</a> · <a href="/livraison-mulebuy/">livraison</a>.</p>
</section>
"""

LOCAL_COUPONS = f"""
<section id="local" class="local-box" data-fr-fingerprint="coupon-not-douane" data-fr-deepen="{STAMP}">
<h2>Empreinte coupons FR</h2>
<ol>
<li><strong>Coupon ≠ douane</strong> — un code n’annule pas Colissimo Collect ni les droits d’import.</li>
<li><strong>Checkout EUR</strong> — estimez freight / droits en EUR après shortlist + QC.</li>
<li><strong>Table vérité</strong> — codes globaux → <a href="{HUB}/mulebuy-coupons/">bestmulebuysheets.com/mulebuy-coupons</a>.</li>
<li><strong>Twins</strong> — <code>mulebuyspreadsheets.{{co.uk,es,us}}</code> restent 301→hub ; ne pas les hreflang.</li>
</ol>
<p>Planifier l’envoi : <a href="/mulebuy-shipping/">shipping FR</a>.</p>
</section>
"""

THICKEN_SHIP = f"""
<h2 id="colissimo-douane">Colissimo, douane.gouv.fr et code postal à cinq chiffres (maj {TODAY_FR})</h2>
<p>Expédier vers la France signifie : destination estimateur <strong>France</strong>, une vraie adresse avec <strong>code postal à cinq chiffres</strong> (ex. <strong>75001</strong>), souvent <strong>Colissimo</strong> en dernier kilomètre, et des droits sous <strong>douane.gouv.fr</strong> selon la SKU — pas un héros Spreadsheet sur cette URL. Devis en <strong>EUR</strong>. Brand Spreadsheet / coupons vérité / dataset restent sur <a href="{HUB}/">bestmulebuysheets.com</a>.</p>
<p>Utilisez l’estimateur officiel pour comparer les lignes, puis revérifiez la déclaration avant envoi. Autre page livraison : <a href="/livraison-mulebuy/">livraison MuleBuy France</a>.</p>
"""

THICKEN_LIVRAISON = f"""
<h2 id="delais-colissimo">Délais, Colissimo et douane (maj {TODAY_FR})</h2>
<p>Cette page cadre la <strong>livraison vers une adresse en France</strong> : Colissimo / réseaux FR, TVA et droits séparés du freight agent, code postal à cinq chiffres. Ce n’est pas un second hub Spreadsheet. Catalogue / Independent Index · 8,000+ → <a href="{HUB}/">bestmulebuysheets.com</a>.</p>
<p>Checklist technique (estimateur, volume, restricted) : <a href="/mulebuy-shipping/">mulebuy-shipping</a>. Source douane : <a href="https://www.douane.gouv.fr/" rel="noopener" target="_blank">douane.gouv.fr</a>.</p>
"""

THICKEN_SHEET = f"""
<h2 id="cede-hub">Pourquoi cette page n’est pas le Brand Spreadsheet</h2>
<p>Le GSC montrait des clics exacts <em>mulebuy spreadsheet</em> / <em>spreadsheet mulebuy</em> sur le desk FR alors que le hub restait à 0 clic — c’est de la cannibalisation. L’Independent Index · <strong>8,000+</strong>, la table coupons et finds-dataset vivent sur <a href="{HUB}/">bestmulebuysheets.com</a>. Cette URL .fr est un aide-atterrissage FR (Colissimo / douane / CP à cinq chiffres) — pas un second héros Spreadsheet global.</p>
<p>Ouvrir le hub : <a href="{HUB}/">Independent Index</a> · <a href="{HUB}/finds-dataset/">dataset</a> · <a href="{HUB}/mulebuy-coupons/">coupons</a>. Suite locale : <a href="/mulebuy-shipping/">shipping FR</a>.</p>
"""

THICKEN_COUPONS = f"""
<h2 id="hub-truth">Vérité hub vs landing FR (maj {TODAY_FR})</h2>
<p>Gardez cette page pour le framing coupon FR et le flux d’inscription. La table vérité globale est sur <a href="{HUB}/mulebuy-coupons/">bestmulebuysheets.com/mulebuy-coupons</a>. Un coupon ne remplace jamais les droits <strong>douane.gouv.fr</strong> ni les frais <strong>Colissimo</strong> Collect — estimez-les en <strong>EUR</strong> sur le <a href="/mulebuy-shipping/">guide shipping</a>.</p>
"""


def _load_env(path: Path) -> None:
    text = path.read_text()
    host = pass_val = None
    for line in text.splitlines():
        if line.startswith("HOST="):
            host = line.split("=", 1)[1].strip().strip('"').strip("'")
        if line.startswith("RAW_LINE="):
            # Password = entire RAW_LINE value including leading semicolon (len 16).
            pass_val = line.split("=", 1)[1]
    if not host or not pass_val:
        raise SystemExit(f"HOST/RAW_LINE missing in {path}")
    os.environ.setdefault("ORIGIN_SSH_HOST", host)
    os.environ.setdefault("ORIGIN_SSH_PASS", pass_val)


def _connect():
    try:
        import paramiko
    except ImportError:
        import subprocess

        subprocess.check_call([sys.executable, "-m", "pip", "install", "paramiko", "-q"])
        import paramiko

    password = os.environ.get("ORIGIN_SSH_PASS")
    if not password:
        raise SystemExit("Set ORIGIN_SSH_PASS or pass --load-env")
    host = os.environ.get("ORIGIN_SSH_HOST", "31.97.41.31")
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(host, username="root", password=password, timeout=30)
    return client


def _run(client, cmd: str, timeout: int = 120) -> str:
    _, stdout, stderr = client.exec_command(cmd, timeout=timeout)
    out = (stdout.read() + stderr.read()).decode(errors="replace").strip()
    return out


def _inject_head_style(html: str) -> str:
    if f'id="fr-deepen-{STAMP}"' in html:
        return html
    return html.replace("</head>", STYLE + "\n</head>", 1)


def _strip_twin_hreflang(html: str) -> str:
    """Remove hreflang pointing at 301 twins; keep self fr-FR; x-default → hub."""
    html = re.sub(
        r'\s*<link rel="alternate" hreflang="(?:es-ES|en-US|en-GB)" href="https://mulebuyspreadsheets\.(?:es|us|co\.uk)/[^"]*"\s*/?>',
        "",
        html,
    )
    html = re.sub(
        r'<link rel="alternate" hreflang="x-default" href="https://mulebuyspreadsheets\.[^"]*"\s*/?>',
        f'<link rel="alternate" hreflang="x-default" href="{HUB}/">',
        html,
    )
    return html


def _soften_brand(html: str) -> str:
    html = html.replace("<span>Spreadsheet</span>", "<span>France</span>", 1)
    html = html.replace("<h3>MuleBuy Spreadsheet</h3>", "<h3>MuleBuy France</h3>")
    html = html.replace(
        "Guide indépendant en français sur MuleBuy et sur la façon d’utiliser le catalogue w2clinks",
        "Desk FR indépendant (Colissimo / douane.gouv.fr / code postal à cinq chiffres). Brand Spreadsheet → bestmulebuysheets.com. Ancien texte catalogue",
        1,
    )
    return html


def deepen_shipping(html: str) -> str:
    html = _inject_head_style(html)
    html = _soften_brand(html)
    new_title = "MuleBuy livraison France — Colissimo, douane.gouv.fr, CP à 5 chiffres"
    html = re.sub(r"<title>.*?</title>", f"<title>{new_title}</title>", html, count=1, flags=re.S)
    html = re.sub(
        r'name="description" content="[^"]*"',
        'name="description" content="Livraison MuleBuy vers la France : Colissimo, douane.gouv.fr, code postal à cinq chiffres, EUR. Brand Spreadsheet → bestmulebuysheets.com."',
        html,
        count=1,
    )
    html = html.replace(
        '"name": "MuleBuy Spreadsheet en français: livraison et douane vers la France"',
        f'"name": "{new_title}"',
    )
    html = html.replace(
        '"description": "Independent MuleBuy ship for la France."',
        '"description": "Livraison MuleBuy France : Colissimo, douane.gouv.fr, CP à cinq chiffres. Brand Spreadsheet → bestmulebuysheets.com."',
    )
    html = html.replace(
        "<h1>Expédier vers la France : estimateur, volume, douane</h1>\n"
        "  <p class=\"lead\">Destination France — 法国, pas EU. L’adresse est une rue française, code postal à cinq chiffres, pas un code postal belge.</p>",
        "<h1>Expédier vers la France — Colissimo · douane · CP à cinq chiffres</h1>\n"
        "  <p class=\"lead\">Destination France — pas EU, pas BE. Adresse avec <strong>code postal à cinq chiffres</strong> (ex. <strong>75001</strong>). "
        f"Last mile souvent <strong>Colissimo</strong> ; droits : <strong>douane.gouv.fr</strong>. Maj {TODAY_FR}. Brand Spreadsheet → bestmulebuysheets.com.</p>\n"
        f"  {HUB_UPLINK}",
        1,
    )
    if 'id="local"' not in html:
        html = html.replace(
            "<h2>L’estimateur officiel décide</h2>",
            f"{LOCAL_SHIP}\n  <h2>L’estimateur officiel décide</h2>",
            1,
        )
    if 'id="colissimo-douane"' not in html:
        html = html.replace(
            "<h2>L’adresse sur ce dest</h2>",
            f"{THICKEN_SHIP}\n  <h2>L’adresse sur ce dest</h2>",
            1,
        )
    return html


def deepen_livraison(html: str) -> str:
    html = _inject_head_style(html)
    html = _soften_brand(html)
    html = _strip_twin_hreflang(html)
    new_title = "Livraison MuleBuy France — Colissimo, douane.gouv.fr, délais"
    html = re.sub(r"<title>.*?</title>", f"<title>{new_title}</title>", html, count=1, flags=re.S)
    html = re.sub(
        r'property="og:title" content="[^"]*"',
        f'property="og:title" content="{new_title}"',
        html,
        count=1,
    )
    html = re.sub(
        r'name="description" content="[^"]*"',
        'name="description" content="Livraison MuleBuy France : Colissimo, douane.gouv.fr, code postal à cinq chiffres, EUR. Brand Spreadsheet → bestmulebuysheets.com."',
        html,
        count=1,
    )
    html = re.sub(
        r'property="og:description" content="[^"]*"',
        'property="og:description" content="Livraison MuleBuy France : Colissimo, douane.gouv.fr, CP à cinq chiffres."',
        html,
        count=1,
    )
    html = html.replace(
        '"name": "Livraison Mulebuy France (2026) — Délais & douane"',
        f'"name": "{new_title}"',
    )
    # Inject FR desk hero (page had no H1) + uplink before keyword card
    if f'data-fr-deepen="{STAMP}"' not in html or 'class="fr-desk-hero"' not in html:
        inject = (
            f'<div class="fr-desk-hero" data-fr-deepen="{STAMP}">\n'
            "  <h1>Livraison MuleBuy vers la France — Colissimo · douane</h1>\n"
            "  <p class=\"lead\">Délais, last mile <strong>Colissimo</strong>, droits via "
            f'<a href="https://www.douane.gouv.fr/" rel="noopener" target="_blank">douane.gouv.fr</a>, '
            f"code postal à cinq chiffres. Maj {TODAY_FR}. Brand Spreadsheet → "
            f'<a href="{HUB}/">bestmulebuysheets.com</a>.</p>\n'
            f"  {HUB_UPLINK}\n"
            "</div>\n"
        )
        html = html.replace(
            '<div class="card od-country-guide od-keyword-topic" data-topic="shipping">',
            inject + '<div class="card od-country-guide od-keyword-topic" data-topic="shipping">',
            1,
        )
    # Soften keyword hero that pushes generic shipping europe
    html = html.replace(
        "<h2><span class=\"od-flag-emoji\" aria-hidden=\"true\">🇫🇷</span> Mots-clés livraison — France</h2>",
        "<h2><span class=\"od-flag-emoji\" aria-hidden=\"true\">🇫🇷</span> Livraison locale — France (pas Spreadsheet hub)</h2>",
        1,
    )
    if 'id="local"' not in html:
        html = html.replace(
            '<div class="card od-live-panel" id="od-live-help-wrap">',
            f"{LOCAL_LIVRAISON}\n" + '<div class="card od-live-panel" id="od-live-help-wrap">',
            1,
        )
    if 'id="delais-colissimo"' not in html:
        html = html.replace(
            "<h2>Douane UE</h2>",
            f"{THICKEN_LIVRAISON}\n  <h2>Douane UE</h2>",
            1,
        )
    return html


def deepen_spreadsheet(html: str) -> str:
    html = _inject_head_style(html)
    html = _soften_brand(html)
    html = _strip_twin_hreflang(html)
    new_title = "MuleBuy desk France — Colissimo / douane (pas Spreadsheet hub)"
    html = re.sub(r"<title>.*?</title>", f"<title>{new_title}</title>", html, count=1, flags=re.S)
    html = re.sub(
        r'property="og:title" content="[^"]*"',
        f'property="og:title" content="{new_title}"',
        html,
        count=1,
    )
    html = re.sub(
        r'name="description" content="[^"]*"',
        'name="description" content="Desk FR MuleBuy : Colissimo, douane.gouv.fr, CP à cinq chiffres. Brand Spreadsheet / Independent Index · 8,000+ → bestmulebuysheets.com."',
        html,
        count=1,
    )
    html = re.sub(
        r'property="og:description" content="[^"]*"',
        'property="og:description" content="Desk FR — pas un second Spreadsheet hub. Catalogue → bestmulebuysheets.com."',
        html,
        count=1,
    )
    html = html.replace(
        '"name": "Mulebuy Spreadsheet 2026 — Liens W2C"',
        '"name": "MuleBuy desk France — Colissimo / douane (pas Spreadsheet hub)"',
    )
    # Kill spreadsheet keyword hero framing
    html = html.replace(
        "<h2><span class=\"od-flag-emoji\" aria-hidden=\"true\">🇫🇷</span> Mots-clés spreadsheet — France</h2>",
        "<h2><span class=\"od-flag-emoji\" aria-hidden=\"true\">🇫🇷</span> Desk FR — intention spreadsheet → hub</h2>",
        1,
    )
    html = html.replace(
        "<h3>Finds &amp; spreadsheet (France)</h3>"
        "<p><strong>mulebuy spreadsheet</strong>, <strong>spreadsheet mulebuy</strong>, "
        "<strong>mulebuy sheets</strong> et <strong>mulebuy spreadsheet 2025</strong> — hub live W2CLinks "
        '(<a href="https://w2clinks.com/spreadsheet/mulebuy/" target="_blank" rel="noopener">spreadsheet</a>).</p>',
        "<h3>Finds France → hub brand</h3>"
        "<p>Les requêtes exactes <em>mulebuy spreadsheet</em> / <em>spreadsheet mulebuy</em> appartiennent au hub "
        f'<a href="{HUB}/">bestmulebuysheets.com</a> (Independent Index · 8,000+). '
        "Ce desk .fr ne concurrence pas ce catalogue.</p>",
        1,
    )
    # Inject H1 + uplink before keyword card
    if 'class="fr-desk-hero"' not in html:
        inject = (
            f'<div class="fr-desk-hero" data-fr-deepen="{STAMP}">\n'
            "  <h1>Desk MuleBuy France — pas un second Spreadsheet hub</h1>\n"
            "  <p class=\"lead\">Atterrissage local (Colissimo / douane.gouv.fr / CP à cinq chiffres). "
            f"Independent Index · 8,000+, coupons et dataset → "
            f'<a href="{HUB}/">bestmulebuysheets.com</a>. Maj {TODAY_FR}.</p>\n'
            f"  {HUB_UPLINK}\n"
            "</div>\n"
        )
        html = html.replace(
            '<div class="card od-country-guide od-keyword-topic" data-topic="spreadsheet">',
            inject + '<div class="card od-country-guide od-keyword-topic" data-topic="spreadsheet">',
            1,
        )
    if 'id="local"' not in html:
        html = html.replace(
            '<div class="card" id="spreadsheet-products">',
            f"{LOCAL_SHEET}\n" + '<div class="card" id="spreadsheet-products">',
            1,
        )
    if 'id="cede-hub"' not in html:
        html = html.replace(
            "<h2>Derniers finds du tableur</h2>",
            f"{THICKEN_SHEET}\n  <h2>Derniers finds du tableur</h2>",
            1,
        )
    # Soften finds CTA toward hub
    html = html.replace(
        "En direct depuis W2CLinks — acheter via Mulebuy. "
        '<a href="https://w2clinks.com/spreadsheet/mulebuy/" target="_blank" rel="noopener">Ouvrir le tableur</a>.',
        "Aperçu local. Catalogue brand / Independent Index → "
        f'<a href="{HUB}/">bestmulebuysheets.com</a> · '
        f'<a href="{HUB}/finds-dataset/">finds-dataset</a>.',
        1,
    )
    return html


def deepen_coupons(html: str) -> str:
    html = _inject_head_style(html)
    html = _soften_brand(html)
    html = _strip_twin_hreflang(html)
    new_title = "Coupons MuleBuy France — landing EUR · vérité sur hub"
    html = re.sub(r"<title>.*?</title>", f"<title>{new_title}</title>", html, count=1, flags=re.S)
    html = re.sub(
        r'property="og:title" content="[^"]*"',
        f'property="og:title" content="{new_title}"',
        html,
        count=1,
    )
    html = re.sub(
        r'name="description" content="[^"]*"',
        'name="description" content="Landing coupons MuleBuy France (EUR). Table vérité → bestmulebuysheets.com/mulebuy-coupons. Coupon ≠ douane / Colissimo."',
        html,
        count=1,
    )
    html = re.sub(
        r'property="og:description" content="[^"]*"',
        'property="og:description" content="Coupons FR — vérité globale sur bestmulebuysheets.com. Coupon ≠ douane."',
        html,
        count=1,
    )
    html = html.replace(
        '"name": "Coupon Mulebuy France 2026 — 200345875"',
        f'"name": "{new_title}"',
    )
    html = html.replace(
        '<span class="od-badge">Independent Mulebuy Spreadsheet Guide</span>\n'
        "    <h1>Coupon Mulebuy 2026 — 200345875</h1>\n"
        "    <p class=\"lead\">mulebuy coupon et mulebuy coupon code — confirmez les promos actives dans le wallet après inscription avec 200345875.</p>",
        '<span class="od-badge">Desk FR · coupons locaux</span>\n'
        "    <h1>Coupons MuleBuy France — EUR · vérité sur hub</h1>\n"
        "    <p class=\"lead\">Landing coupon FR. Table vérité globale → "
        f'<a href="{HUB}/mulebuy-coupons/">bestmulebuysheets.com/mulebuy-coupons</a>. '
        f"Maj {TODAY_FR}. Coupon ≠ douane.gouv.fr / Colissimo Collect.</p>\n"
        f"    {HUB_UPLINK}",
        1,
    )
    html = html.replace(
        "<h2><span class=\"od-flag-emoji\" aria-hidden=\"true\">🇫🇷</span> Mots-clés coupon &amp; parrainage — France</h2>",
        "<h2><span class=\"od-flag-emoji\" aria-hidden=\"true\">🇫🇷</span> Coupons FR — vérité hub</h2>",
        1,
    )
    if 'id="local"' not in html:
        # After hero / promo, before keyword card
        html = html.replace(
            '<div class="card od-country-guide od-keyword-topic" data-topic="coupons">',
            f"{LOCAL_COUPONS}\n"
            '<div class="card od-country-guide od-keyword-topic" data-topic="coupons">',
            1,
        )
    if 'id="hub-truth"' not in html:
        html = html.replace(
            "<h2>Coupons Mulebuy en France</h2>",
            f"{THICKEN_COUPONS}\n  <h2>Coupons Mulebuy en France</h2>",
            1,
        )
    return html


BUILDERS = {
    "mulebuy-shipping": deepen_shipping,
    "livraison-mulebuy": deepen_livraison,
    "mulebuy-spreadsheet": deepen_spreadsheet,
    "mulebuy-coupons": deepen_coupons,
}


def _assert_ok(slug: str, deepened: str) -> None:
    for must in (
        'id="local"',
        'class="hub-uplink"',
        "Colissimo",
        "douane.gouv.fr",
        HUB,
        f'data-fr-deepen="{STAMP}"',
        "finds-dataset",
    ):
        if must not in deepened:
            raise SystemExit(f"{slug}: missing {must}")
    if "mulebuyspreadsheets." in deepened and "hreflang" in deepened:
        # twin hosts must not remain as alternate
        if re.search(
            r'rel="alternate"[^>]*mulebuyspreadsheets\.(?:es|us|co\.uk)',
            deepened,
        ):
            raise SystemExit(f"{slug}: twin hreflang still present")
    if re.search(r"<h1[^>]*>[^<]*Spreadsheet 2026", deepened, re.I):
        raise SystemExit(f"{slug}: H1 still Spreadsheet hero")
    if re.search(r"<h1[^>]*>[^<]*Mulebuy Spreadsheet", deepened, re.I):
        raise SystemExit(f"{slug}: H1 still Spreadsheet hero")
    title_m = re.search(r"<title>(.*?)</title>", deepened, re.S | re.I)
    if title_m:
        t = title_m.group(1)
        if re.search(r"Mulebuy Spreadsheet 2026|Spreadsheet en français", t, re.I):
            raise SystemExit(f"{slug}: <title> still Spreadsheet hero: {t}")
        if "Spreadsheet" in t and "pas Spreadsheet" not in t and "not Spreadsheet" not in t:
            # shipping/coupons titles should not say Spreadsheet at all
            if slug != "mulebuy-spreadsheet":
                raise SystemExit(f"{slug}: <title> still mentions Spreadsheet: {t}")


def build() -> dict[str, Path]:
    out: dict[str, Path] = {}
    for slug in PAGES:
        base = OVERLAY / slug / "live-base.index.html"
        if not base.exists():
            raise SystemExit(f"missing live base: {base}")
        deepened = BUILDERS[slug](base.read_text(errors="replace"))
        _assert_ok(slug, deepened)
        dest = OVERLAY / slug / "index.html.fr-deepen"
        dest.write_text(deepened)
        out[slug] = dest
        print("BUILT", dest, "bytes", dest.stat().st_size)
    return out


def deploy(built: dict[str, Path], store_internal: Path | None) -> dict:
    client = _connect()
    bak = f"/www/backup/mulebuy-fr-deepen-{datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%S')}"
    cmds = [f"mkdir -p '{bak}'"]
    for slug in PAGES:
        cmds.append(
            f"cp -a '{REMOTE}/{slug}/index.html' '{bak}/{slug}-index.html.before' 2>/dev/null || true"
        )
    cmds.append(f"cp -a '{REMOTE}/sitemap.xml' '{bak}/sitemap.xml.before' 2>/dev/null || true")
    print(_run(client, " && ".join(cmds)))

    sftp = client.open_sftp()
    for slug, path in built.items():
        remote = f"{REMOTE}/{slug}/index.html"
        sftp.put(str(path), remote)
        print("PUT", remote)
    try:
        with sftp.open(f"{REMOTE}/sitemap.xml", "r") as fh:
            sm = fh.read().decode(errors="replace")
        for slug in PAGES:
            loc = f"https://{HOST}/{slug}/"
            sm = re.sub(
                rf"(<loc>{re.escape(loc)}</loc>\s*<lastmod>)[^<]+",
                rf"\g<1>{TODAY}",
                sm,
            )
            sm = re.sub(
                rf"(<url>\s*<loc>{re.escape(loc)}</loc>\s*)(?:<lastmod>[^<]*</lastmod>\s*)?",
                rf"\1<lastmod>{TODAY}</lastmod>\n",
                sm,
            )
        sm = re.sub(
            rf"(<loc>https://{re.escape(HOST)}/</loc>\s*<lastmod>)[^<]+",
            rf"\g<1>{TODAY}",
            sm,
        )
        tmp = f"/tmp/mulebuy-fr-sitemap-{STAMP}.xml"
        Path(tmp).write_text(sm)
        sftp.put(tmp, f"{REMOTE}/sitemap.xml")
        print("PUT sitemap.xml lastmod", TODAY)
    except Exception as exc:  # noqa: BLE001
        print("SITEMAP_WARN", exc)
    sftp.close()

    _run(
        client,
        " && ".join(
            [f"chown www:www '{REMOTE}/{slug}/index.html'" for slug in PAGES]
            + [f"chown www:www '{REMOTE}/sitemap.xml'"]
        ),
    )
    print("BACKUP", bak)
    meta = {"backup": bak, "stamp": STAMP, "pages": list(PAGES)}
    if store_internal:
        store_internal.mkdir(parents=True, exist_ok=True)
        (store_internal / "backup.txt").write_text(bak + "\n")
    client.close()
    return meta


def verify() -> dict:
    checks = []
    for slug in PAGES:
        url = f"https://{HOST}/{slug}/"
        req = Request(url, headers={"User-Agent": "mulebuy-fr-deepen/1.0"})
        with urlopen(req, timeout=30) as resp:
            body = resp.read().decode(errors="replace")
            code = resp.status
        row = {
            "url": url,
            "http": code,
            "id_local": 'id="local"' in body,
            "hub_uplink": "bestmulebuysheets.com" in body and "finds-dataset" in body,
            "colissimo": body.count("Colissimo"),
            "douane": body.lower().count("douane.gouv.fr"),
            "cp5": ("cinq chiffres" in body) or ("75001" in body),
            "data_fr_deepen": f'data-fr-deepen="{STAMP}"' in body,
            "twin_hreflang": bool(
                re.search(
                    r'rel="alternate"[^>]*mulebuyspreadsheets\.(?:es|us|co\.uk)',
                    body,
                )
            ),
            "spreadsheet_h1": bool(
                re.search(r"<h1[^>]*>[^<]*(Mulebuy Spreadsheet|Spreadsheet 2026)", body, re.I)
            ),
        }
        m = re.search(r"<title>(.*?)</title>", body, re.S | re.I)
        row["title"] = re.sub(r"\s+", " ", m.group(1)).strip() if m else None
        checks.append(row)

    # homepage + hub untouched markers
    for label, url in (("home", f"https://{HOST}/"), ("hub", f"{HUB}/")):
        req = Request(url, headers={"User-Agent": "mulebuy-fr-deepen/1.0"})
        with urlopen(req, timeout=30) as resp:
            body = resp.read().decode(errors="replace")
            code = resp.status
        checks.append(
            {
                "url": url,
                "label": label,
                "http": code,
                "data_fr_deepen": f'data-fr-deepen="{STAMP}"' in body,
            }
        )

    twin_rows = []
    for t in (
        "https://mulebuyspreadsheets.co.uk/",
        "https://mulebuyspreadsheets.es/",
        "https://mulebuyspreadsheets.us/",
    ):
        u = urlparse(t)
        conn = http.client.HTTPSConnection(u.netloc, timeout=20)
        conn.request("GET", u.path or "/", headers={"User-Agent": "mulebuy-fr-deepen/1.0"})
        r = conn.getresponse()
        twin_rows.append({"url": t, "http": r.status, "location": r.getheader("Location")})
        conn.close()
    return {
        "at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "checks": checks,
        "twins": twin_rows,
    }


def gsc_submit(sa: Path, out_path: Path) -> dict:
    try:
        from google.oauth2 import service_account
        from googleapiclient.discovery import build
    except ImportError:
        import subprocess

        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "google-api-python-client", "google-auth", "-q"]
        )
        from google.oauth2 import service_account
        from googleapiclient.discovery import build

    creds = service_account.Credentials.from_service_account_file(
        str(sa),
        scopes=["https://www.googleapis.com/auth/webmasters"],
    )
    gsc = build("searchconsole", "v1", credentials=creds, cache_discovery=False)
    site = f"sc-domain:{HOST}"
    feed = f"https://{HOST}/sitemap.xml"
    gsc.sitemaps().submit(siteUrl=site, feedpath=feed).execute()
    time.sleep(1)
    listed = gsc.sitemaps().list(siteUrl=site).execute()
    result = {
        "site": site,
        "feed": feed,
        "submitted_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "list": listed,
    }
    out_path.write_text(json.dumps(result, indent=2) + "\n")
    print("GSC_SUBMIT", site, feed)
    return result


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--load-env", type=Path, help="usfans-ssh.env with HOST= and RAW_LINE=")
    ap.add_argument("--build-only", action="store_true")
    ap.add_argument("--deploy", action="store_true")
    ap.add_argument("--verify", action="store_true")
    ap.add_argument("--gsc", action="store_true")
    ap.add_argument(
        "--store-internal",
        type=Path,
        default=None,
        help="Project store internal/mulebuy-fr-deepen",
    )
    ap.add_argument("--gsc-sa", type=Path, default=None)
    args = ap.parse_args()
    if args.load_env:
        _load_env(args.load_env)
    built = build()
    if args.build_only and not args.deploy:
        return
    meta: dict = {}
    if args.deploy:
        meta = deploy(built, args.store_internal)
    if args.verify or args.deploy:
        time.sleep(2)
        ver = verify()
        ver["backup"] = meta.get("backup")
        if args.store_internal:
            args.store_internal.mkdir(parents=True, exist_ok=True)
            (args.store_internal / "live_verify.json").write_text(
                json.dumps(ver, indent=2) + "\n"
            )
        print(json.dumps(ver, indent=2))
        bad = [
            c
            for c in ver["checks"]
            if c.get("url", "").startswith(f"https://{HOST}/")
            and c.get("label") is None
            and (
                not c.get("id_local")
                or not c.get("hub_uplink")
                or not c.get("data_fr_deepen")
                or not c.get("colissimo")
                or not c.get("douane")
                or c.get("twin_hreflang")
                or c.get("spreadsheet_h1")
                or c.get("http") != 200
            )
        ]
        # home/hub must NOT have data-fr-deepen
        untouched_bad = [
            c
            for c in ver["checks"]
            if c.get("label") in ("home", "hub")
            and (c.get("http") != 200 or c.get("data_fr_deepen"))
        ]
        twin_bad = [
            t
            for t in ver.get("twins", [])
            if t.get("http") not in (301, 302)
            or not (t.get("location") or "").startswith(HUB)
        ]
        if bad or twin_bad or untouched_bad:
            print("VERIFY_FAIL", bad, twin_bad, untouched_bad)
            sys.exit(2)
        print("VERIFY_OK")
    if args.gsc:
        sa = args.gsc_sa
        if not sa:
            raise SystemExit("--gsc-sa required")
        out = (args.store_internal or Path("/tmp")) / "gsc_sitemap_submit.json"
        gsc_submit(sa, out)


if __name__ == "__main__":
    main()
