"""建立「海洋保護區專案」團隊規劃簡報（10 頁）。
用法：python tools/build_ocean_deck.py [輸出路徑]"""
import sys
from pathlib import Path

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.util import Inches, Pt

FONT = "微軟正黑體"
NAVY = RGBColor(0x0B, 0x3D, 0x5C)      # 主色
ACCENT = RGBColor(0xF2, 0x9E, 0x4C)    # 強調色（每頁只用一次）
GRAY = RGBColor(0x5A, 0x65, 0x70)
LIGHT = RGBColor(0xF4, 0xF6, 0xF8)
LINE = RGBColor(0xC9, 0xD3, 0xDC)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
SHEET_URL = ("https://docs.google.com/spreadsheets/d/1kwjux4npaHXeMYmDJPR7uiw6roIgY6yz-15H00NJQGg/"
             "edit?gid=2119896583#gid=2119896583")

prs = Presentation()
prs.slide_width, prs.slide_height = Inches(13.333), Inches(7.5)
BLANK = prs.slide_layouts[6]


# ---------- helpers ----------
def new_slide(notes=""):
    s = prs.slides.add_slide(BLANK)
    s.background.fill.solid()
    s.background.fill.fore_color.rgb = WHITE
    if notes:
        s.notes_slide.notes_text_frame.text = notes
    return s


def text(slide, x, y, w, h, lines, size=24, color=GRAY, bold=False, align=PP_ALIGN.LEFT,
         anchor=MSO_ANCHOR.TOP, spacing=6):
    """lines：字串或 (字串, {size,color,bold}) 的清單。"""
    tb = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = anchor
    for i, item in enumerate([lines] if isinstance(lines, str) else lines):
        t, opt = (item, {}) if isinstance(item, str) else item
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = align
        p.space_after = Pt(spacing)
        r = p.add_run()
        r.text = t
        f = r.font
        f.name, f.size = FONT, Pt(opt.get("size", size))
        f.bold = opt.get("bold", bold)
        f.color.rgb = opt.get("color", color)
        if opt.get("link"):
            r.hyperlink.address = opt["link"]
    return tb


def box(slide, x, y, w, h, fill=LIGHT, line=None, shape=MSO_SHAPE.ROUNDED_RECTANGLE, dash=False):
    sh = slide.shapes.add_shape(shape, Inches(x), Inches(y), Inches(w), Inches(h))
    if shape == MSO_SHAPE.ROUNDED_RECTANGLE:
        sh.adjustments[0] = 0.08
    if fill is None:
        sh.fill.background()
    else:
        sh.fill.solid()
        sh.fill.fore_color.rgb = fill
    if line is None:
        sh.line.fill.background()
    else:
        sh.line.color.rgb = line
        sh.line.width = Pt(1.5)
        if dash:
            from pptx.enum.dml import MSO_LINE
            sh.line.dash_style = MSO_LINE.DASH
    sh.shadow.inherit = False
    return sh


def label(shape, lines, size=24, color=NAVY, bold=True, align=PP_ALIGN.CENTER):
    tf = shape.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    for i, item in enumerate([lines] if isinstance(lines, str) else lines):
        t, opt = (item, {}) if isinstance(item, str) else item
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = align
        r = p.add_run()
        r.text = t
        r.font.name, r.font.size = FONT, Pt(opt.get("size", size))
        r.font.bold = opt.get("bold", bold)
        r.font.color.rgb = opt.get("color", color)


def title(slide, t):
    """標題統一位置與大小，下方一條強調色短線（本頁唯一強調色）。"""
    text(slide, 0.6, 0.4, 12.1, 1.0, t, size=40, color=NAVY, bold=True, anchor=MSO_ANCHOR.MIDDLE)
    box(slide, 0.6, 1.45, 1.2, 0.08, fill=ACCENT, shape=MSO_SHAPE.RECTANGLE)


# ---------- p.1 封面 ----------
s = new_slide("封面。專案名稱與比賽名稱待補。")
box(s, 0, 0, 13.333, 7.5, fill=NAVY, shape=MSO_SHAPE.RECTANGLE)
box(s, 0.9, 3.55, 1.6, 0.1, fill=ACCENT, shape=MSO_SHAPE.RECTANGLE)
text(s, 0.9, 1.9, 11.5, 1.6, "【待補：專案名稱】", size=54, color=WHITE, bold=True, anchor=MSO_ANCHOR.BOTTOM)
text(s, 0.9, 3.9, 11.5, 1.2, ["海洋保護區專案｜團隊規劃", ("【待補：比賽名稱、日期】", {"size": 24})],
     size=28, color=WHITE)

# ---------- p.2 專案管理表 ----------
s = new_slide("介紹上一個比賽用過的專案管理表，說明這次也用同樣方式追蹤分工與進度。"
              "表單內容待補（目前無法讀取該試算表）。")
title(s, "我們沿用上次比賽的專案管理表追蹤進度")
ph = box(s, 0.6, 1.9, 7.4, 4.6, fill=LIGHT, line=LINE, dash=True)
label(ph, "【待補：專案管理表截圖】", size=24, color=GRAY, bold=False)
text(s, 8.4, 1.9, 4.3, 4.6, [
    ("上次怎麼用這張表", {"bold": True, "color": NAVY, "size": 28}),
    "【待補】", "【待補】", "【待補】",
], size=24, spacing=14)
text(s, 0.6, 6.7, 12.1, 0.5, [("表單連結：上一個比賽的專案管理表", {"link": SHEET_URL})], size=14)

# ---------- p.3 實地考察 ----------
s = new_slide("先跟大家約一天實地考察，考察完再開始規劃工作分工。日期與地點請大家回覆後確認。")
title(s, "先約一天實地考察，回來再開始規劃工作")
b1 = box(s, 0.6, 1.95, 5.6, 1.6, fill=NAVY)
label(b1, [("① 實地考察", {"size": 32}), ("一天", {"size": 24, "bold": False})], color=WHITE)
arrow = s.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, Inches(6.35), Inches(2.45), Inches(0.6), Inches(0.6))
arrow.fill.solid(); arrow.fill.fore_color.rgb = LINE; arrow.line.fill.background()
b2 = box(s, 7.1, 1.95, 5.6, 1.6, fill=LIGHT, line=NAVY)
label(b2, [("② 規劃工作", {"size": 32}), ("分工與時程", {"size": 24, "bold": False})])
info = box(s, 0.6, 3.95, 12.1, 2.8, fill=LIGHT)
text(s, 1.0, 4.15, 11.3, 2.4, [
    "日期：【待補】",
    "地點：【待補】",
    "集合時間與地點：【待補】",
], size=24, spacing=16, anchor=MSO_ANCHOR.MIDDLE)

# ---------- p.4 甘特圖（先空著） ----------
s = new_slide("甘特圖待實地考察後再規劃，本頁先保留。")
title(s, "工作時程甘特圖（待規劃）")
ph = box(s, 0.6, 1.9, 12.1, 4.9, fill=None, line=LINE, dash=True)
label(ph, "【待補：甘特圖】", size=24, color=GRAY, bold=False)

# ---------- p.5 隊名 ----------
s = new_slide("請每個人設計兩個團隊名稱，下週 11/23（一）一起討論決定。")
title(s, "每人提兩個隊名，11/23 一起決定")
for i, (big, small) in enumerate([("2 個", "每個人提出的隊名數量"), ("11/23（一）", "討論並決定團隊名稱")]):
    x = 0.6 + i * 6.25
    c = box(s, x, 2.1, 5.85, 3.6, fill=LIGHT)
    label(c, [(big, {"size": 60}), (small, {"size": 24, "bold": False, "color": GRAY})])

# ---------- p.6 工作規劃 1 ----------
s = new_slide("第一步：選一個海洋保護區找資料。先釐清保護區的定義，"
              "再以保護區為中心往外擴張，定義要調查的範圍圈，盤點周邊商家、垃圾清運、洋流與天氣。")
title(s, "第一步：選一個海洋保護區，摸清周邊環境")
cx, cy = 3.4, 4.35
for r, fill in [(2.45, LIGHT), (1.65, RGBColor(0xD6, 0xE4, 0xEE))]:
    box(s, cx - r, cy - r, 2 * r, 2 * r, fill=fill, line=LINE, shape=MSO_SHAPE.OVAL)
core = box(s, cx - 0.95, cy - 0.95, 1.9, 1.9, fill=NAVY, shape=MSO_SHAPE.OVAL)
label(core, ["海洋", "保護區"], size=24, color=WHITE)
text(s, cx - 1.2, cy - 1.62, 2.4, 0.5, "範圍圈", size=18, color=NAVY, bold=True, align=PP_ALIGN.CENTER)
text(s, cx - 1.2, cy - 2.42, 2.4, 0.5, "周邊環境", size=18, color=NAVY, bold=True, align=PP_ALIGN.CENTER)
text(s, 6.6, 1.9, 6.1, 5.0, [
    ("釐清定義", {"bold": True, "color": NAVY, "size": 28}),
    "・保護區是什麼意思",
    "・以保護區為中心，往外劃出範圍圈",
    ("盤點周邊", {"bold": True, "color": NAVY, "size": 28}),
    "・周邊商家",
    "・周邊垃圾清運",
    "・洋流、天氣",
], size=24, spacing=10)

# ---------- p.7 工作規劃 2 ----------
s = new_slide("第二步：找出這個海洋保護區的問題，分成垃圾、漁獲、政治三類，"
              "每個議題都要查目前已經有哪些解法。")
title(s, "第二步：找出保護區的問題，以及目前的解法")
for i, name in enumerate(["垃圾問題", "漁獲問題", "政治問題"]):
    c = box(s, 0.6 + i * 4.15, 1.95, 3.8, 2.7, fill=LIGHT)
    label(c, [(f"0{i + 1}", {"size": 24, "color": GRAY}), (name, {"size": 36})])
bar = box(s, 0.6, 5.0, 12.1, 1.5, fill=NAVY)
label(bar, "每個議題都要查：目前的解法是什麼？", size=28, color=WHITE)

# ---------- p.8 工作規劃 3 ----------
s = new_slide("第三步：參考海邊管理做得不錯的國家。說明參考誰、為什麼參考他，"
              "有哪些值得參考的地方，別人這樣做有沒有問題，以及我們目前為什麼沒有這麼做。")
title(s, "第三步：參考海岸管理做得好的國家")
qs = ["參考誰？為什麼參考他？", "有哪些值得參考的點？", "別人這麼做，有沒有問題？", "我們為什麼沒有這麼做？"]
for i, q in enumerate(qs):
    x, y = 0.6 + (i % 2) * 6.25, 1.95 + (i // 2) * 2.55
    c = box(s, x, y, 5.85, 2.25, fill=LIGHT)
    label(c, [(f"Q{i + 1}", {"size": 24, "color": GRAY}), (q, {"size": 28})])

# ---------- p.9 團隊訪談：5 個形容詞 ----------
s = new_slide("請每個人用 5 個形容詞，形容自己的個性和做事風格。")
title(s, "用 5 個形容詞，形容你的個性和做事風格")
for i in range(5):
    x = 0.6 + i * 2.45
    c = box(s, x, 2.3, 2.2, 2.9, fill=LIGHT, line=LINE)
    label(c, [(str(i + 1), {"size": 40}), ("＿＿＿＿", {"size": 24, "bold": False, "color": GRAY})])

# ---------- p.10 團隊訪談（標題） ----------
s = new_slide("團隊訪談。")
box(s, 0, 0, 13.333, 7.5, fill=NAVY, shape=MSO_SHAPE.RECTANGLE)
text(s, 0.9, 2.6, 11.5, 1.6, "團隊訪談", size=54, color=WHITE, bold=True, anchor=MSO_ANCHOR.MIDDLE)
box(s, 0.9, 4.3, 1.6, 0.1, fill=ACCENT, shape=MSO_SHAPE.RECTANGLE)

out = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent / "簡報" / "海洋保護區_團隊規劃.pptx"
prs.save(out)
print(out)
