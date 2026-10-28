# Deploy — AllChinaBuy hub defend (2026-10-28)

Action 2 LIVE: reinforce hub Independent Index · 11,300+ + Open directory + coupons/dataset discovery.
Tag: `allchinabuy-hub-defend-20261028`

Origin: Baota. Root: `/www/wwwroot/allchina-buy.com`

## GUARDS

- Surgical overlay only — **do not** wholesale-replace ranked homepage beyond `index.html.platform-patched`.
- **Do not** deepen NL (`acbuyspreadsheets.nl`).
- **Do not** rewrite CA / revive twins / Phase C.
- **Do not** touch UK keep this round.
- Do not invent row counts higher than Typesense `found` (11365 → display 11,300+).
- External Reddit Sheets / allchinafinds / acbuy.net / official .com: **do not touch** (copy only).

## Push

```bash
HUB=/www/wwwroot/allchina-buy.com
LOCAL=sites/allchina-buy.com/overlay
BAK=/www/backup/allchinabuy-hub-defend-$(date +%Y%m%d-%H%M%S)

mkdir -p "$BAK/allchinabuy-coupons" "$BAK/finds-dataset" "$BAK/data"
cp -a "$HUB/index.html" "$HUB/llms.txt" "$HUB/sitemap.xml" "$BAK/" 2>/dev/null || true
cp -a "$HUB/allchinabuy-coupons/index.html" "$BAK/allchinabuy-coupons/" 2>/dev/null || true
cp -a "$HUB/finds-dataset/index.html" "$BAK/finds-dataset/" 2>/dev/null || true
cp -a "$HUB/data/"*.json "$BAK/data/" 2>/dev/null || true

cp "$LOCAL/index.html.platform-patched" "$HUB/index.html"
mkdir -p "$HUB/allchinabuy-coupons" "$HUB/finds-dataset" "$HUB/data"
cp "$LOCAL/allchinabuy-coupons/index.html" "$HUB/allchinabuy-coupons/index.html"
cp "$LOCAL/finds-dataset/index.html" "$HUB/finds-dataset/index.html"
cp "$LOCAL/data/finds-dataset.json" "$LOCAL/data/coupons-truth.json" "$HUB/data/"
cp "$LOCAL/llms.txt" "$LOCAL/sitemap.xml" "$HUB/"
```

## Verify

- `/` Independent Index · 11,300+; **Open directory** CTA; `#hub-defend` names Reddit Sheets / allchinafinds / acbuy.net; stamp 2026-10-28
- `/allchinabuy-coupons/` + `/finds-dataset/` + JSON `hub_defend=allchinabuy-hub-defend-20261028` · `last_verified=2026-10-28`
- twins still 301; CA 200 untouched; NL/UK heroes untouched this round
