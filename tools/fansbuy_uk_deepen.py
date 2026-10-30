#!/usr/bin/env python3
"""Deepen fansbuy.co.uk keep desk: Royal Mail / HMRC / GBP + kill spreadsheet hero.

LIVE only on fansbuy.co.uk. Does not touch hub (fansbuysheets.net), nl/de watch,
or revive twins / Phase C. Requires ORIGIN_SSH_PASS (or --load-env usfans-ssh.env).
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

from strip_editor_notes import strip_html

ROOT = Path(__file__).resolve().parents[1]
OVERLAY = ROOT / "sites" / "fansbuy.co.uk" / "overlay"
HOST = "fansbuy.co.uk"
REMOTE = f"/www/wwwroot/{HOST}"
STAMP = "20261028"
TODAY = "2026-10-28"
HUB = "https://fansbuysheets.net"
PAGES = (
    "fansbuy-shipping-guide",
    "fansbuy-spreadsheet",
    "fansbuy-coupons",
    "fansbuy-qc-guide",
)

STYLE = (
    f'<style id="uk-deepen-{STAMP}">.hub-uplink{{margin:14px 0 0;padding:12px 14px;'
    "border-left:3px solid #dc2626;background:#fff5f5;color:#3f1f1f;line-height:1.6;"
    "font-size:15px;max-width:760px}}.hub-uplink a{{color:#b91c1c;font-weight:600}}"
    "#local{scroll-margin-top:88px}.local-box{margin:1.25em 0;padding:14px 16px;"
    "border:1px solid #e2e8f0;border-radius:10px;background:#f8fafc}</style>"
)

HUB_UPLINK = (
    f'<p class="hub-uplink" data-uk-deepen="{STAMP}" data-step4-hub="1">'
    "Brand Spreadsheet / Coupons truth / Independent Index · 12,000+ → "
    f'<a href="{HUB}/">fansbuysheets.net</a> · '
    f'<a href="{HUB}/fansbuy-coupons/">coupons</a> · '
    f'<a href="{HUB}/finds-dataset/">dataset</a>. '
    "This URL = UK desk only (Royal Mail / HMRC / GBP / UK postcode)."
    "</p>"
)

LOCAL_SHIP = f"""
<section id="local" class="local-box" data-uk-fingerprint="royal-mail-hmrc-gbp" data-uk-deepen="{STAMP}">
<h2>UK fingerprint before you pick a line</h2>
<ol>
<li><strong>Estimator destination: United Kingdom</strong> — GB, not EU and not IE as a stand-in.</li>
<li><strong>Address</strong> — UK postcode pattern (e.g. <code>SW1A 1AA</code>); NI may need separate SKU / line checks.</li>
<li><strong>Last mile</strong> — often <strong>Royal Mail</strong> / UK parcel networks; this desk does not invent a service point.</li>
<li><strong>Duties</strong> — SKU + declaration decide. Morning source: <a href="https://www.gov.uk/government/organisations/hm-revenue-customs" rel="noopener" target="_blank">HMRC</a>. Quote freight in <strong>GBP</strong>.</li>
</ol>
<p>QC before ship: <a href="/fansbuy-qc-guide/">QC photos</a> · local coupons (truth on hub): <a href="/fansbuy-coupons/">UK coupons</a>.</p>
</section>
"""

LOCAL_SHEET = f"""
<section id="local" class="local-box" data-uk-fingerprint="uk-desk-not-second-hub" data-uk-deepen="{STAMP}">
<h2>UK desk — not a second Spreadsheet hub</h2>
<ol>
<li><strong>Brand Spreadsheet intent</strong> belongs on <a href="{HUB}/">fansbuysheets.net</a> (Independent Index · 12,000+).</li>
<li><strong>This .co.uk URL</strong> helps UK landing: Royal Mail, HMRC, GBP, UK postcode — not a competing finds hero.</li>
<li><strong>Coupons truth table</strong> → <a href="{HUB}/fansbuy-coupons/">hub coupons</a>; UK landing copy may stay local.</li>
<li><strong>Dataset / W2C rows</strong> → <a href="{HUB}/finds-dataset/">hub finds-dataset</a>.</li>
</ol>
<p>Next on this desk: <a href="/fansbuy-shipping-guide/">UK shipping</a> · <a href="/fansbuy-qc-guide/">QC before Royal Mail</a>.</p>
</section>
"""

LOCAL_COUPONS = f"""
<section id="local" class="local-box" data-uk-fingerprint="coupon-not-hmrc" data-uk-deepen="{STAMP}">
<h2>UK coupons fingerprint</h2>
<ol>
<li><strong>Coupon ≠ HMRC duties</strong> — a code does not waive Royal Mail collect fees or import VAT.</li>
<li><strong>GBP checkout</strong> — estimate freight/duty in GBP after shortlist + QC.</li>
<li><strong>Truth table</strong> — global working codes → <a href="{HUB}/fansbuy-coupons/">fansbuysheets.net/fansbuy-coupons</a>.</li>
<li><strong>Twin</strong> — <code>fansbuyspreadsheet.uk</code> stays 301→this desk; do not revive a second UK coupons URL.</li>
</ol>
<p>Ship planning: <a href="/fansbuy-shipping-guide/">UK shipping guide</a>.</p>
</section>
"""

LOCAL_QC = f"""
<section id="local" class="local-box" data-uk-fingerprint="qc-before-royal-mail" data-uk-deepen="{STAMP}">
<h2>QC fingerprint for UK parcels</h2>
<ol>
<li><strong>Approve/reject in warehouse</strong> — before the parcel meets <strong>Royal Mail</strong> / UK last mile.</li>
<li><strong>Declaration vs SKU</strong> — mismatches show up at <strong>HMRC</strong>; photos are your record.</li>
<li><strong>Address</strong> — UK postcode + phone; NI ≠ mainland assumptions.</li>
<li><strong>Brand finds / Spreadsheet</strong> → <a href="{HUB}/">fansbuysheets.net</a>, not a desk hero.</li>
</ol>
<p>Freight context: <a href="/fansbuy-shipping-guide/">UK shipping</a>.</p>
</section>
"""

THICKEN_SHIP = f"""
<h2 id="royal-mail-hmrc">Royal Mail, HMRC and GBP (updated {TODAY})</h2>
<p>Shipping to the UK means: estimator destination <strong>United Kingdom</strong>, a real <strong>UK postcode</strong>, often <strong>Royal Mail</strong> on the last mile, and duties under <strong>HMRC</strong> rules for the SKU — not a Spreadsheet hero on this URL. Quote lines and volumetric weight in <strong>GBP</strong>. Brand Spreadsheet / coupons truth / dataset stay on <a href="{HUB}/">fansbuysheets.net</a>.</p>
<p>Use the calculator below for line comparison, then re-check declaration before submit. QC first: <a href="/fansbuy-qc-guide/">QC photos before Royal Mail</a>.</p>
"""

THICKEN_SHEET = f"""
<h2 id="cede-hub">Why this page is not the brand Spreadsheet</h2>
<p>GSC showed exact <em>fansbuy spreadsheet</em> clicks landing on the UK desk while the hub sat deeper. That is cannibalization. The Independent Index · <strong>12,000+</strong>, coupons truth and finds-dataset live on <a href="{HUB}/">fansbuysheets.net</a>. This .co.uk page is a UK landing helper (Royal Mail / HMRC / GBP) with optional local browsing — not a second global Spreadsheet hero.</p>
<p>Open the hub catalogue: <a href="{HUB}/">Independent Index</a> · <a href="{HUB}/finds-dataset/">dataset</a> · <a href="{HUB}/fansbuy-coupons/">coupons</a>. Local next step: <a href="/fansbuy-shipping-guide/">UK shipping</a>.</p>
"""

THICKEN_COUPONS = f"""
<h2 id="hub-truth">Hub truth vs UK landing (updated {TODAY})</h2>
<p>Keep using this page for UK-framed coupon copy and invite flow. The verified global truth table is on <a href="{HUB}/fansbuy-coupons/">fansbuysheets.net/fansbuy-coupons</a>. A coupon never replaces <strong>HMRC</strong> duties or <strong>Royal Mail</strong> collect fees — estimate those in <strong>GBP</strong> on the <a href="/fansbuy-shipping-guide/">shipping guide</a>.</p>
"""

THICKEN_QC = f"""
<h2 id="hmrc-photos">Photos, HMRC and Royal Mail (updated {TODAY})</h2>
<p>UK buyers should settle size, colour and defect notes while stock is still in the China warehouse. Once the parcel is with <strong>Royal Mail</strong>, photo disputes get harder and <strong>HMRC</strong> collect fees are separate from merchandise refunds. Brand Spreadsheet browsing → <a href="{HUB}/">fansbuysheets.net</a>.</p>
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
    if f'id="uk-deepen-{STAMP}"' in html:
        return html
    return html.replace("</head>", STYLE + "\n</head>", 1)


def _soften_brand(html: str) -> str:
    html = html.replace("<span>Spreadsheet</span>", "<span>UK</span>", 1)
    html = html.replace("<h3>FansBuy Spreadsheet</h3>", "<h3>FansBuy UK</h3>")
    html = html.replace(
        "&copy; 2026 FansBuy Spreadsheet.",
        "&copy; 2026 FansBuy UK (co.uk desk).",
    )
    html = html.replace(
        "Independence notice.</strong> FansBuy Spreadsheet is an independent information site.",
        "Independence notice.</strong> fansbuy.co.uk is the UK desk (Royal Mail / HMRC / GBP). "
        "Brand Spreadsheet → fansbuysheets.net. FansBuy Spreadsheet copy on this host is",
    )
    return html


def deepen_shipping(html: str) -> str:
    html = _inject_head_style(html)
    html = _soften_brand(html)
    new_title = "FansBuy Shipping to UK — Royal Mail, HMRC, GBP"
    html = re.sub(r"<title>.*?</title>", f"<title>{new_title}</title>", html, count=1, flags=re.S)
    html = re.sub(
        r'property="og:title" content="[^"]*"',
        f'property="og:title" content="{new_title}"',
        html,
        count=1,
    )
    html = re.sub(
        r'name="description" content="[^"]*"',
        'name="description" content="FansBuy shipping to the UK: Royal Mail last mile, HMRC duties, GBP quotes, UK postcode. Brand Spreadsheet → fansbuysheets.net."',
        html,
        count=1,
    )
    html = html.replace(
        '<h1 class="atit">FansBuy Shipping UK<br><em>Royal Mail, costs, calculator</em></h1>\n'
        "    <p class=\"aint\">Everything about FansBuy shipping &mdash; all lines compared, delivery times by country, real costs and a free interactive calculator so you know what you&rsquo;ll pay before checkout.</p>\n"
        "  </header>",
        '<h1 class="atit">FansBuy shipping to the UK<br><em>Royal Mail · HMRC · GBP</em></h1>\n'
        '    <p class="aint">UK desk shipping: compare lines, volumetric weight and timelines for a United Kingdom delivery address — then check HMRC before you submit. Updated '
        f"{TODAY}. Brand Spreadsheet stays on fansbuysheets.net.</p>\n"
        f"    {HUB_UPLINK}\n"
        "  </header>",
        1,
    )
    if 'id="local"' not in html:
        html = html.replace(
            '<h2 class="ph" id="calculator">Free FansBuy shipping calculator</h2>',
            f"{LOCAL_SHIP}\n  <h2 class=\"ph\" id=\"calculator\">Free FansBuy shipping calculator</h2>",
            1,
        )
    if 'id="royal-mail-hmrc"' not in html:
        html = html.replace(
            '<h2 class="ph" id="lines">All FansBuy shipping lines</h2>',
            f"{THICKEN_SHIP}\n  <h2 class=\"ph\" id=\"lines\">All FansBuy shipping lines</h2>",
            1,
        )
    return html


def deepen_spreadsheet(html: str) -> str:
    html = _inject_head_style(html)
    html = _soften_brand(html)
    new_title = "FansBuy UK desk — Royal Mail / HMRC (not Spreadsheet hub)"
    html = re.sub(r"<title>.*?</title>", f"<title>{new_title}</title>", html, count=1, flags=re.S)
    html = re.sub(
        r'property="og:title" content="[^"]*"',
        f'property="og:title" content="{new_title}"',
        html,
        count=1,
    )
    html = re.sub(
        r'property="og:description" content="[^"]*"',
        'property="og:description" content="UK landing desk for FansBuy: Royal Mail, HMRC, GBP. Brand Spreadsheet / Independent Index → fansbuysheets.net."',
        html,
        count=1,
    )
    html = re.sub(
        r'name="description" content="[^"]*"',
        'name="description" content="UK landing desk for FansBuy: Royal Mail, HMRC, GBP. Brand Spreadsheet / Independent Index · 12,000+ → fansbuysheets.net."',
        html,
        count=1,
    )
    html = html.replace(
        '"name":"FansBuy Spreadsheet 2026"',
        '"name":"FansBuy UK desk — Royal Mail / HMRC"',
    )
    html = html.replace(
        "<h1>FansBuy Spreadsheet UK<br><em>W2C links and QC 2026</em></h1>\n"
        "  <p class=\"hsub\">Browse 12,000+ products &mdash; shoes, bags, clothing and accessories with direct FansBuy purchase links.</p>",
        "<h1>FansBuy UK desk<br><em>Royal Mail · HMRC · GBP — not a second Spreadsheet hub</em></h1>\n"
        "  <p class=\"hsub\">Local UK landing helper. The Independent Index · 12,000+, coupons truth and finds-dataset live on "
        f'<a href="{HUB}/">fansbuysheets.net</a>. Updated {TODAY}.</p>\n'
        f"  {HUB_UPLINK}",
        1,
    )
    # Soften editor notes H2 that still says "this spreadsheet"
    html = html.replace(
        "<h2>How UK buyers should use this spreadsheet</h2>",
        "<h2>How UK buyers should use this desk (then open the hub)</h2>",
        1,
    )
    if 'id="local"' not in html:
        html = html.replace(
            '<p style="font-size:12px;font-weight:700;color:#dc2626;text-transform:uppercase">UK editor notes</p>',
            f"{LOCAL_SHEET}\n"
            '<p style="font-size:12px;font-weight:700;color:#dc2626;text-transform:uppercase">UK editor notes</p>',
            1,
        )
    if 'id="cede-hub"' not in html:
        html = html.replace(
            "<h2>How UK buyers should use this desk (then open the hub)</h2>",
            f"{THICKEN_SHEET}\n<h2>How UK buyers should use this desk (then open the hub)</h2>",
            1,
        )
    return html


def deepen_coupons(html: str) -> str:
    html = _inject_head_style(html)
    html = _soften_brand(html)
    new_title = "FansBuy Coupons UK — GBP landing · truth on hub"
    html = re.sub(r"<title>.*?</title>", f"<title>{new_title}</title>", html, count=1, flags=re.S)
    html = re.sub(
        r'property="og:title" content="[^"]*"',
        f'property="og:title" content="{new_title}"',
        html,
        count=1,
    )
    html = re.sub(
        r'name="description" content="[^"]*"',
        'name="description" content="FansBuy UK coupon landing in GBP. Global truth table → fansbuysheets.net/fansbuy-coupons. Coupon ≠ HMRC duties."',
        html,
        count=1,
    )
    html = html.replace(
        '<h1 style="font-size:clamp(24px,4vw,36px);font-weight:600;letter-spacing:-.8px;line-height:1.18;margin-bottom:12px">FansBuy <span style="color:var(--acc)">Coupon Codes</span><br>2026 &mdash; All Working Discounts</h1>\n'
        '    <p style="font-size:16px;color:var(--g3);line-height:1.8;border-left:3px solid var(--acc);padding-left:16px">Every working FansBuy coupon code in one place. Verified weekly. Click any code to copy it instantly.</p>\n'
        "  </header>",
        '<h1 style="font-size:clamp(24px,4vw,36px);font-weight:600;letter-spacing:-.8px;line-height:1.18;margin-bottom:12px">FansBuy <span style="color:var(--acc)">UK coupons</span><br>GBP landing · truth on hub</h1>\n'
        '    <p style="font-size:16px;color:var(--g3);line-height:1.8;border-left:3px solid var(--acc);padding-left:16px">UK-framed coupon landing. Verified global truth table → '
        f'<a href="{HUB}/fansbuy-coupons/">fansbuysheets.net/fansbuy-coupons</a>. Updated {TODAY}. Coupon ≠ HMRC / Royal Mail fees.</p>\n'
        f"    {HUB_UPLINK}\n"
        "  </header>",
        1,
    )
    html = html.replace(
        '<a href="/fansbuy-spreadsheet/" class="sbcta">Browse FansBuy Spreadsheet &rarr;</a>',
        f'<a href="{HUB}/" class="sbcta">Open hub Independent Index &rarr;</a>',
        1,
    )
    if 'id="local"' not in html:
        html = html.replace(
            '<p style="font-size:12px;font-weight:700;color:#dc2626;text-transform:uppercase">UK editor notes</p><h2>Coupons checklist (UK)</h2>',
            f"{LOCAL_COUPONS}\n"
            '<p style="font-size:12px;font-weight:700;color:#dc2626;text-transform:uppercase">UK editor notes</p><h2>Coupons checklist (UK)</h2>',
            1,
        )
    if 'id="hub-truth"' not in html:
        html = html.replace(
            '<h2 class="ph">How to use an agent coupon code</h2>',
            f"{THICKEN_COUPONS}\n  <h2 class=\"ph\">How to use an agent coupon code</h2>",
            1,
        )
    return html


def deepen_qc(html: str) -> str:
    html = _inject_head_style(html)
    html = _soften_brand(html)
    new_title = "FansBuy QC UK — photos before Royal Mail &amp; HMRC"
    html = re.sub(r"<title>.*?</title>", f"<title>{new_title}</title>", html, count=1, flags=re.S)
    html = re.sub(
        r'property="og:title" content="[^"]*"',
        'property="og:title" content="FansBuy QC UK — photos before Royal Mail &amp; HMRC"',
        html,
        count=1,
    )
    html = re.sub(
        r'name="description" content="[^"]*"',
        'name="description" content="FansBuy QC for UK parcels: approve before Royal Mail. HMRC collect ≠ merchandise refund. Brand Spreadsheet → fansbuysheets.net."',
        html,
        count=1,
    )
    # Replace H1 + intro + spreadsheet CTA
    old_cta = (
        '<a href="/fansbuy-spreadsheet/" style="display:inline-block;padding:12px 24px;background:var(--acc);color:#fff;border-radius:9px;font-size:14px;font-weight:500;text-decoration:none;transition:background .15s" onmouseover="this.style.background=\'var(--acd)\'" onmouseout="this.style.background=\'var(--acc)\'">Browse FansBuy Spreadsheet &rarr;</a>'
    )
    new_cta = (
        f'<a href="{HUB}/" style="display:inline-block;padding:12px 24px;background:var(--acc);color:#fff;border-radius:9px;font-size:14px;font-weight:500;text-decoration:none;transition:background .15s" onmouseover="this.style.background=\'var(--acd)\'" onmouseout="this.style.background=\'var(--acc)\'">Open hub Independent Index &rarr;</a>'
    )
    html = html.replace(old_cta, new_cta, 1)
    html = html.replace(
        '<h1 style="font-size:clamp(24px,3.5vw,36px);font-weight:600;letter-spacing:-.7px;margin-bottom:14px">FansBuy QC Photos — pics before Royal Mail</h1>\n'
        '  <p style="font-size:16px;color:var(--g3);line-height:1.8;margin-bottom:28px">How to review FansBuy QC photos: what to check on shoes, clothing and bags — and when to approve or reject your item.<br><br>\n'
        "    This page is part of <strong>FansBuy UK</strong>.  </code>.\n"
        "  </p>",
        '<h1 style="font-size:clamp(24px,3.5vw,36px);font-weight:600;letter-spacing:-.7px;margin-bottom:14px">FansBuy QC UK — photos before Royal Mail</h1>\n'
        '  <p style="font-size:16px;color:var(--g3);line-height:1.8;margin-bottom:28px">Review QC while goods are in warehouse — before <strong>Royal Mail</strong> and before <strong>HMRC</strong> collect. Updated '
        f"{TODAY}. Brand Spreadsheet → fansbuysheets.net.</p>\n"
        f"  {HUB_UPLINK}",
        1,
    )
    if 'id="local"' not in html:
        html = html.replace(
            '<p style="font-size:12px;font-weight:700;color:#dc2626;text-transform:uppercase">UK editor notes</p><h2>QC before shipping to the UK</h2>',
            f"{LOCAL_QC}\n"
            '<p style="font-size:12px;font-weight:700;color:#dc2626;text-transform:uppercase">UK editor notes</p><h2>QC before shipping to the UK</h2>',
            1,
        )
    if 'id="hmrc-photos"' not in html:
        html = html.replace(
            "<h2>QC before shipping to the UK</h2>",
            f"{THICKEN_QC}\n<h2>QC before shipping to the UK</h2>",
            1,
        )
    return html


BUILDERS = {
    "fansbuy-shipping-guide": deepen_shipping,
    "fansbuy-spreadsheet": deepen_spreadsheet,
    "fansbuy-coupons": deepen_coupons,
    "fansbuy-qc-guide": deepen_qc,
}


def _assert_ok(slug: str, deepened: str) -> None:
    for must in (
        'id="local"',
        'class="hub-uplink"',
        "Royal Mail",
        "HMRC",
        HUB,
        f'data-uk-deepen="{STAMP}"',
    ):
        if must not in deepened:
            raise SystemExit(f"{slug}: missing {must}")
    if re.search(r"<h1[^>]*>[^<]*Spreadsheet", deepened, re.I):
        raise SystemExit(f"{slug}: H1 still Spreadsheet hero")
    title_m = re.search(r"<title>(.*?)</title>", deepened, re.S | re.I)
    if title_m and re.search(r"Spreadsheet UK|FansBuy Spreadsheet", title_m.group(1), re.I):
        # allow "not Spreadsheet hub" phrasing
        if "not Spreadsheet" not in title_m.group(1) and "not a second" not in title_m.group(1):
            if re.search(r"FansBuy Spreadsheet", title_m.group(1), re.I):
                raise SystemExit(f"{slug}: <title> still Spreadsheet hero: {title_m.group(1)}")


def build() -> dict[str, Path]:
    out: dict[str, Path] = {}
    for slug in PAGES:
        base = OVERLAY / slug / "live-base.index.html"
        if not base.exists():
            raise SystemExit(f"missing live base: {base}")
        deepened = strip_html(BUILDERS[slug](base.read_text(errors="replace")))
        _assert_ok(slug, deepened)
        dest = OVERLAY / slug / "index.html.uk-deepen"
        dest.write_text(deepened)
        out[slug] = dest
        print("BUILT", dest, "bytes", dest.stat().st_size)
    return out


def deploy(built: dict[str, Path], store_internal: Path | None) -> dict:
    client = _connect()
    bak = f"/www/backup/fansbuy-uk-deepen-{datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%S')}"
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
        sftp.get(f"{REMOTE}/sitemap.xml", str(OVERLAY / "sitemap.xml.before-uk-deepen"))
        for slug in PAGES:
            loc = f"https://{HOST}/{slug}/"
            sm = re.sub(
                rf"(<loc>{re.escape(loc)}</loc>\s*<lastmod>)[^<]+",
                rf"\g<1>{TODAY}",
                sm,
            )
        sm = re.sub(
            rf"(<loc>https://{re.escape(HOST)}/</loc>\s*<lastmod>)[^<]+",
            rf"\g<1>{TODAY}",
            sm,
        )
        # also money aliases if present
        for extra in ("is-fansbuy-legit",):
            loc = f"https://{HOST}/{extra}/"
            sm = re.sub(
                rf"(<loc>{re.escape(loc)}</loc>\s*<lastmod>)[^<]+",
                rf"\g<1>{TODAY}",
                sm,
            )
        local_sm = OVERLAY / "sitemap.xml"
        local_sm.write_text(sm)
        sftp.put(str(local_sm), f"{REMOTE}/sitemap.xml")
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
        req = Request(url, headers={"User-Agent": "fansbuy-uk-deepen/1.0"})
        with urlopen(req, timeout=60) as resp:
            body = resp.read().decode(errors="replace")
            code = resp.status
        title_m = re.search(r"<title>(.*?)</title>", body, re.S | re.I)
        row = {
            "url": url,
            "http": code,
            "id_local": 'id="local"' in body,
            "hub_uplink": HUB in body and "finds-dataset" in body and "hub-uplink" in body,
            "royal_mail": body.count("Royal Mail"),
            "hmrc": body.count("HMRC"),
            "gbp": body.count("GBP"),
            "data_uk_deepen": f'data-uk-deepen="{STAMP}"' in body,
            "spreadsheet_h1": bool(re.search(r"<h1[^>]*>[^<]*Spreadsheet", body, re.I)),
            "title": re.sub(r"\s+", " ", title_m.group(1)).strip() if title_m else None,
        }
        checks.append(row)

    # homepage + hub must remain untouched by our stamp
    for url, label in (
        (f"https://{HOST}/", "home"),
        (f"{HUB}/", "hub"),
    ):
        req = Request(url, headers={"User-Agent": "fansbuy-uk-deepen/1.0"})
        with urlopen(req, timeout=60) as resp:
            body = resp.read().decode(errors="replace")
            code = resp.status
        checks.append(
            {
                "url": url,
                "label": label,
                "http": code,
                "data_uk_deepen": f'data-uk-deepen="{STAMP}"' in body,
            }
        )

    twin_rows = []
    for t in (
        "https://fansbuyspreadsheet.uk/",
        "https://fansbuy.eu/",
        "https://fansbuyspreadsheet.eu/",
        "https://fansspreadsheet.net/",
    ):
        u = urlparse(t)
        conn = http.client.HTTPSConnection(u.netloc, timeout=20)
        conn.request("GET", u.path or "/", headers={"User-Agent": "fansbuy-uk-deepen/1.0"})
        r = conn.getresponse()
        twin_rows.append({"url": t, "http": r.status, "location": r.getheader("Location")})
        conn.close()

    # watch desks must stay 200 and without our stamp (we did not write them)
    watch_rows = []
    for t in ("https://fansbuy.nl/", "https://fansbuyspreadsheet.de/"):
        req = Request(t, headers={"User-Agent": "fansbuy-uk-deepen/1.0"})
        with urlopen(req, timeout=20) as resp:
            body = resp.read().decode(errors="replace")
            watch_rows.append(
                {
                    "url": t,
                    "http": resp.status,
                    "data_uk_deepen": f'data-uk-deepen="{STAMP}"' in body,
                }
            )

    return {
        "at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "checks": checks,
        "twins": twin_rows,
        "watch": watch_rows,
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
    ap.add_argument("--store-internal", type=Path, default=None)
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
            and "/fansbuy-" in c.get("url", "")
            and (
                not c.get("id_local")
                or not c.get("hub_uplink")
                or not c.get("data_uk_deepen")
                or c.get("spreadsheet_h1")
                or c.get("http") != 200
            )
        ]
        # home/hub must NOT carry our deepen stamp
        leaked = [
            c
            for c in ver["checks"]
            if c.get("label") in ("home", "hub") and c.get("data_uk_deepen")
        ]
        twin_bad = [
            t
            for t in ver.get("twins", [])
            if t.get("http") not in (301, 302)
        ]
        # .uk twin must land on .co.uk; .eu / fansspreadsheet → hub
        for t in ver.get("twins", []):
            loc = t.get("location") or ""
            if "fansbuyspreadsheet.uk" in t.get("url", "") and "fansbuy.co.uk" not in loc:
                twin_bad.append(t)
            if t.get("url") in (
                "https://fansbuy.eu/",
                "https://fansbuyspreadsheet.eu/",
                "https://fansspreadsheet.net/",
            ) and "fansbuysheets.net" not in loc:
                twin_bad.append(t)
        watch_bad = [w for w in ver.get("watch", []) if w.get("data_uk_deepen") or w.get("http") != 200]
        if bad or leaked or twin_bad or watch_bad:
            print("VERIFY_FAIL", bad, leaked, twin_bad, watch_bad)
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
