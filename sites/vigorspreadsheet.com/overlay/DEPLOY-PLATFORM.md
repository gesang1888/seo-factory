# Deploy — VigorBuy platform opt (2026-10-26)

Origin: Baota host used by portfolio desks.  
Root: `/www/wwwroot/vigorspreadsheet.com`

## GUARDS

- **Do not** rsync leftover Georgia dest `overlay/index.html` over the ranked CMS homepage — publish only `index.html.platform-patched`.
- **Do not** revive Phase C sunsets; do not invent country spreadsheet domains.
- Hub must **not** treat lookalike hosts as keep desks.
- Nginx vhost must `include .../extension/vigorspreadsheet.com/*.conf` (was missing before this opt).

## Files to push

```bash
HUB=/www/wwwroot/vigorspreadsheet.com
LOCAL=sites/vigorspreadsheet.com/overlay
BAK=/www/backup/vigorbuy-platform-$(date +%Y%m%d-%H%M%S)
NGX=/www/server/panel/vhost/nginx/vigorspreadsheet.com.conf

mkdir -p "$BAK"
cp -a "$HUB/index.html" "$HUB/sitemap.xml" "$HUB/coupons.html" "$BAK/" 2>/dev/null || true
cp -a "$HUB/vigorbuy-coupons" "$BAK/vigorbuy-coupons" 2>/dev/null || true
cp -a "$NGX" "$BAK/vigorspreadsheet.com.conf.bak"

cp "$LOCAL/index.html.platform-patched" "$HUB/index.html"
mkdir -p "$HUB/vigorbuy-coupons"
cp "$LOCAL/vigorbuy-coupons/index.html" "$HUB/vigorbuy-coupons/index.html"
rsync -av "$LOCAL/finds-dataset/" "$HUB/finds-dataset/"
mkdir -p "$HUB/data"
cp "$LOCAL/data/coupons-truth.json" "$LOCAL/data/finds-dataset.json" "$HUB/data/"
cp "$LOCAL/llms.txt" "$LOCAL/sitemap.xml" "$HUB/"

mkdir -p /www/server/panel/vhost/nginx/extension/vigorspreadsheet.com
cp "$LOCAL/_deploy/thin-page-redirects.conf" \
  /www/server/panel/vhost/nginx/extension/vigorspreadsheet.com/thin-page-redirects.conf
# Ensure SSL server block includes extension/*.conf before location /
nginx -t && nginx -s reload
```

## GSC

Submit `https://vigorspreadsheet.com/sitemap.xml` after deploy.

## Verify

- `/` title contains Independent Index · 12,400+
- Hero CTAs Spreadsheet / Coupons / Dataset / Register; `#local` money URLs ≤6
- `/vigorbuy-coupons/` has truth callout + 26 Oct 2026 + FAQ-LD
- `/data/*.json` + `/finds-dataset/` + `/llms.txt` → 200
- `/coupons/` · `/coupons.html` → 301 `/vigorbuy-coupons/`
