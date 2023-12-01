from pico2d import *

def get_pow_distance(ax, ay, ox, oy):
    return pow(int(ox-ax), 2) + pow(int(oy-ay), 2)

class house:
    image = None

    def __init__(self):
        self.x, self.y = 800, 400
        self.radius = 200
        self.stones = []
        self.stones_clone = []
        self.score_color = '--'
        self.score = 0
        self.RGB = (0, 0, 0)
        self.font = load_font('ENCR10B.TTF', 64)

        if house.image == None:
            house.image = load_image('House_400x400.png')

    def draw(self):
        self.image.draw(self.x, self.y)
        if len(self.stones_clone) == 0:
            self.RGB = (0, 0, 0)
        elif self.score_color == '--':
            self.RGB = (0, 0, 0)
        elif self.stones_clone[0][0] == 'RED':
            self.RGB = (255, 0, 0)
        elif self.stones_clone[0][0] == 'BLUE':
            self.RGB = (0, 0, 255)
        self.font.draw(self.x - 170, self.y + 250, f'{self.score_color} : {self.score}', self.RGB)

    def update(self):
        self.stones_clone = self.stones.copy()
        self.sort_distance()
        self.update_score()
        self.stones.clear()
        pass

    def get_bc(self):
        return self.x, self.y, self.radius

    def handle_collision(self, group, oppo):
        if group == 'house:stone':
            self.stones.append((oppo.color, get_pow_distance(self.x, self.y, oppo.x, oppo.y)))
            pass

    def sort_distance(self):
        if len(self.stones_clone) < 2:
            return
        for i in range(0, len(self.stones_clone)-1):
            for j in range(0, len(self.stones_clone)-i-1):
                if self.stones_clone[j][1] > self.stones_clone[j+1][1]:
                    self.stones_clone[j], self.stones_clone[j+1] = self.stones_clone[j+1], self.stones_clone[j]

    def update_score(self):
        if len(self.stones) == 0:
            self.score_color = '--'
            self.score = 0
            return
        elif len(self.stones) == 1:
            self.score = 1
            self.score_color = self.stones_clone[0][0]
        else:
            self.score_color = self.stones_clone[0][0]
            if self.stones_clone[0][1] == self.stones_clone[1][1]:
                self.score_color = '--'
                self.score = 0
                return
            self.score = 1
            for i in range(0, len(self.stones_clone)-1):
                if self.stones_clone[i][0] != self.stones_clone[i+1][0]:
                    if self.stones_clone[i][1] == self.stones_clone[i+1][1]:
                        self.score -= 1
                    return
                else:
                    self.score += 1