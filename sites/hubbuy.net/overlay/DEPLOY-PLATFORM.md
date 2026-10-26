# HubBuy platform deploy

Root: `/www/wwwroot/hubbuy.net`

## LIVE steps (Baota)

```bash
STAMP=$(date +%Y%m%d-%H%M%S)
BAK=/www/backup/hubbuy-platform-$STAMP
HUB=/www/wwwroot/hubbuy.net
LOCAL=sites/hubbuy.net/overlay   # from repo checkout

mkdir -p "$BAK"
cp -a "$HUB/template/pc/index.htm" "$HUB/coupons.html" "$HUB/llms.txt" "$HUB/sitemap.xml" "$BAK/" 2>/dev/null || true
cp -a /www/server/panel/vhost/nginx/extension/hubbuy.net "$BAK/extension" 2>/dev/null || true

# CMS homepage surgical patch (do NOT drop Georgia dest index.html over PHP home)
cp "$LOCAL/cms-templates/index.htm.platform-patched" "$HUB/template/pc/index.htm"

mkdir -p "$HUB/hubbuy-coupons" "$HUB/finds-dataset" "$HUB/hb-data"
cp "$LOCAL/hubbuy-coupons/index.html" "$HUB/hubbuy-coupons/index.html"
cp "$LOCAL/finds-dataset/index.html" "$HUB/finds-dataset/index.html"
cp "$LOCAL/hb-data/"*.json "$HUB/hb-data/"
cp "$LOCAL/llms.txt" "$HUB/llms.txt"
cp "$LOCAL/sitemap.xml" "$HUB/sitemap.xml"
cp "$LOCAL/_deploy/platform-opt.conf" /www/server/panel/vhost/nginx/extension/hubbuy.net/platform-opt.conf

# Optional: align ey_config web_title / web_description (Independent Index · 10,000+)
# Clear EyouCMS runtime cache under $HUB/data/runtime if present

nginx -t && nginx -s reload
```

## Verify

- `/` title contains Independent Index · 10,000+
- `/hubbuy-coupons/` 200; `/coupons.html` 301 → coupons
- `/finds-dataset/` 200; `/data/coupons-truth.json` + `/data/finds-dataset.json` 200 JSON
- `hubbuyspreadsheet.net` still 301 → hub
- Submit sitemap in GSC

## Red lines

- Do **not** rsync leftover Georgia `overlay/index.htm` / wwwroot `index.html` over the ranked CMS homepage
- Do **not** revive twin or invent country spreadsheet TLDs
- Do **not** print SSH / GSC secrets
