# 复数域 DNS 配置（kakospreadsheets.*）

在 **Cloudflare**（或注册商 DNS）为以下域添加记录，指向源站 `31.97.41.31`：

| 域名 | 类型 | 名称 | 内容 | 代理 |
|------|------|------|------|------|
| kakospreadsheets.es | A | @ | 31.97.41.31 | 已代理（橙云） |
| kakospreadsheets.fr | A | @ | 31.97.41.31 | 已代理 |
| kakospreadsheets.nl | A | @ | 31.97.41.31 | 已代理 |
| kakospreadsheets.ca | A | @ | 31.97.41.31 | 已代理 |

服务器 nginx 已配置 301：

- `kakospreadsheets.es` → `https://kakospreadsheet.es/kakobuy-spreadsheets/`
- `kakospreadsheets.fr` → `https://kakospreadsheet.fr/kakobuy-spreadsheets/`
- `kakospreadsheets.nl` → `https://kakospreadsheet.nl/kakobuy-spreadsheets/`
- `kakospreadsheets.ca` → `https://kakospreadsheet.ca/kakobuy-spreadsheets/`

DNS 生效后，在服务器重签证书：

```bash
/root/.acme.sh/acme.sh --issue -d kakospreadsheets.es -w /www/wwwroot/kakospreadsheets.es --force
```

或在本地：

```bash
KAKOBUY_SKIP_BAOTA=1 KAKOBUY_SKIP_NGINX=1 python3 scripts/deploy_kakobuy.py
# 仅证书步骤需单独 SSH 执行 issue_certs
```
