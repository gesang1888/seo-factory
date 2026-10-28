#!/usr/bin/env python3
"""Deepen hipobuyspreadsheet.nl keep desk: Douane / NL-postcode / 1234 AB + hub uplink.

LIVE only on hipobuyspreadsheet.nl. Does not touch hub, UK, or revive Phase C.
Requires ORIGIN_SSH_PASS (or internal/usfans-ssh.env via --load-env).
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
OVERLAY = ROOT / "sites" / "hipobuyspreadsheet.nl" / "overlay"
HOST = "hipobuyspreadsheet.nl"
REMOTE = f"/www/wwwroot/{HOST}"
STAMP = "20261028"
HUB = "https://hipobuyspreadsheet.net"
PAGES = (
    "hipobuy-shipping-guide",
    "is-hipobuy-legit",
    "hipobuy-spreadsheet",
)

STYLE = (
    f'<style id="nl-deepen-{STAMP}">.hub-uplink{{margin:14px 0 0;padding:12px 14px;'
    "border-left:3px solid #0f766e;background:#f0fdfa;color:#134e4a;line-height:1.6;"
    "font-size:15px;max-width:760px}}.hub-uplink a{{color:#0f766e;font-weight:600}}"
    "#local{scroll-margin-top:88px}.local-box{margin:1.25em 0;padding:14px 16px;"
    "border:1px solid #e2e8f0;border-radius:10px;background:#f8fafc}</style>"
)

HUB_UPLINK = (
    f'<p class="hub-uplink" data-nl-deepen="{STAMP}" data-step4-hub="1">'
    "Merk / Spreadsheet / Coupons / Dataset → "
    f'<a href="{HUB}/">hipobuyspreadsheet.net</a> · '
    f'<a href="{HUB}/hipobuy-coupons/">coupons</a> · '
    f'<a href="{HUB}/finds-dataset/">dataset</a> '
    "(Independent Index · 8,600+). Deze URL = NL lokaal "
    "(NL-postcode <code>1234 AB</code> · Douane · PostNL)."
    "</p>"
)

LOCAL_SHIP = f"""
<section id="local" class="local-box" data-nl-fingerprint="nl-postcode-douane-postnl" data-nl-deepen="{STAMP}">
<h2>NL-fingerprint vóór lijnkeuze</h2>
<ol>
<li><strong>Estimator-bestemming: Nederland</strong> — kies NL, niet EU en niet DE/BE.</li>
<li><strong>Adres</strong> — Nederlandse postcode-vorm <code>1234 AB</code> (geen Duits Packstation-nummer).</li>
<li><strong>Last mile</strong> — vaak <strong>PostNL</strong> of DHL; check de live SKU in de app.</li>
<li><strong>Douane / BTW — drie modi</strong>: Tax free · Prepaid Duty · Duties Payable by Recipient. Bron: <a href="https://www.belastingdienst.nl/wps/wcm/connect/nl/douane/douane" rel="noopener" target="_blank">Belastingdienst Douane</a>.</li>
</ol>
<p>Merk-spreadsheet / coupons / dataset blijven op de hub <a href="{HUB}/">hipobuyspreadsheet.net</a>.</p>
</section>
"""

LOCAL_LEGIT = f"""
<section id="local" class="local-box" data-nl-fingerprint="legit-nl-douane-1234ab" data-nl-deepen="{STAMP}">
<h2>NL-fingerprint bij „is HipoBuy legitiem?”</h2>
<ol>
<li><strong>Escrow ≠ Douane</strong> — escrow dekt de agent; invoer volgt de geboekte lijn (Tax free / Prepaid Duty / Duties Payable by Recipient).</li>
<li><strong>Adres</strong> — postcode <code>1234 AB</code>; verkeerd land = verkeerde last mile.</li>
<li><strong>Last mile</strong> — PostNL/DHL op de live SKU; deze desk opent geen ticket.</li>
<li><strong>Bron</strong> — <a href="https://www.belastingdienst.nl/wps/wcm/connect/nl/douane/douane" rel="noopener" target="_blank">Belastingdienst Douane</a>; verzending: <a href="/hipobuy-shipping-guide/">shipping guide</a>.</li>
</ol>
<p>Globale spreadsheet / coupons / dataset → <a href="{HUB}/">hipobuyspreadsheet.net</a> (8,600+).</p>
</section>
"""

LOCAL_SHEET = f"""
<section id="local" class="local-box" data-nl-fingerprint="spreadsheet-note-yields-hub" data-nl-deepen="{STAMP}">
<h2>Deze URL is géén tweede spreadsheet-hub</h2>
<ol>
<li><strong>Brand spreadsheet / finds / QC-index</strong> → alleen hub <a href="{HUB}/">hipobuyspreadsheet.net</a> (Independent Index · 8,600+).</li>
<li><strong>NL desk</strong> — postcode <code>1234 AB</code>, Douane-drie modi, PostNL/DHL last mile.</li>
<li><strong>Coupons / dataset-waarheid</strong> → <a href="{HUB}/hipobuy-coupons/">hub coupons</a> · <a href="{HUB}/finds-dataset/">finds-dataset</a>.</li>
<li><strong>Verzending NL</strong> → <a href="/hipobuy-shipping-guide/">hipobuy-shipping-guide</a> (estimator-snapshot + volumgewicht).</li>
</ol>
</section>
"""

THICKEN_SHIP = f"""
<h2 class="ph" id="nl-postcode-douane">NL-postcode <code>1234 AB</code>, Douane, PostNL</h2>
<p class="pp">Deze desk legt <strong>verzendkosten naar Nederland</strong> uit — geen Spreadsheet-held. Vul in de officiële estimator bestemming <strong>Netherlands</strong>, met een Nederlands adres in de vorm <strong>1234 AB</strong>. Last mile staat vaak op <strong>PostNL</strong> of DHL (live SKU). Invoer volgt één van de <strong>drie Douane-modi</strong> hierboven; wij verzinnen geen eurobedragen en geen aangegeven waarde.</p>
<p class="pp">Merk-spreadsheet / coupons / dataset: <a href="{HUB}/">hipobuyspreadsheet.net</a> · <a href="{HUB}/hipobuy-coupons/">coupons</a> · <a href="{HUB}/finds-dataset/">dataset</a> (8,600+). Estimator-lab hierboven blijft snapshot <strong>29 Sep 2026</strong> — geen kassa.</p>
"""

THICKEN_LEGIT = f"""
<h2 class="ph" id="nl-legit-douane">Legitiem voor een Nederlands adres</h2>
<p class="pp"><strong>Is HipoBuy legitiem?</strong> Voor NL-kopers: escrow dekt de agent; <strong>Douane/BTW</strong> volgt de lijn (Tax free · Prepaid Duty · Duties Payable by Recipient). Gebruik postcode <strong>1234 AB</strong> en check PostNL/DHL op de live SKU. Dit desk is infosite — geen account, geen porto, geen ticket.</p>
<p class="pp">Globale catalogus / spreadsheet / coupons → hub <a href="{HUB}/">hipobuyspreadsheet.net</a>. Lokale verzending: <a href="/hipobuy-shipping-guide/">shipping guide</a>.</p>
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
    out = (stdout.read() + stderr.read()).decode(errors="replace").strip()
    return out


def _soften_brand(html: str) -> str:
    html = html.replace(
        '<span>Spreadsheet</span>',
        '<span>Nederland</span>',
        1,
    )
    html = html.replace(
        "<h3>HipoBuy Spreadsheet</h3>",
        "<h3>HipoBuy Nederland</h3>",
        1,
    )
    html = html.replace(
        "&copy; 2026 HipoBuy Spreadsheet.",
        "&copy; 2026 HipoBuy Nederland (NL desk).",
        1,
    )
    html = re.sub(
        r"(Onafhankelijkheidsnotitie\.</strong>)\s*HipoBuy Spreadsheet is",
        r"\1 hipobuyspreadsheet.nl is de NL-desk (NL-postcode / Douane / PostNL). "
        r"Merk-spreadsheet → hipobuyspreadsheet.net. Deze tekst was",
        html,
        count=1,
    )
    return html


def _inject_head_style(html: str) -> str:
    if f'id="nl-deepen-{STAMP}"' in html:
        return html
    return html.replace("</head>", STYLE + "\n</head>", 1)


def deepen_shipping(html: str) -> str:
    html = _inject_head_style(html)
    html = _soften_brand(html)
    new_title = (
        "HipoBuy verzending Nederland — Douane, NL-postcode 1234 AB, PostNL"
    )
    new_desc = (
        "NL desk: estimator-snapshot 29 Sep 2026, Douane-drie modi (Tax free / Prepaid Duty / "
        "Duties Payable by Recipient), postcode 1234 AB, PostNL/DHL. Merk-spreadsheet → "
        "hipobuyspreadsheet.net (8,600+)."
    )
    html = re.sub(r"<title>.*?</title>", f"<title>{new_title}</title>", html, count=1, flags=re.S)
    html = re.sub(
        r'name="description" content="[^"]*"',
        f'name="description" content="{new_desc}"',
        html,
        count=1,
    )
    html = re.sub(
        r'property="og:title" content="[^"]*"',
        f'property="og:title" content="{new_title}"',
        html,
        count=1,
    )
    html = re.sub(
        r'property="og:description" content="[^"]*"',
        f'property="og:description" content="{new_desc}"',
        html,
        count=1,
    )
    html = html.replace(
        '<span class="atg" style="background:var(--acl);color:var(--acd)">Shipping Guide</span>',
        f'<span class="atg" style="background:var(--acl);color:var(--acd)" data-nl-deepen="{STAMP}">NL verzending · Douane · 1234 AB</span>',
        1,
    )
    html = html.replace(
        '<span class="adt">Lab 29 Sep 2026</span>',
        f'<span class="adt">Lab 29 Sep 2026 · desk deepen {STAMP[:4]}-{STAMP[4:6]}-{STAMP[6:]}</span>',
        1,
    )
    # Keep NL H1 (already local); tighten lead + inject uplink/local
    if 'class="hub-uplink"' not in html:
        html = html.replace(
            '<p class="aint">Na magazijnfoto’s: werkelijk gewicht versus L×B×H/8000, daarna een NL-bestemming in HipoBuy — niet de USA-rij uit de sjabloontabel.</p>\n  </header>',
            '<p class="aint">Na magazijnfoto’s: werkelijk gewicht versus L×B×H/8000, daarna bestemming <strong>Netherlands</strong> met postcode <strong>1234 AB</strong> — niet de USA-rij. Douane: drie modi hieronder.</p>\n'
            f"  {HUB_UPLINK}\n"
            f"  {LOCAL_SHIP}\n"
            "  </header>",
            1,
        )
    if 'id="nl-postcode-douane"' not in html:
        html = html.replace(
            '<h2 class="ph" id="calculator">Geen USA-rekenmachine op deze desk</h2>',
            THICKEN_SHIP + '\n<h2 class="ph" id="calculator">Geen USA-rekenmachine op deze desk</h2>',
            1,
        )
    return html


def deepen_legit(html: str) -> str:
    html = _inject_head_style(html)
    html = _soften_brand(html)
    new_title = "Is HipoBuy legitiem? Nederland — Douane, escrow, PostNL"
    new_desc = (
        "Is HipoBuy legitiem voor een Nederlands adres? Escrow, QC, Douane-drie modi, "
        "postcode 1234 AB, PostNL/DHL. Score 4.3/5. Merk-spreadsheet → hipobuyspreadsheet.net."
    )
    html = re.sub(r"<title>.*?</title>", f"<title>{new_title}</title>", html, count=1, flags=re.S)
    html = re.sub(
        r'name="description" content="[^"]*"',
        f'name="description" content="{new_desc}"',
        html,
        count=1,
    )
    html = re.sub(
        r'property="og:title" content="[^"]*"',
        f'property="og:title" content="{new_title}"',
        html,
        count=1,
    )
    html = re.sub(
        r'property="og:description" content="[^"]*"',
        f'property="og:description" content="{new_desc}"',
        html,
        count=1,
    )
    html = re.sub(
        r'("headline":\s*")[^"]+(")',
        r'\1Is HipoBuy legitiem? NL Douane & escrow 2026\2',
        html,
        count=1,
    )
    html = html.replace(
        '<span class="atg" style="background:var(--acl);color:var(--acd)">Trust Review</span>',
        f'<span class="atg" style="background:var(--acl);color:var(--acd)" data-nl-deepen="{STAMP}">NL trust · Douane · 1234 AB</span>',
        1,
    )
    html = html.replace(
        '<span class="adt">Updated June 2026</span>',
        f'<span class="adt">Updated 28 Oct 2026 · deepen {STAMP}</span>',
        1,
    )
    html = re.sub(
        r'<h1 class="atit">Is Hipobuy <em>Legit</em>\?<br>Honest Review 2026</h1>',
        '<h1 class="atit">Is HipoBuy <em>legitiem</em>?<br>Nederland · Douane &amp; escrow</h1>',
        html,
        count=1,
    )
    html = html.replace(
        '<p class="aint">Hipobuy is a Chinese buying agent connecting Western buyers to Weidian, Taobao and 1688. This page gives you the honest community verdict based on buyer protection analysis and real order experiences.</p>\n  </header>',
        '<p class="aint">HipoBuy is een Chinese inkoopagent (Weidian / Taobao / 1688). Deze NL-desk beantwoordt „is HipoBuy legitiem?” met escrow + lokale Douane/PostNL-context — geen tweede spreadsheet-hub.</p>\n'
        f"  {HUB_UPLINK}\n"
        f"  {LOCAL_LEGIT}\n"
        "  </header>",
        1,
    )
    html = html.replace(
        '<p class="vlb">Our Verdict</p><p class="vt">Yes &mdash; Hipobuy is legit and safe to use in 2026</p>',
        '<p class="vlb">Ons oordeel</p><p class="vt">Ja — HipoBuy is legitiem; Douane volgt je NL-lijn</p>',
        1,
    )
    html = html.replace(
        'Use the <a href="/hipobuy-spreadsheet">Hipobuy spreadsheet</a> to browse products, our <a href="/hipobuy-shipping-guide">shipping guide</a> to estimate costs',
        f'Gebruik de hub-<a href="{HUB}/">spreadsheet / Independent Index</a> voor catalogus, onze <a href="/hipobuy-shipping-guide/">shipping guide</a> voor NL-porto',
        1,
    )
    if 'id="nl-legit-douane"' not in html:
        html = html.replace(
            '<h2 class="ph" id="faq">Frequently asked questions</h2>',
            THICKEN_LEGIT + '\n<h2 class="ph" id="faq">Frequently asked questions</h2>',
            1,
        )
    return html


def deepen_spreadsheet(html: str) -> str:
    html = _inject_head_style(html)
    html = _soften_brand(html)
    new_title = "HipoBuy Nederland — NL-postcode & Douane (spreadsheet → hub)"
    new_desc = (
        "NL desk-notitie: merk-spreadsheet / finds / dataset horen op hipobuyspreadsheet.net "
        "(Independent Index · 8,600+). Hier: NL-postcode 1234 AB, Douane, PostNL."
    )
    html = re.sub(r"<title>.*?</title>", f"<title>{new_title}</title>", html, count=1, flags=re.S)
    html = re.sub(
        r'name="description" content="[^"]*"',
        f'name="description" content="{new_desc}"',
        html,
        count=1,
    )
    html = re.sub(
        r'property="og:title" content="[^"]*"',
        f'property="og:title" content="{new_title}"',
        html,
        count=1,
    )
    html = re.sub(
        r'property="og:description" content="[^"]*"',
        f'property="og:description" content="{new_desc}"',
        html,
        count=1,
    )
    html = re.sub(
        r'("name":\s*")Hipobuy Spreadsheet 2026(")',
        r'\1HipoBuy Nederland — spreadsheet note yields hub\2',
        html,
        count=1,
    )
    # Kill Spreadsheet hero
    html = html.replace(
        '<div class="hbg">Updated daily &middot; 2026</div>\n'
        "  <h1>Hipobuy Spreadsheet<br><em>2026 Edition</em></h1>\n"
        '  <p class="hsub">Browse 12,000+ products &mdash; shoes, bags, clothing and accessories with direct Hipobuy purchase links.</p>',
        f'<div class="hbg" data-nl-deepen="{STAMP}">NL desk · spreadsheet → hub · 28 Oct 2026</div>\n'
        "  <h1>HipoBuy Nederland<br><em>geen tweede spreadsheet-hub</em></h1>\n"
        '  <p class="hsub">Merk-spreadsheet / Independent Index (8,600+) staat op '
        f'<a href="{HUB}/">hipobuyspreadsheet.net</a>. Deze URL helpt NL-kopers met Douane, '
        "postcode <strong>1234 AB</strong> en PostNL.</p>",
        1,
    )
    if 'class="hub-uplink"' not in html:
        html = html.replace(
            '  <div class="hst">\n'
            '    <div class="hs"><div class="hsn">12,000+</div><div class="hsl">Products</div></div>',
            f"  {HUB_UPLINK}\n"
            f"  {LOCAL_SHEET}\n"
            '  <div class="hst">\n'
            f'    <div class="hs"><div class="hsn">8,600+</div><div class="hsl">Hub index</div></div>',
            1,
        )
    # NL editor notes → yield hub
    html = html.replace(
        "<h2>How Netherlands buyers use this sheet</h2>"
        "<p>Treat each row as a lead: open the listing, confirm size/batch, then QC. "
        "Note estimated weight so you can model EUR freight and BTW/douane before submit.</p>"
        '<p>Pair with <a href="/hipobuy-shipping-guide/">shipping</a> and '
        '<a href="/hipobuy-qc-guide/">QC</a>.</p>',
        "<h2>Nederland: sheet-intent → hub; desk = Douane / PostNL</h2>"
        "<p>Rijen/catalogus: open de hub <a href=\""
        + HUB
        + "/\">Independent Index</a> of "
        f'<a href="{HUB}/finds-dataset/">finds-dataset</a>. Schat gewicht, modelleer EUR-vracht '
        "en BTW/Douane met postcode <strong>1234 AB</strong> vóór submit.</p>"
        '<p>Pair: <a href="/hipobuy-shipping-guide/">shipping</a> · '
        '<a href="/hipobuy-qc-guide/">QC</a> · '
        f'<a href="{HUB}/hipobuy-coupons/">hub coupons</a>.</p>',
        1,
    )
    return html


BUILDERS = {
    "hipobuy-shipping-guide": deepen_shipping,
    "is-hipobuy-legit": deepen_legit,
    "hipobuy-spreadsheet": deepen_spreadsheet,
}


def build() -> dict[str, Path]:
    out: dict[str, Path] = {}
    for slug in PAGES:
        base = OVERLAY / slug / "live-base.index.html"
        if not base.exists():
            raise SystemExit(f"missing live base: {base}")
        deepened = BUILDERS[slug](base.read_text(errors="replace"))
        for must in (
            'id="local"',
            'class="hub-uplink"',
            "1234 AB",
            "Douane",
            f'data-nl-deepen="{STAMP}"',
            "hipobuyspreadsheet.net",
            "finds-dataset",
            "8,600",
        ):
            if must not in deepened:
                raise SystemExit(f"{slug}: missing {must}")
        if re.search(r"<h1[^>]*>[^<]*Spreadsheet", deepened, re.I):
            raise SystemExit(f"{slug}: H1 still Spreadsheet hero")
        title_m = re.search(r"<title>(.*?)</title>", deepened, re.S | re.I)
        if title_m and re.search(r"Spreadsheet 2026", title_m.group(1), re.I):
            raise SystemExit(f"{slug}: <title> still Spreadsheet hero")
        if slug == "hipobuy-shipping-guide":
            for must in ("PostNL", "Tax free", "Prepaid Duty", "Duties Payable by Recipient", "29 Sep 2026"):
                if must not in deepened:
                    raise SystemExit(f"{slug}: missing {must}")
        dest = OVERLAY / slug / "index.html.nl-deepen"
        dest.write_text(deepened)
        out[slug] = dest
        print("BUILT", dest, "bytes", dest.stat().st_size)
    return out


def deploy(built: dict[str, Path], store_internal: Path | None) -> dict:
    client = _connect()
    bak = f"/www/backup/hipobuy-nl-deepen-{datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%S')}"
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

    today = "2026-10-28"
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
        # ensure spreadsheet + legit + shipping present
        for slug in PAGES:
            loc = f"https://{HOST}/{slug}/"
            if loc not in sm:
                sm = sm.replace(
                    "</urlset>",
                    f"<url><loc>{loc}</loc><lastmod>{today}</lastmod></url>\n</urlset>",
                )
        tmp = Path(f"/tmp/hipobuy-nl-sitemap-{STAMP}.xml")
        tmp.write_text(sm)
        sftp.put(str(tmp), f"{REMOTE}/sitemap.xml")
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
        req = Request(url, headers={"User-Agent": "hipobuy-nl-deepen/1.0"})
        with urlopen(req, timeout=30) as resp:
            body = resp.read().decode(errors="replace")
            code = resp.status
        row = {
            "url": url,
            "http": code,
            "id_local": 'id="local"' in body,
            "hub_uplink": "hipobuyspreadsheet.net" in body and "finds-dataset" in body,
            "postcode_1234ab": body.count("1234 AB"),
            "douane": body.count("Douane"),
            "data_nl_deepen": f'data-nl-deepen="{STAMP}"' in body,
            "spreadsheet_h1": bool(re.search(r"<h1[^>]*>[^<]*Spreadsheet", body, re.I)),
        }
        m = re.search(r"<title>(.*?)</title>", body, re.S | re.I)
        row["title"] = re.sub(r"\s+", " ", m.group(1)).strip() if m else None
        h1 = re.search(r"<h1[^>]*>(.*?)</h1>", body, re.S | re.I)
        row["h1"] = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", h1.group(1))).strip() if h1 else None
        checks.append(row)

    # home + hub untouched markers
    for url, forbid in [
        (f"https://{HOST}/", f'data-nl-deepen="{STAMP}"'),
        (f"{HUB}/", f'data-nl-deepen="{STAMP}"'),
    ]:
        req = Request(url, headers={"User-Agent": "hipobuy-nl-deepen/1.0"})
        with urlopen(req, timeout=30) as resp:
            body = resp.read().decode(errors="replace")
            code = resp.status
        checks.append(
            {
                "url": url,
                "http": code,
                "untouched_no_nl_deepen": forbid not in body,
            }
        )

    # Phase C / twin still 301
    import http.client
    from urllib.parse import urlparse

    twins = [
        ("https://hipobuy.at/", "https://hipobuyspreadsheet.net"),
        ("https://hipobuyspreadsheet.eu/", "https://hipobuyspreadsheet.net"),
        ("https://hipobuyreview.com/", "https://hipobuyspreadsheet.net"),
        ("https://hipobuyspreadsheet.us/", "https://hipobuyspreadsheet.net"),
        ("https://hipobuyspreadsheets.uk/", "https://hipobuyspreadsheet.co.uk"),
    ]
    twin_rows = []
    for t, expect_prefix in twins:
        u = urlparse(t)
        conn = http.client.HTTPSConnection(u.netloc, timeout=20)
        conn.request("GET", u.path or "/", headers={"User-Agent": "hipobuy-nl-deepen/1.0"})
        r = conn.getresponse()
        loc = r.getheader("Location") or ""
        twin_rows.append(
            {
                "url": t,
                "http": r.status,
                "location": loc,
                "ok": r.status in (301, 302) and loc.startswith(expect_prefix),
            }
        )
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
            and c.get("url") != f"https://{HOST}/"
            and (
                not c.get("id_local")
                or not c.get("hub_uplink")
                or not c.get("data_nl_deepen")
                or c.get("spreadsheet_h1")
                or c.get("http") != 200
            )
        ]
        home_hub_bad = [
            c
            for c in ver["checks"]
            if c.get("url") in (f"https://{HOST}/", f"{HUB}/")
            and not c.get("untouched_no_nl_deepen")
        ]
        twin_bad = [t for t in ver.get("twins", []) if not t.get("ok")]
        if bad or twin_bad or home_hub_bad:
            print("VERIFY_FAIL", bad, twin_bad, home_hub_bad)
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
