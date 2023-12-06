from pico2d import *

import play_mode


class focus:
    image = None

    def __init__(self):
        if focus.image == None:
            focus.image = load_image('Focus_64x64.png')
        pass


    def draw(self):
        self.image.clip_draw(0, 0, 64, 64, play_mode.playing_stone[play_mode.playing_stone_pointer].sx, play_mode.playing_stone[play_mode.playing_stone_pointer].sy)

    def update(self):
        pass
