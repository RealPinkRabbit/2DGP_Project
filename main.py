from pico2d import *
from stone import blue_stone
from math import *

canvas_width = 1280
canvas_height = 800

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

open_canvas(canvas_width, canvas_height)
create_world()
while running:
    handle_events()
    update_world()
    render_world()
    delay(0.01)
close_canvas()