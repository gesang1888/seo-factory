#!/usr/bin/env python3
"""Repair invalid FAQ JSON-LD on litbuyspreadsheetnow.com.

Google Search Console reported:
  Unparsable structured data — Missing ')' or object member name
First detected 2026-09-10 on https://litbuyspreadsheetnow.com/

Cause: a misspelling FAQ question was spliced inside the first FAQ object:

  [{"@type":"Question",{"@type":"Question","name":"Is this the same as ...

instead of two sibling Question objects. This script reconstructs valid JSON-LD
and can deploy the patched homepage to the Baota VPS.

Usage:
  python3 scripts/fix_litbuy_jsonld.py --self-test
  python3 scripts/fix_litbuy_jsonld.py --file /path/to/index.html
  LITBUY_DEPLOY_PASS='...' python3 scripts/fix_litbuy_jsonld.py --deploy
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path

JSONLD_RE = re.compile(
    r'(<script[^>]*type=["\']application/ld\+json["\'][^>]*>)(.*?)(</script>)',
    re.I | re.S,
)

BROKEN_PREFIX = '{"@type":"Question",{"@type":"Question"'
FIXED_PREFIX = '{"@type":"Question"'
SIBLING_MARKER = (
    'This is the same LitBuy spreadsheet regardless of how it is spelled."}},"name":'
)
SIBLING_FIXED = (
    'This is the same LitBuy spreadsheet regardless of how it is spelled."}},'
    '{"@type":"Question","name":'
)

DOMAIN = "litbuyspreadsheetnow.com"
REMOTE_INDEX = f"/www/wwwroot/{DOMAIN}/index.html"
HOST = os.environ.get(
    "LITBUY_DEPLOY_HOST",
    os.environ.get("KAKOBUY_DEPLOY_HOST", os.environ.get("ORIENTDIG_DEPLOY_HOST", "31.97.41.31")),
)
USER = os.environ.get(
    "LITBUY_DEPLOY_USER",
    os.environ.get("KAKOBUY_DEPLOY_USER", os.environ.get("ORIENTDIG_DEPLOY_USER", "root")),
)


def parse_jsonld_blocks(html: str) -> list[tuple[re.Match[str], object | None, Exception | None]]:
    results = []
    for match in JSONLD_RE.finditer(html):
        raw = match.group(2).strip()
        try:
            results.append((match, json.loads(raw), None))
        except Exception as exc:  # noqa: BLE001 — report any parse failure
            results.append((match, None, exc))
    return results


def repair_faq_jsonld(html: str) -> tuple[str, bool]:
    """Return (html, changed). Raises ValueError if FAQ JSON-LD cannot be repaired."""
    blocks = parse_jsonld_blocks(html)
    faq_match = None
    faq_err = None
    for match, obj, err in blocks:
        raw = match.group(2)
        if '"@type":"FAQPage"' in raw or (obj and obj.get("@type") == "FAQPage"):
            faq_match = match
            faq_err = err
            if obj is not None:
                return html, False
            break
    if faq_match is None:
        raise ValueError("No FAQPage JSON-LD block found")

    raw = faq_match.group(2).strip()
    if BROKEN_PREFIX not in raw:
        raise ValueError(f"FAQ JSON-LD is invalid but not the known splice: {faq_err}")

    fixed = raw.replace(BROKEN_PREFIX, FIXED_PREFIX, 1)
    if SIBLING_MARKER not in fixed:
        raise ValueError("Known splice prefix found, but sibling marker is missing")
    fixed = fixed.replace(SIBLING_MARKER, SIBLING_FIXED, 1)

    obj = json.loads(fixed)
    if obj.get("@type") != "FAQPage":
        raise ValueError("Repaired block is not FAQPage")
    entities = obj.get("mainEntity") or []
    if len(entities) < 2:
        raise ValueError("Repaired FAQPage has too few questions")
    for i, item in enumerate(entities):
        if item.get("@type") != "Question" or not item.get("name"):
            raise ValueError(f"FAQ item {i} missing Question/name")
        answer = item.get("acceptedAnswer") or {}
        if answer.get("@type") != "Answer" or not answer.get("text"):
            raise ValueError(f"FAQ item {i} missing Answer/text")

    compact = json.dumps(obj, ensure_ascii=False, separators=(",", ":"))
    new_html = html[: faq_match.start(2)] + compact + html[faq_match.end(2) :]
    return new_html, True


def assert_all_jsonld_valid(html: str) -> list[str]:
    types = []
    for i, (match, obj, err) in enumerate(parse_jsonld_blocks(html)):
        if err is not None:
            raise ValueError(f"JSON-LD block {i} still invalid: {err}")
        types.append(str(obj.get("@type")))
    return types


def _connect():
    try:
        import paramiko
    except ImportError:
        import subprocess

        subprocess.check_call([sys.executable, "-m", "pip", "install", "paramiko", "-q"])
        import paramiko

    password = (
        os.environ.get("LITBUY_DEPLOY_PASS")
        or os.environ.get("KAKOBUY_DEPLOY_PASS")
        or os.environ.get("ORIENTDIG_DEPLOY_PASS")
        or os.environ.get("BBDBUY_DEPLOY_PASS")
    )
    if not password:
        print("Set LITBUY_DEPLOY_PASS (or KAKOBUY_DEPLOY_PASS / ORIENTDIG_DEPLOY_PASS)", file=sys.stderr)
        sys.exit(1)
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(HOST, username=USER, password=password, timeout=30)
    return client


def _run(client, cmd: str, timeout: int = 60) -> str:
    _, stdout, stderr = client.exec_command(cmd, timeout=timeout)
    return (stdout.read() + stderr.read()).decode(errors="replace").strip()


def deploy_repair() -> None:
    client = _connect()
    sftp = client.open_sftp()
    local = Path("/tmp/litbuy-index.live.html")
    sftp.get(REMOTE_INDEX, str(local))
    html = local.read_text(encoding="utf-8")
    new_html, changed = repair_faq_jsonld(html)
    types = assert_all_jsonld_valid(new_html)
    print(f"live JSON-LD types: {types}")
    if not changed:
        print("FAQ JSON-LD already valid; no deploy needed")
        client.close()
        return

    stamp = _run(client, "date -u +%Y%m%d_%H%M%S")
    bak = f"{REMOTE_INDEX}.bak-jsonld-{stamp}"
    _run(client, f"cp -a {REMOTE_INDEX} {bak}")
    print(f"backup {bak}")

    patched = Path("/tmp/litbuy-index.patched.html")
    patched.write_text(new_html, encoding="utf-8")
    tmp_remote = f"{REMOTE_INDEX}.new-jsonld"
    sftp.put(str(patched), tmp_remote)
    _run(
        client,
        f"mv {tmp_remote} {REMOTE_INDEX} && chown www:www {REMOTE_INDEX} && chmod 755 {REMOTE_INDEX}",
    )
    sftp.close()
    print(_run(client, f"wc -c {REMOTE_INDEX}; stat -c '%y %n' {REMOTE_INDEX}"))
    client.close()
    print("deployed patched index.html")


BROKEN_FIXTURE = """<!doctype html><html><head>
<script type="application/ld+json">{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question",{"@type":"Question","name":"Is this the same as 'lit buy spreadsheet' or 'lid buy spreadsheet'?","acceptedAnswer":{"@type":"Answer","text":"Yes — 'lit buy', 'lid buy', 'lite buy' and 'libuy' are all common spellings for the LitBuy shopping agent. This is the same LitBuy spreadsheet regardless of how it is spelled."}},"name":"What is the Litbuy Spreadsheet?","acceptedAnswer":{"@type":"Answer","text":"The Litbuy Spreadsheet is a curated database."}}]}</script>
<script type="application/ld+json">{"@context":"https://schema.org","@type":"WebSite","name":"LitBuy Spreadsheet"}</script>
</head><body></body></html>"""


def self_test() -> None:
    try:
        json.loads(JSONLD_RE.search(BROKEN_FIXTURE).group(2))
        raise SystemExit("fixture unexpectedly parsed")
    except json.JSONDecodeError:
        pass
    fixed, changed = repair_faq_jsonld(BROKEN_FIXTURE)
    assert changed
    types = assert_all_jsonld_valid(fixed)
    assert types == ["FAQPage", "WebSite"], types
    faq = json.loads(JSONLD_RE.search(fixed).group(2))
    names = [q["name"] for q in faq["mainEntity"]]
    assert names[0].startswith("Is this the same as")
    assert names[1] == "What is the Litbuy Spreadsheet?"
    unchanged, changed2 = repair_faq_jsonld(fixed)
    assert not changed2
    assert unchanged == fixed
    print("self-test OK")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--file", type=Path)
    parser.add_argument("--inplace", action="store_true")
    parser.add_argument("--deploy", action="store_true")
    args = parser.parse_args()

    if args.self_test:
        self_test()
        return
    if args.deploy:
        deploy_repair()
        return
    if not args.file:
        parser.error("pass --self-test, --deploy, or --file")
    html = args.file.read_text(encoding="utf-8")
    new_html, changed = repair_faq_jsonld(html)
    types = assert_all_jsonld_valid(new_html)
    print(f"changed={changed} jsonld={types}")
    if args.inplace and changed:
        args.file.write_text(new_html, encoding="utf-8")
        print(f"wrote {args.file}")


if __name__ == "__main__":
    main()
