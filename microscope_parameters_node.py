from node import *

class MicroscopeParametersNode(Node):

    def __init__(self):
        super(type(self), self).__init__()
        self.type = Node.TYPE_SYSTEM_PARAMETERS
        self.label = "System parameters"
        self.add_input(InputTextAttribute("placeholder"))
        self.add_output(InputTextAttribute("placeholder"))
        self.size = [216, 150]

    def render_node_body(self):
        pass

    def render(self):
        super(type(self), self).render_start()
        self.render_node_body()
        super(type(self), self).render_body()
        super(type(self), self).render_end()