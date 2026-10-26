# hipobuyspreadsheet.net homepage surgical notes

**Do not** overwrite EyouCMS `template/pc/index.htm` with a Georgia desk skin.

## Platform opt applied 2026-10-26 (LIVE)

| Item | Before | After |
|------|--------|-------|
| `<title>` / og:title | `Hipobuy Spreadsheet: 8,600+ Finds, Prices & QC Photos` | `HipoBuy Spreadsheet — 8,600+ QC Finds \| Independent Index (2026)` |
| `web_description` (DB) | `Browse 2000+ verified…` | `Browse 8,600+ HipoBuy spreadsheet finds… Independent index…` |
| Hero lead | `Updated August 2026` | `Updated 26 October 2026` + not Sheet / not checkout |
| Hero CTAs | Browse + signup only | + Coupons / QC / Legit / Dataset |
| JSON-LD WebSite | no `dateModified` | `dateModified: 2026-10-26` + alternateName brand variants |
| `/wd-img/` | HTML refs → **404** | nginx proxy (USFans pattern) |

Patched files in overlay: `cms-templates/seo.htm`, `cms-templates/index.htm`. Deploy: `DEPLOY-PLATFORM.md`.

## Gaps observed earlier (closed)

- Meta description still said "2000+" while H1/title said **8,600+** — aligned via `ey_config.web_description` + template.
- No first-screen links to `/hipobuy-coupons/`, `/is-hipobuy-legit/`, `/hipobuy-qc-guide/` — added.
- No `dateModified` in homepage JSON-LD — added.
- Sitemap listed `/shoes381/` (404) — already removed in overlay `sitemap.xml`.
