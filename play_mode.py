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
blue_remained_stone = 1
red_remained_stone = 1
blue_score = [0, 0, 0, 0, 0, 0]
red_score = [0, 0, 0, 0, 0, 0]
playing_stone = [] # moving stone
playing_stone_pointer = 0
moved_stone = []
first_attack = 'BLUE'
playing_background = None
frame = 0
waiting_count = 0


def init():
    global running
    global playing_background
    global playing_stone
    global house_1
    global mini_map_1
    global score_pane_1
    global focus

    focus = load_image('Focus_64x64.png')

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
    global playing_stone_pointer
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
            playing_stone[playing_stone_pointer].handle_event(event)

    pass

def update():
    global playing_stone
    global playing_stone_pointer
    global blue_remained_stone
    global red_remained_stone
    global frame
    global waiting_count
    frame = (frame + 1) % 60
    game_world.update_object()
    game_world.handle_collisions()
    # playing_stone에 의해 움직이고 있는 공을 실시간으로 추가
    for pairs in game_world.objects:
        for stones in pairs:
            if stones.__class__.__name__ == 'blue_stone' or stones.__class__.__name__ == 'red_stone':
                if stones.is_launched == True and stones.is_handling == False:
                    if stones not in playing_stone:
                        if stones.vx != 0 or stones.vy != 0:
                            playing_stone.append(stones)
                    else:
                        if stones.vx == 0 and stones.vy == 0:
                            if len(playing_stone)-1 == playing_stone_pointer:
                                playing_stone_pointer -= 1
                            playing_stone.remove(stones)
    # playing_stone 내 모든 공이 멈추면 다음 공 가져오기
    for stones in playing_stone:
        if stones.vx == 0 and stones.vy == 0 and stones.is_launched == True:
            waiting_count += 1
            if waiting_count == 5:
                waiting_count = 0
                for pairs in game_world.objects:
                    for o in pairs:
                        if playing_stone[0] == o:
                            game_world.change_depth(o, 3)
                playing_stone[0].is_handling = False
                playing_stone_pointer = 0
                if playing_stone[0].color == 'BLUE':
                    playing_stone.clear()
                    blue_remained_stone -= 1
                    playing_stone.append(red_stone(200 + 552//2, 600, 0, 0))
                elif playing_stone[0].color == 'RED':
                    playing_stone.clear()
                    red_remained_stone -= 1
                    playing_stone.append(blue_stone(200 + 552//2, 600, 0, 0))
                game_world.add_object(playing_stone[0], 2)
                game_world.add_collision_pair('house:stone', None, playing_stone[0])
                game_world.add_collision_pair('stone:stone', playing_stone[0], playing_stone[0])
        else:
            waiting_count = 0
    # 엔드가 끝났다면, 다음 엔드로 넘어가기
    if check_finished_end() == True:
        reset_end()
    delay(0.01)

def draw():
    global playing_stone
    clear_canvas()
    game_world.render_object()
    focus.clip_draw(0, 0, 64, 64, playing_stone[playing_stone_pointer].sx, playing_stone[playing_stone_pointer].sy)
    update_canvas()
    pass

def pause():
    pass

def resume():
    pass

def check_finished_end():
    global blue_remained_stone
    global red_remained_stone
    if blue_remained_stone == 0 and red_remained_stone == 0:
        return True
    return False

def reset_end():
    global current_end
    global blue_remained_stone
    global red_remained_stone
    global house_1
    global blue_score
    global red_score
    global first_attack
    blue_remained_stone = 8
    red_remained_stone = 8
    # 점수 책정
    if house_1.score_color == 'BLUE':
        blue_score[current_end - 1] = house_1.score
    elif house_1.score_color == 'RED':
        red_score[current_end - 1] = house_1.score
    current_end += 1
    # print(blue_score)
    # print(red_score)

    # 게임월드 돌 삭제
    for pairs in game_world.objects:
        for stones in pairs:
            if stones.__class__.__name__ == 'blue_stone' or stones.__class__.__name__ == 'red_stone':
                game_world.remove_object(stones)
                game_world.remove_collision_object(stones)
    playing_stone.clear()
    if first_attack == 'BLUE':
        first_attack = 'RED'
        playing_stone.append(red_stone(200 + 552 // 2, 600, 0, 0))
    elif first_attack == 'RED':
        first_attack = 'BLUE'
        playing_stone.append(red_stone(200 + 552 // 2, 600, 0, 0))
    game_world.add_object(playing_stone[0], 2)
    game_world.add_collision_pair('house:stone', None, playing_stone[0])
    game_world.add_collision_pair('stone:stone', playing_stone[0], playing_stone[0])

    pass