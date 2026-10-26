# DEPLOY Step 4 — bbdbuy.ca

## Ownership
- Brand / global **spreadsheet** queries → `https://bbdbuyeu.net/`
- This country desk → local intent only (carrier, postcode, customs, local coupons/QC)

## Patch
Surgical on ranked Georgia `index.html` (title / H1 / meta / `#local` + hub uplink).
Do **not** wholesale overwrite with a thinner desk template.

## Money URLs (≤6)
- `/`
- `/bbdbuy-shipping/`

## Apply on Baota origin
```bash
# from backup + patched file in this overlay
cp /www/wwwroot/bbdbuy.ca/index.html /www/backup/portfolio-step4-YYYYMMDD/bbdbuy.ca/
cp sites/bbdbuy.ca/overlay/index.html.step4-patched /www/wwwroot/bbdbuy.ca/index.html
```

## Verify
curl -sL https://bbdbuy.ca/ | grep -E '<title>|<h1|id="local"|hub-uplink|data-step4'
