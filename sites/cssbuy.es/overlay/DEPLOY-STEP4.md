# DEPLOY Step 4 — cssbuy.es

## Ownership
- Brand / global **spreadsheet** queries → `https://cssbuyspreadsheet.eu/`
- This country desk → local intent only (carrier, postcode, customs, local coupons/QC)

## Patch
Surgical on ranked Georgia `index.html` (title / H1 / meta / `#local` + hub uplink).
Do **not** wholesale overwrite with a thinner desk template.

## Money URLs (≤6)
- `/`
- `/cssbuy-shipping/`
- `/cssbuy-coupons/`
- `/is-cssbuy-legit/`
- `/cssbuy-spreadsheet/`

## Apply on Baota origin
```bash
# from backup + patched file in this overlay
cp /www/wwwroot/cssbuy.es/index.html /www/backup/portfolio-step4-YYYYMMDD/cssbuy.es/
cp sites/cssbuy.es/overlay/index.html.step4-patched /www/wwwroot/cssbuy.es/index.html
```

## Verify
curl -sL https://cssbuy.es/ | grep -E '<title>|<h1|id="local"|hub-uplink|data-step4'
