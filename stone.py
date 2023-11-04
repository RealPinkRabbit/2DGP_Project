from pico2d import *
from math import *

class blue_stone:
    image = None
    minV = 0.02
    vDecRate = 0.98
    def __init__(self, x = 500, y = 300):
        self.x, self.y = x, y
        self.vx, self.vy = -5, -3
        if (blue_stone.image == None):
            blue_stone.image = load_image('Stone_Blue_64x64.png')

    def draw(self):
        self.image.draw(self.x, self.y)

    def update(self):
        self.x += self.vx
        self.vx *= blue_stone.vDecRate
        if (fabs(self.vx) < blue_stone.minV):
            self.vx = 0

        self.y += self.vy
        self.vy *= blue_stone.vDecRate
        if (fabs(self.vx) < blue_stone.minV):
            self.vy = 0