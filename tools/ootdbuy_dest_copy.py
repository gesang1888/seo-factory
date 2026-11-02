"""Localized inner copy for OOTDBuy dest desks, UK-cluster depth.

Public pages: no ops notes, no declared-value coaching, no invented transit
days or duty rates. Unique coupons/community/qc-guide CMS are not rendered here.
Invite FCGYHLJWL stays off dest titles.
"""
from __future__ import annotations

A = "OOTDBuy"
OFF = "ootdbuy.com"
EST = "https://ootdbuy.com/estimation/"


def geo(dest: str) -> str:
    return {
        "NL": "nederland",
        "US": "usa",
        "CA": "canada",
        "GB": "uk",
        "DE": "deutschland",
    }.get(dest, dest.lower())


def inner_keywords(kind: str, d: dict) -> list[str]:
    g = geo(d["dest"])
    table = {
        "spreadsheet": [f"{A} spreadsheet", f"ootdbuy spreadsheet {g}", "ootdbuy trusted sellers"],
        "finds": ["ootdbuy finds", "ootdbuy spreadsheet finds", "best ootdbuy items"],
        "qc": ["ootdbuy qc", f"ootdbuy qc {g}", "ootdbuy warehouse photos"],
        "shipping": ["ootdbuy shipping", f"ootdbuy shipping {g}", "ootdbuy delivery time"],
        "legal": ["ootdbuy safe", "ootdbuy legit", f"ootdbuy safe {g}"],
        "guide": ["ootdbuy spreadsheet guide", "how to use ootdbuy", "ootdbuy buying guide"],
        "faq": ["ootdbuy faq", "ootdbuy spreadsheet faq", "ootdbuy questions"],
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
        },
        "finds": {
            "nl": f"Beste {A} finds – Nederland 2026",
            "us": f"Top {A} Spreadsheet Finds – Best US Picks 2026",
            "ca": f"Top {A} Spreadsheet Finds – Best Canada Picks 2026",
            "uk": f"Top {A} Spreadsheet Finds – Best UK Picks 2026",
            "de": f"{A} spreadsheet finds – Auswahl Deutschland 2026",
        },
        "qc": {
            "nl": f"{A} QC-foto’s Nederland – magazijncheck",
            "us": f"{A} QC Photos for US Buyers – Warehouse Check",
            "ca": f"{A} QC Photos for Canada Buyers – Warehouse Check",
            "uk": f"{A} QC Photos for UK Buyers – Warehouse Check",
            "de": f"{A} QC-Fotos nach Deutschland – Lagercheck",
        },
        "shipping": {
            "nl": f"{A} verzending Nederland – kosten, tijd en DHL",
            "us": f"{A} Shipping to the USA – Cost, Time & USPS",
            "ca": f"{A} Shipping to Canada – Cost, Time & Canada Post",
            "uk": f"{A} Shipping to the UK – Cost, Time & Royal Mail",
            "de": f"{A} Versand nach Deutschland – Preis, Zeit und DHL",
        },
        "legal": {
            "nl": f"Is {A} veilig en legaal in Nederland?",
            "us": f"Is {A} Safe & Legal for US Buyers? Full Guide",
            "ca": f"Is {A} Safe & Legal for Canada Buyers? Full Guide",
            "uk": f"Is {A} Safe & Legal for UK Buyers? Full Guide",
            "de": f"Ist {A} sicher und legal in Deutschland?",
        },
        "guide": {
            "nl": f"{A}-spreadsheet gebruiken – startergids NL",
            "us": f"How to Use {A} Spreadsheet – Beginner Guide USA",
            "ca": f"How to Use {A} Spreadsheet – Beginner Guide Canada",
            "uk": f"How to Use {A} Spreadsheet – Beginner Guide UK",
            "de": f"{A}-Spreadsheet nutzen – Start für Deutschland",
        },
        "faq": {
            "nl": f"{A} spreadsheet FAQ – gids Nederland 2026",
            "us": f"{A} Spreadsheet FAQ – US Buyers Guide 2026",
            "ca": f"{A} Spreadsheet FAQ – Canada Buyers Guide 2026",
            "uk": f"{A} Spreadsheet FAQ – UK Buyers Guide 2026",
            "de": f"{A} Spreadsheet FAQ – Leitfaden Deutschland",
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
        },
        "finds": {
            "nl": f"Beste {A} finds voor Nederland (2026)",
            "us": f"Top {A} Finds for US Buyers (2026 Guide)",
            "ca": f"Top {A} Finds for Canada Buyers (2026 Guide)",
            "uk": f"Top {A} Finds for UK Buyers (2026 Guide)",
            "de": f"{A} Finds für Käufer in Deutschland (2026)",
        },
        "qc": {
            "nl": f"{A} QC-foto’s vóór verzending naar Nederland",
            "us": f"{A} QC photos before shipping to the United States",
            "ca": f"{A} QC photos before shipping to Canada",
            "uk": f"{A} QC photos before shipping to the United Kingdom",
            "de": f"{A} QC-Fotos vor dem Versand nach Deutschland",
        },
        "shipping": {
            "nl": f"{A} verzending naar Nederland",
            "us": f"{A} shipping to the United States",
            "ca": f"{A} shipping to Canada",
            "uk": f"{A} shipping to the United Kingdom",
            "de": f"{A} Versand nach Deutschland",
        },
        "legal": {
            "nl": f"Is {A} veilig en legaal in Nederland?",
            "us": f"Is {A} safe and legal for US buyers?",
            "ca": f"Is {A} safe and legal for Canada buyers?",
            "uk": f"Is {A} safe and legal for UK buyers?",
            "de": f"Ist {A} sicher und legal in Deutschland?",
        },
        "guide": {
            "nl": f"Kopen via {A}: stappenplan voor Nederland",
            "us": f"How to buy with {A}: US address steps",
            "ca": f"How to buy with {A}: Canada address steps",
            "uk": f"How to buy with {A}: UK address steps",
            "de": f"Kaufen über {A}: Schritte für eine deutsche Adresse",
        },
        "faq": {
            "nl": f"{A} FAQ voor kopers in Nederland (2026)",
            "us": f"{A} FAQ for US Buyers (2026)",
            "ca": f"{A} FAQ for Canada Buyers (2026)",
            "uk": f"{A} FAQ for UK Buyers (2026)",
            "de": f"{A} FAQ für Käufer in Deutschland (2026)",
        },
    }
    return table[kind][key]


def sections_for(kind: str, d: dict, host: str):
    h1 = inner_h1(kind, d)
    fn = {"nl": _nl, "us": _us, "ca": _ca, "uk": _uk, "de": _de}[d["key"]]
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
                f"Copy the product URL from the Chinese shop, paste it on {OFF}, and OOTDBuy buys it into the warehouse. {host} is the spreadsheet and guide for that path toward a UK door.",
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
                f"Paste the Chinese shop URL on {OFF}. OOTDBuy buys into the warehouse, then you book a line toward a US door after QC.",
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
                f"Paste the Chinese shop URL on {OFF}. OOTDBuy buys into the warehouse, then you book a line toward a Canada Post door after QC.",
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
                f"Auf dem Label stehen eine deutsche Straße und eine fünfstellige PLZ. Packstation-Nummern sind ein DE-Muster — {city}. Eine österreichische 1010 Wien oder eine vierstellige AT-PLZ ist das falsche Land, auch wenn die App Deutsch anzeigt.",
                f"Öffne {EST} und setze das Ziel auf Deutschland, bevor du internationale Fracht zahlst. Der Schätzer entscheidet die SKU, nicht dieser Hostname.",
            ]),
            (f"Preise in {ccy}", [
                f"Die Karten auf dieser Seite zeigen Finds in {ccy}. Du zahlst auf {OFF} — Karte, PayPal oder Guthaben, je nachdem, was das Konto an dem Morgen anbietet.",
                f"Steht in der offiziellen App noch ein Dollarzeichen, gilt die Zahl in der App und der Rechner {EST} mit Ziel Deutschland. Diese Seite ist keine Kasse.",
            ]),
            ("Taobao-, 1688- oder Weidian-Link einfügen", [
                f"Kopiere die Produkt-URL aus dem chinesischen Shop, füge sie auf {OFF} ein. OOTDBuy kauft in dein Lager. {host} ist das Spreadsheet und die Anleitung für den Weg zu einer deutschen Tür.",
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
                f"Kopieer de product-URL uit de Chinese shop en plak die op {OFF}. OOTDBuy koopt naar het magazijn. {host} is de spreadsheet en de handleiding naar een Nederlandse deur.",
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
    }
    return packs[key]


def extra_faq(d: dict, host: str) -> list:
    post, city, customs, curl, ccy = d["post"], d["city"], d["customs"], d["customs_url"], d["ccy"]
    key = d["key"]
    packs = {
        "uk": [
            ("Does OOTDBuy sell the goods on this site?", [
                f"No. OOTDBuy is a purchasing agent: it buys from Chinese third-party shops in your name, photographs the parcel in its warehouse, then you book an international SKU. {host} is a spreadsheet for a UK door. Orders, payment and claims stay on {OFF}.",
            ]),
            ("Can I pay on this hostname?", [
                f"No. Register and pay only on {OFF}. {host} never takes a card. Display currency here is {ccy}; the live amount is in the app.",
            ]),
            ("Which estimator country do I pick?", [
                f"United Kingdom — not this TLD, not EU, not Ireland. Open {EST} before you pay freight. {city}.",
            ]),
            ("Does QC happen in the UK?", [
                f"No. Warehouse photos are taken in China. {post} is last-mile after you accept QC. Extra angles are an in-app add-on.",
            ]),
            ("Who pays import VAT?", [
                f"The booked SKU decides prepaid vs collect. {post} can add a handling fee. Read {curl} ({customs}) the morning you ship. This page does not invent a declared value.",
            ]),
            ("Is Northern Ireland the same SKU?", [
                f"Often not. Northern Ireland can be another carrier product than mainland {post}. Pick the live line in the app; do not swap the country name on this desk.",
            ]),
            ("Why do Dutch words return zero cards?", [
                "They should — this desk is English for UK buyers. Local-language catalogue words often return zero because the index keys are sneakers, hoodie, jacket.",
            ]),
            ("Where is the invite code?", [
                f"Not in this title. Coupon and invite URLs already on {host} stay as they are. New cluster titles do not paste a code.",
            ]),
        ],
        "us": [
            ("Does OOTDBuy sell the goods on this site?", [
                f"No. OOTDBuy buys from Chinese shops in your name. {host} is a spreadsheet toward a US ZIP. Checkout stays on {OFF}.",
            ]),
            ("Can I pay here?", [
                f"No. Pay on {OFF}. This page shows {ccy} as display. Live freight is {EST} with destination United States.",
            ]),
            ("Which estimator country?", [
                f"United States — not this TLD, not Canada. A Canadian A1A 1A1 code is the wrong country. {city}.",
            ]),
            ("Does QC happen at USPS?", [
                f"No. Photos are taken in the China warehouse. {post} or FedEx is last-mile after you accept QC.",
            ]),
            ("Who pays duty?", [
                f"The booked SKU. This page does not invent a de-minimis dollar. Source: {curl} ({customs}) the morning you ship.",
            ]),
            ("Is a Canada Post SKU the same?", [
                "No. A Canadian postal code is a different country. Stay on this US desk for a US ZIP.",
            ]),
            ("Why do local words return zero cards?", [
                "The finds index is English (sneakers, hoodie, jacket). That is not an empty shop.",
            ]),
            ("Where is the invite code?", [
                f"Not in this title. Existing coupon URLs on {host} stay. New titles do not paste a code.",
            ]),
        ],
        "ca": [
            ("Does OOTDBuy sell the goods on this site?", [
                f"No. OOTDBuy is the purchasing agent. {host} is a spreadsheet toward a Canadian postal code. Pay on {OFF}.",
            ]),
            ("Can I pay here?", [
                f"No. Pay on {OFF}. Display here is {ccy}. Live freight is {EST} with destination Canada.",
            ]),
            ("Which estimator country?", [
                f"Canada — not this TLD, not US. A US ZIP is the wrong country. {city}.",
            ]),
            ("Does QC happen at Canada Post?", [
                f"No. Photos are taken in China. {post} is last-mile after you accept QC.",
            ]),
            ("Who pays GST/HST on import?", [
                f"The booked SKU. Read {curl} ({customs}) the morning you ship. This page does not invent a declared value.",
            ]),
            ("Is a USPS SKU the same?", [
                "No. A US ZIP is a different country. Stay on this Canadian desk for an A1A 1A1 label.",
            ]),
            ("Why do French catalogue words return zero?", [
                "The index keys are English (sneakers, hoodie, jacket). Type the English key.",
            ]),
            ("Where is the invite code?", [
                f"Not in this title. Ranked coupon URLs on {host} stay as they are.",
            ]),
        ],
        "de": [
            ("Verkauft OOTDBuy die Ware auf dieser Seite?", [
                f"Nein. OOTDBuy ist Einkaufsagent. {host} ist das Spreadsheet zu einer deutschen Tür. Bestellen und zahlen nur auf {OFF}.",
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
                f"Die gebuchte SKU. Quelle am Versandmorgen: {curl} ({customs}). Diese Seite nennt keinen Deklarationsbetrag.",
            ]),
            ("Ist Österreich dieselbe SKU?", [
                "Nein. Eine vierstellige AT-PLZ ist das falsche Land. Dieses Desk bleibt Deutschland.",
            ]),
            ("Warum findet der Katalog nichts auf Deutsch?", [
                "Der Index ist englisch (sneakers, hoodie, jacket). Das ist kein leerer Shop.",
            ]),
            ("Wo steht der Invite-Code?", [
                f"Nicht in diesem Title. Vorhandene Coupon-URLs auf {host} bleiben. Neue Cluster-Titel kleben keinen Code.",
            ]),
        ],
        "nl": [
            ("Verkoopt OOTDBuy de spullen op deze site?", [
                f"Nee. OOTDBuy is inkoopagent. {host} is de spreadsheet naar een Nederlandse deur. Bestellen en betalen alleen op {OFF}.",
            ]),
            ("Kan ik hier betalen?", [
                f"Nee. Betalen op {OFF}. Weergave hier in {ccy}. Live vracht: {EST} met bestemming Nederland. iDEAL bevestig je in de app.",
            ]),
            ("Welk estimator-land?", [
                f"Nederland — niet deze TLD, niet BE, niet EU. {city}. Een Belgische postcode is het verkeerde land.",
            ]),
            ("Gebeurt QC bij PostNL?", [
                f"Nee. Magazijnfoto’s komen uit China. {post} is last-mile na geaccepteerde QC.",
            ]),
            ("Wie betaalt invoer?", [
                f"De geboekte SKU. Bron die ochtend: {curl} ({customs}). Deze pagina verzint geen aangegeven waarde.",
            ]),
            ("Is België dezelfde SKU?", [
                "Nee. Een Belgische viercijferige postcode is het verkeerde land. Dit desk blijft Nederland.",
            ]),
            ("Waarom vindt de catalogus niets in het Nederlands?", [
                "De index is Engels (sneakers, hoodie, jacket). Dat is geen lege shop.",
            ]),
            ("Waar staat de invite-code?", [
                f"Niet in deze title. Bestaande coupon-URL’s op {host} blijven. Nieuwe cluster-titels plakken geen code.",
            ]),
        ],
    }
    return packs[key]


def more_depth(d: dict, host: str) -> list:
    post, city, customs, curl, ccy = d["post"], d["city"], d["customs"], d["customs_url"], d["ccy"]
    key = d["key"]
    packs = {
        "uk": [
            ("Warehouse in China, not a Royal Mail depot", [
                f"QC photos are taken in the OOTDBuy warehouse in China. A {post} depot in the UK is last-mile, not a second QC studio. Ask for extra angles in the app before you pay freight to the United Kingdom.",
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
                f"{host} is a spreadsheet and guide toward a UK door. It is not a second OOTDBuy till, not {customs}, not {post} customer service. Register and tickets only on {OFF}.",
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
                f"QC photos are taken in the OOTDBuy warehouse in China. A {post} depot in the United States is last-mile, not a second QC studio. Ask for extra angles in the app before you pay freight to the United States.",
                f"Storage days are in official Help on {OFF}. After QC, open {EST} with destination United States. {city}.",
            ]),
            ("First order: one clothing SKU", [
                f"For the first US door, one hoodie or a pair of sneakers with warehouse photos is enough. Consolidating un-QCd pieces on the first invoice mixes {customs} and Collect.",
                f"Restricted, perfume, batteries and liquids stay off until the app allows them the morning you ship.",
            ]),
            ("English catalogue keys are labels", [
                "The category wall says sneakers, hoodie, jacket, bag because the index is English. Local words often return zero cards — that is not an empty shop.",
                f"Estimator country stays the United States, {ccy} is display, checkout is {OFF}.",
            ]),
            ("What this hostname is not", [
                f"{host} is a spreadsheet toward a US door. It is not a second OOTDBuy till, not {customs}, not {post} customer service. Register only on {OFF}.",
                "A Canadian postal code in the A1A 1A1 pattern is the wrong country.",
            ]),
            ("Tracking after the border", [
                f"Warehouse status lives in the app. After the international line, tracking follows the SKU — often {post} or FedEx.",
                f"Who pays duty and Collect is the booked SKU. Source: {curl} ({customs}). This page does not invent a de-minimis dollar.",
            ]),
            ("Returns only in the warehouse", [
                f"Fail-QC is handled in-app while the piece is in China. After {post} delivered, {customs} does not reopen a warehouse ticket.",
                f"Two payments stay normal. {OFF}.",
            ]),
            ("Neighbour countries are other SKUs", [
                f"{city} is the address test. A Canadian A1A 1A1 code in the estimator is the wrong country.",
                f"A ranked duty article on {host} is not a live tariff. Confirm in the app and on CBP the day you ship.",
            ]),
        ],
        "ca": [
            ("Warehouse in China, not a Canada Post depot", [
                f"QC photos are taken in the OOTDBuy warehouse in China. A {post} depot in Canada is last-mile, not a second QC studio.",
                f"Storage days are in official Help on {OFF}. After QC, open {EST} with destination Canada. {city}.",
            ]),
            ("First order: one clothing SKU", [
                f"For the first Canadian door, one hoodie or a pair of sneakers with warehouse photos is enough.",
                "Restricted, perfume, batteries and liquids stay off until the app allows them the morning you ship.",
            ]),
            ("English catalogue keys are labels", [
                "The category wall says sneakers, hoodie, jacket, bag because the index is English. Canadian words often return zero cards — that is not an empty shop.",
                f"Estimator country stays Canada, {ccy} is display, checkout is {OFF}.",
            ]),
            ("What this hostname is not", [
                f"{host} is a spreadsheet toward a Canadian door. It is not a second OOTDBuy till, not {customs}, not {post} customer service. Register only on {OFF}.",
                "A US ZIP is the wrong country.",
            ]),
            ("Tracking after the border", [
                f"Warehouse status lives in the app. After the international line, tracking follows the SKU — often {post}.",
                f"Who pays GST/HST and Collect is the booked SKU. Source: {curl} ({customs}).",
            ]),
            ("Returns only in the warehouse", [
                f"Fail-QC is handled in-app while the piece is in China. After {post} delivered, {customs} does not reopen a warehouse ticket.",
                f"Two payments stay normal. {OFF}.",
            ]),
            ("Neighbour countries are other SKUs", [
                f"{city} is the address test. A US ZIP in the estimator is the wrong country.",
                f"A ranked GST article on {host} is not a live tariff. Confirm in the app and on CBSA the day you ship.",
            ]),
        ],
        "de": [
            ("Lager in China, kein DHL-Depot", [
                f"QC-Fotos entstehen im OOTDBuy-Lager in China. Ein {post}-Depot in Deutschland ist letzte Meile, kein zweites QC-Studio. Extra-Winkel in der App anfragen, bevor du Fracht nach Deutschland zahlst.",
                f"Lagerdauer steht in der Help auf {OFF}. Nach QC {EST} mit Ziel Deutschland öffnen. {city}.",
            ]),
            ("Erste Bestellung: eine Kleidungs-SKU", [
                f"Für die erste deutsche Tür reicht ein Hoodie oder ein Paar Sneaker mit Lagerfotos. Ungeprüftes Bündeln auf der ersten Rechnung vermischt {customs} und Nachnahme.",
                "Restricted, Parfum, Akkus und Flüssigkeiten bleiben draußen, bis die App sie am Versandmorgen erlaubt.",
            ]),
            ("Englische Katalogschlüssel sind Labels", [
                "Die Kategorie-Wand sagt sneakers, hoodie, jacket, bag, weil der Index englisch ist. Deutsche Wörter liefern oft 0 Karten — das ist kein leerer Shop.",
                f"Schätzer-Land bleibt Deutschland, {ccy} ist Anzeige, Kasse ist {OFF}.",
            ]),
            ("Was dieser Hostname nicht ist", [
                f"{host} ist Spreadsheet und Anleitung zu einer deutschen Tür. Keine zweite OOTDBuy-Kasse, kein {customs}, kein {post}-Kundendienst. Registrieren nur auf {OFF}.",
                "Packstation ist DE. 1010 Wien ist AT.",
            ]),
            ("Sendungsverfolgung nach der Grenze", [
                f"Im Lager siehst du den Status in der App. Nach der internationalen Linie folgt das Tracking der SKU — oft {post}. Nachnahme kann an der Tür erscheinen.",
                f"Wer Zoll und Collect zahlt, steht auf der SKU. Quelle: {curl} ({customs}). Kein Deklarationsbetrag auf dieser Seite.",
            ]),
            ("Retouren nur im Lager", [
                f"Fail-QC oder falsche Größe läuft in der App, solange das Teil in China ist. Nach {post}-Zustellung öffnet {customs} kein Lagerticket.",
                f"Zwei Zahlungen bleiben normal. {OFF}.",
            ]),
            ("Nachbarländer sind andere SKUs", [
                f"{city} ist der Adresstest. Eine österreichische PLZ im Schätzer ist das falsche Land.",
                f"Ein gerankter Zollartikel auf {host} ist kein Live-Tarif. In der App und auf zoll.de am Versandtag prüfen, dann buchen.",
            ]),
        ],
        "nl": [
            ("Magazijn in China, geen PostNL-depot", [
                f"QC-foto’s komen uit het OOTDBuy-magazijn in China. Een {post}-depot in Nederland is last-mile, geen tweede QC-studio. Vraag extra hoeken in de app vóór je vracht naar Nederland betaalt.",
                f"Magazijndagen staan in de Help op {OFF}. Na QC open je {EST} met bestemming Nederland. {city}.",
            ]),
            ("Eerste bestelling: één kleding-SKU", [
                f"Voor de eerste Nederlandse deur volstaat een hoodie of een paar sneakers met magazijnfoto’s. Ongecheckte stukken bundelen op de eerste factuur mengt {customs} en Collect.",
                "Restricted, parfum, accu’s en vloeistoffen blijven eraf tot de app ze de ochtend van verzending toestaat.",
            ]),
            ("Engelse catalogsleutels zijn labels", [
                "De categorie-muur zegt sneakers, hoodie, jacket, bag omdat de index Engels is. Nederlandse woorden geven vaak 0 kaarten — dat is geen lege shop.",
                f"Estimator-land blijft Nederland, {ccy} is weergave, kassa is {OFF}.",
            ]),
            ("Wat deze hostname niet is", [
                f"{host} is spreadsheet en handleiding naar een Nederlandse deur. Geen tweede OOTDBuy-kassa, geen {customs}, geen {post}-klantenservice. Registreren alleen op {OFF}.",
                "Een Belgische viercijferige postcode is het verkeerde land. iDEAL bevestig je in de app, niet hier.",
            ]),
            ("Tracking na de grens", [
                f"In het magazijn zie je status in de app. Na de internationale lijn volgt tracking de SKU — vaak {post}. Collect kan aan de deur verschijnen.",
                f"Wie invoer en Collect betaalt, staat op de SKU. Bron: {curl} ({customs}). Deze pagina plakt geen tarief in de title.",
            ]),
            ("Retour alleen in het magazijn", [
                f"Fail-QC of verkeerde maat loopt in de app zolang het stuk in China is. Na {post}-bezorging heropent {customs} geen magazijnticket.",
                f"Twee betalingen blijven normaal. {OFF}.",
            ]),
            ("Buurlanden zijn andere SKUs", [
                f"{city} is de adres-test. Een Belgische postcode in de estimator is het verkeerde land.",
                f"Een gerankte btw-pagina op {host} is geen live tarief. Bevestig in de app en bij Douane op de verzenddag, dan boek je de lijn.",
            ]),
        ],
    }
    return packs[key]


def wrap_copy(host: str, d: dict, keep_slug: str):
    h1 = inner_h1("guide", d)
    lead = f"Guide pages on {host} stay on this hostname. Ranked copy for /{keep_slug}/ is the keep URL."
    secs = extra_local(d, host)[:2]
    return h1, lead, secs


def _core_en(kind, host, d, dest_name, neighbour, last_mile_note):
    post, city, customs, curl, ccy = d["post"], d["city"], d["customs"], d["customs_url"], d["ccy"]
    if kind == "spreadsheet":
        return (
            f"A curated {A} spreadsheet for {dest_name} buyers on {host}: trusted sellers, QC photos and finds in one index. It is not Excel and not checkout. Order on {OFF} in {ccy} after you pick destination {dest_name}.",
            [
                (f"What is an {A} spreadsheet?", [
                    f"An {A} spreadsheet on {host} is a shortlist of warehouse-checked SKUs meant for a {dest_name} delivery address — sneakers, hoodies, jackets and bags that still open in the official app. It does not take payment and it is not a second OOTDBuy storefront.",
                    f"Rows stay useful only while the source link is live and at least one warehouse photo exists. A price-0 or restricted card is a dead source, not a discount. Keywords: OOTDBuy spreadsheet, ootdbuy spreadsheet {geo(d['dest'])}, ootdbuy trusted sellers.",
                ]),
                (f"Why {dest_name} buyers start with a sheet", [
                    f"Searching Taobao, 1688 and Weidian by hand dumps thousands of expired cards. The sheet keeps finds you already accepted in QC before you ask {post} to move a carton toward {city}.",
                    f"{neighbour} This page is written for {dest_name}, {ccy}, and {customs}.",
                ]),
                (f"How {A} spreadsheets work", [
                    f"Open a find on {host}, read warehouse photos in the official {A} app, then book an international line with destination {dest_name}. {host} only explains that order. Cart, wallet and tickets stay on {OFF}.",
                    f"English catalogue keys (sneakers, hoodie, jacket) on the wall are display labels. Live money is in {EST}.",
                ]),
                ("What types of products are included?", [
                    "Shoes, hoodies, jackets, bags and watches dominate because those SKUs still have QC angles. Electronics, perfume, liquids and other restricted classes stay off the sheet unless the official app shows them as allowed the morning you submit.",
                    "A find that passed QC last month can still go restricted. Recheck the official product page before you pay freight.",
                ]),
                (f"Is using an {A} spreadsheet safer?", [
                    f"Safer here means you saw warehouse photos before international freight — not that {customs} disappears. Read {curl} the morning you ship. This page does not paste a rate into the title.",
                    f"The sheet also keeps you off dead Weidian links. It does not file a {customs} entry and it does not pick a declared value for you. {city}.",
                ]),
                (f"Who should use an {A} spreadsheet?", [
                    f"First-time {dest_name} buyers who need an address test and anyone who already uses {A} but wants spreadsheet, finds, QC and shipping in one site in {ccy}.",
                    f"If you ship to a different country, this is the wrong page. Orders stay on {OFF}.",
                ]),
                ("Common mistakes without a spreadsheet", [
                    f"Pasting the wrong country into the estimator, treating {host} as checkout, or booking freight before QC. Last-mile is often {post}; Collect can add a fee the estimator hides.",
                    f"Another miss: assuming a ranked duty article on this site is a live tariff. Confirm in the official app and on {customs} the day you ship.",
                ]),
                ("How to use a spreadsheet efficiently", [
                    f"Keep spreadsheet, finds and QC in one tab set. When a find is accepted, open the official freight form toward {dest_name}. Source: {customs}.",
                    f"Skip under-declaration tricks. Pay what the booked SKU and {EST} show. Orders stay on {OFF}.",
                ]),
                (f"Is an {A} spreadsheet required?", [
                    "No. You can search the official app by hand. The sheet exists so buyers are not starting from thousands of dead cards every week.",
                    f"You still register and pay on {OFF}. {host} never sees the account.",
                ]),
                (f"Ready to use an {A} spreadsheet?", [
                    f"Use the cluster links for finds, QC photos and shipping to {dest_name}. Then register on {OFF}. This site stays an index in {ccy}.",
                ]),
            ],
        )
    if kind == "finds":
        return (
            f"Top {A} spreadsheet finds for {dest_name} buyers on {host}: QC-checked sneakers, hoodies and bags aimed at a {dest_name} address, not a second global catalogue.",
            [
                (f"What are top {A} finds?", [
                    f"Finds on {host} are SKUs kept after warehouse photos — usually shoes, jackets and bags that still open in the official app. They are not a shop window and they are not copied from another country list with the name swapped.",
                    "A find drops off when the source URL dies or the warehouse no longer has the piece. Price-0 is a removed card, not a sale.",
                ]),
                (f"Why {dest_name} buyers use curated {A} finds", [
                    f"Manual search mixes dead Weidian links with live cards. Curated finds are the ones that still photograph in China before you book {post} toward {city}.",
                    f"{ccy} display on this desk, destination {dest_name}, and a real local postcode beat hunting forum screenshots that never list a {customs} path.",
                ]),
                ("Popular product categories", [
                    "Sneakers and hoodies fill the wall because those lots still have QC angles. Bags and jackets follow. Restricted goods stay off even if a forum names them.",
                    "Category keys on this site are English display labels. They do not change the estimator country.",
                ]),
                ("How these finds are selected", [
                    f"A find needs a live source URL, at least one warehouse photo, and estimator destination {dest_name} — not this hostname as a country. {city} is the address test.",
                    "We do not keep a find because it was popular last season. If QC fails, it leaves the list.",
                ]),
                (f"Are {A} finds safer than searching manually?", [
                    f"You still read {customs} ({curl}) the morning you ship. A find only means the piece was photographed in China before international freight.",
                    "Safer is not duty-free. Import charges and Collect can still apply. This page does not invent a figure.",
                ]),
                (f"Who should use top {A} finds?", [
                    f"Buyers who already have a {dest_name} door and want QC’d picks. First orders should stay on simple clothing SKUs with photos.",
                    f"If your label matches {city}, stay on this site. Sister country pages are separate files.",
                ]),
                (f"Ready to explore top {A} finds?", [
                    f"Open QC next, then shipping to {dest_name}. Register and pay on {OFF}. {host} is information only.",
                ]),
            ],
        )
    if kind == "qc":
        return (
            f"QC on {host} means warehouse photos in the official {A} app, taken in China, before you pay freight to {dest_name}.",
            [
                ("What QC is on this site", [
                    f"Quality check is extra angles of the piece in the warehouse — seams, tags, sole, print. It is not a laboratory, not a brand-authentication court, and not a {customs} x-ray.",
                    "Photos land in the official app while the SKU is still in China. That is the only window that matters for a retake.",
                ]),
                ("When to ask for extra photos", [
                    f"Ask while the SKU is in the warehouse. After {post} has the carton, {customs} is the wrong office for a warehouse retake.",
                    "Extra angles are often a paid add-on in the official app. Open tickets in the OOTDBuy app.",
                ]),
                ("What QC does not do", [
                    f"QC does not file a {customs} entry, does not pay import tax, and does not invent a declared value. Educational source: {curl}.",
                    "A clean QC album is not a promise the SKU will pass a later platform rule. Recheck before you book the line.",
                ]),
                (f"QC and a {dest_name} address", [
                    f"Use destination {dest_name} and {city} in the estimator. {neighbour}",
                    f"Warehouse photos are taken in China either way. The {dest_name} part is the door on the label after you accept QC.",
                ]),
                ("If a find fails QC", [
                    "Leave it in the warehouse or return it in the official app. Do not book international freight on a reject just to get it over with.",
                    f"Failed QC is cheaper in China than after {post} attempts delivery.",
                ]),
                ("Ready to ship after QC?", [
                    f"Only then open {EST} toward {dest_name}. {host} does not take payment. {ccy} totals live in the app.",
                ]),
            ],
        )
    if kind == "shipping":
        return (
            f"{A} shipping to {dest_name} uses the official estimator, not this domain. Open the live freight form after warehouse photos. Last-mile is often {post}.",
            [
                (f"How {A} shipping to {dest_name} works", [
                    f"Warehouse in China → you accept QC → you book a line with destination {dest_name} → {post} or the SKU’s last-mile partner hands it over. {host} does not print a live quote.",
                    f"The label needs {city}. Confirm destination in {EST} the morning you ship. {last_mile_note}",
                ]),
                (f"{A} shipping options for {dest_name} buyers", [
                    "Tax-free, prepaid and collect are properties of the booked SKU in the official app. This page does not rename them. Collect can add a fee the estimator hides.",
                    f"{post} may also add a handling fee on collect parcels. Read the SKU, then the live estimator — not a screenshot from last year.",
                ]),
                ("Weight, volume and the calculator", [
                    f"Most air SKUs bill max(actual, L×W×H/divisor). A puffy jacket is light on the scale and expensive in volume. Geometry only — live money is {EST} with destination {dest_name}.",
                    "The lab habit of 35×25×10 cm and 1000 g is not your carton. Measure the warehouse box in the app.",
                ]),
                ("Two payments", [
                    f"Goods plus China domestic into the warehouse, then international freight after QC. {host} never charges you.",
                    f"Storage days sit between those payments. Confirm the live Help article on {OFF} the morning you ship.",
                ]),
                ("Import at the door", [
                    f"Who pays duty is the booked SKU. Educational source: {curl} ({customs}). This page does not invent a declared value.",
                    f"{last_mile_note}",
                ]),
                ("Ready to book freight?", [
                    f"Accept QC, open {EST} toward {dest_name}, pay on {OFF}. {ccy} on this page is display.",
                ]),
            ],
        )
    if kind == "legal":
        return (
            f"Is {A} safe and legal for {dest_name} buyers? {host} explains the agent path and names {customs}. It is not a lawyer and it does not coach a declared value.",
            [
                (f"What “safe” means on {host}", [
                    f"Safe here means you register on {OFF}, you see warehouse photos before freight, and you read {curl} the morning you ship. It does not mean duty-free.",
                    f"{A} is a purchasing agent, not the Chinese shop and not {customs}. {host} is a spreadsheet, not checkout.",
                ]),
                ("What this page will not do", [
                    "It will not tell you what number to type as a declared value. It will not invent a de-minimis threshold or paste a live tariff into the title.",
                    f"Educational source for {dest_name}: {curl} ({customs}). Confirm the same morning you book the line.",
                ]),
                ("Orders and claims", [
                    f"Accounts, payment and tickets stay on {OFF}. {host} does not see your wallet. Restricted is a platform purchase block, not a seizure notice.",
                    f"If a find is restricted the morning you submit, skip it. The sheet is not a workaround.",
                ]),
                (f"Address test for {dest_name}", [
                    f"{city}. {neighbour} Estimator country is {dest_name}, not this TLD.",
                    f"Last-mile is often {post}. Collect can add a fee.",
                ]),
                ("Ready to order?", [
                    f"Read QC and shipping next. Register on {OFF}. Display on this desk is {ccy}.",
                ]),
            ],
        )
    if kind == "guide":
        return (
            f"How to use the {A} spreadsheet on {host} for a {dest_name} door: paste a link on {OFF}, wait for QC, then book freight in {EST}.",
            [
                ("Step 1 — register on the official site", [
                    f"Create the account on {OFF}. {host} never collects a password or a card. Log In / Register in this header goes there.",
                ]),
                ("Step 2 — paste a product link", [
                    "Taobao, 1688 or Weidian URL. OOTDBuy buys into the warehouse in your name. A dead link is a dead row, not a discount.",
                ]),
                ("Step 3 — wait for warehouse photos", [
                    "QC lands in the app while the piece is in China. Extra angles are often paid. Do not book international freight on a reject.",
                ]),
                (f"Step 4 — estimator destination {dest_name}", [
                    f"Open {EST}. {city}. {neighbour} {last_mile_note}",
                ]),
                ("Step 5 — two payments", [
                    f"Goods first, freight after QC. Storage days are in official Help on {OFF}. {ccy} on this page is display.",
                ]),
                ("Step 6 — import is the SKU", [
                    f"Prepaid vs collect is chosen when you submit the parcel. Read {curl} ({customs}). No declared-value coaching here.",
                ]),
                ("Common first-order mistakes", [
                    f"Wrong estimator country, freight before QC, treating {host} as till, or bundling un-QCd pieces on invoice one.",
                    "Restricted, perfume and liquids stay off until the app allows them that morning.",
                ]),
                ("Ready?", [
                    f"Open spreadsheet, finds and QC on {host}, then register on {OFF}.",
                ]),
            ],
        )
    # faq
    return (
        f"{A} spreadsheet FAQ for {dest_name} buyers on {host}. Orders stay on {OFF}. Display {ccy}.",
        [
            (f"Is {host} the official {A} site?", [
                f"No. Official register, cart and estimator are on {OFF} and {EST}. {host} is the spreadsheet and guide for a {dest_name} door.",
            ]),
            ("How many times do I pay?", [
                "Twice is normal: goods into China, then international freight after QC. If the app charges once, the app wins.",
            ]),
            ("What is volumetric weight?", [
                f"Most air SKUs bill max(actual, L×W×H/divisor). Live money is {EST} with destination {dest_name}.",
            ]),
            (f"Who pays {customs}?", [
                f"The booked SKU. Source the morning you ship: {curl}. This page does not invent a declared value.",
            ]),
        ],
    )


def _uk(kind, host, d):
    return _core_en(
        kind, host, d, "the United Kingdom",
        "Northern Ireland is often another carrier product than mainland Royal Mail.",
        "Last mile is often Royal Mail. Do not paste an EU code postal into the estimator.",
    )


def _us(kind, host, d):
    return _core_en(
        kind, host, d, "the United States",
        "A Canadian postal code in the A1A 1A1 pattern is the wrong country.",
        "Last mile is often USPS or FedEx. This desk does not invent a de-minimis dollar.",
    )


def _ca(kind, host, d):
    return _core_en(
        kind, host, d, "Canada",
        "A US ZIP is the wrong country.",
        "Last mile is often Canada Post. GST/HST on import follows the booked SKU.",
    )


def _de(kind, host, d):
    post, city, customs, curl, ccy = d["post"], d["city"], d["customs"], d["customs_url"], d["ccy"]
    if kind == "spreadsheet":
        return (
            f"Ein kuratiertes {A}-Spreadsheet für Käufer in Deutschland auf {host}: Verkäufer, QC-Fotos und Finds in einem Index. Kein Excel, keine Kasse. Bestellen auf {OFF} in {ccy}, Ziel Deutschland.",
            [
                (f"Was ist ein {A}-Spreadsheet?", [
                    f"Ein {A}-Spreadsheet auf {host} ist eine Kurzliste lagergeprüfter SKUs für eine deutsche Lieferadresse — Sneaker, Hoodies, Jacken und Taschen, die in der offiziellen App noch öffnen. Es kassiert nicht und ist kein zweites OOTDBuy-Schaufenster.",
                    "Zeilen bleiben nützlich, solange der Quell-Link lebt und mindestens ein Lagerfoto existiert. Price-0 oder Restricted ist eine tote Quelle, kein Rabatt.",
                ]),
                ("Warum deutsche Käufer mit einem Sheet starten", [
                    f"Taobao, 1688 und Weidian von Hand zu durchsuchen kippt Tausende abgelaufene Karten. Das Sheet hält Finds, die du im QC akzeptiert hast, bevor {post} einen Karton zu {city} bewegt.",
                    "Packstation ist DE. 1010 Wien ist AT. Diese Seite ist für Deutschland, EUR und Zoll geschrieben.",
                ]),
                (f"So funktionieren {A}-Spreadsheets", [
                    f"Finde auf {host} öffnen, Lagerfotos in der offiziellen App lesen, dann internationale Linie mit Ziel Deutschland buchen. Warenkorb und Tickets bleiben auf {OFF}.",
                    f"Englische Katalogschlüssel (sneakers, hoodie, jacket) sind Anzeige. Live-Geld steht in {EST}.",
                ]),
                ("Welche Produkte stehen drin?", [
                    "Schuhe, Hoodies, Jacken, Taschen und Uhren, weil diese SKUs noch QC-Winkel haben. Elektronik, Parfum und Flüssigkeiten bleiben draußen, bis die App sie am Versandmorgen erlaubt.",
                ]),
                ("Ist ein Spreadsheet sicherer?", [
                    f"Sicherer heißt hier: Lagerfotos vor internationaler Fracht — nicht, dass {customs} verschwindet. {curl} am Versandmorgen lesen. Kein Deklarationsbetrag auf dieser Seite.",
                ]),
                ("Wer sollte es nutzen?", [
                    f"Erstbesteller mit deutscher Adresse und alle, die {A} schon nutzen, aber Spreadsheet, Finds, QC und Versand auf einer deutschen Site in {ccy} wollen.",
                ]),
                ("Typische Fehler ohne Sheet", [
                    f"AT-PLZ im Schätzer, {host} als Kasse, Fracht vor QC. Letzte Meile oft {post}; Nachnahme kann extra kosten.",
                ]),
                ("Effizient nutzen", [
                    f"Spreadsheet, Finds und QC in einem Tab-Satz. Nach akzeptiertem QC {EST} mit Ziel Deutschland. Quelle: {customs}. Bestellen auf {OFF}.",
                ]),
                ("Ist das Sheet Pflicht?", [
                    f"Nein. Du kannst die App von Hand durchsuchen. Registrieren trotzdem auf {OFF}.",
                ]),
                ("Bereit?", [
                    f"Cluster-Links für Finds, QC und Versand. Dann {OFF}. Anzeige in {ccy}.",
                ]),
            ],
        )
    if kind == "finds":
        return (
            f"Top {A}-Finds für Deutschland auf {host}: QC-geprüfte Sneaker, Hoodies und Taschen für eine deutsche Adresse, kein zweiter Weltkatalog.",
            [
                ("Was sind Top-Finds?", [
                    f"Finds auf {host} sind SKUs nach Lagerfotos — meist Schuhe, Jacken und Taschen, die in der App noch öffnen. Kein Schaufenster, keine AT-Liste mit anderem Ländernamen.",
                    "Ein Find fällt raus, wenn die URL stirbt oder das Lager das Teil nicht mehr hat. Price-0 ist entfernt, kein Sale.",
                ]),
                ("Warum kuratierte Finds", [
                    f"Manuelle Suche mischt tote Weidian-Links mit lebenden Karten. Kuratierte Finds fotografieren noch in China, bevor du {post} nach {city} buchst.",
                ]),
                ("Kategorien", [
                    "Sneaker und Hoodies füllen die Wand, weil diese Lots noch QC-Winkel haben. Restricted bleibt draußen.",
                ]),
                ("Auswahl", [
                    f"Lebender Quell-Link, mindestens ein Lagerfoto, Schätzer-Ziel Deutschland. {city} ist der Adresstest.",
                ]),
                ("Sicherer als manuell?", [
                    f"Du liest trotzdem {customs} ({curl}) am Versandmorgen. Ein Find heißt nur: fotografiert in China vor internationaler Fracht.",
                ]),
                ("Für wen?", [
                    "Käufer mit deutscher Tür und QC-geprüften Picks. Erste Bestellung: einfache Kleidungs-SKU mit Fotos.",
                ]),
                ("Weiter", [
                    f"Als Nächstes QC, dann Versand. Registrieren auf {OFF}.",
                ]),
            ],
        )
    if kind == "qc":
        return (
            f"QC auf {host} sind Lagerfotos in der offiziellen {A}-App, aufgenommen in China, bevor du Fracht nach Deutschland zahlst.",
            [
                ("Was QC hier ist", [
                    f"Zusätzliche Winkel im Lager — Nähte, Etikett, Sohle, Print. Kein Labor, kein Markengericht, kein {customs}-Röntgen.",
                    "Fotos landen in der App, solange die SKU in China ist. Das ist das Fenster für eine Nachaufnahme.",
                ]),
                ("Wann extra Fotos", [
                    f"Solange die SKU im Lager ist. Wenn {post} den Karton hat, ist {customs} die falsche Stelle für eine Lagernachaufnahme.",
                ]),
                ("Was QC nicht tut", [
                    f"QC gibt keine Zollerklärung ab und erfindet keinen Deklarationsbetrag. Quelle: {curl}.",
                ]),
                ("QC und deutsche Adresse", [
                    f"Ziel Deutschland und {city} im Schätzer. Packstation ist DE, 1010 Wien ist AT.",
                ]),
                ("Wenn ein Find durchfällt", [
                    f"Im Lager lassen oder in der App retournieren. Keine internationale Fracht auf ein Reject. Fail-QC ist in China billiger als nach {post}.",
                ]),
                ("Bereit nach QC?", [
                    f"Dann {EST} nach Deutschland. {host} kassiert nicht. {ccy} lebt in der App.",
                ]),
            ],
        )
    if kind == "shipping":
        return (
            f"{A}-Versand nach Deutschland nutzt den offiziellen Schätzer, nicht diese Domain. Live-Frachtformular nach Lagerfotos. Letzte Meile oft {post}.",
            [
                ("Ablauf", [
                    f"Lager in China → QC akzeptieren → Linie mit Ziel Deutschland buchen → {post} oder SKU-Partner stellt zu. {host} druckt kein Live-Angebot.",
                    f"Label braucht {city}. Ziel in {EST} am Versandmorgen prüfen. Packstation geht, wenn die SKU sie anbietet.",
                ]),
                ("Optionen", [
                    "Tax-free, prepaid und Empfänger sind Eigenschaften der gebuchten SKU. Nachnahme kann eine Gebühr addieren, die der Schätzer verbirgt.",
                ]),
                ("Gewicht und Volumen", [
                    f"Luft-SKUs rechnen meist max(Ist, L×B×H/Teiler). Eine Daunenjacke ist leicht und voluminös. Live-Geld: {EST} mit Ziel Deutschland.",
                ]),
                ("Zwei Zahlungen", [
                    f"Ware plus Inland nach China, dann internationale Fracht nach QC. {host} kassiert nie. Lagerdauer in der Help auf {OFF}.",
                ]),
                ("Einfuhr an der Tür", [
                    f"Wer Zoll zahlt, steht auf der SKU. Quelle: {curl} ({customs}). Kein Deklarationsbetrag hier.",
                ]),
                ("Fracht buchen?", [
                    f"QC akzeptieren, {EST} nach Deutschland, zahlen auf {OFF}. {ccy} auf dieser Seite ist Anzeige.",
                ]),
            ],
        )
    if kind == "legal":
        return (
            f"Ist {A} sicher und legal für Käufer in Deutschland? {host} erklärt den Agentenweg und nennt {customs}. Kein Anwalt, kein Deklarationscoaching.",
            [
                ("Was „sicher“ hier heißt", [
                    f"Registrieren auf {OFF}, Lagerfotos vor Fracht, {curl} am Versandmorgen. Nicht zollfrei.",
                    f"{A} ist Einkaufsagent, nicht der chinesische Shop und nicht {customs}. {host} ist Spreadsheet, keine Kasse.",
                ]),
                ("Was diese Seite nicht tut", [
                    "Sie sagt nicht, welche Zahl du als Warenwert eintippst. Sie erfindet keinen Schwellenwert.",
                    f"Quelle für Deutschland: {curl} ({customs}).",
                ]),
                ("Bestellung und Reklamation", [
                    f"Konto, Zahlung und Tickets auf {OFF}. Restricted ist eine Plattform-Sperre, kein Beschlagnahmebescheid.",
                ]),
                ("Adresstest", [
                    f"{city}. Packstation ist DE. Schätzer-Land ist Deutschland, nicht diese TLD. Letzte Meile oft {post}.",
                ]),
                ("Bestellen?", [
                    f"QC und Versand als Nächstes. Registrieren auf {OFF}. Anzeige {ccy}.",
                ]),
            ],
        )
    if kind == "guide":
        return (
            f"{A}-Spreadsheet auf {host} für eine deutsche Tür: Link auf {OFF} einfügen, QC abwarten, Fracht in {EST} buchen.",
            [
                ("Schritt 1 — auf der offiziellen Site registrieren", [
                    f"Konto auf {OFF}. {host} sammelt kein Passwort und keine Karte.",
                ]),
                ("Schritt 2 — Produktlink einfügen", [
                    "Taobao-, 1688- oder Weidian-URL. OOTDBuy kauft ins Lager auf deinen Namen.",
                ]),
                ("Schritt 3 — Lagerfotos", [
                    "QC in der App, solange das Teil in China ist. Extra-Winkel oft kostenpflichtig.",
                ]),
                ("Schritt 4 — Schätzer-Ziel Deutschland", [
                    f"{EST}. {city}. Packstation ist DE, nicht AT.",
                ]),
                ("Schritt 5 — zwei Zahlungen", [
                    f"Ware zuerst, Fracht nach QC. Lagerdauer in der Help auf {OFF}. {ccy} ist Anzeige.",
                ]),
                ("Schritt 6 — Einfuhr ist die SKU", [
                    f"Prepaid oder Empfänger beim Paket. {curl} ({customs}). Kein Deklarationscoaching.",
                ]),
                ("Typische Fehler", [
                    f"Falsches Schätzer-Land, Fracht vor QC, {host} als Kasse, ungeprüfte Teile auf Rechnung eins bündeln.",
                ]),
                ("Bereit?", [
                    f"Spreadsheet, Finds und QC auf {host}, dann {OFF}.",
                ]),
            ],
        )
    return (
        f"{A} Spreadsheet FAQ für Deutschland auf {host}. Bestellen auf {OFF}. Anzeige {ccy}.",
        [
            (f"Ist {host} die offizielle {A}-Site?", [
                f"Nein. Registrieren, Warenkorb und Schätzer auf {OFF} und {EST}. {host} ist Spreadsheet für eine deutsche Tür.",
            ]),
            ("Wie oft zahle ich?", [
                "Zweimal ist normal: Ware nach China, dann internationale Fracht nach QC.",
            ]),
            ("Was ist Volumengewicht?", [
                f"Luft-SKUs rechnen meist max(Ist, L×B×H/Teiler). Live-Geld: {EST} mit Ziel Deutschland.",
            ]),
            (f"Wer zahlt {customs}?", [
                f"Die gebuchte SKU. Quelle am Versandmorgen: {curl}. Kein Deklarationsbetrag auf dieser Seite.",
            ]),
        ],
    )


def _nl(kind, host, d):
    post, city, customs, curl, ccy = d["post"], d["city"], d["customs"], d["customs_url"], d["ccy"]
    if kind == "spreadsheet":
        return (
            f"Een {A}-spreadsheet voor kopers in Nederland op {host}: vertrouwde sellers, QC-foto’s en finds in één index. Geen Excel, geen kassa. Bestellen op {OFF} in {ccy} met bestemming Nederland.",
            [
                (f"Wat is een {A}-spreadsheet?", [
                    f"Een {A}-spreadsheet op {host} is een shortlist van magazijngecheckte SKU’s voor een Nederlands afleveradres — sneakers, hoodies, jassen en tassen die in de officiële app nog openen. Het int geen betaling en is geen tweede OOTDBuy-winkel.",
                    "Rijen blijven nuttig zolang de bronlink leeft en er minstens één magazijnfoto is. Price-0 of restricted is een dode bron, geen korting.",
                ]),
                ("Waarom Nederlandse kopers met een sheet starten", [
                    f"Taobao, 1688 en Weidian met de hand doorzoeken levert duizenden verlopen kaarten. De sheet houdt finds die je in QC accepteerde, voordat {post} een doos naar {city} brengt.",
                    "Een Belgische viercijferige postcode is het verkeerde land. Deze pagina is voor Nederland, EUR en Douane.",
                ]),
                (f"Hoe {A}-spreadsheets werken", [
                    f"Open een find op {host}, lees magazijnfoto’s in de officiële app, boek daarna een internationale lijn met bestemming Nederland. Winkelwagen en tickets blijven op {OFF}.",
                    f"Engelse catalogsleutels (sneakers, hoodie, jacket) zijn weergave. Live geld staat in {EST}.",
                ]),
                ("Welke producten staan erin?", [
                    "Schoenen, hoodies, jassen, tassen en horloges, omdat die SKU’s nog QC-hoeken hebben. Elektronica, parfum en vloeistoffen blijven eraf tot de app ze de ochtend van verzending toestaat.",
                ]),
                ("Is een spreadsheet veiliger?", [
                    f"Veiliger betekent hier: magazijnfoto’s vóór internationale vracht — niet dat {customs} verdwijnt. Lees {curl} op de verzenddag. Deze pagina plakt geen tarief in de title.",
                ]),
                ("Wie zou het gebruiken?", [
                    f"Eerste-keer-kopers met een Nederlands adres en iedereen die {A} al gebruikt maar spreadsheet, finds, QC en verzending op één Nederlandse site in {ccy} wil.",
                ]),
                ("Veelgemaakte fouten zonder sheet", [
                    f"Belgische postcode in de estimator, {host} als kassa, vracht vóór QC. Last-mile vaak {post}; Collect kan extra kosten.",
                ]),
                ("Efficiënt gebruiken", [
                    f"Spreadsheet, finds en QC in één tabset. Na geaccepteerde QC {EST} met bestemming Nederland. Bron: {customs}. Bestellen op {OFF}.",
                ]),
                ("Is de sheet verplicht?", [
                    f"Nee. Je kunt de app met de hand doorzoeken. Registreren blijft op {OFF}.",
                ]),
                ("Klaar?", [
                    f"Cluster-links voor finds, QC en verzending. Daarna {OFF}. Weergave in {ccy}.",
                ]),
            ],
        )
    if kind == "finds":
        return (
            f"Beste {A}-finds voor Nederland op {host}: QC-gecheckte sneakers, hoodies en tassen voor een Nederlands adres, geen tweede wereldcatalogus.",
            [
                ("Wat zijn top-finds?", [
                    f"Finds op {host} zijn SKU’s na magazijnfoto’s — meestal schoenen, jassen en tassen die in de app nog openen. Geen etalage, geen Belgische lijst met een andere landsnaam.",
                    "Een find valt af als de URL sterft of het magazijn het stuk niet meer heeft. Price-0 is verwijderd, geen sale.",
                ]),
                ("Waarom gecureerde finds", [
                    f"Handmatig zoeken mengt dode Weidian-links met levende kaarten. Gecureerde finds fotograferen nog in China voordat je {post} naar {city} boekt.",
                ]),
                ("Categorieën", [
                    "Sneakers en hoodies vullen de muur omdat die lots nog QC-hoeken hebben. Restricted blijft eraf.",
                ]),
                ("Selectie", [
                    f"Levende bron-URL, minstens één magazijnfoto, estimator-bestemming Nederland. {city} is de adres-test.",
                ]),
                ("Veiliger dan handmatig?", [
                    f"Je leest toch {customs} ({curl}) op de verzenddag. Een find betekent alleen: gefotografeerd in China vóór internationale vracht.",
                ]),
                ("Voor wie?", [
                    "Kopers met een Nederlandse deur en QC-picks. Eerste order: eenvoudige kleding-SKU met foto’s.",
                ]),
                ("Verder", [
                    f"Daarna QC, dan verzending. Registreren op {OFF}.",
                ]),
            ],
        )
    if kind == "qc":
        return (
            f"QC op {host} zijn magazijnfoto’s in de officiële {A}-app, gemaakt in China, vóór je vracht naar Nederland betaalt.",
            [
                ("Wat QC hier is", [
                    f"Extra hoeken in het magazijn — naden, label, zool, print. Geen laboratorium, geen merkrechter, geen {customs}-röntgen.",
                    "Foto’s landen in de app zolang de SKU in China is. Dat is het raam voor een extra shot.",
                ]),
                ("Wanneer extra foto’s", [
                    f"Zolang de SKU in het magazijn is. Als {post} de doos heeft, is {customs} de verkeerde loket voor een magazijn-retake.",
                ]),
                ("Wat QC niet doet", [
                    f"QC dient geen douaneaangifte in en verzint geen aangegeven waarde. Bron: {curl}.",
                ]),
                ("QC en Nederlands adres", [
                    f"Bestemming Nederland en {city} in de estimator. Een Belgische postcode is het verkeerde land.",
                ]),
                ("Als een find faalt", [
                    f"In het magazijn laten of in de app retourneren. Geen internationale vracht op een reject. Fail-QC is in China goedkoper dan na {post}.",
                ]),
                ("Klaar na QC?", [
                    f"Dan {EST} naar Nederland. {host} int niets. {ccy} leeft in de app.",
                ]),
            ],
        )
    if kind == "shipping":
        return (
            f"{A}-verzending naar Nederland gebruikt de officiële estimator, niet dit domein. Live vrachtformulier na magazijnfoto’s. Last-mile vaak {post}.",
            [
                ("Verloop", [
                    f"Magazijn in China → QC accepteren → lijn met bestemming Nederland boeken → {post} of SKU-partner bezorgt. {host} drukt geen live quote.",
                    f"Label heeft {city} nodig. Bestemming in {EST} op de verzenddag checken.",
                ]),
                ("Opties", [
                    "Tax-free, prepaid en collect zijn eigenschappen van de geboekte SKU. Collect kan een toeslag adden die de calculator verbergt.",
                ]),
                ("Gewicht en volume", [
                    f"Lucht-SKU’s rekenen meestal max(werkelijk, L×B×H/deler). Een donsjas is licht en volumineus. Live geld: {EST} met bestemming Nederland.",
                ]),
                ("Twee betalingen", [
                    f"Goederen plus inland naar China, daarna internationale vracht na QC. {host} int nooit. Magazijndagen in de Help op {OFF}.",
                ]),
                ("Invoer aan de deur", [
                    f"Wie invoer betaalt, staat op de SKU. Bron: {curl} ({customs}). Geen aangegeven waarde hier.",
                ]),
                ("Vracht boeken?", [
                    f"QC accepteren, {EST} naar Nederland, betalen op {OFF}. {ccy} op deze pagina is weergave.",
                ]),
            ],
        )
    if kind == "legal":
        return (
            f"Is {A} veilig en legaal voor kopers in Nederland? {host} legt het agentpad uit en noemt {customs}. Geen advocaat, geen aangegeven-waarde-coaching.",
            [
                ("Wat „veilig” hier betekent", [
                    f"Registreren op {OFF}, magazijnfoto’s vóór vracht, {curl} op de verzenddag. Niet douanevrij.",
                    f"{A} is inkoopagent, niet de Chinese shop en niet {customs}. {host} is spreadsheet, geen kassa.",
                ]),
                ("Wat deze pagina niet doet", [
                    "Ze zegt niet welk getal je als aangegeven waarde intikt. Ze verzint geen drempel.",
                    f"Bron voor Nederland: {curl} ({customs}).",
                ]),
                ("Orders en claims", [
                    f"Account, betaling en tickets op {OFF}. Restricted is een platformblokkade, geen inbeslagname.",
                ]),
                ("Adres-test", [
                    f"{city}. Een Belgische postcode is het verkeerde land. Estimator-land is Nederland, niet deze TLD. Last-mile vaak {post}.",
                ]),
                ("Bestellen?", [
                    f"QC en verzending hierna. Registreren op {OFF}. Weergave {ccy}.",
                ]),
            ],
        )
    if kind == "guide":
        return (
            f"{A}-spreadsheet op {host} voor een Nederlandse deur: link plakken op {OFF}, QC afwachten, vracht in {EST} boeken.",
            [
                ("Stap 1 — registreren op de officiële site", [
                    f"Account op {OFF}. {host} verzamelt geen wachtwoord en geen kaart. iDEAL bevestig je in de app.",
                ]),
                ("Stap 2 — productlink plakken", [
                    "Taobao-, 1688- of Weidian-URL. OOTDBuy koopt naar het magazijn op jouw naam.",
                ]),
                ("Stap 3 — magazijnfoto’s", [
                    "QC in de app zolang het stuk in China is. Extra hoeken vaak betaald.",
                ]),
                ("Stap 4 — estimator-bestemming Nederland", [
                    f"{EST}. {city}. Geen Belgische postcode, geen Duits Packstation-nummer.",
                ]),
                ("Stap 5 — twee betalingen", [
                    f"Goederen eerst, vracht na QC. Magazijndagen in de Help op {OFF}. {ccy} is weergave.",
                ]),
                ("Stap 6 — invoer is de SKU", [
                    f"Prepaid of collect bij het pakket. {curl} ({customs}). Geen aangegeven-waarde-coaching.",
                ]),
                ("Typische fouten", [
                    f"Verkeerd estimator-land, vracht vóór QC, {host} als kassa, ongecheckte stukken op factuur één bundelen.",
                ]),
                ("Klaar?", [
                    f"Spreadsheet, finds en QC op {host}, daarna {OFF}.",
                ]),
            ],
        )
    return (
        f"{A} spreadsheet FAQ voor Nederland op {host}. Bestellen op {OFF}. Weergave {ccy}.",
        [
            (f"Is {host} de officiële {A}-site?", [
                f"Nee. Registreren, winkelwagen en estimator op {OFF} en {EST}. {host} is de spreadsheet voor een Nederlandse deur.",
            ]),
            ("Hoe vaak betaal ik?", [
                "Twee keer is normaal: goederen naar China, daarna internationale vracht na QC.",
            ]),
            ("Wat is volumgewicht?", [
                f"Lucht-SKU’s rekenen meestal max(werkelijk, L×B×H/deler). Live geld: {EST} met bestemming Nederland.",
            ]),
            (f"Wie betaalt {customs}?", [
                f"De geboekte SKU. Bron op de verzenddag: {curl}. Deze pagina verzint geen aangegeven waarde.",
            ]),
        ],
    )
