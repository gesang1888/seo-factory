#!/usr/bin/env python3
"""Surgical patch for ranked NL HipoBuy shipping-guide wrap.

Keeps the 29 Sep 2026 NL lab table, volume widget, and Dutch customs copy.
Strips the leftover USA/UK calculator, fake DHL/EMS rate cards, and
duplicate English estimator paragraphs.

Does not overwrite this URL with leftover Spreadsheet 2026 or with
/hipobuy-freight/ CMS. Does not touch hipobuyspreadsheet.net.

Usage:
  python3 tools/patch_hipobuy_nl_shipping.py --self-test
  python3 tools/patch_hipobuy_nl_shipping.py --from-origin --write
  ORIGIN_SSH_PASS='...' python3 tools/patch_hipobuy_nl_shipping.py --deploy
"""
from __future__ import annotations

import argparse
import json
import os
import re
import ssl
import sys
import time
import urllib.request
from html import unescape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HOST = "hipobuyspreadsheet.nl"
ORIGIN_IP = "31.97.41.31"
REMOTE = f"/www/wwwroot/{HOST}/hipobuy-shipping-guide/index.html"
CANONICAL = f"https://{HOST}/hipobuy-shipping-guide/"
ORIGIN_URL = CANONICAL
SSH_HOST = os.environ.get("ORIGIN_SSH_HOST", "31.97.41.31")
SSH_USER = os.environ.get("ORIGIN_SSH_USER", "root")
OVERLAY = ROOT / "sites" / HOST / "overlay" / "hipobuy-shipping-guide" / "index.html"
PATCH_MARK = 'data-shipping-patch="20261020nl"'

KEEP_NEEDLES = (
    "NL AIR DHL-HIPO-EUCR1T",
    "$34.20",
    'id="lab-20260929"',
    'id="vol-calc"',
    "Btw en douane",
    "Geen onderwaardering",
    "No declared-value coaching",
    CANONICAL,
    "hipobuy-nl-desk.css",
    "/hipobuy-freight/",
)
GONE_NEEDLES = (
    "Template delivery grid",
    "All Hipobuy shipping lines",
    "Free Hipobuy shipping calculator",
    "Does Hipobuy ship to the USA",
    "A 700g parcel to the USA",
    'const RATES={"us"',
    "The generic USA/UK/AU/CA comparison",
    "wa.me/8615396628356",
    "i18n + currency engine",
    "5&ndash;8 days to USA",
    "Economy Line A",
)
DUTCH_ESTIMATOR = """\
<p class="pp" id="estimator-open"><a href="https://hipobuy.com/estimation">Open de officiële HipoBuy-estimator</a> met bestemming Nederland voordat je internationaal porto betaalt. De tabel hierboven is een snapshot van 29 sep 2026, geen kassa. USD-cijfers: de officiële valutaswitch verandert soms alleen het teken, niet het getal.</p>
"""

DUTCH_FAQ = [
    (
        "Hoeveel kost HipoBuy-verzending naar Nederland?",
        "Snapshot 29 sep 2026, zelfde dag, 1000 g en 35×25×10 cm, Clothes / common goods: goedkoopste lijn NL AIR DHL-HIPO-EUCR1T ongeveer $34.20 (10–16 dagen, 1100 g volume). China Post SURFACE was goedkoper op die meetdag maar 60–90 werkdagen. Dit is geen kassa — open de officiële estimator met bestemming Netherlands na magazijnfoto’s.",
    ),
    (
        "Waarom staat hier geen USA-rekenmachine?",
        "Deze desk is Nederland. De oude sjabloon (DHL Express naar USA, ~$38 / 700 g, plus USA/UK/AU/CA-grid) hoort niet op dit host. Porto staat in de officiële estimator; de widget hierboven rekent alleen volumgewicht.",
    ),
    (
        "Wat is volumgewicht?",
        "De meeste NL-luchtlijnen factureren max(echt gewicht, L×B×H/8000), vaak afgerond op 100 g. 35×25×10 cm is 8750 cm³ → ongeveer 1094 g volume → vaak 1100 g. Sommige EUB-SKU’s delen door 6000. Alleen meetkunde; het geld staat in de officiële estimator.",
    ),
    (
        "Wie betaalt invoer in Nederland?",
        "Dat volgt de geboekte lijn: Tax free, Prepaid Duty of Duties Payable by Recipient. Douane mag controleren. Bron: Belastingdienst Douane. Deze pagina verzint geen eurobedragen en geen aangegeven waarde. Geen onderwaardering.",
    ),
    (
        "Kan ik zendingen bundelen?",
        "Ja. Officiële statuspagina (eigen opname 30 sep 2026) noemt 90 dagen gratis opslag vanaf Stored — bevestig die tekst in de app op de ochtend van verzenden. Items gemarkeerd voor individuele verzending bundel je niet. PostNL of DHL moet op de live-SKU staan.",
    ),
    (
        "Waar klaag ik als iets misgaat?",
        "Alleen op hipobuy.com. hipobuyspreadsheet.nl is een onafhankelijke infosite: we zien je account niet, we innen geen porto en we openen geen ticket. Bewaar het in-app-nummer.",
    ),
]


def _faq_html() -> str:
    items = []
    svg = (
        '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" '
        'stroke-width="2"><polyline points="6 9 12 15 18 9"/></svg>'
    )
    for q, a in DUTCH_FAQ:
        items.append(
            f"""<div class="faq-item" itemscope itemprop="mainEntity" itemtype="https://schema.org/Question">
  <div class="faq-q" onclick="toggleFaq(this)" tabindex="0" onkeydown="if(event.key==='Enter')toggleFaq(this)" itemprop="name">{q}
    {svg}
  </div>
  <div class="faq-a" itemprop="acceptedAnswer" itemscope itemtype="https://schema.org/Answer">
    <div itemprop="text">{a}</div>
  </div>
</div>"""
        )
    return (
        '<h2 class="ph" id="calculator">Geen USA-rekenmachine op deze desk</h2>\n'
        '<p class="pp">De oude sjabloon (DHL Express naar USA, ~$38 / 700 g) is van deze pagina gehaald. '
        'Prijs voor Nederland staat in de <a href="https://hipobuy.com/estimation">officiële HipoBuy-estimator</a> '
        "met bestemming Netherlands. De widget hierboven rekent alleen volumgewicht, geen porto. "
        'CMS-zus: <a href="/hipobuy-freight/">/hipobuy-freight/</a>.</p>\n'
        '<h2 class="ph" id="faq">FAQ</h2>\n'
        '<div itemscope itemtype="https://schema.org/FAQPage">'
        + "\n".join(items)
        + "</div>\n"
    )


def _faq_jsonld() -> str:
    payload = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {
                "@type": "Question",
                "name": q,
                "acceptedAnswer": {"@type": "Answer", "text": a},
            }
            for q, a in DUTCH_FAQ
        ],
    }
    blob = json.dumps(payload, ensure_ascii=False, separators=(",", ":"))
    return f'<script type="application/ld+json">{blob}</script>\n'


TOGGLE_FAQ_JS = """\
<script>
function toggleFaq(el){
  var i=el.closest('.faq-item'), w=i.classList.contains('open');
  document.querySelectorAll('.faq-item').forEach(function(x){x.classList.remove('open');});
  if(!w) i.classList.add('open');
}
</script>
"""

DUP_EST_RE = re.compile(
    r'<p class="pp">The generic USA/UK/AU/CA comparison[\s\S]*?'
    r'(?=<h2 class="ph" id="douane">)',
    re.I,
)
CALC_RE = re.compile(
    r'<h2 class="ph" id="calculator">[\s\S]*?(?=</main>)',
    re.I,
)
WAF_RE = re.compile(
    r'<div class="waf">[\s\S]*?class="wafb"[\s\S]*?</a>\s*</div>\s*',
    re.I,
)
I18N_RE = re.compile(
    r"<script>\s*/\* ══ i18n \+ currency engine ══ \*/[\s\S]*?</script>\s*",
    re.I,
)
RATES_RE = re.compile(r"<script>\s*const RATES=\{[\s\S]*?</script>\s*", re.I)
DESC_RE = re.compile(
    r'(<meta name="description" content=")[^"]*(")',
    re.I,
)
OG_DESC_RE = re.compile(
    r'(<meta property="og:description" content=")[^"]*(")',
    re.I,
)
NEW_DESC = (
    "HipoBuy verzendkosten naar Nederland: officiële estimator-snapshot "
    "29 sep 2026 voor 1000 g / 35×25×10 cm plus volumgewicht. Alleen uitleg, geen kassa."
)


def fetch_origin() -> str:
    """Pull origin HTML (Baota) so Cloudflare email-obfuscation is not baked in."""
    import subprocess

    cmd = [
        "curl",
        "-fsS",
        "--resolve",
        f"{HOST}:443:{ORIGIN_IP}",
        "-k",
        "-H",
        f"Host: {HOST}",
        "-H",
        "User-Agent: hipobuy-nl-shipping-patch/20261020",
        ORIGIN_URL,
    ]
    try:
        return subprocess.check_output(cmd, timeout=30).decode("utf-8", "replace")
    except (subprocess.CalledProcessError, FileNotFoundError):
        ctx = ssl.create_default_context()
        req = urllib.request.Request(
            ORIGIN_URL,
            headers={"User-Agent": "hipobuy-nl-shipping-patch/20261020"},
        )
        with urllib.request.urlopen(req, timeout=30, context=ctx) as resp:
            return resp.read().decode("utf-8", "replace")


def patch_html(html: str) -> tuple[str, bool]:
    if PATCH_MARK in html and "Geen USA-rekenmachine op deze desk" in html:
        return html, False
    if "hipobuyspreadsheet.net" in html and HOST not in html:
        raise ValueError("refusing to patch .net hub HTML")
    if CANONICAL not in html:
        raise ValueError("canonical missing — not the ranked NL wrap")
    if 'id="lab-20260929"' not in html or "NL AIR DHL-HIPO-EUCR1T" not in html:
        raise ValueError("NL lab table missing — abort rather than smash keep copy")

    out = html
    if PATCH_MARK not in out:
        out = out.replace(
            "<body ",
            f"<body {PATCH_MARK} ",
            1,
        )
        if PATCH_MARK not in out:
            out = out.replace(
                "<body>",
                f"<body {PATCH_MARK}>",
                1,
            )

    out, n_dup = DUP_EST_RE.subn(DUTCH_ESTIMATOR, out, count=1)
    if n_dup != 1:
        raise ValueError(f"duplicate estimator block count={n_dup}")

    out, n_calc = CALC_RE.subn(_faq_html(), out, count=1)
    if n_calc != 1:
        raise ValueError(f"USA calculator block count={n_calc}")

    out, n_waf = WAF_RE.subn("", out)
    out, n_i18n = I18N_RE.subn("", out)
    out, n_rates = RATES_RE.subn("", out)
    if n_waf < 1 or n_i18n != 1 or n_rates != 1:
        raise ValueError(f"leftover js counts waf={n_waf} i18n={n_i18n} rates={n_rates}")

    if "function toggleFaq" not in out:
        out = out.replace("</body>", TOGGLE_FAQ_JS + "</body>", 1)

    if 'type="application/ld+json"' in out and '"@type":"FAQPage"' not in out:
        out = out.replace(
            "</head>",
            _faq_jsonld() + "</head>",
            1,
        )

    out, n_desc = DESC_RE.subn(rf"\1{NEW_DESC}\2", out, count=1)
    if n_desc != 1:
        raise ValueError("description meta missing")
    out, n_og = OG_DESC_RE.subn(rf"\1{NEW_DESC}\2", out, count=1)
    if n_og != 1:
        raise ValueError("og:description missing")

    # Drop leftover English calc heading if the regex left a stray copy.
    if "Free Hipobuy shipping calculator" in out:
        raise ValueError("calculator heading still present")
    return out, True


def assert_ok(html: str) -> None:
    missing = [n for n in KEEP_NEEDLES if n not in html]
    leftover = [n for n in GONE_NEEDLES if n in html]
    if missing:
        raise AssertionError(f"keep missing: {missing}")
    if leftover:
        raise AssertionError(f"poison still present: {leftover}")
    if PATCH_MARK not in html:
        raise AssertionError("patch marker missing")
    if html.lower().count("open the official hipobuy estimator") > 0:
        raise AssertionError("English estimator spam still present")
    if html.count("https://hipobuy.com/estimation") > 6:
        raise AssertionError("too many estimator links")
    if '"@type":"FAQPage"' not in html:
        raise AssertionError("FAQ JSON-LD missing")
    # Visible FAQs must parse as JSON-LD.
    blocks = re.findall(
        r'<script[^>]*type=["\']application/ld\+json["\'][^>]*>(.*?)</script>',
        html,
        re.I | re.S,
    )
    faq = None
    for raw in blocks:
        obj = json.loads(unescape(raw.strip()))
        if obj.get("@type") == "FAQPage":
            faq = obj
    if not faq or len(faq.get("mainEntity") or []) != len(DUTCH_FAQ):
        raise AssertionError("FAQ JSON-LD question count mismatch")
    if len(html) < 8000:
        raise AssertionError(f"patched HTML too thin ({len(html)} bytes)")
    if "onderwaardering" not in html.lower() and "declared-value" not in html.lower():
        raise AssertionError("customs education missing")


def _synthetic_origin() -> str:
    return f"""<!DOCTYPE html>
<html lang="nl-NL"><head>
<title>HipoBuy verzendkosten naar Nederland — lab 29 Sep 2026</title>
<meta name="description" content="HipoBuy shipping to Nederland: official estimator snapshot 29 Sep 2026 for 1000 g / 35×25×10 cm plus the on-page calculator. Educational customs notes only.">
<meta property="og:description" content="HipoBuy shipping to Nederland: official estimator snapshot 29 Sep 2026 for 1000 g / 35×25×10 cm plus the on-page calculator. Educational customs notes only.">
<link rel="canonical" href="{CANONICAL}">
<link rel="stylesheet" href="/assets/css/hipobuy-nl-desk.css?v=20261006h">
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"Article","url":"{CANONICAL}"}}</script>
</head>
<body data-inner-chrome="20261006h-hipobuy-nl">
<main id="main">
<aside>Official HipoBuy estimator · 29 Sep 2026. Goedkoopste lijn NL AIR DHL-HIPO-EUCR1T ongeveer $34.20. <strong>No declared-value coaching.</strong></aside>
<div class="tw hipo-lab" id="lab-20260929"><table><tr><td><code>NL AIR DHL-HIPO-EUCR1T</code></td><td class="mv">$34.20</td></tr></table></div>
<p class="pp">The generic USA/UK/AU/CA comparison further down is a template leftover. Use the 29 Sep 2026 table above for Nederland.</p>
<p class="pp"><a href="https://hipobuy.com/estimation">Open the official HipoBuy estimator</a> with this country selected before you pay international freight. The table above is a snapshot from 29 Sep 2026, not checkout. USD digits stay dollars when the official selector only changes the symbol.</p>
<p class="pp"><a href="https://hipobuy.com/estimation">Open the official HipoBuy estimator</a> with this country selected before you pay international freight. The table above is a snapshot from 29 Sep 2026, not checkout. USD digits stay dollars when the official selector only changes the symbol.</p>
<h2 class="ph" id="douane">Btw en douane — drie modi, alleen uitleg</h2>
<p class="pp"><strong>Geen onderwaardering.</strong></p>
<div class="vol" id="vol-calc">Volumgewicht berekenen (geen prijs)</div>
<h2 class="ph" id="calculator">Free Hipobuy shipping calculator</h2>
  <div class="calc" id="calc"><div class="cres" id="cres"></div>
  <h2 class="ph">All Hipobuy shipping lines</h2>
  <p class="lt">5&ndash;8 days to USA</p>
  <h2 class="ph">Template delivery grid (USA/UK/AU/CA — not the lab above)</h2>
  <h2 class="ph">FAQ</h2>
  <div itemscope itemtype="https://schema.org/FAQPage"><div class="faq-item" itemscope itemprop="mainEntity" itemtype="https://schema.org/Question">
  <div class="faq-q">Does Hipobuy ship to the USA?</div>
  <div class="faq-a" itemprop="acceptedAnswer" itemscope itemtype="https://schema.org/Answer">
    <div itemprop="text">A 700g parcel to the USA costs approximately $11&ndash;16 via economy.</div>
  </div>
</div></div>
</main>
<footer><a href="/hipobuy-freight/">Verzending en douane</a>
<a href="https://hipobuy.com/estimation">schatter</a></footer>
<script>(function(){{var b=document.querySelector('.burger');}})();</script>
<div class="waf">
  <div class="wabu"><b>Need help?</b><span>Chat on WhatsApp</span></div>
  <a href="https://wa.me/8615396628356" class="wafb">wa</a>
</div>
<script>
/* ══ i18n + currency engine ══ */
const LANGS=[];
function toggleFaq(el){{}}
</script>
<script>
const RATES={{"us": {{"dhl": [38, 8.0], "ems": [24, 4.8], "ecoA": [16, 3.0], "ecoB": [11, 1.9]}}}};
function cu(){{}}
</script>
</body></html>
"""


def self_test() -> None:
    raw = _synthetic_origin()
    patched, changed = patch_html(raw)
    assert changed, "synthetic should change"
    assert_ok(patched)
    again, changed2 = patch_html(patched)
    assert not changed2 and again == patched, "idempotent"
    # Refuse .net smash
    try:
        patch_html(raw.replace(CANONICAL, "https://hipobuyspreadsheet.net/").replace(HOST, "example.com"))
        raise AssertionError("should refuse foreign canonical")
    except ValueError:
        pass
    print("self-test ok", len(patched))


def write_overlay(html: str) -> Path:
    OVERLAY.parent.mkdir(parents=True, exist_ok=True)
    OVERLAY.write_text(html, encoding="utf-8")
    return OVERLAY


def _connect():
    try:
        import paramiko
    except ImportError:
        import subprocess

        subprocess.check_call([sys.executable, "-m", "pip", "install", "paramiko", "-q"])
        import paramiko

    password = (
        os.environ.get("ORIGIN_SSH_PASS")
        or os.environ.get("HIPOBAY_DEPLOY_PASS")
        or os.environ.get("LITBUY_DEPLOY_PASS")
    )
    if not password:
        raise SystemExit("Set ORIGIN_SSH_PASS")
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(SSH_HOST, username=SSH_USER, password=password, timeout=30)
    return client


def _run(client, cmd: str, timeout: int = 60) -> str:
    _, stdout, stderr = client.exec_command(cmd, timeout=timeout)
    return (stdout.read() + stderr.read()).decode(errors="replace").strip()


def deploy(html: str) -> None:
    if "hipobuyspreadsheet.net" in REMOTE:
        raise SystemExit("refusing .net PUT")
    client = _connect()
    sftp = client.open_sftp()
    stamp = time.strftime("%Y%m%d-%H%M%S")
    bak = f"/www/backup/hipobuy-nl-shipping-{stamp}/index.html"
    _run(client, f"mkdir -p '{Path(bak).parent}'")
    try:
        sftp.stat(REMOTE)
        _run(client, f"cp -a '{REMOTE}' '{bak}'")
        print("backup", bak)
    except FileNotFoundError:
        print("no prior file", REMOTE)
    tmp = Path("/tmp/hipobuy-nl-shipping-patched.html")
    tmp.write_text(html, encoding="utf-8")
    sftp.put(str(tmp), REMOTE)
    _run(client, f"chown www:www '{REMOTE}' && chmod 644 '{REMOTE}'")
    print("PUT", REMOTE, len(html))
    sftp.close()
    client.close()


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--self-test", action="store_true")
    ap.add_argument("--file", type=Path)
    ap.add_argument("--from-origin", action="store_true")
    ap.add_argument("--write", action="store_true")
    ap.add_argument("--deploy", action="store_true")
    args = ap.parse_args()
    if args.self_test:
        self_test()
        return
    if args.file:
        raw = args.file.read_text(encoding="utf-8")
    elif args.from_origin or args.deploy:
        raw = fetch_origin()
    else:
        raise SystemExit("pass --self-test, --file, or --from-origin")
    patched, changed = patch_html(raw)
    assert_ok(patched)
    print("changed", changed, "bytes", len(patched))
    if args.write:
        path = write_overlay(patched)
        print("wrote", path)
    if args.deploy:
        deploy(patched)


if __name__ == "__main__":
    main()
