# -*- coding: utf-8 -*-
"""SVG-иллюстрации в стиле конспектов по швам (плоские формы, крем / синий / терракот / янтарь)."""

NAVY, NAVY2 = "#1F2A47", "#2E3C63"
CREAM, PAPER, TAN, LINE = "#F5EEE2", "#FDF8EE", "#EBE3CE", "#CFC1A2"
TERRA, AMBER, BLUE, YEL, PURPLE, GREEN = "#B8432A", "#EDB563", "#6F8FBA", "#E2B04A", "#8B6FB3", "#5E8C61"
GRAY = "#55596A"
_n = [0]


def _id(p):
    _n[0] += 1
    return f"{p}{_n[0]}"


def svg(w, h, body):
    return (f'<svg viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg" '
            f'font-family="Nunito, sans-serif">{body}</svg>')


def tile(x, y, w, h, fill=TAN, rx=12):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}"/>'


def iron(x, y, s=1.0, body=NAVY, handle=NAVY2, sole="#C9CEDB", level=0.5, flip=False, dot=AMBER):
    """Утюг сбоку (носик справа). Габариты в единицах 0..200 x 0..102."""
    cid = _id("c")
    win = (f'<clipPath id="{cid}"><rect x="62" y="52" width="72" height="26" rx="7"/></clipPath>'
           f'<rect x="62" y="52" width="72" height="26" rx="7" fill="#DCE8F4"/>')
    if level > 0:
        win += (f'<rect x="62" y="{52 + 26 * (1 - level):.1f}" width="72" height="{26 * level:.1f}" '
                f'fill="{BLUE}" clip-path="url(#{cid})"/>')
    t = f"translate({x} {y}) scale({-s if flip else s} {s})"
    if flip:
        t = f"translate({x + 200 * s} {y}) scale({-s} {s})"
    return (f'<g transform="{t}">'
            f'<path d="M10 98 H188 Q201 98 195 86 L176 52 Q168 40 152 40 H46 Q14 40 10 72 Z" fill="{body}"/>'
            f'<path d="M46 40 C48 6 130 2 152 40 L135 40 C126 22 72 22 63 40 Z" fill="{handle}"/>'
            f'<rect x="5" y="92" width="192" height="10" rx="5" fill="{sole}"/>'
            f'{win}<circle cx="30" cy="68" r="5.5" fill="{dot}"/></g>')


def wave(x, y, n=4, color=TERRA, w=2.5, up=-9, dash="5 5"):
    d = f"M{x} {y} q8 {up} 16 0" + " t16 0" * (n - 1)
    return f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{w}" stroke-linecap="round" stroke-dasharray="{dash}"/>'


def badge(cx, cy, kind, r=20):
    if kind == "ok":
        return (f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{GREEN}"/>'
                f'<path d="M{cx-9} {cy+1} l6 7 l12 -14" fill="none" stroke="#fff" stroke-width="4.5" stroke-linecap="round" stroke-linejoin="round"/>')
    return (f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{TERRA}"/>'
            f'<path d="M{cx-8} {cy-8} l16 16 M{cx+8} {cy-8} l-16 16" stroke="#fff" stroke-width="4.5" stroke-linecap="round"/>')


# ───────────────────────── титульная ─────────────────────────
def title_art():
    b = ""
    b += f'<path d="M-10 392 H560" stroke="#6F7893" stroke-width="3" stroke-dasharray="14 12" fill="none"/>'
    # «пуговица» — капля в кремовом круге
    b += f'<circle cx="70" cy="150" r="64" fill="{CREAM}"/><circle cx="70" cy="150" r="52" fill="none" stroke="#CFC8B6" stroke-width="3"/>'
    b += f'<path d="M70 106 C70 106 40 140 40 160 a30 30 0 0 0 60 0 C100 140 70 106 70 106Z" fill="{BLUE}"/>'
    b += f'<path d="M56 160 a14 14 0 0 0 12 14" fill="none" stroke="#fff" stroke-width="4" stroke-linecap="round" opacity=".7"/>'
    b += f'<circle cx="212" cy="58" r="26" fill="{AMBER}"/><path d="M212 44 C212 44 198 60 198 68 a14 14 0 0 0 28 0 C226 60 212 44 212 44Z" fill="{NAVY}"/>'
    # пунктирная «нить» пара
    b += (f'<path d="M20 372 C110 380 150 330 215 320 C290 308 330 330 395 292" fill="none" '
          f'stroke="{AMBER}" stroke-width="6" stroke-linecap="round" stroke-dasharray="16 14"/>')
    # утюг
    b += iron(250, 150, 1.5, body=CREAM, handle="#D9D0BB", sole="#E8A25A", level=0.55, dot=TERRA)
    # пар
    for i, x in enumerate((300, 360, 420)):
        b += f'<path d="M{x} 128 q-14 -22 0 -42 q14 -20 0 -42" fill="none" stroke="#E7765B" stroke-width="5" stroke-linecap="round" stroke-dasharray="1 0" opacity="{1 - i*0.18:.2f}"/>'
    return svg(560, 440, b)


# ───────────────────────── 1. розетка ─────────────────────────
def plug(A):
    b = tile(0, 0, 426, 124) + tile(0, 140, 426, 124)
    # верх: розетка + вилка
    b += f'<rect x="36" y="22" width="80" height="80" rx="18" fill="{PAPER}" stroke="{LINE}" stroke-width="2"/>'
    b += f'<circle cx="76" cy="62" r="28" fill="none" stroke="{LINE}" stroke-width="2"/>'
    b += f'<rect x="104" y="40" width="74" height="44" rx="12" fill="{NAVY}"/>'
    b += f'<rect x="92" y="48" width="14" height="7" rx="2" fill="{NAVY2}"/><rect x="92" y="69" width="14" height="7" rx="2" fill="{NAVY2}"/>'
    b += f'<path d="M178 62 C230 62 230 98 290 98" fill="none" stroke="{NAVY}" stroke-width="6" stroke-linecap="round"/>'
    b += badge(370, 62, "ok", 24)
    # низ: тройник
    b += f'<path d="M30 202 H70" stroke="{NAVY}" stroke-width="6" stroke-linecap="round"/>'
    b += f'<rect x="70" y="180" width="170" height="44" rx="14" fill="{PAPER}" stroke="{LINE}" stroke-width="2"/>'
    for cx in (105, 155, 205):
        b += f'<circle cx="{cx}" cy="202" r="13" fill="none" stroke="{LINE}" stroke-width="2"/><circle cx="{cx-4}" cy="202" r="2.5" fill="{GRAY}"/><circle cx="{cx+4}" cy="202" r="2.5" fill="{GRAY}"/>'
    b += f'<path d="M240 202 H290" stroke="{NAVY}" stroke-width="6" stroke-linecap="round"/><rect x="288" y="190" width="40" height="24" rx="8" fill="{NAVY}"/>'
    b += badge(380, 202, "no", 24)
    return svg(426, 264, b)


# ───────────────────────── 2. подготовка ─────────────────────────
def prep(A):
    b = tile(0, 0, 426, 168) + tile(0, 184, 426, 100)
    b += iron(150, 62, 1.25, level=0.6)
    # кувшин
    b += f'<g transform="rotate(-28 90 52)"><path d="M60 20 H112 L106 76 Q105 86 94 86 H78 Q67 86 66 76 Z" fill="#DCE8F4" stroke="{BLUE}" stroke-width="3"/><rect x="62" y="44" width="48" height="30" fill="{BLUE}" opacity=".85"/></g>'
    b += f'<path d="M142 78 C152 100 168 108 176 120" fill="none" stroke="{BLUE}" stroke-width="5" stroke-linecap="round" stroke-dasharray="1 9"/>'
    b += f'<path d="M142 78 C150 90 162 98 170 108" fill="none" stroke="{BLUE}" stroke-width="3" stroke-linecap="round"/>'
    # индикатор + регулятор
    b += f'<circle cx="86" cy="234" r="26" fill="{AMBER}"/><circle cx="86" cy="234" r="15" fill="#fff" opacity=".55"/>'
    for a in range(0, 360, 45):
        b += f'<line x1="86" y1="234" x2="86" y2="194" stroke="{AMBER}" stroke-width="4" stroke-linecap="round" transform="rotate({a} 86 234) translate(0 -3)" opacity=".0"/>'
    b += f'<circle cx="86" cy="234" r="34" fill="none" stroke="{AMBER}" stroke-width="3" stroke-dasharray="4 7"/>'
    b += f'<circle cx="300" cy="234" r="38" fill="{PAPER}" stroke="{LINE}" stroke-width="2"/>'
    for a in range(-120, 121, 40):
        b += f'<line x1="300" y1="198" x2="300" y2="204" stroke="{GRAY}" stroke-width="3" stroke-linecap="round" transform="rotate({a} 300 234)"/>'
    b += f'<path d="M300 234 L300 208" stroke="{TERRA}" stroke-width="5" stroke-linecap="round" transform="rotate(40 300 234)"/><circle cx="300" cy="234" r="6" fill="{NAVY}"/>'
    return svg(426, 284, b)


# ───────────────────────── 3. температуры ─────────────────────────
def temps(A):
    b = tile(0, 0, 426, 230)
    segs = ((20, BLUE, 1, "110°"), (150, YEL, 2, "150°"), (280, TERRA, 3, "200°"))
    for x, col, n, lab in segs:
        b += f'<rect x="{x}" y="92" width="126" height="46" rx="12" fill="{col}"/>'
        for i in range(n):
            b += f'<circle cx="{x + 63 + (i - (n-1)/2) * 22}" cy="115" r="7" fill="{NAVY if col != TERRA else "#fff"}"/>'
        b += f'<text x="{x + 63}" y="170" text-anchor="middle" font-weight="800" font-size="20" fill="{NAVY}">{lab}</text>'
    b += f'<path d="M30 40 H380" stroke="{TERRA}" stroke-width="4" stroke-linecap="round"/><path d="M366 28 L384 40 L366 52" fill="none" stroke="{TERRA}" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>'
    b += wave(32, 200, 3, color=BLUE, up=-7) + wave(172, 200, 5, color="#C79A2E", up=-9) + wave(302, 200, 7, color=TERRA, up=-12)
    return svg(426, 230, b)


# ───────────────────────── 4. устройство ─────────────────────────
def inside(A):
    res, gen, ten, sole = A["inside"]
    b = tile(0, 0, 426, 236)
    b += f'<path d="M36 176 H384 Q408 176 398 152 L352 84 Q338 62 312 62 H116 Q46 62 36 130 Z" fill="{PAPER}" stroke="{NAVY}" stroke-width="4" stroke-linejoin="round"/>'
    b += f'<path d="M110 62 C112 14 292 10 330 62 L304 62 C286 36 146 36 134 62 Z" fill="{NAVY2}"/>'
    b += f'<rect x="96" y="78" width="120" height="50" rx="9" fill="#DCE8F4"/><rect x="96" y="98" width="120" height="30" rx="9" fill="{BLUE}"/>'
    b += f'<path d="M96 100 q15 -9 30 0 t30 0 t30 0 t30 0" fill="none" stroke="#fff" stroke-width="2.5" opacity=".7"/>'
    b += f'<rect x="236" y="82" width="64" height="46" rx="9" fill="{AMBER}"/><path d="M252 112 q8 -12 0 -22 M268 112 q8 -12 0 -22 M284 112 q8 -12 0 -22" fill="none" stroke="{NAVY}" stroke-width="3" stroke-linecap="round"/>'
    b += f'<path d="M70 150 l16 -12 l16 12 l16 -12 l16 12 l16 -12 l16 12 l16 -12 l16 12 l16 -12 l16 12 l16 -12 l16 12 l16 -12 l16 12" fill="none" stroke="{TERRA}" stroke-width="5" stroke-linejoin="round" stroke-linecap="round"/>'
    b += f'<rect x="30" y="170" width="362" height="14" rx="7" fill="{NAVY}"/>'
    for x in range(70, 360, 36):
        b += f'<circle cx="{x}" cy="177" r="2.8" fill="{CREAM}"/>'
    b += wave(60, 204, 4, color="#7F93B8", up=-7) + wave(190, 204, 4, color="#7F93B8", up=-7) + wave(310, 204, 3, color="#7F93B8", up=-7)
    # легенда
    items = ((20, 258, BLUE, res), (216, 258, AMBER, gen), (20, 286, TERRA, ten), (216, 286, NAVY, sole))
    for x, y, c, t in items:
        b += f'<circle cx="{x+9}" cy="{y-6}" r="8" fill="{c}"/><text x="{x+26}" y="{y}" font-size="16.5" font-weight="700" fill="{NAVY}">{t}</text>'
    return svg(426, 296, b)


# ───────────────────────── 5. плечики ─────────────────────────
def hanger(A):
    b = tile(0, 0, 426, 290)
    b += f'<path d="M150 50 V36 a10 10 0 1 1 10 10" fill="none" stroke="{NAVY}" stroke-width="4" stroke-linecap="round"/>'
    b += f'<path d="M150 50 L52 104 H248 Z" fill="none" stroke="{NAVY}" stroke-width="4" stroke-linejoin="round"/>'
    b += f'<path d="M72 100 L36 146 L60 160 L82 132 V260 H218 V132 L240 160 L264 146 L228 100 Q150 118 72 100Z" fill="{BLUE}"/>'
    b += f'<path d="M150 112 V260" stroke="#5B7BA6" stroke-width="2.5" stroke-dasharray="6 6"/>'
    # утюг справа, носик к вещи
    b += iron(236, 168, 0.95, flip=True, level=0.6)
    b += wave(228, 160, 2, color="#7F93B8", up=-7) + wave(228, 186, 2, color="#7F93B8", up=-7) + wave(228, 212, 2, color="#7F93B8", up=-7)
    # рука тянет край влево
    b += f'<path d="M100 234 H22" stroke="{TERRA}" stroke-width="4.5" stroke-linecap="round"/><path d="M36 222 L20 234 L36 246" fill="none" stroke="{TERRA}" stroke-width="4.5" stroke-linecap="round" stroke-linejoin="round"/>'
    return svg(426, 290, b)


# ───────────────────────── 6. нельзя ─────────────────────────
def nogo(A):
    b = tile(0, 0, 426, 230)
    sw = ((20, YEL), (150, BLUE), (280, PURPLE))
    for (x, c), lab in zip(sw, A["nogo"]):
        b += f'<rect x="{x}" y="34" width="126" height="106" rx="12" fill="{c}"/>'
        b += f'<path d="M{x+14} 126 L{x+60} 46 M{x+40} 130 L{x+86} 50 M{x+66} 134 L{x+112} 54" stroke="#fff" stroke-width="5" opacity=".22" stroke-linecap="round"/>'
        b += badge(x + 110, 38, "no", 18)
        b += f'<text x="{x + 63}" y="178" text-anchor="middle" font-weight="800" font-size="17" fill="{NAVY}">{lab}</text>'
    b += wave(40, 206, 5, color=TERRA, up=-8) + wave(170, 206, 5, color=TERRA, up=-8) + wave(300, 206, 5, color=TERRA, up=-8)
    return svg(426, 230, b)


# ───────────────────────── 7. сухая глажка ─────────────────────────
def dry(A):
    b = tile(0, 0, 426, 240)
    b += iron(26, 66, 1.3, level=0.0)
    b += wave(40, 214, 6, color=TERRA, up=-9)
    b += f'<circle cx="352" cy="96" r="44" fill="{PAPER}" stroke="{LINE}" stroke-width="2"/>'
    b += f'<path d="M352 66 C352 66 330 94 330 106 a22 22 0 0 0 44 0 C374 94 352 66 352 66Z" fill="{BLUE}"/>'
    b += f'<path d="M322 66 L382 126" stroke="{TERRA}" stroke-width="7" stroke-linecap="round"/>'
    return svg(426, 240, b)


# ───────────────────────── 8. подошва ─────────────────────────
def sole(A):
    clean, clogged = A["sole"]
    b = tile(0, 0, 426, 260)

    def one(cx, bad):
        o = f'<path d="M{cx} 22 Q{cx+78} 70 {cx+72} 188 Q{cx} 214 {cx-72} 188 Q{cx-78} 70 {cx} 22Z" fill="#D5DAE5" stroke="{NAVY}" stroke-width="3.5"/>'
        pts = [(cx, 70), (cx-24, 98), (cx+24, 98), (cx-40, 130), (cx, 130), (cx+40, 130), (cx-30, 162), (cx+30, 162), (cx, 176)]
        for i, (x, y) in enumerate(pts):
            o += f'<ellipse cx="{x}" cy="{y}" rx="7" ry="9" fill="{NAVY}"/>'
            if bad and i % 2 == 0:
                o += f'<ellipse cx="{x}" cy="{y}" rx="9" ry="11" fill="{PAPER}" stroke="{AMBER}" stroke-width="3"/>'
            elif bad:
                o += f'<ellipse cx="{x}" cy="{y}" rx="7" ry="9" fill="{PAPER}"/>'
        return o

    b += one(108, False) + one(318, True)
    b += f'<text x="108" y="246" text-anchor="middle" font-weight="800" font-size="17" fill="{NAVY}">{clean}</text>'
    b += f'<text x="318" y="246" text-anchor="middle" font-weight="800" font-size="17" fill="{NAVY}">{clogged}</text>'
    return svg(426, 260, b)


# ───────────────────────── 9. ВТО ─────────────────────────
def vto(A):
    lab = A["vto"]
    b = ""
    for k in range(3):
        y = k * 108
        b += tile(0, y, 426, 98)
        b += f'<text x="18" y="{y+24}" font-weight="800" font-size="15.5" fill="{TERRA}" letter-spacing=".5">{lab[k]}</text>'
        cy = y + 54
        b += f'<rect x="60" y="{cy}" width="150" height="12" fill="{BLUE}"/><rect x="210" y="{cy}" width="150" height="12" fill="{YEL}"/>'
        if k == 0:   # оба припуска в одну сторону
            b += f'<rect x="210" y="{cy+12}" width="60" height="12" fill="{BLUE}"/><rect x="210" y="{cy+24}" width="60" height="12" fill="{YEL}"/>'
            b += f'<path d="M180 {y+22} H250" stroke="{TERRA}" stroke-width="4" stroke-linecap="round"/><path d="M238 {y+14} L252 {y+22} L238 {y+30}" fill="none" stroke="{TERRA}" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>'
        elif k == 1:  # в разные стороны
            b += f'<rect x="150" y="{cy+12}" width="60" height="12" fill="{BLUE}"/><rect x="210" y="{cy+12}" width="60" height="12" fill="{YEL}"/>'
            b += f'<path d="M205 {y+22} H160" stroke="{TERRA}" stroke-width="4" stroke-linecap="round"/><path d="M172 {y+14} L158 {y+22} L172 {y+30}" fill="none" stroke="{TERRA}" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>'
            b += f'<path d="M215 {y+22} H260" stroke="{TERRA}" stroke-width="4" stroke-linecap="round"/><path d="M248 {y+14} L262 {y+22} L248 {y+30}" fill="none" stroke="{TERRA}" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>'
        else:         # приутюжить — сплющено, давление сверху
            b += f'<rect x="170" y="{y+14}" width="80" height="16" rx="6" fill="{NAVY}"/><path d="M210 {y+32} V{y+46}" stroke="{TERRA}" stroke-width="4" stroke-linecap="round"/><path d="M202 {y+40} L210 {y+48} L218 {y+40}" fill="none" stroke="{TERRA}" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>'
        b += f'<path d="M210 {cy-8} V{cy+44}" stroke="{TERRA}" stroke-width="2.5" stroke-dasharray="5 4"/>'
    return svg(426, 314, b)
