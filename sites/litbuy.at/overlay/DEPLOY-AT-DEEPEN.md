# Deploy — litbuy.at AT deepen (action 1)

Thicken keep-desk local fingerprints: **Zoll / Post AT Sendungsverfolgung / 1010 Wien**. **Do not** 301. **Do not** revive twins. **Do not** overwrite homepage Wien/BMF hero with spreadsheet. Brand spreadsheet stays on hub `litbuyspreadsheet.eu`.

## Build + LIVE

```bash
python3 tools/litbuy_at_deepen.py \
  --load-env /path/to/usfans-ssh.env \
  --deploy --verify --gsc \
  --gsc-sa /path/to/gsc-sa.json \
  --store-internal /path/to/internal/litbuy-at-deepen
```

Manual copy (if needed):

```bash
STAMP=$(date +%Y%m%d-%H%M%S)
mkdir -p /www/backup/litbuy-at-deepen-$STAMP
cp /www/wwwroot/litbuy.at/zoll-ust-oesterreich/index.html /www/backup/litbuy-at-deepen-$STAMP/
cp /www/wwwroot/litbuy.at/post-at-sendungsverfolgung/index.html /www/backup/litbuy-at-deepen-$STAMP/
cp /www/wwwroot/litbuy.at/litbuy-shipping/index.html /www/backup/litbuy-at-deepen-$STAMP/

cp overlay/zoll-ust-oesterreich/index.html.at-deepen /www/wwwroot/litbuy.at/zoll-ust-oesterreich/index.html
cp overlay/post-at-sendungsverfolgung/index.html.at-deepen /www/wwwroot/litbuy.at/post-at-sendungsverfolgung/index.html
cp overlay/litbuy-shipping/index.html.at-deepen /www/wwwroot/litbuy.at/litbuy-shipping/index.html
```

## Verify

- Titles/H1 keep local framing (Zoll / Post AT / Versand AT) — **no** Spreadsheet hero
- Each page has `#local` + hub uplink → litbuyspreadsheet.eu + coupons + dataset
- Tokens: **BMF** / **Post AT** / **1010 Wien**
- Twins now/es/us/me.uk/nl/fr still **301 → hub**
- Homepage left alone (already Wien/BMF + `#local`)
