from pico2d import *

import game_world
import play_mode


class mini_map:
    image = None
    mini_blue_stone_image = None
    mini_red_stone_image = None

    def __init__(self):
        self.font = load_font('ENCR10B.TTF', 64)
        self.stones = []
        if mini_map.image == None:
            mini_map.image = load_image('Mini_Field_82x750.png')
        if mini_map.mini_blue_stone_image == None:
            mini_map.mini_blue_stone_image = load_image('Mini_Blue_Stone_5x5.png')
        if mini_map.mini_red_stone_image == None:
            mini_map.mini_red_stone_image = load_image('Mini_Red_Stone_5x5.png')

    def draw(self):
        self.image.clip_draw_to_origin(0, 0, 82, 750, 100 - 82 // 2, 25)
        for stone in self.stones:
            if stone[0] == 'BLUE':
                cx, cy = self.normalization(stone[1], stone[2])
                mini_map.mini_blue_stone_image.clip_draw(0, 0, 5, 5, cx, cy)
            elif stone[0] == 'RED':
                cx, cy = self.normalization(stone[1], stone[2])
                mini_map.mini_red_stone_image.clip_draw(0, 0, 5, 5, cx, cy)
        pass

    def update(self):
        self.stones.clear()
        for pairs in game_world.objects:
            for stones in pairs:
                if stones.__class__.__name__ == 'blue_stone' or stones.__class__.__name__ == 'red_stone':
                    self.stones.append((stones.color, stones.x, stones.y))
        pass

    def normalization(self, x, y):
        x = (x - 200) / 6.7 + 100 - 82 // 2
        y = y / 6.7 + 25
        return x, y