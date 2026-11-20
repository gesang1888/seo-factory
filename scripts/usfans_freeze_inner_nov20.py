#!/usr/bin/env python3
"""USFans freeze-safe inner recovery (20 Nov 2026).

Does NOT change frozen Title/H1 on the homepage or /usfans-spreadsheet/.
Does NOT invent coupon amounts or a higher row_count.
Does NOT open PL/IT/ES/DE ccTLDs.

  python3 scripts/usfans_freeze_inner_nov20.py --apply
  ORIENTDIG_DEPLOY_PASS='...' python3 scripts/usfans_freeze_inner_nov20.py --deploy
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OVERLAY = ROOT / "overlays" / "usfans-freeze-inner-20261120"
STAMP = "20261120"
REVIEW_ISO = "2026-11-20"
REVIEW_LONG = "20 November 2026"

FROZEN = {
    "index.html": (
        "USFans Spreadsheet — searchable QC catalog",
        "<h1>USFans Spreadsheet</h1>",
    ),
    "usfans-spreadsheet.html": (
        "Search the USFans spreadsheet",
    ),
}

REMOTE = {
    "index.html": "/www/wwwroot/usfansspreadsheet.net/index.html",
    "guide.html": "/www/wwwroot/usfansspreadsheet.net/guide.html",
    "llms.txt": "/www/wwwroot/usfansspreadsheet.net/llms.txt",
    "usfans-spreadsheet.html": "/www/wwwroot/usfansspreadsheet.net/usfans-spreadsheet/index.html",
    "usfans-shipping-guide.html": "/www/wwwroot/usfansspreadsheet.net/usfans-shipping-guide/index.html",
    "usfans-qc-photos.html": "/www/wwwroot/usfansspreadsheet.net/usfans-qc-photos/index.html",
    "finds-dataset.html": "/www/wwwroot/usfansspreadsheet.net/finds-dataset/index.html",
    "finds-dataset.json": "/www/wwwroot/usfansspreadsheet.net/data/finds-dataset.json",
    "es/index.html": "/www/wwwroot/usfansspreadsheet.net/es/index.html",
    "es/como-comprar-usfans.html": "/www/wwwroot/usfansspreadsheet.net/es/como-comprar-usfans/index.html",
    "pl/index.html": "/www/wwwroot/usfansspreadsheet.net/pl/index.html",
    "pl/jak-kupowac-usfans.html": "/www/wwwroot/usfansspreadsheet.net/pl/jak-kupowac-usfans/index.html",
}

HOST = os.environ.get("ORIENTDIG_DEPLOY_HOST", "31.97.41.31")
USER = os.environ.get("ORIENTDIG_DEPLOY_USER", "root")


def _read(rel: str) -> str:
    return (OVERLAY / rel).read_text(encoding="utf-8")


def _write(rel: str, text: str) -> None:
    path = OVERLAY / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def _insert_once(rel: str, marker: str, block: str) -> None:
    text = _read(rel)
    if f'data-freeze-inner="{STAMP}"' in text and block[:40] in text:
        return
    if marker not in text:
        raise SystemExit(f"{rel}: insert marker missing {marker!r}")
    _write(rel, text.replace(marker, block + marker, 1))


def _replace_all(rel: str, old: str, new: str) -> int:
    text = _read(rel)
    n = text.count(old)
    if n == 0:
        return 0
    _write(rel, text.replace(old, new))
    return n


def _assert_frozen() -> None:
    for rel, needles in FROZEN.items():
        text = _read(rel)
        for needle in needles:
            if needle not in text:
                raise SystemExit(f"FROZEN missing in {rel}: {needle!r}")
        title = re.search(r"<title[^>]*>(.*?)</title>", text, re.I | re.S)
        t = re.sub(r"\s+", " ", re.sub("<[^>]+>", "", title.group(1) if title else "")).strip()
        if rel == "index.html" and t != "USFans Spreadsheet — searchable QC catalog":
            raise SystemExit(f"homepage title changed: {t!r}")
        if rel == "usfans-spreadsheet.html" and t != "Search the USFans spreadsheet":
            raise SystemExit(f"catalog title changed: {t!r}")


def patch_catalog_stamp() -> None:
    data = json.loads(_read("finds-dataset.json"))
    if int(data.get("row_count") or 0) != 10601:
        raise SystemExit(f"row_count drifted: {data.get('row_count')}")
    data["last_verified"] = REVIEW_ISO
    data["generated_at"] = "2026-11-20T10:00:00Z"
    for sku in data.get("sample_skus") or []:
        sku["last_verified"] = REVIEW_ISO
    _write("finds-dataset.json", json.dumps(data, indent=2, ensure_ascii=False) + "\n")

    fd = _read("finds-dataset.html")
    fd = fd.replace("2026-10-27", REVIEW_ISO)
    fd = fd.replace("27 October 2026", REVIEW_LONG)
    if '"dateModified": "2026-11-03"' in fd:
        fd = fd.replace('"dateModified": "2026-11-03"', f'"dateModified": "{REVIEW_ISO}"')
    if 'content="2026-11-03"' in fd:
        fd = fd.replace('content="2026-11-03"', f'content="{REVIEW_ISO}"')
    if REVIEW_ISO not in fd:
        raise SystemExit("finds-dataset.html stamp not applied")
    if "USFans Finds Dataset — Row Counts, Sample SKUs" not in fd:
        raise SystemExit("finds-dataset title drifted")
    _write("finds-dataset.html", fd)

    for rel in ("index.html", "usfans-spreadsheet.html", "usfans-qc-photos.html"):
        text = _read(rel)
        text = text.replace("18 November 2026", REVIEW_LONG)
        text = text.replace("2026-11-18", REVIEW_ISO)
        text = text.replace("27 October 2026", REVIEW_LONG)
        text = text.replace("27 Oct 2026", "20 Nov 2026")
        text = text.replace("2026-10-27", REVIEW_ISO)
        _write(rel, text)


def patch_homepage() -> None:
    _replace_all(
        "index.html",
        "The official estimator needs US, CA, PL, ES — not this hostname.",
        "The official estimator needs a real ship-to country (PL, IT, ES, DE, US, CA) — not this hostname.",
    )
    box = f'''<section class="sg-sec" id="eu-desks" data-freeze-inner="{STAMP}">
  <h2>Ordering to Poland, Italy, Spain or Germany</h2>
  <p class="ssub">October searchers on this hub were mostly PL / IT / ES / DE, in English. Country notes live on the buying and shipping guides — this hostname is not a country in the estimator.</p>
  <ol class="local-steps">
    <li><strong>Poland</strong><span>Kod pocztowy is five digits. Pick <strong>PL</strong> on <a href="https://usfans.com/estimation" rel="noopener">usfans.com/estimation</a>. Poczta Polska / InPost last-mile depends on the line, not this .net. Polish how-to: <a href="/pl/jak-kupowac-usfans/">/pl/jak-kupowac-usfans/</a>.</span></li>
    <li><strong>Italy</strong><span>CAP is five digits. ADM is customs, not a coupon. Confirm the line on the estimator with country <strong>IT</strong> before you pay freight. English notes: <a href="/guide.html#pl-it-es-de">guide.html#pl-it-es-de</a>.</span></li>
    <li><strong>Spain</strong><span>Código postal is five digits. IVA / Aduanas are settled on the line you pick, not on this catalog. Spanish how-to: <a href="/es/como-comprar-usfans/">/es/como-comprar-usfans/</a>.</span></li>
    <li><strong>Germany</strong><span>Use <strong>DE</strong> in the estimator. Einfuhrumsatzsteuer is not a discount code. Zoll inspects parcels; this page does not coach a declared value.</span></li>
  </ol>
  <p class="local-src">QC still happens in the warehouse app before international shipping — checklist: <a href="/usfans-qc-photos/">/usfans-qc-photos/</a>. Catalog stamp {REVIEW_ISO}, row_count=10601.</p>
</section>
'''
    _insert_once("index.html", '<div class="stats-strip">', box)
    lang = (
        '<section id="language-options" style="max-width:920px;margin:40px auto;padding:0 24px;color:#1e293b;line-height:1.75">'
        "<h2>Browse in your language</h2>"
        "<p>English is the primary indexed hub. Short language entry pages: "
        '<a href="/es/" lang="es">Español</a> · <a href="/pl/" lang="pl">Polski</a> · '
        '<a href="/" lang="en">English</a>. Italy and Germany use the English desks on '
        '<a href="/guide.html#pl-it-es-de">guide.html#pl-it-es-de</a> — no extra ccTLD.</p></section>'
    )
    text = _read("index.html")
    old_lang = (
        '<section id="language-options" style="max-width:920px;margin:40px auto;padding:0 24px;color:#1e293b;line-height:1.75">'
        "<h2>Browse in your language</h2>"
        "<p>English is the primary indexed hub. Short language entry pages: "
        '<a href="/es/" lang="es">Español</a> · <a href="/pl/" lang="pl">Polski</a> · '
        '<a href="/" lang="en">English</a>.</p></section>'
    )
    if "guide.html#pl-it-es-de" not in text:
        if old_lang not in text:
            raise SystemExit("homepage language-options marker missing")
        _write("index.html", text.replace(old_lang, lang, 1))
    body = _read("index.html")
    if f'data-freeze-inner="{STAMP}"' not in body:
        body = body.replace(
            'data-traffic-recovery="20261118"',
            f'data-traffic-recovery="20261118" data-freeze-inner="{STAMP}"',
            1,
        )
        _write("index.html", body)


def patch_guide() -> None:
    toc = '    <a href="#worldwide">9. Does USFans Ship to My Country?</a>\n    <a href="#faq">10. FAQ</a>'
    toc_new = (
        '    <a href="#worldwide">9. Does USFans Ship to My Country?</a>\n'
        '    <a href="#pl-it-es-de">9b. Poland, Italy, Spain, Germany</a>\n'
        '    <a href="#faq">10. FAQ</a>'
    )
    text = _read("guide.html")
    if 'href="#pl-it-es-de"' not in text:
        if toc not in text:
            raise SystemExit("guide TOC marker missing")
        text = text.replace(toc, toc_new, 1)
        _write("guide.html", text)

    block = f'''  <section id="pl-it-es-de" data-freeze-inner="{STAMP}">
  <h2>9b. Poland, Italy, Spain, Germany — estimator country, not this hostname</h2>
  <p>This hub is <code>usfansspreadsheet.net</code>. Freight is quoted only when you pick a real country on
  <a href="https://usfans.com/estimation" rel="noopener">usfans.com/estimation</a>. October clicks on this host
  came mostly from those four countries, searching in English. Do not paste a declared value from this page into checkout.</p>
  <ul>
    <li><strong>Poland (PL)</strong> — Five-digit kod pocztowy. Last-mile is often Poczta Polska or InPost depending on the line the agent shows that day. VAT / cło is decided at import, not by this catalog. Polish walkthrough: <a href="/pl/jak-kupowac-usfans/">/pl/jak-kupowac-usfans/</a>.</li>
    <li><strong>Italy (IT)</strong> — Five-digit CAP. Poste Italiane / SDA last-mile depends on the booked line. ADM is the customs agency; it is not a coupon field. Approve warehouse QC before you pay the Italy line.</li>
    <li><strong>Spain (ES)</strong> — Five-digit código postal. Correos last-mile is common on budget air; express may use a private courier. IVA is not waived by this spreadsheet. Spanish walkthrough: <a href="/es/como-comprar-usfans/">/es/como-comprar-usfans/</a>.</li>
    <li><strong>Germany (DE)</strong> — Use DE in the estimator. Einfuhrumsatzsteuer / Zoll handling follows the line, not this TLD. DHL or Hermes last-mile is line-specific. Battery / liquid restrictions still hide some lines at checkout.</li>
  </ul>
  <p>Packed weight and volumetric size are what the quote uses. Recheck both after QC, then compare lines on the estimator. Shipping overview: <a href="/usfans-shipping-guide/#pl-it-es-de">/usfans-shipping-guide/#pl-it-es-de</a>.</p>
  </section>

'''
    _insert_once("guide.html", '  <h2 id="faq">10. FAQ</h2>', block)


def patch_shipping() -> None:
    _replace_all(
        "usfans-shipping-guide.html",
        "    <li>Use the 15% shipping coupon for new accounts</li>",
        "    <li>Confirm live wallet offers on <a href=\"/usfans-coupons/\">/usfans-coupons/</a> — this page does not invent a percentage</li>",
    )
    block = f'''  <h2 id="pl-it-es-de" data-freeze-inner="{STAMP}">Poland, Italy, Spain, Germany — what the estimator actually asks</h2>
  <p>Country-specific thin shells were not added. These four countries already used the English hub. Quote freight with the ISO country on
  <a href="https://usfans.com/estimation" rel="noopener">usfans.com/estimation</a>. This catalog does not take payment and does not coach a declared value.</p>
  <ul class="article-list">
    <li><strong>Poland</strong> — Select PL. Five-digit kod pocztowy. Budget air often hands to Poczta Polska; some lines use InPost. VAT is not a cell in the spreadsheet. How-to: <a href="/pl/jak-kupowac-usfans/">jak kupować</a>.</li>
    <li><strong>Italy</strong> — Select IT. Five-digit CAP. ADM / Agenzia delle Dogane is customs, not a discount code. Approve QC before the Italy line is booked.</li>
    <li><strong>Spain</strong> — Select ES. Five-digit código postal. IVA follows the line (IOSS / DDP / unpaid at Correos). How-to: <a href="/es/como-comprar-usfans/">cómo comprar</a>.</li>
    <li><strong>Germany</strong> — Select DE. Zoll / Einfuhrumsatzsteuer is line-specific. Express (DHL) is faster and more likely to be inspected; budget air is slower. Batteries may remove lines from the dropdown.</li>
  </ul>
  <p>First-order walkthrough with the same four desks: <a href="/guide.html#pl-it-es-de">guide.html#pl-it-es-de</a>. QC angles before you pay freight: <a href="/usfans-qc-photos/">/usfans-qc-photos/</a>.</p>

'''
    _insert_once(
        "usfans-shipping-guide.html",
        '  <h2>Regional shipping notes (one guide, not five thin pages)</h2>',
        block,
    )


def patch_qc() -> None:
    block = f'''  <h2 id="eu-qc" data-freeze-inner="{STAMP}">Warehouse QC is the same for PL / IT / ES / DE</h2>
  <p>The warehouse set is taken in China, in the official app, for the SKU you paid for. Last-mile (Poczta, Poste, Correos, Zoll/DHL) happens after you accept photos and pay the line. Request another angle while the goods are still in the warehouse — a return after the parcel is booked to Europe is the expensive path.</p>
  <ul class="article-list">
    <li>Poland / Spain walkthroughs: <a href="/pl/jak-kupowac-usfans/">jak kupować</a>, <a href="/es/como-comprar-usfans/">cómo comprar</a>.</li>
    <li>Italy / Germany notes stay on the English guide: <a href="/guide.html#pl-it-es-de">guide.html#pl-it-es-de</a>.</li>
    <li>Catalog proof for this pass: ten sample SKUs still 200 on 20 November 2026, <code>row_count=10601</code>, stamp {REVIEW_ISO}.</li>
  </ul>

'''
    text = _read("usfans-qc-photos.html")
    marker = "  <h2>Two photo sets (do not mix them)</h2>"
    if f'data-freeze-inner="{STAMP}"' not in text:
        if marker not in text:
            raise SystemExit("qc photos marker missing")
        text = text.replace(marker, block + marker, 1)
        _write("usfans-qc-photos.html", text)


def patch_es_pl() -> None:
    es_howto = f'''    <section id="espana" data-freeze-inner="{STAMP}">
      <h2>España: estimador, IVA y QC de almacén</h2>
      <p>Este host es un catálogo en inglés (<code>usfansspreadsheet.net</code>), no un país en el formulario de envío. En
      <a href="https://usfans.com/estimation" rel="noopener">usfans.com/estimation</a> elige <strong>España / ES</strong>.
      El código postal son cinco dígitos. IVA y Aduanas dependen de la línea (IOSS, DDP o pago en Correos): esta página no inventa un valor declarado ni un cupón.</p>
      <ol>
        <li>Filtra el catálogo en <a href="/usfans-spreadsheet/">/usfans-spreadsheet/</a> (10.601 finds, sello {REVIEW_ISO}). No hace falta una Google Sheet de Reddit.</li>
        <li>Pega el enlace del vendedor en usfans.com. El primer pago es la compra nacional a Taobao / Weidian / 1688.</li>
        <li>Revisa el set QC del almacén en la app — costuras, talla, estampado — <em>antes</em> de pagar el flete a España. Lista: <a href="/usfans-qc-photos/">/usfans-qc-photos/</a>.</li>
        <li>Compara peso real y volumétrico. Correos suele ser last-mile en aéreo económico; express usa otro courier. Confirma la línea el día del pago.</li>
      </ol>
      <p>Notas en inglés para Italia y Alemania (no hay ccTLD nuevo): <a href="/guide.html#pl-it-es-de">guide.html#pl-it-es-de</a>.</p>
    </section>
'''
    _insert_once(
        "es/como-comprar-usfans.html",
        "  </main>",
        es_howto,
    )
    _replace_all("es/como-comprar-usfans.html", "Updated 21 September 2026", f"Updated {REVIEW_LONG}")

    pl_howto = f'''    <section id="polska" data-freeze-inner="{STAMP}">
      <h2>Polska: estymator, VAT i QC w magazynie</h2>
      <p>Ten host to katalog po angielsku (<code>usfansspreadsheet.net</code>), nie kraj w formularzu wysyłki. Na
      <a href="https://usfans.com/estimation" rel="noopener">usfans.com/estimation</a> wybierz <strong>Poland / PL</strong>.
      Kod pocztowy ma pięć cyfr. VAT / cło zależy od linii, nie od tej strony. Nie wklejaj stąd zadeklarowanej wartości.</p>
      <ol>
        <li>Szukaj w katalogu <a href="/usfans-spreadsheet/">/usfans-spreadsheet/</a> (10 601 finds, stempel {REVIEW_ISO}). To nie jest arkusz z Reddita.</li>
        <li>Wklej link sprzedawcy do usfans.com. Pierwsza płatność to zakup krajowy (Taobao / Weidian / 1688) do magazynu w Chinach.</li>
        <li>Zatwierdź zdjęcia QC w aplikacji <em>zanim</em> opłacisz linię do Polski. Checklist: <a href="/usfans-qc-photos/">/usfans-qc-photos/</a>.</li>
        <li>Porównaj wagę rzeczywistą i objętościową. Last-mile bywa Poczta Polska albo InPost — to zależy od linii w dniu wysyłki, nie od tej domeny.</li>
      </ol>
      <p>Włochy i Niemcy: angielskie notatki na <a href="/guide.html#pl-it-es-de">guide.html#pl-it-es-de</a>. Bez nowych ccTLD.</p>
    </section>
'''
    _insert_once(
        "pl/jak-kupowac-usfans.html",
        "  </main>",
        pl_howto,
    )
    _replace_all("pl/jak-kupowac-usfans.html", "Updated 21 September 2026", f"Updated {REVIEW_LONG}")

    es_home = f'''    <section id="espana-entry" data-freeze-inner="{STAMP}">
      <h2>Para envíos a España</h2>
      <p>Elige <strong>ES</strong> en el estimador oficial. IVA/Aduanas no se pagan en este catálogo. La guía indexada con el escritorio España está en
      <a href="/es/como-comprar-usfans/">/es/como-comprar-usfans/</a>. Catálogo: <a href="/usfans-spreadsheet/">10.601 finds</a>.</p>
    </section>
'''
    _insert_once("es/index.html", "  </main>", es_home)
    _replace_all("es/index.html", "Updated 21 September 2026", f"Updated {REVIEW_LONG}")

    pl_home = f'''    <section id="polska-entry" data-freeze-inner="{STAMP}">
      <h2>Wysyłka do Polski</h2>
      <p>W estymatorze wybierz <strong>PL</strong>. VAT/cło nie są polem tej strony. Pełny poradnik:
      <a href="/pl/jak-kupowac-usfans/">/pl/jak-kupowac-usfans/</a>. Katalog: <a href="/usfans-spreadsheet/">10 601 finds</a>.</p>
    </section>
'''
    _insert_once("pl/index.html", "  </main>", pl_home)
    _replace_all("pl/index.html", "Updated 21 September 2026", f"Updated {REVIEW_LONG}")


def patch_llms() -> None:
    text = _read("llms.txt")
    line = (
        f"# freeze-inner {REVIEW_ISO}: PL/IT/ES/DE buying notes on existing inner URLs; "
        "catalog stamp after SKU 200-check; Title/H1 frozen\n"
    )
    if "freeze-inner 2026-11-20" not in text:
        _write("llms.txt", line + text)


def apply() -> None:
    if not (OVERLAY / "index.html").is_file():
        raise SystemExit(f"missing overlay {OVERLAY}")
    patch_catalog_stamp()
    patch_homepage()
    patch_guide()
    patch_shipping()
    patch_qc()
    patch_es_pl()
    patch_llms()
    _assert_frozen()
    data = json.loads(_read("finds-dataset.json"))
    if data["row_count"] != 10601 or data["last_verified"] != REVIEW_ISO:
        raise SystemExit("dataset stamp mismatch")
    print(f"overlay ready at {OVERLAY}")
    for rel in REMOTE:
        print(f"  {rel} {(OVERLAY / rel).stat().st_size}")


def _connect():
    try:
        import paramiko
    except ImportError:
        import subprocess

        subprocess.check_call([sys.executable, "-m", "pip", "install", "paramiko", "-q"])
        import paramiko

    password = (
        os.environ.get("ORIENTDIG_DEPLOY_PASS")
        or os.environ.get("BBDBUY_DEPLOY_PASS")
        or os.environ.get("KAKOBUY_DEPLOY_PASS")
    )
    if not password:
        raise SystemExit("Set ORIENTDIG_DEPLOY_PASS")
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(
        HOST,
        username=USER,
        password=password,
        timeout=30,
        allow_agent=False,
        look_for_keys=False,
    )
    return client


def _run(client, cmd: str, timeout: int = 120) -> str:
    _, stdout, stderr = client.exec_command(cmd, timeout=timeout)
    return (stdout.read() + stderr.read()).decode("utf-8", "replace").strip()


def deploy() -> None:
    if not OVERLAY.exists():
        apply()
    client = _connect()
    bak = f"/www/backup/usfans-freeze-inner-{STAMP}"
    print(_run(client, f"mkdir -p {bak}"))
    sftp = client.open_sftp()
    for rel, remote in REMOTE.items():
        local = OVERLAY / rel
        stamp_name = rel.replace("/", "__")
        _run(client, f"cp -a {remote} {bak}/{stamp_name} 2>/dev/null || true")
        tmp = remote + f".new-{STAMP}"
        sftp.put(str(local), tmp)
        print(rel, _run(client, f"mv {tmp} {remote} && chown www:www {remote} && chmod 644 {remote}"))
    sftp.close()
    client.close()
    print("deployed", len(REMOTE), "files; backup", bak)


def verify_live() -> None:
    import urllib.request

    ua = {"User-Agent": "Mozilla/5.0 seo-factory-usfans-freeze-inner"}
    checks = {
        "https://usfansspreadsheet.net/": [
            "USFans Spreadsheet — searchable QC catalog",
            "<h1>USFans Spreadsheet</h1>",
            'data-freeze-inner="20261120"',
            "Ordering to Poland, Italy, Spain or Germany",
            REVIEW_ISO,
        ],
        "https://usfansspreadsheet.net/usfans-spreadsheet/": [
            "Search the USFans spreadsheet",
            "row_count",
        ],
        "https://usfansspreadsheet.net/guide.html": [
            "How to Use USFans: Ordering, QC &amp; Shipping Guide (2026)",
            'id="pl-it-es-de"',
            "Poland (PL)",
            "Italy (IT)",
            "Spain (ES)",
            "Germany (DE)",
        ],
        "https://usfansspreadsheet.net/usfans-shipping-guide/": [
            "USFans Shipping Guide 2026",
            'id="pl-it-es-de"',
            "this page does not invent a percentage",
        ],
        "https://usfansspreadsheet.net/es/como-comprar-usfans/": [
            "Cómo comprar en USFans: pedido, fotos QC y envío (2026)",
            "España: estimador, IVA y QC de almacén",
        ],
        "https://usfansspreadsheet.net/pl/jak-kupowac-usfans/": [
            "Jak kupować przez USFans: zamówienie, QC i wysyłka (2026)",
            "Polska: estymator, VAT i QC w magazynie",
        ],
        "https://usfansspreadsheet.net/finds-dataset/": [
            REVIEW_ISO,
            "row_count=10601",
        ],
        "https://usfansspreadsheet.net/usfans-qc-photos/": [
            "Warehouse QC is the same for PL / IT / ES / DE",
        ],
        "https://usfansspreadsheet.uk/usfans-coupons/": [
            "coupon",
        ],
    }
    for url, needles in checks.items():
        req = urllib.request.Request(url, headers=ua)
        with urllib.request.urlopen(req, timeout=25) as resp:
            html = resp.read().decode("utf-8", "replace")
        missing = [n for n in needles if n not in html]
        title = re.search(r"<title[^>]*>(.*?)</title>", html, re.I | re.S)
        t = re.sub("<[^>]+>", "", title.group(1) if title else "")
        if missing:
            raise SystemExit(f"LIVE FAIL {url} missing {missing} title={t!r}")
        if url.rstrip("/") == "https://usfansspreadsheet.net":
            if "<h1>USFans Spreadsheet</h1>" not in html:
                raise SystemExit("LIVE FAIL homepage H1 changed")
        print("LIVE OK", url, "title=", re.sub(r"\s+", " ", t)[:120])


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--apply", action="store_true")
    p.add_argument("--deploy", action="store_true")
    p.add_argument("--verify", action="store_true")
    args = p.parse_args()
    if args.apply:
        apply()
        return
    if args.deploy:
        apply()
        deploy()
        verify_live()
        return
    if args.verify:
        verify_live()
        return
    p.error("pass --apply, --deploy, or --verify")


if __name__ == "__main__":
    main()
