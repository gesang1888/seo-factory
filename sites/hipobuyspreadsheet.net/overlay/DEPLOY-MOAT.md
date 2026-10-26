# Deploy — A-hub QC / price freshness moat

Same Baota fleet as USFans (`31.97.41.31`). Do **not** overwrite CMS homepages or Phase A–C redirect stubs.

```bash
HOST=31.97.41.31
ROOT=/www/wwwroot/hipobuyspreadsheet.net
LOCAL=sites/hipobuyspreadsheet.net/overlay

stamp=$(date +%Y%m%d-%H%M%S)
ssh root@$HOST "mkdir -p /www/backup/hipobuyspreadsheet.net-moat-$stamp && \
  cp -a $ROOT/sitemap.xml $ROOT/llms.txt $ROOT/data $ROOT/finds-dataset \
  $ROOT/hipobuy-coupons $ROOT/hipobuy-qc-guide $ROOT/is-hipobuy-legit \
  /www/backup/hipobuyspreadsheet.net-moat-$stamp/ 2>/dev/null; true"

rsync -av "$LOCAL/data/" root@$HOST:$ROOT/data/
rsync -av "$LOCAL/finds-dataset/" root@$HOST:$ROOT/finds-dataset/
rsync -av "$LOCAL/hipobuy-coupons/" root@$HOST:$ROOT/hipobuy-coupons/
rsync -av "$LOCAL/hipobuy-qc-guide/" root@$HOST:$ROOT/hipobuy-qc-guide/
rsync -av "$LOCAL/is-hipobuy-legit/" root@$HOST:$ROOT/is-hipobuy-legit/
scp "$LOCAL/llms.txt" root@$HOST:$ROOT/llms.txt
scp "$LOCAL/sitemap.xml" root@$HOST:$ROOT/sitemap.xml
# llms if present:
# scp "$LOCAL/llms.txt" root@$HOST:$ROOT/llms.txt
```

GSC after deploy: submit `https://hipobuyspreadsheet.net/sitemap.xml`; URL inspection on `/finds-dataset/` + `/data/finds-dataset.json`.
