# Deploy — boonspreadsheet.com

**Do not** rsync `overlay/index.html` (Georgia skin) over the live CMS homepage.

Platform opt (2026-10-26): see **`DEPLOY-PLATFORM.md`** — Independent Index home patch, coupons truth, finds-dataset, llms, sitemap, `/start/` 301.

```bash
HOST=<boon-origin>
ROOT=/www/wwwroot/boonspreadsheet.com
LOCAL=sites/boonspreadsheet.com/overlay
# Homepage: only index.html.platform-patched
rsync -av "$LOCAL/boonbuy-coupons/" root@$HOST:$ROOT/boonbuy-coupons/
rsync -av "$LOCAL/is-boonbuy-legit/" root@$HOST:$ROOT/is-boonbuy-legit/
rsync -av "$LOCAL/boonbuy-qc-guide/" root@$HOST:$ROOT/boonbuy-qc-guide/
scp "$LOCAL/llms.txt" "$LOCAL/sitemap.xml" root@$HOST:$ROOT/
```
