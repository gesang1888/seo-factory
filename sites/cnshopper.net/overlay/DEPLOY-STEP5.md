# Deploy Step 5 — cnshopper.net → cnshopperspreadsheet.net

Twin host consolidation (portfolio Step 5 Phase A, 2026-10-26).

## Status
- **LIVE (Step5 new)** on same Baota origin as usfansspreadsheet.net
- Backup: `/www/backup/portfolio-step5-20261026-141745/cnshopper.net.conf.bak` (if rewritten this step)
- curl: `https://cnshopper.net/` and deep path → `301 https://cnshopperspreadsheet.net$request_uri`

## Replay
1. Keep existing TLS certs under `/www/server/panel/vhost/cert/cnshopper.net/`
2. Replace vhost with catch-all redirect (see `_deploy/twin-host-redirect.conf`)
3. `nginx -t && nginx -s reload`
4. Do **not** overwrite Step 2–4 content on **target** `cnshopperspreadsheet.net`

## Guard
- No new doorway domains
- Do not reverse USFans `.uk`→`.co.uk` (Step 4)
- Phase B soft-sunset must not target this redirect destination
