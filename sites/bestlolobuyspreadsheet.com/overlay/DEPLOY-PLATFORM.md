# Deploy — LoloBuy platform opt (2026-10-26)

Origin: Baota host used by portfolio desks.  
Root: `/www/wwwroot/bestlolobuyspreadsheet.com`

## GUARDS

- **Do not** rsync leftover Georgia dest `overlay/index.html` over the ranked CMS homepage — publish only `index.html.platform-patched`.
- **Do not** revive Phase A twin `lolospreadsheet.com` (already 301 → hub).
- Do not invent new country spreadsheet domains.
- Hub must **not** link the sunset twin as a live SOP desk.

## Files to push

```bash
HUB=/www/wwwroot/bestlolobuyspreadsheet.com
LOCAL=sites/bestlolobuyspreadsheet.com/overlay
BAK=/www/backup/lolobuy-platform-$(date +%Y%m%d-%H%M%S)

mkdir -p "$BAK"
cp -a "$HUB/index.html" "$HUB/sitemap.xml" "$HUB/llms.txt" "$BAK/" 2>/dev/null || true
cp -a "$HUB/guides/coupons" "$BAK/guides-coupons" 2>/dev/null || true

cp "$LOCAL/index.html.platform-patched" "$HUB/index.html"
mkdir -p "$HUB/guides/coupons"
cp "$LOCAL/guides/coupons/index.html" "$HUB/guides/coupons/index.html"
rsync -av "$LOCAL/finds-dataset/" "$HUB/finds-dataset/"
mkdir -p "$HUB/data"
cp "$LOCAL/data/coupons-truth.json" "$LOCAL/data/finds-dataset.json" "$HUB/data/"
cp "$LOCAL/llms.txt" "$LOCAL/sitemap.xml" "$HUB/"

mkdir -p /www/server/panel/vhost/nginx/extension/bestlolobuyspreadsheet.com
cp "$LOCAL/_deploy/thin-page-redirects.conf" \
  /www/server/panel/vhost/nginx/extension/bestlolobuyspreadsheet.com/thin-page-redirects.conf
nginx -t && nginx -s reload
```

## GSC

Submit `https://bestlolobuyspreadsheet.com/sitemap.xml` after deploy.

## Verify

- `/` title contains Independent Index · 9,200+
- Hero CTAs Spreadsheet / Coupons / Dataset / Register; `#local` money URLs ≤6; no live twin href to lolospreadsheet.com
- `/guides/coupons/` has truth callout + 26 Oct 2026 + FAQ-LD
- `/data/*.json` + `/finds-dataset/` + `/llms.txt` → 200
- `/coupons/` · `/coupons.html` → 301 `/guides/coupons/`
- `lolospreadsheet.com/` still 301 → hub
