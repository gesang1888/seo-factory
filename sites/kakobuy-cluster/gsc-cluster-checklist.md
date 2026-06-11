# Kakobuy 集群 — Google Search Console 操作清单（2026-06-10）

适用：五站已部署，`sitemap.xml` 线上 200，hreflang 互链，`x-default` → `kakospreadsheet.ca`。

**提交前建议：** Cloudflare 对各域执行 **Purge Everything**（避免 URL 检查读到旧 HTML）。

---

## 一、添加 GSC 资源（5 个「网址前缀」）

登录 [Google Search Console](https://search.google.com/search-console/welcome)，为每个域添加 **网址前缀**：

| # | GSC 资源（网址前缀） |
|---|---------------------|
| 1 | `https://kakospreadsheet.es/` |
| 2 | `https://kakospreadsheet.fr/` |
| 3 | `https://kakospreadsheet.ca/` |
| 4 | `https://kakospreadsheet.nl/` |
| 5 | `https://kakobuy.fi/` |

**验证方式（任选其一）：**

- **DNS TXT**（推荐，Cloudflare 加一条 TXT）
- **HTML 文件**：下载 `google*.html` 上传到 `/www/wwwroot/{domain}/`
- **HTML meta 标签**：写入首页 `<head>`

> 不要添加 `kakospreadsheets.*` 复数域（仅 301 跳转，非内容站）。

---

## 二、提交站点地图（每个资源 1 条）

在对应资源的左侧 **站点地图 → 添加新的站点地图**，粘贴完整 URL：

```
https://kakospreadsheet.es/sitemap.xml
https://kakospreadsheet.fr/sitemap.xml
https://kakospreadsheet.ca/sitemap.xml
https://kakospreadsheet.nl/sitemap.xml
https://kakobuy.fi/sitemap.xml
```

**期望结果：** 状态「成功」；已发现 URL 数约 22–26（与 `dist/{domain}/sitemap.xml` 一致）。

**快捷入口（需已登录 GSC）：**

| 域 | 站点地图页 |
|----|-----------|
| ES | [打开](https://search.google.com/search-console/sitemaps?resource_id=https%3A%2F%2Fkakospreadsheet.es%2F) |
| FR | [打开](https://search.google.com/search-console/sitemaps?resource_id=https%3A%2F%2Fkakospreadsheet.fr%2F) |
| CA | [打开](https://search.google.com/search-console/sitemaps?resource_id=https%3A%2F%2Fkakospreadsheet.ca%2F) |
| NL | [打开](https://search.google.com/search-console/sitemaps?resource_id=https%3A%2F%2Fkakospreadsheet.nl%2F) |
| FI | [打开](https://search.google.com/search-console/sitemaps?resource_id=https%3A%2F%2Fkakobuy.fi%2F) |

---

## 三、网址检查 + 请求编入索引（P1，Day 1–7）

**规则：** 在哪个域名的 GSC 资源里，就只对该域名的 URL 操作。

对每个 URL：**网址检查** → **测试已发布的网址** → **请求编入索引**。

### 3.1 kakospreadsheet.es（7 条）

```
https://kakospreadsheet.es/
https://kakospreadsheet.es/kakobuy-spreadsheet/
https://kakospreadsheet.es/kakobuy-opiniones/
https://kakospreadsheet.es/kakobuy-coupon/
https://kakospreadsheet.es/es-kakobuy-confiable/
https://kakospreadsheet.es/envio-kakobuy-espana/
https://kakospreadsheet.es/kakobuy-qc/
```

### 3.2 kakospreadsheet.fr（7 条）

```
https://kakospreadsheet.fr/
https://kakospreadsheet.fr/kakobuy-spreadsheet/
https://kakospreadsheet.fr/avis-kakobuy/
https://kakospreadsheet.fr/kakobuy-coupon/
https://kakospreadsheet.fr/livraison-kakobuy/
https://kakospreadsheet.fr/kakobuy-france/
https://kakospreadsheet.fr/is-kakobuy-legit/
```

### 3.3 kakospreadsheet.ca（7 条，x-default）

```
https://kakospreadsheet.ca/
https://kakospreadsheet.ca/kakobuy-spreadsheet/
https://kakospreadsheet.ca/kakobuy-coupon/
https://kakospreadsheet.ca/best-kakobuy-spreadsheet/
https://kakospreadsheet.ca/is-kakobuy-legit/
https://kakospreadsheet.ca/kakobuy-shipping-to-canada/
https://kakospreadsheet.ca/kakobuy-canada/
```

### 3.4 kakospreadsheet.nl（7 条）

```
https://kakospreadsheet.nl/
https://kakospreadsheet.nl/best-kakobuy-spreadsheet/
https://kakospreadsheet.nl/kakobuy-spreadsheet/
https://kakospreadsheet.nl/kakobuy-coupon/
https://kakospreadsheet.nl/kakobuy-ervaringen/
https://kakospreadsheet.nl/kakobuy-shipping/
https://kakospreadsheet.nl/kakobuy-verzending/
```

### 3.5 kakobuy.fi（7 条）

```
https://kakobuy.fi/
https://kakobuy.fi/kakobuy-spreadsheet/
https://kakobuy.fi/kakobuy-kokemuksia/
https://kakobuy.fi/kakobuy-toimitus/
https://kakobuy.fi/kakobuy-coupon/
https://kakobuy.fi/kakobuy-suomi/
https://kakobuy.fi/is-kakobuy-legit/
```

**网址检查快捷链接示例（FR 首页）：**  
[检查 kakospreadsheet.fr 首页](https://search.google.com/search-console/inspect?resource_id=https%3A%2F%2Fkakospreadsheet.fr%2F&url=https%3A%2F%2Fkakospreadsheet.fr%2F)

---

## 四、国际化验收（每个首页检查一次）

在 **对应资源** 的网址检查中确认：

| 资源 | 检查 URL | 期望 |
|------|----------|------|
| .es | `https://kakospreadsheet.es/` | `lang` 西语；hreflang 5 链 + x-default→.ca |
| .fr | `https://kakospreadsheet.fr/` | `lang=fr-FR`；hreflang 完整 |
| .ca | `https://kakospreadsheet.ca/` | `lang=en-CA`；x-default 指向自身 |
| .nl | `https://kakospreadsheet.nl/` | `lang=nl-NL` |
| .fi | `https://kakobuy.fi/` | `lang=fi-FI` |

---

## 五、2–4 周后盯的报告

| 报告 | 看什么 |
|------|--------|
| **页面 → 已编入索引** | 五站首页 + spreadsheet 专页是否入库 |
| **站点地图** | 已处理 URL ≈ sitemap 条数 |
| **效果** | `kakobuy spreadsheet`、各国 coupon/avis/opiniones 词 |
| **链接** | 外链是否指向 W2CLinks / 邀请链，而非旧 orientdig 域 |

---

## 六、API 自动提交（可选）

若已配置 Google OAuth / 服务账号，可运行：

```bash
cd ~/Projects/seo-factory
# 需先放置 credentials：data/gsc/oauth_client.json + 首次授权生成 token.json
python3 scripts/submit_gsc_kakobuy.py --sitemaps
python3 scripts/submit_gsc_kakobuy.py --inspect-p1   # 仅检查可达性，不代替「请求编入索引」
```

配置源：`sites/kakobuy-cluster/cluster-config.json` → `gsc_sitemaps` / `gsc_p1_urls`。
