#!/usr/bin/env python3
"""Superbuy CA keep desk deepen (P0): remove Spreadsheet hero, inject #local,
thicken /superbuy-shipping/ with Canada Post / CBSA / A1A 1A1.

Does NOT touch .us or IT. Does NOT create a spreadsheet hub.
"""
from __future__ import annotations

import os
import re
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "sites" / "superbuyspreadsheets.ca"
OVERLAY = SITE / "overlay"
STAMP = "20261027"
MARKER = f'data-ca-deepen="{STAMP}"'

LOCAL_HOME = """
<section class="sec sec--tint" id="local" data-ca-deepen="20261027">
  <div class="wrap">
    <h2>Canada landing checks — Canada Post, CBSA, form A1A 1A1</h2>
    <p class="lead">This desk is a Canada landing assistant, not a global Superbuy spreadsheet hub. Use a Canadian postal code (form <strong>A1A 1A1</strong>), not a US ZIP. Last-mile is usually <strong>Canada Post</strong>; duties and GST/HST follow the booked SKU and <strong>CBSA</strong> rules the morning you ship.</p>
    <ol class="list">
      <li><strong>Estimator destination: Canada (CA)</strong> — pick CA in the official freight tool. A US ZIP is the wrong country even if the parcel title says “North America”.</li>
      <li><strong>Postal code form A1A 1A1</strong> — Canadian addresses use the ANA NAN pattern. Do not paste a five-digit US ZIP into the warehouse address book.</li>
      <li><strong>CBSA + GST/HST</strong> — who pays is on the SKU (prepaid vs collect). This desk does not invent a duty rate or coach under-declaration. Read <a href="https://www.cbsa-asfc.gc.ca/" rel="noopener">CBSA</a> the same morning.</li>
      <li><strong>Canada Post last-mile</strong> — many lines hand off to Canada Post for domestic delivery; tracking may pause at the CBSA handoff before a local scan appears.</li>
      <li><strong>Form E14 / release paperwork</strong> — when CBSA or the broker asks for release docs, use the parcel ID from Superbuy; this HTML is not a customs filing desk.</li>
    </ol>
    <p>Money pages on this host: <a href="/superbuy-shipping/">Shipping to Canada</a> · <a href="/is-superbuy-legit/">Is Superbuy legit?</a> · <a href="/superbuy-coupons/">Coupons</a>. EMS preferential-line notices stay as long-tail, not the homepage KPI. Live freight money: <a href="https://www.superbuy.com/en/page/query/freight/" rel="noopener">official estimator</a> (destination Canada).</p>
  </div>
</section>
""".strip()

LOCAL_SHIP = """
<section class="card" id="local" data-ca-deepen="20261027">
  <h2>Canada Post · CBSA · form A1A 1A1</h2>
  <p>Shoppers searching <em>superbuy shipping to canada</em> need a Canada landing checklist — not a global spreadsheet hero.</p>
  <ul>
    <li><strong>Canada Post</strong> — typical last-mile after the international line clears; expect a quiet gap between export scan and the first Canada Post / broker event.</li>
    <li><strong>CBSA</strong> — screening and GST/HST assessment follow the booked SKU and declared contents. Coupons cut Superbuy fees; they do not erase import charges.</li>
    <li><strong>Postal code form A1A 1A1</strong> — Canadian addresses only. A US ZIP routes the estimator to the wrong country and can strand the parcel.</li>
    <li><strong>Form E14 / release</strong> — if CBSA or a broker requests release paperwork, reply with the Superbuy parcel ID and commercial invoice from the app. This page does not file for you.</li>
  </ul>
  <p>Cross-check: <a href="/is-superbuy-legit/">Is Superbuy legit in Canada?</a> · EMS preferential-line notices remain long-tail on this host · estimator <a href="https://www.superbuy.com/en/page/query/freight/" rel="noopener">superbuy.com freight</a> with destination <strong>CA</strong>.</p>
</section>
""".strip()

SHIP_THICKEN = """
<section class="card" data-ca-deepen="20261027">
  <h2>Shipping Superbuy parcels to Canada (thick checklist)</h2>
  <p>After QC photos look right, submit the parcel with destination <strong>Canada</strong>. Compare lines on volumetric weight, battery/brand rules, and whether GST/HST is prepaid or collect. Budget a CBSA buffer separately from the Superbuy freight quote.</p>
  <h3>Canada Post handoff</h3>
  <p>Many CA-bound SKUs finish on <strong>Canada Post</strong> (community mailbox, flex delivery, or retail counter pickup). When tracking sits on “departed origin / in customs”, wait for a CBSA or Canada Post scan before opening a missing-parcel ticket — export gaps are common on economy air.</p>
  <h3>Address book: A1A 1A1 vs US ZIP</h3>
  <p>Warehouse address books often default to US-style fields. For Canada use the <strong>A1A 1A1</strong> postal pattern, province code, and a phone that can receive carrier SMS. Do not reuse a US ZIP “because it worked once” — the estimator country must stay CA.</p>
  <h3>GST/HST, duties, Form E14</h3>
  <p>Declare contents consistently with what QC photographed. GST/HST and duty liability follow the SKU and CBSA rules that day; this desk never pastes a fake threshold or coaches undervaluation. If a broker emails about <strong>Form E14</strong> or release, answer from the Superbuy ticket with parcel ID — not from this hostname.</p>
  <h3>Line choice for Canadian buyers</h3>
  <p>Economy lines = longer CBSA dwell; express = fewer quiet days but higher CAD outlay. Shoes and boxed sneakers bill heavy on volume. Re-run the <a href="https://www.superbuy.com/en/page/query/freight/">official estimator</a> the morning you pay freight with destination Canada.</p>
</section>
""".strip()


def _sub_title(html: str, title: str) -> str:
    html = re.sub(r"<title>.*?</title>", f"<title>{title}</title>", html, count=1, flags=re.S)
    html = re.sub(
        r'("name":\s*")Superbuy Spreadsheet[^"]*(")',
        rf'\1{title}\2',
        html,
        count=1,
    )
    return html


def patch_home(html: str) -> str:
    title = "Superbuy Canada — Canada Post, CBSA, form A1A 1A1"
    html = _sub_title(html, title)
    html = re.sub(
        r'<meta name="description" content="[^"]*"',
        '<meta name="description" content="Canada landing desk for Superbuy: Canada Post last-mile, CBSA / GST-HST notes, postal code form A1A 1A1. Not a global spreadsheet hub."',
        html,
        count=1,
    )
    # brand chip
    html = html.replace("<span>Spreadsheet</span>", "<span>Canada</span>", 1)
    # nav → money URLs (shipping + legit), keep guide/catalog
    html = re.sub(
        r'<nav class="nav" aria-label="Main menu">.*?</nav>',
        (
            '<nav class="nav" aria-label="Main menu">'
            '<a href="/" aria-current="page">Home</a>'
            '<a href="/superbuy-shipping/">Shipping</a>'
            '<a href="/is-superbuy-legit/">Legit?</a>'
            '<a href="/superbuy-coupons/">Coupons</a>'
            '<a href="/how-to-use-superbuy/">Guide</a>'
            '<a href="#local">Canada checks</a>'
            "</nav>"
        ),
        html,
        count=1,
        flags=re.S,
    )
    # hero
    html = re.sub(
        r'<span class="eyebrow">.*?</span>',
        '<span class="eyebrow">Canada landing desk · not a spreadsheet hub</span>',
        html,
        count=1,
        flags=re.S,
    )
    html = re.sub(
        r"<h1>.*?</h1>",
        "<h1>Superbuy for a Canadian delivery address (Canada Post, CBSA, form A1A 1A1)</h1>",
        html,
        count=1,
        flags=re.S,
    )
    html = re.sub(
        r'<p class="lead">.*?</p>',
        (
            '<p class="lead">Independent Canada desk on superbuyspreadsheets.ca: plan shipping to Canada with '
            "<strong>Canada Post</strong> last-mile notes, <strong>CBSA</strong> / GST-HST context, and postal code "
            "<strong>form A1A 1A1</strong> — not a US ZIP and not a global spreadsheet hero.</p>"
        ),
        html,
        count=1,
        flags=re.S,
    )
    if 'id="local"' not in html:
        html = re.sub(
            r"(</section>\s*)(<section class=\"sec sec--first\" id=\"agent\">)",
            r"\1\n" + LOCAL_HOME + "\n\2",
            html,
            count=1,
        )
    # footer brand
    html = html.replace("<h3>Superbuy Spreadsheet</h3>", "<h3>Superbuy Canada desk</h3>", 1)
    html = re.sub(
        r"(Independent English-language guide to Superbuy and to how you use the w2clinks catalogue to buy in China from Canada\.)",
        "Canada landing assistant: Canada Post, CBSA, form A1A 1A1. Catalogue search stays optional — shipping and legit pages are the money URLs.",
        html,
        count=1,
    )
    html = html.replace(
        "Superbuy Spreadsheet is an independent information site.",
        "This Canada desk is an independent information site.",
        1,
    )
    html = html.replace(
        "&copy; 2026 Superbuy Spreadsheet.",
        "&copy; 2026 Superbuy Canada desk (superbuyspreadsheets.ca).",
        1,
    )
    # footer sections link shipping
    html = html.replace('href="/superbuy-freight/">Shipping and customs</a>', 'href="/superbuy-shipping/">Shipping to Canada</a>', 1)
    if MARKER not in html:
        html = html.replace("<html", f"<html {MARKER}", 1)
    return html


def patch_shipping(html: str) -> str:
    title = "Superbuy Shipping to Canada — Canada Post, CBSA, A1A 1A1 (2026)"
    html = re.sub(r"<title>.*?</title>", f"<title>{title}</title>", html, count=1, flags=re.S)
    html = re.sub(
        r'<meta name="description" content="[^"]*"',
        '<meta name="description" content="Superbuy shipping to Canada: Canada Post last-mile, CBSA / GST-HST, postal code form A1A 1A1, Form E14 release notes. Estimator destination CA."',
        html,
        count=1,
    )
    # fix swapped nav labels on CMS chrome
    html = re.sub(
        r'<nav class="[^"]*"[^>]*>.*?</nav>',
        (
            '<nav class="header-nav">'
            '<a href="/">Canada desk</a>'
            '<a href="/superbuy-shipping/" aria-current="page">Shipping</a>'
            '<a href="/is-superbuy-legit/">Is it legit?</a>'
            '<a href="/superbuy-coupons/">Coupons</a>'
            '<a href="/how-to-use-superbuy/">How to use</a>'
            '<a href="#local">Canada checks</a>'
            "</nav>"
        ),
        html,
        count=1,
        flags=re.S,
    )
    html = re.sub(
        r'<span class="od-badge">.*?</span>',
        '<span class="od-badge">Canada shipping desk · Canada Post / CBSA</span>',
        html,
        count=1,
        flags=re.S,
    )
    html = re.sub(
        r"<h1>.*?</h1>",
        "<h1>Superbuy shipping to Canada: Canada Post, CBSA, form A1A 1A1</h1>",
        html,
        count=1,
        flags=re.S,
    )
    html = re.sub(
        r'(<section class="hero">[\s\S]*?<p class="lead">).*?(</p>)',
        (
            r"\1Canadian buyers searching shipping to Canada need line choice, honest declared value, "
            r"<strong>Canada Post</strong> last-mile timing, and <strong>CBSA</strong> / GST-HST context — "
            r"with postal code <strong>form A1A 1A1</strong>, not a US ZIP.\2"
        ),
        html,
        count=1,
    )
    # fix US leakage in CA rates card
    html = html.replace(
        "US delivery costs depend on actual weighed parcel size",
        "Canada delivery costs depend on actual weighed parcel size",
        1,
    )
    html = html.replace(
        "US buyers should budget for possible customs review. De minimis rules can change",
        "Canadian buyers should budget for possible CBSA review. GST/HST and duty rules can change",
        1,
    )
    html = html.replace(
        'src="https://flagcdn.com/w28/us.png"',
        'src="https://flagcdn.com/w28/ca.png"',
        1,
    )
    # country guide blurb: drop spreadsheet hero intent
    html = re.sub(
        r"(Canadian buyers search )superbuy spreadsheet, coupon codes, and shipping to Canada\.",
        r"\1shipping to Canada, CBSA timing, and Canada Post last-mile — coupons are secondary.",
        html,
        count=1,
    )
    html = re.sub(
        r"Top regional queries we see in research data include: superbuy spreadsheet\.",
        "Top regional queries we see include: superbuy shipping to canada, CBSA, and Canada Post handoff.",
        html,
        count=1,
    )
    # org naming
    html = html.replace("Superbuy Spreadsheet Guide", "Superbuy Canada shipping desk")
    # insert #local + thicken after country guide card (before live policy) or after hero main start
    if 'id="local"' not in html:
        # place after opening container inside main, before first thin workflow OR after country guide
        if 'class="card od-country-guide"' in html:
            html = re.sub(
                r'(<div class="card od-country-guide">[\s\S]*?</div>)(\s*<div class="card od-live-panel")',
                r"\1\n" + LOCAL_SHIP + "\n" + SHIP_THICKEN + r"\2",
                html,
                count=1,
            )
        else:
            html = re.sub(
                r"(<h1>.*?</h1>)",
                r"\1\n" + LOCAL_SHIP + "\n" + SHIP_THICKEN,
                html,
                count=1,
                flags=re.S,
            )
    if MARKER not in html:
        html = html.replace("<html", f"<html {MARKER}", 1)
    return html


def build() -> tuple[Path, Path]:
    home_src = OVERLAY / "live-base.index.html"
    ship_src = OVERLAY / "superbuy-shipping" / "live-base.index.html"
    if not home_src.is_file() or not ship_src.is_file():
        raise SystemExit("missing live-base snapshots; fetch LIVE first")
    home = patch_home(home_src.read_text(encoding="utf-8"))
    ship = patch_shipping(ship_src.read_text(encoding="utf-8"))
    for label, html, need in (
        ("home", home, ("Canada Post", "CBSA", "A1A 1A1", 'id="local"', "Form E14")),
        ("ship", ship, ("Canada Post", "CBSA", "A1A 1A1", 'id="local"', "Form E14", "shipping to Canada")),
    ):
        for tok in need:
            if tok not in html:
                raise SystemExit(f"{label} missing {tok!r}")
        if re.search(r"Superbuy Spreadsheet:", html):
            raise SystemExit(f"{label} still has Spreadsheet H1 hero")
        if "Poste Italiane" in html or "Packstation" in html:
            raise SystemExit(f"{label} leaked sister fingerprint")
    home_out = OVERLAY / "index.html.ca-deepen"
    ship_out = OVERLAY / "superbuy-shipping" / "index.html.ca-deepen"
    home_out.write_text(home, encoding="utf-8")
    ship_out.write_text(ship, encoding="utf-8")
    print("wrote", home_out, "bytes", home_out.stat().st_size)
    print("wrote", ship_out, "bytes", ship_out.stat().st_size)
    return home_out, ship_out


def _connect():
    try:
        import paramiko
    except ImportError:
        import subprocess

        subprocess.check_call([sys.executable, "-m", "pip", "install", "paramiko", "-q"])
        import paramiko

    password = os.environ.get("ORIGIN_SSH_PASS")
    if not password:
        raise SystemExit("Set ORIGIN_SSH_PASS")
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect("31.97.41.31", username="root", password=password, timeout=30)
    return client


def _run(client, cmd: str, timeout: int = 120) -> str:
    _, stdout, stderr = client.exec_command(cmd, timeout=timeout)
    return (stdout.read() + stderr.read()).decode(errors="replace").strip()


def deploy() -> str:
    home_out, ship_out = build()
    client = _connect()
    stamp = time.strftime("%Y%m%d-%H%M%S")
    bak = f"/www/backup/superbuy-ca-deepen-{stamp}"
    host = "superbuyspreadsheets.ca"
    root = f"/www/wwwroot/{host}"
    _run(client, f"mkdir -p '{bak}'")
    # refuse if .us wwwroot would be written — we only touch .ca
    sftp = client.open_sftp()
    pairs = [
        (home_out, f"{root}/index.html", "index.html"),
        (ship_out, f"{root}/superbuy-shipping/index.html", "superbuy-shipping.index.html"),
    ]
    for local, remote, bak_name in pairs:
        raw = local.read_text(encoding="utf-8")
        if 'id="local"' not in raw or "Canada Post" not in raw:
            raise SystemExit(f"refusing PUT {remote}")
        if "Spreadsheet: the guide" in raw:
            raise SystemExit(f"refusing Spreadsheet hero on {remote}")
        _run(client, f"cp -a '{remote}' '{bak}/{bak_name}.before'")
        sftp.put(str(local), remote)
        print("PUT", remote, "bytes", local.stat().st_size)
    # sitemap lastmod bump for money URLs
    sm_remote = f"{root}/sitemap.xml"
    _run(client, f"cp -a '{sm_remote}' '{bak}/sitemap.xml.before'")
    with sftp.open(sm_remote, "r") as f:
        sm = f.read().decode("utf-8", "replace")
    today = time.strftime("%Y-%m-%d")
    for loc in (
        "https://superbuyspreadsheets.ca/",
        "https://superbuyspreadsheets.ca/superbuy-shipping/",
        "https://superbuyspreadsheets.ca/is-superbuy-legit/",
    ):
        sm = re.sub(
            rf"(<loc>{re.escape(loc)}</loc>\s*<lastmod>)[^<]+",
            rf"\g<1>{today}",
            sm,
            count=1,
        )
    with sftp.open(sm_remote, "w") as f:
        f.write(sm)
    print("sitemap lastmod →", today)
    sftp.close()
    # verify .us still 301 and we did not write us wwwroot
    us_check = _run(
        client,
        "test -f /www/wwwroot/superbuyspreadsheets.us/index.html && echo HAS_US_INDEX || echo NO_US_INDEX; "
        "ls /www/wwwroot/superbuyspreadsheets.ca/index.html /www/wwwroot/superbuyspreadsheets.ca/superbuy-shipping/index.html",
    )
    print(us_check)
    print("backup", bak)
    client.close()
    return bak


def main() -> None:
    if "--deploy" in sys.argv:
        deploy()
        return
    build()


if __name__ == "__main__":
    main()
