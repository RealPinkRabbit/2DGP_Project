from pico2d import *
from math import *

import game_world

def space_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_SPACE

def space_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_SPACE

def z_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_z

def z_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_z

def x_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_x

def x_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_x

def w_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_w

def w_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_w

def a_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_a

def a_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_a

def s_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_s

def s_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_s

def d_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_d

def d_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_d

def r_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_r

def r_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_r

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
y_min_boundary = 124
y_max_boundary = 800 - 124

class Idle:
    @staticmethod
    def enter(stone, e):
        if space_down(e):
            stone.x = 750
            stone.y = 400
            stone.vx = 0
            stone.vy = 0
        elif right_down(e):
            stone.vx += stone.get_power() / 100
            stone.card_dx = 50
            stone.card_dy = 0
            stone.message = 'R'
        elif left_down(e):
            stone.vx -= stone.get_power() / 100
            stone.card_dx = -50
            stone.card_dy = 0
            stone.message = 'L'
        elif up_down(e):
            stone.vy += stone.get_power() / 100
            stone.card_dx = 0
            stone.card_dy = 50
            stone.message = 'U'
        elif down_down(e):
            stone.vy -= stone.get_power() / 100
            stone.card_dx = 0
            stone.card_dy = -50
            stone.message = 'D'
        elif right_up(e):
            stone.message = ''
        elif left_up(e):
            stone.message = ''
        elif up_up(e):
            stone.message = ''
        elif down_up(e):
            stone.message = ''
        elif z_down(e):
            stone.vx = 100
        elif x_down(e):
            stone.vy = 100
        elif w_down(e):
            stone.vy = 5
        elif a_down(e):
            stone.vx = -5
        elif s_down(e):
            stone.vy = -5
        elif d_down(e):
            stone.vx = 5
        elif r_down(e):
            stone.x = 400
            stone.y = 400
            stone.vx = 0
            stone.vy = 0
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
                   up_down: Idle, up_up: Idle,
                   down_down: Idle, down_up: Idle,
                   space_down: Idle, space_up: Idle,
                   z_down: Idle, z_up: Idle,
                   x_down: Idle, x_up: Idle,
                   w_down: Idle, w_up: Idle,
                   a_down: Idle, a_up: Idle,
                   s_down: Idle, s_up: Idle,
                   d_down: Idle, d_up: Idle,
                   r_down: Idle, r_up: Idle}
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
        self.card_dx, self.card_dy = 0, 0
        self.message = ''
        self.m = 100
        self.radius = blue_stone.default_radius
        self.state_machine = StateMachine(self)
        self.state_machine.start()
        self.color = 'BLUE'
        self.font = load_font('ENCR10B.TTF', 32)
        if (blue_stone.image == None):
            blue_stone.image = load_image('Stone_Blue_64x64.png')

    def draw(self):
        self.state_machine.draw()
        self.font.draw(self.x + self.card_dx - 10, self.y + self.card_dy, f'{self.message}', (0, 0, 0))

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

        Distance = sqrt(pow(self.x - oppo_x, 2) + pow(self.y - oppo_y, 2))

        # # 동적충돌 연산
        # # self~oppo 방향 벡터
        # nx = (oppo_x - self.x) / Distance
        # ny = (oppo_y - self.y) / Distance
        #
        # # 충돌 방향에 대한 법선 벡터
        # tx = -ny
        # ty = nx
        #
        # # 법선 내적
        # dpTan1 = self.vx * tx + self.vy * ty
        # dpTan2 = oppo_vx * tx + oppo_vy * ty
        #
        # # 충돌방향 내적
        # dpNorm1 = self.vx * nx + self.vy * ny
        # dpNorm2 = oppo_vx * nx + oppo_vy * ny
        #
        # # 일직선 상의 모멘텀 보존
        # m1 = (dpNorm1 * (self.m - oppo_m) + 2*oppo_m * dpNorm2) / (self.m + oppo_m)
        # m2 = (dpNorm2 * (self.m - oppo_m) + 2*oppo_m * dpNorm1) / (self.m + oppo_m)
        #
        #
        # self.vx = tx * dpTan1 + nx * m1
        # self.vy = ty * dpTan1 + ny * m1
        # oppo_vx = tx * dpTan2 + nx * m2
        # oppo_vy = ty * dpTan2 + ny * m2

        # 정적충돌 연산
        Overlap = 0.5 * (Distance - 2 * self.radius)
        self.x -= Overlap * (self.x - oppo_x) / Distance
        self.y -= Overlap * (self.y - oppo_y) / Distance

        pass
        # if self.x < oppo_x:
        #     lxx, lxy = get_local_x(self.x, self.y, oppo_x, oppo_y)
        #     lyx, lyy = get_local_y(self.x, self.y, oppo_x, oppo_y)
        # elif self.x > oppo_x:
        #     lxx, lxy = get_local_x(oppo_x, oppo_y, self.x, self.y)
        #     lyx, lyy = get_local_y(oppo_x, oppo_y, self.x, self.y)
        # else:
        #     self.vx, oppo_vx = oppo_vx, self.vx
        #     return
        #
        # ltheta = get_radian(lxx, lxy)
        #
        # if self.x < oppo_x:
        #     check_t1 = get_internal_product(self.vx, self.vy, lxx, lxy)
        #     check_t2 = get_internal_product(oppo_vx, oppo_vy, lxx, lxy)
        # elif self.x > oppo_x:
        #     check_t1 = get_internal_product(oppo_vx, oppo_vy, lxx, lxy)
        #     check_t2 = get_internal_product(self.vx, self.vy, lxx, lxy)
        #
        # if (check_t1 <= 0 and check_t2 >= 0):
        #     return
        # if (check_t1 * check_t2 > 0):
        #     if (check_t1 < 0 and fabs(check_t1) > fabs(check_t2)):
        #         return
        #     if (check_t1 > 0 and fabs(check_t1) < fabs(check_t2)):
        #         return
        #
        # self_theta = get_radian(self.vx, self.vy)
        # oppo_theta = get_radian(oppo_vx, oppo_vy)
        #
        # self.vx = ((oppo_m * 2 * oppo_vx * cos(oppo_theta - ltheta)) * lxx / (self.m + oppo_m)) + self.vx * sin(self_theta - ltheta) * lyx
        # self.vy = ((oppo_m * 2 * oppo_vy * cos(oppo_theta - ltheta)) * lxy / (self.m + oppo_m)) + self.vy * sin(self_theta - ltheta) * lyy




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


class red_stone:

    image = None
    minV = 0.02
    vDecRate = 0.98
    default_radius = 32

    def __init__(self, x = 100, y = 100, vx = 0, vy = 0):
        self.x, self.y = x, y
        self.vx, self.vy = vx, vy
        self.card_dx, self.card_dy = 0, 0
        self.message = ''
        self.m = 100
        self.radius = blue_stone.default_radius
        self.state_machine = StateMachine(self)
        self.state_machine.start()
        self.color = 'RED'
        self.font = load_font('ENCR10B.TTF', 16)
        if (red_stone.image == None):
            red_stone.image = load_image('Stone_Red_64x64.png')

    def draw(self):
        self.state_machine.draw()
        self.font.draw(self.x + self.card_dx, self.y + self.card_dy, f'{self.message}', (0, 0, 0))

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

        self.vx = ((oppo_m * 2 * oppo_vx * -cos(oppo_theta - ltheta)) * lxx / (self.m + oppo_m)) - self.vx * -sin(self_theta - ltheta) * lyx
        self.vy = ((oppo_m * 2 * oppo_vy * -cos(oppo_theta - ltheta)) * lxy / (self.m + oppo_m)) - self.vy * -sin(self_theta - ltheta) * lyy
