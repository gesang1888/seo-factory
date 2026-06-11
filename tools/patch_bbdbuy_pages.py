#!/usr/bin/env python3
"""Post-rebrand patches: slug regions, renames, and new BBDBuy pages."""

from __future__ import annotations

import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parents[1]
PAGES_PATH = ROOT / "scripts" / "pages_bbdbuy.py"

NEW_PAGES_BLOCK = '''
    _page(
        "bbdbuy-link",
        title_en="BBDBuy Link: Paste & Convert Marketplace URLs ({year})",
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
        title_en="BBDBuy App & Mobile Ordering ({year})",
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
        title_en="BBDBuy Telegram Channels ({year})",
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
        title_en="BBDBuy Link Converter for US Shoppers ({year})",
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
        title_en="BBDBuy Canada: Spreadsheet & Ordering Guide ({year})",
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
        title_en="BBDBuy Shipping to Canada ({year})",
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
        title_en="Recensioni BBDBuy ({year}): Guida Indipendente",
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
'''


def main() -> None:
    text = PAGES_PATH.read_text(encoding="utf-8")

    text = text.replace(
        'regions=["FR", "ES"],\n        title_en=f"BBDBuy Discord',
        'regions=None,\n        title_en=f"BBDBuy Discord',
    )
    text = text.replace(
        'regions=["FR"],\n        title_en=f"BBDBuy Coupon',
        'regions=None,\n        title_en=f"BBDBuy Coupon',
    )
    text = text.replace('"bbdbuy-fiable"', '"bbdbuy-affidabile"')
    text = text.replace("BBDBuy Fiable", "BBDBuy Affidabile")
    text = text.replace("bbdbuy fiable", "bbdbuy affidabile")

    year_match = re.search(r'YEAR = "(\d{4})"', text)
    year = year_match.group(1) if year_match else "2026"
    block = NEW_PAGES_BLOCK.replace("{year}", year)

    insert_marker = "\n]\n\nPAGE_BY_SLUG"
    if insert_marker not in text:
        raise SystemExit("Could not find PAGES list terminator")

    for slug in [
        "bbdbuy-link",
        "bbdbuy-app",
        "bbdbuy-telegram",
        "bbdbuy-link-converter",
        "bbdbuy-canada",
        "bbdbuy-shipping-to-canada",
        "recensioni-bbdbuy",
    ]:
        if f'"{slug}"' in text:
            block = re.sub(
                rf'    _page\(\s*\n\s*"{re.escape(slug)}",.*?\),\n',
                "",
                block,
                flags=re.DOTALL,
            )

    if block.strip():
        text = text.replace(insert_marker, f"\n{block}\n]\n\nPAGE_BY_SLUG")

    PAGES_PATH.write_text(text, encoding="utf-8")
    print(f"patched {PAGES_PATH.name}")


if __name__ == "__main__":
    main()
