# hipobuy.at — platform opt (sunset under Phase C country cap)

Keep only `hipobuyspreadsheet.nl` + `hipobuyspreadsheet.co.uk`.  
This host whole-site 301 → `https://hipobuyspreadsheet.net$request_uri`.

```bash
HOST=31.97.41.31
stamp=$(date +%Y%m%d-%H%M%S)
ssh root@$HOST "cp /www/server/panel/vhost/nginx/hipobuy.at.conf /www/backup/hipobuy-at-$stamp.conf.bak"
scp overlay/_deploy/platform-host-redirect.conf root@$HOST:/www/server/panel/vhost/nginx/hipobuy.at.conf
ssh root@$HOST "nginx -t && nginx -s reload"
curl -sI https://hipobuy.at/ | head
```

Do not revive content on this TLD.
