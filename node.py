from itertools import count
import imgui
import config as cfg
import tkinter as tk
from tkinter import filedialog
tkroot = tk.Tk()
tkroot.withdraw()

class Node(object):
    idgen = count(0)
    ## typedef
    TYPE_NONE = 1
    TYPE_LOAD = 2
    TYPE_REGISTER = 4
    TYPE_SYSTEM_PARAMETERS = 8
    TYPE_SPATIAL_FILTER = 16
    TYPE_TEMPORAL_FILTER = 32
    TYPE_RECONSTRUCTION = 64

    def __init__(self):
        self.id = next(Node.idgen)
        self.label = ""
        self.type = Node.TYPE_NONE
        self.position = cfg.node_editor_context_menu_position
        self.size = (0, 0)
        # In/outputs
        self.input = list()
        self.output = list()
        self.n_inputs = 0
        self.n_outputs = 0
        cfg.node_list.append(self)
        cfg.node_editor_context_menu_visible = False

    def __eq__(self, other):
        if type(self) is type(other):
            return self.id == other.id
        return False

    def __str__(self):
        self_str =  f"Node: type = {self.type},\t id = {self.id},\t label = {self.label}.\n"
        for node in self.input:
            self_str += str(node)
        for node in self.output:
            self_str += str(node)
        self_str += "\n"
        return self_str

    def add_input(self, input_attribute):
        input_attribute.input = True
        input_attribute.parent_node_id = self.id
        self.input.append(input_attribute)

    def add_output(self, output_attribute):
        output_attribute.input = False
        output_attribute.parent_node_id = self.id
        self.output.append(output_attribute)

    def render_start(self):
        imgui.push_id(str(self.id))
        imgui.push_style_color(imgui.COLOR_BORDER, *cfg.node_type_colors[self.type])
        imgui.push_style_color(imgui.COLOR_TITLE_BACKGROUND, *cfg.node_type_colors[self.type])
        imgui.push_style_color(imgui.COLOR_TITLE_BACKGROUND_ACTIVE, *cfg.node_type_colors[self.type])
        imgui.push_style_color(imgui.COLOR_TITLE_BACKGROUND_COLLAPSED, *cfg.node_type_colors[self.type])
        imgui.set_next_window_size(*self.size, imgui.ONCE)
        imgui.set_next_window_position(*self.position, imgui.ONCE)
        _, stay_open = imgui.begin(self.label + "##" + str(self.id), flags = imgui.WINDOW_NO_RESIZE | imgui.WINDOW_NO_BRING_TO_FRONT_ON_FOCUS, closable = True)
        if not stay_open:
            cfg.node_list.remove(self)

    def render_end(self):
        for attribute in self.input:
            attribute.render()
        for attribute in self.output:
            attribute.render()
        imgui.end()
        imgui.pop_id()
        imgui.pop_style_color(4)


class Attribute(object):
    idgen = count(0)
    TYPE_NONE = 1
    TYPE_TEXT = 2
    TYPE_FILE = 4
    TYPE_FLOAT = 8
    TYPE_SYSTEM_PARAMETERS = 16

    def __init__(self, label = ""):
        self.id = next(Attribute.idgen)
        self.label = label
        self.type = Attribute.TYPE_NONE
        self.connectable = False
        self.linked_nodes = list()
        self.value = None
        self.draw_start = None
        self.draw_end = None
        self.input = True
        self.connectable = False
        self.parent_node_id = None

    def __eq__(self, other):
        if type(self) is type(other):
            return self.id == other.id
        return False

    def __str__(self):
        return f"{'Input' if self.input else 'Output'} attribute: type = {self.type},\t id = {self.id},\t label = {self.label}.\n"

    def render_start(self):
        imgui.push_id(f"Attribute{self.id}")
        self.draw_start = imgui.get_cursor_screen_pos()
        imgui.begin_group()

    def render_end(self):
        self.draw_end = imgui.get_cursor_screen_pos()
        imgui.end_group()
        ## render connector
        if self.connectable:
            window_width = imgui.get_window_width()
            window_position = imgui.get_window_position()
            connector_position = (self.draw_start[0] + (cfg.connector_horizontal_offset if self.input else window_width + cfg.connector_horizontal_offset), (self.draw_start[1] + self.draw_end[1]) / 2 + cfg.connector_vertical_offset)
            # Make an invisible window behind the connector blob
            imgui.set_next_window_size(cfg.connector_radius * 2 + 1, cfg.connector_radius * 2 + 1)
            imgui.set_next_window_position(connector_position[0] - 1 * cfg.connector_radius, connector_position[1] - 1 * cfg.connector_radius)
            imgui.push_style_color(imgui.COLOR_WINDOW_BACKGROUND, 0.0, 0.0, 0.0, 0.0)
            imgui.push_style_color(imgui.COLOR_BORDER, 0.0, 0.0, 0.0, 0.0)
            imgui.push_style_color(imgui.COLOR_BORDER_SHADOW, 0.0, 0.0, 0.0, 0.0)
            imgui.begin(f"Attribute{self.id}", flags = imgui.WINDOW_NO_TITLE_BAR | imgui.WINDOW_NO_MOVE | imgui.WINDOW_NO_RESIZE | imgui.WINDOW_NO_COLLAPSE | imgui.WINDOW_NO_SAVED_SETTINGS | imgui.WINDOW_NO_SCROLLBAR)

            if imgui.begin_drag_drop_source():
                cfg.active_connector = self.id
                imgui.set_drag_drop_payload('connector', str(self.id).encode())
                imgui.text(f"Connector from attribute {self.id}")
                imgui.end_drag_drop_source()
            if not self.id == cfg.active_connector:
                if imgui.begin_drag_drop_target():
                    payload = imgui.accept_drag_drop_payload('connector')
                    if payload is not None:
                        print("Received node: ", payload)
                    imgui.end_drag_drop_target()
            imgui.end()
            imgui.pop_style_color(3)
            # Render the connector blob
            draw_list = imgui.get_overlay_draw_list()
            draw_list.add_circle_filled(connector_position[0], connector_position[1], cfg.connector_radius, imgui.get_color_u32_rgba(*self.colour), cfg.connector_segments)

            # If connected, render the connection
        imgui.pop_id()

    def render(self):
        self.render_start()
        self.render_end()

    def connect_input(self):
        pass

    def connect_output(self):
        pass



class InputTextAttribute(Attribute):
    def __init__(self, label = ""):
        super(type(self), self).__init__(label)
        self.type = Attribute.TYPE_TEXT
        self.colour = cfg.attribute_type_colors[self.type]
        self.value = ""
        self.width = 200
        self.connectable = True

    def render(self):
        super(InputTextAttribute, self).render_start()
        self.render_attribute_body()
        super(InputTextAttribute, self).render_end()

    def render_attribute_body(self):
        if self.label:
            imgui.text(self.label)
        imgui.push_item_width(self.width)
        _, self.value = imgui.input_text("##", self.value, 256)
        imgui.pop_item_width()


class FileAttribute(Attribute):
    def __init__(self, label = ""):
        super(type(self), self).__init__(label)
        self.type = Attribute.TYPE_FILE
        self.colour = cfg.attribute_type_colors[self.type]
        self.value = ""
        self.connectable = True

    def render(self):
        super(FileAttribute, self).render_start()
        self.render_attribute_body()
        super(FileAttribute, self).render_end()

    def render_attribute_body(self):
        imgui.push_item_width(160)
        if not self.label == "":
            imgui.text(self.label)
        _, self.value = imgui.input_text("##", self.value, 256)
        imgui.pop_item_width()
        imgui.same_line()
        button_browse = imgui.button("...", width = 30, height = 20)
        if button_browse:
            self.value = filedialog.askopenfilename()


class FloatAttribute(Attribute):
    def __init__(self, label = ""):
        super(type(self), self).__init__(label)
        self.type = Attribute.TYPE_FLOAT
        self.colour = cfg.attribute_type_colors[self.type]
        self.value = 0.0
        self.connectable = True

    def render(self):
        super(type(self), self).render_start()
        self.render_attribute_body()
        super(type(self), self).render_end()

    def render_attribute_body(self):
        imgui.push_item_width(50)
        _, self.value = imgui.input_float(self.label, self.value, 0, 0, format = "%.0f")
        imgui.pop_item_width()


class SystemParametersAttribute(Attribute):
    def __init__(self, label = ""):
        super(type(self), self).__init__(label)
        self.type = Attribute.TYPE_SYSTEM_PARAMETERS
        self.colour = cfg.attribute_type_colors[self.type]
        self.connectable = True
        self.pixel_size_nm = 65
        self.dark_adu = 100
        self.adu_per_photon = 0.45

    def render(self):
        super(type(self), self).render_start()
        self.render_attribute_body()
        super(type(self), self).render_end()

    def render_attribute_body(self):
        imgui.push_item_width(50)
        _, self.pixel_size_nm = imgui.input_int("Pixel size (nm)", self.pixel_size_nm, 0)
        _, self.camera_offset = imgui.input_int("Dark counts", self.dark_adu, 0)
        _, self.camera_adu_per_photon = imgui.input_float("ADU per photon", self.adu_per_photon, 0, format = "%.2f")
        imgui.pop_item_width()