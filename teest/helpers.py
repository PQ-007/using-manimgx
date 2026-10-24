"""Shared look and building blocks for the Nand-to-Tetris chapters."""

import numpy as np

import manimgx as m

# ── palette ─────────────────────────────────────────────────────────────
BG = "#0E1117"
FG = "#E6E8EE"
DIM = "#7A8194"
ON = "#FFB020"  # 1 / асаалттай
OFF = "#3A8DFF"  # 0 / унтраалттай
WIRE = "#4B5263"
CHIP = "#9AA3B5"
HL = "#B794F6"  # highlight for "this is the new idea"

FONT = "Noto Sans"
MONO = "Noto Sans Mono"

m.config.background_color = BG

SAFE_W = 13.0  # widest anything may be, leaving a margin inside the 14.2 frame


def bit_color(b):
    return ON if b else OFF


def T(text, size=36, color=FG, max_w=SAFE_W, **kw):
    """Mongolian-safe text, shrunk to fit if wider than max_w."""
    t = m.Text(text, font=FONT, font_size=size, color=color, **kw)
    if t.width > max_w:
        t.scale_to_fit_width(max_w)
    return t


def Mono(text, size=32, color=FG, **kw):
    return m.Text(text, font=MONO, font_size=size, color=color, **kw)


class ChapterScene(m.Scene):
    """Dark background, a caption line at the bottom, and a chapter title card."""

    def setup(self):
        self.background_color = BG
        self._caption = None

    def title_card(self, num, title, subtitle):
        n = T(f"{num}-р бүлэг", 30, DIM)
        t = T(title, 60)
        s = T(subtitle, 32, HL)
        g = m.VGroup(n, t, s).arrange(m.DOWN, buff=0.35)
        self.play(m.FadeIn(n, shift=0.2 * m.UP), m.Write(t), run_time=1.5)
        self.play(m.FadeIn(s, shift=0.2 * m.UP))
        self.wait(2.5)
        self.play(m.FadeOut(g))

    def caption(self, text, wait=2.5, size=30):
        """Replace the bottom caption; then hold it long enough to read."""
        new = T(text, size, FG, max_w=12.5).to_edge(m.DOWN, buff=0.45)
        if self._caption is None:
            self.play(m.FadeIn(new, shift=0.15 * m.UP), run_time=0.6)
        else:
            self.play(m.FadeOut(self._caption, shift=0.15 * m.UP),
                      m.FadeIn(new, shift=0.15 * m.UP), run_time=0.6)
        self._caption = new
        if wait:
            self.wait(wait)
        return new

    def clear_caption(self):
        if self._caption is not None:
            self.play(m.FadeOut(self._caption), run_time=0.4)
            self._caption = None

    def clear_all(self):
        mobs = [mob for mob in self.mobjects]
        if mobs:
            self.play(*[m.FadeOut(mob) for mob in mobs], run_time=0.7)
        self._caption = None


# ── gate shapes ─────────────────────────────────────────────────────────
H = 1.2  # gate body height
R = H / 2


def _arc(cx, cy, r, a0, a1, n=40):
    return [(cx + r * np.cos(a), cy + r * np.sin(a), 0) for a in np.linspace(a0, a1, n)]


def _bezier(p0, p1, p2, n=30):
    p0, p1, p2 = map(np.array, (p0, p1, p2))
    return [tuple((1 - t) ** 2 * p0 + 2 * (1 - t) * t * p1 + t ** 2 * p2) for t in np.linspace(0, 1, n)]


def _poly(points, color=FG, width=4):
    v = m.VMobject()
    v.set_points_as_corners([np.array((*p[:2], 0), dtype=float) for p in points])
    v.set_stroke(color, width)
    return v


def _pin(x, y):
    return m.Dot((x, y, 0), radius=0.001).set_opacity(0)


class Gate(m.VGroup):
    """A gate symbol whose pins move with it: `in_pt(i)` and `out_pt()`."""

    def __init__(self, kind, label=True, color=FG, scale=1.0):
        super().__init__()
        self.kind = kind
        bubble = kind in ("NAND", "NOT", "NOR")
        if kind in ("AND", "NAND"):
            pts = [(-R, R), (0, R)] + _arc(0, 0, R, np.pi / 2, -np.pi / 2) + [(-R, -R), (-R, R)]
            body = _poly(pts, color)
            tip = R
            ins = [(-R, 0.3), (-R, -0.3)]
        elif kind in ("OR", "XOR", "NOR"):
            back = [(-R + 0.18 * (1 - (y / R) ** 2), y, 0) for y in np.linspace(-R, R, 30)]
            top = _bezier((-R, R, 0), (0.15, R, 0), (0.75, 0, 0))
            bot = _bezier((0.75, 0, 0), (0.15, -R, 0), (-R, -R, 0))
            body = _poly(back + top + bot, color)
            tip = 0.75
            xin = -R + 0.18 * (1 - 0.25)
            ins = [(xin, 0.3), (xin, -0.3)]
            if kind == "XOR":
                extra = _poly([(x - 0.17, y, 0) for x, y, _ in back], color)
                body = m.VGroup(body, extra)
                ins = [(xin - 0.17, 0.3), (xin - 0.17, -0.3)]
        elif kind == "NOT":
            body = _poly([(-0.45, 0.42), (-0.45, -0.42), (0.35, 0), (-0.45, 0.42)], color)
            tip = 0.35
            ins = [(-0.45, 0)]
        else:
            raise ValueError(kind)
        self.body = body
        self.add(body)
        out_x = tip
        if bubble:
            b = m.Circle(radius=0.1, color=color, stroke_width=4).move_to((tip + 0.1, 0, 0))
            self.add(b)
            out_x = tip + 0.2
        self.pins = [_pin(x, y) for x, y in ins]
        self.out_pin = _pin(out_x, 0)
        self.add(*self.pins, self.out_pin)
        if label:
            self.label = T(kind, 20, DIM).next_to(body, m.DOWN, buff=0.12)
            self.add(self.label)
        self.scale(scale)

    def in_pt(self, i=0):
        return self.pins[i].get_center()

    def out_pt(self):
        return self.out_pin.get_center()


# ── wires and signals ───────────────────────────────────────────────────
def wire(*points, color=WIRE, width=4):
    """A wire through the given points, with right-angle corners."""
    return _poly([np.array(p, dtype=float) for p in points], color, width)


def hv(a, b, mid=None):
    """Points for an orthogonal wire from a to b: across, then up/down, then across."""
    a, b = np.array(a, dtype=float), np.array(b, dtype=float)
    if abs(a[1] - b[1]) < 1e-6:
        return [a, b]
    x = (a[0] + b[0]) / 2 if mid is None else mid
    return [a, np.array([x, a[1], 0]), np.array([x, b[1], 0]), b]


def signal(w, bit, run_time=0.6):
    """A colored copy of wire `w` drawn along it: the bit flowing. Returns (anim, overlay)."""
    lit = w.copy().set_stroke(bit_color(bit), w.get_stroke_width() + 2)
    lit.set_z_index(2)
    return m.Create(lit, rate_func=m.linear, run_time=run_time), lit


def BitDot(bit, size=30):
    """A bit value in a colored circle."""
    c = m.Circle(radius=0.28, stroke_color=bit_color(bit), stroke_width=4,
                 fill_color=bit_color(bit), fill_opacity=0.18)
    t = Mono(str(bit), size, bit_color(bit)).move_to(c)
    return m.VGroup(c, t)


def bit_text(bit, size=30):
    return Mono(str(bit), size, bit_color(bit))


def Chip(name, w=2.2, h=1.4, color=CHIP, size=30, label_color=FG):
    box = m.RoundedRectangle(width=w, height=h, corner_radius=0.12, color=color, stroke_width=4)
    box.set_fill(BG, 1)
    lab = T(name, size, label_color).move_to(box)
    if lab.width > w - 0.2:
        lab.scale_to_fit_width(w - 0.2)
    return m.VGroup(box, lab)


# ── truth tables ────────────────────────────────────────────────────────
class TruthTable(m.VGroup):
    """Headers plus empty rows; `cell(r, c)` gives the spot, `fill(...)` the animation."""

    def __init__(self, headers, n_rows, col_w=0.9, row_h=0.55, size=28):
        super().__init__()
        self.col_w, self.row_h, self.size = col_w, row_h, size
        self.n_cols = len(headers)
        self.heads = m.VGroup(*[
            T(h, 26, DIM).move_to((c * col_w, 0, 0)) for c, h in enumerate(headers)
        ])
        x0, x1 = -col_w / 2, (self.n_cols - 0.5) * col_w
        self.rule = m.Line((x0, -row_h / 2, 0), (x1, -row_h / 2, 0), color=WIRE, stroke_width=2)
        last_in = self.n_cols - 2
        xs = (last_in + 0.5) * col_w
        self.sep = m.Line((xs, row_h / 2, 0), (xs, -row_h * (n_rows + 0.5), 0), color=WIRE, stroke_width=2)
        self.slots = [[_pin(c * col_w, -(r + 1) * row_h) for c in range(self.n_cols)] for r in range(n_rows)]
        self.add(self.heads, self.rule, self.sep, *[p for row in self.slots for p in row])
        self.values = m.VGroup()
        self.add(self.values)

    def cell(self, r, c):
        return self.slots[r][c].get_center()

    def fill(self, r, bits, highlight_out=True):
        """Write one row: every value colored by its bit, the output last."""
        cells = []
        for c, b in enumerate(bits):
            t = bit_text(b, self.size).move_to(self.cell(r, c))
            cells.append(t)
            self.values.add(t)
        anims = [m.FadeIn(t, scale=1.3) for t in cells[:-1]]
        out = m.FadeIn(cells[-1], scale=1.6) if highlight_out else m.FadeIn(cells[-1])
        return m.Succession(m.AnimationGroup(*anims), out, run_time=0.8)
