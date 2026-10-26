# Deploy — W2C / w2clinks platform opt (2026-10-26)

Origin: Baota host used by portfolio desks (`31.97.41.31`).  
Roots: `/www/wwwroot/w2clinks.com` (+ companion `w2crep.org` KEEP — not 301)

## GUARDS

- **Do not** rsync a Georgia desk skin over the ranked EyouCMS homepage.
- Publish homepage only via surgical `template/pc/{seo,index,header}.htm` patches (`*.platform-patched`).
- **Do not** 301 `w2crep.org` / `w2cclothes.com` / `w2cshoes.com` (vertical companions; Phase C watch for rep/shoes).
- **Do not** revive Phase A–C sunsets for other brands.
- CMS runtime lives under `$ROOT/data/` — put public JSON in `$ROOT/w2c-data/` + nginx alias.

## Files to push (hub)

```bash
ROOT=/www/wwwroot/w2clinks.com
LOCAL=sites/w2clinks.com/overlay
BAK=/www/backup/w2c-platform-$(date +%Y%m%d-%H%M%S)

mkdir -p "$BAK"
cp -a "$ROOT/template/pc/index.htm" "$ROOT/template/pc/header.htm" "$ROOT/template/pc/seo.htm" \
  "$ROOT/llms.txt" "$BAK/"

cp "$LOCAL/index.htm.platform-patched" "$ROOT/template/pc/index.htm"
cp "$LOCAL/header.htm.platform-patched" "$ROOT/template/pc/header.htm"
cp "$LOCAL/seo.htm.platform-patched" "$ROOT/template/pc/seo.htm"
rsync -av "$LOCAL/finds-dataset/" "$ROOT/finds-dataset/"
mkdir -p "$ROOT/w2c-data"
cp "$LOCAL/data/coupons-truth.json" "$LOCAL/data/finds-dataset.json" "$ROOT/w2c-data/"
cp "$LOCAL/llms.txt" "$ROOT/"

mkdir -p /www/server/panel/vhost/nginx/extension/w2clinks.com
cp "$LOCAL/_deploy/thin-page-redirects.conf" \
  /www/server/panel/vhost/nginx/extension/w2clinks.com/thin-page-redirects.conf
# ensure site nginx includes extension/*.conf (already true on this host)
nginx -t && nginx -s reload

rm -rf "$ROOT/data/runtime/cache/"* "$ROOT/data/runtime/temp/"* 2>/dev/null || true
```

## Companion w2crep.org (KEEP)

```bash
cp sites/w2crep.org/overlay/index.html.platform-patched /www/wwwroot/w2crep.org/index.html
cp sites/w2crep.org/overlay/llms.txt /www/wwwroot/w2crep.org/llms.txt
```

## GSC

Submit `https://w2clinks.com/sitemap.xml` (and/or sitemap-pages.xml) after deploy. Optional: w2crep.org sitemap.

## Verify

- `/` title contains Independent Index · 11,300+
- Hero CTAs: Directory / Categories / Dataset; `#local` money URLs ≤6
- `/finds-dataset/` + `/data/finds-dataset.json` + `/data/coupons-truth.json` → 200
- `/coupons.html` → 301 `/agents/`
- `w2crep.org/` still 200 (not 301); uplink mentions w2clinks Independent Index
