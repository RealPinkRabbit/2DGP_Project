from pico2d import *

import game_framework
import pause_mode
import result_mode
import title_mode
from stone import blue_stone, red_stone
from house import house
import game_world
from background import FixedBackground as background
from math import *
from mini_map import mini_map
from score_pane import score_pane

canvas_width = 1280
canvas_height = 800

def init():
    global running
    global playing_background
    global playing_stone
    # global blue_stone_1
    # global blue_stone_2, blue_stone_3
    # global red_stone_1
    # global red_stone_2
    global house_1
    global mini_map_1
    global score_pane_1

    playing_stone = []
    running = True

    mini_map_1 = mini_map()
    score_pane_1 = score_pane()

    playing_background = background()
    # blue_stone_1 = blue_stone(400, 400 - 64, 0, 0)
    playing_stone.append(blue_stone(200 + 552//2, 600, 0, 0))
    # blue_stone_2 = blue_stone(400, 400, 0, 0)
    # blue_stone_3 = blue_stone(400, 400 + 64, 0, 0)
    #
    # red_stone_1 = red_stone(800, 550, 0, 0)
    # red_stone_2 = red_stone(800, 450, 0, 0)
    house_1 = house()

    game_world.add_object(playing_background, 0)
    game_world.add_object(mini_map_1)
    game_world.add_object(score_pane_1)
    game_world.add_object(playing_stone[0], 3)
    # game_world.add_object(blue_stone_2, 3)
    # game_world.add_object(blue_stone_3, 3)
    # game_world.add_object(red_stone_1, 2)
    # game_world.add_object(red_stone_2, 2)
    game_world.add_object(house_1, 1)

    game_world.add_collision_pair('house:stone', house_1, playing_stone[0])
    # game_world.add_collision_pair('house:stone', None, blue_stone_2)
    # game_world.add_collision_pair('house:stone', None, blue_stone_3)
    # game_world.add_collision_pair('house:stone', None, red_stone_1)
    # game_world.add_collision_pair('house:stone', None, red_stone_2)
    game_world.add_collision_pair('stone:stone', playing_stone[0], playing_stone[0])
    # game_world.add_collision_pair('stone:stone', blue_stone_2, blue_stone_2)
    # game_world.add_collision_pair('stone:stone', blue_stone_3, blue_stone_3)
    # game_world.add_collision_pair('stone:stone', red_stone_1, red_stone_1)
    # game_world.add_collision_pair('stone:stone', red_stone_2, red_stone_2)

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
            game_framework.push_mode(pause_mode)
            # game_framework.quit()
        # elif event.type == SDL_KEYDOWN and event.key == SDLK_SPACE:
        #     game_framework.change_mode(result_mode)
        else:
            if playing_stone[0] != None:
                playing_stone[0].handle_event(event)
            else:
                pass
    pass

def update():
    game_world.update_object()
    game_world.handle_collisions()
    delay(0.01)

def draw():
    clear_canvas()
    game_world.render_object()
    update_canvas()
    pass

def pause():
    pass

def resume():
    pass