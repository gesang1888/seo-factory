#!/usr/bin/env python3
"""Preflight checks before running cloud_seo_optimize.py."""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def ok(msg: str) -> None:
    print(f"  OK  {msg}")


def fail(msg: str) -> None:
    print(f"  FAIL {msg}")


def main() -> int:
    print("Cursor SDK SEO — preflight\n")
    errors = 0

    try:
        import cursor_sdk  # noqa: F401

        ok("cursor-sdk installed")
    except ImportError:
        fail("cursor-sdk missing — run: pip install -r requirements-cloud.txt")
        errors += 1

    key = os.environ.get("CURSOR_API_KEY", "").strip()
    if key:
        ok(f"CURSOR_API_KEY set ({key[:12]}...)")
    else:
        fail("CURSOR_API_KEY not set — https://cursor.com/dashboard/integrations")
        errors += 1

    repo = os.environ.get("SEO_FACTORY_REPO_URL", "").strip()
    if repo:
        ok(f"SEO_FACTORY_REPO_URL = {repo}")
    else:
        fail("SEO_FACTORY_REPO_URL not set (e.g. https://github.com/gesang1888/seo-factory)")
        errors += 1

    try:
        url = subprocess.check_output(
            ["git", "remote", "get-url", "origin"],
            cwd=ROOT,
            text=True,
        ).strip()
        ok(f"git origin = {url}")
    except subprocess.CalledProcessError:
        fail("no git origin remote")
        errors += 1

    if key:
        try:
            from cursor_sdk import Cursor

            repos = Cursor.repositories.list(api_key=key)
            urls = [
                getattr(r, "url", None) or (r.get("url") if isinstance(r, dict) else str(r))
                for r in (repos or [])
            ]
            if urls:
                ok(f"Cursor connected repos: {len(urls)}")
                for u in urls[:8]:
                    print(f"       - {u}")
                if repo and not any(repo.rstrip("/") in (u or "").rstrip("/") for u in urls):
                    fail(f"{repo} not in Cursor connected repos — link GitHub in Cursor Integrations")
                    errors += 1
            else:
                fail("No repos in Cursor — connect GitHub at cursor.com/settings")
                errors += 1
        except Exception as exc:
            fail(f"Cursor API: {exc}")
            errors += 1

    script = ROOT / "scripts" / "cloud_seo_optimize.py"
    if script.is_file():
        ok("cloud_seo_optimize.py present")
    else:
        fail("missing scripts/cloud_seo_optimize.py")
        errors += 1

    print()
    if errors:
        print(f"{errors} issue(s). Fix above, then run cloud SEO.")
        return 1
    print("Ready. Example:")
    print("  ./run-cloud-seo.sh --task slugs --brand lovegobuy \\")
    print("    --slugs best-lovegobuy-spreadsheet --domain lovegobuyspreadsheet.nl --create-pr")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
