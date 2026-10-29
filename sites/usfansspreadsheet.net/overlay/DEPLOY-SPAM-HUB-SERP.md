# Deploy — Spam-hub SERP recovery LIVE (2026-10-29)

Track 1 LIVE: year-dated CTR + dataset citation + index hygiene on **existing hub only**.

Tag: `spam-hub-serp-live-20261029` · stamp `2026-10-29`

Origin: Baota. Root: `/www/wwwroot/usfansspreadsheet.net`  
Auth: `internal/usfans-ssh.env` (HOST + RAW_LINE password). Never print secrets.

## GUARDS

- Surgical overlay only on **hub** `usfansspreadsheet.net`.
- **Do not** deepen NL/UK desks.
- **Do not** revive twin `usfansspreadsheet.uk` (keep 301→`.co.uk`).
- **Do not** Phase C / register mirror TLDs / thin shells.
- Do not invent row counts higher than stamped `row_count=10601` (display **10,601**).

## Push

```bash
HUB=/www/wwwroot/usfansspreadsheet.net
LOCAL=sites/usfansspreadsheet.net/overlay
BAK=/www/backup/usfans-spam-hub-serp-$(date +%Y%m%d-%H%M%S)

mkdir -p "$BAK/usfans-spreadsheet" "$BAK/finds-dataset" "$BAK/usfans-coupons" "$BAK/data"
cp -a "$HUB/usfans-spreadsheet/index.html" "$BAK/usfans-spreadsheet/" 2>/dev/null || true
cp -a "$HUB/finds-dataset/index.html" "$BAK/finds-dataset/" 2>/dev/null || true
cp -a "$HUB/usfans-coupons/index.html" "$BAK/usfans-coupons/" 2>/dev/null || true
cp -a "$HUB/index.html" "$HUB/llms.txt" "$HUB/sitemap.xml" "$HUB/data/"*.json "$BAK/" 2>/dev/null || true

mkdir -p "$HUB/usfans-spreadsheet" "$HUB/finds-dataset" "$HUB/usfans-coupons" "$HUB/data"
cp "$LOCAL/usfans-spreadsheet/index.html" "$HUB/usfans-spreadsheet/index.html"
cp "$LOCAL/finds-dataset/index.html" "$HUB/finds-dataset/index.html"
cp "$LOCAL/usfans-coupons/index.html" "$HUB/usfans-coupons/index.html"
cp "$LOCAL/index.html" "$HUB/index.html"
cp "$LOCAL/data/finds-dataset.json" "$LOCAL/data/coupons-truth.json" "$HUB/data/"
cp "$LOCAL/llms.txt" "$LOCAL/sitemap.xml" "$HUB/"
```

## Verify

- `/` title/H1 contain **USFans Spreadsheet 2026 — Independent Index · 10,601**
- FAQ cites `row_count=10601` + `/finds-dataset/`
- JSON `last_verified=2026-10-29` · `spam_hub_serp=spam-hub-serp-live-20261029`
- Alias `/usfans-spreadsheet-2026/` still **301→/**
- Twin `.uk` still 301→`.co.uk`; NL/UK heroes unchanged
