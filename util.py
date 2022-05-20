from PIL import Image
import numpy as np
import time
from datetime import datetime
import glob
import config as cfg

_util_time_var = None

def info(message):
    if cfg.log_level <= 2:
        print('\033[94m' + message)

def warning(message):
    if cfg.log_level <= 1:
        print('\033[93m'+message)

def error(message):
    if cfg.log_level <= 0:
        print('\033[91m'+message)


def tic():
    global _util_time_var
    _util_time_var = time.time()


def toc():
    global _util_time_var
    time_elapsed = (time.time() - _util_time_var) * 1000
    return time_elapsed


def timestamp():
    now = datetime.now()
    timestamp = now.strftime("%H%M%S")
    return timestamp


def datestamp():
    now = datetime.now()
    datestamp = now.strftime("%Y%m%d")
    return datestamp


class Path:
    def __init__(self, path):
        path = path.replace("\\", "/")
        self.path = path
        mark = self.path.rfind("/")
        self.root = self.path[:mark + 1]
        mark = self.path.rfind("/")
        mark2 = self.path.rfind(".")
        self.title = self.path[mark + 1:mark2]
        self.name = self.title
        mark = self.path.rfind(".")
        self.type = self.path[mark:]

    def __str__(self):
        return self.path
#
#
# def Load(path):
#     if isinstance(path, Path):
#         path = path.path
#     """Default expected expected is .tiff. So Load() defaults to LoadTiff() or LoadFolder()"""
#     if (path[-4:] == ".tif") or (path[-5:] == ".tiff"):
#         return LoadTiff(path)
#     elif path[-1:] == "/":
#         return LoadFolder(path)
#     else:
#         CS_ERROR("Invalid file path")
#
#
# def LoadTiff(path):
#     if isinstance(path, Path):
#         path = path.path
#     CS_INFO("Loading: "+path)
#     _data = Image.open(path)
#     _frame = np.asarray(_data)
#
#     width = _frame.shape[0]
#     height = _frame.shape[1]
#     depth = _data.n_frames
#     data = np.zeros((width, height, depth), dtype=np.float32)
#     for f in range(0, depth):
#         _data.seek(f)
#         data[:, :, f] = np.asarray(_data)
#
#     data = np.squeeze(data)
#     return data
#
# def LoadFolder(path):
#     paths = glob.glob(path+"*.tiff") + glob.glob(path+"*.tif")
#     _data = Image.open(paths[0])
#     _frame = np.asarray(_data)
#
#     width = _frame.shape[0]
#     height = _frame.shape[1]
#     depth = len(paths)
#     data = np.zeros((width, height, depth), dtype=np.float32)
#     for f in range(0, len(paths)):
#         CS_INFO("Loading "+paths[f])
#         _data = Image.open(paths[f])
#         data[:, :, f] = np.asarray(_data)
#     return data