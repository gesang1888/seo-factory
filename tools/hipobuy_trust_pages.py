#!/usr/bin/env python3
"""Build HipoBuy country-desk help / news / about pages (ES-style trust blocks).

Local language per TLD. Does not PUT hipobuyspreadsheet.net.
No under-declaration coaching. Invite stays in body, not titles.
"""
from __future__ import annotations

import os
import re
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from hipobuy_desk_copy import DATE, lab_block  # noqa: E402

EST = "https://hipobuy.com/estimation"
REG = "https://hipobuy.com/register?inviteCode=VGEICZNX0"
OFFICIAL = "https://hipobuy.com/"
HELP_OFF = "https://hipobuy.com/help"
DISCORD = "https://discord.gg/ePA4XhmBWX"
REDDIT = "https://www.reddit.com/r/Hipobuy_/"
NET = "https://hipobuyspreadsheet.net/"
INVITE = "VGEICZNX0"

HOSTS = {
    "at": {
        "host": "hipobuy.at",
        "lang": "de-AT",
        "howto": "/www/wwwroot/hipobuy.at/how-to-use-hipobuy/index.html",
        "ship": "/www/wwwroot/hipobuy.at/hipobuy-shipping-guide/index.html",
        "overlay": ROOT / "sites/hipobuy.at/overlay/index.html",
        "slugs": {"help": "hilfe", "news": "neuigkeiten", "about": "ueber-uns"},
        "dest": "AT",
        "dest_label": "Österreich",
        "lines": 14,
        "cheap": "AT AIR DHL-HIPO-EUCR1T",
        "usd": 33.96,
        "days": "10–16",
        "customs": "https://www.bmf.gv.at/themen/zoll.html",
        "ioss": "https://taxation-customs.ec.europa.eu/vat-e-commerce_en",
    },
    "nl": {
        "host": "hipobuyspreadsheet.nl",
        "lang": "nl-NL",
        "howto": "/www/wwwroot/hipobuyspreadsheet.nl/how-to-use-hipobuy/index.html",
        "ship": "/www/wwwroot/hipobuyspreadsheet.nl/hipobuy-shipping-guide/index.html",
        "overlay": ROOT / "sites/hipobuyspreadsheet.nl/overlay/index.html",
        "slugs": {"help": "hulp", "news": "nieuws", "about": "over-ons"},
        "dest": "NL",
        "dest_label": "Nederland",
        "lines": 20,
        "cheap": "NL AIR DHL-HIPO-EUCR1T",
        "usd": 34.20,
        "days": "10–16",
        "customs": "https://www.belastingdienst.nl/wps/wcm/connect/nl/douane/douane",
        "ioss": "https://taxation-customs.ec.europa.eu/vat-e-commerce_en",
    },
    "uk": {
        "host": "hipobuyspreadsheet.co.uk",
        "lang": "en-GB",
        "howto": "/www/wwwroot/hipobuyspreadsheet.co.uk/how-to-use-hipobuy/index.html",
        "ship": "/www/wwwroot/hipobuyspreadsheet.co.uk/hipobuy-shipping-guide/index.html",
        "overlay": ROOT / "sites/hipobuyspreadsheet.co.uk/overlay/index.html",
        "slugs": {"help": "help", "news": "news", "about": "who-we-are"},
        "dest": "GB",
        "dest_label": "United Kingdom",
        "lines": 16,
        "cheap": "HIPO-RoyalMail-GB-1",
        "usd": 23.83,
        "days": "7–13",
        "customs": "https://www.gov.uk/goods-sent-from-abroad",
        "ioss": "",
        "job": "coupons",
    },
    "eu": {
        "host": "hipobuyspreadsheet.eu",
        "lang": "en",
        "howto": "/www/wwwroot/hipobuyspreadsheet.eu/how-to-use-hipobuy/index.html",
        "ship": "/www/wwwroot/hipobuyspreadsheet.eu/hipobuy-shipping-guide/index.html",
        "overlay": ROOT / "sites/hipobuyspreadsheet.eu/overlay/index.html",
        "slugs": {"help": "help", "news": "news", "about": "who-we-are"},
        "dest": None,
        "dest_label": "a member state",
        "lines": None,
        "cheap": None,
        "usd": None,
        "days": None,
        "customs": "https://taxation-customs.ec.europa.eu/vat-e-commerce_en",
        "ioss": "https://taxation-customs.ec.europa.eu/vat-e-commerce_en",
        "job": "coupons",
    },
    "us": {
        "host": "hipobuyspreadsheet.us",
        "lang": "en-US",
        "howto": "/www/wwwroot/hipobuyspreadsheet.us/how-to-use-hipobuy/index.html",
        "ship": "/www/wwwroot/hipobuyspreadsheet.us/hipobuy-shipping-guide/index.html",
        "overlay": ROOT / "sites/hipobuyspreadsheet.us/overlay/index.html",
        "slugs": {"help": "help", "news": "news", "about": "who-we-are"},
        "dest": "US",
        "dest_label": "the United States",
        "lines": 8,
        "cheap": "US AIR USPS-ZF1",
        "usd": 32.82,
        "days": "11–23",
        "customs": "https://www.cbp.gov/travel/international-visitors/kbyg/customs-duty-info",
        "ioss": "",
    },
    "ukhaul": {
        "host": "hipobuyspreadsheets.uk",
        "lang": "en-GB",
        "howto": "/www/wwwroot/hipobuyspreadsheets.uk/how-to-use-hipobuy/index.html",
        "ship": "/www/wwwroot/hipobuyspreadsheets.uk/hipobuy-shipping-guide/index.html",
        "overlay": ROOT / "sites/hipobuyspreadsheets.uk/overlay/index.html",
        "slugs": {"help": "help", "news": "news", "about": "who-we-are"},
        "dest": "GB",
        "dest_label": "the United Kingdom",
        "lines": 16,
        "cheap": "HIPO-RoyalMail-GB-1",
        "usd": 23.83,
        "days": "7–13",
        "customs": "https://www.gov.uk/goods-sent-from-abroad",
        "ioss": "",
        "job": "haul",
    },
}

OUT = Path("/tmp/cms-trust")


def _wc(html: str) -> int:
    text = re.sub(r"<[^>]+>", " ", html)
    return len(re.findall(r"[A-Za-zÄÖÜäöüßéèêáàóòúùíìç0-9']+", text))


def _art(h1: str, blocks: list[str]) -> str:
    body = "\n".join(blocks)
    return (
        '<article class="hipo-howto" style="max-width:760px;margin:40px auto;'
        'padding:0 24px 64px;text-align:left">\n'
        f'<h1 style="font-size:clamp(24px,3.5vw,36px);font-weight:600;'
        f'letter-spacing:-.7px;margin-bottom:14px;text-align:left">{h1}</h1>\n'
        f"{body}\n</article>\n"
    )


def _p(t: str) -> str:
    if t.startswith("<"):
        return t
    return f'<p class="pp">{t}</p>'


def _h2(t: str) -> str:
    return f'<h2 class="ph">{t}</h2>'


def _h3(t: str) -> str:
    return f'<h3 class="ph">{t}</h3>'


def _links(d: dict, extra: str = "") -> str:
    s = d["slugs"]
    host = d["host"]
    lang = d.get("lang", "en")
    if lang.startswith("de"):
        nav = (
            f'<a href="/{s["help"]}/">Hilfe</a> · '
            f'<a href="/{s["news"]}/">Neuigkeiten</a> · '
            f'<a href="/{s["about"]}/">Über uns</a> · '
            f'<a href="/hipobuy-shipping-guide/">Versand</a> · '
            f'<a href="{EST}">Offizieller Schätzer</a> · '
            f'<a href="{REG}">Registrieren</a> · '
            f'<a href="{NET}">Finds-Hub</a>'
        )
        indep = (
            f"Unabhängiger Desk auf {host}. Wir führen dein HipoBuy-Konto nicht. "
            f"Invite {INVITE} kann diesem Desk eine Provision bringen, wenn du darüber registrierst; "
            "ohne Code geht es auf hipobuy.com. Keine Unterdeklaration."
        )
    elif lang.startswith("nl"):
        nav = (
            f'<a href="/{s["help"]}/">Hulp</a> · '
            f'<a href="/{s["news"]}/">Nieuws</a> · '
            f'<a href="/{s["about"]}/">Over ons</a> · '
            f'<a href="/hipobuy-shipping-guide/">Verzending</a> · '
            f'<a href="{EST}">Officiële estimator</a> · '
            f'<a href="{REG}">Registreren</a> · '
            f'<a href="{NET}">Finds-hub</a>'
        )
        indep = (
            f"Onafhankelijke desk op {host}. Wij beheren je HipoBuy-account niet. "
            f"Invite {INVITE} kan commissie opleveren als je via die URL registreert; "
            "zonder code kan ook. Geen onderwaarderingstips."
        )
    else:
        nav = (
            f'<a href="/{s["help"]}/">Help</a> · '
            f'<a href="/{s["news"]}/">News</a> · '
            f'<a href="/{s["about"]}/">Who we are</a> · '
            f'<a href="/hipobuy-shipping-guide/">Shipping</a> · '
            f'<a href="{EST}">Official estimator</a> · '
            f'<a href="{REG}">Register</a> · '
            f'<a href="{NET}">Finds hub</a>'
        )
        indep = (
            f"Independent desk on {host}. We do not run your HipoBuy account. "
            f"Invite {INVITE} may earn this desk a commission if you register through it; "
            "you can join at hipobuy.com without it. No declared-value coaching."
        )
    return f'<p class="pp">{extra}{nav}</p><p class="pp">{indep}</p>'


def help_at(d: dict) -> tuple[str, str, str]:
    title = "Hilfe: fünfzehn Fragen zu HipoBuy in Österreich"
    desc = (
        "FAQ für eine österreichische Lieferadresse: zwei Zahlungen, USD-Zahlen, "
        "Volumengewicht, Zoll/MwSt ohne Unterdeklaration. Stand 29 Sep 2026."
    )
    s = d["slugs"]
    blocks = [
        _p(
            "Diese Seite gilt für eine <strong>österreichische Straße</strong> auf hipobuy.at. "
            "Wir sehen dein Konto nicht. Bestellungen, Zahlungen und Reklamationen laufen nur auf "
            f'<a href="{OFFICIAL}">hipobuy.com</a>.'
        ),
        _h2("Was HipoBuy ist, und in welcher Sprache"),
        _h3("Verkauft HipoBuy die Ware selbst?"),
        _p(
            "Nein. HipoBuy ist ein Einkaufsagent: er kauft in chinesischen Drittshops in deinem "
            "Namen und lagert, bis du eine internationale Linie buchst. Qualität und Echtheit "
            "stehen in der Plattform-Hilfe, nicht in diesem Desk."
        ),
        _h3("Kann ich die App auf Deutsch stellen?"),
        _p(
            "Der Sprachwähler der Plattform listet unter anderem Deutsch. Wir haben am "
            f"{DATE} die AT-Linien über die öffentliche Schätz-API gemessen — Feldnamen dort "
            "bleiben englisch. Die Lieferadresse muss trotzdem AT-Format haben."
        ),
        _h3("Warum findet der Katalog nichts auf Deutsch?"),
        _p(
            "Der Index, den die Spreadsheet-Suche nutzt, ist englisch (sneakers, hoodie, jacket). "
            "Deutsche Wörter wie Turnschuhe oder Kapuzenpullover liefern oft eine leere Grid. "
            "Am 30.&nbsp;Sep.&nbsp;2026 war /api/products/ auf diesem Host 404, bis nginx die PHP-Datei "
            "erreichte; danach kamen englische Titel aus w2clinks zurück."
        ),
        _h2("Was du zahlst"),
        _h3("Wie oft wird kassiert?"),
        _p(
            "Zweimal: zuerst Ware plus Inlandversand in China, später der internationale Versand "
            "nach den Lagerfotos. Dazwischen kannst du mehrere Teile im Lager sammeln."
        ),
        _h3("Warum stehen überall Dollar?"),
        _p(
            "USD ist die Standardwährung der Plattform. Am 29.&nbsp;Aug.&nbsp;2026 (gleiche Messung "
            "wie auf hipobuy.es dokumentiert) änderte der Euro-Schalter nur das Symbol, nicht die "
            "Zahl. Lies Beträge als Dollar; die Umrechnung macht Bank oder Zahlungsart. Deshalb "
            "steht unsere Labortabelle in USD."
        ),
        _h3("Was ist Volumengewicht?"),
        _p(
            f"L×B×H/8000 auf den meisten Luftlinien (manchmal /6000). Es wird das Maximum aus "
            f"Istgewicht und Volumen berechnet. Unser Laborkarton {DATE} (1000&nbsp;g, 35×25×10&nbsp;cm) "
            f"wurde nach Österreich oft mit 1100&nbsp;g Volumen abgerechnet. "
            f'<a href="{EST}">Schätzer vor dem Buchen öffnen</a>.'
        ),
        _h2("Zoll und MwSt in Österreich"),
        _h3("Wer zahlt Abgaben?"),
        _p(
            "Das steht auf der gebuchten Linie: ohne Abgaben, vorausbezahlt, oder zu Lasten des "
            "Empfängers. Im letzten Fall kann der Zusteller vor der Übergabe kassieren — inkl. "
            "einer Bearbeitungsgebühr, die der Schätzer oft nicht zeigt. "
            f'<a href="{d["customs"]}">BMF Zoll</a> und die '
            f'<a href="{d["ioss"]}">IOSS-Hinweise der Kommission</a> (Orientierung 150&nbsp;€ für '
            f"bestimmte Fernverkäufe) sind die Quellen für das, was wir nicht selbst messen. "
            f"<strong>Keine Tipps zur Unterdeklaration.</strong>"
        ),
        _h2("Lager, Fotos, was reisen darf"),
        _h3("Kann ich mehrere Bestellungen in einem Karton bündeln?"),
        _p(
            "Ja, das ist der übliche Sparweg. Teile bleiben im Lager, bis du den internationalen "
            "Versand auslöst. Maximale Lagerdauer steht in der offiziellen Hilfe und kann sich ändern."
        ),
        _h3("Gibt es QC-Fotos?"),
        _p(
            "Die Plattform fotografiert Ware im Lager. Der Detailgrad variiert; Extra-Fotos sind "
            "ein Zusatzdienst. Reklamationen sind einfacher, solange die Ware noch in China liegt."
        ),
        _h3("Was darf nicht?"),
        _p(
            "Tabak, Alkohol, Arzneimittel und verbotene Artikel reisen nicht. Flüssigkeiten, "
            "Pulver und Pasten können Gefahrgut-Papiere brauchen. Das ist Plattformregel, nicht AT-Zollrecht."
        ),
        _h2("Wenn etwas nicht stimmt"),
        _h3("Das Paket ist leichter als geschätzt"),
        _p(
            "Die offizielle FAQ hat einen Eintrag zu geschätztem versus tatsächlichem Gewicht und "
            "zu Porto-Rückerstattung. Lies dort, nicht in einem Screenshot dieser HTML-Seite."
        ),
        _h3("Wo reklamiere ich?"),
        _p(
            f"Nur auf hipobuy.com, nicht hier. Offizielle Hilfe: <a href=\"{HELP_OFF}\">{HELP_OFF}</a>. "
            f'Discord <a href="{DISCORD}">HipoBuy</a>, Reddit <a href="{REDDIT}">r/Hipobuy_</a>.'
        ),
        _h3("Gehört der Invite in den Title?"),
        _p(
            f"Nein. Code {INVITE} steht im Coupon-Artikel und wird in der App neu eingegeben."
        ),
        _h2("Schätzer und Tickets"),
        _p(
            f"Öffne <a href=\"{EST}\">hipobuy.com/estimation</a> mit Ziel Austria, nachdem QC-Fotos da sind. "
            "Im Support-Ticket immer Austria schreiben, nicht Germany, auch wenn DHL last-mile ähnlich aussieht. "
            "Zwei Kartons nach einem QC-Split heißen zwei Schätzungen — operateFee kann sich verdoppeln. "
            "LitBuy.at bleibt ein anderer Agent. Der Finds-Katalog mit Tausenden Zeilen bleibt auf "
            f'<a href="{NET}">hipobuyspreadsheet.net</a>. hipobuyspreadsheet.nl und .eu sind eigene Desks, kein 301.'
        ),
        _p(
            "Die englische 700-g-USA-Tabelle auf der Versandseite ist eine Hülle. Für Österreich gilt die "
            f"Labortabelle vom {DATE} und danach die Live-SKU. Versicherung entscheidest du in HipoBuy pro Linie, "
            "nicht als Pauschalsatz auf dieser FAQ."
        ),
        _p(
            f'<a href="/{s["news"]}/">Neuigkeiten mit Datum</a> · '
            f'<a href="/{s["about"]}/">Wer wir sind</a> · '
            f'<a href="/hipobuy-shipping-guide/">AT-Versandlabor</a> · '
            f'<a href="/how-to-use-hipobuy/">Ablauf</a>'
        ),
        _links(d),
    ]
    return title, desc, _art(title, blocks)


def help_nl(d: dict) -> tuple[str, str, str]:
    title = "Hulp: vijftien vragen over HipoBuy in Nederland"
    desc = (
        "FAQ voor een Nederlands huisadres: twee betalingen, USD-cijfers, volumgewicht, "
        "btw/douane zonder onderwaardering. Stand 29 sep 2026."
    )
    s = d["slugs"]
    blocks = [
        _p(
            "Deze pagina hoort bij een <strong>Nederlands huisadres</strong> op hipobuyspreadsheet.nl. "
            "Wij zien je account niet. Bestellen, betalen en claims gaan alleen via "
            f'<a href="{OFFICIAL}">hipobuy.com</a>.'
        ),
        _h2("Wat HipoBuy is"),
        _h3("Verkoopt HipoBuy de spullen zelf?"),
        _p(
            "Nee. Het is een inkoopagent: hij koopt in Chinese shops op jouw naam en houdt de "
            "goederen in het magazijn tot jij een internationale lijn boekt."
        ),
        _h3("Kan de app in het Nederlands?"),
        _p(
            "De taalkiezer van het officiële site bevat onder meer Nederlands. Onze meting "
            f"{DATE} liep via de publieke estimator-API met bestemming NL; veldnamen daar blijven Engels. "
            "Het adres moet wél NL-formaat zijn."
        ),
        _h3("Waarom is de catalogus leeg in het Nederlands?"),
        _p(
            "De zoekindex is Engels (sneakers, hoodie). Nederlandse woorden geven vaak 0 hits. "
            "Op 30&nbsp;sep&nbsp;2026 gaf /api/products/ op dit host 404 totdat nginx de PHP-file "
            "aanbood; daarna kwamen Engelse titels van w2clinks."
        ),
        _h2("Wat je betaalt"),
        _h3("Hoe vaak betaal ik?"),
        _p(
            "Twee keer: eerst product plus binnenlands China-vervoer, later internationaal na de "
            "magazijnfoto’s. Daartussen kun je items bundelen."
        ),
        _h3("Waarom dollars?"),
        _p(
            "USD is de standaard. De euro-schakelaar veranderde in de Aug-2026-check alleen het "
            "symbool, niet het getal. Lees bedragen als dollars. Onze labtabel staat daarom in USD. "
            f'<a href="{EST}">Open de officiële estimator vóór je boekt</a>.'
        ),
        _h3("Volumgewicht?"),
        _p(
            f"L×B×H/8000 op de meeste luchtlijnen. Factuur = max(ist, volume). Labkarton {DATE} "
            f"1000&nbsp;g / 35×25×10&nbsp;cm naar NL werd vaak 1100&nbsp;g volume."
        ),
        _h2("Btw en douane in Nederland"),
        _h3("Wie betaalt invoer?"),
        _p(
            "Dat staat op de geboekte lijn. Sommige SKU’s zijn prepaid, andere laten de last-mile "
            "innen vóór bezorging — plus een mogelijke behandelingsfee die de estimator niet toont. "
            f'<a href="{d["customs"]}">Belastingdienst Douane</a> en de '
            f'<a href="{d["ioss"]}">IOSS-toelichting van de Commissie</a> (vaak 150&nbsp;€ als '
            "oriëntatie voor bepaalde zendingen) zijn de bronnen voor wat wij niet zelf meten. "
            "<strong>Geen tips voor onderwaardering.</strong>"
        ),
        _h2("Magazijn en foto’s"),
        _h3("Bundelen?"),
        _p("Ja. Artikelen blijven in China tot jij verzending start. Maximale opslagtijd: officiële help."),
        _h3("QC-foto’s?"),
        _p("Ja, plus optionele extra foto’s. Returns zijn makkelijker zolang de goederen in het magazijn liggen."),
        _h3("Wat mag niet mee?"),
        _p("Tabak, alcohol, geneesmiddelen, verboden goederen. Vloeistoffen/poeders kunnen extra papier vragen."),
        _h2("Als het misgaat"),
        _h3("Lichter dan geschat?"),
        _p("Officiële FAQ over geschat vs echt gewicht en portoteruggave — niet dit HTML-bestand."),
        _h3("Waar claim ik?"),
        _p(
            f'Alleen hipobuy.com. Hulp: <a href="{HELP_OFF}">{HELP_OFF}</a>. '
            f'<a href="{DISCORD}">Discord</a> · <a href="{REDDIT}">Reddit</a>.'
        ),
        _h3("Hoort de invite in de title?"),
        _p(
            f"Nee. Code {INVITE} staat op de coupon-URL en typ je opnieuw in de app."
        ),
        _h2("Estimator en tickets"),
        _p(
            f'Open <a href="{EST}">hipobuy.com/estimation</a> met bestemming Netherlands nadat de QC-foto’s er zijn. '
            "In een supportticket schrijf je Netherlands, niet Belgium of EU, ook als DHL last-mile lijkt. "
            "Twee dozen na een QC-split zijn twee schattingen — operateFee kan verdubbelen. "
            "ootdbuy.nl is een andere agent. De finds-catalogus blijft op "
            f'<a href="{NET}">hipobuyspreadsheet.net</a>. hipobuy.at en .eu zijn eigen desks, geen 301.'
        ),
        _p(
            "De Engelse 700-g-USA-tabel op sommige templates is een restant. Voor Nederland geldt de "
            f"labtabel van {DATE} en daarna de live-SKU. Verzekering kies je in HipoBuy per lijn, "
            "niet als forfait op deze FAQ."
        ),
        _p(
            f'<a href="/{s["news"]}/">Nieuws met datum</a> · '
            f'<a href="/{s["about"]}/">Over ons</a> · '
            f'<a href="/hipobuy-shipping-guide/">NL-labtabel</a>'
        ),
        _links(d),
    ]
    return title, desc, _art(title, blocks)


def help_en(d: dict, flavour: str) -> tuple[str, str, str]:
    host = d["host"]
    if flavour == "us":
        title = "Help: fifteen questions about HipoBuy to the United States"
        where = "a <strong>US street address</strong> on hipobuyspreadsheet.us"
        tax_h = "CBP and duties — educational"
        tax_b = (
            f'US treatment follows the booked SKU. Read <a href="{d["customs"]}">CBP duty basics</a>. '
            "This desk does not invent a de-minimis dollar figure for your carton. "
            "<strong>No under-declaration tips.</strong>"
        )
        cat = "English (sneakers, hoodie). /api/products/ on this host 404ed until 30 Sep 2026 nginx rewrite."
    elif flavour == "eu":
        title = "Help: fifteen questions on the HipoBuy EU coupon desk"
        where = "a <strong>member-state address</strong> on hipobuyspreadsheet.eu — the TLD is not a destination"
        tax_h = "VAT / IOSS — educational"
        tax_b = (
            f'The Commission explains IOSS for certain low-value distance sales '
            f'(often discussed around €150) at <a href="{d["ioss"]}">{d["ioss"]}</a>. '
            "The estimator still needs a country code (ES, IE, IT…), not “EU”. Spain-specific freight "
            "copy lives on hipobuy.es, not here. <strong>No declared-value coaching.</strong>"
        )
        cat = "English index. Spanish/French/German queries often return zero cards. Coupon desk does not clone hipobuy.es."
    elif flavour == "haul":
        title = "Help: fifteen questions on the HipoBuy UK haul log"
        where = "the <strong>Nominet haul log</strong> on hipobuyspreadsheets.uk — not the .co.uk coupon desk"
        tax_h = "HMRC — educational"
        tax_b = (
            f'UK import VAT/duty follow the carrier product. <a href="{d["customs"]}">GOV.UK goods sent from abroad</a>. '
            "Northern Ireland is often another SKU. <strong>No declared-value coaching.</strong>"
        )
        cat = "English catalogue index. This host’s /api/products/ 404ed until 30 Sep 2026."
    else:
        title = "Help: fifteen questions on the HipoBuy UK spreadsheet desk"
        where = "the <strong>.co.uk coupon and sizing desk</strong> — not a redirect onto hipobuyspreadsheets.uk"
        tax_h = "HMRC — educational"
        tax_b = (
            f'UK import rules follow the booked line. <a href="{d["customs"]}">GOV.UK goods sent from abroad</a>. '
            "Royal Mail versus Evri dollars live on the haul-log lab. <strong>No declared-value coaching.</strong>"
        )
        cat = "English catalogue. Coupons and UK 8 sizing are this host’s ranked jobs."
    desc = title + f" Dated {DATE}. Independent desk on {host}."
    s = d["slugs"]
    blocks = [
        _p(f"This FAQ is for {where}. We cannot see your HipoBuy account. Orders stay on hipobuy.com."),
        _h2("What HipoBuy is"),
        _h3("Does HipoBuy sell the items?"),
        _p(
            "No. It is a purchasing agent: it buys from third-party Chinese shops in your name, "
            "stores the goods, then books an international line after you confirm warehouse photos."
        ),
        _h3("Language of the official site"),
        _p(
            f"The official language selector includes several European languages plus English and Chinese. "
            f"Our {DATE} lab used the public estimator API. Address format still has to match the destination country."
        ),
        _h3("Why is the on-site catalogue empty?"),
        _p(cat),
        _h2("What you pay"),
        _h3("How many payments?"),
        _p("Two: goods plus China domestic first, international freight after QC photos. You can consolidate in warehouse."),
        _h3("Why USD?"),
        _p(
            "USD is the platform default. Switching the selector to EUR/GBP has been observed to change the "
            f"symbol without converting the number. Treat figures as dollars. Open "
            f'<a href="{EST}">hipobuy.com/estimation</a> before you book.'
        ),
        _h3("Volumetric weight?"),
        _p(
            f"Usually L×W×H/8000. Billed = max(actual, volumetric). Lab carton {DATE}: 1000&nbsp;g, "
            f"35×25×10&nbsp;cm, clothes/common goods."
        ),
        _h2(tax_h),
        _p(tax_b),
        _h2("Warehouse"),
        _h3("Can I combine orders?"),
        _p("Yes. Storage limits are in official help and can change."),
        _h3("QC photos?"),
        _p("Yes, plus optional extra photos. Disputes are easier while goods remain in the warehouse."),
        _h3("What cannot ship?"),
        _p("Tobacco, alcohol, medicines, banned goods. Liquids/powders/pastes may need extra paperwork."),
        _h2("If something is wrong"),
        _h3("Lighter than estimated?"),
        _p("Official FAQ covers estimated vs actual billed weight and excess postage refunds."),
        _h3("Where do I claim?"),
        _p(
            f'Only on hipobuy.com. <a href="{HELP_OFF}">Official help</a> · '
            f'<a href="{DISCORD}">Discord</a> · <a href="{REDDIT}">Reddit</a>.'
        ),
        _h3("Invite in the title?"),
        _p(f"No. {INVITE} lives on the coupon URL and is re-typed in-app."),
        _h2("Estimator and tickets"),
        _p(_estimator_ticket(flavour, d)),
        _p(
            f'<a href="/{s["news"]}/">Dated news</a> · <a href="/{s["about"]}/">Who we are</a> · '
            f'<a href="/hipobuy-shipping-guide/">Shipping</a>'
        ),
        _links(d),
    ]
    return title, desc, _art(title, blocks)


def _estimator_ticket(flavour: str, d: dict) -> str:
    if flavour == "us":
        dest = "United States"
        extra = (
            "Write United States in tickets, not EU. FedEx-tax-prepaid SKUs billed volumetric 2000&nbsp;g "
            "on the same 1000&nbsp;g lab carton — read last-mile, not only the dollar."
        )
    elif flavour == "eu":
        dest = "the member-state country (ES, IE, IT…), never “EU”"
        extra = (
            "Spain-only freight copy stays on hipobuy.es. This TLD is a coupon desk. "
            "IOSS is a SKU you read the morning you book."
        )
    elif flavour == "haul":
        dest = "United Kingdom"
        extra = (
            "Northern Ireland is often another product. This Nominet host is not a 301 onto "
            "hipobuyspreadsheet.co.uk. Coupons stay on the .co.uk desk."
        )
    else:
        dest = "United Kingdom"
        extra = (
            "This .co.uk host ranks coupons and UK 8 sizing. Haul-log dollars live on "
            "hipobuyspreadsheets.uk. Re-type the invite in-app; the coupon article expires."
        )
    return (
        f'Open <a href="{EST}">hipobuy.com/estimation</a> with destination {dest} after QC photos. '
        f"{extra} Two cartons after a QC split are two estimates. "
        f"The 700&nbsp;g USA widget leftover on some templates is not this lab. "
        f"Insurance is chosen per line in HipoBuy. Finds stay on "
        f'<a href="{NET}">hipobuyspreadsheet.net</a>.'
    )


def news_at(d: dict) -> tuple[str, str, str]:
    title = "Neuigkeiten: was wir an HipoBuy für Österreich geprüft haben"
    desc = f"Datierte Checks {DATE} und 30 Sep 2026: AT-Linien, USD-Zahlen, Katalog-API. Kein Firmenblog."
    blocks = [
        _p(
            "Das ist kein Newsletter der Plattform. Es sind <strong>unsere</strong> Checks mit Datum, "
            "damit du siehst, welche Zahl frisch ist. Nächste Runde kommt oben dran; wir überschreiben "
            "alte Sätze nicht still."
        ),
        _h2(f"Check 1 · {DATE} · AT-Linien im öffentlichen Schätzer"),
        _p(
            f"Paket 1000&nbsp;g, 35×25×10&nbsp;cm, Kategorie Kleidung/gewöhnliche Ware, Ziel AT. "
            f"Die API lieferte <strong>{d['lines']} Linien</strong>. Günstigste carriable Zeile: "
            f"<code>{d['cheap']}</code> etwa ${d['usd']:.2f} ({d['days']} Tage, oft 1100&nbsp;g Volumen). "
            f"Express-EUCR lag wenige Dollar höher bei kürzerem Fenster. Das ist ein Snapshot, kein Checkout."
        ),
        _p(
            f"Für dich: filtere auf verfügbare Linien, bevor du Tage vergleichst. "
            f'<a href="{EST}">Schätzer mit Ziel Austria öffnen</a> — nicht die USA-700-g-Hülle weiter unten auf der Versandseite.'
        ),
        _h2("Check 2 · Währungsschalter wandelt nicht um"),
        _p(
            "Wie auf der spanischen Schwesterdesk dokumentiert (29 Aug 2026): Euro-Symbol, gleiche Ziffer. "
            "Wir drucken Laborsätze in USD. Deine Bank rechnet."
        ),
        _h2("Check 3 · 30 Sep 2026 · Katalog-API auf diesem Host"),
        _p(
            "Die Spreadsheet-Seite rief /api/products/ auf hipobuy.at auf. nginx lieferte 404 "
            "(try_files nur Datei, nicht index.php). Dieselbe PHP-Datei antwortete unter "
            "/api/products/index.php. Nach dem Rewrite kamen Treffer mit englischen Titeln und "
            "Bildern von w2clinks. Deutsche Suchwörter bleiben schlecht; englische Keywords funktionieren."
        ),
        _h2("Check 4 · Offizieller Schätzer vor dem Buchen"),
        _p(
            f"Zahlen auf dieser Site altern. Der öffentliche Schätzer "
            f'<a href="{EST}">{EST}</a> ist die Quelle für den Betrag am Büchertag. '
            "Wir speichern keine Unterdeklarations-Tipps."
        ),
        _h2("Check 5 · Deutsch in der App, Englisch im Katalog"),
        _p(
            "Der Sprachwähler der Plattform enthält Deutsch. Der Finds-Index bleibt englisch. "
            "Turnschuhe, Kapuzenpullover, Jacke liefern oft 0 Karten; sneakers, hoodie, jacket nicht. "
            "Das ist kein leerer Shop — das ist ein englischer Index. Am 30.&nbsp;Sep.&nbsp;2026 war zusätzlich "
            "nginx schuld, bis /api/products/ die PHP-Datei erreichte."
        ),
        _h2("Wie wir messen"),
        _p(
            "Versand: HipoBuy clientapi international2, Parameter notiert. Katalog: GET /api/products/ "
            "auf diesem Host. Zollrecht: BMF und Kommission, verlinkt, nicht selbst erfunden. "
            "Wir zählen keine 58 Spanien-Linien auf diesen Desk — das ist hipobuy.es. Hier sind es "
            f"{d['lines']} AT-Zeilen vom {DATE}. Wenn HipoBuy eine Linie vom Markt nimmt, gilt die App, "
            "nicht dieser HTML-Absatz."
        ),
        _p(
            "Was das für dich heißt: filtere auf verfügbare AT-Linien, lies USD als Dollar, öffne den "
            f"Schätzer am Büchertag. Zollrecht steht bei <a href=\"{d['customs']}\">BMF</a>, nicht in dieser HTML. "
            "LitBuy.at ist ein anderer Agent — wir 301en nicht dorthin. "
            "hipobuyspreadsheet.nl, .eu und .net bleiben eigene Hosts."
        ),
        _p(
            "Nächste Runde: wenn sich die günstigste AT-Linie oder der Katalog-Proxy ändert, kommt ein "
            "neuer Check mit Datum oben. Alte Sätze bleiben stehen, damit du die Drift siehst. "
            "Invite-Strings gehören in die Coupon-URL, nicht in Title-Tags."
        ),
        _links(d),
    ]
    return title, desc, _art(title, blocks)


def news_nl(d: dict) -> tuple[str, str, str]:
    title = "Nieuws: wat we voor Nederland op HipoBuy hebben nagemeten"
    desc = f"Gedateerde checks {DATE} en 30 sep 2026: NL-lijnen, USD, catalogus-API. Geen bedrijfsblog."
    blocks = [
        _p(
            "Dit is geen persbericht van HipoBuy. Het zijn gedateerde controles. Nieuwe rondes komen "
            "bovenaan; oude zinnen worden niet stiekem herschreven."
        ),
        _h2(f"Check 1 · {DATE} · NL-lijnen"),
        _p(
            f"1000&nbsp;g / 35×25×10&nbsp;cm, kleding/gewone goederen, bestemming NL. "
            f"<strong>{d['lines']} lijnen</strong> in de API. Goedkoopste carriable: "
            f"<code>{d['cheap']}</code> ± ${d['usd']:.2f} ({d['days']} dagen, vaak 1100&nbsp;g volume). "
            f"China Post SURFACE was goedkoper in USD en 60–90 werkdagen — lees last-mile, niet alleen de prijs."
        ),
        _p(f'<a href="{EST}">Estimator met bestemming Netherlands</a> vóór je boekt.'),
        _h2("Check 2 · Valutakiezer rekent niet om"),
        _p("Euro-symbool, hetzelfde getal (check 29 aug 2026 op het officiële site). Labtabel in USD."),
        _h2("Check 3 · 30 sep 2026 · /api/products/ was 404"),
        _p(
            "De spreadsheet-grid op dit host bleef leeg omdat nginx /api/products/ niet naar index.php "
            "stuurde. Na de rewrite: Engelse hits van w2clinks. Nederlandse zoektermen blijven zwak."
        ),
        _h2("Check 4 · Officiële tool wint van HTML"),
        _p(
            f'Tarieven wijzigen. <a href="{EST}">{EST}</a> is de live bron. Geen onderwaarderingstips.'
        ),
        _h2("Check 5 · Nederlands in de app, Engels in de catalogus"),
        _p(
            "De taalkiezer van HipoBuy bevat Nederlands. De finds-index blijft Engels. "
            "sneakers, hoodie, jacket vullen de grid; Nederlandse woorden geven vaak 0 hits. "
            "Op 30&nbsp;sep&nbsp;2026 kwam daar een nginx-404 bij tot /api/products/ naar index.php wees."
        ),
        _h2("Check 6 · Invite hoort niet in de title"),
        _p(
            f"Code {INVITE} stond op 29&nbsp;sep&nbsp;2026 op de couponkaart. Hij wordt in de app opnieuw "
            "getypt. We zetten hem niet in <code>&lt;title&gt;</code> of in de homepage-H1. "
            "Dat is dezelfde regel als op hipobuy.es, alleen in het Nederlands."
        ),
        _h2("Methode"),
        _p(
            "Estimator-API met vaste parameters (1000&nbsp;g, 35×25×10&nbsp;cm, kleding/gewone goederen). "
            "Catalogus via GET op dit host. Douane: Belastingdienst + Commissie, verlinkt, niet verzonnen. "
            f"Dat zijn {d['lines']} NL-lijnen, geen kopie van de Spaanse 58-lijnen-pagina. "
            "Als HipoBuy een SKU schrapt, wint de app van deze HTML."
        ),
        _p(
            "Wat dit voor jou betekent: filter op beschikbare NL-lijnen, lees USD als dollars, open de "
            f"estimator op de boekingsdag. Douanerecht staat bij <a href=\"{d['customs']}\">Belastingdienst Douane</a>, "
            "niet in deze HTML. ootdbuy.nl is een andere agent. hipobuy.at, .eu en .net blijven eigen hosts. "
            "Op de live-SKU moet PostNL of DHL staan, niet alleen „goedkope lijn“. SURFACE (60–90 werkdagen) "
            "is alleen een optie als je die wachttijd accepteert — de luchtankerprijs op de meetdag was DHL-EUCR."
        ),
        _p(
            "Volgende ronde komt bovenaan met een nieuwe datum. SURFACE blijft alleen relevant als je "
            "60–90 werkdagen accepteert; DHL-EUCR was de luchtankerprijs op de meetdag. "
            "Invite-strings horen op de coupon-URL, niet in title-tags. "
            "Wij publiceren geen eurobedragen in lopende tekst: de cijfers zijn dollars."
        ),
        _links(d),
    ]
    return title, desc, _art(title, blocks)


def news_en(d: dict, flavour: str) -> tuple[str, str, str]:
    host = d["host"]
    if flavour == "eu":
        title = "News: what we checked on the HipoBuy EU coupon desk"
        c1 = (
            f"We did not invent a Spain line table on this host — hipobuy.es already covers ES. "
            f"On {DATE} we measured AT/NL/GB/US via the public estimator API (destination must be a "
            f"country code, never “EU”). This desk’s ranked job remains coupons; IOSS is a SKU you read "
            f"in-app the morning you book."
        )
    elif flavour == "us":
        title = "News: what we checked for HipoBuy to the United States"
        c1 = (
            f"Lab carton {DATE}: 1000&nbsp;g / 35×25×10&nbsp;cm, clothes/common goods, destination US. "
            f"<strong>{d['lines']} lines</strong>. Cheapest carriable: <code>{d['cheap']}</code> about "
            f"${d['usd']:.2f} ({d['days']} workdays, billed actual 1000&nbsp;g). Integrator SKUs billed "
            f"volumetric 1100–2000&nbsp;g on the same carton."
        )
    elif flavour == "haul":
        title = "News: what we checked on the UK haul log"
        c1 = (
            f"Lab carton {DATE}, destination GB: <strong>{d['lines']} lines</strong>. Cheapest carriable "
            f"<code>{d['cheap']}</code> about ${d['usd']:.2f} ({d['days']} workdays, billed 1100&nbsp;g). "
            f"Evri-AF1 about $33.88 / 7–10 workdays. Northern Ireland is often another product. "
            f"This host is not a 301 onto hipobuyspreadsheet.co.uk."
        )
    else:
        title = "News: what we checked on the UK spreadsheet desk"
        c1 = (
            f"On {DATE} the exclusive invite card on /hipobuy-coupons/ still showed {INVITE}. "
            f"GB estimator snapshot (same carton) lives on the haul-log shipping lab: "
            f"<code>{d['cheap']}</code> about ${d['usd']:.2f}. This .co.uk host keeps coupons and UK 8 sizing."
        )
    desc = title + f" {DATE} / 30 Sep 2026. {host}."
    blocks = [
        _p(
            "Not a company blog. Dated checks. New rounds go on top; we do not silently rewrite old sentences."
        ),
        _h2(f"Check 1 · {DATE}"),
        _p(c1),
        _p(f'Open <a href="{EST}">{EST}</a> before you pay international freight.'),
        _h2("Check 2 · Currency selector"),
        _p(
            "USD figures kept their digits when the official UI was switched toward euro (documented 29 Aug 2026). "
            "Lab amounts on this desk are USD."
        ),
        _h2("Check 3 · 30 Sep 2026 · catalogue API"),
        _p(
            f"/{host} spreadsheet called /api/products/ and got 404 until nginx rewrote the directory to "
            "index.php. After the fix, English w2clinks hits and absolute image URLs on w2clinks.com."
        ),
        _h2("Check 4 · Official estimator beats HTML"),
        _p(
            "Rates move. We do not coach declared value. Re-run in-app after QC photos. "
            f"The public tool is <a href=\"{EST}\">{EST}</a> — this HTML is a snapshot, not checkout."
        ),
        _h2("Check 5 · language of the app vs the catalogue"),
        _p(_news_lang_check(flavour)),
        _h2("Check 6 · invite stays off the title"),
        _p(
            f"On {DATE} the exclusive coupon card still listed {INVITE}. Re-type it in-app. "
            "It does not belong in <code>&lt;title&gt;</code> or the homepage H1 — same rule as hipobuy.es, "
            "localised for this desk’s job."
        ),
        _h2("Method"),
        _p(
            "Estimator API with a recorded parcel (1000&nbsp;g, 35×25×10&nbsp;cm, clothes/common goods). "
            "Catalogue GET on this host. Tax: linked official pages, not invented rates. "
            "We do not paste hipobuy.es Spain counts onto this TLD. Re-run after every QC return. "
            "If HipoBuy withdraws a SKU, the app wins over this HTML."
        ),
        _p(_news_means(flavour, d)),
        _p(
            "The next round will be dated and stacked above this one. Old checks stay so you can see drift. "
            "Invite strings belong on the coupon URL, not in titles. "
            "We do not publish euro or sterling amounts in running prose: the lab digits are dollars."
        ),
        _links(d),
    ]
    return title, desc, _art(title, blocks)


def _news_lang_check(flavour: str) -> str:
    if flavour == "eu":
        return (
            "The official language selector includes several European languages. The finds index stays English. "
            "Spanish, French or German queries often return zero cards; sneakers/hoodie fill the grid. "
            "This coupon desk does not clone hipobuy.es Spanish search. On 30 Sep 2026 /api/products/ 404ed "
            "until nginx reached index.php."
        )
    if flavour == "us":
        return (
            "English queries match the index. This US desk does not need a Spanish translator. "
            "The empty grid on 30 Sep 2026 was nginx: /api/products/ did not rewrite to index.php. "
            "After the fix, English w2clinks titles and absolute image URLs came back."
        )
    if flavour == "haul":
        return (
            "English catalogue index. This haul-log host is not a Spanish clone and not the .co.uk coupon desk. "
            "On 30 Sep 2026 the spreadsheet grid 404ed until nginx rewrote /api/products/ to index.php."
        )
    return (
        "English catalogue. Coupons and UK 8 sizing are this host’s ranked jobs — not a Spanish search UI. "
        "On 30 Sep 2026 /api/products/ 404ed until nginx reached index.php. After the fix, English hits returned."
    )


def _news_means(flavour: str, d: dict) -> str:
    tax = d.get("customs") or d.get("ioss") or EST
    if flavour == "eu":
        return (
            f"What this means: pick a member-state country in <a href=\"{EST}\">the estimator</a>, "
            f"read USD digits as dollars, open the coupon article for {INVITE}. "
            f'IOSS notes: <a href="{d["ioss"]}">{d["ioss"]}</a>. Spain freight stays on hipobuy.es.'
        )
    if flavour == "us":
        return (
            f"What this means: filter available US lines, treat figures as USD, re-run "
            f'<a href="{EST}">the estimator</a> after photos. Duty basics: '
            f'<a href="{tax}">CBP</a>. hipobuy.at is another desk.'
        )
    if flavour == "haul":
        return (
            f"What this means: read Royal Mail vs Evri last-mile on the live SKU, treat lab dollars as USD, "
            f'open <a href="{EST}">the estimator</a> with destination United Kingdom. '
            f'<a href="{tax}">GOV.UK goods sent from abroad</a>. Coupons stay on .co.uk.'
        )
    return (
        f"What this means: copy {INVITE} from /hipobuy-coupons/, check UK 8 sizing, treat lab dollars as USD. "
        f'Haul-log freight lives on hipobuyspreadsheets.uk. Tax: <a href="{tax}">GOV.UK</a>.'
    )


def about_at(d: dict) -> tuple[str, str, str]:
    title = "Über uns: unabhängiger HipoBuy-Desk für Österreich"
    desc = "hipobuy.at ist redaktionell unabhängig. Keine Bestellungen, kein Kontozugriff. Messung 29 Sep 2026."
    blocks = [
        _p(
            "<strong>hipobuy.at ist nicht HipoBuy.</strong> Es ist ein redaktioneller AT-Desk: Versandlabor, "
            "Ablauf, Hilfe, Neuigkeiten. Wir lagern nichts, kassieren kein Porto, sehen keine Accounts."
        ),
        _h2("Wie wir arbeiten"),
        _h3("Quellen"),
        _p(
            f"Versandzahlen: öffentlicher HipoBuy-Schätzer, Parameter und Datum notiert. Zoll: "
            f'<a href="{d["customs"]}">BMF</a>, <a href="{d["ioss"]}">EU-Kommission</a>. '
            "Was wir nicht geprüft haben, bleibt weg."
        ),
        _h3("Warum wenige Euro-Beträge"),
        _p(
            "Tarife ändern sich wöchentlich. Eine hier kopierte Zahl wäre morgen falsch. Deshalb "
            f'<a href="{EST}">Schätzer</a> plus Snapshot vom {DATE} in USD.'
        ),
        _h3("Invite"),
        _p(
            f"Registrierungslink kann {INVITE} enthalten. Provision möglich, ohne Aufpreis für dich. "
            "Du kannst ohne Code auf hipobuy.com starten. Unbequeme Facts (leere deutsche Katalogsuche, "
            "USD-Zahlen) bleiben trotzdem stehen."
        ),
        _h2("Was wir nicht sind"),
        _p(
            "Kein Shop, kein Lager, kein Ticket-System. Reklamationen nur auf hipobuy.com. "
            f'Discord <a href="{DISCORD}">HipoBuy</a> und Reddit <a href="{REDDIT}">r/Hipobuy_</a> '
            "sind Kanäle der Plattform, nicht unseres Desks. "
            "Wir 301en nicht auf hipobuyspreadsheet.net und nicht auf LitBuy.at."
        ),
        _h2("Kontakt"),
        _p(
            "Wenn eine Laborspalte oder ein Link bricht, schreiben wir das mit Datum in Neuigkeiten. "
            "Wir korrigieren nicht still. Dieser AT-Desk beantwortet keine Bestelltickets."
        ),
        _p(
            "HipoBuy nennt in der Hilfe u. a. Hong Kong Jointown Trading Co., Limited (72090932), "
            "EVERLINE TRADING CO., LIMITED (Kington, UK) und weitere Gesellschaften. Das ist Plattformtext, "
            "prüfbar im Footer ihrer Hilfe — Stand 29 Aug 2026 auf der spanischen Schwesterdesk dokumentiert. "
            "Wir erfinden keine Firmennamen und keine Zoll-Sätze."
        ),
        _p(
            "Deutsch auf diesem Desk, Englisch im Katalogindex. Österreichische Straße in der App, "
            "nicht Germany. Der Finds-Hub mit Tausenden Zeilen bleibt auf hipobuyspreadsheet.net."
        ),
        _links(d, extra="LitBuy.at ist ein anderer Agent. Finds-Hub: "),
    ]
    return title, desc, _art(title, blocks)


def about_nl(d: dict) -> tuple[str, str, str]:
    title = "Over ons: onafhankelijke HipoBuy-desk voor Nederland"
    desc = "hipobuyspreadsheet.nl is redactioneel onafhankelijk. Geen bestellingen, geen accounttoegang."
    blocks = [
        _p(
            "<strong>Dit host is niet HipoBuy.</strong> Het is een NL-desk: labtabel, stappenplan, hulp, nieuws. "
            "Wij zien je account niet. ootdbuy.nl is een andere agent."
        ),
        _h2("Bronnen"),
        _p(
            f"Estimator-API met datum. Douane: <a href=\"{d['customs']}\">Belastingdienst</a>, "
            f'<a href="{d["ioss"]}">Commissie</a>. Geen verzonnen tarieven.'
        ),
        _h2("Waarom USD in de labtabel"),
        _p(f"Tarieven wijzigen. Live bedrag: <a href=\"{EST}\">estimator</a>. Snapshot {DATE}."),
        _h2("Invite"),
        _p(
            f"{INVITE} kan commissie opleveren als je via de coupon-URL registreert. Zonder code kan ook. "
            "Onhandige feiten (lege Nederlandse cataloguszoek, 404 op /api/products/ tot 30 sep) blijven staan."
        ),
        _h2("Wat we niet zijn"),
        _p(
            "Geen shop, geen magazijn, geen ticketsysteem. Claims alleen op hipobuy.com. "
            f'<a href="{DISCORD}">Discord</a> en <a href="{REDDIT}">Reddit</a> zijn kanalen van het '
            "platform, niet van deze desk. We 301’en niet naar hipobuyspreadsheet.net en niet naar ootdbuy.nl."
        ),
        _h2("Contact"),
        _p(
            "Als een labkolom of een link stukgaat, zetten we dat met datum in Nieuws. "
            "We herschrijven niet stiekem. Deze NL-desk beantwoordt geen besteltickets."
        ),
        _p(
            "HipoBuy noemt in de help o.a. Hong Kong Jointown Trading Co., Limited (72090932) en "
            "EVERLINE TRADING CO., LIMITED. Dat is platformtekst, te checken in de footer van hun help — "
            "niet onze claim."
        ),
        _p(
            "Nederlands op deze desk, Engels in de catalogusindex. Nederlands huisadres in de app, "
            "niet Belgium en niet EU als landcode. De finds-hub met duizenden rijen blijft op "
            "hipobuyspreadsheet.net. hipobuy.at is een Duitstalig AT-desk, geen 301 naar hier. "
            "Wij publiceren geen eurobedragen in lopende tekst: de labcijfers zijn dollars. "
            "Geen onderwaarderingstips. Onafhankelijke NL-desk, geen HipoBuy-accountbeheer."
        ),
        _links(d),
    ]
    return title, desc, _art(title, blocks)


def about_en(d: dict, flavour: str) -> tuple[str, str, str]:
    host = d["host"]
    if flavour == "eu":
        title = "Who we are: independent HipoBuy EU coupon desk"
        job = (
            "Coupon desk for a real member-state address. Not hipobuy.es, not the AT/NL freight labs, "
            "not the .net finds hub."
        )
    elif flavour == "us":
        title = "Who we are: independent HipoBuy US desk"
        job = "US freight lab and FAQ. Not a clone of the EU coupon desk or hipobuy.at."
    elif flavour == "haul":
        title = "Who we are: independent HipoBuy UK haul log"
        job = (
            "Nominet haul log (line codes + spreadsheet). Not a 301 onto hipobuyspreadsheet.co.uk. "
            "/about/ on this host already redirects home, so this page lives at /who-we-are/."
        )
    else:
        title = "Who we are: independent HipoBuy UK spreadsheet desk"
        job = "Coupons and UK sizing. Haul-log freight dollars stay on hipobuyspreadsheets.uk."
    desc = f"{host} is editorial. We do not run HipoBuy accounts. Dated {DATE}."
    blocks = [
        _p(f"<strong>{host} is not HipoBuy.</strong> {job} We do not store goods or see your account."),
        _h2("Sources"),
        _p(
            f"Freight: public estimator API with recorded parcel and date. Tax pages we did not measure "
            f"are linked ("
            + (f'<a href="{d["customs"]}">{d["customs"]}</a>' if d.get("customs") else "official sites")
            + "). No invented duty rates."
        ),
        _h2("Why few live prices in prose"),
        _p(f"Lines move. Use <a href=\"{EST}\">{EST}</a> plus the dated snapshot where we have one."),
        _h2("Invite"),
        _p(
            f"{INVITE} on the coupon URL may pay this desk a commission. You can register without it. "
            "Uncomfortable facts stay published (USD digits, empty non-English catalogue search, API 404 until 30 Sep 2026)."
        ),
        _h2("What we are not"),
        _p(
            "Not a shop, warehouse, or ticket queue. Claims only on hipobuy.com. "
            f'<a href="{DISCORD}">Discord</a> and <a href="{REDDIT}">Reddit</a> belong to the platform. '
            "We do not 301 this TLD onto hipobuyspreadsheet.net or onto a sister desk."
        ),
        _h2("Contact"),
        _p(
            "If a lab column or a link breaks, we date it on News. We do not silently rewrite old checks. "
            "This desk does not answer order tickets."
        ),
        _p(
            "HipoBuy’s own help names Hong Kong Jointown Trading Co., Limited (72090932), "
            "EVERLINE TRADING CO., LIMITED (Kington, UK) and others. That is platform text, "
            "checkable in their help footer — recorded 29 Aug 2026 on hipobuy.es, not a claim we invented. "
            "We do not invent company names or duty rates."
        ),
        _links(d),
    ]
    return title, desc, _art(title, blocks)


def shipping_trust(d: dict, key: str) -> str:
    est_p = (
        f'<p class="pp"><a href="{EST}">Open the official HipoBuy estimator</a> with this country selected '
        f"before you pay international freight. The table above is a snapshot from {DATE}, not checkout. "
        "USD digits: switching the official currency selector has been observed to change the symbol without converting the number.</p>"
        if d.get("dest")
        else (
            f'<p class="pp">The estimator needs a <strong>member-state country code</strong> (ES, IE, IT…), '
            f'not “EU”. Open <a href="{EST}">{EST}</a>. Spain-only line copy belongs on hipobuy.es. '
            "USD digits stay dollars even when the UI shows a euro sign.</p>"
        )
    )
    if key == "at":
        customs = (
            f'<h2 class="ph" id="zoll">Zoll und MwSt — nur Erklärung</h2>'
            f'<p class="pp">Wer Abgaben zahlt, steht auf der Live-SKU in drei englischen Labels: '
            f"Tax free, Prepaid Duty, Duties Payable by Recipient. Im letzten Fall kann der Zusteller "
            f"vor der Übergabe kassieren — inkl. einer Bearbeitungsgebühr, die der Schätzer oft nicht zeigt. "
            f"„Tax free“ löscht nicht die Befugnis der Zollstelle zur Prüfung, nur wer den Vorgang trägt.</p>"
            f'<p class="pp">EU-Orientierung oft 150&nbsp;€ für bestimmte Fernverkäufe (IOSS). Darüber können '
            f"Zölle greifen. Konkrete Sätze stehen nicht in dieser HTML. "
            f'<a href="{d["customs"]}">BMF Zoll</a> · '
            f'<a href="{d["ioss"]}">IOSS / Kommission</a>. '
            f"<strong>Keine Unterdeklaration.</strong></p>"
            f'<p class="pp">USD-Ziffern: der Währungsschalter ändert oft nur das Symbol. Laborsätze hier in Dollar. '
            f'<a href="/hilfe/">Hilfe</a> · <a href="/neuigkeiten/">Neuigkeiten</a> · '
            f'<a href="/ueber-uns/">Über uns</a>.</p>'
        )
    elif key == "nl":
        customs = (
            f'<h2 class="ph" id="douane">Btw en douane — alleen uitleg</h2>'
            f'<p class="pp">Invoer volgt de geboekte lijn. Drie labels in de estimator: Tax free, Prepaid Duty, '
            f"Duties Payable by Recipient. Bij de laatste kan last-mile innen vóór bezorging, plus een "
            f"mogelijke behandelingsfee die de estimator niet toont. Tax free schrapt niet de bevoegdheid "
            f"van de douane om te controleren.</p>"
            f'<p class="pp">EU-oriëntatie vaak 150&nbsp;€ (IOSS) voor bepaalde zendingen. Daarboven kunnen '
            f"invoerrechten spelen. Geen verzonnen tarieven hier. "
            f'<a href="{d["customs"]}">Belastingdienst Douane</a> · '
            f'<a href="{d["ioss"]}">IOSS</a>. <strong>Geen onderwaardering.</strong></p>'
            f'<p class="pp">USD-cijfers, euro-symbool. '
            f'<a href="/hulp/">Hulp</a> · <a href="/nieuws/">Nieuws</a> · '
            f'<a href="/over-ons/">Over ons</a>.</p>'
        )
    elif key == "us":
        customs = (
            f'<h2 class="ph" id="cbp">CBP — educational</h2>'
            f'<p class="pp">US treatment follows the booked product. This desk does not invent a de-minimis '
            f"dollar figure for your carton — HipoBuy’s own help table is labelled indicative and gathered "
            f"from the internet. Read the SKU label (tax free / prepaid / payable by recipient) the morning you book.</p>"
            f'<p class="pp"><a href="{d["customs"]}">CBP duty overview</a>. '
            f"<strong>No under-declaration tips.</strong></p>"
            f'<p class="pp">USD is native here. Still re-run <a href="{EST}">the estimator</a> after photos. '
            f'<a href="/help/">Help</a> · <a href="/news/">News</a> · <a href="/who-we-are/">Who we are</a>.</p>'
        )
    elif key == "eu":
        customs = (
            f'<h2 class="ph" id="ioss">VAT / IOSS — educational</h2>'
            f'<p class="pp">Pick a country in the estimator. IOSS is a SKU, not a TLD. The Commission explains '
            f"the import one-stop shop for certain low-value distance sales (often discussed around €150). "
            f"Above that, customs duty can apply. Spain-only line copy belongs on hipobuy.es.</p>"
            f'<p class="pp"><a href="{d["ioss"]}">European Commission VAT e-commerce</a>. '
            f"<strong>No declared-value coaching.</strong></p>"
            f'<p class="pp"><a href="/help/">Help</a> · <a href="/news/">News</a> · '
            f'<a href="/who-we-are/">Who we are</a>.</p>'
        )
    else:
        ni = " Northern Ireland is often another carrier product." if key == "ukhaul" else " This .co.uk host still ranks coupons; haul-log dollars live on hipobuyspreadsheets.uk." if key == "uk" else ""
        customs = (
            f'<h2 class="ph" id="hmrc">HMRC — educational</h2>'
            f'<p class="pp">UK import VAT/duty follow the carrier SKU.{ni} '
            f"Read Tax free / Prepaid Duty / Duties Payable by Recipient on the live line. "
            f"A cheaper list price on a recipient-pays SKU is not a cheaper landed cost.</p>"
            f'<p class="pp"><a href="{d["customs"]}">GOV.UK goods sent from abroad</a>. '
            f"<strong>No declared-value coaching.</strong></p>"
            f'<p class="pp">USD lab digits. <a href="{EST}">Official estimator</a>. '
            f'<a href="/help/">Help</a> · <a href="/news/">News</a> · '
            f'<a href="/who-we-are/">Who we are</a>.</p>'
        )
    extra_lab = ""
    if key == "uk" and d.get("dest") == "GB":
        extra_lab = lab_block(
            "GB",
            "United Kingdom",
            "Cheapest carriable on the lab day: HIPO-RoyalMail-GB-1 about $23.83. This .co.uk host still ranks coupons; the table is here so GBP landed cost is not a surprise.",
        )
    return extra_lab + est_p + customs


def wrap(base: str, *, canonical: str, title: str, desc: str, lang: str, article: str, crumb: str) -> str:
    html = base
    html = re.sub(r'<html lang="[^"]*"', f'<html lang="{lang}"', html, count=1)
    html = re.sub(r"<title>.*?</title>", f"<title>{title}</title>", html, count=1, flags=re.S)
    html = re.sub(
        r'<meta name="description" content="[^"]*"',
        f'<meta name="description" content="{desc}"',
        html,
        count=1,
    )
    html = re.sub(
        r'<meta property="og:title" content="[^"]*"',
        f'<meta property="og:title" content="{title}"',
        html,
        count=1,
    )
    html = re.sub(
        r'<meta property="og:description" content="[^"]*"',
        f'<meta property="og:description" content="{desc}"',
        html,
        count=1,
    )
    html = re.sub(
        r'<meta property="og:url" content="[^"]*"',
        f'<meta property="og:url" content="{canonical}"',
        html,
        count=1,
    )
    html = re.sub(
        r'<link rel="canonical" href="[^"]*"',
        f'<link rel="canonical" href="{canonical}"',
        html,
        count=1,
    )
    html = re.sub(
        r'<article class="hipo-howto".*?</article>',
        article.strip(),
        html,
        count=1,
        flags=re.S,
    )
    html = re.sub(
        r"(<div class=\"bc\"[^>]*>.*?<span>)([^<]+)(</span></div>)",
        rf"\1{crumb}\3",
        html,
        count=1,
        flags=re.S,
    )
    # fallback breadcrumb used on these templates
    html = re.sub(
        r"(<span>)How to Use Hipobuy(</span>)",
        rf"<span>{crumb}</span>",
        html,
        count=1,
    )
    return html


def patch_shipping(html: str, key: str, d: dict) -> str:
    block = shipping_trust(d, key)
    needle = '  <h2 class="ph" id="calculator">'
    if needle not in html:
        raise ValueError(f"{key}: calculator heading missing")
    if "id=\"zoll\"" in html or "id=\"douane\"" in html or "id=\"cbp\"" in html or "id=\"hmrc\"" in html or "id=\"ioss\"" in html:
        return html
    return html.replace(needle, block + "\n" + needle, 1)


def pages_for(key: str, d: dict) -> dict[str, tuple[str, str, str, str]]:
    """slug -> (title, desc, article, crumb)"""
    if key == "at":
        h, n, a = help_at(d), news_at(d), about_at(d)
    elif key == "nl":
        h, n, a = help_nl(d), news_nl(d), about_nl(d)
    else:
        fl = {"uk": "uk", "eu": "eu", "us": "us", "ukhaul": "haul"}[key]
        h, n, a = help_en(d, fl), news_en(d, fl), about_en(d, fl)
    crumbs = {
        "at": ("Hilfe", "Neuigkeiten", "Über uns"),
        "nl": ("Hulp", "Nieuws", "Over ons"),
    }.get(key, ("Help", "News", "Who we are"))
    return {
        d["slugs"]["help"]: (*h, crumbs[0]),
        d["slugs"]["news"]: (*n, crumbs[1]),
        d["slugs"]["about"]: (*a, crumbs[2]),
    }


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
    client.connect("31.97.41.31", username="root", password=password, timeout=30)
    return client


def _run(client, cmd: str, timeout: int = 60) -> str:
    _, stdout, stderr = client.exec_command(cmd, timeout=timeout)
    return (stdout.read() + stderr.read()).decode(errors="replace").strip()


def _validate() -> None:
    for key, d in HOSTS.items():
        if d["host"].endswith(".net"):
            raise SystemExit("refusing .net")
        built = pages_for(key, d)
        for slug, (title, desc, article, crumb) in built.items():
            n = _wc(article)
            min_w = 280 if slug == d["slugs"]["about"] else 450
            flag = "OK" if n >= min_w else "SHORT"
            print(f"{flag:5} {key}/{slug} words={n} {title[:56]}")
            if n < min_w:
                raise SystemExit(f"{key}/{slug} too short: {n}")


def main() -> None:
    _validate()
    if "--dry" in sys.argv:
        print("dry-run ok")
        return
    client = _connect()
    sftp = client.open_sftp()
    OUT.mkdir(parents=True, exist_ok=True)
    stamp = time.strftime("%Y%m%d-%H%M%S")
    bak = f"/www/backup/hipobuy-trust-{stamp}"
    print(_run(client, f"mkdir -p '{bak}'"))
    uploaded: list[str] = []

    for key, d in HOSTS.items():
        with sftp.open(d["howto"]) as fh:
            chrome = fh.read().decode("utf-8", "replace")
        built = pages_for(key, d)
        for slug, (title, desc, article, crumb) in built.items():
            n = _wc(article)
            canonical = f"https://{d['host']}/{slug}/"
            html = wrap(
                chrome,
                canonical=canonical,
                title=title,
                desc=desc.replace('"', "&quot;"),
                lang=d["lang"],
                article=article,
                crumb=crumb,
            )
            local_dir = OUT / d["host"] / slug
            local_dir.mkdir(parents=True, exist_ok=True)
            local = local_dir / "index.html"
            local.write_text(html, encoding="utf-8")
            remote_dir = f"/www/wwwroot/{d['host']}/{slug}"
            remote = f"{remote_dir}/index.html"
            _run(client, f"mkdir -p '{remote_dir}'")
            try:
                sftp.stat(remote)
                _run(client, f"mkdir -p '{bak}/{d['host']}/{slug}' && cp -a '{remote}' '{bak}/{d['host']}/{slug}/index.html'")
            except FileNotFoundError:
                pass
            sftp.put(str(local), remote)
            uploaded.append(remote)
            print(f"PUT {remote} words={n}")

        with sftp.open(d["ship"]) as fh:
            ship_html = fh.read().decode("utf-8", "replace")
        ship2 = patch_shipping(ship_html, key, d)
        ship_local = OUT / d["host"] / "hipobuy-shipping-guide.html"
        ship_local.write_text(ship2, encoding="utf-8")
        _run(client, f"cp -a '{d['ship']}' '{bak}/{d['host']}-shipping.html'")
        sftp.put(str(ship_local), d["ship"])
        uploaded.append(d["ship"])
        print("PUT", d["ship"], "trust-insert")

        overlay = d["overlay"]
        if overlay.is_file():
            remote_ov = f"/www/wwwroot/{d['host']}/index.html"
            _run(client, f"cp -a '{remote_ov}' '{bak}/{d['host']}-index.html'")
            sftp.put(str(overlay), remote_ov)
            uploaded.append(remote_ov)
            print("PUT overlay", d["host"])

        # sitemap
        sm = f"/www/wwwroot/{d['host']}/sitemap.xml"
        try:
            with sftp.open(sm) as fh:
                smx = fh.read().decode("utf-8", "replace")
            changed = False
            for slug in d["slugs"].values():
                loc = f"https://{d['host']}/{slug}/"
                if loc not in smx:
                    entry = (
                        "  <url>\n"
                        f"    <loc>{loc}</loc>\n"
                        "    <lastmod>2026-09-30</lastmod>\n"
                        "  </url>\n"
                    )
                    if "</urlset>" in smx:
                        smx = smx.replace("</urlset>", entry + "</urlset>")
                        changed = True
            if changed:
                _run(client, f"cp -a '{sm}' '{bak}/{d['host']}-sitemap.xml'")
                with sftp.open(sm, "w") as fh:
                    fh.write(smx)
                uploaded.append(sm)
                print("sitemap", d["host"])
        except FileNotFoundError:
            print("no sitemap", d["host"])

    # US optional alias
    us_ship = "/www/wwwroot/hipobuyspreadsheet.us/guides/shipping/index.html"
    us_src = str(OUT / "hipobuyspreadsheet.us" / "hipobuy-shipping-guide.html")
    try:
        sftp.stat(us_ship)
        sftp.put(us_src, us_ship)
        uploaded.append(us_ship)
        print("PUT", us_ship)
    except FileNotFoundError:
        pass

    _run(
        client,
        "chown www:www "
        + " ".join(f"'{p}'" for p in uploaded)
        + " && chmod 644 "
        + " ".join(f"'{p}'" for p in uploaded),
    )
    print("backup", bak)
    print("count", len(uploaded))
    sftp.close()
    client.close()


if __name__ == "__main__":
    main()
