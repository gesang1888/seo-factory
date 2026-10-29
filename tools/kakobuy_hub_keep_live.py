#!/usr/bin/env python3
"""Kakobuy hub hard reclaim + FI/ES/CA keep deepen LIVE (confirmed 1.2).

Hub kakobuydocs.com: year-dated title/H1 + Independent Index/dataset citation stamp.
Keep desks: Posti (FI) · Correos (ES) · Canada Post/CBSA (CA) — no spreadsheet heroes;
hub uplink to kakobuydocs.com. No new domains / no lookalike .co.uk. No consumer ops notes.

Requires ORIGIN_SSH_PASS (or --load-env internal/usfans-ssh.env).
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
STORE = Path("/cursor/stores/bc-eb8405c7-0d3c-48be-958d-5f25b92c606c")
STAMP = "20261029"
TAG = f"kakobuy-hub-keep-live-{STAMP}"
DATE = "2026-10-29"
DATE_HUMAN = "29 Oct 2026"
YEAR = "2026"
HUB = "https://kakobuydocs.com"
ROW = "11365"
ROW_DISP = "11,300+"
UA = "kakobuy-hub-keep-live/1.0"

# Consumer-visible ops needles — must stay out of page copy (comments/attrs OK).
FORBIDDEN_CONSUMER = (
    "Desk ES ·",
    "Desk CA ·",
    "Desk FI ·",
    "Keep desks",
    "keep desks",
    "Do not revive",
    "do not revive",
    "Phase A/B/C",
    "Phase A/",
    "Twins tips",
    "twins tips",
    "Twins 301",
    "hub reclaim",
    "Hub reclaim",
    "Not a dest-country skin",
    "not a dest-country skin",
    "local KPI only",
    "LATAM",
    "latam-note",
    "data-latam-overflow",
    "Sin twin LATAM",
    "money URLs ≤6",
    "Hub ownership · money",
    "US keep desk",
    "keep desk",
    "Lab 1 oct 2026",
    "Lab 1 oct. 2026",
)

STYLE = (
    f'<style id="hub-keep-{STAMP}">'
    ".hub-uplink{margin:14px 0 0;padding:12px 14px;border-left:3px solid #0f766e;"
    "background:#f0fdfa;color:#134e4a;line-height:1.6;font-size:15px;max-width:760px}"
    ".hub-uplink a{color:#0f766e;font-weight:600}"
    "#local{scroll-margin-top:88px}"
    ".local-box{margin:1.25em 0;padding:14px 16px;border:1px solid #e2e8f0;"
    "border-radius:12px;background:#f8fafc}"
    ".local-box h2{margin:0 0 .55em;font-size:1.12rem}"
    ".local-box ol{margin:.35em 0 0;padding-left:1.2em}"
    ".local-box li{margin:.32em 0}</style>"
)

HUB_UPLINK_FI = (
    f'<p class="hub-uplink" data-hub-keep="{STAMP}" data-step4-hub="1">'
    f"Globaali Kakobuy Independent Index · {ROW_DISP} / spreadsheet / coupons / dataset → "
    f'<a href="{HUB}/">{HUB.replace("https://", "")}</a> · '
    f'<a href="{HUB}/kakobuy-spreadsheet/">spreadsheet {YEAR}</a> · '
    f'<a href="{HUB}/kakobuy-coupons/">coupons</a> · '
    f'<a href="{HUB}/finds-dataset/">dataset</a>. '
    "Tämä host = suomalainen postinumero, Posti, Tulli — ei toinen spreadsheet-hub."
    "</p>"
)

HUB_UPLINK_ES = (
    f'<p class="hub-uplink" data-hub-keep="{STAMP}" data-step4-hub="1">'
    f"Índice global Kakobuy Independent Index · {ROW_DISP} / spreadsheet / coupons / dataset → "
    f'<a href="{HUB}/">{HUB.replace("https://", "")}</a> · '
    f'<a href="{HUB}/kakobuy-spreadsheet/">spreadsheet {YEAR}</a> · '
    f'<a href="{HUB}/kakobuy-coupons/">coupons</a> · '
    f'<a href="{HUB}/finds-dataset/">dataset</a>. '
    "Este host = dirección ES, Correos, AEAT — no un segundo hub de spreadsheet."
    "</p>"
)

HUB_UPLINK_CA = (
    f'<p class="hub-uplink" data-hub-keep="{STAMP}" data-step4-hub="1">'
    f"Global Kakobuy Independent Index · {ROW_DISP} / spreadsheet / coupons / dataset → "
    f'<a href="{HUB}/">{HUB.replace("https://", "")}</a> · '
    f'<a href="{HUB}/kakobuy-spreadsheet/">spreadsheet {YEAR}</a> · '
    f'<a href="{HUB}/kakobuy-coupons/">coupons</a> · '
    f'<a href="{HUB}/finds-dataset/">dataset</a>. '
    "This host = Canadian postal code, Canada Post, CBSA — not a second spreadsheet hub."
    "</p>"
)

LOCAL_FI = f"""
<section id="local" class="local-box" data-fi-fingerprint="posti-tulli-00100" data-hub-keep="{STAMP}">
<h2>Suomi ennen lähetystä</h2>
<ol>
<li><strong>Arvioijan kohde: Suomi</strong> — valitse Finland / Suomi, ei EU eikä tämä TLD.</li>
<li><strong>Osoite</strong> — suomalainen katu + <strong>viisinumeroinen postinumero</strong> (esim. <code>00100</code>).</li>
<li><strong>Viimeinen kilometri</strong> — usein <strong>Posti</strong>; desk ei keksi noutopistettä.</li>
<li><strong>Tulli / ALV</strong> — lukee SKU:sta. Lähde: <a href="https://tulli.fi/" rel="noopener" target="_blank">Tulli</a>. Ei aliarvostusta.</li>
</ol>
<p>Brand-index → <a href="{HUB}/kakobuy-spreadsheet/">kakobuydocs.com/kakobuy-spreadsheet</a> ({YEAR}). Stempel: <strong>{DATE_HUMAN}</strong>.</p>
</section>
"""

LOCAL_ES = f"""
<section id="local" class="local-box" data-es-fingerprint="correos-aeat-cp5" data-hub-keep="{STAMP}">
<h2>Huella España antes de enviar</h2>
<ol>
<li><strong>Destino del estimador: España</strong> — Spain / España, no «EU» ni este TLD.</li>
<li><strong>Dirección</strong> — calle española + <strong>código postal de cinco dígitos</strong>.</li>
<li><strong>Última milla</strong> — a menudo <strong>Correos</strong>; el desk no inventa un Collect.</li>
<li><strong>Aranceles / IVA</strong> — según SKU. Fuente: <a href="https://sede.agenciatributaria.gob.es/" rel="noopener" target="_blank">AEAT</a>.</li>
</ol>
<p>Índice de marca → <a href="{HUB}/kakobuy-spreadsheet/">kakobuydocs.com/kakobuy-spreadsheet</a> ({YEAR}). Sello: <strong>{DATE_HUMAN}</strong>.</p>
</section>
"""

LOCAL_CA = f"""
<section id="local" class="local-box" data-ca-fingerprint="canada-post-cbsa-a1a" data-hub-keep="{STAMP}">
<h2>Canada fingerprint before you ship</h2>
<ol>
<li><strong>Estimator destination: Canada</strong> — pick Canada, not this hostname and not a US ZIP.</li>
<li><strong>Address</strong> — Canadian street + postal code form <strong>A1A 1A1</strong>.</li>
<li><strong>Last mile</strong> — often <strong>Canada Post</strong>; this desk does not invent a depot.</li>
<li><strong>Duties / GST</strong> — SKU decides prepaid vs collect. Source: <a href="https://www.cbsa-asfc.gc.ca/" rel="noopener" target="_blank">CBSA</a>.</li>
</ol>
<p>Brand Independent Index → <a href="{HUB}/kakobuy-spreadsheet/">kakobuydocs.com/kakobuy-spreadsheet</a> ({YEAR}). Stamp: <strong>{DATE_HUMAN}</strong>.</p>
</section>
"""

PAGES = {
    "kakobuydocs.com": [
        ("home", "/"),
        ("kakobuy-spreadsheet", "/kakobuy-spreadsheet/"),
        ("kakobuy-coupons", "/kakobuy-coupons/"),
        ("finds-dataset", "/finds-dataset/"),
        ("data-finds", "/data/finds-dataset.json"),
        ("data-coupons", "/data/coupons-truth.json"),
        ("llms", "/llms.txt"),
    ],
    "kakobuy.fi": [
        ("home", "/"),
        ("kakobuy-kokemuksia", "/kakobuy-kokemuksia/"),
        ("kakobuy-toimitus", "/kakobuy-toimitus/"),
        ("kakobuy-shipping", "/kakobuy-shipping/"),
    ],
    "kakospreadsheet.es": [
        ("home", "/"),
        ("como-comprar-en-kakobuy", "/como-comprar-en-kakobuy/"),
        ("how-to-use-kakobuy", "/how-to-use-kakobuy/"),
        ("envio-kakobuy-espana", "/envio-kakobuy-espana/"),
        ("kakobuy-opiniones", "/kakobuy-opiniones/"),
        ("es-kakobuy-confiable", "/es-kakobuy-confiable/"),
    ],
    "kakospreadsheet.ca": [
        ("home", "/"),
        ("kakobuy-shipping", "/kakobuy-shipping/"),
        ("kakobuy-shipping-to-canada", "/kakobuy-shipping-to-canada/"),
        ("how-to-use-kakobuy", "/how-to-use-kakobuy/"),
        ("is-kakobuy-legit", "/is-kakobuy-legit/"),
        ("kakobuy-spreadsheet", "/kakobuy-spreadsheet/"),
    ],
}


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


def _fetch(url: str) -> str:
    req = Request(url, headers={"User-Agent": UA})
    with urlopen(req, timeout=45) as resp:
        return resp.read().decode("utf-8", "replace")


def _connect():
    try:
        import paramiko
    except ImportError:
        import subprocess

        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "--user", "paramiko", "-q"]
        )
        import site

        user_site = site.getusersitepackages()
        if user_site not in sys.path:
            sys.path.append(user_site)
        import paramiko

    password = os.environ.get("ORIGIN_SSH_PASS")
    if not password:
        raise SystemExit("Set ORIGIN_SSH_PASS or pass --load-env")
    host = os.environ.get("ORIGIN_SSH_HOST", "31.97.41.31")
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(host, username="root", password=password, timeout=30)
    return client


def _run(client, cmd: str, timeout: int = 180) -> str:
    _, stdout, stderr = client.exec_command(cmd, timeout=timeout)
    return (stdout.read() + stderr.read()).decode(errors="replace").strip()


def _overlay_path(host: str, key: str) -> Path:
    base = ROOT / "sites" / host / "overlay"
    if key == "home":
        return base / f"index.html.hub-keep"
    if key == "data-finds":
        return base / "data" / "finds-dataset.json"
    if key == "data-coupons":
        return base / "data" / "coupons-truth.json"
    if key == "llms":
        return base / "llms.txt"
    return base / key / f"index.html.hub-keep"


def _remote_path(host: str, key: str) -> str:
    root = f"/www/wwwroot/{host}"
    if key == "home":
        return f"{root}/index.html"
    if key == "data-finds":
        return f"{root}/data/finds-dataset.json"
    if key == "data-coupons":
        return f"{root}/data/coupons-truth.json"
    if key == "llms":
        return f"{root}/llms.txt"
    return f"{root}/{key}/index.html"


def _inject_style(html: str) -> str:
    if f'id="hub-keep-{STAMP}"' in html:
        return html
    if "</head>" not in html:
        return html
    return html.replace("</head>", STYLE + "\n</head>", 1)


def _mark_body(html: str) -> str:
    if f'data-hub-keep="{STAMP}"' in html[:2500]:
        return html
    return re.sub(
        r"<body([^>]*)>",
        rf'<body\1 data-hub-keep="{STAMP}">',
        html,
        count=1,
        flags=re.I,
    )


def _set_title(html: str, title: str) -> str:
    html = re.sub(r"<title>.*?</title>", f"<title>{title}</title>", html, count=1, flags=re.S)
    if re.search(r'property="og:title"', html):
        html = re.sub(
            r'property="og:title" content="[^"]*"',
            f'property="og:title" content="{title}"',
            html,
            count=1,
        )
    return html


def _set_desc(html: str, desc: str) -> str:
    if re.search(r'<meta name="description"', html, re.I):
        html = re.sub(
            r'<meta name="description" content="[^"]*"',
            f'<meta name="description" content="{desc}"',
            html,
            count=1,
            flags=re.I,
        )
    if re.search(r'property="og:description"', html):
        html = re.sub(
            r'property="og:description" content="[^"]*"',
            f'property="og:description" content="{desc}"',
            html,
            count=1,
        )
    return html


def _assert_no_ops(label: str, text: str) -> None:
    # Strip HTML comments before scanning consumer copy.
    visible = re.sub(r"<!--.*?-->", "", text, flags=re.S)
    # Ignore data-* attribute values that only stamp scrub/keep tags.
    visible = re.sub(r'\sdata-[\w-]+=("[^"]*"|\'[^\']*\')', "", visible)
    for needle in FORBIDDEN_CONSUMER:
        if needle in visible:
            raise SystemExit(f"{label}: forbidden consumer ops needle {needle!r}")


def _stamp_comment(html: str) -> str:
    marker = f"<!-- {TAG} -->"
    if marker in html:
        return html
    if "<head>" in html:
        return html.replace("<head>", f"<head>\n{marker}", 1)
    return marker + "\n" + html


# ---------- Hub hard reclaim ----------


def patch_hub_spreadsheet(html: str) -> str:
    html = _stamp_comment(html)
    html = html.replace(
        "<!-- hub-reclaim=kakobuy-hub-reclaim-20261027 -->",
        f"<!-- hub-reclaim={TAG} -->",
    )
    if f"hub-reclaim={TAG}" not in html and "hub-reclaim=" not in html[:800]:
        html = html.replace("<head>", f"<head>\n<!-- hub-reclaim={TAG} -->", 1)

    title = f"Kakobuy Spreadsheet {YEAR} — Independent Index · {ROW_DISP}"
    desc = (
        f"Kakobuy spreadsheet {YEAR}: Independent Index · {ROW_DISP} "
        f"(Typesense found={ROW}, {DATE_HUMAN}). Open directory + coupons truth + "
        f"public dataset citation on kakobuydocs.com — not a Google Sheet dump."
    )
    html = _set_title(html, title)
    html = _set_desc(html, desc)
    html = re.sub(
        r'property="article:modified_time" content="[^"]*"',
        f'property="article:modified_time" content="{DATE}"',
        html,
        count=1,
    )
    html = re.sub(
        r'("dateModified":\s*")2026-10-27(")',
        rf'\1{DATE}\2',
        html,
    )
    html = re.sub(
        r'("name":\s*")Kakobuy Spreadsheet — Independent Index · 11,300\+(")',
        rf'\1{title}\2',
        html,
        count=1,
    )
    html = html.replace(
        "Independent Index · 11,300+ · last_verified 27 Oct 2026",
        f"Independent Index · {ROW_DISP} · {YEAR} · last_verified {DATE_HUMAN}",
    )
    html = re.sub(
        r"<h1>Kakobuy Spreadsheet<br><em>Independent Index · 11,300\+</em></h1>",
        f"<h1>Kakobuy Spreadsheet {YEAR}<br><em>Independent Index · {ROW_DISP}</em></h1>",
        html,
        count=1,
    )
    html = html.replace("last_verified 2026-10-27", f"last_verified {DATE}")
    html = html.replace("27 Oct 2026", DATE_HUMAN)
    html = html.replace("2026-10-27", DATE)
    html = html.replace("kakobuy-hub-reclaim-20261027", TAG)
    # Strengthen dataset citation block wording (consumer-safe).
    html = html.replace(
        "KakobuyDocs · Independent Index",
        f"KakobuyDocs · Independent Index {YEAR}",
    )
    html = html.replace(
        f"found={ROW}</li>",
        f"found={ROW} · cited {DATE}</li>",
    )
    html = re.sub(
        r"hero_h1_2:'Independent Index · 11,300\+'",
        f"hero_h1_2:'Independent Index · {ROW_DISP}'",
        html,
    )
    html = re.sub(
        r"hero_badge:'Independent Index · 11,300\+ · last_verified [^']*'",
        f"hero_badge:'Independent Index · {ROW_DISP} · {YEAR} · last_verified {DATE_HUMAN}'",
        html,
    )
    html = re.sub(
        r"hero_h1_1:'Kakobuy Spreadsheet'",
        f"hero_h1_1:'Kakobuy Spreadsheet {YEAR}'",
        html,
    )
    html = _mark_body(html)
    _assert_no_ops("hub-spreadsheet", html)
    if f"Spreadsheet {YEAR}" not in html or ROW_DISP not in html or DATE not in html:
        raise SystemExit("hub spreadsheet missing year/index/date citation")
    return html


def patch_hub_home(html: str) -> str:
    html = _stamp_comment(html)
    html = re.sub(
        r"<!-- platform_opt=[^>]+-->",
        f"<!-- platform_opt={TAG} -->",
        html,
        count=1,
    )
    title = f"Kakobuy Docs {YEAR} — Independent Index · {ROW_DISP}"
    desc = (
        f"Kakobuy Independent Index · {ROW_DISP} ({YEAR}). Open directory, coupons truth, "
        f"and finds-dataset citation stamped {DATE_HUMAN} on kakobuydocs.com."
    )
    html = _set_title(html, title)
    html = _set_desc(html, desc)
    html = html.replace("2026-10-27", DATE)
    html = html.replace("kakobuy-hub-reclaim-20261027", TAG)
    html = re.sub(
        r"(<h1>Kakobuy Docs — Independent Index <em>)11,300\+(</em></h1>)",
        rf"\1{ROW_DISP}\2",
        html,
        count=1,
    )
    # Soften any leftover ops phrases if present.
    for bad, good in (
        ("Keep desks: kakobuy.fi / kakospreadsheet.es / kakospreadsheet.ca. Twins kakobuytips.com + kakospreadsheet.fr/.nl 301→this hub. ", ""),
        ("Do not revive sunset twins.", ""),
        ("Keep country desks: kakobuy.fi, kakospreadsheet.es, kakospreadsheet.ca. Do not revive sunset twins.", "Country guides: kakobuy.fi, kakospreadsheet.es, kakospreadsheet.ca."),
        ("FI/ES/CA desks keep local postal / customs KPI (Posti/Tulli, Correos/AEAT, Canada Post/CBSA).", "Country guides cover Posti/Tulli, Correos/AEAT, Canada Post/CBSA."),
    ):
        html = html.replace(bad, good)
    html = _mark_body(html)
    _assert_no_ops("hub-home", html)
    return html


def patch_hub_generic(html: str) -> str:
    html = _stamp_comment(html)
    html = html.replace("2026-10-27", DATE)
    html = html.replace("27 Oct 2026", DATE_HUMAN)
    html = html.replace("kakobuy-hub-reclaim-20261027", TAG)
    html = _mark_body(html)
    _assert_no_ops("hub-generic", html)
    return html


def patch_finds_json(raw: str) -> str:
    data = json.loads(raw)
    data["last_verified"] = DATE
    data["generated_at"] = f"{DATE}T12:40:00Z"
    data["platform_opt"] = TAG
    data["measurement"] = (
        f"w2clinks.com/public/typesense-search.php found={ROW} on {DATE}"
    )
    data["anti_sheet_note"] = (
        f"Public, citable row counts + dated category proofs ({YEAR}). "
        "Brand spreadsheet SERP targets /kakobuy-spreadsheet/ + Independent Index "
        f"on kakobuydocs.com (stamp {DATE})."
    )
    data["row_count"] = int(ROW)
    data["row_count_display"] = ROW_DISP
    return json.dumps(data, indent=2, ensure_ascii=False) + "\n"


def patch_coupons_json(raw: str) -> str:
    data = json.loads(raw)
    data["last_verified"] = DATE
    data["platform_opt"] = TAG
    note = data.get("serp_note", "")
    note = re.sub(r"FI/ES/CA keep local KPI only\.?\s*", "", note)
    note = re.sub(r"Twins tips/\.fr/\.nl stay 301→hub\.?\s*", "", note)
    data["serp_note"] = (
        note.strip()
        or f"Brand spreadsheet queries consolidate on kakobuydocs.com /kakobuy-spreadsheet/ + Independent Index · {ROW_DISP} ({YEAR})."
    )
    return json.dumps(data, indent=2, ensure_ascii=False) + "\n"


def patch_llms(text: str) -> str:
    text = text.replace("2026-10-27", DATE)
    text = text.replace("kakobuy-hub-reclaim-20261027", TAG)
    if TAG not in text:
        text = f"# {TAG}\n" + text
    if f"Independent Index · {ROW_DISP}" not in text and "11,300+" in text:
        pass
    if f"Spreadsheet {YEAR}" not in text:
        text = text.replace(
            "kakobuy-spreadsheet",
            f"kakobuy-spreadsheet ({YEAR} Independent Index)",
            1,
        )
    return text


# ---------- Keep desks ----------


def _soften_fi(html: str) -> str:
    html = html.replace("<span>Spreadsheet</span>", "<span>Suomi</span>", 1)
    html = html.replace("<h3>Kakobuy Spreadsheet</h3>", "<h3>Kakobuy Suomi</h3>")
    html = html.replace(
        "Kakobuy Spreadsheet on riippumaton tietosivusto",
        "kakobuy.fi on riippumaton FI-opas (Posti / Tulli)",
    )
    html = html.replace(
        "&copy; 2026 Kakobuy Spreadsheet.",
        "&copy; 2026 Kakobuy Suomi.",
    )
    html = html.replace("Spreadsheet ja kategoriat", "Katalogi ja kategoriat")
    html = re.sub(
        r'("name":\s*")Kakobuy Spreadsheet suomeksi:[^"]*(")',
        r'\1Kakobuy Suomi — Posti, Tulli, postinumero\2',
        html,
        count=1,
    )
    return html


def _soften_es(html: str) -> str:
    html = html.replace("<span>Spreadsheet</span>", "<span>España</span>", 1)
    html = html.replace("<h3>Kakobuy Spreadsheet</h3>", "<h3>Kakobuy España</h3>")
    html = html.replace(
        "Kakobuy Spreadsheet es un sitio informativo independiente",
        "kakospreadsheet.es es una guía ES independiente (Correos / AEAT)",
    )
    html = html.replace(
        "&copy; 2026 Kakobuy Spreadsheet.",
        "&copy; 2026 Kakobuy España.",
    )
    html = html.replace("Spreadsheet y categorías", "Catálogo y categorías")
    html = re.sub(
        r'("name":\s*")Kakobuy Spreadsheet en español:[^"]*(")',
        r'\1Kakobuy España — Correos, AEAT, código postal\2',
        html,
        count=1,
    )
    return html


def _soften_ca(html: str) -> str:
    html = html.replace("<span>Spreadsheet</span>", "<span>Canada</span>", 1)
    html = html.replace("<h3>Kakobuy Spreadsheet</h3>", "<h3>Kakobuy Canada</h3>")
    html = html.replace(
        "Kakobuy Spreadsheet is an independent information site",
        "kakospreadsheet.ca is an independent Canada guide (Canada Post / CBSA)",
    )
    html = html.replace(
        "&copy; 2026 Kakobuy Spreadsheet.",
        "&copy; 2026 Kakobuy Canada.",
    )
    html = re.sub(
        r'("name":\s*")Kakobuy Spreadsheet in English:[^"]*(")',
        r'\1Kakobuy Canada — Canada Post, CBSA, postal code\2',
        html,
    )
    return html


def _ensure_uplink(html: str, uplink: str) -> str:
    if f'data-hub-keep="{STAMP}"' in html and "hub-uplink" in html and HUB in html:
        # Refresh existing step4 uplink line if present
        if 'class="hub-uplink"' in html and f'data-hub-keep="{STAMP}"' not in html:
            html = re.sub(
                r'<p class="hub-uplink"[^>]*>.*?</p>',
                uplink,
                html,
                count=1,
                flags=re.S,
            )
        elif f'data-hub-keep="{STAMP}"' not in html:
            html = html.replace("</header>", "</header>\n" + uplink, 1)
        return html
    if 'class="hub-uplink"' in html:
        html = re.sub(
            r'<p class="hub-uplink"[^>]*>.*?</p>',
            uplink,
            html,
            count=1,
            flags=re.S,
        )
        return html
    if 'id="local"' in html:
        return re.sub(
            r'(<section[^>]*id="local"[^>]*>)',
            uplink + r"\n\1",
            html,
            count=1,
        )
    if "</header>" in html:
        return html.replace("</header>", "</header>\n" + uplink, 1)
    return html.replace("<body", uplink + "\n<body", 1)


def _ensure_local(html: str, block: str) -> str:
    # Already has this stamp's fingerprint box.
    if f'data-hub-keep="{STAMP}"' in html and "local-box" in html and 'id="local"' in html:
        # Prefer fingerprint-bearing local-box; if only old #local exists, append.
        if "data-fi-fingerprint=" in html or "data-es-fingerprint=" in html or "data-ca-fingerprint=" in html:
            return html
    if 'id="local"' in html and "local-box" not in html:
        return re.sub(
            r'(<section[^>]*id="local"[\s\S]*?</section>)',
            r"\1\n" + block,
            html,
            count=1,
        )
    if "local-box" in html and f'data-hub-keep="{STAMP}"' in html:
        return html
    m = re.search(r'<p class="hub-uplink"[\s\S]*?</p>', html)
    if m:
        i = m.end()
        return html[:i] + "\n" + block + html[i:]
    if "</header>" in html:
        return html.replace("</header>", "</header>\n" + block, 1)
    return html + "\n" + block


def patch_fi_home(html: str) -> str:
    html = _stamp_comment(html)
    html = _inject_style(html)
    html = _soften_fi(html)
    html = _mark_body(html)
    html = _set_title(html, "Kakobuy Suomi — Posti, Tulli, postinumero 00100")
    html = _set_desc(
        html,
        f"FI-opas Kakobuy: suomalainen postinumero (00100), Posti, Tulli. "
        f"Brand Independent Index {YEAR} → kakobuydocs.com. Päivitetty {DATE_HUMAN}.",
    )
    html = _ensure_uplink(html, HUB_UPLINK_FI)
    if f'data-hub-keep="{STAMP}"' not in html or "Posti" not in html:
        html = _ensure_local(html, LOCAL_FI)
    elif 'data-fi-fingerprint="posti-tulli-00100"' not in html:
        html = _ensure_local(html, LOCAL_FI)
    _assert_no_ops("fi-home", html)
    if "Posti" not in html or "Tulli" not in html or HUB not in html:
        raise SystemExit("fi-home missing Posti/Tulli/hub")
    if re.search(r"<h1>[^<]*Spreadsheet", html, re.I):
        raise SystemExit("fi-home spreadsheet H1")
    return html


def patch_fi_inner(html: str) -> str:
    html = _stamp_comment(html)
    html = _inject_style(html)
    html = _soften_fi(html)
    html = _mark_body(html)
    html = _ensure_uplink(html, HUB_UPLINK_FI)
    if "Posti" not in html or "00100" not in html:
        html = _ensure_local(html, LOCAL_FI)
    # Drop spreadsheet from titles if present
    title_m = re.search(r"<title>(.*?)</title>", html, re.S | re.I)
    if title_m and re.search(r"Spreadsheet", title_m.group(1), re.I):
        html = _set_title(
            html,
            "Kakobuy toimitus Suomeen — Posti, Tulli, postinumero",
        )
    _assert_no_ops("fi-inner", html)
    return html


def patch_es_home(html: str) -> str:
    html = _stamp_comment(html)
    html = _inject_style(html)
    html = _soften_es(html)
    html = _mark_body(html)
    html = _set_title(html, "Kakobuy España — Correos, AEAT, código postal")
    html = _set_desc(
        html,
        f"Guía ES Kakobuy: Correos, AEAT y CP de cinco dígitos. "
        f"Independent Index {YEAR} → kakobuydocs.com. Actualizado {DATE_HUMAN}.",
    )
    html = _ensure_uplink(html, HUB_UPLINK_ES)
    if 'data-es-fingerprint="correos-aeat-cp5"' not in html:
        html = _ensure_local(html, LOCAL_ES)
    _assert_no_ops("es-home", html)
    if "Correos" not in html or "AEAT" not in html or HUB not in html:
        raise SystemExit("es-home missing Correos/AEAT/hub")
    if re.search(r"<h1>[^<]*Spreadsheet", html, re.I):
        raise SystemExit("es-home spreadsheet H1")
    return html


def patch_es_inner(html: str) -> str:
    html = _stamp_comment(html)
    html = _inject_style(html)
    html = _soften_es(html)
    html = _mark_body(html)
    html = _ensure_uplink(html, HUB_UPLINK_ES)
    if "Correos" not in html or "AEAT" not in html:
        html = _ensure_local(html, LOCAL_ES)
    title_m = re.search(r"<title>(.*?)</title>", html, re.S | re.I)
    if title_m and re.search(r"Spreadsheet", title_m.group(1), re.I):
        html = _set_title(
            html,
            "Kakobuy España — Correos, AEAT, dirección",
        )
    _assert_no_ops("es-inner", html)
    return html


def patch_ca_home(html: str) -> str:
    html = _stamp_comment(html)
    html = _inject_style(html)
    html = _soften_ca(html)
    html = _mark_body(html)
    html = _set_title(html, "Kakobuy Canada — Canada Post, CBSA, postal code A1A 1A1")
    html = _set_desc(
        html,
        f"Canada guide for Kakobuy: Canada Post, CBSA, postal code A1A 1A1. "
        f"Brand Independent Index {YEAR} → kakobuydocs.com. Updated {DATE_HUMAN}.",
    )
    # Soften JSON-LD leftover Spain name
    html = html.replace('"name": "Kakobuy España"', '"name": "Kakobuy Canada"')
    html = _ensure_uplink(html, HUB_UPLINK_CA)
    if 'data-ca-fingerprint="canada-post-cbsa-a1a"' not in html:
        html = _ensure_local(html, LOCAL_CA)
    # Ensure Canada Post token appears (CBSA already common)
    if "Canada Post" not in html:
        html = html.replace(
            "Canada · CBSA / local shipping",
            "Canada · Canada Post / CBSA",
            1,
        )
        if "Canada Post" not in html:
            html = _ensure_local(html, LOCAL_CA)
    _assert_no_ops("ca-home", html)
    if "Canada Post" not in html or "CBSA" not in html or HUB not in html:
        raise SystemExit("ca-home missing Canada Post/CBSA/hub")
    if re.search(r"<h1>[^<]*Spreadsheet", html, re.I):
        raise SystemExit("ca-home spreadsheet H1")
    return html


def patch_ca_shipping(html: str) -> str:
    html = _stamp_comment(html)
    html = _inject_style(html)
    html = _soften_ca(html)
    html = _mark_body(html)
    html = _set_title(
        html,
        "Kakobuy shipping to Canada — Canada Post, CBSA, A1A 1A1",
    )
    html = _set_desc(
        html,
        f"Shipping Kakobuy to Canada: estimator Canada, Canada Post, CBSA, postal A1A 1A1. "
        f"Brand spreadsheet → kakobuydocs.com. {DATE_HUMAN}.",
    )
    html = re.sub(
        r"<h1>Shipping to Canada: estimator, volume, customs</h1>",
        "<h1>Shipping to Canada — Canada Post, CBSA, postal code</h1>",
        html,
        count=1,
    )
    html = re.sub(
        r"<h1>The cheapest line is not always the cheapest parcel</h1>",
        "<h1>Shipping to Canada — Canada Post, CBSA, weight</h1>",
        html,
        count=1,
    )
    html = _ensure_uplink(html, HUB_UPLINK_CA)
    html = _ensure_local(html, LOCAL_CA)
    _assert_no_ops("ca-shipping", html)
    if re.search(r"<h1>[^<]*Spreadsheet", html, re.I):
        raise SystemExit("ca-shipping spreadsheet H1")
    title_m = re.search(r"<title>(.*?)</title>", html, re.S | re.I)
    if title_m and re.search(r"Spreadsheet", title_m.group(1), re.I):
        raise SystemExit("ca-shipping title spreadsheet hero")
    return html


def patch_ca_howto(html: str) -> str:
    html = _stamp_comment(html)
    html = _inject_style(html)
    html = _soften_ca(html)
    html = _mark_body(html)
    html = _set_title(
        html,
        "First Kakobuy order from Canada — Canada Post, CBSA",
    )
    html = _set_desc(
        html,
        f"First Kakobuy order to a Canadian address: A1A 1A1, Canada Post, CBSA. "
        f"Brand Independent Index → kakobuydocs.com. {DATE_HUMAN}.",
    )
    html = re.sub(
        r"<h1>First Kakobuy order, from Canada</h1>",
        "<h1>First Kakobuy order from Canada<br><em>Canada Post · CBSA · A1A 1A1</em></h1>",
        html,
        count=1,
    )
    html = _ensure_uplink(html, HUB_UPLINK_CA)
    html = _ensure_local(html, LOCAL_CA)
    _assert_no_ops("ca-howto", html)
    if re.search(r"<title>[^<]*Spreadsheet", html, re.I):
        raise SystemExit("ca-howto title spreadsheet")
    return html


def patch_ca_legit(html: str) -> str:
    html = _stamp_comment(html)
    html = _inject_style(html)
    html = _soften_ca(html)
    html = _mark_body(html)
    html = _set_title(
        html,
        "Is Kakobuy legit in Canada? — CBSA, Canada Post",
    )
    html = _set_desc(
        html,
        f"Is Kakobuy a real agent for Canada: escrow vs CBSA, Canada Post last mile. "
        f"Brand index → kakobuydocs.com. {DATE_HUMAN}.",
    )
    html = re.sub(
        r"<h1>Is Kakobuy a real purchasing agent\?</h1>",
        "<h1>Is Kakobuy legit for Canada?<br><em>CBSA · Canada Post</em></h1>",
        html,
        count=1,
    )
    html = _ensure_uplink(html, HUB_UPLINK_CA)
    html = _ensure_local(html, LOCAL_CA)
    _assert_no_ops("ca-legit", html)
    if re.search(r"<title>[^<]*Spreadsheet", html, re.I):
        raise SystemExit("ca-legit title spreadsheet")
    return html


def patch_ca_sheet(html: str) -> str:
    """Kill spreadsheet hero on CA desk URL; point to hub."""
    html = _stamp_comment(html)
    html = _inject_style(html)
    html = _soften_ca(html)
    html = _mark_body(html)
    html = _set_title(
        html,
        "Kakobuy Canada catalogue — not a second spreadsheet hub",
    )
    html = _set_desc(
        html,
        f"This Canada URL is local postal framing (Canada Post / CBSA). "
        f"Brand Kakobuy Spreadsheet {YEAR} / Independent Index · {ROW_DISP} → kakobuydocs.com.",
    )
    html = re.sub(
        r'<span class="eyebrow"[^>]*>Spreadsheet</span>',
        '<span class="eyebrow" style="color:var(--acd)">Canada desk</span>',
        html,
        count=1,
    )
    html = re.sub(
        r"<h1>Kakobuy Spreadsheet is a catalogue, not a grid</h1>",
        f"<h1>Canada desk — not a second spreadsheet hub<br>"
        f"<em>Brand Index {YEAR} → kakobuydocs.com</em></h1>",
        html,
        count=1,
    )
    html = re.sub(
        r'(<p class="lead">)Cards with a photo, a brand and the shop link\. Thirty-three categories, the same wall as w2clinks\.(</p>)',
        rf"\1Brand spreadsheet / Independent Index · {ROW_DISP} lives on "
        f'<a href="{HUB}/kakobuy-spreadsheet/">kakobuydocs.com/kakobuy-spreadsheet</a>. '
        r"This host covers <strong>Canada Post</strong>, <strong>CBSA</strong>, and postal "
        r"<strong>A1A 1A1</strong>.\2",
        html,
        count=1,
    )
    html = _ensure_uplink(html, HUB_UPLINK_CA)
    html = _ensure_local(html, LOCAL_CA)
    _assert_no_ops("ca-sheet", html)
    if re.search(r"<h1>[^<]*Spreadsheet is a catalogue", html, re.I):
        raise SystemExit("ca-sheet still spreadsheet hero H1")
    if re.search(r"<title>[^<]*Spreadsheet in English", html, re.I):
        raise SystemExit("ca-sheet title still spreadsheet hero")
    return html


PATCHERS = {
    ("kakobuydocs.com", "home"): patch_hub_home,
    ("kakobuydocs.com", "kakobuy-spreadsheet"): patch_hub_spreadsheet,
    ("kakobuydocs.com", "kakobuy-coupons"): patch_hub_generic,
    ("kakobuydocs.com", "finds-dataset"): patch_hub_generic,
    ("kakobuydocs.com", "data-finds"): patch_finds_json,
    ("kakobuydocs.com", "data-coupons"): patch_coupons_json,
    ("kakobuydocs.com", "llms"): patch_llms,
    ("kakobuy.fi", "home"): patch_fi_home,
    ("kakobuy.fi", "kakobuy-kokemuksia"): patch_fi_inner,
    ("kakobuy.fi", "kakobuy-toimitus"): patch_fi_inner,
    ("kakobuy.fi", "kakobuy-shipping"): patch_fi_inner,
    ("kakospreadsheet.es", "home"): patch_es_home,
    ("kakospreadsheet.es", "como-comprar-en-kakobuy"): patch_es_inner,
    ("kakospreadsheet.es", "how-to-use-kakobuy"): patch_es_inner,
    ("kakospreadsheet.es", "envio-kakobuy-espana"): patch_es_inner,
    ("kakospreadsheet.es", "kakobuy-opiniones"): patch_es_inner,
    ("kakospreadsheet.es", "es-kakobuy-confiable"): patch_es_inner,
    ("kakospreadsheet.ca", "home"): patch_ca_home,
    ("kakospreadsheet.ca", "kakobuy-shipping"): patch_ca_shipping,
    ("kakospreadsheet.ca", "kakobuy-shipping-to-canada"): patch_ca_shipping,
    ("kakospreadsheet.ca", "how-to-use-kakobuy"): patch_ca_howto,
    ("kakospreadsheet.ca", "is-kakobuy-legit"): patch_ca_legit,
    ("kakospreadsheet.ca", "kakobuy-spreadsheet"): patch_ca_sheet,
}


def build() -> dict[str, Path]:
    outs: dict[str, Path] = {}
    for host, pages in PAGES.items():
        for key, path in pages:
            url = f"https://{host}{path}"
            print("FETCH", url)
            raw = _fetch(url)
            patcher = PATCHERS[(host, key)]
            built = patcher(raw)
            dest = _overlay_path(host, key)
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_text(built, encoding="utf-8")
            # Also refresh canonical overlay for hub money pages
            if host == "kakobuydocs.com" and key in (
                "home",
                "kakobuy-spreadsheet",
                "kakobuy-coupons",
                "finds-dataset",
            ):
                canon = (
                    ROOT / "sites" / host / "overlay" / "index.html"
                    if key == "home"
                    else ROOT / "sites" / host / "overlay" / key / "index.html"
                )
                canon.parent.mkdir(parents=True, exist_ok=True)
                canon.write_text(built, encoding="utf-8")
            if host == "kakobuydocs.com" and key in ("data-finds", "data-coupons", "llms"):
                # already wrote canonical path via _overlay_path
                pass
            if host != "kakobuydocs.com" and key == "home":
                canon = ROOT / "sites" / host / "overlay" / "index.html"
                canon.write_text(built, encoding="utf-8")
            outs[f"{host}:{key}"] = dest
            print("BUILT", dest, "bytes", dest.stat().st_size)
    # Deploy notes
    for host in PAGES:
        note = ROOT / "sites" / host / "overlay" / "DEPLOY-HUB-KEEP-LIVE.md"
        note.write_text(
            f"# Deploy — {TAG}\n\n"
            f"Confirmed 1.2: hub hard reclaim + deepen keep FI/ES/CA.\n"
            f"Stamp **{DATE}**. No new domains / no lookalike .co.uk.\n"
            f"No consumer ops notes.\n\n"
            f"Tool: `tools/kakobuy_hub_keep_live.py --load-env … --deploy --verify --gsc`\n",
            encoding="utf-8",
        )
    return outs


def deploy(built: dict[str, Path], store_internal: Path | None) -> dict:
    client = _connect()
    bak = f"/www/backup/{TAG}-{datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%S')}"
    _run(client, f"mkdir -p '{bak}'")
    sftp = client.open_sftp()
    for label, local in built.items():
        host, key = label.split(":", 1)
        remote = _remote_path(host, key)
        # backup
        bak_name = f"{host}__{key}.before".replace("/", "_")
        _run(client, f"cp -a '{remote}' '{bak}/{bak_name}' 2>/dev/null || true")
        # ensure dir
        if key not in ("home", "llms") and not key.startswith("data-"):
            _run(client, f"mkdir -p '{remote.rsplit('/', 1)[0]}'")
        if key.startswith("data-"):
            _run(client, f"mkdir -p '/www/wwwroot/{host}/data'")
        text = local.read_text(encoding="utf-8")
        if key.startswith("data-"):
            pass
        else:
            if f"{TAG}" not in text and f'data-hub-keep="{STAMP}"' not in text:
                raise SystemExit(f"refusing PUT without stamp: {remote}")
            if host != "kakobuydocs.com" and re.search(
                r"<h1>[^<]*Spreadsheet is a catalogue", text, re.I
            ):
                raise SystemExit(f"refusing spreadsheet hero PUT {remote}")
        sftp.put(str(local), remote)
        print("PUT", remote, "bytes", local.stat().st_size)

    # sitemap lastmod bumps
    today = DATE
    for host, pages in PAGES.items():
        sm_remote = f"/www/wwwroot/{host}/sitemap.xml"
        _run(client, f"cp -a '{sm_remote}' '{bak}/{host}-sitemap.xml.before' 2>/dev/null || true")
        try:
            with sftp.open(sm_remote, "r") as fh:
                sm = fh.read().decode("utf-8", "replace")
        except OSError:
            continue
        for key, path in pages:
            if key.startswith("data-") or key == "llms":
                continue
            loc = f"https://{host}{path}"
            sm = re.sub(
                rf"(<loc>{re.escape(loc)}</loc>\s*<lastmod>)[^<]+",
                rf"\g<1>{today}",
                sm,
                count=1,
            )
        with sftp.open(sm_remote, "w") as fh:
            fh.write(sm)
        print("sitemap", host, "→", today)

    sftp.close()
    _run(
        client,
        " && ".join(
            [
                f"chown -R www:www /www/wwwroot/{h} 2>/dev/null || true"
                for h in PAGES
            ]
        ),
    )
    meta = {"backup": bak, "tag": TAG, "stamp": STAMP}
    if store_internal:
        store_internal.mkdir(parents=True, exist_ok=True)
        (store_internal / "backup.txt").write_text(bak + "\n")
    print("BACKUP", bak)
    client.close()
    return meta


def verify() -> dict:
    checks = []

    def grab(url: str) -> tuple[int, str, str]:
        req = Request(url, headers={"User-Agent": UA})
        with urlopen(req, timeout=40) as resp:
            body = resp.read().decode("utf-8", "replace")
            return resp.status, body, resp.geturl()

    # Hub
    for path, need in (
        (
            "/kakobuy-spreadsheet/",
            ("Spreadsheet 2026", "Independent Index", ROW_DISP, DATE, "Open directory"),
        ),
        ("/", ("Independent Index", ROW_DISP, DATE)),
        ("/finds-dataset/", (DATE, ROW_DISP)),
        ("/kakobuy-coupons/", (DATE,)),
    ):
        url = f"{HUB}{path}"
        code, body, final = grab(url)
        row = {
            "url": url,
            "http": code,
            "final": final,
            "has_year": YEAR in body and ("Spreadsheet 2026" in body or path == "/"),
            "has_index": ROW_DISP in body,
            "has_date": DATE in body,
            "tag": TAG in body or f'data-hub-keep="{STAMP}"' in body,
        }
        for n in need:
            row[f"need_{n[:12]}"] = n in body
        title_m = re.search(r"<title>(.*?)</title>", body, re.S | re.I)
        row["title"] = re.sub(r"\s+", " ", title_m.group(1)).strip() if title_m else None
        checks.append(row)

    # JSON
    for path in ("/data/finds-dataset.json", "/data/coupons-truth.json"):
        url = f"{HUB}{path}"
        code, body, _ = grab(url)
        data = json.loads(body)
        checks.append(
            {
                "url": url,
                "http": code,
                "last_verified": data.get("last_verified"),
                "platform_opt": data.get("platform_opt"),
                "row_count": data.get("row_count"),
                "ok": data.get("last_verified") == DATE and data.get("platform_opt") == TAG,
            }
        )

    # Keep desks
    desk_specs = [
        (
            "https://kakobuy.fi/",
            {"Posti": True, "Tulli": True, "hub": HUB, "no_sheet_h1": True},
        ),
        (
            "https://kakospreadsheet.es/",
            {"Correos": True, "AEAT": True, "hub": HUB, "no_sheet_h1": True},
        ),
        (
            "https://kakospreadsheet.ca/",
            {"Canada Post": True, "CBSA": True, "hub": HUB, "no_sheet_h1": True},
        ),
        (
            "https://kakospreadsheet.ca/kakobuy-shipping/",
            {"Canada Post": True, "CBSA": True, "hub": HUB, "no_sheet_title": True},
        ),
        (
            "https://kakospreadsheet.ca/kakobuy-spreadsheet/",
            {"Canada Post": True, "hub": HUB, "no_sheet_title": True, "no_sheet_h1_cat": True},
        ),
        (
            "https://kakobuy.fi/kakobuy-kokemuksia/",
            {"Posti": True, "hub": HUB},
        ),
        (
            "https://kakospreadsheet.es/envio-kakobuy-espana/",
            {"Correos": True, "hub": HUB},
        ),
    ]
    for url, spec in desk_specs:
        code, body, final = grab(url)
        title_m = re.search(r"<title>(.*?)</title>", body, re.S | re.I)
        title = re.sub(r"\s+", " ", title_m.group(1)).strip() if title_m else ""
        h1_m = re.search(r"<h1[^>]*>(.*?)</h1>", body, re.S | re.I)
        h1 = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", h1_m.group(1) if h1_m else "")).strip()
        visible = re.sub(r"<!--.*?-->", "", body, flags=re.S)
        visible = re.sub(r'\sdata-[\w-]+=("[^"]*"|\'[^\']*\')', "", visible)
        ops_hits = [n for n in FORBIDDEN_CONSUMER if n in visible]
        row = {
            "url": url,
            "http": code,
            "title": title[:140],
            "h1": h1[:140],
            "tag": f'data-hub-keep="{STAMP}"' in body or TAG in body,
            "ops_hits": ops_hits,
        }
        for tok, _ in [(k, v) for k, v in spec.items() if k not in ("hub",) and not k.startswith("no_")]:
            row[tok] = tok in body
        if "hub" in spec:
            row["hub_uplink"] = HUB in body and (
                "hub-uplink" in body or "finds-dataset" in body or "kakobuy-spreadsheet" in body
            )
        if spec.get("no_sheet_h1"):
            row["spreadsheet_h1"] = bool(re.search(r"<h1>[^<]*Spreadsheet", body, re.I))
        if spec.get("no_sheet_title"):
            row["title_spreadsheet_hero"] = bool(
                re.search(r"Spreadsheet in English", title, re.I)
            )
        if spec.get("no_sheet_h1_cat"):
            row["sheet_catalogue_h1"] = "Spreadsheet is a catalogue" in h1
        checks.append(row)

    # Twins still 301
    twins = []
    import http.client
    from urllib.parse import urlparse

    for t in (
        "https://kakobuytips.com/",
        "https://kakospreadsheet.fr/",
        "https://kakospreadsheet.nl/",
    ):
        u = urlparse(t)
        conn = http.client.HTTPSConnection(u.netloc, timeout=20)
        conn.request("GET", "/", headers={"User-Agent": UA})
        r = conn.getresponse()
        twins.append({"url": t, "http": r.status, "location": r.getheader("Location")})
        conn.close()

    return {
        "at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "tag": TAG,
        "checks": checks,
        "twins": twins,
    }


def verify_ok(ver: dict) -> bool:
    bad = []
    for c in ver["checks"]:
        if c.get("http") not in (200, None) and "error" not in c:
            if c.get("http") != 200:
                bad.append(c)
                continue
        if "ok" in c and not c["ok"]:
            bad.append(c)
        if c.get("ops_hits"):
            bad.append(c)
        if c.get("spreadsheet_h1") or c.get("title_spreadsheet_hero") or c.get("sheet_catalogue_h1"):
            bad.append(c)
        if c.get("url", "").startswith(HUB) and c.get("url", "").endswith("/kakobuy-spreadsheet/"):
            if not (c.get("has_year") and c.get("has_index") and c.get("has_date")):
                bad.append(c)
        if "Canada Post" in c and c.get("Canada Post") is False:
            bad.append(c)
        if "Posti" in c and c.get("Posti") is False:
            bad.append(c)
        if "Correos" in c and c.get("Correos") is False:
            bad.append(c)
    twin_bad = [
        t
        for t in ver.get("twins", [])
        if t.get("http") not in (301, 302)
        or "kakobuydocs.com" not in (t.get("location") or "")
    ]
    return not bad and not twin_bad, bad, twin_bad


def gsc_submit(sa: Path, out_path: Path) -> dict:
    try:
        from google.oauth2 import service_account
        from googleapiclient.discovery import build as gbuild
    except ImportError:
        import subprocess

        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "google-api-python-client", "google-auth", "-q"]
        )
        from google.oauth2 import service_account
        from googleapiclient.discovery import build as gbuild

    creds = service_account.Credentials.from_service_account_file(
        str(sa),
        scopes=["https://www.googleapis.com/auth/webmasters"],
    )
    gsc = gbuild("searchconsole", "v1", credentials=creds, cache_discovery=False)
    results = []
    for host in PAGES:
        site = f"sc-domain:{host}"
        feed = f"https://{host}/sitemap.xml"
        try:
            gsc.sitemaps().submit(siteUrl=site, feedpath=feed).execute()
            results.append({"site": site, "feed": feed, "ok": True})
            print("GSC_SUBMIT", site)
        except Exception as exc:  # noqa: BLE001
            results.append({"site": site, "feed": feed, "ok": False, "error": str(exc)})
            print("GSC_WARN", site, exc)
    out = {
        "submitted_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "results": results,
    }
    out_path.write_text(json.dumps(out, indent=2) + "\n")
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--load-env", type=Path)
    ap.add_argument("--build-only", action="store_true")
    ap.add_argument("--deploy", action="store_true")
    ap.add_argument("--verify", action="store_true")
    ap.add_argument("--gsc", action="store_true")
    ap.add_argument("--store-internal", type=Path, default=None)
    ap.add_argument(
        "--gsc-sa",
        type=Path,
        default=STORE / "internal" / "gsc-sa.json",
    )
    args = ap.parse_args()
    if args.load_env:
        _load_env(args.load_env)

    built = build()
    if args.build_only and not args.deploy:
        print("BUILD_ONLY done", len(built))
        return

    meta: dict = {}
    if args.deploy:
        meta = deploy(built, args.store_internal)

    if args.verify or args.deploy:
        time.sleep(3)
        ver = verify()
        ver["backup"] = meta.get("backup")
        ok, bad, twin_bad = verify_ok(ver)
        ver["all_ok"] = ok
        ver["bad"] = bad
        ver["twin_bad"] = twin_bad
        if args.store_internal:
            args.store_internal.mkdir(parents=True, exist_ok=True)
            (args.store_internal / "live_verify.json").write_text(
                json.dumps(ver, indent=2) + "\n"
            )
        print(json.dumps({"all_ok": ok, "bad_n": len(bad), "twin_bad_n": len(twin_bad)}, indent=2))
        if not ok:
            print("VERIFY_FAIL", json.dumps(bad[:5], indent=2))
            print("TWIN_BAD", twin_bad)
            sys.exit(2)
        print("VERIFY_OK")

    if args.gsc:
        out = (args.store_internal or Path("/tmp")) / "gsc_sitemap_submit.json"
        gsc_submit(args.gsc_sa, out)


if __name__ == "__main__":
    main()
