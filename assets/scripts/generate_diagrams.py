#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成吉他学习知识库所需的 SVG 图示:
- 基础和弦图(C/G/D/Em/Am/E/A/Dm/F/Fmaj7)
- 强力和弦指型图
- 全指板自然音名图
- A 小调五声音阶盒子图
- 吉他部件标注图
- 扫弦方向示意图

SVG 为矢量+文本格式,GitHub 原生渲染,可版本管理,无需外部图床。
运行: python3 assets/scripts/generate_diagrams.py
"""
import os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.normpath(os.path.join(HERE, "..", "images"))
os.makedirs(OUT, exist_ok=True)

# 配色(在 GitHub 亮/暗主题下都清晰:白底+深色描边)
BG = "#ffffff"
LINE = "#2b2b2b"
DOT = "#1f6feb"
ROOT = "#d1242f"
TEXT = "#2b2b2b"
MUTE = "#8b8b8b"


def save(name, svg):
    path = os.path.join(OUT, name)
    with open(path, "w", encoding="utf-8") as f:
        f.write(svg)
    print("wrote", os.path.relpath(path, os.path.join(HERE, "..", "..")))


# ---------------------------------------------------------------------------
# 和弦图
# frets: 6 个值,索引 0..5 = 第6弦(低E)..第1弦(高e);-1=X(不弹),0=空弦,n=品
# fingers: 6 个值,1食2中3无名4小指,0/None=空弦或不标
# barre: (fret, from_idx, to_idx) 横按,可为 None
# ---------------------------------------------------------------------------
def chord_svg(name, frets, fingers, barre=None, base_fret=1):
    W, H = 200, 240
    left, top = 34, 56
    n_str, n_fret = 6, 5
    sw = 124 / (n_str - 1)      # 弦间距
    fh = 150 / n_fret           # 品间距
    right = left + (n_str - 1) * sw
    bottom = top + n_fret * fh

    def sx(i):  # 弦 i 的 x 坐标(0=6弦在左)
        return left + i * sw

    def fy(f):  # 第 f 根品丝的 y
        return top + f * fh

    parts = []
    parts.append(
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" '
        f'font-family="Helvetica,Arial,sans-serif">')
    parts.append(f'<rect width="{W}" height="{H}" fill="{BG}"/>')
    # 标题
    parts.append(
        f'<text x="{W/2}" y="28" font-size="26" font-weight="bold" '
        f'text-anchor="middle" fill="{TEXT}">{name}</text>')

    # 起始品标注(高把位)
    nut_is_top = base_fret == 1
    if not nut_is_top:
        parts.append(
            f'<text x="{left-14}" y="{fy(0)+fh/1.4:.1f}" font-size="14" '
            f'text-anchor="middle" fill="{TEXT}">{base_fret}fr</text>')

    # 弦(竖线),低音弦更粗
    for i in range(n_str):
        wdt = 2.4 - i * 0.28
        parts.append(
            f'<line x1="{sx(i):.1f}" y1="{top}" x2="{sx(i):.1f}" y2="{bottom:.1f}" '
            f'stroke="{LINE}" stroke-width="{wdt:.2f}"/>')
    # 品丝(横线)
    for f in range(n_fret + 1):
        wdt = 6 if (f == 0 and nut_is_top) else 1.6  # 顶部弦枕加粗
        parts.append(
            f'<line x1="{left}" y1="{fy(f):.1f}" x2="{right:.1f}" y2="{fy(f):.1f}" '
            f'stroke="{LINE}" stroke-width="{wdt}"/>')

    # 横按
    if barre:
        bf, a, b = barre
        y = top + (bf - 0.5) * fh
        parts.append(
            f'<rect x="{sx(a)-9:.1f}" y="{y-9:.1f}" width="{sx(b)-sx(a)+18:.1f}" '
            f'height="18" rx="9" fill="{DOT}"/>')

    # X / O(弦顶状态)
    for i in range(n_str):
        v = frets[i]
        if v == -1:
            parts.append(
                f'<text x="{sx(i):.1f}" y="{top-8}" font-size="16" '
                f'text-anchor="middle" fill="{MUTE}">✕</text>')
        elif v == 0:
            parts.append(
                f'<circle cx="{sx(i):.1f}" cy="{top-13}" r="6" fill="none" '
                f'stroke="{LINE}" stroke-width="1.6"/>')

    # 手指点
    for i in range(n_str):
        v = frets[i]
        if v and v > 0:
            rel = v - base_fret + 1
            cy = top + (rel - 0.5) * fh
            # 横按覆盖的点不重复画大圆,但画手指数字
            covered = barre and barre[0] == rel and barre[1] <= i <= barre[2]
            if not covered:
                parts.append(
                    f'<circle cx="{sx(i):.1f}" cy="{cy:.1f}" r="9" fill="{DOT}"/>')
            fg = fingers[i]
            if fg:
                parts.append(
                    f'<text x="{sx(i):.1f}" y="{cy+5:.1f}" font-size="13" '
                    f'font-weight="bold" text-anchor="middle" fill="#fff">{fg}</text>')

    # 底部弦名
    names = ["E", "A", "D", "G", "B", "e"]
    for i in range(n_str):
        parts.append(
            f'<text x="{sx(i):.1f}" y="{bottom+20:.1f}" font-size="12" '
            f'text-anchor="middle" fill="{MUTE}">{names[i]}</text>')

    parts.append("</svg>")
    return "\n".join(parts)


CHORDS = {
    "C":     ([-1, 3, 2, 0, 1, 0], [None, 3, 2, None, 1, None], None, 1),
    "G":     ([3, 2, 0, 0, 0, 3], [2, 1, None, None, None, 3], None, 1),
    "D":     ([-1, -1, 0, 2, 3, 2], [None, None, None, 1, 3, 2], None, 1),
    "Em":    ([0, 2, 2, 0, 0, 0], [None, 2, 3, None, None, None], None, 1),
    "Am":    ([-1, 0, 2, 2, 1, 0], [None, None, 2, 3, 1, None], None, 1),
    "E":     ([0, 2, 2, 1, 0, 0], [None, 2, 3, 1, None, None], None, 1),
    "A":     ([-1, 0, 2, 2, 2, 0], [None, None, 1, 2, 3, None], None, 1),
    "Dm":    ([-1, -1, 0, 2, 3, 1], [None, None, None, 2, 3, 1], None, 1),
    "F":     ([1, 3, 3, 2, 1, 1], [1, 3, 4, 2, 1, 1], (1, 0, 5), 1),
    "Fmaj7": ([-1, -1, 3, 2, 1, 0], [None, None, 3, 2, 1, None], None, 1),
}

for nm, (fr, fg, ba, bf) in CHORDS.items():
    save(f"chord-{nm}.svg", chord_svg(nm, fr, fg, ba, bf))


# ---------------------------------------------------------------------------
# 强力和弦指型(根音在 6 弦,以 G5 为例:6弦3品 + 5弦5品 + 4弦5品)
# ---------------------------------------------------------------------------
save("powerchord-E.svg",
     chord_svg("G5", [3, 5, 5, -1, -1, -1], [1, 3, 4, None, None, None], None, 3))
save("powerchord-A.svg",
     chord_svg("C5", [-1, 3, 5, 5, -1, -1], [None, 1, 3, 4, None, None], None, 3))


# ---------------------------------------------------------------------------
# 全指板自然音名图(前 12 品)
# ---------------------------------------------------------------------------
def fretboard_svg():
    string_names = ["e", "B", "G", "D", "A", "E"]  # 上到下:1弦..6弦
    # 各弦从空弦起每品音名(自然音用本名,升音用 #)
    chromatic = ["E", "F", "F#", "G", "G#", "A", "A#", "B", "C", "C#", "D", "D#"]

    def note_at(open_note, fret):
        idx = (chromatic.index(open_note) + fret) % 12
        return chromatic[idx]

    open_notes = ["E", "B", "G", "D", "A", "E"]  # 1..6 弦空弦
    n_fret = 12
    left, top = 60, 40
    fw, sh = 66, 34
    W = left + n_fret * fw + 30
    H = top + 6 * sh + 50

    p = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" '
         f'font-family="Helvetica,Arial,sans-serif">',
         f'<rect width="{W}" height="{H}" fill="{BG}"/>',
         f'<text x="{W/2}" y="24" font-size="18" font-weight="bold" '
         f'text-anchor="middle" fill="{TEXT}">指板自然音名图(前 12 品)</text>']

    # 品位记号
    markers = [3, 5, 7, 9, 12]
    for m in markers:
        x = left + (m - 0.5) * fw
        p.append(f'<text x="{x:.1f}" y="{top-6}" font-size="12" '
                 f'text-anchor="middle" fill="{MUTE}">{m}</text>')

    # 弦线
    for s in range(6):
        y = top + s * sh + sh / 2
        p.append(f'<line x1="{left}" y1="{y:.1f}" x2="{left+n_fret*fw}" y2="{y:.1f}" '
                 f'stroke="{LINE}" stroke-width="{0.8+s*0.25:.2f}"/>')
        p.append(f'<text x="{left-16}" y="{y+4:.1f}" font-size="13" '
                 f'text-anchor="middle" fill="{TEXT}">{string_names[s]}</text>')
    # 品丝
    for f in range(n_fret + 1):
        x = left + f * fw
        wdt = 6 if f == 0 else 1.4
        p.append(f'<line x1="{x}" y1="{top+sh/2:.1f}" x2="{x}" y2="{top+6*sh-sh/2:.1f}" '
                 f'stroke="{LINE}" stroke-width="{wdt}"/>')

    # 音名圆点
    for s in range(6):
        for f in range(1, n_fret + 1):
            note = note_at(open_notes[s], f)
            x = left + (f - 0.5) * fw
            y = top + s * sh + sh / 2
            is_natural = "#" not in note
            fill = ROOT if note in ("E",) and s in (0, 5) else (DOT if is_natural else "#9aa0a6")
            r = 12 if is_natural else 10
            p.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{fill}"/>')
            p.append(f'<text x="{x:.1f}" y="{y+4:.1f}" font-size="11" font-weight="bold" '
                     f'text-anchor="middle" fill="#fff">{note}</text>')

    p.append(f'<text x="{left}" y="{H-14}" font-size="11" fill="{MUTE}">'
             f'蓝=自然音  灰=升降音  红=E(1弦/6弦同名)</text>')
    p.append("</svg>")
    return "\n".join(p)


save("fretboard-notes.svg", fretboard_svg())


# ---------------------------------------------------------------------------
# A 小调五声音阶第一把位盒子(5-8 品)
# ---------------------------------------------------------------------------
def pentatonic_box_svg():
    # (弦索引0=6弦..5=1弦, 品)  A小调五声 box1
    # 6弦:5,8 / 5弦:5,7 / 4弦:5,7 / 3弦:5,7 / 2弦:5,8 / 1弦:5,8
    dots = [
        (0, 5, True), (0, 8, False),
        (1, 5, False), (1, 7, True),
        (2, 5, False), (2, 7, False),
        (3, 5, False), (3, 7, False),
        (4, 5, False), (4, 8, False),
        (5, 5, True), (5, 8, False),
    ]
    start, span = 5, 4  # 显示 5..8 品
    string_names = ["E", "A", "D", "G", "B", "e"]  # 6..1
    left, top = 56, 56
    sw, fh = 46, 56
    W = left + span * fh + 30
    H = top + 5 * sw + 60

    p = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" '
         f'font-family="Helvetica,Arial,sans-serif">',
         f'<rect width="{W}" height="{H}" fill="{BG}"/>',
         f'<text x="{W/2}" y="26" font-size="17" font-weight="bold" '
         f'text-anchor="middle" fill="{TEXT}">A 小调五声 · 第一把位(5–8 品)</text>']

    # 横线=弦(6弦在下),这里画 6 根弦水平
    for s in range(6):
        y = top + s * sw
        p.append(f'<line x1="{left}" y1="{y}" x2="{left+span*fh}" y2="{y}" '
                 f'stroke="{LINE}" stroke-width="{2.0-s*0.22:.2f}"/>')
    # 竖线=品丝
    for f in range(span + 1):
        x = left + f * fh
        p.append(f'<line x1="{x}" y1="{top}" x2="{x}" y2="{top+5*sw}" '
                 f'stroke="{LINE}" stroke-width="1.4"/>')
        if f < span:
            p.append(f'<text x="{x+fh/2:.1f}" y="{top+5*sw+24:.1f}" font-size="12" '
                     f'text-anchor="middle" fill="{MUTE}">{start+f}</text>')
    # 弦名(顶部对应,1弦e在上还是下?这里 s=0 顶部画成 6弦E)
    names_top = ["E", "A", "D", "G", "B", "e"]
    for s in range(6):
        y = top + s * sw
        p.append(f'<text x="{left-16}" y="{y+4:.1f}" font-size="12" '
                 f'text-anchor="middle" fill="{TEXT}">{names_top[s]}</text>')

    # 点
    for (s, fret, is_root) in dots:
        # s: 0=6弦 -> 顶部 y; 品 fret 落在 (fret-start) 区间中点
        y = top + s * sw
        x = left + (fret - start + 0.5) * fh
        col = ROOT if is_root else DOT
        p.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="13" fill="{col}"/>')
        if is_root:
            p.append(f'<text x="{x:.1f}" y="{y+4:.1f}" font-size="11" font-weight="bold" '
                     f'text-anchor="middle" fill="#fff">A</text>')

    p.append(f'<text x="{left}" y="{H-14}" font-size="11" fill="{MUTE}">'
             f'红=根音 A  蓝=音阶其他音</text>')
    p.append("</svg>")
    return "\n".join(p)


save("pentatonic-Am-box1.svg", pentatonic_box_svg())


# ---------------------------------------------------------------------------
# 吉他部件标注图(原声吉他简化示意)
# ---------------------------------------------------------------------------
def guitar_parts_svg():
    W, H = 760, 320
    p = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" '
         f'font-family="Helvetica,Arial,sans-serif">',
         f'<rect width="{W}" height="{H}" fill="{BG}"/>',
         f'<text x="{W/2}" y="26" font-size="18" font-weight="bold" '
         f'text-anchor="middle" fill="{TEXT}">原声吉他部件示意图</text>']

    body = "#e8c79a"
    edge = "#9c6b2f"
    # 琴体
    p.append(f'<ellipse cx="600" cy="180" rx="110" ry="95" fill="{body}" stroke="{edge}" stroke-width="3"/>')
    p.append(f'<ellipse cx="520" cy="180" rx="70" ry="78" fill="{body}" stroke="{edge}" stroke-width="3"/>')
    p.append(f'<rect x="450" y="150" width="160" height="60" fill="{body}"/>')
    # 音孔
    p.append(f'<circle cx="560" cy="180" r="34" fill="#3b2a16"/>')
    p.append(f'<circle cx="560" cy="180" r="34" fill="none" stroke="{edge}" stroke-width="3"/>')
    # 琴桥
    p.append(f'<rect x="600" y="195" width="44" height="14" rx="3" fill="#3b2a16"/>')
    # 琴颈
    p.append(f'<rect x="150" y="166" width="330" height="28" fill="#5a3d22"/>')
    # 品丝
    for i in range(8):
        x = 180 + i * 36
        p.append(f'<line x1="{x}" y1="166" x2="{x}" y2="194" stroke="#cfcfcf" stroke-width="2"/>')
    # 琴头
    p.append(f'<rect x="110" y="150" width="48" height="60" rx="6" fill="#5a3d22"/>')
    for i in range(3):
        p.append(f'<circle cx="120" cy="{162+i*16}" r="4" fill="#d9d9d9"/>')
        p.append(f'<circle cx="148" cy="{162+i*16}" r="4" fill="#d9d9d9"/>')
    # 弦
    for i in range(6):
        y = 169 + i * 4.6
        p.append(f'<line x1="158" y1="{y:.1f}" x2="622" y2="{200}" stroke="#bbb" stroke-width="0.8"/>')

    # 标注
    labels = [
        (134, 130, "琴头 Headstock", 110, 150),
        (134, 240, "弦钮 Tuners", 130, 178),
        (250, 130, "琴颈/指板 Neck", 300, 166),
        (250, 240, "品丝 Frets", 250, 194),
        (560, 110, "音孔 Soundhole", 560, 146),
        (660, 110, "琴身 Body", 660, 150),
        (640, 250, "琴桥 Bridge", 622, 205),
    ]
    for tx, ty, txt, lx, ly in labels:
        p.append(f'<line x1="{tx}" y1="{ty}" x2="{lx}" y2="{ly}" stroke="{MUTE}" stroke-width="1"/>')
        p.append(f'<text x="{tx}" y="{ty-4}" font-size="13" text-anchor="middle" fill="{TEXT}">{txt}</text>')

    p.append("</svg>")
    return "\n".join(p)


save("guitar-parts.svg", guitar_parts_svg())


# ---------------------------------------------------------------------------
# 扫弦方向示意图(万能扫弦型 ↓ ↓↑ ↑↓↑)
# ---------------------------------------------------------------------------
def strum_svg():
    W, H = 560, 160
    pattern = [("↓", "1"), ("", "&"), ("↓", "2"), ("↑", "&"),
               ("", "3"), ("↑", "&"), ("↓", "4"), ("↑", "&")]
    p = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" '
         f'font-family="Helvetica,Arial,sans-serif">',
         f'<rect width="{W}" height="{H}" fill="{BG}"/>',
         f'<text x="{W/2}" y="28" font-size="17" font-weight="bold" '
         f'text-anchor="middle" fill="{TEXT}">万能扫弦型 ↓ ↓↑ ↑↓↑</text>']
    n = len(pattern)
    left, step = 50, (W - 100) / (n - 1)
    for i, (arrow, beat) in enumerate(pattern):
        x = left + i * step
        if arrow == "↓":
            p.append(f'<text x="{x:.0f}" y="86" font-size="40" text-anchor="middle" fill="{DOT}">↓</text>')
        elif arrow == "↑":
            p.append(f'<text x="{x:.0f}" y="86" font-size="40" text-anchor="middle" fill="{ROOT}">↑</text>')
        else:
            p.append(f'<text x="{x:.0f}" y="80" font-size="22" text-anchor="middle" fill="{MUTE}">·</text>')
        p.append(f'<text x="{x:.0f}" y="120" font-size="15" text-anchor="middle" fill="{TEXT}">{beat}</text>')
    p.append(f'<text x="{W/2}" y="146" font-size="12" text-anchor="middle" fill="{MUTE}">'
             f'蓝↓=下扫  红↑=上扫  ·=右手摆动但不触弦(保持持续律动)</text>')
    p.append("</svg>")
    return "\n".join(p)


save("strum-universal.svg", strum_svg())

print("\nAll diagrams generated to", OUT)


# ---------------------------------------------------------------------------
# 坐姿示意图(简化人形 + 吉他,标注要点)
# ---------------------------------------------------------------------------
def posture_svg():
    W, H = 460, 360
    skin = "#e8b88a"
    cloth = "#3a6ea5"
    body = "#e8c79a"
    edge = "#9c6b2f"
    p = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" '
         f'font-family="Helvetica,Arial,sans-serif">',
         f'<rect width="{W}" height="{H}" fill="{BG}"/>',
         f'<text x="{W/2}" y="26" font-size="17" font-weight="bold" '
         f'text-anchor="middle" fill="{TEXT}">民谣/电吉他 基本坐姿(示意)</text>']
    # 椅子
    p.append(f'<rect x="150" y="250" width="120" height="12" fill="#888"/>')
    p.append(f'<rect x="155" y="262" width="8" height="70" fill="#888"/>')
    p.append(f'<rect x="258" y="262" width="8" height="70" fill="#888"/>')
    # 躯干(挺直)
    p.append(f'<line x1="210" y1="120" x2="210" y2="250" stroke="{cloth}" stroke-width="26" stroke-linecap="round"/>')
    # 头
    p.append(f'<circle cx="210" cy="100" r="22" fill="{skin}"/>')
    # 大腿(坐着,水平)
    p.append(f'<line x1="210" y1="248" x2="300" y2="250" stroke="{cloth}" stroke-width="22" stroke-linecap="round"/>')
    # 小腿
    p.append(f'<line x1="300" y1="250" x2="305" y2="332" stroke="{cloth}" stroke-width="18" stroke-linecap="round"/>')
    # 吉他琴体(架在右腿上,竖直面)
    p.append(f'<ellipse cx="250" cy="225" rx="46" ry="40" fill="{body}" stroke="{edge}" stroke-width="3"/>')
    p.append(f'<circle cx="250" cy="225" r="14" fill="#3b2a16"/>')
    # 琴颈(略上扬)
    p.append(f'<rect x="95" y="150" width="150" height="16" rx="4" fill="#5a3d22" transform="rotate(-12 245 158)"/>')
    # 左臂(按弦,伸向琴颈)
    p.append(f'<line x1="200" y1="150" x2="120" y2="172" stroke="{skin}" stroke-width="13" stroke-linecap="round"/>')
    # 右臂(搭在琴身上缘拨弦)
    p.append(f'<line x1="215" y1="150" x2="265" y2="205" stroke="{skin}" stroke-width="13" stroke-linecap="round"/>')

    notes = [
        (380, 100, "背挺直,不驼背"),
        (380, 150, "琴颈略上扬"),
        (385, 205, "右小臂搭琴身上缘"),
        (380, 250, "琴腰架右大腿"),
        (110, 130, "左手拇指在颈背"),
        (95, 300, "肩膀放松下沉"),
    ]
    for tx, ty, txt in notes:
        p.append(f'<text x="{tx}" y="{ty}" font-size="12" fill="{ROOT}" '
                 f'text-anchor="{"end" if tx<200 else "start"}">• {txt}</text>')
    p.append(f'<text x="{W/2}" y="{H-8}" font-size="11" text-anchor="middle" fill="{MUTE}">'
             f'示意图,真实姿势请配合视频参考(见 持琴与姿势.md 末尾链接)</text>')
    p.append("</svg>")
    return "\n".join(p)


save("posture-sitting.svg", posture_svg())
