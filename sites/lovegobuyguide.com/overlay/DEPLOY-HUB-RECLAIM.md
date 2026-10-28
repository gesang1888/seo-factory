# Deploy — LoveGoBuy hub reclaim (2026-10-28)

Action 2 LIVE: strengthen `/lovegobuy-spreadsheet/` + `/lovegobuy-coupon/` + dataset/coupons signals for brand `lovegobuy spreadsheet` SERP vs JadeShip / Reddit / Puro.

Origin: Baota. Root: `/www/wwwroot/lovegobuyguide.com`

## GUARDS

- Surgical overlay only — keep Rubik hub homepage skin; publish stamped reclaim files.
- **Do not** revive Phase C twins (`.eu` / `.ca` / `.es` / spreadsheet.nl / spreadsheet.it) — keep 301.
- **Do not** deepen NL / IT keep heroes this action.
- **Do not** operate external `.co.uk` / lovegobuysheet.org / JadeShip / Puro.
- Do not invent row counts higher than Typesense `found` (11365 → display 11,300+).

## Push

```bash
HUB=/www/wwwroot/lovegobuyguide.com
LOCAL=sites/lovegobuyguide.com/overlay
BAK=/www/backup/lovegobuy-hub-reclaim-$(date +%Y%m%d-%H%M%S)

mkdir -p "$BAK/lovegobuy-spreadsheet" "$BAK/lovegobuy-coupon" "$BAK/finds-dataset" "$BAK/data"
cp -a "$HUB/index.html" "$HUB/llms.txt" "$BAK/" 2>/dev/null || true
cp -a "$HUB/lovegobuy-spreadsheet/index.html" "$BAK/lovegobuy-spreadsheet/" 2>/dev/null || true
cp -a "$HUB/lovegobuy-coupon/index.html" "$BAK/lovegobuy-coupon/" 2>/dev/null || true
cp -a "$HUB/finds-dataset/index.html" "$BAK/finds-dataset/" 2>/dev/null || true
cp -a "$HUB/data/"*.json "$BAK/data/" 2>/dev/null || true

mkdir -p "$HUB/lovegobuy-spreadsheet" "$HUB/lovegobuy-coupon" "$HUB/finds-dataset" "$HUB/data"
cp "$LOCAL/index.html" "$HUB/index.html"
cp "$LOCAL/lovegobuy-spreadsheet/index.html" "$HUB/lovegobuy-spreadsheet/index.html"
cp "$LOCAL/lovegobuy-coupon/index.html" "$HUB/lovegobuy-coupon/index.html"
cp "$LOCAL/finds-dataset/index.html" "$HUB/finds-dataset/index.html"
cp "$LOCAL/data/finds-dataset.json" "$LOCAL/data/coupons-truth.json" "$HUB/data/"
cp "$LOCAL/llms.txt" "$HUB/"
chown -R www:www "$HUB/index.html" "$HUB/lovegobuy-spreadsheet" "$HUB/lovegobuy-coupon" "$HUB/finds-dataset" "$HUB/data" "$HUB/llms.txt"
```

## Verify

- `/lovegobuy-spreadsheet/` title contains Independent Index · 11,300+; CTAs Open directory / Dataset / Coupons; reclaim box names JadeShip / Reddit / Puro; twins 301 note
- `/finds-dataset/` + `/data/finds-dataset.json` last_verified=2026-10-28 · row_count=11365 · hub_reclaim=lovegobuy-hub-reclaim-20261028
- `/lovegobuy-coupon/` + `/data/coupons-truth.json` stamped 2026-10-28
- `/` Independent Index · 11,300+ with Open directory CTA
- .eu/.ca/.es still 301→hub; spreadsheet.nl→.nl; spreadsheet.it→.it; NL/IT still 200 (untouched)
