# Deploy — CSSBuy hub reclaim (2026-10-28)

Action 2 LIVE: reclaim hub `cssbuyspreadsheet.eu` for brand `cssbuy spreadsheet` / coupons / dataset vs **W2C / JadeShip / Reddit**, and stop **NL desk** spreadsheet cannibalization on `cssbuy.nl`.

Origin: Baota. Roots: `/www/wwwroot/cssbuyspreadsheet.eu` + `/www/wwwroot/cssbuy.nl`

## GUARDS

- Surgical overlay only — publish `index.html.hub-reclaim` (Barlow hub skin); do **not** rsync Georgia `overlay/index.html` over ranked CMS if it diverges.
- **Do not** deepen ES keep this action.
- **Do not** revive Phase C / twins (spreadsheet.es/nl/it/fr → desks; .de/.us/.at/.ca/.uk → hub) — keep 301.
- **Do not** roll NL back to Spreadsheet H1 — keep Douane / NL-postcode hero; anti-cannibal uplink only.
- Do not invent row counts higher than Typesense `found` (11365 → display 11,300+).
- Do not operate external W2C / JadeShip / github.io / .life domains (name only in copy).

## Push

```bash
HUB=/www/wwwroot/cssbuyspreadsheet.eu
NL=/www/wwwroot/cssbuy.nl
LOCAL=sites/cssbuyspreadsheet.eu/overlay
NLLOC=sites/cssbuy.nl/overlay
BAK=/www/backup/cssbuy-hub-reclaim-$(date +%Y%m%d-%H%M%S)

mkdir -p "$BAK/spreadsheet" "$BAK/cssbuy-coupons" "$BAK/finds-dataset" "$BAK/is-cssbuy-legit" "$BAK/data" "$BAK/nl"
cp -a "$HUB/index.html" "$HUB/llms.txt" "$BAK/" 2>/dev/null || true
cp -a "$HUB/spreadsheet/index.html" "$BAK/spreadsheet/" 2>/dev/null || true
cp -a "$HUB/cssbuy-coupons/index.html" "$BAK/cssbuy-coupons/" 2>/dev/null || true
cp -a "$HUB/finds-dataset/index.html" "$BAK/finds-dataset/" 2>/dev/null || true
cp -a "$HUB/is-cssbuy-legit/index.html" "$BAK/is-cssbuy-legit/" 2>/dev/null || true
cp -a "$HUB/data/"*.json "$BAK/data/" 2>/dev/null || true
cp -a "$NL/index.html" "$BAK/nl/" 2>/dev/null || true

mkdir -p "$HUB/spreadsheet" "$HUB/cssbuy-coupons" "$HUB/finds-dataset" "$HUB/is-cssbuy-legit" "$HUB/data"
cp "$LOCAL/index.html.hub-reclaim" "$HUB/index.html"
cp "$LOCAL/spreadsheet/index.html" "$HUB/spreadsheet/index.html"
cp "$LOCAL/cssbuy-coupons/index.html" "$HUB/cssbuy-coupons/index.html"
cp "$LOCAL/finds-dataset/index.html" "$HUB/finds-dataset/index.html"
cp "$LOCAL/is-cssbuy-legit/index.html" "$HUB/is-cssbuy-legit/index.html"
cp "$LOCAL/data/finds-dataset.json" "$LOCAL/data/coupons-truth.json" "$HUB/data/"
cp "$LOCAL/llms.txt" "$HUB/"
cp "$NLLOC/index.html.hub-reclaim" "$NL/index.html"
chown -R www:www "$HUB/index.html" "$HUB/spreadsheet" "$HUB/cssbuy-coupons" "$HUB/finds-dataset" "$HUB/is-cssbuy-legit" "$HUB/data" "$HUB/llms.txt" "$NL/index.html"
```

## Verify

- `/` title Independent Index · 11,300+; CTA **Open directory**; reclaim box names W2C / JadeShip / Reddit; stamp 2026-10-28
- `/spreadsheet/` title Independent Index · 11,300+; Open directory / Dataset / Coupons CTAs
- `/finds-dataset/` + `/data/finds-dataset.json` last_verified=2026-10-28 · row_count=11365 · hub_reclaim=cssbuy-hub-reclaim-20261028
- `/cssbuy-coupons/` + `/data/coupons-truth.json` stamped 2026-10-28
- `cssbuy.nl/` title still NL-postcode/Douane; H1 unchanged; hub-uplink anti-cannibal; JSON-LD name not “Spreadsheet”
- twins sheet.es/nl/it/fr still 301→desks; .de/.us still 301→hub; ES keep untouched
