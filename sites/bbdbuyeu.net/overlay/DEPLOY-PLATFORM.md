# DEPLOY — BBDBuy platform opt (2026-10-26)

## Ownership
- **Flagship money:** `bbdbuy.it` — local QC / coupon / Poste / IVA (do **not** force global spreadsheet hub copy)
- **Brand spreadsheet hub:** `bbdbuyeu.net`
- Keep desks: `.ca` / `.uk` / `.us`
- Do **not** revive Phase A–C spreadsheet twins already 301'd

## LIVE targets (Baota)
Backup stamp: `/www/backup/bbdbuy-platform-20261026-*`

### bbdbuy.it
- Deploy `bbdbuy-coupons/`, `bbdbuy-qc/`, `is-bbdbuy-legit/`, `llms.txt`, `sitemap.xml`
- Surgical home: `index.html.platform-patched` (nav Coupon/QC + Italia brand chip) — **do not** wholesale overwrite with desk template `index.html`

### bbdbuy.ca
- `index.html.platform-patched` (money URLs ≤6 + nav)
- `bbdbuy-coupons/`, `bbdbuy-qc/`

### bbdbuy.uk / bbdbuy.us
- `index.html.platform-patched` (`#local` + hub uplink)
- coupons/QC citation pages

### bbdbuyeu.net
- `index.html` (Independent Index SERP + hero CTAs + dataset nav)
- `finds-dataset/`, `data/finds-dataset.json`, `data/coupons-truth.json`

## Verify
```bash
curl -sL https://bbdbuy.it/bbdbuy-coupons/ | grep -E 'Coupon BBDBuy|platform_opt'
curl -sL https://bbdbuy.it/ | grep -E 'id="local"|bbdbuy-coupons|hub-uplink'
curl -sL https://bbdbuy.uk/ | grep -E 'id="local"|Royal Mail|bbdbuyeu.net'
curl -sL https://bbdbuyeu.net/ | grep -E 'Independent Index|finds-dataset'
curl -sL https://bbdbuyeu.net/data/coupons-truth.json | head -c 200
# twins still 301
curl -sI https://bbdbuyeuspreadsheet.com/ | head -5
```
