from pico2d import *
from stone import blue_stone
import game_world
from math import *

canvas_width = 1280
canvas_height = 800

def create_world():
    global running
    global stone_1, stone_2

    running = True

    stone_2 = blue_stone(400, 230, 3, 10)
    stone_1 = blue_stone(100, 100, 20, 20)

    game_world.add_object(stone_1, 0)
    game_world.add_object(stone_2, 0)

    game_world.add_collision_pair('stone:stone', stone_1, stone_2)
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
    game_world.update_object()
    game_world.handle_collisions()

def render_world():
    clear_canvas()
    game_world.render_object()
    update_canvas()
    pass

open_canvas(canvas_width, canvas_height)
create_world()
while running:
    handle_events()
    update_world()
    render_world()
    delay(0.1)
close_canvas()