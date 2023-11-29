from pico2d import *

import game_framework
import title_mode
from stone import blue_stone, red_stone
from house import house
import game_world
from background import background
from math import *

canvas_width = 1280
canvas_height = 800

def init():
    global running
    global playing_background
    global blue_stone_1, blue_stone_2
    global red_stone_1
    global red_stone_2
    global house_1

    running = True

    playing_background = background()
    blue_stone_1 = blue_stone(400, 400, 0, 0)
    blue_stone_2 = blue_stone(800, 200, 0, 0)
    red_stone_1 = red_stone(800, 550, 0, 0)
    red_stone_2 = red_stone(800, 450, 0, 0)
    house_1 = house()

    game_world.add_object(playing_background, 0)
    game_world.add_object(blue_stone_1, 3)
    game_world.add_object(blue_stone_2, 3)
    game_world.add_object(red_stone_1, 2)
    game_world.add_object(red_stone_2, 2)
    game_world.add_object(house_1, 1)

    game_world.add_collision_pair('house:stone', house_1, blue_stone_1)
    game_world.add_collision_pair('house:stone', None, blue_stone_2)
    game_world.add_collision_pair('house:stone', None, red_stone_1)
    game_world.add_collision_pair('house:stone', None, red_stone_2)
    game_world.add_collision_pair('stone:stone', blue_stone_1, blue_stone_2)
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
            # game_framework.change_mode(title_mode)
            game_framework.quit()
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