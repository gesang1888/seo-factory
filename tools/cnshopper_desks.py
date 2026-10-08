#!/usr/bin/env python3
"""CNShopper .net hub: unique CMS homepage. Sibling spreadsheet.net stays independent.

Gates:
1. Homepage is unique CMS (money title CNShopper Spreadsheet). Not leftover dest
   #local / “not a customs territory” H1 / products-API dump.
2. Titles have no invite token. Body has no customs coaching / 58-line.
3. Two same-agent .net hosts stay independent — no 301 between cnshopper.net and
   cnshopperspreadsheet.net. Do not leftover-PUT either (SKIP_UNIQUE).
4. Ranked unique inners on cnshopper.net must 200. Do not 301
   /cnshopper-spreadsheet-2026.html into / (0 GSC clicks; keep until it cannibalises).
5. Official storage is 90 days on cnshopper.com — confirm Help the morning you ship.
"""
from __future__ import annotations

import os
import re
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "sites"
EST = "https://www.cnshopper.com/en/estimate"
OFFICIAL = "https://www.cnshopper.com/en"
HELP = "https://www.cnshopper.com/en/help"
DATE = "8 Oct 2026"
EMAIL = "cnfd85269032661@gmail.com"
MONEY_TITLE = "CNShopper Spreadsheet 2026"
SIBLING = "cnshopperspreadsheet.net"
HOST = "cnshopper.net"

RANKED_CMS = (
    ("/cnshopper-spreadsheet-2026.html", 20000),
    ("/cnshopper-coupon-tracker-2026.html", 20000),
    ("/is-cnshopper-legit.html", 20000),
    ("/cnshopper-shipping-lines-2026.html", 20000),
    ("/cnshopper-real-shipping-bills-2026.html", 8000),
    ("/cnshopper-user-reports-2026.html", 8000),
    ("/cnshopper-faq.html", 8000),
    ("/fr/avis-cnshopper.html", 8000),
)

INNER_TITLES = {
    "/cnshopper-spreadsheet-2026.html": "CNShopper Spreadsheet Categories 2026",
    "/cnshopper-coupon-tracker-2026.html": "CNShopper Coupons 2026",
    "/is-cnshopper-legit.html": "Is CNShopper Legit?",
    "/cnshopper-shipping-lines-2026.html": "CNShopper Shipping Lines 2026",
}


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
    if EMAIL not in html:
        err.append("missing contact email")
    if "wa.me/8615396628356" not in html:
        err.append("missing WhatsApp +8615396628356")
    if "447856544534" in html or "+44 7856" in html:
        err.append("old UK WhatsApp still on homepage")
    if "w2clinks.com/spreadsheet/cnshopper/" not in html:
        err.append("missing w2clinks CNShopper sheet")
    if SIBLING not in html or "no 301" not in html.lower():
        err.append("missing sibling independence")
    if re.search(r"58 l[ií]neas para Espa|23[,.]81\s*USD|how to under-?declar", html, flags=re.I):
        err.append("spain snapshot / coaching")
    if len(html) < 20000:
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
        raise SystemExit("leftover_hub_skins.py must SKIP_UNIQUE cnshopper.net")
    print("unique overlay ok", dest, "bytes", len(html))


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
    bak = f"/www/backup/cnshopper-hub-deepen-{stamp}"
    _run(client, f"mkdir -p '{bak}'")
    sftp = client.open_sftp()

    net_conf = "/www/server/panel/vhost/nginx/cnshopper.net.conf"
    net_bak = "/www/server/panel/vhost/nginx/cnshopper.net.conf.bak-evasion-alias"
    live_conf = _run(client, f"cat '{net_conf}'")
    if SIBLING in live_conf and "return 301" in live_conf:
        _run(client, f"cp -a '{net_conf}' '{bak}/cnshopper.net.conf.stub-301'")
        _run(client, f"cp -a '{net_bak}' '{net_conf}'")
        print("restored", net_conf, "from bak-evasion-alias")
    else:
        print("cnshopper.net vhost already serving")

    local = OUT / HOST / "overlay" / "index.html"
    remote = f"/www/wwwroot/{HOST}/index.html"
    raw = local.read_text(encoding="utf-8")
    err = _unique_home_errors(raw)
    if err:
        raise SystemExit("refusing PUT: " + "; ".join(err))
    _run(client, f"cp -a '{remote}' '{bak}/{HOST}.index.html'")
    sftp.put(str(local), remote)
    print("PUT", remote, "bytes", local.stat().st_size)

    nginx_t = _run(client, "nginx -t 2>&1")
    print(nginx_t)
    if "successful" not in nginx_t.lower() and "ok" not in nginx_t.lower():
        raise SystemExit("nginx -t failed; not reloading")
    print(_run(client, "nginx -s reload 2>&1"))
    sftp.close()
    print("backup", bak)
    print("did not PUT", SIBLING, "homepage")
    client.close()
    _cf_purge(HOST)


def live_check() -> None:
    import urllib.error
    import urllib.request

    class NR(urllib.request.HTTPRedirectHandler):
        def redirect_request(self, req, fp, code, msg, headers, newurl):
            return None

    def fetch(url, follow=True):
        req = urllib.request.Request(url, headers={"User-Agent": "cnshopper-hub-check/1.0"})
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
        if loc and SIBLING in loc:
            print("FAIL sibling 301 from", HOST)
            fail += 1
    else:
        print("indep home", code)

    code, _, loc, body = fetch(f"https://{SIBLING}/", follow=False)
    if code in (301, 302, 303, 307, 308):
        print("FAIL sibling hub 301", loc)
        fail += 1
        if loc and HOST in loc:
            print("FAIL sibling 301s onto", HOST)
    else:
        print("indep sibling", code, len(body) if body else 0)
        code, _, _, body = fetch(f"https://{SIBLING}/", follow=True)
        if code != 200 or len(body) < 4000:
            print("FAIL sibling collapsed", code, len(body) if body else 0)
            fail += 1

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
            if re.search(r"invite\s*(code)?\s*[A-Z0-9]{5,}", title, flags=re.I):
                print("FAIL invite in inner title", path, title)
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
