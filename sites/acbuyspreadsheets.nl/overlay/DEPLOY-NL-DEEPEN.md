# DEPLOY — AllChinaBuy / ACBuy NL deepen (action 1)

## Scope
- Host: **acbuyspreadsheets.nl** only
- Pages: `/` · `/acbuy-shipping-guide/` · `/is-acbuy-legit/` · `/acbuy-spreadsheet/` · `/acbuy-coupons/`
- **Do not** write hub `allchina-buy.com`, CA, UK, or revive twin `allchinabuyspreadsheet.nl`
- **No Phase C**

## Build + deploy
```bash
# live-base.index.html already staged under overlay/ (+ per-slug dirs)
python3 tools/acbuy_nl_deepen.py --build
python3 tools/acbuy_nl_deepen.py --load-env /cursor/stores/self/internal/usfans-ssh.env --deploy
python3 tools/acbuy_nl_deepen.py --verify
python3 tools/acbuy_nl_deepen.py --submit-gsc /cursor/stores/self/internal/gsc-sa.json
```

## Verify
```bash
curl -sL https://acbuyspreadsheets.nl/ | grep -E 'Douane|1234 AB|PostNL|data-nl-deepen|allchina-buy.com'
curl -sL https://acbuyspreadsheets.nl/acbuy-shipping-guide/ | grep -E 'Douane|1234 AB|id="local"|PostNL'
curl -sI https://allchinabuyspreadsheet.nl/ | head -5   # still 301 → .nl keep
curl -sL https://allchina-buy.com/ | grep -c data-nl-deepen   # expect 0
```

## Artefacts
- `index.html.nl-deepen` + `*/index.html.nl-deepen` — deepened HTML
- `live-base.index.html` + `*/live-base.index.html` — pre-change LIVE snapshot
- Baota backup: `/www/backup/acbuy-nl-deepen-<stamp>/`
