#!/usr/bin/env python3
"""Route /api/{name}/ to index.php on SugarGoo country desks.

Does not touch unique dest articles or now.com html files.
"""
from __future__ import annotations

import os
import sys

HOSTS = [
    "sugargoospreadsheets.us",
    "sugargoospreadsheet.au",
    "sugargoospreadsheets.fr",
    "sugargoospreadsheets2026.ca",
    "sugargoospreadsheetnow.com",
    "sugargoospreadsheets.uk",
    "sugargoospreadsheet.es",
    "sugargoospreadsheets.de",
    "sugargoo.at",
    "sugargoospreadsheets.nl",
]

OLD = """    location /api/ {
        try_files $uri =404;
        add_header X-Robots-Tag "noindex, nofollow" always;
    }
"""

NEW = """    location /api/ {
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


def main() -> None:
    dry = "--dry" in sys.argv
    client = None if dry else _connect()
    changed = 0
    for host in HOSTS:
        path = f"/www/server/panel/vhost/nginx/{host}.conf"
        if dry:
            print("dry", path)
            continue
        raw = _run(client, f"cat '{path}'")
        if "rewrite ^/api/([^/]+)/?$ /api/$1/index.php last" in raw:
            print("ok", host, "already rewritten")
            continue
        if OLD not in raw:
            print("skip", host, "api block mismatch")
            continue
        bak = f"/www/backup/sugargoo-nginx-{host}.conf"
        _run(client, f"cp -a '{path}' '{bak}'")
        new = raw.replace(OLD, NEW, 1)
        # write via python on remote to keep quoting
        import paramiko

        sftp = client.open_sftp()
        with sftp.open(path, "w") as fh:
            fh.write(new)
        sftp.close()
        print("PATCH", path)
        changed += 1
    if not dry:
        print(_run(client, "nginx -t && nginx -s reload"))
        client.close()
    print("changed", changed)


if __name__ == "__main__":
    main()
