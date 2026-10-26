# Deploy — BoonBuy platform opt (2026-10-26)

Origin: Baota host used by portfolio desks (`31.97.41.31`).  
Root: `/www/wwwroot/boonspreadsheet.com`

## GUARDS

- **Do not** rsync Georgia `overlay/index.html` over the ranked CMS homepage.
- Publish homepage only from `index.html.platform-patched` (surgical Independent Index / CTA / `#local`).
- Do **not** revive any country spreadsheet TLD (none in keep list for BoonBuy).
- Keep existing `gsc-redirects.conf` (spreadsheet inners → `/`, `/coupons/` → `/boonbuy-coupons/`).

## Files to push

```bash
ROOT=/www/wwwroot/boonspreadsheet.com
LOCAL=sites/boonspreadsheet.com/overlay

# backup first
cp -a "$ROOT" "/www/backup/boonbuy-platform-$(date +%Y%m%d-%H%M%S)"

# homepage surgical
cp "$LOCAL/index.html.platform-patched" "$ROOT/index.html"

# citation + moat
rsync -av "$LOCAL/boonbuy-coupons/" "$ROOT/boonbuy-coupons/"
rsync -av "$LOCAL/finds-dataset/" "$ROOT/finds-dataset/"
mkdir -p "$ROOT/data"
cp "$LOCAL/data/coupons-truth.json" "$LOCAL/data/finds-dataset.json" "$ROOT/data/"
cp "$LOCAL/llms.txt" "$LOCAL/sitemap.xml" "$ROOT/"

# thin /start/
cp "$LOCAL/_deploy/thin-page-redirects.conf" \
  /www/server/panel/vhost/nginx/extension/boonspreadsheet.com/thin-page-redirects.conf
nginx -t && nginx -s reload
```

## GSC

Submit `https://boonspreadsheet.com/sitemap.xml` after deploy.

## Verify

- `/` title contains Independent Index · 12,400+
- `/boonbuy-coupons/` has truth callout + FAQ JSON-LD; dates 26 Oct 2026
- `/data/coupons-truth.json` + `/data/finds-dataset.json` + `/finds-dataset/` → 200
- `/llms.txt` → 200
- `/start/` → 301 home; `/shipping/` still → shipping-guide
