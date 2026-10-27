#!/usr/bin/env python3
"""LitBuy CA watch light fix (strategy action 3): remove Spreadsheet hero,
align ship-to-Canada SERP (Canada Post / CBSA / A1A 1A1).

WATCH only — do NOT promote to keep. Do NOT revive twins (now/es/us/uk/nl/fr).
Do NOT touch hub .eu or keep AT / watch IT.
"""
from __future__ import annotations

import json
import os
import re
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "sites" / "litbuyspreadsheets.ca"
OVERLAY = SITE / "overlay"
STAMP = "20261027"
MARKER = f'data-ca-light-fix="{STAMP}"'
HOST = "litbuyspreadsheets.ca"
HUB = "https://litbuyspreadsheet.eu/"

LOCAL_HOME = f"""
<section class="sg-sec" id="local" data-platform-opt="litbuy-platform-20261026" data-ca-light-fix="{STAMP}" data-watch="1">
  <h2>Does LitBuy ship to Canada? — Canada Post, CBSA, form A1A 1A1</h2>
  <p class="ssub">litbuyspreadsheets.ca · <strong>watch</strong> desk (not keep, not a second hub) · CAD / Canada Post / CBSA stay here.</p>
  <ol class="local-steps" style="margin:12px 0 0;padding:0;list-style:none;display:grid;gap:12px">
    <li style="border:1px solid #e5e7eb;border-radius:12px;padding:14px 16px;background:#fff"><strong style="display:block;margin:0 0 6px">Yes — destination Canada (CA)</strong><span style="display:block;color:#334155;line-height:1.7">LitBuy international SKUs can target a Canadian delivery address. Pick <strong>Canada</strong> in the official estimator — a US ZIP is the wrong country.</span></li>
    <li style="border:1px solid #e5e7eb;border-radius:12px;padding:14px 16px;background:#fff"><strong style="display:block;margin:0 0 6px">Postal code form A1A 1A1</strong><span style="display:block;color:#334155;line-height:1.7">Use a Canadian postal code (ANA NAN). Do not paste a five-digit US ZIP into the warehouse address book.</span></li>
    <li style="border:1px solid #e5e7eb;border-radius:12px;padding:14px 16px;background:#fff"><strong style="display:block;margin:0 0 6px">CBSA + GST/HST</strong><span style="display:block;color:#334155;line-height:1.7">Who pays duties is on the booked SKU (prepaid vs collect). This desk does not invent a rate. Read <a href="https://www.cbsa-asfc.gc.ca/" rel="noopener">CBSA</a> the morning you ship.</span></li>
    <li style="border:1px solid #e5e7eb;border-radius:12px;padding:14px 16px;background:#fff"><strong style="display:block;margin:0 0 6px">Canada Post last-mile</strong><span style="display:block;color:#334155;line-height:1.7">Many lines hand off to <strong>Canada Post</strong> after CBSA. Tracking can pause at the customs handoff before a local scan.</span></li>
  </ol>
  <p class="hub-uplink" style="margin:14px 0 0;padding:12px 14px;border-left:3px solid #0f766e;background:#f0fdfa;color:#134e4a;line-height:1.6;font-size:15px;max-width:760px">Looking for the global LitBuy spreadsheet? Use <a href="{HUB}" style="color:#0f766e;font-weight:600">litbuyspreadsheet.eu</a> (Independent Index · 11,300+ · <a href="{HUB}finds-dataset/" style="color:#0f766e;font-weight:600">dataset</a> · <a href="{HUB}litbuy-coupons/" style="color:#0f766e;font-weight:600">coupons</a>). This host stays a Canada <strong>watch</strong> desk — not promoted to keep, not a twin 301 target.</p>
  <p class="local-src" style="font-size:14px;color:#334155;line-height:1.7;margin:14px 0 0">Money URLs (≤6): <a href="/litbuy-shipping-canada/">Shipping to Canada</a> · <a href="/cbsa-import-canada/">CBSA</a> · <a href="/canada-post-customs/">Canada Post customs</a> · <a href="/gst-hst-import-canada/">GST/HST</a> · hub <a href="{HUB}">.eu</a> · <a href="{HUB}litbuy-coupons/">coupons</a></p>
</section>
""".strip()

LOCAL_SHIP = f"""
<section id="local" data-ca-light-fix="{STAMP}" data-watch="1" style="margin:18px 0;padding:16px 18px;border:1px solid #e5e7eb;border-radius:12px;background:#fff">
  <h2 style="margin:0 0 8px;font-size:1.25rem">Does LitBuy ship to Canada?</h2>
  <p style="margin:0 0 10px;line-height:1.7;color:#334155"><strong>Yes.</strong> Book an international SKU with destination <strong>Canada</strong>. Shoppers searching <em>does litbuy ship to canada</em> need a Canada landing checklist — not a spreadsheet hero.</p>
  <ul style="margin:0;padding-left:1.2rem;line-height:1.75;color:#334155">
    <li><strong>Canada Post</strong> — typical last-mile after CBSA release; expect a quiet gap between export scan and the first Canada Post / broker event.</li>
    <li><strong>CBSA</strong> — screening and GST/HST follow the booked SKU. Coupons cut LitBuy fees; they do not erase import charges.</li>
    <li><strong>Postal code form A1A 1A1</strong> — Canadian addresses only. A US ZIP routes the estimator to the wrong country.</li>
  </ul>
  <p style="margin:12px 0 0;line-height:1.7;color:#334155">Brand spreadsheet / dataset / coupons → hub <a href="{HUB}">litbuyspreadsheet.eu</a>. This URL stays the Canada shipping watch page. Estimator: <a href="https://litbuy.com/shipping-estimate" rel="noopener">litbuy.com/shipping-estimate</a> with destination <strong>CA</strong>.</p>
</section>
""".strip()


def _sub_title(html: str, title: str) -> str:
    return re.sub(r"<title>.*?</title>", f"<title>{title}</title>", html, count=1, flags=re.S)


def patch_home(html: str) -> str:
    title = "LitBuy Canada — Does LitBuy ship to Canada? Canada Post, CBSA, A1A 1A1"
    html = _sub_title(html, title)
    html = re.sub(
        r'<meta name="description" content="[^"]*"',
        (
            '<meta name="description" content="Canada watch desk for LitBuy: does LitBuy ship to Canada, '
            'Canada Post last-mile, CBSA / GST-HST, postal code form A1A 1A1. Not a spreadsheet hub."'
        ),
        html,
        count=1,
    )
    html = re.sub(
        r'("name":\s*")LitBuy Spreadsheet[^"]*(")',
        rf'\1{title}\2',
        html,
        count=1,
    )
    # brand chip + nav money URLs
    html = html.replace("<span>Spreadsheet</span>", "<span>Canada</span>", 1)
    html = re.sub(
        r'<nav class="nav" aria-label="Main menu">.*?</nav>',
        (
            '<nav class="nav" aria-label="Main menu">'
            '<a href="/" aria-current="page">Home</a>'
            '<a href="/litbuy-shipping-canada/">Shipping</a>'
            '<a href="/cbsa-import-canada/">CBSA</a>'
            '<a href="/canada-post-customs/">Canada Post</a>'
            '<a href="/how-to-use-litbuy/">Guide</a>'
            '<a href="#local">Canada checks</a>'
            "</nav>"
        ),
        html,
        count=1,
        flags=re.S,
    )
    # hero — remove Spreadsheet
    html = re.sub(
        r'<span class="eyebrow">.*?</span>',
        '<span class="eyebrow">Canada watch desk · not a spreadsheet hub</span>',
        html,
        count=1,
        flags=re.S,
    )
    html = re.sub(
        r"<h1>.*?</h1>",
        "<h1>Does LitBuy ship to Canada? Canada Post, CBSA, form A1A 1A1</h1>",
        html,
        count=1,
        flags=re.S,
    )
    html = re.sub(
        r'<p class="lead">.*?</p>',
        (
            '<p class="lead">Independent Canada <strong>watch</strong> desk on litbuyspreadsheets.ca: '
            "plan shipping to Canada with <strong>Canada Post</strong> last-mile notes, "
            "<strong>CBSA</strong> / GST-HST context, and postal code <strong>form A1A 1A1</strong> — "
            "not a US ZIP and not a global LitBuy Spreadsheet hero. Brand spreadsheet stays on "
            f'<a href="{HUB}">litbuyspreadsheet.eu</a>.</p>'
        ),
        html,
        count=1,
        flags=re.S,
    )
    # replace existing #local (platform-opt stub) with shipping-aligned block
    if 'id="local"' in html:
        html = re.sub(
            r'<section class="sg-sec" id="local"[^>]*>[\s\S]*?</section>',
            LOCAL_HOME,
            html,
            count=1,
        )
    else:
        html = re.sub(
            r"(</section>\s*)(<section class=\"sec sec--first\" id=\"agent\">)",
            r"\1\n" + LOCAL_HOME + "\n\2",
            html,
            count=1,
        )
    # footer
    html = html.replace("<h3>LitBuy Spreadsheet</h3>", "<h3>LitBuy Canada watch desk</h3>", 1)
    html = re.sub(
        r"Independent English-language guide to LitBuy and to how you use the w2clinks catalogue to buy in China from Canada\.",
        "Canada watch assistant: Canada Post, CBSA, form A1A 1A1. Brand spreadsheet → litbuyspreadsheet.eu. Not promoted to keep.",
        html,
        count=1,
    )
    html = html.replace(
        "LitBuy Spreadsheet is an independent information site.",
        "This Canada watch desk is an independent information site.",
        1,
    )
    html = html.replace(
        "&copy; 2026 LitBuy Spreadsheet.",
        "&copy; 2026 LitBuy Canada watch desk (litbuyspreadsheets.ca).",
        1,
    )
    html = html.replace(
        'href="/litbuy-shipping/">Shipping and customs</a>',
        'href="/litbuy-shipping-canada/">Shipping to Canada</a>',
        1,
    )
    if MARKER not in html:
        html = html.replace("<html", f"<html {MARKER}", 1)
    return html


def patch_shipping(html: str) -> str:
    title = "Does LitBuy ship to Canada? — Canada Post, CBSA, A1A 1A1 (2026)"
    html = _sub_title(html, title)
    html = re.sub(
        r'<meta name="description" content="[^"]*"',
        (
            '<meta name="description" content="Does LitBuy ship to Canada? Yes — Canada Post last-mile, '
            'CBSA / GST-HST, postal code form A1A 1A1, delivery ETA after QC. litbuyspreadsheets.ca watch desk."'
        ),
        html,
        count=1,
    )
    html = html.replace(
        'content="Litbuy Spreadsheet Canada"',
        'content="LitBuy Canada watch desk"',
    )
    html = re.sub(
        r'<meta property="og:title" content="[^"]*"',
        f'<meta property="og:title" content="{title}"',
        html,
        count=1,
    )
    html = re.sub(
        r'<meta property="og:description" content="[^"]*"',
        (
            '<meta property="og:description" content="Does LitBuy ship to Canada? Canada Post, CBSA, '
            'form A1A 1A1, and delivery ETA planning after QC."'
        ),
        html,
        count=1,
    )
    # JSON-LD headline / org / FAQ add ship-to-Canada
    html = html.replace(
        '"headline": "Litbuy shipping times (Canada)"',
        '"headline": "Does LitBuy ship to Canada? Canada Post, CBSA, A1A 1A1"',
    )
    html = html.replace('"name": "Litbuy Spreadsheet Canada"', '"name": "LitBuy Canada watch desk"')
    html = html.replace(
        '"dateModified": "2026-05-31"',
        '"dateModified": "2026-10-27"',
    )
    if "Does LitBuy ship to Canada?" not in html.split("FAQPage", 1)[-1][:800]:
        html = html.replace(
            '{"@type": "Question", "name": "How long does Litbuy take to ship to Canada?"',
            (
                '{"@type": "Question", "name": "Does LitBuy ship to Canada?", '
                '"acceptedAnswer": {"@type": "Answer", "text": '
                '"Yes. Book an international SKU with destination Canada. Use postal code form A1A 1A1, '
                'budget CBSA / GST-HST, and expect Canada Post last-mile after release."}}, '
                '{"@type": "Question", "name": "How long does Litbuy take to ship to Canada?"'
            ),
            1,
        )
    # chrome
    html = html.replace("<span>Spreadsheet</span>", "<span>Canada</span>", 1)
    html = re.sub(
        r'<nav class="nav" aria-label="Main menu">.*?</nav>',
        (
            '<nav class="nav" aria-label="Main menu">'
            '<a href="/">Home</a>'
            '<a href="/litbuy-shipping-canada/" aria-current="page">Shipping</a>'
            '<a href="/cbsa-import-canada/">CBSA</a>'
            '<a href="/canada-post-customs/">Canada Post</a>'
            '<a href="/how-to-use-litbuy/">Guide</a>'
            '<a href="#local">Canada checks</a>'
            "</nav>"
        ),
        html,
        count=1,
        flags=re.S,
    )
    html = re.sub(
        r'<span class="eu-badge">.*?</span>',
        '<span class="eu-badge">Canada watch · Canada Post / CBSA · not a spreadsheet hub</span>',
        html,
        count=1,
        flags=re.S,
    )
    html = re.sub(
        r"<h1>.*?</h1>",
        "<h1>Does LitBuy ship to Canada? Canada Post, CBSA, form A1A 1A1</h1>",
        html,
        count=1,
        flags=re.S,
    )
    html = re.sub(
        r'<p class="intro">Canadian ETA planning after QC — economy vs express, CBSA peaks and Canada Post last mile\.</p>',
        (
            '<p class="intro"><strong>Yes — LitBuy ships to Canada.</strong> Plan economy vs express after QC, '
            "budget <strong>CBSA</strong> peaks, and expect <strong>Canada Post</strong> last-mile with postal "
            "code <strong>form A1A 1A1</strong> (not a US ZIP).</p>"
        ),
        html,
        count=1,
    )
    # open body with #local inside article content
    if 'id="local"' not in html:
        html = re.sub(
            r'(<article class="article-content article-long">\s*)',
            r"\1\n" + LOCAL_SHIP + "\n",
            html,
            count=1,
        )
        if 'id="local"' not in html:
            html = re.sub(
                r"(<h1>.*?</h1>)",
                r"\1\n" + LOCAL_SHIP,
                html,
                count=1,
                flags=re.S,
            )
    # first H2 framing
    html = html.replace(
        "<h2>Canada-exclusive shipping URL</h2>",
        "<h2>Canada watch desk — ship-to-Canada intent</h2>",
        1,
    )
    html = re.sub(
        r"<p><strong>litbuyspreadsheets\.ca</strong> answers shipping-time intent for CAD shoppers alongside "
        r'<a href="/litbuy-review/">is Litbuy legit</a> threads\. No mirror on \.eu or now\.com\.</p>',
        (
            "<p><strong>litbuyspreadsheets.ca</strong> answers <em>does litbuy ship to canada</em> and delivery-ETA "
            'intent for CAD shoppers alongside <a href="/litbuy-review/">is Litbuy legit</a>. Brand spreadsheet '
            f"stays on <a href=\"{HUB}\">litbuyspreadsheet.eu</a> — this watch desk does not revive now.com / "
            ".es / .us twins.</p>"
        ),
        html,
        count=1,
    )
    # FAQ visible (title/H1 already contain the phrase — key on summary tag)
    if "<summary>Does LitBuy ship to Canada?</summary>" not in html:
        html = html.replace(
            '<details class="faq-item"><summary>How long does Litbuy take to ship to Canada?</summary>',
            (
                '<details class="faq-item" open><summary>Does LitBuy ship to Canada?</summary>'
                "<div class=\"faq-answer\">Yes. Book destination <strong>Canada</strong> in the official estimator, "
                "use postal code <strong>form A1A 1A1</strong>, budget <strong>CBSA</strong> / GST-HST, and expect "
                "<strong>Canada Post</strong> last-mile after release. This page is a watch desk — brand spreadsheet "
                f'→ <a href="{HUB}">litbuyspreadsheet.eu</a>.</div></details>'
                '<details class="faq-item"><summary>How long does Litbuy take to ship to Canada?</summary>'
            ),
            1,
        )
    # sidebar: drop spreadsheet hero link prominence → hub
    html = html.replace(
        '<li><a href="/litbuy-spreadsheet/">Spreadsheet</a></li>',
        f'<li><a href="{HUB}">Spreadsheet (hub .eu)</a></li>',
        1,
    )
    # footer
    html = html.replace("<h3>LitBuy Spreadsheet</h3>", "<h3>LitBuy Canada watch desk</h3>", 1)
    html = re.sub(
        r"Independent English-language guide to LitBuy and to how you use the w2clinks catalogue to buy in China from Canada\.",
        "Canada watch: ship-to-Canada, Canada Post, CBSA, form A1A 1A1. Not promoted to keep.",
        html,
        count=1,
    )
    html = html.replace(
        "LitBuy Spreadsheet is an independent information site.",
        "This Canada watch desk is an independent information site.",
        1,
    )
    html = html.replace(
        "&copy; 2026 LitBuy Spreadsheet.",
        "&copy; 2026 LitBuy Canada watch desk (litbuyspreadsheets.ca).",
        1,
    )
    html = html.replace(
        'href="/litbuy-shipping/">Shipping and customs</a>',
        'href="/litbuy-shipping-canada/">Shipping to Canada</a>',
        1,
    )
    if MARKER not in html:
        html = html.replace("<html", f"<html {MARKER}", 1)
    return html


def _assert_ok(label: str, html: str, need: tuple[str, ...]) -> None:
    for tok in need:
        if tok not in html:
            raise SystemExit(f"{label} missing {tok!r}")
    if re.search(r"LitBuy Spreadsheet:", html) or re.search(r"LitBuy Spreadsheet: the guide", html):
        raise SystemExit(f"{label} still has Spreadsheet H1 hero")
    if "Poste Italiane" in html or "Packstation" in html or "1010 Wien" in html:
        raise SystemExit(f"{label} leaked sister fingerprint")
    # watch guard: must not claim keep
    if re.search(r"promoted to keep|keep desk|second hub", html, re.I) and "not promoted to keep" not in html.lower():
        # allow explicit "not promoted to keep"
        pass


def build() -> tuple[Path, Path]:
    home_src = OVERLAY / "live-base.index.html"
    ship_src = OVERLAY / "litbuy-shipping-canada" / "live-base.index.html"
    if not home_src.is_file() or not ship_src.is_file():
        raise SystemExit("missing live-base snapshots; fetch LIVE first")
    home = patch_home(home_src.read_text(encoding="utf-8"))
    ship = patch_shipping(ship_src.read_text(encoding="utf-8"))
    _assert_ok(
        "home",
        home,
        ("Canada Post", "CBSA", "A1A 1A1", 'id="local"', "Does LitBuy ship to Canada", "watch", HUB),
    )
    _assert_ok(
        "ship",
        ship,
        ("Canada Post", "CBSA", "A1A 1A1", 'id="local"', "Does LitBuy ship to Canada", "watch", HUB),
    )
    home_out = OVERLAY / "index.html.ca-light-fix"
    ship_out = OVERLAY / "litbuy-shipping-canada" / "index.html.ca-light-fix"
    home_out.write_text(home, encoding="utf-8")
    ship_out.write_text(ship, encoding="utf-8")
    print("wrote", home_out, "bytes", home_out.stat().st_size)
    print("wrote", ship_out, "bytes", ship_out.stat().st_size)
    return home_out, ship_out


def _load_ssh_pass() -> tuple[str, str]:
    password = os.environ.get("ORIGIN_SSH_PASS")
    host = os.environ.get("ORIGIN_SSH_HOST", "31.97.41.31")
    if password:
        return host, password
    env_path = Path(
        "/cursor/stores/bc-eb8405c7-0d3c-48be-958d-5f25b92c606c/internal/usfans-ssh.env"
    )
    if not env_path.is_file():
        raise SystemExit("Set ORIGIN_SSH_PASS or provide internal/usfans-ssh.env")
    host_v, raw = "31.97.41.31", None
    for line in env_path.read_text(encoding="utf-8").splitlines():
        if line.startswith("HOST="):
            host_v = line.split("=", 1)[1].strip()
        elif line.startswith("RAW_LINE="):
            raw = line.split("=", 1)[1]
    if not raw:
        raise SystemExit("RAW_LINE missing in usfans-ssh.env")
    return host_v, raw


def _connect():
    try:
        import paramiko
    except ImportError:
        import subprocess

        subprocess.check_call([sys.executable, "-m", "pip", "install", "paramiko", "-q"])
        import paramiko

    host, password = _load_ssh_pass()
    os.environ["ORIGIN_SSH_PASS"] = password  # for child tools; do not print
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(host, username="root", password=password, timeout=30)
    return client


def _run(client, cmd: str, timeout: int = 120) -> str:
    _, stdout, stderr = client.exec_command(cmd, timeout=timeout)
    return (stdout.read() + stderr.read()).decode(errors="replace").strip()


def deploy() -> str:
    home_out, ship_out = build()
    client = _connect()
    stamp = time.strftime("%Y%m%d-%H%M%S")
    bak = f"/www/backup/litbuy-ca-light-fix-{stamp}"
    root = f"/www/wwwroot/{HOST}"
    _run(client, f"mkdir -p '{bak}'")
    # hard refuse writing twin / hub / AT / IT roots
    forbidden = [
        "litbuyspreadsheet.eu",
        "litbuy.at",
        "litbuyspreadsheet.it",
        "litbuyspreadsheetnow.com",
        "litbuyspreadsheets.es",
        "litbuyspreadsheets.us",
        "litbuyspreadsheet.me.uk",
        "litbuyspreadsheets.nl",
        "litspreadsheet.fr",
    ]
    sftp = client.open_sftp()
    pairs = [
        (home_out, f"{root}/index.html", "index.html"),
        (ship_out, f"{root}/litbuy-shipping-canada/index.html", "litbuy-shipping-canada.index.html"),
    ]
    for local, remote, bak_name in pairs:
        raw = local.read_text(encoding="utf-8")
        if 'id="local"' not in raw or "Canada Post" not in raw:
            raise SystemExit(f"refusing PUT {remote}")
        if "LitBuy Spreadsheet: the guide" in raw or "LitBuy Spreadsheet:" in raw.split("<h1>", 1)[-1][:80]:
            raise SystemExit(f"refusing Spreadsheet hero on {remote}")
        if any(f"/www/wwwroot/{h}" in remote for h in forbidden):
            raise SystemExit(f"refusing forbidden host path {remote}")
        _run(client, f"cp -a '{remote}' '{bak}/{bak_name}.before'")
        sftp.put(str(local), remote)
        _run(client, f"chown www:www '{remote}'")
        print("PUT", remote, "bytes", local.stat().st_size)
    # sitemap lastmod bump for money URLs only
    sm_remote = f"{root}/sitemap.xml"
    _run(client, f"cp -a '{sm_remote}' '{bak}/sitemap.xml.before'")
    with sftp.open(sm_remote, "r") as f:
        sm = f.read().decode("utf-8", "replace")
    today = time.strftime("%Y-%m-%d")
    for loc in (
        f"https://{HOST}/",
        f"https://{HOST}/litbuy-shipping-canada/",
        f"https://{HOST}/cbsa-import-canada/",
        f"https://{HOST}/canada-post-customs/",
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
    twin_check = _run(
        client,
        "echo '--- twin wwwroot presence (expect NO live index writes this round) ---'; "
        "for h in litbuyspreadsheetnow.com litbuyspreadsheets.es litbuyspreadsheets.us "
        "litbuyspreadsheet.me.uk litbuyspreadsheets.nl litspreadsheet.fr; do "
        "  echo -n \"$h \"; test -d /www/wwwroot/$h && echo HAS_DIR || echo NO_DIR; "
        "done; "
        f"ls '{root}/index.html' '{root}/litbuy-shipping-canada/index.html'",
    )
    print(twin_check)
    print("backup", bak)
    client.close()
    return bak


def submit_gsc(out_json: Path | None = None) -> dict:
    sa = os.environ.get(
        "GSC_SA_JSON",
        "/cursor/stores/bc-eb8405c7-0d3c-48be-958d-5f25b92c606c/internal/gsc-sa.json",
    )
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

    scopes = ["https://www.googleapis.com/auth/webmasters"]
    creds = service_account.Credentials.from_service_account_file(sa, scopes=scopes)
    gsc = build("searchconsole", "v1", credentials=creds, cache_discovery=False)
    site = f"sc-domain:{HOST}"
    feed = f"https://{HOST}/sitemap.xml"
    gsc.sitemaps().submit(siteUrl=site, feedpath=feed).execute()
    time.sleep(0.5)
    meta = gsc.sitemaps().get(siteUrl=site, feedpath=feed).execute()
    result = {
        "site": site,
        "feed": feed,
        "submitted": True,
        "errors": meta.get("errors"),
        "warnings": meta.get("warnings"),
        "lastSubmitted": meta.get("lastSubmitted"),
        "isPending": meta.get("isPending"),
    }
    if out_json:
        out_json.parent.mkdir(parents=True, exist_ok=True)
        out_json.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))
    return result


def main() -> None:
    if "--deploy" in sys.argv:
        bak = deploy()
        print("DEPLOY_OK", bak)
        return
    if "--gsc" in sys.argv:
        out = Path(
            "/cursor/stores/bc-eb8405c7-0d3c-48be-958d-5f25b92c606c/internal/litbuy-ca-light-fix/gsc_sitemap_submit.json"
        )
        submit_gsc(out)
        return
    build()


if __name__ == "__main__":
    main()
