import pico2d
import play_mode

pico2d.open_canvas(play_mode.canvas_width, play_mode.canvas_height)
play_mode.init()
while play_mode.running:
    play_mode.handle_events()
    play_mode.update()
    play_mode.draw()
    pico2d.delay(0.01)
play_mode.finish()
pico2d.close_canvas()