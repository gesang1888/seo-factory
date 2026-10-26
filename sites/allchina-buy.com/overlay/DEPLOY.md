# Deploy — allchina-buy.com
```bash
HOST=<allchina-origin>
ROOT=/www/wwwroot/allchina-buy.com
LOCAL=sites/allchina-buy.com/overlay
rsync -av "$LOCAL/allchinabuy-coupons/" root@$HOST:$ROOT/allchinabuy-coupons/
rsync -av "$LOCAL/allchinabuy-qc-guide/" root@$HOST:$ROOT/allchinabuy-qc-guide/
scp "$LOCAL/llms.txt" "$LOCAL/sitemap.xml" root@$HOST:$ROOT/
# Homepage only if ops confirms overlay matches live chrome:
# scp "$LOCAL/index.html" root@$HOST:$ROOT/index.html
```
