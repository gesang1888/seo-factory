#!/usr/bin/env python3
"""Deepen bbdbuy.it keep desk: Poste / ADM / CAP / IVA + hub uplink.

LIVE only on bbdbuy.it. Does not touch hub (bbdbuyeu.net), CA/UK/US, or revive twins.
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
OVERLAY = ROOT / "sites" / "bbdbuy.it" / "overlay"
HOST = "bbdbuy.it"
REMOTE = f"/www/wwwroot/{HOST}"
STAMP = "20261028"
HUB = "https://bbdbuyeu.net"
TODAY = "2026-10-28"
PAGES = (
    "bbdbuy-qc",
    "bbdbuy-coupons",
    "bbdbuy-shipping",
)

STYLE = (
    f'<style id="it-deepen-{STAMP}">.hub-uplink{{margin:14px 0 0;padding:12px 14px;'
    "border-left:3px solid #0f766e;background:#f0fdfa;color:#134e4a;line-height:1.6;"
    "font-size:15px;max-width:760px}}.hub-uplink a{{color:#0f766e;font-weight:600}}"
    "#local{scroll-margin-top:88px}.local-box{margin:1.25em 0;padding:14px 16px;"
    "border:1px solid #e2e8f0;border-radius:10px;background:#f8fafc}</style>"
)

HUB_UPLINK = (
    f'<p class="hub-uplink" data-it-deepen="{STAMP}" data-step4-hub="1">'
    "Brand spreadsheet / coupons / dataset → "
    f'<a href="{HUB}/">bbdbuyeu.net</a> · '
    f'<a href="{HUB}/bbdbuyeu-coupons/">coupons</a> · '
    f'<a href="{HUB}/finds-dataset/">dataset</a> · '
    f'<a href="{HUB}/bbdbuyeu-spreadsheet/">spreadsheet</a> '
    "(Independent Index · 10,000+). Questa URL = desk Italia "
    "(Poste Italiane / ADM / CAP a cinque cifre / IVA)."
    "</p>"
)

LOCAL_QC = f"""
<section id="local" class="local-box" data-it-fingerprint="qc-poste-adm-cap" data-it-deepen="{STAMP}">
<h2>Fingerprint Italia prima del QC</h2>
<ol>
<li><strong>Destinazione</strong> — stima su <strong>Italia</strong>, non «EU» generica.</li>
<li><strong>Indirizzo</strong> — via italiana + <strong>CAP a cinque cifre</strong> (es. <code>20121</code> Milano).</li>
<li><strong>Last mile</strong> — spesso <strong>Poste Italiane</strong>; il desk non inventa il punto di ritiro.</li>
<li><strong>Dogana / IVA</strong> — SKU + linea decidono. Fonte mattutina: <a href="https://www.adm.gov.it/portale/" rel="noopener" target="_blank">ADM (Agenzia delle Dogane e dei Monopoli)</a>.</li>
</ol>
<p>Spedizione: <a href="/bbdbuy-shipping/">spedire in Italia</a> · Spreadsheet brand: <a href="{HUB}/">bbdbuyeu.net</a>.</p>
</section>
"""

LOCAL_COUPONS = f"""
<section id="local" class="local-box" data-it-fingerprint="coupon-vs-adm-poste" data-it-deepen="{STAMP}">
<h2>Fingerprint Italia: coupon ≠ dogana</h2>
<ol>
<li><strong>Riscatto</strong> — i codici vivono sull’app/sito ufficiale BBDBuy; questo host non incassa.</li>
<li><strong>ADM / IVA</strong> — un coupon non azzera i dazi. Fonte: <a href="https://www.adm.gov.it/portale/" rel="noopener" target="_blank">ADM</a>.</li>
<li><strong>Last mile</strong> — costi <strong>Poste Italiane</strong> seguono peso/volume + linea, non l’invite.</li>
<li><strong>Verità coupon globale</strong> — pack live / Independent Index → <a href="{HUB}/bbdbuyeu-coupons/">bbdbuyeu.net/bbdbuyeu-coupons/</a>.</li>
</ol>
</section>
"""

LOCAL_SHIP = f"""
<section id="local" class="local-box" data-it-fingerprint="poste-adm-cap-iva" data-it-deepen="{STAMP}">
<h2>Fingerprint Italia prima della linea</h2>
<ol>
<li><strong>Destinazione Italia</strong> — preventivo su IT, non EU/DE.</li>
<li><strong>CAP</strong> — cinque cifre (es. <code>20121</code> Milano), non un Packstation DE.</li>
<li><strong>Last mile</strong> — spesso <strong>Poste Italiane</strong>; tracking internazionale → scans nazionali.</li>
<li><strong>ADM / IVA</strong> — <a href="https://www.adm.gov.it/portale/" rel="noopener" target="_blank">ADM</a> + SKU; QC prima di chiudere: <a href="/bbdbuy-qc/">guida QC</a>.</li>
</ol>
</section>
"""

THICKEN_QC = f"""
<h2 id="poste-adm-qc">Poste Italiane, ADM e CAP prima di accettare</h2>
<p>Il QC in magazzino serve a evitare un cartone verso un <strong>CAP italiano</strong> con pezzo sbagliato. Last mile tipico: <strong>Poste Italiane</strong>. Rischio doganale/IVA: <strong>ADM</strong> — un re-QC costa meno di un reso dall’Italia. Brand spreadsheet / dataset restano su <a href="{HUB}/">bbdbuyeu.net</a>; qui solo procedura locale.</p>
<p>Checklist rapida: foto nitide di etichetta/taglia/colore → confronta listing → se dubbio chiedi re-QC → solo dopo chiudi verso Poste. Coupon Italia: <a href="/bbdbuy-coupons/">checklist coupon</a>.</p>
"""

THICKEN_COUPONS = f"""
<h2 id="coupon-hub-it">Coupon sul desk IT vs verità hub</h2>
<p>La checklist locale resta legata a <strong>Poste Italiane</strong> / <strong>ADM</strong> / <strong>CAP</strong> / IVA. I pack coupon live, dataset e brand spreadsheet vivono su <a href="{HUB}/bbdbuyeu-coupons/">bbdbuyeu.net</a> (Independent Index · 10,000+) — questo desk non è un secondo hub. Confronta sempre il freight dopo lo sconto, non solo la percentuale.</p>
"""

THICKEN_SHIP = f"""
<h2 id="poste-adm-cap">Poste Italiane, ADM, CAP e IVA</h2>
<p>Spedire in Italia significa: preventivo su <strong>Italia</strong>, indirizzo con <strong>CAP a cinque cifre</strong>, last mile spesso <strong>Poste Italiane</strong>, e dazi/IVA secondo <strong>ADM</strong> + SKU — nessun eroe Spreadsheet su questa URL. QC prima della linea: <a href="/bbdbuy-qc/">QC BBDBuy</a>. Brand spreadsheet / coupons / dataset → <a href="{HUB}/">bbdbuyeu.net</a>.</p>
<p>Tracking parte internazionale; le scans inland spesso passano da Poste. Se lo stato resta a lungo su dogana: tieni documenti e leggi ADM quel giorno — uno screenshot Discord non è una dichiarazione.</p>
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


def _inject_head_style(html: str) -> str:
    if f'id="it-deepen-{STAMP}"' in html:
        return html
    return html.replace("</head>", STYLE + "\n</head>", 1)


def _soften_shipping_brand(html: str) -> str:
    html = html.replace("<span>Spreadsheet</span>", "<span>Italia</span>", 1)
    html = html.replace("<h3>BBDBuy Spreadsheet</h3>", "<h3>BBDBuy Italia</h3>")
    html = html.replace(
        "&copy; 2026 BBDBuy Spreadsheet.",
        "&copy; 2026 BBDBuy Italia (IT desk).",
    )
    html = re.sub(
        r"(Nota di indipendenza\.</strong>)\s*BBDBuy Spreadsheet è",
        r"\1 bbdbuy.it è il desk Italia (Poste Italiane / ADM / CAP). "
        r"Brand spreadsheet → bbdbuyeu.net. BBDBuy Spreadsheet era",
        html,
        count=1,
    )
    return html


def deepen_qc(html: str) -> str:
    html = _inject_head_style(html)
    html = re.sub(
        r"<title>.*?</title>",
        "<title>QC BBDBuy Italia — Poste Italiane, ADM, CAP | BBDBuy.it</title>",
        html,
        count=1,
        flags=re.S,
    )
    html = re.sub(
        r'property="og:title" content="[^"]*"',
        'property="og:title" content="QC BBDBuy Italia — Poste Italiane, ADM, CAP"',
        html,
        count=1,
    )
    html = html.replace(
        'content="2026-10-26"',
        f'content="{TODAY}"',
    )
    html = html.replace(
        '<div class="eyebrow">bbdbuy.it · QC locale</div>',
        f'<div class="eyebrow">bbdbuy.it · QC · Poste / ADM / CAP · aggiornato {TODAY}</div>',
        1,
    )
    html = html.replace(
        "Aggiornato 2026-10-26 · desk indipendente · platform_opt=bbdbuy-platform-20261026",
        f"Aggiornato {TODAY} · desk IT deepen · data-it-deepen={STAMP}",
        1,
    )
    if f'data-it-deepen="{STAMP}"' not in html or "hub-uplink" not in html:
        html = html.replace(
            "</div></section>\n<article class=\"wrap\">",
            f"</div>\n{HUB_UPLINK}\n</section>\n<article class=\"wrap\">",
            1,
        )
    if 'id="local"' not in html:
        html = html.replace(
            '<article class="wrap">\n'
            "<p>Il QC è il passaggio foto",
            f'<article class="wrap">\n{LOCAL_QC}\n'
            "<p>Il QC è il passaggio foto",
            1,
        )
    if 'id="poste-adm-qc"' not in html:
        html = html.replace(
            "<h2>Catalogo locale vs QC ufficiale</h2>",
            THICKEN_QC + "\n<h2>Catalogo locale vs QC ufficiale</h2>",
            1,
        )
    # strengthen hub handoff for brand spreadsheet
    html = html.replace(
        'Lo spreadsheet globale resta su <a href="https://bbdbuyeu.net/">bbdbuyeu.net</a>.',
        "Lo spreadsheet / dataset / coupons brand restano su "
        f'<a href="{HUB}/">bbdbuyeu.net</a> · '
        f'<a href="{HUB}/finds-dataset/">dataset</a> · '
        f'<a href="{HUB}/bbdbuyeu-spreadsheet/">spreadsheet</a>.',
        1,
    )
    html = html.replace(
        '<nav class="nav"><a href="/">Home</a><a href="/bbdbuy-coupons/">Coupon</a><a href="/is-bbdbuy-legit/">Affidabile?</a></nav>',
        '<nav class="nav"><a href="/">Home</a><a href="/bbdbuy-coupons/">Coupon</a>'
        '<a href="/bbdbuy-shipping/">Spedizione</a><a href="/is-bbdbuy-legit/">Affidabile?</a>'
        f'<a href="{HUB}/">Hub spreadsheet</a></nav>',
        1,
    )
    return html


def deepen_coupons(html: str) -> str:
    html = _inject_head_style(html)
    html = re.sub(
        r"<title>.*?</title>",
        "<title>Coupon BBDBuy Italia — checklist Poste, ADM, CAP | BBDBuy.it</title>",
        html,
        count=1,
        flags=re.S,
    )
    html = re.sub(
        r'property="og:title" content="[^"]*"',
        'property="og:title" content="Coupon BBDBuy Italia — checklist Poste, ADM, CAP"',
        html,
        count=1,
    )
    html = html.replace('content="2026-10-26"', f'content="{TODAY}"')
    html = html.replace(
        '<div class="eyebrow">bbdbuy.it · intent locale IT</div>',
        f'<div class="eyebrow">bbdbuy.it · coupon locale · Poste / ADM · aggiornato {TODAY}</div>',
        1,
    )
    html = html.replace(
        "Aggiornato 2026-10-26 · desk indipendente · platform_opt=bbdbuy-platform-20261026",
        f"Aggiornato {TODAY} · desk IT deepen · data-it-deepen={STAMP}",
        1,
    )
    if "hub-uplink" not in html or f'data-it-deepen="{STAMP}"' not in html:
        html = html.replace(
            "</div></section>\n<article class=\"wrap\">",
            f"</div>\n{HUB_UPLINK}\n</section>\n<article class=\"wrap\">",
            1,
        )
    if 'id="local"' not in html:
        html = html.replace(
            '<article class="wrap">\n'
            "<p>Le query <em>codici coupon bbdbuy</em>",
            f'<article class="wrap">\n{LOCAL_COUPONS}\n'
            "<p>Le query <em>codici coupon bbdbuy</em>",
            1,
        )
    if 'id="coupon-hub-it"' not in html:
        html = html.replace(
            "<h2>Ruolo di bbdbuy.it</h2>",
            THICKEN_COUPONS + "\n<h2>Ruolo di bbdbuy.it</h2>",
            1,
        )
    html = html.replace(
        '<p class="hub">Cerchi lo spreadsheet globale BBDBuy / BBDBuyEU? → '
        '<a href="https://bbdbuyeu.net/">bbdbuyeu.net</a>. Qui restano coupon + dogana italiana.</p>',
        '<p class="hub">Cerchi brand spreadsheet / coupons truth / dataset? → '
        f'<a href="{HUB}/">bbdbuyeu.net</a> · '
        f'<a href="{HUB}/bbdbuyeu-coupons/">coupons</a> · '
        f'<a href="{HUB}/finds-dataset/">dataset</a> · '
        f'<a href="{HUB}/bbdbuyeu-spreadsheet/">spreadsheet</a>. '
        "Qui restano checklist Italia + dogana (ADM/IVA), non un secondo hub.</p>",
        1,
    )
    return html


def deepen_shipping(html: str) -> str:
    html = _inject_head_style(html)
    html = _soften_shipping_brand(html)
    new_title = "Spedizione in Italia — Poste Italiane, ADM, CAP, IVA"
    html = re.sub(
        r"<title>.*?</title>",
        f"<title>{new_title} | BBDBuy.it</title>",
        html,
        count=1,
        flags=re.S,
    )
    html = html.replace(
        '"name": "BBDBuy Spreadsheet in italiano: spedizione e dogana dall’Italia"',
        f'"name": "{new_title}"',
    )
    html = html.replace(
        '"description": "Independent BBDBuy ship for l’Italia."',
        '"description": "Spedizione in Italia: Poste Italiane, ADM, CAP a cinque cifre, IVA. Brand spreadsheet → bbdbuyeu.net."',
    )
    html = re.sub(
        r'<meta name="description" content="[^"]*"',
        '<meta name="description" content="Spedizione BBDBuy verso l’Italia: Poste Italiane, ADM, CAP a cinque cifre, IVA. Brand spreadsheet su bbdbuyeu.net."',
        html,
        count=1,
    )
    lead_old = (
        '<p class="lead">Destinazione Italy — 意大利, non EU. L’indirizzo è una via italiana '
        "e CAP a cinque cifre. Poste Italiane è il corriere locale di riferimento.</p>"
    )
    lead_new = (
        '<p class="lead">Destinazione <strong>Italia</strong> — non EU generica. Indirizzo con '
        "<strong>CAP a cinque cifre</strong> (es. <code>20121</code>). Last mile spesso "
        "<strong>Poste Italiane</strong>; dazi/IVA: <strong>ADM</strong>.</p>\n"
        f"  {HUB_UPLINK}\n"
        f"  {LOCAL_SHIP}"
    )
    if f'data-it-deepen="{STAMP}"' not in html or "hub-uplink" not in html:
        if lead_old in html:
            html = html.replace(lead_old, lead_new, 1)
        else:
            # fallback: inject after first lead
            html = re.sub(
                r'(<p class="lead">.*?</p>)',
                rf"\1\n  {HUB_UPLINK}\n  {LOCAL_SHIP}",
                html,
                count=1,
                flags=re.S,
            )
    if 'id="poste-adm-cap"' not in html:
        html = html.replace(
            "<h2>Il preventivo pubblico era dietro login</h2>",
            THICKEN_SHIP + "\n  <h2>Il preventivo pubblico era dietro login</h2>",
            1,
        )
    # footer CTA: prefer hub for spreadsheet seekers
    html = html.replace(
        '<p><a class="btn" href="https://www.bbdbuy.com/estimation">Sito ufficiale BBDBuy</a> '
        '<a class="btn btn--ghost" href="/aiuto/">Aiuto</a></p>',
        '<p><a class="btn" href="https://www.bbdbuy.com/estimation">Sito ufficiale BBDBuy</a> '
        f'<a class="btn btn--ghost" href="{HUB}/">Hub spreadsheet</a> '
        '<a class="btn btn--ghost" href="/bbdbuy-qc/">QC Italia</a></p>',
        1,
    )
    return html


BUILDERS = {
    "bbdbuy-qc": deepen_qc,
    "bbdbuy-coupons": deepen_coupons,
    "bbdbuy-shipping": deepen_shipping,
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
            "Poste Italiane",
            "ADM",
            f'data-it-deepen="{STAMP}"',
            "bbdbuyeu.net",
            "finds-dataset",
        ):
            if must not in deepened:
                raise SystemExit(f"{slug}: missing {must}")
        if "CAP" not in deepened and "cap" not in deepened.lower():
            raise SystemExit(f"{slug}: missing CAP fingerprint")
        if re.search(r"<h1>[^<]*Spreadsheet", deepened, re.I):
            raise SystemExit(f"{slug}: H1 still Spreadsheet hero")
        title_m = re.search(r"<title>(.*?)</title>", deepened, re.S | re.I)
        if title_m and re.search(r"Spreadsheet", title_m.group(1), re.I):
            raise SystemExit(f"{slug}: <title> still Spreadsheet hero")
        dest = OVERLAY / slug / "index.html.it-deepen"
        dest.write_text(deepened)
        # also refresh deployable index.html for qc/coupons (citation pages)
        if slug in ("bbdbuy-qc", "bbdbuy-coupons"):
            (OVERLAY / slug / "index.html").write_text(deepened)
        out[slug] = dest
        print("BUILT", dest, "bytes", dest.stat().st_size)
    return out


def deploy(built: dict[str, Path], store_internal: Path | None) -> dict:
    client = _connect()
    bak = f"/www/backup/bbdbuy-it-deepen-{datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%S')}"
    cmds = [f"mkdir -p '{bak}'"]
    for slug in PAGES:
        cmds.append(
            f"cp -a '{REMOTE}/{slug}/index.html' '{bak}/{slug}-index.html.before' 2>/dev/null || true"
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
                rf"(<url>\s*<loc>{re.escape(loc)}</loc>\s*)(?:<lastmod>[^<]*</lastmod>\s*)?",
                rf"\1<lastmod>{TODAY}</lastmod>\n",
                sm,
            )
        sm = re.sub(
            rf"(<loc>https://{re.escape(HOST)}/</loc>\s*<lastmod>)[^<]+",
            rf"\g<1>{TODAY}",
            sm,
        )
        tmp = f"/tmp/bbdbuy-it-sitemap-{STAMP}.xml"
        Path(tmp).write_text(sm)
        sftp.put(tmp, f"{REMOTE}/sitemap.xml")
        print("PUT sitemap.xml lastmod", TODAY)
        # keep repo overlay sitemap in sync if present
        local_sm = OVERLAY / "sitemap.xml"
        if local_sm.exists():
            local_sm.write_text(sm)
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
        req = Request(url, headers={"User-Agent": "bbdbuy-it-deepen/1.0"})
        with urlopen(req, timeout=30) as resp:
            body = resp.read().decode(errors="replace")
            code = resp.status
        row = {
            "url": url,
            "http": code,
            "id_local": 'id="local"' in body,
            "hub_uplink": "bbdbuyeu.net" in body and "finds-dataset" in body,
            "poste": body.count("Poste Italiane"),
            "adm": body.count("ADM"),
            "cap": "CAP" in body,
            "data_it_deepen": f'data-it-deepen="{STAMP}"' in body,
            "spreadsheet_h1": bool(re.search(r"<h1>[^<]*Spreadsheet", body, re.I)),
        }
        m = re.search(r"<title>(.*?)</title>", body, re.S | re.I)
        row["title"] = re.sub(r"\s+", " ", m.group(1)).strip() if m else None
        if row["title"] and re.search(r"Spreadsheet", row["title"], re.I):
            row["spreadsheet_title"] = True
        else:
            row["spreadsheet_title"] = False
        checks.append(row)

    # homepage + hub untouched markers
    for url, expect_deepen in (
        (f"https://{HOST}/", False),
        (f"{HUB}/", False),
    ):
        req = Request(url, headers={"User-Agent": "bbdbuy-it-deepen/1.0"})
        with urlopen(req, timeout=30) as resp:
            body = resp.read().decode(errors="replace")
            code = resp.status
        checks.append(
            {
                "url": url,
                "http": code,
                "data_it_deepen": f'data-it-deepen="{STAMP}"' in body,
                "expect_no_it_deepen": expect_deepen is False,
                "untouched_ok": (f'data-it-deepen="{STAMP}"' not in body),
            }
        )

    twins = [
        "https://bbdbuyspreadsheet.ca/",
        "https://bbdbuyspreadsheet.uk/",
        "https://bbdbuyspreadsheet.us/",
        "https://bbdbuyeuspreadsheet.com/",
        "https://bbdbuyspreadsheet.de/",
    ]
    twin_rows = []
    for t in twins:
        u = urlparse(t)
        conn = http.client.HTTPSConnection(u.netloc, timeout=20)
        conn.request("GET", u.path or "/", headers={"User-Agent": "bbdbuy-it-deepen/1.0"})
        r = conn.getresponse()
        twin_rows.append(
            {"url": t, "http": r.status, "location": r.getheader("Location")}
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
            and c["url"].rstrip("/").count("/") >= 3  # money pages only
            and (
                not c.get("id_local")
                or not c.get("hub_uplink")
                or not c.get("data_it_deepen")
                or c.get("spreadsheet_h1")
                or c.get("spreadsheet_title")
                or c.get("http") != 200
            )
        ]
        # home/hub must remain without data-it-deepen
        untouched_bad = [
            c
            for c in ver["checks"]
            if c.get("expect_no_it_deepen") and not c.get("untouched_ok")
        ]
        twin_ok_targets = {
            "https://bbdbuyspreadsheet.ca/": "bbdbuy.ca",
            "https://bbdbuyspreadsheet.uk/": "bbdbuy.uk",
            "https://bbdbuyspreadsheet.us/": "bbdbuy.us",
            "https://bbdbuyeuspreadsheet.com/": "bbdbuyeu.net",
            "https://bbdbuyspreadsheet.de/": "bbdbuyeu.net",
        }
        twin_bad = []
        for t in ver.get("twins", []):
            loc = (t.get("location") or "").lower()
            want = twin_ok_targets.get(t["url"], "")
            if t.get("http") not in (301, 302) or want not in loc:
                twin_bad.append(t)
        if bad or untouched_bad or twin_bad:
            print("VERIFY_FAIL", bad, untouched_bad, twin_bad)
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
