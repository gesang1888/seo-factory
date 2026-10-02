#!/usr/bin/env python3
"""Superbuy country desks: dest-unique #local, keep ranked CMS inners.

Gates:
1. Each host #local has that dest fingerprint, no sister fingerprints.
2. Estimator country ≠ TLD (CA / IT / US dests; no .eu/.net hub on this cluster).
3. Titles have no invite code; body has no customs coaching / 58-line snapshot.
4. Same-agent country URLs stay independent (no 301). CA ≠ IT ≠ US.
5. No same-country twins on this cluster to convert.
6. Georgia homes get #local; ranked 14–42KB inners stay (EMS notice, shipping, recensioni).
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
EST = "https://www.superbuy.com/en/page/query/freight/"
OFFICIAL = "https://www.superbuy.com/"
HELP = "https://www.superbuy.com/en/page/guide/feecomposition/"
DATE = "2 Oct 2026"
INVITE = "EKgwfI"
STORAGE = (
    "Official fee-composition guide: 90 free warehouse days "
    f"({HELP}); confirm that article the morning you ship"
)

DESTS = {
    "ca": {
        "host": "superbuyspreadsheets.ca",
        "lang": "en-CA",
        "loc": "en",
        "dest": "CA",
        "dest_label": "Canada",
        "ccy": "CAD",
        "title": "Superbuy Canada — CBSA notes, Canadian postal code",
        "h1": "Superbuy for a Canadian delivery address (form A1A 1A1, not a US ZIP)",
        "keep": [
            ("/superbuy-announcement-ems-preferential-lines-service-suspension-notice/", "EMS notice (ranked)"),
            ("/superbuy-shipping/", "Shipping CA"),
            ("/superbuy-coupons/", "Coupons"),
            ("/is-superbuy-legit/", "Legit?"),
        ],
    },
    "it": {
        "host": "superbuyspreadsheets.it",
        "lang": "it-IT",
        "loc": "it",
        "dest": "IT",
        "dest_label": "Italia",
        "ccy": "EUR",
        "title": "Superbuy Italia — Poste Italiane, EUR, ADM",
        "h1": "Superbuy per un indirizzo in Italia (EUR, Poste Italiane)",
        "keep": [
            ("/superbuy-recensioni/", "Recensioni"),
            ("/is-superbuy-legit/", "È affidabile?"),
            ("/spedizione-superbuy/", "Spedizione IT"),
            ("/how-to-use-superbuy/", "Come si usa"),
        ],
    },
    "us": {
        "host": "superbuyspreadsheets.us",
        "lang": "en-US",
        "loc": "en",
        "dest": "US",
        "dest_label": "the United States",
        "ccy": "USD",
        "title": "Superbuy US — USPS notes, no invented de-minimis dollar",
        "h1": "Superbuy for a US delivery address (this desk does not invent a de-minimis dollar)",
        "keep": [
            ("/superbuy-spreadsheet/", "Spreadsheet"),
            ("/superbuy-announcements/", "Announcements"),
            ("/superbuy-coupons/", "Coupons"),
            ("/is-superbuy-legit/", "Is it legit?"),
        ],
    },
}

EST_NOTE = {
    "ca": "Estimator country is CA, not this TLD, not US, not a .net hub.",
    "it": "Il paese dell’estimator è IT, non questo TLD, non EU.",
    "us": "Estimator country is US, not this TLD, not CA, not EU.",
}

STORE_NOTE = {
    "it": "Magazzino: guida ufficiale 90 giorni gratis; conferma l’articolo il mattino della spedizione.",
    "en": "Warehouse: official fee-composition guide 90 free days; confirm that article the morning you ship.",
}

TRAIL = {
    "it": ("I soldi veri stanno in", "questo HTML non è cassa."),
    "en": ("Live money is in", "this HTML is not checkout."),
}

DEST_LOCAL_CSS = (
    ".sg-sec#local{margin:1.25rem 0 0}"
    ".sg-sec#local h2{margin-top:0}"
    ".ssub{color:var(--muted,#57534e);font-size:.95rem;margin:0 0 12px}"
)


def _facts(spec: dict) -> dict:
    return {
        "agent": "Superbuy",
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
        s = re.sub(r"\s*[—\-–:,]*\s*(invite|ref|code|coupon|partner)?\s*EKgwfI", "", s, flags=re.I)
        s = s.replace(INVITE, "")
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
    title_m = re.search(r"<title>(.*?)</title>", html, flags=re.S)
    title = title_m.group(1) if title_m else ""
    if INVITE in title:
        err.append("invite in title")
    if re.search(r"58 l[ií]neas para Espa|23[,.]81\s*USD|how to under-?declar", html, flags=re.I):
        err.append("spain snapshot / coaching")
    if err:
        raise RuntimeError(f"{key}: {'; '.join(err)}")
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
    fps = {k: dest_local_pack(DESTS[k].get("dest"))["fingerprint"] for k in blobs}
    for key, inner in blobs.items():
        fp = fps[key]
        if fp not in inner:
            raise SystemExit(f"{key} missing fingerprint {fp!r}")
        for other, ofp in fps.items():
            if other == key or ofp == fp:
                continue
            if ofp in inner:
                raise SystemExit(f"{key} leaked {other} {ofp!r}")
        if INVITE in inner:
            raise SystemExit(f"{key} invite in #local")
        if EST.split("://", 1)[-1].rstrip("/") not in inner and EST not in inner:
            raise SystemExit(f"{key} missing estimator")
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
    bak = f"/www/backup/superbuy-desks-{stamp}"
    _run(client, f"mkdir -p '{bak}'")
    sftp = client.open_sftp()
    for spec in DESTS.values():
        local = OUT / spec["host"] / "overlay" / "index.html"
        remote = f"/www/wwwroot/{spec['host']}/index.html"
        raw = local.read_text(encoding="utf-8")
        if 'id="local"' not in raw:
            raise SystemExit(f"refusing to PUT {spec['host']} without #local")
        _run(client, f"cp -a '{remote}' '{bak}/{spec['host']}.index.html'")
        sftp.put(str(local), remote)
        print("PUT", remote, "bytes", local.stat().st_size)
    sftp.close()
    print("backup", bak)
    print("no same-country twins to convert")
    client.close()


def live_check() -> None:
    import urllib.request

    pairs = [
        ("ca", "https://superbuyspreadsheets.ca/", "form A1A 1A1", ("Packstation", "Poste Italiane", "00-001 Warszawa")),
        ("it", "https://superbuyspreadsheets.it/", "Poste Italiane", ("Packstation", "form A1A 1A1", "1010 Wien")),
        ("us", "https://superbuyspreadsheets.us/", "does not invent a de-minimis dollar", ("Packstation", "form A1A 1A1", "Poste Italiane")),
    ]

    class NR(urllib.request.HTTPRedirectHandler):
        def redirect_request(self, req, fp, code, msg, headers, newurl):
            return None

    def fetch(url, follow=True):
        req = urllib.request.Request(url, headers={"User-Agent": "sb-desk-check/1.0"})
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
        print(f"{key:2} {code} bytes={len(body)} local={bool(inner)} fp={fp in html}")
        if code != 200 or not inner or fp not in inner:
            print("  FAIL status/local/fp")
            fail += 1
            continue
        for alien in aliens:
            if alien in inner:
                print("  FAIL sister", alien)
                fail += 1
        if INVITE in title:
            print("  FAIL invite in title")
            fail += 1
        if re.search(r"58 l[ií]neas para Espa|23[,.]81\s*USD|how to under-?declar", html, flags=re.I):
            print("  FAIL snapshot/coaching")
            fail += 1
        if EST not in inner:
            print("  FAIL estimator url missing")
            fail += 1

    inners = [
        "https://superbuyspreadsheets.ca/superbuy-announcement-ems-preferential-lines-service-suspension-notice/",
        "https://superbuyspreadsheets.ca/superbuy-shipping/",
        "https://superbuyspreadsheets.it/superbuy-recensioni/",
        "https://superbuyspreadsheets.it/is-superbuy-legit/",
        "https://superbuyspreadsheets.it/spedizione-superbuy/",
        "https://superbuyspreadsheets.us/superbuy-spreadsheet/",
    ]
    for url in inners:
        code, final, _, body = fetch(url, follow=True)
        if code == 404 or len(body) < 8000:
            print("FAIL inner", url, code, len(body))
            fail += 1
        else:
            print("inner", code, len(body), final)

    dest_urls = [f"https://{spec['host']}/" for spec in DESTS.values()]
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
