# Deploy — FSBuy platform opt (2026-10-26)

Origin: Baota host used by portfolio desks.  
Root: `/www/wwwroot/fsbuyspreadsheets.com`

## GUARDS

- **Do not** rsync leftover Georgia dest `overlay/index.html` over the ranked CMS homepage — publish only `index.html.platform-patched`.
- **Do not** revive Phase C sunsets; do not invent country spreadsheet domains; do not revive 410 twin `fsbuyspreadsheet.org`.
- Hub must **not** treat lookalike hosts (e.g. fsbuy.org) as keep desks.
- Nginx vhost already `include .../extension/fsbuyspreadsheets.com/*.conf` (keep it).

## Files to push

```bash
HUB=/www/wwwroot/fsbuyspreadsheets.com
LOCAL=sites/fsbuyspreadsheets.com/overlay
BAK=/www/backup/fsbuy-platform-$(date +%Y%m%d-%H%M%S)
NGX=/www/server/panel/vhost/nginx/fsbuyspreadsheets.com.conf

mkdir -p "$BAK"
cp -a "$HUB/index.html" "$HUB/sitemap.xml" "$HUB/coupons.html" "$BAK/" 2>/dev/null || true
cp -a "$HUB/fsbuy-coupons" "$BAK/fsbuy-coupons" 2>/dev/null || true
cp -a "$NGX" "$BAK/fsbuyspreadsheets.com.conf.bak"

cp "$LOCAL/index.html.platform-patched" "$HUB/index.html"
mkdir -p "$HUB/fsbuy-coupons"
cp "$LOCAL/fsbuy-coupons/index.html" "$HUB/fsbuy-coupons/index.html"
rsync -av "$LOCAL/finds-dataset/" "$HUB/finds-dataset/"
mkdir -p "$HUB/data"
cp "$LOCAL/data/coupons-truth.json" "$LOCAL/data/finds-dataset.json" "$HUB/data/"
cp "$LOCAL/llms.txt" "$LOCAL/sitemap.xml" "$HUB/"

mkdir -p /www/server/panel/vhost/nginx/extension/fsbuyspreadsheets.com
cp "$LOCAL/_deploy/thin-page-redirects.conf" \
  /www/server/panel/vhost/nginx/extension/fsbuyspreadsheets.com/thin-page-redirects.conf
nginx -t && nginx -s reload
```

## GSC

Submit `https://fsbuyspreadsheets.com/sitemap.xml` after deploy.

## Verify

- `/` title contains Independent Index · 12,400+
- Hero CTAs Spreadsheet / Coupons / Dataset / Register; `#local` money URLs ≤6
- `/fsbuy-coupons/` has truth callout + 26 Oct 2026 + FAQ-LD
- `/data/*.json` + `/finds-dataset/` + `/llms.txt` → 200
- `/coupons/` · `/coupons.html` → 301 `/fsbuy-coupons/`
- `fsbuyspreadsheet.org` still 410 (not revived)
