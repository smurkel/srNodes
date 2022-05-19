from node import *

class LoadDataNode(Node):

    def __init__(self):
        super(LoadDataNode, self).__init__()
        self.type = Node.TYPE_LOAD
        self.label = "Load data"
        self.add_output(FileAttribute())
        self.size = [216, 76]


    def render_node_body(self):
        imgui.text("Select source file")

    def render(self):
        super(LoadDataNode, self).gui_start()
        self.render_node_body()
        super(LoadDataNode, self).gui_end()
