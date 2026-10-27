# Deploy — USFans UK deepen (action 3)

Scope: **usfansspreadsheet.co.uk** money URLs only.

```bash
python3 tools/usfans_uk_deepen.py \
  --load-env /cursor/stores/self/internal/usfans-ssh.env \
  --deploy --verify --gsc \
  --store-internal /cursor/stores/self/internal/usfans-uk-deepen \
  --gsc-sa /cursor/stores/self/internal/gsc-sa.json
```

Writes:

- `/usfans-shipping-guide/` — ship-to-UK SERP · Royal Mail · HMRC · `#local` · hub uplink
- `/usfans-refund-guide/` — UK refund · HMRC/Royal Mail · `#local` · hub uplink
- `/usfans-coupons/` — twin `.uk` coupon sink narrative · hub truth uplink
- `/usfans-freight/` — drop Spreadsheet title hero · HMRC/Royal Mail `#local`

Does **not**:

- revive `usfansspreadsheet.uk` (keep 301→`.co.uk`)
- touch hub `usfansspreadsheet.net` or NL desk
- open PL/ES/IT/DE desks

Backup on Baota: `/www/backup/usfans-uk-deepen-<UTC>/`.
