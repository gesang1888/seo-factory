#!/usr/bin/env python3
"""CNShopper desks: surgical #local on two independent .net hubs.

Gates:
1. Each hub #local has the HUB fingerprint, no dest-country fingerprints.
2. Estimator country ≠ TLD; .net must say it is not a customs territory.
   cnshopper.net GSC: 1 ESP click. spreadsheet.net: 1 NZL click. Mixed 0-clk
   impressions. Still hubs — not ES, not NZ, not “EU”.
3. Titles have no invite token; no frozen code. Body has no customs coaching
   / 58-line snapshot. Unique coupon HTML stays on each host’s own files.
4. Two unique same-agent .net hosts with different jobs stay independent
   (SOP/agent-desk vs QC/Trustpilot spreadsheet). No 301 between them.
   Restore cnshopper.net vhost (currently a catch-all 301 onto spreadsheet
   home, which 404s unique 32KB paths).
5. Keep existing gsc-redirects. Do not invent extra 301s. Deep unique HTML
   must 200, not 404.
6. 4KB homes get #local. Do not PUT a 5KB dest overlay over unique 15–36KB HTML.

Official /en/estimate and /en/help 200. Do not invent a free-day count in #local.
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
EST = "https://www.cnshopper.com/en/estimate"
OFFICIAL = "https://www.cnshopper.com/en"
HELP = "https://www.cnshopper.com/en/help"
DATE = "2 Oct 2026"
INVITE = "___no_frozen_cnshopper_invite___"
HUB_MIN = 6000
LIVE_HUB_MIN = 7000
STORAGE = (
    "Official CNShopper Help is the live site "
    f"({HELP}); confirm that live copy the morning you ship. "
    "This desk does not invent a free-day count."
)

HUBS = {
    "net": {
        "host": "cnshopper.net",
        "lang": "en",
        "loc": "en",
        "dest": None,
        "dest_label": "a country in the estimator",
        "ccy": "USD",
        "title": None,
        "h1": None,
        "chrome": (
            "agent desk for global",
            "SOP vs QC logs",
            "CNShopper",
        ),
        "keep": [
            ("/cnshopper-spreadsheet-2026.html", "Spreadsheet 2026"),
            ("/cnshopper-coupon-tracker-2026.html", "Coupon tracker"),
            ("/is-cnshopper-legit.html", "Legit"),
            ("/fr/avis-cnshopper.html", "FR avis"),
        ],
        "insert_before": "<h2>Country agent desk — register and last-mile product names</h2>",
        "note_from": '<p class="note">CNShopper · global · cnshopper.net · agent desk</p>',
        "note_to": '<p class="note">CNShopper · global · cnshopper.net · not a customs territory</p>',
        "inject_nav": True,
        "ranked": (
            ("/cnshopper-spreadsheet-2026.html", 8000),
            ("/cnshopper-coupon-tracker-2026.html", 8000),
            ("/cnshopper-shipping-lines-2026.html", 8000),
            ("/cnshopper-real-shipping-bills-2026.html", 8000),
            ("/cnshopper-user-reports-2026.html", 8000),
            ("/cnshopper-faq.html", 8000),
            ("/is-cnshopper-legit.html", 8000),
            ("/fr/avis-cnshopper.html", 8000),
        ),
    },
    "ss": {
        "host": "cnshopperspreadsheet.net",
        "lang": "en",
        "loc": "en",
        "dest": None,
        "dest_label": "a country in the estimator",
        "ccy": "USD",
        "title": None,
        "h1": None,
        "chrome": (
            "FashionReps",
            "WeMimi",
            "Trustpilot",
            "CNShopper",
        ),
        "keep": [
            ("/cnshopperspread-user-reports-2026.html", "Trustpilot / Reddit notes"),
            ("/cnshopperspread-coupon-tracker-2026.html", "Coupon tracker"),
            ("/cnshopperspread-shipping-lines-2026.html", "Shipping lines"),
            ("/shoes/", "Shoes"),
        ],
        "insert_before": "<h2>What this host is for</h2>",
        "note_from": '<p class="note">CNShopper · spreadsheet · cnshopperspreadsheet.net · not FashionReps, not WeMimi</p>',
        "note_to": '<p class="note">CNShopper · spreadsheet · cnshopperspreadsheet.net · not a customs territory</p>',
        "inject_nav": False,
        "ranked": (
            ("/cnshopperspread-user-reports-2026.html", 8000),
            ("/cnshopperspread-coupon-tracker-2026.html", 8000),
            ("/cnshopperspread-shipping-lines-2026.html", 8000),
            ("/cnshopperspread-real-shipping-bills-2026.html", 8000),
            ("/shoes/", 3000),
            ("/jackets/", 3000),
            ("/jersey/", 3000),
        ),
    },
}

EST_NOTE = {
    "net": (
        "This .net operations/agent-desk hub is not a customs territory. One Spain "
        "click does not make .net an ES dest. Pick the real ship-to country in the "
        "official estimator, not this hostname, not “EU” as one country."
    ),
    "ss": (
        "This .net spreadsheet hub is not a customs territory. One New Zealand click "
        "does not make .net an NZ dest. Pick the real ship-to country in the official "
        "estimator, not this hostname, not “EU” as one country."
    ),
}

STORE_NOTE = {
    "en": (
        "Warehouse: official CNShopper Help. Confirm that live copy the morning "
        "you ship. Do not invent a free-day count on this hub."
    ),
}

TRAIL = {"en": ("Live money is in", "this HTML is not checkout.")}

HUB_LOCAL_CSS = (
    ".sg-sec#local{margin:1.25rem 0 0}"
    ".sg-sec#local h2{margin-top:0}"
    ".ssub{color:var(--muted,#57534e);font-size:.95rem;margin:0 0 12px}"
    ".local-steps{margin:12px 0 0;padding:0;list-style:none;display:grid;gap:12px}"
    ".local-steps li{border:1px solid color-mix(in srgb, var(--ink,#1c1917) 16%, transparent);"
    "border-radius:12px;padding:14px 16px;background:var(--card,#ffffff)}"
    ".local-steps strong{display:block;margin:0 0 6px;font-size:15px}"
    ".local-steps span{display:block;color:var(--muted,#57534e);line-height:1.7;font-size:15px}"
    ".local-src{font-size:14px;color:var(--muted,#57534e);line-height:1.7;margin:14px 0 0}"
    "#local{scroll-margin-top:96px}"
    "nav{display:flex;flex-wrap:wrap;gap:.8rem 1.2rem;margin:.4rem 0 0}"
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

KEEP_REDIRECTS: tuple[tuple[str, str], ...] = ()
NAV_END = "</nav>"


def _facts(spec: dict) -> dict:
    return {
        "agent": "CNShopper",
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


def _scrub_ss_alias_copy(html: str) -> str:
    html = html.replace(
        '<p><a href="https://cnshopper.net/">cnshopper.net</a> is a same-job alias with zero clicks. After this homepage is unique it 301s here (unknown paths land on <code>/</code>).',
        '<p><a href="https://cnshopper.net/">cnshopper.net</a> is the independent operations/agent-desk host (unique 32KB SOP HTML). This spreadsheet host keeps QC and Trustpilot notes. Do not 301 them together.',
    )
    html = html.replace(
        "Independent CNShopper spreadsheet. cnshopper.net is the same-job alias.",
        "Independent CNShopper spreadsheet. cnshopper.net is the independent agent-desk host.",
    )
    return html


def _inject_nav(html: str, spec: dict, facts: dict) -> str:
    links = "".join(
        f'<a href="{escape(href)}">{escape(lab)}</a>\n' for href, lab in (spec.get("keep") or [])[:4]
    )
    nav = (
        f"<nav>{links}"
        f'<a href="#local">{escape(local_cta(facts))}</a></nav>'
    )
    note = spec["note_to"]
    if note not in html:
        raise RuntimeError(f"{spec['host']} note missing after rewrite")
    if spec.get("inject_nav"):
        html = html.replace(note, note + "\n  " + nav, 1)
        return html
    if 'href="#local"' not in html:
        if NAV_END not in html:
            raise RuntimeError(f"{spec['host']} nav missing")
        html = html.replace(
            NAV_END,
            f'<a href="#local">{escape(local_cta(facts))}</a></nav>',
            1,
        )
    return html


def patch_static(html: str, key: str, spec: dict) -> str:
    facts = _facts(spec)
    block = _local_block(key, spec)
    loc = spec["loc"]
    if spec.get("note_from") and spec["note_from"] in html:
        html = html.replace(spec["note_from"], spec["note_to"], 1)
    if key == "ss":
        html = _scrub_ss_alias_copy(html)
    html = _inject_nav(html, spec, facts)
    if 'class="skip"' not in html:
        html = re.sub(
            r"(<body[^>]*>)",
            r"\1\n" + skip_link(skip_label(loc)).rstrip(),
            html,
            count=1,
        )
    if 'id="main"' not in html:
        html = html.replace("<main>", '<main id="main">', 1)
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
        marker = spec["insert_before"]
        if marker not in html:
            raise RuntimeError(f"{key} insert marker missing")
        html = html.replace(marker, block + "\n" + marker, 1)
    err: list[str] = []
    _check_local_section(html, facts, err)
    title_m = re.search(r"<title>(.*?)</title>", html, flags=re.S)
    title = title_m.group(1) if title_m else ""
    if re.search(r"invite\s*(code|id)?\s*[A-Z0-9]{5,}", title, flags=re.I) or INVITE in title:
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


def put() -> None:
    generate()
    client = _connect()
    stamp = time.strftime("%Y%m%d-%H%M%S")
    bak = f"/www/backup/cnshopper-desks-{stamp}"
    _run(client, f"mkdir -p '{bak}'")
    sftp = client.open_sftp()

    net_conf = "/www/server/panel/vhost/nginx/cnshopper.net.conf"
    net_bak = "/www/server/panel/vhost/nginx/cnshopper.net.conf.bak-evasion-alias"
    live_conf = _run(client, f"cat '{net_conf}'")
    if "cnshopperspreadsheet.net" in live_conf and "return 301" in live_conf:
        _run(client, f"cp -a '{net_conf}' '{bak}/cnshopper.net.conf.stub-301'")
        _run(client, f"cp -a '{net_bak}' '{net_conf}'")
        print("restored", net_conf, "from bak-evasion-alias")
    else:
        print("cnshopper.net vhost already serving")

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
        _run(client, f"cp -a '{ext}/.' '{bak}/nginx-{spec['host']}/' 2>/dev/null || true")

    nginx_t = _run(client, "nginx -t 2>&1")
    print(nginx_t)
    if "successful" not in nginx_t.lower() and "ok" not in nginx_t.lower():
        raise SystemExit("nginx -t failed; not reloading")
    print(_run(client, "nginx -s reload 2>&1"))
    sftp.close()
    print("backup", bak)
    print("two independent .net hubs; unique HTML kept; cnshopper.net vhost restored")
    client.close()


def live_check() -> None:
    import urllib.request

    class NR(urllib.request.HTTPRedirectHandler):
        def redirect_request(self, req, fp, code, msg, headers, newurl):
            return None

    def fetch(url, follow=True):
        req = urllib.request.Request(url, headers={"User-Agent": "cnshopper-desk-check/1.0"})
        opener = urllib.request.build_opener() if follow else urllib.request.build_opener(NR)
        try:
            with opener.open(req, timeout=25) as resp:
                return resp.status, resp.geturl(), resp.headers.get("Location") or "", resp.read()
        except urllib.error.HTTPError as e:
            return e.code, url, e.headers.get("Location") or "", e.read() if e.fp else b""

    fail = 0
    fp = "not a customs territory"
    for key, spec in HUBS.items():
        host = spec["host"]
        url = f"https://{host}/"
        code, _, loc, body = fetch(url, follow=True)
        html = body.decode("utf-8", "replace")
        title_m = re.search(r"<title>(.*?)</title>", html, flags=re.S)
        title = title_m.group(1) if title_m else ""
        inner_m = re.search(r'<section class="sg-sec" id="local".*?</section>', html, flags=re.S)
        inner = inner_m.group(0) if inner_m else ""
        print(f"{key} {code} bytes={len(body)} local={bool(inner)} fp={fp in html}")
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
            if len(body) < LIVE_HUB_MIN:
                print("  FAIL hub collapsed", len(body))
                fail += 1
            for marker in spec.get("chrome") or ():
                if marker not in html:
                    print("  FAIL hub chrome gone", marker)
                    fail += 1

        code, _, loc, _ = fetch(url, follow=False)
        if code in (301, 302, 303, 307, 308):
            print("FAIL hub 301", host, loc)
            fail += 1
        else:
            print("indep hub", host, code)

        other = "cnshopperspreadsheet.net" if host == "cnshopper.net" else "cnshopper.net"
        if loc and other in loc:
            print("FAIL sibling 301", host, "->", loc)
            fail += 1

        for path, min_bytes in spec.get("ranked") or ():
            inner_url = f"https://{host}{path}"
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

        code, _, loc, _ = fetch(f"https://www.{host}/", follow=False)
        if code in (301, 302, 303, 307, 308) and host in (loc or ""):
            print("www apex", host, code, loc)
        else:
            print("www", host, code, loc)

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
