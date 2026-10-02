#!/usr/bin/env python3
"""Route /api/products/ to PHP on HipoBuy country desks.

Static try_files only looks for index.html, so the catalog JSON 404s and
/hipobuy-spreadsheet/ renders an empty grid. Does not touch .net.
"""
from __future__ import annotations

import os
import sys

HOSTS = [
    "hipobuy.at",
    "hipobuyspreadsheet.nl",
    "hipobuyspreadsheet.co.uk",
    "hipobuyspreadsheet.eu",
    "hipobuyspreadsheet.us",
    "hipobuyspreadsheets.uk",
]

OLD_API = """    location /api/ {
        try_files $uri =404;
        add_header X-Robots-Tag "noindex, nofollow" always;
    }
"""

NEW_API = """    location /api/ {
        rewrite ^/api/([^/]+)/?$ /api/$1/index.php last;
        add_header X-Robots-Tag "noindex, nofollow" always;
    }
"""


def _connect():
    try:
        import paramiko
    except ImportError:
        import subprocess

        subprocess.check_call([sys.executable, "-m", "pip", "install", "paramiko", "-q"])
        import paramiko

    password = (
        os.environ.get("ORIGIN_SSH_PASS")
        or os.environ.get("HIPOBAY_DEPLOY_PASS")
        or os.environ.get("LITBUY_DEPLOY_PASS")
    )
    if not password:
        print("Set ORIGIN_SSH_PASS", file=sys.stderr)
        sys.exit(1)
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect("31.97.41.31", username="root", password=password, timeout=30)
    return client


def _run(client, cmd: str, timeout: int = 60) -> str:
    _, stdout, stderr = client.exec_command(cmd, timeout=timeout)
    return (stdout.read() + stderr.read()).decode(errors="replace").strip()


def main() -> None:
    client = _connect()
    sftp = client.open_sftp()
    stamp = _run(client, "date +%Y%m%d-%H%M%S")
    bak_root = f"/www/backup/hipobuy-api-nginx-{stamp}"
    print(_run(client, f"mkdir -p '{bak_root}'"))

    patched = 0
    for host in HOSTS:
        if host.endswith(".net"):
            raise SystemExit("refusing .net")
        remote = f"/www/server/panel/vhost/nginx/{host}.conf"
        bak = f"{bak_root}/{host}.conf"
        _run(client, f"cp -a '{remote}' '{bak}'")
        with sftp.open(remote, "r") as fh:
            text = fh.read().decode()
        if NEW_API in text:
            print("already", host)
            continue
        n = text.count(OLD_API)
        if n < 1:
            print("MISSING api block", host, file=sys.stderr)
            sftp.close()
            client.close()
            sys.exit(1)
        text = text.replace(OLD_API, NEW_API)
        with sftp.open(remote, "w") as fh:
            fh.write(text)
        print("vhost", host, "replaced", n)
        patched += 1
    if patched == 0:
        print("nothing to patch")
        sftp.close()
        client.close()
        return

    test = _run(client, "nginx -t")
    print(test)
    if "syntax is ok" not in test or "test is successful" not in test:
        print("nginx -t failed; restoring", file=sys.stderr)
        for host in HOSTS:
            remote = f"/www/server/panel/vhost/nginx/{host}.conf"
            bak = f"{bak_root}/{host}.conf"
            _run(client, f"cp -a '{bak}' '{remote}'")
        print(_run(client, "nginx -t"))
        sftp.close()
        client.close()
        sys.exit(1)

    print(_run(client, "nginx -s reload"))
    print("backup", bak_root)
    sftp.close()
    client.close()


if __name__ == "__main__":
    main()
