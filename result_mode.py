from pico2d import get_events, load_image, clear_canvas, update_canvas, get_time
from sdl2 import SDL_QUIT, SDL_KEYDOWN, SDLK_ESCAPE, SDLK_SPACE, SDL_MOUSEMOTION, SDL_MOUSEBUTTONDOWN, SDL_MOUSEBUTTONUP

import game_framework
import play_mode
import title_mode


def init():
    global result_image
    global result_pane_image
    result_image = load_image('Result_1280x800.png')
    result_pane_image = load_image('Result_Pane_1280x800.png')


def finish():
    global result_image
    global result_pane_image
    del result_image
    del result_pane_image

def update():
    pass

def draw():
    clear_canvas()
    result_image.clip_draw_to_origin(0, 0, 1280, 800, 0, 0)
    result_pane_image.draw(640, 400)
    update_canvas()
    pass

def handle_events():
    global Act_Button_1, Act_Button_2
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.change_mode(title_mode)

def pause():
    pass

def resume():
    pass