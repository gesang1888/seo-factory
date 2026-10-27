# Deploy — SugarGoo hub reclaim (2026-10-27)

Action 2 LIVE: strengthen `/best-sugargoo-spreadsheet-2026.html` + `/sugargoo-coupon-2026.html` + dataset/coupons signals for brand `sugargoo spreadsheet` SERP.

Origin: Baota. Root: `/www/wwwroot/sugargoospreadsheetnow.com`

## GUARDS

- Surgical overlay only — **do not** wholesale-replace ranked homepage skin beyond stamped platform-patched file.
- **Do not** revive Phase C twins (`us` / `uk` / `es` / `fr` / `de` / `nl` / `at` / `spreadsheets2026.ca`) — keep 301→hub.
- **Do not** touch AU keep hero (separate worker / action 1).
- **Do not** operate external `sugargoo.ca` / `.es` / `.pt` / `.cheap`.
- Do not invent row counts higher than Typesense `found` (11365 → display 11,300+).

## Push

```bash
HUB=/www/wwwroot/sugargoospreadsheetnow.com
LOCAL=sites/sugargoospreadsheetnow.com/overlay
BAK=/www/backup/sugargoo-hub-reclaim-$(date +%Y%m%d-%H%M%S)

mkdir -p "$BAK/finds-dataset" "$BAK/data"
cp -a "$HUB/best-sugargoo-spreadsheet-2026.html" "$HUB/sugargoo-coupon-2026.html" "$HUB/index.html" "$BAK/" 2>/dev/null || true
cp -a "$HUB/finds-dataset/index.html" "$BAK/finds-dataset/" 2>/dev/null || true
cp -a "$HUB/llms.txt" "$HUB/data/"*.json "$BAK/" 2>/dev/null || true

mkdir -p "$HUB/finds-dataset" "$HUB/data"
cp "$LOCAL/best-sugargoo-spreadsheet-2026.html" "$HUB/best-sugargoo-spreadsheet-2026.html"
cp "$LOCAL/sugargoo-coupon-2026.html" "$HUB/sugargoo-coupon-2026.html"
cp "$LOCAL/finds-dataset/index.html" "$HUB/finds-dataset/index.html"
cp "$LOCAL/index.html.platform-patched" "$HUB/index.html"
cp "$LOCAL/data/finds-dataset.json" "$LOCAL/data/coupons-truth.json" "$HUB/data/"
cp "$LOCAL/llms.txt" "$HUB/"
chown -R www:www "$HUB/best-sugargoo-spreadsheet-2026.html" "$HUB/sugargoo-coupon-2026.html" "$HUB/index.html" "$HUB/finds-dataset" "$HUB/data" "$HUB/llms.txt"
```

## Verify

- `/best-sugargoo-spreadsheet-2026.html` title contains Independent Index · 11,300+; CTAs Open directory / Dataset / Coupons; reclaim box; twins 301 note
- `/finds-dataset/` + `/data/finds-dataset.json` last_verified=2026-10-27 · row_count=11365
- `/sugargoo-coupon-2026.html` + `/data/coupons-truth.json` stamped 2026-10-27
- `/` Independent Index · 11,300+ with Open directory CTA; category wall kept
- us/uk/es/fr/de/nl/at/ca still 301→hub; AU still 200 (untouched)
