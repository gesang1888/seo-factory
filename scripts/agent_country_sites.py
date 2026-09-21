#!/usr/bin/env python3
"""Split the 161-site panel by shopping-agent, and make country TLDs independent.

Rules (August 2026 spam-update):
- Different agents never 301 to each other or to w2clinks.com.
- Same agent, different countries stay up as local sites (unique copy, language,
  last-mile carrier). They are not doorways onto one canonical ccTLD.
- 410 thin clones and the w2cclothes/w2cshoes identical twins stay as they are.
"""

from __future__ import annotations

import argparse
import html
import json
import os
import re
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from spam_update_p0 import Baota  # noqa: E402

INV_PATH = ROOT / "scripts" / "agent_country_inventory.json"

GONE_410 = {
    "bestmulebuysheets.com",
    "dgobuyspreadsheet.com",
    "esgobuyspreadsheet.net",
    "fsbuyspreadsheet.org",
    "hoospreadsheet.net",
    "joyagoospreadsheets.de",
    "pantherbuy.net",
    "rizzitgospreadsheets.net",
    "shipzobuyspreadsheet.net",
    "tigspreadsheet.com",
    "vigorspreadsheet.com",
}
KEEP_AS_IS = {
    "allchina-buy.com",
    "bbdbuyeu.net",
    "w2clinks.com",
    "w2crep.org",
    "w2cclothes.com",
    "w2cshoes.com",
    "repsicon.com",
} | set(
    json.loads((ROOT / "scripts" / "spam_update_p0_inventory.json").read_text())["indie"].get(
        "independent_agents", []
    )
)

AGENT_PATTERNS = [
    ("bbdbuyeu", "BBDBuyEU"),
    ("allchinabuy", "AllChinaBuy"),
    ("usfans", "USFans"),
    ("fansbuy", "FansBuy"),
    ("kakobuy", "KakoBuy"),
    ("lovegobuy", "LoveGoBuy"),
    ("orientdig", "OrientDig"),
    ("cssbuy", "CSSBuy"),
    ("sugargoo", "SugarGoo"),
    ("hipobuy", "HipoBuy"),
    ("ootdbuy", "OOTDBuy"),
    ("mycnbox", "MyCNBox"),
    ("superbuy", "Superbuy"),
    ("mulebuy", "MuleBuy"),
    ("hubbuy", "HubBuy"),
    ("wemimi", "WeMimi"),
    ("fashionreps", "FashionReps"),
    ("cnshopper", "CNShopper"),
    ("oopbuy", "OOPBuy"),
    ("basetao", "BaseTao"),
    ("acbuy", "ACBuy"),
    ("bbdbuy", "BBDBuy"),
    ("litbuy", "LitBuy"),
    ("kako", "KakoBuy"),
    ("fans", "FansBuy"),
    ("lit", "LitBuy"),
]

CC_FROM_HOST = [
    (".co.uk", "UK"),
    (".me.uk", "UK"),
    (".uk", "UK"),
    (".us", "US"),
    (".ca", "CA"),
    (".nl", "NL"),
    (".de", "DE"),
    (".fr", "FR"),
    (".es", "ES"),
    (".it", "IT"),
    (".at", "AT"),
    (".au", "AU"),
    (".fi", "FI"),
    (".pl", "PL"),
    (".eu", "EU"),
]

COUNTRIES = {
    "UK": {
        "lang": "en",
        "locale": "en-GB",
        "currency": "GBP",
        "carrier": "Royal Mail",
        "label": "United Kingdom",
        "hook": "Quote after packed kg, then pick a line that actually hands off to Royal Mail or a tax-prepaid product — not a screenshot from a US blog.",
        "customs": "UK import rules and any VAT/duty are set by HMRC and the carrier product you buy. This page does not pick a declared value for you.",
    },
    "US": {
        "lang": "en",
        "locale": "en-US",
        "currency": "USD",
        "carrier": "USPS",
        "label": "United States",
        "hook": "US last-mile is usually USPS or a commercial integrator. Volumetric shoe boxes punish cheap lines harder than a 500 g T-shirt haul.",
        "customs": "US customs treatment depends on the line and the shipment facts. Follow CBP and the carrier — no under-declaration coaching here.",
    },
    "CA": {
        "lang": "en",
        "locale": "en-CA",
        "currency": "CAD",
        "carrier": "Canada Post",
        "label": "Canada",
        "hook": "CAD budgeting and Canada Post last-mile change which agent line is sane. Do not reuse a US quote.",
        "customs": "CBSA processes commercial import on the product you selected. Read the live agent quote, not a US duty meme.",
    },
    "NL": {
        "lang": "nl",
        "locale": "nl-NL",
        "currency": "EUR",
        "carrier": "PostNL",
        "label": "Netherlands",
        "hook": "Nederlandse hauls landen vaak via PostNL of een fiscale EU-lijn. Een UK-quote is hier niks waard.",
        "customs": "Btw/invoer volgt het product dat de agent verkoopt (fiscalcleared of niet). Dit is geen advies om lager aan te geven.",
        "en_hook": "Dutch hauls usually terminate on PostNL or a fiscal EU product. A UK quote is useless here.",
    },
    "DE": {
        "lang": "de",
        "locale": "de-DE",
        "currency": "EUR",
        "carrier": "DHL",
        "label": "Germany",
        "hook": "Deutsche Sendungen enden oft bei DHL. Wähle die Linie nach Steuerprodukt und Volumen, nicht nach einem US-Screenshot.",
        "customs": "Einfuhr/USt hängen vom gebuchten Produkt ab. Keine Unterdeklaration auf dieser Seite.",
        "en_hook": "German parcels often terminate at DHL. Pick the line by tax product and volume.",
    },
    "FR": {
        "lang": "fr",
        "locale": "fr-FR",
        "currency": "EUR",
        "carrier": "Colissimo",
        "label": "France",
        "hook": "En France, Colissimo / Colis Exo et les lignes fiscales UE ne se comparent pas à un tarif US.",
        "customs": "TVA et formalités suivent le produit transporteur. Pas de sous-déclaration ici.",
        "en_hook": "French last-mile (Colissimo-class) and EU fiscal lines are not a US rate card.",
    },
    "ES": {
        "lang": "es",
        "locale": "es-ES",
        "currency": "EUR",
        "carrier": "Correos",
        "label": "Spain",
        "hook": "En España el tramo final suele ser Correos. No copies un presupuesto de Alemania.",
        "customs": "IVA/aduanas dependen del producto contratado. Esta guía no elige un valor declarado.",
        "en_hook": "Spanish last-mile is often Correos. Do not copy a German quote.",
    },
    "IT": {
        "lang": "it",
        "locale": "it-IT",
        "currency": "EUR",
        "carrier": "Poste Italiane",
        "label": "Italy",
        "hook": "In Italia l’ultimo miglio è spesso Poste. Le linee fiscali UE non sono un listino USA.",
        "customs": "IVA e dogana seguono il prodotto spedizioniere. Nessuna sotto-dichiarazione.",
        "en_hook": "Italian last-mile is often Poste. EU fiscal lines are not a US price list.",
    },
    "AT": {
        "lang": "de",
        "locale": "de-AT",
        "currency": "EUR",
        "carrier": "Österreichische Post",
        "label": "Austria",
        "hook": "Österreich ist nicht Deutschland: anderes Last-Mile-Produkt, anderer Quote-Screen.",
        "customs": "Einfuhr folgt dem gebuchten Produkt. Keine Unterdeklaration.",
        "en_hook": "Austria is not Germany — different last-mile product, different quote.",
    },
    "AU": {
        "lang": "en",
        "locale": "en-AU",
        "currency": "AUD",
        "carrier": "Australia Post",
        "label": "Australia",
        "hook": "AUD and Australia Post transit kill lines that look cheap on a US calculator.",
        "customs": "ABF processes the shipment as booked. This page does not set a declared value.",
    },
    "FI": {
        "lang": "fi",
        "locale": "fi-FI",
        "currency": "EUR",
        "carrier": "Posti",
        "label": "Finland",
        "hook": "Suomessa viimeinen kilometri on usein Posti. Älä käytä Saksan hintaa.",
        "customs": "ALV/tulli seuraa valittua tuotetta. Ei aliarvostusohjeita.",
        "en_hook": "Finnish last-mile is often Posti. Do not reuse a German price.",
    },
    "PL": {
        "lang": "pl",
        "locale": "pl-PL",
        "currency": "PLN",
        "carrier": "InPost / Poczta Polska",
        "label": "Poland",
        "hook": "W Polsce last mile to często InPost albo Poczta. Cennik DE tu nie działa.",
        "customs": "VAT/odprawa zależy od produktu. Zero uczenia zaniżania wartości.",
        "en_hook": "Polish last-mile is often InPost or Poczta. A DE rate card does not apply.",
    },
    "EU": {
        "lang": "en",
        "locale": "en",
        "currency": "EUR",
        "carrier": "EU fiscal / local post",
        "label": "European Union",
        "hook": "An .eu hub is for fiscal-line shopping across member states — not a clone of the US page with the TLD swapped.",
        "customs": "IOSS/fiscal products are still specific SKUs in the agent app. Read that SKU.",
    },
    "GLOBAL": {
        "lang": "en",
        "locale": "en",
        "currency": "USD",
        "carrier": "agent line card",
        "label": "global",
        "hook": "This hostname is the global desk for the agent, not a doorway onto a country TLD.",
        "customs": "Use the destination your account actually ships to. No declared-value coaching.",
    },
}

AGENT_META = {
    "CSSBuy": {"register": "https://www.cssbuy.com/", "accent": "#0f766e", "pitch": "CSSBuy line cards and warehouse photos — local last-mile, not a shared mall."},
    "OrientDig": {"register": "https://orientdig.com/register", "accent": "#7c3aed", "pitch": "OrientDig agent workflow for this country only. No sister-ccTLD funnel."},
    "BBDBuy": {"register": "https://www.bbdbuy.com/", "accent": "#b45309", "pitch": "BBDBuy country desk. Not BBDBuyEU, not a W2C clone."},
    "BBDBuyEU": {"register": "https://www.bbdbuyeu.com/", "accent": "#1d4ed8", "pitch": "BBDBuyEU is the EU checkout brand — keep it off BBDBuy country domains."},
    "AllChinaBuy": {"register": "https://www.allchinabuy.com/", "accent": "#be123c", "pitch": "AllChinaBuy local shipping notes. ACBuy country domains stay on the ACBuy agent."},
    "ACBuy": {"register": "https://www.acbuy.com/", "accent": "#9f1239", "pitch": "ACBuy country hub. Do not swap AllChinaBuy HTML onto this host."},
    "SugarGoo": {"register": "https://www.sugargoo.com/", "accent": "#ea580c", "pitch": "SugarGoo warehouse and lines for this destination."},
    "LitBuy": {"register": "https://www.litbuy.com/", "accent": "#365314", "pitch": "LitBuy country notebook — last-mile first."},
    "LoveGoBuy": {"register": "https://www.lovegobuy.com/", "accent": "#9d174d", "pitch": "LoveGoBuy for this country’s quote screen only."},
    "HipoBuy": {"register": "https://www.hipobuy.com/", "accent": "#0e7490", "pitch": "HipoBuy local parcel math, not a review-site clone."},
    "OOTDBuy": {"register": "https://www.ootdbuy.com/", "accent": "#a21caf", "pitch": "OOTDBuy destination guide. .org/.net globals are not this country."},
    "MyCNBox": {"register": "https://www.mycnbox.com/", "accent": "#1e3a8a", "pitch": "MyCNBox last-mile for this country. Haul.com stays the haul SOP."},
    "USFans": {"register": "https://www.usfans.com/", "accent": "#b91c1c", "pitch": "USFans country spreadsheet — UK/NL/US are separate documents."},
    "FansBuy": {"register": "https://www.fansbuy.com/", "accent": "#9f1239", "pitch": "FansBuy is not USFans. Keep the brands and the countries apart."},
    "KakoBuy": {"register": "https://www.kakobuy.com/", "accent": "#0369a1", "pitch": "KakoBuy country desk (FI/CA/ES/FR/NL). Docs/tips hosts are operator manuals."},
    "Superbuy": {"register": "https://www.superbuy.com/", "accent": "#c2410c", "pitch": "Superbuy country spreadsheet, not a generic agent skin."},
    "MuleBuy": {"register": "https://www.mulebuy.com/", "accent": "#44403c", "pitch": "MuleBuy country notes. The .org thin twin stays gone."},
    "HubBuy": {"register": "https://www.hubbuy.com/", "accent": "#115e59", "pitch": "HubBuy operations vs spreadsheet host — two jobs if both exist."},
    "WeMimi": {"register": "https://www.wemimi.com/", "accent": "#6d28d9", "pitch": "WeMimi country/global desk."},
    "FashionReps": {"register": "/", "accent": "#111827", "pitch": "FashionReps finds commentary — not another shopping-agent doorway."},
    "CNShopper": {"register": "https://www.cnshopper.com/", "accent": "#1f2937", "pitch": "CNShopper local notes."},
    "OOPBuy": {"register": "https://www.oopbuy.com/", "accent": "#92400e", "pitch": "OOPBuy Italy desk."},
    "BaseTao": {"register": "https://www.basetao.com/", "accent": "#1e40af", "pitch": "BaseTao global spreadsheet."},
    "UNKNOWN": {"register": "/", "accent": "#334155", "pitch": "Independent host — do not 301 it onto another agent."},
}


def esc(s: str) -> str:
    return html.escape(s, quote=True)


def classify_host(host: str) -> dict:
    agent = "UNKNOWN"
    for needle, name in AGENT_PATTERNS:
        if needle in host.replace("-", ""):
            # allchina-buy.com contains allchina not allchinabuy after hyphen strip? 
            agent = name
            break
    # hyphenated brands
    compact = host.replace("-", "")
    if agent == "UNKNOWN":
        for needle, name in AGENT_PATTERNS:
            if needle in compact:
                agent = name
                break
    if "allchina" in compact:
        agent = "AllChinaBuy"
    country = "GLOBAL"
    for suffix, cc in CC_FROM_HOST:
        if host.endswith(suffix):
            country = cc
            break
    status = "live"
    if host in GONE_410:
        status = "410"
    elif host in KEEP_AS_IS:
        status = "keep"
    return {"host": host, "agent": agent, "country": country, "status": status}


def build_inventory(hosts: list[str]) -> dict:
    rows = [classify_host(h) for h in hosts]
    by_agent: dict[str, dict[str, list[str]]] = defaultdict(lambda: defaultdict(list))
    for r in rows:
        by_agent[r["agent"]][r["country"]].append(r["host"])
    return {
        "policy": "One agent family per cluster. Country TLDs stay independent local sites. Do not 301 UK/NL/DE onto a .net/.us doorway.",
        "sites": rows,
        "by_agent": {a: dict(c) for a, c in sorted(by_agent.items())},
    }


def page_html(row: dict) -> str:
    cc = COUNTRIES[row["country"]]
    meta = AGENT_META.get(row["agent"], AGENT_META["UNKNOWN"])
    lang = cc["lang"]
    role = "spreadsheet desk" if "spreadsheet" in row["host"] else "agent desk"
    title = f"{row['agent']} {cc['label']} {role} — {cc['carrier']}"
    h1 = f"{row['agent']} {role} for {cc['label']} ({cc['currency']})"
    hook = cc.get("hook") or cc.get("en_hook")
    body_en = cc.get("en_hook")
    return f"""<!doctype html>
<html lang="{esc(lang)}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(meta['pitch'] + ' ' + hook)[:170]}">
<link rel="canonical" href="https://{esc(row['host'])}/">
<meta name="robots" content="index,follow">
<style>
:root {{ --accent:{meta['accent']}; }}
body {{ margin:0; font-family: Georgia, ui-serif, serif; background:#f7f5f0; color:#1c1917; line-height:1.55; }}
header,main,footer {{ max-width:44rem; margin:0 auto; padding:1.2rem; }}
a.cta {{ display:inline-block; background:var(--accent); color:#fff; text-decoration:none; padding:.7rem 1rem; border-radius:.6rem; }}
.note {{ color:#57534e; font-size:.92rem; }}
h1 {{ font-size:clamp(1.6rem,4vw,2.2rem); }}
</style>
<script type="application/ld+json">{json.dumps({
    "@context": "https://schema.org",
    "@type": "WebPage",
    "name": title,
    "inLanguage": cc["locale"],
    "about": row["agent"],
    "url": f"https://{row['host']}/",
}, ensure_ascii=False)}</script>
</head>
<body>
<header>
  <p class="note">{esc(row['agent'])} · {esc(cc['label'])} · {esc(row['host'])}</p>
</header>
<main>
  <h1>{esc(h1)}</h1>
  <p>{esc(meta['pitch'])}</p>
  <p>{esc(hook)}</p>
  {f'<p lang="en">{esc(body_en)}</p>' if body_en and lang != 'en' else ''}
  <p>{esc(cc['customs'])}</p>
  <p>Packed weight inside {esc(row['agent'])} is the only honest input. Sister country domains of {esc(row['agent'])} are other local desks — they are not this URL.</p>
  {f'<p><a class="cta" href="{esc(meta["register"])}">Open {esc(row["agent"])}</a></p>' if meta['register'] not in {'/', ''} else ''}
</main>
<footer>
  <p class="note">{esc(row['host'])} is the {esc(cc['label'])} desk for {esc(row['agent'])}. Independent notes, not the official {esc(row['agent'])} site.</p>
</footer>
</body>
</html>
"""


def restore_usfans_nginx(conf: str, host: str) -> str:
    conf = re.sub(
        r"location / \{\s*return 301 https://usfansspreadsheet\.net\$request_uri;\s*\}",
        "location / { try_files $uri $uri/ $uri/index.html =404; }",
        conf,
    )
    conf = conf.replace(
        "return 301 https://usfansspreadsheet.net$request_uri;",
        f"return 301 https://{host}$request_uri;",
    )
    return conf


def apply(bt: Baota, inventory: dict, dry_run: bool = False) -> None:
    usfans_countries = ["usfansspreadsheet.uk", "usfansspreadsheet.nl", "usfansspreadsheet.co.uk"]
    for host in usfans_countries:
        nginx = f"/www/server/panel/vhost/nginx/{host}.conf"
        original = bt.get(nginx) or ""
        new = restore_usfans_nginx(original, host)
        rewrite = f"/www/server/panel/vhost/rewrite/{host}.conf"
        if dry_run:
            print("dry-run usfans", host, "changed", new != original)
            continue
        if new != original:
            print("usfans nginx", host, bt.put(nginx, new).get("msg"))
        print("usfans rewrite", host, bt.put(rewrite, "# country-independent HTTPS apex\n").get("msg"))

    for row in inventory["sites"]:
        if row["status"] != "live":
            continue
        html_doc = page_html(row)
        dest = f"/www/wwwroot/{row['host']}/index.html"
        overlay = ROOT / "sites" / row["host"] / "overlay" / "index.html"
        overlay.parent.mkdir(parents=True, exist_ok=True)
        overlay.write_text(html_doc)
        if dry_run:
            print("dry-run page", row["host"])
            continue
        print("put", dest, bt.put(dest, html_doc).get("msg", "")[:60])
    if not dry_run:
        print("reload", bt.reload_nginx())


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-inventory", action="store_true")
    parser.add_argument("--hosts-json", default="")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()
    if args.hosts_json:
        hosts = json.loads(Path(args.hosts_json).read_text())
    elif INV_PATH.exists() and not args.write_inventory:
        hosts = [s["host"] for s in json.loads(INV_PATH.read_text())["sites"]]
    else:
        raise SystemExit("Need --write-inventory with --hosts-json, or an existing inventory")

    if args.write_inventory:
        inv = build_inventory(hosts)
        INV_PATH.write_text(json.dumps(inv, indent=2, ensure_ascii=False) + "\n")
        print("wrote", INV_PATH, "agents", len(inv["by_agent"]), "sites", len(inv["sites"]))
        for agent, countries in inv["by_agent"].items():
            print(f"  {agent}: " + ", ".join(f"{cc}={len(hs)}" for cc, hs in countries.items()))
        return 0

    inv = json.loads(INV_PATH.read_text())
    if args.apply or args.dry_run:
        key = os.environ.get("BT_KEY", "")
        if not key:
            raise SystemExit("BT_KEY required")
        apply(Baota(key), inv, dry_run=args.dry_run)
        return 0
    print("Pass --write-inventory, --dry-run or --apply")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
