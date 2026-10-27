#!/usr/bin/env python3
"""Deepen sugargoospreadsheet.au keep desk: AU/GST local intent + hub uplink.

LIVE only on sugargoospreadsheet.au. Does NOT revive Phase C twins
(us/uk/es/fr/de/nl/at/ca). Does NOT touch sugargoo.ca/.es/.pt/.cheap.
Does NOT reclaim hub (separate worker).

Requires ORIGIN_SSH_PASS (or --load-env internal/usfans-ssh.env).
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
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
OVERLAY = ROOT / "sites" / "sugargoospreadsheet.au" / "overlay"
HOST = "sugargoospreadsheet.au"
REMOTE = f"/www/wwwroot/{HOST}"
STAMP = "20261027"
HUB = "https://sugargoospreadsheetnow.com"
TODAY = "2026-10-27"

STYLE = (
    f'<style id="au-deepen-{STAMP}">'
    ".hub-uplink{margin:14px 0 0;padding:12px 14px;"
    "border-left:3px solid #ff7103;background:#fff5eb;color:#3f2a14;line-height:1.65;"
    "font-size:15px;max-width:760px}.hub-uplink a{color:#cc5a02;font-weight:600}"
    "#local{scroll-margin-top:96px}.local-box{margin:1.25em 0;padding:14px 16px;"
    "border:1px solid #e2e8f0;border-radius:10px;background:#f8fafc}"
    ".local-box ol{margin:8px 0 0;padding-left:1.2em}.local-box li{margin:0 0 8px}"
    "</style>"
)

HUB_UPLINK = (
    f'<p class="hub-uplink" data-au-deepen="{STAMP}" data-step4-hub="1">'
    "Brand Spreadsheet / Coupons / finds → "
    f'<a href="{HUB}/">sugargoospreadsheetnow.com</a> · '
    f'<a href="{HUB}/sugargoo-coupon-2026.html">coupons 2026</a> · '
    f'<a href="{HUB}/best-sugargoo-spreadsheet-2026.html">best spreadsheet 2026</a>. '
    "This .au desk = GST / ABF / four-digit AU postcode / Australia Post — not a second spreadsheet hero."
    "</p>"
)

LOCAL_GST = f"""
<section id="local" class="local-box" data-au-fingerprint="gst-abf-ato-postcode" data-au-deepen="{STAMP}">
<h2>AU fingerprint before you ship</h2>
<ol>
<li><strong>Estimator destination: Australia</strong> — pick AU / 澳大利亚, not US and not “global”.</li>
<li><strong>Address</strong> — Australian <strong>four-digit postcode</strong> (e.g. <code>2000</code> Sydney). A UK/US postcode is the wrong country.</li>
<li><strong>GST / ABF / ATO</strong> — who collects GST depends on customs value and whether a GST-registered seller/marketplace/redeliverer charged it. Source the morning you ship: <a href="https://www.abf.gov.au/" rel="noopener" target="_blank">ABF</a> · <a href="https://www.ato.gov.au/" rel="noopener" target="_blank">ATO</a> (LVIG / imported goods).</li>
<li><strong>Last mile</strong> — often <strong>Australia Post</strong> after the international partner; this desk does not invent transit days.</li>
</ol>
<p>Brand spreadsheet / coupons stay on the hub <a href="{HUB}/">sugargoospreadsheetnow.com</a>. Money on this host: <a href="/gst-import-australia/">GST / ABF</a> · <a href="/sugargoo-shipping-australia/">Shipping AU</a>.</p>
</section>
"""

THICKEN_GST = f"""
<h2 id="ato-lvig-postcode">ATO LVIG, four-digit postcode, Australia Post</h2>
<p>This page is the <strong>Australia GST / import</strong> landing — not a SugarGoo Spreadsheet hero. For low-value imported goods (LVIG), a GST-registered overseas seller, marketplace or redeliverer may already collect the 10% GST at checkout when customs value is A$1,000 or less. Above that threshold, expect ABF border processing where GST, any duty and processing charges can apply. Re-read <strong>ATO</strong> and <strong>ABF</strong> the morning you submit the parcel; Discord screenshots are not a filing.</p>
<p>Use an Australian street + <strong>four-digit postcode</strong> in the warehouse address book. After QC, compare volumetric weight on AU-bound SKUs. Last-mile is often <strong>Australia Post</strong>: an international tracking number can sit quiet until a local scan appears — keep invoices and the in-app parcel ID ready if ABF or the carrier asks for evidence.</p>
<p>Brand Spreadsheet / coupons / “best spreadsheet 2026” → hub <a href="{HUB}/">sugargoospreadsheetnow.com</a>. This URL stays GST · ABF · AU postcode.</p>
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


def _fetch(url: str) -> str:
    req = Request(url, headers={"User-Agent": "sugargoo-au-deepen/1.0"})
    with urlopen(req, timeout=45) as resp:
        return resp.read().decode(errors="replace")


def _inject_head_style(html: str) -> str:
    if f'id="au-deepen-{STAMP}"' in html:
        return html
    return html.replace("</head>", STYLE + "\n</head>", 1)


def deepen_home(html: str) -> str:
    """Overlay homepage already has AU framing; add hub uplink + money nav + stamp."""
    html = _inject_head_style(html)
    # Badge / lab date
    html = html.replace(
        '<div class="hbg">Lab 30 Sep 2026</div>',
        f'<div class="hbg" data-au-deepen="{STAMP}">AU desk · GST / ABF · updated {TODAY}</div>',
        1,
    )
    html = html.replace(
        '<p class="eu-badge">Australia · AUD · GST</p>',
        f'<p class="eu-badge" data-au-deepen="{STAMP}">Australia · AUD · GST / ABF · four-digit postcode</p>',
        1,
    )
    # Nav: local money first; brand spreadsheet → hub
    html = re.sub(
        r'<nav class="nav" id="site-nav">.*?</nav>',
        (
            '<nav class="nav" id="site-nav">'
            '<a href="/" class="active">Home</a>'
            '<a href="/gst-import-australia/">GST / ABF</a>'
            '<a href="/sugargoo-shipping-australia/">Shipping AU</a>'
            f'<a href="{HUB}/sugargoo-coupon-2026.html">Coupons (hub)</a>'
            '<a href="/#local">AU checks</a>'
            '<a href="/help/">Help</a>'
            "</nav>"
        ),
        html,
        count=1,
        flags=re.S,
    )
    # Topbar: spreadsheet → hub
    html = html.replace(
        '<div class="topbar"><div class="container">Independent desk · Australia · AUD · GST · '
        '<a href="https://w2clinks.com/spreadsheet/sugargoo/?utm_source=sugargoospreadsheet_au'
        '&utm_medium=desk&utm_campaign=sugargoo" target="_blank" rel="noopener">Full spreadsheet →</a></div></div>',
        '<div class="topbar"><div class="container">Independent AU desk · GST / ABF · '
        f'Brand spreadsheet → <a href="{HUB}/" rel="noopener">sugargoospreadsheetnow.com</a></div></div>',
        1,
    )
    # Strengthen #local fingerprint + hub uplink after local section
    if f'data-au-deepen="{STAMP}"' not in html or "data-step4-hub" not in html:
        old_local_tail = (
            '<p class="local-src">Already on this host (kept): '
            '<a href="/gst-import-australia/">GST / ABF — educational</a> · '
            '<a href="/sugargoo-spreadsheet/">Spreadsheet guide</a> · '
            '<a href="/sugargoo-coupons/">Coupons</a> · '
            '<a href="/sugargoo-review/">Review</a></p>\n</section>'
        )
        new_local_tail = (
            '<p class="local-src">Already on this host (kept): '
            '<a href="/gst-import-australia/">GST / ABF — educational</a> · '
            '<a href="/sugargoo-shipping-australia/">Shipping AU</a> · '
            '<a href="/sugargoo-review/">Review</a></p>\n'
            f"{HUB_UPLINK}\n"
            "</section>"
        )
        if old_local_tail in html:
            html = html.replace(old_local_tail, new_local_tail, 1)
        elif "data-step4-hub" not in html:
            html = html.replace(
                '</section>\n<section class="sg-sec" id="agent">',
                f"{HUB_UPLINK}\n</section>\n<section class=\"sg-sec\" id=\"agent\">",
                1,
            )
    # Enrich local steps with Australia Post / ATO / example postcode
    html = html.replace(
        "<li><strong>Address</strong><span>Australian four-digit postcode. This desk does not invent Australia-Post transit days.</span></li>",
        "<li><strong>Address</strong><span>Australian <strong>four-digit postcode</strong> (e.g. <code>2000</code> Sydney). This desk does not invent Australia Post transit days.</span></li>",
        1,
    )
    html = html.replace(
        "<li><strong>GST / ABF</strong><span>The SKU decides. Collect can add a last-mile fee. Source: ABF the morning you ship. The ranked GST article on this host stays — we do not copy a GST rate into this title.</span></li>",
        "<li><strong>GST / ABF / ATO</strong><span>The SKU decides. Collect can add a last-mile fee. Source: <strong>ABF</strong> + <strong>ATO</strong> (LVIG / imported goods) the morning you ship. The ranked GST article on this host stays — we do not copy a GST rate into this title.</span></li>",
        1,
    )
    html = html.replace(
        "<li><strong>Last mile</strong><span>Read the live SKU. Catalogue prices here show AUD as display conversion, not checkout.</span></li>",
        "<li><strong>Last mile / Australia Post</strong><span>Often Australia Post after the international partner. Read the live SKU. Catalogue prices here show AUD as display conversion, not checkout.</span></li>",
        1,
    )
    # Mark #local section
    html = html.replace(
        '<section class="sg-sec" id="local">',
        f'<section class="sg-sec" id="local" data-au-fingerprint="gst-abf-postcode" data-au-deepen="{STAMP}">',
        1,
    )
    # Kept money cards: push spreadsheet to hub wording
    html = html.replace(
        '<a href="/sugargoo-spreadsheet/"><strong>Spreadsheet guide</strong><span> kept · not overwritten</span></a>',
        f'<a href="{HUB}/best-sugargoo-spreadsheet-2026.html"><strong>Spreadsheet (hub)</strong><span> brand table → now.com</span></a>',
        1,
    )
    html = html.replace(
        '<a href="/sugargoo-coupons/"><strong>Coupons</strong><span> kept · not overwritten</span></a>',
        f'<a href="{HUB}/sugargoo-coupon-2026.html"><strong>Coupons (hub)</strong><span> brand coupons → now.com</span></a>',
        1,
    )
    # Footer: sunset twins narrative + soften spreadsheet money links
    html = html.replace(
        "<p>Independent information desk on sugargoospreadsheet.au. Not the official SugarGoo site. Sister country hosts stay separate files — no 301.</p>",
        f"<p>Independent AU desk on sugargoospreadsheet.au (GST / ABF). Brand spreadsheet → <a href=\"{HUB}/\">sugargoospreadsheetnow.com</a>. Phase C twins 301→hub — not revived.</p>",
        1,
    )
    html = html.replace(
        "Sister country hosts stay separate files — no 301. Copy reviewed 30 Sep 2026.",
        f"Twins us/uk/es/fr/de/nl/at/ca → hub (not revived). Copy reviewed {TODAY}.",
        1,
    )
    html = html.replace(
        '<li><a href="/gst-import-australia/">GST / ABF — educational</a></li>'
        '<li><a href="/sugargoo-spreadsheet/">Spreadsheet guide</a></li>'
        '<li><a href="/sugargoo-coupons/">Coupons</a></li>'
        '<li><a href="/sugargoo-review/">Review</a></li>',
        '<li><a href="/gst-import-australia/">GST / ABF — educational</a></li>'
        '<li><a href="/sugargoo-shipping-australia/">Shipping AU</a></li>'
        f'<li><a href="{HUB}/">Hub spreadsheet</a></li>'
        f'<li><a href="{HUB}/sugargoo-coupon-2026.html">Hub coupons</a></li>'
        '<li><a href="/sugargoo-review/">Review</a></li>',
        1,
    )
    # Footer locale cluster: only hub + AU (no twin resurrection links as peers)
    html = re.sub(
        r'<p class="footer-locale-cluster"[^>]*>.*?</p>',
        (
            '<p class="footer-locale-cluster" style="margin:12px 0;font-size:13px;color:#94A3B8">'
            "Active: "
            f'<a href="{HUB}/">Global hub</a> · '
            '<a href="https://sugargoospreadsheet.au/">Australia desk</a>'
            " · other country hosts 301→hub (Phase C sunset)</p>"
        ),
        html,
        count=1,
        flags=re.S,
    )
    # meta description bump
    html = re.sub(
        r'<meta name="description" content="[^"]*"',
        '<meta name="description" content="AU keep desk for SugarGoo: GST / ABF / ATO LVIG, four-digit Australian postcode, Australia Post last-mile. Brand spreadsheet → sugargoospreadsheetnow.com."',
        html,
        count=1,
    )
    html = re.sub(
        r'property="og:description" content="[^"]*"',
        'property="og:description" content="AU keep desk: GST / ABF / four-digit postcode. Brand spreadsheet on sugargoospreadsheetnow.com."',
        html,
        count=1,
    )
    return html


def deepen_gst(html: str) -> str:
    html = _inject_head_style(html)
    # Soften brand chip
    html = html.replace("<span>Spreadsheet</span>", "<span>Australia</span>", 1)
    # Title stays GST-focused; tighten
    html = re.sub(
        r"<title>.*?</title>",
        "<title>Sugargoo Australia GST &amp; Import Duty — ABF, ATO, Australia Post</title>",
        html,
        count=1,
        flags=re.S,
    )
    html = re.sub(
        r'<meta name="description" content="[^"]*"',
        '<meta name="description" content="SugarGoo parcels to Australia: GST / ABF / ATO LVIG, A$1,000 customs-value notes, four-digit AU postcode, Australia Post last-mile. Brand spreadsheet → sugargoospreadsheetnow.com."',
        html,
        count=1,
    )
    # Nav: local money
    html = re.sub(
        r'<nav class="nav" aria-label="Main menu">.*?</nav>',
        (
            '<nav class="nav" aria-label="Main menu">'
            '<a href="/">Home</a>'
            '<a href="/gst-import-australia/" aria-current="page">GST / ABF</a>'
            '<a href="/sugargoo-shipping-australia/">Shipping AU</a>'
            '<a href="#local">AU checks</a>'
            f'<a href="{HUB}/">Hub</a>'
            '<a href="/help/">Help</a>'
            "</nav>"
        ),
        html,
        count=1,
        flags=re.S,
    )
    # Inject hub uplink + #local after quick-answer block
    if f'data-au-deepen="{STAMP}"' not in html:
        anchor = (
            "removes GST.</p>\n"
            if "removes GST.</p>" in html
            else None
        )
        # Live page ends first paragraphs then h2 — insert after the "not tax advice" para
        needle = (
            "This is general planning information, not tax or customs advice. Check the\n"
            "transaction record and official guidance rather than assuming that a declared value\n"
            "removes GST.</p>\n"
        )
        if needle in html:
            html = html.replace(
                needle,
                needle + f"{HUB_UPLINK}\n{LOCAL_GST}\n",
                1,
            )
        else:
            # fallback: after h1 block
            html = html.replace(
                "<h1>GST &amp; Import Duty on Sugargoo Parcels to Australia</h1>\n",
                "<h1>GST &amp; Import Duty on Sugargoo Parcels to Australia</h1>\n"
                f"{HUB_UPLINK}\n{LOCAL_GST}\n",
                1,
            )
            del anchor  # unused quiet
    if 'id="ato-lvig-postcode"' not in html:
        html = html.replace(
            "<h2>5. Official Australian sources</h2>",
            THICKEN_GST + "\n<h2>5. Official Australian sources</h2>",
            1,
        )
    # Editor notes: local intent + hub uplink (no spreadsheet guide framing)
    html = re.sub(
        r'<section id="gsc-editor-notes".*?</section>',
        (
            '<section id="gsc-editor-notes" style="max-width:720px;margin:2rem auto;padding:1.25rem;'
            'border-top:1px solid #e2e8f0;line-height:1.65;color:#334155">'
            '<h2 style="font-size:1.1rem;margin:0 0 .5rem">Australia editor notes (en-AU)</h2>'
            '<p style="margin:0 0 .75rem">AU keep desk for GST / ABF / ATO LVIG and Australia Post last-mile. '
            f'Brand Spreadsheet / coupons → <a href="{HUB}/">sugargoospreadsheetnow.com</a>. '
            f"Updated {TODAY}.</p>"
            '<p style="margin:0">Related: <a href="/gst-import-australia/">GST import</a>, '
            '<a href="/sugargoo-shipping-australia/">Shipping AU</a>, '
            '<a href="/au-buyer-guides/">AU buyer guides</a>, '
            f'<a href="{HUB}/sugargoo-coupon-2026.html">Hub coupons</a>, '
            f'<a href="{HUB}/best-sugargoo-spreadsheet-2026.html">Hub spreadsheet</a>.</p>'
            "</section>"
        ),
        html,
        count=1,
        flags=re.S,
    )
    # Footer soften
    html = html.replace("<h3>SugarGoo Spreadsheet</h3>", "<h3>SugarGoo Australia desk</h3>", 1)
    html = html.replace(
        "Independent English-language guide to SugarGoo and to how you use the w2clinks catalogue to buy in China from Australia.",
        "Independent AU desk: GST / ABF / four-digit postcode. Brand spreadsheet → sugargoospreadsheetnow.com.",
        1,
    )
    html = html.replace(
        "<strong>Independence notice.</strong> SugarGoo Spreadsheet is an independent information site.",
        "<strong>Independence notice.</strong> sugargoospreadsheet.au is an independent AU information desk (GST / ABF).",
        1,
    )
    html = html.replace(
        "&copy; 2026 SugarGoo Spreadsheet.",
        "&copy; 2026 sugargoospreadsheet.au Australia desk.",
        1,
    )
    # Body marker
    if "data-inner-chrome" in html and f"data-au-deepen" not in html[:800]:
        html = html.replace(
            'data-inner-chrome="20261006x-sugargoo-au"',
            f'data-inner-chrome="20261006x-sugargoo-au" data-au-deepen="{STAMP}"',
            1,
        )
    return html


def build(live_gst: str | None = None, overlay_home: str | None = None) -> dict[str, Path]:
    home_src = overlay_home or (OVERLAY / "index.html").read_text(encoding="utf-8")
    # Prefer saved live-base if present for GST
    gst_live_path = OVERLAY / "gst-import-australia" / "live-base.index.html"
    if live_gst is None:
        if gst_live_path.exists():
            live_gst = gst_live_path.read_text(encoding="utf-8")
        else:
            live_gst = _fetch(f"https://{HOST}/gst-import-australia/")

    # Save live baselines
    gst_dir = OVERLAY / "gst-import-australia"
    gst_dir.mkdir(parents=True, exist_ok=True)
    gst_live_path.write_text(live_gst, encoding="utf-8")
    live_home = OVERLAY / "live-base.index.html"
    if not live_home.exists() or live_home.stat().st_size < 1000:
        live_home.write_text(_fetch(f"https://{HOST}/"), encoding="utf-8")

    home = deepen_home(home_src)
    gst = deepen_gst(live_gst)

    # Guardrails
    for label, html in (("home", home), ("gst", gst)):
        if 'id="local"' not in html:
            raise SystemExit(f"{label}: missing #local")
        if HUB not in html:
            raise SystemExit(f"{label}: missing hub uplink")
        if f'data-au-deepen="{STAMP}"' not in html:
            raise SystemExit(f"{label}: missing data-au-deepen")
        if re.search(r"<h1>[^<]*Spreadsheet", html, re.I):
            raise SystemExit(f"{label}: H1 still Spreadsheet hero")
        title_m = re.search(r"<title>(.*?)</title>", html, re.S | re.I)
        if title_m and re.search(r"Spreadsheet", title_m.group(1), re.I):
            raise SystemExit(f"{label}: <title> still Spreadsheet hero")
        for tok in ("GST", "ABF", "Australia Post", "four-digit"):
            if tok not in html:
                raise SystemExit(f"{label}: missing fingerprint {tok}")

    home_out = OVERLAY / "index.html.au-deepen"
    gst_out = gst_dir / "index.html.au-deepen"
    home_out.write_text(home, encoding="utf-8")
    gst_out.write_text(gst, encoding="utf-8")
    # Keep overlay/index.html in sync for repo source of truth
    (OVERLAY / "index.html").write_text(home, encoding="utf-8")
    print("BUILT", home_out, home_out.stat().st_size)
    print("BUILT", gst_out, gst_out.stat().st_size)
    return {"home": home_out, "gst": gst_out}


def deploy(built: dict[str, Path], store_internal: Path | None) -> dict:
    client = _connect()
    bak = f"/www/backup/sugargoo-au-deepen-{datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%S')}"
    cmds = [
        f"mkdir -p '{bak}'",
        f"cp -a '{REMOTE}/index.html' '{bak}/index.html.before' 2>/dev/null || true",
        f"cp -a '{REMOTE}/gst-import-australia/index.html' '{bak}/gst-import-australia-index.html.before' 2>/dev/null || true",
        f"cp -a '{REMOTE}/sitemap.xml' '{bak}/sitemap.xml.before' 2>/dev/null || true",
    ]
    print(_run(client, " && ".join(cmds)))

    sftp = client.open_sftp()
    mapping = {
        built["home"]: f"{REMOTE}/index.html",
        built["gst"]: f"{REMOTE}/gst-import-australia/index.html",
    }
    for local, remote in mapping.items():
        sftp.put(str(local), remote)
        print("PUT", remote)

    # bump sitemap lastmod
    try:
        with sftp.open(f"{REMOTE}/sitemap.xml", "r") as fh:
            sm = fh.read().decode(errors="replace")
        for loc in (f"https://{HOST}/", f"https://{HOST}/gst-import-australia/"):
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
        tmp = f"/tmp/sugargoo-au-sitemap-{STAMP}.xml"
        Path(tmp).write_text(sm, encoding="utf-8")
        sftp.put(tmp, f"{REMOTE}/sitemap.xml")
        print("PUT sitemap.xml lastmod", TODAY)
    except Exception as exc:  # noqa: BLE001
        print("SITEMAP_WARN", exc)
    sftp.close()

    _run(
        client,
        " && ".join(
            [
                f"chown www:www '{REMOTE}/index.html'",
                f"chown www:www '{REMOTE}/gst-import-australia/index.html'",
                f"chown www:www '{REMOTE}/sitemap.xml'",
            ]
        ),
    )
    print("BACKUP", bak)
    meta = {"backup": bak, "stamp": STAMP, "pages": ["/", "/gst-import-australia/"]}
    if store_internal:
        store_internal.mkdir(parents=True, exist_ok=True)
        (store_internal / "backup.txt").write_text(bak + "\n", encoding="utf-8")
    client.close()
    return meta


def verify() -> dict:
    pages = []
    for path in ("/", "/gst-import-australia/"):
        url = f"https://{HOST}{path}"
        req = Request(url, headers={"User-Agent": "sugargoo-au-deepen/1.0"})
        with urlopen(req, timeout=30) as resp:
            body = resp.read().decode(errors="replace")
            code = resp.status
        title_m = re.search(r"<title>(.*?)</title>", body, re.S | re.I)
        pages.append(
            {
                "url": url,
                "http": code,
                "id_local": 'id="local"' in body,
                "hub_uplink": HUB in body and "data-step4-hub" in body,
                "gst": body.count("GST"),
                "abf": body.count("ABF"),
                "australia_post": body.lower().count("australia post"),
                "four_digit": "four-digit" in body,
                "data_au_deepen": f'data-au-deepen="{STAMP}"' in body,
                "spreadsheet_h1": bool(re.search(r"<h1>[^<]*Spreadsheet", body, re.I)),
                "title": re.sub(r"\s+", " ", title_m.group(1)).strip() if title_m else None,
            }
        )

    twins = [
        "sugargoospreadsheets.us",
        "sugargoospreadsheets.uk",
        "sugargoospreadsheet.es",
        "sugargoospreadsheets.fr",
        "sugargoospreadsheets.de",
        "sugargoospreadsheets.nl",
        "sugargoo.at",
        "sugargoospreadsheets2026.ca",
    ]
    twin_rows = []
    for host in twins:
        conn = http.client.HTTPSConnection(host, timeout=20)
        conn.request("GET", "/", headers={"User-Agent": "sugargoo-au-deepen/1.0"})
        r = conn.getresponse()
        twin_rows.append(
            {"host": host, "http": r.status, "location": r.getheader("Location")}
        )
        conn.close()

    # External domains must remain untouched (spot-check reachable only)
    external = []
    for host in ("sugargoo.ca", "sugargoo.es"):
        try:
            conn = http.client.HTTPSConnection(host, timeout=15)
            conn.request("HEAD", "/", headers={"User-Agent": "sugargoo-au-deepen/1.0"})
            r = conn.getresponse()
            external.append({"host": host, "http": r.status, "note": "not touched"})
            conn.close()
        except Exception as exc:  # noqa: BLE001
            external.append({"host": host, "error": str(exc)[:120], "note": "not touched"})

    return {
        "at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "pages": pages,
        "twins": twin_rows,
        "external_untouched": external,
    }


def gsc_submit(sa: Path, out_path: Path) -> dict:
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
    out_path.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print("GSC_SUBMIT", site, feed)
    return result


def write_deploy_md() -> None:
    path = OVERLAY / "DEPLOY-AU-DEEPEN.md"
    path.write_text(
        f"""# Deploy AU deepen ({STAMP})

```bash
python3 tools/sugargoo_au_deepen.py \\
  --load-env /cursor/stores/self/internal/usfans-ssh.env \\
  --deploy --verify --gsc \\
  --store-internal /cursor/stores/self/internal/sugargoo-au-deepen \\
  --gsc-sa /cursor/stores/self/internal/gsc-sa.json
```

Puts only:
- `/www/wwwroot/{HOST}/index.html`
- `/www/wwwroot/{HOST}/gst-import-australia/index.html`
- sitemap lastmod bump

Does **not** write twin wwwroots or external sugargoo.ca/.es/.pt/.cheap.
""",
        encoding="utf-8",
    )


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--load-env", type=Path)
    ap.add_argument("--build-only", action="store_true")
    ap.add_argument("--deploy", action="store_true")
    ap.add_argument("--verify", action="store_true")
    ap.add_argument("--gsc", action="store_true")
    ap.add_argument("--store-internal", type=Path, default=None)
    ap.add_argument("--gsc-sa", type=Path, default=None)
    ap.add_argument(
        "--live-gst",
        type=Path,
        default=None,
        help="Optional path to saved LIVE GST HTML",
    )
    args = ap.parse_args()
    if args.load_env:
        _load_env(args.load_env)

    live_gst = args.live_gst.read_text(encoding="utf-8") if args.live_gst else None
    # If overlay index already deepened, rebuild from pre-deepen if available
    home_src_path = OVERLAY / "index.html"
    pre = OVERLAY / "index.html.pre-deepen"
    if "data-au-deepen" in home_src_path.read_text(encoding="utf-8") and pre.exists():
        overlay_home = pre.read_text(encoding="utf-8")
    else:
        if "data-au-deepen" not in home_src_path.read_text(encoding="utf-8"):
            pre.write_text(home_src_path.read_text(encoding="utf-8"), encoding="utf-8")
        overlay_home = None

    built = build(live_gst=live_gst, overlay_home=overlay_home)
    write_deploy_md()

    if args.build_only and not args.deploy:
        return

    meta: dict = {}
    if args.deploy:
        meta = deploy(built, args.store_internal)
    if args.verify or args.deploy:
        time.sleep(3)
        ver = verify()
        ver["backup"] = meta.get("backup")
        if args.store_internal:
            args.store_internal.mkdir(parents=True, exist_ok=True)
            (args.store_internal / "live_verify.json").write_text(
                json.dumps(ver, indent=2) + "\n", encoding="utf-8"
            )
        print(json.dumps(ver, indent=2))
        bad = [
            p
            for p in ver["pages"]
            if p["http"] != 200
            or not p["id_local"]
            or not p["hub_uplink"]
            or p["spreadsheet_h1"]
            or not p["data_au_deepen"]
        ]
        twin_bad = [
            t
            for t in ver["twins"]
            if t["http"] not in (301, 302)
            or not (t.get("location") or "").startswith(HUB)
        ]
        if bad or twin_bad:
            raise SystemExit(f"VERIFY_FAIL pages={bad} twins={twin_bad}")
    if args.gsc:
        sa = args.gsc_sa or Path("/cursor/stores/self/internal/gsc-sa.json")
        out = (args.store_internal or Path("/tmp")) / "gsc_sitemap_submit.json"
        if args.store_internal:
            args.store_internal.mkdir(parents=True, exist_ok=True)
        gsc_submit(sa, out)


if __name__ == "__main__":
    main()
