from pico2d import get_events, load_image, clear_canvas, update_canvas, get_time
import game_framework
import play_mode
import title_mode


def init():
    global image
    global logo_start_time

    image = load_image('tuk_credit_1280x800.png')
    logo_start_time = get_time()


def finish():
    pass

def update():
    if get_time() - logo_start_time >= 2.0:
        game_framework.change_mode(title_mode)
    pass

def draw():
    clear_canvas()
    image.draw(640, 400)
    update_canvas()
    pass

def handle_events():
    events = get_events()

def pause():
    pass

def resume():
    pass