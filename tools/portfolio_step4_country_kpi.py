#!/usr/bin/env python3
"""Step 4: country desks — local-intent home chrome + brand spreadsheet → primary hub.

Surgical patches on ranked Georgia homes (~40–50KB). Does NOT wholesale-replace
index.html with thinner desk overlays (DEPLOY GUARD from Steps 2–3).

Usage:
  python3 tools/portfolio_step4_country_kpi.py --dry-run
  python3 tools/portfolio_step4_country_kpi.py --write-repo
  python3 tools/portfolio_step4_country_kpi.py --apply-remote   # needs SSH env
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from desk_template import DEST_LOCAL, SKIP_CSS, customs_for  # noqa: E402

STORE_JSON = Path(
    "/cursor/stores/bc-eb8405c7-0d3c-48be-958d-5f25b92c606c/internal/portfolio-gsc/13_country_kpi.json"
)

# A/B country sites with clicks (Step 1 grades) + required list from assignment.
SITES: list[dict] = [
    {
        "host": "bbdbuy.it",
        "grade": "A",
        "brand": "BBDBuy",
        "dest": "IT",
        "loc": "it",
        "hub": "https://bbdbuyeu.net/",
        "hub_label": "BBDBuy spreadsheet hub",
        "title": "BBDBuy Italia — Poste Italiane, IVA e QC locale",
        "h1": "BBDBuy per un indirizzo in Italia",
        "desc": "Desk indipendente per l’Italia: CAP a cinque cifre, Poste Italiane, ADM/IVA, coupon e QC in italiano. Il termine globale «BBDBuy spreadsheet» vive sul hub.",
        "money": [
            "/",
            "/bbdbuy-shipping/",
            "/bbdbuy-coupons/",
            "/bbdbuy-qc/",
            "/is-bbdbuy-legit/",
            "/bbdbuy-spreadsheet/",
        ],
        "uplink": "Cerchi lo spreadsheet globale BBDBuy? Usa il <a href=\"https://bbdbuyeu.net/\">hub bbdbuyeu.net</a> — qui restano CAP italiano, Poste Italiane e dogana ADM.",
    },
    {
        "host": "fansbuy.co.uk",
        "grade": "A",
        "brand": "FansBuy",
        "dest": "GB",
        "loc": "en",
        "hub": "https://fansbuysheets.net/",
        "hub_label": "FansBuy spreadsheet hub",
        "title": "FansBuy UK — Royal Mail, HMRC & GBP desk",
        "h1": "FansBuy for a UK delivery address",
        "desc": "Independent UK desk: GB postcodes, Royal Mail last-mile, HMRC notes, coupons and QC. Global «FansBuy spreadsheet» queries belong on the primary hub.",
        "money": [
            "/",
            "/fansbuy-shipping-guide/",
            "/fansbuy-coupons/",
            "/fansbuy-qc-guide/",
            "/is-fansbuy-legit/",
            "/fansbuy-spreadsheet/",
        ],
        "uplink": "Looking for the global FansBuy spreadsheet? Use the <a href=\"https://fansbuysheets.net/\">fansbuysheets.net hub</a> — this desk covers UK postcodes, Royal Mail and HMRC.",
    },
    {
        "host": "hipobuyspreadsheet.nl",
        "grade": "A",
        "brand": "HipoBuy",
        "dest": "NL",
        "loc": "nl",
        "hub": "https://hipobuyspreadsheet.net/",
        "hub_label": "HipoBuy spreadsheet hub",
        "title": "HipoBuy Nederland — NL-postcode, Douane & verzending",
        "h1": "HipoBuy voor een Nederlands bezorgadres",
        "desc": "NL-desk: Nederlandse postcode (1234 AB), Douane/BTW, coupons en QC. Het globale «HipoBuy spreadsheet»-zoekwoord hoort op de primary hub.",
        "money": [
            "/",
            "/hipobuy-shipping-guide/",
            "/hipobuy-coupons/",
            "/hipobuy-qc-guide/",
            "/is-hipobuy-legit/",
            "/hipobuy-spreadsheet/",
        ],
        "uplink": "Zoek je de globale HipoBuy spreadsheet? Ga naar <a href=\"https://hipobuyspreadsheet.net/\">hipobuyspreadsheet.net</a> — hier blijven NL-postcode, Douane en lokale verzending.",
    },
    {
        "host": "mycnbox.nl",
        "grade": "A",
        "brand": "MyCNBox",
        "dest": "NL",
        "loc": "nl",
        "hub": "https://mycnbox.eu/",
        "hub_label": "MyCNBox spreadsheet hub",
        "title": "MyCNBox Nederland — Nederlandse postcode & Douane",
        "h1": "MyCNBox voor een Nederlands bezorgadres",
        "desc": "NL-desk voor MyCNBox: postcode 1234 AB, Douane, coupons/QC. Globale «MyCNBox spreadsheet»-intent → mycnbox.eu hub.",
        "money": [
            "/",
            "/mycnbox-shipping-guide/",
            "/mycnbox-coupons/",
            "/mycnbox-qc-guide/",
            "/is-mycnbox-legit/",
            "/mycnbox-spreadsheet/",
        ],
        "uplink": "Globale MyCNBox spreadsheet? Open <a href=\"https://mycnbox.eu/\">mycnbox.eu</a>. Deze host blijft de NL-hulp (postcode, Douane, coupons).",
    },
    {
        "host": "mycnbox.co.uk",
        "grade": "B",
        "brand": "MyCNBox",
        "dest": "GB",
        "loc": "en",
        "hub": "https://mycnbox.eu/",
        "hub_label": "MyCNBox spreadsheet hub",
        "title": "MyCNBox UK — GBP, Royal Mail, HMRC notes",
        "h1": "MyCNBox for a UK delivery address",
        "desc": "UK desk: GB postcodes, Royal Mail, HMRC. Global «MyCNBox spreadsheet» → mycnbox.eu.",
        "money": [
            "/",
            "/mycnbox-shipping-guide/",
            "/mycnbox-coupons/",
            "/mycnbox-qc-guide/",
            "/is-mycnbox-legit/",
            "/mycnbox-spreadsheet/",
        ],
        "uplink": "Global MyCNBox spreadsheet lives on <a href=\"https://mycnbox.eu/\">mycnbox.eu</a>. This desk is UK last-mile and HMRC only.",
    },
    {
        "host": "mycnbox.pl",
        "grade": "B",
        "brand": "MyCNBox",
        "dest": "PL",
        "loc": "en",  # Georgia chrome often EN; keep local fingerprint PL
        "hub": "https://mycnbox.eu/",
        "hub_label": "MyCNBox spreadsheet hub",
        "title": "MyCNBox Polska — 00-001 Warszawa, KAS, InPost",
        "h1": "MyCNBox for a Polish delivery address",
        "desc": "Poland desk: kod 00-001 Warszawa, KAS, local carriers. Global spreadsheet term → mycnbox.eu.",
        "money": [
            "/",
            "/mycnbox-shipping-guide/",
            "/mycnbox-coupons/",
            "/mycnbox-qc-guide/",
            "/is-mycnbox-legit/",
            "/mycnbox-spreadsheet/",
        ],
        "uplink": "Global MyCNBox spreadsheet → <a href=\"https://mycnbox.eu/\">mycnbox.eu</a>. Here: Polish postcode and KAS notes.",
    },
    {
        "host": "cssbuy.es",
        "grade": "B",
        "brand": "CSSBuy",
        "dest": "ES",
        "loc": "es",
        "hub": "https://cssbuyspreadsheet.eu/",
        "hub_label": "CSSBuy spreadsheet hub",
        "title": "CSSBuy España — Correos, AEAT y cupones",
        "h1": "CSSBuy para una dirección en España",
        "desc": "Desk ES: código postal de cinco dígitos, Correos, Agencia Tributaria, cupones/QC. La query global «CSSBuy spreadsheet» pertenece al hub .eu.",
        "money": [
            "/",
            "/cssbuy-shipping/",
            "/cssbuy-coupons/",
            "/is-cssbuy-legit/",
            "/cssbuy-spreadsheet/",
        ],
        "uplink": "¿Buscas el spreadsheet global de CSSBuy? Usa <a href=\"https://cssbuyspreadsheet.eu/\">cssbuyspreadsheet.eu</a>. Aquí: Correos, AEAT y cupones en español.",
    },
    {
        "host": "cssbuy.nl",
        "grade": "B",
        "brand": "CSSBuy",
        "dest": "NL",
        "loc": "nl",
        "hub": "https://cssbuyspreadsheet.eu/",
        "hub_label": "CSSBuy spreadsheet hub",
        "title": "CSSBuy Nederland — NL-postcode, Douane & coupons",
        "h1": "CSSBuy voor een Nederlands bezorgadres",
        "desc": "NL-desk: Nederlandse postcode, Douane, coupons. Globale «CSSBuy spreadsheet» → cssbuyspreadsheet.eu.",
        "money": [
            "/",
            "/cssbuy-shipping/",
            "/cssbuy-coupons/",
            "/cssbuy-spreadsheet/",
        ],
        "uplink": "Globale CSSBuy spreadsheet → <a href=\"https://cssbuyspreadsheet.eu/\">cssbuyspreadsheet.eu</a>. Deze host: NL-postcode en Douane.",
    },
    {
        "host": "lovegobuy.nl",
        "grade": "B",
        "brand": "LoveGoBuy",
        "dest": "NL",
        "loc": "nl",
        "hub": "https://lovegobuyguide.com/",
        "hub_label": "LoveGoBuy guide hub",
        "title": "LoveGoBuy Nederland — PostNL-lijnen en NL-postcode",
        "h1": "LoveGoBuy voor een Nederlands bezorgadres",
        "desc": "NL-desk: Nederlandse postcode, PostNL/DHL last-mile, Douane. Merk-gids/spreadsheet → lovegobuyguide.com.",
        "money": [
            "/",
            "/lovegobuy-shipping/",
            "/is-lovegobuy-legit/",
            "/lovegobuy-spreadsheet/",
        ],
        "uplink": "LoveGoBuy merk-gids / spreadsheet → <a href=\"https://lovegobuyguide.com/\">lovegobuyguide.com</a>. Hier: NL-postcode en verzending.",
    },
    {
        "host": "mulebuy.fr",
        "grade": "B",
        "brand": "MuleBuy",
        "dest": "FR",
        "loc": "fr",
        "hub": "https://bestmulebuysheets.com/",
        "hub_label": "MuleBuy spreadsheet hub",
        "title": "MuleBuy France — Colissimo, pas un code postal belge",
        "h1": "MuleBuy pour une adresse en France",
        "desc": "Desk FR: code postal à cinq chiffres, Colissimo, douane.gouv.fr, coupons. Le terme global «MuleBuy spreadsheet» → bestmulebuysheets.com.",
        "money": [
            "/",
            "/mulebuy-shipping/",
            "/mulebuy-coupons/",
            "/is-mulebuy-legit/",
            "/mulebuy-spreadsheet/",
        ],
        "uplink": "Spreadsheet global MuleBuy → <a href=\"https://bestmulebuysheets.com/\">bestmulebuysheets.com</a>. Ici: Colissimo et douane FR (pas un code postal belge).",
    },
    {
        "host": "bbdbuy.ca",
        "grade": "B",
        "brand": "BBDBuy",
        "dest": "CA",
        "loc": "en",
        "hub": "https://bbdbuyeu.net/",
        "hub_label": "BBDBuy spreadsheet hub",
        "title": "BBDBuy Canada — CBSA, postal form A1A 1A1",
        "h1": "BBDBuy for a Canadian delivery address",
        "desc": "Canada desk: postal form A1A 1A1, CBSA, local shipping notes. Global BBDBuy spreadsheet → bbdbuyeu.net.",
        "money": ["/", "/bbdbuy-shipping/"],
        "uplink": "Global BBDBuy spreadsheet → <a href=\"https://bbdbuyeu.net/\">bbdbuyeu.net</a>. This desk: Canadian postal codes and CBSA.",
    },
    {
        "host": "kakobuy.fi",
        "grade": "B",
        "brand": "Kakobuy",
        "dest": "FI",
        "loc": "en",
        "hub": "https://kakobuydocs.com/",
        "hub_label": "Kakobuy docs hub",
        "title": "Kakobuy Suomi — Posti, suomalainen postinumero",
        "h1": "Kakobuy for a Finnish delivery address",
        "desc": "Finland desk: suomalainen postinumero, Posti last-mile, Tulli notes. Brand spreadsheet queries should not be primary H1 here.",
        "money": ["/", "/kakobuy-shipping/"],
        "uplink": "Kakobuy brand / spreadsheet docs → <a href=\"https://kakobuydocs.com/\">kakobuydocs.com</a>. This host stays Finnish postcode / Posti / Tulli.",
        "fingerprint_override": "suomalainen postinumero",
        "fp_h2": "What applies today to a Finnish delivery address",
        "fp_steps": [
            ("Estimator destination: Finland", "Pick FI — not SE, not this hostname. A Swedish postnummer is the wrong country."),
            ("Address", "Finnish postcode (suomalainen postinumero), five digits."),
            ("Duties", "SKU decides. Posti can add a collect fee. Source: Tulli the morning you ship."),
            ("Last mile", "Often Posti. This desk does not invent a declared value for FI."),
        ],
        "customs_name": "Tulli",
        "customs_url": "https://tulli.fi/",
    },
    {
        "host": "litbuy.at",
        "grade": "B",
        "brand": "LitBuy",
        "dest": "AT",
        "loc": "de",
        "hub": "https://litbuyspreadsheetnow.com/",
        "hub_label": "LitBuy spreadsheet hub",
        "title": "LitBuy Österreich — 1010 Wien, BMF Zoll",
        "h1": "LitBuy für eine österreichische Adresse",
        "desc": "AT-Desk: vierstellige PLZ (1010 Wien), BMF Zoll, Österreichische Post. Globales «LitBuy Spreadsheet» → litbuyspreadsheetnow.com.",
        "money": ["/", "/litbuy-shipping/"],
        "uplink": "Globales LitBuy Spreadsheet → <a href=\"https://litbuyspreadsheetnow.com/\">litbuyspreadsheetnow.com</a>. Dieses Desk: 1010 Wien / BMF Zoll.",
    },
    {
        "host": "orientdig.es",
        "grade": "B",
        "brand": "OrientDig",
        "dest": "ES",
        "loc": "es",
        "hub": "https://orientdig.es/",
        "hub_label": "OrientDig ES desk",
        "title": "OrientDig España — Correos y Agencia Tributaria",
        "h1": "OrientDig para una dirección en España",
        "desc": "Desk ES country-only: Correos, AEAT, cupones locales. Sin H1 «OrientDig Spreadsheet» global.",
        "money": ["/", "/orientdig-shipping/"],
        "uplink": "OrientDig opera como desk ES: Correos + AEAT. No competir por un hub spreadsheet inexistente.",
        "skip_hub_link": True,
    },
    {
        "host": "hipobuyspreadsheet.co.uk",
        "grade": "B",
        "brand": "HipoBuy",
        "dest": "GB",
        "loc": "en",
        "hub": "https://hipobuyspreadsheet.net/",
        "hub_label": "HipoBuy spreadsheet hub",
        "title": "HipoBuy UK — Royal Mail & HMRC desk",
        "h1": "HipoBuy for a UK delivery address",
        "desc": "UK twin desk: GB postcodes, Royal Mail, HMRC. Global HipoBuy spreadsheet → hipobuyspreadsheet.net (not this TLD).",
        "money": ["/"],
        "uplink": "Global HipoBuy spreadsheet → <a href=\"https://hipobuyspreadsheet.net/\">hipobuyspreadsheet.net</a>. Twin UK desk keeps local framing only.",
    },
    {
        "host": "usfansspreadsheet.co.uk",
        "grade": "B",
        "brand": "USFans",
        "dest": "GB",
        "loc": "en",
        "hub": "https://usfansspreadsheet.net/",
        "hub_label": "USFans spreadsheet hub",
        "title": "USFans UK — Royal Mail & HMRC notes",
        "h1": "USFans for a UK delivery address",
        "desc": "UK desk (live twin): GB postcodes, Royal Mail, HMRC. Primary «USFans spreadsheet» → usfansspreadsheet.net. usfansspreadsheet.uk 301s here.",
        "money": ["/"],
        "uplink": "Primary USFans spreadsheet hub is <a href=\"https://usfansspreadsheet.net/\">usfansspreadsheet.net</a>. This UK twin is a landing assistant only.",
    },
    {
        "host": "usfansspreadsheet.uk",
        "grade": "B",
        "brand": "USFans",
        "dest": "GB",
        "loc": "en",
        "hub": "https://usfansspreadsheet.net/",
        "hub_label": "USFans spreadsheet hub",
        "title": "USFans UK — Royal Mail & HMRC notes",
        "h1": "USFans for a UK delivery address",
        "desc": "nginx 301 → usfansspreadsheet.co.uk; patch kept on disk for twin map. Live KPI measured on .co.uk.",
        "money": ["/"],
        "uplink": "301 twin: live content on <a href=\"https://usfansspreadsheet.co.uk/\">usfansspreadsheet.co.uk</a>; brand spreadsheet → usfansspreadsheet.net.",
        "deploy_note": "origin returns 301 to .co.uk",
    },
]


def _pack(site: dict) -> dict:
    if site.get("fingerprint_override"):
        return {
            "h2": site.get("fp_h2") or "Local delivery checks",
            "fingerprint": site["fingerprint_override"],
            "steps": site.get("fp_steps")
            or [
                ("Estimator destination", "Pick the correct country code."),
                ("Address", site["fingerprint_override"]),
                ("Duties", "Follow the official customs source the morning you ship."),
                ("Last mile", "Confirm the live carrier SKU."),
            ],
        }
    return DEST_LOCAL[site["dest"]]


def _customs(site: dict) -> tuple[str, str]:
    if site.get("customs_name"):
        return site["customs_name"], site.get("customs_url") or "#"
    return customs_for(site["dest"])


def local_block(site: dict) -> str:
    pack = _pack(site)
    cname, curl = _customs(site)
    steps = "".join(
        f"<li><strong>{escape(t)}</strong><span>{escape(b)}</span></li>"
        for t, b in pack["steps"]
    )
    money = " · ".join(
        f'<a href="{escape(p)}">{escape(p.rstrip("/") or "Home")}</a>' for p in site["money"][:6]
    )
    hub_p = ""
    if not site.get("skip_hub_link"):
        hub_p = f'<p class="hub-uplink" data-step4-hub="1">{site["uplink"]}</p>'
    else:
        hub_p = f'<p class="hub-uplink" data-step4-hub="1">{site["uplink"]}</p>'
    return f"""<!-- portfolio-step4-local -->
<section class="sg-sec" id="local" data-step4="1">
  <h2>{escape(pack["h2"])}</h2>
  <p class="ssub">{escape(site["host"])} · local-intent desk · not a second brand hub.</p>
  <ol class="local-steps">{steps}</ol>
  <p class="local-src">Official source: <a href="{escape(curl)}" rel="noopener">{escape(cname)}</a>. Lab 26 Oct 2026.</p>
  <p class="local-src">Money URLs (keep ≤6): {money}</p>
  {hub_p}
</section>
<!-- /portfolio-step4-local -->
"""


def ensure_css(html: str) -> str:
    if "portfolio-step4-local-css" in html:
        return html
    css = (
        "/* portfolio-step4-local-css */\n"
        + SKIP_CSS
        + ".hub-uplink{margin:14px 0 0;padding:12px 14px;border-left:3px solid #0f766e;"
        "background:#f0fdfa;color:#134e4a;line-height:1.6;font-size:15px;max-width:760px}"
        ".hub-uplink a{color:#0f766e;font-weight:600}\n"
    )
    if "</style>" in html:
        return html.replace("</style>", css + "</style>", 1)
    return html.replace("</head>", f"<style>{css}</style>\n</head>", 1)


def patch_html(html: str, site: dict) -> tuple[str, list[str]]:
    notes: list[str] = []
    pack = _pack(site)
    fp = pack["fingerprint"]

    # title
    new_html, n = re.subn(
        r"<title>[^<]*</title>",
        f"<title>{escape(site['title'])}</title>",
        html,
        count=1,
        flags=re.I,
    )
    if n:
        notes.append("title")
        html = new_html

    # meta description
    new_html, n = re.subn(
        r'(<meta\s+name=["\']description["\']\s+content=["\'])([^"\']*)(["\'])',
        lambda m: m.group(1) + site["desc"].replace('"', "&quot;") + m.group(3),
        html,
        count=1,
        flags=re.I,
    )
    if n:
        notes.append("meta-description")
        html = new_html

    # H1 — only first
    new_html, n = re.subn(
        r"(<h1[^>]*>)(.*?)(</h1>)",
        lambda m: m.group(1) + escape(site["h1"]) + m.group(3),
        html,
        count=1,
        flags=re.I | re.S,
    )
    if n:
        notes.append("h1")
        html = new_html

    # JSON-LD WebPage name if it still carries Spreadsheet hero
    def fix_ld(m: re.Match) -> str:
        block = m.group(0)
        if "Spreadsheet" in block and site["brand"] in block:
            block2 = re.sub(
                r'("name"\s*:\s*")([^"]*Spreadsheet[^"]*)(")',
                lambda mm: mm.group(1) + site["title"].replace('"', "") + mm.group(3),
                block,
                count=1,
            )
            return block2
        return block

    new_html, n = re.subn(
        r'<script type="application/ld\+json">\{[^{}]*"@type"\s*:\s*"WebPage"[^{}]*\}</script>',
        fix_ld,
        html,
        flags=re.I,
    )
    if n:
        notes.append("jsonld-webpage")
        html = new_html

    # inject / replace #local block BEFORE CSS (CSS marker must not collide)
    block = local_block(site)
    has_step4_block = "<!-- portfolio-step4-local -->" in html
    if has_step4_block:
        html = re.sub(
            r"<!-- portfolio-step4-local -->.*?<!-- /portfolio-step4-local -->",
            block,
            html,
            count=1,
            flags=re.S,
        )
        notes.append("local-refresh")
    elif re.search(r'id=["\']local["\']', html):
        if "data-step4-hub" not in html:
            html = re.sub(
                r'(id=["\']local["\'][\s\S]*?</section>)',
                lambda m: m.group(1)[:-10]
                + f'<p class="hub-uplink" data-step4-hub="1">{site["uplink"]}</p>\n</section>',
                html,
                count=1,
            )
            notes.append("hub-uplink-on-existing-local")
        if fp not in html:
            html = re.sub(
                r'(id=["\']local["\'][^>]*>)',
                r'\1\n  <p class="local-src" data-step4-fp="1">' + escape(fp) + "</p>",
                html,
                count=1,
            )
            notes.append("fingerprint-inject")
    else:
        m = re.search(r"</h1>\s*(?:<p class=\"lead\">.*?</p>\s*)?", html, re.I | re.S)
        if m:
            pos = m.end()
            html = html[:pos] + "\n" + block + "\n" + html[pos:]
            notes.append("local-inject-after-h1")
        elif "<main" in html.lower():
            html = re.sub(r"<main\b", block + "\n<main", html, count=1, flags=re.I)
            notes.append("local-inject-main")
        else:
            html = html.replace("</body>", block + "\n</body>", 1)
            notes.append("local-inject-body")

    html = ensure_css(html)

    if fp not in html and 'data-step4-hub="1">' in html:
        html = html.replace(
            'data-step4-hub="1">',
            f'data-step4-hub="1"><span data-fp="{escape(fp)}">{escape(fp)}. </span>',
            1,
        )
        notes.append("fingerprint-forced")
    elif fp not in html:
        # last resort: append fingerprint note near injected block
        html = html.replace(
            'data-step4="1">',
            f'data-step4="1"><p class="local-src" data-step4-fp="1">{escape(fp)}</p>',
            1,
        )
        notes.append("fingerprint-on-section")

    # soften residual primary H1-style "Brand Spreadsheet:" in og:title if present
    new_html, n = re.subn(
        r'(property=["\']og:title["\']\s+content=["\'])([^"\']*)(["\'])',
        lambda m: m.group(1) + site["title"].replace('"', "&quot;") + m.group(3),
        html,
        count=1,
        flags=re.I,
    )
    if n:
        notes.append("og:title")
        html = new_html

    return html, notes


def ssh_connect():
    import paramiko

    text = Path(
        "/cursor/stores/bc-eb8405c7-0d3c-48be-958d-5f25b92c606c/internal/usfans-ssh.env"
    ).read_text()
    host = None
    raw = None
    for line in text.splitlines():
        if line.startswith("HOST="):
            host = line.split("=", 1)[1].strip()
        if line.startswith("RAW_LINE="):
            raw = line.split("=", 1)[1]
    s = raw or ""
    if s.startswith("'"):
        s = s[1:]
    if s.endswith("'"):
        s = s[:-1]
    cands = [s, s.lstrip(";")]
    if ";" in s:
        parts = s.split(";")
        cands += [";".join(parts[1:]), parts[-1]]
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    for uname in ("root", "www", "ubuntu", "admin"):
        for pw in cands:
            if not pw:
                continue
            try:
                client.connect(
                    host,
                    username=uname,
                    password=pw,
                    timeout=15,
                    allow_agent=False,
                    look_for_keys=False,
                )
                return client
            except Exception:
                continue
    raise RuntimeError("SSH connect failed")


def remote_read(client, host: str) -> str | None:
    cmd = f"test -f /www/wwwroot/{host}/index.html && cat /www/wwwroot/{host}/index.html || true"
    _, stdout, _ = client.exec_command(cmd, timeout=60)
    data = stdout.read()
    return data.decode("utf-8", "replace") if data else None


def remote_write(client, host: str, html: str, backup_root: str) -> None:
    import hashlib

    sftp = client.open_sftp()
    remote = f"/www/wwwroot/{host}/index.html"
    # backup
    bak_dir = f"{backup_root}/{host}"
    client.exec_command(f"mkdir -p {bak_dir}", timeout=30)
    client.exec_command(f"cp -a {remote} {bak_dir}/index.html", timeout=30)
    tmp = f"/tmp/step4-{host}-{hashlib.sha1(host.encode()).hexdigest()[:8]}.html"
    with sftp.file(tmp, "w") as f:
        f.write(html)
    client.exec_command(f"mv {tmp} {remote} && chmod 644 {remote}", timeout=30)
    sftp.close()


def write_repo_artifacts(results: list[dict]) -> None:
    for r in results:
        host = r["host"]
        out_dir = ROOT / "sites" / host / "overlay"
        out_dir.mkdir(parents=True, exist_ok=True)
        if r.get("patched_html"):
            (out_dir / "index.html.step4-patched").write_text(r["patched_html"], encoding="utf-8")
        deploy = out_dir / "DEPLOY-STEP4.md"
        site = next(s for s in SITES if s["host"] == host)
        deploy.write_text(
            f"""# DEPLOY Step 4 — {host}

## Ownership
- Brand / global **spreadsheet** queries → `{site['hub']}`
- This country desk → local intent only (carrier, postcode, customs, local coupons/QC)

## Patch
Surgical on ranked Georgia `index.html` (title / H1 / meta / `#local` + hub uplink).
Do **not** wholesale overwrite with a thinner desk template.

## Money URLs (≤6)
{chr(10).join('- `' + p + '`' for p in site['money'])}

## Apply on Baota origin
```bash
# from backup + patched file in this overlay
cp /www/wwwroot/{host}/index.html /www/backup/portfolio-step4-YYYYMMDD/{host}/
cp sites/{host}/overlay/index.html.step4-patched /www/wwwroot/{host}/index.html
```

## Verify
curl -sL https://{host}/ | grep -E '<title>|<h1|id=\"local\"|hub-uplink|data-step4'
""",
            encoding="utf-8",
        )


def build_kpi_json(results: list[dict], backup: str | None) -> dict:
    return {
        "step": 4,
        "date": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
        "ownership_rule": {
            "brand_spreadsheet": "primary_hub_only",
            "country_desk": "local_intent_only",
            "local_signals": [
                "carrier",
                "postcode_format",
                "customs_authority",
                "local_language_coupons_qc",
            ],
        },
        "weekly_kpi": {
            "per_country": [
                "GSC clicks on money URLs (≤6)",
                "Share of queries with local tokens (carrier/postcode/customs/coupon-local)",
                "Share of queries matching brand+spreadsheet (should fall week-over-week)",
                "#local fingerprint still present (crawl check)",
                "Hub uplink click events or GSC impressions on hub from country referrals (optional)",
            ],
            "per_hub": [
                "Brand+spreadsheet query clicks + average position",
                "Homepage CTR for brand spreadsheet variants",
                "Country twin should not outrank hub on identical brand+spreadsheet head terms",
            ],
        },
        "backup": backup,
        "sites": [
            {
                "host": r["host"],
                "grade": r["grade"],
                "brand": r["brand"],
                "hub": r["hub"],
                "deploy": r["deploy"],
                "notes": r["notes"],
                "title": r["title"],
                "h1": r["h1"],
                "money": r["money"],
                "fingerprint": r["fingerprint"],
            }
            for r in results
        ],
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--write-repo", action="store_true")
    ap.add_argument("--apply-remote", action="store_true")
    ap.add_argument("--hosts", nargs="*", help="subset of hosts")
    args = ap.parse_args()

    sites = SITES
    if args.hosts:
        want = set(args.hosts)
        sites = [s for s in SITES if s["host"] in want]

    client = None
    backup = None
    if args.apply_remote:
        client = ssh_connect()
        stamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
        backup = f"/www/backup/portfolio-step4-{stamp}"
        client.exec_command(f"mkdir -p {backup}", timeout=30)

    results = []
    for site in sites:
        html = None
        source = "none"
        if client:
            html = remote_read(client, site["host"])
            source = "remote" if html else "missing-remote"
        if not html:
            live_base = ROOT / "sites" / site["host"] / "live-base" / "index.html"
            overlay = ROOT / "sites" / site["host"] / "overlay" / "index.html"
            for cand, label in ((live_base, "live-base"), (overlay, "overlay")):
                if cand.is_file():
                    html = cand.read_text(encoding="utf-8", errors="replace")
                    source = label
                    break
        if not html:
            results.append(
                {
                    **{k: site[k] for k in ("host", "grade", "brand", "hub", "title", "h1", "money")},
                    "deploy": "skip-no-html",
                    "notes": ["no-source"],
                    "fingerprint": _pack(site)["fingerprint"],
                    "patched_html": None,
                }
            )
            continue

        patched, notes = patch_html(html, site)
        deploy = "dry-run"
        if args.apply_remote and source == "remote":
            if not args.dry_run:
                remote_write(client, site["host"], patched, backup)
                deploy = "LIVE"
            else:
                deploy = "dry-remote"
        elif args.write_repo:
            deploy = "repo-artifact"
        results.append(
            {
                **{k: site[k] for k in ("host", "grade", "brand", "hub", "title", "h1", "money")},
                "deploy": deploy,
                "notes": notes + [f"source:{source}"],
                "fingerprint": _pack(site)["fingerprint"],
                "patched_html": patched,
            }
        )
        print(f"{site['host']}: {deploy} notes={notes} source={source}")

    if args.write_repo or args.apply_remote:
        write_repo_artifacts(results)
        payload = build_kpi_json(results, backup)
        STORE_JSON.parent.mkdir(parents=True, exist_ok=True)
        STORE_JSON.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print("wrote", STORE_JSON)

    if client:
        client.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
