#!/usr/bin/env python3
"""EsgoBuy desks: surgical #local on the unique 34KB .net catalog hub.

Gates:
1. Hub #local has the HUB fingerprint, no dest-country fingerprints.
2. Estimator country ≠ TLD; .net must say it is not a customs territory.
   GSC is mixed USA/CAN/GBR/ITA — still a hub, not a dest country.
3. Titles have no invite token V0HXH6F40B; body has no customs coaching / 58-line snapshot.
   Coupon stacking stays on /esgobuy-coupons/ (not the homepage title).
4. Single public dest host on origin — no same-agent country 301. www already 301s to apex.
5. No same-country extra hosts on origin. Ranked unique inners must 200. 2026 unique
   (23KB, 0 clk) 301s into stronger unique spreadsheet (42KB) — keep. Deep paths must not 404.
6. Unique 34KB catalog stays. Surgical #local insert only — do not PUT a 5KB country
   template over 23–44KB CMS. spam-p0 `return 410` is restored to try_files.

Official Help/estimation are 200 on www.esgobuy.com; do not invent a free-day count.
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
EST = "https://www.esgobuy.com/estimation"
OFFICIAL = "https://www.esgobuy.com/"
HELP = "https://www.esgobuy.com/help"
DATE = "2 Oct 2026"
INVITE = "V0HXH6F40B"
HUB_MIN = 30000
LIVE_HUB_MIN = 30000
STORAGE = (
    "Official EsgoBuy Help is the live site "
    f"({HELP}); confirm that live copy the morning you ship. "
    "This desk does not invent a free-day count."
)

HUBS = {
    "net": {
        "host": "esgobuyspreadsheet.net",
        "lang": "en",
        "loc": "en",
        "dest": None,
        "dest_label": "a country in the estimator",
        "ccy": "USD",
        "title": None,
        "h1": None,
        "keep": [
            ("/esgobuy-coupons/", "Coupons"),
            ("/esgobuy-shipping-guide/", "Shipping"),
            ("/is-esgobuy-legit/", "Legit"),
            ("/esgobuy-spreadsheet/", "Spreadsheet"),
            ("/esgobuy-shoes-spreadsheet/", "Shoes (ranked)"),
            ("/blog/", "Blog"),
        ],
    },
}

EST_NOTE = {
    "net": (
        "This .net hub is not a customs territory. Mixed US/CA/GB clicks do not "
        "make .net a customs dest. Pick the real ship-to country in the official "
        "estimator, not this hostname, not “EU” as one country."
    ),
}

STORE_NOTE = {
    "en": (
        "Warehouse: official EsgoBuy Help. Confirm that live copy the morning you "
        "ship. Do not invent a free-day count on this hub."
    ),
}

TRAIL = {"en": ("Live money is in", "this HTML is not checkout.")}

HUB_LOCAL_CSS = (
    ".sg-sec#local{max-width:1100px;margin:1.5rem auto;padding:0 24px}"
    ".sg-sec#local h2{margin-top:0}"
    ".ssub{color:var(--g3,#555);font-size:.95rem;margin:0 0 12px}"
    ".local-steps{margin:12px 0 0;padding:0;list-style:none;display:grid;gap:12px}"
    ".local-steps li{border:1px solid #e5e7eb;border-radius:12px;padding:14px 16px;background:#fff}"
    ".local-steps strong{display:block;margin:0 0 6px;font-size:15px}"
    ".local-steps span{display:block;color:#334155;line-height:1.7;font-size:15px}"
    ".local-src{font-size:14px;color:#334155;line-height:1.7;margin:14px 0 0}"
    "#local{scroll-margin-top:96px}"
)

ALIENS = ("1010 Wien", "Packstation", "form A1A 1A1", "Poste Italiane", "00-001 Warszawa")

TITLE_SCRUB_REL = (
    "esgobuy-coupons/index.html",
    "esgobuy-invite-code/index.html",
)

RANKED_CMS = (
    ("/esgobuy-coupons/", 20000),
    ("/esgobuy-shipping-guide/", 20000),
    ("/is-esgobuy-legit/", 20000),
    ("/esgobuy-spreadsheet/", 20000),
    ("/esgobuy-shoes-spreadsheet/", 8000),
    ("/how-to-use-esgobuy/", 8000),
    ("/blog/", 8000),
    ("/esgobuy-qc-guide/", 8000),
    ("/esgobuy-refund-guide/", 8000),
    ("/esgobuy-invite-code/", 8000),
    ("/esgobuy-community/", 8000),
)

KEEP_REDIRECTS = (
    ("/esgobuy-spreadsheet-2026/", "/esgobuy-spreadsheet/"),
    ("/esgobuy-spreadsheet-2026", "/esgobuy-spreadsheet/"),
)

INVITE_REGISTER = "https://www.esgobuy.com/user/register?affcode=V0HXH6F40B"

HERO_END = "</section>\n<div class=\"trust\">"
NAV_UL = '<ul class="nl">'
CHROME = ("class=\"nav\"", "hero fade-in", "ccard", "EsgoBuy Spreadsheet")


def _facts(spec: dict) -> dict:
    return {
        "agent": "EsgoBuy",
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
        s = re.sub(re.escape(INVITE), "", s, flags=re.I)
        s = re.sub(r"(?i)\s*[—\-–:,]*\s*invite\s*$", "", s)
        s = re.sub(r"\s{2,}", " ", s).strip(" —–-,;")
        return s

    def title_sub(m):
        if new_title:
            return f"<title>{escape(new_title)}</title>"
        return f"<title>{scrub(m.group(1))}</title>"

    html = re.sub(r"<title>(.*?)</title>", title_sub, html, count=1, flags=re.S)
    html = re.sub(
        r'(<meta property="og:title" content=")([^"]+)(")',
        lambda m: m.group(1) + (new_title or scrub(m.group(2))) + m.group(3),
        html,
        count=1,
    )
    return html


def _scrub_token_from_home(html: str) -> str:
    html = html.replace(
        '<div class="ann">&#128293; EsgoBuy deal: verify email for <strong>¥1080 shipping coupons</strong> · '
        "Invite <strong>V0HXH6F40B</strong> · "
        f'<a href="{INVITE_REGISTER}" target="_blank" rel="noopener">Register &rarr;</a></div>',
        '<div class="ann">&#128293; EsgoBuy deal: verify email for <strong>¥1080 shipping coupons</strong> · '
        'coupon stacking on the coupons page · '
        '<a href="/esgobuy-coupons/">Open coupons &rarr;</a></div>',
    )
    html = html.replace(INVITE_REGISTER, OFFICIAL)
    html = html.replace("Register + ¥1080 coupons", "Open EsgoBuy")
    html = html.replace(
        "Use <strong>V0HXH6F40B</strong> for ¥1080 shipping coupon pack off. Verified weekly.",
        "Coupon stacking stays on /esgobuy-coupons/ · ¥1080 shipping coupon pack. Verified weekly.",
    )
    html = html.replace(INVITE, "")
    html = html.replace("affcode=", "")
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
        html = html.replace("<body>", "<body>\n" + skip_link(skip_label(loc)).rstrip(), 1)
    if 'id="main"' not in html:
        html = html.replace(
            '<section class="hero fade-in">',
            '<section class="hero fade-in" id="main">',
            1,
        )
    if 'href="#local"' not in html:
        if NAV_UL not in html:
            raise RuntimeError("hub nav missing")
        html = html.replace(
            NAV_UL,
            NAV_UL + f'<li><a href="#local">{escape(local_cta(facts))}</a></li>',
            1,
        )
    if "#local{scroll-margin-top" not in html:
        if "</style>" in html:
            html = html.replace("</style>", SKIP_CSS + HUB_LOCAL_CSS + "\n</style>", 1)
        else:
            html = html.replace("</head>", "<style>" + SKIP_CSS + HUB_LOCAL_CSS + "</style>\n</head>", 1)
    if 'id="local"' in html:
        html = re.sub(
            r'<section class="sg-sec" id="local".*?</section>',
            block,
            html,
            count=1,
            flags=re.S,
        )
    else:
        if HERO_END not in html:
            raise RuntimeError("hub hero marker missing")
        html = html.replace(HERO_END, "</section>\n" + block + "\n<div class=\"trust\">", 1)
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
    if "not a customs territory" not in html:
        err.append("hub missing fingerprint")
    if len(html.encode("utf-8")) < HUB_MIN:
        err.append(f"hub collapsed to {len(html.encode('utf-8'))} bytes")
    for marker in CHROME:
        if marker not in html:
            err.append(f"hub chrome missing {marker}")
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
        s = re.sub(r"(?i)\s*[—\-–:,]*\s*invite\b", "", s)
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
    bak = f"/www/backup/esgobuy-desks-{stamp}"
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
        if local.stat().st_size < HUB_MIN:
            raise SystemExit(f"refusing to PUT collapsed hub {local.stat().st_size} B")
        for marker in CHROME:
            if marker not in raw:
                raise SystemExit(f"refusing to PUT hub missing chrome {marker}")
        _run(client, f"cp -a '{remote}' '{bak}/{spec['host']}.index.html'")
        sftp.put(str(local), remote)
        print("PUT", remote, "bytes", local.stat().st_size)

        vhost = f"/www/server/panel/vhost/nginx/{spec['host']}.conf"
        _run(client, f"cp -a '{vhost}' '{bak}/{spec['host']}.conf'")
        vraw = _run(client, f"cat '{vhost}'")
        new = vraw.replace(
            "    location / { return 410; }",
            "    location / { try_files $uri $uri/ $uri/index.html =404; }",
            1,
        )
        if new == vraw:
            new = vraw.replace(
                "    location / {\n        return 410;\n    }",
                "    location / {\n        try_files $uri $uri/ $uri/index.html =404;\n    }",
                1,
            )
        if "return 410" in new and "try_files $uri $uri/ $uri/index.html =404" not in new:
            raise SystemExit("hub nginx still 410 and restore did not match")
        if new != vraw:
            with sftp.file(vhost, "w") as fh:
                fh.write(new)
            print("restored vhost try_files (was 410)")
        else:
            print("hub nginx already serving")

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
            leftover = bool(re.search(r"(?i)[—\-–:,]\s*invite\b", title))
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
            print("scrub title", rel, "title", title)

    nginx_t = _run(client, "nginx -t 2>&1")
    print(nginx_t)
    if "successful" not in nginx_t.lower() and "ok" not in nginx_t.lower():
        raise SystemExit("nginx -t failed; not reloading")
    print(_run(client, "nginx -s reload 2>&1"))
    sftp.close()
    print("backup", bak)
    print("unique 34KB catalog kept; 410 restored; 2026→spreadsheet kept; no dest overlay")
    client.close()


def live_check() -> None:
    import urllib.request

    class NR(urllib.request.HTTPRedirectHandler):
        def redirect_request(self, req, fp, code, msg, headers, newurl):
            return None

    def fetch(url, follow=True):
        req = urllib.request.Request(url, headers={"User-Agent": "esgobuy-desk-check/1.0"})
        opener = urllib.request.build_opener() if follow else urllib.request.build_opener(NR)
        try:
            with opener.open(req, timeout=25) as resp:
                return resp.status, resp.geturl(), resp.headers.get("Location") or "", resp.read()
        except urllib.error.HTTPError as e:
            return e.code, url, e.headers.get("Location") or "", e.read() if e.fp else b""

    fail = 0
    url = "https://esgobuyspreadsheet.net/"
    code, _, loc, body = fetch(url, follow=True)
    html = body.decode("utf-8", "replace")
    title_m = re.search(r"<title>(.*?)</title>", html, flags=re.S)
    title = title_m.group(1) if title_m else ""
    inner_m = re.search(r'<section class="sg-sec" id="local".*?</section>', html, flags=re.S)
    inner = inner_m.group(0) if inner_m else ""
    fp = "not a customs territory"
    print(f"net {code} bytes={len(body)} local={bool(inner)} fp={fp in html}")
    if code == 410:
        print("  FAIL homepage still 410")
        fail += 1
    elif code != 200 or not inner or fp not in inner:
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
        if len(body) < LIVE_HUB_MIN:
            print("  FAIL hub collapsed", len(body))
            fail += 1
        for marker in CHROME:
            if marker not in html:
                print("  FAIL hub chrome gone", marker)
                fail += 1

    code, _, loc, _ = fetch(url, follow=False)
    if code in (301, 302, 303, 307, 308):
        print("FAIL hub 301", loc)
        fail += 1
    else:
        print("indep hub", code)

    for path, min_bytes in RANKED_CMS:
        inner_url = f"https://esgobuyspreadsheet.net{path}"
        code, _, loc, _ = fetch(inner_url, follow=False)
        if code in (301, 302, 303, 307, 308) and loc:
            if path.rstrip("/") not in loc and not loc.rstrip("/").endswith(path.rstrip("/")):
                print("FAIL 301 inner", inner_url, "->", loc)
                fail += 1
                continue
        code, final, _, body = fetch(inner_url, follow=True)
        if code == 404 or code == 410 or len(body) < min_bytes:
            print("FAIL inner", inner_url, code, len(body), final)
            fail += 1
        else:
            print("inner", code, len(body), final)
            html = body.decode("utf-8", "replace")
            title_m = re.search(r"<title>(.*?)</title>", html, flags=re.S)
            title = title_m.group(1) if title_m else ""
            if path in ("/esgobuy-coupons/", "/esgobuy-invite-code/") and (
                INVITE in title or re.search(r"(?i)[—\-–:,]\s*invite\s*$", title)
            ):
                print("FAIL invite in inner title", path, title)
                fail += 1

    for src, dst in KEEP_REDIRECTS:
        inner_url = f"https://esgobuyspreadsheet.net{src}"
        code, _, loc, _ = fetch(inner_url, follow=False)
        if code not in (301, 302, 303, 307, 308) or dst.rstrip("/") not in (loc or ""):
            print("FAIL expected 301", inner_url, code, "->", loc, "want", dst)
            fail += 1
        else:
            print("kept 301", src, "->", loc)
            code2, final, _, body = fetch(inner_url, follow=True)
            if code2 != 200 or len(body) < 8000:
                print("FAIL redirect target thin/404", final, code2, len(body))
                fail += 1
            else:
                print("redirect target", code2, len(body), final)

    code, _, loc, _ = fetch("https://www.esgobuyspreadsheet.net/", follow=False)
    if code in (301, 302, 303, 307, 308) and "esgobuyspreadsheet.net" in (loc or ""):
        print("www apex", code, loc)
    else:
        print("www", code, loc)

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
