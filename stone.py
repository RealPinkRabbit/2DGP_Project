from pico2d import *
from math import *

class blue_stone:
    image = None
    minV = 0.02
    vDecRate = 0.98
    def __init__(self, x = 600, y = 750):
        self.x, self.y = x, y
        self.vx, self.vy = 100, -100
        self.radius = 32
        if (blue_stone.image == None):
            blue_stone.image = load_image('Stone_Blue_64x64.png')

    def draw(self):
        self.image.draw(self.x, self.y)

    def update(self):
        self.x += self.vx
        if (self.x < 0 + self.radius):
            self.x += 2*(self.radius - self.x)
            self.vx *= -1
        elif (self.x > 1280 - self.radius):
            self.x -= 2*(self.x - (1280 - self.radius))
            self.vx *= -1
        self.vx *= blue_stone.vDecRate
        if (fabs(self.vx) < blue_stone.minV):
            self.vx = 0

        self.y += self.vy
        if (self.y < 0 + self.radius):
            self.y += 2*(self.radius - self.y)
            self.vy *= -1
        elif (self.y > 800 - self.radius):
            self.y -= 2*(self.y - (800 - self.radius))
            self.vy *= -1
        self.vy *= blue_stone.vDecRate
        if (fabs(self.vx) < blue_stone.minV):
            self.vy = 0