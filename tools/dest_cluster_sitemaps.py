#!/usr/bin/env python3
"""Merge spreadsheet-cluster inner URLs into each dest sitemap.xml, PUT live, GSC-submit that one feed.

Does not call the Indexing API. Does not URL-inspect. Does not revive 301 twins.
Does not smash hipobuyspreadsheet.net. Preserves every existing <loc> (coupons, blog, …).
GSC: sitemaps().submit(siteUrl, feedpath=https://{host}/sitemap.xml) only.
"""
from __future__ import annotations

import json
import os
import re
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from html import unescape
from pathlib import Path
from urllib.error import HTTPError
from urllib.request import HTTPRedirectHandler, Request, build_opener, urlopen

_TOOLS = Path(__file__).resolve().parent
if str(_TOOLS) not in sys.path:
    sys.path.insert(0, str(_TOOLS))
from dest_spreadsheet_cluster import (  # noqa: E402
    PHP_CSSBUY,
    TWINS,
    UNIQUE_PHP_HUBS,
    _connect,
    _import_keep_maps,
    _norm_slug,
    _run,
    dest_hosts,
    map_pages,
    overlay_dir,
    spec_for,
)

ROOT = Path(__file__).resolve().parents[1]
TODAY = "2026-10-30"
SA = os.environ.get("GSC_SA_JSON", "/tmp/hipobuy-creds/sa.json")
GSC_SCOPES = ["https://www.googleapis.com/auth/webmasters"]
LOG = Path("/tmp/dest-cluster-sitemaps.json")
URL_BLOCK = re.compile(r"<url\b[^>]*>.*?</url>", re.I | re.S)
LOC_RE = re.compile(r"<loc>\s*([^<]+)\s*</loc>", re.I)
LASTMOD_RE = re.compile(r"<lastmod>[^<]*</lastmod>", re.I)
SAMPLE_HOSTS = (
    "cssbuy.es",
    "fansbuy.co.uk",
    "bbdbuy.it",
    "kakobuy.fi",
    "lovegobuy.nl",
    "acbuyspreadsheets.nl",
    "mycnbox.nl",
)
PHP_SKIP_SLUGS = {"/spreadsheet", "/guide/shipping", "/guide/customs", "/guide/first-order"}


class _NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def _active_hosts() -> list[str]:
    return [h for h in dest_hosts() if h not in TWINS and h not in UNIQUE_PHP_HUBS]


def _norm_loc(url: str) -> str:
    u = unescape((url or "").strip())
    u = re.sub(r"^https?://(www\.)?", "https://", u, flags=re.I)
    return u.rstrip("/").lower()


def _loc_from_slug(host: str, slug: str) -> str:
    slug = (slug or "/").strip() or "/"
    if slug == "/":
        return f"https://{host}/"
    slug = _norm_slug(slug)
    return f"https://{host}{slug}"


def cluster_locs(spec: dict) -> list[str]:
    host = spec["host"]
    php = host in PHP_CSSBUY
    seen: set[str] = set()
    out: list[str] = []
    slugs = ["/"]
    for slug, _path in map_pages(spec).values():
        if php and _norm_slug(slug).rstrip("/") in PHP_SKIP_SLUGS:
            continue
        slugs.append(slug)
    for loc in [_loc_from_slug(host, slug) for slug in slugs]:
        key = _norm_loc(loc)
        if key in seen:
            continue
        seen.add(key)
        out.append(loc)
    return out


def _head_status(url: str) -> tuple[int | str, str]:
    opener = build_opener(_NoRedirect)
    headers = {"User-Agent": "dest-cluster-sitemaps/1.0"}
    for method in ("HEAD", "GET"):
        req = Request(url, headers=headers, method=method)
        try:
            with opener.open(req, timeout=18) as resp:
                return resp.status, resp.geturl()
        except HTTPError as exc:
            loc = exc.headers.get("Location") or ""
            return exc.code, loc
        except Exception:
            continue
    return "ERR", ""


def filter_live_200(host: str, candidates: list[str], existing: set[str]) -> tuple[list[str], list[dict]]:
    """Keep locs already in the sitemap; only insert URLs that 200 on this host."""
    keep: list[str] = []
    probe: list[str] = []
    for loc in candidates:
        if _norm_loc(loc) in existing:
            keep.append(loc)
        else:
            probe.append(loc)
    dropped: list[dict] = []
    if not probe:
        return keep, dropped
    with ThreadPoolExecutor(max_workers=12) as pool:
        futs = {pool.submit(_head_status, url): url for url in probe}
        for fut in as_completed(futs):
            url = futs[fut]
            code, loc = fut.result()
            # Same-host 200/304 only. Cross-host 301 and internal aliases stay out.
            ok = code in (200, 304) and (not loc or _norm_loc(loc) == _norm_loc(url))
            if ok:
                keep.append(url)
            else:
                dropped.append({"url": url, "status": code, "location": loc[:180]})
    keep.sort(key=lambda u: (0 if _norm_loc(u) == _norm_loc(f"https://{host}/") else 1, u))
    return keep, dropped


def _url_block(loc: str, lastmod: str, priority: str) -> str:
    return (
        "  <url>\n"
        f"    <loc>{loc}</loc>\n"
        f"    <lastmod>{lastmod}</lastmod>\n"
        "    <changefreq>weekly</changefreq>\n"
        f"    <priority>{priority}</priority>\n"
        "  </url>\n"
    )


def _new_urlset(locs: list[str], host: str) -> str:
    home = _norm_loc(f"https://{host}/")
    parts = [
        '<?xml version="1.0" encoding="UTF-8"?>\n',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n',
    ]
    for loc in locs:
        pri = "1.0" if _norm_loc(loc) == home else "0.8"
        parts.append(_url_block(loc, TODAY, pri))
    parts.append("</urlset>\n")
    return "".join(parts)


def _set_lastmod(block: str) -> str:
    if LASTMOD_RE.search(block):
        return LASTMOD_RE.sub(f"<lastmod>{TODAY}</lastmod>", block, count=1)
    return re.sub(r"(</loc>)", rf"\1\n    <lastmod>{TODAY}</lastmod>", block, count=1, flags=re.I)


def _is_urlset(xml: str) -> bool:
    return bool(re.search(r"<urlset\b", xml, re.I))


def _is_index(xml: str) -> bool:
    return bool(re.search(r"<sitemapindex\b", xml, re.I))


def merge_urlset(xml: str, host: str, locs: list[str]) -> tuple[str, list[str], list[str]]:
    if not _is_urlset(xml):
        return _new_urlset(locs, host), list(locs), []
    blocks = URL_BLOCK.findall(xml)
    by_norm: dict[str, str] = {}
    order: list[str] = []
    for block in blocks:
        m = LOC_RE.search(block)
        if not m:
            continue
        key = _norm_loc(m.group(1))
        if key not in by_norm:
            order.append(key)
        by_norm[key] = block
    added: list[str] = []
    bumped: list[str] = []
    replacements: list[tuple[str, str]] = []
    for loc in locs:
        key = _norm_loc(loc)
        if key in by_norm:
            old = by_norm[key]
            new = _set_lastmod(old)
            if new != old:
                replacements.append((old, new))
                by_norm[key] = new
                bumped.append(loc)
        else:
            added.append(loc)
    out = xml
    for old, new in replacements:
        out = out.replace(old, new, 1)
    if added:
        home = _norm_loc(f"https://{host}/")
        insert = "".join(
            _url_block(loc, TODAY, "1.0" if _norm_loc(loc) == home else "0.8") for loc in added
        )
        if "</urlset>" in out:
            out = out.replace("</urlset>", insert + "</urlset>", 1)
        else:
            out = out.rstrip() + "\n" + insert + "</urlset>\n"
    if not out.endswith("\n"):
        out += "\n"
    return out, added, bumped


def merge_index(xml: str, host: str, locs: list[str]) -> tuple[str, str, bool]:
    child = f"https://{host}/sitemap-cluster.xml"
    child_xml = _new_urlset(locs, host)
    if _norm_loc(child) in {_norm_loc(m) for m in LOC_RE.findall(xml)}:
        xml = re.sub(
            rf"(<loc>\s*{re.escape(child)}\s*</loc>\s*)(?:<lastmod>[^<]*</lastmod>\s*)?",
            rf"\1<lastmod>{TODAY}</lastmod>\n    ",
            xml,
            count=1,
            flags=re.I,
        )
        return xml, child_xml, False
    block = (
        "  <sitemap>\n"
        f"    <loc>{child}</loc>\n"
        f"    <lastmod>{TODAY}</lastmod>\n"
        "  </sitemap>\n"
    )
    if "</sitemapindex>" in xml:
        xml = xml.replace("</sitemapindex>", block + "</sitemapindex>", 1)
    else:
        xml = xml.rstrip() + "\n" + block + "</sitemapindex>\n"
    if not xml.endswith("\n"):
        xml += "\n"
    return xml, child_xml, True


def _looks_like_sitemap(raw: str) -> bool:
    if not raw or len(raw) < 40:
        return False
    head = raw.lstrip()[:400].lower()
    if head.startswith("<!doctype") or "<html" in head[:80]:
        return False
    return _is_urlset(raw) or _is_index(raw)


def _read_remote(sftp, host: str) -> str:
    path = f"/www/wwwroot/{host}/sitemap.xml"
    try:
        with sftp.open(path, "r") as fh:
            raw = fh.read()
        if isinstance(raw, bytes):
            raw = raw.decode("utf-8", errors="replace")
        return raw
    except OSError:
        return ""


def generate(client=None) -> dict:
    keep_maps = _import_keep_maps()
    own_client = client is None
    if own_client:
        client = _connect()
    sftp = client.open_sftp()
    rows = []
    try:
        for host in _active_hosts():
            spec = spec_for(host, keep_maps)
            live = _read_remote(sftp, host)
            overlay = overlay_dir(host)
            local_sm = overlay / "sitemap.xml"
            source = "live"
            raw = live
            if not _looks_like_sitemap(raw):
                if local_sm.is_file():
                    raw = local_sm.read_text(encoding="utf-8", errors="replace")
                    source = "overlay"
                else:
                    raw = ""
                    source = "new"
            existing = {_norm_loc(m) for m in LOC_RE.findall(raw)} if _looks_like_sitemap(raw) else set()
            locs, dropped = filter_live_200(host, cluster_locs(spec), existing)
            extra_child = None
            added: list[str] = []
            bumped: list[str] = []
            if _looks_like_sitemap(raw) and _is_index(raw):
                merged, child_xml, child_new = merge_index(raw, host, locs)
                extra_child = child_xml
                added = locs if child_new else []
                bumped = [] if child_new else locs
                kind = "sitemapindex"
            else:
                merged, added, bumped = merge_urlset(raw if _looks_like_sitemap(raw) else "", host, locs)
                kind = "urlset"
            overlay.mkdir(parents=True, exist_ok=True)
            local_sm.write_text(merged, encoding="utf-8")
            child_rel = None
            if extra_child:
                child_path = overlay / "sitemap-cluster.xml"
                child_path.write_text(extra_child, encoding="utf-8")
                child_rel = str(child_path.relative_to(ROOT))
            row = {
                "host": host,
                "kind": kind,
                "source": source,
                "cluster": locs,
                "added": added,
                "bumped": bumped,
                "dropped_redirect": dropped,
                "url_count": len(LOC_RE.findall(merged)) if kind == "urlset" else len(locs),
                "local": str(local_sm.relative_to(ROOT)),
                "child": child_rel,
                "php": host in PHP_CSSBUY,
            }
            rows.append(row)
            print(
                "MERGE",
                host,
                kind,
                source,
                "added",
                len(added),
                "bumped",
                len(bumped),
                "drop",
                len(dropped),
                "urls",
                row["url_count"],
            )
    finally:
        sftp.close()
        if own_client:
            client.close()
    summary = {
        "at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "today": TODAY,
        "hosts": len(rows),
        "added_total": sum(len(r["added"]) for r in rows),
        "bumped_total": sum(len(r["bumped"]) for r in rows),
        "dropped_total": sum(len(r.get("dropped_redirect") or []) for r in rows),
        "rows": rows,
    }
    LOG.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(
        "GENERATE",
        len(rows),
        "added",
        summary["added_total"],
        "bumped",
        summary["bumped_total"],
        "dropped",
        summary["dropped_total"],
    )
    return summary


def put(summary: dict | None = None) -> dict:
    if summary is None:
        if LOG.is_file():
            summary = json.loads(LOG.read_text(encoding="utf-8"))
        else:
            summary = generate()
    client = _connect()
    stamp = time.strftime("%Y%m%d-%H%M%S")
    bak = f"/www/backup/dest-cluster-sitemaps-{stamp}"
    print(_run(client, f"mkdir -p '{bak}'"))
    sftp = client.open_sftp()
    put_ok: list[str] = []
    put_fail: list[dict] = []
    for row in summary.get("rows") or []:
        host = row["host"]
        local = ROOT / row["local"]
        if not local.is_file():
            put_fail.append({"host": host, "error": "missing local sitemap"})
            continue
        remote_root = f"/www/wwwroot/{host}"
        remote = f"{remote_root}/sitemap.xml"
        try:
            _run(client, f"mkdir -p '{bak}/{host}' '{remote_root}'")
            _run(client, f"test -f '{remote}' && cp -a '{remote}' '{bak}/{host}/sitemap.xml' || true")
            sftp.put(str(local), remote)
            chown = [f"chown www:www '{remote}'"]
            if row.get("child"):
                child_local = ROOT / row["child"]
                child_remote = f"{remote_root}/sitemap-cluster.xml"
                if child_local.is_file():
                    _run(
                        client,
                        f"test -f '{child_remote}' && cp -a '{child_remote}' '{bak}/{host}/sitemap-cluster.xml' || true",
                    )
                    sftp.put(str(child_local), child_remote)
                    chown.append(f"chown www:www '{child_remote}'")
            _run(client, " && ".join(chown))
            put_ok.append(host)
            print("PUT", host, "added", len(row.get("added") or []))
        except OSError as exc:
            print("PUT_FAIL", host, exc)
            put_fail.append({"host": host, "error": str(exc)[:240]})
    sftp.close()
    client.close()
    summary["backup"] = bak
    summary["put_ok"] = put_ok
    summary["put_fail"] = put_fail
    LOG.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print("PUT_DONE", len(put_ok), "fail", len(put_fail), "backup", bak)
    return summary


def verify(summary: dict | None = None) -> dict:
    if summary is None and LOG.is_file():
        summary = json.loads(LOG.read_text(encoding="utf-8"))
    summary = summary or {}
    by_host = {r["host"]: r for r in summary.get("rows") or []}
    checks = []
    for host in SAMPLE_HOSTS:
        row = by_host.get(host)
        url = f"https://{host}/sitemap.xml"
        item = {"host": host, "url": url}
        try:
            req = Request(url, headers={"User-Agent": "dest-cluster-sitemaps/1.0"})
            with urlopen(req, timeout=25) as resp:
                body = resp.read().decode("utf-8", errors="replace")
                item["http"] = resp.status
        except Exception as exc:  # noqa: BLE001
            item["error"] = str(exc)[:200]
            checks.append(item)
            print("VERIFY_FAIL", host, item.get("error"))
            continue
        locs = [_norm_loc(m) for m in LOC_RE.findall(body)]
        cluster = [_norm_loc(u) for u in (row or {}).get("cluster") or []]
        item["live_urls"] = len(locs)
        item["has_finds"] = any("finds" in loc for loc in locs)
        item["has_qc"] = any(re.search(r"(?:^|/)qc(?:/|$)|-qc(?:/|$)", loc) for loc in locs)
        if cluster:
            missing = [u for u in (row or {}).get("cluster") or [] if _norm_loc(u) not in locs]
            item["cluster_missing"] = missing
            item["cluster_ok"] = not missing
        # sitemapindex: cluster urls live in the child file
        if _is_index(body) and row and row.get("child"):
            child_url = f"https://{host}/sitemap-cluster.xml"
            try:
                creq = Request(child_url, headers={"User-Agent": "dest-cluster-sitemaps/1.0"})
                with urlopen(creq, timeout=20) as cresp:
                    child_http = cresp.status
                    cbody = cresp.read().decode("utf-8", errors="replace")
                clocs = {_norm_loc(m) for m in LOC_RE.findall(cbody)}
                item["child_http"] = child_http
                item["cluster_missing"] = [
                    u for u in (row or {}).get("cluster") or [] if _norm_loc(u) not in clocs
                ]
                item["cluster_ok"] = not item["cluster_missing"]
                item["has_finds"] = any("finds" in loc for loc in clocs)
            except Exception as exc:  # noqa: BLE001
                item["child_error"] = str(exc)[:200]
                item["cluster_ok"] = False
        checks.append(item)
        print(
            "VERIFY",
            host,
            "http",
            item.get("http"),
            "urls",
            item.get("live_urls"),
            "finds",
            item.get("has_finds"),
            "qc",
            item.get("has_qc"),
            "cluster_ok",
            item.get("cluster_ok"),
        )
    # Twin must stay a redirect and must not be in put_ok.
    twin = "cssbuy.at"
    twin_item = {"host": twin, "skipped": True}
    try:
        req = Request(
            f"https://{twin}/sitemap.xml",
            headers={"User-Agent": "dest-cluster-sitemaps/1.0"},
            method="GET",
        )
        with urlopen(req, timeout=20) as resp:
            twin_item["http"] = resp.status
            twin_item["final"] = resp.geturl()
    except Exception as exc:  # noqa: BLE001
        twin_item["error"] = str(exc)[:200]
    twin_item["in_put_ok"] = twin in (summary.get("put_ok") or [])
    checks.append(twin_item)
    print("VERIFY_TWIN", twin, twin_item)
    summary["verify"] = checks
    LOG.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    bad = [
        c
        for c in checks
        if c.get("host") != twin and (c.get("cluster_ok") is False or c.get("http") not in (200, None))
    ]
    if bad:
        print("VERIFY_WARN", [c["host"] for c in bad])
    return summary


def _gsc_service():
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

    creds = service_account.Credentials.from_service_account_file(SA, scopes=GSC_SCOPES)
    return build("searchconsole", "v1", credentials=creds, cache_discovery=False)


def _property(listed: dict, host: str) -> str | None:
    for cand in (f"sc-domain:{host}", f"https://{host}/", f"http://{host}/"):
        if cand in listed:
            return cand
    return None


def gsc_submit(summary: dict | None = None) -> dict:
    if "indexing" in " ".join(GSC_SCOPES).lower():
        raise SystemExit("refusing indexing scope")
    if summary is None and LOG.is_file():
        summary = json.loads(LOG.read_text(encoding="utf-8"))
    summary = summary or {}
    hosts = list(summary.get("put_ok") or [])
    if not hosts:
        hosts = [r["host"] for r in summary.get("rows") or []]
    gsc = _gsc_service()
    listed = {
        row["siteUrl"]: row.get("permissionLevel")
        for row in gsc.sites().list().execute().get("siteEntry", [])
    }
    sitemap_ok: list[dict] = []
    sitemap_fail: list[dict] = []
    missing: list[str] = []
    print("GSC properties", len(listed), "submit", len(hosts), "scope", GSC_SCOPES)
    for host in hosts:
        if host in TWINS or host in UNIQUE_PHP_HUBS:
            print("SKIP_TWIN", host)
            continue
        use = _property(listed, host)
        perm = listed.get(use) if use else None
        if not use:
            print("MISSING", host)
            missing.append(host)
            continue
        if perm and perm not in ("siteOwner", "siteFullUser"):
            print("NOT_OWNER", host, perm)
            missing.append(host)
            continue
        feed = f"https://{host}/sitemap.xml"
        try:
            gsc.sitemaps().submit(siteUrl=use, feedpath=feed).execute()
            print("SITEMAP", host, use)
            sitemap_ok.append({"host": host, "site": use, "feed": feed})
        except Exception as exc:  # noqa: BLE001
            print("SITEMAP_FAIL", host, type(exc).__name__, str(exc)[:180])
            sitemap_fail.append({"host": host, "site": use, "error": str(exc)[:240]})
        time.sleep(0.35)
    summary["gsc"] = {
        "ok": sitemap_ok,
        "fail": sitemap_fail,
        "missing": missing,
        "indexing": False,
        "submitted_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "feed": "https://{host}/sitemap.xml",
    }
    LOG.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(
        "GSC_DONE sitemap_ok",
        len(sitemap_ok),
        "fail",
        len(sitemap_fail),
        "missing",
        len(missing),
        "indexing",
        False,
    )
    return summary


def main() -> None:
    cmd = sys.argv[1] if len(sys.argv) > 1 else "all"
    if cmd == "generate":
        generate()
    elif cmd == "put":
        put()
    elif cmd == "verify":
        verify()
    elif cmd == "gsc":
        gsc_submit()
    elif cmd == "all":
        summary = generate()
        summary = put(summary)
        summary = verify(summary)
        gsc_submit(summary)
    else:
        raise SystemExit(f"unknown cmd {cmd}")


if __name__ == "__main__":
    main()
