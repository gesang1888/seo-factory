"""Localized inner copy for FansBuy dest desks, UK-cluster depth.

Public pages: no ops notes, no declared-value coaching, no invented transit
days or duty rates. Unique coupons/avis/envio/legit CMS are not rendered here.
Invite codes stay off dest titles.
"""
from __future__ import annotations

A = "FansBuy"
OFF = "fansbuy.com"
EST = "https://fansbuy.com/estimates"


def geo(dest: str) -> str:
    return {
        "NL": "nederland",
        "US": "usa",
        "CA": "canada",
        "GB": "uk",
        "DE": "deutschland",
        "AT": "osterreich",
        "ES": "espana",
        "FR": "france",
        "IT": "italia",
    }.get(dest, dest.lower())


def inner_keywords(kind: str, d: dict) -> list[str]:
    g = geo(d["dest"])
    table = {
        "spreadsheet": [f"{A} spreadsheet", f"fansbuy spreadsheet {g}", "fansbuy trusted sellers"],
        "finds": ["fansbuy finds", "fansbuy spreadsheet finds", "best fansbuy items"],
        "qc": ["fansbuy qc", f"fansbuy qc {g}", "fansbuy warehouse photos"],
        "shipping": ["fansbuy shipping", f"fansbuy shipping {g}", "fansbuy delivery time"],
        "legal": ["fansbuy safe", "fansbuy legit", f"fansbuy safe {g}"],
        "guide": ["fansbuy spreadsheet guide", "how to use fansbuy", "fansbuy buying guide"],
        "faq": ["fansbuy faq", "fansbuy spreadsheet faq", "fansbuy questions"],
    }
    return table[kind]


def inner_serp_title(kind: str, d: dict) -> str:
    key = d["key"]
    table = {
        "spreadsheet": {
            "nl": f"{A} Spreadsheet Nederland – Beste finds en QC",
            "us": f"{A} Spreadsheet USA – Best Sellers, QC & Finds",
            "ca": f"{A} Spreadsheet Canada – Best Sellers, QC & Finds",
            "uk": f"{A} Spreadsheet UK – Best Sellers, QC & Finds",
            "de": f"{A} Spreadsheet Deutschland – Finds und QC",
            "at": f"{A} Spreadsheet Österreich – Finds und QC",
            "es": f"{A} Spreadsheet España – Mejores finds y QC",
            "fr": f"{A} Spreadsheet France – Meilleurs finds et QC",
            "it": f"{A} Spreadsheet Italia – Finds e QC",
        },
        "finds": {
            "nl": f"Beste {A} finds – Nederland 2026",
            "us": f"Top {A} Spreadsheet Finds – Best US Picks 2026",
            "ca": f"Top {A} Spreadsheet Finds – Best Canada Picks 2026",
            "uk": f"Top {A} Spreadsheet Finds – Best UK Picks 2026",
            "de": f"{A} spreadsheet finds – Auswahl Deutschland 2026",
            "at": f"{A} spreadsheet finds – Auswahl Österreich 2026",
            "es": f"Mejores finds {A} – España 2026",
            "fr": f"Meilleurs finds {A} – France 2026",
            "it": f"Migliori finds {A} – Italia 2026",
        },
        "qc": {
            "nl": f"{A} QC-foto’s Nederland – magazijncheck",
            "us": f"{A} QC Photos for US Buyers – Warehouse Check",
            "ca": f"{A} QC Photos for Canada Buyers – Warehouse Check",
            "uk": f"{A} QC Photos for UK Buyers – Warehouse Check",
            "de": f"{A} QC-Fotos nach Deutschland – Lagercheck",
            "at": f"{A} QC-Fotos nach Österreich – Lagercheck",
            "es": f"Fotos QC {A} para España – almacén",
            "fr": f"Photos QC {A} pour la France – entrepôt",
            "it": f"Foto QC {A} per l’Italia – magazzino",
        },
        "shipping": {
            "nl": f"{A} verzending Nederland – kosten, tijd en DHL",
            "us": f"{A} Shipping to the USA – Cost, Time & USPS",
            "ca": f"{A} Shipping to Canada – Cost, Time & Canada Post",
            "uk": f"{A} Shipping to the UK – Cost, Time & Royal Mail",
            "de": f"{A} Versand nach Deutschland – Preis, Zeit und DHL",
            "at": f"{A} Versand nach Österreich – Preis, Zeit und Post",
            "es": f"{A} envío a España – coste, plazo y Correos",
            "fr": f"{A} livraison France – coût, délai et Colissimo",
            "it": f"{A} spedizione Italia – costo, tempi e Poste",
        },
        "legal": {
            "nl": f"Is {A} veilig en legaal in Nederland?",
            "us": f"Is {A} Safe & Legal for US Buyers? Full Guide",
            "ca": f"Is {A} Safe & Legal for Canada Buyers? Full Guide",
            "uk": f"Is {A} Safe & Legal for UK Buyers? Full Guide",
            "de": f"Ist {A} sicher und legal in Deutschland?",
            "at": f"Ist {A} sicher und legal in Österreich?",
            "es": f"¿Es {A} seguro y legal en España?",
            "fr": f"{A} est-il sûr et légal en France ?",
            "it": f"{A} è sicuro e legale in Italia?",
        },
        "guide": {
            "nl": f"{A}-spreadsheet gebruiken – startergids NL",
            "us": f"How to Use {A} Spreadsheet – Beginner Guide USA",
            "ca": f"How to Use {A} Spreadsheet – Beginner Guide Canada",
            "uk": f"How to Use {A} Spreadsheet – Beginner Guide UK",
            "de": f"{A}-Spreadsheet nutzen – Start für Deutschland",
            "at": f"{A}-Spreadsheet nutzen – Start für Österreich",
            "es": f"Cómo usar el spreadsheet {A} – guía España",
            "fr": f"Utiliser le spreadsheet {A} – guide France",
            "it": f"Usare lo spreadsheet {A} – guida Italia",
        },
        "faq": {
            "nl": f"{A} spreadsheet FAQ – gids Nederland 2026",
            "us": f"{A} Spreadsheet FAQ – US Buyers Guide 2026",
            "ca": f"{A} Spreadsheet FAQ – Canada Buyers Guide 2026",
            "uk": f"{A} Spreadsheet FAQ – UK Buyers Guide 2026",
            "de": f"{A} Spreadsheet FAQ – Leitfaden Deutschland",
            "at": f"{A} Spreadsheet FAQ – Leitfaden Österreich",
            "es": f"FAQ spreadsheet {A} – guía España 2026",
            "fr": f"FAQ spreadsheet {A} – guide France 2026",
            "it": f"FAQ spreadsheet {A} – guida Italia 2026",
        },
    }
    return table[kind][key]


def inner_h1(kind: str, d: dict) -> str:
    key = d["key"]
    table = {
        "spreadsheet": {
            "nl": f"{A} Spreadsheet voor kopers in Nederland",
            "us": f"{A} Spreadsheet for US Buyers",
            "ca": f"{A} Spreadsheet for Canadian Buyers",
            "uk": f"{A} Spreadsheet for UK Buyers",
            "de": f"{A} Spreadsheet für Käufer in Deutschland",
            "at": f"{A} Spreadsheet für Käufer in Österreich",
            "es": f"{A} Spreadsheet para compradores en España",
            "fr": f"{A} Spreadsheet pour acheteurs en France",
            "it": f"{A} Spreadsheet per acquirenti in Italia",
        },
        "finds": {
            "nl": f"Beste {A} finds voor Nederland (2026)",
            "us": f"Top {A} Finds for US Buyers (2026 Guide)",
            "ca": f"Top {A} Finds for Canada Buyers (2026 Guide)",
            "uk": f"Top {A} Finds for UK Buyers (2026 Guide)",
            "de": f"{A} Finds für Käufer in Deutschland (2026)",
            "at": f"{A} Finds für Käufer in Österreich (2026)",
            "es": f"Mejores finds {A} para España (2026)",
            "fr": f"Meilleurs finds {A} pour la France (2026)",
            "it": f"Migliori finds {A} per l’Italia (2026)",
        },
        "qc": {
            "nl": f"{A} QC-foto’s vóór verzending naar Nederland",
            "us": f"{A} QC photos before shipping to the United States",
            "ca": f"{A} QC photos before shipping to Canada",
            "uk": f"{A} QC photos before shipping to the United Kingdom",
            "de": f"{A} QC-Fotos vor dem Versand nach Deutschland",
            "at": f"{A} QC-Fotos vor dem Versand nach Österreich",
            "es": f"Fotos QC {A} antes del envío a España",
            "fr": f"Photos QC {A} avant l’envoi vers la France",
            "it": f"Foto QC {A} prima della spedizione in Italia",
        },
        "shipping": {
            "nl": f"{A} verzending naar Nederland",
            "us": f"{A} shipping to the United States",
            "ca": f"{A} shipping to Canada",
            "uk": f"{A} shipping to the United Kingdom",
            "de": f"{A} Versand nach Deutschland",
            "at": f"{A} Versand nach Österreich",
            "es": f"{A} envío a España",
            "fr": f"{A} livraison vers la France",
            "it": f"{A} spedizione in Italia",
        },
        "legal": {
            "nl": f"Is {A} veilig en legaal in Nederland?",
            "us": f"Is {A} safe and legal for US buyers?",
            "ca": f"Is {A} safe and legal for Canada buyers?",
            "uk": f"Is {A} safe and legal for UK buyers?",
            "de": f"Ist {A} sicher und legal in Deutschland?",
            "at": f"Ist {A} sicher und legal in Österreich?",
            "es": f"¿Es {A} seguro y legal en España?",
            "fr": f"{A} est-il sûr et légal en France ?",
            "it": f"{A} è sicuro e legale in Italia?",
        },
        "guide": {
            "nl": f"Kopen via {A}: stappenplan voor Nederland",
            "us": f"How to buy with {A}: US address steps",
            "ca": f"How to buy with {A}: Canada address steps",
            "uk": f"How to buy with {A}: UK address steps",
            "de": f"Kaufen über {A}: Schritte für eine deutsche Adresse",
            "at": f"Kaufen über {A}: Schritte für eine österreichische Adresse",
            "es": f"Comprar con {A}: pasos para una dirección en España",
            "fr": f"Acheter avec {A}: étapes pour une adresse en France",
            "it": f"Comprare con {A}: passi per un indirizzo in Italia",
        },
        "faq": {
            "nl": f"{A} FAQ voor kopers in Nederland (2026)",
            "us": f"{A} FAQ for US Buyers (2026)",
            "ca": f"{A} FAQ for Canada Buyers (2026)",
            "uk": f"{A} FAQ for UK Buyers (2026)",
            "de": f"{A} FAQ für Käufer in Deutschland (2026)",
            "at": f"{A} FAQ für Käufer in Österreich (2026)",
            "es": f"FAQ {A} para compradores en España (2026)",
            "fr": f"FAQ {A} pour acheteurs en France (2026)",
            "it": f"FAQ {A} per acquirenti in Italia (2026)",
        },
    }
    return table[kind][key]


def sections_for(kind: str, d: dict, host: str):
    h1 = inner_h1(kind, d)
    fn = {
        "nl": _nl, "us": _en, "ca": _en, "uk": _en, "de": _de,
        "at": _at, "es": _es, "fr": _fr, "it": _it,
    }[d["key"]]
    lead, secs = fn(kind, host, d)
    if kind != "faq":
        secs = list(secs) + extra_local(d, host) + more_depth(d, host)
    else:
        secs = list(secs) + extra_faq(d, host)
    return h1, lead, secs


def extra_local(d: dict, host: str) -> list:
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
                f"Copy the product URL from the Chinese shop, paste it on {OFF}, and FansBuy buys it into the warehouse. {host} is the spreadsheet and guide for that path toward a UK door.",
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
                f"If the official SPA still prints a dollar symbol after you pick USD, trust the digits in the app and {EST}.",
            ]),
            ("Paste a Taobao, 1688 or Weidian link", [
                f"Paste the Chinese shop URL on {OFF}. FansBuy buys into the warehouse, then you book a line toward a US door after QC.",
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
        "ca": [
            ("How to fill a Canadian delivery address", [
                f"Use a Canadian street and postal code in the A1A 1A1 pattern. A US ZIP is the wrong country. Open {EST} with destination Canada.",
                f"{city} is the format the label needs.",
            ]),
            (f"Prices in {ccy}", [
                f"Finds on this page are shown in {ccy}. Pay on {OFF}. Live freight is the calculator at {EST} with destination Canada.",
                f"If the official screen still prints a US dollar symbol, trust the number in the app and the calculator at {EST}.",
            ]),
            ("Paste a Taobao, 1688 or Weidian link", [
                f"Paste the Chinese shop URL on {OFF}. FansBuy buys into the warehouse, then you book a line toward a Canada Post door after QC.",
                "Shoes, hoodies, jackets and bags dominate because those SKUs still have warehouse photos.",
            ]),
            ("QC photos, then Canada Post", [
                f"Accept warehouse photos in the app, then book freight. Last mile is often {post}.",
                f"Two payments: goods first, freight after QC. Storage days live in official Help on {OFF}.",
            ]),
            ("Import charges", [
                f"Who pays duty and GST/HST on import depends on the booked SKU. Read {curl} ({customs}) the morning you ship. This page does not invent a de-minimis dollar or a declared value.",
            ]),
        ],
        "de": [
            ("Lieferadresse in Deutschland", [
                f"Auf dem Label stehen eine deutsche Straße und eine fünfstellige PLZ. Packstation-Nummern sind ein DE-Muster — {city}. Eine österreichische 1010 Wien oder eine vierstellige AT-PLZ ist das falsche Land.",
                f"Öffne {EST} und setze das Ziel auf Deutschland, bevor du internationale Fracht zahlst.",
            ]),
            (f"Preise in {ccy}", [
                f"Die Karten auf dieser Seite zeigen Finds in {ccy}. Du zahlst auf {OFF}.",
                f"Steht in der offiziellen App noch ein Dollarzeichen, gilt die Zahl in der App und der Rechner {EST} mit Ziel Deutschland.",
            ]),
            ("Taobao-, 1688- oder Weidian-Link einfügen", [
                f"Kopiere die Produkt-URL, füge sie auf {OFF} ein. FansBuy kauft in dein Lager. {host} ist das Spreadsheet für den Weg zu einer deutschen Tür.",
                "Sneaker, Hoodies, Jacken und Taschen stehen meist in der Liste, weil diese SKUs noch QC-Winkel haben.",
            ]),
            ("QC-Fotos, dann DHL", [
                f"Warte auf Lagerfotos in der App. Erst nach akzeptiertem QC buchst du die internationale Linie. Letzte Meile oft {post}. Packstation geht, wenn die SKU sie anbietet — das ist kein AT-Briefkasten.",
                f"Zwei Zahlungen sind normal: Ware nach China, dann Porto. Lagerdauer steht in der Help auf {OFF}.",
            ]),
            ("Abgaben", [
                f"Wer Zoll, Einfuhrumsatzsteuer und Nachnahme zahlt, steht auf der gebuchten SKU. Quelle am Versandmorgen: {curl} ({customs}). Diese Seite nennt keinen Satz und keinen Deklarationsbetrag.",
            ]),
        ],
        "at": [
            ("Lieferadresse in Österreich", [
                f"Auf dem Label stehen eine österreichische Straße und eine vierstellige PLZ — {city}. Eine deutsche Packstation oder eine fünfstellige DE-PLZ ist das falsche Land, auch wenn die App Deutsch anzeigt.",
                f"Öffne {EST} und setze das Ziel auf Österreich, bevor du internationale Fracht zahlst. Nicht „EU“, nicht Deutschland.",
            ]),
            (f"Preise in {ccy}", [
                f"Finds auf dieser Seite in {ccy}. Zahlen auf {OFF}. Live-Fracht: {EST} mit Ziel Österreich.",
                "Steht in der App noch ein Dollarzeichen, gilt die Zahl in der App und der Rechner, nicht diese Seite.",
            ]),
            ("Taobao-, 1688- oder Weidian-Link einfügen", [
                f"Produkt-URL auf {OFF} einfügen. FansBuy kauft ins Lager. {host} ist das Spreadsheet zu einer österreichischen Tür.",
                "Sneaker, Hoodies, Jacken und Taschen haben meist QC-Fotos.",
            ]),
            ("QC-Fotos, dann Österreichische Post", [
                f"Lagerfotos in der App abwarten, dann die internationale Linie buchen. Letzte Meile oft {post}. Das ist keine DHL-Packstation.",
                f"Zwei Zahlungen: Ware nach China, dann Porto. Lagerdauer in der Help auf {OFF}.",
            ]),
            ("Abgaben", [
                f"Wer Zoll und Einfuhrumsatzsteuer zahlt, steht auf der SKU. Quelle: {curl} ({customs}). Kein Deklarationsbetrag auf dieser Seite.",
            ]),
        ],
        "nl": [
            ("Bezorgadres in Nederland", [
                f"Op het label horen een Nederlandse straat en {city}. Een Duits Packstation-nummer of een Belgische postcode is het verkeerde land.",
                f"Kies in {EST} bestemming Nederland vóór je internationale vracht betaalt.",
            ]),
            (f"Prijzen in {ccy}", [
                f"Finds op deze pagina staan in {ccy}. Betalen op {OFF} — kaart, PayPal, saldo of iDEAL, wat het account die ochtend aanbiedt.",
                f"Staat in de SPA nog een dollarteken, dan geldt het bedrag in de app en {EST} met bestemming Nederland.",
            ]),
            ("Plak een Taobao-, 1688- of Weidian-link", [
                f"Plak de product-URL op {OFF}. FansBuy koopt naar het magazijn. {host} is de spreadsheet naar een Nederlandse deur.",
                "Sneakers, hoodies, jassen en tassen hebben meestal QC-foto’s.",
            ]),
            ("QC-foto’s, dan PostNL of DHL", [
                f"Wacht op magazijnfoto’s, daarna de internationale lijn. Last-mile vaak {post}.",
                f"Twee betalingen: goederen naar China, daarna vracht. Magazijndagen in de Help op {OFF}.",
            ]),
            ("Douane", [
                f"Wie invoerrechten en btw bij invoer betaalt, staat op de SKU. Bron: {curl} ({customs}). Deze pagina verzint geen tarief en geen aangegeven waarde.",
            ]),
        ],
        "es": [
            ("Dirección en España", [
                f"En la etiqueta: calle española y código postal de cinco dígitos. Canarias y Ceuta/Melilla suelen ser otro producto de transporte que la península. {city}.",
                f"Abre {EST} con destino España antes de pagar el flete. No uses «EU» ni un código postal francés.",
            ]),
            (f"Precios en {ccy}", [
                f"Los finds de esta página se muestran en {ccy}. Pagas en {OFF}.",
                f"Si la app sigue pintando un símbolo de dólar, fíate de la cifra en la app y de {EST}.",
            ]),
            ("Pega un enlace de Taobao, 1688 o Weidian", [
                f"Pega la URL en {OFF}. FansBuy compra al almacén. {host} es el spreadsheet hacia una puerta en España.",
                "Zapatillas, sudaderas, chaquetas y bolsos suelen tener ángulos QC.",
            ]),
            ("Fotos QC, luego Correos", [
                f"Acepta las fotos de almacén y reserva la línea. Last-mile a menudo {post}.",
                f"Dos pagos: mercancía a China, luego flete. Días de almacén en Help de {OFF}.",
            ]),
            ("Aduanas", [
                f"Quién paga aranceles e IVA de importación lo dice la SKU. Fuente: {curl} ({customs}). Esta página no inventa un valor declarado.",
            ]),
        ],
        "fr": [
            ("Adresse en France", [
                f"Sur l’étiquette: rue française et code postal à cinq chiffres. Un code belge ou un Packstation allemand est le mauvais pays. {city}.",
                f"Ouvre {EST} avec destination France avant de payer le fret. Pas « EU ».",
            ]),
            (f"Prix en {ccy}", [
                f"Les finds de cette page s’affichent en {ccy}. Paiement sur {OFF}.",
                f"Si l’app affiche encore un dollar, fais confiance au chiffre dans l’app et à {EST}.",
            ]),
            ("Colle un lien Taobao, 1688 ou Weidian", [
                f"Colle l’URL sur {OFF}. FansBuy achète vers l’entrepôt. {host} est le spreadsheet vers une porte en France.",
                "Baskets, hoodies, vestes et sacs ont souvent des angles QC.",
            ]),
            ("Photos QC, puis Colissimo", [
                f"Accepte les photos d’entrepôt, puis réserve la ligne. Last-mile souvent {post}.",
                f"Deux paiements: marchandise vers la Chine, puis fret. Jours de stockage dans Help sur {OFF}.",
            ]),
            ("Douane", [
                f"Qui paie droits et TVA à l’import est sur la SKU. Source: {curl} ({customs}). Cette page n’invente pas de valeur déclarée.",
            ]),
        ],
        "it": [
            ("Indirizzo in Italia", [
                f"Sull’etichetta: via italiana e CAP a cinque cifre. Un Packstation tedesco è il paese sbagliato. {city}.",
                f"Apri {EST} con destinazione Italia prima di pagare il nolo. Non «EU».",
            ]),
            (f"Prezzi in {ccy}", [
                f"I finds di questa pagina sono in {ccy}. Paghi su {OFF}.",
                f"Se l’app stampa ancora un dollaro, vale la cifra in-app e {EST}.",
            ]),
            ("Incolla un link Taobao, 1688 o Weidian", [
                f"Incolla l’URL su {OFF}. FansBuy compra verso il magazzino. {host} è lo spreadsheet verso una porta in Italia.",
                "Sneaker, felpe, giacche e borse hanno di solito angoli QC.",
            ]),
            ("Foto QC, poi Poste Italiane", [
                f"Accetta le foto di magazzino, poi prenota la linea. Last-mile spesso {post}.",
                f"Due pagamenti: merce in Cina, poi nolo. Giorni di magazzino nella Help su {OFF}.",
            ]),
            ("Dogana", [
                f"Chi paga dazi e IVA all’import è sulla SKU. Fonte: {curl} ({customs}). Questa pagina non inventa un valore dichiarato.",
            ]),
        ],
    }
    return packs[key]


def extra_faq(d: dict, host: str) -> list:
    post, city, customs, curl, ccy = d["post"], d["city"], d["customs"], d["customs_url"], d["ccy"]
    key = d["key"]
    packs = {
        "uk": [
            ("Does FansBuy sell the goods on this site?", [
                f"No. FansBuy is a purchasing agent. {host} is a spreadsheet for a UK door. Orders, payment and claims stay on {OFF}.",
            ]),
            ("Can I pay on this hostname?", [
                f"No. Register and pay only on {OFF}. Display currency here is {ccy}; the live amount is in the app.",
            ]),
            ("Which estimator country do I pick?", [
                f"United Kingdom — not this TLD, not EU, not Ireland. Open {EST} before you pay freight. {city}.",
            ]),
            ("Does QC happen in the UK?", [
                f"No. Warehouse photos are taken in China. {post} is last-mile after you accept QC.",
            ]),
            ("Who pays import VAT?", [
                f"The booked SKU decides prepaid vs collect. Read {curl} ({customs}) the morning you ship. This page does not invent a declared value.",
            ]),
            ("Is Northern Ireland the same SKU?", [
                f"Often not. Northern Ireland can be another carrier product than mainland {post}. Pick the live line in the app.",
            ]),
            ("Why do local words return zero cards?", [
                "The finds index is English (sneakers, hoodie, jacket). That is not an empty shop.",
            ]),
            ("Where is the invite code?", [
                f"Not in this title. Coupon URLs already on {host} stay as they are.",
            ]),
        ],
        "us": [
            ("Does FansBuy sell the goods on this site?", [
                f"No. FansBuy buys from Chinese shops in your name. Checkout stays on {OFF}.",
            ]),
            ("Can I pay here?", [
                f"No. Pay on {OFF}. This page shows {ccy} as display. Live freight is {EST} with destination United States.",
            ]),
            ("Which estimator country?", [
                f"United States — not this TLD, not Canada. {city}.",
            ]),
            ("Does QC happen at USPS?", [
                f"No. Photos are taken in the China warehouse. {post} or FedEx is last-mile after you accept QC.",
            ]),
            ("Who pays duty?", [
                f"The booked SKU. This page does not invent a de-minimis dollar. Source: {curl} ({customs}).",
            ]),
            ("Is a Canada Post SKU the same?", [
                "No. A Canadian postal code is a different country.",
            ]),
            ("Why do local words return zero cards?", [
                "The finds index is English (sneakers, hoodie, jacket).",
            ]),
            ("Where is the invite code?", [
                f"Not in this title. Existing coupon URLs on {host} stay.",
            ]),
        ],
        "ca": [
            ("Does FansBuy sell the goods on this site?", [
                f"No. FansBuy is the purchasing agent. Pay on {OFF}.",
            ]),
            ("Can I pay here?", [
                f"No. Pay on {OFF}. Display here is {ccy}. Live freight is {EST} with destination Canada.",
            ]),
            ("Which estimator country?", [
                f"Canada — not this TLD, not US. {city}.",
            ]),
            ("Does QC happen at Canada Post?", [
                f"No. Photos are taken in China. {post} is last-mile after you accept QC.",
            ]),
            ("Who pays GST/HST on import?", [
                f"The booked SKU. Read {curl} ({customs}) the morning you ship. This page does not invent a declared value.",
            ]),
            ("Is a USPS SKU the same?", [
                "No. A US ZIP is a different country.",
            ]),
            ("Why do French catalogue words return zero?", [
                "The index keys are English (sneakers, hoodie, jacket).",
            ]),
            ("Where is the invite code?", [
                f"Not in this title. Ranked coupon URLs on {host} stay as they are.",
            ]),
        ],
        "de": [
            ("Verkauft FansBuy die Ware auf dieser Seite?", [
                f"Nein. FansBuy ist Einkaufsagent. Bestellen und zahlen nur auf {OFF}.",
            ]),
            ("Kann ich hier zahlen?", [
                f"Nein. Zahlen auf {OFF}. Anzeige hier in {ccy}. Live-Fracht: {EST} mit Ziel Deutschland.",
            ]),
            ("Welches Schätzer-Land?", [
                f"Deutschland — nicht diese TLD, nicht AT, nicht „EU“. {city}. Packstation ist DE, 1010 Wien ist AT.",
            ]),
            ("Passiert QC bei DHL?", [
                f"Nein. Lagerfotos entstehen in China. {post} ist letzte Meile nach akzeptiertem QC.",
            ]),
            ("Wer zahlt Einfuhrumsatzsteuer?", [
                f"Die gebuchte SKU. Quelle: {curl} ({customs}). Kein Deklarationsbetrag auf dieser Seite.",
            ]),
            ("Ist Österreich dieselbe SKU?", [
                "Nein. Eine vierstellige AT-PLZ ist das falsche Land. Dieses Desk bleibt Deutschland.",
            ]),
            ("Warum findet der Katalog nichts auf Deutsch?", [
                "Der Index ist englisch (sneakers, hoodie, jacket).",
            ]),
            ("Wo steht der Invite-Code?", [
                f"Nicht in diesem Title. Vorhandene Coupon-URLs auf {host} bleiben.",
            ]),
        ],
        "at": [
            ("Verkauft FansBuy die Ware auf dieser Seite?", [
                f"Nein. FansBuy ist Einkaufsagent. Bestellen und zahlen nur auf {OFF}.",
            ]),
            ("Kann ich hier zahlen?", [
                f"Nein. Zahlen auf {OFF}. Anzeige in {ccy}. Live-Fracht: {EST} mit Ziel Österreich.",
            ]),
            ("Welches Schätzer-Land?", [
                f"Österreich — nicht diese TLD, nicht DE, nicht „EU“. {city}. Packstation ist DE.",
            ]),
            ("Passiert QC bei der Post?", [
                f"Nein. Lagerfotos in China. {post} ist letzte Meile nach QC.",
            ]),
            ("Wer zahlt Einfuhrumsatzsteuer?", [
                f"Die gebuchte SKU. Quelle: {curl} ({customs}). Kein Deklarationsbetrag.",
            ]),
            ("Ist Deutschland dieselbe SKU?", [
                "Nein. Eine fünfstellige DE-PLZ oder Packstation ist das falsche Land.",
            ]),
            ("Warum findet der Katalog nichts auf Deutsch?", [
                "Der Index ist englisch (sneakers, hoodie, jacket).",
            ]),
            ("Wo steht der Invite-Code?", [
                f"Nicht in diesem Title. Coupon-URLs auf {host} bleiben.",
            ]),
        ],
        "nl": [
            ("Verkoopt FansBuy de spullen op deze site?", [
                f"Nee. FansBuy is inkoopagent. Bestellen en betalen alleen op {OFF}.",
            ]),
            ("Kan ik hier betalen?", [
                f"Nee. Betalen op {OFF}. Weergave hier in {ccy}. Live vracht: {EST} met bestemming Nederland.",
            ]),
            ("Welk estimator-land?", [
                f"Nederland — niet deze TLD, niet BE, niet EU. {city}.",
            ]),
            ("Gebeurt QC bij PostNL?", [
                f"Nee. Magazijnfoto’s komen uit China. {post} is last-mile na QC.",
            ]),
            ("Wie betaalt invoer?", [
                f"De geboekte SKU. Bron: {curl} ({customs}). Deze pagina verzint geen aangegeven waarde.",
            ]),
            ("Is België dezelfde SKU?", [
                "Nee. Een Belgische postcode is het verkeerde land.",
            ]),
            ("Waarom vindt de catalogus niets in het Nederlands?", [
                "De index is Engels (sneakers, hoodie, jacket).",
            ]),
            ("Waar staat de invite-code?", [
                f"Niet in deze title. Bestaande coupon-URL’s op {host} blijven.",
            ]),
        ],
        "es": [
            ("¿FansBuy vende los productos de esta web?", [
                f"No. FansBuy es agente de compras. Pedidos y pagos solo en {OFF}.",
            ]),
            ("¿Puedo pagar aquí?", [
                f"No. Paga en {OFF}. Visualización en {ccy}. Flete vivo: {EST} con destino España.",
            ]),
            ("¿Qué país elijo en el estimador?", [
                f"España — no este TLD, no EU, no Francia. {city}.",
            ]),
            ("¿El QC ocurre en Correos?", [
                f"No. Las fotos salen del almacén en China. {post} es last-mile después del QC.",
            ]),
            ("¿Quién paga aranceles?", [
                f"La SKU. Fuente: {curl} ({customs}). Esta página no inventa un valor declarado.",
            ]),
            ("¿Canarias es la misma SKU?", [
                "A menudo no. Canarias y Ceuta/Melilla pueden ser otro producto de transporte. Elige la línea viva en la app.",
            ]),
            ("¿Por qué el catálogo no encuentra nada en español?", [
                "El índice está en inglés (sneakers, hoodie, jacket).",
            ]),
            ("¿Dónde está el código de invitación?", [
                f"No en este título. Las URLs de cupones en {host} se quedan.",
            ]),
        ],
        "fr": [
            ("FansBuy vend-il les produits sur ce site ?", [
                f"Non. FansBuy est agent d’achat. Commandes et paiements uniquement sur {OFF}.",
            ]),
            ("Puis-je payer ici ?", [
                f"Non. Paiement sur {OFF}. Affichage {ccy}. Fret live: {EST} destination France.",
            ]),
            ("Quel pays dans l’estimateur ?", [
                f"France — pas ce TLD, pas EU, pas Belgique. {city}.",
            ]),
            ("Le QC se fait-il chez Colissimo ?", [
                f"Non. Photos prises en Chine. {post} est last-mile après QC.",
            ]),
            ("Qui paie la douane ?", [
                f"La SKU. Source: {curl} ({customs}). Cette page n’invente pas de valeur déclarée.",
            ]),
            ("La Belgique est-elle la même SKU ?", [
                "Non. Un code postal belge est le mauvais pays.",
            ]),
            ("Pourquoi le catalogue ne trouve rien en français ?", [
                "L’index est anglais (sneakers, hoodie, jacket).",
            ]),
            ("Où est le code d’invitation ?", [
                f"Pas dans ce titre. Les URL coupon sur {host} restent.",
            ]),
        ],
        "it": [
            ("FansBuy vende i prodotti su questo sito?", [
                f"No. FansBuy è agente d’acquisto. Ordini e pagamenti solo su {OFF}.",
            ]),
            ("Posso pagare qui?", [
                f"No. Paghi su {OFF}. Visualizzazione {ccy}. Nolo live: {EST} destinazione Italia.",
            ]),
            ("Quale paese nell’estimator?", [
                f"Italia — non questo TLD, non EU. {city}.",
            ]),
            ("Il QC avviene da Poste?", [
                f"No. Foto dal magazzino in Cina. {post} è last-mile dopo il QC.",
            ]),
            ("Chi paga dazi e IVA?", [
                f"La SKU. Fonte: {curl} ({customs}). Questa pagina non inventa un valore dichiarato.",
            ]),
            ("San Marino o AT è la stessa SKU?", [
                "No. Resta su questo desk Italia per un CAP italiano.",
            ]),
            ("Perché il catalogo non trova nulla in italiano?", [
                "L’indice è inglese (sneakers, hoodie, jacket).",
            ]),
            ("Dov’è il codice invite?", [
                f"Non in questo title. Le URL coupon su {host} restano.",
            ]),
        ],
    }
    return packs[key]


def more_depth(d: dict, host: str) -> list:
    post, city, customs, curl, ccy = d["post"], d["city"], d["customs"], d["customs_url"], d["ccy"]
    key = d["key"]
    dest_name = d["label"]
    packs = {
        "uk": [
            ("Warehouse in China, not a Royal Mail depot", [
                f"QC photos are taken in the FansBuy warehouse in China. A {post} depot in the UK is last-mile, not a second QC studio.",
                f"Storage days are in official Help on {OFF}. After QC, open {EST} with destination United Kingdom. {city}.",
            ]),
            ("First order: one clothing SKU", [
                "For the first UK door, one hoodie or a pair of sneakers with warehouse photos is enough.",
                "Restricted, perfume, batteries and liquids stay off until the app allows them the morning you ship.",
            ]),
            ("English catalogue keys are labels", [
                "The category wall says sneakers, hoodie, jacket, bag because the index is English.",
                f"Estimator country stays the United Kingdom, {ccy} is display, checkout is {OFF}.",
            ]),
            ("What this hostname is not", [
                f"{host} is a spreadsheet toward a UK door. Register and tickets only on {OFF}.",
                "Northern Ireland is often another carrier product.",
            ]),
            ("Tracking after the border", [
                f"After the international line, tracking follows the SKU — often {post}.",
                f"Who pays import VAT is the booked SKU. Source: {curl} ({customs}).",
            ]),
            ("Returns only in the warehouse", [
                f"Fail-QC is handled in-app while the piece is in China. After {post} delivered, {customs} does not reopen a warehouse ticket.",
            ]),
            ("Neighbour countries are other SKUs", [
                f"{city} is the address test. An EU code in the estimator is the wrong country.",
            ]),
        ],
        "us": [
            ("Warehouse in China, not a USPS depot", [
                f"QC photos are taken in China. A {post} depot is last-mile. Open {EST} with destination United States. {city}.",
            ]),
            ("First order: one clothing SKU", [
                "One hoodie or a pair of sneakers with warehouse photos is enough for the first US door.",
            ]),
            ("English catalogue keys are labels", [
                f"Index keys stay English. Estimator country stays the United States, {ccy} is display, checkout is {OFF}.",
            ]),
            ("What this hostname is not", [
                f"{host} is a spreadsheet toward a US door. Register only on {OFF}. A Canadian A1A 1A1 code is the wrong country.",
            ]),
            ("Tracking after the border", [
                f"Tracking follows the SKU — often {post} or FedEx. Who pays duty is the booked SKU. Source: {curl} ({customs}).",
            ]),
            ("Returns only in the warehouse", [
                f"Fail-QC is in-app while the piece is in China. After {post} delivered, {customs} does not reopen a warehouse ticket.",
            ]),
            ("Neighbour countries are other SKUs", [
                "A Canadian postal code in the estimator is the wrong country.",
            ]),
        ],
        "ca": [
            ("Warehouse in China, not a Canada Post depot", [
                f"QC photos are taken in China. After QC, open {EST} with destination Canada. {city}.",
            ]),
            ("First order: one clothing SKU", [
                "One hoodie or a pair of sneakers with warehouse photos is enough for the first Canadian door.",
            ]),
            ("English catalogue keys are labels", [
                f"Canadian words often return zero cards. Estimator country stays Canada, {ccy} is display, checkout is {OFF}.",
            ]),
            ("What this hostname is not", [
                f"{host} is a spreadsheet toward a Canadian door. Register only on {OFF}. A US ZIP is the wrong country.",
            ]),
            ("Tracking after the border", [
                f"Tracking follows the SKU — often {post}. GST/HST is on the booked SKU. Source: {curl} ({customs}).",
            ]),
            ("Returns only in the warehouse", [
                f"Fail-QC is in-app in China. After {post} delivered, {customs} does not reopen a warehouse ticket.",
            ]),
            ("Neighbour countries are other SKUs", [
                "A US ZIP in the estimator is the wrong country.",
            ]),
        ],
        "de": [
            ("Lager in China, kein DHL-Depot", [
                f"QC-Fotos entstehen in China. Nach QC {EST} mit Ziel Deutschland öffnen. {city}.",
            ]),
            ("Erste Bestellung: eine Kleidungs-SKU", [
                "Ein Hoodie oder ein Paar Sneaker mit Lagerfotos reicht für die erste deutsche Tür.",
            ]),
            ("Englische Katalogschlüssel sind Labels", [
                f"Deutsche Wörter liefern oft 0 Karten. Schätzer-Land bleibt Deutschland, {ccy} ist Anzeige, Kasse ist {OFF}.",
            ]),
            ("Was dieser Hostname nicht ist", [
                f"{host} ist Spreadsheet zu einer deutschen Tür. Registrieren nur auf {OFF}. Packstation ist DE. 1010 Wien ist AT.",
            ]),
            ("Sendungsverfolgung nach der Grenze", [
                f"Tracking folgt der SKU — oft {post}. Zoll steht auf der SKU. Quelle: {curl} ({customs}).",
            ]),
            ("Retouren nur im Lager", [
                f"Fail-QC läuft in der App in China. Nach {post}-Zustellung öffnet {customs} kein Lagerticket.",
            ]),
            ("Nachbarländer sind andere SKUs", [
                "Eine österreichische PLZ im Schätzer ist das falsche Land.",
            ]),
        ],
        "at": [
            ("Lager in China, kein Post-Depot", [
                f"QC-Fotos in China. Nach QC {EST} mit Ziel Österreich. {city}. Keine deutsche Packstation.",
            ]),
            ("Erste Bestellung: eine Kleidungs-SKU", [
                "Ein Hoodie oder Sneaker mit Lagerfotos reicht für die erste österreichische Tür.",
            ]),
            ("Englische Katalogschlüssel sind Labels", [
                f"Schätzer-Land bleibt Österreich, {ccy} ist Anzeige, Kasse ist {OFF}.",
            ]),
            ("Was dieser Hostname nicht ist", [
                f"{host} ist Spreadsheet zu einer österreichischen Tür. Registrieren nur auf {OFF}. Packstation ist DE.",
            ]),
            ("Sendungsverfolgung nach der Grenze", [
                f"Tracking folgt der SKU — oft {post}. Quelle: {curl} ({customs}).",
            ]),
            ("Retouren nur im Lager", [
                "Fail-QC in der App in China. Nach Zustellung kein Lagerticket über den Zoll.",
            ]),
            ("Nachbarländer sind andere SKUs", [
                "Eine fünfstellige DE-PLZ im Schätzer ist das falsche Land.",
            ]),
        ],
        "nl": [
            ("Magazijn in China, geen PostNL-depot", [
                f"QC-foto’s uit China. Na QC {EST} met bestemming Nederland. {city}.",
            ]),
            ("Eerste bestelling: één kleding-SKU", [
                "Een hoodie of sneakers met magazijnfoto’s volstaat voor de eerste Nederlandse deur.",
            ]),
            ("Engelse catalogsleutels zijn labels", [
                f"Estimator-land blijft Nederland, {ccy} is weergave, kassa is {OFF}.",
            ]),
            ("Wat deze hostname niet is", [
                f"{host} is spreadsheet naar een Nederlandse deur. Registreren alleen op {OFF}. Een Belgische postcode is het verkeerde land.",
            ]),
            ("Tracking na de grens", [
                f"Tracking volgt de SKU — vaak {post}. Bron: {curl} ({customs}).",
            ]),
            ("Retour alleen in het magazijn", [
                "Fail-QC in de app in China. Na bezorging geen magazijnticket via Douane.",
            ]),
            ("Buurlanden zijn andere SKUs", [
                "Een Belgische postcode in de estimator is het verkeerde land. iDEAL bevestig je in de app.",
            ]),
        ],
        "es": [
            ("Almacén en China, no un depósito de Correos", [
                f"Fotos QC en China. Después {EST} con destino España. {city}.",
            ]),
            ("Primer pedido: una SKU de ropa", [
                "Una sudadera o unas zapatillas con fotos de almacén bastan para la primera puerta en España.",
            ]),
            ("Las claves del catálogo son etiquetas", [
                f"El país del estimador sigue siendo España, {ccy} es visualización, caja es {OFF}.",
            ]),
            ("Lo que no es este hostname", [
                f"{host} es spreadsheet hacia una puerta en España. Registro solo en {OFF}.",
            ]),
            ("Seguimiento tras la frontera", [
                f"El tracking sigue la SKU — a menudo {post}. Fuente: {curl} ({customs}).",
            ]),
            ("Devoluciones solo en almacén", [
                "Fail-QC en la app en China. Tras la entrega, aduanas no reabre el ticket de almacén.",
            ]),
            ("Países vecinos son otras SKU", [
                "Un código postal francés en el estimador es el país equivocado. Canarias puede ser otra línea.",
            ]),
        ],
        "fr": [
            ("Entrepôt en Chine, pas un dépôt Colissimo", [
                f"Photos QC en Chine. Ensuite {EST} destination France. {city}.",
            ]),
            ("Première commande: une SKU vêtement", [
                "Un hoodie ou une paire de baskets avec photos d’entrepôt suffit.",
            ]),
            ("Les clés catalogue sont des labels", [
                f"Pays estimateur: France. {ccy} est l’affichage. Caisse: {OFF}.",
            ]),
            ("Ce que ce hostname n’est pas", [
                f"{host} est un spreadsheet vers une porte en France. Inscription seulement sur {OFF}.",
            ]),
            ("Suivi après la frontière", [
                f"Le tracking suit la SKU — souvent {post}. Source: {curl} ({customs}).",
            ]),
            ("Retours seulement en entrepôt", [
                "Fail-QC dans l’app en Chine. Après livraison, la douane ne rouvre pas le ticket entrepôt.",
            ]),
            ("Les pays voisins sont d’autres SKU", [
                "Un code postal belge dans l’estimateur est le mauvais pays.",
            ]),
        ],
        "it": [
            ("Magazzino in Cina, non un deposito Poste", [
                f"Foto QC in Cina. Poi {EST} destinazione Italia. {city}.",
            ]),
            ("Primo ordine: una SKU di abbigliamento", [
                "Una felpa o un paio di sneaker con foto magazzino basta per la prima porta in Italia.",
            ]),
            ("Le chiavi catalogo sono etichette", [
                f"Paese estimator: Italia. {ccy} è display. Cassa: {OFF}.",
            ]),
            ("Cosa non è questo hostname", [
                f"{host} è spreadsheet verso una porta in Italia. Registrazione solo su {OFF}.",
            ]),
            ("Tracking dopo il confine", [
                f"Il tracking segue la SKU — spesso {post}. Fonte: {curl} ({customs}).",
            ]),
            ("Resi solo in magazzino", [
                "Fail-QC in-app in Cina. Dopo la consegna la dogana non riapre il ticket magazzino.",
            ]),
            ("I paesi vicini sono altre SKU", [
                "Un CAP austriaco o un Packstation tedesco è il paese sbagliato.",
            ]),
        ],
    }
    return packs[key]


def wrap_copy(host: str, d: dict, keep_slug: str):
    h1 = inner_h1("guide", d)
    lead = f"Guide pages on {host} stay on this hostname."
    secs = extra_local(d, host)[:2]
    return h1, lead, secs


def _en(kind, host, d):
    dest_name = d["label"]
    post, city, customs, curl, ccy = d["post"], d["city"], d["customs"], d["customs_url"], d["ccy"]
    neighbour = {
        "uk": "Ireland and EU codes are other estimator countries.",
        "us": "A Canadian A1A 1A1 code is the wrong country.",
        "ca": "A US ZIP is the wrong country.",
    }[d["key"]]
    if kind == "spreadsheet":
        return (
            f"A curated {A} spreadsheet for {dest_name} buyers on {host}: trusted sellers, QC photos and finds in one index. Order on {OFF} in {ccy} after you pick destination {dest_name}.",
            [
                (f"What is an {A} spreadsheet?", [
                    f"An {A} spreadsheet on {host} is a shortlist of warehouse-checked SKUs meant for a {dest_name} delivery address. It does not take payment.",
                    f"Rows stay useful only while the source link is live and at least one warehouse photo exists. Keywords: FansBuy spreadsheet, fansbuy spreadsheet {geo(d['dest'])}, fansbuy trusted sellers.",
                ]),
                (f"Why {dest_name} buyers start with a sheet", [
                    f"The sheet keeps finds you already accepted in QC before you ask {post} to move a carton toward {city}.",
                    f"{neighbour} This page is written for {dest_name}, {ccy}, and {customs}.",
                ]),
                (f"How {A} spreadsheets work", [
                    f"Open a find, read warehouse photos in the official app, then book a line with destination {dest_name}. Cart and tickets stay on {OFF}.",
                    f"Live money is in {EST}.",
                ]),
                ("What types of products are included?", [
                    "Shoes, hoodies, jackets, bags and watches dominate because those SKUs still have QC angles. Electronics, perfume and liquids stay off unless the app allows them the morning you submit.",
                ]),
                (f"Is using an {A} spreadsheet safer?", [
                    f"Safer than guessing a random Weidian link, because warehouse photos exist. It is not a customs guarantee. Read {curl} ({customs}) the morning you ship.",
                ]),
            ],
        )
    if kind == "finds":
        return (
            f"Top {A} finds for a {dest_name} address on {host}. QC first, then freight via {EST}.",
            [
                ("How finds are picked", [
                    f"A find stays on {host} while the source link opens and at least one warehouse photo exists. Price-0 cards are dead links.",
                ]),
                ("Sneakers, hoodies, jackets", [
                    "Those categories still photograph well in the warehouse. Restricted classes stay off until the app allows them.",
                ]),
                ("Open the official app", [
                    f"Cards on {host} are an index. You paste the same link on {OFF} and pay there in {ccy}.",
                ]),
            ],
        )
    if kind == "qc":
        return (
            f"{A} warehouse photos before a carton moves toward {dest_name}. {post} is last-mile, not a QC studio.",
            [
                ("What QC photos show", [
                    "Angles of the piece in the China warehouse: labels, flaws, measurements. Extra angles are often paid in-app.",
                ]),
                ("Accept QC before freight", [
                    f"Do not book {EST} with destination {dest_name} until you accept the photos. Fail-QC is cheaper in the warehouse than after {customs}.",
                ]),
                ("Where QC happens", [
                    f"China warehouse, not a {post} depot. {city} is the label after you accept.",
                ]),
            ],
        )
    if kind == "shipping":
        return (
            f"{A} shipping toward {dest_name}: pick the live SKU in {EST}, last-mile often {post}.",
            [
                ("Estimator country", [
                    f"Set destination {dest_name} — not this TLD. {city}. {neighbour}",
                ]),
                ("Two payments", [
                    f"Goods into China, then international freight. Storage days live in Help on {OFF}.",
                ]),
                ("Who pays import", [
                    f"The booked SKU. {post} can add collect. Source: {curl} ({customs}). No declared-value coaching on this page.",
                ]),
            ],
        )
    if kind == "legal":
        return (
            f"Is {A} safe and legal for a {dest_name} delivery address? Purchasing agent, not a shop. Pay on {OFF}.",
            [
                ("Purchasing agent", [
                    f"{A} buys from Chinese third-party shops in your name. {host} is a spreadsheet, not checkout.",
                ]),
                ("Customs is the SKU", [
                    f"Who pays duty is on the booked line. Read {curl} ({customs}) the morning you ship. This page does not invent a declared value.",
                ]),
                ("Restricted is not seizure", [
                    "A restricted or price-0 card is a purchase block or a dead link, not a customs notice.",
                ]),
            ],
        )
    if kind == "guide":
        return (
            f"How to buy with {A} toward {dest_name}: paste a link on {OFF}, accept QC, then book {EST}.",
            [
                ("Register on the official site", [
                    f"Create the account on {OFF} before you paste a product URL. {host} never takes a card.",
                ]),
                ("Paste, QC, ship", [
                    f"Paste Taobao/1688/Weidian on {OFF}. Wait for warehouse photos. Book destination {dest_name} in {EST}. Last-mile often {post}.",
                ]),
                ("Address test", [
                    f"{city}. {neighbour}",
                ]),
            ],
        )
    return (
        f"{A} FAQ for {dest_name} buyers on {host}.",
        extra_faq(d, host)[:4],
    )


def _de(kind, host, d):
    post, city, customs, curl, ccy = d["post"], d["city"], d["customs"], d["customs_url"], d["ccy"]
    if kind == "spreadsheet":
        return (
            f"Ein {A}-Spreadsheet für Käufer in Deutschland auf {host}: Finds, QC und Versand. Bestellen auf {OFF} in {ccy}.",
            [
                ("Was ist ein FansBuy-Spreadsheet?", [
                    f"Eine Kurzliste lagergeprüfter SKUs für eine deutsche Lieferadresse. Keine Kasse. Keywords: FansBuy spreadsheet, fansbuy spreadsheet deutschland, fansbuy trusted sellers.",
                ]),
                ("Warum Deutschland mit einem Sheet startet", [
                    f"Du akzeptierst QC, bevor {post} den Karton zur {city} bewegt. Packstation ist DE. 1010 Wien ist AT.",
                ]),
                ("So funktioniert es", [
                    f"Find öffnen, Lagerfotos in der App, Linie mit Ziel Deutschland in {EST}. Zahlen auf {OFF}.",
                ]),
            ],
        )
    if kind == "finds":
        return (f"{A}-Finds für eine deutsche Adresse auf {host}.", [
            ("Wie Finds bleiben", ["Nur solange der Quell-Link lebt und ein Lagerfoto existiert."]),
            ("Kategorien", ["Sneaker, Hoodies, Jacken, Taschen — weil QC-Winkel existieren."]),
        ])
    if kind == "qc":
        return (f"{A} QC-Fotos vor dem Versand nach Deutschland.", [
            ("Wo QC passiert", ["Im Lager in China, nicht im DHL-Depot."]),
            ("Erst QC, dann Fracht", [f"Nicht {EST} mit Ziel Deutschland buchen, bevor du die Fotos akzeptierst."]),
        ])
    if kind == "shipping":
        return (f"{A} Versand nach Deutschland. Last-mile oft {post}.", [
            ("Schätzer-Land", [f"Deutschland, nicht AT, nicht EU. {city}."]),
            ("Abgaben", [f"Steht auf der SKU. Quelle: {curl} ({customs}). Kein Deklarationsbetrag."]),
        ])
    if kind == "legal":
        return (f"Ist {A} sicher und legal in Deutschland?", [
            ("Einkaufsagent", [f"FansBuy kauft in deinem Namen. Zahlen auf {OFF}."]),
            ("Zoll", [f"Die SKU entscheidet. Quelle: {curl} ({customs})."]),
        ])
    if kind == "guide":
        return (f"Kaufen über {A} nach Deutschland: Link auf {OFF}, QC, dann {EST}.", [
            ("Registrieren", [f"Konto nur auf {OFF}."]),
            ("Adresse", [f"{city}. Packstation ist DE, nicht AT."]),
        ])
    return (f"{A} FAQ für Deutschland auf {host}.", extra_faq(d, host)[:4])


def _at(kind, host, d):
    post, city, customs, curl, ccy = d["post"], d["city"], d["customs"], d["customs_url"], d["ccy"]
    if kind == "spreadsheet":
        return (
            f"Ein {A}-Spreadsheet für Käufer in Österreich auf {host}. Bestellen auf {OFF} in {ccy}.",
            [
                ("Was ist das Spreadsheet?", [
                    "Kurzliste lagergeprüfter SKUs für eine österreichische Tür. Keine Kasse.",
                ]),
                ("Österreich, nicht DE", [
                    f"{city}. Packstation und fünfstellige DE-PLZ sind das falsche Land. Schätzer: Österreich in {EST}.",
                ]),
            ],
        )
    if kind == "finds":
        return (f"{A}-Finds für Österreich auf {host}.", [
            ("Finds", ["Sneaker, Hoodies, Jacken mit Lagerfotos. Restricted bleibt draußen."]),
        ])
    if kind == "qc":
        return (f"{A} QC-Fotos vor dem Versand nach Österreich.", [
            ("Lager in China", [f"Nicht bei {post}. Extra-Winkel oft kostenpflichtig."]),
        ])
    if kind == "shipping":
        return (f"{A} Versand nach Österreich. Last-mile oft {post}.", [
            ("Schätzer", [f"Österreich, nicht DE, nicht EU. {city}."]),
            ("Zoll", [f"SKU entscheidet. Quelle: {curl} ({customs})."]),
        ])
    if kind == "legal":
        return (f"Ist {A} sicher und legal in Österreich?", [
            ("Agent", [f"Einkaufsagent. Zahlen auf {OFF}."]),
            ("Zoll", [f"Quelle: {curl} ({customs}). Kein Deklarationsbetrag."]),
        ])
    if kind == "guide":
        return (f"Kaufen über {A} nach Österreich.", [
            ("Schritte", [f"Registrieren auf {OFF}, Link einfügen, QC, {EST} mit Ziel Österreich."]),
        ])
    return (f"{A} FAQ für Österreich auf {host}.", extra_faq(d, host)[:4])


def _nl(kind, host, d):
    post, city, customs, curl, ccy = d["post"], d["city"], d["customs"], d["customs_url"], d["ccy"]
    if kind == "spreadsheet":
        return (
            f"Een {A}-spreadsheet voor kopers in Nederland op {host}. Bestellen op {OFF} in {ccy}.",
            [
                ("Wat is de spreadsheet?", [
                    "Een shortlist van magazijn-gecheckte SKUs naar een Nederlandse deur. Geen kassa.",
                ]),
                ("Nederland, niet BE", [
                    f"{city}. Een Belgische postcode is het verkeerde land. Estimator: Nederland in {EST}.",
                ]),
            ],
        )
    if kind == "finds":
        return (f"{A}-finds voor Nederland op {host}.", [
            ("Finds", ["Sneakers, hoodies, jassen met magazijnfoto’s."]),
        ])
    if kind == "qc":
        return (f"{A} QC-foto’s vóór verzending naar Nederland.", [
            ("Magazijn in China", [f"Niet bij {post}."]),
        ])
    if kind == "shipping":
        return (f"{A} verzending naar Nederland. Last-mile vaak {post}.", [
            ("Estimator", [f"Nederland, niet BE, niet EU. {city}."]),
            ("Douane", [f"SKU beslist. Bron: {curl} ({customs})."]),
        ])
    if kind == "legal":
        return (f"Is {A} veilig en legaal in Nederland?", [
            ("Agent", [f"Inkoopagent. Betalen op {OFF}."]),
            ("Douane", [f"Bron: {curl} ({customs}). Geen aangegeven waarde op deze pagina."]),
        ])
    if kind == "guide":
        return (f"Kopen via {A} naar Nederland.", [
            ("Stappen", [f"Registreren op {OFF}, link plakken, QC, {EST} met bestemming Nederland. iDEAL in de app."]),
        ])
    return (f"{A} FAQ voor Nederland op {host}.", extra_faq(d, host)[:4])


def _es(kind, host, d):
    post, city, customs, curl, ccy = d["post"], d["city"], d["customs"], d["customs_url"], d["ccy"]
    if kind == "spreadsheet":
        return (
            f"Un spreadsheet {A} para compradores en España en {host}. Pedidos en {OFF} en {ccy}.",
            [
                ("Qué es", ["Índice de SKU con fotos de almacén hacia una puerta en España. No es caja."]),
                ("España, no EU", [f"{city}. Canarias puede ser otra línea. Estimador: España en {EST}."]),
            ],
        )
    if kind == "finds":
        return (f"Finds {A} para España en {host}.", [
            ("Finds", ["Zapatillas, sudaderas, chaquetas con fotos de almacén."]),
        ])
    if kind == "qc":
        return (f"Fotos QC {A} antes del envío a España.", [
            ("Almacén en China", [f"No en {post}."]),
        ])
    if kind == "shipping":
        return (f"Envío {A} a España. Last-mile a menudo {post}.", [
            ("Estimador", [f"España, no este TLD, no EU. {city}."]),
            ("Aduanas", [f"La SKU. Fuente: {curl} ({customs})."]),
        ])
    if kind == "legal":
        return (f"¿Es {A} legal en España?", [
            ("Agente", [f"Agente de compras. Pago en {OFF}."]),
            ("Aduanas", [f"Fuente: {curl} ({customs}). Sin valor declarado en esta página."]),
        ])
    if kind == "guide":
        return (f"Comprar con {A} hacia España.", [
            ("Pasos", [f"Registro en {OFF}, pegar enlace, QC, {EST} destino España."]),
        ])
    return (f"FAQ {A} para España en {host}.", extra_faq(d, host)[:4])


def _fr(kind, host, d):
    post, city, customs, curl, ccy = d["post"], d["city"], d["customs"], d["customs_url"], d["ccy"]
    if kind == "spreadsheet":
        return (
            f"Un spreadsheet {A} pour acheteurs en France sur {host}. Commandes sur {OFF} en {ccy}.",
            [
                ("Qu’est-ce que c’est", ["Index de SKU avec photos d’entrepôt vers une porte en France. Pas une caisse."]),
                ("France, pas EU", [f"{city}. Un code belge est le mauvais pays. Estimateur: France dans {EST}."]),
            ],
        )
    if kind == "finds":
        return (f"Finds {A} pour la France sur {host}.", [
            ("Finds", ["Baskets, hoodies, vestes avec photos d’entrepôt."]),
        ])
    if kind == "qc":
        return (f"Photos QC {A} avant l’envoi vers la France.", [
            ("Entrepôt en Chine", [f"Pas chez {post}."]),
        ])
    if kind == "shipping":
        return (f"Livraison {A} vers la France. Last-mile souvent {post}.", [
            ("Estimateur", [f"France, pas ce TLD, pas EU. {city}."]),
            ("Douane", [f"La SKU. Source: {curl} ({customs})."]),
        ])
    if kind == "legal":
        return (f"{A} est-il légal en France ?", [
            ("Agent", [f"Agent d’achat. Paiement sur {OFF}."]),
            ("Douane", [f"Source: {curl} ({customs}). Pas de valeur déclarée ici."]),
        ])
    if kind == "guide":
        return (f"Acheter avec {A} vers la France.", [
            ("Étapes", [f"Inscription sur {OFF}, coller le lien, QC, {EST} destination France."]),
        ])
    return (f"FAQ {A} pour la France sur {host}.", extra_faq(d, host)[:4])


def _it(kind, host, d):
    post, city, customs, curl, ccy = d["post"], d["city"], d["customs"], d["customs_url"], d["ccy"]
    if kind == "spreadsheet":
        return (
            f"Uno spreadsheet {A} per acquirenti in Italia su {host}. Ordini su {OFF} in {ccy}.",
            [
                ("Che cos’è", ["Indice di SKU con foto magazzino verso una porta in Italia. Non è cassa."]),
                ("Italia, non EU", [f"{city}. Un Packstation tedesco è il paese sbagliato. Estimator: Italia in {EST}."]),
            ],
        )
    if kind == "finds":
        return (f"Finds {A} per l’Italia su {host}.", [
            ("Finds", ["Sneaker, felpe, giacche con foto magazzino."]),
        ])
    if kind == "qc":
        return (f"Foto QC {A} prima della spedizione in Italia.", [
            ("Magazzino in Cina", [f"Non da {post}."]),
        ])
    if kind == "shipping":
        return (f"Spedizione {A} in Italia. Last-mile spesso {post}.", [
            ("Estimator", [f"Italia, non questo TLD, non EU. {city}."]),
            ("Dogana", [f"La SKU. Fonte: {curl} ({customs})."]),
        ])
    if kind == "legal":
        return (f"{A} è legale in Italia?", [
            ("Agente", [f"Agente d’acquisto. Pagamento su {OFF}."]),
            ("Dogana", [f"Fonte: {curl} ({customs}). Nessun valore dichiarato in questa pagina."]),
        ])
    if kind == "guide":
        return (f"Comprare con {A} verso l’Italia.", [
            ("Passi", [f"Registrati su {OFF}, incolla il link, QC, {EST} destinazione Italia."]),
        ])
    return (f"FAQ {A} per l’Italia su {host}.", extra_faq(d, host)[:4])
