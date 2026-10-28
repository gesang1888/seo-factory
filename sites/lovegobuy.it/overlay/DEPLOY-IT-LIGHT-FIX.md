# Deploy — lovegobuy.it keep desk (IT light-fix)

Strategy action 3: remove Spreadsheet H1; keep Poste/CAP title; thicken `#local` + hub uplink.

## Scope

- **Host:** `lovegobuy.it` only (`/www/wwwroot/lovegobuy.it/index.html`)
- **Do not touch:** hub `lovegobuyguide.com`, keep `lovegobuy.nl`
- **Do not revive:** Phase C twins (`.eu/.ca/.es`→hub, `spreadsheet.nl`→`.nl`, `spreadsheet.it`→`.it`)

## Build + deploy

```bash
# LIVE baseline already at overlay/live-base.index.html
python3 tools/lovegobuy_it_light_fix.py          # writes index.html.it-light-fix
python3 tools/lovegobuy_it_light_fix.py --deploy  # Baota backup + PUT
```

SSH: `internal/usfans-ssh.env` (`ORIGIN_SSH_PASS` / `RAW_LINE`). Never print the password.

## Verify

- `https://lovegobuy.it/` → **200**, H1 = `LoveGoBuy per un indirizzo in Italia` (no Spreadsheet)
- `#local` has Poste / CAP / ADM + uplink `lovegobuyguide.com`
- hub + `.nl` mtime unchanged; twins still **301**
