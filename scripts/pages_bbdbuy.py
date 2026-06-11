"""Page metadata and content for BBDBuy Spreadsheet cluster."""

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

CTA_SPREADSHEET = "Open BBDBuy Spreadsheet"
CTA_BROWSE = "Browse Spreadsheet"
CTA_FINDS = "See Latest Finds"
CTA_COUPONS = "Check BBDBuy Coupons"
CTA_START = "Start on BBDBuy"
CTA_OPEN = "Open BBDBuy"
CTA_SEARCH = "Search Products on BBDBuy"
CTA_VISIT = "Visit BBDBuy Platform"
CTA_VIEW_FINDS = "View Finds on BBDBuy"
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
        title_en=f"BBDBuy Spreadsheet Guide: Finds, Coupons & Shipping ({YEAR})",
        desc_en="Use this BBDBuy spreadsheet guide to browse curated finds, coupon tips, shipping basics, and QC workflow. Product links open on W2CLinks.",
        h1_en="BBDBuy Spreadsheet: Finds, Coupons and Shipping Guide",
        cta=CTA_SPREADSHEET,
        cta_href=SPREADSHEET,
        intro_en=(
            "BBDBuy is a China shopping agent for Taobao, 1688, and Weidian. "
            "This guide explains how spreadsheet-style product lists and finds work, "
            "and links you to browse entries on W2CLinks — not a fake local database."
        ),
        sections_en=[
            (
                "What this spreadsheet guide covers",
                "Searchers looking for an bbdbuy spreadsheet usually want a browsable list of "
                "community finds with links to source items. W2CLinks hosts the spreadsheet hub "
                f"at <a href=\"{SPREADSHEET}\" target=\"_blank\" rel=\"noopener\">w2clinks.com/spreadsheet/</a> "
                "where you can filter by category, brand, or keyword.",
            ),
            (
                "How BBDBuy fits in",
                f"After you pick an item, you purchase through BBDBuy ({PLATFORM}). "
                "BBDBuy buys from Chinese marketplaces, performs QC photos in warehouse, "
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
                "Is this the official BBDBuy spreadsheet?",
                "No. This is an independent guide site. Spreadsheet and find links are provided through W2CLinks.",
            ),
            (
                "How do I open the BBDBuy spreadsheet?",
                f"Use the Open BBDBuy Spreadsheet button to go to {SPREADSHEET}",
            ),
            (
                "Does BBDBuy support Taobao and 1688?",
                "Yes. BBDBuy accepts product links and keyword search from Taobao, Tmall, 1688, and Weidian.",
            ),
        ],
        title_nl="BBDBuy Spreadsheet: Finds, Coupons en Verzending ({})".format(YEAR),
        desc_nl="Gids voor bbdbuy spreadsheet: finds, coupons en verzending. Links openen op W2CLinks.",
        h1_nl="BBDBuy Spreadsheet: Finds, Coupons en Verzending",
        intro_nl=(
            "BBDBuy is een China shopping agent voor Taobao, 1688 en Weidian. "
            "Deze gids legt spreadsheet/finds uit; productlinks openen op W2CLinks."
        ),
        title_de="BBDBuy Spreadsheet: Finds, Gutscheine & Versand ({})".format(YEAR),
        desc_de="BBDBuy Spreadsheet Guide: Finds, Gutscheine und Versand. Produktlinks führen zu W2CLinks.",
        h1_de="BBDBuy Spreadsheet: Finds, Gutscheine und Versand",
        intro_de=(
            "BBDBuy ist ein China Shopping Agent für Taobao, 1688 und Weidian. "
            "Diese Seite erklärt Spreadsheet/Finds; Links führen zu W2CLinks."
        ),
        title_it="BBDBuy Spreadsheet: Finds, Coupon e Spedizione ({})".format(YEAR),
        desc_it="Guida bbdbuy spreadsheet: finds, coupon e spedizione. I link prodotti aprono su W2CLinks.",
        h1_it="BBDBuy Spreadsheet: Finds, Coupon e Spedizione",
        intro_it=(
            "BBDBuy è un agente di shopping cinese per Taobao, 1688 e Weidian. "
            "Questa guida spiega spreadsheet/finds; i link aprono su W2CLinks."
        ),
        title_fr="BBDBuy Spreadsheet : Finds, Coupons et Livraison ({})".format(YEAR),
        desc_fr="Guide bbdbuy spreadsheet : finds, coupons et livraison. Les liens produits passent par W2CLinks.",
        h1_fr="BBDBuy Spreadsheet : Finds, Coupons et Livraison",
        intro_fr=(
            "BBDBuy est un agent d'achat Chine pour Taobao, 1688 et Weidian. "
            "Ce guide explique le tableur/finds ; les liens produits passent par W2CLinks."
        ),
        title_es=f"BBDBuy Spreadsheet: Finds, Cupones y Envíos ({YEAR})",
        desc_es="Guía bbdbuy spreadsheet: finds, cupones y envíos. Los enlaces de productos abren en W2CLinks.",
        h1_es="BBDBuy Spreadsheet: Finds, Cupones y Envíos",
        intro_es=(
            "BBDBuy es un agente de compras en China para Taobao, 1688 y Weidian. "
            "Esta guía explica spreadsheet/finds; los enlaces de productos abren en W2CLinks."
        ),
    ),
    _page(
        "bbdbuy-spreadsheet",
        title_en=f"BBDBuy Spreadsheet: Browse Product Lists ({YEAR})",
        desc_en="bbdbuy spreadsheet — browse curated product lists with filters on W2CLinks, then order via BBDBuy.",
        h1_en="BBDBuy Spreadsheet",
        cta=CTA_BROWSE,
        cta_href=SPREADSHEET,
        intro_en=(
            "The bbdbuy spreadsheet keyword maps to the W2CLinks browse hub — filter by category, "
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
            ("Where do I order?", f"After picking an item, purchase through BBDBuy ({PLATFORM})."),
        ],
        title_es=f"BBDBuy Spreadsheet: Listas de Productos ({YEAR})",
        desc_es="bbdbuy spreadsheet — explora listas de finds en W2CLinks y compra via BBDBuy.",
        h1_es="BBDBuy Spreadsheet",
        intro_es="bbdbuy spreadsheet lleva al hub W2CLinks — filtra por categoría, marca o palabra clave.",
        title_fr="BBDBuy Spreadsheet : Parcourir les Finds ({})".format(YEAR),
        h1_fr="BBDBuy Spreadsheet",
        intro_fr="Le mot-clé bbdbuy spreadsheet mène au hub W2CLinks — filtres par catégorie et marque.",
        title_de="BBDBuy Spreadsheet: Produktlisten ({})".format(YEAR),
        h1_de="BBDBuy Spreadsheet",
        intro_de="bbdbuy spreadsheet führt zum W2CLinks-Hub — nach Kategorie, Marke oder Keyword filtern.",
    ),
    _page(
        "bbdbuy-spreadsheets",
        title_en=f"BBDBuy Spreadsheets: Browse Lists & Finds ({YEAR})",
        desc_en="bbdbuy spreadsheets explained — plural search guide for browsing multiple find lists on W2CLinks.",
        h1_en="BBDBuy Spreadsheets: Browse Lists and Finds",
        cta=CTA_BROWSE,
        cta_href=SPREADSHEET,
        intro_en="People search bbdbuy spreadsheets (plural) when they want multiple curated lists, not a single file.",
        sections_en=[
            (
                "Spreadsheet vs spreadsheets",
                "Singular bbdbuy spreadsheet often means the main hub. Plural spreadsheets refers to "
                "category slices, brand lists, and seasonal find collections — all browsable on W2CLinks.",
            ),
            (
                "Browse by intent",
                f"Try keyword search: <a href=\"{product_search_url('jordan')}\" target=\"_blank\" rel=\"noopener\">jordan finds</a> "
                f"or <a href=\"{product_search_url('dunk')}\" target=\"_blank\" rel=\"noopener\">dunk finds</a>.",
            ),
        ],
        faq_en=[
            ("Are there multiple BBDBuy spreadsheets?", "Community find lists are aggregated on W2CLinks spreadsheet hub."),
            ("Where do spreadsheets link to?", f"All browse CTAs go to {SPREADSHEET}"),
        ],
    ),
    _page(
        "bbdbuy-finds",
        title_en=f"BBDBuy Finds: Latest Product Discovery ({YEAR})",
        desc_en="bbdbuy finds guide — how community product discovery works and where to browse latest entries on W2CLinks.",
        h1_en="BBDBuy Finds: Latest Product Discovery",
        cta=CTA_FINDS,
        cta_href=SPREADSHEET,
        intro_en="bbdbuy finds covers QC-backed product discoveries shared by shoppers — browse them on W2CLinks, order via BBDBuy.",
        sections_en=[
            (
                "What are finds?",
                "Finds are curated product entries with source links, often organized like a spreadsheet. "
                "They help you discover items before pasting links into BBDBuy.",
            ),
            (
                "Search finds on W2CLinks",
                f"Open <a href=\"{SPREADSHEET}\" target=\"_blank\" rel=\"noopener\">W2CLinks spreadsheet</a> "
                "and sort by newest to see recent additions.",
            ),
        ],
        faq_en=[
            ("Are finds stored on this site?", "No. This site is a guide; finds live on W2CLinks spreadsheet."),
            ("How do I buy a find?", "Copy the source link into BBDBuy, pay, wait for QC, then ship."),
        ],
    ),
    _page(
        "bbdbuy-coupons",
        title_en=f"BBDBuy Coupons & Bonus Codes ({YEAR})",
        desc_en="bbdbuy coupons and shipping bonus tips — check current promotions on BBDBuy and browse deals on W2CLinks.",
        h1_en="BBDBuy Coupons and Bonus Codes",
        cta=CTA_COUPONS,
        cta_href=SPREADSHEET,
        intro_en="Coupon availability changes. This page explains how BBDBuy coupons work without promising fixed discounts.",
        sections_en=[
            (
                "Where coupons appear",
                f"BBDBuy may show registration or shipping coupons inside <a href=\"{PLATFORM}\" target=\"_blank\" rel=\"noopener\">orientdig.com</a>. "
                "Always verify terms in your account before checkout.",
            ),
            (
                "Browse deal categories",
                f"Use W2CLinks spreadsheet to find items first: <a href=\"{SPREADSHEET}\" target=\"_blank\" rel=\"noopener\">open spreadsheet</a>.",
            ),
        ],
        faq_en=[
            ("Are coupon codes guaranteed?", "No. Promotions change; verify on BBDBuy at checkout."),
            ("Can I stack spreadsheet browsing with coupons?", "Yes — pick items on W2CLinks, then apply eligible BBDBuy coupons when paying."),
        ],
    ),
    _page(
        "is-bbdbuy-legit",
        title_en=f"Is BBDBuy Legit? Agent Workflow Explained ({YEAR})",
        desc_en="Is bbdbuy legit — objective guide to BBDBuy shopping agent workflow, payments, QC, warehouse storage, and risks.",
        h1_en="Is BBDBuy Legit?",
        cta=CTA_START,
        cta_href=SPREADSHEET,
        intro_en="BBDBuy operates as a China shopping agent. Legitimacy depends on following standard agent workflow and understanding cross-border risks.",
        sections_en=[
            (
                "How the agent model works",
                "You pay BBDBuy to purchase from Taobao/1688/Weidian sellers. Items arrive at BBDBuy warehouse for QC photos. "
                "You then choose international shipping lines.",
            ),
            (
                "What to verify yourself",
                "Check payment method protection, read QC photos carefully, understand return limits on Chinese marketplaces, "
                "and budget for customs duties in your country.",
            ),
        ],
        faq_en=[
            ("Is BBDBuy an official marketplace?", "No. It is a third-party purchasing agent, not Taobao itself."),
            ("Can orders fail?", "Yes — seller delays, QC issues, customs holds, and shipping disruptions can occur."),
        ],
    ),
    _page(
        "is-bbdbuy-safe",
        title_en=f"Is BBDBuy Safe? Payments, QC & Risk FAQ ({YEAR})",
        desc_en="Is bbdbuy safe — FAQ on account security, payment methods, QC process, and realistic cross-border shopping risks.",
        h1_en="Is BBDBuy Safe?",
        cta=CTA_OPEN,
        cta_href=SPREADSHEET,
        intro_en="Safety means understanding agent escrow flow, QC inspection, and that no cross-border purchase is risk-free.",
        sections_en=[
            (
                "Account and payment safety",
                "Use strong passwords and enable any available account protections on BBDBuy. "
                "Prefer payment methods with buyer dispute options where available.",
            ),
            (
                "QC as your checkpoint",
                "Warehouse QC photos let you approve or reject items before international shipping — use this step.",
            ),
        ],
        faq_en=[
            ("Is shopping through an agent 100% safe?", "No cross-border agent purchase is risk-free."),
            ("What if QC fails?", "You may exchange or refund per BBDBuy policy before shipping — check current terms."),
        ],
    ),
    _page(
        "bbdbuy-shipping",
        title_en=f"BBDBuy Shipping Times, Lines & Process ({YEAR})",
        desc_en="bbdbuy shipping guide — warehouse storage, parcel submission, line selection, and realistic delivery timelines.",
        h1_en="BBDBuy Shipping: Times, Lines and Process",
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
            ("How long does BBDBuy shipping take?", "Varies by line and destination — often weeks, not days."),
            ("Are duties included?", "Usually not. Import taxes may apply in your country."),
        ],
    ),
    _page(
        "bbdbuy-qc",
        title_en=f"BBDBuy QC Photos & Warehouse Inspection ({YEAR})",
        desc_en="bbdbuy qc guide — quality check photos, warehouse inspection workflow, and how finds relate to QC on W2CLinks.",
        h1_en="BBDBuy QC: Warehouse Inspection Guide",
        cta=CTA_VIEW_FINDS,
        cta_href=SPREADSHEET,
        intro_en="QC (quality check) photos are taken when items arrive at BBDBuy warehouse — your chance to verify before shipping.",
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
            ("What is qc bbdbuy search intent?", "Users want sample QC photos and process explanation — covered here."),
        ],
    ),
    _page(
        "how-to-use-bbdbuy",
        title_en=f"How to Use BBDBuy: Order Tutorial ({YEAR})",
        desc_en="How to order on BBDBuy — paste links, search keywords, pay, QC review, and submit international shipping.",
        h1_en="How to Use BBDBuy: Step-by-Step",
        cta=CTA_SEARCH,
        cta_href=SPREADSHEET,
        intro_en="BBDBuy lets you paste Taobao/Tmall/1688/Weidian links or search by keyword/image before purchasing.",
        sections_en=[
            (
                "Step 1 — Find products",
                f"Browse <a href=\"{SPREADSHEET}\" target=\"_blank\" rel=\"noopener\">W2CLinks spreadsheet</a> or paste a marketplace link into BBDBuy.",
            ),
            (
                "Step 2 — Pay and wait for QC",
                "Complete payment on BBDBuy. Wait for warehouse inbound and QC photos.",
            ),
            (
                "Step 3 — Ship internationally",
                "Approve QC, select a shipping line, pay freight, track parcel.",
            ),
        ],
        faq_en=[
            ("Can I search by image?", "BBDBuy help center mentions image search — check current app/web features."),
            ("Do I need an account?", "Yes, register on BBDBuy before placing orders."),
        ],
    ),
    _page(
        "bbdbuy-review",
        title_en=f"BBDBuy Reviews & Trust Signals ({YEAR})",
        desc_en="bbdbuy reviews guide — how to evaluate Trustpilot, Reddit threads, and QC evidence without fake ratings.",
        h1_en="BBDBuy Reviews and Trust Signals",
        cta=CTA_VISIT,
        cta_href=REGISTER,
        intro_en="This page does not display fabricated star ratings. Use multiple trust signals and your own QC review.",
        sections_en=[
            (
                "Where shoppers discuss BBDBuy",
                "Reddit, Discord, and review platforms — read recent posts about shipping lines and QC quality.",
            ),
            (
                "Browse finds while researching",
                f"Compare community picks on <a href=\"{SPREADSHEET}\" target=\"_blank\" rel=\"noopener\">W2CLinks spreadsheet</a>.",
            ),
        ],
        faq_en=[
            ("Does this site publish fake Trustpilot scores?", "No. We link to BBDBuy and encourage independent verification."),
            ("What matters most?", "QC photo review, shipping line choice, and realistic customs expectations."),
        ],
    ),
    # UK extras
    _page(
        "what-is-bbdbuy",
        regions=["UK"],
        title_en=f"What Is BBDBuy? China Shopping Agent Explained ({YEAR})",
        desc_en="What is BBDBuy — UK-focused explainer for Taobao, 1688, Weidian agent shopping and spreadsheet finds.",
        h1_en="What Is BBDBuy?",
        cta=CTA_SPREADSHEET,
        cta_href=SPREADSHEET,
        intro_en="BBDBuy is a China shopping agent helping UK buyers source from Taobao, 1688, and Weidian with QC and international shipping.",
        sections_en=[("UK buyer context", "Budget for VAT/duty where applicable. Use QC before shipping to avoid costly mistakes.")],
        faq_en=[("Is BBDBuy a UK company?", "It is a cross-border agent serving international buyers including the UK.")],
    ),
    _page(
        "how-long-does-bbdbuy-take-to-ship",
        regions=["UK"],
        title_en=f"How Long Does BBDBuy Take to Ship to the UK? ({YEAR})",
        desc_en="How long does bbdbuy take to ship — UK delivery timelines, customs, and line selection tips.",
        h1_en="How Long Does BBDBuy Take to Ship?",
        cta=CTA_ESTIMATE,
        cta_href=SPREADSHEET,
        intro_en="UK delivery time depends on shipping line, season, and HMRC processing — no fixed guarantee.",
        sections_en=[("Realistic planning", "Many lines take several weeks total after parcel submission.")],
        faq_en=[("Does Royal Mail handle last mile?", "Depends on line — check BBDBuy tracking details.")],
    ),
    _page(
        "bbdbuy-spreadsheet-reddit",
        regions=["UK"],
        title_en=f"BBDBuy Spreadsheet Reddit Threads ({YEAR})",
        desc_en="bbdbuy spreadsheet reddit — how UK shoppers use Reddit finds and W2CLinks spreadsheet together.",
        h1_en="BBDBuy Spreadsheet Reddit Guide",
        cta=CTA_BROWSE,
        cta_href=SPREADSHEET,
        intro_en="Reddit communities share BBDBuy finds; W2CLinks spreadsheet organizes browsable lists with filters.",
        sections_en=[("Using both", "Read Reddit for tips, browse W2CLinks for structured search.")],
        faq_en=[("Is Reddit official?", "No — community discussion, not BBDBuy support.")],
    ),
    # US extras
    _page(
        "best-bbdbuy-spreadsheet",
        regions=["US"],
        title_en=f"Best BBDBuy Spreadsheet Browse Tips ({YEAR})",
        desc_en="best bbdbuy spreadsheet — US guide to filtering finds, categories, and brands on W2CLinks.",
        h1_en="Best BBDBuy Spreadsheet Browse Tips",
        cta=CTA_BROWSE,
        cta_href=SPREADSHEET,
        intro_en="The best bbdbuy spreadsheet experience is filtered browsing on W2CLinks — sort by newest and use category filters.",
        sections_en=[("US shopper tips", "Factor US customs and use QC before consolidating heavy parcels.")],
        faq_en=[("Is there one official best list?", "No single list — browse categories and keywords on W2CLinks.")],
    ),
    _page(
        "bbdbuy-spreadsheet-2026",
        regions=["US"],
        title_en=f"BBDBuy Spreadsheet {YEAR}: Updated Finds Hub",
        desc_en=f"bbdbuy spreadsheet {YEAR} — current W2CLinks hub for US shoppers browsing newest finds.",
        h1_en=f"BBDBuy Spreadsheet {YEAR}",
        cta=CTA_SPREADSHEET,
        cta_href=SPREADSHEET,
        intro_en=f"{YEAR} find lists update continuously on W2CLinks — this guide links to the live hub.",
        sections_en=[("Stay current", "Sort by newest on W2CLinks rather than static reposts.")],
        faq_en=[("Is this a downloadable file?", "No — it is a browsable web hub on W2CLinks.")],
    ),
    _page(
        "bbdbuy-shipping-calculator",
        regions=["US"],
        title_en=f"BBDBuy Shipping Calculator & Line Selection ({YEAR})",
        desc_en="bbdbuy shipping calculator — estimate freight on BBDBuy and browse items on W2CLinks first.",
        h1_en="BBDBuy Shipping Calculator Guide",
        cta=CTA_ESTIMATE,
        cta_href=SPREADSHEET,
        intro_en="Use BBDBuy's freight estimator when submitting parcels; browse products on W2CLinks beforehand.",
        sections_en=[("Calculator tips", "Weigh consolidated parcels and compare lines inside BBDBuy checkout.")],
        faq_en=[("Are calculator results final?", "Estimates may change after re-weigh at warehouse.")],
    ),
    _page(
        "bbdbuy-customer-service",
        regions=["US"],
        title_en=f"BBDBuy Customer Service & Support Channels ({YEAR})",
        desc_en="bbdbuy customer service — tickets, help center, and when to contact BBDBuy vs browse W2CLinks finds.",
        h1_en="BBDBuy Customer Service",
        cta=CTA_VISIT,
        cta_href=REGISTER,
        intro_en="Order issues go to BBDBuy support; product discovery questions may be answered via W2CLinks browse.",
        sections_en=[("Support scope", "Shipping delays, QC disputes, and payment issues — use BBDBuy tickets.")],
        faq_en=[("Does this site provide support?", "No — independent guide; contact BBDBuy for orders.")],
    ),
    _page(
        "bbdbuy-payment-methods",
        regions=["US"],
        title_en=f"BBDBuy Payment Methods FAQ ({YEAR})",
        desc_en="bbdbuy payment methods — cards, wallets, and checkout tips for US buyers.",
        h1_en="BBDBuy Payment Methods",
        cta=CTA_START,
        cta_href=SPREADSHEET,
        intro_en="Available payment methods depend on BBDBuy account region and current checkout options.",
        sections_en=[("Before paying", "Confirm total includes service fees and expected domestic China shipping.")],
        faq_en=[("Are all US cards accepted?", "Check BBDBuy checkout for your card/wallet availability.")],
    ),
    _page(
        "bbdbuy-tracking",
        regions=["US"],
        title_en=f"BBDBuy Tracking: Parcel Status Guide ({YEAR})",
        desc_en="bbdbuy tracking — how to follow warehouse, international line, and last-mile tracking.",
        h1_en="BBDBuy Tracking Guide",
        cta=CTA_OPEN,
        cta_href=REGISTER,
        intro_en="Tracking numbers appear after parcel submission — stages include warehouse processing and line handoff.",
        sections_en=[("Tracking gaps", "Delays between scans are common on economy lines.")],
        faq_en=[("Why is tracking stuck?", "Customs or carrier backlog — contact BBDBuy if overdue.")],
    ),
    # NL extras
    _page(
        "bbdbuy-coupon-code",
        regions=["NL"],
        title_en=f"BBDBuy Coupon Code NL ({YEAR})",
        desc_en="bbdbuy coupon code — Dutch guide to checking BBDBuy promotions and browsing W2CLinks finds.",
        h1_en="BBDBuy Coupon Code",
        cta=CTA_COUPONS,
        cta_href=SPREADSHEET,
        intro_nl="Couponcodes voor BBDBuy wisselen — controleer altijd in je account. Finds browse je via W2CLinks.",
        intro_en="BBDBuy coupon codes change frequently — verify at checkout. Browse finds on W2CLinks.",
        sections_en=[("NL tip", "Combine coupon checks with browsing newest finds on W2CLinks.")],
        faq_en=[("Gegarandeerd korting?", "Nee — promoties veranderen.")],
    ),
    _page(
        "bbdbuy-trustpilot",
        regions=["NL", "DE"],
        title_en=f"BBDBuy Trustpilot & Reviews ({YEAR})",
        desc_en="bbdbuy trustpilot — evaluate reviews objectively alongside QC and shipping experience.",
        h1_en="BBDBuy Trustpilot Guide",
        cta=CTA_VISIT,
        cta_href=REGISTER,
        intro_en="Read Trustpilot reviews critically — focus on recent shipping and QC themes.",
        sections_en=[("Balanced view", "Cross-check Reddit/Discord and your own QC photos.")],
        faq_en=[("Fake reviews?", "Use multiple sources; this site does not publish scores.")],
    ),
    _page(
        "cnfans-to-bbdbuy",
        regions=["NL"],
        title_en=f"CNFans to BBDBuy: Agent Comparison Notes ({YEAR})",
        desc_en="cnfans to bbdbuy — neutral workflow comparison for Dutch shoppers choosing a China agent.",
        h1_en="CNFans to BBDBuy: Comparison Notes",
        cta=CTA_SPREADSHEET,
        cta_href=SPREADSHEET,
        intro_en="Both are shopping agents with link paste, QC, and international shipping — compare fees and lines yourself.",
        sections_en=[("Neutral comparison", "We do not rank agents; browse finds on W2CLinks regardless of agent choice.")],
        faq_en=[("Which is better?", "Depends on fees, lines, and support — evaluate current terms.")],
    ),
    # DE extras
    _page(
        "bbdbuy-erfahrungen",
        regions=["DE", "AT"],
        title_en=f"BBDBuy Erfahrungen ({YEAR}): Agent Guide",
        desc_en="bbdbuy erfahrungen — Erfahrungsberichte, QC, Versand und Spreadsheet-Finds über W2CLinks.",
        h1_de="BBDBuy Erfahrungen",
        h1_en="BBDBuy Erfahrungen",
        cta=CTA_SPREADSHEET,
        cta_href=SPREADSHEET,
        intro_de="BBDBuy Erfahrungen hängen von Versandlinie, QC und Zoll ab — keine garantierten Lieferzeiten.",
        intro_en="BBDBuy experiences vary by shipping line, QC, and customs.",
        sections_en=[("DE context", "Zoll und Einfuhrumsatzsteuer in Deutschland einplanen.")],
        faq_en=[("Sind Erfahrungen garantiert?", "Nein — individuelle Bestellungen variieren.")],
    ),
    _page(
        "bbdbuy-codes",
        regions=["DE", "AT"],
        title_en=f"BBDBuy Codes & Gutscheine ({YEAR})",
        desc_en="bbdbuy codes — Gutscheine prüfen und Finds auf W2CLinks durchsuchen.",
        h1_de="BBDBuy Codes",
        h1_en="BBDBuy Codes",
        cta=CTA_COUPONS,
        cta_href=SPREADSHEET,
        intro_de="BBDBuy Codes ändern sich — im Konto prüfen.",
        intro_en="BBDBuy codes change — verify in account.",
        sections_en=[("Codes finden", "BBDBuy Konto und Aktionen prüfen.")],
        faq_en=[("Fester Rabatt?", "Nein.")],
    ),
    _page(
        "qc-bbdbuy",
        regions=["DE", "AT"],
        title_en=f"QC BBDBuy: Qualitätskontrolle ({YEAR})",
        desc_en="qc bbdbuy — QC-Fotos, Lagerprozess und Finds auf W2CLinks.",
        h1_de="QC BBDBuy",
        h1_en="QC BBDBuy",
        cta=CTA_VIEW_FINDS,
        cta_href=SPREADSHEET,
        intro_de="QC-Fotos zeigen erhaltene Artikel im BBDBuy-Lager.",
        intro_en="QC photos show received items at BBDBuy warehouse.",
        sections_en=[("QC prüfen", "Vor internationalem Versand Fotos sorgfältig prüfen.")],
        faq_en=[("QC überspringen?", "Nicht empfohlen.")],
    ),
    # IT extras
    _page(
        "spreadsheet-bbdbuy",
        regions=["IT", "FR"],
        title_en=f"Spreadsheet BBDBuy: Browse Guide ({YEAR})",
        desc_en="spreadsheet bbdbuy — browse curated lists on W2CLinks with BBDBuy ordering workflow.",
        h1_en="Spreadsheet BBDBuy",
        cta=CTA_BROWSE,
        cta_href=SPREADSHEET,
        intro_it="spreadsheet bbdbuy — lista finds su W2CLinks, ordini su BBDBuy.",
        intro_en="spreadsheet bbdbuy keyword maps to the W2CLinks browse hub.",
        sections_en=[("Keyword variant", "Same hub as bbdbuy spreadsheet — W2CLinks.")],
        faq_en=[("File Excel?", "No — web browse hub on W2CLinks.")],
    ),
    _page(
        "bbdbuy-coupon-codes",
        regions=["IT"],
        title_en=f"BBDBuy Coupon Codes ({YEAR})",
        desc_en="bbdbuy coupon codes — check BBDBuy promotions and browse W2CLinks finds.",
        h1_en="BBDBuy Coupon Codes",
        cta=CTA_COUPONS,
        cta_href=SPREADSHEET,
        intro_it="Codici coupon BBDBuy — verifica in checkout.",
        intro_en="BBDBuy coupon codes — verify at checkout.",
        sections_en=[("Browse first", "Pick items on W2CLinks before applying codes.")],
        faq_en=[("Fixed discount?", "No — promotions vary.")],
    ),
    _page(
        "bbdbuy-reddit",
        regions=["IT"],
        title_en=f"BBDBuy Reddit Community Guide ({YEAR})",
        desc_en="bbdbuy reddit — community finds discussion and W2CLinks spreadsheet browsing.",
        h1_en="BBDBuy Reddit Guide",
        cta=CTA_BROWSE,
        cta_href=SPREADSHEET,
        intro_en="Reddit threads complement structured browsing on W2CLinks.",
        sections_en=[("Community tips", "Verify links and compare QC themes.")],
        faq_en=[("Official support?", "Use BBDBuy help center for orders.")],
    ),
    # FR extras
    _page(
        "bbdbuy-discord",
        regions=None,
        title_en=f"BBDBuy Discord: Community Channels ({YEAR})",
        desc_en="bbdbuy discord — community discussion vs W2CLinks spreadsheet browsing.",
        h1_fr="BBDBuy Discord",
        h1_en="BBDBuy Discord",
        cta=CTA_BROWSE,
        cta_href=SPREADSHEET,
        intro_fr="Discord bbdbuy — discussions communautaires ; finds structurés sur W2CLinks.",
        intro_en="bbdbuy discord searches reflect community channels — browse lists on W2CLinks.",
        intro_es="bbdbuy discord — canales comunitarios; finds estructurados en W2CLinks.",
        sections_en=[("Discord vs guide", "Not official support.")],
        faq_en=[("Lien Discord officiel?", "Vérifiez les sources communautaires.")],
    ),
    _page(
        "bbdbuy-coupon",
        regions=None,
        title_en=f"BBDBuy Coupon: Codes Promo ({YEAR})",
        desc_en="bbdbuy coupon — codes promo et finds sur W2CLinks.",
        h1_fr="BBDBuy Coupon",
        h1_en="BBDBuy Coupon",
        cta=CTA_COUPONS,
        cta_href=SPREADSHEET,
        intro_fr="Coupons BBDBuy — vérifiez les conditions au checkout.",
        intro_en="BBDBuy coupon — verify terms at checkout.",
        sections_en=[("Promo", "Les offres changent sans garantie.")],
        faq_en=[("Réduction fixe?", "Non.")],
    ),
    _page(
        "avis-bbdbuy",
        regions=["FR"],
        title_en=f"Avis BBDBuy ({YEAR}): Guide Indépendant",
        desc_en="avis bbdbuy — évaluer l'agent sans notes fabriquées ; finds via W2CLinks.",
        h1_fr="Avis BBDBuy",
        h1_en="Avis BBDBuy",
        cta=CTA_VISIT,
        cta_href=REGISTER,
        intro_fr="Avis bbdbuy — lisez QC, livraison et support ; pas de notes inventées ici.",
        intro_en="avis bbdbuy — evaluate QC, shipping, support; no fake ratings here.",
        sections_en=[("Sources", "Trustpilot, Reddit, Discord — croisez les avis récents.")],
        faq_en=[("Site officiel?", "Non — guide indépendant.")],
    ),
    _page(
        "bbdbuy-affidabile",
        regions=["FR"],
        title_en=f"BBDBuy Affidabile ? Sécurité et Risques ({YEAR})",
        desc_en="bbdbuy affidabile — agent d'achat, QC, paiement et risques transfrontaliers.",
        h1_fr="BBDBuy Affidabile ?",
        h1_en="BBDBuy Affidabile?",
        cta=CTA_START,
        cta_href=SPREADSHEET,
        intro_fr="BBDBuy fiable dépend du workflow agent — pas de promesse zéro risque.",
        intro_en="Fiable depends on agent workflow — not zero risk.",
        sections_en=[("Risques", "Douanes, délais, QC — à comprendre avant commande.")],
        faq_en=[("100% sûr?", "Non pour tout achat international.")],
    ),
    _page(
        "livraison-bbdbuy",
        regions=["FR"],
        title_en=f"Livraison BBDBuy: Délais et Process ({YEAR})",
        desc_en="livraison bbdbuy — entrepôt, QC, lignes d'expédition et délais réalistes.",
        h1_fr="Livraison BBDBuy",
        h1_en="Livraison BBDBuy",
        cta=CTA_ESTIMATE,
        cta_href=SPREADSHEET,
        intro_fr="Livraison bbdbuy — délais variables selon ligne et douanes.",
        intro_en="Shipping timelines vary by line and customs.",
        sections_en=[("Process", "Achat → QC → colis → suivi.")],
        faq_en=[("Délai fixe?", "Non garanti.")],
    ),
    _page(
        "guide-bbdbuy",
        regions=["FR"],
        title_en=f"Guide BBDBuy: Tableur et Commandes ({YEAR})",
        desc_en="guide bbdbuy — tableur BBDBuy sur W2CLinks et tutoriel agent.",
        h1_fr="Guide BBDBuy",
        h1_en="Guide BBDBuy",
        cta=CTA_SEARCH,
        cta_href=SPREADSHEET,
        intro_fr="Guide bbdbuy — tableur sur W2CLinks, commandes sur BBDBuy.",
        intro_en="Full guide — spreadsheet on W2CLinks, orders on BBDBuy.",
        sections_en=[("Tableur", "Mot-clé EN bbdbuy spreadsheet ; explications FR ici.")],
        faq_en=[("Tableur local?", "Non — hub W2CLinks.")],
    ),
    # ES extras
    _page(
        "como-comprar-en-bbdbuy",
        regions=["ES"],
        title_en=f"Cómo Comprar en BBDBuy ({YEAR})",
        desc_en="como comprar en bbdbuy — guía paso a paso para spreadsheet, QC y envío internacional.",
        h1_es="Cómo Comprar en BBDBuy",
        h1_en="Cómo Comprar en BBDBuy",
        cta=CTA_START,
        cta_href=SPREADSHEET,
        intro_es=(
            "como comprar en bbdbuy — busca finds en W2CLinks, pega el enlace en BBDBuy, "
            "revisa QC y envía el paquete a España."
        ),
        intro_en="Spanish how-to-buy guide for BBDBuy spreadsheet workflow via W2CLinks.",
        sections_en=[
            (
                "Pasos básicos",
                "1) Buscar en W2CLinks spreadsheet. 2) Copiar enlace del producto. "
                "3) Pegar en BBDBuy y pagar. 4) Revisar fotos QC. 5) Enviar paquete.",
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
        "bbdbuy-shipping-coupons",
        regions=["ES"],
        title_en=f"BBDBuy Shipping Coupons ({YEAR})",
        desc_en="bbdbuy shipping coupons — promociones de envío y finds en W2CLinks.",
        h1_es="BBDBuy Shipping Coupons",
        h1_en="BBDBuy Shipping Coupons",
        cta=CTA_COUPONS,
        cta_href=SPREADSHEET,
        intro_es="Cupones de envío BBDBuy — verifica condiciones en checkout; busca finds en W2CLinks.",
        intro_en="Shipping coupon intent — verify promotions on BBDBuy at checkout.",
        sections_en=[
            ("Cupones de envío", "Las promociones cambian; confirma en tu cuenta BBDBuy."),
            ("Browse first", "Encuentra productos en W2CLinks antes de aplicar cupones."),
        ],
        faq_en=[
            ("¿Descuento fijo?", "No — las promociones varían."),
            ("¿Combinar con spreadsheet?", "Sí — elige items en W2CLinks y aplica cupones al pagar."),
        ],
    ),

    _page(
        "bbdbuy-link",
        title_en="BBDBuy Link: Paste & Convert Marketplace URLs (2026)",
        desc_en="bbdbuy link guide — how to paste Taobao, 1688, and Weidian URLs into the agent workflow.",
        h1_en="BBDBuy Link Guide",
        cta=CTA_START,
        cta_href=SPREADSHEET,
        intro_en=(
            "bbdbuy link searches usually mean converting or pasting marketplace URLs into the "
            "shopping agent — browse finds on W2CLinks first, then paste links on OrientDig."
        ),
        sections_en=[
            (
                "Link paste workflow",
                f"Copy a product URL from W2CLinks spreadsheet or a seller page, then paste into "
                f'<a href="{{PLATFORM}}" target="_blank" rel="noopener">orientdig.com</a> to create an order.',
            ),
            (
                "Link converter intent",
                "Some searchers want Taobao/1688/Weidian link conversion — the agent platform handles "
                "normalized links after you paste the original URL.",
            ),
        ],
        faq_en=[
            ("Does BBDBuy host a link converter?", "Ordering links are handled on OrientDig after paste."),
            ("Where do I find product links?", f"Browse W2CLinks spreadsheet: {{SPREADSHEET}}"),
        ],
    ),
    _page(
        "bbdbuy-app",
        title_en="BBDBuy App & Mobile Ordering (2026)",
        desc_en="bbdbuy app guide — mobile access, account setup, and spreadsheet browsing on W2CLinks.",
        h1_en="BBDBuy App Guide",
        cta=CTA_OPEN,
        cta_href=REGISTER,
        intro_en=(
            "bbdbuy app searches reflect mobile ordering interest. Register on OrientDig and browse "
            "finds on W2CLinks from any device."
        ),
        sections_en=[
            (
                "Mobile workflow",
                "Use your phone to browse W2CLinks spreadsheet, copy links, and complete checkout on OrientDig.",
            ),
            (
                "App vs web",
                "Check OrientDig help center for current native app availability in your region.",
            ),
        ],
        faq_en=[
            ("Is there a standalone BBDBuy app?", "This guide site is web-only; orders go through OrientDig."),
            ("Can I browse finds on mobile?", f"Yes — open {{SPREADSHEET}} in your mobile browser."),
        ],
    ),
    _page(
        "bbdbuy-telegram",
        regions=["UK"],
        title_en="BBDBuy Telegram Channels (2026)",
        desc_en="bbdbuy telegram — community link sharing vs structured W2CLinks spreadsheet browsing.",
        h1_en="BBDBuy Telegram Guide",
        cta=CTA_BROWSE,
        cta_href=SPREADSHEET,
        intro_en=(
            "Telegram groups share BBDBuy finds informally; W2CLinks spreadsheet offers filterable browse lists."
        ),
        sections_en=[
            ("Telegram vs spreadsheet", "Use Telegram for tips, W2CLinks for searchable finds."),
            ("Not official support", "Community channels are not BBDBuy or OrientDig customer service."),
        ],
        faq_en=[
            ("Is Telegram official?", "No — verify links and compare QC themes independently."),
            ("Where to browse finds?", f"W2CLinks: {{SPREADSHEET}}"),
        ],
    ),
    _page(
        "bbdbuy-link-converter",
        regions=["US"],
        title_en="BBDBuy Link Converter for US Shoppers (2026)",
        desc_en="bbdbuy link converter — paste Taobao/1688/Weidian URLs and order via OrientDig after browsing W2CLinks.",
        h1_en="BBDBuy Link Converter Guide",
        cta=CTA_START,
        cta_href=REGISTER,
        intro_en=(
            "US shoppers searching bbdbuy link converter want a fast path from marketplace URLs to agent checkout. "
            "Browse on W2CLinks, paste links on OrientDig."
        ),
        sections_en=[
            (
                "Converter workflow",
                f"Paste raw seller URLs into OrientDig ({{PLATFORM}}) — no separate converter needed on this guide site.",
            ),
            (
                "US customs note",
                "Factor US import duties and use QC photos before consolidating heavy parcels.",
            ),
        ],
        faq_en=[
            ("Is conversion instant?", "OrientDig normalizes links after paste — verify listing details."),
            ("Where are finds?", f"W2CLinks spreadsheet: {{SPREADSHEET}}"),
        ],
    ),
    _page(
        "bbdbuy-canada",
        regions=["CA"],
        title_en="BBDBuy Canada: Spreadsheet & Ordering Guide (2026)",
        desc_en="bbdbuy canada — CAD-aware guide for Canadian buyers using W2CLinks finds and OrientDig shipping.",
        h1_en="BBDBuy Canada Guide",
        cta=CTA_SPREADSHEET,
        cta_href=SPREADSHEET,
        intro_en=(
            "Canadian buyers use BBDBuy spreadsheet guides to browse W2CLinks finds and order through OrientDig "
            "with realistic CBSA/customs expectations."
        ),
        sections_en=[
            ("CAD pricing context", "Display prices may show CAD on this site; verify checkout totals on OrientDig."),
            ("Canada shipping", "Delivery times vary by line and CBSA processing — budget extra time."),
        ],
        faq_en=[
            ("Is BBDBuy Canada-specific?", "This is an independent guide for Canadian shoppers."),
            ("French content?", "bbdbuy.ca uses English (en-CA) content."),
        ],
    ),
    _page(
        "bbdbuy-shipping-to-canada",
        regions=["CA"],
        title_en="BBDBuy Shipping to Canada (2026)",
        desc_en="bbdbuy shipping to canada — lines, CBSA customs, and parcel planning for Canadian buyers.",
        h1_en="BBDBuy Shipping to Canada",
        cta=CTA_ESTIMATE,
        cta_href=SPREADSHEET,
        intro_en="Shipping to Canada starts after QC approval and parcel submission on OrientDig.",
        sections_en=[
            ("CBSA and duties", "Import charges may apply depending on declared value and shipping line."),
            ("Line selection", "Compare economy vs express lines inside OrientDig checkout."),
        ],
        faq_en=[
            ("How long to Canada?", "Often several weeks — no fixed guarantee."),
            ("Are duties included?", "Usually not — budget for CBSA assessment."),
        ],
    ),
    _page(
        "recensioni-bbdbuy",
        regions=["IT"],
        title_en="Recensioni BBDBuy (2026): Guida Indipendente",
        desc_en="recensioni bbdbuy — valutare l'agente senza punteggi inventati; finds via W2CLinks.",
        h1_it="Recensioni BBDBuy",
        h1_en="Recensioni BBDBuy",
        cta=CTA_VISIT,
        cta_href=REGISTER,
        intro_it=(
            "Le ricerche recensioni bbdbuy chiedono prove QC, tempi di spedizione e supporto — "
            "nessuna valutazione fabbricata su questo sito."
        ),
        intro_en="recensioni bbdbuy — evaluate QC, shipping, and support without fake ratings.",
        sections_en=[
            ("Fonti", "Trustpilot, Reddit, Discord — confronta recensioni recenti."),
            ("Finds", "Confronta le scelte della community su W2CLinks spreadsheet."),
        ],
        faq_en=[
            ("Sito ufficiale?", "No — guida indipendente."),
            ("Dove ordinare?", "Dopo la ricerca finds, ordina su OrientDig."),
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
