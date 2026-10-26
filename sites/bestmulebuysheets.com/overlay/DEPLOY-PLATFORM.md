# Deploy — MuleBuy platform opt (2026-10-26)

Origin: Baota host used by portfolio desks.  
Roots: `/www/wwwroot/bestmulebuysheets.com` (+ keep `mulebuy.fr`)

## GUARDS

- **Do not** rsync a new skin over the ranked hub homepage wholesale — publish only `index.html.platform-patched`.
- Keep `mulebuy.fr`: surgical hub-uplink / `#local` only — **do not** 301, **do not** overwrite Colissimo / douane hero.
- **Do not** revive Phase B twins (`mulebuyspreadsheets.co.uk` / `.es` / `.us`) — already 301.
- Do not invent new country spreadsheet domains.
- Hub must **not** link sunset twins as live desks.

## Files to push

```bash
HUB=/www/wwwroot/bestmulebuysheets.com
LOCAL=sites/bestmulebuysheets.com/overlay
BAK=/www/backup/mulebuy-platform-$(date +%Y%m%d-%H%M%S)

mkdir -p "$BAK"
cp -a "$HUB/index.html" "$HUB/sitemap.xml" "$HUB/llms.txt" "$BAK/" 2>/dev/null || true

cp "$LOCAL/index.html.platform-patched" "$HUB/index.html"
rsync -av "$LOCAL/mulebuy-coupons/" "$HUB/mulebuy-coupons/"
rsync -av "$LOCAL/finds-dataset/" "$HUB/finds-dataset/"
mkdir -p "$HUB/data"
cp "$LOCAL/data/coupons-truth.json" "$LOCAL/data/finds-dataset.json" "$HUB/data/"
cp "$LOCAL/llms.txt" "$LOCAL/sitemap.xml" "$HUB/"

mkdir -p /www/server/panel/vhost/nginx/extension/bestmulebuysheets.com
cp "$LOCAL/_deploy/thin-page-redirects.conf" \
  /www/server/panel/vhost/nginx/extension/bestmulebuysheets.com/thin-page-redirects.conf
# ensure extension include exists in vhost if missing
nginx -t && nginx -s reload

cp sites/mulebuy.fr/overlay/index.html.platform-patched /www/wwwroot/mulebuy.fr/index.html
```

## GSC

Submit sitemaps for bestmulebuysheets.com + mulebuy.fr after deploy.

## Verify

- `/` title contains Independent Index · 8,000+
- Hero CTAs Spreadsheet / Coupons / Dataset / Register; `#local` money URLs ≤6; footer no live sunset twin links
- `/mulebuy-coupons/` has truth callout + 26 Oct 2026
- `/data/*.json` + `/finds-dataset/` + `/llms.txt` → 200
- `/coupons.html` → 301 `/mulebuy-coupons/`
- FR uplink mentions dataset/coupons; Colissimo hero intact
- twins .co.uk/.es/.us still 301→hub
