#!/usr/bin/env python3
"""PUT HipoBuy country-desk overlays and surgical inner patches.

Reads ORIGIN_SSH_PASS (or HIPOBAY_DEPLOY_PASS). Never logs the password.
Does not touch hipobuyspreadsheet.net.
"""
from __future__ import annotations

import os
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATCHED = Path("/tmp/cms-patched")

HOST = "31.97.41.31"
USER = "root"

# live path, local path
PUTS = [
    ("/www/wwwroot/hipobuy.at/index.html", ROOT / "sites/hipobuy.at/overlay/index.html"),
    ("/www/wwwroot/hipobuyspreadsheet.nl/index.html", ROOT / "sites/hipobuyspreadsheet.nl/overlay/index.html"),
    ("/www/wwwroot/hipobuyspreadsheet.co.uk/index.html", ROOT / "sites/hipobuyspreadsheet.co.uk/overlay/index.html"),
    ("/www/wwwroot/hipobuyspreadsheet.eu/index.html", ROOT / "sites/hipobuyspreadsheet.eu/overlay/index.html"),
    ("/www/wwwroot/hipobuyspreadsheet.us/index.html", ROOT / "sites/hipobuyspreadsheet.us/overlay/index.html"),
    ("/www/wwwroot/hipobuyspreadsheets.uk/index.html", ROOT / "sites/hipobuyspreadsheets.uk/overlay/index.html"),
    ("/www/wwwroot/hipobuy.at/hipobuy-shipping-guide/index.html", PATCHED / "at-ship.html"),
    ("/www/wwwroot/hipobuyspreadsheet.nl/hipobuy-shipping-guide/index.html", PATCHED / "nl-ship.html"),
    ("/www/wwwroot/hipobuyspreadsheet.us/hipobuy-shipping-guide/index.html", PATCHED / "us-ship.html"),
    ("/www/wwwroot/hipobuyspreadsheets.uk/hipobuy-shipping-guide/index.html", PATCHED / "ukhaul-ship.html"),
    ("/www/wwwroot/hipobuyspreadsheet.eu/hipobuy-coupons/index.html", PATCHED / "eu-coup.html"),
    ("/www/wwwroot/hipobuyspreadsheet.co.uk/hipobuy-coupons/index.html", PATCHED / "uk-coup.html"),
    ("/www/wwwroot/hipobuyspreadsheet.co.uk/blog/posts/hipobuy-sizing-guide/index.html", PATCHED / "uk-size.html"),
    ("/www/wwwroot/hipobuy.at/how-to-use-hipobuy/index.html", PATCHED / "at-how.html"),
    ("/www/wwwroot/hipobuyspreadsheet.nl/how-to-use-hipobuy/index.html", PATCHED / "nl-how.html"),
    ("/www/wwwroot/hipobuyspreadsheet.us/how-to-use-hipobuy/index.html", PATCHED / "us-how.html"),
    ("/www/wwwroot/hipobuyspreadsheet.co.uk/how-to-use-hipobuy/index.html", PATCHED / "uk-how.html"),
    ("/www/wwwroot/hipobuyspreadsheet.eu/how-to-use-hipobuy/index.html", PATCHED / "eu-how.html"),
    ("/www/wwwroot/hipobuyspreadsheets.uk/how-to-use-hipobuy/index.html", PATCHED / "ukhaul-how.html"),
]

OPTIONAL = [
    ("/www/wwwroot/hipobuyspreadsheet.us/guides/shipping/index.html", PATCHED / "us-ship.html"),
]


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
    client.connect(HOST, username=USER, password=password, timeout=30)
    return client


def _run(client, cmd: str, timeout: int = 60) -> str:
    _, stdout, stderr = client.exec_command(cmd, timeout=timeout)
    return (stdout.read() + stderr.read()).decode(errors="replace").strip()


def main() -> None:
    for _remote, local in PUTS:
        if not local.is_file():
            raise SystemExit(f"missing local {local}")
    client = _connect()
    sftp = client.open_sftp()
    stamp = time.strftime("%Y%m%d-%H%M%S")
    backup_root = f"/www/backup/hipobuy-desk-{stamp}"
    print(_run(client, f"mkdir -p {backup_root}"))

    extras = []
    for remote, local in OPTIONAL:
        try:
            sftp.stat(remote)
            extras.append((remote, local))
            print("optional exists", remote)
        except FileNotFoundError:
            print("optional skip", remote)

    uploaded = []
    for remote, local in PUTS + extras:
        if "hipobuyspreadsheet.net" in remote:
            raise SystemExit("refusing .net PUT")
        bak = backup_root + remote.replace("/www/wwwroot", "")
        parent = str(Path(bak).parent)
        _run(client, f"mkdir -p '{parent}'")
        try:
            sftp.stat(remote)
            _run(client, f"cp -a '{remote}' '{bak}'")
        except FileNotFoundError:
            print("no prior file", remote)
        sftp.put(str(local), remote)
        uploaded.append(remote)
        print("PUT", remote, local.stat().st_size)

    _run(
        client,
        "chown www:www "
        + " ".join(f"'{p}'" for p in uploaded)
        + " && chmod 644 "
        + " ".join(f"'{p}'" for p in uploaded),
    )
    print("backup", backup_root)
    print("count", len(uploaded))
    sftp.close()
    client.close()


if __name__ == "__main__":
    main()
