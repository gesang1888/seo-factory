# DEPLOY Step 4 — lovegobuy.nl

## Ownership
- Brand / global **spreadsheet** queries → `https://lovegobuyguide.com/`
- This country desk → local intent only (carrier, postcode, customs, local coupons/QC)

## Patch
Surgical on ranked Georgia `index.html` (title / H1 / meta / `#local` + hub uplink).
Do **not** wholesale overwrite with a thinner desk template.

## Money URLs (≤6)
- `/`
- `/lovegobuy-shipping/`
- `/is-lovegobuy-legit/`
- `/lovegobuy-spreadsheet/`

## Apply on Baota origin
```bash
# from backup + patched file in this overlay
cp /www/wwwroot/lovegobuy.nl/index.html /www/backup/portfolio-step4-YYYYMMDD/lovegobuy.nl/
cp sites/lovegobuy.nl/overlay/index.html.step4-patched /www/wwwroot/lovegobuy.nl/index.html
```

## Verify
curl -sL https://lovegobuy.nl/ | grep -E '<title>|<h1|id="local"|hub-uplink|data-step4'
