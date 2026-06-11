# Google Search Console — Kakobuy 集群

> **完整操作清单（站点地图 + 网址检查 P1 列表）：** 见 [`gsc-cluster-checklist.md`](./gsc-cluster-checklist.md)

## 一、添加资源（5 个独立属性）

每个域名在 GSC 单独添加「网域」或「网址前缀」属性：

| 属性 | Sitemap URL |
|------|-------------|
| `kakospreadsheet.es` | https://kakospreadsheet.es/sitemap.xml |
| `kakospreadsheet.fr` | https://kakospreadsheet.fr/sitemap.xml |
| `kakospreadsheet.ca` | https://kakospreadsheet.ca/sitemap.xml |
| `kakospreadsheet.nl` | https://kakospreadsheet.nl/sitemap.xml |
| `kakobuy.fi` | https://kakobuy.fi/sitemap.xml |

## 二、验证方式（Cloudflare 站点推荐）

站点经 Cloudflare 代理，推荐：

1. **DNS 验证（网域属性）** — 在 Cloudflare DNS 添加 Google 提供的 TXT 记录
2. 或 **HTML 文件验证** — 上传 `google*.html` 到 `/www/wwwroot/{domain}/`

## 三、提交 Sitemap 步骤

对每个已验证属性：

1. 左侧 **Sitemaps（站点地图）**
2. 输入：`sitemap.xml`
3. 点击 **提交**

## 四、提交后检查（约 48h）

- **网页** → 查看「已编入索引」数量
- **效果** → 按国家过滤查询词
- 重点词：`kakobuy spreadsheet`、`kakobuy coupon`、`is kakobuy legit` 及各国本地化词

## 五、hreflang 提示

五站已互链 hreflang，`x-default` 为 `kakospreadsheet.ca`。GSC 国际化报告可在 `.ca` 属性查看 cluster 覆盖。
