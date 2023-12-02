from pico2d import get_events, load_image, clear_canvas, update_canvas, get_time
from sdl2 import SDL_QUIT, SDL_KEYDOWN, SDLK_ESCAPE, SDLK_SPACE

import game_framework
import play_mode


def init():
    global image
    global start_image
    global method_image
    image = load_image('Title_1280x800.png')
    start_image = load_image('Game_Start_Banner_320x256.png')
    method_image = load_image('Game_Method_Banner_320x256.png')


def finish():
    global image
    global start_image
    global method_image
    del image
    del start_image
    del method_image

def update():
    pass

def draw():
    clear_canvas()
    image.clip_draw_to_origin(0, 0, 1280, 800, 0, 0)
    update_canvas()
    pass

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_SPACE):
            game_framework.change_mode(play_mode)


def pause():
    pass

def resume():
    pass