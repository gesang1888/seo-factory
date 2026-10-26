# Deploy — MyCNBox platform opt (2026-10-26)

Origin: Baota host used by portfolio desks.  
Roots: `/www/wwwroot/mycnbox.eu` (+ keep desks `.nl` / `.co.uk` / `.pl`)

## GUARDS

- **Do not** rsync Georgia `overlay/index.html` over the ranked CMS homepage (~20KB Poppins hub).
- Publish hub homepage only from `index.html.platform-patched` (surgical Independent Index / CTA / `#local` / haul 301 copy).
- Keep desks: surgical uplink only from `index.html.platform-patched` — do **not** overwrite with Georgia skins.
- Do **not** revive `mycnbox.es` / `.de` / `.fr` sunsets; leave haul 301 → `.eu` intact.
- Keep existing Step3 thin shipping/customs redirects; add coupons.html 301 only.

## Files to push

```bash
EU=/www/wwwroot/mycnbox.eu
LOCAL=sites/mycnbox.eu/overlay

cp -a "$EU" "/www/backup/mycnbox-platform-$(date +%Y%m%d-%H%M%S)"

cp "$LOCAL/index.html.platform-patched" "$EU/index.html"
rsync -av "$LOCAL/mycnbox-coupons/" "$EU/mycnbox-coupons/"
rsync -av "$LOCAL/finds-dataset/" "$EU/finds-dataset/"
rsync -av "$LOCAL/is-mycnbox-legit/" "$EU/is-mycnbox-legit/"
mkdir -p "$EU/data"
cp "$LOCAL/data/coupons-truth.json" "$LOCAL/data/finds-dataset.json" "$EU/data/"
cp "$LOCAL/llms.txt" "$LOCAL/sitemap.xml" "$EU/"

# nginx thin redirects (coupons.html → /mycnbox-coupons/)
# merge $LOCAL/_deploy/thin-page-redirects.conf into site nginx include; nginx -t && reload

for H in mycnbox.nl mycnbox.co.uk mycnbox.pl; do
  cp "sites/$H/overlay/index.html.platform-patched" "/www/wwwroot/$H/index.html"
done
```

## GSC

Submit sitemaps for mycnbox.eu + keep desks after deploy.

## Verify

- `/` title contains Independent Index · 11,300+
- `/#local` money URLs present; haul narrative says 301
- `/mycnbox-coupons/` has truth callout + FAQ JSON-LD; date 26 Oct 2026
- `/data/coupons-truth.json` + `/data/finds-dataset.json` + `/finds-dataset/` → 200
- `/coupons.html` → 301 `/mycnbox-coupons/`
- keep desks hub-uplink mentions dataset
- es/de/fr untouched; haul still 301→.eu
