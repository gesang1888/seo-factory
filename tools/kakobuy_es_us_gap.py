#!/usr/bin/env python3
"""Kakobuy gap R1+R2 LIVE: deepen ES keep + hub US shipping block.

- ES (kakospreadsheet.es): Correos/AEAT/CP5 deepen on thin money pages + hub uplink.
  Consumer pages must NOT show LATAM/ops/twin callouts (ops stay in docs/internal).
- Hub (kakobuydocs.com): /shipping-to-us/ USPS·CBP·ZIP + homepage US block;
  CTA uplink to spreadsheet/dataset (NOT a competing spreadsheet hero).
- No new domains. No kakobuys.co.uk. Twins stay 301→hub.

Requires ORIGIN_SSH_PASS (or --load-env internal/usfans-ssh.env).
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
ES_OVERLAY = ROOT / "sites" / "kakospreadsheet.es" / "overlay"
HUB_OVERLAY = ROOT / "sites" / "kakobuydocs.com" / "overlay"
STAMP = "20261029"
TAG = f"kakobuy-es-us-gap-{STAMP}"
HUB = "https://kakobuydocs.com"
ES_HOST = "kakospreadsheet.es"
HUB_HOST = "kakobuydocs.com"
ES_REMOTE = f"/www/wwwroot/{ES_HOST}"
HUB_REMOTE = f"/www/wwwroot/{HUB_HOST}"

ES_STYLE = (
    f'<style id="es-gap-{STAMP}">'
    ".hub-uplink{margin:14px 0 0;padding:12px 14px;"
    "border-left:3px solid #0f766e;background:#f0fdfa;color:#134e4a;line-height:1.6;"
    "font-size:15px;max-width:760px}.hub-uplink a{color:#0f766e;font-weight:600}"
    "#local{scroll-margin-top:88px}.local-box{margin:1.25em 0;padding:14px 16px;"
    "border:1px solid #ccfbf1;border-radius:12px;background:#f0fdfa;color:#134e4a}"
    "</style>"
)

# Ops/LATAM overflow policy lives in docs/internal only — never inject on consumer HTML.
FORBIDDEN_CONSUMER_OPS = (
    "latam-note",
    "data-latam-overflow",
    "twin LATAM",
    "desk LATAM",
    "Sin twin LATAM",
    "Sin desk LATAM",
    "Desk ES ·",
    "Desk CA ·",
    "Keep desks",
    "Do not revive",
    "Phase A/B/C",
    "Twins tips",
    "hub reclaim",
    "Not a dest-country skin",
    "local KPI only",
    "LATAM",
)

HUB_UPLINK_ES = (
    f'<p class="hub-uplink" data-es-gap="{STAMP}">'
    "Brand spreadsheet / Independent Index → "
    f'<a href="{HUB}/">{HUB_HOST}</a> · '
    f'<a href="{HUB}/kakobuy-coupons/">coupons</a> · '
    f'<a href="{HUB}/finds-dataset/">dataset</a>. '
    "Este host no es un segundo hub."
    "</p>"
)

LOCAL_COMO = f"""
<section id="local" class="local-box" data-es-fingerprint="correos-aeat-cp5" data-es-gap="{STAMP}">
<h2>Huella ES · Correos / AEAT</h2>
<ol>
<li><strong>Destino del estimador: España</strong> — Spain / España, no «EU» ni este TLD.</li>
<li><strong>Dirección</strong> — calle española + <strong>código postal de cinco dígitos</strong>.</li>
<li><strong>Última milla</strong> — a menudo <strong>Correos</strong> (posible tasa Collect).</li>
<li><strong>Aranceles / IVA</strong> — lo dice la SKU. Fuente: <a href="https://sede.agenciatributaria.gob.es/" rel="noopener" target="_blank">AEAT</a>. Sin valor declarado inventado.</li>
</ol>
{HUB_UPLINK_ES}
<p>Detalle envío: <a href="/envio-kakobuy-espana/">/envio-kakobuy-espana</a> · Opiniones: <a href="/kakobuy-opiniones/">¿es fiable?</a>.</p>
</section>
"""

LOCAL_HOWTO = f"""
<section id="local" class="local-box" data-es-fingerprint="primer-pedido-correos-aeat" data-es-gap="{STAMP}">
<h2>Primer pedido: España, Correos, AEAT</h2>
<ol>
<li><strong>Estimador</strong> — destino <strong>España</strong> (Spain), no EU genérico.</li>
<li><strong>Dirección</strong> — calle española + CP de cinco dígitos.</li>
<li><strong>QC → consolidar → línea</strong> — fotos en almacén antes del flete; última milla a menudo <strong>Correos</strong>.</li>
<li><strong>Aduanas</strong> — declara según SKU; lee <a href="https://sede.agenciatributaria.gob.es/" rel="noopener" target="_blank">AEAT</a> el día del envío.</li>
</ol>
{HUB_UPLINK_ES}
<p>Envío: <a href="/envio-kakobuy-espana/">Correos / IVA / AEAT</a> · Cómo comprar: <a href="/como-comprar-en-kakobuy/">pasos</a>.</p>
</section>
"""

THICKEN_COMO = f"""
<h2 id="correos-aeat-gap">Correos, AEAT y código postal (España)</h2>
<p data-es-gap="{STAMP}">Comprar desde España en esta guía significa: estimador en <strong>España</strong>, dirección con <strong>CP de cinco dígitos</strong>, última milla a menudo <strong>Correos</strong>, y aranceles/IVA según la SKU y la <strong>AEAT</strong> — no un héroe «Kakobuy Spreadsheet». El índice global vive en <a href="{HUB}/kakobuy-spreadsheet/">{HUB_HOST}/kakobuy-spreadsheet</a>.</p>
"""

THICKEN_HOWTO = f"""
<h2 id="correos-aeat-primer">Dirección ES, Correos y AEAT en el primer haul</h2>
<p data-es-gap="{STAMP}">El primer pedido desde España no necesita un héroe Spreadsheet: pega el enlace, paga en la app oficial, espera QC, consolida y elige línea con destino <strong>España</strong>. Tracking doméstico suele pasar por <strong>Correos</strong>; reglas de entrada las marca la <strong>AEAT</strong>.</p>
"""

US_BLOCK_HOME = f"""
<section class="sec" id="us-intent" data-hub-us="{STAMP}" data-tag="{TAG}">
  <h2 class="stit">United States · USPS / CBP</h2>
  <p class="pp">US shipping / customs framing on this hub. Brand finds stay on the Independent Index — this block does not replace the spreadsheet.</p>
  <div class="local-box" style="margin:16px 0 0;max-width:820px">
    <ol>
      <li><strong>Estimator destination: United States</strong> — pick US, not “North America”, not a Canadian postal code.</li>
      <li><strong>Address</strong> — US street + <strong>ZIP</strong>. This hub does not file CBP entries.</li>
      <li><strong>Duties</strong> — SKU says tax-free / prepaid / collect. <strong>USPS</strong> or FedEx can add a collect fee. Source: <a href="https://www.cbp.gov/" rel="noopener">CBP</a> the morning you ship — no invented de-minimis dollar.</li>
      <li><strong>Last mile</strong> — often <strong>USPS</strong> or a commercial integrator after export.</li>
    </ol>
    <p class="money" style="margin-top:12px">Deep page: <a href="/shipping-to-us/">/shipping-to-us/</a> · Brand spreadsheet / dataset CTA: <a href="/kakobuy-spreadsheet/">/kakobuy-spreadsheet/</a> · <a href="/finds-dataset/">/finds-dataset/</a> · <a href="/kakobuy-coupons/">/kakobuy-coupons/</a></p>
  </div>
</section>
"""

SHIPPING_TO_US_HTML = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<!-- {TAG} -->
<title>Kakobuy shipping to the US — USPS, CBP, ZIP notes</title>
<meta name="description" content="Hub-only Kakobuy shipping-to-US notes: USPS last-mile, CBP / customs context, US ZIP. Not a spreadsheet hero. CTA to Independent Index · dataset · coupons on kakobuydocs.com. ">
<meta property="og:title" content="Kakobuy shipping to the US — USPS, CBP, ZIP">
<meta property="og:description" content="USPS / CBP / ZIP framing on the Kakobuy docs hub. Spreadsheet intent stays on /kakobuy-spreadsheet/.">
<meta property="og:url" content="https://kakobuydocs.com/shipping-to-us/">
<link rel="canonical" href="https://kakobuydocs.com/shipping-to-us/">
<link rel="icon" type="image/png" href="/assets/images/official-favicon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<script type="application/ld+json">
{{"@context":"https://schema.org","@graph":[
  {{"@type":"WebPage","name":"Kakobuy shipping to the US — USPS, CBP, ZIP notes","url":"https://kakobuydocs.com/shipping-to-us/","dateModified":"2026-10-29","isPartOf":{{"@type":"WebSite","url":"https://kakobuydocs.com/"}},"description":"Hub-only US shipping / customs notes. Brand spreadsheet stays on /kakobuy-spreadsheet/."}},
  {{"@type":"BreadcrumbList","itemListElement":[
    {{"@type":"ListItem","position":1,"name":"Home","item":"https://kakobuydocs.com/"}},
    {{"@type":"ListItem","position":2,"name":"Shipping to US","item":"https://kakobuydocs.com/shipping-to-us/"}}
  ]}},
  {{"@type":"FAQPage","mainEntity":[
    {{"@type":"Question","name":"Is this a United States country guide?","acceptedAnswer":{{"@type":"Answer","text":"No. This is a hub shipping-to-US page with USPS / CBP / ZIP framing. Brand spreadsheet / finds stay on /kakobuy-spreadsheet/ and /finds-dataset/."}}}},
    {{"@type":"Question","name":"How should I read a Kakobuy quote for USPS?","acceptedAnswer":{{"@type":"Answer","text":"Create the agent account with a US address and ZIP. Pick United States in the official estimator. USD line names (USPS vs integrator) appear after the warehouse accepts the parcel — this HTML is not a live quote."}}}},
    {{"@type":"Question","name":"Does this page invent a de-minimis dollar?","acceptedAnswer":{{"@type":"Answer","text":"No. Duties follow the booked SKU (tax-free / prepaid / collect). USPS or FedEx can add a collect fee. Source CBP the morning you ship."}}}}
  ]}}
]}}
</script>
<style>
:root{{--acc:#FF5C00;--acd:#e05000;--acl:#fff4ed;--bk:#111;--g2:#2d2d2d;--g3:#555;--g4:#888;--g5:#e5e5e5;--g6:#f6f6f6;--wh:#fff;--f:'IBM Plex Sans',system-ui,sans-serif}}
*,*::before,*::after{{box-sizing:border-box;margin:0;padding:0}}
body{{font-family:var(--f);background:#fff;color:#111;font-size:15px;line-height:1.7}}
a{{color:var(--acc);text-decoration:none}}a:hover{{text-decoration:underline;text-underline-offset:3px}}
.nav{{position:sticky;top:0;z-index:100;background:#fff;border-bottom:1px solid var(--g5);padding:0 24px;height:60px;display:flex;align-items:center;justify-content:space-between;gap:16px}}
.nbrand{{display:flex;align-items:center;gap:14px}}
.nlo img{{height:36px;width:auto;max-width:190px;object-fit:contain;background:#111;padding:6px 10px;border-radius:8px}}
.nl{{display:flex;gap:4px;list-style:none}}
.nl a{{font-size:13px;padding:6px 10px;border-radius:6px;color:var(--g4)}}
.nl a.on{{color:#111;font-weight:600}}
.ann{{background:var(--acc);color:#fff;text-align:center;padding:9px 16px;font-size:13px;font-weight:500}}
.ann a{{color:#fff;text-decoration:underline}}
.wrap{{max-width:820px;margin:0 auto;padding:40px 24px 64px}}
.hbg{{display:inline-flex;background:var(--acl);color:var(--acd);font-size:12px;font-weight:600;padding:5px 14px;border-radius:20px;margin-bottom:18px}}
h1{{font-size:clamp(26px,4vw,40px);font-weight:800;letter-spacing:-1.2px;line-height:1.15;margin-bottom:14px}}
.lead{{font-size:17px;color:var(--g3);margin-bottom:22px;line-height:1.75}}
.ctas{{display:flex;gap:12px;flex-wrap:wrap;margin:22px 0 28px}}
.cp{{padding:12px 22px;background:var(--acc);color:#fff;border-radius:10px;font-weight:600}}
.cs{{padding:11px 18px;border:1.5px solid var(--g5);color:#111;border-radius:10px;font-weight:500}}
.box{{border:1px solid var(--g5);border-radius:14px;padding:18px 20px;background:var(--g6);margin:18px 0}}
.box h2{{font-size:18px;margin-bottom:8px}}
.box ol{{margin:8px 0 0 18px}}.box li{{margin:8px 0;color:var(--g2)}}
h2{{font-size:22px;font-weight:700;margin:28px 0 10px}}
p{{margin:0 0 14px;color:var(--g2)}}
.faq details{{border:1px solid var(--g5);border-radius:12px;padding:12px 14px;margin:10px 0}}
.faq summary{{font-weight:600;cursor:pointer}}
.ft{{background:#1a1a1a;color:#aaa;padding:28px 24px;font-size:13px}}
.ft a{{color:#ddd}}
@media(max-width:720px){{.nl{{display:none}}}}
</style>
</head>
<body data-hub-us="{STAMP}" data-tag="{TAG}">
<div class="ann">US shipping notes · CTA → <a href="/kakobuy-spreadsheet/">Independent Index</a> · <a href="/finds-dataset/">dataset</a></div>
<nav class="nav">
  <div class="nbrand"><a class="nlo" href="/"><img src="/assets/images/official-logo.png" width="180" height="36" alt="Kakobuy"></a></div>
  <ul class="nl">
    <li><a href="/">Docs</a></li>
    <li><a href="/kakobuy-spreadsheet/">Spreadsheet</a></li>
    <li><a href="/finds-dataset/">Dataset</a></li>
    <li><a href="/kakobuy-coupons/">Coupons</a></li>
    <li><a class="on" href="/shipping-to-us/">US shipping</a></li>
  </ul>
</nav>
<main class="wrap">
  <div class="hbg">United States · USPS · CBP · ZIP</div>
  <h1>Kakobuy shipping to the US</h1>
  <p class="lead">USPS / customs framing for buyers who land on the English hub from USA impressions. This page covers US shipping / customs framing. Brand finds stay on the Independent Index.</p>
  <div class="ctas">
    <a class="cp" href="/kakobuy-spreadsheet/">Open spreadsheet / Index</a>
    <a class="cs" href="/finds-dataset/">Dataset · 11,300+</a>
    <a class="cs" href="/kakobuy-coupons/">Coupons</a>
    <a class="cs" href="/kakobuy-shipping-guide/">Full shipping guide</a>
  </div>

  <section class="box" id="local" data-us-fingerprint="usps-cbp-zip">
    <h2>US fingerprint before you book a line</h2>
    <ol>
      <li><strong>Estimator destination: United States</strong> — pick US in the official app, not this hostname and not a Canadian postal code.</li>
      <li><strong>Address</strong> — US street + <strong>ZIP</strong>. This hub does not file CBP entries.</li>
      <li><strong>Duties</strong> — the booked SKU says tax-free / prepaid / collect. <strong>USPS</strong> or FedEx can add a collect fee the estimator hides. Source: <a href="https://www.cbp.gov/" rel="noopener">CBP</a> the morning you ship. No invented de-minimis dollar on this HTML.</li>
      <li><strong>Last mile</strong> — often <strong>USPS</strong> or a commercial integrator after export handoff.</li>
    </ol>
  </section>

  <h2>What this page is / is not</h2>
  <p><strong>Is:</strong> hub-only conversion surface for USA brand/workflow impressions that currently show with near-zero CTR. Named USPS · CBP · ZIP so the SERP snippet is not a generic DHL table.</p>
  <p><strong>Is not:</strong> a second Independent Index, a Google Sheet clone, or a Google Sheet clone — spreadsheet / finds stay on /kakobuy-spreadsheet/.</p>

  <h2>Uplink to hub money URLs</h2>
  <p>When the query is <em>kakobuy spreadsheet</em> / finds / coupons, use:</p>
  <p><a href="/kakobuy-spreadsheet/">/kakobuy-spreadsheet/</a> · <a href="/finds-dataset/">/finds-dataset/</a> · <a href="/kakobuy-coupons/">/kakobuy-coupons/</a> · <a href="/">hub home</a>. Country guides: FI / ES / CA.</p>

  <section class="faq" id="faq">
    <h2>FAQ</h2>
    <details open>
      <summary>Is this a United States country guide?</summary>
      <p>No. kakobuydocs.com stays the English brand hub. Country guides are on kakobuy.fi, kakospreadsheet.es, and kakospreadsheet.ca. This URL deepens US shipping notes on the hub.</p>
    </details>
    <details>
      <summary>Where does the spreadsheet live?</summary>
      <p>On this same hub: <a href="/kakobuy-spreadsheet/">Independent Index</a> and <a href="/finds-dataset/">public dataset</a>. This shipping page deliberately does not reuse a spreadsheet H1.</p>
    </details>
    <details>
      <summary>USPS vs DHL wording?</summary>
      <p>Ranked <a href="/kakobuy-shipping-guide/">/kakobuy-shipping-guide/</a> already compares lines (incl. USA/DHL). This page adds the missing USPS / CBP / ZIP fingerprint for US SERP snippets.</p>
    </details>
  </section>
</main>
<footer class="ft">
  <p>kakobuydocs.com — hub-only /shipping-to-us/ · tag {TAG}. Not Excel. Independent of kakobuy.com checkout.</p>
  <p><a href="/">Home</a> · <a href="/kakobuy-spreadsheet/">Spreadsheet</a> · <a href="/finds-dataset/">Dataset</a> · <a href="/kakobuy-shipping-guide/">Shipping guide</a></p>
</footer>
</body>
</html>
"""


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
    req = Request(url, headers={"User-Agent": "kakobuy-es-us-gap/1.0"})
    with urlopen(req, timeout=45) as resp:
        return resp.read().decode("utf-8", errors="replace")


def _inject_head_style(html: str) -> str:
    if f'id="es-gap-{STAMP}"' in html:
        return html
    return html.replace("</head>", ES_STYLE + "\n</head>", 1)


def _set_title_desc(html: str, title: str, desc: str) -> str:
    html = re.sub(r"<title>.*?</title>", f"<title>{title}</title>", html, count=1, flags=re.S)
    if 'name="description"' in html:
        html = re.sub(
            r'<meta name="description" content="[^"]*"',
            f'<meta name="description" content="{desc}"',
            html,
            count=1,
        )
    else:
        html = html.replace(
            "</title>",
            f'</title>\n<meta name="description" content="{desc}">',
            1,
        )
    return html


def _ensure_marker_comment(html: str) -> str:
    needle = f"<!-- {TAG} -->"
    if needle in html or f"es_gap={TAG}" in html:
        return html
    return html.replace("<head>", f"<head>\n<!-- {TAG} -->", 1)


def _strip_consumer_ops(html: str) -> str:
    """Defense: never leave LATAM/ops callouts on consumer HTML."""
    html = re.sub(
        r'<p\b[^>]*\b(?:class="[^"]*latam-note[^"]*"|data-latam-overflow=)[^>]*>.*?</p>\s*',
        "",
        html,
        flags=re.S | re.I,
    )
    html = re.sub(r"\.latam-note\{[^}]*\}", "", html)
    for frag in (
        " Sin twin LATAM.",
        " Sin desk LATAM.",
        " Sin twin LATAM",
        " Sin desk LATAM",
    ):
        html = html.replace(frag, "")
    return html


def _ensure_es_gap_local(html: str) -> str:
    """Stamp existing #local + ensure hub uplink. Never inject LATAM/ops copy."""
    html = _strip_consumer_ops(html)

    def repl(m: re.Match[str]) -> str:
        block = m.group(0)
        if "data-es-gap=" not in block:
            block = block.replace("<section", f'<section data-es-gap="{STAMP}"', 1)
        if "hub-uplink" not in block and HUB_HOST not in block:
            block = block.replace("</section>", HUB_UPLINK_ES + "\n</section>", 1)
        return block

    new, n = re.subn(
        r'<section[^>]*\bid="local"[^>]*>.*?</section>',
        repl,
        html,
        count=1,
        flags=re.S,
    )
    if n == 0:
        insert = (
            f'<section id="local" class="local-box" data-es-gap="{STAMP}">'
            f"<h2>España · Correos / AEAT</h2>{HUB_UPLINK_ES}</section>"
        )
        if "</main>" in html:
            new = html.replace("</main>", insert + "\n</main>", 1)
        else:
            new = html + insert
    return _ensure_marker_comment(new)


def build_es_como(live: str) -> str:
    html = live
    html = _set_title_desc(
        html,
        "Cómo comprar en Kakobuy desde España — Correos, AEAT, CP",
        "Pasos Kakobuy España: cuenta, QC, consolidar, envío. Correos / AEAT / CP cinco dígitos. Hub spreadsheet en kakobuydocs.com.",
    )
    html = _inject_head_style(html)
    html = _ensure_marker_comment(html)
    if 'id="local"' not in html:
        html = html.replace(
            '<div class="container article-layout"><article class="article">',
            '<div class="container article-layout"><article class="article">\n' + LOCAL_COMO,
            1,
        )
    else:
        html = _ensure_es_gap_local(html)
    if 'id="correos-aeat-gap"' not in html:
        html = html.replace(
            '<h2 id="errores">Errores frecuentes</h2>',
            THICKEN_COMO + '\n<h2 id="errores">Errores frecuentes</h2>',
            1,
        )
    return _strip_consumer_ops(html)


def build_es_howto(live: str) -> str:
    html = live
    html = _set_title_desc(
        html,
        "Primer pedido Kakobuy España — Correos, AEAT, dirección",
        "Guía primer haul Kakobuy desde España: Correos, AEAT, CP cinco dígitos. Brand spreadsheet → kakobuydocs.com.",
    )
    html = _inject_head_style(html)
    html = _ensure_marker_comment(html)
    # Drop Spreadsheet brand chip → España
    html = html.replace("<span>Spreadsheet</span>", "<span>España</span>", 1)
    html = html.replace("<h3>Kakobuy Spreadsheet</h3>", "<h3>Kakobuy España</h3>", 1)
    if 'id="local"' not in html:
        html = html.replace(
            '<article class="pw">',
            '<article class="pw">\n' + LOCAL_HOWTO,
            1,
        )
    else:
        html = _ensure_es_gap_local(html)
    if 'id="correos-aeat-primer"' not in html:
        html = html.replace(
            "<h2>Primer haul: plano primero</h2>",
            THICKEN_HOWTO + "\n<h2>Primer haul: plano primero</h2>",
            1,
        )
    return _strip_consumer_ops(html)


def build_es_local_pages(live: str) -> str:
    """Home / opiniones / confiable / envio: stamp #local + hub uplink; no LATAM/ops UI."""
    html = _ensure_marker_comment(live)
    html = _ensure_es_gap_local(html)
    return _strip_consumer_ops(html)


def build_hub_home(live: str) -> str:
    html = live
    html = _ensure_marker_comment(html)
    # bump platform comment
    html = html.replace(
        "<!-- platform_opt=kakobuy-hub-reclaim-20261027 -->",
        f"<!-- platform_opt=kakobuy-hub-reclaim-20261027 · {TAG} -->",
        1,
    )
    if 'id="us-intent"' not in html:
        # insert US block after hero section (after Hub ownership local-box closes / </section> of hero)
        anchor = '</section>\n<section class="sec" id="official-promo">'
        if anchor in html:
            html = html.replace(anchor, "</section>\n" + US_BLOCK_HOME + '\n<section class="sec" id="official-promo">', 1)
        else:
            html = html.replace(
                '<section class="sec" id="official-promo">',
                US_BLOCK_HOME + '\n<section class="sec" id="official-promo">',
                1,
            )
    # Add shipping-to-us in Already ranking guides if missing
    if "/shipping-to-us/" not in html.split("Already ranking", 1)[-1][:1200]:
        card = (
            '<a href="/shipping-to-us/" class="gc"><span class="gtg">US shipping</span>'
            "<p class=\"gtit\">Shipping to the US · USPS / CBP</p>"
            '<p class="gdesc">USPS · CBP · ZIP shipping notes.</p></a>'
        )
        html = html.replace(
            '<a href="/how-to-use-kakobuy/" class="gc">',
            card + '<a href="/how-to-use-kakobuy/" class="gc">',
            1,
        )
    # footer keep link
    if "/shipping-to-us/" not in html[html.find("Hub money") : html.find("Hub money") + 400]:
        html = html.replace(
            '<a href="/kakobuy-spreadsheet/">Spreadsheet</a><br>',
            '<a href="/kakobuy-spreadsheet/">Spreadsheet</a><br><a href="/shipping-to-us/">US shipping</a><br>',
            1,
        )
    # FAQ add US question in JSON-LD if absent
    if "shipping-to-us" not in html.split("FAQPage", 1)[-1][:1500]:
        faq_q = (
            '{"@type":"Question","name":"Where does United States shipping intent live?",'
            '"acceptedAnswer":{"@type":"Answer","text":"USA shipping / USPS / CBP notes live on '
            "kakobuydocs.com/shipping-to-us/. Brand spreadsheet stays on "
            '/kakobuy-spreadsheet/. Country guides remain on .fi / .es / .ca."}}'
        )
        html = html.replace(
            '{"@type":"Question","name":"Where do brand spreadsheet queries belong?"',
            faq_q + ',{"@type":"Question","name":"Where do brand spreadsheet queries belong?"',
            1,
        )
    return html


def patch_sitemap(xml: str, loc: str, lastmod: str = "2026-10-29") -> str:
    if loc in xml:
        # bump lastmod for that url if present
        pattern = rf"(<loc>{re.escape(loc)}</loc>\s*<lastmod>)[^<]+"
        return re.sub(pattern, rf"\g<1>{lastmod}", xml, count=1)
    entry = (
        f"  <url>\n    <loc>{loc}</loc>\n"
        f"    <lastmod>{lastmod}</lastmod>\n"
        f"    <changefreq>weekly</changefreq>\n"
        f"    <priority>0.8</priority>\n  </url>\n"
    )
    if "</urlset>" in xml:
        return xml.replace("</urlset>", entry + "</urlset>")
    return xml + "\n" + entry


def build_all() -> dict[str, Path]:
    out: dict[str, Path] = {}

    # --- ES ---
    es_pages = {
        "como-comprar-en-kakobuy": (
            f"https://{ES_HOST}/como-comprar-en-kakobuy/",
            build_es_como,
            ES_OVERLAY / "como-comprar-en-kakobuy" / f"index.html.es-gap",
        ),
        "how-to-use-kakobuy": (
            f"https://{ES_HOST}/how-to-use-kakobuy/",
            build_es_howto,
            ES_OVERLAY / "how-to-use-kakobuy" / f"index.html.es-gap",
        ),
        "home": (
            f"https://{ES_HOST}/",
            build_es_local_pages,
            ES_OVERLAY / "index.html.es-gap",
        ),
        "opiniones": (
            f"https://{ES_HOST}/kakobuy-opiniones/",
            build_es_local_pages,
            ES_OVERLAY / "kakobuy-opiniones" / "index.html.es-gap",
        ),
        "confiable": (
            f"https://{ES_HOST}/es-kakobuy-confiable/",
            build_es_local_pages,
            ES_OVERLAY / "es-kakobuy-confiable" / "index.html.es-gap",
        ),
        "envio": (
            f"https://{ES_HOST}/envio-kakobuy-espana/",
            build_es_local_pages,
            ES_OVERLAY / "envio-kakobuy-espana" / "index.html.es-gap",
        ),
    }
    for key, (url, builder, dest) in es_pages.items():
        print(f"build ES {key} …")
        live = _fetch(url)
        # save live-base
        lb = dest.with_name("live-base.index.html")
        lb.parent.mkdir(parents=True, exist_ok=True)
        lb.write_text(live)
        built = builder(live)
        dest.write_text(built)
        out[f"es:{key}"] = dest
        assert f'data-es-gap="{STAMP}"' in built or TAG in built
        if key in ("como-comprar-en-kakobuy", "how-to-use-kakobuy"):
            assert "Correos" in built and "AEAT" in built
            assert HUB_HOST in built
        assert "Correos" in built
        assert HUB_HOST in built
        for bad in FORBIDDEN_CONSUMER_OPS:
            assert bad.lower() not in built.lower(), f"{key} still has ops needle {bad!r}"

    es_sm = _fetch(f"https://{ES_HOST}/sitemap.xml")
    for loc in (
        f"https://{ES_HOST}/",
        f"https://{ES_HOST}/como-comprar-en-kakobuy/",
        f"https://{ES_HOST}/how-to-use-kakobuy/",
        f"https://{ES_HOST}/kakobuy-opiniones/",
        f"https://{ES_HOST}/es-kakobuy-confiable/",
        f"https://{ES_HOST}/envio-kakobuy-espana/",
    ):
        es_sm = patch_sitemap(es_sm, loc)
    es_sm_path = ES_OVERLAY / "sitemap.xml.es-gap"
    es_sm_path.write_text(es_sm)
    out["es:sitemap"] = es_sm_path

    # --- HUB ---
    print("build hub shipping-to-us …")
    us_path = HUB_OVERLAY / "shipping-to-us" / "index.html"
    us_path.parent.mkdir(parents=True, exist_ok=True)
    us_path.write_text(SHIPPING_TO_US_HTML)
    out["hub:shipping-to-us"] = us_path
    assert "USPS" in SHIPPING_TO_US_HTML and "CBP" in SHIPPING_TO_US_HTML
    assert "kakobuy-spreadsheet" in SHIPPING_TO_US_HTML
    # must NOT be spreadsheet hero
    assert "Independent Index" not in re.search(r"<h1>(.*?)</h1>", SHIPPING_TO_US_HTML, re.S).group(1)

    print("build hub home …")
    hub_live = _fetch(f"https://{HUB_HOST}/")
    lb_hub = HUB_OVERLAY / "live-base" / "index.html.gap-before"
    lb_hub.parent.mkdir(parents=True, exist_ok=True)
    lb_hub.write_text(hub_live)
    hub_built = build_hub_home(hub_live)
    hub_home_path = HUB_OVERLAY / "index.html.es-us-gap"
    hub_home_path.write_text(hub_built)
    out["hub:home"] = hub_home_path
    assert 'id="us-intent"' in hub_built
    assert "/shipping-to-us/" in hub_built
    assert "USPS" in hub_built and "CBP" in hub_built

    hub_sm = _fetch(f"https://{HUB_HOST}/sitemap.xml")
    hub_sm = patch_sitemap(hub_sm, f"https://{HUB_HOST}/")
    hub_sm = patch_sitemap(hub_sm, f"https://{HUB_HOST}/shipping-to-us/")
    hub_sm_path = HUB_OVERLAY / "sitemap.xml.es-us-gap"
    hub_sm_path.write_text(hub_sm)
    out["hub:sitemap"] = hub_sm_path

    # llms stub line
    llms_path = HUB_OVERLAY / "llms.txt"
    if llms_path.exists():
        llms = llms_path.read_text()
        if "/shipping-to-us/" not in llms:
            llms = llms.rstrip() + (
                f"\n\n## United States (hub-only, {STAMP})\n"
                f"- /shipping-to-us/ — USPS / CBP / ZIP notes; CTA → spreadsheet + dataset\n"
                f"- No US country guide domain; no kakobuys.co.uk\n"
            )
            llms_path.write_text(llms)
        out["hub:llms"] = llms_path

    deploy_md = HUB_OVERLAY / "DEPLOY-ES-US-GAP.md"
    deploy_md.write_text(
        f"""# Deploy — Kakobuy ES deepen + hub US block ({STAMP})

Gap plan R1+R2. Tag `{TAG}`.

## Guards

- No new domains. No `kakobuys.co.uk`. Sunset twins stay 301→hub (ops/docs only).
- ES keep stays Correos/AEAT/CP5 + hub uplink; **no** consumer LATAM/ops/twin callouts (ops → docs/internal).
- Hub `/shipping-to-us/` is **not** a spreadsheet hero; CTA → `/kakobuy-spreadsheet/` + `/finds-dataset/`.

## Roots

- `{ES_REMOTE}`
- `{HUB_REMOTE}`

## Publish (surgical)

```bash
python3 tools/kakobuy_es_us_gap.py --load-env /cursor/stores/self/internal/usfans-ssh.env --deploy --verify
```

Or manual cp of `*.es-gap` / `shipping-to-us/index.html` / `index.html.es-us-gap` / sitemaps.
"""
    )
    out["deploy_md"] = deploy_md
    (ES_OVERLAY / "DEPLOY-ES-US-GAP.md").write_text(deploy_md.read_text())

    print("built", len(out), "artifacts")
    return out


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


def deploy(built: dict[str, Path]) -> dict:
    client = _connect()
    bak = f"/www/backup/kakobuy-es-us-gap-{STAMP}-{datetime.now(timezone.utc).strftime('%H%M%S')}"
    _run(client, f"mkdir -p {bak}/es {bak}/hub/shipping-to-us")
    meta = {"backup": bak, "stamp": STAMP, "tag": TAG}

    # backup + publish ES
    es_map = [
        (built["es:home"], f"{ES_REMOTE}/index.html", f"{bak}/es/index.html.before"),
        (
            built["es:como-comprar-en-kakobuy"],
            f"{ES_REMOTE}/como-comprar-en-kakobuy/index.html",
            f"{bak}/es/como-comprar.index.html.before",
        ),
        (
            built["es:how-to-use-kakobuy"],
            f"{ES_REMOTE}/how-to-use-kakobuy/index.html",
            f"{bak}/es/how-to-use.index.html.before",
        ),
        (
            built["es:opiniones"],
            f"{ES_REMOTE}/kakobuy-opiniones/index.html",
            f"{bak}/es/opiniones.index.html.before",
        ),
        (
            built["es:confiable"],
            f"{ES_REMOTE}/es-kakobuy-confiable/index.html",
            f"{bak}/es/confiable.index.html.before",
        ),
        (
            built["es:envio"],
            f"{ES_REMOTE}/envio-kakobuy-espana/index.html",
            f"{bak}/es/envio.index.html.before",
        ),
        (built["es:sitemap"], f"{ES_REMOTE}/sitemap.xml", f"{bak}/es/sitemap.xml.before"),
    ]
    sftp = client.open_sftp()
    for local, remote, bpath in es_map:
        _run(client, f"mkdir -p $(dirname {remote}) $(dirname {bpath})")
        _run(client, f"cp -a {remote} {bpath} 2>/dev/null || true")
        sftp.put(str(local), remote)
        print("put", remote)
    _run(
        client,
        f"chown -R www:www {ES_REMOTE}/index.html "
        f"{ES_REMOTE}/como-comprar-en-kakobuy {ES_REMOTE}/how-to-use-kakobuy "
        f"{ES_REMOTE}/kakobuy-opiniones {ES_REMOTE}/es-kakobuy-confiable "
        f"{ES_REMOTE}/envio-kakobuy-espana {ES_REMOTE}/sitemap.xml",
    )

    # hub
    hub_map = [
        (built["hub:home"], f"{HUB_REMOTE}/index.html", f"{bak}/hub/index.html.before"),
        (
            built["hub:shipping-to-us"],
            f"{HUB_REMOTE}/shipping-to-us/index.html",
            f"{bak}/hub/shipping-to-us/index.html.before",
        ),
        (built["hub:sitemap"], f"{HUB_REMOTE}/sitemap.xml", f"{bak}/hub/sitemap.xml.before"),
    ]
    if "hub:llms" in built:
        hub_map.append(
            (built["hub:llms"], f"{HUB_REMOTE}/llms.txt", f"{bak}/hub/llms.txt.before")
        )
    for local, remote, bpath in hub_map:
        _run(client, f"mkdir -p $(dirname {remote}) $(dirname {bpath})")
        _run(client, f"cp -a {remote} {bpath} 2>/dev/null || true")
        sftp.put(str(local), remote)
        print("put", remote)
    _run(
        client,
        f"chown -R www:www {HUB_REMOTE}/index.html {HUB_REMOTE}/shipping-to-us "
        f"{HUB_REMOTE}/sitemap.xml {HUB_REMOTE}/llms.txt",
    )
    sftp.close()
    meta["published"] = [r for _, r, _ in es_map + hub_map]
    client.close()
    return meta


def verify() -> dict:
    checks = []

    def grab(url: str) -> tuple[int, str]:
        req = Request(url, headers={"User-Agent": "kakobuy-es-us-gap-verify/1.0"})
        try:
            with urlopen(req, timeout=45) as resp:
                return resp.status, resp.read().decode("utf-8", errors="replace")
        except Exception as exc:  # noqa: BLE001
            return 0, str(exc)

    cases = [
        (f"https://{ES_HOST}/", ("Correos", "AEAT", HUB_HOST, STAMP)),
        (
            f"https://{ES_HOST}/como-comprar-en-kakobuy/",
            ("Correos", "AEAT", HUB_HOST, "data-es-gap"),
        ),
        (
            f"https://{ES_HOST}/how-to-use-kakobuy/",
            ("Correos", "AEAT", HUB_HOST, "data-es-gap"),
        ),
        (f"https://{ES_HOST}/kakobuy-opiniones/", ("Correos", HUB_HOST)),
        (f"https://{ES_HOST}/envio-kakobuy-espana/", ("Correos", "AEAT", HUB_HOST)),
        (
            f"https://{HUB_HOST}/shipping-to-us/",
            ("USPS", "CBP", "ZIP", "/kakobuy-spreadsheet/", TAG),
        ),
        (f"https://{HUB_HOST}/", ("us-intent", "USPS", "/shipping-to-us/")),
        (f"https://{HUB_HOST}/sitemap.xml", ("shipping-to-us",)),
    ]
    for url, needles in cases:
        code, body = grab(url)
        missing = [n for n in needles if n not in body]
        # spreadsheet hero forbidden on shipping-to-us H1
        forbid_ok = True
        if "shipping-to-us" in url and code == 200:
            h1 = re.search(r"<h1[^>]*>(.*?)</h1>", body, re.S)
            if h1 and re.search(r"spreadsheet|Independent Index", h1.group(1), re.I):
                forbid_ok = False
                missing.append("H1_MUST_NOT_BE_SPREADSHEET")
        # ES consumer pages must not reintroduce LATAM/ops callouts
        ops_hits = []
        if ES_HOST in url and code == 200:
            for bad in FORBIDDEN_CONSUMER_OPS:
                if bad.lower() in body.lower():
                    ops_hits.append(bad)
                    forbid_ok = False
        ok = code == 200 and not missing and forbid_ok
        checks.append(
            {
                "url": url,
                "http": code,
                "ok": ok,
                "missing": missing,
                "ops_hits": ops_hits,
            }
        )
        print(("OK" if ok else "FAIL"), url, code, missing or "", ops_hits or "")

    # twins still 301
    for twin in ("kakobuytips.com", "kakospreadsheet.fr", "kakospreadsheet.nl"):
        req = Request(f"https://{twin}/", headers={"User-Agent": "kakobuy-es-us-gap-verify/1.0"}, method="HEAD")
        try:
            with urlopen(req, timeout=30) as resp:
                # urllib follows redirects; check final
                final = resp.geturl()
                ok = HUB_HOST in final
                checks.append({"url": f"https://{twin}/", "http": resp.status, "ok": ok, "final": final})
                print(("OK" if ok else "FAIL"), twin, "→", final)
        except Exception as exc:  # noqa: BLE001
            # HEAD may fail on some; try GET with no redirect via curl-like check
            checks.append({"url": f"https://{twin}/", "ok": False, "error": str(exc)})
            print("FAIL", twin, exc)

    return {"stamp": STAMP, "checks": checks, "all_ok": all(c.get("ok") for c in checks)}


def gsc_submit() -> dict:
    """Best-effort sitemap submit via SA if googleapiclient available."""
    sa = Path("/cursor/stores/bc-eb8405c7-0d3c-48be-958d-5f25b92c606c/internal/gsc-sa.json")
    if not sa.exists():
        return {"skipped": True, "reason": "no gsc-sa.json"}
    try:
        from google.oauth2 import service_account
        from googleapiclient.discovery import build
    except ImportError:
        import subprocess

        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "google-auth", "google-api-python-client", "-q"]
        )
        from google.oauth2 import service_account
        from googleapiclient.discovery import build

    creds = service_account.Credentials.from_service_account_file(
        str(sa), scopes=["https://www.googleapis.com/auth/webmasters"]
    )
    svc = build("searchconsole", "v1", credentials=creds, cache_discovery=False)
    results = {}
    for site, sm in (
        (f"sc-domain:{ES_HOST}", f"https://{ES_HOST}/sitemap.xml"),
        (f"sc-domain:{HUB_HOST}", f"https://{HUB_HOST}/sitemap.xml"),
        (f"https://{HUB_HOST}/", f"https://{HUB_HOST}/sitemap.xml"),
    ):
        try:
            svc.sitemaps().submit(siteUrl=site, feedpath=sm).execute()
            results[site] = {"ok": True, "sitemap": sm}
            print("GSC submit ok", site)
        except Exception as exc:  # noqa: BLE001
            results[site] = {"ok": False, "error": str(exc)[:300]}
            print("GSC submit fail", site, str(exc)[:200])
    return results


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--load-env", type=Path)
    ap.add_argument("--build-only", action="store_true")
    ap.add_argument("--deploy", action="store_true")
    ap.add_argument("--verify", action="store_true")
    ap.add_argument("--gsc", action="store_true")
    args = ap.parse_args()
    if args.load_env:
        _load_env(args.load_env)

    built = build_all()
    meta = {"built": {k: str(v) for k, v in built.items()}}
    if args.deploy:
        meta["deploy"] = deploy(built)
        time.sleep(2)
    if args.verify or args.deploy:
        meta["verify"] = verify()
    if args.gsc:
        meta["gsc"] = gsc_submit()

    out_dir = Path("/cursor/stores/bc-eb8405c7-0d3c-48be-958d-5f25b92c606c/internal/kakobuy-es-us-gap")
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "live_verify.json").write_text(json.dumps(meta, indent=2)[:200000])
    if meta.get("deploy"):
        (out_dir / "backup.txt").write_text(meta["deploy"].get("backup", "") + "\n")
    print(json.dumps({"all_ok": meta.get("verify", {}).get("all_ok"), "backup": meta.get("deploy", {}).get("backup")}, indent=2))


if __name__ == "__main__":
    main()
