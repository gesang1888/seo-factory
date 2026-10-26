# Deploy — usfansspreadsheet.net

Verified origin: host from `internal/usfans-ssh.env`, docroot `/www/wwwroot/usfansspreadsheet.net`.

```bash
# backup then rsync overlay heroes (never wipe unrelated CMS assets)
stamp=$(date +%Y%m%d-%H%M%S)
ssh root@$HOST "mkdir -p /www/backup/usfans-step2-$stamp && cp -a /www/wwwroot/usfansspreadsheet.net/index.html /www/wwwroot/usfansspreadsheet.net/llms.txt /www/wwwroot/usfansspreadsheet.net/sitemap.xml /www/wwwroot/usfansspreadsheet.net/usfans-coupons /www/backup/usfans-step2-$stamp/ 2>/dev/null; true"
rsync -av sites/usfansspreadsheet.net/overlay/usfans-coupons/ root@$HOST:/www/wwwroot/usfansspreadsheet.net/usfans-coupons/
scp sites/usfansspreadsheet.net/overlay/index.html \
    sites/usfansspreadsheet.net/overlay/llms.txt \
    sites/usfansspreadsheet.net/overlay/sitemap.xml \
    sites/usfansspreadsheet.net/overlay/sitemap_index.xml \
    root@$HOST:/www/wwwroot/usfansspreadsheet.net/
# keep net-vs-org / shipping-guide / legit in sync if changed
rsync -av sites/usfansspreadsheet.net/overlay/usfansspreadsheet-net-vs-org/ root@$HOST:/www/wwwroot/usfansspreadsheet.net/usfansspreadsheet-net-vs-org/
rsync -av sites/usfansspreadsheet.net/overlay/usfans-shipping-guide/ root@$HOST:/www/wwwroot/usfansspreadsheet.net/usfans-shipping-guide/
rsync -av sites/usfansspreadsheet.net/overlay/is-usfans-legit/ root@$HOST:/www/wwwroot/usfansspreadsheet.net/is-usfans-legit/
```

## A-hub QC moat (Step 5.1)

Also see `DEPLOY-MOAT.md`. Adds `/finds-dataset/` + `/data/*.json`; thickens coupons truth table; optional reddit-community Discord coexistence block. Do not overwrite homepage hero.
