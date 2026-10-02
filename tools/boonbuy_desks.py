#!/usr/bin/env python3
"""BoonBuy desks: dest-unique #local on the .com hub; restore ranked CMS inners.

Gates:
1. Hub #local has the HUB fingerprint, no dest-country fingerprints.
2. Estimator country ≠ TLD; .com must say it is not a customs territory.
3. Titles have no invite token G8ZWVJI95; body has no customs coaching / 58-line snapshot.
   Coupon stacking stays on /boonbuy-coupons/ (not the homepage title).
4. Single public dest host — no same-agent country 301. www already 301s to apex.
5. No same-country extra hosts on origin. Ranked unique inners must 200 (not 301
   onto thin /coupons/ /shipping/ /start/). Deep paths must not 404.
6. Georgia home gets #local; do not PUT a 5KB country template over 24–45KB CMS.
   Official Help is an SPA — do not invent a free-day count.

ia-collapse.conf was 301ing GSC winners (coupons 169 clk / 45KB, legit 27 clk / 41KB,
shipping 22 clk / 45KB) onto 4–5KB Georgia skins. Disable that collapse.
gsc-redirects 2026→spreadsheet is backwards (12 clk unique into 2 clk) — drop it.
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
        "title": "BoonBuy .com hub — not a customs territory",
        "h1": "This .com hostname is not a customs territory — pick a real country",
        "keep": [
            ("/boonbuy-coupons/", "Coupons (ranked)"),
            ("/is-boonbuy-legit/", "Legit (ranked)"),
            ("/boonbuy-shipping-guide/", "Shipping guide"),
            ("/boonbuy-invite-code/", "Invite stacking"),
            ("/boonbuy-spreadsheet-2026/", "Spreadsheet 2026"),
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
    ("/boonbuy-spreadsheet-2026/", 8000),
    ("/boonbuy-refund-guide/", 8000),
    ("/boonbuy-spreadsheet/", 8000),
)


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
        print("hub", key, spec["host"], "bytes", len(html))
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


def put() -> None:
    generate()
    client = _connect()
    stamp = time.strftime("%Y%m%d-%H%M%S")
    bak = f"/www/backup/boonbuy-desks-{stamp}"
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
        _run(client, f"cp -a '{remote}' '{bak}/{spec['host']}.index.html'")
        sftp.put(str(local), remote)
        print("PUT", remote, "bytes", local.stat().st_size)

        ext = f"/www/server/panel/vhost/nginx/extension/{spec['host']}"
        _run(client, f"mkdir -p '{bak}/nginx'")
        _run(client, f"cp -a '{ext}/.' '{bak}/nginx/'")
        collapse = (
            "# disabled 2026-10-02 desks: unique ranked CMS must serve at GSC URLs.\n"
            "# Thin /coupons/ /shipping/ /start/ remain as extra paths, not destinations.\n"
        )
        with sftp.file(f"{ext}/ia-collapse.conf", "w") as fh:
            fh.write(collapse)
        print("disabled", f"{ext}/ia-collapse.conf")
        gsc = (
            "# GSC path aliases disabled 2026-10-02: /boonbuy-spreadsheet-2026/ "
            "outranks /boonbuy-spreadsheet/; both unique HTML stay.\n"
        )
        with sftp.file(f"{ext}/gsc-redirects.conf", "w") as fh:
            fh.write(gsc)
        print("cleared", f"{ext}/gsc-redirects.conf")

        root = f"/www/wwwroot/{spec['host']}"
        for rel in TITLE_SCRUB_REL:
            remote_inner = f"{root}/{rel}"
            try:
                with sftp.open(remote_inner) as fh:
                    inner_html = fh.read().decode("utf-8")
            except FileNotFoundError:
                print("skip missing", remote_inner)
                continue
            if INVITE not in inner_html and "G8ZWVJI95" not in inner_html:
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
    print("ranked CMS restored; .com hub not overwritten as a dest skin; AWS extra host skipped")
    client.close()


def live_check() -> None:
    import urllib.request

    pairs = [
        (
            "com",
            "https://boonspreadsheet.com/",
            "not a customs territory",
            ALIENS,
        ),
    ]

    class NR(urllib.request.HTTPRedirectHandler):
        def redirect_request(self, req, fp, code, msg, headers, newurl):
            return None

    def fetch(url, follow=True):
        req = urllib.request.Request(url, headers={"User-Agent": "boonbuy-desk-check/1.0"})
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

    dest_urls = ["https://boonspreadsheet.com/"]
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
