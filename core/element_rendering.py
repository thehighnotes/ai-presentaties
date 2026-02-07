"""
Centralized matplotlib element rendering.
Used by both the Qt designer preview and generated presentations.

This ensures visual consistency between preview and final output.
"""

import math
from typing import Dict, Any, Optional, Callable
from dataclasses import dataclass

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from matplotlib.patches import FancyBboxPatch, Circle, Wedge, Rectangle

from .styling import PresentationStyle
from .animations import AnimationHelper


# Get colors from central styling
COLORS = PresentationStyle.COLORS

# Animation phases and their time ranges
ANIMATION_PHASES = {
    'immediate': (0.0, 0.2),
    'early': (0.2, 0.4),
    'middle': (0.4, 0.6),
    'late': (0.6, 0.8),
    'final': (0.8, 1.0)
}


@dataclass
class RenderContext:
    """Context passed to element renderers."""
    ax: Axes
    progress: float  # Overall animation progress 0-1
    colors: Dict[str, str]

    # Computed per-element
    elem_progress: float = 0.0  # Element's own progress after phase/easing
    alpha: float = 1.0


class ElementRenderer:
    """
    Renders presentation elements to matplotlib axes.

    Usage:
        renderer = ElementRenderer(ax, colors=COLORS)
        renderer.render(element_data, progress=0.5)
    """

    def __init__(self, ax: Axes, colors: Optional[Dict[str, str]] = None):
        self.ax = ax
        self.colors = colors or COLORS
        self._elem_progress = 0.0

    def render(self, elem: Dict[str, Any], progress: float) -> None:
        """Render a single element with animation."""
        # Calculate element's animation state
        phase = elem.get('animation_phase', 'early')
        base_start, base_end = ANIMATION_PHASES.get(phase, (0.2, 0.4))

        # Apply timing modifiers
        duration = elem.get('duration', 1.0)
        delay = elem.get('delay', 0.0)
        speed = elem.get('speed', 1.0)

        start = base_start + delay * 0.05
        phase_length = (base_end - base_start) * duration
        end = min(1.0, start + phase_length)

        # Calculate normalized progress within this element's phase
        if progress < start:
            elem_progress = 0.0
        elif progress >= end:
            elem_progress = 1.0
        else:
            t = (progress - start) / max(end - start, 0.01)
            easing = elem.get('easing', 'ease_in_out')
            elem_progress = self._apply_easing(t, easing)

        self._elem_progress = elem_progress
        alpha = elem_progress

        if alpha <= 0:
            return

        elem_type = elem.get('type', 'text')
        pos = elem.get('position', {'x': 50, 'y': 50})
        x, y = pos['x'], pos['y']

        # Dispatch to specific renderer
        renderer_method = getattr(self, f'_render_{elem_type}', None)
        if renderer_method:
            renderer_method(elem, x, y, alpha, speed)
        else:
            self._render_generic(elem, x, y, alpha)

    def _apply_easing(self, t: float, easing: str) -> float:
        """Apply easing function using AnimationHelper."""
        if easing == 'linear':
            return t
        elif easing == 'ease_in':
            return AnimationHelper.ease_in(t)
        elif easing == 'ease_out':
            return AnimationHelper.ease_out(t)
        elif easing == 'ease_in_out':
            return AnimationHelper.ease_in_out(t)
        elif easing == 'ease_in_cubic':
            return AnimationHelper.ease_in_cubic(t)
        elif easing == 'ease_out_cubic':
            return AnimationHelper.ease_out_cubic(t)
        elif easing == 'elastic_out':
            return AnimationHelper.elastic_ease_out(t)
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

    def _stagger_alpha(self, base_alpha: float, index: int, total_items: int, stagger: bool = True) -> float:
        """Calculate alpha for staggered item reveal."""
        if not stagger or total_items <= 1:
            return base_alpha

        item_portion = 1.0 / total_items
        item_start = index * item_portion
        item_end = item_start + item_portion * 1.5

        if base_alpha < item_start:
            return 0.0
        elif base_alpha >= item_end:
            return 1.0
        else:
            t = (base_alpha - item_start) / (item_end - item_start)
            return min(1.0, max(0.0, t))

    # =========================================================================
    # Text Elements
    # =========================================================================

    def _render_text(self, elem: Dict, x: float, y: float, alpha: float, speed: float) -> None:
        content = elem.get('content', 'Text')
        fontsize = elem.get('fontsize', 14)
        style = elem.get('style', 'normal')
        color = elem.get('color', self.colors['text'])

        fontweight = 'bold' if style == 'title' else 'normal'
        self.ax.text(x, y, content, fontsize=fontsize, ha='center', va='center',
                    color=color, alpha=alpha, fontweight=fontweight)

    def _render_typewriter_text(self, elem: Dict, x: float, y: float, alpha: float, speed: float) -> None:
        content = elem.get('content', 'Typing...')
        type_progress = min(1.0, alpha * speed)
        visible_chars = int(len(content) * type_progress)
        display = content[:visible_chars]
        if visible_chars < len(content):
            display += '|'
        self.ax.text(x, y, display, fontsize=14, ha='center', va='center',
                    color=self.colors['text'], alpha=min(1.0, alpha * 2), family='monospace')

    def _render_code_block(self, elem: Dict, x: float, y: float, alpha: float, speed: float) -> None:
        w, h = elem.get('width', 30), elem.get('height', 15)
        self.ax.add_patch(FancyBboxPatch((x - w/2, y - h/2), w, h,
                                        boxstyle="round,pad=0.3",
                                        facecolor='#0d1117',
                                        edgecolor=self.colors['dim'],
                                        linewidth=1.5, alpha=alpha))
        code = elem.get('code', '# code')
        self.ax.text(x - w/2 + 2, y + h/4, code[:40],
                    fontsize=9, ha='left', color=self.colors['secondary'],
                    alpha=alpha, family='monospace')

    def _render_code_execution(self, elem: Dict, x: float, y: float, alpha: float, speed: float) -> None:
        w, h = elem.get('width', 30), elem.get('height', 20)
        # Code section
        self.ax.add_patch(FancyBboxPatch((x - w/2, y), w, h * 0.5,
                                        boxstyle="round,pad=0.2",
                                        facecolor='#0d1117',
                                        edgecolor=self.colors['dim'],
                                        linewidth=1, alpha=alpha))
        code = elem.get('code', '>>> code')
        self.ax.text(x - w/2 + 2, y + h * 0.35, code[:30],
                    fontsize=8, ha='left', color=self.colors['secondary'],
                    alpha=alpha, family='monospace')
        # Output section (appears after code)
        out_alpha = max(0, alpha * 2 - 0.5)
        if out_alpha > 0:
            self.ax.add_patch(FancyBboxPatch((x - w/2, y - h * 0.4), w, h * 0.35,
                                            boxstyle="round,pad=0.2",
                                            facecolor=self.colors['bg_light'],
                                            edgecolor=self.colors['success'],
                                            linewidth=1.5, alpha=out_alpha))
            output = elem.get('output', 'output')
            self.ax.text(x - w/2 + 2, y - h * 0.25, output[:25],
                        fontsize=8, ha='left', color=self.colors['success'],
                        alpha=out_alpha, family='monospace')

    # =========================================================================
    # Containers
    # =========================================================================

    def _render_box(self, elem: Dict, x: float, y: float, alpha: float, speed: float) -> None:
        w, h = elem.get('width', 20), elem.get('height', 12)
        color = elem.get('color', self.colors['primary'])
        rect = FancyBboxPatch((x - w/2, y - h/2), w, h,
                              boxstyle="round,pad=0.3",
                              facecolor=self.colors['bg_light'],
                              edgecolor=color,
                              linewidth=2, alpha=alpha)
        self.ax.add_patch(rect)
        if elem.get('title'):
            self.ax.text(x, y + h/4, elem['title'], fontsize=11,
                        fontweight='bold', ha='center', color=color, alpha=alpha)
        if elem.get('content'):
            self.ax.text(x, y - h/6, elem['content'][:50], fontsize=9,
                        ha='center', color=self.colors['text'], alpha=alpha)

    def _render_comparison(self, elem: Dict, x: float, y: float, alpha: float, speed: float) -> None:
        w, h = elem.get('width', 40), elem.get('height', 20)
        # Left box
        self.ax.add_patch(FancyBboxPatch((x - w/2, y - h/2), w/2 - 2, h,
                                        boxstyle="round,pad=0.2",
                                        facecolor=self.colors['bg_light'],
                                        edgecolor=self.colors['warning'],
                                        linewidth=2, alpha=alpha))
        # Right box
        self.ax.add_patch(FancyBboxPatch((x + 2, y - h/2), w/2 - 2, h,
                                        boxstyle="round,pad=0.2",
                                        facecolor=self.colors['bg_light'],
                                        edgecolor=self.colors['success'],
                                        linewidth=2, alpha=alpha))
        self.ax.text(x - w/4, y, elem.get('left_title', 'Before')[:10],
                    fontsize=10, fontweight='bold', ha='center', color=self.colors['warning'], alpha=alpha)
        self.ax.text(x + w/4, y, elem.get('right_title', 'After')[:10],
                    fontsize=10, fontweight='bold', ha='center', color=self.colors['success'], alpha=alpha)

    def _render_conversation(self, elem: Dict, x: float, y: float, alpha: float, speed: float) -> None:
        w, h = elem.get('width', 35), elem.get('height', 25)
        messages = elem.get('messages', [{'role': 'user', 'content': 'Hello'},
                                         {'role': 'assistant', 'content': 'Hi!'}])[:5]
        if not messages:
            messages = [{'role': 'user', 'content': 'Sample message'}]

        stagger = elem.get('stagger', True)
        msg_h = min(h / len(messages) - 2, 10)
        user_color = elem.get('user_color', self.colors['primary'])
        assistant_color = elem.get('assistant_color', self.colors['secondary'])

        for i, msg in enumerate(messages):
            m_alpha = self._stagger_alpha(alpha, i, len(messages), stagger)

            if m_alpha > 0:
                my = y + h/2 - i * (msg_h + 2) - msg_h/2 - 1
                role = msg.get('role', 'user')
                is_user = role == 'user' or role == 'Input'
                msg_w = w * 0.7
                mx = x - (w/2 - msg_w/2 - 2) if is_user else x + (w/2 - msg_w/2 - 2)
                color = user_color if is_user else assistant_color

                self.ax.add_patch(FancyBboxPatch((mx - msg_w/2, my - msg_h/2),
                                                msg_w, msg_h,
                                                boxstyle="round,pad=0.3",
                                                facecolor=color,
                                                edgecolor='none',
                                                alpha=m_alpha * 0.4))

                name = msg.get('name', role.capitalize())
                self.ax.text(mx - msg_w/2 + 2, my + msg_h/2 - 1.5, name[:10],
                            fontsize=6, fontweight='bold', ha='left',
                            color=color, alpha=m_alpha)

                content = msg.get('content', '')
                self.ax.text(mx, my - 1, content[:35],
                            fontsize=8, ha='center', va='center',
                            color=self.colors['text'], alpha=m_alpha)

    # =========================================================================
    # Lists
    # =========================================================================

    def _render_bullet_list(self, elem: Dict, x: float, y: float, alpha: float, speed: float) -> None:
        items = elem.get('items', [])[:6]
        stagger = elem.get('stagger', True)
        spacing = elem.get('spacing', 5)
        for j, item in enumerate(items):
            item_alpha = self._stagger_alpha(alpha, j, len(items), stagger)
            if item_alpha > 0:
                text = item if isinstance(item, str) else str(item)
                self.ax.text(x - 12, y + 8 - j * spacing, f"• {text}",
                           fontsize=10, ha='left', color=self.colors['text'], alpha=item_alpha)

    def _render_checklist(self, elem: Dict, x: float, y: float, alpha: float, speed: float) -> None:
        items = elem.get('items', [])[:5]
        stagger = elem.get('stagger', True)
        spacing = elem.get('spacing', 5)
        for j, item in enumerate(items):
            item_alpha = self._stagger_alpha(alpha, j, len(items), stagger)
            if item_alpha > 0:
                text = item if isinstance(item, str) else str(item)
                iy = y + 6 - j * spacing
                self.ax.add_patch(Rectangle((x - 12, iy - 1.5), 3, 3,
                                           facecolor=self.colors['success'],
                                           edgecolor=self.colors['success'],
                                           linewidth=1, alpha=item_alpha))
                self.ax.text(x - 7, iy, text[:20], fontsize=10, ha='left',
                           color=self.colors['text'], alpha=item_alpha)

    def _render_timeline(self, elem: Dict, x: float, y: float, alpha: float, speed: float) -> None:
        w = elem.get('width', 50)
        events = elem.get('events', [{'date': '2023', 'title': 'Event'}])[:5]
        self.ax.plot([x - w/2, x + w/2], [y, y], color=self.colors['dim'], lw=2, alpha=alpha)
        ev_spacing = w / max(len(events), 1)
        stagger = elem.get('stagger', True)
        for i, ev in enumerate(events):
            ev_alpha = self._stagger_alpha(alpha, i, len(events), stagger)
            if ev_alpha > 0:
                ex = x - w/2 + (i + 0.5) * ev_spacing
                self.ax.add_patch(Circle((ex, y), 1.5, facecolor=self.colors['primary'],
                                        edgecolor='white', linewidth=1, alpha=ev_alpha))
                title = ev.get('title', '')[:10] if isinstance(ev, dict) else str(ev)[:10]
                self.ax.text(ex, y + 4, title,
                            fontsize=7, ha='center', color=self.colors['text'], alpha=ev_alpha)
                date = ev.get('date', '')[:6] if isinstance(ev, dict) else ''
                self.ax.text(ex, y - 4, date,
                            fontsize=6, ha='center', color=self.colors['dim'], alpha=ev_alpha)

    # =========================================================================
    # Layout
    # =========================================================================

    def _render_flow(self, elem: Dict, x: float, y: float, alpha: float, speed: float) -> None:
        w = elem.get('width', 50)
        steps = elem.get('steps', [{'title': 'Step 1'}, {'title': 'Step 2'}])[:6]
        if not steps:
            steps = [{'title': 'Step'}]
        step_w = w / len(steps) - 3
        step_h = 12
        default_colors = [self.colors['warning'], self.colors['primary'],
                         self.colors['success'], self.colors['accent']]
        stagger = elem.get('stagger', True)

        for i, step in enumerate(steps):
            step_alpha = self._stagger_alpha(alpha, i, len(steps), stagger)

            if step_alpha > 0:
                sx = x - w/2 + i * (step_w + 3) + step_w/2
                color = step.get('color', default_colors[i % len(default_colors)])
                if isinstance(color, str) and color in self.colors:
                    color = self.colors[color]

                self.ax.add_patch(FancyBboxPatch((sx - step_w/2, y - step_h/2), step_w, step_h,
                                                boxstyle="round,pad=0.3",
                                                facecolor=self.colors['bg_light'],
                                                edgecolor=color,
                                                linewidth=2, alpha=step_alpha))

                title = step.get('title', step.get('label', f'Step {i+1}'))
                self.ax.text(sx, y + 1, str(title)[:12],
                            fontsize=9, fontweight='bold', ha='center', va='center',
                            color=color, alpha=step_alpha)

                subtitle = step.get('subtitle', '')
                if subtitle:
                    self.ax.text(sx, y - 3, subtitle[:15],
                                fontsize=7, ha='center', va='center',
                                color=self.colors['dim'], alpha=step_alpha * 0.8)

                if i < len(steps) - 1:
                    arrow_x = sx + step_w/2 + 0.5
                    self.ax.annotate('', xy=(arrow_x + 2, y), xytext=(arrow_x, y),
                                   arrowprops=dict(arrowstyle='->', lw=1.5,
                                                  color=self.colors['dim']),
                                   alpha=step_alpha * 0.7)

    def _render_grid(self, elem: Dict, x: float, y: float, alpha: float, speed: float) -> None:
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
                                                    facecolor=self.colors['bg_light'],
                                                    edgecolor=self.colors['primary'],
                                                    linewidth=1.5, alpha=cell_alpha))
                    if idx < len(items):
                        item = items[idx]
                        title = item.get('title', '')[:12] if isinstance(item, dict) else str(item)[:12]
                        self.ax.text(cx, cy + 2, title,
                                    fontsize=8, fontweight='bold', ha='center',
                                    color=self.colors['text'], alpha=cell_alpha)
                        desc = item.get('description', '') if isinstance(item, dict) else ''
                        if desc:
                            self.ax.text(cx, cy - 2, desc[:12],
                                        fontsize=7, ha='center',
                                        color=self.colors['dim'], alpha=cell_alpha * 0.8)
                idx += 1

    def _render_stacked_boxes(self, elem: Dict, x: float, y: float, alpha: float, speed: float) -> None:
        base_width = elem.get('base_width', elem.get('width', 40))
        box_height = elem.get('box_height', 10)
        width_decrease = elem.get('width_decrease', 4)
        spacing = elem.get('spacing', 12)
        items = elem.get('items', [{'title': 'Layer 1'}, {'title': 'Layer 2'}])[:6]
        stagger = elem.get('stagger', True)

        for i, item in enumerate(items):
            b_alpha = self._stagger_alpha(alpha, i, len(items), stagger)

            if b_alpha > 0:
                box_w = base_width - (i * width_decrease)
                by = y + (len(items)/2 - i - 0.5) * spacing

                color_name = item.get('color', 'primary') if isinstance(item, dict) else 'primary'
                color = self.colors.get(color_name, self.colors['primary'])

                self.ax.add_patch(FancyBboxPatch((x - box_w/2, by - box_height/2),
                                                box_w, box_height,
                                                boxstyle="round,pad=0.3",
                                                facecolor=self.colors['bg_light'],
                                                edgecolor=color,
                                                linewidth=2, alpha=b_alpha))

                title = item.get('title', f'Layer {i+1}')[:20] if isinstance(item, dict) else str(item)[:20]
                self.ax.text(x, by + 1, title,
                            fontsize=9, fontweight='bold', ha='center', va='center',
                            color=color, alpha=b_alpha)

                desc = item.get('description', '') if isinstance(item, dict) else ''
                if desc:
                    self.ax.text(x, by - 2.5, desc[:25],
                                fontsize=7, ha='center', va='center',
                                color=self.colors['dim'], alpha=b_alpha * 0.8)

    # =========================================================================
    # Connectors
    # =========================================================================

    def _render_arrow(self, elem: Dict, x: float, y: float, alpha: float, speed: float) -> None:
        start_pos = elem.get('start', {'x': 30, 'y': 50})
        end_pos = elem.get('end', {'x': 70, 'y': 50})
        ex = start_pos['x'] + (end_pos['x'] - start_pos['x']) * alpha
        ey = start_pos['y'] + (end_pos['y'] - start_pos['y']) * alpha
        color = elem.get('color', self.colors['primary'])
        self.ax.annotate('', xy=(ex, ey), xytext=(start_pos['x'], start_pos['y']),
                       arrowprops=dict(arrowstyle='-|>', lw=2, color=color))

    def _render_arc_arrow(self, elem: Dict, x: float, y: float, alpha: float, speed: float) -> None:
        start_pos = elem.get('start', {'x': 30, 'y': 50})
        end_pos = elem.get('end', {'x': 70, 'y': 50})
        ex = start_pos['x'] + (end_pos['x'] - start_pos['x']) * alpha
        ey = start_pos['y'] + (end_pos['y'] - start_pos['y']) * alpha
        arc_height = elem.get('arc_height', 15)
        rad = arc_height / 50  # Convert to matplotlib rad units
        color = elem.get('color', self.colors['primary'])
        self.ax.annotate('', xy=(ex, ey), xytext=(start_pos['x'], start_pos['y']),
                       arrowprops=dict(arrowstyle='-|>', lw=2, color=color,
                                      connectionstyle=f'arc3,rad={rad}'))

    def _render_particle_flow(self, elem: Dict, x: float, y: float, alpha: float, speed: float) -> None:
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
            circle = Circle((px, py), size, facecolor=self.colors['accent'],
                           edgecolor='none', alpha=p_alpha)
            self.ax.add_patch(circle)

    # =========================================================================
    # AI Visuals
    # =========================================================================

    def _render_neural_network(self, elem: Dict, x: float, y: float, alpha: float, speed: float) -> None:
        w, h = elem.get('width', 40), elem.get('height', 30)
        layers = elem.get('layers', [3, 5, 5, 2])
        show_connections = elem.get('show_connections', True)
        sp = w / (len(layers) + 1)

        # Store node positions for connections
        node_positions = []

        for li, n in enumerate(layers):
            layer_alpha = self._stagger_alpha(alpha, li, len(layers), True)
            if layer_alpha <= 0:
                continue
            lx = x - w/2 + (li + 1) * sp
            ns = h / (n + 1)
            layer_nodes = []
            for ni in range(n):
                ny = y - h/2 + (ni + 1) * ns
                layer_nodes.append((lx, ny))
                circle = Circle((lx, ny), 1.5, facecolor=self.colors['primary'],
                               edgecolor='white', linewidth=0.5, alpha=layer_alpha)
                self.ax.add_patch(circle)
            node_positions.append(layer_nodes)

        # Draw connections
        if show_connections and len(node_positions) > 1:
            for li in range(len(node_positions) - 1):
                conn_alpha = self._stagger_alpha(alpha, li, len(layers) - 1, True) * 0.3
                if conn_alpha > 0:
                    for n1 in node_positions[li]:
                        for n2 in node_positions[li + 1]:
                            self.ax.plot([n1[0], n2[0]], [n1[1], n2[1]],
                                       color=self.colors['dim'], lw=0.5, alpha=conn_alpha)

    def _render_attention_heatmap(self, elem: Dict, x: float, y: float, alpha: float, speed: float) -> None:
        w, h = elem.get('width', 30), elem.get('height', 30)
        tokens_x = elem.get('tokens_x', ['A', 'B', 'C'])[:8]
        tokens_y = elem.get('tokens_y', tokens_x)[:8]
        title = elem.get('title', '')
        n_x, n_y = len(tokens_x), len(tokens_y)

        grid_w = w * 0.8
        grid_h = h * 0.8
        grid_x = x - grid_w/2 + 3
        grid_y = y - grid_h/2
        cell_w = grid_w / max(n_x, 1)
        cell_h = grid_h / max(n_y, 1)

        if title:
            self.ax.text(x, y + h/2 + 3, title,
                        fontsize=12, fontweight='bold', ha='center',
                        color=self.colors['text'], alpha=alpha)

        np.random.seed(42)
        for i in range(n_y):
            for j in range(n_x):
                cell_idx = i * n_x + j
                stagger = elem.get('stagger', True)
                cell_alpha = self._stagger_alpha(alpha, cell_idx, n_x * n_y, stagger)

                if cell_alpha > 0:
                    cx = grid_x + j * cell_w
                    cy = grid_y + (n_y - 1 - i) * cell_h

                    # Generate attention weight - diagonal stronger (self-attention)
                    base_weight = np.random.rand() * 0.5
                    if i == j:
                        weight = 0.7 + np.random.rand() * 0.3
                    elif abs(i - j) == 1:
                        weight = 0.3 + np.random.rand() * 0.4
                    else:
                        weight = base_weight

                    display_weight = weight * cell_alpha

                    self.ax.add_patch(Rectangle((cx + 0.3, cy + 0.3),
                                               cell_w - 0.6, cell_h - 0.6,
                                               facecolor=self.colors['accent'],
                                               edgecolor=self.colors['bg_light'],
                                               linewidth=0.5,
                                               alpha=display_weight))

                    if elem.get('show_values', False) and cell_alpha > 0.5:
                        self.ax.text(cx + cell_w/2, cy + cell_h/2, f'{weight:.1f}',
                                    fontsize=6, ha='center', va='center',
                                    color='white', alpha=cell_alpha)

        # X-axis token labels (top)
        for j, tok in enumerate(tokens_x):
            self.ax.text(grid_x + j * cell_w + cell_w/2, grid_y + grid_h + 1.5,
                        tok[:6], fontsize=8, ha='center', va='bottom',
                        color=self.colors['text'], alpha=alpha)

        # Y-axis token labels (left)
        for i, tok in enumerate(tokens_y):
            self.ax.text(grid_x - 1.5, grid_y + (n_y - 1 - i) * cell_h + cell_h/2,
                        tok[:6], fontsize=8, ha='right', va='center',
                        color=self.colors['text'], alpha=alpha)

    def _render_token_flow(self, elem: Dict, x: float, y: float, alpha: float, speed: float) -> None:
        w, h = elem.get('width', 45), elem.get('height', 20)
        input_text = elem.get('input_text', 'Hello world')
        tokens = input_text.split()[:5]
        show_embeddings = elem.get('show_embeddings', True)

        # Input box
        self.ax.add_patch(FancyBboxPatch((x - w/2, y - h/4), w * 0.25, h/2,
                                        boxstyle="round,pad=0.2",
                                        facecolor='#0d1117',
                                        edgecolor=self.colors['dim'],
                                        linewidth=1, alpha=alpha))
        self.ax.text(x - w/2 + w * 0.125, y, input_text[:8],
                    fontsize=8, ha='center', color=self.colors['text'], alpha=alpha)

        # Arrow
        self.ax.annotate('', xy=(x - w/4 + 5, y), xytext=(x - w/4, y),
                       arrowprops=dict(arrowstyle='->', lw=1.5, color=self.colors['dim']),
                       alpha=alpha)

        # Tokens with staggered reveal
        for i, tok in enumerate(tokens):
            tok_alpha = self._stagger_alpha(alpha, i, len(tokens), True)
            if tok_alpha > 0:
                tx = x - w/4 + 8 + i * 8
                self.ax.add_patch(FancyBboxPatch((tx - 3, y - 3), 6, 6,
                                                boxstyle="round,pad=0.1",
                                                facecolor=self.colors['bg_light'],
                                                edgecolor=self.colors['accent'],
                                                linewidth=1, alpha=tok_alpha))
                self.ax.text(tx, y, tok[:5], fontsize=7, ha='center',
                            color=self.colors['accent'], alpha=tok_alpha)

    def _render_model_comparison(self, elem: Dict, x: float, y: float, alpha: float, speed: float) -> None:
        w, h = elem.get('width', 45), elem.get('height', 30)
        models = elem.get('models', [{'name': 'Model A'}, {'name': 'Model B'}])[:4]
        comparison_rows = elem.get('comparison_rows', [])
        n_models = len(models)
        col_w = w / (n_models + 1)
        n_rows = len(comparison_rows)
        row_h = h / (n_rows + 1.5) if n_rows > 0 else h * 0.6

        stagger = elem.get('stagger', True)
        for i, model in enumerate(models):
            m_alpha = self._stagger_alpha(alpha, i, n_models, stagger)

            if m_alpha > 0:
                mx = x - w/2 + (i + 1.5) * col_w
                color_name = model.get('color', 'primary')
                color = self.colors.get(color_name, self.colors['primary'])

                self.ax.text(mx, y + h/2 - 3, model.get('name', f'Model {i+1}')[:10],
                            fontsize=10, fontweight='bold', ha='center', va='center',
                            color=color, alpha=m_alpha)

                for row_idx, row_label in enumerate(comparison_rows):
                    row_alpha = self._stagger_alpha(alpha, row_idx + n_models, n_rows + n_models, stagger)
                    if row_alpha > 0:
                        ry = y + h/2 - (row_idx + 2) * row_h

                        if i == 0:
                            self.ax.text(x - w/2 + col_w/2, ry, row_label[:10],
                                        fontsize=8, ha='center', va='center',
                                        color=self.colors['dim'], alpha=row_alpha)

                        value = model.get(row_label.lower(), model.get(row_label, ''))
                        self.ax.text(mx, ry, str(value)[:12],
                                    fontsize=9, ha='center', va='center',
                                    color=self.colors['text'], alpha=row_alpha)

        if n_rows > 0:
            for row_idx in range(n_rows + 1):
                ly = y + h/2 - (row_idx + 1.2) * row_h
                self.ax.plot([x - w/2 + col_w * 0.3, x + w/2 - col_w * 0.3], [ly, ly],
                           color=self.colors['dim'], lw=0.5, alpha=alpha * 0.3)

    # =========================================================================
    # Metrics
    # =========================================================================

    def _render_similarity_meter(self, elem: Dict, x: float, y: float, alpha: float, speed: float) -> None:
        r = elem.get('radius', 8)
        score = elem.get('score', 75)
        label = elem.get('label', '')
        current_score = score * alpha

        # Background
        wedge_bg = Wedge((x, y), r, 0, 180, facecolor=self.colors['bg_light'],
                        edgecolor=self.colors['dim'], linewidth=2)
        self.ax.add_patch(wedge_bg)

        # Fill based on score
        fill_angle = 180 * (1 - current_score / 100)
        color = self.colors['success'] if current_score > 66 else (
            self.colors['accent'] if current_score > 33 else self.colors['warning'])
        wedge_fill = Wedge((x, y), r, fill_angle, 180, facecolor=color, edgecolor='none')
        self.ax.add_patch(wedge_fill)

        self.ax.text(x, y - 2, f"{int(current_score)}%", fontsize=12,
                    fontweight='bold', ha='center', va='center', color='white')

        if label:
            self.ax.text(x, y - r - 2, label, fontsize=9, ha='center',
                        color=self.colors['text'], alpha=alpha)

    def _render_progress_bar(self, elem: Dict, x: float, y: float, alpha: float, speed: float) -> None:
        w = elem.get('width', 30)
        current = elem.get('current', 5)
        total = elem.get('total', 10)
        label = elem.get('label', '')
        pct = (current / max(total, 1)) * alpha

        # Background
        self.ax.add_patch(FancyBboxPatch((x - w/2, y - 2), w, 4,
                                        boxstyle="round,pad=0.1",
                                        facecolor=self.colors['bg_light'],
                                        edgecolor=self.colors['dim'], linewidth=1.5, alpha=alpha))
        # Fill
        self.ax.add_patch(FancyBboxPatch((x - w/2, y - 2), w * pct, 4,
                                        boxstyle="round,pad=0.1",
                                        facecolor=self.colors['success'], edgecolor='none', alpha=alpha))

        if label:
            self.ax.text(x, y + 5, label, fontsize=9, ha='center',
                        color=self.colors['text'], alpha=alpha)

    def _render_weight_comparison(self, elem: Dict, x: float, y: float, alpha: float, speed: float) -> None:
        w, h = elem.get('width', 35), elem.get('height', 15)
        before = elem.get('before_weights', [0.3, 0.5, 0.2])[:5]
        after = elem.get('after_weights', [0.7, 0.8, 0.6])[:5]
        labels = elem.get('labels', [])
        bar_h = h / max(len(before), 1) - 1
        stagger = elem.get('stagger', True)

        for i in range(len(before)):
            bar_alpha = self._stagger_alpha(alpha, i, len(before), stagger)
            if bar_alpha > 0:
                by = y + h/2 - i * (bar_h + 1) - bar_h/2
                bw = (w/2 - 2) * before[i] * alpha
                self.ax.add_patch(Rectangle((x - w/2, by - bar_h/2), bw, bar_h,
                                           facecolor=self.colors['warning'], alpha=bar_alpha * 0.8))
                if i < len(after):
                    aw = (w/2 - 2) * after[i] * alpha
                    self.ax.add_patch(Rectangle((x + 2, by - bar_h/2), aw, bar_h,
                                               facecolor=self.colors['success'], alpha=bar_alpha * 0.8))
                if i < len(labels):
                    self.ax.text(x, by, labels[i][:8], fontsize=7, ha='center', va='center',
                               color=self.colors['text'], alpha=bar_alpha)

    def _render_parameter_slider(self, elem: Dict, x: float, y: float, alpha: float, speed: float) -> None:
        w = elem.get('width', 30)
        val = elem.get('current_value', 0.5)
        min_v = elem.get('min_value', 0)
        max_v = elem.get('max_value', 1)
        label = elem.get('label', 'Param')
        pct = (val - min_v) / (max_v - min_v) if max_v != min_v else 0.5

        # Label
        self.ax.text(x, y + 5, label[:15], fontsize=10,
                    fontweight='bold', ha='center', color=self.colors['text'], alpha=alpha)

        # Track
        self.ax.add_patch(Rectangle((x - w/2, y - 1), w, 2,
                                   facecolor='#333', edgecolor='#555',
                                   linewidth=0.5, alpha=alpha))
        # Fill
        self.ax.add_patch(Rectangle((x - w/2, y - 1), w * pct * alpha, 2,
                                   facecolor=self.colors['accent'], alpha=alpha))
        # Handle
        hx = x - w/2 + w * pct * alpha
        self.ax.add_patch(Circle((hx, y), 1.5, facecolor='white',
                                edgecolor=self.colors['accent'], linewidth=1.5, alpha=alpha))
        # Value
        self.ax.text(x, y - 4, f"{val:.2f}", fontsize=8, ha='center',
                    color=self.colors['accent'], alpha=alpha)

    # =========================================================================
    # 3D Elements
    # =========================================================================

    def _render_scatter_3d(self, elem: Dict, x: float, y: float, alpha: float, speed: float) -> None:
        w, h = elem.get('width', 30), elem.get('height', 25)
        self.ax.add_patch(FancyBboxPatch((x - w/2, y - h/2), w, h,
                                        boxstyle="round,pad=0.2",
                                        facecolor='#0d0d14',
                                        edgecolor=self.colors['dim'],
                                        linewidth=1.5, alpha=alpha))
        cx, cy = x, y
        # Draw axes
        self.ax.plot([cx - 8, cx + 8], [cy - 5, cy - 5], color=self.colors['warning'], lw=1.5, alpha=alpha)
        self.ax.plot([cx, cx], [cy - 5, cy + 8], color=self.colors['success'], lw=1.5, alpha=alpha)
        self.ax.plot([cx, cx - 6], [cy - 5, cy - 2], color=self.colors['primary'], lw=1.5, alpha=alpha)

        # Default points if none provided
        points = elem.get('points', [])
        if not points:
            points = [{'x': 2, 'y': 3}, {'x': -3, 'y': 4}, {'x': 4, 'y': -2}, {'x': -2, 'y': -3}, {'x': 0, 'y': 5}]

        for i, pt in enumerate(points[:10]):
            p_alpha = self._stagger_alpha(alpha, i, len(points), True)
            if p_alpha > 0:
                px = pt.get('x', 0) if isinstance(pt, dict) else 0
                py = pt.get('y', 0) if isinstance(pt, dict) else 0
                self.ax.add_patch(Circle((cx + px, cy + py), 1,
                                        facecolor=self.colors['accent'],
                                        edgecolor='white', linewidth=0.5, alpha=p_alpha))

    def _render_vector_3d(self, elem: Dict, x: float, y: float, alpha: float, speed: float) -> None:
        w, h = elem.get('width', 30), elem.get('height', 25)
        self.ax.add_patch(FancyBboxPatch((x - w/2, y - h/2), w, h,
                                        boxstyle="round,pad=0.2",
                                        facecolor='#0d0d14',
                                        edgecolor=self.colors['dim'],
                                        linewidth=1.5, alpha=alpha))
        cx, cy = x, y
        # Draw axes
        self.ax.plot([cx - 8, cx + 8], [cy - 5, cy - 5], color=self.colors['warning'], lw=1.5, alpha=alpha)
        self.ax.plot([cx, cx], [cy - 5, cy + 8], color=self.colors['success'], lw=1.5, alpha=alpha)
        self.ax.plot([cx, cx - 6], [cy - 5, cy - 2], color=self.colors['primary'], lw=1.5, alpha=alpha)

        # Default vectors if none provided
        vectors = elem.get('vectors', [])
        if not vectors:
            vectors = [{'x': 5, 'y': 4, 'color': 'warning'},
                      {'x': -4, 'y': 5, 'color': 'success'},
                      {'x': 3, 'y': -4, 'color': 'accent'}]

        for i, vec in enumerate(vectors[:6]):
            v_alpha = self._stagger_alpha(alpha, i, len(vectors), True)
            if v_alpha > 0:
                vx = vec.get('x', 0) if isinstance(vec, dict) else 0
                vy = vec.get('y', 0) if isinstance(vec, dict) else 0
                color_name = vec.get('color', 'accent') if isinstance(vec, dict) else 'accent'
                color = self.colors.get(color_name, self.colors['accent'])
                self.ax.annotate('', xy=(cx + vx * v_alpha, cy + vy * v_alpha), xytext=(cx, cy),
                               arrowprops=dict(arrowstyle='->', lw=2, color=color), alpha=v_alpha)

    # =========================================================================
    # Generic Fallback
    # =========================================================================

    def _render_generic(self, elem: Dict, x: float, y: float, alpha: float) -> None:
        w, h = elem.get('width', 15), elem.get('height', 10)
        elem_type = elem.get('type', 'unknown')
        self.ax.add_patch(FancyBboxPatch((x - w/2, y - h/2), w, h,
                                        boxstyle="round,pad=0.2",
                                        facecolor=self.colors['bg_light'],
                                        edgecolor=self.colors['dim'],
                                        linewidth=1.5, linestyle='--', alpha=alpha))
        self.ax.text(x, y, elem_type[:10], fontsize=9, ha='center',
                    color=self.colors['dim'], alpha=alpha)


def render_step(ax: Axes, step_data: Dict, progress: float,
                colors: Optional[Dict[str, str]] = None,
                show_title: bool = True,
                show_phase_markers: bool = False) -> None:
    """
    Convenience function to render a complete step.

    Args:
        ax: Matplotlib axes
        step_data: Step dictionary with 'elements', 'title', etc.
        progress: Animation progress 0-1
        colors: Optional color override
        show_title: Whether to show step title
        show_phase_markers: Whether to show phase indicator at bottom
    """
    colors = colors or COLORS

    ax.clear()
    ax.set_facecolor(colors.get('bg', '#0a0a0a'))
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.set_aspect('equal')
    ax.axis('off')

    # Title
    if show_title:
        title = step_data.get('title', '')
        if title:
            ax.text(50, 96, title, fontsize=18, fontweight='bold',
                   ha='center', va='top', color=colors.get('primary', '#3B82F6'))

    # Render elements
    renderer = ElementRenderer(ax, colors)
    for elem in step_data.get('elements', []):
        renderer.render(elem, progress)

    # Phase markers
    if show_phase_markers:
        phases = [('imm', 0.0), ('early', 0.2), ('mid', 0.4), ('late', 0.6), ('final', 0.8)]
        for name, start in phases:
            x = 10 + start * 80
            color = colors.get('accent', '#F59E0B') if progress >= start else colors.get('dim', '#6B7280')
            ax.plot([x, x], [2, 5], color=color, linewidth=2)
            ax.text(x, 1, name, fontsize=7, ha='center', color=color)
        ax.axhline(y=3.5, xmin=0.1, xmax=0.1 + 0.8 * progress,
                  color=colors.get('primary', '#3B82F6'), linewidth=3)
