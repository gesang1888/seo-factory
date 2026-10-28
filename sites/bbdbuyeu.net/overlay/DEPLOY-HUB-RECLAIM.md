# Deploy — BBDBuy hub reclaim (2026-10-28)

Action 2 LIVE: strengthen `/bbdbuyeu-spreadsheet/` + `/bbdbuyeu-coupons/` + dataset/coupons signals for brand `bbdbuy spreadsheet` SERP.

Origin: Baota. Root: `/www/wwwroot/bbdbuyeu.net`

## GUARDS

- Surgical overlay only — keep on-site `/api/products/` search on spreadsheet page.
- **Do not** revive Phase C twins (`bbdbuyeuspreadsheet.com` / sheet.ca·uk·us / `.de`) — keep 301.
- **Do not** deepen IT / touch CA·UK·US heroes (separate actions).
- Do not invent row counts higher than API/Typesense `found` (**11365** → display **11,300+**).
- Do not touch external `.co.uk` / `.org` / competing sheet dirs.

## Push

```bash
HUB=/www/wwwroot/bbdbuyeu.net
LOCAL=sites/bbdbuyeu.net/overlay
BAK=/www/backup/bbdbuy-hub-reclaim-$(date +%Y%m%d-%H%M%S)

mkdir -p "$BAK/bbdbuyeu-spreadsheet" "$BAK/bbdbuyeu-coupons" "$BAK/finds-dataset" "$BAK/data"
cp -a "$HUB/bbdbuyeu-spreadsheet/index.html" "$BAK/bbdbuyeu-spreadsheet/" 2>/dev/null || true
cp -a "$HUB/bbdbuyeu-coupons/index.html" "$BAK/bbdbuyeu-coupons/" 2>/dev/null || true
cp -a "$HUB/finds-dataset/index.html" "$BAK/finds-dataset/" 2>/dev/null || true
cp -a "$HUB/index.html" "$HUB/llms.txt" "$HUB/data/"*.json "$BAK/" 2>/dev/null || true

mkdir -p "$HUB/bbdbuyeu-spreadsheet" "$HUB/bbdbuyeu-coupons" "$HUB/finds-dataset" "$HUB/data"
cp "$LOCAL/bbdbuyeu-spreadsheet/index.html" "$HUB/bbdbuyeu-spreadsheet/index.html"
cp "$LOCAL/bbdbuyeu-coupons/index.html" "$HUB/bbdbuyeu-coupons/index.html"
cp "$LOCAL/finds-dataset/index.html" "$HUB/finds-dataset/index.html"
cp "$LOCAL/index.html" "$HUB/index.html"
cp "$LOCAL/data/finds-dataset.json" "$LOCAL/data/coupons-truth.json" "$HUB/data/"
cp "$LOCAL/llms.txt" "$HUB/"
```

## Verify

- `/bbdbuyeu-spreadsheet/` title contains Independent Index · 11,300+; CTAs Open directory / Dataset / Coupons; reclaim box; twins 301 note
- `/finds-dataset/` + `/data/finds-dataset.json` last_verified=2026-10-28 · row_count=11365
- `/bbdbuyeu-coupons/` + `/data/coupons-truth.json` stamped 2026-10-28 · BBD5OFF / 1QodRw
- `/` Independent Index · 11,300+ · Open directory
- sheet.ca→.ca · .uk→.uk · .us→.us · .com→hub · .de→hub still 301
- bbdbuy.it hero unchanged (not this action)
