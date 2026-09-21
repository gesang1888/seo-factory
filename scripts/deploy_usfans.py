#!/usr/bin/env python3
"""Deploy the USFans SEO overlay onto the Baota VPS.

Uploads overlay HTML onto usfansspreadsheet.net without wiping api/,
styles.css, images or PHP. Adds thin-page 301s and points sibling
ccTLDs at the canonical host.

  export USFANS_DEPLOY_PASS='...'
  python3 scripts/deploy_usfans.py
"""

from __future__ import annotations

import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

try:
    import paramiko
except ImportError:
    import subprocess

    subprocess.check_call([sys.executable, "-m", "pip", "install", "paramiko", "-q"])
    import paramiko

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.usfans_config import (  # noqa: E402
    CANONICAL_HOST,
    CANONICAL_ORIGIN,
    KEEP_PATHS,
    path_variants,
    thin_redirects,
)

HOST = os.environ.get("USFANS_DEPLOY_HOST", "31.97.41.31")
USER = os.environ.get("USFANS_DEPLOY_USER", "root")
WEBROOT = "/www/wwwroot"
NGINX_DIR = "/www/server/panel/vhost/nginx"
CERT_DIR = "/www/server/panel/vhost/cert"
OVERLAY = ROOT / "sites" / "usfansspreadsheet.net" / "overlay"

# .org is not on this VPS (Hostinger). Only these siblings live here.
SATELLITES_ON_VPS = [
    "usfansspreadsheet.uk",
    "usfansspreadsheet.co.uk",
    "usfansspreadsheet.nl",
]

SKIP_UPLOAD_NAMES = {
    "nginx",
    "cloudflare",
    "_redirects",
    "styles.css",
    "usfanslogo.png",
}

KEEP_REMOTE = {
    "api",
    "assets",
    "css",
    "images",
    "js",
    "public",
    "wd-img",
    "styles.css",
    "usfanslogo.png",
    ".user.ini",
    ".htaccess",
    ".well-known",
    "favicon.ico",
}

STAMP = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")

ALIAS_REDIRECTS = {
    "/shipping.html": "/usfans-shipping-guide/",
    "/shipping": "/usfans-shipping-guide/",
    "/shipping/": "/usfans-shipping-guide/",
    "/spreadsheet": "/usfans-spreadsheet/",
    "/spreadsheet/": "/usfans-spreadsheet/",
    "/coupons": "/usfans-coupons/",
    "/coupons/": "/usfans-coupons/",
    "/feed": "/",
    "/feed/": "/",
    "/404": "/",
    "/404/": "/",
}


def connect() -> paramiko.SSHClient:
    password = os.environ.get("USFANS_DEPLOY_PASS") or os.environ.get("ORIENTDIG_DEPLOY_PASS")
    if not password:
        print("Set USFANS_DEPLOY_PASS", file=sys.stderr)
        sys.exit(1)
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(HOST, username=USER, password=password, timeout=30)
    return client


def run(client: paramiko.SSHClient, cmd: str, timeout: int = 120) -> str:
    _, stdout, stderr = client.exec_command(cmd, timeout=timeout)
    return (stdout.read() + stderr.read()).decode(errors="replace").strip()


def mkdir_p(sftp: paramiko.SFTPClient, remote: str) -> None:
    parts = remote.strip("/").split("/")
    built = ""
    for part in parts:
        built += f"/{part}"
        try:
            sftp.stat(built)
        except OSError:
            sftp.mkdir(built)


def upload_file(sftp: paramiko.SFTPClient, local: Path, remote: str) -> None:
    mkdir_p(sftp, "/".join(remote.split("/")[:-1]))
    sftp.put(str(local), remote)


def upload_overlay(client: paramiko.SSHClient) -> int:
    remote_root = f"{WEBROOT}/{CANONICAL_HOST}"
    sftp = client.open_sftp()
    count = 0
    for path in sorted(OVERLAY.rglob("*")):
        rel = path.relative_to(OVERLAY).as_posix()
        top = rel.split("/", 1)[0]
        if top in SKIP_UPLOAD_NAMES or path.name in SKIP_UPLOAD_NAMES:
            continue
        if not path.is_file():
            continue
        remote = f"{remote_root}/{rel}"
        upload_file(sftp, path, remote)
        count += 1
    sftp.close()
    run(client, f"chown -R www:www {remote_root}")
    return count


def slash_normalize_conf() -> str:
    lines = ["# Keep-page slash normalization. Thin URLs live in thin-redirects.conf.", ""]
    used = set()
    for path in KEEP_PATHS:
        if not path.endswith("/") or path == "/":
            continue
        bare = path.rstrip("/")
        if bare in used:
            continue
        used.add(bare)
        lines.append(f"location = {bare} {{ return 301 {CANONICAL_ORIGIN}{path}; }}")
    for src, dest in ALIAS_REDIRECTS.items():
        if src in used:
            continue
        used.add(src)
        abs_dest = dest if dest.startswith("http") else CANONICAL_ORIGIN + dest
        lines.append(f"location = {src} {{ return 301 {abs_dest}; }}")
    lines.append("")
    return "\n".join(lines)


def thin_conf() -> str:
    lines = ["# Thin brand/dupe spreadsheet URLs → real category or live sheet.", ""]
    for src, dest in sorted(thin_redirects().items()):
        abs_dest = dest if dest.startswith("http") else dest
        for variant in path_variants(src):
            if variant == "/":
                continue
            lines.append(f"location = {variant} {{")
            lines.append(f"    return 301 {abs_dest};")
            lines.append("}")
            lines.append("")
    return "\n".join(lines)


def patch_satellite_nginx(conf: str, domain: str) -> str:
    conf = conf.replace(
        f"return 301 https://{domain}$request_uri;",
        f"return 301 {CANONICAL_ORIGIN}$request_uri;",
    )
    conf = re.sub(
        r"location / \{\s*try_files \$uri \$uri/ \$uri/index.html =404;\s*\}",
        "location / {\n        return 301 https://usfansspreadsheet.net$request_uri;\n    }",
        conf,
    )
    return conf


def write_nginx_snippets(client: paramiko.SSHClient) -> None:
    sftp = client.open_sftp()
    ext_dir = f"{NGINX_DIR}/extension/{CANONICAL_HOST}"
    mkdir_p(sftp, ext_dir)

    gsc_path = f"{ext_dir}/gsc-redirects.conf"
    thin_path = f"{ext_dir}/thin-redirects.conf"
    run(client, f"cp -a {gsc_path} {gsc_path}.bak-{STAMP} 2>/dev/null || true")

    with sftp.file(gsc_path, "w") as fh:
        fh.write(slash_normalize_conf())
    with sftp.file(thin_path, "w") as fh:
        fh.write(thin_conf())

    for domain in SATELLITES_ON_VPS:
        conf_path = f"{NGINX_DIR}/{domain}.conf"
        run(client, f"cp -a {conf_path} {conf_path}.bak-decluster-{STAMP}")
        with sftp.file(conf_path, "r") as fh:
            original = fh.read().decode()
        patched = patch_satellite_nginx(original, domain)
        with sftp.file(conf_path, "w") as fh:
            fh.write(patched)
        sat_ext = f"{NGINX_DIR}/extension/{domain}/gsc-redirects.conf"
        run(
            client,
            f"test -f {sat_ext} && mv {sat_ext} {sat_ext}.disabled-{STAMP} || true",
        )
        print(f"patched satellite nginx {domain}")

    sftp.close()


def nginx_reload(client: paramiko.SSHClient) -> None:
    test = run(client, "nginx -t 2>&1")
    print(test)
    if "successful" not in test.lower() and "ok" not in test.lower():
        raise SystemExit("nginx -t failed; not reloading")
    print(run(client, "nginx -s reload 2>&1"))


def verify(client: paramiko.SSHClient) -> None:
    checks = [
        (
            f"curl -sk --resolve {CANONICAL_HOST}:443:{HOST} https://{CANONICAL_HOST}/ "
            "| grep -oE 'Independent USFans spreadsheet|Official hub|Open live spreadsheet|class=\"prod\"|Loading trending finds' | sort | uniq -c",
            "home",
        ),
        (
            f"curl -skI --resolve {CANONICAL_HOST}:443:{HOST} https://{CANONICAL_HOST}/usfans-amiri-spreadsheet/ "
            "| grep -iE 'HTTP/|location:|x-robots' | head -6",
            "thin amiri",
        ),
        (
            f"curl -skI --resolve {CANONICAL_HOST}:443:{HOST} https://{CANONICAL_HOST}/usfans-spreadsheet-2026/ "
            "| grep -iE 'HTTP/|location:' | head -6",
            "thin 2026 dupe",
        ),
        (
            f"curl -sk --resolve {CANONICAL_HOST}:443:{HOST} https://{CANONICAL_HOST}/sitemap.xml "
            "| grep -c '<loc>'",
            "sitemap loc count",
        ),
        (
            f"curl -skI --resolve usfansspreadsheet.uk:443:{HOST} https://usfansspreadsheet.uk/ "
            "| grep -iE 'HTTP/|location:' | head -6",
            "uk 301",
        ),
        (
            f"curl -skI --resolve usfansspreadsheet.nl:443:{HOST} https://usfansspreadsheet.nl/usfans-coupons/ "
            "| grep -iE 'HTTP/|location:' | head -6",
            "nl path 301",
        ),
        (
            f"curl -skI --resolve usfansspreadsheet.co.uk:443:{HOST} https://usfansspreadsheet.co.uk/ "
            "| grep -iE 'HTTP/|location:' | head -6",
            "co.uk 301",
        ),
    ]
    for cmd, label in checks:
        print(f"=== verify {label} ===")
        print(run(client, cmd, timeout=60))


def main() -> None:
    if not (OVERLAY / "index.html").is_file():
        print("Run python3 scripts/build_usfans_overlay.py first", file=sys.stderr)
        sys.exit(1)

    client = connect()
    print(f"connected {HOST}")
    print("1/4 backup index.html")
    run(
        client,
        f"cp -a {WEBROOT}/{CANONICAL_HOST}/index.html "
        f"{WEBROOT}/{CANONICAL_HOST}/index.html.bak-decluster-{STAMP}",
    )
    print("2/4 upload overlay")
    n = upload_overlay(client)
    print(f"uploaded {n} files")
    print("3/4 nginx snippets + satellite 301")
    write_nginx_snippets(client)
    nginx_reload(client)
    print("4/4 verify origin")
    verify(client)
    client.close()
    print("deploy done")


if __name__ == "__main__":
    main()
