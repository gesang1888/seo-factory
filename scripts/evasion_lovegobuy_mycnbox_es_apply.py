#!/usr/bin/env python3
"""PUT LoveGoBuy NL/IT + MyCNBox.es homepages.

Never PUT lovegobuyguide.com. Never PUT hipobuyspreadsheet.eu coupons.
Never PUT inner CMS (shipping, coupons, recensioni, invite, community).
Do not 301 lovegobuyspreadsheet.nl this round (own clicks + coupon CMS).

  export BT_KEY='...'
  python3 scripts/evasion_lovegobuy_mycnbox_es_apply.py --apply
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
    "lovegobuy.nl": ROOT / "sites/lovegobuy.nl/overlay/index.html",
    "lovegobuyspreadsheet.nl": ROOT / "sites/lovegobuyspreadsheet.nl/overlay/index.html",
    "lovegobuy.it": ROOT / "sites/lovegobuy.it/overlay/index.html",
    "mycnbox.es": ROOT / "sites/mycnbox.es/overlay/index.html",
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
