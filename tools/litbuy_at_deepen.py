#!/usr/bin/env python3
"""Deepen litbuy.at keep desk: Zoll / Post AT / 1010 Wien + hub uplink.

LIVE only on litbuy.at. Does not touch hub, CA/IT, or revive twins.
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
OVERLAY = ROOT / "sites" / "litbuy.at" / "overlay"
HOST = "litbuy.at"
REMOTE = f"/www/wwwroot/{HOST}"
STAMP = "20261027"
HUB = "https://litbuyspreadsheet.eu"
PAGES = (
    "zoll-ust-oesterreich",
    "post-at-sendungsverfolgung",
    "litbuy-shipping",
)

STYLE = (
    f'<style id="at-deepen-{STAMP}">.hub-uplink{{margin:14px 0 0;padding:12px 14px;'
    "border-left:3px solid #C49200;background:#fff8df;color:#3f3a1f;line-height:1.6;"
    "font-size:15px;max-width:760px}}.hub-uplink a{{color:#C49200;font-weight:600}}"
    "#local{scroll-margin-top:88px}.local-box{margin:1.25em 0;padding:14px 16px;"
    "border:1px solid #e2e8f0;border-radius:10px;background:#f8fafc}</style>"
)

HUB_UPLINK = (
    f'<p class="hub-uplink" data-at-deepen="{STAMP}" data-step4-hub="1">'
    "Brand / Spreadsheet / Coupons / Dataset → "
    f'<a href="{HUB}/">litbuyspreadsheet.eu</a> · '
    f'<a href="{HUB}/litbuy-coupons/">coupons</a> · '
    f'<a href="{HUB}/finds-dataset/">dataset</a> '
    "(Independent Index · 11,300+). Diese URL = AT lokal (Zoll / Post AT / 1010 Wien)."
    "</p>"
)

LOCAL_ZOLL = f"""
<section id="local" class="local-box" data-at-fingerprint="bmf-zoll-1010-wien" data-at-deepen="{STAMP}">
<h2>AT-Fingerprint vor dem Versand</h2>
<ol>
<li><strong>Schätzer-Ziel: Österreich</strong> — Land AT wählen, nicht DE und nicht „EU“.</li>
<li><strong>Adresse</strong> — österreichische vierstellige PLZ (z.&nbsp;B. <code>1010 Wien</code>).</li>
<li><strong>Last mile</strong> — oft <strong>Post AT</strong> / Österreichische Post; Desk erfindet keinen Servicepunkt.</li>
<li><strong>Abgaben</strong> — SKU entscheidet. Quelle morgens: <a href="https://www.bmf.gv.at/themen/zoll.html" rel="noopener" target="_blank">BMF Zoll</a>.</li>
</ol>
<p>Sendungsverfolgung: <a href="/post-at-sendungsverfolgung/">Post AT Sendungsverfolgung</a> · Versand-Checkliste: <a href="/litbuy-shipping/">Versand nach Österreich</a>.</p>
</section>
"""

LOCAL_POST = f"""
<section id="local" class="local-box" data-at-fingerprint="post-at-sendungsverfolgung-1010" data-at-deepen="{STAMP}">
<h2>AT-Fingerprint für die Sendungsverfolgung</h2>
<ol>
<li><strong>Tracking</strong> — internationale Nummer zuerst; inländisch oft <strong>Post AT Sendungsverfolgung</strong> / Paketverfolgung.</li>
<li><strong>Adresse</strong> — vierstellige PLZ, z.&nbsp;B. <code>1010 Wien</code> (kein DE-Packstationsmuster).</li>
<li><strong>Zoll-Status</strong> — lange „Zoll“-Phase: Dokumente bereithalten; Regeln: <a href="https://www.bmf.gv.at/themen/zoll.html" rel="noopener" target="_blank">BMF Zoll</a>.</li>
<li><strong>Telefon</strong> — AT-Format (+43) korrekt hinterlegen, sonst Zustellversuch scheitert.</li>
</ol>
<p>Abgaben planen: <a href="/zoll-ust-oesterreich/">Zoll &amp; USt Österreich</a>.</p>
</section>
"""

LOCAL_SHIP = f"""
<section id="local" class="local-box" data-at-fingerprint="post-at-bmf-1010-wien" data-at-deepen="{STAMP}">
<h2>AT-Fingerprint vor Linienwahl</h2>
<ol>
<li><strong>Ziel Austria</strong> — Schätzer auf Österreich, nicht DE/EU.</li>
<li><strong>PLZ</strong> — vierstellig, z.&nbsp;B. <code>1010 Wien</code>.</li>
<li><strong>Last mile</strong> — oft <strong>Post AT</strong>; Tracking: <a href="/post-at-sendungsverfolgung/">Sendungsverfolgung</a>.</li>
<li><strong>Zoll / USt</strong> — <a href="/zoll-ust-oesterreich/">Zoll &amp; USt Österreich</a> · Quelle: <a href="https://www.bmf.gv.at/themen/zoll.html" rel="noopener" target="_blank">BMF Zoll</a>.</li>
</ol>
</section>
"""

THICKEN_ZOLL = """
<h2 id="bmf-1010">BMF, 1010 Wien und Post AT</h2>
<p>Dieser Desk erklärt <strong>Zoll &amp; USt Österreich</strong> für eine österreichische Straße — nicht den globalen Spreadsheet-Hero. Die Lieferadresse trägt eine vierstellige PLZ (Beispiel <strong>1010 Wien</strong>). Abgaben folgen der SKU und der Linie; aktuelle Hinweise stehen beim <strong>BMF Zoll</strong>. Die letzte Meile läuft oft über <strong>Post AT</strong> — siehe <a href="/post-at-sendungsverfolgung/">Sendungsverfolgung</a>.</p>
<p>Brand-Spreadsheet / Coupons / Dataset bleiben auf dem Hub <a href="https://litbuyspreadsheet.eu/">litbuyspreadsheet.eu</a>. Hier: lokale Kosten und Zustellung.</p>
"""

THICKEN_POST = """
<h2 id="paketverfolgung">Paketverfolgung und Statuscodes</h2>
<p><strong>Post AT Sendungsverfolgung</strong> zeigt Export, EU-Eingang und inländische Zustellung. Zwischen Label-Druck und erstem Scan kann es Lücken geben — das ist normal. Bleibt der Status lange auf „Zoll“, prüfen Sie Deklaration und Fristen (SMS/Brief), bevor Rücksendung droht.</p>
<p>Adresse mit <strong>1010 Wien</strong>-Muster (vierstellige PLZ) und +43-Telefon; Abgaben-Kontext: <a href="/zoll-ust-oesterreich/">Zoll &amp; USt</a> und <a href="https://www.bmf.gv.at/themen/zoll.html" rel="noopener" target="_blank">BMF</a>.</p>
"""

THICKEN_SHIP = """
<h2 id="post-at-zoll">Post AT, BMF Zoll, 1010 Wien</h2>
<p>Versand nach Österreich heißt: Schätzer-Ziel <strong>AT</strong>, Adresse mit vierstelliger PLZ (z.&nbsp;B. <strong>1010 Wien</strong>), oft <strong>Post AT</strong> als Last-Mile, und Abgaben nach <strong>BMF Zoll</strong> / SKU — kein Spreadsheet-Hero auf dieser URL. Tracking: <a href="/post-at-sendungsverfolgung/">Post AT Sendungsverfolgung</a>. Zoll-Rechnung: <a href="/zoll-ust-oesterreich/">Zoll &amp; USt Österreich</a>.</p>
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
        '<span>Österreich</span>',
        1,
    )
    html = re.sub(
        r"<h3>LitBuy Spreadsheet</h3>",
        "<h3>LitBuy Österreich</h3>",
        html,
        count=1,
    )
    html = re.sub(
        r"(Unabhängigkeitshinweis\.</strong>)\s*LitBuy Spreadsheet ist",
        r"\1 litbuy.at ist der AT-Desk (BMF Zoll / Post AT / 1010 Wien). Brand-Spreadsheet → litbuyspreadsheet.eu. LitBuy Spreadsheet war",
        html,
        count=1,
    )
    # Prefer AT desk wording in footer independence when still Spreadsheet-hero
    html = html.replace(
        "og:site_name\" content=\"Litbuy Spreadsheet Österreich\"",
        "og:site_name\" content=\"LitBuy Österreich\"",
    )
    html = html.replace(
        '"name": "Litbuy Spreadsheet Österreich"',
        '"name": "LitBuy Österreich"',
    )
    return html


def _inject_head_style(html: str) -> str:
    if f'id="at-deepen-{STAMP}"' in html:
        return html
    return html.replace(
        "</head>",
        STYLE + "\n</head>",
        1,
    )


def _bump_dates(html: str) -> str:
    html = html.replace('"dateModified": "2026-05-31"', '"dateModified": "2026-10-27"')
    return html


def deepen_zoll(html: str) -> str:
    html = _inject_head_style(html)
    html = _soften_brand(html)
    html = _bump_dates(html)
    # title stays Zoll-focused; tighten description
    html = re.sub(
        r"<title>.*?</title>",
        "<title>Zoll &amp; USt Österreich – BMF, Post AT, 1010 Wien | LitBuy</title>",
        html,
        count=1,
        flags=re.S,
    )
    html = re.sub(
        r'property="og:title" content="[^"]*"',
        'property="og:title" content="Zoll &amp; USt Österreich – BMF, Post AT, 1010 Wien"',
        html,
        count=1,
    )
    # eyebrow + hub uplink under intro
    html = html.replace(
        '<span class="eu-badge">Exclusive · litbuy.at</span>',
        '<span class="eu-badge">Zoll / BMF / 1010 Wien · aktualisiert 27.10.2026</span>',
        1,
    )
    if f'data-at-deepen="{STAMP}"' not in html:
        html = html.replace(
            '<p class="intro" style="margin-top:12px;font-size:14px;color:#6B7280">'
            "<em>Veröffentlicht am 31.05.2026 · Kein Äquivalent auf litbuyspreadsheet.eu</em></p>\n"
            "</div></section>",
            '<p class="intro" style="margin-top:12px;font-size:14px;color:#6B7280">'
            "<em>Aktualisiert 27.10.2026 · lokaler AT-Desk, kein zweites Brand-Hub</em></p>\n"
            f"{HUB_UPLINK}\n"
            "</div></section>",
            1,
        )
    if 'id="local"' not in html:
        html = html.replace(
            '<article class="article-content article-long">\n\n'
            "<h2>Unterschied zum englischen EU-Hub</h2>",
            '<article class="article-content article-long">\n'
            f"{LOCAL_ZOLL}\n"
            "<h2>Unterschied zum englischen EU-Hub</h2>",
            1,
        )
    if 'id="bmf-1010"' not in html:
        html = html.replace(
            "<h2>Offizielle Quellen</h2>",
            THICKEN_ZOLL + "\n<h2>Offizielle Quellen</h2>",
            1,
        )
    # sidebar hub dataset
    html = html.replace(
        '<div class="sidebar-card"><h4>Litbuy</h4><ul><li><a href="/litbuy-spreadsheet/">Spreadsheet</a></li>'
        '<li><a href="/litbuy-coupons/">Coupons</a></li></ul></div>',
        '<div class="sidebar-card"><h4>Hub (Brand)</h4><ul>'
        f'<li><a href="{HUB}/">litbuyspreadsheet.eu</a></li>'
        f'<li><a href="{HUB}/litbuy-coupons/">Coupons</a></li>'
        f'<li><a href="{HUB}/finds-dataset/">Dataset</a></li>'
        "</ul></div>",
        1,
    )
    html = html.replace(
        "Siehe auch <a href=\"/post-at-sendungsverfolgung/\">Post AT Sendungsverfolgung</a> und <a href=\"/litbuy-coupons/\">Coupons</a>.",
        "Siehe auch <a href=\"/post-at-sendungsverfolgung/\">Post AT Sendungsverfolgung</a>, "
        "<a href=\"/litbuy-shipping/\">Versand</a> und Hub-"
        f'<a href="{HUB}/litbuy-coupons/">Coupons</a>.',
        1,
    )
    return html


def deepen_post(html: str) -> str:
    html = _inject_head_style(html)
    html = _soften_brand(html)
    html = _bump_dates(html)
    html = re.sub(
        r"<title>.*?</title>",
        "<title>Post AT Sendungsverfolgung – Paketverfolgung, 1010 Wien | LitBuy</title>",
        html,
        count=1,
        flags=re.S,
    )
    html = re.sub(
        r'property="og:title" content="[^"]*"',
        'property="og:title" content="Post AT Sendungsverfolgung – Paketverfolgung, 1010 Wien"',
        html,
        count=1,
    )
    html = html.replace(
        '<span class="eu-badge">Exclusive · litbuy.at</span>',
        '<span class="eu-badge">Post AT · Sendungsverfolgung · aktualisiert 27.10.2026</span>',
        1,
    )
    html = html.replace(
        "Dieser Artikel existiert nicht auf litbuyspreadsheetnow.com. Fokus: <strong>Post AT</strong> und letzte Meile in Österreich.",
        "Fokus: <strong>Post AT</strong> und letzte Meile in Österreich. Brand-Spreadsheet → "
        f'<a href="{HUB}/">litbuyspreadsheet.eu</a> (kein Twin-Hub).',
        1,
    )
    if f'data-at-deepen="{STAMP}"' not in html:
        html = html.replace(
            '<p class="intro" style="margin-top:12px;font-size:14px;color:#6B7280">'
            "<em>Veröffentlicht am 31.05.2026 · Kein Äquivalent auf litbuyspreadsheet.eu</em></p>\n"
            "</div></section>",
            '<p class="intro" style="margin-top:12px;font-size:14px;color:#6B7280">'
            "<em>Aktualisiert 27.10.2026 · lokaler AT-Desk</em></p>\n"
            f"{HUB_UPLINK}\n"
            "</div></section>",
            1,
        )
    if 'id="local"' not in html:
        html = html.replace(
            '<article class="article-content article-long">\n\n'
            "<h2>Nur für litbuy.at</h2>",
            '<article class="article-content article-long">\n'
            f"{LOCAL_POST}\n"
            "<h2>Nur für litbuy.at</h2>",
            1,
        )
    if 'id="paketverfolgung"' not in html:
        html = html.replace(
            "<h2>Verknüpfung mit Spreadsheet-Kauf</h2>",
            THICKEN_POST + "\n<h2>Verknüpfung mit Spreadsheet-Kauf</h2>",
            1,
        )
    html = html.replace(
        '<div class="sidebar-card"><h4>Litbuy</h4><ul><li><a href="/litbuy-spreadsheet/">Spreadsheet</a></li>'
        '<li><a href="/litbuy-coupons/">Coupons</a></li></ul></div>',
        '<div class="sidebar-card"><h4>Hub (Brand)</h4><ul>'
        f'<li><a href="{HUB}/">litbuyspreadsheet.eu</a></li>'
        f'<li><a href="{HUB}/litbuy-coupons/">Coupons</a></li>'
        f'<li><a href="{HUB}/finds-dataset/">Dataset</a></li>'
        "</ul></div>",
        1,
    )
    return html


def deepen_shipping(html: str) -> str:
    html = _inject_head_style(html)
    html = _soften_brand(html)
    new_title = "Versand nach Österreich — Post AT, BMF Zoll, 1010 Wien"
    html = re.sub(
        r"<title>.*?</title>",
        f"<title>{new_title}</title>",
        html,
        count=1,
        flags=re.S,
    )
    html = html.replace(
        '"name": "LitBuy Spreadsheet auf Deutsch: Versand und Zoll aus Österreich"',
        f'"name": "{new_title}"',
    )
    html = html.replace(
        '"description": "Independent LitBuy ship for Österreich."',
        '"description": "Versand nach Österreich: Post AT, BMF Zoll, PLZ 1010 Wien. Brand-Spreadsheet → litbuyspreadsheet.eu."',
    )
    # lead already has 1010 Wien; inject hub + local after lead
    # Note: STYLE CSS mentions .hub-uplink — check data-at-deepen, not the class name alone.
    if f'data-at-deepen="{STAMP}"' not in html:
        html = html.replace(
            '<p class="lead">Ziel Austria — 奥地利, nicht EU und nicht DE. Die Lieferadresse ist eine österreichische PLZ (z. B. 1010 Wien).</p>',
            '<p class="lead">Ziel Austria — nicht EU und nicht DE. Lieferadresse: österreichische PLZ (z.&nbsp;B. <strong>1010 Wien</strong>). Last mile oft <strong>Post AT</strong>; Abgaben: <strong>BMF Zoll</strong>.</p>\n'
            f"  {HUB_UPLINK}\n"
            f"  {LOCAL_SHIP}",
            1,
        )
    if 'id="post-at-zoll"' not in html:
        html = html.replace(
            "<h2>Der öffentliche Schätzer war hinter Login</h2>",
            THICKEN_SHIP + "\n  <h2>Der öffentliche Schätzer war hinter Login</h2>",
            1,
        )
    html = html.replace(
        "<h3>LitBuy Spreadsheet</h3>",
        "<h3>LitBuy Österreich</h3>",
    )
    html = html.replace(
        "&copy; 2026 LitBuy Spreadsheet.",
        "&copy; 2026 LitBuy Österreich (AT desk).",
    )
    html = re.sub(
        r"(Unabhängigkeitshinweis\.</strong>)\s*LitBuy Spreadsheet ist",
        r"\1 litbuy.at ist der AT-Desk (Post AT / BMF Zoll / 1010 Wien). Brand-Spreadsheet → litbuyspreadsheet.eu. Dieser Text war",
        html,
        count=1,
    )
    return html


BUILDERS = {
    "zoll-ust-oesterreich": deepen_zoll,
    "post-at-sendungsverfolgung": deepen_post,
    "litbuy-shipping": deepen_shipping,
}


def build() -> dict[str, Path]:
    out: dict[str, Path] = {}
    for slug in PAGES:
        base = OVERLAY / slug / "live-base.index.html"
        if not base.exists():
            raise SystemExit(f"missing live base: {base}")
        deepened = BUILDERS[slug](base.read_text(errors="replace"))
        # sanity
        for must in ('id="local"', 'class="hub-uplink"', "1010 Wien", f'data-at-deepen="{STAMP}"'):
            if must not in deepened:
                raise SystemExit(f"{slug}: missing {must}")
        if slug != "litbuy-shipping":
            for must in ("BMF", "Post AT"):
                if must not in deepened:
                    raise SystemExit(f"{slug}: missing {must}")
        else:
            if "Post AT" not in deepened or "BMF Zoll" not in deepened:
                raise SystemExit(f"{slug}: missing Post AT / BMF Zoll")
        if re.search(r"<h1>[^<]*Spreadsheet", deepened, re.I):
            raise SystemExit(f"{slug}: H1 still Spreadsheet hero")
        title_m = re.search(r"<title>(.*?)</title>", deepened, re.S | re.I)
        if title_m and re.search(r"Spreadsheet", title_m.group(1), re.I):
            raise SystemExit(f"{slug}: <title> still Spreadsheet hero")
        dest = OVERLAY / slug / "index.html.at-deepen"
        dest.write_text(deepened)
        out[slug] = dest
        print("BUILT", dest, "bytes", dest.stat().st_size)
    return out


def deploy(built: dict[str, Path], store_internal: Path | None) -> dict:
    client = _connect()
    bak = f"/www/backup/litbuy-at-deepen-{datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%S')}"
    cmds = [
        f"mkdir -p '{bak}'",
    ]
    for slug in PAGES:
        cmds.append(f"cp -a '{REMOTE}/{slug}/index.html' '{bak}/{slug}-index.html.before' 2>/dev/null || true")
    print(_run(client, " && ".join(cmds)))

    sftp = client.open_sftp()
    for slug, path in built.items():
        remote = f"{REMOTE}/{slug}/index.html"
        sftp.put(str(path), remote)
        print("PUT", remote)
    # bump sitemap lastmod for money URLs
    try:
        with sftp.open(f"{REMOTE}/sitemap.xml", "r") as fh:
            sm = fh.read().decode(errors="replace")
        today = "2026-10-27"
        for slug in PAGES:
            loc = f"https://{HOST}/{slug}/"
            sm = re.sub(
                rf"(<loc>{re.escape(loc)}</loc>\s*<lastmod>)[^<]+",
                rf"\g<1>{today}",
                sm,
            )
            # also if lastmod precedes other tags order differs — rewrite block
            sm = re.sub(
                rf"(<url>\s*<loc>{re.escape(loc)}</loc>\s*)(?:<lastmod>[^<]*</lastmod>\s*)?",
                rf"\1<lastmod>{today}</lastmod>\n",
                sm,
            )
        # homepage too lightly
        sm = re.sub(
            rf"(<loc>https://{re.escape(HOST)}/</loc>\s*<lastmod>)[^<]+",
            rf"\g<1>{today}",
            sm,
        )
        tmp = f"/tmp/litbuy-at-sitemap-{STAMP}.xml"
        Path(tmp).write_text(sm)
        sftp.put(tmp, f"{REMOTE}/sitemap.xml")
        print("PUT sitemap.xml lastmod", today)
    except Exception as exc:  # noqa: BLE001
        print("SITEMAP_WARN", exc)
    sftp.close()

    # chown
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
    twins = [
        "https://litbuyspreadsheetnow.com/",
        "https://litbuyspreadsheets.es/",
        "https://litbuyspreadsheets.us/",
        "https://litbuyspreadsheet.me.uk/",
        "https://litbuyspreadsheets.nl/",
        "https://litspreadsheet.fr/",
    ]
    for slug in PAGES:
        url = f"https://{HOST}/{slug}/"
        req = Request(url, headers={"User-Agent": "litbuy-at-deepen/1.0"})
        with urlopen(req, timeout=30) as resp:
            body = resp.read().decode(errors="replace")
            code = resp.status
        row = {
            "url": url,
            "http": code,
            "id_local": 'id="local"' in body,
            "hub_uplink": "litbuyspreadsheet.eu" in body and "finds-dataset" in body,
            "wien_1010": body.count("1010 Wien"),
            "post_at": body.lower().count("post at"),
            "bmf": body.count("BMF"),
            "data_at_deepen": f'data-at-deepen="{STAMP}"' in body,
            "spreadsheet_h1": bool(re.search(r"<h1>[^<]*Spreadsheet", body, re.I)),
        }
        m = re.search(r"<title>(.*?)</title>", body, re.S | re.I)
        row["title"] = re.sub(r"\s+", " ", m.group(1)).strip() if m else None
        checks.append(row)
    for t in twins:
        req = Request(t, headers={"User-Agent": "litbuy-at-deepen/1.0"}, method="GET")
        try:
            with urlopen(req, timeout=20) as resp:
                checks.append({"url": t, "http": resp.status, "location": resp.geturl()})
        except Exception as exc:  # noqa: BLE001
            # urllib follows redirects; 301 final may be 200 on hub
            loc = getattr(exc, "headers", None)
            checks.append({"url": t, "error": str(exc)[:120]})
    # explicit no-follow twin check via curl-like: use http.client
    import http.client
    from urllib.parse import urlparse

    twin_rows = []
    for t in twins:
        u = urlparse(t)
        conn = http.client.HTTPSConnection(u.netloc, timeout=20)
        conn.request("GET", u.path or "/", headers={"User-Agent": "litbuy-at-deepen/1.0"})
        r = conn.getresponse()
        twin_rows.append(
            {
                "url": t,
                "http": r.status,
                "location": r.getheader("Location"),
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
    ap.add_argument(
        "--store-internal",
        type=Path,
        default=None,
        help="Project store internal/litbuy-at-deepen",
    )
    ap.add_argument(
        "--gsc-sa",
        type=Path,
        default=None,
    )
    args = ap.parse_args()
    if args.load_env:
        _load_env(args.load_env)
    built = build()
    if args.build_only and not args.deploy:
        return
    meta = {}
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
            and (
                not c.get("id_local")
                or not c.get("hub_uplink")
                or not c.get("data_at_deepen")
                or c.get("spreadsheet_h1")
                or c.get("http") != 200
            )
        ]
        twin_bad = [
            t
            for t in ver.get("twins", [])
            if t.get("http") not in (301, 302)
            or not (t.get("location") or "").startswith(HUB)
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
