# DEPLOY Step 4 — usfansspreadsheet.co.uk

## Ownership
- Brand / global **spreadsheet** queries → `https://usfansspreadsheet.net/`
- This country desk → local intent only (carrier, postcode, customs, local coupons/QC)

## Patch
Surgical on ranked Georgia `index.html` (title / H1 / meta / `#local` + hub uplink).
Do **not** wholesale overwrite with a thinner desk template.

## Money URLs (≤6)
- `/`

## Apply on Baota origin
```bash
# from backup + patched file in this overlay
cp /www/wwwroot/usfansspreadsheet.co.uk/index.html /www/backup/portfolio-step4-YYYYMMDD/usfansspreadsheet.co.uk/
cp sites/usfansspreadsheet.co.uk/overlay/index.html.step4-patched /www/wwwroot/usfansspreadsheet.co.uk/index.html
```

## Verify
curl -sL https://usfansspreadsheet.co.uk/ | grep -E '<title>|<h1|id="local"|hub-uplink|data-step4'
