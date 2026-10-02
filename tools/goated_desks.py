#!/usr/bin/env python3
"""Goated desks: dest-unique #local on the .com hub; restore ranked CMS inners.

Gates:
1. Hub #local has the HUB fingerprint, no dest-country fingerprints.
2. Estimator country ≠ TLD; .com must say it is not a customs territory.
   GSC is SWE-heavy; the hostname is still .com, not a .se customs dest.
3. Titles have no invite token mwrnen; body has no customs coaching / 58-line snapshot.
   Coupon stacking stays on /goatedbuy-coupons/ (not the homepage title).
4. Single public dest host — no same-agent country 301. www already 301s to apex.
5. No same-country extra hosts on origin. Ranked unique inners must 200 (not 301
   onto thin /coupons/ /shipping/ /start/). Deep paths must not 404.
6. Billboard home gets #local; do not PUT a 5KB country template over 24–45KB CMS.
   Official Help/estimate paths 404; cite the live hash-router freight form.
   Do not invent a free-day count.

ia-collapse.conf was 301ing GSC winners (legit 11 clk / 41KB, coupons 9 clk / 43KB,
spreadsheet 5 clk / 38KB, shipping 3 clk / 45KB) onto 4–5KB skins. Disable that collapse.
gsc-redirects 2026→spreadsheet is weaker unique into stronger unique (1 clk → 5 clk) — keep it.
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
EST = "https://goatedbuy.com/#/pages/estimation/shipping"
OFFICIAL = "https://goatedbuy.com/"
DATE = "2 Oct 2026"
INVITE = "mwrnen"
STORAGE = (
    "Official GoatedBuy Help is an SPA shell "
    f"({OFFICIAL}); /help and /estimate 404. Confirm that live copy the morning you ship. "
    "This desk does not invent a free-day count."
)

HUBS = {
    "com": {
        "host": "goatedspreadsheet.com",
        "lang": "en",
        "loc": "en",
        "dest": None,
        "dest_label": "a country in the estimator",
        "ccy": "USD",
        "title": "GoatedBuy .com hub — not a customs territory",
        "h1": "This .com hostname is not a customs territory — pick a real country",
        "keep": [
            ("/goatedbuy-coupons/", "Coupons (ranked)"),
            ("/is-goatedbuy-legit/", "Legit (ranked)"),
            ("/goatedbuy-spreadsheet/", "Spreadsheet (ranked)"),
            ("/goatedbuy-shipping-guide/", "Shipping guide"),
            ("/how-to-use-goatedbuy/", "How to use"),
            ("/blog/", "Blog"),
        ],
    },
}

EST_NOTE = {
    "com": "This .com hub is not a customs territory. Sweden-heavy clicks do not make .com a SE dest. Pick the real ship-to country in the official freight form, not this hostname, not “EU” as one country.",
}

STORE_NOTE = {
    "en": "Warehouse: official GoatedBuy Help is an SPA; /help 404s. Confirm that live copy the morning you ship. Do not invent a free-day count on this hub.",
}

TRAIL = {
    "en": ("Live money is in", "this HTML is not checkout."),
}

DEST_LOCAL_CSS = (
    ".sg-sec#local{margin:1.25rem 0 0}"
    ".sg-sec#local h2{margin-top:0}"
    ".ssub{color:var(--muted,#a1a1aa);font-size:.95rem;margin:0 0 12px}"
)

ALIENS = ("1010 Wien", "Packstation", "form A1A 1A1", "Poste Italiane", "00-001 Warszawa")

TITLE_SCRUB_REL = (
    "coupons/index.html",
)

RANKED_CMS = (
    ("/is-goatedbuy-legit/", 20000),
    ("/goatedbuy-coupons/", 20000),
    ("/goatedbuy-spreadsheet/", 20000),
    ("/goatedbuy-shipping-guide/", 20000),
    ("/how-to-use-goatedbuy/", 8000),
    ("/blog/", 8000),
    ("/goatedbuy-invite-code/", 8000),
    ("/goatedbuy-community/", 8000),
    ("/goatedbuy-qc-guide/", 8000),
    ("/goatedbuy-refund-guide/", 8000),
    ("/goatedbuy-shoes-spreadsheet/", 8000),
    ("/blog/posts/goatedbuy-qc-rejection-guide/", 8000),
)

# Weaker unique 2026 into stronger unique spreadsheet — keep the 301.
KEEP_REDIRECTS = (
    ("/goatedbuy-spreadsheet-2026/", "/goatedbuy-spreadsheet/"),
)


def _facts(spec: dict) -> dict:
    return {
        "agent": "GoatedBuy",
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
    html = re.sub(
        r'(<meta property="og:title" content=")([^"]+)(")',
        lambda m: m.group(1) + (new_title or scrub(m.group(2))) + m.group(3),
        html,
        count=1,
    )
    return html


def _scrub_token_from_home(html: str) -> str:
    html = html.replace(
        "https://www.goatedbuy.com/#/pages/account/register?invite-code=mwrnen",
        "https://goatedbuy.com/",
    )
    html = html.replace(
        "https://goatedbuy.com/#/pages/account/register?invite-code=mwrnen",
        "https://goatedbuy.com/",
    )
    html = html.replace(
        "mwrnen is a hash-router invite on goatedbuy.com register. If you open the site without #/pages/account/register?invite-code=mwrnen you may create a naked account.",
        "Register on GoatedBuy itself. Coupon stacking stays on /goatedbuy-coupons/ — this homepage does not print a token.",
    )
    html = html.replace(
        "mwrnen is a hash-router invite on goatedbuy.",
        "Coupon stacking stays on /goatedbuy-coupons/.",
    )
    html = html.replace("Attach mwrnen on GoatedBuy", "Open GoatedBuy, then pick a real country")
    html = html.replace('<a href="/coupons/">mwrnen</a>', '<a href="/goatedbuy-coupons/">Coupons</a>')
    html = html.replace("plus a 15% off hook and invite-code mwrnen", "plus a 15% off hook")
    html = html.replace("and invite-code mwrnen", "")
    html = html.replace("invite-code mwrnen", "not a customs territory")
    html = html.replace("invite-code=mwrnen", "")
    html = html.replace("?invite-code=", "")
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
            f'    <a href="/goatedbuy-coupons/">Coupons</a>\n'
            f'    <a href="/is-goatedbuy-legit/">Legit</a>\n  </nav>',
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
        if specs[key].get("dest") is None and "not a customs territory" not in inner:
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
        s = re.sub(r"(?i)\s*[—\-–:,]*\s*(invite\s+)?mwrnen", "", s)
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


def put() -> None:
    generate()
    client = _connect()
    stamp = time.strftime("%Y%m%d-%H%M%S")
    bak = f"/www/backup/goated-desks-{stamp}"
    _run(client, f"mkdir -p '{bak}'")
    sftp = client.open_sftp()
    for spec in HUBS.values():
        local = OUT / spec["host"] / "overlay" / "index.html"
        remote = f"/www/wwwroot/{spec['host']}/index.html"
        raw = local.read_text(encoding="utf-8")
        if 'id="local"' not in raw:
            raise SystemExit(f"refusing to PUT {spec['host']} without #local")
        if "not a customs territory" not in raw:
            raise SystemExit(f"refusing to PUT {spec['host']} without hub fingerprint")
        if INVITE in raw:
            raise SystemExit(f"refusing to PUT {spec['host']} with frozen invite token")
        live = _run(client, f"wc -c < '{remote}'")
        try:
            live_n = int(live.strip().split()[0])
        except ValueError:
            live_n = 0
        if live_n > 20000:
            raise SystemExit(f"refusing to PUT over unique CMS home {live_n} B")
        _run(client, f"cp -a '{remote}' '{bak}/{spec['host']}.index.html'")
        sftp.put(str(local), remote)
        print("PUT", remote, "bytes", local.stat().st_size)

        ext = f"/www/server/panel/vhost/nginx/extension/{spec['host']}"
        _run(client, f"mkdir -p '{bak}/nginx'")
        _run(client, f"cp -a '{ext}/.' '{bak}/nginx/'")
        collapse = (
            "# disabled 2026-10-02 desks: unique ranked CMS must serve at GSC URLs.\n"
            "# Thin /coupons/ /shipping/ /start/ remain as extra paths, not destinations.\n"
            "# gsc-redirects 2026→spreadsheet stays (1 clk unique into 5 clk unique).\n"
        )
        with sftp.file(f"{ext}/ia-collapse.conf", "w") as fh:
            fh.write(collapse)
        print("disabled", f"{ext}/ia-collapse.conf")
        print("kept gsc-redirects.conf (2026→spreadsheet)")

        root = f"/www/wwwroot/{spec['host']}"
        for rel in TITLE_SCRUB_REL:
            remote_inner = f"{root}/{rel}"
            try:
                with sftp.open(remote_inner) as fh:
                    inner_html = fh.read().decode("utf-8")
            except FileNotFoundError:
                print("skip missing", remote_inner)
                continue
            if INVITE not in inner_html and "mwrnen" not in inner_html:
                print("title already clean", rel)
                continue
            title_m = re.search(r"<title>(.*?)</title>", inner_html, flags=re.S)
            title = title_m.group(1) if title_m else ""
            if INVITE not in title:
                print("token only in body, leave unique/thin body", rel)
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
    print("ranked CMS restored; .com hub not overwritten as a dest skin; 2026→spreadsheet kept")
    client.close()


def live_check() -> None:
    import urllib.request

    pairs = [
        (
            "com",
            "https://goatedspreadsheet.com/",
            "not a customs territory",
            ALIENS,
        ),
    ]

    class NR(urllib.request.HTTPRedirectHandler):
        def redirect_request(self, req, fp, code, msg, headers, newurl):
            return None

    def fetch(url, follow=True):
        req = urllib.request.Request(url, headers={"User-Agent": "goated-desk-check/1.0"})
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
        if re.search(r"invite\s*(code)?\s*[A-Z0-9]{5,}", title, flags=re.I) or INVITE in title:
            print("  FAIL invite in title")
            fail += 1
        if INVITE in html:
            print("  FAIL frozen invite on homepage")
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

    for path, min_bytes in RANKED_CMS:
        url = f"https://goatedspreadsheet.com{path}"
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
            if path in ("/goatedbuy-coupons/", "/coupons/") and (
                INVITE in title or re.search(r"invite\s*(code)?\s*[A-Z0-9]{5,}", title, flags=re.I)
            ):
                print("FAIL invite in inner title", path, title)
                fail += 1

    for src, dst in KEEP_REDIRECTS:
        url = f"https://goatedspreadsheet.com{src}"
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

    dest_urls = [
        "https://goatedspreadsheet.com/",
        "https://goatedbuy.com/",
    ]
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
