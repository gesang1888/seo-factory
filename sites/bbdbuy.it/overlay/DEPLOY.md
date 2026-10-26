# Deploy — bbdbuy.it
Do **not** overwrite ranked homepage with overlay/index.html.
```bash
HOST=<bbdbuy-it-origin>
ROOT=/www/wwwroot/bbdbuy.it
LOCAL=sites/bbdbuy.it/overlay
rsync -av "$LOCAL/bbdbuy-coupons/" root@$HOST:$ROOT/bbdbuy-coupons/
rsync -av "$LOCAL/bbdbuy-qc/" root@$HOST:$ROOT/bbdbuy-qc/
rsync -av "$LOCAL/is-bbdbuy-legit/" root@$HOST:$ROOT/is-bbdbuy-legit/
scp "$LOCAL/llms.txt" "$LOCAL/sitemap.xml" root@$HOST:$ROOT/
```
