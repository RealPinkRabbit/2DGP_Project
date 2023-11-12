from pico2d import *

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