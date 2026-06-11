# Lovegobuy 八国 SEO 集群

基于 Semrush 导出（2026-06）+ 用户域名列表。

## 集群域（8）

| 域名 | 市场 | 角色 | 品牌词 Vol (Semrush) |
|------|------|------|---------------------|
| lovegobuyspreadsheet.es | 西班牙 es-ES | spreadsheet | 2,900 |
| lovegobuyspreadsheet.it | 意大利 it-IT | spreadsheet | 480 |
| lovegobuy.it | 意大利 it-IT | brand 短域 | 480 |
| lovegobuyspreadsheet.nl | 荷兰 nl-NL | spreadsheet | 140 |
| lovegobuy.nl | 荷兰 nl-NL | brand 短域 | 140 |
| lovegobuyspreadsheet.ca | 加拿大 en-CA | spreadsheet | 260 |
| lovegobuyspreadsheet.eu | 欧洲 en | pan-EU | — |
| lovegobuyguide.com | 国际 en | guide + **x-default** | — |

全球 `lovegobuy` 约 **17K/月**（FR 9.9K 最大，但本批无 .fr 域）。

## 配置

| 项 | 值 |
|----|-----|
| 官网 | https://www.lovegobuy.com |
| 邀请码 | `W5RJX3` |
| 注册链接 | https://www.lovegobuy.com/?invite_code=W5RJX3 |
| Spreadsheet | https://w2clinks.com/spreadsheet/ |

## 构建与部署

```bash
cd ~/Projects/seo-factory
python3 build_lovegobuy_site.py

export LOVEGOBUY_DEPLOY_PASS='...'   # 或复用 KAKOBUY_DEPLOY_PASS
./deploy-lovegobuy.sh
```

## 数据

```
data/semrush/lovegobuy_raw/Lovegobuy/*.xlsx
```

## GSC

见 `gsc-cluster-checklist.md`
