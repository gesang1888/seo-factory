#!/usr/bin/env python3
"""LoLoBuy desks: dest-unique #local on two unique .com hubs; restore ranked CMS.

Gates:
1. Each hub #local has the HUB fingerprint, no dest-country fingerprints.
2. Estimator country ≠ TLD; .com must say it is not a customs territory.
3. Titles have no invite token 2pgzy; body has no customs coaching / 58-line snapshot.
   Coupon stacking stays on /guides/coupons/ (not the homepage title).
4. Two unique same-agent .com hubs stay independent (no 301). QC triage ≠ parcel SOP.
   www already 301s apex. Not two country dests.
5. No same-country extra to collapse: unique SOP home (6 clk) must not 301 onto QC home.
   Ranked unique inners must 200 (not 301 /spreadsheet/ onto /). Deep paths must not 404.
6. Georgia homes (~6.5KB) get #local. Do not PUT a 5KB dest overlay over unique 15–21KB
   guides. Official Help is a 200 SPA; do not invent a free-day count.

ia-collapse.conf 301s /spreadsheet/ (16KB unique) onto home and noindexes ranked
brand/category URLs (GSC clicks). Disable that collapse. Keep slash aliases.
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
EST = "https://www.lolobuy.com/estimation"
OFFICIAL = "https://www.lolobuy.com/"
HELP = "https://www.lolobuy.com/help"
DATE = "2 Oct 2026"
INVITE = "2pgzy"
HUB_MIN = 6000
LIVE_HUB_MIN = 7000
STORAGE = (
    "Official LoLoBuy Help is the live SPA "
    f"({HELP}); confirm that live copy the morning you ship. "
    "This desk does not invent a free-day count."
)

HUBS = {
    "qc": {
        "host": "bestlolobuyspreadsheet.com",
        "lang": "en",
        "loc": "en",
        "dest": None,
        "dest_label": "a country in the estimator",
        "ccy": "USD",
        "title": None,
        "h1": None,
        "chrome": ("layout-runway", "reject tool", "QC"),
        "keep": [
            ("/guides/coupons/", "Coupons (ranked)"),
            ("/guides/shipping/", "Shipping (ranked)"),
            ("/guides/is-lolobuy-legit/", "Legit"),
            ("/spreadsheet/", "Spreadsheet"),
            ("/guides/qc/", "QC guide"),
        ],
    },
    "sop": {
        "host": "lolospreadsheet.com",
        "lang": "en",
        "loc": "en",
        "dest": None,
        "dest_label": "a country in the estimator",
        "ccy": "USD",
        "title": None,
        "h1": None,
        "chrome": ("layout-opsboard", "operations desk", "parcel SOP"),
        "keep": [
            ("/guides/", "Guides (ranked)"),
            ("/guides/is-lolobuy-legit/", "Legit"),
            ("/spreadsheet/", "Spreadsheet"),
            ("/brand/prada/", "Prada"),
        ],
    },
}

EST_NOTE = {
    "qc": (
        "This .com hub is not a customs territory. QC-triage copy does not make "
        ".com a dest country. Pick the real ship-to country in the official estimator, "
        "not this hostname, not “EU” as one country. lolospreadsheet.com stays the SOP hub."
    ),
    "sop": (
        "This .com hub is not a customs territory. Parcel-SOP copy does not make "
        ".com a dest country. Pick the real ship-to country in the official estimator, "
        "not this hostname, not “EU” as one country. bestlolobuyspreadsheet.com stays the QC hub."
    ),
}

STORE_NOTE = {
    "en": (
        "Warehouse: official LoLoBuy Help is an SPA. Confirm that live copy the "
        "morning you ship. Do not invent a free-day count on this hub."
    ),
}

TRAIL = {"en": ("Live money is in", "this HTML is not checkout.")}

HUB_LOCAL_CSS = (
    ".sg-sec#local{margin:1.25rem 0 0}"
    ".sg-sec#local h2{margin-top:0}"
    ".ssub{color:var(--muted,#a1a1aa);font-size:.95rem;margin:0 0 12px}"
    ".local-steps{margin:12px 0 0;padding:0;list-style:none;display:grid;gap:12px}"
    ".local-steps li{border:1px solid color-mix(in srgb, var(--ink,#fafafa) 16%, transparent);border-radius:12px;padding:14px 16px;background:var(--card,#1c1c1c)}"
    ".local-steps strong{display:block;margin:0 0 6px;font-size:15px}"
    ".local-steps span{display:block;color:var(--muted,#a1a1aa);line-height:1.7;font-size:15px}"
    ".local-src{font-size:14px;color:var(--muted,#a1a1aa);line-height:1.7;margin:14px 0 0}"
    "#local{scroll-margin-top:96px}"
)

ALIENS = ("1010 Wien", "Packstation", "form A1A 1A1", "Poste Italiane", "00-001 Warszawa")

TITLE_SCRUB = {
    "bestlolobuyspreadsheet.com": (
        "guides/coupons/index.html",
        "coupons/index.html",
    ),
    "lolospreadsheet.com": (
        "guides/coupons/index.html",
        "coupons/index.html",
    ),
}

RANKED_CMS = {
    "bestlolobuyspreadsheet.com": (
        ("/guides/coupons/", 15000),
        ("/guides/shipping/", 12000),
        ("/guides/is-lolobuy-legit/", 12000),
        ("/guides/qc/", 12000),
        ("/guides/how-to-use/", 12000),
        ("/spreadsheet/", 12000),
        ("/guides/", 12000),
        ("/brand/nike/", 8000),
        ("/brand/louis-vuitton/", 8000),
        ("/coupons/", 3000),
        ("/shipping/", 3000),
        ("/start/", 3000),
    ),
    "lolospreadsheet.com": (
        ("/guides/", 8000),
        ("/guides/is-lolobuy-legit/", 8000),
        ("/spreadsheet/", 8000),
        ("/brand/prada/", 8000),
        ("/guides/how-to-use/", 8000),
        ("/guides/qc/", 8000),
        ("/guides/coupons/", 3000),
        ("/start/", 3000),
    ),
}

KEEP_REDIRECTS = {
    "bestlolobuyspreadsheet.com": (
        ("/guides/coupons", "/guides/coupons/"),
        ("/guides/shipping", "/guides/shipping/"),
        ("/spreadsheet", "/spreadsheet/"),
        ("/guides/is-lolobuy-legit", "/guides/is-lolobuy-legit/"),
    ),
    "lolospreadsheet.com": (
        ("/guides/coupons", "/guides/coupons/"),
        ("/guides/shipping", "/guides/shipping/"),
        ("/spreadsheet", "/spreadsheet/"),
        ("/guides", "/guides/"),
    ),
}

HERO_END = "</section>\n<section class=\"grid\">"
INVITE_REGISTER = "https://www.lolobuy.com/index?inviteCode=2pgzy"


def _facts(spec: dict) -> dict:
    return {
        "agent": "LoLoBuy",
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
        s = re.sub(r"(?i)\s*[—\-–:,]*\s*invite\b", "", s)
        s = re.sub(r"\s{2,}", " ", s).strip(" —–-,;&")
        return s

    def title_sub(m):
        if new_title:
            return f"<title>{escape(new_title)}</title>"
        return f"<title>{scrub(m.group(1))}</title>"

    html = re.sub(r"<title>(.*?)</title>", title_sub, html, count=1, flags=re.S)
    return html


def _scrub_token_from_home(html: str, host: str) -> str:
    html = html.replace(
        f'<p class="note">LoLoBuy · {host} · invite code 2pgzy</p>',
        f'<p class="note">LoLoBuy · {host} · not a customs territory</p>',
    )
    html = html.replace('<a href="/coupons/">2pgzy</a>', '<a href="/guides/coupons/">Coupons</a>')
    html = html.replace(
        "Invite 2pgzy is the LoLoBuy register code. It does not grade QC for you.",
        "Coupon stacking stays on /guides/coupons/. This homepage does not print a token.",
    )
    html = html.replace(INVITE_REGISTER, OFFICIAL)
    html = html.replace("Attach 2pgzy on LoLoBuy", "Open LoLoBuy")
    html = html.replace(
        '<h3>What is 2pgzy?</h3><p>LoLoBuy inviteCode on lolobuy.com register.</p>',
        "<h3>Where are coupons?</h3><p>Coupon stacking stays on /guides/coupons/. This homepage does not print a token.</p>",
    )
    html = html.replace(
        '"name": "What is 2pgzy?"',
        '"name": "Where are coupons?"',
    )
    html = html.replace(
        '"text": "LoLoBuy inviteCode on lolobuy.com register."',
        '"text": "Coupon stacking stays on /guides/coupons/. This homepage does not print a token."',
    )
    html = html.replace(INVITE, "")
    html = html.replace("inviteCode=", "")
    return html


def patch_static(html: str, key: str, spec: dict) -> str:
    facts = _facts(spec)
    block = _local_block(key, spec)
    loc = spec["loc"]
    html = _scrub_token_from_home(html, spec["host"])
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
        html = html.replace("<main>", '<main id="main">', 1)
    if 'href="#local"' not in html:
        if "</nav>" not in html:
            raise RuntimeError(f"{key} nav missing")
        html = html.replace(
            "</nav>",
            f'<a href="#local">{escape(local_cta(facts))}</a>\n'
            f'<a href="/guides/coupons/">Coupons</a></nav>',
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
            raise RuntimeError(f"{key} hero marker missing")
        html = html.replace(HERO_END, "</section>\n" + block + "\n<section class=\"grid\">", 1)
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
    for marker in spec.get("chrome") or ():
        if marker not in html:
            err.append(f"hub chrome missing {marker}")
    if err:
        raise RuntimeError(f"{key}: {'; '.join(err)}")
    return html


SKIP_UNIQUE_CMS = frozenset({"bestlolobuyspreadsheet.com", "lolospreadsheet.com"})


def generate() -> None:
    assert_dest_packs_unique()
    blobs = {}
    specs = {**HUBS}
    for key, spec in specs.items():
        if spec["host"] in SKIP_UNIQUE_CMS:
            print("SKIP unique CMS", spec["host"])
            continue
        src = OUT / spec["host"] / "live-base" / "index.html"
        html = patch_static(src.read_text(encoding="utf-8"), key, spec)
        dest = OUT / spec["host"] / "overlay" / "index.html"
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(html, encoding="utf-8")
        inner = re.search(r'<section class="sg-sec" id="local".*?</section>', html, flags=re.S)
        blobs[key] = inner.group(0) if inner else ""
        print("hub", key, spec["host"], "bytes", len(html.encode("utf-8")))
    if not blobs:
        print("generate skipped all unique CMS hubs")
        return
    fps = {k: dest_local_pack(specs[k].get("dest"))["fingerprint"] for k in blobs}
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
    bak = f"/www/backup/lolobuy-desks-{stamp}"
    _run(client, f"mkdir -p '{bak}'")
    sftp = client.open_sftp()
    collapse = (
        "# disabled 2026-10-02 desks: unique ranked CMS must serve at GSC URLs.\n"
        "# Thin /coupons/ /shipping/ /start/ remain as extra paths, not destinations.\n"
        "# Do not noindex ranked /brand/ /category/ that still take GSC clicks.\n"
        "# gsc-redirects slash aliases kept; /spreadsheet/ must 200 the unique file.\n"
    )
    for spec in HUBS.values():
        if spec["host"] in SKIP_UNIQUE_CMS:
            print("SKIP unique PUT", spec["host"])
            continue
        local = OUT / spec["host"] / "overlay" / "index.html"
        remote = f"/www/wwwroot/{spec['host']}/index.html"
        raw = local.read_text(encoding="utf-8")
        if 'id="local"' not in raw or "not a customs territory" not in raw:
            raise SystemExit(f"refusing to PUT {spec['host']} without hub #local")
        if INVITE in raw:
            raise SystemExit(f"refusing to PUT {spec['host']} with frozen invite token")
        if local.stat().st_size < HUB_MIN:
            raise SystemExit(f"refusing to PUT collapsed hub {local.stat().st_size} B")
        live = _run(client, f"wc -c < '{remote}'")
        try:
            live_n = int(live.strip().split()[0])
        except ValueError:
            live_n = 0
        if live_n > 15000:
            raise SystemExit(f"refusing to PUT over unique CMS home {live_n} B")
        for marker in spec.get("chrome") or ():
            if marker not in raw:
                raise SystemExit(f"refusing to PUT hub missing chrome {marker}")
        _run(client, f"cp -a '{remote}' '{bak}/{spec['host']}.index.html'")
        sftp.put(str(local), remote)
        print("PUT", remote, "bytes", local.stat().st_size)

        ext = f"/www/server/panel/vhost/nginx/extension/{spec['host']}"
        _run(client, f"mkdir -p '{bak}/nginx-{spec['host']}'")
        _run(client, f"cp -a '{ext}/.' '{bak}/nginx-{spec['host']}/'")
        with sftp.file(f"{ext}/ia-collapse.conf", "w") as fh:
            fh.write(collapse)
        print("disabled", f"{ext}/ia-collapse.conf")

        root = f"/www/wwwroot/{spec['host']}"
        for rel in TITLE_SCRUB.get(spec["host"]) or ():
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
                print("title already clean", spec["host"], rel)
                continue
            before = len(inner_html)
            _run(client, f"cp -a '{remote_inner}' '{bak}/{spec['host']}_{rel.replace('/', '_')}'")
            scrubbed = _scrub_title_token(inner_html)
            title_m = re.search(r"<title>(.*?)</title>", scrubbed, flags=re.S)
            title = title_m.group(1) if title_m else ""
            if INVITE in title:
                raise SystemExit(f"title still has invite after scrub: {rel} {title!r}")
            if abs(len(scrubbed) - before) > 400:
                raise SystemExit(f"title scrub changed {rel} too much ({before}->{len(scrubbed)})")
            with sftp.file(remote_inner, "w") as fh:
                fh.write(scrubbed)
            print("scrub title", spec["host"], rel, "title", title)

    nginx_t = _run(client, "nginx -t 2>&1")
    print(nginx_t)
    if "successful" not in nginx_t.lower() and "ok" not in nginx_t.lower():
        raise SystemExit("nginx -t failed; not reloading")
    print(_run(client, "nginx -s reload 2>&1"))
    sftp.close()
    print("backup", bak)
    print("both unique .com hubs kept independent; no 5KB overwrite of 15–21KB guides")
    client.close()


def live_check() -> None:
    import urllib.request

    class NR(urllib.request.HTTPRedirectHandler):
        def redirect_request(self, req, fp, code, msg, headers, newurl):
            return None

    def fetch(url, follow=True):
        req = urllib.request.Request(url, headers={"User-Agent": "lolobuy-desk-check/1.0"})
        opener = urllib.request.build_opener() if follow else urllib.request.build_opener(NR)
        try:
            with opener.open(req, timeout=25) as resp:
                return resp.status, resp.geturl(), resp.headers.get("Location") or "", resp.read()
        except urllib.error.HTTPError as e:
            return e.code, url, e.headers.get("Location") or "", e.read() if e.fp else b""

    fail = 0
    for key, spec in HUBS.items():
        url = f"https://{spec['host']}/"
        code, _, loc, body = fetch(url, follow=True)
        html = body.decode("utf-8", "replace")
        title_m = re.search(r"<title>(.*?)</title>", html, flags=re.S)
        title = title_m.group(1) if title_m else ""
        inner_m = re.search(r'<section class="sg-sec" id="local".*?</section>', html, flags=re.S)
        inner = inner_m.group(0) if inner_m else ""
        fp = "not a customs territory"
        print(f"{key:3} {code} bytes={len(body)} local={bool(inner)} fp={fp in html}")
        if code != 200 or not inner or fp not in inner:
            print("  FAIL status/local/fp")
            fail += 1
            continue
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
        for marker in spec.get("chrome") or ():
            if marker not in html:
                print("  FAIL hub chrome gone", marker)
                fail += 1
        code, _, loc, _ = fetch(url, follow=False)
        if code in (301, 302, 303, 307, 308):
            print("FAIL hub 301", spec["host"], loc)
            fail += 1
        else:
            print("indep hub", spec["host"], code)

        for path, min_bytes in RANKED_CMS[spec["host"]]:
            inner_url = f"https://{spec['host']}{path}"
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
                if path in ("/guides/coupons/", "/coupons/") and (
                    INVITE in title or re.search(r"(?i)[—\-–:,]\s*invite\b", title)
                ):
                    print("FAIL invite in inner title", path, title)
                    fail += 1

        for src, dst in KEEP_REDIRECTS[spec["host"]]:
            inner_url = f"https://{spec['host']}{src}"
            code, _, loc, _ = fetch(inner_url, follow=False)
            if code not in (301, 302, 303, 307, 308) or dst.rstrip("/") not in (loc or ""):
                print("FAIL expected 301", inner_url, code, "->", loc, "want", dst)
                fail += 1
            else:
                print("kept 301", src, "->", loc)

    for a, other in (
        ("https://bestlolobuyspreadsheet.com/", "lolospreadsheet.com"),
        ("https://lolospreadsheet.com/", "bestlolobuyspreadsheet.com"),
    ):
        code, _, loc, _ = fetch(a, follow=False)
        if code in (301, 302, 303, 307, 308) and loc and other in loc:
            print("FAIL twin 301", a, loc)
            fail += 1
        else:
            print("indep twins", a, code)

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
