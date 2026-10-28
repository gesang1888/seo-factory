#!/usr/bin/env python3
"""Deepen cssbuy.es keep desk: Correos / AEAT / CP5 + hub uplink.

LIVE only on cssbuy.es. Does not touch hub cssbuyspreadsheet.eu, other desks,
or revive Phase C / spreadsheet twins.
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
OVERLAY = ROOT / "sites" / "cssbuy.es" / "overlay"
HOST = "cssbuy.es"
REMOTE = f"/www/wwwroot/{HOST}"
STAMP = "20261028"
HUB = "https://cssbuyspreadsheet.eu"
PAGES = (
    "cssbuy-shipping",
    "cssbuy-coupons",
    "how-to-use-cssbuy",
)

STYLE = (
    f'<style id="es-deepen-{STAMP}">'
    ".hub-uplink{margin:14px 0 0;padding:12px 14px;"
    "border-left:3px solid #00C853;background:#e8f8ee;color:#1f3d2a;line-height:1.6;"
    "font-size:15px;max-width:760px}.hub-uplink a{color:#009E44;font-weight:600}"
    "#local{scroll-margin-top:88px}.local-box{margin:1.25em 0;padding:14px 16px;"
    "border:1px solid #eaecf0;border-radius:12px;background:#f5f6f7}</style>"
)

HUB_UPLINK = (
    f'<p class="hub-uplink" data-es-deepen="{STAMP}" data-step4-hub="1">'
    "¿Buscas el spreadsheet / coupons / dataset global de CSSBuy? Usa "
    f'<a href="{HUB}/">cssbuyspreadsheet.eu</a> · '
    f'<a href="{HUB}/cssbuy-coupons/">coupons</a> · '
    f'<a href="{HUB}/finds-dataset/">dataset</a> '
    "(Independent Index · 11,300+). Aquí: Correos, AEAT y dirección en España."
    "</p>"
)

LOCAL_SHIP = f"""
<section id="local" class="local-box" data-es-fingerprint="correos-aeat-cp5" data-es-deepen="{STAMP}">
<h2>Huella ES antes de elegir línea</h2>
<ol>
<li><strong>Destino del estimador: España</strong> — elige Spain / España, no «EU» ni este TLD.</li>
<li><strong>Dirección</strong> — calle española y <strong>código postal de cinco dígitos</strong> (no CAP italiano ni code postal francés).</li>
<li><strong>Última milla</strong> — a menudo <strong>Correos</strong>; el desk no inventa un punto Collect.</li>
<li><strong>Aranceles / IVA</strong> — lo dice la SKU. Fuente: <a href="https://sede.agenciatributaria.gob.es/" rel="noopener" target="_blank">AEAT / Agencia Tributaria</a>. Sin valor declarado inventado.</li>
</ol>
<p>Cupones locales: <a href="/cssbuy-coupons/">/cssbuy-coupons</a> · Primer pedido: <a href="/how-to-use-cssbuy/">guía</a>.</p>
</section>
"""

LOCAL_COUPONS = f"""
<section id="local" class="local-box" data-es-fingerprint="cupon-no-es-aduana" data-es-deepen="{STAMP}">
<h2>Cupón ES ≠ aduana</h2>
<ol>
<li><strong>Cupón / invite</strong> — se aplica en <a href="https://www.cssbuy.com/" rel="nofollow noopener" target="_blank">cssbuy.com</a> tras login; este desk no imprime códigos inventados.</li>
<li><strong>Pack de verdad (global)</strong> — fechas y invite en hub <a href="{HUB}/cssbuy-coupons/">cssbuyspreadsheet.eu/cssbuy-coupons</a> + <a href="{HUB}/finds-dataset/">dataset</a>.</li>
<li><strong>Dirección</strong> — sigue siendo calle española + CP de cinco dígitos; el cupón no cambia Correos ni AEAT.</li>
<li><strong>Aranceles</strong> — IVA / tasas Collect las marca la SKU y la <a href="https://sede.agenciatributaria.gob.es/" rel="noopener" target="_blank">AEAT</a>, no el código de descuento.</li>
</ol>
<p>Envío ES: <a href="/cssbuy-shipping/">Correos / AEAT</a>.</p>
</section>
"""

LOCAL_FIRST = f"""
<section id="local" class="local-box" data-es-fingerprint="primer-pedido-correos-aeat" data-es-deepen="{STAMP}">
<h2>Primer pedido: huella España</h2>
<ol>
<li><strong>Estimador</strong> — destino <strong>España</strong> (Spain), no EU genérico.</li>
<li><strong>Dirección</strong> — calle española + <strong>código postal de cinco dígitos</strong>.</li>
<li><strong>QC → consolidar → línea</strong> — fotos en almacén antes de pagar el flete; última milla a menudo <strong>Correos</strong>.</li>
<li><strong>Aduanas</strong> — declara según SKU; lee <a href="https://sede.agenciatributaria.gob.es/" rel="noopener" target="_blank">AEAT</a> el día del envío. Sin infradeclaración.</li>
</ol>
<p>Detalle envío: <a href="/cssbuy-shipping/">/cssbuy-shipping</a> · Cupones: <a href="/cssbuy-coupons/">/cssbuy-coupons</a>.</p>
</section>
"""

THICKEN_SHIP = """
<h2 id="correos-aeat">Correos, AEAT y código postal</h2>
<p>Enviar a España en este desk significa: estimador en <strong>España</strong>, dirección con <strong>código postal de cinco dígitos</strong>, última milla a menudo <strong>Correos</strong> (posible tasa Collect), y aranceles/IVA según la SKU y la <strong>Agencia Tributaria (AEAT)</strong> — no un héroe «CSSBuy Spreadsheet». Fuente oficial: <a href="https://sede.agenciatributaria.gob.es/" rel="noopener" target="_blank">sede.agenciatributaria.gob.es</a>.</p>
<p>El catálogo global / Independent Index / coupons truth viven en el hub <a href="https://cssbuyspreadsheet.eu/">cssbuyspreadsheet.eu</a>. Esta URL solo aclara el tramo ES.</p>
"""

THICKEN_COUPONS = """
<h2 id="cupon-checklist-es">Checklist cupón hacia España</h2>
<p>Antes de pegar un invite: (1) confirma el código <em>in-app</em> el mismo día; (2) elige destino España en el estimador; (3) revisa que la dirección lleve CP de cinco dígitos; (4) no confundes descuento con despacho de <strong>Correos</strong> ni con IVA de la <strong>AEAT</strong>.</p>
<p>La tabla de verdad de cupones y el dataset (11,300+) están en el hub — <a href="https://cssbuyspreadsheet.eu/cssbuy-coupons/">coupons</a> · <a href="https://cssbuyspreadsheet.eu/finds-dataset/">dataset</a> — no en el título de este desk.</p>
"""

THICKEN_FIRST = """
<h2 id="primer-pedido-es">Dirección ES, Correos y AEAT en el primer haul</h2>
<p>El primer pedido desde España no necesita un héroe Spreadsheet: copia el enlace, paga en la app oficial, espera QC, consolida y elige línea con destino <strong>España</strong>. La dirección es calle española + CP de cinco dígitos; el tracking doméstico suele pasar por <strong>Correos</strong>; las reglas de entrada las marca la <strong>AEAT</strong>.</p>
<p>Si buscas el índice global o coupons truth, sube al hub <a href="https://cssbuyspreadsheet.eu/">cssbuyspreadsheet.eu</a>. Aquí: checklist local del primer pedido.</p>
"""


def _load_env(path: Path) -> None:
    text = path.read_text()
    host = pass_val = None
    for line in text.splitlines():
        if line.startswith("HOST="):
            host = line.split("=", 1)[1].strip().strip('"').strip("'")
        if line.startswith("RAW_LINE="):
            raw = line.split("=", 1)[1]
            # Keep leading semicolon; strip only matching outer quotes if present.
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
    html = html.replace("<span>Spreadsheet</span>", "<span>España</span>", 1)
    html = html.replace("<h3>CSSBuy Spreadsheet</h3>", "<h3>CSSBuy España</h3>", 1)
    html = html.replace(
        "Spreadsheet y categorías",
        "Catálogo y categorías",
    )
    html = html.replace(
        "<strong>Aviso de independencia.</strong> CSSBuy Spreadsheet es un sitio informativo independiente.",
        "<strong>Aviso de independencia.</strong> cssbuy.es es el desk ES (Correos / AEAT / CP cinco dígitos). "
        "Brand spreadsheet → cssbuyspreadsheet.eu. Este sitio es informativo e independiente.",
        1,
    )
    html = html.replace(
        "&copy; 2026 CSSBuy Spreadsheet.",
        "&copy; 2026 CSSBuy España (desk ES).",
        1,
    )
    return html


def _inject_head_style(html: str) -> str:
    if f'id="es-deepen-{STAMP}"' in html:
        return html
    return html.replace("</head>", STYLE + "\n</head>", 1)


def _set_title_desc(html: str, title: str, desc: str) -> str:
    html = re.sub(r"<title>.*?</title>", f"<title>{title}</title>", html, count=1, flags=re.S)
    html = re.sub(
        r'<meta name="description" content="[^"]*"',
        f'<meta name="description" content="{desc}"',
        html,
        count=1,
    )
    # JSON-LD WebPage name/description
    html = re.sub(
        r'("name":\s*")CSSBuy Spreadsheet en español:[^"]*"',
        rf'\1{title}"',
        html,
        count=1,
    )
    html = re.sub(
        r'("description":\s*")Independent CSSBuy [^"]*"',
        rf'\1{desc}"',
        html,
        count=2,
    )
    return html


def deepen_shipping(html: str) -> str:
    html = _inject_head_style(html)
    html = _soften_brand(html)
    title = "Envío a España — Correos, AEAT, código postal | CSSBuy"
    desc = (
        "Envío CSSBuy a España: estimador Spain, Correos, AEAT y CP de cinco dígitos. "
        "Brand spreadsheet → cssbuyspreadsheet.eu."
    )
    html = _set_title_desc(html, title, desc)
    html = html.replace(
        '<span class="eyebrow" style="color:var(--acd)">Envío</span>',
        '<span class="eyebrow" style="color:var(--acd)">Envío · Correos / AEAT · actualizado 28 Oct 2026</span>',
        1,
    )
    if f'data-es-deepen="{STAMP}"' not in html:
        html = html.replace(
            '<p class="lead">Destino Spain — 西班牙, no EU. La dirección es una calle española y código postal de cinco dígitos. no copiamos un recuento de líneas.</p>',
            '<p class="lead">Destino <strong>España</strong> (Spain), no EU. Calle española + <strong>código postal de cinco dígitos</strong>; última milla a menudo <strong>Correos</strong>; aranceles según <strong>AEAT</strong>.</p>\n'
            f"  {HUB_UPLINK}\n"
            f"  {LOCAL_SHIP}",
            1,
        )
    if 'id="correos-aeat"' not in html:
        html = html.replace(
            "<h2>El estimador público estaba detrás de login</h2>",
            THICKEN_SHIP + "\n  <h2>El estimador público estaba detrás de login</h2>",
            1,
        )
    html = html.replace(
        '<p><a class="btn" href="https://www.cssbuy.com/?action=estimates&amp;go=page">Sitio oficial CSSBuy</a> <a class="btn btn--ghost" href="/ayuda/">Ayuda</a></p>',
        '<p><a class="btn" href="https://www.cssbuy.com/?action=estimates&amp;go=page">Sitio oficial CSSBuy</a> '
        '<a class="btn btn--ghost" href="/how-to-use-cssbuy/">Primer pedido</a> '
        f'<a class="btn btn--ghost" href="{HUB}/finds-dataset/">Dataset hub</a></p>',
        1,
    )
    return html


def deepen_coupons(html: str) -> str:
    html = _inject_head_style(html)
    html = _soften_brand(html)
    title = "Cupones CSSBuy España — checklist Correos, AEAT | CSSBuy"
    desc = (
        "Cupones CSSBuy hacia España: el código no sustituye Correos ni AEAT. "
        "Pack de verdad en cssbuyspreadsheet.eu."
    )
    html = _set_title_desc(html, title, desc)
    html = html.replace(
        '<span class="eyebrow" style="color:var(--acd)">Códigos</span>',
        '<span class="eyebrow" style="color:var(--acd)">Cupones ES · Correos / AEAT · 28 Oct 2026</span>',
        1,
    )
    html = re.sub(
        r"<h1>Cupones: no en el título de este dest</h1>",
        "<h1>Cupones CSSBuy hacia España (no es aduana)</h1>",
        html,
        count=1,
    )
    if f'data-es-deepen="{STAMP}"' not in html:
        html = html.replace(
            '<p class="lead">Este dest no imprime códigos de invitación en el título ni en la portada. Si CSSBuy publica un código, está después del login en https://www.cssbuy.com/.</p>',
            '<p class="lead">Este desk no imprime códigos inventados en el título. Si hay invite, se aplica tras login en cssbuy.com. El cupón <strong>no</strong> sustituye a <strong>Correos</strong> ni a la <strong>AEAT</strong>.</p>\n'
            f"  {HUB_UPLINK}\n"
            f"  {LOCAL_COUPONS}",
            1,
        )
    if 'id="cupon-checklist-es"' not in html:
        html = html.replace(
            "<p>La dirección sigue siendo una calle española y código postal de cinco dígitos. no copiamos un recuento de líneas. Destino en el estimador: Spain — 西班牙.</p>",
            THICKEN_COUPONS
            + "\n  <p>La dirección sigue siendo calle española + CP de cinco dígitos. Destino del estimador: <strong>España</strong>.</p>",
            1,
        )
    html = html.replace(
        '<p><a class="btn" href="https://www.cssbuy.com/">Sitio oficial</a> <a class="btn btn--ghost" href="/catalogo/">Catálogo</a></p>',
        '<p><a class="btn" href="https://www.cssbuy.com/">Sitio oficial</a> '
        f'<a class="btn btn--ghost" href="{HUB}/cssbuy-coupons/">Coupons hub</a> '
        '<a class="btn btn--ghost" href="/cssbuy-shipping/">Envío ES</a></p>',
        1,
    )
    return html


def deepen_first(html: str) -> str:
    html = _inject_head_style(html)
    html = _soften_brand(html)
    title = "Primer pedido CSSBuy España — Correos, AEAT, dirección | CSSBuy"
    desc = (
        "Primer pedido CSSBuy desde España: dirección CP5, Correos, AEAT. "
        "Spreadsheet global → cssbuyspreadsheet.eu."
    )
    html = _set_title_desc(html, title, desc)
    html = html.replace(
        '<span class="eyebrow" style="color:var(--acd)">Guía</span>',
        '<span class="eyebrow" style="color:var(--acd)">Primer pedido · Correos / AEAT · 28 Oct 2026</span>',
        1,
    )
    if f'data-es-deepen="{STAMP}"' not in html:
        html = html.replace(
            '<p class="lead">Copias el enlace, lo pegas en el agente, revisas la foto de almacén, consolidas, eliges destino Spain — 西班牙. La dirección es una calle española y código postal de cinco dígitos. no copiamos un recuento de líneas.</p>',
            '<p class="lead">Copias el enlace, QC en almacén, consolidas y eliges destino <strong>España</strong>. Calle española + <strong>CP de cinco dígitos</strong>; última milla a menudo <strong>Correos</strong>; entrada según <strong>AEAT</strong>.</p>\n'
            f"  {HUB_UPLINK}\n"
            f"  {LOCAL_FIRST}",
            1,
        )
    if 'id="primer-pedido-es"' not in html:
        html = html.replace(
            "<h2>1. Abre una ficha en w2clinks</h2>",
            THICKEN_FIRST + "\n  <h2>1. Abre una ficha en w2clinks</h2>",
            1,
        )
    html = html.replace(
        '<p><a class="btn" href="/how-to-use-cssbuy/">Guía</a> <a class="btn btn--ghost" href="/cssbuy-shipping/">Plan de envío</a></p>',
        '<p><a class="btn" href="/cssbuy-shipping/">Envío Correos / AEAT</a> '
        '<a class="btn btn--ghost" href="/cssbuy-coupons/">Cupones ES</a> '
        f'<a class="btn btn--ghost" href="{HUB}/">Hub spreadsheet</a></p>',
        1,
    )
    return html


BUILDERS = {
    "cssbuy-shipping": deepen_shipping,
    "cssbuy-coupons": deepen_coupons,
    "how-to-use-cssbuy": deepen_first,
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
            "Correos",
            "AEAT",
            f'data-es-deepen="{STAMP}"',
            "cssbuyspreadsheet.eu",
            "finds-dataset",
        ):
            if must not in deepened:
                raise SystemExit(f"{slug}: missing {must}")
        if re.search(r"<h1>[^<]*Spreadsheet", deepened, re.I):
            raise SystemExit(f"{slug}: H1 still Spreadsheet hero")
        title_m = re.search(r"<title>(.*?)</title>", deepened, re.S | re.I)
        if title_m and re.search(r"Spreadsheet", title_m.group(1), re.I):
            raise SystemExit(f"{slug}: <title> still Spreadsheet hero")
        dest = OVERLAY / slug / "index.html.es-deepen"
        dest.write_text(deepened)
        out[slug] = dest
        print("BUILT", dest, "bytes", dest.stat().st_size)
    return out


def deploy(built: dict[str, Path], store_internal: Path | None) -> dict:
    client = _connect()
    bak = f"/www/backup/cssbuy-es-deepen-{datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%S')}"
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
        # how-to-use may already be in sitemap; coupons may be missing — ensure entries
        for slug in PAGES:
            loc = f"https://{HOST}/{slug}/"
            if loc not in sm:
                sm = sm.replace(
                    "</urlset>",
                    f"  <url>\n    <loc>{loc}</loc>\n    <lastmod>{today}</lastmod>\n"
                    f"    <changefreq>weekly</changefreq>\n    <priority>0.8</priority>\n  </url>\n</urlset>",
                )
        sm = re.sub(
            rf"(<loc>https://{re.escape(HOST)}/</loc>\s*<lastmod>)[^<]+",
            rf"\g<1>{today}",
            sm,
        )
        # also /guide/shipping alias note: sitemap uses money URL
        tmp = f"/tmp/cssbuy-es-sitemap-{STAMP}.xml"
        Path(tmp).write_text(sm)
        sftp.put(tmp, f"{REMOTE}/sitemap.xml")
        # keep overlay copy
        (OVERLAY / "sitemap.xml").write_text(sm)
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
    # ensure homepage NOT stamped
    home_check = _run(
        client,
        f"grep -c 'data-es-deepen' '{REMOTE}/index.html' || true; "
        f"grep -c 'data-es-deepen' '{REMOTE}/../cssbuyspreadsheet.eu/index.html' 2>/dev/null || true; "
        f"ls '{bak}'",
    )
    print("HOME_HUB_STAMP_CHECK", home_check)
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
        req = Request(url, headers={"User-Agent": "cssbuy-es-deepen/1.0"})
        with urlopen(req, timeout=30) as resp:
            body = resp.read().decode(errors="replace")
            code = resp.status
        row = {
            "url": url,
            "http": code,
            "id_local": 'id="local"' in body,
            "hub_uplink": "cssbuyspreadsheet.eu" in body and "finds-dataset" in body,
            "correos": body.count("Correos"),
            "aeat": body.count("AEAT") + body.count("Agencia Tributaria"),
            "data_es_deepen": f'data-es-deepen="{STAMP}"' in body,
            "spreadsheet_h1": bool(re.search(r"<h1>[^<]*Spreadsheet", body, re.I)),
        }
        m = re.search(r"<title>(.*?)</title>", body, re.S | re.I)
        row["title"] = re.sub(r"\s+", " ", m.group(1)).strip() if m else None
        row["title_spreadsheet"] = bool(
            row["title"] and re.search(r"Spreadsheet", row["title"], re.I)
        )
        checks.append(row)

    # homepage + hub must remain 200 and NOT carry deepen stamp
    for url in (f"https://{HOST}/", f"{HUB}/"):
        req = Request(url, headers={"User-Agent": "cssbuy-es-deepen/1.0"})
        with urlopen(req, timeout=30) as resp:
            body = resp.read().decode(errors="replace")
            checks.append(
                {
                    "url": url,
                    "http": resp.status,
                    "data_es_deepen": f'data-es-deepen="{STAMP}"' in body,
                    "untouched": f'data-es-deepen="{STAMP}"' not in body,
                }
            )

    twins = [
        "https://cssbuyspreadsheet.es/",
        "https://cssbuyspreadsheet.nl/",
        "https://cssbuyspreadsheet.it/",
        "https://cssbuyspreadsheet.fr/",
        "https://cssbuyspreadsheets.de/",
        "https://cssbuyspreadsheets.us/",
        "https://cssbuy.at/",
        "https://cssbuyspreadsheet.ca/",
        "https://cssbuyspreadsheet.uk/",
    ]
    twin_rows = []
    for t in twins:
        u = urlparse(t)
        conn = http.client.HTTPSConnection(u.netloc, timeout=20)
        conn.request("GET", u.path or "/", headers={"User-Agent": "cssbuy-es-deepen/1.0"})
        r = conn.getresponse()
        twin_rows.append({"url": t, "http": r.status, "location": r.getheader("Location")})
        conn.close()

    # guide/shipping alias should still 301→shipping money URL
    u = urlparse("https://cssbuy.es/guide/shipping")
    conn = http.client.HTTPSConnection(u.netloc, timeout=20)
    conn.request("GET", u.path, headers={"User-Agent": "cssbuy-es-deepen/1.0"})
    r = conn.getresponse()
    alias = {"url": "https://cssbuy.es/guide/shipping", "http": r.status, "location": r.getheader("Location")}
    conn.close()

    return {
        "at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "checks": checks,
        "twins": twin_rows,
        "guide_shipping_alias": alias,
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
                or not c.get("data_es_deepen")
                or c.get("spreadsheet_h1")
                or c.get("title_spreadsheet")
                or c.get("http") != 200
            )
        ]
        untouched_bad = [
            c
            for c in ver["checks"]
            if c.get("url") in (f"https://{HOST}/", f"{HUB}/") and not c.get("untouched")
        ]
        twin_ok_loc = {
            "https://cssbuyspreadsheet.es/": "https://cssbuy.es",
            "https://cssbuyspreadsheet.nl/": "https://cssbuy.nl",
            "https://cssbuyspreadsheet.it/": "https://cssbuy.it",
            "https://cssbuyspreadsheet.fr/": "https://cssbuy.fr",
        }
        twin_hub = (
            "https://cssbuyspreadsheets.de/",
            "https://cssbuyspreadsheets.us/",
            "https://cssbuy.at/",
            "https://cssbuyspreadsheet.ca/",
            "https://cssbuyspreadsheet.uk/",
        )
        twin_bad = []
        for t in ver.get("twins", []):
            loc = (t.get("location") or "").rstrip("/")
            if t.get("http") not in (301, 302):
                twin_bad.append(t)
                continue
            if t["url"] in twin_ok_loc:
                want = twin_ok_loc[t["url"]].rstrip("/")
                if not loc.startswith(want):
                    twin_bad.append(t)
            elif t["url"] in twin_hub:
                if "cssbuyspreadsheet.eu" not in loc:
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
