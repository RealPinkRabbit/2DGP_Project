from pico2d import *

import game_world
import play_mode


class mini_map:
    image = None
    mini_blue_stone_image = None
    mini_red_stone_image = None
    # mini_view = None

    def __init__(self):
        self.font = load_font('ENCR10B.TTF', 64)
        self.stones = []
        self.view = []
        if mini_map.image == None:
            mini_map.image = load_image('Mini_Field_82x750.png')
        if mini_map.mini_blue_stone_image == None:
            mini_map.mini_blue_stone_image = load_image('Mini_Blue_Stone_5x5.png')
        if mini_map.mini_red_stone_image == None:
            mini_map.mini_red_stone_image = load_image('Mini_Red_Stone_5x5.png')
        # if mini_map.mini_view == None:
        #     mini_map.mini_view = load_image('Mini_View_130x93.png')

    def draw(self):
        self.image.clip_draw_to_origin(0, 0, 82, 750, 100 - 82 // 2, 25)
        for stone in self.stones:
            if stone[0] == 'BLUE':
                cx, cy = self.normalization(stone[1], stone[2])
                mini_map.mini_blue_stone_image.clip_draw(0, 0, 5, 5, cx, cy)
            elif stone[0] == 'RED':
                cx, cy = self.normalization(stone[1], stone[2])
                mini_map.mini_red_stone_image.clip_draw(0, 0, 5, 5, cx, cy)
        # vx, vy = self.normalization_2(self.view[0][0], self.view[0][1])
        # mini_map.mini_view.clip_draw(0, 0, 130, 93, vx, vy)
        pass

    def update(self):
        self.stones.clear()
        for pairs in game_world.objects:
            for stones in pairs:
                if stones.__class__.__name__ == 'blue_stone' or stones.__class__.__name__ == 'red_stone':
                    self.stones.append((stones.color, stones.x, stones.y))
        # self.view.clear()
        # self.view.append((play_mode.playing_background.window_left, play_mode.playing_background.window_bottom))

        pass

    def normalization(self, x, y):
        cx = (x - 200) / 6.7 + 100 - 82 // 2
        cy = y / 6.7 + 25
        return cx, cy

    def normalization_2(self, x, y):
        # # x ... (0) 범위를 (100 - 82 // 2 - 5)로 변환
        # # y ... (0 ~ 5024 - 800) 범위를 (25 ~ 25 + 750 - 93)으로 변환
        # # = 0~4224 를 25~682 로
        # cx = 100 - 82 // 2 - 5
        # cy = int((y + 25) / 6.43) - 5
        # return cx, cy
        pass