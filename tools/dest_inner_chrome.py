#!/usr/bin/env python3
"""Wrap ranked dest inner HTML in the same header/footer/logo/colors as the CMS homepage.

Keeps title, description, canonical, JSON-LD, gtag, and the article body.
Does not PUT 5KB overlays. Does not touch HipoBuy/LitBuy/SugarGoo/Kakobuy gold
or CSSBuy PHP AT/ES/FR/IT/NL. Does not rewrite root index.html.
"""
from __future__ import annotations

import json
import os
import re
import sys
import time
from html import unescape
from pathlib import Path

MARKER = 'data-inner-chrome="20261002"'
MIN_TEXT = 120
SKIP_REL = {"index.html", "404.html", "404/index.html"}
SITE_HEADER_RE = re.compile(
    r"<header\b[^>]*(?:site-header|cssbuy-header)[^>]*>",
    re.I,
)
NAV_BAR_RE = re.compile(
    r'<nav\b[^>]*class="nav(?:\s[^"]*)?"[^>]*>',
    re.I,
)
SCRIPT_RE = re.compile(r"<script\b[\s\S]*?</script>", re.I)
ANN_RE = re.compile(
    r'<div class="(?:ann|cssbuy-topbar)"[\s\S]*?</div>\s*',
    re.I,
)


def _element_inner(html: str, tag: str, start: int = 0) -> tuple[str, int, int] | None:
    open_re = re.compile(rf"<{tag}\b[^>]*>", re.I)
    close_re = re.compile(rf"</{tag}\s*>", re.I)
    m = open_re.search(html, start)
    if not m:
        return None
    pos = m.end()
    depth = 1
    while depth:
        om = open_re.search(html, pos)
        cm = close_re.search(html, pos)
        if not cm:
            return None
        if om and om.start() < cm.start():
            depth += 1
            pos = om.end()
        else:
            depth -= 1
            if depth == 0:
                return html[m.end() : cm.start()], m.start(), cm.end()
            pos = cm.end()
    return None


def _text_len(chunk: str) -> int:
    text = re.sub(r"<script[\s\S]*?</script>", " ", chunk, flags=re.I)
    text = re.sub(r"<style[\s\S]*?</style>", " ", text, flags=re.I)
    text = re.sub(r"<[^>]+>", " ", text)
    text = unescape(text)
    return len(re.sub(r"\s+", "", text))


def _substantial(chunk: str) -> bool:
    if not chunk:
        return False
    return _text_len(chunk) >= MIN_TEXT or len(chunk) >= 400


def _chrome_end(html: str) -> int | None:
    hm = SITE_HEADER_RE.search(html)
    if hm:
        block = _element_inner(html, "header", hm.start())
        if block:
            return block[2]
    nm = NAV_BAR_RE.search(html)
    if nm:
        block = _element_inner(html, "nav", nm.start())
        if block:
            return block[2]
    return None


def extract_article(html: str) -> str | None:
    start = _chrome_end(html)
    if start is not None:
        fm = re.search(r"<footer\b", html[start:], re.I)
        if fm:
            chunk = ANN_RE.sub("", html[start : start + fm.start()]).strip()
            if _substantial(chunk):
                return chunk

    main = _element_inner(html, "main")
    if main and _substantial(main[0]):
        extra = ""
        fm = re.search(r"<footer\b", html[main[2] :], re.I)
        if fm:
            extra = html[main[2] : main[2] + fm.start()].strip()
        chunk = (main[0] + "\n" + extra).strip()
        return chunk if _substantial(chunk) else main[0].strip()

    bm = re.search(r"<body\b[^>]*>([\s\S]*)</body>", html, re.I)
    if not bm:
        return None
    body = bm.group(1)
    body = ANN_RE.sub("", body)
    body = re.sub(r"<header\b[\s\S]*?</header>", "", body, count=1, flags=re.I)
    body = re.sub(r"<nav\b[\s\S]*?</nav>", "", body, count=1, flags=re.I)
    body = re.sub(r"<footer\b[\s\S]*?</footer>", "", body, count=1, flags=re.I)
    body = body.strip()
    return body if _substantial(body) else None


def after_footer_keep(html: str, article: str) -> str:
    m = re.search(r"</footer\s*>", html, re.I)
    if not m:
        return ""
    rest = re.sub(r"</body>.*", "", html[m.end() :], flags=re.I | re.S)

    def _drop_dup(match: re.Match) -> str:
        block = match.group(0)
        idm = re.search(r'\sid="([^"]+)"', block[:240])
        if idm and idm.group(1) and f'id="{idm.group(1)}"' in article:
            return ""
        text = re.sub(r"<[^>]+>", " ", block)
        key = re.sub(r"\s+", " ", unescape(text)).strip()[:80]
        art_text = re.sub(r"\s+", " ", unescape(re.sub(r"<[^>]+>", " ", article)))
        if key and key in art_text:
            return ""
        return block

    rest = re.sub(r"<section\b[\s\S]*?</section>", _drop_dup, rest, flags=re.I)
    return rest.strip()


def _html_tag(html: str) -> str:
    m = re.search(r"<html\b[^>]*>", html, re.I)
    return m.group(0) if m else "<html>"


def _head_inner(html: str) -> str:
    m = re.search(r"<head\b[^>]*>([\s\S]*)</head>", html, re.I)
    return m.group(1) if m else ""


def _body_scripts_outside_article(html: str, article: str) -> str:
    bm = re.search(r"<body\b[^>]*>([\s\S]*)</body>", html, re.I)
    if not bm:
        return ""
    keep = []
    for script in SCRIPT_RE.findall(bm.group(1)):
        if script in article:
            continue
        keep.append(script)
    return "\n".join(keep)


def wrap_html(html: str, snip: dict) -> tuple[str | None, str]:
    if MARKER in html or ("inner-article" in html and "desk-cms.css" in html):
        return None, "already"
    if "Georgia" in html and "#00C853" in html and len(html) < 8000:
        return None, "skip-georgia-shell"
    article = extract_article(html)
    if not article:
        return None, "no-article"
    article = ANN_RE.sub("", article).strip()
    if not _substantial(article):
        return None, "thin-article"
    head = _head_inner(html)
    inject = snip["inject"]
    if "desk-cms.css" not in head:
        head = head.rstrip() + "\n" + inject + "\n"
    else:
        if MARKER.split("=")[0] not in head:
            head = head.rstrip() + "\n" + inject + "\n"
    trailing = after_footer_keep(html, article)
    extra_scripts = _body_scripts_outside_article(html, article + trailing)
    out = (
        "<!DOCTYPE html>\n"
        f"{_html_tag(html)}\n"
        f"<head>\n{head.rstrip()}\n</head>\n"
        f"<body {MARKER}>\n"
        f"{snip['skip']}"
        f"{snip['header']}\n"
        f'<main id="main" class="container inner-article">\n{article}\n</main>\n'
        f"{snip['footer']}\n"
        f"{trailing}\n"
        f"{extra_scripts}\n"
        "</body></html>\n"
    )
    if "Georgia" in out and "#00C853" in out:
        return None, "georgia-leak"
    return out, "ok"


def build_snips() -> dict:
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from desk_template import skip_label, skip_link
    from hub_skin_desks import AGENTS, HOSTS, header_html, footer_html

    snips = {}
    for host, d in HOSTS.items():
        ag = AGENTS[d["agent"]]
        css = "\n".join(
            f'<link rel="stylesheet" href="{href}?v=20261002-inner">' for href in ag["css"]
        )
        inject = (
            "<!-- dest inner chrome 20261002 -->\n"
            '<link rel="preconnect" href="https://fonts.googleapis.com">\n'
            '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
            '<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap" rel="stylesheet">\n'
            f"{css}\n"
        )
        snips[host] = {
            "skip": skip_link(skip_label(d["loc"])),
            "header": header_html(host, inner=True),
            "footer": footer_html(host),
            "inject": inject,
            "agent": d["agent"],
            "css": list(ag["css"]),
        }
    return snips


def _connect():
    try:
        import paramiko
    except ImportError:
        import subprocess

        subprocess.check_call([sys.executable, "-m", "pip", "install", "paramiko", "-q"])
        import paramiko

    password = os.environ.get("ORIGIN_SSH_PASS")
    if not password:
        raise SystemExit("Set ORIGIN_SSH_PASS")
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect("31.97.41.31", username="root", password=password, timeout=30)
    return client


def _run(client, cmd: str, timeout: int = 180) -> str:
    _, stdout, stderr = client.exec_command(cmd, timeout=timeout)
    return (stdout.read() + stderr.read()).decode(errors="replace").strip()


def dry_run(host: str | None = None) -> None:
    import urllib.request
    import ssl

    snips = build_snips()
    hosts = [host] if host else list(snips)
    ctx = ssl.create_default_context()
    samples = {
        "allchinabuyspreadsheet.ca": "/allchinabuy-shipping-guide/",
        "lovegobuy.nl": "/lovegobuy-shipping/",
        "cssbuyspreadsheet.ca": "/spreadsheet/",
        "superbuyspreadsheets.ca": "/about/",
        "bbdbuy.ca": "/bbdbuy-shipping/",
        "orientdig.at": "/orientdig-shipping/",
        "mycnbox.pl": "/mycnbox-spreadsheet/",
        "mulebuy.fr": "/how-to-use-mulebuy/",
        "usfansspreadsheet.nl": "/usfans-spreadsheet/",
        "cssbuyspreadsheets.de": "/guides/shipping/",
    }
    ok = 0
    for h in hosts:
        if h not in snips:
            print("SKIP unknown", h)
            continue
        path = samples.get(h)
        if not path:
            continue
        url = f"https://{h}{path}"
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 dest-inner-chrome"})
        raw = urllib.request.urlopen(req, timeout=25, context=ctx).read().decode("utf-8", "replace")
        out, why = wrap_html(raw, snips[h])
        art = extract_article(raw) or ""
        if out is None:
            print("FAIL", h, path, why, "article", _text_len(art))
            continue
        checks = [
            MARKER in out,
            "desk-cms.css" in out,
            'class="brand-logo"' in out,
            'class="site-header"' in out,
            'class="site-footer"' in out,
            "/#local" in out,
            "/#catalog" in out,
            "Georgia" not in out or "#00C853" not in out,
            _text_len(art) >= MIN_TEXT,
        ]
        if not all(checks):
            print("FAIL checks", h, checks)
            continue
        print(
            "OK",
            h,
            path,
            "in",
            len(raw),
            "out",
            len(out),
            "article_text",
            _text_len(art),
            snips[h]["agent"],
        )
        ok += 1
    print("dry-run ok", ok)


def put(*, only_host: str | None = None, limit: int = 0) -> None:
    snips = build_snips()
    inventory = Path("/tmp/dest-inners.json")
    if not inventory.is_file():
        raise SystemExit("missing /tmp/dest-inners.json")
    rows = json.loads(inventory.read_text())
    client = _connect()
    stamp = time.strftime("%Y%m%d-%H%M%S")
    bak = f"/www/backup/dest-inner-chrome-{stamp}"
    print(_run(client, f"mkdir -p '{bak}'"))
    sftp = client.open_sftp()
    cms_css = Path(__file__).resolve().parents[1] / "sites" / "shared" / "desk-cms.css"
    stats = {"ok": 0, "already": 0, "skip": 0, "fail": 0}
    fail_rows = []
    for row in rows:
        host = row["host"]
        if only_host and host != only_host:
            continue
        if host not in snips:
            print("SKIP host not in HOSTS", host)
            stats["skip"] += 1
            continue
        snip = snips[host]
        remote_root = f"/www/wwwroot/{host}"
        _run(client, f"mkdir -p '{remote_root}/assets/css' '{bak}/{host}'")
        if cms_css.is_file():
            sftp.put(str(cms_css), f"{remote_root}/assets/css/desk-cms.css")
            _run(client, f"chown www:www '{remote_root}/assets/css/desk-cms.css'")
        files = row.get("files") or []
        n = 0
        for item in files:
            rel = item["rel"].lstrip("/")
            if rel in SKIP_REL:
                stats["skip"] += 1
                continue
            remote = f"{remote_root}/{rel}"
            try:
                with sftp.open(remote, "r") as fh:
                    raw = fh.read().decode("utf-8", "replace")
            except OSError as exc:
                stats["fail"] += 1
                fail_rows.append((host, rel, f"read {exc}"))
                continue
            out, why = wrap_html(raw, snip)
            if out is None:
                stats[why if why in stats else "skip"] = stats.get(why if why in stats else "skip", 0) + 1
                if why not in {"already", "skip-georgia-shell"}:
                    if why not in stats:
                        stats["skip"] += 1
                    if why not in {"already"}:
                        fail_rows.append((host, rel, why))
                continue
            rel_dir = str(Path(rel).parent)
            _run(client, f"mkdir -p '{bak}/{host}/{rel_dir}' && cp -a '{remote}' '{bak}/{host}/{rel}'")
            tmp = f"{remote}.innernew"
            with sftp.open(tmp, "w") as fh:
                fh.write(out.encode("utf-8"))
            _run(client, f"mv -f '{tmp}' '{remote}' && chown www:www '{remote}'")
            stats["ok"] += 1
            n += 1
            if limit and stats["ok"] >= limit:
                break
        print("HOST", host, "wrapped", n, "/", len(files))
        if limit and stats["ok"] >= limit:
            break
    sftp.close()
    print("backup", bak)
    print("stats", json.dumps(stats, sort_keys=True))
    if fail_rows:
        print("issues", len(fail_rows))
        for host, rel, why in fail_rows[:40]:
            print(" ", why, host, rel)
    client.close()


def worker() -> None:
    snips = json.loads(Path("/tmp/inner-chrome-snips.json").read_text())
    rows = json.loads(Path("/tmp/dest-inners.json").read_text())
    only = os.environ.get("ONLY_HOST", "").strip()
    bak = os.environ.get("INNER_BAK", "").strip() or f"/www/backup/dest-inner-chrome-{time.strftime('%Y%m%d-%H%M%S')}"
    os.makedirs(bak, exist_ok=True)
    stats = {"ok": 0, "already": 0, "skip": 0, "fail": 0}
    issues = []
    for row in rows:
        host = row["host"]
        if only and host != only:
            continue
        if host not in snips:
            stats["skip"] += 1
            continue
        snip = snips[host]
        root = f"/www/wwwroot/{host}"
        host_bak = Path(bak) / host
        host_bak.mkdir(parents=True, exist_ok=True)
        wrapped = 0
        for item in row.get("files") or []:
            rel = item["rel"].lstrip("/")
            if rel in SKIP_REL:
                stats["skip"] += 1
                continue
            path = Path(root) / rel
            if not path.is_file():
                stats["fail"] += 1
                issues.append((host, rel, "missing"))
                continue
            raw = path.read_text(encoding="utf-8", errors="replace")
            out, why = wrap_html(raw, snip)
            if out is None:
                if why == "already":
                    stats["already"] += 1
                else:
                    stats["skip"] += 1
                    issues.append((host, rel, why))
                continue
            dest_bak = host_bak / rel
            dest_bak.parent.mkdir(parents=True, exist_ok=True)
            dest_bak.write_bytes(path.read_bytes())
            path.write_text(out, encoding="utf-8")
            try:
                import grp
                import pwd

                os.chown(path, pwd.getpwnam("www").pw_uid, grp.getgrnam("www").gr_gid)
            except Exception:
                pass
            stats["ok"] += 1
            wrapped += 1
        print("HOST", host, "wrapped", wrapped, "/", len(row.get("files") or []))
    print("backup", bak)
    print("stats", json.dumps(stats, sort_keys=True))
    print("issues", len(issues))
    for host, rel, why in issues[:80]:
        print(" ", why, host, rel)


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "dry-run"
    if cmd == "worker":
        worker()
    elif cmd == "put":
        host = sys.argv[2] if len(sys.argv) > 2 else None
        put(only_host=host)
    elif cmd == "put-one":
        put(only_host=sys.argv[2], limit=1)
    elif cmd == "snips":
        out = Path("/tmp/inner-chrome-snips.json")
        out.write_text(json.dumps(build_snips()), encoding="utf-8")
        print("wrote", out, "hosts", len(json.loads(out.read_text())))
    else:
        dry_run(sys.argv[2] if len(sys.argv) > 2 else None)
