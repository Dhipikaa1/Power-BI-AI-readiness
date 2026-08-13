"""
Builds before/after AI-Readiness scorecards in the same visual style the sempy notebook
renders (scoring/AI_Readiness_Score.ipynb), using the real sample-model scores.

Outputs (docs/images/):
  scorecard-before.html / scorecard-after.html  -> exact browser render (open to view)
  scorecard-before.png  / scorecard-after.png   -> embeddable proof images (PIL)

Dev tool. Run:  py -3 _build_scorecards.py
"""
import os
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
from _run_sempy_scores import score, grade

HERE = os.path.dirname(os.path.abspath(__file__))
IMG = os.path.join(HERE, "docs", "images")
os.makedirs(IMG, exist_ok=True)

NAVY = (47, 84, 150)
GREEN = (46, 204, 113)
ORANGE = (243, 156, 18)
RED = (231, 76, 60)
GREY = (102, 102, 102)
ALT = (242, 242, 242)


def score_color(s):
    if s >= 80:
        return GREEN
    if s >= 60:
        return ORANGE
    return RED


def _font(size, bold=False):
    names = ("segoeuib.ttf", "seguisb.ttf", "arialbd.ttf") if bold else ("segoeui.ttf", "arial.ttf")
    for name in names:
        try:
            return ImageFont.truetype(name, size)
        except OSError:
            continue
    return ImageFont.load_default()


def _center(draw, cx, y, text, font, fill):
    w = draw.textlength(text, font=font)
    draw.text((cx - w / 2, y), text, font=font, fill=fill)


def _hex(c):
    return "#%02x%02x%02x" % c


def card_html(model_label, cats, overall):
    g, color = grade(overall), score_color(overall)
    n = len(cats)
    bars = ""
    for cat, s in cats:
        bars += (f'<div style="width:{99/n:.1f}%;background:{_hex(score_color(s))};'
                 f'height:30px;display:inline-block;text-align:center;color:white;'
                 f'font-size:9px;line-height:30px;overflow:hidden;" '
                 f'title="{cat}: {s:.0f}/100">{cat[:8]}</div>')
    rows = ""
    for i, (cat, s) in enumerate(cats):
        bg = "#f2f2f2" if i % 2 == 0 else "white"
        status = "PASS" if s >= 80 else ("WARN" if s >= 60 else "FAIL")
        rows += (f'<tr style="background:{bg};"><td style="padding:5px;">{i+1}</td>'
                 f'<td style="padding:5px;">{cat}</td>'
                 f'<td style="text-align:center;font-weight:bold;color:{_hex(score_color(s))};">'
                 f'{s:.0f}</td><td style="text-align:center;">{status}</td></tr>')
    return f"""<!doctype html><html><head><meta charset="utf-8">
<style>body{{font-family:Segoe UI,Arial,sans-serif;margin:0;padding:16px;background:#fff;}}</style>
</head><body>
<div style="border:2px solid {_hex(color)};border-radius:12px;padding:20px;margin:10px 0;max-width:900px;">
  <h2 style="color:{_hex(color)};margin:0;">AI Readiness Score: {overall}/100 - Grade {g}</h2>
  <p style="color:#666;">Model: {model_label} | Workspace: Sample</p>
  <p style="color:#666;">Assessed: {datetime.now().strftime('%Y-%m-%d %H:%M')} | {n} categories, each 0-100, simple average</p>
  <div style="background:#eee;border-radius:6px;overflow:hidden;margin:10px 0;">{bars}</div>
  <table style="width:100%;border-collapse:collapse;margin-top:10px;font-size:12px;">
    <tr style="background:#2F5496;color:white;"><th style="text-align:left;padding:6px;">#</th><th style="text-align:left;padding:6px;">Category</th><th style="text-align:center;">Score /100</th><th style="text-align:center;">Status</th></tr>
    {rows}
    <tr style="background:#2F5496;color:white;font-weight:bold;"><td style="padding:6px;"></td><td style="padding:6px;">OVERALL (Average)</td><td style="text-align:center;">{overall:.1f}</td><td style="text-align:center;">{g}</td></tr>
  </table>
</div></body></html>"""


def render_png(model_label, cats, overall, path):
    g, color = grade(overall), score_color(overall)
    pad, inner_w = 20, 860
    card_x, card_y, card_w = 16, 16, inner_w + 2 * pad
    n = len(cats)
    row_h, bar_h = 26, 30

    f_title = _font(24, bold=True)
    f_sub = _font(14)
    f_bar = _font(10)
    f_cell = _font(14)
    f_head = _font(14, bold=True)

    yy = card_y + pad + 40 + 22 + 22 + 12 + bar_h + 12 + 28 + row_h * n + row_h
    card_h = (yy + pad) - card_y
    W, H = card_x + card_w + 16, card_y + card_h + 16

    img = Image.new("RGB", (W, H), "white")
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([card_x, card_y, card_x + card_w, card_y + card_h],
                        radius=12, outline=color, width=2)

    x = card_x + pad
    yy = card_y + pad
    d.text((x, yy), f"AI Readiness Score: {overall}/100 - Grade {g}", font=f_title, fill=color)
    yy += 40
    d.text((x, yy), f"Model: {model_label} | Workspace: Sample", font=f_sub, fill=GREY)
    yy += 22
    d.text((x, yy), f"Assessed: {datetime.now().strftime('%Y-%m-%d %H:%M')} | "
                    f"{n} categories, each 0-100, simple average", font=f_sub, fill=GREY)
    yy += 22 + 12

    seg_w = inner_w / n
    for i, (cat, s) in enumerate(cats):
        bx = x + i * seg_w
        d.rectangle([bx, yy, bx + seg_w, yy + bar_h], fill=score_color(s))
        _center(d, bx + seg_w / 2, yy + bar_h / 2 - 6, cat[:8], f_bar, "white")
    yy += bar_h + 12

    cx_num, cx_cat = x + 8, x + 52
    cx_score, cx_status = x + 560, x + 730
    d.rectangle([x, yy, x + inner_w, yy + 28], fill=NAVY)
    d.text((cx_num, yy + 6), "#", font=f_head, fill="white")
    d.text((cx_cat, yy + 6), "Category", font=f_head, fill="white")
    _center(d, cx_score, yy + 6, "Score /100", f_head, "white")
    _center(d, cx_status, yy + 6, "Status", f_head, "white")
    yy += 28

    for i, (cat, s) in enumerate(cats):
        if i % 2 == 0:
            d.rectangle([x, yy, x + inner_w, yy + row_h], fill=ALT)
        status = "PASS" if s >= 80 else ("WARN" if s >= 60 else "FAIL")
        d.text((cx_num, yy + 5), str(i + 1), font=f_cell, fill=(60, 60, 60))
        d.text((cx_cat, yy + 5), cat, font=f_cell, fill=(60, 60, 60))
        _center(d, cx_score, yy + 5, f"{s:.0f}", f_head, score_color(s))
        _center(d, cx_status, yy + 5, status, f_cell, (60, 60, 60))
        yy += row_h

    d.rectangle([x, yy, x + inner_w, yy + row_h], fill=NAVY)
    d.text((cx_cat, yy + 5), "OVERALL (Average)", font=f_head, fill="white")
    _center(d, cx_score, yy + 5, f"{overall:.1f}", f_head, "white")
    _center(d, cx_status, yy + 5, g, f_head, "white")

    img.save(path)


def build(state, model_label):
    defn = os.path.join(HERE, "sample-model", state,
                        "ContosoRetailMini.SemanticModel", "definition")
    cats, overall = score(defn)
    open(os.path.join(IMG, f"scorecard-{state}.html"), "w", encoding="utf-8").write(
        card_html(model_label, cats, overall))
    render_png(model_label, cats, overall, os.path.join(IMG, f"scorecard-{state}.png"))
    print(f"{state}: {overall} ({grade(overall)})")


if __name__ == "__main__":
    build("before", "ContosoRetailMini (before)")
    build("after", "ContosoRetailMini (after)")
