# Deploy — USFans NL light-fix (strategy action 2)

Remove Spreadsheet title/H1 cannibal on the ranked Georgia homepage. Keep `#local`
Douane / NL-postcode / PostNL and hub uplink to `usfansspreadsheet.net`.

**Do not** wholesale-replace with thin CMS skin `overlay/index.html`.
**Do not** write hub `.net`, UK `.co.uk`, or twin `.uk` (no Phase C revive).

```bash
python3 tools/usfans_nl_light_fix.py          # build → overlay/index.html.nl-light-fix
python3 tools/usfans_nl_light_fix.py --deploy # Baota backup + PUT NL only
```

SSH: `internal/usfans-ssh.env` (`HOST=` + entire `RAW_LINE=` as root password).

Verify:

```bash
curl -sI https://usfansspreadsheet.nl/ | head -1   # 200
curl -s https://usfansspreadsheet.nl/ | rg -o '<title>[^<]+</title>|<h1[^>]*>[^<]+</h1>|data-nl-light-fix|hub-uplink|Douane|1234 AB'
# expect title/H1 without Spreadsheet; marker + Douane + hub uplink
```
