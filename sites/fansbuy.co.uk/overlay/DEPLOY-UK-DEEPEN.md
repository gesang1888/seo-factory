# DEPLOY — FansBuy UK deepen (action 1)

## Scope
- Host: `fansbuy.co.uk` only
- Pages: shipping-guide · spreadsheet (de-hero) · coupons · qc-guide
- Do **not** write hub `fansbuysheets.net`, nl/de watch, or revive twins / Phase C
- Homepage already Step-4 local — leave alone this round

## Build + Baota
```bash
python3 tools/fansbuy_uk_deepen.py \
  --load-env /path/to/internal/usfans-ssh.env \
  --deploy --verify --gsc \
  --gsc-sa /path/to/internal/gsc-sa.json \
  --store-internal /path/to/internal/fansbuy-uk-deepen
```

## Verify
```bash
curl -sL https://fansbuy.co.uk/fansbuy-shipping-guide/ | grep -E 'id="local"|hub-uplink|Royal Mail|HMRC|data-uk-deepen'
curl -sL https://fansbuy.co.uk/fansbuy-spreadsheet/ | grep -E '<title>|<h1|id="local"|hub-uplink'
# twin still 301
curl -sI https://fansbuyspreadsheet.uk/ | head -5
```
