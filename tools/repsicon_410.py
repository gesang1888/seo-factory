#!/usr/bin/env python3
"""410 thin repsicon leftover; strip remote-eval prepends on origin PHP.

Not a dest overlay. FashionReps / HubBuy unique CMS stay.

Gates this change honours:
1–3. No dest copy is rewritten. No invite, no 58-line snapshot, no
   customs coaching added.
4. FashionReps unique hub stays independently open (no 301).
5. No twins on repsicon. After 410, deep paths are Gone, not a fake dest.
6. Unique PHP/HTML hubs are not replaced with a 5KB country template.
   Only the thin Baota leftover is 410’d. Remote-eval prepends are stripped
   from Eyou index.php so unique FashionReps HTML keeps rendering.

Skip unique dest overwrite. Skip w2clinks PHP overlay.
"""
from __future__ import annotations

import os
import re
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# Generic remote-eval prepend used on leftover Eyou index.php files.
# Do not hard-code a payload URL.
EVAL_LINE = re.compile(
    r"^\s*eval\s*\(\s*['\"]\?>['\"]\s*\.\s*file_get_contents\s*\(\s*base64_decode\s*\([^;]+;\s*$",
    re.M,
)
INI_OFF = re.compile(r"^\s*ini_set\(\s*[\"']display_errors[\"']\s*,\s*[\"']off[\"']\s*\)\s*;\s*$", re.M)

STRIP_HOSTS = (
    "repsicon.com",
    "fashionrepsspreadsheet.com",
    "cnbuysheet.net",
    "usfans.cheap",
)
QUARANTINE = (
    "repsicon.com/i.php",
)
FASHION_MIN = 80000
FASHION_HOST = "fashionrepsspreadsheet.com"
FASHION_FP = "not a customs territory"
FASHION_CHROME = (
    "FashionReps Spreadsheet 2026",
    'id="local"',
)


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


def _run(client, cmd: str, timeout: int = 90) -> str:
    _, stdout, stderr = client.exec_command(cmd, timeout=timeout)
    return (stdout.read() + stderr.read()).decode(errors="replace").strip()


def _strip_eval(raw: str) -> str:
    lines = raw.splitlines(keepends=True)
    if not lines or not lines[0].lstrip().startswith("<?php"):
        raise RuntimeError("not a PHP bootstrap")
    out = [lines[0]]
    i = 1
    while i < len(lines):
        s = lines[i].strip()
        if not s:
            i += 1
            continue
        if INI_OFF.match(s) or EVAL_LINE.match(s):
            i += 1
            continue
        break
    out.extend(lines[i:])
    text = "".join(out)
    text = re.sub(r"\n{3,}", "\n\n", text)
    if EVAL_LINE.search(text):
        raise RuntimeError("eval prepend still present after strip")
    if "file_get_contents" in text and "base64_decode" in text:
        raise RuntimeError("base64 remote fetch still present")
    if "<?php" not in text:
        raise RuntimeError("stripped PHP no longer starts as PHP")
    return text


def put() -> None:
    client = _connect()
    stamp = time.strftime("%Y%m%d-%H%M%S")
    bak = f"/www/backup/repsicon-410-{stamp}"
    _run(client, f"mkdir -p '{bak}'")
    sftp = client.open_sftp()

    for host in STRIP_HOSTS:
        remote = f"/www/wwwroot/{host}/index.php"
        exists = _run(client, f"test -f '{remote}' && echo yes || echo no")
        if exists.strip() != "yes":
            print("skip missing", remote)
            continue
        _run(client, f"cp -a '{remote}' '{bak}/{host}.index.php'")
        with sftp.file(remote, "r") as fh:
            raw = fh.read().decode("utf-8", "replace")
        if "file_get_contents" not in raw or "base64_decode" not in raw:
            print("already clean", remote)
            continue
        cleaned = _strip_eval(raw)
        with sftp.file(remote, "w") as fh:
            fh.write(cleaned)
        print("stripped eval", remote, "bytes", len(cleaned.encode()))

    for rel in QUARANTINE:
        remote = f"/www/wwwroot/{rel}"
        exists = _run(client, f"test -f '{remote}' && echo yes || echo no")
        if exists.strip() == "yes":
            _run(client, f"cp -a '{remote}' '{bak}/{rel.replace('/', '_')}'")
            _run(client, f"mv '{remote}' '{remote}.bak-probe'")
            print("quarantined", remote)

    vhost = "/www/server/panel/vhost/nginx/repsicon.com.conf"
    rewrite = "/www/server/panel/vhost/rewrite/repsicon.com.conf"
    _run(client, f"cp -a '{vhost}' '{bak}/repsicon.com.conf'")
    _run(client, f"cp -a '{rewrite}' '{bak}/repsicon.com.rewrite.conf' 2>/dev/null || true")
    with sftp.file(rewrite, "w") as fh:
        fh.write("# thin leftover + remote-eval index.php; 410 Gone\nreturn 410;\n")
    print("wrote rewrite 410 for repsicon.com")

    live_fr = _run(client, f"wc -c < /www/wwwroot/{FASHION_HOST}/index.html")
    print("fashionreps index.html on disk", live_fr, "(not overwritten)")

    nginx_t = _run(client, "nginx -t 2>&1")
    print(nginx_t)
    if "successful" not in nginx_t.lower() and "ok" not in nginx_t.lower():
        raise SystemExit("nginx -t failed; not reloading")
    print(_run(client, "nginx -s reload 2>&1"))
    sftp.close()
    print("backup", bak)
    client.close()


def live_check() -> None:
    import urllib.request

    class NR(urllib.request.HTTPRedirectHandler):
        def redirect_request(self, req, fp, code, msg, headers, newurl):
            return None

    def fetch(url, follow=True):
        req = urllib.request.Request(
            url,
            headers={
                "User-Agent": "repsicon-410-check/1.0",
                "Cache-Control": "no-cache",
            },
        )
        opener = urllib.request.build_opener() if follow else urllib.request.build_opener(NR)
        try:
            with opener.open(req, timeout=25) as resp:
                return resp.status, resp.geturl(), resp.headers.get("Location") or "", resp.read()
        except urllib.error.HTTPError as e:
            return e.code, url, e.headers.get("Location") or "", e.read() if e.fp else b""

    fail = 0
    for url in ("https://repsicon.com/", "https://www.repsicon.com/", "https://repsicon.com/liang.php"):
        code, _, loc, body = fetch(url, follow=False)
        print(f"repsicon {url} {code} loc={loc} bytes={len(body)}")
        if code != 410:
            print("  FAIL expected 410")
            fail += 1
        text = body.decode("utf-8", "replace")
        if "file_get_contents" in text or "base64_decode" in text:
            print("  FAIL leaked PHP source")
            fail += 1

    code, _, loc, body = fetch(f"https://{FASHION_HOST}/", follow=True)
    html = body.decode("utf-8", "replace")
    print(f"fashionreps {code} bytes={len(body)} local={'id=\"local\"' in html} fp={FASHION_FP in html}")
    if code != 200 or len(body) < FASHION_MIN:
        print("  FAIL unique FashionReps hub collapsed", code, len(body))
        fail += 1
    if FASHION_FP not in html:
        print("  FAIL hub fingerprint gone")
        fail += 1
    for marker in FASHION_CHROME:
        if marker not in html:
            print("  FAIL chrome", marker)
            fail += 1
    if re.search(r"58 l[ií]neas para Espa|23[,.]81\s*USD", html, flags=re.I):
        print("  FAIL snapshot")
        fail += 1
    title_m = re.search(r"<title>(.*?)</title>", html, flags=re.S)
    title = title_m.group(1) if title_m else ""
    if re.search(r"invite\s*(code)?\s*[A-Z0-9]{5,}", title, flags=re.I):
        print("  FAIL invite in title")
        fail += 1
    if code in (301, 302):
        print("  FAIL fashionreps 301", loc)
        fail += 1

    code, _, loc, _ = fetch(f"https://{FASHION_HOST}/", follow=False)
    if code in (301, 302, 303, 307, 308):
        print("FAIL fashionreps redirect", loc)
        fail += 1
    else:
        print("indep fashionreps", code)

    code, _, loc, body = fetch("https://w2crep.org/", follow=False)
    if code != 200 or len(body) < 40000:
        print("FAIL w2crep hub", code, len(body))
        fail += 1
    else:
        print("indep w2crep", code, len(body))

    if fail:
        raise SystemExit(f"live_check failures: {fail}")
    print("live_check ok")


def main() -> None:
    if "--put" in sys.argv:
        put()
        return
    if "--check" in sys.argv:
        live_check()
        return
    print("usage: repsicon_410.py --put | --check")


if __name__ == "__main__":
    main()
