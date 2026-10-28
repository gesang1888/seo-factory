# Deploy — FansBuy hub reclaim (2026-10-28)

Action 2 LIVE: reclaim hub `fansbuysheets.net` for brand `fansbuy spreadsheet` / coupons / dataset vs **fansbuyspreadsheet.com / fansbuy.org / w2clinks / qcradar**. Observation reinforcement + SERP reclaim — not a full Georgia rewrite.

Origin: Baota. Root: `/www/wwwroot/fansbuysheets.net`

## GUARDS

- Surgical overlay only — publish `index.html.hub-reclaim` (ranked CMS skin); do **not** rsync Georgia `overlay/index.html` over ranked CMS.
- **Do not** deepen UK keep this action (Royal Mail / HMRC hero stays).
- **Do not** revive Phase C / twins (.eu / fansspreadsheet.net / .uk) — keep **301**.
- **Do not** promote nl/de from watch.
- **Do not** operate or mirror-register external fansbuyspreadsheet.com / fansbuy.org / w2clinks / qcradar (name only in copy).
- Do not invent row counts higher than Typesense `found` (11365 → display 11,300+); clear prior inflated 12,000+.

## Push

```bash
HUB=/www/wwwroot/fansbuysheets.net
LOCAL=sites/fansbuysheets.net/overlay
BAK=/www/backup/fansbuy-hub-reclaim-$(date +%Y%m%d-%H%M%S)

mkdir -p "$BAK/fansbuy-spreadsheet" "$BAK/fansbuy-coupons" "$BAK/finds-dataset" "$BAK/is-fansbuy-legit" "$BAK/data"
cp -a "$HUB/index.html" "$HUB/llms.txt" "$HUB/sitemap.xml" "$BAK/" 2>/dev/null || true
cp -a "$HUB/fansbuy-spreadsheet/index.html" "$BAK/fansbuy-spreadsheet/" 2>/dev/null || true
cp -a "$HUB/fansbuy-coupons/index.html" "$BAK/fansbuy-coupons/" 2>/dev/null || true
cp -a "$HUB/finds-dataset/index.html" "$BAK/finds-dataset/" 2>/dev/null || true
cp -a "$HUB/is-fansbuy-legit/index.html" "$BAK/is-fansbuy-legit/" 2>/dev/null || true
cp -a "$HUB/data/"*.json "$BAK/data/" 2>/dev/null || true

mkdir -p "$HUB/fansbuy-spreadsheet" "$HUB/fansbuy-coupons" "$HUB/finds-dataset" "$HUB/is-fansbuy-legit" "$HUB/data"
cp "$LOCAL/index.html.hub-reclaim" "$HUB/index.html"
cp "$LOCAL/fansbuy-spreadsheet/index.html" "$HUB/fansbuy-spreadsheet/index.html"
cp "$LOCAL/fansbuy-coupons/index.html" "$HUB/fansbuy-coupons/index.html"
cp "$LOCAL/finds-dataset/index.html" "$HUB/finds-dataset/index.html"
cp "$LOCAL/is-fansbuy-legit/index.html" "$HUB/is-fansbuy-legit/index.html"
cp "$LOCAL/data/finds-dataset.json" "$LOCAL/data/coupons-truth.json" "$HUB/data/"
cp "$LOCAL/llms.txt" "$HUB/"
# keep existing sitemap.xml unless intentionally refreshed
chown -R www:www "$HUB/index.html" "$HUB/fansbuy-spreadsheet" "$HUB/fansbuy-coupons" "$HUB/finds-dataset" "$HUB/is-fansbuy-legit" "$HUB/data" "$HUB/llms.txt"
```

## Verify

- `/` title Independent Index · 11,300+; H1 Independent Index · 11,300+; CTA **Open directory**; reclaim box names fansbuyspreadsheet.com / fansbuy.org; stamp 2026-10-28
- `/fansbuy-spreadsheet/` title Independent Index · 11,300+; Open directory / Dataset / Coupons CTAs; no inflated 12,000+
- `/finds-dataset/` + `/data/finds-dataset.json` last_verified=2026-10-28 · row_count=11365 · hub_reclaim=fansbuy-hub-reclaim-20261028
- `/fansbuy-coupons/` + `/data/coupons-truth.json` stamped 2026-10-28
- twins still 301→hub / .uk→.co.uk; nl/de still 200 watch; UK untouched this action
