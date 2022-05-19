import glfw
window = None

cursor_pos = [0, 0]
mouse_event = None
MOUSE_BUTTON_LEFT = 0
MOUSE_BUTTON_RIGHT = 1
MOUSE_BUTTON_MIDDLE = 2
MOUSE_BUTTON_CLICK = 1
MOUSE_BUTTON_RELEASE = 0

def start(glfwwindow):
    global window
    window = glfwwindow
    glfw.set_mouse_button_callback(window, mouse_button_callback)


def on_update():
    global cursor_pos, mouse_event
    mouse_event = None
    cursor_pos = glfw.get_cursor_pos(window)
    glfw.poll_events()

def mouse_button_callback(window, button, action, mods):
    global mouse_event
    mouse_event = MouseButtonEvent(button, action, mods)


def get_mouse_event(button, action, mods = 0, pop_event = True):
    global mouse_event
    """
    :param button: 0 (left), 1 (right), or 2 (scrollwheel / middle) 
    :param action: 0 (click) or 1 (release)
    :param mods: various, see glfw docs.
    :return: True if requested event did indeed occur, False otherwise
    """
    if mouse_event:
        if mouse_event.check(button, action, mods):
            if pop_event:
                mouse_event = None
            return True
    else:
        return False

def get_mouse_button(button):
    """
    :param button: one of input.MOUSE_BUTTON_LEFT, _RIGHT, or _MIDDLE
    :return: True is pressed, False otherwise
    """
    return glfw.get_mouse_button(window, button)

class MouseButtonEvent:
    def __init__(self, button, action, mods):
        self.button = button
        self.action = action
        self.mods = mods

    def check(self, requested_button, requested_action, requested_mods):
        if self.button == requested_button:
            if self.action == requested_action:
                if self.mods == requested_mods:
                    return True


