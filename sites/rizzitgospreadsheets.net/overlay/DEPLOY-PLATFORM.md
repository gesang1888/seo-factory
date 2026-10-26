# Deploy — RizzitGo platform opt (2026-10-26)

Origin: Baota host used by portfolio desks.  
Root: `/www/wwwroot/rizzitgospreadsheets.net`

## GUARDS

- **Do not** rsync a new skin over the ranked hub homepage wholesale — publish only `index.html.platform-patched`.
- **No** country spreadsheet desks for this brand — do not invent / deploy country TLDs.
- **Do not** invent 301s involving rizzitgospreadsheet.com / rizzitgo.org (not origin vhosts).
- Keep Step 3 customs → shipping-guide 301.
- Do not print SSH/GSC secrets.

## Files to push

```bash
HUB=/www/wwwroot/rizzitgospreadsheets.net
LOCAL=sites/rizzitgospreadsheets.net/overlay
BAK=/www/backup/rizzitgo-platform-$(date +%Y%m%d-%H%M%S)

mkdir -p "$BAK"
cp -a "$HUB/index.html" "$HUB/sitemap.xml" "$HUB/llms.txt" "$HUB/coupons.html" "$BAK/" 2>/dev/null || true
cp -a "$HUB/rizzitgo-coupons" "$BAK/" 2>/dev/null || true

cp "$LOCAL/index.html.platform-patched" "$HUB/index.html"
rsync -av "$LOCAL/rizzitgo-coupons/" "$HUB/rizzitgo-coupons/"
rsync -av "$LOCAL/finds-dataset/" "$HUB/finds-dataset/"
mkdir -p "$HUB/data"
cp "$LOCAL/data/coupons-truth.json" "$LOCAL/data/finds-dataset.json" "$HUB/data/"
cp "$LOCAL/llms.txt" "$LOCAL/sitemap.xml" "$HUB/"

mkdir -p /www/server/panel/vhost/nginx/extension/rizzitgospreadsheets.net
cp "$LOCAL/_deploy/thin-page-redirects.conf" \
  /www/server/panel/vhost/nginx/extension/rizzitgospreadsheets.net/thin-page-redirects.conf
nginx -t && nginx -s reload
```

## GSC

Submit `https://rizzitgospreadsheets.net/sitemap.xml` after deploy.

## Verify

- `/` title contains Independent Index · 12,400+
- Hero CTAs Spreadsheet / Coupons / Dataset / Register; `#local` money URLs ≤6; hub-only (no country desks)
- `/rizzitgo-coupons/` has truth callout + 26 Oct 2026
- `/data/*.json` + `/finds-dataset/` + `/llms.txt` → 200
- `/coupons.html` → 301 `/rizzitgo-coupons/`
- customs blog still 301 → shipping-guide
