from graphics import *


class Screen:

    def __init__(self, dimx=1000, dimy=1000):
        self.dimy = dimy
        self.dimx = dimx

        self.win = GraphWin('Simulation', self.dimx, self.dimy)
        self.win.setBackground(color_rgb(255, 255, 255))

        self.txt = Text(Point(self.win.width / 2, self.win.height / 2), None)
        self.txt.draw(self.win)

    def set_text(self, txt):
        self.txt.setText(txt)

    def get_mouse(self):
        self.win.getMouse()