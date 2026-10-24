import manimgx as m


class FontTest(m.Scene):
    def construct(self):
        s = "Мөнгөн үсэг: Ө ө Ү ү Ң ң Ё ё"
        a = m.Text(s).shift(1.5 * m.UP)
        b = m.Tex(s).shift(0.3 * m.UP)
        c = m.Text(s, font="Noto Sans").shift(1.0 * m.DOWN)
        d = m.Text("Логик хаалга → нэмэгч → регистр", font="Noto Sans", font_size=36).shift(2.2 * m.DOWN)
        self.add(a, b, c, d)
        self.wait(0.5)
