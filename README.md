# 十一五日游 · 23 城方案集

2026 国庆五日游计划：23 份"轻松慢节奏、美食与美景兼得"的城市方案，输出为纯静态网页（无外部依赖，离线可开）。

**在线地址**：<http://111.229.218.104/travel/>（腾讯云 Caddy 部署，根路径为站点导航门户）

## 方案一览

| 分组 | 方案 |
|---|---|
| 🍜 吃货天堂 | 成都、重庆、长沙、潮汕、广州·顺德、武汉 |
| ⛰️ 山水画卷 | 大理、桂林·阳朔、杭州、三峡（宜昌坐船慢游）、贵州（安顺·西江）、庐山·九江 |
| 🌊 海滨度假 | 厦门、青岛、海口·三亚、威海、威海·荣成 |
| 🏯 人文古城 | 西安、福州·泉州、济南·泰山·曲阜、大同·平遥·太原、皖南（绩溪·歙县） |
| 🏙️ 都市漫步 | 上海 |

每份方案包含：十月天气、住宿区域、四项指数（轻松/美食/美景/十一人流）、每日"上午/下午/晚上"三段式行程、必吃清单、预约提醒与避坑贴士。

## 目录结构

```
plans_data_a.py ~ plans_data_f.py   # 21 份行程数据（每城一个 dict）
build.py                            # 网页生成器（数据 → HTML）
index.html                          # 总览页：对比表 + 分组卡片
plan-01-chengdu.html ... plan-21-wanxi.html   # 各方案详情页
```

## 使用

```bash
python build.py    # 修改 plans_data_*.py 后重新生成全部页面
```

生成后可直接双击 `index.html` 本地浏览，或部署到任意静态服务器。

## 部署（腾讯云示例）

```bash
tar czf site.tar.gz *.html
scp -q site.tar.gz cloud104:~/
ssh cloud104 'sudo tar xzf ~/site.tar.gz -C /var/www/travel && rm ~/site.tar.gz'
```

服务器侧由 Caddy 提供服务：`/etc/caddy/Caddyfile` 中 `:80 { root * /var/www/travel; file_server; encode gzip }`。
