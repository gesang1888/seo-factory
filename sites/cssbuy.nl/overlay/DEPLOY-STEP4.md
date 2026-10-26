# DEPLOY Step 4 — cssbuy.nl

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
- `/cssbuy-spreadsheet/`

## Apply on Baota origin
```bash
# from backup + patched file in this overlay
cp /www/wwwroot/cssbuy.nl/index.html /www/backup/portfolio-step4-YYYYMMDD/cssbuy.nl/
cp sites/cssbuy.nl/overlay/index.html.step4-patched /www/wwwroot/cssbuy.nl/index.html
```

## Verify
curl -sL https://cssbuy.nl/ | grep -E '<title>|<h1|id="local"|hub-uplink|data-step4'
