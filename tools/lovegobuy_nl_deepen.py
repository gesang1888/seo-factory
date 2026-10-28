#!/usr/bin/env python3
"""Deepen lovegobuy.nl keep desk: PostNL / Douane / 1234 AB + hub uplink.

LIVE only on lovegobuy.nl. Does not touch hub (lovegobuyguide.com), IT, or revive twins.
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

ROOT = Path(__file__).resolve().parents[1]
OVERLAY = ROOT / "sites" / "lovegobuy.nl" / "overlay"
HOST = "lovegobuy.nl"
REMOTE = f"/www/wwwroot/{HOST}"
STAMP = "20261028"
HUB = "https://lovegobuyguide.com"
TODAY = "2026-10-28"
PAGES = (
    "lovegobuy-shipping",
    "lovegobuy-ervaringen",
    "lovegobuy-coupon",
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
    "Merk-gids / Spreadsheet / Coupons / Dataset → "
    f'<a href="{HUB}/">lovegobuyguide.com</a> · '
    f'<a href="{HUB}/lovegobuy-coupon/">coupons</a> · '
    f'<a href="{HUB}/finds-dataset/">dataset</a> '
    "(Independent Index · 11,300+). Deze URL = NL lokaal "
    "(PostNL / Douane / postcode <code>1234 AB</code>)."
    "</p>"
)

LOCAL_SHIP = f"""
<section id="local" class="local-box" data-nl-fingerprint="postnl-douane-1234ab" data-nl-deepen="{STAMP}">
<h2>NL-fingerprint vóór je een lijn boekt</h2>
<ol>
<li><strong>Schatter-bestemming: Nederland</strong> — kies NL, niet EU en niet BE/DE.</li>
<li><strong>Adres</strong> — Nederlandse postcode (vorm <code>1234 AB</code>), geen Duits Packstation.</li>
<li><strong>Last mile</strong> — vaak <strong>PostNL</strong> of DHL; desk verzint geen servicepunt.</li>
<li><strong>Invoer</strong> — SKU + lijn beslissen. Bron ochtend van verzenden: <a href="https://www.belastingdienst.nl/wps/wcm/connect/nl/douane/" rel="noopener" target="_blank">Belastingdienst Douane</a>.</li>
</ol>
<p>Ervaringen: <a href="/lovegobuy-ervaringen/">LoveGoBuy ervaringen NL</a> · Merk-spreadsheet: <a href="{HUB}/">lovegobuyguide.com</a>.</p>
</section>
"""

LOCAL_ERV = f"""
<section id="local" class="local-box" data-nl-fingerprint="ervaringen-postnl-douane" data-nl-deepen="{STAMP}">
<h2>NL-fingerprint bij ervaringen</h2>
<ol>
<li><strong>Lees recente NL-hauls</strong> — let op postcode <code>1234 AB</code>, lijnnaam en of last mile <strong>PostNL</strong> of DHL was.</li>
<li><strong>Douane / BTW</strong> — vertraging ≠ scam; check SKU-inklaring en <a href="https://www.belastingdienst.nl/wps/wcm/connect/nl/douane/" rel="noopener" target="_blank">Douane</a>.</li>
<li><strong>QC vóór verzenden</strong> — reclameren is makkelijker in het magazijn dan na inklaring.</li>
<li><strong>Merk-spreadsheet</strong> — Independent Index / coupons / dataset staan op <a href="{HUB}/">lovegobuyguide.com</a>, niet op dit desk.</li>
</ol>
<p>Verzending: <a href="/lovegobuy-shipping/">Verzenden naar Nederland</a>.</p>
</section>
"""

LOCAL_COUPON = f"""
<section id="local" class="local-box" data-nl-fingerprint="coupon-vs-douane-postnl" data-nl-deepen="{STAMP}">
<h2>NL-fingerprint: coupon ≠ Douane</h2>
<ol>
<li><strong>Invite / wallet</strong> — korting geldt in de officiële app; deze host int niets.</li>
<li><strong>BTW / Douane</strong> — een coupon verlaagt geen inklaringsfee. Bron: <a href="https://www.belastingdienst.nl/wps/wcm/connect/nl/douane/" rel="noopener" target="_blank">Douane</a>.</li>
<li><strong>Last mile</strong> — <strong>PostNL</strong>/DHL-kosten volgen gewicht + lijn, niet de invite-code.</li>
<li><strong>Globale coupon-waarheid</strong> — live packs / Independent Index → <a href="{HUB}/lovegobuy-coupon/">lovegobuyguide.com/lovegobuy-coupon/</a>.</li>
</ol>
</section>
"""

THICKEN_SHIP = f"""
<h2 id="postnl-douane">PostNL, Douane en postcode 1234 AB</h2>
<p>Verzenden naar Nederland betekent: schatter op <strong>Netherlands</strong>, bezorgadres met postcode <strong>1234 AB</strong>, last mile vaak <strong>PostNL</strong> (of DHL), en invoer volgens <strong>Belastingdienst Douane</strong> + de gekozen SKU — geen Spreadsheet-held op deze URL. Ervaringen van NL-hauls: <a href="/lovegobuy-ervaringen/">ervaringen</a>. Merk-spreadsheet / dataset → <a href="{HUB}/">lovegobuyguide.com</a>.</p>
<p>Tracking start internationaal; inlandse scans lopen vaak via PostNL. Blijft de status lang op douane/inklaring: bewaar documentatie en lees de Douane-pagina van die ochtend — een Discord-screenshot is geen aangifte.</p>
"""

THICKEN_ERV = f"""
<h2 id="postnl-ervaring">Wat een bruikbare NL-ervaring vermeldt</h2>
<p>Goede <strong>LoveGoBuy ervaringen</strong> noemen: parcelgewicht, lijn, of last mile <strong>PostNL</strong>/DHL was, postcode-patroon <strong>1234 AB</strong>, en of er Collect/Douane-kosten bij kwamen. Slechte signalen: alleen hype zonder datum, of “geen BTW” zonder SKU-context.</p>
<p>Douane-vertraging is een verwachtingsprobleem, geen automatisch oordeel over de agent. Plan invoer via <a href="/lovegobuy-shipping/">verzending NL</a> en de <a href="https://www.belastingdienst.nl/wps/wcm/connect/nl/douane/" rel="noopener" target="_blank">Douane</a>. Voor de live finds-catalogus en coupons: <a href="{HUB}/">lovegobuyguide.com</a> (Independent Index · 11,300+).</p>
"""

THICKEN_COUPON = f"""
<h2 id="coupon-hub">Coupon op NL-desk vs hub-waarheid</h2>
<p>Invite <strong>W5RJX3</strong> helpt bij registratie op lovegobuy.com; lokale NL-context blijft PostNL / Douane / <code>1234 AB</code>. De actuele coupon-tabel, dataset en brand spreadsheet horen op <a href="{HUB}/lovegobuy-coupon/">lovegobuyguide.com</a> — dit desk herhaalt geen tweede hub.</p>
"""


def _load_env(path: Path) -> None:
    text = path.read_text()
    host = pass_val = None
    for line in text.splitlines():
        if line.startswith("HOST="):
            host = line.split("=", 1)[1].strip().strip('"').strip("'")
        if line.startswith("RAW_LINE="):
            raw = line.split("=", 1)[1]
            # Keep leading semicolon; only strip matching outer quotes if both ends quoted.
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


def _inject_head_style(html: str) -> str:
    if f'id="nl-deepen-{STAMP}"' in html:
        return html
    return html.replace("</head>", STYLE + "\n</head>", 1)


def _soften_brand(html: str) -> str:
    html = html.replace("<span>Spreadsheet</span>", "<span>Nederland</span>", 1)
    html = html.replace("<h3>LoveGoBuy Spreadsheet</h3>", "<h3>LoveGoBuy Nederland</h3>")
    html = html.replace(
        "&copy; 2026 LoveGoBuy Spreadsheet.",
        "&copy; 2026 LoveGoBuy Nederland (NL desk).",
    )
    html = re.sub(
        r"(Onafhankelijkheidsnotitie\.</strong>)\s*LoveGoBuy Spreadsheet is",
        r"\1 lovegobuy.nl is de NL-desk (PostNL / Douane / 1234 AB). "
        r"Merk-spreadsheet → lovegobuyguide.com. LoveGoBuy Spreadsheet was",
        html,
        count=1,
    )
    html = html.replace(
        '"name": "Lovegobuy Spreadsheet Guide"',
        '"name": "LoveGoBuy Nederland desk"',
    )
    return html


def deepen_shipping(html: str) -> str:
    html = _inject_head_style(html)
    html = _soften_brand(html)
    new_title = "Verzending naar Nederland — PostNL, Douane, NL-postcode | LoveGoBuy"
    html = re.sub(r"<title>.*?</title>", f"<title>{new_title}</title>", html, count=1, flags=re.S)
    html = html.replace(
        '"name": "LoveGoBuy Spreadsheet in het Nederlands: verzending en douane naar Nederland"',
        f'"name": "{new_title}"',
    )
    html = html.replace(
        '"description": "Independent LoveGoBuy ship for Nederland."',
        '"description": "Verzending naar NL: PostNL, Douane, postcode 1234 AB. Merk-spreadsheet → lovegobuyguide.com."',
    )
    if f'data-nl-deepen="{STAMP}"' not in html:
        html = html.replace(
            '<p class="lead">Bestemming Netherlands — 荷兰, niet EU. Het afleveradres is een Nederlandse postcode (vorm 1234 AB), geen Duits afhaalautomaat-nummer.</p>',
            '<p class="lead">Bestemming <strong>Netherlands</strong>, niet EU. Bezorgadres met postcode <strong>1234 AB</strong>. Last mile vaak <strong>PostNL</strong> of DHL; invoer: <strong>Douane</strong>.</p>\n'
            f"  {HUB_UPLINK}\n"
            f"  {LOCAL_SHIP}",
            1,
        )
    if 'id="postnl-douane"' not in html:
        html = html.replace(
            "<h2>De officiële schatter beslist</h2>",
            THICKEN_SHIP + "\n  <h2>De officiële schatter beslist</h2>",
            1,
        )
    # address section reinforce PostNL
    html = html.replace(
        "<h2>Het adres op dit dest</h2>\n  <p>Het afleveradres is een Nederlandse postcode (vorm 1234 AB), geen Duits afhaalautomaat-nummer.",
        "<h2>Het adres op dit dest</h2>\n  <p>Het afleveradres is een Nederlandse postcode (vorm <strong>1234 AB</strong>), geen Duits afhaalautomaat-nummer. Last mile landt vaak bij <strong>PostNL</strong>.",
        1,
    )
    return html


def deepen_ervaringen(html: str) -> str:
    html = _inject_head_style(html)
    html = _soften_brand(html)
    new_title = "LoveGoBuy ervaringen Nederland — PostNL, Douane, reviews | 2026"
    html = re.sub(r"<title>.*?</title>", f"<title>{new_title}</title>", html, count=1, flags=re.S)
    html = re.sub(
        r'("name":\s*")LoveGoBuy Ervaringen 2026 — Reviews(")',
        rf'\1{new_title}\2',
        html,
        count=1,
    )
    html = re.sub(
        r'("description":\s*")[^"]*(")',
        r'\1LoveGoBuy ervaringen NL: PostNL, Douane, QC. Merk-spreadsheet → lovegobuyguide.com.\2',
        html,
        count=1,
    )
    # Replace spreadsheet-first lead + keyword block with local + hub uplink
    old_lead_block = (
        '  <p class="lead">Nederlandse zoekers gebruiken lovegobuy spreadsheet en lovegobuy spreadsheets (meervoud). Filter finds op W2CLinks, bestel via Lovegobuy en plan BTW/douane realistisch in.</p>\n'
        '  <div class="od-keyword-article"><h3>Search intent overview for Netherlands</h3><p>Shoppers in Netherlands often combine brand queries (lovegobuy) with product discovery (lovegobuy spreadsheet) and trust questions (is lovegobuy legit / is lovegobuy safe). This guide translates those searches into actions on W2CLinks and Lovegobuy.</p><p>Top regional queries we see in research data include: lovegobuy spreadsheet. Each maps to a guide section on this site rather than a standalone product page.</p><h3>From keyword to action</h3><p>Open <a href="https://w2clinks.com/spreadsheet/lovegobuy/" target="_blank" rel="noopener">W2CLinks spreadsheet</a>, pick a category, copy the source link, and paste into Lovegobuy. Review QC, then read <a href="../lovegobuy-shipping/">shipping guide</a> and <a href="../lovegobuy-coupons/">coupon notes</a> for your parcel.</p></div>'
    )
    new_lead_block = (
        '  <h1>LoveGoBuy ervaringen in Nederland</h1>\n'
        '  <p class="lead">Reviews en hauls voor een Nederlands adres: <strong>PostNL</strong>/DHL last mile, postcode <strong>1234 AB</strong>, <strong>Douane</strong>/BTW. Merk-spreadsheet en dataset → <a href="'
        + HUB
        + '/">lovegobuyguide.com</a>.</p>\n'
        f"  {HUB_UPLINK}\n"
        f"  {LOCAL_ERV}"
    )
    if old_lead_block in html:
        html = html.replace(old_lead_block, new_lead_block, 1)
    elif f'data-nl-deepen="{STAMP}"' not in html:
        # fallback: inject after Landengids h2
        html = html.replace(
            '<h2><span class="od-flag-emoji" aria-hidden="true">🇳🇱</span> Landengids: Netherlands</h2>',
            '<h2><span class="od-flag-emoji" aria-hidden="true">🇳🇱</span> Landengids: Netherlands</h2>\n'
            + new_lead_block,
            1,
        )
    if 'id="postnl-ervaring"' not in html:
        html = html.replace(
            "<h2>Waar ervaringen nuttig zijn</h2>",
            THICKEN_ERV + "\n      <h2>Waar ervaringen nuttig zijn</h2>",
            1,
        )
    # Rewrite spreadsheet-intent card → hub handoff
    html = html.replace(
        "<h2>Wat zoekers met lovegobuy spreadsheet bedoelen</h2>\n"
        "      <p>Gebruikers willen een live W2CLinks-hub met categorie-, merk- en zoekfilters — geen nep-inventaris. Dit partner-resource legt de workflow uit en stuurt elke productactie naar https://w2clinks.com/spreadsheet/lovegobuy/.</p>",
        "<h2>Merk-spreadsheet hoort op de hub</h2>\n"
        "      <p>Zoekers die <em>lovegobuy spreadsheet</em> typen willen de Independent Index / finds / coupons — dat is <a href=\""
        + HUB
        + '/">lovegobuyguide.com</a> (11,300+), niet dit NL-desk. Hier: ervaringen met PostNL, Douane en <code>1234 AB</code>.</p>',
        1,
    )
    html = html.replace(
        "<p>Open het spreadsheet, sorteer op newest, filter categorie of merk, kopieer de bronlink naar Lovegobuy, betaal, wacht op inbound, controleer QC en dien daarna het internationale pakket in.</p>",
        "<p>Shortlist op de hub-catalogus, plak de bronlink in LoveGoBuy, betaal, wacht op inbound, keur QC, boeken daarna een lijn naar Nederland (PostNL/DHL last mile). Coupons: <a href=\""
        + HUB
        + '/lovegobuy-coupon/">hub coupons</a>.</p>',
        1,
    )
    html = html.replace(
        'Browse <a href="https://w2clinks.com/spreadsheet/lovegobuy/" target="_blank" rel="noopener">W2CLinks</a>, registreer met',
        'Shortlist via <a href="' + HUB + '/">lovegobuyguide.com</a>, registreer met',
        1,
    )
    return html


def deepen_coupon(html: str) -> str:
    html = _inject_head_style(html)
    html = _soften_brand(html)
    new_title = "LoveGoBuy coupon Nederland — invite W5RJX3, Douane vs korting"
    html = re.sub(r"<title>.*?</title>", f"<title>{new_title}</title>", html, count=1, flags=re.S)
    html = re.sub(
        r'("name":\s*")Coupon LoveGoBuy 2026 — W5RJX3(")',
        rf'\1{new_title}\2',
        html,
        count=1,
    )
    old_lead_block = (
        '  <p class="lead">Nederlandse zoekers gebruiken lovegobuy spreadsheet en lovegobuy spreadsheets (meervoud). Filter finds op W2CLinks, bestel via Lovegobuy en plan BTW/douane realistisch in.</p>\n'
        '  <div class="od-keyword-article"><h3>Search intent overview for Netherlands</h3><p>Shoppers in Netherlands often combine brand queries (lovegobuy) with product discovery (lovegobuy spreadsheet) and trust questions (is lovegobuy legit / is lovegobuy safe). This guide translates those searches into actions on W2CLinks and Lovegobuy.</p><p>Top regional queries we see in research data include: lovegobuy spreadsheet. Each maps to a guide section on this site rather than a standalone product page.</p><h3>From keyword to action</h3><p>Open <a href="https://w2clinks.com/spreadsheet/lovegobuy/" target="_blank" rel="noopener">W2CLinks spreadsheet</a>, pick a category, copy the source link, and paste into Lovegobuy. Review QC, then read <a href="../lovegobuy-shipping/">shipping guide</a> and <a href="../lovegobuy-coupons/">coupon notes</a> for your parcel.</p></div>'
    )
    new_lead_block = (
        '  <h1>LoveGoBuy coupon voor Nederland</h1>\n'
        '  <p class="lead">Invite <strong>W5RJX3</strong> voor NL-kopers. Coupon ≠ vrijstelling van <strong>Douane</strong>/BTW; last mile vaak <strong>PostNL</strong>. Live coupon-tabel → <a href="'
        + HUB
        + '/lovegobuy-coupon/">hub</a>.</p>\n'
        f"  {HUB_UPLINK}\n"
        f"  {LOCAL_COUPON}"
    )
    if old_lead_block in html:
        html = html.replace(old_lead_block, new_lead_block, 1)
    elif f'data-nl-deepen="{STAMP}"' not in html:
        html = html.replace(
            '<h2><span class="od-flag-emoji" aria-hidden="true">🇳🇱</span> Landengids: Netherlands</h2>',
            '<h2><span class="od-flag-emoji" aria-hidden="true">🇳🇱</span> Landengids: Netherlands</h2>\n'
            + new_lead_block,
            1,
        )
    if 'id="coupon-hub"' not in html:
        html = html.replace(
            "<h2>Lovegobuy coupons &amp; bonus (live)</h2>",
            THICKEN_COUPON + "\n  <h2>Lovegobuy coupons &amp; bonus (live)</h2>",
            1,
        )
    html = html.replace(
        "Shortlist finds op <a href=\"https://w2clinks.com/spreadsheet/lovegobuy/\" target=\"_blank\" rel=\"noopener\">W2CLinks</a>",
        'Shortlist finds op <a href="' + HUB + '/">lovegobuyguide.com</a>',
        1,
    )
    html = html.replace(
        "Shortlist eerst op https://w2clinks.com/spreadsheet/lovegobuy/.",
        f"Shortlist eerst op {HUB}/ (Independent Index).",
        1,
    )
    return html


BUILDERS = {
    "lovegobuy-shipping": deepen_shipping,
    "lovegobuy-ervaringen": deepen_ervaringen,
    "lovegobuy-coupon": deepen_coupon,
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
            "PostNL",
            "1234 AB",
            "Douane",
            f'data-nl-deepen="{STAMP}"',
            "lovegobuyguide.com",
        ):
            if must not in deepened:
                raise SystemExit(f"{slug}: missing {must}")
        if re.search(r"<h1>[^<]*Spreadsheet", deepened, re.I):
            raise SystemExit(f"{slug}: H1 still Spreadsheet hero")
        title_m = re.search(r"<title>(.*?)</title>", deepened, re.S | re.I)
        if title_m and re.search(r"Spreadsheet", title_m.group(1), re.I):
            raise SystemExit(f"{slug}: <title> still Spreadsheet hero")
        dest = OVERLAY / slug / "index.html.nl-deepen"
        dest.write_text(deepened)
        out[slug] = dest
        print("BUILT", dest, "bytes", dest.stat().st_size)
    return out


def deploy(built: dict[str, Path], store_internal: Path | None) -> dict:
    client = _connect()
    bak = f"/www/backup/lovegobuy-nl-deepen-{datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%S')}"
    cmds = [f"mkdir -p '{bak}'"]
    for slug in PAGES:
        cmds.append(
            f"cp -a '{REMOTE}/{slug}/index.html' '{bak}/{slug}-index.html.before' 2>/dev/null || true"
        )
    # refuse accidental hub/IT writes by asserting remote roots exist separately
    cmds.append(
        "test -d /www/wwwroot/lovegobuy.nl && test -d /www/wwwroot/lovegobuyguide.com "
        "&& test -d /www/wwwroot/lovegobuy.it && echo ROOTS_OK"
    )
    print(_run(client, " && ".join(cmds)))

    sftp = client.open_sftp()
    for slug, path in built.items():
        remote = f"{REMOTE}/{slug}/index.html"
        sftp.put(str(path), remote)
        print("PUT", remote)

    try:
        with sftp.open(f"{REMOTE}/sitemap.xml", "r") as fh:
            sm = fh.read().decode(errors="replace")
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
        tmp = f"/tmp/lovegobuy-nl-sitemap-{STAMP}.xml"
        Path(tmp).write_text(sm)
        sftp.put(tmp, f"{REMOTE}/sitemap.xml")
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
    # prove we did not write hub/IT index in this session (mtime check soft)
    untouched = _run(
        client,
        "stat -c '%n %y' /www/wwwroot/lovegobuyguide.com/index.html "
        "/www/wwwroot/lovegobuy.it/index.html 2>/dev/null || true",
    )
    print("UNTOUCHED_HUB_IT", untouched)
    print("BACKUP", bak)
    meta = {"backup": bak, "stamp": STAMP, "pages": list(PAGES), "hub_it_stat": untouched}
    if store_internal:
        store_internal.mkdir(parents=True, exist_ok=True)
        (store_internal / "backup.txt").write_text(bak + "\n")
    client.close()
    return meta


def verify() -> dict:
    checks = []
    for slug in PAGES:
        url = f"https://{HOST}/{slug}/"
        req = Request(url, headers={"User-Agent": "lovegobuy-nl-deepen/1.0"})
        with urlopen(req, timeout=30) as resp:
            body = resp.read().decode(errors="replace")
            code = resp.status
        row = {
            "url": url,
            "http": code,
            "id_local": 'id="local"' in body,
            "hub_uplink": "lovegobuyguide.com" in body and "finds-dataset" in body,
            "postnl": body.count("PostNL"),
            "douane": body.count("Douane"),
            "postcode": body.count("1234 AB"),
            "data_nl_deepen": f'data-nl-deepen="{STAMP}"' in body,
            "spreadsheet_h1": bool(re.search(r"<h1>[^<]*Spreadsheet", body, re.I)),
        }
        m = re.search(r"<title>(.*?)</title>", body, re.S | re.I)
        row["title"] = re.sub(r"\s+", " ", m.group(1)).strip() if m else None
        if m and re.search(r"Spreadsheet", m.group(1), re.I):
            row["spreadsheet_title"] = True
        checks.append(row)

    # home still 200, untouched deepen stamp optional
    req = Request(f"https://{HOST}/", headers={"User-Agent": "lovegobuy-nl-deepen/1.0"})
    with urlopen(req, timeout=30) as resp:
        home = resp.read().decode(errors="replace")
        checks.append(
            {
                "url": f"https://{HOST}/",
                "http": resp.status,
                "postnl": home.count("PostNL"),
                "hub_uplink": "lovegobuyguide.com" in home,
                "data_nl_deepen": f'data-nl-deepen="{STAMP}"' in home,
                "note": "home not rewritten this pass",
            }
        )

    twins = [
        "https://lovegobuyspreadsheet.nl/",
        "https://lovegobuyspreadsheet.it/",
        "https://lovegobuyspreadsheet.eu/",
        "https://lovegobuyspreadsheet.ca/",
        "https://lovegobuyspreadsheet.es/",
    ]
    twin_rows = []
    for t in twins:
        u = urlparse(t)
        conn = http.client.HTTPSConnection(u.netloc, timeout=20)
        conn.request("GET", u.path or "/", headers={"User-Agent": "lovegobuy-nl-deepen/1.0"})
        r = conn.getresponse()
        twin_rows.append({"url": t, "http": r.status, "location": r.getheader("Location")})
        conn.close()

    # hub + IT still 200, not our deepen
    for other in ("https://lovegobuyguide.com/", "https://lovegobuy.it/"):
        u = urlparse(other)
        conn = http.client.HTTPSConnection(u.netloc, timeout=20)
        conn.request("GET", "/", headers={"User-Agent": "lovegobuy-nl-deepen/1.0"})
        r = conn.getresponse()
        body = r.read().decode(errors="replace")
        twin_rows.append(
            {
                "url": other,
                "http": r.status,
                "has_nl_deepen": f'data-nl-deepen="{STAMP}"' in body,
            }
        )
        conn.close()

    return {
        "at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "checks": checks,
        "twins_and_siblings": twin_rows,
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
            if c.get("url", "").startswith(f"https://{HOST}/lovegobuy-")
            and (
                c.get("http") != 200
                or not c.get("id_local")
                or not c.get("hub_uplink")
                or not c.get("data_nl_deepen")
                or c.get("spreadsheet_h1")
                or c.get("spreadsheet_title")
                or not c.get("postnl")
            )
        ]
        twin_expect = {
            "https://lovegobuyspreadsheet.nl/": "lovegobuy.nl",
            "https://lovegobuyspreadsheet.it/": "lovegobuy.it",
            "https://lovegobuyspreadsheet.eu/": "lovegobuyguide.com",
            "https://lovegobuyspreadsheet.ca/": "lovegobuyguide.com",
            "https://lovegobuyspreadsheet.es/": "lovegobuyguide.com",
        }
        twin_bad = []
        for t in ver.get("twins_and_siblings", []):
            url = t.get("url", "")
            if url in twin_expect:
                loc = t.get("location") or ""
                if t.get("http") not in (301, 302) or twin_expect[url] not in loc:
                    twin_bad.append(t)
            elif url in ("https://lovegobuyguide.com/", "https://lovegobuy.it/"):
                if t.get("http") != 200 or t.get("has_nl_deepen"):
                    twin_bad.append(t)
        if bad or twin_bad:
            print("VERIFY_FAIL", bad, twin_bad)
            raise SystemExit(1)
        print("VERIFY_OK")
    if args.gsc:
        if not args.gsc_sa:
            raise SystemExit("--gsc-sa required")
        out = (args.store_internal or Path("/tmp")) / "gsc_sitemap_submit.json"
        if args.store_internal:
            args.store_internal.mkdir(parents=True, exist_ok=True)
        gsc_submit(args.gsc_sa, out)


if __name__ == "__main__":
    main()
