#!/usr/bin/env python3
"""Deepen usfansspreadsheet.co.uk keep desk (action 3): HMRC / refund / ship-to-UK
+ #local fingerprint + hub uplink.

LIVE only on usfansspreadsheet.co.uk. Does NOT revive twin .uk (keep 301→.co.uk).
Does NOT touch hub (.net) or NL. No new PL/ES/IT/DE desks.
Requires ORIGIN_SSH_PASS (or internal/usfans-ssh.env via --load-env).
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
OVERLAY = ROOT / "sites" / "usfansspreadsheet.co.uk" / "overlay"
HOST = "usfansspreadsheet.co.uk"
REMOTE = f"/www/wwwroot/{HOST}"
STAMP = "20261027"
HUB = "https://usfansspreadsheet.net"
TWIN = "usfansspreadsheet.uk"
PAGES = (
    "usfans-shipping-guide",
    "usfans-refund-guide",
    "usfans-coupons",
    "usfans-freight",
)

STYLE = (
    f'<style id="uk-deepen-{STAMP}">.hub-uplink{{margin:14px 0 18px;padding:12px 14px;'
    "border-left:3px solid #FF5C00;background:#fff7f2;color:#3f2a1f;line-height:1.6;"
    "font-size:15px;max-width:920px}}.hub-uplink a{{color:#c2410c;font-weight:600}}"
    "#local{scroll-margin-top:88px}.local-box{margin:1.25em auto;padding:16px 18px;"
    "border:1px solid #d0dae6;border-radius:12px;background:#f8fafc;max-width:920px;"
    "color:#1e293b;line-height:1.7}.local-box ol{margin:0.6em 0 0.4em 1.2em}"
    ".local-box li{margin:0.35em 0}.uk-thicken{max-width:920px;margin:20px auto;"
    "padding:16px 18px;border:1px solid #e2e8f0;border-radius:12px;background:#fff;"
    "color:#1e293b;line-height:1.7}</style>"
)

HUB_UPLINK = (
    f'<p class="hub-uplink" data-uk-deepen="{STAMP}" data-step4-hub="1">'
    "Brand / Spreadsheet / Coupons truth → "
    f'<a href="{HUB}/">usfansspreadsheet.net</a> · '
    f'<a href="{HUB}/usfans-coupons/">coupons</a> · '
    f'<a href="{HUB}/usfans-spreadsheet/">spreadsheet</a> '
    "(Independent Index · 10,601). This URL = UK local "
    "(HMRC / Royal Mail / UK postcode / NI). Twin "
    f"<code>{TWIN}</code> stays 301 → <code>.co.uk</code> — not revived."
    "</p>"
)

LOCAL_SHIP = f"""
<section id="local" class="local-box" data-uk-fingerprint="hmrc-royal-mail-ni" data-uk-deepen="{STAMP}">
<h2>UK fingerprint before you book a line</h2>
<ol>
<li><strong>Estimator destination: United Kingdom (GB)</strong> — not this TLD, not EU, not IE.</li>
<li><strong>Address</strong> — UK postcode. <strong>Northern Ireland</strong> is often another carrier product; do not assume the same Royal Mail SKU as mainland GB.</li>
<li><strong>Last mile</strong> — often <strong>Royal Mail</strong> (or the live SKU handoff). Quiet gaps between export and first UK scan are common on economy air.</li>
<li><strong>Duties / VAT</strong> — the booked SKU decides prepaid vs collect. Source the morning you ship: <a href="https://www.gov.uk/goods-sent-from-abroad" rel="noopener" target="_blank">HMRC goods sent from abroad</a>. No declared-value coaching on this desk.</li>
</ol>
<p>Also: <a href="/usfans-refund-guide/">UK refunds</a> · <a href="/usfans-freight/">freight / customs notes</a> · hub spreadsheet on <a href="{HUB}/">.net</a>.</p>
</section>
"""

LOCAL_REFUND = f"""
<section id="local" class="local-box" data-uk-fingerprint="refund-hmrc-royal-mail" data-uk-deepen="{STAMP}">
<h2>UK fingerprint for refunds &amp; disputes</h2>
<ol>
<li><strong>Warehouse first</strong> — QC reject / wrong item / damaged in warehouse is faster than a post-delivery return after <strong>HMRC</strong> / carrier collect.</li>
<li><strong>Lost after export</strong> — keep the international tracking string and any <strong>Royal Mail</strong> last-mile scan; open the in-app ticket with parcel ID, not this hostname.</li>
<li><strong>Collect fees</strong> — Royal Mail / broker collect is not an automatic USFans refund; duties follow the SKU and HMRC rules that day.</li>
<li><strong>NI vs GB</strong> — if the line or address was Northern Ireland, treat it as a different product when arguing delivery failure.</li>
</ol>
<p>Shipping timing: <a href="/usfans-shipping-guide/">UK shipping guide</a>. Brand spreadsheet → <a href="{HUB}/">usfansspreadsheet.net</a>.</p>
</section>
"""

LOCAL_COUPONS = f"""
<section id="local" class="local-box" data-uk-fingerprint="coupons-uk-desk-hub" data-uk-deepen="{STAMP}">
<h2>UK desk coupons vs hub truth</h2>
<ol>
<li><strong>This host</strong> — <code>.co.uk</code> keeps local coupon copy for UK buyers (GBP desk). Twin <code>{TWIN}</code> already <strong>301 → here</strong>; we do not revive it.</li>
<li><strong>Hub truth</strong> — global spreadsheet / coupon verification lives on <a href="{HUB}/usfans-coupons/">usfansspreadsheet.net/usfans-coupons/</a>.</li>
<li><strong>Fees ≠ duties</strong> — a coupon cuts agent fees; it does not erase <strong>HMRC</strong> VAT/duty or Royal Mail collect.</li>
<li><strong>Ship after QC</strong> — re-check codes the morning you register, then plan <a href="/usfans-shipping-guide/">UK shipping</a>.</li>
</ol>
</section>
"""

LOCAL_FREIGHT = f"""
<section id="local" class="local-box" data-uk-fingerprint="freight-hmrc-royal-mail" data-uk-deepen="{STAMP}">
<h2>UK fingerprint for freight &amp; customs</h2>
<ol>
<li><strong>Destination GB</strong> — estimator country United Kingdom; UK postcode on the label.</li>
<li><strong>Northern Ireland</strong> — often another SKU; do not reuse a mainland GB Royal Mail assumption.</li>
<li><strong>HMRC</strong> — who pays import charges is on the booked line; read <a href="https://www.gov.uk/goods-sent-from-abroad" rel="noopener" target="_blank">gov.uk goods-sent-from-abroad</a> the morning you submit.</li>
<li><strong>Last mile</strong> — often Royal Mail after the international handoff.</li>
</ol>
<p>Rates &amp; times: <a href="/usfans-shipping-guide/">shipping guide</a>. Brand spreadsheet → <a href="{HUB}/">.net hub</a>.</p>
</section>
"""

THICKEN_SHIP = f"""
<section class="uk-thicken" id="ship-to-uk" data-uk-deepen="{STAMP}">
<h2>Does USFans ship to the UK — and how long?</h2>
<p>Yes: pick destination <strong>United Kingdom (GB)</strong> in the official estimator after QC. Shoppers asking <em>does usfans ship to uk</em> or <em>how long does usfans take to ship to uk</em> need line choice + last-mile reality — not a second spreadsheet hub.</p>
<ul>
<li><strong>Typical air window</strong> — express lines often land faster; economy air adds quiet days before the first <strong>Royal Mail</strong> (or live SKU) scan. Re-read the calculator table the morning you pay freight.</li>
<li><strong>HMRC buffer</strong> — budget import VAT/duty separately from the freight quote. Prepaid vs collect is on the SKU; this desk never invents a threshold.</li>
<li><strong>Northern Ireland</strong> — confirm the live product; NI is frequently not the same Royal Mail mainland SKU.</li>
<li><strong>Tracking gaps</strong> — export → customs → UK scan can stall; wait for a carrier event before a missing-parcel ticket unless the SLA in-app says otherwise.</li>
</ul>
<p>Refunds after a failed delivery: <a href="/usfans-refund-guide/">refund guide</a>. Brand finds index: <a href="{HUB}/usfans-spreadsheet/">hub spreadsheet</a>.</p>
</section>
"""

THICKEN_REFUND = f"""
<section class="uk-thicken" id="uk-refund-hmrc" data-uk-deepen="{STAMP}">
<h2>UK refunds after HMRC / Royal Mail</h2>
<p>Fastest wins stay in the warehouse: reject on QC, exchange size, or cancel before international submit. After the parcel leaves China:</p>
<ul>
<li><strong>Lost in transit</strong> — attach the international number plus any Royal Mail last-mile event; USFans tickets need the parcel ID from the app.</li>
<li><strong>Collect / duties surprise</strong> — HMRC or carrier collect fees are not the same as an agent merchandise refund. Coupons do not erase import charges.</li>
<li><strong>Wrong address / NI mismatch</strong> — if GB vs Northern Ireland was wrong in the address book, treat re-ship as a new estimate, not a silent retry of the same SKU.</li>
</ul>
<p>Plan the outbound line on the <a href="/usfans-shipping-guide/">UK shipping guide</a> before you need this page.</p>
</section>
"""

THICKEN_COUPONS = f"""
<section class="uk-thicken" id="uk-coupon-sink" data-uk-deepen="{STAMP}">
<h2>Twin .uk coupon URLs sink here</h2>
<p>Old <code>{TWIN}</code> coupon paths <strong>301 to this .co.uk page</strong>. Keep using <a href="/usfans-coupons/">usfansspreadsheet.co.uk/usfans-coupons/</a> for the UK desk copy; verify global codes on <a href="{HUB}/usfans-coupons/">the .net hub</a>. Do not stand the twin back up.</p>
</section>
"""

THICKEN_FREIGHT = f"""
<section class="uk-thicken" id="hmrc-volume" data-uk-deepen="{STAMP}">
<h2>HMRC, volume weight, Royal Mail</h2>
<p>Freight to the UK is max(actual, volumetric) on most air SKUs, then last-mile often via <strong>Royal Mail</strong>. Duties follow <strong>HMRC</strong> and the booked line — this HTML is not a filing desk and not a spreadsheet hero. Re-run the official estimator with destination <strong>GB</strong> the morning you pay.</p>
</section>
"""


def _load_env(path: Path) -> None:
    text = path.read_text()
    host = pass_val = None
    for line in text.splitlines():
        if line.startswith("HOST="):
            host = line.split("=", 1)[1].strip().strip('"').strip("'")
        if line.startswith("RAW_LINE="):
            # Entire RAW_LINE value including leading semicolon (len 16).
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


def _soften_footer(html: str) -> str:
    html = html.replace("<h3>USFans Spreadsheet</h3>", "<h3>USFans UK desk</h3>", 1)
    html = html.replace(
        "&copy; 2026 USFans Spreadsheet.",
        "&copy; 2026 USFans UK desk (usfansspreadsheet.co.uk).",
        1,
    )
    return html


def _hub_sidebar_cta(html: str) -> str:
    html = html.replace(
        '<a href="/usfans-spreadsheet/" class="sbcta">Browse USFans Spreadsheet &rarr;</a>',
        f'<a href="{HUB}/usfans-spreadsheet/" class="sbcta" data-uk-deepen="{STAMP}">Hub spreadsheet &rarr;</a>',
        1,
    )
    # refund-style primary CTA
    html = re.sub(
        r'(<a href="/usfans-spreadsheet/"[^>]*>)Browse USFans Spreadsheet &rarr;(</a>)',
        rf'<a href="{HUB}/usfans-spreadsheet/" data-uk-deepen="{STAMP}">Open hub spreadsheet &rarr;</a>',
        html,
        count=1,
    )
    return html


def _inject_before_editor(html: str, blocks: str) -> str:
    marker = '<section id="gsc-editor-notes"'
    if marker not in html:
        return html
    if f'data-uk-deepen="{STAMP}"' in html and 'id="local"' in html:
        return html
    return html.replace(marker, blocks + "\n" + marker, 1)


def deepen_shipping(html: str) -> str:
    html = _inject_head_style(html)
    html = _soften_footer(html)
    html = _hub_sidebar_cta(html)
    title = "USFans Shipping to UK — Royal Mail, HMRC, Times (2026)"
    html = re.sub(r"<title>.*?</title>", f"<title>{title}</title>", html, count=1, flags=re.S)
    html = re.sub(
        r'<meta name="description" content="[^"]*"',
        '<meta name="description" content="Does USFans ship to the UK? Lines, delivery times, Royal Mail last-mile, HMRC notes, Northern Ireland vs GB. Not a second spreadsheet hub."',
        html,
        count=1,
    )
    html = re.sub(
        r'(<h1 class="atit">).*?(</h1>)',
        r"\1USFans shipping to the UK<br><em>Royal Mail · HMRC · times 2026</em>\2",
        html,
        count=1,
        flags=re.S,
    )
    html = re.sub(
        r'<p class="aint">.*?</p>',
        (
            '<p class="aint">Ship to the United Kingdom after QC: compare lines, delivery windows, '
            "and real costs. Last-mile is often <strong>Royal Mail</strong>; duties follow "
            "<strong>HMRC</strong>. Northern Ireland is often another SKU. Brand spreadsheet stays on "
            f'<a href="{HUB}/">usfansspreadsheet.net</a>.</p>\n'
            f"  {HUB_UPLINK}"
        ),
        html,
        count=1,
        flags=re.S,
    )
    if 'id="local"' not in html:
        html = html.replace(
            '<h2 class="ph" id="calculator">Free USFans shipping calculator</h2>',
            LOCAL_SHIP + '\n  <h2 class="ph" id="calculator">Free USFans shipping calculator</h2>',
            1,
        )
    if 'id="ship-to-uk"' not in html:
        html = html.replace(
            '<h2 class="ph">Delivery times by country</h2>',
            THICKEN_SHIP + '\n  <h2 class="ph">Delivery times by country</h2>',
            1,
        )
    # editor notes: cede brand sheet + twin narrative
    html = html.replace(
        "<h2>UK editor notes — Usfans Shipping Guide</h2>",
        "<h2>UK editor notes — shipping to UK (HMRC / Royal Mail)</h2>",
        1,
    )
    html = re.sub(
        r"(<section id=\"gsc-editor-notes\"[^>]*>.*?<p>)This guide on https://usfansspreadsheet\.co\.uk/ is written for United Kingdom USFans buyers who use W2C spreadsheets,",
        rf"\1UK shipping desk on https://usfansspreadsheet.co.uk/ for GB postcodes, Royal Mail last-mile and HMRC context. Brand W2C spreadsheet → {HUB}. Twin {TWIN} stays 301→.co.uk. Written for United Kingdom buyers who still use warehouse QC photos,",
        html,
        count=1,
        flags=re.S,
    )
    return html


def deepen_refund(html: str) -> str:
    html = _inject_head_style(html)
    html = _soften_footer(html)
    html = _hub_sidebar_cta(html)
    title = "USFans UK Refund Guide — HMRC, Royal Mail, Disputes (2026)"
    html = re.sub(r"<title>.*?</title>", f"<title>{title}</title>", html, count=1, flags=re.S)
    html = re.sub(
        r'<meta name="description" content="[^"]*"',
        '<meta name="description" content="How to refund on USFans for UK buyers: QC rejects, lost parcels, Royal Mail last-mile, HMRC collect vs agent refund. Hub spreadsheet on .net."',
        html,
        count=1,
    )
    html = re.sub(
        r"(<h1[^>]*>).*?(</h1>)",
        r"\1How to refund on USFans (UK) — HMRC, Royal Mail, disputes 2026\2",
        html,
        count=1,
        flags=re.S,
    )
    # intro paragraph after h1
    html = re.sub(
        r'(<p style="font-size:16px;color:var\(--g3\);line-height:1\.8;margin-bottom:28px">).*?(</p>)',
        (
            r"\1Step-by-step UK refunds on USFans: QC rejections, wrong items, lost parcels and disputes. "
            "Prefer warehouse fixes before international submit. After export, keep Royal Mail / "
            "carrier scans; HMRC collect is not an automatic merchandise refund."
            f"<br><br>Local desk on <strong>usfansspreadsheet.co.uk</strong> — brand spreadsheet → "
            f'<a href="{HUB}/">usfansspreadsheet.net</a>.\2\n'
            f"  {HUB_UPLINK}"
        ),
        html,
        count=1,
        flags=re.S,
    )
    html = _inject_before_editor(html, LOCAL_REFUND + "\n" + THICKEN_REFUND)
    html = html.replace(
        "<h2>UK editor notes — Usfans Refund Guide</h2>",
        "<h2>UK editor notes — refunds (HMRC / Royal Mail)</h2>",
        1,
    )
    return html


def deepen_coupons(html: str) -> str:
    html = _inject_head_style(html)
    html = _soften_footer(html)
    html = _hub_sidebar_cta(html)
    title = "USFans UK Coupon Codes 2026 — Desk + Hub Truth"
    html = re.sub(r"<title>.*?</title>", f"<title>{title}</title>", html, count=1, flags=re.S)
    html = re.sub(
        r'<meta name="description" content="[^"]*"',
        f'<meta name="description" content="USFans coupon codes on the UK .co.uk desk. Twin {TWIN} 301s here. Verify global codes on usfansspreadsheet.net. Coupons cut fees — not HMRC duties."',
        html,
        count=1,
    )
    # lead under h1
    html = re.sub(
        r'(<p style="font-size:16px;color:var\(--g3\);line-height:1\.8;border-left:3px solid var\(--acc\);padding-left:16px">).*?(</p>)',
        (
            r"\1Working USFans coupon codes for UK buyers on this .co.uk desk. "
            f"Twin <code>{TWIN}</code> coupon URLs 301 here — not revived. "
            f'Global verification → <a href="{HUB}/usfans-coupons/">hub coupons</a>. '
            "Coupons cut agent fees; they do not erase HMRC VAT/duty.\2\n"
            f"    {HUB_UPLINK}"
        ),
        html,
        count=1,
        flags=re.S,
    )
    html = _inject_before_editor(html, LOCAL_COUPONS + "\n" + THICKEN_COUPONS)
    html = html.replace(
        "<h2>UK editor notes — Usfans Coupons</h2>",
        "<h2>UK editor notes — coupons (desk sinks twin .uk)</h2>",
        1,
    )
    return html


def deepen_freight(html: str) -> str:
    html = _inject_head_style(html)
    html = _soften_footer(html)
    title = "USFans UK Freight — HMRC, Royal Mail, Volume Weight"
    html = re.sub(r"<title>.*?</title>", f"<title>{title}</title>", html, count=1, flags=re.S)
    html = re.sub(
        r'<meta name="description" content="[^"]*"',
        '<meta name="description" content="USFans freight to the United Kingdom: estimator destination GB, volume weight, HMRC notes, Royal Mail last-mile, Northern Ireland caveats. Not a spreadsheet hub."',
        html,
        count=1,
    )
    # JSON-LD name if spreadsheet hero
    html = html.replace(
        "USFans Spreadsheet in English: shipping and customs from the United Kingdom",
        title,
    )
    html = re.sub(
        r'<span class="eyebrow"[^>]*>.*?</span>',
        '<span class="eyebrow" style="color:var(--acd)">UK freight · HMRC / Royal Mail</span>',
        html,
        count=1,
        flags=re.S,
    )
    if f'data-uk-deepen="{STAMP}"' not in html:
        html = html.replace(
            '<p class="lead">Pick destination United Kingdom — 英国 in the public estimator — no login. The delivery address uses a UK postcode. Northern Ireland is often another carrier product.</p>',
            (
                '<p class="lead">Pick destination <strong>United Kingdom (GB)</strong> in the public estimator — no login. '
                "UK postcode on the label. <strong>Northern Ireland</strong> is often another carrier product. "
                "Last-mile often <strong>Royal Mail</strong>; duties follow <strong>HMRC</strong>.</p>\n"
                f"  {HUB_UPLINK}\n"
                f"  {LOCAL_FREIGHT}"
            ),
            1,
        )
    if 'id="hmrc-volume"' not in html:
        html = html.replace(
            "<h2>The official estimator decides</h2>",
            THICKEN_FREIGHT + "\n  <h2>The official estimator decides</h2>",
            1,
        )
    return html


BUILDERS = {
    "usfans-shipping-guide": deepen_shipping,
    "usfans-refund-guide": deepen_refund,
    "usfans-coupons": deepen_coupons,
    "usfans-freight": deepen_freight,
}


def _sanity(slug: str, html: str) -> None:
    must = [
        'id="local"',
        'class="hub-uplink"',
        "HMRC",
        "Royal Mail",
        f'data-uk-deepen="{STAMP}"',
        "usfansspreadsheet.net",
    ]
    for token in must:
        if token not in html:
            raise SystemExit(f"{slug}: missing {token}")
    if slug == "usfans-shipping-guide":
        for token in ("ship to the UK", "Northern Ireland", "how long"):
            if token.lower() not in html.lower():
                raise SystemExit(f"{slug}: missing SERP token {token}")
    if slug == "usfans-coupons" and TWIN not in html:
        raise SystemExit(f"{slug}: missing twin 301 narrative")
    if re.search(r"<h1[^>]*>[^<]*Spreadsheet", html, re.I):
        raise SystemExit(f"{slug}: H1 still Spreadsheet hero")
    title_m = re.search(r"<title>(.*?)</title>", html, re.S | re.I)
    if title_m and re.search(r"Spreadsheet", title_m.group(1), re.I) and slug == "usfans-freight":
        raise SystemExit(f"{slug}: <title> still Spreadsheet hero")
    if title_m and re.search(r"Spreadsheet in English", title_m.group(1), re.I):
        raise SystemExit(f"{slug}: <title> still Spreadsheet-in-English hero")


def build() -> dict[str, Path]:
    out: dict[str, Path] = {}
    for slug in PAGES:
        base = OVERLAY / slug / "live-base.index.html"
        if not base.exists():
            raise SystemExit(f"missing live base: {base}")
        deepened = strip_html(BUILDERS[slug](base.read_text(errors="replace")))
        _sanity(slug, deepened)
        dest = OVERLAY / slug / "index.html.uk-deepen"
        dest.write_text(deepened)
        out[slug] = dest
        print("BUILT", dest, "bytes", dest.stat().st_size)
    return out


def pull_live_bases() -> None:
    client = _connect()
    sftp = client.open_sftp()
    for slug in PAGES:
        d = OVERLAY / slug
        d.mkdir(parents=True, exist_ok=True)
        remote = f"{REMOTE}/{slug}/index.html"
        local = d / "live-base.index.html"
        sftp.get(remote, str(local))
        print("PULLED", remote, "->", local)
    sftp.close()
    client.close()


def deploy(built: dict[str, Path], store_internal: Path | None) -> dict:
    client = _connect()
    bak = f"/www/backup/usfans-uk-deepen-{datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%S')}"
    cmds = [f"mkdir -p '{bak}'"]
    for slug in PAGES:
        cmds.append(
            f"cp -a '{REMOTE}/{slug}/index.html' '{bak}/{slug}-index.html.before' 2>/dev/null || true"
        )
    # never touch twin wwwroot
    cmds.append(f"test ! -e /www/wwwroot/{TWIN}/index.html || echo TWIN_WWWROOT_PRESENT")
    print(_run(client, " && ".join(cmds)))

    sftp = client.open_sftp()
    for slug, path in built.items():
        remote = f"{REMOTE}/{slug}/index.html"
        sftp.put(str(path), remote)
        print("PUT", remote)

    today = "2026-10-27"
    try:
        with sftp.open(f"{REMOTE}/sitemap.xml", "r") as fh:
            sm = fh.read().decode(errors="replace")
        for slug in PAGES:
            loc = f"https://{HOST}/{slug}/"
            sm = re.sub(
                rf"(<loc>{re.escape(loc)}</loc>\s*<lastmod>)[^<]+",
                rf"\g<1>{today}",
                sm,
            )
            sm = re.sub(
                rf"(<url>\s*<loc>{re.escape(loc)}</loc>\s*)(?:<lastmod>[^<]*</lastmod>\s*)?",
                rf"\1<lastmod>{today}</lastmod>\n",
                sm,
            )
        sm = re.sub(
            rf"(<loc>https://{re.escape(HOST)}/</loc>\s*<lastmod>)[^<]+",
            rf"\g<1>{today}",
            sm,
        )
        tmp = f"/tmp/usfans-uk-sitemap-{STAMP}.xml"
        Path(tmp).write_text(sm)
        sftp.put(tmp, f"{REMOTE}/sitemap.xml")
        print("PUT sitemap.xml lastmod", today)
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
    # assert twin still redirects at nginx layer (do not write twin files)
    twin_check = _run(
        client,
        f"grep -R \"{TWIN}\" /www/server/panel/vhost/nginx/ 2>/dev/null | head -5; "
        f"ls /www/wwwroot/{TWIN} 2>&1 | head -3",
    )
    print("TWIN_DISK", twin_check[:500])
    print("BACKUP", bak)
    meta = {"backup": bak, "stamp": STAMP, "pages": list(PAGES), "twin_untouched": True}
    if store_internal:
        store_internal.mkdir(parents=True, exist_ok=True)
        (store_internal / "backup.txt").write_text(bak + "\n")
    client.close()
    return meta


def _http_nofollow(url: str) -> dict:
    u = urlparse(url)
    conn = http.client.HTTPSConnection(u.netloc, timeout=25)
    conn.request("GET", u.path or "/", headers={"User-Agent": "usfans-uk-deepen/1.0"})
    r = conn.getresponse()
    row = {"url": url, "http": r.status, "location": r.getheader("Location")}
    conn.close()
    return row


def verify() -> dict:
    checks = []
    for slug in PAGES:
        url = f"https://{HOST}/{slug}/"
        req = Request(url, headers={"User-Agent": "usfans-uk-deepen/1.0"})
        with urlopen(req, timeout=30) as resp:
            body = resp.read().decode(errors="replace")
            code = resp.status
        title_m = re.search(r"<title>(.*?)</title>", body, re.S | re.I)
        row = {
            "url": url,
            "http": code,
            "id_local": 'id="local"' in body,
            "hub_uplink": "usfansspreadsheet.net" in body and "hub-uplink" in body,
            "hmrc": body.count("HMRC"),
            "royal_mail": body.lower().count("royal mail"),
            "data_uk_deepen": f'data-uk-deepen="{STAMP}"' in body,
            "spreadsheet_h1": bool(re.search(r"<h1[^>]*>[^<]*Spreadsheet", body, re.I)),
            "title": re.sub(r"\s+", " ", title_m.group(1)).strip() if title_m else None,
        }
        checks.append(row)

    # homepage still 200 + local (untouched by this deploy)
    home_url = f"https://{HOST}/"
    req = Request(home_url, headers={"User-Agent": "usfans-uk-deepen/1.0"})
    with urlopen(req, timeout=30) as resp:
        home = resp.read().decode(errors="replace")
        home_code = resp.status
    checks.append(
        {
            "url": home_url,
            "http": home_code,
            "id_local": 'id="local"' in home,
            "untouched_deploy": f'data-uk-deepen="{STAMP}"' not in home,
            "hmrc": home.count("HMRC"),
        }
    )

    # hub + nl must remain reachable and were not written by this tool
    for other in ("https://usfansspreadsheet.net/", "https://usfansspreadsheet.nl/"):
        row = _http_nofollow(other)
        # may 200; just record
        if row["http"] in (301, 302) and row.get("location"):
            checks.append(row)
        else:
            req = Request(other, headers={"User-Agent": "usfans-uk-deepen/1.0"})
            with urlopen(req, timeout=25) as resp:
                checks.append({"url": other, "http": resp.status, "note": "not_touched"})

    twin_rows = [
        _http_nofollow("https://usfansspreadsheet.uk/"),
        _http_nofollow("https://usfansspreadsheet.uk/usfans-coupons/"),
    ]
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
    ap.add_argument("--pull", action="store_true", help="Refresh live-base.index.html from Baota")
    ap.add_argument("--build-only", action="store_true")
    ap.add_argument("--deploy", action="store_true")
    ap.add_argument("--verify", action="store_true")
    ap.add_argument("--gsc", action="store_true")
    ap.add_argument("--store-internal", type=Path, default=None)
    ap.add_argument("--gsc-sa", type=Path, default=None)
    args = ap.parse_args()
    if args.load_env:
        _load_env(args.load_env)
    if args.pull:
        pull_live_bases()
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
            if c.get("url", "").startswith(f"https://{HOST}/usfans-")
            and (
                not c.get("id_local")
                or not c.get("hub_uplink")
                or not c.get("data_uk_deepen")
                or c.get("spreadsheet_h1")
                or c.get("http") != 200
            )
        ]
        twin_bad = [
            t
            for t in ver.get("twins", [])
            if t.get("http") not in (301, 302)
            or "usfansspreadsheet.co.uk" not in (t.get("location") or "")
        ]
        if bad or twin_bad:
            print("VERIFY_FAIL", bad, twin_bad)
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
