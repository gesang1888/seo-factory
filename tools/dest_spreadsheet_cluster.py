#!/usr/bin/env python3
"""Retitle dest-country desks to the kakobuy.co.uk spreadsheet cluster.

Pattern (localized, not an English doorway clone):
  Title / H1: {Brand} Spreadsheet for {Country} Buyers
  keywords + WebSite JSON-LD: {Brand} spreadsheet, {brand} spreadsheet {geo}, {brand} sheet
  Seven inners: spreadsheet / finds / QC / shipping-to-country / is-it-legal / guide / FAQ

Does not revive 301 twins. Does not smash CSSBuy PHP gold (cssbuy-lite public/).
Does not PUT hipobuyspreadsheet.net. Does not coach a declared value.
Maps ranked keep slugs instead of duplicating them.
"""
from __future__ import annotations

import json
import os
import re
import sys
import time
from html import escape, unescape
from pathlib import Path

_TOOLS = Path(__file__).resolve().parent
if str(_TOOLS) not in sys.path:
    sys.path.insert(0, str(_TOOLS))
from desk_template import (
    CUSTOMS,
    DEST_LOCAL,
    FORBIDDEN_HTML,
    KW_GEO,
    cluster_country_name,
    cluster_desc,
    cluster_h1,
    cluster_keywords,
    cluster_title,
    dest_local_pack,
    inject_jsonld,
    skip_label,
    skip_link,
    website_ld,
    webpage_ld,
)

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "sites"
MARKER = 'data-spreadsheet-cluster="20261030"'
DATE = "30 Oct 2026"

TWINS = {
    "fansbuy.eu",
    "sugargoospreadsheets.de",
    "ootdbuyspreadsheet.de",
    "litbuyspreadsheet.me.uk",
    "litbuyspreadsheets.es",
    "acbuyspreadsheets.ca",
    "allchinabuyspreadsheet.nl",
    "cssbuy.at",  # nginx 301 → cssbuyspreadsheet.eu (Phase B sunset)
}
PHP_CSSBUY = {"cssbuy.at", "cssbuy.es", "cssbuy.fr", "cssbuy.it", "cssbuy.nl"}
UNIQUE_PHP_HUBS = {"hipobuyspreadsheet.net"}

BRAND_PREFIXES = (
    ("allchinabuy", "AllChinaBuy"),
    ("hipobuy", "HipoBuy"),
    ("sugargoo", "SugarGoo"),
    ("lovegobuy", "LoveGoBuy"),
    ("orientdig", "OrientDig"),
    ("superbuy", "Superbuy"),
    ("kakobuy", "Kakobuy"),
    ("cssbuy", "CSSBuy"),
    ("bbdbuy", "BBDBuy"),
    ("fansbuy", "FansBuy"),
    ("mulebuy", "MuleBuy"),
    ("mycnbox", "MyCNBox"),
    ("ootdbuy", "OOTDBuy"),
    ("oopbuy", "OOPBuy"),
    ("usfans", "USFans"),
    ("joyagoo", "JoyaGoo"),
    ("litbuy", "LitBuy"),
    ("litspreadsheet", "LitBuy"),
    ("acbuy", "ACBuy"),
    ("kako", "Kakobuy"),
)

TLD_DEST = (
    (".co.uk", "GB"),
    (".me.uk", "GB"),
    (".uk", "GB"),
    (".at", "AT"),
    (".es", "ES"),
    (".fr", "FR"),
    (".it", "IT"),
    (".nl", "NL"),
    (".de", "DE"),
    (".ca", "CA"),
    (".us", "US"),
    (".au", "AU"),
    (".fi", "FI"),
    (".pl", "PL"),
)

LOC_FOR = {
    "AT": "de",
    "DE": "de",
    "ES": "es",
    "FR": "fr",
    "IT": "it",
    "NL": "nl",
    "FI": "fi",
    "PL": "en",
    "GB": "en",
    "US": "en",
    "CA": "en",
    "AU": "en",
}
LANG_FOR = {
    "AT": "de-AT",
    "DE": "de-DE",
    "ES": "es-ES",
    "FR": "fr-FR",
    "IT": "it-IT",
    "NL": "nl-NL",
    "FI": "fi-FI",
    "PL": "pl-PL",
    "GB": "en-GB",
    "US": "en-US",
    "CA": "en-CA",
    "AU": "en-AU",
}
LABEL_FOR = {
    "AT": "Österreich",
    "AU": "Australia",
    "CA": "Canada",
    "DE": "Deutschland",
    "ES": "España",
    "FI": "Suomi",
    "FR": "France",
    "GB": "the United Kingdom",
    "IT": "Italia",
    "NL": "Nederland",
    "PL": "Poland",
    "US": "the United States",
}
CCY_FOR = {
    "AT": "EUR",
    "AU": "AUD",
    "CA": "CAD",
    "DE": "EUR",
    "ES": "EUR",
    "FI": "EUR",
    "FR": "EUR",
    "GB": "GBP",
    "IT": "EUR",
    "NL": "EUR",
    "PL": "PLN",
    "US": "USD",
}

PAGE_LAB = {
    "en": {
        "spreadsheet": "Spreadsheet",
        "finds": "Finds",
        "qc": "QC",
        "shipping": "Shipping",
        "legal": "Is it legal?",
        "guide": "Guide",
        "faq": "FAQ",
    },
    "de": {
        "spreadsheet": "Spreadsheet",
        "finds": "Finds",
        "qc": "QC",
        "shipping": "Versand",
        "legal": "Legal?",
        "guide": "Ratgeber",
        "faq": "FAQ",
    },
    "es": {
        "spreadsheet": "Spreadsheet",
        "finds": "Finds",
        "qc": "QC",
        "shipping": "Envío",
        "legal": "¿Es legal?",
        "guide": "Guía",
        "faq": "FAQ",
    },
    "fr": {
        "spreadsheet": "Spreadsheet",
        "finds": "Finds",
        "qc": "QC",
        "shipping": "Livraison",
        "legal": "Est-ce légal ?",
        "guide": "Guide",
        "faq": "FAQ",
    },
    "it": {
        "spreadsheet": "Spreadsheet",
        "finds": "Finds",
        "qc": "QC",
        "shipping": "Spedizione",
        "legal": "È legale?",
        "guide": "Guida",
        "faq": "FAQ",
    },
    "nl": {
        "spreadsheet": "Spreadsheet",
        "finds": "Finds",
        "qc": "QC",
        "shipping": "Verzending",
        "legal": "Is het legaal?",
        "guide": "Gids",
        "faq": "FAQ",
    },
    "fi": {
        "spreadsheet": "Spreadsheet",
        "finds": "Finds",
        "qc": "QC",
        "shipping": "Toimitus",
        "legal": "Onko se laillista?",
        "guide": "Ohje",
        "faq": "FAQ",
    },
}

KINDS = ("spreadsheet", "finds", "qc", "shipping", "legal", "guide", "faq")

SHIP_TOK = ("shipping", "envio", "envío", "livraison", "spedizione", "verzending", "toimitus", "versand", "freight", "sendung")
LEGAL_TOK = ("legit", "legal", "safe", "confiable", "kokemuksia", "opiniones", "review", "serios", "avis", "ervaringen", "affidabile")
GUIDE_TOK = ("how-to", "handleiding", "anleitung", "ohje", "ratgeber", "first-order", "come-usar", "come-funziona", "como-comprar", "cómo-usar", "como-usar")


def dest_hosts() -> list[str]:
    p = Path("/tmp/dest-hosts.txt")
    if p.is_file():
        return [ln.strip() for ln in p.read_text().splitlines() if ln.strip()]
    return sorted(
        d.name
        for d in OUT.iterdir()
        if d.is_dir() and (d / "overlay").is_dir()
    )


def brand_from_host(host: str) -> str:
    h = host.lower().split(".")[0]
    for prefix, brand in BRAND_PREFIXES:
        if h.startswith(prefix):
            return brand
    return host.split(".")[0].title()


def dest_from_host(host: str) -> str | None:
    h = host.lower()
    for suf, dest in TLD_DEST:
        if h.endswith(suf):
            return dest
    return None


def brand_slug(agent: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", agent.lower())


def _import_keep_maps() -> dict[str, dict]:
    extra: dict[str, dict] = {}
    try:
        from hub_skin_desks import HOSTS as H  # type: ignore

        for host, d in H.items():
            extra[host] = {
                "agent": d["agent"],
                "dest": d.get("dest"),
                "loc": d.get("loc") or "en",
                "lang": d.get("lang") or "en",
                "dest_label": d.get("dest_label") or "",
                "ccy": d.get("ccy") or "EUR",
                "keep": list(d.get("keep") or []),
            }
    except Exception:
        pass
    desk_mods = (
        "kakobuy_desks",
        "litbuy_desks",
        "sugargoo_desks",
        "cssbuy_desks",
        "mycnbox_desks",
        "fansbuy_desks",
        "hipobuy_cms_home",
        "joyagoo_desks",
        "acbuy_desks",
        "allchinabuy_desks",
        "bbdbuy_desks",
        "lovegobuy_desks",
        "mulebuy_desks",
        "ootdbuy_desks",
        "orientdig_desks",
        "superbuy_desks",
        "usfans_desks",
        "oopbuy_desks",
    )
    for modname in desk_mods:
        try:
            mod = __import__(modname)
        except Exception:
            continue
        for attr in ("HOSTS", "PHP_HOSTS", "STATIC_HOSTS", "DESTS"):
            block = getattr(mod, attr, None)
            if not isinstance(block, dict):
                continue
            for key, spec in block.items():
                if not isinstance(spec, dict) or not spec.get("host"):
                    continue
                host = spec["host"]
                row = extra.setdefault(host, {})
                row.setdefault("agent", spec.get("agent") or brand_from_host(host))
                if spec.get("dest") is not None or "dest" in spec:
                    row["dest"] = spec.get("dest")
                row.setdefault("loc", spec.get("loc") or LOC_FOR.get(spec.get("dest") or "", "en"))
                row.setdefault("lang", spec.get("lang") or "en")
                row.setdefault("dest_label", spec.get("dest_label") or "")
                row.setdefault("ccy", spec.get("ccy") or "EUR")
                keep = list(spec.get("keep") or [])
                if keep:
                    row["keep"] = list(dict.fromkeys((row.get("keep") or []) + keep))
    return extra


def spec_for(host: str, keep_maps: dict[str, dict]) -> dict:
    base = keep_maps.get(host) or {}
    dest = base.get("dest") if "dest" in base else dest_from_host(host)
    loc = base.get("loc") or LOC_FOR.get(dest or "", "en")
    agent = base.get("agent") or brand_from_host(host)
    dest_label = base.get("dest_label") or LABEL_FOR.get(dest or "", host)
    cname, curl = CUSTOMS.get(dest or "", ("the destination customs site", ""))
    pack = dest_local_pack(dest)
    return {
        "host": host,
        "agent": agent,
        "dest": dest,
        "loc": loc,
        "lang": base.get("lang") or LANG_FOR.get(dest or "", "en"),
        "dest_label": dest_label,
        "ccy": base.get("ccy") or CCY_FOR.get(dest or "", "EUR"),
        "keep": list(base.get("keep") or []),
        "customs": cname,
        "customs_url": curl,
        "fingerprint": pack.get("fingerprint") or "",
        "duty": pack.get("duty") or "",
        "php": host in PHP_CSSBUY,
        "title": cluster_title(agent, dest, loc, dest_label),
        "h1": cluster_h1(agent, dest, loc, dest_label),
        "keywords": cluster_keywords(agent, dest, loc, dest_label),
        "desc": cluster_desc(agent, dest, loc, dest_label, host, cname),
        "geo": KW_GEO.get(dest or "", "")
        or re.sub(r"[^a-z0-9]+", "", cluster_country_name(dest, loc, dest_label).lower()),
        "slug": brand_slug(agent),
    }


def overlay_dir(host: str) -> Path:
    return OUT / host / "overlay"


def home_file(host: str) -> Path | None:
    overlay = overlay_dir(host)
    idx = overlay / "index.html"
    live = overlay / "live-base" / "index.html"
    live2 = overlay / "live-base-index.html"
    candidates = []
    if idx.is_file():
        candidates.append(idx)
    if live.is_file():
        candidates.append(live)
    if live2.is_file():
        candidates.append(live2)
    if not candidates:
        return None
    candidates.sort(key=lambda p: p.stat().st_size, reverse=True)
    # Prefer generated overlay/index.html when it is a real desk, not a stub.
    if idx.is_file() and idx.stat().st_size >= 8000:
        return idx
    return candidates[0]


def overlay_paths(host: str) -> list[tuple[str, Path]]:
    overlay = overlay_dir(host)
    if not overlay.is_dir():
        return []
    found: list[tuple[str, Path]] = []
    for p in overlay.rglob("*"):
        if not p.is_file():
            continue
        name = p.name
        if name in {"index.html.platform-patched", "index.html.step4-patched"}:
            continue
        if name.endswith((".nl-deepen", ".es-deepen", ".fi-deepen", ".it-deepen")):
            continue
        rel = p.relative_to(overlay).as_posix()
        if rel in {"index.html", "live-base/index.html", "live-base-index.html", "404.html"}:
            continue
        if name == "index.html":
            slug = "/" + str(p.parent.relative_to(overlay)).replace("\\", "/") + "/"
            found.append((slug, p))
        elif name == "live-base.index.html":
            slug = "/" + str(p.parent.relative_to(overlay)).replace("\\", "/") + "/"
            found.append((slug, p))
        elif name.endswith(".html") and "/" not in rel:
            slug = "/" + name
            found.append((slug, p))
    # Prefer real index.html over live-base.index.html for the same slug.
    by_slug: dict[str, Path] = {}
    for slug, path in found:
        prev = by_slug.get(slug)
        if prev is None or (path.name == "index.html" and prev.name != "index.html"):
            by_slug[slug] = path
    return sorted(by_slug.items())


def classify_slug(slug: str) -> str | None:
    s = slug.lower().rstrip("/")
    tail = s.rsplit("/", 1)[-1]
    if any(tok in s for tok in ("coupon", "cupon", "cupón", "gutschein")):
        return None
    if "finds" in tail:
        return "finds"
    if re.search(r"(?:^|/)qc(?:/|$)|-qc(?:/|$)", s) or tail == "qc":
        return "qc"
    if "spreadsheet" in s or tail == "spreadsheet":
        return "spreadsheet"
    if any(tok in s for tok in SHIP_TOK):
        return "shipping"
    if any(tok in s for tok in LEGAL_TOK):
        return "legal"
    if "faq" in tail or tail == "faq":
        return "faq"
    if any(tok in s for tok in GUIDE_TOK):
        return "guide"
    if tail in {"guide", "guides", "ohje", "hulp", "guida", "guia", "guía"} or s.endswith("/guide"):
        return "guide"
    return None


def default_slug(kind: str, spec: dict) -> str:
    b, geo = spec["slug"], spec["geo"] or "dest"
    return {
        "spreadsheet": f"/{b}-spreadsheet/",
        "finds": f"/{b}-finds/",
        "qc": f"/{b}-qc/",
        "shipping": f"/{b}-shipping-to-{geo}/",
        "legal": f"/is-{b}-legal-{geo}/",
        "guide": f"/{b}-guide/",
        "faq": f"/{b}-faq/",
    }[kind]


def _norm_slug(slug: str) -> str:
    slug = slug if slug.startswith("/") else "/" + slug
    if slug.endswith(".html"):
        return slug
    return slug if slug.endswith("/") else slug + "/"


def _is_cluster_clone(path: Path | None) -> bool:
    if not path or not path.is_file():
        return False
    try:
        head = path.read_text(encoding="utf-8", errors="replace")[:4000]
    except OSError:
        return False
    return 'class="cluster-page"' in head


def map_pages(spec: dict) -> dict[str, tuple[str, Path | None]]:
    host = spec["host"]
    mapped: dict[str, tuple[str, Path | None]] = {}
    overlay_map = {_norm_slug(s): p for s, p in overlay_paths(host)}
    keep_slugs = [_norm_slug(k[0] if isinstance(k, (list, tuple)) else k) for k in spec.get("keep") or []]
    for slug in keep_slugs:
        if re.search(r"[^\x00-\x7F]", slug):
            continue
        kind = classify_slug(slug)
        if not kind or kind in mapped:
            continue
        path = overlay_map.get(slug)
        if _is_cluster_clone(path):
            path = None
        mapped[kind] = (slug, path)
    for slug, path in overlay_map.items():
        if re.search(r"[^\x00-\x7F]", slug):
            continue
        kind = classify_slug(slug)
        if not kind or kind in mapped:
            continue
        if _is_cluster_clone(path):
            mapped[kind] = (slug, path)
            continue
        mapped[kind] = (slug, path)
    for kind in KINDS:
        if kind in mapped:
            continue
        slug = default_slug(kind, spec)
        existing = overlay_map.get(_norm_slug(slug))
        mapped[kind] = (slug, existing)
    return mapped


def labs(spec: dict) -> dict[str, str]:
    return PAGE_LAB.get(spec["loc"], PAGE_LAB["en"])


def inner_title(kind: str, spec: dict) -> str:
    agent, name = spec["agent"], cluster_country_name(spec["dest"], spec["loc"], spec["dest_label"])
    loc = spec["loc"]
    table = {
        "spreadsheet": {
            "en": f"{agent} spreadsheet — {name} buyers",
            "de": f"{agent} Spreadsheet — {name}",
            "es": f"{agent} spreadsheet — compradores en {name}",
            "fr": f"{agent} spreadsheet — acheteurs en {name}",
            "it": f"{agent} spreadsheet — acquirenti in {name}",
            "nl": f"{agent} spreadsheet — kopers in {name}",
            "fi": f"{agent} spreadsheet — ostajat Suomessa",
        },
        "finds": {
            "en": f"{agent} finds for {name} buyers",
            "de": f"{agent} Finds für Käufer in {name}",
            "es": f"{agent} finds para {name}",
            "fr": f"{agent} finds pour {name}",
            "it": f"{agent} finds per {name}",
            "nl": f"{agent} finds voor {name}",
            "fi": f"{agent} finds Suomessa",
        },
        "qc": {
            "en": f"{agent} QC photos before shipping to {name}",
            "de": f"{agent} QC-Fotos vor dem Versand nach {name}",
            "es": f"{agent} QC antes de enviar a {name}",
            "fr": f"{agent} QC avant envoi vers {name}",
            "it": f"{agent} QC prima della spedizione in {name}",
            "nl": f"{agent} QC vóór verzending naar {name}",
            "fi": f"{agent} QC ennen toimitusta Suomeen",
        },
        "shipping": {
            "en": f"{agent} shipping to {name}",
            "de": f"{agent} Versand nach {name}",
            "es": f"{agent} envío a {name}",
            "fr": f"{agent} livraison vers {name}",
            "it": f"{agent} spedizione in {name}",
            "nl": f"{agent} verzending naar {name}",
            "fi": f"{agent} toimitus Suomeen",
        },
        "legal": {
            "en": f"Is {agent} legal in {name}?",
            "de": f"Ist {agent} in {name} legal?",
            "es": f"¿Es legal {agent} en {name}?",
            "fr": f"{agent} est-il légal en {name} ?",
            "it": f"{agent} è legale in {name}?",
            "nl": f"Is {agent} legaal in {name}?",
            "fi": f"Onko {agent} laillinen Suomessa?",
        },
        "guide": {
            "en": f"{agent} guide for {name} buyers",
            "de": f"{agent} Ratgeber für {name}",
            "es": f"Guía {agent} para {name}",
            "fr": f"Guide {agent} pour {name}",
            "it": f"Guida {agent} per {name}",
            "nl": f"{agent}-gids voor {name}",
            "fi": f"{agent}-ohje Suomelle",
        },
        "faq": {
            "en": f"{agent} spreadsheet FAQ — {name}",
            "de": f"{agent} Spreadsheet FAQ — {name}",
            "es": f"FAQ spreadsheet {agent} — {name}",
            "fr": f"FAQ spreadsheet {agent} — {name}",
            "it": f"FAQ spreadsheet {agent} — {name}",
            "nl": f"{agent} spreadsheet FAQ — {name}",
            "fi": f"{agent} spreadsheet FAQ — Suomi",
        },
    }
    row = table[kind]
    return row.get(loc, row["en"])


def inner_body(kind: str, spec: dict, pages: dict[str, tuple[str, Path | None]]) -> str:
    loc = spec["loc"]
    agent, host, dest = spec["agent"], spec["host"], spec["dest_label"]
    name = cluster_country_name(spec["dest"], spec["loc"], dest)
    fp, duty, customs = spec["fingerprint"], spec["duty"], spec["customs"]
    kws = ", ".join(spec["keywords"])
    title = inner_title(kind, spec)
    nav = "".join(
        f'<li><a href="{escape(pages[k][0])}">{escape(labs(spec)[k])}</a></li>'
        for k in KINDS
        if k in pages
    )
    blocks = {
        "spreadsheet": {
            "en": (
                f"This page is the {escape(agent)} spreadsheet for {escape(name)} buyers on {escape(host)} — an index, not Excel and not checkout. Keywords: {escape(kws)}.",
                f"Warehouse QC photos land in the official app before you book a line to {escape(name)}. Finds you keep on this sheet are SKUs you already accepted, not a shop.",
                f"Local check: {escape(fp)}. {escape(duty)} Educational source: {escape(customs)}. This desk does not invent a declared value.",
            ),
            "de": (
                f"Diese Seite ist das {escape(agent)} Spreadsheet für Käufer in {escape(name)} auf {escape(host)} — ein Index, keine Excel-Datei, keine Kasse. Keywords: {escape(kws)}.",
                f"QC-Fotos kommen in der offiziellen App, bevor du eine Linie nach {escape(name)} buchst. Finds auf diesem Sheet sind akzeptierte SKUs, kein Shop.",
                f"Lokal: {escape(fp)}. {escape(duty)} Quelle: {escape(customs)}. Keine Unterdeklaration.",
            ),
            "es": (
                f"Esta página es el spreadsheet {escape(agent)} para compradores en {escape(name)} en {escape(host)}: un índice, no Excel ni caja. Keywords: {escape(kws)}.",
                f"Las fotos QC llegan a la app oficial antes de reservar la línea a {escape(name)}. Los finds de esta hoja son SKU aceptados, no una tienda.",
                f"Check local: {escape(fp)}. {escape(duty)} Fuente: {escape(customs)}. Sin infradeclaración.",
            ),
            "fr": (
                f"Cette page est le spreadsheet {escape(agent)} pour les acheteurs en {escape(name)} sur {escape(host)} — un index, pas Excel, pas une caisse. Keywords : {escape(kws)}.",
                f"Les photos QC arrivent dans l’app officielle avant de réserver une ligne vers {escape(name)}. Les finds de cette feuille sont des SKU acceptés, pas une boutique.",
                f"Check local : {escape(fp)}. {escape(duty)} Source : {escape(customs)}. Pas de sous-déclaration.",
            ),
            "it": (
                f"Questa pagina è lo spreadsheet {escape(agent)} per acquirenti in {escape(name)} su {escape(host)}: un indice, non Excel, non cassa. Keywords: {escape(kws)}.",
                f"Le foto QC arrivano nell’app ufficiale prima di prenotare la linea verso {escape(name)}. I finds di questo foglio sono SKU accettati, non un negozio.",
                f"Check locale: {escape(fp)}. {escape(duty)} Fonte: {escape(customs)}. Niente sottofatturazione.",
            ),
            "nl": (
                f"Deze pagina is de {escape(agent)} spreadsheet voor kopers in {escape(name)} op {escape(host)} — een index, geen Excel, geen kassa. Keywords: {escape(kws)}.",
                f"QC-foto’s landden in de officiële app vóór je een lijn naar {escape(name)} boekt. Finds op dit sheet zijn geaccepteerde SKU’s, geen winkel.",
                f"Lokaal: {escape(fp)}. {escape(duty)} Bron: {escape(customs)}. Geen onderwaardering.",
            ),
            "fi": (
                f"Tämä sivu on {escape(agent)} spreadsheet suomalaisille ostajille hostilla {escape(host)} — indeksi, ei Excel, ei kassa. Keywords: {escape(kws)}.",
                f"QC-kuvat tulevat viralliseen appiin ennen kuin varaat linjan Suomeen. Tämän sheetin findsit ovat hyväksyttyjä SKU:ita, ei kauppa.",
                f"Paikallinen: {escape(fp)}. {escape(duty)} Lähde: {escape(customs)}. Ei aliarvostusta.",
            ),
        },
        "finds": {
            "en": (
                f"{escape(agent)} finds for {escape(name)} sit on this dest desk, not as a second global catalogue. English index keys (sneakers, hoodie, jacket) still feed the catalogue on {escape(host)}.",
                f"QC the warehouse photos before a find leaves China toward {escape(name)}. A restricted or price-0 card is a dead source link, not a bargain.",
                f"{escape(fp)} is the address test for this host. Last-mile and duty notes: {escape(duty)} Source: {escape(customs)}.",
            ),
            "de": (
                f"{escape(agent)} Finds für {escape(name)} liegen auf diesem Dest-Desk, nicht als zweiter globaler Katalog. Englische Index-Keys speisen den Katalog auf {escape(host)}.",
                f"QC der Lagerfotos, bevor ein Find nach {escape(name)} geht. Restricted oder Preis 0 ist ein toter Link, kein Schnäppchen.",
                f"{escape(fp)} ist der Adresstest. {escape(duty)} Quelle: {escape(customs)}.",
            ),
            "es": (
                f"Los finds de {escape(agent)} para {escape(name)} viven en este desk, no como segundo catálogo global. Las claves inglesas alimentan el catálogo en {escape(host)}.",
                f"Haz QC de las fotos de almacén antes de que un find salga hacia {escape(name)}. Restricted o precio 0 es un enlace muerto, no una ganga.",
                f"{escape(fp)} es la prueba de dirección. {escape(duty)} Fuente: {escape(customs)}.",
            ),
            "fr": (
                f"Les finds {escape(agent)} pour {escape(name)} restent sur ce desk, pas un second catalogue mondial. Les clés anglaises alimentent le catalogue sur {escape(host)}.",
                f"QC des photos d’entrepôt avant qu’un find parte vers {escape(name)}. Restricted ou prix 0 est un lien mort, pas une affaire.",
                f"{escape(fp)} est le test d’adresse. {escape(duty)} Source : {escape(customs)}.",
            ),
            "it": (
                f"I finds {escape(agent)} per {escape(name)} stanno su questo desk, non un secondo catalogo globale. Le chiavi inglesi alimentano il catalogo su {escape(host)}.",
                f"QC delle foto di magazzino prima che un find parta verso {escape(name)}. Restricted o prezzo 0 è un link morto, non un affare.",
                f"{escape(fp)} è il test dell’indirizzo. {escape(duty)} Fonte: {escape(customs)}.",
            ),
            "nl": (
                f"{escape(agent)}-finds voor {escape(name)} staan op deze dest-desk, geen tweede globale catalogus. Engelse indexkeys voeden de catalogus op {escape(host)}.",
                f"QC de magazijnfoto’s voordat een find naar {escape(name)} vertrekt. Restricted of prijs 0 is een dode link, geen koopje.",
                f"{escape(fp)} is de adrescheck. {escape(duty)} Bron: {escape(customs)}.",
            ),
            "fi": (
                f"{escape(agent)} finds Suomelle ovat tällä deskillä, ei toisena globaalina katalogina. Englanninkieliset avaimet syöttävät katalogin hostilla {escape(host)}.",
                f"QC-varastokuvat ennen kuin find lähtee Suomeen. Restricted tai hinta 0 on kuollut linkki, ei löytö.",
                f"{escape(fp)} on osoitetesti. {escape(duty)} Lähde: {escape(customs)}.",
            ),
        },
        "qc": {
            "en": (
                f"QC on {escape(host)} means warehouse photos in the official {escape(agent)} app, taken in China, before you pay international freight to {escape(name)}.",
                f"Extra angles are often paid. Claim while the piece is still in the warehouse — not after {escape(customs)} has the carton.",
                f"Address fingerprint for this desk: {escape(fp)}. {escape(duty)} This HTML does not open tickets and does not coach a declared value.",
            ),
            "de": (
                f"QC auf {escape(host)} heißt Lagerfotos in der offiziellen {escape(agent)}-App in China, bevor du international nach {escape(name)} zahlst.",
                f"Extra-Winkel sind oft kostenpflichtig. Reklamieren, solange das Stück im Lager ist — nicht nachdem {escape(customs)} den Karton hat.",
                f"Adress-Fingerprint: {escape(fp)}. {escape(duty)} Dieses HTML öffnet keine Tickets und coacht keinen Deklarationswert.",
            ),
            "es": (
                f"QC en {escape(host)} son fotos de almacén en la app oficial de {escape(agent)}, en China, antes de pagar el flete a {escape(name)}.",
                f"Los ángulos extra suelen pagarse. Reclama mientras la pieza sigue en almacén, no después de {escape(customs)}.",
                f"Huella de dirección: {escape(fp)}. {escape(duty)} Este HTML no abre tickets ni inventa un valor declarado.",
            ),
            "fr": (
                f"Le QC sur {escape(host)} ce sont les photos d’entrepôt dans l’app officielle {escape(agent)}, en Chine, avant de payer le fret vers {escape(name)}.",
                f"Les angles extra sont souvent payants. Réclame tant que la pièce est en entrepôt, pas après {escape(customs)}.",
                f"Empreinte d’adresse : {escape(fp)}. {escape(duty)} Cet HTML n’ouvre pas de ticket et n’invente pas une valeur déclarée.",
            ),
            "it": (
                f"QC su {escape(host)} sono le foto di magazzino nell’app ufficiale {escape(agent)}, in Cina, prima di pagare il nolo verso {escape(name)}.",
                f"Gli angoli extra spesso si pagano. Reclama mentre il pezzo è in magazzino, non dopo {escape(customs)}.",
                f"Fingerprint indirizzo: {escape(fp)}. {escape(duty)} Questo HTML non apre ticket e non inventa un valore dichiarato.",
            ),
            "nl": (
                f"QC op {escape(host)} zijn magazijnfoto’s in de officiële {escape(agent)}-app, in China, vóór je internationaal naar {escape(name)} betaalt.",
                f"Extra hoeken zijn vaak betaald. Reclameer zolang het stuk in het magazijn ligt, niet na {escape(customs)}.",
                f"Adresfingerprint: {escape(fp)}. {escape(duty)} Deze HTML opent geen tickets en verzint geen aangegeven waarde.",
            ),
            "fi": (
                f"QC hostilla {escape(host)} tarkoittaa varastokuvia virallisessa {escape(agent)}-apissa Kiinassa, ennen kuin maksat rahdin Suomeen.",
                f"Lisäkulmat ovat usein maksullisia. Reklamoi kun kappale on vielä varastossa, ei tullin jälkeen ({escape(customs)}).",
                f"Osoite-fingerprint: {escape(fp)}. {escape(duty)} Tämä HTML ei avaa tikettejä eikä keksi ilmoitusarvoa.",
            ),
        },
        "shipping": {
            "en": (
                f"{escape(agent)} shipping to {escape(name)} is an official-estimator country code, not this TLD. Open the live freight form toward {escape(name)} after warehouse photos.",
                f"Who pays at the border is on the booked SKU (tax-free / prepaid / collect). Last-mile can add a collect fee. Source: {escape(customs)}.",
                f"Desk fingerprint: {escape(fp)}. {escape(duty)} Ranked shipping URLs on {escape(host)} stay — this page does not overwrite them with a live quote.",
            ),
            "de": (
                f"{escape(agent)}-Versand nach {escape(name)} ist ein Schätzer-Ländercode, nicht diese TLD. Offiziellen Schätzer nach {escape(name)} nach Lagerfotos öffnen.",
                f"Wer an der Grenze zahlt, steht auf der SKU. Die letzte Meile kann Collect-Gebühren addieren. Quelle: {escape(customs)}.",
                f"Fingerprint: {escape(fp)}. {escape(duty)} Rankende Versand-URLs auf {escape(host)} bleiben.",
            ),
            "es": (
                f"El envío {escape(agent)} a {escape(name)} es un código de país del estimador, no este TLD. Abre el formulario oficial hacia {escape(name)} tras las fotos de almacén.",
                f"Quién paga en frontera lo dice la SKU. La última milla puede añadir tasa Collect. Fuente: {escape(customs)}.",
                f"Huella: {escape(fp)}. {escape(duty)} Las URL de envío que ya posicionan en {escape(host)} se conservan.",
            ),
            "fr": (
                f"La livraison {escape(agent)} vers {escape(name)} est un code pays de l’estimateur, pas ce TLD. Ouvre le formulaire officiel vers {escape(name)} après les photos d’entrepôt.",
                f"Qui paie à la frontière est sur la SKU. Le dernier kilomètre peut ajouter des frais Collect. Source : {escape(customs)}.",
                f"Empreinte : {escape(fp)}. {escape(duty)} Les URL livraison déjà classées sur {escape(host)} restent.",
            ),
            "it": (
                f"La spedizione {escape(agent)} verso {escape(name)} è un codice paese dell’estimator, non questo TLD. Apri il modulo ufficiale verso {escape(name)} dopo le foto di magazzino.",
                f"Chi paga in dogana lo dice la SKU. L’ultimo miglio può aggiungere un fee Collect. Fonte: {escape(customs)}.",
                f"Fingerprint: {escape(fp)}. {escape(duty)} Gli URL spedizione già in ranking su {escape(host)} restano.",
            ),
            "nl": (
                f"{escape(agent)}-verzending naar {escape(name)} is een estimator-landcode, niet deze TLD. Open het officiële formulier naar {escape(name)} na magazijnfoto’s.",
                f"Wie aan de grens betaalt, staat op de SKU. Last-mile kan Collect-fees optellen. Bron: {escape(customs)}.",
                f"Fingerprint: {escape(fp)}. {escape(duty)} Rankende verzend-URL’s op {escape(host)} blijven.",
            ),
            "fi": (
                f"{escape(agent)}-toimitus Suomeen on arvioijan maakoodi, ei tämä TLD. Avaa virallinen lomake kohteeseen Suomi varastokuvien jälkeen.",
                f"Kuka maksaa rajalla, seisoo SKU:lla. Viimeinen kilometri voi lisätä Collect-maksun. Lähde: {escape(customs)}.",
                f"Fingerprint: {escape(fp)}. {escape(duty)} Rankkaavat toimitus-URL:t hostilla {escape(host)} säilyvät.",
            ),
        },
        "legal": {
            "en": (
                f"Is {escape(agent)} legal in {escape(name)}? {escape(agent)} is a purchasing agent: it buys from Chinese third-party shops in your name. {escape(host)} is an independent information desk, not the official app and not a customs office.",
                f"Using an agent is not a crime. Restricted goods, platform bans and the booked SKU still apply. Read {escape(customs)} the morning you ship. This page does not coach under-declaration.",
                f"Local address test: {escape(fp)}. {escape(duty)} Orders, payment and claims stay on the official {escape(agent)} site.",
            ),
            "de": (
                f"Ist {escape(agent)} in {escape(name)} legal? {escape(agent)} ist ein Einkaufsagent. {escape(host)} ist ein Infodesk, nicht die offizielle App und kein Zollamt.",
                f"Einen Agenten zu nutzen ist keine Straftat. Restricted, Plattformregeln und die SKU gelten weiter. {escape(customs)} am Versandmorgen lesen. Keine Unterdeklaration.",
                f"Adresstest: {escape(fp)}. {escape(duty)} Bestellung und Reklamation nur auf der offiziellen {escape(agent)}-Seite.",
            ),
            "es": (
                f"¿Es legal {escape(agent)} en {escape(name)}? {escape(agent)} es un agente de compras. {escape(host)} es un desk informativo, no la app oficial ni aduanas.",
                f"Usar un agente no es un delito. Restricted, normas de plataforma y la SKU siguen. Lee {escape(customs)} el día del envío. Sin infradeclaración.",
                f"Prueba de dirección: {escape(fp)}. {escape(duty)} Pedidos y reclamaciones solo en el sitio oficial de {escape(agent)}.",
            ),
            "fr": (
                f"{escape(agent)} est-il légal en {escape(name)} ? {escape(agent)} est un agent d’achat. {escape(host)} est un desk d’information, pas l’app officielle ni la douane.",
                f"Utiliser un agent n’est pas un délit. Restricted, règles plateforme et SKU restent. Lis {escape(customs)} le matin de l’envoi. Pas de sous-déclaration.",
                f"Test d’adresse : {escape(fp)}. {escape(duty)} Commandes et réclamations uniquement sur le site officiel {escape(agent)}.",
            ),
            "it": (
                f"{escape(agent)} è legale in {escape(name)}? {escape(agent)} è un agente d’acquisto. {escape(host)} è un desk informativo, non l’app ufficiale né la dogana.",
                f"Usare un agente non è un reato. Restricted, regole piattaforma e SKU restano. Leggi {escape(customs)} il giorno della spedizione. Niente sottofatturazione.",
                f"Test indirizzo: {escape(fp)}. {escape(duty)} Ordini e reclami solo sul sito ufficiale {escape(agent)}.",
            ),
            "nl": (
                f"Is {escape(agent)} legaal in {escape(name)}? {escape(agent)} is een inkoopagent. {escape(host)} is een infodesk, niet de officiële app en geen douane.",
                f"Een agent gebruiken is geen misdrijf. Restricted, platformregels en de SKU blijven. Lees {escape(customs)} op de verzenddag. Geen onderwaardering.",
                f"Adrescheck: {escape(fp)}. {escape(duty)} Bestellen en klachten alleen op de officiële {escape(agent)}-site.",
            ),
            "fi": (
                f"Onko {escape(agent)} laillinen Suomessa? {escape(agent)} on ostoagentti. {escape(host)} on infodesk, ei virallinen appi eikä tulli.",
                f"Agentin käyttö ei ole rikos. Restricted, alustasäännöt ja SKU pätevät. Lue {escape(customs)} lähetysaamuna. Ei aliarvostusta.",
                f"Osoitetesti: {escape(fp)}. {escape(duty)} Tilaukset ja reklamaatiot vain virallisella {escape(agent)}-sivustolla.",
            ),
        },
        "guide": {
            "en": (
                f"Guide: paste a source link into official {escape(agent)}, wait for warehouse QC, then book a line to {escape(name)} in the estimator — not this hostname.",
                f"The spreadsheet on {escape(host)} is the haul log (item, QC, line, tracking). Catalogue search stays English keys. Lab {DATE}.",
                f"{escape(fp)}. {escape(duty)} Source: {escape(customs)}. Sister country hosts stay separate files — no 301.",
            ),
            "de": (
                f"Ablauf: Quell-Link in offizielles {escape(agent)} kleben, QC abwarten, dann Linie nach {escape(name)} im Schätzer — nicht dieser Hostname.",
                f"Das Spreadsheet auf {escape(host)} ist das Haul-Log (Item, QC, Linie, Tracking). Katalogsuche bleibt englische Keys. Lab {DATE}.",
                f"{escape(fp)}. {escape(duty)} Quelle: {escape(customs)}. Schwester-Länderhosts bleiben eigene Dateien — kein 301.",
            ),
            "es": (
                f"Guía: pega el enlace en el {escape(agent)} oficial, espera el QC de almacén y reserva la línea a {escape(name)} en el estimador, no este hostname.",
                f"El spreadsheet de {escape(host)} es el haul log (ítem, QC, línea, tracking). La búsqueda del catálogo sigue en claves inglesas. Lab {DATE}.",
                f"{escape(fp)}. {escape(duty)} Fuente: {escape(customs)}. Los hosts hermanos siguen en archivos separados — sin 301.",
            ),
            "fr": (
                f"Guide : colle le lien dans {escape(agent)} officiel, attends le QC entrepôt, puis réserve une ligne vers {escape(name)} dans l’estimateur — pas ce nom d’hôte.",
                f"Le spreadsheet sur {escape(host)} est le haul log (pièce, QC, ligne, tracking). La recherche catalogue reste des clés anglaises. Lab {DATE}.",
                f"{escape(fp)}. {escape(duty)} Source : {escape(customs)}. Les hôtes sœurs restent des fichiers séparés — pas de 301.",
            ),
            "it": (
                f"Guida: incolla il link nell’{escape(agent)} ufficiale, aspetta il QC di magazzino, poi prenota la linea verso {escape(name)} nell’estimator — non questo hostname.",
                f"Lo spreadsheet su {escape(host)} è il haul log (pezzo, QC, linea, tracking). La ricerca catalogo resta chiavi inglesi. Lab {DATE}.",
                f"{escape(fp)}. {escape(duty)} Fonte: {escape(customs)}. Gli host fratelli restano file separati — niente 301.",
            ),
            "nl": (
                f"Gids: plak de bronlink in officiële {escape(agent)}, wacht op magazijn-QC, boek daarna een lijn naar {escape(name)} in de estimator — niet deze hostname.",
                f"De spreadsheet op {escape(host)} is de haul-log (item, QC, lijn, tracking). Cataloguszoeken blijft Engelse keys. Lab {DATE}.",
                f"{escape(fp)}. {escape(duty)} Bron: {escape(customs)}. Zushosts blijven aparte bestanden — geen 301.",
            ),
            "fi": (
                f"Ohje: liitä lähdelinkki viralliseen {escape(agent)}-appiin, odota varasto-QC, varaa sitten linja Suomeen arvioijassa — ei tämä hostname.",
                f"Spreadsheet hostilla {escape(host)} on haul-loki (tuote, QC, linja, seurantanumero). Katalogihaku pysyy englanninkielisinä avaimina. Lab {DATE}.",
                f"{escape(fp)}. {escape(duty)} Lähde: {escape(customs)}. Sisarhostit pysyvät erillisinä tiedostoina — ei 301.",
            ),
        },
        "faq": {
            "en": (
                f"Does {escape(host)} sell the items? No. {escape(agent)} is the purchasing agent. This hostname is the {escape(name)} spreadsheet desk — catalogue, QC notes, shipping-to-{escape(name)}, legal.",
                f"Pay twice: goods + China domestic, then the international SKU. Bundle in the warehouse. Storage: confirm official Help the morning you ship. Lab {DATE}.",
                f"{escape(fp)}. {escape(duty)} Source: {escape(customs)}. No declared-value coaching. Claims only on the official {escape(agent)} site.",
            ),
            "de": (
                f"Verkauft {escape(host)} die Ware? Nein. {escape(agent)} ist der Einkaufsagent. Dieser Hostname ist das Spreadsheet-Desk für {escape(name)}.",
                f"Zwei Zahlungen: Ware plus Inland China, dann die internationale SKU. Im Lager bündeln. Speicherfrist: offizielles Help am Versandmorgen. Lab {DATE}.",
                f"{escape(fp)}. {escape(duty)} Quelle: {escape(customs)}. Keine Unterdeklaration.",
            ),
            "es": (
                f"¿{escape(host)} vende los productos? No. {escape(agent)} es el agente. Este hostname es el desk spreadsheet para {escape(name)}.",
                f"Pagas dos veces: mercancía más China doméstico, luego la SKU internacional. Agrupa en almacén. Almacén: confirma Help el día del envío. Lab {DATE}.",
                f"{escape(fp)}. {escape(duty)} Fuente: {escape(customs)}. Sin infradeclaración.",
            ),
            "fr": (
                f"{escape(host)} vend-il les pièces ? Non. {escape(agent)} est l’agent d’achat. Ce nom d’hôte est le desk spreadsheet pour {escape(name)}.",
                f"Deux paiements : marchandises plus Chine domestique, puis la SKU internationale. Groupe à l’entrepôt. Stockage : Help officiel le matin de l’envoi. Lab {DATE}.",
                f"{escape(fp)}. {escape(duty)} Source : {escape(customs)}. Pas de sous-déclaration.",
            ),
            "it": (
                f"{escape(host)} vende i pezzi? No. {escape(agent)} è l’agente. Questo hostname è il desk spreadsheet per {escape(name)}.",
                f"Due pagamenti: merce più Cina domestica, poi la SKU internazionale. Raggruppa in magazzino. Stoccaggio: Help ufficiale il giorno della spedizione. Lab {DATE}.",
                f"{escape(fp)}. {escape(duty)} Fonte: {escape(customs)}. Niente sottofatturazione.",
            ),
            "nl": (
                f"Verkoopt {escape(host)} de spullen? Nee. {escape(agent)} is de inkoopagent. Deze hostname is de spreadsheet-desk voor {escape(name)}.",
                f"Twee betalingen: goederen plus binnenlands China, daarna de internationale SKU. Bundel in het magazijn. Opslag: officiële Help op de verzenddag. Lab {DATE}.",
                f"{escape(fp)}. {escape(duty)} Bron: {escape(customs)}. Geen onderwaardering.",
            ),
            "fi": (
                f"Myykö {escape(host)} tuotteet? Ei. {escape(agent)} on ostoagentti. Tämä hostname on spreadsheet-desk Suomelle.",
                f"Kaksi maksua: tavara plus Kiinan kotimaan rahti, sitten kansainvälinen SKU. Yhdistä varastossa. Varastointi: virallinen Help lähetysaamuna. Lab {DATE}.",
                f"{escape(fp)}. {escape(duty)} Lähde: {escape(customs)}. Ei aliarvostusta.",
            ),
        },
    }
    row = blocks[kind]
    a, b, c = row.get(loc, row["en"])
    return f"""<article class="cluster-page" {MARKER} data-kind="{kind}">
<h1>{escape(title)}</h1>
<p class="lead">{a}</p>
<p>{b}</p>
<p>{c}</p>
<h2>{escape(labs(spec)["spreadsheet"])} / finds / QC / {escape(labs(spec)["shipping"])}</h2>
<ul class="cluster-links">{nav}</ul>
<p class="legal-note">{escape(host)} is an information desk for {escape(dest)}, not {escape(agent)}. Sister country hosts stay separate files — no 301. Copy reviewed {DATE}.</p>
</article>
"""


def _head_inner(html: str) -> str:
    m = re.search(r"<head\b[^>]*>([\s\S]*)</head>", html, re.I)
    return m.group(1) if m else ""


def _html_tag(html: str) -> str:
    m = re.search(r"<html\b[^>]*>", html, re.I)
    return m.group(0) if m else "<html>"


def _first_block(html: str, tag: str) -> str:
    m = re.search(rf"<{tag}\b[^>]*>[\s\S]*?</{tag}>", html, re.I)
    return m.group(0) if m else ""


def replace_title(html: str, title: str, desc: str | None = None) -> str:
    esc = escape(title)
    html = re.sub(r"<title>[\s\S]*?</title>", f"<title>{esc}</title>", html, count=1, flags=re.I)
    html = re.sub(
        r'(<meta\s+property="og:title"\s+content=")[^"]*(")',
        rf"\1{esc}\2",
        html,
        count=1,
        flags=re.I,
    )
    if desc:
        d = escape(desc)
        html = re.sub(
            r'(<meta\s+name="description"\s+content=")[^"]*(")',
            rf"\1{d}\2",
            html,
            count=1,
            flags=re.I,
        )
        html = re.sub(
            r'(<meta\s+property="og:description"\s+content=")[^"]*(")',
            rf"\1{d}\2",
            html,
            count=1,
            flags=re.I,
        )
    return html


def upsert_keywords(html: str, keywords: list[str]) -> str:
    content = escape(", ".join(keywords))
    tag = f'<meta name="keywords" content="{content}">'
    if re.search(r'<meta\s+name="keywords"', html, re.I):
        return re.sub(r'<meta\s+name="keywords"[^>]*>', tag, html, count=1, flags=re.I)
    if "<title>" in html.lower():
        return re.sub(r"(</title>)", r"\1\n" + tag, html, count=1, flags=re.I)
    return tag + html


def replace_first_h1(html: str, h1: str) -> str:
    return re.sub(r"<h1\b[^>]*>[\s\S]*?</h1>", f"<h1>{h1}</h1>", html, count=1, flags=re.I)


def patch_jsonld(html: str, spec: dict, *, url: str, name: str, desc: str) -> str:
    keywords = spec["keywords"]

    def repl(m: re.Match) -> str:
        raw = m.group(1).strip()
        try:
            data = json.loads(raw)
        except json.JSONDecodeError:
            return m.group(0)
        if not isinstance(data, dict):
            return m.group(0)
        typ = data.get("@type")
        if typ in ("WebPage", "WebSite"):
            data["name"] = name
            if desc:
                data["description"] = desc
        if typ == "WebSite":
            data["keywords"] = keywords
            data["url"] = url
        return f'<script type="application/ld+json">{json.dumps(data, ensure_ascii=False)}</script>'

    html = re.sub(
        r'<script type="application/ld\+json">([\s\S]*?)</script>',
        repl,
        html,
        flags=re.I,
    )
    if '"@type": "WebSite"' not in html and '"@type":"WebSite"' not in html:
        html = inject_jsonld(
            html,
            website_ld(
                url=url,
                name=name,
                lang=spec["lang"],
                brand=spec["agent"],
                host=spec["host"],
                keywords=keywords,
            ),
            webpage_ld(
                url=url,
                name=name,
                desc=desc,
                lang=spec["lang"],
                brand=spec["agent"],
                host=spec["host"],
            ),
        )
    return html


def rewrite_uplink(html: str, spec: dict) -> str:
    m = re.search(r'(<p class="hub-uplink"[^>]*>)([\s\S]*?)(</p>)', html, re.I)
    if not m:
        return html
    hrefs = re.findall(r'href="(https://[^"]+)"', m.group(2))
    hub = hrefs[0] if hrefs else ""
    name = cluster_country_name(spec["dest"], spec["loc"], spec["dest_label"])
    loc = spec["loc"]
    hub_bit = f' Global catalogue → <a href="{escape(hub)}">{escape(hub)}</a>.' if hub else ""
    copy = {
        "de": f"Dieses Host ist das {escape(spec['agent'])} Spreadsheet für Käufer in {escape(name)}.{hub_bit} Versand, QC und Legal bleiben auf {escape(spec['host'])}.",
        "es": f"Este host es el spreadsheet {escape(spec['agent'])} para compradores en {escape(name)}.{hub_bit} Envío, QC y legal siguen en {escape(spec['host'])}.",
        "fr": f"Cet hôte est le spreadsheet {escape(spec['agent'])} pour les acheteurs en {escape(name)}.{hub_bit} Livraison, QC et legal restent sur {escape(spec['host'])}.",
        "it": f"Questo host è lo spreadsheet {escape(spec['agent'])} per acquirenti in {escape(name)}.{hub_bit} Spedizione, QC e legal restano su {escape(spec['host'])}.",
        "nl": f"Dit host is de {escape(spec['agent'])} spreadsheet voor kopers in {escape(name)}.{hub_bit} Verzending, QC en legal blijven op {escape(spec['host'])}.",
        "fi": f"Tämä host on {escape(spec['agent'])} spreadsheet suomalaisille ostajille.{hub_bit} Toimitus, QC ja legal pysyvät hostilla {escape(spec['host'])}.",
        "en": f"This host is the {escape(spec['agent'])} spreadsheet for {escape(name)} buyers.{hub_bit} Shipping, QC and legal stay on {escape(spec['host'])}.",
    }
    inner = copy.get(loc, copy["en"])
    return html[: m.start()] + m.group(1) + inner + m.group(3) + html[m.end() :]


def cluster_nav(spec: dict, pages: dict[str, tuple[str, Path | None]]) -> str:
    loc = spec["loc"]
    labels = labs(spec)
    items = "".join(
        f'<a href="{escape(pages[k][0])}">{escape(labels[k])}</a>'
        for k in KINDS
        if k in pages
    )
    heading = {
        "de": "Spreadsheet-Cluster",
        "es": "Cluster spreadsheet",
        "fr": "Cluster spreadsheet",
        "it": "Cluster spreadsheet",
        "nl": "Spreadsheet-cluster",
        "fi": "Spreadsheet-klusteri",
        "en": "Spreadsheet cluster",
    }.get(loc, "Spreadsheet cluster")
    return (
        f'<nav class="cluster-nav" {MARKER} aria-label="{escape(heading)}">'
        f"<strong>{escape(heading)}</strong> {items}</nav>"
    )


def ensure_cluster_nav(html: str, spec: dict, pages: dict) -> str:
    if 'class="cluster-nav"' in html:
        html = re.sub(
            r'<nav class="cluster-nav"[^>]*>[\s\S]*?</nav>',
            cluster_nav(spec, pages),
            html,
            count=1,
            flags=re.I,
        )
        return html
    nav = cluster_nav(spec, pages)
    if re.search(r"</h1>", html, re.I):
        return re.sub(r"</h1>", "</h1>\n" + nav, html, count=1, flags=re.I)
    return html


CLUSTER_CSS = (
    '<style id="spreadsheet-cluster-css">'
    ".cluster-nav{display:flex;flex-wrap:wrap;gap:8px 14px;align-items:center;"
    "margin:12px 0 8px;font-size:14px;font-weight:600}"
    ".cluster-nav a{text-decoration:none}"
    ".cluster-page{max-width:760px;margin:0 auto;padding:8px 0 24px}"
    ".cluster-page .lead{font-size:18px;line-height:1.65}"
    ".cluster-links{display:grid;gap:6px}"
    "</style>\n"
)


def patch_home(html: str, spec: dict, pages: dict) -> str:
    url = f"https://{spec['host']}/"
    html = replace_title(html, spec["title"], spec["desc"])
    html = upsert_keywords(html, spec["keywords"])
    html = replace_first_h1(html, escape(spec["h1"]))
    html = patch_jsonld(html, spec, url=url, name=spec["title"], desc=spec["desc"])
    html = rewrite_uplink(html, spec)
    html = ensure_cluster_nav(html, spec, pages)
    if 'id="spreadsheet-cluster-css"' not in html and "</head>" in html.lower():
        html = re.sub(r"</head>", CLUSTER_CSS + "</head>", html, count=1, flags=re.I)
    if MARKER.split("=")[0] not in html:
        html = html.replace("<body", f"<body {MARKER}", 1)
    return html


def write_inner_file(spec: dict, kind: str, slug: str, pages: dict, chrome_html: str) -> Path:
    overlay = overlay_dir(spec["host"])
    if slug.endswith(".html") and "/" not in slug.strip("/"):
        dest = overlay / slug.lstrip("/")
    else:
        rel = slug.strip("/")
        dest = overlay / rel / "index.html"
    dest.parent.mkdir(parents=True, exist_ok=True)
    title = inner_title(kind, spec)
    desc = spec["desc"]
    url = f"https://{spec['host']}{slug if slug.endswith('/') or slug.endswith('.html') else slug + '/'}"
    header = _first_block(chrome_html, "header")
    footer = _first_block(chrome_html, "footer")
    head = _head_inner(chrome_html)
    head = re.sub(r"<title>[\s\S]*?</title>", f"<title>{escape(title)}</title>", head, count=1, flags=re.I)
    head = re.sub(
        r'(<link rel="canonical" href=")[^"]*(")',
        rf"\1{escape(url)}\2",
        head,
        count=1,
        flags=re.I,
    )
    if 'rel="canonical"' not in head.lower():
        head += f'\n<link rel="canonical" href="{escape(url)}">'
    head = upsert_keywords(f"<title>{escape(title)}</title>\n" + head, spec["keywords"])
    head = re.sub(r"<title>[\s\S]*?</title>\s*<title>[\s\S]*?</title>", f"<title>{escape(title)}</title>", head, count=1)
    skip = skip_link(skip_label(spec["loc"]))
    body = inner_body(kind, spec, pages)
    html = (
        "<!DOCTYPE html>\n"
        f"{_html_tag(chrome_html)}\n"
        f"<head>\n{head.strip()}\n</head>\n"
        f"<body {MARKER}>\n"
        f"{skip}"
        f"{header}\n"
        f'<main id="main" class="container inner-article">\n{body}\n</main>\n'
        f"{footer}\n"
        "</body></html>\n"
    )
    html = patch_jsonld(html, spec, url=url, name=title, desc=desc)
    dest.write_text(html, encoding="utf-8")
    return dest


def patch_existing_inner(path: Path, spec: dict, kind: str) -> None:
    html = path.read_text(encoding="utf-8", errors="replace")
    title = inner_title(kind, spec)
    html = replace_title(html, title, spec["desc"])
    html = upsert_keywords(html, spec["keywords"])
    html = replace_first_h1(html, escape(title))
    slug_guess = "/"
    try:
        rel = path.relative_to(overlay_dir(spec["host"])).as_posix()
        if rel.endswith("/index.html"):
            slug_guess = "/" + rel[: -len("/index.html")] + "/"
        elif rel.endswith("/live-base.index.html"):
            slug_guess = "/" + str(path.parent.relative_to(overlay_dir(spec["host"]))) + "/"
        elif rel.endswith(".html"):
            slug_guess = "/" + path.name
    except ValueError:
        pass
    url = f"https://{spec['host']}{slug_guess}"
    html = patch_jsonld(html, spec, url=url, name=title, desc=spec["desc"])
    path.write_text(html, encoding="utf-8")


def forbidden_hits(html: str, spec: dict) -> list[str]:
    err = []
    for pat in FORBIDDEN_HTML:
        if re.search(pat, html, flags=re.I) and not (
            spec.get("dest") == "ES" and spec.get("agent") == "HipoBuy"
        ):
            err.append(pat)
    return err


def fallback_chrome_file(spec: dict) -> Path | None:
    if not spec.get("php"):
        return None
    for other in ("cssbuy.es", "cssbuy.nl", "cssbuy.fr", "cssbuy.it"):
        hf = home_file(other)
        if hf is not None:
            return hf
    return None


def generate_one(spec: dict) -> dict:
    host = spec["host"]
    home = home_file(host)
    chrome_src = home or fallback_chrome_file(spec)
    if chrome_src is None:
        return {"host": host, "status": "no-home"}
    pages = map_pages(spec)
    raw = chrome_src.read_text(encoding="utf-8", errors="replace")
    patched = patch_home(raw, spec, pages)
    hits = forbidden_hits(patched, spec)
    if hits:
        raise RuntimeError(f"{host} home forbidden {hits}")
    if home is not None:
        home.write_text(patched, encoding="utf-8")
        home_rel = str(home.relative_to(OUT))
        status = "ok"
    else:
        home_rel = ""
        status = "ok-php-inners-only"
    wrote = []
    for kind, (slug, path) in pages.items():
        default = default_slug(kind, spec)
        if path and path.is_file() and path.stat().st_size >= 1200:
            patch_existing_inner(path, spec, kind)
            wrote.append((kind, slug, "patched", str(path.relative_to(OUT))))
        elif path is None and slug.rstrip("/") != default.rstrip("/"):
            # Ranked keep URL with no overlay copy — do not smash live unique HTML.
            wrote.append((kind, slug, "keep-live", ""))
        else:
            dest = write_inner_file(spec, kind, slug, pages, patched)
            wrote.append((kind, slug, "created", str(dest.relative_to(OUT))))
    return {"host": host, "status": status, "home": home_rel, "pages": wrote}


def generate() -> list[dict]:
    keep_maps = _import_keep_maps()
    rows = []
    for host in dest_hosts():
        if host in TWINS or host in UNIQUE_PHP_HUBS:
            rows.append({"host": host, "status": "skip-twin-or-php"})
            continue
        spec = spec_for(host, keep_maps)
        rows.append(generate_one(spec))
    return rows


def check(rows: list[dict] | None = None) -> None:
    keep_maps = _import_keep_maps()
    bad = []
    n_ok = 0
    for host in dest_hosts():
        if host in TWINS or host in UNIQUE_PHP_HUBS:
            hf = home_file(host)
            if hf and MARKER.split("=")[0] in hf.read_text(encoding="utf-8", errors="replace"):
                bad.append(f"{host} twin should not be clustered")
            continue
        spec = spec_for(host, keep_maps)
        home = home_file(host)
        if home is None and spec.get("php"):
            pages = map_pages(spec)
        elif home is None:
            bad.append(f"{host} missing home")
            continue
        else:
            html = home.read_text(encoding="utf-8", errors="replace")
            if spec["title"] not in html:
                bad.append(f"{host} missing title {spec['title']!r}")
            if spec["h1"] not in html:
                bad.append(f"{host} missing h1")
            for kw in spec["keywords"]:
                if kw.lower() not in html.lower():
                    bad.append(f"{host} missing keyword {kw}")
                    break
            if "application/ld+json" not in html:
                bad.append(f"{host} missing JSON-LD")
            if spec["fingerprint"] and spec["fingerprint"] not in html:
                if 'id="local"' not in html:
                    bad.append(f"{host} missing fingerprint/{'#local'}")
            pages = map_pages(spec)
        for kind, (slug, path) in pages.items():
            overlay = overlay_dir(host)
            default = default_slug(kind, spec)
            if path and path.is_file():
                p = path
            elif slug.rstrip("/") != default.rstrip("/"):
                continue
            elif slug.endswith(".html") and slug.count("/") == 1:
                p = overlay / slug.lstrip("/")
            else:
                p = overlay / slug.strip("/") / "index.html"
            if not p.is_file():
                bad.append(f"{host} missing inner {kind} {slug}")
                continue
            inner = p.read_text(encoding="utf-8", errors="replace")
            if spec["keywords"][0].split()[0].lower() not in inner.lower():
                bad.append(f"{host} {kind} missing brand")
        n_ok += 1
    if bad:
        raise SystemExit("CHECK_FAIL\n" + "\n".join(bad[:40]))
    print("CHECK_OK", n_ok, "dests")


def _connect():
    try:
        import paramiko
    except ImportError:
        import subprocess

        subprocess.check_call([sys.executable, "-m", "pip", "install", "paramiko", "-q"])
        import paramiko

    password = os.environ.get("ORIGIN_SSH_PASS")
    if not password:
        cred = Path("/tmp/hipobuy-creds/origin.pass")
        if cred.is_file():
            password = cred.read_text().strip()
    if not password:
        raise SystemExit("Set ORIGIN_SSH_PASS")
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect("31.97.41.31", username="root", password=password, timeout=30)
    return client


def _run(client, cmd: str, timeout: int = 120) -> str:
    _, stdout, stderr = client.exec_command(cmd, timeout=timeout)
    return (stdout.read() + stderr.read()).decode(errors="replace").strip()


def put() -> None:
    rows = generate()
    check(rows)
    client = _connect()
    stamp = time.strftime("%Y%m%d-%H%M%S")
    bak = f"/www/backup/dest-spreadsheet-cluster-{stamp}"
    print(_run(client, f"mkdir -p '{bak}'"))
    sftp = client.open_sftp()
    put_n = 0
    skip_n = 0
    for row in rows:
        host = row["host"]
        if not str(row.get("status", "")).startswith("ok"):
            skip_n += 1
            continue
        remote_root = f"/www/wwwroot/{host}"
        overlay = overlay_dir(host)
        _run(client, f"mkdir -p '{bak}/{host}' '{remote_root}'")
        home_rel = row.get("home") or ""
        home_local = (OUT / home_rel) if home_rel else None
        # CSSBuy PHP gold is cssbuy-lite; some ccTLDs still serve a static
        # wwwroot/index.html (cssbuy.es). Patch that file, never public/index.php.
        put_home = bool(home_local and home_local.is_file() and home_local.name == "index.html")
        if put_home:
            remote = f"{remote_root}/index.html"
            _run(client, f"test -f '{remote}' && cp -a '{remote}' '{bak}/{host}/index.html' || true")
            sftp.put(str(home_local), remote)
            _run(client, f"chown www:www '{remote}'")
            put_n += 1
        for kind, slug, how, rel in row.get("pages") or []:
            if how == "keep-live":
                continue
            if host in PHP_CSSBUY and slug.rstrip("/") in {
                "/spreadsheet",
                "/guide/shipping",
                "/guide/customs",
                "/guide/first-order",
            }:
                continue
            local = OUT / rel
            if not local.is_file():
                continue
            rel_web = slug.lstrip("/")
            if rel_web.endswith("/"):
                remote = f"{remote_root}/{rel_web}index.html"
                _run(client, f"mkdir -p '{remote_root}/{rel_web}'")
            else:
                remote = f"{remote_root}/{rel_web}"
                _run(client, f"mkdir -p '{str(Path(remote).parent)}'")
            try:
                _run(client, f"test -f '{remote}' && cp -a '{remote}' '{bak}/{host}/{rel_web.replace('/', '_')}' || true")
                sftp.put(str(local), remote)
                _run(client, f"chown www:www '{remote}'")
                put_n += 1
            except OSError as exc:
                print("PUT_FAIL", host, slug, exc)
        print("PUT", host)
    sftp.close()
    if PHP_CSSBUY:
        php_root = ROOT / "sites" / "cssbuy-shared" / "php"
        php_files = [
            (php_root / "overlay/app/Http/Controllers/HomeController.php", "/www/wwwroot/cssbuy-lite/app/Http/Controllers/HomeController.php"),
            (php_root / "overlay/resources/views/home.php", "/www/wwwroot/cssbuy-lite/resources/views/home.php"),
            (php_root / "overlay/resources/views/layouts/app.php", "/www/wwwroot/cssbuy-lite/resources/views/layouts/app.php"),
            (php_root / "overlay/app/Services/DestLocal.php", "/www/wwwroot/cssbuy-lite/app/Services/DestLocal.php"),
        ]
        for local, remote in php_files:
            if not local.is_file():
                continue
            if "/public/" in remote:
                raise SystemExit(f"refusing public gold {remote}")
            _run(client, f"cp -a '{remote}' '{bak}/php-{Path(remote).name}'")
            sftp2 = client.open_sftp()
            sftp2.put(str(local), remote)
            sftp2.close()
            _run(client, f"chown www:www '{remote}'")
            print("PUT", remote)
            put_n += 1
    client.close()
    print("PUT_DONE", put_n, "skip", skip_n, "backup", bak)


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "generate"
    if cmd == "put":
        put()
    elif cmd == "check":
        check()
    else:
        rows = generate()
        ok = sum(1 for r in rows if r.get("status") == "ok")
        skip = sum(1 for r in rows if str(r.get("status", "")).startswith("skip"))
        print("generated", ok, "skip", skip)
        check(rows)
