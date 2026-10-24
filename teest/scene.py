import manimgx as m


class SquareToCircle(m.Scene):
    def construct(self):
        square = m.Square(color=m.BLUE, fill_opacity=0.5)
        circle = m.Circle(color=m.RED, fill_opacity=0.5)
        self.play(m.Create(square))
        self.wait(0.5)
        self.play(m.Transform(square, circle))
        self.wait(0.5)
