# -*- coding: utf-8 -*-
"""十一五日游方案集 · 静态网页生成器
用法：python build.py
输出：index.html + plan-01-xxx.html ... plan-14-wuhan.html（共15个页面）
"""
import os
import re
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

from plans_data_a import PLANS_A
from plans_data_b import PLANS_B
from plans_data_c import PLANS_C
from plans_data_d import PLANS_D
from plans_data_e import PLANS_E
from plans_data_f import PLANS_F

PLANS = PLANS_A + PLANS_B + PLANS_C + PLANS_D + PLANS_E + PLANS_F
HERE = os.path.dirname(os.path.abspath(__file__))

TYPE_ORDER = ["吃货天堂", "山水画卷", "海滨度假", "人文古城", "都市漫步"]
TYPE_ICON = {"吃货天堂": "🍜", "山水画卷": "⛰️", "海滨度假": "🌊", "人文古城": "🏯", "都市漫步": "🏙️"}
SCORE_NOTE = {
    "轻松": "越多越省力",
    "美食": "越多越好吃",
    "美景": "越多越好看",
    "十一人流": "越多越拥挤",
}

CSS = """
*{box-sizing:border-box;margin:0;padding:0}
html{scroll-behavior:smooth;overflow-x:hidden}
body{font-family:"PingFang SC","Microsoft YaHei","Noto Sans SC","Source Han Sans SC",system-ui,sans-serif;color:#2c2a26;background:#faf9f5;line-height:1.8;-webkit-font-smoothing:antialiased;zoom:1.12}
a{color:inherit;text-decoration:none}
.wrap{max-width:1000px;margin:0 auto;padding:0 22px}
/* ---- 详情页头部 ---- */
.hero{background:linear-gradient(165deg,color-mix(in srgb,var(--accent) 14%,#fff),#faf9f5 72%);border-bottom:1px solid #ece4d6;padding:34px 0 28px}
.back{display:inline-block;font-size:13px;color:#8a8375;margin-bottom:14px}
.back:hover{color:var(--accent)}
.emoji{font-size:42px;line-height:1}
h1.title{font-size:29px;margin:10px 0 8px;letter-spacing:.5px;color:#26241f}
.subtitle{color:#6b675e;font-size:15.5px;max-width:680px}
.tags{margin-top:14px;display:flex;flex-wrap:wrap;gap:8px}
.tag{font-size:12.5px;padding:3px 12px;border-radius:999px;background:color-mix(in srgb,var(--accent) 10%,#fff);color:color-mix(in srgb,var(--accent) 82%,#000);border:1px solid color-mix(in srgb,var(--accent) 28%,#fff)}
/* ---- 速览 ---- */
.facts{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:14px;margin:26px 0 8px}
.fact{background:#fff;border:1px solid #ece4d6;border-radius:14px;padding:13px 16px;font-size:13.8px;color:#4a463e}
.fact b{display:block;font-size:12px;color:#9a9384;font-weight:600;margin-bottom:3px;letter-spacing:1.5px}
.scores{display:grid;grid-template-columns:repeat(auto-fit,minmax(190px,1fr));gap:14px;margin:14px 0 6px}
.score{background:#fff;border:1px solid #ece4d6;border-radius:14px;padding:11px 16px}
.score .lab{font-size:12.5px;color:#9a9384;display:flex;justify-content:space-between;align-items:baseline}
.score .lab em{font-style:normal;color:#c2bbaa;font-size:11px}
.dots{font-size:15px;color:var(--accent);letter-spacing:3px;margin-top:2px}
/* ---- 章节 ---- */
h2.sec{font-size:20px;margin:34px 0 14px;display:flex;align-items:center;gap:10px;color:#26241f}
h2.sec::before{content:"";width:5px;height:19px;border-radius:3px;background:var(--accent)}
.strip{display:grid;grid-template-columns:repeat(auto-fit,minmax(170px,1fr));gap:10px}
.chip{background:#fff;border:1px solid #ece4d6;border-radius:12px;padding:9px 12px;font-size:13px;color:#57534a}
.chip b{color:var(--accent);display:block;font-size:11.5px;margin-bottom:1px;letter-spacing:1px}
/* ---- 每日行程 ---- */
.day{background:#fff;border:1px solid #ece4d6;border-radius:16px;padding:18px 22px;margin-bottom:16px;box-shadow:0 1px 2px rgba(60,50,30,.03)}
.day h3{font-size:16.5px;margin-bottom:10px;color:#33302a}
.day h3 .d{color:color-mix(in srgb,var(--accent) 85%,#000)}
.slot{display:flex;gap:14px;padding:9px 0;border-top:1px dashed #efe8da}
.day .slot:first-of-type{border-top:0}
.slot .lab{flex:0 0 52px;height:26px;border-radius:8px;font-size:12.5px;display:flex;align-items:center;justify-content:center;margin-top:3px;font-weight:600}
.lab.am{background:#fdf3e2;color:#a06a12}
.lab.pm{background:#e8f3ec;color:#2f7d51}
.lab.eve{background:#efecfa;color:#5d4fb3}
.slot p{flex:1;font-size:14.3px;color:#4a463e}
.eats{margin-top:8px;background:color-mix(in srgb,var(--accent) 7%,#fff);border:1px dashed color-mix(in srgb,var(--accent) 38%,#fff);border-radius:10px;padding:8px 14px;font-size:13.3px;color:#6b675e}
.eats b{color:var(--accent);font-weight:600;margin-right:6px}
/* ---- 必吃清单 ---- */
.eatgrid{display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:10px}
.eat{background:#fff;border:1px solid #ece4d6;border-radius:10px;padding:8px 14px;font-size:13.8px;color:#4a463e}
.eat::before{content:"✦ ";color:var(--accent)}
/* ---- 实用信息 ---- */
.info{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:14px}
.info .box{background:#fff;border:1px solid #ece4d6;border-radius:14px;padding:15px 18px}
.box h4{font-size:14.5px;margin-bottom:7px;color:#33302a}
.box ul{list-style:none}
.box li{font-size:13.5px;color:#57534a;padding:3px 0 3px 16px;position:relative}
.box li::before{content:"";position:absolute;left:2px;top:14px;width:5px;height:5px;border-radius:50%;background:color-mix(in srgb,var(--accent) 65%,#fff)}
/* ---- 上下翻页 ---- */
.pager{display:flex;gap:12px;margin:30px 0 10px}
.pager a{flex:1;background:#fff;border:1px solid #ece4d6;border-radius:12px;padding:11px 16px;font-size:13.5px;color:#57534a;transition:.15s}
.pager a:hover{border-color:var(--accent);color:var(--accent)}
.pager a small{display:block;color:#b7b0a2;font-size:11.5px;margin-bottom:1px}
.pager a.next{text-align:right}
.pager a.home{flex:0 0 140px;display:flex;align-items:center;justify-content:center}
footer{padding:20px 0 36px;color:#b7b0a2;font-size:12.5px;text-align:center}
/* ---- 总览页 ---- */
.idx-hero{background:linear-gradient(160deg,#fdf3e7,#faf9f5);border-bottom:1px solid #ece4d6;padding:46px 0 32px;text-align:center}
.idx-hero .kicker{font-size:13px;letter-spacing:5px;color:#a89f8d}
.idx-hero h1{font-size:33px;margin:10px 0 8px;color:#26241f}
.idx-hero p{color:#6b675e;font-size:14.5px}
.pick{background:#fff;border:1px solid #ece4d6;border-radius:14px;padding:14px 20px;margin:18px 0;font-size:13.8px;color:#57534a;line-height:2}
.pick b{color:#26241f}
.tablewrap{overflow-x:auto;background:#fff;border:1px solid #ece4d6;border-radius:14px}
table{width:100%;border-collapse:collapse;font-size:13.2px;min-width:1020px}
th{background:#f4efe6;padding:10px 10px;font-size:12.2px;color:#8a8375;letter-spacing:1px;white-space:nowrap;text-align:left}
td{padding:10px;border-top:1px solid #f0eade;vertical-align:middle}
tbody tr:hover td{background:#fbf7ef}
td a.city{font-weight:600}
td a.city:hover{color:#c05a2e}
.mini{letter-spacing:2px;color:#c05a2e;white-space:nowrap}
.cardgrid{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:16px;margin-top:14px}
.card{background:#fff;border:1px solid #ece4d6;border-radius:16px;padding:19px;transition:.15s;display:block}
.card:hover{transform:translateY(-3px);box-shadow:0 10px 24px rgba(60,50,30,.09);border-color:#d8cdb8}
.card .top{display:flex;align-items:center;gap:10px}
.card .top .emoji{font-size:29px}
.card h3{font-size:17.5px;color:#26241f}
.card .sub{font-size:13px;color:#8a8375;margin:8px 0 10px;min-height:42px}
.card .meta{display:flex;gap:8px;flex-wrap:wrap;font-size:12.2px;color:#6b675e}
.card .meta span{background:#f6f1e7;border-radius:8px;padding:2px 9px}
.card .go{margin-top:11px;font-size:13px;color:#c05a2e;font-weight:600}
@media (max-width:640px){
  h1.title{font-size:24px}
  .slot{flex-direction:column;gap:6px}
  .slot .lab{margin-top:0}
  .idx-hero h1{font-size:26px}
}
@media print{
  .pager,.back,.card .go{display:none}
  .day{break-inside:avoid}
  body{background:#fff;zoom:1}
}
"""


def dots(n):
    return "●" * n + "○" * (5 - n)


def page(fname, body, accent="#c05a2e"):
    head = (
        '<!DOCTYPE html>\n<html lang="zh-CN">\n<head>\n<meta charset="UTF-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
        "<title>" + body["title"] + "</title>\n<style>:root{--accent:" + accent + "}\n"
        + CSS + "</style>\n</head>\n<body>\n"
    )
    html = head + body["html"] + "\n</body>\n</html>\n"
    path = os.path.join(HERE, fname)
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)
    return fname


def detail_body(p, prev, nxt):
    parts = []
    parts.append('<header class="hero"><div class="wrap">')
    parts.append('<a class="back" href="index.html">← 返回总览（%d 城方案）</a>' % len(PLANS))
    parts.append('<div class="emoji">' + p["emoji"] + "</div>")
    parts.append('<h1 class="title">' + p["title"] + "</h1>")
    parts.append('<p class="subtitle">' + p["subtitle"] + "</p>")
    parts.append(
        '<div class="tags">'
        + "".join('<span class="tag">' + t + "</span>" for t in p["tags"])
        + "</div>"
    )
    parts.append("</div></header>")

    parts.append('<main class="wrap">')
    # 速览
    parts.append('<div class="facts">')
    for label, val in [
        ("🌤️ 十月天气", p["weather"]),
        ("👥 适合谁", p["best_for"]),
        ("💰 预算参考", p["budget"]),
        ("🏠 住哪一带", p["stay"]),
    ]:
        parts.append('<div class="fact"><b>' + label + "</b>" + val + "</div>")
    parts.append("</div>")
    # 指数
    parts.append('<div class="scores">')
    for label, val in p["scores"].items():
        parts.append(
            '<div class="score"><div class="lab"><span>'
            + label
            + '</span><em>'
            + SCORE_NOTE[label]
            + "</em></div>"
            + '<div class="dots">'
            + dots(val)
            + "</div></div>"
        )
    parts.append("</div>")

    # 行程一览
    parts.append('<h2 class="sec">行程一览</h2><div class="strip">')
    for d in p["days"]:
        key, _, theme = d["t"].partition("｜")
        parts.append('<div class="chip"><b>' + key + "</b>" + (theme or d["t"]) + "</div>")
    parts.append("</div>")

    # 每日安排
    parts.append('<h2 class="sec">每日安排</h2>')
    for d in p["days"]:
        key, _, theme = d["t"].partition("｜")
        parts.append('<section class="day"><h3><span class="d">' + key + "</span> ｜ " + (theme or "") + "</h3>")
        for label, cls, txt in [("上午", "am", d["am"]), ("下午", "pm", d["pm"]), ("晚上", "eve", d["eve"])]:
            if txt:
                parts.append(
                    '<div class="slot"><span class="lab ' + cls + '">' + label + "</span><p>" + txt + "</p></div>"
                )
        parts.append('<div class="eats"><b>🍽 今日觅食</b>' + d["eats"] + "</div>")
        parts.append("</section>")

    # 必吃清单
    parts.append('<h2 class="sec">必吃清单</h2><div class="eatgrid">')
    for m in p["must_eat"]:
        parts.append('<div class="eat">' + m + "</div>")
    parts.append("</div>")

    # 实用信息
    parts.append('<h2 class="sec">实用信息</h2><div class="info">')
    parts.append('<div class="box"><h4>🚄 交通指南</h4><ul><li>' + p["transport"] + "</li></ul></div>")
    parts.append('<div class="box"><h4>🎫 提前预约/购票</h4><ul>')
    for b in p["booking"]:
        parts.append("<li>" + b + "</li>")
    parts.append("</ul></div>")
    parts.append('<div class="box"><h4>💡 避坑与小贴士</h4><ul>')
    for t in p["tips"]:
        parts.append("<li>" + t + "</li>")
    parts.append("</ul></div>")
    parts.append("</div>")

    # 翻页
    parts.append('<nav class="pager">')
    if prev:
        parts.append(
            '<a href="plan-%02d-%s.html"><small>上一份 · %s</small>%s</a>'
            % (prev["num"], prev["slug"], prev["city"], prev["title"])
        )
    parts.append('<a class="home" href="index.html">返回总览</a>')
    if nxt:
        parts.append(
            '<a class="next" href="plan-%02d-%s.html"><small>下一份 · %s</small>%s</a>'
            % (nxt["num"], nxt["slug"], nxt["city"], nxt["title"])
        )
    parts.append("</nav>")
    parts.append(
        '<footer>十一五日游方案集 · 方案 %02d / %d · 生成于 2026-09-23 · 价格与开放信息请以出行时为准</footer>'
        % (p["num"], len(PLANS))
    )
    parts.append("</main>")
    return {"title": p["title"] + " · 十一五日游方案集", "html": "\n".join(parts)}


def index_body(plans):
    parts = []
    parts.append('<header class="idx-hero"><div class="wrap">')
    parts.append('<div class="kicker">2026 国庆 · 轻松慢节奏 · 美食与美景兼得</div>')
    parts.append("<h1>十一五日游 · %d 城方案集</h1>" % len(plans))
    parts.append(
        "<p>每份都是五天四晚、每天只安排两三个重点的“不赶路”计划；点击对比表或卡片查看完整行程。</p>"
    )
    parts.append("</div></header>")
    parts.append('<main class="wrap">')

    parts.append(
        '<div class="pick"><b>怎么选：</b>'
        "就想吃 → 成都 / 重庆 / 长沙 / 潮汕 / 广州顺德 / 武汉；"
        "看山水 → 大理 / 桂林阳朔 / 杭州（十月桂花季）；"
        "想看海 → 厦门 / 青岛 / 海南；"
        "爱人文 → 西安 / 福州泉州 / 皖南。"
        "<br><b>指数说明：</b>●越多代表越轻松 / 越好吃 / 越好看，也代表人越多（十一人流为反向指标，选低更清静）。</div>"
    )

    # 对比表
    parts.append('<h2 class="sec">%d 份方案对比表</h2>' % len(plans))
    parts.append('<div class="tablewrap"><table>')
    parts.append(
        "<tr><th>#</th><th>城市</th><th>类型</th><th>轻松</th><th>美食</th><th>美景</th>"
        + "<th>十一人流</th><th>预算/人</th><th>一句话点评</th></tr>"
    )
    for p in plans:
        budget_short = re.sub(r"（[^）]*）", "", p["budget"]).replace("约 ", "").strip()
        parts.append(
            '<tr><td>%02d</td><td><a class="city" href="plan-%02d-%s.html">%s %s</a></td><td>%s</td>'
            % (p["num"], p["num"], p["slug"], p["emoji"], p["city"], p["type"])
            + "".join('<td class="mini">%s</td>' % dots(p["scores"][k]) for k in ["轻松", "美食", "美景", "十一人流"])
            + "<td>%s</td><td>%s</td></tr>" % (budget_short, p["highlight"])
        )
    parts.append("</table></div>")

    # 分组卡片
    by_type = {}
    for p in plans:
        by_type.setdefault(p["type"], []).append(p)
    for t in TYPE_ORDER:
        group = by_type.get(t, [])
        if not group:
            continue
        parts.append('<h2 class="sec">%s %s（%d 份）</h2><div class="cardgrid">' % (TYPE_ICON[t], t, len(group)))
        for p in group:
            parts.append('<a class="card" href="plan-%02d-%s.html">' % (p["num"], p["slug"]))
            parts.append('<div class="top"><span class="emoji">' + p["emoji"] + "</span><h3>" + p["city"] + " · " + p["title"].split("·")[-1].strip() + "</h3></div>")
            parts.append('<p class="sub">' + p["subtitle"] + "</p>")
            parts.append(
                '<div class="meta"><span>轻松 %s</span><span>美食 %s</span><span>美景 %s</span><span>人流 %s</span></div>'
                % (dots(p["scores"]["轻松"]), dots(p["scores"]["美食"]), dots(p["scores"]["美景"]), dots(p["scores"]["十一人流"]))
            )
            parts.append('<div class="go">查看完整五日行程 →</div>')
            parts.append("</a>")
        parts.append("</div>")

    parts.append(
        '<footer>十一五日游方案集 · 共 %d 份 · 生成于 2026-09-23<br>'
        "预算为不含往返大交通的人均估算；十一期间价格与预约政策波动大，出行前请逐项核实。</footer>"
        % len(plans)
    )
    parts.append("</main>")
    return {"title": "十一五日游 · %d 城方案集（总览）" % len(plans), "html": "\n".join(parts)}


def main():
    made = []
    made.append(page("index.html", index_body(PLANS)))
    for i, p in enumerate(PLANS):
        prev = PLANS[i - 1] if i > 0 else None
        nxt = PLANS[i + 1] if i < len(PLANS) - 1 else None
        made.append(page("plan-%02d-%s.html" % (p["num"], p["slug"]), detail_body(p, prev, nxt), p["accent"]))
    print("生成完成，共 %d 个页面：" % len(made))
    for m in made:
        print("  -", m)


if __name__ == "__main__":
    main()
