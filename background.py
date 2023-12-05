from pico2d import *

import play_mode

class background:
    image = None

    def __init__(self):
        self.x, self.y = 640, 400
        if background.image == None:
            background.image = load_image('Play_mode_background_1280x800.png')

    def draw(self):
        self.image.draw(self.x, self.y)

    def update(self):
        pass

class FixedBackground:
    def __init__(self):
        self.image = load_image('Background_1280x5024.png')
        self.cw = get_canvas_width()
        self.ch = get_canvas_height()
        self.w = self.image.w
        self.h = self.image.h - 250
        self.window_left = 0
        self.window_bottom = 0
        self.view_mode = False
        self.bgm = load_music('Curling_Playing.mp3')
        self.bgm.set_volume(32)
        self.bgm.repeat_play()

    def draw(self):
        self.image.clip_draw_to_origin(self.window_left, self.window_bottom, self.cw, self.ch, 0, 0)

    def update(self):
        self.window_left = int(play_mode.playing_stone[play_mode.playing_stone_pointer].x) - self.cw // 2
        self.window_bottom = int(play_mode.playing_stone[play_mode.playing_stone_pointer].y) - self.ch // 2
        self.window_left = clamp(0, int(play_mode.playing_stone[play_mode.playing_stone_pointer].x) - self.cw // 2, self.w - self.cw - 1)
        if (self.view_mode == False):
            self.window_bottom = clamp(0, int(play_mode.playing_stone[play_mode.playing_stone_pointer].y) - self.ch // 2 + 200, self.h - self.ch - 1)
        else:
            self.window_bottom = 5024 - 250 - 800 - 1