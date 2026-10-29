#!/usr/bin/env python3
"""Track 2 gains-desk light-fix #1: bbdbuy.it/bbdbuy-spreadsheet/

Scrub Spreadsheet catalog hero → IT handoff uplink to bbdbuyeu.net.
Keep Poste/ADM/CAP fingerprints elsewhere on the page. Do NOT touch hub,
CA/UK/US, twins, homepage, CSSBuy ES, FashionReps, or mycnbox.nl.
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
SLUG = "bbdbuy-spreadsheet"
HOST = "bbdbuy.it"
REMOTE = f"/www/wwwroot/{HOST}"
STAMP = "20261029"
HUB = "https://bbdbuyeu.net"
TODAY = "2026-10-29"
MARKER = f'data-it-light-fix="{STAMP}"'

TITLE = "BBDBuy Italia desk — spreadsheet brand → bbdbuyeu.net"
H1 = "BBDBuy Italia: non un secondo spreadsheet-hub"
DESC = (
    "bbdbuy.it è il desk Italia (Poste Italiane / ADM / CAP). "
    "Brand spreadsheet / Independent Index → bbdbuyeu.net. Non un catalogo-eroe."
)

STYLE = (
    f'<style id="it-light-fix-{STAMP}">.hub-uplink{{margin:14px 0;padding:12px 14px;'
    "border-left:3px solid #0f766e;background:#f0fdfa;color:#134e4a;line-height:1.6;"
    "font-size:15px;max-width:760px}}.hub-uplink a{{color:#0f766e;font-weight:600}}"
    "#local{scroll-margin-top:88px}.local-box{margin:1.25em 0;padding:14px 16px;"
    "border:1px solid #e2e8f0;border-radius:10px;background:#f8fafc}"
    ".local-box h2{margin:0 0 .6em;font-size:1.15rem}.local-box ol{margin:.4em 0 0;"
    "padding-left:1.2em}.local-box li{margin:.35em 0}</style>"
)

HUB_UPLINK = (
    f'<p class="hub-uplink" {MARKER} data-step4-hub="1">'
    "Brand spreadsheet / coupons / dataset / Independent Index → "
    f'<a href="{HUB}/">bbdbuyeu.net</a> · '
    f'<a href="{HUB}/bbdbuyeu-spreadsheet/">spreadsheet</a> · '
    f'<a href="{HUB}/bbdbuyeu-coupons/">coupons</a> · '
    f'<a href="{HUB}/finds-dataset/">dataset</a> '
    "(10,000+). Questa URL = desk Italia handoff — non un secondo catalogo-hub."
    "</p>"
)

LOCAL = f"""
<section id="local" class="local-box" data-it-fingerprint="it-desk-not-sheet-hub" {MARKER}>
<h2>Questa URL non è un secondo spreadsheet-hub</h2>
<ol>
<li><strong>Brand spreadsheet / finds / dataset</strong> → solo
<a href="{HUB}/">bbdbuyeu.net</a> (Independent Index · 10,000+).</li>
<li><strong>Questo desk</strong> = destinazione <strong>Italia</strong>,
<strong>CAP a cinque cifre</strong>, last mile spesso <strong>Poste Italiane</strong>,
contesto doganale <strong>ADM</strong> / IVA.</li>
<li><strong>Perché resta la pagina?</strong> — chi cerca «bbdbuy spreadsheet» da IT
deve essere mandato al hub, non a un eroe-catalogo su .it.</li>
</ol>
<p>Spedizione IT: <a href="/bbdbuy-shipping/">Poste / ADM / CAP</a> ·
QC: <a href="/bbdbuy-qc/">guida QC</a> ·
coupon locale: <a href="/bbdbuy-coupons/">checklist</a>.</p>
</section>
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
    return (stdout.read() + stderr.read()).decode(errors="replace").strip()


def fetch_live_base() -> Path:
    dest_dir = OVERLAY / SLUG
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest = dest_dir / "live-base.index.html"
    req = Request(
        f"https://{HOST}/{SLUG}/",
        headers={"User-Agent": "bbdbuy-it-spreadsheet-light-fix/1.0"},
    )
    with urlopen(req, timeout=30) as resp:
        body = resp.read().decode(errors="replace")
    # strip CF beacon/email-decode noise for cleaner overlay (keep if present)
    dest.write_text(body)
    print("FETCHED", dest, "bytes", dest.stat().st_size)
    return dest


def patch(html: str) -> str:
    if f'id="it-light-fix-{STAMP}"' not in html:
        html = html.replace("</head>", STYLE + "\n</head>", 1)

    html = re.sub(
        r"<title>.*?</title>",
        f"<title>{TITLE}</title>",
        html,
        count=1,
        flags=re.S,
    )
    html = re.sub(
        r'<meta name="description" content="[^"]*"',
        f'<meta name="description" content="{DESC}"',
        html,
        count=1,
    )
    html = re.sub(
        r'("name":\s*")BBDBuy Spreadsheet in italiano:[^"]*(")',
        rf'\1{TITLE}\2',
        html,
        count=1,
    )
    html = html.replace(
        '"description": "Independent BBDBuy spreadsheet for l’Italia."',
        f'"description": "{DESC}"',
        1,
    )

    html = html.replace("<span>Spreadsheet</span>", "<span>Italia</span>", 1)
    html = re.sub(
        r'<span class="eyebrow"[^>]*>Spreadsheet</span>',
        f'<span class="eyebrow" style="color:var(--acd)">Desk Italia · handoff hub · {TODAY}</span>',
        html,
        count=1,
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
            '<p class="lead">Il brand <strong>spreadsheet</strong> / Independent Index vive su '
            f'<a href="{HUB}/">bbdbuyeu.net</a>. Qui resti sul desk <strong>Italia</strong>: '
            "indirizzo con <strong>CAP a cinque cifre</strong>, last mile spesso "
            "<strong>Poste Italiane</strong>, contesto <strong>ADM</strong> / IVA — "
            "non un catalogo-eroe su .it.</p>"
        ),
        html,
        count=1,
        flags=re.S,
    )

    # replace figure caption soft (keep image, reframe)
    html = re.sub(
        r"(<figcaption>)[^<]*(</figcaption>)",
        r"\1Riferimento catalogo w2clinks: schede prodotto. "
        r"La verità brand spreadsheet / dataset resta su bbdbuyeu.net. "
        r"Scatto di riferimento 6 Oct 2026.\2",
        html,
        count=1,
    )

    # body paragraph already has Poste — keep + clarify handoff
    html = html.replace(
        "Cerca in inglese (sneakers, hoodie, jacket). L’indirizzo su questo dest è una via "
        "italiana e CAP a cinque cifre. Poste Italiane è il corriere locale di riferimento.",
        "Se cerchi brand spreadsheet / dataset / coupons globali, apri "
        f'<a href="{HUB}/">bbdbuyeu.net</a>. Su questo desk: destinazione <strong>Italia</strong>, '
        "via + <strong>CAP a cinque cifre</strong>, last mile spesso <strong>Poste Italiane</strong>, "
        "dazi/IVA secondo <strong>ADM</strong> + SKU.",
        1,
    )

    # CTAs → hub primary
    html = html.replace(
        '<p><a class="btn" href="/catalogo/">Apri il catalogo</a> '
        '<a class="btn btn--ghost" href="/how-to-use-bbdbuy/">Guida</a></p>',
        f'<p><a class="btn" href="{HUB}/">Apri hub spreadsheet</a> '
        f'<a class="btn btn--ghost" href="{HUB}/bbdbuyeu-spreadsheet/">Index hub</a> '
        '<a class="btn btn--ghost" href="/bbdbuy-shipping/">Spedizione IT</a></p>',
        1,
    )

    if "hub-uplink" not in html or MARKER not in html:
        # inject after lead / before figure if needed — prefer after CTAs block end of article
        if "</article>" in html:
            inject = f"\n{HUB_UPLINK}\n{LOCAL}\n"
            html = html.replace("</article>", inject + "</article>", 1)
        else:
            html = html.replace("</main>", f"{HUB_UPLINK}\n{LOCAL}\n</main>", 1)

    # footer soften Spreadsheet hero brand (Poste/ADM stay on desk elsewhere)
    html = html.replace("<h3>BBDBuy Spreadsheet</h3>", "<h3>BBDBuy Italia desk</h3>", 1)
    html = html.replace(
        "Guida indipendente in italiano su BBDBuy e su come usi il catalogo w2clinks "
        "per comprare in Cina dall’Italia.",
        "Desk Italia: Poste Italiane / ADM / CAP. Brand spreadsheet → bbdbuyeu.net.",
        1,
    )
    html = html.replace(
        "<strong>Nota di indipendenza.</strong> BBDBuy Spreadsheet è un sito informativo indipendente.",
        "<strong>Nota di indipendenza.</strong> bbdbuy.it è il desk Italia "
        "(Poste Italiane / ADM / CAP). Brand spreadsheet → bbdbuyeu.net. "
        "BBDBuy Spreadsheet era un sito informativo indipendente.",
        1,
    )
    html = html.replace(
        "&copy; 2026 BBDBuy Spreadsheet.",
        "&copy; 2026 BBDBuy Italia desk (bbdbuy.it).",
        1,
    )

    # nav: add hub + local
    if 'href="#local"' not in html.split("</nav>", 1)[0]:
        html = re.sub(
            r"(</nav>)",
            f'<a href="#local">Locale IT</a><a href="{HUB}/">Hub spreadsheet</a></nav>',
            html,
            count=1,
        )

    if MARKER not in html.split("<body", 1)[0] and f"<html" in html:
        # also stamp html root for verify ease
        if f" {MARKER}" not in html[:500]:
            html = html.replace("<html", f"<html {MARKER}", 1)

    return html


def _assert_ok(html: str) -> None:
    need = (
        H1,
        TITLE,
        "Poste Italiane",
        "ADM",
        "CAP",
        'id="local"',
        "hub-uplink",
        "bbdbuyeu.net",
        "finds-dataset",
        MARKER,
    )
    for tok in need:
        if tok not in html:
            raise SystemExit(f"missing {tok!r}")
    h1 = re.search(r"<h1[^>]*>(.*?)</h1>", html, flags=re.S)
    if not h1:
        raise SystemExit("missing H1")
    h1_text = re.sub(r"<[^>]+>", "", h1.group(1))
    if re.search(r"Spreadsheet", h1_text, re.I) and "secondo spreadsheet-hub" not in h1_text:
        # allow the negation phrasing only
        if "non un secondo" not in h1_text.lower():
            raise SystemExit(f"H1 still Spreadsheet hero: {h1_text!r}")
    title_m = re.search(r"<title>(.*?)</title>", html, flags=re.S)
    if title_m and re.search(r"Spreadsheet in italiano|catalogo", title_m.group(1), re.I):
        raise SystemExit(f"title still catalog hero: {title_m.group(1)!r}")
    # do not leak sister fingerprints
    for bad in ("Douane", "1234 AB", "PostNL", "Correos", "AEAT", "Independent Index · 11,300"):
        if bad in html:
            raise SystemExit(f"leaked sister fingerprint {bad!r}")


def build() -> Path:
    base = OVERLAY / SLUG / "live-base.index.html"
    if not base.is_file():
        fetch_live_base()
    patched = patch(base.read_text(encoding="utf-8", errors="replace"))
    _assert_ok(patched)
    out = OVERLAY / SLUG / "index.html.it-light-fix"
    out.write_text(patched, encoding="utf-8")
    # deployable alias
    (OVERLAY / SLUG / "index.html").write_text(patched, encoding="utf-8")
    print("BUILT", out, "bytes", out.stat().st_size)
    return out


def deploy(built: Path, store_internal: Path | None) -> dict:
    client = _connect()
    bak = (
        f"/www/backup/bbdbuy-it-spreadsheet-light-fix-"
        f"{datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%S')}"
    )
    print(
        _run(
            client,
            f"mkdir -p '{bak}' && "
            f"cp -a '{REMOTE}/{SLUG}/index.html' '{bak}/{SLUG}-index.html.before' 2>/dev/null || true && "
            f"cp -a '{REMOTE}/sitemap.xml' '{bak}/sitemap.xml.before' 2>/dev/null || true",
        )
    )
    sftp = client.open_sftp()
    remote = f"{REMOTE}/{SLUG}/index.html"
    sftp.put(str(built), remote)
    print("PUT", remote)

    try:
        with sftp.open(f"{REMOTE}/sitemap.xml", "r") as fh:
            sm = fh.read().decode(errors="replace")
        loc = f"https://{HOST}/{SLUG}/"
        if loc in sm:
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
        else:
            sm = sm.replace(
                "</urlset>",
                f"<url><loc>{loc}</loc><lastmod>{TODAY}</lastmod></url>\n</urlset>",
                1,
            )
        sm = re.sub(
            rf"(<loc>https://{re.escape(HOST)}/</loc>\s*<lastmod>)[^<]+",
            rf"\g<1>{TODAY}",
            sm,
        )
        tmp = f"/tmp/bbdbuy-it-sitemap-light-{STAMP}.xml"
        Path(tmp).write_text(sm)
        sftp.put(tmp, f"{REMOTE}/sitemap.xml")
        local_sm = OVERLAY / "sitemap.xml"
        if local_sm.exists():
            local_sm.write_text(sm)
        print("PUT sitemap.xml lastmod", TODAY)
    except Exception as exc:  # noqa: BLE001
        print("SITEMAP_WARN", exc)

    sftp.close()
    _run(
        client,
        f"chown www:www '{REMOTE}/{SLUG}/index.html' '{REMOTE}/sitemap.xml'",
    )
    print("BACKUP", bak)
    meta = {"backup": bak, "stamp": STAMP, "page": SLUG}
    if store_internal:
        store_internal.mkdir(parents=True, exist_ok=True)
        (store_internal / "backup.txt").write_text(bak + "\n")
    client.close()
    return meta


def verify() -> dict:
    url = f"https://{HOST}/{SLUG}/"
    req = Request(url, headers={"User-Agent": "bbdbuy-it-spreadsheet-light-fix/1.0"})
    with urlopen(req, timeout=30) as resp:
        body = resp.read().decode(errors="replace")
        code = resp.status
    title_m = re.search(r"<title>(.*?)</title>", body, re.S | re.I)
    h1_m = re.search(r"<h1[^>]*>(.*?)</h1>", body, re.S | re.I)
    title = re.sub(r"\s+", " ", title_m.group(1)).strip() if title_m else None
    h1 = re.sub(r"<[^>]+>", "", h1_m.group(1)) if h1_m else None
    h1 = re.sub(r"\s+", " ", h1).strip() if h1 else None
    row = {
        "url": url,
        "http": code,
        "title": title,
        "h1": h1,
        "id_local": 'id="local"' in body,
        "hub_uplink": "bbdbuyeu.net" in body and "finds-dataset" in body,
        "poste": "Poste Italiane" in body,
        "adm": "ADM" in body,
        "cap": "CAP" in body,
        "marker": MARKER in body,
        "spreadsheet_h1_hero": bool(
            h1 and re.search(r"Spreadsheet", h1, re.I) and "secondo spreadsheet-hub" not in h1
        ),
        "catalog_title_hero": bool(
            title and re.search(r"Spreadsheet in italiano|catalogo e come", title, re.I)
        ),
    }

    # untouched surfaces
    untouched = []
    for u, must_not in (
        (f"https://{HOST}/", MARKER),
        (f"https://{HOST}/bbdbuy-shipping/", MARKER),
        (f"{HUB}/", MARKER),
        ("https://mycnbox.nl/", MARKER),
        ("https://cssbuy.es/", MARKER),
        ("https://fashionrepsspreadsheet.com/", MARKER),
    ):
        req = Request(u, headers={"User-Agent": "bbdbuy-it-spreadsheet-light-fix/1.0"})
        with urlopen(req, timeout=30) as resp:
            b = resp.read().decode(errors="replace")
            code = resp.status
        untouched.append(
            {
                "url": u,
                "http": code,
                "has_marker": must_not in b,
                "ok": must_not not in b and code == 200,
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
        conn.request("GET", u.path or "/", headers={"User-Agent": "bbdbuy-light/1.0"})
        r = conn.getresponse()
        twin_rows.append({"url": t, "http": r.status, "location": r.getheader("Location")})
        conn.close()

    # NL observe skip evidence (already has uplink + Douane H1)
    nl_req = Request("https://mycnbox.nl/", headers={"User-Agent": "bbdbuy-light/1.0"})
    with urlopen(nl_req, timeout=30) as resp:
        nl = resp.read().decode(errors="replace")
    nl_h1_m = re.search(r"<h1[^>]*>(.*?)</h1>", nl, re.S)
    nl_h1 = re.sub(r"<[^>]+>", "", nl_h1_m.group(1)) if nl_h1_m else None
    nl_h1 = re.sub(r"\s+", " ", nl_h1).strip() if nl_h1 else None
    nl_skip = {
        "url": "https://mycnbox.nl/",
        "decision": "skip-14d-observe",
        "reason": (
            "Homepage already has hub-uplink → mycnbox.eu + Douane H1 intact; "
            "/mycnbox-spreadsheet/ already deepened. Extra CTA not clearly safe this round."
        ),
        "h1": nl_h1,
        "douane": "Douane" in nl,
        "hub_uplink_present": 'class="hub-uplink"' in nl and "mycnbox.eu" in nl,
        "marker_absent": MARKER not in nl,
    }

    return {
        "at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "page": row,
        "untouched": untouched,
        "twins": twin_rows,
        "nl_skip": nl_skip,
    }


def gsc_submit(sa: Path, out_path: Path) -> dict:
    try:
        from google.oauth2 import service_account
        from googleapiclient.discovery import build
    except ImportError:
        import subprocess

        subprocess.check_call(
            [
                sys.executable,
                "-m",
                "pip",
                "install",
                "google-api-python-client",
                "google-auth",
                "-q",
            ]
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
    ap.add_argument("--load-env", type=Path)
    ap.add_argument("--fetch", action="store_true")
    ap.add_argument("--build-only", action="store_true")
    ap.add_argument("--deploy", action="store_true")
    ap.add_argument("--verify", action="store_true")
    ap.add_argument("--gsc", action="store_true")
    ap.add_argument("--store-internal", type=Path, default=None)
    ap.add_argument("--gsc-sa", type=Path, default=None)
    args = ap.parse_args()
    if args.load_env:
        _load_env(args.load_env)
    if args.fetch:
        fetch_live_base()
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
        page = ver["page"]
        bad_page = (
            page.get("http") != 200
            or not page.get("id_local")
            or not page.get("hub_uplink")
            or not page.get("marker")
            or not page.get("poste")
            or not page.get("adm")
            or page.get("spreadsheet_h1_hero")
            or page.get("catalog_title_hero")
        )
        untouched_bad = [u for u in ver["untouched"] if not u.get("ok")]
        twin_ok = {
            "https://bbdbuyspreadsheet.ca/": "bbdbuy.ca",
            "https://bbdbuyspreadsheet.uk/": "bbdbuy.uk",
            "https://bbdbuyspreadsheet.us/": "bbdbuy.us",
            "https://bbdbuyeuspreadsheet.com/": "bbdbuyeu.net",
            "https://bbdbuyspreadsheet.de/": "bbdbuyeu.net",
        }
        twin_bad = []
        for t in ver.get("twins", []):
            loc = (t.get("location") or "").lower()
            want = twin_ok.get(t["url"], "")
            if t.get("http") not in (301, 302) or want not in loc:
                twin_bad.append(t)
        if bad_page or untouched_bad or twin_bad:
            print("VERIFY_FAIL", {"page": page if bad_page else "ok"}, untouched_bad, twin_bad)
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
