"""Fetch Lovegobuy.com homepage carousel activities at build time."""

from __future__ import annotations

import json
import re
import ssl
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CACHE_PATH = ROOT / "data" / "lovegobuy-activities.json"
HOME_URL = "https://www.lovegobuy.com/"
INVITE_URL = "https://www.lovegobuy.com/?invite_code=W5RJX3"
IMG_BASE = "https://www.lovegobuy.com"

SSL_CTX = ssl.create_default_context()
SSL_CTX.check_hostname = False
SSL_CTX.verify_mode = ssl.CERT_NONE

# Snapshot from lovegobuy.com homepage (2026-06) when fetch is blocked by Cloudflare
DEFAULT_ACTIVITIES: list[dict] = [
    {
        "id": "coupon",
        "title_zh": "新用户优惠券礼包 $137",
        "url": INVITE_URL,
        "image": f"{IMG_BASE}/uploads/10001/20260506/ecb439d8bae930a2c1acf2f67fc0e5a5.png",
        "kind": "register_coupon",
    },
    {
        "id": "cashback",
        "title_zh": "Share Unboxing — earn up to 100% cashback",
        "url": f"{HOME_URL}activity",
        "image": f"{IMG_BASE}/uploads/10001/20260603/d4914f0a83a532d8c0fe25b93073b9cb.png",
        "kind": "campaign",
    },
    {
        "id": "qc",
        "title_zh": "Update QC infos",
        "url": HOME_URL,
        "image": f"{IMG_BASE}/uploads/10001/20260603/8366380a1261fddeb3ca90e919efda86.png",
        "kind": "campaign",
    },
    {
        "id": "referral",
        "title_zh": "Invite friends — earn rewards",
        "url": INVITE_URL,
        "image": f"{IMG_BASE}/uploads/10001/20260507/e0b056e10f3b8e5a435293dcdfaec22a.png",
        "kind": "campaign",
    },
    {
        "id": "ticket",
        "title_zh": "Service Ticket System Upgrade Notice",
        "url": f"{HOME_URL}help",
        "image": f"{IMG_BASE}/uploads/10001/20260506/3f698f8eb43cf678e615aa2ed645cccc.png",
        "kind": "notice",
    },
]

TITLE_I18N: dict[str, dict[str, str]] = {
    "coupon": {
        "en": "New users: $137 coupon pack — register on Lovegobuy",
        "es": "Nuevos usuarios: pack de cupones $137 — regístrate en Lovegobuy",
        "nl": "Nieuwe gebruikers: $137 couponpakket — registreer op Lovegobuy",
        "it": "Nuovi utenti: pacchetto coupon $137 — registrati su Lovegobuy",
    },
    "cashback": {
        "en": "Share Unboxing — earn up to 100% cashback",
        "es": "Comparte unboxing — hasta 100% cashback",
        "nl": "Deel unboxing — tot 100% cashback",
        "it": "Condividi unboxing — fino al 100% cashback",
    },
    "qc": {
        "en": "Update QC infos on Lovegobuy",
        "es": "Actualiza información QC en Lovegobuy",
        "nl": "QC-informatie bijwerken op Lovegobuy",
        "it": "Aggiorna info QC su Lovegobuy",
    },
    "referral": {
        "en": "Invite friends — Lovegobuy referral rewards",
        "es": "Invita amigos — recompensas Lovegobuy",
        "nl": "Nodig vrienden uit — Lovegobuy-beloningen",
        "it": "Invita amici — premi Lovegobuy",
    },
    "ticket": {
        "en": "Service Ticket System upgrade notice",
        "es": "Aviso: actualización del sistema de tickets",
        "nl": "Mededeling: upgrade ticketsysteem",
        "it": "Avviso: aggiornamento sistema ticket",
    },
}


def _http_get(url: str, timeout: int = 25) -> str | None:
    try:
        req = urllib.request.Request(
            url,
            headers={"User-Agent": "Mozilla/5.0 (compatible; LovegobuySpreadsheetBuilder/1.0)"},
        )
        with urllib.request.urlopen(req, context=SSL_CTX, timeout=timeout) as resp:
            return resp.read().decode("utf-8", errors="replace")
    except Exception:
        return None


def _parse_homepage(html: str) -> list[dict]:
    imgs = re.findall(
        r"https://www\.lovegobuy\.com/uploads/10001/[^\"'\\s]+\.(?:png|jpg|webp)",
        html,
    )
    seen: set[str] = set()
    unique: list[str] = []
    for url in imgs:
        if url not in seen:
            seen.add(url)
            unique.append(url)
    if len(unique) < 2:
        return []
    kinds = ("register_coupon", "campaign", "campaign", "campaign", "notice")
    titles = (
        "New users coupon pack",
        "Lovegobuy campaign",
        "Lovegobuy promotion",
        "Lovegobuy referral",
        "Lovegobuy announcement",
    )
    items: list[dict] = []
    for i, img in enumerate(unique[:5]):
        kind = kinds[i] if i < len(kinds) else "campaign"
        item = {
            "id": str(i + 1),
            "title_zh": titles[i] if i < len(titles) else "Lovegobuy promotion",
            "url": INVITE_URL if kind == "register_coupon" else HOME_URL,
            "image": img,
            "kind": kind,
        }
        items.append(item)
    return items


def _apply_i18n(items: list[dict]) -> None:
    for item in items:
        i18n = TITLE_I18N.get(item["id"], {})
        item["title_en"] = i18n.get("en", item.get("title_zh", ""))
        for lang in ("es", "nl", "it"):
            item[f"title_{lang}"] = i18n.get(lang, item["title_en"])
        if item.get("kind") == "register_coupon":
            item["url"] = INVITE_URL


def refresh_activities() -> list[dict]:
    html = _http_get(HOME_URL)
    items = _parse_homepage(html) if html and "Just a moment" not in html else []
    if len(items) < 2:
        items = [dict(x) for x in DEFAULT_ACTIVITIES]
    _apply_i18n(items)
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
