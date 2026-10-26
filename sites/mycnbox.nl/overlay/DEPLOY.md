# Deploy — mycnbox.nl
```bash
HOST=<mycnbox.nl-origin>
ROOT=/www/wwwroot/mycnbox.nl
LOCAL=sites/mycnbox.nl/overlay
rsync -av "$LOCAL/mycnbox-qc-guide/" root@$HOST:$ROOT/mycnbox-qc-guide/
scp "$LOCAL/llms.txt" "$LOCAL/sitemap.xml" root@$HOST:$ROOT/
# Coupons/legit already live — optional content refresh only
```
