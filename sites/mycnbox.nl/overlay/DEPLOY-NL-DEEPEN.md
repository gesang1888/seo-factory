# DEPLOY — MyCNBox NL deepen (action 1)

## Scope
- Host: **mycnbox.nl** only
- Pages: `/mycnbox-shipping-guide/` · `/is-mycnbox-legit/` · `/mycnbox-spreadsheet/` · `/mycnbox-coupons/`
- **Do not** write hub `mycnbox.eu`, UK/PL, watch es/de/fr, or revive `mycnboxhaul.com`

## Build + deploy
```bash
# fetch LIVE bases into overlay/*/live-base.index.html first if missing
python3 tools/mycnbox_nl_deepen.py --build
python3 tools/mycnbox_nl_deepen.py --load-env /cursor/stores/self/internal/usfans-ssh.env --deploy
python3 tools/mycnbox_nl_deepen.py --verify
```

## Verify
```bash
curl -sL https://mycnbox.nl/mycnbox-shipping-guide/ | grep -E 'Douane|1234 AB|id="local"|data-nl-deepen|mycnbox.eu'
curl -sI https://mycnboxhaul.com/ | head -5   # still 301 → .eu
curl -sL https://mycnbox.eu/ | grep -c data-nl-deepen   # expect 0
```

## Artefacts
- `*/index.html.nl-deepen` — deepened HTML
- `*/live-base.index.html` — pre-change LIVE snapshot
- Baota backup: `/www/backup/mycnbox-nl-deepen-<stamp>/`
