#!/usr/bin/env python3
"""ootdbuyspreadsheet.net hub: unique Spreadsheet 2026 home. .org twin stays independent.

Gates:
1. Homepage is unique CMS (money title OOTDBuy Spreadsheet 2026). Not leftover
   dest #local / “not a customs territory” H1 / products-API dump. Not a clone of
   leftover ootdbuyspreadsheet.org dest skin.
2. Titles have no invite token. Body has no customs coaching. Frozen invite
   stays off the homepage. Coupon stacking stays on ranked /ootdbuy-coupon-2026.html
   (not the homepage title). Extra /coupons.html is 图文.
3. Independent of ootdbuyspreadsheet.org — no 301. Dest ccTLDs stay themselves.
   www already 301s apex. Do not leftover-PUT (SKIP_UNIQUE).
4. Ranked unique inners must 200. Do not PUT /ootdbuy-coupon-2026.html,
   /how-to-buy-from-china-2026.html, /best-ootdbuy-spreadsheet-2026.html, /categories/.
   Keep /coupons/ → coupon guide 301. Thin /start/ /shipping/ stay 404. Extra /coupons.html is 图文.
5. Official ootdbuy.com 9 Oct 2026: $500 new-user gift pack, 20% OFF shipping,
   €3 EU parcel notice, Exception Ticket. Chrome #FF6A00 / Nunito Sans. Do not
   invent a free-day count. Official Discord discord.gg/FwcPNG2BFS.
"""
from __future__ import annotations

import os
import re
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "sites"
OFFICIAL = "https://ootdbuy.com/"
DATE = "9 Oct 2026"
EMAIL = "cnfd85269032661@gmail.com"
MONEY_TITLE = "OOTDBuy Spreadsheet 2026"
HOST = "ootdbuyspreadsheet.net"
TWIN = "ootdbuyspreadsheet.org"
INVITE = "FCGYHLJWL"
HUB_MIN = 20000
LIVE_HUB_MIN = 21000
CHROME = (
    'class="nav"',
    "hero fade-in",
    "nbrand",
    "ccard",
    "OOTDBuy Spreadsheet 2026",
    "#FF6A00",
    "Nunito Sans",
)

RANKED_CMS = (
    ("/ootdbuy-coupon-2026.html", 20000),
    ("/how-to-buy-from-china-2026.html", 20000),
    ("/best-ootdbuy-spreadsheet-2026.html", 20000),
    ("/categories/", 8000),
)

KEEP_REDIRECTS = (
    ("/categories", "/categories/"),
    ("/coupons/", "/ootdbuy-coupons-guide/"),
    ("/ootdbuy-coupons-guide/", "/ootdbuy-coupon-2026.html"),
)

INNER_TITLES = {
    "/ootdbuy-coupon-2026.html": "OOTDBuy Coupon 2026",
    "/best-ootdbuy-spreadsheet-2026.html": "Best OOTDBuy Spreadsheet 2026",
}

THIN_404 = ("/shipping/", "/start/")
DESTS = (
    "https://ootdbuyspreadsheet.org/",
    "https://ootdbuy.nl/",
    "https://ootdbuyspreadsheet.ca/",
    "https://ootdbuyspreadsheet.co.uk/",
    "https://ootdbuyspreadsheet.de/",
    "https://ootdbuyspreadsheet.us/",
)


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
    h1 = re.sub(r"\s+", " ", h1).strip()
    if MONEY_TITLE not in title.replace("&amp;", "&"):
        err.append(f"title missing money words: {title!r}")
    if "Coupons" in title or "$500" in title or "20%" in title:
        err.append(f"coupon pack still in money title: {title!r}")
    if MONEY_TITLE.replace(" 2026","") not in h1.replace("&amp;", "&") or "2026" not in h1:
        err.append(f"h1 missing money words: {h1!r}")
    if re.search(r"invite\s*(code)?\s*[A-Z0-9]{5,}", title, flags=re.I) or INVITE in title:
        err.append("invite in title")
    if (
        "inviteCode=" in html
        or "invite_id=" in html
        or "inviter=" in html
        or "invite_code=" in html
        or "rno=" in html
    ):
        err.append("frozen invite token still on homepage")
    if INVITE in html:
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
    if "$500" not in html:
        err.append("missing official $500 gift pack")
    if "20% OFF" not in html:
        err.append("missing official 20% OFF shipping")
    if "€3" not in html and "EUR 3" not in html:
        err.append("missing official €3 EU parcel")
    if "Exception Ticket" not in html:
        err.append("missing Exception Ticket")
    if "discord.gg/FwcPNG2BFS" not in html:
        err.append("missing official Discord")
    if "does not invent a free-day" not in html:
        err.append("missing no-invented-storage line")
    if "Women's Fashion" not in html and "Women’s Fashion" not in html:
        err.append("missing Women's Fashion")
    if "dest-country skin" not in html:
        err.append("missing dest-country-skin line")
    if TWIN not in html:
        err.append(f"missing twin independence {TWIN}")
    if "w2clinks" not in html:
        err.append("missing w2clinks naming")
    if "official-promo" not in html:
        err.append("missing official promo strip")
    if "/assets/images/official-logo.png" not in html:
        err.append("missing official ootdbuy trademark")
    if "/assets/official/official-home.jpg" not in html:
        err.append("missing official homepage 图文")
    if re.search(r"58 l[ií]neas para Espa|23[,.]81\s*USD|how to under-?declar", html, flags=re.I):
        err.append("spain snapshot / coaching")
    for marker in CHROME:
        if marker not in html:
            err.append(f"hub chrome missing {marker}")
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
        raise SystemExit("leftover_hub_skins.py must SKIP_UNIQUE ootdbuyspreadsheet.net")
    coupons = OUT / HOST / "overlay" / "coupons.html"
    ch = coupons.read_text(encoding="utf-8")
    cerr = []
    if "OOTDBuy Coupons 2026" not in ch:
        cerr.append("coupons title")
    if "$500" not in ch:
        cerr.append("coupons missing $500")
    if "/assets/images/official-logo.png" not in ch:
        cerr.append("coupons missing official logo")
    if INVITE in ch:
        cerr.append("invite token on coupons overlay")
    title_m = re.search(r"<title>(.*?)</title>", ch, flags=re.S)
    title = re.sub(r"<[^>]+>", "", title_m.group(1) if title_m else "")
    if re.search(r"invite\s*(code)?\s*[A-Z0-9]{5,}", title, flags=re.I):
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
    bak = f"/www/backup/ootdbuy-hub-deepen-{stamp}"
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
    img_dir = OUT / HOST / "overlay" / "assets" / "images"
    for img in sorted(img_dir.rglob("*")):
        if not img.is_file():
            continue
        rel = img.relative_to(img_dir).as_posix()
        remote_img = f"/www/wwwroot/{HOST}/assets/images/{rel}"
        _run(client, f"mkdir -p '{Path(remote_img).parent}'")
        sftp.put(str(img), remote_img)
        print("PUT image", rel, img.stat().st_size)
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
    print("did not PUT ranked inners; did not rewrite gsc-redirects; did not PUT", TWIN)
    client.close()
    _cf_purge(HOST)


def live_check() -> None:
    import urllib.error
    import urllib.request

    class NR(urllib.request.HTTPRedirectHandler):
        def redirect_request(self, req, fp, code, msg, headers, newurl):
            return None

    def fetch(url, follow=True):
        req = urllib.request.Request(url, headers={"User-Agent": "ootd-hub-check/1.0"})
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
    if code not in (301, 302, 303, 307, 308) or HOST not in (loc or ""):
        print("FAIL www not 301 apex", code, loc)
        fail += 1
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

    coup_url = f"https://{HOST}/coupons.html"
    code, final, _, body = fetch(coup_url, follow=True)
    ch = body.decode("utf-8", "replace")
    if code != 200 or len(body) < 2000 or "$500" not in ch:
        print("FAIL coupons.html", code, len(body), final)
        fail += 1
    else:
        print("coupons.html", code, len(body), final)

    for path in THIN_404:
        url = f"https://{HOST}{path}"
        code, _, loc, _ = fetch(url, follow=False)
        if code == 404:
            print("thin 404", path)
        elif code in (301, 302, 303, 307, 308):
            print("thin redirect", path, code, loc)
        else:
            print("note thin", path, code)

    code, _, loc, _ = fetch(f"https://{TWIN}/", follow=False)
    if code in (301, 302, 303, 307, 308) and HOST in (loc or ""):
        print("FAIL .org 301 into .net", loc)
        fail += 1
    else:
        print("twin indep", code, loc or "")

    code, _, loc, _ = fetch(f"https://{HOST}/", follow=False)
    if code in (301, 302, 303, 307, 308) and TWIN in (loc or ""):
        print("FAIL .net 301 into .org", loc)
        fail += 1

    for a in DESTS:
        code, _, loc, _ = fetch(a, follow=False)
        if code in (301, 302, 303, 307, 308) and HOST in (loc or ""):
            print("FAIL dest 301 into .net", a, loc)
            fail += 1
        else:
            print("indep", a, code)

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
