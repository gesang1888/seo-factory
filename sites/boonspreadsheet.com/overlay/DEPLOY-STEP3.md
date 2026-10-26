# Deploy Step 3 — boonspreadsheet.com

Thin shipping/customs/language cleanup (2026-10-26).

## Nginx
```bash
mkdir -p /www/server/panel/vhost/nginx/extension/boonspreadsheet.com
cp sites/boonspreadsheet.com/overlay/_deploy/thin-page-redirects.conf \
  /www/server/panel/vhost/nginx/extension/boonspreadsheet.com/thin-page-redirects.conf
nginx -t && nginx -s reload
```

## Docroot stubs
Rsync redirect stubs from `sites/boonspreadsheet.com/overlay/` (paths listed in `_deploy`). Do **not** overwrite unrelated CMS heroes from Step 2.

## Sitemap
Remove thin URLs listed in actions JSON / this step report. Keep deep `*-shipping-guide/` targets.

## Noindex shells
Paths in `_deploy/noindex-paths.txt`: ensure `<meta name="robots" content="noindex, follow">` and drop from sitemap.
