import imgui
import config as cfg
from dataset import *
from opengl_classes import *
from OpenGL.GL import *
from OpenGL.GLU import *

texture_shader = None
screen_shader = None
texture = None
vertex_array = None
fbo = None
dataset = Dataset("test_dataset/img_0001_Img.tif")


def start():
    global texture_shader, texture, vertex_array, screen_shader
    texture = Texture(format = "ru16")
    texture.update(dataset.frames[0].load())
    texture_shader = Shader("shaders/image_to_texture.glsl")
    vertices = [-1.0, 1.0, 1.0, -1.0, -1.0, 1.0, 1.0, -1.0, 1.0, 1.0, 1.0, 1.0]
    indices = [0, 1, 2, 2, 0, 3]
    vertex_buffer = VertexBuffer(vertices)
    index_buffer = IndexBuffer(indices)
    vertex_array = VertexArray(vertex_buffer, index_buffer)
    update_fbo()

def on_update():
    if cfg.fbo_needs_update:
        update_fbo()

    # render to fbo
    fbo.bind()
    vertex_array.bind()
    texture_shader.bind()
    texture.bind(0)
    texture_shader.uniform1f("image_width", float(dataset.width))
    texture_shader.uniform1f("image_height", float(dataset.height))
    glDrawElements(GL_TRIANGLES, vertex_array.indexBuffer.getCount(), GL_UNSIGNED_SHORT, None)
    texture_shader.unbind()
    vertex_array.unbind()
    fbo.unbind()
    glActiveTexture(GL_TEXTURE0)


def data_browser_window():
    imgui.begin("data browser window", False, imgui.WINDOW_NO_TITLE_BAR | imgui.WINDOW_NO_COLLAPSE | imgui.WINDOW_NO_RESIZE | imgui.WINDOW_NO_MOVE)
    window_width = imgui.get_window_width() - 16
    imgui.image(fbo.texture.renderer_id, window_width, window_width, uv0 = (-0.1, -0.1), uv1 = (1.1, 1.1))
    imgui.end()

def update_fbo():
    global fbo
    cfg.fbo_needs_update = False
    fbo = FrameBuffer(dataset.roi[3] - dataset.roi[1], dataset.roi[2] - dataset.roi[0])

