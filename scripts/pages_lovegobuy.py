"""Page metadata and localized content for Lovegobuy Spreadsheet cluster."""

from __future__ import annotations

from scripts.link_helpers_lovegobuy import (
    AGENT_PLATFORM,
    category_url,
    main_spreadsheet_url,
    product_search_url,
)

YEAR = "2026"
SPREADSHEET = main_spreadsheet_url()
PLATFORM = AGENT_PLATFORM["baseUrl"]
REGISTER = AGENT_PLATFORM["registerUrl"]

CTA_SPREADSHEET = "Open Lovegobuy Spreadsheet"
CTA_BROWSE = "Browse Spreadsheet"
CTA_COUPONS = "Lovegobuy Coupons"
CTA_REGISTER = "Register on Lovegobuy"
CTA_SHIPPING = "Shipping Guide"


def _faq(items: list[tuple[str, str]]) -> list[dict[str, str]]:
    return [{"question": q, "answer": a} for q, a in items]


def _loc(
    *,
    title: str,
    description: str,
    h1: str,
    intro: str,
    sections: list[tuple[str, str]] | None = None,
    faq: list[tuple[str, str]] | None = None,
) -> dict:
    return {
        "title": title,
        "description": description,
        "h1": h1,
        "intro": intro,
        "sections": sections or [],
        "faq": _faq(faq or []),
    }


def _page(
    slug: str,
    *,
    cta: str,
    cta_href: str,
    en: dict | None = None,
    es: dict | None = None,
    fr: dict | None = None,
    nl: dict | None = None,
    it: dict | None = None,
    fi: dict | None = None,
    regions: list[str] | None = None,
) -> dict:
    base = en or es or fr or nl or it or fi
    if base is None:
        raise ValueError(f"page {slug!r} needs at least one locale block")
    return {
        "slug": slug,
        "regions": regions,
        "cta": cta,
        "cta_href": cta_href,
        "en": en or base,
        "es": es or base,
        "fr": fr or base,
        "nl": nl or base,
        "it": it or base,
        "fi": fi or base,
    }


# --- Shared section blocks (W2CLinks) ---
SEC_SPREADSHEET = (
    "Browse finds on W2CLinks",
    f'The live spreadsheet hub is at <a href="{SPREADSHEET}" target="_blank" rel="noopener">'
    "w2clinks.com/spreadsheet/</a> — filter by category, brand, or keyword. "
    "This site is an independent guide; we do not host a local product database.",
)
SEC_AGENT = (
    "Order on Lovegobuy",
    f"After you pick a find, paste the seller link on "
    f'<a href="{REGISTER}" target="_blank" rel="noopener">Lovegobuy</a> ({PLATFORM}). '
    "Lovegobuy purchases from Taobao, 1688, and Weidian, provides QC photos, then ships internationally.",
)
SEC_CATS = (
    "Quick categories",
    f'Sneakers: <a href="{category_url("SNEAKERS")}" target="_blank" rel="noopener">Browse sneakers</a>. '
    f'Hoodies: <a href="{category_url("HOODIES")}" target="_blank" rel="noopener">Browse hoodies</a>. '
    f'Bags: <a href="{category_url("BAGS")}" target="_blank" rel="noopener">Browse bags</a>.',
)


PAGES: list[dict] = [
    _page(
        "",
        cta=CTA_SPREADSHEET,
        cta_href=SPREADSHEET,
        en=_loc(
            title=f"Lovegobuy Spreadsheet Guide — Finds, Coupons & Shipping ({YEAR})",
            description="Independent Lovegobuy spreadsheet guide: browse finds on W2CLinks, coupon tips, shipping and QC basics for global buyers.",
            h1="Lovegobuy Spreadsheet: Finds, Coupons and Shipping Guide",
            intro=(
                "Lovegobuy is a China shopping agent for Taobao, 1688, and Weidian. "
                "This guide explains spreadsheet-style finds and links you to W2CLinks — not a fake local catalog."
            ),
            sections=[SEC_SPREADSHEET, SEC_AGENT, SEC_CATS],
            faq=[
                ("Is this the official Lovegobuy spreadsheet?", "No — independent guide. Spreadsheet links open W2CLinks."),
                ("How do I open the Lovegobuy spreadsheet?", f"Use the button above or visit {SPREADSHEET}"),
                ("Does Lovegobuy support Taobao and 1688?", "Yes — paste links or search by keyword on Lovegobuy."),
            ],
        ),
        es=_loc(
            title=f"Lovegobuy Spreadsheet España — Guía, Cupones y Envío ({YEAR})",
            description="Guía independiente de lovegobuy spreadsheet: finds en W2CLinks, cupones, envío y QC para compradores en España.",
            h1="Lovegobuy Spreadsheet para España",
            intro=(
                "Lovegobuy es un agente de compras en China para Taobao, 1688 y Weidian. "
                "Esta guía explica el spreadsheet de finds y enlaza a W2CLinks."
            ),
            sections=[
                (
                    "Explorar finds en W2CLinks",
                    f'El spreadsheet en vivo está en <a href="{SPREADSHEET}" target="_blank" rel="noopener">'
                    "w2clinks.com/spreadsheet/</a>. Filtra por categoría, marca o palabra clave.",
                ),
                (
                    "Pedir en Lovegobuy",
                    f'Después de elegir un find, pega el enlace en <a href="{REGISTER}" target="_blank" rel="noopener">Lovegobuy</a>.',
                ),
                SEC_CATS,
            ],
            faq=[
                ("¿Es el spreadsheet oficial de Lovegobuy?", "No — guía independiente. Los enlaces abren W2CLinks."),
                ("¿Lovegobuy es confiable?", "Lee nuestra página de opiniones y la guía de legitimidad."),
                ("¿Cuánto tarda el envío a España?", "Varía según la línea — consulta la guía de envío."),
            ],
        ),
        fr=_loc(
            title=f"Lovegobuy Spreadsheet France — Guide, Coupons et Livraison ({YEAR})",
            description="Guide indépendant lovegobuy spreadsheet : finds W2CLinks, coupons, livraison et QC pour la France.",
            h1="Lovegobuy Spreadsheet pour la France",
            intro=(
                "Lovegobuy est un agent d'achat Chine pour Taobao, 1688 et Weidian. "
                "Ce guide explique le tableur de finds via W2CLinks."
            ),
            sections=[
                (
                    "Parcourir les finds sur W2CLinks",
                    f'Le hub spreadsheet : <a href="{SPREADSHEET}" target="_blank" rel="noopener">w2clinks.com/spreadsheet/</a>.',
                ),
                (
                    "Commander sur Lovegobuy",
                    f'Collez le lien vendeur sur <a href="{REGISTER}" target="_blank" rel="noopener">Lovegobuy</a>.',
                ),
                SEC_CATS,
            ],
            faq=[
                ("Est-ce le spreadsheet officiel ?", "Non — guide indépendant avec liens W2CLinks."),
                ("Lovegobuy est-il fiable ?", "Voir notre page avis et la page légitimité."),
                ("Délais livraison France ?", "Variable selon la ligne — voir guide livraison."),
            ],
        ),
        nl=_loc(
            title=f"Lovegobuy Spreadsheet Nederland — Gids, Coupons & Verzending ({YEAR})",
            description="Onafhankelijke lovegobuy spreadsheet gids: finds op W2CLinks, coupons, verzending en QC voor Nederland.",
            h1="Lovegobuy Spreadsheet voor Nederland",
            intro=(
                "Lovegobuy is een China shopping agent voor Taobao, 1688 en Weidian. "
                "Deze gids legt spreadsheet/finds uit via W2CLinks."
            ),
            sections=[
                (
                    "Browse finds op W2CLinks",
                    f'Live spreadsheet: <a href="{SPREADSHEET}" target="_blank" rel="noopener">w2clinks.com/spreadsheet/</a>.',
                ),
                (
                    "Bestellen op Lovegobuy",
                    f'Plak de verkoperlink op <a href="{REGISTER}" target="_blank" rel="noopener">Lovegobuy</a>.',
                ),
                SEC_CATS,
            ],
            faq=[
                ("Is dit het officiële spreadsheet?", "Nee — onafhankelijke gids met W2CLinks-links."),
                ("Is Lovegobuy betrouwbaar?", "Zie onze ervaringen-pagina."),
                ("Hoe lang duurt verzending?", "Zie de verzendgids voor NL."),
            ],
        ),
        fi=_loc(
            title=f"Lovegobuy Spreadsheet — Opas, Kupongit ja Toimitus ({YEAR})",
            description="Riippumaton Lovegobuy spreadsheet -opas: löydöt W2CLinksissä, kupongit, toimitus ja QC suomalaisille ostajille.",
            h1="Lovegobuy Spreadsheet — Opas suomalaisille",
            intro=(
                "Lovegobuy on Kiinan ostovälittäjä Taobaolle, 1688:lle ja Weidianille. "
                "Tämä opas selittää spreadsheet-löydöt W2CLinks-linkin kautta."
            ),
            sections=[
                (
                    "Selaa löytöjä W2CLinksissä",
                    f'Live-spreadsheet: <a href="{SPREADSHEET}" target="_blank" rel="noopener">w2clinks.com/spreadsheet/</a>.',
                ),
                (
                    "Tilaa Lovegobuylta",
                    f'Liitä myyjän linkki <a href="{REGISTER}" target="_blank" rel="noopener">Lovegobuyhin</a>.',
                ),
                SEC_CATS,
            ],
            faq=[
                ("Onko tämä virallinen spreadsheet?", "Ei — riippumaton opas, linkit avautuvat W2CLinksissä."),
                ("Onko Lovegobuy luotettava?", "Katso kokemukset-sivu."),
                ("Kuinka kauan toimitus kestää?", "Katso toimitusopas Suomeen."),
            ],
        ),
    ),
    _page(
        "lovegobuy-spreadsheet",
        cta=CTA_BROWSE,
        cta_href=SPREADSHEET,
        en=_loc(
            title=f"Lovegobuy Spreadsheet ({YEAR}) — Browse Finds on W2CLinks",
            description="lovegobuy spreadsheet — browse community finds, categories and brands. All product actions open W2CLinks.",
            h1="Lovegobuy Spreadsheet",
            intro="Searchers looking for lovegobuy spreadsheet want a browsable list of community finds with source links.",
            sections=[SEC_SPREADSHEET, SEC_CATS, SEC_AGENT],
            faq=[
                ("lovegobuy spreadsheet vs spreadsheets?", "Same hub — plural searches lead here."),
                ("best lovegobuy spreadsheet?", "See our best spreadsheet guide for curated entry points."),
            ],
        ),
        es=_loc(
            title=f"Lovegobuy Spreadsheet ({YEAR}) — Tabla de Finds",
            description="lovegobuy spreadsheet y spreedsheet — tabla de finds en W2CLinks con categorías y marcas.",
            h1="Lovegobuy Spreadsheet",
            intro="Los buscadores de lovegobuy spreadsheet quieren una lista navegable de finds con enlaces.",
            sections=[SEC_SPREADSHEET, SEC_CATS, SEC_AGENT],
            faq=[
                ("¿lovegobuy spreedsheet?", "Variante ortográfica — mismo spreadsheet en W2CLinks."),
                ("¿Mejor spreadsheet?", "Ver guía best/mejor spreadsheet."),
            ],
        ),
        fr=_loc(
            title=f"Lovegobuy Spreadsheet ({YEAR}) — Tableau de Finds",
            description="lovegobuy spreadsheet — tableau de finds communautaires sur W2CLinks.",
            h1="Lovegobuy Spreadsheet",
            intro="Les recherches lovegobuy spreadsheet visent une liste de finds avec liens sources.",
            sections=[SEC_SPREADSHEET, SEC_CATS, SEC_AGENT],
            faq=[("spreadsheet lovegobuy ?", "Même hub W2CLinks — ordre des mots différent.")],
        ),
        nl=_loc(
            title=f"Lovegobuy Spreadsheet ({YEAR}) — Browse Finds",
            description="lovegobuy spreadsheet 2025/2026 — community finds op W2CLinks met filters.",
            h1="Lovegobuy Spreadsheet",
            intro="Zoekers naar lovegobuy spreadsheet willen een doorbladerbare finds-lijst.",
            sections=[SEC_SPREADSHEET, SEC_CATS, SEC_AGENT],
            faq=[("lovegobuy spreadsheet 2025?", "W2CLinks hub wordt doorlopend bijgewerkt.")],
        ),
        fi=_loc(
            title=f"Lovegobuy Spreadsheet ({YEAR}) — Löydöt W2CLinksissä",
            description="lovegobuy spreadsheet — yhteisön löydöt ja kategoriat W2CLinksissä.",
            h1="Lovegobuy Spreadsheet",
            intro="Lovegobuy spreadsheet -hakijat haluavat selattavan löytölistan lähdelinkeillä.",
            sections=[SEC_SPREADSHEET, SEC_CATS, SEC_AGENT],
            faq=[("Mikä on Lovegobuy spreadsheet?", "W2CLinks-hubi community-löydöille.")],
        ),
    ),
    _page(
        "best-lovegobuy-spreadsheet",
        cta=CTA_BROWSE,
        cta_href=SPREADSHEET,
        en=_loc(
            title=f"Best Lovegobuy Spreadsheet ({YEAR})",
            description="best lovegobuy spreadsheet — how to pick categories, brands and filters on W2CLinks.",
            h1="Best Lovegobuy Spreadsheet",
            intro="Commercial intent around the best lovegobuy spreadsheet entry points for shoes, hoodies, and bags.",
            sections=[
                ("Top entry points", f'Start at {SPREADSHEET} then filter sneakers, bags, or search Nike/Adidas.'),
                ("Compare before you buy", "Use QC guide and shipping notes before submitting a parcel."),
            ],
            faq=[("Is there one official best list?", "W2CLinks aggregates community finds — compare multiple picks.")],
        ),
        nl=_loc(
            title=f"Beste Lovegobuy Spreadsheet ({YEAR})",
            description="best lovegobuy spreadsheet / beste lovegobuy spreadsheet — KD-laag hangend fruit voor NL.",
            h1="Beste Lovegobuy Spreadsheet",
            intro="De zoekterm best lovegobuy spreadsheet wijst op curated ingangen voor sneakers en streetwear.",
            sections=[("Startpunten", f'Open {SPREADSHEET} en filter op categorie of merk.')],
            faq=[("Beste spreadsheet 2026?", "W2CLinks hub — filter op nieuwste finds.")],
        ),
        fr=_loc(
            title=f"Meilleur Lovegobuy Spreadsheet ({YEAR})",
            description="meilleur lovegobuy spreadsheet — points d'entrée sur W2CLinks.",
            h1="Meilleur Lovegobuy Spreadsheet",
            intro="Guide pour les recherches commerciales autour du meilleur tableur Lovegobuy.",
            sections=[("Entrées recommandées", f'Commencez sur {SPREADSHEET}.')],
            faq=[],
        ),
        es=_loc(
            title=f"Mejor Lovegobuy Spreadsheet ({YEAR})",
            description="mejor lovegobuy spreadsheet — categorías y marcas en W2CLinks.",
            h1="Mejor Lovegobuy Spreadsheet",
            intro="Guía para quienes buscan el mejor punto de entrada al spreadsheet Lovegobuy.",
            sections=[("Puntos de entrada", f'Abre {SPREADSHEET} y filtra por categoría.')],
            faq=[],
        ),
        fi=_loc(
            title=f"Paras Lovegobuy Spreadsheet ({YEAR})",
            description="paras lovegobuy spreadsheet — parhaat aloitus kohdat W2CLinksissä.",
            h1="Paras Lovegobuy Spreadsheet",
            intro="Kaupallinen haku parhaaseen Lovegobuy spreadsheet -kokemukseen.",
            sections=[("Aloituspisteet", f'Avaa {SPREADSHEET} ja suodata kategorian mukaan.')],
            faq=[],
        ),
    ),
    _page(
        "lovegobuy-coupon",
        cta=CTA_COUPONS,
        cta_href=REGISTER,
        en=_loc(
            title=f"Lovegobuy Coupon Codes ({YEAR})",
            description="lovegobuy coupon codes and coupons — how to apply invitation codes on Lovegobuy after browsing W2CLinks.",
            h1="Lovegobuy Coupon Codes",
            intro="Coupon searches often mean registration bonuses or shipping discounts on Lovegobuy checkout.",
            sections=[
                ("Register with invitation link", f'Use <a href="{REGISTER}" target="_blank" rel="noopener">our Lovegobuy registration link</a> for referral benefits.'),
                ("How to apply coupons", "Enter codes during registration or parcel payment — check Lovegobuy help for current rules."),
            ],
            faq=[
                ("lovegobuy coupon codes?", "Policies change — verify inside Lovegobuy account."),
                ("how to use coupons on lovegobuy?", "Apply at signup or checkout per Lovegobuy UI."),
                ("Multiple coupons?", "Usually one active rule per step — read checkout notes."),
            ],
        ),
        es=_loc(
            title=f"Cupón Lovegobuy — Códigos e Invitación ({YEAR})",
            description="cupon lovegobuy, lovegobuy codes — cómo usar cupones en Lovegobuy.",
            h1="Cupón y códigos Lovegobuy",
            intro="Las búsquedas de cupon lovegobuy suelen referirse a bonos de registro o envío.",
            sections=[("Registro", f'<a href="{REGISTER}" target="_blank" rel="noopener">Enlace de invitación Lovegobuy</a>.')],
            faq=[("¿Cómo usar cupones?", "Durante registro o pago del paquete en Lovegobuy.")],
        ),
        fr=_loc(
            title=f"Code Promo Lovegobuy — Coupons ({YEAR})",
            description="coupon lovegobuy, lovegobuy coupons — codes et invitation.",
            h1="Coupon et codes Lovegobuy",
            intro="Recherches coupon lovegobuy pour bonus d'inscription ou réductions.",
            sections=[("Inscription", f'<a href="{REGISTER}" target="_blank" rel="noopener">Lien d\'invitation</a>.')],
            faq=[],
        ),
        nl=_loc(
            title=f"Lovegobuy Coupon Code — Kortingscodes ({YEAR})",
            description="lovegobuy coupon code, lovegobuy coupons — hoe coupon op Lovegobuy te gebruiken.",
            h1="Lovegobuy coupon en kortingscode",
            intro="Coupon-zoekers willen registratiebonus of verzendkorting.",
            sections=[("Registreren", f'<a href="{REGISTER}" target="_blank" rel="noopener">Lovegobuy uitnodigingslink</a>.')],
            faq=[
                ("how to use coupon on lovegobuy?", "Bij registratie of afrekenen in Lovegobuy."),
                ("Meerdere coupons?", "Meestal één regel per stap."),
            ],
        ),
        fi=_loc(
            title=f"Lovegobuy Kuponki ja alennuskoodit ({YEAR})",
            description="lovegobuy kuponki — rekisteröitymis- ja alennuskoodit.",
            h1="Lovegobuy kuponki",
            intro="Kuponkihaun tarkoitus on usein rekisteröitymisbonus tai toimitusalennus.",
            sections=[("Rekisteröidy", f'<a href="{REGISTER}" target="_blank" rel="noopener">Lovegobuy-kutsulinkki</a>.')],
            faq=[("Miten käytän kuponkia?", "Rekisteröinnissä tai maksuvaiheessa Lovegobuyssa.")],
        ),
    ),
    _page(
        "lovegobuy-shipping",
        cta=CTA_SHIPPING,
        cta_href=SPREADSHEET,
        en=_loc(
            title=f"Lovegobuy Shipping — Costs, Calculator & Delivery ({YEAR})",
            description="lovegobuy shipping, shipping calculator, delivery times — independent guide with W2CLinks browse first.",
            h1="Lovegobuy Shipping Guide",
            intro="Shipping questions cover line selection, weight, insurance, and customs after QC approval.",
            sections=[
                ("Workflow", "Browse W2CLinks → order on Lovegobuy → QC photos → submit parcel → choose shipping line."),
                ("Calculator notes", "Estimate weight and compare economy vs express inside Lovegobuy before paying freight."),
            ],
            faq=[
                ("how much is lovegobuy shipping?", "Depends on weight, line, and destination — quote in Lovegobuy."),
                ("how long does lovegobuy take to ship?", "Often weeks — no universal guarantee."),
                ("does lovegobuy have insurance?", "Optional shipping insurance may be available at checkout."),
            ],
        ),
        es=_loc(
            title=f"Envío Lovegobuy — Costes y Plazos ({YEAR})",
            description="envío lovegobuy — guía de envío a España con aduanas.",
            h1="Envío Lovegobuy",
            intro="Preguntas sobre envío, aduanas españolas y tiempos de entrega.",
            sections=[("Flujo", "W2CLinks → Lovegobuy → QC → paquete → línea de envío.")],
            faq=[("¿Cuánto tarda a España?", "Varía según línea y peso.")],
        ),
        fr=_loc(
            title=f"Livraison Lovegobuy — Délais et Frais ({YEAR})",
            description="livraison lovegobuy — guide livraison France.",
            h1="Livraison Lovegobuy",
            intro="Questions sur délais, douanes et choix de ligne vers la France.",
            sections=[("Parcours", "W2CLinks → commande Lovegobuy → QC → colis → expédition.")],
            faq=[("Délais France ?", "Variable — comparer lignes économiques et express.")],
        ),
        nl=_loc(
            title=f"Lovegobuy Verzending — Calculator en Tijden ({YEAR})",
            description="lovegobuy shipping calculator, how long is lovegobuy shipping — gids voor Nederland.",
            h1="Lovegobuy verzending",
            intro="Verzendvragen: calculator, PostNL/DHL tijden, tracking.",
            sections=[("Calculator", "Schat gewicht en vergelijk lijnen in Lovegobuy checkout.")],
            faq=[
                ("how long is lovegobuy shipping?", "Vaak meerdere weken — afhankelijk van lijn."),
                ("how to track lovegobuy order?", "Tracking in Lovegobuy account na verzending."),
            ],
        ),
        fi=_loc(
            title=f"Lovegobuy Toimitus — Kustannukset ja Ajat ({YEAR})",
            description="lovegobuy toimitus, lovegobuy shipping — opas suomalaisille.",
            h1="Lovegobuy toimitus",
            intro="Toimituskysymykset: paino, linja, tullit Suomeen.",
            sections=[("Prosessi", "W2CLinks → Lovegobuy → QC → paketti → toimituslinja.")],
            faq=[("Kuinka kauan toimitus kestää?", "Useita viikkoja tyypillisesti — riippuu linjasta.")],
        ),
    ),
    _page(
        "is-lovegobuy-legit",
        cta=CTA_REGISTER,
        cta_href=REGISTER,
        en=_loc(
            title="Is Lovegobuy Legit? Safety Guide for Buyers",
            description="is lovegobuy legit, is lovegobuy safe, is lovegobuy real — trust signals without fake ratings.",
            h1="Is Lovegobuy Legit and Safe?",
            intro="Legitimacy searches want QC proof, shipping track record, and payment clarity — not hype.",
            sections=[
                ("What to verify", "QC photos, warehouse timeline, refund policy on Lovegobuy help center."),
                ("Red flags", "Unrealistic shipping promises or unofficial payment requests outside Lovegobuy."),
            ],
            faq=[
                ("is lovegobuy legit?", "Established agent with public QC workflow — do your own due diligence."),
                ("is lovegobuy safe?", "Use official Lovegobuy checkout and review QC before shipping."),
                ("lovegobuy scam?", "Avoid off-platform payments and unverified middlemen."),
            ],
        ),
        es=_loc(
            title="¿Es Lovegobuy legítimo? Guía de confianza",
            description="is lovegobuy legit, lovegobuy es confiable — señales de confianza.",
            h1="¿Es Lovegobuy legítimo y seguro?",
            intro="Búsquedas de legitimidad y si lovegobuy es confiable.",
            sections=[("Verificar", "Fotos QC, políticas de reembolso, soporte oficial.")],
            faq=[("¿Lovegobuy es confiable?", "Agente conocido — revisa QC y políticas actuales.")],
        ),
        fr=_loc(
            title="Lovegobuy est-il fiable ? Guide de confiance",
            description="lovegobuy avis, lovegobuy fiable, is lovegobuy legit — guide indépendant.",
            h1="Lovegobuy est-il légitime ?",
            intro="Les recherches avis et fiabilité demandent preuves QC et politiques claires.",
            sections=[("Vérifications", "QC, délais, support Lovegobuy officiel.")],
            faq=[("Arnaque ?", "Paiements uniquement via Lovegobuy officiel.")],
        ),
        nl=_loc(
            title="Is Lovegobuy betrouwbaar? Legit gids",
            description="is lovegobuy legit, is lovegobuy betrouwbaar — onafhankelijke gids.",
            h1="Is Lovegobuy legit en betrouwbaar?",
            intro="Trust-zoekopdrachten voor Nederlandse kopers.",
            sections=[("Checklist", "QC-foto's, tracking, refund policy.")],
            faq=[("is lovegobuy betrouwbaar?", "Bekende agent — eigen due diligence blijft nodig.")],
        ),
        fi=_loc(
            title="Onko Lovegobuy luotettava? Turvallisuusopas",
            description="is lovegobuy legit, onko lovegobuy luotettava — riippumaton opas.",
            h1="Onko Lovegobuy luotettava?",
            intro="Luotettavuushaut — QC, toimitus ja maksutapa.",
            sections=[("Tarkista", "QC-kuvat, virallinen checkout, tuki.")],
            faq=[("Onko Lovegobuy huijaus?", "Vältä maksuja alustan ulkopuolella.")],
        ),
    ),
    _page(
        "lovegobuy-qc",
        cta=CTA_BROWSE,
        cta_href=SPREADSHEET,
        en=_loc(
            title="Lovegobuy QC Photos Guide",
            description="qc lovegobuy — quality check photos before international shipping.",
            h1="Lovegobuy QC Guide",
            intro="QC photos let you approve items in warehouse before paying international freight.",
            sections=[("QC workflow", "Request photos → review defects → approve or exchange → ship parcel.")],
            faq=[("How many QC photos?", "Typically multiple angles — request more if needed.")],
        ),
        es=_loc(
            title="QC Lovegobuy — Fotos de control de calidad",
            description="qc lovegobuy — fotos QC antes del envío internacional.",
            h1="Guía QC Lovegobuy",
            intro="Las fotos QC permiten revisar el producto en almacén.",
            sections=[("Proceso", "Solicitar fotos → revisar → aprobar → enviar.")],
            faq=[],
        ),
        fr=_loc(
            title="QC Lovegobuy — Photos de contrôle qualité",
            description="lovegobuy qc — photos avant expédition.",
            h1="Guide QC Lovegobuy",
            intro="Les photos QC valident l'article avant frais d'expédition internationale.",
            sections=[],
            faq=[],
        ),
        nl=_loc(
            title="Lovegobuy QC — Kwaliteitscontrole foto's",
            description="lovegobuy qc — foto's voor internationale verzending.",
            h1="Lovegobuy QC gids",
            intro="QC-foto's voor goedkeuring in het magazijn.",
            sections=[],
            faq=[],
        ),
        fi=_loc(
            title="Lovegobuy QC — Laatukuvat",
            description="lovegobuy qc — laatukuvat ennen kansainvälistä toimitusta.",
            h1="Lovegobuy QC-opas",
            intro="QC-kuvat ennen kansainvälisen toimituksen maksamista.",
            sections=[],
            faq=[],
        ),
    ),
    _page(
        "how-to-use-lovegobuy",
        cta=CTA_REGISTER,
        cta_href=REGISTER,
        en=_loc(
            title="How to Use Lovegobuy — Step-by-Step Guide",
            description="how to use lovegobuy, how to buy on lovegobuy, how does lovegobuy work.",
            h1="How to Use Lovegobuy",
            intro="Beginner workflow: browse W2CLinks, paste link, pay, QC, ship.",
            sections=[
                ("Step 1", f'Browse {SPREADSHEET}'),
                ("Step 2", f'Register on <a href="{REGISTER}" target="_blank" rel="noopener">Lovegobuy</a> and paste item URL'),
                ("Step 3", "Pay for items, wait for warehouse, review QC, submit parcel."),
            ],
            faq=[("how does lovegobuy work?", "Agent buys in China, QC in warehouse, ships to you.")],
        ),
        es=_loc(
            title="Cómo usar Lovegobuy — Guía paso a paso",
            description="cómo comprar en lovegobuy — tutorial para principiantes.",
            h1="Cómo usar Lovegobuy",
            intro="Flujo: W2CLinks → pegar enlace → pagar → QC → enviar.",
            sections=[],
            faq=[],
        ),
        fr=_loc(
            title="Comment utiliser Lovegobuy",
            description="guide d'utilisation Lovegobuy pour débutants.",
            h1="Comment utiliser Lovegobuy",
            intro="Parcours débutant via W2CLinks et Lovegobuy.",
            sections=[],
            faq=[],
        ),
        nl=_loc(
            title="Hoe Lovegobuy gebruiken",
            description="how to use lovegobuy — stap voor stap.",
            h1="Hoe Lovegobuy gebruiken",
            intro="Beginnersworkflow met W2CLinks en Lovegobuy.",
            sections=[],
            faq=[],
        ),
        fi=_loc(
            title="Miten käyttää Lovegobuyta — Opas",
            description="miten käyttää lovegobuy — vaihe vaiheelta.",
            h1="Miten käyttää Lovegobuyta",
            intro="Aloittelijan työnkulku: W2CLinks → linkki → maksu → QC → toimitus.",
            sections=[],
            faq=[],
        ),
    ),
    # --- ES exclusive ---
    _page(
        "lovegobuy-opiniones",
        regions=["ES"],
        cta=CTA_REGISTER,
        cta_href=REGISTER,
        es=_loc(
            title=f"Lovegobuy Opiniones ({YEAR}) — ¿Es fiable?",
            description="lovegobuy opiniones — reseñas y señales de confianza sin puntuaciones inventadas.",
            h1="Opiniones sobre Lovegobuy",
            intro="Las búsquedas lovegobuy opiniones piden experiencias reales de envío, QC y soporte.",
            sections=[
                ("Fuentes", "Reddit, Discord, comunidades de replicas — compara opiniones recientes."),
                ("Finds primero", f'Compara picks en <a href="{SPREADSHEET}" target="_blank" rel="noopener">W2CLinks</a> antes de pedir.'),
            ],
            faq=[("¿Opiniones oficiales?", "Esta es una guía independiente, no el sitio de Lovegobuy.")],
        ),
    ),
    _page(
        "es-lovegobuy-confiable",
        regions=["ES"],
        cta=CTA_REGISTER,
        cta_href=REGISTER,
        es=_loc(
            title="¿Lovegobuy es confiable? FAQ España",
            description="lovegobuy es confiable — preguntas de confianza para compradores españoles.",
            h1="¿Lovegobuy es confiable?",
            intro="Variante en español de búsquedas is lovegobuy legit / es confiable.",
            sections=[("Señales positivas", "QC público, flujo de almacén documentado, checkout oficial.")],
            faq=[("¿Es seguro comprar?", "Usa Lovegobuy oficial y revisa QC antes de enviar.")],
        ),
    ),
    _page(
        "envio-lovegobuy-espana",
        regions=["ES"],
        cta=CTA_SHIPPING,
        cta_href=SPREADSHEET,
        es=_loc(
            title="Envío Lovegobuy a España — Aduanas y Plazos",
            description="envío lovegobuy españa — DUA, IVA y tiempos de entrega.",
            h1="Envío Lovegobuy a España",
            intro="Guía de envío específica para España: aduanas, IVA y líneas recomendadas.",
            sections=[("Aduanas", "Posibles tasas según valor declarado y línea de envío.")],
            faq=[("¿Cuánto tarda?", "Semanas típicas — depende de línea y temporada.")],
        ),
    ),
    _page(
        "lovegobuy-app",
        regions=["ES"],
        cta=CTA_REGISTER,
        cta_href=REGISTER,
        es=_loc(
            title=f"Lovegobuy App ({YEAR}) — Móvil y registro",
            description="lovegobuy app — búsquedas móviles y pedidos vía Lovegobuy.",
            h1="Lovegobuy App",
            intro="lovegobuy app refleja interés en compras móviles — navega W2CLinks y pega enlaces en Lovegobuy.",
            sections=[("Flujo móvil", "Copiar enlace desde W2CLinks → pegar en Lovegobuy app o web.")],
            faq=[("¿App oficial?", "Verifica en lovegobuy.com — esta guía es web independiente.")],
        ),
    ),
    _page(
        "como-comprar-en-lovegobuy",
        regions=["ES"],
        cta=CTA_REGISTER,
        cta_href=REGISTER,
        es=_loc(
            title=f"Cómo comprar en Lovegobuy ({YEAR})",
            description="como comprar en lovegobuy — guía paso a paso para España.",
            h1="Cómo comprar en Lovegobuy",
            intro="Flujo: W2CLinks → copiar enlace → Lovegobuy → QC → envío internacional.",
            sections=[SEC_SPREADSHEET, SEC_AGENT],
            faq=[],
        ),
    ),
    # --- IT exclusive ---
    _page(
        "lovegobuy-recensioni",
        regions=["IT"],
        cta=CTA_REGISTER,
        cta_href=REGISTER,
        it=_loc(
            title=f"Lovegobuy Recensioni ({YEAR}) — È affidabile?",
            description="lovegobuy recensioni — opinioni e segnali di fiducia.",
            h1="Lovegobuy recensioni",
            intro="Chi cerca lovegobuy recensioni vuole esperienze su spedizione, QC e supporto.",
            sections=[("Fonti", "Reddit e community — confronta thread recenti.")],
            faq=[("È ufficiale?", "Guida indipendente con link W2CLinks.")],
        ),
    ),
    _page(
        "spedizione-lovegobuy",
        regions=["IT"],
        cta=CTA_SHIPPING,
        cta_href=SPREADSHEET,
        it=_loc(
            title="Spedizione Lovegobuy in Italia — Dogane e tempi",
            description="spedizione lovegobuy — IVA e dogana verso l'Italia.",
            h1="Spedizione Lovegobuy in Italia",
            intro="Guida spedizione Italia — linee economy vs express.",
            sections=[("Dogana", "Possibili costi in base al valore dichiarato.")],
            faq=[],
        ),
    ),
    _page(
        "lovegobuy-italia",
        regions=["IT"],
        cta=CTA_REGISTER,
        cta_href=REGISTER,
        it=_loc(
            title="Lovegobuy Italia — Guida acquirenti",
            description="lovegobuy italia — guida per acquirenti italiani.",
            h1="Lovegobuy Italia",
            intro="Risorsa per l'Italia: finds su W2CLinks e ordini su Lovegobuy.",
            sections=[SEC_SPREADSHEET, SEC_AGENT],
            faq=[],
        ),
    ),
    # --- NL exclusive ---
    _page(
        "lovegobuy-ervaringen",
        regions=["NL"],
        cta=CTA_REGISTER,
        cta_href=REGISTER,
        nl=_loc(
            title=f"Lovegobuy Ervaringen ({YEAR}) — Betrouwbaar?",
            description="lovegobuy reviews, is lovegobuy betrouwbaar — ervaringen zonder nep scores.",
            h1="Lovegobuy ervaringen",
            intro="Zoekers willen ervaringen over verzending, QC en support.",
            sections=[("Community", "Reddit r/FashionReps — recente threads.")],
            faq=[("Betrouwbaar?", "Bekende agent — check zelf QC en policies.")],
        ),
    ),
    _page(
        "lovegobuy-verzending",
        regions=["NL"],
        cta=CTA_SHIPPING,
        cta_href=SPREADSHEET,
        nl=_loc(
            title="Lovegobuy Verzending Nederland — BTW en PostNL",
            description="lovegobuy verzending — specifiek voor Nederland.",
            h1="Lovegobuy verzending naar Nederland",
            intro="NL-specifieke verzendgids met BTW 21% context.",
            sections=[("PostNL/DHL", "Vergelijk economy vs express in Lovegobuy.")],
            faq=[("Hoe lang?", "Vaak 2–4 weken of meer — geen vaste belofte.")],
        ),
    ),
    # --- CA exclusive ---
    _page(
        "lovegobuy-canada",
        regions=["CA"],
        cta=CTA_REGISTER,
        cta_href=REGISTER,
        en=_loc(
            title=f"Lovegobuy Canada Guide ({YEAR})",
            description="lovegobuy canada — CAD guide for Canadian buyers using W2CLinks and Lovegobuy.",
            h1="Lovegobuy Canada Guide",
            intro="Canadian buyers browse W2CLinks finds and order through Lovegobuy with CAD-aware planning.",
            sections=[
                ("CAD context", "Verify checkout totals on Lovegobuy — display prices here are illustrative."),
                ("CBSA", "Budget for possible duties depending on declared value."),
            ],
            faq=[("lovegobuy canada shipping?", "See shipping-to-Canada page for line notes.")],
        ),
    ),
    _page(
        "lovegobuy-shipping-to-canada",
        regions=["CA"],
        cta=CTA_SHIPPING,
        cta_href=SPREADSHEET,
        en=_loc(
            title="Lovegobuy Shipping to Canada — CBSA & Delivery",
            description="lovegobuy shipping to canada, how much is lovegobuy shipping — Canadian freight guide.",
            h1="Lovegobuy Shipping to Canada",
            intro="Shipping to Canada after QC approval and parcel submission on Lovegobuy.",
            sections=[
                ("CBSA", "Import charges may apply — economy vs express trade-offs."),
                ("Insurance", "Optional shipping insurance at Lovegobuy checkout."),
            ],
            faq=[
                ("How long to Canada?", "Often several weeks."),
                ("Are duties included?", "Usually not — plan for CBSA assessment."),
            ],
        ),
    ),
    _page(
        "lovegobuy-warehouse",
        regions=["CA"],
        cta=CTA_REGISTER,
        cta_href=REGISTER,
        en=_loc(
            title="Lovegobuy Warehouse — Storage & Parcel Guide",
            description="lovegobuy warehouse — what storing means and how to submit parcels.",
            h1="Lovegobuy Warehouse Workflow",
            intro="Warehouse stage: items arrive, QC, storage window, then international parcel.",
            sections=[("Storing meaning", "Items wait in warehouse until you bundle and pay freight.")],
            faq=[("what does storing mean?", "Holding period before you ship internationally.")],
        ),
    ),
    # --- EU / INT exclusive ---
    _page(
        "lovegobuy-europe",
        regions=["EU"],
        cta=CTA_REGISTER,
        cta_href=REGISTER,
        en=_loc(
            title=f"Lovegobuy Europe Guide ({YEAR})",
            description="lovegobuy europe — EU buyer guide with W2CLinks spreadsheet.",
            h1="Lovegobuy Europe",
            intro="Pan-European English guide for Lovegobuy spreadsheet workflow.",
            sections=[SEC_SPREADSHEET, SEC_AGENT],
            faq=[],
        ),
    ),
    _page(
        "lovegobuy-shipping-eu",
        regions=["EU"],
        cta=CTA_SHIPPING,
        cta_href=SPREADSHEET,
        en=_loc(
            title="Lovegobuy Shipping to Europe — VAT & Customs",
            description="lovegobuy shipping europe — freight and import notes.",
            h1="Lovegobuy Shipping in Europe",
            intro="Compare economy vs express lines when shipping from Lovegobuy warehouse to EU.",
            sections=[("VAT", "IOSS and national import rules vary by country.")],
            faq=[],
        ),
    ),
    _page(
        "lovegobuy-guide",
        regions=["INT"],
        cta=CTA_REGISTER,
        cta_href=REGISTER,
        en=_loc(
            title=f"Lovegobuy Guide ({YEAR}) — Spreadsheet & Agent Workflow",
            description="lovegobuy guide — international resource hub on lovegobuyguide.com.",
            h1="Lovegobuy Guide",
            intro="English hub: browse W2CLinks finds, order on Lovegobuy, read shipping and QC guides.",
            sections=[SEC_SPREADSHEET, SEC_AGENT],
            faq=[],
        ),
    ),
    _page(
        "lovegobuy-spreadsheet-guide",
        regions=["INT"],
        cta=CTA_BROWSE,
        cta_href=SPREADSHEET,
        en=_loc(
            title="Lovegobuy Spreadsheet Guide — W2CLinks Browse",
            description="lovegobuy spreadsheet guide — how to use the live spreadsheet hub.",
            h1="Lovegobuy Spreadsheet Guide",
            intro="Step-by-step spreadsheet browsing before you paste links into Lovegobuy.",
            sections=[SEC_SPREADSHEET],
            faq=[],
        ),
    ),
    # --- Lightweight stubs for remaining common slugs ---
    _page(
        "lovegobuy-spreadsheets",
        cta=CTA_BROWSE,
        cta_href=SPREADSHEET,
        en=_loc(
            title="Lovegobuy Spreadsheets — Plural Search Hub",
            description="lovegobuy spreadsheets — redirects to the main spreadsheet hub on W2CLinks.",
            h1="Lovegobuy Spreadsheets",
            intro="Plural searches map to the same W2CLinks spreadsheet experience.",
            sections=[SEC_SPREADSHEET],
            faq=[],
        ),
    ),
    _page(
        "lovegobuy-finds",
        cta=CTA_BROWSE,
        cta_href=SPREADSHEET,
        en=_loc(
            title="Lovegobuy Finds — Latest Picks",
            description="lovegobuy finds — community product picks on W2CLinks.",
            h1="Lovegobuy Finds",
            intro="Browse trending finds via W2CLinks filters.",
            sections=[SEC_SPREADSHEET],
            faq=[],
        ),
    ),
    _page(
        "lovegobuy-coupons",
        cta=CTA_COUPONS,
        cta_href=REGISTER,
        en=_loc(
            title="Lovegobuy Coupons",
            description="lovegobuy coupons — see coupon codes page.",
            h1="Lovegobuy Coupons",
            intro="Coupon hub — registration and shipping discounts on Lovegobuy.",
            sections=[],
            faq=[],
        ),
    ),
    _page(
        "is-lovegobuy-safe",
        cta=CTA_REGISTER,
        cta_href=REGISTER,
        en=_loc(
            title="Is Lovegobuy Safe?",
            description="is lovegobuy safe — safety checklist for buyers.",
            h1="Is Lovegobuy Safe?",
            intro="Safety means official checkout, QC review, and realistic shipping expectations.",
            sections=[],
            faq=[("is lovegobuy safe?", "Use official Lovegobuy and verify QC photos.")],
        ),
    ),
    _page(
        "lovegobuy-discord",
        cta=CTA_BROWSE,
        cta_href=SPREADSHEET,
        en=_loc(
            title="Lovegobuy Discord & Community",
            description="lovegobuy discord, lovegobuy telegram — community channels.",
            h1="Lovegobuy Discord",
            intro="Community channels are not official customer support — use Lovegobuy help for orders.",
            sections=[],
            faq=[],
        ),
    ),
    _page(
        "lovegobuy-review",
        cta=CTA_REGISTER,
        cta_href=REGISTER,
        en=_loc(
            title="Lovegobuy Review — Independent Guide",
            description="lovegobuy reviews — evaluate QC, shipping, and support.",
            h1="Lovegobuy Review",
            intro="Review-style guide without fabricated star ratings.",
            sections=[],
            faq=[],
        ),
    ),
    _page(
        "lovegobuy-shipping-calculator",
        regions=["CA"],
        cta=CTA_SHIPPING,
        cta_href=SPREADSHEET,
        en=_loc(
            title="Lovegobuy Shipping Calculator Notes",
            description="lovegobuy shipping calculator — how to estimate freight on Lovegobuy.",
            h1="Lovegobuy Shipping Calculator",
            intro="Estimate parcel weight and compare lines inside Lovegobuy before paying freight.",
            sections=[],
            faq=[],
        ),
    ),
    _page(
        "lovegobuy-payment-methods",
        regions=["CA"],
        cta=CTA_REGISTER,
        cta_href=REGISTER,
        en=_loc(
            title="Lovegobuy Payment Methods",
            description="lovegobuy payment methods — checkout options on Lovegobuy.",
            h1="Lovegobuy Payment Methods",
            intro="Payment options vary by region — verify inside Lovegobuy checkout.",
            sections=[],
            faq=[],
        ),
    ),
    _page(
        "lovegobuy-tracking",
        regions=["CA"],
        cta=CTA_REGISTER,
        cta_href=REGISTER,
        en=_loc(
            title="Lovegobuy Tracking Guide",
            description="lovegobuy tracking — how to track parcels after shipping.",
            h1="Lovegobuy Tracking",
            intro="Tracking updates appear in Lovegobuy account after international dispatch.",
            sections=[],
            faq=[],
        ),
    ),
]

PAGE_BY_SLUG: dict[str, dict] = {p["slug"]: p for p in PAGES}


def get_page(slug: str) -> dict | None:
    return PAGE_BY_SLUG.get(slug)


def page_allowed(page: dict, region: str) -> bool:
    regions = page.get("regions")
    if regions is None:
        return True
    return region in regions
