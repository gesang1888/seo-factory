#!/usr/bin/env python3
"""Collect Reddit discussions about OrientDig for SEO/GEO pain-point expansion."""

from __future__ import annotations

import json
import re
import ssl
import urllib.parse
import urllib.request
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT_JSON = ROOT / "data" / "reddit" / "orientdig_pain_points.json"
OUT_MD = ROOT / "output" / "reddit_orientdig_geo_insights.md"

PULLPUSH = "https://api.pullpush.io/reddit/search/submission/"
QUERIES = ["orientdig", "orientdig shipping", "orientdig coupon", "orientdig qc", "orientdig payment"]

THEME_RULES: list[tuple[str, list[str]]] = [
    ("shipping_time", ["ship", "wait", "slow", "weeks", "delay", "haul", "delivery", "customs", "tax", "duties"]),
    ("website_ux", ["site", "website", "confus", "how", "work", "doesnt work", "broken", "interface"]),
    ("payment", ["payment", "pay", "card", "paypal", "balance", "top up", "recharge"]),
    ("qc_photos", ["qc", "quality", "photos", "review this", "gl", "rl"]),
    ("tracking", ["track", "logistics", "where", "parcel", "status"]),
    ("trust_scam", ["scam", "legit", "trust", "fake", "avoid", "risk"]),
    ("agent_compare", ["acbuy", "cnfans", "sugargoo", "pandabuy", "vs", "switch", "better agent"]),
    ("coupons", ["coupon", "1300", "discount", "bonus", "rmb"]),
    ("warehouse", ["warehouse", "storage", "rehearsal", "consolidat"]),
    ("support", ["support", "service", "reply", "answer", "help"]),
]

GEO_SUBS = {
    "EU": {"FashionReps", "FrenchyReps", "FashionRepsPolska", "FashionRepsIT", "OrientDig_OD", "Repsneakers", "1688Reps"},
    "US": {"FashionReps", "Repsneakers", "RepsneakersDogs", "pandabuy_jerseys", "rep"},
}

PAGE_MAP = {
    "shipping_time": ["/orientdig-shipping/", "/how-long-does-orientdig-take-to-ship/", "/livraison-orientdig/"],
    "website_ux": ["/how-to-use-orientdig/", "/what-is-orientdig/", "/guide-orientdig/"],
    "payment": ["/orientdig-payment-methods/", "/is-orientdig-safe/"],
    "qc_photos": ["/orientdig-qc/", "/qc-orientdig/"],
    "tracking": ["/orientdig-tracking/", "/orientdig-shipping/"],
    "trust_scam": ["/is-orientdig-legit/", "/is-orientdig-safe/", "/avis-orientdig/", "/orientdig-fiable/"],
    "agent_compare": ["/cnfans-to-orientdig/", "/orientdig-review/", "/orientdig-erfahrungen/"],
    "coupons": ["/orientdig-coupons/", "/orientdig-coupon-code/", "/orientdig-codes/"],
    "warehouse": ["/orientdig-shipping/", "/orientdig-qc/"],
    "support": ["/orientdig-customer-service/", "/orientdig-review/"],
}

SSL_CTX = ssl.create_default_context()
SSL_CTX.check_hostname = False
SSL_CTX.verify_mode = ssl.CERT_NONE


def fetch_posts(query: str, size: int = 80) -> list[dict]:
    url = PULLPUSH + "?" + urllib.parse.urlencode(
        {"q": query, "size": size, "sort": "desc", "sort_type": "score"}
    )
    req = urllib.request.Request(url, headers={"User-Agent": "OrientDigSEOResearch/1.0"})
    with urllib.request.urlopen(req, context=SSL_CTX, timeout=30) as resp:
        data = json.loads(resp.read().decode())
    return data.get("data") or []


def classify(text: str) -> list[str]:
    low = text.lower()
    hits = []
    for theme, keys in THEME_RULES:
        if any(k in low for k in keys):
            hits.append(theme)
    return hits or ["general"]


def geo_for_sub(sub: str) -> str:
    if sub in GEO_SUBS["US"]:
        return "US"
    if sub in GEO_SUBS["EU"] or sub == "OrientDig_OD":
        return "EU"
    return "Global"


def clean(text: str) -> str:
    text = re.sub(r"\s+", " ", text or "").strip()
    return text[:500]


def build_report(posts: list[dict]) -> dict:
    by_theme: dict[str, list[dict]] = defaultdict(list)
    seen = set()
    for p in posts:
        pid = p.get("id")
        if pid in seen:
            continue
        seen.add(pid)
        title = p.get("title") or ""
        body = p.get("selftext") or ""
        text = f"{title}. {body}"
        themes = classify(text)
        sub = p.get("subreddit") or ""
        entry = {
            "title": clean(title),
            "snippet": clean(body) or clean(title),
            "subreddit": sub,
            "geo": geo_for_sub(sub),
            "score": p.get("score") or 0,
            "url": "https://reddit.com" + (p.get("permalink") or ""),
            "themes": themes,
            "suggested_pages": list(
                dict.fromkeys(
                    page for th in themes for page in PAGE_MAP.get(th, ["/orientdig-review/"])
                )
            ),
        }
        for th in themes:
            by_theme[th].append(entry)

    summaries = []
    for theme, items in sorted(by_theme.items(), key=lambda x: -len(x[1])):
        items.sort(key=lambda x: -x["score"])
        top = items[:5]
        eu = sum(1 for i in items if i["geo"] == "EU")
        us = sum(1 for i in items if i["geo"] == "US")
        summaries.append(
            {
                "theme": theme,
                "count": len(items),
                "geo_split": {"EU": eu, "US": us, "Global": len(items) - eu - us},
                "suggested_pages": PAGE_MAP.get(theme, []),
                "top_threads": top,
                "seo_angle": _seo_angle(theme),
            }
        )

    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source": "Reddit via PullPush API (public submissions)",
        "total_posts": len(seen),
        "themes": summaries,
    }


def _seo_angle(theme: str) -> str:
    angles = {
        "shipping_time": "Address EU/US delivery expectations, customs, and no fixed ETA claims.",
        "website_ux": "Beginner guides: paste link → QC → ship; link W2CLinks spreadsheet separately.",
        "payment": "Explain checkout currencies and when charges happen (item vs freight).",
        "qc_photos": "QC approval workflow before international shipping.",
        "tracking": "Warehouse vs international line tracking stages.",
        "trust_scam": "Objective legit/safe pages — no fake ratings; explain agent model risks.",
        "agent_compare": "Neutral comparison pages (CNFans, ACBuy) without attack copy.",
        "coupons": "1300CNY coupon interest — verify on OrientDig, no guaranteed discount promises.",
        "warehouse": "Free storage limits, consolidation, rehearsal shipping FAQ.",
        "support": "When to use OrientDig help center vs independent guide.",
    }
    return angles.get(theme, "Expand FAQ cluster around OrientDig spreadsheet intent.")


def write_markdown(report: dict) -> None:
    OUT_MD.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Reddit OrientDig 用户痛点 — SEO/GEO 扩展报告",
        "",
        f"生成时间：{report['generated_at']}",
        "",
        f"样本帖数：{report['total_posts']}（PullPush 公开搜索）",
        "",
        "## 主题概览",
        "",
    ]
    for t in report["themes"]:
        lines.append(f"### {t['theme']} ({t['count']} 帖)")
        lines.append("")
        lines.append(f"- **SEO 角度：** {t['seo_angle']}")
        gs = t["geo_split"]
        lines.append(f"- **地区分布：** EU {gs['EU']} / US {gs['US']} / Global {gs['Global']}")
        lines.append(f"- **建议页面：** {', '.join(t['suggested_pages'])}")
        lines.append("")
        lines.append("**代表讨论：**")
        for th in t["top_threads"][:3]:
            lines.append(f"- [{th['title']}]({th['url']}) — r/{th['subreddit']} ({th['geo']}, score {th['score']})")
            if th["snippet"]:
                lines.append(f"  > {th['snippet'][:200]}")
        lines.append("")

    lines.extend(
        [
            "## GEO 执行建议",
            "",
            "- **UK/US：** 强化 shipping time、payment、tracking、site UX 类 FAQ",
            "- **EU（FR/DE/IT/NL）：** 强化 customs、agent 对比、QC、coupon 词落地页",
            "- **Reddit 社区：** r/OrientDig_OD、r/FashionReps、r/FrenchyReps 是主要讨论场",
            "- **内容原则：** 引用社区痛点但不做虚假官方背书；转化仍走 W2CLinks spreadsheet",
            "",
        ]
    )
    OUT_MD.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    posts: list[dict] = []
    for q in QUERIES:
        try:
            posts.extend(fetch_posts(q, 60))
        except Exception as exc:
            print(f"warn: {q}: {exc}")
    report = build_report(posts)
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    write_markdown(report)
    print(f"themes: {len(report['themes'])}")
    print(f"json: {OUT_JSON}")
    print(f"md: {OUT_MD}")


if __name__ == "__main__":
    main()
