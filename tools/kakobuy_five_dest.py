#!/usr/bin/env python3
"""Deepen the five Kakobuy dest desks to the kakobuy.co.uk cluster.

Order: reclaim FR/NL 301 (nginx), then homepage SERP title + WebSite keywords,
then thicken keep inners (FI → CA → ES → FR → NL). Does not smash unique
/ohje/. Does not coach a declared value. GSC: sitemap submit only.
"""
from __future__ import annotations

import json
import os
import re
import sys
import time
from datetime import datetime, timezone
from html import escape, unescape
from pathlib import Path

_TOOLS = Path(__file__).resolve().parent
if str(_TOOLS) not in sys.path:
    sys.path.insert(0, str(_TOOLS))
from desk_template import (
    cluster_keywords,
    cluster_title_serp,
    faq_ld,
    inject_jsonld,
    website_ld,
)
from kakobuy_five_copy import (  # noqa: E402
    inner_keywords,
    inner_serp_title,
    sections_for as copy_sections,
    wrap_copy,
)

ROOT = Path(__file__).resolve().parents[1]
STAMP = "20261101"
TODAY = "2026-11-01"
MARKER = f'data-kakobuy-five="{STAMP}"'
_SA_CANDIDATES = [
    os.environ.get("GSC_SA_JSON", ""),
    "/tmp/hipobuy-creds/sa.json",
    "/cursor/stores/self/internal/gsc-sa.json",
]
SA = next((p for p in _SA_CANDIDATES if p and Path(p).is_file()), "/tmp/hipobuy-creds/sa.json")
BAK_NGINX = "/www/backup/portfolio-step5-phaseb-20261026-150339"

HOSTS = {
    "kakobuy.fi": {
        "key": "fi",
        "dest": "FI",
        "loc": "fi",
        "lang": "fi-FI",
        "label": "Suomi",
        "customs": "Tulli",
        "customs_url": "https://tulli.fi/",
        "post": "Posti",
        "city": "00100 Helsinki",
        "pages": {
            "spreadsheet": "kakobuy-spreadsheet",
            "finds": "kakobuy-finds",
            "qc": "kakobuy-qc",
            "shipping": "kakobuy-toimitus",
            "legal": "kakobuy-kokemuksia",
            "faq": "faq",
        },
        "skip": {"ohje"},
        "canon": [("kakobuy-shipping", "kakobuy-toimitus")],
    },
    "kakospreadsheet.ca": {
        "key": "ca",
        "dest": "CA",
        "loc": "en",
        "lang": "en-CA",
        "label": "Canada",
        "customs": "CBSA",
        "customs_url": "https://www.cbsa-asfc.gc.ca/",
        "post": "Canada Post",
        "city": "postal code A1A 1A1",
        "pages": {
            "spreadsheet": "kakobuy-spreadsheet",
            "finds": "kakobuy-finds",
            "qc": "kakobuy-qc",
            "shipping": "kakobuy-shipping-to-canada",
            "legal": "is-kakobuy-legit",
            "guide": "kakobuy-guide",
            "faq": "kakobuy-faq",
        },
        "skip": set(),
        "canon": [("kakobuy-shipping", "kakobuy-shipping-to-canada")],
    },
    "kakospreadsheet.es": {
        "key": "es",
        "dest": "ES",
        "loc": "es",
        "lang": "es-ES",
        "label": "España",
        "customs": "Agencia Tributaria",
        "customs_url": "https://sede.agenciatributaria.gob.es/",
        "post": "Correos",
        "city": "código postal de cinco dígitos",
        "pages": {
            "spreadsheet": "kakobuy-spreadsheet",
            "finds": "kakobuy-finds",
            "qc": "kakobuy-qc",
            "shipping": "envio-kakobuy-espana",
            "legal": "kakobuy-opiniones",
            "guide": "kakobuy-guide",
            "faq": "kakobuy-faq",
        },
        "skip": set(),
        "canon": [("kakobuy-shipping", "envio-kakobuy-espana")],
    },
    "kakospreadsheet.fr": {
        "key": "fr",
        "dest": "FR",
        "loc": "fr",
        "lang": "fr-FR",
        "label": "France",
        "customs": "douane.gouv.fr",
        "customs_url": "https://www.douane.gouv.fr/",
        "post": "Colissimo",
        "city": "code postal à cinq chiffres, pas un code belge",
        "pages": {
            "spreadsheet": "kakobuy-spreadsheet",
            "finds": "kakobuy-finds",
            "qc": "kakobuy-qc",
            "shipping": "livraison-kakobuy",
            "legal": "avis-kakobuy",
            "guide": "kakobuy-guide",
            "faq": "kakobuy-faq",
        },
        "skip": set(),
        "canon": [("kakobuy-shipping", "livraison-kakobuy")],
    },
    "kakospreadsheet.nl": {
        "key": "nl",
        "dest": "NL",
        "loc": "nl",
        "lang": "nl-NL",
        "label": "Nederland",
        "customs": "Belastingdienst Douane",
        "customs_url": "https://www.belastingdienst.nl/wps/wcm/connect/nl/douane/",
        "post": "PostNL / DHL",
        "city": "Nederlandse postcode 1234 AB",
        "pages": {
            "spreadsheet": "kakobuy-spreadsheet",
            "finds": "kakobuy-finds",
            "qc": "kakobuy-qc",
            "shipping": "kakobuy-verzending",
            "legal": "kakobuy-ervaringen",
            "guide": "kakobuy-guide",
            "faq": "kakobuy-faq",
        },
        "skip": set(),
        "canon": [("kakobuy-shipping", "kakobuy-verzending")],
    },
}

ORDER = [
    "kakobuy.fi",
    "kakospreadsheet.ca",
    "kakospreadsheet.es",
    "kakospreadsheet.fr",
    "kakospreadsheet.nl",
]


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
    """Restore dest vhosts for FR/NL (undo Phase B catch-all 301 to kakobuydocs.com)."""
    client = _connect()
    stamp = time.strftime("%Y%m%d-%H%M%S")
    bak = f"/www/backup/kakobuy-five-reclaim-{stamp}"
    print(_run(client, f"mkdir -p '{bak}'"))
    for host in ("kakospreadsheet.fr", "kakospreadsheet.nl"):
        live = f"/www/server/panel/vhost/nginx/{host}.conf"
        src = f"{BAK_NGINX}/{host}.conf.bak"
        head = _run(client, f"head -c 800 '{live}'")
        sunset = "kakobuydocs.com" in head and "return 301" in head
        if not sunset:
            print("SKIP_RESTORE", host, "already dest vhost")
            continue
        print(_run(client, f"cp -a '{live}' '{bak}/{host}.conf.before'"))
        print(_run(client, f"cp -a '{src}' '{live}'"))
        print("RESTORE", host)
    # FI: serve /faq/ instead of 301 to /ohje/
    gsc = "/www/server/panel/vhost/nginx/extension/kakobuy.fi/gsc-redirects.conf"
    raw = _run(client, f"cat '{gsc}'")
    patched = re.sub(
        r"location\s*=\s*/faq/?\s*\{[^}]*kakobuy\.fi/ohje/?[^}]*\}\s*",
        "",
        raw,
        flags=re.I,
    )
    if patched != raw:
        print(_run(client, f"cp -a '{gsc}' '{bak}/gsc-redirects.conf.before'"))
        sftp = client.open_sftp()
        with sftp.open(gsc, "w") as fh:
            fh.write(patched)
        sftp.close()
        print("PATCH FI faq 301 removed")
    else:
        print("FI_FAQ_REDIRECT", "unchanged" if "/faq" in raw else "already clear")
    print(_run(client, "nginx -t && nginx -s reload"))
    client.close()
    print("RECLAIM_NGINX", bak)


def sections_for(kind: str, d: dict, host: str) -> tuple[str, str, list[tuple[str, list[str]]]]:
    return copy_sections(kind, d, host)


def _nav(d: dict) -> str:
    labels = {
        "spreadsheet": "Spreadsheet",
        "finds": "Finds",
        "qc": "QC",
        "shipping": {"en": "Shipping", "es": "Envío", "fr": "Livraison", "nl": "Verzending", "fi": "Toimitus"}[d["loc"]],
        "legal": {"en": "Is it legal?", "es": "¿Es legal?", "fr": "Est-ce légal ?", "nl": "Is het legaal?", "fi": "Onko se laillista?"}[d["loc"]],
        "guide": {"en": "Guide", "es": "Guía", "fr": "Guide", "nl": "Gids", "fi": "Ohje"}[d["loc"]],
        "faq": "FAQ",
    }
    items = []
    for kind, slug in d["pages"].items():
        items.append(f'<li><a href="/{slug}/">{escape(labels.get(kind, kind))}</a></li>')
    if d["loc"] == "fi":
        items.append('<li><a href="/ohje/">Ohje</a></li>')
    return '<ul class="cluster-links">' + "".join(items) + "</ul>"


def render_article(host: str, kind: str, d: dict) -> str:
    h1, lead, secs = sections_for(kind, d, host)
    loc = d["loc"]
    img, alt = {
        "spreadsheet": ("/media/official-home-20261001.jpg", "Kakobuy"),
        "finds": ("/img/cat/sneakers.jpg", "Kakobuy finds"),
        "qc": ("/media/help-restricted-20261001.jpg", "Kakobuy QC"),
        "shipping": ("/media/estimator-20261001.jpg", "Kakobuy shipping"),
        "legal": ("/media/official-home-20261001.jpg", "Kakobuy"),
        "guide": ("/media/official-home-20261001.jpg", "Kakobuy"),
        "faq": ("/img/cat/hoodie.jpg", "Kakobuy FAQ"),
    }.get(kind, ("/media/official-home-20261001.jpg", "Kakobuy"))
    chunks = [
        f'<article class="cluster-page" data-spreadsheet-cluster="20261030" {MARKER} data-kakobuy-deepen="{STAMP}" data-kind="{escape(kind)}">',
        f"<h1>{escape(h1)}</h1>",
        f'<p class="lead">{escape(lead)}</p>',
        f'<figure class="kb-illust"><img src="{img}" alt="{escape(alt)}" width="1400" height="900" loading="lazy" decoding="async"></figure>',
    ]
    if kind == "finds":
        cells = "".join(
            f'<img src="{u}" alt="{a}" width="560" height="560" loading="lazy">'
            for u, a in (
                ("/img/cat/sneakers.jpg", "Sneakers"),
                ("/img/cat/hoodie.jpg", "Hoodie"),
                ("/img/cat/bags.jpg", "Bags"),
            )
        )
        chunks.append(f'<div class="kb-illust-grid">{cells}</div>')
    for h2, paras in secs:
        chunks.append(f"<h2>{escape(h2)}</h2>")
        for p in paras:
            chunks.append(f"<p>{escape(p)}</p>")
    h2nav = {
        "en": "Spreadsheet / finds / QC / Shipping",
        "es": "Spreadsheet / finds / QC / Envío",
        "fr": "Spreadsheet / finds / QC / Livraison",
        "nl": "Spreadsheet / finds / QC / Verzending",
        "fi": "Spreadsheet / finds / QC / Toimitus",
    }[loc]
    chunks.append(f"<h2>{escape(h2nav)}</h2>")
    chunks.append(_nav(d))
    cta = {
        "en": f"Shop and pay on kakobuy.com. Prices on this page are shown in local currency for {d['label']}.",
        "es": f"Compra y paga en kakobuy.com. Los precios de esta página se muestran en moneda local para {d['label']}.",
        "fr": f"Commande et paiement sur kakobuy.com. Les prix de cette page sont affichés dans la monnaie locale pour {d['label']}.",
        "nl": f"Bestellen en betalen op kakobuy.com. Prijzen op deze pagina staan in lokale valuta voor {d['label']}.",
        "fi": f"Tilaa ja maksa osoitteessa kakobuy.com. Hinnat tällä sivulla näytetään paikallisessa valuutassa.",
    }[loc]
    chunks.append(f'<p class="kb-cta">{escape(cta)}</p>')
    chunks.append("</article>")
    return "\n".join(chunks) + "\n"


MAIN_RE = re.compile(r"(<main\b[^>]*>)(.*?)(</main>)", re.I | re.S)


def swap_main(html: str, inner: str) -> str:
    if not MAIN_RE.search(html):
        raise ValueError("missing <main>")
    return MAIN_RE.sub(lambda m: m.group(1) + "\n" + inner + m.group(3), html, count=1)


def upsert_meta(html: str, name: str, content: str) -> str:
    tag = f'<meta name="{name}" content="{escape(content)}">'
    if re.search(rf'<meta\s+name="{name}"', html, re.I):
        return re.sub(rf'<meta\s+name="{name}"[^>]*>', tag, html, count=1, flags=re.I)
    return html.replace("</head>", tag + "\n</head>", 1)


def patch_cluster_nav(html: str, d: dict) -> str:
    labels = {
        "spreadsheet": "Spreadsheet",
        "finds": "Finds",
        "qc": "QC",
        "shipping": {"en": "Shipping", "es": "Envío", "fr": "Livraison", "nl": "Verzending", "fi": "Toimitus"}[d["loc"]],
        "legal": {"en": "Is it legal?", "es": "¿Es legal?", "fr": "Est-ce légal ?", "nl": "Is het legaal?", "fi": "Onko se laillista?"}[d["loc"]],
        "guide": {"en": "Guide", "es": "Guía", "fr": "Guide", "nl": "Gids", "fi": "Ohje"}[d["loc"]],
        "faq": "FAQ",
    }
    links = []
    for kind, slug in d["pages"].items():
        links.append(f'<a href="/{slug}/">{escape(labels.get(kind, kind))}</a>')
    if d["loc"] == "fi":
        links.append('<a href="/ohje/">Ohje</a>')
    inner = "".join(links)
    return re.sub(
        r'<nav class="cluster-nav"[^>]*>.*?</nav>',
        f'<nav class="cluster-nav" data-spreadsheet-cluster="20261030" aria-label="Kakobuy">{inner}</nav>',
        html,
        count=1,
        flags=re.I | re.S,
    )


def patch_home(host: str, d: dict) -> Path:
    path = overlay(host) / "index.html"
    html = path.read_text(encoding="utf-8")
    serp = cluster_title_serp("Kakobuy", d["dest"], d["loc"], d["label"])
    kws = cluster_keywords("Kakobuy", d["dest"], d["loc"], d["label"])
    html = patch_cluster_nav(html, d)
    html = re.sub(r"<title>[\s\S]*?</title>", f"<title>{escape(serp)}</title>", html, count=1, flags=re.I)
    html = re.sub(
        r'(<meta\s+property="og:title"\s+content=")[^"]*(")',
        rf"\1{escape(serp)}\2",
        html,
        count=1,
        flags=re.I,
    )
    # Keep H1 unsuffixed (kakobuy.co.uk pattern).
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
                brand="Kakobuy",
                host=host,
                keywords=kws,
            ),
        )
        html = html.replace("<body", f"<body {MARKER}", 1)
    path.write_text(html, encoding="utf-8")
    return path


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
        return f'<script type="application/ld+json">{json.dumps(data, ensure_ascii=False)}</script>'

    return repl


def deepen_inner(host: str, kind: str, d: dict) -> Path | None:
    slug = d["pages"].get(kind)
    if not slug or slug in d.get("skip", set()):
        return None
    path = overlay(host) / slug / "index.html"
    if not path.is_file():
        print("MISSING", host, slug)
        return None
    html = path.read_text(encoding="utf-8")
    inner = render_article(host, kind, d)
    html = swap_main(html, inner)
    h1, lead, secs = sections_for(kind, d, host)
    serp = inner_serp_title(kind, d["loc"], d["label"])
    kws = inner_keywords(kind, d["dest"])
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
    path.write_text(html, encoding="utf-8")
    return path


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


def wrap_old_shipping(host: str, d: dict) -> Path | None:
    keep_slug = d["pages"]["shipping"]
    src = overlay(host) / keep_slug / "index.html"
    if not src.is_file():
        return None
    dest_dir = overlay(host) / "kakobuy-shipping"
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest = dest_dir / "index.html"
    html = src.read_text(encoding="utf-8")
    h1, lead, secs = wrap_copy(host, d, keep_slug)
    img = "/media/estimator-20261001.jpg"
    chunks = [
        f'<article class="cluster-page" {MARKER} data-kind="shipping-wrap">',
        f"<h1>{escape(h1)}</h1>",
        f'<p class="lead">{escape(lead)}</p>',
        f'<figure class="kb-illust"><img src="{img}" alt="Kakobuy" width="1400" height="900" loading="lazy" decoding="async"></figure>',
    ]
    for h2, paras in secs:
        chunks.append(f"<h2>{escape(h2)}</h2>")
        for p in paras:
            chunks.append(f"<p>{escape(p)}</p>")
    chunks.append(_nav(d))
    chunks.append("</article>\n")
    html = swap_main(html, "\n".join(chunks))
    keep_url = f"https://{host}/{keep_slug}/"
    wrap_url = f"https://{host}/kakobuy-shipping/"
    html = re.sub(r"<title>[\s\S]*?</title>", f"<title>{escape(h1)}</title>", html, flags=re.I)
    html = re.sub(
        r'(<meta\s+property="og:title"\s+content=")[^"]*(")',
        rf"\1{escape(h1)}\2",
        html,
        count=1,
        flags=re.I,
    )
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
    dest.write_text(html, encoding="utf-8")
    print("WRAP", host, "kakobuy-shipping ->", keep_slug)
    return dest


def bump_sitemap(host: str, d: dict) -> None:
    path = overlay(host) / "sitemap.xml"
    if not path.is_file():
        return
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


def generate() -> list[Path]:
    written: list[Path] = []
    for host in ORDER:
        d = HOSTS[host]
        ohje = overlay(host) / "ohje" / "index.html"
        ohje_hash = ohje.read_bytes() if ohje.is_file() else None
        written.append(patch_home(host, d))
        print("HOME", host, cluster_title_serp("Kakobuy", d["dest"], d["loc"], d["label"]))
        for kind in d["pages"]:
            p = deepen_inner(host, kind, d)
            if p:
                written.append(p)
                print("INNER", host, kind, p.relative_to(ROOT))
        wrap = wrap_old_shipping(host, d)
        if wrap:
            written.append(wrap)
        bump_sitemap(host, d)
        sm = overlay(host) / "sitemap.xml"
        if sm.is_file():
            written.append(sm)
        if ohje_hash is not None and ohje.read_bytes() != ohje_hash:
            raise SystemExit(f"refused to smash unique /ohje/ on {host}")
    return written


def put(files: list[Path] | None = None) -> None:
    if files is None:
        files = generate()
    client = _connect()
    stamp = time.strftime("%Y%m%d-%H%M%S")
    bak = f"/www/backup/kakobuy-five-dest-{stamp}"
    print(_run(client, f"mkdir -p '{bak}'"))
    sftp = client.open_sftp()
    n = 0
    for path in files:
        rel = path.relative_to(ROOT / "sites").as_posix()  # host/overlay/...
        host = rel.split("/", 1)[0]
        rest = path.relative_to(overlay(host)).as_posix()
        remote = f"/www/wwwroot/{host}/{rest}"
        _run(client, f"mkdir -p '{str(Path(remote).parent)}'")
        _run(client, f"test -f '{remote}' && mkdir -p '{bak}/{host}' && cp -a '{remote}' '{bak}/{host}/{rest.replace('/', '_')}' || true")
        sftp.put(str(path), remote)
        _run(client, f"chown www:www '{remote}'")
        n += 1
        print("PUT", remote)
    sftp.close()
    client.close()
    print("PUT_DONE", n, "backup", bak)


def verify() -> None:
    from urllib.request import Request, build_opener, HTTPSHandler, HTTPRedirectHandler

    class NoRedir(HTTPRedirectHandler):
        def redirect_request(self, *a, **k):
            return None

    opener = build_opener(NoRedir(), HTTPSHandler())
    checks = [
        ("https://kakospreadsheet.fr/", "Kakobuy Spreadsheet pour acheteurs en France"),
        ("https://kakospreadsheet.nl/", "Kakobuy Spreadsheet voor kopers in Nederland"),
        ("https://kakobuy.fi/", "Finds ja QC"),
        ("https://kakospreadsheet.ca/", "Best Finds"),
        ("https://kakospreadsheet.es/", "Mejores finds y QC"),
        ("https://kakobuy.fi/faq/", "FAQ"),
        ("https://kakobuy.fi/kakobuy-spreadsheet/", "spreadsheet"),
        ("https://kakobuy.fi/ohje/", "Ohje"),
        ("https://kakospreadsheet.fr/kakobuy-finds/", "finds"),
        ("https://kakospreadsheet.fr/kakobuy-faq/", "FAQPage"),
        ("https://kakospreadsheet.nl/kakobuy-verzending/", "verzending"),
        ("https://kakospreadsheet.nl/kakobuy-guide/", "Gids"),
        ("https://kakospreadsheet.es/envio-kakobuy-espana/", "Envío"),
        ("https://kakospreadsheet.ca/kakobuy-shipping-to-canada/", "Canada Post"),
        ("https://kakospreadsheet.ca/kakobuy-spreadsheet/", "kakobuy trusted sellers"),
        ("https://kakobuy.fi/kakobuy-spreadsheet/", "kakobuy spreadsheet suomi"),
        ("https://kakospreadsheet.nl/", "aria-label=\"Kakobuy\""),
        ("https://kakobuy.fi/kakobuy-shipping/", "kakobuy-toimitus"),
        ("https://kakospreadsheet.ca/kakobuy-shipping/", "kakobuy-shipping-to-canada"),
    ]
    for url, needle in checks:
        try:
            r = opener.open(Request(url, headers={"User-Agent": "kakobuy-five/1.0"}), timeout=20)
            body = r.read().decode("utf-8", "replace")
            desk = r.headers.get("X-Desk")
            ok = needle.lower() in body.lower()
            print("VERIFY", r.status, url, "desk", desk, "hit", ok, "five", MARKER.split("=")[0] in body)
        except Exception as exc:
            from urllib.error import HTTPError

            if isinstance(exc, HTTPError):
                print("VERIFY", exc.code, url, exc.headers.get("Location"))
            else:
                print("VERIFY_ERR", url, type(exc).__name__, str(exc)[:120])


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
