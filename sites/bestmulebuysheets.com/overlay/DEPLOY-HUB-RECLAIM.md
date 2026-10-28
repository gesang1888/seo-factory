# Deploy — MuleBuy hub reclaim (2026-10-28)

Action 2 LIVE: strengthen hub Independent Index · 8,000+ + `/mulebuy-spreadsheet.html` + coupons/dataset for brand `mulebuy spreadsheet` SERP.

Origin: Baota. Root: `/www/wwwroot/bestmulebuysheets.com`

## GUARDS

- Surgical overlay only — **do not** wholesale-replace ranked homepage skin beyond `index.html.hub-reclaim`.
- **Do not** deepen FR keep (Colissimo / douane hero untouched).
- **Do not** revive Phase B/C twins (`.co.uk` / `.es` / `.us`) — keep 301→hub.
- **Do not** invent row counts above the established hub claim (**8,000+**; Typesense unfiltered found is NOT MuleBuy-only).
- External mymulebuyspreadsheet / mulegrid / mulebuysheets / w2cspreadsheet: **name in copy only** — do not mirror or register.

## Push

```bash
HUB=/www/wwwroot/bestmulebuysheets.com
LOCAL=sites/bestmulebuysheets.com/overlay
BAK=/www/backup/mulebuy-hub-reclaim-$(date +%Y%m%d-%H%M%S)

mkdir -p "$BAK/mulebuy-coupons" "$BAK/finds-dataset" "$BAK/data"
cp -a "$HUB/index.html" "$HUB/mulebuy-spreadsheet.html" "$HUB/llms.txt" "$HUB/sitemap.xml" "$BAK/" 2>/dev/null || true
cp -a "$HUB/mulebuy-coupons/index.html" "$BAK/mulebuy-coupons/" 2>/dev/null || true
cp -a "$HUB/finds-dataset/index.html" "$BAK/finds-dataset/" 2>/dev/null || true
cp -a "$HUB/data/"*.json "$BAK/data/" 2>/dev/null || true

cp "$LOCAL/index.html.hub-reclaim" "$HUB/index.html"
cp "$LOCAL/mulebuy-spreadsheet.html.hub-reclaim" "$HUB/mulebuy-spreadsheet.html"
mkdir -p "$HUB/mulebuy-coupons" "$HUB/finds-dataset" "$HUB/data"
cp "$LOCAL/mulebuy-coupons/index.html" "$HUB/mulebuy-coupons/index.html"
cp "$LOCAL/finds-dataset/index.html" "$HUB/finds-dataset/index.html"
cp "$LOCAL/data/finds-dataset.json" "$LOCAL/data/coupons-truth.json" "$HUB/data/"
cp "$LOCAL/llms.txt" "$LOCAL/sitemap.xml" "$HUB/"
```

## Verify

- `/` title still Independent Index · 8,000+; primary CTA **Open directory**; reclaim box names mymule… / mulegrid / mulebuysheets / w2cspreadsheet
- `/mulebuy-spreadsheet.html` title/H1 → Independent Index · 8,000+; CTAs Open directory / Dataset / Coupons; reclaim box
- `/mulebuy-coupons/` + `/finds-dataset/` + JSON `last_verified=2026-10-28` · `hub_reclaim=mulebuy-hub-reclaim-20261028`
- twins .co.uk/.es/.us still 301→hub; FR still Colissimo hero (untouched)
