#!/usr/bin/env python3
"""Deploy OrientDig Spreadsheet static sites to Baota/nginx server."""

from __future__ import annotations

import os
import sys
from pathlib import Path

try:
    import paramiko
except ImportError:
    import subprocess

    subprocess.check_call([sys.executable, "-m", "pip", "install", "paramiko", "-q"])
    import paramiko

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"
WEBROOT = "/www/wwwroot"
NGINX_DIR = "/www/server/panel/vhost/nginx"
CERT_DIR = "/www/server/panel/vhost/cert"
ACME = "/root/.acme.sh/acme.sh"

CANONICAL = [
    "orientdigspreadsheet.uk",
    "orientdigspreadsheet.us",
    "orientdigspreadsheet.nl",
    "orientdigspreadsheet.it",
    "orientdigspreadsheet.de",
    "orientdigspreadsheet.fr",
]

PLURAL_REDIRECT = {
    "orientdigspreadsheets.uk": "https://orientdigspreadsheet.uk/orientdig-spreadsheets/",
    "orientdigspreadsheets.nl": "https://orientdigspreadsheet.nl/orientdig-spreadsheets/",
    "orientdigspreadsheets.de": "https://orientdigspreadsheet.de/orientdig-spreadsheets/",
    "orientdigspreadsheets.fr": "https://orientdigspreadsheet.fr/orientdig-spreadsheets/",
}

HOST = os.environ.get("ORIENTDIG_DEPLOY_HOST", "31.97.41.31")
USER = os.environ.get("ORIENTDIG_DEPLOY_USER", "root")


def connect() -> paramiko.SSHClient:
    password = os.environ.get("ORIENTDIG_DEPLOY_PASS")
    if not password:
        print("Set ORIENTDIG_DEPLOY_PASS", file=sys.stderr)
        sys.exit(1)
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(HOST, username=USER, password=password, timeout=30)
    return client


def run(client: paramiko.SSHClient, cmd: str, timeout: int = 120) -> str:
    _, stdout, stderr = client.exec_command(cmd, timeout=timeout)
    out = stdout.read().decode()
    err = stderr.read().decode()
    return (out + err).strip()


def upload_tree(sftp: paramiko.SFTPClient, local: Path, remote: str) -> None:
    for path in local.rglob("*"):
        rel = path.relative_to(local).as_posix()
        remote_path = f"{remote}/{rel}" if rel != "." else remote
        if path.is_dir():
            try:
                sftp.stat(remote_path)
            except OSError:
                sftp.mkdir(remote_path)
        else:
            sftp.put(str(path), remote_path)


def deploy_files(client: paramiko.SSHClient) -> None:
    sftp = client.open_sftp()
    all_domains = CANONICAL + list(PLURAL_REDIRECT.keys())
    for domain in all_domains:
        local = DIST / domain
        if not local.is_dir():
            print(f"skip missing local {domain}")
            continue
        remote = f"{WEBROOT}/{domain}"
        run(
            client,
            f"mkdir -p {remote} && find {remote} -mindepth 1 -maxdepth 1 "
            f"! -name '.user.ini' -exec rm -rf {{}} +",
        )
        upload_tree(sftp, local, remote)
        run(client, f"chown -R www:www {remote}")
        print(f"uploaded {domain}")
    sftp.close()


def issue_certs(client: paramiko.SSHClient, domains: list[str]) -> None:
    for domain in domains:
        web = f"{WEBROOT}/{domain}"
        cert = f"{CERT_DIR}/{domain}"
        cmd = f"""
set -e
mkdir -p {cert}
{ACME} --issue -d {domain} -w {web} --force 2>&1 | tail -6
{ACME} --install-cert -d {domain} \\
  --key-file {cert}/privkey.pem \\
  --fullchain-file {cert}/fullchain.pem 2>&1 | tail -2
test -f {cert}/fullchain.pem && echo CERT_OK_{domain} || echo CERT_FAIL_{domain}
"""
        print(f"=== cert {domain} ===")
        print(run(client, cmd, timeout=300)[-600:])


def write_canonical_nginx(domain: str) -> str:
    return f"""server
{{
    listen 80;
    listen 443 ssl;
    http2 on;
    ssl_certificate    {CERT_DIR}/{domain}/fullchain.pem;
    ssl_certificate_key    {CERT_DIR}/{domain}/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_prefer_server_ciphers on;
    server_name {domain} www.{domain};
    index index.html index.htm index.php;
    root {WEBROOT}/{domain};
    include {NGINX_DIR}/well-known/{domain}.conf;
    include enable-php-74.conf;
    error_page 404 /404.html;
    location /api/ {{
        try_files $uri =404;
    }}
    location / {{
        try_files $uri $uri/ $uri/index.html =404;
    }}
    location /assets/ {{
        expires 7d;
        add_header Cache-Control "public, max-age=604800, must-revalidate";
    }}
    location ~ \\.well-known {{
        allow all;
    }}
    access_log  /www/wwwlogs/{domain}.log;
    error_log  /www/wwwlogs/{domain}.error.log;
}}
"""


def write_plural_nginx(domain: str, target: str) -> str:
    return f"""server
{{
    listen 80;
    listen 443 ssl;
    http2 on;
    ssl_certificate    {CERT_DIR}/{domain}/fullchain.pem;
    ssl_certificate_key    {CERT_DIR}/{domain}/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_prefer_server_ciphers on;
    server_name {domain} www.{domain};
    root {WEBROOT}/{domain};
    include {NGINX_DIR}/well-known/{domain}.conf;
    location / {{
        return 301 {target};
    }}
    location ~ \\.well-known {{
        allow all;
    }}
    access_log  /www/wwwlogs/{domain}.log;
    error_log  /www/wwwlogs/{domain}.error.log;
}}
"""


def patch_nginx(client: paramiko.SSHClient) -> None:
    sftp = client.open_sftp()
    for domain in CANONICAL:
        conf = f"{NGINX_DIR}/{domain}.conf"
        content = write_canonical_nginx(domain)
        with sftp.file(conf, "w") as f:
            f.write(content)
        print(f"nginx canonical {domain}")
    for domain, target in PLURAL_REDIRECT.items():
        conf = f"{NGINX_DIR}/{domain}.conf"
        content = write_plural_nginx(domain, target)
        with sftp.file(conf, "w") as f:
            f.write(content)
        print(f"nginx plural {domain} -> {target}")
    sftp.close()
    print(run(client, "nginx -t 2>&1 && nginx -s reload 2>&1"))


def verify(client: paramiko.SSHClient) -> None:
    checks = [
        ("orientdigspreadsheet.uk", "OrientDig"),
        ("orientdigspreadsheet.us", "OrientDig"),
        ("orientdigspreadsheet.nl", "OrientDig"),
    ]
    for domain, needle in checks:
        cmd = (
            f"curl -sk --resolve {domain}:443:127.0.0.1 https://{domain}/ "
            f"| grep -oiE '<title>[^<]+|{needle}|AllChinaBuy|w2clinks.com/spreadsheet' | head -6"
        )
        print(f"=== verify {domain} ===")
        print(run(client, cmd))


def main() -> None:
    if not DIST.is_dir():
        print("Run build_site.py first", file=sys.stderr)
        sys.exit(1)
    client = connect()
    print("1/4 upload files...")
    deploy_files(client)
    print("2/4 issue SSL certs...")
    issue_certs(client, CANONICAL + list(PLURAL_REDIRECT.keys()))
    print("3/4 patch nginx...")
    patch_nginx(client)
    print("4/4 verify...")
    verify(client)
    client.close()
    print("deploy done")


if __name__ == "__main__":
    main()
