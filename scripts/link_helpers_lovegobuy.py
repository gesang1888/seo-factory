"""Lovegobuy cluster link helpers — loads site.lovegobuy.config.json + W2CLinks."""

from __future__ import annotations

import json
import re
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parents[1]
_CONFIG_PATH = ROOT / "site.lovegobuy.config.json"
_CONFIG = json.loads(_CONFIG_PATH.read_text(encoding="utf-8"))
_AGENT = _CONFIG.get("agentPlatform", {})
_CONTACT = _CONFIG.get("contact", {})

MAIN_SITE = _CONFIG.get("mainSite", {})

AGENT_PLATFORM = {
    "name": _AGENT.get("name", "Lovegobuy"),
    "baseUrl": _AGENT.get("baseUrl", "https://www.lovegobuy.com"),
    "faviconUrl": _AGENT.get("faviconUrl", "https://www.lovegobuy.com/favicon.ico"),
    "logoAsset": _AGENT.get("logoAsset", "assets/images/lovegobuy-logo.png"),
    "registerUrl": _CONTACT.get(
        "platformRegisterUrl", "https://www.lovegobuy.com/?invite_code=W5RJX3"
    ),
}


def main_spreadsheet_url() -> str:
    return MAIN_SITE["spreadsheetUrl"]


def category_url(category: str) -> str:
    return MAIN_SITE["categoryUrlPattern"].replace(
        "{CATEGORY}", quote(str(category).upper())
    )


def slugify_brand(brand: str) -> str:
    value = str(brand).strip().lower()
    value = re.sub(r"[^a-z0-9\s-]", "", value)
    return re.sub(r"[\s-]+", "-", value).strip("-")


def brand_url(brand: str) -> str:
    return MAIN_SITE["brandUrlPattern"].replace("{brand}", quote(slugify_brand(brand)))


def product_search_url(keyword: str) -> str:
    return MAIN_SITE["productSearchUrlPattern"].replace(
        "{keyword}", quote(str(keyword).strip())
    )


def external_attrs() -> str:
    return 'target="_blank" rel="noopener"'


def whatsapp_url() -> str:
    return _CONTACT.get("whatsappUrl", "https://wa.me/447856544534")


def whatsapp_number() -> str:
    return _CONTACT.get("whatsappNumber", "+44 7856 544534")
