"""
Constants and configuration for the Qt Designer.
Integrates with core/styling.py for consistent colors.
"""

from core.styling import PresentationStyle

# Import colors from core styling and add UI-specific extras
COLORS = {
    **PresentationStyle.COLORS,
    # UI-specific colors
    'bg': '#08080c',
    'panel': '#0d0d14',
}

# Element definitions - all 26 types (type_id, display_name, icon)
ELEMENTS = [
    # Basic Text
    ('text', 'Text', 'Aa'),
    ('typewriter_text', 'Typewriter', 'Ty|'),
    ('code_block', 'Code', '</>'),
    ('code_execution', 'Code+Out', '>>>'),
    # Containers
    ('box', 'Box', '[ ]'),
    ('comparison', 'Compare', '<>'),
    ('conversation', 'Chat', '...'),
    # Lists
    ('bullet_list', 'Bullets', '***'),
    ('checklist', 'Checklist', '[x]'),
    ('timeline', 'Timeline', 'o-o'),
    # Layout
    ('flow', 'Flow', '>>>'),
    ('grid', 'Grid', '##'),
    ('stacked_boxes', 'Stacked', '==='),
    # Connectors
    ('arrow', 'Arrow', '->'),
    ('arc_arrow', 'Arc', '~>'),
    ('particle_flow', 'Particles', '***'),
    # AI Visuals
    ('neural_network', 'Neural Net', 'ooo'),
    ('attention_heatmap', 'Attention', 'HM'),
    ('token_flow', 'Tokens', 'T>E'),
    ('model_comparison', 'Models', 'A|B'),
    # Metrics
    ('similarity_meter', 'Meter', '%'),
    ('progress_bar', 'Progress', '[=]'),
    ('weight_comparison', 'Weights', 'W'),
    ('parameter_slider', 'Slider', '-o-'),
    # 3D
    ('scatter_3d', '3D Scatter', '3D'),
    ('vector_3d', '3D Vector', 'v3'),
]

# Default properties by element type
ELEMENT_DEFAULTS = {
    'text': {'content': 'Text', 'width': 15, 'height': 5},
    'typewriter_text': {'content': 'Typing...', 'width': 20, 'height': 5, 'show_cursor': True},
    'code_block': {'code': '# code here', 'language': 'python', 'width': 30, 'height': 15},
    'code_execution': {'code': 'print("Hello")', 'output': 'Hello', 'width': 30, 'height': 20},
    'box': {'title': 'Box', 'content': '', 'width': 20, 'height': 12},
    'comparison': {'left_title': 'Before', 'right_title': 'After', 'width': 40, 'height': 20},
    'conversation': {'messages': [], 'width': 35, 'height': 25},
    'bullet_list': {'items': ['Item 1', 'Item 2', 'Item 3'], 'width': 25, 'height': 18},
    'checklist': {'items': ['Task 1', 'Task 2'], 'width': 25, 'height': 15},
    'timeline': {'events': [{'date': '2023', 'title': 'Event'}], 'width': 50, 'height': 12},
    'flow': {'steps': [{'label': 'Step 1'}, {'label': 'Step 2'}], 'width': 50, 'height': 10},
    'grid': {'columns': 2, 'rows': 2, 'items': [], 'width': 35, 'height': 25},
    'stacked_boxes': {'items': [{'title': 'Top'}, {'title': 'Bottom'}], 'width': 30, 'height': 20},
    'arrow': {'start': {'x': 30, 'y': 50}, 'end': {'x': 70, 'y': 50}, 'width': 40, 'height': 5},
    'arc_arrow': {'start': {'x': 30, 'y': 50}, 'end': {'x': 70, 'y': 50}, 'arc_height': 15, 'width': 40, 'height': 15},
    'particle_flow': {'start': {'x': 20, 'y': 50}, 'end': {'x': 80, 'y': 50}, 'num_particles': 20, 'width': 60, 'height': 8},
    'neural_network': {'layers': [3, 5, 5, 2], 'width': 40, 'height': 30},
    'attention_heatmap': {'tokens_x': ['The', 'cat', 'sat'], 'tokens_y': ['The', 'cat', 'sat'], 'width': 30, 'height': 30},
    'token_flow': {'input_text': 'Hello world', 'width': 45, 'height': 20},
    'model_comparison': {'models': [{'name': 'GPT-3'}, {'name': 'GPT-4'}], 'width': 45, 'height': 30},
    'similarity_meter': {'score': 75, 'radius': 8, 'label': 'Similarity', 'width': 18, 'height': 12},
    'progress_bar': {'current': 7, 'total': 10, 'label': 'Progress', 'width': 30, 'height': 6},
    'weight_comparison': {'before_weights': [0.3, 0.5], 'after_weights': [0.7, 0.8], 'width': 35, 'height': 15},
    'parameter_slider': {'label': 'Temperature', 'current_value': 0.7, 'min_value': 0, 'max_value': 2, 'width': 30, 'height': 8},
    'scatter_3d': {'points': [], 'camera_elev': 20, 'camera_azim': 45, 'width': 30, 'height': 25},
    'vector_3d': {'vectors': [], 'camera_elev': 20, 'camera_azim': 45, 'width': 30, 'height': 25},
}

# Animation phases and their time ranges
ANIMATION_PHASES = {
    'immediate': (0.0, 0.2),
    'early': (0.2, 0.4),
    'middle': (0.4, 0.6),
    'late': (0.6, 0.8),
    'final': (0.8, 1.0)
}

# Easing function names
EASING_FUNCTIONS = [
    'linear', 'ease_in', 'ease_out', 'ease_in_out',
    'ease_in_cubic', 'ease_out_cubic', 'elastic_out', 'bounce_out'
]

# Continuous effect types
CONTINUOUS_EFFECTS = ['none', 'pulse', 'breathing']

# Canvas settings
CANVAS_WIDTH = 800
CANVAS_HEIGHT = 600
GRID_SPACING_X = 80
GRID_SPACING_Y = 60
SNAP_GRID_SIZE = 10  # Snap to 10-unit grid in 0-100 coordinate space
