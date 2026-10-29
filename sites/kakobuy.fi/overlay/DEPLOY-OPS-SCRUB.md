# Deploy — Kakobuy ops scrub (20261029)

Tag `kakobuy-ops-scrub-20261029`. Strip consumer-visible desk/LATAM/twin/Phase/ops notes. Keep local fingerprints + hub uplink.

```bash
python3 tools/kakobuy_ops_scrub.py \
  --load-env /cursor/stores/self/internal/usfans-ssh.env --deploy --verify
```
