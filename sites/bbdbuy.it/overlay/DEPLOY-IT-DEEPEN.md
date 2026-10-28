# DEPLOY — BBDBuy IT deepen (2026-10-28)

## Scope
- **Only** `bbdbuy.it` money pages: `/bbdbuy-qc/` · `/bbdbuy-coupons/` · `/bbdbuy-shipping/`
- **Do not** touch hub `bbdbuyeu.net`, CA/UK/US desks, or Phase C twins
- Home `/` already Poste/ADM/`#local` — leave alone this round

## Build + LIVE
```bash
python3 tools/bbdbuy_it_deepen.py \
  --load-env /cursor/stores/self/internal/usfans-ssh.env \
  --deploy --verify --gsc \
  --gsc-sa /cursor/stores/self/internal/gsc-sa.json \
  --store-internal /cursor/stores/self/internal/bbdbuy-it-deepen
```

Backup stamp: `/www/backup/bbdbuy-it-deepen-*`

## Verify
```bash
curl -sL https://bbdbuy.it/bbdbuy-qc/ | grep -E 'id="local"|Poste Italiane|data-it-deepen|finds-dataset'
curl -sL https://bbdbuy.it/bbdbuy-coupons/ | grep -E 'id="local"|ADM|bbdbuyeu-coupons|data-it-deepen'
curl -sL https://bbdbuy.it/bbdbuy-shipping/ | grep -E 'id="local"|Poste Italiane|bbdbuyeu.net|Spreadsheet'
# title must NOT contain Spreadsheet
curl -sL https://bbdbuy.it/bbdbuy-shipping/ | grep -o '<title>[^<]*</title>'
# hub / home untouched
curl -sL https://bbdbuy.it/ | grep -c data-it-deepen || true
curl -sL https://bbdbuyeu.net/ | grep -c data-it-deepen || true
# twins still 301
curl -sI https://bbdbuyspreadsheet.ca/ | head -3
```
