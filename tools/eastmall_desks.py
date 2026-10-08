#!/usr/bin/env python3
"""EastMallBuy .com hub: unique CMS money homepage. Ranked inners stay 200.

Gates:
1. Homepage is unique CMS (money title EastMallBuy Spreadsheet 2026). Not leftover
   dest #local / “not a customs territory” H1 / products-API dump.
2. Titles have no invite token cnfd85269032661. Body has no customs coaching / 58-line.
   Register invite query-string stays off the homepage (email local-part is allowed).
3. Independent of eastmallbuyspreadsheet.com (competitor EASTMALLFINDS) — no 301.
   eastmall.com has no DNS; official checkout is eastmallbuy.com. www already 301s apex.
   Do not leftover-PUT (SKIP_UNIQUE).
4. Ranked unique inners must 200. Do not PUT /eastmallbuy-coupons/ or the 12k product
   dump inner. Slash aliases stay.
5. Official eastmallbuy.com homepage 8 Oct 2026: $200 new-user coupons, monthly 3KG
   free-shipping lucky draw, 24h/8h/24h SLAs, free QC pictures. Help: 90 days free
   storage (60 days abnormal), 200 register points. Do not copy Hangzhou or a 5-day
   return window from a competitor review. Do not invent a SHIP code.
"""
from __future__ import annotations

import os
import re
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "sites"
OFFICIAL = "https://www.eastmallbuy.com/web/#/home"
DATE = "8 Oct 2026"
EMAIL = "cnfd85269032661@gmail.com"
MONEY_TITLE = "EastMallBuy Spreadsheet 2026"
HOST = "eastmallspreadsheet.com"
COMPETITOR = "eastmallbuyspreadsheet.com"
INVITE = "cnfd85269032661"
HUB_MIN = 24000
LIVE_HUB_MIN = 25000

RANKED_CMS = (
    ("/eastmallbuy-spreadsheet/", 20000),
    ("/eastmallbuy-coupons/", 20000),
    ("/eastmallbuy-shipping-guide/", 20000),
    ("/is-eastmallbuy-legit/", 20000),
    ("/eastmallbuy-spreadsheet-2026/", 8000),
    ("/eastmallbuy-shoes-spreadsheet/", 8000),
    ("/how-to-use-eastmallbuy/", 8000),
    ("/blog/", 8000),
    ("/eastmallbuy-qc-guide/", 8000),
    ("/eastmallbuy-refund-guide/", 8000),
    ("/eastmallbuy-invite-code/", 8000),
    ("/eastmallbuy-community/", 8000),
    ("/coupons/", 3000),
    ("/shipping/", 3000),
    ("/start/", 3000),
)

KEEP_REDIRECTS = (
    ("/eastmallbuy-spreadsheet", "/eastmallbuy-spreadsheet/"),
    ("/eastmallbuy-coupons", "/eastmallbuy-coupons/"),
    ("/eastmallbuy-shipping-guide", "/eastmallbuy-shipping-guide/"),
    ("/coupons", "/coupons/"),
    ("/shipping", "/shipping/"),
    ("/start", "/start/"),
)

INNER_TITLES = {
    "/eastmallbuy-spreadsheet/": "EastMallBuy Spreadsheet 2026",
    "/eastmallbuy-coupons/": "EastMallBuy Coupon Codes 2026",
    "/is-eastmallbuy-legit/": "Is EastMallBuy Legit",
}


def _decode_cf_email(html: str) -> str:
    out = []
    for m in re.finditer(r'data-cfemail="([0-9a-fA-F]+)"', html):
        hexed = m.group(1)
        key = int(hexed[:2], 16)
        chars = [chr(int(hexed[i : i + 2], 16) ^ key) for i in range(2, len(hexed), 2)]
        out.append("".join(chars))
    return " ".join(out)


def _has_contact_email(html: str) -> bool:
    if EMAIL in html:
        return True
    return EMAIL in _decode_cf_email(html)


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
    if re.search(r"invite\s*(code)?\s*[A-Z0-9]{5,}", title, flags=re.I) or INVITE in title:
        err.append("invite in title")
    if "inviter=" in html or "inviter id" in html.lower():
        err.append("frozen invite token still on homepage")
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
    if "w2clinks.com/spreadsheet/eastmallbuy/" not in html:
        err.append("missing w2clinks EastMallBuy sheet")
    if "90 days" not in html and "90-day" not in html:
        err.append("missing official 90 days free storage")
    if "60 days" not in html and "60-day" not in html:
        err.append("missing official 60-day abnormal storage")
    if "$200" not in html and "200 coupons" not in html.lower():
        err.append("missing official $200 new-user coupons")
    if "3KG" not in html and "3kg" not in html.lower():
        err.append("missing official 3KG lucky draw")
    if "24" not in html or "8" not in html:
        err.append("missing official 24h/8h SLA")
    if "200 points" not in html:
        err.append("missing official 200 register points")
    if "free pictures" not in html and "QC pictures" not in html and "quality inspection" not in html:
        err.append("missing official free QC pictures")
    if "Hangzhou" in html:
        err.append("copied competitor Hangzhou warehouse")
    if re.search(r"5-day (post-arrival )?return", html, flags=re.I):
        err.append("copied competitor 5-day return")
    if "official-promo" not in html:
        err.append("missing official promo strip")
    if "/assets/images/official-logo.png" not in html:
        err.append("missing official EastMallBuy trademark")
    if "/assets/official/official-finds.jpg" not in html:
        err.append("missing w2clinks finds screenshot")
    if "/assets/official/official-storage.jpg" not in html:
        err.append("missing official 90-day storage screenshot")
    if "/assets/official/official-sla.jpg" not in html:
        err.append("missing official SLA screenshot")
    if re.search(r"coupon code SHIP|Use Code:\s*SHIP", html, flags=re.I):
        err.append("invented SHIP code")
    if re.search(r"58 l[ií]neas para Espa|23[,.]81\s*USD|how to under-?declar", html, flags=re.I):
        err.append("spain snapshot / coaching")
    if len(html) < HUB_MIN:
        err.append(f"home too small {len(html)}")
    return err


def generate() -> None:
    dest = OUT / HOST / "overlay" / "index.html"
    html = dest.read_text(encoding="utf-8")
    err = _unique_home_errors(html)
    if err:
        raise SystemExit("unique overlay: " + "; ".join(err))
    leftover = ROOT / "tools" / "leftover_hub_skins.py"
    skip = leftover.read_text(encoding="utf-8")
    if f'"{HOST}"' not in skip or "SKIP_UNIQUE" not in skip:
        raise SystemExit("leftover_hub_skins.py must SKIP_UNIQUE eastmallspreadsheet.com")
    coupons = OUT / HOST / "overlay" / "coupons.html"
    ch = coupons.read_text(encoding="utf-8")
    cerr = []
    if "EastMallBuy Coupons 2026" not in ch:
        cerr.append("coupons title")
    if "90 days" not in ch and "90-day" not in ch:
        cerr.append("coupons missing 90-day storage")
    if "$200" not in ch and "200 coupons" not in ch.lower():
        cerr.append("coupons missing $200 new-user coupons")
    if "3KG" not in ch and "3kg" not in ch.lower():
        cerr.append("coupons missing 3KG lucky draw")
    if "/assets/images/official-logo.png" not in ch:
        cerr.append("coupons missing official logo")
    if "inviter=" in ch or "inviter id" in ch.lower():
        cerr.append("invite token on coupons overlay")
    title_m = re.search(r"<title>(.*?)</title>", ch, flags=re.S)
    title = re.sub(r"<[^>]+>", "", title_m.group(1) if title_m else "")
    if re.search(r"invite\s*(code)?\s*[A-Z0-9]{5,}", title, flags=re.I) or INVITE in title:
        cerr.append("invite in coupons title")
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
    bak = f"/www/backup/eastmall-hub-deepen-{stamp}"
    _run(client, f"mkdir -p '{bak}'")
    sftp = client.open_sftp()

    local = OUT / HOST / "overlay" / "index.html"
    remote = f"/www/wwwroot/{HOST}/index.html"
    raw = local.read_text(encoding="utf-8")
    err = _unique_home_errors(raw)
    if err:
        raise SystemExit("refusing PUT: " + "; ".join(err))
    _run(client, f"cp -a '{remote}' '{bak}/{HOST}.index.html'")
    sftp.put(str(local), remote)
    print("PUT", remote, "bytes", local.stat().st_size)

    coup_l = OUT / HOST / "overlay" / "coupons.html"
    coup_r = f"/www/wwwroot/{HOST}/coupons.html"
    _run(client, f"cp -a '{coup_r}' '{bak}/{HOST}.coupons.html' 2>/dev/null || true")
    sftp.put(str(coup_l), coup_r)
    print("PUT", coup_r, "bytes", coup_l.stat().st_size)

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
        sftp.put(str(img), f"/www/wwwroot/{HOST}/assets/official/{img.name}")
        print("PUT official", img.name, img.stat().st_size)

    nginx_t = _run(client, "nginx -t 2>&1")
    print(nginx_t)
    if "successful" not in nginx_t.lower() and "ok" not in nginx_t.lower():
        raise SystemExit("nginx -t failed; not reloading")
    print(_run(client, "nginx -s reload 2>&1"))
    sftp.close()
    print("backup", bak)
    print("did not PUT ranked inners; did not rewrite gsc-redirects; did not PUT", COMPETITOR)
    client.close()
    _cf_purge(HOST)


def live_check() -> None:
    import urllib.error
    import urllib.request

    class NR(urllib.request.HTTPRedirectHandler):
        def redirect_request(self, req, fp, code, msg, headers, newurl):
            return None

    def fetch(url, follow=True):
        req = urllib.request.Request(url, headers={"User-Agent": "eastmall-hub-check/1.0"})
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
        if len(body) < LIVE_HUB_MIN:
            print("  FAIL home too small", len(body))
            fail += 1
        for e in _unique_home_errors(html):
            print("  FAIL", e)
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

    for src, dst in KEEP_REDIRECTS:
        url = f"https://{HOST}{src}"
        code, _, loc, _ = fetch(url, follow=False)
        if code not in (301, 302, 303, 307, 308) or dst.rstrip("/") not in (loc or ""):
            print("FAIL expected 301", url, code, "->", loc, "want", dst)
            fail += 1
        else:
            print("kept 301", src, "->", loc)

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
            html = body.decode("utf-8", "replace")
            title_m = re.search(r"<title>(.*?)</title>", html, flags=re.S)
            title = title_m.group(1) if title_m else ""
            need = INNER_TITLES.get(path)
            if need and need not in title.replace("&amp;", "&"):
                print("FAIL inner title drifted", path, title)
                fail += 1
            if path in ("/eastmallbuy-coupons/", "/coupons/", "/eastmallbuy-invite-code/", "/start/") and (
                re.search(r"invite\s*(code)?\s*[A-Z0-9]{5,}", title, flags=re.I)
            ):
                print("FAIL invite in inner title", path, title)
                fail += 1

    coup_url = f"https://{HOST}/coupons.html"
    code, final, _, body = fetch(coup_url, follow=True)
    ch = body.decode("utf-8", "replace")
    if code != 200 or len(body) < 4000 or ("90 days" not in ch and "90-day" not in ch):
        print("FAIL coupons.html", code, len(body), final)
        fail += 1
    else:
        print("coupons.html", code, len(body), final)

    code, _, loc, _ = fetch(f"https://{COMPETITOR}/", follow=False)
    if code in (301, 302, 303, 307, 308) and HOST in (loc or ""):
        print("FAIL competitor 301 into hub", loc)
        fail += 1
    else:
        print("competitor indep", code, loc or "")

    code, _, loc, _ = fetch(f"https://{HOST}/", follow=False)
    if code in (301, 302, 303, 307, 308) and COMPETITOR in (loc or ""):
        print("FAIL hub 301 into competitor", loc)
        fail += 1

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
