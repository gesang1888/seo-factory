#!/usr/bin/env python3
"""PUT LoveGoBuy EU, HipoBuy EU homepage, MyCNBox.de, FansBuy NL/EU.

Never PUT hipobuyspreadsheet.net (66KB hub). Never PUT hipobuy coupons/shipping CMS.
Never PUT FansBuy shipping/coupons/how-to. Never PUT MyCNBox DE spreadsheet/invite.
Never PUT cssbuy.* PHP. Do not 301 lovegobuyspreadsheet.nl.

  export BT_KEY='...'
  python3 scripts/evasion_eu_fansbuy_mycnbox_de_apply.py --apply
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
    "lovegobuyspreadsheet.eu": ROOT / "sites/lovegobuyspreadsheet.eu/overlay/index.html",
    "hipobuyspreadsheet.eu": ROOT / "sites/hipobuyspreadsheet.eu/overlay/index.html",
    "mycnbox.de": ROOT / "sites/mycnbox.de/overlay/index.html",
    "fansbuy.nl": ROOT / "sites/fansbuy.nl/overlay/index.html",
    "fansbuy.eu": ROOT / "sites/fansbuy.eu/overlay/index.html",
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
