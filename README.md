# seo-factory

SEO 内容生产流水线：整合 Semrush、Google Search Console 与产品数据，按站点生成优化内容。

## 目录结构

```
seo-factory/
├── data/                  # 原始数据（不入库大文件）
│   ├── semrush/           # Semrush 关键词、竞品等导出
│   ├── gsc/               # Google Search Console 导出
│   └── products/          # 产品/类目数据
├── sites/                 # 按域名组织的站点配置与内容
│   └── fansspreadsheet.net/
├── output/                # 脚本生成的中间产物与最终输出
├── scripts/               # 数据处理与生成脚本
├── templates/             # 页面/段落 HTML 或 Markdown 模板
├── prompts/               # LLM prompt 模板
└── README.md
```

## 工作流（规划）

1. **导入数据** — 将 Semrush、GSC、产品 CSV/JSON 放入 `data/` 对应子目录
2. **分析** — `scripts/` 清洗、合并关键词与页面机会
3. **生成** — 结合 `templates/` 与 `prompts/` 产出草稿
4. **发布** — 输出到 `output/` 或 `sites/<domain>/`

## 当前站点

| 域名 | 目录 |
|------|------|
| fansspreadsheet.net | `sites/fansspreadsheet.net/` |

## 快速开始

```bash
cd ~/Projects/seo-factory

# 将导出文件放入 data 子目录后，运行脚本（待实现）
# python scripts/analyze.py --site fansspreadsheet.net
```

## 数据约定

- `data/semrush/` — 关键词难度、搜索量、SERP 等
- `data/gsc/` — 查询、展示、点击、排名
- `data/products/` — SKU、类目、卖点等结构化数据

大体积原始导出默认被 `.gitignore` 忽略；仅保留目录占位文件。
