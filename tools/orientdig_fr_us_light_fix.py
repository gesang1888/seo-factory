#!/usr/bin/env python3
"""OrientDig FR + US keep light-fix (strategy action 2): remove Spreadsheet hero,
align Colissimo / USPS + #local hub uplink to orientdig.es.

KEEP desks only — do NOT reclaim hub orientdig.es; do NOT deepen watch AT/DE/UK;
do NOT revive twins (spreadsheet.nl/.it→es, spreadsheet.fr→fr, spreadsheet.us→us).
"""
from __future__ import annotations

import json
import os
import re
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STAMP = "20261028"
MARKER_FR = f'data-fr-light-fix="{STAMP}"'
MARKER_US = f'data-us-light-fix="{STAMP}"'
HUB = "https://orientdig.es/"

FR_HOST = "orientdig.fr"
US_HOST = "orientdig.us"

FR_TITLE = "OrientDig France — Colissimo, pas un code postal belge"
US_TITLE = "OrientDig United States — USPS, CBP, ZIP notes"

LOCAL_FR = f"""
<section class="sg-sec" id="local" data-platform-opt="orientdig-platform-20261026" {MARKER_FR} data-keep="1" style="max-width:72rem;margin:1.25rem auto;padding:0 1.25rem">
  <h2>Desk FR · Colissimo, code postal à cinq chiffres</h2>
  <p class="ssub">orientdig.fr = <strong>keep</strong> country desk (Colissimo / douane FR). Brand spreadsheet + coupons → <a href="{HUB}">orientdig.es</a>.</p>
  <ol class="local-steps" style="margin:12px 0 0;padding:0;list-style:none;display:grid;gap:12px">
    <li style="border:1px solid #e5e7eb;border-radius:12px;padding:14px 16px;background:#fff"><strong style="display:block;margin:0 0 6px">Destination estimateur : France</strong><span style="display:block;color:#334155;line-height:1.7">Choisir <strong>FR</strong>, pas EU, pas BE. Un code postal belge à quatre chiffres est le mauvais pays.</span></li>
    <li style="border:1px solid #e5e7eb;border-radius:12px;padding:14px 16px;background:#fff"><strong style="display:block;margin:0 0 6px">Adresse FR · CP 5 chiffres</strong><span style="display:block;color:#334155;line-height:1.7">Rue française + code postal à cinq chiffres. Ce desk n’est pas la Belgique.</span></li>
    <li style="border:1px solid #e5e7eb;border-radius:12px;padding:14px 16px;background:#fff"><strong style="display:block;margin:0 0 6px">Droits / douane</strong><span style="display:block;color:#334155;line-height:1.7">La SKU décide (tax-free / prepaid / destinataire). <strong>Colissimo</strong> peut ajouter des frais en Collect. Source : <a href="https://www.douane.gouv.fr/" rel="noopener">douane.gouv.fr</a> le matin de l’envoi.</span></li>
    <li style="border:1px solid #e5e7eb;border-radius:12px;padding:14px 16px;background:#fff"><strong style="display:block;margin:0 0 6px">Dernier kilomètre · Colissimo</strong><span style="display:block;color:#334155;line-height:1.7">Souvent <strong>Colissimo</strong>. Les pages livraison / avis sur cet hôte restent — on ne les remplace pas par un héros Spreadsheet.</span></li>
  </ol>
  <p class="hub-uplink" style="margin:14px 0 0;padding:12px 14px;border-left:3px solid #0f766e;background:#f0fdfa;color:#134e4a;line-height:1.6;font-size:15px;max-width:760px">Cherches le spreadsheet / dataset OrientDig ? Utilise le hub <a href="{HUB}" style="color:#0f766e;font-weight:600">orientdig.es</a> (Independent Index · 8,000+ · <a href="{HUB}finds-dataset/" style="color:#0f766e;font-weight:600">dataset</a> · <a href="{HUB}orientdig-coupons/" style="color:#0f766e;font-weight:600">cupones</a>). Cet hôte reste un desk <strong>keep</strong> FR — pas un second hub.</p>
  <p class="local-src" style="font-size:14px;color:#334155;line-height:1.7;margin:14px 0 0">Money local : <a href="/">accueil</a> · <a href="/orientdig-freight/">livraison</a> · <a href="/avis-orientdig/">avis</a> · hub <a href="{HUB}">orientdig.es</a></p>
</section>
""".strip()

LOCAL_US = f"""
<section class="sg-sec" id="local" data-platform-opt="orientdig-platform-20261026" {MARKER_US} data-keep="1" style="max-width:72rem;margin:1.25rem auto;padding:0 1.25rem">
  <h2>US desk · USPS, CBP, ZIP</h2>
  <p class="ssub">orientdig.us = <strong>keep</strong> country desk (USPS / USD / CBP). Brand spreadsheet + coupons → <a href="{HUB}">orientdig.es</a>.</p>
  <ol class="local-steps" style="margin:12px 0 0;padding:0;list-style:none;display:grid;gap:12px">
    <li style="border:1px solid #e5e7eb;border-radius:12px;padding:14px 16px;background:#fff"><strong style="display:block;margin:0 0 6px">Estimator destination: United States</strong><span style="display:block;color:#334155;line-height:1.7">Pick <strong>US</strong>, not this TLD, not “EU”. A Canadian postal code is the wrong country.</span></li>
    <li style="border:1px solid #e5e7eb;border-radius:12px;padding:14px 16px;background:#fff"><strong style="display:block;margin:0 0 6px">US street + ZIP</strong><span style="display:block;color:#334155;line-height:1.7">US delivery address only. This desk does not file CBP entries.</span></li>
    <li style="border:1px solid #e5e7eb;border-radius:12px;padding:14px 16px;background:#fff"><strong style="display:block;margin:0 0 6px">Duties / CBP · de-minimis context</strong><span style="display:block;color:#334155;line-height:1.7">The booked SKU says tax-free / prepaid / collect. <strong>USPS</strong> or FedEx can add a collect fee. Source: <a href="https://www.cbp.gov/" rel="noopener">CBP</a> the morning you ship — this desk does not invent a de-minimis dollar.</span></li>
    <li style="border:1px solid #e5e7eb;border-radius:12px;padding:14px 16px;background:#fff"><strong style="display:block;margin:0 0 6px">Last mile · USPS</strong><span style="display:block;color:#334155;line-height:1.7">Often <strong>USPS</strong> or FedEx. Shipping pages on this host stay local — we do not overwrite them with a Spreadsheet hero.</span></li>
  </ol>
  <p class="hub-uplink" style="margin:14px 0 0;padding:12px 14px;border-left:3px solid #0f766e;background:#f0fdfa;color:#134e4a;line-height:1.6;font-size:15px;max-width:760px">Looking for the OrientDig spreadsheet / dataset? Use hub <a href="{HUB}" style="color:#0f766e;font-weight:600">orientdig.es</a> (Independent Index · 8,000+ · <a href="{HUB}finds-dataset/" style="color:#0f766e;font-weight:600">dataset</a> · <a href="{HUB}orientdig-coupons/" style="color:#0f766e;font-weight:600">coupons</a>). This host stays a US <strong>keep</strong> desk — not a second hub.</p>
  <p class="local-src" style="font-size:14px;color:#334155;line-height:1.7;margin:14px 0 0">Money local: <a href="/">home</a> · <a href="/orientdig-freight/">shipping</a> · <a href="/orientdig-coupons/">coupons article</a> · hub <a href="{HUB}">orientdig.es</a></p>
</section>
""".strip()

FREIGHT_UPLINK_FR = (
    f'<p class="hub-uplink" data-fr-light-fix="{STAMP}" style="margin:14px 0;padding:12px 14px;'
    f'border-left:3px solid #0f766e;background:#f0fdfa;color:#134e4a;line-height:1.6;max-width:760px">'
    f"Spreadsheet / dataset OrientDig → hub <a href=\"{HUB}\">orientdig.es</a>. "
    f"Cette page reste livraison / douane FR (Colissimo) — pas un héros Spreadsheet.</p>"
)

FREIGHT_UPLINK_US = (
    f'<p class="hub-uplink" data-us-light-fix="{STAMP}" style="margin:14px 0;padding:12px 14px;'
    f'border-left:3px solid #0f766e;background:#f0fdfa;color:#134e4a;line-height:1.6;max-width:760px">'
    f"OrientDig spreadsheet / dataset → hub <a href=\"{HUB}\">orientdig.es</a>. "
    f"This page stays US shipping / CBP (USPS) — not a Spreadsheet hero.</p>"
)

AVIS_SNIPPET = (
    f'<p class="hub-uplink" data-fr-light-fix="{STAMP}" style="margin:14px 0;padding:12px 14px;'
    f'border-left:3px solid #0f766e;background:#f0fdfa;color:#134e4a;line-height:1.6;max-width:760px">'
    f"Avis et Colissimo pour une adresse en France restent ici. "
    f"Catalogue / spreadsheet → <a href=\"{HUB}\">orientdig.es</a>.</p>"
)


def _sub_title(html: str, title: str) -> str:
    return re.sub(r"<title>.*?</title>", f"<title>{title}</title>", html, count=1, flags=re.S)


def _replace_local(html: str, block: str) -> str:
    if 'id="local"' in html:
        return re.sub(
            r'<section[^>]*id="local"[^>]*>[\s\S]*?</section>',
            block,
            html,
            count=1,
        )
    # insert before agent / first major sec if missing
    return re.sub(
        r'(<section[^>]*id="agent"[^>]*>)',
        block + "\n\\1",
        html,
        count=1,
    )


def patch_fr_home(html: str) -> str:
    html = _sub_title(html, FR_TITLE)
    html = re.sub(
        r'<meta name="description" content="[^"]*"',
        (
            '<meta name="description" content="OrientDig France keep desk: Colissimo, code postal '
            "à cinq chiffres, douane FR. Pas un héros Spreadsheet — catalogue → orientdig.es.\""
        ),
        html,
        count=1,
    )
    html = re.sub(
        r'("name":\s*")OrientDig Spreadsheet[^"]*(")',
        rf'\1{FR_TITLE}\2',
        html,
        count=1,
    )
    html = html.replace("<span>Spreadsheet</span>", "<span>France</span>", 1)
    html = re.sub(
        r'<span class="eyebrow">.*?</span>',
        '<span class="eyebrow">Desk FR keep · Colissimo · pas un code postal belge</span>',
        html,
        count=1,
        flags=re.S,
    )
    html = re.sub(
        r"<h1>.*?</h1>",
        "<h1>OrientDig pour une adresse en France</h1>",
        html,
        count=1,
        flags=re.S,
    )
    html = re.sub(
        r'<p class="lead">.*?</p>',
        (
            '<p class="lead">Assistant livraison <strong>France</strong> : estimateur destination FR, '
            "<strong>Colissimo</strong> dernier kilomètre, code postal à cinq chiffres "
            "(≠ Belgique), notes douane. Le spreadsheet / dataset reste sur "
            f'<a href="{HUB}">orientdig.es</a> — cet hôte n’est pas un second hub.</p>'
        ),
        html,
        count=1,
        flags=re.S,
    )
    html = _replace_local(html, LOCAL_FR)
    html = html.replace("<h3>OrientDig Spreadsheet</h3>", "<h3>OrientDig France desk</h3>", 1)
    html = html.replace(
        "OrientDig Spreadsheet est un site d’information indépendant.",
        "Ce desk France (orientdig.fr) est un site d’information indépendant.",
        1,
    )
    html = html.replace(
        "&copy; 2026 OrientDig Spreadsheet.",
        "&copy; 2026 OrientDig France desk (orientdig.fr).",
        1,
    )
    if MARKER_FR not in html.replace(LOCAL_FR, ""):
        html = html.replace("<html", f"<html {MARKER_FR}", 1)
    elif MARKER_FR not in html.split(">", 1)[0]:
        html = html.replace("<html", f"<html {MARKER_FR}", 1)
    return html


def patch_us_home(html: str) -> str:
    html = _sub_title(html, US_TITLE)
    html = re.sub(
        r'<meta name="description" content="[^"]*"',
        (
            '<meta name="description" content="OrientDig United States keep desk: USPS last-mile, '
            'CBP / de-minimis context, US ZIP. Not a Spreadsheet hero — catalogue → orientdig.es."'
        ),
        html,
        count=1,
    )
    html = re.sub(
        r'("name":\s*")OrientDig Spreadsheet[^"]*(")',
        rf'\1{US_TITLE}\2',
        html,
        count=1,
    )
    html = html.replace("<span>Spreadsheet</span>", "<span>United States</span>", 1)
    html = re.sub(
        r'<span class="eyebrow">.*?</span>',
        '<span class="eyebrow">US keep desk · USPS · CBP · ZIP</span>',
        html,
        count=1,
        flags=re.S,
    )
    html = re.sub(
        r"<h1>.*?</h1>",
        "<h1>OrientDig for a US delivery address</h1>",
        html,
        count=1,
        flags=re.S,
    )
    html = re.sub(
        r'<p class="lead">.*?</p>',
        (
            '<p class="lead">United States landing assistant: estimator destination <strong>US</strong>, '
            "<strong>USPS</strong> last-mile notes, CBP / de-minimis context, US ZIP — "
            "not a global OrientDig Spreadsheet hero. Brand spreadsheet stays on "
            f'<a href="{HUB}">orientdig.es</a>.</p>'
        ),
        html,
        count=1,
        flags=re.S,
    )
    html = _replace_local(html, LOCAL_US)
    html = html.replace("<h3>OrientDig Spreadsheet</h3>", "<h3>OrientDig United States desk</h3>", 1)
    html = html.replace(
        "OrientDig Spreadsheet is an independent information site.",
        "This United States desk (orientdig.us) is an independent information site.",
        1,
    )
    html = html.replace(
        "&copy; 2026 OrientDig Spreadsheet.",
        "&copy; 2026 OrientDig United States desk (orientdig.us).",
        1,
    )
    if "<html" in html and MARKER_US not in html.split(">", 1)[0]:
        html = html.replace("<html", f"<html {MARKER_US}", 1)
    return html


def patch_fr_freight(html: str) -> str:
    title = "OrientDig France — livraison Colissimo et douane"
    html = _sub_title(html, title)
    html = re.sub(
        r'("name":\s*")OrientDig Spreadsheet[^"]*(")',
        rf'\1{title}\2',
        html,
        count=1,
    )
    html = html.replace("<span>Spreadsheet</span>", "<span>France</span>", 1)
    html = html.replace("<h3>OrientDig Spreadsheet</h3>", "<h3>OrientDig France desk</h3>", 1)
    html = html.replace(
        "&copy; 2026 OrientDig Spreadsheet.",
        "&copy; 2026 OrientDig France desk (orientdig.fr).",
        1,
    )
    if "hub-uplink" not in html:
        html = re.sub(r"(</h1>)", r"\1\n" + FREIGHT_UPLINK_FR, html, count=1)
    if MARKER_FR not in html.split(">", 1)[0]:
        html = html.replace("<html", f"<html {MARKER_FR}", 1)
    return html


def patch_us_freight(html: str) -> str:
    title = "OrientDig United States — USPS shipping and CBP notes"
    html = _sub_title(html, title)
    html = re.sub(
        r'("name":\s*")OrientDig Spreadsheet[^"]*(")',
        rf'\1{title}\2',
        html,
        count=1,
    )
    html = html.replace("<span>Spreadsheet</span>", "<span>United States</span>", 1)
    html = html.replace("<h3>OrientDig Spreadsheet</h3>", "<h3>OrientDig United States desk</h3>", 1)
    html = html.replace(
        "&copy; 2026 OrientDig Spreadsheet.",
        "&copy; 2026 OrientDig United States desk (orientdig.us).",
        1,
    )
    if "hub-uplink" not in html:
        html = re.sub(r"(</h1>)", r"\1\n" + FREIGHT_UPLINK_US, html, count=1)
    if MARKER_US not in html.split(">", 1)[0]:
        html = html.replace("<html", f"<html {MARKER_US}", 1)
    return html


def patch_fr_avis(html: str) -> str:
    # title already local; thicken with Colissimo + hub uplink only
    if "hub-uplink" not in html and "Colissimo" not in html:
        # insert after first h2 if present, else after body open content
        if re.search(r"<h2[^>]*>", html):
            html = re.sub(r"(</h2>)", r"\1\n" + AVIS_SNIPPET, html, count=1)
        else:
            html = re.sub(
                r'(<main[^>]*>|<article[^>]*>|<div class="content"[^>]*>)',
                r"\1\n" + AVIS_SNIPPET,
                html,
                count=1,
            )
    elif "hub-uplink" not in html:
        html = re.sub(r"(</h2>)", r"\1\n" + AVIS_SNIPPET, html, count=1)
    if MARKER_FR not in html.split(">", 1)[0]:
        html = html.replace("<html", f"<html {MARKER_FR}", 1)
    return html


def _assert_home(label: str, html: str, must: tuple[str, ...], forbid_h1_spreadsheet: bool = True) -> None:
    missing = [t for t in must if t not in html]
    if missing:
        raise SystemExit(f"{label} missing tokens: {missing}")
    h1 = re.search(r"<h1[^>]*>(.*?)</h1>", html, re.S)
    if forbid_h1_spreadsheet and h1 and re.search(r"spreadsheet", h1.group(1), re.I):
        raise SystemExit(f"{label} H1 still has Spreadsheet")
    title = re.search(r"<title>(.*?)</title>", html, re.S)
    if title and re.search(r"spreadsheet", title.group(1), re.I):
        raise SystemExit(f"{label} title still has Spreadsheet")


def build() -> dict[str, Path]:
    fr_overlay = ROOT / "sites" / "orientdig.fr" / "overlay"
    us_overlay = ROOT / "sites" / "orientdig.us" / "overlay"
    paths = {
        "fr_home": fr_overlay / "live-base.index.html",
        "us_home": us_overlay / "live-base.index.html",
        "fr_freight": fr_overlay / "orientdig-freight" / "live-base.index.html",
        "us_freight": us_overlay / "orientdig-freight" / "live-base.index.html",
        "fr_avis": fr_overlay / "avis-orientdig" / "live-base.index.html",
    }
    for k, p in paths.items():
        if not p.is_file():
            raise SystemExit(f"missing live-base: {p}")

    out: dict[str, Path] = {}
    fr_home = patch_fr_home(paths["fr_home"].read_text(encoding="utf-8"))
    _assert_home(
        "fr_home",
        fr_home,
        ("Colissimo", 'id="local"', HUB, "adresse en France", "keep", MARKER_FR),
    )
    out["fr_home"] = fr_overlay / "index.html.fr-light-fix"
    out["fr_home"].write_text(fr_home, encoding="utf-8")

    us_home = patch_us_home(paths["us_home"].read_text(encoding="utf-8"))
    _assert_home(
        "us_home",
        us_home,
        ("USPS", "CBP", 'id="local"', HUB, "US delivery address", "keep", MARKER_US),
    )
    out["us_home"] = us_overlay / "index.html.us-light-fix"
    out["us_home"].write_text(us_home, encoding="utf-8")

    fr_freight = patch_fr_freight(paths["fr_freight"].read_text(encoding="utf-8"))
    _assert_home("fr_freight", fr_freight, ("Colissimo", HUB, MARKER_FR), forbid_h1_spreadsheet=False)
    out["fr_freight"] = fr_overlay / "orientdig-freight" / "index.html.fr-light-fix"
    out["fr_freight"].parent.mkdir(parents=True, exist_ok=True)
    out["fr_freight"].write_text(fr_freight, encoding="utf-8")

    us_freight = patch_us_freight(paths["us_freight"].read_text(encoding="utf-8"))
    _assert_home("us_freight", us_freight, ("USPS", "CBP", HUB, MARKER_US), forbid_h1_spreadsheet=False)
    out["us_freight"] = us_overlay / "orientdig-freight" / "index.html.us-light-fix"
    out["us_freight"].parent.mkdir(parents=True, exist_ok=True)
    out["us_freight"].write_text(us_freight, encoding="utf-8")

    fr_avis = patch_fr_avis(paths["fr_avis"].read_text(encoding="utf-8"))
    if HUB not in fr_avis or "Colissimo" not in fr_avis:
        raise SystemExit("fr_avis missing Colissimo or hub uplink")
    out["fr_avis"] = fr_overlay / "avis-orientdig" / "index.html.fr-light-fix"
    out["fr_avis"].parent.mkdir(parents=True, exist_ok=True)
    out["fr_avis"].write_text(fr_avis, encoding="utf-8")

    for k, p in out.items():
        print("wrote", k, p, "bytes", p.stat().st_size)
    return out


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
    os.environ["ORIGIN_SSH_PASS"] = password  # do not print
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(host, username="root", password=password, timeout=30, allow_agent=False, look_for_keys=False)
    return client


def _run(client, cmd: str, timeout: int = 120) -> str:
    _, stdout, stderr = client.exec_command(cmd, timeout=timeout)
    return (stdout.read() + stderr.read()).decode(errors="replace").strip()


def _bump_sitemap(sm: str, locs: list[str], today: str) -> str:
    for loc in locs:
        sm = re.sub(
            rf"(<loc>{re.escape(loc)}</loc>\s*<lastmod>)[^<]+",
            rf"\g<1>{today}",
            sm,
            count=1,
        )
    return sm


def deploy() -> str:
    out = build()
    client = _connect()
    stamp = time.strftime("%Y%m%d-%H%M%S")
    bak = f"/www/backup/orientdig-fr-us-light-fix-{stamp}"
    _run(client, f"mkdir -p '{bak}/fr' '{bak}/us'")

    forbidden = [
        "orientdig.es",
        "orientdig.at",
        "orientdigspreadsheet.de",
        "orientdigspreadsheet.uk",
        "orientdigspreadsheet.nl",
        "orientdigspreadsheet.it",
        "orientdigspreadsheet.fr",
        "orientdigspreadsheet.us",
    ]
    sftp = client.open_sftp()

    # capture hub + watch mtimes before writes (must stay unchanged)
    before_mtimes = _run(
        client,
        "stat -c '%n %Y' "
        "/www/wwwroot/orientdig.es/index.html "
        "/www/wwwroot/orientdig.at/index.html "
        "/www/wwwroot/orientdigspreadsheet.de/index.html "
        "/www/wwwroot/orientdigspreadsheet.uk/index.html "
        "2>/dev/null || true",
    )

    pairs = [
        (out["fr_home"], f"/www/wwwroot/{FR_HOST}/index.html", f"{bak}/fr/index.html.before", ("Colissimo", 'id="local"')),
        (out["fr_freight"], f"/www/wwwroot/{FR_HOST}/orientdig-freight/index.html", f"{bak}/fr/orientdig-freight.index.html.before", ("Colissimo", HUB)),
        (out["fr_avis"], f"/www/wwwroot/{FR_HOST}/avis-orientdig/index.html", f"{bak}/fr/avis-orientdig.index.html.before", ("Colissimo", HUB)),
        (out["us_home"], f"/www/wwwroot/{US_HOST}/index.html", f"{bak}/us/index.html.before", ("USPS", 'id="local"')),
        (out["us_freight"], f"/www/wwwroot/{US_HOST}/orientdig-freight/index.html", f"{bak}/us/orientdig-freight.index.html.before", ("USPS", HUB)),
    ]

    for local, remote, bak_path, need in pairs:
        raw = local.read_text(encoding="utf-8")
        for token in need:
            if token not in raw:
                raise SystemExit(f"refusing PUT {remote}: missing {token}")
        h1 = re.search(r"<h1[^>]*>(.*?)</h1>", raw, re.S)
        if h1 and re.search(r"spreadsheet", h1.group(1), re.I) and remote.endswith("/index.html") and "/orientdig-freight/" not in remote and "/avis-" not in remote:
            raise SystemExit(f"refusing Spreadsheet hero on {remote}")
        if any(f"/www/wwwroot/{h}" in remote for h in forbidden):
            raise SystemExit(f"refusing forbidden host path {remote}")
        _run(client, f"cp -a '{remote}' '{bak_path}'")
        sftp.put(str(local), remote)
        _run(client, f"chown www:www '{remote}'")
        print("PUT", remote, "bytes", local.stat().st_size)

    today = time.strftime("%Y-%m-%d")
    for host, locs in (
        (
            FR_HOST,
            [
                f"https://{FR_HOST}/",
                f"https://{FR_HOST}/orientdig-freight/",
                f"https://{FR_HOST}/avis-orientdig/",
            ],
        ),
        (
            US_HOST,
            [
                f"https://{US_HOST}/",
                f"https://{US_HOST}/orientdig-freight/",
            ],
        ),
    ):
        sm_remote = f"/www/wwwroot/{host}/sitemap.xml"
        bak_sm = f"{bak}/{host.split('.')[-1] if False else host}/sitemap.xml.before".replace(
            f"{bak}/{host}/", f"{bak}/{'fr' if host.endswith('.fr') else 'us'}/"
        )
        # simpler bak path
        side = "fr" if host.endswith(".fr") else "us"
        bak_sm = f"{bak}/{side}/sitemap.xml.before"
        _run(client, f"cp -a '{sm_remote}' '{bak_sm}'")
        with sftp.open(sm_remote, "r") as f:
            sm = f.read().decode("utf-8", "replace")
        sm = _bump_sitemap(sm, locs, today)
        with sftp.open(sm_remote, "w") as f:
            f.write(sm)
        print("sitemap", host, "lastmod →", today)

    after_mtimes = _run(
        client,
        "stat -c '%n %Y' "
        "/www/wwwroot/orientdig.es/index.html "
        "/www/wwwroot/orientdig.at/index.html "
        "/www/wwwroot/orientdigspreadsheet.de/index.html "
        "/www/wwwroot/orientdigspreadsheet.uk/index.html "
        "2>/dev/null || true",
    )
    if before_mtimes != after_mtimes:
        raise SystemExit("hub/watch mtimes changed — abort integrity")

    twin_check = _run(
        client,
        "echo '--- twin / watch / hub (expect NO writes this round) ---'; "
        "for h in orientdig.es orientdig.at orientdigspreadsheet.de orientdigspreadsheet.uk "
        "orientdigspreadsheet.nl orientdigspreadsheet.it orientdigspreadsheet.fr orientdigspreadsheet.us; do "
        "  echo -n \"$h \"; test -d /www/wwwroot/$h && echo HAS_DIR || echo NO_DIR; "
        "done; "
        f"ls '/www/wwwroot/{FR_HOST}/index.html' '/www/wwwroot/{US_HOST}/index.html'",
    )
    print(twin_check)
    print("backup", bak)
    print("mtimes_ok", before_mtimes.replace("\n", " | "))
    sftp.close()
    client.close()
    return bak


def verify(out_json: Path | None = None) -> dict:
    import urllib.request

    ua = {"User-Agent": "Mozilla/5.0 orientdig-fr-us-light-fix"}

    def fetch(url: str) -> tuple[int, str]:
        req = urllib.request.Request(url, headers=ua)
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                return r.status, r.read().decode("utf-8", "replace")
        except Exception as e:
            return 0, str(e)

    results: dict = {"checked_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "urls": {}}
    checks = [
        ("fr_home", f"https://{FR_HOST}/", ("Colissimo", "adresse en France", 'id="local"', HUB), True),
        ("us_home", f"https://{US_HOST}/", ("USPS", "US delivery address", 'id="local"', HUB), True),
        ("fr_freight", f"https://{FR_HOST}/orientdig-freight/", ("Colissimo", HUB), False),
        ("us_freight", f"https://{US_HOST}/orientdig-freight/", ("USPS", HUB), False),
        ("fr_avis", f"https://{FR_HOST}/avis-orientdig/", ("Colissimo", HUB), False),
        ("hub", HUB, (), False),
    ]
    for key, url, must, no_sheet_h1 in checks:
        code, body = fetch(url)
        title_m = re.search(r"<title>(.*?)</title>", body, re.S)
        h1_m = re.search(r"<h1[^>]*>(.*?)</h1>", body, re.S)
        title = re.sub(r"\s+", " ", title_m.group(1)).strip() if title_m else None
        h1 = re.sub(r"<[^>]+>", "", re.sub(r"\s+", " ", h1_m.group(1))).strip() if h1_m else None
        missing = [t for t in must if t not in body]
        sheet_h1 = bool(h1 and re.search(r"spreadsheet", h1, re.I))
        sheet_title = bool(title and re.search(r"spreadsheet", title, re.I))
        ok = code == 200 and not missing and (not no_sheet_h1 or (not sheet_h1 and not sheet_title))
        results["urls"][key] = {
            "url": url,
            "http": code,
            "title": title,
            "h1": h1,
            "missing": missing,
            "spreadsheet_in_h1": sheet_h1,
            "spreadsheet_in_title": sheet_title,
            "ok": ok,
        }
    # twin 301 spot-check
    for twin, expect in (
        ("https://orientdigspreadsheet.nl/", "orientdig.es"),
        ("https://orientdigspreadsheet.it/", "orientdig.es"),
        ("https://orientdigspreadsheet.fr/", "orientdig.fr"),
        ("https://orientdigspreadsheet.us/", "orientdig.us"),
    ):
        req = urllib.request.Request(twin, headers=ua, method="GET")
        try:
            opener = urllib.request.build_opener(urllib.request.HTTPRedirectHandler)
            # manual: no auto redirect
            class NoRedir(urllib.request.HTTPRedirectHandler):
                def redirect_request(self, req, fp, code, msg, headers, newurl):  # noqa: N803
                    return None

            opener = urllib.request.build_opener(NoRedir)
            try:
                opener.open(req, timeout=20)
                code, loc = 200, None
            except urllib.error.HTTPError as e:
                code = e.code
                loc = e.headers.get("Location")
        except Exception as e:
            code, loc = 0, str(e)
        results["urls"][f"twin:{twin}"] = {
            "http": code,
            "location": loc,
            "ok": code in (301, 302) and loc and expect in loc,
        }

    results["all_ok"] = all(v.get("ok") for v in results["urls"].values() if isinstance(v, dict) and "ok" in v)
    if out_json:
        out_json.parent.mkdir(parents=True, exist_ok=True)
        out_json.write_text(json.dumps(results, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(results, indent=2, ensure_ascii=False))
    return results


def main() -> None:
    if "--deploy" in sys.argv:
        bak = deploy()
        print("DEPLOY_OK", bak)
        return
    if "--verify" in sys.argv:
        out = Path(
            "/cursor/stores/bc-eb8405c7-0d3c-48be-958d-5f25b92c606c/internal/orientdig-fr-us-light-fix/live_verify.json"
        )
        verify(out)
        return
    build()


if __name__ == "__main__":
    main()
