# Deploy — FishGoo platform opt (2026-10-26)

Origin: Baota host used by portfolio desks.  
Root: `/www/wwwroot/fishgoospreadsheet.net`

## GUARDS

- **Do not** rsync leftover Georgia dest `overlay/index.html` over the ranked homepage — publish only `index.html.platform-patched`.
- **Do not** revive Phase C sunsets; do not invent country spreadsheet domains.
- Patch **ia-collapse.conf** so `/fishgoo-coupons/` is not rewritten to `/coupons/`.
- Retarget **gsc-redirects** `/coupons` · `/coupons/` → `/fishgoo-coupons/` (exact locations are first-match).
- Nginx vhost already `include .../extension/fishgoospreadsheet.net/*.conf` (keep it).

## Files to push

```bash
HUB=/www/wwwroot/fishgoospreadsheet.net
LOCAL=sites/fishgoospreadsheet.net/overlay
BAK=/www/backup/fishgoo-platform-$(date +%Y%m%d-%H%M%S)
EXT=/www/server/panel/vhost/nginx/extension/fishgoospreadsheet.net

mkdir -p "$BAK"
cp -a "$HUB/index.html" "$HUB/sitemap.xml" "$HUB/coupons.html" "$HUB/llms.txt" "$BAK/" 2>/dev/null || true
cp -a "$EXT" "$BAK/extension" 2>/dev/null || true

cp "$LOCAL/index.html.platform-patched" "$HUB/index.html"
mkdir -p "$HUB/fishgoo-coupons" "$HUB/finds-dataset" "$HUB/data"
cp "$LOCAL/fishgoo-coupons/index.html" "$HUB/fishgoo-coupons/index.html"
cp "$LOCAL/finds-dataset/index.html" "$HUB/finds-dataset/index.html"
cp "$LOCAL/data/"*.json "$HUB/data/"
cp "$LOCAL/llms.txt" "$LOCAL/sitemap.xml" "$HUB/"

cp "$LOCAL/_deploy/platform-opt.conf" "$EXT/platform-opt.conf"
cp "$LOCAL/_deploy/ia-collapse.conf" "$EXT/ia-collapse.conf"
# Retarget coupons aliases in gsc-redirects (exact location first-match)
sed -i 's#return 301 https://fishgoospreadsheet.net/coupons.html;#return 301 https://fishgoospreadsheet.net/fishgoo-coupons/;#g' \
  "$EXT/gsc-redirects.conf"

nginx -t && nginx -s reload
```

## GSC

Submit `https://fishgoospreadsheet.net/sitemap.xml` after deploy.

## Verify

- `/` title contains Independent Index · 11,300+
- Hero CTAs Spreadsheet / Coupons / Dataset / Register; `#local` money URLs ≤6
- `/fishgoo-coupons/` has truth callout + 26 Oct 2026 + FAQ-LD
- `/data/*.json` + `/finds-dataset/` + `/llms.txt` → 200
- `/coupons/` · `/coupons.html` → 301 `/fishgoo-coupons/`
