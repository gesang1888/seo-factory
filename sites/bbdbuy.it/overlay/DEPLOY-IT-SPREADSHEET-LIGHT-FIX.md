# Deploy — BBDBuy IT spreadsheet light-fix (2026-10-29)

## Scope
- **Only** `bbdbuy.it/bbdbuy-spreadsheet/`
- Scrub Spreadsheet catalog hero → IT handoff uplink to `bbdbuyeu.net`
- Keep Poste / ADM / CAP fingerprints on this URL
- **Do not** touch hub, homepage, qc/coupons/shipping deepen pages, CA/UK/US, twins
- **Do not** change mycnbox.nl / cssbuy.es / FashionReps (NL optional skipped — 14d observe)

## Build + LIVE
```bash
python3 tools/bbdbuy_it_spreadsheet_light_fix.py \
  --load-env /cursor/stores/self/internal/usfans-ssh.env \
  --deploy --verify --gsc \
  --gsc-sa /cursor/stores/self/internal/gsc-sa.json \
  --store-internal /cursor/stores/self/internal/gains-desk-light-fix
```

Backup stamp: `/www/backup/bbdbuy-it-spreadsheet-light-fix-*`

## Verify
```bash
curl -sL https://bbdbuy.it/bbdbuy-spreadsheet/ | grep -E '<title>|<h1|id="local"|hub-uplink|Poste Italiane|ADM|data-it-light-fix|bbdbuyeu.net'
# title/H1 must NOT be catalog Spreadsheet hero
curl -sI https://bbdbuyspreadsheet.ca/ | head -3
# untouched
curl -sL https://bbdbuy.it/ | grep -c data-it-light-fix || true
curl -sL https://mycnbox.nl/ | grep -c data-it-light-fix || true
```
