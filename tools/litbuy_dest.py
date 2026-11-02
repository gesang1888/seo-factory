#!/usr/bin/env python3
"""Deepen LitBuy dest desks to UK-cluster inner depth.

Live dests: litbuy.at / litbuyspreadsheet.it / litbuyspreadsheets.ca.
Reclaim US/UK/FR/ES/NL from hub 301. Unique hub litbuyspreadsheet.eu
Independent Index is not PUT. Hub twin litbuyspreadsheetnow.com stays
301 to .eu. Skip ch/be/pt (no vhost). Unique coupons/legit/Zoll/CBSA
CMS are not smashed. Invite O4K87NHKR off dest titles. Register on
https://litbuy.com/register ; estimator https://litbuy.com/shipping-estimate.
GSC: sitemap submit only. No declared-value coaching.
"""
from __future__ import annotations

import json
import os
import re
import shutil
import sys
import time
from html import escape
from pathlib import Path

_TOOLS = Path(__file__).resolve().parent
if str(_TOOLS) not in sys.path:
    sys.path.insert(0, str(_TOOLS))
from desk_template import cluster_keywords, cluster_title, faq_ld, inject_jsonld, website_ld
from litbuy_dest_copy import inner_h1, inner_keywords, inner_serp_title, sections_for, wrap_copy
import litbuy_dest_skin as cbskin

ROOT = Path(__file__).resolve().parents[1]
STAMP = "20261102"
TODAY = "2026-11-02"
MARKER = f'data-litbuy-dest="{STAMP}"'
_SA_CANDIDATES = [
    os.environ.get("GSC_SA_JSON", ""),
    "/tmp/hipobuy-creds/sa.json",
    "/cursor/stores/self/internal/gsc-sa.json",
]
SA = next((p for p in _SA_CANDIDATES if p and Path(p).is_file()), "/tmp/hipobuy-creds/sa.json")
BAK_B = "/www/backup/portfolio-step5-phaseb-20261026-150339"
BAK_C = "/www/backup/portfolio-step5-phasec-20261026-151213"
A = "LitBuy"
W2C_SHEET = "https://w2clinks.com/spreadsheet/litbuy/"

PRODUCTS_PHP = r"""<?php
declare(strict_types=1);

header('Content-Type: application/json; charset=utf-8');
header('Access-Control-Allow-Origin: *');

$upstream = 'https://w2clinks.com/public/typesense-search.php';
$page = max(1, (int)($_GET['page'] ?? 1));
$perPage = max(1, min(48, (int)($_GET['per_page'] ?? $_GET['limit'] ?? 24)));
$sort = preg_replace('/[^a-z0-9_-]/i', '', (string)($_GET['sort'] ?? 'newest')) ?: 'newest';
$q = trim((string)($_GET['q'] ?? $_GET['keyword'] ?? ''));
$category = trim((string)($_GET['category'] ?? ''));
$brand = trim((string)($_GET['brand'] ?? ''));
$typeid = trim((string)($_GET['typeid'] ?? ''));

header('Cache-Control: public, max-age=' . ($q !== '' || $category !== '' || $brand !== '' ? 60 : 300));

function w2c_api_key(): string
{
    foreach (['W2CLINKS_API_KEY', 'W2C_PRODUCTS_API_KEY'] as $name) {
        $env = getenv($name);
        if (is_string($env) && $env !== '') {
            return $env;
        }
    }
    $local = __DIR__ . '/config.local.php';
    if (is_file($local)) {
        $cfg = include $local;
        if (is_array($cfg) && !empty($cfg['api_key'])) {
            return (string) $cfg['api_key'];
        }
    }
    return '';
}

$params = [
    'page' => $page,
    'per_page' => $perPage,
    'sort' => $sort,
];
if ($q !== '') {
    $params['q'] = $q;
}
if ($category !== '') {
    $params['category'] = $category;
}
if ($brand !== '') {
    $params['brand'] = $brand;
}
if ($typeid !== '' && ctype_digit($typeid)) {
    $params['typeid'] = $typeid;
}

$apiKey = w2c_api_key();
if ($apiKey !== '') {
    $params['api_key'] = $apiKey;
}

$url = $upstream . '?' . http_build_query($params);

$headers = [
    'Accept: application/json',
    'User-Agent: LitBuySpreadsheetProxy/1.1',
];
if ($apiKey !== '') {
    $headers[] = 'Authorization: Bearer ' . $apiKey;
    $headers[] = 'X-API-Key: ' . $apiKey;
    $headers[] = 'X-TYPESENSE-API-KEY: ' . $apiKey;
}

$ch = curl_init($url);
curl_setopt_array($ch, [
    CURLOPT_RETURNTRANSFER => true,
    CURLOPT_FOLLOWLOCATION => true,
    CURLOPT_CONNECTTIMEOUT => 8,
    CURLOPT_TIMEOUT => 15,
    CURLOPT_HTTPHEADER => $headers,
]);
$body = curl_exec($ch);
$code = (int) curl_getinfo($ch, CURLINFO_RESPONSE_CODE);
curl_close($ch);

if ($body === false || $code < 200 || $code >= 300) {
    http_response_code(502);
    echo json_encode(['ok' => false, 'hits' => [], 'found' => 0, 'items' => []]);
    exit;
}
echo $body;
"""

PRODUCTS_INDEX = r"""<?php
declare(strict_types=1);
$_GET['per_page'] = (string) max(1, min(48, (int) ($_GET['limit'] ?? $_GET['per_page'] ?? 24)));
$upstream = dirname(__DIR__) . '/products.php';
if (!is_file($upstream)) {
    header('Content-Type: application/json; charset=utf-8');
    http_response_code(502);
    echo json_encode(['ok' => false, 'items' => []]);
    exit;
}
ob_start();
require $upstream;
$raw = ob_get_clean();
$data = json_decode((string) $raw, true);
if (!is_array($data)) {
    header('Content-Type: application/json; charset=utf-8');
    http_response_code(502);
    echo json_encode(['ok' => false, 'items' => []]);
    exit;
}
$sheet = 'https://w2clinks.com/spreadsheet/litbuy/';
$base = 'https://w2clinks.com';
$items = [];
foreach (($data['hits'] ?? $data['items'] ?? []) as $h) {
    if (!is_array($h)) {
        continue;
    }
    $href = (string) ($h['url'] ?? $h['href'] ?? $h['target'] ?? '');
    if ($href === '') {
        $href = $sheet;
    } elseif ($href[0] === '/') {
        $href = $base . $href;
    }
    $items[] = [
        'title' => (string) ($h['title'] ?? ''),
        'image' => (string) ($h['image'] ?? ''),
        'price' => $h['price_cny'] ?? $h['price'] ?? '',
        'currency' => (string) ($h['currency'] ?? 'CNY'),
        'href' => $href,
        'target' => $href,
    ];
}
header('Content-Type: application/json; charset=utf-8');
echo json_encode(
    [
        'ok' => true,
        'items' => $items,
        'products' => $items,
        'found' => $data['found'] ?? count($items),
        'page' => $data['page'] ?? 1,
        'spreadsheet' => $sheet,
    ],
    JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE
);
"""


def cluster_title_serp(agent: str, dest: str | None, loc: str, dest_label: str | None = None) -> str:
    if loc == "pl":
        base = f"{agent} Spreadsheet dla kupujących w Polsce"
    else:
        base = cluster_title(agent, dest, loc, dest_label)
    suffix = {
        "de": " – Beste Finds & QC",
        "nl": " – Beste finds en QC",
        "es": " – Mejores finds y QC",
        "fr": " – Meilleurs finds et QC",
        "it": " – Finds e QC",
    }.get(loc, " – Best Finds & QC")
    return base + suffix



def pages_for(host: str) -> dict[str, str]:
    if host.endswith(".at"):
        shipping, legal = "litbuy-shipping-to-osterreich", "is-litbuy-legal-osterreich"
    elif host.endswith(".it"):
        shipping, legal = "litbuy-shipping-to-italia", "is-litbuy-legal-italia"
    elif host.endswith(".ca"):
        shipping, legal = "litbuy-shipping-to-canada", "is-litbuy-legal-canada"
    elif host.endswith(".us"):
        shipping, legal = "litbuy-shipping-to-usa", "is-litbuy-legal-us"
    elif "me.uk" in host:
        shipping, legal = "litbuy-shipping-to-uk", "is-litbuy-legal-uk"
    elif host.endswith(".fr"):
        shipping, legal = "litbuy-shipping-to-france", "is-litbuy-legal-france"
    elif host.endswith(".es"):
        shipping, legal = "litbuy-shipping-to-espana", "is-litbuy-legal-espana"
    else:
        shipping, legal = "litbuy-shipping-to-nederland", "is-litbuy-legal-nederland"
    return {
        "spreadsheet": "litbuy-spreadsheet",
        "finds": "litbuy-finds",
        "qc": "litbuy-qc",
        "shipping": shipping,
        "legal": legal,
        "guide": "litbuy-guide",
        "faq": "litbuy-faq",
    }


HOSTS = {
    "litbuy.at": {
        "key": "at", "dest": "AT", "loc": "de", "lang": "de-AT", "label": "Österreich",
        "ccy": "EUR", "customs": "BMF Zoll", "customs_url": "https://www.bmf.gv.at/themen/zoll.html",
        "post": "Österreichische Post", "city": "österreichische PLZ (form 1010)",
        "pages": pages_for("litbuy.at"), "skip": set(),
        "canon": [
            ("litbuy-shipping-to-österreich", "litbuy-shipping-to-osterreich"),
            ("is-litbuy-legal-österreich", "is-litbuy-legal-osterreich"),
        ],
    },
    "litbuyspreadsheet.it": {
        "key": "it", "dest": "IT", "loc": "it", "lang": "it-IT", "label": "l’Italia",
        "ccy": "EUR", "customs": "Agenzia delle Dogane", "customs_url": "https://www.adm.gov.it/",
        "post": "Poste Italiane", "city": "CAP italiano (form 00100)",
        "pages": pages_for("litbuyspreadsheet.it"), "skip": set(), "canon": [],
    },
    "litbuyspreadsheets.ca": {
        "key": "ca", "dest": "CA", "loc": "en", "lang": "en-CA", "label": "Canada",
        "ccy": "CAD", "customs": "CBSA", "customs_url": "https://www.cbsa-asfc.gc.ca/",
        "post": "Canada Post", "city": "Canadian postal code (form A1A 1A1)",
        "pages": pages_for("litbuyspreadsheets.ca"), "skip": set(), "canon": [],
    },
    "litbuyspreadsheets.us": {
        "key": "us", "dest": "US", "loc": "en", "lang": "en-US", "label": "the United States",
        "ccy": "USD", "customs": "CBP", "customs_url": "https://www.cbp.gov/",
        "post": "USPS", "city": "US ZIP (form 10001)",
        "pages": pages_for("litbuyspreadsheets.us"), "skip": set(), "canon": [],
    },
    "litbuyspreadsheet.me.uk": {
        "key": "uk", "dest": "GB", "loc": "en", "lang": "en-GB", "label": "the United Kingdom",
        "ccy": "GBP", "customs": "HMRC", "customs_url": "https://www.gov.uk/goods-sent-from-abroad",
        "post": "Royal Mail", "city": "UK postcode (form SW1A 1AA)",
        "pages": pages_for("litbuyspreadsheet.me.uk"), "skip": set(), "canon": [],
    },
    "litspreadsheet.fr": {
        "key": "fr", "dest": "FR", "loc": "fr", "lang": "fr-FR", "label": "France",
        "ccy": "EUR", "customs": "douane FR", "customs_url": "https://www.douane.gouv.fr/",
        "post": "La Poste", "city": "code postal français (form 75001)",
        "pages": pages_for("litspreadsheet.fr"), "skip": set(), "canon": [],
    },
    "litbuyspreadsheets.es": {
        "key": "es", "dest": "ES", "loc": "es", "lang": "es-ES", "label": "España",
        "ccy": "EUR", "customs": "Agencia Tributaria", "customs_url": "https://sede.agenciatributaria.gob.es/",
        "post": "Correos", "city": "código postal español (form 28001)",
        "pages": pages_for("litbuyspreadsheets.es"), "skip": set(), "canon": [],
    },
    "litbuyspreadsheets.nl": {
        "key": "nl", "dest": "NL", "loc": "nl", "lang": "nl-NL", "label": "Nederland",
        "ccy": "EUR", "customs": "Douane", "customs_url": "https://www.belastingdienst.nl/wps/wcm/connect/bldcontentnl/belastingdienst/prive/douane/",
        "post": "PostNL", "city": "Nederlandse postcode (form 1234 AB)",
        "pages": pages_for("litbuyspreadsheets.nl"), "skip": set(), "canon": [],
    },
}

ORDER = [
    "litbuy.at",
    "litbuyspreadsheet.it",
    "litbuyspreadsheets.ca",
    "litbuyspreadsheets.us",
    "litbuyspreadsheet.me.uk",
    "litspreadsheet.fr",
    "litbuyspreadsheets.es",
    "litbuyspreadsheets.nl",
]

TWINS_KEEP: dict[str, str] = {
    "litbuyspreadsheetnow.com": "litbuyspreadsheet.eu",
}

HUB_KEEP = "litbuyspreadsheet.eu"

SKIP_HOSTS = {
    "litbuyspreadsheet.eu",
    "litbuyspreadsheetnow.com",
    "litbuy.ch",
    "litbuyspreadsheet.ch",
    "litbuyspreadsheets.be",
    "litbuy.pt",
}

LEFTOVER_SKIN = {
    "litbuy.at": ["start", "katalog", "hilfe", "neuigkeiten", "ueber-uns"],
    "litbuyspreadsheet.it": ["start", "catalogo", "aiuto", "novita", "chi-siamo"],
    "litbuyspreadsheets.ca": ["start", "catalog", "help", "news", "about"],
    "litbuyspreadsheets.us": ["start", "catalog", "help", "news", "about"],
    "litbuyspreadsheet.me.uk": ["start", "catalog", "help", "news", "about"],
    "litspreadsheet.fr": ["start", "catalogue", "aide", "actualites", "a-propos"],
    "litbuyspreadsheets.es": ["start", "catalogo", "ayuda", "novedades", "sobre-nosotros"],
    "litbuyspreadsheets.nl": ["start", "catalogus", "hulp", "nieuws", "over-ons"],
}


NAV_LAB = {
    "de": {"spreadsheet": "Spreadsheet", "finds": "Finds", "qc": "QC", "shipping": "Versand", "legal": "Legal?", "guide": "Anleitung", "faq": "FAQ"},
    "nl": {"spreadsheet": "Spreadsheet", "finds": "Finds", "qc": "QC", "shipping": "Verzending", "legal": "Legaal?", "guide": "Handleiding", "faq": "FAQ"},
    "es": {"spreadsheet": "Spreadsheet", "finds": "Finds", "qc": "QC", "shipping": "Envío", "legal": "¿Es legal?", "guide": "Guía", "faq": "FAQ"},
    "fr": {"spreadsheet": "Spreadsheet", "finds": "Finds", "qc": "QC", "shipping": "Livraison", "legal": "Légal ?", "guide": "Guide", "faq": "FAQ"},
    "it": {"spreadsheet": "Spreadsheet", "finds": "Finds", "qc": "QC", "shipping": "Spedizione", "legal": "È legale?", "guide": "Guida", "faq": "FAQ"},
    "en": {"spreadsheet": "Spreadsheet", "finds": "Finds", "qc": "QC", "shipping": "Shipping", "legal": "Is it legal?", "guide": "Guide", "faq": "FAQ"},
}

H2NAV = {
    "de": "Spreadsheet / Finds / QC / Versand",
    "nl": "Spreadsheet / finds / QC / Verzending",
    "es": "Spreadsheet / finds / QC / Envío",
    "fr": "Spreadsheet / finds / QC / Livraison",
    "it": "Spreadsheet / finds / QC / Spedizione",
    "en": "Spreadsheet / finds / QC / Shipping",
}

CTA = {
    "de": "Bestellen und zahlen auf litbuy.com. Anzeige auf dieser Seite in lokaler Währung.",
    "nl": "Bestellen en betalen op litbuy.com. Prijzen op deze pagina staan in lokale valuta.",
    "es": "Pide y paga en litbuy.com. Precios en esta página en moneda local.",
    "fr": "Commandez et payez sur litbuy.com. Prix affichés dans la devise locale.",
    "it": "Ordina e paga su litbuy.com. Prezzi in valuta locale.",
    "en": "Shop and pay on litbuy.com. Prices on this page are shown in local currency.",
}

UNIQUE_PUT = {
    "spreadsheet",
    "post-at-sendungsverfolgung",
    "zoll-ust-oesterreich",
    "ratgeber-oesterreich",
    "dsgvo-litbuy-oesterreich",
    "ist-litbuy-serioes",
    "litbuy-shipping-canada",
    "cbsa-import-canada",
    "gst-hst-import-canada",
    "canada-post-customs",
    "ca-buyer-guides",
    "dogana-poste-italiane",
    "iva-importazione-italia",
    "guide-italia",
    "de-minimis-us-litbuy",
    "duties-taxes-usps-fedex",
    "litbuy-shipping-times-us",
    "us-customs-declaration-guide",
    "vat-on-imports-uk-2026",
    "hmrc-import-charges-uk",
    "litbuy-shipping-uk",
    "royal-mail-customs-uk",
    "livraison-litbuy-france",
    "tva-import-france",
    "colissimo-douane-france",
    "aduana-correos-espana",
    "iva-importacion-espana",
    "guias-espana",
    "guias-comprador-es",
    "douane-nederland-dhl",
    "btw-import-nederland",
    "litbuy-verzendkosten-nederland",
    "ideal-betalen-litbuy",
    "ioss-import-vat-eu",
    "ecommerce-vat-reform-eu",
    "what-is-litbuy",
    "litbuy-coupon",
    "litbuy-coupons",
    "is-litbuy-legit",
    "is-litbuy-safe",
    "litbuy-qc-guide",
    "litbuy-refund-guide",
    "litbuy-shoes-spreadsheet",
    "litbuy-spreadsheet-2026",
    "litbuy-community",
    "litbuy-invite-code",
    "litbuy-freight",
    "litbuy-haul",
    "litbuy-announcements",
    "best-litbuy-spreadsheet",
    "litbuy-spreadsheets",
    "how-to-use-litbuy",
    "litbuy-review",
    "gst-import-australia",
    "litbuy-shipping-australia",
    "de-minimis-us-litbuy",
    "cbp-declared-value-us",
    "litbuy-shipping-times-us",
    "vat-on-imports-uk-2026",
    "royal-mail-customs-uk",
    "cbsa-import-canada",
    "gst-landed-cost-canada",
    "litbuy-shipping-canada",
    "aduana-iva-espana",
    "guias-comprador-es",
    "btw-import-nederland",
    "kaeuferguides-at",
    "zoll-einfuhr-oesterreich",
    "ioss-import-vat-eu",
    "ecommerce-vat-reform-eu",
    "affiliate-disclosure",
    "partner-disclosure",
    "privacy-policy",
    "cookie-policy",
    "refund-policy",
    "contact",
    "terms",
    "category",
    "blog",
    "brand",
    "guides",
}

RECLAIM = {
    "litbuyspreadsheets.us": "litbuy.at",
    "litbuyspreadsheet.me.uk": "litbuy.at",
    "litspreadsheet.fr": "litbuy.at",
    "litbuyspreadsheets.es": "litbuy.at",
    "litbuyspreadsheets.nl": "litbuy.at",
}


def _is_unique(rest: str) -> bool:
    parts = Path(rest).parts
    if any(p in UNIQUE_PUT for p in parts):
        return True
    return any(p.startswith("litbuy-announcement") for p in parts)


def overlay(host: str) -> Path:
    return ROOT / "sites" / host / "overlay"


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


def _run(client, cmd: str, timeout: int = 90) -> str:
    _, stdout, stderr = client.exec_command(cmd, timeout=timeout)
    return (stdout.read() + stderr.read()).decode(errors="replace").strip()


def reclaim_nginx() -> None:
    """Clone the AT dest vhost onto Phase B/C catch-all 301 vhosts. Keep hub."""
    if not RECLAIM:
        print("RECLAIM_NGINX 0")
        return
    client = _connect()
    sftp = client.open_sftp()
    stamp = time.strftime("%Y%m%d-%H%M%S")
    bak = f"/www/backup/litbuy-reclaim-{stamp}"
    _run(client, f"mkdir -p '{bak}'")
    template = _run(client, "cat /www/server/panel/vhost/nginx/litbuy.at.conf")
    if "enable-php-74.conf" not in template or "rewrite ^/api/" not in template:
        raise SystemExit("AT dest vhost missing php-74 /api rewrite")
    n = 0
    try:
        for host in RECLAIM:
            path = f"/www/server/panel/vhost/nginx/{host}.conf"
            orig = _run(client, f"cat '{path}'")
            already = (
                "enable-php-74.conf" in orig
                and "rewrite ^/api/" in orig
                and "return 301 https://litbuyspreadsheet.eu" not in orig
            )
            if already:
                print("RECLAIM_SKIP already dest", host)
                continue
            _run(client, f"cp -a '{path}' '{bak}/{host}.conf'")
            raw = template.replace("litbuy.at", host)
            _run(client, f"mkdir -p '/www/server/panel/vhost/nginx/extension/{host}'")
            rw = f"/www/server/panel/vhost/rewrite/{host}.conf"
            if "No such file" in _run(client, f"test -f '{rw}' && echo OK || echo MISSING"):
                _run(client, f"touch '{rw}'")
            with sftp.open(path, "w") as fh:
                fh.write(raw)
            print("RECLAIM", host)
            n += 1
        if n:
            test = _run(client, "nginx -t && nginx -s reload")
            print(test)
            if "successful" not in test and "ok" not in test.lower():
                raise SystemExit("nginx -t failed after reclaim")
    finally:
        sftp.close()
        client.close()
    print("RECLAIM_NGINX", n, "backup", bak)


def _nav(d: dict) -> str:
    labels = NAV_LAB[d["loc"] if d["loc"] in NAV_LAB else "en"]
    items = []
    for kind, slug in d["pages"].items():
        items.append(f'<li><a href="/{slug}/">{escape(labels.get(kind, kind))}</a></li>')
    return '<ul class="cluster-links">' + "".join(items) + "</ul>"


def _nav_links(d: dict) -> str:
    labels = NAV_LAB[d["loc"] if d["loc"] in NAV_LAB else "en"]
    return "".join(
        f'<a href="/{slug}/">{escape(labels.get(kind, kind))}</a>' for kind, slug in d["pages"].items()
    )


def render_article(host: str, kind: str, d: dict) -> str:
    h1, lead, secs = sections_for(kind, d, host)
    loc = d["loc"] if d["loc"] in H2NAV else "en"
    figs = cbskin.article_figures(kind, d)
    chunks = [
        f'<article class="cluster-page" data-spreadsheet-cluster="20261030" {MARKER} data-kind="{escape(kind)}">',
        f"<h1>{escape(h1)}</h1>",
        f'<p class="lead">{escape(lead)}</p>',
    ]
    if figs:
        chunks.append(figs[0])
    for i, (h2, paras) in enumerate(secs):
        chunks.append(f"<h2>{escape(h2)}</h2>")
        for p in paras:
            chunks.append(f"<p>{escape(p)}</p>")
        if i == 1 and len(figs) > 1:
            chunks.append(figs[1])
    chunks.append(f"<h2>{escape(H2NAV[loc])}</h2>")
    chunks.append(_nav(d))
    chunks.append(f'<p class="kb-cta">{escape(CTA[loc])}</p>')
    chunks.append("</article>")
    return "\n".join(chunks) + "\n"


MAIN_RE = re.compile(r"(<main\b[^>]*>)(.*?)(</main>)", re.I | re.S)


def swap_main(html: str, inner: str) -> str:
    if not MAIN_RE.search(html):
        raise ValueError("missing <main>")
    return MAIN_RE.sub(lambda m: m.group(1) + "\n" + inner + m.group(3), html, count=1)


def ensure_cluster_shell(host: str, path: Path) -> str:
    html = path.read_text(encoding="utf-8")
    if MAIN_RE.search(html):
        return html
    for kind in ("spreadsheet", "finds", "faq", "shipping", "guide"):
        slug = HOSTS[host]["pages"].get(kind)
        if not slug:
            continue
        src = overlay(host) / slug / "index.html"
        if src.is_file() and src != path:
            shell = src.read_text(encoding="utf-8")
            if MAIN_RE.search(shell):
                print("SHELL", host, path.parent.name, "from", slug)
                return shell
    for fb_host, fb_slug in (("litbuy.at", "litbuy-finds"),):
        fb = overlay(fb_host) / fb_slug / "index.html"
        if fb.is_file():
            shell = fb.read_text(encoding="utf-8")
            if MAIN_RE.search(shell):
                print("SHELL", host, path.parent.name, "from", fb_host, fb_slug)
                return shell
    raise ValueError(f"missing <main> and no cluster shell on {host} {path}")


def upsert_meta(html: str, name: str, content: str) -> str:
    tag = f'<meta name="{name}" content="{escape(content)}">'
    if re.search(rf'<meta\s+name="{name}"', html, re.I):
        return re.sub(rf'<meta\s+name="{name}"[^>]*>', tag, html, count=1, flags=re.I)
    return html.replace("</head>", tag + "\n</head>", 1)


def patch_cluster_nav(html: str, d: dict) -> str:
    inner = _nav_links(d)
    nav = f'<nav class="cluster-nav" data-spreadsheet-cluster="20261030" aria-label="LitBuy">{inner}</nav>'
    if re.search(r'<nav class="cluster-nav"', html, re.I):
        return re.sub(
            r'<nav class="cluster-nav"[^>]*>.*?</nav>',
            nav,
            html,
            count=1,
            flags=re.I | re.S,
        )
    return re.sub(r"(</h1>)", r"\1" + nav, html, count=1, flags=re.I)


def _home_ld_replacer(host, serp, kws, d):
    def repl(m: re.Match) -> str:
        raw = m.group(1).strip()
        try:
            data = json.loads(raw)
        except json.JSONDecodeError:
            return m.group(0)
        if not isinstance(data, dict):
            return m.group(0)
        if data.get("@type") == "WebPage":
            data["name"] = serp
            data["url"] = f"https://{host}/"
            data["@id"] = f"https://{host}/"
            data["inLanguage"] = d.get("lang") or "en"
            if d.get("dest") == "CA":
                data["description"] = (
                    f"{A} Spreadsheet for Canadian buyers on {host}. Finds, QC, shipping. Source: {d['customs']}."
                )
            part = data.get("isPartOf")
            if isinstance(part, dict):
                part["@type"] = "WebSite"
                part["name"] = serp
                part["url"] = f"https://{host}/"
                part["keywords"] = kws
                data["isPartOf"] = part
        if data.get("@type") == "WebSite":
            data["name"] = serp
            data["keywords"] = kws
            data["url"] = f"https://{host}/"
            data["inLanguage"] = d.get("lang") or "en"
        return f'<script type="application/ld+json">{json.dumps(data, ensure_ascii=False)}</script>'

    return repl


def patch_home(host: str, d: dict) -> Path:
    path = overlay(host) / "index.html"
    html = path.read_text(encoding="utf-8")
    serp = cluster_title_serp(A, d["dest"], d["loc"], d["label"])
    kws = cluster_keywords(A, d["dest"], d["loc"], d["label"])
    html = re.sub(r'(<html\b[^>]*\blang=")[^"]*', rf'\1{d["lang"]}', html, count=1, flags=re.I)
    html = patch_cluster_nav(html, d)
    html = re.sub(r"<title>[\s\S]*?</title>", f"<title>{escape(serp)}</title>", html, count=1, flags=re.I)
    desc = {
        "de": f"{A} Spreadsheet für {d['label']} auf {host}. Finds, QC, Versand. Quelle: {d['customs']}.",
        "nl": f"{A} spreadsheet voor {d['label']} op {host}. Finds, QC, verzending. Bron: {d['customs']}.",
        "it": f"{A} Spreadsheet per {d['label']} su {host}. Finds, QC, spedizione. Fonte: {d['customs']}.",
    }.get(d["loc"], f"{A} Spreadsheet for {d['label']} buyers on {host}. Finds, QC, shipping. Source: {d['customs']}.")
    if d.get("dest") == "CA":
        desc = f"{A} Spreadsheet for Canadian buyers on {host}. Finds, QC, shipping. Source: {d['customs']}."
    html = upsert_meta(html, "description", desc)
    html = upsert_meta(html, "keywords", ", ".join(kws))
    html = re.sub(
        r'(<link\s+rel="canonical"\s+href=")[^"]*(")',
        rf'\1https://{host}/\2',
        html,
        count=1,
        flags=re.I,
    )
    html = re.sub(
        r'(<meta\s+property="og:url"\s+content=")[^"]*(")',
        rf'\1https://{host}/\2',
        html,
        count=1,
        flags=re.I,
    )
    h1 = cluster_title_serp(A, d["dest"], d["loc"], d["label"]).split(" – ")[0].split(" - ")[0]
    html = re.sub(r"<h1>[\s\S]*?</h1>", f"<h1>{escape(h1)}</h1>", html, count=1, flags=re.I)
    html = re.sub(
        r'(<meta\s+property="og:title"\s+content=")[^"]*(")',
        rf"\1{escape(serp)}\2",
        html,
        count=1,
        flags=re.I,
    )
    html = re.sub(
        r'<script type="application/ld\+json">([\s\S]*?)</script>',
        _home_ld_replacer(host, serp, kws, d),
        html,
        count=1,
        flags=re.I,
    )
    if MARKER.split("=")[0] not in html:
        html = inject_jsonld(
            html,
            website_ld(
                url=f"https://{host}/",
                name=serp,
                lang=d["lang"],
                brand=A,
                host=host,
                keywords=kws,
            ),
        )
        html = html.replace("<body", f"<body {MARKER}", 1)
    html = cbskin.rebuild_home(html, host, d)
    html = retarget_host(html, host, d)
    path.write_text(html, encoding="utf-8")
    return path


def retarget_host(html: str, host: str, d: dict) -> str:
    for old in ("litbuy.at", "litbuyspreadsheet.it", "litbuyspreadsheets.ca"):
        html = html.replace(f"https://{old}/", f"https://{host}/")
        html = html.replace(f"support@{old}", f"support@{host}")
        if old != host:
            html = html.replace(old, host)
    html = re.sub(r"\?inviteCode=[A-Za-z0-9]+", "", html)
    html = re.sub(r"\?O4K87NHKR", "", html)
    html = html.replace("https://litbuy.com/register?O4K87NHKR", "https://litbuy.com/register")
    html = html.replace("O4K87NHKR", "")
    html = re.sub(r'"inLanguage": "en-CA"', f'"inLanguage": "{d["lang"]}"', html)
    html = re.sub(r'\s*<link rel="alternate"[^>]*hreflang="[^"]*"[^>]*>', "", html, flags=re.I)
    html = html.replace("litbuyspreadsheet.ca", host)
    loc = d.get("loc") or "en"
    if loc == "en":
        html = html.replace("Naar de inhoud", "Skip to content")
        html = html.replace("Zum Inhalt", "Skip to content")
        html = html.replace("Vai al contenuto", "Skip to content")
    elif loc == "nl":
        html = html.replace("Skip to content", "Naar de inhoud")
        html = html.replace("Zum Inhalt", "Naar de inhoud")
    elif loc == "de":
        html = html.replace("Skip to content", "Zum Inhalt")
        html = html.replace("Naar de inhoud", "Zum Inhalt")
    html = re.sub(r"\?inviteCode=[A-Za-z0-9]+", "", html)
    return html


def _inner_ld_replacer(page_url: str, name: str, kws: list[str], desc: str):
    def repl(m: re.Match) -> str:
        raw = m.group(1).strip()
        try:
            data = json.loads(raw)
        except json.JSONDecodeError:
            return m.group(0)
        if isinstance(data, dict) and data.get("@type") == "WebPage":
            data["@id"] = page_url
            data["url"] = page_url
            data["name"] = name
            data["description"] = desc[:220]
            data["keywords"] = kws
        return f'<script type="application/ld+json">{json.dumps(data, ensure_ascii=False)}</script>'

    return repl


def deepen_inner(host: str, kind: str, d: dict) -> Path | None:
    slug = d["pages"].get(kind)
    if not slug or kind in d.get("skip", set()):
        return None
    path = overlay(host) / slug / "index.html"
    if not path.is_file():
        print("MISSING", host, slug)
        return None
    html = ensure_cluster_shell(host, path)
    inner = render_article(host, kind, d)
    html = swap_main(html, inner)
    html = re.sub(r'(<html\b[^>]*\blang=")[^"]*', rf'\1{d["lang"]}', html, count=1, flags=re.I)
    h1, lead, secs = sections_for(kind, d, host)
    serp = inner_serp_title(kind, d)
    kws = inner_keywords(kind, d)
    page_url = f"https://{host}/{slug}/"
    html = re.sub(r"<title>[\s\S]*?</title>", f"<title>{escape(serp)}</title>", html, flags=re.I)
    html = re.sub(
        r'(<meta\s+property="og:title"\s+content=")[^"]*(")',
        rf"\1{escape(serp)}\2",
        html,
        count=1,
        flags=re.I,
    )
    html = re.sub(
        r'(<meta\s+property="og:url"\s+content=")[^"]*(")',
        rf"\1{page_url}\2",
        html,
        count=1,
        flags=re.I,
    )
    html = re.sub(
        r'(<link\s+rel="canonical"\s+href=")[^"]*(")',
        rf"\1{page_url}\2",
        html,
        count=1,
        flags=re.I,
    )
    html = re.sub(
        r'<script type="application/ld\+json">([\s\S]*?)</script>',
        _inner_ld_replacer(page_url, serp, kws, lead),
        html,
        count=1,
        flags=re.I,
    )
    html = upsert_meta(html, "keywords", ", ".join(kws))
    html = upsert_meta(html, "description", lead[:220])
    html = re.sub(
        r'(<meta\s+property="og:description"\s+content=")[^"]*(")',
        rf"\1{escape(lead[:220])}\2",
        html,
        count=1,
        flags=re.I,
    )
    html = patch_cluster_nav(html, d)
    if kind == "faq":
        pairs = [(h2, " ".join(paras)) for h2, paras in secs]
        block = faq_ld(d["lang"], pairs)
        dumped = json.dumps(block, ensure_ascii=False)
        if '"FAQPage"' in html:
            html = re.sub(
                r'<script type="application/ld\+json">\s*\{[^{}]*"@type"\s*:\s*"FAQPage"[\s\S]*?</script>',
                f'<script type="application/ld+json">{dumped}</script>',
                html,
                count=1,
            )
        else:
            html = inject_jsonld(html, block)
    html = retarget_host(html, host, d)
    path.write_text(html, encoding="utf-8")
    return path


def wrap_old_slug(host: str, d: dict, old: str, keep: str) -> Path | None:
    src = overlay(host) / keep / "index.html"
    if not src.is_file():
        src = overlay(host) / old / "index.html"
    if not src.is_file():
        return None
    dest_dir = overlay(host) / old
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest = dest_dir / "index.html"
    html = src.read_text(encoding="utf-8")
    h1, lead, secs = wrap_copy(host, d, keep)
    chunks = [
        f'<article class="cluster-page" {MARKER} data-kind="wrap">',
        f"<h1>{escape(h1)}</h1>",
        f'<p class="lead">{escape(lead)}</p>',
    ]
    for h2, paras in secs:
        chunks.append(f"<h2>{escape(h2)}</h2>")
        for p in paras:
            chunks.append(f"<p>{escape(p)}</p>")
    chunks.append(_nav(d))
    chunks.append("</article>\n")
    html = swap_main(html, "\n".join(chunks))
    keep_url = f"https://{host}/{keep}/"
    wrap_url = f"https://{host}/{old}/"
    html = re.sub(r"<title>[\s\S]*?</title>", f"<title>{escape(h1)}</title>", html, flags=re.I)
    html = re.sub(
        r'(<link\s+rel="canonical"\s+href=")[^"]*(")',
        rf"\1{keep_url}\2",
        html,
        count=1,
        flags=re.I,
    )
    html = re.sub(
        r'(<meta\s+property="og:url"\s+content=")[^"]*(")',
        rf"\1{wrap_url}\2",
        html,
        count=1,
        flags=re.I,
    )
    html = upsert_meta(html, "description", lead[:220])
    html = cbskin.skin_chrome(html, host, d)
    dest.write_text(html, encoding="utf-8")
    print("WRAP", host, old, "->", keep)
    return dest


def bump_sitemap(host: str, d: dict) -> None:
    path = overlay(host) / "sitemap.xml"
    if not path.is_file():
        path.write_text(
            '<?xml version="1.0" encoding="UTF-8"?>\n'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n</urlset>\n',
            encoding="utf-8",
        )
    sm = path.read_text(encoding="utf-8")
    locs = [f"https://{host}/"] + [f"https://{host}/{slug}/" for slug in d["pages"].values()]
    for loc in locs:
        sm = re.sub(
            rf"(<loc>\s*{re.escape(loc)}\s*</loc>\s*<lastmod>)[^<]+",
            rf"\g<1>{TODAY}",
            sm,
        )
        if loc not in sm and "</urlset>" in sm:
            sm = sm.replace(
                "</urlset>",
                "  <url>\n"
                f"    <loc>{loc}</loc>\n"
                f"    <lastmod>{TODAY}</lastmod>\n"
                "    <changefreq>weekly</changefreq>\n"
                "    <priority>0.8</priority>\n"
                "  </url>\n</urlset>",
                1,
            )
    path.write_text(sm, encoding="utf-8")


def seed_missing_cluster(host: str, template: str | None = None) -> None:
    dest = overlay(host)
    dest.mkdir(parents=True, exist_ok=True)
    d = HOSTS[host]
    if template is None:
        template = "litbuy.at"
    src = overlay(template)
    live = dest / "live-base" / "index.html"
    home = dest / "index.html"
    template_home = overlay(template) / "index.html"
    if not home.is_file() and template_home.is_file() and host != template:
        home.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(template_home, home)
        print("SEED home from template", host, template)
    elif not home.is_file() and live.is_file():
        shutil.copy2(live, home)
        print("SEED home from live-base", host)
    skip_slugs = {d["pages"][k] for k in d.get("skip", set()) if k in d["pages"]}
    needed = ["index.html"] + [d["pages"][k] for k in d["pages"] if k not in d.get("skip", set())]
    fallbacks = [
        overlay("litbuy.at") / "litbuy-finds" / "index.html",
        overlay("litbuy.at") / "litbuy-faq" / "index.html",
        overlay("litbuy.at") / "index.html",
    ]
    for name in needed:
        if name == "index.html":
            target = dest / "index.html"
            source = src / "index.html" if (src / "index.html").is_file() else src / "live-base" / "index.html"
        else:
            if name in skip_slugs:
                continue
            target = dest / name / "index.html"
            source = src / name / "index.html"
            if not source.is_file():
                for fb_host in ("litbuy.at", "litbuyspreadsheet.it", "litbuyspreadsheets.ca"):
                    cand = overlay(fb_host) / name / "index.html"
                    if cand.is_file():
                        source = cand
                        template = fb_host
                        break
            if not source.is_file():
                source = next((p for p in fallbacks if p.is_file()), source)
        if target.is_file():
            continue
        if not source.is_file():
            print("SEED_SKIP missing template", host, name)
            continue
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(source.read_bytes())
        print("SEED", host, name, "from", source.parent.parent.name if name != "index.html" else template)


def reskin_overlay() -> list[Path]:
    written: list[Path] = []
    for host in ORDER:
        d = HOSTS[host]
        root = overlay(host)
        if not root.is_dir():
            continue
        for path in root.rglob("*.html"):
            if "live-base" in path.parts or path.name.startswith("live-base"):
                continue
            rest = path.relative_to(root).as_posix()
            if _is_unique(rest):
                continue
            html = path.read_text(encoding="utf-8", errors="replace")
            html = cbskin.skin_chrome(html, host, d)
            html = retarget_host(html, host, d)
            path.write_text(html, encoding="utf-8")
            written.append(path)
            print("RESKIN", host, rest, path.stat().st_size)
    return written


def leftover_skin() -> list[Path]:
    written: list[Path] = []
    client = None
    sftp = None
    try:
        for host, slugs in LEFTOVER_SKIN.items():
            if host not in ORDER:
                continue
            d = HOSTS[host]
            for slug in slugs:
                if _is_unique(slug):
                    print("SKIP leftover unique", host, slug)
                    continue
                path = overlay(host) / slug / "index.html"
                if not path.is_file():
                    alt = path.parent / "live-base.index.html"
                    if alt.is_file():
                        path.parent.mkdir(parents=True, exist_ok=True)
                        shutil.copy2(alt, path)
                    else:
                        if sftp is None:
                            client = _connect()
                            sftp = client.open_sftp()
                        remote = f"/www/wwwroot/{host}/{slug}/index.html"
                        try:
                            path.parent.mkdir(parents=True, exist_ok=True)
                            sftp.get(remote, str(path))
                        except Exception as exc:  # noqa: BLE001
                            print("SKIP leftover", host, slug, type(exc).__name__)
                            continue
                if path.stat().st_size < 200:
                    print("SKIP leftover empty", host, slug)
                    continue
                html = path.read_text(encoding="utf-8", errors="replace")
                html = cbskin.skin_chrome(html, host, d)
                html = retarget_host(html, host, d)
                html = re.sub(r'\s*<link rel="alternate"[^>]*hreflang="[^"]*"[^>]*>', "", html, flags=re.I)
                path.write_text(html, encoding="utf-8")
                written.append(path)
                print("LEFTOVER_SKIN", host, slug, path.stat().st_size)
    finally:
        if sftp is not None:
            sftp.close()
        if client is not None:
            client.close()
    return written


def pull_missing_homes() -> None:
    need = [
        h
        for h in ORDER
        if not (overlay(h) / "index.html").is_file()
        and not (overlay(h) / "live-base" / "index.html").is_file()
    ]
    if not need:
        return
    client = _connect()
    sftp = client.open_sftp()
    try:
        for host in need:
            dest = overlay(host)
            live = dest / "live-base" / "index.html"
            live.parent.mkdir(parents=True, exist_ok=True)
            try:
                sftp.get(f"/www/wwwroot/{host}/index.html", str(live))
                print("PULL home", host, live.stat().st_size)
            except Exception as exc:  # noqa: BLE001
                print("PULL_FAIL", host, type(exc).__name__)
    finally:
        sftp.close()
        client.close()


def pull_official_media() -> None:
    dest = ROOT / "sites" / "shared" / "litbuy-media"
    shots = dest / "shots"
    cats = dest / "cats"
    dest.mkdir(parents=True, exist_ok=True)
    shots.mkdir(parents=True, exist_ok=True)
    cats.mkdir(parents=True, exist_ok=True)
    seed_cats = Path("/tmp/litbuy-media/cats")
    if not seed_cats.is_dir():
        seed_cats = Path("/tmp/hipobuy-media/cats")
    if seed_cats.is_dir() and not any(cats.iterdir()):
        for p in seed_cats.iterdir():
            if p.is_file():
                shutil.copy2(p, cats / p.name)
        print("SEED cats from snapshot", len(list(cats.iterdir())))
    client = _connect()
    sftp = client.open_sftp()
    try:
        for remote_shots in (
            "/www/wwwroot/litbuy.at/media",
            "/www/wwwroot/litbuy.at/media/shots",
            "/www/wwwroot/litbuy.at/assets/images",
        ):
            try:
                for name in sftp.listdir(remote_shots):
                    if not name.lower().endswith((".jpg", ".jpeg", ".png", ".webp")):
                        continue
                    local = shots / name
                    sftp.get(f"{remote_shots}/{name}", str(local))
                    print("PULL shot", name, local.stat().st_size)
            except Exception as exc:  # noqa: BLE001
                print("PULL_SHOTS_FAIL", remote_shots, type(exc).__name__, str(exc)[:120])
        for remote, local_name in (
            ("/www/wwwroot/litbuy.at/assets/images/litbuy-logo.png", dest / "litbuy-logo.png"),
            ("/www/wwwroot/litbuy.at/assets/images/litbuy-logo-eu.png", dest / "litbuy-logo-eu.png"),
            ("/www/wwwroot/litbuy.at/media/official-home-20261001.jpg", dest / "official-home.jpg"),
            ("/www/wwwroot/litbuy.at/media/official-home-20261001.jpg", dest / "shots" / "oficial-inicio.jpg"),
            ("/www/wwwroot/litbuy.at/media/estimator-20261001.jpg", dest / "shots" / "estimator-de.jpg"),
            ("/www/wwwroot/litbuy.at/media/estimator-20261001.jpg", dest / "shots" / "estimator-at.jpg"),
            ("/www/wwwroot/litbuy.at/media/help-restricted-20261001.jpg", dest / "shots" / "oficial-diy.jpg"),
            ("/www/wwwroot/acbuyspreadsheets.ca/img/cat/sneakers.png", cats / "sneakers.png"),
        ):
            try:
                sftp.get(remote, str(local_name))
                print("PULL", local_name.name, local_name.stat().st_size)
            except Exception as exc:  # noqa: BLE001
                print("PULL_SKIP", remote, type(exc).__name__)
        for host in ORDER:
            try:
                for name in sftp.listdir(f"/www/wwwroot/{host}/img"):
                    if name.lower().endswith(".png"):
                        local = cats / name
                        sftp.get(f"/www/wwwroot/{host}/img/{name}", str(local))
                        print("PULL cat", host, name, local.stat().st_size)
            except Exception as exc:  # noqa: BLE001
                print("PULL_CAT_SKIP", host, type(exc).__name__)
            try:
                for name in sftp.listdir(f"/www/wwwroot/{host}/img/cat"):
                    if name.lower().endswith(".png"):
                        local = cats / name
                        sftp.get(f"/www/wwwroot/{host}/img/cat/{name}", str(local))
                        print("PULL cat", host, name, local.stat().st_size)
            except Exception as exc:  # noqa: BLE001
                print("PULL_CAT_DIR_SKIP", host, type(exc).__name__)
        if not any(cats.iterdir()):
            try:
                for name in sftp.listdir("/www/wwwroot/litbuy.at/img"):
                    if name.lower().endswith(".png"):
                        local = cats / name
                        sftp.get(f"/www/wwwroot/litbuy.at/img/{name}", str(local))
                        print("PULL cat fallback", name, local.stat().st_size)
            except Exception as exc:  # noqa: BLE001
                print("PULL_CAT_FALLBACK_SKIP", type(exc).__name__)
        try:
            for name in sftp.listdir("/www/wwwroot/acbuyspreadsheets.ca/img/cat"):
                if name.lower().endswith(".png"):
                    local = cats / name
                    if not local.is_file():
                        sftp.get(f"/www/wwwroot/acbuyspreadsheets.ca/img/cat/{name}", str(local))
                        print("PULL cat acbuy", name, local.stat().st_size)
        except Exception as exc:  # noqa: BLE001
            print("PULL_CAT_ACBUY_SKIP", type(exc).__name__)
    finally:
        sftp.close()
        client.close()
    home = dest / "official-home.jpg"
    if not home.is_file() or home.stat().st_size < 200:
        for cand in (
            dest / "hero.jpg",
            shots / "oficial-inicio.jpg",
            shots / "official-home-20261001.jpg",
            shots / "estimator-20261001.jpg",
            shots / "official-home-20260930.jpg",
            shots / "catalogus.jpg",
            shots / "volume-voorbeeld.jpg",
        ):
            if cand.is_file() and cand.stat().st_size > 200:
                shutil.copy2(cand, home)
                print("SEED official-home", cand.name)
                break
    est_src = next(
        (
            p
            for p in (
                shots / "estimator-20261001.jpg",
                shots / "estimator-at.jpg",
                shots / "estimator-de.jpg",
                shots / "estimator-au.jpg",
                shots / "estimator-20260930.jpg",
                dest / "official-home.jpg",
            )
            if p.is_file() and p.stat().st_size > 200
        ),
        None,
    )
    if est_src:
        for key in ("uk", "nl", "us", "at", "au", "ca", "fr", "es", "de", "it"):
            dest_est = shots / f"estimator-{key}.jpg"
            if not dest_est.is_file() or dest_est.stat().st_size < 200:
                shutil.copy2(est_src, dest_est)


def generate() -> list[Path]:
    written: list[Path] = []
    pull_official_media()
    pull_missing_homes()
    for host in ORDER:
        d = HOSTS[host]
        seed_missing_cluster(host)
        written.extend(cbskin.install_media(host))
        theme_src = ROOT / "sites" / "shared" / "themes" / "litbuy-theme.css"
        if theme_src.is_file():
            css_dir = overlay(host) / "assets" / "css"
            css_dir.mkdir(parents=True, exist_ok=True)
            theme_out = css_dir / "litbuy-theme.css"
            shutil.copy2(theme_src, theme_out)
            written.append(theme_out)
        written.append(patch_home(host, d))
        print("HOME", host, cluster_title_serp(A, d["dest"], d["loc"], d["label"]))
        for kind in d["pages"]:
            p = deepen_inner(host, kind, d)
            if p:
                written.append(p)
                print("INNER", host, kind, p.relative_to(ROOT))
        for old, keep in d.get("canon") or []:
            wrap = wrap_old_slug(host, d, old, keep)
            if wrap:
                written.append(wrap)
        cbskin.skin_overlay_files(host, d, [p for p in written if str(p).startswith(str(overlay(host)))])
        bump_sitemap(host, d)
        sm = overlay(host) / "sitemap.xml"
        if sm.is_file():
            written.append(sm)
        written.extend(write_api_overlay(host))
    written.extend(leftover_skin())
    return written


def write_api_overlay(host: str) -> list[Path]:
    api_dir = overlay(host) / "api"
    prod_dir = api_dir / "products"
    prod_dir.mkdir(parents=True, exist_ok=True)
    upstream = api_dir / "products.php"
    index = prod_dir / "index.php"
    upstream.write_text(PRODUCTS_PHP, encoding="utf-8")
    index.write_text(PRODUCTS_INDEX, encoding="utf-8")
    print("API", host, "products.php + products/index.php")
    return [upstream, index]


def _w2c_api_key() -> str:
    for name in ("W2CLINKS_API_KEY", "W2C_PRODUCTS_API_KEY"):
        val = (os.environ.get(name) or "").strip()
        if val:
            return val
    for path in (
        Path("/cursor/stores/self/w2c-api-key"),
        Path("/tmp/hipobuy-creds/w2c-api-key"),
    ):
        if path.is_file():
            val = path.read_text(encoding="utf-8").strip()
            if val:
                return val
    return ""


def put_api_secrets(client) -> None:
    key = _w2c_api_key()
    if not key:
        print("API_KEY_SKIP no key file")
        return
    body = (
        "<?php\ndeclare(strict_types=1);\n"
        "return ['api_key' => " + json.dumps(key) + "];\n"
    )
    sftp = client.open_sftp()
    n = 0
    for host in ORDER:
        remote = f"/www/wwwroot/{host}/api/config.local.php"
        _run(client, f"mkdir -p '/www/wwwroot/{host}/api'")
        bak = remote + ".bak"
        _run(client, f"test -f '{remote}' && cp -a '{remote}' '{bak}' || true")
        with sftp.open(remote, "w") as fh:
            fh.write(body)
        _run(client, f"chown www:www '{remote}' && chmod 640 '{remote}'")
        n += 1
    sftp.close()
    print("API_KEY_PUT", n, "hosts")


def fix_api_nginx(client) -> None:
    rewrite_line = "rewrite ^/api/([^/]+)/?$ /api/$1/index.php last;"
    olds = [
        """    location /api/ {
        try_files $uri =404;
        add_header X-Robots-Tag "noindex, nofollow" always;
    }
""",
        """    location /api/ {
        try_files $uri =404;
    }
""",
    ]
    new = """    location /api/ {
        rewrite ^/api/([^/]+)/?$ /api/$1/index.php last;
        add_header X-Robots-Tag "noindex, nofollow" always;
    }
"""
    php_inc = "    include enable-php-74.conf;\n"
    loc_open = re.compile(r"location\s+(?:\^~\s+)?/api/\s*\{")
    changed = 0
    sftp = client.open_sftp()
    stamp = time.strftime("%Y%m%d-%H%M%S")
    bak_root = f"/www/backup/litbuy-api-nginx-{stamp}"
    _run(client, f"mkdir -p '{bak_root}'")
    for host in ORDER:
        path = f"/www/server/panel/vhost/nginx/{host}.conf"
        raw = _run(client, f"cat '{path}'")
        orig = raw
        if rewrite_line not in raw:
            matched = next((blk for blk in olds if blk in raw), None)
            if matched:
                raw = raw.replace(matched, new, 1)
            else:
                m = loc_open.search(raw)
                if m:
                    raw = raw[: m.end()] + "\n        " + rewrite_line + raw[m.end() :]
                else:
                    idx = raw.rfind("    access_log ")
                    if idx == -1:
                        print("skip", host, "api insert point missing")
                        continue
                    raw = raw[:idx] + new + "\n" + raw[idx:]
        if "enable-php-74.conf" not in raw and "php-cgi-74.sock" not in raw:
            m = loc_open.search(raw)
            if m:
                raw = raw[: m.start()] + php_inc + "\n" + raw[m.start() :]
            else:
                idx = raw.rfind("    access_log ")
                if idx != -1:
                    raw = raw[:idx] + php_inc + raw[idx:]
        if "index index.html;" in raw and "index.php" not in raw.split("index index.html;", 1)[0][-80:]:
            raw = raw.replace("    index index.html;\n", "    index index.html index.htm index.php;\n", 1)
        if raw == orig:
            print("ok", host, "api rewrite")
            continue
        _run(client, f"cp -a '{path}' '{bak_root}/{host}.conf'")
        with sftp.open(path, "w") as fh:
            fh.write(raw)
        print("PATCH", path)
        changed += 1
    sftp.close()
    if changed:
        print(_run(client, "nginx -t && nginx -s reload"))
    print("NGINX_API", changed)


def put(files: list[Path] | None = None) -> None:
    if files is None:
        files = generate()
    client = _connect()
    stamp = time.strftime("%Y%m%d-%H%M%S")
    bak = f"/www/backup/litbuy-dest-{stamp}"
    print(_run(client, f"mkdir -p '{bak}'"))
    sftp = client.open_sftp()
    n = 0
    for path in files:
        rel = path.relative_to(ROOT / "sites").as_posix()
        host = rel.split("/", 1)[0]
        if host == HUB_KEEP or host in SKIP_HOSTS or host in TWINS_KEEP:
            print("PUT_SKIP hub/twin", host)
            continue
        rest = path.relative_to(overlay(host)).as_posix()
        if rest.split("/", 1)[0] in {"live-base", "live-base.index.html"}:
            print("PUT_SKIP live-base", host, rest)
            continue
        remote = f"/www/wwwroot/{host}/{rest}"
        _run(client, f"mkdir -p '{str(Path(remote).parent)}'")
        _run(
            client,
            f"test -f '{remote}' && mkdir -p '{bak}/{host}' && cp -a '{remote}' '{bak}/{host}/{rest.replace('/', '_')}' || true",
        )
        if _is_unique(rest):
            print("PUT_SKIP unique", host, rest)
            continue
        sftp.put(str(path), remote)
        _run(client, f"chown www:www '{remote}'")
        n += 1
        print("PUT", remote)
    sftp.close()
    put_api_secrets(client)
    fix_api_nginx(client)
    client.close()
    print("PUT_DONE", n, "backup", bak)


def verify() -> None:
    from urllib.error import HTTPError
    from urllib.request import HTTPRedirectHandler, HTTPSHandler, Request, build_opener

    class NoRedir(HTTPRedirectHandler):
        def redirect_request(self, *a, **k):
            return None

    opener = build_opener(NoRedir(), HTTPSHandler())
    checks = [
        ("https://litbuy.at/", "Käufer in Österreich"),
        ("https://litbuy.at/", 'name="q"'),
        ("https://litbuy.at/", "Österreichische Post"),
        ("https://litbuy.at/", "cb-head"),
        ("https://litbuy.at/", 'action="https://w2clinks.com/spreadsheet/"'),
        ("https://litbuyspreadsheet.it/", "acquirenti in Italia"),
        ("https://litbuyspreadsheet.it/", "Poste Italiane"),
        ("https://litbuyspreadsheets.ca/", "Canadian Buyers"),
        ("https://litbuyspreadsheets.ca/", "Canada Post"),
        ("https://litbuyspreadsheets.us/", "US Buyers"),
        ("https://litbuyspreadsheets.us/", "USPS"),
        ("https://litbuyspreadsheet.me.uk/", "UK Buyers"),
        ("https://litbuyspreadsheet.me.uk/", "Royal Mail"),
        ("https://litspreadsheet.fr/", "acheteurs en France"),
        ("https://litspreadsheet.fr/", "La Poste"),
        ("https://litbuyspreadsheets.es/", "compradores en España"),
        ("https://litbuyspreadsheets.nl/", "kopers in Nederland"),
        ("https://litbuyspreadsheets.nl/", "PostNL"),
        ("https://litbuyspreadsheet.eu/", "Independent Index"),
        ("https://litbuy.at/litbuy-coupons/", "LitBuy"),
    ]
    for url, needle in checks:
        req = Request(url, headers={"User-Agent": "litbuy-dest/1.0"})
        try:
            with opener.open(req, timeout=22) as resp:
                raw = resp.read().decode("utf-8", "replace")
                ok = True if needle is None else needle in raw
                print("VERIFY", resp.status, url, "OK" if ok else "MISS " + (needle or ""))
                if needle is None:
                    print("VERIFY_UNEXP_200", url)
        except HTTPError as exc:
            loc = exc.headers.get("Location") if exc.headers else ""
            print("VERIFY", exc.code, url, loc)
        except Exception as exc:  # noqa: BLE001
            print("VERIFY_ERR", url, type(exc).__name__, str(exc)[:120])
    for url in (
        "https://litbuy.at/litbuy-coupons/",
        "https://litbuy.at/post-at-sendungsverfolgung/",
        "https://litbuyspreadsheets.ca/cbsa-import-canada/",
        "https://litbuyspreadsheet.it/dogana-poste-italiane/",
        "https://litbuyspreadsheet.eu/",
    ):
        req = Request(url, headers={"User-Agent": "litbuy-dest/1.0"})
        try:
            with opener.open(req, timeout=22) as resp:
                raw = resp.read().decode("utf-8", "replace")
                smashed = 'class="cb-head' in raw or 'class="cb-head ' in raw
                print("VERIFY_UNIQUE", resp.status, url, "SMASHED" if smashed else "CLEAN")
        except Exception as exc:  # noqa: BLE001
            print("VERIFY_UNIQUE_ERR", url, type(exc).__name__, str(exc)[:120])
    for host in ORDER:
        url = f"https://{host}/"
        req = Request(url, headers={"User-Agent": "litbuy-dest/1.0"})
        try:
            with opener.open(req, timeout=22) as resp:
                raw = resp.read().decode("utf-8", "replace")
                bad = (
                    'class="lmi"' in raw
                    or 'id="lang-grid"' in raw
                    or 'data-t="mt"' in raw
                    or "function openLM(){pL=" in raw
                )
                print("VERIFY_MODAL", resp.status, url, "GONE" if not bad else "STILL_PRESENT")
        except Exception as exc:  # noqa: BLE001
            print("VERIFY_MODAL_ERR", url, type(exc).__name__, str(exc)[:120])
    for twin, dest in TWINS_KEEP.items():
        url = f"https://{twin}/"
        req = Request(url, headers={"User-Agent": "litbuy-dest/1.0"})
        try:
            with opener.open(req, timeout=22) as resp:
                print("VERIFY_UNEXP_200", twin, resp.status)
        except HTTPError as exc:
            loc = exc.headers.get("Location") if exc.headers else ""
            ok = exc.code in (301, 302, 308) and dest in (loc or "")
            print("VERIFY_TWIN", exc.code, url, loc, "OK" if ok else "MISS " + dest)
        except Exception as exc:  # noqa: BLE001
            print("VERIFY_ERR", url, type(exc).__name__, str(exc)[:120])
    verify_api()


def verify_api() -> None:
    from urllib.request import Request, urlopen

    for host in ORDER:
        for path, needle_q in (
            (f"https://{host}/api/products/?limit=2&page=1", None),
            (f"https://{host}/api/products/?q=sneakers&limit=2&page=1", "sneakers"),
        ):
            req = Request(
                path,
                headers={
                    "User-Agent": "Mozilla/5.0 (compatible; LitBuyDestVerify/1.0)",
                    "Accept": "application/json",
                },
            )
            try:
                with urlopen(req, timeout=22) as resp:
                    raw = resp.read().decode("utf-8", "replace")
                    data = json.loads(raw)
                    items = data.get("items") or data.get("products") or []
                    hrefs = [str(it.get("href") or it.get("target") or "") for it in items if isinstance(it, dict)]
                    w2c = sum(1 for h in hrefs if h.startswith("https://w2clinks.com/"))
                    print(
                        "VERIFY_API",
                        resp.status,
                        host,
                        "q=" + (needle_q or "-"),
                        "n=" + str(len(items)),
                        "w2c=" + str(w2c),
                        "found=" + str(data.get("found", "")),
                    )
                    if resp.status != 200 or not items or w2c == 0:
                        print("VERIFY_API_FAIL", host, path.split("?")[0])
            except Exception as exc:  # noqa: BLE001
                print("VERIFY_API_ERR", host, type(exc).__name__, str(exc)[:120])


def gsc_submit() -> None:
    if not Path(SA).is_file():
        print("GSC_SKIP no sa.json")
        return
    try:
        from google.oauth2 import service_account
        from googleapiclient.discovery import build
    except ImportError:
        import subprocess

        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "google-api-python-client", "google-auth", "-q"]
        )
        from google.oauth2 import service_account
        from googleapiclient.discovery import build

    creds = service_account.Credentials.from_service_account_file(
        SA, scopes=["https://www.googleapis.com/auth/webmasters"]
    )
    gsc = build("searchconsole", "v1", credentials=creds, cache_discovery=False)
    listed = {row["siteUrl"] for row in gsc.sites().list().execute().get("siteEntry", [])}
    for host in ORDER:
        site = f"sc-domain:{host}" if f"sc-domain:{host}" in listed else f"https://{host}/"
        feed = f"https://{host}/sitemap.xml"
        try:
            gsc.sitemaps().submit(siteUrl=site if site in listed else f"https://{host}/", feedpath=feed).execute()
            print("SITEMAP", host, site)
        except Exception as exc:  # noqa: BLE001
            print("SITEMAP_FAIL", host, type(exc).__name__, str(exc)[:180])
        time.sleep(0.35)


def main() -> None:
    cmd = sys.argv[1] if len(sys.argv) > 1 else "all"
    if cmd == "reclaim":
        reclaim_nginx()
    elif cmd == "generate":
        generate()
    elif cmd == "put":
        put()
    elif cmd == "verify":
        verify()
    elif cmd == "gsc":
        gsc_submit()
    elif cmd == "leftover":
        files = leftover_skin()
        put(files)
        verify()
    elif cmd == "reskin":
        files = reskin_overlay()
        put(files)
        verify()
    elif cmd == "all":
        reclaim_nginx()
        files = generate()
        put(files)
        verify()
        gsc_submit()
    else:
        raise SystemExit(f"unknown {cmd}")


if __name__ == "__main__":
    main()
