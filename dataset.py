from PIL import Image
from util import *
import re
from itertools import count

class Frame:
    idgen = count(1)

    def __init__(self, path, index = None):
        self.id = next(Frame.idgen)
        self.path = path
        self.index = index
        self.data = None
        self.transform = None
        self.width = 1
        self.height = 1

    def load(self):
        if not self.data is None:
            return self.data
        image = Image.open(self.path)
        if self.index:
            image.seek(self.index)
        self.data = np.asarray(image)
        self.width, self.height = self.data.shape
        return self.data

class Dataset:
    def __init__(self, path):
        self.path = path
        self.frames = list()
        self.n_frames = 0
        self.load()
        self.frames[0].load()
        self.width = self.frames[0].width
        self.height = self.frames[0].height
        self.roi = (0, 0, self.width, self.height) # left, bottom, right, top
        print(self.roi)

    def load(self):
        data = Image.open(self.path)
        file_frame_count = data.n_frames
        if file_frame_count == 1:
            directory = Path(self.path).root
            def numericalSort(value):
                numbers = re.compile(r'(\d+)')
                parts = numbers.split(value)
                parts[1::2] = map(int, parts[1::2])
                return parts
            files = sorted(glob.glob(directory+"*.tif*"), key = numericalSort)
            for file in files:
                self.n_frames += 1
                self.frames.append(Frame(file))
        else:
            for f in range(file_frame_count):
                self.n_frames += 1
                self.frames.append(Frame(self.path, index = f))

    def set_roi(self, roi):
        self.roi = roi
        cfg.fbo_needs_update = True
