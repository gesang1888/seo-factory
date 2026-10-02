#!/usr/bin/env python3
"""HipoBuy review.com extra hub: restore independence + dest-unique #local.

Gates:
1. Hub #local has the HUB fingerprint, no dest-country fingerprints.
2. Estimator country ≠ TLD; .com must say it is not a customs territory.
3. Titles have no invite token VGEICZNX0; body has no customs coaching / 58-line snapshot.
   Coupon stacking stays on /hipobuy-coupons/ (not the homepage title).
4. Same-agent country dests (hipobuy.at etc.) and the PHP .net hub stay independent — no 301.
5. Catch-all 301 into hipobuyspreadsheet.net 404ed ranked unique paths. Restore the
   origin vhost so GSC URLs 200. Deep paths must not 404.
6. Thin Georgia home gets #local. Do not PUT a 5KB overlay over unique 27–58KB CMS
   or over the 69KB PHP .net hub (already has #local).

hipobuyspreadsheet.net is EyouCMS PHP (GSC 2739 clk, live ~69KB, #local already).
Leave it alone. hipobuyreview.com is the extra .com with unique ranked CMS.
"""
from __future__ import annotations

import os
import re
import sys
import time
from html import escape
from pathlib import Path

_TOOLS = Path(__file__).resolve().parent
if str(_TOOLS) not in sys.path:
    sys.path.insert(0, str(_TOOLS))
from desk_template import (
    SKIP_CSS,
    _check_local_section,
    assert_dest_packs_unique,
    dest_local_pack,
    local_cta,
    local_guide_html,
    skip_label,
    skip_link,
)

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "sites"
EST = "https://hipobuy.com/estimation"
OFFICIAL = "https://hipobuy.com/"
HELP = "https://hipobuy.com/help"
DATE = "2 Oct 2026"
INVITE = "VGEICZNX0"
STORAGE = (
    "Official HipoBuy Help is the live SPA "
    f"({HELP}); confirm that live copy the morning you ship. "
    "This desk does not invent a free-day count."
)

HUBS = {
    "com": {
        "host": "hipobuyreview.com",
        "lang": "en",
        "loc": "en",
        "dest": None,
        "dest_label": "a country in the estimator",
        "ccy": "USD",
        "title": "HipoBuy .com hub — not a customs territory",
        "h1": "This .com hostname is not a customs territory — pick a real country",
        "keep": [
            ("/hipobuy-coupons/", "Coupons (ranked)"),
            ("/is-hipobuy-legit/", "Legit (ranked)"),
            ("/hipobuy-shipping-guide/", "Shipping guide"),
            ("/hipobuy-spreadsheet/", "Spreadsheet"),
            ("/hipobuy-refund-guide/", "Refunds"),
        ],
    },
}

EST_NOTE = {
    "com": "This .com hub is not a customs territory. Country ccTLDs (AT, NL, UK…) stay independent. Pick the real ship-to country in the official estimator, not this hostname, not “EU” as one country.",
}

STORE_NOTE = {
    "en": "Warehouse: official HipoBuy Help (SPA). Confirm that live copy the morning you ship. Do not invent a free-day count on this hub.",
}

TRAIL = {"en": ("Live money is in", "this HTML is not checkout.")}

DEST_LOCAL_CSS = (
    ".sg-sec#local{margin:1.25rem 0 0}"
    ".sg-sec#local h2{margin-top:0}"
    ".ssub{color:var(--muted,#57534e);font-size:.95rem;margin:0 0 12px}"
)

ALIENS = ("1010 Wien", "Packstation", "form A1A 1A1", "Poste Italiane", "00-001 Warszawa")

TITLE_SCRUB_REL = (
    "hipobuy-coupons/index.html",
    "hipobuy-invite-code/index.html",
)

RANKED_CMS = (
    ("/hipobuy-coupons/", 20000),
    ("/is-hipobuy-legit/", 20000),
    ("/hipobuy-shipping-guide/", 20000),
    ("/hipobuy-spreadsheet/", 20000),
    ("/hipobuy-refund-guide/", 8000),
    ("/how-to-use-hipobuy/", 8000),
    ("/blog/", 8000),
    ("/hipobuy-invite-code/", 8000),
)

KEEP_REDIRECTS = (
    ("/hipobuy-spreadsheet-2026/", "/hipobuy-spreadsheet/"),
)


def _facts(spec: dict) -> dict:
    return {
        "agent": "HipoBuy",
        "host": spec["host"],
        "lang": spec["lang"],
        "loc": spec["loc"],
        "dest": spec.get("dest"),
        "dest_label": spec.get("dest_label") or "a country in the estimator",
        "ccy": spec["ccy"],
        "storage": STORAGE,
        "estimator": EST,
        "official": OFFICIAL,
        "date": DATE,
        "keep": spec.get("keep") or [],
        "codes_off_title": [INVITE],
        "strict_html_codes": True,
    }


def _local_block(key: str, spec: dict) -> str:
    facts = _facts(spec)
    loc = spec["loc"]
    fp = dest_local_pack(facts.get("dest"))["fingerprint"]
    store = STORE_NOTE.get(loc) or STORE_NOTE["en"]
    live, not_co = TRAIL.get(loc) or TRAIL["en"]
    extra = (
        f'<p class="local-src">{escape(fp)}. {escape(EST_NOTE[key])} {escape(store)} '
        f"{escape(live)} <a href=\"{escape(facts['estimator'])}\">{escape(facts['estimator'])}</a> "
        f"— {escape(not_co)}</p>"
    )
    html = local_guide_html(facts).strip()
    if not html.endswith("</section>"):
        raise RuntimeError(f"{key}: missing section")
    html = html[: -len("</section>")] + extra + "\n</section>"
    err: list[str] = []
    _check_local_section(html, facts, err)
    if err:
        raise RuntimeError(f"{key} #local: {'; '.join(err)}")
    return html


def _strip_invite_title(html: str, new_title: str | None = None) -> str:
    def scrub(s: str) -> str:
        s = re.sub(r"\s*[—\-–:,]*\s*(invite|ref|code|coupon)\s*[A-Za-z0-9]{5,}", "", s, flags=re.I)
        s = re.sub(re.escape(INVITE), "", s, flags=re.I)
        s = re.sub(r"\s{2,}", " ", s).strip(" —–-,;")
        return s

    def title_sub(m):
        if new_title:
            return f"<title>{escape(new_title)}</title>"
        return f"<title>{scrub(m.group(1))}</title>"

    html = re.sub(r"<title>(.*?)</title>", title_sub, html, count=1, flags=re.S)
    return html


def _scrub_token_from_home(html: str) -> str:
    html = html.replace(f"https://hipobuy.com/register?inviteCode={INVITE}", OFFICIAL)
    html = html.replace(f"inviteCode={INVITE}", "")
    html = html.replace(INVITE, "")
    return html


def patch_static(html: str, key: str, spec: dict) -> str:
    facts = _facts(spec)
    block = _local_block(key, spec)
    loc = spec["loc"]
    html = _scrub_token_from_home(html)
    html = _strip_invite_title(html, spec.get("title"))
    if spec.get("h1"):
        html = re.sub(r"<h1>.*?</h1>", f"<h1>{escape(spec['h1'])}</h1>", html, count=1, flags=re.S)
    if 'class="skip"' not in html:
        html = re.sub(
            r"(<body[^>]*>)",
            r"\1\n" + skip_link(skip_label(loc)).rstrip(),
            html,
            count=1,
        )
    if 'id="main"' not in html:
        html = re.sub(r"<main>", '<main id="main">', html, count=1)
    if 'href="#local"' not in html:
        html = html.replace(
            "</header>",
            f'  <nav><a href="#local">{escape(local_cta(facts))}</a>\n'
            f'    <a href="/hipobuy-coupons/">Coupons</a>\n'
            f'    <a href="/is-hipobuy-legit/">Legit</a></nav>\n</header>',
            1,
        )
    if "#local{scroll-margin-top" not in html:
        if "</style>" in html:
            html = html.replace("</style>", SKIP_CSS + DEST_LOCAL_CSS + "\n</style>", 1)
        else:
            html = html.replace("</head>", "<style>" + SKIP_CSS + DEST_LOCAL_CSS + "</style>\n</head>", 1)
    if 'id="local"' in html:
        html = re.sub(
            r'<section class="sg-sec" id="local".*?</section>',
            block,
            html,
            count=1,
            flags=re.S,
        )
    else:
        html = re.sub(r"(<h1>.*?</h1>)", r"\1\n" + block, html, count=1, flags=re.S)
    err: list[str] = []
    _check_local_section(html, facts, err)
    title_m = re.search(r"<title>(.*?)</title>", html, flags=re.S)
    title = title_m.group(1) if title_m else ""
    if re.search(r"invite\s*(code)?\s*[A-Z0-9]{5,}", title, flags=re.I) or INVITE in title:
        err.append("invite in title")
    if INVITE in html:
        err.append("frozen invite token still on homepage")
    if re.search(r"58 l[ií]neas para Espa|23[,.]81\s*USD|how to under-?declar", html, flags=re.I):
        err.append("spain snapshot / coaching")
    if err:
        raise RuntimeError(f"{key}: {'; '.join(err)}")
    return html


def generate() -> None:
    assert_dest_packs_unique()
    blobs = {}
    specs = {**HUBS}
    for key, spec in specs.items():
        src = OUT / spec["host"] / "live-base" / "index.html"
        html = patch_static(src.read_text(encoding="utf-8"), key, spec)
        dest = OUT / spec["host"] / "overlay" / "index.html"
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(html, encoding="utf-8")
        inner = re.search(r'<section class="sg-sec" id="local".*?</section>', html, flags=re.S)
        blobs[key] = inner.group(0) if inner else ""
        print("hub", key, spec["host"], "bytes", len(html.encode("utf-8")))
    fps = {k: dest_local_pack(specs[k].get("dest"))["fingerprint"] for k in blobs}
    for key, inner in blobs.items():
        fp = fps[key]
        if fp not in inner:
            raise SystemExit(f"{key} missing fingerprint {fp!r}")
        for alien in ALIENS:
            if alien in inner:
                raise SystemExit(f"{key} leaked dest {alien!r}")
        if EST not in inner:
            raise SystemExit(f"{key} missing estimator")
        if "not a customs territory" not in inner:
            raise SystemExit(f"{key} hub missing customs-territory line")
        if INVITE in inner:
            raise SystemExit(f"{key} #local still has invite token")
    print("generate ok", len(blobs), "desks")


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


def _scrub_title_token(html: str) -> str:
    def scrub(s: str) -> str:
        s = re.sub(re.escape(INVITE), "", s, flags=re.I)
        s = re.sub(r"(?i)\s*[—\-–:,]*\s*(invite\s+)?VGEICZNX0", "", s)
        s = re.sub(r"(?i)\s*[—\-–:,]*\s*invite(\s*code)?\s*$", "", s)
        s = re.sub(r"\s{2,}", " ", s).strip(" —–-,;&")
        return s

    html = re.sub(
        r"<title>(.*?)</title>",
        lambda m: f"<title>{scrub(m.group(1))}</title>",
        html,
        count=1,
        flags=re.S,
    )
    html = re.sub(
        r"<h1([^>]*)>(.*?)</h1>",
        lambda m: f"<h1{m.group(1)}>{scrub(m.group(2))}</h1>",
        html,
        count=1,
        flags=re.S,
    )
    return html


def put() -> None:
    generate()
    client = _connect()
    stamp = time.strftime("%Y%m%d-%H%M%S")
    bak = f"/www/backup/hipobuyreview-desks-{stamp}"
    _run(client, f"mkdir -p '{bak}'")
    sftp = client.open_sftp()
    for spec in HUBS.values():
        local = OUT / spec["host"] / "overlay" / "index.html"
        remote = f"/www/wwwroot/{spec['host']}/index.html"
        raw = local.read_text(encoding="utf-8")
        if 'id="local"' not in raw or "not a customs territory" not in raw:
            raise SystemExit(f"refusing to PUT {spec['host']} without hub #local")
        if INVITE in raw:
            raise SystemExit(f"refusing to PUT {spec['host']} with frozen invite token")
        live = _run(client, f"wc -c < '{remote}'")
        try:
            live_n = int(live.strip().split()[0])
        except ValueError:
            live_n = 0
        if live_n > 20000:
            raise SystemExit(f"refusing to PUT over unique CMS home {live_n} B")
        vhost = f"/www/server/panel/vhost/nginx/{spec['host']}.conf"
        _run(client, f"cp -a '{vhost}' '{bak}/{spec['host']}.conf'")
        _run(client, f"cp -a '{remote}' '{bak}/{spec['host']}.index.html'")
        vhost_src = OUT / spec["host"] / "live-base" / "vhost.conf"
        sftp.put(str(vhost_src), vhost)
        print("restored vhost", vhost)
        sftp.put(str(local), remote)
        print("PUT", remote, "bytes", local.stat().st_size)

        root = f"/www/wwwroot/{spec['host']}"
        for rel in TITLE_SCRUB_REL:
            remote_inner = f"{root}/{rel}"
            try:
                with sftp.open(remote_inner) as fh:
                    inner_html = fh.read().decode("utf-8")
            except FileNotFoundError:
                print("skip missing", remote_inner)
                continue
            title_m = re.search(r"<title>(.*?)</title>", inner_html, flags=re.S)
            title = title_m.group(1) if title_m else ""
            leftover = bool(re.search(r"(?i)[—\-–:,]\s*invite\s*$", title))
            if INVITE not in title and not leftover:
                print("title already clean", rel)
                continue
            before = len(inner_html)
            _run(client, f"cp -a '{remote_inner}' '{bak}/{rel.replace('/', '_')}'")
            scrubbed = _scrub_title_token(inner_html)
            title_m = re.search(r"<title>(.*?)</title>", scrubbed, flags=re.S)
            title = title_m.group(1) if title_m else ""
            if INVITE in title:
                raise SystemExit(f"title still has invite after scrub: {rel} {title!r}")
            if abs(len(scrubbed) - before) > 400:
                raise SystemExit(f"title scrub changed {rel} too much ({before}->{len(scrubbed)})")
            with sftp.file(remote_inner, "w") as fh:
                fh.write(scrubbed)
            print("scrub title", rel, "bytes", len(scrubbed))

    nginx_t = _run(client, "nginx -t 2>&1")
    print(nginx_t)
    if "successful" not in nginx_t.lower() and "ok" not in nginx_t.lower():
        raise SystemExit("nginx -t failed; not reloading")
    print(_run(client, "nginx -s reload 2>&1"))
    sftp.close()
    print("backup", bak)
    print("review.com restored independent; PHP .net hub untouched")
    client.close()


def live_check() -> None:
    import urllib.request

    class NR(urllib.request.HTTPRedirectHandler):
        def redirect_request(self, req, fp, code, msg, headers, newurl):
            return None

    def fetch(url, follow=True):
        req = urllib.request.Request(url, headers={"User-Agent": "hipobuyreview-desk-check/1.0"})
        opener = urllib.request.build_opener() if follow else urllib.request.build_opener(NR)
        try:
            with opener.open(req, timeout=25) as resp:
                return resp.status, resp.geturl(), resp.headers.get("Location") or "", resp.read()
        except urllib.error.HTTPError as e:
            return e.code, url, e.headers.get("Location") or "", e.read() if e.fp else b""

    fail = 0
    url = "https://hipobuyreview.com/"
    code, _, loc, body = fetch(url, follow=True)
    html = body.decode("utf-8", "replace")
    title_m = re.search(r"<title>(.*?)</title>", html, flags=re.S)
    title = title_m.group(1) if title_m else ""
    inner_m = re.search(r'<section class="sg-sec" id="local".*?</section>', html, flags=re.S)
    inner = inner_m.group(0) if inner_m else ""
    fp = "not a customs territory"
    print(f"com {code} bytes={len(body)} local={bool(inner)} fp={fp in html}")
    if code != 200 or not inner or fp not in inner:
        print("  FAIL status/local/fp")
        fail += 1
    else:
        for alien in ALIENS:
            if alien in inner:
                print("  FAIL sister", alien)
                fail += 1
        if INVITE in title or INVITE in html:
            print("  FAIL invite on homepage")
            fail += 1
        if re.search(r"58 l[ií]neas para Espa|23[,.]81\s*USD|how to under-?declar", html, flags=re.I):
            print("  FAIL snapshot/coaching")
            fail += 1
        if EST not in inner:
            print("  FAIL estimator")
            fail += 1

    code, _, loc, _ = fetch("https://hipobuyreview.com/", follow=False)
    if code in (301, 302, 303, 307, 308) and loc and "hipobuyspreadsheet.net" in loc:
        print("FAIL 301 review into .net", loc)
        fail += 1
    else:
        print("indep review.com", code)

    for path, min_bytes in RANKED_CMS:
        url = f"https://hipobuyreview.com{path}"
        code, _, loc, _ = fetch(url, follow=False)
        if code in (301, 302, 303, 307, 308) and loc:
            if "hipobuyspreadsheet.net" in loc:
                print("FAIL 301 inner into .net", url, "->", loc)
                fail += 1
                continue
            if path.rstrip("/") not in loc and not loc.rstrip("/").endswith(path.rstrip("/")):
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
            if path in ("/hipobuy-coupons/", "/hipobuy-invite-code/") and (
                INVITE in title or re.search(r"(?i)[—\-–:,]\s*invite\s*$", title)
            ):
                print("FAIL invite in inner title", path, title)
                fail += 1

    for src, dst in KEEP_REDIRECTS:
        url = f"https://hipobuyreview.com{src}"
        code, _, loc, _ = fetch(url, follow=False)
        if code not in (301, 302, 303, 307, 308) or dst.rstrip("/") not in (loc or ""):
            print("FAIL expected 301", url, code, "->", loc, "want", dst)
            fail += 1
        else:
            print("kept 301", src, "->", loc)
            code2, final, _, body = fetch(url, follow=True)
            if code2 != 200 or len(body) < 8000:
                print("FAIL redirect target thin/404", final, code2, len(body))
                fail += 1
            else:
                print("redirect target", code2, len(body), final)

    php = "https://hipobuyspreadsheet.net/"
    code, _, loc, body = fetch(php, follow=True)
    html = body.decode("utf-8", "replace")
    print("php", code, len(body), "local", 'id="local"' in html)
    if code != 200 or len(body) < 40000 or 'id="local"' not in html:
        print("FAIL PHP .net hub collapsed or missing #local")
        fail += 1
    if re.search(r"58 l[ií]neas para Espa|23[,.]81\s*USD", html, flags=re.I):
        print("FAIL php snapshot")
        fail += 1

    for a in ("https://hipobuy.at/", "https://hipobuyspreadsheet.nl/", "https://hipobuyspreadsheet.net/"):
        code, _, loc, _ = fetch(a, follow=False)
        if code in (301, 302, 303, 307, 308) and loc and "hipobuyreview.com" in loc:
            print("FAIL dest 301 into review", a, loc)
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
