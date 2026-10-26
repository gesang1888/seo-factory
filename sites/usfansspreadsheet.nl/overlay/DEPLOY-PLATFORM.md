# Deploy — USFans NL platform opt

Live NL lacked `#local` / hub uplink. Surgical patch of the ranked Georgia home (do not replace with unused CMS skin overlay wholesale):

```bash
scp sites/usfansspreadsheet.nl/overlay/index.html.platform-patched \
  root@$HOST:/www/wwwroot/usfansspreadsheet.nl/index.html
```

Adds `#local` Douane/NL-postcode block, money URLs ≤6, hub uplink to usfansspreadsheet.net, Coupons/Legit/Lokaal nav.
