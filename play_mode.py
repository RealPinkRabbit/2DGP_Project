from pico2d import *

import game_framework
import title_mode
from stone import blue_stone # red_stone
from house import house
import game_world
from math import *

canvas_width = 1280
canvas_height = 800

def init():
    global running
    global blue_stone_1, stone_2
    # global red_stone_1
    global house_1

    running = True

    blue_stone_1 = blue_stone(400, 400, 0, 0)
    # red_stone_1 = red_stone(900, 400, 0, 0)
    house_1 = house()

    # stone_2 = blue_stone(700, 400, -20, 20)

    game_world.add_object(blue_stone_1, 1)
    # game_world.add_object(red_stone_1, 1)
    game_world.add_object(house_1, 0)
    # game_world.add_object(stone_2, 0)

    # game_world.add_collision_pair('house:stone', house_1, blue_stone_1)
    # game_world.add_collision_pair('house:stone', house_1, red_stone_1)
    # game_world.add_collision_pair('stone:stone', stone_1, stone_2)
    pass

def finish():
    game_world.clear()
    pass

def handle_events():
    global running
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.change_mode(title_mode)
        else:
            blue_stone_1.handle_event(event)
    pass

def update():
    game_world.update_object()
    game_world.handle_collisions()

def draw():
    clear_canvas()
    game_world.render_object()
    update_canvas()
    pass

def pause():
    pass

def resume():
    pass