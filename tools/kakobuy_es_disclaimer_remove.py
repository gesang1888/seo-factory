#!/usr/bin/env python3
"""Strip LATAM/ops disclaimer callouts from kakospreadsheet.es consumer pages.

Keeps Correos / AEAT / CP5 deepen + hub uplink from gap R1.
Removes only consumer-visible LATAM overflow / no-twin / sister-domain notes.

Requires ORIGIN_SSH_PASS (or --load-env internal/usfans-ssh.env).
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
OVERLAY = ROOT / "sites" / "kakospreadsheet.es" / "overlay"
STORE = Path("/cursor/stores/bc-eb8405c7-0d3c-48be-958d-5f25b92c606c")
STAMP = "20261029"
TAG = f"kakobuy-es-disclaimer-rm-{STAMP}"
HOST = "kakospreadsheet.es"
REMOTE = f"/www/wwwroot/{HOST}"
HUB_HOST = "kakobuydocs.com"
SUFFIX = "es-disclaimer-rm"

PAGES: dict[str, str] = {
    "home": "/",
    "como-comprar-en-kakobuy": "/como-comprar-en-kakobuy/",
    "how-to-use-kakobuy": "/how-to-use-kakobuy/",
    "kakobuy-opiniones": "/kakobuy-opiniones/",
    "es-kakobuy-confiable": "/es-kakobuy-confiable/",
    "envio-kakobuy-espana": "/envio-kakobuy-espana/",
}

FORBIDDEN_NEEDLES = (
    "latam-note",
    "data-latam-overflow",
    "twin LATAM",
    "desk LATAM",
    "Sin twin LATAM",
    "Sin desk LATAM",
    "no sister",
    "LATAM overflow",
)


def _load_env(path: Path) -> None:
    text = path.read_text()
    host = pass_val = None
    for line in text.splitlines():
        if line.startswith("HOST="):
            host = line.split("=", 1)[1].strip().strip('"').strip("'")
        if line.startswith("RAW_LINE="):
            raw = line.split("=", 1)[1]
            if (raw.startswith('"') and raw.endswith('"')) or (
                raw.startswith("'") and raw.endswith("'")
            ):
                raw = raw[1:-1]
            pass_val = raw
    if not host or not pass_val:
        raise SystemExit(f"HOST/RAW_LINE missing in {path}")
    os.environ.setdefault("ORIGIN_SSH_HOST", host)
    os.environ.setdefault("ORIGIN_SSH_PASS", pass_val)


def _fetch(url: str) -> str:
    req = Request(url, headers={"User-Agent": "kakobuy-es-disclaimer-rm/1.0"})
    with urlopen(req, timeout=45) as resp:
        return resp.read().decode("utf-8", errors="replace")


def _connect():
    try:
        import paramiko
    except ImportError:
        import subprocess

        subprocess.check_call([sys.executable, "-m", "pip", "install", "paramiko", "-q"])
        import paramiko

    password = os.environ.get("ORIGIN_SSH_PASS")
    if not password:
        raise SystemExit("Set ORIGIN_SSH_PASS or pass --load-env")
    host = os.environ.get("ORIGIN_SSH_HOST", "31.97.41.31")
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(host, username="root", password=password, timeout=30)
    return client


def _run(client, cmd: str, timeout: int = 120) -> str:
    _, stdout, stderr = client.exec_command(cmd, timeout=timeout)
    return (stdout.read() + stderr.read()).decode(errors="replace").strip()


def strip_latam_ops(html: str) -> str:
    """Remove LATAM/ops callouts; keep Correos/AEAT/hub deepen."""
    # Full latam-note paragraphs (possibly multi-line).
    html = re.sub(
        r'<p\b[^>]*\b(?:class="[^"]*latam-note[^"]*"|data-latam-overflow=)[^>]*>.*?</p>\s*',
        "",
        html,
        flags=re.S | re.I,
    )
    # Orphan CSS rule for .latam-note inside es-gap style block.
    html = re.sub(r"\.latam-note\{[^}]*\}", "", html)
    # Meta / og description ops fragments.
    for frag in (
        " Sin twin LATAM.",
        " Sin desk LATAM.",
        " Sin twin LATAM",
        " Sin desk LATAM",
    ):
        html = html.replace(frag, "")
    # Marker comment (idempotent).
    needle = f"<!-- {TAG} -->"
    if needle not in html:
        html = html.replace("<head>", f"<head>\n{needle}", 1)
    # Stamp body once for verify without consumer-visible ops copy.
    if f'data-es-disclaimer-rm="{STAMP}"' not in html:
        html = html.replace(
            "<body",
            f'<body data-es-disclaimer-rm="{STAMP}"',
            1,
        )
    return html


def _dest_for(slug: str) -> Path:
    if slug == "home":
        return OVERLAY / f"index.html.{SUFFIX}"
    return OVERLAY / slug / f"index.html.{SUFFIX}"


def build_all() -> dict[str, Path]:
    out: dict[str, Path] = {}
    for slug, path in PAGES.items():
        url = f"https://{HOST}{path}"
        print(f"build {slug} …")
        live = _fetch(url)
        dest = _dest_for(slug)
        dest.parent.mkdir(parents=True, exist_ok=True)
        lb = dest.with_name(
            "live-base.index.html" if slug != "home" else "live-base.index.html.disclaimer-before"
        )
        if slug == "home":
            lb = OVERLAY / "live-base.index.html.disclaimer-before"
        lb.write_text(live)
        built = strip_latam_ops(live)
        # Must still keep local deepen + hub where they existed.
        if "Correos" not in built:
            raise SystemExit(f"{slug}: Correos missing after strip")
        if "AEAT" not in built and slug != "kakobuy-opiniones":
            # opiniones may still have Correos via stabilize; require AEAT on money pages
            if slug in (
                "home",
                "como-comprar-en-kakobuy",
                "how-to-use-kakobuy",
                "envio-kakobuy-espana",
                "es-kakobuy-confiable",
            ):
                raise SystemExit(f"{slug}: AEAT missing after strip")
        for bad in FORBIDDEN_NEEDLES:
            if bad.lower() in built.lower():
                raise SystemExit(f"{slug}: still contains ops needle {bad!r}")
        dest.write_text(built)
        out[slug] = dest
        print("  wrote", dest, "bytes", dest.stat().st_size)
    deploy_md = OVERLAY / "DEPLOY-ES-DISCLAIMER-RM.md"
    deploy_md.write_text(
        f"""# Deploy — strip LATAM/ops disclaimer from ES consumer pages ({STAMP})

Tag `{TAG}`. Keeps Correos/AEAT/CP5 + hub uplink. Removes `latam-note` / twin LATAM ops copy only.

```bash
python3 tools/kakobuy_es_disclaimer_remove.py \\
  --load-env /cursor/stores/self/internal/usfans-ssh.env --deploy --verify
```
"""
    )
    out["deploy_md"] = deploy_md
    return out


def deploy(built: dict[str, Path]) -> dict:
    client = _connect()
    bak = (
        f"/www/backup/kakobuy-es-disclaimer-rm-"
        f"{datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%S')}"
    )
    _run(client, f"mkdir -p '{bak}'")
    sftp = client.open_sftp()
    published = []
    for slug in PAGES:
        local = built[slug]
        if slug == "home":
            remote = f"{REMOTE}/index.html"
            bpath = f"{bak}/index.html.before"
        else:
            remote = f"{REMOTE}/{slug}/index.html"
            bpath = f"{bak}/{slug}.index.html.before"
        _run(client, f"mkdir -p $(dirname '{remote}') $(dirname '{bpath}')")
        _run(client, f"cp -a '{remote}' '{bpath}' 2>/dev/null || true")
        sftp.put(str(local), remote)
        published.append(remote)
        print("put", remote)
    chown_targets = [f"{REMOTE}/index.html"] + [
        f"{REMOTE}/{slug}" for slug in PAGES if slug != "home"
    ]
    _run(client, "chown -R www:www " + " ".join(chown_targets))
    sftp.close()
    client.close()
    return {"backup": bak, "stamp": STAMP, "tag": TAG, "published": published}


def verify() -> dict:
    checks = []
    for slug, path in PAGES.items():
        url = f"https://{HOST}{path}"
        req = Request(url, headers={"User-Agent": "kakobuy-es-disclaimer-rm/1.0"})
        try:
            with urlopen(req, timeout=45) as resp:
                code = resp.status
                body = resp.read().decode("utf-8", errors="replace")
        except Exception as exc:  # noqa: BLE001
            checks.append({"url": url, "ok": False, "error": str(exc)})
            print("FAIL", url, exc)
            continue
        bad = [n for n in FORBIDDEN_NEEDLES if n.lower() in body.lower()]
        keep_ok = "Correos" in body and (
            "AEAT" in body
            or slug in ("kakobuy-opiniones",)  # stabilize page may lean Correos
        )
        # Hub uplink must remain on deepen pages.
        hub_ok = HUB_HOST in body or slug in (
            "kakobuy-opiniones",
            "es-kakobuy-confiable",
            "envio-kakobuy-espana",
            "home",
        )
        # For home/stabilize, hub may only be in latam note we removed — ensure
        # deepen still has Correos; hub uplink preferred but not hard-fail if
        # stabilize pages never had a separate hub-uplink block.
        if slug in ("como-comprar-en-kakobuy", "how-to-use-kakobuy"):
            hub_ok = HUB_HOST in body
        stamped = f'data-es-disclaimer-rm="{STAMP}"' in body
        ok = code == 200 and not bad and keep_ok and hub_ok and stamped
        row = {
            "url": url,
            "http": code,
            "ok": ok,
            "forbidden_hits": bad,
            "correos": "Correos" in body,
            "aeat": "AEAT" in body,
            "hub": HUB_HOST in body,
            "stamped": stamped,
        }
        checks.append(row)
        print(("OK" if ok else "FAIL"), url, code, bad or "")
    return {"stamp": STAMP, "checks": checks, "all_ok": all(c.get("ok") for c in checks)}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--load-env", type=Path)
    ap.add_argument("--build-only", action="store_true")
    ap.add_argument("--deploy", action="store_true")
    ap.add_argument("--verify", action="store_true")
    args = ap.parse_args()
    if args.load_env:
        _load_env(args.load_env)

    built = build_all()
    meta: dict = {"built": {k: str(v) for k, v in built.items()}}
    if args.deploy:
        meta["deploy"] = deploy(built)
        time.sleep(2)
    if args.verify or args.deploy:
        meta["verify"] = verify()

    out_dir = STORE / "internal" / "kakobuy-es-disclaimer-rm"
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "live_verify.json").write_text(json.dumps(meta, indent=2)[:200000])
    if meta.get("deploy"):
        (out_dir / "backup.txt").write_text(meta["deploy"].get("backup", "") + "\n")
    print(
        json.dumps(
            {
                "all_ok": meta.get("verify", {}).get("all_ok"),
                "backup": meta.get("deploy", {}).get("backup"),
            },
            indent=2,
        )
    )
    if meta.get("verify") and not meta["verify"].get("all_ok"):
        sys.exit(1)


if __name__ == "__main__":
    main()
