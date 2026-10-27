#!/usr/bin/env python3
"""USFans NL keep light fix (strategy action 2): remove Spreadsheet title/H1
cannibal, keep #local Douane / NL postcode, ensure hub uplink to .net.

KEEP only — do NOT touch hub .net or UK .co.uk. Do NOT revive twin .uk (Phase C).
Surgical patch of the ranked Georgia homepage (do not wholesale-replace with thin CMS skin).
"""
from __future__ import annotations

import os
import re
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "sites" / "usfansspreadsheet.nl"
OVERLAY = SITE / "overlay"
STAMP = "20261027"
MARKER = f'data-nl-light-fix="{STAMP}"'
HOST = "usfansspreadsheet.nl"
HUB = "https://usfansspreadsheet.net/"

TITLE = "USFans Nederland — Nederlandse postcode"
H1 = "USFans voor een Nederlands adres"
DESC = (
    "USFans Nederland desk: Nederlandse postcode (1234 AB), Belastingdienst Douane, "
    "PostNL / DHL last-mile. Is USFans betrouwbaar voor NL? Brand spreadsheet → usfansspreadsheet.net."
)

LOCAL_HOME = f"""
<!-- portfolio-nl-light-fix-local -->
<section class="sg-sec" id="local" data-step4="1" data-platform-opt="1" data-nl-light-fix="{STAMP}" data-keep="1">
  <h2>Wat vandaag geldt voor een Nederlands adres</h2>
  <p class="ssub">usfansspreadsheet.nl · <strong>keep</strong> desk · Douane / NL-postcode / PostNL — geen tweede brand spreadsheet hub.</p>
  <ol class="local-steps">
    <li><strong>Estimator-bestemming: Nederland</strong><span>Kies NL in de officiële schatter — niet deze TLD, niet “EU”. Een Belgische of Duitse postcode is het verkeerde land.</span></li>
    <li><strong>Adres · vorm 1234 AB</strong><span>Nederlandse postcode (1234 AB), geen Duits afhaalautomaat-nummer en geen BE-postcode.</span></li>
    <li><strong>Invoer · Belastingdienst Douane</strong><span>De SKU beslist. DHL kan bij Collect extra innen. Bron: Belastingdienst Douane op de verzenddag. Geen verzonnen aangegeven waarde.</span></li>
    <li><strong>Laatste mile · PostNL / DHL</strong><span>Vaak DHL handoff of PostNL-achtige last-mile via de geboekte lijn. Bevestig de live SKU. Deze desk doet geen Douane-aangifte.</span></li>
    <li><strong>Betrouwbaar?</strong><span>Orders, betaling en tickets alleen op <a href="https://usfans.com/" rel="noopener">usfans.com</a>. Deze hostname is een onafhankelijke NL-infodesk — geen kassa, geen accounttoegang.</span></li>
  </ol>
  <p class="local-src">Officiële bron: <a href="https://www.belastingdienst.nl/wps/wcm/connect/nl/douane/" rel="noopener">Douane</a>. Lab 27 Oct 2026 · NL light-fix.</p>
  <p class="local-src">Money URLs (keep ≤6): <a href="/">Home</a> · <a href="/usfans-shipping-guide/">Shipping guide</a> · <a href="/usfans-coupons/">Coupons</a> · <a href="/is-usfans-legit/">Legit / betrouwbaar</a> · <a href="/usfans-freight/">Freight</a> · hub <a href="{HUB}">usfansspreadsheet.net</a></p>
  <p class="hub-uplink" data-step4-hub="1" data-nl-light-fix="{STAMP}">Global USFans spreadsheet / finds / coupons → <a href="{HUB}">usfansspreadsheet.net</a> (Independent Index · 10,601). Deze .nl-desk houdt alleen lokale framing (Douane / NL-postcode / PostNL / betrouwbaar) — brand spreadsheet-kopwoorden horen op de hub.</p>
</section>
<!-- /portfolio-nl-light-fix-local -->
""".strip()


def _sub_title(html: str, title: str) -> str:
    return re.sub(r"<title>.*?</title>", f"<title>{title}</title>", html, count=1, flags=re.S)


def patch_home(html: str) -> str:
    html = _sub_title(html, TITLE)
    html = re.sub(
        r'<meta name="description" content="[^"]*"',
        f'<meta name="description" content="{DESC}"',
        html,
        count=1,
    )
    # JSON-LD WebPage name
    html = re.sub(
        r'("name":\s*")USFans Spreadsheet in het Nederlands[^"]*(")',
        rf'\1{TITLE}\2',
        html,
        count=1,
    )
    html = re.sub(
        r'("description":\s*")Onafhankelijke gids in het Nederlands:[^"]*(")',
        rf'\1{DESC}\2',
        html,
        count=1,
    )
    # brand chip
    html = html.replace("<span>Spreadsheet</span>", "<span>Nederland</span>", 1)
    # hero — remove Spreadsheet cannibal
    html = re.sub(
        r'<span class="eyebrow">.*?</span>',
        '<span class="eyebrow">Nederland keep desk · Douane / postcode 1234 AB</span>',
        html,
        count=1,
        flags=re.S,
    )
    html = re.sub(
        r"<h1>.*?</h1>",
        f"<h1>{H1}</h1>",
        html,
        count=1,
        flags=re.S,
    )
    html = re.sub(
        r'<p class="lead">Hoe je een productlink in de agent plakt.*?</p>',
        (
            '<p class="lead">Plan USFans naar een <strong>Nederlands adres</strong>: '
            "kies NL in de schatter, vul postcode <strong>1234 AB</strong>, lees "
            "<strong>Belastingdienst Douane</strong> en last-mile via <strong>PostNL / DHL</strong>. "
            "Zoek je de globale spreadsheet / finds? → "
            f'<a href="{HUB}">usfansspreadsheet.net</a>.</p>'
        ),
        html,
        count=1,
        flags=re.S,
    )
    # replace #local block (platform-opt stub or prior light-fix)
    if 'id="local"' in html:
        html = re.sub(
            r"(?:<!-- portfolio-(?:platform-opt|nl-light-fix)-local -->\s*)?"
            r'<section class="sg-sec" id="local"[^>]*>[\s\S]*?</section>'
            r"(?:\s*<!-- /portfolio-(?:platform-opt|nl-light-fix)-local -->)?",
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
    # footer — drop Spreadsheet brand hero
    html = html.replace("<h3>USFans Spreadsheet</h3>", "<h3>USFans Nederland desk</h3>", 1)
    html = re.sub(
        r"Onafhankelijke Nederlandstalige gids over USFans en hoe je de w2clinks-catalogus gebruikt om vanuit Nederland in China te kopen\.",
        "Nederland keep desk: Douane, postcode 1234 AB, PostNL/DHL. Brand spreadsheet → usfansspreadsheet.net.",
        html,
        count=1,
    )
    html = html.replace(
        "USFans Spreadsheet is een onafhankelijke infosite.",
        "Deze Nederland keep desk is een onafhankelijke infosite.",
        1,
    )
    html = html.replace(
        "&copy; 2026 USFans Spreadsheet. Nederlandse tekst, nagelezen voor publicatie.",
        "&copy; 2026 USFans Nederland desk (usfansspreadsheet.nl). Keep · niet de brand spreadsheet hub.",
        1,
    )
    if MARKER not in html:
        html = re.sub(r"<html\b", f"<html {MARKER}", html, count=1)
    return html


def _assert_ok(label: str, html: str) -> None:
    need = (
        TITLE,
        H1,
        'id="local"',
        "Douane",
        "1234 AB",
        "PostNL",
        "betrouwbaar",
        HUB,
        "hub-uplink",
        MARKER,
    )
    for token in need:
        if token not in html:
            raise SystemExit(f"{label}: missing {token!r}")
    # refuse Spreadsheet hero in title / first H1
    m_title = re.search(r"<title>(.*?)</title>", html, re.S)
    m_h1 = re.search(r"<h1[^>]*>(.*?)</h1>", html, re.S)
    title = m_title.group(1) if m_title else ""
    h1 = re.sub(r"<[^>]+>", "", m_h1.group(1) if m_h1 else "")
    if re.search(r"Spreadsheet", title, re.I):
        raise SystemExit(f"{label}: Spreadsheet still in title: {title}")
    if re.search(r"Spreadsheet", h1, re.I):
        raise SystemExit(f"{label}: Spreadsheet still in H1: {h1}")
    # must not claim twin revive / Phase C
    if re.search(r"usfansspreadsheet\.uk(?!/)", html) and "301" not in html:
        # allow mentioning twin only in pass-through; refuse active twin CTA as live target
        pass


def build() -> Path:
    src = OVERLAY / "live-base.index.html"
    if not src.is_file():
        raise SystemExit("missing overlay/live-base.index.html — fetch LIVE first")
    home = patch_home(src.read_text(encoding="utf-8"))
    _assert_ok("home", home)
    out = OVERLAY / "index.html.nl-light-fix"
    out.write_text(home, encoding="utf-8")
    print("wrote", out, "bytes", out.stat().st_size)
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

        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "--user", "paramiko", "-q"]
        )
        import paramiko

    host, password = _load_ssh_pass()
    os.environ["ORIGIN_SSH_PASS"] = password  # do not print
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(host, username="root", password=password, timeout=30)
    return client


def _run(client, cmd: str, timeout: int = 120) -> str:
    _, stdout, stderr = client.exec_command(cmd, timeout=timeout)
    return (stdout.read() + stderr.read()).decode(errors="replace").strip()


def deploy() -> str:
    home_out = build()
    client = _connect()
    stamp = time.strftime("%Y%m%d-%H%M%S")
    bak = f"/www/backup/usfans-nl-light-fix-{stamp}"
    root = f"/www/wwwroot/{HOST}"
    _run(client, f"mkdir -p '{bak}'")
    # hard refuse writing hub / UK / twin
    forbidden = [
        "usfansspreadsheet.net",
        "usfansspreadsheet.co.uk",
        "usfansspreadsheet.uk",
    ]
    remote = f"{root}/index.html"
    raw = home_out.read_text(encoding="utf-8")
    if 'id="local"' not in raw or "Douane" not in raw or HUB not in raw:
        raise SystemExit(f"refusing PUT {remote}: missing local/hub markers")
    if "USFans Spreadsheet:" in raw.split("<h1>", 1)[-1][:120]:
        raise SystemExit(f"refusing Spreadsheet hero on {remote}")
    if any(f"/www/wwwroot/{h}" in remote for h in forbidden):
        raise SystemExit(f"refusing forbidden host path {remote}")
    # only NL wwwroot
    if root != f"/www/wwwroot/{HOST}":
        raise SystemExit("host root mismatch")
    _run(client, f"cp -a '{remote}' '{bak}/index.html.before'")
    sftp = client.open_sftp()
    sftp.put(str(home_out), remote)
    _run(client, f"chown www:www '{remote}'")
    print("PUT", remote, "bytes", home_out.stat().st_size)
    # sitemap lastmod for home + money URLs
    sm_remote = f"{root}/sitemap.xml"
    try:
        _run(client, f"test -f '{sm_remote}' && cp -a '{sm_remote}' '{bak}/sitemap.xml.before'")
        with sftp.open(sm_remote, "r") as f:
            sm = f.read().decode("utf-8", "replace")
        today = time.strftime("%Y-%m-%d")
        for loc in (
            f"https://{HOST}/",
            f"https://{HOST}/usfans-shipping-guide/",
            f"https://{HOST}/usfans-freight/",
            f"https://{HOST}/is-usfans-legit/",
            f"https://{HOST}/usfans-coupons/",
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
    except OSError as exc:
        print("sitemap skip:", exc)
    sftp.close()
    guard = _run(
        client,
        "echo '--- refuse hub/UK/twin writes this round ---'; "
        "echo -n 'nl '; ls -la /www/wwwroot/usfansspreadsheet.nl/index.html; "
        "echo -n 'hub mtime '; stat -c '%y' /www/wwwroot/usfansspreadsheet.net/index.html; "
        "echo -n 'uk mtime '; stat -c '%y' /www/wwwroot/usfansspreadsheet.co.uk/index.html; "
        "echo -n 'twin '; test -d /www/wwwroot/usfansspreadsheet.uk && echo HAS_DIR || echo NO_DIR; "
        f"rg -o '<title>[^<]+</title>|<h1[^>]*>[^<]+</h1>|data-nl-light-fix=\"[^\"]+\"|hub-uplink' "
        f"/www/wwwroot/usfansspreadsheet.nl/index.html | head -20",
    )
    print(guard)
    print("backup", bak)
    client.close()
    return bak


def main() -> None:
    if "--deploy" in sys.argv:
        bak = deploy()
        print("DEPLOY_OK", bak)
        return
    build()


if __name__ == "__main__":
    main()
