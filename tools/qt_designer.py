"""
Presentation Designer - PySide6 Version (Full Featured)
A proper GUI toolkit for a proper visual editor.

Usage:
    python -m tools.qt_designer [schema.json]
"""

import sys
import json
import copy
from pathlib import Path
from typing import Optional, Dict, Any, List

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QGraphicsView, QGraphicsScene, QGraphicsItem, QGraphicsRectItem,
    QGraphicsEllipseItem, QGraphicsTextItem, QGraphicsLineItem,
    QGraphicsPathItem, QGraphicsPolygonItem,
    QListWidget, QListWidgetItem, QScrollArea, QLabel, QPushButton,
    QSlider, QSpinBox, QDoubleSpinBox, QLineEdit, QComboBox, QCheckBox,
    QGroupBox, QFormLayout, QSplitter, QFileDialog, QMessageBox,
    QDockWidget, QToolBar, QStatusBar, QFrame, QSizePolicy,
    QTabWidget, QTextEdit, QDialog, QDialogButtonBox, QPlainTextEdit,
    QInputDialog
)
from PySide6.QtCore import Qt, QRectF, QPointF, Signal, QTimer, QLineF
from PySide6.QtGui import (
    QColor, QPen, QBrush, QFont, QPainter, QAction, QKeySequence,
    QWheelEvent, QTransform, QPainterPath, QPolygonF, QLinearGradient,
    QRadialGradient, QUndoStack, QUndoCommand
)

import numpy as np
import math

# Matplotlib with Qt backend
import matplotlib
matplotlib.use('QtAgg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.patches import (
    FancyBboxPatch, Circle, Wedge, Rectangle, FancyArrowPatch, Arc, Polygon
)
from matplotlib.lines import Line2D

# Color palette matching the original designer
COLORS = {
    'primary': '#3B82F6',
    'secondary': '#10B981',
    'accent': '#F59E0B',
    'highlight': '#EC4899',
    'warning': '#EF4444',
    'success': '#10B981',
    'text': '#F0F0F0',
    'dim': '#6B7280',
    'bg': '#08080c',
    'bg_light': '#1a1a2e',
    'panel': '#0d0d14',
}

# Element definitions - all 26 types
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
    ('bullet_list', 'Bullets', '•••'),
    ('checklist', 'Checklist', '[x]'),
    ('timeline', 'Timeline', 'o-o'),
    # Layout
    ('flow', 'Flow', '>>>'),
    ('grid', 'Grid', '##'),
    ('stacked_boxes', 'Stacked', '≡'),
    # Connectors
    ('arrow', 'Arrow', '→'),
    ('arc_arrow', 'Arc', '↷'),
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


class MoveCommand(QUndoCommand):
    """Undo command for element movement."""
    def __init__(self, item, old_pos, new_pos):
        super().__init__("Move Element")
        self.item = item
        self.old_pos = old_pos
        self.new_pos = new_pos

    def redo(self):
        self.item.setPos(self.new_pos)
        self.item._sync_data_from_pos()

    def undo(self):
        self.item.setPos(self.old_pos)
        self.item._sync_data_from_pos()


class AddElementCommand(QUndoCommand):
    """Undo command for adding elements."""
    def __init__(self, scene, step_elements, elem_data, item):
        super().__init__(f"Add {elem_data.get('type', 'element')}")
        self.scene = scene
        self.step_elements = step_elements
        self.elem_data = elem_data
        self.item = item

    def redo(self):
        if self.elem_data not in self.step_elements:
            self.step_elements.append(self.elem_data)
        if self.item not in self.scene.items():
            self.scene.addItem(self.item)

    def undo(self):
        if self.elem_data in self.step_elements:
            self.step_elements.remove(self.elem_data)
        if self.item in self.scene.items():
            self.scene.removeItem(self.item)


class DeleteElementCommand(QUndoCommand):
    """Undo command for deleting elements."""
    def __init__(self, scene, step_elements, elem_data, item):
        super().__init__(f"Delete {elem_data.get('type', 'element')}")
        self.scene = scene
        self.step_elements = step_elements
        self.elem_data = elem_data
        self.item = item

    def redo(self):
        if self.elem_data in self.step_elements:
            self.step_elements.remove(self.elem_data)
        if self.item in self.scene.items():
            self.scene.removeItem(self.item)

    def undo(self):
        if self.elem_data not in self.step_elements:
            self.step_elements.append(self.elem_data)
        if self.item not in self.scene.items():
            self.scene.addItem(self.item)


class CanvasElement(QGraphicsRectItem):
    """A draggable, selectable element on the canvas with custom rendering."""

    def __init__(self, elem_data: Dict[str, Any], scene_rect: QRectF):
        self.elem_data = elem_data
        self.scene_rect = scene_rect
        self._moving = False
        self._start_pos = None

        # Calculate position and size
        pos = elem_data.get('position', {'x': 50, 'y': 50})
        elem_type = elem_data.get('type', 'text')
        defaults = ELEMENT_DEFAULTS.get(elem_type, {'width': 15, 'height': 10})

        w = elem_data.get('width', defaults.get('width', 15)) * 8
        h = elem_data.get('height', defaults.get('height', 10)) * 6

        x = pos['x'] / 100 * scene_rect.width()
        y = (100 - pos['y']) / 100 * scene_rect.height()

        super().__init__(0, 0, w, h)
        self.setPos(x - w/2, y - h/2)

        # Make it interactive
        self.setFlag(QGraphicsItem.ItemIsMovable)
        self.setFlag(QGraphicsItem.ItemIsSelectable)
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges)
        self.setAcceptHoverEvents(True)

        # Cache colors
        self._colors = {k: QColor(v) for k, v in COLORS.items()}

    def _sync_data_from_pos(self):
        """Sync element data from current position."""
        rect = self.scene_rect
        new_x = (self.pos().x() + self.rect().width()/2) / rect.width() * 100
        new_y = 100 - (self.pos().y() + self.rect().height()/2) / rect.height() * 100
        if 'position' not in self.elem_data:
            self.elem_data['position'] = {}
        self.elem_data['position']['x'] = round(max(0, min(100, new_x)), 1)
        self.elem_data['position']['y'] = round(max(0, min(100, new_y)), 1)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._moving = True
            self._start_pos = self.pos()
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        if self._moving and self._start_pos and self._start_pos != self.pos():
            # Create undo command
            scene = self.scene()
            if scene and hasattr(scene, 'undo_stack'):
                scene.undo_stack.push(MoveCommand(self, self._start_pos, self.pos()))
        self._moving = False
        self._start_pos = None
        super().mouseReleaseEvent(event)

    def itemChange(self, change, value):
        if change == QGraphicsItem.ItemPositionHasChanged:
            self._sync_data_from_pos()
        return super().itemChange(change, value)

    def paint(self, painter, option, widget):
        """Custom paint based on element type."""
        painter.setRenderHint(QPainter.Antialiasing)

        elem_type = self.elem_data.get('type', 'text')
        rect = self.rect()
        w, h = rect.width(), rect.height()

        # Selection highlight
        if self.isSelected():
            painter.setPen(QPen(self._colors['accent'], 3))
        else:
            painter.setPen(QPen(self._colors['primary'], 2))

        # Draw based on type
        if elem_type == 'text':
            self._draw_text(painter, rect)
        elif elem_type == 'typewriter_text':
            self._draw_typewriter(painter, rect)
        elif elem_type == 'code_block':
            self._draw_code_block(painter, rect)
        elif elem_type == 'code_execution':
            self._draw_code_execution(painter, rect)
        elif elem_type == 'box':
            self._draw_box(painter, rect)
        elif elem_type == 'comparison':
            self._draw_comparison(painter, rect)
        elif elem_type == 'bullet_list':
            self._draw_bullet_list(painter, rect)
        elif elem_type == 'checklist':
            self._draw_checklist(painter, rect)
        elif elem_type == 'flow':
            self._draw_flow(painter, rect)
        elif elem_type == 'grid':
            self._draw_grid(painter, rect)
        elif elem_type in ('arrow', 'arc_arrow'):
            self._draw_arrow(painter, rect, elem_type == 'arc_arrow')
        elif elem_type == 'particle_flow':
            self._draw_particle_flow(painter, rect)
        elif elem_type == 'neural_network':
            self._draw_neural_network(painter, rect)
        elif elem_type == 'similarity_meter':
            self._draw_similarity_meter(painter, rect)
        elif elem_type == 'progress_bar':
            self._draw_progress_bar(painter, rect)
        elif elem_type == 'parameter_slider':
            self._draw_parameter_slider(painter, rect)
        elif elem_type in ('scatter_3d', 'vector_3d'):
            self._draw_3d_placeholder(painter, rect, elem_type)
        elif elem_type == 'attention_heatmap':
            self._draw_attention_heatmap(painter, rect)
        elif elem_type == 'token_flow':
            self._draw_token_flow(painter, rect)
        else:
            self._draw_generic(painter, rect, elem_type)

    def _draw_text(self, painter, rect):
        painter.setBrush(Qt.NoBrush)
        painter.drawRoundedRect(rect, 4, 4)
        content = self.elem_data.get('content', 'Text')
        painter.setPen(self._colors['text'])
        painter.setFont(QFont('sans-serif', 11))
        painter.drawText(rect, Qt.AlignCenter, content[:30])

    def _draw_typewriter(self, painter, rect):
        painter.setBrush(Qt.NoBrush)
        painter.drawRoundedRect(rect, 4, 4)
        content = self.elem_data.get('content', 'Typing...')
        if self.elem_data.get('show_cursor', True):
            content += '|'
        painter.setPen(self._colors['text'])
        painter.setFont(QFont('monospace', 10))
        painter.drawText(rect, Qt.AlignCenter, content[:25])

    def _draw_code_block(self, painter, rect):
        painter.setBrush(QBrush(QColor('#0d1117')))
        painter.drawRoundedRect(rect, 6, 6)
        code = self.elem_data.get('code', '# code')
        painter.setPen(self._colors['secondary'])
        painter.setFont(QFont('monospace', 9))
        painter.drawText(rect.adjusted(8, 8, -8, -8), Qt.AlignTop | Qt.AlignLeft, code[:50])

    def _draw_code_execution(self, painter, rect):
        # Code section
        code_rect = QRectF(rect.x(), rect.y(), rect.width(), rect.height() * 0.6)
        painter.setBrush(QBrush(QColor('#0d1117')))
        painter.drawRoundedRect(code_rect, 6, 6)

        # Output section
        out_rect = QRectF(rect.x(), rect.y() + rect.height() * 0.65, rect.width(), rect.height() * 0.35)
        painter.setPen(QPen(self._colors['success'], 2))
        painter.setBrush(QBrush(self._colors['bg_light']))
        painter.drawRoundedRect(out_rect, 6, 6)

        # Text
        painter.setPen(self._colors['text'])
        painter.setFont(QFont('monospace', 8))
        painter.drawText(code_rect.adjusted(6, 6, -6, -6), Qt.AlignTop, self.elem_data.get('code', '>>>')[:30])
        painter.setPen(self._colors['success'])
        painter.drawText(out_rect.adjusted(6, 4, -6, -4), Qt.AlignTop, self.elem_data.get('output', 'output')[:20])

    def _draw_box(self, painter, rect):
        painter.setBrush(QBrush(self._colors['bg_light']))
        painter.drawRoundedRect(rect, 8, 8)
        title = self.elem_data.get('title', '')
        if title:
            painter.setPen(self._colors['primary'])
            painter.setFont(QFont('sans-serif', 10, QFont.Bold))
            painter.drawText(rect.adjusted(0, 8, 0, 0), Qt.AlignHCenter | Qt.AlignTop, title[:20])
        content = self.elem_data.get('content', '')
        if content:
            painter.setPen(self._colors['text'])
            painter.setFont(QFont('sans-serif', 9))
            painter.drawText(rect.adjusted(8, 28, -8, -8), Qt.AlignTop, content[:50])

    def _draw_comparison(self, painter, rect):
        half_w = rect.width() / 2 - 4
        # Left box
        left_rect = QRectF(rect.x(), rect.y(), half_w, rect.height())
        painter.setPen(QPen(self._colors['warning'], 2))
        painter.setBrush(QBrush(self._colors['bg_light']))
        painter.drawRoundedRect(left_rect, 6, 6)
        # Right box
        right_rect = QRectF(rect.x() + half_w + 8, rect.y(), half_w, rect.height())
        painter.setPen(QPen(self._colors['success'], 2))
        painter.drawRoundedRect(right_rect, 6, 6)
        # Labels
        painter.setFont(QFont('sans-serif', 9, QFont.Bold))
        painter.setPen(self._colors['warning'])
        painter.drawText(left_rect, Qt.AlignCenter, self.elem_data.get('left_title', 'Before')[:10])
        painter.setPen(self._colors['success'])
        painter.drawText(right_rect, Qt.AlignCenter, self.elem_data.get('right_title', 'After')[:10])

    def _draw_bullet_list(self, painter, rect):
        painter.setBrush(Qt.NoBrush)
        painter.drawRoundedRect(rect, 4, 4)
        items = self.elem_data.get('items', [])[:5]
        painter.setPen(self._colors['text'])
        painter.setFont(QFont('sans-serif', 9))
        y = rect.y() + 12
        for item in items:
            painter.drawText(rect.x() + 10, y, f"• {item[:20]}")
            y += 16

    def _draw_checklist(self, painter, rect):
        painter.setBrush(Qt.NoBrush)
        painter.drawRoundedRect(rect, 4, 4)
        items = self.elem_data.get('items', [])[:4]
        y = rect.y() + 14
        for item in items:
            # Checkbox
            cb_rect = QRectF(rect.x() + 8, y - 8, 12, 12)
            painter.setPen(QPen(self._colors['success'], 2))
            painter.setBrush(QBrush(self._colors['success']))
            painter.drawRoundedRect(cb_rect, 2, 2)
            # Text
            painter.setPen(self._colors['text'])
            painter.setFont(QFont('sans-serif', 9))
            painter.drawText(rect.x() + 26, y + 2, item[:18])
            y += 20

    def _draw_flow(self, painter, rect):
        steps = self.elem_data.get('steps', [])[:5]
        if not steps:
            steps = [{'label': 'Step'}]
        step_w = rect.width() / len(steps) - 8
        x = rect.x() + 4
        for i, step in enumerate(steps):
            step_rect = QRectF(x, rect.y() + 4, step_w, rect.height() - 8)
            painter.setPen(QPen(self._colors['primary'], 2))
            painter.setBrush(QBrush(self._colors['bg_light']))
            painter.drawRoundedRect(step_rect, 6, 6)
            painter.setPen(self._colors['text'])
            painter.setFont(QFont('sans-serif', 8))
            painter.drawText(step_rect, Qt.AlignCenter, step.get('label', f'S{i+1}')[:8])
            # Arrow
            if i < len(steps) - 1:
                painter.setPen(QPen(self._colors['dim'], 2))
                ax = x + step_w + 2
                ay = rect.y() + rect.height() / 2
                painter.drawLine(QPointF(ax, ay), QPointF(ax + 4, ay))
            x += step_w + 8

    def _draw_grid(self, painter, rect):
        cols = self.elem_data.get('columns', 2)
        rows = self.elem_data.get('rows', 2)
        cell_w = rect.width() / cols - 4
        cell_h = rect.height() / rows - 4
        items = self.elem_data.get('items', [])
        idx = 0
        for r in range(rows):
            for c in range(cols):
                cell_rect = QRectF(rect.x() + c * (cell_w + 4) + 2,
                                   rect.y() + r * (cell_h + 4) + 2,
                                   cell_w, cell_h)
                painter.setPen(QPen(self._colors['primary'], 1))
                painter.setBrush(QBrush(self._colors['bg_light']))
                painter.drawRoundedRect(cell_rect, 4, 4)
                if idx < len(items):
                    painter.setPen(self._colors['text'])
                    painter.setFont(QFont('sans-serif', 7))
                    painter.drawText(cell_rect, Qt.AlignCenter, items[idx].get('title', '')[:8])
                idx += 1

    def _draw_arrow(self, painter, rect, is_arc=False):
        painter.setBrush(Qt.NoBrush)
        # Draw bounding box faintly
        painter.setPen(QPen(self._colors['dim'], 1, Qt.DotLine))
        painter.drawRect(rect)
        # Arrow line
        painter.setPen(QPen(self._colors['primary'], 3))
        start_x = rect.x() + 10
        end_x = rect.x() + rect.width() - 10
        y = rect.y() + rect.height() / 2
        if is_arc:
            path = QPainterPath()
            path.moveTo(start_x, y)
            ctrl_y = y - self.elem_data.get('arc_height', 15) * 2
            path.quadTo((start_x + end_x) / 2, ctrl_y, end_x, y)
            painter.drawPath(path)
        else:
            painter.drawLine(QPointF(start_x, y), QPointF(end_x - 10, y))
        # Arrowhead
        painter.setBrush(QBrush(self._colors['primary']))
        arrow_head = QPolygonF([
            QPointF(end_x, y),
            QPointF(end_x - 12, y - 6),
            QPointF(end_x - 12, y + 6)
        ])
        painter.drawPolygon(arrow_head)

    def _draw_particle_flow(self, painter, rect):
        painter.setBrush(Qt.NoBrush)
        painter.setPen(QPen(self._colors['dim'], 1, Qt.DashLine))
        painter.drawRect(rect)
        # Particles
        n = min(self.elem_data.get('num_particles', 10), 12)
        y = rect.y() + rect.height() / 2
        for i in range(n):
            t = i / max(n - 1, 1)
            px = rect.x() + 10 + (rect.width() - 20) * t
            py = y + np.sin(i * 1.2) * 8
            size = 4 + np.sin(t * 3.14) * 3
            painter.setPen(Qt.NoPen)
            painter.setBrush(QBrush(self._colors['accent']))
            painter.drawEllipse(QPointF(px, py), size, size)

    def _draw_neural_network(self, painter, rect):
        painter.setBrush(QBrush(self._colors['bg_light']))
        painter.drawRoundedRect(rect, 8, 8)
        layers = self.elem_data.get('layers', [3, 4, 2])
        spacing_x = rect.width() / (len(layers) + 1)
        for li, n in enumerate(layers):
            lx = rect.x() + (li + 1) * spacing_x
            spacing_y = rect.height() / (n + 1)
            for ni in range(n):
                ny = rect.y() + (ni + 1) * spacing_y
                painter.setPen(QPen(self._colors['text'], 1))
                painter.setBrush(QBrush(self._colors['primary']))
                painter.drawEllipse(QPointF(lx, ny), 6, 6)

    def _draw_similarity_meter(self, painter, rect):
        cx, cy = rect.x() + rect.width() / 2, rect.y() + rect.height() * 0.6
        r = min(rect.width(), rect.height()) * 0.4
        score = self.elem_data.get('score', 75)
        # Background arc
        painter.setPen(QPen(self._colors['dim'], 4))
        painter.setBrush(Qt.NoBrush)
        painter.drawArc(QRectF(cx - r, cy - r, r * 2, r * 2), 0, 180 * 16)
        # Score arc
        color = self._colors['success'] if score > 66 else (self._colors['accent'] if score > 33 else self._colors['warning'])
        painter.setPen(QPen(color, 6))
        painter.drawArc(QRectF(cx - r, cy - r, r * 2, r * 2), 180 * 16, -int(score / 100 * 180) * 16)
        # Text
        painter.setPen(self._colors['text'])
        painter.setFont(QFont('sans-serif', 12, QFont.Bold))
        painter.drawText(rect, Qt.AlignHCenter | Qt.AlignBottom, f"{score}%")

    def _draw_progress_bar(self, painter, rect):
        current = self.elem_data.get('current', 5)
        total = self.elem_data.get('total', 10)
        pct = current / max(total, 1)
        # Background
        bar_rect = QRectF(rect.x() + 10, rect.y() + rect.height() / 2 - 8, rect.width() - 20, 16)
        painter.setPen(QPen(self._colors['dim'], 1))
        painter.setBrush(QBrush(self._colors['bg_light']))
        painter.drawRoundedRect(bar_rect, 8, 8)
        # Fill
        fill_rect = QRectF(bar_rect.x(), bar_rect.y(), bar_rect.width() * pct, bar_rect.height())
        painter.setPen(Qt.NoPen)
        painter.setBrush(QBrush(self._colors['success']))
        painter.drawRoundedRect(fill_rect, 8, 8)
        # Label
        label = self.elem_data.get('label', '')
        if label:
            painter.setPen(self._colors['text'])
            painter.setFont(QFont('sans-serif', 8))
            painter.drawText(rect.adjusted(0, 4, 0, 0), Qt.AlignHCenter | Qt.AlignTop, label[:15])

    def _draw_parameter_slider(self, painter, rect):
        val = self.elem_data.get('current_value', 0.5)
        min_v = self.elem_data.get('min_value', 0)
        max_v = self.elem_data.get('max_value', 1)
        pct = (val - min_v) / (max_v - min_v) if max_v != min_v else 0.5
        # Label
        painter.setPen(self._colors['text'])
        painter.setFont(QFont('sans-serif', 9, QFont.Bold))
        painter.drawText(rect.adjusted(0, 4, 0, 0), Qt.AlignHCenter | Qt.AlignTop,
                        self.elem_data.get('label', 'Param')[:12])
        # Track
        track_rect = QRectF(rect.x() + 10, rect.y() + rect.height() / 2, rect.width() - 20, 6)
        painter.setPen(Qt.NoPen)
        painter.setBrush(QBrush(QColor('#333')))
        painter.drawRoundedRect(track_rect, 3, 3)
        # Fill
        fill_rect = QRectF(track_rect.x(), track_rect.y(), track_rect.width() * pct, track_rect.height())
        painter.setBrush(QBrush(self._colors['accent']))
        painter.drawRoundedRect(fill_rect, 3, 3)
        # Handle
        hx = track_rect.x() + track_rect.width() * pct
        painter.setPen(QPen(self._colors['accent'], 2))
        painter.setBrush(QBrush(QColor('white')))
        painter.drawEllipse(QPointF(hx, track_rect.y() + 3), 8, 8)
        # Value
        painter.setPen(self._colors['accent'])
        painter.setFont(QFont('sans-serif', 8))
        painter.drawText(rect.adjusted(0, 0, 0, -4), Qt.AlignHCenter | Qt.AlignBottom, f"{val:.2f}")

    def _draw_3d_placeholder(self, painter, rect, elem_type):
        painter.setBrush(QBrush(QColor('#0d0d14')))
        painter.drawRoundedRect(rect, 8, 8)
        # Axes
        cx, cy = rect.x() + rect.width() / 2, rect.y() + rect.height() / 2
        painter.setPen(QPen(self._colors['dim'], 1))
        painter.drawLine(QPointF(cx - 30, cy + 20), QPointF(cx + 30, cy + 20))  # X
        painter.drawLine(QPointF(cx, cy + 20), QPointF(cx, cy - 25))  # Z
        painter.drawLine(QPointF(cx, cy + 20), QPointF(cx - 20, cy + 5))  # Y
        # Label
        painter.setPen(self._colors['primary'])
        painter.setFont(QFont('sans-serif', 12, QFont.Bold))
        label = '3D' if elem_type == 'scatter_3d' else 'Vec3D'
        painter.drawText(rect, Qt.AlignCenter, label)

    def _draw_attention_heatmap(self, painter, rect):
        painter.setBrush(QBrush(self._colors['bg_light']))
        painter.drawRoundedRect(rect, 6, 6)
        tokens = self.elem_data.get('tokens_x', ['A', 'B', 'C'])[:4]
        n = len(tokens)
        cell_size = min(rect.width(), rect.height()) / (n + 1.5)
        # Grid
        for i in range(n):
            for j in range(n):
                cx = rect.x() + (j + 1.2) * cell_size
                cy = rect.y() + (i + 1.2) * cell_size
                weight = 0.3 + 0.7 * ((i + j) % 3) / 2
                color = QColor(self._colors['accent'])
                color.setAlphaF(weight)
                painter.setPen(Qt.NoPen)
                painter.setBrush(QBrush(color))
                painter.drawRect(QRectF(cx, cy, cell_size * 0.8, cell_size * 0.8))

    def _draw_token_flow(self, painter, rect):
        painter.setBrush(QBrush(self._colors['bg_light']))
        painter.drawRoundedRect(rect, 6, 6)
        text = self.elem_data.get('input_text', 'Hello')
        # Input box
        in_rect = QRectF(rect.x() + 8, rect.y() + 8, rect.width() * 0.3, rect.height() - 16)
        painter.setPen(QPen(self._colors['dim'], 1))
        painter.setBrush(QBrush(QColor('#0d0d14')))
        painter.drawRoundedRect(in_rect, 4, 4)
        painter.setPen(self._colors['text'])
        painter.setFont(QFont('sans-serif', 8))
        painter.drawText(in_rect, Qt.AlignCenter, text[:10])
        # Arrow
        painter.setPen(QPen(self._colors['dim'], 2))
        ax = rect.x() + rect.width() * 0.4
        ay = rect.y() + rect.height() / 2
        painter.drawLine(QPointF(ax, ay), QPointF(ax + 15, ay))
        # Tokens
        tokens = text.split()[:3] or ['tok']
        tx = rect.x() + rect.width() * 0.5
        for tok in tokens:
            tok_rect = QRectF(tx, rect.y() + rect.height() / 2 - 12, 30, 24)
            painter.setPen(QPen(self._colors['accent'], 1))
            painter.setBrush(QBrush(self._colors['bg_light']))
            painter.drawRoundedRect(tok_rect, 4, 4)
            painter.setPen(self._colors['accent'])
            painter.setFont(QFont('sans-serif', 7))
            painter.drawText(tok_rect, Qt.AlignCenter, tok[:5])
            tx += 35

    def _draw_generic(self, painter, rect, elem_type):
        painter.setBrush(QBrush(self._colors['bg_light']))
        painter.drawRoundedRect(rect, 6, 6)
        painter.setPen(self._colors['dim'])
        painter.setFont(QFont('sans-serif', 9))
        painter.drawText(rect, Qt.AlignCenter, elem_type[:12])


class CanvasView(QGraphicsView):
    """Zoomable, pannable canvas view."""

    element_selected = Signal(object)
    element_deselected = Signal()

    def __init__(self, undo_stack: QUndoStack):
        super().__init__()
        self.undo_stack = undo_stack

        # Setup scene
        self.scene_obj = QGraphicsScene()
        self.scene_obj.setSceneRect(0, 0, 800, 600)
        self.scene_obj.undo_stack = undo_stack
        self.setScene(self.scene_obj)

        # Rendering
        self.setRenderHint(QPainter.Antialiasing)
        self.setRenderHint(QPainter.SmoothPixmapTransform)
        self.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)

        # Background
        self.setBackgroundBrush(QBrush(QColor(COLORS['bg'])))

        # Interaction
        self.setDragMode(QGraphicsView.RubberBandDrag)
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.setResizeAnchor(QGraphicsView.AnchorUnderMouse)

        # Track zoom level
        self.zoom_level = 1.0

        # Panning state
        self._panning = False
        self._pan_start = None

        # Selection tracking
        self.scene_obj.selectionChanged.connect(self._on_selection_changed)

        # Draw grid
        self._draw_grid()

    def _draw_grid(self):
        """Draw subtle grid lines."""
        pen = QPen(QColor('#1a1a2e'), 0.5, Qt.DotLine)
        rect = self.scene_obj.sceneRect()
        for x in range(0, int(rect.width()) + 1, 80):
            line = self.scene_obj.addLine(x, 0, x, rect.height(), pen)
            line.setZValue(-100)
        for y in range(0, int(rect.height()) + 1, 60):
            line = self.scene_obj.addLine(0, y, rect.width(), y, pen)
            line.setZValue(-100)

    def _on_selection_changed(self):
        selected = self.scene_obj.selectedItems()
        if selected and isinstance(selected[0], CanvasElement):
            self.element_selected.emit(selected[0].elem_data)
        else:
            self.element_deselected.emit()

    def wheelEvent(self, event: QWheelEvent):
        """Zoom with mouse wheel."""
        factor = 1.15
        if event.angleDelta().y() > 0:
            self.zoom_level = min(5.0, self.zoom_level * factor)
            self.scale(factor, factor)
        else:
            self.zoom_level = max(0.2, self.zoom_level / factor)
            self.scale(1/factor, 1/factor)

    def mousePressEvent(self, event):
        """Handle middle mouse for panning."""
        if event.button() == Qt.MiddleButton:
            self._panning = True
            self._pan_start = event.pos()
            self.setCursor(Qt.ClosedHandCursor)
        else:
            super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self._panning and self._pan_start:
            delta = event.pos() - self._pan_start
            self._pan_start = event.pos()
            self.horizontalScrollBar().setValue(self.horizontalScrollBar().value() - delta.x())
            self.verticalScrollBar().setValue(self.verticalScrollBar().value() - delta.y())
        else:
            super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MiddleButton:
            self._panning = False
            self.setCursor(Qt.ArrowCursor)
        else:
            super().mouseReleaseEvent(event)

    def add_element(self, elem_data: Dict[str, Any]) -> CanvasElement:
        """Add an element to the canvas."""
        item = CanvasElement(elem_data, self.scene_obj.sceneRect())
        self.scene_obj.addItem(item)
        return item

    def clear_elements(self):
        """Remove all elements (but keep grid)."""
        for item in list(self.scene_obj.items()):
            if isinstance(item, CanvasElement):
                self.scene_obj.removeItem(item)

    def get_selected_item(self) -> Optional[CanvasElement]:
        """Get currently selected element."""
        selected = self.scene_obj.selectedItems()
        if selected and isinstance(selected[0], CanvasElement):
            return selected[0]
        return None


class ElementPalette(QWidget):
    """Left panel with draggable element types."""

    element_clicked = Signal(str)

    def __init__(self):
        super().__init__()
        self.setFixedWidth(160)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(4)

        # Header
        header = QLabel("ELEMENTS")
        header.setFont(QFont('sans-serif', 11, QFont.Bold))
        header.setStyleSheet(f"color: {COLORS['accent']};")
        header.setAlignment(Qt.AlignCenter)
        layout.addWidget(header)

        # Scrollable element list
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setStyleSheet("QScrollArea { border: none; background: transparent; }")

        container = QWidget()
        container_layout = QVBoxLayout(container)
        container_layout.setSpacing(3)

        for elem_type, name, icon in ELEMENTS:
            btn = QPushButton(f" {icon}  {name}")
            btn.setFixedHeight(32)
            btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: {COLORS['bg_light']};
                    color: {COLORS['text']};
                    border: 1px solid {COLORS['dim']};
                    border-radius: 4px;
                    text-align: left;
                    padding-left: 8px;
                    font-size: 11px;
                }}
                QPushButton:hover {{
                    background-color: {COLORS['primary']};
                    border-color: {COLORS['primary']};
                }}
            """)
            btn.clicked.connect(lambda checked, t=elem_type: self.element_clicked.emit(t))
            container_layout.addWidget(btn)

        container_layout.addStretch()
        scroll.setWidget(container)
        layout.addWidget(scroll)


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
        self.setFixedWidth(300)
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
        self.easing_combo.addItems([
            'linear', 'ease_in', 'ease_out', 'ease_in_out',
            'ease_in_cubic', 'ease_out_cubic', 'elastic_out', 'bounce_out'
        ])
        self.easing_combo.currentTextChanged.connect(lambda v: self._emit('easing', v))
        easing_layout.addWidget(self.easing_combo)
        layout.addWidget(easing_group)

        # Effect section
        effect_group = QGroupBox("Continuous Effect")
        effect_layout = QVBoxLayout(effect_group)
        self.effect_combo = QComboBox()
        self.effect_combo.addItems(['none', 'pulse', 'breathing'])
        self.effect_combo.currentTextChanged.connect(lambda v: self._emit('continuous_effect', v))
        effect_layout.addWidget(self.effect_combo)
        layout.addWidget(effect_group)

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
            if elem_type == 'typewriter_text':
                self._add_check('show_cursor', elem_data.get('show_cursor', True))

        elif elem_type in ('code_block', 'code_execution'):
            self._add_text('code', elem_data.get('code', ''))
            self._add_line('language', elem_data.get('language', 'python'))
            if elem_type == 'code_execution':
                self._add_line('output', elem_data.get('output', ''))

        elif elem_type == 'box':
            self._add_line('title', elem_data.get('title', ''))
            self._add_line('content', elem_data.get('content', ''))
            self._add_spin('width', elem_data.get('width', 20), 5, 100)
            self._add_spin('height', elem_data.get('height', 12), 5, 100)

        elif elem_type == 'comparison':
            self._add_line('left_title', elem_data.get('left_title', 'Before'))
            self._add_line('right_title', elem_data.get('right_title', 'After'))
            self._add_spin('width', elem_data.get('width', 40), 10, 100)
            self._add_spin('height', elem_data.get('height', 20), 10, 100)

        elif elem_type in ('bullet_list', 'checklist'):
            self._add_list_button('items', elem_data.get('items', []), 'string')
            self._add_float('spacing', elem_data.get('spacing', 6.0), 2, 20)
            self._add_check('stagger', elem_data.get('stagger', True))

        elif elem_type == 'flow':
            self._add_list_button('steps', elem_data.get('steps', []), 'dict')
            self._add_spin('width', elem_data.get('width', 50), 20, 100)
            self._add_check('stagger', elem_data.get('stagger', True))

        elif elem_type == 'grid':
            self._add_spin('columns', elem_data.get('columns', 2), 1, 6)
            self._add_spin('rows', elem_data.get('rows', 2), 1, 6)
            self._add_list_button('items', elem_data.get('items', []), 'dict')

        elif elem_type in ('arrow', 'arc_arrow', 'particle_flow'):
            start = elem_data.get('start', {'x': 30, 'y': 50})
            end = elem_data.get('end', {'x': 70, 'y': 50})
            self._add_spin('start_x', start.get('x', 30), 0, 100)
            self._add_spin('start_y', start.get('y', 50), 0, 100)
            self._add_spin('end_x', end.get('x', 70), 0, 100)
            self._add_spin('end_y', end.get('y', 50), 0, 100)
            if elem_type == 'arc_arrow':
                self._add_spin('arc_height', elem_data.get('arc_height', 15), 1, 50)
            if elem_type == 'particle_flow':
                self._add_spin('num_particles', elem_data.get('num_particles', 20), 5, 100)
                self._add_float('spread', elem_data.get('spread', 0.5), 0, 3)

        elif elem_type == 'neural_network':
            layers = elem_data.get('layers', [3, 5, 5, 2])
            self._add_line('layers', ','.join(map(str, layers)))
            self._add_spin('width', elem_data.get('width', 40), 20, 100)
            self._add_spin('height', elem_data.get('height', 30), 15, 100)
            self._add_check('show_connections', elem_data.get('show_connections', True))

        elif elem_type == 'similarity_meter':
            self._add_spin('score', elem_data.get('score', 75), 0, 100)
            self._add_spin('radius', elem_data.get('radius', 8), 3, 20)
            self._add_line('label', elem_data.get('label', 'Similarity'))

        elif elem_type == 'progress_bar':
            self._add_spin('current', elem_data.get('current', 5), 0, 1000)
            self._add_spin('total', elem_data.get('total', 10), 1, 1000)
            self._add_spin('width', elem_data.get('width', 30), 10, 100)
            self._add_line('label', elem_data.get('label', 'Progress'))

        elif elem_type == 'parameter_slider':
            self._add_line('label', elem_data.get('label', 'Parameter'))
            self._add_float('current_value', elem_data.get('current_value', 0.5), -100, 100)
            self._add_float('min_value', elem_data.get('min_value', 0), -100, 100)
            self._add_float('max_value', elem_data.get('max_value', 1), -100, 100)
            self._add_spin('width', elem_data.get('width', 30), 10, 100)

        elif elem_type in ('scatter_3d', 'vector_3d'):
            self._add_float('camera_elev', elem_data.get('camera_elev', 20), -90, 90)
            self._add_float('camera_azim', elem_data.get('camera_azim', 45), 0, 360)
            self._add_check('rotate_camera', elem_data.get('rotate_camera', False))
            list_name = 'points' if elem_type == 'scatter_3d' else 'vectors'
            self._add_list_button(list_name, elem_data.get(list_name, []), 'dict')

        elif elem_type == 'attention_heatmap':
            self._add_list_button('tokens_x', elem_data.get('tokens_x', []), 'string')
            self._add_spin('width', elem_data.get('width', 30), 10, 100)
            self._add_spin('height', elem_data.get('height', 30), 10, 100)
            self._add_check('show_values', elem_data.get('show_values', True))

        elif elem_type == 'token_flow':
            self._add_line('input_text', elem_data.get('input_text', 'Hello world'))
            self._add_spin('width', elem_data.get('width', 45), 20, 100)
            self._add_spin('height', elem_data.get('height', 20), 10, 100)
            self._add_check('show_embeddings', elem_data.get('show_embeddings', True))

        elif elem_type == 'weight_comparison':
            self._add_list_button('before_weights', elem_data.get('before_weights', []), 'float')
            self._add_list_button('after_weights', elem_data.get('after_weights', []), 'float')

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

    def _edit_list(self, name, item_type):
        if self.current_elem is None:
            return
        items = self.current_elem.get(name, [])
        dialog = ListEditorDialog(f"Edit {name}", items, item_type, self)
        if dialog.exec() == QDialog.Accepted:
            new_items = dialog.get_items()
            self._emit(name, new_items)
            self.widgets[name].setText(f"Edit ({len(new_items)} items)")


class StepNavigator(QWidget):
    """Bottom bar for navigating between steps."""

    step_changed = Signal(int)
    step_added = Signal()
    step_removed = Signal()
    step_renamed = Signal(int, str)

    def __init__(self):
        super().__init__()
        self.setFixedHeight(50)
        self.setStyleSheet(f"background-color: {COLORS['panel']};")
        self.current_step = 0
        self.total_steps = 1
        self.step_names = ['Step 1']

        layout = QHBoxLayout(self)
        layout.setContentsMargins(16, 8, 16, 8)

        btn_style = f"""
            QPushButton {{
                background-color: {COLORS['bg_light']};
                color: {COLORS['text']};
                border: 1px solid {COLORS['dim']};
                border-radius: 4px;
                font-weight: bold;
                font-size: 14px;
            }}
            QPushButton:hover {{
                background-color: {COLORS['primary']};
            }}
        """

        # Previous button
        self.prev_btn = QPushButton("◀")
        self.prev_btn.setFixedSize(40, 32)
        self.prev_btn.setStyleSheet(btn_style)
        self.prev_btn.clicked.connect(self._prev_step)
        layout.addWidget(self.prev_btn)

        # Add step
        self.add_btn = QPushButton("+")
        self.add_btn.setFixedSize(40, 32)
        self.add_btn.setStyleSheet(btn_style)
        self.add_btn.clicked.connect(self.step_added.emit)
        layout.addWidget(self.add_btn)

        # Remove step
        self.remove_btn = QPushButton("−")
        self.remove_btn.setFixedSize(40, 32)
        self.remove_btn.setStyleSheet(btn_style)
        self.remove_btn.clicked.connect(self.step_removed.emit)
        layout.addWidget(self.remove_btn)

        layout.addStretch()

        # Step label (clickable to rename)
        self.step_label = QPushButton("Step 1/1")
        self.step_label.setFont(QFont('sans-serif', 12, QFont.Bold))
        self.step_label.setStyleSheet(f"""
            QPushButton {{
                color: {COLORS['primary']};
                background: transparent;
                border: none;
                padding: 4px 12px;
            }}
            QPushButton:hover {{
                background-color: {COLORS['bg_light']};
                border-radius: 4px;
            }}
        """)
        self.step_label.clicked.connect(self._rename_step)
        layout.addWidget(self.step_label)

        layout.addStretch()

        # Next button
        self.next_btn = QPushButton("▶")
        self.next_btn.setFixedSize(40, 32)
        self.next_btn.setStyleSheet(btn_style)
        self.next_btn.clicked.connect(self._next_step)
        layout.addWidget(self.next_btn)

    def _prev_step(self):
        if self.current_step > 0:
            self.current_step -= 1
            self.step_changed.emit(self.current_step)
            self._update_label()

    def _next_step(self):
        if self.current_step < self.total_steps - 1:
            self.current_step += 1
            self.step_changed.emit(self.current_step)
            self._update_label()

    def _rename_step(self):
        name, ok = QInputDialog.getText(
            self, "Rename Step", "Step name:",
            QLineEdit.Normal, self.step_names[self.current_step]
        )
        if ok and name:
            self.step_names[self.current_step] = name
            self.step_renamed.emit(self.current_step, name)
            self._update_label()

    def set_steps(self, current: int, total: int, names: List[str]):
        self.current_step = current
        self.total_steps = total
        self.step_names = names
        self._update_label()

    def _update_label(self):
        name = self.step_names[self.current_step] if self.current_step < len(self.step_names) else f'Step {self.current_step + 1}'
        self.step_label.setText(f"{name} ({self.current_step + 1}/{self.total_steps})")


class PreviewWindow(QWidget):
    """Animation preview window using matplotlib."""

    def __init__(self, step_data: Dict, step_name: str, parent=None):
        super().__init__(parent, Qt.Window)  # Make it a separate window
        self.step_data = step_data
        self.step_name = step_name
        self.progress = 0.0
        self.playing = False
        self.loop = True

        self.setWindowTitle(f"Preview: {step_name}")
        self.setMinimumSize(900, 700)
        self.setStyleSheet(f"background-color: {COLORS['bg']};")

        # Enable keyboard focus
        self.setFocusPolicy(Qt.StrongFocus)

        self._setup_ui()
        self._setup_timer()
        self._render()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Matplotlib figure
        self.figure = Figure(figsize=(10, 7), facecolor=COLORS['bg'])
        self.canvas = FigureCanvas(self.figure)
        self.ax = self.figure.add_subplot(111)
        layout.addWidget(self.canvas, stretch=1)

        # Controls bar
        controls = QWidget()
        controls.setFixedHeight(60)
        controls.setStyleSheet(f"background-color: {COLORS['panel']};")
        ctrl_layout = QHBoxLayout(controls)
        ctrl_layout.setContentsMargins(16, 8, 16, 8)

        btn_style = f"""
            QPushButton {{
                background-color: {COLORS['bg_light']};
                color: {COLORS['text']};
                border: 1px solid {COLORS['dim']};
                border-radius: 4px;
                font-size: 16px;
                font-weight: bold;
            }}
            QPushButton:hover {{ background-color: {COLORS['primary']}; }}
            QPushButton:checked {{ background-color: {COLORS['accent']}; }}
        """

        # Play/Pause
        self.play_btn = QPushButton("▶")
        self.play_btn.setFixedSize(50, 40)
        self.play_btn.setStyleSheet(btn_style)
        self.play_btn.clicked.connect(self._toggle_play)
        ctrl_layout.addWidget(self.play_btn)

        # Reset
        self.reset_btn = QPushButton("⟲")
        self.reset_btn.setFixedSize(50, 40)
        self.reset_btn.setStyleSheet(btn_style)
        self.reset_btn.clicked.connect(self._reset)
        ctrl_layout.addWidget(self.reset_btn)

        ctrl_layout.addSpacing(16)

        # Progress slider
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(0, 1000)
        self.slider.setValue(0)
        self.slider.setStyleSheet(f"""
            QSlider::groove:horizontal {{
                background: {COLORS['bg_light']};
                height: 8px;
                border-radius: 4px;
            }}
            QSlider::handle:horizontal {{
                background: {COLORS['primary']};
                width: 18px;
                margin: -5px 0;
                border-radius: 9px;
            }}
            QSlider::sub-page:horizontal {{
                background: {COLORS['primary']};
                border-radius: 4px;
            }}
        """)
        self.slider.valueChanged.connect(self._on_slider_change)
        self.slider.sliderPressed.connect(lambda: setattr(self, 'playing', False))
        ctrl_layout.addWidget(self.slider, stretch=1)

        ctrl_layout.addSpacing(16)

        # Progress label
        self.progress_label = QLabel("0%")
        self.progress_label.setFixedWidth(50)
        self.progress_label.setStyleSheet(f"color: {COLORS['text']}; font-size: 14px; font-weight: bold;")
        ctrl_layout.addWidget(self.progress_label)

        ctrl_layout.addSpacing(16)

        # Loop toggle
        self.loop_btn = QPushButton("🔁")
        self.loop_btn.setFixedSize(50, 40)
        self.loop_btn.setCheckable(True)
        self.loop_btn.setChecked(True)
        self.loop_btn.setStyleSheet(btn_style)
        self.loop_btn.toggled.connect(lambda v: setattr(self, 'loop', v))
        ctrl_layout.addWidget(self.loop_btn)

        layout.addWidget(controls)

    def _setup_timer(self):
        self.timer = QTimer(self)
        self.timer.timeout.connect(self._tick)
        self.timer.setInterval(33)  # ~30fps

    def _toggle_play(self):
        self.playing = not self.playing
        self.play_btn.setText("⏸" if self.playing else "▶")
        if self.playing:
            self.timer.start()
        else:
            self.timer.stop()

    def _reset(self):
        self.progress = 0.0
        self.slider.setValue(0)
        self._render()

    def _on_slider_change(self, value):
        self.progress = value / 1000.0
        self.progress_label.setText(f"{int(self.progress * 100)}%")
        self._render()

    def _tick(self):
        self.progress += 0.015
        if self.progress >= 1.0:
            if self.loop:
                self.progress = 0.0
            else:
                self.progress = 1.0
                self.playing = False
                self.play_btn.setText("▶")
                self.timer.stop()

        self.slider.blockSignals(True)
        self.slider.setValue(int(self.progress * 1000))
        self.slider.blockSignals(False)
        self.progress_label.setText(f"{int(self.progress * 100)}%")
        self._render()

    def _render(self):
        """Render the current frame."""
        self.ax.clear()
        self.ax.set_facecolor(COLORS['bg'])
        self.ax.set_xlim(0, 100)
        self.ax.set_ylim(0, 100)
        self.ax.set_aspect('equal')
        self.ax.axis('off')

        # Title
        title = self.step_data.get('title', self.step_name)
        if title:
            self.ax.text(50, 96, title, fontsize=18, fontweight='bold',
                        ha='center', va='top', color=COLORS['primary'])

        # Render elements
        for elem in self.step_data.get('elements', []):
            self._render_element(elem, self.progress)

        # Draw phase markers at bottom
        self._draw_phase_markers()

        self.canvas.draw_idle()

    def _draw_phase_markers(self):
        """Draw phase indicator at bottom."""
        phases = [('imm', 0.0), ('early', 0.2), ('mid', 0.4), ('late', 0.6), ('final', 0.8)]
        for name, start in phases:
            x = 10 + start * 80
            color = COLORS['accent'] if self.progress >= start else COLORS['dim']
            self.ax.plot([x, x], [2, 5], color=color, linewidth=2)
            self.ax.text(x, 1, name, fontsize=7, ha='center', color=color)
        # Progress line
        self.ax.axhline(y=3.5, xmin=0.1, xmax=0.1 + 0.8 * self.progress,
                       color=COLORS['primary'], linewidth=3)

    def _stagger_alpha(self, base_alpha, index, total_items, stagger=True):
        """Calculate alpha for staggered item reveal.

        With stagger=True, items appear sequentially during the animation.
        Duration affects how fast the sequence plays out.
        """
        if not stagger or total_items <= 1:
            return base_alpha

        # Each item gets an equal portion of the animation
        # Duration is already factored into base_alpha's timing
        item_portion = 1.0 / total_items
        item_start = index * item_portion
        item_end = item_start + item_portion * 1.5  # Overlap for smooth transition

        if base_alpha < item_start:
            return 0.0
        elif base_alpha >= item_end:
            return 1.0
        else:
            # Fade in during this item's portion
            t = (base_alpha - item_start) / (item_end - item_start)
            return min(1.0, max(0.0, t))

    def _apply_easing(self, t, easing):
        """Apply easing function."""
        if easing == 'linear':
            return t
        elif easing == 'ease_in':
            return t * t
        elif easing == 'ease_out':
            return 1 - (1 - t) ** 2
        elif easing == 'ease_in_out':
            return 3 * t * t - 2 * t * t * t
        elif easing == 'ease_in_cubic':
            return t * t * t
        elif easing == 'ease_out_cubic':
            return 1 - (1 - t) ** 3
        elif easing == 'elastic_out':
            if t == 0 or t == 1:
                return t
            return math.pow(2, -10 * t) * math.sin((t - 0.075) * (2 * math.pi) / 0.3) + 1
        elif easing == 'bounce_out':
            if t < 1/2.75:
                return 7.5625 * t * t
            elif t < 2/2.75:
                t -= 1.5/2.75
                return 7.5625 * t * t + 0.75
            elif t < 2.5/2.75:
                t -= 2.25/2.75
                return 7.5625 * t * t + 0.9375
            else:
                t -= 2.625/2.75
                return 7.5625 * t * t + 0.984375
        return t

    def _render_element(self, elem, progress):
        """Render a single element with animation."""
        phase = elem.get('animation_phase', 'early')
        phase_ranges = {
            'immediate': (0.0, 0.2),
            'early': (0.2, 0.4),
            'middle': (0.4, 0.6),
            'late': (0.6, 0.8),
            'final': (0.8, 1.0)
        }
        base_start, base_end = phase_ranges.get(phase, (0.2, 0.4))

        # Apply timing modifiers
        duration = elem.get('duration', 1.0)
        delay = elem.get('delay', 0.0)
        speed = elem.get('speed', 1.0)

        # Delay shifts start forward
        start = base_start + delay * 0.05

        # Duration scales how long the fade-in takes
        # duration=1.0 means standard 20% of animation
        # duration=2.0 means 40% of animation (slower fade)
        # duration=0.5 means 10% of animation (faster fade)
        phase_length = (base_end - base_start) * duration
        end = min(1.0, start + phase_length)

        # Calculate normalized progress within this element's phase (0 to 1)
        if progress < start:
            elem_progress = 0.0
        elif progress >= end:
            elem_progress = 1.0
        else:
            t = (progress - start) / max(end - start, 0.01)
            easing = elem.get('easing', 'ease_in_out')
            elem_progress = self._apply_easing(t, easing)

        # Store for use in staggered animations
        self._elem_progress = elem_progress
        self._phase_length = phase_length
        self._duration = duration

        # Alpha for simple fade-in (most elements just use this directly)
        alpha = elem_progress

        if alpha <= 0:
            return

        elem_type = elem.get('type', 'text')
        pos = elem.get('position', {'x': 50, 'y': 50})
        x, y = pos['x'], pos['y']

        # Render based on type
        if elem_type == 'text':
            content = elem.get('content', 'Text')
            self.ax.text(x, y, content, fontsize=14, ha='center', va='center',
                        color=COLORS['text'], alpha=alpha)

        elif elem_type == 'typewriter_text':
            content = elem.get('content', 'Typing...')
            type_progress = min(1.0, alpha * speed)
            visible_chars = int(len(content) * type_progress)
            display = content[:visible_chars]
            if visible_chars < len(content):
                display += '|'
            self.ax.text(x, y, display, fontsize=14, ha='center', va='center',
                        color=COLORS['text'], alpha=min(1.0, alpha * 2), family='monospace')

        elif elem_type == 'box':
            w, h = elem.get('width', 20), elem.get('height', 12)
            rect = FancyBboxPatch((x - w/2, y - h/2), w, h,
                                  boxstyle="round,pad=0.3",
                                  facecolor=COLORS['bg_light'],
                                  edgecolor=COLORS['primary'],
                                  linewidth=2, alpha=alpha)
            self.ax.add_patch(rect)
            if elem.get('title'):
                self.ax.text(x, y + h/4, elem['title'], fontsize=11,
                            fontweight='bold', ha='center', color=COLORS['primary'], alpha=alpha)

        elif elem_type == 'similarity_meter':
            r = elem.get('radius', 8)
            score = elem.get('score', 75)
            current_score = score * alpha
            # Background
            wedge_bg = Wedge((x, y), r, 0, 180, facecolor=COLORS['bg_light'],
                            edgecolor=COLORS['dim'], linewidth=2)
            self.ax.add_patch(wedge_bg)
            # Fill
            fill_angle = 180 * (1 - current_score / 100)
            color = COLORS['success'] if current_score > 66 else (COLORS['accent'] if current_score > 33 else COLORS['warning'])
            wedge_fill = Wedge((x, y), r, fill_angle, 180, facecolor=color, edgecolor='none')
            self.ax.add_patch(wedge_fill)
            self.ax.text(x, y - 2, f"{int(current_score)}%", fontsize=12,
                        fontweight='bold', ha='center', va='center', color='white')

        elif elem_type == 'progress_bar':
            w = elem.get('width', 30)
            current = elem.get('current', 5)
            total = elem.get('total', 10)
            pct = (current / max(total, 1)) * alpha
            # Background
            self.ax.add_patch(FancyBboxPatch((x - w/2, y - 2), w, 4,
                                            boxstyle="round,pad=0.1",
                                            facecolor=COLORS['bg_light'],
                                            edgecolor=COLORS['dim'], linewidth=1.5, alpha=alpha))
            # Fill
            self.ax.add_patch(FancyBboxPatch((x - w/2, y - 2), w * pct, 4,
                                            boxstyle="round,pad=0.1",
                                            facecolor=COLORS['success'], edgecolor='none', alpha=alpha))

        elif elem_type == 'neural_network':
            w, h = elem.get('width', 40), elem.get('height', 30)
            layers = elem.get('layers', [3, 5, 5, 2])
            sp = w / (len(layers) + 1)
            for li, n in enumerate(layers):
                layer_alpha = self._stagger_alpha(alpha, li, len(layers), True)
                if layer_alpha <= 0:
                    continue
                lx = x - w/2 + (li + 1) * sp
                ns = h / (n + 1)
                for ni in range(n):
                    ny = y - h/2 + (ni + 1) * ns
                    circle = Circle((lx, ny), 1.5, facecolor=COLORS['primary'],
                                   edgecolor='white', linewidth=0.5, alpha=layer_alpha)
                    self.ax.add_patch(circle)

        elif elem_type == 'particle_flow':
            start_pos = elem.get('start', {'x': 20, 'y': 50})
            end_pos = elem.get('end', {'x': 80, 'y': 50})
            n = elem.get('num_particles', 20)
            spread = elem.get('spread', 0.5)
            flow_alpha = min(1.0, alpha * speed)
            for i in range(n):
                t_pos = ((i / n) + flow_alpha * 2) % 1.0
                px = start_pos['x'] + (end_pos['x'] - start_pos['x']) * t_pos
                py = start_pos['y'] + (end_pos['y'] - start_pos['y']) * t_pos
                py += np.sin(i * 1.5) * spread * 5
                size = 0.4 + np.sin(t_pos * np.pi) * 0.3
                p_alpha = max(0, 0.3 + np.sin(t_pos * np.pi) * 0.7) * alpha
                circle = Circle((px, py), size, facecolor=COLORS['accent'],
                               edgecolor='none', alpha=p_alpha)
                self.ax.add_patch(circle)

        elif elem_type in ('arrow', 'arc_arrow'):
            start_pos = elem.get('start', {'x': 30, 'y': 50})
            end_pos = elem.get('end', {'x': 70, 'y': 50})
            # Animate the endpoint
            ex = start_pos['x'] + (end_pos['x'] - start_pos['x']) * alpha
            ey = start_pos['y'] + (end_pos['y'] - start_pos['y']) * alpha
            style = 'arc3,rad=0.2' if elem_type == 'arc_arrow' else None
            self.ax.annotate('', xy=(ex, ey), xytext=(start_pos['x'], start_pos['y']),
                           arrowprops=dict(arrowstyle='-|>', lw=2,
                                          color=COLORS['primary'],
                                          connectionstyle=style))

        elif elem_type == 'comparison':
            w, h = elem.get('width', 40), elem.get('height', 20)
            # Left box
            self.ax.add_patch(FancyBboxPatch((x - w/2, y - h/2), w/2 - 2, h,
                                            boxstyle="round,pad=0.2",
                                            facecolor=COLORS['bg_light'],
                                            edgecolor=COLORS['warning'],
                                            linewidth=2, alpha=alpha))
            # Right box
            self.ax.add_patch(FancyBboxPatch((x + 2, y - h/2), w/2 - 2, h,
                                            boxstyle="round,pad=0.2",
                                            facecolor=COLORS['bg_light'],
                                            edgecolor=COLORS['success'],
                                            linewidth=2, alpha=alpha))
            self.ax.text(x - w/4, y, elem.get('left_title', 'Before')[:10],
                        fontsize=10, fontweight='bold', ha='center', color=COLORS['warning'], alpha=alpha)
            self.ax.text(x + w/4, y, elem.get('right_title', 'After')[:10],
                        fontsize=10, fontweight='bold', ha='center', color=COLORS['success'], alpha=alpha)

        elif elem_type == 'bullet_list':
            items = elem.get('items', [])[:6]
            stagger = elem.get('stagger', True)
            for j, item in enumerate(items):
                item_alpha = self._stagger_alpha(alpha, j, len(items), stagger)
                if item_alpha > 0:
                    self.ax.text(x - 12, y + 8 - j * 5, f"• {item}",
                               fontsize=10, ha='left', color=COLORS['text'], alpha=item_alpha)

        elif elem_type == 'checklist':
            items = elem.get('items', [])[:5]
            stagger = elem.get('stagger', True)
            for j, item in enumerate(items):
                item_alpha = self._stagger_alpha(alpha, j, len(items), stagger)
                if item_alpha > 0:
                    iy = y + 6 - j * 5
                    self.ax.add_patch(Rectangle((x - 12, iy - 1.5), 3, 3,
                                               facecolor=COLORS['success'],
                                               edgecolor=COLORS['success'],
                                               linewidth=1, alpha=item_alpha))
                    self.ax.text(x - 7, iy, item[:20], fontsize=10, ha='left',
                               color=COLORS['text'], alpha=item_alpha)

        elif elem_type == 'code_block':
            w, h = elem.get('width', 30), elem.get('height', 15)
            self.ax.add_patch(FancyBboxPatch((x - w/2, y - h/2), w, h,
                                            boxstyle="round,pad=0.3",
                                            facecolor='#0d1117',
                                            edgecolor=COLORS['dim'],
                                            linewidth=1.5, alpha=alpha))
            code = elem.get('code', '# code')
            self.ax.text(x - w/2 + 2, y + h/4, code[:40],
                        fontsize=9, ha='left', color=COLORS['secondary'],
                        alpha=alpha, family='monospace')

        elif elem_type == 'parameter_slider':
            w = elem.get('width', 30)
            val = elem.get('current_value', 0.5)
            min_v = elem.get('min_value', 0)
            max_v = elem.get('max_value', 1)
            pct = (val - min_v) / (max_v - min_v) if max_v != min_v else 0.5
            # Label
            self.ax.text(x, y + 5, elem.get('label', 'Param')[:15], fontsize=10,
                        fontweight='bold', ha='center', color=COLORS['text'], alpha=alpha)
            # Track
            self.ax.add_patch(Rectangle((x - w/2, y - 1), w, 2,
                                       facecolor='#333', edgecolor='#555',
                                       linewidth=0.5, alpha=alpha))
            # Fill
            self.ax.add_patch(Rectangle((x - w/2, y - 1), w * pct * alpha, 2,
                                       facecolor=COLORS['accent'], alpha=alpha))
            # Handle
            hx = x - w/2 + w * pct * alpha
            self.ax.add_patch(Circle((hx, y), 1.5, facecolor='white',
                                    edgecolor=COLORS['accent'], linewidth=1.5, alpha=alpha))

        elif elem_type == 'attention_heatmap':
            w, h = elem.get('width', 30), elem.get('height', 30)
            tokens_x = elem.get('tokens_x', ['A', 'B', 'C'])[:8]
            tokens_y = elem.get('tokens_y', tokens_x)[:8]
            title = elem.get('title', '')
            n_x, n_y = len(tokens_x), len(tokens_y)

            # Reserve space for title and labels
            grid_w = w * 0.8
            grid_h = h * 0.8
            grid_x = x - grid_w/2 + 3  # Offset for Y labels
            grid_y = y - grid_h/2
            cell_w = grid_w / max(n_x, 1)
            cell_h = grid_h / max(n_y, 1)

            # Title
            if title:
                self.ax.text(x, y + h/2 + 3, title,
                            fontsize=12, fontweight='bold', ha='center',
                            color=COLORS['text'], alpha=alpha)

            # Draw cells with animated weights
            np.random.seed(42)  # Consistent random weights
            for i in range(n_y):
                for j in range(n_x):
                    cell_idx = i * n_x + j
                    stagger = elem.get('stagger', True)
                    cell_alpha = self._stagger_alpha(alpha, cell_idx, n_x * n_y, stagger)

                    if cell_alpha > 0:
                        cx = grid_x + j * cell_w
                        cy = grid_y + (n_y - 1 - i) * cell_h  # Flip Y so first token is at top

                        # Generate attention weight - diagonal stronger (self-attention)
                        base_weight = np.random.rand() * 0.5
                        if i == j:  # Diagonal - self attention
                            weight = 0.7 + np.random.rand() * 0.3
                        elif abs(i - j) == 1:  # Adjacent
                            weight = 0.3 + np.random.rand() * 0.4
                        else:
                            weight = base_weight

                        # Animate the weight reveal
                        display_weight = weight * cell_alpha

                        self.ax.add_patch(Rectangle((cx + 0.3, cy + 0.3),
                                                   cell_w - 0.6, cell_h - 0.6,
                                                   facecolor=COLORS['accent'],
                                                   edgecolor=COLORS['bg_light'],
                                                   linewidth=0.5,
                                                   alpha=display_weight))

                        # Show weight value if show_values is true
                        if elem.get('show_values', False) and cell_alpha > 0.5:
                            self.ax.text(cx + cell_w/2, cy + cell_h/2, f'{weight:.1f}',
                                        fontsize=6, ha='center', va='center',
                                        color='white', alpha=cell_alpha)

            # X-axis token labels (top)
            for j, tok in enumerate(tokens_x):
                self.ax.text(grid_x + j * cell_w + cell_w/2, grid_y + grid_h + 1.5,
                            tok[:6], fontsize=8, ha='center', va='bottom',
                            color=COLORS['text'], alpha=alpha, rotation=0)

            # Y-axis token labels (left)
            for i, tok in enumerate(tokens_y):
                self.ax.text(grid_x - 1.5, grid_y + (n_y - 1 - i) * cell_h + cell_h/2,
                            tok[:6], fontsize=8, ha='right', va='center',
                            color=COLORS['text'], alpha=alpha)

        elif elem_type == 'token_flow':
            w, h = elem.get('width', 45), elem.get('height', 20)
            input_text = elem.get('input_text', 'Hello world')
            tokens = input_text.split()[:5]
            # Input box
            self.ax.add_patch(FancyBboxPatch((x - w/2, y - h/4), w * 0.25, h/2,
                                            boxstyle="round,pad=0.2",
                                            facecolor='#0d1117',
                                            edgecolor=COLORS['dim'],
                                            linewidth=1, alpha=alpha))
            self.ax.text(x - w/2 + w * 0.125, y, input_text[:8],
                        fontsize=8, ha='center', color=COLORS['text'], alpha=alpha)
            # Tokens with staggered reveal
            for i, tok in enumerate(tokens):
                tok_alpha = self._stagger_alpha(alpha, i, len(tokens), True)
                if tok_alpha > 0:
                    tx = x - w/4 + 3 + i * 8
                    self.ax.add_patch(FancyBboxPatch((tx - 3, y - 3), 6, 6,
                                                    boxstyle="round,pad=0.1",
                                                    facecolor=COLORS['bg_light'],
                                                    edgecolor=COLORS['accent'],
                                                    linewidth=1, alpha=tok_alpha))
                    self.ax.text(tx, y, tok[:5], fontsize=7, ha='center',
                                color=COLORS['accent'], alpha=tok_alpha)

        elif elem_type == 'flow':
            w = elem.get('width', 50)
            steps = elem.get('steps', [{'title': 'Step 1'}, {'title': 'Step 2'}])[:6]
            if not steps:
                steps = [{'title': 'Step'}]
            step_w = w / len(steps) - 3
            step_h = 12
            default_colors = [COLORS['warning'], COLORS['primary'], COLORS['success'], COLORS['accent']]
            stagger = elem.get('stagger', True)

            for i, step in enumerate(steps):
                step_alpha = self._stagger_alpha(alpha, i, len(steps), stagger)

                if step_alpha > 0:
                    sx = x - w/2 + i * (step_w + 3) + step_w/2
                    color = step.get('color', default_colors[i % len(default_colors)])
                    if isinstance(color, str) and color in COLORS:
                        color = COLORS[color]

                    # Step box
                    self.ax.add_patch(FancyBboxPatch((sx - step_w/2, y - step_h/2), step_w, step_h,
                                                    boxstyle="round,pad=0.3",
                                                    facecolor=COLORS['bg_light'],
                                                    edgecolor=color,
                                                    linewidth=2, alpha=step_alpha))

                    # Title (use 'title' or fallback to 'label')
                    title = step.get('title', step.get('label', f'Step {i+1}'))
                    self.ax.text(sx, y + 1, title[:12],
                                fontsize=9, fontweight='bold', ha='center', va='center',
                                color=color, alpha=step_alpha)

                    # Subtitle if present
                    subtitle = step.get('subtitle', '')
                    if subtitle:
                        self.ax.text(sx, y - 3, subtitle[:15],
                                    fontsize=7, ha='center', va='center',
                                    color=COLORS['dim'], alpha=step_alpha * 0.8)

                    # Arrow to next step
                    if i < len(steps) - 1:
                        arrow_x = sx + step_w/2 + 0.5
                        self.ax.annotate('', xy=(arrow_x + 2, y), xytext=(arrow_x, y),
                                       arrowprops=dict(arrowstyle='->', lw=1.5,
                                                      color=COLORS['dim']),
                                       alpha=step_alpha * 0.7)

        elif elem_type == 'timeline':
            w = elem.get('width', 50)
            events = elem.get('events', [{'date': '2023', 'title': 'Event'}])[:5]
            self.ax.plot([x - w/2, x + w/2], [y, y], color=COLORS['dim'], lw=2, alpha=alpha)
            ev_spacing = w / max(len(events), 1)
            stagger = elem.get('stagger', True)
            for i, ev in enumerate(events):
                ev_alpha = self._stagger_alpha(alpha, i, len(events), stagger)
                if ev_alpha > 0:
                    ex = x - w/2 + (i + 0.5) * ev_spacing
                    self.ax.add_patch(Circle((ex, y), 1.5, facecolor=COLORS['primary'],
                                            edgecolor='white', linewidth=1, alpha=ev_alpha))
                    self.ax.text(ex, y + 4, ev.get('title', '')[:10],
                                fontsize=7, ha='center', color=COLORS['text'], alpha=ev_alpha)
                    self.ax.text(ex, y - 4, ev.get('date', '')[:6],
                                fontsize=6, ha='center', color=COLORS['dim'], alpha=ev_alpha)

        elif elem_type == 'grid':
            w, h = elem.get('width', 35), elem.get('height', 25)
            cols, rows = elem.get('columns', 2), elem.get('rows', 2)
            items = elem.get('items', [])
            cell_w = elem.get('cell_width', w / cols - 2)
            cell_h = elem.get('cell_height', h / rows - 2)
            stagger = elem.get('stagger', True)

            idx = 0
            total_cells = cols * rows
            for r in range(rows):
                for c in range(cols):
                    cell_alpha = self._stagger_alpha(alpha, idx, total_cells, stagger)

                    if cell_alpha > 0:
                        cx = x - w/2 + c * (cell_w + 2) + cell_w/2 + 1
                        cy = y + h/2 - r * (cell_h + 2) - cell_h/2 - 1

                        self.ax.add_patch(FancyBboxPatch((cx - cell_w/2, cy - cell_h/2),
                                                        cell_w, cell_h,
                                                        boxstyle="round,pad=0.2",
                                                        facecolor=COLORS['bg_light'],
                                                        edgecolor=COLORS['primary'],
                                                        linewidth=1.5, alpha=cell_alpha))
                        if idx < len(items):
                            item = items[idx]
                            # Title
                            self.ax.text(cx, cy + 2, item.get('title', '')[:12],
                                        fontsize=8, fontweight='bold', ha='center',
                                        color=COLORS['text'], alpha=cell_alpha)
                            # Description if present
                            desc = item.get('description', '')
                            if desc:
                                self.ax.text(cx, cy - 2, desc[:12],
                                            fontsize=7, ha='center',
                                            color=COLORS['dim'], alpha=cell_alpha * 0.8)
                    idx += 1

        elif elem_type == 'model_comparison':
            w, h = elem.get('width', 45), elem.get('height', 30)
            models = elem.get('models', [{'name': 'Model A'}, {'name': 'Model B'}])[:4]
            comparison_rows = elem.get('comparison_rows', [])
            n_models = len(models)
            col_w = w / (n_models + 1)  # +1 for label column
            n_rows = len(comparison_rows)
            row_h = h / (n_rows + 1.5) if n_rows > 0 else h * 0.6

            # Header row with model names
            stagger = elem.get('stagger', True)
            for i, model in enumerate(models):
                m_alpha = self._stagger_alpha(alpha, i, n_models, stagger)

                if m_alpha > 0:
                    mx = x - w/2 + (i + 1.5) * col_w
                    color_name = model.get('color', 'primary')
                    color = COLORS.get(color_name, COLORS['primary'])

                    # Model name header
                    self.ax.text(mx, y + h/2 - 3, model.get('name', f'Model {i+1}')[:10],
                                fontsize=10, fontweight='bold', ha='center', va='center',
                                color=color, alpha=m_alpha)

                    # Draw comparison row values
                    for row_idx, row_label in enumerate(comparison_rows):
                        row_alpha = self._stagger_alpha(alpha, row_idx + n_models, n_rows + n_models, stagger)
                        if row_alpha > 0:
                            ry = y + h/2 - (row_idx + 2) * row_h

                            # Row label (only for first model)
                            if i == 0:
                                self.ax.text(x - w/2 + col_w/2, ry, row_label[:10],
                                            fontsize=8, ha='center', va='center',
                                            color=COLORS['dim'], alpha=row_alpha)

                            # Get value from model data (lowercase key)
                            value = model.get(row_label.lower(), model.get(row_label, ''))
                            self.ax.text(mx, ry, str(value)[:12],
                                        fontsize=9, ha='center', va='center',
                                        color=COLORS['text'], alpha=row_alpha)

            # Draw grid lines
            if n_rows > 0:
                for row_idx in range(n_rows + 1):
                    ly = y + h/2 - (row_idx + 1.2) * row_h
                    self.ax.plot([x - w/2 + col_w * 0.3, x + w/2 - col_w * 0.3], [ly, ly],
                               color=COLORS['dim'], lw=0.5, alpha=alpha * 0.3)

        elif elem_type == 'weight_comparison':
            w, h = elem.get('width', 35), elem.get('height', 15)
            before = elem.get('before_weights', [0.3, 0.5, 0.2])[:5]
            after = elem.get('after_weights', [0.7, 0.8, 0.6])[:5]
            bar_h = h / max(len(before), 1) - 1
            stagger = elem.get('stagger', True)
            for i in range(len(before)):
                bar_alpha = self._stagger_alpha(alpha, i, len(before), stagger)
                if bar_alpha > 0:
                    by = y + h/2 - i * (bar_h + 1) - bar_h/2
                    bw = (w/2 - 2) * before[i] * alpha
                    self.ax.add_patch(Rectangle((x - w/2, by - bar_h/2), bw, bar_h,
                                               facecolor=COLORS['warning'], alpha=bar_alpha * 0.8))
                    aw = (w/2 - 2) * after[i] * alpha
                    self.ax.add_patch(Rectangle((x + 2, by - bar_h/2), aw, bar_h,
                                               facecolor=COLORS['success'], alpha=bar_alpha * 0.8))

        elif elem_type in ('scatter_3d', 'vector_3d'):
            w, h = elem.get('width', 30), elem.get('height', 25)
            self.ax.add_patch(FancyBboxPatch((x - w/2, y - h/2), w, h,
                                            boxstyle="round,pad=0.2",
                                            facecolor='#0d0d14',
                                            edgecolor=COLORS['dim'],
                                            linewidth=1.5, alpha=alpha))
            cx, cy = x, y
            self.ax.plot([cx - 8, cx + 8], [cy - 5, cy - 5], color=COLORS['warning'], lw=1.5, alpha=alpha)
            self.ax.plot([cx, cx], [cy - 5, cy + 8], color=COLORS['success'], lw=1.5, alpha=alpha)
            self.ax.plot([cx, cx - 6], [cy - 5, cy - 2], color=COLORS['primary'], lw=1.5, alpha=alpha)
            if elem_type == 'scatter_3d':
                points = [(2, 3), (-3, 4), (4, -2), (-2, -3), (0, 5)]
                for i, (px, py) in enumerate(points):
                    p_alpha = self._stagger_alpha(alpha, i, len(points), True)
                    if p_alpha > 0:
                        self.ax.add_patch(Circle((cx + px, cy + py), 1,
                                                facecolor=COLORS['accent'],
                                                edgecolor='white', linewidth=0.5, alpha=p_alpha))
            else:
                vectors = [(5, 4), (-4, 5), (3, -4)]
                colors = [COLORS['warning'], COLORS['success'], COLORS['accent']]
                for i, ((vx, vy), col) in enumerate(zip(vectors, colors)):
                    v_alpha = self._stagger_alpha(alpha, i, len(vectors), True)
                    if v_alpha > 0:
                        self.ax.annotate('', xy=(cx + vx * v_alpha, cy + vy * v_alpha), xytext=(cx, cy),
                                       arrowprops=dict(arrowstyle='->', lw=2, color=col), alpha=v_alpha)

        elif elem_type == 'stacked_boxes':
            base_width = elem.get('base_width', elem.get('width', 40))
            box_height = elem.get('box_height', 10)
            width_decrease = elem.get('width_decrease', 4)
            spacing = elem.get('spacing', 12)
            items = elem.get('items', [{'title': 'Layer 1'}, {'title': 'Layer 2'}])[:6]
            stagger = elem.get('stagger', True)

            for i, item in enumerate(items):
                b_alpha = self._stagger_alpha(alpha, i, len(items), stagger)

                if b_alpha > 0:
                    # Each box gets progressively smaller
                    box_w = base_width - (i * width_decrease)
                    by = y + (len(items)/2 - i - 0.5) * spacing

                    # Get color from item or use default
                    color_name = item.get('color', 'primary')
                    color = COLORS.get(color_name, COLORS['primary'])

                    self.ax.add_patch(FancyBboxPatch((x - box_w/2, by - box_height/2),
                                                    box_w, box_height,
                                                    boxstyle="round,pad=0.3",
                                                    facecolor=COLORS['bg_light'],
                                                    edgecolor=color,
                                                    linewidth=2, alpha=b_alpha))

                    # Title
                    self.ax.text(x, by + 1, item.get('title', f'Layer {i+1}')[:20],
                                fontsize=9, fontweight='bold', ha='center', va='center',
                                color=color, alpha=b_alpha)

                    # Description if present
                    desc = item.get('description', '')
                    if desc:
                        self.ax.text(x, by - 2.5, desc[:25],
                                    fontsize=7, ha='center', va='center',
                                    color=COLORS['dim'], alpha=b_alpha * 0.8)

        elif elem_type == 'conversation':
            w, h = elem.get('width', 35), elem.get('height', 25)
            messages = elem.get('messages', [{'role': 'user', 'content': 'Hello'},
                                             {'role': 'assistant', 'content': 'Hi!'}])[:5]
            if not messages:
                messages = [{'role': 'user', 'content': 'Sample message'}]

            stagger = elem.get('stagger', True)
            msg_h = min(h / len(messages) - 2, 10)
            user_color = elem.get('user_color', COLORS['primary'])
            assistant_color = elem.get('assistant_color', COLORS['secondary'])

            for i, msg in enumerate(messages):
                m_alpha = self._stagger_alpha(alpha, i, len(messages), stagger)

                if m_alpha > 0:
                    my = y + h/2 - i * (msg_h + 2) - msg_h/2 - 1
                    role = msg.get('role', 'user')
                    is_user = role == 'user' or role == 'Input'
                    msg_w = w * 0.7
                    mx = x - (w/2 - msg_w/2 - 2) if is_user else x + (w/2 - msg_w/2 - 2)
                    color = user_color if is_user else assistant_color

                    # Message bubble
                    self.ax.add_patch(FancyBboxPatch((mx - msg_w/2, my - msg_h/2),
                                                    msg_w, msg_h,
                                                    boxstyle="round,pad=0.3",
                                                    facecolor=color,
                                                    edgecolor='none',
                                                    alpha=m_alpha * 0.4))

                    # Role/name label
                    name = msg.get('name', role.capitalize())
                    self.ax.text(mx - msg_w/2 + 2, my + msg_h/2 - 1.5, name[:10],
                                fontsize=6, fontweight='bold', ha='left',
                                color=color, alpha=m_alpha)

                    # Content
                    content = msg.get('content', '')
                    self.ax.text(mx, my - 1, content[:35],
                                fontsize=8, ha='center', va='center',
                                color=COLORS['text'], alpha=m_alpha)

        elif elem_type == 'code_execution':
            w, h = elem.get('width', 30), elem.get('height', 20)
            # Code section
            self.ax.add_patch(FancyBboxPatch((x - w/2, y), w, h * 0.5,
                                            boxstyle="round,pad=0.2",
                                            facecolor='#0d1117',
                                            edgecolor=COLORS['dim'],
                                            linewidth=1, alpha=alpha))
            code = elem.get('code', '>>> code')
            self.ax.text(x - w/2 + 2, y + h * 0.35, code[:30],
                        fontsize=8, ha='left', color=COLORS['secondary'],
                        alpha=alpha, family='monospace')
            # Output section (appears after code)
            out_alpha = max(0, alpha * 2 - 0.5)
            if out_alpha > 0:
                self.ax.add_patch(FancyBboxPatch((x - w/2, y - h * 0.4), w, h * 0.35,
                                                boxstyle="round,pad=0.2",
                                                facecolor=COLORS['bg_light'],
                                                edgecolor=COLORS['success'],
                                                linewidth=1.5, alpha=out_alpha))
                output = elem.get('output', 'output')
                self.ax.text(x - w/2 + 2, y - h * 0.25, output[:25],
                            fontsize=8, ha='left', color=COLORS['success'],
                            alpha=out_alpha, family='monospace')

        else:
            # Generic placeholder
            w, h = elem.get('width', 15), elem.get('height', 10)
            self.ax.add_patch(FancyBboxPatch((x - w/2, y - h/2), w, h,
                                            boxstyle="round,pad=0.2",
                                            facecolor=COLORS['bg_light'],
                                            edgecolor=COLORS['dim'],
                                            linewidth=1.5, linestyle='--', alpha=alpha))
            self.ax.text(x, y, elem_type[:10], fontsize=9, ha='center',
                        color=COLORS['dim'], alpha=alpha)

    def keyPressEvent(self, event):
        """Handle keyboard shortcuts."""
        if event.key() == Qt.Key_Space:
            self._toggle_play()
        elif event.key() == Qt.Key_R:
            self._reset()
        elif event.key() in (Qt.Key_Escape, Qt.Key_Q):
            self.close()
        else:
            super().keyPressEvent(event)

    def showEvent(self, event):
        """Grab focus when shown."""
        super().showEvent(event)
        self.setFocus()
        self.activateWindow()

    def closeEvent(self, event):
        """Stop timer on close."""
        self.timer.stop()
        super().closeEvent(event)


class PresentationDesigner(QMainWindow):
    """Main application window."""

    def __init__(self, schema_path: Optional[str] = None):
        super().__init__()
        self.schema_path = schema_path
        self.schema = self._load_or_create_schema(schema_path)
        self.current_step = 0

        # Undo stack
        self.undo_stack = QUndoStack(self)
        self.undo_stack.setUndoLimit(50)

        self._setup_ui()
        self._setup_menu()
        self._connect_signals()
        self._load_step(0)

    def _load_or_create_schema(self, path: Optional[str]) -> Dict:
        if path and Path(path).exists():
            with open(path) as f:
                return json.load(f)
        return {
            'name': 'new_presentation',
            'title': 'New Presentation',
            'steps': [{'name': 'Step 1', 'title': 'Introduction', 'elements': []}]
        }

    def _setup_ui(self):
        self.setWindowTitle(f"Presentation Designer - {self.schema.get('name', 'Untitled')}")
        self.setMinimumSize(1280, 800)

        # Dark theme
        self.setStyleSheet(f"""
            QMainWindow, QWidget {{
                background-color: {COLORS['bg']};
                color: {COLORS['text']};
            }}
            QGroupBox {{
                color: {COLORS['secondary']};
                font-weight: bold;
                border: 1px solid {COLORS['dim']};
                border-radius: 4px;
                margin-top: 12px;
                padding-top: 8px;
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
            }}
            QSpinBox, QDoubleSpinBox, QLineEdit, QComboBox, QPlainTextEdit {{
                background-color: {COLORS['bg_light']};
                border: 1px solid {COLORS['dim']};
                border-radius: 4px;
                padding: 4px 8px;
                color: {COLORS['text']};
                min-height: 24px;
            }}
            QSpinBox:focus, QDoubleSpinBox:focus, QLineEdit:focus, QComboBox:focus {{
                border-color: {COLORS['primary']};
            }}
            QComboBox::drop-down {{
                border: none;
                width: 20px;
            }}
            QComboBox::down-arrow {{
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 6px solid {COLORS['text']};
                margin-right: 5px;
            }}
            QScrollBar:vertical {{
                background: {COLORS['bg_light']};
                width: 12px;
                border-radius: 6px;
            }}
            QScrollBar::handle:vertical {{
                background: {COLORS['dim']};
                border-radius: 6px;
                min-height: 20px;
            }}
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
                height: 0;
            }}
            QCheckBox::indicator {{
                width: 18px;
                height: 18px;
                border: 2px solid {COLORS['dim']};
                border-radius: 4px;
                background: {COLORS['bg_light']};
            }}
            QCheckBox::indicator:checked {{
                background: {COLORS['success']};
                border-color: {COLORS['success']};
            }}
        """)

        # Central widget
        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QVBoxLayout(central)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Content area
        content_layout = QHBoxLayout()
        content_layout.setSpacing(0)

        # Left: Element palette
        self.palette = ElementPalette()
        content_layout.addWidget(self.palette)

        # Center: Canvas
        self.canvas = CanvasView(self.undo_stack)
        content_layout.addWidget(self.canvas, stretch=1)

        # Right: Properties
        self.properties = PropertiesPanel()
        content_layout.addWidget(self.properties)

        main_layout.addLayout(content_layout, stretch=1)

        # Bottom: Step navigator
        self.navigator = StepNavigator()
        self._update_navigator()
        main_layout.addWidget(self.navigator)

        # Status bar
        self.statusBar().showMessage("Ready • Middle-click to pan • Scroll to zoom")
        self.statusBar().setStyleSheet(f"color: {COLORS['dim']}; padding: 4px;")

    def _setup_menu(self):
        menubar = self.menuBar()
        menubar.setStyleSheet(f"""
            QMenuBar {{
                background-color: {COLORS['panel']};
                color: {COLORS['text']};
                padding: 4px;
            }}
            QMenuBar::item:selected {{
                background-color: {COLORS['primary']};
            }}
            QMenu {{
                background-color: {COLORS['bg_light']};
                color: {COLORS['text']};
                border: 1px solid {COLORS['dim']};
            }}
            QMenu::item:selected {{
                background-color: {COLORS['primary']};
            }}
        """)

        # File menu
        file_menu = menubar.addMenu("&File")

        new_action = QAction("&New", self)
        new_action.setShortcut(QKeySequence.New)
        new_action.triggered.connect(self._new_presentation)
        file_menu.addAction(new_action)

        open_action = QAction("&Open...", self)
        open_action.setShortcut(QKeySequence.Open)
        open_action.triggered.connect(self._open_file)
        file_menu.addAction(open_action)

        save_action = QAction("&Save", self)
        save_action.setShortcut(QKeySequence.Save)
        save_action.triggered.connect(self._save_file)
        file_menu.addAction(save_action)

        file_menu.addSeparator()

        generate_action = QAction("&Generate Python...", self)
        generate_action.setShortcut("Ctrl+G")
        generate_action.triggered.connect(self._generate_python)
        file_menu.addAction(generate_action)

        file_menu.addSeparator()

        quit_action = QAction("&Quit", self)
        quit_action.setShortcut(QKeySequence.Quit)
        quit_action.triggered.connect(self.close)
        file_menu.addAction(quit_action)

        # Edit menu
        edit_menu = menubar.addMenu("&Edit")

        undo_action = QAction("&Undo", self)
        undo_action.setShortcut(QKeySequence.Undo)
        undo_action.triggered.connect(self.undo_stack.undo)
        edit_menu.addAction(undo_action)

        redo_action = QAction("&Redo", self)
        redo_action.setShortcut(QKeySequence.Redo)
        redo_action.triggered.connect(self.undo_stack.redo)
        edit_menu.addAction(redo_action)

        edit_menu.addSeparator()

        delete_action = QAction("&Delete Element", self)
        delete_action.setShortcut(QKeySequence.Delete)
        delete_action.triggered.connect(self._delete_selected)
        edit_menu.addAction(delete_action)

        duplicate_action = QAction("D&uplicate", self)
        duplicate_action.setShortcut("Ctrl+D")
        duplicate_action.triggered.connect(self._duplicate_selected)
        edit_menu.addAction(duplicate_action)

        # View menu
        view_menu = menubar.addMenu("&View")

        zoom_in = QAction("Zoom &In", self)
        zoom_in.setShortcut("Ctrl+=")
        zoom_in.triggered.connect(lambda: self.canvas.scale(1.15, 1.15))
        view_menu.addAction(zoom_in)

        zoom_out = QAction("Zoom &Out", self)
        zoom_out.setShortcut("Ctrl+-")
        zoom_out.triggered.connect(lambda: self.canvas.scale(1/1.15, 1/1.15))
        view_menu.addAction(zoom_out)

        zoom_reset = QAction("&Reset Zoom", self)
        zoom_reset.setShortcut("Ctrl+0")
        zoom_reset.triggered.connect(self._reset_zoom)
        view_menu.addAction(zoom_reset)

        view_menu.addSeparator()

        preview_action = QAction("&Preview Animation", self)
        preview_action.setShortcut("P")
        preview_action.triggered.connect(self._show_preview)
        view_menu.addAction(preview_action)

    def _connect_signals(self):
        self.palette.element_clicked.connect(self._add_element)
        self.canvas.element_selected.connect(self.properties.set_element)
        self.canvas.element_deselected.connect(lambda: self.properties.set_element(None))
        self.properties.property_changed.connect(self._on_property_changed)
        self.navigator.step_changed.connect(self._load_step)
        self.navigator.step_added.connect(self._add_step)
        self.navigator.step_removed.connect(self._remove_step)
        self.navigator.step_renamed.connect(self._rename_step)

    def _update_navigator(self):
        names = [s.get('name', f'Step {i+1}') for i, s in enumerate(self.schema['steps'])]
        self.navigator.set_steps(self.current_step, len(self.schema['steps']), names)

    def _load_step(self, step_idx: int):
        self.current_step = step_idx
        self.canvas.clear_elements()

        if 0 <= step_idx < len(self.schema['steps']):
            step = self.schema['steps'][step_idx]
            for elem in step.get('elements', []):
                self.canvas.add_element(elem)
            self._update_navigator()
            self.statusBar().showMessage(f"Loaded: {step.get('name', 'Untitled')}")

    def _add_element(self, elem_type: str):
        defaults = copy.deepcopy(ELEMENT_DEFAULTS.get(elem_type, {}))
        elem_data = {
            'type': elem_type,
            'position': {'x': 50, 'y': 50},
            'animation_phase': 'early',
            **defaults
        }

        step_elements = self.schema['steps'][self.current_step]['elements']
        item = self.canvas.add_element(elem_data)

        # Undo command
        cmd = AddElementCommand(self.canvas.scene_obj, step_elements, elem_data, item)
        self.undo_stack.push(cmd)

        item.setSelected(True)
        self.statusBar().showMessage(f"Added {elem_type}")

    def _on_property_changed(self, prop: str, value):
        item = self.canvas.get_selected_item()
        if not item:
            return

        if prop in ('x', 'y'):
            if 'position' not in item.elem_data:
                item.elem_data['position'] = {}
            item.elem_data['position'][prop] = value
            # Update visual position
            rect = self.canvas.scene_obj.sceneRect()
            pos = item.elem_data['position']
            x = pos['x'] / 100 * rect.width() - item.rect().width()/2
            y = (100 - pos['y']) / 100 * rect.height() - item.rect().height()/2
            item.setPos(x, y)
        elif prop in ('start_x', 'start_y'):
            key = 'start'
            if key not in item.elem_data:
                item.elem_data[key] = {'x': 30, 'y': 50}
            item.elem_data[key][prop.split('_')[1]] = value
        elif prop in ('end_x', 'end_y'):
            key = 'end'
            if key not in item.elem_data:
                item.elem_data[key] = {'x': 70, 'y': 50}
            item.elem_data[key][prop.split('_')[1]] = value
        elif prop == 'layers':
            try:
                layers = [int(x.strip()) for x in value.split(',')]
                item.elem_data['layers'] = layers
            except ValueError:
                pass
        else:
            item.elem_data[prop] = value

        item.update()

    def _delete_selected(self):
        item = self.canvas.get_selected_item()
        if item:
            step_elements = self.schema['steps'][self.current_step]['elements']
            cmd = DeleteElementCommand(self.canvas.scene_obj, step_elements, item.elem_data, item)
            self.undo_stack.push(cmd)
            self.properties.set_element(None)

    def _duplicate_selected(self):
        item = self.canvas.get_selected_item()
        if item:
            new_data = copy.deepcopy(item.elem_data)
            new_data['position']['x'] = min(95, new_data['position']['x'] + 5)
            new_data['position']['y'] = max(5, new_data['position']['y'] - 5)

            step_elements = self.schema['steps'][self.current_step]['elements']
            new_item = self.canvas.add_element(new_data)

            cmd = AddElementCommand(self.canvas.scene_obj, step_elements, new_data, new_item)
            self.undo_stack.push(cmd)

            item.setSelected(False)
            new_item.setSelected(True)

    def _add_step(self):
        idx = len(self.schema['steps']) + 1
        self.schema['steps'].append({
            'name': f'Step {idx}',
            'title': f'New Step {idx}',
            'elements': []
        })
        self._update_navigator()

    def _remove_step(self):
        if len(self.schema['steps']) <= 1:
            QMessageBox.warning(self, "Warning", "Cannot remove the last step.")
            return
        self.schema['steps'].pop(self.current_step)
        if self.current_step >= len(self.schema['steps']):
            self.current_step = len(self.schema['steps']) - 1
        self._load_step(self.current_step)

    def _rename_step(self, idx: int, name: str):
        if 0 <= idx < len(self.schema['steps']):
            self.schema['steps'][idx]['name'] = name

    def _reset_zoom(self):
        self.canvas.resetTransform()
        self.canvas.zoom_level = 1.0

    def _show_preview(self):
        """Open the animation preview window."""
        if 0 <= self.current_step < len(self.schema['steps']):
            step = self.schema['steps'][self.current_step]
            step_name = step.get('name', f'Step {self.current_step + 1}')
            self.preview_window = PreviewWindow(step, step_name, self)
            self.preview_window.show()

    def _new_presentation(self):
        self.schema = {
            'name': 'new_presentation',
            'title': 'New Presentation',
            'steps': [{'name': 'Step 1', 'title': 'Introduction', 'elements': []}]
        }
        self.schema_path = None
        self.current_step = 0
        self.undo_stack.clear()
        self._load_step(0)
        self.setWindowTitle("Presentation Designer - Untitled")

    def _open_file(self):
        path, _ = QFileDialog.getOpenFileName(self, "Open Schema", "schemas/", "JSON Files (*.json)")
        if path:
            with open(path) as f:
                self.schema = json.load(f)
            self.schema_path = path
            self.current_step = 0
            self.undo_stack.clear()
            self._load_step(0)
            self.setWindowTitle(f"Presentation Designer - {self.schema.get('name', 'Untitled')}")

    def _save_file(self):
        if not self.schema_path:
            path, _ = QFileDialog.getSaveFileName(self, "Save Schema", "schemas/", "JSON Files (*.json)")
            if not path:
                return
            if not path.endswith('.json'):
                path += '.json'
            self.schema_path = path

        with open(self.schema_path, 'w') as f:
            json.dump(self.schema, f, indent=2)

        self.statusBar().showMessage(f"Saved: {self.schema_path}")

    def _generate_python(self):
        if not self.schema_path:
            QMessageBox.warning(self, "Warning", "Save the schema first.")
            return

        try:
            from tools.generator import PresentationGenerator
            gen = PresentationGenerator(self.schema_path)
            output_path = gen.generate()
            QMessageBox.information(self, "Generated", f"Python file generated:\n{output_path}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Generation failed:\n{e}")


def main():
    app = QApplication(sys.argv)

    # Set application-wide font
    font = QFont('sans-serif', 10)
    app.setFont(font)

    schema_path = sys.argv[1] if len(sys.argv) > 1 else None
    window = PresentationDesigner(schema_path)
    window.show()

    sys.exit(app.exec())


if __name__ == '__main__':
    main()
