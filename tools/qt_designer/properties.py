"""
Properties panel for the Qt Designer.
Right sidebar for editing selected element properties.
"""

import json
from typing import Optional, Dict, Any, List

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QScrollArea, QLabel, QPushButton,
    QSpinBox, QDoubleSpinBox, QLineEdit, QComboBox, QCheckBox,
    QGroupBox, QFormLayout, QTabWidget, QPlainTextEdit,
    QDialog, QDialogButtonBox, QColorDialog, QHBoxLayout, QFileDialog
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont, QColor

from .constants import COLORS, EASING_FUNCTIONS, CONTINUOUS_EFFECTS, ENTRY_ANIMATIONS, ARROW_HEAD_STYLES

# Available colormaps for attention heatmap
COLORMAPS = ['accent', 'primary', 'secondary', 'warning', 'success', 'highlight']

# Arrow styles
ARROW_STYLES = ['simple', 'fancy', 'curved']

# Timeline orientations
ORIENTATIONS = ['horizontal', 'vertical']

# Arc arrow directions
DIRECTIONS = ['up', 'down']

# Typewriter reveal modes
REVEAL_MODES = ['char', 'word']


class ListEditorDialog(QDialog):
    """Dialog for editing list properties."""

    def __init__(self, title: str, items: List, item_type: str = 'string', parent=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setMinimumSize(400, 300)
        self.item_type = item_type

        layout = QVBoxLayout(self)

        # Instructions
        if item_type == 'string':
            layout.addWidget(QLabel("One item per line:"))
            self.text_edit = QPlainTextEdit()
            self.text_edit.setPlainText('\n'.join(str(i) for i in items))
            layout.addWidget(self.text_edit)
        elif item_type == 'dict':
            layout.addWidget(QLabel("JSON format (list of objects):"))
            self.text_edit = QPlainTextEdit()
            self.text_edit.setPlainText(json.dumps(items, indent=2))
            layout.addWidget(self.text_edit)
        elif item_type == 'float':
            layout.addWidget(QLabel("Comma-separated numbers:"))
            self.text_edit = QPlainTextEdit()
            self.text_edit.setPlainText(','.join(str(i) for i in items))
            layout.addWidget(self.text_edit)

        # Buttons
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    def get_items(self) -> List:
        """Parse and return the items."""
        text = self.text_edit.toPlainText().strip()
        if self.item_type == 'string':
            return [line.strip() for line in text.split('\n') if line.strip()]
        elif self.item_type == 'dict':
            try:
                return json.loads(text)
            except json.JSONDecodeError:
                return []
        elif self.item_type == 'float':
            try:
                return [float(x.strip()) for x in text.split(',') if x.strip()]
            except ValueError:
                return []
        return []


class PropertiesPanel(QWidget):
    """Right panel for editing selected element properties."""

    property_changed = Signal(str, object)

    def __init__(self):
        super().__init__()
        self.setMinimumWidth(250)
        self.setMaximumWidth(450)
        self.current_elem = None
        self.widgets = {}
        self._updating = False

        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(6)

        # Header
        header = QLabel("PROPERTIES")
        header.setFont(QFont('sans-serif', 11, QFont.Bold))
        header.setStyleSheet(f"color: {COLORS['accent']};")
        header.setAlignment(Qt.AlignCenter)
        layout.addWidget(header)

        # Element type badge
        self.type_label = QLabel("No Selection")
        self.type_label.setAlignment(Qt.AlignCenter)
        self.type_label.setStyleSheet(f"""
            background-color: {COLORS['bg_light']};
            color: {COLORS['primary']};
            padding: 8px;
            border-radius: 4px;
            font-weight: bold;
            font-size: 12px;
        """)
        layout.addWidget(self.type_label)

        # Tabs for Content / Animation
        self.tabs = QTabWidget()
        self.tabs.setStyleSheet(f"""
            QTabWidget::pane {{
                border: 1px solid {COLORS['dim']};
                border-radius: 4px;
                background: {COLORS['panel']};
            }}
            QTabBar::tab {{
                background: {COLORS['bg_light']};
                color: {COLORS['text']};
                padding: 8px 16px;
                border: 1px solid {COLORS['dim']};
                border-bottom: none;
                border-radius: 4px 4px 0 0;
            }}
            QTabBar::tab:selected {{
                background: {COLORS['panel']};
                border-color: {COLORS['primary']};
            }}
        """)

        # Content tab
        self.content_tab = QWidget()
        self.content_layout = QVBoxLayout(self.content_tab)
        self.content_layout.setContentsMargins(8, 8, 8, 8)

        self.props_scroll = QScrollArea()
        self.props_scroll.setWidgetResizable(True)
        self.props_scroll.setStyleSheet("QScrollArea { border: none; }")
        self.props_container = QWidget()
        self.props_layout = QFormLayout(self.props_container)
        self.props_layout.setSpacing(8)
        self.props_scroll.setWidget(self.props_container)
        self.content_layout.addWidget(self.props_scroll)

        self.tabs.addTab(self.content_tab, "Content")

        # Animation tab
        self.anim_tab = QWidget()
        self._create_animation_tab()
        self.tabs.addTab(self.anim_tab, "Animation")

        layout.addWidget(self.tabs)

    def _create_animation_tab(self):
        """Create the animation controls tab."""
        layout = QVBoxLayout(self.anim_tab)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(12)

        # Timing section
        timing_group = QGroupBox("Timing")
        timing_layout = QFormLayout(timing_group)

        self.duration_spin = QDoubleSpinBox()
        self.duration_spin.setRange(0.1, 5.0)
        self.duration_spin.setSingleStep(0.1)
        self.duration_spin.setValue(1.0)
        self.duration_spin.valueChanged.connect(lambda v: self._emit('duration', v))
        timing_layout.addRow("Duration:", self.duration_spin)

        self.delay_spin = QDoubleSpinBox()
        self.delay_spin.setRange(0.0, 3.0)
        self.delay_spin.setSingleStep(0.1)
        self.delay_spin.setValue(0.0)
        self.delay_spin.valueChanged.connect(lambda v: self._emit('delay', v))
        timing_layout.addRow("Delay:", self.delay_spin)

        self.speed_spin = QDoubleSpinBox()
        self.speed_spin.setRange(0.1, 4.0)
        self.speed_spin.setSingleStep(0.1)
        self.speed_spin.setValue(1.0)
        self.speed_spin.valueChanged.connect(lambda v: self._emit('speed', v))
        timing_layout.addRow("Speed:", self.speed_spin)

        layout.addWidget(timing_group)

        # Phase section
        phase_group = QGroupBox("Phase")
        phase_layout = QVBoxLayout(phase_group)
        self.phase_combo = QComboBox()
        self.phase_combo.addItems(['immediate', 'early', 'middle', 'late', 'final'])
        self.phase_combo.currentTextChanged.connect(lambda v: self._emit('animation_phase', v))
        phase_layout.addWidget(self.phase_combo)
        layout.addWidget(phase_group)

        # Easing section
        easing_group = QGroupBox("Easing")
        easing_layout = QVBoxLayout(easing_group)
        self.easing_combo = QComboBox()
        self.easing_combo.addItems(EASING_FUNCTIONS)
        self.easing_combo.currentTextChanged.connect(lambda v: self._emit('easing', v))
        easing_layout.addWidget(self.easing_combo)
        layout.addWidget(easing_group)

        # Effect section
        effect_group = QGroupBox("Continuous Effect")
        effect_layout = QVBoxLayout(effect_group)
        self.effect_combo = QComboBox()
        self.effect_combo.addItems(CONTINUOUS_EFFECTS)
        self.effect_combo.currentTextChanged.connect(lambda v: self._emit('continuous_effect', v))
        effect_layout.addWidget(self.effect_combo)
        layout.addWidget(effect_group)

        # Entry animation section
        entry_group = QGroupBox("Entry Animation")
        entry_layout = QFormLayout(entry_group)

        self.entry_combo = QComboBox()
        self.entry_combo.addItems(ENTRY_ANIMATIONS)
        self.entry_combo.currentTextChanged.connect(lambda v: self._emit('entry_animation', v))
        entry_layout.addRow("Type:", self.entry_combo)

        self.entry_distance_spin = QSpinBox()
        self.entry_distance_spin.setRange(5, 100)
        self.entry_distance_spin.setValue(30)
        self.entry_distance_spin.valueChanged.connect(lambda v: self._emit('entry_distance', v))
        entry_layout.addRow("Distance:", self.entry_distance_spin)

        layout.addWidget(entry_group)

        layout.addStretch()

    def _emit(self, prop, value):
        if not self._updating and self.current_elem is not None:
            self.property_changed.emit(prop, value)

    def set_element(self, elem_data: Optional[Dict[str, Any]]):
        """Update panel to show properties for an element."""
        self._updating = True
        self.current_elem = elem_data

        # Clear existing property widgets
        while self.props_layout.count():
            item = self.props_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        self.widgets.clear()

        if elem_data is None:
            self.type_label.setText("No Selection")
            self._updating = False
            return

        elem_type = elem_data.get('type', 'unknown')
        self.type_label.setText(elem_type.upper().replace('_', ' '))

        # Build properties based on element type
        self._add_position_props(elem_data)
        self._add_type_specific_props(elem_data, elem_type)

        # Update animation controls
        self.duration_spin.setValue(elem_data.get('duration', 1.0))
        self.delay_spin.setValue(elem_data.get('delay', 0.0))
        self.speed_spin.setValue(elem_data.get('speed', 1.0))
        self.phase_combo.setCurrentText(elem_data.get('animation_phase', 'early'))
        self.easing_combo.setCurrentText(elem_data.get('easing', 'ease_in_out'))
        self.effect_combo.setCurrentText(elem_data.get('continuous_effect', 'none'))
        self.entry_combo.setCurrentText(elem_data.get('entry_animation', 'none'))
        self.entry_distance_spin.setValue(elem_data.get('entry_distance', 30))

        self._updating = False

    def _add_position_props(self, elem_data):
        """Add x, y position properties."""
        pos = elem_data.get('position', {'x': 50, 'y': 50})
        self._add_spin('x', pos.get('x', 50), 0, 100)
        self._add_spin('y', pos.get('y', 50), 0, 100)

    def _add_type_specific_props(self, elem_data, elem_type):
        """Add properties specific to element type."""
        if elem_type in ('text', 'typewriter_text'):
            self._add_line('content', elem_data.get('content', ''))
            self._add_spin('width', elem_data.get('width', 15), 5, 100)
            self._add_spin('height', elem_data.get('height', 5), 3, 100)
            self._add_color('color', elem_data.get('color', 'text'))
            self._add_spin('fontsize', elem_data.get('fontsize', 14), 8, 48)
            self._add_check('highlight', elem_data.get('highlight', False))
            self._add_color('highlight_color', elem_data.get('highlight_color', 'accent'))
            self._add_check('underline', elem_data.get('underline', False))
            self._add_color('underline_color', elem_data.get('underline_color', 'primary'))
            if elem_type == 'typewriter_text':
                self._add_check('show_cursor', elem_data.get('show_cursor', True))
                self._add_line('cursor_char', elem_data.get('cursor_char', '|'))
                self._add_combo('reveal', elem_data.get('reveal', 'char'), REVEAL_MODES)

        elif elem_type == 'counter':
            self._add_float('value', elem_data.get('value', 1000), -1e9, 1e9)
            self._add_line('prefix', elem_data.get('prefix', ''))
            self._add_line('suffix', elem_data.get('suffix', ''))
            self._add_spin('decimals', elem_data.get('decimals', 0), 0, 6)
            self._add_spin('fontsize', elem_data.get('fontsize', 24), 12, 72)
            self._add_spin('width', elem_data.get('width', 15), 5, 100)
            self._add_spin('height', elem_data.get('height', 8), 3, 100)
            self._add_color('color', elem_data.get('color', 'text'))
            self._add_check('glow', elem_data.get('glow', False))
            self._add_color('glow_color', elem_data.get('glow_color', 'accent'))

        elif elem_type == 'image':
            self._add_file_picker('src', elem_data.get('src', ''))
            self._add_spin('width', elem_data.get('width', 25), 5, 100)
            self._add_spin('height', elem_data.get('height', 20), 5, 100)
            self._add_check('border', elem_data.get('border', False))
            self._add_color('border_color', elem_data.get('border_color', 'dim'))
            self._add_check('shadow', elem_data.get('shadow', False))

        elif elem_type in ('code_block', 'code_execution'):
            self._add_text('code', elem_data.get('code', ''))
            self._add_line('language', elem_data.get('language', 'python'))
            self._add_spin('width', elem_data.get('width', 30), 10, 100)
            self._add_spin('height', elem_data.get('height', 15), 5, 100)
            if elem_type == 'code_execution':
                self._add_text('output', elem_data.get('output', ''))
                self._add_check('stagger', elem_data.get('stagger', True))

        elif elem_type == 'box':
            self._add_line('title', elem_data.get('title', ''))
            self._add_line('content', elem_data.get('content', ''))
            self._add_spin('width', elem_data.get('width', 20), 5, 100)
            self._add_spin('height', elem_data.get('height', 12), 5, 100)
            self._add_color('color', elem_data.get('color', 'primary'))
            self._add_check('shadow', elem_data.get('shadow', False))
            self._add_check('glow', elem_data.get('glow', False))
            self._add_color('glow_color', elem_data.get('glow_color', 'accent'))

        elif elem_type == 'comparison':
            self._add_line('left_title', elem_data.get('left_title', 'Before'))
            self._add_line('left_content', elem_data.get('left_content', ''))
            self._add_line('right_title', elem_data.get('right_title', 'After'))
            self._add_line('right_content', elem_data.get('right_content', ''))
            self._add_spin('width', elem_data.get('width', 40), 10, 100)
            self._add_spin('height', elem_data.get('height', 20), 10, 100)
            self._add_color('left_color', elem_data.get('left_color', 'warning'))
            self._add_color('right_color', elem_data.get('right_color', 'success'))

        elif elem_type in ('bullet_list', 'checklist'):
            self._add_list_button('items', elem_data.get('items', []), 'string')
            self._add_spin('width', elem_data.get('width', 25), 10, 100)
            self._add_spin('height', elem_data.get('height', 18), 10, 100)
            self._add_float('spacing', elem_data.get('spacing', 6.0), 2, 20)
            self._add_check('stagger', elem_data.get('stagger', True))
            self._add_line('bullet_char', elem_data.get('bullet_char', '•'))
            self._add_color('text_color', elem_data.get('text_color', 'text'))
            if elem_type == 'checklist':
                self._add_color('check_color', elem_data.get('check_color', 'success'))

        elif elem_type == 'flow':
            self._add_list_button('steps', elem_data.get('steps', []), 'dict')
            self._add_spin('width', elem_data.get('width', 50), 20, 100)
            self._add_spin('height', elem_data.get('height', 10), 5, 100)
            self._add_check('stagger', elem_data.get('stagger', True))

        elif elem_type == 'grid':
            self._add_spin('columns', elem_data.get('columns', 2), 1, 6)
            self._add_spin('rows', elem_data.get('rows', 2), 1, 6)
            self._add_list_button('items', elem_data.get('items', []), 'dict')
            self._add_spin('width', elem_data.get('width', 35), 15, 100)
            self._add_spin('height', elem_data.get('height', 25), 15, 100)
            self._add_spin('cell_width', elem_data.get('cell_width', 15), 5, 50)
            self._add_spin('cell_height', elem_data.get('cell_height', 10), 5, 50)

        elif elem_type in ('arrow', 'arc_arrow', 'particle_flow'):
            start = elem_data.get('start', {'x': 30, 'y': 50})
            end = elem_data.get('end', {'x': 70, 'y': 50})
            self._add_spin('start_x', start.get('x', 30), 0, 100)
            self._add_spin('start_y', start.get('y', 50), 0, 100)
            self._add_spin('end_x', end.get('x', 70), 0, 100)
            self._add_spin('end_y', end.get('y', 50), 0, 100)
            self._add_color('color', elem_data.get('color', 'primary'))
            self._add_float('width', elem_data.get('width', 2.0), 0.5, 10)
            if elem_type == 'arrow':
                self._add_float('head_size', elem_data.get('head_size', 15), 5, 40)
                self._add_combo('style', elem_data.get('style', 'simple'), ARROW_STYLES)
                self._add_combo('head_style', elem_data.get('head_style', 'arrow'), ARROW_HEAD_STYLES)
                self._add_check('draw_animation', elem_data.get('draw_animation', False))
                self._add_check('marching_ants', elem_data.get('marching_ants', False))
            if elem_type == 'arc_arrow':
                self._add_spin('arc_height', elem_data.get('arc_height', 15), 1, 50)
                self._add_combo('direction', elem_data.get('direction', 'up'), DIRECTIONS)
                self._add_check('glow', elem_data.get('glow', False))
                self._add_check('draw_animation', elem_data.get('draw_animation', False))
            if elem_type == 'particle_flow':
                self._add_spin('num_particles', elem_data.get('num_particles', 20), 5, 100)
                self._add_float('spread', elem_data.get('spread', 0.5), 0, 3)
                self._add_float('particle_size', elem_data.get('particle_size', 0.7), 0.2, 3)

        elif elem_type == 'neural_network':
            layers = elem_data.get('layers', [3, 5, 5, 2])
            self._add_line('layers', ','.join(map(str, layers)))
            self._add_list_button('layer_labels', elem_data.get('layer_labels', []), 'string')
            self._add_spin('width', elem_data.get('width', 40), 20, 100)
            self._add_spin('height', elem_data.get('height', 30), 15, 100)
            self._add_check('show_connections', elem_data.get('show_connections', True))
            self._add_color('node_color', elem_data.get('node_color', 'primary'))
            self._add_color('connection_color', elem_data.get('connection_color', 'dim'))

        elif elem_type == 'similarity_meter':
            self._add_spin('score', elem_data.get('score', 75), 0, 100)
            self._add_spin('radius', elem_data.get('radius', 8), 3, 20)
            self._add_line('label', elem_data.get('label', 'Similarity'))
            self._add_spin('width', elem_data.get('width', 18), 10, 50)
            self._add_spin('height', elem_data.get('height', 12), 8, 50)
            self._add_color('low_color', elem_data.get('low_color', 'warning'))
            self._add_color('medium_color', elem_data.get('medium_color', 'accent'))
            self._add_color('high_color', elem_data.get('high_color', 'success'))
            self._add_check('show_needle', elem_data.get('show_needle', True))
            self._add_check('animate_needle', elem_data.get('animate_needle', True))
            self._add_check('glow', elem_data.get('glow', False))

        elif elem_type == 'progress_bar':
            self._add_spin('current', elem_data.get('current', 5), 0, 1000)
            self._add_spin('total', elem_data.get('total', 10), 1, 1000)
            self._add_spin('width', elem_data.get('width', 30), 10, 100)
            self._add_spin('height', elem_data.get('height', 4), 2, 20)
            self._add_line('label', elem_data.get('label', 'Progress'))
            self._add_color('color', elem_data.get('color', 'success'))
            self._add_check('animate_fill', elem_data.get('animate_fill', True))
            self._add_check('show_percent', elem_data.get('show_percent', True))
            self._add_check('glow', elem_data.get('glow', False))

        elif elem_type == 'parameter_slider':
            self._add_line('label', elem_data.get('label', 'Parameter'))
            self._add_line('description', elem_data.get('description', ''))
            self._add_float('current_value', elem_data.get('current_value', 0.5), -100, 100)
            self._add_float('min_value', elem_data.get('min_value', 0), -100, 100)
            self._add_float('max_value', elem_data.get('max_value', 1), -100, 100)
            self._add_spin('width', elem_data.get('width', 30), 10, 100)
            self._add_spin('height', elem_data.get('height', 8), 5, 30)
            self._add_color('color', elem_data.get('color', 'accent'))

        elif elem_type in ('scatter_3d', 'vector_3d'):
            self._add_float('camera_elev', elem_data.get('camera_elev', 20), -90, 90)
            self._add_float('camera_azim', elem_data.get('camera_azim', 45), 0, 360)
            self._add_check('rotate_camera', elem_data.get('rotate_camera', False))
            self._add_float('camera_rotation_speed', elem_data.get('camera_rotation_speed', 30), 5, 180)
            self._add_spin('width', elem_data.get('width', 30), 15, 100)
            self._add_spin('height', elem_data.get('height', 25), 15, 100)
            list_name = 'points' if elem_type == 'scatter_3d' else 'vectors'
            self._add_list_button(list_name, elem_data.get(list_name, []), 'dict')
            if elem_type == 'scatter_3d':
                self._add_check('show_vectors', elem_data.get('show_vectors', False))
                self._add_check('stagger_points', elem_data.get('stagger_points', True))

        elif elem_type == 'attention_heatmap':
            self._add_list_button('tokens_x', elem_data.get('tokens_x', []), 'string')
            self._add_list_button('tokens_y', elem_data.get('tokens_y', []), 'string')
            self._add_line('title', elem_data.get('title', ''))
            self._add_spin('width', elem_data.get('width', 30), 10, 100)
            self._add_spin('height', elem_data.get('height', 30), 10, 100)
            self._add_check('show_values', elem_data.get('show_values', True))
            self._add_check('stagger', elem_data.get('stagger', True))
            self._add_combo('colormap', elem_data.get('colormap', 'accent'), COLORMAPS)

        elif elem_type == 'token_flow':
            self._add_line('input_text', elem_data.get('input_text', 'Hello world'))
            self._add_list_button('tokens', elem_data.get('tokens', []), 'string')
            self._add_spin('width', elem_data.get('width', 45), 20, 100)
            self._add_spin('height', elem_data.get('height', 20), 10, 100)
            self._add_check('show_embeddings', elem_data.get('show_embeddings', True))
            self._add_check('stagger', elem_data.get('stagger', True))

        elif elem_type == 'weight_comparison':
            self._add_list_button('before_weights', elem_data.get('before_weights', []), 'float')
            self._add_list_button('after_weights', elem_data.get('after_weights', []), 'float')
            self._add_list_button('labels', elem_data.get('labels', []), 'string')
            self._add_spin('width', elem_data.get('width', 35), 15, 100)
            self._add_spin('height', elem_data.get('height', 15), 10, 100)
            self._add_float('bar_height', elem_data.get('bar_height', 3), 1, 10)
            self._add_check('animate_bars', elem_data.get('animate_bars', True))

        elif elem_type == 'conversation':
            self._add_list_button('messages', elem_data.get('messages', []), 'dict')
            self._add_spin('width', elem_data.get('width', 35), 15, 100)
            self._add_spin('height', elem_data.get('height', 25), 10, 100)
            self._add_float('bubble_spacing', elem_data.get('bubble_spacing', 2), 1, 10)
            self._add_color('user_color', elem_data.get('user_color', 'primary'))
            self._add_color('assistant_color', elem_data.get('assistant_color', 'secondary'))
            self._add_color('system_color', elem_data.get('system_color', 'dim'))

        elif elem_type == 'timeline':
            self._add_list_button('events', elem_data.get('events', []), 'dict')
            self._add_spin('width', elem_data.get('width', 50), 20, 100)
            self._add_spin('height', elem_data.get('height', 15), 10, 100)
            self._add_combo('orientation', elem_data.get('orientation', 'horizontal'), ORIENTATIONS)
            self._add_color('line_color', elem_data.get('line_color', 'dim'))
            self._add_check('stagger', elem_data.get('stagger', True))

        elif elem_type == 'stacked_boxes':
            self._add_list_button('items', elem_data.get('items', []), 'dict')
            self._add_spin('base_width', elem_data.get('base_width', 40), 10, 100)
            self._add_spin('box_height', elem_data.get('box_height', 10), 5, 30)
            self._add_spin('width_decrease', elem_data.get('width_decrease', 4), 0, 15)
            self._add_spin('spacing', elem_data.get('spacing', 12), 5, 30)
            self._add_check('stagger', elem_data.get('stagger', True))

        elif elem_type == 'model_comparison':
            self._add_list_button('models', elem_data.get('models', []), 'dict')
            self._add_list_button('comparison_rows', elem_data.get('comparison_rows', []), 'string')
            self._add_spin('width', elem_data.get('width', 45), 20, 100)
            self._add_spin('height', elem_data.get('height', 30), 15, 100)
            self._add_check('stagger', elem_data.get('stagger', True))

        # Training Visualization Elements
        elif elem_type == 'loss_curve':
            self._add_line('title', elem_data.get('title', 'Training Loss'))
            default_values = [1.0, 0.7, 0.5, 0.35, 0.25, 0.18, 0.12, 0.09, 0.07, 0.05]
            self._add_list_button('values', elem_data.get('values', default_values), 'float')
            self._add_list_button('val_values', elem_data.get('val_values', []), 'float')
            self._add_spin('width', elem_data.get('width', 40), 20, 100)
            self._add_spin('height', elem_data.get('height', 25), 15, 100)
            self._add_check('animate_draw', elem_data.get('animate_draw', True))
            self._add_check('show_grid', elem_data.get('show_grid', True))
            self._add_check('show_min', elem_data.get('show_min', True))
            self._add_color('line_color', elem_data.get('line_color', 'primary'))
            self._add_color('val_line_color', elem_data.get('val_line_color', 'warning'))

        elif elem_type in ('decision_boundary_2d', 'xor_problem'):
            self._add_line('title', elem_data.get('title', 'Decision Boundary' if elem_type == 'decision_boundary_2d' else 'XOR Problem'))
            self._add_spin('width', elem_data.get('width', 35), 20, 100)
            self._add_spin('height', elem_data.get('height', 30), 20, 100)
            default_points = [{'x': 0, 'y': 0, 'label': 0}, {'x': 0, 'y': 1, 'label': 1},
                             {'x': 1, 'y': 0, 'label': 1}, {'x': 1, 'y': 1, 'label': 0}]
            self._add_list_button('points', elem_data.get('points', default_points), 'dict')
            self._add_check('animate_training', elem_data.get('animate_training', True))
            if elem_type == 'xor_problem':
                self._add_spin('epoch', elem_data.get('epoch', 0), 0, 10000)
                self._add_spin('total_epochs', elem_data.get('total_epochs', 1000), 1, 100000)
                self._add_check('show_linear_attempt', elem_data.get('show_linear_attempt', False))
                self._add_check('show_hidden_space', elem_data.get('show_hidden_space', False))

        elif elem_type == 'gradient_flow':
            self._add_line('title', elem_data.get('title', 'Gradient Flow'))
            layers = elem_data.get('layers', [3, 5, 5, 2])
            self._add_line('layers', ','.join(map(str, layers)))
            default_gradients = [1.0, 0.5, 0.2, 0.05]
            self._add_list_button('gradient_magnitudes', elem_data.get('gradient_magnitudes', default_gradients), 'float')
            self._add_spin('width', elem_data.get('width', 50), 25, 100)
            self._add_spin('height', elem_data.get('height', 20), 10, 50)
            self._add_check('animate_flow', elem_data.get('animate_flow', True))
            self._add_check('show_vanishing', elem_data.get('show_vanishing', True))

        elif elem_type == 'dropout_layer':
            self._add_line('title', elem_data.get('title', 'Dropout Layer'))
            self._add_spin('num_nodes', elem_data.get('num_nodes', 8), 4, 32)
            self._add_float('dropout_rate', elem_data.get('dropout_rate', 0.3), 0.0, 0.9)
            self._add_spin('width', elem_data.get('width', 30), 15, 80)
            self._add_spin('height', elem_data.get('height', 20), 10, 50)
            self._add_check('animate_drops', elem_data.get('animate_drops', True))
            self._add_check('show_scaling', elem_data.get('show_scaling', True))
            self._add_spin('seed', elem_data.get('seed', 42), 0, 9999)

        elif elem_type == 'optimizer_paths':
            self._add_line('title', elem_data.get('title', 'Optimizer Comparison'))
            default_optimizers = [
                {'name': 'SGD', 'color': 'warning', 'path': [[-15, 12], [-10, 8], [-5, 5], [-2, 2], [0, 0]]},
                {'name': 'Adam', 'color': 'success', 'path': [[-15, -8], [-8, -4], [-2, -1], [0, 0]]},
                {'name': 'RMSprop', 'color': 'primary', 'path': [[15, 10], [8, 6], [3, 2], [0, 0]]}
            ]
            self._add_list_button('optimizers', elem_data.get('optimizers', default_optimizers), 'dict')
            self._add_spin('width', elem_data.get('width', 40), 20, 100)
            self._add_spin('height', elem_data.get('height', 35), 20, 100)
            self._add_combo('surface_type', elem_data.get('surface_type', 'convex'), ['convex', 'saddle', 'local_minima'])
            self._add_check('animate_paths', elem_data.get('animate_paths', True))
            self._add_check('show_contours', elem_data.get('show_contours', True))
            self._add_check('show_labels', elem_data.get('show_labels', True))

        elif elem_type == 'confusion_matrix':
            self._add_line('title', elem_data.get('title', 'Confusion Matrix'))
            self._add_list_button('matrix', elem_data.get('matrix', [[45, 5], [8, 42]]), 'dict')
            self._add_list_button('labels', elem_data.get('labels', ['Neg', 'Pos']), 'string')
            self._add_spin('width', elem_data.get('width', 30), 15, 80)
            self._add_spin('height', elem_data.get('height', 30), 15, 80)
            self._add_check('animate_fill', elem_data.get('animate_fill', True))
            self._add_check('show_percentages', elem_data.get('show_percentages', False))

    def _add_spin(self, name, value, min_v, max_v):
        spin = QSpinBox()
        spin.setRange(min_v, max_v)
        spin.setValue(int(value))
        spin.valueChanged.connect(lambda v, n=name: self._emit(n, v))
        self.props_layout.addRow(f"{name}:", spin)
        self.widgets[name] = spin

    def _add_float(self, name, value, min_v, max_v):
        spin = QDoubleSpinBox()
        spin.setRange(min_v, max_v)
        spin.setDecimals(2)
        spin.setValue(float(value))
        spin.valueChanged.connect(lambda v, n=name: self._emit(n, v))
        self.props_layout.addRow(f"{name}:", spin)
        self.widgets[name] = spin

    def _add_line(self, name, value):
        edit = QLineEdit(str(value))
        edit.textChanged.connect(lambda v, n=name: self._emit(n, v))
        self.props_layout.addRow(f"{name}:", edit)
        self.widgets[name] = edit

    def _add_file_picker(self, name, value):
        """Add a file picker with text field and browse button."""
        import os
        container = QWidget()
        layout = QHBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(4)

        # Text field showing current path
        edit = QLineEdit(str(value))
        edit.setPlaceholderText("Select an image file...")
        edit.textChanged.connect(lambda v, n=name: self._emit(n, v))
        layout.addWidget(edit, 1)

        # Browse button
        btn = QPushButton("...")
        btn.setFixedWidth(30)
        btn.setToolTip("Browse for image file")

        def browse():
            # Start in current directory or directory of current file
            start_dir = os.path.dirname(value) if value and os.path.exists(os.path.dirname(value)) else os.getcwd()
            file_path, _ = QFileDialog.getOpenFileName(
                self,
                "Select Image",
                start_dir,
                "Images (*.png *.jpg *.jpeg *.gif *.bmp *.svg);;All Files (*)"
            )
            if file_path:
                edit.setText(file_path)

        btn.clicked.connect(browse)
        layout.addWidget(btn)

        self.props_layout.addRow(f"{name}:", container)
        self.widgets[name] = edit  # Store the edit widget for updates

    def _add_text(self, name, value):
        edit = QPlainTextEdit()
        edit.setPlainText(str(value))
        edit.setMaximumHeight(80)
        edit.textChanged.connect(lambda n=name: self._emit(n, edit.toPlainText()))
        self.props_layout.addRow(f"{name}:", edit)
        self.widgets[name] = edit

    def _add_check(self, name, value):
        check = QCheckBox()
        check.setChecked(bool(value))
        check.toggled.connect(lambda v, n=name: self._emit(n, v))
        self.props_layout.addRow(f"{name}:", check)
        self.widgets[name] = check

    def _add_list_button(self, name, value, item_type):
        btn = QPushButton(f"Edit ({len(value)} items)")
        btn.clicked.connect(lambda: self._edit_list(name, item_type))
        self.props_layout.addRow(f"{name}:", btn)
        self.widgets[name] = btn

    def _add_combo(self, name, value, options):
        """Add a dropdown combo box."""
        combo = QComboBox()
        combo.addItems(options)
        combo.setCurrentText(str(value) if value in options else options[0])
        combo.currentTextChanged.connect(lambda v, n=name: self._emit(n, v))
        self.props_layout.addRow(f"{name}:", combo)
        self.widgets[name] = combo

    def _add_color(self, name, value):
        """Add a color picker button."""
        container = QWidget()
        layout = QHBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(4)

        # Color preview box
        preview = QLabel()
        preview.setFixedSize(24, 24)
        color_val = value if value else '#3B82F6'
        preview.setStyleSheet(f"background-color: {color_val}; border: 1px solid #555; border-radius: 3px;")
        layout.addWidget(preview)

        # Pick button
        btn = QPushButton("Pick")
        btn.setMaximumWidth(50)
        def pick_color():
            initial = QColor(value) if value else QColor('#3B82F6')
            color = QColorDialog.getColor(initial, self, f"Pick {name}")
            if color.isValid():
                hex_color = color.name()
                preview.setStyleSheet(f"background-color: {hex_color}; border: 1px solid #555; border-radius: 3px;")
                self._emit(name, hex_color)
        btn.clicked.connect(pick_color)
        layout.addWidget(btn)

        # Color name dropdown for named colors
        named = QComboBox()
        named.addItems(['custom'] + list(COLORS.keys()))
        if value in COLORS:
            named.setCurrentText(value)
        elif value in COLORS.values():
            # Find key by value
            for k, v in COLORS.items():
                if v == value:
                    named.setCurrentText(k)
                    break
        def on_named_change(text):
            if text != 'custom' and text in COLORS:
                hex_color = COLORS[text]
                preview.setStyleSheet(f"background-color: {hex_color}; border: 1px solid #555; border-radius: 3px;")
                self._emit(name, text)  # Emit the name, not hex
        named.currentTextChanged.connect(on_named_change)
        layout.addWidget(named)

        self.props_layout.addRow(f"{name}:", container)
        self.widgets[name] = container

    def _edit_list(self, name, item_type):
        if self.current_elem is None:
            return
        items = self.current_elem.get(name, [])
        dialog = ListEditorDialog(f"Edit {name}", items, item_type, self)
        if dialog.exec() == QDialog.Accepted:
            new_items = dialog.get_items()
            self._emit(name, new_items)
            self.widgets[name].setText(f"Edit ({len(new_items)} items)")
