# Deploy — LoveGoBuy platform opt (2026-10-26)

Origin: Baota host used by portfolio desks.  
Roots: `/www/wwwroot/lovegobuyguide.com` (+ keep `lovegobuy.nl` / `lovegobuy.it`)

## GUARDS

- **Do not** rsync a new Georgia skin over the ranked hub homepage wholesale — publish only `index.html.platform-patched`.
- Keep NL/IT: surgical hub-uplink / `#local` only — **do not** 301, **do not** overwrite PostNL / Poste heroes.
- **Do not** revive Phase A/B/C twins (`lovegobuyspreadsheet.eu` / `.ca` / `.es` / `.nl` / `.it`) — already 301.
- Do not invent new country spreadsheet domains.
- Hub must **not** link sunset twins as live desks.

## Files to push

```bash
HUB=/www/wwwroot/lovegobuyguide.com
LOCAL=sites/lovegobuyguide.com/overlay
BAK=/www/backup/lovegobuy-platform-$(date +%Y%m%d-%H%M%S)

mkdir -p "$BAK"
cp -a "$HUB/index.html" "$HUB/lovegobuy-coupon/index.html" "$HUB/llms.txt" "$HUB/coupons.html" "$BAK/" 2>/dev/null || true

cp "$LOCAL/index.html.platform-patched" "$HUB/index.html"
rsync -av "$LOCAL/lovegobuy-coupon/" "$HUB/lovegobuy-coupon/"
rsync -av "$LOCAL/finds-dataset/" "$HUB/finds-dataset/"
mkdir -p "$HUB/data"
cp "$LOCAL/data/coupons-truth.json" "$LOCAL/data/finds-dataset.json" "$HUB/data/"
cp "$LOCAL/llms.txt" "$HUB/"

mkdir -p /www/server/panel/vhost/nginx/extension/lovegobuyguide.com
cp "$LOCAL/_deploy/thin-page-redirects.conf" \
  /www/server/panel/vhost/nginx/extension/lovegobuyguide.com/thin-page-redirects.conf
# ensure site nginx includes extension/*.conf (already true on this host)
nginx -t && nginx -s reload

cp sites/lovegobuy.nl/overlay/index.html.platform-patched /www/wwwroot/lovegobuy.nl/index.html
cp sites/lovegobuy.it/overlay/index.html.platform-patched /www/wwwroot/lovegobuy.it/index.html
```

## GSC

Submit sitemaps for lovegobuyguide.com + lovegobuy.nl + lovegobuy.it after deploy.

## Verify

- `/` title contains Independent Index · 11,300+
- Hero CTAs Coupons / Dataset; `#local` money URLs ≤6; footer no live sunset twin links
- `/lovegobuy-coupon/` has truth callout + 26 Oct 2026
- `/data/*.json` + `/finds-dataset/` + `/llms.txt` → 200
- `/coupons.html` → 301 `/lovegobuy-coupon/`
- NL uplink mentions dataset/coupons; IT has `#local` hub uplink
- .eu/.ca/.es still 301→hub; spreadsheet.nl→.nl ; spreadsheet.it→.it
