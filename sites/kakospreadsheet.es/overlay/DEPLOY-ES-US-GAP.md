# Deploy — Kakobuy ES deepen + hub US block (20261029)

Gap plan R1+R2. Tag `kakobuy-es-us-gap-20261029`.

## Guards

- No new domains. No `kakobuys.co.uk`. Twins tips/.fr/.nl stay 301→hub.
- ES keep stays Correos/AEAT/CP5 + hub uplink; **no** consumer LATAM/ops/twin callouts (ops → docs/internal).
- Hub `/shipping-to-us/` is **not** a spreadsheet hero; CTA → `/kakobuy-spreadsheet/` + `/finds-dataset/`.

## Roots

- `/www/wwwroot/kakospreadsheet.es`
- `/www/wwwroot/kakobuydocs.com`

## Publish (surgical)

```bash
python3 tools/kakobuy_es_us_gap.py --load-env /cursor/stores/self/internal/usfans-ssh.env --deploy --verify
```

Or manual cp of `*.es-gap` / `shipping-to-us/index.html` / `index.html.es-us-gap` / sitemaps.
