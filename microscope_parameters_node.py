from node import *

class MicroscopeParametersNode(Node):

    def __init__(self):
        super(type(self), self).__init__()
        self.type = Node.TYPE_SYSTEM_PARAMETERS
        self.label = "System parameters"
        self.add_output(SystemParametersAttribute())
        self.size = [216, 100]

    def render_node_body(self):
        pass

    def render(self):
        super(type(self), self).gui_start()
        self.render_node_body()
        super(type(self), self).gui_end()