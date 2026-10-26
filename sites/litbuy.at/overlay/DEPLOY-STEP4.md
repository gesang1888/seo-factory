# DEPLOY Step 4 — litbuy.at

## Ownership
- Brand / global **spreadsheet** queries → `https://litbuyspreadsheetnow.com/`
- This country desk → local intent only (carrier, postcode, customs, local coupons/QC)

## Patch
Surgical on ranked Georgia `index.html` (title / H1 / meta / `#local` + hub uplink).
Do **not** wholesale overwrite with a thinner desk template.

## Money URLs (≤6)
- `/`
- `/litbuy-shipping/`

## Apply on Baota origin
```bash
# from backup + patched file in this overlay
cp /www/wwwroot/litbuy.at/index.html /www/backup/portfolio-step4-YYYYMMDD/litbuy.at/
cp sites/litbuy.at/overlay/index.html.step4-patched /www/wwwroot/litbuy.at/index.html
```

## Verify
curl -sL https://litbuy.at/ | grep -E '<title>|<h1|id="local"|hub-uplink|data-step4'
