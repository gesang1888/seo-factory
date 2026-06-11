# kakobuy.fi 建站内容方案

## 定位

- 芬兰市场，fi-FI，EUR
- 域名直接用 `kakobuy` 抢品牌词（非 spreadsheet 子域）
- 正文芬兰语，品牌/技术词保留 Kakobuy / Spreadsheet / QC
- **Semrush 数据待补充后微调 slug 优先级**

## 页面矩阵（基于推断 + 集群模板）

| URL | 目标关键词 | 角色 |
|-----|-----------|------|
| `/` | kakobuy | 品牌 hub |
| `/kakobuy-spreadsheet/` | kakobuy spreadsheet | 核心工具页 |
| `/kakobuy-kokemuksia/` | kakobuy kokemuksia, luotettava | **FI 独占** 评测 |
| `/kakobuy-toimitus/` | kakobuy toimitus, tullit | **FI 独占** 物流关税 |
| `/kakobuy-suomi/` | kakobuy suomi | **FI 独占** 本国买家指南 |
| `/kakobuy-coupon/` | kakobuy kuponki | 优惠码 |
| `/kakobuy-shipping/` | kakobuy shipping (EN) | 英语长尾 fallback |
| `/is-kakobuy-legit/` | is kakobuy legit (EN) | 英语信任页 |
| `/kakobuy-qc/` | kakobuy qc | QC 教程 |
| `/how-to-use-kakobuy/` | miten käyttää kakobuy | 教程 |

## 首页关键词网格

- Kakobuy Spreadsheet
- Kakobuy kokemuksia
- Kakobuy toimitus Suomeen
- Kakobuy kuponki
- Onko Kakobuy luotettava?
- Kakobuy QC-kuvat

## FAQ（芬兰语）

1. Onko Kakobuy luotettava?
2. Kuinka kauan Kakobuy-toimitus kestää Suomeen?
3. Miten käytän Kakobuy-kuponkia?
4. Mitä QC tarkoittaa Kakobuyssa?
5. Mitkä ovat tullimaksut Suomessa?
6. Miten seuraan Kakobuy-tilausta?

## 本地化

- 关税：ALV 24% + Tulli 免税额度说明
- 物流：Posti / DHL Finland 时效
- 可与 NL/CA 共享英文 FAQ 结构，但 H1/meta 必须芬兰语

## 数据回流

上线 2 周后从 GSC 导出芬兰查询，写入 `data/gsc/kakobuy.fi_queries.csv`，迭代 keyword-plan。
