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

# Element definitions - 28 types (type_id, display_name, icon)
ELEMENTS = [
    # Basic Text
    ('text', 'Text', 'Aa'),
    ('typewriter_text', 'Typewriter', 'Ty|'),
    ('counter', 'Counter', '123'),
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
    # Media
    ('image', 'Image', 'IMG'),
    # 3D
    ('scatter_3d', '3D Scatter', '3D'),
    ('vector_3d', '3D Vector', 'v3'),
    # Training Visualizations
    ('loss_curve', 'Loss Curve', '📉'),
    ('decision_boundary_2d', 'Decision 2D', '◐'),
    ('xor_problem', 'XOR Problem', '⊕'),
    ('gradient_flow', 'Gradients', '←'),
    ('dropout_layer', 'Dropout', '◌'),
    ('optimizer_paths', 'Optimizers', '↯'),
    ('confusion_matrix', 'Confusion', '▦'),
]

# Default properties by element type - all with sensible sample data
ELEMENT_DEFAULTS = {
    'text': {'content': 'Text', 'width': 15, 'height': 5},
    'typewriter_text': {'content': 'Typing...', 'width': 20, 'height': 5, 'show_cursor': True, 'reveal': 'char'},
    'counter': {'value': 1000, 'prefix': '', 'suffix': '', 'decimals': 0, 'fontsize': 24, 'glow': False, 'width': 15, 'height': 8},
    'image': {'src': '', 'width': 25, 'height': 20, 'border': False, 'shadow': False},
    'code_block': {'code': '# Example code\ndef hello():\n    print("Hello!")', 'language': 'python', 'width': 30, 'height': 15},
    'code_execution': {'code': 'result = 2 + 2\nprint(result)', 'output': '4', 'width': 30, 'height': 20},
    'box': {'title': 'Box Title', 'content': 'Content here', 'width': 20, 'height': 12},
    'comparison': {'left_title': 'Before', 'left_content': 'Old approach', 'right_title': 'After', 'right_content': 'New approach', 'width': 40, 'height': 20},
    'conversation': {
        'messages': [
            {'role': 'user', 'content': 'Hello, how are you?'},
            {'role': 'assistant', 'content': 'I am doing well, thanks!'},
            {'role': 'user', 'content': 'Great to hear!'}
        ],
        'width': 35, 'height': 25
    },
    'bullet_list': {'items': ['First item', 'Second item', 'Third item'], 'width': 25, 'height': 18},
    'checklist': {'items': ['Task completed', 'Another task', 'Final task'], 'width': 25, 'height': 15},
    'timeline': {
        'events': [
            {'date': '2023', 'title': 'Started'},
            {'date': '2024', 'title': 'Progress'},
            {'date': '2025', 'title': 'Complete'}
        ],
        'width': 50, 'height': 15
    },
    'flow': {'steps': [{'title': 'Input'}, {'title': 'Process'}, {'title': 'Output'}], 'width': 50, 'height': 12},
    'grid': {
        'columns': 2, 'rows': 2,
        'items': [
            {'title': 'Cell 1', 'description': 'First'},
            {'title': 'Cell 2', 'description': 'Second'},
            {'title': 'Cell 3', 'description': 'Third'},
            {'title': 'Cell 4', 'description': 'Fourth'}
        ],
        'width': 35, 'height': 25
    },
    'stacked_boxes': {
        'items': [
            {'title': 'Layer 1', 'color': 'primary'},
            {'title': 'Layer 2', 'color': 'secondary'},
            {'title': 'Layer 3', 'color': 'accent'}
        ],
        'width': 30, 'height': 25
    },
    'arrow': {'start': {'x': 30, 'y': 50}, 'end': {'x': 70, 'y': 50}, 'style': 'simple', 'width': 2, 'head_size': 15},
    'arc_arrow': {'start': {'x': 30, 'y': 50}, 'end': {'x': 70, 'y': 50}, 'arc_height': 15, 'direction': 'up', 'width': 2},
    'particle_flow': {'start': {'x': 20, 'y': 50}, 'end': {'x': 80, 'y': 50}, 'num_particles': 20, 'spread': 0.5, 'width': 60, 'height': 8},
    'neural_network': {'layers': [3, 5, 5, 2], 'layer_labels': ['Input', 'Hidden 1', 'Hidden 2', 'Output'], 'width': 40, 'height': 30, 'show_connections': True},
    'attention_heatmap': {
        'tokens_x': ['The', 'cat', 'sat'],
        'tokens_y': ['The', 'cat', 'sat'],
        'weights': [[0.9, 0.2, 0.1], [0.2, 0.8, 0.3], [0.1, 0.3, 0.7]],
        'title': 'Attention',
        'width': 30, 'height': 30, 'show_values': True
    },
    'token_flow': {'input_text': 'Hello world', 'tokens': ['Hello', 'world'], 'width': 45, 'height': 20, 'show_embeddings': True},
    'model_comparison': {
        'models': [
            {'name': 'GPT-3', 'params': '175B', 'context': '4K', 'color': 'warning'},
            {'name': 'GPT-4', 'params': '1.7T', 'context': '128K', 'color': 'success'}
        ],
        'comparison_rows': ['Params', 'Context'],
        'width': 45, 'height': 30
    },
    'similarity_meter': {'score': 75, 'radius': 8, 'label': 'Similarity', 'width': 18, 'height': 12},
    'progress_bar': {'current': 7, 'total': 10, 'label': 'Progress', 'width': 30, 'height': 6},
    'weight_comparison': {
        'before_weights': [0.3, 0.5, 0.2],
        'after_weights': [0.7, 0.8, 0.6],
        'labels': ['Weight A', 'Weight B', 'Weight C'],
        'width': 35, 'height': 18
    },
    'parameter_slider': {'label': 'Temperature', 'description': 'Controls randomness', 'current_value': 0.7, 'min_value': 0, 'max_value': 2, 'width': 30, 'height': 10},
    'scatter_3d': {
        'points': [
            {'x': 2, 'y': 3, 'z': 1, 'color': 'accent'},
            {'x': -2, 'y': 1, 'z': 3, 'color': 'primary'},
            {'x': 1, 'y': -2, 'z': 2, 'color': 'secondary'},
            {'x': -1, 'y': -1, 'z': -2, 'color': 'warning'},
            {'x': 3, 'y': 2, 'z': -1, 'color': 'success'}
        ],
        'camera_elev': 20, 'camera_azim': 45, 'rotate_camera': False, 'width': 30, 'height': 25
    },
    'vector_3d': {
        'vectors': [
            {'x': 4, 'y': 2, 'z': 3, 'color': 'warning', 'label': 'v1'},
            {'x': -3, 'y': 4, 'z': 1, 'color': 'success', 'label': 'v2'},
            {'x': 2, 'y': -2, 'z': 4, 'color': 'accent', 'label': 'v3'}
        ],
        'camera_elev': 20, 'camera_azim': 45, 'rotate_camera': False, 'width': 30, 'height': 25
    },
    # Training Visualization Elements
    'loss_curve': {
        'values': [1.0, 0.7, 0.5, 0.35, 0.25, 0.18, 0.12, 0.09, 0.07, 0.05],
        'val_values': [],
        'title': 'Training Loss',
        'animate_draw': True,
        'show_grid': True,
        'show_min': True,
        'width': 40,
        'height': 25
    },
    'decision_boundary_2d': {
        'points': [
            {'x': 0, 'y': 0, 'label': 0},
            {'x': 0, 'y': 1, 'label': 1},
            {'x': 1, 'y': 0, 'label': 1},
            {'x': 1, 'y': 1, 'label': 0}
        ],
        'title': 'Decision Boundary',
        'animate_training': True,
        'width': 35,
        'height': 30
    },
    'xor_problem': {
        'title': 'XOR Problem',
        'epoch': 0,
        'total_epochs': 1000,
        'show_linear_attempt': False,
        'show_hidden_space': False,
        'width': 40,
        'height': 35
    },
    'gradient_flow': {
        'layers': [2, 4, 1],
        'gradient_magnitudes': [1.0, 0.3],
        'title': 'Gradient Flow',
        'animate_flow': True,
        'show_vanishing': True,
        'width': 50,
        'height': 20
    },
    'dropout_layer': {
        'num_nodes': 8,
        'dropout_rate': 0.3,
        'title': 'Dropout Layer',
        'animate_drops': True,
        'show_scaling': True,
        'seed': 42,
        'width': 30,
        'height': 20
    },
    'optimizer_paths': {
        'optimizers': [
            {'name': 'SGD', 'color': 'warning', 'path': [[-15, 12], [-10, 8], [-5, 5], [-2, 2], [0, 0]]},
            {'name': 'Adam', 'color': 'success', 'path': [[-15, -8], [-8, -4], [-2, -1], [0, 0]]},
            {'name': 'RMSprop', 'color': 'primary', 'path': [[15, 10], [8, 6], [3, 2], [0, 0]]}
        ],
        'title': 'Optimizer Comparison',
        'surface_type': 'convex',
        'animate_paths': True,
        'show_contours': True,
        'show_labels': True,
        'width': 40,
        'height': 35
    },
    'confusion_matrix': {
        'matrix': [[45, 5], [8, 42]],
        'labels': ['Neg', 'Pos'],
        'title': 'Confusion Matrix',
        'animate_fill': True,
        'show_percentages': False,
        'width': 30,
        'height': 30
    },
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

# Entry animations (fly-in directions)
ENTRY_ANIMATIONS = ['none', 'left', 'right', 'top', 'bottom', 'zoom']

# Arrow head styles
ARROW_HEAD_STYLES = ['arrow', 'circle', 'diamond', 'none']

# Step transition types
STEP_TRANSITIONS = ['none', 'fade', 'slide_left', 'slide_right', 'slide_up', 'slide_down', 'zoom']

# Canvas settings
CANVAS_WIDTH = 800
CANVAS_HEIGHT = 600
GRID_SPACING_X = 80
GRID_SPACING_Y = 60
SNAP_GRID_SIZE = 10  # Snap to 10-unit grid in 0-100 coordinate space
