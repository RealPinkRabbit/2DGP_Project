from pico2d import get_events, load_image, clear_canvas, update_canvas, get_time, load_font, load_music
from sdl2 import SDL_QUIT, SDL_KEYDOWN, SDLK_ESCAPE, SDLK_SPACE, SDL_MOUSEMOTION, SDL_MOUSEBUTTONDOWN, SDL_MOUSEBUTTONUP

import game_framework
import play_mode
import stone
import title_mode


def init():
    global result_image
    global result_pane_image
    global cat_standing_image
    global cat_happy_image
    global cat_sad_image
    global duck_standing_image
    global duck_happy_image
    global duck_sad_image
    global Blue_team
    global Red_team
    global Blue_score
    global Red_score
    global result_font
    global small_result_font
    global start_time
    result_image = load_image('Result_1280x800.png')
    result_image.bgm = load_music('Curling_Result.mp3')
    result_image.bgm.set_volume(32)
    result_image.bgm.play()
    result_pane_image = load_image('Result_Pane_1280x800.png')
    cat_standing_image = load_image('Cat_Standing_1280x800.png')
    cat_happy_image = load_image('Cat_Happy_1280x800.png')
    cat_sad_image = load_image('Cat_Sad_1280x800.png')
    duck_standing_image = load_image('Duck_Standing_1280x800.png')
    duck_happy_image = load_image('Duck_Happy_1280x800.png')
    duck_sad_image = load_image('Duck_Sad_1280x800.png')
    Blue_team = load_image('Stone_Blue_64x64.png')
    Red_team = load_image('Stone_Red_64x64.png')
    Blue_score = 0
    Red_score = 0
    for i in play_mode.blue_score:
        Blue_score += i
    for i in play_mode.red_score:
        Red_score += i
    result_font = load_font('Maplestory Bold.ttf', 128)
    small_result_font = load_font('Maplestory Bold.ttf', 32)
    start_time = get_time()


def finish():
    global result_image
    global result_pane_image
    global cat_standing_image
    global cat_happy_image
    global cat_sad_image
    global duck_standing_image
    global duck_happy_image
    global duck_sad_image
    global Blue_team
    global Red_team
    del result_image
    del result_pane_image
    del cat_standing_image
    del cat_happy_image
    del cat_sad_image
    del duck_standing_image
    del duck_happy_image
    del duck_sad_image
    del Blue_team
    del Red_team
    play_mode.blue_score = [0, 0, 0, 0, 0, 0]
    play_mode.red_score = [0, 0, 0, 0, 0, 0]

def update():
    pass


def draw():
    clear_canvas()
    result_image.clip_draw_to_origin(0, 0, 1280, 800, 0, 0)
    result_pane_image.draw(640, 400)
    if get_time() - start_time >= 1.0:
        Blue_team.draw(640 - 320, 550)
        Red_team.draw(640 + 320, 550)
    if get_time() - start_time >= 2.0 and get_time() - start_time < 4.0:
        if stone.blue_stone.character == 'DUCK':
            duck_standing_image.clip_draw(0, 0, 1280, 800, 640 - 320, 400, 320, 200)
        elif stone.blue_stone.character == 'CAT':
            cat_standing_image.clip_draw(0, 0, 1280, 800, 640 - 320, 400, 320, 200)
        if stone.red_stone.character == 'DUCK':
            duck_standing_image.clip_draw(0, 0, 1280, 800, 640 + 320, 400, 320, 200)
        elif stone.red_stone.character == 'CAT':
            cat_standing_image.clip_draw(0, 0, 1280, 800, 640 + 320, 400, 320, 200)
    if get_time() - start_time >= 3.0:
        result_font.draw(540 - 20, 400, f'{Blue_score}', (200, 200, 255))
        result_font.draw(640 - 20, 400, ':', (255, 255, 255))
        result_font.draw(740 - 20, 400, f'{Red_score}', (255, 200, 200))
    if get_time() - start_time >= 4.0:
        if Blue_score > Red_score:
            result_font.draw(640 - 320 - 150, 200, 'WIN', (255, 255, 0))
            result_font.draw(640 + 320 - 150, 200, 'LOSE', (255, 0, 255))
            if stone.blue_stone.character == 'DUCK':
                duck_happy_image.clip_draw(0, 0, 1280, 800, 640 - 320, 400, 320, 200)
            elif stone.blue_stone.character == 'CAT':
                cat_happy_image.clip_draw(0, 0, 1280, 800, 640 - 320, 400, 320, 200)
            if stone.red_stone.character == 'DUCK':
                duck_sad_image.clip_draw(0, 0, 1280, 800, 640 + 320, 400, 320, 200)
            elif stone.red_stone.character == 'CAT':
                cat_sad_image.clip_draw(0, 0, 1280, 800, 640 + 320, 400, 320, 200)
        elif Blue_score < Red_score:
            result_font.draw(640 - 320 - 150, 200, 'LOSE', (255, 0, 255))
            result_font.draw(640 + 320 - 150, 200, 'WIN', (255, 255, 0))
            if stone.blue_stone.character == 'DUCK':
                duck_sad_image.clip_draw(0, 0, 1280, 800, 640 - 320, 400, 320, 200)
            elif stone.blue_stone.character == 'CAT':
                cat_sad_image.clip_draw(0, 0, 1280, 800, 640 - 320, 400, 320, 200)
            if stone.red_stone.character == 'DUCK':
                duck_happy_image.clip_draw(0, 0, 1280, 800, 640 + 320, 400, 320, 200)
            elif stone.red_stone.character == 'CAT':
                cat_happy_image.clip_draw(0, 0, 1280, 800, 640 + 320, 400, 320, 200)
        elif Blue_score == Red_score:
            result_font.draw(640 - 150, 200, 'DRAW', (0, 255, 0))
            if stone.blue_stone.character == 'DUCK':
                duck_happy_image.clip_draw(0, 0, 1280, 800, 640 - 320, 400, 320, 200)
            elif stone.blue_stone.character == 'CAT':
                cat_happy_image.clip_draw(0, 0, 1280, 800, 640 - 320, 400, 320, 200)
            if stone.red_stone.character == 'DUCK':
                duck_happy_image.clip_draw(0, 0, 1280, 800, 640 + 320, 400, 320, 200)
            elif stone.red_stone.character == 'CAT':
                cat_happy_image.clip_draw(0, 0, 1280, 800, 640 + 320, 400, 320, 200)
    if get_time() - start_time >= 6.0:
        small_result_font.draw(720, 100, 'ESC 키를 눌러서 타이틀 화면으로...', (150, 150, 150))
    update_canvas()
    pass


def handle_events():
    global Act_Button_1, Act_Button_2
    global result_image
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE and get_time() - start_time >= 6.0:
            result_image.bgm.stop()
            game_framework.change_mode(title_mode)


def pause():
    pass


def resume():
    pass
