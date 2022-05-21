import imgui
import config as cfg
from dataset import *
from opengl_classes import *
from OpenGL.GL import *
from OpenGL.GLU import *
import input

shader = Shader()
roi_shader = Shader()
texture = Texture()
vertex_array = VertexArray()
fbo = FrameBuffer()
projection_matrix = np.matrix([
    [2 / 2048,  0,          0,          0],
    [0,         2 / 2048,   0,          0],
    [0,         0,          -2 / 100,   0],
    [0,         0,          0,          1],
])
camera_position = [0.0, 0.0, 0.0]
camera_zoom = 1.0

imagedata = np.ones((2048, 2028))
img_shape = [512, 512]

view_projection_matrix = None

def start():
    global texture, shader, fbo, roi_shader
    texture = Texture(format="ru16")
    set_image(imagedata)
    shader = Shader("shaders/textured_shader.glsl")
    #roi_shader = Shader("shaders/roi_shader.glsl")
    fbo = FrameBuffer(2048, 2048)

def on_update():
    pass


def image_viewer_window():
    global camera_position, camera_zoom
    imgui.begin("image viewer", False, imgui.WINDOW_NO_TITLE_BAR | imgui.WINDOW_NO_COLLAPSE | imgui.WINDOW_NO_RESIZE | imgui.WINDOW_NO_MOVE)
    image_window_size = imgui.get_window_width() - 16
    render()
    imgui.image(fbo.texture.renderer_id, image_window_size, image_window_size)

    clamp_camera_params = False
    if imgui.is_window_hovered():
        if input.get_mouse_button(input.MOUSE_BUTTON_MIDDLE):
            camera_position[0] += input.cursor_delta[0] * cfg.image_viewer_pan_speed
            camera_position[1] += input.cursor_delta[1] * cfg.image_viewer_pan_speed
            clamp_camera_params = True

        if input.scroll_delta[1] != 0:
            clamp_camera_params = True
            camera_zoom *= (1.0 + input.scroll_delta[1] * cfg.image_viewer_zoom_step)

    if clamp_camera_params:
        camera_position[0] = min([camera_position[0], camera_zoom * img_shape[0]])
        camera_position[1] = min([camera_position[1], camera_zoom * img_shape[1]])
        camera_position[0] = max([camera_position[0], -camera_zoom * img_shape[0]])
        camera_position[1] = max([camera_position[1], -camera_zoom * img_shape[1]])
    imgui.end()


def set_image(image):
    global vertex_array, camera_position, img_shape
    # Make a quad of the right size
    width, height = np.shape(image)
    img_shape = [width, height]
    w = width
    h = height
    camera_position = [-w / 2, -h / 2, 0.0]
    vertex_attributes = [0.0, h, 1.0, 0.0, 1.0,
                         0.0, 0.0, 1.0, 0.0, 0.0,
                         w, 0.0, 1.0, 1.0, 0.0,
                         w, h, 1.0, 1.0, 1.0]
    indices = [0, 1, 2, 2, 0, 3]
    vertex_buffer = VertexBuffer(vertex_attributes)
    index_buffer = IndexBuffer(indices)
    vertex_array = VertexArray(vertex_buffer, index_buffer)

    # Upload the image to the texture
    #texture.update(image)

def render():
    global view_projection_matrix
    # render to fbo
    fbo.clear((0.0, 0.0, 0.0))
    fbo.bind()

    vertex_array.bind()
    shader.bind()
    texture.bind(0)

    ## upload camera uniform variables
    view_matrix = np.matrix([
        [camera_zoom, 0.0, 0.0, camera_position[0]],
        [0.0, camera_zoom, 0.0, camera_position[1]],
        [0.0, 0.0, camera_zoom, camera_position[2]],
        [0.0, 0.0, 0.0, 1.0],
    ])
    view_projection_matrix = np.matmul(projection_matrix, view_matrix)
    shader.uniformmat4("cameraMatrix", view_projection_matrix)
    glDrawElements(GL_TRIANGLES, vertex_array.indexBuffer.getCount(), GL_UNSIGNED_SHORT, None)
    shader.unbind()
    vertex_array.unbind()
    fbo.unbind(viewport = (0, 0, cfg.window_width, cfg.window_height))
    glActiveTexture(GL_TEXTURE0)

def render_roi(roi, colour):
    vertex_array.bind()

    ## roi model matrix
    roi_width = roi[2] - roi[0]
    roi_height = roi[3] - roi[1]

    roi_model_matrix = np.matrix([
        [roi_width / 2048, 0.0, 0.0, roi[0] / 2048],
        [0.0, roi_height / 2048, 0.0, roi[1] / 2048],
        [0.0, 0.0, 1.0, 0.0],
        [0.0, 0.0, 0.0, 1.0],
    ])

## Imageviewer behaviour:
# In a window, render an imgui image which display the current data (image).
# Dragging should move the image but not the window.
# Scrolling should zoom in/out on the window.
# The way to do this:
# Make a quad with width/height equal to that of the image to be shown.
# Render this quad with an orthogonal camera matrix
# Make the camera move and zoom for mouse input.
