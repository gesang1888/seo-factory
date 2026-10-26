# Deploy — w2crep.org companion (KEEP, not 301) — W2C platform opt 2026-10-26

Root: `/www/wwwroot/w2crep.org`

## GUARDS

- **Do not** whole-site 301 to w2clinks.com (vertical companion; Phase C watch).
- Surgical homepage only (`index.html.platform-patched`).
- Do not invent a competing Independent Index count — cite hub 11,300+.

## Push

```bash
cp sites/w2crep.org/overlay/index.html.platform-patched /www/wwwroot/w2crep.org/index.html
cp sites/w2crep.org/overlay/llms.txt /www/wwwroot/w2crep.org/llms.txt
```

## Verify

- `/` still **200** (not 301)
- Title mentions companion + W2C Links · 11,300+
- `#local` links to https://w2clinks.com/finds-dataset/
