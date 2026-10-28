#!/usr/bin/env python3
"""Deepen acbuyspreadsheets.nl keep desk: Douane / 1234 AB / PostNL + kill sheet hero.

LIVE only on acbuyspreadsheets.nl. Does not touch hub (allchina-buy.com), CA,
UK, or revive twin allchinabuyspreadsheet.nl. No Phase C.
Requires ORIGIN_SSH_PASS (or --load-env usfans-ssh.env).
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

ROOT = Path(__file__).resolve().parents[1]
OVERLAY = ROOT / "sites" / "acbuyspreadsheets.nl" / "overlay"
HOST = "acbuyspreadsheets.nl"
REMOTE = f"/www/wwwroot/{HOST}"
STAMP = "20261028"
HUB = "https://allchina-buy.com"
# Strategy action 1: shipping + kill sheet hero on home + /acbuy-spreadsheet/
# + money uplink (coupons) + legit NL fingerprint (same pattern as MyCNBox NL).
PAGES = (
    "_home",
    "acbuy-shipping-guide",
    "is-acbuy-legit",
    "acbuy-spreadsheet",
    "acbuy-coupons",
)

STYLE = (
    f'<style id="nl-deepen-{STAMP}">.hub-uplink{{margin:14px 0;padding:12px 14px;'
    "border-left:3px solid #31B38C;background:#eefaf5;color:#1f3f35;line-height:1.6;"
    "font-size:15px;max-width:760px}}.hub-uplink a{{color:#27BA9B;font-weight:600}}"
    "#local{scroll-margin-top:88px}.local-box{margin:1.25em 0;padding:14px 16px;"
    "border:1px solid #e2e8f0;border-radius:10px;background:#f8fafc}"
    ".local-box h2{margin:0 0 .6em;font-size:1.15rem}.local-box ol{margin:.4em 0 0;padding-left:1.2em}"
    ".local-box li{margin:.35em 0}</style>"
)

HUB_UPLINK = (
    f'<p class="hub-uplink" data-nl-deepen="{STAMP}" data-step4-hub="1">'
    "Globale AllChinaBuy / ACBuy Independent Index / spreadsheet / coupons / dataset → "
    f'<a href="{HUB}/">allchina-buy.com</a> · '
    f'<a href="{HUB}/allchinabuy-coupons/">coupons</a> · '
    f'<a href="{HUB}/finds-dataset/">dataset · 11,300+</a>. '
    "Dit desk = Nederlandse postcode, Douane en PostNL — geen tweede spreadsheet-hub."
    "</p>"
)

LOCAL_SHIP = f"""
<section id="local" class="local-box" data-nl-fingerprint="douane-1234ab-postnl" data-nl-deepen="{STAMP}">
<h2>NL-fingerprint vóór je verzendt</h2>
<ol>
<li><strong>Estimator-bestemming: Nederland</strong> — kies NL, niet EU en niet deze hostname.</li>
<li><strong>Adres</strong> — Nederlandse postcode vorm <code>1234 AB</code> (geen Duits Packstation-nummer).</li>
<li><strong>Last mile</strong> — vaak <strong>PostNL</strong> / DHL-handoff; desk verzint geen servicepunt.</li>
<li><strong>Invoer / Douane</strong> — SKU beslist prepaid vs ontvanger. Bron ochtend van verzenden:
<a href="https://www.belastingdienst.nl/wps/wcm/connect/nl/douane/" rel="noopener" target="_blank">Belastingdienst Douane</a>.</li>
</ol>
<p>Cross-links: <a href="/is-acbuy-legit/">Is ACBuy betrouwbaar?</a> ·
<a href="/acbuy-coupons/">NL coupons</a> · brand-index →
<a href="{HUB}/">allchina-buy.com</a>.</p>
</section>
"""

LOCAL_LEGIT = f"""
<section id="local" class="local-box" data-nl-fingerprint="escrow-douane-1234ab" data-nl-deepen="{STAMP}">
<h2>NL-fingerprint bij «is ACBuy betrouwbaar?»</h2>
<ol>
<li><strong>Escrow ≠ Douane</strong> — agent-escrow beschermt de China-koop; invoer naar NL volgt SKU + Douane.</li>
<li><strong>Adres</strong> — <code>1234 AB</code>-vorm; verkeerd land in de estimator = verkeerde quote.</li>
<li><strong>Last mile</strong> — PostNL/DHL-status is geen scam-signaal; houd tracking + Douane-SMS bij.</li>
<li><strong>Klachten</strong> — alleen op <a href="https://www.acbuy.com/" rel="nofollow noopener" target="_blank">acbuy.com</a>; dit desk ziet je account niet.</li>
</ol>
<p>Verzend-check: <a href="/acbuy-shipping-guide/">verzending Nederland</a>.</p>
</section>
"""

LOCAL_SHEET = f"""
<section id="local" class="local-box" data-nl-fingerprint="nl-desk-not-sheet-hub" data-nl-deepen="{STAMP}">
<h2>Deze URL is geen tweede spreadsheet-hub</h2>
<ol>
<li><strong>Brand spreadsheet / finds / dataset</strong> → alleen
<a href="{HUB}/">allchina-buy.com</a> (Independent Index · 11,300+).</li>
<li><strong>Dit desk</strong> = Nederlandse postcode <code>1234 AB</code>, Douane, PostNL, lokale coupons.</li>
<li><strong>Waarom hier nog een pagina?</strong> — NL-zoekers die «acbuy spreadsheet» typen moeten
duidelijk naar de hub, niet een tweede heldencatalogus op .nl.</li>
</ol>
<p>Verzending NL: <a href="/acbuy-shipping-guide/">Douane &amp; 1234 AB</a>.</p>
</section>
"""

LOCAL_COUPON = f"""
<section id="local" class="local-box" data-nl-fingerprint="coupon-ne-douane" data-nl-deepen="{STAMP}">
<h2>NL-coupon ≠ Douane</h2>
<ol>
<li><strong>Coupon / invite</strong> verlaagt agent-fees of eerste order — <em>niet</em> BTW/invoer.</li>
<li><strong>Wereldwijde coupon-waarheidstabel</strong> →
<a href="{HUB}/allchinabuy-coupons/">allchina-buy.com/allchinabuy-coupons</a>; dit desk houdt NL-framing.</li>
<li><strong>Verzenden naar NL</strong> blijft <code>1234 AB</code> + Douane / PostNL — zie
<a href="/acbuy-shipping-guide/">shipping-guide</a>.</li>
</ol>
</section>
"""

LOCAL_HOME_THICKEN = f"""
<section class="local-box" id="douane-postnl-home" data-nl-deepen="{STAMP}" style="max-width:760px;margin:1.5em auto;padding:14px 16px">
<h2>Nederland: Douane, postcode 1234 AB, PostNL</h2>
<p>Deze homepage is de <strong>NL-desk</strong> — geen «ACBuy Spreadsheet»-held.
Afleveradres met postcode-vorm <strong>1234 AB</strong>; invoer volgens
<a href="https://www.belastingdienst.nl/wps/wcm/connect/nl/douane/" rel="noopener" target="_blank">Belastingdienst Douane</a>;
last mile vaak <strong>PostNL</strong>. Wereldwijde Independent Index · 11,300+ →
<a href="{HUB}/">allchina-buy.com</a>. Detail:
<a href="/acbuy-shipping-guide/">verzending Nederland</a>. Stempel: <strong>28 Oct 2026</strong>.</p>
</section>
"""

THICKEN_SHIP = f"""
<section class="local-box" id="douane-1234ab" data-nl-deepen="{STAMP}">
<h2>Douane, postcode 1234 AB, PostNL</h2>
<p>Verzending naar <strong>Nederland</strong> betekent: estimator op <strong>NL</strong>, afleveradres met
postcode-vorm <strong>1234 AB</strong>, last mile vaak via <strong>PostNL</strong> (soms DHL-handoff), en
invoer volgens de <strong>SKU</strong> + actuele
<a href="https://www.belastingdienst.nl/wps/wcm/connect/nl/douane/" rel="noopener" target="_blank">Douane</a>-regels.
Deze URL is geen generieke «Shipping Guide 2026» en geen spreadsheet-held — brand-index blijft op
<a href="{HUB}/">allchina-buy.com</a>.</p>
<p>Prepaid duty vs duties payable by recipient kies je bij het pakket, niet bij de aankoop.
Geen onderwaardering. Datumstempel verdieping: <strong>28 Oct 2026</strong>.</p>
</section>
"""

THICKEN_LEGIT = f"""
<section class="local-box" id="nl-legit-note" data-nl-deepen="{STAMP}">
<h2>Nederland: escrow, Douane, PostNL</h2>
<p>«Is ACBuy betrouwbaar?» voor een <strong>Nederlands bezorgadres</strong> hangt af van escrow in China
én correcte invoer naar NL. Escrow lost geen Douane-geschil op. Check tracking +
<a href="/acbuy-shipping-guide/">verzending Nederland</a> (1234 AB / Douane / PostNL) vóór je «scam» concludeert.
Brand spreadsheet-intent → <a href="{HUB}/">allchina-buy.com</a>.</p>
</section>
"""

THICKEN_SHEET = f"""
<section class="local-box" id="sheet-intent-hub" data-nl-deepen="{STAMP}">
<h2>Sheet-intent hoort op de hub</h2>
<p>Zoekers met exact <strong>acbuy spreadsheet</strong> / <strong>allchinabuy spreadsheet</strong> moeten naar
<a href="{HUB}/">allchina-buy.com</a> (Independent Index · 11,300+ ·
<a href="{HUB}/finds-dataset/">dataset</a> ·
<a href="{HUB}/allchinabuy-coupons/">coupons</a>).
acbuyspreadsheets.nl blijft de NL-desk: Douane, <code>1234 AB</code>, PostNL — zie
<a href="/acbuy-shipping-guide/">shipping-guide</a>.</p>
</section>
"""

THICKEN_COUPON = f"""
<section class="local-box" id="nl-coupon-note" data-nl-deepen="{STAMP}">
<h2>Lokale coupon-context</h2>
<p>Codes hier zijn NL-desk framing. De canonieke werkende-lijst + Independent Index staan op
<a href="{HUB}/allchinabuy-coupons/">allchina-buy.com/allchinabuy-coupons</a>.
Een coupon verandert geen Douane-aangifte — plan invoer via
<a href="/acbuy-shipping-guide/">verzending Nederland</a> (1234 AB / PostNL).</p>
</section>
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


def _inject_head_style(html: str) -> str:
    if f'id="nl-deepen-{STAMP}"' in html:
        return html
    if "</head>" not in html:
        raise SystemExit("no </head>")
    return html.replace("</head>", STYLE + "\n</head>", 1)


def _soften_brand(html: str) -> str:
    html = html.replace("<span>Spreadsheet</span>", "<span>Nederland</span>", 1)
    return html


def _mark_body(html: str) -> str:
    if f'data-nl-deepen="{STAMP}"' in html[:1200]:
        return html
    return re.sub(
        r"<body([^>]*)>",
        rf'<body\1 data-nl-deepen="{STAMP}">',
        html,
        count=1,
        flags=re.I,
    )


def _set_title(html: str, title: str, og: str | None = None) -> str:
    html = re.sub(r"<title>.*?</title>", f"<title>{title}</title>", html, count=1, flags=re.S)
    if og is None:
        og = title.replace("&amp;", "&")
    if re.search(r'property="og:title"', html):
        html = re.sub(
            r'property="og:title" content="[^"]*"',
            f'property="og:title" content="{og}"',
            html,
            count=1,
        )
    # WebPage JSON-LD name (home)
    html = re.sub(
        r'("name":\s*")ACBuy Spreadsheet in het Nederlands:[^"]*(")',
        rf'\1{og}\2',
        html,
        count=1,
    )
    return html


def _set_description(html: str, desc: str) -> str:
    if re.search(r'<meta name="description"', html, re.I):
        return re.sub(
            r'<meta name="description" content="[^"]*"',
            f'<meta name="description" content="{desc}"',
            html,
            count=1,
            flags=re.I,
        )
    return html.replace(
        "</head>",
        f'<meta name="description" content="{desc}">\n</head>',
        1,
    )


def deepen_home(html: str) -> str:
    html = _inject_head_style(html)
    html = _soften_brand(html)
    html = _mark_body(html)
    html = _set_title(
        html,
        "ACBuy Nederland — Douane, NL-postcode 1234 AB, PostNL",
        "ACBuy Nederland — Douane, NL-postcode 1234 AB, PostNL",
    )
    html = _set_description(
        html,
        "NL-desk voor ACBuy/AllChinaBuy: Nederlandse postcode 1234 AB, Belastingdienst Douane, "
        "PostNL. Brand spreadsheet → allchina-buy.com. Bijgewerkt 28 Oct 2026.",
    )
    html = re.sub(
        r"<h1>ACBuy Spreadsheet: de gids om in China te kopen vanaf Nederland</h1>",
        "<h1>ACBuy Nederland: Douane, postcode 1234 AB, PostNL</h1>",
        html,
        count=1,
    )
    html = re.sub(
        r'(<p class="lead">)Hoe je een productlink in de agent plakt, hoe de catalogus van w2clinks werkt, hoe een pakket naar Nederland reist en wat je nagaat vóór de Douane\.(</p>)',
        r"\1Lokale desk voor een Nederlands adres: postcode-vorm <strong>1234 AB</strong>, "
        r"<strong>Douane</strong>-invoer, last mile vaak <strong>PostNL</strong>. "
        f'Brand Independent Index → <a href="{HUB}/">allchina-buy.com</a>.\2',
        html,
        count=1,
    )
    # Reinforce PostNL near existing #local without replacing platform uplink
    if 'id="douane-postnl-home"' not in html and 'id="local"' in html:
        html = re.sub(
            r'(<section class="sec" id="local"[\s\S]*?</section>)',
            r"\1\n" + LOCAL_HOME_THICKEN,
            html,
            count=1,
        )
    if HUB_UPLINK not in html and 'data-step4-hub="1"' not in html:
        html = html.replace("</header>", "</header>\n" + HUB_UPLINK, 1)
    elif 'class="hub-uplink"' not in html and 'id="local"' in html:
        # platform already has inline uplink; still add visible hub-uplink box once
        html = re.sub(
            r'(<section class="sec" id="local"[\s\S]*?</section>)',
            r"\1\n" + HUB_UPLINK,
            html,
            count=1,
        )
    return html


def deepen_shipping(html: str) -> str:
    html = _inject_head_style(html)
    html = _soften_brand(html)
    html = _mark_body(html)
    html = _set_title(
        html,
        "ACBuy verzending Nederland — Douane, NL-postcode 1234 AB, PostNL",
        "ACBuy verzending Nederland — Douane, NL-postcode 1234 AB, PostNL",
    )
    html = _set_description(
        html,
        "NL-desk verzending: postcode 1234 AB, Belastingdienst Douane, PostNL. "
        "Brand spreadsheet → allchina-buy.com. Bijgewerkt 28 Oct 2026.",
    )
    html = re.sub(
        r'<h1 class="atit">.*?</h1>',
        '<h1 class="atit">ACBuy verzending naar Nederland<br>'
        "<em>Douane, NL-postcode 1234 AB, PostNL</em></h1>",
        html,
        count=1,
        flags=re.S,
    )
    html = re.sub(
        r'(<p class="aint">).*?(</p>)',
        r"\1Hoe een pakket naar een Nederlands adres reist: estimator op NL, "
        r"postcode-vorm <strong>1234 AB</strong>, last mile vaak <strong>PostNL</strong>, "
        r"invoer volgens SKU + <strong>Douane</strong>. "
        r"Wereldwijde spreadsheet/coupons → "
        f'<a href="{HUB}/">allchina-buy.com</a>.\2',
        html,
        count=1,
        flags=re.S,
    )
    html = html.replace(
        '<span class="adt">Updated June 2026</span>',
        f'<span class="adt" data-nl-deepen="{STAMP}">Updated 28 Oct 2026 · NL Douane / PostNL</span>',
        1,
    )
    if HUB_UPLINK not in html and 'data-step4-hub="1"' not in html:
        html = html.replace('<header class="ahd">', HUB_UPLINK + '\n<header class="ahd">', 1)
    if 'id="local"' not in html:
        html = html.replace(
            '<h2 class="ph" id="calculator">',
            LOCAL_SHIP + "\n" + THICKEN_SHIP + '\n<h2 class="ph" id="calculator">',
            1,
        )
    if 'id="nl-table-note"' not in html:
        html = html.replace(
            '<h2 class="ph">Delivery times by country</h2>',
            '<h2 class="ph" id="nl-table-note">Levertijden — focus Nederland</h2>\n'
            "<p>Onderstaande tabel is lab-context. Voor <strong>Nederland</strong> kies je NL in de "
            "officiële estimator; postcode <strong>1234 AB</strong>; Douane-regels op de verzenddag; "
            "last mile vaak <strong>PostNL</strong>. "
            f'Geen spreadsheet-held op deze URL — index op <a href="{HUB}/">allchina-buy.com</a>.</p>',
            1,
        )
    return html


def deepen_legit(html: str) -> str:
    html = _inject_head_style(html)
    html = _soften_brand(html)
    html = _mark_body(html)
    html = _set_title(
        html,
        "Is ACBuy betrouwbaar? Nederland — Douane, escrow, PostNL",
        "Is ACBuy betrouwbaar? Nederland — Douane, escrow, PostNL",
    )
    html = _set_description(
        html,
        "Is ACBuy betrouwbaar voor een Nederlands adres? Escrow, Douane, postcode 1234 AB, PostNL. "
        "Brand spreadsheet → allchina-buy.com. 28 Oct 2026.",
    )
    html = re.sub(
        r'<h1 class="atit">.*?</h1>',
        '<h1 class="atit">Is ACBuy <em>betrouwbaar</em>?<br>Nederland · Douane &amp; escrow</h1>',
        html,
        count=1,
        flags=re.S,
    )
    html = re.sub(
        r'(<p class="aint">).*?(</p>)',
        r"\1ACBuy is een Chinese inkoopagent (AllChinaBuy). Voor Nederland: escrow in China is niet "
        r"hetzelfde als <strong>Douane</strong>-invoer. Adres met <strong>1234 AB</strong>; "
        r'verzending via <a href="/acbuy-shipping-guide/">NL shipping-guide</a>. '
        f'Brand-index → <a href="{HUB}/">allchina-buy.com</a>.\2',
        html,
        count=1,
        flags=re.S,
    )
    html = html.replace(
        '<span class="adt">Updated June 2026</span>',
        f'<span class="adt" data-nl-deepen="{STAMP}">Updated 28 Oct 2026 · NL Douane</span>',
        1,
    )
    if HUB_UPLINK not in html and 'data-step4-hub="1"' not in html:
        html = html.replace('<header class="ahd">', HUB_UPLINK + '\n<header class="ahd">', 1)
    if 'id="local"' not in html:
        if 'class="verd' in html:
            html = re.sub(
                r'(<div class="verd[\s\S]*?</div>\s*</div>)',
                r"\1\n" + LOCAL_LEGIT + "\n" + THICKEN_LEGIT,
                html,
                count=1,
            )
        else:
            html = html.replace(
                "</header>",
                "</header>\n" + LOCAL_LEGIT + THICKEN_LEGIT,
                1,
            )
    html = re.sub(
        r'href="/acbuy-spreadsheet/"',
        f'href="{HUB}/"',
        html,
        count=2,
    )
    return html


def deepen_spreadsheet(html: str) -> str:
    html = _inject_head_style(html)
    html = _soften_brand(html)
    html = _mark_body(html)
    html = _set_title(
        html,
        "ACBuy Nederland — NL-postcode &amp; Douane (spreadsheet → hub)",
        "ACBuy Nederland — NL-postcode & Douane (spreadsheet → hub)",
    )
    html = _set_description(
        html,
        "acbuyspreadsheets.nl is de NL-desk (1234 AB, Douane, PostNL). Exact «acbuy spreadsheet» → "
        "allchina-buy.com Independent Index 11,300+. 28 Oct 2026.",
    )
    html = re.sub(
        r"<h1>ACBuy spreadsheet Nederland 2026</h1>",
        "<h1>ACBuy Nederland<br><em>geen tweede spreadsheet-hub</em></h1>",
        html,
        count=1,
    )
    html = re.sub(
        r'(<p class="hsub">).*?(</p>)',
        r"\1Brand spreadsheet / finds / dataset staan op "
        f'<a href="{HUB}/">allchina-buy.com</a> (Independent Index · 11,300+). '
        r"Dit desk dekt <strong>NL-postcode 1234 AB</strong>, Douane en PostNL.\2",
        html,
        count=1,
        flags=re.S,
    )
    # Soften schema name
    html = re.sub(
        r'("name":\s*")ACBuy Spreadsheet 2026(")',
        r'\1ACBuy Nederland desk — spreadsheet → hub\2',
        html,
        count=1,
    )
    if HUB_UPLINK not in html and 'data-step4-hub="1"' not in html:
        if "</section>" in html:
            html = html.replace("</section>", "</section>\n" + HUB_UPLINK, 1)
        else:
            html = html.replace("</header>", "</header>\n" + HUB_UPLINK, 1)
    if 'id="local"' not in html:
        html = html.replace(
            HUB_UPLINK,
            HUB_UPLINK + "\n" + LOCAL_SHEET + "\n" + THICKEN_SHEET,
            1,
        )
    return html


def deepen_coupons(html: str) -> str:
    html = _inject_head_style(html)
    html = _soften_brand(html)
    html = _mark_body(html)
    html = _set_title(
        html,
        "ACBuy coupons Nederland — codes, Douane ≠ korting",
        "ACBuy coupons Nederland — codes, Douane ≠ korting",
    )
    html = _set_description(
        html,
        "NL-desk coupons. Wereldwijde waarheidstabel → allchina-buy.com/allchinabuy-coupons. "
        "Coupon ≠ Douane. Postcode 1234 AB / PostNL. 28 Oct 2026.",
    )
    html = re.sub(
        r"<h1[^>]*>.*?</h1>",
        '<h1 style="font-size:clamp(24px,4vw,36px);font-weight:600;letter-spacing:-.8px;'
        'line-height:1.18;margin-bottom:12px">ACBuy <span style="color:var(--acc)">'
        "coupons Nederland</span><br>codes · Douane ≠ korting</h1>",
        html,
        count=1,
        flags=re.S,
    )
    html = re.sub(
        r'(<p style="font-size:16px;color:var\(--g3\);line-height:1\.8;border-left:3px solid var\(--acc\);padding-left:16px">).*?(</p>)',
        r"\1NL-desk framing voor ACBuy-codes. Canonieke werkende-lijst + Independent Index → "
        f'<a href="{HUB}/allchinabuy-coupons/">allchina-buy.com/allchinabuy-coupons</a>. '
        r"Een coupon verandert geen <strong>Douane</strong>-aangifte; verzending blijft "
        r'<a href="/acbuy-shipping-guide/">1234 AB / PostNL</a>.\2',
        html,
        count=1,
        flags=re.S,
    )
    # Insert uplink after article header (second </header> is content header)
    if HUB_UPLINK not in html and 'data-step4-hub="1"' not in html:
        # Prefer content header close
        parts = html.split("</header>", 2)
        if len(parts) >= 3:
            html = parts[0] + "</header>" + parts[1] + "</header>\n" + HUB_UPLINK + parts[2]
        else:
            html = html.replace("</header>", "</header>\n" + HUB_UPLINK, 1)
    if 'id="local"' not in html:
        html = html.replace(
            HUB_UPLINK,
            HUB_UPLINK + "\n" + LOCAL_COUPON + "\n" + THICKEN_COUPON,
            1,
        )
    return html


PATCHERS = {
    "_home": deepen_home,
    "acbuy-shipping-guide": deepen_shipping,
    "is-acbuy-legit": deepen_legit,
    "acbuy-spreadsheet": deepen_spreadsheet,
    "acbuy-coupons": deepen_coupons,
}

REQUIRED = {
    "_home": (
        "Douane",
        "1234 AB",
        "PostNL",
        'id="local"',
        "allchina-buy.com",
        "finds-dataset",
        f'data-nl-deepen="{STAMP}"',
        "ACBuy Nederland",
    ),
    "acbuy-shipping-guide": (
        "Douane",
        "1234 AB",
        "PostNL",
        'id="local"',
        "allchina-buy.com",
        "finds-dataset",
        f'data-nl-deepen="{STAMP}"',
    ),
    "is-acbuy-legit": (
        "Douane",
        "1234 AB",
        "PostNL",
        'id="local"',
        "allchina-buy.com",
        f'data-nl-deepen="{STAMP}"',
    ),
    "acbuy-spreadsheet": (
        "Douane",
        "1234 AB",
        "PostNL",
        'id="local"',
        "allchina-buy.com",
        "11,300",
        "geen tweede spreadsheet-hub",
        f'data-nl-deepen="{STAMP}"',
    ),
    "acbuy-coupons": (
        "Douane",
        "1234 AB",
        "PostNL",
        'id="local"',
        "allchina-buy.com",
        f'data-nl-deepen="{STAMP}"',
    ),
}

FORBIDDEN_H1 = (
    r"<h1[^>]*>\s*ACBuy Spreadsheet:",
    r"<h1[^>]*>\s*ACBuy spreadsheet Nederland 2026",
    r"<h1[^>]*>[^<]*Shipping Guide 2026",
)


def _src_path(slug: str) -> Path:
    if slug == "_home":
        return OVERLAY / "live-base.index.html"
    return OVERLAY / slug / "live-base.index.html"


def _out_path(slug: str) -> Path:
    if slug == "_home":
        return OVERLAY / "index.html.nl-deepen"
    return OVERLAY / slug / "index.html.nl-deepen"


def _assert_ok(label: str, html: str) -> None:
    for tok in REQUIRED[label]:
        if tok not in html:
            raise SystemExit(f"{label} missing {tok!r}")
    for pat in FORBIDDEN_H1:
        if re.search(pat, html, re.I | re.S):
            raise SystemExit(f"{label} still has forbidden Spreadsheet/generic H1 ({pat})")
    # Home/sheet must not keep Spreadsheet as H1 hero word in title
    title_m = re.search(r"<title>(.*?)</title>", html, re.S | re.I)
    title = title_m.group(1) if title_m else ""
    if label in ("_home", "acbuy-spreadsheet") and re.search(
        r"ACBuy Spreadsheet|ACBuy spreadsheet Nederland 2026", title, re.I
    ):
        raise SystemExit(f"{label} title still Spreadsheet hero: {title!r}")
    for alien in (
        "1010 Wien",
        "Royal Mail",
        "HMRC",
        "00-001",
        "Colissimo",
        "CBSA",
        "A1A 1A1",
        "Correos",
    ):
        if alien in html:
            raise SystemExit(f"{label} leaked sister fingerprint {alien!r}")
    if "data-hub-reclaim" in html or "data-hub-defend" in html:
        raise SystemExit(f"{label} has hub-reclaim/defend marker")


def build() -> dict[str, Path]:
    outs: dict[str, Path] = {}
    for slug in PAGES:
        src = _src_path(slug)
        if not src.is_file():
            raise SystemExit(f"missing live-base {src}")
        html = PATCHERS[slug](src.read_text(encoding="utf-8", errors="replace"))
        _assert_ok(slug, html)
        out = _out_path(slug)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(html, encoding="utf-8")
        print("wrote", out, "bytes", out.stat().st_size)
        outs[slug] = out
    return outs


def _remote_path(slug: str) -> str:
    if slug == "_home":
        return f"{REMOTE}/index.html"
    return f"{REMOTE}/{slug}/index.html"


def deploy() -> str:
    outs = build()
    client = _connect()
    stamp = time.strftime("%Y%m%d-%H%M%S")
    bak = f"/www/backup/acbuy-nl-deepen-{stamp}"

    # Refuse writing hub / CA / UK / twin roots (sanity)
    for forbidden in (
        "/www/wwwroot/allchina-buy.com",
        "/www/wwwroot/acbuyspreadsheets.ca",
        "/www/wwwroot/allchinabuyspreadsheets.co.uk",
        "/www/wwwroot/allchinabuyspreadsheet.nl",
        "/www/wwwroot/allchinabuyspreadsheet.ca",
    ):
        assert not REMOTE.startswith(forbidden)

    _run(client, f"mkdir -p '{bak}'")
    sftp = client.open_sftp()
    for slug, local in outs.items():
        remote = _remote_path(slug)
        raw = local.read_text(encoding="utf-8")
        if 'id="local"' not in raw or "Douane" not in raw or "PostNL" not in raw:
            raise SystemExit(f"refusing PUT {remote}")
        if re.search(r"<h1[^>]*>\s*ACBuy Spreadsheet:", raw, re.I | re.S):
            raise SystemExit(f"refusing Spreadsheet hero PUT {remote}")
        if slug != "_home":
            _run(client, f"mkdir -p '{REMOTE}/{slug}'")
        bak_name = "home-index.html.before" if slug == "_home" else f"{slug}-index.html.before"
        _run(client, f"cp -a '{remote}' '{bak}/{bak_name}' 2>/dev/null || true")
        sftp.put(str(local), remote)
        print("PUT", remote, "bytes", local.stat().st_size)

    # sitemap lastmod bump
    sm_remote = f"{REMOTE}/sitemap.xml"
    _run(client, f"cp -a '{sm_remote}' '{bak}/sitemap.xml.before' 2>/dev/null || true")
    try:
        with sftp.open(sm_remote, "r") as f:
            sm = f.read().decode("utf-8", "replace")
    except OSError:
        sm = ""
    today = time.strftime("%Y-%m-%d")
    if sm:
        for loc in (
            f"https://{HOST}/",
            f"https://{HOST}/acbuy-shipping-guide/",
            f"https://{HOST}/is-acbuy-legit/",
            f"https://{HOST}/acbuy-spreadsheet/",
            f"https://{HOST}/acbuy-coupons/",
        ):
            sm = re.sub(
                rf"(<loc>{re.escape(loc)}</loc>\s*<lastmod>)[^<]+",
                rf"\g<1>{today}",
                sm,
                count=1,
            )
        with sftp.open(sm_remote, "w") as f:
            f.write(sm)
        (OVERLAY / "sitemap.xml").write_text(sm, encoding="utf-8")
        print("sitemap lastmod →", today)
    sftp.close()

    check = _run(
        client,
        "grep -l 'data-nl-deepen=\"20261028\"' "
        f"{REMOTE}/index.html "
        f"{REMOTE}/acbuy-shipping-guide/index.html "
        f"{REMOTE}/is-acbuy-legit/index.html "
        f"{REMOTE}/acbuy-spreadsheet/index.html "
        f"{REMOTE}/acbuy-coupons/index.html; "
        "grep -l 'data-nl-deepen' /www/wwwroot/allchina-buy.com/index.html 2>/dev/null || echo hub_clean; "
        f"ls '{bak}'",
    )
    print(check)
    print("backup", bak)
    client.close()
    return bak


def verify_live() -> dict:
    import http.client
    import urllib.request
    from urllib.parse import urlparse

    checks = []
    urls = [
        f"https://{HOST}/",
        f"https://{HOST}/acbuy-shipping-guide/",
        f"https://{HOST}/is-acbuy-legit/",
        f"https://{HOST}/acbuy-spreadsheet/",
        f"https://{HOST}/acbuy-coupons/",
        "https://allchina-buy.com/",
        "https://allchinabuyspreadsheet.nl/",
        "https://acbuyspreadsheets.ca/",
    ]
    for url in urls:
        req = urllib.request.Request(
            url, method="GET", headers={"User-Agent": "acbuy-nl-deepen/1"}
        )
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                body = resp.read().decode("utf-8", "replace")
                code = resp.status
                final = resp.geturl()
        except Exception as exc:  # noqa: BLE001
            checks.append({"url": url, "error": str(exc)})
            continue
        title_m = re.search(r"<title>(.*?)</title>", body, re.S | re.I)
        h1_m = re.search(r"<h1[^>]*>(.*?)</h1>", body, re.S | re.I)
        title = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", title_m.group(1) if title_m else "")).strip()
        h1 = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", h1_m.group(1) if h1_m else "")).strip()
        entry = {
            "url": url,
            "http": code,
            "final": final,
            "title": title[:160],
            "h1": h1[:160],
            "id_local": 'id="local"' in body,
            "hub_uplink": "allchina-buy.com" in body
            and ("hub-uplink" in body or "finds-dataset" in body or "allchinabuy-coupons" in body),
            "postcode_1234ab": body.count("1234 AB"),
            "douane": body.lower().count("douane"),
            "postnl": body.count("PostNL"),
            "data_nl_deepen": f'data-nl-deepen="{STAMP}"' in body,
            "spreadsheet_h1": bool(
                re.search(r"<h1[^>]*>\s*ACBuy Spreadsheet", body, re.I | re.S)
            ),
        }
        if url in ("https://allchina-buy.com/", "https://acbuyspreadsheets.ca/"):
            entry["untouched_no_nl_deepen"] = f'data-nl-deepen="{STAMP}"' not in body
        checks.append(entry)

    twins = []
    for url, expect_loc in (
        ("https://allchinabuyspreadsheet.nl/", "https://acbuyspreadsheets.nl/"),
    ):
        u = urlparse(url)
        conn = http.client.HTTPSConnection(u.netloc, timeout=20)
        conn.request("HEAD", u.path or "/", headers={"User-Agent": "acbuy-nl-deepen/1"})
        resp = conn.getresponse()
        loc = resp.getheader("Location") or ""
        twins.append(
            {
                "url": url,
                "http": resp.status,
                "location": loc,
                "ok": resp.status in (301, 302) and expect_loc.rstrip("/") in loc.rstrip("/"),
            }
        )
        conn.close()

    return {
        "at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "checks": checks,
        "twins": twins,
    }


def submit_gsc(sa_path: Path) -> dict:
    try:
        from google.oauth2 import service_account
        from googleapiclient.discovery import build
    except ImportError:
        import subprocess

        subprocess.check_call(
            [
                sys.executable,
                "-m",
                "pip",
                "install",
                "google-api-python-client",
                "google-auth",
                "-q",
            ]
        )
        from google.oauth2 import service_account
        from googleapiclient.discovery import build

    scopes = ["https://www.googleapis.com/auth/webmasters"]
    creds = service_account.Credentials.from_service_account_file(str(sa_path), scopes=scopes)
    gsc = build("searchconsole", "v1", credentials=creds, cache_discovery=False)
    site = f"sc-domain:{HOST}"
    feed = f"https://{HOST}/sitemap.xml"
    gsc.sitemaps().submit(siteUrl=site, feedpath=feed).execute()
    listed = gsc.sitemaps().list(siteUrl=site).execute()
    return {
        "site": site,
        "feed": feed,
        "submitted_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "list": listed,
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--load-env", type=Path, help="internal/usfans-ssh.env")
    ap.add_argument("--build", action="store_true")
    ap.add_argument("--deploy", action="store_true")
    ap.add_argument("--verify", action="store_true")
    ap.add_argument("--submit-gsc", type=Path, nargs="?", const=True)
    args = ap.parse_args()
    if args.load_env:
        _load_env(args.load_env)
    if args.deploy:
        bak = deploy()
        print("DONE backup", bak)
        return
    if args.build or not any([args.verify, args.submit_gsc]):
        build()
    if args.verify:
        result = verify_live()
        print(json.dumps(result, indent=2, ensure_ascii=False))
    if args.submit_gsc is not None:
        sa = (
            Path(args.submit_gsc)
            if isinstance(args.submit_gsc, Path)
            else Path("/cursor/stores/self/internal/gsc-sa.json")
        )
        out = submit_gsc(sa)
        print(
            json.dumps(
                {
                    "site": out["site"],
                    "feed": out["feed"],
                    "submitted_at": out["submitted_at"],
                },
                indent=2,
            )
        )
        out_path = ROOT / "tmp-acbuy-nl-gsc-submit.json"
        # Prefer store internal when available
        store = Path("/cursor/stores/self/internal/allchinabuy-nl-deepen")
        store.mkdir(parents=True, exist_ok=True)
        (store / "gsc_sitemap_submit.json").write_text(
            json.dumps(out, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
        )
        print("wrote", store / "gsc_sitemap_submit.json")


if __name__ == "__main__":
    main()
