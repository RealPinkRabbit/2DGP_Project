from pico2d import get_events, load_image, clear_canvas, update_canvas, get_time
from sdl2 import SDL_QUIT, SDL_KEYDOWN, SDLK_ESCAPE, SDLK_SPACE, SDL_MOUSEMOTION, SDL_MOUSEBUTTONDOWN, SDL_MOUSEBUTTONUP

import game_framework
import game_world
import play_mode
import title_mode


def init():
    global pause_image
    global resume_image
    global quit_image
    global Act_Button_3, Act_Button_4
    Act_Button_3, Act_Button_4 = 0, 0
    pause_image = load_image('Pause_image_1280x800.png')
    resume_image = load_image('Resume_Banner_384x240.png')
    quit_image = load_image('Quit_Banner_256x240.png')


def finish():
    global pause_image
    global resume_image
    global quit_image
    del pause_image
    del resume_image
    del quit_image

def update():
    pass

def draw():
    clear_canvas()
    pause_image.clip_draw_to_origin(0, 0, 1280, 800, 0, 0)
    resume_image.clip_draw_to_origin(0, 0 + 80*Act_Button_3, 384, 80, 640 - 384//2, 350 - 80//2)
    quit_image.clip_draw_to_origin(0, 0 + 80*Act_Button_4, 256, 80, 640 - 256//2, 200 - 80//2)
    update_canvas()

def handle_events():
    global Act_Button_3, Act_Button_4
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.pop_mode()
        elif event.type == SDL_MOUSEMOTION or event.type == SDL_MOUSEBUTTONDOWN or event.type == SDL_MOUSEBUTTONUP:
            if event.x >= 640 - 384//2 and event.x <= 640 - 384//2 + 384 and 800 - 1 - event.y >= 350 - 80//2 and 800 - 1 - event.y <= 350 - 80//2 + 80:
                if event.type == SDL_MOUSEBUTTONDOWN:
                    Act_Button_3 = 2
                else:
                    Act_Button_3 = 1
                if event.type == SDL_MOUSEBUTTONUP:
                    game_framework.pop_mode()
            else:
                Act_Button_3 = 0
            if event.x >= 640 - 256//2 and event.x <= 640 - 256//2 + 256 and 800 - 1 - event.y >= 200 - 80//2 and 800 - 1 - event.y <= 200 - 80//2 + 80:
                if event.type == SDL_MOUSEBUTTONDOWN:
                    Act_Button_4 = 2
                else:
                    Act_Button_4 = 1
                if event.type == SDL_MOUSEBUTTONUP:
                    game_world.clear()
                    game_framework.pop_mode()
                    game_framework.change_mode(title_mode)
            else:
                Act_Button_4 = 0

def pause():
    pass

def resume():
    pass