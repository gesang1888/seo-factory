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
            description=(
                "Independent Lovegobuy spreadsheet guide: browse community finds on W2CLinks, "
                "$137 new-user coupons, shipping lines, QC workflow and invite code W5RJX3."
            ),
            h1="Lovegobuy Spreadsheet: Finds, Coupons and Shipping Guide",
            intro=(
                "Lovegobuy is a China shopping agent for Taobao, 1688, and Weidian. "
                "This partner guide explains spreadsheet-style finds on W2CLinks, how to register with invite W5RJX3, "
                "and when to read QC photos before international shipping — not a fake local product catalog."
            ),
            sections=[
                SEC_SPREADSHEET,
                SEC_AGENT,
                SEC_CATS,
                (
                    "New-user coupons and registration",
                    f'Lovegobuy.com promotes a $137 coupon pack for new accounts — amounts change with campaigns. '
                    f'Browse finds on <a href="{SPREADSHEET}" target="_blank" rel="noopener">W2CLinks</a> first, then register via '
                    f'<a href="{REGISTER}" target="_blank" rel="sponsored noopener">invite W5RJX3</a> and confirm live bonuses in your wallet.',
                ),
                (
                    "Shipping, QC and trust guides",
                    'After warehouse inbound, review QC photos before submitting a parcel. '
                    'See <a href="/lovegobuy-shipping/">shipping</a>, '
                    '<a href="/lovegobuy-qc/">QC</a>, '
                    '<a href="/is-lovegobuy-legit/">legitimacy</a> and '
                    '<a href="/how-to-use-lovegobuy/">how to use Lovegobuy</a> for step-by-step notes.',
                ),
            ],
            faq=[
                ("Is this the official Lovegobuy spreadsheet?", "No — independent partner guide. Spreadsheet links open W2CLinks."),
                ("How do I open the Lovegobuy spreadsheet?", f"Use the button above or visit {SPREADSHEET} — filter by category or brand."),
                ("Does Lovegobuy support Taobao and 1688?", "Yes — paste seller links or search by keyword on Lovegobuy."),
                ("lovegobuy spreadsheet vs spreadsheets?", "Same W2CLinks hub — plural searches lead to the spreadsheet page."),
                ("Where is the international hub?", "lovegobuyguide.com is the English x-default; country domains mirror locale guides."),
            ],
        ),
        es=_loc(
            title=f"Lovegobuy Spreadsheet España — Guía, Cupones y Envío ({YEAR})",
            description=(
                "Guía lovegobuy spreadsheet para España: finds en W2CLinks, cupón $137, código W5RJX3, "
                "opiniones, envío y QC para compradores españoles."
            ),
            h1="Lovegobuy Spreadsheet para España",
            intro=(
                "Lovegobuy es un agente de compras en China para Taobao, 1688 y Weidian. "
                "Esta guía partner explica el spreadsheet de finds en W2CLinks, registro con invitación W5RJX3 "
                "y el flujo QC → envío internacional hacia España."
            ),
            sections=[
                (
                    "Explorar finds en W2CLinks",
                    f'El spreadsheet en vivo está en <a href="{SPREADSHEET}" target="_blank" rel="noopener">'
                    "w2clinks.com/spreadsheet/</a>. Filtra por categoría, marca o palabra clave — "
                    "no es un catálogo local falso.",
                ),
                (
                    "Registro y cupones en España",
                    f'Explora finds, luego regístrate con '
                    f'<a href="{REGISTER}" target="_blank" rel="sponsored noopener">invite W5RJX3</a>. '
                    "Lovegobuy.com promociona pack de cupones para nuevos usuarios (p. ej. $137) — verifica en tu cuenta.",
                ),
                (
                    "Pedir en Lovegobuy",
                    f'Pega el enlace del vendedor en <a href="{REGISTER}" target="_blank" rel="noopener">Lovegobuy</a> '
                    f"({PLATFORM}), revisa fotos QC en almacén y solo entonces crea el paquete internacional.",
                ),
                SEC_CATS,
                (
                    "Guías relacionadas en español",
                    'Lee <a href="/lovegobuy-opiniones/">opiniones</a>, '
                    '<a href="/es-lovegobuy-confiable/">¿es confiable?</a>, '
                    '<a href="/lovegobuy-coupon/">cupones</a>, '
                    '<a href="/envio-lovegobuy-espana/">envío a España</a> y '
                    '<a href="/como-comprar-en-lovegobuy/">cómo comprar</a>.',
                ),
            ],
            faq=[
                ("¿Es el spreadsheet oficial de Lovegobuy?", "No — guía partner independiente. Los enlaces abren W2CLinks."),
                ("¿Lovegobuy es confiable?", "Lee opiniones y la página es-lovegobuy-confiable — usa solo checkout oficial."),
                ("¿Cuánto tarda el envío a España?", "Semanas según línea y aduanas — consulta envio-lovegobuy-espana."),
                ("¿lovegobuy spreedsheet?", "Variante ortográfica — mismo hub W2CLinks."),
                ("¿Cómo usar cupones?", "Durante registro o pago del paquete — ver lovegobuy-coupon."),
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
            description=(
                "lovegobuy spreadsheet gids voor NL: W2CLinks finds, coupon W5RJX3, $137 pakket, "
                "verzending, QC en ervaringen voor Nederlandse kopers."
            ),
            h1="Lovegobuy Spreadsheet voor Nederland",
            intro=(
                "Lovegobuy is een China shopping agent voor Taobao, 1688 en Weidian. "
                "Deze partner-gids legt spreadsheet/finds uit via W2CLinks, registratie met W5RJX3 "
                "en het QC → internationale verzending pad naar Nederland."
            ),
            sections=[
                (
                    "Browse finds op W2CLinks",
                    f'Live spreadsheet: <a href="{SPREADSHEET}" target="_blank" rel="noopener">w2clinks.com/spreadsheet/</a> — '
                    "filter op categorie, merk of zoekwoord. Geen nep-inventaris op deze site.",
                ),
                (
                    "Registratie en coupons",
                    f'Browse eerst op W2CLinks, registreer via '
                    f'<a href="{REGISTER}" target="_blank" rel="sponsored noopener">invite W5RJX3</a> '
                    "en controleer het $137 couponpakket (bedragen wijzigen) in je Lovegobuy-wallet.",
                ),
                (
                    "Bestellen op Lovegobuy",
                    f'Plak de verkoperlink op <a href="{REGISTER}" target="_blank" rel="noopener">Lovegobuy</a>, '
                    "bekijk QC-foto's in het magazijn en dien daarna het pakket in.",
                ),
                SEC_CATS,
                (
                    "Verder lezen op deze site",
                    'Zie <a href="/best-lovegobuy-spreadsheet/">best spreadsheet</a>, '
                    '<a href="/lovegobuy-ervaringen/">ervaringen</a>, '
                    '<a href="/lovegobuy-verzending/">verzending NL</a>, '
                    '<a href="/lovegobuy-coupon/">coupon</a> en '
                    '<a href="/is-lovegobuy-legit/">betrouwbaarheid</a>.',
                ),
            ],
            faq=[
                ("Is dit het officiële spreadsheet?", "Nee — onafhankelijke partner-gids; productlinks openen W2CLinks."),
                ("Is Lovegobuy betrouwbaar?", "Lees lovegobuy-ervaringen en is-lovegobuy-legit — gebruik alleen officieel dashboard."),
                ("Hoe lang duurt verzending naar NL?", "Vaak meerdere weken — zie lovegobuy-verzending voor PostNL/DHL context."),
                ("lovegobuy spreadsheet 2025/2026?", "W2CLinks-hub wordt doorlopend bijgewerkt — sorteer op newest."),
                ("BTW en invoer?", "Coupons vervangen geen invoer/BTW — budget apart naast kortingen."),
            ],
        ),
        it=_loc(
            title=f"Lovegobuy Spreadsheet Italia — Guida, Coupon e Spedizione ({YEAR})",
            description=(
                "lovegobuy spreadsheet per l'Italia: finds su W2CLinks, coupon $137, codice W5RJX3, "
                "recensioni, spedizione e QC per acquirenti italiani."
            ),
            h1="Lovegobuy Spreadsheet per l'Italia",
            intro=(
                "Lovegobuy è un agente di acquisti dalla Cina per Taobao, 1688 e Weidian. "
                "Questa guida partner spiega il spreadsheet di finds su W2CLinks, registrazione con W5RJX3 "
                "e il flusso QC → spedizione internazionale verso l'Italia."
            ),
            sections=[
                (
                    "Sfoglia finds su W2CLinks",
                    f'Lo spreadsheet live è su <a href="{SPREADSHEET}" target="_blank" rel="noopener">'
                    "w2clinks.com/spreadsheet/</a> — filtra per categoria, brand o parola chiave.",
                ),
                (
                    "Registrazione e coupon",
                    f'Esplora i finds, poi registrati con '
                    f'<a href="{REGISTER}" target="_blank" rel="sponsored noopener">invite W5RJX3</a>. '
                    "Lovegobuy.com promuove un pacchetto coupon per nuovi utenti (es. $137) — verifica nel wallet.",
                ),
                (
                    "Ordina su Lovegobuy",
                    f'Incolla il link venditore su <a href="{REGISTER}" target="_blank" rel="noopener">Lovegobuy</a> '
                    f"({PLATFORM}), controlla le foto QC in magazzino e poi crea il pacco internazionale.",
                ),
                SEC_CATS,
                (
                    "Guide correlate in italiano",
                    'Leggi <a href="/lovegobuy-recensioni/">recensioni</a>, '
                    '<a href="/spedizione-lovegobuy/">spedizione Italia</a>, '
                    '<a href="/lovegobuy-coupon/">coupon</a> e '
                    '<a href="/how-to-use-lovegobuy/">guida principianti</a>.',
                ),
            ],
            faq=[
                ("È lo spreadsheet ufficiale Lovegobuy?", "No — guida partner indipendente; i link aprono W2CLinks."),
                ("Lovegobuy è affidabile?", "Vedi lovegobuy-recensioni e usa solo checkout su lovegobuy.com."),
                ("Quanto ci mette la spedizione in Italia?", "Settimane tipiche — dipende da linea e dogana."),
                ("lovegobuy spreadsheet 2026?", "Hub W2CLinks aggiornato — ordina per newest."),
                ("Come usare i coupon?", "Alla registrazione o al pagamento del pacco — vedi lovegobuy-coupon."),
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
            description=(
                "lovegobuy spreadsheet — browse community finds, categories and brands on W2CLinks. "
                "Canada, international and EU buyers: paste links into Lovegobuy after QC review."
            ),
            h1="Lovegobuy Spreadsheet",
            intro=(
                "Searchers looking for lovegobuy spreadsheet want a live, filterable browse hub — not a static Excel file. "
                "This page routes every product action to W2CLinks and explains the Lovegobuy order path after you pick a find."
            ),
            sections=[
                SEC_SPREADSHEET,
                SEC_CATS,
                SEC_AGENT,
                (
                    "Workflow after you pick a find",
                    "Copy the seller URL from W2CLinks → paste into Lovegobuy → pay → wait for warehouse inbound → "
                    "review QC photos → submit parcel with a shipping line. Skipping QC is the most common first-order mistake.",
                ),
                (
                    "Related guides",
                    'Home hub: <a href="/">spreadsheet guide</a>. '
                    'Trust: <a href="/is-lovegobuy-legit/">is Lovegobuy legit</a>. '
                    'Savings: <a href="/lovegobuy-coupon/">coupons</a>. '
                    'Canada: <a href="/lovegobuy-canada/">Canada notes</a>.',
                ),
            ],
            faq=[
                ("lovegobuy spreadsheet vs spreadsheets?", "Same W2CLinks hub — plural searches lead here."),
                ("best lovegobuy spreadsheet?", "See best-lovegobuy-spreadsheet for curated entry points and filters."),
                ("spreadsheet lovegobuy keyword order?", "Same intent — open W2CLinks and sort by newest."),
                ("Does this page host products?", "No — independent guide; checkout happens on Lovegobuy."),
            ],
        ),
        es=_loc(
            title=f"Lovegobuy Spreadsheet ({YEAR}) — Tabla de Finds en W2CLinks",
            description=(
                "lovegobuy spreadsheet y spreedsheet — tabla de finds en W2CLinks con categorías, marcas "
                "y flujo Lovegobuy para España."
            ),
            h1="Lovegobuy Spreadsheet",
            intro=(
                "Los buscadores de lovegobuy spreadsheet quieren un hub vivo con filtros — no un Excel estático. "
                "Esta página envía cada acción de producto a W2CLinks y explica el pedido en Lovegobuy tras elegir un find."
            ),
            sections=[
                SEC_SPREADSHEET,
                SEC_CATS,
                SEC_AGENT,
                (
                    "Flujo tras elegir un find",
                    "Copia URL del vendedor → pega en Lovegobuy → paga → inbound en almacén → fotos QC → paquete internacional.",
                ),
                (
                    "Enlaces útiles",
                    '<a href="/">guía principal</a>, '
                    '<a href="/lovegobuy-opiniones/">opiniones</a>, '
                    '<a href="/es-lovegobuy-confiable/">confiable</a>, '
                    '<a href="/lovegobuy-coupon/">cupones</a>.',
                ),
            ],
            faq=[
                ("¿lovegobuy spreedsheet?", "Variante ortográfica — mismo spreadsheet en W2CLinks."),
                ("¿Mejor spreadsheet?", "Ver best-lovegobuy-spreadsheet o filtra por newest en W2CLinks."),
                ("¿spreadsheet lovegobuy?", "Mismo intent — orden de palabras distinto."),
                ("¿Esta página vende productos?", "No — guía partner; checkout en Lovegobuy."),
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
            title=f"Lovegobuy Spreadsheet ({YEAR}) — Browse Finds op W2CLinks",
            description=(
                "lovegobuy spreadsheet 2025/2026 — community finds op W2CLinks met filters, "
                "Lovegobuy-workflow en links naar best spreadsheet / ervaringen."
            ),
            h1="Lovegobuy Spreadsheet",
            intro=(
                "Zoekers naar lovegobuy spreadsheet willen een live hub met categorie- en merkfilters — "
                "niet een statische download. Deze pagina stuurt elke productactie naar W2CLinks."
            ),
            sections=[
                SEC_SPREADSHEET,
                SEC_CATS,
                SEC_AGENT,
                (
                    "Workflow na je find",
                    "Kopieer verkoper-URL → plak in Lovegobuy → betaal → inbound magazijn → QC-foto's → internationaal pakket.",
                ),
                (
                    "Gerelateerde pagina's",
                    '<a href="/best-lovegobuy-spreadsheet/">best spreadsheet</a>, '
                    '<a href="/lovegobuy-ervaringen/">ervaringen</a>, '
                    '<a href="/lovegobuy-verzending/">verzending</a>.',
                ),
            ],
            faq=[
                ("lovegobuy spreadsheet 2025/2026?", "W2CLinks-hub wordt doorlopend bijgewerkt — sorteer op newest."),
                ("best lovegobuy spreadsheet?", "Zie /best-lovegobuy-spreadsheet/ voor NL entry points."),
                ("spreadsheet lovegobuy?", "Zelfde intent — andere woordvolgorde."),
                ("Host deze pagina producten?", "Nee — partner-gids; checkout op Lovegobuy."),
            ],
        ),
        it=_loc(
            title=f"Lovegobuy Spreadsheet ({YEAR}) — Finds su W2CLinks",
            description=(
                "lovegobuy spreadsheet — finds community su W2CLinks con filtri, "
                "workflow Lovegobuy e link a recensioni/spedizione Italia."
            ),
            h1="Lovegobuy Spreadsheet",
            intro=(
                "Chi cerca lovegobuy spreadsheet vuole un hub live con filtri — non un file Excel statico. "
                "Questa pagina indirizza ogni azione prodotto verso W2CLinks."
            ),
            sections=[
                SEC_SPREADSHEET,
                SEC_CATS,
                SEC_AGENT,
                (
                    "Workflow dopo il find",
                    "Copia URL venditore → incolla su Lovegobuy → paga → inbound magazzino → foto QC → pacco internazionale.",
                ),
                (
                    "Guide correlate",
                    '<a href="/">guida home</a>, '
                    '<a href="/lovegobuy-recensioni/">recensioni</a>, '
                    '<a href="/spedizione-lovegobuy/">spedizione</a>, '
                    '<a href="/lovegobuy-coupon/">coupon</a>.',
                ),
            ],
            faq=[
                ("lovegobuy spreadsheet 2026?", "Hub W2CLinks aggiornato — ordina per newest."),
                ("spreadsheet lovegobuy?", "Stesso intent — ordine parole diverso."),
                ("Questa pagina vende prodotti?", "No — guida partner; checkout su Lovegobuy."),
                ("Miglior spreadsheet?", "Filtra per categoria su W2CLinks o leggi la home guide."),
            ],
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
            title=f"Beste Lovegobuy Spreadsheet {YEAR} — NL Gids & W2CLinks",
            description="Beste Lovegobuy spreadsheet voor Nederland: sneakers, hoodies en bags op W2CLinks. Filter, vergelijk QC en bestel via Lovegobuy.",
            h1="Beste Lovegobuy Spreadsheet voor Nederland",
            intro=(
                "Zoek je de beste Lovegobuy spreadsheet voor NL? Start op W2CLinks met newest-sortering, "
                "filter op sneakers of merken zoals Nike en Adidas, en rond af op Lovegobuy met QC en verzending."
            ),
            sections=[
                (
                    "Waarom W2CLinks de beste ingang is",
                    f'Er is geen enkele officiële Excel-lijst — de beste Lovegobuy spreadsheet-ervaring is de live hub op '
                    f'<a href="{SPREADSHEET}" target="_blank" rel="noopener">W2CLinks</a>: categorieën, merken en keyword-zoek.',
                ),
                (
                    "Topcategorieën voor NL-kopers",
                    f'Begin met <a href="{category_url("SNEAKERS")}" target="_blank" rel="noopener">SNEAKERS</a>, '
                    f'<a href="{category_url("HOODIES")}" target="_blank" rel="noopener">HOODIES</a> of '
                    f'<a href="{category_url("BAGS")}" target="_blank" rel="noopener">BAGS</a>. '
                    "Sorteer op newest en vergelijk meerdere finds voordat je betaalt.",
                ),
                (
                    "Registreren en bestellen",
                    f'Na het kiezen van een find: registreer op Lovegobuy via '
                    f'<a href="{REGISTER}" target="_blank" rel="sponsored noopener">invite W5RJX3</a>, '
                    "plak de seller-link, controleer QC-foto's en kies daarna een verzendlijn naar Nederland.",
                ),
            ],
            faq=[
                (
                    "Wat is de beste Lovegobuy spreadsheet in 2026?",
                    "Voor Nederlandse kopers is de W2CLinks-hub met filters en newest-sort de meest praktische ingang — geen statische download.",
                ),
                (
                    "Is best lovegobuy spreadsheet betrouwbaar?",
                    "Finds zijn community-curated; controleer altijd QC, verkoper en gewicht vóór internationale verzending.",
                ),
                (
                    "Hoe lang duurt verzending naar NL?",
                    "Hangt af van lijn en gewicht — zie onze verzendgids; combineer lichte items om kosten te spreiden.",
                ),
            ],
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
            title=f"Lovegobuy Coupon Codes ({YEAR}) — Canada & International",
            description="lovegobuy coupon codes for Canadian buyers: $137 new-user pack, invite W5RJX3, and how to apply coupons after W2CLinks browsing.",
            h1="Lovegobuy Coupon Codes",
            intro=(
                "Searches for lovegobuy coupon codes usually mean registration bonuses (e.g. the current $137 new-user "
                "pack on Lovegobuy.com) or shipping-stage discounts — always confirm live rules in your dashboard."
            ),
            sections=[
                (
                    "Register with invitation link",
                    f'Open finds on <a href="{SPREADSHEET}" target="_blank" rel="noopener">W2CLinks</a>, then register via '
                    f'<a href="{REGISTER}" target="_blank" rel="sponsored noopener">invite code W5RJX3</a> before checkout.',
                ),
                (
                    "Canada-specific notes",
                    "Coupons reduce fees but rarely eliminate customs or GST/HST on import. Budget parcel weight and line "
                    "choice separately — see our Canada shipping and legit guides for CBSA context.",
                ),
                (
                    "How to apply coupons",
                    "Enter eligible codes during registration or international parcel payment. "
                    "Stale Reddit codes may not work — verify inside Lovegobuy before paying.",
                ),
            ],
            faq=[
                ("lovegobuy coupon codes?", "Campaign amounts change — check Lovegobuy wallet after registering with W5RJX3."),
                ("how to use coupons on lovegobuy?", "Apply at signup or parcel step per on-screen prompts."),
                ("lovegobuy coupon codes Canada?", "Same account rules; import taxes are separate from coupon savings."),
                ("Multiple coupons?", "Usually one active rule per step — read checkout notes."),
            ],
        ),
        es=_loc(
            title=f"Cupón Lovegobuy {YEAR} — Códigos, Invitación y España",
            description="cupon lovegobuy y lovegobuy coupon: pack $137, código W5RJX3 y cómo aplicar cupones tras buscar en W2CLinks.",
            h1="Cupón y códigos Lovegobuy",
            intro=(
                "Las búsquedas cupon lovegobuy y lovegobuy coupon en España suelen mezclar bonos de registro, "
                "descuentos de envío y códigos de invitación — verifica siempre en tu cuenta Lovegobuy."
            ),
            sections=[
                (
                    "Registro con invitación",
                    f'Explora finds en <a href="{SPREADSHEET}" target="_blank" rel="noopener">W2CLinks</a> y regístrate con '
                    f'<a href="{REGISTER}" target="_blank" rel="sponsored noopener">invite W5RJX3</a>.',
                ),
                (
                    "Pack de cupones actual",
                    "Lovegobuy.com promociona un pack de cupones para nuevos usuarios (p. ej. $137) — importes y elegibilidad cambian.",
                ),
                (
                    "Cupón vs aduanas",
                    "Un cupón no sustituye posibles tasas de importación en España — revisa IVA y DUA en la guía de envío.",
                ),
            ],
            faq=[
                ("¿Cómo usar cupones en Lovegobuy?", "Durante registro o pago del paquete internacional."),
                ("¿lovegobuy es confiable con cupones?", "Usa solo checkout oficial — evita códigos de terceros no verificados."),
                ("¿Puedo combinar varios cupones?", "Normalmente una regla activa por paso."),
            ],
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
            title=f"Lovegobuy Coupon Code Nederland — Kortingscodes ({YEAR})",
            description=(
                "lovegobuy coupon code en lovegobuy coupons voor NL: $137 pakket, invite W5RJX3, "
                "hoe coupon te gebruiken na W2CLinks browse en BTW/invoer context."
            ),
            h1="Lovegobuy coupon en kortingscode",
            intro=(
                "Coupon-zoekers in Nederland willen registratiebonus (bijv. $137 pakket op Lovegobuy.com), "
                "verzendkorting of invite-code W5RJX3 — controleer altijd live regels in je dashboard, "
                "niet verouderde Reddit-codes."
            ),
            sections=[
                (
                    "Browse eerst, registreer daarna",
                    f'Shortlist finds op <a href="{SPREADSHEET}" target="_blank" rel="noopener">W2CLinks</a>, '
                    f'registreer via <a href="{REGISTER}" target="_blank" rel="sponsored noopener">invite W5RJX3</a> '
                    "en bevestig het couponpakket in je Lovegobuy-wallet vóór betaling.",
                ),
                (
                    "$137 new-user pakket",
                    "Lovegobuy.com promoot een $137 couponpakket voor nieuwe accounts — bedragen en voorwaarden wijzigen per campagne. "
                    "Oudere threads kunnen andere bedragen noemen; vertrouw alleen je live account.",
                ),
                (
                    "NL: coupon vs BTW/invoer",
                    "Coupons verlagen fees of verzendkosten maar elimineren zelden invoer/BTW bij import naar Nederland. "
                    "Budget gewicht en verzendlijn apart — zie <a href=\"/lovegobuy-verzending/\">verzendgids</a> "
                    "en <a href=\"/lovegobuy-ervaringen/\">ervaringen</a>.",
                ),
                (
                    "Hoe coupon toepassen",
                    "Voer in aanmerking komende codes in bij registratie of internationale pakketbetaling. "
                    "Meestal één actieve regel per stap — lees checkout-meldingen in Lovegobuy.",
                ),
            ],
            faq=[
                ("how to use coupon on lovegobuy?", "Bij registratie of pakketbetaling — volg prompts in Lovegobuy dashboard."),
                ("lovegobuy coupon code Nederland?", "Zelfde accountregels als internationaal; importkosten zijn apart."),
                ("Meerdere coupons?", "Meestal één regel per stap — geen stacken zonder bevestiging."),
                ("Is W5RJX3 veilig?", "Officiële invite-link naar lovegobuy.com — geen betalingen buiten platform."),
                ("Coupon na W2CLinks browse?", "Ja — browse eerst, registreer daarna zodat je weet wat je bestelt."),
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
            title="Is Lovegobuy Legit? Canada & International Safety Guide",
            description="is lovegobuy legit, is lovegobuy safe, is lovegobuy real — QC workflow, payments and Canada import context.",
            h1="Is Lovegobuy Legit and Safe?",
            intro=(
                "Legitimacy searches want proof: QC photos, warehouse tracking, official checkout, and realistic customs "
                "expectations — especially for Canada where CBSA screening adds time beyond agent processing."
            ),
            sections=[
                (
                    "What to verify before shipping",
                    "QC photos from multiple angles, warehouse inbound status, refund/exchange rules on Lovegobuy help, "
                    f'and that you registered via <a href="{REGISTER}" target="_blank" rel="sponsored noopener">official Lovegobuy</a>.',
                ),
                (
                    "Canada buyer checklist",
                    "Read declared value rules, choose tracked lines when possible, and compare economy vs express for GST/HST risk. "
                    "A legit agent does not promise zero customs holds.",
                ),
                (
                    "Red flags",
                    "Off-platform wire requests, cloned sites without QC step, or 'guaranteed 5-day DDP' claims without line proof.",
                ),
            ],
            faq=[
                ("is lovegobuy legit?", "Established agent model with QC warehouse workflow — verify policies yourself."),
                ("is lovegobuy safe?", "Safer when you use official checkout, approve QC, and avoid unofficial middlemen."),
                ("is lovegobuy real?", "Real service — but cross-border reps still carry seller and customs risk."),
                ("lovegobuy scam?", "Scams often mimic agents; never pay outside Lovegobuy dashboard."),
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
            title=f"Lovegobuy Opiniones {YEAR} — ¿Es fiable en España?",
            description="lovegobuy opiniones: envío, QC, cupones y soporte. Guía independiente para compradores en España con W2CLinks.",
            h1="Opiniones sobre Lovegobuy",
            intro=(
                "Las búsquedas lovegobuy opiniones mezclan reseñas de envío, tiempos de QC, cupones y soporte. "
                "Esta guía resume señales útiles sin inventar puntuaciones — compara siempre hilos recientes."
            ),
            sections=[
                (
                    "Dónde leer opiniones útiles",
                    "Reddit (r/FashionReps, comunidades de replicas), Discord y foros en español — prioriza experiencias "
                    "de los últimos 6–12 meses con fotos QC y números de seguimiento.",
                ),
                (
                    "Workflow antes de opinar",
                    f'Compara finds en <a href="{SPREADSHEET}" target="_blank" rel="noopener">W2CLinks</a>, registra con '
                    f'<a href="{REGISTER}" target="_blank" rel="sponsored noopener">W5RJX3</a>, revisa QC y solo entonces envía a España.',
                ),
                (
                    "Opiniones negativas frecuentes",
                    "Retrasos aduaneros, líneas economy lentas o sellers que no envían al almacén — a menudo no son 'estafa' sino "
                    "expectativas mal calibradas. Lee también nuestra guía de envío a España.",
                ),
            ],
            faq=[
                ("¿Lovegobuy opiniones son positivas?", "Varían por línea, peso y temporada — no hay una nota única oficial."),
                ("¿Es fiable según opiniones?", "Agente conocido con QC — haz tu propia due diligence."),
                ("¿Opiniones oficiales?", "Recurso partner independiente — pedidos y soporte en lovegobuy.com."),
            ],
        ),
    ),
    _page(
        "es-lovegobuy-confiable",
        regions=["ES"],
        cta=CTA_REGISTER,
        cta_href=REGISTER,
        es=_loc(
            title=f"¿Lovegobuy es confiable? Guía España {YEAR}",
            description="lovegobuy es confiable y es fiable: señales de confianza, QC, pagos y aduanas para compradores españoles.",
            h1="¿Lovegobuy es confiable?",
            intro=(
                "Búsquedas como lovegobuy es confiable, es fiable y is lovegobuy legit buscan lo mismo: "
                "¿puedo pagar, recibir QC y enviar a España sin sorpresas?"
            ),
            sections=[
                (
                    "Señales de un agente confiable",
                    "Fotos QC en almacén, panel de parcel con líneas rastreables, políticas publicadas y checkout solo en lovegobuy.com.",
                ),
                (
                    "Qué hacer tú en España",
                    "Declara valores coherentes, elige línea acorde al peso, revisa IVA/DUA y no pagues fuera de la plataforma.",
                ),
                (
                    "Enlaces útiles",
                    f'<a href="/lovegobuy-opiniones/">opiniones</a>, <a href="/envio-lovegobuy-espana/">envío España</a>, '
                    f'<a href="/lovegobuy-coupon/">cupones</a> y <a href="/como-comprar-en-lovegobuy/">cómo comprar</a>.',
                ),
            ],
            faq=[
                ("¿Es seguro comprar en Lovegobuy?", "Más seguro con QC aprobado y pagos oficiales — riesgo de aduana sigue existiendo."),
                ("¿Lovegobuy es una estafa?", "Evita intermediarios que piden transferencias externas."),
                ("¿Cómo empezar?", f'Registra con <a href="{REGISTER}" target="_blank" rel="sponsored noopener">invitación W5RJX3</a>.'),
            ],
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
            title=f"Lovegobuy Recensioni {YEAR} — È affidabile?",
            description="lovegobuy recensioni: spedizione, QC, coupon e supporto. Guida per acquirenti italiani con W2CLinks.",
            h1="Lovegobuy recensioni",
            intro=(
                "Chi cerca lovegobuy recensioni vuole capire tempi di spedizione verso l'Italia, qualità delle foto QC "
                "e reattività del supporto — confronta sempre thread recenti, non screenshot vecchi."
            ),
            sections=[
                (
                    "Dove leggere recensioni utili",
                    "Reddit, Discord e community replica — cerca parcel ID, peso reale e linea usata, non solo hype su un singolo find.",
                ),
                (
                    "Flusso consigliato",
                    f'Sfoglia <a href="{SPREADSHEET}" target="_blank" rel="noopener">W2CLinks</a>, registrati con '
                    f'<a href="{REGISTER}" target="_blank" rel="sponsored noopener">W5RJX3</a>, approva QC e poi scegli la linea verso IT.',
                ),
                (
                    "Recensioni negative comuni",
                    "Dogana lenta, linee economy o seller che non spediscono al magazzino — spesso problemi di processo, non necessariamente truffa.",
                ),
            ],
            faq=[
                ("Lovegobuy è affidabile?", "Agente noto con workflow QC — fai due diligence personale."),
                ("Le recensioni sono ufficiali?", "Guida partner indipendente — ordini su lovegobuy.com."),
                ("Quanto ci mette la spedizione in Italia?", "Settimane tipiche — dipende da linea e dogana."),
            ],
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
            title=f"Lovegobuy Ervaringen {YEAR} — Betrouwbaar in NL?",
            description="lovegobuy ervaringen en reviews: verzending naar Nederland, QC, coupons. Onafhankelijke gids met W2CLinks.",
            h1="Lovegobuy ervaringen",
            intro=(
                "lovegobuy ervaringen en is lovegobuy betrouwbaar horen bij dezelfde vraag: "
                "hoe verloopt verzending naar NL, QC en support in de praktijk?"
            ),
            sections=[
                (
                    "Waar ervaringen nuttig zijn",
                    "Reddit r/FashionReps en NL/EU threads — let op parcelgewicht, verzendlijn en recente data, niet alleen hype.",
                ),
                (
                    "Aanbevolen workflow",
                    f'Browse <a href="{SPREADSHEET}" target="_blank" rel="noopener">W2CLinks</a>, registreer met '
                    f'<a href="{REGISTER}" target="_blank" rel="sponsored noopener">W5RJX3</a>, keur QC goed en kies daarna een lijn naar Nederland.',
                ),
                (
                    "Veelgehoorde klachten",
                    "Douane-vertraging, economy-lijnen of sellers die niet inbounden — vaak verwachtingsproblemen; zie verzendgids NL.",
                ),
            ],
            faq=[
                ("Is Lovegobuy betrouwbaar volgens ervaringen?", "Bekende agent met QC — eigen due diligence blijft nodig."),
                ("Hoe lang duurt verzending NL?", "Weken typisch — afhankelijk van lijn en seizoen."),
                ("Officiële reviews?", "Partner-gids — support en orders via lovegobuy.com."),
            ],
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
            title=f"Lovegobuy Europe Guide {YEAR} — EU Spreadsheet Hub",
            description="lovegobuy europe: W2CLinks spreadsheet, VAT notes and Lovegobuy ordering for EU buyers on lovegobuyspreadsheet.eu.",
            h1="Lovegobuy Europe",
            intro=(
                "Pan-EU English hub for lovegobuy europe searches: browse community finds on W2CLinks, "
                "order through Lovegobuy, and read country-specific shipping notes where available."
            ),
            sections=[
                SEC_SPREADSHEET,
                SEC_AGENT,
                (
                    "EU shipping snapshot",
                    "VAT and IOSS rules differ by member state — economy lines save money but add time. "
                    "Combine lighter items per parcel and compare tracked vs semi-tracked services.",
                ),
                (
                    "Country sites in this cluster",
                    "For localized guides see our ES, IT, NL and CA properties via hreflang — this .eu domain is the English pan-European entry.",
                ),
            ],
            faq=[
                ("Is Lovegobuy available in Europe?", "Yes — warehouse export to EU countries with line-dependent customs."),
                ("Best starting point?", f'{SPREADSHEET} for finds, then register with invite W5RJX3 on Lovegobuy.'),
            ],
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
            title=f"Lovegobuy Guide {YEAR} — x-default Spreadsheet & Agent Hub",
            description="lovegobuy guide on lovegobuyguide.com: W2CLinks spreadsheet, invite W5RJX3, shipping, QC and coupon workflows.",
            h1="Lovegobuy Guide",
            intro=(
                "International English hub (hreflang x-default): discover finds on W2CLinks, paste links into Lovegobuy, "
                "review QC photos, and ship with realistic customs expectations."
            ),
            sections=[
                SEC_SPREADSHEET,
                SEC_AGENT,
                (
                    "Core guides on this site",
                    '<a href="/lovegobuy-spreadsheet/">spreadsheet</a>, <a href="/lovegobuy-shipping/">shipping</a>, '
                    '<a href="/is-lovegobuy-legit/">legitimacy</a>, <a href="/lovegobuy-coupon/">coupons</a> and '
                    '<a href="/how-to-use-lovegobuy/">how to use</a>.',
                ),
                (
                    "Official promotions",
                    "Lovegobuy.com may show a new-user coupon pack (e.g. $137) — confirm live amounts in your dashboard after "
                    f'<a href="{REGISTER}" target="_blank" rel="sponsored noopener">registration</a>.',
                ),
            ],
            faq=[
                ("What is lovegobuyguide.com?", "Independent partner resource for spreadsheet discovery — orders on Lovegobuy."),
                ("Where is the spreadsheet?", f'Live hub: <a href="{SPREADSHEET}" target="_blank" rel="noopener">W2CLinks</a>.'),
                ("Invite code?", "W5RJX3 on official Lovegobuy registration."),
            ],
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
