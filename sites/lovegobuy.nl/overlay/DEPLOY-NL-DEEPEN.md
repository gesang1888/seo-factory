# Deploy LoveGoBuy NL deepen

```bash
python3 tools/lovegobuy_nl_deepen.py \
  --load-env /path/to/internal/usfans-ssh.env \
  --deploy --verify --gsc \
  --store-internal /path/to/internal/lovegobuy-nl-deepen \
  --gsc-sa /path/to/internal/gsc-sa.json
```

Touches only `lovegobuy.nl` wwwroot money URLs:
- `/lovegobuy-shipping/`
- `/lovegobuy-ervaringen/`
- `/lovegobuy-coupon/`

Does **not** write hub `lovegobuyguide.com` or `lovegobuy.it`. Does **not** revive twins.
