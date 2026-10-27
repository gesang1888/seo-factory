# Deploy — USFans hub stabilize / reclaim (2026-10-27)

Action 1 LIVE: strengthen `/usfans-spreadsheet/` + dataset/coupons signals for bare brand `usfans spreadsheet` SERP (pos~48 baseline) while holding Top5 vs Reddit / `.org` / usfanshub.com.

Origin: Baota. Root: `/www/wwwroot/usfansspreadsheet.net`  
Auth: `internal/usfans-ssh.env` (HOST + RAW_LINE password). Never print secrets.

## GUARDS

- Surgical overlay only on **hub** `usfansspreadsheet.net`.
- **Do not** deepen NL/UK desks in this action.
- **Do not** revive twin `usfansspreadsheet.uk` (keep 301→`.co.uk`).
- **Do not** Phase C / register mirror TLDs against `.org` / hub.com.
- Do not invent row counts higher than stamped `row_count=10601` (display **10,601**).

## Push

```bash
HUB=/www/wwwroot/usfansspreadsheet.net
LOCAL=sites/usfansspreadsheet.net/overlay
BAK=/www/backup/usfans-hub-stabilize-$(date +%Y%m%d-%H%M%S)

mkdir -p "$BAK/usfans-spreadsheet" "$BAK/finds-dataset" "$BAK/usfans-coupons" "$BAK/data"
cp -a "$HUB/usfans-spreadsheet/index.html" "$BAK/usfans-spreadsheet/" 2>/dev/null || true
cp -a "$HUB/finds-dataset/index.html" "$BAK/finds-dataset/" 2>/dev/null || true
cp -a "$HUB/usfans-coupons/index.html" "$BAK/usfans-coupons/" 2>/dev/null || true
cp -a "$HUB/index.html" "$HUB/llms.txt" "$HUB/data/"*.json "$BAK/" 2>/dev/null || true

mkdir -p "$HUB/usfans-spreadsheet" "$HUB/finds-dataset" "$HUB/usfans-coupons" "$HUB/data"
cp "$LOCAL/usfans-spreadsheet/index.html" "$HUB/usfans-spreadsheet/index.html"
cp "$LOCAL/finds-dataset/index.html" "$HUB/finds-dataset/index.html"
cp "$LOCAL/usfans-coupons/index.html" "$HUB/usfans-coupons/index.html"
cp "$LOCAL/index.html" "$HUB/index.html"
cp "$LOCAL/data/finds-dataset.json" "$LOCAL/data/coupons-truth.json" "$HUB/data/"
cp "$LOCAL/llms.txt" "$HUB/"
```

## Verify

- `/usfans-spreadsheet/` title contains Independent Index · 10,601; CTAs Dataset/Coupons/Open directory; reclaim box; twin 301 note
- `/finds-dataset/` + `/data/finds-dataset.json` last_verified=2026-10-27 · row_count=10601 · hub_stabilize tag
- `/usfans-coupons/` + `/data/coupons-truth.json` stamped hub_stabilize
- `/` still Independent Index · 10,601; Open directory CTA
- `usfansspreadsheet.uk` still 301→`.co.uk`
- `.co.uk` / `.nl` heroes **unchanged** this action
