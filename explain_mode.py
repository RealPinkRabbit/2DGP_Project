from pico2d import get_events, load_image, clear_canvas, update_canvas, get_time, load_music
from sdl2 import SDL_QUIT, SDL_KEYDOWN, SDLK_ESCAPE, SDLK_SPACE, SDL_MOUSEMOTION, SDL_MOUSEBUTTONDOWN, SDL_MOUSEBUTTONUP

import game_framework
import play_mode
import title_mode


def init():
    global image
    global return_image
    global Act_Button_1
    Act_Button_1 = 0
    image = load_image('Title_1280x800.png')
    return_image = load_image('Return_Banner_320x384.png')


def finish():
    global image
    global return_image
    del image
    del return_image


def update():
    pass


def draw():
    clear_canvas()
    image.clip_draw_to_origin(0, 0, 1280, 800, 0, 0)
    return_image.clip_draw_to_origin(0, 0 + 128 * Act_Button_1, 320, 128, 1280 - 350, 50)
    update_canvas()
    pass


def handle_events():
    global Act_Button_1
    global image
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.pop_mode()
        elif event.type == SDL_MOUSEMOTION or event.type == SDL_MOUSEBUTTONDOWN or event.type == SDL_MOUSEBUTTONUP:
            if event.x >= 1280 - 350 and event.x <= 1280 - 350 + 320 and 800 - 1 - event.y >= 50 and 800 - 1 - event.y <= 50 + 128:
                if event.type == SDL_MOUSEBUTTONDOWN:
                    Act_Button_1 = 2
                else:
                    Act_Button_1 = 1
                if event.type == SDL_MOUSEBUTTONUP:
                    game_framework.pop_mode()
            else:
                Act_Button_1 = 0


def pause():
    pass


def resume():
    pass
