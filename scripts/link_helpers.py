from urllib.parse import quote
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
_CONFIG = json.loads((ROOT / "site.config.json").read_text(encoding="utf-8"))
_AGENT = _CONFIG.get("agentPlatform", {})
_CONTACT = _CONFIG.get("contact", {})

MAIN_SITE = _CONFIG.get("mainSite", {
    "baseUrl": "https://w2clinks.com",
    "spreadsheetUrl": "https://w2clinks.com/spreadsheet/",
    "categoryUrlPattern": "https://w2clinks.com/spreadsheet/?category={CATEGORY}&page=1&sort=newest",
    "brandUrlPattern": "https://w2clinks.com/spreadsheet/?page=1&sort=newest&brand={brand}",
    "productSearchUrlPattern": "https://w2clinks.com/spreadsheet/?page=1&sort=newest&keyword={keyword}",
})

AGENT_PLATFORM = {
    "name": _AGENT.get("name", "OrientDig"),
    "baseUrl": _AGENT.get("baseUrl", "https://orientdig.com"),
    "faviconUrl": _AGENT.get("faviconUrl", "https://orientdig.com/site.ico"),
    "logoAsset": _AGENT.get("logoAsset", "assets/images/orientdig-logo.png"),
    "registerUrl": _CONTACT.get(
        "platformRegisterUrl", "https://orientdig.com/register?ref=100246065"
    ),
}


def main_spreadsheet_url():
    return MAIN_SITE["spreadsheetUrl"]


def category_url(category):
    return MAIN_SITE["categoryUrlPattern"].replace("{CATEGORY}", quote(str(category).upper()))


def slugify_brand(brand):
    value = str(brand).strip().lower()
    value = re.sub(r"[^a-z0-9\s-]", "", value)
    return re.sub(r"[\s-]+", "-", value).strip("-")


def brand_url(brand):
    return MAIN_SITE["brandUrlPattern"].replace("{brand}", quote(slugify_brand(brand)))


def product_search_url(keyword):
    return MAIN_SITE["productSearchUrlPattern"].replace(
        "{keyword}", quote(str(keyword).strip())
    )


def external_attrs() -> str:
    return 'target="_blank" rel="noopener"'


def whatsapp_url() -> str:
    return _CONTACT.get("whatsappUrl", "https://wa.me/447856544534")


def whatsapp_number() -> str:
    return _CONTACT.get("whatsappNumber", "+44 7856 544534")
