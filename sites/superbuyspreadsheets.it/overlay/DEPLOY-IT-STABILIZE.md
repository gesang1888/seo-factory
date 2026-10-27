# Deploy — superbuyspreadsheets.it IT stabilize (P1)

Baota root:

`/www/wwwroot/superbuyspreadsheets.it`

Copy (after backup):

```bash
cp sites/superbuyspreadsheets.it/overlay/index.html.stabilize-patched /www/wwwroot/superbuyspreadsheets.it/index.html
cp sites/superbuyspreadsheets.it/overlay/is-superbuy-legit/index.html.stabilize-patched /www/wwwroot/superbuyspreadsheets.it/is-superbuy-legit/index.html
cp sites/superbuyspreadsheets.it/overlay/superbuy-recensioni/index.html.stabilize-patched /www/wwwroot/superbuyspreadsheets.it/superbuy-recensioni/index.html
cp sites/superbuyspreadsheets.it/overlay/spedizione-superbuy/index.html.stabilize-patched /www/wwwroot/superbuyspreadsheets.it/spedizione-superbuy/index.html
chown www:www /www/wwwroot/superbuyspreadsheets.it/index.html \
  /www/wwwroot/superbuyspreadsheets.it/is-superbuy-legit/index.html \
  /www/wwwroot/superbuyspreadsheets.it/superbuy-recensioni/index.html \
  /www/wwwroot/superbuyspreadsheets.it/spedizione-superbuy/index.html
```

Backup example: `/www/backup/superbuy-it-stabilize-YYYYMMDD-HHMMSS`

Verify:

```bash
curl -sL https://superbuyspreadsheets.it/ | grep -E 'it_stabilize|Poste Italiane|id="local"|Spreadsheet'
curl -sL https://superbuyspreadsheets.it/is-superbuy-legit/ | grep -E 'affidabile|Poste Italiane|ADM|CAP|id="local"'
curl -sI https://superbuyspreadsheets.us/ | head -n 5   # still 301 → .ca
```

Red lines: do **not** revive `.us`; do **not** create a Superbuy spreadsheet hub; IT-only PUT.
