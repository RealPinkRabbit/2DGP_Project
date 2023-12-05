from pico2d import *

import play_mode


class mini_map:
    image = None

    def __init__(self):
        self.font = load_font('ENCR10B.TTF', 64)
        if mini_map.image == None:
            mini_map.image = load_image('Mini_Field_82x750.png')

    def draw(self):
        self.image.clip_draw_to_origin(0, 0, 82, 750, 100 - 82 // 2, 25)
        # self.image.draw(self.sx, self.sy)
        # self.font.draw(self.sx - 170, self.sy + 250, f'{self.score_color} : {self.score}', self.RGB)
        pass

    def update(self):
        # self.sx = self.x - play_mode.playing_background.window_left
        # self.sy = self.y - play_mode.playing_background.window_bottom
        # self.stones_clone = self.stones.copy()
        # self.sort_distance()
        # self.update_score()
        # self.stones.clear()
        pass
