# Deploy — Spam-hub SERP recovery LIVE (2026-10-29)

Track 1 LIVE: consolidate year-dated CTR + dataset citation on **allchina-buy.com** hub only.

Tag: `spam-hub-serp-live-20261029` · stamp `2026-10-29`

Origin: Baota. Root: `/www/wwwroot/allchina-buy.com`

## GUARDS

- Surgical overlay only — homepage from `index.html.platform-patched`.
- **Do not** deepen NL / rewrite CA / revive twins / Phase C / thin shells.
- Do not invent row counts above Typesense `found` (11365 → display **11,300+**).
- Coupons stay citation — homepage remains Independent Index hero.

## Push

```bash
HUB=/www/wwwroot/allchina-buy.com
LOCAL=sites/allchina-buy.com/overlay
BAK=/www/backup/allchinabuy-spam-hub-serp-$(date +%Y%m%d-%H%M%S)

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

- `/` Independent Index · 11,300+; stamp **29 October 2026**; FAQ cites `row_count=11365`
- JSON `spam_hub_serp=spam-hub-serp-live-20261029`
- twins still 301; NL/UK/CA untouched this round
