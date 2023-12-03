from pico2d import get_events, load_image, clear_canvas, update_canvas, get_time
from sdl2 import SDL_QUIT, SDL_KEYDOWN, SDLK_ESCAPE, SDLK_SPACE, SDL_MOUSEMOTION, SDL_MOUSEBUTTONDOWN, SDL_MOUSEBUTTONUP

import game_framework
import play_mode


def init():
    global image
    global main_image
    global start_image
    global method_image
    global Act_Button_1, Act_Button_2
    Act_Button_1, Act_Button_2 = 0, 0
    image = load_image('Title_1280x800.png')
    main_image = load_image('Main_Image_1280x800.png')
    start_image = load_image('Game_Start_Banner_320x384.png')
    method_image = load_image('Game_Method_Banner_320x384.png')


def finish():
    global image
    global main_image
    global start_image
    global method_image
    del image
    del main_image
    del start_image
    del method_image

def update():
    pass

def draw():
    clear_canvas()
    image.clip_draw_to_origin(0, 0, 1280, 800, 0, 0)
    main_image.clip_draw_to_origin(0, 0, 1280, 800, 0, 0)
    start_image.clip_draw_to_origin(0, 0 + 128 * Act_Button_1, 320, 128, 1280 - 350, 200)
    method_image.clip_draw_to_origin(0, 0 + 128 * Act_Button_2, 320, 128, 1280 - 350, 50)
    update_canvas()
    pass

def handle_events():
    global Act_Button_1, Act_Button_2
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_SPACE):
            game_framework.change_mode(play_mode)
        elif event.type == SDL_MOUSEMOTION or event.type == SDL_MOUSEBUTTONDOWN or event.type == SDL_MOUSEBUTTONUP:
            if event.x >= 1280 - 350 and event.x <= 1280 - 350 + 320 and 800 - 1 - event.y >= 200 and 800 - 1 - event.y <= 200 + 128:
                if event.type == SDL_MOUSEBUTTONDOWN:
                    Act_Button_1 = 2
                else:
                    Act_Button_1 = 1
                if event.type == SDL_MOUSEBUTTONUP:
                    game_framework.change_mode(play_mode)
            else:
                Act_Button_1 = 0
            if event.x >= 1280 - 350 and event.x <= 1280 - 350 + 320 and 800 - 1 - event.y >= 50 and 800 - 1 - event.y <= 50 + 128:
                if event.type == SDL_MOUSEBUTTONDOWN:
                    Act_Button_2 = 2
                else:
                    Act_Button_2 = 1
                if event.type == SDL_MOUSEBUTTONUP:
                    pass
            else:
                Act_Button_2 = 0

def pause():
    pass

def resume():
    pass