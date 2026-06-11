"""Country-specific SEO blocks derived from keyword CSV."""

from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CSV_PATH = ROOT / "data" / "keywords" / "kakobuy_keywords_cleaned_relevant.csv"

COUNTRY_MAP = {
    "NL": "NL",
    "FR": "FR",
    "ES": "ES",
    "CA": "CA",
    "FI": "FI",
}

REGION_INTROS: dict[str, dict[str, str]] = {
    "UK": {
        "en": (
            "UK shoppers searching kakobuy spreadsheet usually want HMRC-aware shipping tips, "
            "GBP-friendly budgeting, and Reddit-style finds lists. Browse live entries on W2CLinks, "
            "then order through Kakobuy with QC before consolidating parcels to the UK."
        ),
    },
    "US": {
        "en": (
            "US buyers compare kakobuy spreadsheet lists, coupon codes, and shipping calculators. "
            "This guide links to the W2CLinks browse hub and explains Kakobuy agent workflow, "
            "customs, and payment options without fake local product pages."
        ),
    },
    "NL": {
        "nl": (
            "Nederlandse zoekers gebruiken kakobuy spreadsheet en kakobuy spreadsheets (meervoud). "
            "Filter finds op W2CLinks, bestel via Kakobuy en plan BTW/douane realistisch in."
        ),
        "en": (
            "Dutch search volume includes kakobuy spreadsheets plural — use category filters on W2CLinks "
            "and verify Kakobuy shipping lines to the Netherlands."
        ),
    },
    "DE": {
        "de": (
            "Deutsche Nutzer suchen kakobuy spreadsheet, Erfahrungen und Trustpilot-Bewertungen. "
            "Diese Seite erklärt den Agent-Workflow, QC und Zoll — alle Produktlinks führen zu W2CLinks."
        ),
    },
    "IT": {
        "it": (
            "In Italia kakobuy spreadsheet ha buon volume con KD basso. "
            "Usa W2CLinks per browse e Kakobuy per acquisto, QC e spedizione internazionale."
        ),
    },
    "FR": {
        "fr": (
            "En France, kakobuy et kakobuy spreadsheet dominent les recherches. "
            "Ce guide en français explique le tableur sur W2CLinks et les commandes sur Kakobuy."
        ),
    },
    "ES": {
        "es": (
            "En España, kakobuy spreadsheet y como comprar en kakobuy son búsquedas frecuentes. "
            "Esta guía explica el spreadsheet en W2CLinks y el flujo de compra en Kakobuy."
        ),
    },
    "CA": {
        "en": (
            "Canadian buyers search kakobuy spreadsheet, coupon codes, and shipping to Canada. "
            "Browse W2CLinks finds, order on Kakobuy, and plan for CBSA duties and CAD checkout totals."
        ),
    },
    "FI": {
        "fi": (
            "Suomalaiset hakijat etsivät kakobuy spreadsheet -löytöjä ja toimitusohjeita. "
            "Selaa W2CLinks-hubiä, tilaa Kakobuylta ja huomioi tullit ja ALV."
        ),
        "en": (
            "Finnish buyers use kakobuy spreadsheet and shipping guides — W2CLinks browse, Kakobuy orders."
        ),
    },
}


def load_keywords() -> dict[str, list[dict]]:
    by_country: dict[str, list[dict]] = {k: [] for k in COUNTRY_MAP}
    if not CSV_PATH.is_file():
        return by_country
    with CSV_PATH.open(encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            c = row.get("country", "").strip()
            if c not in by_country:
                continue
            try:
                vol = int(float(row.get("Volume") or 0))
            except ValueError:
                vol = 0
            by_country[c].append(
                {
                    "keyword": row.get("Keyword") or row.get("kw_norm") or "",
                    "volume": vol,
                    "cluster": row.get("cluster") or "",
                }
            )
    for c in by_country:
        by_country[c].sort(key=lambda x: x["volume"], reverse=True)
    return by_country


def top_keywords(region: str, n: int = 8) -> list[str]:
    data = load_keywords()
    return [k["keyword"] for k in data.get(region, [])[:n] if k["keyword"]]


def country_seo_block(region: str, lang: str) -> dict:
    intros = REGION_INTROS.get(region, {})
    intro = intros.get(lang) or intros.get("en") or ""
    kws = top_keywords(region, 10)
    kw_line = ", ".join(kws[:6]) if kws else "kakobuy spreadsheet"
    return {
        "intro": intro,
        "keywords": kws,
        "keyword_line": kw_line,
    }
