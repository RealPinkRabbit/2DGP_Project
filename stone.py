from pico2d import *
from math import *

import game_world

def space_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_SPACE

def up_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_UP

def up_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_UP

def down_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_DOWN

def down_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_DOWN

def right_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_RIGHT

def right_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_RIGHT

def left_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_LEFT

def left_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_LEFT

# 해당 스톤 운동벡터의 단위벡터를 반환하는 메서드
# 조금이라도 움직임이 있으면 해당 방향으로의 단위벡터 반환,
# 멈춰있으면 0, 0 반환
def get_unit_vector_xy(vx, vy):
    div = sqrt(pow(vx, 2) + pow(vy, 2))
    if div == 0:
        return 0, 0
    return vx/div, vy/div

# 스톤 o에 대하여 스톤 a의 상대적인 벡터(충돌지점)를 반환하는 메서드
# 두 스톤 모두 멈춰있는 경우는 논외
# 한쪽이라도 운동이 있으면 언제나 크기가 default_radius인 벡터 반환
# 경우에 따라 vx 또는 vy 둘 중 하나는 값이 0이 나올 수 있음.
# def get_relative_collision_xy(avx, avy, ovx, ovy):
#     rvx, rvy = ovx-avx, ovy-avy
#     rvx *= -1
#     rvy *= -1
#     vx, vy = get_unit_vector_xy(rvx, rvy)
#     vx *= blue_stone.default_radius
#     vy *= blue_stone.default_radius
#     return vx, vy

# # 두 스톤의 충돌지점의 좌표를 구하는 메서드
# def get_collision_xy(ax, ay, ox, oy):
#     return (ax + ox) / 2, (ay + oy) / 2

def get_local_x(ax, ay, ox, oy):
    return get_unit_vector_xy(ox-ax, oy-ay)

def get_local_y(ax, ay, ox, oy):
    mx, my = get_unit_vector_xy(ox-ax, oy-ay)
    r, theta = coor_to_polcoor(mx, my)
    theta += pi/2
    mx, my = polcoor_to_coor(r, theta)
    return mx, my

def coor_to_polcoor(x, y):
    r = sqrt(pow(x, 2) + pow(y, 2))
    if round(fabs(x), 4) == 0.0000:
        if x*y > 0:
            theta = atan(inf)
        elif x*y < 0:
            theta = atan(-inf)
        else:
            theta = 0
    else:
        theta = atan(y/x)
    return r, theta

def polcoor_to_coor(r, theta):
    x = r * cos(theta)
    y = r * sin(theta)
    return x, y

def get_internal_product(avx, avy, ovx, ovy):
    return avx*ovx + avy*ovy


def get_radian(vx, vy):
    mx, mv = get_unit_vector_xy(vx, vy)
    if vy >= 0:
        rad = acos(mx)
    else:
        rad = pi + acos(-mx)
    return rad


# 두 점의 좌표와 방향을 알 때, 두 직선의 교점을 구하는 메서드
# 단, 기울기가 같은 입력은 받지 않도록 함
def get_cross_xy(ax, ay, avx, avy, ox, oy, ovx, ovy):

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

class Idle:
    @staticmethod
    def enter(stone, e):
        if right_down(e):
            stone.vx += 1
        if left_down(e):
            stone.vx -= 1
        if up_down(e):
            stone.vy += 1
        if down_down(e):
            stone.vy -= 1
        pass

    @staticmethod
    def exit(stone, e):
        pass

    @staticmethod
    def do(stone):
        stone.x += stone.vx
        stone.y += stone.vy

        stone.stone_wall_collision()

        stone.vx *= blue_stone.vDecRate
        if (fabs(stone.vx) < blue_stone.minV):
            stone.vx = 0

        stone.vy *= blue_stone.vDecRate
        if (fabs(stone.vy) < blue_stone.minV):
            stone.vy = 0

    @staticmethod
    def draw(stone):
        stone.image.draw(stone.x, stone.y)
        pass

class StateMachine:
    def __init__(self, stone):
        self.stone = stone
        self.cur_state = Idle
        self.transitions = {
            Idle: {right_down: Idle, left_down: Idle, left_up: Idle, right_up: Idle,
                   up_down: Idle, down_down: Idle, up_up: Idle, down_up: Idle}
        }

    def start(self):
        self.cur_state.enter(self.stone, ('START', 0))

    def update(self):
        self.cur_state.do(self.stone)

    def draw(self):
        self.cur_state.draw(self.stone)

    def handle_event(self, e):
        for check_event, next_state in self.transitions[self.cur_state].items():
            if check_event(e):
                self.cur_state.exit(self.stone, e)
                self.cur_state = next_state
                self.cur_state.enter(self.stone, e)
                return True
        return False


class blue_stone:

    image = None
    minV = 0.02
    vDecRate = 0.98
    default_radius = 32

    def __init__(self, x = 100, y = 100, vx = 0, vy = 0):
        self.x, self.y = x, y
        self.vx, self.vy = vx, vy
        self.m = 100
        self.radius = blue_stone.default_radius
        self.state_machine = StateMachine(self)
        self.state_machine.start()
        if (blue_stone.image == None):
            blue_stone.image = load_image('Stone_Blue_64x64.png')

    def draw(self):
        self.state_machine.draw()

    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        self.state_machine.handle_event(('INPUT', event))

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
            print("collision occured")
            self.get_vxvy_after_collision(oppo.m, oppo.x, oppo.y, oppo.vx, oppo.vy)
        if group == 'house:stone':
            pass

    def get_power(self):
        return sqrt(pow(self.vx, 2)+pow(self.vy, 2))

    def get_local_radian(self):
        mx, mv = get_unit_vector_xy(self.vx, self.vy)
        if self.vy >= 0:
            rad = acos(mx) + pi
        else:
            rad = acos(-mx)
        return rad

    def get_vxvy_after_collision(self, oppo_m, oppo_x, oppo_y, oppo_vx, oppo_vy):
        if self.x < oppo_x:
            lxx, lxy = get_local_x(self.x, self.y, oppo_x, oppo_y)
            lyx, lyy = get_local_y(self.x, self.y, oppo_x, oppo_y)
        elif self.x > oppo_x:
            lxx, lxy = get_local_x(oppo_x, oppo_y, self.x, self.y)
            lyx, lyy = get_local_y(oppo_x, oppo_y, self.x, self.y)
        else:
            self.vx, oppo_vx = oppo_vx, self.vx
            return

        ltheta = get_radian(lxx, lxy)

        if self.x < oppo_x:
            check_t1 = get_internal_product(self.vx, self.vy, lxx, lxy)
            check_t2 = get_internal_product(oppo_vx, oppo_vy, lxx, lxy)
        elif self.x > oppo_x:
            check_t1 = get_internal_product(oppo_vx, oppo_vy, lxx, lxy)
            check_t2 = get_internal_product(self.vx, self.vy, lxx, lxy)

        if (check_t1 <= 0 and check_t2 >= 0):
            return
        if (check_t1 * check_t2 > 0):
            if (check_t1 < 0 and fabs(check_t1) > fabs(check_t2)):
                return
            if (check_t1 > 0 and fabs(check_t1) < fabs(check_t2)):
                return

        self_theta = get_radian(self.vx, self.vy)
        oppo_theta = get_radian(oppo_vx, oppo_vy)

        self.vx = ((oppo_m * 2 * oppo_vx * cos(oppo_theta - ltheta + pi/2)) * lxx / (self.m + oppo_m)) - self.vx * sin(self_theta - ltheta + pi/2) * lyx
        self.vy = ((oppo_m * 2 * oppo_vy * cos(oppo_theta - ltheta + pi/2)) * lxy / (self.m + oppo_m)) - self.vy * sin(self_theta - ltheta + pi/2) * lyy




# 정규화
        # a_r, a_theta = coor_to_polcoor(self.vx, self.vy)
        # a_theta -= ltheta
        # tself_vx, tself_vy = polcoor_to_coor(a_r, a_theta)
        # tself_theta = get_radian(tself_vx, tself_vy)

        # o_r, o_theta = coor_to_polcoor(oppo_vx, oppo_vy)
        # o_theta -= ltheta
        # toppo_vx, toppo_vy = polcoor_to_coor(o_r, o_theta)
        # toppo_theta = get_radian(toppo_vx, toppo_vy)

        # tself_vx = ((oppo_m * 2 * oppo_vx * cos(-toppo_theta)) * lxx / (self.m + oppo_m)) - tself_vx * sin(-tself_theta) * lyx
        # tself_vy = ((oppo_m * 2 * oppo_vy * cos(-toppo_theta)) * lxy / (self.m + oppo_m)) - tself_vy * sin(-tself_theta) * lyy

        # a_r, a_theta = coor_to_polcoor(tself_vx, tself_vy)
        # a_theta += ltheta
        # self.vx, self.vy = polcoor_to_coor(a_r, a_theta)


# class red_stone:
#
#     image = None
#     minV = 0.02
#     vDecRate = 0.98
#     default_radius = 16
#
#     def __init__(self, x = 100, y = 100, vx = 0, vy = 0):
#         self.x, self.y = x, y
#         self.vx, self.vy = vx, vy
#         self.m = 100
#         self.radius = red_stone.default_radius
#         if (red_stone.image == None):
#             red_stone.image = load_image('Stone_Red_32x32.png')
#
#     def draw(self):
#         self.image.draw(self.x, self.y)
#
#     def update(self):
#         self.x += self.vx
#         self.y += self.vy
#
#         self.stone_wall_collision()
#
#         self.vx *= red_stone.vDecRate
#         if (fabs(self.vx) < red_stone.minV):
#             self.vx = 0
#
#         self.vy *= red_stone.vDecRate
#         if (fabs(self.vy) < red_stone.minV):
#             self.vy = 0
#
#     def stone_wall_collision(self):
#         if (self.x < x_min_boundary + self.radius):
#             self.x += 2*(self.radius - (self.x - x_min_boundary))
#             self.vx *= -1
#         elif (self.x > x_max_boundary - self.radius):
#             self.x -= 2*(self.x - (x_max_boundary - self.radius))
#             self.vx *= -1
#
#         if (self.y < y_min_boundary + self.radius):
#             self.y += 2*(self.radius - (self.y - y_min_boundary))
#             self.vy *= -1
#         elif (self.y > y_max_boundary - self.radius):
#             self.y -= 2*(self.y - (y_max_boundary - self.radius))
#             self.vy *= -1
#
#     def get_bc(self):
#         return self.x, self.y, self.radius
#
#     def handle_collision(self, group, oppo):
#         if group == 'stone:stone':
#             # print("collision occured")
#             # self.get_vxvy_after_collision(oppo.m, oppo.x, oppo.y, oppo.vx, oppo.vy)
#             pass
#         if group == 'house:stone':
#             pass