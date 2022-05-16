import imgui
from imgui.integrations.glfw import GlfwRenderer
import config as cfg
import input

impl = None

def start(window):
    global impl
    imgui.create_context()
    impl = GlfwRenderer(window)

def on_update():
    impl.process_inputs()
    imgui.new_frame()

    imgui.push_style_var(imgui.STYLE_WINDOW_ROUNDING, 0.0)
    imgui.push_style_color(imgui.COLOR_WINDOW_BACKGROUND, *cfg.color_background)
    imgui.push_style_color(imgui.COLOR_CHECK_MARK, *cfg.color_checkmark)
    imgui.push_style_color(imgui.COLOR_FRAME_BACKGROUND, *cfg.color_frame_background)
    imgui.push_style_color(imgui.COLOR_FRAME_BACKGROUND_ACTIVE,*cfg.color_frame_background)
    imgui.push_style_color(imgui.COLOR_FRAME_BACKGROUND_HOVERED, *cfg.color_frame_background)
    imgui.push_style_color(imgui.COLOR_TEXT, *cfg.color_text)
    imgui.push_style_color(imgui.COLOR_POPUP_BACKGROUND, *cfg.color_frame_background_light_shade)
    gui()
    imgui.pop_style_var(1)
    imgui.pop_style_color(7)
    imgui.render()
    impl.render(imgui.get_draw_data())

def exit():
    impl.shutdown()

def gui():
    node_editor_window()

def node_editor_window():
    imgui.begin("Node editor", flags = imgui.WINDOW_NO_TITLE_BAR | imgui.WINDOW_NO_RESIZE | imgui.WINDOW_NO_MOVE | imgui.WINDOW_NO_BRING_TO_FRONT_ON_FOCUS)
    if input.get_mouse_event(button = input.MOUSE_BUTTON_RIGHT, action = input.MOUSE_BUTTON_RELEASE):
        cfg.node_editor_context_menu_visible = True
        cfg.node_editor_context_menu_position = input.cursor_pos
    if cfg.node_editor_context_menu_visible:
        imgui.set_next_window_position(cfg.node_editor_context_menu_position[0], cfg.node_editor_context_menu_position[1])
        imgui.set_next_window_size(cfg.node_editor_context_menu_size[0], cfg.node_editor_context_menu_size[1])
        if imgui.begin("##node_editor_context_menu", flags = imgui.WINDOW_NO_RESIZE | imgui.WINDOW_NO_MOVE | imgui.WINDOW_NO_COLLAPSE | imgui.WINDOW_NO_TITLE_BAR):
            imgui.text("context menu")
            if not imgui.is_window_hovered(imgui.HOVERED_ALLOW_WHEN_BLOCKED_BY_ACTIVE_ITEM):
                cfg.node_editor_context_menu_visible = True
            imgui.end()
    imgui.end()



