from node import *

class RegisterNode(Node):
    def __init__(self):
        super(type(self), self).__init__()
        self.type = Node.TYPE_REGISTER
        self.label = "Register frames"
        self.add_input(InputTextAttribute("placeholder"))
        self.add_output(InputTextAttribute("placeholder"))
        self.size = [216, 150]
        self.mode = 0

    def render_node_body(self):
        pass

    def render(self):
        super(type(self), self).gui_start()
        self.render_node_body()
        super(type(self), self).gui_end()