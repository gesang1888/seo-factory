#!/usr/bin/env python3
"""FansBuy .net hub: unique Spreadsheet 2026 home. .eu twin stays independent.

Gates:
1. Homepage is unique CMS (money title FansBuy Spreadsheet 2026). Not leftover
   dest #local / “not a customs territory” H1 / products-API dump.
2. Titles have no invite token. Body has no customs coaching. Frozen invite
   stays off the homepage. Ranked /fansbuy-invite-code/ may keep 200.
   Coupon stacking stays on /fansbuy-coupons/ (not the homepage title).
3. Independent of fansbuy.eu — no 301. FansBuy is not USFans. Official
   checkout is fansbuy.com. www already 301s apex. Do not leftover-PUT
   (SKIP_UNIQUE). Keep slash aliases. Keep pre-existing
   /fansbuy-spreadsheet-2026/ → /fansbuy-spreadsheet/.
4. Ranked unique inners must 200. Do not PUT /fansbuy-coupons/. Thin leftover
   /coupons/ /shipping/ /start/ stay 404. Extra /coupons.html is 图文.
5. Official fansbuy.com 9 Oct 2026: QC Photos & Videos · 90-Day Free Storage,
   150+ lines, Anniversary Giveaway through 14 Oct 2026, FANS26 26% OFF
   shipping (not the money title). Chrome #FF3444 / Noto Sans (MiSans-like).
   Official Discord cited from that homepage. Do not restore dest #local.
"""
from __future__ import annotations

import os
import re
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "sites"
OFFICIAL = "https://fansbuy.com/"
DATE = "9 Oct 2026"
EMAIL = "cnfd85269032661@gmail.com"
MONEY_TITLE = "FansBuy Spreadsheet 2026"
HOST = "fansbuysheets.net"
TWIN = "fansbuy.eu"
INVITE = "Fans-pys5Zt48"
HUB_MIN = 20000
LIVE_HUB_MIN = 21000
CHROME = (
    'class="nav"',
    "hero fade-in",
    "nbrand",
    "ccard",
    "FansBuy Spreadsheet 2026",
    "#FF3444",
    "Noto Sans",
)

RANKED_CMS = (
    ("/fansbuy-coupons/", 20000),
    ("/fansbuy-shipping-guide/", 20000),
    ("/fansbuy-invite-code/", 15000),
    ("/fansbuy-spreadsheet/", 20000),
    ("/is-fansbuy-legit/", 20000),
    ("/fansbuy-refund-guide/", 15000),
    ("/how-to-use-fansbuy/", 15000),
    ("/fansbuy-shoes-spreadsheet/", 8000),
    ("/blog/", 8000),
    ("/fansbuy-qc-guide/", 8000),
)

KEEP_REDIRECTS = (
    ("/fansbuy-coupons", "/fansbuy-coupons/"),
    ("/fansbuy-shipping-guide", "/fansbuy-shipping-guide/"),
    ("/fansbuy-invite-code", "/fansbuy-invite-code/"),
    ("/fansbuy-spreadsheet", "/fansbuy-spreadsheet/"),
    ("/is-fansbuy-legit", "/is-fansbuy-legit/"),
    ("/fansbuy-refund-guide", "/fansbuy-refund-guide/"),
    ("/how-to-use-fansbuy", "/how-to-use-fansbuy/"),
    ("/fansbuy-spreadsheet-2026/", "/fansbuy-spreadsheet/"),
)

INNER_TITLES = {
    "/fansbuy-spreadsheet/": "FansBuy Spreadsheet",
}

THIN_404 = ("/coupons/", "/shipping/", "/start/")


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
    if "QC" in title or "Coupons" in title or "FANS26" in title or "26%" in title:
        err.append(f"coupon pack still in money title: {title!r}")
    if MONEY_TITLE not in h1.replace("&amp;", "&"):
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
    if "90-Day Free Storage" not in html and "90-Day" not in html:
        err.append("missing official 90-Day Free Storage")
    if "150+" not in html:
        err.append("missing official 150+ shipping lines")
    if "FANS26" not in html:
        err.append("missing official FANS26 (body, not title)")
    if "14 Oct 2026" not in html and "October 14" not in html:
        err.append("missing anniversary deadline 14 Oct 2026")
    if "discord.com/invite/4VPxrzrB6Z" not in html:
        err.append("missing official Discord from homepage")
    if "Women's Fashion" not in html:
        err.append("missing Women's Fashion")
    if "dest-country skin" not in html:
        err.append("missing dest-country-skin line")
    if TWIN not in html:
        err.append(f"missing twin independence {TWIN}")
    if "USFans" not in html and "usfans" not in html:
        err.append("missing FansBuy ≠ USFans")
    if "official-promo" not in html:
        err.append("missing official promo strip")
    if "/assets/images/official-logo.png" not in html:
        err.append("missing official FansBuy trademark")
    if "/assets/official/official-home.jpg" not in html and "/assets/official/official-promo.jpg" not in html:
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
        raise SystemExit("leftover_hub_skins.py must SKIP_UNIQUE fansbuysheets.net")
    coupons = OUT / HOST / "overlay" / "coupons.html"
    ch = coupons.read_text(encoding="utf-8")
    cerr = []
    if "FansBuy Coupons 2026" not in ch:
        cerr.append("coupons title")
    if "FANS26" not in ch:
        cerr.append("coupons missing FANS26")
    if "90-Day Free Storage" not in ch:
        cerr.append("coupons missing 90-Day Free Storage")
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
    bak = f"/www/backup/fansbuy-sheets-hub-deepen-{stamp}"
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
    for img in sorted(img_dir.glob("*")):
        sftp.put(str(img), f"/www/wwwroot/{HOST}/assets/images/{img.name}")
        print("PUT image", img.name, img.stat().st_size)
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
        req = urllib.request.Request(url, headers={"User-Agent": "fansbuy-sheets-hub-check/1.0"})
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
    if code != 200 or len(body) < 2000 or "FANS26" not in ch:
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
        print("FAIL .eu 301 into .net", loc)
        fail += 1
    else:
        print("twin indep", code, loc or "")

    code, _, loc, _ = fetch(f"https://{HOST}/", follow=False)
    if code in (301, 302, 303, 307, 308) and TWIN in (loc or ""):
        print("FAIL .net 301 into .eu", loc)
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
