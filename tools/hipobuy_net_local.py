#!/usr/bin/env python3
"""Surgical #local insert on hipobuyspreadsheet.net homepage only.

Live / is EyouCMS (`template/pc/index.htm`), not a Georgia dest skin.
Do not overwrite ranked news/category html. Do not re-inject dest-template
("not a customs territory"). Keep hipo / hippo buy spellings.
"""
from __future__ import annotations

import re
from pathlib import Path

_TOOLS = Path(__file__).resolve().parent
NET_HOST = "hipobuyspreadsheet.net"
REMOTE_INDEX = f"/www/wwwroot/{NET_HOST}/index.html"
REMOTE_TEMPLATE = f"/www/wwwroot/{NET_HOST}/template/pc/index.htm"
HERO_END = "    </section>\n\n    <!-- ============ CATEGORIES ============ -->"

HUB_LOCAL = """
<section class="container sg-sec" id="local" data-hub-reclaim="20261103">
  <h2>How to use this HipoBuy spreadsheet</h2>
  <p class="ssub">Search 8,600+ finds. Cite the dated JSON. Check coupons and QC on their own pages. Pay and ship on hipobuy.com.</p>
  <ol class="local-steps">
    <li><strong>Search the catalog</strong><span>Filter hipo buy / hippo buy / hipobuy spreadsheet finds in the directory below or the search box. You do not need Excel or a Reddit thread to open the list.</span></li>
    <li><strong>Cite the dated dataset</strong><span><code>row_count</code> 8,600+, last reviewed 28 October 2026, on <a href="/finds-dataset/">/finds-dataset/</a> and the public JSON. We do not invent a higher count.</span></li>
    <li><strong>Check coupons separately</strong><span>Signup offers change in the official app. This hub logs what we last verified on <a href="/hipobuy-coupons/">/hipobuy-coupons/</a>.</span></li>
    <li><strong>QC, then a real country</strong><span>Read <a href="/hipobuy-qc-guide/">/hipobuy-qc-guide/</a> before you approve warehouse photos. Freight needs a real country on <a href="https://hipobuy.com/estimation" rel="noopener">hipobuy.com/estimation</a> — not this hostname.</span></li>
  </ol>
  <p class="local-src">Register and pay only on hipobuy.com. This page does not take payment and does not coach a declared value.</p>
</section>
""".strip()


def patch_net_home(html: str) -> str:
    """Replace dest-template #local with the hub four-step. Keep typo cluster."""
    html = re.sub(
        r'<section class="[^"]*" id="local"[^>]*>.*?</section>',
        HUB_LOCAL,
        html,
        count=1,
        flags=re.S,
    )
    if 'id="local"' not in html:
        if HERO_END in html:
            html = html.replace(
                HERO_END,
                "    </section>\n\n    " + HUB_LOCAL + "\n\n    <!-- ============ CATEGORIES ============ -->",
                1,
            )
        else:
            raise RuntimeError(".net homepage missing hero/h1 for #local insert")
    if "not a customs territory" in html:
        raise RuntimeError(".net still has dest-template 'not a customs territory'")
    if "location-name swap" in html:
        raise RuntimeError(".net still has dest-template location-name swap")
    for needle in (
        "hipo buy",
        "hippo buy",
        "/hipobuy-coupons/",
        "/finds-dataset/",
        "/hipobuy-qc-guide/",
        "hipobuy.com/estimation",
        'data-hub-reclaim="20261103"',
    ):
        if needle not in html:
            raise RuntimeError(f".net missing {needle!r}")
    return html
