# Deploy — fansbuy.co.uk
```bash
HOST=<fansbuy.co.uk-origin>
ROOT=/www/wwwroot/fansbuy.co.uk
LOCAL=sites/fansbuy.co.uk/overlay
rsync -av "$LOCAL/fansbuy-qc-guide/" root@$HOST:$ROOT/fansbuy-qc-guide/
scp "$LOCAL/llms.txt" "$LOCAL/sitemap.xml" root@$HOST:$ROOT/
# Coupons/legit already live — optional content refresh only
```
