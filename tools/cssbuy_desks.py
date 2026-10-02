#!/usr/bin/env python3
"""CSSBuy country desks: dest-unique #local inside the live PHP gold.

Gates:
1. Each host #local has that dest fingerprint, no sister fingerprints.
2. Estimator country ≠ TLD; .eu must say it is not a customs territory.
3. Titles have no invite code; body has no customs coaching / 58-line snapshot.
4. Same-agent country URLs stay independent (no 301).
5. Same-country twins: target #local first, then keep 301; deep paths must not 404.
6. PHP gold (cssbuy-lite) stays the CMS — never PUT a 5KB country template over public/.

Order: PHP AT → ES → FR → IT → NL, then static CA / UK / DE / US, then EU hub.
Twins cssbuyspreadsheet.{es,fr,it,nl} already 301 to cssbuy.* — do not reverse.
"""
from __future__ import annotations

import json
import os
import re
import sys
import time
from html import escape
from pathlib import Path

_TOOLS = Path(__file__).resolve().parent
if str(_TOOLS) not in sys.path:
    sys.path.insert(0, str(_TOOLS))
from desk_template import (
    SKIP_CSS,
    _check_local_section,
    dest_local_pack,
    local_cta,
    local_guide_html,
    skip_label,
    skip_link,
    validate_desk,
)

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "sites"
PHP_OUT = OUT / "cssbuy-shared" / "php"
LIVE_PHP = PHP_OUT / "live-base"
EST = "https://www.cssbuy.com/?action=estimates&go=page"
OFFICIAL = "https://www.cssbuy.com/"
DATE = "2 Oct 2026"
INVITE = "1Yi9"
STORAGE = (
    "90 free days from In Warehouse (official CSSBuy warehouse FAQ), "
    "then ¥15 per order per month; confirm live Help the morning you ship"
)
BRAND = "#E85D1A"

# PHP gold — shared cssbuy-lite, keyed by HTTP_HOST. Do not overwrite public/.
PHP_HOSTS = {
    "at": {
        "host": "cssbuy.at",
        "lang": "de-AT",
        "locale": "Österreich",
        "loc": "de",
        "dest": "AT",
        "dest_label": "Österreich",
        "ccy": "EUR",
        "keep": [
            ("/guide/shipping", "Versand"),
            ("/guide/customs", "Zoll"),
            ("/spreadsheet", "Spreadsheet"),
            ("/guide/first-order", "Erste Bestellung"),
        ],
    },
    "es": {
        "host": "cssbuy.es",
        "lang": "es-ES",
        "locale": "España",
        "loc": "es",
        "dest": "ES",
        "dest_label": "España",
        "ccy": "EUR",
        "keep": [
            ("/guide/shipping", "Envío"),
            ("/guide/customs", "Aduanas"),
            ("/spreadsheet", "Spreadsheet"),
            ("/guide/first-order", "Primer pedido"),
        ],
    },
    "fr": {
        "host": "cssbuy.fr",
        "lang": "fr-FR",
        "locale": "France",
        "loc": "fr",
        "dest": "FR",
        "dest_label": "France",
        "ccy": "EUR",
        "keep": [
            ("/guide/shipping", "Livraison"),
            ("/guide/customs", "Douane"),
            ("/spreadsheet", "Spreadsheet"),
            ("/guide/first-order", "Première commande"),
        ],
    },
    "it": {
        "host": "cssbuy.it",
        "lang": "it-IT",
        "locale": "Italia",
        "loc": "it",
        "dest": "IT",
        "dest_label": "Italia",
        "ccy": "EUR",
        "keep": [
            ("/guide/shipping", "Spedizione"),
            ("/guide/customs", "Dogana"),
            ("/spreadsheet", "Spreadsheet"),
            ("/guide/first-order", "Primo ordine"),
        ],
    },
    "nl": {
        "host": "cssbuy.nl",
        "lang": "nl-NL",
        "locale": "Nederland",
        "loc": "nl",
        "dest": "NL",
        "dest_label": "Nederland",
        "ccy": "EUR",
        "keep": [
            ("/guide/shipping", "Verzending"),
            ("/guide/customs", "Douane"),
            ("/spreadsheet", "Spreadsheet"),
            ("/guide/first-order", "Eerste bestelling"),
        ],
    },
}

# Independent static dests. Deepen in place. Never 301 onto a PHP ccTLD.
STATIC_HOSTS = {
    "ca": {
        "host": "cssbuyspreadsheet.ca",
        "lang": "en-CA",
        "locale": "Canada",
        "loc": "en",
        "dest": "CA",
        "dest_label": "Canada",
        "ccy": "CAD",
        "keep": [
            ("/spreadsheet/", "Spreadsheet"),
            ("/faq/", "FAQ"),
            ("/guides/", "Guides"),
            ("/guides/shipping/", "Shipping to Canada"),
        ],
    },
    "uk": {
        "host": "cssbuyspreadsheet.uk",
        "lang": "en-GB",
        "locale": "United Kingdom",
        "loc": "en",
        "dest": "GB",
        "dest_label": "the United Kingdom",
        "ccy": "GBP",
        "keep": [
            ("/spreadsheet/", "Spreadsheet"),
            ("/faq/", "FAQ"),
            ("/guides/", "Guides"),
            ("/guides/shipping/", "Shipping to the UK"),
        ],
    },
    "de": {
        "host": "cssbuyspreadsheets.de",
        "lang": "de-DE",
        "locale": "Deutschland",
        "loc": "de",
        "dest": "DE",
        "dest_label": "Deutschland",
        "ccy": "EUR",
        "keep": [
            ("/spreadsheet/", "Spreadsheet"),
            ("/faq/", "Zoll-FAQ"),
            ("/guides/", "Ratgeber"),
            ("/guides/shipping/", "Versand"),
        ],
    },
    "us": {
        "host": "cssbuyspreadsheets.us",
        "lang": "en-US",
        "locale": "United States",
        "loc": "en",
        "dest": "US",
        "dest_label": "the United States",
        "ccy": "USD",
        "keep": [
            ("/spreadsheet/", "Spreadsheet"),
            ("/faq/", "FAQ"),
            ("/guides/", "Guides"),
            ("/guides/shipping/", "Shipping"),
        ],
    },
    "eu": {
        "host": "cssbuyspreadsheet.eu",
        "lang": "en",
        "locale": "European Union",
        "loc": "en",
        "dest": None,
        "dest_label": "a country in the estimator",
        "ccy": "EUR",
        "keep": [
            ("/spreadsheet/", "Spreadsheet"),
            ("/faq/", "FAQ"),
            ("/guides/", "Guides"),
            ("/guides/shipping/", "Shipping"),
        ],
    },
}

TWINS = {
    "cssbuyspreadsheet.es": "cssbuy.es",
    "cssbuyspreadsheet.fr": "cssbuy.fr",
    "cssbuyspreadsheet.it": "cssbuy.it",
    "cssbuyspreadsheet.nl": "cssbuy.nl",
}

TWIN_PATH_MAP = [
    ("/guides/customs", "/guide/customs"),
    ("/guides/costs", "/guide/costs"),
    ("/guides/payment", "/guide/payment"),
    ("/guides/tracking", "/guide/tracking"),
    ("/guides/coupon", "/guide/coupon"),
    ("/guides/is-safe", "/guide/is-safe"),
    ("/guides/first-order", "/guide/first-order"),
    ("/guides/vs-pandabuy", "/guide/vs-pandabuy"),
]

LOCAL_CSS = SKIP_CSS + f"""
.dest-local-wrap{{background:#fff8f3;border-top:1px solid #f3d5c4;border-bottom:1px solid #f3d5c4}}
.sg-sec{{margin:0;padding:8px 0 12px}}
.sg-sec h2{{font-size:clamp(22px,3vw,30px);font-weight:700;letter-spacing:-.4px;margin:0 0 8px;color:#1a1a1a}}
.sg-sec .ssub{{color:#555;margin:0 0 12px;font-size:15px;line-height:1.65}}
.sg-sec a{{color:{BRAND}}}
.local-steps li{{border-color:#f3d5c4}}
"""

ESTIMATOR_NOTE = {
    "at": "Schätzer-Land ist AT mit vierstelliger PLZ, nicht die TLD .at, nicht DE, nicht „EU“.",
    "es": "El país del estimador es ES, no este TLD, no EU.",
    "fr": "Le pays de l’estimateur est FR, pas ce TLD, pas BE, pas EU.",
    "it": "Il paese dell’estimator è IT, non questo TLD, non EU.",
    "nl": "Estimator-land is NL, niet deze TLD, niet EU.",
    "ca": "Estimator country is CA, not this TLD, not a US ZIP.",
    "uk": "Estimator country is GB, not this TLD, not EU.",
    "de": "Schätzer-Land ist DE, nicht diese TLD, nicht AT, nicht „EU“.",
    "us": "Estimator country is US, not this TLD, not EU.",
    "eu": "This hostname is not a customs territory. Open the estimator with a real country, not .eu.",
}

STORAGE_NOTE = {
    "de": "Lager: 90 freie Tage ab In Warehouse (offizielle CSSBuy-FAQ), danach ¥15/Bestellung/Monat. Am Versandmorgen in Help prüfen.",
    "es": "Almacén: 90 días gratis desde In Warehouse (FAQ oficial CSSBuy), luego ¥15/pedido/mes. Confirma Help el día del envío.",
    "fr": "Entrepôt : 90 jours gratuits dès In Warehouse (FAQ officielle CSSBuy), puis ¥15/commande/mois. Vérifier Help le matin de l’envoi.",
    "it": "Magazzino: 90 giorni gratis da In Warehouse (FAQ ufficiale CSSBuy), poi ¥15/ordine/mese. Conferma Help il giorno della spedizione.",
    "nl": "Magazijn: 90 gratis dagen vanaf In Warehouse (officiële CSSBuy-FAQ), daarna ¥15/order/maand. Check Help op de verzenddag.",
    "en": "Warehouse: 90 free days from In Warehouse (official CSSBuy FAQ), then ¥15/order/month. Confirm Help the morning you ship.",
}


def _facts(spec: dict) -> dict:
    return {
        "agent": "CSSBuy",
        "host": spec["host"],
        "lang": spec["lang"],
        "loc": spec["loc"],
        "dest": spec.get("dest"),
        "dest_label": spec.get("dest_label") or "a country in the estimator",
        "ccy": spec["ccy"],
        "storage": STORAGE,
        "estimator": EST,
        "official": OFFICIAL,
        "date": DATE,
        "email": f"support@{spec['host']}",
        "keep": spec.get("keep") or [],
        "codes_off_title": [INVITE],
        "strict_html_codes": False,
    }


def _local_block(key: str, spec: dict) -> str:
    facts = _facts(spec)
    loc = spec["loc"]
    pack = dest_local_pack(facts.get("dest"))
    fp = pack["fingerprint"]
    store = STORAGE_NOTE.get(loc) or STORAGE_NOTE["en"]
    extra = (
        f'<p class="local-src">{escape(fp)}. {escape(ESTIMATOR_NOTE[key])} {escape(store)} '
        f'Live money: <a href="{escape(EST)}">{escape(EST)}</a> — this HTML is not checkout.</p>'
    )
    html = local_guide_html(facts).strip()
    if not html.endswith("</section>"):
        raise RuntimeError(f"{key}: local_guide_html missing section")
    html = html[: -len("</section>")] + extra + "\n</section>"
    err: list[str] = []
    _check_local_section(html, facts, err)
    if err:
        raise RuntimeError(f"{key} #local: {'; '.join(err)}")
    if INVITE in html:
        raise RuntimeError(f"{key} #local leaked invite")
    return html


def extra_faqs(key: str, spec: dict) -> list[dict]:
    facts = _facts(spec)
    pack = dest_local_pack(facts.get("dest"))
    dest = facts["dest_label"]
    host = facts["host"]
    est_note = ESTIMATOR_NOTE[key]
    store = STORAGE_NOTE.get(spec["loc"]) or STORAGE_NOTE["en"]
    loc = spec["loc"]
    table = {
        "de": [
            (f"Welches Land im CSSBuy-Schätzer für {host}?",
             f"{est_note} Der Schätzer braucht einen Ländercode, nicht diesen Hostnamen. {pack['duty']}"),
            ("Wer zahlt Einfuhr auf diese Adresse?",
             f"{pack['duty']} {pack['threshold']}"),
            ("Wie lange lagert CSSBuy?",
             f"{store} Diese Zahl kommt aus der offiziellen Warehouse-FAQ, nicht aus einem Discord-Screenshot."),
            ("Ist das die offizielle CSSBuy-Kasse?",
             f"Nein. {host} ist ein Infodesk für {dest}. Bestellung, Zahlung und Reklamation nur auf cssbuy.com. Schwester-Länderhosts bleiben eigene Dateien — kein 301."),
        ],
        "es": [
            (f"¿Qué país pongo en el estimador de CSSBuy en {host}?",
             f"{est_note} El formulario oficial pide un país, no este hostname. {pack['duty']}"),
            ("¿Quién paga aranceles a esta dirección?",
             f"{pack['duty']} {pack['threshold']}"),
            ("¿Cuánto tiempo guarda CSSBuy el paquete?",
             f"{store} La cifra sale de la FAQ oficial de almacén, no de un recuento de líneas ajeno."),
            ("¿Esta página cobra el flete?",
             f"No. {host} es un desk informativo para {dest}. Pedidos y pagos solo en cssbuy.com. Los hosts hermanos siguen en archivos separados — sin 301."),
        ],
        "fr": [
            (f"Quel pays dans l’estimateur CSSBuy sur {host} ?",
             f"{est_note} Le formulaire officiel veut un code pays, pas ce nom d’hôte. {pack['duty']}"),
            ("Qui paie les droits vers cette adresse ?",
             f"{pack['duty']} {pack['threshold']}"),
            ("Combien de temps CSSBuy stocke-t-il ?",
             f"{store} Le chiffre vient de la FAQ entrepôt officielle, pas d’un dossier Belgique."),
            ("Cette page encaisse-t-elle le fret ?",
             f"Non. {host} est un desk d’information pour {dest}. Commandes et paiements uniquement sur cssbuy.com. Les hôtes sœurs restent des fichiers séparés — pas de 301."),
        ],
        "it": [
            (f"Quale paese nell’estimator CSSBuy su {host}?",
             f"{est_note} Il modulo ufficiale vuole un codice paese, non questo hostname. {pack['duty']}"),
            ("Chi paga i dazi verso questo indirizzo?",
             f"{pack['duty']} {pack['threshold']}"),
            ("Quanto tiene CSSBuy in magazzino?",
             f"{store} Il numero viene dalla FAQ magazzino ufficiale."),
            ("Questa pagina incassa il nolo?",
             f"No. {host} è un desk informativo per {dest}. Ordini e pagamenti solo su cssbuy.com. Gli host fratelli restano file separati — niente 301."),
        ],
        "nl": [
            (f"Welk land in de CSSBuy-estimator op {host}?",
             f"{est_note} Het officiële formulier wil een landcode, niet deze hostname. {pack['duty']}"),
            ("Wie betaalt invoer naar dit adres?",
             f"{pack['duty']} {pack['threshold']}"),
            ("Hoe lang slaat CSSBuy op?",
             f"{store} Het getal komt uit de officiële warehouse-FAQ."),
            ("Is dit de kassa?",
             f"Nee. {host} is een infodesk voor {dest}. Bestellen en betalen alleen op cssbuy.com. Zushosts blijven aparte bestanden — geen 301."),
        ],
        "en": [
            (f"Which country in the CSSBuy estimator on {host}?",
             f"{est_note} The official form wants a country code, not this hostname. {pack['duty']}"),
            ("Who pays import charges to this address?",
             f"{pack['duty']} {pack['threshold']}"),
            ("How long does CSSBuy store a parcel?",
             f"{store} That number is from the official warehouse FAQ, not a Discord screenshot."),
            ("Does this page take payment?",
             f"No. {host} is an information desk for {dest}. Orders and payment stay on cssbuy.com. Sister country hosts stay separate files — no 301."),
        ],
    }
    rows = table.get(loc) or table["en"]
    return [{"q": q, "a": a} for q, a in rows]


def _php_escape(s: str) -> str:
    return s.replace("\\", "\\\\").replace("'", "\\'")


def dest_local_php() -> str:
    faq_map = {k: extra_faqs(k, spec) for k, spec in PHP_HOSTS.items()}
    cta_map = {k: local_cta(_facts(spec)) for k, spec in PHP_HOSTS.items()}
    skip_map = {k: skip_label(spec["loc"]) for k, spec in PHP_HOSTS.items()}
    host_map = {spec["host"]: k for k, spec in PHP_HOSTS.items()}
    php = """<?php

namespace App\\Services;

/**
 * Dest-unique #local briefing keyed by HTTP_HOST.
 * Generated — do not hand-edit fingerprints.
 */
class DestLocal
{
    public static function key(?string $host = null): ?string
    {
        $host = $host ?? ($GLOBALS['domain_host'] ?? '');
        $map = __HOST_MAP__;
        return $map[$host] ?? null;
    }

    public static function html(): string
    {
        $key = self::key();
        if (!$key) {
            return '';
        }
        $path = BASE_PATH . '/resources/views/partials/dest-local-' . $key . '.php';
        if (!is_file($path)) {
            return '';
        }
        ob_start();
        include $path;
        $inner = ob_get_clean();
        if ($inner === '') {
            return '';
        }
        return '<section class="lite-section dest-local-wrap"><div class="container">'
            . $inner
            . '</div></section>';
    }

    public static function css(): string
    {
        return __CSS__;
    }

    public static function cta(): string
    {
        $key = self::key();
        $map = __CTA_MAP__;
        return $map[$key] ?? '';
    }

    public static function skipLabel(): string
    {
        $key = self::key();
        $map = __SKIP_MAP__;
        $lang = $GLOBALS['locale'] ?? 'en';
        if ($key && isset($map[$key])) {
            return $map[$key];
        }
        $fallback = ['de' => 'Zum Inhalt', 'es' => 'Saltar al contenido', 'fr' => 'Aller au contenu', 'it' => 'Vai al contenuto', 'nl' => 'Naar de inhoud'];
        return $fallback[$lang] ?? 'Skip to content';
    }

    public static function faqs(): array
    {
        $key = self::key();
        $all = json_decode(__FAQ_JSON__, true);
        if (!$key || !is_array($all) || empty($all[$key])) {
            return [];
        }
        return $all[$key];
    }
}
"""
    return (
        php.replace("__HOST_MAP__", php_assoc(host_map))
        .replace("__CSS__", php_str(LOCAL_CSS))
        .replace("__CTA_MAP__", php_assoc(cta_map))
        .replace("__SKIP_MAP__", php_assoc(skip_map))
        .replace("__FAQ_JSON__", php_str(json.dumps(faq_map, ensure_ascii=False)))
    )


def php_str(s: str) -> str:
    return "'" + _php_escape(s) + "'"


def php_assoc(d: dict) -> str:
    parts = []
    for k, v in d.items():
        parts.append(f"{php_str(k)} => {php_str(v)}")
    return "[" + ", ".join(parts) + "]"


def patch_home_php(src: str) -> str:
    needle = """</section>

<section class="lite-section">
  <div class="container">
    <div class="section-head"><h2><?= __t('featured_title') ?></h2></div>
"""
    insert = """</section>

<?= class_exists(\\App\\Services\\DestLocal::class) ? \\App\\Services\\DestLocal::html() : '' ?>

<section class="lite-section">
  <div class="container">
    <div class="section-head"><h2><?= __t('featured_title') ?></h2></div>
"""
    if needle not in src:
        raise RuntimeError("home.php hero/featured marker missing")
    if "DestLocal::html" in src:
        return src
    return src.replace(needle, insert, 1)


def patch_layout_php(src: str) -> str:
    if "dest-local-css" not in src:
        css_block = """<?php if (class_exists(\\App\\Services\\DestLocal::class)): ?>
<style id="dest-local-css"><?= \\App\\Services\\DestLocal::css() ?></style>
<?php endif; ?>
</head>
"""
        if "</head>" not in src:
            raise RuntimeError("layout missing </head>")
        src = src.replace("</head>", css_block, 1)
    if 'href="#main"' not in src:
        body = (
            '<body class="tpl-<?= $tpl ?>" data-currency="<?= e($c[\'currency\'][\'code\']) ?>" '
            'data-rate="<?= e((string)$c[\'currency\'][\'rate\']) ?>">'
        )
        skip_html = (
            '<a class="skip" href="#main">'
            "<?= class_exists(\\App\\Services\\DestLocal::class) ? \\App\\Services\\DestLocal::skipLabel() : 'Skip to content' ?>"
            "</a>"
        )
        if body not in src:
            raise RuntimeError("layout body tag mismatch")
        src = src.replace(body, body + "\n" + skip_html, 1)
    if 'href="/#local"' not in src:
        src = src.replace(
            '<a href="/"><?= __t(\'nav_home\') ?></a>',
            '<a href="/"><?= __t(\'nav_home\') ?></a>\n      <?php if (class_exists(\\App\\Services\\DestLocal::class) && \\App\\Services\\DestLocal::cta()): ?>\n      <a href="/#local"><?= e(\\App\\Services\\DestLocal::cta()) ?></a>\n      <?php endif; ?>',
            1,
        )
    src = src.replace("<main><?= $content ?? '' ?></main>", '<main id="main"><?= $content ?? \'\' ?></main>', 1)
    return src


def patch_home_controller(src: str) -> str:
    if "DestLocal::faqs" in src:
        return src
    needle = """        $faqs = $this->faqs($config);

        $faqSchema = ["""
    insert = """        $faqs = $this->faqs($config);
        if (class_exists(\\App\\Services\\DestLocal::class)) {
            $faqs = array_merge($faqs, \\App\\Services\\DestLocal::faqs());
        }

        $faqSchema = ["""
    if needle not in src:
        raise RuntimeError("HomeController faqs marker missing")
    return src.replace(needle, insert, 1)


def patch_static_home(html: str, key: str, spec: dict) -> str:
    facts = _facts(spec)
    block = _local_block(key, spec)
    loc = spec["loc"]
    if 'class="skip"' not in html:
        html = html.replace("<body>", "<body>\n" + skip_link(skip_label(loc)).rstrip(), 1)
    if 'id="main"' not in html:
        html = html.replace("<main>", '<main id="main">', 1)
    if "#local{scroll-margin-top" not in html:
        html = html.replace("</style>", SKIP_CSS + "\n</style>", 1)
    if 'id="local"' in html:
        html = re.sub(
            r'<section class="sg-sec" id="local".*?</section>',
            block,
            html,
            count=1,
            flags=re.S,
        )
    else:
        html = re.sub(r"(<h1>.*?</h1>)", r"\1\n" + block, html, count=1, flags=re.S)
    err: list[str] = []
    _check_local_section(html, facts, err)
    title_m = re.search(r"<title>(.*?)</title>", html, flags=re.S)
    title = title_m.group(1) if title_m else ""
    if INVITE in title:
        err.append("invite in title")
    for pat in (
        r"58 l[ií]neas para Espa",
        r"23[,.]81\s*USD",
        r"how to under-?declar",
        r"c[oó]mo infradeclar",
        r"comment sous-d[eé]clar",
        r"wie unterdeklar",
    ):
        if re.search(pat, html, flags=re.I):
            err.append(f"forbidden {pat}")
    if err:
        raise RuntimeError(f"{key} static: {'; '.join(err)}")
    if key == "eu" and "not a customs territory" not in html:
        raise RuntimeError("eu missing hub fingerprint")
    if key == "fr" and re.search(r"Belgique|Belgium", title):
        raise RuntimeError("fr title became Belgium")
    return html


def generate() -> None:
    PHP_OUT.mkdir(parents=True, exist_ok=True)
    partials = PHP_OUT / "overlay" / "resources" / "views" / "partials"
    partials.mkdir(parents=True, exist_ok=True)
    services = PHP_OUT / "overlay" / "app" / "Services"
    services.mkdir(parents=True, exist_ok=True)
    views = PHP_OUT / "overlay" / "resources" / "views"
    layouts = views / "layouts"
    layouts.mkdir(parents=True, exist_ok=True)
    controllers = PHP_OUT / "overlay" / "app" / "Http" / "Controllers"
    controllers.mkdir(parents=True, exist_ok=True)

    (services / "DestLocal.php").write_text(dest_local_php(), encoding="utf-8")
    for key, spec in PHP_HOSTS.items():
        html = _local_block(key, spec)
        (partials / f"dest-local-{key}.php").write_text(html + "\n", encoding="utf-8")
        print("partial", key, "bytes", len(html))

    home = patch_home_php((LIVE_PHP / "home.php").read_text(encoding="utf-8"))
    layout = patch_layout_php((LIVE_PHP / "layouts_app.php").read_text(encoding="utf-8"))
    ctrl = patch_home_controller((LIVE_PHP / "HomeController.php").read_text(encoding="utf-8"))
    (views / "home.php").write_text(home, encoding="utf-8")
    (layouts / "app.php").write_text(layout, encoding="utf-8")
    (controllers / "HomeController.php").write_text(ctrl, encoding="utf-8")

    if "DestLocal::html" not in home:
        raise RuntimeError("patched home.php missing DestLocal")
    if 'id="main"' not in layout:
        raise RuntimeError("patched layout missing #main")
    if "DestLocal::faqs" not in ctrl:
        raise RuntimeError("patched controller missing dest FAQs")

    for key, spec in STATIC_HOSTS.items():
        src = OUT / spec["host"] / "live-base" / "index.html"
        if not src.is_file():
            raise SystemExit(f"missing live-base {src}")
        html = patch_static_home(src.read_text(encoding="utf-8"), key, spec)
        dest = OUT / spec["host"] / "overlay" / "index.html"
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(html, encoding="utf-8")
        print("static", key, spec["host"], "bytes", len(html))

    # Gate 1 across PHP fragments: no sister leak, fingerprints unique.
    blobs = {}
    for key, spec in PHP_HOSTS.items():
        text = (partials / f"dest-local-{key}.php").read_text(encoding="utf-8")
        blobs[key] = (spec, text)
    for key, spec in STATIC_HOSTS.items():
        text = (OUT / spec["host"] / "overlay" / "index.html").read_text(encoding="utf-8")
        inner_m = re.search(r'<section class="sg-sec" id="local".*?</section>', text, flags=re.S)
        blobs[key] = (spec, inner_m.group(0) if inner_m else "")
    fps = {k: dest_local_pack(spec.get("dest"))["fingerprint"] for k, (spec, _) in blobs.items()}
    for key, (spec, inner) in blobs.items():
        fp = fps[key]
        if fp not in inner:
            raise SystemExit(f"{key} missing fingerprint {fp!r}")
        for other, ofp in fps.items():
            if other == key:
                continue
            if ofp in inner:
                raise SystemExit(f"{key} #local leaked {other} fingerprint {ofp!r}")
        if INVITE in inner:
            raise SystemExit(f"{key} invite in #local")
    print("generate ok", len(blobs), "desks")


def _connect():
    try:
        import paramiko
    except ImportError:
        import subprocess

        subprocess.check_call([sys.executable, "-m", "pip", "install", "paramiko", "-q"])
        import paramiko

    password = os.environ.get("ORIGIN_SSH_PASS")
    if not password:
        raise SystemExit("Set ORIGIN_SSH_PASS")
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect("31.97.41.31", username="root", password=password, timeout=30)
    return client


def _run(client, cmd: str, timeout: int = 90) -> str:
    _, stdout, stderr = client.exec_command(cmd, timeout=timeout)
    return (stdout.read() + stderr.read()).decode(errors="replace").strip()


def _put_file(sftp, local: Path, remote: str) -> None:
    sftp.put(str(local), remote)
    print("PUT", remote, "bytes", local.stat().st_size)


def put() -> None:
    generate()
    client = _connect()
    stamp = time.strftime("%Y%m%d-%H%M%S")
    bak = f"/www/backup/cssbuy-desks-{stamp}"
    php_files = [
        ("overlay/app/Services/DestLocal.php", "/www/wwwroot/cssbuy-lite/app/Services/DestLocal.php"),
        ("overlay/resources/views/home.php", "/www/wwwroot/cssbuy-lite/resources/views/home.php"),
        ("overlay/resources/views/layouts/app.php", "/www/wwwroot/cssbuy-lite/resources/views/layouts/app.php"),
        ("overlay/app/Http/Controllers/HomeController.php", "/www/wwwroot/cssbuy-lite/app/Http/Controllers/HomeController.php"),
    ]
    for key in PHP_HOSTS:
        php_files.append(
            (
                f"overlay/resources/views/partials/dest-local-{key}.php",
                f"/www/wwwroot/cssbuy-lite/resources/views/partials/dest-local-{key}.php",
            )
        )
    # Gate 6: never touch public/index.php or unused ccTLD stubs.
    backup_cmd = (
        f"mkdir -p '{bak}/php' '{bak}/static' && "
        f"cp -a /www/wwwroot/cssbuy-lite/resources/views/home.php "
        f"/www/wwwroot/cssbuy-lite/resources/views/layouts/app.php "
        f"/www/wwwroot/cssbuy-lite/app/Http/Controllers/HomeController.php "
        f"'{bak}/php/' && "
        f"mkdir -p '{bak}/php/partials' '{bak}/php/Services'"
    )
    print(_run(client, backup_cmd))
    sftp = client.open_sftp()
    _run(client, "mkdir -p /www/wwwroot/cssbuy-lite/resources/views/partials /www/wwwroot/cssbuy-lite/app/Services")
    for rel, remote in php_files:
        local = PHP_OUT / rel
        if not local.is_file():
            raise SystemExit(f"missing {local}")
        # Refuse accidental public overwrite.
        if "/public/" in remote or remote.endswith("/cssbuy-lite/public/index.php"):
            raise SystemExit(f"refusing to PUT public gold {remote}")
        _put_file(sftp, local, remote)
    for key, spec in STATIC_HOSTS.items():
        host = spec["host"]
        local = OUT / host / "overlay" / "index.html"
        remote = f"/www/wwwroot/{host}/index.html"
        _run(client, f"cp -a '{remote}' '{bak}/static/{host}.index.html'")
        _put_file(sftp, local, remote)
    sftp.close()
    _run(
        client,
        "chown -R www:www /www/wwwroot/cssbuy-lite/app/Services/DestLocal.php "
        "/www/wwwroot/cssbuy-lite/resources/views/partials "
        "/www/wwwroot/cssbuy-lite/resources/views/home.php "
        "/www/wwwroot/cssbuy-lite/resources/views/layouts/app.php "
        "/www/wwwroot/cssbuy-lite/app/Http/Controllers/HomeController.php",
    )
    patch_twins(client)
    print("backup", bak)
    client.close()


def patch_twins(client) -> None:
    """Add ranked-path maps so twins 301 onto real PHP routes, not only /."""
    changed = 0
    for twin, target in TWINS.items():
        path = f"/www/server/panel/vhost/nginx/{twin}.conf"
        raw = _run(client, f"cat '{path}'")
        if not raw:
            print("skip missing nginx", twin)
            continue
        extra = []
        for src, dest in TWIN_PATH_MAP:
            loc = f"    location = {src} {{ return 301 https://{target}{dest}; }}"
            loc_slash = f"    location = {src}/ {{ return 301 https://{target}{dest}; }}"
            if f"location = {src} " in raw or f"location = {src}{{" in raw:
                continue
            extra.append(loc)
            extra.append(loc_slash)
        # Prefer /#faq over collapsing FAQ onto /.
        if "location = /faq " in raw and f"https://{target}/;" in raw:
            raw2 = raw.replace(
                f"    location = /faq {{ return 301 https://{target}/; }}",
                f"    location = /faq {{ return 301 https://{target}/#faq; }}",
                1,
            )
            raw2 = raw2.replace(
                f"    location = /faq/ {{ return 301 https://{target}/; }}",
                f"    location = /faq/ {{ return 301 https://{target}/#faq; }}",
                1,
            )
            raw = raw2
        if extra:
            marker = "    location / { return 301"
            block = "\n".join(extra) + "\n" + marker
            if marker not in raw:
                print("skip", twin, "no catch-all marker")
                continue
            raw = raw.replace(marker, block, 1)
        bak = f"/www/backup/cssbuy-twin-{twin}.conf"
        _run(client, f"cp -a '{path}' '{bak}'")
        sftp = client.open_sftp()
        with sftp.open(path, "w") as fh:
            fh.write(raw)
        sftp.close()
        changed += 1
        print("PATCH nginx", twin, "extra", len(extra) // 2)
    if changed:
        print(_run(client, "nginx -t && nginx -s reload"))


def live_check() -> None:
    import urllib.request

    pairs = [
        ("at", "https://cssbuy.at/", "1010 Wien", ("Packstation", "Colissimo", "Poste Italiane")),
        ("es", "https://cssbuy.es/", "no copiamos un recuento de líneas", ("Packstation", "1010 Wien", "pas un code postal belge")),
        ("fr", "https://cssbuy.fr/", "pas un code postal belge", ("Packstation", "1010 Wien", "Poste Italiane")),
        ("it", "https://cssbuy.it/", "Poste Italiane", ("Packstation", "1010 Wien", "pas un code postal belge")),
        ("nl", "https://cssbuy.nl/", "Nederlandse postcode", ("Packstation", "1010 Wien", "Poste Italiane")),
        ("ca", "https://cssbuyspreadsheet.ca/", "form A1A 1A1", ("Packstation", "Poste Italiane", "1010 Wien")),
        ("uk", "https://cssbuyspreadsheet.uk/", "Northern Ireland is often another", ("Packstation", "1010 Wien", "Poste Italiane")),
        ("de", "https://cssbuyspreadsheets.de/", "Packstation", ("1010 Wien", "form A1A 1A1", "Poste Italiane")),
        ("us", "https://cssbuyspreadsheets.us/", "does not invent a de-minimis dollar", ("Packstation", "form A1A 1A1", "1010 Wien")),
        ("eu", "https://cssbuyspreadsheet.eu/", "not a customs territory", ("1010 Wien", "Packstation", "form A1A 1A1")),
    ]
    ctx_headers = {"User-Agent": "cssbuy-desk-check/1.0"}

    def fetch(url: str, follow: bool = True) -> tuple[int, str, str, bytes]:
        req = urllib.request.Request(url, headers=ctx_headers)
        opener = urllib.request.build_opener(
            urllib.request.HTTPRedirectHandler() if follow else urllib.request.HTTPHandler()
        )
        # Manual for Location
        class NoRedirect(urllib.request.HTTPRedirectHandler):
            def redirect_request(self, req, fp, code, msg, headers, newurl):
                return None

        if not follow:
            opener = urllib.request.build_opener(NoRedirect)
        try:
            with opener.open(req, timeout=25) as resp:
                body = resp.read()
                return resp.status, resp.geturl(), resp.headers.get("Location") or "", body
        except urllib.error.HTTPError as e:
            loc = e.headers.get("Location") or ""
            body = e.read() if e.fp else b""
            return e.code, url, loc, body

    fail = 0
    for key, url, fp, aliens in pairs:
        code, final, loc, body = fetch(url, follow=True)
        html = body.decode("utf-8", "replace")
        title_m = re.search(r"<title>(.*?)</title>", html, flags=re.S)
        title = title_m.group(1) if title_m else ""
        inner_m = re.search(r'<section class="sg-sec" id="local".*?</section>', html, flags=re.S)
        inner = inner_m.group(0) if inner_m else ""
        print(f"{key:3} {code} bytes={len(body)} local={bool(inner)} fp={fp in html}")
        if code != 200:
            print("  FAIL status", code)
            fail += 1
            continue
        if not inner:
            print("  FAIL missing #local")
            fail += 1
            continue
        if fp not in inner:
            print("  FAIL missing dest fingerprint")
            fail += 1
        for alien in aliens:
            if alien in inner:
                print("  FAIL sister leak", alien)
                fail += 1
        if INVITE in title:
            print("  FAIL invite in title")
            fail += 1
        if re.search(r"23[,.]81\\s*USD|58 l[ií]neas para Espa", html, flags=re.I):
            print("  FAIL Spain gold snapshot")
            fail += 1
        if key in PHP_HOSTS and len(body) < 8000:
            print("  FAIL PHP gold collapsed to thin template", len(body))
            fail += 1
        if key == "eu" and "not a customs territory" not in inner:
            print("  FAIL eu hub fingerprint")
            fail += 1
        if key in PHP_HOSTS and "cssbuy-lite" not in html and 'class="lite-hero"' not in html:
            print("  FAIL PHP chrome gone")
            fail += 1

    # Gate 4: sister country URLs independent (no 301).
    for a, b in (
        ("https://cssbuy.fr/", "https://cssbuy.es/"),
        ("https://cssbuy.at/", "https://cssbuy.nl/"),
        ("https://cssbuy.it/", "https://cssbuy.fr/"),
        ("https://cssbuyspreadsheet.ca/", "https://cssbuyspreadsheets.us/"),
        ("https://cssbuyspreadsheet.uk/", "https://cssbuy.fr/"),
        ("https://cssbuyspreadsheet.eu/", "https://cssbuy.nl/"),
    ):
        code, final, loc, _ = fetch(a, follow=False)
        if code in (301, 302, 303, 307, 308) and loc:
            print("FAIL 301", a, "->", loc)
            fail += 1
        else:
            print("indep", a, code)

    # Gate 5: twins 301 to target that now has #local; a mapped path is not 404.
    for twin, target in TWINS.items():
        code, final, loc, _ = fetch(f"https://{twin}/", follow=False)
        print("twin", twin, code, loc)
        if code not in (301, 302, 308) or target not in (loc or ""):
            print("  FAIL twin 301")
            fail += 1
        code2, _, loc2, body2 = fetch(f"https://{twin}/guides/shipping", follow=True)
        html2 = body2.decode("utf-8", "replace")
        if code2 == 404:
            print("  FAIL deep path 404", twin)
            fail += 1
        else:
            print("  deep", twin, code2, "bytes", len(body2), "404", code2 == 404)

    if fail:
        raise SystemExit(f"live_check failures: {fail}")
    print("live_check ok")


def main() -> None:
    if "--put" in sys.argv:
        put()
        return
    if "--check" in sys.argv:
        live_check()
        return
    generate()


if __name__ == "__main__":
    main()
