from pico2d import *

import play_mode


class score_pane:
    image = None
    Blue_Stone_image = None
    Red_Stone_image = None
    Stone_Pointer = None

    def __init__(self):
        self.font = load_font('Maplestory Bold.ttf', 32)
        self.x = 200 + 552 + (1280 - (200 + 552)) // 2 - 200
        self.y = 800 // 2 - 500 // 2 + 100
        if score_pane.image == None:
            score_pane.image = load_image('Score_Pane_400x500.png')
        if score_pane.Blue_Stone_image == None:
            score_pane.Blue_Stone_image = load_image('Stone_Blue_64x64.png')
        if score_pane.Red_Stone_image == None:
            score_pane.Red_Stone_image = load_image('Stone_Red_64x64.png')
        if score_pane.Stone_Pointer == None:
            score_pane.Stone_Pointer = load_image('Stone_Pointer_64x64.png')

    def draw(self):
        self.image.clip_draw_to_origin(0, 0, 400, 500, self.x, self.y)
        self.font.draw(self.x + 20, self.y + 470, f'{play_mode.current_end}', (255, 255, 255))
        self.font.draw(self.x + 60, self.y + 430, f'{play_mode.total_end}', (255, 255, 255))
        for i in range(len(play_mode.blue_score)):
            if i+1 < play_mode.current_end:
                self.font.draw(self.x + 165 + i * 40, self.y + 425, f'{play_mode.blue_score[i]}', (255, 255, 255))
            else:
                self.font.draw(self.x + 165 + i * 40, self.y + 425, f'{play_mode.blue_score[i]}', (255, 255, 255))
                # self.font.draw(self.x + 170 + i * 40, self.y + 425, '-', (255, 255, 255))
        for i in range(len(play_mode.red_score)):
            if i+1 < play_mode.current_end:
                self.font.draw(self.x + 165 + i * 40, self.y + 470, f'{play_mode.red_score[i]}', (255, 255, 255))
            else:
                self.font.draw(self.x + 165 + i * 40, self.y + 470, f'{play_mode.red_score[i]}', (255, 255, 255))
                # self.font.draw(self.x + 170 + i * 40, self.y + 470, '-', (255, 255, 255))
        for i in range(play_mode.blue_remained_stone):
            score_pane.Blue_Stone_image.draw(self.x + 80 + (i%4) * 80, self.y + 140 - (i//4) * 80)
            if i+1 == play_mode.blue_remained_stone and play_mode.playing_stone[0].color == 'BLUE':
                score_pane.Stone_Pointer.draw(self.x + 80 + (i%4) * 80, self.y + 140 - (i//4) * 80)
        for i in range(play_mode.red_remained_stone):
            score_pane.Red_Stone_image.draw(self.x + 80 + (i%4) * 80, self.y + 340 - (i//4) * 80)
            if i+1 == play_mode.red_remained_stone and play_mode.playing_stone[0].color == 'RED':
                score_pane.Stone_Pointer.draw(self.x + 80 + (i%4) * 80, self.y + 340 - (i//4) * 80)
        # self.image.draw(self.sx, self.sy)
        # stone.font.draw(stone.sx + stone.card_dx - 10, stone.sy + stone.card_dy, f'{stone.message}', (0, 0, 0))
        # self.font.draw(self.sx - 170, self.sy + 250, f'{self.score_color} : {self.score}', self.RGB)
        pass

    def update(self):
        # self.sx = self.x - play_mode.playing_background.window_left
        # self.sy = self.y - play_mode.playing_background.window_bottom
        # self.stones_clone = self.stones.copy()
        # self.sort_distance()
        # self.update_score()
        # self.stones.clear()
        pass
