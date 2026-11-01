#!/usr/bin/env python3
"""Deepen the five Kakobuy dest desks to the kakobuy.co.uk cluster.

Order: reclaim FR/NL 301 (nginx), then homepage SERP title + WebSite keywords,
then thicken keep inners (FI → CA → ES → FR → NL). Does not smash unique
/ohje/. Does not coach a declared value. GSC: sitemap submit only.
"""
from __future__ import annotations

import json
import os
import re
import sys
import time
from datetime import datetime, timezone
from html import escape, unescape
from pathlib import Path

_TOOLS = Path(__file__).resolve().parent
if str(_TOOLS) not in sys.path:
    sys.path.insert(0, str(_TOOLS))
from desk_template import (
    cluster_keywords,
    cluster_title_serp,
    faq_ld,
    inject_jsonld,
    website_ld,
)

ROOT = Path(__file__).resolve().parents[1]
STAMP = "20261101"
TODAY = "2026-11-01"
MARKER = f'data-kakobuy-five="{STAMP}"'
_SA_CANDIDATES = [
    os.environ.get("GSC_SA_JSON", ""),
    "/tmp/hipobuy-creds/sa.json",
    "/cursor/stores/self/internal/gsc-sa.json",
]
SA = next((p for p in _SA_CANDIDATES if p and Path(p).is_file()), "/tmp/hipobuy-creds/sa.json")
BAK_NGINX = "/www/backup/portfolio-step5-phaseb-20261026-150339"

HOSTS = {
    "kakobuy.fi": {
        "key": "fi",
        "dest": "FI",
        "loc": "fi",
        "lang": "fi-FI",
        "label": "Suomi",
        "customs": "Tulli",
        "customs_url": "https://tulli.fi/",
        "post": "Posti",
        "city": "00100 Helsinki",
        "pages": {
            "spreadsheet": "kakobuy-spreadsheet",
            "finds": "kakobuy-finds",
            "qc": "kakobuy-qc",
            "shipping": "kakobuy-toimitus",
            "legal": "kakobuy-kokemuksia",
            "faq": "faq",
        },
        "skip": {"ohje"},
        "canon": [("kakobuy-shipping", "kakobuy-toimitus")],
    },
    "kakospreadsheet.ca": {
        "key": "ca",
        "dest": "CA",
        "loc": "en",
        "lang": "en-CA",
        "label": "Canada",
        "customs": "CBSA",
        "customs_url": "https://www.cbsa-asfc.gc.ca/",
        "post": "Canada Post",
        "city": "postal code A1A 1A1",
        "pages": {
            "spreadsheet": "kakobuy-spreadsheet",
            "finds": "kakobuy-finds",
            "qc": "kakobuy-qc",
            "shipping": "kakobuy-shipping-to-canada",
            "legal": "is-kakobuy-legit",
            "guide": "kakobuy-guide",
            "faq": "kakobuy-faq",
        },
        "skip": set(),
        "canon": [("kakobuy-shipping", "kakobuy-shipping-to-canada")],
    },
    "kakospreadsheet.es": {
        "key": "es",
        "dest": "ES",
        "loc": "es",
        "lang": "es-ES",
        "label": "España",
        "customs": "Agencia Tributaria",
        "customs_url": "https://sede.agenciatributaria.gob.es/",
        "post": "Correos",
        "city": "código postal de cinco dígitos",
        "pages": {
            "spreadsheet": "kakobuy-spreadsheet",
            "finds": "kakobuy-finds",
            "qc": "kakobuy-qc",
            "shipping": "envio-kakobuy-espana",
            "legal": "kakobuy-opiniones",
            "guide": "kakobuy-guide",
            "faq": "kakobuy-faq",
        },
        "skip": set(),
        "canon": [("kakobuy-shipping", "envio-kakobuy-espana")],
    },
    "kakospreadsheet.fr": {
        "key": "fr",
        "dest": "FR",
        "loc": "fr",
        "lang": "fr-FR",
        "label": "France",
        "customs": "douane.gouv.fr",
        "customs_url": "https://www.douane.gouv.fr/",
        "post": "Colissimo",
        "city": "code postal à cinq chiffres, pas un code belge",
        "pages": {
            "spreadsheet": "kakobuy-spreadsheet",
            "finds": "kakobuy-finds",
            "qc": "kakobuy-qc",
            "shipping": "livraison-kakobuy",
            "legal": "avis-kakobuy",
            "guide": "kakobuy-guide",
            "faq": "kakobuy-faq",
        },
        "skip": set(),
        "canon": [("kakobuy-shipping", "livraison-kakobuy")],
    },
    "kakospreadsheet.nl": {
        "key": "nl",
        "dest": "NL",
        "loc": "nl",
        "lang": "nl-NL",
        "label": "Nederland",
        "customs": "Belastingdienst Douane",
        "customs_url": "https://www.belastingdienst.nl/wps/wcm/connect/nl/douane/",
        "post": "PostNL / DHL",
        "city": "Nederlandse postcode 1234 AB",
        "pages": {
            "spreadsheet": "kakobuy-spreadsheet",
            "finds": "kakobuy-finds",
            "qc": "kakobuy-qc",
            "shipping": "kakobuy-verzending",
            "legal": "kakobuy-ervaringen",
            "guide": "kakobuy-guide",
            "faq": "kakobuy-faq",
        },
        "skip": set(),
        "canon": [("kakobuy-shipping", "kakobuy-verzending")],
    },
}

ORDER = [
    "kakobuy.fi",
    "kakospreadsheet.ca",
    "kakospreadsheet.es",
    "kakospreadsheet.fr",
    "kakospreadsheet.nl",
]


def overlay(host: str) -> Path:
    return ROOT / "sites" / host / "overlay"


def _connect():
    try:
        import paramiko
    except ImportError:
        import subprocess

        subprocess.check_call([sys.executable, "-m", "pip", "install", "paramiko", "-q"])
        import paramiko

    password = os.environ.get("ORIGIN_SSH_PASS")
    if not password:
        cred = Path("/tmp/hipobuy-creds/origin.pass")
        if cred.is_file():
            password = cred.read_text().strip()
    if not password:
        raise SystemExit("Set ORIGIN_SSH_PASS")
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect("31.97.41.31", username="root", password=password, timeout=30)
    return client


def _run(client, cmd: str, timeout: int = 90) -> str:
    _, stdout, stderr = client.exec_command(cmd, timeout=timeout)
    return (stdout.read() + stderr.read()).decode(errors="replace").strip()


def reclaim_nginx() -> None:
    """Restore dest vhosts for FR/NL (undo Phase B catch-all 301 to kakobuydocs.com)."""
    client = _connect()
    stamp = time.strftime("%Y%m%d-%H%M%S")
    bak = f"/www/backup/kakobuy-five-reclaim-{stamp}"
    print(_run(client, f"mkdir -p '{bak}'"))
    for host in ("kakospreadsheet.fr", "kakospreadsheet.nl"):
        live = f"/www/server/panel/vhost/nginx/{host}.conf"
        src = f"{BAK_NGINX}/{host}.conf.bak"
        head = _run(client, f"head -c 800 '{live}'")
        sunset = "kakobuydocs.com" in head and "return 301" in head
        if not sunset:
            print("SKIP_RESTORE", host, "already dest vhost")
            continue
        print(_run(client, f"cp -a '{live}' '{bak}/{host}.conf.before'"))
        print(_run(client, f"cp -a '{src}' '{live}'"))
        print("RESTORE", host)
    # FI: serve /faq/ instead of 301 to /ohje/
    gsc = "/www/server/panel/vhost/nginx/extension/kakobuy.fi/gsc-redirects.conf"
    raw = _run(client, f"cat '{gsc}'")
    patched = re.sub(
        r"location\s*=\s*/faq/?\s*\{[^}]*kakobuy\.fi/ohje/?[^}]*\}\s*",
        "",
        raw,
        flags=re.I,
    )
    if patched != raw:
        print(_run(client, f"cp -a '{gsc}' '{bak}/gsc-redirects.conf.before'"))
        sftp = client.open_sftp()
        with sftp.open(gsc, "w") as fh:
            fh.write(patched)
        sftp.close()
        print("PATCH FI faq 301 removed")
    else:
        print("FI_FAQ_REDIRECT", "unchanged" if "/faq" in raw else "already clear")
    print(_run(client, "nginx -t && nginx -s reload"))
    client.close()
    print("RECLAIM_NGINX", bak)


def _copy(spec: dict) -> dict:
    host = spec  # filled by caller
    return host


def sections_for(kind: str, d: dict, host: str) -> tuple[str, str, list[tuple[str, list[str]]]]:
    loc = d["loc"]
    label, customs, post, city = d["label"], d["customs"], d["post"], d["city"]
    curl = d["customs_url"]
    agent = "Kakobuy"
    if loc == "fi":
        return _sec_fi(kind, host, label, customs, post, city, curl)
    if loc == "es":
        return _sec_es(kind, host, label, customs, post, city, curl)
    if loc == "fr":
        return _sec_fr(kind, host, label, customs, post, city, curl)
    if loc == "nl":
        return _sec_nl(kind, host, label, customs, post, city, curl)
    return _sec_en(kind, host, label, customs, post, city, curl)


def _sec_en(kind, host, label, customs, post, city, curl):
    a = "Kakobuy"
    if kind == "spreadsheet":
        return (
            f"{a} spreadsheet — {label} buyers",
            f"This page is the {a} spreadsheet desk for {label} on {host}: an index of QC’d finds, not Excel and not checkout. Keywords: Kakobuy spreadsheet, kakobuy spreadsheet canada, kakobuy sheet.",
            [
                ("What is a Kakobuy spreadsheet?", [
                    f"A {a} spreadsheet on {host} is a curated index of warehouse-checked SKUs for a {label} delivery address. It is not a second Kakobuy app and it does not take payment.",
                    f"UK-style desks (kakobuy.co.uk) use the same three keywords. This host keeps the geo as Canada — not UK, not a US ZIP. The official estimator still needs destination CA.",
                ]),
                (f"Why {label} buyers start with a sheet", [
                    f"Searching Taobao/1688/Weidian by hand dumps thousands of dead cards. The sheet keeps sneakers, hoodies and bags you already QC’d before you book {post} toward {city}.",
                    "A restricted or price-0 row is a dead source link, not a bargain. This desk does not invent a declared value.",
                ]),
                ("How the sheet works on this host", [
                    f"You open a find, read warehouse photos in the official {a} app, then book an international line with destination {label}. {host} only explains that order. Orders stay on kakobuy.com.",
                    f"English catalogue keys (sneakers, hoodie, jacket) still feed the wall on this host. They are display keys, not a US shop.",
                ]),
                ("What types of products sit here", [
                    "Shoes, hoodies, jackets, bags, watches — the same families UK buyers see, filtered by whether the warehouse still has the SKU. Electronics and perfume stay restricted unless the official app says otherwise.",
                ]),
                ("Is a spreadsheet safer than searching manually?", [
                    f"Safer means you saw QC photos before freight, not that {customs} stops existing. Read {curl} the morning you ship. GST/HST and broker fees change; this HTML does not paste a rate into the title.",
                ]),
                (f"Who should use this {label} sheet", [
                    f"First-time buyers who need a {city} address test, and anyone who already uses {a} but wants finds + QC + shipping in one independent desk. Not a customs broker.",
                ]),
                ("Common mistakes without a sheet", [
                    f"Pasting a US ZIP into the estimator, treating this hostname as checkout, or booking freight before QC. Last-mile is often {post}; Collect can add a fee the estimator hides.",
                ]),
                ("How to use it efficiently", [
                    f"Keep the spreadsheet, the finds list and the QC page in one tab set. When a find is accepted, open the official freight form toward {label}. Source: {customs}. No under-declaration.",
                ]),
            ],
        )
    if kind == "finds":
        return (
            f"{a} finds for {label} buyers",
            f"Top {a} finds on {host} are SKUs already QC’d for a {label} address — not a second global catalogue.",
            [
                ("What are Kakobuy finds on this site?", [
                    f"Finds are rows you keep after warehouse photos: sneakers, jackets, bags. They live on {host} so Canada is not a location-name swap of a UK page.",
                ]),
                (f"Why {label} buyers use curated finds", [
                    f"Manual search mixes dead Weidian links with live cards. Curated finds on this host are the ones that still open in the official app before {post} is booked.",
                ]),
                ("Popular categories", [
                    "Shoes and hoodies dominate the wall because those SKUs still have QC angles. Restricted categories stay off the sheet even if Reddit names them.",
                ]),
                ("How these finds are selected", [
                    f"A find needs a live source URL, at least one warehouse photo, and an estimator destination of {label} — not US, not this TLD. Price-0 cards drop off.",
                ]),
                ("Are finds safer than searching manually?", [
                    f"You still read {customs} ({curl}) the morning you ship. Finds only mean the piece was photographed in China before international freight.",
                ]),
                (f"Who should use finds from {host}", [
                    f"Buyers who already have a {city} address and want QC’d picks, not a US de-minimis article.",
                ]),
                ("Ready to open finds?", [
                    f"Use the cluster nav to QC, then shipping-to-Canada. Official register stays on kakobuy.com. {host} is information only.",
                ]),
            ],
        )
    if kind == "qc":
        return (
            f"{a} QC photos before shipping to {label}",
            f"QC on {host} means warehouse photos in the official {a} app, taken in China, before you pay freight to {label}.",
            [
                ("What QC is on this site", [
                    "Quality check is extra angles of the piece in the warehouse — seams, tags, sole. It is not a laboratory and not a customs x-ray.",
                ]),
                ("When to ask for extra photos", [
                    f"Ask while the SKU is still in China. After {post} has the carton, {customs} is the wrong window for a warehouse retake.",
                ]),
                ("What QC does not do", [
                    f"QC does not file a {customs} entry and does not invent a declared value. Educational source: {curl}.",
                ]),
                (f"QC and a {label} address", [
                    f"Use {city} in the estimator. A US ZIP is the wrong country for this host. Last-mile notes stay on the shipping page.",
                ]),
                ("Paid angles", [
                    "More photos are often a paid add-on in the official app. This HTML does not open tickets.",
                ]),
                ("If a find fails QC", [
                    "Leave it in the warehouse or return per the official app. Do not book international freight on a reject.",
                ]),
                ("Ready to ship after QC?", [
                    f"Only then open the official estimator toward {label}. {host} does not take payment.",
                ]),
            ],
        )
    if kind == "shipping":
        return (
            f"{a} shipping to {label}",
            f"{a} shipping to {label} is an official-estimator country code (CA), not this TLD. Open the live freight form after warehouse photos.",
            [
                (f"How shipping to {label} works", [
                    f"Warehouse in China → you accept QC → you book a line with destination {label} → {post} or the SKU’s last-mile hands it over. {host} does not print a live quote.",
                ]),
                ("Options you actually see in the app", [
                    "Tax-free / prepaid / collect are properties of the booked SKU. This desk does not rename them. Collect can add a broker fee the estimator hides.",
                ]),
                ("How long it takes", [
                    f"Transit days change with the SKU. This page does not invent Canada Post business days. Confirm in the official app the morning you ship.",
                ]),
                ("Costs", [
                    f"International freight + whatever the SKU says at the border. {post} may add a collect handling fee. No rate is pasted into this title.",
                ]),
                (f"Customs and GST/HST for {label}", [
                    f"Read {customs} at {curl} the morning you ship. GST/HST thresholds change. Ranked GST articles on this host stay — we do not copy a percentage here.",
                    "This HTML does not coach a declared value.",
                ]),
                ("Common risks", [
                    f"Wrong country in the estimator (US ZIP), booking before QC, assuming {city} is optional. Northern US routes are not Canada.",
                ]),
                (f"Is this suitable for first-time {label} buyers?", [
                    f"Yes if you treat {host} as a map and kakobuy.com as checkout. Address test: {city}. Source: {customs}.",
                ]),
                ("Ready to ship?", [
                    f"QC first, then the official estimator toward {label}.",
                ]),
            ],
        )
    if kind == "legal":
        return (
            f"Is {a} legal in {label}?",
            f"{a} is a purchasing agent. {host} is an independent information desk, not the official app and not {customs}.",
            [
                (f"Is {a} legal in {label}?", [
                    f"Using a purchasing agent is not a crime in {label}. Restricted goods, platform bans and the booked SKU still apply. Read {curl} the morning you ship.",
                ]),
                (f"Is {a} safe to use from {label}?", [
                    "Safe here means warehouse QC before freight, official-app payment, and a real CA address — not a promise that a parcel skips CBSA.",
                ]),
                ("Main risks", [
                    f"Dead source links, booking collect without reading the SKU, and treating {host} as checkout. {post} can add fees.",
                ]),
                ("How to reduce risk", [
                    f"QC in the official app, estimator destination {label}, {city} on the label. No under-declaration. No invented CBSA dollar.",
                ]),
                ("First-time buyers", [
                    f"Start with the spreadsheet and finds on this host, then the official register. {host} does not see your account.",
                ]),
                ("Final verdict", [
                    f"{a} can be used toward {label} if you follow the official app and {customs}. This desk stays independent. Copy reviewed {TODAY}.",
                ]),
                ("Ready to get started?", [
                    "Open spreadsheet → finds → QC → shipping-to-Canada. Orders only on kakobuy.com.",
                ]),
            ],
        )
    if kind == "guide":
        return (
            f"{a} guide for {label} buyers",
            f"A step-by-step {a} path for a {label} address on {host}. Not checkout.",
            [
                (f"How to buy from {a} ({label} guide)", [
                    f"Find a QC’d SKU, submit it in the official app, wait for warehouse photos, then book international freight toward {label}.",
                ]),
                (f"What {a} is", [
                    f"A China purchasing agent. {host} only explains the {label} desk. Payment stays on kakobuy.com.",
                ]),
                ("Step 1 — find the product", [
                    "Use the spreadsheet and finds on this host. Skip price-0 and restricted cards.",
                ]),
                ("Step 2 — submit the order on Kakobuy", [
                    "Official app only. This HTML cannot see the cart.",
                ]),
                ("Step 3 — QC in the warehouse", [
                    "Photos before freight. Extra angles may be paid.",
                ]),
                (f"Step 4 — choose international shipping to {label}", [
                    f"Estimator destination CA, address {city}. Read {customs} ({curl}) the morning you ship.",
                ]),
                (f"Step 5 — receive the package in {label}", [
                    f"Last-mile is often {post}. Collect can add a fee.",
                ]),
                ("Tips for first orders", [
                    "Do not paste a US ZIP. Do not book freight on a QC reject.",
                ]),
            ],
        )
    # faq
    return (
        f"{a} spreadsheet FAQ — {label}",
        f"Short answers for {label} buyers using the {a} spreadsheet on {host}.",
        [
            ("Do I need an account?", [
                f"Yes, on the official {a} site. {host} does not create accounts.",
            ]),
            (f"Is {a} safe for first-time {label} buyers?", [
                f"QC photos before freight, destination {label}, {city} on the label. Read {customs}. No declared-value coaching.",
            ]),
            ("How do I find reliable products?", [
                "Start with this host’s spreadsheet and finds. Dead Weidian links drop off the sheet.",
            ]),
            ("Will I receive QC photos?", [
                "In the official app, in China, before international freight. Extra angles are often paid.",
            ]),
            (f"How long does shipping to {label} take?", [
                f"It depends on the SKU. This page does not invent {post} days. Confirm in the official estimator.",
            ]),
            (f"Do I pay GST/HST or duty in {label}?", [
                f"The booked SKU says who pays. Collect can add a broker fee. Source: {customs} ({curl}). Thresholds change; we do not paste a rate.",
            ]),
            ("Spreadsheet or manual search?", [
                f"The sheet on {host} exists so {label} buyers are not hunting dead cards. It is still an index, not Excel.",
            ]),
            ("What do buyers usually purchase?", [
                "Shoes, hoodies, jackets, bags — if the warehouse still has QC. Restricted goods stay off.",
            ]),
        ],
    )


def _sec_fi(kind, host, label, customs, post, city, curl):
    a = "Kakobuy"
    if kind == "spreadsheet":
        return (
            f"{a} spreadsheet — ostajat Suomessa",
            f"Tämä sivu on {a} spreadsheet suomalaisille ostajille hostilla {host} — indeksi, ei Excel, ei kassa. Keywords: Kakobuy spreadsheet, kakobuy spreadsheet suomi, kakobuy sheet.",
            [
                ("Mikä on Kakobuy spreadsheet?", [
                    f"Spreadsheet {host}-hostilla on QC-tarkistettujen SKU:iden indeksi suomalaiseen osoitteeseen. Se ei ole toinen Kakobuy-appi eikä kassa.",
                    "kakobuy.co.uk käyttää samoja kolmea avainsanaa UK-geolla. Tämä host pitää geon Suomessa — ei SE, ei EU-geneerinen.",
                ]),
                ("Miksi suomalainen ostaja aloittaa sheetistä", [
                    f"Taobao/1688/Weidian paljaina tuottaa kuolleita kortteja. Sheet pitää findsit, jotka on jo QC:tty ennen kuin {post} lähtee kohti {city}.",
                    "Restricted tai hinta 0 on kuollut linkki, ei löytö. Ei aliarvostusta.",
                ]),
                ("Miten sheet toimii tällä hostilla", [
                    f"Avaat findin, luet varastokuvat virallisessa apissa, sitten varaat linjan kohteeseen Suomi. {host} vain selittää järjestyksen. Tilaukset kakobuy.comissa.",
                ]),
                ("Mitä tuoteperheitä täällä on", [
                    "Kengät, hupparit, takit, kassit — samat perheet kuin UK-deskissä, suodatettuna sillä onko SKU vielä varastossa. Elektroniikka ja tuoksut pysyvät restrictedinä ellei virallinen appi toisin sano.",
                ]),
                ("Onko spreadsheet turvallisempi kuin haku käsin?", [
                    f"Turvallisempi = näit QC-kuvat ennen rahtia, ei se että {customs} katoaa. Lue {curl} lähetysaamuna. ALV ja IOSS muuttuvat; tähän titleen ei liimata prosenttia.",
                ]),
                ("Kenelle tämä Suomen sheet on", [
                    f"Ensikertalaiselle, joka tarvitsee osoitetestin {city}, ja sille joka jo käyttää {a}:ta mutta haluaa finds + QC + toimitus yhdellä riippumattomalla deskillä.",
                ]),
                ("Tyypilliset virheet ilman sheettiä", [
                    f"Ruotsalainen postinumero arvioijassa, tämän hostin luuleminen kassaksi, rahti ennen QC:tä. Viimeinen kilometri on usein {post}; Collect voi lisätä maksun.",
                ]),
                ("Miten käyttää tehokkaasti", [
                    f"Pidä spreadsheet, finds ja QC samassa välilehtisetissä. Kun find on hyväksytty, avaa virallinen arvioija kohteeseen FI. Lähde: {customs}. Ei ilmoitusarvon keksimistä.",
                ]),
            ],
        )
    if kind == "finds":
        return (
            f"{a} finds Suomessa",
            f"{a}-findsit hostilla {host} ovat QC-tarkistettuja SKU:ita suomalaiseen osoitteeseen — ei toinen globaali katalogi.",
            [
                ("Mitä findsit ovat tällä deskillä?", [
                    f"Finds = rivit varastokuvien jälkeen: kengät, takit, kassit. Ne elävät {host}-hostilla, jotta Suomi ei ole UK-sivun maanimen vaihto.",
                ]),
                ("Miksi suomalainen ostaja käyttää kuratoituja findejä", [
                    f"Käsinhaku sekoittaa kuolleet Weidian-linkit ja elävät kortit. Tässä hostissa findsit ovat ne, jotka vielä aukeavat virallisessa apissa ennen {post}-varausta.",
                ]),
                ("Suositut kategoriat", [
                    "Kengät ja hupparit hallitsevat seinää, koska niissä on vielä QC-kulmia. Restricted pysyy poissa sheetistä.",
                ]),
                ("Miten findsit valitaan", [
                    f"Find vaatii elävän lähteen, vähintään yhden varastokuvan ja arvioijan kohteen FI — ei SE, ei tätä TLD:tä. Hinta-0 pudotetaan.",
                ]),
                ("Ovatko findsit turvallisempia?", [
                    f"Luet silti {customs} ({curl}) lähetysaamuna. Finds tarkoittaa vain että kappale kuvattiin Kiinassa ennen kansainvälistä rahtia.",
                ]),
                ("Kenelle {host} findsit ovat", [
                    f"Ostajalle, jolla on {city}-osoite.",
                ]),
                ("Valmis avaamaan findsit?", [
                    "QC, sitten toimitus. Rekisteröinti kakobuy.comissa.",
                ]),
            ],
        )
    if kind == "qc":
        return (
            f"{a} QC ennen toimitusta Suomeen",
            f"QC hostilla {host} = varastokuvat virallisessa {a}-apissa Kiinassa, ennen kuin maksat rahdin Suomeen.",
            [
                ("Mitä QC on tällä deskillä", [
                    "Quality check on lisäkulmia varastossa — saumat, laput, pohja. Ei laboratorio eikä tullin röntgen.",
                ]),
                ("Milloin pyytää lisäkuvia", [
                    f"Kun SKU on vielä Kiinassa. Kun {post} on jo kartongissa, {customs} on väärä ikkuna varastoretakeen.",
                ]),
                ("Mitä QC ei tee", [
                    f"QC ei tee tulli-ilmoitusta eikä keksi ilmoitusarvoa. Lähde: {curl}.",
                ]),
                ("QC ja suomalainen osoite", [
                    f"Arvioijassa FI ja {city}. Ruotsalainen postinumero on väärä maa. Toimitusmuistiinpanot ovat toimitus-sivulla.",
                ]),
                ("Maksulliset kulmat", [
                    "Lisäkuvat ovat usein maksullinen lisä virallisessa apissa. Tämä HTML ei avaa tikettejä.",
                ]),
                ("Jos find kaatuu QC:ssä", [
                    "Jätä varastoon tai palauta virallisen appin mukaan. Älä varaa kansainvälistä rahtia hylkäykselle.",
                ]),
                ("Valmis toimittamaan QC:n jälkeen?", [
                    f"Vasta sitten virallinen arvioija kohteeseen Suomi. {host} ei ota maksua.",
                ]),
            ],
        )
    if kind == "shipping":
        return (
            f"{a} toimitus Suomeen",
            f"{a}-toimitus Suomeen on arvioijan maakoodi FI, ei tämä TLD. Avaa virallinen rahtilomake varastokuvien jälkeen.",
            [
                ("Miten toimitus Suomeen etenee", [
                    f"Varasto Kiinassa → hyväksyt QC:n → varaat linjan kohteeseen Suomi → {post} hoitaa viimeisen kilometrin. {host} ei tulosta live-hintaa.",
                ]),
                ("Mitä vaihtoehtoja apissa näkyy", [
                    "Tax-free / prepaid / collect ovat SKU:n ominaisuuksia. Collect voi lisätä maksun, jota arvioija ei näytä.",
                ]),
                ("Kauanko kestää", [
                    f"SKU ratkaisee. Tämä sivu ei keksi Postin arkipäiviä. Vahvista virallisessa apissa lähetysaamuna.",
                ]),
                ("Kulut", [
                    f"Kansainvälinen rahti + se mitä SKU sanoo rajalla. {post} voi Collectissa lisätä käsittelymaksun. Tähän titleen ei liimata tarifia.",
                ]),
                ("Tulli ja ALV Suomessa", [
                    f"Lue {customs} ({curl}) lähetysaamuna. ALV, IOSS ja kynnykset muuttuvat. Rankkaavat tulliartikkelit tällä hostilla säilyvät.",
                    "Tämä HTML ei opeta aliarvostusta.",
                ]),
                ("Tyypilliset riskit", [
                    f"Väärä maa arvioijassa (SE), rahti ennen QC:tä, {city} jätetty pois. Tämä desk ei ole Ruotsi.",
                ]),
                ("Sopiiko ensikertalaiselle?", [
                    f"Kyllä, jos {host} on kartta ja kakobuy.com kassa. Osoitetesti: {city}. Lähde: {customs}.",
                ]),
                ("Valmis lähettämään?", [
                    "QC ensin, sitten virallinen arvioija kohteeseen FI.",
                ]),
            ],
        )
    if kind == "legal":
        return (
            f"Onko {a} laillinen Suomessa?",
            f"{a} on ostoagentti. {host} selittää Suomen polun; tilaukset kakobuy.comissa.",
            [
                ("Onko Kakobuy laillinen Suomessa?", [
                    f"Ostoagentin käyttö ei ole rikos Suomessa. Restricted, alustan kiellot ja varattu SKU pätevät silti. Lue {curl} lähetysaamuna.",
                ]),
                ("Onko Kakobuy turvallinen Suomesta?", [
                    f"Turvallinen = QC ennen rahtia, maksu virallisessa apissa, oikea FI-osoite — ei lupaus että {customs} jää väliin.",
                ]),
                ("Pääasialliset riskit", [
                    f"Kuolleet lähdelinkit, Collect lukematta SKU:ta, {host} kassana. {post} voi lisätä maksuja.",
                ]),
                ("Miten pienentää riskiä", [
                    f"QC virallisessa apissa, arvioijan kohde FI, {city} tarrassa. Ei aliarvostusta. Ei keksittyä Tulli-euroa.",
                ]),
                ("Ensikertalaiset", [
                    f"Aloita spreadsheetistä ja findsistä tällä hostilla, sitten virallinen rekisteröinti. {host} ei näe tiliäsi.",
                ]),
                ("Yhteenveto", [
                    f"{a}:ta voi käyttää Suomeen, jos noudatat virallista appia ja {customs}ia. Tämä desk pysyy riippumattomana. Teksti {TODAY}.",
                ]),
                ("Miten aloittaa?", [
                    "Spreadsheet → finds → QC → toimitus. Tilaukset vain kakobuy.comissa.",
                ]),
            ],
        )
    return (
        f"{a} spreadsheet FAQ — Suomi",
        f"Lyhyet vastaukset suomalaiselle ostajalle hostilla {host}.",
        [
            ("Tarvitsenko tilin?", [f"Kyllä, virallisella {a}-sivustolla. {host} ei luo tilejä."]),
            ("Onko Kakobuy turvallinen ensikertalaiselle?", [
                f"QC ennen rahtia, kohde FI, {city}. Lue {customs}. Ei ilmoitusarvo-ohjeita.",
            ]),
            ("Miten löydän luotettavia tuotteita?", ["Aloita tämän hostin spreadsheetistä ja findsistä."]),
            ("Saanko QC-kuvat?", ["Virallisessa apissa, Kiinassa, ennen kansainvälistä rahtia. Lisäkulmat usein maksullisia."]),
            ("Kauanko toimitus Suomeen kestää?", [f"SKU ratkaisee. Tämä sivu ei keksi {post}-päiviä."]),
            ("Maksanko tullin tai ALV:n Suomessa?", [
                f"SKU sanoo kuka maksaa. Collect voi lisätä maksun. Lähde: {customs} ({curl}). Kynnykset muuttuvat.",
            ]),
            ("Spreadsheet vai haku käsin?", [f"Sheet hostilla {host} on indeksi, ei Excel."]),
            ("Mitä yleensä ostetaan?", ["Kengät, hupparit, takit, kassit — jos varastossa on vielä QC. Restricted pois."]),
        ],
    )


def _sec_es(kind, host, label, customs, post, city, curl):
    a = "Kakobuy"
    if kind == "spreadsheet":
        return (
            f"{a} spreadsheet — compradores en {label}",
            f"Esta página es el spreadsheet {a} para España en {host}: un índice, no Excel ni caja. Keywords: Kakobuy spreadsheet, kakobuy spreadsheet espana, kakobuy sheet.",
            [
                ("Qué es un spreadsheet Kakobuy", [
                    f"En {host} es un índice de SKU con QC para una dirección en {label}. No es la app oficial ni aduanas.",
                    "kakobuy.co.uk usa las mismas tres keywords con geo uk. Este host mantiene geo España — no un código francés ni un CAP italiano.",
                ]),
                ("Por qué un comprador en España empieza por la hoja", [
                    f"Buscar Taobao/1688/Weidian a mano mezcla enlaces muertos. La hoja guarda finds ya fotografiados en almacén antes de {post} hacia {city}.",
                    "Restricted o precio 0 es un enlace muerto, no una ganga. Sin infradeclaración.",
                ]),
                ("Cómo funciona en este host", [
                    f"Abres un find, lees fotos QC en la app oficial, reservas la línea hacia {label}. {host} solo explica el orden. Pedidos en kakobuy.com.",
                ]),
                ("Qué categorías hay", [
                    "Zapatillas, sudaderas, cazadoras, bolsos — las mismas familias que el desk UK, filtradas por si el SKU sigue en almacén.",
                ]),
                ("¿Es más seguro que buscar a mano?", [
                    f"Más seguro = viste QC antes del flete, no que {customs} desaparezca. Lee {curl} el día del envío. IVA e IOSS cambian; no pegamos un tipo en el title.",
                ]),
                ("Para quién es esta hoja", [
                    f"Quien necesita una prueba de {city} y quien ya usa {a} pero quiere finds + QC + envío en un desk independiente.",
                ]),
                ("Errores sin hoja", [
                    f"Poner un código FR en el estimador, tratar {host} como caja, flete antes del QC. {post} en Collect puede añadir tasa.",
                ]),
                ("Uso eficiente", [
                    f"Spreadsheet, finds y QC juntos. Find aceptado → formulario oficial hacia {label}. Fuente: {customs}. Sin valor declarado inventado.",
                ]),
            ],
        )
    if kind == "finds":
        return (
            f"{a} finds para {label}",
            f"Los finds de {a} en {host} son SKU con QC para una dirección en España, no un segundo catálogo mundial.",
            [
                ("Qué son los finds en este desk", [
                    f"Filas que conservas tras fotos de almacén. Viven en {host} para que España no sea un cambio de nombre de una página UK.",
                ]),
                ("Por qué usar finds curados", [
                    f"La búsqueda manual mezcla Weidian muertos. Aquí solo quedan tarjetas que aún abren en la app oficial antes de {post}.",
                ]),
                ("Categorías", ["Zapatillas y sudaderas dominan porque aún tienen ángulos QC. Restricted fuera."]),
                ("Cómo se eligen", [
                    f"URL viva, al menos una foto de almacén, destino del estimador España — no EU, no este TLD. Precio 0 se cae.",
                ]),
                ("¿Más seguros?", [
                    f"Sigues leyendo {customs} ({curl}) el día del envío. Find = fotografiado en China antes del flete internacional.",
                ]),
                ("Para quién", [
                    f"Quien tiene {city}.",
                ]),
                ("Listo para abrir finds", [
                    "Navegación: QC, luego envío. Registro en kakobuy.com. Este host es información.",
                ]),
            ],
        )
    if kind == "qc":
        return (
            f"{a} QC antes de enviar a {label}",
            f"QC en {host} son fotos de almacén en la app oficial {a}, en China, antes de pagar el flete a {label}.",
            [
                ("Qué es QC aquí", ["Ángulos extra en almacén: costuras, etiquetas, suela. No es un laboratorio ni un escáner de aduanas."]),
                ("Cuándo pedir más fotos", [
                    f"Mientras el SKU sigue en China. Cuando {post} tiene el cartón, {customs} no es la ventana para un retake de almacén.",
                ]),
                ("Qué no hace el QC", [
                    f"No presenta un DUA ni inventa un valor declarado. Fuente: {curl}.",
                ]),
                ("QC y dirección española", [
                    f"Estimador: España. {city}. Un código FR es el país equivocado. El envío se explica en la URL keep de envío.",
                ]),
                ("Ángulos de pago", ["Suelen ser un extra en la app oficial. Este HTML no abre tickets."]),
                ("Si el find falla QC", ["Déjalo en almacén o devuélvelo en la app. No reserves flete internacional sobre un rechazo."]),
                ("¿Enviar después del QC?", [
                    f"Solo entonces el estimador oficial hacia {label}. {host} no cobra.",
                ]),
            ],
        )
    if kind == "shipping":
        return (
            f"{a} envío a {label}",
            f"El envío {a} a {label} es un código de país del estimador, no este TLD. Abre el formulario oficial tras las fotos de almacén.",
            [
                ("Cómo llega un paquete a España", [
                    f"Almacén en China → aceptas QC → reservas línea hacia {label} → {post} en última milla. {host} no imprime un presupuesto en vivo.",
                ]),
                ("Opciones en la app", [
                    "Tax-free / prepaid / collect los dice el SKU. Collect puede añadir tasa de despacho que el estimador oculta.",
                ]),
                ("Plazos", ["El SKU manda. Esta página no inventa días laborables de Correos. Confirma en la app el día del envío."]),
                ("Costes", [
                    f"Flete internacional + lo que diga el SKU en frontera. {post} en Collect puede sumar manejo. No pegamos un arancel en el title.",
                ]),
                ("Aduana e IVA en España", [
                    f"Lee {customs} ({curl}) el día del envío. IVA, IOSS y umbrales cambian. Los artículos de aduana que ya posicionan en este host se conservan.",
                    "Este HTML no enseña a infradeclarar.",
                ]),
                ("Riesgos", [
                    f"País mal elegido en el estimador, flete antes del QC, omitir {city}. Este desk no es Francia.",
                ]),
                ("¿Para el primer pedido?", [
                    f"Sí si {host} es el mapa y kakobuy.com la caja. Prueba de dirección: {city}. Fuente: {customs}.",
                ]),
                ("¿Listo para enviar?", [
                    "QC primero, luego estimador oficial hacia España. Los desks hermanos no son 301 de esta URL.",
                ]),
            ],
        )
    if kind == "legal":
        return (
            f"¿Es legal {a} en {label}?",
            f"{a} es un agente de compras. {host} es un desk informativo, no la app oficial ni {customs}.",
            [
                ("¿Es legal Kakobuy en España?", [
                    f"Usar un agente no es un delito. Restricted, normas de plataforma y el SKU siguen. Lee {curl} el día del envío.",
                ]),
                ("¿Es seguro desde España?", [
                    f"Seguro = QC antes del flete, pago en la app oficial, dirección ES real — no una promesa de que {customs} no ve el cartón.",
                ]),
                ("Riesgos", [
                    f"Enlaces muertos, Collect sin leer el SKU, tratar {host} como caja. {post} puede añadir tasas.",
                ]),
                ("Cómo reducir riesgo", [
                    f"QC en la app, destino España, {city} en la etiqueta. Sin infradeclaración. Sin un euro de AEAT inventado.",
                ]),
                ("Primera compra", [
                    f"Empieza por spreadsheet y finds en este host, luego el registro oficial. {host} no ve tu cuenta.",
                ]),
                ("Veredicto", [
                    f"{a} se puede usar hacia {label} si sigues la app oficial y {customs}. Desk independiente. Texto {TODAY}.",
                ]),
                ("Cómo empezar", ["Spreadsheet → finds → QC → envío. Pedidos solo en kakobuy.com."]),
            ],
        )
    if kind == "guide":
        return (
            f"Guía {a} para {label}",
            f"Pasos para un pedido {a} hacia una dirección en {label} en {host}. No es la caja.",
            [
                ("Cómo comprar en Kakobuy (guía ES)", [
                    f"Encuentra un SKU con QC, envíalo en la app oficial, espera fotos de almacén, reserva flete internacional hacia {label}.",
                ]),
                ("Qué es Kakobuy", [f"Un agente de compras en China. {host} solo explica el desk España. El pago sigue en kakobuy.com."]),
                ("Paso 1 — producto", ["Usa spreadsheet y finds de este host. Salta precio 0 y restricted."]),
                ("Paso 2 — pedido en Kakobuy", ["Solo la app oficial. Este HTML no ve el carrito."]),
                ("Paso 3 — QC en almacén", ["Fotos antes del flete. Ángulos extra a menudo de pago."]),
                ("Paso 4 — envío internacional a España", [
                    f"Destino del estimador ES, dirección {city}. Lee {customs} ({curl}) el día del envío.",
                ]),
                ("Paso 5 — recibir en España", [
                    f"Última milla suele ser {post}. Collect puede añadir tasa. Este desk no rastrea envíos en vivo.",
                ]),
                ("Consejos del primer pedido", [
                    "No pongas un código FR. No reserves flete sobre un QC rechazado. Los hosts hermanos no son 301.",
                ]),
            ],
        )
    return (
        f"FAQ spreadsheet {a} — {label}",
        f"Respuestas cortas para compradores en {label} en {host}.",
        [
            ("¿Necesito cuenta?", [f"Sí, en el sitio oficial de {a}. {host} no crea cuentas."]),
            ("¿Es seguro el primer pedido?", [f"QC antes del flete, destino {label}, {city}. Lee {customs}. Sin valor declarado inventado."]),
            ("¿Cómo encuentro productos fiables?", ["Empieza por spreadsheet y finds de este host."]),
            ("¿Habrá fotos QC?", ["En la app oficial, en China, antes del flete. Ángulos extra a menudo de pago."]),
            ("¿Cuánto tarda el envío a España?", [f"Lo dice el SKU. Esta página no inventa días de {post}."]),
            ("¿Pago IVA o aranceles?", [f"El SKU dice quién paga. Collect puede sumar tasa. Fuente: {customs} ({curl})."]),
            ("¿Hoja o búsqueda a mano?", [f"La hoja en {host} es un índice, no Excel."]),
            ("¿Qué se compra?", ["Zapatillas, sudaderas, cazadoras, bolsos si hay QC. Restricted fuera."]),
        ],
    )


def _sec_fr(kind, host, label, customs, post, city, curl):
    a = "Kakobuy"
    if kind == "spreadsheet":
        return (
            f"{a} spreadsheet — acheteurs en {label}",
            f"Cette page est le spreadsheet {a} pour la France sur {host} — un index, pas Excel, pas une caisse. Keywords : Kakobuy spreadsheet, kakobuy spreadsheet france, kakobuy sheet.",
            [
                ("Qu’est-ce qu’un spreadsheet Kakobuy ?", [
                    f"Sur {host}, un index de SKU déjà passés en QC pour une adresse en {label}. Pas l’app officielle, pas la douane.",
                    "kakobuy.co.uk utilise les trois mêmes mots-clés avec geo uk. Ici le geo reste la France — pas un code postal belge.",
                ]),
                ("Pourquoi un acheteur en France commence par la feuille", [
                    f"Taobao/1688/Weidian à la main mélange des liens morts. La feuille garde les finds photographiés en entrepôt avant {post} vers {city}.",
                    "Restricted ou prix 0 est un lien mort, pas une affaire. Pas de sous-déclaration.",
                ]),
                ("Comment ça marche sur cet hôte", [
                    f"Tu ouvres un find, tu lis les photos QC dans l’app officielle, tu réserves une ligne vers {label}. {host} explique l’ordre. Commandes sur kakobuy.com.",
                ]),
                ("Quelles familles de produits", [
                    "Chaussures, sweats, vestes, sacs — les mêmes familles que le desk UK, filtrées par la dispo entrepôt.",
                ]),
                ("Plus sûr que la recherche manuelle ?", [
                    f"Plus sûr = photos QC avant le fret, pas que {customs} disparaît. Lis {curl} le matin de l’envoi. TVA/IOSS bougent ; on ne colle pas un taux dans le title.",
                ]),
                ("Pour qui", [
                    f"Celui qui a besoin du test d’adresse {city}, et celui qui utilise déjà {a} mais veut finds + QC + livraison sur un desk indépendant.",
                ]),
                ("Erreurs sans feuille", [
                    f"Un code belge dans l’estimateur, prendre {host} pour une caisse, fret avant QC. {post} en Collect peut ajouter des frais.",
                ]),
                ("Usage efficace", [
                    f"Spreadsheet, finds et QC ensemble. Find accepté → formulaire officiel vers {label}. Source : {customs}. Pas de valeur déclarée inventée.",
                ]),
            ],
        )
    if kind == "finds":
        return (
            f"{a} finds pour {label}",
            f"Les finds {a} sur {host} sont des SKU déjà en QC pour une adresse en France, pas un second catalogue mondial.",
            [
                ("Qu’est-ce qu’un find ici", [
                    f"Des lignes gardées après photos d’entrepôt. Elles vivent sur {host} pour que la France ne soit pas un swap de nom d’une page UK.",
                ]),
                ("Pourquoi des finds curatés", [
                    f"La recherche manuelle mélange Weidian morts. Ici ne restent que les cartes qui s’ouvrent encore dans l’app avant {post}.",
                ]),
                ("Catégories", ["Chaussures et sweats dominent tant qu’il reste des angles QC. Restricted dehors."]),
                ("Comment on sélectionne", [
                    f"URL vivante, au moins une photo d’entrepôt, destination estimateur FR — pas BE, pas EU. Prix 0 retiré.",
                ]),
                ("Plus sûr ?", [
                    f"Tu lis quand même {customs} ({curl}) le matin de l’envoi. Find = photographié en Chine avant le fret international.",
                ]),
                ("Pour qui", [f"Qui a {city}. Les hôtes sœurs restent des fichiers séparés — pas de 301."]),
                ("Ouvrir les finds", ["Nav : QC, puis livraison. Inscription sur kakobuy.com. Cet hôte est de l’info."]),
            ],
        )
    if kind == "qc":
        return (
            f"{a} QC avant envoi vers {label}",
            f"Le QC sur {host} ce sont les photos d’entrepôt dans l’app officielle {a}, en Chine, avant de payer le fret vers {label}.",
            [
                ("Le QC sur ce desk", ["Angles supplémentaires en entrepôt. Pas un labo, pas un scanner douane."]),
                ("Quand demander plus de photos", [
                    f"Tant que le SKU est en Chine. Quand {post} a le carton, {customs} n’est pas la fenêtre d’un retake entrepôt.",
                ]),
                ("Ce que le QC ne fait pas", [f"Pas de déclaration en douane, pas de valeur inventée. Source : {curl}."]),
                ("QC et adresse française", [
                    f"Estimateur : France. {city}. Un code belge est le mauvais pays. La livraison est sur la page keep livraison.",
                ]),
                ("Angles payants", ["Souvent un extra dans l’app officielle. Cet HTML n’ouvre pas de ticket."]),
                ("Si le find échoue", ["Laisse-le en entrepôt ou retourne selon l’app. Ne réserve pas le fret international sur un rejet."]),
                ("Expédier après QC ?", [f"Ensuite seulement l’estimateur officiel vers {label}. {host} n’encaisse rien."]),
            ],
        )
    if kind == "shipping":
        return (
            f"{a} livraison vers {label}",
            f"La livraison {a} vers {label} est un code pays de l’estimateur (FR), pas ce TLD. Ouvre le formulaire officiel après les photos d’entrepôt.",
            [
                ("Comment un colis arrive en France", [
                    f"Entrepôt Chine → tu acceptes le QC → tu réserves une ligne vers {label} → {post} au dernier kilomètre. {host} n’imprime pas un devis live.",
                ]),
                ("Options dans l’app", [
                    "Tax-free / prepaid / collect sont sur le SKU. Collect peut ajouter des frais de dédouanement que l’estimateur cache.",
                ]),
                ("Délais", ["Le SKU décide. Cette page n’invente pas les jours Colissimo. Confirme dans l’app le matin de l’envoi."]),
                ("Coûts", [
                    f"Fret international + ce que dit le SKU à la frontière. {post} en Collect peut ajouter des frais. Pas de tarif collé dans le title.",
                ]),
                ("Douane et TVA en France", [
                    f"Lis {customs} ({curl}) le matin de l’envoi. TVA, IOSS et seuils bougent. Les articles douane déjà classés sur cet hôte restent.",
                    "Cet HTML n’apprend pas à sous-déclarer.",
                ]),
                ("Risques", [
                    f"Mauvais pays dans l’estimateur (BE), fret avant QC, omettre {city}. Ce desk n’est pas la Belgique.",
                ]),
                ("Premier achat ?", [
                    f"Oui si {host} est la carte et kakobuy.com la caisse. Test d’adresse : {city}. Source : {customs}.",
                ]),
                ("Prêt à expédier ?", [
                    "QC d’abord, puis estimateur officiel vers FR. Les desks sœurs ne sont pas des 301 de cette URL.",
                ]),
            ],
        )
    if kind == "legal":
        return (
            f"{a} est-il légal en {label} ?",
            f"{a} est un agent d’achat. {host} est un desk d’information, pas l’app officielle ni {customs}.",
            [
                ("Kakobuy est-il légal en France ?", [
                    f"Utiliser un agent n’est pas un délit. Restricted, règles plateforme et SKU restent. Lis {curl} le matin de l’envoi.",
                ]),
                ("Est-ce sûr depuis la France ?", [
                    f"Sûr = QC avant fret, paiement dans l’app, vraie adresse FR — pas une promesse que {customs} ignore le carton.",
                ]),
                ("Risques", [f"Liens morts, Collect sans lire le SKU, {host} comme caisse. {post} peut ajouter des frais."]),
                ("Réduire le risque", [
                    f"QC dans l’app, destination FR, {city} sur l’étiquette. Pas de sous-déclaration. Pas d’euro douane inventé.",
                ]),
                ("Première commande", [f"Spreadsheet et finds sur cet hôte, puis inscription officielle. {host} ne voit pas ton compte."]),
                ("Verdict", [
                    f"{a} peut servir vers {label} si tu suis l’app officielle et {customs}. Desk indépendant. Texte {TODAY}.",
                ]),
                ("Par où commencer", ["Spreadsheet → finds → QC → livraison. Commandes uniquement sur kakobuy.com."]),
            ],
        )
    if kind == "guide":
        return (
            f"Guide {a} pour {label}",
            f"Parcours {a} pour une adresse en {label} sur {host}. Pas la caisse.",
            [
                ("Comment acheter sur Kakobuy (guide FR)", [
                    f"Trouve un SKU avec QC, soumets-le dans l’app, attends les photos d’entrepôt, réserve le fret vers {label}.",
                ]),
                ("Qu’est-ce que Kakobuy", [f"Un agent d’achat en Chine. {host} explique le desk France. Paiement sur kakobuy.com."]),
                ("Étape 1 — produit", ["Spreadsheet et finds de cet hôte. Ignore prix 0 et restricted."]),
                ("Étape 2 — commande", ["App officielle seulement."]),
                ("Étape 3 — QC", ["Photos avant fret. Angles extra souvent payants."]),
                ("Étape 4 — livraison internationale vers la France", [
                    f"Destination estimateur FR, adresse {city}. Lis {customs} ({curl}) le matin de l’envoi.",
                ]),
                ("Étape 5 — réception", [f"Dernier kilomètre souvent {post}. Collect peut ajouter des frais."]),
                ("Conseils première commande", [
                    "Pas de code belge. Pas de fret sur un QC rejeté. Les hôtes sœurs ne sont pas des 301.",
                ]),
            ],
        )
    return (
        f"FAQ spreadsheet {a} — {label}",
        f"Réponses courtes pour les acheteurs en {label} sur {host}.",
        [
            ("Faut-il un compte ?", [f"Oui, sur le site officiel {a}. {host} n’en crée pas."]),
            ("Sûr pour un premier achat ?", [f"QC avant fret, destination {label}, {city}. Lis {customs}. Pas de valeur déclarée inventée."]),
            ("Produits fiables ?", ["Spreadsheet et finds de cet hôte."]),
            ("Photos QC ?", ["Dans l’app officielle, en Chine, avant le fret."]),
            ("Délai vers la France ?", [f"Le SKU décide. Cette page n’invente pas les jours {post}."]),
            ("TVA ou droits ?", [f"Le SKU dit qui paie. Collect peut ajouter des frais. Source : {customs} ({curl})."]),
            ("Feuille ou recherche manuelle ?", [f"La feuille sur {host} est un index, pas Excel."]),
            ("Qu’est-ce qu’on achète ?", ["Chaussures, sweats, vestes, sacs s’il reste du QC. Restricted dehors."]),
        ],
    )


def _sec_nl(kind, host, label, customs, post, city, curl):
    a = "Kakobuy"
    if kind == "spreadsheet":
        return (
            f"{a} spreadsheet — kopers in {label}",
            f"Deze pagina is de {a}-spreadsheet voor Nederland op {host} — een index, geen Excel, geen kassa. Keywords: Kakobuy spreadsheet, kakobuy spreadsheet nederland, kakobuy sheet.",
            [
                ("Wat is een Kakobuy spreadsheet?", [
                    f"Op {host} een index van SKU’s met QC voor een Nederlands adres. Niet de officiële app, geen Douane.",
                    "kakobuy.co.uk gebruikt dezelfde drie keywords met geo uk. Hier blijft de geo Nederland — geen Duitse Packstation, geen Belgische postcode.",
                ]),
                ("Waarom een NL-koper met een sheet begint", [
                    f"Handmatig Taobao/1688/Weidian zoeken mengt dode links. De sheet bewaart finds die al in het magazijn zijn gefotografeerd vóór {post} naar {city}.",
                    "Restricted of prijs 0 is een dode link, geen koopje. Geen onderwaardering.",
                ]),
                ("Hoe het op deze host werkt", [
                    f"Je opent een find, leest QC in de officiële app, boekt een lijn naar {label}. {host} legt alleen de volgorde uit. Bestellen op kakobuy.com.",
                ]),
                ("Welke productfamilies", [
                    "Schoenen, hoodies, jassen, tassen — dezelfde families als het UK-desk, gefilterd op magazijnvoorraad.",
                ]),
                ("Veiliger dan zelf zoeken?", [
                    f"Veiliger = QC-foto’s vóór vracht, niet dat {customs} verdwijnt. Lees {curl} op de verzenddag. BTW/IOSS wijzigen; we plakken geen tarief in de title.",
                ]),
                ("Voor wie", [
                    f"Wie {city} nodig heeft als adrescheck, en wie {a} al gebruikt maar finds + QC + verzending op een onafhankelijke desk wil.",
                ]),
                ("Fouten zonder sheet", [
                    f"Duitse postcode in de estimator, {host} als kassa, vracht vóór QC. {post} kan bij Collect extra innen.",
                ]),
                ("Efficiënt gebruiken", [
                    f"Spreadsheet, finds en QC bij elkaar. Find geaccepteerd → officieel formulier naar {label}. Bron: {customs}. Geen verzonnen aangegeven waarde.",
                ]),
            ],
        )
    if kind == "finds":
        return (
            f"{a} finds voor {label}",
            f"{a}-finds op {host} zijn SKU’s met QC voor een Nederlands adres, geen tweede wereldcatalogus.",
            [
                ("Wat zijn finds op deze desk", [
                    f"Rijen na magazijnfoto’s. Ze staan op {host} zodat Nederland geen naamsverwisseling van een UK-pagina is.",
                ]),
                ("Waarom gecureerde finds", [
                    f"Handmatig zoeken mengt dode Weidian-links. Hier blijven kaarten die nog openen in de app vóór {post}.",
                ]),
                ("Categorieën", ["Schoenen en hoodies domineren zolang er QC-hoeken zijn. Restricted blijft van de sheet."]),
                ("Selectie", [
                    f"Live URL, minstens één magazijnfoto, estimator-bestemming NL — geen DE, geen EU. Prijs 0 valt af.",
                ]),
                ("Veiliger?", [
                    f"Je leest nog steeds {customs} ({curl}) op de verzenddag. Find = in China gefotografeerd vóór internationale vracht.",
                ]),
                ("Voor wie", [f"Wie {city} heeft."]),
                ("Finds openen", ["Nav: QC, dan verzending. Registreren op kakobuy.com. Deze host is informatie."]),
            ],
        )
    if kind == "qc":
        return (
            f"{a} QC vóór verzending naar {label}",
            f"QC op {host} zijn magazijnfoto’s in de officiële {a}-app, in China, vóór je vracht naar {label} betaalt.",
            [
                ("Wat QC hier is", ["Extra hoeken in het magazijn. Geen lab, geen douanescan."]),
                ("Wanneer extra foto’s", [
                    f"Zolang de SKU in China ligt. Als {post} de doos heeft, is {customs} het verkeerde moment voor een magazijn-retake.",
                ]),
                ("Wat QC niet doet", [f"Geen douaneaangifte, geen verzonnen waarde. Bron: {curl}."]),
                ("QC en NL-adres", [
                    f"Estimator: Nederland. {city}. Een Duitse Packstation is het verkeerde land. Verzending staat op de keep-URL.",
                ]),
                ("Betaalde hoeken", ["Vaak een extra in de officiële app. Deze HTML opent geen tickets."]),
                ("Als de find zakt", ["Laat in het magazijn of retour via de app. Boek geen internationale vracht op een afwijzing."]),
                ("Verzenden na QC?", [f"Daarna pas de officiële estimator naar {label}. {host} rekent niets af."]),
            ],
        )
    if kind == "shipping":
        return (
            f"{a} verzending naar {label}",
            f"{a}-verzending naar {label} is een estimator-landcode (NL), niet deze TLD. Open het officiële formulier na magazijnfoto’s.",
            [
                ("Hoe een pakket NL bereikt", [
                    f"Magazijn China → je accepteert QC → je boekt een lijn naar {label} → {post} op de last mile. {host} print geen live quote.",
                ]),
                ("Opties in de app", [
                    "Tax-free / prepaid / collect staan op de SKU. Collect kan een inklaringsfee toevoegen die de estimator verbergt.",
                ]),
                ("Doorlooptijd", ["De SKU bepaalt. Deze pagina verzint geen PostNL-werkdagen. Bevestig in de app op de verzenddag."]),
                ("Kosten", [
                    f"Internationale vracht + wat de SKU aan de grens zegt. {post} kan bij Collect extra innen. Geen tarief in deze title.",
                ]),
                ("Douane en btw in Nederland", [
                    f"Lees {customs} ({curl}) op de verzenddag. Btw, IOSS en drempels wijzigen. Rankende douane-URL’s op deze host blijven.",
                    "Deze HTML leert geen onderwaardering.",
                ]),
                ("Risico’s", [
                    f"Verkeerd land in de estimator (DE), vracht vóór QC, {city} weglaten. Deze desk is geen Duitsland.",
                ]),
                ("Eerste bestelling?", [
                    f"Ja als {host} de kaart is en kakobuy.com de kassa. Adrescheck: {city}. Bron: {customs}.",
                ]),
                ("Klaar om te verzenden?", [
                    "Eerst QC, dan officiële estimator naar NL.",
                ]),
            ],
        )
    if kind == "legal":
        return (
            f"Is {a} legaal in {label}?",
            f"{a} is een inkoopagent. Bestellen op kakobuy.com.",
            [
                ("Is Kakobuy legaal in Nederland?", [
                    f"Een agent gebruiken is geen misdrijf. Restricted, platformregels en de SKU blijven. Lees {curl} op de verzenddag.",
                ]),
                ("Veilig vanuit NL?", [
                    f"Veilig = QC vóór vracht, betalen in de app, echt NL-adres — geen belofte dat {customs} de doos overslaat.",
                ]),
                ("Risico’s", [f"Dode links, Collect zonder SKU te lezen, {host} als kassa. {post} kan fees toevoegen."]),
                ("Risico verlagen", [
                    f"QC in de app, bestemming NL, {city} op het label. Geen onderwaardering. Geen verzonnen Douane-bedrag.",
                ]),
                ("Eerste keer", [f"Begin met spreadsheet en finds op deze host, dan officieel registreren. {host} ziet je account niet."]),
                ("Oordeel", [
                    f"{a} kan naar {label} als je de officiële app en {customs} volgt. Onafhankelijke desk. Tekst {TODAY}.",
                ]),
                ("Starten", ["Spreadsheet → finds → QC → verzending. Bestellingen alleen op kakobuy.com."]),
            ],
        )
    if kind == "guide":
        return (
            f"{a}-gids voor {label}",
            f"Stappen voor een {a}-bestelling naar een adres in {label} op {host}. Geen kassa.",
            [
                ("Hoe kopen via Kakobuy (NL-gids)", [
                    f"Vind een SKU met QC, dien in via de app, wacht op magazijnfoto’s, boek internationale vracht naar {label}.",
                ]),
                ("Wat Kakobuy is", [f"Een China-inkoopagent. {host} legt alleen de NL-desk uit. Betalen op kakobuy.com."]),
                ("Stap 1 — product", ["Spreadsheet en finds van deze host. Sla prijs 0 en restricted over."]),
                ("Stap 2 — bestelling", ["Alleen de officiële app."]),
                ("Stap 3 — QC", ["Foto’s vóór vracht. Extra hoeken vaak betaald."]),
                ("Stap 4 — verzending naar Nederland", [
                    f"Estimator-bestemming NL, adres {city}. Lees {customs} ({curl}) op de verzenddag.",
                ]),
                ("Stap 5 — ontvangen", [f"Last mile vaak {post}. Collect kan extra innen."]),
                ("Tips eerste order", [
                    "Geen Duitse postcode. Geen vracht op afgewezen QC.",
                ]),
            ],
        )
    return (
        f"{a} spreadsheet FAQ — {label}",
        f"Korte antwoorden voor kopers in {label} op {host}.",
        [
            ("Account nodig?", [f"Ja, op de officiële {a}-site. {host} maakt geen accounts."]),
            ("Veilig voor de eerste order?", [f"QC vóór vracht, bestemming {label}, {city}. Lees {customs}. Geen verzonnen waarde."]),
            ("Betrouwbare producten?", ["Spreadsheet en finds van deze host."]),
            ("QC-foto’s?", ["In de officiële app, in China, vóór internationale vracht."]),
            ("Levertijd naar NL?", [f"De SKU bepaalt. Deze pagina verzint geen {post}-dagen."]),
            ("Btw of invoer?", [f"De SKU zegt wie betaalt. Collect kan extra innen. Bron: {customs} ({curl})."]),
            ("Sheet of zelf zoeken?", [f"De sheet op {host} is een index, geen Excel."]),
            ("Wat kopen mensen?", ["Schoenen, hoodies, jassen, tassen als er QC is. Restricted blijft af."]),
        ],
    )


def _nav(d: dict) -> str:
    labels = {
        "spreadsheet": "Spreadsheet",
        "finds": "Finds",
        "qc": "QC",
        "shipping": {"en": "Shipping", "es": "Envío", "fr": "Livraison", "nl": "Verzending", "fi": "Toimitus"}[d["loc"]],
        "legal": {"en": "Is it legal?", "es": "¿Es legal?", "fr": "Est-ce légal ?", "nl": "Is het legaal?", "fi": "Onko se laillista?"}[d["loc"]],
        "guide": {"en": "Guide", "es": "Guía", "fr": "Guide", "nl": "Gids", "fi": "Ohje"}[d["loc"]],
        "faq": "FAQ",
    }
    items = []
    for kind, slug in d["pages"].items():
        items.append(f'<li><a href="/{slug}/">{escape(labels.get(kind, kind))}</a></li>')
    if d["loc"] == "fi":
        items.append('<li><a href="/ohje/">Ohje</a></li>')
    return '<ul class="cluster-links">' + "".join(items) + "</ul>"


def render_article(host: str, kind: str, d: dict) -> str:
    h1, lead, secs = sections_for(kind, d, host)
    loc = d["loc"]
    img, alt = {
        "spreadsheet": ("/media/official-home-20261001.jpg", "Kakobuy"),
        "finds": ("/img/cat/sneakers.jpg", "Kakobuy finds"),
        "qc": ("/media/help-restricted-20261001.jpg", "Kakobuy QC"),
        "shipping": ("/media/estimator-20261001.jpg", "Kakobuy shipping"),
        "legal": ("/media/official-home-20261001.jpg", "Kakobuy"),
        "guide": ("/media/official-home-20261001.jpg", "Kakobuy"),
        "faq": ("/img/cat/hoodie.jpg", "Kakobuy FAQ"),
    }.get(kind, ("/media/official-home-20261001.jpg", "Kakobuy"))
    chunks = [
        f'<article class="cluster-page" data-spreadsheet-cluster="20261030" {MARKER} data-kind="{escape(kind)}">',
        f"<h1>{escape(h1)}</h1>",
        f'<p class="lead">{escape(lead)}</p>',
        f'<figure class="kb-illust"><img src="{img}" alt="{escape(alt)}" width="1400" height="900" loading="lazy" decoding="async"></figure>',
    ]
    for h2, paras in secs:
        chunks.append(f"<h2>{escape(h2)}</h2>")
        for p in paras:
            chunks.append(f"<p>{escape(p)}</p>")
    h2nav = {
        "en": "Spreadsheet / finds / QC / Shipping",
        "es": "Spreadsheet / finds / QC / Envío",
        "fr": "Spreadsheet / finds / QC / Livraison",
        "nl": "Spreadsheet / finds / QC / Verzending",
        "fi": "Spreadsheet / finds / QC / Toimitus",
    }[loc]
    chunks.append(f"<h2>{escape(h2nav)}</h2>")
    chunks.append(_nav(d))
    cta = {
        "en": f"Shop and pay on kakobuy.com. Prices on this page are shown in local currency for {d['label']}.",
        "es": f"Compra y paga en kakobuy.com. Los precios de esta página se muestran en moneda local para {d['label']}.",
        "fr": f"Commande et paiement sur kakobuy.com. Les prix de cette page sont affichés dans la monnaie locale pour {d['label']}.",
        "nl": f"Bestellen en betalen op kakobuy.com. Prijzen op deze pagina staan in lokale valuta voor {d['label']}.",
        "fi": f"Tilaa ja maksa osoitteessa kakobuy.com. Hinnat tällä sivulla näytetään paikallisessa valuutassa.",
    }[loc]
    chunks.append(f'<p class="kb-cta">{escape(cta)}</p>')
    chunks.append("</article>")
    return "\n".join(chunks) + "\n"


MAIN_RE = re.compile(r"(<main\b[^>]*>)(.*?)(</main>)", re.I | re.S)


def swap_main(html: str, inner: str) -> str:
    if not MAIN_RE.search(html):
        raise ValueError("missing <main>")
    return MAIN_RE.sub(lambda m: m.group(1) + "\n" + inner + m.group(3), html, count=1)


def patch_home(host: str, d: dict) -> Path:
    path = overlay(host) / "index.html"
    html = path.read_text(encoding="utf-8")
    serp = cluster_title_serp("Kakobuy", d["dest"], d["loc"], d["label"])
    kws = cluster_keywords("Kakobuy", d["dest"], d["loc"], d["label"])
    html = re.sub(r"<title>[\s\S]*?</title>", f"<title>{escape(serp)}</title>", html, count=1, flags=re.I)
    html = re.sub(
        r'(<meta\s+property="og:title"\s+content=")[^"]*(")',
        rf"\1{escape(serp)}\2",
        html,
        count=1,
        flags=re.I,
    )
    # Keep H1 unsuffixed (kakobuy.co.uk pattern).
    html = re.sub(
        r'<script type="application/ld\+json">([\s\S]*?)</script>',
        _home_ld_replacer(host, serp, kws, d),
        html,
        count=1,
        flags=re.I,
    )
    if MARKER.split("=")[0] not in html:
        html = inject_jsonld(
            html,
            website_ld(
                url=f"https://{host}/",
                name=serp,
                lang=d["lang"],
                brand="Kakobuy",
                host=host,
                keywords=kws,
            ),
        )
        html = html.replace("<body", f"<body {MARKER}", 1)
    path.write_text(html, encoding="utf-8")
    return path


def _home_ld_replacer(host, serp, kws, d):
    def repl(m: re.Match) -> str:
        raw = m.group(1).strip()
        try:
            data = json.loads(raw)
        except json.JSONDecodeError:
            return m.group(0)
        if not isinstance(data, dict):
            return m.group(0)
        if data.get("@type") == "WebPage":
            data["name"] = serp
            part = data.get("isPartOf")
            if isinstance(part, dict):
                part["@type"] = "WebSite"
                part["name"] = serp
                part["url"] = f"https://{host}/"
                part["keywords"] = kws
                data["isPartOf"] = part
        if data.get("@type") == "WebSite":
            data["name"] = serp
            data["keywords"] = kws
            data["url"] = f"https://{host}/"
        return f'<script type="application/ld+json">{json.dumps(data, ensure_ascii=False)}</script>'

    return repl


def deepen_inner(host: str, kind: str, d: dict) -> Path | None:
    slug = d["pages"].get(kind)
    if not slug or slug in d.get("skip", set()):
        return None
    path = overlay(host) / slug / "index.html"
    if not path.is_file():
        print("MISSING", host, slug)
        return None
    html = path.read_text(encoding="utf-8")
    inner = render_article(host, kind, d)
    html = swap_main(html, inner)
    h1, _lead, secs = sections_for(kind, d, host)
    page_url = f"https://{host}/{slug}/"
    html = re.sub(r"<title>[\s\S]*?</title>", f"<title>{escape(h1)}</title>", html, flags=re.I)
    html = re.sub(
        r"(<head>\s*)<title>[\s\S]*?</title>\s*(<meta charset=)",
        r"\1\2",
        html,
        count=1,
        flags=re.I,
    )
    html = re.sub(
        r'(<meta\s+property="og:title"\s+content=")[^"]*(")',
        rf"\1{escape(h1)}\2",
        html,
        count=1,
        flags=re.I,
    )
    html = re.sub(
        r'(<meta\s+property="og:url"\s+content=")[^"]*(")',
        rf"\1{page_url}\2",
        html,
        count=1,
        flags=re.I,
    )
    html = re.sub(
        r'(<link\s+rel="canonical"\s+href=")[^"]*(")',
        rf"\1{page_url}\2",
        html,
        count=1,
        flags=re.I,
    )
    html = re.sub(
        r'<script type="application/ld\+json">([\s\S]*?)</script>',
        _inner_ld_replacer(page_url, h1),
        html,
        count=1,
        flags=re.I,
    )
    if kind == "faq" and '"FAQPage"' not in html:
        pairs = [(h2, " ".join(paras)) for h2, paras in secs]
        html = inject_jsonld(html, faq_ld(d["lang"], pairs))
    path.write_text(html, encoding="utf-8")
    return path


def _inner_ld_replacer(page_url: str, h1: str):
    def repl(m: re.Match) -> str:
        raw = m.group(1).strip()
        try:
            data = json.loads(raw)
        except json.JSONDecodeError:
            return m.group(0)
        if isinstance(data, dict) and data.get("@type") == "WebPage":
            data["@id"] = page_url
            data["url"] = page_url
            data["name"] = h1
        return f'<script type="application/ld+json">{json.dumps(data, ensure_ascii=False)}</script>'

    return repl


def bump_sitemap(host: str, d: dict) -> None:
    path = overlay(host) / "sitemap.xml"
    if not path.is_file():
        return
    sm = path.read_text(encoding="utf-8")
    locs = [f"https://{host}/"] + [f"https://{host}/{slug}/" for slug in d["pages"].values()]
    for loc in locs:
        sm = re.sub(
            rf"(<loc>\s*{re.escape(loc)}\s*</loc>\s*<lastmod>)[^<]+",
            rf"\g<1>{TODAY}",
            sm,
        )
        if loc not in sm and "</urlset>" in sm:
            sm = sm.replace(
                "</urlset>",
                "  <url>\n"
                f"    <loc>{loc}</loc>\n"
                f"    <lastmod>{TODAY}</lastmod>\n"
                "    <changefreq>weekly</changefreq>\n"
                "    <priority>0.8</priority>\n"
                "  </url>\n</urlset>",
                1,
            )
    path.write_text(sm, encoding="utf-8")


def generate() -> list[Path]:
    written: list[Path] = []
    for host in ORDER:
        d = HOSTS[host]
        ohje = overlay(host) / "ohje" / "index.html"
        ohje_hash = ohje.read_bytes() if ohje.is_file() else None
        written.append(patch_home(host, d))
        print("HOME", host, cluster_title_serp("Kakobuy", d["dest"], d["loc"], d["label"]))
        for kind in d["pages"]:
            p = deepen_inner(host, kind, d)
            if p:
                written.append(p)
                print("INNER", host, kind, p.relative_to(ROOT))
        bump_sitemap(host, d)
        sm = overlay(host) / "sitemap.xml"
        if sm.is_file():
            written.append(sm)
        if ohje_hash is not None and ohje.read_bytes() != ohje_hash:
            raise SystemExit(f"refused to smash unique /ohje/ on {host}")
    return written


def put(files: list[Path] | None = None) -> None:
    if files is None:
        files = generate()
    client = _connect()
    stamp = time.strftime("%Y%m%d-%H%M%S")
    bak = f"/www/backup/kakobuy-five-dest-{stamp}"
    print(_run(client, f"mkdir -p '{bak}'"))
    sftp = client.open_sftp()
    n = 0
    for path in files:
        rel = path.relative_to(ROOT / "sites").as_posix()  # host/overlay/...
        host = rel.split("/", 1)[0]
        rest = path.relative_to(overlay(host)).as_posix()
        remote = f"/www/wwwroot/{host}/{rest}"
        _run(client, f"mkdir -p '{str(Path(remote).parent)}'")
        _run(client, f"test -f '{remote}' && mkdir -p '{bak}/{host}' && cp -a '{remote}' '{bak}/{host}/{rest.replace('/', '_')}' || true")
        sftp.put(str(path), remote)
        _run(client, f"chown www:www '{remote}'")
        n += 1
        print("PUT", remote)
    sftp.close()
    client.close()
    print("PUT_DONE", n, "backup", bak)


def verify() -> None:
    from urllib.request import Request, build_opener, HTTPSHandler, HTTPRedirectHandler

    class NoRedir(HTTPRedirectHandler):
        def redirect_request(self, *a, **k):
            return None

    opener = build_opener(NoRedir(), HTTPSHandler())
    checks = [
        ("https://kakospreadsheet.fr/", "Kakobuy Spreadsheet pour acheteurs en France"),
        ("https://kakospreadsheet.nl/", "Kakobuy Spreadsheet voor kopers in Nederland"),
        ("https://kakobuy.fi/", "Finds ja QC"),
        ("https://kakospreadsheet.ca/", "Best Finds"),
        ("https://kakospreadsheet.es/", "Mejores finds y QC"),
        ("https://kakobuy.fi/faq/", "FAQ"),
        ("https://kakobuy.fi/kakobuy-spreadsheet/", "spreadsheet"),
        ("https://kakobuy.fi/ohje/", "Ohje"),
        ("https://kakospreadsheet.fr/kakobuy-finds/", "finds"),
        ("https://kakospreadsheet.fr/kakobuy-faq/", "FAQPage"),
        ("https://kakospreadsheet.nl/kakobuy-verzending/", "verzending"),
        ("https://kakospreadsheet.nl/kakobuy-guide/", "Gids"),
        ("https://kakospreadsheet.es/envio-kakobuy-espana/", "Envío"),
        ("https://kakospreadsheet.ca/kakobuy-shipping-to-canada/", "Canada"),
    ]
    for url, needle in checks:
        try:
            r = opener.open(Request(url, headers={"User-Agent": "kakobuy-five/1.0"}), timeout=20)
            body = r.read().decode("utf-8", "replace")
            desk = r.headers.get("X-Desk")
            ok = needle.lower() in body.lower()
            print("VERIFY", r.status, url, "desk", desk, "hit", ok, "five", MARKER.split("=")[0] in body)
        except Exception as exc:
            from urllib.error import HTTPError

            if isinstance(exc, HTTPError):
                print("VERIFY", exc.code, url, exc.headers.get("Location"))
            else:
                print("VERIFY_ERR", url, type(exc).__name__, str(exc)[:120])


def gsc_submit() -> None:
    if not Path(SA).is_file():
        print("GSC_SKIP no sa.json")
        return
    try:
        from google.oauth2 import service_account
        from googleapiclient.discovery import build
    except ImportError:
        import subprocess

        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "google-api-python-client", "google-auth", "-q"]
        )
        from google.oauth2 import service_account
        from googleapiclient.discovery import build

    creds = service_account.Credentials.from_service_account_file(
        SA, scopes=["https://www.googleapis.com/auth/webmasters"]
    )
    gsc = build("searchconsole", "v1", credentials=creds, cache_discovery=False)
    listed = {row["siteUrl"] for row in gsc.sites().list().execute().get("siteEntry", [])}
    for host in ORDER:
        site = f"sc-domain:{host}" if f"sc-domain:{host}" in listed else f"https://{host}/"
        feed = f"https://{host}/sitemap.xml"
        try:
            gsc.sitemaps().submit(siteUrl=site if site in listed else f"https://{host}/", feedpath=feed).execute()
            print("SITEMAP", host, site)
        except Exception as exc:  # noqa: BLE001
            print("SITEMAP_FAIL", host, type(exc).__name__, str(exc)[:180])
        time.sleep(0.35)


def main() -> None:
    cmd = sys.argv[1] if len(sys.argv) > 1 else "all"
    if cmd == "reclaim":
        reclaim_nginx()
    elif cmd == "generate":
        generate()
    elif cmd == "put":
        put()
    elif cmd == "verify":
        verify()
    elif cmd == "gsc":
        gsc_submit()
    elif cmd == "all":
        reclaim_nginx()
        files = generate()
        put(files)
        verify()
        gsc_submit()
    else:
        raise SystemExit(f"unknown {cmd}")


if __name__ == "__main__":
    main()
