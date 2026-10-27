# Deploy — Kakobuy hub reclaim (2026-10-27)

Action 1 LIVE: strengthen `/kakobuy-spreadsheet/` + dataset/coupons signals for brand `kakobuy spreadsheet` SERP.

Origin: Baota. Root: `/www/wwwroot/kakobuydocs.com`

## GUARDS

- Surgical overlay only — **do not** wholesale-replace ranked homepage skin beyond stamped platform-patched file.
- **Do not** revive Phase C twins (`kakobuytips.com` / `kakospreadsheet.fr` / `.nl`) — keep 301→hub.
- **Do not** touch FI/ES/CA heroes (keep desks already uplink; not this action).
- Do not invent row counts higher than Typesense `found` (11365 → display 11,300+).

## Push

```bash
HUB=/www/wwwroot/kakobuydocs.com
LOCAL=sites/kakobuydocs.com/overlay
BAK=/www/backup/kakobuy-hub-reclaim-$(date +%Y%m%d-%H%M%S)

mkdir -p "$BAK/kakobuy-spreadsheet" "$BAK/finds-dataset" "$BAK/kakobuy-coupons" "$BAK/data"
cp -a "$HUB/kakobuy-spreadsheet/index.html" "$BAK/kakobuy-spreadsheet/" 2>/dev/null || true
cp -a "$HUB/finds-dataset/index.html" "$BAK/finds-dataset/" 2>/dev/null || true
cp -a "$HUB/kakobuy-coupons/index.html" "$BAK/kakobuy-coupons/" 2>/dev/null || true
cp -a "$HUB/index.html" "$HUB/llms.txt" "$HUB/data/"*.json "$BAK/" 2>/dev/null || true

mkdir -p "$HUB/kakobuy-spreadsheet" "$HUB/finds-dataset" "$HUB/kakobuy-coupons" "$HUB/data"
cp "$LOCAL/kakobuy-spreadsheet/index.html" "$HUB/kakobuy-spreadsheet/index.html"
cp "$LOCAL/finds-dataset/index.html" "$HUB/finds-dataset/index.html"
cp "$LOCAL/kakobuy-coupons/index.html" "$HUB/kakobuy-coupons/index.html"
cp "$LOCAL/index.html.platform-patched" "$HUB/index.html"
cp "$LOCAL/data/finds-dataset.json" "$LOCAL/data/coupons-truth.json" "$HUB/data/"
cp "$LOCAL/llms.txt" "$HUB/"
```

## Verify

- `/kakobuy-spreadsheet/` title contains Independent Index · 11,300+; CTAs Dataset/Coupons/Open directory; reclaim box; twins 301 note
- `/finds-dataset/` + `/data/finds-dataset.json` last_verified=2026-10-27 · row_count=11365
- `/kakobuy-coupons/` + `/data/coupons-truth.json` stamped 2026-10-27
- `/` still Independent Index · 11,300+
- tips/.fr/.nl still 301→hub
