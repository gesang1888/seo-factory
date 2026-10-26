# Deploy — boonspreadsheet.com

**Do not** rsync `overlay/index.html` over the live CMS homepage (ranked “BoonBuy Spreadsheet 2026” page).

```bash
HOST=<boon-origin>
ROOT=/www/wwwroot/boonspreadsheet.com
LOCAL=sites/boonspreadsheet.com/overlay
rsync -av "$LOCAL/boonbuy-coupons/" root@$HOST:$ROOT/boonbuy-coupons/
rsync -av "$LOCAL/is-boonbuy-legit/" root@$HOST:$ROOT/is-boonbuy-legit/
rsync -av "$LOCAL/boonbuy-qc-guide/" root@$HOST:$ROOT/boonbuy-qc-guide/
scp "$LOCAL/llms.txt" "$LOCAL/sitemap.xml" root@$HOST:$ROOT/
```
Optional homepage surgical: bump visible “Updated …” date to 26 October 2026 on the CMS home only.
