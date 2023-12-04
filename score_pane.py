from pico2d import *

import play_mode

class score_pane:
    image = None

    def __init__(self):
        self.font = load_font('ENCR10B.TTF', 64)
        if score_pane.image == None:
            score_pane.image = load_image('Score_Pane_400x500.png')

    def draw(self):
        self.image.clip_draw_to_origin(0, 0, 400, 500, 200+552 + (1280 - (200+552))//2 - 200, 800//2 - 500//2 + 100)
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