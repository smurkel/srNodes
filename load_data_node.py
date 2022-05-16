from node import *

class LoadDataNode(Node):

    def __init__(self, position):
        super(LoadDataNode, self).__init__(position)
        self.type = Node.TYPE_LOAD
        self.label = "Load data"
        self.header_color = (0.5, 0.7, 0.2)
        self.input.append(TextAttribute())
        self.size = [219, 150]

    ## Probably best to use a decorator here!
    @deco
    def render():
        ## Node header
        imgui.text("Select data source")
        imgui.button("Browse")
