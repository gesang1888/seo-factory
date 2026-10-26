# Deploy Step 5 — kakobuytips.com → kakobuydocs.com

Twin host consolidation (portfolio Step 5 Phase A, 2026-10-26).

## Status
- **LIVE (pre-existing / Step4; documented Step5)** on same Baota origin as usfansspreadsheet.net
- Backup: `/www/backup/portfolio-step5-20261026-141745/kakobuytips.com.conf.bak` (if rewritten this step)
- curl: `https://kakobuytips.com/` and deep path → `301 https://kakobuydocs.com$request_uri`

## Replay
1. Keep existing TLS certs under `/www/server/panel/vhost/cert/kakobuytips.com/`
2. Replace vhost with catch-all redirect (see `_deploy/twin-host-redirect.conf`)
3. `nginx -t && nginx -s reload`
4. Do **not** overwrite Step 2–4 content on **target** `kakobuydocs.com`

## Guard
- No new doorway domains
- Do not reverse USFans `.uk`→`.co.uk` (Step 4)
- Phase B soft-sunset must not target this redirect destination
