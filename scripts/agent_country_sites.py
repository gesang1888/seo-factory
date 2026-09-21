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
    # US / global USFans spreadsheet hub — country TLDs are rewritten, not this host.
    "usfansspreadsheet.net",
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

# Long unique agent copy so country pages are not a name-swap of one mall template.
AGENT_BODY = {
    "CSSBuy": "CSSBuy is a veteran Weidian/Taobao purchasing desk. This page only talks about how CSSBuy names lines after warehouse photos — triangle, tax-free, and postal SKUs are labels in their app, not a shared mall. Sister CSSBuy ccTLDs keep their own last-mile notes. Do not paste AllChinaBuy or Superbuy HTML here.",
    "OrientDig": "OrientDig is a separate purchasing agent with its own register URL and QC queue. This country page follows OrientDig’s packed-kg screen and the line names that agent actually sells. It is not a CSSBuy skin and not a doorway onto another OrientDig TLD.",
    "BBDBuy": "BBDBuy (bbdbuy.com checkout) is not BBDBuyEU. Country storefronts on BBDBuy domains stay on the BBDBuy warehouse and coupon rules. EU-fiscal marketing belongs on BBDBuyEU hosts. W2C catalog clones do not belong on these ccTLDs.",
    "BBDBuyEU": "BBDBuyEU is the EU-facing checkout brand (bbdbuyeu.com). This host must not reuse BBDBuy country copy, AllChinaBuy leftovers, or a W2C product grid. Talk about BBDBuyEU line names and the destination the account ships to.",
    "AllChinaBuy": "AllChinaBuy shipping notes for this destination. ACBuy country domains are a different agent key in this panel — do not swap the HTML. Coupon codes and warehouse photos come from the AllChinaBuy app, not from a sister ccTLD.",
    "ACBuy": "ACBuy is filed as its own agent here even when people confuse it with AllChinaBuy. This country’s last-mile products are whatever ACBuy’s quote screen shows after packing. AllChinaBuy URLs stay on AllChinaBuy hosts.",
    "SugarGoo": "SugarGoo warehouse photos and the line card for this destination. SugarGoo’s “now” global host is a current-rates desk, not a country clone. Expert QC options are SugarGoo SKUs — other agents’ QC menus do not apply.",
    "LitBuy": "LitBuy country notebook. Spreadsheet vs agent-desk hostnames on LitBuy ccTLDs have different jobs. LitBuy coupons and line names come from the LitBuy account; do not import a CSSBuy rate table.",
    "LoveGoBuy": "LoveGoBuy quote screen for this country only. LoveGoBuy’s EU/IT/NL/CA/ES hosts are separate local desks. Coupon pages on other agents are irrelevant here.",
    "HipoBuy": "HipoBuy parcel math: volumetric on sneakers vs gram weight on tees, using HipoBuy’s own line names. Review-site roundups that mix HipoBuy with Superbuy belong somewhere else.",
    "OOTDBuy": "OOTDBuy destination guide. The .org and .net OOTDBuy hosts are global desks, not this country. Outfit/QC language stays on the OOTDBuy warehouse workflow.",
    "MyCNBox": "MyCNBox last-mile for this country. mycnboxhaul.com is the haul SOP host; country ccTLDs are quote desks. Do not 301 them onto each other.",
    "USFans": "USFans spreadsheets are country documents. The .net host is the US/global desk and stays untouched. .uk, .co.uk and .nl are live local sheets — they must not 301 onto .net.",
    "FansBuy": "FansBuy is a different brand from USFans. FansBuy country/EU/DE hosts keep FansBuy line names. Do not redirect FansBuy onto usfansspreadsheet.net or the other way around.",
    "KakoBuy": "KakoBuy country desk. Finland (Posti), Canada, Spain, France and the Netherlands each have their own host. kakobuydocs / tips style hostnames — if present — are operator manuals, not country doorways.",
    "Superbuy": "Superbuy is the older full-service agent. Country spreadsheet hosts here only discuss Superbuy’s own line card after packed kg. Do not dress Superbuy HTML as CSSBuy or OrientDig.",
    "MuleBuy": "MuleBuy country notes. The thin .org twin is gone (410). Remaining MuleBuy ccTLDs stay up as local desks with MuleBuy warehouse vocabulary.",
    "HubBuy": "HubBuy operations host versus spreadsheet host: two jobs. Product rows that were synced from a catalog belong under HubBuy URLs, not as a W2C doorway homepage.",
    "WeMimi": "WeMimi global/country desk. wemimi.net and the spreadsheet host — if both exist — are not aliases. Do not 301 WeMimi onto FashionReps or HubBuy.",
    "FashionReps": "FashionReps commentary and find notes. This is not a shopping-agent register funnel and not a W2CLinks clone. No agent checkout CTA on this host.",
    "CNShopper": "CNShopper local notes. The .net operations host and the spreadsheet host split SOP vs QC logs. Other agents’ coupon blogs do not belong here.",
    "OOPBuy": "OOPBuy Italy desk. Poste Italiane last-mile and OOPBuy’s own line names. Not a Superbuy Italy skin.",
    "BaseTao": "BaseTao global spreadsheet. BaseTao’s warehouse and expert QC are the only workflow on this host. No country-TLD doorway network is attached here.",
    "UNKNOWN": "Independent shopping-agent hub. It is not a country TLD of CSSBuy/OrientDig/BBDBuy and must not 301 onto w2clinks.com.",
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


REGISTER = {
    "UK": "Open the agent account from a UK delivery address so the quote screen shows GBP and Royal Mail-handed products. Signup on this country host; packed-kg comparison lives on the spreadsheet hostname if one exists.",
    "US": "Create the agent account with a US address. USD line names (USPS vs integrator) appear after the warehouse accepts the parcel — not on a UK page.",
    "CA": "Canadian account + CAD. Do not reuse a US login’s address book to price a Canada Post product.",
    "NL": "Maak het agent-account met een Nederlands adres. PostNL-productnamen horen op deze desk, niet op de UK-spreadsheet.",
    "DE": "Konto mit deutscher Lieferadresse. DHL-Produktnamen gehören hierher, nicht auf die AT-Domain.",
    "FR": "Créez le compte avec une adresse FR. Colissimo n’est pas un tarif copié depuis .es.",
    "ES": "Alta con dirección en España. Correos sale en esta mesa, no en la italiana.",
    "IT": "Registrazione con indirizzo IT. Poste Italiane è il prodotto di questa desk.",
    "AT": "Konto mit österreichischer Adresse. Nicht das deutsche DHL-Menü.",
    "AU": "Australian account, AUD, Australia Post products only on this desk.",
    "FI": "Suomalainen toimitusosoite. Posti-tuotteet tällä deskillä.",
    "PL": "Konto z polskim adresem. InPost / Poczta — nie cennik DE.",
    "EU": "Use the member-state address you actually ship to. .eu is not a shortcut that replaces a country desk.",
    "GLOBAL": "Global register desk: pick a real destination in the agent before you compare lines.",
}

COUK = {
    "hook": "This .co.uk document is the commercial-UK sheet: how GB carrier products and VAT-invoice language appear inside the agent after packing. It is not the Nominet .uk sheet.",
    "packed": "On .co.uk, compare Royal Mail / parcel-force class products as the agent spells them on a GB address. Northern Ireland routing is a different carrier SKU — read the live name, do not copy a .uk or .net row.",
    "customs": "HMRC rules follow the carrier product you buy on this .co.uk desk. Educational only; no under-declaration coaching.",
}

PACKED = {
    "UK": "A 2.4 kg hoodie haul that hands off to Royal Mail is a different SKU from the same clothes on an untracked 500 g tee line. Read the product name in the agent app after the warehouse photo, not a US blog screenshot.",
    "US": "USPS Ground Advantage vs a commercial integrator is decided on the line card after packed kg. Shoe boxes eat volumetric weight; a 500 g T-shirt haul does not.",
    "CA": "Canada Post last-mile plus CAD quotes will not match a US invoice for the same cart. Wait for the packed-kg screen inside the agent.",
    "NL": "PostNL brievenbus versus pakket, plus of je een fiscale EU-lijn koopt, verandert de quote. Een UK-screenshot is geen Nederlands tarief.",
    "DE": "DHL Päckchen und Paket sind andere Produkte als eine US-Linie. Volumen bei Schuhen zählt nach dem Wiegen im Lager.",
    "FR": "Colissimo / Colis Exo et une ligne fiscale UE ne se comparent pas à un tarif US. Le poids colisé dans l’agent est la seule entrée honnête.",
    "ES": "Correos no es DHL Alemania. Espera el peso embalado en el agente; no copies un presupuesto DE.",
    "IT": "Poste Italiane e una linea fiscale UE non sono un listino USA. Il peso imballato nell’agente è l’unico input.",
    "AT": "Österreichische Post ist nicht DHL Deutschland. Anderes Last-Mile-Produkt, anderer Quote-Screen nach dem Wiegen.",
    "AU": "Australia Post transit and AUD volumetric on sneakers kill lines that look cheap on a US calculator. Quote after packed kg.",
    "FI": "Posti-loppujakelu ei ole Saksan DHL. Älä käytä DE-hintaa; katso pakattu paino agentissa.",
    "PL": "InPost / Poczta Polska to nie DHL DE. Cennik po zważeniu w magazynie, nie z niemieckiego bloga.",
    "EU": "An .eu host is for fiscal-line shopping across member states. The SKU name (IOSS / fiscal / local post) still has to match the destination you typed in the agent.",
    "GLOBAL": "This hostname is the global desk for the agent. Pick the destination your account actually ships to before you compare lines.",
}


def host_job(host: str) -> dict:
    h = host.lower()
    if "haul" in h:
        return {
            "role": "haul desk",
            "h2": "Packed-haul SOP for this destination",
            "para": (
                "Haul-desk job: the order of operations after items land in the warehouse — "
                "QC photos, rehearsal packing, declared-line product name, and the last-mile "
                "carrier printed on the label. This is not the registration homepage and not "
                "a spreadsheet of historical rows. Sister ccTLDs that omit “haul” keep quote cards."
            ),
        }
    if "spreadsheets" in h:
        return {
            "role": "haul log",
            "h2": "Country haul log (plural spreadsheet host)",
            "para": (
                "Plural “spreadsheets” host: a log of packed-kg rows, QC pass/fail notes, and "
                "which line name was actually purchased for this country. The singular "
                "“spreadsheet” host (if it exists) is the live line card. The bare agent ccTLD "
                "is the register/login desk. Three URLs, three jobs — zero 301 between them."
            ),
        }
    if "spreadsheet" in h:
        return {
            "role": "spreadsheet desk",
            "h2": "Country spreadsheet — line cards for this last-mile only",
            "para": (
                "Singular spreadsheet: the live line card and warehouse-photo notes for this "
                "country’s last-mile. It is not a dump of every SKU in a shared catalog and "
                "not the agent’s marketing homepage. If a bare ccTLD exists, that host handles "
                "account signup; this one handles packed-kg comparison."
            ),
        }
    if "docs" in h:
        return {
            "role": "operator manual",
            "h2": "Agent docs — UI spelling, not a country doorway",
            "para": (
                "Docs hostname: how this agent’s own screens spell warehouse, QC, and line products. "
                "Tips/coupon/review hosts — if they exist — are other manuals. This URL does not 301 "
                "onto a ccTLD spreadsheet and does not host a cloned product grid."
            ),
        }
    if "tips" in h:
        return {
            "role": "operator manual",
            "h2": "Operator tips — packing order, not a mall clone",
            "para": (
                "Tips hostname: packing order, photo checklist, and which quote screen to trust. "
                "It is not the docs host and not a country TLD. Treat it as a handbook, not a doorway."
            ),
        }
    if "coupon" in h:
        return {
            "role": "operator manual",
            "h2": "Coupon notes for this agent only",
            "para": (
                "Coupon hostname: codes and stacking rules as this agent’s account actually shows them. "
                "Foreign-agent coupon blogs and country spreadsheet ccTLDs are different sites."
            ),
        }
    if "review" in h:
        return {
            "role": "operator manual",
            "h2": "Review notes — this agent’s QC, not a roundup blog",
            "para": (
                "Review hostname: QC outcomes and warehouse photo language for this agent. "
                "It is not a multi-agent roundup and not the spreadsheet host’s line card."
            ),
        }
    if "find" in h:
        return {
            "role": "operator manual",
            "h2": "Find notes — commentary, not checkout",
            "para": (
                "Find hostname: commentary and find-pages, not a shopping-agent register funnel "
                "and not a W2C product clone."
            ),
        }
    return {
        "role": "agent desk",
        "h2": "Country agent desk — register and last-mile product names",
        "para": (
            "Bare country host: where readers open an account and learn the last-mile product "
            "names this destination uses. Spreadsheet hosts on the same ccTLD store QC logs. "
            "Do not turn this URL into a copy of another country’s homepage with the TLD swapped."
        ),
    }


def tld_angle(host: str, agent: str, country: str) -> str:
    """Host-specific paragraph so .uk vs .co.uk (same role) are different documents."""
    h = host.lower()
    if h.endswith(".co.uk"):
        return (
            f"{agent} on the commercial .co.uk hostname is a UK document that talks about "
            "how GB routing and HMRC-facing carrier products show up in the agent app. "
            "It is not the Nominet .uk sheet and not a US .net clone. Northern Ireland vs "
            "Great Britain routing is a carrier-product question — this page does not pick a declared value."
        )
    if h.endswith(".uk"):
        return (
            f"{agent} on the .uk hostname is a separate United Kingdom spreadsheet/desk from "
            "any .co.uk twin. Nominet .uk is its own URL: Royal Mail Tracked product names "
            "after packed kg, in GBP. Do not 301 .uk onto .co.uk or onto a .net doorway."
        )
    if h.endswith(".nl"):
        return (
            f"{agent} on .nl is the Netherlands document (PostNL / fiscale EU-lijn). "
            "It is written for a Dutch delivery address, not as an English duplicate of the UK page."
        )
    if h.endswith(".de"):
        return (
            f"{agent} on .de bleibt eine deutsche Seite: DHL-Produktnamen nach dem Wiegen. "
            "Kein Spiegel der AT- oder NL-Domain."
        )
    if h.endswith(".at"):
        return (
            f"{agent} auf .at ist Österreich — Österreichische Post, nicht DHL Deutschland. "
            "Die .de-Domain desselben Agenten ist ein anderes Dokument."
        )
    if h.endswith(".fr"):
        return (
            f"{agent} sur .fr parle Colissimo / Colis Exo et des lignes fiscales UE. "
            "Ce n’est pas la page .be ou .nl avec un autre TLD."
        )
    if h.endswith(".es"):
        return (
            f"{agent} en .es usa Correos y la cotización en EUR para una dirección española. "
            "No copies el texto de .it o .fr."
        )
    if h.endswith(".it"):
        return (
            f"{agent} su .it è la desk Italia (Poste Italiane). Non è Superbuy.it di un altro marchio "
            "e non è la pagina .es."
        )
    if h.endswith(".ca"):
        return (
            f"{agent} on .ca is the Canada desk (CAD, Canada Post). A US spreadsheet for the same "
            "agent is a different document — do not 301 .ca onto .us or .com."
        )
    if h.endswith(".us"):
        return (
            f"{agent} on .us is the United States desk (USD, USPS or a commercial integrator). "
            "Country ccTLDs of the same agent stay on their own hosts."
        )
    if h.endswith(".eu"):
        return (
            f"{agent} on .eu is the multi-member-state fiscal-line desk. It is not a clone of one "
            "member ccTLD. Read the IOSS/fiscal SKU in the agent for the actual destination country."
        )
    if h.endswith(".fi"):
        return (
            f"{agent} .fi on Suomen desk (Posti). Saksan tai Ruotsin sivua ei saa 301:llä tähän."
        )
    if h.endswith(".pl"):
        return (
            f"{agent} na .pl to polski desk (InPost / Poczta). To nie kopia .de."
        )
    if h.endswith(".au"):
        return (
            f"{agent} on .au is the Australia desk (AUD, Australia Post). US volumetric jokes do not apply."
        )
    if "now" in h:
        return (
            f"{agent} “now” hostname: current-rate notes, not an archive of another country’s spreadsheet."
        )
    if h.endswith(".org"):
        return (
            f"{agent} on .org is the public-document / community-facing desk. "
            "A .net or .com twin of the same agent is a different job (operations vs spreadsheet) "
            "and must not 301 onto this .org URL."
        )
    if h.endswith(".net"):
        return (
            f"{agent} on .net is the operations/spreadsheet gTLD. Country ccTLDs stay independent. "
            "A .com or .org twin is not an alias of this .net host."
        )
    if h.endswith(".com"):
        return (
            f"{agent} on .com is the generic global desk. It is not the canonical of country ccTLDs "
            "and not a silent alias of a .net spreadsheet host."
        )
    return f"{agent} hostname {host} is the {country} desk. It does not 301 onto another TLD."


def sibling_country_labels(inventory: dict, row: dict) -> str:
    by = inventory.get("by_agent", {}).get(row["agent"], {})
    others = [cc for cc in by if cc != row["country"]]
    if not others:
        return (
            f"{row['agent']} has no other country desks in this panel. "
            f"{row['host']} still must not 301 onto another shopping agent."
        )
    others = sorted(others)
    seed = sum(ord(c) for c in row["host"])
    a = COUNTRIES[others[seed % len(others)]]["label"]
    b = COUNTRIES[others[(seed // 7) % len(others)]]["label"]
    if a == b and len(others) > 1:
        b = COUNTRIES[others[(seed + 1) % len(others)]]["label"]
    return (
        f"{row['host']} is only the {COUNTRIES[row['country']]['label']} desk for {row['agent']}. "
        f"Other {row['agent']} country hosts (for example {a} and {b}) stay on their own ccTLDs "
        "and must not 301 here."
    )


def same_country_note(inventory: dict, row: dict) -> str:
    hosts = inventory.get("by_agent", {}).get(row["agent"], {}).get(row["country"], [])
    others = [h for h in hosts if h != row["host"]]
    if not others:
        return f"No other {row['agent']} hostname shares this country TLD in the panel."
    jobs = ", ".join(f"{h} ({host_job(h)['role']})" for h in others)
    extra = ""
    if row["host"].endswith(".co.uk"):
        extra = " The .co.uk hostname is a separate UK document from any .uk host — they are not aliases."
    elif row["host"].endswith(".uk") and not row["host"].endswith(".co.uk"):
        extra = " The .uk hostname is a separate UK document from any .co.uk host — they are not aliases."
    return f"Same-country siblings (different jobs): {jobs}.{extra}"


def page_html(row: dict, inventory: dict | None = None) -> str:
    inventory = inventory or {"by_agent": {}}
    cc = COUNTRIES[row["country"]]
    meta = AGENT_META.get(row["agent"], AGENT_META["UNKNOWN"])
    job = host_job(row["host"])
    lang = cc["lang"]
    title = f"{row['agent']} {cc['label']} {job['role']} — {cc['carrier']}"
    h1 = f"{row['agent']} {job['role']} for {cc['label']} ({cc['currency']})"
    hook = cc.get("hook") or cc.get("en_hook")
    body_en = cc.get("en_hook")
    packed = PACKED[row["country"]]
    customs = cc["customs"]
    if row["host"].endswith(".co.uk"):
        hook = COUK["hook"]
        packed = COUK["packed"]
        customs = COUK["customs"]
        body_en = None
    mid = packed if job["role"] != "agent desk" else REGISTER[row["country"]]
    siblings = sibling_country_labels(inventory, row)
    same = same_country_note(inventory, row)
    agent_body = AGENT_BODY.get(row["agent"], AGENT_BODY["UNKNOWN"])
    angle = tld_angle(row["host"], row["agent"], row["country"])
    cta = (
        f'<p><a class="cta" href="{esc(meta["register"])}">Open {esc(row["agent"])} for {esc(cc["label"])}</a></p>'
        if meta["register"] not in {"/", ""}
        else ""
    )
    en_p = f'<p lang="en">{esc(body_en)}</p>' if body_en and lang != "en" else ""
    faq = [
        {
            "@type": "Question",
            "name": f"Is {row['host']} the same site as other {row['agent']} country domains?",
            "acceptedAnswer": {
                "@type": "Answer",
                "text": f"No. {row['host']} is the {cc['label']} {job['role']}. Other {row['agent']} ccTLDs stay independent local sites.",
            },
        },
        {
            "@type": "Question",
            "name": f"How should I read a {row['agent']} quote for {cc['carrier']}?",
            "acceptedAnswer": {
                "@type": "Answer",
                "text": mid,
            },
        },
        {
            "@type": "Question",
            "name": f"Does this page tell me what value to declare on a {cc['label']} haul?",
            "acceptedAnswer": {
                "@type": "Answer",
                "text": customs,
            },
        },
    ]
    ld = [
        {
            "@context": "https://schema.org",
            "@type": "WebPage",
            "name": title,
            "inLanguage": cc["locale"],
            "about": row["agent"],
            "url": f"https://{row['host']}/",
            "isPartOf": {
                "@type": "WebSite",
                "name": f"{row['agent']} {cc['label']} {job['role']}",
                "url": f"https://{row['host']}/",
            },
        },
        {
            "@context": "https://schema.org",
            "@type": "FAQPage",
            "mainEntity": faq,
        },
    ]
    faq_html = "\n".join(
        f"<h3>{esc(q['name'])}</h3><p>{esc(q['acceptedAnswer']['text'])}</p>" for q in faq
    )
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
h2 {{ font-size:1.15rem; }}
</style>
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
</head>
<body>
<header>
  <p class="note">{esc(row['agent'])} · {esc(cc['label'])} · {esc(row['host'])} · {esc(job['role'])}</p>
</header>
<main>
  <h1>{esc(h1)}</h1>
  <p>{esc(meta['pitch'])}</p>
  <p>{esc(agent_body)}</p>
  <p>{esc(hook)}</p>
  {en_p}
  <p>{esc(angle)}</p>
  <h2>{esc(job['h2'])}</h2>
  <p>{esc(job['para'])}</p>
  <p>{esc(mid)}</p>
  <p>{esc(customs)}</p>
  <p>{esc(siblings)}</p>
  <p>{esc(same)}</p>
  <h2>FAQ — {esc(row['host'])}</h2>
  {faq_html}
  {cta}
</main>
<footer>
  <p class="note">{esc(row['host'])} is the {esc(cc['label'])} {esc(job['role'])} for {esc(row['agent'])}. Independent notes, not the official {esc(row['agent'])} site. Different agents stay on their own hosts.</p>
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
            backup = nginx + ".bak-agent-country"
            if original and bt.get(backup) is None:
                bt.put(backup, original)
            print("usfans nginx", host, bt.put(nginx, new).get("msg"))
        print("usfans rewrite", host, bt.put(rewrite, "# country-independent HTTPS apex\n").get("msg"))

    for row in inventory["sites"]:
        if row["status"] != "live":
            continue
        html_doc = page_html(row, inventory)
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
    parser.add_argument("--write-overlays", action="store_true")
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

    inv = build_inventory(hosts)
    INV_PATH.write_text(json.dumps(inv, indent=2, ensure_ascii=False) + "\n")

    if args.write_overlays:
        n = 0
        for row in inv["sites"]:
            if row["status"] != "live":
                continue
            overlay = ROOT / "sites" / row["host"] / "overlay" / "index.html"
            overlay.parent.mkdir(parents=True, exist_ok=True)
            overlay.write_text(page_html(row, inv))
            n += 1
        print("wrote overlays", n)
        return 0

    if args.apply or args.dry_run:
        key = os.environ.get("BT_KEY", "")
        if not key:
            raise SystemExit("BT_KEY required")
        apply(Baota(key), inv, dry_run=args.dry_run)
        return 0
    print("Pass --write-inventory, --write-overlays, --dry-run or --apply")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
