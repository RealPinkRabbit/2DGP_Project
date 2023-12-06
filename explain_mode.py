from pico2d import get_events, load_image, clear_canvas, update_canvas, get_time, load_music, load_font
from sdl2 import SDL_QUIT, SDL_KEYDOWN, SDLK_ESCAPE, SDLK_SPACE, SDL_MOUSEMOTION, SDL_MOUSEBUTTONDOWN, SDL_MOUSEBUTTONUP

import game_framework
import play_mode
import title_mode


def init():
    global image
    global return_image
    global explain_pane_image
    global Act_Button_1
    global explain_font
    Act_Button_1 = 0
    image = load_image('Title_1280x800.png')
    return_image = load_image('Return_Banner_320x384.png')
    explain_pane_image = load_image('Explain_Pane_1280x800.png')
    explain_font = load_font('Maplestory Bold.ttf', 30)


def finish():
    global image
    global return_image
    global explain_pane_image
    del image
    del return_image
    del explain_pane_image

def update():
    pass


def draw():
    clear_canvas()
    image.clip_draw_to_origin(0, 0, 1280, 800, 0, 0)
    explain_pane_image.clip_draw_to_origin(0, 0, 1280, 800 ,0 ,0)
    explain_font.draw(100, 550, '● 본 게임은 동계 스포츠 종목인 컬링을 모델로 하여 제작된 게임입니다.', (255, 255, 255))
    explain_font.draw(100, 500, '● 게임은 총 6세트(엔드)로 구성됩니다', (255, 255, 255))
    explain_font.draw(100, 450, '● 각 세트(엔드) 당 빨강/파랑 팀이 번갈아 가며 각각 8개의 스톤을 투구 합니다.', (255, 255, 255))
    explain_font.draw(100, 400, '● 하우스에 가장 밀접한 스톤 기준으로 점수를 획득하며, 보다 많은 득점을 한 팀이 승리합니다.', (255, 255, 255))
    explain_font.draw(100, 350, '★ 조작법', (255, 255, 255))
    explain_font.draw(100, 300, '    (투구 전)       ↑,↓ : 공의 세기 조작    ←,→ : 공의 투구 위치 조작', (255, 255, 255))
    explain_font.draw(100, 250, '    (투구 후)       ↑,←,→ : 스위핑 조작', (255, 255, 255))
    explain_font.draw(100, 200, '                     a,d : 움직이는 다른 스톤 조작', (255, 255, 255))
    explain_font.draw(100, 150, '     (항시)         w : 하우스 상황 확인', (255, 255, 255))
    explain_font.draw(100, 100, '                     ESC : 일시정지', (255, 255, 255))
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
