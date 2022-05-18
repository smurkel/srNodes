import imgui
from imgui.integrations.glfw import GlfwRenderer
import config as cfg
import input
from load_data_node import *
from register_node import *
from microscope_parameters_node import *
from reconstruction_node import *

impl = None

def start(window):
    global impl
    imgui.create_context()
    impl = GlfwRenderer(window)

def on_update():
    impl.process_inputs()
    imgui.new_frame()

    imgui.push_style_var(imgui.STYLE_WINDOW_ROUNDING, 0.0)
    gui()
    imgui.pop_style_var(1)
    imgui.render()
    impl.render(imgui.get_draw_data())

def exit():
    impl.shutdown()

def gui():
    node_editor_window()
    debug_window()

def node_editor_window():
    imgui.begin("Node editor", flags = imgui.WINDOW_NO_TITLE_BAR | imgui.WINDOW_NO_RESIZE | imgui.WINDOW_NO_MOVE | imgui.WINDOW_NO_BRING_TO_FRONT_ON_FOCUS)

    ## Open context menu
    if input.get_mouse_event(button = input.MOUSE_BUTTON_RIGHT, action = input.MOUSE_BUTTON_RELEASE):
        cfg.node_editor_context_menu_visible = True
        cfg.node_editor_context_menu_position = input.cursor_pos

    ## Context menu
    if cfg.node_editor_context_menu_visible:
        imgui.set_next_window_position(cfg.node_editor_context_menu_position[0], cfg.node_editor_context_menu_position[1])
        imgui.set_next_window_size(cfg.node_editor_context_menu_size[0], cfg.node_editor_context_menu_size[1])
        if imgui.begin("##node_editor_context_menu", flags = imgui.WINDOW_NO_RESIZE | imgui.WINDOW_NO_MOVE | imgui.WINDOW_NO_COLLAPSE | imgui.WINDOW_NO_TITLE_BAR):
            imgui.text("Select node to add")
            imgui.separator()
            add_node_load, _ = imgui.menu_item("Load dataset")
            add_node_system_parameters, _ = imgui.menu_item("Microscope parameters")
            add_node_register, _ = imgui.menu_item("Register frames")
            add_node_reconstruction, _ = imgui.menu_item("Reconstruction (output)")
            if add_node_load:
                LoadDataNode()
            if add_node_register:
                RegisterNode()
            if add_node_system_parameters:
                MicroscopeParametersNode()
            if add_node_reconstruction:
                ReconstructionNode()
            if not imgui.is_window_hovered(imgui.HOVERED_ALLOW_WHEN_BLOCKED_BY_ACTIVE_ITEM):
                cfg.node_editor_context_menu_visible = True
            imgui.end()

    ## Node editor
    for node in cfg.node_list:
        node.render()
    imgui.end()

def debug_window():
    imgui.begin("Debug window", flags = imgui.WINDOW_NO_MOVE)
    imgui.button("drag")
    if imgui.begin_drag_drop_source():
        imgui.set_drag_drop_payload('connector', b'connector_0')
        imgui.end_drag_drop_source()
    imgui.button("drop")
    if imgui.begin_drag_drop_target():
        payload = imgui.accept_drag_drop_payload('connector')
        if payload is not None:
            print("Received", payload)
        imgui.end_drag_drop_target()


    imgui.end()

