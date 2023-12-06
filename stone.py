from pico2d import *
from math import *

import game_framework
import game_world
import play_mode

PIXEL_PER_FEET = (8.0 / 1.0)
RUN_SPEED_KFPH = 20.0
RUN_SPEED_FPM = (RUN_SPEED_KFPH * 1000.0 / 60.0)
RUN_SPEED_FPS = (RUN_SPEED_FPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_FPS * PIXEL_PER_FEET)


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
    return vx / div, vy / div


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
    return get_unit_vector_xy(ox - ax, oy - ay)


def get_local_y(ax, ay, ox, oy):
    mx, my = get_unit_vector_xy(ox - ax, oy - ay)
    r, theta = coor_to_polcoor(mx, my)
    theta += pi / 2
    mx, my = polcoor_to_coor(r, theta)
    return mx, my


def coor_to_polcoor(x, y):
    r = sqrt(pow(x, 2) + pow(y, 2))
    if round(fabs(x), 4) == 0.0000:
        if x * y > 0:
            theta = atan(inf)
        elif x * y < 0:
            theta = atan(-inf)
        else:
            theta = 0
    else:
        theta = atan(y / x)
    return r, theta


def polcoor_to_coor(r, theta):
    x = r * cos(theta)
    y = r * sin(theta)
    return x, y


def get_internal_product(avx, avy, ovx, ovy):
    return avx * ovx + avy * ovy


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
    if (round(avx, 4) == 0.0000):  # a의 운동이 y축과 평행하면
        om = ovy / ovx
        cx = ax
        cy = om * (ax - ox) + oy
        return cx, cy
    elif (round(ovx, 4) == 0.0000):  # o의 운동이 y축과 평행하면
        am = avy / avx
        cx = ox
        cy = am * (ox - ax) + ay
        return cx, cy
    else:  # 두 운동 모두 y축과 평행하지 않으면
        am = avy / avx
        om = ovy / ovx
        cx = (ax * am - ay - ox * om + oy) / (am - om)
        cy = am * (cx - ax) + ay
        return cx, cy


# 추후 조정
x_min_boundary = 200
x_max_boundary = 200 + 552
y_min_boundary = 0
y_max_boundary = 10000


class Idle:
    @staticmethod
    def enter(stone, e):
        if space_down(e):
            if stone.is_launched == False:
                stone.is_launched = True
                stone.vy = stone.power[stone.power_pointer]
        elif right_down(e):
            if stone.is_launched == False:
                stone.x += 32
                if stone.x >= 200 + 552 - 16:
                    stone.x = 200 + 552 - 16
            else:
                stone.vx += stone.get_power() / 100
                stone.vy += stone.get_power() / 200
                if stone.is_swipping == False:
                    stone.is_swipping = True
                    stone.swipped_frame = (play_mode.frame) % 30
                    stone.swipping_image_3_pointer = 0
                # stone.card_dx = 50
                # stone.card_dy = 0
                # stone.message = 'R'
        elif left_down(e):
            if stone.is_launched == False:
                stone.x -= 32
                if stone.x <= 200 + 16:
                    stone.x = 200 + 16
            else:
                stone.vx -= stone.get_power() / 100
                stone.vy += stone.get_power() / 200
                if stone.is_swipping == False:
                    stone.is_swipping = True
                    stone.swipped_frame = (play_mode.frame) % 30
                    stone.swipping_image_2_pointer = 0
                # stone.card_dx = -50
                # stone.card_dy = 0
                # stone.message = 'L'
        elif up_down(e):
            if stone.is_launched == False:
                if stone.power_pointer < 2:
                    stone.power_pointer += 1
            else:
                stone.vy += stone.get_power() / 100
                if stone.is_swipping == False:
                    stone.is_swipping = True
                    stone.swipped_frame = (play_mode.frame) % 30
                    stone.swipping_image_1_pointer = 0
                # stone.card_dx = 0
                # stone.card_dy = 50
                # stone.message = 'U'
        elif down_down(e):
            if stone.is_launched == False:
                if stone.power_pointer > 0:
                    stone.power_pointer -= 1
            # stone.vy -= stone.get_power() / 100
            # stone.card_dx = 0
            # stone.card_dy = -50
            # stone.message = 'D'
            pass
        elif right_up(e):
            # stone.message = ''
            pass
        elif left_up(e):
            stone.swipping_image_1_pointer = 1
            # stone.message = ''
            pass
        elif up_up(e):
            # stone.message = ''
            pass
        elif down_up(e):
            # stone.message = ''
            pass
        elif z_down(e):
            pass
        elif z_up(e):
            pass
        elif x_down(e):
            # stone.vy = 100
            pass
        elif w_down(e):
            play_mode.playing_background.view_mode = True
            # stone.vy = 5
            pass
        elif w_up(e):
            play_mode.playing_background.view_mode = False
            pass
        elif a_down(e):
            # if stone.message != '':
            #     stone.message = ''
            if play_mode.playing_stone_pointer > 0:
                play_mode.playing_stone_pointer -= 1
            # stone.vx = -5
            pass
        elif s_down(e):
            # stone.vy = -5
            pass
        elif d_down(e):
            # if stone.message != '':
            #     stone.message = ''
            if play_mode.playing_stone_pointer < len(play_mode.playing_stone) - 1:
                play_mode.playing_stone_pointer += 1
            # stone.vx = 5
            pass
        elif r_down(e):
            # stone.vx, stone.vy = 0, 0
            # stone.x = 400
            # stone.y = 400
            # stone.vx = 0
            # stone.vy = 0
            pass
        pass

    @staticmethod
    def exit(stone, e):
        pass

    @staticmethod
    def do(stone):
        global frame
        stone.x += stone.vx * game_framework.frame_time * RUN_SPEED_PPS
        stone.y += stone.vy * game_framework.frame_time * RUN_SPEED_PPS
        stone.sx = stone.x - play_mode.playing_background.window_left
        stone.sy = stone.y - play_mode.playing_background.window_bottom

        stone.stone_wall_collision()

        if stone.is_swipping == True:
            if (play_mode.frame - stone.swipped_frame) % 30 < 8:
                stone.image_moving_pixel = 30
            elif (play_mode.frame - stone.swipped_frame) % 30 < 15:
                stone.image_moving_pixel = 0
            elif (play_mode.frame - stone.swipped_frame) % 30 < 23:
                stone.image_moving_pixel = 30
            elif (play_mode.frame - stone.swipped_frame) % 30 < 30:
                stone.image_moving_pixel = 0
            if stone.swipped_frame == play_mode.frame:
                stone.swipping_image_1_pointer = 1
                stone.swipping_image_2_pointer = 1
                stone.swipping_image_3_pointer = 1
                stone.is_swipping = False

        if stone.y > 5024 + stone.radius:
            stone.vx = 0
            stone.vy = 0

        if stone.vx >= 6:
            stone.vx *= stone.vDecRate
        elif stone.vx >= 3:
            stone.vx *= stone.slowVDecRate_1
        else:
            stone.vx *= stone.slowVDecRate_2
        if (fabs(stone.vx) < stone.minV):
            stone.vx = 0

        if stone.vy >= 6:
            stone.vy *= stone.vDecRate
        elif stone.vx >= 3:
            stone.vy *= stone.slowVDecRate_1
        else:
            stone.vy *= stone.slowVDecRate_2
        if (fabs(stone.vy) < stone.minV):
            stone.vy = 0

    @staticmethod
    def draw(stone):
        global temp
        # stone.font.draw(stone.sx + stone.card_dx - 10, stone.sy + stone.card_dy, f'{stone.message}', (0, 0, 0))
        if (stone.is_launched == False):
            temp = stone.x
            stone.estimated_path_image.clip_draw_to_origin(0, 0, 32, 5024, stone.sx - stone.radius, 0)
            stone.powerGauge_image.clip_draw_to_origin(0 + 100 * stone.power_pointer, 0, 100, 100, stone.sx - 100,
                                                       stone.sy - 50)
        elif stone.is_handling == True:
            stone.estimated_path_image.clip_draw_to_origin(0, 0, 32, 5024, temp - stone.radius, 0)
            stone.swipping_image_1.clip_draw(0, 0 + 1280 * stone.swipping_image_1_pointer, 1280, 800, stone.sx,
                                             stone.sy + stone.image_moving_pixel + 120, 270, 200)
            stone.swipping_image_2.clip_draw(0, 0 + 1280 * stone.swipping_image_2_pointer, 1280, 800,
                                             stone.sx + stone.image_moving_pixel - 90, stone.sy + 110, 270, 200)
            stone.swipping_image_2.clip_composite_draw(0, 0 + 1280 * stone.swipping_image_3_pointer, 1280, 800, 0, 'h',
                                                       stone.sx - stone.image_moving_pixel + 90, stone.sy + 110, 270,
                                                       200)
        else:
            stone.swipping_image_1.clip_draw(0, 0 + 1280 * stone.swipping_image_1_pointer, 1280, 800, stone.sx,
                                             stone.sy + stone.image_moving_pixel + 120, 270, 200)
            stone.swipping_image_2.clip_draw(0, 0 + 1280 * stone.swipping_image_2_pointer, 1280, 800,
                                             stone.sx + stone.image_moving_pixel - 90, stone.sy + 110, 270, 200)
            stone.swipping_image_2.clip_composite_draw(0, 0 + 1280 * stone.swipping_image_3_pointer, 1280, 800, 0, 'h',
                                                       stone.sx - stone.image_moving_pixel + 90, stone.sy + 110, 270,
                                                       200)
        stone.image.draw(stone.sx, stone.sy)
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
    powerGauge_image = None
    estimated_path_image = None
    swipping_image_1 = None
    swipping_image_2 = None
    character = 'DUCK'
    minV = 0.02
    vDecRate = 0.995
    slowVDecRate_1 = 0.99
    slowVDecRate_2 = 0.98
    default_radius = 16

    def __init__(self, x=100, y=100, vx=0, vy=0):
        self.x, self.y = x, y
        self.vx, self.vy = vx, vy
        self.sx = 0
        self.sy = 0
        self.card_dx, self.card_dy = 0, 0
        self.message = ''
        self.m = 100
        self.radius = blue_stone.default_radius
        self.character = str(blue_stone.character)
        self.is_launched = False
        self.is_handling = True
        self.is_swipping = False
        self.swipped_frame = 0
        self.image_moving_pixel = 0
        self.power = [23, 26, 30]
        self.power_pointer = 0
        self.swipping_image_1_pointer = 1
        self.swipping_image_2_pointer = 1
        self.swipping_image_3_pointer = 1
        self.state_machine = StateMachine(self)
        self.state_machine.start()
        self.color = 'BLUE'
        self.font = load_font('ENCR10B.TTF', 32)
        if (blue_stone.image == None):
            blue_stone.image = load_image('Stone_Blue_32x32.png')
        if (blue_stone.powerGauge_image == None):
            blue_stone.powerGauge_image = load_image('Power_Gauge_300x100.png')
        if (blue_stone.estimated_path_image == None):
            blue_stone.estimated_path_image = load_image('Estimated_Path_32x5024.png')
        if (blue_stone.swipping_image_1 == None):
            if self.character == 'DUCK':
                blue_stone.swipping_image_1 = load_image('Duck_Swipping_1_1280x800.png')
            elif self.character == 'CAT':
                blue_stone.swipping_image_1 = load_image('Cat_Swipping_1_1280x800.png')
        if (blue_stone.swipping_image_2 == None):
            if self.character == 'DUCK':
                blue_stone.swipping_image_2 = load_image('Duck_Swipping_2_1280x800.png')
            elif self.character == 'CAT':
                blue_stone.swipping_image_2 = load_image('Cat_Swipping_2_1280x800.png')

    def draw(self):
        self.state_machine.draw()

    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        self.state_machine.handle_event(('INPUT', event))

    def stone_wall_collision(self):
        if (self.x < x_min_boundary + self.radius):
            self.x += 2 * (self.radius - (self.x - x_min_boundary))
            self.vx *= -1
        elif (self.x > x_max_boundary - self.radius):
            self.x -= 2 * (self.x - (x_max_boundary - self.radius))
            self.vx *= -1

        if (self.y < y_min_boundary + self.radius):
            self.y += 2 * (self.radius - (self.y - y_min_boundary))
            self.vy *= -1
        elif (self.y > y_max_boundary - self.radius):
            self.y -= 2 * (self.y - (y_max_boundary - self.radius))
            self.vy *= -1

    def get_bc(self):
        return self.x, self.y, self.radius

    def handle_collision(self, group, oppo):
        if group == 'stone:stone':

            if self.x > oppo.x:
                return
            if self.x == oppo.x:
                if self.y > oppo.y:
                    return

            # 정적충돌 연산
            Distance = sqrt(pow(self.x - oppo.x, 2) + pow(self.y - oppo.y, 2))
            Overlap = 0.5 * (Distance - 2 * self.radius)
            if Distance == 0:
                return
            self.x -= Overlap * (self.x - oppo.x) / Distance
            self.y -= Overlap * (self.y - oppo.y) / Distance
            oppo.x += Overlap * (self.x - oppo.x) / Distance
            oppo.y += Overlap * (self.x - oppo.x) / Distance

            # 동적충돌 연산
            # self~oppo 방향 벡터
            nx = (oppo.x - self.x) / Distance
            ny = (oppo.y - self.y) / Distance

            # 충돌 방향에 대한 법선 벡터
            tx = -ny
            ty = nx

            # 법선 내적
            dpTan1 = self.vx * tx + self.vy * ty
            dpTan2 = oppo.vx * tx + oppo.vy * ty

            # 충돌방향 내적
            dpNorm1 = self.vx * nx + self.vy * ny
            dpNorm2 = oppo.vx * nx + oppo.vy * ny

            # 일직선 상의 모멘텀 보존
            m1 = (dpNorm1 * (self.m - oppo.m) + 2 * oppo.m * dpNorm2) / (self.m + oppo.m)
            m2 = (dpNorm2 * (oppo.m - self.m) + 2 * self.m * dpNorm1) / (self.m + oppo.m)

            self.vx = tx * dpTan1 + nx * m1
            self.vy = ty * dpTan1 + ny * m1
            oppo.vx = tx * dpTan2 + nx * m2
            oppo.vy = ty * dpTan2 + ny * m2

        if group == 'house:stone':
            pass

    def get_power(self):
        return sqrt(pow(self.vx, 2) + pow(self.vy, 2))

    def get_local_radian(self):
        mx, mv = get_unit_vector_xy(self.vx, self.vy)
        if self.vy >= 0:
            rad = acos(mx) + pi
        else:
            rad = acos(-mx)
        return rad


class red_stone:
    image = None
    powerGauge_image = None
    estimated_path_image = None
    swipping_image_1 = None
    swipping_image_2 = None
    character = 'CAT'
    minV = 0.02
    vDecRate = 0.995
    slowVDecRate_1 = 0.99
    slowVDecRate_2 = 0.98
    default_radius = 16

    def __init__(self, x=100, y=100, vx=0, vy=0):
        self.x, self.y = x, y
        self.vx, self.vy = vx, vy
        self.sx = 0
        self.sy = 0
        self.card_dx, self.card_dy = 0, 0
        self.message = ''
        self.m = 100
        self.radius = red_stone.default_radius
        self.character = str(red_stone.character)
        self.is_launched = False
        self.is_handling = True
        self.is_swipping = False
        self.swipped_frame = 0
        self.image_moving_pixel = 0
        self.power = [23, 26, 30]
        self.power_pointer = 0
        self.swipping_image_1_pointer = 1
        self.swipping_image_2_pointer = 1
        self.swipping_image_3_pointer = 1
        self.state_machine = StateMachine(self)
        self.state_machine.start()
        self.color = 'RED'
        self.font = load_font('ENCR10B.TTF', 32)
        if (red_stone.image == None):
            red_stone.image = load_image('Stone_Red_32x32.png')
        if (red_stone.powerGauge_image == None):
            red_stone.powerGauge_image = load_image('Power_Gauge_300x100.png')
        if (red_stone.estimated_path_image == None):
            red_stone.estimated_path_image = load_image('Estimated_Path_32x5024.png')
        if (red_stone.swipping_image_1 == None):
            if self.character == 'DUCK':
                red_stone.swipping_image_1 = load_image('Duck_Swipping_1_1280x800.png')
            elif self.character == 'CAT':
                red_stone.swipping_image_1 = load_image('Cat_Swipping_1_1280x800.png')
        if (red_stone.swipping_image_2 == None):
            if self.character == 'DUCK':
                red_stone.swipping_image_2 = load_image('Duck_Swipping_2_1280x800.png')
            elif self.character == 'CAT':
                red_stone.swipping_image_2 = load_image('Cat_Swipping_2_1280x800.png')

    def draw(self):
        self.state_machine.draw()

    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        self.state_machine.handle_event(('INPUT', event))

    def stone_wall_collision(self):
        if (self.x < x_min_boundary + self.radius):
            self.x += 2 * (self.radius - (self.x - x_min_boundary))
            self.vx *= -1
        elif (self.x > x_max_boundary - self.radius):
            self.x -= 2 * (self.x - (x_max_boundary - self.radius))
            self.vx *= -1

        if (self.y < y_min_boundary + self.radius):
            self.y += 2 * (self.radius - (self.y - y_min_boundary))
            self.vy *= -1
        elif (self.y > y_max_boundary - self.radius):
            self.y -= 2 * (self.y - (y_max_boundary - self.radius))
            self.vy *= -1

    def get_bc(self):
        return self.x, self.y, self.radius

    def handle_collision(self, group, oppo):
        if group == 'stone:stone':

            if self.x > oppo.x:
                return
            if self.x == oppo.x:
                if self.y > oppo.y:
                    return

            # 정적충돌 연산
            Distance = sqrt(pow(self.x - oppo.x, 2) + pow(self.y - oppo.y, 2))
            Overlap = 0.5 * (Distance - 2 * self.radius)
            if Distance == 0:
                return
            self.x -= Overlap * (self.x - oppo.x) / Distance
            self.y -= Overlap * (self.y - oppo.y) / Distance
            oppo.x += Overlap * (self.x - oppo.x) / Distance
            oppo.y += Overlap * (self.x - oppo.x) / Distance

            # 동적충돌 연산
            # self~oppo 방향 벡터
            nx = (oppo.x - self.x) / Distance
            ny = (oppo.y - self.y) / Distance

            # 충돌 방향에 대한 법선 벡터
            tx = -ny
            ty = nx

            # 법선 내적
            dpTan1 = self.vx * tx + self.vy * ty
            dpTan2 = oppo.vx * tx + oppo.vy * ty

            # 충돌방향 내적
            dpNorm1 = self.vx * nx + self.vy * ny
            dpNorm2 = oppo.vx * nx + oppo.vy * ny

            # 일직선 상의 모멘텀 보존
            m1 = (dpNorm1 * (self.m - oppo.m) + 2 * oppo.m * dpNorm2) / (self.m + oppo.m)
            m2 = (dpNorm2 * (oppo.m - self.m) + 2 * self.m * dpNorm1) / (self.m + oppo.m)

            self.vx = tx * dpTan1 + nx * m1
            self.vy = ty * dpTan1 + ny * m1
            oppo.vx = tx * dpTan2 + nx * m2
            oppo.vy = ty * dpTan2 + ny * m2

        if group == 'house:stone':
            pass

    def get_power(self):
        return sqrt(pow(self.vx, 2) + pow(self.vy, 2))

    def get_local_radian(self):
        mx, mv = get_unit_vector_xy(self.vx, self.vy)
        if self.vy >= 0:
            rad = acos(mx) + pi
        else:
            rad = acos(-mx)
        return rad
