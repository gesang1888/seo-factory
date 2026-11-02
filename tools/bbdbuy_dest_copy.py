"""Localized inner copy for BBDBuy dest desks, UK-cluster depth.

Public pages: no ops notes, no declared-value coaching, no invented transit
days or duty rates. Unique coupons/telegram/contact CMS are not rendered here.
"""
from __future__ import annotations

A = "BBDBuy"
OFF = "www.bbdbuy.com"
EST = "https://www.bbdbuy.com/estimation"


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
        "CA": "canada",
        "PL": "polska",
    }.get(dest, dest.lower())


def inner_keywords(kind: str, d: dict) -> list[str]:
    g = geo(d["dest"])
    table = {
        "spreadsheet": [f"{A} spreadsheet", f"bbdbuy spreadsheet {g}", "bbdbuy trusted sellers"],
        "finds": ["bbdbuy finds", "bbdbuy spreadsheet finds", "best bbdbuy items"],
        "qc": ["bbdbuy qc", f"bbdbuy qc {g}", "bbdbuy warehouse photos"],
        "shipping": ["bbdbuy shipping", f"bbdbuy shipping {g}", "bbdbuy delivery time"],
        "legal": ["bbdbuy safe", "bbdbuy legit", f"bbdbuy safe {g}"],
        "guide": ["bbdbuy spreadsheet guide", "how to use bbdbuy", "bbdbuy buying guide"],
        "faq": ["bbdbuy faq", "bbdbuy spreadsheet faq", "bbdbuy questions"],
    }
    return table[kind]


def inner_serp_title(kind: str, d: dict) -> str:
    key = d["key"]
    table = {
        "spreadsheet": {
            "uk": f"{A} Spreadsheet UK – Best Sellers, QC & Finds",
            "us": f"{A} Spreadsheet USA – Best Sellers, QC & Finds",
            "ca": f"{A} Spreadsheet Canada – Best Sellers, QC & Finds",
            "at": f"{A} Spreadsheet Österreich – Finds und QC",
            "de": f"{A} Spreadsheet Deutschland – Finds und QC",
            "es": f"{A} Spreadsheet España – Mejores finds y QC",
            "fr": f"{A} Spreadsheet France – Meilleurs finds et QC",
            "it": f"{A} Spreadsheet Italia – Migliori finds e QC",
            "nl": f"{A} Spreadsheet Nederland – Beste finds en QC",
            "pl": f"{A} Spreadsheet Polska – Finds i QC",
        },
        "finds": {
            "uk": f"Top {A} Spreadsheet Finds – Best UK Picks 2026",
            "us": f"Top {A} Spreadsheet Finds – Best US Picks 2026",
            "ca": f"Top {A} Spreadsheet Finds – Best Canada Picks 2026",
            "at": f"{A} spreadsheet finds – Auswahl Österreich 2026",
            "de": f"{A} spreadsheet finds – Auswahl Deutschland 2026",
            "es": f"Mejores finds {A} – selección España 2026",
            "fr": f"Meilleurs finds {A} – sélection France 2026",
            "it": f"Migliori finds {A} – selezione Italia 2026",
            "nl": f"Beste {A} finds – Nederland 2026",
            "pl": f"Najlepsze finds {A} – Polska 2026",
        },
        "qc": {
            "uk": f"{A} QC Photos for UK Buyers – Warehouse Check",
            "us": f"{A} QC Photos for US Buyers – Warehouse Check",
            "ca": f"{A} QC Photos for Canada Buyers – Warehouse Check",
            "at": f"{A} QC-Fotos nach Österreich – Lagercheck",
            "de": f"{A} QC-Fotos nach Deutschland – Lagercheck",
            "es": f"Fotos QC {A} para España – almacén",
            "fr": f"Photos QC {A} France – contrôle entrepôt",
            "it": f"Foto QC {A} Italia – magazzino",
            "nl": f"{A} QC-foto’s Nederland – magazijncheck",
            "pl": f"{A} zdjęcia QC dla Polski – magazyn",
        },
        "shipping": {
            "uk": f"{A} Shipping to the UK – Cost, Time & Royal Mail",
            "us": f"{A} Shipping to the USA – Cost, Time & USPS",
            "ca": f"{A} Shipping to Canada – Cost, Time & Canada Post",
            "at": f"{A} Versand nach Österreich – Preis, Zeit und Post AT",
            "de": f"{A} Versand nach Deutschland – Preis, Zeit und DHL",
            "es": f"Envío {A} a España – coste, plazos y Correos",
            "fr": f"Livraison {A} France – coût, délais et Colissimo",
            "it": f"Spedizione {A} Italia – costi, tempi e Poste",
            "nl": f"{A} verzending Nederland – kosten, tijd en DHL",
            "pl": f"{A} wysyłka do Polski – koszt, czas i InPost",
        },
        "legal": {
            "uk": f"Is {A} Safe & Legal for UK Buyers? Full Guide",
            "us": f"Is {A} Safe & Legal for US Buyers? Full Guide",
            "ca": f"Is {A} Safe & Legal for Canada Buyers? Full Guide",
            "at": f"Ist {A} sicher und legal in Österreich?",
            "de": f"Ist {A} sicher und legal in Deutschland?",
            "es": f"¿{A} es seguro y legal en España? Guía",
            "fr": f"{A} est-il sûr et légal en France ? Guide",
            "it": f"{A} è sicuro e legale in Italia? Guida",
            "nl": f"Is {A} veilig en legaal in Nederland?",
            "pl": f"Czy {A} jest bezpieczny i legalny w Polsce?",
        },
        "guide": {
            "uk": f"How to Use {A} Spreadsheet – Beginner Guide UK",
            "us": f"How to Use {A} Spreadsheet – Beginner Guide USA",
            "ca": f"How to Use {A} Spreadsheet – Beginner Guide Canada",
            "at": f"{A}-Spreadsheet nutzen – Start für Österreich",
            "de": f"{A}-Spreadsheet nutzen – Start für Deutschland",
            "es": f"Cómo usar el spreadsheet {A} – guía España",
            "fr": f"Utiliser le spreadsheet {A} – guide France",
            "it": f"Usare lo spreadsheet {A} – guida Italia",
            "nl": f"{A}-spreadsheet gebruiken – startergids NL",
            "pl": f"Jak używać spreadsheet {A} – poradnik PL",
        },
        "faq": {
            "uk": f"{A} Spreadsheet FAQ – UK Buyers Guide 2026",
            "us": f"{A} Spreadsheet FAQ – US Buyers Guide 2026",
            "ca": f"{A} Spreadsheet FAQ – Canada Buyers Guide 2026",
            "at": f"{A} Spreadsheet FAQ – Leitfaden Österreich",
            "de": f"{A} Spreadsheet FAQ – Leitfaden Deutschland",
            "es": f"FAQ spreadsheet {A} – guía España 2026",
            "fr": f"FAQ spreadsheet {A} – guide France 2026",
            "it": f"FAQ spreadsheet {A} – guida Italia 2026",
            "nl": f"{A} spreadsheet FAQ – gids Nederland 2026",
            "pl": f"{A} spreadsheet FAQ – przewodnik Polska 2026",
        },
    }
    return table[kind][key]


def inner_h1(kind: str, d: dict) -> str:
    key = d["key"]
    table = {
        "spreadsheet": {
            "uk": f"{A} Spreadsheet for UK Buyers",
            "us": f"{A} Spreadsheet for US Buyers",
            "ca": f"{A} Spreadsheet for Canada Buyers",
            "at": f"{A} Spreadsheet für Käufer in Österreich",
            "de": f"{A} Spreadsheet für Käufer in Deutschland",
            "es": f"{A} Spreadsheet para compradores en España",
            "fr": f"{A} Spreadsheet pour acheteurs en France",
            "it": f"{A} Spreadsheet per acquirenti in Italia",
            "nl": f"{A} Spreadsheet voor kopers in Nederland",
            "pl": f"{A} Spreadsheet dla kupujących w Polsce",
        },
        "finds": {
            "uk": f"Top {A} Finds for UK Buyers (2026 Guide)",
            "us": f"Top {A} Finds for US Buyers (2026 Guide)",
            "ca": f"Top {A} Finds for Canada Buyers (2026 Guide)",
            "at": f"{A}-Finds für Österreich (2026)",
            "de": f"{A}-Finds für Deutschland (2026)",
            "es": f"Mejores finds {A} para España (guía 2026)",
            "fr": f"Meilleurs finds {A} pour la France (guide 2026)",
            "it": f"Migliori finds {A} per l’Italia (guida 2026)",
            "nl": f"Beste {A}-finds voor Nederland (gids 2026)",
            "pl": f"Najlepsze finds {A} dla Polski (poradnik 2026)",
        },
        "qc": {
            "uk": f"{A} QC Photos before Shipping to the UK",
            "us": f"{A} QC Photos before Shipping to the USA",
            "ca": f"{A} QC Photos before Shipping to Canada",
            "at": f"{A} QC-Fotos vor dem Versand nach Österreich",
            "de": f"{A} QC-Fotos vor dem Versand nach Deutschland",
            "es": f"Fotos QC de {A} antes de enviar a España",
            "fr": f"Photos QC {A} avant envoi vers la France",
            "it": f"Foto QC {A} prima della spedizione in Italia",
            "nl": f"{A} QC-foto’s vóór verzending naar Nederland",
            "pl": f"Zdjęcia QC {A} przed wysyłką do Polski",
        },
        "shipping": {
            "uk": f"{A} Shipping to the UK (2026 Guide)",
            "us": f"{A} Shipping to the USA (2026 Guide)",
            "ca": f"{A} Shipping to Canada (2026 Guide)",
            "at": f"{A}-Versand nach Österreich (Leitfaden 2026)",
            "de": f"{A}-Versand nach Deutschland (Leitfaden 2026)",
            "es": f"Envío {A} a España (guía 2026)",
            "fr": f"Livraison {A} vers la France (guide 2026)",
            "it": f"Spedizione {A} in Italia (guida 2026)",
            "nl": f"{A}-verzending naar Nederland (gids 2026)",
            "pl": f"Wysyłka {A} do Polski (poradnik 2026)",
        },
        "legal": {
            "uk": f"Is {A} Safe & Legal for UK Buyers?",
            "us": f"Is {A} Safe & Legal for US Buyers?",
            "ca": f"Is {A} Safe & Legal for Canada Buyers?",
            "at": f"Ist {A} sicher und legal in Österreich?",
            "de": f"Ist {A} sicher und legal in Deutschland?",
            "es": f"¿{A} es seguro y legal para compradores en España?",
            "fr": f"{A} est-il sûr et légal pour les acheteurs en France ?",
            "it": f"{A} è sicuro e legale per acquirenti in Italia?",
            "nl": f"Is {A} veilig en legaal voor kopers in Nederland?",
            "pl": f"Czy {A} jest bezpieczny i legalny dla kupujących w Polsce?",
        },
        "guide": {
            "uk": f"Buying from {A}: A Step-by-Step Guide for UK Buyers",
            "us": f"Buying from {A}: A Step-by-Step Guide for US Buyers",
            "ca": f"Buying from {A}: A Step-by-Step Guide for Canada Buyers",
            "at": f"Kaufen über {A}: Schritte für eine österreichische Adresse",
            "de": f"Kaufen über {A}: Schritte für eine deutsche Adresse",
            "es": f"Comprar en {A}: guía paso a paso para España",
            "fr": f"Acheter avec {A} : guide pas à pas pour la France",
            "it": f"Comprare con {A}: guida passo passo per l’Italia",
            "nl": f"Kopen via {A}: stappenplan voor Nederland",
            "pl": f"Zakupy przez {A}: krok po kroku dla Polski",
        },
        "faq": {
            "uk": f"{A} FAQ for UK Buyers (2026)",
            "us": f"{A} FAQ for US Buyers (2026)",
            "ca": f"{A} FAQ for Canada Buyers (2026)",
            "at": f"{A} FAQ für Käufer in Österreich (2026)",
            "de": f"{A} FAQ für Käufer in Deutschland (2026)",
            "es": f"FAQ {A} para compradores en España (2026)",
            "fr": f"FAQ {A} pour acheteurs en France (2026)",
            "it": f"FAQ {A} per acquirenti in Italia (2026)",
            "nl": f"{A} FAQ voor kopers in Nederland (2026)",
            "pl": f"{A} FAQ dla kupujących w Polsce (2026)",
        },
    }
    return table[kind][key]


def sections_for(kind: str, d: dict, host: str):
    h1 = inner_h1(kind, d)
    fn = {
        "uk": _uk,
        "us": _us,
        "ca": _ca,
        "de": _de,
        "it": _it,
        "es": _es,
        "fr": _fr,
        "nl": _nl,
        "pl": _pl,
    }[d["key"]]
    lead, secs = fn(kind, host, d)
    if kind != "faq":
        secs = list(secs) + extra_local(d, host) + more_depth(d, host)
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
                f"Copy the product URL from the Chinese shop, paste it on {OFF}, and BBDBuy buys it into the warehouse. {host} is the spreadsheet and guide for that path toward a UK door.",
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
                f"Paste the Chinese shop URL on {OFF}. BBDBuy buys into the warehouse, then you book a line toward a US door after QC.",
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
                f"If the official screen still prints a dollar symbol, trust the number in the app and the calculator at {EST}.",
            ]),
            ("Paste a Taobao, 1688 or Weidian link", [
                f"Paste the Chinese shop URL on {OFF}. BBDBuy buys into the warehouse, then you book a line toward a Canada Post door after QC.",
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
                f"Produkt-URL auf {OFF} einfügen. BBDBuy kauft ins Lager, danach buchst du die Linie nach Österreich.",
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
                f"Auf dem Label stehen eine deutsche Straße und eine fünfstellige PLZ. Packstation-Nummern sind ein DE-Muster — {city}. Eine österreichische 1010 Wien oder eine vierstellige AT-PLZ ist das falsche Land, auch wenn die App Deutsch anzeigt.",
                f"Öffne {EST} und setze das Ziel auf Deutschland, bevor du internationale Fracht zahlst. Der Schätzer entscheidet die SKU, nicht dieser Hostname.",
            ]),
            (f"Preise in {ccy}", [
                f"Die Karten auf dieser Seite zeigen Finds in {ccy}. Du zahlst auf {OFF} — Karte, PayPal oder Guthaben, je nachdem, was das Konto an dem Morgen anbietet.",
                f"Steht in der offiziellen App noch ein Dollarzeichen, gilt die Zahl in der App und der Rechner {EST} mit Ziel Deutschland. Diese Seite ist keine Kasse.",
            ]),
            ("Taobao-, 1688- oder Weidian-Link einfügen", [
                f"Kopiere die Produkt-URL aus dem chinesischen Shop, füge sie auf {OFF} ein. BBDBuy kauft in dein Lager. {host} ist das Spreadsheet und die Anleitung für den Weg zu einer deutschen Tür.",
                "Sneaker, Hoodies, Jacken und Taschen stehen meist in der Liste, weil diese SKUs noch QC-Winkel haben. Elektronik, Parfum und Flüssigkeiten bleiben draußen, bis die App sie am Versandmorgen erlaubt.",
            ]),
            ("QC-Fotos, dann DHL oder Deutsche Post", [
                f"Warte auf Lagerfotos in der App. Extra-Winkel sind oft kostenpflichtig. Erst nach akzeptiertem QC buchst du die internationale Linie. Letzte Meile oft {post}. Packstation geht, wenn die SKU sie anbietet — das ist kein AT-Briefkasten.",
                f"Zwei Zahlungen sind normal: Ware nach China, dann Porto. Lagerdauer steht in der Help auf {OFF} — lies sie am Versandtag, nicht in einem alten Forumspost.",
            ]),
            ("Abgaben", [
                f"Wer Zoll, Einfuhrumsatzsteuer und Nachnahme zahlt, steht auf der gebuchten SKU. {post} kann Gebühren kassieren, die der Schätzer nicht zeigt. Quelle am Versandmorgen: {curl} ({customs}). Diese Seite nennt keinen Satz und keinen Deklarationsbetrag.",
            ]),
        ],
        "es": [
            ("Dirección de entrega en España", [
                f"En la etiqueta van calle española y {city}. Un code postal francés de cinco cifras o un CAP italiano es el país equivocado, aunque la app esté en español.",
                f"En {EST} elige destino España antes de pagar el flete internacional. Canarias, Ceuta o Melilla pueden ser otro producto de transportista — no copies la SKU de la península. Elige la línea viva en la app.",
            ]),
            (f"Precios en {ccy}", [
                f"Los finds de esta página se muestran en {ccy}. Pagas en {OFF} — tarjeta, PayPal o saldo, lo que ofrezca la cuenta ese día.",
                f"Si la SPA oficial sigue con un símbolo de dólar, fíate del número en la app y de la calculadora {EST} con destino España. Esta página no cobra.",
            ]),
            ("Pega un enlace de Taobao, 1688 o Weidian", [
                f"Copia la URL de la tienda china y pégala en {OFF}. BBDBuy compra al almacén. {host} es el spreadsheet y la guía hacia una puerta en España.",
                "Zapatillas, sudaderas, cazadoras y bolsos suelen tener fotos QC. Electrónica, perfume y líquidos se quedan fuera hasta que la app los permita la mañana del envío.",
            ]),
            ("Fotos QC, luego Correos", [
                f"Espera las fotos de almacén en la app. Ángulos extra suelen ser de pago. Cuando aceptas el QC, reservas la línea internacional. Última milla a menudo {post}.",
                f"Hay dos pagos: mercancía a China, luego flete. Los días de almacén están en la Help de {OFF} — léelos el día que envías.",
            ]),
            ("Aduana", [
                f"Quién paga aranceles, IVA de importación y Collect lo decide la SKU reservada. {post} puede añadir un recargo que el estimador no enseña. Fuente el día del envío: {curl} ({customs}). Esta página no inventa un tipo ni un valor declarado.",
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
                f"Collez l’URL sur {OFF}. BBDBuy achète vers l’entrepôt, puis vous réservez la ligne vers la France.",
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
                f"Sull’etichetta servono una via italiana e {city}. Un código español o un code postal francese è il paese sbagliato, anche se l’app è in italiano.",
                f"In {EST} scegli destinazione Italia prima di pagare il nolo internazionale. Una Packstation tedesca non è un CAP italiano.",
            ]),
            (f"Prezzi in {ccy}", [
                f"I finds di questa pagina sono in {ccy}. Paghi su {OFF} — carta, PayPal o saldo, quello che l’account offre quella mattina.",
                f"Se la SPA ufficiale mostra ancora il dollaro, vale la cifra in app e il calcolatore {EST} con destinazione Italia. Questa pagina non è cassa.",
            ]),
            ("Incolla un link Taobao, 1688 o Weidian", [
                f"Copia l’URL dal negozio cinese e incollalo su {OFF}. BBDBuy compra in magazzino. {host} è lo spreadsheet e la guida verso una porta in Italia.",
                "Sneaker, felpe, giacche e borse hanno di solito foto QC. Elettronica, profumi e liquidi restano fuori finché l’app non li consente il mattino della spedizione.",
            ]),
            ("Foto QC, poi Poste Italiane", [
                f"Aspetta le foto di magazzino in app. Angoli extra spesso a pagamento. Dopo il QC prenoti la linea internazionale. Ultimo miglio spesso {post} o un corriere della SKU, non DHL Germania.",
                f"Due pagamenti: merce in Cina, poi nolo. I giorni di magazzino sono nella Help di {OFF} — leggili il giorno della spedizione.",
            ]),
            ("Dogana", [
                f"Chi paga dazi, IVA all’importazione e Collect lo decide la SKU prenotata. {post} può aggiungere un costo che il calcolatore non mostra. Fonte il mattino della spedizione: {curl} ({customs}). Questa pagina non inventa un’aliquota né un valore dichiarato.",
            ]),
        ],
        "nl": [
            ("Bezorgadres in Nederland", [
                f"Op het label horen een Nederlandse straat en {city}. Een Duits Packstation-nummer of een Belgische viercijferige postcode is het verkeerde land, ook als de app Nederlands toont.",
                f"Kies in {EST} bestemming Nederland vóór je internationale vracht betaalt. De SKU komt uit de calculator, niet van deze hostname.",
            ]),
            (f"Prijzen in {ccy}", [
                f"Finds op deze pagina staan in {ccy}. Betalen doe je op {OFF} — kaart, PayPal, saldo of iDEAL, wat het account die ochtend aanbiedt. iDEAL bevestig je in de officiële app, niet op {host}.",
                f"Staat in de SPA nog een dollarteken, dan geldt het bedrag in de app en de calculator {EST} met bestemming Nederland. Deze pagina is geen kassa.",
            ]),
            ("Plak een Taobao-, 1688- of Weidian-link", [
                f"Kopieer de product-URL uit de Chinese shop en plak die op {OFF}. BBDBuy koopt naar het magazijn. {host} is de spreadsheet en de handleiding naar een Nederlandse deur.",
                "Sneakers, hoodies, jassen en tassen hebben meestal QC-foto’s. Elektronica, parfum en vloeistoffen blijven eraf tot de app ze de ochtend van verzending toestaat.",
            ]),
            ("QC-foto’s, dan PostNL of DHL", [
                f"Wacht op magazijnfoto’s in de app. Extra hoeken zijn vaak betaald. Pas na QC boek je de internationale lijn. Last-mile vaak {post}.",
                f"Twee betalingen: goederen naar China, daarna vracht. Magazijndagen staan in de Help op {OFF} — lees ze op de verzenddag, niet in een oude forumpost.",
            ]),
            ("Douane", [
                f"Wie invoerrechten, btw bij invoer en Collect betaalt, staat op de geboekte SKU. {post} kan een toeslag innen die de calculator niet toont. Bron die ochtend: {curl} ({customs}). Deze pagina verzint geen tarief en geen aangegeven waarde.",
            ]),
        ],
        "pl": [
            ("Adres dostawy w Polsce", [
                f"Na etykiecie potrzebna jest polska ulica i {city}. Niemiecki numer Packstation albo czeski kod to złe państwo, nawet gdy aplikacja jest po polsku.",
                f"W {EST} wybierz destination Poland zanim zapłacisz fracht międzynarodowy. SKU pochodzi z kalkulatora, nie z tej domeny.",
            ]),
            (f"Ceny w {ccy}", [
                f"Finds na tej stronie są w {ccy}. Płacisz na {OFF} — karta, PayPal albo saldo, to co konto oferuje tego ranka. BLIK potwierdzasz w oficjalnej aplikacji, nie na {host}.",
                f"Jeśli SPA nadal pokazuje dolar, obowiązuje kwota w aplikacji i kalkulator {EST} z celem Polska. Ta strona nie jest kasą.",
            ]),
            ("Wklej link Taobao, 1688 albo Weidian", [
                f"Skopiuj URL ze sklepu chińskiego i wklej na {OFF}. BBDBuy kupuje do magazynu. {host} to spreadsheet i przewodnik do drzwi w Polsce.",
                "Sneakersy, bluzy, kurtki i torby zwykle mają zdjęcia QC. Elektronika, perfumy i płyny zostają poza listą, dopóki aplikacja nie pozwoli rano wysyłki.",
            ]),
            ("Zdjęcia QC, potem InPost albo Poczta", [
                f"Poczekaj na zdjęcia magazynowe w aplikacji. Dodatkowe kąty często płatne. Po QC rezerwujesz linię międzynarodową. Last-mile często {post}.",
                f"Dwie płatności: towar do Chin, potem fracht. Dni magazynu są w Help na {OFF} — czytaj w dniu wysyłki.",
            ]),
            ("Cło", [
                f"Kto płaci cło, VAT importowy i Collect, decyduje zarezerwowana SKU. {post} może doliczyć opłatę, której kalkulator nie pokazuje. Źródło rano: {curl} ({customs}). Ta strona nie wymyśla stawki ani wartości zgłoszonej.",
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
                f"No. Use a US ZIP — {city}. Destination United States in {EST}. A Canadian A1A 1A1 code is the wrong estimator country.",
            ]),
            ("Where do I pay?", [
                f"On {OFF}. {host} shows finds in USD; last mile is often {post}.",
                f"Live freight is the calculator {EST} with destination United States, not a Discord screenshot.",
            ]),
            ("When do I book freight?", [
                f"After QC photos. {post} will not retake a warehouse photo once the carton is in the United States.",
                f"Storage days are in Help on {OFF}. Read them the morning you ship.",
            ]),
            ("Who pays duty?", [
                f"The booked SKU. {post} can add Collect that the estimator does not show.",
                f"Read {curl} ({customs}) the morning you ship. This page does not invent a de-minimis dollar or a declared value.",
            ]),
            ("Are English keys (sneakers, hoodie) a Canada shop?", [
                "No. The category wall is English because the index is English. Searching «hoodies» in another language often returns zero cards.",
                "Estimator country stays the United States. Those keys do not change CBP or last-mile.",
            ]),
            ("Two payments — is that an error?", [
                "No. Goods to China first, international freight after QC. Two receipts in the app are normal.",
                f"If the app charges once, the app wins. {OFF}.",
            ]),
            ("Must I use this spreadsheet?", [
                f"No. You can search the official app. The sheet saves dead Weidian cards toward a US door.",
                f"{host} does not see the account. Register only on {OFF}.",
            ]),
            ("Is a Canadian mailbox the same SKU?", [
                f"No. A Canadian postal code is another country in the estimator. {city} is the address test for this desk.",
                f"Confirm destination United States in {EST} the morning you ship.",
            ]),
        ],
        "ca": [
            ("Can I use a US ZIP?", [
                f"No. Use a Canadian postal code — {city}. Destination Canada in {EST}. A US ZIP is the wrong estimator country.",
            ]),
            ("Where do I pay?", [
                f"On {OFF}. Last mile is often {post}. Display currency on this page is CAD.",
            ]),
            ("When do I book freight?", [
                f"After QC photos. Storage days are in Help on {OFF}.",
            ]),
            ("Who pays duty?", [
                f"The booked SKU. Read {curl} ({customs}). This page does not invent a de-minimis dollar or a declared value.",
            ]),
            ("Are English keys (sneakers, hoodie) a US shop?", [
                "No. The category wall is English because the index is English. Canadian words often return zero cards.",
                "Estimator country stays Canada. Those keys do not change CBSA or last-mile.",
            ]),
            ("Two payments — is that an error?", [
                "No. Goods to China first, international freight after QC. Two receipts in the app are normal.",
                f"If the app charges once, the app wins. {OFF}.",
            ]),
            ("Must I use this spreadsheet?", [
                f"No. You can search the official app. The sheet saves dead Weidian cards toward a Canadian door.",
                f"{host} does not see the account. Register only on {OFF}.",
            ]),
            ("Is a US mailbox the same SKU?", [
                f"No. A US ZIP is another country in the estimator. {city} is the address test for this desk.",
                f"Confirm destination Canada in {EST} the morning you ship.",
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
                f"Nein. Deutschland braucht {city}. 1010 Wien und vierstellige AT-PLZ sind Österreich — falsches Schätzerland, auch wenn die App Deutsch ist.",
                f"Packstation-Nummern sind ein DE-Muster. Letzte Meile oft {post}. Ziel Deutschland in {EST} wählen.",
            ]),
            ("Wo zahle ich?", [
                f"Nur auf {OFF}. {host} zeigt Finds in Euro, nimmt aber keine Karte, kein PayPal und kein Guthaben.",
                f"Live-Fracht steht im Rechner {EST} mit Ziel Deutschland, nicht in einem Screenshot aus einem Forum.",
            ]),
            ("Wann buche ich Fracht?", [
                f"Erst nach akzeptierten QC-Fotos in der App. {post} macht keine Nachaufnahme, sobald der Karton in Deutschland ist.",
                f"Lagerdauer steht in der Help auf {OFF}. Lies sie am Versandtag.",
            ]),
            ("Wer zahlt Zoll und Einfuhrumsatzsteuer?", [
                f"Die gebuchte SKU. {post} kann Collect-Gebühren addieren, die der Schätzer nicht zeigt.",
                f"Quelle am Versandmorgen: {curl} ({customs}). Diese Seite nennt keinen Satz und keinen Deklarationsbetrag.",
            ]),
            ("Sind englische Keys (sneakers, hoodie) ein US-Shop?", [
                "Nein. Die Kategorie-Wand ist englisch, weil der Index englisch ist. Deutsche Wörter liefern oft null Karten.",
                "Das Schätzerland bleibt Deutschland. Die Keys ändern weder Zoll noch letzte Meile.",
            ]),
            ("Kann ich eine österreichische Packstation umgehen, indem ich DE wähle?", [
                f"Nein. Die Tür auf dem Label muss zu Deutschland passen. AT-Post ist ein anderer Desk.",
                f"Packstation hier nur, wenn die SKU sie für DE anbietet. Sonst Straße und fünfstellige PLZ.",
            ]),
            ("Zwei Zahlungen — ist das ein Fehler?", [
                "Nein. Zuerst Ware nach China, nach QC die internationale Fracht. Zwei Kassenbelege in der App sind normal.",
                f"Wenn die App nur eine Zahlung zeigt, gilt die App, nicht dieser Text. {OFF}.",
            ]),
            ("Muss ich dieses Spreadsheet nutzen?", [
                f"Nein. Du kannst in der offiziellen App suchen. Das Sheet spart tote Weidian-Karten für eine deutsche Tür.",
                f"{host} sieht das Konto nicht. Register nur auf {OFF}.",
            ]),
        ],
        "es": [
            ("¿Puedo usar un code postal francés?", [
                f"No. España necesita {city}. Un code postal francés o un CAP italiano es el país equivocado, aunque la app esté en español.",
                f"Última milla a menudo {post}. Destino España en {EST}.",
            ]),
            ("¿Dónde pago?", [
                f"Solo en {OFF}. {host} enseña finds en euros, no cobra tarjeta ni PayPal.",
                f"El flete vivo está en {EST} con destino España, no en una captura de un foro.",
            ]),
            ("¿Cuándo reservo el flete?", [
                f"Después de aceptar las fotos QC en la app. {post} no rehace la foto de almacén cuando el cartón ya está en España.",
                f"Los días de almacén están en la Help de {OFF}. Léelos el día del envío.",
            ]),
            ("¿Quién paga aduana e IVA de importación?", [
                f"La SKU reservada. {post} puede añadir Collect que el estimador no enseña.",
                f"Fuente el día del envío: {curl} ({customs}). Esta página no inventa un tipo ni un valor declarado.",
            ]),
            ("¿Las claves inglesas (sneakers, hoodie) son una tienda US?", [
                "No. El muro de categorías está en inglés porque el índice está en inglés. «Zapatillas» o «sudadera» suelen devolver cero fichas.",
                "El país del estimador sigue siendo España. Esas claves no cambian aduana ni última milla.",
            ]),
            ("¿Canarias, Ceuta o Melilla usan la misma SKU que Madrid?", [
                "A menudo no. Son otra puerta. Elige la línea viva en la app; no copies el producto de la península.",
                f"Confirma destino España (o el territorio que corresponda) en {EST} la mañana que envías.",
            ]),
            ("¿Dos pagos son un error?", [
                "No. Primero la mercancía a China, después el flete internacional. Dos recibos en la app son normales.",
                f"Si la app muestra un solo cobro, vale la app. Pedidos en {OFF}.",
            ]),
            ("¿Hace falta este spreadsheet?", [
                f"No. Puedes buscar en la app oficial. El índice evita miles de enlaces Weidian muertos hacia una puerta en España.",
                f"{host} no ve la cuenta. Registro solo en {OFF}.",
            ]),
        ],
        "fr": [
            ("Puis-je mettre un code belge ?", [
                f"Non. France — {city}. Un code postal belge à quatre chiffres est le mauvais pays. Dernier km souvent {post}.",
                f"Destination France dans {EST}. Un código español n’est pas cette page.",
            ]),
            ("Où payer ?", [
                f"Sur {OFF}. {host} montre des finds en euro ; la caisse, le portefeuille et les tickets restent sur le site officiel.",
                f"Fret live : calculateur {EST} destination France.",
            ]),
            ("Quand réserver le fret ?", [
                f"Après les photos QC dans l’app. {post} ne refait pas une photo d’entrepôt une fois le carton en France.",
                f"Durée d’entrepôt dans la Help de {OFF}. Lis-la le matin de l’envoi.",
            ]),
            ("Qui paie la douane ?", [
                f"La SKU réservée. {post} peut ajouter un Collect que l’estimateur ne montre pas.",
                f"Source : {curl} ({customs}). Cette page n’invente pas de taux ni de valeur déclarée.",
            ]),
            ("Les clés anglaises (sneakers, hoodie) sont-elles une boutique BE ?", [
                "Non. Le mur catégories est anglais parce que l’index est anglais. « Baskets » ou « sweat » donnent souvent zéro carte.",
                "Le pays de l’estimateur reste la France. Ces clés ne changent ni la douane ni le dernier km.",
            ]),
            ("Deux paiements — c’est une erreur ?", [
                "Non. Marchandise vers la Chine d’abord, fret international après QC. Deux reçus dans l’app sont normaux.",
                f"Si l’app facture une seule fois, l’app gagne. {OFF}.",
            ]),
            ("Faut-il ce spreadsheet ?", [
                f"Non. Tu peux chercher dans l’app officielle. La feuille évite les cartes Weidian mortes vers une porte en France.",
                f"{host} ne voit pas le compte. Inscription seulement sur {OFF}.",
            ]),
            ("Une boîte belge, c’est la même SKU ?", [
                f"Non. Un code belge à quatre chiffres est un autre pays dans l’estimateur. {city} est le test d’adresse de ce desk.",
                f"Confirme destination France dans {EST} le matin de l’envoi.",
            ]),
        ],
        "it": [
            ("Posso usare un código español?", [
                f"No. L’Italia vuole {city}. Un código español o un code postal francese è il paese sbagliato, anche se l’app è in italiano.",
                f"Ultimo miglio spesso {post}. Destinazione Italia in {EST}. Una Packstation tedesca non sostituisce il CAP.",
            ]),
            ("Dove pago?", [
                f"Solo su {OFF}. {host} mostra finds in euro, non prende carta né PayPal.",
                f"Il nolo live è nel calcolatore {EST} con destinazione Italia, non in uno screenshot da forum.",
            ]),
            ("Quando prenoto il nolo?", [
                f"Dopo le foto QC accettate in app. {post} non rifà la foto di magazzino a cartone già in Italia.",
                f"I giorni di magazzino sono nella Help di {OFF}. Leggili il giorno della spedizione.",
            ]),
            ("Chi paga dazi e IVA all’importazione?", [
                f"La SKU prenotata. {post} può aggiungere Collect che il calcolatore non mostra.",
                f"Fonte il mattino della spedizione: {curl} ({customs}). Questa pagina non inventa un’aliquota né un valore dichiarato.",
            ]),
            ("Le chiavi inglesi (sneakers, hoodie) sono un negozio US?", [
                "No. Il muro categorie è in inglese perché l’indice è in inglese. «Scarpe» o «felpa» spesso danno zero schede.",
                "Il paese del calcolatore resta Italia. Quelle chiavi non cambiano dogana né ultimo miglio.",
            ]),
            ("Due pagamenti sono un errore?", [
                "No. Prima la merce in Cina, poi il nolo internazionale. Due ricevute in app sono normali.",
                f"Se l’app mostra un solo addebito, vale l’app. Ordini su {OFF}.",
            ]),
            ("Devo usare questo spreadsheet?", [
                f"No. Puoi cercare nell’app ufficiale. Lo sheet evita migliaia di link Weidian morti verso una porta in Italia.",
                f"{host} non vede l’account. Registrazione solo su {OFF}.",
            ]),
            ("Posso scrivere un indirizzo GLS inventato?", [
                f"No. Serve una via e un {city} reali. Il corriere lo decide la SKU, non un nickname da forum.",
                f"Scegli la linea viva in {EST} con destinazione Italia.",
            ]),
        ],
        "nl": [
            ("Mag ik een Packstation gebruiken?", [
                f"Nee. Nederland wil {city}. Een Duits Packstation-nummer is het verkeerde land, ook als de app Nederlands is.",
                f"Last-mile vaak {post}. Bestemming Nederland in {EST}.",
            ]),
            ("Waar betaal ik?", [
                f"Alleen op {OFF}. {host} toont finds in euro, neemt geen kaart en geen PayPal. iDEAL bevestig je in de officiële app.",
                f"Live vracht staat in {EST} met bestemming Nederland, niet op een forum-screenshot.",
            ]),
            ("Wanneer boek ik vracht?", [
                f"Pas na geaccepteerde QC-foto’s in de app. {post} maakt geen heropname als de doos al in Nederland is.",
                f"Magazijndagen staan in de Help op {OFF}. Lees ze op de verzenddag.",
            ]),
            ("Wie betaalt invoerrechten en btw bij invoer?", [
                f"De geboekte SKU. {post} kan Collect bijtellen die de calculator niet toont.",
                f"Bron die ochtend: {curl} ({customs}). Deze pagina verzint geen tarief en geen aangegeven waarde.",
            ]),
            ("Zijn Engelse keys (sneakers, hoodie) een US-shop?", [
                "Nee. De categorie-muur is Engels omdat de index Engels is. Nederlandse woorden geven vaak 0 kaarten.",
                "Het calculatorland blijft Nederland. Die keys veranderen douane noch last-mile.",
            ]),
            ("Mag ik een Belgische postcode plakken?", [
                "Nee. Vier cijfers zonder letters is vaak België. NL is 1234 AB. Verkeerd land in de estimator is een andere SKU.",
                f"Bevestig bestemming Nederland in {EST}.",
            ]),
            ("Twee betalingen — is dat een fout?", [
                "Nee. Eerst goederen naar China, na QC de internationale vracht. Twee bonnen in de app zijn normaal.",
                f"Toont de app één betaling, dan geldt de app. Bestellen op {OFF}.",
            ]),
            ("Moet ik deze spreadsheet gebruiken?", [
                f"Nee. Je kunt in de officiële app zoeken. Het sheet spaart dode Weidian-kaarten voor een Nederlandse deur.",
                f"{host} ziet het account niet. Registreren alleen op {OFF}.",
            ]),
        ],
        "pl": [
            ("Czy mogę użyć Packstation?", [
                f"Nie. Polska chce {city}. Niemiecki numer Packstation to złe państwo, nawet gdy aplikacja jest po polsku.",
                f"Last-mile często {post}. Destination Poland w {EST}.",
            ]),
            ("Gdzie płacę?", [
                f"Tylko na {OFF}. {host} pokazuje finds w złotych, nie bierze karty ani PayPal. BLIK potwierdzasz w oficjalnej aplikacji.",
                f"Live fracht jest w {EST} z celem Polska, nie na zrzucie z forum.",
            ]),
            ("Kiedy rezerwuję fracht?", [
                f"Dopiero po zaakceptowanych zdjęciach QC w aplikacji. {post} nie robi powtórki magazynowej, gdy karton jest już w Polsce.",
                f"Dni magazynu są w Help na {OFF}. Czytaj w dniu wysyłki.",
            ]),
            ("Kto płaci cło i VAT importowy?", [
                f"Zarezerwowana SKU. {post} może doliczyć Collect, którego kalkulator nie pokazuje.",
                f"Źródło rano: {curl} ({customs}). Ta strona nie wymyśla stawki ani wartości zgłoszonej.",
            ]),
            ("Czy angielskie klucze (sneakers, hoodie) to sklep US?", [
                "Nie. Ściana kategorii jest po angielsku, bo indeks jest po angielsku. Polskie słowa często dają 0 kart.",
                "Kraj kalkulatora zostaje Polska. Te klucze nie zmieniają cła ani last-mile.",
            ]),
            ("Czy mogę wkleić czeski kod pocztowy?", [
                "Nie. Inny format to często inne państwo i inna SKU w kalkulatorze.",
                f"Potwierdź destination Poland w {EST}. Test etykiety: {city}.",
            ]),
            ("Dwie płatności — to błąd?", [
                "Nie. Najpierw towar do Chin, po QC fracht międzynarodowy. Dwa paragony w aplikacji są normalne.",
                f"Jeśli aplikacja pokazuje jedną płatność, obowiązuje aplikacja. Zamówienia na {OFF}.",
            ]),
            ("Czy muszę używać tego spreadsheet?", [
                f"Nie. Możesz szukać w oficjalnej aplikacji. Arkusz oszczędza martwe karty Weidian do drzwi w Polsce.",
                f"{host} nie widzi konta. Rejestracja tylko na {OFF}.",
            ]),
        ],
    }
    return q[key]


def more_depth(d: dict, host: str) -> list:
    """Extra local H2s for dests below the UK word bar. Unique copy, not a locale swap."""
    post, city, customs, curl, ccy = d["post"], d["city"], d["customs"], d["customs_url"], d["ccy"]
    key = d["key"]
    packs = {
        "uk": [
            ("Warehouse in China, not a Royal Mail depot", [
                f"QC photos are taken in the BBDBuy warehouse in China. A {post} depot in the UK is last-mile, not a second QC studio. Ask for extra angles in the app before you pay freight to the United Kingdom.",
                f"Storage days are in official Help on {OFF}. This page does not invent free extra days. After QC, open {EST} with destination United Kingdom. {city}.",
            ]),
            ("First order: one clothing SKU", [
                f"For the first UK door, one hoodie or a pair of sneakers with warehouse photos is enough. Consolidating un-QCd pieces on the first invoice mixes {customs} and Collect.",
                f"Restricted, perfume, batteries and liquids stay off until the app allows them the morning you ship. {host} lists finds; the block is in the app.",
            ]),
            ("English catalogue keys are labels", [
                "The category wall says sneakers, hoodie, jacket, bag because the index is English. Local words often return zero cards — that is not an empty shop.",
                f"Those keys do not change customs or last-mile. Estimator country stays the United Kingdom, {ccy} is display, checkout is {OFF}.",
            ]),
            ("What this hostname is not", [
                f"{host} is a spreadsheet and guide toward a UK door. It is not a second BBDBuy till, not {customs}, not {post} customer service. Register and tickets only on {OFF}.",
                "Northern Ireland is often another carrier product. Do not assume the same Royal Mail SKU as mainland GB.",
            ]),
            ("Tracking after the border", [
                f"While the SKU is in China you see warehouse status in the app. After the international line, tracking follows the SKU — often {post}. Collect can appear at the door.",
                f"Who pays import VAT and Collect is the booked SKU. Source the morning you ship: {curl} ({customs}). This page does not paste a rate into the title or invent a declared value.",
            ]),
            ("Returns only in the warehouse", [
                f"Fail-QC or a wrong size is handled in-app while the piece is in China. After {post} delivered, {customs} does not reopen a warehouse ticket.",
                f"Two payments stay normal: goods to China, then freight. If the app charges once, the app wins. {OFF}.",
            ]),
            ("Neighbour countries are other SKUs", [
                f"{city} is the address test for this desk. An EU code postal in the estimator is the wrong country.",
                f"A ranked VAT article on {host} is not a live tariff. Confirm in the app and on HMRC the day you ship, then book the line.",
            ]),
        ],
        "us": [
            ("Warehouse in China, not a USPS depot", [
                f"QC photos are taken in the BBDBuy warehouse in China. A {post} depot in the United States is last-mile, not a second QC studio. Ask for extra angles in the app before you pay freight to the United States.",
                f"Storage days are in official Help on {OFF}. This page does not invent free extra days. After QC, open {EST} with destination United States. {city}.",
            ]),
            ("First order: one clothing SKU", [
                f"For the first US door, one hoodie or a pair of sneakers with warehouse photos is enough. Consolidating un-QCd pieces on the first invoice mixes {customs} and Collect.",
                f"Restricted, perfume, batteries and liquids stay off until the app allows them the morning you ship. {host} lists finds; the block is in the app.",
            ]),
            ("English catalogue keys are labels", [
                "The category wall says sneakers, hoodie, jacket, bag because the index is English. Local words often return zero cards — that is not an empty shop.",
                f"Those keys do not change customs or last-mile. Estimator country stays the United States, {ccy} is display, checkout is {OFF}.",
            ]),
            ("What this hostname is not", [
                f"{host} is a spreadsheet and guide toward a US door. It is not a second BBDBuy till, not {customs}, not {post} customer service. Register and tickets only on {OFF}.",
                "A Canadian postal code in the A1A 1A1 pattern is the wrong country. Do not assume the same USPS SKU as a Canada Post line.",
            ]),
            ("Tracking after the border", [
                f"While the SKU is in China you see warehouse status in the app. After the international line, tracking follows the SKU — often {post} or FedEx. Collect can appear at the door.",
                f"Who pays duty and Collect is the booked SKU. Source the morning you ship: {curl} ({customs}). This page does not paste a rate into the title or invent a declared value.",
            ]),
            ("Returns only in the warehouse", [
                f"Fail-QC or a wrong size is handled in-app while the piece is in China. After {post} delivered, {customs} does not reopen a warehouse ticket.",
                f"Two payments stay normal: goods to China, then freight. If the app charges once, the app wins. {OFF}.",
            ]),
            ("Neighbour countries are other SKUs", [
                f"{city} is the address test for this desk. A Canadian A1A 1A1 code in the estimator is the wrong country.",
                f"A ranked duty article on {host} is not a live tariff. Confirm in the app and on CBP the day you ship, then book the line.",
            ]),
        ],
        "ca": [
            ("Warehouse in China, not a Canada Post depot", [
                f"QC photos are taken in the BBDBuy warehouse in China. A {post} depot in Canada is last-mile, not a second QC studio. Ask for extra angles in the app before you pay freight to Canada.",
                f"Storage days are in official Help on {OFF}. This page does not invent free extra days. After QC, open {EST} with destination Canada. {city}.",
            ]),
            ("First order: one clothing SKU", [
                f"For the first Canadian door, one hoodie or a pair of sneakers with warehouse photos is enough. Consolidating un-QCd pieces on the first invoice mixes {customs} and Collect.",
                f"Restricted, perfume, batteries and liquids stay off until the app allows them the morning you ship. {host} lists finds; the block is in the app.",
            ]),
            ("English catalogue keys are labels", [
                "The category wall says sneakers, hoodie, jacket, bag because the index is English. Canadian words often return zero cards — that is not an empty shop.",
                f"Those keys do not change customs or last-mile. Estimator country stays Canada, {ccy} is display, checkout is {OFF}.",
            ]),
            ("What this hostname is not", [
                f"{host} is a spreadsheet and guide toward a Canadian door. It is not a second BBDBuy till, not {customs}, not {post} customer service. Register and tickets only on {OFF}.",
                "A US ZIP is the wrong country. Do not assume the same Canada Post SKU as a USPS line.",
            ]),
            ("Tracking after the border", [
                f"While the SKU is in China you see warehouse status in the app. After the international line, tracking follows the SKU — often {post}. Collect can appear at the door.",
                f"Who pays GST/HST on import and Collect is the booked SKU. Source the morning you ship: {curl} ({customs}). This page does not paste a rate into the title or invent a declared value.",
            ]),
            ("Returns only in the warehouse", [
                f"Fail-QC or a wrong size is handled in-app while the piece is in China. After {post} delivered, {customs} does not reopen a warehouse ticket.",
                f"Two payments stay normal: goods to China, then freight. If the app charges once, the app wins. {OFF}.",
            ]),
            ("Neighbour countries are other SKUs", [
                f"{city} is the address test for this desk. A US ZIP in the estimator is the wrong country.",
                f"A ranked duty article on {host} is not a live tariff. Confirm in the app and on CBSA the day you ship, then book the line.",
            ]),
        ],
        "at": [],
        "fr": [
            ("Entrepôt en Chine, pas un dépôt Colissimo", [
                f"Les photos QC se font dans l’entrepôt BBDBuy en Chine. Un dépôt de {post} en France est le dernier km, pas un second studio QC. Demandez des angles extra dans l’app avant de payer le fret vers la France.",
                f"La durée d’entrepôt est dans la Help de {OFF}. Cette page n’invente pas de jours gratuits. Après QC, {EST} destination France. {city}.",
            ]),
            ("Première commande : une SKU vêtement", [
                f"Pour la première porte en France, un hoodie ou une paire de baskets avec photos suffit. Consolider des pièces sans QC mélange {customs} et Collect.",
                f"Restricted, parfum, batteries et liquides restent dehors tant que l’app ne les autorise pas le matin de l’envoi. {host} liste les finds ; le blocage est dans l’app.",
            ]),
            ("Les clés anglaises sont des étiquettes", [
                "Le mur catégories dit sneakers, hoodie, jacket, bag parce que l’index est anglais. « Baskets » ou « sweat » donnent souvent zéro carte.",
                f"Ces clés ne changent ni la douane ni le dernier km. Pays estimateur = France, {ccy} = affichage, caisse = {OFF}.",
            ]),
            ("Ce que cet hôte n’est pas", [
                f"{host} est spreadsheet et guide vers une porte en France. Pas une seconde caisse BBDBuy, pas {customs}, pas le SAV {post}. Inscription et tickets seulement sur {OFF}.",
                "Un code postal belge à quatre chiffres est le mauvais pays. Pas un código español non plus.",
            ]),
            ("Suivi après la douane", [
                f"Tant que la SKU est en Chine, le statut entrepôt est dans l’app. Après la ligne internationale, le tracking suit la SKU — souvent {post}. Collect peut apparaître à la porte.",
                f"Qui paie droits, TVA à l’importation et Collect = la SKU. Source le matin : {curl} ({customs}). Cette page n’invente pas de taux ni de valeur déclarée.",
            ]),
            ("Retour seulement en entrepôt", [
                f"Fail-QC ou mauvaise taille se règlent in-app tant que la pièce est en Chine. Si {post} a livré, {customs} ne rouvre pas un ticket entrepôt.",
                f"Deux paiements restent normaux. Si l’app n’en montre qu’un, l’app gagne. {OFF}.",
            ]),
            ("Voisins = autres SKU", [
                f"{city} est le test d’étiquette de ce desk. Un code belge est une autre ligne.",
                f"Un article douane classé sur {host} n’est pas un tarif live. Confirmez dans l’app et sur douane.gouv.fr le jour de l’envoi.",
            ]),
        ],
        "de": [
            ("Lager in China, nicht in Frankfurt", [
                f"QC-Fotos entstehen im chinesischen BBDBuy-Lager, solange die SKU dort liegt. Ein DHL-Hub in Deutschland ist Last-Mile, kein zweites QC-Studio. Extra-Winkel buchst du in der App, bevor du die Linie nach Deutschland zahlst — nicht, wenn {post} den Karton schon hat.",
                f"Lagerdauer steht in der offiziellen Help auf {OFF}. Diese Seite erfindet keine kostenlosen Extra-Tage. Nach akzeptiertem QC öffnest du {EST} mit Ziel Deutschland. {city}.",
            ]),
            ("Erste Bestellung: eine Kleidungs-SKU", [
                f"Für die erste Tür nach Deutschland reicht eine Hoodie- oder Sneaker-SKU mit Lagerfotos. Konsolidieren mehrerer ungeprüfter Teile auf der ersten Rechnung macht {customs} und Collect unübersichtlich.",
                f"Restricted, Parfum, Akkus und Flüssigkeiten bleiben draußen, bis die App sie am Versandmorgen erlaubt. {host} listet Finds; die Sperre steht in der App, nicht in diesem HTML.",
            ]),
            ("Englische Katalog-Keys sind Anzeige", [
                "Die Kategorie-Wand spricht sneakers, hoodie, jacket, bag, weil der Index englisch ist. Deutsche Wörter wie Turnschuhe oder Kapuzenpullover liefern oft null Karten — das ist kein leerer Shop.",
                f"Die Keys ändern weder Zollland noch letzte Meile. Schätzerland bleibt Deutschland, Währung {ccy} nur Anzeige, Kasse {OFF}.",
            ]),
            ("Was dieser Hostname nicht ist", [
                f"{host} ist Spreadsheet und Anleitung für eine deutsche Tür. Es ist keine zweite BBDBuy-Kasse, kein Zollamt und kein DHL-Kundenservice. Register, Guthaben, Tickets nur auf {OFF}.",
                f"Ein Screenshot aus einem AT-Forum mit 1010 Wien oder vierstelliger PLZ gehört nicht in diesen Schätzer. Österreich ist ein eigener Desk. Packstation hier nur, wenn die SKU sie für DE anbietet.",
            ]),
            ("Sendungsverfolgung nach der Grenze", [
                f"Solange die SKU in China ist, siehst du Lagerstatus in der App. Sobald die internationale Linie gebucht ist, folgt die Tracking-Nummer der SKU — oft {post}. Collect-Gebühren können an der Tür erscheinen, die der Schätzer nicht zeigte.",
                f"Wer Einfuhrumsatzsteuer und Nachnahme zahlt, steht auf der gebuchten SKU. Quelle am Versandmorgen: {curl} ({customs}). Diese Seite klebt keinen Euro-Satz in die Überschrift und nennt keinen Deklarationsbetrag.",
            ]),
            ("Retoure nur im Lager", [
                f"Fail-QC oder Falschgröße klärst du in der App, solange das Teil in China liegt. Hat {post} zugestellt, ist {customs} die falsche Adresse für ein Lagerticket.",
                f"Zwei Zahlungen bleiben normal: Ware nach China, nach QC die Fracht. Wenn die App an einem Morgen nur eine Kasse zeigt, gilt die App. {OFF}.",
            ]),
            ("Nachbarländer sind andere SKUs", [
                f"1010 Wien, vierstellige AT-PLZ und österreichische Packstation-Mythen sind das falsche Land, auch wenn die App Deutsch spricht. {city} ist der Adresstest für diesen Desk.",
                f"Ein rankender Zollartikel auf {host} ist kein Live-Tarif. Schwellen ändern sich. Bestätigen in der App und auf zoll.de am Versandtag, dann Linie buchen.",
            ]),
        ],
        "es": [
            ("Almacén en China, no un centro de Correos", [
                f"Las fotos QC se hacen en el almacén de BBDBuy en China. Un centro de {post} en España es última milla, no un segundo estudio QC. Pides ángulos extra en la app antes de pagar el flete a España.",
                f"Los días de almacén están en la Help de {OFF}. Esta página no inventa días gratis. Tras el QC, {EST} con destino España. {city}.",
            ]),
            ("Primer pedido: una SKU de ropa", [
                f"Para la primera puerta en España basta una sudadera o un par de zapatillas con fotos de almacén. Consolidar piezas sin QC en la primera factura mezcla {customs} y Collect.",
                f"Restricted, perfume, baterías y líquidos se quedan fuera hasta que la app los permita el día del envío. {host} lista finds; el bloqueo está en la app.",
            ]),
            ("Las claves inglesas son etiquetas", [
                "El muro de categorías dice sneakers, hoodie, jacket, bag porque el índice está en inglés. «Zapatillas» o «sudadera» suelen devolver cero fichas — no es una tienda vacía.",
                f"Esas claves no cambian aduana ni última milla. El país del estimador sigue siendo España, {ccy} es visualización, la caja es {OFF}.",
            ]),
            ("Qué no es este hostname", [
                f"{host} es spreadsheet y guía hacia una puerta en España. No es una segunda caja BBDBuy, ni la Agencia Tributaria, ni atención de {post}. Registro y tickets solo en {OFF}.",
                "Un code postal francés o un CAP italiano no entra en este estimador. Canarias, Ceuta o Melilla pueden ser otro producto de transportista — elige la línea viva, no copies la SKU de Madrid.",
            ]),
            ("Seguimiento después de aduana", [
                f"Mientras la SKU está en China ves el almacén en la app. Cuando reservas la línea internacional, el tracking sigue la SKU — a menudo {post}. Collect puede aparecer en la puerta.",
                f"Quién paga IVA de importación y Collect lo decide la SKU. Fuente el día del envío: {curl} ({customs}). Esta página no pega un tipo en el título ni inventa un valor declarado.",
            ]),
            ("Devolución solo en almacén", [
                f"Un fail-QC o una talla mal se resuelve en la app mientras la pieza está en China. Si {post} ya entregó, {customs} no reabre un ticket de almacén.",
                f"Dos pagos son normales: mercancía a China, después el flete. Si la app cobra una sola vez, vale la app. {OFF}.",
            ]),
            ("Territorios y vecinos", [
                f"Península, Canarias, Ceuta y Melilla no copian siempre la misma SKU. {city} es la prueba de etiqueta de este desk. Un code postal francés es otro país.",
                f"Un artículo de aduana que rankea en {host} no es un arancel live. Confirma en la app y en la Agencia Tributaria el día que envías.",
            ]),
        ],
        "it": [
            ("Magazzino in Cina, non un ufficio Poste", [
                f"Le foto QC nascono nel magazzino BBDBuy in Cina. Un hub di {post} in Italia è ultimo miglio, non un secondo studio QC. Chiedi angoli extra in app prima di pagare il nolo verso l’Italia.",
                f"I giorni di magazzino sono nella Help di {OFF}. Questa pagina non inventa giorni gratis. Dopo il QC, {EST} con destinazione Italia. {city}.",
            ]),
            ("Primo ordine: una SKU di abbigliamento", [
                f"Per la prima porta in Italia basta una felpa o un paio di sneaker con foto di magazzino. Consolidare pezzi senza QC sulla prima fattura mescola {customs} e Collect.",
                f"Restricted, profumi, batterie e liquidi restano fuori finché l’app non li consente il mattino della spedizione. {host} elenca i finds; il blocco sta nell’app.",
            ]),
            ("Le chiavi inglesi sono etichette", [
                "Il muro categorie dice sneakers, hoodie, jacket, bag perché l’indice è in inglese. «Scarpe» o «felpa» spesso danno zero schede — non è un negozio vuoto.",
                f"Quelle chiavi non cambiano dogana né ultimo miglio. Il paese del calcolatore resta Italia, {ccy} è display, la cassa è {OFF}.",
            ]),
            ("Cosa non è questo hostname", [
                f"{host} è spreadsheet e guida verso una porta in Italia. Non è una seconda cassa BBDBuy, non è ADM, non è il customer care di {post}. Registrazione e ticket solo su {OFF}.",
                "Un código español o un code postal francese non entra in questo calcolatore. Una Packstation tedesca non sostituisce un CAP italiano. Il corriere lo decide la SKU, non un nickname da forum.",
            ]),
            ("Tracking dopo la dogana", [
                f"Finché la SKU è in Cina vedi il magazzino in app. Prenotata la linea internazionale, il tracking segue la SKU — spesso {post} o il partner della linea. Collect può comparire alla porta.",
                f"Chi paga dazi, IVA all’importazione e Collect lo decide la SKU. Fonte il mattino della spedizione: {curl} ({customs}). Questa pagina non incolla un’aliquota nel title e non inventa un valore dichiarato.",
            ]),
            ("Reso solo in magazzino", [
                f"Fail-QC o taglia sbagliata si risolvono in app mentre il pezzo è in Cina. Se {post} ha già consegnato, {customs} non riapre un ticket di magazzino.",
                f"Due pagamenti restano normali: merce in Cina, poi il nolo. Se l’app addebita una volta sola, vale l’app. {OFF}.",
            ]),
            ("Vicini e CAP", [
                f"{city} è il test etichetta di questo desk. Un code postal francese a cinque cifre sembra un CAP, ma è un altro paese e un’altra SKU nel calcolatore.",
                f"Un articolo dogana in ranking su {host} non è un tariffario live. Conferma in app e su ADM il giorno della spedizione, poi prenota la linea.",
            ]),
        ],
        "nl": [
            ("Magazijn in China, geen PostNL-depot", [
                f"QC-foto’s ontstaan in het BBDBuy-magazijn in China. Een depot van {post} in Nederland is last-mile, geen tweede QC-studio. Extra hoeken vraag je in de app vóór je vracht naar Nederland betaalt.",
                f"Magazijndagen staan in de Help op {OFF}. Deze pagina verzint geen gratis extra dagen. Na QC open je {EST} met bestemming Nederland. {city}.",
            ]),
            ("Eerste order: één kleding-SKU", [
                f"Voor de eerste Nederlandse deur volstaat één hoodie of een paar sneakers met magazijnfoto’s. Meerdere ongecheckte stukken op de eerste rekening mengen {customs} en Collect.",
                f"Restricted, parfum, batterijen en vloeistoffen blijven eraf tot de app ze toestaat op de verzenddag. {host} toont finds; de blokkade staat in de app.",
            ]),
            ("Engelse catalogus-keys zijn labels", [
                "De categorie-muur zegt sneakers, hoodie, jacket, bag omdat de index Engels is. Nederlandse woorden zoals schoenen of trui geven vaak 0 kaarten — dat is geen lege shop.",
                f"Die keys veranderen douane noch last-mile. Estimator-land blijft Nederland, {ccy} is weergave, kassa is {OFF}. iDEAL bevestig je in de officiële app, niet op {host}.",
            ]),
            ("Wat deze hostname niet is", [
                f"{host} is spreadsheet en handleiding naar een Nederlandse deur. Het is geen tweede BBDBuy-kassa, geen Douane-loket en geen {post}-klantenservice. Registreren en tickets alleen op {OFF}.",
                "Een Duits Packstation-nummer of een Belgische viercijferige postcode hoort niet in deze estimator. NL is 1234 AB. De SKU komt uit de calculator, niet van een Discord-screenshot.",
            ]),
            ("Tracken na de grens", [
                f"Zolang de SKU in China is, zie je magazijnstatus in de app. Na de internationale lijn volgt tracking de SKU — vaak {post}. Collect kan aan de deur verschijnen.",
                f"Wie invoerrechten, btw bij invoer en Collect betaalt, staat op de geboekte SKU. Bron die ochtend: {curl} ({customs}). Deze pagina plakt geen tarief in de title en verzint geen aangegeven waarde.",
            ]),
            ("Retour alleen in het magazijn", [
                f"Fail-QC of verkeerde maat los je in de app op zolang het stuk in China ligt. Heeft {post} al bezorgd, opent {customs} geen magazijnticket.",
                f"Twee betalingen blijven normaal: goederen naar China, daarna vracht. Toont de app één kas, dan geldt de app. {OFF}.",
            ]),
            ("Burenslanden zijn andere SKUs", [
                f"{city} is de adrescheck van dit desk. Packstation is Duitsland. Vier cijfers zonder letters is vaak België. Verkeerd land in de estimator is een andere lijn.",
                f"Een rankende douane-URL op {host} is geen live tarief. Bevestig in de app en bij de Douane op de verzenddag, daarna de lijn boeken.",
            ]),
        ],
        "pl": [
            ("Magazyn w Chinach, nie depot InPost", [
                f"Zdjęcia QC powstają w magazynie BBDBuy w Chinach. Depot {post} w Polsce to last-mile, nie drugie studio QC. Dodatkowe kąty prosisz w aplikacji zanim zapłacisz fracht do Polski.",
                f"Dni magazynu są w Help na {OFF}. Ta strona nie wymyśla darmowych dni. Po QC otwórz {EST} z celem Polska. {city}.",
            ]),
            ("Pierwsze zamówienie: jedna SKU odzieży", [
                f"Na pierwsze drzwi w Polsce wystarczy bluza albo para sneakersów ze zdjęciami. Konsolidacja bez QC miesza {customs} i Collect.",
                f"Restricted, perfumy, baterie i płyny zostają poza listą, dopóki aplikacja nie pozwoli rano wysyłki. {host} listuje finds; blokada jest w aplikacji.",
            ]),
            ("Angielskie klucze katalogu to etykiety", [
                "Ściana kategorii mówi sneakers, hoodie, jacket, bag, bo indeks jest po angielsku. Polskie słowa często dają 0 kart — to nie pusty sklep.",
                f"Te klucze nie zmieniają cła ani last-mile. Kraj kalkulatora zostaje Polska, {ccy} to wyświetlanie, kasa to {OFF}. BLIK potwierdzasz w aplikacji.",
            ]),
            ("Czym ta domena nie jest", [
                f"{host} to spreadsheet i przewodnik do drzwi w Polsce. To nie druga kasa BBDBuy, nie {customs}, nie infolinia {post}. Rejestracja i tickety tylko na {OFF}.",
                "Niemiecki Packstation albo czeski kod to złe państwo. SKU pochodzi z kalkulatora, nie ze zrzutu Discord.",
            ]),
            ("Tracking po granicy", [
                f"Dopóki SKU jest w Chinach, status magazynu jest w aplikacji. Po linii międzynarodowej tracking idzie za SKU — często {post}. Collect może pojawić się przy drzwiach.",
                f"Kto płaci cło, VAT importowy i Collect, decyduje SKU. Źródło rano: {curl} ({customs}). Ta strona nie wkleja stawki w tytuł i nie wymyśla wartości zgłoszonej.",
            ]),
            ("Zwrot tylko w magazynie", [
                f"Fail-QC albo zły rozmiar załatwiasz w aplikacji, dopóki rzecz jest w Chinach. Gdy {post} już doręczył, {customs} nie otwiera biletu magazynowego.",
                f"Dwie płatności zostają normalne. Jeśli aplikacja pokazuje jedną kasę, obowiązuje aplikacja. {OFF}.",
            ]),
            ("Sąsiedzi to inne SKU", [
                f"{city} to test etykiety tego desku. Packstation to Niemcy. Inny format kodu to często inne państwo i inna linia.",
                f"Rankingowy artykuł celny na {host} nie jest żywą taryfą. Potwierdź w aplikacji i w KAS w dniu wysyłki, potem rezerwuj linię.",
            ]),
        ],
    }
    return packs[key]


def wrap_copy(host: str, d: dict, keep_slug: str):
    url = f"/{keep_slug}/"
    loc = d["loc"]
    if loc == "fr":
        return (
            f"Avis {A} France",
            f"Les avis BBDBuy pour une adresse en France sont sur {url}. Commandes sur {OFF}.",
            [("Lire la suite", [f"Ouvrez {url}. Colissimo, douane.gouv.fr."])],
        )
    if loc == "de":
        return (
            f"{A} Spreadsheet",
            f"Der ausführliche Text steht unter {url}. Bestellen auf {OFF}.",
            [("Weiterlesen", [f"Öffne {url}."])],
        )
    if loc == "nl":
        return (
            f"{A} verzending",
            f"De volledige gids staat op {url}. Bestellen op {OFF}.",
            [("Verder lezen", [f"Open {url}."])],
        )
    if loc == "pl":
        return (
            f"{A} wysyłka",
            f"Pełny przewodnik jest na {url}. Zamówienia na {OFF}.",
            [("Czytaj dalej", [f"Otwórz {url}."])],
        )
    if loc == "it":
        return (
            f"{A} spreadsheet",
            f"L’articolo completo è su {url}. Ordini su {OFF}.",
            [("Continua", [f"Apri {url}."])],
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
                ("What is a BBDBuy spreadsheet?", [
                    f"A {A} spreadsheet on {host} is a shortlist of warehouse-checked SKUs meant for a UK delivery address — sneakers, hoodies, jackets and bags that still open in the official app. It does not take payment and it is not a second BBDBuy storefront.",
                    f"Rows stay useful only while the source link is live and at least one warehouse photo exists. A price-0 or restricted card is a dead source, not a discount. Keywords: BBDBuy spreadsheet, bbdbuy spreadsheet uk, bbdbuy trusted sellers.",
                ]),
                ("Why UK buyers start with a sheet", [
                    f"Searching Taobao, 1688 and Weidian by hand dumps thousands of expired cards. The sheet keeps finds you already accepted in QC before you ask {post} to move a carton toward a UK postcode.",
                    "UK buyers also avoid an EU IOSS screenshot in the official estimator. This page is written for GB, GBP, and HMRC — Northern Ireland is often another carrier product, not a mainland Royal Mail SKU with the country name swapped.",
                ]),
                ("How BBDBuy spreadsheets work", [
                    f"Open a find on {host}, read warehouse photos in the official {A} app, then book an international line with destination United Kingdom. {host} only explains that order. Cart, wallet and tickets stay on {OFF}.",
                    f"English catalogue keys (sneakers, hoodie, jacket) on the wall are display labels. They are not a US shop and they do not change the estimator country. Live money is in {EST}.",
                ]),
                ("What types of products are included?", [
                    "Shoes, hoodies, jackets, bags and watches dominate because those SKUs still have QC angles. Electronics, perfume, liquids and other restricted classes stay off the sheet unless the official app shows them as allowed the morning you submit.",
                    "A find that passed QC last month can still go restricted. Recheck the official product page before you pay freight. This index does not freeze a catalogue.",
                ]),
                ("Is using a BBDBuy spreadsheet safer?", [
                    f"Safer here means you saw warehouse photos before international freight — not that {customs} disappears. Read {curl} the morning you ship. Import VAT, broker fees and Collect handling change; this page does not paste a rate into the title.",
                    f"The sheet also keeps you off dead Weidian links. It does not file an HMRC entry and it does not pick a declared value for you. {city}.",
                ]),
                ("Who should use a BBDBuy spreadsheet?", [
                    f"First-time UK buyers who need an address test and anyone who already uses {A} but wants spreadsheet, finds, QC and shipping-to-UK in one British site in {ccy}.",
                    "If you ship to a French door, this is the wrong country page. If you need a broker, hire one — orders stay on www.bbdbuy.com.",
                ]),
                ("Common mistakes without a spreadsheet", [
                    f"Pasting an EU code postal into the estimator, treating {host} as checkout, or booking freight before QC. Last-mile is often {post}; Collect can add a fee the estimator hides.",
                    "Another miss: assuming a ranked VAT article on this site is a live tariff. Thresholds move. Confirm in the official app and on the HMRC page the day you ship.",
                ]),
                ("How to use a spreadsheet efficiently", [
                    f"Keep spreadsheet, finds and QC in one tab set. When a find is accepted, open the official freight form toward the United Kingdom. Source: {customs}.",
                    f"Skip under-declaration tricks. Pay what the booked SKU and {EST} show. Orders stay on {OFF}.",
                ]),
                ("Is a BBDBuy spreadsheet required?", [
                    "No. You can search the official app by hand. The sheet exists so UK buyers are not starting from thousands of dead cards every week.",
                    f"You still register and pay on {OFF}. {host} never sees the account.",
                ]),
                ("Ready to use a BBDBuy spreadsheet?", [
                    f"Use the cluster links for finds, QC photos and shipping to the UK. Then register on {OFF}. This site stays an index in {ccy}.",
                ]),
            ],
        )
    if kind == "finds":
        return (
            f"Top {A} spreadsheet finds for UK buyers on {host}: QC-checked sneakers, hoodies and bags aimed at a UK address, not a second global catalogue.",
            [
                ("What are top BBDBuy finds?", [
                    f"Finds on {host} are SKUs kept after warehouse photos — usually shoes, jackets and bags that still open in the official app. They are not a shop window and they are not copied from a US list with the country name swapped.",
                    "A find drops off when the source URL dies or the warehouse no longer has the piece. Price-0 is a removed card, not a sale.",
                ]),
                ("Why UK buyers use curated BBDBuy finds", [
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
                ("Are BBDBuy finds safer than searching manually?", [
                    f"You still read {customs} ({curl}) the morning you ship. A find only means the piece was photographed in China before international freight.",
                    "Safer is not duty-free. Import VAT and Collect can still apply. This page does not invent an HMRC figure.",
                ]),
                ("Who should use top BBDBuy finds?", [
                    "Buyers who already have a UK door and want QC’d picks, not an EU IOSS article. First orders should stay on simple clothing SKUs with photos.",
                    f"If your label is a UK postcode, stay on this British site. Sister country pages are separate files.",
                ]),
                ("Ready to explore top BBDBuy finds?", [
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
                    "Extra angles are often a paid add-on in the official app. Open tickets in the BBDBuy app.",
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
                ("How BBDBuy shipping to the UK works", [
                    f"Warehouse in China → you accept QC → you book a line with destination United Kingdom → {post} or the SKU’s last-mile partner hands it over. {host} does not print a live quote.",
                    f"The label needs a real UK postcode. {city}. Confirm destination GB in {EST} the morning you ship.",
                ]),
                ("BBDBuy shipping options for UK buyers", [
                    "Tax-free, prepaid and collect are properties of the booked SKU in the official app. This page does not rename them. Collect can add a fee the estimator hides.",
                    f"{post} may also add a handling fee on collect parcels. Read the SKU, then the live estimator — not a screenshot from last year.",
                ]),
                ("How long BBDBuy shipping to the UK takes", [
                    "Transit days change with the SKU and the line you book. This page does not invent Royal Mail business days.",
                    "Confirm in the official app the morning you ship. Warehouse processing is separate from international transit.",
                ]),
                ("BBDBuy shipping costs to the UK", [
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
                ("Is BBDBuy shipping suitable for first-time UK buyers?", [
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
                ("Is BBDBuy legal in the UK?", [
                    f"Using a purchasing agent is not a crime in the United Kingdom. Restricted goods, platform rules and the booked SKU still apply. Read {curl} the morning you ship.",
                    "Legal here means the agent model itself. It does not mean every SKU on Taobao is allowed through HMRC.",
                ]),
                ("Is BBDBuy safe to use?", [
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
                ("Is BBDBuy suitable for first-time UK buyers?", [
                    f"Yes if you start with the spreadsheet and finds on {host}, then the official register. This site does not see your account.",
                    "Skip restricted categories on the first order. Clothing SKUs with QC photos are the usual first path.",
                ]),
                ("Final verdict: should UK buyers use BBDBuy?", [
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
                ("How to buy from BBDBuy (UK guide)", [
                    f"Find a QC’d SKU on the spreadsheet or finds list, submit it in the official app, wait for warehouse photos, then book international freight toward the United Kingdom with a UK postcode on the label.",
                    "Do not skip QC to save a day. UK last-mile will not retake a warehouse photo.",
                ]),
                ("What is BBDBuy?", [
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
                "Cards on this hostname are an index, not stock BBDBuy owns.",
            ]),
            ("What is the BBDBuy spreadsheet?", [
                "A shortlist of warehouse-checked SKUs for a UK door. Not Excel, not a second shop.",
                "Keywords: BBDBuy spreadsheet, bbdbuy spreadsheet uk, bbdbuy sheet.",
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


def _ca(kind, host, d):
    post, city, customs, curl, ccy = d["post"], d["city"], d["customs"], d["customs_url"], d["ccy"]
    if kind == "spreadsheet":
        return (
            f"A curated {A} spreadsheet for Canada buyers on {host}: trusted sellers, QC photos and finds in one index. It is not Excel and not checkout. Order on {OFF} in {ccy} after you pick destination Canada.",
            [
                ("What is a BBDBuy spreadsheet?", [
                    f"A {A} spreadsheet on {host} is a shortlist of warehouse-checked SKUs meant for a Canadian delivery address — sneakers, hoodies, jackets and bags that still open in the official app. It does not take payment and it is not a second BBDBuy storefront.",
                    f"Rows stay useful only while the source link is live and at least one warehouse photo exists. A price-0 or restricted card is a dead source, not a discount. Keywords: BBDBuy spreadsheet, bbdbuy spreadsheet canada, bbdbuy trusted sellers.",
                ]),
                ("Why Canada buyers start with a sheet", [
                    f"Searching Taobao, 1688 and Weidian by hand dumps thousands of expired cards. The sheet keeps finds you already accepted in QC before you ask {post} to move a carton toward a Canadian postal code.",
                    "Canada buyers also avoid a US de-minimis screenshot in the official estimator. This page is written for CA, CAD, and CBSA — A US ZIP is the wrong country, not a Canada Post SKU with the country name swapped.",
                ]),
                ("How BBDBuy spreadsheets work", [
                    f"Open a find on {host}, read warehouse photos in the official {A} app, then book an international line with destination Canada. {host} only explains that order. Cart, wallet and tickets stay on {OFF}.",
                    f"English catalogue keys (sneakers, hoodie, jacket) on the wall are display labels. They are not a US shop and they do not change the estimator country. Live money is in {EST}.",
                ]),
                ("What types of products are included?", [
                    "Shoes, hoodies, jackets, bags and watches dominate because those SKUs still have QC angles. Electronics, perfume, liquids and other restricted classes stay off the sheet unless the official app shows them as allowed the morning you submit.",
                    "A find that passed QC last month can still go restricted. Recheck the official product page before you pay freight. This index does not freeze a catalogue.",
                ]),
                ("Is using a BBDBuy spreadsheet safer?", [
                    f"Safer here means you saw warehouse photos before international freight — not that {customs} disappears. Read {curl} the morning you ship. GST/HST, broker fees and Collect handling change; this page does not paste a rate into the title.",
                    f"The sheet also keeps you off dead Weidian links. It does not file a CBSA entry and it does not pick a declared value for you. {city}.",
                ]),
                ("Who should use a BBDBuy spreadsheet?", [
                    f"First-time Canada buyers who need an address test and anyone who already uses {A} but wants spreadsheet, finds, QC and shipping-to-Canada in one Canadian site in {ccy}.",
                    "If you ship to a US door, this is the wrong country page. If you need a broker, hire one — orders stay on www.bbdbuy.com.",
                ]),
                ("Common mistakes without a spreadsheet", [
                    f"Pasting a US ZIP into the estimator, treating {host} as checkout, or booking freight before QC. Last-mile is often {post}; Collect can add a fee the estimator hides.",
                    "Another miss: assuming a ranked VAT article on this site is a live tariff. Thresholds move. Confirm in the official app and on the CBSA page the day you ship.",
                ]),
                ("How to use a spreadsheet efficiently", [
                    f"Keep spreadsheet, finds and QC in one tab set. When a find is accepted, open the official freight form toward Canada. Source: {customs}.",
                    f"Skip under-declaration tricks. Pay what the booked SKU and {EST} show. Orders stay on {OFF}.",
                ]),
                ("Is a BBDBuy spreadsheet required?", [
                    "No. You can search the official app by hand. The sheet exists so Canada buyers are not starting from thousands of dead cards every week.",
                    f"You still register and pay on {OFF}. {host} never sees the account.",
                ]),
                ("Ready to use a BBDBuy spreadsheet?", [
                    f"Use the cluster links for finds, QC photos and shipping to Canada. Then register on {OFF}. This site stays an index in {ccy}.",
                ]),
            ],
        )
    if kind == "finds":
        return (
            f"Top {A} spreadsheet finds for Canada buyers on {host}: QC-checked sneakers, hoodies and bags aimed at a Canadian address, not a second global catalogue.",
            [
                ("What are top BBDBuy finds?", [
                    f"Finds on {host} are SKUs kept after warehouse photos — usually shoes, jackets and bags that still open in the official app. They are not a shop window and they are not copied from a US list with the country name swapped.",
                    "A find drops off when the source URL dies or the warehouse no longer has the piece. Price-0 is a removed card, not a sale.",
                ]),
                ("Why Canada buyers use curated BBDBuy finds", [
                    f"Manual search mixes dead Weidian links with live cards. Curated finds are the ones that still photograph in China before you book {post} toward a Canadian postal code.",
                    f"{ccy} display on this desk, destination Canada, and a real Canadian postal code beat hunting Reddit screenshots that never list a CBSA path. {city}.",
                ]),
                ("Popular product categories", [
                    "Sneakers and hoodies fill the wall because those lots still have QC angles. Bags and jackets follow. Restricted goods stay off even if a forum names them.",
                    "Category keys on this site are English display labels. They do not make the parcel a US import.",
                ]),
                ("How these finds are selected", [
                    f"A find needs a live source URL, at least one warehouse photo, and estimator destination Canada — not this hostname as a country. {city} is the address test.",
                    "We do not keep a find because it was popular last season. If QC fails, it leaves the list.",
                ]),
                ("Are BBDBuy finds safer than searching manually?", [
                    f"You still read {customs} ({curl}) the morning you ship. A find only means the piece was photographed in China before international freight.",
                    "Safer is not duty-free. GST/HST on import and Collect can still apply. This page does not invent a CBSA figure.",
                ]),
                ("Who should use top BBDBuy finds?", [
                    "Buyers who already have a Canadian door and want QC’d picks, not a US de-minimis article. First orders should stay on simple clothing SKUs with photos.",
                    f"If your label is a Canadian postal code, stay on this Canadian site. Sister country pages are separate files.",
                ]),
                ("Ready to explore top BBDBuy finds?", [
                    f"Open QC next, then shipping to Canada. Register and pay on {OFF}. {host} is information only.",
                ]),
            ],
        )
    if kind == "qc":
        return (
            f"QC on {host} means warehouse photos in the official {A} app, taken in China, before you pay freight to Canada.",
            [
                ("What QC is on this site", [
                    "Quality check is extra angles of the piece in the warehouse — seams, tags, sole, print. It is not a laboratory, not a brand-authentication court, and not a CBSA x-ray.",
                    "Photos land in the official app while the SKU is still in China. That is the only window that matters for a retake.",
                ]),
                ("When to ask for extra photos", [
                    f"Ask while the SKU is in the warehouse. After {post} has the carton, {customs} is the wrong office for a warehouse retake.",
                    "Extra angles are often a paid add-on in the official app. Open tickets in the BBDBuy app.",
                ]),
                ("What QC does not do", [
                    f"QC does not file a CBSA entry, does not pay GST/HST on import, and does not invent a declared value. Educational source: {curl}.",
                    "A clean QC album is not a promise the SKU will pass a later platform rule. Recheck before you book the line.",
                ]),
                ("QC and a Canadian address", [
                    f"Use destination Canada and a Canadian postal code in the estimator. A US ZIP is the wrong country for this site. {city}.",
                    "Warehouse photos are taken in China either way. The Canada part is the door on the label after you accept QC.",
                ]),
                ("If a find fails QC", [
                    "Leave it in the warehouse or return it in the official app. Do not book international freight on a reject just to 'get it over with'.",
                    f"Failed QC is cheaper in China than after {post} attempts delivery.",
                ]),
                ("Ready to ship after QC?", [
                    f"Only then open {EST} toward Canada. {host} does not take payment. {ccy} totals live in the app.",
                ]),
            ],
        )
    if kind == "shipping":
        return (
            f"{A} shipping to Canada uses the official estimator country code CA, not this domain. Open the live freight form after warehouse photos. Last-mile is often {post}.",
            [
                ("How BBDBuy shipping to Canada works", [
                    f"Warehouse in China → you accept QC → you book a line with destination Canada → {post} or the SKU’s last-mile partner hands it over. {host} does not print a live quote.",
                    f"The label needs a real Canadian postal code. {city}. Confirm destination Canada in {EST} the morning you ship.",
                ]),
                ("BBDBuy shipping options for Canada buyers", [
                    "Tax-free, prepaid and collect are properties of the booked SKU in the official app. This page does not rename them. Collect can add a fee the estimator hides.",
                    f"{post} may also add a handling fee on collect parcels. Read the SKU, then the live estimator — not a screenshot from last year.",
                ]),
                ("How long BBDBuy shipping to Canada takes", [
                    "Transit days change with the SKU and the line you book. This page does not invent Canada Post business days.",
                    "Confirm in the official app the morning you ship. Warehouse processing is separate from international transit.",
                ]),
                ("BBDBuy shipping costs to Canada", [
                    f"You pay international freight plus whatever the SKU says at the border. {post} can add collect handling. No dollar amount is pasted into this title because the live form moves.",
                    f"{ccy} is the local currency on this site. Checkout still happens on {OFF}.",
                ]),
                ("Customs, VAT and import fees", [
                    f"Read {customs} at {curl} the morning you ship. GST/HST import thresholds and Collect rules change. Ranked VAT articles on this site stay as local notes — they are not a live tariff table.",
                    "This page does not coach a declared value. Pay what the booked SKU and CBSA rules require.",
                ]),
                ("Common shipping risks", [
                    f"Wrong country in the estimator (US ZIP), booking before QC, ignoring a US mailbox as another carrier product. Those mistakes are Canada-path errors, not 'agent is down'.",
                    "Restricted SKUs that slipped into the warehouse still cannot ride a Canada line if the official app blocks them at submit.",
                ]),
                ("Is BBDBuy shipping suitable for first-time Canada buyers?", [
                    f"Yes if you treat {host} as a map and {OFF} as checkout. Address test: Canadian postal code. Source: {customs}.",
                    "Start with one clothing SKU, accept QC, then book. Do not consolidate a pile of un-QCd items on the first order.",
                ]),
                ("Ready to ship safely to Canada?", [
                    f"QC first, then {EST} toward Canada. Orders only on {OFF}.",
                ]),
            ],
        )
    if kind == "legal":
        return (
            f"{A} is a purchasing agent. {host} explains the Canada path; it is not the official app and not {customs}. Read CBSA the morning you ship.",
            [
                ("Is BBDBuy legal in Canada?", [
                    f"Using a purchasing agent is not a crime in Canada. Restricted goods, platform rules and the booked SKU still apply. Read {curl} the morning you ship.",
                    "Legal here means the agent model itself. It does not mean every SKU on Taobao is allowed through CBSA.",
                ]),
                ("Is BBDBuy safe to use?", [
                    f"Safe on this page means warehouse QC before freight, payment in the official app, and a real Canadian address — not a promise that a parcel skips {customs}.",
                    f"{ccy} checkout, destination Canada, Canadian postal code on the label. {host} never holds the wallet.",
                ]),
                ("What are the main risks for Canada buyers?", [
                    f"Dead source links, booking collect without reading the SKU, and treating {host} as checkout. {post} can add fees.",
                    "A second risk is pasting a US ZIP because the estimator UI looks similar. That is the wrong country for this site. A US ZIP is the wrong country.",
                ]),
                ("How can Canada buyers reduce risk?", [
                    f"QC in the official app, estimator destination Canada, Canadian postal code on the label. No under-declaration. No invented CBSA figure.",
                    "Keep spreadsheet, finds and QC together so you are not booking freight on a screenshot from another country page.",
                ]),
                ("Is BBDBuy suitable for first-time Canada buyers?", [
                    f"Yes if you start with the spreadsheet and finds on {host}, then the official register. This site does not see your account.",
                    "Skip restricted categories on the first order. Clothing SKUs with QC photos are the usual first path.",
                ]),
                ("Final verdict: should Canada buyers use BBDBuy?", [
                    f"{A} can be used toward Canada if you follow the official app and {customs}. This site stays independent information. Orders on {OFF}.",
                ]),
                ("Ready to get started?", [
                    f"Open spreadsheet → finds → QC → shipping to Canada. Pay only on {OFF}.",
                ]),
            ],
        )
    if kind == "guide":
        return (
            f"A step-by-step {A} path for a Canadian address on {host}. Photos in the warehouse, then freight. Not checkout.",
            [
                ("How to buy from BBDBuy (Canada guide)", [
                    f"Find a QC’d SKU on the spreadsheet or finds list, submit it in the official app, wait for warehouse photos, then book international freight toward Canada with a Canadian postal code on the label.",
                    "Do not skip QC to save a day. Canada last-mile will not retake a warehouse photo.",
                ]),
                ("What is BBDBuy?", [
                    f"A China purchasing agent. {host} only explains the Canada path in {ccy}. Payment, tickets and the estimator stay on {OFF}.",
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
                ("Step 3 — book Canada freight", [
                    f"Open {EST} with destination Canada. {city}. Last-mile is often {post}.",
                    "Prepaid vs collect is a SKU property. This page does not invent Canada Post days or a CBSA rate.",
                ]),
                ("Step 4 — pay only on the official site", [
                    f"Register and pay on {OFF}. {host} never stores a card. CAD on this desk is display conversion, not checkout.",
                    "If the official SPA still prints USD digits after you pick CAD, trust the digits and the estimator.",
                ]),
                ("Common beginner mistakes", [
                    "US destination in the estimator, booking before QC, treating this hostname as a shop.",
                    "A US ZIP is the wrong country — do not assume the same Canada Post SKU as a USPS line.",
                ]),
                ("Ready to start?", [
                    f"Spreadsheet → finds → QC → shipping. Then {OFF}.",
                ]),
            ],
        )
    # faq
    return (
        f"{A} spreadsheet FAQ for Canada buyers on {host}: index, QC, {post}, {customs}. Not checkout.",
        [
            ("Does this site sell the goods?", [
                f"No. {A} is a purchasing agent. Orders stay on {OFF}. {host} lists finds for Canada buyers.",
                "Cards on this hostname are an index, not stock BBDBuy owns.",
            ]),
            ("What is the BBDBuy spreadsheet?", [
                "A shortlist of warehouse-checked SKUs for a Canadian door. Not Excel, not a second shop.",
                "Keywords: BBDBuy spreadsheet, bbdbuy spreadsheet canada, bbdbuy sheet.",
            ]),
            ("How do I use QC photos?", [
                "They land in the official app while the piece is in China. Ask for extra angles there, not after last-mile.",
                f"{post} will not retake a warehouse photo.",
            ]),
            ("How does shipping to Canada work?", [
                f"Estimator destination Canada, then the booked SKU. Last-mile is often {post}. Live quote: {EST}.",
                f"{city}. This page does not invent transit days.",
            ]),
            ("Who pays import charges?", [
                f"The booked SKU. {post} can add a collect fee. Source: {curl}. No declared-value coaching.",
                "Ranked VAT notes on this host stay; they are not a live tariff.",
            ]),
            ("Why CAD here and dollars on the official SPA?", [
                f"Display conversion of the China warehouse card. Checkout currency is whatever {OFF} shows the morning you pay.",
                "Trust the official digits and the estimator.",
            ]),
            ("Is a US ZIP the same as a Canadian postal code?", [
                "No. A US ZIP is another estimator country. Do not assume the same Canada Post SKU.",
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
                ("What is a BBDBuy spreadsheet?", [
                    f"A {A} spreadsheet on {host} is a shortlist of warehouse-checked SKUs meant for a US delivery address — sneakers, hoodies, jackets and bags that still open in the official app. It does not take payment and it is not a second BBDBuy storefront.",
                    "Rows stay useful only while the source link is live and at least one warehouse photo exists. A price-0 or restricted card is a dead source, not a discount. Keywords: BBDBuy spreadsheet, bbdbuy spreadsheet usa, bbdbuy trusted sellers.",
                ]),
                ("Why US buyers start with a sheet", [
                    f"Manual Taobao/Weidian search mixes expired cards with live lots. The sheet keeps finds you already accepted in QC before you ask {post} to move a carton toward a US ZIP.",
                    f"US buyers also avoid a Canadian postal code (form A1A 1A1) in the official estimator. This page is written for CBP territory, {ccy}, and a US ZIP — this desk does not invent a de-minimis dollar.",
                ]),
                ("How BBDBuy spreadsheets work", [
                    f"Open a find on {host}, read warehouse photos in the official {A} app, then book an international line with destination United States. Cart, wallet and tickets stay on {OFF}.",
                    f"English catalogue keys on the wall are display labels. They do not change the estimator country. Live money is in {EST}.",
                ]),
                ("What types of products are included?", [
                    "Shoes, hoodies, jackets and bags dominate because those SKUs still have QC angles. Electronics, batteries, perfume and other restricted classes stay off unless the official app shows them as allowed the morning you submit.",
                    "A find that passed QC last month can still go restricted. Recheck before you pay freight.",
                ]),
                ("Is using a BBDBuy spreadsheet safer?", [
                    f"Safer means warehouse photos before international freight — not that {customs} disappears. Read {curl} the morning you ship. Informal-entry rules change; this page does not paste a dollar into the title.",
                    f"The sheet keeps you off dead Weidian links. It does not file a CBP entry and it does not pick a declared value. Address test: {city}.",
                ]),
                ("Who should use a BBDBuy spreadsheet?", [
                    f"First-time US buyers who need a ZIP test and anyone who already uses {A} but wants spreadsheet, finds, QC and shipping-to-US on one American site in {ccy}.",
                    "If you ship to Canada, this is the wrong country page. Orders stay on www.bbdbuy.com.",
                ]),
                ("Common mistakes without a spreadsheet", [
                    f"Pasting a Canadian postal code, treating {host} as checkout, or booking freight before QC. Last-mile is often {post} or FedEx; Collect can add a fee the estimator hides.",
                    "Another miss: treating a ranked de-minimis article as a live threshold. Rules move. Confirm in-app and on CBP the day you ship.",
                ]),
                ("How to use a spreadsheet efficiently", [
                    f"Keep spreadsheet, finds and QC together. When a find is accepted, open {EST} toward the United States. Source: {customs}.",
                    f"No under-declaration. Pay what the booked SKU shows. Orders on {OFF}.",
                ]),
                ("Is a BBDBuy spreadsheet required?", [
                    "No. You can search the official app by hand. The sheet exists so US buyers are not restarting from dead cards every week.",
                    f"Register and pay on {OFF}. {host} never sees the account.",
                ]),
                ("Ready to use a BBDBuy spreadsheet?", [
                    f"Use finds, QC and shipping to the USA, then register on {OFF}. This site stays an index in {ccy}.",
                ]),
            ],
        )
    if kind == "finds":
        return (
            f"Top {A} spreadsheet finds for US buyers on {host}: QC-checked sneakers, hoodies and bags aimed at a US ZIP, not a second global catalogue.",
            [
                ("What are top BBDBuy finds?", [
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
                    "Extra angles are often paid in-app. Open tickets in the BBDBuy app.",
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
                ("How BBDBuy shipping to the USA works", [
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
                ("Is BBDBuy legal in the United States?", [
                    f"Using a purchasing agent is not itself a crime. Restricted goods, platform rules and the booked SKU still apply. Read {curl}.",
                    "Legal here means the agent model. It does not mean every Taobao SKU is allowed through CBP.",
                ]),
                ("Is BBDBuy safe to use?", [
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
                ("How to buy from BBDBuy (US guide)", [
                    "Pick a QC’d SKU, submit it in the official app, wait for warehouse photos, then book freight toward the United States with a US ZIP on the label.",
                    f"Do not skip QC. {post} will not retake a warehouse photo.",
                ]),
                ("What is BBDBuy?", [
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
            ("What is the BBDBuy spreadsheet?", [
                "A shortlist of warehouse-checked SKUs for a US ZIP. Not Excel.",
                "Keywords: BBDBuy spreadsheet, bbdbuy spreadsheet usa, bbdbuy sheet.",
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
                ("Was ist ein BBDBuy-Spreadsheet?", [
                    f"Auf {host} ist das Spreadsheet eine Shortlist lagergeprüfter SKUs für eine österreichische Adresse — Sneaker, Hoodies, Jacken, Taschen, die in der offiziellen App noch öffnen. Es kassiert nicht und ist kein zweites BBDBuy-Schaufenster.",
                    "Zeilen bleiben nur nützlich, solange der Quelllink lebt und mindestens ein Lagerfoto existiert. Preis 0 oder Restricted ist eine tote Quelle, kein Rabatt. Keywords: BBDBuy spreadsheet, bbdbuy spreadsheet osterreich, bbdbuy trusted sellers.",
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
                ("Was sind BBDBuy-Finds?", [
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
                ("Ist BBDBuy in Österreich legal?", [
                    f"Ein Einkaufsagent ist in Österreich kein Straftatbestand. Restricted, Plattformregeln und die SKU gelten weiter. {curl} lesen.",
                    "Legal heißt das Agent-Modell. Nicht jede Taobao-SKU darf durch BMF Zoll.",
                ]),
                ("Ist BBDBuy sicher?", [
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
                ("Was ist BBDBuy?", [
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
                "Keywords: BBDBuy spreadsheet, bbdbuy spreadsheet osterreich, bbdbuy sheet.",
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
                ("Was ist ein BBDBuy-Spreadsheet?", [
                    f"Auf {host} ist das Spreadsheet eine Shortlist lagergeprüfter SKUs für eine deutsche Adresse — Sneaker, Hoodies, Jacken, Taschen. Es kassiert nicht.",
                    "Preis 0 oder Restricted ist tot, kein Rabatt. Keywords: BBDBuy spreadsheet, bbdbuy spreadsheet deutschland, bbdbuy trusted sellers.",
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
                ("Was ist BBDBuy?", [
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
        f"{A} Spreadsheet-FAQ Deutschland auf {host}: Index, QC, {post}, {customs}. Keine Kasse.",
        [
            ("Verkauft diese Site die Ware?", [
                f"Nein. {A} ist Einkaufsagent. Bestellungen bleiben auf {OFF}. {host} listet Finds für eine deutsche Tür — kein zweites Lager, keine zweite Kasse.",
                "Karten auf diesem Hostname sind ein Index, kein Bestand, den BBDBuy selbst hält.",
            ]),
            ("Was ist das BBDBuy-Spreadsheet?", [
                f"Eine Shortlist lagergeprüfter SKUs für {city}. Kein Excel, kein zweiter Shop. Keywords: BBDBuy spreadsheet, bbdbuy spreadsheet deutschland, bbdbuy trusted sellers.",
                "Eine Zeile bleibt nur nützlich, solange der Quelllink lebt und mindestens ein Lagerfoto existiert. Preis 0 oder Restricted ist tot, kein Rabatt.",
            ]),
            ("Wie nutze ich QC-Fotos?", [
                "Sie landen in der offiziellen App, solange das Teil in China liegt. Extra-Winkel dort anfragen, nicht nach der Last-Mile.",
                f"{post} macht keine Nachaufnahme im Lager, sobald der Karton in Deutschland ist. Tickets nur in der App.",
            ]),
            ("Wie funktioniert Versand nach Deutschland?", [
                f"Schätzerziel Deutschland, dann die gebuchte SKU. Letzte Meile oft {post}. Live-Quote: {EST}. Packstation nur, wenn die SKU sie für DE anbietet.",
                f"{city}. Diese Seite erfindet keine DHL-Werktage und keinen Zollsatz.",
            ]),
            ("Wer zahlt Zoll und Einfuhrumsatzsteuer?", [
                f"Die gebuchte SKU. {post} kann Collect-Gebühren addieren, die der Schätzer nicht zeigt. Quelle: {curl} ({customs}).",
                "Rankende Zollnotizen auf diesem Host bleiben lokale Hinweise — kein Live-Tarif. Kein Deklarationsbetrag auf dieser Seite.",
            ]),
            ("Warum Euro hier und Dollar in der offiziellen SPA?", [
                f"Anzeige-Umrechnung der China-Lagerkarte. Die Kassenwährung ist, was {OFF} am Zahlungsmorgen zeigt. {ccy} auf {host} ist Display.",
                f"Steht in der App noch ein Dollarzeichen, gelten die Ziffern und {EST} mit Ziel Deutschland.",
            ]),
            ("Darf ich 1010 Wien oder eine AT-PLZ nutzen?", [
                "Nein. Vierstellige österreichische PLZ und 1010 Wien sind das falsche Schätzerland, auch wenn die App Deutsch ist.",
                f"Deutschland braucht {city}. AT-Labels gehören auf den Österreich-Desk, nicht hier.",
            ]),
            ("Wo registriere ich mich?", [
                f"Nur auf {OFF}. {host} nimmt keine Karte, kein PayPal, kein Guthaben.",
                "Dieser Desk erklärt den DE-Weg. Konto, Wallet und Tickets bleiben auf der offiziellen Domain.",
            ]),
        ],
    )


def _es(kind, host, d):
    post, city, customs, curl, ccy = d["post"], d["city"], d["customs"], d["customs_url"], d["ccy"]
    if kind == "spreadsheet":
        return (
            f"Un spreadsheet {A} para compradores en España en {host}: sellers con QC, finds en un índice. No es Excel ni caja. Pedidos en {OFF} en {ccy} con destino España.",
            [
                ("Qué es un spreadsheet BBDBuy", [
                    f"En {host} es una shortlist de SKU fotografiados en almacén para una dirección española. No cobra y no es un segundo escaparate.",
                    "Precio 0 o restricted es fuente muerta. Keywords: BBDBuy spreadsheet, bbdbuy spreadsheet espana, bbdbuy trusted sellers.",
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
                ("Qué es BBDBuy", [
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
        f"FAQ spreadsheet {A} para España en {host}: índice, QC, {post}, {customs}. No es caja.",
        [
            ("¿Esta web vende la mercancía?", [
                f"No. {A} es agente de compra. Los pedidos siguen en {OFF}. {host} lista finds para una puerta en España — no es un segundo almacén ni una segunda caja.",
                "Las fichas de este hostname son un índice, no stock que BBDBuy posea.",
            ]),
            ("Qué es el spreadsheet BBDBuy", [
                f"Una shortlist de SKU con fotos de almacén para {city}. No es Excel ni una segunda tienda. Keywords: BBDBuy spreadsheet, bbdbuy spreadsheet espana, bbdbuy trusted sellers.",
                "Una fila sirve mientras el enlace fuente vive y hay al menos una foto. Precio 0 o restricted es fuente muerta, no un descuento.",
            ]),
            ("Cómo uso las fotos QC", [
                "Llegan a la app oficial mientras la pieza está en China. Pide ángulos extra ahí, no después de la última milla.",
                f"{post} no rehace la foto de almacén cuando el cartón ya está en España. Tickets solo en la app.",
            ]),
            ("Cómo funciona el envío a España", [
                f"Destino España en el estimador, luego la SKU reservada. Última milla a menudo {post}. Cotización viva: {EST}.",
                f"{city}. Canarias, Ceuta o Melilla pueden ser otra SKU. Esta página no inventa plazos de Correos ni un tipo de IVA.",
            ]),
            ("Quién paga aduana e IVA de importación", [
                f"La SKU reservada. {post} puede añadir Collect que el estimador no enseña. Fuente: {curl} ({customs}).",
                "Las notas de aduana que rankean en este host son avisos locales, no un arancel live. Esta página no inventa un valor declarado.",
            ]),
            ("Por qué euros aquí y dólares en la SPA oficial", [
                f"Conversión de visualización de la ficha de almacén en China. La moneda de caja es la que muestre {OFF} el día que pagas. {ccy} en {host} es display.",
                f"Si la app sigue con símbolo de dólar, valen las cifras y {EST} con destino España.",
            ]),
            ("¿Puedo usar un code postal francés?", [
                "No. Un code postal francés o un CAP italiano es el país equivocado, aunque la app esté en español.",
                f"España necesita {city}. Un recuento de líneas francés no se copia a este desk.",
            ]),
            ("Dónde me registro", [
                f"Solo en {OFF}. {host} no cobra tarjeta ni PayPal ni saldo.",
                "Este desk explica el camino ES. Cuenta, wallet y tickets quedan en el dominio oficial.",
            ]),
        ],
    )


def _fr(kind, host, d):
    post, city, customs, curl, ccy = d["post"], d["city"], d["customs"], d["customs_url"], d["ccy"]
    if kind == "spreadsheet":
        return (
            f"Un spreadsheet {A} pour acheteurs en France sur {host} : sellers QC, finds dans un index. Pas Excel, pas une caisse. Commandes sur {OFF} en {ccy}, destination France.",
            [
                ("Qu’est-ce qu’un spreadsheet BBDBuy ?", [
                    f"Sur {host}, une shortlist de SKU photographiés en entrepôt pour une adresse française. Ça n’encaisse pas.",
                    "Prix 0 ou restricted = source morte. Keywords: BBDBuy spreadsheet, bbdbuy spreadsheet france, bbdbuy trusted sellers.",
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
                ("C’est quoi BBDBuy", [
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
                f"Shortlist pour {city}. Pas Excel. Keywords: bbdbuy spreadsheet france.",
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
                ("Cos’è uno spreadsheet BBDBuy", [
                    f"Su {host} è una shortlist di SKU fotografati in magazzino per un indirizzo italiano. Non incassa.",
                    "Prezzo 0 o restricted è fonte morta. Keywords: BBDBuy spreadsheet, bbdbuy spreadsheet italia, bbdbuy trusted sellers.",
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
                ("Cos’è BBDBuy", [
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
        f"FAQ spreadsheet {A} Italia su {host}: indice, QC, {post}, {customs}. Non è cassa.",
        [
            ("Questo sito vende la merce?", [
                f"No. {A} è agente d’acquisto. Gli ordini restano su {OFF}. {host} elenca i finds per una porta in Italia — non è un secondo magazzino né una seconda cassa.",
                "Le schede di questo hostname sono un indice, non stock che BBDBuy possiede.",
            ]),
            ("Cos’è lo spreadsheet BBDBuy?", [
                f"Una shortlist di SKU con foto di magazzino per {city}. Non è Excel né un secondo negozio. Keywords: BBDBuy spreadsheet, bbdbuy spreadsheet italia, bbdbuy trusted sellers.",
                "Una riga resta utile finché il link sorgente è vivo e c’è almeno una foto. Prezzo 0 o restricted è fonte morta, non uno sconto.",
            ]),
            ("Come uso le foto QC?", [
                "Arrivano nell’app ufficiale finché il pezzo è in Cina. Chiedi angoli extra lì, non dopo l’ultimo miglio.",
                f"{post} non rifà la foto di magazzino a cartone già in Italia. Ticket solo in app.",
            ]),
            ("Come funziona la spedizione in Italia?", [
                f"Destinazione Italia nel calcolatore, poi la SKU prenotata. Ultimo miglio spesso {post}. Quote live: {EST}.",
                f"{city}. Questa pagina non inventa giorni Poste né un’aliquota ADM. Una Packstation tedesca non sostituisce il CAP.",
            ]),
            ("Chi paga dazi e IVA all’importazione?", [
                f"La SKU prenotata. {post} può aggiungere Collect che il calcolatore non mostra. Fonte: {curl} ({customs}).",
                "Le note dogana in ranking su questo host restano avvisi locali, non un tariffario live. Nessun valore dichiarato su questa pagina.",
            ]),
            ("Perché euro qui e dollari nella SPA ufficiale?", [
                f"Conversione di display della scheda magazzino in Cina. La valuta di cassa è quella che {OFF} mostra il mattino del pagamento. {ccy} su {host} è display.",
                f"Se l’app stampa ancora il dollaro, valgono le cifre e {EST} con destinazione Italia.",
            ]),
            ("Posso usare un code postal francese?", [
                "No. Un code postal francese o un código español è il paese sbagliato, anche se l’app è in italiano.",
                f"L’Italia vuole {city}. Un foglio ES o FR non si copia su questo desk.",
            ]),
            ("Dove mi registro?", [
                f"Solo su {OFF}. {host} non prende carta, PayPal né saldo.",
                "Questo desk spiega il percorso IT. Account, wallet e ticket restano sul dominio ufficiale.",
            ]),
        ],
    )


def _nl(kind, host, d):
    post, city, customs, curl, ccy = d["post"], d["city"], d["customs"], d["customs_url"], d["ccy"]
    if kind == "spreadsheet":
        return (
            f"Een {A}-spreadsheet voor kopers in Nederland op {host}: QC-checked sellers en finds in één index. Geen Excel, geen kassa. Bestellen op {OFF} in {ccy}, bestemming Nederland.",
            [
                ("Wat is een BBDBuy-spreadsheet?", [
                    f"Op {host} is het een shortlist van magazijnfoto-SKU’s voor een Nederlands adres. Het incasseert niet.",
                    "Prijs 0 of restricted is een dode bron. Keywords: BBDBuy spreadsheet, bbdbuy spreadsheet nederland, bbdbuy trusted sellers.",
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
                ("Wat is BBDBuy", [
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
        f"{A} spreadsheet-FAQ Nederland op {host}: index, QC, {post}, {customs}. Geen kassa.",
        [
            ("Verkoopt deze site de goederen?", [
                f"Nee. {A} is inkoopagent. Bestellingen blijven op {OFF}. {host} toont finds voor een Nederlandse deur — geen tweede magazijn, geen tweede kassa.",
                "Kaarten op deze hostname zijn een index, geen voorraad die BBDBuy zelf houdt.",
            ]),
            ("Wat is de BBDBuy-spreadsheet?", [
                f"Een shortlist van magazijnfoto-SKU’s voor {city}. Geen Excel, geen tweede shop. Keywords: BBDBuy spreadsheet, bbdbuy spreadsheet nederland, bbdbuy trusted sellers.",
                "Een rij blijft nuttig zolang de bronlink leeft en er minstens één foto is. Prijs 0 of restricted is dood, geen korting.",
            ]),
            ("Hoe gebruik ik QC-foto’s?", [
                "Ze landen in de officiële app zolang het stuk in China ligt. Extra hoeken daar vragen, niet na last-mile.",
                f"{post} maakt geen heropname in het magazijn als de doos al in Nederland is. Tickets alleen in de app.",
            ]),
            ("Hoe werkt verzending naar Nederland?", [
                f"Estimator-bestemming Nederland, daarna de geboekte SKU. Last-mile vaak {post}. Live quote: {EST}.",
                f"{city}. Deze pagina verzint geen DHL-werkdagen en geen douanetarief. Packstation is Duitsland, geen NL-label.",
            ]),
            ("Wie betaalt invoerrechten en btw bij invoer?", [
                f"De geboekte SKU. {post} kan Collect-toeslagen innen die de calculator niet toont. Bron: {curl} ({customs}).",
                "Rankende douane-notities op deze host blijven lokale hints — geen live tarief. Geen aangegeven waarde op deze pagina.",
            ]),
            ("Waarom euro hier en dollars in de officiële SPA?", [
                f"Weergaveconversie van de China-magazijnkaart. De kassavaluta is wat {OFF} toont op de betaalochtend. {ccy} op {host} is display.",
                f"Staat in de app nog een dollarteken, dan gelden de cijfers en {EST} met bestemming Nederland. iDEAL bevestig je in de app.",
            ]),
            ("Mag ik een Packstation of Belgische postcode?", [
                "Nee. Een Duits Packstation-nummer of vier cijfers zonder letters (vaak België) is het verkeerde land, ook als de app Nederlands is.",
                f"Nederland wil {city}. Een DE- of BE-label hoort niet op dit desk.",
            ]),
            ("Waar registreer ik?", [
                f"Alleen op {OFF}. {host} neemt geen kaart, PayPal of saldo.",
                "Dit desk legt het NL-pad uit. Account, wallet en tickets blijven op het officiële domein.",
            ]),
        ],
    )


def _pl(kind, host, d):
    post, city, customs, curl, ccy = d["post"], d["city"], d["customs"], d["customs_url"], d["ccy"]
    if kind == "spreadsheet":
        return (
            f"Arkusz {A} dla kupujących w Polsce na {host}: sprawdzone SKU z QC i finds. To nie Excel i nie kasa. Zamówienia na {OFF} w {ccy}, cel Polska.",
            [
                ("Co to jest spreadsheet BBDBuy?", [
                    f"Na {host} to shortlista SKU ze zdjęciami magazynowymi na polski adres — sneakersy, bluzy, kurtki, torby. Nie pobiera płatności.",
                    "Cena 0 albo restricted to martwe źródło, nie przecena. Keywords: BBDBuy spreadsheet, bbdbuy spreadsheet polska, bbdbuy trusted sellers.",
                ]),
                ("Dlaczego Polska zaczyna od arkusza", [
                    f"Ręczne szukanie miesza martwe karty Weidian. Arkusz trzyma finds już zaakceptowane w QC, zanim {post} pojedzie do {city}.",
                    "Kupujący w PL unikają niemieckiego Packstation. Ta strona to PL, PLN, KAS — kod 00-001, nie automat DE.",
                ]),
                ("Jak to działa", [
                    f"Otwórz find, przeczytaj QC w aplikacji {A}, zarezerwuj linię z celem Polska. Koszyk na {OFF}.",
                    f"Angielskie klucze nie zmieniają kraju kalkulatora. Live pieniądze: {EST}.",
                ]),
                ("Jakie produkty", [
                    "Buty, bluzy, kurtki, torby z kątami QC. Restricted zostaje poza listą, dopóki aplikacja nie pozwoli rano wysyłki.",
                    "Find z zeszłego miesiąca może się zamknąć. Sprawdź kartę oficjalną przed frachtem.",
                ]),
                ("Bezpieczniej?", [
                    f"Bezpieczniej = zdjęcia magazynowe przed frachtem, nie że {customs} znika. {curl} w dniu wysyłki. Żadnej wartości zgłoszonej w tytule.",
                    f"Ten HTML nie składa zgłoszenia celnego. Test adresu: {city}.",
                ]),
                ("Dla kogo", [
                    f"Pierwsze zamówienie do Polski i kto chce spreadsheet/finds/QC/wysyłkę PL na polskim hoście w {ccy}.",
                    "Niemiecka etykieta nie należy na tę stronę. Hosty siostrzane zostają osobnymi plikami.",
                ]),
                ("Błędy bez arkusza", [
                    f"Packstation, traktowanie {host} jako kasy, fracht przed QC. {post} może doliczyć Collect.",
                    "Rankingowy URL celny nie jest żywą taryfą.",
                ]),
                ("Jak używać sprawnie", [
                    f"Po QC {EST} do Polski. Źródło: {customs}.",
                    f"Bez zaniżania wartości. Płatność na {OFF}.",
                ]),
                ("Obowiązkowy?", [
                    "Nie. Aplikację szukasz ręcznie. Arkusz oszczędza martwe karty.",
                    f"{host} nie widzi konta.",
                ]),
                ("Gotowe", [
                    f"Finds, QC, wysyłka PL, potem {OFF}.",
                ]),
            ],
        )
    if kind == "finds":
        return (
            f"Najlepsze finds {A} dla Polski na {host}: QC magazyn na adres PL, nie drugi katalog świata.",
            [
                ("Co to finds", [
                    f"SKU ze zdjęciami magazynowymi na {host}. Nie skopiowane z listy DE ze zmienioną nazwą kraju.",
                    "Cena 0 = karta zdjęta, nie wyprzedaż.",
                ]),
                ("Dlaczego kuracja", [
                    f"Zdjęcia w Chinach zanim {post} pojedzie do {city}.",
                    f"{ccy}, cel PL, kod 00-001. Nie Packstation.",
                ]),
                ("Kategorie", [
                    "Sneakersy i bluzy mają QC. Restricted poza listą.",
                    "Angielskie klucze to etykiety.",
                ]),
                ("Dobór", [
                    f"Żywy URL, zdjęcie, kalkulator Polska. {city}.",
                    "Fail-QC wylatuje.",
                ]),
                ("Bezpieczniej?", [
                    f"Czytaj {customs} ({curl}) w dniu wysyłki. Find = zdjęcia przed frachtem, nie duty-free.",
                ]),
                ("Dla kogo", [
                    "Tylko drzwi w Polsce. Pierwsze zamówienie: odzież ze zdjęciami.",
                    "Niemiecki automat to nie ten desk.",
                ]),
                ("Dalej", [
                    f"QC, potem wysyłka PL. {OFF}.",
                ]),
            ],
        )
    if kind == "qc":
        return (
            f"QC na {host}: zdjęcia magazynowe w aplikacji {A} w Chinach, zanim zapłacisz fracht do Polski.",
            [
                ("Co to QC", [
                    "Kąty magazynowe, nie skaner KAS.",
                    "Zdjęcia lądują w aplikacji, dopóki SKU jest w Chinach.",
                ]),
                ("Dodatkowe zdjęcia", [
                    f"Dopóki leży w magazynie. Gdy {post} ma karton, {customs} nie robi powtórki.",
                    "Dodatkowe kąty często płatne. Ten HTML nie otwiera ticketów.",
                ]),
                ("Czego QC nie robi", [
                    f"Nie składa zgłoszenia i nie wymyśla wartości. {curl}.",
                    "Czysty album ≠ późniejszy pass platformy.",
                ]),
                ("QC i adres PL", [
                    f"Cel Polska, {city}. Packstation to złe państwo.",
                    "Zdjęcia w Chinach. Część PL to drzwi po QC.",
                ]),
                ("Gdy pada", [
                    "Zwrot w aplikacji. Bez frachtu międzynarodowego na reject.",
                    f"Taniej w Chinach niż po {post}.",
                ]),
                ("Wysyłka?", [
                    f"Potem {EST} do Polski. {host} nie kasuje.",
                ]),
            ],
        )
    if kind == "shipping":
        return (
            f"Wysyłka {A} do Polski używa kodu PL kalkulatora, nie tej domeny. Live formularz po QC. Last-mile często {post}.",
            [
                ("Trasa", [
                    f"Magazyn → QC → linia cel Polska → {post}. {host} nie drukuje live quote.",
                    f"Etykieta chce {city}. Cel PL w {EST} w dniu wysyłki.",
                ]),
                ("Opcje", [
                    "Tax-free / prepaid / odbiorca = SKU. Collect może doliczyć opłaty ukryte przez kalkulator.",
                    f"{post} może doliczyć odprawę Collect. BLIK to szyna PL w aplikacji — potwierdź tam.",
                ]),
                ("Czas", [
                    "Dni zmieniają się z SKU. Ta strona nie wymyśla dni InPost.",
                    "Magazyn ≠ tranzyt międzynarodowy.",
                ]),
                ("Koszt", [
                    f"Fracht plus granica według SKU. Żadnej kwoty w tytule. {ccy} to wyświetlanie. Kasa {OFF}.",
                ]),
                ("Cło", [
                    f"{customs} {curl} w dniu wysyłki. Rankingowe URL zostają; to nie żywa taryfa.",
                    "Bez zaniżania. Polski kod, nie niemiecki automat.",
                ]),
                ("Ryzyka", [
                    "Packstation, fracht przed QC, czeski kod.",
                    "Restricted nie jedzie linią PL, jeśli aplikacja blokuje przy submit.",
                ]),
                ("Pierwsze zamówienie", [
                    f"{host} mapa, {OFF} kasa. {city}. Źródło {customs}.",
                    "Jedna SKU odzieży, QC, rezerwacja.",
                ]),
                ("Gotowe", [
                    f"QC, potem {EST} do PL. Tylko {OFF}.",
                ]),
            ],
        )
    if kind == "legal":
        return (
            f"{A} jest agentem zakupowym. {host} tłumaczy ścieżkę PL; to nie {customs}. Czytaj KAS w dniu wysyłki.",
            [
                ("Czy to legalne w Polsce?", [
                    f"Korzystanie z agenta nie jest przestępstwem. Restricted i SKU zostają. {curl}.",
                    "Legalne = model agenta. Nie każda SKU Taobao przejdzie przez KAS.",
                ]),
                ("Czy to bezpieczne?", [
                    f"Bezpieczne = QC przed frachtem, płatność w aplikacji, prawdziwy adres PL — nie omijanie {customs}.",
                    f"{ccy}, cel PL, {city}. {host} nie trzyma karty.",
                ]),
                ("Ryzyka", [
                    f"Martwe linki, Collect bez SKU, {host} jako kasa. {post} może doliczyć opłatę.",
                    "Packstation to złe państwo.",
                ]),
                ("Jak zejść z ryzyka", [
                    f"QC, kalkulator Polska, {city}. Bez zaniżania wartości.",
                    "Spreadsheet, finds i QC razem.",
                ]),
                ("Pierwsze zamówienie", [
                    f"Start na {host}, rejestr na {OFF}. Restricted poza listą.",
                ]),
                ("Werdykt", [
                    f"Używalne do Polski z aplikacją i {customs}. Niezależna informacja. {OFF}.",
                ]),
                ("Start", [
                    "Spreadsheet → finds → QC → wysyłka PL.",
                ]),
            ],
        )
    if kind == "guide":
        return (
            f"Krok po kroku {A} na adres w Polsce na {host}. Zdjęcia magazynowe, potem fracht.",
            [
                ("Jak kupować (PL)", [
                    f"SKU z QC, aplikacja, zdjęcia, fracht do Polski z {city}.",
                    f"Nie pomijaj QC. {post} nie robi powtórki zdjęcia.",
                ]),
                ("Czym jest BBDBuy", [
                    f"Agent. {host} tłumaczy PL w {ccy}. Płatność {OFF}.",
                    "Dwie płatności: towar, potem fracht po QC.",
                ]),
                ("Krok 1", [
                    "Spreadsheet/finds, angielskie klucze. Polskie słowa często zero kart.",
                    "Restricted i cena 0 poza listą.",
                ]),
                ("Krok 2", [
                    "QC w Chinach. Dodatkowe kąty często płatne.",
                    f"{customs} nie otwiera biletu magazynowego po {post}.",
                ]),
                ("Krok 3", [
                    f"{EST} cel Polska. Często {post}. {city}.",
                    "Bez wymyślonych dni InPost.",
                ]),
                ("Krok 4", [
                    f"Płać na {OFF}. {host} nie zapisuje karty.",
                ]),
                ("Błędy", [
                    "DE w kalkulatorze, fracht przed QC, host jako sklep.",
                    "Nie Packstation.",
                ]),
                ("Gotowe", [
                    f"Spreadsheet → finds → QC → wysyłka. {OFF}.",
                ]),
            ],
        )
    return (
        f"FAQ spreadsheet {A} Polska na {host}: indeks, QC, {post}, {customs}. Nie kasa.",
        [
            ("Czy ta strona sprzedaje towar?", [
                f"Nie. {A} jest agentem. Zamówienia zostają na {OFF}. {host} listuje finds do drzwi w Polsce — nie drugi magazyn, nie druga kasa.",
                "Karty na tej domenie to indeks, nie stock BBDBuy.",
            ]),
            ("Co to spreadsheet BBDBuy?", [
                f"Shortlista SKU ze zdjęciami magazynowymi dla {city}. Nie Excel, nie drugi sklep. Keywords: BBDBuy spreadsheet, bbdbuy spreadsheet polska, bbdbuy trusted sellers.",
                "Wiersz działa, dopóki link źródłowy żyje i jest choć jedno zdjęcie. Cena 0 albo restricted to martwe źródło.",
            ]),
            ("Jak używać zdjęć QC?", [
                "Lądują w oficjalnej aplikacji, dopóki rzecz jest w Chinach. Dodatkowe kąty tam, nie po last-mile.",
                f"{post} nie robi powtórki magazynowej, gdy karton jest już w Polsce. Tickety tylko w aplikacji.",
            ]),
            ("Jak działa wysyłka do Polski?", [
                f"Cel Polska w kalkulatorze, potem zarezerwowana SKU. Last-mile często {post}. Live quote: {EST}.",
                f"{city}. Ta strona nie wymyśla dni InPost ani stawki KAS. Packstation nie zastępuje polskiego kodu.",
            ]),
            ("Kto płaci cło i VAT importowy?", [
                f"Zarezerwowana SKU. {post} może doliczyć Collect, którego kalkulator nie pokazuje. Źródło: {curl} ({customs}).",
                "Rankingowe notatki celne na tym hoście to lokalne wskazówki, nie żywa taryfa. Bez wartości zgłoszonej na tej stronie.",
            ]),
            ("Dlaczego złote tutaj i dolary w SPA?", [
                f"Przeliczenie wyświetlania chińskiej karty magazynowej. Waluta kasy to to, co {OFF} pokazuje rano płatności. {ccy} na {host} to display.",
                f"Jeśli aplikacja nadal ma dolar, obowiązują cyfry i {EST} z celem Polska. BLIK potwierdzasz w aplikacji.",
            ]),
            ("Czy mogę użyć Packstation albo czeskiego kodu?", [
                "Nie. Niemiecki numer Packstation albo inny format kodu to złe państwo, nawet gdy aplikacja jest po polsku.",
                f"Polska chce {city}. Etykieta DE nie należy na ten desk.",
            ]),
            ("Gdzie się rejestruję?", [
                f"Tylko na {OFF}. {host} nie bierze karty, PayPal ani salda.",
                "Ten desk tłumaczy ścieżkę PL. Konto, portfel i tickety zostają na oficjalnej domenie.",
            ]),
        ],
    )
