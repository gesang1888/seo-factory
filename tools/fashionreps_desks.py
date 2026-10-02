#!/usr/bin/env python3
"""FashionReps desks: surgical #local on the EyouCMS .com hub.

Gates:
1. Hub #local has the HUB fingerprint, no dest-country fingerprints.
2. Estimator country ≠ TLD; .com must say it is not a customs territory.
3. Titles have no invite code; body has no customs coaching / 58-line snapshot.
4. fashionrepsspreadsheet.com stays independent (www already 301s apex).
   fashionrepsfind.com is a same-agent extra .com — 301 $request_uri after target #local.
   Not two country dests (gate 4). Mixed DEU/ITA/ESP/USA → hub.
5. GSC pretty paths (/shoes381/, /bags/, …) 301 onto live yupoo-* categories (not 404).
6. Hub remains EyouCMS (template/pc/index.htm ~84KB, rendered ~111KB). Do not PUT a
   5KB Georgia skin over PHP. Official FashionReps.com is dead; do not invent storage days.

fashionrepsfind.com DB has no ey_* tables — do not restore empty PHP; keep catch-all 301.
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
EST = "https://www.kakobuy.com/estimate"
OFFICIAL = "https://www.kakobuy.com/"
HELP = "https://www.kakobuy.com/"
DATE = "2 Oct 2026"
HUB_MIN = 80000
LIVE_HUB_MIN = 100000
STORAGE = (
    "Warehouse days follow the purchasing agent you actually checkout with "
    f"(agents already linked on this CMS, e.g. {HELP}); confirm that live copy "
    "the morning you ship. This desk does not invent a free-day count."
)

HUBS = {
    "php": {
        "host": "fashionrepsspreadsheet.com",
        "lang": "en",
        "loc": "en",
        "dest": None,
        "dest_label": "a country in the estimator",
        "ccy": "USD",
        "title": None,  # keep CMS title (102 GSC home clicks, no invite)
        "h1": None,
        "keep": [
            ("/yupoo-sneakers/", "Sneakers"),
            ("/yupoo-hoodie/", "Hoodies"),
            ("/yupoo-bag/", "Bags"),
            ("/#faq", "FAQ"),
            ("/#how-it-works", "How to buy"),
        ],
    },
}

EST_NOTE = {
    "php": (
        "This .com hub is not a customs territory and not a checkout. "
        "Pick the real ship-to country in the freight form of the agent you "
        "actually pay (Kakobuy estimate is one live form already linked here), "
        "not this hostname, not “EU” as one country."
    ),
}

STORE_NOTE = {
    "en": (
        "Warehouse: follow the agent you checkout with; confirm that live copy "
        "the morning you ship. Do not invent a free-day count on this hub."
    ),
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

GSC_ALIASES = (
    ("/shoes381/", "/yupoo-sneakers/"),
    ("/bags/", "/yupoo-bag/"),
    ("/jersey/", "/yupoo-jersey/"),
    ("/pants-shorts/", "/yupoo-shorts/"),
    ("/hoodies-sweaters/", "/yupoo-hoodie/"),
    ("/t-shirts/", "/yupoo-t-shirt/"),
    ("/jackets839/", "/yupoo-jacket/"),
)

HERO_MARKER = "        </section>\n\n        <!-- Hot Deals Section -->"
FAQ_NAV = '                    <li><a href="#faq" class="nav-item">FAQ</a></li>'


def _facts(spec: dict) -> dict:
    return {
        "agent": "FashionReps",
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


def patch_php_hub(html: str) -> str:
    key, spec = "php", HUBS["php"]
    facts = _facts(spec)
    block = _local_block(key, spec)
    html = _strip_invite_title(html, spec.get("title"))
    if 'class="skip"' not in html:
        html = html.replace("<body>", "<body>\n" + skip_link(skip_label(spec["loc"])).rstrip(), 1)
    if 'href="#local"' not in html:
        if FAQ_NAV not in html:
            raise RuntimeError("php hub FAQ nav missing")
        html = html.replace(
            FAQ_NAV,
            FAQ_NAV + "\n                    "
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
        if HERO_MARKER not in html:
            raise RuntimeError("php hub hero marker missing")
        html = html.replace(HERO_MARKER, "        </section>\n" + block + "\n\n        <!-- Hot Deals Section -->", 1)
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
    php_src = OUT / "fashionrepsspreadsheet.com" / "live-base" / "index.htm"
    php_html = patch_php_hub(php_src.read_text(encoding="utf-8"))
    php_dest = OUT / "fashionrepsspreadsheet.com" / "overlay" / "index.htm"
    php_dest.parent.mkdir(parents=True, exist_ok=True)
    php_dest.write_text(php_html, encoding="utf-8")
    inner_m = re.search(r'<section class="sg-sec" id="local".*?</section>', php_html, flags=re.S)
    inner = inner_m.group(0) if inner_m else ""
    fp = dest_local_pack(None)["fingerprint"]
    if fp not in inner:
        raise SystemExit(f"php missing fingerprint {fp!r}")
    for alien in ALIENS:
        if alien in inner:
            raise SystemExit(f"php leaked dest {alien!r}")
    if EST not in inner:
        raise SystemExit("php missing estimator")
    if "not a customs territory" not in inner:
        raise SystemExit("php hub missing customs-territory line")
    print("hub php fashionrepsspreadsheet.com bytes", len(php_html))
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


def _alias_conf() -> str:
    lines = [
        "# GSC pretty paths (shoes381/bags/…) → live EyouCMS dirnames. Do not 404.",
        "# Added 2026-10-02 desks. Does not duplicate gsc-seo.conf /shoes /jackets.",
    ]
    for src, dst in GSC_ALIASES:
        bare = src.rstrip("/")
        lines.append(f"location = {bare} {{ return 301 {dst}; }}")
        lines.append(f"location = {src} {{ return 301 {dst}; }}")
    lines.append(
        "location ~ ^/bags/(wd_[0-9]+)(?:_[0-9]+)?\\.html$ { return 301 /yupoo-bag/$1.html; }"
    )
    lines.append(
        "location ~ ^/pants-shorts/(wd_[0-9]+)(?:_[0-9]+)?\\.html$ { return 301 /yupoo-shorts/$1.html; }"
    )
    lines.append(
        "location ~ ^/shoes381/(wd_[0-9]+)(?:_[0-9]+)?\\.html$ { return 301 /yupoo-sneakers/$1.html; }"
    )
    lines.append("")
    return "\n".join(lines)


def put() -> None:
    generate()
    client = _connect()
    stamp = time.strftime("%Y%m%d-%H%M%S")
    bak = f"/www/backup/fashionreps-desks-{stamp}"
    _run(client, f"mkdir -p '{bak}'")
    sftp = client.open_sftp()
    php_local = OUT / "fashionrepsspreadsheet.com" / "overlay" / "index.htm"
    php_remote = "/www/wwwroot/fashionrepsspreadsheet.com/template/pc/index.htm"
    raw = php_local.read_text(encoding="utf-8")
    if 'id="local"' not in raw or "not a customs territory" not in raw:
        raise SystemExit("refusing to PUT php hub without #local fingerprint")
    if len(raw) < HUB_MIN:
        raise SystemExit(f"refusing to PUT collapsed php hub {len(raw)}")
    if 'class="hero"' not in raw or 'id="faq"' not in raw:
        raise SystemExit("refusing to PUT php hub missing CMS chrome")
    _run(client, f"cp -a '{php_remote}' '{bak}/fashionrepsspreadsheet.com.template-pc-index.htm'")
    sftp.put(str(php_local), php_remote)
    print("PUT", php_remote, "bytes", php_local.stat().st_size)
    print(
        _run(
            client,
            "rm -rf /www/wwwroot/fashionrepsspreadsheet.com/data/runtime/cache/* "
            "/www/wwwroot/fashionrepsspreadsheet.com/data/runtime/temp/* ; echo cache-cleared",
        )
    )

    ext = "/www/server/panel/vhost/nginx/extension/fashionrepsspreadsheet.com"
    alias_path = f"{ext}/gsc-desk-aliases.conf"
    _run(client, f"mkdir -p '{bak}/nginx'")
    _run(client, f"cp -a '{ext}/.' '{bak}/nginx/'")
    with sftp.file(alias_path, "w") as fh:
        fh.write(_alias_conf())
    print("wrote", alias_path)

    nginx_t = _run(client, "nginx -t 2>&1")
    print(nginx_t)
    if "successful" not in nginx_t.lower() and "ok" not in nginx_t.lower():
        raise SystemExit("nginx -t failed; not reloading")
    print(_run(client, "nginx -s reload 2>&1"))
    sftp.close()
    print("backup", bak)
    print("PHP hub kept; find.com catch-all 301 unchanged; no 5KB overwrite")
    client.close()


def live_check() -> None:
    import urllib.request

    class NR(urllib.request.HTTPRedirectHandler):
        def redirect_request(self, req, fp, code, msg, headers, newurl):
            return None

    def fetch(url, follow=True):
        req = urllib.request.Request(url, headers={"User-Agent": "fashionreps-desk-check/1.0"})
        opener = urllib.request.build_opener() if follow else urllib.request.build_opener(NR)
        try:
            with opener.open(req, timeout=25) as resp:
                return resp.status, resp.geturl(), resp.headers.get("Location") or "", resp.read()
        except urllib.error.HTTPError as e:
            return e.code, url, e.headers.get("Location") or "", e.read() if e.fp else b""

    fail = 0
    url = "https://fashionrepsspreadsheet.com/"
    code, _, loc, body = fetch(url, follow=True)
    html = body.decode("utf-8", "replace")
    title_m = re.search(r"<title>(.*?)</title>", html, flags=re.S)
    title = title_m.group(1) if title_m else ""
    inner_m = re.search(r'<section class="sg-sec" id="local".*?</section>', html, flags=re.S)
    inner = inner_m.group(0) if inner_m else ""
    fp = "not a customs territory"
    print(f"php {code} bytes={len(body)} local={bool(inner)} fp={fp in html}")
    if code != 200 or not inner or fp not in inner:
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
        if EST not in inner:
            print("  FAIL estimator url missing")
            fail += 1
        if len(body) < LIVE_HUB_MIN:
            print("  FAIL php hub collapsed", len(body))
            fail += 1
        if 'class="hero"' not in html or 'id="faq"' not in html:
            print("  FAIL php hub chrome")
            fail += 1
        if "网站暂时关闭" in html:
            print("  FAIL php hub still closed")
            fail += 1

    for src, dst in GSC_ALIASES:
        u = f"https://fashionrepsspreadsheet.com{src}"
        code, _, loc, _ = fetch(u, follow=False)
        if code not in (301, 302, 303, 307, 308) or dst.rstrip("/") not in (loc or ""):
            print("FAIL alias 301", src, code, loc)
            fail += 1
            continue
        code, final, _, body = fetch(u, follow=True)
        if code == 404 or len(body) < 8000:
            print("FAIL alias dest", src, "->", final, code, len(body))
            fail += 1
        else:
            print("alias", src, "->", final, code, len(body))

    for path in ("/yupoo-sneakers/", "/yupoo-bag/", "/yupoo-hoodie/"):
        u = f"https://fashionrepsspreadsheet.com{path}"
        code, final, _, body = fetch(u, follow=True)
        if code == 404 or len(body) < 20000:
            print("FAIL cat", path, code, len(body))
            fail += 1
        else:
            print("cat", path, code, len(body))

    code, _, loc, _ = fetch("https://fashionrepsfind.com/", follow=False)
    if code not in (301, 302, 303, 307, 308) or "fashionrepsspreadsheet.com" not in (loc or ""):
        print("FAIL find 301", code, loc)
        fail += 1
    else:
        print("twin 301", "https://fashionrepsfind.com/", "->", loc)

    code, _, loc, _ = fetch("https://fashionrepsfind.com/shoes381/", follow=False)
    if code not in (301, 302, 303, 307, 308) or "shoes381" not in (loc or ""):
        print("FAIL find deep 301", code, loc)
        fail += 1
    else:
        print("twin deep 301", loc)
        code, final, _, body = fetch("https://fashionrepsfind.com/shoes381/", follow=True)
        if code == 404 or len(body) < 8000:
            print("FAIL find deep dest 404", code, len(body), final)
            fail += 1
        else:
            print("twin deep dest", code, len(body), final)

    code, _, loc, _ = fetch("https://fashionrepsspreadsheet.com/", follow=False)
    if code in (301, 302, 303, 307, 308) and loc:
        print("FAIL 301 hub", loc)
        fail += 1
    else:
        print("indep https://fashionrepsspreadsheet.com/", code)

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
