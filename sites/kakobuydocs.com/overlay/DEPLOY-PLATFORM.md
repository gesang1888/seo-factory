# Deploy — Kakobuy platform opt (2026-10-26)

Origin: Baota host used by portfolio desks.  
Roots: `/www/wwwroot/kakobuydocs.com` (+ keep `kakobuy.fi` / `kakospreadsheet.es` / `kakospreadsheet.ca`)

## GUARDS

- **Do not** rsync a new skin over the ranked hub homepage wholesale — publish only `index.html.platform-patched`.
- Keep FI/ES/CA: surgical hub-uplink / `#local` only — **do not** 301, **do not** overwrite Posti / Correos / CBSA heroes.
- **Do not** revive Phase A/B/C twins (`kakobuytips.com` / `kakospreadsheet.fr` / `.nl`) — already 301.
- Do not invent new country spreadsheet domains.
- Hub must **not** link sunset twins as live desks.

## Files to push

```bash
HUB=/www/wwwroot/kakobuydocs.com
LOCAL=sites/kakobuydocs.com/overlay
BAK=/www/backup/kakobuy-platform-$(date +%Y%m%d-%H%M%S)

mkdir -p "$BAK"
cp -a "$HUB/index.html" "$HUB/kakobuy-coupons/index.html" "$HUB/llms.txt" "$HUB/coupons.html" "$BAK/" 2>/dev/null || true

cp "$LOCAL/index.html.platform-patched" "$HUB/index.html"
rsync -av "$LOCAL/kakobuy-coupons/" "$HUB/kakobuy-coupons/"
rsync -av "$LOCAL/finds-dataset/" "$HUB/finds-dataset/"
mkdir -p "$HUB/data"
cp "$LOCAL/data/coupons-truth.json" "$LOCAL/data/finds-dataset.json" "$HUB/data/"
cp "$LOCAL/llms.txt" "$HUB/"

mkdir -p /www/server/panel/vhost/nginx/extension/kakobuydocs.com
cp "$LOCAL/_deploy/thin-page-redirects.conf" \
  /www/server/panel/vhost/nginx/extension/kakobuydocs.com/thin-page-redirects.conf
nginx -t && nginx -s reload

cp sites/kakobuy.fi/overlay/index.html.platform-patched /www/wwwroot/kakobuy.fi/index.html
cp sites/kakospreadsheet.es/overlay/index.html.platform-patched /www/wwwroot/kakospreadsheet.es/index.html
cp sites/kakospreadsheet.ca/overlay/index.html.platform-patched /www/wwwroot/kakospreadsheet.ca/index.html
```

## GSC

Submit sitemaps for kakobuydocs.com + kakobuy.fi + kakospreadsheet.es + kakospreadsheet.ca after deploy.

## Verify

- `/` title contains Independent Index · 11,300+
- Hero CTAs Spreadsheet / Coupons / Dataset; `#local` money URLs ≤6; footer no live sunset twin links
- `/kakobuy-coupons/` has truth callout + 26 Oct 2026
- `/data/*.json` + `/finds-dataset/` + `/llms.txt` → 200
- `/coupons.html` → 301 `/kakobuy-coupons/`
- FI uplink mentions dataset/coupons; ES/CA have `#local` hub uplink
- tips/.fr/.nl still 301→hub
