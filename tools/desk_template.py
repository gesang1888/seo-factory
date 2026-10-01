"""Country-desk template: hipobuy.es trust structure + anti-spam gates.

Google August 2026 Spam Update re-applies existing policies (not a new
loophole). This template does not cloak, doorway, or scale thin clones.
It encodes the gold editorial blocks and fails generation when a desk
would look like a location-swap doorway.

Gold reference (do not copy Spain-only lab numbers onto other dests):
https://hipobuy.es/ — editorial home, 15 long Help FAQs, dated News,
About/independence, Envíos unique to ES, Breadcrumb + FAQPage JSON-LD.

What we deepen vs gold (helps users and classifiers):
- Catalogue stays on this host with local-currency display, not an
  off-site CNY search box.
- Each dest must name its own customs source and estimator country.
- Never paste another agent’s Spain line-count onto a non-ES desk.
- Sister country TLDs stay separate files (no 301 hub).
"""
from __future__ import annotations

import json
import re
from html import escape

REQUIRED_HOME_IDS = (
    "catalog",
    "agent",
    "sheet-explain",
    "cat-wall",
    "states",
    "restricted",
    "shots",
    "lab",
    "faq",
)

# hipobuy.es inner IA. Generators map these to local slugs.
REQUIRED_PAGES = ("help", "news", "about")

CUSTOMS = {
    "AT": ("BMF Zoll", "https://www.bmf.gv.at/themen/zoll.html"),
    "DE": ("Zoll", "https://www.zoll.de/"),
    "ES": ("Agencia Tributaria / Correos", "https://sede.agenciatributaria.gob.es/"),
    "FR": ("douane.gouv.fr", "https://www.douane.gouv.fr/"),
    "IT": ("Agenzia delle Dogane e dei Monopoli", "https://www.adm.gov.it/portale/"),
    "NL": ("Douane", "https://www.belastingdienst.nl/wps/wcm/connect/nl/douane/"),
    "US": ("CBP", "https://www.cbp.gov/"),
    "CA": ("CBSA", "https://www.cbsa-asfc.gc.ca/"),
    "GB": ("HMRC", "https://www.gov.uk/goods-sent-from-abroad"),
    "AU": ("ABF", "https://www.abf.gov.au/"),
}

# Fingerprints of hipobuy.es Spain-only lab copy. Mentioning that we do
# *not* copy 58 lines is allowed; pasting their snapshot is not.
FORBIDDEN_HTML = (
    r"58 l[ií]neas para Espa",
    r"58 lines for Spain",
    r"19 de ellas aceptaban",
    r"23[,.]81\s*USD",
    r"32[,.]24\s*USD",
    r"\bES AIR\b",
    r"how to under-?declar",
    r"wie unterdeklar",
    r"c[oó]mo infradeclar",
    r"comment sous-d[eé]clar",
    r"gsc-editor-notes",
    r"impressions on a template",
    r"Cruisezhang0202",
    r"9BCFEVFWG",
)

SKIP_CSS = """.skip{position:absolute;left:-999px;top:8px;background:#fff;padding:8px 12px;z-index:20;border-radius:8px}
.skip:focus{left:12px}
.legal-note{font-size:13px;color:#64748b;line-height:1.65;margin:8px 0 0;max-width:640px}
"""


def og_locale(lang: str) -> str:
    return lang.replace("-", "_") if lang else "en"


def skip_link(label: str) -> str:
    return f'<a class="skip" href="#main">{escape(label)}</a>\n'


def webpage_ld(*, url: str, name: str, desc: str, lang: str, brand: str, host: str) -> dict:
    return {
        "@context": "https://schema.org",
        "@type": "WebPage",
        "@id": url,
        "url": url,
        "name": name,
        "description": desc,
        "inLanguage": lang,
        "isPartOf": {"@type": "WebSite", "name": f"{brand} desk", "url": f"https://{host}/"},
        "publisher": {
            "@type": "Organization",
            "name": f"{brand} independent desk",
            "url": f"https://{host}/",
        },
    }


def breadcrumb_ld(items: list[tuple[str, str]]) -> dict:
    return {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "name": name, "item": url}
            for i, (name, url) in enumerate(items)
        ],
    }


def faq_ld(lang: str, pairs: list[tuple[str, str]]) -> dict:
    return {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "inLanguage": lang,
        "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
            for q, a in pairs
        ],
    }


def itemlist_ld(*, url: str, name: str, items: list[tuple[str, str]]) -> dict:
    return {
        "@context": "https://schema.org",
        "@type": "ItemList",
        "name": name,
        "url": url,
        "numberOfItems": len(items),
        "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "name": h, "description": p}
            for i, (h, p) in enumerate(items)
        ],
    }


def organization_ld(*, name: str, url: str, email: str, lang: str, desc: str) -> dict:
    return {
        "@context": "https://schema.org",
        "@type": "Organization",
        "name": name,
        "url": url,
        "email": email,
        "inLanguage": lang,
        "description": desc,
        "contactPoint": {
            "@type": "ContactPoint",
            "email": email,
            "contactType": "customer support",
            "url": url,
        },
    }


def inject_jsonld(html: str, *blocks: dict) -> str:
    extra = "".join(
        f'<script type="application/ld+json">{json.dumps(b, ensure_ascii=False)}</script>\n'
        for b in blocks
        if b
    )
    if "</head>" not in html:
        raise ValueError("inject_jsonld: missing </head>")
    return html.replace("</head>", extra + "</head>", 1)


def customs_for(dest: str | None) -> tuple[str, str]:
    if not dest:
        return ("the destination customs site named in the estimator", "")
    return CUSTOMS.get(dest, (f"customs for {dest}", ""))


def _f(facts: dict) -> dict:
    dest = facts.get("dest")
    cname, curl = customs_for(dest)
    return {
        **facts,
        "customs": facts.get("customs") or cname,
        "customs_url": facts.get("customs_url") or curl,
        "dest_label": facts.get("dest_label") or "a country in the estimator",
        "ccy": facts.get("ccy") or "USD",
        "date": facts.get("date") or "1 Oct 2026",
        "storage": facts.get("storage") or "see official Help Center",
        "agent": facts.get("agent") or "the agent",
        "host": facts.get("host") or "",
        "estimator": facts.get("estimator") or "",
        "official": facts.get("official") or "",
    }


def long_faqs(facts: dict) -> list[tuple[str, str]]:
    """Fifteen Help FAQs in the desk language. Each dest answer names local customs."""
    x = _f(facts)
    loc = facts.get("loc") or "en"
    packs = {
        "de": _faq_de,
        "es": _faq_es,
        "fr": _faq_fr,
        "it": _faq_it,
        "nl": _faq_nl,
    }
    fn = packs.get(loc, _faq_en)
    pairs = fn(x)
    extras = _faq_extras(loc, x)
    if len(pairs) != 15 or len(extras) != 15:
        raise RuntimeError(f"faq count {len(pairs)} extras {len(extras)}")
    return [(q, f"{a} {ex}".strip()) for (q, a), ex in zip(pairs, extras)]


def _faq_extras(loc: str, x: dict) -> list[str]:
    """Second paragraph per question — unique topic, dest-named. Gold Help answers run 50–80 words."""
    dest, agent, host = x["dest_label"], x["agent"], x["host"]
    cname, ccy, store, est = x["customs"], x["ccy"], x["storage"], x["estimator"]
    date, official = x["date"], x["official"]
    table = {
        "en": [
            f"The cards on {host} are a reading of the finds index, not stock {agent} owns. Payment never happens on this hostname.",
            f"Switching chrome language on {host} does not change the official app. Confirm the in-app language the morning you order toward {dest}.",
            f"The category wall still exposes the English keys (sneakers, hoodie, jacket) so you can paste them into /api/products/ on {host}. Measured {date}.",
            f"Warehouse photos sit between the two payments. Do not book international freight to {dest} until you have accepted QC in-app.",
            f"If the official SPA still prints USD digits after you pick {ccy}, trust the digits and {est}, not this HTML. Display rate dated {date}.",
            f"Register links on this desk never collect card numbers. Those fields exist only on {official}. {host} has no saved method.",
            f"The widget uses 35×25×10 cm and 1000 g as a lab habit; your carton will differ. Open {est} with destination {dest} before you pay freight.",
            f"Prepaid vs collect is chosen when you submit the parcel, not when you buy the goods. Read the SKU heading and {cname} the same morning.",
            f"A screenshot of a threshold from Discord is not a filing. {cname} is the source this desk names. We will not invent a declared value for {dest}.",
            f"Storage clock on this agent: {store}. After that the warehouse can charge or dispose — official Help, not this page. Split cartons each need a {dest} estimate.",
            f"If a photo is blurry, buy another angle in-app before the piece leaves China toward {dest}. This desk cannot open a ticket.",
            f"Restricted is a platform purchase block, not a {cname} seizure notice. Price-0 cards on {host} are not a shop error you can checkout.",
            f"Price 0 often means the Weidian or Taobao link died. Open the live {agent} product page the same day; do not plan the haul on this HTML.",
            f"Refunds for actual vs estimated weight are an official FAQ topic. Re-run {est} after warehouse photos, destination {dest}, then pay.",
            f"{host} cannot look up an order ID. Keep the in-app number. Claims and chat live on {official} only.",
        ],
        "de": [
            f"Die Karten auf {host} sind ein Index, kein Lager von {agent}. Auf diesem Hostnamen wird nicht kassiert.",
            f"Die Sprache dieses Desks ändert die App nicht. In-App-Sprache am Bestelltag prüfen. Lieferadresse im {dest}-Format.",
            f"Die Kategorie-Wand zeigt weiter die englischen Schlüssel (sneakers, hoodie, jacket) für /api/products/ auf {host}. Messung {date}.",
            f"Lagerfotos sitzen zwischen den zwei Zahlungen. Internationale Fracht nach {dest} erst nach akzeptiertem QC in der App buchen.",
            f"Wenn die offizielle SPA nach Wahl von {ccy} weiter USD-Ziffern druckt, den Ziffern und {est} trauen, nicht diesem HTML. Kurs {date}.",
            f"Register-Links auf diesem Desk sammeln keine Kartennummern. Die Felder gibt es nur auf {official}. {host} speichert keine Methode.",
            f"Das Widget nutzt 35×25×10 cm und 1000 g als Laborgewohnheit; dein Karton weicht ab. {est} mit Ziel {dest} öffnen, bevor du Porto zahlst.",
            f"Prepaid oder Empfänger wählst du beim Paket, nicht beim Warenkauf. SKU-Kopf und {cname} am selben Morgen lesen. Dieser Desk nennt keine Unterdeklaration für {dest}.",
            f"Ein Discord-Screenshot einer Schwelle ist keine Anmeldung. Quelle dieses Desks: {cname}. Wir erfinden keinen Deklarationsbetrag für {dest}, auch nicht „unter IOSS“.",
            f"Speicherregel: {store}. Danach kann das Lager berechnen oder entsorgen — offizielle Hilfe, nicht diese Seite. Geteilte Kartons jeweils nach {dest} schätzen.",
            f"Unscharfes Foto: extra Winkel in der App kaufen, solange das Stück noch in China ist, Ziel {dest}. Dieser Desk öffnet kein Ticket.",
            f"Restricted ist eine Plattform-Kauf-Sperre, kein {cname}-Beschlag. Preis-0-Karten auf {host} sind kein Checkout und keine Bestellung nach {dest}.",
            f"Preis 0 heißt oft: Weidian- oder Taobao-Link tot. Live-Seite von {agent} am selben Tag öffnen; dieses HTML ist kein Haul-Plan.",
            f"Rückerstattung Schätzung vs. Istgewicht steht in der offiziellen FAQ. {est} nach Lagerfotos mit Ziel {dest} neu rechnen, dann zahlen.",
            f"{host} sieht keine Bestellnummer. Die In-App-ID behalten. Reklamation und Chat nur auf {official}.",
        ],
        "es": [
            f"Las fichas de {host} son un índice, no stock de {agent}. En este hostname no se cobra.",
            f"El idioma de este desk no cambia la app. Confirma el idioma in-app el día que pidas hacia {dest}.",
            f"El muro de categorías sigue mostrando las claves inglesas (sneakers, hoodie, jacket) para /api/products/ en {host}. Medido {date}.",
            f"Las fotos de almacén van entre los dos pagos. No reserves el flete internacional a {dest} hasta aceptar el QC en la app.",
            f"Si la SPA oficial sigue pintando dígitos USD tras elegir {ccy}, fíate de los dígitos y de {est}, no de este HTML. Tipo {date}.",
            f"Los enlaces Register de este desk no recogen números de tarjeta. Esos campos solo existen en {official}. {host} no guarda método.",
            f"El widget usa 35×25×10 cm y 1000 g como hábito de laboratorio; tu caja será otra. Abre {est} con destino {dest} antes de pagar el flete.",
            f"Prepaid o destinatario se elige al enviar el paquete, no al comprar la mercancía. Lee el encabezado de la SKU y {cname} esa mañana.",
            f"Una captura de Discord sobre un umbral no es un trámite. La fuente de este desk es {cname}. No inventamos un valor declarado para {dest}.",
            f"Reloj de almacén: {store}. Después el almacén puede cobrar o destruir — ayuda oficial, no esta página. Cada caja partida se estima hacia {dest}.",
            f"Si la foto sale borrosa, compra otro ángulo in-app antes de que la pieza salga hacia {dest}. Este desk no abre tickets.",
            f"Restricted es un bloqueo de compra de la plataforma, no un embargo de {cname}. Precio 0 en {host} no se paga aquí.",
            f"Precio 0 suele significar que el enlace Weidian o Taobao murió. Abre la ficha viva de {agent} el mismo día; este HTML no es el haul.",
            f"Los reembolsos de estimado vs real están en la FAQ oficial. Vuelve a {est} con destino {dest} tras las fotos y entonces paga.",
            f"{host} no puede buscar un número de pedido. Guarda el ID de la app. Reclamaciones y chat solo en {official}.",
        ],
        "fr": [
            f"Les fiches sur {host} sont un index, pas un stock de {agent}. On n’encaisse rien sur ce nom d’hôte.",
            f"La langue de ce desk ne change pas l’app. Vérifie la langue in-app le matin de la commande vers {dest}.",
            f"Le mur de catégories garde les clés anglaises (sneakers, hoodie, jacket) pour /api/products/ sur {host}. Mesure {date}.",
            f"Les photos d’entrepôt s’intercalent entre les deux paiements. Ne livre pas le fret vers {dest} avant d’avoir accepté le QC dans l’app.",
            f"Si la SPA officielle imprime encore des chiffres USD après {ccy}, croit les chiffres et {est}, pas cet HTML. Taux {date}.",
            f"Les liens Register de ce desk ne collectent pas de numéro de carte. Ces champs n’existent que sur {official}. {host} ne stocke aucune méthode.",
            f"Le widget prend 35×25×10 cm et 1000 g comme habitude labo ; ton carton sera différent. Ouvre {est} vers {dest} avant de payer le fret.",
            f"Prepaid ou destinataire se choisit à l’envoi du colis, pas à l’achat. Lis l’en-tête SKU et {cname} le matin même.",
            f"Une capture Discord d’un seuil n’est pas un dépôt. La source de ce desk est {cname}. On n’invente pas de valeur déclarée pour {dest}.",
            f"Horloge de stockage : {store}. Ensuite l’entrepôt peut facturer ou jeter — aide officielle, pas cette page. Chaque carton coupé s’estime vers {dest}.",
            f"Photo floue : achète un autre angle in-app avant que la pièce parte vers {dest}. Ce desk n’ouvre pas de ticket.",
            f"Restricted est un blocage d’achat plateforme, pas une saisie {cname}. Prix 0 sur {host} n’est pas une caisse.",
            f"Prix 0 veut souvent dire que le lien Weidian ou Taobao est mort. Ouvre la fiche live {agent} le jour même ; cet HTML n’est pas le haul.",
            f"Les remboursements estimé vs réel sont dans la FAQ officielle. Relance {est} vers {dest} après les photos, puis paie.",
            f"{host} ne retrouve pas un numéro de commande. Garde l’ID in-app. Litiges et chat uniquement sur {official}.",
        ],
        "it": [
            f"Le schede su {host} sono un indice, non scorte di {agent}. Su questo hostname non si incassa.",
            f"La lingua di questo desk non cambia l’app. Controlla la lingua in-app il mattino dell’ordine verso {dest}.",
            f"Il muro categorie mostra ancora le chiavi inglesi (sneakers, hoodie, jacket) per /api/products/ su {host}. Misura {date}.",
            f"Le foto di magazzino stanno tra i due pagamenti. Non prenotare il nolo verso {dest} prima di accettare il QC in-app.",
            f"Se la SPA ufficiale stampa ancora cifre USD dopo {ccy}, fidati delle cifre e di {est}, non di questo HTML. Tasso {date}.",
            f"I link Register di questo desk non raccolgono numeri di carta. Quei campi esistono solo su {official}. {host} non salva metodi.",
            f"Il widget usa 35×25×10 cm e 1000 g come abitudine lab; il tuo cartone sarà diverso. Apri {est} verso {dest} prima di pagare il nolo.",
            f"Prepaid o destinatario si sceglie all’invio del pacco, non all’acquisto. Leggi l’intestazione SKU e {cname} quella mattina.",
            f"Uno screenshot Discord di una soglia non è una dichiarazione. La fonte di questo desk è {cname}. Non inventiamo un valore dichiarato per {dest}.",
            f"Orologio di stoccaggio: {store}. Poi il magazzino può addebitare o smaltire — aiuto ufficiale, non questa pagina. Ogni cartone spezzato si stima verso {dest}.",
            f"Foto mossa: compra un altro angolo in-app prima che il pezzo parta verso {dest}. Questo desk non apre ticket.",
            f"Restricted è un blocco di acquisto della piattaforma, non un sequestro {cname}. Prezzo 0 su {host} non è cassa.",
            f"Prezzo 0 spesso significa che il link Weidian o Taobao è morto. Apri la scheda live {agent} lo stesso giorno; questo HTML non è l’haul.",
            f"I rimborsi stima vs reale stanno nella FAQ ufficiale. Rifai {est} verso {dest} dopo le foto, poi paga.",
            f"{host} non trova un numero d’ordine. Tieni l’ID in-app. Reclami e chat solo su {official}.",
        ],
        "nl": [
            f"De kaarten op {host} zijn een index, geen voorraad van {agent}. Op deze hostname wordt niet geïnd.",
            f"De taal van deze desk verandert de app niet. Check de in-app-taal op de ochtend van bestellen naar {dest}.",
            f"De categorie-muur toont nog de Engelse keys (sneakers, hoodie, jacket) voor /api/products/ op {host}. Gemeten {date}.",
            f"Magazijnfoto’s zitten tussen de twee betalingen. Boek geen internationale vracht naar {dest} voor je QC in de app accepteert.",
            f"Als de officiële SPA na {ccy} nog USD-cijfers toont, vertrouw de cijfers en {est}, niet deze HTML. Koers {date}.",
            f"Register-links op deze desk verzamelen geen kaartnummers. Die velden bestaan alleen op {official}. {host} bewaart geen methode.",
            f"De widget gebruikt 35×25×10 cm en 1000 g als labgewoonte; jouw doos wijkt af. Open {est} naar {dest} voor je porto betaalt.",
            f"Prepaid of ontvanger kies je bij het pakket, niet bij de aankoop. Lees de SKU-kop en {cname} die ochtend.",
            f"Een Discord-screenshot van een drempel is geen aangifte. Bron van deze desk: {cname}. Wij verzinnen geen aangegeven waarde voor {dest}.",
            f"Opslagklok: {store}. Daarna kan het magazijn rekenen of vernietigen — officiële help, niet deze pagina. Gesplitste kartons elk naar {dest} schatten.",
            f"Wazige foto: koop een extra hoek in-app voordat het stuk naar {dest} vertrekt. Deze desk opent geen ticket.",
            f"Restricted is een platform-koopblokkade, geen {cname}-inbeslagname. Prijs 0 op {host} is geen kassa.",
            f"Prijs 0 betekent vaak: Weidian- of Taobao-link dood. Open de live {agent}-fiche dezelfde dag; deze HTML is niet de haul.",
            f"Terugbetaling schatting vs werkelijk staat in de officiële FAQ. Draai {est} opnieuw naar {dest} na foto’s, dan betalen.",
            f"{host} kan geen order-ID opzoeken. Bewaar het in-app-nummer. Klachten en chat alleen op {official}.",
        ],
    }
    return table.get(loc, table["en"])


def _faq_en(x: dict) -> list[tuple[str, str]]:
    dest, agent, host = x["dest_label"], x["agent"], x["host"]
    cname, ccy, store, est = x["customs"], x["ccy"], x["storage"], x["estimator"]
    date, official = x["date"], x["official"]
    hub = not x.get("dest")
    dest_line = (
        f"This hostname is a hub, not a customs territory. The official estimator still needs a real country code."
        if hub
        else f"The estimator destination for this desk is {dest}, not the TLD and not “Europe” as one country."
    )
    return [
        (f"Does {agent} sell the goods on this site?",
         f"No. {agent} is a purchasing agent: it buys from Chinese third-party shops in your name, photographs the parcel in its warehouse, then you book an international SKU. {host} is an independent information desk. Orders, payment and claims stay on {official}."),
        (f"Can I use {agent} in a local language?",
         f"The official app language switcher is independent of this desk. We measured the public site on {date}. Field names in the estimator often stay English even when the chrome is translated. The delivery address must still match {dest}."),
        ("Why does the catalogue return nothing for local words?",
         f"The finds index this desk reads is English (sneakers, hoodie, jacket). Local words often return zero cards — that is an English index, not an empty shop. Type the English key. Measured {date} via /api/products/ on {host}."),
        ("How many times do I pay?",
         f"Twice: first the goods plus China domestic shipping into the warehouse, later the international line to {dest}. Between those payments you can consolidate. This desk never charges you; {agent} does, in-app."),
        (f"Why does the official site show dollars while this desk shows {ccy}?",
         f"On the official SPA the currency switcher has been observed to change the symbol without converting the digits. This desk converts the China warehouse card to {ccy} as a dated display (X-Rates {date}), not a checkout price. Re-read the number in-app the morning you pay."),
        ("How do I pay?",
         f"Only inside {official}. Typical rails are card, PayPal and balance top-up — confirm in the official FAQ the same day. {host} never takes card data and does not store a saved method."),
        ("What is volumetric weight?",
         f"Most air SKUs bill max(actual, L×W×H/divisor) with the result in kilograms (the widget shows grams). A puffy jacket is light on the scale and expensive in volume. Geometry only — live money is in {est} with destination {dest}."),
        (f"Who pays duties into {dest}?",
         f"It is a property of the booked SKU (tax-free, prepaid, or collect). Collect can add a last-mile handling fee the estimator often hides. Educational source for this desk: {cname}. No under-declaration tips."),
        ("Is there a tax threshold I should game?",
         f"No. Thresholds, IOSS and de-minimis change and are not a reason to invent a declared value. Read {cname} and the SKU terms the morning you ship. This desk does not coach a number."),
        ("Can I consolidate several orders?",
         f"Yes — that is the usual saving. Pieces wait in the warehouse until you submit a parcel. Free storage on this agent: {store}. If QC splits cartons, estimate each carton to the same destination {dest}."),
        ("Do they photograph the goods?",
         "Yes, warehouse QC photos land in the app after the piece arrives in China. Extra angles are often a paid add-on. Disputes are easier while it is still in the warehouse, not after it has cleared last-mile."),
        ("What cannot ship?",
         f"Tobacco, alcohol, medicines and banned goods do not travel. Liquids, powders and pastes can need dangerous-goods paperwork. That is platform rule, not {cname} law. Restricted / price-0 cards on this catalogue are not buyable."),
        ("Why is a card restricted or priced 0?",
         f"The source link is not available for agent purchase, or the price could not be read. Do not plan a haul around a zero. Transborder shops are often out of scope. Check the live {agent} product page."),
        ("The parcel is lighter than the estimate?",
         f"Official FAQ covers estimated vs actual weight and postage refunds. This HTML is not a live quote. Re-run {est} with destination {dest} after warehouse photos."),
        (f"Where do I claim if something is wrong?",
         f"Only on {official}, never here. {host} cannot see your account. Use in-app chat / the official Help Center. {dest_line}"),
    ]


def _faq_de(x: dict) -> list[tuple[str, str]]:
    dest, agent, host = x["dest_label"], x["agent"], x["host"]
    cname, ccy, store, est = x["customs"], x["ccy"], x["storage"], x["estimator"]
    date, official = x["date"], x["official"]
    return [
        (f"Verkauft {agent} die Ware auf dieser Seite?",
         f"Nein. {agent} ist Einkaufsagent: er kauft in chinesischen Drittshops in deinem Namen, fotografiert im Lager, danach buchst du eine internationale SKU nach {dest}. {host} ist ein unabhängiger Infodesk. Bestellung, Zahlung und Reklamation nur auf {official}."),
        (f"Kann ich {agent} auf Deutsch stellen?",
         f"Der Sprachwähler der Plattform ist unabhängig von diesem Desk. Gemessen {date}. Feldnamen im Schätzer bleiben oft englisch. Die Lieferadresse muss trotzdem {dest}-Format haben."),
        ("Warum findet der Katalog nichts auf Deutsch?",
         f"Der Index, den /api/products/ auf {host} liest, ist englisch (sneakers, hoodie, jacket). Turnschuhe oder Kapuzenpullover liefern oft 0 Karten. Das ist kein leerer Shop — das ist ein englischer Index. Messung {date}."),
        ("Wie oft wird kassiert?",
         f"Zweimal: zuerst Ware plus Inlandversand nach China-Lager, später die internationale Linie nach {dest}. Dazwischen kannst du bündeln. Dieser Desk kassiert nicht."),
        (f"Warum Dollar auf der offiziellen Seite und {ccy} hier?",
         f"Der offizielle Währungsschalter ändert oft nur das Symbol, nicht die Ziffer. Dieser Desk rechnet die China-Karte nach {ccy} um (X-Rates {date}) — Anzeige, kein Kassenpreis. Zahl in der App am Büchertag lesen."),
        ("Wie zahle ich?",
         f"Nur in {official}. Karte, PayPal, Guthaben — in der offiziellen FAQ desselben Tages prüfen. {host} nimmt keine Kartendaten."),
        ("Was ist Volumengewicht?",
         f"Die meisten Luft-SKUs rechnen max(Ist, L×B×H/Teiler) in Kilogramm (Widget in Gramm). Eine Daunenjacke ist leicht und voluminös. Nur Geometrie — Live-Preis in {est} mit Ziel {dest}."),
        (f"Wer zahlt Abgaben nach {dest}?",
         f"Steht auf der gebuchten SKU (tax free / prepaid / Empfänger). Zusteller können extra kassieren. Quelle dieses Desks: {cname}. Keine Tipps zur Unterdeklaration."),
        ("Gibt es eine Schwelle zum Umgehen?",
         f"Nein. Schwellen, IOSS und de-minimis ändern sich. {cname} und die SKU-Bedingungen am Versandtag lesen. Dieser Desk erfindet keinen Deklarationsbetrag."),
        ("Kann ich mehrere Bestellungen bündeln?",
         f"Ja, der übliche Sparweg. Teile warten im Lager. Speicherregel: {store}. Wenn QC zwei Kartons macht, jeden Karton extra nach {dest} schätzen."),
        ("Gibt es QC-Fotos?",
         "Ja, Lagerfotos landen in der App, sobald die Ware in China angekommen ist. Extra-Winkel sind oft kostenpflichtig. Reklamieren ist einfacher, solange das Stück noch im Lager liegt, nicht nach dem Zoll."),
        ("Was darf nicht?",
         f"Tabak, Alkohol, Arzneimittel, verbotene Ware. Flüssigkeiten/Pulver können Gefahrgut sein. Plattformregel, nicht {cname}. Restricted oder Preis 0 nicht bestellen."),
        ("Warum restricted oder Preis 0?",
         f"Herkunftslink nicht für Agentenkauf, oder Preis unlesbar. Ohne echten Preis nicht planen. Transborder-Shops oft außerhalb. Live-Seite von {agent} prüfen."),
        ("Paket leichter als geschätzt?",
         f"Offizielle FAQ zu Schätzung vs. Istgewicht und Porto-Rückerstattung. Dieses HTML ist kein Live-Quote. {est} nach Lagerfotos mit Ziel {dest} neu rechnen."),
        ("Wo reklamiere ich?",
         f"Nur auf {official}, nicht hier. {host} sieht dein Konto nicht. App-Chat / offizielle Hilfe. Schätzer-Ziel ist {dest}, nicht die TLD."),
    ]


def _faq_es(x: dict) -> list[tuple[str, str]]:
    dest, agent, host = x["dest_label"], x["agent"], x["host"]
    cname, ccy, store, est = x["customs"], x["ccy"], x["storage"], x["estimator"]
    date, official = x["date"], x["official"]
    return [
        (f"¿{agent} vende los productos de esta web?",
         f"No. {agent} es un agente de compras: compra en tiendas chinas de terceros a tu nombre, fotografía en almacén y luego tú eliges la línea a {dest}. {host} es un escritorio informativo independiente. Pedidos y reclamaciones solo en {official}."),
        (f"¿Puedo tener {agent} en español?",
         f"El selector de idioma de la plataforma es independiente de este desk. Lo medimos el {date}. Los campos del estimador suelen seguir en inglés. La dirección tiene que ser de {dest}."),
        ("¿Por qué el catálogo no encuentra nada en español?",
         f"El índice de /api/products/ en {host} está en inglés (sneakers, hoodie, jacket). «Zapatillas» o «sudadera» suelen devolver cero fichas. No es una tienda vacía: es un índice inglés. Medido {date}."),
        ("¿Cuántas veces pago?",
         f"Dos: primero mercancía más envío doméstico a China, después la línea internacional a {dest}. Entremedias puedes agrupar. Este desk no cobra."),
        (f"¿Por qué dólares en lo oficial y {ccy} aquí?",
         f"El conmutador oficial a menudo cambia el símbolo y no el número. Este desk convierte la ficha China a {ccy} (X-Rates {date}) como visualización, no como caja. Lee la cifra en la app el día que pagues."),
        ("¿Cómo pago?",
         f"Solo en {official}. Tarjeta, PayPal, saldo — confirma en la FAQ oficial ese día. {host} no guarda tarjetas."),
        ("¿Qué es el peso volumétrico?",
         f"Casi todas las líneas aéreas facturan el máximo entre real y L×A×H/divisor, en kg (el widget enseña gramos). Una chaqueta inflada pesa poco y ocupa mucho. Solo geometría — el dinero está en {est} con destino {dest}."),
        (f"¿Quién paga aranceles al entrar en {dest}?",
         f"Lo dice la SKU (tax free / prepaid / destinatario). El mensajero puede añadir una tasa. Fuente de este desk: {cname}. Sin infradeclaración."),
        ("¿Hay un umbral para jugar?",
         f"No. Umbrales, IOSS y de-minimis cambian. Lee {cname} y la SKU el día del envío. Este desk no inventa un valor declarado."),
        ("¿Puedo juntar pedidos?",
         f"Sí, el ahorro habitual. Las piezas esperan en almacén. Almacenaje: {store}. Si QC parte cajas, estima cada caja hacia {dest}."),
        ("¿Hacen fotos?",
         "Sí, las fotos de QC de almacén llegan a la app cuando la pieza entra en China. Los ángulos extra suelen pagarse. Reclamar es más fácil mientras sigue en almacén, no después de aduana."),
        ("¿Qué no viaja?",
         f"Tabaco, alcohol, medicamentos, prohibidos. Líquidos y polvos pueden ser mercancía peligrosa. Norma de plataforma, no {cname}. Restricted o precio 0 no se piden."),
        ("¿Por qué restricted o precio 0?",
         f"El enlace de origen no admite compra por agente, o no se leyó el precio. No construyas el haul sobre un cero. Comprueba la ficha viva de {agent}."),
        ("¿El paquete pesa menos de lo estimado?",
         f"La FAQ oficial cubre estimado vs real y reembolsos de porte. Este HTML no es un presupuesto. Vuelve a {est} con destino {dest} tras las fotos de almacén."),
        ("¿Dónde reclamo?",
         f"Solo en {official}, nunca aquí. {host} no ve tu cuenta. Chat in-app / ayuda oficial. El destino del estimador es {dest}, no el TLD."),
    ]


def _faq_fr(x: dict) -> list[tuple[str, str]]:
    dest, agent, host = x["dest_label"], x["agent"], x["host"]
    cname, ccy, store, est = x["customs"], x["ccy"], x["storage"], x["estimator"]
    date, official = x["date"], x["official"]
    return [
        (f"{agent} vend-il la marchandise de ce site ?",
         f"Non. {agent} est un agent : il achète dans des boutiques chinoises de tiers à ton nom, photographie à l’entrepôt, puis tu livres une SKU vers {dest}. {host} est un desk d’information indépendant. Commandes et litiges uniquement sur {official}."),
        (f"Puis-je mettre {agent} en français ?",
         f"Le sélecteur de langue de la plateforme est indépendant de ce desk. Mesure {date}. Les champs de l’estimateur restent souvent en anglais. L’adresse doit être au format {dest} — pas la Belgique si le desk est la France."),
        ("Pourquoi le catalogue ne trouve rien en français ?",
         f"L’index /api/products/ sur {host} est anglais (sneakers, hoodie, jacket). « Baskets » ou « sweat » renvoient souvent zéro fiches. Ce n’est pas une boutique vide. Mesuré {date}."),
        ("Combien de fois je paie ?",
         f"Deux fois : d’abord la marchandise + domestique Chine, ensuite la ligne internationale vers {dest}. Entre les deux tu peux grouper. Ce desk n’encaisse pas."),
        (f"Pourquoi des dollars chez l’officiel et du {ccy} ici ?",
         f"Le sélecteur officiel change souvent le symbole sans convertir le chiffre. Ce desk convertit la fiche Chine en {ccy} (X-Rates {date}) pour l’affichage, pas pour la caisse. Relis le montant dans l’app le jour du paiement."),
        ("Comment je paie ?",
         f"Uniquement sur {official}. Carte, PayPal, solde — FAQ officielle du jour. {host} ne stocke pas de carte."),
        ("C’est quoi le poids volumétrique ?",
         f"La plupart des SKU air facturent max(réel, L×l×H/diviseur) en kg (le widget affiche des grammes). Une doudoune pèse peu et volumine. Géométrie seule — l’argent est dans {est} avec destination {dest}."),
        (f"Qui paie les droits vers {dest} ?",
         f"C’est sur la SKU (tax free / prepaid / destinataire). Le livreur peut ajouter des frais. Source de ce desk : {cname}. Pas de conseil de sous-déclaration."),
        ("Y a-t-il un seuil à contourner ?",
         f"Non. Seuils, IOSS et de-minimis bougent. Lis {cname} et la SKU le matin de l’envoi. Ce desk n’invente pas une valeur déclarée."),
        ("Je peux grouper plusieurs commandes ?",
         f"Oui, l’économie habituelle. Les pièces attendent à l’entrepôt. Stockage : {store}. Si le QC coupe en cartons, estime chaque carton vers {dest}."),
        ("Ils photographient ?",
         "Oui, les photos d’entrepôt arrivent dans l’app une fois la pièce en Chine. Les angles extra sont souvent payants. Réclamer est plus simple tant qu’elle est à l’entrepôt, pas après la douane."),
        ("Qu’est-ce qui ne voyage pas ?",
         f"Tabac, alcool, médicaments, interdits. Liquides et poudres peuvent être dangereux. Règle plateforme, pas {cname}. Restricted ou prix 0 : on n’achète pas."),
        ("Pourquoi restricted ou prix 0 ?",
         f"Le lien source n’est pas achetable par agent, ou le prix n’a pas été lu. Ne construis pas le haul sur un zéro. Vérifie la fiche live {agent}."),
        ("Le colis est plus léger que l’estimé ?",
         f"La FAQ officielle couvre estimé vs réel et remboursement de port. Cet HTML n’est pas un devis. Relance {est} vers {dest} après les photos d’entrepôt."),
        ("Où je réclame ?",
         f"Seulement sur {official}, jamais ici. {host} ne voit pas ton compte. Chat in-app / aide officielle. La destination de l’estimateur est {dest}, pas le TLD."),
    ]


def _faq_it(x: dict) -> list[tuple[str, str]]:
    dest, agent, host = x["dest_label"], x["agent"], x["host"]
    cname, ccy, store, est = x["customs"], x["ccy"], x["storage"], x["estimator"]
    date, official = x["date"], x["official"]
    return [
        (f"{agent} vende la merce di questo sito?",
         f"No. {agent} è un agente: compra nei negozi cinesi terzi a tuo nome, fotografa in magazzino, poi tu prenoti la SKU verso {dest}. {host} è un desk informativo indipendente. Ordini e reclami solo su {official}."),
        (f"Posso mettere {agent} in italiano?",
         f"Il selettore lingua della piattaforma è indipendente da questo desk. Misura {date}. I campi dell’estimator restano spesso in inglese. L’indirizzo deve essere {dest}."),
        ("Perché il catalogo non trova nulla in italiano?",
         f"L’indice /api/products/ su {host} è inglese (sneakers, hoodie, jacket). «Scarpe» o «felpa» spesso danno zero schede. Non è un negozio vuoto. Misurato {date}."),
        ("Quante volte pago?",
         f"Due: prima merce + domestico Cina, poi la linea internazionale verso {dest}. In mezzo puoi raggruppare. Questo desk non incassa."),
        (f"Perché dollari sull’ufficiale e {ccy} qui?",
         f"Il selettore ufficiale spesso cambia il simbolo senza convertire la cifra. Questo desk converte la scheda Cina in {ccy} (X-Rates {date}) come display, non come cassa. Rileggi l’importo in-app il giorno del pagamento."),
        ("Come pago?",
         f"Solo su {official}. Carta, PayPal, saldo — FAQ ufficiale dello stesso giorno. {host} non conserva carte."),
        ("Cos’è il peso volumetrico?",
         f"Molte SKU aeree fatturano max(reale, L×P×H/divisore) in kg (il widget mostra grammi). Un piumino pesa poco e occupa. Solo geometria — i soldi stanno in {est} con destinazione {dest}."),
        (f"Chi paga dazi verso {dest}?",
         f"Lo dice la SKU (tax free / prepaid / destinatario). Il corriere può aggiungere un fee. Fonte di questo desk: {cname}. Niente sottofatturazione."),
        ("C’è una soglia da aggirare?",
         f"No. Soglie, IOSS e de-minimis cambiano. Leggi {cname} e la SKU il giorno della spedizione. Questo desk non inventa un valore dichiarato."),
        ("Posso unire più ordini?",
         f"Sì, il risparmio abituale. I pezzi aspettano in magazzino. Stoccaggio: {store}. Se il QC spezza i cartoni, stima ogni cartone verso {dest}."),
        ("Fanno foto?",
         "Sì, le foto QC di magazzino arrivano in-app quando il pezzo è in Cina. Gli angoli extra sono spesso a pagamento. Reclamare è più facile mentre sta ancora in magazzino, non dopo lo sdoganamento."),
        ("Cosa non viaggia?",
         f"Tabacco, alcol, farmaci, vietati. Liquidi e polveri possono essere merce pericolosa. Regola piattaforma, non {cname}. Restricted o prezzo 0 non si ordinano."),
        ("Perché restricted o prezzo 0?",
         f"Il link di origine non è acquistabile dall’agente, o il prezzo non è stato letto. Non costruire l’haul su uno zero. Controlla la scheda live {agent}."),
        ("Il pacco è più leggero della stima?",
         f"La FAQ ufficiale copre stima vs reale e rimborsi porto. Questo HTML non è un preventivo. Rifai {est} verso {dest} dopo le foto di magazzino."),
        ("Dove reclamo?",
         f"Solo su {official}, mai qui. {host} non vede il tuo account. Chat in-app / aiuto ufficiale. La destinazione dell’estimator è {dest}, non il TLD."),
    ]


def _faq_nl(x: dict) -> list[tuple[str, str]]:
    dest, agent, host = x["dest_label"], x["agent"], x["host"]
    cname, ccy, store, est = x["customs"], x["ccy"], x["storage"], x["estimator"]
    date, official = x["date"], x["official"]
    return [
        (f"Verkoopt {agent} de spullen op deze site?",
         f"Nee. {agent} is een inkoopagent: hij koopt in Chinese derdewinkels op jouw naam, fotografeert in het magazijn, daarna boek jij een internationale SKU naar {dest}. {host} is een onafhankelijke infodesk. Bestellen en klachten alleen op {official}."),
        (f"Kan ik {agent} in het Nederlands zetten?",
         f"De taalschakelaar van het platform is onafhankelijk van deze desk. Gemeten {date}. Veldnamen in de estimator blijven vaak Engels. Het afleveradres moet {dest}-formaat hebben."),
        ("Waarom vindt de catalogus niets in het Nederlands?",
         f"De index van /api/products/ op {host} is Engels (sneakers, hoodie, jacket). «Sneakers» werkt; lokale woorden geven vaak 0 kaarten. Dat is geen lege shop. Gemeten {date}."),
        ("Hoe vaak betaal ik?",
         f"Twee keer: eerst goederen plus binnenlands China, later de internationale lijn naar {dest}. Daartussen kun je bundelen. Deze desk int niks."),
        (f"Waarom dollars op de officiële site en {ccy} hier?",
         f"De officiële valutaswitch verandert vaak alleen het teken, niet het cijfer. Deze desk rekent de China-kaart om naar {ccy} (X-Rates {date}) als weergave, niet als kassa. Lees het bedrag in de app op de dag van betalen."),
        ("Hoe betaal ik?",
         f"Alleen op {official}. Kaart, PayPal, saldo — officiële FAQ van die dag. {host} bewaart geen kaarten."),
        ("Wat is volumgewicht?",
         f"De meeste lucht-SKU’s rekenen max(werkelijk, L×B×H/deler) in kg (widget in gram). Een donsjas is licht en volumineus. Alleen meetkunde — het geld staat in {est} met bestemming {dest}."),
        (f"Wie betaalt invoer naar {dest}?",
         f"Dat staat op de geboekte SKU (tax free / prepaid / ontvanger). De bezorger kan extra innen. Bron van deze desk: {cname}. Geen onderwaarderingstips."),
        ("Is er een drempel om te spelen?",
         f"Nee. Drempels, IOSS en de-minimis wijzigen. Lees {cname} en de SKU op de verzenddag. Deze desk verzint geen aangegeven waarde."),
        ("Kan ik bestellingen bundelen?",
         f"Ja, de gebruikelijke besparing. Stukken wachten in het magazijn. Opslag: {store}. Als QC kartons splitst, schat elk karton naar {dest}."),
        ("Maken ze foto’s?",
         "Ja, magazijn-QC-foto’s landen in de app zodra het stuk in China is. Extra hoeken zijn vaak betaald. Reclame is makkelijker zolang het nog in het magazijn ligt, niet na de douane."),
        ("Wat mag niet mee?",
         f"Tabak, alcohol, medicijnen, verboden spullen. Vloeistoffen en poeders kunnen gevaarlijke goederen zijn. Platformregel, niet {cname}. Restricted of prijs 0 niet bestellen."),
        ("Waarom restricted of prijs 0?",
         f"De bronlink is niet koopbaar via de agent, of de prijs is niet gelezen. Bouw de haul niet op een nul. Check de live {agent}-fiche."),
        ("Het pakket is lichter dan de schatting?",
         f"De officiële FAQ dekt schatting vs werkelijk en portoterugbetaling. Deze HTML is geen live quote. Draai {est} opnieuw naar {dest} na magazijnfoto’s."),
        ("Waar klaag ik?",
         f"Alleen op {official}, nooit hier. {host} ziet je account niet. In-app chat / officiële help. Estimator-bestemming is {dest}, niet de TLD."),
    ]


def lab_copy(facts: dict) -> dict:
    loc = facts.get("loc") or "en"
    x = _f(facts)
    dest, est, date = x["dest_label"], x["estimator"], x["date"]
    hub = not facts.get("dest")
    table = {
        "de": {
            "h2": "Frachtlabor — kein Checkout",
            "cta": "Offiziellen Schätzer öffnen",
            "hub": f"Der Schätzer braucht ein <strong>Land</strong>, nicht diesen Hostnamen. {escape(est)} mit AT, DE, FR, ES… Spanien-Linien eines anderen Agenten bleiben weg.",
            "dest": f"Offiziellen Schätzer mit Ziel <strong>{escape(dest)}</strong> öffnen, bevor du international zahlst. Messgewohnheit: 1000 g / 35×25×10 cm, Kleidung. Labor {escape(date)}. USD-Ziffern können Dollar bleiben, wenn nur das Symbol wechselt.",
        },
        "es": {
            "h2": "Laboratorio de envío — no es caja",
            "cta": "Abrir el estimador oficial",
            "hub": f"El estimador quiere un <strong>país</strong>, no este hostname. {escape(est)} con US, FR, ES… No copiamos el recuento de líneas de España de otro agente.",
            "dest": f"Abre el estimador oficial con destino <strong>{escape(dest)}</strong> antes de pagar el flete. Hábito de laboratorio: 1000 g / 35×25×10 cm, ropa. Lab {escape(date)}. Los dígitos USD pueden seguir en dólares si solo cambia el símbolo.",
        },
        "fr": {
            "h2": "Labo fret — pas une caisse",
            "cta": "Ouvrir l’estimateur officiel",
            "hub": f"L’estimateur veut un <strong>pays</strong>, pas ce nom d’hôte. {escape(est)} avec US, FR, ES… Pas de copie des lignes ES d’un autre agent.",
            "dest": f"Ouvre l’estimateur officiel avec destination <strong>{escape(dest)}</strong> avant de payer le fret. Habitude labo : 1000 g / 35×25×10 cm, vêtements. Lab {escape(date)}. Les chiffres USD peuvent rester en dollars si seul le symbole change.",
        },
        "it": {
            "h2": "Laboratorio spedizione — non è cassa",
            "cta": "Apri l’estimator ufficiale",
            "hub": f"L’estimator vuole un <strong>paese</strong>, non questo hostname. {escape(est)} con US, FR, ES… Niente conteggio linee Spagna di un altro agente.",
            "dest": f"Apri l’estimator ufficiale con destinazione <strong>{escape(dest)}</strong> prima di pagare il nolo. Abitudine lab: 1000 g / 35×25×10 cm, abbigliamento. Lab {escape(date)}. Le cifre USD possono restare dollari se cambia solo il simbolo.",
        },
        "nl": {
            "h2": "Vrachtlab — geen kassa",
            "cta": "Open de officiële estimator",
            "hub": f"De estimator wil een <strong>land</strong>, niet deze hostname. {escape(est)} met US, FR, ES… Geen Spaanse lijnentelling van een andere agent.",
            "dest": f"Open de officiële estimator met bestemming <strong>{escape(dest)}</strong> voordat je internationaal betaalt. Labgewoonte: 1000 g / 35×25×10 cm, kleding. Lab {escape(date)}. USD-cijfers kunnen dollar blijven als alleen het teken wisselt.",
        },
        "en": {
            "h2": "Freight lab — not checkout",
            "cta": "Open the official freight estimate",
            "hub": f"The official estimator needs a <strong>country</strong>, not this hostname. Open {escape(est)} and pick US, CA, FR, ES… Spain-only line counts stay off this hub.",
            "dest": f"Open the official freight estimate with destination <strong>{escape(dest)}</strong> before you pay international freight. Snapshot habit: 1000 g / 35×25×10 cm, clothing. Lab {escape(date)}. USD digits may stay dollars when only the symbol changes.",
        },
    }
    row = table.get(loc, table["en"])
    return {"h2": row["h2"], "cta": row["cta"], "ssub": row["hub"] if hub else row["dest"]}


def keep_copy(loc: str) -> tuple[str, str]:
    return {
        "de": ("Bereits rankend auf diesem Host", "bleibt · nicht überschrieben"),
        "es": ("Ya posiciona en este host", "se conserva · no se pisa"),
        "fr": ("Déjà classé sur cet hôte", "conservé · non écrasé"),
        "it": ("Già in ranking su questo host", "resta · non sovrascritto"),
        "nl": ("Al rankend op deze host", "blijft · niet overschreven"),
        "en": ("Already ranking on this host", "kept · not overwritten"),
    }.get(loc, ("Already ranking on this host", "kept · not overwritten"))


def independence_copy(facts: dict) -> str:
    loc = facts.get("loc") or "en"
    x = _f(facts)
    return {
        "de": f"Unabhängigkeit: {x['host']} ist ein Infodesk, nicht {x['agent']}. Keine Bestellungen, kein Kontozugriff, kein Porto. Schwester-Länderhosts bleiben eigene Dateien — kein 301. Inhalt redaktionell geprüft {x['date']}.",
        "es": f"Independencia: {x['host']} es un escritorio informativo, no {x['agent']}. No gestionamos pedidos ni cobramos envíos. Los hosts hermanos siguen en archivos separados — sin 301. Texto revisado {x['date']}.",
        "fr": f"Indépendance : {x['host']} est un desk d’information, pas {x['agent']}. Pas de commandes, pas d’accès compte, pas de port. Les hôtes sœurs restent des fichiers séparés — pas de 301. Relu {x['date']}.",
        "it": f"Indipendenza: {x['host']} è un desk informativo, non {x['agent']}. Niente ordini, niente accesso al conto, niente nolo. Gli host fratelli restano file separati — niente 301. Testo rivisto {x['date']}.",
        "nl": f"Onafhankelijkheid: {x['host']} is een infodesk, niet {x['agent']}. Geen bestellingen, geen accounttoegang, geen porto. Zushosts blijven aparte bestanden — geen 301. Tekst nagekeken {x['date']}.",
        "en": f"Independence: {x['host']} is an information desk, not {x['agent']}. We do not run orders, take payment, or see your account. Sister country hosts stay separate files — no 301. Copy reviewed {x['date']}.",
    }.get(loc, "")


def skip_label(loc: str) -> str:
    return {
        "de": "Zum Inhalt",
        "es": "Saltar al contenido",
        "fr": "Aller au contenu",
        "it": "Vai al contenuto",
        "nl": "Naar de inhoud",
        "en": "Skip to content",
    }.get(loc, "Skip to content")


def vol_js_labels(loc: str) -> tuple[str, str]:
    """Returns (volumetric, billed) words for the widget."""
    return {
        "de": ("Volumen", "berechnet"),
        "es": ("Volumétrico", "facturado"),
        "fr": ("Volumétrique", "facturé"),
        "it": ("Volumetrico", "fatturato"),
        "nl": ("Volumetrisch", "gefactureerd"),
        "en": ("Volumetric", "billed"),
    }.get(loc, ("Volumetric", "billed"))


def validate_desk(html: str, facts: dict, *, page: str = "home") -> list[str]:
    """Return error strings. Empty list = pass. Call from generators."""
    err: list[str] = []
    x = _f(facts)
    title_m = re.search(r"<title>(.*?)</title>", html, flags=re.S)
    title = title_m.group(1) if title_m else ""
    for tok in facts.get("codes_off_title") or []:
        if tok and tok in title:
            err.append(f"code {tok} in title")
        if tok and page == "home" and tok in html and facts.get("strict_html_codes"):
            err.append(f"code {tok} leaked into HTML")
    for pat in FORBIDDEN_HTML:
        if re.search(pat, html, flags=re.I) and not (
            x.get("dest") == "ES" and x.get("agent") == "HipoBuy"
        ):
            err.append(f"forbidden pattern {pat}")
    if x.get("dest") == "FR" and re.search(r"Belgique|Belgium", title):
        err.append("FR title became Belgium")
    if 'lang="' not in html[:500]:
        err.append("missing html lang")
    if "application/ld+json" not in html:
        err.append("missing JSON-LD")
    if page == "home":
        for sid in REQUIRED_HOME_IDS:
            if f'id="{sid}"' not in html:
                err.append(f"missing #{sid}")
        if "/api/products/" not in html:
            err.append("missing catalogue API")
        if f'var FX_CCY="{x["ccy"]}"' not in html:
            err.append(f"missing FX_CCY {x['ccy']}")
    if "href=\"#main\"" not in html and "href='#main'" not in html:
        err.append("missing skip-to-content")
    if x["host"] and x["host"] not in html:
        err.append("host not mentioned")
    if page in ("home", "help") and x.get("dest"):
        if x["dest_label"] not in html:
            err.append("dest_label missing from dest desk")
        if x["customs"] not in html:
            err.append("customs source missing from dest desk")
    details = re.findall(r"<details class=\"sg-faq\".*?</details>", html, flags=re.S)
    if page in ("home", "help") and len(details) < 12:
        err.append(f"faq count {len(details)}")
    if page == "help":
        if "FAQPage" not in html:
            err.append("help missing FAQPage JSON-LD")
        short = 0
        for block in details:
            paras = re.findall(r"<p>(.*?)</p>", block, flags=re.S)
            text = re.sub(r"<[^>]+>", " ", " ".join(paras))
            if len(re.findall(r"[A-Za-zÀ-ÿ0-9]{2,}", text)) < 40:
                short += 1
        if short > 2:
            err.append(f"help FAQ too short ({short} thin answers)")
    if page == "news" and "ItemList" not in html:
        err.append("news missing ItemList JSON-LD")
    if page == "about" and "ContactPoint" not in html:
        err.append("about missing Organization ContactPoint JSON-LD")
    if "Georgia" in html or "#00C853" in html:
        if x.get("agent") != "HipoBuy":
            err.append("HipoBuy green / Georgia leaked")
    return err


if __name__ == "__main__":
    sample = {
        "agent": "LitBuy",
        "host": "litbuy.at",
        "lang": "de-AT",
        "loc": "de",
        "dest": "AT",
        "dest_label": "Österreich",
        "ccy": "EUR",
        "storage": "90 free days from stocked/listed, 120-day max",
        "estimator": "https://litbuy.com/shipping-estimate",
        "official": "https://litbuy.com/",
        "date": "1 Oct 2026",
        "codes_off_title": ["O4K87NHKR"],
        "strict_html_codes": True,
    }
    pairs = long_faqs(sample)
    assert len(pairs) == 15
    print("desk_template ok", len(pairs), "faqs ·", customs_for("AT")[0], "·", customs_for("ES")[0])
