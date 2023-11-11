# 모든 화면 상에 그려지는 객체들은
# update()함수, draw()함수를 꼭 가져야 함
from math import pow

objects = [ [] for _ in range(5) ] # 시각 월드
collision_pairs = {} # 충돌 월드


def add_object(o, depth = 0):
    objects[depth].append(o)


def remove_collision_object(o):
    for pairs in collision_pairs.values():
        if o in pairs[0]:
            pairs[0].remove(o)
        if o in pairs[1]:
            pairs[1].remove(o)


def remove_object(o):
    for layer in objects:
        if o in layer:
            layer.remove(o)
            remove_collision_object(o)
            return
    raise ValueError('Cannont delete non existing object')

def update_object():
    for layer in objects:
        for o in layer:
            o.update()
def render_object():
    for layer in objects:
        for o in layer:
            o.draw()

def collide(a, b):
    a_x, a_y, a_rad = a.get_bc()
    b_x, b_y, b_rad = b.get_bc()

    if (pow(a_x-b_x,2)+pow(a_y-b_y,2) > pow(a_rad+b_rad,2)):
        return False
    return True

def add_collision_pair(group, a, b):
    if group not in collision_pairs:
        print(f'Added new group {group}')
        collision_pairs[group] = [ [], [] ]
    if a:
        collision_pairs[group][0].append(a)
    if b:
        collision_pairs[group][1].append(b)

def handle_collisions():
    for group, pairs in collision_pairs.items():
        for a in pairs[0]:
            for b in pairs[1]:
                if collide(a, b):
                    a.handle_collision(group, b)
                    b.handle_collision(group, a)