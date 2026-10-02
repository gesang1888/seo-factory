#!/usr/bin/env python3
"""USFans country desks: dest-unique #local, keep the 32KB .net CMS hub.

Gates:
1. Each host #local has that dest fingerprint, no sister fingerprints.
2. Estimator country ≠ TLD; .net must say it is not a customs territory.
3. Titles have no invite code; body has no customs coaching / 58-line snapshot.
4. Same-agent country URLs stay independent (no 301). UK ≠ NL; neither 301s to FansBuy.
5. Same-country twins: target #local first, then 301; deep paths must not 404.
6. Hub stays the original ~32KB CMS homepage — never PUT a 5KB country template over it.
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
EST = "https://usfans.com/estimation"
OFFICIAL = "https://usfans.com/"
HELP = "https://usfans.com/help"
DATE = "2 Oct 2026"
HUB_HOST = "usfansspreadsheet.net"
HUB_MIN = 28000
STORAGE = (
    "Official Help Center → Goods storage period "
    f"({HELP}); confirm that article the morning you ship"
)

DESTS = {
    "uk": {
        "host": "usfansspreadsheet.co.uk",
        "lang": "en-GB",
        "loc": "en",
        "dest": "GB",
        "dest_label": "the United Kingdom",
        "ccy": "GBP",
        "title": "USFans UK — Royal Mail lines, GBP, HMRC notes",
        "h1": "USFans for a UK delivery address (GBP, Royal Mail last-mile)",
        "keep": [
            ("/usfans-coupons/", "Coupons article"),
            ("/usfans-refund-guide/", "Refunds"),
            ("/usfans-shipping-guide/", "UK shipping"),
            ("/is-usfans-legit/", "Is it legit?"),
        ],
    },
    "nl": {
        "host": "usfansspreadsheet.nl",
        "lang": "nl-NL",
        "loc": "nl",
        "dest": "NL",
        "dest_label": "Nederland",
        "ccy": "EUR",
        "title": "USFans Nederland — Nederlandse postcode, geen Duitse automaat",
        "h1": "USFans voor een Nederlands adres (EUR, Nederlandse postcode)",
        "keep": [
            ("/usfans-refund-guide/", "Refund"),
            ("/usfans-shipping-guide/", "Verzending"),
            ("/usfans-coupons/", "Coupons"),
            ("/is-usfans-legit/", "Legit?"),
        ],
    },
}

HUB = {
    "host": HUB_HOST,
    "lang": "en",
    "loc": "en",
    "dest": None,
    "dest_label": "a country in the estimator",
    "ccy": "USD",
    "title": "USFans Spreadsheet — 10,601 QC Finds (2026)",
    "keep": [
        ("/usfans-spreadsheet/", "Search spreadsheet"),
        ("/guide.html", "How to buy"),
        ("/electronics.html", "Electronics"),
        ("/is-usfans-legit/", "Legit?"),
    ],
}

CONVERT_TWINS = {
    "usfansspreadsheet.uk": "usfansspreadsheet.co.uk",
}

EST_NOTE = {
    "uk": "Estimator country is GB, not this TLD, not EU, not the .net hub.",
    "nl": "Estimator-land is NL, niet deze TLD, niet EU, niet BE.",
    "hub": "This .net hub is not a customs territory. Pick the real ship-to country in the estimator, not this hostname.",
}

STORE_NOTE = {
    "nl": "Magazijn: officiële Help Center → Goods storage period; bevestig het artikel op de verzenddag.",
    "en": "Warehouse: official Help Center → Goods storage period; confirm that article the morning you ship.",
}

TRAIL = {
    "nl": ("Live-geld staat in", "deze HTML is geen kassa."),
    "en": ("Live money is in", "this HTML is not checkout."),
}

DEST_LOCAL_CSS = (
    ".sg-sec#local{margin:1.25rem 0 0}"
    ".sg-sec#local h2{margin-top:0}"
    ".ssub{color:var(--muted,#57534e);font-size:.95rem;margin:0 0 12px}"
)
HUB_LOCAL_CSS = (
    ".sg-sec#local{max-width:72rem;margin:1.5rem auto;padding:0 1.25rem}"
    ".sg-sec#local h2{margin-top:0}"
    ".ssub{color:#57534e;font-size:.95rem;margin:0 0 12px}"
    ".local-steps{margin:12px 0 0;padding:0;list-style:none;display:grid;gap:12px}"
    ".local-steps li{border:1px solid #e5e7eb;border-radius:12px;padding:14px 16px;background:#fff}"
    ".local-src{font-size:14px;color:#334155;line-height:1.7;margin:14px 0 0}"
)


def _facts(spec: dict) -> dict:
    return {
        "agent": "USFans",
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
    def title_sub(m):
        if new_title:
            return f"<title>{escape(new_title)}</title>"
        return m.group(0)

    return re.sub(r"<title>(.*?)</title>", title_sub, html, count=1, flags=re.S)


def patch_static(html: str, key: str, spec: dict) -> str:
    facts = _facts(spec)
    block = _local_block(key, spec)
    loc = spec["loc"]
    html = _strip_invite_title(html, spec.get("title"))
    if spec.get("h1"):
        html = re.sub(r"<h1>.*?</h1>", f"<h1>{escape(spec['h1'])}</h1>", html, count=1, flags=re.S)
    html = re.sub(r"impressions on a template", "impressions on this dest desk", html, flags=re.I)
    if 'class="skip"' not in html:
        html = html.replace("<body>", "<body>\n" + skip_link(skip_label(loc)).rstrip(), 1)
    if 'id="main"' not in html:
        html = html.replace("<main>", '<main id="main">', 1)
    if 'href="#local"' not in html and "</nav>" in html:
        html = html.replace(
            "</nav>",
            f'    <a href="#local">{escape(local_cta(facts))}</a>\n  </nav>',
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
    if re.search(r"58 l[ií]neas para Espa|23[,.]81\s*USD|how to under-?declar", html, flags=re.I):
        err.append("spain snapshot / coaching")
    if err:
        raise RuntimeError(f"{key}: {'; '.join(err)}")
    return html


def patch_hub(html: str) -> str:
    facts = _facts(HUB)
    block = _local_block("hub", HUB)
    if 'class="skip"' not in html:
        html = html.replace("<body>", "<body>\n" + skip_link("Skip to content").rstrip(), 1)
    if 'href="#local"' not in html:
        html = html.replace(
            '      <a href="blog/">Blog</a>\n    </nav>',
            '      <a href="blog/">Blog</a>\n      <a href="#local">Pick a country</a>\n    </nav>',
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
        marker = "</section>\n\n<div class=\"stats-strip\">"
        if marker not in html:
            raise RuntimeError("hub hero marker missing")
        html = html.replace(marker, "</section>\n" + block + "\n<div class=\"stats-strip\">", 1)
    err: list[str] = []
    _check_local_section(html, facts, err)
    if "not a customs territory" not in html:
        err.append("hub missing fingerprint")
    if len(html) < HUB_MIN:
        err.append(f"hub collapsed to {len(html)} bytes")
    if 'class="hero' not in html or "cat-grid" not in html or "search-bar" not in html:
        err.append("hub chrome missing")
    if err:
        raise RuntimeError(f"hub: {'; '.join(err)}")
    return html


def generate() -> None:
    assert_dest_packs_unique()
    blobs = {}
    for key, spec in DESTS.items():
        src = OUT / spec["host"] / "live-base" / "index.html"
        html = patch_static(src.read_text(encoding="utf-8"), key, spec)
        dest = OUT / spec["host"] / "overlay" / "index.html"
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(html, encoding="utf-8")
        inner = re.search(r'<section class="sg-sec" id="local".*?</section>', html, flags=re.S)
        blobs[key] = inner.group(0) if inner else ""
        print("dest", key, spec["host"], "bytes", len(html))
    hub_src = OUT / HUB_HOST / "live-base" / "index.html"
    hub_html = patch_hub(hub_src.read_text(encoding="utf-8"))
    hub_dest = OUT / HUB_HOST / "overlay" / "index.html"
    hub_dest.parent.mkdir(parents=True, exist_ok=True)
    hub_dest.write_text(hub_html, encoding="utf-8")
    inner = re.search(r'<section class="sg-sec" id="local".*?</section>', hub_html, flags=re.S)
    blobs["hub"] = inner.group(0) if inner else ""
    print("hub", HUB_HOST, "bytes", len(hub_html), "was", hub_src.stat().st_size)

    fps = {
        k: dest_local_pack(DESTS[k]["dest"] if k in DESTS else None)["fingerprint"]
        for k in blobs
    }
    for key, inner in blobs.items():
        fp = fps[key]
        if fp not in inner:
            raise SystemExit(f"{key} missing fingerprint {fp!r}")
        for other, ofp in fps.items():
            if other == key or ofp == fp:
                continue
            if ofp in inner:
                raise SystemExit(f"{key} leaked {other} {ofp!r}")
        if EST.split("://", 1)[-1].rstrip("/") not in inner and EST not in inner:
            raise SystemExit(f"{key} missing estimator")
        if key == "hub" and "not a customs territory" not in inner:
            raise SystemExit("hub missing customs-territory line")
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


def _ensure_catch_all(raw: str, target: str) -> str:
    needle_try = "    location / {\n        try_files $uri $uri/ $uri/index.html =404;\n    }"
    if needle_try in raw:
        return raw.replace(needle_try, f"    location / {{ return 301 https://{target}$request_uri; }}", 1)
    home_only = f"location / {{ return 301 https://{target}/; }}"
    keep_uri = f"location / {{ return 301 https://{target}$request_uri; }}"
    if home_only in raw:
        return raw.replace(home_only, keep_uri, 1)
    return re.sub(
        rf"(location\s+/\s*\{{\s*return\s+301\s+https://{re.escape(target)})/;(\s*\}})",
        rf"\1$request_uri;\2",
        raw,
        count=1,
    )


def patch_twins(client) -> None:
    changed = 0
    for twin, target in CONVERT_TWINS.items():
        path = f"/www/server/panel/vhost/nginx/{twin}.conf"
        raw = _run(client, f"cat '{path}'")
        if not raw:
            print("skip missing", twin)
            continue
        if f"https://{target}$request_uri" in raw:
            print("twin already $request_uri", twin, "→", target)
        else:
            new = _ensure_catch_all(raw, target)
            if new != raw:
                _run(client, f"cp -a '{path}' '/www/backup/usfans-twin-{twin}.conf'")
                sftp = client.open_sftp()
                with sftp.open(path, "w") as fh:
                    fh.write(new)
                sftp.close()
                changed += 1
                print("PATCH nginx", twin, "catch-all $request_uri →", target)
            else:
                print("twin already 301", twin, "→", target)
        gsc = f"/www/server/panel/vhost/nginx/extension/{twin}/gsc-redirects.conf"
        graw = _run(client, f"cat '{gsc}'")
        if graw and f"https://{twin}/" in graw:
            _run(client, f"cp -a '{gsc}' '/www/backup/usfans-gsc-{twin}.conf'")
            graw = graw.replace(f"https://{twin}/", f"https://{target}/")
            sftp = client.open_sftp()
            with sftp.open(gsc, "w") as fh:
                fh.write(graw)
            sftp.close()
            changed += 1
            print("PATCH nginx GSC redirects", twin, "→", target)
    if changed:
        print(_run(client, "nginx -t && nginx -s reload"))


def put() -> None:
    generate()
    client = _connect()
    stamp = time.strftime("%Y%m%d-%H%M%S")
    bak = f"/www/backup/usfans-desks-{stamp}"
    _run(client, f"mkdir -p '{bak}'")
    sftp = client.open_sftp()
    puts = [(spec["host"], OUT / spec["host"] / "overlay" / "index.html") for spec in DESTS.values()]
    puts.append((HUB_HOST, OUT / HUB_HOST / "overlay" / "index.html"))
    for host, local in puts:
        remote = f"/www/wwwroot/{host}/index.html"
        raw = local.read_text(encoding="utf-8")
        if 'id="local"' not in raw:
            raise SystemExit(f"refusing to PUT {host} without #local")
        if host == HUB_HOST and local.stat().st_size < HUB_MIN:
            raise SystemExit("refusing to PUT thin template over .net hub")
        _run(client, f"cp -a '{remote}' '{bak}/{host}.index.html'")
        sftp.put(str(local), remote)
        print("PUT", remote, "bytes", local.stat().st_size)
    sftp.close()
    patch_twins(client)
    print("backup", bak)
    client.close()


def live_check() -> None:
    import urllib.request

    pairs = [
        ("uk", "https://usfansspreadsheet.co.uk/", "Northern Ireland is often another", ("Packstation", "form A1A 1A1", "Poste Italiane")),
        ("nl", "https://usfansspreadsheet.nl/", "Nederlandse postcode", ("Packstation", "form A1A 1A1", "Poste Italiane")),
        ("hub", "https://usfansspreadsheet.net/", "not a customs territory", ("1010 Wien", "Packstation", "form A1A 1A1")),
    ]

    class NR(urllib.request.HTTPRedirectHandler):
        def redirect_request(self, req, fp, code, msg, headers, newurl):
            return None

    def fetch(url, follow=True):
        req = urllib.request.Request(url, headers={"User-Agent": "usf-desk-check/1.0"})
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
        if re.search(r"58 l[ií]neas para Espa|23[,.]81\s*USD|how to under-?declar", html, flags=re.I):
            print("  FAIL snapshot/coaching")
            fail += 1
        if key == "hub" and len(body) < HUB_MIN:
            print("  FAIL hub collapsed", len(body))
            fail += 1
        if key == "hub" and ("cat-grid" not in html or 'class="hero' not in html or "search-bar" not in html):
            print("  FAIL hub chrome gone")
            fail += 1
        if EST not in inner:
            print("  FAIL estimator url missing")
            fail += 1

    inners = [
        "https://usfansspreadsheet.co.uk/usfans-coupons/",
        "https://usfansspreadsheet.co.uk/usfans-shipping-guide/",
        "https://usfansspreadsheet.nl/usfans-shipping-guide/",
        "https://usfansspreadsheet.net/usfans-spreadsheet/",
        "https://usfansspreadsheet.net/electronics.html",
        "https://usfansspreadsheet.net/guide.html",
    ]
    for url in inners:
        code, final, _, body = fetch(url, follow=True)
        if code == 404 or len(body) < 4000:
            print("FAIL inner", url, code, len(body))
            fail += 1
        else:
            print("inner", code, len(body), final)

    dest_urls = [
        "https://usfansspreadsheet.co.uk/",
        "https://usfansspreadsheet.nl/",
        "https://usfansspreadsheet.net/",
        "https://fansbuy.co.uk/",
        "https://fansbuy.nl/",
    ]
    for a in dest_urls:
        code, _, loc, _ = fetch(a, follow=False)
        if code in (301, 302, 303, 307, 308) and loc:
            print("FAIL 301", a, "->", loc)
            fail += 1
        else:
            print("indep", a, code)

    twins = [
        ("https://usfansspreadsheet.uk/", "usfansspreadsheet.co.uk"),
        ("https://usfansspreadsheet.uk/usfans-coupons/", "usfansspreadsheet.co.uk"),
    ]
    for src, dest_host in twins:
        code, final, loc, body = fetch(src, follow=True)
        deep = src.rstrip("/").count("/") > 2
        if dest_host not in final or code == 404 or (deep and len(body) < 8000):
            print("FAIL twin", src, code, final, len(body))
            fail += 1
        else:
            print("twin", src, "→", final, code, len(body))

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
