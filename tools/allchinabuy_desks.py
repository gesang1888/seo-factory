#!/usr/bin/env python3
"""AllChinaBuy / ACBuy country desks: dest-unique #local, keep the 48KB .com hub.

Gates:
1. Each host #local has that dest fingerprint, no sister fingerprints.
2. Estimator country ≠ TLD; the .com hub must say it is not a customs territory.
3. Titles have no invite/ref code; body has no customs coaching / 58-line snapshot.
4. Same-agent country URLs stay independent (no 301). CA ≠ NL ≠ UK.
5. Same-country twins: target #local first, then 301; deep paths must not 404.
6. Hub stays the original ~48KB CMS homepage — never PUT a 5KB country template over it.
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
EST = "https://www.acbuy.com/estimation/"
OFFICIAL = "https://www.acbuy.com/"
HELP = "https://www.acbuy.com/en/page/help/"
DATE = "2 Oct 2026"
INVITE = "5F2RRA"
INVITE2 = "EwjrSk"
COUPON = "ACBUY5"
STORAGE = (
    "Official ACBuy homepage / Help: 90 free warehouse days "
    f"({HELP}); confirm that article the morning you ship"
)
HUB_HOST = "allchina-buy.com"
HUB_MIN = 40000

DESTS = {
    "ca": {
        "host": "allchinabuyspreadsheet.ca",
        "lang": "en-CA",
        "loc": "en",
        "dest": "CA",
        "dest_label": "Canada",
        "ccy": "CAD",
        "title": "AllChinaBuy Canada — Canada Post, CAD, CBSA notes",
        "h1": "AllChinaBuy for a Canadian delivery address (CAD, form A1A 1A1)",
        "keep": [
            ("/allchinabuy-shipping-guide/", "Shipping CA"),
            ("/is-allchinabuy-legit/", "Is it legit?"),
            ("/allchinabuy-spreadsheet/", "Spreadsheet"),
            ("/allchinabuy-coupons/", "Coupons article"),
        ],
    },
    "nl": {
        "host": "acbuyspreadsheets.nl",
        "lang": "nl-NL",
        "loc": "nl",
        "dest": "NL",
        "dest_label": "Nederland",
        "ccy": "EUR",
        "title": "ACBuy Nederland — Nederlandse postcode, geen Duitse automaat",
        "h1": "ACBuy voor een Nederlands adres (EUR, Nederlandse postcode)",
        "keep": [
            ("/is-acbuy-legit/", "Review NL"),
            ("/acbuy-shipping-guide/", "Verzending"),
            ("/acbuy-coupons/", "Coupons"),
            ("/how-to-use-acbuy/", "Handleiding"),
        ],
    },
    "uk": {
        "host": "allchinabuyspreadsheets.co.uk",
        "lang": "en-GB",
        "loc": "en",
        "dest": "GB",
        "dest_label": "the United Kingdom",
        "ccy": "GBP",
        "title": "AllChinaBuy UK — Royal Mail, GBP, HMRC notes",
        "h1": "AllChinaBuy for a UK delivery address (GBP, Royal Mail last-mile)",
        "keep": [
            ("/allchinabuy-shipping-guide/", "UK shipping"),
            ("/allchinabuy-spreadsheet/", "Spreadsheet"),
            ("/how-to-use-allchinabuy/", "How to use"),
            ("/is-allchinabuy-legit/", "Is it legit?"),
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
    "title": "AllChinaBuy Spreadsheet 2026: 10,000+ Live Product Links",
    "keep": [
        ("/allchinabuy-spreadsheet/", "Spreadsheet catalog"),
        ("/how-to-use-allchinabuy/", "How to use"),
        ("/is-allchinabuy-legit/", "Is it legit?"),
        ("/allchinabuy-coupons/", "Coupons article"),
    ],
}

# Same-agent same-country extras. Dest = GSC clicks, then ccTLD.
# CA: allchinabuyspreadsheet.ca has 1 click; acbuy CA has 0.
# NL: acbuyspreadsheets.nl has 3 clicks; allchina NL has 0.
CONVERT_TWINS = {
    "acbuyspreadsheets.ca": "allchinabuyspreadsheet.ca",
    "allchinabuyspreadsheet.nl": "acbuyspreadsheets.nl",
}

PATH_MAP = {
    "acbuyspreadsheets.ca": [
        ("/acbuy-community/", "/allchinabuy-community/"),
        ("/acbuy-coupons/", "/allchinabuy-coupons/"),
        ("/acbuy-invite-code/", "/allchinabuy-invite-code/"),
        ("/acbuy-qc-guide/", "/allchinabuy-qc-guide/"),
        ("/acbuy-refund-guide/", "/allchinabuy-refund-guide/"),
        ("/acbuy-shipping-guide/", "/allchinabuy-shipping-guide/"),
        ("/acbuy-shoes-spreadsheet/", "/allchinabuy-shoes-spreadsheet/"),
        ("/acbuy-spreadsheet-2026/", "/allchinabuy-spreadsheet-2026/"),
        ("/acbuy-spreadsheet/", "/allchinabuy-spreadsheet/"),
        ("/how-to-use-acbuy/", "/how-to-use-allchinabuy/"),
        ("/is-acbuy-legit/", "/is-allchinabuy-legit/"),
        ("/spreadsheet/", "/allchinabuy-spreadsheet/"),
        ("/blog/posts/acbuy-customs-guide/", "/blog/posts/allchinabuy-customs-guide/"),
        ("/blog/posts/acbuy-reviews-2026/", "/blog/posts/allchinabuy-reviews-2026/"),
        ("/blog/posts/acbuy-spreadsheet-guide/", "/blog/posts/allchinabuy-spreadsheet-guide/"),
        ("/blog/posts/is-acbuy-legit/", "/is-allchinabuy-legit/"),
        ("/blog/posts/acbuy-points-coupons/", "/allchinabuy-coupons/"),
        ("/blog/posts/acbuy-shipping-tracking/", "/allchinabuy-shipping-guide/"),
        ("/blog/posts/acbuy-vs-allchinabuy/", "/is-allchinabuy-legit/"),
        ("/blog/posts/best-acbuy-spreadsheet/", "/allchinabuy-spreadsheet/"),
    ],
    "allchinabuyspreadsheet.nl": [
        ("/allchinabuy-community/", "/acbuy-community/"),
        ("/allchinabuy-coupons/", "/acbuy-coupons/"),
        ("/allchinabuy-invite-code/", "/acbuy-invite-code/"),
        ("/allchinabuy-qc-guide/", "/acbuy-qc-guide/"),
        ("/allchinabuy-refund-guide/", "/acbuy-refund-guide/"),
        ("/allchinabuy-shipping-guide/", "/acbuy-shipping-guide/"),
        ("/allchinabuy-shoes-spreadsheet/", "/acbuy-shoes-spreadsheet/"),
        ("/allchinabuy-spreadsheet-2026/", "/acbuy-spreadsheet-2026/"),
        ("/allchinabuy-spreadsheet/", "/acbuy-spreadsheet/"),
        ("/how-to-use-allchinabuy/", "/how-to-use-acbuy/"),
        ("/is-allchinabuy-legit/", "/is-acbuy-legit/"),
        ("/spreadsheet/", "/acbuy-spreadsheet/"),
        ("/blog/posts/allchinabuy-customs-guide/", "/blog/posts/acbuy-customs-guide/"),
        ("/blog/posts/allchinabuy-reviews-2026/", "/blog/posts/acbuy-reviews-2026/"),
        ("/blog/posts/allchinabuy-spreadsheet-guide/", "/blog/posts/acbuy-spreadsheet-guide/"),
        ("/blog/posts/is-allchinabuy-legit/", "/is-acbuy-legit/"),
        ("/blog/posts/allchinabuy-vs-ootdbuy/", "/blog/posts/acbuy-vs-allchinabuy/"),
        ("/blog/posts/postnl-btw-import-nl/", "/acbuy-shipping-guide/"),
        ("/blog/posts/nl-haul-consolidation-tips/", "/acbuy-shipping-guide/"),
        ("/blog/posts/taobao-spreadsheet-allchinabuy/", "/acbuy-spreadsheet/"),
        ("/blog/posts/acbuy-spreadsheet-allchinabuy/", "/acbuy-spreadsheet-2026/"),
        ("/blog/posts/acbuy-customs-guide/", "/acbuy-shipping-guide/"),
    ],
}

EST_NOTE = {
    "ca": "Estimator country is CA, not this TLD, not US, not the .com hub.",
    "nl": "Estimator-land is NL, niet deze TLD, niet EU, niet BE, niet het .com-hub.",
    "uk": "Estimator country is GB, not this TLD, not EU, not the .com hub.",
    "hub": "This .com hub is not a customs territory. Pick CA, NL or GB in the estimator — not this hostname, not “EU”.",
}

STORE_NOTE = {
    "nl": "Magazijn: officiële ACBuy Help 90 dagen gratis; bevestig het artikel op de verzenddag.",
    "en": "Warehouse: official ACBuy Help 90 free days; confirm that article the morning you ship.",
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
    ".sg-sec#local{max-width:1100px;margin:1.25rem auto;padding:0 1.2rem}"
    ".sg-sec#local h2{margin-top:0}"
    ".ssub{color:#57534e;font-size:.95rem;margin:0 0 12px}"
    ".local-steps{margin:12px 0 0;padding:0;list-style:none;display:grid;gap:12px}"
    ".local-steps li{border:1px solid #e5e7eb;border-radius:12px;padding:14px 16px;background:#fff}"
    ".local-src{font-size:14px;color:#334155;line-height:1.7;margin:14px 0 0}"
)


def _facts(spec: dict) -> dict:
    return {
        "agent": "AllChinaBuy",
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
        "codes_off_title": [INVITE, INVITE2, COUPON],
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
        s = re.sub(r"\s*[—\-–:,]*\s*(invite|ref|code)?\s*(5F2RRA|EwjrSk|ACBUY5)", "", s, flags=re.I)
        for code in (INVITE, INVITE2, COUPON):
            s = s.replace(code, "")
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
    for code in (INVITE, INVITE2, COUPON):
        if code in title:
            err.append(f"{code} in title")
    if re.search(r"58 l[ií]neas para Espa|23[,.]81\s*USD|how to under-?declar", html, flags=re.I):
        err.append("spain snapshot / coaching")
    if re.search(r"impressions on a template", html, flags=re.I):
        err.append("template-impressions copy")
    return err


def patch_static(html: str, key: str, spec: dict) -> str:
    facts = _facts(spec)
    block = _local_block(key, spec)
    loc = spec["loc"]
    html = _strip_invite_title(html, spec.get("title"))
    if spec.get("h1"):
        html = re.sub(r"<h1>.*?</h1>", f"<h1>{escape(spec['h1'])}</h1>", html, count=1, flags=re.S)
    html = re.sub(r"impressions on a template", "impressions on this dest desk", html, flags=re.I)
    html = html.replace(
        "ACBuy is a different agent key.",
        "ACBuy is the current AllChinaBuy brand name; acbuyspreadsheets.ca 301s here.",
    )
    html = html.replace(
        "ACBuy country hosts are a different agent — do not paste that HTML here.",
        "ACBuy is the current AllChinaBuy name. Canada and NL stay on their own dests — do not 301 this .co.uk onto them or the .com hub.",
    )
    html = html.replace(
        'AllChinaBuy staat op <a href="https://allchinabuyspreadsheet.nl/">allchinabuyspreadsheet.nl</a> — ander bedrijf, andere HTML.',
        'allchinabuyspreadsheet.nl 301t naar dit Nederlandse dest (zelfde agent; ACBuy is de huidige naam).',
    )
    html = html.replace("Not ACBuy. Not the UK .co.uk desk.", "Same agent as ACBuy. Not the UK .co.uk desk.")
    html = html.replace("Not ACBuy. Not allchina-buy.com.", "Same agent as ACBuy. Not the .com hub.")
    html = html.replace("Independent CA notes. Not ACBuy.", "Independent CA notes. Same agent as ACBuy.")
    html = html.replace("Independent UK notes. Not ACBuy.", "Independent UK notes. Same agent as ACBuy.")
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
    err.extend(_title_ok(html))
    if err:
        raise RuntimeError(f"{key}: {'; '.join(err)}")
    return html


def patch_hub(html: str) -> str:
    facts = _facts(HUB)
    block = _local_block("hub", HUB)
    html = _strip_invite_title(html, HUB["title"])
    if 'class="skip"' not in html:
        html = html.replace("<body>", "<body>\n" + skip_link("Skip to content").rstrip(), 1)
    if 'id="main"' not in html:
        html = html.replace("<main>", '<main id="main">', 1)
    if 'href="#local"' not in html:
        html = html.replace(
            '<li><a href="/">Home</a></li>',
            '<li><a href="/">Home</a></li>\n      <li><a href="#local">Pick a country</a></li>',
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
        marker = "  </section>\n  <div class=\"agents-bar\">"
        if marker not in html:
            raise RuntimeError("hub hero marker missing")
        html = html.replace(marker, "  </section>\n" + block + "\n  <div class=\"agents-bar\">", 1)
    err: list[str] = []
    _check_local_section(html, facts, err)
    err.extend(_title_ok(html))
    if "not a customs territory" not in html:
        err.append("hub missing fingerprint")
    if len(html) < HUB_MIN:
        err.append(f"hub collapsed to {len(html)} bytes")
    if 'class="hero' not in html or "category-grid" not in html:
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
        for code in (INVITE, INVITE2):
            if code in inner:
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
    bak = f"/www/backup/allchinabuy-desks-{stamp}"
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
            raise SystemExit("refusing to PUT thin template over .com hub")
        _run(client, f"cp -a '{remote}' '{bak}/{host}.index.html'")
        sftp.put(str(local), remote)
        print("PUT", remote, "bytes", local.stat().st_size)
    sftp.close()
    patch_twins(client)
    print("backup", bak)
    client.close()


def _rewrite_gsc(graw: str, twin: str, target: str) -> str:
    old_host = f"https://{twin}/"
    new_host = f"https://{target}/"
    graw = graw.replace(old_host, new_host)
    maps = sorted(PATH_MAP.get(twin, []), key=lambda p: len(p[0]), reverse=True)
    for src, dest in maps:
        graw = graw.replace(f"{new_host}{src.lstrip('/')}", f"{new_host}{dest.lstrip('/')}")
        # after first replace, some targets already include dest path
        graw = graw.replace(f"{new_host}{src}", f"{new_host}{dest}")
    existing = set(re.findall(r"location = (/[^\s{]+)", graw))
    extras = []
    for src, dest in PATH_MAP.get(twin, []):
        slash = src if src.endswith("/") else src + "/"
        if slash not in existing:
            extras.append(f"location = {slash} {{ return 301 {new_host}{dest.lstrip('/')}; }}")
    if extras:
        graw = graw.rstrip() + "\n" + "\n".join(extras) + "\n"
    return graw


def patch_twins(client) -> None:
    changed = 0
    for twin, target in CONVERT_TWINS.items():
        path = f"/www/server/panel/vhost/nginx/{twin}.conf"
        raw = _run(client, f"cat '{path}'")
        if not raw:
            print("skip missing", twin)
            continue
        needle = "    location / {\n        try_files $uri $uri/ $uri/index.html =404;\n    }"
        if needle in raw:
            raw = raw.replace(needle, f"    location / {{ return 301 https://{target}/; }}", 1)
            _run(client, f"cp -a '{path}' '/www/backup/allchinabuy-twin-{twin}.conf'")
            sftp = client.open_sftp()
            with sftp.open(path, "w") as fh:
                fh.write(raw)
            sftp.close()
            changed += 1
            print("PATCH nginx", twin, "catch-all →", target)
        gsc = f"/www/server/panel/vhost/nginx/extension/{twin}/gsc-redirects.conf"
        graw = _run(client, f"cat '{gsc}'")
        if graw and f"https://{twin}/" in graw:
            _run(client, f"cp -a '{gsc}' '/www/backup/allchinabuy-gsc-{twin}.conf'")
            graw = _rewrite_gsc(graw, twin, target)
            sftp = client.open_sftp()
            with sftp.open(gsc, "w") as fh:
                fh.write(graw)
            sftp.close()
            changed += 1
            print("PATCH nginx GSC redirects", twin, "→", target)
    if changed:
        print(_run(client, "nginx -t && nginx -s reload"))


def live_check() -> None:
    import urllib.request

    pairs = [
        ("ca", "https://allchinabuyspreadsheet.ca/", "form A1A 1A1", ("Packstation", "Poste Italiane", "1010 Wien", "Nederlandse postcode")),
        ("nl", "https://acbuyspreadsheets.nl/", "Nederlandse postcode", ("Packstation", "form A1A 1A1", "1010 Wien", "Poste Italiane")),
        ("uk", "https://allchinabuyspreadsheets.co.uk/", "Northern Ireland is often another", ("Packstation", "form A1A 1A1", "Poste Italiane")),
        ("hub", "https://allchina-buy.com/", "not a customs territory", ("1010 Wien", "Packstation", "form A1A 1A1", "Nederlandse postcode")),
    ]

    class NR(urllib.request.HTTPRedirectHandler):
        def redirect_request(self, req, fp, code, msg, headers, newurl):
            return None

    def fetch(url, follow=True):
        req = urllib.request.Request(url, headers={"User-Agent": "acb-desk-check/1.0"})
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
        for code_s in (INVITE, INVITE2, COUPON):
            if code_s in title:
                print("  FAIL invite in title", code_s)
                fail += 1
        if re.search(r"58 l[ií]neas para Espa|23[,.]81\s*USD|how to under-?declar", html, flags=re.I):
            print("  FAIL snapshot/coaching")
            fail += 1
        if key == "hub" and len(body) < HUB_MIN:
            print("  FAIL hub collapsed", len(body))
            fail += 1
        if key == "hub" and ("category-grid" not in html or 'class="hero' not in html):
            print("  FAIL hub chrome gone")
            fail += 1
        if EST not in inner:
            print("  FAIL estimator url missing")
            fail += 1

    inners = [
        "https://allchinabuyspreadsheet.ca/allchinabuy-shipping-guide/",
        "https://allchinabuyspreadsheet.ca/is-allchinabuy-legit/",
        "https://acbuyspreadsheets.nl/is-acbuy-legit/",
        "https://acbuyspreadsheets.nl/acbuy-shipping-guide/",
        "https://allchinabuyspreadsheets.co.uk/allchinabuy-shipping-guide/",
        "https://allchina-buy.com/allchinabuy-spreadsheet/",
        "https://allchina-buy.com/is-allchinabuy-legit/",
    ]
    for url in inners:
        code, final, _, body = fetch(url, follow=True)
        if code == 404 or len(body) < 8000:
            print("FAIL inner", url, code, len(body))
            fail += 1
        else:
            print("inner", code, len(body), final)

    dest_urls = [f"https://{spec['host']}/" for spec in DESTS.values()] + [f"https://{HUB_HOST}/"]
    for a in dest_urls:
        code, _, loc, _ = fetch(a, follow=False)
        if code in (301, 302, 303, 307, 308) and loc:
            print("FAIL 301", a, "->", loc)
            fail += 1
        else:
            print("indep", a, code)

    for twin, target in CONVERT_TWINS.items():
        code, _, loc, _ = fetch(f"https://{twin}/", follow=False)
        print("twin", twin, code, loc)
        if code not in (301, 302, 308) or target not in (loc or ""):
            print("  FAIL twin 301")
            fail += 1
        deep = (
            f"https://{twin}/is-acbuy-legit/"
            if twin.startswith("acbuy")
            else f"https://{twin}/allchinabuy-shipping-guide/"
        )
        code2, final2, _, body2 = fetch(deep, follow=True)
        if code2 == 404 or len(body2) < 8000:
            print("  FAIL deep 404", twin, code2, len(body2), final2)
            fail += 1
        else:
            print("  deep", twin, code2, "bytes", len(body2), final2)

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
