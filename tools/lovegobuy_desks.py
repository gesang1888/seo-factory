#!/usr/bin/env python3
"""LoveGoBuy country desks: dest-unique #local, keep ranked CMS inners.

Gates:
1. Each host #local has that dest fingerprint, no sister fingerprints.
2. Estimator country ≠ TLD; .eu (and the .com hub) must say not a customs territory.
3. Titles have no invite code; body has no customs coaching / 58-line snapshot.
4. Same-agent country URLs stay independent (no 301).
5. Same-country twins: target #local first, then 301; deep paths must not 404.
6. Do not PUT a 5KB country template over a unique CMS hub — these homes are
   the existing Georgia files with a surgical #local insert; inners stay.
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
EST = "https://www.lovegobuy.com/shipping/estimation/index"
OFFICIAL = "https://www.lovegobuy.com/"
DATE = "2 Oct 2026"
INVITE = "W5RJX3"
STORAGE = (
    "Public copies disagree (60 vs 90 free warehouse days); "
    "confirm live Help the morning you ship — do not treat either figure as official"
)

DESTS = {
    "es": {
        "host": "lovegobuyspreadsheet.es",
        "lang": "es-ES",
        "loc": "es",
        "dest": "ES",
        "dest_label": "España",
        "ccy": "EUR",
        "title": "LoveGoBuy España — Correos, opiniones y envío ya en ranking",
        "h1": "LoveGoBuy para una dirección en España (EUR, Correos)",
        "keep": [
            ("/lovegobuy-opiniones/", "Opiniones"),
            ("/es-lovegobuy-confiable/", "¿Es fiable?"),
            ("/envio-lovegobuy-espana/", "Envío a España"),
            ("/lovegobuy-spreadsheet/", "Spreadsheet"),
        ],
    },
    "it": {
        "host": "lovegobuy.it",
        "lang": "it-IT",
        "loc": "it",
        "dest": "IT",
        "dest_label": "Italia",
        "ccy": "EUR",
        "title": "LoveGoBuy Italia — Poste, recensioni e spedizione",
        "h1": "LoveGoBuy per un indirizzo in Italia (EUR, Poste Italiane)",
        "keep": [
            ("/lovegobuy-recensioni/", "Recensioni"),
            ("/spedizione-lovegobuy/", "Spedizione"),
            ("/lovegobuy-spreadsheet/", "Spreadsheet"),
            ("/is-lovegobuy-legit/", "È affidabile?"),
        ],
    },
    "nl": {
        "host": "lovegobuy.nl",
        "lang": "nl-NL",
        "loc": "nl",
        "dest": "NL",
        "dest_label": "Nederland",
        "ccy": "EUR",
        "title": "LoveGoBuy Nederland — PostNL-lijnen en verzending",
        "h1": "LoveGoBuy voor een Nederlands adres (EUR, PostNL)",
        "keep": [
            ("/lovegobuy-shipping/", "Verzending NL"),
            ("/lovegobuy-ervaringen/", "Ervaringen"),
            ("/lovegobuy-coupon/", "Coupons"),
            ("/lovegobuy-spreadsheet/", "Spreadsheet"),
        ],
    },
    "ca": {
        "host": "lovegobuyspreadsheet.ca",
        "lang": "en-CA",
        "loc": "en",
        "dest": "CA",
        "dest_label": "Canada",
        "ccy": "CAD",
        "title": "LoveGoBuy Canada — Canada Post, CAD, CBSA notes",
        "h1": "LoveGoBuy for a Canadian delivery address (CAD, Canada Post)",
        "keep": [
            ("/lovegobuy-spreadsheet/", "Canada spreadsheet"),
            ("/is-lovegobuy-legit/", "Is it legit?"),
            ("/lovegobuy-shipping/", "Shipping CA"),
            ("/how-to-use-lovegobuy/", "How to use"),
        ],
    },
}

HUBS = {
    "eu": {
        "host": "lovegobuyspreadsheet.eu",
        "lang": "en",
        "loc": "en",
        "dest": None,
        "dest_label": "a country in the estimator",
        "ccy": "EUR",
        "title": "LoveGoBuy EU spreadsheet hub — pick a country in the estimator",
        "h1": "This .eu hostname is not a customs territory",
        "keep": [
            ("/lovegobuy-europe/", "Europe notes"),
            ("/lovegobuy-spreadsheet/", "Spreadsheet"),
            ("/lovegobuy-shipping-eu/", "Shipping EU article"),
            ("/is-lovegobuy-legit/", "Is it legit?"),
        ],
    },
    "guide": {
        "host": "lovegobuyguide.com",
        "lang": "en",
        "loc": "en",
        "dest": None,
        "dest_label": "a country in the estimator",
        "ccy": "USD",
        "title": "LoveGoBuy global desk — pick a country in the estimator",
        "h1": "This hostname is not a customs territory",
        "keep": [
            ("/lovegobuy-spreadsheet/", "Spreadsheet"),
            ("/is-lovegobuy-legit/", "Is it legit?"),
            ("/how-to-use-lovegobuy/", "How to use"),
            ("/lovegobuy-shipping/", "Shipping article"),
        ],
    },
}

# IT twin already 301 → lovegobuy.it. NL twin is converted after target #local.
TWINS = {
    "lovegobuyspreadsheet.it": "lovegobuy.it",
    "lovegobuyspreadsheet.nl": "lovegobuy.nl",
}

TWIN_EXTRA = {
    "lovegobuyspreadsheet.it": [
        ("/lovegobuy-shipping", "/spedizione-lovegobuy/"),
        ("/is-lovegobuy-safe", "/is-lovegobuy-legit/"),
        ("/best-lovegobuy-spreadsheet", "/lovegobuy-spreadsheet/"),
        ("/lovegobuy-review", "/lovegobuy-recensioni/"),
        ("/lovegobuy-spreadsheets", "/lovegobuy-spreadsheet/"),
        ("/lovegobuy-coupons", "/lovegobuy-coupon/"),
        ("/lovegobuy-qc", "/lovegobuy-recensioni/"),
        ("/lovegobuy-finds", "/lovegobuy-spreadsheet/"),
        ("/lovegobuy-discord", "/how-to-use-lovegobuy/"),
    ],
    "lovegobuyspreadsheet.nl": [
        ("/lovegobuy-coupons", "/lovegobuy-coupon/"),
        ("/lovegobuy-verzending", "/lovegobuy-verzending/"),
        ("/best-lovegobuy-spreadsheet", "/lovegobuy-spreadsheet/"),
        ("/lovegobuy-spreadsheet", "/lovegobuy-spreadsheet/"),
        ("/lovegobuy-ervaringen", "/lovegobuy-ervaringen/"),
        ("/how-to-use-lovegobuy", "/how-to-use-lovegobuy/"),
        ("/is-lovegobuy-legit", "/is-lovegobuy-legit/"),
        ("/lovegobuy-shipping", "/lovegobuy-shipping/"),
        ("/lovegobuy-coupon", "/lovegobuy-coupon/"),
        ("/lovegobuy-finds", "/lovegobuy-spreadsheet/"),
        ("/lovegobuy-qc", "/lovegobuy-ervaringen/"),
        ("/lovegobuy-discord", "/how-to-use-lovegobuy/"),
    ],
}

EST_NOTE = {
    "es": "El país del estimador es ES, no este TLD, no EU.",
    "it": "Il paese dell’estimator è IT, non questo TLD, non EU.",
    "nl": "Estimator-land is NL, niet deze TLD, niet EU, niet BE.",
    "ca": "Estimator country is CA, not this TLD, not a US ZIP.",
    "eu": "This hostname is not a customs territory. Open the estimator with a real country, not .eu.",
    "guide": "This hostname is not a customs territory. Open the estimator with a real country, not this .com.",
}

STORE_NOTE = {
    "es": "Almacén: copias públicas no coinciden (60 vs 90 días). Confirma Help el día del envío. No trates ninguna cifra como oficial.",
    "it": "Magazzino: le copie pubbliche non coincidono (60 vs 90 giorni). Conferma Help il giorno della spedizione. Non trattare nessuna cifra come ufficiale.",
    "nl": "Magazijn: publieke kopieën verschillen (60 vs 90 dagen). Bevestig Help op de verzenddag. Geen van beide cijfers als officieel behandelen.",
    "en": "Warehouse: public copies disagree (60 vs 90 free days). Confirm live Help the morning you ship. Do not treat either figure as official.",
}

TRAIL = {
    "es": ("El dinero real está en", "este HTML no es caja."),
    "it": ("I soldi veri stanno in", "questo HTML non è cassa."),
    "nl": ("Live-geld staat in", "deze HTML is geen kassa."),
    "en": ("Live money is in", "this HTML is not checkout."),
}

DEST_LOCAL_CSS = (
    ".sg-sec#local{margin:1.25rem 0 0}"
    ".sg-sec#local h2{margin-top:0}"
    ".ssub{color:var(--muted,#57534e);font-size:.95rem;margin:0 0 12px}"
)


def _facts(spec: dict) -> dict:
    dest = spec.get("dest")
    return {
        "agent": "LoveGoBuy",
        "host": spec["host"],
        "lang": spec["lang"],
        "loc": spec["loc"],
        "dest": dest,
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
        s = re.sub(r"\s*[—\-–:,]*\s*(cupón|coupon|invite)?\s*W5RJX3", "", s, flags=re.I)
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

    def ld_sub(m):
        blob = m.group(2)
        blob = re.sub(
            r'("name"\s*:\s*")([^"]*W5RJX3[^"]*)(")',
            lambda n: n.group(1) + scrub(n.group(2)) + n.group(3),
            blob,
        )
        return m.group(1) + blob + m.group(3)

    html = re.sub(
        r'(<script type="application/ld\+json">)(.*?)(</script>)',
        ld_sub,
        html,
        count=1,
        flags=re.S,
    )
    return html


def patch_static(html: str, key: str, spec: dict) -> str:
    facts = _facts(spec)
    block = _local_block(key, spec)
    loc = spec["loc"]
    html = _strip_invite_title(html, spec.get("title"))
    if spec.get("h1"):
        html = re.sub(r"<h1>.*?</h1>", f"<h1>{escape(spec['h1'])}</h1>", html, count=1, flags=re.S)
    html = re.sub(r"impressions on a template", "impressions on this Canada desk", html, flags=re.I)
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
        html = html.replace("</style>", SKIP_CSS + DEST_LOCAL_CSS + "\n</style>", 1)
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
    if "impressions on a template" in html.lower():
        err.append("gsc editor note left in body")
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
    for key, spec in HUBS.items():
        src = OUT / spec["host"] / "live-base" / "index.html"
        html = patch_static(src.read_text(encoding="utf-8"), key, spec)
        dest = OUT / spec["host"] / "overlay" / "index.html"
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(html, encoding="utf-8")
        inner = re.search(r'<section class="sg-sec" id="local".*?</section>', html, flags=re.S)
        blobs[key] = inner.group(0) if inner else ""
        print("hub", key, spec["host"], "bytes", len(html), "was", src.stat().st_size)

    fps = {}
    for k in blobs:
        dest = DESTS[k]["dest"] if k in DESTS else None
        fps[k] = dest_local_pack(dest)["fingerprint"]
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
        if key in ("eu", "guide") and "not a customs territory" not in inner:
            raise SystemExit(f"{key} hub missing customs-territory line")
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
    bak = f"/www/backup/lovegobuy-desks-{stamp}"
    _run(client, f"mkdir -p '{bak}'")
    sftp = client.open_sftp()
    puts = [(spec["host"], OUT / spec["host"] / "overlay" / "index.html") for spec in DESTS.values()]
    puts += [(spec["host"], OUT / spec["host"] / "overlay" / "index.html") for spec in HUBS.values()]
    for host, local in puts:
        remote = f"/www/wwwroot/{host}/index.html"
        raw = local.read_text(encoding="utf-8")
        if 'id="local"' not in raw:
            raise SystemExit(f"refusing to PUT {host} without #local")
        if host in {h["host"] for h in HUBS.values()} and "not a customs territory" not in raw:
            raise SystemExit(f"refusing to PUT hub {host} without HUB fingerprint")
        _run(client, f"cp -a '{remote}' '{bak}/{host}.index.html'")
        sftp.put(str(local), remote)
        print("PUT", remote, "bytes", local.stat().st_size)
    sftp.close()
    patch_twins(client)
    print("backup", bak)
    client.close()


def _map_lines(twin: str, target: str) -> str:
    lines = []
    for src, dest in TWIN_EXTRA.get(twin, []):
        lines.append(f"    location = {src} {{ return 301 https://{target}{dest}; }}")
        lines.append(f"    location = {src}/ {{ return 301 https://{target}{dest}; }}")
    return "\n".join(lines)


def patch_twins(client) -> None:
    changed = 0
    for twin, target in TWINS.items():
        path = f"/www/server/panel/vhost/nginx/{twin}.conf"
        raw = _run(client, f"cat '{path}'")
        if not raw:
            print("skip missing", twin)
            continue
        extra = []
        for src, dest in TWIN_EXTRA.get(twin, []):
            if f"location = {src} " in raw or f"location = {src}{{" in raw:
                continue
            extra.append(f"    location = {src} {{ return 301 https://{target}{dest}; }}")
            extra.append(f"    location = {src}/ {{ return 301 https://{target}{dest}; }}")
        if twin == "lovegobuyspreadsheet.nl":
            needle = "    location / {\n        try_files $uri $uri/ $uri/index.html =404;\n    }"
            if needle in raw:
                raw = raw.replace(needle, "    location / { return 301 https://lovegobuy.nl/; }", 1)
                _run(client, f"cp -a '{path}' '/www/backup/lovegobuy-twin-{twin}.conf'")
                sftp = client.open_sftp()
                with sftp.open(path, "w") as fh:
                    fh.write(raw)
                sftp.close()
                changed += 1
                print("PATCH nginx NL twin catch-all → lovegobuy.nl")
            gsc = f"/www/server/panel/vhost/nginx/extension/{twin}/gsc-redirects.conf"
            graw = _run(client, f"cat '{gsc}'")
            if graw and "https://lovegobuyspreadsheet.nl/" in graw:
                _run(client, f"cp -a '{gsc}' '/www/backup/lovegobuy-nl-gsc-redirects.conf'")
                graw = graw.replace("https://lovegobuyspreadsheet.nl/", "https://lovegobuy.nl/")
                graw = graw.replace("https://lovegobuy.nl/lovegobuy-coupons/", "https://lovegobuy.nl/lovegobuy-coupon/")
                graw = graw.replace("https://lovegobuy.nl/lovegobuy-qc/", "https://lovegobuy.nl/lovegobuy-ervaringen/")
                graw = graw.replace("https://lovegobuy.nl/lovegobuy-discord/", "https://lovegobuy.nl/how-to-use-lovegobuy/")
                sftp = client.open_sftp()
                with sftp.open(gsc, "w") as fh:
                    fh.write(graw)
                sftp.close()
                changed += 1
                print("PATCH nginx NL GSC redirects → lovegobuy.nl")
            continue
        if extra:
            marker = "    location / { return 301"
            if marker not in raw:
                print("skip", twin, "no catch-all")
                continue
            raw = raw.replace(marker, "\n".join(extra) + "\n" + marker, 1)
            _run(client, f"cp -a '{path}' '/www/backup/lovegobuy-twin-{twin}.conf'")
            sftp = client.open_sftp()
            with sftp.open(path, "w") as fh:
                fh.write(raw)
            sftp.close()
            changed += 1
            print("PATCH nginx", twin, "extra", len(extra) // 2)
        else:
            print("ok nginx", twin)
    if changed:
        print(_run(client, "nginx -t && nginx -s reload"))


def live_check() -> None:
    import urllib.request

    pairs = [
        ("es", "https://lovegobuyspreadsheet.es/", "no copiamos un recuento de líneas", ("Packstation", "Poste Italiane", "form A1A 1A1")),
        ("it", "https://lovegobuy.it/", "Poste Italiane", ("Packstation", "form A1A 1A1", "1010 Wien")),
        ("nl", "https://lovegobuy.nl/", "Nederlandse postcode", ("Packstation", "form A1A 1A1", "Poste Italiane")),
        ("ca", "https://lovegobuyspreadsheet.ca/", "form A1A 1A1", ("Packstation", "Poste Italiane", "1010 Wien")),
        ("eu", "https://lovegobuyspreadsheet.eu/", "not a customs territory", ("Packstation", "form A1A 1A1", "Poste Italiane")),
        ("guide", "https://lovegobuyguide.com/", "not a customs territory", ("Packstation", "form A1A 1A1", "Poste Italiane")),
    ]

    class NR(urllib.request.HTTPRedirectHandler):
        def redirect_request(self, req, fp, code, msg, headers, newurl):
            return None

    def fetch(url, follow=True):
        req = urllib.request.Request(url, headers={"User-Agent": "lgb-desk-check/1.0"})
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
        print(f"{key:5} {code} bytes={len(body)} local={bool(inner)} fp={fp in html}")
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
        if key in ("eu", "guide") and "not a customs territory" not in inner:
            print("  FAIL hub fingerprint")
            fail += 1

    inners = [
        "https://lovegobuyspreadsheet.es/lovegobuy-opiniones/",
        "https://lovegobuy.it/lovegobuy-recensioni/",
        "https://lovegobuy.nl/lovegobuy-shipping/",
        "https://lovegobuyspreadsheet.ca/lovegobuy-spreadsheet/",
        "https://lovegobuyspreadsheet.eu/lovegobuy-europe/",
        "https://lovegobuyguide.com/lovegobuy-spreadsheet/",
    ]
    for url in inners:
        code, final, _, body = fetch(url, follow=True)
        if code == 404 or len(body) < 8000:
            print("FAIL inner", url, code, len(body))
            fail += 1
        else:
            print("inner", code, len(body), final)

    for a in (
        "https://lovegobuyspreadsheet.es/",
        "https://lovegobuy.it/",
        "https://lovegobuy.nl/",
        "https://lovegobuyspreadsheet.ca/",
        "https://lovegobuyspreadsheet.eu/",
        "https://lovegobuyguide.com/",
    ):
        code, _, loc, _ = fetch(a, follow=False)
        if code in (301, 302, 303, 307, 308) and loc:
            print("FAIL 301", a, "->", loc)
            fail += 1
        else:
            print("indep", a, code)

    for twin, target in TWINS.items():
        code, _, loc, _ = fetch(f"https://{twin}/", follow=False)
        print("twin", twin, code, loc)
        if code not in (301, 302, 308) or target not in (loc or ""):
            print("  FAIL twin 301")
            fail += 1
        deep = (
            f"https://{twin}/lovegobuy-coupons"
            if twin.endswith(".nl")
            else f"https://{twin}/lovegobuy-recensioni"
        )
        code2, _, _, body2 = fetch(deep, follow=True)
        if code2 == 404:
            print("  FAIL deep 404", twin)
            fail += 1
        else:
            print("  deep", twin, code2, "bytes", len(body2))

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
