# Deploy — superbuyspreadsheets.ca deepen (P0)

Remove Spreadsheet homepage hero; inject Canada `#local` (Canada Post / CBSA / form A1A 1A1); thicken `/superbuy-shipping/`.

**Do not** revive `.us`. **Do not** create a Superbuy spreadsheet hub. **Do not** PUT IT.

## Publish

```bash
export ORIGIN_SSH_PASS=…   # from internal/usfans-ssh.env RAW_LINE=
python3 tools/superbuy_ca_deepen.py --deploy
```

Manual copy (Baota):

```bash
STAMP=$(date +%Y%m%d-%H%M%S)
mkdir -p /www/backup/superbuy-ca-deepen-$STAMP
cp /www/wwwroot/superbuyspreadsheets.ca/index.html /www/backup/superbuy-ca-deepen-$STAMP/
cp /www/wwwroot/superbuyspreadsheets.ca/superbuy-shipping/index.html /www/backup/superbuy-ca-deepen-$STAMP/
cp overlay/index.html.ca-deepen /www/wwwroot/superbuyspreadsheets.ca/index.html
cp overlay/superbuy-shipping/index.html.ca-deepen /www/wwwroot/superbuyspreadsheets.ca/superbuy-shipping/index.html
```

## Verify

- `/` title/H1: Canada Post / CBSA / A1A 1A1 — **no** “Superbuy Spreadsheet” hero
- `/` and `/superbuy-shipping/` have `id="local"` + Canada Post
- `.us` still **301 → .ca**
- EMS notice URL still 200 (long-tail, not homepage KPI)
