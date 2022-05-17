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
    TYPE_SPATIAL_FILTER = 8
    TYPE_TEMPORAL_FILTER = 16

    def __init__(self, position):
        self.id = next(Node.idgen)
        self.label = ""
        self.type = Node.TYPE_NONE
        self.position = position
        self.size = (0, 0)
        # In/outputs
        self.input = list()
        self.output = list()
        self.n_inputs = 0
        self.n_outputs = 0
        cfg.node_list.append(self)
        cfg.node_editor_context_menu_visible = False

        ## Cosmetic:
        self.header_color = (0.5, 0.5, 0.5)

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
        input_attribute.colour = cfg.node_type_colors[self.type]
        self.input.append(input_attribute)

    def add_output(self, output_attribute):
        output_attribute.input = False
        output_attribute.colour = cfg.node_type_colors[self.type]
        self.output.append(output_attribute)

    def render_start(self):
        imgui.push_id(str(self.id))
        imgui.push_style_color(imgui.COLOR_HEADER, *self.header_color)
        imgui.set_next_window_size(*self.size, imgui.ONCE)
        imgui.set_next_window_position(*self.position, imgui.ONCE)
        imgui.begin(self.label + "##" + str(self.id))

    def render_body(self):
        for attribute in self.input:
            attribute.render()
        for attribute in self.output:
            attribute.render()

    def render_end(self):
        imgui.end()
        imgui.pop_id()
        imgui.pop_style_color(1)


    def deco(self, render_function):
        def render_wrap(self):
            self.render_start()
            render_function()
            self.render_body()
            self.render_end()
        return render_wrap

class Attribute(object):
    idgen = count(0)
    TYPE_NONE = 1
    TYPE_TEXT = 2
    TYPE_FILE = 4
    TYPE_FLOAT = 8

    def __init__(self, label = ""):
        self.id = next(Attribute.idgen)
        self.label = label
        self.type = Attribute.TYPE_NONE
        self.connectable = False
        self.linked_nodes = list()
        self.colour = (0.0, 0.0, 0.0, 1.0)
        self.value = None
        self.draw_start = None
        self.draw_end = None
        self.input = True
        self.connectable = False

    def __eq__(self, other):
        if type(self) is type(other):
            return self.id == other.id
        return False

    def __str__(self):
        return f"{'Input' if self.input else 'Output'} attribute: type = {self.type},\t id = {self.id},\t label = {self.label}.\n"

    def render_start(self):
        imgui.push_id(f"Attribute{self.id}")
        self.draw_start = imgui.get_cursor_screen_pos()


    def render_end(self):
        self.draw_end = imgui.get_cursor_screen_pos()
        self.render_connector()
        imgui.pop_id()

    def render(self):
        self.render_start()
        self.render_end()

    def connect_input(self):
        pass

    def connect_output(self):
        pass

    def render_connector(self):
        if self.connectable:
            window_width = imgui.get_window_width()
            connector_position = (self.draw_start[0] + (cfg.connector_horizontal_offset if self.input else window_width + cfg.connector_horizontal_offset), (self.draw_start[1] + self.draw_end[1]) / 2 + cfg.connector_vertical_offset)
            draw_list = imgui.get_overlay_draw_list()
            draw_list.add_circle_filled(connector_position[0], connector_position[1], cfg.connector_radius, imgui.get_color_u32_rgba(*self.colour), cfg.connector_segments)



class InputTextAttribute(Attribute):
    def __init__(self, label = ""):
        super(type(self), self).__init__(label)
        self.type = Attribute.TYPE_TEXT
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
        self.value = ""
        self.connectable = True

    def render(self):
        super(FileAttribute, self).render_start()
        self.render_attribute_body()
        super(FileAttribute, self).render_end()

    def render_attribute_body(self):
        imgui.push_item_width(160)
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
