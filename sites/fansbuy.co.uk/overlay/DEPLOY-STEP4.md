# DEPLOY Step 4 — fansbuy.co.uk

## Ownership
- Brand / global **spreadsheet** queries → `https://fansbuysheets.net/`
- This country desk → local intent only (carrier, postcode, customs, local coupons/QC)

## Patch
Surgical on ranked Georgia `index.html` (title / H1 / meta / `#local` + hub uplink).
Do **not** wholesale overwrite with a thinner desk template.

## Money URLs (≤6)
- `/`
- `/fansbuy-shipping-guide/`
- `/fansbuy-coupons/`
- `/fansbuy-qc-guide/`
- `/is-fansbuy-legit/`
- `/fansbuy-spreadsheet/`

## Apply on Baota origin
```bash
# from backup + patched file in this overlay
cp /www/wwwroot/fansbuy.co.uk/index.html /www/backup/portfolio-step4-YYYYMMDD/fansbuy.co.uk/
cp sites/fansbuy.co.uk/overlay/index.html.step4-patched /www/wwwroot/fansbuy.co.uk/index.html
```

## Verify
curl -sL https://fansbuy.co.uk/ | grep -E '<title>|<h1|id="local"|hub-uplink|data-step4'
