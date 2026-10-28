# Deploy — MuleBuy FR deepen (action 1)

**Scope:** `mulebuy.fr` only — shipping / livraison / spreadsheet / coupons.  
**Do not:** touch `bestmulebuysheets.com`, revive `.co.uk`/`.es`/`.us`, Phase C, or rewrite homepage (already Colissimo-local).

```bash
# from repo root
python3 tools/mulebuy_fr_deepen.py \
  --load-env /cursor/stores/self/internal/usfans-ssh.env \
  --deploy --verify --gsc \
  --gsc-sa /cursor/stores/self/internal/gsc-sa.json \
  --store-internal /cursor/stores/self/internal/mulebuy-fr-deepen
```

Artifacts per slug: `live-base.index.html` + `index.html.fr-deepen`.  
Backup on Baota: `/www/backup/mulebuy-fr-deepen-<UTC>`.
