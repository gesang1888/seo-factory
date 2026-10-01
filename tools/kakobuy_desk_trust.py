"""Localized About + homepage editorial for Kakobuy country desks.

Teal Inter chrome — not HipoBuy green, not LitBuy yellow, not SugarGoo orange.
Warehouse clock: confirm official Help; public copies quote 100 or 180 days.
No Spain line-count copy, no under-declaration, invite/coupon off titles.
US brand notes stay on kakobuytips.com — this cluster does not take US.
"""
from __future__ import annotations

CAT_WALL = [
    ("sneakers", "sneakers.jpg"),
    ("t-shirt", "t-shirt.jpg"),
    ("hoodie", "hoodie.jpg"),
    ("jacket", "jacket.jpg"),
    ("jeans", "jeans.jpg"),
    ("shorts", "shorts.jpg"),
    ("underwear", "underwear.jpg"),
    ("jersey", "jersey.jpg"),
    ("hats", "hats.jpg"),
    ("bags", "bags.jpg"),
    ("eyewear", "eyewear.jpg"),
    ("headphones", "headphones.jpg"),
    ("perfume", "perfume.jpg"),
    ("watches", "watches.jpg"),
    ("jewelry", "jewelry.jpg"),
    ("toys", "toys.jpg"),
]

CAT_LABELS = {
    "en": {
        "sneakers": "Sneakers",
        "t-shirt": "T-shirts",
        "hoodie": "Hoodies",
        "jacket": "Jackets",
        "jeans": "Jeans",
        "shorts": "Shorts",
        "underwear": "Underwear",
        "jersey": "Jerseys",
        "hats": "Hats",
        "bags": "Bags",
        "eyewear": "Eyewear",
        "headphones": "Headphones",
        "perfume": "Perfume",
        "watches": "Watches",
        "jewelry": "Jewelry",
        "toys": "Toys",
    },
    "es": {
        "sneakers": "Zapatillas",
        "t-shirt": "Camisetas",
        "hoodie": "Sudaderas",
        "jacket": "Chaquetas",
        "jeans": "Vaqueros",
        "shorts": "Pantalones cortos",
        "underwear": "Ropa interior",
        "jersey": "Camisetas de equipo",
        "hats": "Gorras y gorros",
        "bags": "Bolsos y mochilas",
        "eyewear": "Gafas",
        "headphones": "Auriculares",
        "perfume": "Perfumes",
        "watches": "Relojes",
        "jewelry": "Joyería",
        "toys": "Juguetes de diseño",
    },
    "fr": {
        "sneakers": "Baskets",
        "t-shirt": "T-shirts",
        "hoodie": "Sweats",
        "jacket": "Vestes",
        "jeans": "Jeans",
        "shorts": "Shorts",
        "underwear": "Sous-vêtements",
        "jersey": "Maillots",
        "hats": "Casquettes",
        "bags": "Sacs",
        "eyewear": "Lunettes",
        "headphones": "Casques",
        "perfume": "Parfums",
        "watches": "Montres",
        "jewelry": "Bijoux",
        "toys": "Figurines",
    },
    "nl": {
        "sneakers": "Sneakers",
        "t-shirt": "T-shirts",
        "hoodie": "Hoodies",
        "jacket": "Jassen",
        "jeans": "Jeans",
        "shorts": "Shorts",
        "underwear": "Ondergoed",
        "jersey": "Shirts",
        "hats": "Petten",
        "bags": "Tassen",
        "eyewear": "Brillen",
        "headphones": "Koptelefoons",
        "perfume": "Parfum",
        "watches": "Horloges",
        "jewelry": "Sieraden",
        "toys": "Designspeelgoed",
    },
    "fi": {
        "sneakers": "Lenkkarit",
        "t-shirt": "T-paidat",
        "hoodie": "Hupparit",
        "jacket": "Takit",
        "jeans": "Farkut",
        "shorts": "Shortsit",
        "underwear": "Alusvaatteet",
        "jersey": "Pelipaidat",
        "hats": "Hatut",
        "bags": "Laukut",
        "eyewear": "Silmälasit",
        "headphones": "Kuulokkeet",
        "perfume": "Tuoksut",
        "watches": "Kellot",
        "jewelry": "Korut",
        "toys": "Figuurit",
    },
}


def loc(key: str) -> str:
    return {"es": "es", "fr": "fr", "nl": "nl", "fi": "fi"}.get(key, "en")


def pack(key: str, d: dict) -> dict:
    host = d["host"]
    dest = d["dest_label"]
    locl = d["locale"]
    mail = d["mail"]
    L = loc(key)

    if L == "es":
        return {
            "agent_h": "Un agente de compras es un intermediario, no una tienda",
            "agent_lead": (
                f"Kakobuy no vende el producto. Compra por ti en tiendas chinas que no envían "
                f"al extranjero, lo fotografía en el almacén y después tú eliges la línea hacia {dest}."
            ),
            "agent_p": (
                "Pagas dos veces (mercancía más doméstico en China, después el flete internacional) "
                f"y puedes agrupar entre medias. {host} es un desk independiente, no kakobuy.com. "
                "No copiamos un recuento de líneas de otro agente ni un cupón de Finlandia."
            ),
            "agent_btn": "Ver el catálogo de esta portada",
            "agent_cap": (
                "Inicio oficial kakobuy.com. Captura propia del 1 oct 2026. El estimador es un SPA: "
                "el HTML crudo era poco; el navegador sí renderizó la portada."
            ),
            "sheet_h": "Un spreadsheet no es una hoja de Excel",
            "sheet_lead": (
                "Aquí «spreadsheet» es un catálogo de fichas con foto, marca, precio de referencia "
                "y el enlace que el agente puede abrir — no un .xlsx de filas."
            ),
            "sheet_p": (
                "El índice de esta portada es inglés (sneakers, hoodie, jacket). «Zapatillas» suele "
                "devolver cero; sneakers llena la rejilla. Las finds completas siguen en w2clinks. "
                "El artículo /envio-kakobuy-espana/ se conserva."
            ),
            "sheet_btn": "Abrir el catálogo",
            "wall_h": "Dieciséis categorías para el primer pedido",
            "wall_lead": (
                "Cada tarjeta abre la clave inglesa en el catálogo de esta portada. Empieza por una: "
                "mezclar cinco categorías encarece el carton hacia España."
            ),
            "rest_h": "Muchas fichas no se pueden comprar aunque aparezcan",
            "rest_lead": (
                "Restricted o precio 0 no es un fallo de esta portada: el enlace de origen no admite "
                "compra por agente, o no se leyó el precio."
            ),
            "rest_p": (
                "Tabaco, alcohol y medicamentos suelen rechazarse — la lista vive en la ayuda oficial. "
                "Sin infradeclaración. El recuento de líneas de otro agente no se pega aquí."
            ),
            "rest_btn": "Ayuda de este desk",
            "rest_cap": (
                "Help Center oficial de Kakobuy. Captura 1 oct 2026. El reloj de almacén se confirma "
                "allí: copias públicas citan 100 o 180 días — este desk no elige un número."
            ),
            "shots_h": "Superficie oficial, con fecha",
            "shots_lead": (
                "kakobuy.com/tools/estimate es un SPA. El 1 oct 2026 el navegador renderizó el "
                "formulario. Destino de este desk: España, no este TLD."
            ),
            "shot_est_cap": (
                f"Estimador oficial. Captura 1 oct 2026. Destino {dest}. Los importes salen al pulsar "
                "Estimate — no los copiamos. No hay un recuento de 58 líneas ajenas."
            ),
            "about_nav": "Sobre",
            "about_title": f"Quiénes somos: desk independiente de Kakobuy en {locl}",
            "about_desc": (
                f"{host} es un desk editorial independiente para una dirección en España. Lab 1 oct 2026."
            ),
            "about_h1": f"Quiénes somos: desk independiente de Kakobuy en <em>{locl}</em>",
            "about_lead": (
                f"<strong>{host} no es Kakobuy.</strong> Desk editorial: catálogo, laboratorio de envío, "
                "ayuda y novedades. No almacenamos, no cobramos flete, no vemos cuentas."
            ),
            "how_h": "Cómo trabajamos",
            "src_h": "Fuentes",
            "src_p": (
                "Flete: estimador público kakobuy.com/tools/estimate, con fecha. Aduana: Agencia "
                "Tributaria, enlazada en /envio-kakobuy-espana/. Lo no comprobado no se afirma."
            ),
            "why_h": "Por qué hay pocos euros en el texto",
            "why_p": (
                "Las líneas cambian cada semana. Un recuento copiado de otro agente estaría mal mañana. "
                "Por eso el estimador oficial más una captura con fecha."
            ),
            "inv_h": "Códigos",
            "inv_p": (
                "Los cupones y el invite viven en /kakobuy-coupon/ y /kakobuy-coupons/ de este host. "
                "Esta portada no pone códigos en el título. Puedes entrar en kakobuy.com sin ellos."
            ),
            "not_h": "Lo que no somos",
            "not_p": (
                "Ni tienda, ni almacén, ni cola de tickets. Reclamaciones solo en kakobuy.com. No "
                "hacemos 301 de este ccTLD hacia kakobuydocs.com ni hacia Finlandia o Canadá."
            ),
            "co_h": "Contacto",
            "co_p": (
                f"Si se rompe una columna del laboratorio, lo datamos en Novedades. Redacción: {mail}."
            ),
            "legal": (
                "No inventamos un recuento de líneas ni un valor declarado. Reloj de almacén: confirmar "
                "Help Center oficial (copias públicas 100 o 180 días). Sin infradeclaración."
            ),
        }

    if L == "fr":
        return {
            "agent_h": "Un agent d’achat est un intermédiaire, pas une boutique",
            "agent_lead": (
                f"Kakobuy ne vend pas la marchandise. Il achète dans des boutiques chinoises qui "
                f"n’expédient pas à l’étranger, photographie à l’entrepôt, puis tu livres vers {dest}."
            ),
            "agent_p": (
                "Deux paiements, un entrepôt au milieu. Ce host est un desk indépendant, pas "
                "kakobuy.com. Destination France, pas la Belgique, pas kakospreadsheet.es."
            ),
            "agent_btn": "Voir le catalogue de cette accueil",
            "agent_cap": (
                "Accueil officiel kakobuy.com. Capture du 1 oct. 2026. SPA rendu dans le navigateur, "
                "pas une coquille HTML."
            ),
            "sheet_h": "Un spreadsheet n’est pas un fichier Excel",
            "sheet_lead": (
                "Ici, « spreadsheet » est un catalogue de fiches (photo, marque, prix, lien agent), "
                "pas un tableau de lignes."
            ),
            "sheet_p": (
                "L’index est anglais (sneakers, hoodie, jacket). « Baskets » renvoie souvent zéro. "
                "Les articles /livraison-kakobuy/ et /kakobuy-france/ restent."
            ),
            "sheet_btn": "Ouvrir le catalogue",
            "wall_h": "Seize catégories pour le premier colis",
            "wall_lead": (
                "Chaque tuile ouvre la clé anglaise. Une seule catégorie au premier envoi vers la France."
            ),
            "rest_h": "Beaucoup de fiches ne s’achètent pas",
            "rest_lead": (
                "Restricted ou prix 0 : le lien source n’est pas achetable par l’agent, ou le prix n’a pas été lu."
            ),
            "rest_p": (
                "Tabac, alcool, médicaments : aide officielle, on n’invente pas la liste. Pas de sous-déclaration."
            ),
            "rest_btn": "Aide de ce desk",
            "rest_cap": (
                "Help Center Kakobuy. Capture 1 oct. 2026. Horloge d’entrepôt à confirmer là-bas "
                "(copies publiques : 100 ou 180 jours)."
            ),
            "shots_h": "Interface officielle, avec date",
            "shots_lead": (
                "kakobuy.com/tools/estimate est un SPA. Le 1 oct. 2026 le formulaire a rendu. Destination France."
            ),
            "shot_est_cap": (
                f"Estimateur officiel. Capture 1 oct. 2026. Destination {dest}, pas un code postal belge."
            ),
            "about_nav": "À propos",
            "about_title": "À propos : desk indépendant Kakobuy pour la France",
            "about_desc": f"{host} est un desk éditorial pour une adresse en France. Lab 1 oct. 2026. Pas la Belgique.",
            "about_h1": "À propos : desk indépendant Kakobuy pour la <em>France</em>",
            "about_lead": (
                f"<strong>{host} n’est pas Kakobuy.</strong> Catalogue, labo fret, aide, actualités. "
                "On n’encaisse pas le port."
            ),
            "how_h": "Comment on travaille",
            "src_h": "Sources",
            "src_p": (
                "Fret : kakobuy.com/tools/estimate, daté. Douane : douane.gouv.fr via /livraison-kakobuy/. "
                "Ce qui n’est pas mesuré n’est pas écrit."
            ),
            "why_h": "Pourquoi si peu d’euros",
            "why_p": "Les SKU bougent. Un tableau copié d’Espagne serait faux demain.",
            "inv_h": "Codes",
            "inv_p": (
                "Coupons sur /kakobuy-coupon/ de cet hôte. Cette accueil ne met pas de code dans le titre."
            ),
            "not_h": "Ce que nous ne sommes pas",
            "not_p": (
                "Ni boutique ni file de tickets. Pas de 301 vers kakobuydocs.com, l’Espagne ou la Finlande."
            ),
            "co_h": "Contact",
            "co_p": f"Labo cassé : on le date dans Actualités. Rédaction : {mail}.",
            "legal": (
                "Pas de valeur déclarée inventée. Stockage : confirmer l’aide officielle (copies 100 ou 180 jours)."
            ),
        }

    if L == "nl":
        return {
            "agent_h": "Een inkoopagent is een tussenpersoon, geen winkel",
            "agent_lead": (
                f"Kakobuy verkoopt de spullen niet. Het koopt in Chinese shops, fotografeert in het "
                f"magazijn, daarna boek jij de lijn naar {dest}."
            ),
            "agent_p": (
                f"Twee betalingen, bundelen tussendoor. {host} is een onafhankelijke desk. "
                "Bestemming Nederland met Nederlandse postcode, geen Duits afhaalautomaat-nummer."
            ),
            "agent_btn": "Catalogus op deze homepage",
            "agent_cap": "Officiële homepage kakobuy.com. Eigen opname 1 okt 2026. SPA gerenderd in de browser.",
            "sheet_h": "Een spreadsheet is geen Excel-bestand",
            "sheet_lead": "Kaarten met foto, merk, referentieprijs en de link die de agent opent — geen rijenbestand.",
            "sheet_p": (
                "Index Engels (sneakers, hoodie, jacket). /kakobuy-verzending/ en /kakobuy-ervaringen/ blijven."
            ),
            "sheet_btn": "Catalogus openen",
            "wall_h": "Zestien categorieën voor het eerste pakket",
            "wall_lead": "Begin met één Engelse sleutel. Vijf categorieën maken NL-vracht duur.",
            "rest_h": "Veel listings zijn niet koopbaar",
            "rest_lead": "Restricted of prijs 0: bronlink niet koopbaar via de agent.",
            "rest_p": "Tabak, alcohol, medicijnen: officiële help. Geen onderwaardering.",
            "rest_btn": "Hulp van deze desk",
            "rest_cap": (
                "Kakobuy Help Center. Opname 1 okt 2026. Opslagklok daar bevestigen (kopieën: 100 of 180 dagen)."
            ),
            "shots_h": "Officiële interface, met datum",
            "shots_lead": "kakobuy.com/tools/estimate is een SPA. 1 okt 2026 renderde het formulier. Bestemming Nederland.",
            "shot_est_cap": f"Officiële estimator. Opname 1 okt 2026. Bestemming {dest}.",
            "about_nav": "Over ons",
            "about_title": "Over ons: onafhankelijke Kakobuy-desk voor Nederland",
            "about_desc": f"{host} is een redactionele desk voor een Nederlands adres. Lab 1 okt 2026.",
            "about_h1": "Over ons: onafhankelijke Kakobuy-desk voor <em>Nederland</em>",
            "about_lead": f"<strong>{host} is niet Kakobuy.</strong> Catalogus, vrachtlab, hulp, nieuws.",
            "how_h": "Hoe we werken",
            "src_h": "Bronnen",
            "src_p": "Vracht: kakobuy.com/tools/estimate. Douane: Belastingdienst via /kakobuy-verzending/.",
            "why_h": "Waarom weinig eurobedragen",
            "why_p": "SKU’s wijzigen wekelijks. Geen gekopieerde ES-lijnentelling.",
            "inv_h": "Codes",
            "inv_p": "Coupons op /kakobuy-coupon/ van deze host. Niet in deze titel.",
            "not_h": "Wat we niet zijn",
            "not_p": "Geen shop, geen 301 naar docs, Finland of Spanje.",
            "co_h": "Contact",
            "co_p": f"Lab stuk: dateren in Nieuws. Redactie: {mail}.",
            "legal": "Geen verzonnen aangegeven waarde. Opslag: officiële Help (kopieën 100 of 180 dagen).",
        }

    if L == "fi":
        return {
            "agent_h": "Ostoagentti on välikäsi, ei kauppa",
            "agent_lead": (
                f"Kakobuy ei myy tuotetta. Se ostaa kiinalaisista kaupoista, jotka eivät lähetä "
                f"ulkomaille, kuvaa varastossa, sitten valitset linjan kohti {dest}."
            ),
            "agent_p": (
                f"Maksat kahdesti ja voit yhdistää välissä. {host} on riippumaton desk, ei kakobuy.com. "
                "Kohde Suomi (FI), ei EU, ei Ruotsi. Viisinumeroinen postinumero kuten 00100 Helsinki."
            ),
            "agent_btn": "Katso tämän etusivun katalogi",
            "agent_cap": (
                "Virallinen kakobuy.com. Oma kuvakaappaus 1. loka 2026. SPA renderöityi selaimessa."
            ),
            "sheet_h": "Spreadsheet ei ole Excel-tiedosto",
            "sheet_lead": (
                "Tässä «spreadsheet» on korttikatalogi (kuva, merkki, viitehinta, agenttilinkki), ei rivitiedosto."
            ),
            "sheet_p": (
                "Indeksi on englanti (sneakers, hoodie, jacket). «Lenkkarit» antaa usein nollan. "
                "/kakobuy-toimitus/, /kakobuy-kokemuksia/ ja /kakobuy-suomi/ säilyvät."
            ),
            "sheet_btn": "Avaa katalogi",
            "wall_h": "Kuusitoista kategoriaa ensimmäiseen tilaukseen",
            "wall_lead": "Aloita yhdellä englanninkielisellä avaimella. Viisi kategoriaa tekee FI-rahdin kalliiksi.",
            "rest_h": "Monia kortteja ei voi ostaa, vaikka ne näkyvät",
            "rest_lead": "Restricted tai hinta 0: lähdelinkki ei ole agenttiostettavissa.",
            "rest_p": (
                "Tupakka, alkoholi, lääkkeet: virallinen ohje. Ei aliarvostusta. Tämä ei ole "
                "saksalainen automaattinumero."
            ),
            "rest_btn": "Tämän deskin ohje",
            "rest_cap": (
                "Kakobuyn Help Center. Kuvakaappaus 1. loka 2026. Varastokello vahvistetaan siellä: "
                "julkiset kopiot mainitsevat 100 tai 180 päivää — tämä desk ei valitse lukua."
            ),
            "shots_h": "Virallinen pinta, päivämäärällä",
            "shots_lead": (
                "kakobuy.com/tools/estimate on SPA. 1. loka 2026 selain renderöi lomakkeen. Kohde Suomi, ei SE."
            ),
            "shot_est_cap": (
                f"Virallinen arvioija. Kuvakaappaus 1. loka 2026. Kohde {dest}, postinumero kuten 00100 Helsinki."
            ),
            "about_nav": "Meistä",
            "about_title": "Meistä: riippumaton Kakobuy-desk Suomelle",
            "about_desc": f"{host} on toimituksellinen desk suomalaiselle osoitteelle. Lab 1. loka 2026. Tulli: tulli.fi.",
            "about_h1": "Meistä: riippumaton Kakobuy-desk <em>Suomelle</em>",
            "about_lead": (
                f"<strong>{host} ei ole Kakobuy.</strong> Katalogi, rahtilaboratorio, ohje, uutiset. "
                "Emme varastoi emmekä kassaa."
            ),
            "how_h": "Miten työskentelemme",
            "src_h": "Lähteet",
            "src_p": (
                "Rahti: kakobuy.com/tools/estimate, päivätty. Tulli: tulli.fi rankkaavan /kakobuy-toimitus/-artikkelin kautta. "
                "Mittaamatonta ei kirjoiteta."
            ),
            "why_h": "Miksi tekstissä on vähän euroja",
            "why_p": "SKU:t vaihtuvat viikoittain. Toisen agentin Espanja-rivimäärää ei kopioida Suomeen.",
            "inv_h": "Koodit",
            "inv_p": "Kupongit ovat /kakobuy-coupon/ tällä hostilla. Tätä otsikkoa ne eivät täytä.",
            "not_h": "Mitä emme ole",
            "not_p": (
                "Emme ole kauppa emmekä tikettijono. Ei 301:tä kakobuydocs.comiin, Espanjaan tai Kanadaan."
            ),
            "co_h": "Yhteystiedot",
            "co_p": f"Jos laboratorio hajoaa, päiväämme sen Uutisissa. Toimitus: {mail}.",
            "legal": (
                "Emme keksi ilmoitettua arvoa. Varasto: vahvista virallinen Help (julkiset kopiot 100 tai 180 päivää). "
                "Lähde: Tulli."
            ),
        }

    return {
        "agent_h": "A purchasing agent is an intermediary, not a shop",
        "agent_lead": (
            f"Kakobuy does not sell the goods. It buys from Chinese third-party shops that will not "
            f"ship abroad, photographs the parcel in its warehouse, then you book an international SKU to {dest}."
        ),
        "agent_p": (
            f"You pay twice and can consolidate in between. {host} is an independent desk, not kakobuy.com. "
            "US Kakobuy notes stay on kakobuytips.com — this cluster does not take the United States. "
            "A US ZIP in the estimator is the wrong country for this host."
        ),
        "agent_btn": "Open the catalogue on this homepage",
        "agent_cap": (
            "Official kakobuy.com home. Own capture 1 Oct 2026. The public site is a SPA: raw HTML was thin; "
            "the browser rendered the chrome."
        ),
        "sheet_h": "A spreadsheet is not an Excel file",
        "sheet_lead": (
            "Here «spreadsheet» means a card catalogue — photo, brand, reference price and the link the "
            "agent can open — not a grid of rows."
        ),
        "sheet_p": (
            "The index on this homepage is English (sneakers, hoodie, jacket). Local words often return "
            "zero cards. Ranked URLs /kakobuy-shipping-to-canada/ and /kakobuy-canada/ stay."
        ),
        "sheet_btn": "Open the catalogue",
        "wall_h": "Sixteen categories for the first order",
        "wall_lead": (
            "Each tile opens the English key on this homepage catalogue. Start with one: mixing five "
            "categories is the fastest way to an expensive carton into Canada."
        ),
        "rest_h": "Many cards cannot be bought even when they appear",
        "rest_lead": (
            "Restricted or price 0 is not a shop error on this host: the source link is not purchasable "
            "by the agent, or the price could not be read."
        ),
        "rest_p": (
            "Tobacco, alcohol and medicines are usually refused — that list lives in official Help. "
            "No declared-value coaching. GST/HST articles already ranking stay; we do not copy a rate into this title."
        ),
        "rest_btn": "Help on this desk",
        "rest_cap": (
            "Official Kakobuy Help Center. Capture 1 Oct 2026. Storage clock is confirmed there: public "
            "copies quote 100 days from in-storage and 180 days. This desk does not pick a number."
        ),
        "shots_h": "Official surface, with a date",
        "shots_lead": (
            "kakobuy.com/tools/estimate is a SPA. On 1 Oct 2026 the browser rendered the form. "
            "Destination for this desk: Canada, not this TLD and not the United States."
        ),
        "shot_est_cap": (
            f"Official freight estimate. Capture 1 Oct 2026. Destination {dest}. Live money appears after "
            "you run Estimate — we do not paste another agent’s line count here."
        ),
        "about_nav": "About",
        "about_title": f"Who we are: independent Kakobuy desk for {locl}",
        "about_desc": (
            f"{host} is an independent editorial desk for a Canadian delivery address. Lab 1 Oct 2026. CBSA."
        ),
        "about_h1": f"Who we are: independent Kakobuy desk for <em>{locl}</em>",
        "about_lead": (
            f"<strong>{host} is not Kakobuy.</strong> Editorial desk: catalogue, freight lab, help and news. "
            "We do not store goods, take freight, or see accounts."
        ),
        "how_h": "How we work",
        "src_h": "Sources",
        "src_p": (
            "Freight: public estimator kakobuy.com/tools/estimate, dated. Customs: CBSA via the ranked "
            "shipping-to-Canada article. What we have not measured is not claimed."
        ),
        "why_h": "Why so few dollar figures in the copy",
        "why_p": (
            "Lines move every week. A Spain line-count from another agent would be wrong tomorrow. "
            "Hence the official estimator plus a dated screenshot."
        ),
        "inv_h": "Codes",
        "inv_p": (
            "Coupons live on /kakobuy-coupon/ on this host. This homepage does not put codes in the title. "
            "You can open kakobuy.com without them."
        ),
        "not_h": "What we are not",
        "not_p": (
            "Not a shop, warehouse or ticket queue. Claims only on kakobuy.com. We do not 301 this ccTLD "
            "onto kakobuydocs.com, Spain or Finland. kakobuytips.com is the US alias, not this desk."
        ),
        "co_h": "Contact",
        "co_p": (
            f"If a lab column or a ranked URL breaks, we date it on News. Editorial: {mail}."
        ),
        "legal": (
            "We do not invent a declared value or a de-minimis dollar for Canada. Storage: confirm official "
            "Help (public copies quote 100 or 180 days). Source: CBSA."
        ),
    }
