# Deploy — USFans platform end-to-end opt (2026-10-26)

Primary hub for brand spreadsheet SERP: `usfansspreadsheet.net`.  
Country keep: `.co.uk` (canonical UK; `.uk` → `.co.uk` already) + `.nl`.  
Do **not** revive Phase A–C redirected twins. Do **not** overwrite ranked Georgia/country heroes wholesale — surgical patches only.

Auth: `internal/usfans-ssh.env` (HOST + RAW_LINE password). Never print secrets.

## 1. Hub (`usfansspreadsheet.net`)

```bash
HOST=…   # from usfans-ssh.env
ROOT=/www/wwwroot/usfansspreadsheet.net
LOCAL=sites/usfansspreadsheet.net/overlay
stamp=$(date +%Y%m%d-%H%M%S)

ssh root@$HOST "mkdir -p /www/backup/usfans-platform-$stamp && \
  cp -a $ROOT/index.html $ROOT/llms.txt $ROOT/sitemap.xml $ROOT/data \
  $ROOT/finds-dataset $ROOT/usfans-coupons $ROOT/is-usfans-legit \
  /www/backup/usfans-platform-$stamp/ 2>/dev/null; true"

scp "$LOCAL/index.html" root@$HOST:$ROOT/index.html
rsync -av "$LOCAL/data/" root@$HOST:$ROOT/data/
# moat surfaces already LIVE; re-sync if overlay drifted
rsync -av "$LOCAL/finds-dataset/" root@$HOST:$ROOT/finds-dataset/
rsync -av "$LOCAL/usfans-coupons/" root@$HOST:$ROOT/usfans-coupons/
rsync -av "$LOCAL/is-usfans-legit/" root@$HOST:$ROOT/is-usfans-legit/
scp "$LOCAL/llms.txt" root@$HOST:$ROOT/llms.txt
scp "$LOCAL/sitemap.xml" root@$HOST:$ROOT/sitemap.xml
```

`wd-img` nginx already LIVE from images-fix — do not remove. Verify sample `/wd-img/` → 200 `image/webp` + `X-Img-Proxy: usfansspreadsheet`.

## 2. UK desk money URLs

```bash
scp sites/usfansspreadsheet.co.uk/overlay/index.html.platform-patched \
  root@$HOST:/www/wwwroot/usfansspreadsheet.co.uk/index.html
```

## 3. NL desk `#local` + hub uplink

Live NL was still the Georgia twin **without** `#local`. Apply surgical platform-patched home (keeps hero copy):

```bash
scp sites/usfansspreadsheet.nl/overlay/index.html.platform-patched \
  root@$HOST:/www/wwwroot/usfansspreadsheet.nl/index.html
```

## 4. Verify

```bash
curl -sL https://usfansspreadsheet.net/ | grep -E 'Independent Index|usfans-coupons|finds-dataset|alternateName|10,601'
curl -sI "https://usfansspreadsheet.net/wd-img/si.geilicdn.com/test.jpg" | head
curl -sL https://usfansspreadsheet.co.uk/ | grep -E 'usfans-coupons|id="local"|Money URLs'
curl -sL https://usfansspreadsheet.nl/ | grep -E 'id="local"|usfansspreadsheet.net|Money URLs'
curl -sI https://usfansspreadsheet.uk/ | head   # still 301 → .co.uk
```

GSC: resubmit `https://usfansspreadsheet.net/sitemap.xml`; inspect `/`, `/usfans-coupons/`, `/finds-dataset/`.
