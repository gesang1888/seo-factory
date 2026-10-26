# Deploy — CSSBuy platform opt (2026-10-26)

Origin: Baota host used by portfolio desks.  
Roots: `/www/wwwroot/cssbuyspreadsheet.eu` (+ keep desks `cssbuy.es` / `.nl` / `.it` / `.fr`)

## GUARDS

- **Do not** rsync Georgia `overlay/index.html` over the ranked CMS homepage (~21KB Barlow hub).
- Publish hub homepage only from `index.html.platform-patched`.
- Keep desks: surgical uplink / local KPI only from `index.html.platform-patched` — do **not** overwrite with thinner skins.
- Do **not** revive `cssbuyspreadsheets.de` / `.us` sunsets; leave spreadsheet.* twins 301 → cssbuy.* intact.
- Add coupons.html 301 only via extension thin-page-redirects.conf.

## Files to push

```bash
EU=/www/wwwroot/cssbuyspreadsheet.eu
LOCAL=sites/cssbuyspreadsheet.eu/overlay

cp -a "$EU" "/www/backup/cssbuy-platform-$(date +%Y%m%d-%H%M%S)"

cp "$LOCAL/index.html.platform-patched" "$EU/index.html"
rsync -av "$LOCAL/cssbuy-coupons/" "$EU/cssbuy-coupons/"
rsync -av "$LOCAL/finds-dataset/" "$EU/finds-dataset/"
rsync -av "$LOCAL/is-cssbuy-legit/" "$EU/is-cssbuy-legit/"
mkdir -p "$EU/data"
cp "$LOCAL/data/coupons-truth.json" "$LOCAL/data/finds-dataset.json" "$EU/data/"
cp "$LOCAL/llms.txt" "$LOCAL/sitemap.xml" "$EU/"

# nginx: copy thin-page-redirects.conf into extension/cssbuyspreadsheet.eu/; nginx -t && reload

for H in cssbuy.es cssbuy.nl cssbuy.it cssbuy.fr; do
  cp "sites/$H/overlay/index.html.platform-patched" "/www/wwwroot/$H/index.html"
done
```

## Verify

- `/` title contains Independent Index · 11,300+
- `/#local` money URLs present; twin/.de/.us narrative says 301
- `/cssbuy-coupons/` has truth callout + FAQ JSON-LD; date 26 Oct 2026
- `/data/*.json` + `/finds-dataset/` → 200
- `/coupons.html` → 301 `/cssbuy-coupons/`
- keep desks hub-uplink mentions dataset
- .de/.us still 301→.eu; spreadsheet twins still 301→cssbuy.*
