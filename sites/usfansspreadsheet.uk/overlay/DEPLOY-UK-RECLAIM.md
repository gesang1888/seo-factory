# usfansspreadsheet.uk — independent GB-collect dest

Lifted 2026-11-03. This host is **not** a 301 onto `.co.uk`.

## Identity (must stay unique vs `.co.uk`)

- Title: `USFans Spreadsheet — GB collect, NI & IM postcodes`
- H1: `USFans for GB collect, Northern Ireland and Crown posts`
- Estimator country: United Kingdom (GB) — not this `.uk` TLD
- Postcodes: BT = NI, IM = Isle of Man, JE/GY = Crown dependencies
- Last mile: Royal Mail collect on mainland GB; NI/IM/JE/GY are other live SKUs
- Hub spreadsheet: https://usfansspreadsheet.net/
- Sibling: https://usfansspreadsheet.co.uk/ stays live. No dest-to-dest 301.

## Replay

```bash
ORIGIN_SSH_PASS=… python3 tools/usfans_uk_reclaim.py all
```

Does: generate overlay, clone dest nginx from the `.co.uk` pattern with `.uk` certs/root, rsync assets/img/media/api (not HTML), PUT overlay, GSC `sitemaps().submit` on `sc-domain:usfansspreadsheet.uk` only.

Unique leftover CMS on disk (coupons, legit, invite, qc-guide, refund, how-to-use, community, shoes) is **not** smashed.
