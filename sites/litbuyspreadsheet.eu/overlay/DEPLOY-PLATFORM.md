# Deploy — LitBuy platform opt (2026-10-26)

Origin: Baota host used by portfolio desks.  
Roots: `/www/wwwroot/litbuyspreadsheet.eu` (+ keep `litbuy.at`; watch `litbuyspreadsheets.ca` / `litbuyspreadsheet.it`)

## GUARDS

- **Do not** rsync a new Georgia skin over the ranked hub homepage wholesale — publish only `index.html.platform-patched`.
- Keep AT: surgical hub-uplink fix only (`now.com` → `.eu`).
- Watch CA/IT: light `#local` hub uplink only — **do not** 301.
- **Do not** revive Phase C twins (`litbuyspreadsheets.es` / `.us` / now / me.uk / nl / fr) — already 301→hub.
- Do not invent new country spreadsheet domains.

## Files to push

```bash
HUB=/www/wwwroot/litbuyspreadsheet.eu
LOCAL=sites/litbuyspreadsheet.eu/overlay
BAK=/www/backup/litbuy-platform-$(date +%Y%m%d-%H%M%S)

mkdir -p "$BAK"
cp -a "$HUB/index.html" "$HUB/litbuy-coupons/index.html" "$HUB/llms.txt" "$BAK/" 2>/dev/null || true

cp "$LOCAL/index.html.platform-patched" "$HUB/index.html"
rsync -av "$LOCAL/litbuy-coupons/" "$HUB/litbuy-coupons/"
rsync -av "$LOCAL/finds-dataset/" "$HUB/finds-dataset/"
mkdir -p "$HUB/data"
cp "$LOCAL/data/coupons-truth.json" "$LOCAL/data/finds-dataset.json" "$HUB/data/"
cp "$LOCAL/llms.txt" "$HUB/"

mkdir -p /www/server/panel/vhost/nginx/extension/litbuyspreadsheet.eu
cp "$LOCAL/_deploy/thin-page-redirects.conf"   /www/server/panel/vhost/nginx/extension/litbuyspreadsheet.eu/thin-page-redirects.conf
nginx -t && nginx -s reload

cp sites/litbuy.at/overlay/index.html.platform-patched /www/wwwroot/litbuy.at/index.html
cp sites/litbuyspreadsheets.ca/overlay/index.html.platform-patched /www/wwwroot/litbuyspreadsheets.ca/index.html
cp sites/litbuyspreadsheet.it/overlay/index.html.platform-patched /www/wwwroot/litbuyspreadsheet.it/index.html
```

## GSC

Submit sitemaps for litbuyspreadsheet.eu + litbuy.at (+ optional CA/IT) after deploy.

## Verify

- `/` title contains Independent Index · 11,300+
- Hero CTAs Coupons / Dataset; `#local` money URLs ≤6; footer no live sunset twin links
- `/litbuy-coupons/` has truth callout + 26 Oct 2026
- `/data/*.json` + `/finds-dataset/` → 200
- `/coupons.html` → 301 `/litbuy-coupons/`
- AT uplink → litbuyspreadsheet.eu (not now.com)
- CA/IT still 200 with hub uplink; es/us still 301
