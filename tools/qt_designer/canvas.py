"""
Canvas components for the Qt Designer.
CanvasElement: Draggable, selectable element with custom rendering.
CanvasView: Zoomable, pannable view with grid.
"""

from typing import Optional, Dict, Any

import numpy as np

from PySide6.QtWidgets import (
    QGraphicsView, QGraphicsScene, QGraphicsItem, QGraphicsRectItem
)
from PySide6.QtCore import Qt, QRectF, QPointF, Signal
from PySide6.QtGui import (
    QColor, QPen, QBrush, QFont, QPainter, QWheelEvent,
    QPainterPath, QPolygonF, QUndoStack
)

from .constants import COLORS, ELEMENT_DEFAULTS, CANVAS_WIDTH, CANVAS_HEIGHT, GRID_SPACING_X, GRID_SPACING_Y, SNAP_GRID_SIZE
from .commands import MoveCommand, NudgeCommand


class CanvasElement(QGraphicsRectItem):
    """A draggable, selectable element on the canvas with custom rendering."""

    def __init__(self, elem_data: Dict[str, Any], scene_rect: QRectF):
        self.elem_data = elem_data
        self.scene_rect = scene_rect
        self._moving = False
        self._start_pos = None
        self._snap_enabled = False

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

    def set_snap_enabled(self, enabled: bool):
        """Enable or disable snap-to-grid."""
        self._snap_enabled = enabled

    def _sync_data_from_pos(self):
        """Sync element data from current position."""
        rect = self.scene_rect
        new_x = (self.pos().x() + self.rect().width()/2) / rect.width() * 100
        new_y = 100 - (self.pos().y() + self.rect().height()/2) / rect.height() * 100
        if 'position' not in self.elem_data:
            self.elem_data['position'] = {}
        self.elem_data['position']['x'] = round(max(0, min(100, new_x)), 1)
        self.elem_data['position']['y'] = round(max(0, min(100, new_y)), 1)

    def _update_visual_position(self):
        """Update visual position from element data."""
        pos = self.elem_data.get('position', {'x': 50, 'y': 50})
        x = pos['x'] / 100 * self.scene_rect.width() - self.rect().width()/2
        y = (100 - pos['y']) / 100 * self.scene_rect.height() - self.rect().height()/2
        self.setPos(x, y)

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
        elif change == QGraphicsItem.ItemPositionChange and self._snap_enabled:
            # Snap to grid
            new_pos = value
            # Convert to 0-100 coords
            x_coord = (new_pos.x() + self.rect().width()/2) / self.scene_rect.width() * 100
            y_coord = 100 - (new_pos.y() + self.rect().height()/2) / self.scene_rect.height() * 100
            # Snap
            x_coord = round(x_coord / SNAP_GRID_SIZE) * SNAP_GRID_SIZE
            y_coord = round(y_coord / SNAP_GRID_SIZE) * SNAP_GRID_SIZE
            # Convert back
            new_x = x_coord / 100 * self.scene_rect.width() - self.rect().width()/2
            new_y = (100 - y_coord) / 100 * self.scene_rect.height() - self.rect().height()/2
            return QPointF(new_x, new_y)
        return super().itemChange(change, value)

    def paint(self, painter, option, widget):
        """Custom paint based on element type."""
        painter.setRenderHint(QPainter.Antialiasing)

        elem_type = self.elem_data.get('type', 'text')
        rect = self.rect()

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
        elif elem_type == 'conversation':
            self._draw_conversation(painter, rect)
        elif elem_type == 'timeline':
            self._draw_timeline(painter, rect)
        elif elem_type == 'stacked_boxes':
            self._draw_stacked_boxes(painter, rect)
        elif elem_type == 'model_comparison':
            self._draw_model_comparison(painter, rect)
        elif elem_type == 'weight_comparison':
            self._draw_weight_comparison(painter, rect)
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
            text = item if isinstance(item, str) else str(item)
            painter.drawText(rect.x() + 10, y, f"* {text[:20]}")
            y += 16

    def _draw_checklist(self, painter, rect):
        painter.setBrush(Qt.NoBrush)
        painter.drawRoundedRect(rect, 4, 4)
        items = self.elem_data.get('items', [])[:4]
        y = rect.y() + 14
        for item in items:
            text = item if isinstance(item, str) else str(item)
            # Checkbox
            cb_rect = QRectF(rect.x() + 8, y - 8, 12, 12)
            painter.setPen(QPen(self._colors['success'], 2))
            painter.setBrush(QBrush(self._colors['success']))
            painter.drawRoundedRect(cb_rect, 2, 2)
            # Text
            painter.setPen(self._colors['text'])
            painter.setFont(QFont('sans-serif', 9))
            painter.drawText(rect.x() + 26, y + 2, text[:18])
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
            label = step.get('label', step.get('title', f'S{i+1}'))
            painter.drawText(step_rect, Qt.AlignCenter, str(label)[:8])
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
                    item = items[idx]
                    title = item.get('title', '') if isinstance(item, dict) else str(item)
                    painter.setPen(self._colors['text'])
                    painter.setFont(QFont('sans-serif', 7))
                    painter.drawText(cell_rect, Qt.AlignCenter, title[:8])
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

    def _draw_conversation(self, painter, rect):
        painter.setBrush(QBrush(self._colors['bg_light']))
        painter.drawRoundedRect(rect, 6, 6)
        messages = self.elem_data.get('messages', [])[:3]
        if not messages:
            messages = [{'role': 'user', 'content': 'Hello'}]
        msg_h = min(rect.height() / len(messages) - 4, 20)
        for i, msg in enumerate(messages):
            my = rect.y() + 4 + i * (msg_h + 4)
            role = msg.get('role', 'user')
            is_user = role in ('user', 'Input')
            color = self._colors['primary'] if is_user else self._colors['secondary']
            msg_w = rect.width() * 0.7
            mx = rect.x() + 4 if is_user else rect.x() + rect.width() - msg_w - 4
            painter.setPen(Qt.NoPen)
            painter.setBrush(QBrush(color))
            painter.drawRoundedRect(QRectF(mx, my, msg_w, msg_h), 4, 4)
            painter.setPen(self._colors['text'])
            painter.setFont(QFont('sans-serif', 7))
            content = msg.get('content', '')[:20]
            painter.drawText(QRectF(mx, my, msg_w, msg_h), Qt.AlignCenter, content)

    def _draw_timeline(self, painter, rect):
        painter.setBrush(Qt.NoBrush)
        painter.drawRoundedRect(rect, 4, 4)
        events = self.elem_data.get('events', [])[:4]
        # Line
        painter.setPen(QPen(self._colors['dim'], 2))
        y = rect.y() + rect.height() / 2
        painter.drawLine(QPointF(rect.x() + 10, y), QPointF(rect.x() + rect.width() - 10, y))
        # Events
        spacing = (rect.width() - 20) / max(len(events), 1)
        for i, ev in enumerate(events):
            ex = rect.x() + 10 + i * spacing + spacing / 2
            painter.setPen(Qt.NoPen)
            painter.setBrush(QBrush(self._colors['primary']))
            painter.drawEllipse(QPointF(ex, y), 5, 5)
            painter.setPen(self._colors['text'])
            painter.setFont(QFont('sans-serif', 7))
            title = ev.get('title', '')[:8] if isinstance(ev, dict) else str(ev)[:8]
            painter.drawText(QRectF(ex - 20, y - 18, 40, 15), Qt.AlignCenter, title)

    def _draw_stacked_boxes(self, painter, rect):
        items = self.elem_data.get('items', [])[:4]
        if not items:
            items = [{'title': 'Layer'}]
        base_w = rect.width() * 0.9
        box_h = rect.height() / len(items) - 4
        for i, item in enumerate(items):
            box_w = base_w - i * 8
            bx = rect.x() + (rect.width() - box_w) / 2
            by = rect.y() + i * (box_h + 4)
            painter.setPen(QPen(self._colors['primary'], 2))
            painter.setBrush(QBrush(self._colors['bg_light']))
            painter.drawRoundedRect(QRectF(bx, by, box_w, box_h), 4, 4)
            painter.setPen(self._colors['text'])
            painter.setFont(QFont('sans-serif', 8))
            title = item.get('title', f'Layer {i+1}')[:15] if isinstance(item, dict) else str(item)[:15]
            painter.drawText(QRectF(bx, by, box_w, box_h), Qt.AlignCenter, title)

    def _draw_model_comparison(self, painter, rect):
        painter.setBrush(QBrush(self._colors['bg_light']))
        painter.drawRoundedRect(rect, 6, 6)
        models = self.elem_data.get('models', [])[:3]
        if not models:
            models = [{'name': 'Model A'}, {'name': 'Model B'}]
        col_w = rect.width() / len(models)
        for i, model in enumerate(models):
            mx = rect.x() + i * col_w + col_w / 2
            color = self._colors.get(model.get('color', 'primary'), self._colors['primary'])
            painter.setPen(color)
            painter.setFont(QFont('sans-serif', 9, QFont.Bold))
            name = model.get('name', f'Model {i+1}')[:10]
            painter.drawText(QRectF(mx - col_w/2, rect.y() + 4, col_w, 20), Qt.AlignCenter, name)

    def _draw_weight_comparison(self, painter, rect):
        painter.setBrush(QBrush(self._colors['bg_light']))
        painter.drawRoundedRect(rect, 6, 6)
        before = self.elem_data.get('before_weights', [0.3, 0.5])[:4]
        after = self.elem_data.get('after_weights', [0.7, 0.8])[:4]
        bar_h = (rect.height() - 10) / max(len(before), 1) - 2
        max_w = rect.width() / 2 - 10
        for i in range(len(before)):
            by = rect.y() + 5 + i * (bar_h + 2)
            # Before bar
            bw = max_w * before[i]
            painter.setPen(Qt.NoPen)
            painter.setBrush(QBrush(self._colors['warning']))
            painter.drawRoundedRect(QRectF(rect.x() + 5, by, bw, bar_h), 2, 2)
            # After bar
            if i < len(after):
                aw = max_w * after[i]
                painter.setBrush(QBrush(self._colors['success']))
                painter.drawRoundedRect(QRectF(rect.x() + rect.width()/2 + 5, by, aw, bar_h), 2, 2)

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
        self._snap_enabled = False

        # Setup scene
        self.scene_obj = QGraphicsScene()
        self.scene_obj.setSceneRect(0, 0, CANVAS_WIDTH, CANVAS_HEIGHT)
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
        for x in range(0, int(rect.width()) + 1, GRID_SPACING_X):
            line = self.scene_obj.addLine(x, 0, x, rect.height(), pen)
            line.setZValue(-100)
        for y in range(0, int(rect.height()) + 1, GRID_SPACING_Y):
            line = self.scene_obj.addLine(0, y, rect.width(), y, pen)
            line.setZValue(-100)

    def _on_selection_changed(self):
        selected = self.scene_obj.selectedItems()
        if selected and isinstance(selected[0], CanvasElement):
            self.element_selected.emit(selected[0].elem_data)
        else:
            self.element_deselected.emit()

    def set_snap_enabled(self, enabled: bool):
        """Enable or disable snap-to-grid for all elements."""
        self._snap_enabled = enabled
        for item in self.scene_obj.items():
            if isinstance(item, CanvasElement):
                item.set_snap_enabled(enabled)

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

    def keyPressEvent(self, event):
        """Handle keyboard shortcuts including arrow key nudging."""
        item = self.get_selected_item()
        if item:
            # Arrow key nudging
            nudge_amount = 5 if event.modifiers() & Qt.ShiftModifier else 1
            dx, dy = 0, 0
            if event.key() == Qt.Key_Left:
                dx = -nudge_amount
            elif event.key() == Qt.Key_Right:
                dx = nudge_amount
            elif event.key() == Qt.Key_Up:
                dy = nudge_amount  # Y increases upward in our coord system
            elif event.key() == Qt.Key_Down:
                dy = -nudge_amount

            if dx != 0 or dy != 0:
                cmd = NudgeCommand(item, dx, dy)
                self.undo_stack.push(cmd)
                return

        super().keyPressEvent(event)

    def add_element(self, elem_data: Dict[str, Any]) -> CanvasElement:
        """Add an element to the canvas."""
        item = CanvasElement(elem_data, self.scene_obj.sceneRect())
        item.set_snap_enabled(self._snap_enabled)
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

    def get_selected_items(self):
        """Get all selected elements (for multi-select support)."""
        return [item for item in self.scene_obj.selectedItems() if isinstance(item, CanvasElement)]
