# Deploy — Spam-hub SERP recovery LIVE (2026-10-29)

Track 1 LIVE: hold `basetao spreadsheet` ~#1 CTR via Independent Index snippet + dataset citation vs JadeShip/link farms.

Tag: `spam-hub-serp-live-20261029` · stamp `2026-10-29`

Origin: Baota. Root: `/www/wwwroot/basetaospreadsheet.com`

## GUARDS

- Publish homepage **only** from `index.html.platform-patched` (never Georgia `overlay/index.html`).
- **Do not** revive `basetaospreadsheet.shop` or invent country desks.
- Do not invent row counts above Typesense `found` (11365 → display **11,300+**).
- Referral/calculator stay secondary to spreadsheet hero.

## Push

```bash
ROOT=/www/wwwroot/basetaospreadsheet.com
LOCAL=sites/basetaospreadsheet.com/overlay
BAK=/www/backup/basetao-spam-hub-serp-$(date +%Y%m%d-%H%M%S)

mkdir -p "$BAK"
cp -a "$ROOT/index.html" "$ROOT/llms.txt" "$ROOT/sitemap.xml" \
  "$ROOT/basetao-coupon-tracker-2026.html" "$ROOT/finds-dataset" "$ROOT/data" "$BAK/" 2>/dev/null || true

cp "$LOCAL/index.html.platform-patched" "$ROOT/index.html"
mkdir -p "$ROOT/finds-dataset" "$ROOT/data"
cp "$LOCAL/finds-dataset/index.html" "$ROOT/finds-dataset/index.html"
cp "$LOCAL/basetao-coupon-tracker-2026.html" "$ROOT/basetao-coupon-tracker-2026.html"
cp "$LOCAL/data/finds-dataset.json" "$LOCAL/data/coupons-truth.json" "$ROOT/data/"
cp "$LOCAL/llms.txt" "$LOCAL/sitemap.xml" "$ROOT/"
```

## Verify

- `/` H1 **Basetao Spreadsheet 2026 — Independent Index · 11,300+**
- Meta/FAQ mention JadeShip differentiation + `row_count=11365`
- `/finds-dataset/` + JSON `last_verified=2026-10-29` · `spam_hub_serp=…`
- No `.shop` revival
