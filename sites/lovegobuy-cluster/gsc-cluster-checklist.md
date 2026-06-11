# Lovegobuy 集群 — GSC 操作清单

## 一、添加 8 个「网址前缀」资源

```
https://lovegobuyspreadsheet.es/
https://lovegobuyspreadsheet.it/
https://lovegobuy.it/
https://lovegobuyspreadsheet.nl/
https://lovegobuy.nl/
https://lovegobuyspreadsheet.ca/
https://lovegobuyspreadsheet.eu/
https://lovegobuyguide.com/
```

## 二、提交站点地图（每资源 1 条）

见 `cluster-config.json` → `gsc_sitemaps`。

## 三、P1 网址检查

见 `cluster-config.json` → `gsc_p1_urls`（约 24 条核心 URL）。

**规则：** 在哪个域的资源里，就只对该域 URL 点「请求编入索引」。
