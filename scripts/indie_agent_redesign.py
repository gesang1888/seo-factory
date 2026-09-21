#!/usr/bin/env python3
"""Redesign 13 independent agent hubs after the spam-update P0 301s.

Restores nginx from .bak-spam-p0, writes unique 4-page hubs, and collapses
cookie-cutter URL variants onto those pages. Does not 301 anything to
w2clinks.com. Secrets stay in BT_KEY.
"""

from __future__ import annotations

import argparse
import html
import json
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from spam_update_p0 import Baota  # noqa: E402

AGENTS = json.loads((ROOT / "scripts" / "indie_agents.json").read_text())["agents"]
TEMPLATE_SLUG_HOSTS = {
    "boonspreadsheet.com",
    "eastmallspreadsheet.com",
    "gtspreadsheet.com",
    "pikospreadsheets.net",
    "fsbuyspreadsheets.com",
    "spanbuyspreadsheets.com",
    "pingubuyspreadsheet.net",
    "ossbuyspreadsheets.org",
    "goatedspreadsheet.com",
}


def esc(s: str) -> str:
    return html.escape(s, quote=True)


def css(site: dict) -> str:
    t = site["theme"]
    dark = t["layout"] in {"terminal", "runway", "billboard"}
    card = "#0f172a" if t["layout"] == "terminal" else ("#1c1c1c" if dark else "#ffffff")
    muted = "#7dd3fc" if t["layout"] == "terminal" else ("#a1a1aa" if dark else "#57534e")
    return f"""
:root {{ --bg:{t['bg']}; --ink:{t['ink']}; --accent:{t['accent']}; --card:{card}; --muted:{muted}; }}
* {{ box-sizing:border-box; }}
html,body {{ margin:0; background:var(--bg); color:var(--ink); font-family:{t['font']}; line-height:1.55; }}
a {{ color:var(--accent); }}
header,main,footer {{ max-width:76rem; margin:0 auto; padding:1rem 1.25rem; }}
nav {{ display:flex; flex-wrap:wrap; gap:.8rem 1.2rem; }}
.hero {{ padding:1.4rem 0 1rem; }}
.grid {{ display:grid; gap:1rem; grid-template-columns:repeat(auto-fit,minmax(16rem,1fr)); }}
.card {{ background:var(--card); color:inherit; padding:1rem 1.1rem; border:1px solid color-mix(in srgb, var(--ink) 16%, transparent); border-radius:1rem; }}
.cta {{ display:inline-block; background:var(--accent); color:#fff; text-decoration:none; padding:.7rem 1rem; border-radius:.7rem; font-weight:700; }}
.note {{ color:var(--muted); font-size:.92rem; }}
table {{ width:100%; border-collapse:collapse; }}
td,th {{ text-align:left; padding:.45rem .3rem; border-bottom:1px solid color-mix(in srgb, var(--ink) 14%, transparent); }}
ol {{ padding-left:1.2rem; }}
.layout-ledger .hero {{ border-left:6px solid var(--accent); padding-left:1rem; }}
.layout-dock header {{ display:flex; justify-content:space-between; gap:1rem; align-items:end; }}
.layout-terminal {{ letter-spacing:.01em; }}
.layout-terminal .card {{ border-radius:0; }}
.layout-fieldnotes .hero {{ max-width:40rem; }}
.layout-runway h1 {{ text-transform:uppercase; letter-spacing:.06em; }}
.layout-ticket .cta {{ border-radius:999px; }}
.layout-stencil h1 {{ font-stretch:condensed; }}
.layout-opsboard .grid {{ grid-template-columns:1.2fr .8fr; }}
.layout-relay nav {{ justify-content:space-between; }}
.layout-harbor {{ background-image:linear-gradient(180deg, transparent 0, color-mix(in srgb, var(--accent) 10%, transparent) 100%); }}
.layout-stamp h1 {{ font-weight:400; }}
.layout-channel .card {{ border-radius:.2rem; }}
.layout-billboard h1 {{ font-size:clamp(2rem,6vw,4rem); line-height:1.05; }}
@media (max-width:800px) {{ .layout-opsboard .grid {{ grid-template-columns:1fr; }} }}
""".strip()


def nav_html(site: dict) -> str:
    bits = []
    for label, href in site["nav"]:
        bits.append(f'<a href="{esc(href)}">{esc(label)}</a>')
    return "\n".join(bits)


def faq_html(site: dict) -> str:
    parts = ["<section><h2>Questions this hub actually answers</h2>"]
    for q, a in site["faq"]:
        parts.append(f"<h3>{esc(q)}</h3><p>{esc(a)}</p>")
    parts.append("</section>")
    return "\n".join(parts)


def jsonld(site: dict, page: str, url: str, name: str, desc: str) -> str:
    data = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "WebSite",
                "name": name,
                "url": f"https://{site['host']}/",
                "about": site["agent"],
            },
            {
                "@type": "WebPage",
                "name": name,
                "url": url,
                "description": desc,
                "isPartOf": {"@type": "WebSite", "url": f"https://{site['host']}/"},
            },
        ],
    }
    if page == "home":
        data["@graph"].append(
            {
                "@type": "FAQPage",
                "mainEntity": [
                    {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
                    for q, a in site["faq"]
                ],
            }
        )
    if page == "start":
        data["@graph"].append(
            {
                "@type": "HowTo",
                "name": site["start_title"],
                "step": [
                    {"@type": "HowToStep", "position": i, "text": step}
                    for i, step in enumerate(site["start_steps"], 1)
                ],
            }
        )
    return json.dumps(data, ensure_ascii=False, indent=2)


def shell(site: dict, title: str, desc: str, canonical: str, page: str, body: str) -> str:
    layout = site["theme"]["layout"]
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{esc(canonical)}">
<meta name="robots" content="index,follow">
<style>{css(site)}</style>
<script type="application/ld+json">{jsonld(site, page, canonical, title, desc)}</script>
</head>
<body class="layout-{esc(layout)}">
<header>
  <p class="note">{esc(site['agent'])} · independent hub · {esc(site['host'])}</p>
  <nav>{nav_html(site)}</nav>
</header>
<main>
{body}
</main>
<footer>
  <p class="note">Independent notes about {esc(site['agent'])}. Not {esc(site['agent'])}'s official site. Not a doorway to other agent domains. Educational shipping notes only — follow your destination's customs rules.</p>
</footer>
</body>
</html>
"""


def home_body(site: dict) -> str:
    cards = [
        ("Warehouse", site["warehouse"]),
        ("QC", site["qc"]),
        ("Who should skip it", site["who_not"]),
    ]
    card_html = "\n".join(
        f'<article class="card"><h2>{esc(h)}</h2><p>{esc(p)}</p></article>' for h, p in cards
    )
    extra = ""
    if site["theme"]["layout"] == "opsboard":
        extra = f'<aside class="card"><h2>Sister document</h2><p>QC pass/fail lives on <a href="https://bestlolobuyspreadsheet.com/">bestlolobuyspreadsheet.com</a>. This page stays on parcel SOP.</p></aside>'
    if site["theme"]["layout"] == "runway":
        extra = f'<aside class="card"><h2>Sister document</h2><p>Warehouse-to-tracking SOP lives on <a href="https://lolospreadsheet.com/">lolospreadsheet.com</a>. This page stays on QC triage.</p></aside>'
    return f"""
<section class="hero">
  <h1>{esc(site['home_h1'])}</h1>
  <p>{esc(site['lead'])}</p>
  <p>{esc(site['angle'])}</p>
  <p><a class="cta" href="{esc(site['register'])}">Open {esc(site['agent'])}</a></p>
</section>
<section class="grid">
{card_html}
{extra}
</section>
{faq_html(site)}
"""


def start_body(site: dict) -> str:
    steps = "\n".join(f"<li>{esc(s)}</li>" for s in site["start_steps"])
    return f"""
<section class="hero">
  <h1>{esc(site['start_title'])}</h1>
  <ol>{steps}</ol>
  <p><a class="cta" href="{esc(site['register'])}">Register on {esc(site['agent'])}</a></p>
</section>
"""


def ship_body(site: dict) -> str:
    pts = "\n".join(f"<li>{esc(s)}</li>" for s in site["ship_points"])
    return f"""
<section class="hero">
  <h1>{esc(site['ship_title'])}</h1>
  <p>{esc(site['ship_body'])}</p>
  <ul>{pts}</ul>
  <p class="note">Rates move. The live quote inside {esc(site['agent'])} is the number you pay. This page does not calculate declared value for you.</p>
</section>
"""


def coupon_body(site: dict) -> str:
    rows = "\n".join(
        f"<tr><th>{esc(k)}</th><td>{esc(v)}</td></tr>" for k, v in site["offers"]
    )
    inv = f"<p>{esc(site['invite_label'])}: <strong>{esc(site['invite'])}</strong></p>" if site.get("invite") else ""
    return f"""
<section class="hero">
  <h1>{esc(site['coupon_title'])}</h1>
  {inv}
  <p>{esc(site['coupon_body'])}</p>
  <table>{rows}</table>
  <p><a class="cta" href="{esc(site['register'])}">Apply it on {esc(site['agent'])}</a></p>
</section>
"""


def robots_txt(site: dict) -> str:
    extra = ""
    if site["host"] == "fishgoospreadsheet.net":
        extra = "Disallow: /fishgoo-\n"
    if site["host"] in {"lolospreadsheet.com", "bestlolobuyspreadsheet.com"}:
        extra += "Disallow: /brand/\nDisallow: /category/\n"
    return f"""User-agent: *
Allow: /
Allow: /start/
Allow: /shipping/
Allow: /coupons/
Disallow: /api/
Disallow: /assets/
{extra}
Sitemap: https://{site['host']}/sitemap.xml
"""


def sitemap_xml(site: dict) -> str:
    urls = ["/", "/start/", "/shipping/", "/coupons/"]
    body = "\n".join(
        f"  <url><loc>https://{site['host']}{u}</loc><changefreq>weekly</changefreq></url>"
        for u in urls
    )
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{body}
</urlset>
"""


def ia_collapse_conf(site: dict) -> str:
    slug = site["slug"]
    host = site["host"]
    lines = [
        f"# indie-agent-redesign: collapse cookie-cutter variants on {host}",
        f"rewrite ^/{slug}-spreadsheet(?:-2026)?/?$ / permanent;",
        f"rewrite ^/{slug}-shoes-spreadsheet/?$ / permanent;",
        f"rewrite ^/{slug}-community/?$ / permanent;",
        f"rewrite ^/{slug}-coupons/?$ /coupons/ permanent;",
        f"rewrite ^/{slug}-invite-code/?$ /coupons/ permanent;",
        f"rewrite ^/{slug}-shipping-guide/?$ /shipping/ permanent;",
        f"rewrite ^/{slug}-qc-guide/?$ /shipping/ permanent;",
        f"rewrite ^/{slug}-refund-guide/?$ /shipping/ permanent;",
        f"rewrite ^/how-to-use-{slug}/?$ /start/ permanent;",
        f"rewrite ^/is-{slug}-legit/?$ /start/ permanent;",
        "rewrite ^/blog/?$ / permanent;",
    ]
    if host == "fishgoospreadsheet.net":
        lines += [
            "rewrite ^/beginner-guide\\.html$ /start/ permanent;",
            "rewrite ^/coupons\\.html$ /coupons/ permanent;",
            'location ~ ^/fishgoo-[a-z0-9-]+-spreadsheet { add_header X-Robots-Tag "noindex, follow" always; try_files $uri $uri/ $uri/index.html =404; }',
        ]
    if host in {"lolospreadsheet.com", "bestlolobuyspreadsheet.com"}:
        lines += [
            "rewrite ^/spreadsheet/?$ / permanent;",
            "rewrite ^/guides/?$ /start/ permanent;",
            'location ^~ /brand/ { add_header X-Robots-Tag "noindex, follow" always; try_files $uri $uri/ $uri/index.html =404; }',
            'location ^~ /category/ { add_header X-Robots-Tag "noindex, follow" always; try_files $uri $uri/ $uri/index.html =404; }',
        ]
    if host == "itaobuyspreadsheet.net":
        lines += [
            "rewrite ^/itaobuy-shipping-lines-2026\\.html$ /shipping/ permanent;",
            "rewrite ^/itaobuy-coupon-tracker-2026\\.html$ /coupons/ permanent;",
        ]
    return "\n".join(lines) + "\n"


def write_overlay(site: dict) -> Path:
    out = ROOT / "sites" / site["host"] / "overlay"
    pages = {
        "index.html": shell(
            site,
            site["home_title"],
            site["lead"][:160],
            f"https://{site['host']}/",
            "home",
            home_body(site),
        ),
        "start/index.html": shell(
            site,
            site["start_title"],
            f"How to place a first {site['agent']} order.",
            f"https://{site['host']}/start/",
            "start",
            start_body(site),
        ),
        "shipping/index.html": shell(
            site,
            site["ship_title"],
            site["ship_body"][:160],
            f"https://{site['host']}/shipping/",
            "shipping",
            ship_body(site),
        ),
        "coupons/index.html": shell(
            site,
            site["coupon_title"],
            site["coupon_body"][:160],
            f"https://{site['host']}/coupons/",
            "coupons",
            coupon_body(site),
        ),
        "robots.txt": robots_txt(site),
        "sitemap.xml": sitemap_xml(site),
        "nginx-ia-collapse.conf": ia_collapse_conf(site),
    }
    for rel, data in pages.items():
        path = out / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(data)
    return out


TYPESENSE_PROXY_RE = re.compile(
    r"\n\s*location = /api/typesense-search\.php \{.*?\n\s*\}\n",
    re.S,
)
TYPESENSE_GONE = """
    location = /api/typesense-search.php {
        add_header X-Robots-Tag "noindex, nofollow" always;
        return 404;
    }
"""


def restore_nginx(bt: Baota, host: str) -> dict:
    nginx = f"/www/server/panel/vhost/nginx/{host}.conf"
    bak = nginx + ".bak-spam-p0"
    original = bt.get(bak)
    if not original:
        return {"status": False, "msg": "missing bak"}
    # Safety: never restore a copy that still 301s the whole site to w2clinks.
    if "return 301 https://w2clinks.com/" in original and "try_files" not in original:
        return {"status": False, "msg": "bak itself is a w2clinks 301"}
    restored = TYPESENSE_PROXY_RE.sub("\n" + TYPESENSE_GONE, original)
    return bt.put(nginx, restored)


def deploy(bt: Baota, dry_run: bool = False) -> None:
    for site in AGENTS:
        host = site["host"]
        overlay = write_overlay(site)
        mapping = {
            f"/www/wwwroot/{host}/index.html": (overlay / "index.html").read_text(),
            f"/www/wwwroot/{host}/start/index.html": (overlay / "start/index.html").read_text(),
            f"/www/wwwroot/{host}/shipping/index.html": (overlay / "shipping/index.html").read_text(),
            f"/www/wwwroot/{host}/coupons/index.html": (overlay / "coupons/index.html").read_text(),
            f"/www/wwwroot/{host}/robots.txt": (overlay / "robots.txt").read_text(),
            f"/www/wwwroot/{host}/sitemap.xml": (overlay / "sitemap.xml").read_text(),
            f"/www/server/panel/vhost/nginx/extension/{host}/ia-collapse.conf": (
                overlay / "nginx-ia-collapse.conf"
            ).read_text(),
        }
        if dry_run:
            print(host, "dry-run", len(mapping), "files")
            continue
        print("restore nginx", host, restore_nginx(bt, host))
        for path, data in mapping.items():
            print("put", path, bt.put(path, data).get("msg", "")[:80])
    if not dry_run:
        print("reload", bt.reload_nginx())


def jaccard_report() -> None:
    toks = {}
    for site in AGENTS:
        text = " ".join(
            [
                site["lead"],
                site["angle"],
                site["warehouse"],
                site["qc"],
                site["who_not"],
                site["ship_body"],
                site["coupon_body"],
            ]
        ).lower()
        toks[site["host"]] = set(w for w in text.replace("'", "").split() if len(w) > 3)
    print("pairwise Jaccard on unique copy (expect << 0.45):")
    hosts = [s["host"] for s in AGENTS]
    worst = 0.0
    for i, a in enumerate(hosts):
        for b in hosts[i + 1 :]:
            A, B = toks[a], toks[b]
            j = len(A & B) / len(A | B)
            worst = max(worst, j)
            if j >= 0.22:
                print(f"  {j:.2f} {a} vs {b}")
    print("max", round(worst, 3))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-overlays", action="store_true")
    parser.add_argument("--jaccard", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()
    if args.write_overlays or args.dry_run or args.apply:
        for site in AGENTS:
            write_overlay(site)
            print("wrote", site["host"])
    if args.jaccard:
        jaccard_report()
    if args.apply or args.dry_run:
        key = os.environ.get("BT_KEY", "")
        if not key:
            raise SystemExit("BT_KEY is required for --apply/--dry-run")
        deploy(Baota(key), dry_run=args.dry_run)
        return 0
    if not (args.write_overlays or args.jaccard):
        print("Pass --write-overlays, --jaccard, --dry-run or --apply")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
