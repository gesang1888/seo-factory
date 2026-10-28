#!/usr/bin/env python3
"""Deepen mycnbox.nl keep desk: Douane / 1234 AB / PostNL-DHL + hub uplink.

LIVE only on mycnbox.nl. Does not touch hub (.eu), UK/PL, watch es/de/fr,
or revive haul.com (Phase C). Requires ORIGIN_SSH_PASS (or --load-env).
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
OVERLAY = ROOT / "sites" / "mycnbox.nl" / "overlay"
HOST = "mycnbox.nl"
REMOTE = f"/www/wwwroot/{HOST}"
STAMP = "20261028"
HUB = "https://mycnbox.eu"
PAGES = (
    "mycnbox-shipping-guide",
    "is-mycnbox-legit",
    "mycnbox-spreadsheet",
    "mycnbox-coupons",
)

STYLE = (
    f'<style id="nl-deepen-{STAMP}">.hub-uplink{{margin:14px 0 0;padding:12px 14px;'
    "border-left:3px solid #ff5501;background:#fff7f2;color:#3f2a1f;line-height:1.6;"
    "font-size:15px;max-width:760px}}.hub-uplink a{{color:#ff5501;font-weight:600}}"
    "#local{scroll-margin-top:88px}.local-box{margin:1.25em 0;padding:14px 16px;"
    "border:1px solid #e2e8f0;border-radius:10px;background:#f8fafc}"
    ".local-box h2{margin:0 0 .6em;font-size:1.15rem}.local-box ol{margin:.4em 0 0;padding-left:1.2em}"
    ".local-box li{margin:.35em 0}</style>"
)

HUB_UPLINK = (
    f'<p class="hub-uplink" data-nl-deepen="{STAMP}" data-step4-hub="1">'
    "Globale MyCNBox Independent Index / spreadsheet / coupons / dataset → "
    f'<a href="{HUB}/">mycnbox.eu</a> · '
    f'<a href="{HUB}/mycnbox-coupons/">coupons</a> · '
    f'<a href="{HUB}/finds-dataset/">dataset · 11,300+</a>. '
    "Dit desk = NL-postcode, Douane en lokale verzending — geen tweede spreadsheet-hub."
    "</p>"
)

LOCAL_SHIP = f"""
<section id="local" class="local-box" data-nl-fingerprint="douane-1234ab-postnl" data-nl-deepen="{STAMP}">
<h2>NL-fingerprint vóór je verzendt</h2>
<ol>
<li><strong>Estimator-bestemming: Nederland</strong> — kies NL, niet EU en niet deze hostname.</li>
<li><strong>Adres</strong> — Nederlandse postcode vorm <code>1234 AB</code> (geen Duits Packstation-nummer).</li>
<li><strong>Last mile</strong> — vaak <strong>DHL</strong> / PostNL-handoff; desk verzint geen servicepunt.</li>
<li><strong>Invoer / Douane</strong> — SKU beslist prepaid vs ontvanger. Bron ochtend van verzenden:
<a href="https://www.belastingdienst.nl/wps/wcm/connect/nl/douane/" rel="noopener" target="_blank">Belastingdienst Douane</a>.</li>
</ol>
<p>Cross-links: <a href="/is-mycnbox-legit/">Is MyCNBox legitiem?</a> ·
<a href="/mycnbox-coupons/">NL coupons</a> · brand-index →
<a href="{HUB}/">mycnbox.eu</a>.</p>
</section>
"""

LOCAL_LEGIT = f"""
<section id="local" class="local-box" data-nl-fingerprint="escrow-douane-1234ab" data-nl-deepen="{STAMP}">
<h2>NL-fingerprint bij «is MyCNBox legitiem?»</h2>
<ol>
<li><strong>Escrow ≠ Douane</strong> — agent-escrow beschermt de China-koop; invoer naar NL volgt SKU + Douane.</li>
<li><strong>Adres</strong> — <code>1234 AB</code>-vorm; verkeerd land in de estimator = verkeerde quote.</li>
<li><strong>Last mile</strong> — DHL/PostNL-status is geen scam-signaal; houd tracking + Douane-SMS bij.</li>
<li><strong>Klachten</strong> — alleen op <a href="https://www.mycnbox.com/" rel="nofollow noopener" target="_blank">mycnbox.com</a>; dit desk ziet je account niet.</li>
</ol>
<p>Verzend-check: <a href="/mycnbox-shipping-guide/">verzending Nederland</a>.</p>
</section>
"""

LOCAL_SHEET = f"""
<section id="local" class="local-box" data-nl-fingerprint="nl-desk-not-sheet-hub" data-nl-deepen="{STAMP}">
<h2>Deze URL is geen tweede spreadsheet-hub</h2>
<ol>
<li><strong>Brand spreadsheet / finds / dataset</strong> → alleen
<a href="{HUB}/">mycnbox.eu</a> (Independent Index · 11,300+).</li>
<li><strong>Dit desk</strong> = Nederlandse postcode <code>1234 AB</code>, Douane, lokale coupons/QC.</li>
<li><strong>Waarom hier nog een pagina?</strong> — NL-zoekers die «mycnbox spreadsheet» typen moeten
duidelijk naar de hub, niet een tweede heldencatalogus op .nl.</li>
</ol>
<p>Verzending NL: <a href="/mycnbox-shipping-guide/">Douane &amp; 1234 AB</a>.</p>
</section>
"""

LOCAL_COUPON = f"""
<section id="local" class="local-box" data-nl-fingerprint="coupon-ne-douane" data-nl-deepen="{STAMP}">
<h2>NL-coupon ≠ Douane</h2>
<ol>
<li><strong>Coupon / invite</strong> verlaagt agent-fees of eerste order — <em>niet</em> BTW/invoer.</li>
<li><strong>Wereldwijde coupon-waarheidstabel</strong> →
<a href="{HUB}/mycnbox-coupons/">mycnbox.eu/mycnbox-coupons</a>; dit desk houdt NL-framing.</li>
<li><strong>Verzenden naar NL</strong> blijft <code>1234 AB</code> + Douane — zie
<a href="/mycnbox-shipping-guide/">shipping-guide</a>.</li>
</ol>
</section>
"""

THICKEN_SHIP = f"""
<section class="local-box" id="douane-1234ab" data-nl-deepen="{STAMP}">
<h2>Douane, postcode 1234 AB, DHL/PostNL</h2>
<p>Verzending naar <strong>Nederland</strong> betekent: estimator op <strong>NL</strong>, afleveradres met
postcode-vorm <strong>1234 AB</strong>, last mile vaak via <strong>DHL</strong> (soms PostNL-handoff), en
invoer volgens de <strong>SKU</strong> + actuele
<a href="https://www.belastingdienst.nl/wps/wcm/connect/nl/douane/" rel="noopener" target="_blank">Douane</a>-regels.
Deze URL is geen «Shipping Guide 2026»-generiek stuk en geen spreadsheet-held — brand-index blijft op
<a href="{HUB}/">mycnbox.eu</a>.</p>
<p>Prepaid duty vs duties payable by recipient kies je bij het pakket, niet bij de aankoop.
Geen onderwaardering. iDEAL is een NL-betaalrail in de officiële app — bevestig daar, niet op dit desk.
Datumstempel verdieping: <strong>28 Oct 2026</strong>.</p>
</section>
"""

THICKEN_LEGIT = f"""
<section class="local-box" id="nl-legit-note" data-nl-deepen="{STAMP}">
<h2>Nederland: escrow, Douane, PostNL/DHL</h2>
<p>«Is MyCNBox legitiem?» voor een <strong>Nederlands bezorgadres</strong> hangt af van escrow in China
én correcte invoer naar NL. Escrow lost geen Douane-geschil op. Check tracking +
<a href="/mycnbox-shipping-guide/">verzending Nederland</a> (1234 AB / Douane) vóór je «scam» concludeert.
Brand spreadsheet-intent → <a href="{HUB}/">mycnbox.eu</a>.</p>
</section>
"""

THICKEN_SHEET = f"""
<section class="local-box" id="sheet-intent-hub" data-nl-deepen="{STAMP}">
<h2>Sheet-intent hoort op de hub</h2>
<p>Zoekers met exact <strong>mycnbox spreadsheet</strong> moeten naar
<a href="{HUB}/">mycnbox.eu</a> (Independent Index · 11,300+ ·
<a href="{HUB}/finds-dataset/">dataset</a> ·
<a href="{HUB}/mycnbox-coupons/">coupons</a>).
mycnbox.nl blijft de NL-desk: Douane, <code>1234 AB</code>, lokale verzending — zie
<a href="/mycnbox-shipping-guide/">shipping-guide</a>.</p>
</section>
"""

THICKEN_COUPON = f"""
<section class="local-box" id="nl-coupon-note" data-nl-deepen="{STAMP}">
<h2>Lokale coupon-context</h2>
<p>Codes hier zijn NL-desk framing. De canonieke werkende-lijst + Independent Index staan op
<a href="{HUB}/mycnbox-coupons/">mycnbox.eu/mycnbox-coupons</a>.
Een coupon verandert geen Douane-aangifte — plan invoer via
<a href="/mycnbox-shipping-guide/">verzending Nederland</a>.</p>
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
            # Keep leading semicolon; strip only wrapping quotes if both ends quoted.
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
    html = re.sub(
        r"<h3>MyCNBox Spreadsheet</h3>",
        "<h3>MyCNBox Nederland</h3>",
        html,
        count=1,
    )
    html = html.replace(
        "MyCNBox Spreadsheet is een onafhankelijke",
        "mycnbox.nl is de NL-desk (Douane / 1234 AB). Brand-spreadsheet → mycnbox.eu. MyCNBox Spreadsheet was een onafhankelijke",
        1,
    )
    html = html.replace(
        "&copy; 2026 MyCNBox Spreadsheet.",
        "&copy; 2026 MyCNBox Nederland desk.",
        1,
    )
    return html


def _mark_body(html: str) -> str:
    if f'data-nl-deepen="{STAMP}"' in html[:800]:
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
        og = re.sub(r"<[^>]+>", "", title)
        og = og.replace("&amp;", "&")
    html = re.sub(
        r'property="og:title" content="[^"]*"',
        f'property="og:title" content="{og}"',
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


def deepen_shipping(html: str) -> str:
    html = _inject_head_style(html)
    html = _soften_brand(html)
    html = _mark_body(html)
    html = _set_title(
        html,
        "MyCNBox verzending Nederland — Douane, NL-postcode 1234 AB, PostNL/DHL",
        "MyCNBox verzending Nederland — Douane, NL-postcode 1234 AB, PostNL/DHL",
    )
    html = _set_description(
        html,
        "NL-desk verzending: postcode 1234 AB, Belastingdienst Douane, DHL/PostNL. "
        "Brand spreadsheet → mycnbox.eu. Bijgewerkt 28 Oct 2026.",
    )
    html = re.sub(
        r'<h1 class="atit">.*?</h1>',
        '<h1 class="atit">MyCNBox verzending naar Nederland<br>'
        "<em>Douane, NL-postcode 1234 AB, DHL/PostNL</em></h1>",
        html,
        count=1,
        flags=re.S,
    )
    html = re.sub(
        r'(<p class="aint">).*?(</p>)',
        r"\1Hoe een pakket naar een Nederlands adres reist: estimator op NL, "
        r"postcode-vorm <strong>1234 AB</strong>, last mile vaak DHL/PostNL, "
        r"invoer volgens SKU + <strong>Douane</strong>. "
        r"Wereldwijde spreadsheet/coupons → "
        f'<a href="{HUB}/">mycnbox.eu</a>.\2',
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
        html = html.replace("</header>", "</header>\n" + HUB_UPLINK, 1)
    if 'id="local"' not in html:
        html = html.replace(
            '<h2 class="ph" id="calculator">',
            LOCAL_SHIP + "\n" + THICKEN_SHIP + '\n<h2 class="ph" id="calculator">',
            1,
        )
    # Prefer NL row visibility note before multi-country table
    if 'id="nl-table-note"' not in html:
        html = html.replace(
            '<h2 class="ph">Delivery times by country</h2>',
            '<h2 class="ph" id="nl-table-note">Levertijden — focus Nederland</h2>\n'
            "<p>Onderstaande tabel is lab-context. Voor <strong>Nederland</strong> kies je NL in de "
            "officiële estimator; postcode <strong>1234 AB</strong>; Douane-regels op de verzenddag. "
            f"Geen spreadsheet-held op deze URL — index op <a href=\"{HUB}/\">mycnbox.eu</a>.</p>",
            1,
        )
    return html


def deepen_legit(html: str) -> str:
    html = _inject_head_style(html)
    html = _soften_brand(html)
    html = _mark_body(html)
    html = _set_title(
        html,
        "Is MyCNBox legitiem? Nederland — Douane, escrow, PostNL/DHL",
        "Is MyCNBox legitiem? Nederland — Douane, escrow, PostNL/DHL",
    )
    html = _set_description(
        html,
        "Is MyCNBox legitiem voor een Nederlands adres? Escrow, Douane, postcode 1234 AB. "
        "Brand spreadsheet → mycnbox.eu. 28 Oct 2026.",
    )
    html = re.sub(
        r'<h1 class="atit">.*?</h1>',
        '<h1 class="atit">Is MyCNBox <em>legitiem</em>?<br>Nederland · Douane &amp; escrow</h1>',
        html,
        count=1,
        flags=re.S,
    )
    html = re.sub(
        r'(<p class="aint">).*?(</p>)',
        r"\1MyCNBox is een Chinese inkoopagent. Voor Nederland: escrow in China is niet hetzelfde "
        r"als <strong>Douane</strong>-invoer. Adres met <strong>1234 AB</strong>; verzending via "
        r'<a href="/mycnbox-shipping-guide/">NL shipping-guide</a>. '
        f'Brand-index → <a href="{HUB}/">mycnbox.eu</a>.\2',
        html,
        count=1,
        flags=re.S,
    )
    if HUB_UPLINK not in html and 'data-step4-hub="1"' not in html:
        html = html.replace("</header>", "</header>\n" + HUB_UPLINK, 1)
    if 'id="local"' not in html:
        # insert after verdict block if present, else after header
        if 'class="verd' in html:
            html = re.sub(
                r'(<div class="verd[\s\S]*?</div>\s*</div>)',
                r"\1\n" + LOCAL_LEGIT + "\n" + THICKEN_LEGIT,
                html,
                count=1,
            )
        else:
            html = html.replace("</header>", "</header>\n" + LOCAL_LEGIT + THICKEN_LEGIT, 1)
    # Soften spreadsheet CTA in verdict if any
    html = html.replace(
        "Open the MyCNBox Spreadsheet",
        "Open the MyCNBox hub Independent Index",
    )
    html = re.sub(
        r'href="/mycnbox-spreadsheet/"',
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
        "MyCNBox Nederland — NL-postcode &amp; Douane (spreadsheet → hub)",
        "MyCNBox Nederland — NL-postcode & Douane (spreadsheet → hub)",
    )
    html = _set_description(
        html,
        "mycnbox.nl is de NL-desk (1234 AB, Douane). Exact «mycnbox spreadsheet» → mycnbox.eu "
        "Independent Index 11,300+. 28 Oct 2026.",
    )
    html = re.sub(
        r"<h1>MyCNBox Spreadsheet<br><em>2026 Edition</em></h1>",
        "<h1>MyCNBox Nederland<br><em>geen tweede spreadsheet-hub</em></h1>",
        html,
        count=1,
    )
    html = re.sub(
        r'(<p class="hsub">).*?(</p>)',
        r"\1Brand spreadsheet / finds / dataset staan op "
        f'<a href="{HUB}/">mycnbox.eu</a> (Independent Index · 11,300+). '
        r"Dit desk dekt <strong>NL-postcode 1234 AB</strong>, Douane en lokale verzending.\2",
        html,
        count=1,
        flags=re.S,
    )
    if HUB_UPLINK not in html and 'data-step4-hub="1"' not in html:
        # after hero section closing
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
        "MyCNBox coupons Nederland — codes, Douane ≠ korting",
        "MyCNBox coupons Nederland — codes, Douane ≠ korting",
    )
    html = _set_description(
        html,
        "NL-desk coupons. Wereldwijde waarheidstabel → mycnbox.eu/mycnbox-coupons. "
        "Coupon ≠ Douane. Postcode 1234 AB. 28 Oct 2026.",
    )
    html = re.sub(
        r"<h1[^>]*>.*?</h1>",
        '<h1 style="font-size:clamp(24px,4vw,36px);font-weight:600;letter-spacing:-.8px;'
        'line-height:1.18;margin-bottom:12px">MyCNBox <span style="color:var(--acc)">'
        "coupons Nederland</span><br>codes · Douane ≠ korting</h1>",
        html,
        count=1,
        flags=re.S,
    )
    html = re.sub(
        r'(<p style="font-size:16px;color:var\(--g3\);line-height:1\.8;border-left:3px solid var\(--acc\);padding-left:16px">).*?(</p>)',
        r"\1NL-desk framing voor MyCNBox-codes. Canonieke werkende-lijst + Independent Index → "
        f'<a href="{HUB}/mycnbox-coupons/">mycnbox.eu/mycnbox-coupons</a>. '
        r"Een coupon verandert geen <strong>Douane</strong>-aangifte; verzending blijft "
        r'<a href="/mycnbox-shipping-guide/">1234 AB / Douane</a>.\2',
        html,
        count=1,
        flags=re.S,
    )
    if HUB_UPLINK not in html and 'data-step4-hub="1"' not in html:
        html = html.replace("</header>", "</header>\n" + HUB_UPLINK, 1)
    if 'id="local"' not in html:
        html = html.replace(
            HUB_UPLINK,
            HUB_UPLINK + "\n" + LOCAL_COUPON + "\n" + THICKEN_COUPON,
            1,
        )
    return html


PATCHERS = {
    "mycnbox-shipping-guide": deepen_shipping,
    "is-mycnbox-legit": deepen_legit,
    "mycnbox-spreadsheet": deepen_spreadsheet,
    "mycnbox-coupons": deepen_coupons,
}

REQUIRED = {
    "mycnbox-shipping-guide": (
        "Douane",
        "1234 AB",
        'id="local"',
        "mycnbox.eu",
        "finds-dataset",
        f'data-nl-deepen="{STAMP}"',
    ),
    "is-mycnbox-legit": (
        "Douane",
        "1234 AB",
        'id="local"',
        "mycnbox.eu",
        f'data-nl-deepen="{STAMP}"',
    ),
    "mycnbox-spreadsheet": (
        "Douane",
        "1234 AB",
        'id="local"',
        "mycnbox.eu",
        "11,300",
        "geen tweede spreadsheet-hub",
        f'data-nl-deepen="{STAMP}"',
    ),
    "mycnbox-coupons": (
        "Douane",
        "1234 AB",
        'id="local"',
        "mycnbox.eu",
        f'data-nl-deepen="{STAMP}"',
    ),
}

FORBIDDEN_H1 = (
    r"<h1[^>]*>\s*MyCNBox Spreadsheet\s*<br",
    r"<h1[^>]*>[^<]*Shipping Guide 2026",
    r"<h1[^>]*>[^<]*Coupon Codes 2026",
)


def _assert_ok(label: str, html: str) -> None:
    for tok in REQUIRED[label]:
        if tok not in html:
            raise SystemExit(f"{label} missing {tok!r}")
    for pat in FORBIDDEN_H1:
        if re.search(pat, html, re.I | re.S):
            raise SystemExit(f"{label} still has forbidden Spreadsheet/generic H1 ({pat})")
    for alien in (
        "Packstation",
        "1010 Wien",
        "Royal Mail",
        "HMRC",
        "00-001",
        "Colissimo",
        "CBSA",
        "A1A 1A1",
    ):
        # allow in "geen Duits Packstation" negation on NL pages
        if alien == "Packstation":
            continue
        if alien in html:
            raise SystemExit(f"{label} leaked sister fingerprint {alien!r}")
    # Must not claim hub reclaim content
    if "data-hub-reclaim" in html:
        raise SystemExit(f"{label} has hub-reclaim marker")


def build() -> dict[str, Path]:
    outs: dict[str, Path] = {}
    for slug in PAGES:
        src = OVERLAY / slug / "live-base.index.html"
        if not src.is_file():
            raise SystemExit(f"missing live-base {src}")
        html = PATCHERS[slug](src.read_text(encoding="utf-8", errors="replace"))
        _assert_ok(slug, html)
        out = OVERLAY / slug / "index.html.nl-deepen"
        out.write_text(html, encoding="utf-8")
        print("wrote", out, "bytes", out.stat().st_size)
        outs[slug] = out
    return outs


def deploy() -> str:
    outs = build()
    client = _connect()
    stamp = time.strftime("%Y%m%d-%H%M%S")
    bak = f"/www/backup/mycnbox-nl-deepen-{stamp}"
    # Refuse writing hub / watch / twin roots
    for forbidden in (
        "/www/wwwroot/mycnbox.eu/",
        "/www/wwwroot/mycnbox.es/",
        "/www/wwwroot/mycnbox.de/",
        "/www/wwwroot/mycnbox.fr/",
        "/www/wwwroot/mycnboxhaul.com/",
        "/www/wwwroot/mycnbox.co.uk/",
        "/www/wwwroot/mycnbox.pl/",
    ):
        # sanity: we never pass these paths below
        assert forbidden != REMOTE + "/"

    _run(client, f"mkdir -p '{bak}'")
    sftp = client.open_sftp()
    for slug, local in outs.items():
        remote = f"{REMOTE}/{slug}/index.html"
        raw = local.read_text(encoding="utf-8")
        if 'id="local"' not in raw or "Douane" not in raw:
            raise SystemExit(f"refusing PUT {remote}")
        if re.search(r"<h1[^>]*>\s*MyCNBox Spreadsheet\s*<br", raw, re.I | re.S):
            raise SystemExit(f"refusing Spreadsheet hero PUT {remote}")
        _run(client, f"mkdir -p '{REMOTE}/{slug}'")
        _run(client, f"cp -a '{remote}' '{bak}/{slug}-index.html.before' 2>/dev/null || true")
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
            f"https://{HOST}/mycnbox-shipping-guide/",
            f"https://{HOST}/is-mycnbox-legit/",
            f"https://{HOST}/mycnbox-spreadsheet/",
            f"https://{HOST}/mycnbox-coupons/",
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

    # Confirm we did not write hub
    check = _run(
        client,
        "grep -l 'data-nl-deepen=\"20261028\"' "
        f"{REMOTE}/mycnbox-shipping-guide/index.html "
        f"{REMOTE}/is-mycnbox-legit/index.html "
        f"{REMOTE}/mycnbox-spreadsheet/index.html "
        f"{REMOTE}/mycnbox-coupons/index.html; "
        "grep -l 'data-nl-deepen' /www/wwwroot/mycnbox.eu/index.html 2>/dev/null || echo hub_clean; "
        f"ls '{bak}'",
    )
    print(check)
    print("backup", bak)
    client.close()
    return bak


def verify_live() -> dict:
    import urllib.request

    checks = []
    urls = [
        f"https://{HOST}/mycnbox-shipping-guide/",
        f"https://{HOST}/is-mycnbox-legit/",
        f"https://{HOST}/mycnbox-spreadsheet/",
        f"https://{HOST}/mycnbox-coupons/",
        f"https://{HOST}/",
        "https://mycnbox.eu/",
        "https://mycnboxhaul.com/",
        "https://mycnbox.es/",
    ]
    for url in urls:
        req = urllib.request.Request(url, method="GET", headers={"User-Agent": "mycnbox-nl-deepen/1"})
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                body = resp.read().decode("utf-8", "replace")
                code = resp.status
                final = resp.geturl()
        except Exception as exc:  # noqa: BLE001
            # http.client for redirects without follow
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
            "hub_uplink": "mycnbox.eu" in body and ("hub-uplink" in body or "finds-dataset" in body),
            "postcode_1234ab": body.count("1234 AB"),
            "douane": body.lower().count("douane"),
            "data_nl_deepen": f'data-nl-deepen="{STAMP}"' in body,
            "spreadsheet_h1": bool(
                re.search(r"<h1[^>]*>\s*MyCNBox Spreadsheet", body, re.I | re.S)
            ),
        }
        if url.rstrip("/").endswith("mycnbox.nl") or url.rstrip("/").endswith("mycnbox.eu"):
            if "nl-deepen" not in url and HOST not in url.split("/")[2] if False else False:
                pass
        if url in (f"https://{HOST}/", "https://mycnbox.eu/"):
            entry["untouched_no_nl_deepen"] = f'data-nl-deepen="{STAMP}"' not in body
        checks.append(entry)

    # redirect checks without follow
    twins = []
    for url, expect_loc in (
        ("https://mycnboxhaul.com/", "https://mycnbox.eu/"),
        ("https://mycnbox.nl/mycnbox-shipping/", "https://mycnbox.nl/mycnbox-shipping-guide/"),
    ):
        import http.client
        from urllib.parse import urlparse

        u = urlparse(url)
        conn = http.client.HTTPSConnection(u.netloc, timeout=20)
        conn.request("HEAD", u.path or "/", headers={"User-Agent": "mycnbox-nl-deepen/1"})
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
    if args.submit_gsc:
        sa = (
            Path(args.submit_gsc)
            if isinstance(args.submit_gsc, Path) or args.submit_gsc is not True
            else Path("/cursor/stores/self/internal/gsc-sa.json")
        )
        if args.submit_gsc is True:
            sa = Path("/cursor/stores/self/internal/gsc-sa.json")
        out = submit_gsc(Path(sa))
        print(json.dumps({"site": out["site"], "feed": out["feed"], "submitted_at": out["submitted_at"]}, indent=2))
        # full list to stdout path via caller


if __name__ == "__main__":
    main()
