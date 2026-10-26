# Deploy — fashionrepsspreadsheet.com

```bash
HOST=<fashionreps-origin>   # ops: fill verified host
ROOT=/www/wwwroot/fashionrepsspreadsheet.com
LOCAL=sites/fashionrepsspreadsheet.com/overlay
rsync -av "$LOCAL/fashionreps-coupons/" root@$HOST:$ROOT/fashionreps-coupons/
rsync -av "$LOCAL/is-fashionreps-legit/" root@$HOST:$ROOT/is-fashionreps-legit/
scp "$LOCAL/llms.txt" "$LOCAL/sitemap.xml" root@$HOST:$ROOT/
# Homepage: backup CMS/index first, then sync index.htm only if live chrome matches overlay
# scp "$LOCAL/index.htm" root@$HOST:$ROOT/index.htm
```
GSC: resubmit sitemap after deploy.
