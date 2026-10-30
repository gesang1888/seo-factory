#!/usr/bin/env python3
"""Remove consumer-visible 运营说明 / Editor notes / hub-reclaim GSC padding.

Strips:
  - <section/div/aside> with gsc-*-editor-notes, hub-reclaim, *-gsc-extra*, gsc-heavy
  - Editor-notes kicker labels (UK/NL/AU/… editor notes, Notes éditeur, Notas del editor)
  - Hub-reclaim badges and gsc-enrich comments

Does not touch unique PHP (hipobuyspreadsheet.net live) and does not rewrite
buyer copy outside those ops boxes. Generators that used to re-inject notes
should call strip_html() after their other edits.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

OPEN_TAG = re.compile(r"<(section|div|aside)\b([^>]*?)(/?)>", re.I | re.S)
COMMENT_GSC = re.compile(r"<!--\s*gsc-enrich[^>]*-->\s*", re.I)

# Opening-tag fingerprints for ops boxes.
OPS_ATTR = re.compile(
    r"""
    id\s*=\s*["'][^"']*(?:editor-notes|hub-reclaim|gsc-heavy)[^"']*["']
    | class\s*=\s*["'][^"']*(?:gsc-extra|gsc-heavy|gsc-w2crep-extra|gsc-crawled|reclaim-box)[^"']*["']
    | data-hub-reclaim\s*=
    """,
    re.I | re.X,
)

KICKER_P = re.compile(
    r"""<p\b[^>]*>\s*(?:
        (?:UK|NL|US|AU|CA|IT|FR|ES|EU|AT|Global|Australia|Canada|France|España|
           KakobuyDocs|UK\s+sheets)?\s*
        (?:editor\s+notes|Notes\s+pour|Notas\s+del\s+editor|Notes\s+éditeur)
        (?:\s*[\(—\-–:].{0,80})?
        | Hub\s+ownership[^<]{0,120}
        | Hub\s+reclaim[^<]{0,160}
      )\s*</p>\s*""",
    re.I | re.X | re.S,
)

HUB_BADGE = re.compile(
    r'<p\s+class="(?:eu-badge|local-src)"[^>]*>[^<]*(?:Hub reclaim|hub-reclaim)[^<]*</p>\s*',
    re.I,
)

REFRESH_P = re.compile(
    r'<p\b[^>]*class="[^"]*gsc-extra-refresh[^"]*"[^>]*>.*?</p>\s*',
    re.I | re.S,
)

H2_OPS = re.compile(
    r"<h2\b[^>]*>\s*(?:Editor notes|UK editor notes|NL editor notes|US editor notes|"
    r"Australia editor notes|Canada editor notes|Notas del editor|Notes pour|"
    r"Notes éditeur|Hub reclaim)\b[\s\S]*?</h2>\s*"
    r"(?:<(?:p|ul|ol|div)\b[\s\S]*?</(?:p|ul|ol|div)>\s*){0,8}",
    re.I,
)

COMMENT_HUB_ONLY = re.compile(r"<!--\s*hub-reclaim=[^>]*-->\s*", re.I)
DATA_HUB_ATTR = re.compile(r"\s+data-hub-reclaim=(?:\"[^\"]*\"|'[^']*')", re.I)
# Visible / SERP stamps: brand-hub-reclaim-YYYYMMDD and hub_reclaim=...
STAMP_TOKEN = re.compile(
    r"(?:\s*[·•|,;:]\s*)?(?:[a-z0-9-]+-)?hub[-_]?reclaim(?:-\d{8}|=[a-z0-9-]+-\d{8})",
    re.I,
)
PHRASE_HUB = re.compile(r"\bhub reclaim:?\s*", re.I)

SKIP_NAME = re.compile(
    r"\.(ops-scrub|es-gap|es-disclaimer-rm|platform-patched|stabilize-patched|"
    r"ca-light-fix|nl-deepen|uk-deepen)$"
)

# Visible leftover phrases that should not remain after box removal.
LEFTOVER = (
    "gsc-editor-notes",
    "gsc-basetao-editor-notes",
    "gsc-ca-editor-notes",
    "gsc-it-editor-notes",
    "gsc-uk-editor-notes",
    "id=\"hub-reclaim\"",
    "data-hub-reclaim",
    "Editor notes",
    "UK editor notes",
    "NL editor notes",
    "US editor notes",
    "Global editor notes",
    "Australia editor notes",
    "Canada editor notes",
    "AT editor notes",
    "EU editor notes",
    "Notas del editor",
    "Notes pour la France",
    "Notes éditeur",
    "KakobuyDocs editor notes",
    "UK sheets editor notes",
    "Hub reclaim",
    "hub-reclaim-",
    "运营说明",
)


def _match_open(html: str, start: int) -> tuple[str, int, int, bool] | None:
    m = OPEN_TAG.match(html, start)
    if not m:
        return None
    tag, attrs, self_close = m.group(1), m.group(2), bool(m.group(3))
    return tag.lower(), m.start(), m.end(), self_close or attrs.rstrip().endswith("/")


def _element_end(html: str, tag: str, content_start: int) -> int:
    """Return index just after the matching close tag, respecting nesting."""
    open_re = re.compile(rf"<{tag}\b", re.I)
    close_re = re.compile(rf"</{tag}\s*>", re.I)
    depth = 1
    i = content_start
    while i < len(html) and depth:
        nxt_open = open_re.search(html, i)
        nxt_close = close_re.search(html, i)
        if not nxt_close:
            return len(html)
        if nxt_open and nxt_open.start() < nxt_close.start():
            # Could be a self-closing lookalike; treat as nested open.
            depth += 1
            i = nxt_open.end()
        else:
            depth -= 1
            i = nxt_close.end()
    return i


def _strip_ops_elements(html: str) -> str:
    out: list[str] = []
    i = 0
    n = len(html)
    while i < n:
        m = OPEN_TAG.search(html, i)
        if not m:
            out.append(html[i:])
            break
        tag, attrs, slash = m.group(1), m.group(2), m.group(3)
        if not OPS_ATTR.search(attrs):
            out.append(html[i : m.end()])
            i = m.end()
            continue
        out.append(html[i : m.start()])
        self_close = bool(slash) or attrs.rstrip().endswith("/")
        if self_close:
            i = m.end()
            continue
        end = _element_end(html, tag, m.end())
        i = end
        while i < n and html[i] in " \t\r\n":
            i += 1
    return "".join(out)


def strip_html(html: str) -> str:
    html = COMMENT_GSC.sub("", html)
    html = COMMENT_HUB_ONLY.sub("", html)
    html = _strip_ops_elements(html)
    html = KICKER_P.sub("", html)
    html = HUB_BADGE.sub("", html)
    html = REFRESH_P.sub("", html)
    html = H2_OPS.sub("", html)
    html = DATA_HUB_ATTR.sub("", html)
    html = html.replace("Hub reclaim money URL", "Brand spreadsheet")
    html = html.replace("hub reclaim money URL", "Brand spreadsheet")
    html = STAMP_TOKEN.sub("", html)
    html = PHRASE_HUB.sub("", html)
    html = re.sub(r"\n{3,}", "\n\n", html)
    return html


def leftovers(html: str) -> list[str]:
    hits = []
    for tok in LEFTOVER:
        if tok.lower() in html.lower() or tok in html:
            # Editorial WhatsApp is not ops
            if tok.lower() == "editor notes" and "editorial whatsapp" in html.lower() and html.lower().count("editor notes") == 0:
                continue
            if tok in html or tok.lower() in html.lower():
                hits.append(tok)
    # filter Editorial WhatsApp false positive on "Editor notes"
    if "Editor notes" in hits and "editorial whatsapp" in html.lower():
        # count real editor-notes vs WhatsApp
        if not re.search(r"editor notes", html, re.I):
            hits = [h for h in hits if h != "Editor notes"]
    return hits


def iter_html_files(root: Path) -> list[Path]:
    files: list[Path] = []
    for p in root.rglob("*"):
        if not p.is_file():
            continue
        name = p.name.lower()
        if not (
            name.endswith((".html", ".htm", ".php"))
            or ".html." in name
            or name.endswith(".index.html")
        ):
            continue
        rel = str(p.relative_to(root))
        files.append(p)
    return files


def overlay_to_url(path: Path, root: Path) -> str | None:
    """Map sites/{host}/overlay/... to https://{host}/...  Skip snapshots."""
    try:
        rel = path.relative_to(root / "sites")
    except ValueError:
        return None
    parts = rel.parts
    if len(parts) < 3 or parts[1] != "overlay":
        return None
    host = parts[0]
    rest = parts[2:]
    if not rest:
        return None
    if rest[0] == "live-base" or "live-base" in rest[0]:
        return None
    if rest[-1].startswith("live-base"):
        return None
    if SKIP_NAME.search(rest[-1]):
        return None
    name = rest[-1]
    dirs = rest[:-1]
    if name in {"index.html", "index.htm"}:
        slug = "/".join(dirs)
        return f"https://{host}/" if not slug else f"https://{host}/{slug}/"
    if name.endswith(".html"):
        slug = "/".join(dirs + (name,))
        return f"https://{host}/{slug}"
    return None


def _ssh_client():
    import os

    try:
        import paramiko
    except ImportError:
        import subprocess as sp

        sp.check_call([sys.executable, "-m", "pip", "install", "paramiko", "-q"])
        import paramiko

    password = os.environ.get("ORIGIN_SSH_PASS")
    if not password:
        pfile = Path("/tmp/hipobuy-creds/origin.pass")
        if pfile.is_file():
            password = pfile.read_text().rstrip("\n")
    if not password:
        raise SystemExit("Set ORIGIN_SSH_PASS")
    host = os.environ.get("ORIGIN_SSH_HOST", "31.97.41.31")
    port = int(os.environ.get("ORIGIN_SSH_PORT", "22"))
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(
        host,
        port=port,
        username="root",
        password=password,
        timeout=30,
        allow_agent=False,
        look_for_keys=False,
    )
    return client


def deploy_live(manifest: Path) -> int:
    import json
    from datetime import datetime, timezone

    rows = json.loads(manifest.read_text(encoding="utf-8"))
    client = _ssh_client()
    sftp = client.open_sftp()
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    bak = f"/www/backup/strip-editor-notes-{stamp}"
    _, out, err = client.exec_command(f"mkdir -p '{bak}'", timeout=30)
    out.read()
    err.read()
    ok = 0
    for row in rows:
        remote = row["remote"]
        if "hipobuyspreadsheet.net" in remote:
            print("SKIP unique hub", remote)
            continue
        local = Path("/tmp/stripped-live") / remote.replace("/www/wwwroot/", "")
        if not local.is_file():
            print("MISSING", local)
            continue
        _, out, err = client.exec_command(
            f"cp -a '{remote}' '{bak}/' 2>/dev/null || true", timeout=30
        )
        out.read()
        err.read()
        sftp.put(str(local), remote)
        _, out, err = client.exec_command(f"chown www:www '{remote}'", timeout=20)
        out.read()
        err.read()
        print("PUT", remote, "bytes", local.stat().st_size)
        ok += 1
    sftp.close()
    client.close()
    print("deployed", ok, "backup", bak)
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", type=Path, default=ROOT)
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--report", action="store_true")
    ap.add_argument("--deploy-live", type=Path, help="JSON manifest of stripped live files")
    args = ap.parse_args()
    if args.deploy_live:
        return deploy_live(args.deploy_live)
    root: Path = args.root
    files = iter_html_files(root / "sites")
    changed = []
    remaining = []
    for p in files:
        original = p.read_text(encoding="utf-8", errors="replace")
        if not leftovers(original) and not OPS_ATTR.search(original) and "gsc-extra" not in original:
            continue
        new = strip_html(original)
        if new != original:
            changed.append((p, len(original) - len(new)))
            if not args.dry_run:
                p.write_text(new, encoding="utf-8")
        left = leftovers(new)
        if left:
            remaining.append((p, left))
    print(f"scanned {len(files)} html/php under sites/")
    print(f"changed {len(changed)}")
    for p, delta in changed:
        print(f"  -{delta:5d}  {p.relative_to(root)}")
    if remaining:
        print(f"remaining {len(remaining)}")
        for p, left in remaining:
            print(f"  KEEP? {p.relative_to(root)} :: {left}")
    else:
        print("remaining 0")
    return 0


if __name__ == "__main__":
    sys.exit(main())
