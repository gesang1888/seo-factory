# Deploy — litbuyspreadsheets.ca CA watch light fix (action 3)

Surgical SERP alignment for `does litbuy ship to canada`. Remove Spreadsheet homepage hero. Hub uplink only.

**Watch only** — do **not** promote to keep. Do **not** 301. Do **not** revive twins (now/es/us/uk/nl/fr). Do **not** touch hub `.eu`, keep `litbuy.at`, or watch IT.

## LIVE root

`/www/wwwroot/litbuyspreadsheets.ca`

## Build + publish

```bash
python3 tools/litbuy_ca_light_fix.py
# with ORIGIN_SSH_PASS (or internal/usfans-ssh.env RAW_LINE):
python3 tools/litbuy_ca_light_fix.py --deploy
python3 tools/litbuy_ca_light_fix.py --gsc
```

Files:

- `sites/litbuyspreadsheets.ca/overlay/index.html.ca-light-fix` → `/www/wwwroot/litbuyspreadsheets.ca/index.html`
- `sites/litbuyspreadsheets.ca/overlay/litbuy-shipping-canada/index.html.ca-light-fix` → `/www/wwwroot/litbuyspreadsheets.ca/litbuy-shipping-canada/index.html`

Backup example: `/www/backup/litbuy-ca-light-fix-YYYYMMDD-HHMMSS`

## Verify

```bash
curl -sL https://litbuyspreadsheets.ca/ | grep -E 'ca-light-fix|Does LitBuy ship to Canada|Canada Post|A1A 1A1'
curl -sL https://litbuyspreadsheets.ca/litbuy-shipping-canada/ | grep -E 'ca-light-fix|Does LitBuy ship to Canada|Canada Post'
curl -sI https://litbuyspreadsheetnow.com/ | head -2   # expect 301 → hub
curl -sI https://litbuyspreadsheets.us/ | head -2      # expect 301 → hub
```

Submit `https://litbuyspreadsheets.ca/sitemap.xml` after deploy (CA property only).
