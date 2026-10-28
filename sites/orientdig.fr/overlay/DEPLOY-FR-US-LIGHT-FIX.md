# Deploy — OrientDig FR + US light-fix (2026-10-28)

Strategy action 2: drop Spreadsheet title/H1 → Colissimo / USPS + `#local` hub uplink.

```bash
python3 tools/orientdig_fr_us_light_fix.py          # build from live-base
python3 tools/orientdig_fr_us_light_fix.py --deploy # Baota backup + PUT FR/US only
python3 tools/orientdig_fr_us_light_fix.py --verify
```

Writes only:
- `/www/wwwroot/orientdig.fr/` (index, orientdig-freight, avis-orientdig, sitemap)
- `/www/wwwroot/orientdig.us/` (index, orientdig-freight, sitemap)

Do **not** write hub `orientdig.es`, watch AT/DE/UK, or twin wwwroots.
