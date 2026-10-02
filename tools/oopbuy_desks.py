#!/usr/bin/env python3
"""OOPBuy IT dest: Georgia 4.5KB home gets dest #local; unique CMS inners stay.

Gates:
1. Dest #local has Poste Italiane; no sister fingerprints.
2. Estimator country is IT (matches .it ccTLD — not a .eu/.net/.com hub).
   GSC SA is 403; dest chosen by ccTLD. Official SPA /estimation and /help.
   Do not invent a free-day count.
3. Homepage title has no invite token. Frozen CS5Z9ITOI stays on
   /oopbuy-coupons/ only. No customs coaching / 58-line snapshot.
4. Single origin dest host. www currently SNI-falls onto ACBuy CA — add www
   301 apex $request_uri. No same-agent country 301 (no other OOPBuy ccTLD
   on this panel).
5. No twins. Ranked 24–58KB inners must 200 (not 404). Deep www paths keep
   $request_uri onto this dest, not another agent.
6. Unique 24–58KB CMS inners stay. Only the 4.5KB Georgia home is rewritten
   as a dest desk — do not PUT a 5KB template over spreadsheet/coupons/legit.

Official Help/estimation are SPA shells (200 ~5KB). Confirm live copy; do
not invent warehouse days.
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
EST = "https://oopbuy.com/estimation"
OFFICIAL = "https://oopbuy.com/"
HELP = "https://oopbuy.com/help"
DATE = "2 Oct 2026"
INVITE = "CS5Z9ITOI"
HOST = "oopbuyspreadsheets.it"
PUBLIC = "oopbuyspreadsheets.it"
DEST_MIN = 3500
DEST_MAX = 16000
STORAGE = (
    "Official OOPBuy Help is the live site "
    f"({HELP}); that URL is a SPA shell. "
    "Confirm the live copy the morning you ship. "
    "This desk does not invent a free-day count."
)

DESTS = {
    "it": {
        "host": HOST,
        "lang": "it-IT",
        "loc": "it",
        "dest": "IT",
        "dest_label": "Italia",
        "ccy": "EUR",
        "title": "OOPBuy Italia — CAP italiano, Poste Italiane, EUR",
        "h1": "OOPBuy per un indirizzo di consegna in Italia",
        "keep": [
            ("/oopbuy-spreadsheet/", "Spreadsheet"),
            ("/oopbuy-coupons/", "Coupon (codici restano lì)"),
            ("/is-oopbuy-legit/", "È affidabile?"),
            ("/oopbuy-shipping-guide/", "Spedizione"),
            ("/how-to-use-oopbuy/", "How-to"),
        ],
    },
}

EST_NOTE = {
    "it": (
        "Nel form nolo ufficiale scegli IT, non EU come un solo paese, "
        "non questo hostname al posto del CAP. Un code postal francese "
        "o un código español è il paese sbagliato."
    ),
}

STORE_NOTE = {
    "it": (
        "Magazzino: Help ufficiale OOPBuy. Quell’URL è una SPA — conferma "
        "la copia live il mattino della spedizione. Non inventare un numero "
        "di giorni gratis su questo desk."
    ),
}

TRAIL = {"it": ("Il denaro vero sta in", "questo HTML non è cassa.")}

ALIENS = (
    "1010 Wien",
    "Packstation",
    "form A1A 1A1",
    "00-001 Warszawa",
    "00100 Helsinki",
    "no copiamos un recuento de líneas",
    "pas un code postal belge",
    "Nederlandse postcode",
    "does not invent a de-minimis dollar",
    "Northern Ireland is often another",
    "do not copy a GST rate",
    "not a customs territory",
)

RANKED_CMS = (
    ("/oopbuy-spreadsheet/", 20000),
    ("/oopbuy-shipping-guide/", 20000),
    ("/is-oopbuy-legit/", 20000),
    ("/oopbuy-coupons/", 20000),
    ("/how-to-use-oopbuy/", 8000),
    ("/oopbuy-qc-guide/", 8000),
    ("/oopbuy-refund-guide/", 8000),
    ("/oopbuy-spreadsheet-2026/", 8000),
    ("/blog/", 8000),
)

WWW_BLOCK = """server {
    listen 80;
    listen 443 ssl;
    http2 on;
    server_name www.oopbuyspreadsheets.it;
    ssl_certificate    /www/server/panel/vhost/cert/oopbuyspreadsheets.it/fullchain.pem;
    ssl_certificate_key    /www/server/panel/vhost/cert/oopbuyspreadsheets.it/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    include /www/server/panel/vhost/nginx/well-known/oopbuyspreadsheets.it.conf;
    return 301 https://oopbuyspreadsheets.it$request_uri;
}

"""


def _facts(spec: dict) -> dict:
    return {
        "agent": "OOPBuy",
        "host": spec["host"],
        "lang": spec["lang"],
        "loc": spec["loc"],
        "dest": spec.get("dest"),
        "dest_label": spec.get("dest_label") or "Italia",
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
    store = STORE_NOTE.get(loc) or STORE_NOTE["it"]
    live, not_co = TRAIL.get(loc) or TRAIL["it"]
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


def dest_home(key: str, spec: dict) -> str:
    facts = _facts(spec)
    block = _local_block(key, spec)
    nav = "".join(
        f'<a href="{escape(href)}">{escape(label)}</a>\n    '
        for href, label in spec["keep"]
    )
    title = spec["title"]
    h1 = spec["h1"]
    cta = escape(local_cta(facts))
    skip = skip_link(skip_label(spec["loc"])).rstrip()
    html = f"""<!doctype html>
<html lang="it-IT">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{escape(title)}</title>
<meta name="description" content="Desk OOPBuy per un indirizzo IT: CAP a cinque cifre, Poste Italiane, EUR. Spreadsheet e coupon già in ranking restano. Niente 301 verso un altro agente.">
<link rel="canonical" href="https://{HOST}/">
<link rel="alternate" hreflang="it-IT" href="https://{HOST}/">
<meta name="robots" content="index,follow">
<style>
:root {{ --ink:#1c1917; --muted:#57534e; --bg:#f8fafc; --card:#fff; --accent:#0f766e; }}
body {{ margin:0; font-family: Georgia, ui-serif, serif; background:var(--bg); color:var(--ink); line-height:1.55; }}
header, main, footer {{ max-width:46rem; margin:0 auto; padding:1.25rem; }}
.note {{ color:var(--muted); font-size:.92rem; }}
h1 {{ font-size:clamp(1.55rem,4vw,2.15rem); }}
h2 {{ font-size:1.18rem; margin-top:1.8rem; }}
table {{ width:100%; border-collapse:collapse; background:var(--card); }}
th, td {{ border:1px solid #d6d3d1; padding:.55rem .65rem; text-align:left; font-size:.95rem; }}
th {{ background:#ecfdf5; }}
a.cta {{ display:inline-block; background:var(--accent); color:#fff; text-decoration:none; padding:.7rem 1rem; border-radius:.5rem; }}
.box {{ background:var(--card); padding:1rem 1.1rem; border-radius:.5rem; }}
nav.local a {{ margin-right:1rem; }}
{SKIP_CSS}
</style>
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"WebPage","name":"{escape(title)}","inLanguage":"it-IT","url":"https://{HOST}/","about":"OOPBuy","isPartOf":{{"@type":"WebSite","name":"OOPBuy Italia","url":"https://{HOST}/"}}}}</script>
</head>
<body>
{skip}
<header>
  <p class="note">OOPBuy · Italia · {HOST} · Poste Italiane / EUR</p>
  <nav class="local">
    <a href="#local">{cta}</a>
    {nav}
  </nav>
</header>
<main id="main">
  <h1>{escape(h1)}</h1>
{block}
  <p>Questa hostname è il desk <strong>Italia</strong>. Lo spreadsheet, i coupon, la guida spedizione e la recensione già in ranking restano sotto i loro URL. Un nolo NL o un CAP tedesco è il documento sbagliato.</p>
  <p>Apri OOPBuy con un indirizzo IT così la valuta è EUR. Confronta le linee solo dopo le foto magazzino e i kg fatturati. Questo HTML non è cassa.</p>

  <h2>Pagine già su questo host</h2>
  <p>W2C: <a href="/oopbuy-spreadsheet/">/oopbuy-spreadsheet/</a>. Coupon (i codici restano lì): <a href="/oopbuy-coupons/">/oopbuy-coupons/</a>. Recensione: <a href="/is-oopbuy-legit/">/is-oopbuy-legit/</a>. Spedizione: <a href="/oopbuy-shipping-guide/">/oopbuy-shipping-guide/</a>.</p>

  <h2>Cosa cambia per un CAP italiano</h2>
  <table>
    <thead><tr><th>Confronto</th><th>Check IT</th></tr></thead>
    <tbody>
      <tr><td>Valuta</td><td>EUR dopo un indirizzo IT. Un ticket USD/CAD è un altro documento.</td></tr>
      <tr><td>Ultimo miglio</td><td>La SKU live parla di Poste Italiane / un prodotto IT, o solo di un nome generico?</td></tr>
      <tr><td>Volumetrico</td><td>Scatole e piumini dopo QC. I grammi Weidian non sono i kg fatturati.</td></tr>
      <tr><td>Dazi vs fee corriere</td><td>Lo decide la SKU e ADM. Questa pagina non sceglie un valore dichiarato.</td></tr>
    </tbody>
  </table>

  <h2>IVA / dogana — solo spiegata</h2>
  <div class="box">
    <p>IVA e dazi verso l’Italia seguono la linea acquistata in OOPBuy e i fatti della spedizione. <strong>Niente sottofatturazione.</strong></p>
  </div>
  <p><a class="cta" href="{escape(OFFICIAL)}">Aprire OOPBuy con un indirizzo IT</a></p>
</main>
<footer>
  <p class="note">Note indipendenti IT, non il sito ufficiale OOPBuy. Altri agenti restano file separati — niente 301.</p>
</footer>
</body>
</html>
"""
    err: list[str] = []
    _check_local_section(html, facts, err)
    title_m = re.search(r"<title>(.*?)</title>", html, flags=re.S)
    title_txt = title_m.group(1) if title_m else ""
    if INVITE in title_txt or re.search(r"invite\s*(code)?\s*[A-Z0-9]{5,}", title_txt, flags=re.I):
        err.append("invite in title")
    if INVITE in html:
        # stacking is allowed on coupons inner, not dest home
        err.append("frozen invite token on dest homepage")
    if re.search(r"58 l[ií]neas para Espa|23[,.]81\s*USD|how to under-?declar", html, flags=re.I):
        err.append("spain snapshot / coaching")
    fp = dest_local_pack("IT")["fingerprint"]
    if fp not in html:
        err.append("missing dest fingerprint")
    for alien in ALIENS:
        inner_m = re.search(r'<section class="sg-sec" id="local".*?</section>', html, flags=re.S)
        inner = inner_m.group(0) if inner_m else html
        if alien in inner:
            err.append(f"sister {alien}")
    n = len(html.encode("utf-8"))
    if n < DEST_MIN:
        err.append(f"dest home too small {n}")
    if n > DEST_MAX:
        err.append(f"dest home too large {n} (would look like a unique CMS overwrite)")
    if EST not in html:
        err.append("missing estimator")
    if re.search(r"90\s*dagen|90\s*days|60\s*-?\s*day", html, flags=re.I):
        err.append("invented free-day count")
    if err:
        raise RuntimeError(f"{key} dest home: {'; '.join(err)}")
    return html


def generate() -> None:
    assert_dest_packs_unique()
    blobs = {}
    for key, spec in DESTS.items():
        html = dest_home(key, spec)
        dest = OUT / spec["host"] / "overlay" / "index.html"
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(html, encoding="utf-8")
        inner = re.search(r'<section class="sg-sec" id="local".*?</section>', html, flags=re.S)
        blobs[key] = inner.group(0) if inner else ""
        print("dest", key, spec["host"], "bytes", len(html.encode("utf-8")))
    fps = {k: dest_local_pack(DESTS[k].get("dest"))["fingerprint"] for k in blobs}
    for key, inner in blobs.items():
        fp = fps[key]
        if fp not in inner:
            raise SystemExit(f"{key} missing fingerprint {fp!r}")
        for alien in ALIENS:
            if alien in inner:
                raise SystemExit(f"{key} leaked dest {alien!r}")
        if EST not in inner:
            raise SystemExit(f"{key} missing estimator")
        if INVITE in inner:
            raise SystemExit(f"{key} #local still has invite token")
        if re.search(r"90\s*dagen|90\s*days|60\s*-?\s*day", inner, flags=re.I):
            raise SystemExit(f"{key} invented free-day count in #local")
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
    bak = f"/www/backup/oopbuy-desks-{stamp}"
    _run(client, f"mkdir -p '{bak}'")
    sftp = client.open_sftp()
    for spec in DESTS.values():
        local = OUT / spec["host"] / "overlay" / "index.html"
        remote = f"/www/wwwroot/{spec['host']}/index.html"
        raw = local.read_text(encoding="utf-8")
        if 'id="local"' not in raw or "Poste Italiane" not in raw:
            raise SystemExit(f"refusing to PUT {spec['host']} without IT #local")
        if INVITE in raw:
            raise SystemExit(f"refusing to PUT {spec['host']} with invite on dest home")
        n = local.stat().st_size
        if n < DEST_MIN or n > DEST_MAX:
            raise SystemExit(f"refusing to PUT dest home size {n}")
        live = _run(client, f"wc -c < '{remote}'")
        try:
            live_n = int(live.strip().split()[0])
        except ValueError:
            live_n = 0
        if live_n and live_n >= 15000:
            raise SystemExit(f"refusing to PUT dest overlay over unique home {live_n} B")
        _run(client, f"cp -a '{remote}' '{bak}/{spec['host']}.index.html'")
        sftp.put(str(local), remote)
        print("PUT", remote, "bytes", n)

        vhost = f"/www/server/panel/vhost/nginx/{spec['host']}.conf"
        _run(client, f"cp -a '{vhost}' '{bak}/{spec['host']}.conf'")
        vraw = _run(client, f"cat '{vhost}'")
        if "server_name www.oopbuyspreadsheets.it" not in vraw:
            if not vraw.startswith("server"):
                raise SystemExit("unexpected vhost prefix")
            with sftp.file(vhost, "w") as fh:
                fh.write(WWW_BLOCK + vraw)
            print("added www 301 apex $request_uri")
        else:
            print("www already mapped")

        for rel, min_b in RANKED_CMS:
            inner = f"/www/wwwroot/{spec['host']}{rel}index.html"
            nbytes = _run(client, f"wc -c < '{inner}' 2>/dev/null || echo 0")
            try:
                inner_n = int(nbytes.strip().split()[0])
            except ValueError:
                inner_n = 0
            if inner_n and inner_n < min_b:
                raise SystemExit(f"unique CMS shrank {rel} {inner_n}")
            print("keep unique", rel, inner_n)

    nginx_t = _run(client, "nginx -t 2>&1")
    print(nginx_t)
    if "successful" not in nginx_t.lower() and "ok" not in nginx_t.lower():
        raise SystemExit("nginx -t failed; not reloading")
    print(_run(client, "nginx -s reload 2>&1"))
    sftp.close()
    print("backup", bak)
    print("Georgia home rewritten as IT dest; unique CMS kept; www no longer leaks to ACBuy CA")
    client.close()


def live_check() -> None:
    import urllib.request

    class NR(urllib.request.HTTPRedirectHandler):
        def redirect_request(self, req, fp, code, msg, headers, newurl):
            return None

    def fetch(url, follow=True):
        req = urllib.request.Request(
            url,
            headers={
                "User-Agent": "oopbuy-desk-check/1.0",
                "Cache-Control": "no-cache",
                "Pragma": "no-cache",
            },
        )
        opener = urllib.request.build_opener() if follow else urllib.request.build_opener(NR)
        try:
            with opener.open(req, timeout=25) as resp:
                return resp.status, resp.geturl(), resp.headers.get("Location") or "", resp.read()
        except urllib.error.HTTPError as e:
            return e.code, url, e.headers.get("Location") or "", e.read() if e.fp else b""

    fail = 0
    url = f"https://{PUBLIC}/"
    code, _, loc, body = fetch(url, follow=True)
    html = body.decode("utf-8", "replace")
    title_m = re.search(r"<title>(.*?)</title>", html, flags=re.S)
    title = title_m.group(1) if title_m else ""
    inner_m = re.search(r'<section class="sg-sec" id="local".*?</section>', html, flags=re.S)
    inner = inner_m.group(0) if inner_m else ""
    fp = "Poste Italiane"
    print(f"it {code} bytes={len(body)} local={bool(inner)} fp={fp in html}")
    if code != 200 or not inner or fp not in inner:
        print("  FAIL status/local/fp")
        fail += 1
    else:
        for alien in ALIENS:
            if alien in inner:
                print("  FAIL sister", alien)
                fail += 1
        if INVITE in title or re.search(r"invite\s*(code)?\s*[A-Z0-9]{5,}", title, flags=re.I):
            print("  FAIL invite in title")
            fail += 1
        if INVITE in html:
            print("  FAIL invite on dest homepage")
            fail += 1
        if re.search(r"58 l[ií]neas para Espa|23[,.]81\s*USD|how to under-?declar", html, flags=re.I):
            print("  FAIL snapshot/coaching")
            fail += 1
        if re.search(r"90\s*dagen|90\s*days|60\s*-?\s*day", inner, flags=re.I):
            print("  FAIL invented free-day copy")
            fail += 1
        if EST not in inner:
            print("  FAIL estimator")
            fail += 1
        if not (DEST_MIN <= len(body) <= DEST_MAX + 2000):
            print("  FAIL dest size", len(body))
            fail += 1

    code, _, loc, _ = fetch(url, follow=False)
    if code in (301, 302, 303, 307, 308):
        print("FAIL dest 301", loc)
        fail += 1
    else:
        print("indep dest", code)

    code, _, loc, _ = fetch("https://www.oopbuyspreadsheets.it/", follow=False)
    if code in (301, 302, 303, 307, 308) and PUBLIC in (loc or "") and "acbuy" not in (loc or "").lower():
        print("www apex", code, loc)
    else:
        print("FAIL www", code, loc)
        fail += 1

    deep = "/oopbuy-spreadsheet/"
    code, _, loc, _ = fetch(f"https://www.oopbuyspreadsheets.it{deep}", follow=False)
    if code in (301, 302, 303, 307, 308) and PUBLIC in (loc or "") and deep.rstrip("/") in (loc or "") and "acbuy" not in (loc or "").lower():
        print("www deep $request_uri", code, loc)
    else:
        print("FAIL www deep", code, loc)
        fail += 1

    for path, min_bytes in RANKED_CMS:
        inner_url = f"https://{PUBLIC}{path}"
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
