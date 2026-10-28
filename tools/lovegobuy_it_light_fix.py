#!/usr/bin/env python3
"""LoveGoBuy IT keep light fix (strategy action 3): remove Spreadsheet H1,
keep Poste/CAP title + thicken #local with hub uplink.

KEEP only — do NOT revive Phase C twins (.eu/.ca/.es→hub, spreadsheet.nl→.nl,
spreadsheet.it→.it). Do NOT touch hub lovegobuyguide.com or keep lovegobuy.nl.
"""
from __future__ import annotations

import json
import os
import re
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "sites" / "lovegobuy.it"
OVERLAY = SITE / "overlay"
STAMP = "20261028"
MARKER = f'data-it-light-fix="{STAMP}"'
HOST = "lovegobuy.it"
HUB = "https://lovegobuyguide.com/"

TITLE = "LoveGoBuy Italia — Poste Italiane, CAP e spedizione"
H1 = "LoveGoBuy per un indirizzo in Italia"

LOCAL_HOME = f"""
<section class="sg-sec sg-local" id="local" data-platform-opt="lovegobuy-20261026" data-it-light-fix="{STAMP}" data-keep="1">
  <h2>Cosa vale oggi per un indirizzo in Italia</h2>
  <p class="ssub">lovegobuy.it · <strong>keep</strong> desk locale · Poste Italiane / CAP / ADM — non un secondo brand hub.</p>
  <ol class="local-steps" style="margin:12px 0 0;padding:0;list-style:none;display:grid;gap:12px">
    <li style="border:1px solid #e5e7eb;border-radius:12px;padding:14px 16px;background:#fff"><strong style="display:block;margin:0 0 6px">Destinazione estimator: Italia</strong><span style="display:block;color:#334155;line-height:1.7">Scegli <strong>Italia / IT</strong>, non EU e non questo hostname. Un CAP francese o un código español è il paese sbagliato.</span></li>
    <li style="border:1px solid #e5e7eb;border-radius:12px;padding:14px 16px;background:#fff"><strong style="display:block;margin:0 0 6px">Indirizzo + CAP a cinque cifre</strong><span style="display:block;color:#334155;line-height:1.7">Via italiana e CAP a <strong>cinque cifre</strong> (es. 00100). Non incollare un postcode NL o un ZIP US nella rubrica magazzino.</span></li>
    <li style="border:1px solid #e5e7eb;border-radius:12px;padding:14px 16px;background:#fff"><strong style="display:block;margin:0 0 6px">ADM · dazi</strong><span style="display:block;color:#334155;line-height:1.7">Chi paga dazi lo dice la SKU. Fonte: <a href="https://www.adm.gov.it/portale/" rel="noopener">Agenzia delle Dogane e dei Monopoli (ADM)</a>. Niente valore dichiarato inventato.</span></li>
    <li style="border:1px solid #e5e7eb;border-radius:12px;padding:14px 16px;background:#fff"><strong style="display:block;margin:0 0 6px">Poste Italiane · ultimo miglio</strong><span style="display:block;color:#334155;line-height:1.7">Molte linee consegnano con <strong>Poste Italiane</strong> dopo lo sdoganamento; può comparire un fee Collect. Il tracking può restare fermo tra export e primo evento locale.</span></li>
  </ol>
  <p class="hub-uplink" style="margin:14px 0 0;padding:12px 14px;border-left:3px solid #0f766e;background:#f0fdfa;color:#134e4a;line-height:1.6;font-size:15px;max-width:760px">Cerchi la guida globale / spreadsheet / Independent Index · 11,300+? Usa <a href="{HUB}" style="color:#0f766e;font-weight:600">lovegobuyguide.com</a> (<a href="{HUB}lovegobuy-coupon/" style="color:#0f766e;font-weight:600">coupons</a> · <a href="{HUB}finds-dataset/" style="color:#0f766e;font-weight:600">dataset</a>). Questo host resta desk <strong>keep</strong> IT (Poste / CAP / ADM) — non un twin da resuscitare.</p>
  <p class="local-src" style="font-size:14px;color:#334155;line-height:1.7;margin:14px 0 0">URL utili: <a href="/lovegobuy-recensioni/">Recensioni</a> · <a href="/spedizione-lovegobuy/">Spedizione</a> · <a href="/lovegobuy-shipping/">Spedizione e dogana</a> · hub <a href="{HUB}">guide.com</a></p>
</section>
""".strip()


def _sub_title(html: str, title: str) -> str:
    return re.sub(r"<title>.*?</title>", f"<title>{title}</title>", html, count=1, flags=re.S)


def patch_home(html: str) -> str:
    html = _sub_title(html, TITLE)
    html = re.sub(
        r'<meta name="description" content="[^"]*"',
        (
            '<meta name="description" content="Desk IT LoveGoBuy: indirizzo in Italia, CAP a cinque cifre, '
            'Poste Italiane, ADM. Guida/spreadsheet globale → lovegobuyguide.com. Non un secondo brand hub."'
        ),
        html,
        count=1,
    )
    # JSON-LD WebPage name (still Spreadsheet-first on LIVE)
    html = re.sub(
        r'("name":\s*")LoveGoBuy Spreadsheet in italiano:[^"]*(")',
        rf'\1{TITLE}\2',
        html,
        count=1,
    )
    # brand chip
    html = html.replace("<span>Spreadsheet</span>", "<span>Italia</span>", 1)
    # nav: keep existing money URLs; ensure #local present
    if 'href="#local"' not in html.split("</nav>", 1)[0]:
        html = re.sub(
            r"(</nav>)",
            '<a href="#local">Locale IT</a></nav>',
            html,
            count=1,
        )
    # hero
    html = re.sub(
        r'<span class="eyebrow">.*?</span>',
        '<span class="eyebrow">Desk keep Italia · Poste Italiane · CAP · ADM</span>',
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
        r'<p class="lead">.*?</p>',
        (
            '<p class="lead">Desk <strong>keep</strong> indipendente su lovegobuy.it: pianifica un indirizzo in '
            "<strong>Italia</strong> con <strong>CAP a cinque cifre</strong>, "
            "<strong>Poste Italiane</strong> all’ultimo miglio e contesto <strong>ADM</strong> — "
            "non un eroe «LoveGoBuy Spreadsheet». Guida / dataset / coupons → "
            f'<a href="{HUB}">lovegobuyguide.com</a>.</p>'
        ),
        html,
        count=1,
        flags=re.S,
    )
    # replace #local
    if 'id="local"' in html:
        html = re.sub(
            r'<section[^>]*id="local"[^>]*>[\s\S]*?</section>',
            LOCAL_HOME,
            html,
            count=1,
        )
    else:
        html = re.sub(
            r"(</section>\s*)(<section class=\"sec)",
            r"\1\n" + LOCAL_HOME + "\n\2",
            html,
            count=1,
        )
    # footer — drop Spreadsheet brand hero
    html = html.replace("<h3>LoveGoBuy Spreadsheet</h3>", "<h3>LoveGoBuy Italia desk</h3>", 1)
    html = re.sub(
        r"Guida indipendente in italiano su LoveGoBuy e su come usi il catalogo w2clinks per comprare in Cina dall’Italia\.",
        "Desk keep Italia: Poste Italiane, CAP a cinque cifre, ADM. Spreadsheet / Independent Index → lovegobuyguide.com.",
        html,
        count=1,
    )
    html = html.replace(
        "LoveGoBuy Spreadsheet è un sito informativo indipendente.",
        "Questo desk Italia (lovegobuy.it) è un sito informativo indipendente.",
        1,
    )
    html = html.replace(
        "&copy; 2026 LoveGoBuy Spreadsheet.",
        "&copy; 2026 LoveGoBuy Italia desk (lovegobuy.it).",
        1,
    )
    if MARKER not in html:
        html = html.replace("<html", f"<html {MARKER}", 1)
    return html


def _assert_ok(label: str, html: str) -> None:
    need = (
        H1,
        "Poste Italiane",
        "CAP",
        "ADM",
        'id="local"',
        HUB,
        "keep",
        MARKER,
    )
    for tok in need:
        if tok not in html:
            raise SystemExit(f"{label} missing {tok!r}")
    h1 = re.search(r"<h1[^>]*>(.*?)</h1>", html, flags=re.S)
    if not h1:
        raise SystemExit(f"{label} missing H1")
    h1_text = re.sub(r"<[^>]+>", "", h1.group(1))
    if re.search(r"Spreadsheet", h1_text, re.I):
        raise SystemExit(f"{label} H1 still has Spreadsheet: {h1_text!r}")
    # sister fingerprints must not leak
    for bad in ("PostNL", "1234 AB", "Douane", "Canada Post", "CBSA", "Packstation"):
        if bad in html:
            raise SystemExit(f"{label} leaked sister fingerprint {bad!r}")


def build() -> Path:
    src = OVERLAY / "live-base.index.html"
    if not src.is_file():
        raise SystemExit("missing overlay/live-base.index.html — fetch LIVE first")
    home = patch_home(src.read_text(encoding="utf-8"))
    _assert_ok("home", home)
    out = OVERLAY / "index.html.it-light-fix"
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
    home_out = build()
    client = _connect()
    stamp = time.strftime("%Y%m%d-%H%M%S")
    bak = f"/www/backup/lovegobuy-it-light-fix-{stamp}"
    root = f"/www/wwwroot/{HOST}"
    _run(client, f"mkdir -p '{bak}'")
    # hard refuse writing hub / NL / twin roots
    forbidden = [
        "lovegobuyguide.com",
        "lovegobuy.nl",
        "lovegobuyspreadsheet.nl",
        "lovegobuyspreadsheet.it",
        "lovegobuyspreadsheet.eu",
        "lovegobuyspreadsheet.ca",
        "lovegobuyspreadsheet.es",
        "lovegobuyspreadsheet.co.uk",
        "lovegobuysheet.org",
    ]
    sftp = client.open_sftp()
    remote = f"{root}/index.html"
    raw = home_out.read_text(encoding="utf-8")
    if 'id="local"' not in raw or "Poste Italiane" not in raw or HUB not in raw:
        raise SystemExit(f"refusing PUT {remote}")
    if "LoveGoBuy Spreadsheet:" in raw.split("<h1>", 1)[-1][:120]:
        raise SystemExit(f"refusing Spreadsheet hero on {remote}")
    if any(f"/www/wwwroot/{h}" in remote for h in forbidden):
        raise SystemExit(f"refusing forbidden host path {remote}")
    # capture mtimes of untouched hosts before write
    mtimes_before = _run(
        client,
        "stat -c '%n %Y' /www/wwwroot/lovegobuyguide.com/index.html "
        "/www/wwwroot/lovegobuy.nl/index.html 2>/dev/null",
    )
    _run(client, f"cp -a '{remote}' '{bak}/index.html.before'")
    sftp.put(str(home_out), remote)
    _run(client, f"chown www:www '{remote}'")
    print("PUT", remote, "bytes", home_out.stat().st_size)
    # sitemap lastmod bump for money URLs only (if present)
    sm_remote = f"{root}/sitemap.xml"
    try:
        _run(client, f"cp -a '{sm_remote}' '{bak}/sitemap.xml.before'")
        with sftp.open(sm_remote, "r") as f:
            sm = f.read().decode("utf-8", "replace")
        today = time.strftime("%Y-%m-%d")
        for loc in (
            f"https://{HOST}/",
            f"https://{HOST}/lovegobuy-recensioni/",
            f"https://{HOST}/spedizione-lovegobuy/",
            f"https://{HOST}/lovegobuy-shipping/",
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
    except Exception as e:
        print("sitemap skip:", type(e).__name__)
    sftp.close()
    mtimes_after = _run(
        client,
        "stat -c '%n %Y' /www/wwwroot/lovegobuyguide.com/index.html "
        "/www/wwwroot/lovegobuy.nl/index.html 2>/dev/null",
    )
    if mtimes_before != mtimes_after:
        raise SystemExit("hub/NL mtime changed — abort signal; investigate")
    twin_check = _run(
        client,
        "echo '--- twin 301 expect; no wwwroot writes this round ---'; "
        "for h in lovegobuyspreadsheet.nl lovegobuyspreadsheet.it lovegobuyspreadsheet.eu "
        "lovegobuyspreadsheet.ca lovegobuyspreadsheet.es; do "
        "  echo -n \"$h \"; test -d /www/wwwroot/$h && echo HAS_DIR || echo NO_DIR; "
        "done; "
        f"ls '{root}/index.html'; "
        f"grep -o 'data-it-light-fix=\"[^\"]*\"' '{root}/index.html' | head -1; "
        f"grep -o '<h1>[^<]*</h1>' '{root}/index.html' | head -1",
    )
    print(twin_check)
    print("backup", bak)
    print("hub/NL mtimes unchanged:", mtimes_after.replace("\n", " | "))
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
