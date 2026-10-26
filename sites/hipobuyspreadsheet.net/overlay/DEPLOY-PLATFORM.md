# Deploy — HipoBuy platform end-to-end opt (2026-10-26)

Primary hub only for brand spreadsheet SERP. Keep country desks: `.nl` + `.co.uk`.  
Do **not** overwrite ranked CMS homepage with Georgia `index.html`. Apply surgical CMS templates + nginx.

## 1. Hub (`hipobuyspreadsheet.net`)

```bash
HOST=31.97.41.31
ROOT=/www/wwwroot/hipobuyspreadsheet.net
LOCAL=sites/hipobuyspreadsheet.net/overlay
stamp=$(date +%Y%m%d-%H%M%S)

ssh root@$HOST "mkdir -p /www/backup/hipobuy-platform-$stamp && \
  cp -a $ROOT/template/pc/seo.htm $ROOT/template/pc/index.htm \
  $ROOT/sitemap.xml $ROOT/llms.txt $ROOT/data $ROOT/finds-dataset \
  $ROOT/hipobuy-coupons $ROOT/hipobuy-qc-guide $ROOT/is-hipobuy-legit \
  /www/backup/hipobuy-platform-$stamp/ 2>/dev/null; true"

# Surgical CMS chrome (title / H1 lead / hero CTAs) — never full Georgia overwrite
scp "$LOCAL/cms-templates/seo.htm" root@$HOST:$ROOT/template/pc/seo.htm
scp "$LOCAL/cms-templates/index.htm" root@$HOST:$ROOT/template/pc/index.htm

# Moat surfaces (extend, don't break)
rsync -av "$LOCAL/data/" root@$HOST:$ROOT/data/
rsync -av "$LOCAL/finds-dataset/" root@$HOST:$ROOT/finds-dataset/
rsync -av "$LOCAL/hipobuy-coupons/" root@$HOST:$ROOT/hipobuy-coupons/
rsync -av "$LOCAL/hipobuy-qc-guide/" root@$HOST:$ROOT/hipobuy-qc-guide/
rsync -av "$LOCAL/is-hipobuy-legit/" root@$HOST:$ROOT/is-hipobuy-legit/
scp "$LOCAL/llms.txt" root@$HOST:$ROOT/llms.txt
scp "$LOCAL/sitemap.xml" root@$HOST:$ROOT/sitemap.xml

# Weidian img proxy (same pattern as USFans)
scp "$LOCAL/_deploy/wd-img.conf" root@$HOST:/www/server/panel/vhost/nginx/extension/hipobuyspreadsheet.net/wd-img.conf
scp "$LOCAL/_deploy/wd-img-html.conf" root@$HOST:/www/server/panel/vhost/nginx/extension/hipobuyspreadsheet.net/wd-img-html.conf

# Align CMS web_description (2000+ → 8,600+) via MySQL ey_config, then:
ssh root@$HOST "rm -rf $ROOT/data/runtime/cache/* $ROOT/data/runtime/temp/*; nginx -t && nginx -s reload"
```

`web_description` target value:

> Browse 8,600+ HipoBuy spreadsheet finds with QC photos, CNY/USD context and agent buy links. Updated 26 October 2026. Independent index on hipobuyspreadsheet.net — not HipoBuy.com checkout and not a Google Sheet dump.

## 2. UK desk money URLs

```bash
scp sites/hipobuyspreadsheet.co.uk/overlay/index.html.platform-patched \
  root@$HOST:/www/wwwroot/hipobuyspreadsheet.co.uk/index.html
```

## 3. Cap leftover country twin (`hipobuy.at` → hub)

Phase C kept only `.nl` + `.co.uk`. Apply whole-host 301 (backup first):

```bash
ssh root@$HOST "cp /www/server/panel/vhost/nginx/hipobuy.at.conf \
  /www/backup/hipobuy-platform-$stamp/hipobuy.at.conf.bak"
scp sites/hipobuy.at/overlay/_deploy/platform-host-redirect.conf \
  root@$HOST:/www/server/panel/vhost/nginx/hipobuy.at.conf
ssh root@$HOST "nginx -t && nginx -s reload"
```

## 4. Verify

```bash
curl -sL https://hipobuyspreadsheet.net/ | grep -E 'Independent Index|8,600\+|hipobuy-coupons|dateModified|26 October'
curl -sI "https://hipobuyspreadsheet.net/wd-img/si.geilicdn.com/test.jpg" | head
curl -sI https://hipobuy.at/ | head
curl -sL https://hipobuyspreadsheet.co.uk/ | grep -E 'hipobuy-coupons|id="local"'
```

GSC: resubmit `https://hipobuyspreadsheet.net/sitemap.xml`; URL inspection on `/`, `/hipobuy-coupons/`, `/finds-dataset/`.
