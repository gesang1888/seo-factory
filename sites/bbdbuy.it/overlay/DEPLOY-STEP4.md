# DEPLOY Step 4 — bbdbuy.it

## Ownership
- Brand / global **spreadsheet** queries → `https://bbdbuyeu.net/`
- This country desk → local intent only (carrier, postcode, customs, local coupons/QC)

## Patch
Surgical on ranked Georgia `index.html` (title / H1 / meta / `#local` + hub uplink).
Do **not** wholesale overwrite with a thinner desk template.

## Money URLs (≤6)
- `/`
- `/bbdbuy-shipping/`
- `/bbdbuy-coupons/`
- `/bbdbuy-qc/`
- `/is-bbdbuy-legit/`
- `/bbdbuy-spreadsheet/`

## Apply on Baota origin
```bash
# from backup + patched file in this overlay
cp /www/wwwroot/bbdbuy.it/index.html /www/backup/portfolio-step4-YYYYMMDD/bbdbuy.it/
cp sites/bbdbuy.it/overlay/index.html.step4-patched /www/wwwroot/bbdbuy.it/index.html
```

## Verify
curl -sL https://bbdbuy.it/ | grep -E '<title>|<h1|id="local"|hub-uplink|data-step4'
