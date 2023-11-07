from pico2d import *
from math import fabs, pow, sqrt, acos


# 해당 벡터의 크기가 1인 벡터를 반환하는 메서드
def get_unit_vector_xy(vx, vy):
    div = sqrt(pow(vx, 2) + pow(vy, 2))
    return vx / div, vy / div

# o에 대해 상대적인 a의 벡터(충돌지점)을 반환하는 메서드
def get_relative_collision_xy(avx, avy, ovx, ovy):
    rvx, rvy = ovx-avx, ovy-avy
    rvx *= -1
    rvy *= -1
    return get_unit_vector_xy(rvx, rvy)

# 추후 조정
x_min_boundary = 0
x_max_boundary = 1280
y_min_boundary = 0
y_max_boundary = 800


class blue_stone:

    image = None
    minV = 0.02
    vDecRate = 0.98

    def __init__(self, x = 100, y = 100):
        self.x, self.y = x, y
        self.vx, self.vy = 30, 30
        self.radius = 32
        if (blue_stone.image == None):
            blue_stone.image = load_image('Stone_Blue_64x64.png')

    def draw(self):
        self.image.draw(self.x, self.y)

    def update(self):
        self.x += self.vx
        self.y += self.vy

        self.stone_wall_collision()

        self.vx *= blue_stone.vDecRate
        if (fabs(self.vx) < blue_stone.minV):
            self.vx = 0

        self.vy *= blue_stone.vDecRate
        if (fabs(self.vx) < blue_stone.minV):
            self.vy = 0

    def stone_wall_collision(self):
        if (self.x < x_min_boundary + self.radius):
            self.x += 2*(self.radius - (self.x - x_min_boundary))
            self.vx *= -1
        elif (self.x > x_max_boundary - self.radius):
            self.x -= 2*(self.x - (x_max_boundary - self.radius))
            self.vx *= -1

        if (self.y < y_min_boundary + self.radius):
            self.y += 2*(self.radius - (self.y - y_min_boundary))
            self.vy *= -1
        elif (self.y > y_max_boundary - self.radius):
            self.y -= 2*(self.y - (y_max_boundary - self.radius))
            self.vy *= -1

    def get_bc(self):
        return self.x, self.y, self.radius

    def handle_collision(self, group, oppo):
        if group == 'stone:stone':
            ############################################
            ############################################
            pass

    def get_power(self):
        return sqrt(pow(self.vx, 2)+pow(self.vy, 2))

    def get_radian(self):
        return acos(self.vx/self.get_power())

