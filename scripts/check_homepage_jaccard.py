#!/usr/bin/env python3
"""Sanity-check that new country homepages are not near-duplicate templates."""

from __future__ import annotations

import re
import sys
from itertools import combinations
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FILES = [
    ROOT / "sites/cssbuyspreadsheets.de/overlay/index.html",
    ROOT / "sites/cssbuyspreadsheet.ca/overlay/index.html",
    ROOT / "sites/cssbuyspreadsheet.uk/overlay/index.html",
    ROOT / "sites/cssbuyspreadsheet.eu/overlay/index.html",
    ROOT / "sites/cssbuyspreadsheets.us/overlay/index.html",
    ROOT / "sites/bbdbuy.uk/overlay/index.html",
    ROOT / "sites/bbdbuy.us/overlay/index.html",
    ROOT / "sites/bbdbuy.ca/overlay/index.html",
    ROOT / "sites/usfansspreadsheet.co.uk/overlay/index.html",
    ROOT / "sites/usfansspreadsheet.nl/overlay/index.html",
    ROOT / "sites/mycnbox.co.uk/overlay/index.html",
    ROOT / "sites/mycnbox.nl/overlay/index.html",
    ROOT / "sites/allchinabuyspreadsheets.co.uk/overlay/index.html",
    ROOT / "sites/allchinabuyspreadsheet.ca/overlay/index.html",
    ROOT / "sites/allchinabuyspreadsheet.nl/overlay/index.html",
    ROOT / "sites/kakospreadsheet.es/overlay/index.html",
    ROOT / "sites/kakobuy.fi/overlay/index.html",
    ROOT / "sites/kakospreadsheet.ca/overlay/index.html",
    ROOT / "sites/kakospreadsheet.fr/overlay/index.html",
    ROOT / "sites/kakospreadsheet.nl/overlay/index.html",
    ROOT / "sites/orientdig.es/overlay/index.html",
    ROOT / "sites/orientdig.at/overlay/index.html",
    ROOT / "sites/orientdig.fr/overlay/index.html",
]


def words(html: str) -> set[str]:
    text = re.sub(r"<script[\s\S]*?</script>", " ", html, flags=re.I)
    text = re.sub(r"<style[\s\S]*?</style>", " ", text, flags=re.I)
    text = re.sub(r"<[^>]+>", " ", text)
    return set(re.findall(r"[A-Za-zÀ-ÿ]{4,}", text.lower()))


def jaccard(a: set[str], b: set[str]) -> float:
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)


def main() -> int:
    bags = {p: words(p.read_text(encoding="utf-8")) for p in FILES}
    worst = 0.0
    fail = 0
    for a, b in combinations(FILES, 2):
        j = jaccard(bags[a], bags[b])
        worst = max(worst, j)
        flag = ""
        if j >= 0.55:
            flag = " FAIL"
            fail += 1
        print(f"{j:.3f}{flag}\t{a.parent.parent.name}\tvs\t{b.parent.parent.name}")
    print(f"worst={worst:.3f} fails={fail}")
    return 1 if fail else 0


if __name__ == "__main__":
    raise SystemExit(main())
