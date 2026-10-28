# DEPLOY NL deepen — hipobuyspreadsheet.nl

## Scope
- Keep desk only: `hipobuyspreadsheet.nl`
- Pages: `/hipobuy-shipping-guide/` · `/is-hipobuy-legit/` · `/hipobuy-spreadsheet/`
- **Do not** touch hub `hipobuyspreadsheet.net`, UK, or Phase C sunsets

## Build + deploy
```bash
python3 tools/hipobuy_nl_deepen.py \
  --load-env /cursor/stores/self/internal/usfans-ssh.env \
  --deploy --verify --gsc \
  --store-internal /cursor/stores/self/internal/hipobuy-nl-deepen \
  --gsc-sa /cursor/stores/self/internal/gsc-sa.json
```

## Verify
```bash
curl -sL https://hipobuyspreadsheet.nl/hipobuy-shipping-guide/ | grep -E 'data-nl-deepen|id="local"|1234 AB|hub-uplink'
curl -sI https://hipobuy.at/   # expect 301 → hub
```

## Backup
Created on origin under `/www/backup/hipobuy-nl-deepen-YYYYMMDD-HHMMSS/`.
