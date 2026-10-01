"""Localized About + homepage editorial for LitBuy country desks.

HipoBuy.es-style blocks, LitBuy facts. Yellow/dach/US chrome — not HipoBuy green,
not Georgia memos. No Spain line-count copy, no under-declaration, invite/coupon
off titles. Warehouse: 90 free days from stocked/listed, 120-day max.
"""
from __future__ import annotations

# English catalogue keys (small label on each tile) + local display name.
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
    "de": {
        "sneakers": "Sneaker",
        "t-shirt": "T-Shirts",
        "hoodie": "Hoodies",
        "jacket": "Jacken",
        "jeans": "Jeans",
        "shorts": "Shorts",
        "underwear": "Unterwäsche",
        "jersey": "Trikots",
        "hats": "Caps",
        "bags": "Taschen",
        "eyewear": "Brillen",
        "headphones": "Kopfhörer",
        "perfume": "Parfum",
        "watches": "Uhren",
        "jewelry": "Schmuck",
        "toys": "Design-Spielzeug",
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
    "it": {
        "sneakers": "Sneakers",
        "t-shirt": "Magliette",
        "hoodie": "Felpe",
        "jacket": "Giacche",
        "jeans": "Jeans",
        "shorts": "Shorts",
        "underwear": "Intimo",
        "jersey": "Maglie",
        "hats": "Cappelli",
        "bags": "Borse",
        "eyewear": "Occhiali",
        "headphones": "Cuffie",
        "perfume": "Profumi",
        "watches": "Orologi",
        "jewelry": "Gioielli",
        "toys": "Giocattoli",
    },
}


def loc(key: str) -> str:
    if key == "es":
        return "es"
    if key == "fr":
        return "fr"
    if key == "at":
        return "de"
    if key == "nl":
        return "nl"
    if key == "it":
        return "it"
    return "en"


def pack(key: str, d: dict) -> dict:
    """All homepage prose + About meta for one desk. Invite/coupon never in titles."""
    host = d["host"]
    dest = d["dest_label"]
    locl = d["locale"]
    mail = d["mail"]
    L = loc(key)

    if L == "es":
        p = {
            "agent_h": "Un agente de compras es un intermediario, no una tienda",
            "agent_lead": (
                f"LitBuy no vende el producto. Compra por ti en tiendas chinas que no envían "
                f"al extranjero, lo fotografía en el almacén, lo guarda y después tú eliges la "
                f"línea internacional hacia {dest}."
            ),
            "agent_p": (
                "Esa diferencia lo cambia todo: pagas dos veces (primero la mercancía más el "
                "doméstico en China, después el flete internacional), esperas dos veces y tienes "
                "un punto intermedio para juntar pedidos o cambiar de SKU. Este host es un desk "
                f"independiente en {host}, no el sitio oficial."
            ),
            "agent_btn": "Ver el catálogo de esta portada",
            "agent_cap": (
                "Inicio oficial litbuy.com. Captura propia del 1 oct 2026. El HTML vacío de "
                "un SPA ya no: la portada renderizó. Why Choose muestra 120-Day Storage."
            ),
            "sheet_h": "Un spreadsheet no es una hoja de Excel",
            "sheet_lead": (
                "Aquí «spreadsheet» no es una tabla de filas y columnas: es un catálogo de fichas "
                "con foto, marca, precio de referencia y el enlace que el agente puede abrir."
            ),
            "sheet_p": (
                "En esta portada el índice es inglés (sneakers, hoodie, jacket). «Zapatillas» suele "
                "devolver cero tarjetas; sneakers llena la rejilla. Las miles de finds completas "
                "siguen en w2clinks — este desk no las copia a un .xlsx."
            ),
            "sheet_btn": "Abrir el catálogo",
            "wall_h": "Dieciséis categorías para no perderte el primer día",
            "wall_lead": (
                "Cada tarjeta abre la clave inglesa en el catálogo de esta portada. Empieza por "
                "una sola: mezclar cinco categorías en el primer pedido es la forma más rápida "
                "de un paquete caro y difícil de encajar."
            ),
            "rest_h": "Muchos productos no se pueden comprar aunque aparezcan",
            "rest_lead": (
                "En el sitio oficial verás fichas «Restricted item» o con precio a cero. No es un "
                "fallo: el enlace de origen no está disponible para el agente o no se pudo leer el precio."
            ),
            "rest_p": (
                "Si la ficha no muestra precio y opciones reales, no cuentes con ella. Tabaco, "
                "alcohol y medicamentos suelen rechazarse — la lista vive en la ayuda oficial, "
                "no la inventamos aquí. Sin infradeclaración."
            ),
            "rest_btn": "Ayuda de este desk",
            "rest_cap": (
                "Help Center oficial. Captura propia del 1 oct 2026. Storage Period (90 días gratis) "
                "y Prohibited Items están ahí — no copiamos una tabla de otro agente."
            ),
            "shots_h": "Superficie oficial, con fecha",
            "shots_lead": (
                "El estimador de LitBuy era un cascarón SPA (~2 KB) si solo mirabas el HTML. "
                "El 1 oct 2026 el navegador sí renderizó el formulario. No pegamos las 58 líneas "
                "de España de otro agente."
            ),
            "shot_est_cap": (
                f"Freight estimate oficial. Captura propia del 1 oct 2026. Destino de este desk: "
                f"{dest}. Los importes del día salen al pulsar Estimate — no los copiamos aquí."
            ),
            "about_nav": "Sobre",
            "about_title": f"Quiénes somos: desk independiente de LitBuy en {locl}",
            "about_desc": (
                f"{host} es un desk editorial independiente. No hacemos pedidos ni vemos tu cuenta. "
                "Lab 1 oct 2026."
            ),
            "about_h1": f"Quiénes somos: desk independiente de LitBuy en <em>{locl}</em>",
            "about_lead": (
                f"<strong>{host} no es LitBuy.</strong> Es un desk editorial: catálogo, laboratorio "
                "de envío, ayuda y novedades. No almacenamos mercancía, no cobramos flete, no vemos cuentas."
            ),
            "how_h": "Cómo trabajamos",
            "src_h": "Fuentes",
            "src_p": (
                "Flete: estimador público en litbuy.com/shipping-estimate, con fecha. Aduana: "
                "fuentes oficiales del país de destino, enlazadas en los artículos que ya rankean. "
                "Lo que no hemos comprobado no se afirma."
            ),
            "why_h": "Por qué hay pocos euros en el texto",
            "why_p": (
                "Las tarifas cambian cada semana. Un número copiado aquí estaría mal mañana. Por eso "
                "el estimador oficial más una captura con fecha, no una tabla inventada."
            ),
            "inv_h": "Invite",
            "inv_p": (
                "El botón Register puede llevar un código de afiliado. Puede haber comisión, sin recargo "
                "para ti. Puedes entrar en litbuy.com sin código. Los hechos incómodos (catálogo en "
                "inglés, el conmutador de moneda que no convierte) se quedan publicados."
            ),
            "not_h": "Lo que no somos",
            "not_p": (
                "Ni tienda, ni almacén, ni cola de tickets. Reclamaciones solo en litbuy.com. No "
                "hacemos 301 de este TLD hacia otro host del mismo agente ni hacia un hub."
            ),
            "co_h": "Contacto",
            "co_p": (
                f"Si se rompe una columna del laboratorio o un enlace, lo datamos en Novedades. No "
                f"reescribimos en silencio. Este desk no responde tickets de pedido. Redacción: {mail}."
            ),
            "legal": (
                "No inventamos nombres de sociedad ni tipos de aduana. El pie y la ayuda oficiales "
                "son la fuente. Almacén: 90 días gratis desde stocked/listed, tope 120 "
                "(Help Center oficial, 1 oct 2026). Sin infradeclaración."
            ),
        }
        return p

    if L == "fr":
        p = {
            "agent_h": "Un agent d’achat est un intermédiaire, pas une boutique",
            "agent_lead": (
                f"LitBuy ne vend pas la marchandise. Il achète pour toi dans des boutiques chinoises "
                f"qui n’expédient pas à l’étranger, photographie à l’entrepôt, stocke, puis tu livres "
                f"vers {dest}."
            ),
            "agent_p": (
                "Ça change tout : tu paies deux fois (marchandise + domestique Chine, puis la ligne "
                "internationale), tu attends deux fois, et tu peux regrouper ou changer de SKU entre "
                f"les deux. Ce host {host} est un desk indépendant, pas le site officiel. Destination "
                "France, pas la Belgique."
            ),
            "agent_btn": "Voir le catalogue de cette accueil",
            "agent_cap": (
                "Accueil officiel litbuy.com. Capture du 1 oct. 2026. Plus une coquille SPA : "
                "la page a rendu. Why Choose affiche 120-Day Storage."
            ),
            "sheet_h": "Un spreadsheet n’est pas un fichier Excel",
            "sheet_lead": (
                "Ici, « spreadsheet » n’est pas un tableau de lignes : c’est un catalogue de fiches "
                "avec photo, marque, prix de référence et le lien que l’agent peut ouvrir."
            ),
            "sheet_p": (
                "L’index de cette accueil est anglais (sneakers, hoodie, jacket). « Baskets » renvoie "
                "souvent zéro carte ; sneakers remplit la grille. Les milliers de finds restent sur "
                "w2clinks — on ne les verse pas dans un .xlsx."
            ),
            "sheet_btn": "Ouvrir le catalogue",
            "wall_h": "Seize catégories pour le premier jour",
            "wall_lead": (
                "Chaque tuile ouvre la clé anglaise sur le catalogue de cette accueil. Commence par "
                "une seule : mélanger cinq catégories au premier colis est le plus court chemin vers "
                "un carton cher et mal calé."
            ),
            "rest_h": "Beaucoup de fiches ne s’achètent pas, même affichées",
            "rest_lead": (
                "Sur le site officiel, des fiches « Restricted item » ou à prix zéro. Ce n’est pas un "
                "bug : le lien source n’est pas achetable par l’agent, ou le prix n’a pas pu être lu."
            ),
            "rest_p": (
                "Pas de prix ni d’options réels : n’en compte pas. Tabac, alcool, médicaments sont "
                "souvent refusés — la liste est dans l’aide officielle, on ne l’invente pas. Pas de "
                "sous-déclaration."
            ),
            "rest_btn": "Aide de ce desk",
            "rest_cap": (
                "Help Center officiel. Capture du 1 oct. 2026. Storage Period (90 jours gratuits) "
                "et Prohibited Items sont là — pas de table copiée d’un autre agent."
            ),
            "shots_h": "Interface officielle, avec date",
            "shots_lead": (
                "L’estimateur LitBuy (shipping-estimate) est un SPA. Le 1 oct. 2026 le navigateur "
                "a bien rendu le formulaire. On ne colle pas un compteur de lignes ES."
            ),
            "shot_est_cap": (
                f"Freight estimate officiel. Capture du 1 oct. 2026. Destination de ce desk : {dest}. "
                "Les montants du jour sortent après Estimate — pas recopiés ici."
            ),
            "about_nav": "À propos",
            "about_title": f"À propos : desk indépendant LitBuy pour {locl}",
            "about_desc": (
                f"{host} est un desk éditorial indépendant. Pas de commandes, pas d’accès au compte. "
                "Lab 1 oct. 2026. France, pas la Belgique."
            ),
            "about_h1": f"À propos : desk indépendant LitBuy pour la <em>France</em>",
            "about_lead": (
                f"<strong>{host} n’est pas LitBuy.</strong> Desk éditorial : catalogue, labo fret, "
                "aide, actualités. On n’entrepose rien, on n’encaisse pas le port, on ne voit pas les comptes."
            ),
            "how_h": "Comment on travaille",
            "src_h": "Sources",
            "src_p": (
                "Fret : estimateur public litbuy.com/shipping-estimate, daté. Douane : sources "
                "officielles du pays, via les articles déjà classés. Ce qu’on n’a pas vérifié n’est pas écrit."
            ),
            "why_h": "Pourquoi si peu d’euros dans le texte",
            "why_p": (
                "Les tarifs bougent chaque semaine. Un chiffre copié ici serait faux demain. D’où "
                "l’estimateur officiel plus une capture datée, pas un tableau inventé."
            ),
            "inv_h": "Invite",
            "inv_p": (
                "Le bouton Register peut porter un code d’affiliation. Commission possible, sans "
                "surcoût. Tu peux t’inscrire sur litbuy.com sans code. Les faits gênants restent."
            ),
            "not_h": "Ce que nous ne sommes pas",
            "not_p": (
                "Ni boutique, ni entrepôt, ni file de tickets. Litiges seulement sur litbuy.com. "
                "Pas de 301 de ce TLD vers un autre host du même agent."
            ),
            "co_h": "Contact",
            "co_p": (
                f"Si une colonne du labo ou un lien casse, on le date dans Actualités. On ne réécrit "
                f"pas en silence. Pas de tickets commande. Rédaction : {mail}."
            ),
            "legal": (
                "On n’invente ni raison sociale ni taux de douane. Entrepôt : 90 jours gratuits "
                "depuis stocked/listed, plafond 120 (Help Center officiel, 1 oct. 2026). Pas de sous-déclaration."
            ),
        }
        return p

    if L == "de":
        land = "Österreich" if key == "at" else "Deutschland"
        p = {
            "agent_h": "Ein Einkaufsagent ist ein Zwischenhändler, kein Shop",
            "agent_lead": (
                f"LitBuy verkauft die Ware nicht. Er kauft in chinesischen Shops, die nicht ins "
                f"Ausland senden, fotografiert im Lager, lagert ein — danach buchst du die Linie nach {dest}."
            ),
            "agent_p": (
                "Das ändert den Ablauf: zweimal zahlen (Ware plus Inland China, später international), "
                "zweimal warten, dazwischen bündeln oder SKU wechseln. "
                f"{host} ist ein unabhängiger Desk, nicht die offizielle Site."
            ),
            "agent_btn": "Katalog dieser Startseite",
            "agent_cap": (
                "Offizielle Startseite litbuy.com. Eigene Aufnahme 1 Oct 2026. Keine leere SPA-Schale: "
                "die Seite hat gerendert. Why Choose zeigt 120-Day Storage."
            ),
            "sheet_h": "Ein Spreadsheet ist keine Excel-Datei",
            "sheet_lead": (
                "«Spreadsheet» meint hier keinen Zellenraster, sondern einen Katalog aus Karten: Foto, "
                "Marke, Referenzpreis, Link für den Agenten."
            ),
            "sheet_p": (
                "Der Index auf dieser Startseite ist englisch (sneakers, hoodie, jacket). «Turnschuhe» "
                "liefert oft ein leeres Raster; sneakers füllt es. Die Find-Menge bleibt auf w2clinks — "
                "kein .xlsx auf diesem Desk."
            ),
            "sheet_btn": "Katalog öffnen",
            "wall_h": "Sechzehn Kategorien für den ersten Tag",
            "wall_lead": (
                "Jede Kachel öffnet den englischen Schlüssel im Katalog dieser Startseite. Fang mit "
                "einer an: fünf Kategorien im ersten Karton machen den Versand teuer und unhandlich."
            ),
            "rest_h": "Viele Listings sind nicht kaufbar, obwohl sie erscheinen",
            "rest_lead": (
                "Offiziell siehst du «Restricted item» oder Preis null. Kein Seitenfehler: der "
                "Quell-Link ist für den Agenten nicht kaufbar oder der Preis nicht lesbar."
            ),
            "rest_p": (
                "Ohne echten Preis und Optionen nicht einplanen. Tabak, Alkohol, Arzneimittel werden "
                "oft abgelehnt — die Liste steht in der offiziellen Hilfe, wir erfinden sie nicht. "
                "Keine Unterdeklaration."
            ),
            "rest_btn": "Hilfe dieses Desks",
            "rest_cap": (
                "Offizielles Help Center. Aufnahme 1. Okt 2026. Storage Period (90 Tage gratis) "
                "und Prohibited Items liegen dort — keine fremde Verbotstabelle."
            ),
            "shots_h": "Offizielle Oberfläche, mit Datum",
            "shots_lead": (
                "Der LitBuy-Schätzer (shipping-estimate) ist ein SPA. Am 1. Okt 2026 hat "
                "der Browser das Formular gerendert. Keine ES-Linienzahl eines anderen Agenten."
            ),
            "shot_est_cap": (
                f"Offizieller Freight-Estimate. Aufnahme 1 Oct 2026. Ziel dieses Desks: {dest} "
                f"({land}). Beträge erscheinen nach Estimate — hier nicht kopiert."
            ),
            "about_nav": "Über uns",
            "about_title": f"Über uns: unabhängiger LitBuy-Desk für {land}",
            "about_desc": (
                f"{host} ist redaktionell unabhängig. Keine Bestellungen, kein Kontozugriff. "
                "Messung 1 Oct 2026."
            ),
            "about_h1": f"Über uns: unabhängiger LitBuy-Desk für <em>{land}</em>",
            "about_lead": (
                f"<strong>{host} ist nicht LitBuy.</strong> Redaktioneller Desk: Katalog, Versandlabor, "
                "Hilfe, Neuigkeiten. Wir lagern nichts, kassieren kein Porto, sehen keine Accounts."
            ),
            "how_h": "Wie wir arbeiten",
            "src_h": "Quellen",
            "src_p": (
                "Versand: öffentlicher Schätzer litbuy.com/shipping-estimate, mit Datum. Zoll: "
                "amtliche Quellen des Ziellands über die bereits rankenden Artikel. Ungeprüftes bleibt weg."
            ),
            "why_h": "Warum wenige Euro-Beträge",
            "why_p": (
                "Tarife ändern sich wöchentlich. Eine hier kopierte Zahl wäre morgen falsch. Deshalb "
                "Schätzer plus Snapshot, kein erfundenes Tableau."
            ),
            "inv_h": "Invite",
            "inv_p": (
                "Der Register-Link kann einen Affiliate-Code tragen. Provision möglich, ohne Aufpreis. "
                "Ohne Code auf litbuy.com starten. Unbequeme Facts bleiben stehen."
            ),
            "not_h": "Was wir nicht sind",
            "not_p": (
                "Kein Shop, kein Lager, kein Ticket-System. Reklamationen nur auf litbuy.com. "
                "Wir 301en dieses TLD nicht auf einen Schwester-Host desselben Agenten."
            ),
            "co_h": "Kontakt",
            "co_p": (
                f"Wenn eine Laborspalte oder ein Link bricht, datieren wir das in Neuigkeiten. "
                f"Keine stillen Korrekturen. Keine Bestelltickets. Redaktion: {mail}."
            ),
            "legal": (
                "Keine erfundenen Firmennamen oder Zoll-Sätze. Lager: 90 Tage gratis ab stocked/listed, "
                "höchstens 120 (offizielles Help Center, 1. Okt 2026). Keine Unterdeklaration."
            ),
        }
        return p

    if L == "nl":
        p = {
            "agent_h": "Een inkoopagent is een tussenpersoon, geen winkel",
            "agent_lead": (
                f"LitBuy verkoopt de spullen niet. Het koopt in Chinese shops die niet naar het "
                f"buitenland sturen, fotografeert in het magazijn, slaat op, daarna boek jij de lijn naar {dest}."
            ),
            "agent_p": (
                "Dat verandert de route: twee keer betalen (product plus binnenlands China, later "
                f"internationaal), twee keer wachten, tussendoor bundelen. {host} is een onafhankelijke "
                "desk, niet de officiële site."
            ),
            "agent_btn": "Catalogus op deze homepage",
            "agent_cap": (
                "Officiële homepage litbuy.com. Eigen opname 1 okt 2026. Geen lege SPA-schil: de "
                "pagina renderde. Why Choose toont 120-Day Storage."
            ),
            "sheet_h": "Een spreadsheet is geen Excel-bestand",
            "sheet_lead": (
                "«Spreadsheet» betekent hier geen rijen en kolommen, maar een catalogus van kaarten: "
                "foto, merk, referentieprijs en de link die de agent kan openen."
            ),
            "sheet_p": (
                "De index op deze homepage is Engels (sneakers, hoodie, jacket). «Sneakers» vult het "
                "raster; vertaalde woorden vaak 0. De finds blijven op w2clinks — geen .xlsx hier."
            ),
            "sheet_btn": "Catalogus openen",
            "wall_h": "Zestien categorieën voor de eerste dag",
            "wall_lead": (
                "Elke tegel opent de Engelse sleutel in de catalogus van deze homepage. Begin met één: "
                "vijf categorieën in het eerste pakket maakt verzenden duur en lastig."
            ),
            "rest_h": "Veel listings zijn niet koopbaar, ook al staan ze er",
            "rest_lead": (
                "Op de officiële site zie je «Restricted item» of prijs nul. Geen bug: de bronlink is "
                "niet koopbaar voor de agent, of de prijs was niet leesbaar."
            ),
            "rest_p": (
                "Geen echte prijs en opties: reken er niet op. Tabak, alcohol, geneesmiddelen worden "
                "vaak geweigerd — de lijst staat in de officiële help, wij verzinnen hem niet. Geen onderwaardering."
            ),
            "rest_btn": "Hulp van deze desk",
            "rest_cap": (
                "Officieel Help Center. Opname 1 okt 2026. Storage Period (90 dagen gratis) "
                "en Prohibited Items staan daar — geen tabel van een andere agent."
            ),
            "shots_h": "Officiële interface, met datum",
            "shots_lead": (
                "De LitBuy-estimator (shipping-estimate) is een SPA. Op 1 okt 2026 renderde "
                "de browser het formulier wel. Geen Spaanse lijntelling van een andere agent."
            ),
            "shot_est_cap": (
                f"Officiële freight estimate. Opname 1 okt 2026. Bestemming van deze desk: {dest}. "
                "Bedragen verschijnen na Estimate — hier niet gekopieerd."
            ),
            "about_nav": "Over ons",
            "about_title": f"Over ons: onafhankelijke LitBuy-desk voor {locl}",
            "about_desc": (
                f"{host} is redactioneel onafhankelijk. Geen orders, geen accounttoegang. Lab 1 okt 2026."
            ),
            "about_h1": f"Over ons: onafhankelijke LitBuy-desk voor <em>{locl}</em>",
            "about_lead": (
                f"<strong>{host} is LitBuy niet.</strong> Redactionele desk: catalogus, vrachtlab, "
                "hulp, nieuws. We slaan niets op, innen geen vracht, zien geen accounts."
            ),
            "how_h": "Hoe we werken",
            "src_h": "Bronnen",
            "src_p": (
                "Vracht: publieke estimator litbuy.com/shipping-estimate, met datum. Douane: officiële "
                "bronnen van het land via artikelen die al ranken. Wat we niet checkten, schrijven we niet."
            ),
            "why_h": "Waarom weinig eurobedragen in de tekst",
            "why_p": (
                "Tarieven schuiven wekelijks. Een hier gekopieerd cijfer is morgen fout. Daarom de "
                "officiële estimator plus een gedateerde screenshot, geen verzonnen tabel."
            ),
            "inv_h": "Invite",
            "inv_p": (
                "De Register-knop kan een affiliatecode dragen. Commissie mogelijk, zonder toeslag. "
                "Zonder code op litbuy.com starten. Ongemakkelijke feiten blijven staan."
            ),
            "not_h": "Wat we niet zijn",
            "not_p": (
                "Geen winkel, geen magazijn, geen ticketwachtrij. Claims alleen op litbuy.com. "
                "We 301’en dit TLD niet naar een zusterhost van dezelfde agent."
            ),
            "co_h": "Contact",
            "co_p": (
                f"Als een labkolom of een link stukgaat, dateren we dat in Nieuws. Geen stille herschrijving. "
                f"Geen ordertickets. Redactie: {mail}."
            ),
            "legal": (
                "Geen verzonnen bedrijfsnamen of douanetarieven. Magazijn: 90 dagen gratis vanaf stocked/listed, "
                "max 120 (officieel Help Center, 1 okt 2026). Geen onderwaardering."
            ),
        }
        return p

    if L == "it":
        p = {
            "agent_h": "Un agente d’acquisto è un intermediario, non un negozio",
            "agent_lead": (
                f"LitBuy non vende il prodotto. Compra per te in shop cinesi che non spediscono "
                f"all’estero, fotografa in magazzino, stocca, poi tu scegli la linea verso {dest}."
            ),
            "agent_p": (
                "Cambia tutto: paghi due volte (merce più domestico Cina, poi il freight "
                "internazionale), aspetti due volte, e in mezzo puoi raggruppare o cambiare SKU. "
                f"{host} è un desk indipendente, non il sito ufficiale."
            ),
            "agent_btn": "Vedi il catalogo di questa home",
            "agent_cap": (
                "Home ufficiale litbuy.com. Cattura del 1 ott 2026. Non è più un guscio SPA: "
                "la pagina ha renderizzato. Why Choose mostra 120-Day Storage."
            ),
            "sheet_h": "Uno spreadsheet non è un file Excel",
            "sheet_lead": (
                "Qui «spreadsheet» non è una tabella di righe: è un catalogo di schede con foto, "
                "marca, prezzo di riferimento e il link che l’agente può aprire."
            ),
            "sheet_p": (
                "L’indice di questa home è inglese (sneakers, hoodie, jacket). «Scarpe» spesso "
                "restituisce zero schede; sneakers riempie la griglia. I finds restano su w2clinks — "
                "niente .xlsx su questo desk."
            ),
            "sheet_btn": "Apri il catalogo",
            "wall_h": "Sedici categorie per il primo giorno",
            "wall_lead": (
                "Ogni tessera apre la chiave inglese nel catalogo di questa home. Inizia da una sola: "
                "mescolare cinque categorie nel primo pacco è la via più corta a un cartone caro."
            ),
            "rest_h": "Molte schede non si comprano, anche se compaiono",
            "rest_lead": (
                "Sul sito ufficiale vedi «Restricted item» o prezzo zero. Non è un bug: il link "
                "sorgente non è acquistabile dall’agente, o il prezzo non è stato letto."
            ),
            "rest_p": (
                "Senza prezzo e opzioni reali non contarci. Tabacco, alcol, farmaci sono rifiuti "
                "tipici — la lista sta nell’help ufficiale, non la inventiamo. Niente sottodichiarazione."
            ),
            "rest_btn": "Aiuto di questo desk",
            "rest_cap": (
                "Help Center ufficiale. Cattura del 1 ott 2026. Storage Period (90 giorni gratis) "
                "e Prohibited Items sono lì — nessuna tabella copiata da un altro agente."
            ),
            "shots_h": "Interfaccia ufficiale, con data",
            "shots_lead": (
                "Lo shipping-estimate LitBuy è una SPA. Il 1 ott 2026 il browser ha renderizzato "
                "il modulo. Non incolliamo il conteggio linee ES di un altro agente."
            ),
            "shot_est_cap": (
                f"Freight estimator ufficiale. Cattura del 1 ott 2026. Destinazione di questo desk: "
                f"{dest}. Gli importi del giorno escono dopo Check — non copiati qui."
            ),
            "about_nav": "Chi siamo",
            "about_title": f"Chi siamo: desk indipendente LitBuy per {locl}",
            "about_desc": (
                f"{host} è un desk editoriale indipendente. Niente ordini, niente accesso al conto. "
                "Lab 1 ott 2026."
            ),
            "about_h1": f"Chi siamo: desk indipendente LitBuy per l’<em>Italia</em>",
            "about_lead": (
                f"<strong>{host} non è LitBuy.</strong> Desk editoriale: catalogo, laboratorio spedizioni, "
                "aiuto, novità. Non stocchiamo merce, non incassiamo il porto, non vediamo i conti."
            ),
            "how_h": "Come lavoriamo",
            "src_h": "Fonti",
            "src_p": (
                "Spedizione: estimator pubblico litbuy.com/shipping-estimate, datato. Dogana: fonti "
                "ufficiali del paese, via gli articoli già in ranking. Ciò che non abbiamo verificato non si scrive."
            ),
            "why_h": "Perché così pochi euro nel testo",
            "why_p": (
                "Le tariffe si muovono ogni settimana. Un numero copiato qui sarebbe sbagliato domani. "
                "Perciò l’estimator ufficiale più uno screenshot datato, non una tabella inventata."
            ),
            "inv_h": "Invite",
            "inv_p": (
                "Il pulsante Register apre litbuy.com/register, senza copiare un codice di un altro agente. "
                "Puoi iscriverti senza codice. I fatti scomodi restano pubblicati."
            ),
            "not_h": "Cosa non siamo",
            "not_p": (
                "Né negozio, né magazzino, né coda ticket. Reclami solo su litbuy.com. Non facciamo "
                "301 di questo TLD verso un altro host dello stesso agente."
            ),
            "co_h": "Contatto",
            "co_p": (
                f"Se una colonna del laboratorio o un link si rompe, lo datiamo in Novità. Niente "
                f"riscritture silenziose. Niente ticket ordine. Redazione: {mail}."
            ),
            "legal": (
                "Non inventiamo ragioni sociali né aliquote doganali. Magazzino: 90 giorni gratis da "
                "stocked/listed, tetto 120 (Help Center ufficiale, 1 ott 2026). Niente sottodichiarazione."
            ),
        }
        return p

    # English desks (US/UK/CA) + EU/now hubs

    dest_bit = (
        "This hostname is not a destination — pick a country in the official estimator."
        if key in ("now", "eu")
        else f"International SKU destination for this desk: {dest}."
    )
    p = {
        "agent_h": "A purchasing agent is an intermediary, not a shop",
        "agent_lead": (
            "LitBuy does not sell the goods. It buys for you in Chinese shops that do not ship "
            f"abroad, photographs in the warehouse, stores, then you book the international line. {dest_bit}"
        ),
        "agent_p": (
            "That changes the path: you pay twice (goods plus China domestic, later international freight), "
            "you wait twice, and you can consolidate or switch SKU in between. "
            f"{host} is an independent information desk, not litbuy.com."
        ),
        "agent_btn": "See the catalogue on this homepage",
        "agent_cap": (
            "Official litbuy.com home. Own capture 1 Oct 2026. Not the empty SPA shell: the page "
            "rendered. Why Choose on the hero reads 120-Day Storage."
        ),
        "sheet_h": "A spreadsheet is not an Excel file",
        "sheet_lead": (
            "Here “spreadsheet” is not rows and columns. It is a catalogue of product cards — photo, "
            "brand, reference price, and the link the agent can open."
        ),
        "sheet_p": (
            "The index on this homepage is English (sneakers, hoodie, jacket). Local translations often "
            "return zero cards; the English key fills the grid. The full finds stay on w2clinks — this "
            "desk does not dump them into a .xlsx."
        ),
        "sheet_btn": "Open the catalogue",
        "wall_h": "Sixteen categories so the first day is not a maze",
        "wall_lead": (
            "Each tile opens the English key on this homepage catalogue. Start with one category: mixing "
            "five on the first parcel is the fastest way to an expensive, awkward carton."
        ),
        "rest_h": "Many listings cannot be bought even when they appear",
        "rest_lead": (
            "On the official site you will see “Restricted item” cards and zero prices. That is not a "
            "broken page: the source link is not available to the agent, or the price could not be read."
        ),
        "rest_p": (
            "If a card has no real price and options, do not count on it. Tobacco, alcohol and medicines "
            "are typical refusals — the list lives in official help, we do not invent one here. No "
            "under-declaration."
        ),
        "rest_btn": "Help on this desk",
        "rest_cap": (
            "Official Help Center. Own capture 1 Oct 2026. Storage Period (90 free days from "
            "stocked/listed) and Prohibited Items sit there — not another agent’s table."
        ),
        "shots_h": "Official UI, with a date",
        "shots_lead": (
            "LitBuy’s shipping-estimate page is a SPA. On 1 Oct 2026 the browser rendered the form. "
            "We do not paste another agent’s Spain line count."
        ),
        "shot_est_cap": (
            f"Official freight estimate. Own capture 1 Oct 2026. Destination for this desk: {dest}. "
            "Live amounts appear after Check — not copied here."
            if key not in ("now", "eu")
            else (
                "Official freight estimate. Own capture 1 Oct 2026. This hub is not a destination — "
                "pick a country in the form. Live amounts appear after Check."
            )
        ),
        "about_nav": "About",
        "about_title": f"Who we are: independent LitBuy desk for {locl}",
        "about_desc": (
            f"{host} is an independent editorial desk. No orders, no account access. Lab 1 Oct 2026."
        ),
        "about_h1": f"Who we are: independent LitBuy desk for <em>{locl}</em>",
        "about_lead": (
            f"<strong>{host} is not LitBuy.</strong> Editorial desk: catalogue, freight lab, help, news. "
            "We do not store goods, collect postage, or see accounts."
        ),
        "how_h": "How we work",
        "src_h": "Sources",
        "src_p": (
            "Freight: public estimator at litbuy.com/shipping-estimate, dated. Duty: official sources "
            "for the destination, via ranked articles on this host. What we have not checked stays off the page."
        ),
        "why_h": "Why so few live amounts in the prose",
        "why_p": (
            "Lines move weekly. A number copied here would be wrong tomorrow. So: official estimator "
            "plus a dated screenshot, not an invented table."
        ),
        "inv_h": "Invite",
        "inv_p": (
            "The Register button may carry an affiliate code. Commission possible, no surcharge. You can "
            "join at litbuy.com without it. Uncomfortable facts stay published."
        ),
        "not_h": "What we are not",
        "not_p": (
            "Not a shop, warehouse, or ticket queue. Claims only on litbuy.com. We do not 301 this TLD "
            "onto another same-agent host or onto a hub."
        ),
        "co_h": "Contact",
        "co_p": (
            f"If a lab column or a link breaks, we date it on News. We do not silently rewrite old checks. "
            f"This desk does not answer order tickets. Editorial: {mail}."
        ),
        "legal": (
            "We do not invent company names or duty rates. Warehouse: 90 free days from stocked/listed, "
            "120-day max (official Help Center, 1 Oct 2026). No declared-value coaching."
        ),
    }
    if key in ("now", "eu"):
        p["about_title"] = (
            "Who we are: LitBuy coupon / spreadsheet hub"
            if key == "now"
            else "Who we are: LitBuy English Europe hub"
        )
        p["about_h1"] = (
            "Who we are: independent LitBuy <em>hub</em>"
            if key == "now"
            else "Who we are: independent LitBuy <em>EU hub</em>"
        )
        p["src_p"] = (
            "Freight: public estimator — this hostname is not a destination. Pick a country in "
            "shipping-estimate. Dated articles already on this host stay. What we have not checked stays off the page."
        )
    return p
