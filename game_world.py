# 모든 화면 상에 그려지는 객체들은
# update()함수, draw()함수를 꼭 가져야 함

objects = [ [] for _ in range(10) ]

def add_object(o, depth = 0):
    objects[depth].append(o)

def remove_object(o):
    for layer in objects:
        if o in layer:
            layer.remove(o)
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