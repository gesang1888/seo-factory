# Deploy Step 3 — ootdbuyspreadsheet.net

Thin shipping/customs/language cleanup (2026-10-26).

## Nginx
```bash
mkdir -p /www/server/panel/vhost/nginx/extension/ootdbuyspreadsheet.net
cp sites/ootdbuyspreadsheet.net/overlay/_deploy/thin-page-redirects.conf \
  /www/server/panel/vhost/nginx/extension/ootdbuyspreadsheet.net/thin-page-redirects.conf
nginx -t && nginx -s reload
```

## Docroot stubs
Rsync redirect stubs from `sites/ootdbuyspreadsheet.net/overlay/` (paths listed in `_deploy`). Do **not** overwrite unrelated CMS heroes from Step 2.

## Sitemap
Remove thin URLs listed in actions JSON / this step report. Keep deep `*-shipping-guide/` targets.

## Noindex shells
Paths in `_deploy/noindex-paths.txt`: ensure `<meta name="robots" content="noindex, follow">` and drop from sitemap.
