#!/usr/bin/env python3
"""Deploy OrientDig partner sites (orientdig.us/es/fr/at) to Baota/nginx server."""

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

PARTNER_DOMAINS = [
    "orientdig.us",
    "orientdig.es",
    "orientdig.fr",
    "orientdig.at",
]

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


def register_baota_sites(client: paramiko.SSHClient) -> None:
    """Register sites in Baota panel DB so they appear in the Websites list."""
    domains_json = ",".join(f'"{d}"' for d in PARTNER_DOMAINS)
    script = f"""
cd /www/server/panel
/www/server/panel/pyenv/bin/python3 << 'EOF'
import json, sys
sys.path.insert(0, '/www/server/panel')
sys.path.insert(0, '/www/server/panel/class')
import public
from panelSite import panelSite

domains = [{domains_json}]
ps = panelSite()
for d in domains:
    existing = public.M('sites').where('name=?', (d,)).find()
    if existing:
        print(f'already registered {{d}}')
        continue
    get = public.to_dict_obj({{
        'webname': json.dumps({{'domain': d, 'domainlist': [], 'count': 1}}),
        'path': f'/www/wwwroot/{{d}}',
        'type': 'PHP',
        'version': '74',
        'port': '80',
        'ps': d,
        'type_id': 0,
        'ftp': 'false',
    }})
    try:
        result = ps.AddSite(get)
        print(f'registered {{d}}:', result)
    except Exception as exc:
        # AddSite may partially succeed (DB row + nginx) before optional FTP step.
        row = public.M('sites').where('name=?', (d,)).find()
        if row:
            print(f'registered {{d}} (partial): {{exc}}')
        else:
            print(f'FAILED {{d}}: {{exc}}')
EOF
"""
    print(run(client, script, timeout=180))


def deploy_files(client: paramiko.SSHClient) -> None:
    sftp = client.open_sftp()
    for domain in PARTNER_DOMAINS:
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


def issue_certs(client: paramiko.SSHClient) -> None:
    for domain in PARTNER_DOMAINS:
        web = f"{WEBROOT}/{domain}"
        cert = f"{CERT_DIR}/{domain}"
        cmd = f"""
set -e
mkdir -p {cert}
{ACME} --issue -d {domain} -w {web} --force 2>&1 | tail -6 || true
{ACME} --install-cert -d {domain} \\
  --key-file {cert}/privkey.pem \\
  --fullchain-file {cert}/fullchain.pem 2>&1 | tail -2 || true
test -s {cert}/fullchain.pem && openssl x509 -in {cert}/fullchain.pem -noout && echo CERT_OK_{domain} || echo CERT_FAIL_{domain}
"""
        print(f"=== cert {domain} ===")
        print(run(client, cmd, timeout=300)[-600:])
    ensure_certs(client)


def write_nginx(domain: str) -> str:
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
    include {NGINX_DIR}/extension/{domain}/*.conf;
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


def ensure_well_known(client: paramiko.SSHClient) -> None:
    for domain in PARTNER_DOMAINS:
        run(client, f"mkdir -p {NGINX_DIR}/extension/{domain}")
        conf = f"{NGINX_DIR}/well-known/{domain}.conf"
        run(
            client,
            f"grep -q 'well-known' {conf} 2>/dev/null || "
            f"printf '%s\\n' 'location ~ \\.well-known {{' '    allow all;' '}}' > {conf}",
        )


def ensure_certs(client: paramiko.SSHClient) -> None:
    for domain in PARTNER_DOMAINS:
        cert = f"{CERT_DIR}/{domain}"
        chain = f"{cert}/fullchain.pem"
        check = run(client, f"test -s {chain} && openssl x509 -in {chain} -noout 2>/dev/null && echo VALID || echo INVALID")
        if "VALID" in check:
            continue
        run(client, f"mkdir -p {cert}")
        run(
            client,
            f"openssl req -x509 -nodes -days 365 -newkey rsa:2048 "
            f"-keyout {cert}/privkey.pem -out {chain} -subj '/CN={domain}' 2>/dev/null",
        )
        print(f"self-signed fallback cert {domain}")


def patch_nginx(client: paramiko.SSHClient) -> None:
    ensure_well_known(client)
    sftp = client.open_sftp()
    for domain in PARTNER_DOMAINS:
        conf = f"{NGINX_DIR}/{domain}.conf"
        content = write_nginx(domain)
        with sftp.file(conf, "w") as f:
            f.write(content)
        print(f"nginx {domain}")
    sftp.close()
    print(run(client, "nginx -t 2>&1 && nginx -s reload 2>&1"))


def verify(client: paramiko.SSHClient) -> None:
    for domain in PARTNER_DOMAINS:
        cmd = (
            f"curl -s -H 'Host: {domain}' http://127.0.0.1/ "
            f"| grep -oiE '<title>[^<]+|Official Partner|w2clinks.com/spreadsheet|447856544534' | head -8"
        )
        print(f"=== verify {domain} ===")
        print(run(client, cmd))


def main() -> None:
    missing = [d for d in PARTNER_DOMAINS if not (DIST / d).is_dir()]
    if missing:
        print(f"Run build_partner_site.py first — missing: {missing}", file=sys.stderr)
        sys.exit(1)
    client = connect()
    print("1/5 register Baota sites...")
    register_baota_sites(client)
    print("2/5 upload files...")
    deploy_files(client)
    print("3/5 issue SSL certs...")
    issue_certs(client)
    print("4/5 patch nginx...")
    patch_nginx(client)
    print("5/5 verify...")
    verify(client)
    client.close()
    print("partner deploy done")


if __name__ == "__main__":
    main()
