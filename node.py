from itertools import count
import imgui
import config as cfg
import tkinter as tk
from tkinter import filedialog
import config as cfg
import input

tkroot = tk.Tk()
tkroot.withdraw()

connector_draw_list = list()

def render_connectors():
    global connector_draw_list
    draw_list = imgui.get_overlay_draw_list()
    for connector in connector_draw_list:
        draw_list.add_circle_filled(connector[0], connector[1], cfg.connector_radius,
                            imgui.get_color_u32_rgba(*connector[2]), cfg.connector_segments)
    connector_draw_list = list()

class Node(object):
    idgen = count(1)
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
        self.input_attributes = list()
        self.output_attributes = list()
        self.n_inputs = 0
        self.n_outputs = 0
        cfg.current_project.nodes.append(self)
        cfg.node_editor_context_menu_visible = False

    def __eq__(self, other):
        if type(self) is type(other):
            return self.id == other.id
        return False

    def __str__(self):
        self_str =  f"Node: type = {self.type},\t id = {self.id},\t label = {self.label}.\n"
        for node in self.input_attributes:
            self_str += str(node)
        for node in self.output_attributes:
            self_str += str(node)
        self_str += "\n"
        return self_str

    def add_input(self, input_attribute):
        input_attribute.input = True
        input_attribute.parent_node_id = self.id
        self.input_attributes.append(input_attribute)

    def add_output(self, output_attribute):
        output_attribute.input = False
        output_attribute.parent_node_id = self.id
        self.output_attributes.append(output_attribute)

    def gui_start(self):
        imgui.push_id(str(self.id))
        imgui.push_style_color(imgui.COLOR_BORDER, *cfg.node_type_colors[self.type])
        imgui.push_style_color(imgui.COLOR_TITLE_BACKGROUND, *cfg.node_type_colors[self.type])
        imgui.push_style_color(imgui.COLOR_TITLE_BACKGROUND_ACTIVE, *cfg.node_type_colors[self.type])
        imgui.push_style_color(imgui.COLOR_TITLE_BACKGROUND_COLLAPSED, *cfg.node_type_colors[self.type])
        imgui.set_next_window_size(*self.size, imgui.ONCE)
        imgui.set_next_window_position(*self.position, imgui.ONCE)
        _, stay_open = imgui.begin(self.label + "##" + str(self.id), flags = imgui.WINDOW_NO_RESIZE | imgui.WINDOW_NO_BRING_TO_FRONT_ON_FOCUS | imgui.WINDOW_NO_SAVED_SETTINGS, closable = True)
        if not stay_open:
            self.delete()

    def gui_end(self):
        for attribute in self.input_attributes:
            attribute.render()
        for attribute in self.output_attributes:
            attribute.render()
        imgui.end()
        imgui.pop_id()
        imgui.pop_style_color(4)

    def delete(self):
        cfg.node_list.remove(self)
        for attribute in self.input_attributes:
            attribute.delete()
        for attribute in self.output_attributes:
            attribute.delete()

class Attribute(object):
    idgen = count(1)
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
        self.linked_attributes = list()
        self.value = None
        self.draw_start = None
        self.draw_end = None
        self.input = None
        self.parent_node_id = None
        self.connector_position = (0, 0)

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
        ## Render connector + drag&drop connections
        if self.connectable:
            window_width = imgui.get_window_width()
            window_position = imgui.get_window_position()
            self.connector_position = (self.draw_start[0] + (cfg.connector_horizontal_offset if self.input else window_width + cfg.connector_horizontal_offset), (self.draw_start[1] + self.draw_end[1]) / 2 + cfg.connector_vertical_offset)
            # Make an invisible window behind the connector blob
            connector_window_size = (cfg.connector_radius + cfg.connector_window_padding) * 2 + 1
            imgui.set_next_window_size(connector_window_size, connector_window_size)
            imgui.set_next_window_position(self.connector_position[0] - 1 * cfg.connector_radius - cfg.connector_window_padding - 1, self.connector_position[1] - 1 * cfg.connector_radius - cfg.connector_window_padding - 1)
            imgui.push_style_color(imgui.COLOR_WINDOW_BACKGROUND, 0.0, 0.0, 0.0, 0.0)
            imgui.push_style_color(imgui.COLOR_BORDER, 0.0, 0.0, 0.0, 0.0)
            imgui.push_style_color(imgui.COLOR_BORDER_SHADOW, 0.0, 0.0, 0.0, 0.0)
            imgui.push_style_color(imgui.COLOR_DRAG_DROP_TARGET, 0.0, 1.0, 0.0, 1.0)
            imgui.begin(f"Attribute{self.id}", False, imgui.WINDOW_NO_TITLE_BAR | imgui.WINDOW_NO_MOVE | imgui.WINDOW_NO_RESIZE | imgui.WINDOW_NO_COLLAPSE | imgui.WINDOW_NO_SAVED_SETTINGS | imgui.WINDOW_NO_SCROLLBAR | imgui.WINDOW_NO_SAVED_SETTINGS)
            ## Middle-mouse click deletes all connections
            if input.get_mouse_event(input.MOUSE_BUTTON_MIDDLE, input.PRESS, pop_event = False) and imgui.is_window_hovered():
                print(self.parent_node_id)
                self.disconnect_all()

            ## Allow drag source if no current node being edited
            if self == cfg.active_connector or cfg.active_connector is None:
                if imgui.begin_drag_drop_source():
                    cfg.active_connector = self
                    imgui.set_drag_drop_payload('connector', b'1') # Arbitrary payload value - we manually keep track of the payload elsewhere
                    imgui.text(f"Connector from attribute {self.id}")
                    imgui.end_drag_drop_source()
            # Else, if there is an active node, allow drop target.
            elif not cfg.active_connector is None:
                imgui.begin_child(f"Attribute{self.id}drop_target")
                imgui.end_child()
                if imgui.begin_drag_drop_target():
                    payload = imgui.accept_drag_drop_payload('connector')
                    if payload is not None:
                        self.connect_attribute()
                    imgui.end_drag_drop_target()

            imgui.end()
            imgui.pop_style_color(4)
            # Render the connector blob
            connector_draw_list.append((self.connector_position[0], self.connector_position[1], self.colour))


            # render connections - output to input only!
            draw_list = imgui.get_overlay_draw_list()
            if not self.input:
                for partner in self.linked_attributes:
                    partner_position = partner.connector_position
                    draw_list.add_line(*self.connector_position, *partner_position, imgui.get_color_u32_rgba(*cfg.connection_line_color), cfg.connection_line_thickness)
        imgui.pop_id()

    def render(self):
        self.render_start()
        self.render_end()

    def connect_attribute(self):
        print("trying to connect")
        io_match = not (self.input == cfg.active_connector.input)
        different_node = not (self.parent_node_id == cfg.active_connector.parent_node_id)
        not_linked_yet = not (cfg.active_connector in self.linked_attributes)
        if not io_match: print("Can't connect input/input or output/output")
        if not different_node: print("Can't connect attributes on same node")
        if not not_linked_yet: print("Attributes are already linked")
        if io_match and different_node and not_linked_yet:
            self.linked_attributes.append(cfg.active_connector)
            cfg.active_connector.linked_attributes.append(self)
            print("Drop node - connections:", self.linked_attributes)
            print("Drag node - connections:", cfg.active_connector.linked_attributes)
            print("Linked!")

    def disconnect_all(self):
        for partner in self.linked_attributes:
            partner.linked_attributes.remove(self)
        self.linked_attributes = list()

    def delete(self):
        for partner in self.linked_attributes:
            partner.linked_attributes.remove(self)
        self.linked_attributes = list()

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