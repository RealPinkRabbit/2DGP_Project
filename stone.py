from pico2d import *
from math import fabs, pow, sqrt, acos

import game_world


# 해당 스톤 운동벡터의 단위벡터를 반환하는 메서드
def get_unit_vector_xy(vx, vy):
    div = sqrt(pow(vx, 2) + pow(vy, 2))
    if div == 0:
        return 0, 0
    return vx/div, vy/div

# 스톤 o에 대하여 스톤 a의 상대적인 벡터(충돌지점)를 반환하는 메서드
def get_relative_collision_xy(avx, avy, ovx, ovy):
    rvx, rvy = ovx-avx, ovy-avy
    rvx *= -1
    rvy *= -1
    vx, vy = get_unit_vector_xy(rvx, rvy)
    vx *= blue_stone.default_radius
    vy *= blue_stone.default_radius
    return vx, vy

# 두 스톤의 충돌지점의 좌표를 구하는 메서드
def get_collision_xy(ax, ay, avx, avy, ox, oy, ovx, ovy):
    a_relative_vx, a_relative_vy = get_relative_collision_xy(avx, avy, ovx, ovy)
    o_relative_vx, o_relative_vy = -a_relative_vx, -a_relative_vy

    moved_ax, moved_ay = ax + a_relative_vx, ay + a_relative_vy
    moved_ox, moved_oy = ox + o_relative_vx, oy + o_relative_vy
    cx, cy = get_cross_xy(moved_ax, moved_ay, avx, avy, moved_ox, moved_oy, ovx, ovy)
    return cx, cy

# 두 점의 좌표와 방향을 알 때, 두 직선의 교점을 구하는 메서드
# 단, 기울기가 같은 입력은 받지 않도록 함 !!!!!! 해당부분 수정 필요
# 아니, 받도록 하되 예외처리를 내부에서 모두 해결
# 멈춰있는 물체와 충돌 발생시에도 오류 발생
# round() 메서드로 약간 깎아냄
def get_cross_xy(ax, ay, avx, avy, ox, oy, ovx, ovy):
    aux, auy = get_unit_vector_xy(avx, avy)
    oux, ouy = get_unit_vector_xy(ovx, ovy)
    # if (round(fabs(aux), 4) == round(fabs(oux), 4) and aux * oux > 0.0 and auy * ouy > 0.0):
    #     print("get_cross_xy exception occured")
    #     return None, None
    if ():
        pass
    else: # 기울기가 다르면
        if (round(avx,4) == 0.0000): # a의 운동이 y축과 평행하면
            om = ovy/ovx
            cx = ax
            cy = om * (ax - ox) + oy
            return cx, cy
        elif (round(ovx,4) == 0.0000): # o의 운동이 y축과 평행하면
            am = avy/avx
            cx = ox
            cy = am * (ox - ax) + ay
            return cx, cy
        else: # 두 운동 모두 y축과 평행하지 않으면
            am = avy/avx
            om = ovy/ovx
            cx = (ax * am - ay - ox * om + oy) / (am - om)
            cy = am * (cx - ax) + ay
            return cx, cy


# 추후 조정
x_min_boundary = 0
x_max_boundary = 1280
y_min_boundary = 0
y_max_boundary = 800


class blue_stone:

    image = None
    minV = 0.02
    vDecRate = 0.98
    default_radius = 32

    def __init__(self, x = 100, y = 100, vx = 0, vy = 0):
        self.x, self.y = x, y
        self.vx, self.vy = vx, vy
        self.radius = blue_stone.default_radius
        if (blue_stone.image == None):
            blue_stone.image = load_image('Stone_Blue_64x64.png')

    def draw(self):
        self.image.draw(self.x, self.y)

    def update(self):
        self.x += self.vx
        self.y += self.vy
        print(self.vx + self.vy)

        self.stone_wall_collision()

        self.vx *= blue_stone.vDecRate
        if (fabs(self.vx) < blue_stone.minV):
            self.vx = 0

        self.vy *= blue_stone.vDecRate
        if (fabs(self.vy) < blue_stone.minV):
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
        global stone
        if group == 'stone:stone':
            ############################################
            cx, cy = get_collision_xy(self.x, self.y, self.vx, self.vy, oppo.x, oppo.y, oppo.vx, oppo.vy)
            stone = blue_stone(cx, cy, 0, 0)
            game_world.add_object(stone, 0)
            ############################################
            pass

    def get_power(self):
        return sqrt(pow(self.vx, 2)+pow(self.vy, 2))

    def get_radian(self):
        return acos(self.vx/self.get_power())

