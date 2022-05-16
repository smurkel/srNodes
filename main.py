import glfw
import OpenGL.GL
import config as cfg
import gui as gui
import window
import input

if __name__ == "__main__":
    application_window = window.start()
    input.start(application_window)
    gui.start(application_window)
    while not glfw.window_should_close(application_window):

        window.on_update()
        input.on_update()
        gui.on_update()
        window.end_frame()

    gui.exit()
    window.exit()