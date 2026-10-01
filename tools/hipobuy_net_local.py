#!/usr/bin/env python3
"""Surgical #local insert on hipobuyspreadsheet.net homepage only.

Live / is EyouCMS (`template/pc/index.htm`), not the small Georgia index.html.
Do not overwrite ranked news/category html. Hub pack: this hostname is not
a customs territory.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

_TOOLS = Path(__file__).resolve().parent
if str(_TOOLS) not in sys.path:
    sys.path.insert(0, str(_TOOLS))
from desk_template import (  # noqa: E402
    SKIP_CSS,
    _check_local_section,
    local_guide_html,
)

NET_HOST = "hipobuyspreadsheet.net"
REMOTE_INDEX = f"/www/wwwroot/{NET_HOST}/index.html"
REMOTE_TEMPLATE = f"/www/wwwroot/{NET_HOST}/template/pc/index.htm"
HERO_END = "    </section>\n\n    <!-- ============ CATEGORIES ============ -->"


def net_facts() -> dict:
    return {
        "agent": "HipoBuy",
        "host": NET_HOST,
        "lang": "en",
        "loc": "en",
        "dest": None,
        "dest_label": "a country in the estimator",
        "ccy": "USD",
        "storage": "90 free days from Stored, see official Help Center",
        "estimator": "https://hipobuy.com/estimation",
        "official": "https://hipobuy.com/",
        "date": "1 Oct 2026",
        "email": "cnfd85269032661@gmail.com",
        "keep": [
            ("/shoes/", "Shoes"),
            ("/hoodies-sweaters/", "Hoodies"),
            ("/news/", "News"),
            ("/about/", "About"),
        ],
        "codes_off_title": ["VGEICZNX0"],
        "strict_html_codes": False,
    }


def _guide_block() -> str:
    facts = net_facts()
    guide = local_guide_html(facts).strip()
    return (
        f"<style>{SKIP_CSS}</style>\n"
        f"{guide}"
    )


def patch_net_home(html: str) -> str:
    """Patch the live CMS homepage template (or a tiny static stub)."""
    facts = net_facts()
    block = _guide_block()
    html = re.sub(
        r'<style>\.skip\{.*?</style>\s*<section class="sg-sec" id="local".*?</section>',
        block,
        html,
        count=1,
        flags=re.S,
    )
    html = re.sub(
        r'<section class="sg-sec" id="local".*?</section>',
        local_guide_html(facts).strip(),
        html,
        count=1,
        flags=re.S,
    )
    if 'id="local"' not in html:
        if HERO_END in html:
            html = html.replace(HERO_END, "    </section>\n\n    " + block + "\n\n    <!-- ============ CATEGORIES ============ -->", 1)
        elif "</h1>" in html:
            html = re.sub(r"</h1>", "</h1>\n" + block, html, count=1)
        else:
            raise RuntimeError(".net homepage missing hero/h1 for #local insert")
    err: list[str] = []
    _check_local_section(html, facts, err)
    if err:
        raise RuntimeError(f".net #local: {'; '.join(err)}")
    if "not a customs territory" not in html:
        raise RuntimeError(".net missing hub fingerprint")
    return html
