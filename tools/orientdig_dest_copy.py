"""Localized inner copy for OrientDig dest desks, UK-cluster depth.

Public pages: no ops notes, no declared-value coaching, no invented transit
days or duty rates. Unique ES CMS and FR avis/freight are not rendered here.
"""
from __future__ import annotations

A = "OrientDig"
OFF = "orientdig.com"
EST = "https://orientdig.com/estimation/"


def geo(dest: str) -> str:
    return {
        "AT": "osterreich",
        "ES": "espana",
        "FR": "france",
        "US": "usa",
        "DE": "deutschland",
        "IT": "italia",
        "NL": "nederland",
        "GB": "uk",
    }.get(dest, dest.lower())


def inner_keywords(kind: str, d: dict) -> list[str]:
    g = geo(d["dest"])
    table = {
        "spreadsheet": [f"{A} spreadsheet", f"orientdig spreadsheet {g}", "orientdig trusted sellers"],
        "finds": ["orientdig finds", "orientdig spreadsheet finds", "best orientdig items"],
        "qc": ["orientdig qc", f"orientdig qc {g}", "orientdig warehouse photos"],
        "shipping": ["orientdig shipping", f"orientdig shipping {g}", "orientdig delivery time"],
        "legal": ["orientdig safe", "orientdig legit", f"orientdig safe {g}"],
        "guide": ["orientdig spreadsheet guide", "how to use orientdig", "orientdig buying guide"],
        "faq": ["orientdig faq", "orientdig spreadsheet faq", "orientdig questions"],
    }
    return table[kind]


def inner_serp_title(kind: str, d: dict) -> str:
    key = d["key"]
    table = {
        "spreadsheet": {
            "uk": f"{A} Spreadsheet UK – Best Sellers, QC & Finds",
            "us": f"{A} Spreadsheet USA – Best Sellers, QC & Finds",
            "at": f"{A} Spreadsheet Österreich – Finds und QC",
            "de": f"{A} Spreadsheet Deutschland – Finds und QC",
            "es": f"{A} Spreadsheet España – Mejores finds y QC",
            "fr": f"{A} Spreadsheet France – Meilleurs finds et QC",
            "it": f"{A} Spreadsheet Italia – Migliori finds e QC",
            "nl": f"{A} Spreadsheet Nederland – Beste finds en QC",
        },
        "finds": {
            "uk": f"Top {A} Spreadsheet Finds – Best UK Picks 2026",
            "us": f"Top {A} Spreadsheet Finds – Best US Picks 2026",
            "at": f"{A} spreadsheet finds – Auswahl Österreich 2026",
            "de": f"{A} spreadsheet finds – Auswahl Deutschland 2026",
            "es": f"Mejores finds {A} – selección España 2026",
            "fr": f"Meilleurs finds {A} – sélection France 2026",
            "it": f"Migliori finds {A} – selezione Italia 2026",
            "nl": f"Beste {A} finds – Nederland 2026",
        },
        "qc": {
            "uk": f"{A} QC Photos for UK Buyers – Warehouse Check",
            "us": f"{A} QC Photos for US Buyers – Warehouse Check",
            "at": f"{A} QC-Fotos nach Österreich – Lagercheck",
            "de": f"{A} QC-Fotos nach Deutschland – Lagercheck",
            "es": f"Fotos QC {A} para España – almacén",
            "fr": f"Photos QC {A} France – contrôle entrepôt",
            "it": f"Foto QC {A} Italia – magazzino",
            "nl": f"{A} QC-foto’s Nederland – magazijncheck",
        },
        "shipping": {
            "uk": f"{A} Shipping to the UK – Cost, Time & Royal Mail",
            "us": f"{A} Shipping to the USA – Cost, Time & USPS",
            "at": f"{A} Versand nach Österreich – Preis, Zeit und Post AT",
            "de": f"{A} Versand nach Deutschland – Preis, Zeit und DHL",
            "es": f"Envío {A} a España – coste, plazos y Correos",
            "fr": f"Livraison {A} France – coût, délais et Colissimo",
            "it": f"Spedizione {A} Italia – costi, tempi e Poste",
            "nl": f"{A} verzending Nederland – kosten, tijd en DHL",
        },
        "legal": {
            "uk": f"Is {A} Safe & Legal for UK Buyers? Full Guide",
            "us": f"Is {A} Safe & Legal for US Buyers? Full Guide",
            "at": f"Ist {A} sicher und legal in Österreich?",
            "de": f"Ist {A} sicher und legal in Deutschland?",
            "es": f"¿{A} es seguro y legal en España? Guía",
            "fr": f"{A} est-il sûr et légal en France ? Guide",
            "it": f"{A} è sicuro e legale in Italia? Guida",
            "nl": f"Is {A} veilig en legaal in Nederland?",
        },
        "guide": {
            "uk": f"How to Use {A} Spreadsheet – Beginner Guide UK",
            "us": f"How to Use {A} Spreadsheet – Beginner Guide USA",
            "at": f"{A}-Spreadsheet nutzen – Start für Österreich",
            "de": f"{A}-Spreadsheet nutzen – Start für Deutschland",
            "es": f"Cómo usar el spreadsheet {A} – guía España",
            "fr": f"Utiliser le spreadsheet {A} – guide France",
            "it": f"Usare lo spreadsheet {A} – guida Italia",
            "nl": f"{A}-spreadsheet gebruiken – startergids NL",
        },
        "faq": {
            "uk": f"{A} Spreadsheet FAQ – UK Buyers Guide 2026",
            "us": f"{A} Spreadsheet FAQ – US Buyers Guide 2026",
            "at": f"{A} Spreadsheet FAQ – Leitfaden Österreich",
            "de": f"{A} Spreadsheet FAQ – Leitfaden Deutschland",
            "es": f"FAQ spreadsheet {A} – guía España 2026",
            "fr": f"FAQ spreadsheet {A} – guide France 2026",
            "it": f"FAQ spreadsheet {A} – guida Italia 2026",
            "nl": f"{A} spreadsheet FAQ – gids Nederland 2026",
        },
    }
    return table[kind][key]


def inner_h1(kind: str, d: dict) -> str:
    key = d["key"]
    table = {
        "spreadsheet": {
            "uk": f"{A} Spreadsheet for UK Buyers",
            "us": f"{A} Spreadsheet for US Buyers",
            "at": f"{A} Spreadsheet für Käufer in Österreich",
            "de": f"{A} Spreadsheet für Käufer in Deutschland",
            "es": f"{A} Spreadsheet para compradores en España",
            "fr": f"{A} Spreadsheet pour acheteurs en France",
            "it": f"{A} Spreadsheet per acquirenti in Italia",
            "nl": f"{A} Spreadsheet voor kopers in Nederland",
        },
        "finds": {
            "uk": f"Top {A} Finds for UK Buyers (2026 Guide)",
            "us": f"Top {A} Finds for US Buyers (2026 Guide)",
            "at": f"{A}-Finds für Österreich (2026)",
            "de": f"{A}-Finds für Deutschland (2026)",
            "es": f"Mejores finds {A} para España (guía 2026)",
            "fr": f"Meilleurs finds {A} pour la France (guide 2026)",
            "it": f"Migliori finds {A} per l’Italia (guida 2026)",
            "nl": f"Beste {A}-finds voor Nederland (gids 2026)",
        },
        "qc": {
            "uk": f"{A} QC Photos before Shipping to the UK",
            "us": f"{A} QC Photos before Shipping to the USA",
            "at": f"{A} QC-Fotos vor dem Versand nach Österreich",
            "de": f"{A} QC-Fotos vor dem Versand nach Deutschland",
            "es": f"Fotos QC de {A} antes de enviar a España",
            "fr": f"Photos QC {A} avant envoi vers la France",
            "it": f"Foto QC {A} prima della spedizione in Italia",
            "nl": f"{A} QC-foto’s vóór verzending naar Nederland",
        },
        "shipping": {
            "uk": f"{A} Shipping to the UK (2026 Guide)",
            "us": f"{A} Shipping to the USA (2026 Guide)",
            "at": f"{A}-Versand nach Österreich (Leitfaden 2026)",
            "de": f"{A}-Versand nach Deutschland (Leitfaden 2026)",
            "es": f"Envío {A} a España (guía 2026)",
            "fr": f"Livraison {A} vers la France (guide 2026)",
            "it": f"Spedizione {A} in Italia (guida 2026)",
            "nl": f"{A}-verzending naar Nederland (gids 2026)",
        },
        "legal": {
            "uk": f"Is {A} Safe & Legal for UK Buyers?",
            "us": f"Is {A} Safe & Legal for US Buyers?",
            "at": f"Ist {A} sicher und legal in Österreich?",
            "de": f"Ist {A} sicher und legal in Deutschland?",
            "es": f"¿{A} es seguro y legal para compradores en España?",
            "fr": f"{A} est-il sûr et légal pour les acheteurs en France ?",
            "it": f"{A} è sicuro e legale per acquirenti in Italia?",
            "nl": f"Is {A} veilig en legaal voor kopers in Nederland?",
        },
        "guide": {
            "uk": f"Buying from {A}: A Step-by-Step Guide for UK Buyers",
            "us": f"Buying from {A}: A Step-by-Step Guide for US Buyers",
            "at": f"Kaufen über {A}: Schritte für eine österreichische Adresse",
            "de": f"Kaufen über {A}: Schritte für eine deutsche Adresse",
            "es": f"Comprar en {A}: guía paso a paso para España",
            "fr": f"Acheter avec {A} : guide pas à pas pour la France",
            "it": f"Comprare con {A}: guida passo passo per l’Italia",
            "nl": f"Kopen via {A}: stappenplan voor Nederland",
        },
        "faq": {
            "uk": f"{A} FAQ for UK Buyers (2026)",
            "us": f"{A} FAQ for US Buyers (2026)",
            "at": f"{A} FAQ für Käufer in Österreich (2026)",
            "de": f"{A} FAQ für Käufer in Deutschland (2026)",
            "es": f"FAQ {A} para compradores en España (2026)",
            "fr": f"FAQ {A} pour acheteurs en France (2026)",
            "it": f"FAQ {A} per acquirenti in Italia (2026)",
            "nl": f"{A} FAQ voor kopers in Nederland (2026)",
        },
    }
    return table[kind][key]


def sections_for(kind: str, d: dict, host: str):
    h1 = inner_h1(kind, d)
    fn = {
        "uk": _uk,
        "us": _us,
        "at": _at,
        "de": _de,
        "es": _es,
        "fr": _fr,
        "it": _it,
        "nl": _nl,
    }[d["key"]]
    lead, secs = fn(kind, host, d)
    if kind != "faq":
        secs = list(secs) + extra_local(d, host)
    else:
        secs = list(secs) + extra_faq(d, host)
    return h1, lead, secs


def extra_local(d: dict, host: str) -> list:
    """Local buyer depth: address, currency, last-mile, QC. No ops notes."""
    post, city, customs, curl, ccy = d["post"], d["city"], d["customs"], d["customs_url"], d["ccy"]
    key = d["key"]
    packs = {
        "uk": [
            ("How to fill a UK delivery address", [
                f"Use a UK street and postcode on the label. Northern Ireland is often a different carrier product than mainland {post}, so pick the live line in the app instead of swapping the country name.",
                f"Open {EST} and set destination United Kingdom before you pay international freight.",
            ]),
            (f"Prices in {ccy}", [
                f"This page shows finds in {ccy}. You pay on {OFF} — card, PayPal or balance, whatever the official account offers that day.",
                f"If the official screen still prints a dollar symbol, trust the number in the app and the calculator at {EST}.",
            ]),
            ("Paste a Taobao, 1688 or Weidian link", [
                f"Copy the product URL from the Chinese shop, paste it on {OFF}, and OrientDig buys it into the warehouse. {host} is the spreadsheet and guide for that path toward a UK door.",
                "Sneakers, hoodies, jackets and bags are the usual rows because those SKUs still have QC angles. Electronics, perfume and liquids stay off the sheet unless the app allows them the morning you submit.",
            ]),
            ("QC photos, then Royal Mail", [
                f"Wait for warehouse photos in the app. Extra angles are often a paid add-on. After you accept QC, book the international line. Last mile is often {post}.",
                f"Two payments are normal: goods into China, then freight. Storage days are listed in official Help on {OFF} — read them the day you ship.",
            ]),
            ("Import charges", [
                f"Who pays VAT and handling depends on the booked SKU. {post} can add a collect fee. Read {curl} ({customs}) the morning you ship. This page does not invent a rate or a declared value.",
            ]),
        ],
        "us": [
            ("How to fill a US delivery address", [
                f"Use a US street and ZIP. A Canadian postal code in the A1A 1A1 pattern is the wrong country. Open {EST} with destination United States.",
                f"{city} is the format the label needs.",
            ]),
            (f"Prices in {ccy}", [
                f"Finds on this page are shown in {ccy}. Pay on {OFF}. Live freight is the calculator at {EST}.",
            ]),
            ("Paste a Taobao, 1688 or Weidian link", [
                f"Paste the Chinese shop URL on {OFF}. OrientDig buys into the warehouse, then you book a line toward a US door after QC.",
                "Shoes, hoodies, jackets and bags dominate because those SKUs still have warehouse photos.",
            ]),
            ("QC photos, then USPS", [
                f"Accept warehouse photos in the app, then book freight. Last mile is often {post} or FedEx.",
                f"Two payments: goods first, freight after QC. Storage days live in official Help on {OFF}.",
            ]),
            ("Import charges", [
                f"Who pays duty depends on the booked SKU. Read {curl} ({customs}) the morning you ship. This page does not invent a de-minimis dollar or a declared value.",
            ]),
        ],
        "at": [
            ("Lieferadresse in Österreich", [
                f"Österreichische Straße und vierstellige PLZ — {city}. Eine deutsche Packstation oder fünfstellige DE-PLZ ist das falsche Land.",
                f"Im Schätzer {EST} Ziel Österreich wählen, bevor du Porto zahlst.",
            ]),
            (f"Preise in {ccy}", [
                f"Finds auf dieser Seite stehen in {ccy}. Zahlen tust du auf {OFF}.",
                f"Live-Fracht steht im Rechner {EST} mit Ziel Österreich.",
            ]),
            ("Taobao-, 1688- oder Weidian-Link einfügen", [
                f"Produkt-URL auf {OFF} einfügen. OrientDig kauft ins Lager, danach buchst du die Linie nach Österreich.",
                "Sneaker, Hoodies, Jacken und Taschen haben meist QC-Fotos.",
            ]),
            ("QC-Fotos, dann Österreichische Post", [
                f"Lagerfotos in der App prüfen, dann Fracht buchen. Letzte Meile oft {post}, nicht DHL DE.",
                f"Zwei Zahlungen: Ware, dann Porto. Lagerdauer steht in der Help auf {OFF}.",
            ]),
            ("Abgaben", [
                f"Wer Zoll und Nachnahme zahlt, steht auf der SKU. Quelle: {curl} ({customs}). Diese Seite nennt keinen Deklarationsbetrag.",
            ]),
        ],
        "de": [
            ("Lieferadresse in Deutschland", [
                f"Fünfstellige PLZ. Packstation ist ein deutsches Muster — {city}. 1010 Wien ist Österreich, nicht hier.",
                f"Im Schätzer {EST} Ziel Deutschland wählen.",
            ]),
            (f"Preise in {ccy}", [
                f"Finds auf dieser Seite in {ccy}. Zahlen auf {OFF}. Live-Fracht: {EST} mit Ziel Deutschland.",
            ]),
            ("Taobao-, 1688- oder Weidian-Link einfügen", [
                f"Link auf {OFF} einfügen. OrientDig kauft ins Lager, du buchst danach die Linie nach Deutschland.",
                "Sneaker, Hoodies, Jacken und Taschen haben meist QC-Fotos.",
            ]),
            ("QC-Fotos, dann DHL", [
                f"Fotos in der App prüfen, dann Fracht. Letzte Meile oft {post}. Packstation möglich.",
                f"Zwei Zahlungen: Ware, dann Porto. Lagerdauer in der Help auf {OFF}.",
            ]),
            ("Abgaben", [
                f"SKU entscheidet, wer Zoll zahlt. DHL kann Gebühren kassieren, die der Schätzer nicht zeigt. Quelle: {curl} ({customs}). Kein Deklarationsbetrag auf dieser Seite.",
            ]),
        ],
        "es": [
            ("Dirección de entrega en España", [
                f"Calle española y {city}. Un code postal francés o un CAP italiano es el país equivocado.",
                f"En {EST} elige destino España antes de pagar el flete.",
            ]),
            (f"Precios en {ccy}", [
                f"Los finds de esta página se muestran en {ccy}. Pagas en {OFF}. El flete en vivo está en {EST}.",
            ]),
            ("Pega un enlace de Taobao, 1688 o Weidian", [
                f"Pega la URL en {OFF}. OrientDig compra al almacén y luego reservas la línea hacia España.",
                "Zapatillas, sudaderas, cazadoras y bolsos suelen tener fotos QC.",
            ]),
            ("Fotos QC, luego Correos", [
                f"Revisa las fotos en la app y reserva el flete. Última milla a menudo {post}.",
                f"Dos pagos: mercancía, luego flete. Días de almacén en la Help de {OFF}.",
            ]),
            ("Aduana", [
                f"Quién paga aranceles lo decide la SKU. Fuente: {curl} ({customs}). Esta página no inventa un valor declarado.",
            ]),
        ],
        "fr": [
            ("Adresse de livraison en France", [
                f"Rue française et {city}. Un code postal belge à quatre chiffres est le mauvais pays.",
                f"Dans {EST}, choisissez destination France avant de payer le fret.",
            ]),
            (f"Prix en {ccy}", [
                f"Les finds de cette page s’affichent en {ccy}. Vous payez sur {OFF}. Le fret live est dans {EST}.",
            ]),
            ("Coller un lien Taobao, 1688 ou Weidian", [
                f"Collez l’URL sur {OFF}. OrientDig achète vers l’entrepôt, puis vous réservez la ligne vers la France.",
                "Baskets, hoodies, vestes et sacs ont le plus souvent des photos QC.",
            ]),
            ("Photos QC, puis Colissimo", [
                f"Validez les photos dans l’app, puis le fret. Dernier km souvent {post}.",
                f"Deux paiements : marchandise, puis fret. Durée d’entrepôt dans la Help de {OFF}.",
            ]),
            ("Douane", [
                f"Qui paie droits et Collect dépend de la SKU. Source : {curl} ({customs}). Cette page n’invente pas de valeur déclarée.",
            ]),
        ],
        "it": [
            ("Indirizzo di consegna in Italia", [
                f"Via italiana e {city}. Un código español o un code postal francese è il paese sbagliato.",
                f"In {EST} scegli destinazione Italia prima di pagare il nolo.",
            ]),
            (f"Prezzi in {ccy}", [
                f"I finds di questa pagina sono in {ccy}. Paghi su {OFF}. Il nolo live è in {EST}.",
            ]),
            ("Incolla un link Taobao, 1688 o Weidian", [
                f"Incolla l’URL su {OFF}. OrientDig compra in magazzino, poi prenoti la linea verso l’Italia.",
                "Sneaker, felpe, giacche e borse hanno di solito foto QC.",
            ]),
            ("Foto QC, poi Poste Italiane", [
                f"Controlla le foto in app, poi il nolo. Ultimo miglio spesso {post}.",
                f"Due pagamenti: merce, poi nolo. Giorni di magazzino nella Help di {OFF}.",
            ]),
            ("Dogana", [
                f"Chi paga dazi lo decide la SKU. Fonte: {curl} ({customs}). Questa pagina non inventa un valore dichiarato.",
            ]),
        ],
        "nl": [
            ("Bezorgadres in Nederland", [
                f"Nederlandse straat en {city}. Een Duits Packstation of Belgische postcode is het verkeerde land.",
                f"Kies in {EST} bestemming Nederland vóór je vracht betaalt.",
            ]),
            (f"Prijzen in {ccy}", [
                f"Finds op deze pagina staan in {ccy}. Betalen doe je op {OFF}. Live vracht: {EST}. iDEAL bevestig je in de app.",
            ]),
            ("Plak een Taobao-, 1688- of Weidian-link", [
                f"Plak de URL op {OFF}. OrientDig koopt naar het magazijn, daarna boek je de lijn naar Nederland.",
                "Sneakers, hoodies, jassen en tassen hebben meestal QC-foto’s.",
            ]),
            ("QC-foto’s, dan PostNL", [
                f"Foto’s in de app checken, daarna vracht. Last-mile vaak {post}.",
                f"Twee betalingen: goederen, daarna vracht. Magazijndagen in de Help op {OFF}.",
            ]),
            ("Douane", [
                f"Wie invoerrechten betaalt, staat op de SKU. Bron: {curl} ({customs}). Deze pagina verzint geen aangegeven waarde.",
            ]),
        ],
    }
    return packs[key]


def extra_faq(d: dict, host: str) -> list:
    post, city, customs, curl = d["post"], d["city"], d["customs"], d["customs_url"]
    key = d["key"]
    q = {
        "uk": [
            ("Does Northern Ireland use the same Royal Mail SKU?", [
                f"Often not. {city}. Pick the live line in the app. Mainland last mile is often {post}.",
                f"Confirm destination United Kingdom in {EST}.",
            ]),
            ("Where do I pay?", [
                f"On {OFF}. This page shows finds in the local currency; the account, wallet and tickets stay on the official site.",
            ]),
            ("When do I book freight?", [
                f"After you accept QC photos in the app. Storage days are in official Help on {OFF}.",
            ]),
            ("Who pays import VAT?", [
                f"The booked SKU. Read {curl} ({customs}) the morning you ship. This page does not invent a rate.",
            ]),
        ],
        "us": [
            ("Can I use a Canadian postal code?", [
                f"No. Use a US ZIP — {city}. Destination United States in {EST}.",
            ]),
            ("Where do I pay?", [
                f"On {OFF}. Last mile is often {post}.",
            ]),
            ("When do I book freight?", [
                f"After QC photos. Storage days are in Help on {OFF}.",
            ]),
            ("Who pays duty?", [
                f"The booked SKU. Read {curl} ({customs}). This page does not invent a de-minimis dollar.",
            ]),
        ],
        "at": [
            ("Darf ich eine deutsche Packstation angeben?", [
                f"Nein. Adresse in Österreich — {city}. Packstation ist Deutschland. Letzte Meile oft {post}.",
            ]),
            ("Wo zahle ich?", [
                f"Auf {OFF}. Schätzer: {EST} mit Ziel Österreich.",
            ]),
            ("Wann buche ich Fracht?", [
                f"Nach den QC-Fotos. Lagerdauer in der Help auf {OFF}.",
            ]),
            ("Wer zahlt Zoll?", [
                f"Die SKU. Quelle: {curl} ({customs}). Kein Deklarationsbetrag auf dieser Seite.",
            ]),
        ],
        "de": [
            ("Darf ich 1010 Wien verwenden?", [
                f"Nein. Deutschland — {city}. Packstation möglich. Letzte Meile oft {post}.",
            ]),
            ("Wo zahle ich?", [
                f"Auf {OFF}. Schätzer: {EST} mit Ziel Deutschland.",
            ]),
            ("Wann buche ich Fracht?", [
                f"Nach den QC-Fotos. Lagerdauer in der Help auf {OFF}.",
            ]),
            ("Wer zahlt Zoll?", [
                f"Die SKU. Quelle: {curl} ({customs}). Kein Deklarationsbetrag auf dieser Seite.",
            ]),
        ],
        "es": [
            ("¿Puedo usar un code postal francés?", [
                f"No. España — {city}. Última milla a menudo {post}.",
            ]),
            ("¿Dónde pago?", [
                f"En {OFF}. Calculadora: {EST} destino España.",
            ]),
            ("¿Cuándo reservo el flete?", [
                f"Después de las fotos QC. Días de almacén en la Help de {OFF}.",
            ]),
            ("¿Quién paga aduana?", [
                f"La SKU. Fuente: {curl} ({customs}). Esta página no inventa un valor declarado.",
            ]),
        ],
        "fr": [
            ("Puis-je mettre un code belge ?", [
                f"Non. France — {city}. Dernier km souvent {post}.",
            ]),
            ("Où payer ?", [
                f"Sur {OFF}. Calculateur : {EST} destination France.",
            ]),
            ("Quand réserver le fret ?", [
                f"Après les photos QC. Durée d’entrepôt dans la Help de {OFF}.",
            ]),
            ("Qui paie la douane ?", [
                f"La SKU. Source : {curl} ({customs}). Cette page n’invente pas de valeur déclarée.",
            ]),
        ],
        "it": [
            ("Posso usare un código español?", [
                f"No. Italia — {city}. Ultimo miglio spesso {post}.",
            ]),
            ("Dove pago?", [
                f"Su {OFF}. Calcolatore: {EST} destinazione Italia.",
            ]),
            ("Quando prenoto il nolo?", [
                f"Dopo le foto QC. Giorni di magazzino nella Help di {OFF}.",
            ]),
            ("Chi paga la dogana?", [
                f"La SKU. Fonte: {curl} ({customs}). Questa pagina non inventa un valore dichiarato.",
            ]),
        ],
        "nl": [
            ("Mag ik een Packstation gebruiken?", [
                f"Nee. Nederland — {city}. Last-mile vaak {post}.",
            ]),
            ("Waar betaal ik?", [
                f"Op {OFF}. Calculator: {EST} bestemming Nederland. iDEAL in de app.",
            ]),
            ("Wanneer boek ik vracht?", [
                f"Na de QC-foto’s. Magazijndagen in de Help op {OFF}.",
            ]),
            ("Wie betaalt douane?", [
                f"De SKU. Bron: {curl} ({customs}). Deze pagina verzint geen aangegeven waarde.",
            ]),
        ],
    }
    return q[key]


def wrap_copy(host: str, d: dict, keep_slug: str):
    url = f"/{keep_slug}/"
    loc = d["loc"]
    if loc == "fr":
        return (
            f"Avis {A} France",
            f"Les avis OrientDig pour une adresse en France sont sur {url}. Commandes sur {OFF}.",
            [("Lire la suite", [f"Ouvrez {url}. Colissimo, douane.gouv.fr."])],
        )
    if loc == "de":
        return (
            f"{A} Spreadsheet",
            f"Der ausführliche Text steht unter {url}. Bestellen auf {OFF}.",
            [("Weiterlesen", [f"Öffne {url}."])],
        )
    return (
        f"{A} spreadsheet",
        f"The full article is {url}. Orders stay on {OFF}.",
        [("Continue", [f"Open {url}."])],
    )


def _uk(kind, host, d):
    post, city, customs, curl, ccy = d["post"], d["city"], d["customs"], d["customs_url"], d["ccy"]
    if kind == "spreadsheet":
        return (
            f"A curated {A} spreadsheet for UK buyers on {host}: trusted sellers, QC photos and finds in one index. It is not Excel and not checkout. Order on {OFF} in {ccy} after you pick destination United Kingdom.",
            [
                ("What is an OrientDig spreadsheet?", [
                    f"An {A} spreadsheet on {host} is a shortlist of warehouse-checked SKUs meant for a UK delivery address — sneakers, hoodies, jackets and bags that still open in the official app. It does not take payment and it is not a second OrientDig storefront.",
                    f"Rows stay useful only while the source link is live and at least one warehouse photo exists. A price-0 or restricted card is a dead source, not a discount. Keywords: OrientDig spreadsheet, orientdig spreadsheet uk, orientdig trusted sellers.",
                ]),
                ("Why UK buyers start with a sheet", [
                    f"Searching Taobao, 1688 and Weidian by hand dumps thousands of expired cards. The sheet keeps finds you already accepted in QC before you ask {post} to move a carton toward a UK postcode.",
                    "UK buyers also avoid an EU IOSS screenshot in the official estimator. This page is written for GB, GBP, and HMRC — Northern Ireland is often another carrier product, not a mainland Royal Mail SKU with the country name swapped.",
                ]),
                ("How OrientDig spreadsheets work", [
                    f"Open a find on {host}, read warehouse photos in the official {A} app, then book an international line with destination United Kingdom. {host} only explains that order. Cart, wallet and tickets stay on {OFF}.",
                    f"English catalogue keys (sneakers, hoodie, jacket) on the wall are display labels. They are not a US shop and they do not change the estimator country. Live money is in {EST}.",
                ]),
                ("What types of products are included?", [
                    "Shoes, hoodies, jackets, bags and watches dominate because those SKUs still have QC angles. Electronics, perfume, liquids and other restricted classes stay off the sheet unless the official app shows them as allowed the morning you submit.",
                    "A find that passed QC last month can still go restricted. Recheck the official product page before you pay freight. This index does not freeze a catalogue.",
                ]),
                ("Is using an OrientDig spreadsheet safer?", [
                    f"Safer here means you saw warehouse photos before international freight — not that {customs} disappears. Read {curl} the morning you ship. Import VAT, broker fees and Collect handling change; this page does not paste a rate into the title.",
                    f"The sheet also keeps you off dead Weidian links. It does not file an HMRC entry and it does not pick a declared value for you. {city}.",
                ]),
                ("Who should use an OrientDig spreadsheet?", [
                    f"First-time UK buyers who need an address test and anyone who already uses {A} but wants spreadsheet, finds, QC and shipping-to-UK in one British site in {ccy}.",
                    "If you ship to a French door, this is the wrong country page. If you need a broker, hire one — orders stay on orientdig.com.",
                ]),
                ("Common mistakes without a spreadsheet", [
                    f"Pasting an EU code postal into the estimator, treating {host} as checkout, or booking freight before QC. Last-mile is often {post}; Collect can add a fee the estimator hides.",
                    "Another miss: assuming a ranked VAT article on this site is a live tariff. Thresholds move. Confirm in the official app and on the HMRC page the day you ship.",
                ]),
                ("How to use a spreadsheet efficiently", [
                    f"Keep spreadsheet, finds and QC in one tab set. When a find is accepted, open the official freight form toward the United Kingdom. Source: {customs}.",
                    f"Skip under-declaration tricks. Pay what the booked SKU and {EST} show. Orders stay on {OFF}.",
                ]),
                ("Is an OrientDig spreadsheet required?", [
                    "No. You can search the official app by hand. The sheet exists so UK buyers are not starting from thousands of dead cards every week.",
                    f"You still register and pay on {OFF}. {host} never sees the account.",
                ]),
                ("Ready to use an OrientDig spreadsheet?", [
                    f"Use the cluster links for finds, QC photos and shipping to the UK. Then register on {OFF}. This site stays an index in {ccy}.",
                ]),
            ],
        )
    if kind == "finds":
        return (
            f"Top {A} spreadsheet finds for UK buyers on {host}: QC-checked sneakers, hoodies and bags aimed at a UK address, not a second global catalogue.",
            [
                ("What are top OrientDig finds?", [
                    f"Finds on {host} are SKUs kept after warehouse photos — usually shoes, jackets and bags that still open in the official app. They are not a shop window and they are not copied from a US list with the country name swapped.",
                    "A find drops off when the source URL dies or the warehouse no longer has the piece. Price-0 is a removed card, not a sale.",
                ]),
                ("Why UK buyers use curated OrientDig finds", [
                    f"Manual search mixes dead Weidian links with live cards. Curated finds are the ones that still photograph in China before you book {post} toward a UK postcode.",
                    f"{ccy} display on this desk, destination GB, and a real UK postcode beat hunting Reddit screenshots that never list an HMRC path. {city}.",
                ]),
                ("Popular product categories", [
                    "Sneakers and hoodies fill the wall because those lots still have QC angles. Bags and jackets follow. Restricted goods stay off even if a forum names them.",
                    "Category keys on this site are English display labels. They do not make the parcel an EU import.",
                ]),
                ("How these finds are selected", [
                    f"A find needs a live source URL, at least one warehouse photo, and estimator destination United Kingdom — not this hostname as a country. {city} is the address test.",
                    "We do not keep a find because it was popular last season. If QC fails, it leaves the list.",
                ]),
                ("Are OrientDig finds safer than searching manually?", [
                    f"You still read {customs} ({curl}) the morning you ship. A find only means the piece was photographed in China before international freight.",
                    "Safer is not duty-free. Import VAT and Collect can still apply. This page does not invent an HMRC figure.",
                ]),
                ("Who should use top OrientDig finds?", [
                    "Buyers who already have a UK door and want QC’d picks, not an EU IOSS article. First orders should stay on simple clothing SKUs with photos.",
                    f"If your label is a UK postcode, stay on this British site. Sister country pages are separate files.",
                ]),
                ("Ready to explore top OrientDig finds?", [
                    f"Open QC next, then shipping to the UK. Register and pay on {OFF}. {host} is information only.",
                ]),
            ],
        )
    if kind == "qc":
        return (
            f"QC on {host} means warehouse photos in the official {A} app, taken in China, before you pay freight to the United Kingdom.",
            [
                ("What QC is on this site", [
                    "Quality check is extra angles of the piece in the warehouse — seams, tags, sole, print. It is not a laboratory, not a brand-authentication court, and not an HMRC x-ray.",
                    "Photos land in the official app while the SKU is still in China. That is the only window that matters for a retake.",
                ]),
                ("When to ask for extra photos", [
                    f"Ask while the SKU is in the warehouse. After {post} has the carton, {customs} is the wrong office for a warehouse retake.",
                    "Extra angles are often a paid add-on in the official app. Open tickets in the OrientDig app.",
                ]),
                ("What QC does not do", [
                    f"QC does not file an HMRC entry, does not pay import VAT, and does not invent a declared value. Educational source: {curl}.",
                    "A clean QC album is not a promise the SKU will pass a later platform rule. Recheck before you book the line.",
                ]),
                ("QC and a UK address", [
                    f"Use destination United Kingdom and a UK postcode in the estimator. A French code postal is the wrong country for this site. {city}.",
                    "Warehouse photos are taken in China either way. The UK part is the door on the label after you accept QC.",
                ]),
                ("If a find fails QC", [
                    "Leave it in the warehouse or return it in the official app. Do not book international freight on a reject just to 'get it over with'.",
                    f"Failed QC is cheaper in China than after {post} attempts delivery.",
                ]),
                ("Ready to ship after QC?", [
                    f"Only then open {EST} toward the United Kingdom. {host} does not take payment. {ccy} totals live in the app.",
                ]),
            ],
        )
    if kind == "shipping":
        return (
            f"{A} shipping to the UK uses the official estimator country code GB, not this domain. Open the live freight form after warehouse photos. Last-mile is often {post}.",
            [
                ("How OrientDig shipping to the UK works", [
                    f"Warehouse in China → you accept QC → you book a line with destination United Kingdom → {post} or the SKU’s last-mile partner hands it over. {host} does not print a live quote.",
                    f"The label needs a real UK postcode. {city}. Confirm destination GB in {EST} the morning you ship.",
                ]),
                ("OrientDig shipping options for UK buyers", [
                    "Tax-free, prepaid and collect are properties of the booked SKU in the official app. This page does not rename them. Collect can add a fee the estimator hides.",
                    f"{post} may also add a handling fee on collect parcels. Read the SKU, then the live estimator — not a screenshot from last year.",
                ]),
                ("How long OrientDig shipping to the UK takes", [
                    "Transit days change with the SKU and the line you book. This page does not invent Royal Mail business days.",
                    "Confirm in the official app the morning you ship. Warehouse processing is separate from international transit.",
                ]),
                ("OrientDig shipping costs to the UK", [
                    f"You pay international freight plus whatever the SKU says at the border. {post} can add collect handling. No pound amount is pasted into this title because the live form moves.",
                    f"{ccy} is the local currency on this site. Checkout still happens on {OFF}.",
                ]),
                ("Customs, VAT and import fees", [
                    f"Read {customs} at {curl} the morning you ship. Import VAT thresholds and Collect rules change. Ranked VAT articles on this site stay as local notes — they are not a live tariff table.",
                    "This page does not coach a declared value. Pay what the booked SKU and HMRC rules require.",
                ]),
                ("Common shipping risks", [
                    f"Wrong country in the estimator (EU code postal), booking before QC, ignoring Northern Ireland as another carrier product. Those mistakes are UK-path errors, not 'agent is down'.",
                    "Restricted SKUs that slipped into the warehouse still cannot ride a UK line if the official app blocks them at submit.",
                ]),
                ("Is OrientDig shipping suitable for first-time UK buyers?", [
                    f"Yes if you treat {host} as a map and {OFF} as checkout. Address test: UK postcode. Source: {customs}.",
                    "Start with one clothing SKU, accept QC, then book. Do not consolidate a pile of un-QCd items on the first order.",
                ]),
                ("Ready to ship safely to the UK?", [
                    f"QC first, then {EST} toward the United Kingdom. Orders only on {OFF}.",
                ]),
            ],
        )
    if kind == "legal":
        return (
            f"{A} is a purchasing agent. {host} explains the UK path; it is not the official app and not {customs}. Read HMRC the morning you ship.",
            [
                ("Is OrientDig legal in the UK?", [
                    f"Using a purchasing agent is not a crime in the United Kingdom. Restricted goods, platform rules and the booked SKU still apply. Read {curl} the morning you ship.",
                    "Legal here means the agent model itself. It does not mean every SKU on Taobao is allowed through HMRC.",
                ]),
                ("Is OrientDig safe to use?", [
                    f"Safe on this page means warehouse QC before freight, payment in the official app, and a real UK address — not a promise that a parcel skips {customs}.",
                    f"{ccy} checkout, destination GB, UK postcode on the label. {host} never holds the wallet.",
                ]),
                ("What are the main risks for UK buyers?", [
                    f"Dead source links, booking collect without reading the SKU, and treating {host} as checkout. {post} can add fees.",
                    "A second risk is pasting an EU code postal because the estimator UI looks similar. That is the wrong country for this site. Northern Ireland is often another carrier product.",
                ]),
                ("How can UK buyers reduce risk?", [
                    f"QC in the official app, estimator destination United Kingdom, UK postcode on the label. No under-declaration. No invented HMRC figure.",
                    "Keep spreadsheet, finds and QC together so you are not booking freight on a screenshot from another country page.",
                ]),
                ("Is OrientDig suitable for first-time UK buyers?", [
                    f"Yes if you start with the spreadsheet and finds on {host}, then the official register. This site does not see your account.",
                    "Skip restricted categories on the first order. Clothing SKUs with QC photos are the usual first path.",
                ]),
                ("Final verdict: should UK buyers use OrientDig?", [
                    f"{A} can be used toward the United Kingdom if you follow the official app and {customs}. This site stays independent information. Orders on {OFF}.",
                ]),
                ("Ready to get started?", [
                    f"Open spreadsheet → finds → QC → shipping to the UK. Pay only on {OFF}.",
                ]),
            ],
        )
    if kind == "guide":
        return (
            f"A step-by-step {A} path for a UK address on {host}. Photos in the warehouse, then freight. Not checkout.",
            [
                ("How to buy from OrientDig (UK guide)", [
                    f"Find a QC’d SKU on the spreadsheet or finds list, submit it in the official app, wait for warehouse photos, then book international freight toward the United Kingdom with a UK postcode on the label.",
                    "Do not skip QC to save a day. UK last-mile will not retake a warehouse photo.",
                ]),
                ("What is OrientDig?", [
                    f"A China purchasing agent. {host} only explains the UK path in {ccy}. Payment, tickets and the estimator stay on {OFF}.",
                    "Two payments are normal: goods to the warehouse, then international freight after QC.",
                ]),
                ("Step 1 — pick a find", [
                    f"Use the spreadsheet and finds pages on {host}. English keys (sneakers, hoodie) still feed the catalogue. Local words often return zero cards — that is an English index, not an empty shop.",
                    "Skip restricted and price-0 cards. They are dead sources.",
                ]),
                ("Step 2 — warehouse QC", [
                    "Accept or reject while the piece is in China. Extra angles are often paid in-app.",
                    f"After {post} has the carton, {customs} will not open a warehouse ticket for you.",
                ]),
                ("Step 3 — book GB freight", [
                    f"Open {EST} with destination United Kingdom. {city}. Last-mile is often {post}.",
                    "Prepaid vs collect is a SKU property. This page does not invent Royal Mail days or an HMRC rate.",
                ]),
                ("Step 4 — pay only on the official site", [
                    f"Register and pay on {OFF}. {host} never stores a card. GBP on this desk is display conversion, not checkout.",
                    "If the official SPA still prints USD digits after you pick GBP, trust the digits and the estimator.",
                ]),
                ("Common beginner mistakes", [
                    "EU destination in the estimator, booking before QC, treating this hostname as a shop.",
                    "Northern Ireland is often another carrier product — do not assume the same Royal Mail SKU as mainland GB.",
                ]),
                ("Ready to start?", [
                    f"Spreadsheet → finds → QC → shipping. Then {OFF}.",
                ]),
            ],
        )
    # faq
    return (
        f"{A} spreadsheet FAQ for UK buyers on {host}: index, QC, {post}, {customs}. Not checkout.",
        [
            ("Does this site sell the goods?", [
                f"No. {A} is a purchasing agent. Orders stay on {OFF}. {host} lists finds for UK buyers.",
                "Cards on this hostname are an index, not stock OrientDig owns.",
            ]),
            ("What is the OrientDig spreadsheet?", [
                "A shortlist of warehouse-checked SKUs for a UK door. Not Excel, not a second shop.",
                "Keywords: OrientDig spreadsheet, orientdig spreadsheet uk, orientdig sheet.",
            ]),
            ("How do I use QC photos?", [
                "They land in the official app while the piece is in China. Ask for extra angles there, not after last-mile.",
                f"{post} will not retake a warehouse photo.",
            ]),
            ("How does shipping to the UK work?", [
                f"Estimator destination GB, then the booked SKU. Last-mile is often {post}. Live quote: {EST}.",
                f"{city}. This page does not invent transit days.",
            ]),
            ("Who pays import charges?", [
                f"The booked SKU. {post} can add a collect fee. Source: {curl}. No declared-value coaching.",
                "Ranked VAT notes on this host stay; they are not a live tariff.",
            ]),
            ("Why GBP here and dollars on the official SPA?", [
                f"Display conversion of the China warehouse card. Checkout currency is whatever {OFF} shows the morning you pay.",
                "Trust the official digits and the estimator.",
            ]),
            ("Is Northern Ireland the same as mainland GB?", [
                "Often another carrier product. Do not assume the same Royal Mail SKU.",
                "Pick the live line in the official app.",
            ]),
            ("Where do I register?", [
                f"Only on {OFF}. {host} does not take cards.",
            ]),
        ],
    )


def _us(kind, host, d):
    post, city, customs, curl, ccy = d["post"], d["city"], d["customs"], d["customs_url"], d["ccy"]
    if kind == "spreadsheet":
        return (
            f"A curated {A} spreadsheet for US buyers on {host}: trusted sellers, QC photos and finds in one index. It is not Excel and not checkout. Order on {OFF} in {ccy} after you pick destination United States.",
            [
                ("What is an OrientDig spreadsheet?", [
                    f"An {A} spreadsheet on {host} is a shortlist of warehouse-checked SKUs meant for a US delivery address — sneakers, hoodies, jackets and bags that still open in the official app. It does not take payment and it is not a second OrientDig storefront.",
                    "Rows stay useful only while the source link is live and at least one warehouse photo exists. A price-0 or restricted card is a dead source, not a discount. Keywords: OrientDig spreadsheet, orientdig spreadsheet usa, orientdig trusted sellers.",
                ]),
                ("Why US buyers start with a sheet", [
                    f"Manual Taobao/Weidian search mixes expired cards with live lots. The sheet keeps finds you already accepted in QC before you ask {post} to move a carton toward a US ZIP.",
                    f"US buyers also avoid a Canadian postal code (form A1A 1A1) in the official estimator. This page is written for CBP territory, {ccy}, and a US ZIP — this desk does not invent a de-minimis dollar.",
                ]),
                ("How OrientDig spreadsheets work", [
                    f"Open a find on {host}, read warehouse photos in the official {A} app, then book an international line with destination United States. Cart, wallet and tickets stay on {OFF}.",
                    f"English catalogue keys on the wall are display labels. They do not change the estimator country. Live money is in {EST}.",
                ]),
                ("What types of products are included?", [
                    "Shoes, hoodies, jackets and bags dominate because those SKUs still have QC angles. Electronics, batteries, perfume and other restricted classes stay off unless the official app shows them as allowed the morning you submit.",
                    "A find that passed QC last month can still go restricted. Recheck before you pay freight.",
                ]),
                ("Is using an OrientDig spreadsheet safer?", [
                    f"Safer means warehouse photos before international freight — not that {customs} disappears. Read {curl} the morning you ship. Informal-entry rules change; this page does not paste a dollar into the title.",
                    f"The sheet keeps you off dead Weidian links. It does not file a CBP entry and it does not pick a declared value. Address test: {city}.",
                ]),
                ("Who should use an OrientDig spreadsheet?", [
                    f"First-time US buyers who need a ZIP test and anyone who already uses {A} but wants spreadsheet, finds, QC and shipping-to-US on one American site in {ccy}.",
                    "If you ship to Canada, this is the wrong country page. Orders stay on orientdig.com.",
                ]),
                ("Common mistakes without a spreadsheet", [
                    f"Pasting a Canadian postal code, treating {host} as checkout, or booking freight before QC. Last-mile is often {post} or FedEx; Collect can add a fee the estimator hides.",
                    "Another miss: treating a ranked de-minimis article as a live threshold. Rules move. Confirm in-app and on CBP the day you ship.",
                ]),
                ("How to use a spreadsheet efficiently", [
                    f"Keep spreadsheet, finds and QC together. When a find is accepted, open {EST} toward the United States. Source: {customs}.",
                    f"No under-declaration. Pay what the booked SKU shows. Orders on {OFF}.",
                ]),
                ("Is an OrientDig spreadsheet required?", [
                    "No. You can search the official app by hand. The sheet exists so US buyers are not restarting from dead cards every week.",
                    f"Register and pay on {OFF}. {host} never sees the account.",
                ]),
                ("Ready to use an OrientDig spreadsheet?", [
                    f"Use finds, QC and shipping to the USA, then register on {OFF}. This site stays an index in {ccy}.",
                ]),
            ],
        )
    if kind == "finds":
        return (
            f"Top {A} spreadsheet finds for US buyers on {host}: QC-checked sneakers, hoodies and bags aimed at a US ZIP, not a second global catalogue.",
            [
                ("What are top OrientDig finds?", [
                    f"Finds on {host} are SKUs kept after warehouse photos. They are not copied from a UK list with the country name swapped.",
                    "Price-0 is a removed card, not a sale.",
                ]),
                ("Why US buyers use curated finds", [
                    f"Curated finds still photograph in China before you book {post} toward a US ZIP.",
                    f"{ccy} on this desk, destination US, and a real ZIP beat forum screenshots that never name CBP. This desk does not invent a de-minimis dollar.",
                ]),
                ("Popular product categories", [
                    "Sneakers and hoodies still have QC angles. Restricted goods stay off even if a Discord names them.",
                    "English category keys are display labels. They do not make the parcel a Canadian import.",
                ]),
                ("How these finds are selected", [
                    f"Live source URL, at least one warehouse photo, estimator destination United States. Address test: {city}.",
                    "Failed QC leaves the list.",
                ]),
                ("Are finds safer than searching manually?", [
                    f"You still read {customs} ({curl}) the morning you ship. A find only means photos in China before freight.",
                    "Safer is not duty-free. Collect can still apply.",
                ]),
                ("Who should use these finds?", [
                    "US doors only. First orders: simple clothing SKUs with photos.",
                    "Canadian labels belong on a Canada desk, not here.",
                ]),
                ("Ready to explore?", [
                    f"Open QC, then shipping to the USA. Pay on {OFF}.",
                ]),
            ],
        )
    if kind == "qc":
        return (
            f"QC on {host} means warehouse photos in the official {A} app, taken in China, before you pay freight to the United States.",
            [
                ("What QC is on this site", [
                    "Extra warehouse angles — seams, tags, sole, print. Not a lab, not CBP x-ray, not brand court.",
                    "Photos land in-app while the SKU is still in China.",
                ]),
                ("When to ask for extra photos", [
                    f"While the SKU is in the warehouse. After {post} has the carton, {customs} is the wrong office for a retake.",
                    "Extra angles are often paid in-app. Open tickets in the OrientDig app.",
                ]),
                ("What QC does not do", [
                    f"It does not file a CBP entry and does not invent a de-minimis dollar. Source: {curl}.",
                    "A clean album is not a later platform pass. Recheck before you book.",
                ]),
                ("QC and a US address", [
                    f"Destination United States and a US ZIP. A Canadian postal code is the wrong country. {city}.",
                    "Photos are taken in China either way. The US part is the door after you accept QC.",
                ]),
                ("If a find fails QC", [
                    "Return it in-app. Do not book international freight on a reject.",
                    f"Failed QC is cheaper in China than after {post} attempts delivery.",
                ]),
                ("Ready to ship after QC?", [
                    f"Then open {EST} toward the United States. {host} does not take payment.",
                ]),
            ],
        )
    if kind == "shipping":
        return (
            f"{A} shipping to the USA uses estimator country US, not this domain. Open the live form after warehouse photos. Last-mile is often {post}.",
            [
                ("How OrientDig shipping to the USA works", [
                    f"China warehouse → accept QC → book a line with destination United States → {post} or FedEx. {host} does not print a live quote.",
                    f"The label needs a real US ZIP. Confirm destination US in {EST} the morning you ship.",
                ]),
                ("Shipping options", [
                    "Tax-free, prepaid and collect are SKU properties. Collect can add a fee the estimator hides.",
                    f"{post} or FedEx may add handling on collect parcels. Read the live SKU.",
                ]),
                ("How long it takes", [
                    "Transit days change with the SKU. This page does not invent USPS business days.",
                    "Warehouse processing is separate from international transit.",
                ]),
                ("Shipping costs", [
                    f"International freight plus whatever the SKU says at the border. No dollar is pasted into this title because the live form moves. This desk does not invent a de-minimis dollar.",
                    f"{ccy} is the local currency on this site. Checkout on {OFF}.",
                ]),
                ("CBP and import fees", [
                    f"Read {customs} at {curl} the morning you ship. Informal-entry rules change. Ranked educational URLs on this host stay — they are not a live threshold.",
                    "No declared-value coaching. Pay what the booked SKU and CBP require.",
                ]),
                ("Common shipping risks", [
                    "Canadian postal code in the estimator, booking before QC, skipping a real ZIP.",
                    "Restricted SKUs still cannot ride a US line if the app blocks them at submit.",
                ]),
                ("First-time US buyers", [
                    f"Treat {host} as a map and {OFF} as checkout. Address test: {city}. Source: {customs}.",
                    "Start with one clothing SKU, accept QC, then book.",
                ]),
                ("Ready to ship?", [
                    f"QC first, then {EST} toward the United States. Orders only on {OFF}.",
                ]),
            ],
        )
    if kind == "legal":
        return (
            f"{A} is a purchasing agent. {host} explains the US path; it is not {customs}. Read CBP the morning you ship.",
            [
                ("Is OrientDig legal in the United States?", [
                    f"Using a purchasing agent is not itself a crime. Restricted goods, platform rules and the booked SKU still apply. Read {curl}.",
                    "Legal here means the agent model. It does not mean every Taobao SKU is allowed through CBP.",
                ]),
                ("Is OrientDig safe to use?", [
                    f"Safe means warehouse QC before freight, payment in the official app, and a real US ZIP — not a promise the parcel skips {customs}.",
                    f"{ccy} on this desk, destination US. {host} never holds the wallet.",
                ]),
                ("Main risks for US buyers", [
                    f"Dead links, collect without reading the SKU, treating {host} as checkout. {post} can add fees.",
                    "A second risk is a Canadian postal code because the UI looks similar. Wrong country. This desk does not invent a de-minimis dollar.",
                ]),
                ("How to reduce risk", [
                    "QC in-app, estimator destination United States, US ZIP on the label. No under-declaration.",
                    "Keep spreadsheet, finds and QC together.",
                ]),
                ("First-time US buyers", [
                    f"Start on {host}, then the official register. This site does not see your account.",
                    "Skip restricted categories on the first order.",
                ]),
                ("Verdict", [
                    f"{A} can be used toward the United States if you follow the official app and {customs}. Independent information only. Orders on {OFF}.",
                ]),
                ("Ready?", [
                    f"Spreadsheet → finds → QC → shipping to the USA. Pay on {OFF}.",
                ]),
            ],
        )
    if kind == "guide":
        return (
            f"A step-by-step {A} path for a US address on {host}. Photos in the warehouse, then freight. Not checkout.",
            [
                ("How to buy from OrientDig (US guide)", [
                    "Pick a QC’d SKU, submit it in the official app, wait for warehouse photos, then book freight toward the United States with a US ZIP on the label.",
                    f"Do not skip QC. {post} will not retake a warehouse photo.",
                ]),
                ("What is OrientDig?", [
                    f"A China purchasing agent. {host} explains the US path in {ccy}. Payment stays on {OFF}.",
                    "Two payments: goods to the warehouse, then international freight after QC.",
                ]),
                ("Step 1 — pick a find", [
                    "Use spreadsheet and finds. English keys still feed the catalogue. Local slang often returns zero — English index, not an empty shop.",
                    "Skip restricted and price-0 cards.",
                ]),
                ("Step 2 — warehouse QC", [
                    "Accept or reject in China. Extra angles are often paid.",
                    f"After {post} has the carton, {customs} will not open a warehouse ticket.",
                ]),
                ("Step 3 — book US freight", [
                    f"Open {EST} with destination United States. Last-mile is often {post}. {city}.",
                    "This page does not invent USPS days or a CBP dollar.",
                ]),
                ("Step 4 — pay on the official site", [
                    f"Register on {OFF}. {host} never stores a card.",
                    "If the SPA still prints unexpected digits after you pick USD, trust the estimator.",
                ]),
                ("Beginner mistakes", [
                    "Canada in the estimator, booking before QC, treating this hostname as a shop.",
                    "De-minimis headlines on forums are not this lab. Read CBP the morning you ship.",
                ]),
                ("Ready?", [
                    f"Spreadsheet → finds → QC → shipping. Then {OFF}.",
                ]),
            ],
        )
    return (
        f"{A} spreadsheet FAQ for US buyers on {host}: index, QC, {post}, {customs}. Not checkout.",
        [
            ("Does this site sell the goods?", [
                f"No. Orders stay on {OFF}. {host} lists finds for US buyers.",
                "Cards are an index, not stock.",
            ]),
            ("What is the OrientDig spreadsheet?", [
                "A shortlist of warehouse-checked SKUs for a US ZIP. Not Excel.",
                "Keywords: OrientDig spreadsheet, orientdig spreadsheet usa, orientdig sheet.",
            ]),
            ("How do I use QC photos?", [
                "They land in-app while the piece is in China.",
                f"{post} will not retake a warehouse photo.",
            ]),
            ("How does shipping to the USA work?", [
                f"Estimator destination US. Last-mile often {post}. Live quote: {EST}.",
                f"{city}. No invented transit days.",
            ]),
            ("Who pays import charges?", [
                f"The booked SKU. Collect can add a fee. Source: {curl}. This desk does not invent a de-minimis dollar.",
                "No declared-value coaching.",
            ]),
            ("Why USD here?", [
                f"Display conversion of the China card. Checkout is whatever {OFF} shows that morning.",
            ]),
            ("Can I use a Canadian postal code?", [
                "No. That is the wrong country for this site.",
            ]),
            ("Where do I register?", [
                f"Only on {OFF}. {host} does not take cards.",
            ]),
        ],
    )


def _at(kind, host, d):
    post, city, customs, curl, ccy = d["post"], d["city"], d["customs"], d["customs_url"], d["ccy"]
    if kind == "spreadsheet":
        return (
            f"Ein kuratiertes {A}-Spreadsheet für Käufer in Österreich auf {host}: geprüfte Seller, QC-Fotos und Finds in einem Index. Kein Excel, keine Kasse. Bestellen auf {OFF} in {ccy}, Ziel Österreich.",
            [
                ("Was ist ein OrientDig-Spreadsheet?", [
                    f"Auf {host} ist das Spreadsheet eine Shortlist lagergeprüfter SKUs für eine österreichische Adresse — Sneaker, Hoodies, Jacken, Taschen, die in der offiziellen App noch öffnen. Es kassiert nicht und ist kein zweites OrientDig-Schaufenster.",
                    "Zeilen bleiben nur nützlich, solange der Quelllink lebt und mindestens ein Lagerfoto existiert. Preis 0 oder Restricted ist eine tote Quelle, kein Rabatt. Keywords: OrientDig spreadsheet, orientdig spreadsheet osterreich, orientdig trusted sellers.",
                ]),
                ("Warum österreichische Käufer mit einem Sheet starten", [
                    f"Taobao/Weidian von Hand mischt abgelaufene Karten. Das Sheet hält Finds, die du im QC schon akzeptiert hast, bevor {post} einen Karton nach {city} bewegt.",
                    "Österreichische Käufer vermeiden eine deutsche fünfstellige PLZ im Schätzer. Diese Seite ist AT, EUR, BMF Zoll — nicht DHL DE und nicht Packstation.",
                ]),
                ("So funktioniert das Spreadsheet", [
                    f"Find auf {host} öffnen, Lagerfotos in der {A}-App lesen, dann internationale Linie mit Ziel Österreich buchen. Warenkorb bleibt auf {OFF}.",
                    f"Englische Katalogschlüssel (sneakers, hoodie, jacket) sind Anzeige. Sie ändern das Schätzerland nicht. Live-Geld: {EST}.",
                ]),
                ("Welche Produkte stehen drauf?", [
                    "Schuhe, Hoodies, Jacken, Taschen, weil dort QC-Winkel existieren. Elektronik, Parfum, Flüssiges bleibt draußen, bis die App sie am Versandmorgen erlaubt.",
                    "Ein Find von letztem Monat kann Restricted werden. Vor der Fracht die offizielle Produktseite neu lesen.",
                ]),
                ("Ist ein Spreadsheet sicherer?", [
                    f"Sicherer heißt Lagerfotos vor der Fracht — nicht, dass {customs} verschwindet. {curl} am Versandmorgen lesen. IOSS und Collect ändern sich; diese Seite klebt keinen Satz in den Title.",
                    f"Das Sheet hält dich von toten Weidian-Links weg. Es gibt keine Zollanmeldung ab und erfindet keinen Deklarationswert. Adresstest: {city}.",
                ]),
                ("Wer soll es nutzen?", [
                    f"Erstbesteller mit österreichischer Tür und alle, die {A} schon nutzen, aber Spreadsheet, Finds, QC und Versand-AT auf einem AT-Host in {ccy} wollen.",
                    "Wer nach Deutschland schickt, ist auf der falschen Country-Seite.",
                ]),
                ("Typische Fehler ohne Sheet", [
                    f"Deutsche PLZ im Schätzer, {host} als Kasse, Fracht vor QC. Letzte Meile oft {post}; Collect kann Gebühren addieren, die der Schätzer verbirgt.",
                    "Ein rankender Zollartikel auf diesem Host ist kein Live-Tarif. Schwellen bewegen sich. App und BMF Zoll am Versandtag.",
                ]),
                ("Sheet effizient nutzen", [
                    f"Spreadsheet, Finds und QC in einem Tab-Satz. Nach akzeptiertem QC den offiziellen Schätzer nach Österreich öffnen. Quelle: {customs}.",
                    f"Keine Unterdeklaration. Zahlen, was SKU und {EST} zeigen. Bestellung auf {OFF}.",
                ]),
                ("Muss man das Spreadsheet nutzen?", [
                    "Nein. Du kannst die App von Hand durchsuchen. Das Sheet spart österreichischen Käufern tote Karten.",
                    f"Registrieren und zahlen auf {OFF}. {host} sieht das Konto nicht.",
                ]),
                ("Bereit?", [
                    f"Finds, QC und Versand nach Österreich, dann {OFF}. Index in {ccy}.",
                ]),
            ],
        )
    if kind == "finds":
        return (
            f"Top {A}-Finds für Österreich auf {host}: QC-geprüfte Sneaker, Hoodies und Taschen für eine AT-Adresse, kein zweiter Weltkatalog.",
            [
                ("Was sind OrientDig-Finds?", [
                    f"Finds auf {host} sind SKUs nach Lagerfotos. Sie sind nicht von einer DE-Liste mit Ortsnamen-Tausch kopiert.",
                    "Preis 0 ist eine entfernte Karte, kein Sale.",
                ]),
                ("Warum kuratierte Finds", [
                    f"Sie werden in China fotografiert, bevor {post} Richtung {city} fährt.",
                    f"{ccy}, Ziel AT, vierstellige PLZ schlagen Forum-Screenshots ohne BMF-Pfad.",
                ]),
                ("Kategorien", [
                    "Sneaker und Hoodies haben noch QC-Winkel. Restricted bleibt draußen.",
                    "Englische Keys sind Anzeige, kein DE-Import.",
                ]),
                ("Auswahl", [
                    f"Lebender Quelllink, mindestens ein Lagerfoto, Schätzer-Ziel Österreich. Adresstest: {city}.",
                    "Fail-QC verlässt die Liste.",
                ]),
                ("Sicherer als Handsuche?", [
                    f"{customs} ({curl}) am Versandmorgen lesen. Ein Find heißt nur: Fotos in China vor der Fracht.",
                    "Sicherer ist nicht zollfrei. Collect kann gelten.",
                ]),
                ("Für wen?", [
                    "Nur österreichische Türen. Erste Bestellung: einfache Kleidung mit Fotos.",
                    "Packstation-Labels gehören nach Deutschland, nicht hierher.",
                ]),
                ("Weiter", [
                    f"QC, dann Versand nach Österreich. Zahlen auf {OFF}.",
                ]),
            ],
        )
    if kind == "qc":
        return (
            f"QC auf {host} sind Lagerfotos in der offiziellen {A}-App in China, bevor du Fracht nach Österreich zahlst.",
            [
                ("Was QC hier ist", [
                    "Zusätzliche Lagerwinkel — Nähte, Etikett, Sohle, Print. Kein Labor, kein BMF-Röntgen.",
                    "Fotos kommen in der App, solange die SKU in China ist.",
                ]),
                ("Wann Extra-Fotos", [
                    f"Solange die SKU im Lager ist. Wenn {post} den Karton hat, ist {customs} die falsche Stelle für eine Nachaufnahme.",
                    "Extra-Winkel sind oft kostenpflichtig. Dieses HTML öffnet keine Tickets.",
                ]),
                ("Was QC nicht tut", [
                    f"Keine Zollanmeldung, kein erfundener Deklarationswert. Quelle: {curl}.",
                    "Ein sauberes Album ist kein späterer Plattform-Pass. Vor dem Buchen neu prüfen.",
                ]),
                ("QC und AT-Adresse", [
                    f"Ziel Österreich, {city}. Eine deutsche fünfstellige PLZ ist das falsche Land.",
                    "Fotos entstehen in China. Der AT-Teil ist die Tür nach akzeptiertem QC.",
                ]),
                ("Wenn QC scheitert", [
                    "In der App retournieren. Keine internationale Fracht auf ein Reject.",
                    f"Fail-QC ist in China billiger als nach Zustellversuch durch {post}.",
                ]),
                ("Danach versenden?", [
                    f"Dann {EST} Richtung Österreich. {host} kassiert nicht.",
                ]),
            ],
        )
    if kind == "shipping":
        return (
            f"{A}-Versand nach Österreich nutzt den Schätzer-Code AT, nicht diese Domain. Live-Formular nach Lagerfotos. Letzte Meile oft {post}.",
            [
                ("Ablauf", [
                    f"China-Lager → QC akzeptieren → Linie mit Ziel Österreich → {post}. {host} druckt kein Live-Quote.",
                    f"Das Label braucht {city}. Ziel AT in {EST} am Versandmorgen.",
                ]),
                ("Optionen", [
                    "Tax-free, prepaid, Empfänger stehen auf der SKU. Collect kann Gebühren addieren, die der Schätzer verbirgt.",
                    f"{post} kann bei Collect extra kassieren. Live-SKU lesen.",
                ]),
                ("Dauer", [
                    "Transittage ändern sich mit der SKU. Diese Seite erfindet keine Post-AT-Werktage.",
                    "Lagerbearbeitung ist nicht internationaler Transit.",
                ]),
                ("Kosten", [
                    f"Internationale Fracht plus das, was die SKU an der Grenze sagt. Kein Eurobetrag im Title, weil das Live-Formular wandert.",
                    f"{ccy} ist Anzeige. Kasse auf {OFF}.",
                ]),
                ("Zoll", [
                    f"{customs} unter {curl} am Versandmorgen. IOSS ändert sich. Rankende Zoll-URLs auf diesem Host bleiben — kein Live-Tarif.",
                    "Keine Unterdeklaration. Zahlen, was SKU und BMF verlangen.",
                ]),
                ("Risiken", [
                    f"Deutsche PLZ im Schätzer, Fracht vor QC, Packstation statt {city}.",
                    "Restricted-SKUs fahren keine AT-Linie, wenn die App sie beim Submit blockt.",
                ]),
                ("Erstbesteller", [
                    f"{host} als Karte, {OFF} als Kasse. Adresstest: {city}. Quelle: {customs}.",
                    "Eine Kleidungs-SKU, QC, dann buchen.",
                ]),
                ("Bereit?", [
                    f"Zuerst QC, dann {EST} nach Österreich. Nur {OFF}.",
                ]),
            ],
        )
    if kind == "legal":
        return (
            f"{A} ist Einkaufsagent. {host} erklärt den AT-Weg, ist nicht {customs}. BMF Zoll am Versandmorgen lesen.",
            [
                ("Ist OrientDig in Österreich legal?", [
                    f"Ein Einkaufsagent ist in Österreich kein Straftatbestand. Restricted, Plattformregeln und die SKU gelten weiter. {curl} lesen.",
                    "Legal heißt das Agent-Modell. Nicht jede Taobao-SKU darf durch BMF Zoll.",
                ]),
                ("Ist OrientDig sicher?", [
                    f"Sicher heißt QC vor Fracht, Zahlung in der App, echte AT-Adresse — kein Versprechen, dass das Paket {customs} umgeht.",
                    f"{ccy}, Ziel AT, {city}. {host} hält keine Geldbörse.",
                ]),
                ("Risiken", [
                    f"Tote Links, Collect ohne SKU-Lesen, {host} als Kasse. {post} kann Gebühren addieren.",
                    "Zweite Falle: deutsche PLZ, weil die UI ähnlich aussieht. Falsches Land. Keine Packstation.",
                ]),
                ("Risiko senken", [
                    f"QC in der App, Schätzer-Ziel Österreich, {city} auf dem Label. Keine Unterdeklaration.",
                    "Spreadsheet, Finds und QC zusammenhalten.",
                ]),
                ("Erstbesteller", [
                    f"Auf {host} starten, dann offiziell registrieren. Diese Site sieht das Konto nicht.",
                    "Restricted in der ersten Bestellung weglassen.",
                ]),
                ("Fazit", [
                    f"{A} ist nach Österreich nutzbar, wenn du App und {customs} folgst. Unabhängige Information. Bestellung auf {OFF}.",
                ]),
                ("Start", [
                    f"Spreadsheet → Finds → QC → Versand AT. Zahlen auf {OFF}.",
                ]),
            ],
        )
    if kind == "guide":
        return (
            f"Schrittfolge {A} für eine österreichische Adresse auf {host}. Fotos im Lager, dann Fracht. Keine Kasse.",
            [
                ("So kaufst du (AT)", [
                    f"QC-SKU finden, in der App einreichen, Lagerfotos abwarten, Fracht nach Österreich mit {city} auf dem Label buchen.",
                    f"QC nicht überspringen. {post} macht keine Nachaufnahme.",
                ]),
                ("Was ist OrientDig?", [
                    f"China-Einkaufsagent. {host} erklärt den AT-Weg in {ccy}. Zahlung auf {OFF}.",
                    "Zwei Zahlungen: Ware ins Lager, danach internationale Fracht nach QC.",
                ]),
                ("Schritt 1 — Find", [
                    "Spreadsheet und Finds. Englische Keys füttern den Katalog. Deutsche Suchworte oft 0 — englischer Index, kein leerer Shop.",
                    "Restricted und Preis 0 weglassen.",
                ]),
                ("Schritt 2 — QC", [
                    "In China akzeptieren oder ablehnen. Extra-Winkel oft kostenpflichtig.",
                    f"Hat {post} den Karton, öffnet {customs} kein Lagerticket.",
                ]),
                ("Schritt 3 — Fracht AT", [
                    f"{EST} mit Ziel Österreich. Letzte Meile oft {post}. {city}.",
                    "Keine erfundenen Post-Tage, kein BMF-Satz.",
                ]),
                ("Schritt 4 — zahlen", [
                    f"Registrieren auf {OFF}. {host} speichert keine Karte.",
                    "Wenn die SPA nach EUR weiter USD-Ziffern druckt, den Schätzer glauben.",
                ]),
                ("Anfängerfehler", [
                    "DE im Schätzer, Fracht vor QC, Host als Shop.",
                    "Packstation ist DE, nicht AT.",
                ]),
                ("Start", [
                    f"Spreadsheet → Finds → QC → Versand. Dann {OFF}.",
                ]),
            ],
        )
    return (
        f"{A} Spreadsheet-FAQ für Österreich auf {host}: Index, QC, {post}, {customs}. Keine Kasse.",
        [
            ("Verkauft diese Site die Ware?", [
                f"Nein. Bestellung auf {OFF}. {host} zeigt Finds für Österreich.",
                "Karten sind ein Index, kein Lager.",
            ]),
            ("Was ist das Spreadsheet?", [
                f"Shortlist lagergeprüfter SKUs für {city}. Kein Excel.",
                "Keywords: OrientDig spreadsheet, orientdig spreadsheet osterreich, orientdig sheet.",
            ]),
            ("Wie nutze ich QC?", [
                "Fotos in der App, solange das Stück in China ist.",
                f"{post} macht keine Nachaufnahme.",
            ]),
            ("Wie geht Versand nach Österreich?", [
                f"Schätzer-Ziel AT. Letzte Meile oft {post}. Quote: {EST}.",
                f"{city}. Keine erfundenen Transittage.",
            ]),
            ("Wer zahlt Abgaben?", [
                f"Die SKU. Collect kann extra kosten. Quelle: {curl}. Keine Unterdeklaration.",
            ]),
            ("Warum EUR hier?", [
                f"Anzeigeumrechnung der China-Karte. Kasse ist, was {OFF} am Morgen zeigt.",
            ]),
            ("Darf ich eine deutsche PLZ nutzen?", [
                "Nein. Falsches Land. Keine Packstation.",
            ]),
            ("Wo registrieren?", [
                f"Nur {OFF}. {host} nimmt keine Karten.",
            ]),
        ],
    )
def _de(kind, host, d):
    post, city, customs, curl, ccy = d["post"], d["city"], d["customs"], d["customs_url"], d["ccy"]
    if kind == "spreadsheet":
        return (
            f"Ein kuratiertes {A}-Spreadsheet für Käufer in Deutschland auf {host}: geprüfte Seller, QC-Fotos und Finds. Kein Excel, keine Kasse. Bestellen auf {OFF} in {ccy}, Ziel Deutschland.",
            [
                ("Was ist ein OrientDig-Spreadsheet?", [
                    f"Auf {host} ist das Spreadsheet eine Shortlist lagergeprüfter SKUs für eine deutsche Adresse — Sneaker, Hoodies, Jacken, Taschen. Es kassiert nicht.",
                    "Preis 0 oder Restricted ist tot, kein Rabatt. Keywords: OrientDig spreadsheet, orientdig spreadsheet deutschland, orientdig trusted sellers.",
                ]),
                ("Warum deutsche Käufer mit einem Sheet starten", [
                    f"Handsuche mischt tote Weidian-Karten. Das Sheet hält QC-akzeptierte Finds, bevor {post} Richtung {city} fährt.",
                    "Deutsche Käufer vermeiden eine österreichische vierstellige PLZ. Diese Seite ist DE, EUR, zoll.de — Packstation möglich, nicht Post AT, nicht 1010 Wien.",
                ]),
                ("So funktioniert es", [
                    f"Find öffnen, Lagerfotos in der {A}-App, Linie mit Ziel Deutschland. Warenkorb auf {OFF}.",
                    f"Englische Keys ändern das Schätzerland nicht. Live-Geld: {EST}.",
                ]),
                ("Welche Produkte?", [
                    "Schuhe, Hoodies, Jacken, Taschen mit QC-Winkeln. Restricted bleibt draußen, bis die App es am Versandmorgen erlaubt.",
                    "Vor der Fracht die Produktseite neu prüfen.",
                ]),
                ("Sicherer?", [
                    f"Lagerfotos vor der Fracht — {customs} bleibt. {curl} am Versandmorgen. Kein Satz im Title.",
                    f"Kein Deklarationswert auf dieser Seite. Adresstest: {city}.",
                ]),
                ("Für wen?", [
                    f"Erstbesteller mit deutscher Tür und alle, die Spreadsheet/Finds/QC/Versand-DE auf einem DE-Host in {ccy} wollen.",
                    "AT-Labels gehören nach Österreich.",
                ]),
                ("Fehler ohne Sheet", [
                    f"1010 Wien im Schätzer, {host} als Kasse, Fracht vor QC. {post} kann Collect-Gebühren addieren.",
                    "Ein rankender Zollartikel ist kein Live-Tarif.",
                ]),
                ("Effizient nutzen", [
                    f"Nach QC {EST} nach Deutschland. Quelle: {customs}.",
                    f"Keine Unterdeklaration. Zahlen auf {OFF}.",
                ]),
                ("Pflicht?", [
                    "Nein. Die App geht auch ohne Sheet. Das Sheet spart tote Karten.",
                    f"{host} sieht das Konto nicht.",
                ]),
                ("Bereit?", [
                    f"Finds, QC, Versand DE, dann {OFF}.",
                ]),
            ],
        )
    if kind == "finds":
        return (
            f"Top {A}-Finds für Deutschland auf {host}: QC-geprüfte Ware für eine DE-Adresse, kein zweiter Weltkatalog.",
            [
                ("Was sind Finds?", [
                    f"SKUs nach Lagerfotos auf {host}. Nicht von einer AT-Liste kopiert.",
                    "Preis 0 ist entfernt, kein Sale.",
                ]),
                ("Warum kuratiert", [
                    f"Fotos in China, bevor {post} Richtung Packstation oder Straße fährt.",
                    f"{ccy}, Ziel DE, fünfstellige PLZ. Kein 1010 Wien.",
                ]),
                ("Kategorien", [
                    "Sneaker und Hoodies haben QC-Winkel. Restricted bleibt draußen.",
                    "Englische Keys sind Anzeige.",
                ]),
                ("Auswahl", [
                    f"Quelllink, Lagerfoto, Schätzer-Ziel Deutschland. {city}.",
                    "Fail-QC raus.",
                ]),
                ("Sicherer?", [
                    f"{customs} ({curl}) am Versandmorgen. Find = Fotos vor Fracht, nicht zollfrei.",
                ]),
                ("Für wen?", [
                    "Nur deutsche Türen. Erste Bestellung: Kleidung mit Fotos.",
                    "Österreichische Post-Labels nicht hier.",
                ]),
                ("Weiter", [
                    f"QC, dann Versand DE. {OFF}.",
                ]),
            ],
        )
    if kind == "qc":
        return (
            f"QC auf {host}: Lagerfotos in der {A}-App in China, bevor du Fracht nach Deutschland zahlst.",
            [
                ("Was QC ist", [
                    "Lagerwinkel, kein Zoll-Röntgen, kein Markengericht.",
                    "Fotos in der App, solange die SKU in China ist.",
                ]),
                ("Extra-Fotos", [
                    f"Nur im Lager. Hat {post} den Karton, ist {customs} die falsche Stelle.",
                    "Oft kostenpflichtig. HTML öffnet keine Tickets.",
                ]),
                ("Was QC nicht tut", [
                    f"Keine Zollanmeldung, kein Deklarationswert. {curl}.",
                    "Sauberes Album ≠ späterer Plattform-Pass.",
                ]),
                ("QC und DE-Adresse", [
                    f"Ziel Deutschland, {city}. 1010 Wien ist das falsche Land.",
                    "Fotos in China. DE-Teil ist die Tür nach QC.",
                ]),
                ("Fail-QC", [
                    "In der App retournieren, nicht international buchen.",
                    f"In China billiger als nach {post}.",
                ]),
                ("Danach?", [
                    f"{EST} nach Deutschland. {host} kassiert nicht.",
                ]),
            ],
        )
    if kind == "shipping":
        return (
            f"{A}-Versand nach Deutschland: Schätzer-Code DE, nicht diese Domain. Live-Formular nach QC. Letzte Meile oft {post}.",
            [
                ("Ablauf", [
                    f"Lager → QC → Linie Ziel Deutschland → {post}. Kein Live-Quote auf {host}.",
                    f"Label: {city}. Ziel DE in {EST} am Versandmorgen.",
                ]),
                ("Optionen", [
                    "Tax-free / prepaid / Empfänger auf der SKU. Collect kann extra kosten.",
                    "DHL kann Zollgebühren kassieren, die der Schätzer nicht zeigt.",
                ]),
                ("Dauer", [
                    "Keine erfundenen DHL-Werktage. SKU am Versandmorgen.",
                    "Lager ≠ Transit.",
                ]),
                ("Kosten", [
                    f"Fracht plus Grenze laut SKU. Kein Euro im Title. {ccy} nur Anzeige. Kasse {OFF}.",
                ]),
                ("Zoll", [
                    f"{customs} {curl} am Versandmorgen. Rankende URLs bleiben, kein Live-Tarif.",
                    "Keine Unterdeklaration.",
                ]),
                ("Risiken", [
                    "AT-PLZ, Fracht vor QC, 1010 Wien statt Packstation/Straße.",
                    "Restricted blockt die DE-Linie beim Submit.",
                ]),
                ("Erstbesteller", [
                    f"{host} Karte, {OFF} Kasse. {city}. Quelle {customs}.",
                    "Eine Kleidungs-SKU, QC, buchen.",
                ]),
                ("Bereit?", [
                    f"QC, dann {EST} nach DE. Nur {OFF}.",
                ]),
            ],
        )
    if kind == "legal":
        return (
            f"{A} ist Einkaufsagent. {host} erklärt DE, ist nicht {customs}. zoll.de am Versandmorgen.",
            [
                ("Legal in Deutschland?", [
                    f"Agent-Modell ist kein Straftatbestand. Restricted und SKU gelten. {curl}.",
                    "Nicht jede Taobao-SKU darf durch den Zoll.",
                ]),
                ("Sicher?", [
                    f"QC vor Fracht, Zahlung in der App, echte DE-Adresse — kein Umgehen von {customs}.",
                    f"{ccy}, Ziel DE, {city}. {host} hält keine Karte.",
                ]),
                ("Risiken", [
                    f"Tote Links, Collect ohne SKU, {host} als Kasse. {post} kann extra kassieren.",
                    "AT-PLZ ist das falsche Land.",
                ]),
                ("Risiko senken", [
                    f"QC, Schätzer DE, {city}. Keine Unterdeklaration.",
                    "Spreadsheet/Finds/QC zusammen.",
                ]),
                ("Erstbesteller", [
                    f"{host} dann Register auf {OFF}. Restricted weglassen.",
                ]),
                ("Fazit", [
                    f"Nutzbar nach Deutschland mit App und {customs}. Info only. {OFF}.",
                ]),
                ("Start", [
                    "Spreadsheet → Finds → QC → Versand DE.",
                ]),
            ],
        )
    if kind == "guide":
        return (
            f"Schrittfolge {A} für eine deutsche Adresse auf {host}. Lagerfotos, dann Fracht.",
            [
                ("So kaufen (DE)", [
                    f"QC-SKU, App, Lagerfotos, Fracht nach Deutschland mit {city}.",
                    f"QC nicht skippen. {post} macht keine Nachaufnahme.",
                ]),
                ("Was ist OrientDig?", [
                    f"Einkaufsagent. {host} erklärt DE in {ccy}. Zahlung {OFF}.",
                    "Zwei Zahlungen: Ware, dann Fracht nach QC.",
                ]),
                ("Schritt 1", [
                    "Spreadsheet/Finds, englische Keys. Deutsche Wörter oft 0 Karten.",
                    "Restricted und Preis 0 weg.",
                ]),
                ("Schritt 2", [
                    "QC in China. Extra-Winkel oft paid.",
                    f"{customs} öffnet kein Lagerticket nach {post}.",
                ]),
                ("Schritt 3", [
                    f"{EST} Ziel Deutschland. Oft {post}. {city}.",
                    "Keine erfundenen DHL-Tage.",
                ]),
                ("Schritt 4", [
                    f"Zahlen auf {OFF}. {host} speichert keine Karte.",
                ]),
                ("Fehler", [
                    "AT im Schätzer, Fracht vor QC, Host als Shop.",
                    "1010 Wien ist nicht DE.",
                ]),
                ("Start", [
                    f"Spreadsheet → Finds → QC → Versand. {OFF}.",
                ]),
            ],
        )
    return (
        f"{A} Spreadsheet-FAQ Deutschland auf {host}: Index, QC, {post}, {customs}.",
        [
            ("Verkauft die Site Ware?", [
                f"Nein. Bestellung auf {OFF}. {host} zeigt Finds für Deutschland.",
            ]),
            ("Was ist das Spreadsheet?", [
                f"Shortlist für {city}. Kein Excel. Keywords: orientdig spreadsheet deutschland.",
            ]),
            ("QC?", [
                "Fotos in der App in China.",
                f"{post} keine Nachaufnahme.",
            ]),
            ("Versand DE?", [
                f"Schätzer DE, oft {post}, {EST}. Keine erfundenen Tage.",
            ]),
            ("Abgaben?", [
                f"SKU. Collect extra. {curl}. Keine Unterdeklaration.",
            ]),
            ("EUR hier?", [
                f"Anzeige. Kasse ist {OFF}.",
            ]),
            ("AT-PLZ?", [
                "Nein. Falsches Land.",
            ]),
            ("Register?", [
                f"Nur {OFF}.",
            ]),
        ],
    )


def _es(kind, host, d):
    post, city, customs, curl, ccy = d["post"], d["city"], d["customs"], d["customs_url"], d["ccy"]
    if kind == "spreadsheet":
        return (
            f"Un spreadsheet {A} para compradores en España en {host}: sellers con QC, finds en un índice. No es Excel ni caja. Pedidos en {OFF} en {ccy} con destino España.",
            [
                ("Qué es un spreadsheet OrientDig", [
                    f"En {host} es una shortlist de SKU fotografiados en almacén para una dirección española. No cobra y no es un segundo escaparate.",
                    "Precio 0 o restricted es fuente muerta. Keywords: OrientDig spreadsheet, orientdig spreadsheet espana, orientdig trusted sellers.",
                ]),
                ("Por qué España empieza por una hoja", [
                    f"La búsqueda manual mezcla Weidian muertos. La hoja guarda finds ya aceptados en QC antes de que {post} mueva el cartón hacia {city}.",
                    "Los compradores en España evitan un code postal francés. Esta página es ES, EUR, Agencia Tributaria — no copiamos un recuento de líneas de otro agente.",
                ]),
                ("Cómo funciona", [
                    f"Abre un find, lee QC en la app {A}, reserva línea con destino España. El carrito sigue en {OFF}.",
                    f"Las claves inglesas no cambian el país del estimador. Dinero vivo: {EST}.",
                ]),
                ("Qué productos", [
                    "Zapatillas, sudaderas, chaquetas, bolsos con ángulos QC. Restricted fuera hasta que la app lo permita el día del envío.",
                    "Un find de hace un mes puede cerrarse. Relee la ficha oficial antes del flete.",
                ]),
                ("¿Es más seguro?", [
                    f"Más seguro = fotos de almacén antes del flete, no que {customs} desaparezca. {curl} el día del envío. Sin valor declarado en el title.",
                    f"No presenta un DUA. Prueba de dirección: {city}.",
                ]),
                ("Para quién", [
                    f"Primera compra a España y quien ya usa {A} pero quiere spreadsheet/finds/QC/envío ES en un host español en {ccy}.",
                    "Si el paquete va a Francia, esta no es tu página. Hosts hermanos son archivos distintos — sin 301.",
                ]),
                ("Errores sin hoja", [
                    f"CAP italiano en el estimador, tratar {host} como caja, flete antes de QC. {post} puede añadir tasa Collect.",
                    "Un artículo de aduana rankeado no es un arancel en vivo.",
                ]),
                ("Uso eficiente", [
                    f"Tras QC, {EST} hacia España. Fuente: {customs}.",
                    f"Sin infradeclaración. Pago en {OFF}.",
                ]),
                ("¿Es obligatorio?", [
                    "No. La app se busca a mano. La hoja evita fichas muertas.",
                    f"{host} no ve la cuenta.",
                ]),
                ("Listo", [
                    f"Finds, QC, envío a España, luego {OFF}.",
                ]),
            ],
        )
    if kind == "finds":
        return (
            f"Mejores finds {A} para España en {host}: QC en almacén para una dirección ES, no un segundo catálogo mundial.",
            [
                ("Qué son", [
                    f"SKU con fotos de almacén en {host}. No copiados de una lista FR con el nombre del país cambiado.",
                    "Precio 0 es ficha retirada.",
                ]),
                ("Por qué curados", [
                    f"Se fotografían en China antes de que {post} salga hacia {city}.",
                    f"{ccy}, destino ES, CP de cinco dígitos. No copiamos un recuento de líneas.",
                ]),
                ("Categorías", [
                    "Sneakers y hoodies aún tienen QC. Restricted fuera.",
                    "Claves inglesas son etiqueta.",
                ]),
                ("Selección", [
                    f"URL viva, foto de almacén, estimador España. {city}.",
                    "QC fallido sale de la lista.",
                ]),
                ("¿Más seguro?", [
                    f"Lee {customs} ({curl}) el día del envío. Find = fotos antes del flete, no libre de aranceles.",
                ]),
                ("Para quién", [
                    "Solo puertas en España. Primera orden: ropa con fotos.",
                    "Un code postal francés no es este desk.",
                ]),
                ("Siguiente", [
                    f"QC, luego envío a España. {OFF}.",
                ]),
            ],
        )
    if kind == "qc":
        return (
            f"QC en {host}: fotos de almacén en la app {A} en China, antes de pagar el flete a España.",
            [
                ("Qué es QC", [
                    "Ángulos de almacén, no un escáner de Agencia Tributaria.",
                    "Las fotos llegan a la app mientras la SKU sigue en China.",
                ]),
                ("Fotos extra", [
                    f"Mientras esté en almacén. Si {post} ya tiene el cartón, {customs} no rehace el QC.",
                    "Ángulos extra suelen pagarse. Este HTML no abre tickets.",
                ]),
                ("Qué no hace", [
                    f"No presenta un DUA ni inventa un valor declarado. {curl}.",
                    "Álbum limpio ≠ pase posterior de plataforma.",
                ]),
                ("QC y dirección ES", [
                    f"Destino España, {city}. Un CAP italiano es el país equivocado.",
                    "Fotos en China. La parte ES es la puerta tras aceptar QC.",
                ]),
                ("Si falla", [
                    "Devuelve en la app. No reserves flete internacional.",
                    f"Más barato en China que tras {post}.",
                ]),
                ("¿Enviar?", [
                    f"Luego {EST} hacia España. {host} no cobra.",
                ]),
            ],
        )
    if kind == "shipping":
        return (
            f"El envío {A} a España usa el código ES del estimador, no este dominio. Formulario vivo tras QC. Última milla a menudo {post}.",
            [
                ("Cómo funciona", [
                    f"Almacén → QC → línea destino España → {post}. {host} no imprime un quote vivo.",
                    f"La etiqueta necesita {city}. Destino ES en {EST} el día del envío.",
                ]),
                ("Opciones", [
                    "Tax-free / prepaid / destinatario lo dice la SKU. Collect puede añadir tasa que el estimador oculta.",
                    f"{post} puede añadir despacho en Collect.",
                ]),
                ("Plazos", [
                    "Los días cambian con la SKU. Esta página no inventa plazos de Correos.",
                    "Almacén ≠ tránsito internacional.",
                ]),
                ("Coste", [
                    f"Flete más frontera según SKU. Sin importe en el title. {ccy} es visualización. Caja {OFF}.",
                ]),
                ("Aduana", [
                    f"{customs} {curl} el día del envío. URLs rankeadas se conservan; no son arancel vivo.",
                    "Sin infradeclaración. No copiamos un recuento de líneas.",
                ]),
                ("Riesgos", [
                    "Code postal francés, flete antes de QC, CAP italiano.",
                    "Restricted no sube a una línea ES si la app lo bloquea.",
                ]),
                ("Primera compra", [
                    f"{host} es mapa, {OFF} es caja. {city}. Fuente {customs}.",
                    "Una SKU de ropa, QC, reservar.",
                ]),
                ("Listo", [
                    f"QC, luego {EST} a España. Solo {OFF}.",
                ]),
            ],
        )
    if kind == "legal":
        return (
            f"{A} es agente de compras. {host} explica el camino ES; no es {customs}. Lee AEAT el día del envío.",
            [
                ("¿Es legal en España?", [
                    f"Usar un agente no es delito. Restricted y la SKU siguen. {curl}.",
                    "Legal = modelo de agente. No cada SKU de Taobao pasa Agencia Tributaria.",
                ]),
                ("¿Es seguro?", [
                    f"Seguro = QC antes del flete, pago en la app, dirección ES real — no saltarse {customs}.",
                    f"{ccy}, destino ES, {city}. {host} no guarda tarjeta.",
                ]),
                ("Riesgos", [
                    f"Enlaces muertos, Collect sin leer SKU, tratar {host} como caja. {post} puede añadir tasa.",
                    "Un code postal francés es el país equivocado.",
                ]),
                ("Reducir riesgo", [
                    f"QC, estimador España, {city}. Sin infradeclaración.",
                    "Spreadsheet, finds y QC juntos.",
                ]),
                ("Primera compra", [
                    f"Empieza en {host}, registro en {OFF}. Restricted fuera.",
                ]),
                ("Veredicto", [
                    f"Se puede usar hacia España siguiendo app y {customs}. Información independiente. {OFF}.",
                ]),
                ("Empezar", [
                    "Spreadsheet → finds → QC → envío ES.",
                ]),
            ],
        )
    if kind == "guide":
        return (
            f"Guía {A} paso a paso para una dirección en España en {host}. Fotos de almacén, luego flete.",
            [
                ("Cómo comprar (ES)", [
                    f"SKU con QC, app, fotos, flete a España con {city}.",
                    f"No saltes QC. {post} no rehace la foto.",
                ]),
                ("Qué es OrientDig", [
                    f"Agente. {host} explica ES en {ccy}. Pago {OFF}.",
                    "Dos pagos: mercancía, luego flete tras QC.",
                ]),
                ("Paso 1", [
                    "Spreadsheet/finds, claves inglesas. Palabras en español suelen dar cero.",
                    "Restricted y precio 0 fuera.",
                ]),
                ("Paso 2", [
                    "QC en China. Ángulos extra a menudo de pago.",
                    f"{customs} no abre ticket de almacén tras {post}.",
                ]),
                ("Paso 3", [
                    f"{EST} destino España. A menudo {post}. {city}.",
                    "Sin plazos inventados de Correos.",
                ]),
                ("Paso 4", [
                    f"Paga en {OFF}. {host} no guarda tarjeta.",
                ]),
                ("Errores", [
                    "FR en el estimador, flete antes de QC, host como tienda.",
                    "No copiamos un recuento de líneas.",
                ]),
                ("Listo", [
                    f"Spreadsheet → finds → QC → envío. {OFF}.",
                ]),
            ],
        )
    return (
        f"FAQ spreadsheet {A} para España en {host}: índice, QC, {post}, {customs}.",
        [
            ("¿Esta web vende?", [
                f"No. Pedidos en {OFF}. {host} muestra finds para España.",
            ]),
            ("Qué es el spreadsheet", [
                f"Shortlist para {city}. No Excel. Keywords: orientdig spreadsheet espana.",
            ]),
            ("QC", [
                "Fotos en la app en China.",
                f"{post} no rehace la foto.",
            ]),
            ("Envío a España", [
                f"Estimador ES, a menudo {post}, {EST}. Sin plazos inventados.",
            ]),
            ("Aranceles", [
                f"La SKU. Collect extra. {curl}. Sin infradeclaración.",
            ]),
            ("EUR aquí", [
                f"Visualización. Caja {OFF}.",
            ]),
            ("¿Code postal francés?", [
                "No. País equivocado.",
            ]),
            ("Registro", [
                f"Solo {OFF}.",
            ]),
        ],
    )


def _fr(kind, host, d):
    post, city, customs, curl, ccy = d["post"], d["city"], d["customs"], d["customs_url"], d["ccy"]
    if kind == "spreadsheet":
        return (
            f"Un spreadsheet {A} pour acheteurs en France sur {host} : sellers QC, finds dans un index. Pas Excel, pas une caisse. Commandes sur {OFF} en {ccy}, destination France.",
            [
                ("Qu’est-ce qu’un spreadsheet OrientDig ?", [
                    f"Sur {host}, une shortlist de SKU photographiés en entrepôt pour une adresse française. Ça n’encaisse pas.",
                    "Prix 0 ou restricted = source morte. Keywords: OrientDig spreadsheet, orientdig spreadsheet france, orientdig trusted sellers.",
                ]),
                ("Pourquoi une feuille pour la France", [
                    f"La recherche manuelle mélange des Weidian morts. La feuille garde les finds déjà acceptés en QC avant que {post} parte vers {city}.",
                    "Les acheteurs FR évitent un code postal belge à quatre chiffres. Cette page est FR, EUR, douane.gouv.fr — pas BE.",
                ]),
                ("Comment ça marche", [
                    f"Ouvre un find, lis le QC dans l’app {A}, réserve une ligne destination France. Panier sur {OFF}.",
                    f"Les clés anglaises ne changent pas le pays de l’estimateur. Argent live : {EST}.",
                ]),
                ("Quels produits", [
                    "Baskets, hoodies, vestes, sacs avec angles QC. Restricted dehors tant que l’app ne l’autorise pas le matin de l’envoi.",
                    "Un find d’il y a un mois peut passer restricted. Relis la fiche officielle avant le fret.",
                ]),
                ("Plus sûr ?", [
                    f"Plus sûr = photos d’entrepôt avant le fret, pas la disparition de {customs}. {curl} le matin de l’envoi. Pas de valeur déclarée dans le title.",
                    f"Ce HTML ne dépose pas une DAU. Test d’adresse : {city}.",
                ]),
                ("Pour qui", [
                    f"Première commande France et ceux qui veulent spreadsheet/finds/QC/livraison FR sur un hôte français en {ccy}.",
                    "Un colis Belgique n’est pas cette page. Hôtes sœurs = fichiers séparés, pas de 301.",
                ]),
                ("Erreurs sans feuille", [
                    f"Code belge, traiter {host} comme caisse, fret avant QC. {post} peut ajouter des frais Collect.",
                    "Un article douane classé n’est pas un tarif live.",
                ]),
                ("Usage efficace", [
                    f"Après QC, {EST} vers la France. Source : {customs}.",
                    f"Pas de sous-déclaration. Paiement sur {OFF}.",
                ]),
                ("Obligatoire ?", [
                    "Non. L’app se cherche à la main. La feuille évite les cartes mortes.",
                    f"{host} ne voit pas le compte.",
                ]),
                ("Prêt", [
                    f"Finds, QC, livraison France, puis {OFF}.",
                ]),
            ],
        )
    if kind == "finds":
        return (
            f"Meilleurs finds {A} pour la France sur {host} : QC entrepôt pour une adresse FR, pas un second catalogue mondial.",
            [
                ("C’est quoi", [
                    f"SKU avec photos d’entrepôt sur {host}. Pas copiés d’une liste ES avec le nom du pays changé.",
                    "Prix 0 = fiche retirée.",
                ]),
                ("Pourquoi curatés", [
                    f"Photos en Chine avant que {post} parte vers {city}.",
                    f"{ccy}, destination FR, CP à cinq chiffres, pas un code belge.",
                ]),
                ("Catégories", [
                    "Sneakers et hoodies ont encore du QC. Restricted dehors.",
                    "Clés anglaises = étiquette.",
                ]),
                ("Sélection", [
                    f"URL vivante, photo, estimateur France. {city}.",
                    "QC refusé = hors liste.",
                ]),
                ("Plus sûr ?", [
                    f"Lis {customs} ({curl}) le matin de l’envoi. Find = photos avant fret, pas hors droits.",
                ]),
                ("Pour qui", [
                    "Portes françaises seulement. Première commande : vêtements avec photos.",
                    "Un código español n’est pas ce desk.",
                ]),
                ("Suite", [
                    f"QC, puis livraison France. {OFF}.",
                ]),
            ],
        )
    if kind == "qc":
        return (
            f"Le QC sur {host} : photos d’entrepôt dans l’app {A} en Chine, avant de payer le fret vers la France.",
            [
                ("C’est quoi", [
                    "Angles d’entrepôt, pas un scanner douane.gouv.fr.",
                    "Les photos arrivent dans l’app tant que la SKU est en Chine.",
                ]),
                ("Photos extra", [
                    f"Tant que c’est en entrepôt. Si {post} a le carton, {customs} ne refait pas le QC.",
                    "Angles extra souvent payants. Cet HTML n’ouvre pas de ticket.",
                ]),
                ("Ce que le QC ne fait pas", [
                    f"Pas de DAU, pas de valeur déclarée inventée. {curl}.",
                    "Album propre ≠ passe plateforme plus tard.",
                ]),
                ("QC et adresse FR", [
                    f"Destination France, {city}. Un code belge est le mauvais pays.",
                    "Photos en Chine. La partie FR est la porte après QC.",
                ]),
                ("Si ça échoue", [
                    "Retour in-app. Pas de fret international sur un reject.",
                    f"Moins cher en Chine qu’après {post}.",
                ]),
                ("Envoyer ?", [
                    f"Ensuite {EST} vers la France. {host} n’encaisse pas.",
                ]),
            ],
        )
    if kind == "shipping":
        return (
            f"La livraison {A} vers la France utilise le code FR de l’estimateur, pas ce domaine. Formulaire live après QC. Dernier km souvent {post}.",
            [
                ("Parcours", [
                    f"Entrepôt → QC → ligne destination France → {post}. {host} n’imprime pas un quote live.",
                    f"L’étiquette veut {city}. Destination FR dans {EST} le matin de l’envoi.",
                ]),
                ("Options", [
                    "Tax-free / prepaid / destinataire = SKU. Collect peut ajouter des frais cachés par l’estimateur.",
                    f"{post} peut ajouter un dédouanement Collect.",
                ]),
                ("Délais", [
                    "Les jours bougent avec la SKU. Cette page n’invente pas des jours Colissimo.",
                    "Entrepôt ≠ transit international.",
                ]),
                ("Coût", [
                    f"Fret plus frontière selon SKU. Pas de montant dans le title. {ccy} = affichage. Caisse {OFF}.",
                ]),
                ("Douane", [
                    f"{customs} {curl} le matin de l’envoi. URLs classées conservées ; pas un tarif live.",
                    "Pas de sous-déclaration. Pas un code postal belge.",
                ]),
                ("Risques", [
                    "Code belge, fret avant QC, código español.",
                    "Restricted ne prend pas une ligne FR si l’app bloque au submit.",
                ]),
                ("Première commande", [
                    f"{host} = carte, {OFF} = caisse. {city}. Source {customs}.",
                    "Une SKU vêtement, QC, réserver.",
                ]),
                ("Prêt", [
                    f"QC, puis {EST} vers la France. Seulement {OFF}.",
                ]),
            ],
        )
    if kind == "legal":
        return (
            f"{A} est agent d’achat. {host} explique le chemin FR ; ce n’est pas {customs}. Lis douane.gouv.fr le matin de l’envoi.",
            [
                ("Est-ce légal en France ?", [
                    f"Utiliser un agent n’est pas un délit. Restricted et la SKU restent. {curl}.",
                    "Légal = modèle d’agent. Pas chaque SKU Taobao passe la douane FR.",
                ]),
                ("Est-ce sûr ?", [
                    f"Sûr = QC avant fret, paiement in-app, adresse FR réelle — pas éviter {customs}.",
                    f"{ccy}, destination FR, {city}. {host} ne garde pas de carte.",
                ]),
                ("Risques", [
                    f"Liens morts, Collect sans lire la SKU, traiter {host} comme caisse. {post} peut ajouter des frais.",
                    "Un code belge est le mauvais pays.",
                ]),
                ("Réduire le risque", [
                    f"QC, estimateur France, {city}. Pas de sous-déclaration.",
                    "Spreadsheet, finds et QC ensemble.",
                ]),
                ("Première commande", [
                    f"Démarre sur {host}, registre sur {OFF}. Restricted dehors.",
                ]),
                ("Verdict", [
                    f"Utilisable vers la France en suivant l’app et {customs}. Info indépendante. {OFF}.",
                ]),
                ("Commencer", [
                    "Spreadsheet → finds → QC → livraison FR.",
                ]),
            ],
        )
    if kind == "guide":
        return (
            f"Guide {A} pas à pas pour une adresse en France sur {host}. Photos d’entrepôt, puis fret.",
            [
                ("Comment acheter (FR)", [
                    f"SKU QC, app, photos, fret vers la France avec {city}.",
                    f"Ne saute pas le QC. {post} ne refait pas la photo.",
                ]),
                ("C’est quoi OrientDig", [
                    f"Agent. {host} explique FR en {ccy}. Paiement {OFF}.",
                    "Deux paiements : marchandise, puis fret après QC.",
                ]),
                ("Étape 1", [
                    "Spreadsheet/finds, clés anglaises. Mots français souvent zéro carte.",
                    "Restricted et prix 0 dehors.",
                ]),
                ("Étape 2", [
                    "QC en Chine. Angles extra souvent payants.",
                    f"{customs} n’ouvre pas de ticket entrepôt après {post}.",
                ]),
                ("Étape 3", [
                    f"{EST} destination France. Souvent {post}. {city}.",
                    "Pas de jours Colissimo inventés.",
                ]),
                ("Étape 4", [
                    f"Paie sur {OFF}. {host} ne stocke pas de carte.",
                ]),
                ("Erreurs", [
                    "BE dans l’estimateur, fret avant QC, hôte comme boutique.",
                    "Pas un code postal belge.",
                ]),
                ("Prêt", [
                    f"Spreadsheet → finds → QC → livraison. {OFF}.",
                ]),
            ],
        )
    return (
        f"FAQ spreadsheet {A} France sur {host} : index, QC, {post}, {customs}.",
        [
            ("Ce site vend-il ?", [
                f"Non. Commandes sur {OFF}. {host} liste les finds pour la France.",
            ]),
            ("Spreadsheet ?", [
                f"Shortlist pour {city}. Pas Excel. Keywords: orientdig spreadsheet france.",
            ]),
            ("QC", [
                "Photos in-app en Chine.",
                f"{post} ne refait pas la photo.",
            ]),
            ("Livraison France", [
                f"Estimateur FR, souvent {post}, {EST}. Pas de délais inventés.",
            ]),
            ("Droits", [
                f"La SKU. Collect extra. {curl}. Pas de sous-déclaration.",
            ]),
            ("EUR ici", [
                f"Affichage. Caisse {OFF}.",
            ]),
            ("Code belge ?", [
                "Non. Mauvais pays.",
            ]),
            ("Inscription", [
                f"Seulement {OFF}.",
            ]),
        ],
    )


def _it(kind, host, d):
    post, city, customs, curl, ccy = d["post"], d["city"], d["customs"], d["customs_url"], d["ccy"]
    if kind == "spreadsheet":
        return (
            f"Uno spreadsheet {A} per acquirenti in Italia su {host}: seller con QC e finds in un indice. Non è Excel, non è cassa. Ordini su {OFF} in {ccy}, destinazione Italia.",
            [
                ("Cos’è uno spreadsheet OrientDig", [
                    f"Su {host} è una shortlist di SKU fotografati in magazzino per un indirizzo italiano. Non incassa.",
                    "Prezzo 0 o restricted è fonte morta. Keywords: OrientDig spreadsheet, orientdig spreadsheet italia, orientdig trusted sellers.",
                ]),
                ("Perché l’Italia parte da un foglio", [
                    f"La ricerca a mano mescola Weidian morti. Il foglio tiene i finds già accettati in QC prima che {post} muova il cartone verso {city}.",
                    "Gli acquirenti IT evitano un código español. Questa pagina è IT, EUR, ADM — non Correos.",
                ]),
                ("Come funziona", [
                    f"Apri un find, leggi il QC nell’app {A}, prenota una linea destinazione Italia. Carrello su {OFF}.",
                    f"Le chiavi inglesi non cambiano il paese dell’estimator. Soldi live: {EST}.",
                ]),
                ("Quali prodotti", [
                    "Sneaker, felpe, giacche, borse con angoli QC. Restricted fuori finché l’app non lo consente il mattino della spedizione.",
                    "Un find del mese scorso può chiudersi. Rileggi la scheda ufficiale prima del nolo.",
                ]),
                ("Più sicuro?", [
                    f"Più sicuro = foto di magazzino prima del nolo, non che {customs} sparisca. {curl} il giorno della spedizione. Nessun valore dichiarato nel title.",
                    f"Questo HTML non presenta una bolla doganale. Test indirizzo: {city}.",
                ]),
                ("Per chi", [
                    f"Prima ordine Italia e chi vuole spreadsheet/finds/QC/spedizione IT su un host italiano in {ccy}.",
                    "Un pacco ES non è questa pagina. Host gemelli = file separati, niente 301.",
                ]),
                ("Errori senza foglio", [
                    f"Code postal FR, trattare {host} come cassa, nolo prima del QC. {post} può aggiungere un fee Collect.",
                    "Un articolo dogana in ranking non è un tariffario live.",
                ]),
                ("Uso efficiente", [
                    f"Dopo QC, {EST} verso l’Italia. Fonte: {customs}.",
                    f"Niente sottofatturazione. Pagamento su {OFF}.",
                ]),
                ("Obbligatorio?", [
                    "No. L’app si cerca a mano. Il foglio evita schede morte.",
                    f"{host} non vede l’account.",
                ]),
                ("Pronto", [
                    f"Finds, QC, spedizione Italia, poi {OFF}.",
                ]),
            ],
        )
    if kind == "finds":
        return (
            f"Migliori finds {A} per l’Italia su {host}: QC magazzino per un indirizzo IT, non un secondo catalogo globale.",
            [
                ("Cosa sono", [
                    f"SKU con foto di magazzino su {host}. Non copiati da una lista NL con il nome del paese cambiato.",
                    "Prezzo 0 = scheda tolta.",
                ]),
                ("Perché curati", [
                    f"Foto in Cina prima che {post} parta verso {city}.",
                    f"{ccy}, destinazione IT, CAP a cinque cifre. Non Correos.",
                ]),
                ("Categorie", [
                    "Sneaker e felpe hanno ancora QC. Restricted fuori.",
                    "Chiavi inglesi = etichetta.",
                ]),
                ("Selezione", [
                    f"URL viva, foto, estimator Italia. {city}.",
                    "QC fallito esce.",
                ]),
                ("Più sicuro?", [
                    f"Leggi {customs} ({curl}) il giorno della spedizione. Find = foto prima del nolo, non duty-free.",
                ]),
                ("Per chi", [
                    "Solo porte italiane. Primo ordine: abbigliamento con foto.",
                    "Un code postal francese non è questo desk.",
                ]),
                ("Avanti", [
                    f"QC, poi spedizione Italia. {OFF}.",
                ]),
            ],
        )
    if kind == "qc":
        return (
            f"QC su {host}: foto di magazzino nell’app {A} in Cina, prima di pagare il nolo verso l’Italia.",
            [
                ("Cos’è", [
                    "Angoli di magazzino, non uno scanner ADM.",
                    "Le foto arrivano in-app mentre la SKU è in Cina.",
                ]),
                ("Foto extra", [
                    f"Finché è in magazzino. Se {post} ha il cartone, {customs} non rifà il QC.",
                    "Angoli extra spesso a pagamento. Questo HTML non apre ticket.",
                ]),
                ("Cosa non fa", [
                    f"Niente bolla, niente valore dichiarato inventato. {curl}.",
                    "Album pulito ≠ pass piattaforma dopo.",
                ]),
                ("QC e indirizzo IT", [
                    f"Destinazione Italia, {city}. Un código español è il paese sbagliato.",
                    "Foto in Cina. La parte IT è la porta dopo il QC.",
                ]),
                ("Se fallisce", [
                    "Reso in-app. Niente nolo internazionale su un reject.",
                    f"Più economico in Cina che dopo {post}.",
                ]),
                ("Spedire?", [
                    f"Poi {EST} verso l’Italia. {host} non incassa.",
                ]),
            ],
        )
    if kind == "shipping":
        return (
            f"La spedizione {A} in Italia usa il codice IT dell’estimator, non questo dominio. Form live dopo QC. Ultimo miglio spesso {post}.",
            [
                ("Percorso", [
                    f"Magazzino → QC → linea destinazione Italia → {post}. {host} non stampa un quote live.",
                    f"L’etichetta vuole {city}. Destinazione IT in {EST} il mattino della spedizione.",
                ]),
                ("Opzioni", [
                    "Tax-free / prepaid / destinatario = SKU. Collect può aggiungere fee nascosti dall’estimator.",
                    f"{post} può aggiungere sdoganamento Collect.",
                ]),
                ("Tempi", [
                    "I giorni cambiano con la SKU. Questa pagina non inventa giorni Poste.",
                    "Magazzino ≠ transito internazionale.",
                ]),
                ("Costo", [
                    f"Nolo più frontiera secondo SKU. Nessun importo nel title. {ccy} = display. Cassa {OFF}.",
                ]),
                ("Dogana", [
                    f"{customs} {curl} il giorno della spedizione. URL in ranking restano; non sono tariffario live.",
                    "Niente sottofatturazione. Destinazione IT, non Correos.",
                ]),
                ("Rischi", [
                    "Code postal FR, nolo prima del QC, Packstation.",
                    "Restricted non sale su una linea IT se l’app blocca al submit.",
                ]),
                ("Primo ordine", [
                    f"{host} mappa, {OFF} cassa. {city}. Fonte {customs}.",
                    "Una SKU abbigliamento, QC, prenota.",
                ]),
                ("Pronto", [
                    f"QC, poi {EST} verso l’Italia. Solo {OFF}.",
                ]),
            ],
        )
    if kind == "legal":
        return (
            f"{A} è agente d’acquisto. {host} spiega il percorso IT; non è {customs}. Leggi ADM il giorno della spedizione.",
            [
                ("È legale in Italia?", [
                    f"Usare un agente non è un reato. Restricted e SKU restano. {curl}.",
                    "Legale = modello agente. Non ogni SKU Taobao passa ADM.",
                ]),
                ("È sicuro?", [
                    f"Sicuro = QC prima del nolo, pagamento in-app, indirizzo IT reale — non saltare {customs}.",
                    f"{ccy}, destinazione IT, {city}. {host} non tiene carte.",
                ]),
                ("Rischi", [
                    f"Link morti, Collect senza leggere la SKU, trattare {host} come cassa. {post} può aggiungere fee.",
                    "Un code postal francese è il paese sbagliato.",
                ]),
                ("Ridurre il rischio", [
                    f"QC, estimator Italia, {city}. Niente sottofatturazione.",
                    "Spreadsheet, finds e QC insieme.",
                ]),
                ("Primo ordine", [
                    f"Parti da {host}, registro su {OFF}. Restricted fuori.",
                ]),
                ("Verdetto", [
                    f"Usabile verso l’Italia seguendo app e {customs}. Info indipendente. {OFF}.",
                ]),
                ("Inizia", [
                    "Spreadsheet → finds → QC → spedizione IT.",
                ]),
            ],
        )
    if kind == "guide":
        return (
            f"Guida {A} passo passo per un indirizzo in Italia su {host}. Foto di magazzino, poi nolo.",
            [
                ("Come comprare (IT)", [
                    f"SKU con QC, app, foto, nolo verso l’Italia con {city}.",
                    f"Non saltare il QC. {post} non rifà la foto.",
                ]),
                ("Cos’è OrientDig", [
                    f"Agente. {host} spiega IT in {ccy}. Pagamento {OFF}.",
                    "Due pagamenti: merce, poi nolo dopo QC.",
                ]),
                ("Passo 1", [
                    "Spreadsheet/finds, chiavi inglesi. Parole italiane spesso zero schede.",
                    "Restricted e prezzo 0 fuori.",
                ]),
                ("Passo 2", [
                    "QC in Cina. Angoli extra spesso a pagamento.",
                    f"{customs} non apre ticket magazzino dopo {post}.",
                ]),
                ("Passo 3", [
                    f"{EST} destinazione Italia. Spesso {post}. {city}.",
                    "Niente giorni Poste inventati.",
                ]),
                ("Passo 4", [
                    f"Paga su {OFF}. {host} non salva carte.",
                ]),
                ("Errori", [
                    "ES nell’estimator, nolo prima del QC, host come negozio.",
                    "Non Correos.",
                ]),
                ("Pronto", [
                    f"Spreadsheet → finds → QC → spedizione. {OFF}.",
                ]),
            ],
        )
    return (
        f"FAQ spreadsheet {A} Italia su {host}: indice, QC, {post}, {customs}.",
        [
            ("Questo sito vende?", [
                f"No. Ordini su {OFF}. {host} elenca i finds per l’Italia.",
            ]),
            ("Spreadsheet", [
                f"Shortlist per {city}. Non Excel. Keywords: orientdig spreadsheet italia.",
            ]),
            ("QC", [
                "Foto in-app in Cina.",
                f"{post} non rifà la foto.",
            ]),
            ("Spedizione Italia", [
                f"Estimator IT, spesso {post}, {EST}. Niente tempi inventati.",
            ]),
            ("Dazi", [
                f"La SKU. Collect extra. {curl}. Niente sottofatturazione.",
            ]),
            ("EUR qui", [
                f"Display. Cassa {OFF}.",
            ]),
            ("Code postal FR?", [
                "No. Paese sbagliato.",
            ]),
            ("Registrazione", [
                f"Solo {OFF}.",
            ]),
        ],
    )


def _nl(kind, host, d):
    post, city, customs, curl, ccy = d["post"], d["city"], d["customs"], d["customs_url"], d["ccy"]
    if kind == "spreadsheet":
        return (
            f"Een {A}-spreadsheet voor kopers in Nederland op {host}: QC-checked sellers en finds in één index. Geen Excel, geen kassa. Bestellen op {OFF} in {ccy}, bestemming Nederland.",
            [
                ("Wat is een OrientDig-spreadsheet?", [
                    f"Op {host} is het een shortlist van magazijnfoto-SKU’s voor een Nederlands adres. Het incasseert niet.",
                    "Prijs 0 of restricted is een dode bron. Keywords: OrientDig spreadsheet, orientdig spreadsheet nederland, orientdig trusted sellers.",
                ]),
                ("Waarom NL met een sheet begint", [
                    f"Handzoeken mengt dode Weidian-kaarten. Het sheet houdt finds die je in QC al accepteerde voordat {post} richting {city} rijdt.",
                    "Nederlandse kopers vermijden een Duits Packstation-nummer. Deze pagina is NL, EUR, Douane — Nederlandse postcode 1234 AB, geen DE-automaat.",
                ]),
                ("Hoe het werkt", [
                    f"Open een find, lees QC in de {A}-app, boek een lijn met bestemming Nederland. Winkelwagen op {OFF}.",
                    f"Engelse keys veranderen het estimator-land niet. Live geld: {EST}.",
                ]),
                ("Welke producten", [
                    "Sneakers, hoodies, jassen, tassen met QC-hoeken. Restricted blijft eraf tot de app het toestaat op de verzenddag.",
                    "Een find van vorige maand kan restricted worden. Check de officiële fiche voor vracht.",
                ]),
                ("Veiliger?", [
                    f"Veiliger = magazijnfoto’s voor vracht, niet dat {customs} verdwijnt. {curl} op de verzenddag. Geen aangegeven waarde in de title.",
                    f"Deze HTML dient geen aangifte in. Adrescheck: {city}.",
                ]),
                ("Voor wie", [
                    f"Eerste NL-order en wie spreadsheet/finds/QC/verzending NL op een Nederlandse host in {ccy} wil.",
                    "Een Duits label hoort niet op deze pagina. Zus-hosts blijven aparte files — geen 301.",
                ]),
                ("Fouten zonder sheet", [
                    f"Belgische postcode, {host} als kassa, vracht voor QC. {post} kan Collect-fees optellen.",
                    "Een rankende douane-URL is geen live tarief.",
                ]),
                ("Efficiënt", [
                    f"Na QC {EST} naar Nederland. Bron: {customs}.",
                    f"Geen onderwaardering. Betalen op {OFF}.",
                ]),
                ("Verplicht?", [
                    "Nee. De app zoek je met de hand. Het sheet spaart dode kaarten.",
                    f"{host} ziet het account niet.",
                ]),
                ("Klaar", [
                    f"Finds, QC, verzending NL, daarna {OFF}.",
                ]),
            ],
        )
    if kind == "finds":
        return (
            f"Beste {A}-finds voor Nederland op {host}: QC-magazijn voor een NL-adres, geen tweede wereldcatalogus.",
            [
                ("Wat zijn finds", [
                    f"SKU’s met magazijnfoto’s op {host}. Niet gekopieerd van een DE-lijst met landnaam-wissel.",
                    "Prijs 0 is verwijderd, geen sale.",
                ]),
                ("Waarom gecureerd", [
                    f"Foto’s in China voordat {post} richting {city} gaat.",
                    f"{ccy}, bestemming NL, postcode 1234 AB. Geen Packstation.",
                ]),
                ("Categorieën", [
                    "Sneakers en hoodies hebben nog QC. Restricted eraf.",
                    "Engelse keys zijn labels.",
                ]),
                ("Selectie", [
                    f"Levende URL, foto, estimator Nederland. {city}.",
                    "Fail-QC eraf.",
                ]),
                ("Veiliger?", [
                    f"Lees {customs} ({curl}) op de verzenddag. Find = foto’s voor vracht, niet duty-free.",
                ]),
                ("Voor wie", [
                    "Alleen Nederlandse deuren. Eerste order: kleding met foto’s.",
                    "Een Duitse automaat is dit desk niet.",
                ]),
                ("Verder", [
                    f"QC, daarna verzending NL. {OFF}.",
                ]),
            ],
        )
    if kind == "qc":
        return (
            f"QC op {host}: magazijnfoto’s in de {A}-app in China, vóór je vracht naar Nederland betaalt.",
            [
                ("Wat QC is", [
                    "Magazijnhoeken, geen Douane-scan.",
                    "Foto’s landen in-app zolang de SKU in China is.",
                ]),
                ("Extra foto’s", [
                    f"Zolang het in het magazijn ligt. Heeft {post} de doos, doet {customs} geen heropname.",
                    "Extra hoeken vaak betaald. Deze HTML opent geen tickets.",
                ]),
                ("Wat QC niet doet", [
                    f"Geen aangifte, geen verzonnen aangegeven waarde. {curl}.",
                    "Schoon album ≠ later platform-pass.",
                ]),
                ("QC en NL-adres", [
                    f"Bestemming Nederland, {city}. Packstation is het verkeerde land.",
                    "Foto’s in China. Het NL-deel is de deur na QC.",
                ]),
                ("Als het faalt", [
                    "Retour in-app. Geen internationale vracht op een reject.",
                    f"Goedkoper in China dan na {post}.",
                ]),
                ("Verzenden?", [
                    f"Daarna {EST} naar Nederland. {host} incasseert niet.",
                ]),
            ],
        )
    if kind == "shipping":
        return (
            f"{A}-verzending naar Nederland gebruikt estimator-code NL, niet dit domein. Live formulier na QC. Last-mile vaak {post}.",
            [
                ("Traject", [
                    f"Magazijn → QC → lijn bestemming Nederland → {post}. {host} print geen live quote.",
                    f"Het label wil {city}. Bestemming NL in {EST} op de verzenddag.",
                ]),
                ("Opties", [
                    "Tax-free / prepaid / ontvanger = SKU. Collect kan fees optellen die de estimator verbergt.",
                    f"{post} kan inklaring Collect bijtellen. iDEAL is een NL-rail in de app — bevestig daar.",
                ]),
                ("Duur", [
                    "Dagen wijzigen met de SKU. Deze pagina verzint geen DHL-werkdagen.",
                    "Magazijn ≠ internationaal transit.",
                ]),
                ("Kosten", [
                    f"Vracht plus grens volgens SKU. Geen bedrag in de title. {ccy} is weergave. Kassa {OFF}.",
                ]),
                ("Douane", [
                    f"{customs} {curl} op de verzenddag. Rankende URL’s blijven; geen live tarief.",
                    "Geen onderwaardering. Nederlandse postcode, geen Duits automaat-nummer.",
                ]),
                ("Risico’s", [
                    "Packstation, vracht voor QC, Belgische postcode.",
                    "Restricted rijdt geen NL-lijn als de app blokkeert bij submit.",
                ]),
                ("Eerste order", [
                    f"{host} kaart, {OFF} kassa. {city}. Bron {customs}.",
                    "Eén kleding-SKU, QC, boeken.",
                ]),
                ("Klaar", [
                    f"QC, dan {EST} naar NL. Alleen {OFF}.",
                ]),
            ],
        )
    if kind == "legal":
        return (
            f"{A} is inkoopagent. {host} legt het NL-pad uit; het is niet {customs}. Lees de Douane op de verzenddag.",
            [
                ("Is het legaal in Nederland?", [
                    f"Een agent gebruiken is geen misdrijf. Restricted en SKU blijven. {curl}.",
                    "Legaal = agentmodel. Niet elke Taobao-SKU mag door de Douane.",
                ]),
                ("Is het veilig?", [
                    f"Veilig = QC voor vracht, betalen in-app, echt NL-adres — niet {customs} omzeilen.",
                    f"{ccy}, bestemming NL, {city}. {host} bewaart geen kaart.",
                ]),
                ("Risico’s", [
                    f"Dode links, Collect zonder SKU, {host} als kassa. {post} kan extra innen.",
                    "Packstation is het verkeerde land.",
                ]),
                ("Risico verlagen", [
                    f"QC, estimator Nederland, {city}. Geen onderwaardering.",
                    "Spreadsheet, finds en QC bij elkaar.",
                ]),
                ("Eerste order", [
                    f"Start op {host}, register op {OFF}. Restricted eraf.",
                ]),
                ("Oordeel", [
                    f"Bruikbaar naar Nederland met app en {customs}. Onafhankelijke info. {OFF}.",
                ]),
                ("Start", [
                    "Spreadsheet → finds → QC → verzending NL.",
                ]),
            ],
        )
    if kind == "guide":
        return (
            f"{A}-stappenplan voor een Nederlands adres op {host}. Magazijnfoto’s, daarna vracht.",
            [
                ("Zo kopen (NL)", [
                    f"QC-SKU, app, foto’s, vracht naar Nederland met {city}.",
                    f"Skip QC niet. {post} maakt geen heropname.",
                ]),
                ("Wat is OrientDig", [
                    f"Agent. {host} legt NL uit in {ccy}. Betalen {OFF}.",
                    "Twee betalingen: goederen, daarna vracht na QC.",
                ]),
                ("Stap 1", [
                    "Spreadsheet/finds, Engelse keys. Nederlandse woorden vaak nul kaarten.",
                    "Restricted en prijs 0 eraf.",
                ]),
                ("Stap 2", [
                    "QC in China. Extra hoeken vaak betaald.",
                    f"{customs} opent geen magazijnticket na {post}.",
                ]),
                ("Stap 3", [
                    f"{EST} bestemming Nederland. Vaak {post}. {city}.",
                    "Geen verzonnen DHL-dagen.",
                ]),
                ("Stap 4", [
                    f"Betaal op {OFF}. {host} slaat geen kaart op.",
                ]),
                ("Fouten", [
                    "DE in de estimator, vracht voor QC, host als winkel.",
                    "Geen Packstation.",
                ]),
                ("Klaar", [
                    f"Spreadsheet → finds → QC → verzending. {OFF}.",
                ]),
            ],
        )
    return (
        f"{A} spreadsheet-FAQ Nederland op {host}: index, QC, {post}, {customs}.",
        [
            ("Verkoopt deze site?", [
                f"Nee. Bestellen op {OFF}. {host} toont finds voor Nederland.",
            ]),
            ("Spreadsheet", [
                f"Shortlist voor {city}. Geen Excel. Keywords: orientdig spreadsheet nederland.",
            ]),
            ("QC", [
                "Foto’s in-app in China.",
                f"{post} geen heropname.",
            ]),
            ("Verzending NL", [
                f"Estimator NL, vaak {post}, {EST}. Geen verzonnen dagen.",
            ]),
            ("Invoer", [
                f"De SKU. Collect extra. {curl}. Geen onderwaardering.",
            ]),
            ("EUR hier", [
                f"Weergave. Kassa {OFF}.",
            ]),
            ("Packstation?", [
                "Nee. Verkeerd land.",
            ]),
            ("Registreren", [
                f"Alleen {OFF}.",
            ]),
        ],
    )
