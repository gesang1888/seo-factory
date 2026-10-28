# Deploy — OrientDig hub reclaim (2026-10-28)

Action 1 LIVE: strengthen `/orientdig-spreadsheet/` + coupons/dataset + dual-role ES home for brand `orientdig spreadsheet` SERP.

Origin: Baota. Root: `/www/wwwroot/orientdig.es`

## GUARDS

- Surgical overlay only — **do not** wholesale-replace ranked homepage skin beyond stamped platform-patched file.
- **Keep** Correos / AEAT `#local` dual-role framing on home.
- **Do not** light-fix FR/US this wave.
- **Do not** revive Phase C twins (`.nl` / `.it` → es; spreadsheet.fr → fr; spreadsheet.us → us).
- **Do not** elevate watch AT/DE/UK; do not touch `.net` / JadeShip / Reddit.
- Do not invent row counts above published hub claim (8000 → display 8,000+).

## Push

```bash
HUB=/www/wwwroot/orientdig.es
LOCAL=sites/orientdig.es/overlay
BAK=/www/backup/orientdig-hub-reclaim-$(date +%Y%m%d-%H%M%S)

mkdir -p "$BAK/orientdig-spreadsheet" "$BAK/orientdig-coupons" "$BAK/finds-dataset" \
  "$BAK/como-comprar-en-orientdig" "$BAK/orientdig-shipping-coupons" "$BAK/data"
cp -a "$HUB/index.html" "$HUB/llms.txt" "$HUB/sitemap.xml" "$BAK/" 2>/dev/null || true
cp -a "$HUB/orientdig-spreadsheet/index.html" "$BAK/orientdig-spreadsheet/" 2>/dev/null || true
cp -a "$HUB/orientdig-coupons/index.html" "$BAK/orientdig-coupons/" 2>/dev/null || true
cp -a "$HUB/finds-dataset/index.html" "$BAK/finds-dataset/" 2>/dev/null || true
cp -a "$HUB/como-comprar-en-orientdig/index.html" "$BAK/como-comprar-en-orientdig/" 2>/dev/null || true
cp -a "$HUB/orientdig-shipping-coupons/index.html" "$BAK/orientdig-shipping-coupons/" 2>/dev/null || true
cp -a "$HUB/data/"*.json "$BAK/data/" 2>/dev/null || true

mkdir -p "$HUB/orientdig-spreadsheet" "$HUB/orientdig-coupons" "$HUB/finds-dataset" \
  "$HUB/como-comprar-en-orientdig" "$HUB/orientdig-shipping-coupons" "$HUB/data"
cp "$LOCAL/index.html.platform-patched" "$HUB/index.html"
cp "$LOCAL/orientdig-spreadsheet/index.html" "$HUB/orientdig-spreadsheet/index.html"
cp "$LOCAL/orientdig-coupons/index.html" "$HUB/orientdig-coupons/index.html"
cp "$LOCAL/finds-dataset/index.html" "$HUB/finds-dataset/index.html"
cp "$LOCAL/como-comprar-en-orientdig/index.html" "$HUB/como-comprar-en-orientdig/index.html"
cp "$LOCAL/orientdig-shipping-coupons/index.html" "$HUB/orientdig-shipping-coupons/index.html"
cp "$LOCAL/data/finds-dataset.json" "$LOCAL/data/coupons-truth.json" "$HUB/data/"
cp "$LOCAL/llms.txt" "$LOCAL/sitemap.xml" "$HUB/"
```

## Verify

- `/orientdig-spreadsheet/` title/H1 contain Independent Index · 8,000+; Open directory CTA; reclaim box names .net / JadeShip / Reddit; tag `orientdig-hub-reclaim-20261028`
- `/` still Independent Index · 8,000+ | Correos; Open directory CTA; `#local` Correos/AEAT intact
- `/finds-dataset/` + JSON last_verified=2026-10-28 · row_count=8000 · hub_reclaim=orientdig-hub-reclaim-20261028
- `/orientdig-coupons/` + coupons-truth stamp 2026-10-28
- `/como-comprar-en-orientdig/` + `/orientdig-shipping-coupons/` have hub uplink; still 200
- FR/US untouched; twins .nl/.it still 301→es; spreadsheet.fr→fr; spreadsheet.us→us
