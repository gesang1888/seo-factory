# Deploy — AllChinaBuy platform opt (2026-10-26)

Origin: Baota host used by portfolio desks.  
Roots: `/www/wwwroot/allchina-buy.com` (+ keep desks `acbuyspreadsheets.nl` / `allchinabuyspreadsheets.co.uk`)

## GUARDS

- **Do not** rsync Georgia desk skins over ranked CMS homepages.
- Publish hub homepage only from `index.html.platform-patched`.
- Keep desks: surgical `#local` uplink only from `index.html.platform-patched`.
- **Do not** revive `allchinabuyspreadsheet.nl` / `.ca` (already 301 → keep desks).
- **Do not** rewrite `acbuyspreadsheets.ca` (Phase A redirect-target — protect only).
- Keep existing Step3 thin customs redirects; add coupons.html 301 only.

## Files to push

```bash
HUB=/www/wwwroot/allchina-buy.com
LOCAL=sites/allchina-buy.com/overlay

cp -a "$HUB" "/www/backup/allchinabuy-platform-$(date +%Y%m%d-%H%M%S)"

cp "$LOCAL/index.html.platform-patched" "$HUB/index.html"
rsync -av "$LOCAL/allchinabuy-coupons/" "$HUB/allchinabuy-coupons/"
rsync -av "$LOCAL/finds-dataset/" "$HUB/finds-dataset/"
mkdir -p "$HUB/data"
cp "$LOCAL/data/coupons-truth.json" "$LOCAL/data/finds-dataset.json" "$HUB/data/"
cp "$LOCAL/llms.txt" "$LOCAL/sitemap.xml" "$HUB/"

# nginx thin redirects (coupons.html → /allchinabuy-coupons/)
cp "$LOCAL/_deploy/thin-page-redirects.conf" \
  /www/server/panel/vhost/nginx/extension/allchina-buy.com/thin-page-redirects.conf
nginx -t && nginx -s reload

cp sites/acbuyspreadsheets.nl/overlay/index.html.platform-patched \
  /www/wwwroot/acbuyspreadsheets.nl/index.html
cp sites/allchinabuyspreadsheets.co.uk/overlay/index.html.platform-patched \
  /www/wwwroot/allchinabuyspreadsheets.co.uk/index.html
```

## GSC

Submit sitemaps for allchina-buy.com + keep desks after deploy. Leave CA untouched.

## Verify

- `/` title contains Independent Index · 11,300+
- `/#local` money URLs + keep desks; hreflang points at keep desks (not sunset twins)
- `/allchinabuy-coupons/` has truth callout + date 26 Oct 2026
- `/data/coupons-truth.json` + `/data/finds-dataset.json` + `/finds-dataset/` → 200
- `/coupons.html` → 301 `/allchinabuy-coupons/`
- NL/UK `#local` hub-uplink mentions dataset
- CA / sunset twins untouched (twins still 301)
