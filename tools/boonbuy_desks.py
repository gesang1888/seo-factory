#!/usr/bin/env python3
"""BoonBuy .com hub: unique CMS homepage + ranked coupon/legit/shipping inners.

Gates:
1. Homepage is the unique CMS (money title BoonBuy Spreadsheet). Not leftover
   dest #local / “not a customs territory” / products-API dump.
2. Titles have no invite token G8ZWVJI95; body has no customs coaching / 58-line.
   Coupon stacking stays on /boonbuy-coupons/ (not the homepage title).
3. Single public hub — no 301 to a country dest. www already 301s to apex.
4. Ranked unique inners /boonbuy-coupons/ /is-boonbuy-legit/
   /boonbuy-shipping-guide/ must 200. Spreadsheet inners and /coupons/ 301 into
   the canonical money/coupon URLs.
5. Do not leftover-PUT this host (SKIP_UNIQUE in leftover_hub_skins.py).
   Official Help is an SPA — do not invent a free-day count.

boonbuyspreadsheet.com is AWS, not origin — do not 301 it.
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
EST = "https://boonbuy.com/shipping-estimate"
OFFICIAL = "https://boonbuy.com/"
HELP = "https://boonbuy.com/help"
DATE = "2 Oct 2026"
INVITE = "G8ZWVJI95"
STORAGE = (
    "Official BoonBuy Help is an SPA "
    f"({HELP}); confirm that live copy the morning you ship. "
    "This desk does not invent a free-day count."
)

HUBS = {
    "com": {
        "host": "boonspreadsheet.com",
        "lang": "en",
        "loc": "en",
        "dest": None,
        "dest_label": "a country in the estimator",
        "ccy": "USD",
        "title": "BoonBuy Spreadsheet 2026 — QC Finds & Shipping",
        "h1": "The Complete BoonBuy Spreadsheet 2026",
        "keep": [
            ("/boonbuy-coupons/", "Coupons (ranked)"),
            ("/is-boonbuy-legit/", "Legit (ranked)"),
            ("/boonbuy-shipping-guide/", "Shipping guide"),
            ("/boonbuy-invite-code/", "Invite stacking"),
        ],
    },
}

EST_NOTE = {
    "com": "This .com hub is not a customs territory. Pick the real ship-to country in the official shipping-estimate form, not this hostname, not “EU” as one country.",
}

STORE_NOTE = {
    "en": "Warehouse: official BoonBuy Help (SPA); confirm that live copy the morning you ship. Do not invent a free-day count on this hub.",
}

TRAIL = {
    "en": ("Live money is in", "this HTML is not checkout."),
}

DEST_LOCAL_CSS = (
    ".sg-sec#local{margin:1.25rem 0 0}"
    ".sg-sec#local h2{margin-top:0}"
    ".ssub{color:var(--muted,#57534e);font-size:.95rem;margin:0 0 12px}"
)

ALIENS = ("1010 Wien", "Packstation", "form A1A 1A1", "Poste Italiane", "00-001 Warszawa")

TITLE_SCRUB_REL = (
    "boonbuy-coupons/index.html",
    "boonbuy-invite-code/index.html",
    "coupons/index.html",
)

RANKED_CMS = (
    ("/boonbuy-coupons/", 20000),
    ("/is-boonbuy-legit/", 20000),
    ("/boonbuy-shipping-guide/", 20000),
    ("/boonbuy-invite-code/", 8000),
    ("/boonbuy-refund-guide/", 8000),
)

SHEET_CANNIBALS = (
    "/boonbuy-spreadsheet",
    "/boonbuy-spreadsheet/",
    "/boonbuy-spreadsheet-2026",
    "/boonbuy-spreadsheet-2026/",
)

COUPON_CANNIBALS = (
    "/coupons",
    "/coupons/",
    "/boonbuy-coupons",
)

GSC_REDIRECTS = """# 2026-10-08 hub deepen: money query lives on /. Spreadsheet inners cannibalised
# "boonbuy spreadsheet"; coupon duplicates cannibalised "code promo boonbuy".
# Keep ranked CMS at /boonbuy-coupons/ /is-boonbuy-legit/ /boonbuy-shipping-guide/.
location = /boonbuy-spreadsheet { return 301 https://boonspreadsheet.com/; }
location = /boonbuy-spreadsheet/ { return 301 https://boonspreadsheet.com/; }
location = /boonbuy-spreadsheet-2026 { return 301 https://boonspreadsheet.com/; }
location = /boonbuy-spreadsheet-2026/ { return 301 https://boonspreadsheet.com/; }
location = /coupons { return 301 https://boonspreadsheet.com/boonbuy-coupons/; }
location = /coupons/ { return 301 https://boonspreadsheet.com/boonbuy-coupons/; }
location = /boonbuy-coupons { return 301 https://boonspreadsheet.com/boonbuy-coupons/; }
"""

EMAIL = "cnfd85269032661@gmail.com"
MONEY_TITLE = "BoonBuy Spreadsheet"


def _facts(spec: dict) -> dict:
    return {
        "agent": "BoonBuy",
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
        s = re.sub(r"\s*[—\-–:,]*\s*(invite|ref|code|coupon)\s*[A-Z0-9]{5,}", "", s, flags=re.I)
        s = re.sub(re.escape(INVITE), "", s, flags=re.I)
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
    html = html.replace(f"https://boonbuy.com/register?inviteCode={INVITE}", "https://boonbuy.com/")
    html = html.replace(f"?inviteCode={INVITE}", "")
    html = html.replace(f"invite code {INVITE}", "not a customs territory")
    html = html.replace(f"invite {INVITE}", "the coupons article")
    html = html.replace(f"Attach {INVITE} on BoonBuy", "Open BoonBuy, then pick a real country")
    html = html.replace(
        f"Register on BoonBuy itself with {INVITE} if you want the invite attached.",
        "Register on BoonBuy itself. Coupon stacking stays on /boonbuy-coupons/ — this homepage does not print a token.",
    )
    html = html.replace(INVITE, "")
    html = re.sub(r"register\?inviteCode=", "register", html, flags=re.I)
    return html


def patch_static(html: str, key: str, spec: dict) -> str:
    facts = _facts(spec)
    block = _local_block(key, spec)
    loc = spec["loc"]
    html = _scrub_token_from_home(html)
    html = _strip_invite_title(html, spec.get("title"))
    if spec.get("h1"):
        html = re.sub(r"<h1>.*?</h1>", f"<h1>{escape(spec['h1'])}</h1>", html, count=1, flags=re.S)
    html = re.sub(r"impressions on a template", "impressions on this dest desk", html, flags=re.I)
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
            f'    <a href="#local">{escape(local_cta(facts))}</a>\n'
            f'    <a href="/boonbuy-coupons/">Coupons</a>\n'
            f'    <a href="/is-boonbuy-legit/">Legit</a>\n  </nav>',
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
    if re.search(r"invite\s*(code)?\s*[A-Z0-9]{5,}", title, flags=re.I) or INVITE in title:
        err.append("invite in title")
    if INVITE in html:
        err.append("frozen invite token on homepage")
    if 'id="local"' in html or "not a customs territory" in html.lower():
        err.append("leftover dest hub skin")
    if "/api/products/" in html:
        err.append("products API dump")
    if "not Excel" not in html or "Google Sheet" not in html:
        err.append("missing not-excel copy")
    if EMAIL not in html:
        err.append("missing contact email")
    if re.search(r"58 l[ií]neas para Espa|23[,.]81\s*USD|how to under-?declar", html, flags=re.I):
        err.append("spain snapshot / coaching")
    if len(html) < 20000:
        err.append(f"home too small {len(html)}")
    return err


def generate() -> None:
    dest = OUT / "boonspreadsheet.com" / "overlay" / "index.html"
    html = dest.read_text(encoding="utf-8")
    err = _unique_home_errors(html)
    if err:
        raise SystemExit("unique overlay: " + "; ".join(err))
    redir = OUT / "boonspreadsheet.com" / "overlay" / "gsc-redirects.conf"
    if "location = /boonbuy-spreadsheet/" not in redir.read_text(encoding="utf-8"):
        raise SystemExit("missing spreadsheet 301 in overlay gsc-redirects.conf")
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


def _scrub_title_token(html: str) -> str:
    def scrub(s: str) -> str:
        s = re.sub(r"(?i)\s*[—\-–:,]*\s*(invite\s+)?G8ZWVJI95", "", s)
        s = re.sub(r"&amp;\s*Code Promo", " Code Promo", s)
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
    html = re.sub(
        r'(property="og:title" content=")([^"]+)(")',
        lambda m: m.group(1) + scrub(m.group(2)) + m.group(3),
        html,
        count=1,
    )
    return html


def _scrub_coupon_desc(html: str) -> str:
    html = html.replace(
        "Working BoonBuy coupon codes for 2026 plus invite G8ZWVJI95. Code promo for Europe. Register at boonbuy.com.",
        "Working BoonBuy coupon codes for 2026. Code promo for Europe. Register at boonbuy.com.",
    )
    html = html.replace(
        "All working BoonBuy coupon codes for 2026, updated weekly. Use G8ZWVJI95 — ¥1,000 new-user coupons · up to 30% shipping off.",
        "All working BoonBuy coupon codes for 2026, updated weekly. New-user coupons and up to 30% shipping off — confirm in the official drawer.",
    )
    return html


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
    bak = f"/www/backup/boonbuy-hub-deepen-{stamp}"
    _run(client, f"mkdir -p '{bak}'")
    sftp = client.open_sftp()
    spec = HUBS["com"]
    host = spec["host"]
    local = OUT / host / "overlay" / "index.html"
    remote = f"/www/wwwroot/{host}/index.html"
    raw = local.read_text(encoding="utf-8")
    err = _unique_home_errors(raw)
    if err:
        raise SystemExit("refusing PUT: " + "; ".join(err))
    _run(client, f"cp -a '{remote}' '{bak}/{host}.index.html'")
    sftp.put(str(local), remote)
    print("PUT", remote, "bytes", local.stat().st_size)

    ext = f"/www/server/panel/vhost/nginx/extension/{host}"
    _run(client, f"mkdir -p '{bak}/nginx' && cp -a '{ext}/.' '{bak}/nginx/'")
    collapse = (
        "# disabled 2026-10-02 desks: unique ranked CMS must serve at GSC URLs.\n"
        "# Thin /shipping/ /start/ remain as extra paths, not destinations.\n"
        "# /coupons/ now 301s into /boonbuy-coupons/ (gsc-redirects.conf).\n"
    )
    with sftp.file(f"{ext}/ia-collapse.conf", "w") as fh:
        fh.write(collapse)
    print("disabled", f"{ext}/ia-collapse.conf")
    with sftp.file(f"{ext}/gsc-redirects.conf", "w") as fh:
        fh.write(GSC_REDIRECTS)
    print("wrote", f"{ext}/gsc-redirects.conf")

    root = f"/www/wwwroot/{host}"
    coupon = f"{root}/boonbuy-coupons/index.html"
    try:
        with sftp.open(coupon) as fh:
            coupon_html = fh.read().decode("utf-8")
    except FileNotFoundError:
        coupon_html = ""
        print("skip missing coupon")
    if coupon_html:
        _run(client, f"cp -a '{coupon}' '{bak}/boonbuy-coupons_index.html'")
        scrubbed = _scrub_coupon_desc(_scrub_title_token(coupon_html))
        title_m = re.search(r"<title>(.*?)</title>", scrubbed, flags=re.S)
        title = title_m.group(1) if title_m else ""
        if INVITE in title or re.search(r"invite\s*(code)?\s*[A-Z0-9]{5,}", title, flags=re.I):
            raise SystemExit(f"coupon title still has invite: {title!r}")
        desc_m = re.search(r'<meta name="description" content="([^"]*)"', scrubbed)
        desc = desc_m.group(1) if desc_m else ""
        if INVITE in desc:
            raise SystemExit(f"coupon description still has invite: {desc!r}")
        if "BoonBuy Coupons 2026 Code Promo" not in title:
            raise SystemExit(f"refusing to change coupon money title: {title!r}")
        with sftp.file(coupon, "w") as fh:
            fh.write(scrubbed)
        print("scrub coupon meta", "bytes", len(scrubbed))

    for rel in TITLE_SCRUB_REL:
        if rel.startswith("boonbuy-coupons"):
            continue
        remote_inner = f"{root}/{rel}"
        try:
            with sftp.open(remote_inner) as fh:
                inner_html = fh.read().decode("utf-8")
        except FileNotFoundError:
            print("skip missing", remote_inner)
            continue
        title_m = re.search(r"<title>(.*?)</title>", inner_html, flags=re.S)
        title = title_m.group(1) if title_m else ""
        if INVITE not in title:
            print("title already clean", rel)
            continue
        before = len(inner_html)
        _run(client, f"cp -a '{remote_inner}' '{bak}/{rel.replace('/', '_')}'")
        scrubbed = _scrub_title_token(inner_html)
        title_m = re.search(r"<title>(.*?)</title>", scrubbed, flags=re.S)
        title = title_m.group(1) if title_m else ""
        if INVITE in title or re.search(r"invite\s*(code)?\s*[A-Z0-9]{5,}", title, flags=re.I):
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
    client.close()
    _cf_purge(host)


def live_check() -> None:
    import urllib.error
    import urllib.request

    class NR(urllib.request.HTTPRedirectHandler):
        def redirect_request(self, req, fp, code, msg, headers, newurl):
            return None

    def fetch(url, follow=True):
        req = urllib.request.Request(url, headers={"User-Agent": "boonbuy-hub-check/1.0"})
        opener = urllib.request.build_opener() if follow else urllib.request.build_opener(NR)
        try:
            with opener.open(req, timeout=25) as resp:
                return resp.status, resp.geturl(), resp.headers.get("Location") or "", resp.read()
        except urllib.error.HTTPError as e:
            return e.code, url, e.headers.get("Location") or "", e.read() if e.fp else b""

    fail = 0
    code, _, loc, body = fetch("https://boonspreadsheet.com/", follow=True)
    html = body.decode("utf-8", "replace")
    print(f"home {code} bytes={len(body)} loc={loc!r}")
    if code != 200:
        print("  FAIL home status")
        fail += 1
    else:
        for e in _unique_home_errors(html):
            print("  FAIL", e)
            fail += 1

    code, _, loc, _ = fetch("https://www.boonspreadsheet.com/", follow=False)
    if code not in (301, 302, 303, 307, 308) or "boonspreadsheet.com" not in (loc or "") or "www." in (loc or "").split("://", 1)[-1][:40]:
        # www must 301 to apex
        if "www.boonspreadsheet.com" in (loc or ""):
            print("FAIL www still on www", code, loc)
            fail += 1
        elif code not in (301, 302, 303, 307, 308):
            print("FAIL www not 301", code, loc)
            fail += 1
        else:
            print("www", code, loc)
    else:
        print("www", code, loc)

    for path in SHEET_CANNIBALS:
        url = f"https://boonspreadsheet.com{path}"
        code, _, loc, _ = fetch(url, follow=False)
        if code not in (301, 302, 303, 307, 308) or not loc or not loc.rstrip("/").endswith("boonspreadsheet.com"):
            print("FAIL 301 spreadsheet", url, code, loc)
            fail += 1
        else:
            print("301 sheet", path, "->", loc)

    for path in COUPON_CANNIBALS:
        url = f"https://boonspreadsheet.com{path}"
        code, _, loc, _ = fetch(url, follow=False)
        if code not in (301, 302, 303, 307, 308) or "/boonbuy-coupons/" not in (loc or ""):
            print("FAIL 301 coupon", url, code, loc)
            fail += 1
        else:
            print("301 coupon", path, "->", loc)

    for path, min_bytes in RANKED_CMS:
        url = f"https://boonspreadsheet.com{path}"
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
            if path in ("/boonbuy-coupons/", "/boonbuy-invite-code/") and (
                INVITE in title or re.search(r"invite\s*(code)?\s*[A-Z0-9]{5,}", title, flags=re.I)
            ):
                print("FAIL invite in inner title", path, title)
                fail += 1
            if path == "/boonbuy-coupons/":
                desc_m = re.search(r'<meta name="description" content="([^"]*)"', html)
                desc = desc_m.group(1) if desc_m else ""
                if INVITE in desc:
                    print("FAIL invite in coupon description")
                    fail += 1
                if "BoonBuy Coupons 2026 Code Promo" not in title:
                    print("FAIL coupon money title", title)
                    fail += 1

    code, _, loc, _ = fetch("https://boonspreadsheet.com/", follow=False)
    if code in (301, 302, 303, 307, 308) and loc:
        print("FAIL 301 home", loc)
        fail += 1
    else:
        print("indep home", code)

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
