# Deploy — FansBuy platform opt (2026-10-26)

Origin: Baota host used by portfolio desks (`31.97.41.31`).  
Roots: `/www/wwwroot/fansbuysheets.net` · `/www/wwwroot/fansbuy.co.uk`

## GUARDS

- **Do not** rsync Georgia `overlay/index.html` over the ranked CMS homepage.
- Publish hub homepage only from `index.html.platform-patched` (surgical Independent Index / CTA / `#local` / twin sunset copy).
- Keep `fansbuy.co.uk` as A-tier country desk; **do not** revive `fansbuy.eu` / `fansspreadsheet.net` / `fansbuyspreadsheet.eu` / `fansbuyspreadsheet.uk` (already 301).
- Watch `fansbuy.nl` / `fansbuyspreadsheet.de` only — no revive / no new country spreadsheet TLD.
- Keep existing Step 3 thin redirects + gsc-redirects; extend thin with `/coupons.html` → `/fansbuy-coupons/`.

## Files to push

```bash
ROOT=/www/wwwroot/fansbuysheets.net
UK=/www/wwwroot/fansbuy.co.uk
LOCAL=sites/fansbuysheets.net/overlay
UKLOCAL=sites/fansbuy.co.uk/overlay

stamp=$(date +%Y%m%d-%H%M%S)
cp -a "$ROOT" "/www/backup/fansbuy-platform-$stamp"
cp -a "$UK/index.html" "/www/backup/fansbuy-uk-platform-$stamp-index.html"

# hub homepage surgical
cp "$LOCAL/index.html.platform-patched" "$ROOT/index.html"

# citation + moat
rsync -av "$LOCAL/fansbuy-coupons/" "$ROOT/fansbuy-coupons/"
rsync -av "$LOCAL/is-fansbuy-legit/" "$ROOT/is-fansbuy-legit/"
rsync -av "$LOCAL/finds-dataset/" "$ROOT/finds-dataset/"
mkdir -p "$ROOT/data"
cp "$LOCAL/data/coupons-truth.json" "$LOCAL/data/finds-dataset.json" "$ROOT/data/"
cp "$LOCAL/llms.txt" "$LOCAL/sitemap.xml" "$ROOT/"

# UK desk surgical (keep Step4 chrome)
cp "$UKLOCAL/index.html.platform-patched" "$UK/index.html"

# thin: coupons.html alias → money coupons URL
cp "$LOCAL/_deploy/thin-page-redirects.conf" \
  /www/server/panel/vhost/nginx/extension/fansbuysheets.net/thin-page-redirects.conf
nginx -t && nginx -s reload
```

## GSC

Submit `https://fansbuysheets.net/sitemap.xml` (and optionally `https://fansbuy.co.uk/sitemap.xml`) after deploy.

## Verify

- `/` title contains Independent Index · 12,000+
- Hero CTAs: Coupons / Dataset / Shipping; no “.eu stays independent (no 301)”
- `/fansbuy-coupons/` has truth callout + FAQ JSON-LD; dates 26 Oct 2026
- `/data/coupons-truth.json` includes `platform_opt` + FANS26 confirm_live
- `/coupons.html` → 301 `/fansbuy-coupons/`
- Twins still 301 → hub / UK
- `fansbuy.co.uk` hub uplink mentions dataset; money URLs ≤6 local + hub dataset note
