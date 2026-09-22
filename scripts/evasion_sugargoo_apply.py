#!/usr/bin/env python3
"""PUT unique SugarGoo AU/UK/FR/CA homepages.

Never PUT sugargoospreadsheetnow.com (hub .html impressions).
Never PUT sugargoospreadsheet.es (0 GSC clicks). Never PUT inner CMS
(coupons, review, GST, VAT, CBSA, shipping-canada).

  export BT_KEY='...'
  python3 scripts/evasion_sugargoo_apply.py --apply
"""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from spam_update_p0 import Baota  # noqa: E402

PUTS = {
    "sugargoospreadsheet.au": ROOT / "sites/sugargoospreadsheet.au/overlay/index.html",
    "sugargoospreadsheets.uk": ROOT / "sites/sugargoospreadsheets.uk/overlay/index.html",
    "sugargoospreadsheets.fr": ROOT / "sites/sugargoospreadsheets.fr/overlay/index.html",
    "sugargoospreadsheets2026.ca": ROOT / "sites/sugargoospreadsheets2026.ca/overlay/index.html",
}


def apply(bt: Baota, dry_run: bool = False) -> None:
    for host, html_path in PUTS.items():
        html = html_path.read_text(encoding="utf-8")
        dest = f"/www/wwwroot/{host}/index.html"
        if dry_run:
            print("dry-run put", dest, "bytes", len(html))
            continue
        print("put", dest, bt.put(dest, html).get("msg", "")[:80])


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()
    if not (args.apply or args.dry_run):
        print("Pass --dry-run or --apply (BT_KEY required)")
        return 1
    key = os.environ.get("BT_KEY", "")
    if not key:
        raise SystemExit("BT_KEY required")
    apply(Baota(key), dry_run=args.dry_run)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
