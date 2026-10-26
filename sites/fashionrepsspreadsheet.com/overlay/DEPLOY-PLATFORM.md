# Deploy — FashionReps platform opt (2026-10-26)

Origin: Baota host used by portfolio desks (`31.97.41.31`).  
Root: `/www/wwwroot/fashionrepsspreadsheet.com`

## GUARDS

- **Do not** rsync a Georgia skin over the ranked EyouCMS homepage.
- Publish homepage only via surgical `template/pc/index.htm` + `header.htm` patches (`*.platform-patched`).
- Leave `fashionrepsfind.com` whole-site 301 → this hub (do not revive).
- Keep `gsc-desk-aliases.conf` (shoes381/bags/… → yupoo-*).
- No country spreadsheet desks in keep list — do not create any.

## Files to push

```bash
ROOT=/www/wwwroot/fashionrepsspreadsheet.com
LOCAL=sites/fashionrepsspreadsheet.com/overlay
BAK=/www/backup/fashionreps-platform-$(date +%Y%m%d-%H%M%S)

mkdir -p "$BAK"
cp -a "$ROOT/template/pc/index.htm" "$ROOT/template/pc/header.htm" \
  "$ROOT/llms.txt" "$ROOT/sitemap.xml" "$BAK/"

# homepage surgical (PHP template — not root index.htm static)
cp "$LOCAL/index.htm.platform-patched" "$ROOT/template/pc/index.htm"
cp "$LOCAL/header.htm.platform-patched" "$ROOT/template/pc/header.htm"

# citation + moat
rsync -av "$LOCAL/fashionreps-coupons/" "$ROOT/fashionreps-coupons/"
rsync -av "$LOCAL/is-fashionreps-legit/" "$ROOT/is-fashionreps-legit/"
rsync -av "$LOCAL/finds-dataset/" "$ROOT/finds-dataset/"
# NOTE: $ROOT/data is EyouCMS runtime — put JSON under a public path that does not collide.
# Prefer $ROOT/public/data or dedicated dirs; this deploy uses $ROOT/fr-data mirrored to /data/ via nginx alias OR copies into $ROOT/data/ only for the two JSON filenames if safe.
mkdir -p "$ROOT/fr-data"
cp "$LOCAL/data/coupons-truth.json" "$LOCAL/data/finds-dataset.json" "$ROOT/fr-data/"
cp "$LOCAL/llms.txt" "$LOCAL/sitemap.xml" "$ROOT/"

# clear EyouCMS runtime cache
rm -rf "$ROOT/data/runtime/cache/"* "$ROOT/data/runtime/temp/"* 2>/dev/null || true
```

MySQL (optional SERP alignment): set `ey_config.web_title` / `web_description` to Independent Index · 10,000+.

Nginx: if `/data/*.json` would collide with CMS `data/`, add:

```nginx
location = /data/finds-dataset.json { alias /www/wwwroot/fashionrepsspreadsheet.com/fr-data/finds-dataset.json; }
location = /data/coupons-truth.json { alias /www/wwwroot/fashionrepsspreadsheet.com/fr-data/coupons-truth.json; }
```

## GSC

Submit `https://fashionrepsspreadsheet.com/sitemap.xml` after deploy.

## Verify

- `/` H1/tag contains Independent Index · 10,000+
- `/fashionreps-coupons/` truth callout + FAQ JSON-LD; date 26 Oct 2026
- `/data/coupons-truth.json` + `/data/finds-dataset.json` + `/finds-dataset/` → 200
- `/llms.txt` has no hubbuy-* 404 cites
- `fashionrepsfind.com/` still 301 → hub
