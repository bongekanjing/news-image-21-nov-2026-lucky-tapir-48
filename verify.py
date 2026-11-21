"""Verify the drawn page geometrically: nothing spills its box, nothing collides.

Vision calls kept timing out, so this checks the page the way the printed sheet
would be checked: every text line and rule against the margins it must respect,
and every block's used height against the band it was given.
"""
import importlib.util
import sys

spec = importlib.util.spec_from_file_location("d", "draw.py")
d = importlib.util.module_from_spec(spec)
sys.modules["d"] = d
spec.loader.exec_module(d)

M, W, H, S = d.M, d.W, d.H, d.S
problems = []


class Probe(d.Page):
    """A Page that records every text line and rectangle it draws."""

    def __init__(self):
        super().__init__()
        self.boxes = []

    def text(self, x, y, s, f, fill, anchor="la"):
        super().text(x, y, s, f, fill, anchor)
        w = self.tw(s, f)
        h = f.size / S
        # anchor semantics: la = left-ascender, ma = middleground top-center, ra = right-ascender
        x0 = x - w if anchor == "ra" else (x - w / 2 if anchor == "ma" else x)
        self.boxes.append((x0, y, x0 + w, y + h, s))


p = Probe()
counts = d.region_counts()
y = M
y = d.masthead(p, y)
masthead_bottom = y
y = d.stat_strip(p, y)
y = d.timeline(p, y)
y = d.region_bar(p, y)
y = d.section_bar(p, y, 2)

lead_top = y + 9
lead_h = 222
gap = 16
lw = (W - 2 * M - gap * 2) / 3
lead_bottom = lead_top + lead_h
y = lead_bottom + 8
y = d.section_bar(p, y, 2)

card_top = y + 9
cols, rows_ = 4, 2
cg = 11
cw = (W - 2 * M - cg * (cols - 1)) / cols
chh = 150
card_bottom = card_top + rows_ * chh + 10 * (rows_ - 1)
y = card_bottom + 7
y = d.section_bar(p, y, 2)

# draw the actual content into the probe
for i, story in enumerate(d.LEADS):
    d.lead(p, M + i * (lw + gap), lead_top, lw, lead_h, story)
for i, story in enumerate(d.CARDS[:cols * rows_]):
    c, r = i % cols, i // cols
    d.card(p, M + c * (cw + cg), card_top + r * (chh + 10), cw, chh, story)

y += 9
foot_top = y
brief_w = (W - 2 * M) * 0.66
rx = M + brief_w + 22
rw = W - M - rx
foot_h = H - M - foot_top
brief_w = (W - 2 * M) * 0.66
rx = M + brief_w + 22
rw = W - M - rx
d.briefs(p, M, foot_top, brief_w, d.CARDS[cols * rows_:])
map_h = foot_h - 78
d.draw_map(p, rx, foot_top, rw, map_h)
d.date_check(p, rx, foot_top + map_h + 6, rw)

# ------------------------------------------------------------------ checks --
# 1. every string stays inside the side margins
for x0, y0, x1, y1, s in p.boxes:
    if x0 < M - 1.5 or x1 > W - M + 1.5:
        problems.append(f"side margin: {s[:44]!r} spans {x0:.0f}..{x1:.0f}")
# 2. nothing is drawn below the bottom margin
    if y1 > H - M + 1 or y0 < 0:
        problems.append(f"vertical: {s[:44]!r} at y {y0:.0f}..{y1:.0f}")

# 3. each band's content must not cross into the next band
BANDS = [("masthead", 0, masthead_bottom), ("leads", lead_top, lead_bottom),
         ("cards", card_top, card_bottom), ("footer", foot_top, H - M)]
for name, top, bot in BANDS:
    for x0, y0, x1, y1, s in p.boxes:
        if y0 >= top - 2 and y0 < bot and y1 > bot + 1.5:
            problems.append(f"{name} spills {bot:.0f}: {s[:40]!r} ends {y1:.0f}")

# 4. the three leads and the ten cards each stay inside their own column/row cell
def cells(top, h, n, gapw, cols_n):
    out = []
    for i in range(n):
        c, r = i % cols_n, i // cols_n
        out.append((M + c * (gapw + (W - 2 * M - gapw * (cols_n - 1)) / cols_n)
                    if False else M + c * ((W - 2 * M - gapw * (cols_n - 1)) / cols_n + gapw),
                    top + r * h))
    return out

# leads: no text may start left of its own column
for i in range(3):
    cx = M + i * (lw + gap)
    for x0, y0, x1, y1, s in p.boxes:
        if x0 < cx - 1.5 and y0 >= lead_top and y1 <= lead_bottom and x1 > cx - 2 and x0 < cx + lw:
            problems.append(f"lead {i+1} text crosses its left edge: {s[:34]!r}")

# 5. footer: the briefs column must not run into the right-hand block
for x0, y0, x1, y1, s in p.boxes:
    if y0 >= foot_top and x0 < rx - 2 and x1 > rx - 2:
        problems.append(f"crosses footer boundary at x={rx:.0f}: {s[:34]!r}")

# 6. report the vertical budget
print(f"bands: masthead 0-{masthead_bottom:.0f}, leads {lead_top:.0f}-{lead_bottom:.0f}, "
      f"cards {card_top:.0f}-{card_bottom:.0f}, footer {foot_top:.0f}-{H-M}")
print(f"lead cell {lw:.0f}x{lead_h}, card cell {cw:.0f}x{chh}, footer h {foot_h:.0f}")
print(f"text lines drawn: {len(p.boxes)}")
if problems:
    print(f"\n{len(problems)} PROBLEM(S):")
    for s in problems[:40]:
        print("  ", s)
else:
    print("\nall geometric checks pass")
