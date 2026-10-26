# Deploy — A-hub QC / price freshness moat

Same Baota fleet as USFans (`31.97.41.31`). Do **not** overwrite CMS homepages or Phase A–C redirect stubs.

```bash
HOST=31.97.41.31
ROOT=/www/wwwroot/fansbuysheets.net
LOCAL=sites/fansbuysheets.net/overlay

stamp=$(date +%Y%m%d-%H%M%S)
ssh root@$HOST "mkdir -p /www/backup/fansbuysheets.net-moat-$stamp && \
  cp -a $ROOT/sitemap.xml $ROOT/llms.txt $ROOT/data $ROOT/finds-dataset \
  $ROOT/fansbuy-coupons $ROOT/fansbuy-community \
  /www/backup/fansbuysheets.net-moat-$stamp/ 2>/dev/null; true"

rsync -av "$LOCAL/data/" root@$HOST:$ROOT/data/
rsync -av "$LOCAL/finds-dataset/" root@$HOST:$ROOT/finds-dataset/
# Optional: do not overwrite live fansbuy-coupons chrome unless intentionally refreshed
# rsync -av "$LOCAL/fansbuy-community/" root@$HOST:$ROOT/fansbuy-community/

scp "$LOCAL/sitemap.xml" root@$HOST:$ROOT/sitemap.xml
# llms if present:
# scp "$LOCAL/llms.txt" root@$HOST:$ROOT/llms.txt
```

GSC after deploy: submit `https://fansbuysheets.net/sitemap.xml`; URL inspection on `/finds-dataset/` + `/data/finds-dataset.json`.
