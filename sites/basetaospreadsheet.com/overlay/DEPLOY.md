# Deploy — basetaospreadsheet.com
Do not overwrite CMS homepage with overlay/index.html.
```bash
HOST=<basetao-origin>
ROOT=/www/wwwroot/basetaospreadsheet.com
LOCAL=sites/basetaospreadsheet.com/overlay
rsync -av "$LOCAL/is-basetao-legit/" root@$HOST:$ROOT/is-basetao-legit/
rsync -av "$LOCAL/basetao-qc-guide/" root@$HOST:$ROOT/basetao-qc-guide/
scp "$LOCAL/llms.txt" "$LOCAL/sitemap.xml" root@$HOST:$ROOT/
# Optional: bump lastmod / “Updated” on basetao-coupon-tracker-2026.html to 2026-10-26
```
