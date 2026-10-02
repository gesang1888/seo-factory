#!/usr/bin/env python3
"""W2C Links hub: surgical #local on unique EyouCMS. No 5KB overlay.

Gates:
1. Hub #local has the HUB fingerprint, no dest-country fingerprints.
2. Estimator country ≠ TLD; .com catalog hub must say it is not a
   customs territory. Live freight form is /shipping-calculator/ on
   this host. W2C Links is not an agent warehouse — do not invent days.
3. Homepage title has no invite token. Body has no customs coaching /
   58-line snapshot.
4. w2crep.org stays independently open (no 301 either way). Same-agent
   extras w2cclothes.com / w2cshoes.com keep 301 $request_uri into
   w2crep.org, not into this search CMS.
5. No twins on w2clinks. www already 301 apex $request_uri.
6. Unique PHP CMS stays (surgical insert into template/pc/index.htm +
   header.htm nav). Do not PUT a 5KB dest template over the ~56KB PHP
   home. Do not PUT overlay onto index.html / index.php.

Skip repsicon.com (user: do not process). Skip unique dest overwrite
of sugargoo.ca/.es. Skip cheap no-vhost dests.
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
HOST = "w2clinks.com"
PUBLIC = "w2clinks.com"
EST = "https://w2clinks.com/shipping-calculator/"
OFFICIAL = "https://w2clinks.com/"
HELP = "https://w2clinks.com/guide/"
DATE = "2 Oct 2026"
INVITE = "___no_frozen_w2clinks_invite___"
TEMPLATE_MIN = 10000
HEADER_MIN = 14000
LIVE_HUB_MIN = 50000
STORAGE = (
    "W2C Links is not an agent warehouse. Storage days belong to the "
    f"agent you book. Ranked guide on this host: {HELP}. "
    "Confirm that agent’s Help the morning you ship. "
    "This desk does not invent a free-day count."
)

HUBS = {
    "com": {
        "host": HOST,
        "public": PUBLIC,
        "lang": "en",
        "loc": "en",
        "dest": None,
        "dest_label": "a country in the estimator",
        "ccy": "USD",
        "keep": [
            ("/spreadsheet/", "Spreadsheet"),
            ("/shipping-calculator/", "Shipping calculator"),
            ("/guide/", "Guide"),
            ("/news/", "Blog"),
            ("/agents/", "Agents"),
        ],
    },
}

EST_NOTE = {
    "com": (
        "This .com catalog hub is not a customs territory. Mixed clicks "
        "do not make .com a customs dest. Pick the real ship-to country "
        "in the live freight form on this host, not this hostname, not "
        "“EU” as one country, not w2crep.org as a country."
    ),
}

STORE_NOTE = {
    "en": (
        "Warehouse: W2C Links is not an agent. Confirm storage on the "
        "agent you book. Do not invent a free-day count on this hub."
    ),
}

TRAIL = {"en": ("Live money is in", "this HTML is not checkout.")}

HUB_LOCAL_CSS = (
    ".sg-sec#local{max-width:1100px;margin:1.5rem auto;padding:20px 24px;"
    "color:#111;background:#fff;border-radius:12px}"
    ".sg-sec#local h2{margin-top:0}"
    ".ssub{color:#555;font-size:.95rem;margin:0 0 12px}"
    ".local-src{font-size:14px;color:#2D2D2D;line-height:1.7;margin:14px 0 0}"
    ".local-src a{color:#1A56DB;text-decoration:underline}"
    "#local{scroll-margin-top:88px}"
)

ALIENS = (
    "1010 Wien",
    "Packstation",
    "form A1A 1A1",
    "Poste Italiane",
    "00-001 Warszawa",
    "00100 Helsinki",
    "no copiamos un recuento de líneas",
    "pas un code postal belge",
    "Nederlandse postcode",
    "does not invent a de-minimis dollar",
    "Northern Ireland is often another",
    "do not copy a GST rate",
)

RANKED_CMS = (
    ("/spreadsheet/", 20000),
    ("/shipping-calculator/", 8000),
    ("/guide/", 8000),
    ("/news/", 8000),
    ("/agents/", 8000),
)

EXTRAS_W2CREP = (
    "w2cclothes.com",
    "w2cshoes.com",
)
W2CREP = "w2crep.org"

HERO_END = '  </section>\n\n  <section class="w2c-section w2c-home-cats">'
NAV_MARK = (
    '        <li><a class="nav-link" href="/news/">'
    '<i class="fas fa-newspaper"></i> '
    '<span data-i18n="explore_blog">Blog</span></a></li>\n'
    "      </ul>"
)
TEMPLATE_CHROME = (
    "w2c-hero-drop",
    "EVERY DROP",
    "w2c-home-cats",
    "home-search",
    "Get Links",
    "W2C",
)
LIVE_CHROME = TEMPLATE_CHROME + (
    'class="nav-menu"',
    "Pick a country",
)
AGENT_FAQ_OLD = (
    "W2C Links is a purchasing agent: it buys from Chinese third-party "
    "shops in your name, photographs the parcel in its warehouse, then "
    "you book an international SKU."
)
AGENT_FAQ_NEW = (
    "W2C Links is a spreadsheet catalog, not a purchasing agent. The "
    "agent you pick in the header buys from Chinese third-party shops "
    "in your name, photographs the parcel in its warehouse, then you "
    "book an international SKU."
)


def _facts(spec: dict) -> dict:
    return {
        "agent": "W2C Links",
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
    html = html.replace(AGENT_FAQ_OLD, AGENT_FAQ_NEW)
    if not html.endswith("</section>"):
        raise RuntimeError(f"{key}: missing section")
    html = html[: -len("</section>")] + extra + "\n</section>"
    err: list[str] = []
    _check_local_section(html, facts, err)
    if err:
        raise RuntimeError(f"{key} #local: {'; '.join(err)}")
    if AGENT_FAQ_OLD in html:
        raise RuntimeError("purchasing-agent FAQ still on catalog hub")
    return html


def patch_header(html: str, spec: dict) -> str:
    facts = _facts(spec)
    cta = escape(local_cta(facts))
    if 'href="/#local"' not in html and 'href="#local"' not in html:
        if NAV_MARK not in html:
            raise RuntimeError("header nav marker missing")
        html = html.replace(
            NAV_MARK,
            "        "
            f'<li><a class="nav-link" href="/#local">'
            f'<i class="fas fa-map-marker-alt"></i> '
            f"<span>{cta}</span></a></li>\n" + NAV_MARK,
            1,
        )
    if 'href="/#local"' not in html:
        raise RuntimeError("header missing /#local")
    if "nav-menu" not in html or 'href="/spreadsheet/"' not in html:
        raise RuntimeError("header chrome missing")
    if len(html.encode("utf-8")) < HEADER_MIN:
        raise RuntimeError(f"header collapsed to {len(html.encode('utf-8'))} B")
    return html


def patch_php_hub(html: str) -> str:
    key, spec = "com", HUBS["com"]
    facts = _facts(spec)
    block = _local_block(key, spec)
    loc = spec["loc"]
    if 'class="skip"' not in html:
        html = html.replace(
            "<body>",
            "<body>\n" + skip_link(skip_label(loc)).rstrip(),
            1,
        )
    if 'id="main"' not in html:
        html = html.replace(
            '<main class="w2c-main">',
            '<main class="w2c-main" id="main">',
            1,
        )
    if "#local{scroll-margin-top" not in html:
        html = html.replace(
            "</head>",
            "<style>" + SKIP_CSS + HUB_LOCAL_CSS + "</style>\n</head>",
            1,
        )
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
        html = html.replace(
            HERO_END,
            "  </section>\n" + block + "\n"
            '  <section class="w2c-section w2c-home-cats">',
            1,
        )
    err: list[str] = []
    _check_local_section(html, facts, err)
    title_m = re.search(r"<title>(.*?)</title>", html, flags=re.S)
    title = title_m.group(1) if title_m else ""
    if re.search(r"invite\s*(code)?\s*[A-Z0-9]{5,}", title, flags=re.I):
        err.append("invite in title")
    if INVITE in html:
        err.append("sentinel invite leaked onto homepage")
    if re.search(r"58 l[ií]neas para Espa|23[,.]81\s*USD|how to under-?declar", html, flags=re.I):
        err.append("spain snapshot / coaching")
    if "not a customs territory" not in html:
        err.append("hub missing fingerprint")
    if len(html.encode("utf-8")) < TEMPLATE_MIN:
        err.append(f"template collapsed to {len(html.encode('utf-8'))} bytes")
    for marker in TEMPLATE_CHROME:
        if marker not in html:
            err.append(f"hub chrome missing {marker}")
    if AGENT_FAQ_OLD in html:
        err.append("purchasing-agent FAQ leaked")
    if err:
        raise RuntimeError(f"{key}: {'; '.join(err)}")
    return html


def generate() -> None:
    assert_dest_packs_unique()
    spec = HUBS["com"]
    src = OUT / spec["host"] / "live-base" / "index.htm"
    hdr_src = OUT / spec["host"] / "live-base" / "header.htm"
    php_html = patch_php_hub(src.read_text(encoding="utf-8"))
    hdr_html = patch_header(hdr_src.read_text(encoding="utf-8"), spec)
    dest = OUT / spec["host"] / "overlay" / "index.htm"
    hdr_dest = OUT / spec["host"] / "overlay" / "header.htm"
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(php_html, encoding="utf-8")
    hdr_dest.write_text(hdr_html, encoding="utf-8")
    inner = re.search(r'<section class="sg-sec" id="local".*?</section>', php_html, flags=re.S)
    blob = inner.group(0) if inner else ""
    fp = dest_local_pack(spec.get("dest"))["fingerprint"]
    if fp not in blob:
        raise SystemExit(f"missing fingerprint {fp!r}")
    for alien in ALIENS:
        if alien in blob:
            raise SystemExit(f"leaked dest {alien!r}")
    if EST not in blob:
        raise SystemExit("missing estimator")
    if "not a customs territory" not in blob:
        raise SystemExit("hub missing customs-territory line")
    if INVITE in blob:
        raise SystemExit("#local still has invite token")
    if re.search(r"90\s*dagen|90\s*days|60\s*-?\s*day", blob, flags=re.I):
        raise SystemExit("invented free-day count in #local")
    if AGENT_FAQ_OLD in php_html:
        raise SystemExit("purchasing-agent FAQ still present")
    print("hub", spec["host"], "template", len(php_html.encode("utf-8")), "header", len(hdr_html.encode("utf-8")))
    print("generate ok 1 desks")


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
    bak = f"/www/backup/w2clinks-desks-{stamp}"
    _run(client, f"mkdir -p '{bak}'")
    sftp = client.open_sftp()
    spec = HUBS["com"]
    for name, min_b, chrome in (
        ("index.htm", TEMPLATE_MIN, TEMPLATE_CHROME),
        ("header.htm", HEADER_MIN, ("nav-menu", 'href="/spreadsheet/"', 'href="/#local"')),
    ):
        local = OUT / spec["host"] / "overlay" / name
        remote = f"/www/wwwroot/{spec['host']}/template/pc/{name}"
        raw = local.read_text(encoding="utf-8")
        if name == "index.htm":
            if 'id="local"' not in raw or "not a customs territory" not in raw:
                raise SystemExit(f"refusing to PUT {name} without hub #local")
        if INVITE in raw:
            raise SystemExit(f"refusing to PUT {name} with invite sentinel")
        if local.stat().st_size < min_b:
            raise SystemExit(f"refusing to PUT collapsed {name} {local.stat().st_size} B")
        for marker in chrome:
            if marker not in raw:
                raise SystemExit(f"refusing to PUT {name} missing chrome {marker}")
        live = _run(client, f"wc -c < '{remote}'")
        try:
            live_n = int(live.strip().split()[0])
        except ValueError:
            live_n = 0
        if live_n and live_n < min_b - 500:
            raise SystemExit(f"refusing to PUT over unexpected thin {name} {live_n} B")
        _run(client, f"cp -a '{remote}' '{bak}/{name}'")
        sftp.put(str(local), remote)
        print("PUT", remote, "bytes", local.stat().st_size)

    # Never overwrite PHP bootstrap or a disk line-card.
    php_n = _run(client, f"wc -c < /www/wwwroot/{HOST}/index.php")
    print("keep unique PHP bootstrap", php_n)
    html_exists = _run(client, f"test -f /www/wwwroot/{HOST}/index.html && echo yes || echo no")
    print("index.html on disk", html_exists, "(not overwritten)")

    vhost = f"/www/server/panel/vhost/nginx/{HOST}.conf"
    _run(client, f"cp -a '{vhost}' '{bak}/{HOST}.conf'")
    vnow = _run(client, f"cat '{vhost}'")
    if "https://w2clinks.com$request_uri" not in vnow:
        raise SystemExit("www missing 301 to apex $request_uri")
    if "return 410" in vnow:
        raise SystemExit("hub nginx has return 410")
    if "index index.php" not in vnow:
        raise SystemExit("hub nginx missing PHP index")

    for extra in EXTRAS_W2CREP:
        extra_conf = f"/www/server/panel/vhost/nginx/{extra}.conf"
        eraw = _run(client, f"cat '{extra_conf}'")
        if f"https://{W2CREP}$request_uri" not in eraw:
            raise SystemExit(f"{extra} missing 301 $request_uri into {W2CREP}")
        print("keep extra 301", extra, "->", W2CREP)

    print(
        _run(
            client,
            "rm -rf /www/wwwroot/w2clinks.com/data/runtime/cache/* "
            "/www/wwwroot/w2clinks.com/data/runtime/temp/* ; echo cache-cleared",
        )
    )
    nginx_t = _run(client, "nginx -t 2>&1")
    print(nginx_t)
    if "successful" not in nginx_t.lower() and "ok" not in nginx_t.lower():
        raise SystemExit("nginx -t failed; not reloading")
    print(_run(client, "nginx -s reload 2>&1"))
    sftp.close()
    print("backup", bak)
    print("unique PHP CMS kept; extras still 301 into w2crep; no 5KB overlay")
    client.close()


def live_check() -> None:
    import urllib.request

    class NR(urllib.request.HTTPRedirectHandler):
        def redirect_request(self, req, fp, code, msg, headers, newurl):
            return None

    def fetch(url, follow=True):
        req = urllib.request.Request(
            url,
            headers={
                "User-Agent": "w2clinks-desk-check/1.0",
                "Cache-Control": "no-cache",
                "Pragma": "no-cache",
            },
        )
        opener = urllib.request.build_opener() if follow else urllib.request.build_opener(NR)
        try:
            with opener.open(req, timeout=25) as resp:
                return resp.status, resp.geturl(), resp.headers.get("Location") or "", resp.read()
        except urllib.error.HTTPError as e:
            return e.code, url, e.headers.get("Location") or "", e.read() if e.fp else b""
        except Exception as e:
            return 0, url, "", str(e).encode()

    fail = 0
    url = f"https://{PUBLIC}/"
    code, _, loc, body = fetch(url, follow=True)
    html = body.decode("utf-8", "replace")
    title_m = re.search(r"<title>(.*?)</title>", html, flags=re.S)
    title = title_m.group(1) if title_m else ""
    inner_m = re.search(r'<section class="sg-sec" id="local".*?</section>', html, flags=re.S)
    inner = inner_m.group(0) if inner_m else ""
    fp = "not a customs territory"
    print(f"com {code} bytes={len(body)} local={bool(inner)} fp={fp in html}")
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
        if re.search(r"invite\s*(code)?\s*[A-Z0-9]{5,}", title, flags=re.I):
            print("  FAIL invite in title")
            fail += 1
        if re.search(r"58 l[ií]neas para Espa|23[,.]81\s*USD|how to under-?declar", html, flags=re.I):
            print("  FAIL snapshot/coaching")
            fail += 1
        if re.search(r"90\s*dagen|90\s*days|60\s*-?\s*day", inner, flags=re.I):
            print("  FAIL invented free-day copy")
            fail += 1
        if EST not in inner:
            print("  FAIL estimator")
            fail += 1
        if AGENT_FAQ_OLD in html:
            print("  FAIL purchasing-agent FAQ")
            fail += 1
        if len(body) < LIVE_HUB_MIN:
            print("  FAIL hub collapsed", len(body))
            fail += 1
        for marker in LIVE_CHROME:
            if marker not in html:
                print("  FAIL hub chrome gone", marker)
                fail += 1

    code, _, loc, _ = fetch(url, follow=False)
    if code in (301, 302, 303, 307, 308):
        print("FAIL hub 301", loc)
        fail += 1
    else:
        print("indep hub", code)

    code, _, loc, _ = fetch(f"https://www.{PUBLIC}/", follow=False)
    if code in (301, 302, 303, 307, 308) and PUBLIC in (loc or "") and "w2crep" not in (loc or "").lower():
        print("www 301 apex", code, loc)
    else:
        print("FAIL www", code, loc)
        fail += 1

    code, _, loc, body = fetch(f"https://{W2CREP}/", follow=False)
    if code in (301, 302, 303, 307, 308):
        print("FAIL w2crep 301", loc)
        fail += 1
    elif code != 200 or len(body) < 40000:
        print("FAIL w2crep hub", code, len(body))
        fail += 1
    else:
        print("indep w2crep", code, len(body))

    for extra in EXTRAS_W2CREP:
        code, _, loc, _ = fetch(f"https://{extra}/", follow=False)
        if code in (301, 302, 303, 307, 308) and W2CREP in (loc or "") and "w2clinks" not in (loc or "").lower():
            print("extra apex 301 w2crep", extra, code, loc)
        else:
            print("FAIL extra", extra, code, loc)
            fail += 1
        deep = "/w2crep-spreadsheet/"
        code, _, loc, _ = fetch(f"https://{extra}{deep}", follow=False)
        if code in (301, 302, 303, 307, 308) and W2CREP in (loc or "") and deep.rstrip("/") in (loc or ""):
            print("extra deep $request_uri", extra, code, loc)
        else:
            print("FAIL extra deep", extra, code, loc)
            fail += 1

    code, _, loc, body = fetch("https://repsicon.com/", follow=False)
    if code == 410:
        print("FAIL repsicon 410 (user: do not process)")
        fail += 1
    else:
        print("skip repsicon", code, len(body))

    for path, min_bytes in RANKED_CMS:
        inner_url = f"https://{PUBLIC}{path}"
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
