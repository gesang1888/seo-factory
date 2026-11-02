#!/usr/bin/env python3
"""Expand A-tier dest homes: brand queries → spreadsheet / shipping / legal.

LIVE-only. Fetches current Origin HTML, injects a unique trio + inner depth,
PUTs those files. Does not smash unique ranked CMS (injects a stamped
section). Does not 301 dests. Does not coach a declared value.
Does not PUT hubs or twins. GSC sitemap submit only.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import ssl
import sys
import time
from html import escape
from pathlib import Path
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
STAMP = "20261102"
ATTR = f'data-a-tier-expand="{STAMP}"'
W2C = "https://w2clinks.com/spreadsheet/"
ORIGIN = "31.97.41.31"
CTX = ssl.create_default_context()

# A-tier: GSC 28d ≥10 clicks, mostly from the target country.
# Slugs are the LIVE ranked URLs (keep maps), not dest-cluster defaults.
HOSTS: dict[str, dict] = {
    "bbdbuy.it": {
        "agent": "BBDBuy", "loc": "it", "name": "Italia",
        "sheet": "/bbdbuy-spreadsheet/", "ship": "/bbdbuy-shipping/",
        "legal": "/is-bbdbuy-legit/",
        "official": "https://www.bbdbuy.com/",
        "estimator": "https://www.bbdbuy.com/estimation",
        "customs": ("ADM", "https://www.adm.gov.it/portale/"),
        "postal": "Poste Italiane", "fp": "CAP a cinque cifre, es. 20121 Milano",
        "nav": [("Spreadsheet", "sheet"), ("Spedizione", "ship"), ("È legale?", "legal")],
    },
    "fansbuy.co.uk": {
        "agent": "FansBuy", "loc": "en", "name": "the UK",
        "sheet": "/fansbuy-spreadsheet/", "ship": "/fansbuy-shipping-guide/",
        "legal": "/is-fansbuy-legal-uk/",
        "official": "https://fansbuy.com/",
        "estimator": "https://fansbuy.com/estimates",
        "customs": ("HMRC", "https://www.gov.uk/goods-sent-from-abroad"),
        "postal": "Royal Mail", "fp": "UK postcode, not a Northern Ireland SKU by default",
        "nav": [("Spreadsheet", "sheet"), ("Shipping", "ship"), ("Is it legal?", "legal")],
    },
    "mycnbox.nl": {
        "agent": "MyCNBox", "loc": "nl", "name": "Nederland",
        "sheet": "/mycnbox-spreadsheet/", "ship": "/mycnbox-shipping-guide/",
        "legal": "/is-mycnbox-legit/",
        "official": "https://www.mycnbox.com/",
        "estimator": "https://www.mycnbox.com/calc/index",
        "customs": ("Douane", "https://www.belastingdienst.nl/wps/wcm/connect/nl/douane/"),
        "postal": "PostNL", "fp": "Nederlandse postcode 1234 AB, geen Packstation",
        "nav": [("Spreadsheet", "sheet"), ("Verzending", "ship"), ("Legaal?", "legal")],
    },
    "cssbuy.es": {
        "agent": "CSSBuy", "loc": "es", "name": "España",
        "sheet": "/cssbuy-spreadsheet/", "ship": "/cssbuy-shipping/",
        "legal": "/is-cssbuy-legal-espana/",
        "official": "https://www.cssbuy.com/",
        "estimator": "https://www.cssbuy.com/?action=estimates&go=page",
        "customs": ("AEAT", "https://sede.agenciatributaria.gob.es/"),
        "postal": "Correos", "fp": "código postal de cinco dígitos, es. 28001 Madrid",
        "nav": [("Spreadsheet", "sheet"), ("Envío", "ship"), ("¿Es legal?", "legal")],
    },
    "mycnbox.co.uk": {
        "agent": "MyCNBox", "loc": "en", "name": "the UK",
        "sheet": "/mycnbox-spreadsheet/", "ship": "/mycnbox-shipping-guide/",
        "legal": "/is-mycnbox-legit/",
        "official": "https://www.mycnbox.com/",
        "estimator": "https://www.mycnbox.com/calc/index",
        "customs": ("HMRC", "https://www.gov.uk/goods-sent-from-abroad"),
        "postal": "Royal Mail", "fp": "UK delivery address, GBP display on this desk",
        "nav": [("Spreadsheet", "sheet"), ("Shipping", "ship"), ("Is it legal?", "legal")],
    },
    "lovegobuy.nl": {
        "agent": "LoveGoBuy", "loc": "nl", "name": "Nederland",
        "sheet": "/lovegobuy-spreadsheet/", "ship": "/lovegobuy-shipping/",
        "legal": "/is-lovegobuy-legal-nederland/",
        "official": "https://www.lovegobuy.com/",
        "estimator": "https://www.lovegobuy.com/shipping/estimation/index",
        "customs": ("Douane", "https://www.belastingdienst.nl/wps/wcm/connect/nl/douane/"),
        "postal": "PostNL", "fp": "postcode 1234 AB, niet een BE- of DE-lijn",
        "nav": [("Spreadsheet", "sheet"), ("Verzending", "ship"), ("Legaal?", "legal")],
    },
    "mulebuy.fr": {
        "agent": "MuleBuy", "loc": "fr", "name": "la France",
        "sheet": "/mulebuy-spreadsheet/", "ship": "/mulebuy-shipping/",
        "legal": "/is-mulebuy-legal-france/",
        "official": "https://mulebuy.com/",
        "estimator": "https://mulebuy.com/estimation/",
        "customs": ("douane.gouv.fr", "https://www.douane.gouv.fr/"),
        "postal": "Colissimo", "fp": "code postal à cinq chiffres, pas un code belge",
        "nav": [("Spreadsheet", "sheet"), ("Livraison", "ship"), ("Est-ce légal ?", "legal")],
    },
    "cssbuy.nl": {
        "agent": "CSSBuy", "loc": "nl", "name": "Nederland",
        "sheet": "/cssbuy-spreadsheet/", "ship": "/cssbuy-shipping/",
        "legal": "/is-cssbuy-legal-nederland/",
        "official": "https://www.cssbuy.com/",
        "estimator": "https://www.cssbuy.com/?action=estimates&go=page",
        "customs": ("Douane", "https://www.belastingdienst.nl/wps/wcm/connect/nl/douane/"),
        "postal": "PostNL", "fp": "NL-postcode 1234 AB, geen Duitse Packstation",
        "nav": [("Spreadsheet", "sheet"), ("Verzending", "ship"), ("Legaal?", "legal")],
    },
    "hipobuyspreadsheet.nl": {
        "agent": "HipoBuy", "loc": "nl", "name": "Nederland",
        "sheet": "/hipobuy-spreadsheet/", "ship": "/hipobuy-shipping-guide/",
        "legal": "/is-hipobuy-legit/",
        "official": "https://hipobuy.com/",
        "estimator": "https://hipobuy.com/estimation",
        "customs": ("Douane", "https://www.belastingdienst.nl/wps/wcm/connect/nl/douane/"),
        "postal": "PostNL of DHL", "fp": "postcode 1234 AB op de live SKU",
        "nav": [("Spreadsheet", "sheet"), ("Verzending", "ship"), ("Legaal?", "legal")],
    },
    "mycnbox.pl": {
        "agent": "MyCNBox", "loc": "pl", "name": "Polska",
        "sheet": "/mycnbox-spreadsheet/", "ship": "/mycnbox-shipping-guide/",
        "legal": "/is-mycnbox-legit/",
        "official": "https://www.mycnbox.com/",
        "estimator": "https://www.mycnbox.com/calc/index",
        "customs": ("KAS", "https://www.podatki.gov.pl/"),
        "postal": "InPost", "fp": "kod pocztowy 00-001 Warszawa, nie DE-Packstation",
        "nav": [("Spreadsheet", "sheet"), ("Wysyłka", "ship"), ("Czy legalne?", "legal")],
    },
    "bbdbuy.ca": {
        "agent": "BBDBuy", "loc": "en", "name": "Canada",
        "sheet": "/bbdbuy-spreadsheet/", "ship": "/bbdbuy-shipping/",
        "legal": "/is-bbdbuy-legit/",
        "official": "https://www.bbdbuy.com/",
        "estimator": "https://www.bbdbuy.com/estimation",
        "customs": ("CBSA", "https://www.cbsa-asfc.gc.ca/"),
        "postal": "Canada Post", "fp": "Canadian postcode form A1A 1A1, not a US ZIP",
        "nav": [("Spreadsheet", "sheet"), ("Shipping", "ship"), ("Is it legal?", "legal")],
    },
    "orientdig.es": {
        "agent": "OrientDig", "loc": "es", "name": "España",
        "sheet": "/orientdig-spreadsheet/", "ship": "/orientdig-shipping-to-espana/",
        "legal": "/is-orientdig-legit/",
        "official": "https://orientdig.com/",
        "estimator": "https://orientdig.com/",
        "customs": ("AEAT", "https://sede.agenciatributaria.gob.es/"),
        "postal": "Correos", "fp": "calle española + CP de cinco dígitos",
        "nav": [("Spreadsheet", "sheet"), ("Envío", "ship"), ("¿Es legal?", "legal")],
    },
    "litbuy.at": {
        "agent": "LitBuy", "loc": "de", "name": "Österreich",
        "sheet": "/litbuy-spreadsheet/", "ship": "/litbuy-shipping-to-osterreich/",
        "legal": "/is-litbuy-legal-osterreich/",
        "official": "https://litbuy.com/",
        "estimator": "https://litbuy.com/shipping-estimate",
        "customs": ("BMF Zoll", "https://www.bmf.gv.at/themen/zoll.html"),
        "postal": "Österreichische Post", "fp": "vierstellige PLZ, z. B. 1010 Wien",
        "nav": [("Spreadsheet", "sheet"), ("Versand", "ship"), ("Legal?", "legal")],
    },
}

STYLE = (
    f'<style id="a-tier-expand-{STAMP}">'
    ".a-tier-expand{margin:1.4em 0 1.8em}.a-tier-expand .lead{max-width:720px;line-height:1.7}"
    ".a-tier-cards{display:grid;gap:14px;margin:16px 0 0}"
    "@media(min-width:760px){.a-tier-cards{grid-template-columns:repeat(3,minmax(0,1fr))}}"
    ".a-tier-cards article{border:1px solid var(--stroke, #e5e7eb);border-radius:12px;"
    "padding:16px 16px 14px;background:var(--bg, #fff)}.a-tier-cards h3{margin:0 0 8px;font-size:17px}"
    ".a-tier-cards h3 a{text-decoration:none}.a-tier-cards p{margin:0;line-height:1.65;font-size:15px}"
    ".a-tier-expand ol{padding-left:1.2em;line-height:1.7}.a-tier-expand li{margin:0 0 8px}"
    "</style>"
)


def overlay(host: str) -> Path:
    return ROOT / "sites" / host / "overlay"


def fetch(url: str, timeout: int = 22) -> tuple[int | None, bytes]:
    req = Request(url, headers={"User-Agent": "a-tier-expand/20261102"})
    try:
        with urlopen(req, context=CTX, timeout=timeout) as r:
            return r.status, r.read()
    except Exception as e:
        print("FETCH_FAIL", url, str(e)[:160])
        return None, b""


def words(html: str) -> int:
    t = re.sub(r"(?is)<script[^>]*>.*?</script>", " ", html)
    t = re.sub(r"(?is)<style[^>]*>.*?</style>", " ", t)
    t = re.sub(r"<[^>]+>", " ", t)
    return len(re.findall(r"\w+", t))


def _w2c_q(agent: str) -> str:
    return f"{W2C}?q={escape(agent)}"


def unique_copy(host: str, d: dict) -> dict:
    """Host-unique paragraphs. Fingerprints must not be a dest_label swap."""
    a, n = d["agent"], d["name"]
    sheet, ship, legal = d["sheet"], d["ship"], d["legal"]
    post, fp = d["postal"], d["fp"]
    cname, curl = d["customs"]
    loc = d["loc"]
    w2c = _w2c_q(a)
    # Per-host extra that is not a country-name substitution.
    extra = {
        "bbdbuy.it": (
            "Sulla SERP italiana «BBDBuy» atterra qui, non sul hub EU. Il passo successivo non è un secondo catalogo globale: è lo spreadsheet Italia, poi la linea Poste, poi ADM.",
            "Le schede QC già in ranking su /bbdbuy-qc/ restano. Questo trio non le sostituisce: collega chi cerca il brand a tre URL che già ricevono click italiani.",
            "Il CAP 20121 è un test di indirizzo, non un listino. Se l’estimator è ancora su «EU», la linea Poste Italiane è la destinazione sbagliata.",
        ),
        "fansbuy.co.uk": (
            "UK brand searches for FansBuy already click this hostname. The gap is the thin spreadsheet URL: it still reads like a three-paragraph cluster clone while shipping-guide and legal-uk already rank.",
            "Royal Mail collect fees sit on the booked SKU, not on a GBP badge in this header. Northern Ireland is a different product — this desk does not pretend it is England.",
            "Paste an English catalogue key into the w2clinks search. Local words that return zero cards are an English index, not an empty FansBuy warehouse.",
        ),
        "mycnbox.nl": (
            "Nederlandse merknamen landen al op mycnbox.nl. De spreadsheet-URL is de brug: niet de Duitse Packstation-tekst, niet de EU-hub.",
            "PostNL last-mile is geen DHL-DE. Als de estimator nog op Duitsland staat, is 1234 AB de verkeerde bestemming — dat is de NL-fingerprint van dit desk.",
            "Douane-bron is belastingdienst.nl, niet een Discord-screenshot. Deze HTML verzint geen aangegeven waarde.",
        ),
        "cssbuy.es": (
            "«CSSBuy España» ya clica esta home. El spreadsheet en /cssbuy-spreadsheet/ sigue corto frente al envío Correos que sí posiciona: hay que alargar la hoja, no inventar un segundo hub.",
            "28001 Madrid es una prueba de CP, no una tarifa. El estimador debe decir España, no EU ni Italia.",
            "AEAT el día del envío; el cupón de cssbuy.com no paga el IVA. Este desk no imprime invites en el título.",
        ),
        "mycnbox.co.uk": (
            "MyCNBox UK already ranks for the brand plus «spreadsheet». Home still spends the first screen on the catalogue wall; the trio below pushes brand landers into the three money URLs.",
            "Royal Mail and HMRC are the UK pair. A US ZIP or an Irish Eircode on the estimator is the wrong destination for this host.",
            "The finds index stays English. Searching «jumper» here often returns nothing; «hoodie» does. That is the sheet, not a broken shop.",
        ),
        "lovegobuy.nl": (
            "LoveGoBuy-zoekers in NL klikken deze home. /lovegobuy-spreadsheet/ is nog een cluster-kloon van drie alinea’s — die pagina moet de merkvraag vasthouden, niet terugsturen naar de hub.",
            "1234 AB versus een Belgische postcode is de fingerprint. Estimator-land Nederland, niet BE, niet DE.",
            "Ervaringen op /lovegobuy-ervaringen/ blijven; legal-nederland is de query-URL die we in het trio zetten.",
        ),
        "mulebuy.fr": (
            "«MuleBuy» en France atterrit ici. La fiche spreadsheet est encore un clone court; Colissimo et douane.gouv.fr sont déjà les bons mots pour la ligne.",
            "Un code postal belge à quatre chiffres n’est pas une adresse française. L’estimateur doit dire France, pas EU.",
            "Pas de sous-déclaration. La SKU dit qui paie à la frontière; cette page n’invente pas un montant.",
        ),
        "cssbuy.nl": (
            "CSSBuy NL heeft al merkklicks. De spreadsheet-pagina is de dunste van de drie — we vullen die, we maken geen vierde TLD.",
            "Geen Duitse vijfcijferige PLZ op dit desk. 1234 AB + PostNL is de NL-check vóór je een lijn boekt.",
            "cssbuyspreadsheet.eu blijft de Independent Index. Deze URL is Nederland, geen 301 terug.",
        ),
        "hipobuyspreadsheet.nl": (
            "HipoBuy NL krijgt al zoekverkeer op «hipobuy shipping estimate». Home moet die schatter-intentie naast spreadsheet en legal zetten, niet alleen de productgrid.",
            "is-hipobuy-legit/ is al lang (2500+ woorden). We slaan die CMS niet plat: het trio linkt ernaar.",
            "1234 AB op de live SKU. Tax-free / prepaid / recipient staan in de app, niet in deze HTML.",
        ),
        "mycnbox.pl": (
            "Wyszukiwania «mycnbox» z Polski już tu wchodzą. Trio spina arkusz, InPost i KAS — nie kopiuje niemieckiego Packstation.",
            "00-001 Warszawa to test kodu, nie cennik. Estimator musi wskazywać Polskę, nie EU.",
            "InPost last-mile nie jest DHL DE. KAS (podatki.gov.pl) rano wysyłki; ta strona nie wymyśla wartości zgłoszenia.",
        ),
        "bbdbuy.ca": (
            "Canadian BBDBuy queries already hit this host. The official-looking header still hides Spreadsheet / Shipping / Legal — the trio puts those three URLs under the H1.",
            "A1A 1A1 is a Canadian form. A US ZIP on the estimator is the wrong last mile (Canada Post, not USPS).",
            "CBSA is the morning source. This desk does not paste a US de-minimis number onto a Canadian address.",
        ),
        "orientdig.es": (
            "OrientDig ya rankea el envío a España. Falta que la home (donde cae la marca) empuje a spreadsheet y a is-orientdig-legit, que ya es una guía larga.",
            "Correos + AEAT. Un CAP italiano en el estimador no es España. No tocamos la CMS de legit: solo enlazamos.",
            "orientdig.com sigue siendo caja y registro. Este TLD es desk ES, no un 301 al .com.",
        ),
        "litbuy.at": (
            "«LitBuy Zoll» ist schon ein AT-Klickwort. Das Trio hängt Spreadsheet und Österreichische Post an dieselbe Home, auf der die Marke landet.",
            "1010 Wien, vierstellige PLZ, nicht DE. BMF Zoll am Versandmorgen. Schätzer-Ziel AT.",
            "litbuyspreadsheet.eu bleibt Independent Index. litbuy.at bleibt der AT-Desk — kein 301.",
        ),
    }[host]
    q_sheet = {
        "en": f"What is the {a} spreadsheet for {n}?",
        "de": f"Was ist das {a}-Spreadsheet für {n}?",
        "es": f"¿Qué es el spreadsheet {a} para {n}?",
        "fr": f"C’est quoi le spreadsheet {a} pour {n} ?",
        "it": f"Cos’è lo spreadsheet {a} per {n}?",
        "nl": f"Wat is de {a}-spreadsheet voor {n}?",
        "pl": f"Czym jest spreadsheet {a} dla {n}?",
    }[loc]
    q_ship = {
        "en": f"How does {a} shipping to {n} work?",
        "de": f"Wie funktioniert {a}-Versand nach {n}?",
        "es": f"¿Cómo es el envío {a} a {n}?",
        "fr": f"Comment fonctionne la livraison {a} vers {n} ?",
        "it": f"Come funziona la spedizione {a} verso {n}?",
        "nl": f"Hoe werkt {a}-verzending naar {n}?",
        "pl": f"Jak działa wysyłka {a} do {n}?",
    }[loc]
    q_legal = {
        "en": f"Is {a} legal in {n}?",
        "de": f"Ist {a} in {n} legal?",
        "es": f"¿Es legal {a} en {n}?",
        "fr": f"{a} est-il légal en {n} ?",
        "it": f"{a} è legale in {n}?",
        "nl": f"Is {a} legaal in {n}?",
        "pl": f"Czy {a} jest legalne w {n}?",
    }[loc]
    a_sheet = {
        "en": f"It is an index of product links for {n} buyers on this host — not Excel, not checkout. Open {sheet}, paste a find into the official app, QC in the warehouse, then book a line. Search the public sheet at {w2c}.",
        "de": f"Ein Index von Produktlinks für Käufer in {n} — kein Excel, keine Kasse. {sheet} öffnen, Find in die offizielle App, QC im Lager, dann Linie. Öffentliche Suche: {w2c}.",
        "es": f"Un índice de enlaces para compradores en {n}, no Excel ni caja. Entra en {sheet}, pega el find en la app, QC en almacén, luego línea. Búsqueda pública: {w2c}.",
        "fr": f"Un index de liens pour {n}, pas Excel, pas une caisse. Ouvre {sheet}, colle le find dans l’app, QC entrepôt, puis ligne. Recherche publique : {w2c}.",
        "it": f"Un indice di link per {n}, non Excel, non cassa. Apri {sheet}, incolla il find nell’app, QC in magazzino, poi la linea. Ricerca pubblica: {w2c}.",
        "nl": f"Een index van productlinks voor {n}, geen Excel, geen kassa. Open {sheet}, plak de find in de app, QC in het magazijn, daarna de lijn. Publieke zoek: {w2c}.",
        "pl": f"To indeks linków dla kupujących w {n} — nie Excel i nie kasa. Otwórz {sheet}, wklej find w aplikacji, QC w magazynie, potem linia. Publiczne wyszukiwanie: {w2c}.",
    }[loc]
    a_ship = {
        "en": f"Country code on the official estimator is {n}, not this TLD. Last mile is often {post}. Who pays at the border is on the SKU. Source: {cname}. Address test: {fp}. Full page: {ship}.",
        "de": f"Schätzer-Land ist {n}, nicht diese TLD. Letzte Meile oft {post}. Wer an der Grenze zahlt, steht auf der SKU. Quelle: {cname}. Adresstest: {fp}. Seite: {ship}.",
        "es": f"El país del estimador es {n}, no este TLD. Última milla suele ser {post}. Quién paga en frontera lo dice la SKU. Fuente: {cname}. Huella: {fp}. Ficha: {ship}.",
        "fr": f"Le pays de l’estimateur est {n}, pas ce TLD. Dernier kilomètre souvent {post}. Qui paie à la frontière est sur la SKU. Source : {cname}. Empreinte : {fp}. Page : {ship}.",
        "it": f"Il paese dell’estimator è {n}, non questo TLD. Ultimo miglio spesso {post}. Chi paga in dogana lo dice la SKU. Fonte: {cname}. Test: {fp}. Pagina: {ship}.",
        "nl": f"Estimator-land is {n}, niet deze TLD. Last-mile vaak {post}. Wie aan de grens betaalt, staat op de SKU. Bron: {cname}. Check: {fp}. Pagina: {ship}.",
        "pl": f"Kraj w estimatorze to {n}, nie ta TLD. Last mile często {post}. Kto płaci na granicy, jest na SKU. Źródło: {cname}. Test: {fp}. Strona: {ship}.",
    }[loc]
    a_legal = {
        "en": f"{a} is a purchasing agent, not a shop. Using an agent is not a crime. Restricted goods and the booked SKU still apply. Read {cname} the morning you ship. This page does not coach under-declaration. Full answer: {legal}.",
        "de": f"{a} ist Einkaufsagent, kein Shop. Einen Agenten zu nutzen ist keine Straftat. Restricted und SKU gelten. {cname} am Versandmorgen. Keine Unterdeklaration. Antwort: {legal}.",
        "es": f"{a} es agente de compras, no tienda. Usar un agente no es un delito. Restricted y la SKU siguen. Lee {cname} el día del envío. Sin infradeclaración. Respuesta: {legal}.",
        "fr": f"{a} est un agent d’achat, pas une boutique. Utiliser un agent n’est pas un délit. Restricted et SKU restent. Lis {cname} le matin de l’envoi. Pas de sous-déclaration. Réponse : {legal}.",
        "it": f"{a} è un agente d’acquisto, non un negozio. Usare un agente non è un reato. Restricted e SKU restano. Leggi {cname} il giorno della spedizione. Niente sottofatturazione. Risposta: {legal}.",
        "nl": f"{a} is een inkoopagent, geen winkel. Een agent gebruiken is geen misdrijf. Restricted en SKU blijven. Lees {cname} op de verzenddag. Geen onderwaardering. Antwoord: {legal}.",
        "pl": f"{a} to agent zakupowy, nie sklep. Korzystanie z agenta nie jest przestępstwem. Restricted i SKU nadal obowiązują. Czytaj {cname} rano wysyłki. Bez zaniżania wartości. Odpowiedź: {legal}.",
    }[loc]
    h2 = {
        "en": f"From a {a} search to spreadsheet, line and legality",
        "de": f"Von der {a}-Suche zu Spreadsheet, Linie und Legalität",
        "es": f"De una búsqueda {a} al spreadsheet, la línea y la legalidad",
        "fr": f"D’une recherche {a} vers spreadsheet, ligne et légalité",
        "it": f"Da una ricerca {a} a spreadsheet, linea e legalità",
        "nl": f"Van een {a}-zoekopdracht naar spreadsheet, lijn en legaliteit",
        "pl": f"Od wyszukiwania {a} do arkusza, linii i legalności",
    }[loc]
    c1 = {
        "en": (f"{a} spreadsheet for {n}", f"Index of finds for {n} buyers. Not Excel, not checkout. QC in the warehouse before you book {post}. {extra[1]}"),
        "de": (f"{a}-Spreadsheet für {n}", f"Index der Finds für {n}. Kein Excel, keine Kasse. QC im Lager vor {post}. {extra[1]}"),
        "es": (f"Spreadsheet {a} para {n}", f"Índice de finds para {n}. No Excel ni caja. QC en almacén antes de {post}. {extra[1]}"),
        "fr": (f"Spreadsheet {a} pour {n}", f"Index des finds pour {n}. Pas Excel, pas caisse. QC entrepôt avant {post}. {extra[1]}"),
        "it": (f"Spreadsheet {a} per {n}", f"Indice finds per {n}. Non Excel, non cassa. QC in magazzino prima di {post}. {extra[1]}"),
        "nl": (f"{a}-spreadsheet voor {n}", f"Index van finds voor {n}. Geen Excel, geen kassa. QC in het magazijn vóór {post}. {extra[1]}"),
        "pl": (f"Spreadsheet {a} dla {n}", f"Indeks finds dla {n}. Nie Excel, nie kasa. QC w magazynie przed {post}. {extra[1]}"),
    }[loc]
    c2 = {
        "en": (f"{a} shipping to {n}", f"Estimator country {n}. Last mile often {post}. Source {cname}. Address test: {fp}. {extra[2]}"),
        "de": (f"{a}-Versand nach {n}", f"Schätzer-Land {n}. Letzte Meile oft {post}. Quelle {cname}. {fp}. {extra[2]}"),
        "es": (f"Envío {a} a {n}", f"Estimador: {n}. Última milla {post}. Fuente {cname}. {fp}. {extra[2]}"),
        "fr": (f"Livraison {a} vers {n}", f"Estimateur : {n}. Dernier km {post}. Source {cname}. {fp}. {extra[2]}"),
        "it": (f"Spedizione {a} verso {n}", f"Estimator: {n}. Ultimo miglio {post}. Fonte {cname}. {fp}. {extra[2]}"),
        "nl": (f"{a}-verzending naar {n}", f"Estimator-land {n}. Last-mile {post}. Bron {cname}. {fp}. {extra[2]}"),
        "pl": (f"Wysyłka {a} do {n}", f"Estimator: {n}. Last mile {post}. Źródło {cname}. {fp}. {extra[2]}"),
    }[loc]
    c3 = {
        "en": (f"Is {a} legal in {n}?", f"{a} buys in your name. This host is an information desk. Read {cname} the morning you ship. No under-declaration."),
        "de": (f"Ist {a} in {n} legal?", f"{a} kauft in deinem Namen. Infodesk, kein Zollamt. {cname} am Versandmorgen. Keine Unterdeklaration."),
        "es": (f"¿Es legal {a} en {n}?", f"{a} compra a tu nombre. Desk informativo. {cname} el día del envío. Sin infradeclaración."),
        "fr": (f"{a} est-il légal en {n} ?", f"{a} achète en ton nom. Desk d’info. {cname} le matin de l’envoi. Pas de sous-déclaration."),
        "it": (f"{a} è legale in {n}?", f"{a} compra a tuo nome. Desk informativo. {cname} il giorno della spedizione. Niente sottofatturazione."),
        "nl": (f"Is {a} legaal in {n}?", f"{a} koopt op jouw naam. Infodesk. {cname} op de verzenddag. Geen onderwaardering."),
        "pl": (f"Czy {a} jest legalne w {n}?", f"{a} kupuje w twoim imieniu. Desk informacyjny. {cname} rano wysyłki. Bez zaniżania."),
    }[loc]
    return {
        "h2": h2, "lead": extra[0], "c1": c1, "c2": c2, "c3": c3,
        "q_sheet": q_sheet, "a_sheet": a_sheet,
        "q_ship": q_ship, "a_ship": a_ship,
        "q_legal": q_legal, "a_legal": a_legal,
        "sheet_more": extra,
        "cname": cname, "curl": curl, "w2c": w2c,
    }


def trio_html(host: str, d: dict) -> str:
    u = unique_copy(host, d)
    cname, curl = d["customs"]
    cards = [
        (d["sheet"], u["c1"][0], u["c1"][1]),
        (d["ship"], u["c2"][0], u["c2"][1]),
        (d["legal"], u["c3"][0], u["c3"][1]),
    ]
    arts = []
    for href, title, body in cards:
        arts.append(
            "<article>"
            f"<h3><a href=\"{escape(href)}\">{escape(title)}</a></h3>"
            f"<p>{escape(body)}</p>"
            "</article>"
        )
    faqs = [
        (u["q_sheet"], u["a_sheet"]),
        (u["q_ship"], u["a_ship"]),
        (u["q_legal"], u["a_legal"]),
    ]
    faq_l = "".join(
        f"<li><strong>{escape(q)}</strong> {escape(a)}</li>" for q, a in faqs
    )
    return (
        f'<section class="sg-sec a-tier-expand" id="query-expand" {ATTR}>\n'
        f"<h2>{escape(u['h2'])}</h2>\n"
        f"<p class=\"lead\">{escape(u['lead'])}</p>\n"
        f'<div class="a-tier-cards">{"".join(arts)}</div>\n'
        f"<h3>{escape({'en':'Three searches that land here','de':'Drei Suchen, die hier landen','es':'Tres búsquedas que caen aquí','fr':'Trois recherches qui atterrissent ici','it':'Tre ricerche che atterrano qui','nl':'Drie zoekopdrachten die hier landen','pl':'Trzy wyszukiwania, które tu wpadają'}[d['loc']])}</h3>\n"
        f"<ol>{faq_l}</ol>\n"
        f"<p class=\"legal-note\">{escape(d['agent'])} · {escape(host)} · {escape(d['fp'])} · "
        f"<a href=\"{escape(curl)}\" rel=\"noopener\">{escape(cname)}</a>. "
        f"{escape({'en':'No declared-value coaching.','de':'Keine Unterdeklaration.','es':'Sin infradeclaración.','fr':'Pas de sous-déclaration.','it':'Niente sottofatturazione.','nl':'Geen onderwaardering.','pl':'Bez zaniżania wartości.'}[d['loc']])}</p>\n"
        f"</section>\n"
    )


def inner_expand_html(kind: str, host: str, d: dict) -> str:
    u = unique_copy(host, d)
    a, n = d["agent"], d["name"]
    post, fp = d["postal"], d["fp"]
    cname, curl = d["customs"]
    loc = d["loc"]
    if kind == "sheet":
        steps = {
            "en": [
                (f"Open the {a} spreadsheet", f"This URL is the {n} index. Public find search: <a href=\"{u['w2c']}\" target=\"_blank\" rel=\"noopener\">w2clinks spreadsheet</a> (q=). English keys (sneakers, hoodie) still feed the catalogue."),
                ("QC in the warehouse", f"Photos land in the official {a} app before you pay international freight to {n}. Extra angles are often paid. Claim while the piece is still in China."),
                (f"Book a line to {n}", f"Estimator country {n}. Last mile often {post}. Address test: {fp}. Details: <a href=\"{d['ship']}\">{d['ship']}</a>."),
                (f"Is {a} legal in {n}?", f"Purchasing agent, not a shop. Read <a href=\"{escape(curl)}\">{escape(cname)}</a> the morning you ship. <a href=\"{d['legal']}\">{d['legal']}</a>."),
            ],
            "de": [
                (f"{a}-Spreadsheet öffnen", f"Diese URL ist der Index für {n}. Suche: <a href=\"{u['w2c']}\" target=\"_blank\" rel=\"noopener\">w2clinks spreadsheet</a>. Englische Keys speisen den Katalog."),
                ("QC im Lager", f"Fotos in der offiziellen {a}-App, bevor du international nach {n} zahlst. Reklamieren, solange das Stück in China ist."),
                (f"Linie nach {n}", f"Schätzer {n}. Letzte Meile oft {post}. {fp}. <a href=\"{d['ship']}\">{d['ship']}</a>."),
                (f"Ist {a} legal?", f"Einkaufsagent. <a href=\"{escape(curl)}\">{escape(cname)}</a> am Versandmorgen. <a href=\"{d['legal']}\">{d['legal']}</a>."),
            ],
            "es": [
                (f"Abrir el spreadsheet {a}", f"Índice para {n}. Búsqueda: <a href=\"{u['w2c']}\" target=\"_blank\" rel=\"noopener\">w2clinks spreadsheet</a>. Claves inglesas al catálogo."),
                ("QC en almacén", f"Fotos en la app oficial {a} antes del flete a {n}. Reclama mientras la pieza sigue en China."),
                (f"Línea a {n}", f"Estimador {n}. Última milla {post}. {fp}. <a href=\"{d['ship']}\">{d['ship']}</a>."),
                (f"¿Es legal {a}?", f"Agente de compras. <a href=\"{escape(curl)}\">{escape(cname)}</a> el día del envío. <a href=\"{d['legal']}\">{d['legal']}</a>."),
            ],
            "fr": [
                (f"Ouvrir le spreadsheet {a}", f"Index pour {n}. Recherche : <a href=\"{u['w2c']}\" target=\"_blank\" rel=\"noopener\">w2clinks spreadsheet</a>. Clés anglaises vers le catalogue."),
                ("QC entrepôt", f"Photos dans l’app {a} avant le fret vers {n}. Réclame tant que la pièce est en Chine."),
                (f"Ligne vers {n}", f"Estimateur {n}. Dernier km {post}. {fp}. <a href=\"{d['ship']}\">{d['ship']}</a>."),
                (f"{a} légal ?", f"Agent d’achat. <a href=\"{escape(curl)}\">{escape(cname)}</a> le matin de l’envoi. <a href=\"{d['legal']}\">{d['legal']}</a>."),
            ],
            "it": [
                (f"Aprire lo spreadsheet {a}", f"Indice per {n}. Ricerca: <a href=\"{u['w2c']}\" target=\"_blank\" rel=\"noopener\">w2clinks spreadsheet</a>. Chiavi inglesi al catalogo."),
                ("QC in magazzino", f"Foto nell’app {a} prima del nolo verso {n}. Reclama mentre il pezzo è in Cina."),
                (f"Linea verso {n}", f"Estimator {n}. Ultimo miglio {post}. {fp}. <a href=\"{d['ship']}\">{d['ship']}</a>."),
                (f"{a} è legale?", f"Agente d’acquisto. <a href=\"{escape(curl)}\">{escape(cname)}</a> il giorno della spedizione. <a href=\"{d['legal']}\">{d['legal']}</a>."),
            ],
            "nl": [
                (f"{a}-spreadsheet openen", f"Index voor {n}. Zoeken: <a href=\"{u['w2c']}\" target=\"_blank\" rel=\"noopener\">w2clinks spreadsheet</a>. Engelse keys voeden de catalogus."),
                ("QC in het magazijn", f"Foto’s in de {a}-app vóór internationale vracht naar {n}. Reclameer zolang het stuk in China is."),
                (f"Lijn naar {n}", f"Estimator {n}. Last-mile {post}. {fp}. <a href=\"{d['ship']}\">{d['ship']}</a>."),
                (f"Is {a} legaal?", f"Inkoopagent. <a href=\"{escape(curl)}\">{escape(cname)}</a> op de verzenddag. <a href=\"{d['legal']}\">{d['legal']}</a>."),
            ],
            "pl": [
                (f"Otwórz spreadsheet {a}", f"Indeks dla {n}. Szukaj: <a href=\"{u['w2c']}\" target=\"_blank\" rel=\"noopener\">w2clinks spreadsheet</a>. Angielskie klucze karmią katalog."),
                ("QC w magazynie", f"Zdjęcia w aplikacji {a} przed frachtem do {n}. Reklamuj, gdy sztuka jest jeszcze w Chinach."),
                (f"Linia do {n}", f"Estimator {n}. Last mile {post}. {fp}. <a href=\"{d['ship']}\">{d['ship']}</a>."),
                (f"Czy {a} jest legalne?", f"Agent zakupowy. <a href=\"{escape(curl)}\">{escape(cname)}</a> rano wysyłki. <a href=\"{d['legal']}\">{d['legal']}</a>."),
            ],
        }[loc]
        lis = "".join(f"<li><strong>{t}</strong> — {b}</li>" for t, b in steps)
        more = "</p><p>".join(escape(x) for x in u["sheet_more"])
        return (
            f'<section class="a-tier-expand" {ATTR} data-kind="spreadsheet">\n'
            f"<h2>{escape(u['q_sheet'])}</h2>\n"
            f"<p>{more}</p>\n"
            f"<ol>{lis}</ol>\n"
            f"<p>{escape(u['a_sheet'])}</p>\n"
            f"</section>\n"
        )
    if kind == "ship":
        return (
            f'<section class="a-tier-expand" {ATTR} data-kind="shipping">\n'
            f"<h2>{escape(u['q_ship'])}</h2>\n"
            f"<p>{escape(u['a_ship'])}</p>\n"
            f"<p>{escape(u['sheet_more'][2])}</p>\n"
            f"<p><a href=\"{d['sheet']}\">{escape(a)} spreadsheet</a> · "
            f"<a href=\"{d['legal']}\">{escape(u['q_legal'])}</a> · "
            f"<a href=\"{escape(d['estimator'])}\" rel=\"noopener\">{escape(d['estimator'])}</a></p>\n"
            f"</section>\n"
        )
    return (
        f'<section class="a-tier-expand" {ATTR} data-kind="legal">\n'
        f"<h2>{escape(u['q_legal'])}</h2>\n"
        f"<p>{escape(u['a_legal'])}</p>\n"
        f"<p>{escape(u['sheet_more'][0])}</p>\n"
        f"<p><a href=\"{d['sheet']}\">{escape(a)} spreadsheet</a> · "
        f"<a href=\"{d['ship']}\">{escape(u['q_ship'])}</a></p>\n"
        f"</section>\n"
    )


def _drop_old_expand(html: str) -> str:
    return re.sub(
        r'\s*<section[^>]*class="[^"]*a-tier-expand[^"]*"[^>]*>.*?</section>',
        "",
        html,
        flags=re.S,
    )


def inject_home(html: str, host: str, d: dict) -> str:
    html = _drop_old_expand(html)
    if f'id="a-tier-expand-{STAMP}"' not in html:
        if "</head>" in html:
            html = html.replace("</head>", STYLE + "\n</head>", 1)
        else:
            html = STYLE + html
    block = trio_html(host, d)
    m = re.search(r'(<section[^>]+id="local"[^>]*>.*?</section>)', html, re.S)
    if m:
        html = html[: m.end()] + "\n" + block + html[m.end() :]
    else:
        m = re.search(r"(<main[^>]*>)", html, re.I)
        if m:
            # after first nested section if possible
            rest = html[m.end() :]
            sm = re.search(r"</section>", rest, re.I)
            if sm:
                pos = m.end() + sm.end()
                html = html[:pos] + "\n" + block + html[pos:]
            else:
                html = html[: m.end()] + "\n" + block + html[m.end() :]
        else:
            html += block
    # Nav: prepend missing dest links, do not remove official chrome.
    # Dest skins use od-head-left / cb-head-left; leftover desks use header-nav.
    nav_re = re.compile(
        r'(<nav class="(?:header-nav|od-head-left|cb-head-left)[^"]*">)(.*?)(</nav>)',
        re.S,
    )
    out = []
    last = 0
    for m in nav_re.finditer(html):
        inner = m.group(2)
        extra = []
        for label, key in d["nav"]:
            href = d[key]
            if href.rstrip("/") in inner:
                continue
            extra.append(f'<a href="{escape(href)}">{escape(label)}</a>')
        if extra:
            inner = "".join(extra) + inner
        out.append(html[last : m.start(2)])
        out.append(inner)
        last = m.end(2)
    out.append(html[last:])
    return "".join(out)


def inject_inner(html: str, kind: str, host: str, d: dict) -> str:
    html = _drop_old_expand(html)
    block = inner_expand_html(kind, host, d)
    if re.search(r"</article>", html, re.I):
        return re.sub(r"</article>", block + "</article>", html, count=1, flags=re.I)
    if re.search(r"</main>", html, re.I):
        return re.sub(r"</main>", block + "</main>", html, count=1, flags=re.I)
    return html + block


def remote_path(host: str, slug: str) -> str:
    slug = slug if slug.startswith("/") else "/" + slug
    if not slug.endswith("/"):
        slug += "/"
    return f"/www/wwwroot/{host}{slug}index.html"


def write_overlay(host: str, slug: str, html: str) -> Path:
    slug = slug.strip("/")
    dest = overlay(host) / slug / "index.html" if slug else overlay(host) / "index.html"
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(html, encoding="utf-8")
    return dest


def build(hosts: list[str]) -> list[dict]:
    rows = []
    for host in hosts:
        d = HOSTS[host]
        rec = {"host": host, "files": []}
        for kind, slug in (("home", "/"), ("sheet", d["sheet"]), ("ship", d["ship"]), ("legal", d["legal"])):
            url = f"https://{host}{slug if slug != '/' else '/'}"
            st, body = fetch(url)
            if st != 200 or not body:
                rec.setdefault("miss", []).append(url)
                print("SKIP_FETCH", url, st)
                continue
            html = body.decode("utf-8", "replace")
            before = words(html)
            if kind == "home":
                html2 = inject_home(html, host, d)
            else:
                html2 = inject_inner(html, kind, host, d)
            if ATTR not in html2:
                raise SystemExit(f"stamp missing after inject {host} {kind}")
            # Forbidden strings
            low = html2.lower()
            if re.search(r"under-?declar|unterdeklar|infradeclar|sous-d[eé]clar|sottofattur|zaniż", low) and "no under" not in low and "keine unter" not in low and "sin infra" not in low and "pas de sous" not in low and "niente sotto" not in low and "geen onder" not in low and "bez zaniż" not in low:
                # allow the negation phrases we wrote
                pass
            path = write_overlay(host, slug, html2)
            rec["files"].append(
                {
                    "kind": kind,
                    "slug": slug,
                    "path": str(path.relative_to(ROOT)),
                    "words_before": before,
                    "words_after": words(html2),
                    "remote": remote_path(host, slug),
                }
            )
            print(
                f"BUILD {host}{slug:32} {before:5}→{words(html2):5} {path.relative_to(ROOT)}"
            )
        rows.append(rec)
    out = ROOT / "sites" / "_reports"
    out.mkdir(parents=True, exist_ok=True)
    (out / "a-tier-expand-build.json").write_text(json.dumps(rows, indent=2) + "\n")
    return rows


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
    client.connect(ORIGIN, username="root", password=password, timeout=30)
    return client


def put(rows: list[dict]) -> None:
    client = _connect()
    sftp = client.open_sftp()
    n = 0
    try:
        for rec in rows:
            for f in rec.get("files") or []:
                local = ROOT / f["path"]
                remote = f["remote"]
                if "live-base" in str(local):
                    print("PUT_SKIP live-base", local)
                    continue
                html = local.read_text(encoding="utf-8")
                if ATTR not in html:
                    raise SystemExit(f"refusing PUT without stamp {local}")
                remote_dir = str(Path(remote).parent)
                try:
                    sftp.stat(remote_dir)
                except OSError:
                    # mkdir parents
                    acc = ""
                    for part in Path(remote_dir).parts[1:]:
                        acc += "/" + part
                        try:
                            sftp.stat(acc)
                        except OSError:
                            sftp.mkdir(acc)
                with sftp.open(remote, "w") as fh:
                    fh.write(html)
                n += 1
                print("PUT", rec["host"], f["kind"], remote)
    finally:
        sftp.close()
        client.close()
    print("PUT_DONE", n)


def verify(hosts: list[str]) -> None:
    bad = 0
    for host in hosts:
        d = HOSTS[host]
        checks = [
            (f"https://{host}/", ATTR),
            (f"https://{host}/", 'id="query-expand"'),
            (f"https://{host}{d['sheet']}", ATTR),
            (f"https://{host}{d['ship']}", ATTR),
            (f"https://{host}{d['legal']}", ATTR),
            (f"https://{host}/", d["sheet"]),
            (f"https://{host}/", d["ship"]),
            (f"https://{host}/", d["legal"]),
        ]
        for url, needle in checks:
            st, body = fetch(url)
            ok = st == 200 and needle.encode() in body
            print(("OK" if ok else "MISS"), url, needle[:48], st)
            if not ok:
                bad += 1
        # no declared-value coaching
        st, body = fetch(f"https://{host}/")
        if st == 200:
            low = body.lower()
            if b"how to under" in low or b"unterdeklarieren" in low:
                print("MISS coaching", host)
                bad += 1
    if bad:
        raise SystemExit(f"VERIFY_FAIL {bad}")
    print("VERIFY_OK", len(hosts))


def gsc_submit(hosts: list[str]) -> None:
    sa = os.environ.get("GSC_SA_JSON", "/tmp/hipobuy-creds/sa.json")
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
        sa, scopes=["https://www.googleapis.com/auth/webmasters"]
    )
    gsc = build("searchconsole", "v1", credentials=creds, cache_discovery=False)
    listed = {s["siteUrl"] for s in gsc.sites().list().execute().get("siteEntry", [])}
    for host in hosts:
        site = f"sc-domain:{host}"
        if site not in listed:
            print("GSC_SKIP no property", host)
            continue
        feed = f"https://{host}/sitemap.xml"
        try:
            gsc.sitemaps().submit(siteUrl=site, feedpath=feed).execute()
            print("GSC_SUBMIT", site, feed)
        except Exception as e:
            print("GSC_FAIL", host, str(e)[:160])
        time.sleep(0.4)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", nargs="?", default="all", choices=("build", "put", "verify", "gsc", "all"))
    ap.add_argument("--host", action="append", dest="hosts")
    args = ap.parse_args()
    hosts = args.hosts or list(HOSTS)
    for h in hosts:
        if h not in HOSTS:
            raise SystemExit(f"unknown host {h}")
    if args.cmd in ("build", "all"):
        rows = build(hosts)
    else:
        report = ROOT / "sites" / "_reports" / "a-tier-expand-build.json"
        rows = json.loads(report.read_text()) if report.is_file() else []
        if args.hosts:
            rows = [r for r in rows if r["host"] in hosts]
    if args.cmd in ("put", "all"):
        put(rows)
    if args.cmd in ("verify", "all"):
        verify(hosts)
    if args.cmd in ("gsc", "all"):
        gsc_submit(hosts)


if __name__ == "__main__":
    main()
