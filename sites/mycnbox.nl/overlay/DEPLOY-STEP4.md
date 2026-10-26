# DEPLOY Step 4 — mycnbox.nl

## Ownership
- Brand / global **spreadsheet** queries → `https://mycnbox.eu/`
- This country desk → local intent only (carrier, postcode, customs, local coupons/QC)

## Patch
Surgical on ranked Georgia `index.html` (title / H1 / meta / `#local` + hub uplink).
Do **not** wholesale overwrite with a thinner desk template.

## Money URLs (≤6)
- `/`
- `/mycnbox-shipping-guide/`
- `/mycnbox-coupons/`
- `/mycnbox-qc-guide/`
- `/is-mycnbox-legit/`
- `/mycnbox-spreadsheet/`

## Apply on Baota origin
```bash
# from backup + patched file in this overlay
cp /www/wwwroot/mycnbox.nl/index.html /www/backup/portfolio-step4-YYYYMMDD/mycnbox.nl/
cp sites/mycnbox.nl/overlay/index.html.step4-patched /www/wwwroot/mycnbox.nl/index.html
```

## Verify
curl -sL https://mycnbox.nl/ | grep -E '<title>|<h1|id="local"|hub-uplink|data-step4'
