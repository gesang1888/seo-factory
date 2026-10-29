# Deploy — strip LATAM/ops disclaimer from ES consumer pages (20261029)

Tag `kakobuy-es-disclaimer-rm-20261029`. Keeps Correos/AEAT/CP5 + hub uplink. Removes `latam-note` / twin LATAM ops copy only.

```bash
python3 tools/kakobuy_es_disclaimer_remove.py \
  --load-env /cursor/stores/self/internal/usfans-ssh.env --deploy --verify
```
