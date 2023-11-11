from pico2d import *

class house:
    image = None

    def __init__(self):
        self.x, self.y = 800, 400
        self.radius = 400
        if house.image == None:
            house.image = load_image('House_400x400.png')

    def draw(self):
        self.image.draw(self.x, self.y)
    def update(self):
        pass

    def get_bc(self):
        return self.x, self.y, self.radius

    def handle_collision(self, group, oppo):
        if group == 'house:stone':
            pass