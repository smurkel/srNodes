import imgui
import config as cfg
from dataset import *
from opengl_classes import *
from OpenGL.GL import *
from OpenGL.GLU import *
import input
from itertools import count

shader = Shader()
roi_shader = Shader()
texture = Texture()
vertex_array = VertexArray()
roi_vertex_array = VertexArray()

fbo = FrameBuffer()
projection_matrix = np.matrix([
    [2 / 2048,  0,          0,          0],
    [0,         2 / 2048,   0,          0],
    [0,         0,          -2 / 100,   0],
    [0,         0,          0,          1],
])
camera_position = [0.0, 0.0, 0.0]
camera_zoom = 1.0

imagedata = Dataset("test_dataset/test_img.tif").frames[0].load()
img_shape = None
hist_counts = None
hist_bins = None
view_projection_matrix = None

def start():
    global texture, shader, fbo, roi_shader, roi_vertex_array
    texture = Texture(format="ru16")
    init_image(imagedata)
    shader = Shader("shaders/textured_shader.glsl")
    roi_shader = Shader("shaders/roi_shader.glsl")
    fbo = FrameBuffer(2048, 2048)
    cfg.current_project.rois.append(ROI((0, 0, 200, 100), (1.0, 1.0, 0.0, 1.0), label = "test roi"))
    cfg.current_project.rois.append(ROI((50, 50, 150, 250), (0.5, 1.0, 0.2, 1.0), label="test roi deux"))
    cfg.current_project.rois.append(ROI((100, 100, 450, 950), (0.2, 0.4, 0.9, 1.0), label="test roi 3"))

def on_update():
    pass


def image_viewer_window():
    global camera_position, camera_zoom

    imgui.begin("##image_viewer_data", False,
                imgui.WINDOW_NO_TITLE_BAR | imgui.WINDOW_NO_COLLAPSE | imgui.WINDOW_NO_RESIZE | imgui.WINDOW_NO_MOVE)
    # ROIs:
    active_roi = False
    for roi in cfg.current_project.rois:
        imgui.push_id(str(roi.id) + "_roi")
        imgui.push_style_color(imgui.COLOR_CHECK_MARK, *roi.colour)
        _changed, roi.being_edited = imgui.checkbox("##roi", roi.being_edited)
        if _changed and roi.being_edited:
            for r in cfg.current_project.rois:
                r.being_edited = False
            roi.being_edited = True
        if roi.being_edited:
            active_roi = roi
        imgui.same_line()
        imgui.push_style_color(imgui.COLOR_TEXT, *roi.colour)
        imgui.push_style_color(imgui.COLOR_FRAME_BACKGROUND, 14 / 255, 14 / 255, 14 / 255)
        imgui.push_style_color(imgui.COLOR_FRAME_BACKGROUND_ACTIVE, 14 / 255, 14 / 255, 14 / 255)
        imgui.push_style_color(imgui.COLOR_FRAME_BACKGROUND_HOVERED, 14 / 255, 14 / 255, 14 / 255)
        _, roi.label = imgui.input_text("##roi_label", roi.label, 256)
        imgui.pop_style_color(5)
        imgui.pop_id()

    # Histogram:
    cfg.image_viewer_contrast_header_open, _ = imgui.collapsing_header("Contrast settings",
                                                                       flags=imgui.TREE_NODE_DEFAULT_OPEN)
    if cfg.image_viewer_contrast_header_open:
        imgui.push_style_color(imgui.COLOR_PLOT_HISTOGRAM, 1.0, 1.0, 1.0)
        imgui.push_style_color(imgui.COLOR_PLOT_HISTOGRAM_HOVERED, 1.0, 1.0, 1.0)
        imgui.push_style_color(imgui.COLOR_FRAME_BACKGROUND, 14 / 255, 14 / 255, 14 / 255)
        imgui.push_style_color(imgui.COLOR_CHECK_MARK, 0.3, 1.0, 0.1)
        imgui.push_style_color(imgui.COLOR_FRAME_BACKGROUND_HOVERED, 14 / 255, 14 / 255, 14 / 255)
        imgui.plot_histogram("##image_histogram", hist_counts,
                             graph_size=(cfg.image_viewer_histogram_width, cfg.image_viewer_histogram_height))
        imgui.same_line(position=364)
        _auto_changed, cfg.image_viewer_contrast_auto = imgui.checkbox("auto", cfg.image_viewer_contrast_auto)
        if _auto_changed and cfg.image_viewer_contrast_auto:
            cfg.image_viewer_contrast_max = np.amax(imagedata)
            cfg.iamge_viewer_contrast_min = np.amin(imagedata)
        imgui.pop_style_color(5)
        imgui.push_style_color(imgui.COLOR_FRAME_BACKGROUND, 0.4, 0.4, 0.4)
        imgui.push_style_color(imgui.COLOR_FRAME_BACKGROUND_ACTIVE, 0.5, 0.5, 0.5)
        imgui.push_style_color(imgui.COLOR_FRAME_BACKGROUND_HOVERED, 0.5, 0.5, 0.5)
        imgui.push_style_color(imgui.COLOR_SLIDER_GRAB, 1, 1, 1)
        imgui.push_style_color(imgui.COLOR_SLIDER_GRAB_ACTIVE, 1, 1, 1)
        imgui.push_item_width(cfg.image_viewer_histogram_width)
        _min_changed, cfg.image_viewer_contrast_min = imgui.slider_float("low", cfg.image_viewer_contrast_min, 0,
                                                                         cfg.image_viewer_histogram_max_value,
                                                                         format="low %.0f",
                                                                         power=1.0)
        _max_changed, cfg.image_viewer_contrast_max = imgui.slider_float("high", cfg.image_viewer_contrast_max, 0,
                                                                         cfg.image_viewer_histogram_max_value,
                                                                         format="high %.0f",
                                                                         power=1.0)
        if _min_changed or _max_changed:
            cfg.image_viewer_contrast_auto = False
        imgui.pop_style_color(5)
        imgui.pop_item_width()

    imgui.end()

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
            camera_zoom = min([cfg.image_viewer_zoom_max, camera_zoom])
            camera_zoom = max([cfg.image_viewer_zoom_min, camera_zoom])
            if camera_zoom != cfg.image_viewer_zoom_max:
                camera_position[0] *= (1.0 + input.scroll_delta[1] * cfg.image_viewer_zoom_step)
                camera_position[1] *= (1.0 + input.scroll_delta[1] * cfg.image_viewer_zoom_step)

    if clamp_camera_params:
        camera_position[0] = min([camera_position[0], camera_zoom * img_shape[0]])
        camera_position[1] = min([camera_position[1], camera_zoom * img_shape[1]])
        camera_position[0] = max([camera_position[0], -camera_zoom * img_shape[0]])
        camera_position[1] = max([camera_position[1], -camera_zoom * img_shape[1]])

    # # Editing the active roi, if there is one.
    if active_roi:
        update_roi = False
        if imgui.is_window_hovered():
            if input.get_mouse_event(input.MOUSE_BUTTON_LEFT, input.PRESS):
                cfg.image_viewer_roi_being_drawn = True
                roi_origin = screen_to_pixel_coordinate()
                active_roi.roi = [roi_origin[0], roi_origin[1], roi_origin[0] + 1, roi_origin[1] + 1]
                update_roi = True
            elif cfg.image_viewer_roi_being_drawn:
                if input.get_mouse_event(input.MOUSE_BUTTON_LEFT, input.RELEASE):
                    cfg.image_viewer_roi_being_drawn = False
                else:
                    roi_lims = screen_to_pixel_coordinate()
                    active_roi.roi = [active_roi.roi[0], active_roi.roi[1], roi_lims[0], roi_lims[1]]
                    update_roi = True

        if update_roi:
            active_roi.roi[0] = max([0.0, active_roi.roi[0]])
            active_roi.roi[1] = max([0.0, active_roi.roi[1]])
            active_roi.roi[2] = max([0.0, active_roi.roi[2]])
            active_roi.roi[3] = max([0.0, active_roi.roi[3]])
            active_roi.roi[0] = min([active_roi.roi[0], img_shape[0]])
            active_roi.roi[1] = min([active_roi.roi[1], img_shape[1]])
            active_roi.roi[2] = min([active_roi.roi[2], img_shape[0]])
            active_roi.roi[3] = min([active_roi.roi[3], img_shape[1]])
            active_roi.update_va()

    imgui.end()



def screen_to_pixel_coordinate():
    cursor_position = input.cursor_pos
    img_window_origin = imgui.get_cursor_screen_pos()
    cursor_window_position = np.asarray([cursor_position[0] - img_window_origin[0], cursor_position[1] - 7])
    image_window_size = imgui.get_window_width() - 16
    cursor_ndc_position = 2.0 * cursor_window_position / image_window_size - 1.0
    cursor_image_position = np.dot(np.linalg.inv(projection_matrix), np.matrix([[cursor_ndc_position[0]], [cursor_ndc_position[1]], [0.0], [0.0]]))
    # TODO: figure out how to do this transform.
    pixel_coordinate = [int(cursor_image_position[0] - camera_position[0]), int(cursor_image_position[1] - camera_position[1])]
    return pixel_coordinate

def update_image(image):
    global hist_counts, hist_bins, imagedata
    imagedata = image
    # Upload the image to the texture
    texture.update(image)

    if cfg.image_viewer_contrast_auto:
        cfg.image_viewer_contrast_max = np.amax(image)
        cfg.iamge_viewer_contrast_min = np.amin(image)
    ## Calculate histogram
    # Get high limit for the histogram range
    cfg.image_viewer_histogram_max_value = min(np.asarray(cfg.image_viewer_histogram_max_value_options)[
                                                   np.asarray(cfg.image_viewer_histogram_max_value_options) > np.amax(
                                                       image)])
    hist_counts, hist_bins = np.histogram(image, bins=cfg.image_viewer_histogram_bins)
    hist_counts = hist_counts.astype('float32')
    hist_counts = np.delete(hist_counts, 0)
    hist_bins = np.delete(hist_bins, 0)

def init_image(image):
    global vertex_array, camera_position, img_shape
    # Make a quad of the right size
    height, width = np.shape(image)
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

    update_image(image)

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
    shader.uniform1f("contrast_min", cfg.image_viewer_contrast_min)
    shader.uniform1f("contrast_max", cfg.image_viewer_contrast_max)
    glDrawElements(GL_TRIANGLES, vertex_array.indexBuffer.getCount(), GL_UNSIGNED_SHORT, None)
    shader.unbind()
    vertex_array.unbind()
    glActiveTexture(GL_TEXTURE0)
    ## Render ROIs

    for roi in cfg.current_project.rois:
        if not roi.has_va:
            roi.update_va()
        roi.va.bind()
        roi_shader.bind()
        roi_shader.uniformmat4("cameraMatrix", view_projection_matrix)
        roi_shader.uniform3f("roiColour", roi.colour)
        roi_shader.uniform1f("lineWidth", roi.linewidth / camera_zoom)
        roi_shader.uniform1f("roiWidth", roi.width)
        roi_shader.uniform1f("roiHeight", roi.height)
        glDrawElements(GL_TRIANGLES, vertex_array.indexBuffer.getCount(), GL_UNSIGNED_SHORT, None)
        roi_shader.unbind()
        roi.va.unbind()


    fbo.unbind(viewport = (0, 0, cfg.window_width, cfg.window_height))

class ROI():
    idgen = count(0)
    def __init__(self, roi, colour, label = ""):
        self.id = next(ROI.idgen)
        self.roi = roi
        self.colour = colour
        self.label = label
        self.linewidth = 20
        self.has_va = False
        self.va = VertexArray()
        self.being_edited = True
        self.width = 1
        self.height = 1

    def update_va(self):
        self.has_va = True
        self.width = self.roi[2] - self.roi[0]
        self.height = self.roi[3] - self.roi[1]
        x = self.roi[0]
        y = self.roi[1]

        vertex_attributes = [x, y + self.height, 1.0, 0.0, 1.0,
                             x, y, 1.0, 0.0, 0.0,
                             x + self.width, y, 1.0, 1.0, 0.0,
                             x + self.width, y + self.height, 1.0, 1.0, 1.0]
        indices = [0, 1, 2, 2, 0, 3]
        self.va.update(VertexBuffer(vertex_attributes), IndexBuffer(indices))


## Imageviewer behaviour:
# In a window, render an imgui image which display the current data (image).
# Dragging should move the image but not the window.
# Scrolling should zoom in/out on the window.
# The way to do this:
# Make a quad with width/height equal to that of the image to be shown.
# Render this quad with an orthogonal camera matrix
# Make the camera move and zoom for mouse input.
