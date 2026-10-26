# Deploy — BaseTao platform opt (2026-10-26)

Origin: Baota host used by portfolio desks.  
Root: `/www/wwwroot/basetaospreadsheet.com`

## GUARDS

- **Do not** rsync Georgia `overlay/index.html` over the ranked CMS homepage (~48KB).
- Publish homepage only from `index.html.platform-patched` (surgical Independent Index / CTA / `#local`).
- Do **not** revive country spreadsheet TLDs (keep list empty) or `basetaospreadsheet.shop` without cert.
- Keep existing `gsc-redirects.conf` trailing-slash map.

## Files to push

```bash
ROOT=/www/wwwroot/basetaospreadsheet.com
LOCAL=sites/basetaospreadsheet.com/overlay

# backup first
cp -a "$ROOT" "/www/backup/basetao-platform-$(date +%Y%m%d-%H%M%S)"

# homepage surgical
cp "$LOCAL/index.html.platform-patched" "$ROOT/index.html"

# coupons + referral
cp "$LOCAL/basetao-coupon-tracker-2026.html" "$ROOT/basetao-coupon-tracker-2026.html"
rsync -av "$LOCAL/basetao-referral-code/" "$ROOT/basetao-referral-code/"

# trust + moat
rsync -av "$LOCAL/is-basetao-legit/" "$ROOT/is-basetao-legit/"
rsync -av "$LOCAL/basetao-qc-guide/" "$ROOT/basetao-qc-guide/"
rsync -av "$LOCAL/finds-dataset/" "$ROOT/finds-dataset/"
mkdir -p "$ROOT/data"
cp "$LOCAL/data/coupons-truth.json" "$LOCAL/data/finds-dataset.json" "$ROOT/data/"
cp "$LOCAL/llms.txt" "$LOCAL/sitemap.xml" "$ROOT/"
```

## GSC

Submit `https://basetaospreadsheet.com/sitemap.xml` after deploy.

## Verify

- `/` title contains Independent Index · 11,300+
- `/#local` money URLs present
- `/basetao-coupon-tracker-2026.html` has truth callout + FAQ JSON-LD; date 26 Oct 2026
- `/data/coupons-truth.json` + `/data/finds-dataset.json` + `/finds-dataset/` → 200
- `/is-basetao-legit/` + `/basetao-qc-guide/` → 200
- `/llms.txt` mentions 11,300+ + no country desks
