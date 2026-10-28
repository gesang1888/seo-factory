# Deploy — MyCNBox hub reclaim (2026-10-28)

Action 2 LIVE: reclaim hub `mycnbox.eu` for brand `mycnbox spreadsheet` / coupons / dataset vs **mycnbox.net / mycnboxsheet.org / official mycnbox.com**. Observation reinforcement + SERP reclaim — not a full Georgia rewrite.

Origin: Baota. Root: `/www/wwwroot/mycnbox.eu`

## GUARDS

- Surgical overlay only — publish `index.html.hub-reclaim` (Poppins hub skin); do **not** rsync Georgia `overlay/index.html` over ranked CMS.
- **Do not** deepen NL keep this action (Douane / NL-postcode hero stays).
- **Do not** revive Phase C / watch (es/de/fr) or haul twin — keep haul **301 → .eu**.
- **Do not** operate or mirror-register external mycnbox.net / mycnbox.com / mycnboxsheet.org (name only in copy).
- Do not invent row counts higher than Typesense `found` (11365 → display 11,300+).
- Do not touch UK/PL heroes this action.

## Push

```bash
HUB=/www/wwwroot/mycnbox.eu
LOCAL=sites/mycnbox.eu/overlay
BAK=/www/backup/mycnbox-hub-reclaim-$(date +%Y%m%d-%H%M%S)

mkdir -p "$BAK/mycnbox-spreadsheet" "$BAK/mycnbox-coupons" "$BAK/finds-dataset" "$BAK/is-mycnbox-legit" "$BAK/data"
cp -a "$HUB/index.html" "$HUB/llms.txt" "$HUB/sitemap.xml" "$BAK/" 2>/dev/null || true
cp -a "$HUB/mycnbox-spreadsheet/index.html" "$BAK/mycnbox-spreadsheet/" 2>/dev/null || true
cp -a "$HUB/mycnbox-coupons/index.html" "$BAK/mycnbox-coupons/" 2>/dev/null || true
cp -a "$HUB/finds-dataset/index.html" "$BAK/finds-dataset/" 2>/dev/null || true
cp -a "$HUB/is-mycnbox-legit/index.html" "$BAK/is-mycnbox-legit/" 2>/dev/null || true
cp -a "$HUB/data/"*.json "$BAK/data/" 2>/dev/null || true

mkdir -p "$HUB/mycnbox-spreadsheet" "$HUB/mycnbox-coupons" "$HUB/finds-dataset" "$HUB/is-mycnbox-legit" "$HUB/data"
cp "$LOCAL/index.html.hub-reclaim" "$HUB/index.html"
cp "$LOCAL/mycnbox-spreadsheet/index.html" "$HUB/mycnbox-spreadsheet/index.html"
cp "$LOCAL/mycnbox-coupons/index.html" "$HUB/mycnbox-coupons/index.html"
cp "$LOCAL/finds-dataset/index.html" "$HUB/finds-dataset/index.html"
cp "$LOCAL/is-mycnbox-legit/index.html" "$HUB/is-mycnbox-legit/index.html"
cp "$LOCAL/data/finds-dataset.json" "$LOCAL/data/coupons-truth.json" "$HUB/data/"
cp "$LOCAL/llms.txt" "$LOCAL/sitemap.xml" "$HUB/"
chown -R www:www "$HUB/index.html" "$HUB/mycnbox-spreadsheet" "$HUB/mycnbox-coupons" "$HUB/finds-dataset" "$HUB/is-mycnbox-legit" "$HUB/data" "$HUB/llms.txt" "$HUB/sitemap.xml"
```

## Verify

- `/` title Independent Index · 11,300+; H1 Independent Index · 11,300+; CTA **Open directory**; reclaim box names mycnbox.net / sheet.org; stamp 2026-10-28
- `/mycnbox-spreadsheet/` title Independent Index · 11,300+; Open directory / Dataset / Coupons CTAs; no inflated 12,000+
- `/finds-dataset/` + `/data/finds-dataset.json` last_verified=2026-10-28 · row_count=11365 · hub_reclaim=mycnbox-hub-reclaim-20261028
- `/mycnbox-coupons/` + `/data/coupons-truth.json` stamped 2026-10-28
- haul still 301→.eu; es/de/fr still 200 watch; NL/UK/PL untouched this action
