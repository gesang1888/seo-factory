#!/usr/bin/env python3
"""Build dest-only sitemap.xml for NL-complete country desks, PUT, GSC submit.

Does not call Indexing API. Does not PUT hubs, .cheap, hipobuy.es, sugargoo.ca/.es,
cssbuy.co.uk, cssbuyspreadsheet.de, or repsicon.com. Drops loc URLs whose host
is not this dest.
"""
from __future__ import annotations

import json
import os
import re
import ssl
import sys
import time
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from html import escape
from pathlib import Path
from urllib.parse import urljoin, urlparse

ROOT = Path(__file__).resolve().parents[1]
HOSTS_FILE = ROOT / "data" / "dest-nl-hosts.txt"
OUT_DIR = ROOT / "data" / "dest-sitemaps"
REPORT = Path("/tmp/dest-desk-sitemaps.json")
LASTMOD = "2026-10-07"
UA = "Mozilla/5.0 (compatible; dest-desk-sitemaps/1.0)"
CTX = ssl.create_default_context()
DESK_HINTS = (
    "/start/",
    "/start",
    "/catalog",
    "/catalogus",
    "/katalog",
    "/catalogo",
    "/catalogue",
    "/help",
    "/hulp",
    "/hilfe",
    "/ayuda",
    "/aide",
    "/aiuto",
    "/news",
    "/nieuws",
    "/aktuelles",
    "/noticias",
    "/actualites",
    "/about",
    "/over-ons",
    "/ueber-uns",
    "/sobre-nosotros",
    "/a-propos",
    "/chi-siamo",
    "/shipping",
    "/verzending",
    "/versand",
    "/envio",
    "/envoi",
    "/spedizione",
    "/how-to-use",
    "/handleiding",
    "/anleitung",
    "/guide",
    "/guia",
)
SKIP_PATH_RE = re.compile(
    r"^/(assets|img|images|css|js|static|api|favicon|xmlrpc)(/|$)|"
    r"\.(png|jpe?g|gif|webp|svg|ico|css|js|woff2?|map|txt|pdf)$",
    re.I,
)


def hosts() -> list[str]:
    return [ln.strip() for ln in HOSTS_FILE.read_text().splitlines() if ln.strip() and not ln.startswith("#")]


def _get(url: str, timeout: int = 18) -> tuple[int, str, str]:
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, context=CTX, timeout=timeout) as resp:
            body = resp.read().decode("utf-8", "replace")
            return resp.status, resp.geturl(), body
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", "replace") if exc.fp else ""
        return exc.code, url, body
    except Exception as exc:  # noqa: BLE001
        return 0, url, str(exc)[:180]


def _norm_path(path: str) -> str:
    path = path.split("?")[0].split("#")[0]
    if not path.startswith("/"):
        path = "/" + path
    if path != "/" and not path.endswith("/") and "." not in path.rsplit("/", 1)[-1]:
        path += "/"
    return path


def _is_desk(path: str) -> bool:
    low = path.lower()
    return any(h in low for h in DESK_HINTS)


def extract_paths(host: str, html: str) -> set[str]:
    found: set[str] = {"/", "/start/"}
    for raw in re.findall(r"""href=["']([^"']+)["']""", html, re.I):
        raw = raw.strip()
        if not raw or raw.startswith(("mailto:", "tel:", "javascript:")):
            continue
        if raw.startswith("//"):
            raw = "https:" + raw
        if raw.startswith("http"):
            p = urlparse(raw)
            if p.netloc.lower().removeprefix("www.") != host.lower().removeprefix("www."):
                continue
            path = p.path or "/"
        else:
            path = urlparse(urljoin(f"https://{host}/", raw)).path or "/"
        path = _norm_path(path)
        if SKIP_PATH_RE.search(path):
            continue
        found.add(path)
    return found


def existing_locs(host: str, xml: str) -> tuple[list[str], int]:
    """Same-host loc paths only. Returns (paths, dropped_foreign_count)."""
    keep: list[str] = []
    dropped = 0
    for loc in re.findall(r"<loc>\s*([^<\s]+)\s*</loc>", xml, re.I):
        loc = loc.replace("&amp;", "&").strip()
        p = urlparse(loc)
        net = (p.netloc or host).lower().removeprefix("www.")
        if net != host.lower().removeprefix("www."):
            dropped += 1
            continue
        keep.append(_norm_path(p.path or "/"))
    return keep, dropped


def priority(path: str) -> str:
    if path == "/":
        return "1.0"
    if path == "/start/" or _is_desk(path):
        return "0.8"
    return "0.5"


def render_sitemap(host: str, paths: list[str]) -> str:
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
    ]
    for path in paths:
        loc = f"https://{host}{path}" if path != "/" else f"https://{host}/"
        lines.append("  <url>")
        lines.append(f"    <loc>{escape(loc)}</loc>")
        lines.append(f"    <lastmod>{LASTMOD}</lastmod>")
        lines.append("    <changefreq>weekly</changefreq>")
        lines.append(f"    <priority>{priority(path)}</priority>")
        lines.append("  </url>")
    lines.append("</urlset>")
    lines.append("")
    return "\n".join(lines)


def collect_one(host: str) -> dict:
    home_code, home_final, home_html = _get(f"https://{host}/")
    sm_code, _, sm_xml = _get(f"https://{host}/sitemap.xml")
    row: dict = {
        "host": host,
        "home_code": home_code,
        "home_final": home_final,
        "sitemap_code": sm_code,
        "dropped_foreign": 0,
        "paths": [],
        "desk": [],
        "ok": False,
        "skip": "",
    }
    if home_code != 200:
        row["skip"] = f"home {home_code}"
        return row
    final_host = urlparse(home_final).netloc.lower().removeprefix("www.")
    if final_host and final_host != host.lower().removeprefix("www.") and final_host != host.lower():
        row["skip"] = f"home 301 {final_host}"
        return row
    paths = extract_paths(host, home_html)
    if sm_code == 200 and "<urlset" in sm_xml:
        old, dropped = existing_locs(host, sm_xml)
        row["dropped_foreign"] = dropped
        paths.update(old)
    start_code, _, _ = _get(f"https://{host}/start/")
    if start_code != 200:
        paths.discard("/start/")
        paths.discard("/start")
    ordered = sorted(paths, key=lambda p: (0 if p == "/" else 1 if p == "/start/" else 2 if _is_desk(p) else 3, p))
    row["paths"] = ordered
    row["desk"] = [p for p in ordered if p == "/" or p == "/start/" or _is_desk(p)]
    row["ok"] = True
    xml = render_sitemap(host, ordered)
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUT_DIR / f"{host}.xml").write_text(xml, encoding="utf-8")
    return row


def cmd_build() -> dict:
    rows = []
    hs = hosts()
    print("build dests", len(hs))
    with ThreadPoolExecutor(max_workers=12) as pool:
        futs = {pool.submit(collect_one, h): h for h in hs}
        for fut in as_completed(futs):
            row = fut.result()
            rows.append(row)
            flag = "OK" if row["ok"] else "SKIP"
            print(
                flag,
                row["host"],
                "home",
                row["home_code"],
                "sm",
                row["sitemap_code"],
                "n",
                len(row["paths"]),
                "desk",
                len(row["desk"]),
                "foreign",
                row["dropped_foreign"],
                row.get("skip") or "",
            )
    rows.sort(key=lambda r: r["host"])
    report = {
        "ok": [r["host"] for r in rows if r["ok"]],
        "skip": [{"host": r["host"], "reason": r["skip"]} for r in rows if not r["ok"]],
        "rows": rows,
    }
    REPORT.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print("ok", len(report["ok"]), "skip", len(report["skip"]), "wrote", REPORT)
    return report


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


def _run(client, cmd: str, timeout: int = 60) -> str:
    _, stdout, stderr = client.exec_command(cmd, timeout=timeout)
    return (stdout.read() + stderr.read()).decode(errors="replace").strip()


def cmd_put() -> dict:
    if not REPORT.exists():
        cmd_build()
    report = json.loads(REPORT.read_text())
    client = _connect()
    sftp = client.open_sftp()
    stamp = time.strftime("%Y%m%d-%H%M%S")
    put_ok, put_fail = [], []
    for host in report["ok"]:
        local = OUT_DIR / f"{host}.xml"
        remote = f"/www/wwwroot/{host}/sitemap.xml"
        if not local.exists():
            put_fail.append({"host": host, "error": "missing local xml"})
            continue
        exists = _run(client, f"test -d /www/wwwroot/{host} && echo YES || echo NO")
        if exists != "YES":
            put_fail.append({"host": host, "error": "no wwwroot"})
            continue
        xml = local.read_text(encoding="utf-8")
        if f"https://{host}/" not in xml:
            put_fail.append({"host": host, "error": "xml missing self host"})
            continue
        foreign = re.findall(r"<loc>\s*https?://([^/<]+)", xml)
        bad = [n for n in foreign if n.lower().removeprefix("www.") != host.lower().removeprefix("www.")]
        if bad:
            put_fail.append({"host": host, "error": f"foreign loc {bad[:3]}"})
            continue
        bak = f"/www/backup/dest-sitemap-{host}-{stamp}.xml"
        _run(client, f"test -f '{remote}' && cp -a '{remote}' '{bak}' || true")
        tmp = f"/tmp/dest-sm-{host}.xml"
        with sftp.open(tmp, "w") as fh:
            fh.write(xml)
        _run(client, f"mv '{tmp}' '{remote}' && chown www:www '{remote}' && chmod 644 '{remote}'")
        print("PUT", host, local.stat().st_size)
        put_ok.append(host)
    sftp.close()
    client.close()
    report["put_ok"] = put_ok
    report["put_fail"] = put_fail
    REPORT.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print("put_ok", len(put_ok), "put_fail", len(put_fail))
    return report


def cmd_gsc() -> dict:
    if not REPORT.exists():
        raise SystemExit("run build/put first")
    report = json.loads(REPORT.read_text())
    try:
        from google.oauth2 import service_account
        from googleapiclient.discovery import build
    except ImportError:
        import subprocess

        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "google-api-python-client", "google-auth", "-q"]
        )
        from google.oauth2 import service_account
        from googleapiclient.discovery import build

    sa = os.environ.get("GSC_SA_JSON", "/tmp/hipobuy-creds/sa.json")
    creds = service_account.Credentials.from_service_account_file(
        sa, scopes=["https://www.googleapis.com/auth/webmasters"]
    )
    gsc = build("searchconsole", "v1", credentials=creds, cache_discovery=False)
    listed = {
        row["siteUrl"]: row.get("permissionLevel")
        for row in gsc.sites().list().execute().get("siteEntry", [])
    }

    def prop_for(host: str) -> str | None:
        for cand in (f"sc-domain:{host}", f"https://{host}/", f"http://{host}/"):
            if cand in listed:
                return cand
        return None

    sitemap_ok, sitemap_fail, missing = [], [], []
    targets = report.get("put_ok") or report.get("ok") or []
    for host in targets:
        use = prop_for(host)
        perm = listed.get(use) if use else None
        if not use:
            print("GSC_MISSING", host)
            missing.append(host)
            continue
        if perm not in ("siteOwner", "siteFullUser"):
            print("GSC_NOT_OWNER", host, perm)
            missing.append(host)
            continue
        feed = f"https://{host}/sitemap.xml"
        try:
            gsc.sitemaps().submit(siteUrl=use, feedpath=feed).execute()
            print("SITEMAP", host)
            sitemap_ok.append(host)
        except Exception as exc:  # noqa: BLE001
            print("SITEMAP_FAIL", host, type(exc).__name__, str(exc)[:180])
            sitemap_fail.append({"host": host, "error": str(exc)[:240]})
        time.sleep(0.08)
    report["gsc_ok"] = sitemap_ok
    report["gsc_fail"] = sitemap_fail
    report["gsc_missing"] = missing
    REPORT.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(
        "gsc_ok",
        len(sitemap_ok),
        "gsc_fail",
        len(sitemap_fail),
        "gsc_missing",
        len(missing),
    )
    return report


def cmd_live() -> None:
    hs = hosts()
    bad = 0
    for host in hs:
        code, _, body = _get(f"https://{host}/sitemap.xml")
        n = body.count("<loc>")
        start = f"https://{host}/start/" in body
        foreign = 0
        for loc in re.findall(r"<loc>\s*([^<\s]+)", body or ""):
            net = urlparse(loc).netloc.lower().removeprefix("www.")
            if net and net != host.lower().removeprefix("www."):
                foreign += 1
        ok = code == 200 and n >= 2 and foreign == 0
        if not ok:
            bad += 1
        print(
            ("OK" if ok else "BAD"),
            host,
            code,
            "n",
            n,
            "start",
            start,
            "foreign",
            foreign,
        )
    if bad:
        raise SystemExit(f"live_check failed {bad}")
    print("live_check ok", len(hs))


def main() -> None:
    cmd = sys.argv[1] if len(sys.argv) > 1 else "all"
    if cmd == "build":
        cmd_build()
    elif cmd == "put":
        cmd_put()
    elif cmd == "gsc":
        cmd_gsc()
    elif cmd == "live":
        cmd_live()
    elif cmd == "all":
        cmd_build()
        cmd_put()
        cmd_gsc()
    else:
        raise SystemExit("usage: dest_desk_sitemaps.py [build|put|gsc|live|all]")


if __name__ == "__main__":
    main()
