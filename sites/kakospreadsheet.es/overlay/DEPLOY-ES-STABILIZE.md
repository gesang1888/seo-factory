# Deploy — kakospreadsheet.es ES stabilize (action 3)

Surgical SERP alignment for `kakobuy es fiable` / envío / Correos. Hub uplink only. Do **not** 301. Do **not** revive twins. Do **not** touch public `kakobuy.es` spreadsheet shell (not this keep desk).

## LIVE root

`/www/wwwroot/kakospreadsheet.es`

## Publish

```bash
cp sites/kakospreadsheet.es/overlay/index.html.stabilize-patched /www/wwwroot/kakospreadsheet.es/index.html
cp sites/kakospreadsheet.es/overlay/kakobuy-opiniones/index.html.stabilize-patched /www/wwwroot/kakospreadsheet.es/kakobuy-opiniones/index.html
cp sites/kakospreadsheet.es/overlay/es-kakobuy-confiable/index.html.stabilize-patched /www/wwwroot/kakospreadsheet.es/es-kakobuy-confiable/index.html
cp sites/kakospreadsheet.es/overlay/envio-kakobuy-espana/index.html.stabilize-patched /www/wwwroot/kakospreadsheet.es/envio-kakobuy-espana/index.html
chown www:www /www/wwwroot/kakospreadsheet.es/index.html \
  /www/wwwroot/kakospreadsheet.es/kakobuy-opiniones/index.html \
  /www/wwwroot/kakospreadsheet.es/es-kakobuy-confiable/index.html \
  /www/wwwroot/kakospreadsheet.es/envio-kakobuy-espana/index.html
```

Backup example: `/www/backup/kakobuy-es-stabilize-YYYYMMDD-HHMMSS`

## Verify

```bash
curl -sL https://kakospreadsheet.es/kakobuy-opiniones/ | grep -E 'es_stabilize|fiable|Correos|kakobuydocs'
curl -sI https://kakobuytips.com/ | head -2   # expect 301 → hub
```

Submit `https://kakospreadsheet.es/sitemap.xml` after deploy.
