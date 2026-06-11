"""Fetch Kakobuy.com homepage carousel activities at build time."""

from __future__ import annotations

import json
import re
import ssl
import urllib.request
from html import unescape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CACHE_PATH = ROOT / "data" / "kakobuy-activities.json"
HOME_URL = "https://www.kakobuy.com/"
INVITE_URL = "https://ikako.vip/r/yze69"

SSL_CTX = ssl.create_default_context()
SSL_CTX.check_hostname = False
SSL_CTX.verify_mode = ssl.CERT_NONE

# Fallback when homepage fetch fails (snapshot 2026-06)
DEFAULT_ACTIVITIES = [
    {
        "id": "1",
        "title_zh": "新用户注册即送3000元优惠券！优惠代购，省心转运。",
        "url": INVITE_URL,
        "image": "https://nstatic.kakobuy.com/banner/202601/31/c1b9b68cffdf0ac8fa28c89a4275e042.png",
        "kind": "register_coupon",
    },
    {
        "id": "50",
        "title_zh": "6月份活動開始",
        "url": "https://www.kakobuy.com/tipdetail?id=50",
        "image": "https://nstatic.kakobuy.com/banner/202602/01/8d1ab6034ac0f85d928ab89ce692e0ff.png",
        "kind": "campaign",
    },
    {
        "id": "30",
        "title_zh": "Kakobuy美国用户关税相关公告",
        "url": "https://www.kakobuy.com/tipdetail?id=30",
        "image": "https://kk-oss-srch-hk.kakobuy.com/banner/202606/08/ce7ba995e3cbf8b816e4bbb14cd58428.png",
        "kind": "notice",
    },
]

TITLE_I18N: dict[str, dict[str, str]] = {
    "1": {
        "en": "New users: ¥3000 coupon bundle — register on Kakobuy",
        "es": "Nuevos usuarios: cupón 3000 CNY — regístrate en Kakobuy",
        "fr": "Nouveaux utilisateurs : coupon 3000 CNY — inscrivez-vous",
        "nl": "Nieuwe gebruikers: 3000 CNY coupon — registreer op Kakobuy",
        "fi": "Uudet käyttäjät: 3000 CNY kuponki — rekisteröidy Kakobuyhin",
    },
    "50": {
        "en": "June 2026 Kakobuy campaign",
        "es": "Campaña Kakobuy junio 2026",
        "fr": "Campagne Kakobuy juin 2026",
        "nl": "Kakobuy campagne juni 2026",
        "fi": "Kakobuy-kampanja kesäkuu 2026",
    },
    "30": {
        "en": "Kakobuy US customs & tariff notice",
        "es": "Aviso de aranceles EE.UU. — Kakobuy",
        "fr": "Annonce douanes / tarifs US — Kakobuy",
        "nl": "Kakobuy mededeling VS-tarieven",
        "fi": "Kakobuy Yhdysvaltain tariffi-ilmoitus",
    },
}


def _http_get(url: str, timeout: int = 25) -> str | None:
    try:
        req = urllib.request.Request(
            url,
            headers={"User-Agent": "Mozilla/5.0 (compatible; KakobuySpreadsheetBuilder/1.0)"},
        )
        with urllib.request.urlopen(req, context=SSL_CTX, timeout=timeout) as resp:
            return resp.read().decode("utf-8", errors="replace")
    except Exception:
        return None


def _parse_homepage(html: str) -> list[dict]:
    items: list[dict] = []
    seen: set[str] = set()
    for m in re.finditer(
        r'href="(https://www\.kakobuy\.com/tipdetail\?id=(\d+))"[^>]*>([^<]{4,120})',
        html,
        re.I,
    ):
        url, aid, title = m.group(1), m.group(2), unescape(m.group(3).strip())
        if aid in seen:
            continue
        seen.add(aid)
        items.append({"id": aid, "title_zh": title, "url": url, "image": "", "kind": "campaign"})
    imgs = re.findall(
        r'https://(?:nstatic\.kakobuy\.com|kk-oss-srch-hk\.kakobuy\.com)/banner/[^"\']+\.(?:png|jpg|webp)',
        html,
    )
    for i, item in enumerate(items):
        if i < len(imgs):
            item["image"] = imgs[i]
        if item["id"] == "1":
            item["url"] = INVITE_URL
            item["kind"] = "register_coupon"
        elif "关税" in item.get("title_zh", "") or "tariff" in item.get("title_zh", "").lower():
            item["kind"] = "notice"
    return items


def refresh_activities() -> list[dict]:
    html = _http_get(HOME_URL)
    items = _parse_homepage(html) if html else []
    if len(items) < 2:
        items = [dict(x) for x in DEFAULT_ACTIVITIES]
    for item in items:
        i18n = TITLE_I18N.get(item["id"], {})
        item["title_en"] = i18n.get("en", item.get("title_zh", ""))
        for lang in ("es", "fr", "nl", "fi"):
            item[f"title_{lang}"] = i18n.get(lang, item["title_en"])
        if item["id"] == "1":
            item["url"] = INVITE_URL
    CACHE_PATH.parent.mkdir(parents=True, exist_ok=True)
    CACHE_PATH.write_text(json.dumps({"activities": items}, indent=2), encoding="utf-8")
    return items


def load_activities() -> list[dict]:
    if CACHE_PATH.is_file():
        try:
            data = json.loads(CACHE_PATH.read_text(encoding="utf-8"))
            acts = data.get("activities") or []
            if acts:
                return acts
        except json.JSONDecodeError:
            pass
    return refresh_activities()
