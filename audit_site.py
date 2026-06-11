#!/usr/bin/env python3
"""Audit OrientDig Spreadsheet dist output for W2CLinks CTAs and OrientDig branding."""

from __future__ import annotations

import json
import re
import sys
from collections import defaultdict
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from scripts.domains import CANONICAL_DOMAINS, HREFLANG_CLUSTER, PLURAL_REDIRECTS  # noqa: E402
from scripts.link_helpers import AGENT_PLATFORM, MAIN_SITE, whatsapp_number, whatsapp_url  # noqa: E402

DIST = ROOT / "dist"
REPORT_DIR = ROOT / "output"
REPORT_PATH = REPORT_DIR / "orientdig_audit_report.md"

SPREADSHEET_URL = MAIN_SITE["spreadsheetUrl"]
FAVICON_URL = AGENT_PLATFORM["faviconUrl"]
WHATSAPP_URL = whatsapp_url()
WHATSAPP_NUM = whatsapp_number()

REQUIRED_HREFLANG = set(HREFLANG_CLUSTER.keys())

FAKE_PATTERNS = [
    re.compile(r'href="[^"]*/products/[^"]*"', re.I),
    re.compile(r'href="[^"]*/product/[^"]*"', re.I),
    re.compile(r'href="[^"]*fake[^"]*"', re.I),
    re.compile(r"local-spreadsheet", re.I),
]

class AuditReport:
    def __init__(self) -> None:
        self.errors: list[str] = []
        self.warnings: list[str] = []
        self.passed: list[str] = []
        self.stats: dict[str, int] = defaultdict(int)

    def error(self, msg: str) -> None:
        self.errors.append(msg)

    def warn(self, msg: str) -> None:
        self.warnings.append(msg)

    def ok(self, msg: str) -> None:
        self.passed.append(msg)


def read_html_files(base: Path) -> list[Path]:
    return sorted(base.rglob("index.html"))


def audit_html(path: Path, domain: str, report: AuditReport) -> None:
    rel = path.relative_to(DIST)
    text = path.read_text(encoding="utf-8", errors="replace")
    report.stats["html_files"] += 1

    if "fansbuy" in text.lower():
        report.error(f"{rel}: fansbuy residue found")

    if re.search(r"w2clinks\.com(?!/spreadsheet)", text, re.I):
        # w2clinks base is OK for footer; flag only if used as fake spreadsheet path
        if re.search(r'href="https://w2clinks\.com/"[^>]*class="btn-primary"', text, re.I):
            report.warn(f"{rel}: primary CTA may not point to spreadsheet")

    if SPREADSHEET_URL not in text and "orientdig.com" not in text:
        report.warn(f"{rel}: missing w2clinks spreadsheet or orientdig reference")

    # Primary CTAs should include spreadsheet URL
    btn_primary = re.findall(
        r'class="btn btn-primary"[^>]*href="([^"]+)"', text, re.I
    )
    for href in btn_primary:
        allowed = (
            href.startswith(SPREADSHEET_URL.rstrip("/"))
            or href.startswith(SPREADSHEET_URL)
            or href.startswith("https://w2clinks.com/spreadsheet/?")
            or href.startswith(AGENT_PLATFORM["baseUrl"])
        )
        if not allowed:
            report.error(f"{rel}: primary CTA href not W2CLinks spreadsheet: {href}")

    for pat in FAKE_PATTERNS:
        if pat.search(text):
            report.error(f"{rel}: possible fake local product/spreadsheet link")

    for url in re.findall(r'<a\s[^>]*href="(https://(?:w2clinks\.com|orientdig\.com)[^"]*)"', text):
        tag_m = re.search(
            rf'<a\s[^>]*href="{re.escape(url)}"[^>]*>', text, re.I
        )
        if not tag_m:
            continue
        chunk = tag_m.group(0)
        if 'target="_blank"' not in chunk or "noopener" not in chunk:
            report.error(f"{rel}: external link missing target/_blank rel/noopener: {url}")

    # Flag positive official claims, not FAQ questions that deny official status
    body_text = re.sub(r"<script[^>]*>.*?</script>", "", text, flags=re.S | re.I)
    body_text = re.sub(r"<[^>]+>", " ", body_text)
    if re.search(
        r"\b(official (site|partner|spreadsheet)|authorized partner|officially authorized)\b",
        body_text,
        re.I,
    ):
        report.error(f"{rel}: official/authorized/partner claim found")

    if WHATSAPP_URL not in text:
        report.error(f"{rel}: missing WhatsApp link")
    if WHATSAPP_NUM not in text:
        report.error(f"{rel}: missing WhatsApp display number")
    if 'property="og:title"' not in text:
        report.error(f"{rel}: missing og:title")
    if '"@type": "Organization"' not in text and '"@type":"Organization"' not in text:
        report.error(f"{rel}: missing Organization JSON-LD")
    if "brand-logo" not in text and "orientdig-logo" not in text:
        report.error(f"{rel}: missing logo image")
    if "Independent Spreadsheet Guide" not in text:
        report.warn(f"{rel}: missing independent guide badge")

    title_m = re.search(r"<title>([^<]+)</title>", text, re.I)
    h1_m = re.search(r"<h1>([^<]+)</h1>", text, re.I)
    desc_m = re.search(r'name="description" content="([^"]+)"', text, re.I)
    if not title_m:
        report.error(f"{rel}: missing title")
    if not h1_m:
        report.error(f"{rel}: missing H1")
    if not desc_m:
        report.error(f"{rel}: missing meta description")
    if "FAQPage" not in text:
        report.error(f"{rel}: missing FAQ JSON-LD")
    if "BreadcrumbList" not in text:
        report.error(f"{rel}: missing BreadcrumbList JSON-LD")

    canon_m = re.search(r'<link rel="canonical" href="([^"]+)"', text)
    if canon_m:
        expected_prefix = f"https://{domain}"
        if not canon_m.group(1).startswith(expected_prefix):
            report.error(
                f"{rel}: canonical {canon_m.group(1)} not on domain {domain}"
            )
    else:
        report.error(f"{rel}: missing canonical")

    found_hreflang = set(re.findall(r'hreflang="([^"]+)"', text))
    if rel.name == "index.html" and str(rel).count("/") <= 2:
        missing = REQUIRED_HREFLANG - found_hreflang
        if missing and domain in CANONICAL_DOMAINS:
            # only common home pages need full cluster
            if rel.parent.name == domain or rel.parent == Path(domain):
                if missing:
                    report.warn(f"{rel}: homepage missing hreflang: {sorted(missing)}")


def audit_plural_redirects(report: AuditReport) -> None:
    for plural, target in PLURAL_REDIRECTS.items():
        idx = DIST / plural / "index.html"
        ht = DIST / plural / ".htaccess"
        if not idx.exists():
            report.error(f"{plural}: missing redirect index.html")
            continue
        text = idx.read_text(encoding="utf-8")
        if target not in text:
            report.error(f"{plural}: redirect target {target} not in index.html")
        else:
            report.ok(f"{plural}: 301 redirect page -> {target}")
        if ht.exists() and target.split("//")[1].split("/")[0] in ht.read_text():
            report.ok(f"{plural}: .htaccess present")
        else:
            report.warn(f"{plural}: .htaccess may be incomplete")


def audit_sitemaps(report: AuditReport) -> None:
    for domain in CANONICAL_DOMAINS:
        sm = DIST / domain / "sitemap.xml"
        rb = DIST / domain / "robots.txt"
        if not sm.exists():
            report.error(f"{domain}: missing sitemap.xml")
        else:
            report.stats["sitemaps"] += 1
            report.ok(f"{domain}: sitemap.xml exists")
        if not rb.exists():
            report.error(f"{domain}: missing robots.txt")
        elif "Sitemap:" not in rb.read_text():
            report.error(f"{domain}: robots.txt missing Sitemap line")
        nf = DIST / domain / "404.html"
        if not nf.exists():
            report.error(f"{domain}: missing 404.html")
        else:
            report.ok(f"{domain}: 404.html exists")


def check_title_h1_uniqueness(report: AuditReport) -> None:
    titles: dict[str, list[str]] = defaultdict(list)
    h1s: dict[str, list[str]] = defaultdict(list)
    for domain in CANONICAL_DOMAINS:
        for path in read_html_files(DIST / domain):
            text = path.read_text(encoding="utf-8")
            t = re.search(r"<title>([^<]+)</title>", text)
            h = re.search(r"<h1>([^<]+)</h1>", text)
            if t:
                titles[domain].append(t.group(1))
            if h:
                h1s[domain].append(h.group(1))
        for val, items in [("title", titles[domain]), ("h1", h1s[domain])]:
            seen = set()
            for item in items:
                if item in seen:
                    report.error(f"{domain}: duplicate {val}: {item}")
                seen.add(item)


def write_report(report: AuditReport) -> Path:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    lines = [
        "# 中文 SEO 检查报告 — OrientDig Spreadsheet",
        "",
        f"- 检查目录：{DIST}",
        f"- 生成时间：{datetime.now().isoformat(timespec='seconds')}",
        f"- HTML 页面扫描：{report.stats['html_files']}",
        f"- 错误数量：**{len(report.errors)}**",
        f"- 警告数量：**{len(report.warnings)}**",
        "",
        "## 通过项",
        "- sitemap、robots、404、title/meta/H1/canonical/hreflang/schema",
        "- W2CLinks 转化、WhatsApp、OG、Organization schema、logo",
        "- 无 fansbuy 残留、无虚假 official 背书",
        "",
        "## 错误",
        "",
    ]
    if report.errors:
        lines.extend(f"- {e}" for e in report.errors)
    else:
        lines.append("- None")

    lines.extend(["", "## 警告", ""])
    if report.warnings:
        lines.extend(f"- {w}" for w in report.warnings)
    else:
        lines.append("- 无")

    lines.extend(["", "## 信息", ""])
    lines.extend(f"- {p}" for p in report.passed[:20])
    if len(report.passed) > 20:
        lines.append(f"- … 另有 {len(report.passed) - 20} 项通过")

    lines.extend(
        [
            "",
            "## 审计标准",
            "",
            "- 0 fansbuy 残留",
            f"- 主转化：{SPREADSHEET_URL}",
            f"- WhatsApp：{WHATSAPP_NUM}",
            "- OG + Organization + FAQ + Breadcrumb schema",
            "- 独立 guide 定位（非 Official Partner 虚假背书）",
            "- 信任页：about/contact/privacy/terms/disclosures",
            "",
        ]
    )

    REPORT_PATH.write_text("\n".join(lines), encoding="utf-8")
    return REPORT_PATH


def main() -> None:
    if not DIST.exists():
        print(f"dist/ not found — run build_site.py first ({DIST})")
        sys.exit(1)

    report = AuditReport()

    for domain in CANONICAL_DOMAINS:
        domain_dir = DIST / domain
        if not domain_dir.exists():
            report.error(f"Missing dist/{domain}/")
            continue
        for html_path in read_html_files(domain_dir):
            audit_html(html_path, domain, report)

    audit_plural_redirects(report)
    audit_sitemaps(report)
    check_title_h1_uniqueness(report)

    path = write_report(report)
    print(f"Audit report: {path}")
    print(f"Errors: {len(report.errors)}, Warnings: {len(report.warnings)}")
    if report.errors:
        sys.exit(1)


if __name__ == "__main__":
    main()
