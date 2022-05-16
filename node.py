from itertools import count
import imgui
import config as cfg

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
        self.input = list()
        self.output = list()
        self.position = position
        self.size = (0, 0)
        cfg.node_list.append(self)
        cfg.node_editor_context_menu_visible = False

        ## Cosmetic:
        self.header_color = (0.5, 0.5, 0.5)

    def __eq__(self, other):
        if type(self) is type(other):
            return self.id == other.id
        return False


    def __str__(self):
        return f"Node; id = {self.id}, type = {self.type}"


    def render_start(self):
        imgui.push_id(str(self.id))
        imgui.push_style_color(imgui.COLOR_HEADER, *self.header_color)
        imgui.set_next_window_size(*self.size, imgui.ONCE)
        imgui.set_next_window_position(*self.position, imgui.ONCE)
        imgui.begin(self.label + "##" + str(self.id))

    def render_body(self):
        for attribute in self.input:
            print(str(attribute))
            attribute.render()
        for attribute in self.output:
            print(str(attribute))
            attribute.render()

    def render_end(self):
        imgui.end()
        imgui.pop_id()
        imgui.pop_style_color(1)


def deco(render_function):
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

    def __init__(self):
        self.id = next(Attribute.idgen)
        self.label = ""
        self.type = Attribute.TYPE_NONE
        self.connectable = False
        self.linked_nodes = list()
        self.colour = (0.0, 0.0, 0.0)
        self.value = None

    def __eq__(self, other):
        if type(self) is type(other):
            return self.id == other.id
        return False

    def __str__(self):
        return f"Attribute; type = {self.type}; id = {self.id}"

    def render(self):
        pass

class TextAttribute(Attribute):
    def __init__(self):
        super(TextAttribute, self).__init__()
        self.type = Attribute.TYPE_TEXT
        self.value = " "
        self.width = 200

    def render(self):
        imgui.push_id(f"Attribute{self.id}")
        imgui.push_item_width(self.width)
        _, self.value = imgui.input_text("##", self.value, 256)
        imgui.pop_item_width()
        imgui.pop_id()
