"""
Centralized matplotlib element rendering.
Used by both the Qt designer preview and generated presentations.

This ensures visual consistency between preview and final output.
"""

import math
from typing import Dict, Any, Optional, Callable, Union
from dataclasses import dataclass

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from matplotlib.patches import FancyBboxPatch, Circle, Wedge, Rectangle, FancyArrowPatch, PathPatch
from matplotlib.path import Path
import matplotlib.patheffects as path_effects

from .styling import PresentationStyle
from .animations import AnimationHelper

# For 3D support
from mpl_toolkits.mplot3d import Axes3D, proj3d


class Arrow3D(FancyArrowPatch):
    """Custom 3D arrow for visualization - from original vector_presentation.py"""
    def __init__(self, xs, ys, zs, *args, **kwargs):
        super().__init__((0, 0), (0, 0), *args, **kwargs)
        self._verts3d = xs, ys, zs

    def do_3d_projection(self, renderer=None):
        xs3d, ys3d, zs3d = self._verts3d
        xs, ys, zs = proj3d.proj_transform(xs3d, ys3d, zs3d, self.axes.M)
        self.set_positions((xs[0], ys[0]), (xs[1], ys[1]))
        return np.min(zs)


def step_needs_3d_axes(step_data: Dict) -> bool:
    """Check if a step contains 3D elements that need real 3D axes."""
    elements = step_data.get('elements', [])
    for elem in elements:
        if elem.get('type') in ('scatter_3d', 'vector_3d'):
            return True
    return False

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
        self._global_progress = 0.0  # Overall animation progress for continuous effects

    def _add_shadow(self, x: float, y: float, w: float, h: float, alpha: float,
                    offset: tuple = (2, -2), blur: float = 0.3) -> None:
        """Add a drop shadow behind an element."""
        shadow = FancyBboxPatch(
            (x - w/2 + offset[0], y - h/2 + offset[1]), w, h,
            boxstyle="round,pad=0.3",
            facecolor='black',
            edgecolor='none',
            alpha=alpha * blur
        )
        self.ax.add_patch(shadow)

    def _add_glow(self, x: float, y: float, radius: float, color: str, alpha: float,
                  intensity: float = 0.5) -> None:
        """Add a glow effect behind an element."""
        # Multiple concentric circles with decreasing alpha for glow effect
        for i in range(4, 0, -1):
            glow_r = radius * (1 + i * 0.3)
            glow_alpha = alpha * intensity * (0.15 / i)
            glow = Circle((x, y), glow_r, facecolor=color, edgecolor='none', alpha=glow_alpha)
            self.ax.add_patch(glow)

    def _draw_animated_line(self, start: tuple, end: tuple, progress: float,
                           color: str, lw: float = 2, alpha: float = 1.0) -> None:
        """Draw a line that animates from start to end."""
        if progress <= 0:
            return
        # Calculate current endpoint based on progress
        cx = start[0] + (end[0] - start[0]) * min(1.0, progress)
        cy = start[1] + (end[1] - start[1]) * min(1.0, progress)
        self.ax.plot([start[0], cx], [start[1], cy], color=color, lw=lw, alpha=alpha, solid_capstyle='round')

    def render(self, elem: Dict[str, Any], progress: float) -> None:
        """Render a single element with animation."""
        # Store global progress for continuous effects (camera rotation, particles, etc.)
        self._global_progress = progress

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

        # Apply step-level alpha if present (for step transitions)
        step_alpha = elem.get('_step_alpha', 1.0)
        alpha = alpha * step_alpha

        if alpha <= 0:
            return

        elem_type = elem.get('type', 'text')
        pos = elem.get('position', {'x': 50, 'y': 50})
        x, y = pos['x'], pos['y']

        # Apply entry animation (fly-in from direction)
        entry_animation = elem.get('entry_animation', 'none')
        entry_distance = elem.get('entry_distance', 30)  # How far off-screen to start

        if entry_animation != 'none' and elem_progress < 1.0:
            # Calculate entry offset based on progress (1 = at final position)
            offset_factor = 1.0 - elem_progress
            if entry_animation == 'left':
                x -= entry_distance * offset_factor
            elif entry_animation == 'right':
                x += entry_distance * offset_factor
            elif entry_animation == 'top':
                y += entry_distance * offset_factor
            elif entry_animation == 'bottom':
                y -= entry_distance * offset_factor
            elif entry_animation == 'zoom':
                # Handled via scale below
                pass

        # Apply continuous effects (pulse/breathing) and entry zoom
        continuous_effect = elem.get('continuous_effect', 'none')
        effect_frequency = elem.get('effect_frequency', 1.0)
        scale = 1.0

        # Entry zoom animation
        if entry_animation == 'zoom' and elem_progress < 1.0:
            scale = 0.3 + 0.7 * elem_progress  # Start at 30% scale, grow to 100%

        if continuous_effect == 'pulse' and alpha >= 1.0:
            # Pulse effect: scale oscillates ±10%
            pulse_val = AnimationHelper.pulse(progress, effect_frequency * 2)
            scale = scale * (1.0 + pulse_val * 0.1)
        elif continuous_effect == 'breathing' and alpha >= 1.0:
            # Breathing effect: gentler scale oscillation ±5%
            breath_val = AnimationHelper.pulse(progress, effect_frequency * 0.5)
            scale = scale * (1.0 + breath_val * 0.05)

        # Apply step-level scale if present (for step transitions)
        step_scale = elem.get('_step_scale', 1.0)
        scale = scale * step_scale

        # Dispatch to specific renderer
        renderer_method = getattr(self, f'_render_{elem_type}', None)
        if renderer_method:
            renderer_method(elem, x, y, alpha, speed, scale)
        else:
            self._render_generic(elem, x, y, alpha, scale)

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

    def _render_text(self, elem: Dict, x: float, y: float, alpha: float, speed: float, scale: float = 1.0) -> None:
        content = elem.get('content', 'Text')
        fontsize = elem.get('fontsize', 14) * scale
        style = elem.get('style', 'normal')
        color = elem.get('color', self.colors['text'])
        if isinstance(color, str) and not color.startswith('#'):
            color = self.colors.get(color, color)

        fontweight = 'bold' if style == 'title' else 'normal'

        # Highlight animation: draw animated highlight behind text
        if elem.get('highlight', False):
            highlight_color = elem.get('highlight_color', self.colors['accent'])
            if isinstance(highlight_color, str) and not highlight_color.startswith('#'):
                highlight_color = self.colors.get(highlight_color, highlight_color)
            # Estimate text width (rough)
            text_width = len(content) * fontsize * 0.5
            text_height = fontsize * 1.2
            highlight_progress = min(1.0, alpha * speed * 1.5)
            # Draw highlight rectangle that grows
            self.ax.add_patch(Rectangle(
                (x - text_width/2, y - text_height/2),
                text_width * highlight_progress, text_height,
                facecolor=highlight_color, edgecolor='none', alpha=alpha * 0.3
            ))

        # Underline animation
        if elem.get('underline', False):
            underline_color = elem.get('underline_color', color)
            if isinstance(underline_color, str) and not underline_color.startswith('#'):
                underline_color = self.colors.get(underline_color, underline_color)
            text_width = len(content) * fontsize * 0.5
            underline_progress = min(1.0, alpha * speed * 1.5)
            line_y = y - fontsize * 0.7
            self.ax.plot(
                [x - text_width/2, x - text_width/2 + text_width * underline_progress],
                [line_y, line_y],
                color=underline_color, lw=2 * scale, alpha=alpha, solid_capstyle='round'
            )

        self.ax.text(x, y, content, fontsize=fontsize, ha='center', va='center',
                    color=color, alpha=alpha, fontweight=fontweight)

    def _render_typewriter_text(self, elem: Dict, x: float, y: float, alpha: float, speed: float, scale: float = 1.0) -> None:
        content = elem.get('content', 'Typing...')
        cursor_char = elem.get('cursor_char', '|')
        show_cursor = elem.get('show_cursor', True)
        fontsize = elem.get('fontsize', 14) * scale
        color = elem.get('color', self.colors['text'])
        if isinstance(color, str) and not color.startswith('#'):
            color = self.colors.get(color, color)

        # Reveal mode: 'char' (default) or 'word'
        reveal_mode = elem.get('reveal', 'char')
        type_progress = min(1.0, alpha * speed)

        if reveal_mode == 'word':
            # Word-by-word reveal
            words = content.split(' ')
            visible_words = int(len(words) * type_progress)
            display = ' '.join(words[:visible_words])
            if visible_words < len(words) and show_cursor:
                display += ' ' + cursor_char
        else:
            # Character-by-character reveal
            visible_chars = int(len(content) * type_progress)
            display = content[:visible_chars]
            if visible_chars < len(content) and show_cursor:
                display += cursor_char

        self.ax.text(x, y, display, fontsize=fontsize, ha='center', va='center',
                    color=color, alpha=min(1.0, alpha * 2), family='monospace')

    def _render_counter(self, elem: Dict, x: float, y: float, alpha: float, speed: float, scale: float = 1.0) -> None:
        """Animated number counter that counts up to target value."""
        target = elem.get('value', 100)
        prefix = elem.get('prefix', '')
        suffix = elem.get('suffix', '')
        fontsize = elem.get('fontsize', 24) * scale
        color = elem.get('color', self.colors['primary'])
        if isinstance(color, str) and not color.startswith('#'):
            color = self.colors.get(color, color)
        decimals = elem.get('decimals', 0)

        # Animate the count
        count_progress = min(1.0, alpha * speed * 1.2)
        # Use easing for more satisfying count
        eased_progress = 1 - (1 - count_progress) ** 3  # ease out cubic
        current = target * eased_progress

        if decimals > 0:
            display = f"{prefix}{current:.{decimals}f}{suffix}"
        else:
            display = f"{prefix}{int(current)}{suffix}"

        # Optional glow
        if elem.get('glow', False):
            self._add_glow(x, y, fontsize * 0.8, color, alpha, intensity=0.4)

        self.ax.text(x, y, display, fontsize=fontsize, ha='center', va='center',
                    color=color, alpha=alpha, fontweight='bold')

    def _render_code_block(self, elem: Dict, x: float, y: float, alpha: float, speed: float, scale: float = 1.0) -> None:
        w, h = elem.get('width', 30) * scale, elem.get('height', 15) * scale
        self.ax.add_patch(FancyBboxPatch((x - w/2, y - h/2), w, h,
                                        boxstyle="round,pad=0.3",
                                        facecolor='#0d1117',
                                        edgecolor=self.colors['dim'],
                                        linewidth=1.5, alpha=alpha))
        code = elem.get('code', '# code')
        # Show full code, wrap if needed
        lines = code.split('\n')[:8]  # Max 8 lines
        for i, line in enumerate(lines):
            self.ax.text(x - w/2 + 2, y + h/3 - i * 3, line[:80],
                        fontsize=8, ha='left', color=self.colors['secondary'],
                        alpha=alpha, family='monospace')

    def _render_code_execution(self, elem: Dict, x: float, y: float, alpha: float, speed: float, scale: float = 1.0) -> None:
        w, h = elem.get('width', 30) * scale, elem.get('height', 20) * scale
        # Code section
        self.ax.add_patch(FancyBboxPatch((x - w/2, y), w, h * 0.5,
                                        boxstyle="round,pad=0.2",
                                        facecolor='#0d1117',
                                        edgecolor=self.colors['dim'],
                                        linewidth=1, alpha=alpha))
        code = elem.get('code', '>>> code')
        # Show more code
        lines = code.split('\n')[:4]
        for i, line in enumerate(lines):
            self.ax.text(x - w/2 + 2, y + h * 0.4 - i * 2.5, line[:80],
                        fontsize=7, ha='left', color=self.colors['secondary'],
                        alpha=alpha, family='monospace')
        # Output section (appears after code)
        stagger = elem.get('stagger', True)
        out_alpha = max(0, alpha * 2 - 0.5) if stagger else alpha
        if out_alpha > 0:
            self.ax.add_patch(FancyBboxPatch((x - w/2, y - h * 0.4), w, h * 0.35,
                                            boxstyle="round,pad=0.2",
                                            facecolor=self.colors['bg_light'],
                                            edgecolor=self.colors['success'],
                                            linewidth=1.5, alpha=out_alpha))
            output = elem.get('output', 'output')
            out_lines = output.split('\n')[:3]
            for i, line in enumerate(out_lines):
                self.ax.text(x - w/2 + 2, y - h * 0.2 - i * 2.5, line[:80],
                            fontsize=7, ha='left', color=self.colors['success'],
                            alpha=out_alpha, family='monospace')

    # =========================================================================
    # Containers
    # =========================================================================

    def _render_box(self, elem: Dict, x: float, y: float, alpha: float, speed: float, scale: float = 1.0) -> None:
        w, h = elem.get('width', 20) * scale, elem.get('height', 12) * scale
        color = elem.get('color', self.colors['primary'])
        if isinstance(color, str) and not color.startswith('#'):
            color = self.colors.get(color, color)

        # Optional shadow
        if elem.get('shadow', False):
            shadow_offset = elem.get('shadow_offset', (2, -2))
            self._add_shadow(x, y, w, h, alpha, offset=shadow_offset)

        # Optional glow
        if elem.get('glow', False):
            glow_color = elem.get('glow_color', color)
            if isinstance(glow_color, str) and not glow_color.startswith('#'):
                glow_color = self.colors.get(glow_color, glow_color)
            self._add_glow(x, y, max(w, h) / 2, glow_color, alpha, intensity=0.6)

        rect = FancyBboxPatch((x - w/2, y - h/2), w, h,
                              boxstyle="round,pad=0.3",
                              facecolor=self.colors['bg_light'],
                              edgecolor=color,
                              linewidth=2, alpha=alpha)
        self.ax.add_patch(rect)
        if elem.get('title'):
            self.ax.text(x, y + h/4, elem['title'], fontsize=11 * scale,
                        fontweight='bold', ha='center', color=color, alpha=alpha)
        if elem.get('content'):
            self.ax.text(x, y - h/6, elem['content'], fontsize=9 * scale,
                        ha='center', color=self.colors['text'], alpha=alpha)

    def _render_comparison(self, elem: Dict, x: float, y: float, alpha: float, speed: float, scale: float = 1.0) -> None:
        w, h = elem.get('width', 40) * scale, elem.get('height', 20) * scale
        left_color = elem.get('left_color', self.colors['warning'])
        right_color = elem.get('right_color', self.colors['success'])
        # Left box
        self.ax.add_patch(FancyBboxPatch((x - w/2, y - h/2), w/2 - 2, h,
                                        boxstyle="round,pad=0.2",
                                        facecolor=self.colors['bg_light'],
                                        edgecolor=left_color,
                                        linewidth=2, alpha=alpha))
        # Right box
        self.ax.add_patch(FancyBboxPatch((x + 2, y - h/2), w/2 - 2, h,
                                        boxstyle="round,pad=0.2",
                                        facecolor=self.colors['bg_light'],
                                        edgecolor=right_color,
                                        linewidth=2, alpha=alpha))
        # Titles
        self.ax.text(x - w/4, y + h/3, elem.get('left_title', 'Before'),
                    fontsize=10 * scale, fontweight='bold', ha='center', color=left_color, alpha=alpha)
        self.ax.text(x + w/4, y + h/3, elem.get('right_title', 'After'),
                    fontsize=10 * scale, fontweight='bold', ha='center', color=right_color, alpha=alpha)
        # Content
        left_content = elem.get('left_content', '')
        right_content = elem.get('right_content', '')
        if left_content:
            self.ax.text(x - w/4, y - h/6, left_content,
                        fontsize=8 * scale, ha='center', color=self.colors['text'], alpha=alpha)
        if right_content:
            self.ax.text(x + w/4, y - h/6, right_content,
                        fontsize=8 * scale, ha='center', color=self.colors['text'], alpha=alpha)

    def _render_conversation(self, elem: Dict, x: float, y: float, alpha: float, speed: float, scale: float = 1.0) -> None:
        w, h = elem.get('width', 35) * scale, elem.get('height', 25) * scale
        messages = elem.get('messages', [{'role': 'user', 'content': 'Hello'},
                                         {'role': 'assistant', 'content': 'Hi!'}])[:8]
        if not messages:
            messages = [{'role': 'user', 'content': 'Sample message'}]

        stagger = elem.get('stagger', True)
        bubble_spacing = elem.get('bubble_spacing', 2)
        msg_h = min(h / len(messages) - bubble_spacing, 10)
        user_color = elem.get('user_color', self.colors['primary'])
        assistant_color = elem.get('assistant_color', self.colors['secondary'])
        system_color = elem.get('system_color', self.colors['dim'])

        for i, msg in enumerate(messages):
            m_alpha = self._stagger_alpha(alpha, i, len(messages), stagger)

            if m_alpha > 0:
                my = y + h/2 - i * (msg_h + bubble_spacing) - msg_h/2 - 1
                role = msg.get('role', 'user')
                is_user = role == 'user' or role == 'Input'
                is_system = role == 'system'
                msg_w = w * 0.7
                mx = x - (w/2 - msg_w/2 - 2) if is_user else x + (w/2 - msg_w/2 - 2)
                color = system_color if is_system else (user_color if is_user else assistant_color)

                self.ax.add_patch(FancyBboxPatch((mx - msg_w/2, my - msg_h/2),
                                                msg_w, msg_h,
                                                boxstyle="round,pad=0.3",
                                                facecolor=color,
                                                edgecolor='none',
                                                alpha=m_alpha * 0.4))

                name = msg.get('name', role.capitalize())
                self.ax.text(mx - msg_w/2 + 2, my + msg_h/2 - 1.5, name[:15],
                            fontsize=6, fontweight='bold', ha='left',
                            color=color, alpha=m_alpha)

                content = msg.get('content', '')
                # Show more content
                self.ax.text(mx, my - 1, content[:80],
                            fontsize=8, ha='center', va='center',
                            color=self.colors['text'], alpha=m_alpha)

    # =========================================================================
    # Lists
    # =========================================================================

    def _render_bullet_list(self, elem: Dict, x: float, y: float, alpha: float, speed: float, scale: float = 1.0) -> None:
        items = elem.get('items', [])[:10]
        stagger = elem.get('stagger', True)
        spacing = elem.get('spacing', 5) * scale
        bullet_char = elem.get('bullet_char', '•')
        fontsize = elem.get('fontsize', 10) * scale
        text_color = elem.get('text_color', self.colors['text'])
        for j, item in enumerate(items):
            item_alpha = self._stagger_alpha(alpha, j, len(items), stagger)
            if item_alpha > 0:
                text = item if isinstance(item, str) else str(item)
                self.ax.text(x - 12, y + 8 - j * spacing, f"{bullet_char} {text}",
                           fontsize=fontsize, ha='left', color=text_color, alpha=item_alpha)

    def _render_checklist(self, elem: Dict, x: float, y: float, alpha: float, speed: float, scale: float = 1.0) -> None:
        items = elem.get('items', [])[:10]
        stagger = elem.get('stagger', True)
        spacing = elem.get('spacing', 5) * scale
        check_color = elem.get('check_color', self.colors['success'])
        text_color = elem.get('text_color', self.colors['text'])
        fontsize = elem.get('fontsize', 10) * scale
        for j, item in enumerate(items):
            item_alpha = self._stagger_alpha(alpha, j, len(items), stagger)
            if item_alpha > 0:
                text = item if isinstance(item, str) else str(item)
                iy = y + 6 - j * spacing
                self.ax.add_patch(Rectangle((x - 12, iy - 1.5), 3, 3,
                                           facecolor=check_color,
                                           edgecolor=check_color,
                                           linewidth=1, alpha=item_alpha))
                self.ax.text(x - 7, iy, text, fontsize=fontsize, ha='left',
                           color=text_color, alpha=item_alpha)

    def _render_timeline(self, elem: Dict, x: float, y: float, alpha: float, speed: float, scale: float = 1.0) -> None:
        w = elem.get('width', 50) * scale
        h = elem.get('height', 15) * scale
        events = elem.get('events', [{'date': '2023', 'title': 'Event'}])[:8]
        orientation = elem.get('orientation', 'horizontal')
        line_color = elem.get('line_color', self.colors['dim'])
        stagger = elem.get('stagger', True)

        if orientation == 'vertical':
            # Vertical timeline
            self.ax.plot([x, x], [y - h/2, y + h/2], color=line_color, lw=2, alpha=alpha)
            ev_spacing = h / max(len(events), 1)
            for i, ev in enumerate(events):
                ev_alpha = self._stagger_alpha(alpha, i, len(events), stagger)
                if ev_alpha > 0:
                    ey = y + h/2 - (i + 0.5) * ev_spacing
                    self.ax.add_patch(Circle((x, ey), 1.5, facecolor=self.colors['primary'],
                                            edgecolor='white', linewidth=1, alpha=ev_alpha))
                    title = ev.get('title', '') if isinstance(ev, dict) else str(ev)
                    self.ax.text(x + 5, ey, title[:20],
                                fontsize=7, ha='left', va='center', color=self.colors['text'], alpha=ev_alpha)
                    date = ev.get('date', '') if isinstance(ev, dict) else ''
                    self.ax.text(x - 5, ey, date[:10],
                                fontsize=6, ha='right', va='center', color=self.colors['dim'], alpha=ev_alpha)
        else:
            # Horizontal timeline (default)
            self.ax.plot([x - w/2, x + w/2], [y, y], color=line_color, lw=2, alpha=alpha)
            ev_spacing = w / max(len(events), 1)
            for i, ev in enumerate(events):
                ev_alpha = self._stagger_alpha(alpha, i, len(events), stagger)
                if ev_alpha > 0:
                    ex = x - w/2 + (i + 0.5) * ev_spacing
                    self.ax.add_patch(Circle((ex, y), 1.5, facecolor=self.colors['primary'],
                                            edgecolor='white', linewidth=1, alpha=ev_alpha))
                    title = ev.get('title', '') if isinstance(ev, dict) else str(ev)
                    self.ax.text(ex, y + 4, title[:15],
                                fontsize=7, ha='center', color=self.colors['text'], alpha=ev_alpha)
                    date = ev.get('date', '') if isinstance(ev, dict) else ''
                    self.ax.text(ex, y - 4, date[:10],
                                fontsize=6, ha='center', color=self.colors['dim'], alpha=ev_alpha)

    # =========================================================================
    # Layout
    # =========================================================================

    def _render_flow(self, elem: Dict, x: float, y: float, alpha: float, speed: float, scale: float = 1.0) -> None:
        w = elem.get('width', 50) * scale
        steps = elem.get('steps', [{'title': 'Step 1'}, {'title': 'Step 2'}])[:6]
        if not steps:
            steps = [{'title': 'Step'}]
        step_w = w / len(steps) - 3
        step_h = 12 * scale
        custom_colors = elem.get('colors', [])
        default_colors = [self.colors['warning'], self.colors['primary'],
                         self.colors['success'], self.colors['accent']]
        stagger = elem.get('stagger', True)

        for i, step in enumerate(steps):
            step_alpha = self._stagger_alpha(alpha, i, len(steps), stagger)

            if step_alpha > 0:
                sx = x - w/2 + i * (step_w + 3) + step_w/2
                color = step.get('color', custom_colors[i] if i < len(custom_colors) else default_colors[i % len(default_colors)])
                if isinstance(color, str) and color in self.colors:
                    color = self.colors[color]

                self.ax.add_patch(FancyBboxPatch((sx - step_w/2, y - step_h/2), step_w, step_h,
                                                boxstyle="round,pad=0.3",
                                                facecolor=self.colors['bg_light'],
                                                edgecolor=color,
                                                linewidth=2, alpha=step_alpha))

                title = step.get('title', step.get('label', f'Step {i+1}'))
                self.ax.text(sx, y + 1, str(title)[:15],
                            fontsize=9 * scale, fontweight='bold', ha='center', va='center',
                            color=color, alpha=step_alpha)

                subtitle = step.get('subtitle', '')
                if subtitle:
                    self.ax.text(sx, y - 3, subtitle[:20],
                                fontsize=7 * scale, ha='center', va='center',
                                color=self.colors['dim'], alpha=step_alpha * 0.8)

                if i < len(steps) - 1:
                    arrow_x = sx + step_w/2 + 0.5
                    self.ax.annotate('', xy=(arrow_x + 2, y), xytext=(arrow_x, y),
                                   arrowprops=dict(arrowstyle='->', lw=1.5,
                                                  color=self.colors['dim']),
                                   alpha=step_alpha * 0.7)

    def _render_grid(self, elem: Dict, x: float, y: float, alpha: float, speed: float, scale: float = 1.0) -> None:
        w, h = elem.get('width', 35) * scale, elem.get('height', 25) * scale
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
                        title = item.get('title', '') if isinstance(item, dict) else str(item)
                        self.ax.text(cx, cy + 2, title[:20],
                                    fontsize=8 * scale, fontweight='bold', ha='center',
                                    color=self.colors['text'], alpha=cell_alpha)
                        desc = item.get('description', '') if isinstance(item, dict) else ''
                        if desc:
                            self.ax.text(cx, cy - 2, desc[:25],
                                        fontsize=7 * scale, ha='center',
                                        color=self.colors['dim'], alpha=cell_alpha * 0.8)
                idx += 1

    def _render_stacked_boxes(self, elem: Dict, x: float, y: float, alpha: float, speed: float, scale: float = 1.0) -> None:
        base_width = elem.get('base_width', elem.get('width', 40)) * scale
        box_height = elem.get('box_height', 10) * scale
        width_decrease = elem.get('width_decrease', 4) * scale
        spacing = elem.get('spacing', 12) * scale
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

                title = item.get('title', f'Layer {i+1}') if isinstance(item, dict) else str(item)
                self.ax.text(x, by + 1, title[:25],
                            fontsize=9 * scale, fontweight='bold', ha='center', va='center',
                            color=color, alpha=b_alpha)

                desc = item.get('description', '') if isinstance(item, dict) else ''
                if desc:
                    self.ax.text(x, by - 2.5, desc[:35],
                                fontsize=7 * scale, ha='center', va='center',
                                color=self.colors['dim'], alpha=b_alpha * 0.8)

    # =========================================================================
    # Connectors
    # =========================================================================

    def _render_arrow(self, elem: Dict, x: float, y: float, alpha: float, speed: float, scale: float = 1.0) -> None:
        start_pos = elem.get('start', {'x': 30, 'y': 50})
        end_pos = elem.get('end', {'x': 70, 'y': 50})
        color = elem.get('color', self.colors['primary'])
        if isinstance(color, str) and not color.startswith('#'):
            color = self.colors.get(color, color)
        line_width = elem.get('width', 2) * scale
        head_size = elem.get('head_size', 15)
        style = elem.get('style', 'simple')
        head_style = elem.get('head_style', 'arrow')  # arrow, circle, diamond, none

        # Stroke draw animation: arrow draws from start to end
        draw_progress = elem.get('draw_animation', True)
        if draw_progress:
            progress = min(1.0, alpha * speed * 1.3)
        else:
            progress = 1.0 if alpha > 0 else 0.0

        ex = start_pos['x'] + (end_pos['x'] - start_pos['x']) * progress
        ey = start_pos['y'] + (end_pos['y'] - start_pos['y']) * progress

        # Marching ants effect
        marching_ants = elem.get('marching_ants', False)
        if marching_ants:
            dash_offset = self._global_progress * speed * 20
            linestyle = (0, (5, 3))  # dash pattern
        else:
            dash_offset = 0
            linestyle = '-'

        # Head styles
        if head_style == 'none' or head_style == 'circle' or head_style == 'diamond':
            arrowstyle = '-'  # Plain line, we'll add the head separately
        else:  # arrow (default)
            if style == 'fancy':
                arrowstyle = 'fancy,head_length=0.4,head_width=0.4,tail_width=0.2'
            else:
                arrowstyle = f'-|>,head_length={head_size/30:.2f},head_width={head_size/40:.2f}'

        # Draw the line first (for marching ants control)
        if marching_ants:
            # Draw dashed line with animated offset
            for i in range(3):  # Multiple lines for marching effect
                offset = (dash_offset + i * 2.5) % 8
                self.ax.plot([start_pos['x'], ex], [start_pos['y'], ey],
                           color=color, lw=line_width, alpha=alpha * (0.3 + 0.7 * (i == 0)),
                           linestyle=(offset, (5, 3)), solid_capstyle='round')
            # Arrow head
            if head_style == 'arrow' and progress > 0.1:
                self.ax.annotate('', xy=(ex, ey),
                               xytext=(ex - (end_pos['x'] - start_pos['x']) * 0.05,
                                       ey - (end_pos['y'] - start_pos['y']) * 0.05),
                               arrowprops=dict(arrowstyle='-|>', lw=line_width, color=color))
        else:
            # Standard arrow
            if style == 'curved':
                self.ax.annotate('', xy=(ex, ey), xytext=(start_pos['x'], start_pos['y']),
                               arrowprops=dict(arrowstyle=arrowstyle, lw=line_width, color=color,
                                              connectionstyle='arc3,rad=0.2'))
            else:
                self.ax.annotate('', xy=(ex, ey), xytext=(start_pos['x'], start_pos['y']),
                               arrowprops=dict(arrowstyle=arrowstyle, lw=line_width, color=color))

        # Diamond head (custom)
        if head_style == 'diamond' and progress > 0.1:
            diamond_size = head_size / 5 * scale
            from matplotlib.patches import RegularPolygon
            angle = np.arctan2(end_pos['y'] - start_pos['y'], end_pos['x'] - start_pos['x'])
            diamond = RegularPolygon((ex, ey), numVertices=4, radius=diamond_size,
                                    orientation=angle + np.pi/4,
                                    facecolor=color, edgecolor=color, alpha=alpha)
            self.ax.add_patch(diamond)

        # Circle head (enhance the -o style)
        if head_style == 'circle' and progress > 0.1:
            circle_size = head_size / 6 * scale
            self.ax.add_patch(Circle((ex, ey), circle_size, facecolor=color,
                                    edgecolor='white', linewidth=1, alpha=alpha))

    def _render_arc_arrow(self, elem: Dict, x: float, y: float, alpha: float, speed: float, scale: float = 1.0) -> None:
        start_pos = elem.get('start', {'x': 30, 'y': 50})
        end_pos = elem.get('end', {'x': 70, 'y': 50})
        arc_height = elem.get('arc_height', 15)
        direction = elem.get('direction', 'up')
        color = elem.get('color', self.colors['primary'])
        if isinstance(color, str) and not color.startswith('#'):
            color = self.colors.get(color, color)
        line_width = elem.get('width', 2) * scale
        head_style = elem.get('head_style', 'arrow')

        # Stroke draw animation
        draw_animation = elem.get('draw_animation', True)
        if draw_animation:
            progress = min(1.0, alpha * speed * 1.3)
        else:
            progress = 1.0 if alpha > 0 else 0.0

        ex = start_pos['x'] + (end_pos['x'] - start_pos['x']) * progress
        ey = start_pos['y'] + (end_pos['y'] - start_pos['y']) * progress

        # Direction affects the sign of the arc radius
        rad = arc_height / 50
        if direction == 'down':
            rad = -rad

        # Arrow style
        if head_style == 'none':
            arrowstyle = '-'
        elif head_style == 'circle':
            arrowstyle = '-'  # Draw circle separately
        else:
            arrowstyle = '-|>'

        # Glow effect for arc
        if elem.get('glow', False):
            self._add_glow((start_pos['x'] + ex) / 2,
                          (start_pos['y'] + ey) / 2 + arc_height * (1 if direction == 'up' else -1) * 0.3,
                          arc_height * 0.5, color, alpha, intensity=0.3)

        self.ax.annotate('', xy=(ex, ey), xytext=(start_pos['x'], start_pos['y']),
                       arrowprops=dict(arrowstyle=arrowstyle, lw=line_width, color=color,
                                      connectionstyle=f'arc3,rad={rad}'))

        # Circle head
        if head_style == 'circle' and progress > 0.1:
            circle_size = elem.get('head_size', 12) / 6 * scale
            self.ax.add_patch(Circle((ex, ey), circle_size, facecolor=color,
                                    edgecolor='white', linewidth=1, alpha=alpha))

    def _render_particle_flow(self, elem: Dict, x: float, y: float, alpha: float, speed: float, scale: float = 1.0) -> None:
        start_pos = elem.get('start', {'x': 20, 'y': 50})
        end_pos = elem.get('end', {'x': 80, 'y': 50})
        n = elem.get('num_particles', 20)
        spread = elem.get('spread', 0.5)
        particle_size = elem.get('particle_size', 0.7) * scale
        color = elem.get('color', self.colors['accent'])
        # Use global progress for continuous particle flow, speed affects flow rate
        flow_phase = self._global_progress * speed * 3
        for i in range(n):
            t_pos = ((i / n) + flow_phase) % 1.0
            px = start_pos['x'] + (end_pos['x'] - start_pos['x']) * t_pos
            py = start_pos['y'] + (end_pos['y'] - start_pos['y']) * t_pos
            py += np.sin(i * 1.5) * spread * 5
            size = particle_size * (0.6 + np.sin(t_pos * np.pi) * 0.4)
            p_alpha = max(0, 0.3 + np.sin(t_pos * np.pi) * 0.7) * alpha
            circle = Circle((px, py), size, facecolor=color,
                           edgecolor='none', alpha=p_alpha)
            self.ax.add_patch(circle)

    # =========================================================================
    # AI Visuals
    # =========================================================================

    def _render_neural_network(self, elem: Dict, x: float, y: float, alpha: float, speed: float, scale: float = 1.0) -> None:
        w, h = elem.get('width', 40) * scale, elem.get('height', 30) * scale
        layers = elem.get('layers', [3, 5, 5, 2])
        layer_labels = elem.get('layer_labels', [])
        show_connections = elem.get('show_connections', True)
        node_color = elem.get('node_color', self.colors['primary'])
        connection_color = elem.get('connection_color', self.colors['dim'])
        active_color = elem.get('active_color', self.colors['accent'])
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
                circle = Circle((lx, ny), 1.5 * scale, facecolor=node_color,
                               edgecolor='white', linewidth=0.5, alpha=layer_alpha)
                self.ax.add_patch(circle)
            node_positions.append(layer_nodes)
            # Layer label
            if li < len(layer_labels):
                self.ax.text(lx, y - h/2 - 3, layer_labels[li][:15],
                            fontsize=7 * scale, ha='center', color=self.colors['dim'], alpha=layer_alpha)

        # Draw connections
        if show_connections and len(node_positions) > 1:
            for li in range(len(node_positions) - 1):
                conn_alpha = self._stagger_alpha(alpha, li, len(layers) - 1, True) * 0.3
                if conn_alpha > 0:
                    for n1 in node_positions[li]:
                        for n2 in node_positions[li + 1]:
                            self.ax.plot([n1[0], n2[0]], [n1[1], n2[1]],
                                       color=connection_color, lw=0.5, alpha=conn_alpha)

    def _render_attention_heatmap(self, elem: Dict, x: float, y: float, alpha: float, speed: float, scale: float = 1.0) -> None:
        w, h = elem.get('width', 30) * scale, elem.get('height', 30) * scale
        tokens_x = elem.get('tokens_x', ['A', 'B', 'C'])[:12]
        tokens_y = elem.get('tokens_y', tokens_x)[:12]
        title = elem.get('title', '')
        n_x, n_y = len(tokens_x), len(tokens_y)
        colormap = elem.get('colormap', 'accent')  # Use accent color or specify 'viridis', 'hot', etc.

        # User-provided weights or auto-generate
        user_weights = elem.get('weights', None)

        grid_w = w * 0.8
        grid_h = h * 0.8
        grid_x = x - grid_w/2 + 3
        grid_y = y - grid_h/2
        cell_w = grid_w / max(n_x, 1)
        cell_h = grid_h / max(n_y, 1)

        if title:
            self.ax.text(x, y + h/2 + 3, title,
                        fontsize=12 * scale, fontweight='bold', ha='center',
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

                    # Use provided weights or auto-generate
                    if user_weights and i < len(user_weights) and j < len(user_weights[i]):
                        weight = user_weights[i][j]
                    else:
                        # Generate attention weight - diagonal stronger (self-attention)
                        base_weight = np.random.rand() * 0.5
                        if i == j:
                            weight = 0.7 + np.random.rand() * 0.3
                        elif abs(i - j) == 1:
                            weight = 0.3 + np.random.rand() * 0.4
                        else:
                            weight = base_weight

                    display_weight = weight * cell_alpha

                    # Color selection
                    if colormap in self.colors:
                        cell_color = self.colors[colormap]
                    else:
                        cell_color = self.colors['accent']

                    self.ax.add_patch(Rectangle((cx + 0.3, cy + 0.3),
                                               cell_w - 0.6, cell_h - 0.6,
                                               facecolor=cell_color,
                                               edgecolor=self.colors['bg_light'],
                                               linewidth=0.5,
                                               alpha=display_weight))

                    if elem.get('show_values', False) and cell_alpha > 0.5:
                        self.ax.text(cx + cell_w/2, cy + cell_h/2, f'{weight:.2f}',
                                    fontsize=5 * scale, ha='center', va='center',
                                    color='white', alpha=cell_alpha)

        # X-axis token labels (top)
        for j, tok in enumerate(tokens_x):
            self.ax.text(grid_x + j * cell_w + cell_w/2, grid_y + grid_h + 1.5,
                        tok[:10], fontsize=7 * scale, ha='center', va='bottom',
                        color=self.colors['text'], alpha=alpha, rotation=45 if len(tok) > 4 else 0)

        # Y-axis token labels (left)
        for i, tok in enumerate(tokens_y):
            self.ax.text(grid_x - 1.5, grid_y + (n_y - 1 - i) * cell_h + cell_h/2,
                        tok[:10], fontsize=7 * scale, ha='right', va='center',
                        color=self.colors['text'], alpha=alpha)

    def _render_token_flow(self, elem: Dict, x: float, y: float, alpha: float, speed: float, scale: float = 1.0) -> None:
        w, h = elem.get('width', 45) * scale, elem.get('height', 20) * scale
        input_text = elem.get('input_text', 'Hello world')
        # Use custom tokens if provided, otherwise split
        tokens = elem.get('tokens', None)
        if tokens is None:
            tokens = input_text.split()[:8]
        else:
            tokens = tokens[:8]
        show_embeddings = elem.get('show_embeddings', True)
        embedding_dims_shown = elem.get('embedding_dims_shown', 3)
        stagger = elem.get('stagger', True)

        # Input box
        self.ax.add_patch(FancyBboxPatch((x - w/2, y - h/4), w * 0.25, h/2,
                                        boxstyle="round,pad=0.2",
                                        facecolor='#0d1117',
                                        edgecolor=self.colors['dim'],
                                        linewidth=1, alpha=alpha))
        self.ax.text(x - w/2 + w * 0.125, y, input_text[:15],
                    fontsize=7 * scale, ha='center', color=self.colors['text'], alpha=alpha)

        # Arrow
        self.ax.annotate('', xy=(x - w/4 + 5, y), xytext=(x - w/4, y),
                       arrowprops=dict(arrowstyle='->', lw=1.5, color=self.colors['dim']),
                       alpha=alpha)

        # Tokens with staggered reveal
        token_spacing = min(8, (w * 0.6) / max(len(tokens), 1))
        for i, tok in enumerate(tokens):
            tok_alpha = self._stagger_alpha(alpha, i, len(tokens), stagger)
            if tok_alpha > 0:
                tx = x - w/4 + 8 + i * token_spacing
                self.ax.add_patch(FancyBboxPatch((tx - 3, y - 3), 6, 6,
                                                boxstyle="round,pad=0.1",
                                                facecolor=self.colors['bg_light'],
                                                edgecolor=self.colors['accent'],
                                                linewidth=1, alpha=tok_alpha))
                self.ax.text(tx, y, tok[:6], fontsize=6 * scale, ha='center',
                            color=self.colors['accent'], alpha=tok_alpha)

    def _render_model_comparison(self, elem: Dict, x: float, y: float, alpha: float, speed: float, scale: float = 1.0) -> None:
        w, h = elem.get('width', 45) * scale, elem.get('height', 30) * scale
        models = elem.get('models', [{'name': 'Model A'}, {'name': 'Model B'}])[:5]
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

                self.ax.text(mx, y + h/2 - 3, model.get('name', f'Model {i+1}')[:15],
                            fontsize=10 * scale, fontweight='bold', ha='center', va='center',
                            color=color, alpha=m_alpha)

                for row_idx, row_label in enumerate(comparison_rows):
                    row_alpha = self._stagger_alpha(alpha, row_idx + n_models, n_rows + n_models, stagger)
                    if row_alpha > 0:
                        ry = y + h/2 - (row_idx + 2) * row_h

                        if i == 0:
                            self.ax.text(x - w/2 + col_w/2, ry, row_label[:15],
                                        fontsize=8 * scale, ha='center', va='center',
                                        color=self.colors['dim'], alpha=row_alpha)

                        value = model.get(row_label.lower(), model.get(row_label, ''))
                        self.ax.text(mx, ry, str(value)[:20],
                                    fontsize=9 * scale, ha='center', va='center',
                                    color=self.colors['text'], alpha=row_alpha)

        if n_rows > 0:
            for row_idx in range(n_rows + 1):
                ly = y + h/2 - (row_idx + 1.2) * row_h
                self.ax.plot([x - w/2 + col_w * 0.3, x + w/2 - col_w * 0.3], [ly, ly],
                           color=self.colors['dim'], lw=0.5, alpha=alpha * 0.3)

    # =========================================================================
    # Metrics
    # =========================================================================

    def _render_similarity_meter(self, elem: Dict, x: float, y: float, alpha: float, speed: float, scale: float = 1.0) -> None:
        r = elem.get('radius', 8) * scale
        score = elem.get('score', 75)
        label = elem.get('label', '')

        # Animate the score with easing
        animate_needle = elem.get('animate_needle', True)
        if animate_needle:
            # Use eased progress for smooth needle animation
            ease_progress = min(1.0, alpha * speed * 1.2)
            current_score = score * ease_progress
        else:
            current_score = score * alpha

        # Custom colors
        low_color = elem.get('low_color', self.colors['warning'])
        medium_color = elem.get('medium_color', self.colors['accent'])
        high_color = elem.get('high_color', self.colors['success'])

        # Resolve color names
        for c_name in ['low_color', 'medium_color', 'high_color']:
            c_val = locals()[c_name.replace('_color', '_color')]
            if isinstance(c_val, str) and not c_val.startswith('#'):
                if c_name == 'low_color':
                    low_color = self.colors.get(c_val, c_val)
                elif c_name == 'medium_color':
                    medium_color = self.colors.get(c_val, c_val)
                else:
                    high_color = self.colors.get(c_val, c_val)

        # Background
        wedge_bg = Wedge((x, y), r, 0, 180, facecolor=self.colors['bg_light'],
                        edgecolor=self.colors['dim'], linewidth=2, alpha=alpha)
        self.ax.add_patch(wedge_bg)

        # Determine color based on score
        color = high_color if current_score > 66 else (
            medium_color if current_score > 33 else low_color)

        # Glow effect
        if elem.get('glow', False) and current_score > 0:
            self._add_glow(x, y, r * 0.8, color, alpha, intensity=0.5)

        # Fill based on score
        fill_angle = 180 * (1 - current_score / 100)
        wedge_fill = Wedge((x, y), r, fill_angle, 180, facecolor=color, edgecolor='none', alpha=alpha)
        self.ax.add_patch(wedge_fill)

        # Needle indicator
        if elem.get('show_needle', True):
            needle_angle = np.radians(180 - (current_score / 100) * 180)
            needle_x = x + r * 0.7 * np.cos(needle_angle)
            needle_y = y + r * 0.7 * np.sin(needle_angle)
            self.ax.plot([x, needle_x], [y, needle_y], color='white', lw=2 * scale, alpha=alpha)
            self.ax.add_patch(Circle((x, y), r * 0.1, facecolor='white', edgecolor='none', alpha=alpha))

        self.ax.text(x, y - 2, f"{int(current_score)}%", fontsize=12 * scale,
                    fontweight='bold', ha='center', va='center', color='white', alpha=alpha)

        if label:
            self.ax.text(x, y - r - 2, label, fontsize=9 * scale, ha='center',
                        color=self.colors['text'], alpha=alpha)

    def _render_progress_bar(self, elem: Dict, x: float, y: float, alpha: float, speed: float, scale: float = 1.0) -> None:
        w = elem.get('width', 30) * scale
        h = elem.get('height', 4) * scale
        current = elem.get('current', 5)
        total = elem.get('total', 10)
        label = elem.get('label', '')
        color = elem.get('color', self.colors['success'])
        if isinstance(color, str) and not color.startswith('#'):
            color = self.colors.get(color, color)

        # Animate the fill: grows during fade-in
        animate_fill = elem.get('animate_fill', True)
        if animate_fill:
            pct = (current / max(total, 1)) * min(1.0, alpha * speed * 1.5)
        else:
            pct = (current / max(total, 1))

        # Background
        self.ax.add_patch(FancyBboxPatch((x - w/2, y - h/2), w, h,
                                        boxstyle="round,pad=0.1",
                                        facecolor=self.colors['bg_light'],
                                        edgecolor=self.colors['dim'], linewidth=1.5, alpha=alpha))

        # Glow behind fill
        if elem.get('glow', False) and pct > 0:
            glow_x = x - w/2 + (w * pct) / 2
            self._add_glow(glow_x, y, h * 2, color, alpha, intensity=0.4)

        # Fill
        if pct > 0:
            self.ax.add_patch(FancyBboxPatch((x - w/2, y - h/2), w * pct, h,
                                            boxstyle="round,pad=0.1",
                                            facecolor=color, edgecolor='none', alpha=alpha))

        # Show percentage
        if elem.get('show_percent', False):
            self.ax.text(x + w/2 + 3, y, f"{int(pct * 100)}%", fontsize=8 * scale,
                        ha='left', va='center', color=color, alpha=alpha, fontweight='bold')

        if label:
            self.ax.text(x, y + h/2 + 3, label, fontsize=9 * scale, ha='center',
                        color=self.colors['text'], alpha=alpha)

    def _render_weight_comparison(self, elem: Dict, x: float, y: float, alpha: float, speed: float, scale: float = 1.0) -> None:
        w, h = elem.get('width', 35) * scale, elem.get('height', 15) * scale
        before = elem.get('before_weights', [0.3, 0.5, 0.2])[:8]
        after = elem.get('after_weights', [0.7, 0.8, 0.6])[:8]
        labels = elem.get('labels', [])
        bar_height = elem.get('bar_height', 3) * scale
        bar_h = min(bar_height, h / max(len(before), 1) - 1)
        stagger = elem.get('stagger', True)

        # Animate bars growing
        animate_bars = elem.get('animate_bars', True)
        before_color = elem.get('before_color', self.colors['warning'])
        after_color = elem.get('after_color', self.colors['success'])
        if isinstance(before_color, str) and not before_color.startswith('#'):
            before_color = self.colors.get(before_color, before_color)
        if isinstance(after_color, str) and not after_color.startswith('#'):
            after_color = self.colors.get(after_color, after_color)

        for i in range(len(before)):
            bar_alpha = self._stagger_alpha(alpha, i, len(before), stagger)
            if bar_alpha > 0:
                by = y + h/2 - i * (bar_h + 1) - bar_h/2

                # Animate bar width growth
                growth = min(1.0, bar_alpha * speed * 1.5) if animate_bars else 1.0

                # Before bar (left side)
                bw = (w/2 - 4) * before[i] * growth
                if bw > 0:
                    self.ax.add_patch(Rectangle((x - w/2, by - bar_h/2), bw, bar_h,
                                               facecolor=before_color, alpha=bar_alpha * 0.8))

                # After bar (right side)
                if i < len(after):
                    aw = (w/2 - 4) * after[i] * growth
                    if aw > 0:
                        self.ax.add_patch(Rectangle((x + 4, by - bar_h/2), aw, bar_h,
                                                   facecolor=after_color, alpha=bar_alpha * 0.8))

                # Labels in center
                if i < len(labels):
                    self.ax.text(x, by, labels[i][:12], fontsize=7 * scale, ha='center', va='center',
                               color=self.colors['text'], alpha=bar_alpha)

    def _render_parameter_slider(self, elem: Dict, x: float, y: float, alpha: float, speed: float, scale: float = 1.0) -> None:
        w = elem.get('width', 30) * scale
        val = elem.get('current_value', 0.5)
        min_v = elem.get('min_value', 0)
        max_v = elem.get('max_value', 1)
        label = elem.get('label', 'Param')
        description = elem.get('description', '')
        effect_preview = elem.get('effect_preview', '')
        color = elem.get('color', self.colors['accent'])
        pct = (val - min_v) / (max_v - min_v) if max_v != min_v else 0.5

        # Label
        self.ax.text(x, y + 5, label[:20], fontsize=10 * scale,
                    fontweight='bold', ha='center', color=self.colors['text'], alpha=alpha)

        # Description
        if description:
            self.ax.text(x, y + 8, description[:40], fontsize=7 * scale,
                        ha='center', color=self.colors['dim'], alpha=alpha * 0.8)

        # Track
        self.ax.add_patch(Rectangle((x - w/2, y - 1), w, 2,
                                   facecolor='#333', edgecolor='#555',
                                   linewidth=0.5, alpha=alpha))
        # Fill
        self.ax.add_patch(Rectangle((x - w/2, y - 1), w * pct * alpha, 2,
                                   facecolor=color, alpha=alpha))
        # Handle
        hx = x - w/2 + w * pct * alpha
        self.ax.add_patch(Circle((hx, y), 1.5 * scale, facecolor='white',
                                edgecolor=color, linewidth=1.5, alpha=alpha))
        # Value
        self.ax.text(x, y - 4, f"{val:.2f}", fontsize=8 * scale, ha='center',
                    color=color, alpha=alpha)

        # Effect preview
        if effect_preview:
            self.ax.text(x, y - 7, effect_preview[:30], fontsize=6 * scale,
                        ha='center', color=self.colors['dim'], alpha=alpha * 0.7)

    # =========================================================================
    # 3D Elements
    # =========================================================================

    def _project_3d(self, px: float, py: float, pz: float,
                    elev_rad: float, azim_rad: float,
                    cx: float, cy: float, scale_factor: float) -> tuple:
        """
        Project 3D point to 2D using proper rotation matrices.

        Args:
            px, py, pz: 3D coordinates
            elev_rad: Elevation angle in radians (rotation around X axis)
            azim_rad: Azimuth angle in radians (rotation around Z axis)
            cx, cy: Center point in 2D
            scale_factor: Scaling factor for the projection

        Returns:
            (x_2d, y_2d, depth) tuple - depth used for z-ordering
        """
        # First rotate around Z axis (azimuth)
        x1 = px * np.cos(azim_rad) - py * np.sin(azim_rad)
        y1 = px * np.sin(azim_rad) + py * np.cos(azim_rad)
        z1 = pz

        # Then rotate around X axis (elevation) - looking down from above
        x2 = x1
        y2 = y1 * np.cos(elev_rad) - z1 * np.sin(elev_rad)
        z2 = y1 * np.sin(elev_rad) + z1 * np.cos(elev_rad)

        # Project to 2D (orthographic projection - ignore z2 for position)
        x_2d = cx + x2 * scale_factor
        y_2d = cy + z2 * scale_factor  # Z becomes Y on screen (up)

        return (x_2d, y_2d, y2)  # y2 is depth (further = more negative)

    def _render_3d_axes(self, cx: float, cy: float, scale_factor: float,
                        elev_rad: float, azim_rad: float, alpha: float, scale: float = 1.0) -> tuple:
        """Draw 3D coordinate axes and return origin point."""
        # Project axis endpoints
        origin = self._project_3d(0, 0, 0, elev_rad, azim_rad, cx, cy, scale_factor)
        x_end = self._project_3d(1, 0, 0, elev_rad, azim_rad, cx, cy, scale_factor)
        y_end = self._project_3d(0, 1, 0, elev_rad, azim_rad, cx, cy, scale_factor)
        z_end = self._project_3d(0, 0, 1, elev_rad, azim_rad, cx, cy, scale_factor)

        # Draw axes
        axis_alpha = alpha * 0.7
        self.ax.plot([origin[0], x_end[0]], [origin[1], x_end[1]],
                    color=self.colors['warning'], lw=1.5 * scale, alpha=axis_alpha)
        self.ax.plot([origin[0], y_end[0]], [origin[1], y_end[1]],
                    color=self.colors['success'], lw=1.5 * scale, alpha=axis_alpha)
        self.ax.plot([origin[0], z_end[0]], [origin[1], z_end[1]],
                    color=self.colors['primary'], lw=1.5 * scale, alpha=axis_alpha)

        # Axis labels
        label_offset = scale_factor * 0.15
        self.ax.text(x_end[0] + label_offset, x_end[1], 'X',
                    fontsize=7 * scale, color=self.colors['warning'], alpha=alpha, ha='left')
        self.ax.text(y_end[0] + label_offset, y_end[1], 'Y',
                    fontsize=7 * scale, color=self.colors['success'], alpha=alpha, ha='left')
        self.ax.text(z_end[0], z_end[1] + label_offset, 'Z',
                    fontsize=7 * scale, color=self.colors['primary'], alpha=alpha, ha='center')

        return origin

    def _is_3d_axes(self) -> bool:
        """Check if we're rendering on a 3D axes."""
        return hasattr(self.ax, 'get_zlim')

    def _render_scatter_3d(self, elem: Dict, x: float, y: float, alpha: float, speed: float, scale: float = 1.0) -> None:
        """Render 3D scatter plot. Uses real 3D if on 3D axes, otherwise 2D projection."""
        if self._is_3d_axes():
            self._render_scatter_3d_real(elem, alpha, speed, scale)
        else:
            self._render_scatter_3d_projected(elem, x, y, alpha, speed, scale)

    def _render_scatter_3d_real(self, elem: Dict, alpha: float, speed: float, scale: float = 1.0) -> None:
        """Render 3D scatter using real matplotlib 3D axes."""
        from .styling import PresentationStyle

        elev = elem.get('camera_elev', 20)
        azim = elem.get('camera_azim', 45)
        rotate_camera = elem.get('rotate_camera', False)
        rotation_speed = elem.get('camera_rotation_speed', 30)

        if rotate_camera:
            # Use global progress for continuous rotation, apply speed multiplier
            azim = (azim + self._global_progress * rotation_speed * speed * 10) % 360

        self.ax.view_init(elev=elev, azim=azim)
        PresentationStyle.setup_3d_axis(self.ax)

        points = elem.get('points', [])
        if not points:
            points = [
                {'x': 2, 'y': 3, 'z': 1, 'color': 'accent'},
                {'x': -3, 'y': 4, 'z': 2, 'color': 'primary'},
                {'x': 4, 'y': -2, 'z': -1, 'color': 'secondary'},
            ]

        # Calculate data range
        xs = [pt.get('x', 0) for pt in points if isinstance(pt, dict)]
        ys = [pt.get('y', 0) for pt in points if isinstance(pt, dict)]
        zs = [pt.get('z', 0) for pt in points if isinstance(pt, dict)]

        if xs and ys and zs:
            max_range = max(max(abs(v) for v in xs), max(abs(v) for v in ys), max(abs(v) for v in zs), 1)
            limit = max_range * 1.2
            self.ax.set_xlim(-limit, limit)
            self.ax.set_ylim(-limit, limit)
            self.ax.set_zlim(-limit, limit)

        show_vectors = elem.get('show_vectors', False)
        stagger_points = elem.get('stagger_points', True)

        for i, pt in enumerate(points[:30]):
            p_alpha = self._stagger_alpha(alpha, i, len(points), stagger_points)
            if p_alpha > 0:
                px = pt.get('x', 0)
                py = pt.get('y', 0)
                pz = pt.get('z', 0)
                color_name = pt.get('color', 'accent')
                color = self.colors.get(color_name, self.colors['accent'])
                size = pt.get('size', 80) * scale

                self.ax.scatter([px], [py], [pz], c=[color], s=size, alpha=p_alpha, edgecolors='white', linewidth=0.5)

                if show_vectors:
                    self.ax.plot([0, px], [0, py], [0, pz], color=color, lw=1, alpha=p_alpha * 0.5, linestyle='--')

    def _render_scatter_3d_projected(self, elem: Dict, x: float, y: float, alpha: float, speed: float, scale: float = 1.0) -> None:
        """Fallback: Render 3D scatter using 2D projection."""
        w, h = elem.get('width', 30) * scale, elem.get('height', 25) * scale

        elev = elem.get('camera_elev', 20)
        azim = elem.get('camera_azim', 45)
        rotate_camera = elem.get('rotate_camera', False)
        rotation_speed = elem.get('camera_rotation_speed', 30)

        if rotate_camera:
            # Use global progress for continuous rotation, apply speed multiplier
            azim = (azim + self._global_progress * rotation_speed * speed * 10) % 360

        elev_rad = np.radians(elev)
        azim_rad = np.radians(azim)

        # Background box
        self.ax.add_patch(FancyBboxPatch((x - w/2, y - h/2), w, h,
                                        boxstyle="round,pad=0.2",
                                        facecolor='#0d0d14',
                                        edgecolor=self.colors['dim'],
                                        linewidth=1.5, alpha=alpha))

        cx, cy = x, y

        points = elem.get('points', [])
        if not points:
            points = [
                {'x': 2, 'y': 3, 'z': 1, 'color': 'accent'},
                {'x': -3, 'y': 4, 'z': 2, 'color': 'primary'},
                {'x': 4, 'y': -2, 'z': -1, 'color': 'secondary'},
            ]

        # Calculate data range
        xs = [pt.get('x', 0) for pt in points if isinstance(pt, dict)]
        ys = [pt.get('y', 0) for pt in points if isinstance(pt, dict)]
        zs = [pt.get('z', 0) for pt in points if isinstance(pt, dict)]
        max_range = max(max(abs(v) for v in xs + ys + zs) if xs else 1, 1)

        scale_factor = min(w, h) * 0.35 / max_range
        origin = self._render_3d_axes(cx, cy, scale_factor, elev_rad, azim_rad, alpha, scale)

        stagger_points = elem.get('stagger_points', True)
        show_vectors = elem.get('show_vectors', False)

        projected_points = []
        for i, pt in enumerate(points[:30]):
            p_alpha = self._stagger_alpha(alpha, i, len(points), stagger_points)
            if p_alpha > 0:
                px, py, pz = pt.get('x', 0), pt.get('y', 0), pt.get('z', 0)
                color = self.colors.get(pt.get('color', 'accent'), self.colors['accent'])
                size = pt.get('size', 1.2) * scale
                proj = self._project_3d(px, py, pz, elev_rad, azim_rad, cx, cy, scale_factor)
                projected_points.append((proj, color, size, p_alpha, px, py, pz))

        projected_points.sort(key=lambda p: p[0][2])

        for proj, color, size, p_alpha, px, py, pz in projected_points:
            self.ax.add_patch(Circle((proj[0], proj[1]), size,
                                    facecolor=color, edgecolor='white',
                                    linewidth=0.5, alpha=p_alpha))
            if show_vectors:
                self.ax.plot([origin[0], proj[0]], [origin[1], proj[1]],
                           color=color, lw=0.5, alpha=p_alpha * 0.4, linestyle='--')

    def _render_vector_3d(self, elem: Dict, x: float, y: float, alpha: float, speed: float, scale: float = 1.0) -> None:
        """Render 3D vectors. Uses real 3D if on 3D axes, otherwise 2D projection."""
        if self._is_3d_axes():
            self._render_vector_3d_real(elem, alpha, speed, scale)
        else:
            self._render_vector_3d_projected(elem, x, y, alpha, speed, scale)

    def _render_vector_3d_real(self, elem: Dict, alpha: float, speed: float, scale: float = 1.0) -> None:
        """Render 3D vectors using real matplotlib 3D axes with Arrow3D."""
        from .styling import PresentationStyle

        elev = elem.get('camera_elev', 20)
        azim = elem.get('camera_azim', 45)
        rotate_camera = elem.get('rotate_camera', False)
        rotation_speed = elem.get('camera_rotation_speed', 30)

        if rotate_camera:
            # Use global progress for continuous rotation, apply speed multiplier
            azim = (azim + self._global_progress * rotation_speed * speed * 10) % 360

        self.ax.view_init(elev=elev, azim=azim)
        PresentationStyle.setup_3d_axis(self.ax)

        vectors = elem.get('vectors', [])
        if not vectors:
            vectors = [
                {'x': 4, 'y': 2, 'z': 3, 'color': 'warning', 'label': 'v1'},
                {'x': -3, 'y': 4, 'z': 1, 'color': 'success', 'label': 'v2'},
                {'x': 2, 'y': -2, 'z': 4, 'color': 'accent', 'label': 'v3'}
            ]

        # Calculate data range
        xs = [abs(vec.get('x', 0)) for vec in vectors if isinstance(vec, dict)]
        ys = [abs(vec.get('y', 0)) for vec in vectors if isinstance(vec, dict)]
        zs = [abs(vec.get('z', 0)) for vec in vectors if isinstance(vec, dict)]

        if xs and ys and zs:
            max_range = max(max(xs), max(ys), max(zs), 1)
            limit = max_range * 1.3
            self.ax.set_xlim(-limit, limit)
            self.ax.set_ylim(-limit, limit)
            self.ax.set_zlim(-limit, limit)

        stagger = elem.get('stagger', True)

        for i, vec in enumerate(vectors[:15]):
            v_alpha = self._stagger_alpha(alpha, i, len(vectors), stagger)
            if v_alpha > 0:
                vx = vec.get('x', 0)
                vy = vec.get('y', 0)
                vz = vec.get('z', 0)
                color_name = vec.get('color', 'accent')
                color = self.colors.get(color_name, self.colors['accent'])
                label = vec.get('label', '')

                # Animate vector growth
                vx_anim = vx * min(1.0, v_alpha * 1.2)
                vy_anim = vy * min(1.0, v_alpha * 1.2)
                vz_anim = vz * min(1.0, v_alpha * 1.2)

                # Create 3D arrow using Arrow3D class
                arrow = Arrow3D([0, vx_anim], [0, vy_anim], [0, vz_anim],
                              mutation_scale=15 * scale, linewidth=2.5 * scale,
                              arrowstyle='-|>', color=color, alpha=v_alpha)
                self.ax.add_artist(arrow)

                # Label at tip
                if label and v_alpha > 0.5:
                    self.ax.text(vx + 0.3, vy + 0.3, vz + 0.3, label,
                               fontsize=12 * scale, color=color, fontweight='bold',
                               alpha=v_alpha)

    def _render_vector_3d_projected(self, elem: Dict, x: float, y: float, alpha: float, speed: float, scale: float = 1.0) -> None:
        """Fallback: Render 3D vectors using 2D projection."""
        w, h = elem.get('width', 30) * scale, elem.get('height', 25) * scale

        elev = elem.get('camera_elev', 20)
        azim = elem.get('camera_azim', 45)
        rotate_camera = elem.get('rotate_camera', False)
        rotation_speed = elem.get('camera_rotation_speed', 30)

        if rotate_camera:
            # Use global progress for continuous rotation, apply speed multiplier
            azim = (azim + self._global_progress * rotation_speed * speed * 10) % 360

        elev_rad = np.radians(elev)
        azim_rad = np.radians(azim)

        # Background box
        self.ax.add_patch(FancyBboxPatch((x - w/2, y - h/2), w, h,
                                        boxstyle="round,pad=0.2",
                                        facecolor='#0d0d14',
                                        edgecolor=self.colors['dim'],
                                        linewidth=1.5, alpha=alpha))

        cx, cy = x, y

        vectors = elem.get('vectors', [])
        if not vectors:
            vectors = [
                {'x': 4, 'y': 2, 'z': 3, 'color': 'warning', 'label': 'v1'},
                {'x': -3, 'y': 4, 'z': 1, 'color': 'success', 'label': 'v2'},
                {'x': 2, 'y': -2, 'z': 4, 'color': 'accent', 'label': 'v3'}
            ]

        xs = [abs(vec.get('x', 0)) for vec in vectors if isinstance(vec, dict)]
        ys = [abs(vec.get('y', 0)) for vec in vectors if isinstance(vec, dict)]
        zs = [abs(vec.get('z', 0)) for vec in vectors if isinstance(vec, dict)]
        max_range = max(max(xs, default=1), max(ys, default=1), max(zs, default=1), 1)

        scale_factor = min(w, h) * 0.35 / max_range
        origin = self._render_3d_axes(cx, cy, scale_factor, elev_rad, azim_rad, alpha, scale)

        stagger = elem.get('stagger', True)

        projected_vectors = []
        for i, vec in enumerate(vectors[:15]):
            v_alpha = self._stagger_alpha(alpha, i, len(vectors), stagger)
            if v_alpha > 0:
                vz = vec.get('z', 0)
                color = self.colors.get(vec.get('color', 'accent'), self.colors['accent'])
                label = vec.get('label', '')

                proj = self._project_3d(vx * v_alpha, vy * v_alpha, vz * v_alpha,
                                       elev_rad, azim_rad, cx, cy, scale_factor)
                projected_vectors.append((proj, color, label, v_alpha))

        projected_vectors.sort(key=lambda v: v[0][2])

        for proj, color, label, v_alpha in projected_vectors:
            self.ax.annotate('', xy=(proj[0], proj[1]), xytext=(origin[0], origin[1]),
                           arrowprops=dict(arrowstyle='->', lw=2 * scale, color=color,
                                          shrinkA=0, shrinkB=0))
            if label and v_alpha > 0.5:
                self.ax.text(proj[0] + 1.5, proj[1] + 1, label[:12],
                           fontsize=7 * scale, color=color, alpha=v_alpha, fontweight='bold')

    # =========================================================================
    # Image Element
    # =========================================================================

    def _render_image(self, elem: Dict, x: float, y: float, alpha: float, speed: float, scale: float = 1.0) -> None:
        """Render an image element."""
        import os
        from matplotlib.offsetbox import OffsetImage, AnnotationBbox

        # Check if we're on a 3D axes - images don't work well in 3D
        is_3d = isinstance(self.ax, Axes3D)
        if is_3d:
            # Just show a simple text marker for 3D axes
            src = elem.get('src', '')
            label = f"[IMG: {src[:15]}...]" if len(src) > 15 else f"[IMG: {src}]"
            self.ax.text(x, y, 0, label, fontsize=8 * scale, ha='center',
                        color=self.colors['warning'], alpha=alpha)
            return

        src = elem.get('src', '')
        w = elem.get('width', 20) * scale
        h = elem.get('height', 15) * scale

        if not src or not os.path.exists(src):
            # Show placeholder if image not found
            self.ax.add_patch(FancyBboxPatch((x - w/2, y - h/2), w, h,
                                            boxstyle="round,pad=0.2",
                                            facecolor=self.colors['bg_light'],
                                            edgecolor=self.colors['warning'],
                                            linewidth=1.5, linestyle='--', alpha=alpha))
            self.ax.text(x, y, f"Image: {src[:20]}..." if len(src) > 20 else f"Image: {src}",
                        fontsize=8 * scale, ha='center', color=self.colors['warning'], alpha=alpha)
            return

        try:
            img = plt.imread(src)

            # Calculate zoom to fit desired size (approximate)
            img_h, img_w = img.shape[:2]
            target_size = min(w, h) * 5  # Scale factor for display
            zoom = target_size / max(img_w, img_h)

            imagebox = OffsetImage(img, zoom=zoom, alpha=alpha)
            ab = AnnotationBbox(imagebox, (x, y), frameon=False, pad=0)
            self.ax.add_artist(ab)

            # Optional border
            if elem.get('border', False):
                border_color = elem.get('border_color', self.colors['dim'])
                if isinstance(border_color, str) and not border_color.startswith('#'):
                    border_color = self.colors.get(border_color, border_color)
                self.ax.add_patch(FancyBboxPatch((x - w/2, y - h/2), w, h,
                                                boxstyle="round,pad=0.1",
                                                facecolor='none',
                                                edgecolor=border_color,
                                                linewidth=2, alpha=alpha))

            # Optional shadow
            if elem.get('shadow', False):
                self._add_shadow(x, y, w, h, alpha)

        except Exception as e:
            # Show error placeholder
            self.ax.add_patch(FancyBboxPatch((x - w/2, y - h/2), w, h,
                                            boxstyle="round,pad=0.2",
                                            facecolor=self.colors['bg_light'],
                                            edgecolor=self.colors['warning'],
                                            linewidth=1.5, alpha=alpha))
            self.ax.text(x, y, f"Error: {str(e)[:20]}", fontsize=8 * scale,
                        ha='center', color=self.colors['warning'], alpha=alpha)

    # =========================================================================
    # Generic Fallback
    # =========================================================================

    def _render_generic(self, elem: Dict, x: float, y: float, alpha: float, scale: float = 1.0) -> None:
        w, h = elem.get('width', 15) * scale, elem.get('height', 10) * scale
        elem_type = elem.get('type', 'unknown')
        self.ax.add_patch(FancyBboxPatch((x - w/2, y - h/2), w, h,
                                        boxstyle="round,pad=0.2",
                                        facecolor=self.colors['bg_light'],
                                        edgecolor=self.colors['dim'],
                                        linewidth=1.5, linestyle='--', alpha=alpha))
        self.ax.text(x, y, elem_type[:15], fontsize=9 * scale, ha='center',
                    color=self.colors['dim'], alpha=alpha)

    # =========================================================================
    # Training Visualization Elements
    # These elements consume TrainingState data for interactive visualizations
    # =========================================================================

    def _render_loss_curve(self, elem: Dict, x: float, y: float, alpha: float, speed: float, scale: float = 1.0) -> None:
        """
        Render an animated loss curve chart.

        Properties:
            - values: List of loss values (or pulled from training_state)
            - val_values: Optional validation loss values
            - animate_draw: Whether to animate the line drawing
            - show_grid: Show grid lines
            - show_min: Highlight minimum point
            - y_range: Optional (min, max) for y-axis
            - line_color, val_line_color: Line colors
        """
        w = elem.get('width', 40) * scale
        h = elem.get('height', 25) * scale

        # Get data from element or training state
        values = elem.get('values', elem.get('loss_history', []))
        val_values = elem.get('val_values', elem.get('val_loss_history', []))

        if not values:
            values = [1.0, 0.8, 0.5, 0.3, 0.2, 0.15, 0.1, 0.08, 0.06, 0.05]  # Demo data

        # Chart bounds
        left, right = x - w/2, x + w/2
        bottom, top = y - h/2, y + h/2

        # Background
        self.ax.add_patch(FancyBboxPatch((left, bottom), w, h,
                                        boxstyle="round,pad=0.02",
                                        facecolor=self.colors['bg_light'],
                                        edgecolor=self.colors['dim'],
                                        linewidth=1.5, alpha=alpha * 0.9))

        # Grid
        if elem.get('show_grid', True):
            for i in range(5):
                gy = bottom + (i + 1) * h / 6
                self.ax.plot([left + 5, right - 5], [gy, gy],
                            color=self.colors['dim'], linewidth=0.5, alpha=alpha * 0.3)

        # Calculate y range
        y_range = elem.get('y_range')
        if y_range:
            y_min, y_max = y_range
        else:
            all_vals = values + (val_values if val_values else [])
            y_min, y_max = min(all_vals) * 0.9, max(all_vals) * 1.1
            if y_min == y_max:
                y_min, y_max = 0, y_max * 1.2

        # Animation - how much of the curve to show
        animate_draw = elem.get('animate_draw', True)
        draw_progress = speed if animate_draw else 1.0
        num_points_to_show = max(1, int(len(values) * draw_progress))

        # Plot loss curve
        if len(values) >= 2:
            chart_left, chart_right = left + 8, right - 8
            chart_bottom, chart_top = bottom + 8, top - 15

            visible_values = values[:num_points_to_show]
            xs = [chart_left + (i / (len(values) - 1)) * (chart_right - chart_left)
                  for i in range(len(visible_values))]
            ys = [chart_bottom + ((v - y_min) / (y_max - y_min)) * (chart_top - chart_bottom)
                  for v in visible_values]

            line_color = elem.get('line_color', self.colors['primary'])
            if isinstance(line_color, str) and not line_color.startswith('#'):
                line_color = self.colors.get(line_color, line_color)

            self.ax.plot(xs, ys, color=line_color, linewidth=2.5 * scale, alpha=alpha)

            # Validation loss
            if val_values and len(val_values) >= 2:
                val_visible = val_values[:num_points_to_show]
                val_xs = xs[:len(val_visible)]
                val_ys = [chart_bottom + ((v - y_min) / (y_max - y_min)) * (chart_top - chart_bottom)
                          for v in val_visible]
                val_color = elem.get('val_line_color', self.colors['warning'])
                if isinstance(val_color, str) and not val_color.startswith('#'):
                    val_color = self.colors.get(val_color, val_color)
                self.ax.plot(val_xs, val_ys, color=val_color, linewidth=2 * scale,
                            linestyle='--', alpha=alpha * 0.8)

            # Highlight minimum
            if elem.get('show_min', True) and draw_progress >= 1.0:
                min_idx = np.argmin(visible_values)
                self.ax.scatter([xs[min_idx]], [ys[min_idx]], s=60 * scale,
                               color=self.colors['success'], zorder=10, alpha=alpha)

            # Current point (animated endpoint)
            if animate_draw and len(visible_values) > 0:
                self.ax.scatter([xs[-1]], [ys[-1]], s=80 * scale,
                               color=line_color, zorder=10, alpha=alpha,
                               edgecolors='white', linewidths=2)

        # Title
        title = elem.get('title', 'Loss')
        self.ax.text(x, top - 5, title, fontsize=11 * scale, ha='center',
                    color=self.colors['text'], alpha=alpha, weight='bold')

        # Y-axis labels
        self.ax.text(left + 3, bottom + 8, f"{y_min:.2f}", fontsize=7 * scale,
                    ha='left', va='bottom', color=self.colors['dim'], alpha=alpha)
        self.ax.text(left + 3, top - 15, f"{y_max:.2f}", fontsize=7 * scale,
                    ha='left', va='top', color=self.colors['dim'], alpha=alpha)

    def _render_decision_boundary_2d(self, elem: Dict, x: float, y: float, alpha: float, speed: float, scale: float = 1.0) -> None:
        """
        Render a 2D decision boundary visualization.

        Properties:
            - points: List of {x, y, label} points
            - boundary_resolution: Grid resolution for boundary
            - animate_training: Animate boundary evolution
            - show_margin: Show decision margin
            - class_colors: Dict mapping labels to colors
        """
        w = elem.get('width', 35) * scale
        h = elem.get('height', 30) * scale

        left, right = x - w/2, x + w/2
        bottom, top = y - h/2, y + h/2

        # Background
        self.ax.add_patch(FancyBboxPatch((left, bottom), w, h,
                                        boxstyle="round,pad=0.02",
                                        facecolor='#0a0a12',
                                        edgecolor=self.colors['dim'],
                                        linewidth=1.5, alpha=alpha * 0.9))

        # Get points
        points = elem.get('points', [])
        if not points:
            # XOR demo data
            points = [
                {'x': 0, 'y': 0, 'label': 0},
                {'x': 0, 'y': 1, 'label': 1},
                {'x': 1, 'y': 0, 'label': 1},
                {'x': 1, 'y': 1, 'label': 0},
            ]

        # Calculate data bounds
        xs = [p['x'] for p in points]
        ys = [p['y'] for p in points]
        data_x_range = (min(xs) - 0.3, max(xs) + 0.3)
        data_y_range = (min(ys) - 0.3, max(ys) + 0.3)

        # Map data coords to chart coords
        chart_left, chart_right = left + 5, right - 5
        chart_bottom, chart_top = bottom + 5, top - 12

        def to_chart_x(dx):
            return chart_left + ((dx - data_x_range[0]) / (data_x_range[1] - data_x_range[0])) * (chart_right - chart_left)

        def to_chart_y(dy):
            return chart_bottom + ((dy - data_y_range[0]) / (data_y_range[1] - data_y_range[0])) * (chart_top - chart_bottom)

        # Decision boundary (if provided)
        boundary = elem.get('decision_boundary')
        if boundary is not None and len(boundary) > 0:
            # boundary is a 2D grid of predictions
            res = len(boundary)
            for i in range(res):
                for j in range(res):
                    bx = data_x_range[0] + (i / (res-1)) * (data_x_range[1] - data_x_range[0])
                    by = data_y_range[0] + (j / (res-1)) * (data_y_range[1] - data_y_range[0])
                    pred = boundary[i][j] if isinstance(boundary[i], list) else boundary[i, j]
                    color = self.colors['primary'] if pred > 0.5 else self.colors['warning']
                    cx, cy = to_chart_x(bx), to_chart_y(by)
                    cell_w = (chart_right - chart_left) / res
                    cell_h = (chart_top - chart_bottom) / res
                    self.ax.add_patch(Rectangle((cx - cell_w/2, cy - cell_h/2), cell_w, cell_h,
                                               facecolor=color, alpha=alpha * 0.15))

        # Plot points
        class_colors = elem.get('class_colors', {0: self.colors['warning'], 1: self.colors['primary']})
        for p in points:
            px, py = to_chart_x(p['x']), to_chart_y(p['y'])
            label = p.get('label', 0)
            color = class_colors.get(label, self.colors['accent'])
            if isinstance(color, str) and not color.startswith('#'):
                color = self.colors.get(color, color)
            marker = 'o' if label == 0 else 's'
            self.ax.scatter([px], [py], s=100 * scale, c=[color],
                           marker=marker, edgecolors='white', linewidths=2, alpha=alpha, zorder=5)

        # Title
        title = elem.get('title', 'Decision Boundary')
        self.ax.text(x, top - 3, title, fontsize=10 * scale, ha='center',
                    color=self.colors['text'], alpha=alpha, weight='bold')

    def _render_xor_problem(self, elem: Dict, x: float, y: float, alpha: float, speed: float, scale: float = 1.0) -> None:
        """
        Render the classic XOR problem visualization.

        This is a specialized decision_boundary_2d with XOR-specific features.

        Properties:
            - epoch: Current training epoch
            - show_linear_attempt: Show why linear fails
            - show_hidden_space: Show hidden layer transformation
            - decision_boundary: 2D grid of predictions
            - weights: Network weights for visualization
        """
        w = elem.get('width', 40) * scale
        h = elem.get('height', 35) * scale

        # XOR points
        xor_points = [
            {'x': 0, 'y': 0, 'label': 0, 'expected': 0},
            {'x': 0, 'y': 1, 'label': 1, 'expected': 1},
            {'x': 1, 'y': 0, 'label': 1, 'expected': 1},
            {'x': 1, 'y': 1, 'label': 0, 'expected': 0},
        ]

        # Delegate to decision_boundary_2d with XOR data
        elem_copy = dict(elem)
        elem_copy['points'] = xor_points
        elem_copy['title'] = elem.get('title', 'XOR Problem')
        elem_copy['width'] = w / scale
        elem_copy['height'] = h / scale

        self._render_decision_boundary_2d(elem_copy, x, y, alpha, speed, scale)

        # Add epoch indicator if training
        epoch = elem.get('epoch', 0)
        total_epochs = elem.get('total_epochs', 100)
        if epoch > 0:
            bottom = y - h/2
            self.ax.text(x, bottom + 3, f"Epoch: {epoch}/{total_epochs}",
                        fontsize=8 * scale, ha='center', color=self.colors['dim'], alpha=alpha)

    def _render_gradient_flow(self, elem: Dict, x: float, y: float, alpha: float, speed: float, scale: float = 1.0) -> None:
        """
        Render gradient flow through network layers.

        Properties:
            - layers: List of layer sizes [3, 5, 5, 2]
            - gradient_magnitudes: List of gradient magnitudes per layer
            - animate_flow: Animate gradient flowing backward
            - show_vanishing: Highlight vanishing gradients
            - flow_direction: 'backward' or 'forward'
        """
        w = elem.get('width', 50) * scale
        h = elem.get('height', 20) * scale

        layers = elem.get('layers', [3, 5, 5, 2])
        n_layers = len(layers)

        left, right = x - w/2, x + w/2
        bottom, top = y - h/2, y + h/2

        # Background
        self.ax.add_patch(FancyBboxPatch((left, bottom), w, h,
                                        boxstyle="round,pad=0.02",
                                        facecolor=self.colors['bg_light'],
                                        edgecolor=self.colors['dim'],
                                        linewidth=1.5, alpha=alpha * 0.9))

        # Gradient magnitudes (default: decaying gradients)
        grad_mags = elem.get('gradient_magnitudes', [1.0 / (i + 1) for i in range(n_layers)])

        # Layer positions
        layer_spacing = (w - 20) / (n_layers - 1) if n_layers > 1 else 0
        layer_x = [left + 10 + i * layer_spacing for i in range(n_layers)]

        # Animation progress
        animate = elem.get('animate_flow', True)
        flow_progress = speed if animate else 1.0

        # Draw layers and gradients
        max_nodes = max(layers)
        for i, (lx, n_nodes) in enumerate(zip(layer_x, layers)):
            node_spacing = (h - 15) / max(n_nodes, 1)
            start_y = y - (n_nodes - 1) * node_spacing / 2

            # Gradient magnitude for this layer
            grad_mag = grad_mags[i] if i < len(grad_mags) else 0.1

            for j in range(n_nodes):
                ny = start_y + j * node_spacing

                # Node color based on gradient magnitude
                if elem.get('show_vanishing', True) and grad_mag < 0.1:
                    node_color = self.colors['warning']  # Vanishing
                elif grad_mag > 0.8:
                    node_color = self.colors['success']  # Strong
                else:
                    node_color = self.colors['primary']

                self.ax.scatter([lx], [ny], s=60 * scale * (0.5 + grad_mag * 0.5),
                               c=[node_color], alpha=alpha * (0.4 + grad_mag * 0.6), zorder=5)

            # Draw gradient arrows between layers
            if i < n_layers - 1:
                # Gradient flows backward (right to left)
                arrow_alpha = alpha * grad_mags[i] if i < len(grad_mags) else alpha * 0.3

                # Animation: arrows appear progressively
                layer_progress = (flow_progress * n_layers - (n_layers - 1 - i))
                if layer_progress > 0:
                    arrow_alpha *= min(1.0, layer_progress)

                    mid_y = y
                    from_x, to_x = layer_x[i + 1] - 5, lx + 5

                    # Arrow width based on gradient magnitude
                    arrow_width = 1 + grad_mag * 3

                    self.ax.annotate('', xy=(to_x, mid_y), xytext=(from_x, mid_y),
                                    arrowprops=dict(arrowstyle='->', color=self.colors['accent'],
                                                   lw=arrow_width * scale, alpha=arrow_alpha))

        # Title
        title = elem.get('title', 'Gradient Flow')
        self.ax.text(x, top - 3, title, fontsize=10 * scale, ha='center',
                    color=self.colors['text'], alpha=alpha, weight='bold')

        # Legend
        self.ax.text(right - 5, bottom + 3, "← Backprop", fontsize=7 * scale,
                    ha='right', color=self.colors['accent'], alpha=alpha * 0.7)

    def _render_dropout_layer(self, elem: Dict, x: float, y: float, alpha: float, speed: float, scale: float = 1.0) -> None:
        """
        Render dropout visualization with nodes randomly dropping.

        Properties:
            - num_nodes: Number of nodes to show
            - dropout_rate: Fraction of nodes to drop (0-1)
            - animate_drops: Animate dropping over time
            - seed: Random seed for reproducibility
            - show_scaling: Show output scaling annotation
        """
        w = elem.get('width', 30) * scale
        h = elem.get('height', 20) * scale

        num_nodes = elem.get('num_nodes', 8)
        dropout_rate = elem.get('dropout_rate', 0.3)

        left, right = x - w/2, x + w/2
        bottom, top = y - h/2, y + h/2

        # Background
        self.ax.add_patch(FancyBboxPatch((left, bottom), w, h,
                                        boxstyle="round,pad=0.02",
                                        facecolor=self.colors['bg_light'],
                                        edgecolor=self.colors['dim'],
                                        linewidth=1.5, alpha=alpha * 0.9))

        # Determine which nodes are dropped
        seed = elem.get('seed', 42)
        animate = elem.get('animate_drops', True)
        if animate:
            # Change dropped nodes based on animation progress
            seed = int(seed + speed * 100) % 10000
        np.random.seed(seed)
        dropped = np.random.random(num_nodes) < dropout_rate

        # Node positions (two rows)
        cols = (num_nodes + 1) // 2
        node_positions = []
        for i in range(num_nodes):
            row = i // cols
            col = i % cols
            nx = left + 15 + col * ((w - 30) / max(cols - 1, 1)) if cols > 1 else x
            ny = y + 5 - row * 12
            node_positions.append((nx, ny))

        # Draw nodes
        for i, (nx, ny) in enumerate(node_positions):
            if dropped[i]:
                # Dropped node - X mark
                self.ax.scatter([nx], [ny], s=80 * scale, marker='x',
                               c=[self.colors['warning']], alpha=alpha * 0.6, linewidths=2)
            else:
                # Active node
                self.ax.scatter([nx], [ny], s=80 * scale, marker='o',
                               c=[self.colors['primary']], alpha=alpha,
                               edgecolors='white', linewidths=1.5)

        # Title
        title = elem.get('title', f'Dropout (p={dropout_rate})')
        self.ax.text(x, top - 3, title, fontsize=10 * scale, ha='center',
                    color=self.colors['text'], alpha=alpha, weight='bold')

        # Scaling annotation
        if elem.get('show_scaling', True):
            scale_factor = 1.0 / (1.0 - dropout_rate) if dropout_rate < 1 else float('inf')
            self.ax.text(x, bottom + 3, f"Scale: ×{scale_factor:.2f}",
                        fontsize=8 * scale, ha='center', color=self.colors['dim'], alpha=alpha * 0.8)

    def _render_optimizer_paths(self, elem: Dict, x: float, y: float, alpha: float, speed: float, scale: float = 1.0) -> None:
        """
        Render optimizer trajectory comparison on a loss surface.

        Properties:
            - optimizers: List of {name, path, color}
            - surface_type: 'convex', 'saddle', 'local_minima'
            - animate_paths: Animate trajectories
            - show_contours: Show loss contours
            - show_labels: Show optimizer names
        """
        w = elem.get('width', 40) * scale
        h = elem.get('height', 35) * scale

        left, right = x - w/2, x + w/2
        bottom, top = y - h/2, y + h/2

        # Background
        self.ax.add_patch(FancyBboxPatch((left, bottom), w, h,
                                        boxstyle="round,pad=0.02",
                                        facecolor='#0a0a12',
                                        edgecolor=self.colors['dim'],
                                        linewidth=1.5, alpha=alpha * 0.9))

        chart_left, chart_right = left + 8, right - 8
        chart_bottom, chart_top = bottom + 8, top - 15

        # Draw contour lines (simplified ellipses for convex surface)
        surface_type = elem.get('surface_type', 'convex')
        center_x, center_y = x, y - 5
        if elem.get('show_contours', True):
            for r in [5, 10, 15, 20, 25]:
                ellipse = plt.matplotlib.patches.Ellipse(
                    (center_x, center_y), r * scale * 1.5, r * scale,
                    fill=False, edgecolor=self.colors['dim'], alpha=alpha * 0.3, linewidth=1
                )
                self.ax.add_patch(ellipse)

        # Default optimizer paths
        optimizers = elem.get('optimizers', [
            {'name': 'SGD', 'color': 'warning', 'path': [(-15, 12), (-10, 8), (-5, 5), (-2, 2), (0, 0)]},
            {'name': 'Adam', 'color': 'success', 'path': [(-15, -8), (-8, -4), (-2, -1), (0, 0)]},
            {'name': 'RMSprop', 'color': 'primary', 'path': [(15, 10), (8, 6), (3, 2), (0, 0)]},
        ])

        # Animation
        animate = elem.get('animate_paths', True)

        for opt in optimizers:
            path = opt.get('path', [])
            if len(path) < 2:
                continue

            color = opt.get('color', 'primary')
            if isinstance(color, str) and not color.startswith('#'):
                color = self.colors.get(color, color)

            # Convert path to chart coords
            path_x = [center_x + p[0] * scale for p in path]
            path_y = [center_y + p[1] * scale for p in path]

            # Animate - show partial path
            if animate:
                show_points = max(2, int(len(path) * speed))
            else:
                show_points = len(path)

            self.ax.plot(path_x[:show_points], path_y[:show_points],
                        color=color, linewidth=2 * scale, alpha=alpha)

            # Current position
            if show_points > 0:
                self.ax.scatter([path_x[show_points-1]], [path_y[show_points-1]],
                               s=60 * scale, c=[color], alpha=alpha,
                               edgecolors='white', linewidths=1.5, zorder=5)

            # Label
            if elem.get('show_labels', True):
                self.ax.text(path_x[0], path_y[0] + 3, opt.get('name', ''),
                            fontsize=7 * scale, ha='center', color=color, alpha=alpha)

        # Minimum point
        self.ax.scatter([center_x], [center_y], s=100 * scale, marker='*',
                       c=[self.colors['accent']], alpha=alpha, zorder=10)

        # Title
        title = elem.get('title', 'Optimizer Comparison')
        self.ax.text(x, top - 3, title, fontsize=10 * scale, ha='center',
                    color=self.colors['text'], alpha=alpha, weight='bold')

    def _render_confusion_matrix(self, elem: Dict, x: float, y: float, alpha: float, speed: float, scale: float = 1.0) -> None:
        """
        Render an animated confusion matrix.

        Properties:
            - matrix: 2D list of values
            - labels: Class labels
            - animate_fill: Animate cells filling
            - show_percentages: Show percentage values
            - colormap: Color scheme
        """
        w = elem.get('width', 30) * scale
        h = elem.get('height', 30) * scale

        matrix = elem.get('matrix', [[45, 5], [8, 42]])
        labels = elem.get('labels', ['Neg', 'Pos'])
        n_classes = len(matrix)

        left, right = x - w/2, x + w/2
        bottom, top = y - h/2, y + h/2

        # Background
        self.ax.add_patch(FancyBboxPatch((left, bottom), w, h,
                                        boxstyle="round,pad=0.02",
                                        facecolor=self.colors['bg_light'],
                                        edgecolor=self.colors['dim'],
                                        linewidth=1.5, alpha=alpha * 0.9))

        # Cell dimensions
        chart_left, chart_top = left + 15, top - 15
        cell_w = (w - 25) / n_classes
        cell_h = (h - 25) / n_classes

        # Find max for normalization
        max_val = max(max(row) for row in matrix)

        # Animation
        animate = elem.get('animate_fill', True)

        # Draw cells
        for i in range(n_classes):
            for j in range(n_classes):
                cx = chart_left + j * cell_w
                cy = chart_top - (i + 1) * cell_h

                val = matrix[i][j]
                intensity = val / max_val if max_val > 0 else 0

                # Animation - fade in
                if animate:
                    intensity *= min(1.0, speed * 2)

                # Color: diagonal (correct) = green, off-diagonal = red
                if i == j:
                    color = self.colors['success']
                else:
                    color = self.colors['warning']

                self.ax.add_patch(Rectangle((cx, cy), cell_w - 1, cell_h - 1,
                                           facecolor=color, alpha=alpha * intensity * 0.7))
                self.ax.add_patch(Rectangle((cx, cy), cell_w - 1, cell_h - 1,
                                           fill=False, edgecolor=self.colors['dim'],
                                           linewidth=1, alpha=alpha))

                # Value text
                if elem.get('show_percentages', False):
                    total = sum(sum(row) for row in matrix)
                    text = f"{val/total*100:.0f}%"
                else:
                    text = str(val)

                self.ax.text(cx + cell_w/2 - 0.5, cy + cell_h/2 - 0.5, text,
                            fontsize=9 * scale, ha='center', va='center',
                            color='white' if intensity > 0.5 else self.colors['text'],
                            alpha=alpha)

        # Labels
        for i, label in enumerate(labels):
            # Row label (left)
            self.ax.text(chart_left - 3, chart_top - (i + 0.5) * cell_h,
                        label[:4], fontsize=8 * scale, ha='right', va='center',
                        color=self.colors['text'], alpha=alpha)
            # Column label (top)
            self.ax.text(chart_left + (i + 0.5) * cell_w, chart_top + 2,
                        label[:4], fontsize=8 * scale, ha='center',
                        color=self.colors['text'], alpha=alpha)

        # Title
        title = elem.get('title', 'Confusion Matrix')
        self.ax.text(x, top - 3, title, fontsize=10 * scale, ha='center',
                    color=self.colors['text'], alpha=alpha, weight='bold')


def render_step(ax: Axes, step_data: Dict, progress: float,
                colors: Optional[Dict[str, str]] = None,
                show_title: bool = True,
                show_phase_markers: bool = False,
                step_transition: str = 'none',
                transition_progress: float = 1.0) -> None:
    """
    Convenience function to render a complete step.

    Args:
        ax: Matplotlib axes (2D or 3D)
        step_data: Step dictionary with 'elements', 'title', etc.
        progress: Animation progress 0-1
        colors: Optional color override
        show_title: Whether to show step title
        show_phase_markers: Whether to show phase indicator at bottom
        step_transition: Transition type ('none', 'fade', 'slide_left', 'slide_right', 'zoom')
        transition_progress: Progress of the step transition 0-1 (1 = fully visible)
    """
    colors = colors or COLORS

    # Check if we're on 3D axes
    is_3d = hasattr(ax, 'get_zlim')

    ax.clear()

    if is_3d:
        # 3D axes setup - let individual elements set their own limits
        ax.set_facecolor(colors.get('bg', '#0a0a0a'))
        # Show title differently for 3D
        if show_title:
            title = step_data.get('title', '')
            if title:
                # Use figure-level text for 3D (since ax.text in 3D is positioned in 3D space)
                ax.figure.suptitle(title, fontsize=18, fontweight='bold',
                                  color=colors.get('primary', '#3B82F6'))
    else:
        # 2D axes setup
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

    # Apply step-level transition
    step_alpha = 1.0
    step_offset_x = 0
    step_offset_y = 0
    step_scale = 1.0

    if step_transition != 'none' and transition_progress < 1.0:
        # Ease the transition
        t = transition_progress
        eased = 1 - (1 - t) ** 3  # ease out cubic

        if step_transition == 'fade':
            step_alpha = eased
        elif step_transition == 'slide_left':
            step_offset_x = -50 * (1 - eased)
            step_alpha = eased
        elif step_transition == 'slide_right':
            step_offset_x = 50 * (1 - eased)
            step_alpha = eased
        elif step_transition == 'slide_up':
            step_offset_y = 50 * (1 - eased)
            step_alpha = eased
        elif step_transition == 'slide_down':
            step_offset_y = -50 * (1 - eased)
            step_alpha = eased
        elif step_transition == 'zoom':
            step_scale = 0.5 + 0.5 * eased
            step_alpha = eased

    # Render elements with step transition applied
    renderer = ElementRenderer(ax, colors)
    for elem in step_data.get('elements', []):
        # Apply step-level transforms to element
        if step_transition != 'none' and transition_progress < 1.0:
            # Modify element position temporarily
            original_pos = elem.get('position', {'x': 50, 'y': 50})
            elem = dict(elem)  # Don't modify original
            elem['position'] = {
                'x': original_pos['x'] + step_offset_x,
                'y': original_pos['y'] + step_offset_y
            }
            # Apply step alpha as a multiplier (element will fade with step)
            elem['_step_alpha'] = step_alpha
            elem['_step_scale'] = step_scale

        renderer.render(elem, progress)

    # Phase markers (only for 2D)
    if show_phase_markers and not is_3d:
        phases = [('imm', 0.0), ('early', 0.2), ('mid', 0.4), ('late', 0.6), ('final', 0.8)]
        for name, start in phases:
            x = 10 + start * 80
            color = colors.get('accent', '#F59E0B') if progress >= start else colors.get('dim', '#6B7280')
            ax.plot([x, x], [2, 5], color=color, linewidth=2)
            ax.text(x, 1, name, fontsize=7, ha='center', color=color)
        ax.axhline(y=3.5, xmin=0.1, xmax=0.1 + 0.8 * progress,
                  color=colors.get('primary', '#3B82F6'), linewidth=3)
