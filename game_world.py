objects = []

def add_object(o):
    objects.append(o)

def update_object():
    for o in objects:
        o.update()

def render():
    for o in objects:
        o.draw()