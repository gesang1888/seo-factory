# DEPLOY Step 4 — orientdig.es

## Ownership
- Brand / global **spreadsheet** queries → `https://orientdig.es/`
- This country desk → local intent only (carrier, postcode, customs, local coupons/QC)

## Patch
Surgical on ranked Georgia `index.html` (title / H1 / meta / `#local` + hub uplink).
Do **not** wholesale overwrite with a thinner desk template.

## Money URLs (≤6)
- `/`
- `/orientdig-shipping/`

## Apply on Baota origin
```bash
# from backup + patched file in this overlay
cp /www/wwwroot/orientdig.es/index.html /www/backup/portfolio-step4-YYYYMMDD/orientdig.es/
cp sites/orientdig.es/overlay/index.html.step4-patched /www/wwwroot/orientdig.es/index.html
```

## Verify
curl -sL https://orientdig.es/ | grep -E '<title>|<h1|id="local"|hub-uplink|data-step4'
