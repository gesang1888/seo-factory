"""Page metadata and content for OrientDig Spreadsheet cluster."""

from __future__ import annotations

from scripts.link_helpers import (
    AGENT_PLATFORM,
    category_url,
    main_spreadsheet_url,
    product_search_url,
)

YEAR = "2026"
SPREADSHEET = main_spreadsheet_url()
PLATFORM = AGENT_PLATFORM["baseUrl"]
REGISTER = AGENT_PLATFORM["registerUrl"]

CTA_SPREADSHEET = "Open OrientDig Spreadsheet"
CTA_BROWSE = "Browse Spreadsheet"
CTA_FINDS = "See Latest Finds"
CTA_COUPONS = "Check OrientDig Coupons"
CTA_START = "Start on OrientDig"
CTA_OPEN = "Open OrientDig"
CTA_SEARCH = "Search Products on OrientDig"
CTA_VISIT = "Visit OrientDig Platform"
CTA_VIEW_FINDS = "View Finds on OrientDig"
CTA_ESTIMATE = "Open Spreadsheet"


def _faq(items: list[tuple[str, str]]) -> list[dict[str, str]]:
    return [{"question": q, "answer": a} for q, a in items]


def _page(
    slug: str,
    *,
    title_en: str,
    desc_en: str,
    h1_en: str,
    cta: str,
    cta_href: str,
    intro_en: str,
    sections_en: list[tuple[str, str]],
    faq_en: list[tuple[str, str]],
    title_nl: str = "",
    desc_nl: str = "",
    h1_nl: str = "",
    intro_nl: str = "",
    title_de: str = "",
    desc_de: str = "",
    h1_de: str = "",
    intro_de: str = "",
    title_it: str = "",
    desc_it: str = "",
    h1_it: str = "",
    intro_it: str = "",
    title_fr: str = "",
    desc_fr: str = "",
    h1_fr: str = "",
    intro_fr: str = "",
    title_es: str = "",
    desc_es: str = "",
    h1_es: str = "",
    intro_es: str = "",
    regions: list[str] | None = None,
) -> dict:
    return {
        "slug": slug,
        "regions": regions,
        "cta": cta,
        "cta_href": cta_href,
        "en": {
            "title": title_en,
            "description": desc_en,
            "h1": h1_en,
            "intro": intro_en,
            "sections": sections_en,
            "faq": _faq(faq_en),
        },
        "nl": {
            "title": title_nl or title_en,
            "description": desc_nl or desc_en,
            "h1": h1_nl or h1_en,
            "intro": intro_nl or intro_en,
            "sections": sections_en,
            "faq": _faq(faq_en),
        },
        "de": {
            "title": title_de or title_en,
            "description": desc_de or desc_en,
            "h1": h1_de or h1_en,
            "intro": intro_de or intro_en,
            "sections": sections_en,
            "faq": _faq(faq_en),
        },
        "it": {
            "title": title_it or title_en,
            "description": desc_it or desc_en,
            "h1": h1_it or h1_en,
            "intro": intro_it or intro_en,
            "sections": sections_en,
            "faq": _faq(faq_en),
        },
        "fr": {
            "title": title_fr or title_en,
            "description": desc_fr or desc_en,
            "h1": h1_fr or h1_en,
            "intro": intro_fr or intro_en,
            "sections": sections_en,
            "faq": _faq(faq_en),
        },
        "es": {
            "title": title_es or title_en,
            "description": desc_es or desc_en,
            "h1": h1_es or h1_en,
            "intro": intro_es or intro_en,
            "sections": sections_en,
            "faq": _faq(faq_en),
        },
    }


PAGES: list[dict] = [
    _page(
        "",
        title_en=f"OrientDig Spreadsheet Guide: Finds, Coupons & Shipping ({YEAR})",
        desc_en="Use this OrientDig spreadsheet guide to browse curated finds, coupon tips, shipping basics, and QC workflow. Product links open on W2CLinks.",
        h1_en="OrientDig Spreadsheet: Finds, Coupons and Shipping Guide",
        cta=CTA_SPREADSHEET,
        cta_href=SPREADSHEET,
        intro_en=(
            "OrientDig is a China shopping agent for Taobao, 1688, and Weidian. "
            "This guide explains how spreadsheet-style product lists and finds work, "
            "and links you to browse entries on W2CLinks — not a fake local database."
        ),
        sections_en=[
            (
                "What this spreadsheet guide covers",
                "Searchers looking for an orientdig spreadsheet usually want a browsable list of "
                "community finds with links to source items. W2CLinks hosts the spreadsheet hub "
                f"at <a href=\"{SPREADSHEET}\" target=\"_blank\" rel=\"noopener\">w2clinks.com/spreadsheet/</a> "
                "where you can filter by category, brand, or keyword.",
            ),
            (
                "How OrientDig fits in",
                f"After you pick an item, you purchase through OrientDig ({PLATFORM}). "
                "OrientDig buys from Chinese marketplaces, performs QC photos in warehouse, "
                "then ships internationally when you submit a parcel.",
            ),
            (
                "Quick category links",
                f"Shoes: <a href=\"{category_url('SHOES')}\" target=\"_blank\" rel=\"noopener\">Browse shoes</a>. "
                f"Hoodies: <a href=\"{category_url('HOODIES')}\" target=\"_blank\" rel=\"noopener\">Browse hoodies</a>. "
                f"Bags: <a href=\"{category_url('BAGS')}\" target=\"_blank\" rel=\"noopener\">Browse bags</a>.",
            ),
        ],
        faq_en=[
            (
                "Is this the official OrientDig spreadsheet?",
                "No. This is an independent guide site. Spreadsheet and find links are provided through W2CLinks.",
            ),
            (
                "How do I open the OrientDig spreadsheet?",
                f"Use the Open OrientDig Spreadsheet button to go to {SPREADSHEET}",
            ),
            (
                "Does OrientDig support Taobao and 1688?",
                "Yes. OrientDig accepts product links and keyword search from Taobao, Tmall, 1688, and Weidian.",
            ),
        ],
        title_nl="OrientDig Spreadsheet: Finds, Coupons en Verzending ({})".format(YEAR),
        desc_nl="Gids voor orientdig spreadsheet: finds, coupons en verzending. Links openen op W2CLinks.",
        h1_nl="OrientDig Spreadsheet: Finds, Coupons en Verzending",
        intro_nl=(
            "OrientDig is een China shopping agent voor Taobao, 1688 en Weidian. "
            "Deze gids legt spreadsheet/finds uit; productlinks openen op W2CLinks."
        ),
        title_de="OrientDig Spreadsheet: Finds, Gutscheine & Versand ({})".format(YEAR),
        desc_de="OrientDig Spreadsheet Guide: Finds, Gutscheine und Versand. Produktlinks führen zu W2CLinks.",
        h1_de="OrientDig Spreadsheet: Finds, Gutscheine und Versand",
        intro_de=(
            "OrientDig ist ein China Shopping Agent für Taobao, 1688 und Weidian. "
            "Diese Seite erklärt Spreadsheet/Finds; Links führen zu W2CLinks."
        ),
        title_it="OrientDig Spreadsheet: Finds, Coupon e Spedizione ({})".format(YEAR),
        desc_it="Guida orientdig spreadsheet: finds, coupon e spedizione. I link prodotti aprono su W2CLinks.",
        h1_it="OrientDig Spreadsheet: Finds, Coupon e Spedizione",
        intro_it=(
            "OrientDig è un agente di shopping cinese per Taobao, 1688 e Weidian. "
            "Questa guida spiega spreadsheet/finds; i link aprono su W2CLinks."
        ),
        title_fr="OrientDig Spreadsheet : Finds, Coupons et Livraison ({})".format(YEAR),
        desc_fr="Guide orientdig spreadsheet : finds, coupons et livraison. Les liens produits passent par W2CLinks.",
        h1_fr="OrientDig Spreadsheet : Finds, Coupons et Livraison",
        intro_fr=(
            "OrientDig est un agent d'achat Chine pour Taobao, 1688 et Weidian. "
            "Ce guide explique le tableur/finds ; les liens produits passent par W2CLinks."
        ),
        title_es=f"OrientDig Spreadsheet: Finds, Cupones y Envíos ({YEAR})",
        desc_es="Guía orientdig spreadsheet: finds, cupones y envíos. Los enlaces de productos abren en W2CLinks.",
        h1_es="OrientDig Spreadsheet: Finds, Cupones y Envíos",
        intro_es=(
            "OrientDig es un agente de compras en China para Taobao, 1688 y Weidian. "
            "Esta guía explica spreadsheet/finds; los enlaces de productos abren en W2CLinks."
        ),
    ),
    _page(
        "orientdig-spreadsheet",
        title_en=f"OrientDig Spreadsheet: Browse Product Lists ({YEAR})",
        desc_en="orientdig spreadsheet — browse curated product lists with filters on W2CLinks, then order via OrientDig.",
        h1_en="OrientDig Spreadsheet",
        cta=CTA_BROWSE,
        cta_href=SPREADSHEET,
        intro_en=(
            "The orientdig spreadsheet keyword maps to the W2CLinks browse hub — filter by category, "
            "brand, or keyword. This page is the partner resource entry for spreadsheet browsing."
        ),
        sections_en=[
            (
                "Spreadsheet hub",
                f"Open the live spreadsheet at <a href=\"{SPREADSHEET}\" target=\"_blank\" rel=\"noopener\">w2clinks.com/spreadsheet/</a> "
                "to browse community finds sorted by newest.",
            ),
            (
                "Filter by intent",
                f"Try category filters or keyword search such as "
                f"<a href=\"{product_search_url('jordan')}\" target=\"_blank\" rel=\"noopener\">jordan finds</a>.",
            ),
        ],
        faq_en=[
            ("Is this a downloadable Excel file?", "No — it is a web browse hub on W2CLinks."),
            ("Where do I order?", f"After picking an item, purchase through OrientDig ({PLATFORM})."),
        ],
        title_es=f"OrientDig Spreadsheet: Listas de Productos ({YEAR})",
        desc_es="orientdig spreadsheet — explora listas de finds en W2CLinks y compra via OrientDig.",
        h1_es="OrientDig Spreadsheet",
        intro_es="orientdig spreadsheet lleva al hub W2CLinks — filtra por categoría, marca o palabra clave.",
        title_fr="OrientDig Spreadsheet : Parcourir les Finds ({})".format(YEAR),
        h1_fr="OrientDig Spreadsheet",
        intro_fr="Le mot-clé orientdig spreadsheet mène au hub W2CLinks — filtres par catégorie et marque.",
        title_de="OrientDig Spreadsheet: Produktlisten ({})".format(YEAR),
        h1_de="OrientDig Spreadsheet",
        intro_de="orientdig spreadsheet führt zum W2CLinks-Hub — nach Kategorie, Marke oder Keyword filtern.",
    ),
    _page(
        "orientdig-spreadsheets",
        title_en=f"OrientDig Spreadsheets: Browse Lists & Finds ({YEAR})",
        desc_en="orientdig spreadsheets explained — plural search guide for browsing multiple find lists on W2CLinks.",
        h1_en="OrientDig Spreadsheets: Browse Lists and Finds",
        cta=CTA_BROWSE,
        cta_href=SPREADSHEET,
        intro_en="People search orientdig spreadsheets (plural) when they want multiple curated lists, not a single file.",
        sections_en=[
            (
                "Spreadsheet vs spreadsheets",
                "Singular orientdig spreadsheet often means the main hub. Plural spreadsheets refers to "
                "category slices, brand lists, and seasonal find collections — all browsable on W2CLinks.",
            ),
            (
                "Browse by intent",
                f"Try keyword search: <a href=\"{product_search_url('jordan')}\" target=\"_blank\" rel=\"noopener\">jordan finds</a> "
                f"or <a href=\"{product_search_url('dunk')}\" target=\"_blank\" rel=\"noopener\">dunk finds</a>.",
            ),
        ],
        faq_en=[
            ("Are there multiple OrientDig spreadsheets?", "Community find lists are aggregated on W2CLinks spreadsheet hub."),
            ("Where do spreadsheets link to?", f"All browse CTAs go to {SPREADSHEET}"),
        ],
    ),
    _page(
        "orientdig-finds",
        title_en=f"OrientDig Finds: Latest Product Discovery ({YEAR})",
        desc_en="orientdig finds guide — how community product discovery works and where to browse latest entries on W2CLinks.",
        h1_en="OrientDig Finds: Latest Product Discovery",
        cta=CTA_FINDS,
        cta_href=SPREADSHEET,
        intro_en="orientdig finds covers QC-backed product discoveries shared by shoppers — browse them on W2CLinks, order via OrientDig.",
        sections_en=[
            (
                "What are finds?",
                "Finds are curated product entries with source links, often organized like a spreadsheet. "
                "They help you discover items before pasting links into OrientDig.",
            ),
            (
                "Search finds on W2CLinks",
                f"Open <a href=\"{SPREADSHEET}\" target=\"_blank\" rel=\"noopener\">W2CLinks spreadsheet</a> "
                "and sort by newest to see recent additions.",
            ),
        ],
        faq_en=[
            ("Are finds stored on this site?", "No. This site is a guide; finds live on W2CLinks spreadsheet."),
            ("How do I buy a find?", "Copy the source link into OrientDig, pay, wait for QC, then ship."),
        ],
    ),
    _page(
        "orientdig-coupons",
        title_en=f"OrientDig Coupons & Bonus Codes ({YEAR})",
        desc_en="orientdig coupons and shipping bonus tips — check current promotions on OrientDig and browse deals on W2CLinks.",
        h1_en="OrientDig Coupons and Bonus Codes",
        cta=CTA_COUPONS,
        cta_href=SPREADSHEET,
        intro_en="Coupon availability changes. This page explains how OrientDig coupons work without promising fixed discounts.",
        sections_en=[
            (
                "Where coupons appear",
                f"OrientDig may show registration or shipping coupons inside <a href=\"{PLATFORM}\" target=\"_blank\" rel=\"noopener\">orientdig.com</a>. "
                "Always verify terms in your account before checkout.",
            ),
            (
                "Browse deal categories",
                f"Use W2CLinks spreadsheet to find items first: <a href=\"{SPREADSHEET}\" target=\"_blank\" rel=\"noopener\">open spreadsheet</a>.",
            ),
        ],
        faq_en=[
            ("Are coupon codes guaranteed?", "No. Promotions change; verify on OrientDig at checkout."),
            ("Can I stack spreadsheet browsing with coupons?", "Yes — pick items on W2CLinks, then apply eligible OrientDig coupons when paying."),
        ],
    ),
    _page(
        "is-orientdig-legit",
        title_en=f"Is OrientDig Legit? Agent Workflow Explained ({YEAR})",
        desc_en="Is orientdig legit — objective guide to OrientDig shopping agent workflow, payments, QC, warehouse storage, and risks.",
        h1_en="Is OrientDig Legit?",
        cta=CTA_START,
        cta_href=SPREADSHEET,
        intro_en="OrientDig operates as a China shopping agent. Legitimacy depends on following standard agent workflow and understanding cross-border risks.",
        sections_en=[
            (
                "How the agent model works",
                "You pay OrientDig to purchase from Taobao/1688/Weidian sellers. Items arrive at OrientDig warehouse for QC photos. "
                "You then choose international shipping lines.",
            ),
            (
                "What to verify yourself",
                "Check payment method protection, read QC photos carefully, understand return limits on Chinese marketplaces, "
                "and budget for customs duties in your country.",
            ),
        ],
        faq_en=[
            ("Is OrientDig an official marketplace?", "No. It is a third-party purchasing agent, not Taobao itself."),
            ("Can orders fail?", "Yes — seller delays, QC issues, customs holds, and shipping disruptions can occur."),
        ],
    ),
    _page(
        "is-orientdig-safe",
        title_en=f"Is OrientDig Safe? Payments, QC & Risk FAQ ({YEAR})",
        desc_en="Is orientdig safe — FAQ on account security, payment methods, QC process, and realistic cross-border shopping risks.",
        h1_en="Is OrientDig Safe?",
        cta=CTA_OPEN,
        cta_href=SPREADSHEET,
        intro_en="Safety means understanding agent escrow flow, QC inspection, and that no cross-border purchase is risk-free.",
        sections_en=[
            (
                "Account and payment safety",
                "Use strong passwords and enable any available account protections on OrientDig. "
                "Prefer payment methods with buyer dispute options where available.",
            ),
            (
                "QC as your checkpoint",
                "Warehouse QC photos let you approve or reject items before international shipping — use this step.",
            ),
        ],
        faq_en=[
            ("Is shopping through an agent 100% safe?", "No cross-border agent purchase is risk-free."),
            ("What if QC fails?", "You may exchange or refund per OrientDig policy before shipping — check current terms."),
        ],
    ),
    _page(
        "orientdig-shipping",
        title_en=f"OrientDig Shipping Times, Lines & Process ({YEAR})",
        desc_en="orientdig shipping guide — warehouse storage, parcel submission, line selection, and realistic delivery timelines.",
        h1_en="OrientDig Shipping: Times, Lines and Process",
        cta=CTA_ESTIMATE,
        cta_href=SPREADSHEET,
        intro_en="Shipping starts after items pass QC and you submit a parcel. Timelines vary by line, season, and customs.",
        sections_en=[
            (
                "Typical flow",
                "Purchase → warehouse inbound → QC photos → storage (free period may apply) → choose shipping line → tracking.",
            ),
            (
                "No fixed delivery promise",
                "Avoid assuming exact day counts. Budget extra time during peak seasons and for customs inspection.",
            ),
        ],
        faq_en=[
            ("How long does OrientDig shipping take?", "Varies by line and destination — often weeks, not days."),
            ("Are duties included?", "Usually not. Import taxes may apply in your country."),
        ],
    ),
    _page(
        "orientdig-qc",
        title_en=f"OrientDig QC Photos & Warehouse Inspection ({YEAR})",
        desc_en="orientdig qc guide — quality check photos, warehouse inspection workflow, and how finds relate to QC on W2CLinks.",
        h1_en="OrientDig QC: Warehouse Inspection Guide",
        cta=CTA_VIEW_FINDS,
        cta_href=SPREADSHEET,
        intro_en="QC (quality check) photos are taken when items arrive at OrientDig warehouse — your chance to verify before shipping.",
        sections_en=[
            (
                "What QC shows",
                "Photos of actual items received — check logo, color, size tag, and defects vs seller listing.",
            ),
            (
                "Browse finds before ordering",
                f"Explore community QC-backed finds on <a href=\"{SPREADSHEET}\" target=\"_blank\" rel=\"noopener\">W2CLinks spreadsheet</a>.",
            ),
        ],
        faq_en=[
            ("Can I skip QC?", "Policies vary — QC is strongly recommended before international shipping."),
            ("What is qc orientdig search intent?", "Users want sample QC photos and process explanation — covered here."),
        ],
    ),
    _page(
        "how-to-use-orientdig",
        title_en=f"How to Use OrientDig: Order Tutorial ({YEAR})",
        desc_en="How to order on OrientDig — paste links, search keywords, pay, QC review, and submit international shipping.",
        h1_en="How to Use OrientDig: Step-by-Step",
        cta=CTA_SEARCH,
        cta_href=SPREADSHEET,
        intro_en="OrientDig lets you paste Taobao/Tmall/1688/Weidian links or search by keyword/image before purchasing.",
        sections_en=[
            (
                "Step 1 — Find products",
                f"Browse <a href=\"{SPREADSHEET}\" target=\"_blank\" rel=\"noopener\">W2CLinks spreadsheet</a> or paste a marketplace link into OrientDig.",
            ),
            (
                "Step 2 — Pay and wait for QC",
                "Complete payment on OrientDig. Wait for warehouse inbound and QC photos.",
            ),
            (
                "Step 3 — Ship internationally",
                "Approve QC, select a shipping line, pay freight, track parcel.",
            ),
        ],
        faq_en=[
            ("Can I search by image?", "OrientDig help center mentions image search — check current app/web features."),
            ("Do I need an account?", "Yes, register on OrientDig before placing orders."),
        ],
    ),
    _page(
        "orientdig-review",
        title_en=f"OrientDig Reviews & Trust Signals ({YEAR})",
        desc_en="orientdig reviews guide — how to evaluate Trustpilot, Reddit threads, and QC evidence without fake ratings.",
        h1_en="OrientDig Reviews and Trust Signals",
        cta=CTA_VISIT,
        cta_href=REGISTER,
        intro_en="This page does not display fabricated star ratings. Use multiple trust signals and your own QC review.",
        sections_en=[
            (
                "Where shoppers discuss OrientDig",
                "Reddit, Discord, and review platforms — read recent posts about shipping lines and QC quality.",
            ),
            (
                "Browse finds while researching",
                f"Compare community picks on <a href=\"{SPREADSHEET}\" target=\"_blank\" rel=\"noopener\">W2CLinks spreadsheet</a>.",
            ),
        ],
        faq_en=[
            ("Does this site publish fake Trustpilot scores?", "No. We link to OrientDig and encourage independent verification."),
            ("What matters most?", "QC photo review, shipping line choice, and realistic customs expectations."),
        ],
    ),
    # UK extras
    _page(
        "what-is-orientdig",
        regions=["UK"],
        title_en=f"What Is OrientDig? China Shopping Agent Explained ({YEAR})",
        desc_en="What is OrientDig — UK-focused explainer for Taobao, 1688, Weidian agent shopping and spreadsheet finds.",
        h1_en="What Is OrientDig?",
        cta=CTA_SPREADSHEET,
        cta_href=SPREADSHEET,
        intro_en="OrientDig is a China shopping agent helping UK buyers source from Taobao, 1688, and Weidian with QC and international shipping.",
        sections_en=[("UK buyer context", "Budget for VAT/duty where applicable. Use QC before shipping to avoid costly mistakes.")],
        faq_en=[("Is OrientDig a UK company?", "It is a cross-border agent serving international buyers including the UK.")],
    ),
    _page(
        "how-long-does-orientdig-take-to-ship",
        regions=["UK"],
        title_en=f"How Long Does OrientDig Take to Ship to the UK? ({YEAR})",
        desc_en="How long does orientdig take to ship — UK delivery timelines, customs, and line selection tips.",
        h1_en="How Long Does OrientDig Take to Ship?",
        cta=CTA_ESTIMATE,
        cta_href=SPREADSHEET,
        intro_en="UK delivery time depends on shipping line, season, and HMRC processing — no fixed guarantee.",
        sections_en=[("Realistic planning", "Many lines take several weeks total after parcel submission.")],
        faq_en=[("Does Royal Mail handle last mile?", "Depends on line — check OrientDig tracking details.")],
    ),
    _page(
        "orientdig-spreadsheet-reddit",
        regions=["UK"],
        title_en=f"OrientDig Spreadsheet Reddit Threads ({YEAR})",
        desc_en="orientdig spreadsheet reddit — how UK shoppers use Reddit finds and W2CLinks spreadsheet together.",
        h1_en="OrientDig Spreadsheet Reddit Guide",
        cta=CTA_BROWSE,
        cta_href=SPREADSHEET,
        intro_en="Reddit communities share OrientDig finds; W2CLinks spreadsheet organizes browsable lists with filters.",
        sections_en=[("Using both", "Read Reddit for tips, browse W2CLinks for structured search.")],
        faq_en=[("Is Reddit official?", "No — community discussion, not OrientDig support.")],
    ),
    # US extras
    _page(
        "best-orientdig-spreadsheet",
        regions=["US"],
        title_en=f"Best OrientDig Spreadsheet Browse Tips ({YEAR})",
        desc_en="best orientdig spreadsheet — US guide to filtering finds, categories, and brands on W2CLinks.",
        h1_en="Best OrientDig Spreadsheet Browse Tips",
        cta=CTA_BROWSE,
        cta_href=SPREADSHEET,
        intro_en="The best orientdig spreadsheet experience is filtered browsing on W2CLinks — sort by newest and use category filters.",
        sections_en=[("US shopper tips", "Factor US customs and use QC before consolidating heavy parcels.")],
        faq_en=[("Is there one official best list?", "No single list — browse categories and keywords on W2CLinks.")],
    ),
    _page(
        "orientdig-spreadsheet-2026",
        regions=["US"],
        title_en=f"OrientDig Spreadsheet {YEAR}: Updated Finds Hub",
        desc_en=f"orientdig spreadsheet {YEAR} — current W2CLinks hub for US shoppers browsing newest finds.",
        h1_en=f"OrientDig Spreadsheet {YEAR}",
        cta=CTA_SPREADSHEET,
        cta_href=SPREADSHEET,
        intro_en=f"{YEAR} find lists update continuously on W2CLinks — this guide links to the live hub.",
        sections_en=[("Stay current", "Sort by newest on W2CLinks rather than static reposts.")],
        faq_en=[("Is this a downloadable file?", "No — it is a browsable web hub on W2CLinks.")],
    ),
    _page(
        "orientdig-shipping-calculator",
        regions=["US"],
        title_en=f"OrientDig Shipping Calculator & Line Selection ({YEAR})",
        desc_en="orientdig shipping calculator — estimate freight on OrientDig and browse items on W2CLinks first.",
        h1_en="OrientDig Shipping Calculator Guide",
        cta=CTA_ESTIMATE,
        cta_href=SPREADSHEET,
        intro_en="Use OrientDig's freight estimator when submitting parcels; browse products on W2CLinks beforehand.",
        sections_en=[("Calculator tips", "Weigh consolidated parcels and compare lines inside OrientDig checkout.")],
        faq_en=[("Are calculator results final?", "Estimates may change after re-weigh at warehouse.")],
    ),
    _page(
        "orientdig-customer-service",
        regions=["US"],
        title_en=f"OrientDig Customer Service & Support Channels ({YEAR})",
        desc_en="orientdig customer service — tickets, help center, and when to contact OrientDig vs browse W2CLinks finds.",
        h1_en="OrientDig Customer Service",
        cta=CTA_VISIT,
        cta_href=REGISTER,
        intro_en="Order issues go to OrientDig support; product discovery questions may be answered via W2CLinks browse.",
        sections_en=[("Support scope", "Shipping delays, QC disputes, and payment issues — use OrientDig tickets.")],
        faq_en=[("Does this site provide support?", "No — independent guide; contact OrientDig for orders.")],
    ),
    _page(
        "orientdig-payment-methods",
        regions=["US"],
        title_en=f"OrientDig Payment Methods FAQ ({YEAR})",
        desc_en="orientdig payment methods — cards, wallets, and checkout tips for US buyers.",
        h1_en="OrientDig Payment Methods",
        cta=CTA_START,
        cta_href=SPREADSHEET,
        intro_en="Available payment methods depend on OrientDig account region and current checkout options.",
        sections_en=[("Before paying", "Confirm total includes service fees and expected domestic China shipping.")],
        faq_en=[("Are all US cards accepted?", "Check OrientDig checkout for your card/wallet availability.")],
    ),
    _page(
        "orientdig-tracking",
        regions=["US"],
        title_en=f"OrientDig Tracking: Parcel Status Guide ({YEAR})",
        desc_en="orientdig tracking — how to follow warehouse, international line, and last-mile tracking.",
        h1_en="OrientDig Tracking Guide",
        cta=CTA_OPEN,
        cta_href=REGISTER,
        intro_en="Tracking numbers appear after parcel submission — stages include warehouse processing and line handoff.",
        sections_en=[("Tracking gaps", "Delays between scans are common on economy lines.")],
        faq_en=[("Why is tracking stuck?", "Customs or carrier backlog — contact OrientDig if overdue.")],
    ),
    # NL extras
    _page(
        "orientdig-coupon-code",
        regions=["NL"],
        title_en=f"OrientDig Coupon Code NL ({YEAR})",
        desc_en="orientdig coupon code — Dutch guide to checking OrientDig promotions and browsing W2CLinks finds.",
        h1_en="OrientDig Coupon Code",
        cta=CTA_COUPONS,
        cta_href=SPREADSHEET,
        intro_nl="Couponcodes voor OrientDig wisselen — controleer altijd in je account. Finds browse je via W2CLinks.",
        intro_en="OrientDig coupon codes change frequently — verify at checkout. Browse finds on W2CLinks.",
        sections_en=[("NL tip", "Combine coupon checks with browsing newest finds on W2CLinks.")],
        faq_en=[("Gegarandeerd korting?", "Nee — promoties veranderen.")],
    ),
    _page(
        "orientdig-trustpilot",
        regions=["NL", "DE"],
        title_en=f"OrientDig Trustpilot & Reviews ({YEAR})",
        desc_en="orientdig trustpilot — evaluate reviews objectively alongside QC and shipping experience.",
        h1_en="OrientDig Trustpilot Guide",
        cta=CTA_VISIT,
        cta_href=REGISTER,
        intro_en="Read Trustpilot reviews critically — focus on recent shipping and QC themes.",
        sections_en=[("Balanced view", "Cross-check Reddit/Discord and your own QC photos.")],
        faq_en=[("Fake reviews?", "Use multiple sources; this site does not publish scores.")],
    ),
    _page(
        "cnfans-to-orientdig",
        regions=["NL"],
        title_en=f"CNFans to OrientDig: Agent Comparison Notes ({YEAR})",
        desc_en="cnfans to orientdig — neutral workflow comparison for Dutch shoppers choosing a China agent.",
        h1_en="CNFans to OrientDig: Comparison Notes",
        cta=CTA_SPREADSHEET,
        cta_href=SPREADSHEET,
        intro_en="Both are shopping agents with link paste, QC, and international shipping — compare fees and lines yourself.",
        sections_en=[("Neutral comparison", "We do not rank agents; browse finds on W2CLinks regardless of agent choice.")],
        faq_en=[("Which is better?", "Depends on fees, lines, and support — evaluate current terms.")],
    ),
    # DE extras
    _page(
        "orientdig-erfahrungen",
        regions=["DE", "AT"],
        title_en=f"OrientDig Erfahrungen ({YEAR}): Agent Guide",
        desc_en="orientdig erfahrungen — Erfahrungsberichte, QC, Versand und Spreadsheet-Finds über W2CLinks.",
        h1_de="OrientDig Erfahrungen",
        h1_en="OrientDig Erfahrungen",
        cta=CTA_SPREADSHEET,
        cta_href=SPREADSHEET,
        intro_de="OrientDig Erfahrungen hängen von Versandlinie, QC und Zoll ab — keine garantierten Lieferzeiten.",
        intro_en="OrientDig experiences vary by shipping line, QC, and customs.",
        sections_en=[("DE context", "Zoll und Einfuhrumsatzsteuer in Deutschland einplanen.")],
        faq_en=[("Sind Erfahrungen garantiert?", "Nein — individuelle Bestellungen variieren.")],
    ),
    _page(
        "orientdig-codes",
        regions=["DE", "AT"],
        title_en=f"OrientDig Codes & Gutscheine ({YEAR})",
        desc_en="orientdig codes — Gutscheine prüfen und Finds auf W2CLinks durchsuchen.",
        h1_de="OrientDig Codes",
        h1_en="OrientDig Codes",
        cta=CTA_COUPONS,
        cta_href=SPREADSHEET,
        intro_de="OrientDig Codes ändern sich — im Konto prüfen.",
        intro_en="OrientDig codes change — verify in account.",
        sections_en=[("Codes finden", "OrientDig Konto und Aktionen prüfen.")],
        faq_en=[("Fester Rabatt?", "Nein.")],
    ),
    _page(
        "qc-orientdig",
        regions=["DE", "AT"],
        title_en=f"QC OrientDig: Qualitätskontrolle ({YEAR})",
        desc_en="qc orientdig — QC-Fotos, Lagerprozess und Finds auf W2CLinks.",
        h1_de="QC OrientDig",
        h1_en="QC OrientDig",
        cta=CTA_VIEW_FINDS,
        cta_href=SPREADSHEET,
        intro_de="QC-Fotos zeigen erhaltene Artikel im OrientDig-Lager.",
        intro_en="QC photos show received items at OrientDig warehouse.",
        sections_en=[("QC prüfen", "Vor internationalem Versand Fotos sorgfältig prüfen.")],
        faq_en=[("QC überspringen?", "Nicht empfohlen.")],
    ),
    # IT extras
    _page(
        "spreadsheet-orientdig",
        regions=["IT", "FR"],
        title_en=f"Spreadsheet OrientDig: Browse Guide ({YEAR})",
        desc_en="spreadsheet orientdig — browse curated lists on W2CLinks with OrientDig ordering workflow.",
        h1_en="Spreadsheet OrientDig",
        cta=CTA_BROWSE,
        cta_href=SPREADSHEET,
        intro_it="spreadsheet orientdig — lista finds su W2CLinks, ordini su OrientDig.",
        intro_en="spreadsheet orientdig keyword maps to the W2CLinks browse hub.",
        sections_en=[("Keyword variant", "Same hub as orientdig spreadsheet — W2CLinks.")],
        faq_en=[("File Excel?", "No — web browse hub on W2CLinks.")],
    ),
    _page(
        "orientdig-coupon-codes",
        regions=["IT"],
        title_en=f"OrientDig Coupon Codes ({YEAR})",
        desc_en="orientdig coupon codes — check OrientDig promotions and browse W2CLinks finds.",
        h1_en="OrientDig Coupon Codes",
        cta=CTA_COUPONS,
        cta_href=SPREADSHEET,
        intro_it="Codici coupon OrientDig — verifica in checkout.",
        intro_en="OrientDig coupon codes — verify at checkout.",
        sections_en=[("Browse first", "Pick items on W2CLinks before applying codes.")],
        faq_en=[("Fixed discount?", "No — promotions vary.")],
    ),
    _page(
        "orientdig-reddit",
        regions=["IT"],
        title_en=f"OrientDig Reddit Community Guide ({YEAR})",
        desc_en="orientdig reddit — community finds discussion and W2CLinks spreadsheet browsing.",
        h1_en="OrientDig Reddit Guide",
        cta=CTA_BROWSE,
        cta_href=SPREADSHEET,
        intro_en="Reddit threads complement structured browsing on W2CLinks.",
        sections_en=[("Community tips", "Verify links and compare QC themes.")],
        faq_en=[("Official support?", "Use OrientDig help center for orders.")],
    ),
    # FR extras
    _page(
        "orientdig-discord",
        regions=["FR", "ES"],
        title_en=f"OrientDig Discord: Community Channels ({YEAR})",
        desc_en="orientdig discord — community discussion vs W2CLinks spreadsheet browsing.",
        h1_fr="OrientDig Discord",
        h1_en="OrientDig Discord",
        cta=CTA_BROWSE,
        cta_href=SPREADSHEET,
        intro_fr="Discord orientdig — discussions communautaires ; finds structurés sur W2CLinks.",
        intro_en="orientdig discord searches reflect community channels — browse lists on W2CLinks.",
        intro_es="orientdig discord — canales comunitarios; finds estructurados en W2CLinks.",
        sections_en=[("Discord vs guide", "Not official support.")],
        faq_en=[("Lien Discord officiel?", "Vérifiez les sources communautaires.")],
    ),
    _page(
        "orientdig-coupon",
        regions=["FR"],
        title_en=f"OrientDig Coupon: Codes Promo ({YEAR})",
        desc_en="orientdig coupon — codes promo et finds sur W2CLinks.",
        h1_fr="OrientDig Coupon",
        h1_en="OrientDig Coupon",
        cta=CTA_COUPONS,
        cta_href=SPREADSHEET,
        intro_fr="Coupons OrientDig — vérifiez les conditions au checkout.",
        intro_en="OrientDig coupon — verify terms at checkout.",
        sections_en=[("Promo", "Les offres changent sans garantie.")],
        faq_en=[("Réduction fixe?", "Non.")],
    ),
    _page(
        "avis-orientdig",
        regions=["FR"],
        title_en=f"Avis OrientDig ({YEAR}): Guide Indépendant",
        desc_en="avis orientdig — évaluer l'agent sans notes fabriquées ; finds via W2CLinks.",
        h1_fr="Avis OrientDig",
        h1_en="Avis OrientDig",
        cta=CTA_VISIT,
        cta_href=REGISTER,
        intro_fr="Avis orientdig — lisez QC, livraison et support ; pas de notes inventées ici.",
        intro_en="avis orientdig — evaluate QC, shipping, support; no fake ratings here.",
        sections_en=[("Sources", "Trustpilot, Reddit, Discord — croisez les avis récents.")],
        faq_en=[("Site officiel?", "Non — guide indépendant.")],
    ),
    _page(
        "orientdig-fiable",
        regions=["FR"],
        title_en=f"OrientDig Fiable ? Sécurité et Risques ({YEAR})",
        desc_en="orientdig fiable — agent d'achat, QC, paiement et risques transfrontaliers.",
        h1_fr="OrientDig Fiable ?",
        h1_en="OrientDig Fiable?",
        cta=CTA_START,
        cta_href=SPREADSHEET,
        intro_fr="OrientDig fiable dépend du workflow agent — pas de promesse zéro risque.",
        intro_en="Fiable depends on agent workflow — not zero risk.",
        sections_en=[("Risques", "Douanes, délais, QC — à comprendre avant commande.")],
        faq_en=[("100% sûr?", "Non pour tout achat international.")],
    ),
    _page(
        "livraison-orientdig",
        regions=["FR"],
        title_en=f"Livraison OrientDig: Délais et Process ({YEAR})",
        desc_en="livraison orientdig — entrepôt, QC, lignes d'expédition et délais réalistes.",
        h1_fr="Livraison OrientDig",
        h1_en="Livraison OrientDig",
        cta=CTA_ESTIMATE,
        cta_href=SPREADSHEET,
        intro_fr="Livraison orientdig — délais variables selon ligne et douanes.",
        intro_en="Shipping timelines vary by line and customs.",
        sections_en=[("Process", "Achat → QC → colis → suivi.")],
        faq_en=[("Délai fixe?", "Non garanti.")],
    ),
    _page(
        "guide-orientdig",
        regions=["FR"],
        title_en=f"Guide OrientDig: Tableur et Commandes ({YEAR})",
        desc_en="guide orientdig — tableur OrientDig sur W2CLinks et tutoriel agent.",
        h1_fr="Guide OrientDig",
        h1_en="Guide OrientDig",
        cta=CTA_SEARCH,
        cta_href=SPREADSHEET,
        intro_fr="Guide orientdig — tableur sur W2CLinks, commandes sur OrientDig.",
        intro_en="Full guide — spreadsheet on W2CLinks, orders on OrientDig.",
        sections_en=[("Tableur", "Mot-clé EN orientdig spreadsheet ; explications FR ici.")],
        faq_en=[("Tableur local?", "Non — hub W2CLinks.")],
    ),
    # ES extras
    _page(
        "como-comprar-en-orientdig",
        regions=["ES"],
        title_en=f"Cómo Comprar en OrientDig ({YEAR})",
        desc_en="como comprar en orientdig — guía paso a paso para spreadsheet, QC y envío internacional.",
        h1_es="Cómo Comprar en OrientDig",
        h1_en="Cómo Comprar en OrientDig",
        cta=CTA_START,
        cta_href=SPREADSHEET,
        intro_es=(
            "como comprar en orientdig — busca finds en W2CLinks, pega el enlace en OrientDig, "
            "revisa QC y envía el paquete a España."
        ),
        intro_en="Spanish how-to-buy guide for OrientDig spreadsheet workflow via W2CLinks.",
        sections_en=[
            (
                "Pasos básicos",
                "1) Buscar en W2CLinks spreadsheet. 2) Copiar enlace del producto. "
                "3) Pegar en OrientDig y pagar. 4) Revisar fotos QC. 5) Enviar paquete.",
            ),
            (
                "Aduanas en España",
                "Presupuesta IVA y posibles tasas de importación según valor declarado y línea de envío.",
            ),
        ],
        faq_en=[
            ("¿Es seguro comprar?", "Usa QC y entiende los riesgos de compras internacionales."),
            ("¿Dónde está el spreadsheet?", f"En W2CLinks: {SPREADSHEET}"),
        ],
    ),
    _page(
        "orientdig-shipping-coupons",
        regions=["ES"],
        title_en=f"OrientDig Shipping Coupons ({YEAR})",
        desc_en="orientdig shipping coupons — promociones de envío y finds en W2CLinks.",
        h1_es="OrientDig Shipping Coupons",
        h1_en="OrientDig Shipping Coupons",
        cta=CTA_COUPONS,
        cta_href=SPREADSHEET,
        intro_es="Cupones de envío OrientDig — verifica condiciones en checkout; busca finds en W2CLinks.",
        intro_en="Shipping coupon intent — verify promotions on OrientDig at checkout.",
        sections_en=[
            ("Cupones de envío", "Las promociones cambian; confirma en tu cuenta OrientDig."),
            ("Browse first", "Encuentra productos en W2CLinks antes de aplicar cupones."),
        ],
        faq_en=[
            ("¿Descuento fijo?", "No — las promociones varían."),
            ("¿Combinar con spreadsheet?", "Sí — elige items en W2CLinks y aplica cupones al pagar."),
        ],
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
