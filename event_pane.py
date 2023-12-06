from pico2d import *

import play_mode


class event_pane:
    image = None
    font = None

    def __init__(self):
        self.image_pointer = 0
        self.message = ''
        self.is_presenting = False
        self.RGB = (255, 255, 255)
        if event_pane.image == None:
            event_pane.image = load_image('Event_Scene_1280x800.png')
        if event_pane.font == None:
            event_pane.font = load_font('Maplestory Bold.ttf', 128)


    def draw(self):
        self.image.clip_draw_to_origin(0, 0, 1500, 800, 1280 - self.image_pointer, 0)
        self.font.draw(400 - 1280 + self.image_pointer, 400, f'{self.message}', self.RGB)
        pass

    def update(self):
        if self.is_presenting == True:
            if self.image_pointer < 1200:
                self.image_pointer += 30
            elif self.image_pointer < 1360:
                self.image_pointer += 2
            elif self.image_pointer < 3000:
                self.image_pointer += 30
            else:
                self.image_pointer = 0
                self.is_presenting = False
        pass
