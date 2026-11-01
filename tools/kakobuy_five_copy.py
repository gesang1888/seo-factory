"""Localized inner copy for the five Kakobuy dests, UK-cluster depth.

Public pages: no ops notes, no declared-value coaching, no invented transit
days or duty rates. Unique /ohje/ is not rendered here.
"""
from __future__ import annotations

from desk_template import KW_GEO

A = "Kakobuy"


def geo(dest: str) -> str:
    return KW_GEO.get(dest, dest.lower())


def inner_keywords(kind: str, dest: str) -> list[str]:
    g = geo(dest)
    table = {
        "spreadsheet": [f"{A} spreadsheet", f"kakobuy spreadsheet {g}", "kakobuy trusted sellers"],
        "finds": ["kakobuy finds", "kakobuy spreadsheet finds", "best kakobuy items"],
        "qc": ["kakobuy qc", f"kakobuy qc {g}", "kakobuy warehouse photos"],
        "shipping": ["kakobuy shipping", f"kakobuy shipping {g}", "kakobuy delivery time"],
        "legal": ["kakobuy safe", "kakobuy legit", f"kakobuy safe {g}"],
        "guide": ["kakobuy spreadsheet guide", "how to use kakobuy", "kakobuy buying guide"],
        "faq": ["kakobuy faq", "kakobuy spreadsheet faq", "kakobuy questions"],
    }
    return table[kind]


def inner_serp_title(kind: str, loc: str, label: str) -> str:
    table = {
        "spreadsheet": {
            "en": f"{A} Spreadsheet Canada – Best Sellers, QC & Finds",
            "fi": f"{A} Spreadsheet Suomi – Finds ja QC",
            "es": f"{A} Spreadsheet España – Mejores finds y QC",
            "fr": f"{A} Spreadsheet France – Meilleurs finds et QC",
            "nl": f"{A} Spreadsheet Nederland – Beste finds en QC",
        },
        "finds": {
            "en": f"Top {A} Spreadsheet Finds – Best Canada Picks 2026",
            "fi": f"{A} spreadsheet finds – Suomen valinnat 2026",
            "es": f"Mejores finds {A} – selección España 2026",
            "fr": f"Meilleurs finds {A} – sélection France 2026",
            "nl": f"Beste {A} finds – Nederland 2026",
        },
        "qc": {
            "en": f"{A} QC Photos for Canada Buyers – Warehouse Check",
            "fi": f"{A} QC-kuvat Suomeen – varastotarkistus",
            "es": f"Fotos QC {A} para España – almacén",
            "fr": f"Photos QC {A} France – contrôle entrepôt",
            "nl": f"{A} QC-foto’s Nederland – magazijncheck",
        },
        "shipping": {
            "en": f"{A} Shipping to Canada – Cost, Time & Canada Post",
            "fi": f"{A} toimitus Suomeen – hinta, aika ja Posti",
            "es": f"Envío {A} a España – coste, plazos y Correos",
            "fr": f"Livraison {A} France – coût, délais et Colissimo",
            "nl": f"{A} verzending Nederland – kosten, tijd en PostNL",
        },
        "legal": {
            "en": f"Is {A} Safe & Legal for Canada Buyers? Full Guide",
            "fi": f"Onko {A} turvallinen ja laillinen Suomessa?",
            "es": f"¿{A} es seguro y legal en España? Guía",
            "fr": f"{A} est-il sûr et légal en France ? Guide",
            "nl": f"Is {A} veilig en legaal in Nederland?",
        },
        "guide": {
            "en": f"How to Use {A} Spreadsheet – Beginner Guide Canada",
            "fi": f"Näin käytät {A} spreadsheetiä – aloitusopas Suomi",
            "es": f"Cómo usar el spreadsheet {A} – guía España",
            "fr": f"Utiliser le spreadsheet {A} – guide France",
            "nl": f"{A}-spreadsheet gebruiken – startergids NL",
        },
        "faq": {
            "en": f"{A} Spreadsheet FAQ – Canada Buyers Guide 2026",
            "fi": f"{A} spreadsheet FAQ – opas suomalaisille ostajille",
            "es": f"FAQ spreadsheet {A} – guía España 2026",
            "fr": f"FAQ spreadsheet {A} – guide France 2026",
            "nl": f"{A} spreadsheet FAQ – gids Nederland 2026",
        },
    }
    row = table[kind]
    return row.get(loc, row["en"])


def inner_h1(kind: str, loc: str, label: str) -> str:
    table = {
        "spreadsheet": {
            "en": f"{A} Spreadsheet for Canadian Buyers (2026 Guide)",
            "fi": f"{A} Spreadsheet suomalaisille ostajille (2026-opas)",
            "es": f"{A} Spreadsheet para compradores en España (guía 2026)",
            "fr": f"{A} Spreadsheet pour acheteurs en France (guide 2026)",
            "nl": f"{A} Spreadsheet voor kopers in Nederland (gids 2026)",
        },
        "finds": {
            "en": f"Top {A} Finds for Canada Buyers (2026 Guide)",
            "fi": f"{A}-findsit suomalaisille ostajille (2026)",
            "es": f"Mejores finds {A} para España (guía 2026)",
            "fr": f"Meilleurs finds {A} pour la France (guide 2026)",
            "nl": f"Beste {A}-finds voor Nederland (gids 2026)",
        },
        "qc": {
            "en": f"{A} QC Photos before Shipping to Canada",
            "fi": f"{A} QC-kuvat ennen toimitusta Suomeen",
            "es": f"Fotos QC de {A} antes de enviar a España",
            "fr": f"Photos QC {A} avant envoi vers la France",
            "nl": f"{A} QC-foto’s vóór verzending naar Nederland",
        },
        "shipping": {
            "en": f"{A} Shipping to Canada (2026 Guide)",
            "fi": f"{A}-toimitus Suomeen (opas 2026)",
            "es": f"Envío {A} a España (guía 2026)",
            "fr": f"Livraison {A} vers la France (guide 2026)",
            "nl": f"{A}-verzending naar Nederland (gids 2026)",
        },
        "legal": {
            "en": f"Is {A} Safe & Legal for Canada Buyers?",
            "fi": f"Onko {A} turvallinen ja laillinen Suomessa?",
            "es": f"¿{A} es seguro y legal para compradores en España?",
            "fr": f"{A} est-il sûr et légal pour les acheteurs en France ?",
            "nl": f"Is {A} veilig en legaal voor kopers in Nederland?",
        },
        "guide": {
            "en": f"Buying from {A}: A Step-by-Step Guide for Canada Buyers",
            "fi": f"Ostaminen Kakobuysta: vaiheet suomalaiselle ostajalle",
            "es": f"Comprar en {A}: guía paso a paso para España",
            "fr": f"Acheter avec {A} : guide pas à pas pour la France",
            "nl": f"Kopen via {A}: stappenplan voor Nederland",
        },
        "faq": {
            "en": f"{A} FAQ for Canada Buyers (2026)",
            "fi": f"{A} FAQ suomalaisille ostajille (2026)",
            "es": f"FAQ {A} para compradores en España (2026)",
            "fr": f"FAQ {A} pour acheteurs en France (2026)",
            "nl": f"{A} FAQ voor kopers in Nederland (2026)",
        },
    }
    row = table[kind]
    return row.get(loc, row["en"])


def sections_for(kind: str, d: dict, host: str):
    loc = d["loc"]
    h1 = inner_h1(kind, loc, d["label"])
    fn = {"en": _en, "fi": _fi, "es": _es, "fr": _fr, "nl": _nl}[loc]
    lead, secs = fn(kind, host, d)
    return h1, lead, secs


def _en(kind, host, d):
    post, city, customs, curl = d["post"], d["city"], d["customs"], d["customs_url"]
    if kind == "spreadsheet":
        return (
            f"A curated {A} spreadsheet for Canadian buyers on {host}: trusted sellers, QC photos and finds in one index. It is not Excel and not checkout. Order on kakobuy.com in CAD after you pick destination Canada.",
            [
                ("What is a Kakobuy spreadsheet?", [
                    f"A {A} spreadsheet on {host} is a shortlist of warehouse-checked SKUs meant for a Canadian delivery address — sneakers, hoodies, jackets and bags that still open in the official app. It does not take payment and it is not a second Kakobuy storefront.",
                    f"Rows stay useful only while the source link is live and at least one warehouse photo exists. A price-0 or restricted card is a dead source, not a discount. Keywords on this page: Kakobuy spreadsheet, kakobuy spreadsheet canada, kakobuy trusted sellers.",
                ]),
                ("Why Canada buyers start with a sheet", [
                    f"Searching Taobao, 1688 and Weidian by hand dumps thousands of expired cards. The sheet keeps finds you already accepted in QC before you ask {post} to move a carton toward {city}.",
                    "Canadian buyers also avoid a US ZIP in the official estimator. This page is written for CBSA territory, CAD, and a postal code in the A1A 1A1 pattern — not a de-minimis US lane.",
                ]),
                ("How Kakobuy spreadsheets work", [
                    f"Open a find on {host}, read warehouse photos in the official {A} app, then book an international line with destination Canada. {host} only explains that order. Cart, wallet and tickets stay on kakobuy.com.",
                    "English catalogue keys (sneakers, hoodie, jacket) on the wall are display labels. They are not a US shop and they do not change the estimator country.",
                ]),
                ("What types of products are included?", [
                    "Shoes, hoodies, jackets, bags and watches dominate because those SKUs still have QC angles. Electronics, perfume, liquids and other restricted classes stay off the sheet unless the official app shows them as allowed the morning you submit.",
                    "A find that passed QC last month can still go restricted. Recheck the official product page before you pay freight. This index does not freeze a catalogue.",
                ]),
                ("Is using a Kakobuy spreadsheet safer?", [
                    f"Safer here means you saw warehouse photos before international freight — not that {customs} disappears. Read {curl} the morning you ship. GST/HST, broker fees and Collect handling change; this page does not paste a rate into the title.",
                    "The sheet also keeps you off dead Weidian links. It does not file a CBSA entry and it does not pick a declared value for you.",
                ]),
                ("Who should use a Kakobuy spreadsheet?", [
                    f"First-time Canada buyers who need an address test ({city}) and anyone who already uses {A} but wants spreadsheet, finds, QC and shipping-to-Canada in one Canadian site.",
                    "If you ship to a US door, this is the wrong country page. If you need a broker, hire one — {host} is information only.",
                ]),
                ("Common mistakes without a spreadsheet", [
                    f"Pasting a US ZIP into the estimator, treating {host} as checkout, or booking freight before QC. Last-mile is often {post}; Collect can add a fee the estimator hides.",
                    "Another miss: assuming a ranked GST article on this site is a live tariff. Thresholds move. Confirm in the official app and on the CBSA page the day you ship.",
                ]),
                ("How to use a spreadsheet efficiently", [
                    f"Keep spreadsheet, finds and QC in one tab set. When a find is accepted, open the official freight form toward Canada with {city} on the label. Source: {customs}.",
                    "Skip under-declaration tricks. Pay what the booked SKU and the official estimator show. Orders stay on kakobuy.com.",
                ]),
                ("Is a Kakobuy spreadsheet required?", [
                    "No. You can search the official app by hand. The sheet exists so Canadian buyers are not starting from thousands of dead cards every week.",
                    f"You still register and pay on kakobuy.com. {host} never sees the account.",
                ]),
                ("Ready to use a Kakobuy spreadsheet?", [
                    "Use the cluster links for finds, QC photos and shipping to Canada. Then register on kakobuy.com. This site stays an index.",
                ]),
            ],
        )
    if kind == "finds":
        return (
            f"Top {A} spreadsheet finds for Canada buyers on {host}: QC-checked sneakers, hoodies and bags aimed at a Canadian address, not a second global catalogue.",
            [
                ("What are top Kakobuy finds?", [
                    f"Finds on {host} are SKUs kept after warehouse photos — usually shoes, jackets and bags that still open in the official app. They are not a shop window and they are not copied from a UK list with the country name swapped.",
                    "A find drops off when the source URL dies or the warehouse no longer has the piece. Price-0 is a removed card, not a sale.",
                ]),
                ("Why Canada buyers use curated Kakobuy finds", [
                    f"Manual search mixes dead Weidian links with live cards. Curated finds are the ones that still photograph in China before you book {post} toward {city}.",
                    "CAD prices in the official app, destination Canada, and a real postal code beat hunting Reddit screenshots that never list a CBSA path.",
                ]),
                ("Popular product categories", [
                    "Sneakers and hoodies fill the wall because those lots still have QC angles. Bags and jackets follow. Restricted goods stay off even if a forum names them.",
                    "Category keys on this site are English display labels. They do not make the parcel a US import.",
                ]),
                ("How these finds are selected", [
                    f"A find needs a live source URL, at least one warehouse photo, and estimator destination Canada — not a US ZIP, not this hostname as a country. {city} is the address test.",
                    "We do not keep a find because it was popular last season. If QC fails, it leaves the list.",
                ]),
                ("Are Kakobuy finds safer than searching manually?", [
                    f"You still read {customs} ({curl}) the morning you ship. A find only means the piece was photographed in China before international freight.",
                    "Safer is not duty-free. GST/HST and Collect can still apply. This page does not invent a CBSA dollar.",
                ]),
                ("Who should use top Kakobuy finds?", [
                    f"Buyers who already have a Canadian door and want QC’d picks, not a US de-minimis article. First orders should stay on simple clothing SKUs with photos.",
                    f"If your label is {city}, stay on this Canadian site. Sister country pages are separate files.",
                ]),
                ("Ready to explore top Kakobuy finds?", [
                    "Open QC next, then shipping to Canada. Register and pay on kakobuy.com. {host} is information only.",
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
                    "Extra angles are often a paid add-on in the official app. This HTML cannot open tickets.",
                ]),
                ("What QC does not do", [
                    f"QC does not file a {customs} entry, does not pay GST/HST, and does not invent a declared value. Educational source: {curl}.",
                    "A clean QC album is not a promise the SKU will pass a later platform rule. Recheck before you book the line.",
                ]),
                ("QC and a Canadian address", [
                    f"Use destination Canada and {city} in the estimator. A US ZIP is the wrong country for this site. Last-mile notes sit on the shipping-to-Canada page.",
                    "Warehouse photos are taken in China either way. The Canadian part is the door on the label after you accept QC.",
                ]),
                ("If a find fails QC", [
                    "Leave it in the warehouse or return it in the official app. Do not book international freight on a reject just to 'get it over with'.",
                    "Failed QC is cheaper in China than after {post} attempts delivery.",
                ]),
                ("Ready to ship after QC?", [
                    f"Only then open the official estimator toward Canada. {host} does not take payment. CAD totals live in the app.",
                ]),
            ],
        )
    if kind == "shipping":
        return (
            f"{A} shipping to Canada uses the official estimator country code CA, not this domain. Open the live freight form after warehouse photos. Last-mile is often {post}.",
            [
                ("How Kakobuy shipping to Canada works", [
                    f"Warehouse in China → you accept QC → you book a line with destination Canada → {post} or the SKU’s last-mile partner hands it over. {host} does not print a live quote.",
                    f"The label needs a real Canadian postal code ({city}). A northern US route is not Canada. Confirm destination CA in kakobuy.com/tools/estimate the morning you ship.",
                ]),
                ("Kakobuy shipping options for Canada buyers", [
                    "Tax-free, prepaid and collect are properties of the booked SKU in the official app. This page does not rename them. Collect can add a broker fee the estimator hides.",
                    f"{post} may also add a handling fee on collect parcels. Read the SKU, then the live estimator — not a screenshot from last year.",
                ]),
                ("How long Kakobuy shipping to Canada takes", [
                    "Transit days change with the SKU and the line you book. This page does not invent Canada Post business days.",
                    "Confirm in the official app the morning you ship. Warehouse processing is separate from international transit.",
                ]),
                ("Kakobuy shipping costs to Canada", [
                    f"You pay international freight plus whatever the SKU says at the border. {post} can add collect handling. No dollar amount is pasted into this title because the live form moves.",
                    "CAD is the local currency on this site. Checkout still happens on kakobuy.com.",
                ]),
                ("Customs, GST/HST and import fees", [
                    f"Read {customs} at {curl} the morning you ship. GST/HST thresholds and broker rules change. Ranked GST articles on this site stay as local notes — they are not a live tariff table.",
                    "This HTML does not coach a declared value. Pay what the booked SKU and CBSA rules require.",
                ]),
                ("Common shipping risks", [
                    f"Wrong country in the estimator (US ZIP), booking before QC, skipping {city} on the label. Those mistakes are Canadian-path errors, not 'agent is down'.",
                    "Restricted SKUs that slipped into the warehouse still cannot ride a Canada line if the official app blocks them at submit.",
                ]),
                ("Is Kakobuy shipping suitable for first-time Canada buyers?", [
                    f"Yes if you treat {host} as a map and kakobuy.com as checkout. Address test: {city}. Source: {customs}.",
                    "Start with one clothing SKU, accept QC, then book. Do not consolidate a pile of un-QCd items on the first order.",
                ]),
                ("Ready to ship safely to Canada?", [
                    "QC first, then the official estimator toward Canada. Orders only on kakobuy.com.",
                ]),
            ],
        )
    if kind == "legal":
        return (
            f"{A} is a purchasing agent. {host} explains the Canada path; it is not the official app and not {customs}. Read CBSA the morning you ship.",
            [
                ("Is Kakobuy legal in Canada?", [
                    f"Using a purchasing agent is not a crime in Canada. Restricted goods, platform rules and the booked SKU still apply. Read {curl} the morning you ship.",
                    "Legal here means the agent model itself. It does not mean every SKU on Taobao is allowed through CBSA.",
                ]),
                ("Is Kakobuy safe to use?", [
                    "Safe on this page means warehouse QC before freight, payment in the official app, and a real Canadian address — not a promise that a parcel skips CBSA.",
                    f"CAD checkout, destination Canada, {city} on the label. {host} never holds the wallet.",
                ]),
                ("What are the main risks for Canada buyers?", [
                    f"Dead source links, booking collect without reading the SKU, and treating {host} as checkout. {post} can add fees.",
                    "A second risk is pasting a US ZIP because the estimator UI looks similar. That is the wrong country for this site.",
                ]),
                ("How can Canada buyers reduce risk?", [
                    f"QC in the official app, estimator destination Canada, {city} on the label. No under-declaration. No invented CBSA dollar.",
                    "Keep spreadsheet, finds and QC together so you are not booking freight on a screenshot from another country page.",
                ]),
                ("Is Kakobuy suitable for first-time Canada buyers?", [
                    f"Yes if you start with the spreadsheet and finds on {host}, then the official register. This site does not see your account.",
                    "Skip restricted categories on the first order. Clothing SKUs with QC photos are the usual first path.",
                ]),
                ("Final verdict: should Canada buyers use Kakobuy?", [
                    f"{A} can be used toward Canada if you follow the official app and {customs}. This site stays independent information. Orders on kakobuy.com.",
                ]),
                ("Ready to get started?", [
                    "Open spreadsheet → finds → QC → shipping to Canada. Pay only on kakobuy.com.",
                ]),
            ],
        )
    if kind == "guide":
        return (
            f"A step-by-step {A} path for a Canadian address on {host}. Photos in the warehouse, then freight. Not checkout.",
            [
                ("How to buy from Kakobuy (Canada guide)", [
                    f"Find a QC’d SKU on the spreadsheet or finds list, submit it in the official app, wait for warehouse photos, then book international freight toward Canada with {city} on the label.",
                    "Do not skip QC to save a day. Canadian last-mile will not retake a warehouse photo.",
                ]),
                ("What is Kakobuy?", [
                    f"A China purchasing agent. {host} only explains the Canada path in CAD. Payment, tickets and the estimator stay on kakobuy.com.",
                    "Two payments are normal: goods to the warehouse, then international freight after QC.",
                ]),
                ("Step 1: find the products you want", [
                    "Use the spreadsheet and finds on this Canadian site. Skip price-0 and restricted cards. English category keys are labels, not a US store.",
                ]),
                ("Step 2: submit the order on Kakobuy", [
                    "Official app only. This HTML cannot see the cart. Register on kakobuy.com, not on {host}.",
                ]),
                ("Step 3: QC in the warehouse", [
                    "Photos before freight. Extra angles may be paid. Reject in the app if the piece is wrong — do not book the Canada line on a fail.",
                ]),
                ("Step 4: choose international shipping to Canada", [
                    f"Estimator destination CA, address {city}. Read {customs} ({curl}) the morning you ship. Do not paste a US ZIP.",
                ]),
                ("Step 5: receive your package in Canada", [
                    f"Last-mile is often {post}. Collect can add a fee. Tracking lives in the official app, not in this article.",
                ]),
                ("Common tips for Canada buyers", [
                    "One simple clothing SKU on the first order. QC before freight. Destination Canada every time. No declared-value coaching on this page.",
                ]),
                ("Is Kakobuy suitable for beginners?", [
                    f"Yes if you treat {host} as the map and kakobuy.com as checkout. Source: {customs}.",
                ]),
            ],
        )
    return (
        f"Answers for Canada buyers using the {A} spreadsheet on {host}: QC, shipping, GST/HST and whether you need the sheet.",
        [
            ("Do I need to register an account to use Kakobuy?", [
                f"Yes, on the official {A} site. {host} does not create accounts and cannot reset a password.",
            ]),
            ("Is Kakobuy safe for first-time Canada buyers?", [
                f"QC photos before freight, destination Canada, {city} on the label. Read {customs}. This page does not coach a declared value.",
            ]),
            ("How do Canada buyers usually find reliable products?", [
                "Start with this site’s spreadsheet and finds. Dead Weidian links drop off the sheet. Recheck the official app before you pay freight.",
            ]),
            ("Will I receive Quality Check (QC) photos?", [
                "In the official app, in China, before international freight. Extra angles are often paid.",
            ]),
            ("How long does shipping to Canada usually take?", [
                f"It depends on the SKU and the line you book. This page does not invent {post} days. Confirm in the official estimator.",
            ]),
            ("Do I need to pay GST/HST or duty in Canada?", [
                f"The booked SKU says who pays. Collect can add a broker fee. Source: {customs} ({curl}). Thresholds change; we do not paste a rate.",
            ]),
            ("Is it better to start with a spreadsheet or search manually?", [
                f"The sheet on {host} exists so Canadian buyers are not hunting dead cards. It is still an index, not Excel. You can search the app by hand.",
            ]),
            ("What types of products do Canada buyers usually purchase?", [
                "Shoes, hoodies, jackets, bags — if the warehouse still has QC. Restricted goods stay off.",
            ]),
            ("Can I use Kakobuy without a spreadsheet?", [
                "Yes. The spreadsheet is a shortcut, not a gate. Beginners usually finish faster with the sheet plus QC photos.",
            ]),
            ("Ready to buy with confidence?", [
                "Open spreadsheet, finds, QC and shipping to Canada, then register on kakobuy.com.",
            ]),
        ],
    )


def _fi(kind, host, d):
    post, city, customs, curl = d["post"], d["city"], d["customs"], d["customs_url"]
    if kind == "spreadsheet":
        return (
            f"Kuratoitu {A}-spreadsheet suomalaisille ostajille sivustolla {host}: luotetut myyjät, QC-kuvat ja findsit yhdessä indeksissä. Ei Excel, ei kassa. Tilaa kakobuy.comissa euroissa, arvioijan kohde FI.",
            [
                ("Mikä on Kakobuy spreadsheet?", [
                    f"Spreadsheet sivustolla {host} on varastossa kuvattujen SKU:iden lyhytlista suomalaiseen osoitteeseen — kengät, hupparit, takit ja kassit, jotka vielä aukeavat virallisessa apissa. Se ei ota maksua eikä ole toinen Kakobuy-kauppa.",
                    "Rivi pysyy vain jos lähdelinkki elää ja varastokuva on olemassa. Hinta 0 tai restricted on kuollut lähde, ei ale. Avainsanat: Kakobuy spreadsheet, kakobuy spreadsheet suomi, kakobuy trusted sellers.",
                ]),
                ("Miksi suomalainen ostaja aloittaa sheetistä", [
                    f"Taobao, 1688 ja Weidian paljaina täyttävät syötteen kuolleilla korteilla. Sheet pitää findsit, jotka hyväksyit QC:ssä ennen kuin {post} vie kartongin kohti {city}.",
                    "Suomen polku ei ole Ruotsi. Arvioijassa FI, ei SE, ei geneerinen EU. Postinumero testataan muodossa 00100 Helsinki.",
                ]),
                ("Miten Kakobuy-spreadsheet toimii", [
                    f"Avaat findin {host}-sivustolla, luet varastokuvat virallisessa {A}-apissa, varaat kansainvälisen linjan kohteeseen Suomi. Kori, lompakko ja tiketit jäävät kakobuy.comiin.",
                    "Katalogin englanninkieliset avaimet (sneakers, hoodie) ovat näyttötekstejä, eivät US-kauppaa.",
                ]),
                ("Mitä tuoteperheitä sheetissä on?", [
                    "Kengät, hupparit, takit, kassit ja kellot, koska niissä on yhä QC-kulmia. Elektroniikka, tuoksut ja muut restricted-luokat pysyvät poissa, ellei virallinen appi salli niitä lähetysaamuna.",
                    "Kuukausi sitten hyväksytty find voi mennä restrictediksi. Tarkista virallinen tuotesivu ennen rahtia.",
                ]),
                ("Onko spreadsheet turvallisempi kuin haku käsin?", [
                    f"Turvallisempi tarkoittaa varastokuvia ennen kansainvälistä rahtia — ei sitä että {customs} katoaa. Lue {curl} lähetysaamuna. ALV, IOSS ja Collect muuttuvat; tähän titleen ei liimata prosenttia.",
                    "Sheet pitää pois kuolleet Weidian-linkit. Se ei tee tulli-ilmoitusta eikä valitse ilmoitusarvoa.",
                ]),
                ("Kenelle Suomen sheet on?", [
                    f"Ensikertalaiselle, joka tarvitsee osoitetestin ({city}), ja sille joka jo käyttää {A}:ta mutta haluaa spreadsheetin, findsit, QC:n ja toimituksen yhdellä suomalaisella sivustolla.",
                    "Jos lähetät Ruotsiin, tämä on väärä maa. Tulli-asioihin {customs}, ei tämä sivu.",
                ]),
                ("Tyypilliset virheet ilman sheettiä", [
                    f"Ruotsalainen postinumero arvioijassa, {host} kassana, rahti ennen QC:tä. Viimeinen kilometri on usein {post}; Collect voi lisätä maksun.",
                    "Toinen virhe: luulla että vanha ALV-juttu tällä sivustolla on voimassa oleva tariffi. Kynnykset liikkuvat. Vahvista apissa ja Tullissa lähetyspäivänä.",
                ]),
                ("Miten käyttää sheettiä tehokkaasti", [
                    f"Pidä spreadsheet, finds ja QC samassa välilehtisetissä. Kun find on hyväksytty, avaa virallinen rahtilomake kohteeseen FI, tarrassa {city}. Lähde: {customs}.",
                    "Ei aliarvostuskikkoja. Maksa se mitä varattu SKU ja arvioija näyttävät. Tilaukset kakobuy.comissa.",
                ]),
                ("Onko spreadsheet pakollinen?", [
                    "Ei. Voit hakea virallisesta apista käsin. Sheet on olemassa, jotta suomalainen ostaja ei aloita joka viikko tuhansista kuolleista korteista.",
                    f"Rekisteröinti ja maksu silti kakobuy.comissa. {host} ei näe tiliä.",
                ]),
                ("Valmis käyttämään spreadsheetiä?", [
                    "Avaa finds, QC ja toimitus. Rekisteröidy kakobuy.comissa. Tämä sivusto pysyy indeksinä.",
                ]),
            ],
        )
    if kind == "finds":
        return (
            f"{A}-spreadsheetin findsit suomalaisille ostajille sivustolla {host}: QC-tarkistetut kengät, hupparit ja kassit suomalaiseen osoitteeseen, ei toinen globaali katalogi.",
            [
                ("Mitä Kakobuy-findsit ovat?", [
                    f"Findsit {host}-sivustolla ovat varastokuvien jälkeen pidettyjä SKU:ita. Ne eivät ole myymäläikkuna.",
                    "Find putoaa, kun lähde kuolee tai varastossa ei enää ole kappaletta. Hinta 0 on poistettu kortti.",
                ]),
                ("Miksi suomalainen ostaja käyttää kuratoituja findejä", [
                    f"Käsinhaku sekoittaa kuolleet Weidian-linkit. Kuratoidut findsit ovat ne, jotka vielä kuvataan Kiinassa ennen kuin {post} lähtee kohti {city}.",
                    "Eurot virallisessa apissa, kohde FI ja suomalainen postinumero voittavat foorumikuvakaappaukset ilman Tulli-polkua.",
                ]),
                ("Suositut kategoriat", [
                    "Kengät ja hupparit täyttävät seinän, koska QC-kulmia on yhä. Kassit ja takit seuraavat. Restricted pysyy poissa.",
                    "Kategoria-avaimet ovat englanninkielisiä näyttötekstejä, eivät US-tuontia.",
                ]),
                ("Miten findsit valitaan", [
                    f"Elävä lähde, vähintään yksi varastokuva, arvioijan kohde FI — ei SE, ei tätä verkkotunnusta maana. Osoitetesti: {city}.",
                    "Find ei jää listalle sen takia että se oli suosittu viime kaudella. Jos QC kaatuu, rivi lähtee.",
                ]),
                ("Ovatko findsit turvallisempia kuin haku käsin?", [
                    f"Luet silti {customs} ({curl}) lähetysaamuna. Find tarkoittaa vain että kappale kuvattiin Kiinassa ennen kansainvälistä rahtia.",
                    "Turvallisempi ei ole tulliton. ALV ja Collect voivat yhä tulla. Tämä sivu ei keksi Tulli-euroa.",
                ]),
                ("Kenelle findsit ovat?", [
                    f"Ostajalle, jolla on suomalainen ovi ja joka haluaa QC-tarkistettuja valintoja. Ensimmäinen tilaus kannattaa pitää yksinkertaisissa vaate-SKU:issa.",
                    f"Jos tarra on {city}, pysy tällä Suomen sivustolla.",
                ]),
                ("Valmis avaamaan findsit?", [
                    "Seuraavaksi QC, sitten toimitus. Rekisteröidy kakobuy.comissa.",
                ]),
            ],
        )
    if kind == "qc":
        return (
            f"QC sivustolla {host} tarkoittaa varastokuvia virallisessa {A}-apissa Kiinassa, ennen kuin maksat rahdin Suomeen.",
            [
                ("Mitä QC on tällä sivustolla", [
                    "Quality check on lisäkulmia varastossa — saumat, laput, pohja, printti. Se ei ole laboratorio eikä Tullin röntgen.",
                    "Kuvat tulevat viralliseen appiin kun SKU on vielä Kiinassa. Se on ainoa ikkuna uusintakuvaan.",
                ]),
                ("Milloin pyytää lisäkuvia", [
                    f"Kun SKU on varastossa. Kun {post} on jo kartongissa, {customs} on väärä luukku varastoretakeen.",
                    "Lisäkulmat ovat usein maksullinen lisä virallisessa apissa. Tämä sivu ei avaa tikettejä.",
                ]),
                ("Mitä QC ei tee", [
                    f"QC ei tee tulli-ilmoitusta, ei maksa ALV:ia eikä keksi ilmoitusarvoa. Lähde: {curl}.",
                    "Puhdas QC-albumi ei takaa että SKU läpäisee myöhemmän alustasäännön. Tarkista ennen linjan varausta.",
                ]),
                ("QC ja suomalainen osoite", [
                    f"Arvioijassa FI ja {city}. Ruotsalainen postinumero on väärä maa. Toimitusmuistiinpanot ovat toimitus-sivulla.",
                    "Varastokuvat otetaan silti Kiinassa. Suomen osa on ovi tarrassa QC:n jälkeen.",
                ]),
                ("Jos find kaatuu QC:ssä", [
                    "Jätä varastoon tai palauta virallisen appin mukaan. Älä varaa kansainvälistä rahtia hylkäykselle.",
                    f"Kaatuva QC on halvempi Kiinassa kuin sen jälkeen kun {post} yrittää jakoa.",
                ]),
                ("Valmis toimittamaan QC:n jälkeen?", [
                    f"Vasta sitten virallinen arvioija kohteeseen Suomi. {host} ei ota maksua. Eurot näkyvät apissa.",
                ]),
            ],
        )
    if kind == "shipping":
        return (
            f"{A}-toimitus Suomeen käyttää arvioijan maakoodia FI, ei tätä verkkotunnusta. Avaa virallinen rahtilomake varastokuvien jälkeen. Viimeinen kilometri on usein {post}.",
            [
                ("Miten Kakobuy-toimitus Suomeen etenee", [
                    f"Varasto Kiinassa → hyväksyt QC:n → varaat linjan kohteeseen Suomi → {post} tai SKU:n last-mile luovuttaa. {host} ei tulosta live-hintaa.",
                    f"Tarrassa tarvitaan oikea suomalainen postinumero ({city}). Vahvista kohde FI osoitteessa kakobuy.com/tools/estimate lähetysaamuna.",
                ]),
                ("Toimitusvaihtoehdot suomalaiselle ostajalle", [
                    "Tax-free, prepaid ja collect ovat varatun SKU:n ominaisuuksia virallisessa apissa. Collect voi lisätä välitysmaksun, jota arvioija ei näytä.",
                    f"{post} voi Collectissa lisätä käsittelymaksun. Lue SKU, sitten live-arvioija — ei viime vuoden kuvakaappausta.",
                ]),
                ("Kauanko toimitus Suomeen kestää", [
                    "SKU ja varattu linja ratkaisevat. Tämä sivu ei keksi Postin arkipäiviä.",
                    "Vahvista virallisessa apissa lähetysaamuna. Varastokäsittely on eri asia kuin kansainvälinen transit.",
                ]),
                ("Toimituksen kulut Suomeen", [
                    f"Maksat kansainvälisen rahdin plus sen mitä SKU sanoo rajalla. {post} voi Collectissa lisätä käsittelyn. Tähän titleen ei liimata euroa, koska live-lomake liikkuu.",
                    "EUR on tämän sivuston paikallisvaluutta. Kassa on silti kakobuy.com.",
                ]),
                ("Tulli, ALV ja IOSS Suomessa", [
                    f"Lue {customs} ({curl}) lähetysaamuna. ALV, IOSS ja kynnykset muuttuvat. Vanhat tulliartikkelit tällä sivustolla ovat paikallisia muistiinpanoja, eivät live-tariffia.",
                    "Tämä HTML ei opeta aliarvostusta. Maksa se mitä varattu SKU ja Tulli vaativat.",
                ]),
                ("Tyypilliset toimitusriskit", [
                    f"Väärä maa arvioijassa (SE), rahti ennen QC:tä, {city} pois tarrasta. Nämä ovat Suomen polun virheitä, eivät 'agentti on alhaalla'.",
                    "Restricted-SKU, joka pääsi varastoon, ei silti pääse FI-linjalle jos virallinen appi estää submitin.",
                ]),
                ("Sopiiko ensikertalaiselle?", [
                    f"Kyllä, jos {host} on kartta ja kakobuy.com kassa. Osoitetesti: {city}. Lähde: {customs}.",
                    "Aloita yhdellä vaate-SKU:lla, hyväksy QC, sitten varaa. Älä yhdistä kasaa kuvaamattomia tuoteita ensimmäisellä tilauksella.",
                ]),
                ("Valmis lähettämään Suomeen?", [
                    "QC ensin, sitten virallinen arvioija kohteeseen FI. Tilaukset vain kakobuy.comissa.",
                ]),
            ],
        )
    if kind == "legal":
        return (
            f"{A} on ostoagentti. {host} selittää Suomen polun; se ei ole virallinen appi eikä {customs}. Lue Tulli lähetysaamuna.",
            [
                ("Onko Kakobuy laillinen Suomessa?", [
                    f"Ostoagentin käyttö ei ole rikos Suomessa. Restricted, alustan säännöt ja varattu SKU pätevät silti. Lue {curl} lähetysaamuna.",
                    "Laillinen tarkoittaa agenttimallia. Se ei tarkoita että jokainen Taobao-SKU pääsee Tullista.",
                ]),
                ("Onko Kakobuy turvallinen käyttää?", [
                    "Turvallinen tällä sivulla = varasto-QC ennen rahtia, maksu virallisessa apissa, oikea FI-osoite — ei lupaus että lähetys ohittaa Tullin.",
                    f"Eurot, kohde FI, {city} tarrassa. {host} ei pidä lompakkoa.",
                ]),
                ("Mitkä ovat pääasialliset riskit Suomessa?", [
                    f"Kuolleet lähteet, Collect lukematta SKU:ta, {host} kassana. {post} voi lisätä maksuja.",
                    "Toinen riski: ruotsalainen postinumero, koska arvioijan UI näyttää samalta. Väärä maa tälle sivustolle.",
                ]),
                ("Miten pienentää riskiä?", [
                    f"QC virallisessa apissa, arvioijan kohde FI, {city} tarrassa. Ei aliarvostusta. Ei keksittyä Tulli-euroa.",
                    "Pidä spreadsheet, finds ja QC yhdessä, jotta et varaa rahtia toisen maan sivun kuvakaappauksesta.",
                ]),
                ("Sopiiko ensikertalaiselle Suomessa?", [
                    f"Kyllä, jos aloitat spreadsheetistä ja findsistä sivustolla {host}, sitten virallinen rekisteröinti. Tämä sivusto ei näe tiliä.",
                    "Jätä restricted pois ensimmäisestä tilauksesta. Vaate-SKU:t QC-kuvilla ovat tavallinen alku.",
                ]),
                ("Yhteenveto: kannattaako Kakobuyta käyttää Suomessa?", [
                    f"{A}:ta voi käyttää Suomeen, jos noudatat virallista appia ja {customs}ia. Tämä sivusto pysyy tietosivuna. Tilaukset kakobuy.comissa.",
                ]),
                ("Miten aloittaa?", [
                    "Spreadsheet → finds → QC → toimitus. Maksa vain kakobuy.comissa.",
                ]),
            ],
        )
    return (
        f"Vastauksia suomalaiselle ostajalle, joka käyttää {A}-spreadsheetiä sivustolla {host}: QC, toimitus, ALV ja tarvitaanko sheettiä.",
        [
            ("Tarvitsenko tilin Kakobuyhin?", [
                f"Kyllä, virallisella {A}-sivustolla. {host} ei luo tilejä eikä nollaa salasanaa.",
            ]),
            ("Onko Kakobuy turvallinen ensikertalaiselle Suomessa?", [
                f"QC-kuvat ennen rahtia, kohde FI, {city} tarrassa. Lue {customs}. Tämä sivu ei opeta ilmoitusarvoa.",
            ]),
            ("Miten suomalaiset ostajat löytävät luotettavia tuotteita?", [
                "Aloita tämän sivuston spreadsheetistä ja findsistä. Kuolleet Weidian-linkit putoavat. Tarkista virallinen appi ennen rahtia.",
            ]),
            ("Saanko QC-kuvat?", [
                "Virallisessa apissa, Kiinassa, ennen kansainvälistä rahtia. Lisäkulmat usein maksullisia.",
            ]),
            ("Kauanko toimitus Suomeen yleensä kestää?", [
                f"SKU ja linja ratkaisevat. Tämä sivu ei keksi {post}-päiviä. Vahvista virallisessa arvioijassa.",
            ]),
            ("Maksanko tullin tai ALV:n Suomessa?", [
                f"Varattu SKU sanoo kuka maksaa. Collect voi lisätä maksun. Lähde: {customs} ({curl}). Kynnykset muuttuvat; emme liimaa prosenttia.",
            ]),
            ("Spreadsheet vai haku käsin?", [
                f"Sheet sivustolla {host} on olemassa, jotta suomalainen ostaja ei metsästä kuolleita kortteja. Se on silti indeksi, ei Excel. Voit hakea apista käsin.",
            ]),
            ("Mitä yleensä ostetaan?", [
                "Kengät, hupparit, takit, kassit — jos varastossa on vielä QC. Restricted pois.",
            ]),
            ("Voinko käyttää Kakobuyta ilman spreadsheetiä?", [
                "Kyllä. Spreadsheet on oikotie, ei portti. Ensikertalainen yleensä pääsee nopeammin sheetillä ja QC-kuvilla.",
            ]),
            ("Valmis tilaamaan?", [
                "Avaa spreadsheet, finds, QC ja toimitus, sitten rekisteröidy kakobuy.comissa.",
            ]),
        ],
    )


def _es(kind, host, d):
    post, city, customs, curl = d["post"], d["city"], d["customs"], d["customs_url"]
    if kind == "spreadsheet":
        return (
            f"Spreadsheet {A} para compradores en España en {host}: vendedores de confianza, fotos QC y finds en un índice. No es Excel ni caja. Pedidos en kakobuy.com en EUR, destino España.",
            [
                ("Qué es un spreadsheet Kakobuy?", [
                    f"En {host} es una lista corta de SKU fotografiados en almacén para una dirección en España — zapatillas, sudaderas, chaquetas y bolsos que aún abren en la app oficial. No cobra y no es otra tienda Kakobuy.",
                    "La fila solo sirve si el enlace vive y hay al menos una foto de almacén. Precio 0 o restricted es fuente muerta, no oferta. Keywords: Kakobuy spreadsheet, kakobuy spreadsheet espana, kakobuy trusted sellers.",
                ]),
                ("Por qué un comprador en España empieza por la hoja", [
                    f"Buscar Taobao, 1688 y Weidian a mano llena el feed de tarjetas muertas. La hoja guarda finds ya aceptados en QC antes de que {post} mueva el cartón hacia {city}.",
                    "El camino español no es un código francés. Estimador: España, no FR, no un CAP italiano. El test de dirección es un código postal de cinco dígitos.",
                ]),
                ("Cómo funciona el spreadsheet Kakobuy", [
                    f"Abres un find en {host}, lees las fotos de almacén en la app oficial {A} y reservas una línea internacional con destino España. Carrito, pago y tickets quedan en kakobuy.com.",
                    "Las claves de catálogo en inglés (sneakers, hoodie) son etiquetas de pantalla, no una tienda US.",
                ]),
                ("Qué tipos de productos incluye?", [
                    "Zapatos, sudaderas, chaquetas, bolsos y relojes, porque aún tienen ángulos QC. Electrónica, perfume y otras clases restricted se quedan fuera salvo que la app oficial las permita el día del envío.",
                    "Un find aceptado el mes pasado puede pasar a restricted. Revisa la ficha oficial antes del flete.",
                ]),
                ("¿Es más seguro que buscar a mano?", [
                    f"Más seguro significa fotos de almacén antes del flete internacional — no que {customs} desaparezca. Lee {curl} la mañana del envío. IVA y Collect cambian; esta página no pega un tipo en el title.",
                    "La hoja evita enlaces Weidian muertos. No presenta un DUA y no elige un valor declarado.",
                ]),
                ("Para quién es esta hoja", [
                    f"Para quien prueba una dirección ({city}) y para quien ya usa {A} pero quiere spreadsheet, finds, QC y envío a España en un sitio español.",
                    "Si envías a Francia, esta es la página del país equivocado. Para aduana, {customs}, no esta URL.",
                ]),
                ("Errores sin hoja", [
                    f"Un código francés en el estimador, tratar {host} como caja, flete antes del QC. La última milla suele ser {post}; Collect puede añadir un recargo.",
                    "Otro error: creer que un artículo de IVA antiguo en este sitio es un arancel vigente. Los umbrales se mueven. Confirma en la app y en la Agencia Tributaria el día del envío.",
                ]),
                ("Uso eficiente", [
                    f"Spreadsheet, finds y QC en la misma tira de pestañas. Find aceptado → formulario oficial hacia España, etiqueta con {city}. Fuente: {customs}.",
                    "Sin trucos de infradeclaración. Paga lo que muestren el SKU y el estimador. Pedidos en kakobuy.com.",
                ]),
                ("¿Hace falta el spreadsheet?", [
                    "No. Puedes buscar a mano en la app oficial. La hoja existe para que el comprador en España no empiece cada semana entre miles de tarjetas muertas.",
                    f"Registro y pago siguen en kakobuy.com. {host} no ve la cuenta.",
                ]),
                ("¿Listo para usar el spreadsheet?", [
                    "Abre finds, QC y envío. Regístrate en kakobuy.com. Este sitio sigue siendo un índice.",
                ]),
            ],
        )
    if kind == "finds":
        return (
            f"Finds del spreadsheet {A} para España en {host}: zapatillas, sudaderas y bolsos con QC para una dirección española, no un segundo catálogo mundial.",
            [
                ("Qué son los finds Kakobuy?", [
                    f"En {host} son SKU que se quedan después de las fotos de almacén. No son un escaparate.",
                    "El find cae cuando muere la fuente o el almacén ya no tiene la pieza. Precio 0 es tarjeta retirada.",
                ]),
                ("Por qué usar finds curados en España", [
                    f"La búsqueda manual mezcla Weidian muertos. Los finds curados aún se fotografían en China antes de {post} hacia {city}.",
                    "EUR en la app, destino España y un CP de cinco dígitos ganan a capturas de foros sin ruta de Agencia Tributaria.",
                ]),
                ("Categorías populares", [
                    "Zapatillas y sudaderas llenan el muro porque aún hay ángulos QC. Bolsos y chaquetas siguen. Restricted fuera.",
                    "Las claves de categoría en inglés son etiquetas, no importación US.",
                ]),
                ("Cómo se seleccionan", [
                    f"URL viva, al menos una foto de almacén, destino del estimador España — no un código francés, no este hostname como país. Test: {city}.",
                    "Un find no se queda porque fue popular la temporada pasada. Si el QC falla, sale de la lista.",
                ]),
                ("¿Son más seguros que buscar a mano?", [
                    f"Aun así lees {customs} ({curl}) la mañana del envío. Find solo significa que se fotografió en China antes del flete internacional.",
                    "Más seguro no es libre de IVA. Collect puede aplicar. Esta página no inventa un euro de aduana.",
                ]),
                ("Para quién son", [
                    f"Quien tiene puerta en España y quiere picks con QC. El primer pedido conviene en SKU de ropa con fotos.",
                    f"Si la etiqueta es {city}, quédate en este sitio de España.",
                ]),
                ("¿Listo para ver finds?", [
                    "Sigue QC y luego envío. Registro en kakobuy.com.",
                ]),
            ],
        )
    if kind == "qc":
        return (
            f"QC en {host} son fotos de almacén en la app oficial {A}, en China, antes de pagar el flete a España.",
            [
                ("Qué es el QC en este sitio", [
                    "Quality check son ángulos extra en almacén — costuras, etiquetas, suela, print. No es un laboratorio ni un escáner de aduana.",
                    "Las fotos llegan a la app oficial mientras el SKU sigue en China. Esa es la única ventana para un retake.",
                ]),
                ("Cuándo pedir más fotos", [
                    f"Mientras el SKU está en almacén. Cuando {post} ya tiene el cartón, {customs} no es la ventanilla de un retake de almacén.",
                    "Los ángulos extra suelen ser un extra de pago en la app oficial. Este HTML no abre tickets.",
                ]),
                ("Lo que el QC no hace", [
                    f"El QC no presenta un DUA, no paga IVA y no inventa un valor declarado. Fuente: {curl}.",
                    "Un álbum limpio no garantiza que el SKU pase una regla posterior de la plataforma. Revisa antes de reservar la línea.",
                ]),
                ("QC y una dirección en España", [
                    f"Estimador: España y {city}. Un código francés es el país equivocado. Las notas de última milla están en la página de envío.",
                    "Las fotos de almacén se hacen en China igual. La parte española es la puerta en la etiqueta después del QC.",
                ]),
                ("Si el find falla el QC", [
                    "Déjalo en almacén o devuélvelo en la app oficial. No reserves flete internacional sobre un rechazo.",
                    f"Un QC fallido es más barato en China que cuando {post} intenta entregar.",
                ]),
                ("¿Enviar después del QC?", [
                    f"Solo entonces el estimador oficial hacia España. {host} no cobra. Los totales en EUR viven en la app.",
                ]),
            ],
        )
    if kind == "shipping":
        return (
            f"El envío {A} a España usa el código de país del estimador (ES), no este dominio. Abre el formulario oficial después de las fotos de almacén. La última milla suele ser {post}.",
            [
                ("Cómo llega un paquete Kakobuy a España", [
                    f"Almacén en China → aceptas QC → reservas una línea con destino España → {post} o el last-mile del SKU entrega. {host} no imprime un presupuesto en vivo.",
                    f"La etiqueta necesita un CP español de cinco dígitos ({city}). Confirma destino ES en kakobuy.com/tools/estimate la mañana del envío.",
                ]),
                ("Opciones de envío para España", [
                    "Tax-free, prepaid y collect son propiedades del SKU reservado en la app oficial. Collect puede añadir un recargo de despacho que el estimador oculta.",
                    f"{post} puede añadir manejo en collect. Lee el SKU y luego el estimador en vivo, no una captura del año pasado.",
                ]),
                ("Cuánto tarda el envío a España", [
                    "El SKU y la línea reservada deciden. Esta página no inventa días laborables de Correos.",
                    "Confirma en la app oficial la mañana del envío. El procesado de almacén no es el tránsito internacional.",
                ]),
                ("Costes de envío a España", [
                    f"Pagas el flete internacional más lo que el SKU diga en frontera. {post} puede añadir manejo en collect. No se pega un importe en este title porque el formulario vivo se mueve.",
                    "EUR es la moneda local de este sitio. La caja sigue en kakobuy.com.",
                ]),
                ("Aduana e IVA en España", [
                    f"Lee {customs} ({curl}) la mañana del envío. IVA y umbrales cambian. Los artículos de aduana ya ranqueados en este sitio son notas locales, no una tabla arancelaria en vivo.",
                    "Este HTML no enseña a infradeclarar. Paga lo que exijan el SKU y la Agencia Tributaria.",
                ]),
                ("Riesgos habituales", [
                    f"País equivocado en el estimador (código FR), flete antes del QC, omitir {city}. Son errores de la ruta española, no 'el agente está caído'.",
                    "Un SKU restricted que llegó al almacén igual no sale en una línea ES si la app oficial bloquea el submit.",
                ]),
                ("¿Sirve para una primera compra en España?", [
                    f"Sí si {host} es el mapa y kakobuy.com la caja. Test de dirección: {city}. Fuente: {customs}.",
                    "Empieza con un SKU de ropa, acepta QC, luego reserva. No consolides un montón sin fotos en el primer pedido.",
                ]),
                ("¿Listo para enviar a España?", [
                    "QC primero, luego estimador oficial hacia ES. Pedidos solo en kakobuy.com.",
                ]),
            ],
        )
    if kind == "legal":
        return (
            f"{A} es un agente de compra. {host} explica la ruta de España; no es la app oficial ni {customs}. Lee la Agencia Tributaria la mañana del envío.",
            [
                ("¿Es legal Kakobuy en España?", [
                    f"Usar un agente de compra no es un delito en España. Restricted, normas de plataforma y el SKU reservado siguen aplicando. Lee {curl} la mañana del envío.",
                    "Legal habla del modelo de agente. No significa que cada SKU de Taobao pase aduana.",
                ]),
                ("¿Es seguro usar Kakobuy?", [
                    "Seguro en esta página = QC de almacén antes del flete, pago en la app oficial, dirección española real — no una promesa de que el bulto esquiva a la Agencia Tributaria.",
                    f"EUR, destino España, {city} en la etiqueta. {host} no guarda el monedero.",
                ]),
                ("Riesgos principales en España", [
                    f"Enlaces muertos, collect sin leer el SKU, tratar {host} como caja. {post} puede añadir recargos.",
                    "Otro riesgo: pegar un código francés porque la UI del estimador se parece. País equivocado para este sitio.",
                ]),
                ("Cómo reducir el riesgo", [
                    f"QC en la app oficial, destino España, {city} en la etiqueta. Sin infradeclaración. Sin un euro de aduana inventado.",
                    "Mantén spreadsheet, finds y QC juntos para no reservar flete desde la captura de otra página de país.",
                ]),
                ("¿Sirve para una primera compra?", [
                    f"Sí si empiezas por el spreadsheet y los finds en {host} y luego el registro oficial. Este sitio no ve la cuenta.",
                    "Deja restricted fuera del primer pedido. SKU de ropa con fotos QC es el camino habitual.",
                ]),
                ("Veredicto", [
                    f"{A} puede usarse hacia España si sigues la app oficial y {customs}. Este sitio sigue siendo información. Pedidos en kakobuy.com.",
                ]),
                ("Por dónde empezar", [
                    "Spreadsheet → finds → QC → envío. Paga solo en kakobuy.com.",
                ]),
            ],
        )
    if kind == "guide":
        return (
            f"Ruta {A} paso a paso para una dirección en España en {host}. Fotos en almacén, luego flete. No es la caja.",
            [
                ("Cómo comprar en Kakobuy (guía España)", [
                    f"Elige un SKU con QC en el spreadsheet o en finds, envíalo en la app oficial, espera las fotos de almacén y reserva flete internacional hacia España con {city} en la etiqueta.",
                    "No saltes el QC para ganar un día. La última milla española no va a repetir una foto de almacén.",
                ]),
                ("Qué es Kakobuy", [
                    f"Un agente de compra en China. {host} solo explica la ruta de España en EUR. Pago, tickets y estimador en kakobuy.com.",
                    "Dos pagos son normales: mercancía al almacén y flete internacional después del QC.",
                ]),
                ("Paso 1: encontrar el producto", [
                    "Usa el spreadsheet y los finds de este sitio de España. Omite precio 0 y restricted. Las claves de categoría en inglés son etiquetas, no una tienda US.",
                ]),
                ("Paso 2: enviar el pedido en Kakobuy", [
                    f"Solo la app oficial. Este HTML no ve el carrito. Regístrate en kakobuy.com, no en {host}.",
                ]),
                ("Paso 3: QC en el almacén", [
                    "Fotos antes del flete. Ángulos extra a menudo de pago. Rechaza en la app si la pieza está mal — no reserves la línea a España sobre un fallo.",
                ]),
                ("Paso 4: envío internacional a España", [
                    f"Destino del estimador ES, dirección {city}. Lee {customs} ({curl}) la mañana del envío. No pegues un código francés.",
                ]),
                ("Paso 5: recibir el paquete en España", [
                    f"La última milla suele ser {post}. Collect puede añadir un recargo. El tracking vive en la app oficial.",
                ]),
                ("Consejos para el primer pedido", [
                    "Un SKU de ropa sencillo. QC antes del flete. Destino España siempre. Esta página no enseña valores declarados.",
                ]),
                ("¿Sirve para principiantes?", [
                    f"Sí si {host} es el mapa y kakobuy.com la caja. Fuente: {customs}.",
                ]),
            ],
        )
    return (
        f"Respuestas para compradores en España que usan el spreadsheet {A} en {host}: QC, envío, IVA y si hace falta la hoja.",
        [
            ("¿Hace falta una cuenta en Kakobuy?", [
                f"Sí, en el sitio oficial {A}. {host} no crea cuentas ni restablece contraseñas.",
            ]),
            ("¿Es seguro Kakobuy para una primera compra en España?", [
                f"Fotos QC antes del flete, destino España, {city} en la etiqueta. Lee {customs}. Esta página no enseña un valor declarado.",
            ]),
            ("¿Cómo encuentran productos fiables?", [
                "Empieza por el spreadsheet y los finds de este sitio. Los Weidian muertos caen. Revisa la app oficial antes de pagar el flete.",
            ]),
            ("¿Recibiré fotos QC?", [
                "En la app oficial, en China, antes del flete internacional. Ángulos extra a menudo de pago.",
            ]),
            ("¿Cuánto tarda el envío a España?", [
                f"Depende del SKU y de la línea. Esta página no inventa días de {post}. Confirma en el estimador oficial.",
            ]),
            ("¿Pago IVA o aduana en España?", [
                f"El SKU reservado dice quién paga. Collect puede añadir recargo. Fuente: {customs} ({curl}). Los umbrales cambian; no pegamos un tipo.",
            ]),
            ("¿Spreadsheet o búsqueda manual?", [
                f"La hoja en {host} existe para no cazar tarjetas muertas. Sigue siendo un índice, no Excel. Puedes buscar a mano en la app.",
            ]),
            ("¿Qué se compra habitualmente?", [
                "Zapatos, sudaderas, chaquetas, bolsos — si el almacén aún tiene QC. Restricted fuera.",
            ]),
            ("¿Puedo usar Kakobuy sin spreadsheet?", [
                "Sí. El spreadsheet es un atajo, no una puerta. Quien empieza suele acabar antes con la hoja y las fotos QC.",
            ]),
            ("¿Listo para comprar?", [
                "Abre spreadsheet, finds, QC y envío, luego regístrate en kakobuy.com.",
            ]),
        ],
    )


def _fr(kind, host, d):
    post, city, customs, curl = d["post"], d["city"], d["customs"], d["customs_url"]
    if kind == "spreadsheet":
        return (
            f"Spreadsheet {A} pour les acheteurs en France sur {host} : vendeurs suivis, photos QC et finds dans un index. Pas Excel, pas la caisse. Commandes sur kakobuy.com en EUR, destination France.",
            [
                ("Qu’est-ce qu’un spreadsheet Kakobuy ?", [
                    f"Sur {host}, une liste courte de SKU photographiés en entrepôt pour une adresse en France — sneakers, sweats, vestes et sacs qui s’ouvrent encore dans l’app officielle. Ça n’encaisse rien et ce n’est pas une seconde boutique Kakobuy.",
                    "La ligne ne sert que si le lien source vit et qu’il reste une photo d’entrepôt. Prix 0 ou restricted = source morte, pas une affaire. Mots-clés : Kakobuy spreadsheet, kakobuy spreadsheet france, kakobuy trusted sellers.",
                ]),
                ("Pourquoi un acheteur en France commence par la feuille", [
                    f"Taobao, 1688 et Weidian à la main remplissent le fil de cartes mortes. La feuille garde les finds déjà acceptés en QC avant que {post} déplace le carton vers {city}.",
                    "Le chemin français n’est pas un code belge. Estimateur : France, pas BE, pas un Packstation allemand. Le test d’adresse est un code postal à cinq chiffres.",
                ]),
                ("Comment marche un spreadsheet Kakobuy", [
                    f"Tu ouvres un find sur {host}, tu lis les photos d’entrepôt dans l’app officielle {A}, tu réserves une ligne internationale vers la France. Panier, paiement et tickets restent sur kakobuy.com.",
                    "Les clés catalogue en anglais (sneakers, hoodie) sont des libellés d’affichage, pas une boutique US.",
                ]),
                ("Quelles familles de produits ?", [
                    "Chaussures, sweats, vestes, sacs et montres, tant qu’il reste des angles QC. Électronique, parfum et autres classes restricted restent dehors sauf si l’app officielle les autorise le matin de l’envoi.",
                    "Un find accepté le mois dernier peut passer restricted. Revérifie la fiche officielle avant le fret.",
                ]),
                ("Plus sûr que la recherche manuelle ?", [
                    f"Plus sûr = photos d’entrepôt avant le fret international, pas que {customs} disparaît. Lis {curl} le matin de l’envoi. TVA, IOSS et Collect bougent ; on ne colle pas un taux dans le title.",
                    "La feuille écarte les Weidian morts. Elle ne dépose pas une déclaration en douane et ne choisit pas une valeur déclarée.",
                ]),
                ("Pour qui", [
                    f"Pour un premier test d’adresse ({city}) et pour qui utilise déjà {A} mais veut spreadsheet, finds, QC et livraison France sur un site français.",
                    "Si tu expédies en Belgique, mauvaise page pays. Pour la douane, {customs}, pas cette URL.",
                ]),
                ("Erreurs sans feuille", [
                    f"Un code belge dans l’estimateur, prendre {host} pour une caisse, fret avant QC. Le dernier kilomètre est souvent {post} ; Collect peut ajouter des frais.",
                    "Autre erreur : croire qu’un vieux texte TVA sur ce site est un tarif en vigueur. Les seuils bougent. Confirme dans l’app et sur douane.gouv.fr le jour de l’envoi.",
                ]),
                ("Usage efficace", [
                    f"Spreadsheet, finds et QC dans le même jeu d’onglets. Find accepté → formulaire officiel vers la France, étiquette {city}. Source : {customs}.",
                    "Pas de sous-déclaration. Paie ce que montrent le SKU et l’estimateur. Commandes sur kakobuy.com.",
                ]),
                ("Le spreadsheet est-il obligatoire ?", [
                    "Non. Tu peux chercher à la main dans l’app officielle. La feuille existe pour qu’un acheteur en France ne reparte pas chaque semaine de milliers de cartes mortes.",
                    f"Inscription et paiement restent sur kakobuy.com. {host} ne voit pas le compte.",
                ]),
                ("Prêt à utiliser le spreadsheet ?", [
                    "Ouvre finds, QC et livraison. Inscris-toi sur kakobuy.com. Ce site reste un index.",
                ]),
            ],
        )
    if kind == "finds":
        return (
            f"Finds du spreadsheet {A} pour la France sur {host} : sneakers, sweats et sacs déjà en QC pour une adresse française, pas un second catalogue mondial.",
            [
                ("Qu’est-ce qu’un find Kakobuy ?", [
                    f"Sur {host}, des SKU gardés après les photos d’entrepôt. Ce n’est pas une vitrine.",
                    "Le find tombe quand la source meurt ou que l’entrepôt n’a plus la pièce. Prix 0 = carte retirée.",
                ]),
                ("Pourquoi des finds curatés en France", [
                    f"La recherche manuelle mélange des Weidian morts. Les finds curatés sont encore photographiés en Chine avant {post} vers {city}.",
                    "EUR dans l’app, destination France et un CP à cinq chiffres battent les captures de forum sans parcours douane.gouv.fr.",
                ]),
                ("Catégories fréquentes", [
                    "Sneakers et sweats remplissent le mur tant qu’il reste des angles QC. Sacs et vestes suivent. Restricted dehors.",
                    "Les clés de catégorie en anglais sont des libellés, pas une import US.",
                ]),
                ("Comment on sélectionne", [
                    f"URL vivante, au moins une photo d’entrepôt, destination estimateur France — pas BE, pas ce nom d’hôte comme pays. Test : {city}.",
                    "Un find ne reste pas parce qu’il était populaire la saison dernière. Si le QC échoue, il sort.",
                ]),
                ("Plus sûr que chercher à la main ?", [
                    f"Tu lis quand même {customs} ({curl}) le matin de l’envoi. Find = photographié en Chine avant le fret international.",
                    "Plus sûr n’est pas hors TVA. Collect peut s’appliquer. Cette page n’invente pas un euro de douane.",
                ]),
                ("Pour qui", [
                    f"Qui a une porte en France et veut des picks déjà en QC. La première commande reste sur des SKU vêtements avec photos.",
                    f"Si l’étiquette est {city}, reste sur ce site France.",
                ]),
                ("Ouvrir les finds", [
                    "Ensuite QC, puis livraison. Inscription sur kakobuy.com.",
                ]),
            ],
        )
    if kind == "qc":
        return (
            f"Le QC sur {host} ce sont les photos d’entrepôt dans l’app officielle {A}, en Chine, avant de payer le fret vers la France.",
            [
                ("Le QC sur ce site", [
                    "Quality check = angles supplémentaires en entrepôt — coutures, étiquettes, semelle, print. Pas un labo, pas un scanner douane.",
                    "Les photos arrivent dans l’app officielle tant que le SKU est en Chine. C’est la seule fenêtre pour un retake.",
                ]),
                ("Quand demander plus de photos", [
                    f"Tant que le SKU est en entrepôt. Quand {post} a le carton, {customs} n’est pas le guichet d’un retake entrepôt.",
                    "Les angles extra sont souvent un add-on payant dans l’app officielle. Cet HTML n’ouvre pas de ticket.",
                ]),
                ("Ce que le QC ne fait pas", [
                    f"Le QC ne dépose pas une déclaration, ne paie pas la TVA et n’invente pas une valeur. Source : {curl}.",
                    "Un album propre ne garantit pas qu’un SKU passera une règle plateforme plus tard. Revérifie avant de réserver la ligne.",
                ]),
                ("QC et adresse en France", [
                    f"Estimateur : France et {city}. Un code belge est le mauvais pays. Les notes de dernier kilomètre sont sur la page livraison.",
                    "Les photos d’entrepôt se font en Chine dans tous les cas. La partie France, c’est la porte sur l’étiquette après le QC.",
                ]),
                ("Si le find échoue au QC", [
                    "Laisse-le en entrepôt ou retourne selon l’app officielle. Ne réserve pas le fret international sur un rejet.",
                    f"Un QC refusé coûte moins cher en Chine que lorsque {post} tente la livraison.",
                ]),
                ("Expédier après QC ?", [
                    f"Ensuite seulement l’estimateur officiel vers la France. {host} n’encaisse rien. Les totaux EUR sont dans l’app.",
                ]),
            ],
        )
    if kind == "shipping":
        return (
            f"La livraison {A} vers la France utilise le code pays de l’estimateur (FR), pas ce domaine. Ouvre le formulaire officiel après les photos d’entrepôt. Dernier kilomètre souvent {post}.",
            [
                ("Comment un colis Kakobuy arrive en France", [
                    f"Entrepôt Chine → tu acceptes le QC → tu réserves une ligne vers la France → {post} ou le last-mile du SKU remet. {host} n’imprime pas un devis live.",
                    f"L’étiquette demande un vrai CP français à cinq chiffres ({city}). Confirme la destination FR sur kakobuy.com/tools/estimate le matin de l’envoi.",
                ]),
                ("Options de livraison pour la France", [
                    "Tax-free, prepaid et collect sont des propriétés du SKU réservé dans l’app officielle. Collect peut ajouter des frais de dédouanement que l’estimateur cache.",
                    f"{post} peut ajouter des frais de handling en collect. Lis le SKU, puis l’estimateur live — pas une capture de l’an dernier.",
                ]),
                ("Délais vers la France", [
                    "Le SKU et la ligne réservée décident. Cette page n’invente pas les jours Colissimo.",
                    "Confirme dans l’app officielle le matin de l’envoi. Le processing entrepôt n’est pas le transit international.",
                ]),
                ("Coûts de livraison vers la France", [
                    f"Tu paies le fret international plus ce que dit le SKU à la frontière. {post} en collect peut ajouter du handling. Pas de montant collé dans ce title : le formulaire live bouge.",
                    "EUR est la monnaie locale de ce site. La caisse reste kakobuy.com.",
                ]),
                ("Douane, TVA et IOSS en France", [
                    f"Lis {customs} ({curl}) le matin de l’envoi. TVA, IOSS et seuils bougent. Les articles douane déjà classés ici sont des notes locales, pas un tarif live.",
                    "Cet HTML n’apprend pas à sous-déclarer. Paie ce qu’exigent le SKU et la douane.",
                ]),
                ("Risques fréquents", [
                    f"Mauvais pays dans l’estimateur (BE), fret avant QC, omettre {city}. Ce sont des erreurs du parcours France, pas « l’agent est down ».",
                    "Un SKU restricted arrivé en entrepôt ne sort pas sur une ligne FR si l’app officielle bloque le submit.",
                ]),
                ("Adapté à une première commande en France ?", [
                    f"Oui si {host} est la carte et kakobuy.com la caisse. Test d’adresse : {city}. Source : {customs}.",
                    "Commence par un SKU vêtement, accepte le QC, puis réserve. Ne consolide pas une pile sans photos dès la première commande.",
                ]),
                ("Prêt à expédier vers la France ?", [
                    "QC d’abord, puis estimateur officiel vers FR. Commandes uniquement sur kakobuy.com.",
                ]),
            ],
        )
    if kind == "legal":
        return (
            f"{A} est un agent d’achat. {host} explique le parcours France ; ce n’est pas l’app officielle ni {customs}. Lis douane.gouv.fr le matin de l’envoi.",
            [
                ("Kakobuy est-il légal en France ?", [
                    f"Utiliser un agent d’achat n’est pas un délit en France. Restricted, règles de plateforme et SKU réservé restent. Lis {curl} le matin de l’envoi.",
                    "Légal parle du modèle d’agent. Ça ne veut pas dire que chaque SKU Taobao passe la douane.",
                ]),
                ("Est-ce sûr d’utiliser Kakobuy ?", [
                    "Sûr sur cette page = QC entrepôt avant fret, paiement dans l’app officielle, vraie adresse FR — pas une promesse que le carton ignore la douane.",
                    f"EUR, destination France, {city} sur l’étiquette. {host} ne tient pas le portefeuille.",
                ]),
                ("Risques principaux en France", [
                    f"Liens morts, collect sans lire le SKU, prendre {host} pour une caisse. {post} peut ajouter des frais.",
                    "Autre risque : coller un code belge parce que l’UI de l’estimateur se ressemble. Mauvais pays pour ce site.",
                ]),
                ("Comment réduire le risque", [
                    f"QC dans l’app officielle, destination France, {city} sur l’étiquette. Pas de sous-déclaration. Pas d’euro douane inventé.",
                    "Garde spreadsheet, finds et QC ensemble pour ne pas réserver du fret depuis la capture d’une autre page pays.",
                ]),
                ("Adapté à une première commande ?", [
                    f"Oui si tu commences par le spreadsheet et les finds sur {host}, puis l’inscription officielle. Ce site ne voit pas le compte.",
                    "Laisse restricted hors de la première commande. Les SKU vêtements avec photos QC sont le chemin habituel.",
                ]),
                ("Verdict", [
                    f"{A} peut servir vers la France si tu suis l’app officielle et {customs}. Ce site reste de l’information. Commandes sur kakobuy.com.",
                ]),
                ("Par où commencer", [
                    "Spreadsheet → finds → QC → livraison. Paiement uniquement sur kakobuy.com.",
                ]),
            ],
        )
    if kind == "guide":
        return (
            f"Parcours {A} pas à pas pour une adresse en France sur {host}. Photos en entrepôt, puis fret. Pas la caisse.",
            [
                ("Comment acheter sur Kakobuy (guide France)", [
                    f"Trouve un SKU avec QC sur le spreadsheet ou les finds, soumets-le dans l’app officielle, attends les photos d’entrepôt, réserve le fret international vers la France avec {city} sur l’étiquette.",
                    "Ne saute pas le QC pour gagner un jour. Le last-mile français ne refera pas une photo d’entrepôt.",
                ]),
                ("Qu’est-ce que Kakobuy ?", [
                    f"Un agent d’achat en Chine. {host} explique seulement le parcours France en EUR. Paiement, tickets et estimateur sur kakobuy.com.",
                    "Deux paiements sont normaux : marchandise vers l’entrepôt, puis fret international après QC.",
                ]),
                ("Étape 1 : trouver le produit", [
                    "Utilise le spreadsheet et les finds de ce site France. Ignore prix 0 et restricted. Les clés de catégorie en anglais sont des libellés, pas une boutique US.",
                ]),
                ("Étape 2 : passer commande sur Kakobuy", [
                    f"App officielle seulement. Cet HTML ne voit pas le panier. Inscris-toi sur kakobuy.com, pas sur {host}.",
                ]),
                ("Étape 3 : QC en entrepôt", [
                    "Photos avant le fret. Angles extra souvent payants. Refuse dans l’app si la pièce est mauvaise — ne réserve pas la ligne France sur un échec.",
                ]),
                ("Étape 4 : livraison internationale vers la France", [
                    f"Destination estimateur FR, adresse {city}. Lis {customs} ({curl}) le matin de l’envoi. Pas de code belge.",
                ]),
                ("Étape 5 : réception en France", [
                    f"Dernier kilomètre souvent {post}. Collect peut ajouter des frais. Le tracking vit dans l’app officielle.",
                ]),
                ("Conseils première commande", [
                    "Un SKU vêtement simple. QC avant fret. Destination France à chaque fois. Cette page n’apprend pas de valeur déclarée.",
                ]),
                ("Adapté aux débutants ?", [
                    f"Oui si {host} est la carte et kakobuy.com la caisse. Source : {customs}.",
                ]),
            ],
        )
    return (
        f"Réponses pour les acheteurs en France qui utilisent le spreadsheet {A} sur {host} : QC, livraison, TVA, et s’il faut la feuille.",
        [
            ("Faut-il un compte Kakobuy ?", [
                f"Oui, sur le site officiel {A}. {host} ne crée pas de compte et ne réinitialise pas un mot de passe.",
            ]),
            ("Kakobuy est-il sûr pour une première commande en France ?", [
                f"Photos QC avant fret, destination France, {city} sur l’étiquette. Lis {customs}. Cette page n’apprend pas de valeur déclarée.",
            ]),
            ("Comment trouve-t-on des produits fiables ?", [
                "Commence par le spreadsheet et les finds de ce site. Les Weidian morts tombent. Revérifie l’app officielle avant de payer le fret.",
            ]),
            ("Aurai-je des photos QC ?", [
                "Dans l’app officielle, en Chine, avant le fret international. Angles extra souvent payants.",
            ]),
            ("Quel délai vers la France ?", [
                f"Ça dépend du SKU et de la ligne. Cette page n’invente pas les jours {post}. Confirme dans l’estimateur officiel.",
            ]),
            ("TVA ou droits en France ?", [
                f"Le SKU réservé dit qui paie. Collect peut ajouter des frais. Source : {customs} ({curl}). Les seuils bougent ; on ne colle pas un taux.",
            ]),
            ("Spreadsheet ou recherche manuelle ?", [
                f"La feuille sur {host} existe pour ne pas chasser des cartes mortes. C’est toujours un index, pas Excel. Tu peux chercher à la main dans l’app.",
            ]),
            ("Qu’est-ce qu’on achète le plus ?", [
                "Chaussures, sweats, vestes, sacs — s’il reste du QC en entrepôt. Restricted dehors.",
            ]),
            ("Puis-je utiliser Kakobuy sans spreadsheet ?", [
                "Oui. Le spreadsheet est un raccourci, pas une barrière. Un débutant finit souvent plus vite avec la feuille et les photos QC.",
            ]),
            ("Prêt à commander ?", [
                "Ouvre spreadsheet, finds, QC et livraison, puis inscris-toi sur kakobuy.com.",
            ]),
        ],
    )


def _nl(kind, host, d):
    post, city, customs, curl = d["post"], d["city"], d["customs"], d["customs_url"]
    if kind == "spreadsheet":
        return (
            f"Een {A}-spreadsheet voor kopers in Nederland op {host}: vertrouwde sellers, QC-foto’s en finds in één index. Geen Excel, geen kassa. Bestellen op kakobuy.com in EUR, bestemming Nederland.",
            [
                ("Wat is een Kakobuy spreadsheet?", [
                    f"Op {host} is het een korte lijst magazijn-SKU’s voor een Nederlands adres — sneakers, hoodies, jassen en tassen die nog openen in de officiële app. Het neemt geen betaling aan en is geen tweede Kakobuy-winkel.",
                    "Een rij blijft alleen nuttig als de bronlink leeft en er minstens één magazijnfoto is. Prijs 0 of restricted is een dode bron, geen sale. Keywords: Kakobuy spreadsheet, kakobuy spreadsheet nederland, kakobuy trusted sellers.",
                ]),
                ("Waarom een NL-koper met een sheet begint", [
                    f"Taobao, 1688 en Weidian met de hand vullen de feed met dode kaarten. De sheet bewaart finds die je in QC al accepteerde voordat {post} de doos naar {city} brengt.",
                    "Het NL-pad is geen Duits Packstation en geen Belgische postcode. Estimator: Nederland, niet DE, niet BE. Adrestest is een postcode in de vorm 1234 AB.",
                ]),
                ("Hoe een Kakobuy-spreadsheet werkt", [
                    f"Je opent een find op {host}, leest magazijnfoto’s in de officiële {A}-app, boekt daarna een internationale lijn met bestemming Nederland. Winkelwagen, betaling en tickets blijven op kakobuy.com.",
                    "Engelse cataloguskeys (sneakers, hoodie) zijn weergavelabels, geen US-shop.",
                ]),
                ("Welke productfamilies staan erin?", [
                    "Schoenen, hoodies, jassen, tassen en horloges, zolang er QC-hoeken zijn. Elektronica, parfum en andere restricted klassen blijven eraf tenzij de officiële app ze toestaat op de verzenddag.",
                    "Een find van vorige maand kan alsnog restricted worden. Check de officiële productpagina vóór vracht.",
                ]),
                ("Veiliger dan zelf zoeken?", [
                    f"Veiliger betekent magazijnfoto’s vóór internationale vracht — niet dat {customs} verdwijnt. Lees {curl} op de verzenddag. BTW en Collect wijzigen; dit title plakt geen tarief.",
                    "De sheet houdt dode Weidian-links weg. Hij dient geen douaneaangifte in en kiest geen aangegeven waarde.",
                ]),
                ("Voor wie is deze sheet", [
                    f"Voor een eerste adrestest ({city}) en voor wie {A} al gebruikt maar spreadsheet, finds, QC en verzending naar Nederland op één Nederlandse site wil.",
                    "Verzend je naar Duitsland, dan is dit de verkeerde landpagina. Voor douane: {customs}, niet deze URL.",
                ]),
                ("Fouten zonder sheet", [
                    f"Een Duitse postcode in de estimator, {host} als kassa, vracht vóór QC. Last-mile is vaak {post}; Collect kan extra innen.",
                    "Andere fout: een oud BTW-stuk op deze site voor een levend tarief aanzien. Drempels schuiven. Bevestig in de app en bij de Belastingdienst Douane op de verzenddag.",
                ]),
                ("Efficiënt gebruiken", [
                    f"Houd spreadsheet, finds en QC in één tabset. Find geaccepteerd → officieel vrachtformulier naar Nederland, label {city}. Bron: {customs}.",
                    "Geen onderwaardering. Betaal wat de geboekte SKU en de estimator tonen. Bestellingen op kakobuy.com.",
                ]),
                ("Is een spreadsheet verplicht?", [
                    "Nee. Je kunt in de officiële app met de hand zoeken. De sheet bestaat zodat een NL-koper niet elke week bij duizenden dode kaarten begint.",
                    f"Registratie en betaling blijven op kakobuy.com. {host} ziet het account niet.",
                ]),
                ("Klaar om de spreadsheet te gebruiken?", [
                    "Open finds, QC en verzending. Registreer op kakobuy.com. Deze site blijft een index.",
                ]),
            ],
        )
    if kind == "finds":
        return (
            f"{A}-spreadsheet finds voor Nederland op {host}: QC-gecheckte sneakers, hoodies en tassen voor een Nederlands adres, geen tweede wereldcatalogus.",
            [
                ("Wat zijn Kakobuy-finds?", [
                    f"Op {host} zijn het SKU’s die na magazijnfoto’s blijven staan. Het is geen etalage.",
                    "Een find valt af als de bron sterft of het magazijn het stuk niet meer heeft. Prijs 0 is een verwijderde kaart.",
                ]),
                ("Waarom gecureerde finds in Nederland", [
                    f"Handmatig zoeken mengt dode Weidian-links. Gecureerde finds worden nog in China gefotografeerd voordat {post} richting {city} gaat.",
                    "EUR in de app, bestemming Nederland en postcode 1234 AB slaan forum-screenshots zonder Douane-pad.",
                ]),
                ("Populaire categorieën", [
                    "Sneakers en hoodies vullen de muur zolang er QC-hoeken zijn. Tassen en jassen volgen. Restricted blijft eraf.",
                    "Engelse categoriekeys zijn labels, geen US-import.",
                ]),
                ("Hoe finds worden gekozen", [
                    f"Levende bron-URL, minstens één magazijnfoto, estimator-bestemming Nederland — geen Packstation, geen deze hostname als land. Test: {city}.",
                    "Een find blijft niet staan omdat hij vorig seizoen populair was. Falt QC, dan gaat de rij eraf.",
                ]),
                ("Veiliger dan zelf zoeken?", [
                    f"Je leest {customs} ({curl}) nog steeds op de verzenddag. Find betekent alleen: in China gefotografeerd vóór internationale vracht.",
                    "Veiliger is niet btw-vrij. Collect kan nog. Deze pagina verzint geen Douane-euro.",
                ]),
                ("Voor wie", [
                    f"Wie een Nederlandse deur heeft en QC-picks wil. Eerste order het liefst kleding-SKU’s met foto’s.",
                    f"Staat {city} op het label, blijf op deze Nederlandse site.",
                ]),
                ("Finds openen", [
                    "Daarna QC, dan verzending. Registreren op kakobuy.com.",
                ]),
            ],
        )
    if kind == "qc":
        return (
            f"QC op {host} zijn magazijnfoto’s in de officiële {A}-app, in China, vóór je vracht naar Nederland betaalt.",
            [
                ("Wat QC op deze site is", [
                    "Quality check zijn extra hoeken in het magazijn — naden, labels, zool, print. Geen lab, geen Douane-scan.",
                    "Foto’s landen in de officiële app zolang de SKU in China is. Dat is het enige window voor een retake.",
                ]),
                ("Wanneer extra foto’s vragen", [
                    f"Zolang de SKU in het magazijn ligt. Als {post} de doos al heeft, is {customs} het verkeerde loket voor een magazijn-retake.",
                    "Extra hoeken zijn vaak een betaalde add-on in de officiële app. Deze HTML opent geen tickets.",
                ]),
                ("Wat QC niet doet", [
                    f"QC dient geen aangifte in, betaalt geen BTW en verzint geen aangegeven waarde. Bron: {curl}.",
                    "Een schoon QC-album garandeert niet dat de SKU later een platformregel haalt. Check opnieuw vóór je de lijn boekt.",
                ]),
                ("QC en een Nederlands adres", [
                    f"Estimator: Nederland en {city}. Een Duitse postcode is het verkeerde land. Last-mile-noten staan op de verzendpagina.",
                    "Magazijnfoto’s worden hoe dan ook in China gemaakt. Het Nederlandse deel is de deur op het label na QC.",
                ]),
                ("Als een find QC faalt", [
                    "Laat hem in het magazijn of retourneer via de officiële app. Boek geen internationale vracht op een afwijzing.",
                    f"Gefaalde QC is goedkoper in China dan nadat {post} bezorging probeert.",
                ]),
                ("Verzenden na QC?", [
                    f"Pas dan de officiële estimator naar Nederland. {host} neemt geen betaling. EUR-totalen staan in de app.",
                ]),
            ],
        )
    if kind == "shipping":
        return (
            f"{A}-verzending naar Nederland gebruikt de landcode van de estimator (NL), niet dit domein. Open het officiële vrachtformulier na magazijnfoto’s. Last-mile is vaak {post}.",
            [
                ("Hoe Kakobuy-verzending naar Nederland werkt", [
                    f"Magazijn in China → jij accepteert QC → jij boekt een lijn met bestemming Nederland → {post} of de last-mile van de SKU levert. {host} drukt geen live quote.",
                    f"Op het label hoort een echte Nederlandse postcode ({city}). Bevestig bestemming NL in kakobuy.com/tools/estimate op de verzenddag.",
                ]),
                ("Verzendopties voor Nederland", [
                    "Tax-free, prepaid en collect zijn eigenschappen van de geboekte SKU in de officiële app. Collect kan een inklaringsfee toevoegen die de estimator verbergt.",
                    f"{post} kan bij collect handling toevoegen. Lees de SKU, daarna de live estimator — geen screenshot van vorig jaar.",
                ]),
                ("Hoe lang verzending naar Nederland duurt", [
                    "SKU en geboekte lijn bepalen het. Deze pagina verzint geen PostNL-werkdagen.",
                    "Bevestig in de officiële app op de verzenddag. Magazijnverwerking is iets anders dan internationale transit.",
                ]),
                ("Verzendkosten naar Nederland", [
                    f"Je betaalt internationale vracht plus wat de SKU aan de grens zegt. {post} kan bij collect handling toevoegen. In deze title staat geen bedrag omdat het live formulier beweegt.",
                    "EUR is de lokale valuta op deze site. Afrekenen blijft kakobuy.com.",
                ]),
                ("Douane en BTW in Nederland", [
                    f"Lees {customs} ({curl}) op de verzenddag. BTW en drempels schuiven. Gerankte douane-artikelen op deze site zijn lokale notities, geen live tarieftabel.",
                    "Deze HTML coacht geen onderwaardering. Betaal wat de geboekte SKU en de Douane vragen.",
                ]),
                ("Veelgemaakte risico’s", [
                    f"Verkeerd land in de estimator (DE/BE), vracht vóór QC, {city} weglaten. Dat zijn fouten op het NL-pad, geen ‘agent is down’.",
                    "Een restricted SKU die het magazijn haalde, gaat nog steeds niet mee op een NL-lijn als de officiële app submit blokkeert.",
                ]),
                ("Geschikt voor een eerste NL-order?", [
                    f"Ja als {host} de kaart is en kakobuy.com de kassa. Adrestest: {city}. Bron: {customs}.",
                    "Begin met één kleding-SKU, accepteer QC, boek daarna. Consolideer geen stapel zonder foto’s bij de eerste order.",
                ]),
                ("Klaar om naar Nederland te verzenden?", [
                    "Eerst QC, dan officiële estimator naar NL. Bestellingen alleen op kakobuy.com.",
                ]),
            ],
        )
    if kind == "legal":
        return (
            f"{A} is een inkoopagent. {host} legt het NL-pad uit; het is niet de officiële app en niet {customs}. Lees de Belastingdienst Douane op de verzenddag.",
            [
                ("Is Kakobuy legaal in Nederland?", [
                    f"Een inkoopagent gebruiken is in Nederland geen misdrijf. Restricted, platformregels en de geboekte SKU gelden nog. Lees {curl} op de verzenddag.",
                    "Legaal gaat over het agentmodel. Het betekent niet dat elke Taobao-SKU door de Douane mag.",
                ]),
                ("Is Kakobuy veilig te gebruiken?", [
                    "Veilig op deze pagina = magazijn-QC vóór vracht, betaling in de officiële app, echt Nederlands adres — geen belofte dat een doos de Douane overslaat.",
                    f"EUR, bestemming Nederland, {city} op het label. {host} houdt de portemonnee niet vast.",
                ]),
                ("Belangrijkste risico’s in Nederland", [
                    f"Dode bronnen, collect zonder de SKU te lezen, {host} als kassa. {post} kan extra innen.",
                    "Tweede risico: een Duitse postcode plakken omdat de estimator-UI lijkt. Verkeerd land voor deze site.",
                ]),
                ("Risico verlagen", [
                    f"QC in de officiële app, bestemming Nederland, {city} op het label. Geen onderwaardering. Geen verzonnen Douane-euro.",
                    "Houd spreadsheet, finds en QC bij elkaar zodat je geen vracht boekt vanaf de screenshot van een andere landpagina.",
                ]),
                ("Geschikt voor een eerste order?", [
                    f"Ja als je begint met spreadsheet en finds op {host} en daarna officieel registreert. Deze site ziet het account niet.",
                    "Houd restricted van de eerste order af. Kleding-SKU’s met QC-foto’s zijn het gebruikelijke begin.",
                ]),
                ("Oordeel", [
                    f"{A} kan naar Nederland als je de officiële app en {customs} volgt. Deze site blijft informatie. Bestellingen op kakobuy.com.",
                ]),
                ("Starten", [
                    "Spreadsheet → finds → QC → verzending. Alleen betalen op kakobuy.com.",
                ]),
            ],
        )
    if kind == "guide":
        return (
            f"Stappen voor een {A}-bestelling naar een adres in Nederland op {host}. Foto’s in het magazijn, daarna vracht. Geen kassa.",
            [
                ("Hoe kopen via Kakobuy (NL-gids)", [
                    f"Kies een SKU met QC op spreadsheet of finds, dien in via de officiële app, wacht op magazijnfoto’s, boek internationale vracht naar Nederland met {city} op het label.",
                    "Sla QC niet over om een dag te winnen. Nederlandse last-mile maakt geen magazijnfoto over.",
                ]),
                ("Wat Kakobuy is", [
                    f"Een China-inkoopagent. {host} legt alleen het NL-pad in EUR uit. Betalen, tickets en estimator op kakobuy.com.",
                    "Twee betalingen zijn normaal: goederen naar het magazijn, daarna internationale vracht na QC.",
                ]),
                ("Stap 1: product vinden", [
                    "Gebruik spreadsheet en finds op deze Nederlandse site. Sla prijs 0 en restricted over. Engelse categoriekeys zijn labels, geen US-winkel.",
                ]),
                ("Stap 2: bestelling indienen op Kakobuy", [
                    f"Alleen de officiële app. Deze HTML ziet de winkelwagen niet. Registreer op kakobuy.com, niet op {host}.",
                ]),
                ("Stap 3: QC in het magazijn", [
                    "Foto’s vóór vracht. Extra hoeken vaak betaald. Wijs af in de app als het stuk fout is — boek de NL-lijn niet op een fail.",
                ]),
                ("Stap 4: internationale verzending naar Nederland", [
                    f"Estimator-bestemming NL, adres {city}. Lees {customs} ({curl}) op de verzenddag. Geen Duitse postcode.",
                ]),
                ("Stap 5: ontvangen in Nederland", [
                    f"Last-mile vaak {post}. Collect kan extra innen. Tracking leeft in de officiële app.",
                ]),
                ("Tips eerste order", [
                    "Eén eenvoudige kleding-SKU. QC vóór vracht. Altijd bestemming Nederland. Deze pagina coacht geen aangegeven waarde.",
                ]),
                ("Geschikt voor beginners?", [
                    f"Ja als {host} de kaart is en kakobuy.com de kassa. Bron: {customs}.",
                ]),
            ],
        )
    return (
        f"Antwoorden voor kopers in Nederland die de {A}-spreadsheet op {host} gebruiken: QC, verzending, BTW, en of je de sheet nodig hebt.",
        [
            ("Heb ik een Kakobuy-account nodig?", [
                f"Ja, op de officiële {A}-site. {host} maakt geen accounts en reset geen wachtwoord.",
            ]),
            ("Is Kakobuy veilig voor een eerste NL-order?", [
                f"QC-foto’s vóór vracht, bestemming Nederland, {city} op het label. Lees {customs}. Deze pagina coacht geen aangegeven waarde.",
            ]),
            ("Hoe vinden NL-kopers betrouwbare producten?", [
                "Begin met spreadsheet en finds op deze site. Dode Weidian-links vallen af. Check de officiële app vóór je vracht betaalt.",
            ]),
            ("Krijg ik QC-foto’s?", [
                "In de officiële app, in China, vóór internationale vracht. Extra hoeken vaak betaald.",
            ]),
            ("Hoe lang duurt verzending naar Nederland?", [
                f"Hangt van SKU en lijn af. Deze pagina verzint geen {post}-dagen. Bevestig in de officiële estimator.",
            ]),
            ("Betaal ik BTW of invoer in Nederland?", [
                f"De geboekte SKU zegt wie betaalt. Collect kan extra innen. Bron: {customs} ({curl}). Drempels schuiven; we plakken geen tarief.",
            ]),
            ("Spreadsheet of zelf zoeken?", [
                f"De sheet op {host} bestaat zodat NL-kopers geen dode kaarten hoeven te jagen. Het blijft een index, geen Excel. Je mag in de app met de hand zoeken.",
            ]),
            ("Wat kopen mensen meestal?", [
                "Schoenen, hoodies, jassen, tassen — als het magazijn nog QC heeft. Restricted blijft eraf.",
            ]),
            ("Kan ik Kakobuy zonder spreadsheet gebruiken?", [
                "Ja. De spreadsheet is een shortcut, geen poort. Beginners zijn meestal sneller klaar met sheet plus QC-foto’s.",
            ]),
            ("Klaar om te bestellen?", [
                "Open spreadsheet, finds, QC en verzending, registreer daarna op kakobuy.com.",
            ]),
        ],
    )


def wrap_copy(host: str, d: dict, keep_slug: str) -> tuple[str, str, list[tuple[str, list[str]]]]:
    loc = d["loc"]
    keep = f"/{keep_slug}/"
    post, customs = d["post"], d["customs"]
    table = {
        "en": (
            f"{A} shipping to Canada — see the live guide",
            f"This older shipping URL on {host} points to the Canada shipping article. Last-mile notes for {post} and {customs} live on the keep page.",
            [
                ("Live shipping article", [
                    f"The shipping guide for Canadian buyers is {keep}. It covers the official estimator (destination CA), {post}, CBSA and a postal-code test — without inventing a transit day or a duty rate.",
                    f"Use {keep} as the page to read and share. Orders stay on kakobuy.com.",
                ]),
            ],
        ),
        "fi": (
            f"{A} toimitus Suomeen — katso ajantasainen opas",
            f"Tämä vanhempi toimitus-URL sivustolla {host} ohjaa Suomen toimitusartikkeliin. {post} ja {customs} ovat keep-sivulla.",
            [
                ("Ajantasainen toimitussivu", [
                    f"Suomalaisen ostajan toimitusopas on {keep}. Siinä on virallinen arvioija (kohde FI), {post}, Tulli ja postinumerotesti — ilman keksittyjä päiviä tai tarifia.",
                    f"Lue ja jaa sivu {keep}. Tilaukset kakobuy.comissa.",
                ]),
            ],
        ),
        "es": (
            f"Envío {A} a España — ver la guía actual",
            f"Esta URL antigua de envío en {host} apunta al artículo de envío a España. {post} y {customs} están en la página keep.",
            [
                ("Artículo de envío en vigor", [
                    f"La guía de envío para España es {keep}. Incluye el estimador oficial (destino ES), {post}, Agencia Tributaria y el test de CP — sin inventar plazos ni aranceles.",
                    f"Lee y comparte {keep}. Pedidos en kakobuy.com.",
                ]),
            ],
        ),
        "fr": (
            f"Livraison {A} France — voir le guide à jour",
            f"Cette ancienne URL livraison sur {host} pointe vers l’article livraison France. {post} et {customs} sont sur la page keep.",
            [
                ("Article livraison à jour", [
                    f"Le guide livraison pour la France est {keep}. Estimateur officiel (destination FR), {post}, douane et test de CP — sans inventer un délai ou un tarif.",
                    f"Lis et partage {keep}. Commandes sur kakobuy.com.",
                ]),
            ],
        ),
        "nl": (
            f"{A}-verzending Nederland — bekijk de actuele gids",
            f"Deze oudere verzend-URL op {host} wijst naar het NL-verzendartikel. {post} en {customs} staan op de keep-pagina.",
            [
                ("Actuele verzendpagina", [
                    f"De verzendgids voor Nederland is {keep}. Officiële estimator (bestemming NL), {post}, Douane en postcodetest — zonder verzonnen dagen of tarieven.",
                    f"Lees en deel {keep}. Bestellingen op kakobuy.com.",
                ]),
            ],
        ),
    }
    return table[loc]
