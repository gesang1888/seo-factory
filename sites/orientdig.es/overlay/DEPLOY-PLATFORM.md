# Deploy — OrientDig platform opt (2026-10-26)

Origin: Baota host used by portfolio desks.  
Roots: `/www/wwwroot/orientdig.es` (+ keep `orientdig.fr` / `orientdig.us`)

## GUARDS

- **Do not** rsync a new skin over the ranked ES homepage wholesale — publish only `index.html.platform-patched`.
- Keep Correos / AEAT local framing on `#local`; brand hub claim coexists (no separate primary hub).
- Keep `orientdig.fr` / `orientdig.us`: surgical hub-uplink only — **do not** 301.
- **Do not** revive Phase B/C twins (`.nl` / `.it` → es; spreadsheet.fr → fr; spreadsheet.us → us).
- Do not invent new country spreadsheet domains; do not soft-sunset watch desks (.at / .de / .uk) this wave.
- Hub must **not** link sunset twins as live desks.

## Files to push

```bash
HUB=/www/wwwroot/orientdig.es
LOCAL=sites/orientdig.es/overlay
BAK=/www/backup/orientdig-platform-$(date +%Y%m%d-%H%M%S)

mkdir -p "$BAK"
cp -a "$HUB/index.html" "$HUB/sitemap.xml" "$HUB/llms.txt" "$HUB/orientdig-coupons" "$BAK/" 2>/dev/null || true

cp "$LOCAL/index.html.platform-patched" "$HUB/index.html"
rsync -av "$LOCAL/orientdig-coupons/" "$HUB/orientdig-coupons/"
rsync -av "$LOCAL/finds-dataset/" "$HUB/finds-dataset/"
mkdir -p "$HUB/data"
cp "$LOCAL/data/coupons-truth.json" "$LOCAL/data/finds-dataset.json" "$HUB/data/"
cp "$LOCAL/llms.txt" "$LOCAL/sitemap.xml" "$HUB/"

mkdir -p /www/server/panel/vhost/nginx/extension/orientdig.es
cp "$LOCAL/_deploy/thin-page-redirects.conf" \
  /www/server/panel/vhost/nginx/extension/orientdig.es/thin-page-redirects.conf
nginx -t && nginx -s reload

cp sites/orientdig.fr/overlay/index.html.platform-patched /www/wwwroot/orientdig.fr/index.html
cp sites/orientdig.us/overlay/index.html.platform-patched /www/wwwroot/orientdig.us/index.html
```

## GSC

Submit sitemaps for orientdig.es (+ FR/US if changed) after deploy.

## Verify

- `/` title contains Independent Index · 8,000+
- Hero CTAs Spreadsheet / Cupones / Dataset / Register; `#local` money URLs ≤6; footer no live sunset twin links
- `/orientdig-coupons/` has truth callout + 26 Oct 2026
- `/data/*.json` + `/finds-dataset/` + `/llms.txt` → 200
- `/coupons.html` → 301 `/orientdig-coupons/`
- FR/US uplink mentions hub + coupons/dataset; local heroes intact
- twins .nl/.it still 301→es; spreadsheet.fr→fr; spreadsheet.us→us
