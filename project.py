"""This file defines the class Project(), which is the container for all the user-specified
project settings such as the node setup, ROIs, etc."""


class Project():
    def __init__(self):
        self.dataset = None
        self.rois = list()
        self.nodes = list()



