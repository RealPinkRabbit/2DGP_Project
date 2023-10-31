from pico2d import *

class blue_stone:
    image = None
    def __init__(self, x = 400, y = 100):
        self.x, self.y = x, y
        if (blue_stone.image == None):
            blue_stone.image = load_image('blue_stone.png')

    def draw(self):
        self.image.draw(self.x, self.y)

    def update(self):
        pass

def create_world():
    global running
    global stone1

    running = True
    stone1 = blue_stone()
    pass

def handle_events():
    global running

    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False
    pass

def update_world():
    stone1.update()
    pass

def render_world():
    clear_canvas()
    stone1.draw()
    update_canvas()
    pass

open_canvas()
create_world()
while running:
    handle_events()
    update_world()
    render_world()
close_canvas()