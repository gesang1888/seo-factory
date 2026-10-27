# Deploy AU deepen (20261027)

```bash
python3 tools/sugargoo_au_deepen.py \
  --load-env /cursor/stores/self/internal/usfans-ssh.env \
  --deploy --verify --gsc \
  --store-internal /cursor/stores/self/internal/sugargoo-au-deepen \
  --gsc-sa /cursor/stores/self/internal/gsc-sa.json
```

Puts only:
- `/www/wwwroot/sugargoospreadsheet.au/index.html`
- `/www/wwwroot/sugargoospreadsheet.au/gst-import-australia/index.html`
- sitemap lastmod bump

Does **not** write twin wwwroots or external sugargoo.ca/.es/.pt/.cheap.
