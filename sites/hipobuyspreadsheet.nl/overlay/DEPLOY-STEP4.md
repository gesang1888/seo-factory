# DEPLOY Step 4 — hipobuyspreadsheet.nl

## Ownership
- Brand / global **spreadsheet** queries → `https://hipobuyspreadsheet.net/`
- This country desk → local intent only (carrier, postcode, customs, local coupons/QC)

## Patch
Surgical on ranked Georgia `index.html` (title / H1 / meta / `#local` + hub uplink).
Do **not** wholesale overwrite with a thinner desk template.

## Money URLs (≤6)
- `/`
- `/hipobuy-shipping-guide/`
- `/hipobuy-coupons/`
- `/hipobuy-qc-guide/`
- `/is-hipobuy-legit/`
- `/hipobuy-spreadsheet/`

## Apply on Baota origin
```bash
# from backup + patched file in this overlay
cp /www/wwwroot/hipobuyspreadsheet.nl/index.html /www/backup/portfolio-step4-YYYYMMDD/hipobuyspreadsheet.nl/
cp sites/hipobuyspreadsheet.nl/overlay/index.html.step4-patched /www/wwwroot/hipobuyspreadsheet.nl/index.html
```

## Verify
curl -sL https://hipobuyspreadsheet.nl/ | grep -E '<title>|<h1|id="local"|hub-uplink|data-step4'
