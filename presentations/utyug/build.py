#!/usr/bin/env python3
"""Генератор презентаций «Паровой утюг» (RU / KK) в стиле конспектов по швам.

Запуск:  python3 build.py   ->  ru.html, kk.html
PDF:     node render.js ru.html Паровой_утюг_RU.pdf
"""
import html
from content import RU, KK
import art

FONT_FACES = []
_RANGES = {
    "latin": "U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,U+2000-206F,U+2074,U+20AC,U+2122,U+2191,U+2193,U+2212,U+2215,U+FEFF,U+FFFD",
    "cyrillic": "U+0301,U+0400-045F,U+0490-0491,U+04B0-04B1,U+2116",
    "cyrillic-ext": "U+0460-052F,U+1C80-1C88,U+20B4,U+2DE0-2DFF,U+A640-A69F,U+FE2E-FE2F",
}
for fam, weights in (("Lora", (400, 600, 700)), ("Nunito", (400, 600, 700, 800))):
    for w in weights:
        for sub, rng in _RANGES.items():
            FONT_FACES.append(
                f"@font-face{{font-family:'{fam}';font-weight:{w};font-style:normal;"
                f"src:url('fonts/{fam.lower()}-{sub}-{w}-normal.woff2') format('woff2');unicode-range:{rng};}}"
            )

CSS = """
@page{size:1280px 720px;margin:0}
*{box-sizing:border-box;margin:0;padding:0}
html,body{background:#1F2A47}
body{font-family:'Nunito',sans-serif;color:#1F2A47;-webkit-print-color-adjust:exact;print-color-adjust:exact}
.slide{width:1280px;height:720px;position:relative;overflow:hidden;page-break-after:always;break-after:page}
.light{background:#F5EEE2}
.dark{background:#1F2A47;color:#F5EEE2}
.kicker{position:absolute;left:64px;top:54px;font-weight:800;font-size:16.5px;letter-spacing:.11em;text-transform:uppercase;color:#B8432A}
.dark .kicker{color:#EDB563}
h1{font-family:'Lora',serif;font-weight:600;font-size:46px;line-height:1.12;letter-spacing:-.005em}
.head{position:absolute;left:64px;top:84px;right:64px}
.sub{font-size:16.5px;color:#55596A;margin-top:5px}
.dark .sub{color:#B9C1D6}
.lead{font-size:20px;line-height:1.5;color:#1F2A47}
.dark .lead{color:#DDE2EE}
.lead p+p{margin-top:12px}
.left{position:absolute;left:64px;top:170px;width:644px}
.left.hasSub{top:192px}
.stack{display:flex;flex-direction:column;gap:12px;margin-top:18px}
.card{background:#FDF8EE;border:1.5px dashed #CFC1A2;border-radius:14px;padding:12px 18px 13px 18px;display:flex;gap:14px;align-items:flex-start}
.card .num,.gcard .num{flex:none;width:34px;height:34px;border-radius:50%;background:#B8432A;color:#fff;font-weight:800;font-size:16px;display:flex;align-items:center;justify-content:center;margin-top:3px}
.dotbadge{flex:none;width:58px;height:34px;border-radius:17px;background:#EBE3CE;display:flex;align-items:center;justify-content:center;gap:4px;margin-top:3px}
.dotbadge i{display:block;width:9px;height:9px;border-radius:50%;background:#1F2A47}
.card h3{font-family:'Lora',serif;font-weight:700;font-size:21px;line-height:1.2}
.card h3 small{font-weight:600;font-size:.82em;color:#55596A}
.card p{font-size:16.5px;line-height:1.38;margin-top:2px}
.card.plain{display:block}
.compact .card{padding:9px 16px 10px}
.compact .stack{gap:9px;margin-top:14px}
.compact .call{margin-top:12px;padding:13px 18px 14px}
.compact .call span{font-size:17px}
.duo{display:flex;gap:12px;margin-top:16px}
.duo .card{flex:1;display:block}
.call{background:#1F2A47;color:#F5EEE2;border-radius:12px;padding:16px 20px 17px;margin-top:16px}
.call b{display:block;color:#EDB563;font-weight:800;font-size:15.5px;letter-spacing:.1em;text-transform:uppercase;margin-bottom:6px}
.call span{font-size:18px;line-height:1.45}
.panel{position:absolute;right:64px;top:186px;width:466px;background:#FDF8EE;border:1.5px dashed #CFC1A2;border-radius:18px;padding:20px 20px 18px}
.panel svg{display:block;width:100%;height:auto}
.panel .cap{font-size:15.5px;line-height:1.45;color:#55596A;margin-top:14px;padding:0 4px}
/* dark grid */
.grid{position:absolute;left:64px;right:64px;top:238px;bottom:26px;display:grid;gap:16px}
.g3{grid-template-columns:repeat(3,1fr);grid-template-rows:repeat(2,1fr)}
.g2{grid-template-columns:repeat(2,1fr);grid-template-rows:repeat(2,1fr)}
.gcard{background:#263558;border:1.5px dashed #43557F;border-radius:14px;padding:16px 18px}
.gcard .row{display:flex;align-items:center;gap:11px}
.gcard .num{background:#EDB563;color:#1F2A47;margin-top:0;width:32px;height:32px;font-size:15px}
.gcard h3{font-family:'Lora',serif;font-weight:600;font-size:24px;color:#F5EEE2;line-height:1.15}
.gcard p{font-size:19px;line-height:1.42;margin-top:9px;color:#DDE2EE}
.g2 .gcard p{font-size:20px}
.gcard.cream{background:#F5EEE2;border:1.5px solid #F5EEE2}
.gcard.cream .num{background:#B8432A;color:#fff}
.gcard.cream h3{color:#1F2A47}
.gcard.cream p{color:#1F2A47}
/* contents */
.toc{position:absolute;left:64px;right:64px;top:118px;bottom:24px;display:flex;flex-direction:column;gap:9px}
.toc h1{position:absolute;left:0;top:-62px}
.row{flex:1}
.toc .item{flex:1;background:#FDF8EE;border:1.5px dashed #CFC1A2;border-radius:14px;display:flex;align-items:center;padding:0 22px;gap:16px}
.toc .num{flex:none;width:36px;height:36px;border-radius:50%;background:#B8432A;color:#fff;font-weight:800;font-size:16px;display:flex;align-items:center;justify-content:center}
.toc .t{font-family:'Lora',serif;font-weight:700;font-size:21px;width:520px;flex:none}
.toc .d{font-size:16.5px;color:#55596A}
/* title */
.t-left{position:absolute;left:64px;top:0;bottom:0;width:640px;display:flex;flex-direction:column;justify-content:center}
.t-left .k{font-weight:800;font-size:17px;letter-spacing:.12em;text-transform:uppercase;color:#EDB563}
.t-left h1{font-size:76px;line-height:1.05;margin-top:16px;color:#F5EEE2;font-weight:500}
.t-left .st{font-family:'Lora',serif;font-size:29px;color:#EDB563;margin-top:18px}
.t-left .ds{font-size:19px;line-height:1.55;color:#C5CCDE;margin-top:16px;max-width:600px}
.pills{display:flex;gap:12px;margin-top:22px}
.pill{border:1.5px dashed #43557F;background:#263558;border-radius:999px;padding:11px 20px;font-weight:700;font-size:17px;color:#F5EEE2}
.src{position:absolute;left:64px;bottom:34px;font-size:14px;color:#8E98B3}
.t-art{position:absolute;right:56px;top:150px;width:560px;height:440px}
/* table */
table{position:absolute;left:64px;right:64px;top:176px;width:1152px;border-collapse:collapse;background:#FDF8EE;border:1.5px solid #CFC1A2;table-layout:fixed}
th{background:#1F2A47;color:#F5EEE2;text-align:left;font-weight:700;font-size:17px;padding:11px 12px;border-right:1px solid #3A4668}
td{font-size:17px;padding:10.5px 12px;border-top:1px solid #CFC1A2;border-right:1px solid #CFC1A2;line-height:1.28}
tr:nth-child(even) td{background:#EBE3CE}
td:first-child{font-weight:700}
.dots{display:inline-flex;gap:3px;margin-right:6px;vertical-align:middle}
.dots i{display:block;width:9px;height:9px;border-radius:50%;background:#1F2A47}
/* glossary */
.gl{position:absolute;left:64px;right:64px;top:176px;display:grid;grid-template-columns:1fr 1fr;gap:18px}
.gl table{position:static;width:100%}
.gl td{font-size:18.5px;padding:12px 12px}
.gl th{font-size:18px;padding:12px}
"""


def e(s):
    return html.escape(s, quote=False)


def kicker(t):
    return f'<div class="kicker">{e(t)}</div>'


def head(title, sub=None):
    s = f'<div class="sub">{e(sub)}</div>' if sub else ""
    return f'<div class="head"><h1>{e(title)}</h1>{s}</div>'


def card(i, t, p, small=None):
    sm = f' <small>{e(small)}</small>' if small else ""
    return (f'<div class="card"><div class="num">{i}</div><div><h3>{e(t)}{sm}</h3>'
            f'<p>{e(p)}</p></div></div>')


def dots_card(n, t, p):
    dots = "<i></i>" * n
    return (f'<div class="card"><div class="dotbadge">{dots}</div><div><h3>{e(t)}</h3>'
            f'<p>{e(p)}</p></div></div>')


def content(d, panel_svg):
    has_sub = bool(d.get("sub"))
    lead = "".join(f"<p>{e(x)}</p>" for x in d["lead"])
    cards = "".join(dots_card(int(c[0][1]), c[1], c[2]) if c[0].startswith("@")
                    else card(i + 1, *c) for i, c in enumerate(d["cards"]))
    call = ""
    if d.get("call"):
        call = f'<div class="call"><b>{e(d["call"][0])}</b><span>{e(d["call"][1])}</span></div>'
    panel = (f'<div class="panel" style="top:{d.get("ptop", 186)}px">{panel_svg}'
             f'<div class="cap">{e(d["cap"])}</div></div>')
    return (f'<section class="slide light">{kicker(d["kicker"])}{head(d["title"], d.get("sub"))}'
            f'<div class="left{" hasSub" if has_sub else ""}{" compact" if d.get("compact") else ""}"><div class="lead">{lead}</div>'
            f'<div class="stack">{cards}</div>{call}</div>{panel}</section>')


def grid(d, cols):
    cards = []
    n = len(d["cards"])
    for i, c in enumerate(d["cards"]):
        cream = " cream" if i == n - 1 and d.get("last_cream", True) else ""
        cards.append(f'<div class="gcard{cream}"><div class="row"><div class="num">{i+1}</div>'
                     f'<h3>{e(c[0])}</h3></div><p>{e(c[1])}</p></div>')
    return (f'<section class="slide dark">{kicker(d["kicker"])}{head(d["title"], d.get("sub"))}'
            f'<div class="left" style="top:{d.get("ltop", 170)}px;width:1152px"><div class="lead">{e(d["lead"])}</div></div>'
            f'<div class="grid g{cols}">{"".join(cards)}</div></section>')


def title_slide(d):
    pills = "".join(f'<div class="pill">{e(p)}</div>' for p in d["pills"])
    return (f'<section class="slide dark"><div class="t-left"><div class="k">{e(d["k"])}</div>'
            f'<h1>{e(d["title"])}</h1><div class="st">{e(d["sub"])}</div>'
            f'<div class="ds">{e(d["desc"])}</div><div class="pills">{pills}</div></div>'
            f'<div class="t-art">{art.title_art()}</div><div class="src">{e(d["src"])}</div></section>')


def toc_slide(d):
    items = "".join(f'<div class="item"><div class="num">{i+1}</div><div class="t">{e(t)}</div>'
                    f'<div class="d">{e(s)}</div></div>' for i, (t, s) in enumerate(d["items"]))
    return (f'<section class="slide light"><div class="toc"><h1>{e(d["title"])}</h1>{items}</div></section>')


def table_slide(d):
    th = "".join(f"<th>{e(h)}</th>" for h in d["cols"])
    body = ""
    for r in d["rows"]:
        cells = ""
        for j, c in enumerate(r):
            if j == 0 and c.startswith("@"):
                n = int(c[1])
                dots = '<span class="dots">' + "<i></i>" * n + "</span>"
                cells += f"<td>{dots}{e(c[2:].strip())}</td>"
            else:
                cells += f"<td>{e(c)}</td>"
        body += f"<tr>{cells}</tr>"
    return (f'<section class="slide light">{kicker(d["kicker"])}{head(d["title"])}'
            f'<table style="top:{d.get("ttop", 176)}px"><colgroup><col style="width:27%"><col style="width:40%"><col style="width:33%"></colgroup>'
            f'<tr>{th}</tr>{body}</table></section>')


def glossary_slide(d):
    def tbl(rows):
        b = "".join(f"<tr><td>{e(a)}</td><td>{e(k)}</td></tr>" for a, k in rows)
        return (f'<table><colgroup><col style="width:50%"><col style="width:50%"></colgroup>'
                f'<tr><th>{e(d["cols"][0])}</th><th>{e(d["cols"][1])}</th></tr>{b}</table>')
    half = (len(d["rows"]) + 1) // 2
    return (f'<section class="slide light">{kicker(d["kicker"])}{head(d["title"])}'
            f'<div class="gl">{tbl(d["rows"][:half])}{tbl(d["rows"][half:])}</div></section>')


def build(D, out):
    A = D["art"]
    s = []
    s.append(title_slide(D["title_slide"]))
    s.append(toc_slide(D["toc"]))
    s.append(content(D["safe1"], art.plug(A)))
    s.append(grid(D["safe2"], 3))
    s.append(content(D["prep"], art.prep(A)))
    s.append(grid(D["rules"], 2))
    s.append(content(D["temps"], art.temps(A)))
    s.append(content(D["steam"], art.inside(A)))
    s.append(grid(D["pros"], 3))
    s.append(content(D["how"], art.hanger(A)))
    s.append(content(D["nogo"], art.nogo(A)))
    s.append(content(D["dry"], art.dry(A)))
    s.append(content(D["care"], art.sole(A)))
    s.append(grid(D["selfclean"], 3))
    s.append(content(D["vto"], art.vto(A)))
    s.append(table_slide(D["table"]))
    if "gloss" in D:
        s.append(glossary_slide(D["gloss"]))
    doc = (f'<!doctype html><html lang="{D["lang"]}"><head><meta charset="utf-8">'
           f'<meta name="viewport" content="width=1280"><title>{e(D["doc_title"])}</title>'
           f'<style>{"".join(FONT_FACES)}{CSS}</style></head><body>{"".join(s)}</body></html>')
    with open(out, "w", encoding="utf-8") as f:
        f.write(doc)
    print(out, len(s), "slides")


if __name__ == "__main__":
    build(RU, "ru.html")
    build(KK, "kk.html")
