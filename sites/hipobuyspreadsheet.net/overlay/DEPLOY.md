# Deploy — hipobuyspreadsheet.net (ops)

Origin host used by HipoBuy desks tooling: `31.97.41.31` (same fleet as other wwwroots).  
**This Step 2 PR does not SSH-PUT these files** (SSH verified only for usfansspreadsheet.net docroot).

```bash
# From seo-factory repo root, after merge:
HOST=31.97.41.31
ROOT=/www/wwwroot/hipobuyspreadsheet.net
LOCAL=sites/hipobuyspreadsheet.net/overlay

rsync -av "$LOCAL/hipobuy-coupons/" root@$HOST:$ROOT/hipobuy-coupons/
rsync -av "$LOCAL/is-hipobuy-legit/" root@$HOST:$ROOT/is-hipobuy-legit/
rsync -av "$LOCAL/hipobuy-qc-guide/" root@$HOST:$ROOT/hipobuy-qc-guide/
scp "$LOCAL/llms.txt" root@$HOST:$ROOT/llms.txt
scp "$LOCAL/sitemap.xml" root@$HOST:$ROOT/sitemap.xml
# Optional surgical meta on CMS template (backup first):
# cp $ROOT/template/pc/index.htm /www/backup/hipobuy-net-index-$(date +%Y%m%d).htm
# Then edit description + CTA links per HOME-PATCH.md
# Clear EyouCMS runtime cache under $ROOT/data/runtime/
```

GSC: submit `https://hipobuyspreadsheet.net/sitemap.xml` after deploy.

## A-hub QC moat (Step 5.1)

Also see `DEPLOY-MOAT.md`. Deploys `/finds-dataset/`, `/data/*.json`, and refreshes coupons/QC with truth-table stamps.
