#!/usr/bin/env python3
"""WeMimi .net hub: unique EyouCMS homepage. Sister spreadsheet.com stays independent.

Gates:
1. Homepage is unique CMS (money title WeMimi Spreadsheet 2026). Not leftover dest
   #local / “not a customs territory”.
2. Titles have no invite token. Body has no customs coaching / 58-line.
3. Single PHP hub — no 301 of the homepage. Do not leftover-PUT (SKIP_UNIQUE).
4. wemimispreadsheet.com stays independent. Do not PUT that host this round.
5. Official newcomer pack is ¥1000 on wemimi.com — no invented SHIP code, no
   invented storage-day count. Confirm Help the morning you ship.
"""
from __future__ import annotations

import os
import re
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "sites"
EST = "https://www.wemimi.com/"
OFFICIAL = "https://www.wemimi.com/"
DATE = "8 Oct 2026"
EMAIL = "cnfd85269032661@gmail.com"
MONEY_TITLE = "WeMimi Spreadsheet 2026"
HOST = "wemimi.net"
HUB_MIN = 50000
LIVE_HUB_MIN = 50000

RANKED_CMS = (
    ("/coupons.html", 4000),
)

SISTER = "https://wemimispreadsheet.com/"
SISTER_INNERS = (
    ("/shoes381/", 4000),
    ("/wemimispread-coupon-tracker-2026.html", 4000),
    ("/wemimispread-user-reports-2026.html", 4000),
    ("/wemimispread-shipping-lines-2026.html", 4000),
)


def _decode_cf_email(hexstr: str) -> str:
    try:
        raw = bytes.fromhex(hexstr)
    except ValueError:
        return ""
    if not raw:
        return ""
    key = raw[0]
    return "".join(chr(b ^ key) for b in raw[1:])


def _has_contact_email(html: str) -> bool:
    if EMAIL in html:
        return True
    for hx in re.findall(r"data-cfemail=\"([0-9a-fA-F]+)\"", html):
        if _decode_cf_email(hx) == EMAIL:
            return True
    return False


def _unique_home_errors(html: str) -> list[str]:
    err: list[str] = []
    title_m = re.search(r"<title>(.*?)</title>", html, flags=re.S)
    title = re.sub(r"<[^>]+>", "", title_m.group(1) if title_m else "")
    h1_m = re.search(r"<h1[^>]*>(.*?)</h1>", html, flags=re.S)
    h1 = re.sub(r"<[^>]+>", "", h1_m.group(1) if h1_m else "")
    if MONEY_TITLE not in title.replace("&amp;", "&"):
        err.append(f"title missing money words: {title!r}")
    if MONEY_TITLE not in h1.replace("&amp;", "&"):
        err.append(f"h1 missing money words: {h1!r}")
    if re.search(r"invite\s*(code)?\s*[A-Z0-9]{5,}", title, flags=re.I):
        err.append("invite in title")
    if 'id="local"' in html or "not a customs territory" in html.lower():
        err.append("leftover dest hub skin")
    if "/api/products/" in html:
        err.append("products API dump")
    if "not Excel" not in html or "Google Sheet" not in html:
        err.append("missing not-excel copy")
    if not _has_contact_email(html):
        err.append("missing contact email")
    if "wa.me/8615396628356" not in html:
        err.append("missing WhatsApp +8615396628356")
    if "w2clinks.com/spreadsheet/" not in html:
        err.append("missing w2clinks spreadsheet")
    if "confirm Help the morning you ship" not in html and "Commodity Storage Timeline" not in html:
        err.append("missing official storage confirm-Help copy")
    if "¥1000" not in html or "official-promo" not in html:
        err.append("missing official ¥1000 promo")
    if "/assets/official/official-gift-pack.jpg" not in html:
        err.append("missing official coupon screenshot")
    if "/assets/images/official-logo.png" not in html:
        err.append("missing official wemimi trademark")
    if "coupon code SHIP" in html or "Use Code: SHIP" in html:
        err.append("invented SHIP promo code")
    if re.search(r"58 l[ií]neas para Espa|23[,.]81\s*USD|how to under-?declar", html, flags=re.I):
        err.append("spain snapshot / coaching")
    if 'class="hero"' not in html or 'id="categories"' not in html:
        err.append("hub chrome missing")
    if len(html) < HUB_MIN:
        err.append(f"home too small {len(html)}")
    return err


def generate() -> None:
    dest = OUT / HOST / "overlay" / "index.htm"
    html = dest.read_text(encoding="utf-8")
    err = _unique_home_errors(html)
    if err:
        raise SystemExit("unique overlay: " + "; ".join(err))
    leftover = ROOT / "tools" / "leftover_hub_skins.py"
    skip = leftover.read_text(encoding="utf-8")
    if f'"{HOST}"' not in skip or "SKIP_UNIQUE" not in skip:
        raise SystemExit("leftover_hub_skins.py must SKIP_UNIQUE wemimi.net")
    coupons = OUT / HOST / "overlay" / "coupons.html"
    ch = coupons.read_text(encoding="utf-8")
    cerr = []
    if "WeMimi Coupons 2026" not in ch:
        cerr.append("coupons title")
    if "¥1000" not in ch:
        cerr.append("coupons missing official amount")
    if "/assets/official/official-gift-pack.jpg" not in ch or "/assets/official/official-register.jpg" not in ch:
        cerr.append("coupons missing screenshots")
    if "/assets/images/official-logo.png" not in ch:
        cerr.append("coupons missing official logo")
    title_m = re.search(r"<title>(.*?)</title>", ch, flags=re.S)
    title = re.sub(r"<[^>]+>", "", title_m.group(1) if title_m else "")
    if re.search(r"invite\s*(code)?\s*[A-Z0-9]{5,}", title, flags=re.I):
        cerr.append("invite in coupons title")
    if "coupon code SHIP" in ch or "Use Code: SHIP" in ch:
        cerr.append("invented SHIP on coupons")
    if cerr:
        raise SystemExit("coupons overlay: " + "; ".join(cerr))
    print("unique overlay ok", dest, "bytes", len(html), "coupons", len(ch))


def _connect():
    try:
        import paramiko
    except ImportError:
        import subprocess

        subprocess.check_call([sys.executable, "-m", "pip", "install", "paramiko", "-q"])
        import paramiko

    password = os.environ.get("ORIGIN_SSH_PASS")
    if not password:
        raise SystemExit("Set ORIGIN_SSH_PASS")
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect("31.97.41.31", username="root", password=password, timeout=30)
    return client


def _run(client, cmd: str, timeout: int = 90) -> str:
    _, stdout, stderr = client.exec_command(cmd, timeout=timeout)
    return (stdout.read() + stderr.read()).decode(errors="replace").strip()


def _cf_purge(host: str) -> None:
    import json
    import urllib.error
    import urllib.parse
    import urllib.request

    token = os.environ.get("CLOUDFLARE_API_TOKEN", "").strip()
    if not token:
        print("skip CF purge: no token")
        return
    req = urllib.request.Request(
        "https://api.cloudflare.com/client/v4/zones?" + urllib.parse.urlencode({"name": host}),
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            data = json.loads(resp.read().decode())
    except urllib.error.URLError as e:
        print("CF zone lookup failed", e)
        return
    zid = (data.get("result") or [{}])[0].get("id")
    if not zid:
        print("CF zone not found", host, data.get("errors"))
        return
    preq = urllib.request.Request(
        f"https://api.cloudflare.com/client/v4/zones/{zid}/purge_cache",
        data=json.dumps({"purge_everything": True}).encode(),
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(preq, timeout=20) as resp:
        out = json.loads(resp.read().decode())
    print("CF purge", host, out.get("success"), out.get("errors") or "")


def put() -> None:
    generate()
    client = _connect()
    stamp = time.strftime("%Y%m%d-%H%M%S")
    bak = f"/www/backup/wemimi-hub-deepen-{stamp}"
    _run(client, f"mkdir -p '{bak}'")
    sftp = client.open_sftp()

    local = OUT / HOST / "overlay" / "index.htm"
    remote = f"/www/wwwroot/{HOST}/template/pc/index.htm"
    raw = local.read_text(encoding="utf-8")
    err = _unique_home_errors(raw)
    if err:
        raise SystemExit("refusing PUT: " + "; ".join(err))
    _run(client, f"cp -a '{remote}' '{bak}/{HOST}.template-pc-index.htm'")
    sftp.put(str(local), remote)
    print("PUT", remote, "bytes", local.stat().st_size)
    print(
        _run(
            client,
            "rm -rf /www/wwwroot/wemimi.net/data/runtime/cache/* "
            "/www/wwwroot/wemimi.net/data/runtime/temp/* ; echo cache-cleared",
        )
    )

    coup_l = OUT / HOST / "overlay" / "coupons.html"
    coup_r = f"/www/wwwroot/{HOST}/coupons.html"
    _run(client, f"cp -a '{coup_r}' '{bak}/{HOST}.coupons.html' 2>/dev/null || true")
    sftp.put(str(coup_l), coup_r)
    print("PUT", coup_r, "bytes", coup_l.stat().st_size)

    sm_l = OUT / HOST / "overlay" / "sitemap.xml"
    sm_r = f"/www/wwwroot/{HOST}/sitemap.xml"
    _run(client, f"cp -a '{sm_r}' '{bak}/{HOST}.sitemap.xml' 2>/dev/null || true")
    sftp.put(str(sm_l), sm_r)
    print("PUT", sm_r, "bytes", sm_l.stat().st_size)

    _run(
        client,
        f"mkdir -p '/www/wwwroot/{HOST}/assets/images' '/www/wwwroot/{HOST}/assets/official' "
        f"'{bak}/assets'",
    )
    logo_l = OUT / HOST / "overlay" / "assets" / "images" / "official-logo.png"
    sftp.put(str(logo_l), f"/www/wwwroot/{HOST}/assets/images/official-logo.png")
    print("PUT official-logo.png", logo_l.stat().st_size)
    off_dir = OUT / HOST / "overlay" / "assets" / "official"
    for img in sorted(off_dir.glob("*")):
        if img.suffix.lower() not in {".jpg", ".jpeg", ".png", ".webp"}:
            continue
        sftp.put(str(img), f"/www/wwwroot/{HOST}/assets/official/{img.name}")
        print("PUT official", img.name, img.stat().st_size)

    nginx_t = _run(client, "nginx -t 2>&1")
    print(nginx_t)
    if "successful" not in nginx_t.lower() and "ok" not in nginx_t.lower():
        raise SystemExit("nginx -t failed; not reloading")
    print(_run(client, "nginx -s reload 2>&1"))
    sftp.close()
    print("backup", bak)
    print("did not PUT wemimispreadsheet.com or dead CMS category 404s")
    client.close()
    _cf_purge(HOST)


def live_check() -> None:
    import urllib.error
    import urllib.request

    class NR(urllib.request.HTTPRedirectHandler):
        def redirect_request(self, req, fp, code, msg, headers, newurl):
            return None

    def fetch(url, follow=True):
        req = urllib.request.Request(url, headers={"User-Agent": "wemimi-hub-check/1.0"})
        opener = urllib.request.build_opener() if follow else urllib.request.build_opener(NR)
        try:
            with opener.open(req, timeout=25) as resp:
                return resp.status, resp.geturl(), resp.headers.get("Location") or "", resp.read()
        except urllib.error.HTTPError as e:
            return e.code, url, e.headers.get("Location") or "", e.read() if e.fp else b""

    fail = 0
    code, _, loc, body = fetch(f"https://{HOST}/", follow=True)
    html = body.decode("utf-8", "replace")
    print(f"home {code} bytes={len(body)} loc={loc!r}")
    if code != 200:
        print("  FAIL home status")
        fail += 1
    else:
        for e in _unique_home_errors(html):
            print("  FAIL", e)
            fail += 1
        if len(body) < LIVE_HUB_MIN:
            print("  FAIL php hub collapsed", len(body))
            fail += 1

    code, _, loc, _ = fetch(f"https://www.{HOST}/", follow=False)
    if code not in (301, 302, 303, 307, 308) or HOST not in (loc or "") or "www." in (loc or "").split("://", 1)[-1][:40]:
        if f"www.{HOST}" in (loc or ""):
            print("FAIL www still on www", code, loc)
            fail += 1
        elif code not in (301, 302, 303, 307, 308):
            print("FAIL www not 301", code, loc)
            fail += 1
        else:
            print("www", code, loc)
    else:
        print("www", code, loc)

    code, _, loc, _ = fetch(f"https://{HOST}/", follow=False)
    if code in (301, 302, 303, 307, 308):
        print("FAIL 301 home", loc)
        fail += 1
    else:
        print("indep home", code)

    code, _, loc, _ = fetch(SISTER, follow=False)
    if code in (301, 302, 303, 307, 308) and HOST in (loc or ""):
        print("FAIL 301 sister into hub", loc)
        fail += 1
    else:
        print("indep sister", code, loc)

    for path, min_bytes in RANKED_CMS:
        url = f"https://{HOST}{path}"
        code, _, loc, _ = fetch(url, follow=False)
        if code in (301, 302, 303, 307, 308) and loc:
            print("FAIL 301 inner", url, "->", loc)
            fail += 1
            continue
        code, final, _, body = fetch(url, follow=True)
        if code == 404 or len(body) < min_bytes:
            print("FAIL inner", url, code, len(body), final)
            fail += 1
        else:
            print("inner", code, len(body), final)
            if path == "/coupons.html":
                html = body.decode("utf-8", "replace")
                if "WeMimi Coupons 2026" not in html or "¥1000" not in html:
                    print("FAIL coupons title/amount drifted")
                    fail += 1
                title_m = re.search(r"<title>(.*?)</title>", html, flags=re.S)
                title = title_m.group(1) if title_m else ""
                if re.search(r"invite\s*(code)?\s*[A-Z0-9]{5,}", title, flags=re.I):
                    print("FAIL invite in coupons title", title)
                    fail += 1

    for path, min_bytes in SISTER_INNERS:
        url = f"https://wemimispreadsheet.com{path}"
        code, _, loc, _ = fetch(url, follow=False)
        if code in (301, 302, 303, 307, 308) and loc:
            print("FAIL 301 sister inner", url, "->", loc)
            fail += 1
            continue
        code, final, _, body = fetch(url, follow=True)
        if code == 404 or len(body) < min_bytes:
            print("FAIL sister inner", url, code, len(body))
            fail += 1
        else:
            print("sister inner", code, len(body), final)

    if fail:
        raise SystemExit(f"live_check failures: {fail}")
    print("live_check ok")


def main() -> None:
    if "--put" in sys.argv:
        put()
        return
    if "--check" in sys.argv:
        live_check()
        return
    generate()


if __name__ == "__main__":
    main()
