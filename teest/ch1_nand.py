import numpy as np

import manimgx as m
from helpers import (
    DIM, FG, HL, OFF, ON, WIRE, BitDot, ChapterScene, Gate, Mono, T, TruthTable,
    bit_color, hv, signal, wire,
)

NAND = lambda a, b: int(not (a and b))  # noqa: E731


class Ch1Nand(ChapterScene):
    def construct(self):
        self.title_card(1, "Яагаад яг NAND вэ?", "Ганц хаалга хангалттай")
        self.bits_intro()
        self.nand_table()
        self.build_not()
        self.build_and()
        self.build_or()
        self.summary()

    # ── helpers for driving a circuit ───────────────────────────────────
    def heading(self, text):
        h = T(text, 40).to_edge(m.UP, buff=0.4)
        self.play(m.FadeIn(h, shift=0.2 * m.DOWN))
        return h

    def drive(self, stages, run_time=0.6):
        """Play each stage's (wire, bit) signals together, stage after stage."""
        lit = []
        for stage in stages:
            anims = []
            for w, b in stage:
                a, o = signal(w, b, run_time)
                anims.append(a)
                lit.append(o)
            self.play(*anims)
        return lit

    def put_bits(self, old, spots, bits):
        """Swap the bit badges at `spots` (left of each point) for new values."""
        new = m.VGroup(*[BitDot(b).move_to(p) for p, b in zip(spots, bits)])
        if old is None:
            self.play(m.FadeIn(new, scale=1.3), run_time=0.4)
        else:
            self.play(*[m.FadeTransform(o, n) for o, n in zip(old, new)], run_time=0.4)
        return new

    # ── 1. bits ─────────────────────────────────────────────────────────
    def bits_intro(self):
        h = self.heading("Бүх зүйл битээс эхэлнэ")
        one = m.VGroup(BitDot(1, 44).scale(1.6), T("1 — асаалттай", 34, ON)).arrange(m.RIGHT, buff=0.5)
        zero = m.VGroup(BitDot(0, 44).scale(1.6), T("0 — унтраалттай", 34, OFF)).arrange(m.RIGHT, buff=0.5)
        legend = m.VGroup(one, zero).arrange(m.DOWN, buff=0.7, aligned_edge=m.LEFT).shift(0.3 * m.UP)
        self.caption("Компьютер дахь бүх мэдээлэл бол бит: 0 эсвэл 1.", wait=0)
        self.play(m.LaggedStart(m.FadeIn(one, shift=m.RIGHT), m.FadeIn(zero, shift=m.RIGHT), lag_ratio=0.5))
        self.wait(2.5)
        self.caption("Энэ хоёр өнгийг бүх бүлэгт ашиглана.", 2.5)

        # a row of bits that flicker: data is just many bits
        row = m.VGroup(*[BitDot(b) for b in [1, 0, 1, 1, 0, 0, 1, 0]]).arrange(m.RIGHT, buff=0.2)
        row.next_to(legend, m.DOWN, buff=0.7)
        self.play(m.LaggedStart(*[m.FadeIn(d, scale=1.4) for d in row], lag_ratio=0.1))
        self.caption("Тоо, үсэг, зураг — бүгд л олон битийн цуглуулга.", 3)
        self.play(m.FadeOut(legend), m.FadeOut(row), m.FadeOut(h))

        h = self.heading("Логик хаалга гэж юу вэ?")
        box = m.RoundedRectangle(width=2.4, height=1.6, corner_radius=0.15, color=HL, stroke_width=4)
        q = T("?", 60, HL).move_to(box)
        win1 = wire((-4.5, 0.4, 0), (-1.2, 0.4, 0))
        win2 = wire((-4.5, -0.4, 0), (-1.2, -0.4, 0))
        wout = wire((1.2, 0, 0), (4.5, 0, 0))
        lab_in = T("оролт", 28, DIM).next_to(m.VGroup(win1, win2), m.UP, buff=0.4)
        lab_out = T("гаралт", 28, DIM).next_to(wout, m.UP, buff=0.4)
        self.play(m.Create(box), m.Write(q), m.Create(win1), m.Create(win2), m.Create(wout))
        self.play(m.FadeIn(lab_in), m.FadeIn(lab_out))
        self.caption("Логик хаалга: оролтын битүүдээс нэг гаралтын бит гаргадаг дүрэм.", 0)
        lit = self.drive([[(win1, 1), (win2, 0)], [(wout, 1)]])
        self.wait(2.5)
        self.play(*[m.FadeOut(x) for x in [box, q, win1, win2, wout, lab_in, lab_out, h, *lit]])

    # ── 2. NAND and its truth table ─────────────────────────────────────
    def nand_table(self):
        h = self.heading("NAND хаалга")
        g = Gate("NAND", scale=1.4).move_to((-1.8, 0.4, 0))
        ya, yb = g.in_pt(0)[1], g.in_pt(1)[1]
        wa = wire((-5.2, ya, 0), g.in_pt(0))
        wb = wire((-5.2, yb, 0), g.in_pt(1))
        wo = wire(g.out_pt(), (0.9, g.out_pt()[1], 0))
        la = T("a", 30, DIM).next_to(wa, m.LEFT, buff=1.15)
        lb = T("b", 30, DIM).next_to(wb, m.LEFT, buff=1.15)
        tt = TruthTable(["a", "b", "NAND"], 4, col_w=1.25).move_to((4.3, 0.4, 0))

        self.play(m.Create(g.body), m.FadeIn(g[1:]), run_time=1.2)
        self.play(m.Create(wa), m.Create(wb), m.Create(wo), m.FadeIn(la), m.FadeIn(lb))
        self.caption("NAND = «NOT AND»: AND-ийн яг эсрэг.", 2)
        self.play(m.FadeIn(tt.heads), m.Create(tt.rule), m.Create(tt.sep))

        spots_in = [wa.get_start() + 0.4 * m.LEFT, wb.get_start() + 0.4 * m.LEFT]
        spot_out = wo.get_end() + 0.4 * m.RIGHT
        ins, out = None, None
        captions = [
            "Хоёр оролт 0 бол гаралт 1.",
            "Нэг нь 1 байсан ч гаралт 1 хэвээр.",
            "Нөгөө нь 1 байсан ч мөн адил.",
            "Хоёулаа 1 болоход л гаралт 0 болно!",
        ]
        for r, (a, b) in enumerate([(0, 0), (0, 1), (1, 0), (1, 1)]):
            o = NAND(a, b)
            if r < 2 or r == 3:
                self.caption(captions[r], 0)
            ins = self.put_bits(ins, spots_in, [a, b])
            lit = self.drive([[(wa, a), (wb, b)]], 0.5)
            self.play(m.Indicate(g.body, color=bit_color(o), scale_factor=1.08), run_time=0.5)
            lit += self.drive([[(wo, o)]], 0.4)
            new_out = BitDot(o).move_to(spot_out)
            self.play(m.FadeIn(new_out, scale=1.4) if out is None else m.FadeTransform(out, new_out),
                      tt.fill(r, [a, b, o]), run_time=0.6)
            out = new_out
            self.wait(1.2 if r < 3 else 2.0)
            self.play(*[m.FadeOut(x) for x in lit], run_time=0.3)

        self.play(m.Circumscribe(m.VGroup(*tt.values[-3:]), color=HL))
        self.caption("Гаралт 0 болох ганц тохиолдол: a = 1, b = 1.", 2.5)
        self.caption("Гайхалтай нь: бусад бүх хаалгыг зөвхөн NAND-аар бүтээж болно.", 3.5)
        self.clear_all()

    # ── 3. NOT ─────────────────────────────────────────────────────────
    def tied_nand(self, center, scale=1.3):
        """A NAND with both inputs tied to one wire. Returns (gate, input wire, branches)."""
        g = Gate("NAND", scale=scale).move_to(center)
        jx = g.in_pt(0)[0] - 0.6
        j = np.array([jx, g.get_center()[1] - 0.1 * scale + 0.1 * scale, 0])
        j[1] = (g.in_pt(0)[1] + g.in_pt(1)[1]) / 2
        b1 = wire(j, (jx, g.in_pt(0)[1], 0), g.in_pt(0))
        b2 = wire(j, (jx, g.in_pt(1)[1], 0), g.in_pt(1))
        dot = m.Dot(j, radius=0.07, color=WIRE)
        return g, j, m.VGroup(b1, b2, dot)

    def build_not(self):
        h = self.heading("NOT: NAND-аас")
        g, j, branches = self.tied_nand((-1.6, 0.4, 0))
        wa = wire((-5.2, j[1], 0), j)
        wo = wire(g.out_pt(), (0.9, g.out_pt()[1], 0))
        la = T("a", 30, DIM).next_to(wa, m.LEFT, buff=1.15)
        tt = TruthTable(["a", "NOT"], 2, col_w=1.2).move_to((4.6, 0.7, 0))
        self.play(m.FadeIn(g), m.Create(wa), m.Create(branches), m.Create(wo), m.FadeIn(la))
        self.caption("NAND-ийн хоёр оролтыг нэг утсанд холбоё.", 2)
        self.play(m.FadeIn(tt.heads), m.Create(tt.rule), m.Create(tt.sep))

        ins, out = None, None
        for r, a in enumerate([0, 1]):
            o = int(not a)
            ins = self.put_bits(ins, [wa.get_start() + 0.4 * m.LEFT], [a])
            lit = self.drive([[(wa, a)], [(branches[0], a), (branches[1], a)], [(wo, o)]], 0.45)
            new_out = BitDot(o).move_to(wo.get_end() + 0.4 * m.RIGHT)
            self.play(m.FadeIn(new_out, scale=1.4) if out is None else m.FadeTransform(out, new_out),
                      tt.fill(r, [a, o]), run_time=0.6)
            out = new_out
            self.wait(1.2)
            self.play(*[m.FadeOut(x) for x in lit], run_time=0.3)

        self.caption("Оролтыг урвуулдаг: 0-г 1, 1-г 0 болгоно. Энэ бол NOT.", 2.5)
        circuit = m.VGroup(g, branches)
        sym = Gate("NOT", scale=1.4).move_to(circuit)
        self.play(m.FadeOut(ins), m.FadeOut(out))
        self.play(m.ReplacementTransform(circuit, sym), run_time=1.2)
        self.wait(1.5)
        self.clear_all()

    # ── 4. AND ─────────────────────────────────────────────────────────
    def build_and(self):
        h = self.heading("AND = NAND + NOT")
        g1 = Gate("NAND", scale=1.2).move_to((-3.0, 0.4, 0))
        g2 = Gate("NOT", scale=1.2).move_to((-0.4, 0.4, 0))
        wa = wire((-5.6, g1.in_pt(0)[1], 0), g1.in_pt(0))
        wb = wire((-5.6, g1.in_pt(1)[1], 0), g1.in_pt(1))
        wm = wire(g1.out_pt(), g2.in_pt(0))
        wo = wire(g2.out_pt(), (1.4, g2.out_pt()[1], 0))
        la = T("a", 30, DIM).next_to(wa, m.LEFT, buff=1.15)
        lb = T("b", 30, DIM).next_to(wb, m.LEFT, buff=1.15)
        tt = TruthTable(["a", "b", "AND"], 4, col_w=1.0).move_to((4.6, 0.4, 0))
        self.play(m.FadeIn(g1), m.FadeIn(g2), *[m.Create(w) for w in (wa, wb, wm, wo)],
                  m.FadeIn(la), m.FadeIn(lb))
        self.caption("NAND-ийн гаралтыг дахин урвуулбал AND гарна.", 2)
        self.play(m.FadeIn(tt.heads), m.Create(tt.rule), m.Create(tt.sep))

        ins, out = None, None
        spots = [wa.get_start() + 0.4 * m.LEFT, wb.get_start() + 0.4 * m.LEFT]
        for r, (a, b) in enumerate([(0, 0), (0, 1), (1, 0), (1, 1)]):
            n = NAND(a, b)
            o = int(a and b)
            ins = self.put_bits(ins, spots, [a, b])
            lit = self.drive([[(wa, a), (wb, b)], [(wm, n)], [(wo, o)]], 0.35)
            new_out = BitDot(o).move_to(wo.get_end() + 0.4 * m.RIGHT)
            self.play(m.FadeIn(new_out, scale=1.4) if out is None else m.FadeTransform(out, new_out),
                      tt.fill(r, [a, b, o]), run_time=0.5)
            out = new_out
            self.wait(0.8)
            self.play(*[m.FadeOut(x) for x in lit], run_time=0.3)

        self.caption("Хоёр оролт хоёулаа 1 үед л гаралт 1.", 2.5)
        circuit = m.VGroup(g1, g2, wm)
        sym = Gate("AND", scale=1.4).move_to(circuit)
        self.play(m.FadeOut(ins), m.FadeOut(out))
        self.play(m.ReplacementTransform(circuit, sym), wa.animate.put_start_and_end_on(wa.get_start(), sym.in_pt(0)),
                  wb.animate.put_start_and_end_on(wb.get_start(), sym.in_pt(1)),
                  wo.animate.put_start_and_end_on(sym.out_pt(), wo.get_end()), run_time=1.2)
        self.wait(1.5)
        self.clear_all()

    # ── 5. OR ──────────────────────────────────────────────────────────
    def build_or(self):
        h = self.heading("OR: оролтуудыг урвуулаад NAND")
        na = Gate("NOT", scale=1.0).move_to((-3.4, 1.4, 0))
        nb = Gate("NOT", scale=1.0).move_to((-3.4, -0.6, 0))
        g = Gate("NAND", scale=1.2).move_to((-0.6, 0.4, 0))
        wa = wire((-5.6, na.in_pt(0)[1], 0), na.in_pt(0))
        wb = wire((-5.6, nb.in_pt(0)[1], 0), nb.in_pt(0))
        w1 = wire(*hv(na.out_pt(), g.in_pt(0)))
        w2 = wire(*hv(nb.out_pt(), g.in_pt(1)))
        wo = wire(g.out_pt(), (1.5, g.out_pt()[1], 0))
        la = T("a", 30, DIM).next_to(wa, m.LEFT, buff=1.15)
        lb = T("b", 30, DIM).next_to(wb, m.LEFT, buff=1.15)
        tt = TruthTable(["a", "b", "OR"], 4, col_w=1.0).move_to((4.7, 0.4, 0))
        self.play(*[m.FadeIn(x) for x in (na, nb, g, la, lb)],
                  *[m.Create(w) for w in (wa, wb, w1, w2, wo)])
        self.caption("Оролт бүрийг NOT-оор урвуулж, дараа нь NAND-д оруулъя.", 2)
        self.play(m.FadeIn(tt.heads), m.Create(tt.rule), m.Create(tt.sep))

        ins, out = None, None
        spots = [wa.get_start() + 0.4 * m.LEFT, wb.get_start() + 0.4 * m.LEFT]
        for r, (a, b) in enumerate([(0, 0), (0, 1), (1, 0), (1, 1)]):
            o = int(a or b)
            ins = self.put_bits(ins, spots, [a, b])
            lit = self.drive([[(wa, a), (wb, b)], [(w1, 1 - a), (w2, 1 - b)], [(wo, o)]], 0.35)
            new_out = BitDot(o).move_to(wo.get_end() + 0.4 * m.RIGHT)
            self.play(m.FadeIn(new_out, scale=1.4) if out is None else m.FadeTransform(out, new_out),
                      tt.fill(r, [a, b, o]), run_time=0.5)
            out = new_out
            self.wait(0.8)
            self.play(*[m.FadeOut(x) for x in lit], run_time=0.3)

        self.caption("Аль нэг оролт 1 бол гаралт 1. Энэ бол OR.", 2.5)
        circuit = m.VGroup(na, nb, g, w1, w2)
        sym = Gate("OR", scale=1.4).move_to(circuit)
        self.play(m.FadeOut(ins), m.FadeOut(out))
        self.play(m.ReplacementTransform(circuit, sym),
                  m.FadeOut(wa), m.FadeOut(wb), m.FadeOut(wo), m.FadeOut(la), m.FadeOut(lb), run_time=1.2)
        self.wait(1.5)
        self.clear_all()

    # ── 6. summary ─────────────────────────────────────────────────────
    def summary(self):
        h = self.heading("Нэг NAND — бүх логик")
        nand = Gate("NAND", scale=1.5).move_to((0, 1.5, 0))
        kids = m.VGroup(*[Gate(k, scale=1.2) for k in ("NOT", "AND", "OR")]).arrange(m.RIGHT, buff=2.2)
        kids.move_to((0, -1.75, 0))
        start = nand.label.get_bottom() + 0.2 * m.DOWN
        arrows = m.VGroup(*[m.Arrow(start, k.get_top(), buff=0.15, color=DIM, stroke_width=4)
                            for k in kids])
        self.play(m.FadeIn(nand, scale=0.8))
        self.play(m.LaggedStart(*[m.GrowArrow(a) for a in arrows], lag_ratio=0.2),
                  m.LaggedStart(*[m.FadeIn(k, shift=0.3 * m.DOWN) for k in kids], lag_ratio=0.2))
        self.caption("NOT, AND, OR — бүгдийг нь зөвхөн NAND-аар бүтээлээ.", 3)
        self.caption("Дараагийн бүлэгт: XOR, мультиплексор, шин.", 3)
        self.clear_all()
        self.wait(0.5)
