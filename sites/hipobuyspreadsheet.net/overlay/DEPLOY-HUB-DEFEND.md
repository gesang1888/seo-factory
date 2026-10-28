# Deploy — HipoBuy hub defend (2026-10-28)

Action 2 from country strategy: **defend** hub Independent Index · 8,600+ + coupons/dataset discovery.  
Surgical CMS chrome only — **never** overwrite ranked homepage with Georgia `index.html`.  
**Do not** deepen NL. **Do not** revive Phase C / twins.

Tag: `hipobuy-hub-defend-20261028` · stamp `2026-10-28`

## 1. Hub (`hipobuyspreadsheet.net`)

```bash
HOST=31.97.41.31
ROOT=/www/wwwroot/hipobuyspreadsheet.net
LOCAL=sites/hipobuyspreadsheet.net/overlay
stamp=$(date +%Y%m%d-%H%M%S)

# Backup
ssh root@$HOST "mkdir -p /www/backup/hipobuy-hub-defend-$stamp && \
  cp -a $ROOT/template/pc/seo.htm $ROOT/template/pc/index.htm \
  $ROOT/sitemap.xml $ROOT/llms.txt $ROOT/data $ROOT/finds-dataset \
  $ROOT/hipobuy-coupons $ROOT/hipobuy-qc-guide $ROOT/is-hipobuy-legit \
  /www/backup/hipobuy-hub-defend-$stamp/ 2>/dev/null; true"

# Surgical CMS chrome
scp "$LOCAL/cms-templates/seo.htm" root@$HOST:$ROOT/template/pc/seo.htm
scp "$LOCAL/cms-templates/index.htm" root@$HOST:$ROOT/template/pc/index.htm

# Moat surfaces
rsync -av "$LOCAL/data/" root@$HOST:$ROOT/data/
rsync -av "$LOCAL/finds-dataset/" root@$HOST:$ROOT/finds-dataset/
rsync -av "$LOCAL/hipobuy-coupons/" root@$HOST:$ROOT/hipobuy-coupons/
scp "$LOCAL/llms.txt" root@$HOST:$ROOT/llms.txt
scp "$LOCAL/sitemap.xml" root@$HOST:$ROOT/sitemap.xml

# Align CMS web_description date → 28 October 2026 via MySQL ey_config, then:
ssh root@$HOST "rm -rf $ROOT/data/runtime/cache/* $ROOT/data/runtime/temp/*; nginx -t && nginx -s reload"
```

`web_description` target:

> Browse 8,600+ HipoBuy spreadsheet finds with QC photos, CNY/USD context and agent buy links. Updated 28 October 2026. Independent Index · Open directory on hipobuyspreadsheet.net — not HipoBuy.com checkout and not a Google Sheet dump. Coupons + dated finds dataset on this hub.

## 2. Out of scope this pass

- `hipobuyspreadsheet.nl` / `.co.uk` — **no deepen**
- Phase C / twin 301s (`.at` / `.eu` / review / `.us` / `spreadsheets.uk`) — **leave**
- External `.com` / hipo-sheets / Reddit Sheet — **do not touch**

## 3. Verify

```bash
curl -sL https://hipobuyspreadsheet.net/ | grep -E 'Independent Index|Open directory|hub-defend|8,600\+|28 October'
curl -sL https://hipobuyspreadsheet.net/hipobuy-coupons/ | grep -E '2026-10-28|hub_defend|Open directory'
curl -sL https://hipobuyspreadsheet.net/finds-dataset/ | grep -E '2026-10-28|8,600\+|Open directory'
curl -sL https://hipobuyspreadsheet.net/data/finds-dataset.json | grep -E 'hub_defend|2026-10-28|8600'
curl -sI https://hipobuy.at/ | head -5
curl -sI https://hipobuyspreadsheets.uk/ | head -5
```
