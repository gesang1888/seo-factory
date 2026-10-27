# Deploy — kakobuy.fi FI deepen (action 2)

Thicken keep-desk local fingerprints. **Do not** 301. **Do not** revive twins. **Do not** overwrite homepage Posti/Tulli hero with spreadsheet. Brand spreadsheet stays on hub.

## Backup then publish

```bash
STAMP=$(date +%Y%m%d-%H%M%S)
mkdir -p /www/backup/kakobuy-fi-deepen-$STAMP
cp /www/wwwroot/kakobuy.fi/kakobuy-kokemuksia/index.html /www/backup/kakobuy-fi-deepen-$STAMP/
cp /www/wwwroot/kakobuy.fi/kakobuy-toimitus/index.html /www/backup/kakobuy-fi-deepen-$STAMP/
cp /www/wwwroot/kakobuy.fi/kakobuy-shipping/index.html /www/backup/kakobuy-fi-deepen-$STAMP/

cp overlay/kakobuy-kokemuksia/index.html.fi-deepen /www/wwwroot/kakobuy.fi/kakobuy-kokemuksia/index.html
cp overlay/kakobuy-toimitus/index.html.fi-deepen /www/wwwroot/kakobuy.fi/kakobuy-toimitus/index.html
cp overlay/kakobuy-shipping/index.html.fi-deepen /www/wwwroot/kakobuy.fi/kakobuy-shipping/index.html
```

## Verify

- Titles/H1 keep local framing (kokemuksia / toimitus / Posti / Tulli)
- Each page has hub uplink → kakobuydocs.com + coupons + dataset
- Twins tips/.fr/.nl still 301 → hub
