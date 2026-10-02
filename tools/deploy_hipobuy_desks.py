#!/usr/bin/env python3
"""PUT HipoBuy country-desk overlays and surgical inner patches.

Reads ORIGIN_SSH_PASS (or HIPOBAY_DEPLOY_PASS). Never logs the password.
Country desks: homepage + Help overlays.
hipobuyspreadsheet.net: surgical #local on index.html only — never a CMS overwrite.
"""
from __future__ import annotations

import os
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

HOST = "31.97.41.31"
USER = "root"

from hipobuy_trust_pages import HOSTS  # noqa: E402
from hipobuy_net_local import REMOTE_TEMPLATE as NET_TEMPLATE, patch_net_home  # noqa: E402

PUTS: list[tuple[str, Path]] = []
for _d in HOSTS.values():
    overlay = ROOT / "sites" / _d["host"] / "overlay"
    PUTS.append((f"/www/wwwroot/{_d['host']}/index.html", overlay / "index.html"))
    help_slug = _d["slugs"]["help"]
    PUTS.append(
        (
            f"/www/wwwroot/{_d['host']}/{help_slug}/index.html",
            overlay / help_slug / "index.html",
        )
    )


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
    for remote, local in PUTS:
        if "hipobuyspreadsheet.net" in remote:
            raise SystemExit("refusing bulk .net PUT — use surgical patch")
        if not local.is_file():
            raise SystemExit(f"missing local {local}")
    client = _connect()
    sftp = client.open_sftp()
    stamp = time.strftime("%Y%m%d-%H%M%S")
    backup_root = f"/www/backup/hipobuy-desk-{stamp}"
    print(_run(client, f"mkdir -p {backup_root}"))

    uploaded: list[str] = []
    for remote, local in PUTS:
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

    net_tpl_bak = backup_root + "/hipobuyspreadsheet.net/template-pc-index.htm"
    _run(client, f"mkdir -p '{backup_root}/hipobuyspreadsheet.net'")
    _run(client, f"cp -a '{NET_TEMPLATE}' '{net_tpl_bak}'")
    with sftp.open(NET_TEMPLATE) as fh:
        net_html = fh.read().decode("utf-8", "replace")
    net2 = patch_net_home(net_html)
    net_local = Path("/tmp/hipobuy-net-index.htm")
    net_local.write_text(net2, encoding="utf-8")
    sftp.put(str(net_local), NET_TEMPLATE)
    uploaded.append(NET_TEMPLATE)
    print("PUT surgical", NET_TEMPLATE, len(net2))
    print(
        _run(
            client,
            "rm -rf /www/wwwroot/hipobuyspreadsheet.net/data/runtime/temp/* "
            "/www/wwwroot/hipobuyspreadsheet.net/data/runtime/cache/* 2>/dev/null; echo cache-cleared",
        )
    )

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
