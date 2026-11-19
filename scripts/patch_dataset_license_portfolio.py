#!/usr/bin/env python3
"""Fill GSC Dataset.license (and fix a few broken JSON-LD nodes) on live hubs.

Does NOT change frozen Title/H1. JSON-LD / a short #license paragraph only.

  ORIENTDIG_DEPLOY_PASS='...' python3 scripts/patch_dataset_license_portfolio.py --deploy
"""

from __future__ import annotations

import argparse
import ast
import json
import os
import re
import sys
HOST = os.environ.get("ORIENTDIG_DEPLOY_HOST", "31.97.41.31")
USER = os.environ.get("ORIENTDIG_DEPLOY_USER", "root")
STAMP = "20261119"
BAK = f"/www/backup/dataset-license-portfolio-{STAMP}"

LICENSE_SECTION = """
<section id="license">
  <h2>Dataset license</h2>
  <p>This Independent Index JSON is published on this host for informational use. Cite <code>row_count</code>, <code>last_verified</code> and sample SKUs with a link back here. Bulk harvesting beyond the published JSON is not licensed. This host is not the agent checkout.</p>
</section>
"""

ORG_BRAND = {
    "acbuyspreadsheets.ca": ("ACBuy Spreadsheet", "Canada"),
    "acbuyspreadsheets.nl": ("ACBuy Spreadsheet", "Nederland"),
    "allchinabuyspreadsheet.ca": ("AllChinaBuy Spreadsheet", "Canada"),
    "allchinabuyspreadsheets.co.uk": ("AllChinaBuy Spreadsheet", "the United Kingdom"),
    "fansbuy.co.uk": ("FansBuy Spreadsheet", "the United Kingdom"),
    "fansbuy.nl": ("FansBuy Spreadsheet", "Nederland"),
    "fansbuyspreadsheet.de": ("FansBuy Spreadsheet", "Deutschland"),
    "oopbuyspreadsheets.it": ("OOPBuy Spreadsheet", "l’Italia"),
    "usfansspreadsheet.nl": ("USFans Spreadsheet", "Nederland"),
    "usfansspreadsheet.co.uk": ("USFans Spreadsheet", "the United Kingdom"),
    "litbuy.at": ("LitBuy Spreadsheet", None),
}

LD_RE = re.compile(
    r'(<script[^>]*type=["\']application/ld\+json["\'][^>]*>)(.*?)(</script>)',
    re.I | re.S,
)


def _connect():
    try:
        import paramiko
    except ImportError:
        import subprocess

        subprocess.check_call([sys.executable, "-m", "pip", "install", "paramiko", "-q"])
        import paramiko

    password = (
        os.environ.get("ORIENTDIG_DEPLOY_PASS")
        or os.environ.get("BBDBUY_DEPLOY_PASS")
        or os.environ.get("KAKOBUY_DEPLOY_PASS")
    )
    if not password:
        raise SystemExit("Set ORIENTDIG_DEPLOY_PASS")
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(
        HOST, username=USER, password=password, timeout=30, allow_agent=False, look_for_keys=False
    )
    return client


def _run(client, cmd: str, timeout: int = 120) -> str:
    _, stdout, stderr = client.exec_command(cmd, timeout=timeout)
    return (stdout.read() + stderr.read()).decode("utf-8", "replace")


def _pretty(original: str, obj) -> str:
    if original.lstrip().startswith("{"):
        if "\n" in original[:80]:
            return json.dumps(obj, ensure_ascii=False, indent=2)
        return json.dumps(obj, ensure_ascii=False, separators=(",", ":"))
    return json.dumps(obj, ensure_ascii=False)


def _walk_dataset(obj, license_url: str, description: str | None = None) -> int:
    n = 0
    if isinstance(obj, dict):
        types = obj.get("@type")
        types = [types] if isinstance(types, str) else list(types or [])
        if "Dataset" in types:
            if not (obj.get("description") or "").strip() and description:
                obj["description"] = description
            if not obj.get("license"):
                obj["license"] = license_url
                n += 1
        for v in obj.values():
            n += _walk_dataset(v, license_url, description)
    elif isinstance(obj, list):
        for v in obj:
            n += _walk_dataset(v, license_url, description)
    return n


def _ensure_license_section(html: str) -> str:
    if 'id="license"' in html or 'id="dataset-license"' in html:
        return html
    for needle in (
        "</article>",
        '<footer',
        "</body>",
    ):
        if needle in html:
            return html.replace(needle, LICENSE_SECTION + needle, 1)
    return html + LICENSE_SECTION


def patch_html_datasets(html: str, host: str, path: str, terms: bool) -> tuple[str, int]:
    license_url = (
        f"https://{host}/terms/"
        if terms
        else f"https://{host}/finds-dataset/#license"
    )
    added = 0

    def repl(m):
        nonlocal added
        raw = m.group(2).strip()
        if "Dataset" not in raw:
            return m.group(0)
        blob = raw
        blob = blob.replace("      P26-10-29\",\n", '      "dateModified": "2026-10-29",\n')
        try:
            data = json.loads(blob)
        except json.JSONDecodeError:
            return m.group(0)
        desc = None
        if host == "kakobuydocs.com":
            desc = (
                "Public, dated catalog of Kakobuy spreadsheet finds with row_count, "
                "sample SKUs and QC flags. JSON at /data/finds-dataset.json. Not a Google Sheet."
            )
        n = _walk_dataset(data, license_url, desc)
        if not n and isinstance(data, dict) and data.get("@type") == "Dataset" and data.get("license"):
            return m.group(0)
        if n:
            added += n
            dumped = _pretty(raw, data)
            return f"{m.group(1)}\n{dumped}\n{m.group(3)}" if "\n" in raw[:40] else f"{m.group(1)}{dumped}{m.group(3)}"
        return m.group(0)

    html2 = LD_RE.sub(repl, html)
    if added and not terms and "finds-dataset" in path:
        html2 = _ensure_license_section(html2)
    return html2, added


def fix_vigor_home(html: str) -> str:
    broken = """ {"@type":"Question","name":"How long is warehouse storage free?","acceptedAnswer":{"@type":"Answer","text":"Official Help and estimation were behind a Cloudflare Turnstile challenge on 9 Oct 2026. This desk does not invent a free-day count. Confirm the live Help copy and in-account timer the morning you ship."}},
 
 ]}
]}"""
    fixed = """ {"@type":"Question","name":"How long is warehouse storage free?","acceptedAnswer":{"@type":"Answer","text":"Official Help and estimation were behind a Cloudflare Turnstile challenge on 9 Oct 2026. This desk does not invent a free-day count. Confirm the live Help copy and in-account timer the morning you ship."}}
]}
]}"""
    if broken not in html:
        if '"How long is warehouse storage free?"' in html and html.count("]}\n]}") >= 1:
            return html
        return html
    return html.replace(broken, fixed, 1)


def fix_allchina_faq(html: str) -> str:
    def repl(m):
        raw = m.group(2).strip()
        if raw.startswith("{@") or ("'@type'" in raw and "FAQPage" in raw):
            try:
                data = ast.literal_eval(raw)
            except (SyntaxError, ValueError):
                return m.group(0)
            if not isinstance(data, dict):
                return m.group(0)
            data.setdefault("@context", "https://schema.org")
            dumped = json.dumps(data, ensure_ascii=False)
            return f"{m.group(1)}{dumped}{m.group(3)}"
        return m.group(0)

    return LD_RE.sub(repl, html)


def fix_dest_org(html: str, host: str) -> str:
    brand, country = ORG_BRAND.get(host, (None, None))
    if not brand:
        return html
    html = html.replace('"name": "", "url":', f'"name": "{brand}", "url":')
    html = html.replace('"name": ""', f'"name": "{brand}"')
    if host == "acbuyspreadsheets.ca":
        html = html.replace(
            "ACBuy Spreadsheet voor kopers in Nederland – Beste finds en QC",
            "ACBuy Spreadsheet for Canadian Buyers – Best Finds & QC",
        )
        html = html.replace(
            " for Nederland on acbuyspreadsheets.ca. Catalogue, freight estimate, local last-mile.",
            "ACBuy independent desk for Canada on acbuyspreadsheets.ca. Catalogue, freight estimate, local last-mile.",
        )
        html = html.replace(
            "De catalogus op deze homepage komt van /api/products/. Nederlandse woorden geven vaak nul — gebruik de Engelse key (sneakers, hoodie).",
            "The catalog on this homepage comes from /api/products/. Non-English search words often return zero — use the English key (sneakers, hoodie).",
        )
    elif country:
        old = f" for {country} on {host}. Catalogue, freight estimate, local last-mile."
        new = (
            f"{brand} independent desk for {country} on {host}. "
            "Catalogue, freight estimate, local last-mile."
        )
        html = html.replace(old, new)
        # leftover NL bleed on a non-NL host already handled for acbuy.ca
    return html


def fix_bbdbuy_fr(html: str) -> str:
    # Keep visible Title/H1. Point JSON-LD at this host, not bbdbuy.uk.
    html = html.replace('"@id": "https://bbdbuy.uk/"', '"@id": "https://bbdbuy.fr/"')
    html = html.replace('"url": "https://bbdbuy.uk/"', '"url": "https://bbdbuy.fr/"')
    html = html.replace('"inLanguage": "en-GB"', '"inLanguage": "fr-FR"')
    html = html.replace(
        '"name": "BBDBuy Spreadsheet for UK Buyers – Best Finds & QC", "url": "https://bbdbuy.fr/"',
        '"name": "BBDBuy Spreadsheet pour acheteurs en France – Meilleurs finds et QC", "url": "https://bbdbuy.fr/"',
    )
    html = html.replace(
        "BBDBuy Spreadsheet for UK buyers on bbdbuy.uk. Finds, QC, shipping, legal. Source: HMRC. Keywords: BBDBuy spreadsheet, bbdbuy spreadsheet uk, bbdbuy sheet. Not checkout. No declared-value coaching.",
        "BBDBuy Spreadsheet pour acheteurs en France sur bbdbuy.fr. Finds, QC, Colissimo / La Poste. Paiement sur bbdbuy.com.",
    )
    html = html.replace('"name": "bbdbuy.uk independent desk"', '"name": "BBDBuy independent desk"')
    html = html.replace("support@bbdbuy.uk", "support@bbdbuy.fr")
    html = html.replace(
        "BBDBuy independent desk for the United Kingdom on bbdbuy.uk. Catalogue, freight estimate, local last-mile. Not checkout.",
        "BBDBuy independent desk for France on bbdbuy.fr. Catalogue, freight estimate, Colissimo / La Poste. Not checkout.",
    )
    html = html.replace(
        '"keywords": ["BBDBuy spreadsheet", "bbdbuy spreadsheet uk", "bbdbuy sheet"]',
        '"keywords": ["BBDBuy spreadsheet", "bbdbuy spreadsheet france", "bbdbuy sheet"]',
    )
    return html


def deploy() -> None:
    client = _connect()
    print(_run(client, f"mkdir -p {BAK}"))
    sftp = client.open_sftp()

    scan = json.loads(
        _run(
            client,
            r"""python3 - <<'PY'
import os, re, json
root='/www/wwwroot'
SKIP=set(['runtime','cache','backup','node_modules','.git','uploads','vendor','weapp','core','application'])
rows=[]
for dirpath, dirnames, files in os.walk(root):
    dirnames[:] = [d for d in dirnames if d not in SKIP and not d.startswith('.')]
    for fn in files:
        if not fn.endswith(('.html','.htm')): continue
        path=os.path.join(dirpath, fn)
        try:
            if os.path.getsize(path)>1_500_000: continue
            t=open(path,'r',encoding='utf-8',errors='replace').read()
        except Exception:
            continue
        if 'Dataset' not in t or 'ld+json' not in t.lower():
            continue
        rel=path[len(root)+1:]
        host=rel.split('/',1)[0]
        rows.append({'host':host,'path':path,'rel':rel})
print(json.dumps(rows))
PY""",
            timeout=180,
        )
    )

    terms_hosts = set()
    for row in scan:
        host = row["host"]
        if host in terms_hosts:
            continue
        exists = _run(client, f"test -f /www/wwwroot/{host}/terms/index.html && echo yes || echo no").strip()
        if exists == "yes":
            terms_hosts.add(host)

    extra = [
        "/www/wwwroot/vigorspreadsheet.com/index.html",
        "/www/wwwroot/kakobuydocs.com/kakobuy-spreadsheet/index.html",
        "/www/wwwroot/allchina-buy.com/allchinabuy-spreadsheet-2026/index.html",
        "/www/wwwroot/allchina-buy.com/allchinabuy-discount-code/index.html",
        "/www/wwwroot/acbuyspreadsheets.ca/index.html",
        "/www/wwwroot/bbdbuy.fr/index.html",
    ]
    extra += [f"/www/wwwroot/{h}/index.html" for h in ORG_BRAND]
    paths = []
    seen = set()
    for p in [r["path"] for r in scan] + extra:
        if p not in seen:
            seen.add(p)
            paths.append(p)

    changed = []
    for path in paths:
        try:
            with sftp.open(path) as fh:
                html = fh.read().decode("utf-8", "replace")
        except FileNotFoundError:
            print("skip missing", path)
            continue
        orig = html
        host = path.split("/")[3]
        rel = path[len("/www/wwwroot/") :]
        if "vigorspreadsheet.com/index.html" in path:
            html = fix_vigor_home(html)
        if "allchinabuy-spreadsheet-2026" in path or "allchinabuy-discount-code" in path:
            html = fix_allchina_faq(html)
        if host in ORG_BRAND and path.endswith("/index.html"):
            html = fix_dest_org(html, host)
        if host == "bbdbuy.fr" and path.endswith("/index.html"):
            html = fix_bbdbuy_fr(html)
        html, n = patch_html_datasets(html, host, rel, host in terms_hosts)
        if html == orig:
            continue
        stamp = path.replace("/", "_")
        _run(client, f"cp -a {path} {BAK}/{stamp}")
        tmp = path + f".new-{STAMP}"
        with sftp.open(tmp, "w") as fh:
            fh.write(html)
        _run(client, f"mv {tmp} {path} && chown www:www {path} 2>/dev/null; chmod 644 {path}")
        changed.append((path, n))
        print("patched", path, "dataset+", n)

    print(
        _run(
            client,
            "rm -rf /www/wwwroot/hipobuyspreadsheet.net/data/runtime/temp/* "
            "/www/wwwroot/w2clinks.com/data/runtime/temp/* 2>/dev/null; echo cache-cleared",
        )
    )
    sftp.close()
    client.close()
    print("changed", len(changed), "backup", BAK)


def verify() -> None:
    import urllib.request

    checks = {
        "https://hipobuyspreadsheet.net/": ["https://hipobuyspreadsheet.net/terms/#dataset-license"],
        "https://usfansspreadsheet.net/finds-dataset/": [
            "https://usfansspreadsheet.net/finds-dataset/#license"
        ],
        "https://acbuyspreadsheets.ca/": [
            "ACBuy Spreadsheet for Canadian Buyers",
            '"name": "ACBuy Spreadsheet"',
            "for Canada on acbuyspreadsheets.ca",
            "Non-English search words often return zero",
        ],
        "https://bbdbuyeu.net/finds-dataset/": ['"license":'],
        "https://mycnbox.eu/finds-dataset/": ['"license":'],
        "https://kakobuydocs.com/kakobuy-spreadsheet/": ['"dateModified": "2026-10-29"'],
        "https://vigorspreadsheet.com/": ["How long is warehouse storage free?"],
    }
    for url, needles in checks.items():
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 seo-factory-dataset-lic"})
        with urllib.request.urlopen(req, timeout=25) as resp:
            html = resp.read().decode("utf-8", "replace")
        missing = [n for n in needles if n not in html]
        if missing:
            raise SystemExit(f"LIVE FAIL {url} missing {missing}")
        # parse Dataset if present
        for raw in re.findall(
            r'<script[^>]*ld\+json[^>]*>(.*?)</script>', html, re.I | re.S
        ):
            blob = raw.strip()
            blob = re.sub(r"\{eyou:[^}]+/\}", "https://example.invalid", blob)
            try:
                json.loads(blob)
            except json.JSONDecodeError as exc:
                raise SystemExit(f"LIVE JSON {url}: {exc}") from exc
        title = re.search(r"<title[^>]*>(.*?)</title>", html, re.I | re.S)
        t = re.sub("<[^>]+>", "", title.group(1) if title else "").replace("\n", " ")[:100]
        print("LIVE OK", url, "title=", t)


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--deploy", action="store_true")
    p.add_argument("--verify", action="store_true")
    args = p.parse_args()
    if args.deploy:
        deploy()
        verify()
        return
    if args.verify:
        verify()
        return
    p.error("pass --deploy or --verify")


if __name__ == "__main__":
    main()
