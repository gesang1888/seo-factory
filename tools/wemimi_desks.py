#!/usr/bin/env python3
"""WeMimi desks: surgical #local on PHP CMS hub + Georgia spreadsheet hub.

Gates:
1. Each host #local has the HUB fingerprint, no dest-country fingerprints.
2. Estimator country ≠ TLD; .net / .com hubs say they are not a customs territory.
3. Titles have no invite code; body has no customs coaching / 58-line snapshot.
4. wemimi.net ≠ wemimispreadsheet.com — independent (no 301). www already 301s apex.
5. No same-country twins to convert. Spreadsheet inners stay 200.
6. wemimi.net stays EyouCMS (surgical insert into template/pc/index.htm, HUB_MIN).
   Do not PUT a 5KB country template over the restored PHP home.
   Official Help is an SPA — do not invent warehouse days.
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
EST = "https://www.wemimi.com/"
OFFICIAL = "https://www.wemimi.com/"
HELP = "https://www.wemimi.com/"
DATE = "2 Oct 2026"
STORAGE = (
    "Official WeMimi app storage notice in the live help center "
    f"({HELP}); confirm that live copy the morning you ship. "
    "This desk does not invent a free-day count."
)
HUB_MIN = 50000  # EyouCMS template/pc/index.htm must stay a real CMS home
LIVE_HUB_MIN = 50000  # rendered PHP home

HUBS = {
    "php": {
        "host": "wemimi.net",
        "lang": "en",
        "loc": "en",
        "dest": None,
        "dest_label": "a country in the estimator",
        "ccy": "USD",
        "title": "WeMimi .net hub — not a customs territory",
        "h1": None,  # keep CMS h1
        "kind": "php",
        "keep": [
            ("/#categories", "Category wall"),
            ("/#how-it-works", "How it works"),
            ("/#faq", "FAQ"),
        ],
    },
    "ss": {
        "host": "wemimispreadsheet.com",
        "lang": "en",
        "loc": "en",
        "dest": None,
        "dest_label": "a country in the estimator",
        "ccy": "USD",
        "title": "WeMimi spreadsheet.com hub — not a customs territory",
        "h1": "This .com hostname is not a customs territory — pick a real country",
        "kind": "static",
        "keep": [
            ("/shoes381/", "Shoes (ranked)"),
            ("/wemimispread-coupon-tracker-2026.html", "Coupon tracker"),
            ("/wemimispread-user-reports-2026.html", "User reports"),
            ("/wemimispread-shipping-lines-2026.html", "Shipping lines"),
        ],
    },
}

EST_NOTE = {
    "php": "This .net PHP hub is not a customs territory. Pick the real ship-to country in the official WeMimi app freight estimate, not this hostname, not “EU” as one country, not wemimispreadsheet.com.",
    "ss": "This spreadsheet.com hub is not a customs territory. Pick the real ship-to country in the official WeMimi app freight estimate, not this hostname, not wemimi.net as a country.",
}

STORE_NOTE = {
    "en": "Warehouse: official WeMimi app storage notice (SPA help center); confirm that live copy the morning you ship. Do not invent a free-day count on this hub.",
}

TRAIL = {
    "en": ("Live money is in", "this HTML is not checkout."),
}

HUB_LOCAL_CSS = (
    ".sg-sec#local{margin:1.25rem 0 0}"
    ".sg-sec#local h2{margin-top:0}"
    ".ssub{color:var(--muted,#57534e);font-size:.95rem;margin:0 0 12px}"
    ".local-steps{margin:12px 0 0;padding:0;list-style:none;display:grid;gap:12px}"
    ".local-steps li{border:1px solid #e5e7eb;border-radius:12px;padding:14px 16px;background:#fff}"
    ".local-steps strong{display:block;margin:0 0 6px;font-size:15px}"
    ".local-steps span{display:block;color:#334155;line-height:1.7;font-size:15px}"
    ".local-src{font-size:14px;color:#334155;line-height:1.7;margin:14px 0 0}"
    "#local{scroll-margin-top:96px}"
)

ALIENS = ("1010 Wien", "Packstation", "form A1A 1A1", "Poste Italiane", "00-001 Warszawa")


def _facts(spec: dict) -> dict:
    return {
        "agent": "WeMimi",
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
        "codes_off_title": [],
        "strict_html_codes": False,
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
        s = re.sub(r"\s*[—\-–:,]*\s*(invite|ref|code|coupon)\s*[A-Z0-9]{5,}", "", s, flags=re.I)
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


def _title_ok(html: str) -> list[str]:
    err: list[str] = []
    title_m = re.search(r"<title>(.*?)</title>", html, flags=re.S)
    title = title_m.group(1) if title_m else ""
    if re.search(r"invite\s*(code)?\s*[A-Z0-9]{5,}", title, flags=re.I):
        err.append("invite in title")
    if re.search(r"58 l[ií]neas para Espa|23[,.]81\s*USD|how to under-?declar", html, flags=re.I):
        err.append("spain snapshot / coaching")
    return err


def _scrub_stale_ss(html: str) -> str:
    """Spreadsheet skin still described the PHP hub as 500 — that is no longer true."""
    reps = (
        (
            "Do not 301 onto wemimi.net (currently 500). Independent notes only.",
            "Independent of wemimi.net — no 301 between these hubs.",
        ),
        (
            " <strong>500</strong> — <strong>do not 301 this spreadsheet host onto a 500</strong>, and do not PUT an overlay over that CMS. Restore the hub as an ops job, separately.",
            " 200 as EyouCMS. These two hosts stay independent (no 301).",
        ),
        (
            "currently returns <strong>500</strong>",
            "answers 200 as the EyouCMS hub",
        ),
        (
            "Not a clone of wemimi.net while that hub is erroring.",
            "Not a clone of wemimi.net.",
        ),
        (
            "Blocked until the hub answers 200 with unique copy.",
            "No 301; both hubs stay independent.",
        ),
        (
            "Not a 301 onto wemimi.net while it 500s.",
            "Not a 301 onto wemimi.net.",
        ),
        ("~54&nbsp;MB ThinkPHP", "EyouCMS PHP"),
        ("impressions on a template", "impressions on this dest desk"),
        ("impressions on a 5 KB skin", "impressions on this dest desk"),
    )
    for old, new in reps:
        html = html.replace(old, new)
    return html


def patch_static(html: str, key: str, spec: dict) -> str:
    facts = _facts(spec)
    block = _local_block(key, spec)
    loc = spec["loc"]
    html = _strip_invite_title(html, spec.get("title"))
    html = _scrub_stale_ss(html)
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
    if 'href="#local"' not in html and "</nav>" in html:
        html = html.replace(
            "</nav>",
            f'    <a href="#local">{escape(local_cta(facts))}</a>\n  </nav>',
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
        html = re.sub(r"(<h1>.*?</h1>)", r"\1\n" + block, html, count=1, flags=re.S)
    err: list[str] = []
    _check_local_section(html, facts, err)
    err.extend(_title_ok(html))
    if err:
        raise RuntimeError(f"{key}: {'; '.join(err)}")
    return html


def patch_php_hub(html: str) -> str:
    """Surgical #local into EyouCMS template/pc/index.htm — keep catalog chrome."""
    key, spec = "php", HUBS["php"]
    facts = _facts(spec)
    block = _local_block(key, spec)
    html = _strip_invite_title(html, spec["title"])
    if 'class="skip"' not in html:
        html = html.replace("<body>", "<body>\n" + skip_link("Skip to content").rstrip(), 1)
    if 'id="main"' not in html:
        html = html.replace("<main>", '<main id="main">', 1)
    if 'href="#local"' not in html:
        html = html.replace(
            '<li><a href="#faq" class="nav-item">FAQ</a></li>',
            '<li><a href="#faq" class="nav-item">FAQ</a></li>\n                    '
            f'<li><a href="#local" class="nav-item">{escape(local_cta(facts))}</a></li>',
            1,
        )
    if "#local{scroll-margin-top" not in html:
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
        marker = "</section>\n\n        <!-- Categories Section -->"
        if marker not in html:
            raise RuntimeError("php hub hero marker missing")
        html = html.replace(marker, "</section>\n" + block + "\n        <!-- Categories Section -->", 1)
    err: list[str] = []
    _check_local_section(html, facts, err)
    err.extend(_title_ok(html))
    if "not a customs territory" not in html:
        err.append("hub missing fingerprint")
    if len(html) < HUB_MIN:
        err.append(f"hub collapsed to {len(html)} bytes")
    if 'class="hero"' not in html or 'id="faq"' not in html:
        err.append("hub chrome missing")
    if err:
        raise RuntimeError(f"php hub: {'; '.join(err)}")
    return html


def generate() -> None:
    assert_dest_packs_unique()
    blobs = {}
    php_src = OUT / "wemimi.net" / "live-base" / "index.htm"
    php_html = patch_php_hub(php_src.read_text(encoding="utf-8"))
    php_dest = OUT / "wemimi.net" / "overlay" / "index.htm"
    php_dest.parent.mkdir(parents=True, exist_ok=True)
    php_dest.write_text(php_html, encoding="utf-8")
    inner = re.search(r'<section class="sg-sec" id="local".*?</section>', php_html, flags=re.S)
    blobs["php"] = inner.group(0) if inner else ""
    print("php wemimi.net template bytes", len(php_html), "was", php_src.stat().st_size)

    ss = HUBS["ss"]
    ss_src = OUT / ss["host"] / "live-base" / "index.html"
    ss_html = patch_static(ss_src.read_text(encoding="utf-8"), "ss", ss)
    ss_dest = OUT / ss["host"] / "overlay" / "index.html"
    ss_dest.parent.mkdir(parents=True, exist_ok=True)
    ss_dest.write_text(ss_html, encoding="utf-8")
    inner = re.search(r'<section class="sg-sec" id="local".*?</section>', ss_html, flags=re.S)
    blobs["ss"] = inner.group(0) if inner else ""
    print("ss wemimispreadsheet.com bytes", len(ss_html))

    fps = {k: dest_local_pack(HUBS[k].get("dest"))["fingerprint"] for k in blobs}
    for key, inner in blobs.items():
        fp = fps[key]
        if fp not in inner:
            raise SystemExit(f"{key} missing fingerprint {fp!r}")
        for other, ofp in fps.items():
            if other == key or ofp == fp:
                continue
            if ofp in inner:
                raise SystemExit(f"{key} leaked {other} {ofp!r}")
        for alien in ALIENS:
            if alien in inner:
                raise SystemExit(f"{key} leaked dest {alien!r}")
        if EST.split("://", 1)[-1].rstrip("/") not in inner and EST not in inner:
            raise SystemExit(f"{key} missing estimator")
        if "not a customs territory" not in inner:
            raise SystemExit(f"{key} hub missing customs-territory line")
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


def put() -> None:
    generate()
    client = _connect()
    stamp = time.strftime("%Y%m%d-%H%M%S")
    bak = f"/www/backup/wemimi-desks-{stamp}"
    _run(client, f"mkdir -p '{bak}'")
    sftp = client.open_sftp()

    php_local = OUT / "wemimi.net" / "overlay" / "index.htm"
    php_remote = "/www/wwwroot/wemimi.net/template/pc/index.htm"
    raw = php_local.read_text(encoding="utf-8")
    if 'id="local"' not in raw or "not a customs territory" not in raw:
        raise SystemExit("refusing to PUT php hub without #local fingerprint")
    if php_local.stat().st_size < HUB_MIN:
        raise SystemExit(f"refusing to PUT php hub collapsed to {php_local.stat().st_size}")
    if 'class="hero"' not in raw or 'id="faq"' not in raw:
        raise SystemExit("refusing to PUT php hub missing CMS chrome")
    _run(client, f"cp -a '{php_remote}' '{bak}/wemimi.net.template-pc-index.htm'")
    sftp.put(str(php_local), php_remote)
    print("PUT", php_remote, "bytes", php_local.stat().st_size)
    print(_run(client, "rm -rf /www/wwwroot/wemimi.net/data/runtime/cache/* /www/wwwroot/wemimi.net/data/runtime/temp/* ; echo cache-cleared"))

    ss_local = OUT / "wemimispreadsheet.com" / "overlay" / "index.html"
    ss_remote = "/www/wwwroot/wemimispreadsheet.com/index.html"
    raw = ss_local.read_text(encoding="utf-8")
    if 'id="local"' not in raw or "not a customs territory" not in raw:
        raise SystemExit("refusing to PUT ss hub without #local fingerprint")
    _run(client, f"cp -a '{ss_remote}' '{bak}/wemimispreadsheet.com.index.html'")
    sftp.put(str(ss_local), ss_remote)
    print("PUT", ss_remote, "bytes", ss_local.stat().st_size)
    sftp.close()
    print("backup", bak)
    print("no dests; two hubs stay independent (no 301)")
    client.close()


def live_check() -> None:
    import urllib.request

    pairs = [
        (
            "php",
            "https://wemimi.net/",
            "not a customs territory",
            ALIENS,
        ),
        (
            "ss",
            "https://wemimispreadsheet.com/",
            "not a customs territory",
            ALIENS,
        ),
    ]

    class NR(urllib.request.HTTPRedirectHandler):
        def redirect_request(self, req, fp, code, msg, headers, newurl):
            return None

    def fetch(url, follow=True):
        req = urllib.request.Request(url, headers={"User-Agent": "wemimi-desk-check/1.0"})
        opener = urllib.request.build_opener() if follow else urllib.request.build_opener(NR)
        try:
            with opener.open(req, timeout=25) as resp:
                return resp.status, resp.geturl(), resp.headers.get("Location") or "", resp.read()
        except urllib.error.HTTPError as e:
            return e.code, url, e.headers.get("Location") or "", e.read() if e.fp else b""

    fail = 0
    for key, url, fp, aliens in pairs:
        code, _, loc, body = fetch(url, follow=True)
        html = body.decode("utf-8", "replace")
        title_m = re.search(r"<title>(.*?)</title>", html, flags=re.S)
        title = title_m.group(1) if title_m else ""
        inner_m = re.search(r'<section class="sg-sec" id="local".*?</section>', html, flags=re.S)
        inner = inner_m.group(0) if inner_m else ""
        print(f"{key:3} {code} bytes={len(body)} local={bool(inner)} fp={fp in html}")
        if code != 200 or not inner or fp not in inner:
            print("  FAIL status/local/fp")
            fail += 1
            continue
        for alien in aliens:
            if alien in inner:
                print("  FAIL sister", alien)
                fail += 1
        if re.search(r"invite\s*(code)?\s*[A-Z0-9]{5,}", title, flags=re.I):
            print("  FAIL invite in title")
            fail += 1
        if re.search(r"58 l[ií]neas para Espa|23[,.]81\s*USD|how to under-?declar", html, flags=re.I):
            print("  FAIL snapshot/coaching")
            fail += 1
        if EST not in inner:
            print("  FAIL estimator url missing")
            fail += 1
        if "not a customs territory" not in inner:
            print("  FAIL hub customs line")
            fail += 1
        if key == "php":
            if len(body) < LIVE_HUB_MIN:
                print("  FAIL php hub collapsed", len(body))
                fail += 1
            if 'class="hero"' not in html or 'id="faq"' not in html:
                print("  FAIL php hub chrome")
                fail += 1
            if "网站暂时关闭" in html:
                print("  FAIL php hub still closed")
                fail += 1

    large_inners = [
        "https://wemimispreadsheet.com/shoes381/",
        "https://wemimispreadsheet.com/wemimispread-coupon-tracker-2026.html",
        "https://wemimispreadsheet.com/wemimispread-user-reports-2026.html",
        "https://wemimispreadsheet.com/wemimispread-shipping-lines-2026.html",
    ]
    for url in large_inners:
        code, final, _, body = fetch(url, follow=True)
        if code == 404 or len(body) < 8000:
            print("FAIL inner", url, code, len(body))
            fail += 1
        else:
            print("inner", code, len(body), final)

    dest_urls = ["https://wemimi.net/", "https://wemimispreadsheet.com/"]
    for a in dest_urls:
        code, _, loc, _ = fetch(a, follow=False)
        if code in (301, 302, 303, 307, 308) and loc:
            print("FAIL 301", a, "->", loc)
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
