import glfw
window = None

cursor_pos = [0, 0]
cursor_delta = [0, 0]
scroll_delta = [0, 0]
mouse_event = None
key_event = None

RELEASE = 0
PRESS = 1
REPEAT = 2

MOUSE_BUTTON_LEFT = 0
MOUSE_BUTTON_RIGHT = 1
MOUSE_BUTTON_MIDDLE = 2

def start(glfwwindow):
    global window
    window = glfwwindow
    glfw.set_key_callback(window, key_callback)
    glfw.set_mouse_button_callback(window, mouse_button_callback)
    glfw.set_scroll_callback(window, scroll_callback)

def on_update():
    global cursor_pos, mouse_event, cursor_delta, scroll_delta
    scroll_delta = [0.0, 0.0]
    mouse_event = None
    new_cursor_pos = glfw.get_cursor_pos(window)
    cursor_delta = [new_cursor_pos[0] - cursor_pos[0], new_cursor_pos[1] - cursor_pos[1]]
    cursor_pos = new_cursor_pos
    glfw.poll_events()

def scroll_callback(window, xoffset, yoffset):
    global scroll_delta
    scroll_delta = [xoffset, yoffset]

def mouse_button_callback(window, button, action, mods):
    global mouse_event
    mouse_event = MouseButtonEvent(button, action, mods)


def key_callback(window, button, scancode, action, mods):
    global key_event
    key_event = KeyEvent(button, action, mods)


def get_key_event(key, action, mods = 0, pop_event = True):
    global key_event
    if key_event:
        if key_event.check(key, action, mods):
            if pop_event:
                key_event = None
            return True
    return False


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
    return False


def get_mouse_button(button):
    """
    :param button: one of input.MOUSE_BUTTON_LEFT, _RIGHT, or _MIDDLE
    :return: True is pressed, False otherwise
    """
    return glfw.get_mouse_button(window, button)


class KeyEvent:
    def __init__(self, key, action, mods):
        self.key = key
        self.action = action
        self.mods = mods

    def check(self, requested_key, requested_action, requested_mods):
        if self.key == requested_key:
            if self.action == requested_action:
                if self.mods == requested_mods:
                    return True
        return False


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
        return False

