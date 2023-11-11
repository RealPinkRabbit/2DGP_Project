from pico2d import open_canvas, delay, close_canvas
import play_mode
import logo_mode as start_mode
# import play_mode as start_mode
import game_framework

open_canvas(play_mode.canvas_width, play_mode.canvas_height)
game_framework.run(start_mode)
# play_mode.init()
# while play_mode.running:
#     play_mode.handle_events()
#     play_mode.update()
#     play_mode.draw()
#     delay(0.01)
# play_mode.finish()
close_canvas()