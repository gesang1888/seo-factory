# Deploy — USFans UK platform opt

```bash
scp sites/usfansspreadsheet.co.uk/overlay/index.html.platform-patched \
  root@$HOST:/www/wwwroot/usfansspreadsheet.co.uk/index.html
```

Fills Money URLs ≤6 (shipping / coupons / legit / spreadsheet / freight) and strengthens hub uplink. Keeps `#local`. Does not reverse `.uk`→`.co.uk`.
