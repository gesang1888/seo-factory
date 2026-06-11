# Kakobuy 五国 SEO 集群

基于 Semrush 关键词数据（2026-06）规划的国别站群。

## 集群域

| 域 | 市场 | Semrush 库 | 品牌词 Vol | Spreadsheet Vol | 优先级 |
|----|------|-----------|-----------|-----------------|--------|
| kakospreadsheet.es | 西班牙 | ES | 14,800 | 480 | P0 |
| kakospreadsheet.fr | 法国 | FR | 4,400 | 320 | P0 |
| kakospreadsheet.ca | 加拿大 | CA | 8,100 | 1,300 | P0 |
| kakospreadsheet.nl | 荷兰 | NL | 2,900 | 480 | P1 |
| kakobuy.fi | 芬兰 | FI（待导出） | — | — | P2 |

## 全球上下文

- 全球 `kakobuy` 总搜索量约 **87.2K/月**
- US 22.2K 由 `kakobuytips.com` 覆盖，本集群不抢 US
- `x-default` → `kakospreadsheet.ca`（英语、国际化友好）

## 关键词簇 → 页面类型（全集群共用）

| 簇 | 代表词 | 页面 slug |
|----|--------|-----------|
| spreadsheet | kakobuy spreadsheet | `/kakobuy-spreadsheet/` |
| spreadsheet-commercial | best kakobuy spreadsheet | `/best-kakobuy-spreadsheet/` |
| coupon | kakobuy coupon codes | `/kakobuy-coupon/` |
| shipping | kakobuy shipping calculator | `/kakobuy-shipping/` |
| trust | is kakobuy legit / safe | `/is-kakobuy-legit/` |
| qc | qc kakobuy | `/kakobuy-qc/` |
| how-to | how to use kakobuy | `/how-to-use-kakobuy/` |
| community | kakobuy discord / reddit | `/kakobuy-discord/` |

## 各国独占页（防跨域重复）

见各域 `content-plan.md` 中的「国别独占」章节。

## 数据文件

```
data/semrush/
├── kakobuy_ES_export.csv   # 待放入
├── kakobuy_FR_export.csv
├── kakobuy_CA_export.csv
├── kakobuy_NL_export.csv
└── kakobuy_FI_export.csv   # 待导出
```
