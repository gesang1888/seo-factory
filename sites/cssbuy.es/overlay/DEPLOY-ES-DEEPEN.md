# Deploy: cssbuy.es ES deepen (Correos / AEAT + hub uplink)

Scope: **only** `cssbuy.es` money URLs below. Do **not** write hub `cssbuyspreadsheet.eu`, other desks, or twin wwwroots. No Phase C revive.

## Pages

| Slug | LIVE URL |
|------|----------|
| `cssbuy-shipping` | https://cssbuy.es/cssbuy-shipping/ (`/guide/shipping` → 301) |
| `cssbuy-coupons` | https://cssbuy.es/cssbuy-coupons/ |
| `how-to-use-cssbuy` | https://cssbuy.es/how-to-use-cssbuy/ (first-order) |

Homepage `/` already Correos/AEAT + hub uplink — **leave untouched**.

## Build + deploy

```bash
python3 tools/cssbuy_es_deepen.py \
  --load-env /path/to/internal/usfans-ssh.env \
  --deploy --verify --gsc \
  --gsc-sa /path/to/internal/gsc-sa.json \
  --store-internal /path/to/internal/cssbuy-es-deepen
```

`--build-only` writes `sites/cssbuy.es/overlay/*/index.html.es-deepen` from `live-base.index.html`.

## Backup

Baota path pattern: `/www/backup/cssbuy-es-deepen-YYYYMMDD-HHMMSS/` (`*-index.html.before` + `sitemap.xml.before`).

## Verify

- Three pages HTTP **200**; `id="local"`; Correos + AEAT; hub uplink to `cssbuyspreadsheet.eu` + `finds-dataset`
- Titles / H1 **not** Spreadsheet heroes
- `/` and hub **200** without `data-es-deepen`
- Twins sheet.es/nl/it/fr → desk **301**; .de/.us/.at/.ca/.uk → hub **301**
