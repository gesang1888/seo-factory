#!/usr/bin/env python3
"""Scrub consumer-facing ops/SEO notes across Kakobuy portfolio sites.

Preference (2026-10-29): desk labels, LATAM overflow policy, twin/skip rationale,
"Desk ES · …", Phase C notes — docs/internal only. Keep real local content
(Correos/AEAT, Posti, USPS, hub uplink).

Fetches LIVE HTML, rewrites ops copy, writes overlays, deploys via Baota SSH.
Also patches builders so rebuild will not reinject consumer ops notes.

Requires ORIGIN_SSH_PASS (or --load-env internal/usfans-ssh.env).
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
STORE = Path("/cursor/stores/bc-eb8405c7-0d3c-48be-958d-5f25b92c606c")
STAMP = "20261029"
TAG = f"kakobuy-ops-scrub-{STAMP}"
SUFFIX = "ops-scrub"

# Consumer-visible forbidden ops needles (case-insensitive substring).
FORBIDDEN = (
    "Desk ES ·",
    "Desk CA ·",
    "Desk FI ·",
    "Desk ES independiente",
    "Keep desks",
    "keep desks",
    "Do not revive",
    "do not revive",
    "Phase A/B/C",
    "Phase A/",
    "Twins tips",
    "twins tips",
    "Twins 301",
    "hub reclaim",
    "Hub reclaim",
    "Not a dest-country skin",
    "not a dest-country skin",
    "local KPI only",
    "LATAM",
    "latam-note",
    "data-latam-overflow",
    "Sin twin LATAM",
    "KakobuyDocs · hub reclaim",
    "money URLs ≤6",
    "Hub ownership · money",
    "US keep desk",
    "keep desk",
    "Lab 1 oct 2026",
    "Lab 1 oct. 2026",
)

# Keep these (real local / hub content).
KEEP_HINTS = {
    "kakobuydocs.com": ("Independent Index", "USPS", "CBP"),
    "kakobuy.fi": ("Posti", "Tulli"),
    "kakospreadsheet.es": ("Correos", "AEAT"),
    "kakospreadsheet.ca": ("CBSA", "Canada"),
}

PAGES: dict[str, list[tuple[str, str]]] = {
    "kakobuydocs.com": [
        ("home", "/"),
        ("kakobuy-spreadsheet", "/kakobuy-spreadsheet/"),
        ("kakobuy-coupons", "/kakobuy-coupons/"),
        ("finds-dataset", "/finds-dataset/"),
        ("shipping-to-us", "/shipping-to-us/"),
    ],
    "kakobuy.fi": [
        ("home", "/"),
        ("kakobuy-kokemuksia", "/kakobuy-kokemuksia/"),
        ("kakobuy-toimitus", "/kakobuy-toimitus/"),
        ("kakobuy-shipping", "/kakobuy-shipping/"),
    ],
    "kakospreadsheet.es": [
        ("home", "/"),
        ("como-comprar-en-kakobuy", "/como-comprar-en-kakobuy/"),
        ("how-to-use-kakobuy", "/how-to-use-kakobuy/"),
        ("kakobuy-opiniones", "/kakobuy-opiniones/"),
        ("es-kakobuy-confiable", "/es-kakobuy-confiable/"),
        ("envio-kakobuy-espana", "/envio-kakobuy-espana/"),
        ("ayuda", "/ayuda/"),
    ],
    "kakospreadsheet.ca": [
        ("home", "/"),
        ("help", "/help/"),
    ],
}


def _load_env(path: Path) -> None:
    text = path.read_text()
    host = pass_val = None
    for line in text.splitlines():
        if line.startswith("HOST="):
            host = line.split("=", 1)[1].strip().strip('"').strip("'")
        if line.startswith("RAW_LINE="):
            raw = line.split("=", 1)[1]
            if (raw.startswith('"') and raw.endswith('"')) or (
                raw.startswith("'") and raw.endswith("'")
            ):
                raw = raw[1:-1]
            pass_val = raw
    if not host or not pass_val:
        raise SystemExit(f"HOST/RAW_LINE missing in {path}")
    os.environ.setdefault("ORIGIN_SSH_HOST", host)
    os.environ.setdefault("ORIGIN_SSH_PASS", pass_val)


def _fetch(url: str) -> str:
    req = Request(url, headers={"User-Agent": "kakobuy-ops-scrub/1.0"})
    with urlopen(req, timeout=45) as resp:
        return resp.read().decode("utf-8", errors="replace")


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
    return (stdout.read() + stderr.read()).decode(errors="replace").strip()


def scrub_html(html: str, host: str) -> str:
    """Rewrite consumer-visible ops/SEO notes; keep local fingerprints + hub uplink."""
    # LATAM callouts (defense — already stripped on ES LIVE).
    html = re.sub(
        r'<p\b[^>]*\b(?:class="[^"]*latam-note[^"]*"|data-latam-overflow=)[^>]*>.*?</p>\s*',
        "",
        html,
        flags=re.S | re.I,
    )
    html = re.sub(r"\.latam-note\{[^}]*\}", "", html)

    # --- Desk labels (consumer-visible) ---
    html = html.replace("Desk ES · fiable / envío / Correos", "España · fiable / envío / Correos")
    html = html.replace("Desk ES · intención local", "España · Correos / AEAT")
    html = html.replace("Desk ES · Correos / AEAT", "España · Correos / AEAT")
    html = html.replace("Desk CA · local intent", "Canada · CBSA / local shipping")
    html = html.replace("Desk FI ·", "Suomi ·")
    html = html.replace("<h3>Kakobuy desk ES</h3>", "<h3>Kakobuy España</h3>")
    html = html.replace("Desk independiente ES", "Guía independiente ES")
    html = html.replace(
        "Desk ES independiente: catálogo en inglés, almacén según Help oficial, estimador con destino España. Lab 1 oct 2026.",
        "Guía independiente para España: catálogo, almacén según Help oficial, estimador con destino España.",
    )
    html = html.replace(
        "Desk ES independiente. Catálogo en esta portada. /envio-kakobuy-espana/ se conserva. Lab 1 oct 2026. No copiamos un recuento de líneas ajeno.",
        "Guía independiente para España. Catálogo en esta portada. /envio-kakobuy-espana/ se conserva. No copiamos un recuento de líneas ajeno.",
    )
    html = html.replace("Lab 1 oct 2026.", "")
    html = html.replace("Lab 1 oct 2026", "")
    html = html.replace("Lab 1 oct. 2026.", "")
    html = html.replace("Lab 1 oct. 2026", "")
    # Soft "desk" in Spanish publisher names → guide
    html = html.replace('"Kakobuy desk"', '"Kakobuy España"')
    html = html.replace('"Kakobuy independent desk"', '"Kakobuy guía independiente"')
    html = html.replace(
        '"kakospreadsheet.ca independent desk"',
        '"kakospreadsheet.ca independent guide"',
    )
    html = html.replace("This desk cannot open a ticket", "This site cannot open a ticket")
    html = html.replace("this desk cannot open a ticket", "this site cannot open a ticket")

    # --- Hub ops banners / hero ---
    html = re.sub(
        r'<div class="ann">Independent Index · <strong>11,300\+</strong> · coupons KAKODOCS · twins tips/\.fr/\.nl 301→this hub · keep (<a href="https://kakobuy\.fi/">\.fi</a> / <a href="https://kakospreadsheet\.es/">\.es</a> / <a href="https://kakospreadsheet\.ca/">\.ca</a>) · (<a href="#official-promo">Official 图文</a>)</div>',
        r'<div class="ann">Independent Index · <strong>11,300+</strong> · coupons KAKODOCS · country guides \1 · \2</div>',
        html,
        count=1,
    )
    # shipping-to-us ann (ops "spreadsheet hero" / hub-only jargon softened)
    html = html.replace(
        '<div class="ann">Hub-only US shipping notes · <strong>not</strong> a spreadsheet hero · CTA → ',
        '<div class="ann">US shipping notes · CTA → ',
    )
    html = html.replace(
        '<div class="hbg">United States · USPS · CBP · ZIP · hub-only</div>',
        '<div class="hbg">United States · USPS · CBP · ZIP</div>',
    )

    # Meta / og descriptions with keep-desks / twin ops
    html = re.sub(
        r'(content=")([^"]*?)Keep desks:[^"]*?Confirm offers in-app\."',
        r'\1Kakobuy Independent Index · 11,300+ finds (not Excel / not a Google Sheet). Coupons + dataset on kakobuydocs.com. Country guides: kakobuy.fi / kakospreadsheet.es / kakospreadsheet.ca. Confirm offers in-app."',
        html,
    )
    html = re.sub(
        r'(content=")Independent Index · 11,300\+\. Coupons-truth JSON \+ finds dataset\. Keep FI/ES/CA desks\. Do not revive sunset twins\."',
        r'\1Independent Index · 11,300+. Coupons-truth JSON + finds dataset. Country guides: FI / ES / CA."',
        html,
    )
    html = re.sub(
        r'(content=")Kakobuy spreadsheet hub reclaim: ([^"]+)"',
        r'\1Kakobuy spreadsheet: \2"',
        html,
    )
    html = re.sub(
        r'(content=")Hub-only Kakobuy shipping-to-US notes: ([^"]*?) No US desk domain\."',
        r'\1Kakobuy shipping-to-US notes: \2"',
        html,
    )
    html = html.replace(
        'content="USPS / CBP / ZIP framing on the Kakobuy docs hub. Spreadsheet intent stays on /kakobuy-spreadsheet/."',
        'content="USPS / CBP / ZIP framing for Kakobuy US shipping. Spreadsheet / finds stay on /kakobuy-spreadsheet/."',
    )

    # FAQ JSON-LD Phase A/B/C + do not revive
    html = re.sub(
        r'\{"@type":"Question","name":"What happened to kakobuytips\.com and kakospreadsheet\.fr / \.nl\?","acceptedAnswer":\{"@type":"Answer","text":"[^"]*"\}\}',
        '{"@type":"Question","name":"Where are kakobuytips.com and kakospreadsheet.fr / .nl?","acceptedAnswer":{"@type":"Answer","text":"Those domains redirect to kakobuydocs.com. Country guides remain on kakobuy.fi, kakospreadsheet.es, and kakospreadsheet.ca."}}',
        html,
        count=1,
    )
    # shipping-to-us FAQ ops
    html = html.replace(
        '{"@type":"Question","name":"Does kakobuydocs.com open a United States keep desk?","acceptedAnswer":{"@type":"Answer","text":"No. This is a hub-only shipping-to-US page with USPS / CBP / ZIP framing. There is no .us Kakobuy desk and no new domain. Brand spreadsheet intent stays on /kakobuy-spreadsheet/ and /finds-dataset/."}}',
        '{"@type":"Question","name":"Is this a United States country guide?","acceptedAnswer":{"@type":"Answer","text":"No. This is a hub shipping-to-US page with USPS / CBP / ZIP framing. Brand spreadsheet / finds stay on /kakobuy-spreadsheet/ and /finds-dataset/."}}',
    )

    # Hero subcopy on hub home
    html = re.sub(
        r'<p class="hsub">Brand spreadsheet SERP belongs here \(not on FI/ES/CA desks\)\. Typesense <code>found=11365</code> \(27 Oct 2026\)\. Ranked shipping / spreadsheet / how-to stay 200\. Not Excel / not a Google Sheet\. Twins <strong>kakobuytips\.com</strong> \+ <strong>kakospreadsheet\.fr/\.nl</strong> already 301→this hub — do not revive\.</p>',
        '<p class="hsub">Brand spreadsheet SERP belongs here. Typesense <code>found=11365</code> (27 Oct 2026). Ranked shipping / spreadsheet / how-to stay live. Not Excel / not a Google Sheet. Country guides: <a href="https://kakobuy.fi/">.fi</a> · <a href="https://kakospreadsheet.es/">.es</a> · <a href="https://kakospreadsheet.ca/">.ca</a>.</p>',
        html,
        count=1,
    )
    html = html.replace(
        '<div class="hs"><div class="hsn">FI·ES·CA</div><div class="hsl">keep desks</div></div>',
        '<div class="hs"><div class="hsn">FI·ES·CA</div><div class="hsl">country guides</div></div>',
    )

    # Hub #local ownership box — rewrite ops list to consumer links
    html = re.sub(
        r'<div class="local-box" id="local"[^>]*>\s*<h2>Hub ownership · money URLs ≤6</h2>\s*<ol>.*?</ol>\s*<p class="money">.*?</p>\s*</div>',
        (
            '<div class="local-box" id="local" data-ops-scrub="'
            + STAMP
            + '">'
            "<h2>Start here on this hub</h2>"
            "<ol>"
            '<li><strong>Spreadsheet / finds</strong> — <a href="/kakobuy-spreadsheet/">/kakobuy-spreadsheet/</a> · <a href="/finds-dataset/">/finds-dataset/</a></li>'
            '<li><strong>Coupons</strong> — <a href="/kakobuy-coupons/">/kakobuy-coupons/</a> · truth JSON</li>'
            '<li><strong>How-to / legit / shipping</strong> — ranked guides on this host</li>'
            '<li><strong>Country guides</strong> — <a href="https://kakobuy.fi/">kakobuy.fi</a> (Posti/Tulli) · <a href="https://kakospreadsheet.es/">.es</a> (Correos) · <a href="https://kakospreadsheet.ca/">.ca</a> (CBSA)</li>'
            '<li><strong>US shipping</strong> — <a href="/shipping-to-us/">/shipping-to-us/</a> (USPS · CBP · ZIP)</li>'
            "</ol>"
            '<p class="money">Also: <a href="/">/</a> · <a href="/how-to-use-kakobuy/">how-to</a> · <a href="/is-kakobuy-legit/">legit</a></p>'
            "</div>"
        ),
        html,
        count=1,
        flags=re.S,
    )

    # Trust strip / footer / legal notes
    html = html.replace("Not a dest-country skin", "Independent of kakobuy.com checkout")
    html = html.replace("not a dest-country skin", "independent of kakobuy.com checkout")
    html = html.replace(
        "This host is not a dest-country skin.",
        "This host is independent of kakobuy.com checkout.",
    )
    html = re.sub(
        r"Not a dest-country skin\. Twins tips/\.fr/\.nl 301→here\.",
        "Independent guide — not kakobuy.com checkout.",
        html,
    )
    html = re.sub(
        r"Not a dest-country skin\. Twins tips/\.fr/\.nl stay 301→hub\.",
        "Independent guide — not kakobuy.com checkout.",
        html,
    )
    html = re.sub(
        r" · Twins tips/\.fr/\.nl 301→here\.",
        ".",
        html,
    )
    html = re.sub(
        r"Twins tips/\.fr/\.nl 301→here\. ",
        "",
        html,
    )
    html = re.sub(
        r"Twins tips/\.fr/\.nl stay 301→hub\.",
        "",
        html,
    )
    html = re.sub(
        r"Twins tips/\.fr/\.nl 301→hub — do not revive\.",
        "",
        html,
    )
    html = re.sub(
        r" Copy reviewed 27 Oct 2026\. Twins tips/\.fr/\.nl 301→hub — do not revive\.",
        " Copy reviewed 27 Oct 2026.",
        html,
    )
    html = re.sub(
        r'<br><span style="opacity:\.7">twins tips/\.fr/\.nl → 301 hub</span>',
        "",
        html,
    )
    html = html.replace(
        "<p><strong>Keep desks / official</strong></p>",
        "<p><strong>Country guides / official</strong></p>",
    )
    html = html.replace(
        "kakobuydocs.com — Kakobuy primary hub. Independent Index · 11,300+. Not Excel. Not a Google Sheet. Not a dest-country skin. Twins tips/.fr/.nl 301→here.",
        "kakobuydocs.com — Kakobuy primary hub. Independent Index · 11,300+. Not Excel. Not a Google Sheet. Independent of kakobuy.com checkout.",
    )
    # In case previous replace already changed dest-country
    html = html.replace(
        "kakobuydocs.com — Kakobuy primary hub. Independent Index · 11,300+. Not Excel. Not a Google Sheet. Independent of kakobuy.com checkout. Twins tips/.fr/.nl 301→here.",
        "kakobuydocs.com — Kakobuy primary hub. Independent Index · 11,300+. Not Excel. Not a Google Sheet. Independent of kakobuy.com checkout.",
    )

    # Spreadsheet reclaim box / hero
    html = re.sub(
        r"<!-- Hero — hub reclaim 20261027 -->",
        "<!-- Hero — spreadsheet -->",
        html,
    )
    html = re.sub(
        r"Compete for <em>kakobuy spreadsheet</em> with a falsifiable index: row_count <strong>11365</strong> · stamp <time datetime=\"2026-10-27\">2026-10-27</time> · <a href=\"/data/finds-dataset\.json\">finds-dataset\.json</a> · <a href=\"/data/coupons-truth\.json\">coupons-truth\.json</a>\. Keep desks <a href=\"https://kakobuy\.fi/\">kakobuy\.fi</a> / <a href=\"https://kakospreadsheet\.es/\">\.es</a> / <a href=\"https://kakospreadsheet\.ca/\">\.ca</a> stay local \(Posti / Correos / CBSA\)\. Twins <strong>kakobuytips\.com</strong> · <strong>kakospreadsheet\.fr</strong> · <strong>\.nl</strong> already <strong>301→this hub</strong> — do not revive\.",
        'Compete for <em>kakobuy spreadsheet</em> with a falsifiable index: row_count <strong>11365</strong> · stamp <time datetime="2026-10-27">2026-10-27</time> · <a href="/data/finds-dataset.json">finds-dataset.json</a> · <a href="/data/coupons-truth.json">coupons-truth.json</a>. Country guides: <a href="https://kakobuy.fi/">kakobuy.fi</a> (Posti) · <a href="https://kakospreadsheet.es/">.es</a> (Correos) · <a href="https://kakospreadsheet.ca/">.ca</a> (CBSA).',
        html,
    )
    html = re.sub(
        r'<section class="docs-gsc-extra"[^>]*data-hub-reclaim="[^"]*"[^>]*>'
        r'<p style="font-size:12px;font-weight:700;color:#cc4d1f;text-transform:uppercase">KakobuyDocs · hub reclaim</p>',
        '<section class="docs-gsc-extra" style="max-width:960px;margin:28px auto;padding:28px;background:#fff7f2;border:1px solid #ffd5c2;border-radius:14px;color:#1a1a1a;line-height:1.75" data-ops-scrub="'
        + STAMP
        + '">'
        '<p style="font-size:12px;font-weight:700;color:#cc4d1f;text-transform:uppercase">KakobuyDocs · Independent Index</p>',
        html,
        count=1,
    )
    html = re.sub(
        r"<p>Keep FI/ES/CA local\. Do not revive tips/\.fr/\.nl twins\.</p>",
        "<p>Country guides: FI / ES / CA for local postal context.</p>",
        html,
    )
    html = re.sub(
        r'<p class="legal-note">Keep desks: kakobuy\.fi · kakospreadsheet\.es · kakospreadsheet\.ca \(local KPI only\)\. Twins kakobuytips\.com · kakospreadsheet\.fr · \.nl → 301 this hub \(do not revive\)\. Copy reviewed 27 Oct 2026\.</p>',
        '<p class="legal-note">Country guides: kakobuy.fi · kakospreadsheet.es · kakospreadsheet.ca. Copy reviewed 27 Oct 2026.</p>',
        html,
    )
    html = re.sub(
        r"Keep desks <a href=\"https://kakobuy\.fi/\">kakobuy\.fi</a> / <a href=\"https://kakospreadsheet\.es/\">\.es</a> / <a href=\"https://kakospreadsheet\.ca/\">\.ca</a>",
        'Country guides <a href="https://kakobuy.fi/">kakobuy.fi</a> / <a href="https://kakospreadsheet.es/">.es</a> / <a href="https://kakospreadsheet.ca/">.ca</a>',
        html,
    )

    # finds-dataset
    html = re.sub(
        r"<h2>Keep desks / twins</h2>\s*<p>Keep: (<a href=\"https://kakobuy\.fi/\">kakobuy\.fi</a>) · (<a href=\"https://kakospreadsheet\.es/\">kakospreadsheet\.es</a>) · (<a href=\"https://kakospreadsheet\.ca/\">kakospreadsheet\.ca</a>)\. Twins 301→hub: kakobuytips\.com · kakospreadsheet\.fr · kakospreadsheet\.nl\. Do not revive sunsets\.</p>",
        r"<h2>Country guides</h2>\n<p>\1 · \2 · \3 — Posti / Correos / CBSA local context. Brand spreadsheet stays on this hub.</p>",
        html,
    )
    html = re.sub(
        r"FI/ES/CA keep local postal KPI\.",
        "FI / ES / CA cover local postal context.",
        html,
    )

    # shipping-to-us body ops
    html = html.replace(
        "This page is <strong>not</strong> a Kakobuy Spreadsheet hero and does <strong>not</strong> open a .us desk. Brand finds stay on the Independent Index.",
        "This page covers US shipping / customs framing. Brand finds stay on the Independent Index.",
    )
    html = re.sub(
        r"<p><strong>Is:</strong> hub-only conversion surface for USA brand/workflow impressions that currently show with near-zero CTR\. Named USPS · CBP · ZIP so the SERP snippet is not a generic DHL table\.</p>\s*"
        r"<p><strong>Is not:</strong> a second Independent Index, a Google Sheet clone, a US keep desk, or a new domain \(no kakobuys\.co\.uk either — UK lookalikes stay vetoed\)\.</p>",
        "<p><strong>Is:</strong> USPS · CBP · ZIP notes for buyers shipping to the United States from Kakobuy.</p>\n"
        "<p><strong>Is not:</strong> a second Independent Index or a Google Sheet clone — spreadsheet / finds stay on <a href=\"/kakobuy-spreadsheet/\">/kakobuy-spreadsheet/</a>.</p>",
        html,
        count=1,
    )
    html = html.replace(
        '<p><a href="/kakobuy-spreadsheet/">/kakobuy-spreadsheet/</a> · <a href="/finds-dataset/">/finds-dataset/</a> · <a href="/kakobuy-coupons/">/kakobuy-coupons/</a> · <a href="/">hub home</a>. Keep desks remain FI/ES/CA only.</p>',
        '<p><a href="/kakobuy-spreadsheet/">/kakobuy-spreadsheet/</a> · <a href="/finds-dataset/">/finds-dataset/</a> · <a href="/kakobuy-coupons/">/kakobuy-coupons/</a> · <a href="/">hub home</a>. Country guides: FI / ES / CA.</p>',
    )
    html = re.sub(
        r"<summary>Is this a United States keep desk\?</summary>\s*"
        r"<p>No\. kakobuydocs\.com stays the English brand hub\. FI / ES / CA are the only keep desks\. This URL only deepens US shipping intent on the hub\.</p>",
        "<summary>Is this a United States country guide?</summary>\n"
        "<p>No. kakobuydocs.com stays the English brand hub. Country guides are on kakobuy.fi, kakospreadsheet.es, and kakospreadsheet.ca. This URL deepens US shipping notes on the hub.</p>",
        html,
        count=1,
    )
    html = re.sub(
        r"<p>kakobuydocs\.com — hub-only /shipping-to-us/ · tag [^<]+?\. Not Excel\. Independent of kakobuy\.com checkout\.\s*</p>",
        "<p>kakobuydocs.com — /shipping-to-us/. Not Excel. Independent of kakobuy.com checkout.</p>",
        html,
    )
    html = re.sub(
        r"<p>kakobuydocs\.com — hub-only /shipping-to-us/ · tag [^<]+?\.</p>",
        "<p>kakobuydocs.com — /shipping-to-us/. Not Excel. Independent of kakobuy.com checkout.</p>",
        html,
    )

    # Guides card "Hub reclaim money URL"
    html = html.replace(
        "Hub reclaim money URL. Open directory + dataset + coupons.",
        "Open directory + dataset + coupons.",
    )
    html = html.replace("Money URLs ≤6:", "Key URLs:")
    html = html.replace("money URLs ≤6", "key URLs")
    html = html.replace("Money URLs ≤6", "Key URLs")

    # Coupons footer twin line already handled; Sister country hosts ops soft rewrite
    html = html.replace(
        "Sister country hosts stay separate files — no 301.",
        "Country guides stay on their own hosts.",
    )

    # Hub home #us-intent block (gap R2) — strip keep-desk / new-domain ops jargon
    html = html.replace(
        "There is no US keep desk.",
        "Country guides remain on .fi / .es / .ca.",
    )
    html = html.replace(
        "There is <strong>no</strong> US keep desk and <strong>no</strong> new domain. ",
        "",
    )
    html = html.replace(
        "There is no US keep desk and no new domain. ",
        "",
    )
    html = html.replace(
        '{"@type":"Question","name":"Is kakobuydocs.com a dest-country skin?","acceptedAnswer":{"@type":"Answer","text":"No. This hostname is the English brand hub / docs',
        '{"@type":"Question","name":"Is kakobuydocs.com the official Kakobuy checkout?","acceptedAnswer":{"@type":"Answer","text":"No. This hostname is the English brand hub / docs',
    )
    html = re.sub(
        r'(?i)dest-country skin',
        'official Kakobuy checkout',
        html,
    )
    # Residual "keep desk(s)" after partial rewrites
    html = re.sub(r"(?i)US keep desks?", "US country guide", html)
    html = re.sub(r"(?i)keep desks?", "country guides", html)
    html = re.sub(r"(?i)a United States country guides", "a United States country guide", html)

    # llms.txt style lines if present in HTML (usually separate file)
    html = re.sub(
        r"Keep country desks \(kakobuy\.fi / kakospreadsheet\.es / kakospreadsheet\.ca\) for local postal KPI\. Twins kakobuytips\.com \+ kakospreadsheet\.fr/\.nl 301→this hub\. Do not revive sunsets\.",
        "Country guides: kakobuy.fi / kakospreadsheet.es / kakospreadsheet.ca for local postal context.",
        html,
    )

    # Generic leftover twin/skip phrases
    html = re.sub(r"\s*Do not revive sunset twins\.?", "", html, flags=re.I)
    html = re.sub(r"\s*Do not revive sunsets\.?", "", html, flags=re.I)
    html = re.sub(r"\s*— do not revive\.?", "", html, flags=re.I)
    html = re.sub(r"\s*\(do not revive\)\.?", "", html, flags=re.I)
    html = re.sub(r"\s*Do not revive tips/\.fr/\.nl twins\.?", "", html, flags=re.I)

    # Internal data-* stamps that embed ops jargon (not consumer-visible but reinject risk)
    html = re.sub(
        r'\s*data-hub-reclaim="[^"]*"',
        f' data-ops-scrub="{STAMP}"',
        html,
    )
    html = re.sub(
        r'data-platform-opt="kakobuy-hub-reclaim-[^"]*"',
        f'data-ops-scrub="{STAMP}"',
        html,
    )

    # Stamp
    needle = f"<!-- {TAG} -->"
    if needle not in html:
        html = html.replace("<head>", f"<head>\n{needle}", 1)
    if f'data-ops-scrub="{STAMP}"' not in html:
        html = re.sub(r"<body([^>]*)>", rf'<body\1 data-ops-scrub="{STAMP}">', html, count=1)

    return html


def _overlay_dest(host: str, slug: str) -> Path:
    overlay = ROOT / "sites" / host / "overlay"
    if slug == "home":
        return overlay / f"index.html.{SUFFIX}"
    return overlay / slug / f"index.html.{SUFFIX}"


def _visible_text(html: str) -> str:
    """Rough consumer-visible text: drop scripts/styles/comments/attrs."""
    t = re.sub(r"(?is)<script\b[^>]*>.*?</script>", " ", html)
    t = re.sub(r"(?is)<style\b[^>]*>.*?</style>", " ", t)
    t = re.sub(r"(?is)<!--.*?-->", " ", t)
    t = re.sub(r"(?is)<[^>]+>", " ", t)
    return re.sub(r"\s+", " ", t)


def forbidden_hits(html: str) -> list[str]:
    # Check meta/og/JSON-LD + visible text (attrs alone are not consumer copy).
    meta_chunks = " ".join(
        re.findall(r'(?is)<meta[^>]+content="([^"]*)"', html)
        + re.findall(r"(?is)<title>(.*?)</title>", html)
        + re.findall(r"(?is)<script type=\"application/ld\+json\">(.*?)</script>", html)
    )
    hay = (meta_chunks + " " + _visible_text(html)).lower()
    hits = []
    for n in FORBIDDEN:
        key = n.lower()
        if key not in hay:
            continue
        if key in ("keep desk", "keep desks", "us keep desk") and "keep desk" not in hay:
            continue
        if key in ("not a dest-country skin",) and "dest-country skin" not in hay:
            continue
        hits.append(n)
    seen: set[str] = set()
    out: list[str] = []
    for h in hits:
        if h.lower() in seen:
            continue
        seen.add(h.lower())
        out.append(h)
    return out


def build_all() -> dict:
    built: dict[str, dict[str, Path]] = {}
    for host, pages in PAGES.items():
        built[host] = {}
        for slug, path in pages:
            url = f"https://{host}{path}"
            print(f"build {host}{path} …")
            live = _fetch(url)
            scrubbed = scrub_html(live, host)
            bad = forbidden_hits(scrubbed)
            if bad:
                # Write debug then fail
                dbg = ROOT / "sites" / host / "overlay" / f"_scrub-debug-{slug}.html"
                dbg.parent.mkdir(parents=True, exist_ok=True)
                dbg.write_text(scrubbed)
                raise SystemExit(f"{url}: still has ops needles {bad}; wrote {dbg}")
            # Keep local content
            for hint in KEEP_HINTS.get(host, ()):
                if hint not in scrubbed and host != "kakobuydocs.com":
                    # hub home may not have USPS; shipping-to-us must
                    if host == "kakobuydocs.com" and slug != "shipping-to-us" and hint in (
                        "USPS",
                        "CBP",
                    ):
                        continue
                    if host == "kakospreadsheet.es" and slug == "ayuda" and hint == "AEAT":
                        # ayuda may mention Agencia Tributaria instead
                        if "Agencia Tributaria" in scrubbed or "Correos" in scrubbed:
                            continue
                    if hint not in scrubbed:
                        print(f"  WARN missing keep hint {hint!r} on {url}")
            if host == "kakobuydocs.com" and slug == "shipping-to-us":
                for must in ("USPS", "CBP", "ZIP"):
                    if must not in scrubbed:
                        raise SystemExit(f"{url}: lost {must}")
            if host == "kakospreadsheet.es" and slug != "ayuda":
                if "Correos" not in scrubbed:
                    raise SystemExit(f"{url}: lost Correos")
            dest = _overlay_dest(host, slug)
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_text(scrubbed)
            built[host][slug] = dest
            print("  wrote", dest, dest.stat().st_size)
    # Deploy notes
    for host in PAGES:
        md = ROOT / "sites" / host / "overlay" / "DEPLOY-OPS-SCRUB.md"
        md.write_text(
            f"""# Deploy — Kakobuy ops scrub ({STAMP})

Tag `{TAG}`. Strip consumer-visible desk/LATAM/twin/Phase/ops notes. Keep local fingerprints + hub uplink.

```bash
python3 tools/kakobuy_ops_scrub.py \\
  --load-env /cursor/stores/self/internal/usfans-ssh.env --deploy --verify
```
"""
        )
    return built


def deploy(built: dict) -> dict:
    client = _connect()
    bak = (
        f"/www/backup/kakobuy-ops-scrub-"
        f"{datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%S')}"
    )
    _run(client, f"mkdir -p '{bak}'")
    sftp = client.open_sftp()
    published = []
    for host, pages in built.items():
        remote_root = f"/www/wwwroot/{host}"
        for slug, local in pages.items():
            if slug == "home":
                remote = f"{remote_root}/index.html"
                bpath = f"{bak}/{host}__index.html.before"
            else:
                remote = f"{remote_root}/{slug}/index.html"
                bpath = f"{bak}/{host}__{slug}.index.html.before"
            _run(client, f"mkdir -p $(dirname '{remote}') $(dirname '{bpath}')")
            _run(client, f"cp -a '{remote}' '{bpath}' 2>/dev/null || true")
            sftp.put(str(local), remote)
            published.append(remote)
            print("put", remote)
        # chown host tree pieces we touched
        targets = [f"{remote_root}/index.html"] + [
            f"{remote_root}/{slug}" for slug in pages if slug != "home"
        ]
        _run(client, "chown -R www:www " + " ".join(targets))
    sftp.close()
    client.close()
    return {"backup": bak, "stamp": STAMP, "tag": TAG, "published": published}


def verify() -> dict:
    checks = []
    for host, pages in PAGES.items():
        for slug, path in pages:
            url = f"https://{host}{path}"
            try:
                body = _fetch(url)
                code = 200
            except Exception as exc:  # noqa: BLE001
                checks.append({"url": url, "ok": False, "error": str(exc)})
                print("FAIL", url, exc)
                continue
            bad = forbidden_hits(body)
            stamped = f'data-ops-scrub="{STAMP}"' in body or f"<!-- {TAG} -->" in body
            keep_ok = True
            if host == "kakospreadsheet.es" and slug != "ayuda":
                keep_ok = "Correos" in body
            if host == "kakobuydocs.com" and slug == "shipping-to-us":
                keep_ok = "USPS" in body and "CBP" in body
            if host == "kakobuy.fi":
                keep_ok = "Posti" in body or "Tulli" in body or "posti" in body.lower()
            ok = code == 200 and not bad and keep_ok and stamped
            row = {
                "url": url,
                "http": code,
                "ok": ok,
                "forbidden_hits": bad,
                "stamped": stamped,
                "keep_ok": keep_ok,
            }
            checks.append(row)
            print(("OK" if ok else "FAIL"), url, code, bad or "")
    return {"stamp": STAMP, "checks": checks, "all_ok": all(c.get("ok") for c in checks)}


def patch_static_overlays() -> list[str]:
    """Scrub checked-in consumer overlays so future cp/deploy won't reinject ops."""
    changed: list[str] = []
    paths = [
        ROOT / "sites/kakobuydocs.com/overlay/index.html",
        ROOT / "sites/kakobuydocs.com/overlay/index.html.platform-patched",
        ROOT / "sites/kakobuydocs.com/overlay/index.html.es-us-gap",
        ROOT / "sites/kakobuydocs.com/overlay/kakobuy-spreadsheet/index.html",
        ROOT / "sites/kakobuydocs.com/overlay/kakobuy-coupons/index.html",
        ROOT / "sites/kakobuydocs.com/overlay/finds-dataset/index.html",
        ROOT / "sites/kakobuydocs.com/overlay/shipping-to-us/index.html",
        ROOT / "sites/kakobuydocs.com/overlay/llms.txt",
        ROOT / "sites/kakobuydocs.com/overlay/data/coupons-truth.json",
        ROOT / "sites/kakospreadsheet.es/overlay/index.html",
        ROOT / "sites/kakospreadsheet.es/overlay/index.html.platform-patched",
        ROOT / "sites/kakospreadsheet.es/overlay/index.html.stabilize-patched",
        ROOT / "sites/kakospreadsheet.es/overlay/index.html.es-gap",
        ROOT / "sites/kakospreadsheet.es/overlay/index.html.es-disclaimer-rm",
        ROOT / "sites/kakospreadsheet.es/overlay/ayuda/index.html",
        ROOT / "sites/kakospreadsheet.es/overlay/kakobuy-opiniones/index.html.stabilize-patched",
        ROOT / "sites/kakospreadsheet.es/overlay/kakobuy-opiniones/index.html.es-gap",
        ROOT / "sites/kakospreadsheet.es/overlay/kakobuy-opiniones/index.html.es-disclaimer-rm",
        ROOT / "sites/kakospreadsheet.es/overlay/es-kakobuy-confiable/index.html.stabilize-patched",
        ROOT / "sites/kakospreadsheet.es/overlay/es-kakobuy-confiable/index.html.es-gap",
        ROOT / "sites/kakospreadsheet.es/overlay/es-kakobuy-confiable/index.html.es-disclaimer-rm",
        ROOT / "sites/kakospreadsheet.es/overlay/envio-kakobuy-espana/index.html.stabilize-patched",
        ROOT / "sites/kakospreadsheet.es/overlay/envio-kakobuy-espana/index.html.es-gap",
        ROOT / "sites/kakospreadsheet.es/overlay/envio-kakobuy-espana/index.html.es-disclaimer-rm",
        ROOT / "sites/kakospreadsheet.es/overlay/como-comprar-en-kakobuy/index.html.es-gap",
        ROOT / "sites/kakospreadsheet.es/overlay/como-comprar-en-kakobuy/index.html.es-disclaimer-rm",
        ROOT / "sites/kakospreadsheet.es/overlay/how-to-use-kakobuy/index.html.es-gap",
        ROOT / "sites/kakospreadsheet.es/overlay/how-to-use-kakobuy/index.html.es-disclaimer-rm",
        ROOT / "sites/kakospreadsheet.ca/overlay/index.html",
        ROOT / "sites/kakospreadsheet.ca/overlay/index.html.platform-patched",
        ROOT / "sites/kakospreadsheet.ca/overlay/help/index.html",
    ]
    for p in paths:
        if not p.exists():
            continue
        raw = p.read_text(encoding="utf-8", errors="replace")
        if p.suffix == ".json":
            new = raw
            new = new.replace(
                "FI/ES/CA keep local KPI only. Twins tips/.fr/.nl stay 301→hub.",
                "Country guides: FI / ES / CA for local postal context.",
            )
            new = new.replace(
                "Brand spreadsheet queries consolidate on kakobuydocs.com /kakobuy-spreadsheet/ + Independent Index · 11,300+. FI/ES/CA keep local KPI only. Twins tips/.fr/.nl stay 301→hub.",
                "Brand spreadsheet queries consolidate on kakobuydocs.com /kakobuy-spreadsheet/ + Independent Index · 11,300+. Country guides: FI / ES / CA.",
            )
        elif p.name == "llms.txt":
            new = raw
            new = re.sub(
                r"Keep country desks \(kakobuy\.fi / kakospreadsheet\.es / kakospreadsheet\.ca\) for local postal KPI\. Twins kakobuytips\.com \+ kakospreadsheet\.fr/\.nl 301→this hub\. Do not revive sunsets\.",
                "Country guides: kakobuy.fi / kakospreadsheet.es / kakospreadsheet.ca for local postal context.",
                new,
            )
            new = new.replace("## Keep desks\n", "## Country guides\n")
            new = re.sub(
                r"(?m)^- Twins.*$",
                "- Brand spreadsheet / coupons / dataset stay on kakobuydocs.com",
                new,
            )
        else:
            host = "kakobuydocs.com"
            if "kakospreadsheet.es" in str(p):
                host = "kakospreadsheet.es"
            elif "kakospreadsheet.ca" in str(p):
                host = "kakospreadsheet.ca"
            new = scrub_html(raw, host)
        if new != raw:
            p.write_text(new)
            changed.append(str(p.relative_to(ROOT)))
            print("patched overlay", p.relative_to(ROOT))
    return changed


def patch_builders() -> list[str]:
    """Stop builders from reinjecting consumer ops notes."""
    changed: list[str] = []
    gap = ROOT / "tools" / "kakobuy_es_us_gap.py"
    if gap.exists():
        text = gap.read_text()
        orig = text
        # Expand forbidden list
        if "Desk ES ·" not in text.split("FORBIDDEN_CONSUMER_OPS", 1)[-1][:800]:
            text = text.replace(
                "FORBIDDEN_CONSUMER_OPS = (\n"
                '    "latam-note",\n'
                '    "data-latam-overflow",\n'
                '    "twin LATAM",\n'
                '    "desk LATAM",\n'
                '    "Sin twin LATAM",\n'
                '    "Sin desk LATAM",\n'
                ")",
                "FORBIDDEN_CONSUMER_OPS = (\n"
                '    "latam-note",\n'
                '    "data-latam-overflow",\n'
                '    "twin LATAM",\n'
                '    "desk LATAM",\n'
                '    "Sin twin LATAM",\n'
                '    "Sin desk LATAM",\n'
                '    "Desk ES ·",\n'
                '    "Desk CA ·",\n'
                '    "Keep desks",\n'
                '    "Do not revive",\n'
                '    "Phase A/B/C",\n'
                '    "Twins tips",\n'
                '    "hub reclaim",\n'
                '    "Not a dest-country skin",\n'
                '    "local KPI only",\n'
                '    "LATAM",\n'
                ")",
            )
        text = text.replace(
            'f"<h2>Desk ES · Correos / AEAT</h2>{HUB_UPLINK_ES}</section>"',
            'f"<h2>España · Correos / AEAT</h2>{HUB_UPLINK_ES}</section>"',
        )
        # shipping-to-us template consumer ops
        text = text.replace(
            "Keep desks remain FI/ES/CA only.",
            "Country guides: FI / ES / CA.",
        )
        text = text.replace(
            "<summary>Is this a United States keep desk?</summary>\n"
            "      <p>No. kakobuydocs.com stays the English brand hub. FI / ES / CA are the only keep desks. This URL only deepens US shipping intent on the hub.</p>",
            "<summary>Is this a United States country guide?</summary>\n"
            "      <p>No. kakobuydocs.com stays the English brand hub. Country guides are on kakobuy.fi, kakospreadsheet.es, and kakospreadsheet.ca. This URL deepens US shipping notes on the hub.</p>",
        )
        text = text.replace(
            "Not a dest-country skin. Twins tips/.fr/.nl stay 301→hub.",
            "Independent of kakobuy.com checkout.",
        )
        text = text.replace(
            "a US keep desk, or a new domain (no kakobuys.co.uk either — UK lookalikes stay vetoed).",
            "or a Google Sheet clone — spreadsheet / finds stay on /kakobuy-spreadsheet/.",
        )
        text = text.replace(
            "Hub-only US shipping notes · <strong>not</strong> a spreadsheet hero · CTA → ",
            "US shipping notes · CTA → ",
        )
        text = text.replace(
            "United States · USPS · CBP · ZIP · hub-only",
            "United States · USPS · CBP · ZIP",
        )
        text = text.replace(
            "This page is <strong>not</strong> a Kakobuy Spreadsheet hero and does <strong>not</strong> open a .us desk. Brand finds stay on the Independent Index.",
            "This page covers US shipping / customs framing. Brand finds stay on the Independent Index.",
        )
        text = text.replace(
            'No US desk domain."',
            '"',
        )
        # FAQ schema in US_PAGE
        text = text.replace(
            '{"@type":"Question","name":"Does kakobuydocs.com open a United States keep desk?","acceptedAnswer":{"@type":"Answer","text":"No. This is a hub-only shipping-to-US page with USPS / CBP / ZIP framing. There is no .us Kakobuy desk and no new domain. Brand spreadsheet intent stays on /kakobuy-spreadsheet/ and /finds-dataset/."}}',
            '{"@type":"Question","name":"Is this a United States country guide?","acceptedAnswer":{"@type":"Answer","text":"No. This is a hub shipping-to-US page with USPS / CBP / ZIP framing. Brand spreadsheet / finds stay on /kakobuy-spreadsheet/ and /finds-dataset/."}}',
        )
        if text != orig:
            gap.write_text(text)
            changed.append(str(gap.relative_to(ROOT)))
            print("patched", gap.relative_to(ROOT))

    desks = ROOT / "tools" / "kakobuy_desks.py"
    if desks.exists():
        text = desks.read_text()
        orig = text
        reps = [
            (
                "Desk ES independiente. Catálogo en esta portada. /envio-kakobuy-espana/ se conserva. Lab 1 oct 2026. No copiamos un recuento de líneas ajeno.",
                "Guía independiente para España. Catálogo en esta portada. /envio-kakobuy-espana/ se conserva. No copiamos un recuento de líneas ajeno.",
            ),
            (
                "Desk ES independiente: catálogo en inglés, almacén según Help oficial, estimador con destino España. Lab 1 oct 2026.",
                "Guía independiente para España: catálogo en inglés, almacén según Help oficial, estimador con destino España.",
            ),
            (
                "Notas con fecha de este desk ES. No copiamos un recuento de líneas ajeno. Lab 1 oct 2026.",
                "Notas con fecha para España. No copiamos un recuento de líneas ajeno.",
            ),
            (
                "Desk FR indépendant : catalogue sur cette accueil. Destination France dans l’estimateur. Pas la Belgique. Lab 1 oct. 2026.",
                "Guide indépendant FR : catalogue sur cette accueil. Destination France dans l’estimateur. Pas la Belgique.",
            ),
            (
                "Desk FR indépendant : catalogue anglais, estimateur vers la France. Lab 1 oct. 2026. Pas la Belgique.",
                "Guide indépendant FR : catalogue anglais, estimateur vers la France. Pas la Belgique.",
            ),
            (
                "Notes datées du desk FR. Destination France, pas la Belgique. Lab 1 oct. 2026.",
                "Notes datées pour la France. Destination France, pas la Belgique.",
            ),
        ]
        for a, b in reps:
            text = text.replace(a, b)
        if text != orig:
            desks.write_text(text)
            changed.append(str(desks.relative_to(ROOT)))
            print("patched", desks.relative_to(ROOT))
    return changed


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--load-env", type=Path)
    ap.add_argument("--build", action="store_true")
    ap.add_argument("--patch-overlays", action="store_true")
    ap.add_argument("--patch-builders", action="store_true")
    ap.add_argument("--deploy", action="store_true")
    ap.add_argument("--verify", action="store_true")
    ap.add_argument("--all", action="store_true")
    args = ap.parse_args()
    if args.load_env:
        _load_env(args.load_env)

    meta: dict = {"stamp": STAMP, "tag": TAG}
    do_all = args.all or not any(
        [args.build, args.patch_overlays, args.patch_builders, args.deploy, args.verify]
    )

    if do_all or args.patch_builders:
        meta["builders"] = patch_builders()
    if do_all or args.patch_overlays:
        meta["overlays_patched"] = patch_static_overlays()
    if do_all or args.build:
        built = build_all()
        meta["built"] = {
            h: {s: str(p) for s, p in pages.items()} for h, pages in built.items()
        }
    else:
        built = None
        if args.deploy:
            # load from overlay paths
            built = {}
            for host, pages in PAGES.items():
                built[host] = {}
                for slug, _ in pages:
                    p = _overlay_dest(host, slug)
                    if not p.exists():
                        raise SystemExit(f"missing built overlay {p}; run --build first")
                    built[host][slug] = p

    if (do_all or args.deploy) and built is not None:
        meta["deploy"] = deploy(built)
    if do_all or args.verify:
        # brief CF/cache settle
        import time

        time.sleep(2)
        meta["verify"] = verify()

    out_dir = STORE / "internal" / "kakobuy-ops-scrub"
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "live_verify.json").write_text(json.dumps(meta, indent=2, ensure_ascii=False))
    if meta.get("deploy"):
        (out_dir / "backup.txt").write_text(meta["deploy"].get("backup", "") + "\n")
    print(json.dumps({"all_ok": meta.get("verify", {}).get("all_ok"), "stamp": STAMP}, indent=2))
    if meta.get("verify") and not meta["verify"].get("all_ok"):
        sys.exit(1)


if __name__ == "__main__":
    main()
