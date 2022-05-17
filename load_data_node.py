from node import *

class LoadDataNode(Node):

    def __init__(self):
        super(LoadDataNode, self).__init__()
        self.type = Node.TYPE_LOAD
        self.label = "Load data"
        self.add_output(FileAttribute("File path selection"))
        self.size = [216, 150]


    def render_node_body(self):
        pass

    def render(self):
        super(LoadDataNode, self).render_start()
        self.render_node_body()
        super(LoadDataNode, self).render_body()
        super(LoadDataNode, self).render_end()
