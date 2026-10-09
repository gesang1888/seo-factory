#!/usr/bin/env python3
"""Thinner leftover sisters: unique CMS homes, not clones (Aug 2026 duplicate-site).

Hosts:
- lovegobuyguide.com — Guide 2026 (how-to). Twin lovegobuyspreadsheet.eu.
- lovegobuyspreadsheet.eu — Spreadsheet 2026. Twin lovegobuyguide.com.
- kakobuydocs.com — Docs 2026. Do not PUT ranked /kakobuy-shipping-guide/.
- fansbuy.eu — EU Desk 2026. Twin fansbuysheets.net (no 301).
- cssbuyspreadsheet.eu — Spreadsheet 2026. Skip unique cssbuy.co.uk.

Do not leftover-PUT (SKIP_UNIQUE). Do not invent free-day counts except
FansBuy 90-day and CSSBuy warehouse FAQ already published. Invite tokens
stay off homepages.
"""
from __future__ import annotations

import os
import re
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "sites"
EMAIL = "cnfd85269032661@gmail.com"
HUB_MIN = 17000
LIVE_HUB_MIN = 18000

HOSTS = (
    {
        "host": "lovegobuyguide.com",
        "title": "LoveGoBuy Guide 2026",
        "invite": "W5RJX3",
        "twin": "lovegobuyspreadsheet.eu",
        "chrome": ("#e91e12", "Rubik", "LoveGoBuy Guide 2026"),
        "need": ("does not invent a free-day", "dest-country skin", "not Excel", "Google Sheet"),
        "ranked": (
            ("/how-to-use-lovegobuy/", 8000),
            ("/lovegobuy-spreadsheet/", 8000),
            ("/is-lovegobuy-legit/", 8000),
        ),
        "redirects": (("/lovegobuy-coupons/", "/lovegobuy-coupon/"), ("/coupons/", "/lovegobuy-coupon/")),
        "thin": ("/start/",),
        "dests": ("https://lovegobuyspreadsheet.eu/", "https://lovegobuy.nl/"),
        "inner_titles": {"/lovegobuy-spreadsheet/": "LoveGoBuy Spreadsheet 2026"},
    },
    {
        "host": "lovegobuyspreadsheet.eu",
        "title": "LoveGoBuy Spreadsheet 2026",
        "invite": "W5RJX3",
        "twin": "lovegobuyguide.com",
        "chrome": ("#e91e12", "Rubik", "LoveGoBuy Spreadsheet 2026"),
        "need": ("does not invent a free-day", "dest-country skin", "not Excel", "Google Sheet"),
        "ranked": (
            ("/lovegobuy-spreadsheet/", 8000),
            ("/how-to-use-lovegobuy/", 8000),
            ("/is-lovegobuy-legit/", 8000),
        ),
        "redirects": (("/coupons/", "/lovegobuy-coupon/"),),
        "thin": ("/start/",),
        "dests": ("https://lovegobuyguide.com/", "https://lovegobuy.nl/"),
        "inner_titles": {"/lovegobuy-spreadsheet/": "LoveGoBuy Spreadsheet 2026"},
    },
    {
        "host": "kakobuydocs.com",
        "title": "Kakobuy Docs 2026",
        "invite": "yze69",
        "twin": "kakobuy.com",
        "chrome": ("#FF5C00", "IBM Plex Sans", "Kakobuy Docs 2026"),
        "need": ("$410", "€3", "does not invent a free-day", "dest-country skin", "not Excel", "discord.gg/XAbKcnzmcX"),
        "ranked": (
            ("/kakobuy-shipping-guide/", 20000),
            ("/kakobuy-spreadsheet/", 20000),
            ("/how-to-use-kakobuy/", 20000),
            ("/kakobuy-coupons/", 20000),
            ("/is-kakobuy-legit/", 20000),
            ("/kakobuy-shoes-spreadsheet/", 8000),
        ),
        "redirects": (("/coupons/", "/kakobuy-coupons/"),),
        "thin": ("/start/",),
        "dests": (),
        "inner_titles": {"/kakobuy-shipping-guide/": "Kakobuy Shipping Guide 2026"},
        "forbid_title": ("KAKODOCS",),
    },
    {
        "host": "fansbuy.eu",
        "title": "FansBuy EU Desk 2026",
        "invite": "Fans-pys5Zt48",
        "twin": "fansbuysheets.net",
        "chrome": ("#FF3444", "Noto Sans", "FansBuy EU Desk 2026"),
        "need": ("90-Day Free Storage", "FANS26", "dest-country skin", "not Excel", "14 Oct 2026"),
        "ranked": (
            ("/fansbuy-shipping-guide/", 8000),
            ("/fansbuy-spreadsheet/", 20000),
            ("/how-to-use-fansbuy/", 8000),
            ("/is-fansbuy-legit/", 8000),
            ("/fansbuy-coupons/", 8000),
        ),
        "redirects": (),
        "thin": ("/coupons/",),
        "dests": ("https://fansbuysheets.net/", "https://fansbuy.co.uk/", "https://fansbuy.nl/"),
        "inner_titles": {"/fansbuy-spreadsheet/": "FansBuy Spreadsheet EU"},
        "www_apex_optional": True,  # live www currently 301s a foreign ACBuy dest
    },
    {
        "host": "cssbuyspreadsheet.eu",
        "title": "CSSBuy Spreadsheet 2026",
        "invite": "1Yi9",
        "twin": "cssbuy.co.uk",
        "chrome": ("#E85D1A", "Barlow", "CSSBuy Spreadsheet 2026"),
        "need": ("90 free days", "dest-country skin", "not Excel", "cssbuy.co.uk"),
        "ranked": (
            ("/spreadsheet/", 8000),
            ("/faq/", 8000),
            ("/guides/", 8000),
            ("/guides/shipping/", 8000),
        ),
        "redirects": (),
        "thin": ("/start/", "/coupons/"),
        "dests": ("https://cssbuy.co.uk/",),
        "inner_titles": {"/spreadsheet/": "CSSBuy Spreadsheet EU"},
        "skip_put_twin": True,
    },
)


def _decode_cf_email(html: str) -> str:
    out = []
    for m in re.finditer(r'data-cfemail="([0-9a-fA-F]+)"', html):
        hexed = m.group(1)
        key = int(hexed[:2], 16)
        chars = [chr(int(hexed[i : i + 2], 16) ^ key) for i in range(2, len(hexed), 2)]
        out.append("".join(chars))
    return " ".join(out)


def _has_email(html: str) -> bool:
    return EMAIL in html or EMAIL in _decode_cf_email(html)


def unique_errors(spec: dict, html: str) -> list[str]:
    err: list[str] = []
    title_m = re.search(r"<title>(.*?)</title>", html, flags=re.S)
    title = re.sub(r"<[^>]+>", "", title_m.group(1) if title_m else "")
    h1_m = re.search(r"<h1[^>]*>(.*?)</h1>", html, flags=re.S)
    h1 = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", h1_m.group(1) if h1_m else "")).strip()
    money = spec["title"]
    if money not in title.replace("&amp;", "&"):
        err.append(f"title missing money words: {title!r}")
    if "Coupons" in title or spec["invite"] in title:
        err.append(f"invite/coupon in title: {title!r}")
    if money.split(" 2026")[0] not in h1.replace("&amp;", "&") or "2026" not in h1:
        err.append(f"h1 missing money words: {h1!r}")
    if spec["invite"] in html:
        err.append("frozen invite token still on homepage")
    if "inviteCode=" in html or "invite_id=" in html:
        err.append("frozen invite query")
    if 'id="local"' in html or "not a customs territory" in html.lower():
        err.append("leftover dest hub skin")
    if "/api/products/" in html:
        err.append("products API dump")
    if not _has_email(html):
        err.append("missing contact email")
    if "wa.me/8615396628356" not in html:
        err.append("missing WhatsApp")
    if "Women's Fashion" not in html and "Women’s Fashion" not in html:
        err.append("missing Women's Fashion")
    if spec["twin"] not in html:
        err.append(f"missing twin {spec['twin']}")
    if "official-promo" not in html or "/assets/images/official-logo.png" not in html:
        err.append("missing official 图文 / logo")
    if "w2clinks" not in html:
        err.append("missing w2clinks")
    if 'class="nav"' not in html or "hero fade-in" not in html or "ccard" not in html or "nbrand" not in html:
        err.append("missing hub chrome")
    for marker in spec["chrome"]:
        if marker not in html:
            err.append(f"missing chrome {marker}")
    for n in spec["need"]:
        if n not in html:
            err.append(f"missing {n}")
    for bad in spec.get("forbid_title", ()):
        if bad in title:
            err.append(f"forbid in title {bad}")
    if re.search(r"58 l[ií]neas para Espa|23[,.]81\s*USD|how to under-?declar", html, flags=re.I):
        err.append("coaching")
    if len(html) < HUB_MIN:
        err.append(f"home too small {len(html)}")
    return err


def generate() -> None:
    leftover = (ROOT / "tools" / "leftover_hub_skins.py").read_text(encoding="utf-8")
    if "SKIP_UNIQUE" not in leftover:
        raise SystemExit("leftover_hub_skins.py missing SKIP_UNIQUE")
    for spec in HOSTS:
        host = spec["host"]
        if f'"{host}"' not in leftover:
            raise SystemExit(f"SKIP_UNIQUE must include {host}")
        html = (OUT / host / "overlay" / "index.html").read_text(encoding="utf-8")
        err = unique_errors(spec, html)
        if err:
            raise SystemExit(f"{host}: " + "; ".join(err))
        ch = (OUT / host / "overlay" / "coupons.html").read_text(encoding="utf-8")
        if spec["invite"] in ch:
            raise SystemExit(f"{host} coupons invite leak")
        print("ok", host, len(html))


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
        print("CF zone lookup failed", host, e)
        return
    zid = (data.get("result") or [{}])[0].get("id")
    if not zid:
        print("CF zone not found", host)
        return
    preq = urllib.request.Request(
        f"https://api.cloudflare.com/client/v4/zones/{zid}/purge_cache",
        data=json.dumps({"purge_everything": True}).encode(),
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(preq, timeout=20) as resp:
        out = json.loads(resp.read().decode())
    print("CF purge", host, out.get("success"))


def put() -> None:
    generate()
    client = _connect()
    stamp = time.strftime("%Y%m%d-%H%M%S")
    bak = f"/www/backup/thin-leftover-sisters-{stamp}"
    _run(client, f"mkdir -p '{bak}'")
    sftp = client.open_sftp()
    for spec in HOSTS:
        host = spec["host"]
        local = OUT / host / "overlay" / "index.html"
        err = unique_errors(spec, local.read_text(encoding="utf-8"))
        if err:
            raise SystemExit(f"refusing PUT {host}: " + "; ".join(err))
        remote = f"/www/wwwroot/{host}/index.html"
        _run(client, f"mkdir -p '{bak}/{host}' && cp -a '{remote}' '{bak}/{host}/index.html'")
        sftp.put(str(local), remote)
        print("PUT", remote, local.stat().st_size)
        coup_l = OUT / host / "overlay" / "coupons.html"
        coup_r = f"/www/wwwroot/{host}/coupons.html"
        _run(client, f"cp -a '{coup_r}' '{bak}/{host}/coupons.html' 2>/dev/null || true")
        sftp.put(str(coup_l), coup_r)
        print("PUT", coup_r)
        _run(client, f"mkdir -p '/www/wwwroot/{host}/assets/images' '/www/wwwroot/{host}/assets/official'")
        img_dir = OUT / host / "overlay" / "assets" / "images"
        for img in sorted(img_dir.rglob("*")):
            if not img.is_file():
                continue
            rel = img.relative_to(img_dir).as_posix()
            remote_img = f"/www/wwwroot/{host}/assets/images/{rel}"
            _run(client, f"mkdir -p '{Path(remote_img).parent}'")
            sftp.put(str(img), remote_img)
        off_dir = OUT / host / "overlay" / "assets" / "official"
        for img in sorted(off_dir.glob("*")):
            sftp.put(str(img), f"/www/wwwroot/{host}/assets/official/{img.name}")
        print("PUT assets", host)
    nginx_t = _run(client, "nginx -t 2>&1")
    print(nginx_t)
    if "successful" not in nginx_t.lower() and "ok" not in nginx_t.lower():
        raise SystemExit("nginx -t failed")
    print(_run(client, "nginx -s reload 2>&1"))
    sftp.close()
    print("backup", bak)
    print("did not PUT ranked inners; did not PUT cssbuy.co.uk")
    client.close()
    for spec in HOSTS:
        _cf_purge(spec["host"])


def live_check() -> None:
    import urllib.error
    import urllib.request

    class NR(urllib.request.HTTPRedirectHandler):
        def redirect_request(self, req, fp, code, msg, headers, newurl):
            return None

    def fetch(url, follow=True):
        req = urllib.request.Request(url, headers={"User-Agent": "thin-sisters-check/1.0"})
        opener = urllib.request.build_opener() if follow else urllib.request.build_opener(NR)
        try:
            with opener.open(req, timeout=25) as resp:
                return resp.status, resp.geturl(), resp.headers.get("Location") or "", resp.read()
        except urllib.error.HTTPError as e:
            return e.code, url, e.headers.get("Location") or "", e.read() if e.fp else b""

    fail = 0
    for spec in HOSTS:
        host = spec["host"]
        print("\n====", host)
        code, _, loc, body = fetch(f"https://{host}/", follow=True)
        html = body.decode("utf-8", "replace")
        print("home", code, "bytes", len(body))
        if code != 200:
            print(" FAIL home")
            fail += 1
            continue
        if len(body) < LIVE_HUB_MIN:
            print(" FAIL home too small", len(body))
            fail += 1
        for e in unique_errors(spec, html):
            print(" FAIL", e)
            fail += 1
        code, _, loc, _ = fetch(f"https://www.{host}/", follow=False)
        if spec.get("www_apex_optional"):
            print("www note", code, loc)
        elif code not in (301, 302, 303, 307, 308) or host not in (loc or ""):
            print("FAIL www not 301 apex", code, loc)
            fail += 1
        else:
            print("www", code, loc)
        code, _, loc, _ = fetch(f"https://{host}/", follow=False)
        if code in (301, 302, 303, 307, 308):
            print("FAIL 301 home", loc)
            fail += 1
        for src, dst in spec["redirects"]:
            code, _, loc, _ = fetch(f"https://{host}{src}", follow=False)
            if code not in (301, 302, 303, 307, 308) or dst.rstrip("/") not in (loc or ""):
                print("FAIL 301", src, code, loc, "want", dst)
                fail += 1
            else:
                print("kept 301", src, loc)
        for path, min_bytes in spec["ranked"]:
            url = f"https://{host}{path}"
            code, _, loc, _ = fetch(url, follow=False)
            if code in (301, 302, 303, 307, 308) and loc:
                print("FAIL 301 inner", url, loc)
                fail += 1
                continue
            code, final, _, body = fetch(url, follow=True)
            if code == 404 or len(body) < min_bytes:
                print("FAIL inner", url, code, len(body))
                fail += 1
            else:
                print("inner", path, code, len(body))
                html = body.decode("utf-8", "replace")
                title_m = re.search(r"<title>(.*?)</title>", html, flags=re.S)
                title = title_m.group(1) if title_m else ""
                need = spec["inner_titles"].get(path)
                if need and need not in title.replace("&amp;", "&"):
                    print("FAIL inner title", path, title)
                    fail += 1
        coup = fetch(f"https://{host}/coupons.html", follow=True)
        if coup[0] != 200 or len(coup[3]) < 1500:
            print("FAIL coupons.html", coup[0], len(coup[3]))
            fail += 1
        else:
            print("coupons.html", coup[0], len(coup[3]))
        for path in spec["thin"]:
            code, _, loc, _ = fetch(f"https://{host}{path}", follow=False)
            print("thin", path, code, loc or "")
        twin = spec["twin"]
        if "." in twin and not twin.startswith("kakobuy.com"):
            code, _, loc, _ = fetch(f"https://{twin}/", follow=False)
            if code in (301, 302, 303, 307, 308) and host in (loc or ""):
                print("FAIL twin 301 into host", twin, loc)
                fail += 1
            else:
                print("twin indep", twin, code)
        for a in spec["dests"]:
            code, _, loc, _ = fetch(a, follow=False)
            if code in (301, 302, 303, 307, 308) and host in (loc or ""):
                print("FAIL dest 301 into", host, a, loc)
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
