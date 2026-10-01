#!/usr/bin/env python3
"""Surgical #local insert on hipobuyspreadsheet.net homepage only.

This hostname is a hub, not a customs territory. Do not overwrite ranked
html / news / category URLs with a CMS country-desk template.
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


def patch_net_home(html: str) -> str:
    facts = net_facts()
    guide = local_guide_html(facts).strip()
    if "</style>" in html and ".local-steps{" not in html:
        html = html.replace("</style>", SKIP_CSS + "\n</style>", 1)
    html = re.sub(
        r'<section class="sg-sec" id="local".*?</section>',
        guide,
        html,
        count=1,
        flags=re.S,
    )
    if 'id="local"' not in html:
        if "</h1>" not in html:
            raise RuntimeError(".net homepage missing <h1> for #local insert")
        html = re.sub(r"</h1>", "</h1>\n" + guide, html, count=1)
    err: list[str] = []
    _check_local_section(html, facts, err)
    if err:
        raise RuntimeError(f".net #local: {'; '.join(err)}")
    if "not a customs territory" not in html:
        raise RuntimeError(".net missing hub fingerprint")
    return html
