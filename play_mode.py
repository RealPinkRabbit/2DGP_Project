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

current_end = 1
total_end = 6
blue_remained_stone = 8
red_remained_stone = 8
blue_score = []
red_score = []
playing_stone = [] # moving stone
moved_stone = []
playing_background = None


def init():
    global running
    global playing_background
    global playing_stone
    global house_1
    global mini_map_1
    global score_pane_1

    playing_stone = []
    running = True

    mini_map_1 = mini_map()
    score_pane_1 = score_pane()

    playing_background = background()
    playing_stone.append(blue_stone(200 + 552//2, 600, 0, 0))
    house_1 = house()

    game_world.add_object(playing_background, 0)
    game_world.add_object(mini_map_1, 4)
    game_world.add_object(score_pane_1, 4)
    game_world.add_object(playing_stone[0], 2)
    game_world.add_object(house_1, 1)

    game_world.add_collision_pair('house:stone', house_1, playing_stone[0])
    game_world.add_collision_pair('stone:stone', playing_stone[0], playing_stone[0])
    pass

def finish():
    game_world.clear()
    pass

def handle_events():
    global running
    global playing_background
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            playing_background.bgm.set_volume(8)
            game_framework.push_mode(pause_mode)
            # game_framework.quit()
        # elif event.type == SDL_KEYDOWN and event.key == SDLK_SPACE:
        #     game_framework.change_mode(result_mode)
        else:
            playing_stone[0].handle_event(event)

    pass

def update():
    global playing_stone
    game_world.update_object()
    game_world.handle_collisions()
    for stones in playing_stone:
        if stones.vx == 0 and stones.vy == 0 and stones.is_launched == True:
            for pairs in game_world.objects:
                for o in pairs:
                    if playing_stone[0] == o:
                        game_world.change_depth(o, 3)
            playing_stone[0].is_handling = False
            playing_stone.clear()
            playing_stone.append(blue_stone(200 + 552//2, 600, 0, 0))
            game_world.add_object(playing_stone[0], 2)
            game_world.add_collision_pair('house:stone', None, playing_stone[0])
            game_world.add_collision_pair('stone:stone', playing_stone[0], playing_stone[0])
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