"""Long-form SEO sections (~800–1000 words) merged into page builds."""

from __future__ import annotations

from scripts.link_helpers_lovegobuy import (
    AGENT_PLATFORM,
    category_url,
    main_spreadsheet_url,
    product_search_url,
)

SPREADSHEET = main_spreadsheet_url()
PLATFORM = AGENT_PLATFORM["baseUrl"]
REGISTER = AGENT_PLATFORM["registerUrl"]


def _p(*paragraphs: str) -> list[tuple[str, str]]:
    return [(h, body) for h, body in paragraphs]


def _base_spreadsheet(region: str, lang: str) -> list[tuple[str, str]]:
    en = [
        (
            "What lovegobuy spreadsheet searchers actually want",
            "Most people typing lovegobuy spreadsheet are not looking for a downloadable Excel file on a random blog. "
            "They want a live, filterable browse experience: newest community finds, category slices, brand lists, "
            f"and keyword search that opens on W2CLinks ({SPREADSHEET}). This partner resource explains the workflow "
            "and routes every product action to that hub instead of hosting fake local inventory.",
        ),
        (
            "Step-by-step browse workflow",
            "Start on the spreadsheet hub, sort by newest, then narrow by category or brand. "
            "When a find looks promising, open the listing, copy the source link, and paste it into Lovegobuy. "
            "Pay for the item, wait for warehouse inbound, review QC photos, and only then build an international parcel. "
            "Skipping QC or rushing line selection is where most first-time buyer frustration comes from.",
        ),
        (
            "How finds differ from marketplace listings",
            "Finds are curated discovery entries — often shared in Reddit or Discord communities — aggregated into "
            "a spreadsheet-style browse UI. They help you discover items faster, but they do not replace seller pages, "
            "size charts, or Lovegobuy warehouse inspection. Treat finds as a starting point, not a guarantee.",
        ),
        (
            "Category strategy for smarter parcels",
            f"Shoes usually add more weight than tees or accessories. If you are shipping to {region}, combine lighter "
            "items first and keep heavier categories for a second parcel unless your line supports the weight well. "
            f"Use category filters on W2CLinks — for example "
            f"<a href=\"{category_url('SNEAKERS')}\" target=\"_blank\" rel=\"noopener\">SNEAKERS</a> or "
            f"<a href=\"{category_url('HOODIES')}\" target=\"_blank\" rel=\"noopener\">HOODIES</a> — "
            "to plan parcel economics before ordering.",
        ),
        (
            "Coupons, QC and shipping tie-in",
            "Spreadsheet browsing does not automatically apply coupons or choose shipping lines. "
            f"After you pick items on W2CLinks, verify Lovegobuy promotions in your account, read QC photos carefully, "
            "and compare shipping estimates for your country. A good spreadsheet session ends with a clear parcel plan, "
            "not a cart full of unrelated heavy items.",
        ),
        (
            "Common mistakes to avoid",
            "Do not assume every find is in stock. Do not ignore size tags in QC photos. "
            "Do not pick the cheapest shipping line without reading weight limits and customs risk. "
            "Do not treat community hype as product quality proof — compare multiple finds and check recent additions.",
        ),
    ]
    if lang == "es":
        return [
            (
                "Qué buscan realmente con lovegobuy spreadsheet",
                "La mayoría no busca un Excel estático, sino un hub vivo en W2CLinks con filtros por categoría, "
                "marca y palabra clave. Este recurso de partner explica el flujo y envía cada acción de producto al "
                f"spreadsheet oficial ({SPREADSHEET}).",
            ),
            (
                "Flujo paso a paso",
                "Abre el spreadsheet, ordena por newest, filtra categoría o marca, copia el enlace del producto "
                "y pégalo en Lovegobuy. Paga, espera inbound, revisa QC y solo entonces crea el paquete internacional.",
            ),
            (
                "Errores comunes",
                "No asumas stock permanente. No ignores tallas en fotos QC. No elijas la línea más barata sin "
                "revisar peso, volumen y posibles tasas de importación en España.",
            ),
        ] + en[3:]
    if lang == "fr":
        return [
            (
                "Ce que les recherches lovegobuy spreadsheet signifient",
                "Les utilisateurs veulent un hub W2CLinks filtrable — pas un faux stock local. "
                "Ce guide partenaire explique le parcours et redirige toutes les actions produit vers le tableur live.",
            ),
            (
                "Workflow en étapes",
                "Ouvrez le tableur, triez par newest, filtrez catégorie/marque, copiez le lien source dans Lovegobuy, "
                "payez, attendez l'entrée entrepôt, vérifiez les photos QC, puis soumettez le colis.",
            ),
        ] + en[2:]
    if lang == "de":
        return [
            (
                "Was Nutzer mit lovegobuy spreadsheet meinen",
                "Gesucht wird ein live browse hub auf W2CLinks — keine lokale Produktseite. "
                "Diese Partner-Ressource erklärt den Ablauf und leitet alle Produktaktionen dorthin.",
            ),
            (
                "Schritt-für-Schritt",
                "Spreadsheet öffnen, nach newest sortieren, Kategorie/Marke filtern, Link in Lovegobuy einfügen, "
                "bezahlen, QC prüfen, dann internationales Paket erstellen.",
            ),
        ] + en[2:]
    if lang == "nl":
        return [
            (
                "Wat zoekers met lovegobuy spreadsheet bedoelen",
                "Gebruikers willen een live W2CLinks-hub met categorie-, merk- en zoekfilters — geen nep-inventaris. "
                f"Dit partner-resource legt de workflow uit en stuurt elke productactie naar {SPREADSHEET}.",
            ),
            (
                "Stap-voor-stap",
                "Open het spreadsheet, sorteer op newest, filter categorie of merk, kopieer de bronlink naar Lovegobuy, "
                "betaal, wacht op inbound, controleer QC en dien daarna het internationale pakket in.",
            ),
            (
                "Registratie en coupon",
                f"Nieuwe gebruikers kunnen via onze uitnodigingslink ({REGISTER}) registreren — "
                "promoties op Lovegobuy.com (o.a. $137 couponpakket) wijzigen; controleer altijd in je dashboard.",
            ),
        ] + en[2:]
    if lang == "fi":
        return [
            (
                "Mitä lovegobuy spreadsheet -hakijat oikeasti haluavat",
                "Käyttäjät etsivät live W2CLinks -hubia kategorioilla ja hakusanalla — ei paikallista väärennettyä varastoa. "
                f"Tämä partner-resurssi ohjaa tuotetoiminnot kohteeseen {SPREADSHEET}.",
            ),
            (
                "Vaiheittainen työnkulku",
                "Avaa spreadsheet, järjestä newest, suodata kategoria tai brändi, kopioi linkki Lovegobuyhin, "
                "maksa, odota varastoon saapumista, tarkista QC ja vasta sitten lähetä kansainvälinen paketti.",
            ),
            (
                "Rekisteröityminen ja kuponki",
                f"Uudet käyttäjät voivat rekisteröityä kutsulinkillä ({REGISTER}) — "
                "Lovegobuy.comin kampanjat (esim. $137 kuponkipaketti) muuttuvat; vahvista aina tililläsi.",
            ),
        ] + en[2:]
    return en


def _shipping_deep(region: str, lang: str) -> list[tuple[str, str]]:
    en = [
        (
            "Warehouse stage before international shipping",
            f"International shipping does not start when you pay for a Taobao/1688 item. Items land at the Lovegobuy "
            "warehouse first, go through inbound processing and QC photos, and may sit in free storage for a limited "
            "period. Only after you approve QC and submit a parcel does line selection and tracking begin.",
        ),
        (
            "How to estimate parcel weight realistically",
            "Single sneakers often land around 1.5–2.5 kg with box and packaging. Hoodies may be 0.6–1.2 kg each. "
            "Small accessories can be light but still add volume. Combine items thoughtfully — shipping cost scales "
            "with both actual weight and volumetric weight depending on the line.",
        ),
        (
            "Line selection checklist",
            "Compare estimated delivery window, tracked vs semi-tracked service, compensation rules, and whether "
            "the line accepts your category mix. Economy lines save money but add time and customs exposure. "
            "Express lines cost more but may fit urgent replacements or single-item parcels.",
        ),
        (
            "Customs and declared value",
            f"For {region}, keep declared values honest and consistent with invoice screenshots. "
            "Customs delays are often unrelated to Lovegobuy itself — they happen at import screening. "
            "Budget extra days during peak seasons and avoid assuming 'DDP' unless the line explicitly states it.",
        ),
        (
            "Tracking stages shoppers confuse",
            "Warehouse processing, outbound handoff, export scan, airline/handoff milestones, and import clearance "
            "are different stages. A gap between scans does not always mean loss — but long gaps deserve a support ticket "
            "with parcel ID and line name ready.",
        ),
    ]
    return en


def _trust_deep(lang: str) -> list[tuple[str, str]]:
    return [
        (
            "Agent model in plain language",
            f"Lovegobuy ({PLATFORM}) purchases from Chinese marketplaces on your behalf. "
            "You are not buying directly from Nike or Taobao checkout in your country currency — you are paying "
            "an agent to source, inspect, store, and ship. That model is legitimate when you understand the steps.",
        ),
        (
            "What legit looks like in practice",
            "Legit agent workflow includes visible QC photos, parcel submission controls, trackable lines, "
            "and support channels for warehouse issues. Red flags are fake independent review scores, "
            "promises of zero customs risk, or sites that clone checkout without warehouse inspection.",
        ),
        (
            "Safety vs zero-risk myths",
            "Safe buying means using QC as your checkpoint, choosing payment methods you trust, and reading "
            "current help-center policies. No cross-border rep purchase is 100% risk-free — seller delays, "
            "QC failures, and customs holds can happen on any agent.",
        ),
        (
            "How this partner resource fits",
            "This site is an official partner resource for spreadsheet discovery via W2CLinks. "
            "It does not host checkout or warehouse tools. Use it to learn workflow, compare categories, "
            "and open live finds — then complete orders on Lovegobuy.",
        ),
    ]


def _coupons_deep(lang: str) -> list[tuple[str, str]]:
    return [
        (
            "How Lovegobuy coupons actually work",
            "Coupons and shipping bonuses change over time. Some appear at registration, others during campaigns "
            "or parcel submission. This guide does not publish fixed codes because stale codes create support noise. "
            "Always verify eligibility inside your Lovegobuy account before paying.",
        ),
        (
            "Smart order to save effort",
            f"Browse and shortlist on {SPREADSHEET} first. Confirm size, seller, and weight expectations. "
            "Then apply any eligible coupon at payment or parcel step. Combining unrelated heavy items just "
            "to 'use a coupon' often increases shipping more than the coupon saves.",
        ),
        (
            "$137 new-user coupon pack (synced with Lovegobuy.com)",
            "Lovegobuy.com currently promotes a $137 coupon pack for new registrations — amounts and eligibility "
            "change with campaigns. Register via our invitation link "
            f'<a href="{REGISTER}" target="_blank" rel="sponsored noopener">{REGISTER}</a>, '
            "then confirm the live bonus inside your Lovegobuy wallet before paying. "
            "Older Reddit threads may mention different amounts; treat those as outdated unless the help center confirms them.",
        ),
        (
            "Invitation link vs random signup",
            "Invitation links attribute your account to a referrer and may unlock partner-tracked bonuses. "
            "They do not replace Lovegobuy's own terms — shipping fees, QC, and line rules still apply. "
            "Bookmark the official help center for coupon expiry and parcel-stage bonuses.",
        ),
    ]


def _qc_deep(lang: str) -> list[tuple[str, str]]:
    return [
        (
            "Why QC matters more than spreadsheet hype",
            "Spreadsheet finds show community discovery. QC photos show what actually arrived at warehouse. "
            "Compare logo placement, color, stitching, size tag, insole, tongue, and packaging against the seller listing.",
        ),
        (
            "Shoes vs clothing QC focus",
            "For shoes, check toe shape, sole alignment, glue marks, and box label. "
            "For hoodies and jackets, check zipper, drawstrings, wash tag, and measurement against size chart. "
            "Reject or exchange before international shipping when flaws exceed your tolerance.",
        ),
        (
            "When to ask for more photos",
            "If lighting is poor or angles hide details, request supplemental QC before approving. "
            "Once a parcel ships internationally, options narrow — warehouse stage is your main control point.",
        ),
    ]


def _howto_deep(lang: str) -> list[tuple[str, str]]:
    return [
        (
            "Full order path from find to doorstep",
            f"1) Discover on W2CLinks spreadsheet. 2) Copy product URL. 3) Paste into Lovegobuy buy form. "
            "4) Pay and wait for seller ship-to-warehouse. 5) Review QC photos. 6) Submit parcel with line choice. "
            "7) Track import milestones. Each step has different timing — plan weeks, not days.",
        ),
        (
            "Account setup tips",
            "Use a strong password, save warehouse address rules, and keep balance/top-up records. "
            "Paste exact links — shortened or wrong marketplace links cause purchase delays.",
        ),
        (
            "Payment checklist",
            "Confirm total item price, domestic China shipping to warehouse, service fees, and later international line cost. "
            "Budget as separate stages instead of one guessed number.",
        ),
    ]


def _generic_deep(slug: str, region: str, lang: str) -> list[tuple[str, str]]:
    return _base_spreadsheet(region, lang) + [
        (
            "Related guides on this site",
            "Use the shipping, QC, and coupon guides linked from the homepage for country-specific notes. "
            f"Keyword intent around {slug.replace('-', ' ')} is covered here without duplicating fake product pages.",
        ),
    ]


SLUG_HANDLERS = {
    "": lambda r, l: _base_spreadsheet(r, l),
    "lovegobuy-spreadsheet": lambda r, l: _base_spreadsheet(r, l),
    "lovegobuy-spreadsheets": lambda r, l: _base_spreadsheet(r, l),
    "lovegobuy-finds": lambda r, l: _base_spreadsheet(r, l) + [
        (
            "Searching finds by keyword",
            f"Try keyword search on W2CLinks — e.g. "
            f"<a href=\"{product_search_url('dunk')}\" target=\"_blank\" rel=\"noopener\">dunk finds</a> — "
            "then compare multiple entries before ordering.",
        ),
    ],
    "lovegobuy-shipping": lambda r, l: _shipping_deep(r, l),
    "lovegobuy-shipping-calculator": lambda r, l: _shipping_deep(r, l),
    "lovegobuy-shipping-coupons": lambda r, l: _shipping_deep(r, l) + _coupons_deep(l),
    "livraison-lovegobuy": lambda r, l: _shipping_deep(r, l),
    "envio-lovegobuy-espana": lambda r, l: _shipping_deep(r, l),
    "lovegobuy-toimitus": lambda r, l: _shipping_deep(r, l),
    "lovegobuy-shipping-to-canada": lambda r, l: _shipping_deep(r, l),
    "lovegobuy-coupons": lambda r, l: _coupons_deep(l),
    "lovegobuy-coupon": lambda r, l: _coupons_deep(l),
    "lovegobuy-codes": lambda r, l: _coupons_deep(l),
    "lovegobuy-qc": lambda r, l: _qc_deep(l),
    "qc-lovegobuy": lambda r, l: _qc_deep(l),
    "is-lovegobuy-legit": lambda r, l: _trust_deep(l),
    "is-lovegobuy-safe": lambda r, l: _trust_deep(l),
    "how-to-use-lovegobuy": lambda r, l: _howto_deep(l),
    "como-comprar-en-lovegobuy": lambda r, l: _howto_deep(l),
    "lovegobuy-review": lambda r, l: _trust_deep(l),
    "avis-lovegobuy": lambda r, l: _trust_deep(l),
    "best-lovegobuy-spreadsheet": lambda r, l: _base_spreadsheet(r, l),
}


def merge_deep_sections(
    slug: str,
    region: str,
    lang: str,
    base_sections: list[tuple[str, str]],
) -> list[tuple[str, str]]:
    """Append long-form blocks; dedupe headings already present."""
    handler = SLUG_HANDLERS.get(slug, lambda r, l: _generic_deep(slug, r, l))
    extra = handler(region, lang)
    seen = {h.strip().lower() for h, _ in base_sections}
    merged = list(base_sections)
    for heading, body in extra:
        key = heading.strip().lower()
        if key in seen:
            continue
        seen.add(key)
        merged.append((heading, body))
    return merged
