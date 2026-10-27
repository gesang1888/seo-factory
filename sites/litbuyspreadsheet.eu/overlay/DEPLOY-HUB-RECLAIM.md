# Deploy — LitBuy hub reclaim (2026-10-27)

Action 2 LIVE: strengthen `/litbuy-spreadsheet/` + dataset/coupons signals for brand `litbuy spreadsheet` SERP.

Origin: Baota. Root: `/www/wwwroot/litbuyspreadsheet.eu`

## GUARDS

- Surgical overlay only — **do not** wholesale-replace ranked homepage skin beyond stamped platform-patched file.
- **Do not** revive Phase C twins (`now.com` / `.es` / `.us` / me.uk / nl / fr) — keep 301→hub.
- **Do not** touch AT keep hero or CA/IT watch heroes (not this action).
- Do not invent row counts higher than Typesense `found` (11365 → display 11,300+).

## Push

```bash
HUB=/www/wwwroot/litbuyspreadsheet.eu
LOCAL=sites/litbuyspreadsheet.eu/overlay
BAK=/www/backup/litbuy-hub-reclaim-$(date +%Y%m%d-%H%M%S)

mkdir -p "$BAK/litbuy-spreadsheet" "$BAK/finds-dataset" "$BAK/litbuy-coupons" "$BAK/data"
cp -a "$HUB/litbuy-spreadsheet/index.html" "$BAK/litbuy-spreadsheet/" 2>/dev/null || true
cp -a "$HUB/finds-dataset/index.html" "$BAK/finds-dataset/" 2>/dev/null || true
cp -a "$HUB/litbuy-coupons/index.html" "$BAK/litbuy-coupons/" 2>/dev/null || true
cp -a "$HUB/index.html" "$HUB/llms.txt" "$HUB/data/"*.json "$BAK/" 2>/dev/null || true

mkdir -p "$HUB/litbuy-spreadsheet" "$HUB/finds-dataset" "$HUB/litbuy-coupons" "$HUB/data"
cp "$LOCAL/litbuy-spreadsheet/index.html" "$HUB/litbuy-spreadsheet/index.html"
cp "$LOCAL/finds-dataset/index.html" "$HUB/finds-dataset/index.html"
cp "$LOCAL/litbuy-coupons/index.html" "$HUB/litbuy-coupons/index.html"
cp "$LOCAL/index.html.platform-patched" "$HUB/index.html"
cp "$LOCAL/data/finds-dataset.json" "$LOCAL/data/coupons-truth.json" "$HUB/data/"
cp "$LOCAL/llms.txt" "$HUB/"
```

## Verify

- `/litbuy-spreadsheet/` title contains Independent Index · 11,300+; CTAs Open directory / Dataset / Coupons; reclaim box; twins 301 note
- `/finds-dataset/` + `/data/finds-dataset.json` last_verified=2026-10-27 · row_count=11365
- `/litbuy-coupons/` + `/data/coupons-truth.json` stamped 2026-10-27
- `/` still Independent Index · 11,300+ with Open directory CTA
- now/es/us/me.uk/nl/fr still 301→hub
