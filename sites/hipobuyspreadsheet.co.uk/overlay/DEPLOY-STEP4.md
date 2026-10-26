# DEPLOY Step 4 — hipobuyspreadsheet.co.uk

## Ownership
- Brand / global **spreadsheet** queries → `https://hipobuyspreadsheet.net/`
- This country desk → local intent only (carrier, postcode, customs, local coupons/QC)

## Patch
Surgical on ranked Georgia `index.html` (title / H1 / meta / `#local` + hub uplink).
Do **not** wholesale overwrite with a thinner desk template.

## Money URLs (≤6)
- `/`

## Apply on Baota origin
```bash
# from backup + patched file in this overlay
cp /www/wwwroot/hipobuyspreadsheet.co.uk/index.html /www/backup/portfolio-step4-YYYYMMDD/hipobuyspreadsheet.co.uk/
cp sites/hipobuyspreadsheet.co.uk/overlay/index.html.step4-patched /www/wwwroot/hipobuyspreadsheet.co.uk/index.html
```

## Verify
curl -sL https://hipobuyspreadsheet.co.uk/ | grep -E '<title>|<h1|id="local"|hub-uplink|data-step4'
