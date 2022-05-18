window_width = 1000
window_height = 600
window_title = "SRNodes editor"

clear_color = (0.0, 0.0, 0.0, 1.0)
color_background = (20/255, 20/255, 20/255)
color_frame_background = (227/255, 231/255, 203/255)
color_frame_background_light_shade = (247/255, 241/255, 213/255)
color_checkmark = (0.2, 0.2, 0.22)
color_text = (0.9, 0.9, 0.85)


node_editor_context_menu_visible = False
node_editor_context_menu_position = [0, 0]
node_editor_context_menu_size = [200, 300]
node_list = list()

node_type_colors = dict()
node_type_colors[1] = (0.0, 0.0, 0.0, 1.0)
## Palette https://coolors.co/5349ad-99a15c-65db71-25abba-ba4234
node_type_colors[2] = (83/255, 73/255, 173/255, 1.0)
node_type_colors[4] = (153/255, 161/255, 92/255, 1.0)
node_type_colors[8] = (101/255, 219/255, 113/255, 1.0)
node_type_colors[16] = (37/255, 171/255, 186/255, 1.0)
node_type_colors[32] = (186/255, 66/255, 52/255, 1.0)
node_type_colors[64] = (161/255, 83/255, 113/255, 1.0)

attribute_type_colors = dict()
attribute_type_colors[1] = (0.0, 0.0, 0.0, 1.0)
## Palette https://coolors.co/f79256-f2e86d-bfd7ea-2c666e-9b5094
attribute_type_colors[2] = (247/255, 146/255, 86/255, 1.0)
attribute_type_colors[4] = (242/255, 232/255, 109/255, 1.0)
attribute_type_colors[8] = (191/255, 215/255, 234/255, 1.0)
attribute_type_colors[16] = (44/255, 102/255, 110/255, 1.0)
attribute_type_colors[32] = (155/255, 80/255, 148/255, 1.0)

connector_radius = 5 # was 5
connector_segments = 16
connector_vertical_offset = -2
connector_horizontal_offset = -8

active_connector = None
