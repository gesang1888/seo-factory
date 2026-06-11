"""Turn regional keyword data into readable guide articles (not tag lists)."""

from __future__ import annotations

from html import escape as esc

from scripts.country_seo import top_keywords
from scripts.hub_icons import flag_emoji, region_label
from scripts.link_helpers import main_spreadsheet_url, product_search_url

SPREADSHEET = main_spreadsheet_url()

# Internal page hints per keyword theme
PAGE_LINKS = {
    "spreadsheet": "orientdig-spreadsheet/",
    "finds": "orientdig-finds/",
    "shipping": "orientdig-shipping/",
    "coupons": "orientdig-coupons/",
    "legit": "is-orientdig-legit/",
    "safe": "is-orientdig-safe/",
    "howto": "how-to-use-orientdig/",
    "discord": "orientdig-discord/",
    "coupon_fr": "orientdig-coupon/",
    "spreadsheet_fr": "spreadsheet-orientdig/",
    "avis": "avis-orientdig/",
    "como_comprar": "como-comprar-en-orientdig/",
    "shipping_coupons_es": "orientdig-shipping-coupons/",
    "best_spreadsheet": "best-orientdig-spreadsheet/",
    "calculator": "orientdig-shipping-calculator/",
    "payment": "orientdig-payment-methods/",
    "erfahrungen": "orientdig-erfahrungen/",
    "trustpilot": "orientdig-trustpilot/",
    "codes": "orientdig-codes/",
    "qc": "orientdig-qc/",
}


def _link(home_prefix: str, slug: str, text: str) -> str:
    return f'<a href="{esc(home_prefix + slug)}">{esc(text)}</a>'


def _ext(text: str, url: str) -> str:
    return f'<a href="{esc(url)}" target="_blank" rel="noopener">{esc(text)}</a>'


def _section(heading: str, paragraphs: list[str]) -> str:
    body = "".join(f"<p>{p}</p>" for p in paragraphs)
    return f"<h3>{esc(heading)}</h3>{body}"


def article_us(home_prefix: str) -> str:
    return (
        _section(
            "What US shoppers mean when they search OrientDig",
            [
                "The brand query orientdig usually signals intent to understand the agent itself — registration, "
                "balance top-ups, warehouse flow and whether the platform fits a first purchase. "
                "It is different from orientdig spreadsheet, which almost always means a browsable finds list.",
                "US search volume also clusters around trust queries such as is orientdig legit and is orientdig safe. "
                f"Those questions are answered in our {_link(home_prefix, PAGE_LINKS['legit'], 'legit guide')} and "
                f"{_link(home_prefix, PAGE_LINKS['safe'], 'safety FAQ')}, without fake review scores.",
            ],
        )
        + _section(
            "Spreadsheet, best lists and product discovery",
            [
                f"orientdig spreadsheet and best orientdig spreadsheet map to the same practical action: open the live "
                f"W2CLinks hub ({_ext('w2clinks.com/spreadsheet', SPREADSHEET)}), sort by newest, and filter by category "
                "or brand. This site does not host a local clone — every product button routes outward.",
                f"For deeper browsing tactics, see {_link(home_prefix, PAGE_LINKS['best_spreadsheet'], 'best spreadsheet categories')} "
                f"and {_link(home_prefix, PAGE_LINKS['finds'], 'product finds guide')}. "
                f"Keyword search — for example {_ext('jordan finds', product_search_url('jordan'))} — helps when you "
                "already know the silhouette you want.",
            ],
        )
        + _section(
            "Shipping calculators, coupons and payment planning",
            [
                "orientdig shipping calculator searches reflect parcel planning anxiety: weight, line choice, and whether "
                f"delivery fits a deadline. Read {_link(home_prefix, PAGE_LINKS['shipping'], 'US shipping notes')} for "
                f"estimated line ranges, then confirm live quotes inside OrientDig before paying.",
                "Coupon-related queries such as orientdig coupon and orientdig coupon codes change frequently. "
                f"Use the {_link(home_prefix, PAGE_LINKS['coupons'], 'coupon guide')} for workflow — browse finds first, "
                f"apply eligible codes at checkout — and {_link(home_prefix, PAGE_LINKS['payment'], 'payment methods')} "
                "to compare how you fund the order.",
            ],
        )
        + _section(
            "Recommended US buyer workflow",
            [
                "1) Shortlist on W2CLinks. 2) Paste links into OrientDig. 3) Review QC photos. "
                "4) Compare shipping lines with realistic customs buffer. 5) Track import milestones. "
                f"Full steps live in {_link(home_prefix, PAGE_LINKS['howto'], 'how to use OrientDig')}.",
            ],
        )
    )


def article_fr(home_prefix: str) -> str:
    return (
        _section(
            "Ce que les acheteurs français cherchent avec « orientdig »",
            [
                "En France, la requête orientdig mélange curiosité sur la plateforme agent et envie de trouver des finds "
                "rapidement. Ce n'est pas la peine de confondre la marque avec un tableur local : le browse structuré "
                f"passe par W2CLinks, tandis que la commande se finalise sur orientdig.com.",
                "Les recherches orientdig spreadsheet et spreadsheet orientdig (ordre inversé) pointent vers le même "
                f"besoin : filtrer des listes communautaires. Utilisez {_link(home_prefix, PAGE_LINKS['spreadsheet'], 'OrientDig Spreadsheet')} "
                f"ou la variante {_link(home_prefix, PAGE_LINKS['spreadsheet_fr'], 'spreadsheet orientdig')} selon l'intention exacte.",
            ],
        )
        + _section(
            "Discord, coupons et confiance",
            [
                f"orientdig discord reflète l'habitude d'échanger des liens en communauté. Ce site n'est pas un canal Discord — "
                f"il structure l'intention vers le tableur W2CLinks. Voir {_link(home_prefix, PAGE_LINKS['discord'], 'Discord & community guide')}.",
                f"Pour orientdig coupon, vérifiez toujours les conditions dans votre compte OrientDig. "
                f"Le guide {_link(home_prefix, PAGE_LINKS['coupon_fr'], 'OrientDig coupon')} explique comment combiner "
                f"finds et codes sans promettre une remise fixe.",
                f"Les recherches avis orientdig demandent une lecture prudente : comparez QC, délais et support. "
                f"Notre page {_link(home_prefix, PAGE_LINKS['avis'], 'avis orientdig')} reste un guide indépendant, "
                "sans notes inventées.",
            ],
        )
        + _section(
            "Liens produits, livraison et QC",
            [
                "orientdig link correspond à des questions sur conversion de liens Taobao/1688/Weidian — même logique que "
                f"partout ailleurs : copier l'URL source, coller dans OrientDig, attendre les photos QC. "
                f"Lire {_link(home_prefix, PAGE_LINKS['qc'], 'guide QC')} avant d'expédier.",
                f"Pour la livraison vers la France, consultez {_link(home_prefix, PAGE_LINKS['shipping'], 'livraison OrientDig')} "
                "avec des fourchettes EUR indicatives, puis validez la ligne réelle au moment du colis.",
            ],
        )
    )


def article_es(home_prefix: str) -> str:
    return (
        _section(
            "Qué buscan en España con orientdig y orientdig spreadsheet",
            [
                "orientdig suele ser la búsqueda de entrada: entender el agente, recargar saldo y preparar el primer pedido. "
                "orientdig spreadsheet es más específica — el usuario quiere un listado navegable de finds, no un Excel estático.",
                f"El hub correcto es {_ext('W2CLinks spreadsheet', SPREADSHEET)}. Desde aquí filtras categoría/marca "
                f"y abres {_link(home_prefix, PAGE_LINKS['finds'], 'orientdig finds')} para comparar entradas recientes.",
            ],
        )
        + _section(
            "Cómo comprar, Discord y cupones de envío",
            [
                f"como comprar en orientdig es una intención tutorial clara. Sigue {_link(home_prefix, PAGE_LINKS['como_comprar'], 'cómo comprar en OrientDig')} "
                "paso a paso: enlace → pago → QC → paquete internacional.",
                f"orientdig discord indica búsqueda comunitaria; el finds estructurado sigue en W2CLinks — "
                f"ver {_link(home_prefix, PAGE_LINKS['discord'], 'guía Discord')}.",
                f"orientdig shipping coupons mezcla promos de envío con dudas de peso. Revisa "
                f"{_link(home_prefix, PAGE_LINKS['shipping_coupons_es'], 'shipping coupons')} y "
                f"{_link(home_prefix, PAGE_LINKS['coupons'], 'cupones OrientDig')} antes de pagar.",
            ],
        )
        + _section(
            "Envío, aduanas y QC para compradores españoles",
            [
                "orientdig shipping y preguntas de plazo deben leerse junto con peso real y línea elegida. "
                f"La guía {_link(home_prefix, PAGE_LINKS['shipping'], 'envío OrientDig')} incluye rangos EUR orientativos.",
                f"Antes de enviar internacionalmente, usa {_link(home_prefix, PAGE_LINKS['qc'], 'QC photos guide')} "
                "para validar tallas y defectos visibles.",
            ],
        )
    )


def article_at(home_prefix: str) -> str:
    return (
        _section(
            "Was österreichische OrientDig-Suchen bedeuten",
            [
                "orientdig spreadsheet ist der häufigste produktbezogene Begriff — gemeint ist der W2CLinks-Hub mit "
                f"Filter und Sortierung ({_ext('Spreadsheet öffnen', SPREADSHEET)}), nicht eine lokale Datei.",
                "Erfahrungen, Trustpilot und QC-Fragen sind in DACH-Suchen stark vertreten. "
                f"Lies {_link(home_prefix, PAGE_LINKS['erfahrungen'], 'OrientDig Erfahrungen')} und "
                f"{_link(home_prefix, PAGE_LINKS['trustpilot'], 'Trustpilot Intent Guide')} mit realistischen Erwartungen.",
            ],
        )
        + _section(
            "Gutscheine, QC und Versand nach Österreich",
            [
                f"orientdig codes und Coupon-Intention gehören zur Checkout-Phase — siehe "
                f"{_link(home_prefix, PAGE_LINKS['codes'], 'OrientDig codes')}. Finds zuerst auf W2CLinks wählen.",
                f"qc orientdig betont Fotos vor dem Versand. Der "
                f"{_link(home_prefix, PAGE_LINKS['qc'], 'QC-Leitfaden')} erklärt, worauf du bei Schuhen und Kleidung achtest.",
                f"Für Versand nach Österreich: {_link(home_prefix, PAGE_LINKS['shipping'], 'Versandguide')} mit EUR-Schätzwerten, "
                "dann Live-Preis im OrientDig-Konto bestätigen.",
            ],
        )
    )


def article_generic_en(region: str, home_prefix: str, keywords: list[str]) -> str:
    kw_note = ", ".join(keywords[:6]) if keywords else "orientdig spreadsheet"
    label = region_label(region)
    return (
        _section(
            f"Search intent overview for {label}",
            [
                f"Shoppers in {label} often combine brand queries (orientdig) with product discovery "
                f"(orientdig spreadsheet) and trust questions (is orientdig legit / is orientdig safe). "
                f"This guide translates those searches into actions on W2CLinks and OrientDig.",
                f"Top regional queries we see in research data include: {esc(kw_note)}. "
                "Each maps to a guide section on this site rather than a standalone product page.",
            ],
        )
        + _section(
            "From keyword to action",
            [
                f"Open {_ext('W2CLinks spreadsheet', SPREADSHEET)}, pick a category, copy the source link, "
                f"and paste into OrientDig. Review QC, then read {_link(home_prefix, PAGE_LINKS['shipping'], 'shipping guide')} "
                f"and {_link(home_prefix, PAGE_LINKS['coupons'], 'coupon notes')} for your parcel.",
            ],
        )
    )


REGION_ARTICLE_BUILDERS = {
    "US": lambda hp, _: article_us(hp),
    "FR": lambda hp, _: article_fr(hp),
    "ES": lambda hp, _: article_es(hp),
    "AT": lambda hp, _: article_at(hp),
}


def keyword_guide_article(region: str, lang: str, home_prefix: str = "") -> str:
    """Full article HTML for the country guide card."""
    builder = REGION_ARTICLE_BUILDERS.get(region)
    if builder:
        return builder(home_prefix, lang)
    kws = top_keywords(region, 10)
    return article_generic_en(region, home_prefix, kws)


def country_guide_html(region: str, lang: str, home_prefix: str = "") -> str:
    """Render country guide card with flag + intro + keyword article."""
    from scripts.country_seo import country_seo_block

    block = country_seo_block(region, lang)
    intro = block.get("intro", "")
    if not intro and not top_keywords(region, 3):
        return ""

    label = region_label(region) if region in REGION_ARTICLE_BUILDERS or region in (
        "UK", "NL", "DE", "IT"
    ) else region
    emoji = flag_emoji(region)
    article = keyword_guide_article(region, lang, home_prefix)

    from scripts.i18n_ui import t as ui_t

    ui = lang if lang in ("nl", "de", "it", "fr", "es") else "en"
    title = ui_t(ui, "country_guide")

    return f"""<div class="card od-country-guide">
  <h2><span class="od-flag-emoji" aria-hidden="true">{emoji}</span> {esc(title)}: {esc(label)}</h2>
  <p class="lead">{esc(intro)}</p>
  <div class="od-keyword-article">{article}</div>
</div>"""
