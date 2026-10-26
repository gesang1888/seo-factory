# DEPLOY Step 4 — kakobuy.fi

## Ownership
- Brand / global **spreadsheet** queries → `https://kakobuydocs.com/`
- This country desk → local intent only (carrier, postcode, customs, local coupons/QC)

## Patch
Surgical on ranked Georgia `index.html` (title / H1 / meta / `#local` + hub uplink).
Do **not** wholesale overwrite with a thinner desk template.

## Money URLs (≤6)
- `/`
- `/kakobuy-shipping/`

## Apply on Baota origin
```bash
# from backup + patched file in this overlay
cp /www/wwwroot/kakobuy.fi/index.html /www/backup/portfolio-step4-YYYYMMDD/kakobuy.fi/
cp sites/kakobuy.fi/overlay/index.html.step4-patched /www/wwwroot/kakobuy.fi/index.html
```

## Verify
curl -sL https://kakobuy.fi/ | grep -E '<title>|<h1|id="local"|hub-uplink|data-step4'
