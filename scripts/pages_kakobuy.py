"""Page metadata and localized content for Kakobuy Spreadsheet cluster."""

from __future__ import annotations

from scripts.link_helpers_kakobuy import (
    AGENT_PLATFORM,
    category_url,
    main_spreadsheet_url,
    product_search_url,
)

YEAR = "2026"
SPREADSHEET = main_spreadsheet_url()
PLATFORM = AGENT_PLATFORM["baseUrl"]
REGISTER = AGENT_PLATFORM["registerUrl"]

CTA_SPREADSHEET = "Open Kakobuy Spreadsheet"
CTA_BROWSE = "Browse Spreadsheet"
CTA_COUPONS = "Kakobuy Coupons"
CTA_REGISTER = "Register on Kakobuy"
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
    fi: dict | None = None,
    regions: list[str] | None = None,
) -> dict:
    base = en or es or fr or nl or fi
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
    "Order on Kakobuy",
    f"After you pick a find, paste the seller link on "
    f'<a href="{REGISTER}" target="_blank" rel="noopener">Kakobuy</a> ({PLATFORM}). '
    "Kakobuy purchases from Taobao, 1688, and Weidian, provides QC photos, then ships internationally.",
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
            title=f"Kakobuy Spreadsheet Guide — Finds, Coupons & Shipping ({YEAR})",
            description="Independent Kakobuy spreadsheet guide: browse finds on W2CLinks, coupon tips, shipping and QC basics for global buyers.",
            h1="Kakobuy Spreadsheet: Finds, Coupons and Shipping Guide",
            intro=(
                "Kakobuy is a China shopping agent for Taobao, 1688, and Weidian. "
                "This guide explains spreadsheet-style finds and links you to W2CLinks — not a fake local catalog."
            ),
            sections=[SEC_SPREADSHEET, SEC_AGENT, SEC_CATS],
            faq=[
                ("Is this the official Kakobuy spreadsheet?", "No — independent guide. Spreadsheet links open W2CLinks."),
                ("How do I open the Kakobuy spreadsheet?", f"Use the button above or visit {SPREADSHEET}"),
                ("Does Kakobuy support Taobao and 1688?", "Yes — paste links or search by keyword on Kakobuy."),
            ],
        ),
        es=_loc(
            title=f"Kakobuy Spreadsheet España — Guía, Cupones y Envío ({YEAR})",
            description="Guía independiente de kakobuy spreadsheet: finds en W2CLinks, cupones, envío y QC para compradores en España.",
            h1="Kakobuy Spreadsheet para España",
            intro=(
                "Kakobuy es un agente de compras en China para Taobao, 1688 y Weidian. "
                "Esta guía explica el spreadsheet de finds y enlaza a W2CLinks."
            ),
            sections=[
                (
                    "Explorar finds en W2CLinks",
                    f'El spreadsheet en vivo está en <a href="{SPREADSHEET}" target="_blank" rel="noopener">'
                    "w2clinks.com/spreadsheet/</a>. Filtra por categoría, marca o palabra clave.",
                ),
                (
                    "Pedir en Kakobuy",
                    f'Después de elegir un find, pega el enlace en <a href="{REGISTER}" target="_blank" rel="noopener">Kakobuy</a>.',
                ),
                SEC_CATS,
            ],
            faq=[
                ("¿Es el spreadsheet oficial de Kakobuy?", "No — guía independiente. Los enlaces abren W2CLinks."),
                ("¿Kakobuy es confiable?", "Lee nuestra página de opiniones y la guía de legitimidad."),
                ("¿Cuánto tarda el envío a España?", "Varía según la línea — consulta la guía de envío."),
            ],
        ),
        fr=_loc(
            title=f"Kakobuy Spreadsheet France — Guide, Coupons et Livraison ({YEAR})",
            description="Guide indépendant kakobuy spreadsheet : finds W2CLinks, coupons, livraison et QC pour la France.",
            h1="Kakobuy Spreadsheet pour la France",
            intro=(
                "Kakobuy est un agent d'achat Chine pour Taobao, 1688 et Weidian. "
                "Ce guide explique le tableur de finds via W2CLinks."
            ),
            sections=[
                (
                    "Parcourir les finds sur W2CLinks",
                    f'Le hub spreadsheet : <a href="{SPREADSHEET}" target="_blank" rel="noopener">w2clinks.com/spreadsheet/</a>.',
                ),
                (
                    "Commander sur Kakobuy",
                    f'Collez le lien vendeur sur <a href="{REGISTER}" target="_blank" rel="noopener">Kakobuy</a>.',
                ),
                SEC_CATS,
            ],
            faq=[
                ("Est-ce le spreadsheet officiel ?", "Non — guide indépendant avec liens W2CLinks."),
                ("Kakobuy est-il fiable ?", "Voir notre page avis et la page légitimité."),
                ("Délais livraison France ?", "Variable selon la ligne — voir guide livraison."),
            ],
        ),
        nl=_loc(
            title=f"Kakobuy Spreadsheet Nederland — Gids, Coupons & Verzending ({YEAR})",
            description="Onafhankelijke kakobuy spreadsheet gids: finds op W2CLinks, coupons, verzending en QC voor Nederland.",
            h1="Kakobuy Spreadsheet voor Nederland",
            intro=(
                "Kakobuy is een China shopping agent voor Taobao, 1688 en Weidian. "
                "Deze gids legt spreadsheet/finds uit via W2CLinks."
            ),
            sections=[
                (
                    "Browse finds op W2CLinks",
                    f'Live spreadsheet: <a href="{SPREADSHEET}" target="_blank" rel="noopener">w2clinks.com/spreadsheet/</a>.',
                ),
                (
                    "Bestellen op Kakobuy",
                    f'Plak de verkoperlink op <a href="{REGISTER}" target="_blank" rel="noopener">Kakobuy</a>.',
                ),
                SEC_CATS,
            ],
            faq=[
                ("Is dit het officiële spreadsheet?", "Nee — onafhankelijke gids met W2CLinks-links."),
                ("Is Kakobuy betrouwbaar?", "Zie onze ervaringen-pagina."),
                ("Hoe lang duurt verzending?", "Zie de verzendgids voor NL."),
            ],
        ),
        fi=_loc(
            title=f"Kakobuy Spreadsheet — Opas, Kupongit ja Toimitus ({YEAR})",
            description="Riippumaton Kakobuy spreadsheet -opas: löydöt W2CLinksissä, kupongit, toimitus ja QC suomalaisille ostajille.",
            h1="Kakobuy Spreadsheet — Opas suomalaisille",
            intro=(
                "Kakobuy on Kiinan ostovälittäjä Taobaolle, 1688:lle ja Weidianille. "
                "Tämä opas selittää spreadsheet-löydöt W2CLinks-linkin kautta."
            ),
            sections=[
                (
                    "Selaa löytöjä W2CLinksissä",
                    f'Live-spreadsheet: <a href="{SPREADSHEET}" target="_blank" rel="noopener">w2clinks.com/spreadsheet/</a>.',
                ),
                (
                    "Tilaa Kakobuylta",
                    f'Liitä myyjän linkki <a href="{REGISTER}" target="_blank" rel="noopener">Kakobuyhin</a>.',
                ),
                SEC_CATS,
            ],
            faq=[
                ("Onko tämä virallinen spreadsheet?", "Ei — riippumaton opas, linkit avautuvat W2CLinksissä."),
                ("Onko Kakobuy luotettava?", "Katso kokemukset-sivu."),
                ("Kuinka kauan toimitus kestää?", "Katso toimitusopas Suomeen."),
            ],
        ),
    ),
    _page(
        "kakobuy-spreadsheet",
        cta=CTA_BROWSE,
        cta_href=SPREADSHEET,
        en=_loc(
            title=f"Kakobuy Spreadsheet ({YEAR}) — Browse Finds on W2CLinks",
            description="kakobuy spreadsheet — browse community finds, categories and brands. All product actions open W2CLinks.",
            h1="Kakobuy Spreadsheet",
            intro="Searchers looking for kakobuy spreadsheet want a browsable list of community finds with source links.",
            sections=[SEC_SPREADSHEET, SEC_CATS, SEC_AGENT],
            faq=[
                ("kakobuy spreadsheet vs spreadsheets?", "Same hub — plural searches lead here."),
                ("best kakobuy spreadsheet?", "See our best spreadsheet guide for curated entry points."),
            ],
        ),
        es=_loc(
            title=f"Kakobuy Spreadsheet ({YEAR}) — Tabla de Finds",
            description="kakobuy spreadsheet y spreedsheet — tabla de finds en W2CLinks con categorías y marcas.",
            h1="Kakobuy Spreadsheet",
            intro="Los buscadores de kakobuy spreadsheet quieren una lista navegable de finds con enlaces.",
            sections=[SEC_SPREADSHEET, SEC_CATS, SEC_AGENT],
            faq=[
                ("¿kakobuy spreedsheet?", "Variante ortográfica — mismo spreadsheet en W2CLinks."),
                ("¿Mejor spreadsheet?", "Ver guía best/mejor spreadsheet."),
            ],
        ),
        fr=_loc(
            title=f"Kakobuy Spreadsheet ({YEAR}) — Tableau de Finds",
            description="kakobuy spreadsheet — tableau de finds communautaires sur W2CLinks.",
            h1="Kakobuy Spreadsheet",
            intro="Les recherches kakobuy spreadsheet visent une liste de finds avec liens sources.",
            sections=[SEC_SPREADSHEET, SEC_CATS, SEC_AGENT],
            faq=[("spreadsheet kakobuy ?", "Même hub W2CLinks — ordre des mots différent.")],
        ),
        nl=_loc(
            title=f"Kakobuy Spreadsheet ({YEAR}) — Browse Finds",
            description="kakobuy spreadsheet 2025/2026 — community finds op W2CLinks met filters.",
            h1="Kakobuy Spreadsheet",
            intro="Zoekers naar kakobuy spreadsheet willen een doorbladerbare finds-lijst.",
            sections=[SEC_SPREADSHEET, SEC_CATS, SEC_AGENT],
            faq=[("kakobuy spreadsheet 2025?", "W2CLinks hub wordt doorlopend bijgewerkt.")],
        ),
        fi=_loc(
            title=f"Kakobuy Spreadsheet ({YEAR}) — Löydöt W2CLinksissä",
            description="kakobuy spreadsheet — yhteisön löydöt ja kategoriat W2CLinksissä.",
            h1="Kakobuy Spreadsheet",
            intro="Kakobuy spreadsheet -hakijat haluavat selattavan löytölistan lähdelinkeillä.",
            sections=[SEC_SPREADSHEET, SEC_CATS, SEC_AGENT],
            faq=[("Mikä on Kakobuy spreadsheet?", "W2CLinks-hubi community-löydöille.")],
        ),
    ),
    _page(
        "best-kakobuy-spreadsheet",
        cta=CTA_BROWSE,
        cta_href=SPREADSHEET,
        en=_loc(
            title=f"Best Kakobuy Spreadsheet ({YEAR})",
            description="best kakobuy spreadsheet — how to pick categories, brands and filters on W2CLinks.",
            h1="Best Kakobuy Spreadsheet",
            intro="Commercial intent around the best kakobuy spreadsheet entry points for shoes, hoodies, and bags.",
            sections=[
                ("Top entry points", f'Start at {SPREADSHEET} then filter sneakers, bags, or search Nike/Adidas.'),
                ("Compare before you buy", "Use QC guide and shipping notes before submitting a parcel."),
            ],
            faq=[("Is there one official best list?", "W2CLinks aggregates community finds — compare multiple picks.")],
        ),
        nl=_loc(
            title=f"Beste Kakobuy Spreadsheet ({YEAR})",
            description="best kakobuy spreadsheet / beste kakobuy spreadsheet — KD-laag hangend fruit voor NL.",
            h1="Beste Kakobuy Spreadsheet",
            intro="De zoekterm best kakobuy spreadsheet wijst op curated ingangen voor sneakers en streetwear.",
            sections=[("Startpunten", f'Open {SPREADSHEET} en filter op categorie of merk.')],
            faq=[("Beste spreadsheet 2026?", "W2CLinks hub — filter op nieuwste finds.")],
        ),
        fr=_loc(
            title=f"Meilleur Kakobuy Spreadsheet ({YEAR})",
            description="meilleur kakobuy spreadsheet — points d'entrée sur W2CLinks.",
            h1="Meilleur Kakobuy Spreadsheet",
            intro="Guide pour les recherches commerciales autour du meilleur tableur Kakobuy.",
            sections=[("Entrées recommandées", f'Commencez sur {SPREADSHEET}.')],
            faq=[],
        ),
        es=_loc(
            title=f"Mejor Kakobuy Spreadsheet ({YEAR})",
            description="mejor kakobuy spreadsheet — categorías y marcas en W2CLinks.",
            h1="Mejor Kakobuy Spreadsheet",
            intro="Guía para quienes buscan el mejor punto de entrada al spreadsheet Kakobuy.",
            sections=[("Puntos de entrada", f'Abre {SPREADSHEET} y filtra por categoría.')],
            faq=[],
        ),
        fi=_loc(
            title=f"Paras Kakobuy Spreadsheet ({YEAR})",
            description="paras kakobuy spreadsheet — parhaat aloitus kohdat W2CLinksissä.",
            h1="Paras Kakobuy Spreadsheet",
            intro="Kaupallinen haku parhaaseen Kakobuy spreadsheet -kokemukseen.",
            sections=[("Aloituspisteet", f'Avaa {SPREADSHEET} ja suodata kategorian mukaan.')],
            faq=[],
        ),
    ),
    _page(
        "kakobuy-coupon",
        cta=CTA_COUPONS,
        cta_href=REGISTER,
        en=_loc(
            title=f"Kakobuy Coupon Codes ({YEAR})",
            description="kakobuy coupon codes and coupons — how to apply invitation codes on Kakobuy after browsing W2CLinks.",
            h1="Kakobuy Coupon Codes",
            intro="Coupon searches often mean registration bonuses or shipping discounts on Kakobuy checkout.",
            sections=[
                ("Register with invitation link", f'Use <a href="{REGISTER}" target="_blank" rel="noopener">our Kakobuy registration link</a> for referral benefits.'),
                ("How to apply coupons", "Enter codes during registration or parcel payment — check Kakobuy help for current rules."),
            ],
            faq=[
                ("kakobuy coupon codes?", "Policies change — verify inside Kakobuy account."),
                ("how to use coupons on kakobuy?", "Apply at signup or checkout per Kakobuy UI."),
                ("Multiple coupons?", "Usually one active rule per step — read checkout notes."),
            ],
        ),
        es=_loc(
            title=f"Cupón Kakobuy — Códigos e Invitación ({YEAR})",
            description="cupon kakobuy, kakobuy codes — cómo usar cupones en Kakobuy.",
            h1="Cupón y códigos Kakobuy",
            intro="Las búsquedas de cupon kakobuy suelen referirse a bonos de registro o envío.",
            sections=[("Registro", f'<a href="{REGISTER}" target="_blank" rel="noopener">Enlace de invitación Kakobuy</a>.')],
            faq=[("¿Cómo usar cupones?", "Durante registro o pago del paquete en Kakobuy.")],
        ),
        fr=_loc(
            title=f"Code Promo Kakobuy — Coupons ({YEAR})",
            description="coupon kakobuy, kakobuy coupons — codes et invitation.",
            h1="Coupon et codes Kakobuy",
            intro="Recherches coupon kakobuy pour bonus d'inscription ou réductions.",
            sections=[("Inscription", f'<a href="{REGISTER}" target="_blank" rel="noopener">Lien d\'invitation</a>.')],
            faq=[],
        ),
        nl=_loc(
            title=f"Kakobuy Coupon Code — Kortingscodes ({YEAR})",
            description="kakobuy coupon code, kakobuy coupons — hoe coupon op Kakobuy te gebruiken.",
            h1="Kakobuy coupon en kortingscode",
            intro="Coupon-zoekers willen registratiebonus of verzendkorting.",
            sections=[("Registreren", f'<a href="{REGISTER}" target="_blank" rel="noopener">Kakobuy uitnodigingslink</a>.')],
            faq=[
                ("how to use coupon on kakobuy?", "Bij registratie of afrekenen in Kakobuy."),
                ("Meerdere coupons?", "Meestal één regel per stap."),
            ],
        ),
        fi=_loc(
            title=f"Kakobuy Kuponki ja alennuskoodit ({YEAR})",
            description="kakobuy kuponki — rekisteröitymis- ja alennuskoodit.",
            h1="Kakobuy kuponki",
            intro="Kuponkihaun tarkoitus on usein rekisteröitymisbonus tai toimitusalennus.",
            sections=[("Rekisteröidy", f'<a href="{REGISTER}" target="_blank" rel="noopener">Kakobuy-kutsulinkki</a>.')],
            faq=[("Miten käytän kuponkia?", "Rekisteröinnissä tai maksuvaiheessa Kakobuyssa.")],
        ),
    ),
    _page(
        "kakobuy-shipping",
        cta=CTA_SHIPPING,
        cta_href=SPREADSHEET,
        en=_loc(
            title=f"Kakobuy Shipping — Costs, Calculator & Delivery ({YEAR})",
            description="kakobuy shipping, shipping calculator, delivery times — independent guide with W2CLinks browse first.",
            h1="Kakobuy Shipping Guide",
            intro="Shipping questions cover line selection, weight, insurance, and customs after QC approval.",
            sections=[
                ("Workflow", "Browse W2CLinks → order on Kakobuy → QC photos → submit parcel → choose shipping line."),
                ("Calculator notes", "Estimate weight and compare economy vs express inside Kakobuy before paying freight."),
            ],
            faq=[
                ("how much is kakobuy shipping?", "Depends on weight, line, and destination — quote in Kakobuy."),
                ("how long does kakobuy take to ship?", "Often weeks — no universal guarantee."),
                ("does kakobuy have insurance?", "Optional shipping insurance may be available at checkout."),
            ],
        ),
        es=_loc(
            title=f"Envío Kakobuy — Costes y Plazos ({YEAR})",
            description="envío kakobuy — guía de envío a España con aduanas.",
            h1="Envío Kakobuy",
            intro="Preguntas sobre envío, aduanas españolas y tiempos de entrega.",
            sections=[("Flujo", "W2CLinks → Kakobuy → QC → paquete → línea de envío.")],
            faq=[("¿Cuánto tarda a España?", "Varía según línea y peso.")],
        ),
        fr=_loc(
            title=f"Livraison Kakobuy — Délais et Frais ({YEAR})",
            description="livraison kakobuy — guide livraison France.",
            h1="Livraison Kakobuy",
            intro="Questions sur délais, douanes et choix de ligne vers la France.",
            sections=[("Parcours", "W2CLinks → commande Kakobuy → QC → colis → expédition.")],
            faq=[("Délais France ?", "Variable — comparer lignes économiques et express.")],
        ),
        nl=_loc(
            title=f"Kakobuy Verzending — Calculator en Tijden ({YEAR})",
            description="kakobuy shipping calculator, how long is kakobuy shipping — gids voor Nederland.",
            h1="Kakobuy verzending",
            intro="Verzendvragen: calculator, PostNL/DHL tijden, tracking.",
            sections=[("Calculator", "Schat gewicht en vergelijk lijnen in Kakobuy checkout.")],
            faq=[
                ("how long is kakobuy shipping?", "Vaak meerdere weken — afhankelijk van lijn."),
                ("how to track kakobuy order?", "Tracking in Kakobuy account na verzending."),
            ],
        ),
        fi=_loc(
            title=f"Kakobuy Toimitus — Kustannukset ja Ajat ({YEAR})",
            description="kakobuy toimitus, kakobuy shipping — opas suomalaisille.",
            h1="Kakobuy toimitus",
            intro="Toimituskysymykset: paino, linja, tullit Suomeen.",
            sections=[("Prosessi", "W2CLinks → Kakobuy → QC → paketti → toimituslinja.")],
            faq=[("Kuinka kauan toimitus kestää?", "Useita viikkoja tyypillisesti — riippuu linjasta.")],
        ),
    ),
    _page(
        "is-kakobuy-legit",
        cta=CTA_REGISTER,
        cta_href=REGISTER,
        en=_loc(
            title="Is Kakobuy Legit? Safety Guide for Buyers",
            description="is kakobuy legit, is kakobuy safe, is kakobuy real — trust signals without fake ratings.",
            h1="Is Kakobuy Legit and Safe?",
            intro="Legitimacy searches want QC proof, shipping track record, and payment clarity — not hype.",
            sections=[
                ("What to verify", "QC photos, warehouse timeline, refund policy on Kakobuy help center."),
                ("Red flags", "Unrealistic shipping promises or unofficial payment requests outside Kakobuy."),
            ],
            faq=[
                ("is kakobuy legit?", "Established agent with public QC workflow — do your own due diligence."),
                ("is kakobuy safe?", "Use official Kakobuy checkout and review QC before shipping."),
                ("kakobuy scam?", "Avoid off-platform payments and unverified middlemen."),
            ],
        ),
        es=_loc(
            title="¿Es Kakobuy legítimo? Guía de confianza",
            description="is kakobuy legit, kakobuy es confiable — señales de confianza.",
            h1="¿Es Kakobuy legítimo y seguro?",
            intro="Búsquedas de legitimidad y si kakobuy es confiable.",
            sections=[("Verificar", "Fotos QC, políticas de reembolso, soporte oficial.")],
            faq=[("¿Kakobuy es confiable?", "Agente conocido — revisa QC y políticas actuales.")],
        ),
        fr=_loc(
            title="Kakobuy est-il fiable ? Guide de confiance",
            description="kakobuy avis, kakobuy fiable, is kakobuy legit — guide indépendant.",
            h1="Kakobuy est-il légitime ?",
            intro="Les recherches avis et fiabilité demandent preuves QC et politiques claires.",
            sections=[("Vérifications", "QC, délais, support Kakobuy officiel.")],
            faq=[("Arnaque ?", "Paiements uniquement via Kakobuy officiel.")],
        ),
        nl=_loc(
            title="Is Kakobuy betrouwbaar? Legit gids",
            description="is kakobuy legit, is kakobuy betrouwbaar — onafhankelijke gids.",
            h1="Is Kakobuy legit en betrouwbaar?",
            intro="Trust-zoekopdrachten voor Nederlandse kopers.",
            sections=[("Checklist", "QC-foto's, tracking, refund policy.")],
            faq=[("is kakobuy betrouwbaar?", "Bekende agent — eigen due diligence blijft nodig.")],
        ),
        fi=_loc(
            title="Onko Kakobuy luotettava? Turvallisuusopas",
            description="is kakobuy legit, onko kakobuy luotettava — riippumaton opas.",
            h1="Onko Kakobuy luotettava?",
            intro="Luotettavuushaut — QC, toimitus ja maksutapa.",
            sections=[("Tarkista", "QC-kuvat, virallinen checkout, tuki.")],
            faq=[("Onko Kakobuy huijaus?", "Vältä maksuja alustan ulkopuolella.")],
        ),
    ),
    _page(
        "kakobuy-qc",
        cta=CTA_BROWSE,
        cta_href=SPREADSHEET,
        en=_loc(
            title="Kakobuy QC Photos Guide",
            description="qc kakobuy — quality check photos before international shipping.",
            h1="Kakobuy QC Guide",
            intro="QC photos let you approve items in warehouse before paying international freight.",
            sections=[("QC workflow", "Request photos → review defects → approve or exchange → ship parcel.")],
            faq=[("How many QC photos?", "Typically multiple angles — request more if needed.")],
        ),
        es=_loc(
            title="QC Kakobuy — Fotos de control de calidad",
            description="qc kakobuy — fotos QC antes del envío internacional.",
            h1="Guía QC Kakobuy",
            intro="Las fotos QC permiten revisar el producto en almacén.",
            sections=[("Proceso", "Solicitar fotos → revisar → aprobar → enviar.")],
            faq=[],
        ),
        fr=_loc(
            title="QC Kakobuy — Photos de contrôle qualité",
            description="kakobuy qc — photos avant expédition.",
            h1="Guide QC Kakobuy",
            intro="Les photos QC valident l'article avant frais d'expédition internationale.",
            sections=[],
            faq=[],
        ),
        nl=_loc(
            title="Kakobuy QC — Kwaliteitscontrole foto's",
            description="kakobuy qc — foto's voor internationale verzending.",
            h1="Kakobuy QC gids",
            intro="QC-foto's voor goedkeuring in het magazijn.",
            sections=[],
            faq=[],
        ),
        fi=_loc(
            title="Kakobuy QC — Laatukuvat",
            description="kakobuy qc — laatukuvat ennen kansainvälistä toimitusta.",
            h1="Kakobuy QC-opas",
            intro="QC-kuvat ennen kansainvälisen toimituksen maksamista.",
            sections=[],
            faq=[],
        ),
    ),
    _page(
        "how-to-use-kakobuy",
        cta=CTA_REGISTER,
        cta_href=REGISTER,
        en=_loc(
            title="How to Use Kakobuy — Step-by-Step Guide",
            description="how to use kakobuy, how to buy on kakobuy, how does kakobuy work.",
            h1="How to Use Kakobuy",
            intro="Beginner workflow: browse W2CLinks, paste link, pay, QC, ship.",
            sections=[
                ("Step 1", f'Browse {SPREADSHEET}'),
                ("Step 2", f'Register on <a href="{REGISTER}" target="_blank" rel="noopener">Kakobuy</a> and paste item URL'),
                ("Step 3", "Pay for items, wait for warehouse, review QC, submit parcel."),
            ],
            faq=[("how does kakobuy work?", "Agent buys in China, QC in warehouse, ships to you.")],
        ),
        es=_loc(
            title="Cómo usar Kakobuy — Guía paso a paso",
            description="cómo comprar en kakobuy — tutorial para principiantes.",
            h1="Cómo usar Kakobuy",
            intro="Flujo: W2CLinks → pegar enlace → pagar → QC → enviar.",
            sections=[],
            faq=[],
        ),
        fr=_loc(
            title="Comment utiliser Kakobuy",
            description="guide d'utilisation Kakobuy pour débutants.",
            h1="Comment utiliser Kakobuy",
            intro="Parcours débutant via W2CLinks et Kakobuy.",
            sections=[],
            faq=[],
        ),
        nl=_loc(
            title="Hoe Kakobuy gebruiken",
            description="how to use kakobuy — stap voor stap.",
            h1="Hoe Kakobuy gebruiken",
            intro="Beginnersworkflow met W2CLinks en Kakobuy.",
            sections=[],
            faq=[],
        ),
        fi=_loc(
            title="Miten käyttää Kakobuyta — Opas",
            description="miten käyttää kakobuy — vaihe vaiheelta.",
            h1="Miten käyttää Kakobuyta",
            intro="Aloittelijan työnkulku: W2CLinks → linkki → maksu → QC → toimitus.",
            sections=[],
            faq=[],
        ),
    ),
    # --- ES exclusive ---
    _page(
        "kakobuy-opiniones",
        regions=["ES"],
        cta=CTA_REGISTER,
        cta_href=REGISTER,
        es=_loc(
            title=f"Kakobuy Opiniones ({YEAR}) — ¿Es fiable?",
            description="kakobuy opiniones — reseñas y señales de confianza sin puntuaciones inventadas.",
            h1="Opiniones sobre Kakobuy",
            intro="Las búsquedas kakobuy opiniones piden experiencias reales de envío, QC y soporte.",
            sections=[
                ("Fuentes", "Reddit, Discord, comunidades de replicas — compara opiniones recientes."),
                ("Finds primero", f'Compara picks en <a href="{SPREADSHEET}" target="_blank" rel="noopener">W2CLinks</a> antes de pedir.'),
            ],
            faq=[("¿Opiniones oficiales?", "Esta es una guía independiente, no el sitio de Kakobuy.")],
        ),
    ),
    _page(
        "es-kakobuy-confiable",
        regions=["ES"],
        cta=CTA_REGISTER,
        cta_href=REGISTER,
        es=_loc(
            title="¿Kakobuy es confiable? FAQ España",
            description="kakobuy es confiable — preguntas de confianza para compradores españoles.",
            h1="¿Kakobuy es confiable?",
            intro="Variante en español de búsquedas is kakobuy legit / es confiable.",
            sections=[("Señales positivas", "QC público, flujo de almacén documentado, checkout oficial.")],
            faq=[("¿Es seguro comprar?", "Usa Kakobuy oficial y revisa QC antes de enviar.")],
        ),
    ),
    _page(
        "envio-kakobuy-espana",
        regions=["ES"],
        cta=CTA_SHIPPING,
        cta_href=SPREADSHEET,
        es=_loc(
            title="Envío Kakobuy a España — Aduanas y Plazos",
            description="envío kakobuy españa — DUA, IVA y tiempos de entrega.",
            h1="Envío Kakobuy a España",
            intro="Guía de envío específica para España: aduanas, IVA y líneas recomendadas.",
            sections=[("Aduanas", "Posibles tasas según valor declarado y línea de envío.")],
            faq=[("¿Cuánto tarda?", "Semanas típicas — depende de línea y temporada.")],
        ),
    ),
    _page(
        "kakobuy-app",
        regions=["ES"],
        cta=CTA_REGISTER,
        cta_href=REGISTER,
        es=_loc(
            title=f"Kakobuy App ({YEAR}) — Móvil y registro",
            description="kakobuy app — búsquedas móviles y pedidos vía Kakobuy.",
            h1="Kakobuy App",
            intro="kakobuy app refleja interés en compras móviles — navega W2CLinks y pega enlaces en Kakobuy.",
            sections=[("Flujo móvil", "Copiar enlace desde W2CLinks → pegar en Kakobuy app o web.")],
            faq=[("¿App oficial?", "Verifica en kakobuy.com — esta guía es web independiente.")],
        ),
    ),
    # --- FR exclusive ---
    _page(
        "avis-kakobuy",
        regions=["FR"],
        cta=CTA_REGISTER,
        cta_href=REGISTER,
        fr=_loc(
            title=f"Avis Kakobuy ({YEAR}) — Fiable ou arnaque ?",
            description="kakobuy avis — retours d'expérience et signaux de confiance.",
            h1="Avis sur Kakobuy",
            intro="Recherches kakobuy avis pour la France — expédition, QC, support.",
            sections=[("Sources", "Reddit, Discord — avis récents uniquement.")],
            faq=[("Site officiel ?", "Guide indépendant avec liens W2CLinks.")],
        ),
    ),
    _page(
        "livraison-kakobuy",
        regions=["FR"],
        cta=CTA_SHIPPING,
        cta_href=SPREADSHEET,
        fr=_loc(
            title="Livraison Kakobuy en France — Délais et Douanes",
            description="livraison kakobuy — TVA, douanes et délais vers la France.",
            h1="Livraison Kakobuy en France",
            intro="Guide livraison France — lignes économiques vs express.",
            sections=[("Douanes", "Frais possibles selon valeur déclarée.")],
            faq=[],
        ),
    ),
    _page(
        "kakobuy-france",
        regions=["FR"],
        cta=CTA_REGISTER,
        cta_href=REGISTER,
        fr=_loc(
            title="Kakobuy France — Guide acheteurs",
            description="kakobuy france — guide pour acheteurs français.",
            h1="Kakobuy France",
            intro="Ressource pour acheteurs en France utilisant W2CLinks et Kakobuy.",
            sections=[SEC_SPREADSHEET, SEC_AGENT],
            faq=[],
        ),
    ),
    # --- NL exclusive ---
    _page(
        "kakobuy-ervaringen",
        regions=["NL"],
        cta=CTA_REGISTER,
        cta_href=REGISTER,
        nl=_loc(
            title=f"Kakobuy Ervaringen ({YEAR}) — Betrouwbaar?",
            description="kakobuy reviews, is kakobuy betrouwbaar — ervaringen zonder nep scores.",
            h1="Kakobuy ervaringen",
            intro="Zoekers willen ervaringen over verzending, QC en support.",
            sections=[("Community", "Reddit r/FashionReps — recente threads.")],
            faq=[("Betrouwbaar?", "Bekende agent — check zelf QC en policies.")],
        ),
    ),
    _page(
        "kakobuy-verzending",
        regions=["NL"],
        cta=CTA_SHIPPING,
        cta_href=SPREADSHEET,
        nl=_loc(
            title="Kakobuy Verzending Nederland — BTW en PostNL",
            description="kakobuy verzending — specifiek voor Nederland.",
            h1="Kakobuy verzending naar Nederland",
            intro="NL-specifieke verzendgids met BTW 21% context.",
            sections=[("PostNL/DHL", "Vergelijk economy vs express in Kakobuy.")],
            faq=[("Hoe lang?", "Vaak 2–4 weken of meer — geen vaste belofte.")],
        ),
    ),
    # --- CA exclusive ---
    _page(
        "kakobuy-canada",
        regions=["CA"],
        cta=CTA_REGISTER,
        cta_href=REGISTER,
        en=_loc(
            title=f"Kakobuy Canada Guide ({YEAR})",
            description="kakobuy canada — CAD guide for Canadian buyers using W2CLinks and Kakobuy.",
            h1="Kakobuy Canada Guide",
            intro="Canadian buyers browse W2CLinks finds and order through Kakobuy with CAD-aware planning.",
            sections=[
                ("CAD context", "Verify checkout totals on Kakobuy — display prices here are illustrative."),
                ("CBSA", "Budget for possible duties depending on declared value."),
            ],
            faq=[("kakobuy canada shipping?", "See shipping-to-Canada page for line notes.")],
        ),
    ),
    _page(
        "kakobuy-shipping-to-canada",
        regions=["CA"],
        cta=CTA_SHIPPING,
        cta_href=SPREADSHEET,
        en=_loc(
            title="Kakobuy Shipping to Canada — CBSA & Delivery",
            description="kakobuy shipping to canada, how much is kakobuy shipping — Canadian freight guide.",
            h1="Kakobuy Shipping to Canada",
            intro="Shipping to Canada after QC approval and parcel submission on Kakobuy.",
            sections=[
                ("CBSA", "Import charges may apply — economy vs express trade-offs."),
                ("Insurance", "Optional shipping insurance at Kakobuy checkout."),
            ],
            faq=[
                ("How long to Canada?", "Often several weeks."),
                ("Are duties included?", "Usually not — plan for CBSA assessment."),
            ],
        ),
    ),
    _page(
        "kakobuy-warehouse",
        regions=["CA"],
        cta=CTA_REGISTER,
        cta_href=REGISTER,
        en=_loc(
            title="Kakobuy Warehouse — Storage & Parcel Guide",
            description="kakobuy warehouse — what storing means and how to submit parcels.",
            h1="Kakobuy Warehouse Workflow",
            intro="Warehouse stage: items arrive, QC, storage window, then international parcel.",
            sections=[("Storing meaning", "Items wait in warehouse until you bundle and pay freight.")],
            faq=[("what does storing mean?", "Holding period before you ship internationally.")],
        ),
    ),
    # --- FI exclusive ---
    _page(
        "kakobuy-kokemuksia",
        regions=["FI"],
        cta=CTA_REGISTER,
        cta_href=REGISTER,
        fi=_loc(
            title=f"Kakobuy Kokemuksia ({YEAR}) — Luotettava?",
            description="kakobuy kokemuksia, onko kakobuy luotettava — kokemuksia ilman tekoarvioita.",
            h1="Kakobuy kokemuksia",
            intro="Kokemushaut koskevat toimitusta, QC:tä ja tukea.",
            sections=[("Lähteet", "Reddit-yhteisöt — lue tuoreita ketjuja.")],
            faq=[("Luotettava?", "Tunnettu agentti — tee oma arvio QC:n perusteella.")],
        ),
    ),
    _page(
        "kakobuy-toimitus",
        regions=["FI"],
        cta=CTA_SHIPPING,
        cta_href=SPREADSHEET,
        fi=_loc(
            title="Kakobuy Toimitus Suomeen — Tullit ja Ajat",
            description="kakobuy toimitus — ALV ja tulli Suomessa.",
            h1="Kakobuy toimitus Suomeen",
            intro="Suomeen suunnattu toimitusopas: Posti, tullit, ALV 24%.",
            sections=[("Tulli", "Mahdolliset maksut ilmoitetun arvon mukaan.")],
            faq=[("Kuinka kauan?", "Useita viikkoja tyypillisesti.")],
        ),
    ),
    _page(
        "kakobuy-suomi",
        regions=["FI"],
        cta=CTA_REGISTER,
        cta_href=REGISTER,
        fi=_loc(
            title="Kakobuy Suomi — Opas ostajille",
            description="kakobuy suomi — suomalainen ostajan opas.",
            h1="Kakobuy Suomi",
            intro="Suomalaisille ostajille: W2CLinks-löydöt ja Kakobuy-tilaukset.",
            sections=[SEC_SPREADSHEET, SEC_AGENT],
            faq=[],
        ),
    ),
    # --- Lightweight stubs for remaining common slugs ---
    _page(
        "kakobuy-spreadsheets",
        cta=CTA_BROWSE,
        cta_href=SPREADSHEET,
        en=_loc(
            title="Kakobuy Spreadsheets — Plural Search Hub",
            description="kakobuy spreadsheets — redirects to the main spreadsheet hub on W2CLinks.",
            h1="Kakobuy Spreadsheets",
            intro="Plural searches map to the same W2CLinks spreadsheet experience.",
            sections=[SEC_SPREADSHEET],
            faq=[],
        ),
    ),
    _page(
        "kakobuy-finds",
        cta=CTA_BROWSE,
        cta_href=SPREADSHEET,
        en=_loc(
            title="Kakobuy Finds — Latest Picks",
            description="kakobuy finds — community product picks on W2CLinks.",
            h1="Kakobuy Finds",
            intro="Browse trending finds via W2CLinks filters.",
            sections=[SEC_SPREADSHEET],
            faq=[],
        ),
    ),
    _page(
        "kakobuy-coupons",
        cta=CTA_COUPONS,
        cta_href=REGISTER,
        en=_loc(
            title="Kakobuy Coupons",
            description="kakobuy coupons — see coupon codes page.",
            h1="Kakobuy Coupons",
            intro="Coupon hub — registration and shipping discounts on Kakobuy.",
            sections=[],
            faq=[],
        ),
    ),
    _page(
        "is-kakobuy-safe",
        cta=CTA_REGISTER,
        cta_href=REGISTER,
        en=_loc(
            title="Is Kakobuy Safe?",
            description="is kakobuy safe — safety checklist for buyers.",
            h1="Is Kakobuy Safe?",
            intro="Safety means official checkout, QC review, and realistic shipping expectations.",
            sections=[],
            faq=[("is kakobuy safe?", "Use official Kakobuy and verify QC photos.")],
        ),
    ),
    _page(
        "kakobuy-discord",
        cta=CTA_BROWSE,
        cta_href=SPREADSHEET,
        en=_loc(
            title="Kakobuy Discord & Community",
            description="kakobuy discord, kakobuy telegram — community channels.",
            h1="Kakobuy Discord",
            intro="Community channels are not official customer support — use Kakobuy help for orders.",
            sections=[],
            faq=[],
        ),
    ),
    _page(
        "kakobuy-review",
        cta=CTA_REGISTER,
        cta_href=REGISTER,
        en=_loc(
            title="Kakobuy Review — Independent Guide",
            description="kakobuy reviews — evaluate QC, shipping, and support.",
            h1="Kakobuy Review",
            intro="Review-style guide without fabricated star ratings.",
            sections=[],
            faq=[],
        ),
    ),
    _page(
        "kakobuy-shipping-calculator",
        regions=["CA"],
        cta=CTA_SHIPPING,
        cta_href=SPREADSHEET,
        en=_loc(
            title="Kakobuy Shipping Calculator Notes",
            description="kakobuy shipping calculator — how to estimate freight on Kakobuy.",
            h1="Kakobuy Shipping Calculator",
            intro="Estimate parcel weight and compare lines inside Kakobuy before paying freight.",
            sections=[],
            faq=[],
        ),
    ),
    _page(
        "kakobuy-payment-methods",
        regions=["CA"],
        cta=CTA_REGISTER,
        cta_href=REGISTER,
        en=_loc(
            title="Kakobuy Payment Methods",
            description="kakobuy payment methods — checkout options on Kakobuy.",
            h1="Kakobuy Payment Methods",
            intro="Payment options vary by region — verify inside Kakobuy checkout.",
            sections=[],
            faq=[],
        ),
    ),
    _page(
        "kakobuy-tracking",
        regions=["CA"],
        cta=CTA_REGISTER,
        cta_href=REGISTER,
        en=_loc(
            title="Kakobuy Tracking Guide",
            description="kakobuy tracking — how to track parcels after shipping.",
            h1="Kakobuy Tracking",
            intro="Tracking updates appear in Kakobuy account after international dispatch.",
            sections=[],
            faq=[],
        ),
    ),
    _page(
        "meilleur-kakobuy-spreadsheet",
        regions=["FR"],
        cta=CTA_BROWSE,
        cta_href=SPREADSHEET,
        fr=_loc(
            title=f"Meilleur Kakobuy Spreadsheet ({YEAR})",
            description="meilleur kakobuy spreadsheet — entrées recommandées W2CLinks.",
            h1="Meilleur Kakobuy Spreadsheet",
            intro="Page commerciale FR — synonyme de best spreadsheet.",
            sections=[SEC_SPREADSHEET],
            faq=[],
        ),
    ),
    _page(
        "kakobuy-lululemon",
        regions=["FR"],
        cta=CTA_BROWSE,
        cta_href=product_search_url("lululemon"),
        fr=_loc(
            title="Kakobuy Lululemon Finds",
            description="kakobuy lululemon — browse Lululemon finds on W2CLinks.",
            h1="Kakobuy Lululemon Spreadsheet",
            intro="FR searches for Lululemon finds via Kakobuy spreadsheet workflow.",
            sections=[SEC_SPREADSHEET],
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
