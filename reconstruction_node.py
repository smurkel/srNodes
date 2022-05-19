from node import *

class ReconstructionNode(Node):

    def __init__(self):
        super(type(self), self).__init__()
        self.type = Node.TYPE_RECONSTRUCTION
        self.label = "Reconstruction (output)"
        output_file = FileAttribute()
        output_file.connectable = True
        output_file.label = "Output path"
        output_file.input = True
        self.add_input(output_file)
        self.size = [216, 150]

    def render_node_body(self):
        pass

    def render(self):
        super(type(self), self).gui_start()
        self.render_node_body()
        super(type(self), self).gui_end()