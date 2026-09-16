#!/usr/bin/env python3
"""Deploy Kakobuy cluster to Baota/nginx server.

Domains:
  kakospreadsheet.es / .fr / .nl / .ca
  kakobuy.fi
  kakospreadsheets.{es,fr,nl,ca}  (301 → singular domain)

Prerequisites:
  python3 build_kakobuy_site.py
  export KAKOBUY_DEPLOY_PASS='...'   # or ORIENTDIG_DEPLOY_PASS / BBDBUY_DEPLOY_PASS

Optional env:
  KAKOBUY_DEPLOY_HOST  (default: same as OrientDig/BBDBuy, 31.97.41.31)
  KAKOBUY_DEPLOY_USER  (default: root)
  KAKOBUY_DEPLOY_ONLY=kakobuy.fi
  KAKOBUY_SKIP_CERTS=1
  KAKOBUY_SKIP_BAOTA=1
  KAKOBUY_SKIP_NGINX=1
  W2CLINKS_API_KEY=...          # written to api/config.local.php, not committed
"""

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
sys.path.insert(0, str(ROOT))

from scripts.domains_kakobuy import (  # noqa: E402
    KAKOBUY_DOMAINS,
    PLURAL_REDIRECTS,
)

DIST = ROOT / "dist"
WEBROOT = "/www/wwwroot"
NGINX_DIR = "/www/server/panel/vhost/nginx"
CERT_DIR = "/www/server/panel/vhost/cert"
ACME = "/root/.acme.sh/acme.sh"

CANONICAL_DOMAINS = list(KAKOBUY_DOMAINS.keys())
PLURAL_DOMAINS = list(PLURAL_REDIRECTS.keys())
ALL_DEPLOY_DOMAINS = CANONICAL_DOMAINS + PLURAL_DOMAINS

_ONLY = os.environ.get("KAKOBUY_DEPLOY_ONLY", "").strip()
if _ONLY:
    ALL_DEPLOY_DOMAINS = [d for d in ALL_DEPLOY_DOMAINS if d == _ONLY]
    CANONICAL_DOMAINS = [d for d in CANONICAL_DOMAINS if d == _ONLY]
    PLURAL_REDIRECTS = {k: v for k, v in PLURAL_REDIRECTS.items() if k == _ONLY}

HOST = os.environ.get(
    "KAKOBUY_DEPLOY_HOST",
    os.environ.get("BBDBUY_DEPLOY_HOST", os.environ.get("ORIENTDIG_DEPLOY_HOST", "31.97.41.31")),
)
USER = os.environ.get(
    "KAKOBUY_DEPLOY_USER",
    os.environ.get("BBDBUY_DEPLOY_USER", os.environ.get("ORIENTDIG_DEPLOY_USER", "root")),
)

VERIFY_NEEDLES: dict[str, str] = {
    "kakospreadsheet.es": "Kakobuy Spreadsheet España",
    "kakospreadsheet.fr": "Kakobuy Spreadsheet France",
    "kakospreadsheet.nl": "Kakobuy Spreadsheet Nederland",
    "kakospreadsheet.ca": "Kakobuy Spreadsheet Canada",
    "kakobuy.fi": "Kakobuy Suomi",
}


def _flag(name: str) -> bool:
    return os.environ.get(name, "").strip().lower() in ("1", "true", "yes")


def connect() -> paramiko.SSHClient:
    password = (
        os.environ.get("KAKOBUY_DEPLOY_PASS")
        or os.environ.get("BBDBUY_DEPLOY_PASS")
        or os.environ.get("ORIENTDIG_DEPLOY_PASS")
    )
    if not password:
        print(
            "Set KAKOBUY_DEPLOY_PASS (or BBDBUY_DEPLOY_PASS / ORIENTDIG_DEPLOY_PASS)",
            file=sys.stderr,
        )
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
    for path in sorted(local.rglob("*")):
        rel = path.relative_to(local).as_posix()
        remote_path = f"{remote}/{rel}" if rel != "." else remote
        if path.is_dir():
            try:
                sftp.stat(remote_path)
            except OSError:
                sftp.mkdir(remote_path)
        else:
            parent = "/".join(remote_path.split("/")[:-1])
            if parent:
                try:
                    sftp.stat(parent)
                except OSError:
                    run_parts = parent.strip("/").split("/")
                    built = ""
                    for part in run_parts:
                        built += f"/{part}"
                        try:
                            sftp.stat(built)
                        except OSError:
                            sftp.mkdir(built)
            sftp.put(str(path), remote_path)


def register_baota_sites(client: paramiko.SSHClient) -> None:
    domains_json = ",".join(f'"{d}"' for d in ALL_DEPLOY_DOMAINS)
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
        row = public.M('sites').where('name=?', (d,)).find()
        if row:
            print(f'registered {{d}} (partial): {{exc}}')
        else:
            print(f'FAILED {{d}}: {{exc}}')
EOF
"""
    print(run(client, script, timeout=180))


def write_w2c_api_config(sftp: paramiko.SFTPClient, client: paramiko.SSHClient) -> None:
    key = os.environ.get("W2CLINKS_API_KEY", "").strip()
    if not key:
        print("skip W2C API key file (W2CLINKS_API_KEY unset)")
        return
    escaped = key.replace("\\", "\\\\").replace("'", "\\'")
    body = "<?php\nreturn ['api_key' => '" + escaped + "'];\n"
    for domain in CANONICAL_DOMAINS:
        remote_php = f"{WEBROOT}/{domain}/api/products.php"
        try:
            sftp.stat(remote_php)
        except OSError:
            continue
        remote = f"{WEBROOT}/{domain}/api/config.local.php"
        with sftp.file(remote, "w") as handle:
            handle.write(body)
        run(client, f"chown www:www {remote} && chmod 640 {remote}")
        print(f"wrote API config for {domain}")


def deploy_files(client: paramiko.SSHClient) -> None:
    sftp = client.open_sftp()
    for domain in ALL_DEPLOY_DOMAINS:
        local = DIST / domain
        if not local.is_dir():
            print(f"skip missing local dist/{domain}")
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
    write_w2c_api_config(sftp, client)
    sftp.close()


def ensure_well_known(client: paramiko.SSHClient) -> None:
    for domain in ALL_DEPLOY_DOMAINS:
        run(client, f"mkdir -p {NGINX_DIR}/extension/{domain}")
        conf = f"{NGINX_DIR}/well-known/{domain}.conf"
        run(
            client,
            f"grep -q 'well-known' {conf} 2>/dev/null || "
            f"printf '%s\\n' 'location ~ \\.well-known {{' '    allow all;' '}}' > {conf}",
        )


def ensure_certs(client: paramiko.SSHClient, domains: list[str]) -> None:
    for domain in domains:
        cert = f"{CERT_DIR}/{domain}"
        chain = f"{cert}/fullchain.pem"
        check = run(
            client,
            f"test -s {chain} && openssl x509 -in {chain} -noout 2>/dev/null && echo VALID || echo INVALID",
        )
        if "VALID" in check:
            continue
        run(client, f"mkdir -p {cert}")
        run(
            client,
            f"openssl req -x509 -nodes -days 365 -newkey rsa:2048 "
            f"-keyout {cert}/privkey.pem -out {chain} -subj '/CN={domain}' 2>/dev/null",
        )
        print(f"self-signed fallback cert {domain}")


def issue_certs(client: paramiko.SSHClient) -> None:
    for domain in ALL_DEPLOY_DOMAINS:
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
    ensure_certs(client, ALL_DEPLOY_DOMAINS)


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
    ensure_well_known(client)
    sftp = client.open_sftp()
    for domain in CANONICAL_DOMAINS:
        conf = f"{NGINX_DIR}/{domain}.conf"
        with sftp.file(conf, "w") as f:
            f.write(write_canonical_nginx(domain))
        print(f"nginx canonical {domain}")
    for domain, target in PLURAL_REDIRECTS.items():
        conf = f"{NGINX_DIR}/{domain}.conf"
        with sftp.file(conf, "w") as f:
            f.write(write_plural_nginx(domain, target))
        print(f"nginx plural {domain} -> {target}")
    sftp.close()
    print(run(client, "nginx -t 2>&1 && nginx -s reload 2>&1"))


def verify(client: paramiko.SSHClient) -> None:
    for domain in CANONICAL_DOMAINS:
        needle = VERIFY_NEEDLES.get(domain, "Kakobuy")
        cmd = (
            f"curl -sk --resolve {domain}:443:127.0.0.1 https://{domain}/ "
            f"| grep -oiE '<title>[^<]+|{needle}|kakobuy-logo|w2clinks.com/spreadsheet|ikako.vip' | head -8"
        )
        print(f"=== verify {domain} ===")
        print(run(client, cmd))
    for domain, target in PLURAL_REDIRECTS.items():
        cmd = (
            f"curl -skI --resolve {domain}:443:127.0.0.1 https://{domain}/ "
            f"| grep -iE 'HTTP/|location:' | head -3"
        )
        print(f"=== verify redirect {domain} -> {target} ===")
        print(run(client, cmd))


def main() -> None:
    missing = [d for d in CANONICAL_DOMAINS if not (DIST / d).is_dir()]
    if missing:
        print(f"Run build_kakobuy_site.py first — missing: {missing}", file=sys.stderr)
        sys.exit(1)

    client = connect()
    step = 1
    total = 5

    if not _flag("KAKOBUY_SKIP_BAOTA"):
        print(f"{step}/{total} register Baota sites...")
        register_baota_sites(client)
        step += 1
    else:
        print("skip Baota registration (KAKOBUY_SKIP_BAOTA=1)")

    print(f"{step}/{total} upload files...")
    deploy_files(client)
    step += 1

    if not _flag("KAKOBUY_SKIP_CERTS"):
        print(f"{step}/{total} issue SSL certs...")
        issue_certs(client)
        step += 1
    else:
        print("skip certs (KAKOBUY_SKIP_CERTS=1)")

    if not _flag("KAKOBUY_SKIP_NGINX"):
        print(f"{step}/{total} patch nginx...")
        patch_nginx(client)
        step += 1
    else:
        print("skip nginx (KAKOBUY_SKIP_NGINX=1)")

    print(f"{step}/{total} verify...")
    verify(client)
    if "kakobuy.fi" in CANONICAL_DOMAINS:
        print("=== verify kakobuy.fi product logic ===")
        print(
            run(
                client,
                "curl -sk --resolve kakobuy.fi:443:127.0.0.1 https://kakobuy.fi/ "
                "| grep -oiE 'W2CLinks|Search intent|euroina|Kakobuy Suomi|Avaa spreadsheet|25,5' | head -20",
            )
        )
        print(
            run(
                client,
                "curl -sk --resolve kakobuy.fi:443:127.0.0.1 https://kakobuy.fi/kakobuy-spreadsheet/ "
                "| grep -oiE 'sheet-product|Avaa Kakobuyssa|api/products.php|24 tuotetta|W2CLinks' | head -20",
            )
        )
        print(
            run(
                client,
                "curl -sk --resolve kakobuy.fi:443:127.0.0.1 "
                "'https://kakobuy.fi/api/products.php?per_page=2&q=jordan' "
                "| python3 -c \"import sys,json; d=json.load(sys.stdin); print('api', d.get('ok'), d.get('found'), len(d.get('hits') or []))\"",
            )
        )
    if "kakospreadsheet.fr" in CANONICAL_DOMAINS:
        print("=== verify kakospreadsheet.fr product logic ===")
        print(
            run(
                client,
                "curl -sk --resolve kakospreadsheet.fr:443:127.0.0.1 https://kakospreadsheet.fr/ "
                "| grep -oiE 'W2CLinks|Search intent|prix en euros|Kakobuy Spreadsheet France|Ouvrir le spreadsheet|20 %|3000 CNY|kako buy' | head -20",
            )
        )
        print(
            run(
                client,
                "curl -sk --resolve kakospreadsheet.fr:443:127.0.0.1 https://kakospreadsheet.fr/kakobuy-spreadsheet/ "
                "| grep -oiE 'sheet-product|Ouvrir sur Kakobuy|api/products.php|W2CLinks' | head -20",
            )
        )
        print(
            run(
                client,
                "curl -sk --resolve kakospreadsheet.fr:443:127.0.0.1 https://kakospreadsheet.fr/kako-buy/ "
                "| grep -oiE 'kako buy|kako-buy|Kakobuy' | head -12",
            )
        )
        print(
            run(
                client,
                "curl -sk --resolve kakospreadsheet.fr:443:127.0.0.1 https://kakospreadsheet.fr/kako-spreadsheet/ "
                "| grep -oiE 'kako spreadsheet|kako-spreadsheet|Kakobuy spreadsheet' | head -12",
            )
        )
        print(
            run(
                client,
                "curl -skI --resolve kakospreadsheet.fr:443:127.0.0.1 https://kakospreadsheet.fr/kako-buy-spreadsheet/ "
                "| grep -iE 'HTTP/|location'",
            )
        )
        print(
            run(
                client,
                "curl -sk --resolve kakospreadsheet.fr:443:127.0.0.1 "
                "'https://kakospreadsheet.fr/api/products.php?per_page=2&q=jordan' "
                "| python3 -c \"import sys,json; d=json.load(sys.stdin); print('api', d.get('ok'), d.get('found'), len(d.get('hits') or []))\"",
            )
        )
    if "kakospreadsheet.nl" in CANONICAL_DOMAINS:
        print("=== verify kakospreadsheet.nl product logic ===")
        print(
            run(
                client,
                "curl -sk --resolve kakospreadsheet.nl:443:127.0.0.1 https://kakospreadsheet.nl/ "
                "| grep -oiE 'W2CLinks|Search intent|prijzen in euro|Kakobuy Spreadsheet Nederland|Spreadsheet openen|21 %|3000 CNY|kako buy|betrouwbaar' | head -20",
            )
        )
        print(
            run(
                client,
                "curl -sk --resolve kakospreadsheet.nl:443:127.0.0.1 https://kakospreadsheet.nl/kakobuy-spreadsheet/ "
                "| grep -oiE 'sheet-product|Openen op Kakobuy|api/products.php|Beste Kakobuy|W2CLinks' | head -20",
            )
        )
        print(
            run(
                client,
                "curl -sk --resolve kakospreadsheet.nl:443:127.0.0.1 https://kakospreadsheet.nl/kako-buy/ "
                "| grep -oiE 'kako buy|kako-buy|Kakobuy' | head -12",
            )
        )
        print(
            run(
                client,
                "curl -skI --resolve kakospreadsheet.nl:443:127.0.0.1 https://kakospreadsheet.nl/best-kakobuy-spreadsheet/ "
                "| grep -iE 'HTTP/|location'",
            )
        )
        print(
            run(
                client,
                "curl -sk --resolve kakospreadsheet.nl:443:127.0.0.1 "
                "'https://kakospreadsheet.nl/api/products.php?per_page=2&q=jordan' "
                "| python3 -c \"import sys,json; d=json.load(sys.stdin); print('api', d.get('ok'), d.get('found'), len(d.get('hits') or []))\"",
            )
        )
    if "kakospreadsheet.es" in CANONICAL_DOMAINS:
        print("=== verify kakospreadsheet.es product logic ===")
        print(
            run(
                client,
                "curl -sk --resolve kakospreadsheet.es:443:127.0.0.1 https://kakospreadsheet.es/ "
                "| grep -oiE 'W2CLinks|Search intent|precios en euros|Kakobuy Spreadsheet España|Abrir spreadsheet|21 %|3000 CNY' | head -20",
            )
        )
        print(
            run(
                client,
                "curl -sk --resolve kakospreadsheet.es:443:127.0.0.1 https://kakospreadsheet.es/kakobuy-spreadsheet/ "
                "| grep -oiE 'sheet-product|Abrir en Kakobuy|api/products.php|W2CLinks' | head -20",
            )
        )
        print(
            run(
                client,
                "curl -sk --resolve kakospreadsheet.es:443:127.0.0.1 "
                "'https://kakospreadsheet.es/api/products.php?per_page=2&q=jordan' "
                "| python3 -c \"import sys,json; d=json.load(sys.stdin); print('api', d.get('ok'), d.get('found'), len(d.get('hits') or []))\"",
            )
        )
    if "kakospreadsheet.ca" in CANONICAL_DOMAINS:
        print("=== verify kakospreadsheet.ca product logic ===")
        print(
            run(
                client,
                "curl -sk --resolve kakospreadsheet.ca:443:127.0.0.1 https://kakospreadsheet.ca/ "
                "| grep -oiE 'W2CLinks|Search intent|prices in CAD|Kakobuy Spreadsheet Canada|Open spreadsheet|CBSA|3000 CNY' | head -20",
            )
        )
        print(
            run(
                client,
                "curl -sk --resolve kakospreadsheet.ca:443:127.0.0.1 https://kakospreadsheet.ca/kakobuy-spreadsheet/ "
                "| grep -oiE 'sheet-product|Open on Kakobuy|api/products.php|W2CLinks' | head -20",
            )
        )
        print(
            run(
                client,
                "curl -sk --resolve kakospreadsheet.ca:443:127.0.0.1 "
                "'https://kakospreadsheet.ca/api/products.php?per_page=2&q=jordan' "
                "| python3 -c \"import sys,json; d=json.load(sys.stdin); print('api', d.get('ok'), d.get('found'), len(d.get('hits') or []))\"",
            )
        )
    client.close()
    print("kakobuy deploy done")


if __name__ == "__main__":
    main()
