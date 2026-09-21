# usfansspreadsheet.net SEO overlay

Canonical host: **https://usfansspreadsheet.net/**

This overlay implements the ranking-recovery work: collapse the ccTLD cluster, 301 thin brand landings, make the homepage the live spreadsheet, stamp sitemap dates, and drop “Official hub” claims.

## What to upload to `.net`

Copy `overlay/` onto the existing webroot (keep `styles.css`, `/api/`, images, `wd-img/`):

| File | Purpose |
|------|---------|
| `index.html` | Spreadsheet-first homepage with HTML product cards |
| `sitemap.xml` | 44 keep URLs, `lastmod` = build date |
| `robots.txt` | Points at the new sitemap |
| `usfans-seo.css` | Independent-index banner |
| `usfans-*/index.html` | 301 HTML fallbacks for thin URLs |
| patched keep pages | Same paths as today, chrome cleaned |

## 301s that must be HTTP 301 (not only HTML)

1. **Satellite domains** — include `overlay/nginx/usfans-satellite-301.conf` (or the Cloudflare rule in `overlay/cloudflare/satellite-dynamic-rule.txt`):

   `usfansspreadsheet.uk` / `.co.uk` / `.nl` / `.org` (and `www.`) → `https://usfansspreadsheet.net$request_uri`

2. **Thin pages on `.net`** — include `overlay/nginx/usfans-thin-redirects.conf` or import `overlay/cloudflare/thin-redirects.csv`.

Map source: `sites/usfansspreadsheet.net/redirect-map.json`.

## Rebuild

```bash
python3 scripts/build_usfans_overlay.py --check
```

Needs `data/usfans/homepage-products.json`. Keep-page chrome patches read snapshots from `/tmp/usfans-keep` when present.

## Deploy to the Baota VPS

`usfansspreadsheet.net` / `.uk` / `.nl` / `.co.uk` live on `/www/wwwroot`. `.org` is on Hostinger, not this machine.

```bash
export USFANS_DEPLOY_PASS='...'
python3 scripts/deploy_usfans.py
```

The script overlays HTML onto the existing `.net` docroot (keeps `api/`, `styles.css`, images), writes thin-page 301s into the nginx extension include, and points the sibling ccTLD vhosts at `https://usfansspreadsheet.net$request_uri`.
