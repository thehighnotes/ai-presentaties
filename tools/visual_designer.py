#!/usr/bin/env python3
"""
Visual Presentation Designer v7
Element thumbnails, full preview with animations, undo/redo support
"""

import sys
from pathlib import Path
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Circle, Rectangle, Wedge
import numpy as np
from tkinter import Tk, filedialog, simpledialog, messagebox
import copy
import json

sys.path.insert(0, str(Path(__file__).parent.parent))

from tools.schema import PresentationSchema, Step, LandingPage, SORTED_ELEMENTS
from core import PresentationStyle


class VisualDesigner:
    """Visual presentation designer with thumbnails, preview, and undo/redo"""

    # Use sorted elements from schema (type, name, icon)
    ELEMENTS = [(e[0], e[1]) for e in SORTED_ELEMENTS]
    ELEMENT_ICONS = {e[0]: e[2] for e in SORTED_ELEMENTS}

    # Panel colors
    PANEL_BG = '#0f0f14'
    PANEL_HEADER = '#1a1a24'
    PANEL_BORDER = '#2a2a3a'
    CANVAS_BG = '#0a0a0f'

    def __init__(self, schema_path: str = None):
        self.colors = PresentationStyle.COLORS

        # State
        self.current_step = 0
        self.selected_element = None
        self.dragging = False
        self.drag_offset = (0, 0)
        self.placing_element = None
        self.scroll_offset = 0
        self.unsaved = False

        # UI button regions (initialized here, populated in draw functions)
        self.elem_boxes = []
        self.prop_buttons = []
        self.phase_buttons = []
        self.easing_buttons = []
        self.effect_buttons = []
        self.slider_buttons = []
        self.nav_buttons = []
        self.tab_buttons = []

        # Properties panel tab state: 'props' or 'anim'
        self.props_tab = 'props'

        # Undo/Redo history (per step)
        self.undo_stack = []  # List of (step_index, elements_snapshot)
        self.redo_stack = []
        self.max_history = 50

        # Canvas zoom/pan state
        self.canvas_scale = 1.0
        self.canvas_offset = (0, 0)
        self.scaling = False
        self.scale_start = None

        # Preview state
        self.preview_fig = None
        self.preview_ax = None
        self.animation_progress = 0.0
        self.animation_playing = False
        self.animation_loop = False
        self.frame_time = 0.0  # Continuous time for effects
        self.particle_seeds = {}  # Store random seeds for consistent particle rendering

        # Load schema
        if schema_path and Path(schema_path).exists():
            self.schema = PresentationSchema.from_file(schema_path)
            self.schema_path = schema_path
        else:
            self.schema = self._create_empty_schema()
            self.schema_path = schema_path or "schemas/new_presentation.json"

        if not self.schema.steps:
            self.schema.steps.append(Step(name="Step 1", title="New Step", elements=[]))

        self._setup_ui()

    def _create_empty_schema(self):
        return PresentationSchema(
            name="new_presentation", title="New Presentation",
            landing=LandingPage(title="New Presentation"),
            steps=[]
        )

    def _save_undo_state(self):
        """Save current state to undo stack"""
        step = self._get_current_step()
        if step:
            # Deep copy elements as JSON to ensure full copy
            snapshot = json.loads(json.dumps([e for e in step.elements]))
            self.undo_stack.append((self.current_step, snapshot))
            if len(self.undo_stack) > self.max_history:
                self.undo_stack.pop(0)
            # Clear redo stack on new action
            self.redo_stack.clear()

    def _undo(self):
        """Undo last action"""
        if not self.undo_stack:
            print("Nothing to undo")
            return

        # Save current state to redo
        step = self._get_current_step()
        if step:
            snapshot = json.loads(json.dumps([e for e in step.elements]))
            self.redo_stack.append((self.current_step, snapshot))

        # Restore previous state
        step_idx, elements = self.undo_stack.pop()
        if step_idx < len(self.schema.steps):
            self.current_step = step_idx
            self.schema.steps[step_idx].elements = elements
            self.selected_element = None
            self.unsaved = True
            self._refresh_all()
            print(f"Undo: restored {len(elements)} elements")

    def _redo(self):
        """Redo last undone action"""
        if not self.redo_stack:
            print("Nothing to redo")
            return

        # Save current state to undo
        step = self._get_current_step()
        if step:
            snapshot = json.loads(json.dumps([e for e in step.elements]))
            self.undo_stack.append((self.current_step, snapshot))

        # Restore redo state
        step_idx, elements = self.redo_stack.pop()
        if step_idx < len(self.schema.steps):
            self.current_step = step_idx
            self.schema.steps[step_idx].elements = elements
            self.selected_element = None
            self.unsaved = True
            self._refresh_all()
            print(f"Redo: restored {len(elements)} elements")

    def _setup_ui(self):
        """Setup the UI with clear panel boundaries"""
        # Disable toolbar to prevent zoom conflicts with right-click
        plt.rcParams['toolbar'] = 'None'
        self.fig = plt.figure(figsize=(16, 9), facecolor='#08080c')
        self.fig.canvas.manager.set_window_title('Presentation Designer v7')

        # Disconnect default mouse handlers that conflict with our right-click zoom
        if hasattr(self.fig.canvas, 'toolbar') and self.fig.canvas.toolbar:
            self.fig.canvas.toolbar.pack_forget()

        # Layout:
        # Left panel: elements with thumbnails
        # Center: canvas
        # Right: properties (full height now, no mini preview)

        # Left panel: Elements with thumbnails (x: 0.01-0.18)
        self.ax_left = self.fig.add_axes([0.01, 0.08, 0.17, 0.84])

        # Center: Canvas (x: 0.20-0.74)
        self.ax_canvas = self.fig.add_axes([0.20, 0.12, 0.52, 0.76])

        # Right: Properties (x: 0.74-0.99, full height)
        self.ax_right = self.fig.add_axes([0.74, 0.08, 0.25, 0.84])

        # Top bar (spans full width)
        self.ax_top = self.fig.add_axes([0.01, 0.93, 0.98, 0.06])

        # Bottom bar (under canvas)
        self.ax_bottom = self.fig.add_axes([0.20, 0.02, 0.52, 0.08])

        # Style all panels
        for ax in [self.ax_left, self.ax_right, self.ax_top, self.ax_bottom]:
            ax.set_facecolor(self.PANEL_BG)
            for spine in ax.spines.values():
                spine.set_color(self.PANEL_BORDER)
                spine.set_linewidth(1.5)
            ax.set_xticks([])
            ax.set_yticks([])

        # Canvas special styling
        self.ax_canvas.set_facecolor(self.CANVAS_BG)
        for spine in self.ax_canvas.spines.values():
            spine.set_color(self.colors['primary'])
            spine.set_linewidth(2)

        # Draw static content
        self._draw_top_bar()
        self._draw_left_panel()
        self._draw_right_panel()
        self._draw_bottom_bar()
        self._draw_canvas()

        # Connect events
        self.fig.canvas.mpl_connect('button_press_event', self._on_click)
        self.fig.canvas.mpl_connect('button_release_event', self._on_release)
        self.fig.canvas.mpl_connect('motion_notify_event', self._on_motion)
        self.fig.canvas.mpl_connect('key_press_event', self._on_key)
        self.fig.canvas.mpl_connect('scroll_event', self._on_scroll)

    def _draw_top_bar(self):
        """Draw top menu bar"""
        ax = self.ax_top
        ax.clear()
        ax.set_facecolor(self.PANEL_HEADER)
        ax.set_xlim(0, 100)
        ax.set_ylim(0, 100)
        ax.axis('off')

        # Title
        ax.text(1, 50, 'PRESENTATION DESIGNER', fontsize=12, fontweight='bold',
                ha='left', va='center', color=self.colors['primary'])

        # Menu items - added Ctrl+Z hint
        menu = '[N]ew  [O]pen  [S]ave  [G]en  [P]review  |  Ctrl+Z Undo  Ctrl+Shift+Z Redo'
        ax.text(28, 50, menu, fontsize=9, ha='left', va='center',
                color=self.colors['text'], family='monospace')

        # Presentation name
        ax.text(99, 50, self.schema.title[:30], fontsize=11, ha='right',
                va='center', color=self.colors['accent'])

    def _draw_element_thumbnail(self, ax, elem_type, x, y, w, h, is_active=False):
        """Draw a small thumbnail representation of an element type"""
        # Background
        bg_color = self.colors['accent'] if is_active else '#1a1a24'
        border_color = self.colors['accent'] if is_active else '#2a2a3a'

        thumb_bg = Rectangle((x, y), w, h, facecolor=bg_color,
                             edgecolor=border_color, linewidth=1.5 if is_active else 1,
                             transform=ax.transAxes, clip_on=False)
        ax.add_patch(thumb_bg)

        # Center of thumbnail in axes coords
        cx, cy = x + w/2, y + h/2

        icon_color = 'white' if is_active else self.colors['accent']
        dim_color = 'white' if is_active else self.colors['dim']

        if elem_type == 'text':
            ax.text(cx, cy, 'Aa', fontsize=9, fontweight='bold',
                   ha='center', va='center', color=icon_color, transform=ax.transAxes)

        elif elem_type == 'typewriter_text':
            ax.text(cx - 0.02, cy, 'Ty', fontsize=8, fontweight='bold',
                   ha='center', va='center', color=icon_color, transform=ax.transAxes)
            ax.text(cx + 0.03, cy, '|', fontsize=10, fontweight='bold',
                   ha='center', va='center', color=self.colors['warning'], transform=ax.transAxes)

        elif elem_type == 'box':
            box = Rectangle((cx - 0.03, cy - 0.015), 0.06, 0.03,
                           facecolor='none', edgecolor=icon_color, linewidth=1.5,
                           transform=ax.transAxes)
            ax.add_patch(box)

        elif elem_type == 'bullet_list':
            for i, dy in enumerate([0.012, 0, -0.012]):
                ax.plot(cx - 0.025, cy + dy, 'o', markersize=2, color=icon_color, transform=ax.transAxes)
                ax.plot([cx - 0.01, cx + 0.03], [cy + dy, cy + dy], '-',
                       linewidth=1.5, color=dim_color, transform=ax.transAxes)

        elif elem_type == 'arrow':
            ax.annotate('', xy=(cx + 0.035, cy), xytext=(cx - 0.035, cy),
                       arrowprops=dict(arrowstyle='-|>', color=icon_color, lw=1.5),
                       xycoords=ax.transAxes, textcoords=ax.transAxes)

        elif elem_type == 'arc_arrow':
            ax.annotate('', xy=(cx + 0.03, cy), xytext=(cx - 0.03, cy),
                       arrowprops=dict(arrowstyle='-|>', color=icon_color, lw=1.5,
                                      connectionstyle='arc3,rad=0.3'),
                       xycoords=ax.transAxes, textcoords=ax.transAxes)

        elif elem_type == 'comparison':
            box1 = Rectangle((cx - 0.035, cy - 0.012), 0.03, 0.024,
                            facecolor='none', edgecolor=self.colors['warning'], linewidth=1,
                            transform=ax.transAxes)
            box2 = Rectangle((cx + 0.005, cy - 0.012), 0.03, 0.024,
                            facecolor='none', edgecolor=self.colors['success'], linewidth=1,
                            transform=ax.transAxes)
            ax.add_patch(box1)
            ax.add_patch(box2)

        elif elem_type == 'flow':
            for i, dx in enumerate([-0.025, 0.005, 0.035]):
                box = Rectangle((cx + dx - 0.012, cy - 0.008), 0.018, 0.016,
                               facecolor='none', edgecolor=icon_color, linewidth=1,
                               transform=ax.transAxes)
                ax.add_patch(box)

        elif elem_type == 'code_block':
            box = Rectangle((cx - 0.03, cy - 0.015), 0.06, 0.03,
                           facecolor='#0a0a12', edgecolor=icon_color, linewidth=1,
                           transform=ax.transAxes)
            ax.add_patch(box)
            ax.text(cx, cy, '</>', fontsize=6, ha='center', va='center',
                   color=self.colors['success'], transform=ax.transAxes, family='monospace')

        elif elem_type == 'grid':
            for r in range(2):
                for c in range(2):
                    gx = cx - 0.022 + c * 0.022
                    gy = cy - 0.012 + r * 0.014
                    cell = Rectangle((gx, gy), 0.018, 0.012,
                                    facecolor='none', edgecolor=icon_color, linewidth=0.8,
                                    transform=ax.transAxes)
                    ax.add_patch(cell)

        elif elem_type == 'checklist':
            for i, dy in enumerate([0.01, -0.01]):
                box = Rectangle((cx - 0.03, cy + dy - 0.005), 0.01, 0.01,
                               facecolor='none', edgecolor=icon_color, linewidth=1,
                               transform=ax.transAxes)
                ax.add_patch(box)
                ax.plot([cx - 0.01, cx + 0.03], [cy + dy, cy + dy], '-',
                       linewidth=1, color=dim_color, transform=ax.transAxes)

        elif elem_type == 'particle_flow':
            for i in range(5):
                px = cx - 0.03 + i * 0.015
                py = cy + np.sin(i * 0.8) * 0.008
                ax.plot(px, py, 'o', markersize=2, color=icon_color,
                       alpha=0.5 + i*0.1, transform=ax.transAxes)

        elif elem_type == 'similarity_meter':
            theta = np.linspace(0, np.pi, 20)
            r = 0.022
            xs = cx + r * np.cos(theta)
            ys = cy - 0.008 + r * np.sin(theta)
            ax.plot(xs, ys, '-', linewidth=2, color=icon_color, transform=ax.transAxes)

        elif elem_type == 'progress_bar':
            bar_bg = Rectangle((cx - 0.035, cy - 0.005), 0.07, 0.01,
                              facecolor='#1a1a24', edgecolor=icon_color, linewidth=1,
                              transform=ax.transAxes)
            ax.add_patch(bar_bg)
            bar_fill = Rectangle((cx - 0.035, cy - 0.005), 0.045, 0.01,
                                facecolor=self.colors['success'], edgecolor='none',
                                transform=ax.transAxes)
            ax.add_patch(bar_fill)

        elif elem_type == 'neural_network':
            layers = [[cy + 0.008, cy - 0.008], [cy + 0.012, cy, cy - 0.012], [cy]]
            layer_x = [cx - 0.022, cx, cx + 0.022]
            for lx, nodes in zip(layer_x, layers):
                for ny in nodes:
                    ax.plot(lx, ny, 'o', markersize=3, color=icon_color,
                           markeredgecolor='white', markeredgewidth=0.3, transform=ax.transAxes)

        elif elem_type == 'scatter_3d':
            ax.text(cx, cy, '3D', fontsize=8, fontweight='bold',
                   ha='center', va='center', color=icon_color, transform=ax.transAxes)

        elif elem_type == 'vector_3d':
            ax.text(cx, cy, 'v3', fontsize=8, fontweight='bold',
                   ha='center', va='center', color=icon_color, transform=ax.transAxes)
            ax.annotate('', xy=(cx + 0.02, cy + 0.01), xytext=(cx - 0.01, cy - 0.01),
                       arrowprops=dict(arrowstyle='->', color=icon_color, lw=1),
                       xycoords=ax.transAxes, textcoords=ax.transAxes)

        elif elem_type == 'code_execution':
            box1 = Rectangle((cx - 0.03, cy + 0.002), 0.06, 0.015,
                            facecolor='#0a0a12', edgecolor=icon_color, linewidth=0.8,
                            transform=ax.transAxes)
            box2 = Rectangle((cx - 0.03, cy - 0.018), 0.06, 0.015,
                            facecolor='#1a2e1a', edgecolor=self.colors['success'], linewidth=0.8,
                            transform=ax.transAxes)
            ax.add_patch(box1)
            ax.add_patch(box2)
            ax.annotate('', xy=(cx, cy - 0.005), xytext=(cx, cy),
                       arrowprops=dict(arrowstyle='->', color=self.colors['accent'], lw=0.8),
                       xycoords=ax.transAxes, textcoords=ax.transAxes)

        elif elem_type == 'conversation':
            # Chat bubbles
            b1 = Rectangle((cx - 0.03, cy + 0.005), 0.025, 0.012,
                          facecolor='#1a1a24', edgecolor=self.colors['primary'], linewidth=0.8,
                          transform=ax.transAxes)
            b2 = Rectangle((cx + 0.005, cy - 0.015), 0.025, 0.012,
                          facecolor='#1a1a24', edgecolor=self.colors['secondary'], linewidth=0.8,
                          transform=ax.transAxes)
            ax.add_patch(b1)
            ax.add_patch(b2)

        elif elem_type == 'timeline':
            ax.plot([cx - 0.03, cx + 0.03], [cy, cy], '-',
                   linewidth=1.5, color=icon_color, transform=ax.transAxes)
            for dx in [-0.02, 0, 0.02]:
                ax.plot(cx + dx, cy, 'o', markersize=3, color=icon_color, transform=ax.transAxes)

        elif elem_type == 'stacked_boxes':
            for i, w in enumerate([0.05, 0.04, 0.03]):
                dy = 0.01 - i * 0.012
                box = Rectangle((cx - w/2, cy + dy - 0.005), w, 0.01,
                               facecolor='#1a1a24', edgecolor=icon_color, linewidth=0.8,
                               transform=ax.transAxes)
                ax.add_patch(box)

        elif elem_type == 'attention_heatmap':
            # 2x2 heatmap
            for r in range(2):
                for c in range(2):
                    intensity = 0.8 if r == c else 0.3
                    gx = cx - 0.015 + c * 0.015
                    gy = cy - 0.015 + r * 0.015
                    cell = Rectangle((gx, gy), 0.013, 0.013,
                                    facecolor=plt.cm.viridis(intensity), edgecolor='#333', linewidth=0.3,
                                    transform=ax.transAxes)
                    ax.add_patch(cell)

        elif elem_type == 'token_flow':
            ax.text(cx, cy + 0.01, 'T', fontsize=6, ha='center', va='center',
                   color=icon_color, transform=ax.transAxes)
            ax.annotate('', xy=(cx, cy - 0.005), xytext=(cx, cy + 0.003),
                       arrowprops=dict(arrowstyle='->', color=self.colors['accent'], lw=0.8),
                       xycoords=ax.transAxes, textcoords=ax.transAxes)
            ax.text(cx, cy - 0.012, 'E', fontsize=6, ha='center', va='center',
                   color=self.colors['secondary'], transform=ax.transAxes)

        elif elem_type == 'model_comparison':
            ax.text(cx - 0.015, cy, 'A', fontsize=7, fontweight='bold',
                   ha='center', va='center', color=self.colors['primary'], transform=ax.transAxes)
            ax.plot([cx, cx], [cy - 0.015, cy + 0.015], '-',
                   linewidth=1, color=dim_color, transform=ax.transAxes)
            ax.text(cx + 0.015, cy, 'B', fontsize=7, fontweight='bold',
                   ha='center', va='center', color=self.colors['secondary'], transform=ax.transAxes)

        elif elem_type == 'parameter_slider':
            # Slider track
            ax.plot([cx - 0.025, cx + 0.025], [cy, cy], '-',
                   linewidth=2, color='#333', transform=ax.transAxes)
            # Fill
            ax.plot([cx - 0.025, cx], [cy, cy], '-',
                   linewidth=2, color=icon_color, transform=ax.transAxes)
            # Handle
            ax.plot(cx, cy, 'o', markersize=4, color='white',
                   markeredgecolor=icon_color, markeredgewidth=1, transform=ax.transAxes)

        elif elem_type == 'weight_comparison':
            ax.add_patch(Rectangle((cx - 0.03, cy + 0.003), 0.02, 0.008,
                                  facecolor=self.colors['warning'], edgecolor='none',
                                  transform=ax.transAxes))
            ax.add_patch(Rectangle((cx + 0.01, cy + 0.003), 0.025, 0.008,
                                  facecolor=self.colors['success'], edgecolor='none',
                                  transform=ax.transAxes))
            ax.add_patch(Rectangle((cx - 0.03, cy - 0.01), 0.015, 0.008,
                                  facecolor=self.colors['warning'], edgecolor='none',
                                  transform=ax.transAxes))
            ax.add_patch(Rectangle((cx + 0.01, cy - 0.01), 0.03, 0.008,
                                  facecolor=self.colors['success'], edgecolor='none',
                                  transform=ax.transAxes))

        else:
            # Use icon from ELEMENT_ICONS if available, else first 3 chars
            icon = self.ELEMENT_ICONS.get(elem_type, elem_type[:3])
            ax.text(cx, cy, icon, fontsize=7, ha='center', va='center',
                   color=icon_color, transform=ax.transAxes)

    def _draw_left_panel(self):
        """Draw elements panel with thumbnails"""
        ax = self.ax_left
        ax.clear()
        ax.set_facecolor(self.PANEL_BG)
        ax.set_xlim(0, 100)
        ax.set_ylim(0, 100)

        # Panel header
        header = FancyBboxPatch((0, 90), 100, 10, boxstyle="square",
                                facecolor=self.PANEL_HEADER, edgecolor='none')
        ax.add_patch(header)
        ax.text(50, 95, 'ELEMENTS', fontsize=10, fontweight='bold',
                ha='center', va='center', color=self.colors['accent'])

        # Scroll indicator
        if self.scroll_offset > 0:
            ax.text(50, 87, '^ scroll up', fontsize=7, ha='center',
                    color=self.colors['dim'])

        # Element buttons with thumbnails
        visible = 8
        start = self.scroll_offset
        end = min(start + visible, len(self.ELEMENTS))

        self.elem_boxes = []
        y = 84
        btn_h = 9.5

        for i in range(start, end):
            elem_type, label = self.ELEMENTS[i]
            is_active = (elem_type == self.placing_element)

            # Draw thumbnail
            thumb_x = 0.06
            thumb_y = (y - btn_h + 1) / 100
            thumb_w = 0.35
            thumb_h = (btn_h - 1) / 100

            self._draw_element_thumbnail(ax, elem_type, thumb_x, thumb_y, thumb_w, thumb_h, is_active)

            # Label
            text_color = 'white' if is_active else self.colors['text']
            ax.text(75, y - btn_h/2 + 0.5, label, fontsize=8,
                    ha='center', va='center', color=text_color)

            self.elem_boxes.append((y - btn_h + 1, y, elem_type))
            y -= btn_h + 0.8

        # Scroll down indicator
        if end < len(self.ELEMENTS):
            ax.text(50, y - 3, 'v scroll down', fontsize=7, ha='center',
                    color=self.colors['dim'])

        # Instructions at bottom
        ax.text(50, 3, 'Click element, then\nclick on canvas', fontsize=7,
                ha='center', va='bottom', color=self.colors['dim'],
                linespacing=1.4, style='italic')

        ax.axis('off')

    def _draw_right_panel(self):
        """Draw properties panel with tabbed interface - optimized for readability"""
        ax = self.ax_right
        ax.clear()
        ax.set_facecolor(self.PANEL_BG)
        ax.set_xlim(0, 100)
        ax.set_ylim(0, 100)

        # Reset button lists
        self.prop_buttons = []
        self.phase_buttons = []
        self.easing_buttons = []
        self.effect_buttons = []
        self.slider_buttons = []
        self.tab_buttons = []

        M = 3  # Margin

        # === HEADER (92-100) ===
        ax.add_patch(Rectangle((0, 92), 100, 8, facecolor=self.PANEL_HEADER, edgecolor='none'))
        ax.text(50, 96, 'PROPERTIES', fontsize=11, fontweight='bold',
                ha='center', va='center', color=self.colors['accent'])

        if self.selected_element is not None:
            elements = self._get_current_elements()
            if self.selected_element < len(elements):
                elem = elements[self.selected_element]
                elem_type = elem.get('type', 'unknown')

                # === ELEMENT TYPE BADGE (84-90) ===
                ax.add_patch(FancyBboxPatch((M, 84), 100 - 2*M, 7,
                                           boxstyle="round,pad=0.02",
                                           facecolor=self.colors['primary'],
                                           edgecolor='none', alpha=0.3))
                ax.text(50, 87.5, elem_type.replace('_', ' ').upper(), fontsize=10,
                        fontweight='bold', ha='center', va='center',
                        color=self.colors['primary'])

                # === TAB BUTTONS (75-82) ===
                tab_w = 45
                tabs = [('props', 'Content'), ('anim', 'Animation')]
                for i, (tab_id, tab_label) in enumerate(tabs):
                    is_active = self.props_tab == tab_id
                    tx = M + 1 + i * (tab_w + 3)
                    ty = 76

                    bg_color = '#1a1a2e' if is_active else '#0a0a0f'
                    border_color = self.colors['accent'] if is_active else '#3a3a4a'

                    ax.add_patch(FancyBboxPatch((tx, ty), tab_w, 7,
                                               boxstyle="round,pad=0.02",
                                               facecolor=bg_color,
                                               edgecolor=border_color,
                                               linewidth=2 if is_active else 1))
                    ax.text(tx + tab_w/2, ty + 3.5, tab_label, fontsize=9,
                            fontweight='bold',
                            ha='center', va='center',
                            color='white' if is_active else '#888888')
                    self.tab_buttons.append((ty, ty + 7, tx, tx + tab_w, tab_id))

                # === TAB CONTENT AREA (15-74) ===
                ax.add_patch(FancyBboxPatch((M, 15), 100 - 2*M, 59,
                                           boxstyle="round,pad=0.02",
                                           facecolor='#0d0d14',
                                           edgecolor='#2a2a3a', linewidth=1))

                if self.props_tab == 'props':
                    self._draw_props_tab(ax, elem, M, 6)
                else:
                    self._draw_anim_tab(ax, elem, M, 6)

                # === ACTIONS (8-13) ===
                ax.text(50, 10, '[E] Edit All   [D] Duplicate   [Del] Delete',
                        fontsize=7, ha='center', va='center', color='#888888')

        else:
            # No selection - clear instructions
            ax.text(50, 65, 'No Selection', fontsize=14, ha='center',
                    va='center', color='#666666', style='italic')

            instructions = [
                'Click element to select',
                'Drag to move element',
                '',
                '[E] Edit all properties',
                '[D] Duplicate element',
                '[Del] Delete element',
                '',
                'Right-drag canvas: zoom'
            ]
            y = 52
            for line in instructions:
                ax.text(50, y, line, fontsize=8, ha='center', color='#777777')
                y -= 5

        # === STEP INFO (1-7) ===
        ax.add_patch(FancyBboxPatch((M, 1), 100 - 2*M, 6,
                                   boxstyle="round,pad=0.02",
                                   facecolor='#12121a',
                                   edgecolor='#2a2a3a', linewidth=1))

        step = self._get_current_step()
        if step:
            ax.text(50, 4, f'{step.name[:18]}  ({len(step.elements)} elements)',
                    fontsize=8, ha='center', va='center', color='#aaaaaa')

        ax.axis('off')

    def _draw_props_tab(self, ax, elem, M, BTN_H):
        """Draw the Properties/Content tab"""
        props = self._get_editable_props(elem)

        # Draw up to 7 properties with good spacing
        y = 73
        row_h = 7
        for prop_name, prop_val, prop_type in props[:7]:
            # Label - bright and readable
            ax.text(M + 2, y, f"{prop_name}", fontsize=8,
                    ha='left', va='center', color=self.colors['text'], fontweight='bold')
            # Value box (clickable) - good contrast
            ax.add_patch(FancyBboxPatch((38, y - 3), 55, 6,
                                       boxstyle="round,pad=0.02",
                                       facecolor='#1a1a2e',
                                       edgecolor=self.colors['primary'], linewidth=1))
            ax.text(65, y, str(prop_val)[:12], fontsize=8, ha='center',
                    va='center', color='#ffffff')
            self.prop_buttons.append((y - 3, y + 3, 38, 93, prop_name, self.selected_element))
            y -= row_h

        # Show count if more properties
        if len(props) > 7:
            ax.text(50, y + 2, f'Press [E] for {len(props) - 7} more...', fontsize=7,
                    ha='center', color=self.colors['accent'])

    def _draw_anim_tab(self, ax, elem, M, BTN_H):
        """Draw the Animation tab with granular timing controls"""

        elem_type = elem.get('type', 'text')
        BTN_H = 6  # Button height

        # === TIMING SECTION (top) ===
        ax.text(M + 2, 72, 'Timing', fontsize=9, fontweight='bold',
                ha='left', va='center', color=self.colors['text'])

        # Duration slider
        duration = elem.get('duration', 1.0)
        ax.text(M + 2, 67, 'Duration:', fontsize=7, ha='left', color='#aaaaaa')
        self._draw_slider(ax, M + 28, 65, 62, duration, 0.1, 3.0, 's', 'duration')

        # Delay slider
        delay = elem.get('delay', 0.0)
        ax.text(M + 2, 61, 'Delay:', fontsize=7, ha='left', color='#aaaaaa')
        self._draw_slider(ax, M + 28, 59, 62, delay, 0.0, 2.0, 's', 'delay')

        # Speed multiplier (for animated elements)
        if elem_type in ('particle_flow', 'typewriter_text', 'token_flow', 'neural_network'):
            speed = elem.get('speed', 1.0)
            ax.text(M + 2, 55, 'Speed:', fontsize=7, ha='left', color='#aaaaaa')
            self._draw_slider(ax, M + 28, 53, 62, speed, 0.25, 4.0, 'x', 'speed')
            phase_y = 48
        else:
            phase_y = 52

        # === PHASE SECTION ===
        ax.text(M + 2, phase_y, 'Phase', fontsize=8, fontweight='bold',
                ha='left', va='center', color=self.colors['text'])

        current_phase = elem.get('animation_phase', 'early')
        phases = [('immediate', 'Imm'), ('early', 'Ear'), ('middle', 'Mid'),
                  ('late', 'Late'), ('final', 'Fin')]

        btn_w = 17
        y = phase_y - 6
        for i, (phase_val, phase_label) in enumerate(phases):
            is_cur = phase_val == current_phase
            px = M + 2 + i * (btn_w + 2)

            bg = self.colors['accent'] if is_cur else '#1a1a2e'
            border = self.colors['accent'] if is_cur else '#3a3a4a'
            ax.add_patch(FancyBboxPatch((px, y), btn_w, BTN_H,
                                       boxstyle="round,pad=0.02",
                                       facecolor=bg, edgecolor=border,
                                       linewidth=2 if is_cur else 1))
            ax.text(px + btn_w/2, y + BTN_H/2, phase_label, fontsize=6,
                    ha='center', va='center', fontweight='bold',
                    color='white' if is_cur else '#aaaaaa')
            self.phase_buttons.append((y, y + BTN_H, px, px + btn_w, phase_val))

        # === EASING SECTION ===
        easing_y = y - 10
        ax.text(M + 2, easing_y, 'Easing', fontsize=8, fontweight='bold',
                ha='left', va='center', color=self.colors['text'])

        current_easing = elem.get('easing', 'ease_in_out')
        easings = [
            [('linear', 'Lin'), ('ease_in', 'In'), ('ease_out', 'Out'), ('ease_in_out', 'IO')],
            [('elastic_out', 'Elast'), ('bounce_out', 'Bnce'), ('ease_in_cubic', 'Cub')]
        ]

        btn_w = 21
        for row, easing_row in enumerate(easings):
            ey = easing_y - 6 - row * (BTN_H + 1)
            for i, (easing_val, easing_label) in enumerate(easing_row):
                is_cur = easing_val == current_easing
                px = M + 2 + i * (btn_w + 2)

                bg = self.colors['highlight'] if is_cur else '#1a1a2e'
                border = self.colors['highlight'] if is_cur else '#3a3a4a'
                ax.add_patch(FancyBboxPatch((px, ey), btn_w, BTN_H,
                                           boxstyle="round,pad=0.02",
                                           facecolor=bg, edgecolor=border,
                                           linewidth=2 if is_cur else 1))
                ax.text(px + btn_w/2, ey + BTN_H/2, easing_label, fontsize=6,
                        ha='center', va='center', fontweight='bold',
                        color='white' if is_cur else '#aaaaaa')
                self.easing_buttons.append((ey, ey + BTN_H, px, px + btn_w, easing_val))

        # === EFFECT SECTION ===
        effect_y = easing_y - 22
        ax.text(M + 2, effect_y, 'Effect', fontsize=8, fontweight='bold',
                ha='left', va='center', color=self.colors['text'])

        current_effect = elem.get('continuous_effect', 'none')
        effects = [('none', 'None'), ('pulse', 'Pulse'), ('breathing', 'Breathe')]

        btn_w = 28
        fy = effect_y - 6
        for i, (effect_val, effect_label) in enumerate(effects):
            is_cur = effect_val == current_effect
            px = M + 2 + i * (btn_w + 2)

            bg = self.colors['success'] if is_cur else '#1a1a2e'
            border = self.colors['success'] if is_cur else '#3a3a4a'
            ax.add_patch(FancyBboxPatch((px, fy), btn_w, BTN_H,
                                       boxstyle="round,pad=0.02",
                                       facecolor=bg, edgecolor=border,
                                       linewidth=2 if is_cur else 1))
            ax.text(px + btn_w/2, fy + BTN_H/2, effect_label, fontsize=6,
                    ha='center', va='center', fontweight='bold',
                    color='white' if is_cur else '#aaaaaa')
            self.effect_buttons.append((fy, fy + BTN_H, px, px + btn_w, effect_val))

    def _draw_slider(self, ax, x, y, width, value, min_val, max_val, unit, prop_name):
        """Draw a clickable slider control"""
        # Track background
        ax.add_patch(FancyBboxPatch((x, y), width, 4,
                                   boxstyle="round,pad=0.01",
                                   facecolor='#1a1a2e',
                                   edgecolor='#3a3a4a', linewidth=1))

        # Fill based on value
        pct = (value - min_val) / (max_val - min_val)
        fill_w = max(2, pct * (width - 4))
        ax.add_patch(FancyBboxPatch((x + 1, y + 0.5), fill_w, 3,
                                   boxstyle="round,pad=0.01",
                                   facecolor=self.colors['primary'],
                                   edgecolor='none'))

        # Value label
        ax.text(x + width + 3, y + 2, f'{value:.1f}{unit}', fontsize=7,
                ha='left', va='center', color='white', fontweight='bold')

        # Store slider region for click handling
        self.slider_buttons.append((y, y + 4, x, x + width, prop_name, min_val, max_val))

    def _draw_bottom_bar(self):
        """Draw bottom navigation bar"""
        ax = self.ax_bottom
        ax.clear()
        ax.set_facecolor(self.PANEL_HEADER)
        ax.set_xlim(0, 100)
        ax.set_ylim(0, 100)

        # Navigation buttons
        nav_btns = [
            (8, '<', 'prev'),
            (18, '+', 'add'),
            (28, '-', 'del'),
            (92, '>', 'next'),
        ]

        self.nav_buttons = []
        for x, icon, action in nav_btns:
            btn = FancyBboxPatch((x - 5, 20), 10, 60,
                                 boxstyle="round,pad=0.02",
                                 facecolor='#1a1a24',
                                 edgecolor='#2a2a3a',
                                 linewidth=1)
            ax.add_patch(btn)
            ax.text(x, 50, icon, fontsize=16, fontweight='bold',
                    ha='center', va='center', color=self.colors['text'])
            self.nav_buttons.append((x - 5, x + 5, 20, 80, action))

        # Step indicator
        step = self._get_current_step()
        step_name = step.name[:20] if step else "No step"
        indicator = f'Step {self.current_step + 1}/{len(self.schema.steps)}: {step_name}'
        ax.text(55, 50, indicator, fontsize=11, fontweight='bold',
                ha='center', va='center', color=self.colors['primary'])

        ax.axis('off')

    def _draw_canvas(self):
        """Draw the main canvas with elements"""
        ax = self.ax_canvas
        ax.clear()
        ax.set_facecolor(self.CANVAS_BG)
        ax.set_xlim(0, 100)
        ax.set_ylim(0, 100)

        # Subtle grid
        for i in range(10, 100, 10):
            ax.axhline(i, color='#1a1a1a', linewidth=0.5, alpha=0.5)
            ax.axvline(i, color='#1a1a1a', linewidth=0.5, alpha=0.5)

        step = self._get_current_step()
        if step:
            # Step title
            if step.title:
                ax.text(50, 96, step.title, fontsize=14, fontweight='bold',
                        ha='center', va='top', color=self.colors['primary'])

            # Draw elements
            for i, elem in enumerate(step.elements):
                self._draw_element(ax, elem, i == self.selected_element)

        # Placement indicator
        if self.placing_element:
            ax.text(50, 2, f'Click to place: {self.placing_element}',
                    fontsize=10, ha='center', va='bottom',
                    color=self.colors['accent'],
                    bbox=dict(boxstyle='round,pad=0.3',
                             facecolor='#1a1a1a', edgecolor=self.colors['accent']))

        ax.axis('off')

        # Restore spines styling
        for spine in ax.spines.values():
            spine.set_visible(True)
            spine.set_color(self.colors['primary'])
            spine.set_linewidth(2)

    def _draw_element(self, ax, elem, selected):
        """Draw a single element on canvas"""
        t = elem.get('type', 'text')
        pos = elem.get('position', {'x': 50, 'y': 50})
        x, y = pos['x'], pos['y']

        sel_color = self.colors['accent']
        lw = 2.5 if selected else 1

        if t in ('text', 'typewriter_text'):
            content = elem.get('content', 'Text')[:25]
            bbox = dict(boxstyle='round,pad=0.4',
                       facecolor='#1a1a24' if selected else 'none',
                       edgecolor=sel_color if selected else 'none',
                       linewidth=lw)
            ax.text(x, y, content, fontsize=11, ha='center', va='center',
                   color=self.colors['text'], bbox=bbox)

        elif t == 'box':
            w, h = elem.get('width', 25), elem.get('height', 12)
            ax.add_patch(FancyBboxPatch(
                (x - w/2, y - h/2), w, h,
                boxstyle="round,pad=0.3",
                facecolor='#1a1a24',
                edgecolor=sel_color if selected else self.colors['primary'],
                linewidth=lw))
            if elem.get('title'):
                ax.text(x, y + h/4, elem['title'][:15], fontsize=9,
                       fontweight='bold', ha='center', color=self.colors['primary'])

        elif t == 'bullet_list':
            items = elem.get('items', [])[:4]
            for j, item in enumerate(items):
                ax.text(x - 10, y + 4 - j * 4, f'* {item[:15]}',
                       fontsize=8, ha='left', color=self.colors['text'])
            if selected:
                ax.add_patch(Rectangle((x - 15, y - 10), 30, 18,
                                       fill=False, edgecolor=sel_color, linewidth=lw))

        elif t == 'comparison':
            w, h = elem.get('width', 50), elem.get('height', 18)
            ax.add_patch(FancyBboxPatch(
                (x - w/2, y - h/2), w/2 - 1, h,
                boxstyle="round,pad=0.2", facecolor='#1a1a24',
                edgecolor=self.colors['warning'], linewidth=1))
            ax.add_patch(FancyBboxPatch(
                (x + 1, y - h/2), w/2 - 1, h,
                boxstyle="round,pad=0.2", facecolor='#1a1a24',
                edgecolor=self.colors['success'], linewidth=1))
            if selected:
                ax.add_patch(Rectangle((x - w/2 - 1, y - h/2 - 1), w + 2, h + 2,
                                       fill=False, edgecolor=sel_color, linewidth=lw))

        elif t in ('arrow', 'arc_arrow'):
            start = elem.get('start', {'x': x - 10, 'y': y})
            end = elem.get('end', {'x': x + 10, 'y': y})
            style = 'arc3,rad=0.2' if t == 'arc_arrow' else None
            ax.annotate('', xy=(end['x'], end['y']), xytext=(start['x'], start['y']),
                       arrowprops=dict(arrowstyle='-|>', lw=lw,
                                      color=sel_color if selected else self.colors['primary'],
                                      connectionstyle=style))

        elif t == 'similarity_meter':
            r = elem.get('radius', 5)
            ax.add_patch(Wedge((x, y), r, 0, 180,
                              facecolor=self.colors['success'],
                              edgecolor=sel_color if selected else self.colors['dim'],
                              linewidth=lw))
            ax.text(x, y, f"{elem.get('score', 75)}%", fontsize=8,
                   ha='center', va='center', color='white', fontweight='bold')

        elif t == 'progress_bar':
            w = elem.get('width', 18)
            ax.add_patch(Rectangle((x - w/2, y - 1.5), w, 3,
                                  facecolor='#1a1a24',
                                  edgecolor=sel_color if selected else self.colors['dim'],
                                  linewidth=lw))
            fill = w * elem.get('current', 5) / max(elem.get('total', 10), 1)
            ax.add_patch(Rectangle((x - w/2, y - 1.5), fill, 3,
                                  facecolor=self.colors['success']))

        elif t == 'neural_network':
            w, h = elem.get('width', 35), elem.get('height', 22)
            layers = elem.get('layers', [3, 4, 2])
            sp = w / (len(layers) + 1)
            for li, n in enumerate(layers):
                lx = x - w/2 + (li + 1) * sp
                ns = h / (n + 1)
                for ni in range(n):
                    ny = y - h/2 + (ni + 1) * ns
                    ax.add_patch(Circle((lx, ny), 0.9,
                                       facecolor=self.colors['primary'],
                                       edgecolor='white', linewidth=0.3))
            if selected:
                ax.add_patch(Rectangle((x - w/2 - 1, y - h/2 - 1), w + 2, h + 2,
                                       fill=False, edgecolor=sel_color, linewidth=lw))

        elif t == 'code_block':
            w, h = elem.get('width', 25), elem.get('height', 10)
            ax.add_patch(FancyBboxPatch(
                (x - w/2, y - h/2), w, h,
                boxstyle="round,pad=0.2",
                facecolor='#0a0a12',
                edgecolor=sel_color if selected else self.colors['dim'],
                linewidth=lw))
            code = elem.get('code', 'code...')[:20]
            ax.text(x, y, code, fontsize=7, ha='center', va='center',
                   color=self.colors['success'], family='monospace')

        elif t == 'flow':
            w = elem.get('width', 45)
            steps = elem.get('steps', [{'title': 'Step'}])[:4]
            step_w = w / len(steps) - 2
            for i, s in enumerate(steps):
                sx = x - w/2 + i * (step_w + 2) + step_w/2
                ax.add_patch(FancyBboxPatch(
                    (sx - step_w/2, y - 4), step_w, 8,
                    boxstyle="round,pad=0.2",
                    facecolor='#1a1a24',
                    edgecolor=self.colors['primary'],
                    linewidth=1))
                ax.text(sx, y, s.get('title', '')[:8], fontsize=7,
                       ha='center', va='center', color=self.colors['text'])
            if selected:
                ax.add_patch(Rectangle((x - w/2 - 1, y - 6), w + 2, 12,
                                       fill=False, edgecolor=sel_color, linewidth=lw))

        elif t == 'grid':
            cols = elem.get('columns', 2)
            rows = elem.get('rows', 2)
            items = elem.get('items', [])
            cell_w, cell_h = 12, 6
            total_w = cols * cell_w + (cols - 1) * 2
            total_h = rows * cell_h + (rows - 1) * 2
            for r in range(rows):
                for c in range(cols):
                    idx = r * cols + c
                    cx = x - total_w/2 + c * (cell_w + 2) + cell_w/2
                    cy = y + total_h/2 - r * (cell_h + 2) - cell_h/2
                    ax.add_patch(FancyBboxPatch(
                        (cx - cell_w/2, cy - cell_h/2), cell_w, cell_h,
                        boxstyle="round,pad=0.1",
                        facecolor='#1a1a24',
                        edgecolor=self.colors['primary'],
                        linewidth=0.8))
                    if idx < len(items):
                        ax.text(cx, cy, items[idx].get('title', '')[:6],
                               fontsize=6, ha='center', va='center',
                               color=self.colors['text'])
            if selected:
                ax.add_patch(Rectangle((x - total_w/2 - 1, y - total_h/2 - 1),
                                       total_w + 2, total_h + 2,
                                       fill=False, edgecolor=sel_color, linewidth=lw))

        elif t == 'checklist':
            items = elem.get('items', [])[:4]
            for j, item in enumerate(items):
                iy = y + 4 - j * 4
                ax.add_patch(Rectangle((x - 12, iy - 1.5), 3, 3,
                                       facecolor='none',
                                       edgecolor=self.colors['success'],
                                       linewidth=0.8))
                ax.text(x - 7, iy, item[:12], fontsize=7,
                       ha='left', va='center', color=self.colors['text'])
            if selected:
                ax.add_patch(Rectangle((x - 15, y - 10), 30, 18,
                                       fill=False, edgecolor=sel_color, linewidth=lw))

        elif t == 'particle_flow':
            start = elem.get('start', {'x': x - 15, 'y': y})
            end = elem.get('end', {'x': x + 15, 'y': y})
            n = elem.get('num_particles', 10)
            ax.plot([start['x'], end['x']], [start['y'], end['y']],
                   '--', color=self.colors['dim'], linewidth=0.5, alpha=0.5)
            for i in range(min(n, 8)):
                t_pos = i / max(n - 1, 1)
                px = start['x'] + (end['x'] - start['x']) * t_pos
                py = start['y'] + (end['y'] - start['y']) * t_pos
                ax.add_patch(Circle((px, py), 0.6,
                                   facecolor=self.colors['accent'],
                                   edgecolor='none', alpha=0.4 + t_pos * 0.5))
            if selected:
                min_x = min(start['x'], end['x'])
                min_y = min(start['y'], end['y'])
                w = abs(end['x'] - start['x']) + 4
                h = abs(end['y'] - start['y']) + 6
                ax.add_patch(Rectangle((min_x - 2, min_y - 3), w, h,
                                       fill=False, edgecolor=sel_color, linewidth=lw))

        elif t == 'code_execution':
            w, h = elem.get('width', 30), elem.get('code_height', 8) + elem.get('output_height', 5) + 3
            # Code box
            ax.add_patch(FancyBboxPatch(
                (x - w/2, y + 2), w, elem.get('code_height', 8),
                boxstyle="round,pad=0.2", facecolor='#0a0a12',
                edgecolor=self.colors['dim'], linewidth=0.8))
            ax.text(x, y + 6, elem.get('code', 'code')[:15], fontsize=6,
                   ha='center', va='center', color='#a8ff60', family='monospace')
            # Arrow
            ax.annotate('', xy=(x, y - 1), xytext=(x, y + 1),
                       arrowprops=dict(arrowstyle='->', lw=1, color=self.colors['accent']))
            # Output box
            ax.add_patch(FancyBboxPatch(
                (x - w/2, y - elem.get('output_height', 5) - 1), w, elem.get('output_height', 5),
                boxstyle="round,pad=0.2", facecolor='#1a2e1a',
                edgecolor=self.colors['success'], linewidth=0.8))
            ax.text(x, y - 3, elem.get('output', 'out')[:15], fontsize=6,
                   ha='center', va='center', color='#60ffa8', family='monospace')
            if selected:
                ax.add_patch(Rectangle((x - w/2 - 1, y - h/2 - 1), w + 2, h + 2,
                                       fill=False, edgecolor=sel_color, linewidth=lw))

        elif t == 'conversation':
            w = elem.get('width', 35)
            msgs = elem.get('messages', [{'role': 'user', 'content': 'Hello'}])[:3]
            for i, msg in enumerate(msgs):
                is_user = msg.get('role', 'user') == 'user'
                bx = x - w/4 if is_user else x + w/4 - w/2
                by = y + 6 - i * 5
                color = self.colors['primary'] if is_user else self.colors['secondary']
                ax.add_patch(FancyBboxPatch(
                    (bx, by - 2), w/2 - 2, 4,
                    boxstyle="round,pad=0.2", facecolor='#1a1a24',
                    edgecolor=color, linewidth=0.8))
                ax.text(bx + w/4 - 1, by, msg.get('content', '')[:10], fontsize=6,
                       ha='center', va='center', color=self.colors['text'])
            if selected:
                ax.add_patch(Rectangle((x - w/2 - 1, y - 10), w + 2, 20,
                                       fill=False, edgecolor=sel_color, linewidth=lw))

        elif t == 'timeline':
            w = elem.get('width', 40)
            events = elem.get('events', [{'date': '2023', 'title': 'Event'}])[:4]
            # Main line
            ax.plot([x - w/2, x + w/2], [y, y], color=self.colors['dim'], linewidth=1.5)
            # Events
            spacing = w / max(len(events) - 1, 1) if len(events) > 1 else 0
            for i, ev in enumerate(events):
                ex = x - w/2 + i * spacing
                ax.add_patch(Circle((ex, y), 1.2,
                                   facecolor=self.colors['primary'],
                                   edgecolor='white', linewidth=0.5))
                ax.text(ex, y + 3, ev.get('date', '')[:6], fontsize=5,
                       ha='center', va='bottom', color=self.colors['dim'])
            if selected:
                ax.add_patch(Rectangle((x - w/2 - 2, y - 5), w + 4, 10,
                                       fill=False, edgecolor=sel_color, linewidth=lw))

        elif t == 'stacked_boxes':
            items = elem.get('items', [{'title': 'Item'}])[:4]
            base_w = elem.get('base_width', 30)
            box_h = 5
            for i, item in enumerate(items):
                w = base_w - i * 3
                iy = y + (len(items)/2 - i - 0.5) * (box_h + 1)
                ax.add_patch(FancyBboxPatch(
                    (x - w/2, iy - box_h/2), w, box_h,
                    boxstyle="round,pad=0.2", facecolor='#1a1a24',
                    edgecolor=self.colors['primary'], linewidth=0.8))
                ax.text(x, iy, item.get('title', '')[:10], fontsize=6,
                       ha='center', va='center', color=self.colors['text'])
            if selected:
                ax.add_patch(Rectangle((x - base_w/2 - 1, y - len(items)*3 - 1),
                                       base_w + 2, len(items)*6 + 2,
                                       fill=False, edgecolor=sel_color, linewidth=lw))

        elif t == 'attention_heatmap':
            w, h = elem.get('width', 25), elem.get('height', 25)
            tokens = elem.get('tokens_x', ['A', 'B', 'C'])[:4]
            n = len(tokens)
            cell_s = min(w, h) / n
            for i in range(n):
                for j in range(n):
                    intensity = 0.8 if i == j else 0.3
                    cx = x - w/2 + j * cell_s + cell_s/2
                    cy = y + h/2 - i * cell_s - cell_s/2
                    ax.add_patch(Rectangle(
                        (cx - cell_s/2 + 0.2, cy - cell_s/2 + 0.2),
                        cell_s - 0.4, cell_s - 0.4,
                        facecolor=plt.cm.viridis(intensity),
                        edgecolor='#333', linewidth=0.3))
            if selected:
                ax.add_patch(Rectangle((x - w/2 - 1, y - h/2 - 1), w + 2, h + 2,
                                       fill=False, edgecolor=sel_color, linewidth=lw))

        elif t == 'token_flow':
            w = elem.get('width', 40)
            # Input text box
            ax.add_patch(FancyBboxPatch(
                (x - w/2, y + 4), w, 5,
                boxstyle="round,pad=0.2", facecolor='#1a1a24',
                edgecolor=self.colors['primary'], linewidth=0.8))
            ax.text(x, y + 6.5, elem.get('input_text', 'Hello')[:15], fontsize=6,
                   ha='center', va='center', color=self.colors['text'])
            # Arrow
            ax.annotate('', xy=(x, y + 1), xytext=(x, y + 3),
                       arrowprops=dict(arrowstyle='->', lw=1, color=self.colors['accent']))
            # Tokens
            tokens = elem.get('input_text', 'Hello').split()[:4]
            tok_w = min(8, w / len(tokens) - 1) if tokens else 8
            for i, tok in enumerate(tokens):
                tx = x - w/2 + 3 + i * (tok_w + 1)
                ax.add_patch(FancyBboxPatch(
                    (tx, y - 3), tok_w, 4,
                    boxstyle="round,pad=0.1", facecolor='#1a1a24',
                    edgecolor=self.colors['secondary'], linewidth=0.6))
                ax.text(tx + tok_w/2, y - 1, tok[:5], fontsize=5,
                       ha='center', va='center', color=self.colors['text'])
            if selected:
                ax.add_patch(Rectangle((x - w/2 - 1, y - 5), w + 2, 14,
                                       fill=False, edgecolor=sel_color, linewidth=lw))

        elif t == 'model_comparison':
            w, h = elem.get('width', 45), elem.get('height', 25)
            models = elem.get('models', [{'name': 'A'}, {'name': 'B'}])[:3]
            n = len(models)
            col_w = w / (n + 1)
            # Headers
            for i, m in enumerate(models):
                mx = x - w/2 + (i + 1.5) * col_w
                ax.text(mx, y + h/2 - 2, m.get('name', f'M{i+1}')[:6], fontsize=7,
                       fontweight='bold', ha='center', va='center',
                       color=self.colors['primary'])
            # Grid lines
            for i in range(3):
                ry = y + h/2 - 5 - i * 6
                ax.plot([x - w/2 + col_w, x + w/2], [ry, ry],
                       color=self.colors['dim'], linewidth=0.5, alpha=0.5)
            if selected:
                ax.add_patch(Rectangle((x - w/2 - 1, y - h/2 - 1), w + 2, h + 2,
                                       fill=False, edgecolor=sel_color, linewidth=lw))

        elif t == 'parameter_slider':
            w = elem.get('width', 25)
            label = elem.get('label', 'Parameter')[:12]
            val = elem.get('current_value', 0.5)
            min_v, max_v = elem.get('min_value', 0), elem.get('max_value', 1)
            ratio = (val - min_v) / (max_v - min_v) if max_v != min_v else 0.5
            # Label
            ax.text(x, y + 5, label, fontsize=8, fontweight='bold',
                   ha='center', va='center', color=self.colors['text'])
            # Track
            ax.add_patch(Rectangle((x - w/2, y - 0.5), w, 1,
                                  facecolor='#333', edgecolor='#555', linewidth=0.5))
            # Fill
            ax.add_patch(Rectangle((x - w/2, y - 0.5), w * ratio, 1,
                                  facecolor=self.colors['accent']))
            # Handle
            ax.add_patch(Circle((x - w/2 + w * ratio, y), 1.2,
                               facecolor='white',
                               edgecolor=self.colors['accent'],
                               linewidth=1))
            # Value
            ax.text(x - w/2 + w * ratio, y + 2.5, f'{val}', fontsize=7,
                   ha='center', va='bottom', color=self.colors['accent'])
            if selected:
                ax.add_patch(Rectangle((x - w/2 - 2, y - 3), w + 4, 10,
                                       fill=False, edgecolor=sel_color, linewidth=lw))

        elif t == 'weight_comparison':
            before = elem.get('before_weights', [0.5, 0.3])[:4]
            after = elem.get('after_weights', [0.7, 0.5])[:4]
            bar_w = 15
            for i, (b, a) in enumerate(zip(before, after)):
                iy = y + 3 - i * 4
                # Before bar (left)
                ax.add_patch(Rectangle((x - bar_w - 1, iy - 1), bar_w * b, 2,
                                       facecolor=self.colors['warning']))
                # After bar (right)
                ax.add_patch(Rectangle((x + 1, iy - 1), bar_w * a, 2,
                                       facecolor=self.colors['success']))
            if selected:
                ax.add_patch(Rectangle((x - bar_w - 2, y - 7), bar_w * 2 + 6, 14,
                                       fill=False, edgecolor=sel_color, linewidth=lw))

        elif t == 'scatter_3d':
            # Just show a placeholder for 3D in 2D canvas
            w, h = 20, 15
            ax.add_patch(FancyBboxPatch(
                (x - w/2, y - h/2), w, h,
                boxstyle="round,pad=0.2", facecolor='#1a1a24',
                edgecolor=sel_color if selected else self.colors['primary'],
                linewidth=lw))
            ax.text(x, y, '3D', fontsize=12, fontweight='bold',
                   ha='center', va='center', color=self.colors['primary'])
            points = elem.get('points', [])[:5]
            for i, pt in enumerate(points):
                px = x - 6 + i * 3
                py = y - 3 + (i % 2) * 2
                ax.add_patch(Circle((px, py), 0.8,
                                   facecolor=self.colors['accent'],
                                   edgecolor='none'))

        elif t == 'vector_3d':
            w, h = 18, 14
            ax.add_patch(FancyBboxPatch(
                (x - w/2, y - h/2), w, h,
                boxstyle="round,pad=0.2", facecolor='#1a1a24',
                edgecolor=sel_color if selected else self.colors['primary'],
                linewidth=lw))
            ax.text(x, y + 3, 'v3D', fontsize=10, fontweight='bold',
                   ha='center', va='center', color=self.colors['primary'])
            # Draw some arrows to indicate vectors
            for i, (dx, dy) in enumerate([(3, 2), (-2, 3), (4, -1)]):
                ax.annotate('', xy=(x + dx, y - 2 + dy), xytext=(x, y - 2),
                           arrowprops=dict(arrowstyle='->', lw=0.8,
                                          color=self.colors['accent']))

        else:
            # Generic placeholder
            w, h = elem.get('width', 18), elem.get('height', 10)
            ax.add_patch(FancyBboxPatch(
                (x - w/2, y - h/2), w, h,
                boxstyle="round,pad=0.2", facecolor='#1a1a24',
                edgecolor=sel_color if selected else self.colors['dim'],
                linewidth=lw, linestyle='--'))
            ax.text(x, y, t[:8], fontsize=7, ha='center', va='center',
                   color=self.colors['dim'])

    def _get_editable_props(self, elem):
        """Get editable properties for element - comprehensive by element type"""
        elem_type = elem.get('type', 'text')
        props = []

        # === POSITION (most elements) ===
        if 'position' in elem or elem_type not in ('arrow', 'arc_arrow', 'particle_flow'):
            pos = elem.get('position', {'x': 50, 'y': 50})
            props.append(('x', int(pos['x']), 'pos'))
            props.append(('y', int(pos['y']), 'pos'))

        # === BY ELEMENT TYPE ===

        if elem_type == 'text':
            props.append(('content', str(elem.get('content', ''))[:15], 'str'))

        elif elem_type == 'typewriter_text':
            props.append(('content', str(elem.get('content', ''))[:15], 'str'))
            props.append(('show_cursor', elem.get('show_cursor', True), 'bool'))
            props.append(('cursor_blink_rate', elem.get('cursor_blink_rate', 2.0), 'float'))

        elif elem_type == 'code_block':
            props.append(('code', str(elem.get('code', ''))[:15], 'str'))
            props.append(('language', elem.get('language', 'python'), 'str'))
            props.append(('width', int(elem.get('width', 60)), 'num'))
            props.append(('height', int(elem.get('height', 25)), 'num'))

        elif elem_type == 'code_execution':
            props.append(('code', str(elem.get('code', ''))[:15], 'str'))
            props.append(('output', str(elem.get('output', ''))[:15], 'str'))
            props.append(('language', elem.get('language', 'python'), 'str'))
            props.append(('width', int(elem.get('width', 70)), 'num'))

        elif elem_type == 'box':
            props.append(('title', str(elem.get('title', ''))[:15], 'str'))
            props.append(('content', str(elem.get('content', ''))[:15], 'str'))
            props.append(('width', int(elem.get('width', 60)), 'num'))
            props.append(('height', int(elem.get('height', 20)), 'num'))

        elif elem_type == 'comparison':
            props.append(('left_title', str(elem.get('left_title', 'Before'))[:12], 'str'))
            props.append(('right_title', str(elem.get('right_title', 'After'))[:12], 'str'))
            props.append(('width', int(elem.get('width', 80)), 'num'))
            props.append(('height', int(elem.get('height', 30)), 'num'))

        elif elem_type == 'conversation':
            msgs = elem.get('messages', [])
            props.append(('messages', f'{len(msgs)} msgs', 'list'))
            props.append(('width', int(elem.get('width', 70)), 'num'))
            props.append(('stagger', elem.get('stagger', True), 'bool'))

        elif elem_type == 'bullet_list':
            items = elem.get('items', [])
            props.append(('items', f'{len(items)} items', 'list'))
            props.append(('bullet_char', elem.get('bullet_char', '*'), 'str'))
            props.append(('spacing', elem.get('spacing', 6.0), 'float'))
            props.append(('stagger', elem.get('stagger', True), 'bool'))

        elif elem_type == 'checklist':
            items = elem.get('items', [])
            props.append(('items', f'{len(items)} items', 'list'))
            props.append(('spacing', elem.get('spacing', 6.5), 'float'))
            props.append(('fontsize', elem.get('fontsize', 18), 'num'))

        elif elem_type == 'timeline':
            events = elem.get('events', [])
            props.append(('events', f'{len(events)} events', 'list'))
            props.append(('orientation', elem.get('orientation', 'horizontal'), 'choice'))
            props.append(('width', int(elem.get('width', 80)), 'num'))
            props.append(('height', int(elem.get('height', 25)), 'num'))

        elif elem_type == 'flow':
            steps = elem.get('steps', [])
            props.append(('steps', f'{len(steps)} steps', 'list'))
            props.append(('width', int(elem.get('width', 80)), 'num'))
            props.append(('stagger', elem.get('stagger', True), 'bool'))

        elif elem_type == 'grid':
            items = elem.get('items', [])
            props.append(('items', f'{len(items)} items', 'list'))
            props.append(('columns', elem.get('columns', 2), 'num'))
            props.append(('rows', elem.get('rows', 2), 'num'))
            props.append(('cell_width', int(elem.get('cell_width', 30)), 'num'))
            props.append(('cell_height', int(elem.get('cell_height', 18)), 'num'))

        elif elem_type == 'stacked_boxes':
            items = elem.get('items', [])
            props.append(('items', f'{len(items)} items', 'list'))
            props.append(('base_width', int(elem.get('base_width', 70)), 'num'))
            props.append(('box_height', int(elem.get('box_height', 12)), 'num'))

        elif elem_type in ('arrow', 'arc_arrow', 'particle_flow'):
            start = elem.get('start', {'x': 30, 'y': 50})
            end = elem.get('end', {'x': 70, 'y': 50})
            props.append(('start_x', int(start['x']), 'start'))
            props.append(('start_y', int(start['y']), 'start'))
            props.append(('end_x', int(end['x']), 'end'))
            props.append(('end_y', int(end['y']), 'end'))

            if elem_type == 'arc_arrow':
                props.append(('arc_height', int(elem.get('arc_height', 15)), 'num'))
                props.append(('direction', elem.get('direction', 'up'), 'choice'))

            if elem_type == 'particle_flow':
                props.append(('num_particles', elem.get('num_particles', 30), 'num'))
                props.append(('particle_size', elem.get('particle_size', 30), 'num'))
                props.append(('spread', elem.get('spread', 0.5), 'float'))

        elif elem_type == 'neural_network':
            layers = elem.get('layers', [3, 5, 5, 2])
            props.append(('layers', str(layers), 'layers'))
            props.append(('width', int(elem.get('width', 70)), 'num'))
            props.append(('height', int(elem.get('height', 50)), 'num'))
            props.append(('show_connections', elem.get('show_connections', True), 'bool'))

        elif elem_type == 'attention_heatmap':
            props.append(('title', str(elem.get('title', 'Attention'))[:15], 'str'))
            tokens_x = elem.get('tokens_x', [])
            props.append(('tokens_x', f'{len(tokens_x)} tokens', 'list'))
            props.append(('width', int(elem.get('width', 50)), 'num'))
            props.append(('height', int(elem.get('height', 50)), 'num'))
            props.append(('show_values', elem.get('show_values', True), 'bool'))

        elif elem_type == 'token_flow':
            props.append(('input_text', str(elem.get('input_text', ''))[:15], 'str'))
            props.append(('width', int(elem.get('width', 80)), 'num'))
            props.append(('height', int(elem.get('height', 40)), 'num'))
            props.append(('show_embeddings', elem.get('show_embeddings', True), 'bool'))

        elif elem_type == 'model_comparison':
            models = elem.get('models', [])
            props.append(('models', f'{len(models)} models', 'list'))
            props.append(('width', int(elem.get('width', 85)), 'num'))
            props.append(('height', int(elem.get('height', 50)), 'num'))

        elif elem_type == 'similarity_meter':
            props.append(('score', int(elem.get('score', 75)), 'num'))
            props.append(('radius', int(elem.get('radius', 8)), 'num'))
            props.append(('label', str(elem.get('label', 'Similarity'))[:15], 'str'))

        elif elem_type == 'progress_bar':
            props.append(('current', elem.get('current', 5), 'num'))
            props.append(('total', elem.get('total', 10), 'num'))
            props.append(('width', int(elem.get('width', 30)), 'num'))
            props.append(('label', str(elem.get('label', 'Progress'))[:15], 'str'))

        elif elem_type == 'weight_comparison':
            before = elem.get('before_weights', [])
            after = elem.get('after_weights', [])
            props.append(('before_weights', f'{len(before)} vals', 'list'))
            props.append(('after_weights', f'{len(after)} vals', 'list'))

        elif elem_type == 'parameter_slider':
            props.append(('label', str(elem.get('label', 'Parameter'))[:15], 'str'))
            props.append(('current_value', elem.get('current_value', 0.5), 'float'))
            props.append(('min_value', elem.get('min_value', 0.0), 'float'))
            props.append(('max_value', elem.get('max_value', 1.0), 'float'))
            props.append(('width', int(elem.get('width', 40)), 'num'))

        elif elem_type == 'scatter_3d':
            points = elem.get('points', [])
            props.append(('points', f'{len(points)} pts', 'list'))
            props.append(('camera_elev', elem.get('camera_elev', 20.0), 'float'))
            props.append(('camera_azim', elem.get('camera_azim', 45.0), 'float'))
            props.append(('rotate_camera', elem.get('rotate_camera', False), 'bool'))

        elif elem_type == 'vector_3d':
            vectors = elem.get('vectors', [])
            props.append(('vectors', f'{len(vectors)} vecs', 'list'))
            props.append(('camera_elev', elem.get('camera_elev', 20.0), 'float'))
            props.append(('camera_azim', elem.get('camera_azim', 45.0), 'float'))
            props.append(('rotate_camera', elem.get('rotate_camera', False), 'bool'))

        return props

    def _get_current_step(self):
        if 0 <= self.current_step < len(self.schema.steps):
            return self.schema.steps[self.current_step]
        return None

    def _get_current_elements(self):
        step = self._get_current_step()
        return step.elements if step else []

    def _get_element_at(self, x, y):
        """Find element at canvas position - improved hit detection"""
        elements = self._get_current_elements()
        for i in range(len(elements) - 1, -1, -1):
            elem = elements[i]
            pos = elem.get('position', {'x': 50, 'y': 50})
            elem_type = elem.get('type', 'text')

            # Calculate hit box based on element type
            if elem_type in ('text', 'typewriter_text'):
                # Text elements - use content length for width estimation
                content = elem.get('content', 'Text')
                w = max(10, len(content) * 0.8)
                h = 6
            elif elem_type in ('arrow', 'arc_arrow'):
                # Arrows - use start/end points
                start = elem.get('start', {'x': pos['x'] - 10, 'y': pos['y']})
                end = elem.get('end', {'x': pos['x'] + 10, 'y': pos['y']})
                min_x = min(start['x'], end['x']) - 3
                max_x = max(start['x'], end['x']) + 3
                min_y = min(start['y'], end['y']) - 3
                max_y = max(start['y'], end['y']) + 3
                if min_x <= x <= max_x and min_y <= y <= max_y:
                    return i
                continue
            elif elem_type == 'particle_flow':
                # Particle flow - use start/end
                start = elem.get('start', {'x': pos['x'] - 15, 'y': pos['y']})
                end = elem.get('end', {'x': pos['x'] + 15, 'y': pos['y']})
                min_x = min(start['x'], end['x']) - 3
                max_x = max(start['x'], end['x']) + 3
                min_y = min(start['y'], end['y']) - 3
                max_y = max(start['y'], end['y']) + 3
                if min_x <= x <= max_x and min_y <= y <= max_y:
                    return i
                continue
            elif elem_type == 'similarity_meter':
                # Meter - circular hit area
                r = elem.get('radius', 5) + 2
                if (x - pos['x'])**2 + (y - pos['y'])**2 <= r**2:
                    return i
                continue
            elif elem_type in ('comparison', 'flow', 'grid'):
                w = elem.get('width', 50) / 2 + 3
                h = elem.get('height', 18) / 2 + 3
            elif elem_type == 'neural_network':
                w = elem.get('width', 35) / 2 + 3
                h = elem.get('height', 22) / 2 + 3
            elif elem_type in ('bullet_list', 'checklist'):
                w = 18
                h = 12
            else:
                w = elem.get('width', 18) / 2 + 5
                h = elem.get('height', 10) / 2 + 5

            # Check hit box
            if pos['x'] - w <= x <= pos['x'] + w and pos['y'] - h <= y <= pos['y'] + h:
                return i

        return None

    def _refresh_canvas_only(self):
        """Fast refresh - only redraw canvas"""
        self._draw_canvas()
        self.fig.canvas.draw_idle()
        self.fig.canvas.flush_events()

    def _refresh_all(self):
        """Full refresh of all panels"""
        self._draw_top_bar()
        self._draw_left_panel()
        self._draw_right_panel()
        self._draw_bottom_bar()
        self._draw_canvas()
        self.fig.canvas.draw_idle()
        self.fig.canvas.flush_events()

    # Event handlers
    def _on_click(self, event):
        if event.inaxes == self.ax_left:
            self._handle_left_click(event)
        elif event.inaxes == self.ax_canvas:
            self._handle_canvas_click(event)
        elif event.inaxes == self.ax_right:
            self._handle_right_panel_click(event)
        elif event.inaxes == self.ax_bottom:
            self._handle_bottom_click(event)

    def _handle_left_click(self, event):
        """Handle click on elements panel"""
        y = event.ydata
        if y is None:
            return

        for y_min, y_max, elem_type in self.elem_boxes:
            if y_min <= y <= y_max:
                if self.placing_element == elem_type:
                    self.placing_element = None
                else:
                    self.placing_element = elem_type
                self._draw_left_panel()
                self._draw_canvas()
                self.fig.canvas.draw_idle()
                return

    def _handle_canvas_click(self, event):
        """Handle click on canvas"""
        x, y = event.xdata, event.ydata
        if x is None or y is None:
            return

        # Right mouse button - start scaling only, don't select
        if event.button == 3:
            self.scaling = True
            self.scale_start = (x, y, self.canvas_scale)
            return

        # Only left mouse button (button 1) handles selection and placement
        if event.button != 1:
            return

        if self.placing_element:
            self._save_undo_state()
            self._add_element(self.placing_element, x, y)
            self.placing_element = None
            self._refresh_all()
            return

        clicked = self._get_element_at(x, y)
        if clicked is not None:
            self.selected_element = clicked
            self.dragging = True
            elem = self._get_current_elements()[clicked]
            pos = elem.get('position', {'x': 50, 'y': 50})
            self.drag_offset = (x - pos['x'], y - pos['y'])
        else:
            self.selected_element = None

        self._draw_canvas()
        self._draw_right_panel()
        self.fig.canvas.draw_idle()

    def _handle_right_panel_click(self, event):
        """Handle click on properties panel"""
        x, y = event.xdata, event.ydata
        if x is None or y is None:
            return

        # Check tab buttons first
        for y_min, y_max, x_min, x_max, tab_id in self.tab_buttons:
            if y_min <= y <= y_max and x_min <= x <= x_max:
                if self.props_tab != tab_id:
                    self.props_tab = tab_id
                    self._draw_right_panel()
                    self.fig.canvas.draw_idle()
                return

        # Check phase buttons
        for y_min, y_max, x_min, x_max, phase in self.phase_buttons:
            if y_min <= y <= y_max and x_min <= x <= x_max:
                self._save_undo_state()
                self._set_phase(phase)
                return

        # Check easing buttons
        for y_min, y_max, x_min, x_max, easing in self.easing_buttons:
            if y_min <= y <= y_max and x_min <= x <= x_max:
                self._save_undo_state()
                self._set_easing(easing)
                return

        # Check effect buttons
        for y_min, y_max, x_min, x_max, effect in self.effect_buttons:
            if y_min <= y <= y_max and x_min <= x <= x_max:
                self._save_undo_state()
                self._set_effect(effect)
                return

        # Check slider buttons
        for y_min, y_max, x_min, x_max, prop_name, min_val, max_val in self.slider_buttons:
            if y_min <= y <= y_max and x_min <= x <= x_max:
                self._save_undo_state()
                # Calculate value from click position
                pct = (x - x_min) / (x_max - x_min)
                pct = max(0, min(1, pct))
                new_val = min_val + pct * (max_val - min_val)
                # Round to 1 decimal
                new_val = round(new_val, 1)
                self._set_timing_prop(prop_name, new_val)
                return

        # Check property buttons
        for y_min, y_max, x_min, x_max, prop_name, elem_idx in self.prop_buttons:
            if y_min <= y <= y_max and x_min <= x <= x_max:
                self._save_undo_state()
                self._edit_property_by_index(prop_name, elem_idx)
                return

    def _handle_bottom_click(self, event):
        """Handle click on navigation bar"""
        x, y = event.xdata, event.ydata
        if x is None or y is None:
            return

        for x_min, x_max, y_min, y_max, action in self.nav_buttons:
            if x_min <= x <= x_max and y_min <= y <= y_max:
                if action == 'prev':
                    self._prev_step()
                elif action == 'next':
                    self._next_step()
                elif action == 'add':
                    self._add_step()
                elif action == 'del':
                    self._delete_step()
                return

    def _on_release(self, event):
        if self.dragging:
            self.unsaved = True
        self.dragging = False
        self.scaling = False
        self.scale_start = None

    def _on_motion(self, event):
        # Handle canvas scaling with right mouse button
        if self.scaling and self.scale_start is not None:
            if event.inaxes == self.ax_canvas and event.ydata is not None:
                start_x, start_y, start_scale = self.scale_start
                dy = event.ydata - start_y
                # Scale factor based on vertical drag
                scale_delta = dy * 0.02
                new_scale = max(0.5, min(3.0, start_scale + scale_delta))
                if abs(new_scale - self.canvas_scale) > 0.01:
                    self.canvas_scale = new_scale
                    self._update_canvas_zoom()
            return

        if not self.dragging or self.selected_element is None:
            return
        if event.inaxes != self.ax_canvas:
            return

        x, y = event.xdata, event.ydata
        if x is None or y is None:
            return

        elements = self._get_current_elements()
        if self.selected_element < len(elements):
            new_x = max(5, min(95, x - self.drag_offset[0]))
            new_y = max(5, min(95, y - self.drag_offset[1]))
            elements[self.selected_element]['position'] = {'x': new_x, 'y': new_y}
            self._refresh_canvas_only()

    def _update_canvas_zoom(self):
        """Update canvas view based on scale"""
        center = 50
        half_range = 50 / self.canvas_scale
        self.ax_canvas.set_xlim(center - half_range, center + half_range)
        self.ax_canvas.set_ylim(center - half_range, center + half_range)
        self.fig.canvas.draw_idle()

    def _on_scroll(self, event):
        if event.inaxes == self.ax_left:
            max_scroll = max(0, len(self.ELEMENTS) - 8)
            if event.button == 'up':
                self.scroll_offset = max(0, self.scroll_offset - 1)
            else:
                self.scroll_offset = min(max_scroll, self.scroll_offset + 1)
            self._draw_left_panel()
            self.fig.canvas.draw_idle()

    def _on_key(self, event):
        key = event.key

        # Undo/Redo
        if key == 'ctrl+z':
            self._undo()
            return
        elif key in ('ctrl+shift+z', 'ctrl+Z'):  # Shift makes Z uppercase
            self._redo()
            return

        if key == 'escape':
            self.placing_element = None
            self.selected_element = None
            self._refresh_all()
        elif key in ('delete', 'backspace'):
            self._save_undo_state()
            self._delete_selected()
        elif key == 'd':
            self._save_undo_state()
            self._duplicate_selected()
        elif key == 'e':
            self._save_undo_state()
            self._edit_selected()
        elif key == 's':
            self._save()
        elif key == 'o':
            self._open_file()
        elif key == 'n':
            self._new_file()
        elif key == 'g':
            self._generate()
        elif key == 'p':
            self._open_preview_window()
        elif key == 'left':
            self._prev_step()
        elif key == 'right':
            self._next_step()
        elif key == 'q':
            self._quit()

    # Preview window with animation controls
    def _open_preview_window(self):
        """Open a separate preview window with animation controls"""
        if self.preview_fig is not None:
            try:
                plt.close(self.preview_fig)
            except:
                pass

        self.preview_fig = plt.figure(figsize=(14, 9), facecolor='#08080c')
        self.preview_fig.canvas.manager.set_window_title(f'Preview: Step {self.current_step + 1}')

        self.preview_ax = self.preview_fig.add_axes([0.05, 0.15, 0.9, 0.8])
        self.preview_ax.set_facecolor(self.CANVAS_BG)
        for spine in self.preview_ax.spines.values():
            spine.set_color(self.colors['primary'])
            spine.set_linewidth(2)

        self.preview_controls_ax = self.preview_fig.add_axes([0.05, 0.02, 0.9, 0.10])
        self.preview_controls_ax.set_facecolor(self.PANEL_HEADER)
        self.preview_controls_ax.axis('off')

        self._render_preview_step()
        self._draw_preview_controls()

        self.preview_fig.canvas.mpl_connect('key_press_event', self._on_preview_key)
        self.preview_fig.canvas.mpl_connect('button_press_event', self._on_preview_click)

        self.preview_fig.show()

    def _render_preview_step(self):
        """Render current step in preview window"""
        if self.preview_ax is None:
            return

        ax = self.preview_ax
        ax.clear()
        ax.set_facecolor(self.CANVAS_BG)
        ax.set_xlim(0, 100)
        ax.set_ylim(0, 100)

        step = self._get_current_step()
        if step:
            if step.title:
                ax.text(50, 95, step.title, fontsize=18, fontweight='bold',
                        ha='center', va='top', color=self.colors['primary'])

            for elem in step.elements:
                self._draw_preview_element_full(ax, elem, self.animation_progress)

        ax.axis('off')
        for spine in ax.spines.values():
            spine.set_visible(True)
            spine.set_color(self.colors['primary'])
            spine.set_linewidth(2)

    def _apply_easing(self, t, easing):
        """Apply easing function to normalized time t (0-1)"""
        import math
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
        return t  # fallback to linear

    def _draw_preview_element_full(self, ax, elem, progress):
        """Draw element in full preview with animation progress"""
        phase = elem.get('animation_phase', 'early')
        phase_ranges = {
            'immediate': (0.0, 0.2),
            'early': (0.2, 0.4),
            'middle': (0.4, 0.6),
            'late': (0.6, 0.8),
            'final': (0.8, 1.0)
        }

        start, end = phase_ranges.get(phase, (0.2, 0.4))

        # Apply duration and delay from timing controls
        duration = elem.get('duration', 1.0)
        delay = elem.get('delay', 0.0)
        speed = elem.get('speed', 1.0)

        # Delay shifts the start point (delay of 1.0s = shift by 10%)
        start = start + delay * 0.1

        # Duration affects how long the element animates
        phase_duration = (end - start) * duration
        end = min(1.0, start + phase_duration)

        # Calculate base alpha
        if progress < start:
            alpha = 0.0
        elif progress >= end:
            alpha = 1.0
        else:
            t = (progress - start) / (end - start)
            # Apply easing
            easing = elem.get('easing', 'ease_in_out')
            alpha = self._apply_easing(t, easing)

        if alpha <= 0:
            return

        # Store speed for element-specific animations
        elem_speed = speed

        t = elem.get('type', 'text')
        pos = elem.get('position', {'x': 50, 'y': 50})
        x, y = pos['x'], pos['y']

        if t in ('text', 'typewriter_text'):
            content = elem.get('content', 'Text')
            if t == 'typewriter_text':
                # Apply speed to typewriter - faster speed = more characters visible
                type_progress = min(1.0, alpha * elem_speed)
                visible_chars = int(len(content) * type_progress)
                display_content = content[:visible_chars]
                if visible_chars < len(content):
                    display_content += '|'
                ax.text(x, y, display_content, fontsize=14, ha='center', va='center',
                       color=self.colors['text'], alpha=min(1.0, alpha * 2))
            else:
                ax.text(x, y, content, fontsize=14, ha='center', va='center',
                       color=self.colors['text'], alpha=alpha)

        elif t == 'box':
            w, h = elem.get('width', 25), elem.get('height', 12)
            ax.add_patch(FancyBboxPatch(
                (x - w/2, y - h/2), w, h,
                boxstyle="round,pad=0.3",
                facecolor='#1a1a24',
                edgecolor=self.colors['primary'],
                linewidth=1.5, alpha=alpha))
            if elem.get('title'):
                ax.text(x, y + h/4, elem['title'], fontsize=11,
                       fontweight='bold', ha='center', color=self.colors['primary'], alpha=alpha)

        elif t == 'bullet_list':
            items = elem.get('items', [])
            stagger = elem.get('stagger', 0.1)
            for j, item in enumerate(items):
                item_alpha = min(1.0, max(0, (alpha - j * stagger) / (1 - j * stagger))) if stagger else alpha
                if item_alpha > 0:
                    ax.text(x - 10, y + 6 - j * 5, f'* {item}',
                           fontsize=10, ha='left', color=self.colors['text'], alpha=item_alpha)

        elif t == 'comparison':
            w, h = elem.get('width', 50), elem.get('height', 18)
            ax.add_patch(FancyBboxPatch(
                (x - w/2, y - h/2), w/2 - 1, h,
                boxstyle="round,pad=0.2", facecolor='#1a1a24',
                edgecolor=self.colors['warning'], linewidth=1.5, alpha=alpha))
            ax.add_patch(FancyBboxPatch(
                (x + 1, y - h/2), w/2 - 1, h,
                boxstyle="round,pad=0.2", facecolor='#1a1a24',
                edgecolor=self.colors['success'], linewidth=1.5, alpha=alpha))
            if elem.get('left_title'):
                ax.text(x - w/4, y + h/3, elem['left_title'], fontsize=9,
                       fontweight='bold', ha='center', color=self.colors['warning'], alpha=alpha)
            if elem.get('right_title'):
                ax.text(x + w/4, y + h/3, elem['right_title'], fontsize=9,
                       fontweight='bold', ha='center', color=self.colors['success'], alpha=alpha)

        elif t in ('arrow', 'arc_arrow'):
            start = elem.get('start', {'x': x - 10, 'y': y})
            end = elem.get('end', {'x': x + 10, 'y': y})
            ex = start['x'] + (end['x'] - start['x']) * alpha
            ey = start['y'] + (end['y'] - start['y']) * alpha
            style = 'arc3,rad=0.2' if t == 'arc_arrow' else None
            ax.annotate('', xy=(ex, ey), xytext=(start['x'], start['y']),
                       arrowprops=dict(arrowstyle='-|>', lw=2,
                                      color=self.colors['primary'],
                                      connectionstyle=style))

        elif t == 'similarity_meter':
            r = elem.get('radius', 5)
            score = elem.get('score', 75)
            current_score = score * alpha
            ax.add_patch(Wedge((x, y), r, 0, 180,
                              facecolor='#1a1a24',
                              edgecolor=self.colors['dim'],
                              linewidth=1.5))
            fill_angle = 180 * (1 - current_score / 100)
            ax.add_patch(Wedge((x, y), r, fill_angle, 180,
                              facecolor=self.colors['success'],
                              edgecolor='none'))
            ax.text(x, y - 2, f"{int(current_score)}%", fontsize=10,
                   ha='center', va='center', color='white', fontweight='bold')

        elif t == 'progress_bar':
            w = elem.get('width', 18)
            current = elem.get('current', 5)
            total = elem.get('total', 10)
            ax.add_patch(Rectangle((x - w/2, y - 2), w, 4,
                                  facecolor='#1a1a24',
                                  edgecolor=self.colors['dim'],
                                  linewidth=1.5, alpha=alpha))
            fill = w * (current / max(total, 1)) * alpha
            ax.add_patch(Rectangle((x - w/2, y - 2), fill, 4,
                                  facecolor=self.colors['success'], alpha=alpha))

        elif t == 'neural_network':
            w, h = elem.get('width', 35), elem.get('height', 22)
            layers = elem.get('layers', [3, 4, 2])
            sp = w / (len(layers) + 1)
            for li, n in enumerate(layers):
                layer_alpha = min(1.0, max(0, alpha * len(layers) - li))
                lx = x - w/2 + (li + 1) * sp
                ns = h / (n + 1)
                for ni in range(n):
                    ny = y - h/2 + (ni + 1) * ns
                    ax.add_patch(Circle((lx, ny), 1.2,
                                       facecolor=self.colors['primary'],
                                       edgecolor='white', linewidth=0.5,
                                       alpha=layer_alpha))

        elif t == 'particle_flow':
            start_pos = elem.get('start', {'x': x - 15, 'y': y})
            end_pos = elem.get('end', {'x': x + 15, 'y': y})
            n = elem.get('num_particles', 15)
            # Apply speed to particle movement
            flow_alpha = min(1.0, alpha * elem_speed)
            for i in range(n):
                # Stagger particles and apply speed
                t_pos = ((i / n) + flow_alpha * 2) % 1.0
                px = start_pos['x'] + (end_pos['x'] - start_pos['x']) * t_pos
                py = start_pos['y'] + (end_pos['y'] - start_pos['y']) * t_pos
                # Add some vertical spread based on particle index
                spread = elem.get('spread', 0.5)
                py += np.sin(i * 1.5) * spread * 3
                size = 0.8 + np.sin(t_pos * np.pi) * 0.4
                particle_alpha = 0.3 + np.sin(t_pos * np.pi) * 0.6
                ax.add_patch(Circle((px, py), size,
                                   facecolor=self.colors['accent'],
                                   edgecolor='none', alpha=particle_alpha * alpha))

        elif t == 'code_block':
            w, h = elem.get('width', 30), elem.get('height', 15)
            ax.add_patch(FancyBboxPatch(
                (x - w/2, y - h/2), w, h,
                boxstyle="round,pad=0.2", facecolor='#0d1117',
                edgecolor=self.colors['dim'], linewidth=1.5, alpha=alpha))
            code = elem.get('code', '# code')[:40]
            ax.text(x - w/2 + 2, y + h/4, code, fontsize=8, family='monospace',
                   ha='left', va='center', color=self.colors['secondary'], alpha=alpha)

        elif t == 'code_execution':
            w = elem.get('width', 35)
            code_h, out_h = elem.get('code_height', 8), elem.get('output_height', 5)
            # Code box
            ax.add_patch(FancyBboxPatch(
                (x - w/2, y + 2), w, code_h,
                boxstyle="round,pad=0.2", facecolor='#0d1117',
                edgecolor=self.colors['dim'], linewidth=1, alpha=alpha))
            # Output box
            ax.add_patch(FancyBboxPatch(
                (x - w/2, y - out_h - 2), w, out_h,
                boxstyle="round,pad=0.2", facecolor='#1a1a24',
                edgecolor=self.colors['success'], linewidth=1, alpha=alpha))
            ax.text(x, y + 5, elem.get('code', '>>>')[: 25], fontsize=7, family='monospace',
                   ha='center', color=self.colors['text'], alpha=alpha)
            ax.text(x, y - out_h/2, elem.get('output', 'output')[:20], fontsize=7,
                   ha='center', color=self.colors['success'], alpha=alpha)

        elif t == 'checklist':
            items = elem.get('items', [])[:5]
            for j, item in enumerate(items):
                item_alpha = min(1.0, max(0, alpha * (len(items) + 1) - j))
                iy = y + 6 - j * 5
                ax.add_patch(Rectangle((x - 12, iy - 1), 2.5, 2.5,
                                       facecolor=self.colors['success'] if item_alpha > 0.5 else 'none',
                                       edgecolor=self.colors['success'], linewidth=1, alpha=item_alpha))
                ax.text(x - 8, iy, item[:15], fontsize=9, ha='left',
                       color=self.colors['text'], alpha=item_alpha)

        elif t == 'flow':
            steps = elem.get('steps', [])[:5]
            w = elem.get('width', 60)
            step_w = w / max(len(steps), 1)
            for j, step in enumerate(steps):
                step_alpha = min(1.0, max(0, alpha * (len(steps) + 1) - j))
                sx = x - w/2 + j * step_w + step_w/2
                ax.add_patch(FancyBboxPatch(
                    (sx - step_w/2 + 1, y - 4), step_w - 2, 8,
                    boxstyle="round,pad=0.2", facecolor='#1a1a24',
                    edgecolor=self.colors['primary'], linewidth=1, alpha=step_alpha))
                label = step.get('label', f'S{j+1}')[:6]
                ax.text(sx, y, label, fontsize=8, ha='center', va='center',
                       color=self.colors['text'], alpha=step_alpha)
                if j < len(steps) - 1:
                    ax.annotate('', xy=(sx + step_w/2 - 1, y), xytext=(sx + step_w/2 - 3, y),
                               arrowprops=dict(arrowstyle='->', lw=1, color=self.colors['dim']))

        elif t == 'grid':
            cols, rows = elem.get('columns', 2), elem.get('rows', 2)
            cw, ch = elem.get('cell_width', 15), elem.get('cell_height', 10)
            items = elem.get('items', [])
            for r in range(rows):
                for c in range(cols):
                    idx = r * cols + c
                    cell_alpha = min(1.0, max(0, alpha * (cols * rows + 1) - idx))
                    cx = x - (cols * cw) / 2 + c * cw + cw/2
                    cy = y + (rows * ch) / 2 - r * ch - ch/2
                    ax.add_patch(FancyBboxPatch(
                        (cx - cw/2 + 1, cy - ch/2 + 1), cw - 2, ch - 2,
                        boxstyle="round,pad=0.1", facecolor='#1a1a24',
                        edgecolor=self.colors['primary'], linewidth=1, alpha=cell_alpha))
                    if idx < len(items):
                        ax.text(cx, cy, items[idx].get('title', '')[:5], fontsize=7,
                               ha='center', va='center', color=self.colors['text'], alpha=cell_alpha)

        elif t == 'scatter_3d':
            # Show isometric projection for 3D preview
            w, h = 25, 20
            ax.add_patch(FancyBboxPatch(
                (x - w/2, y - h/2), w, h,
                boxstyle="round,pad=0.2", facecolor='#0d0d14',
                edgecolor=self.colors['primary'], linewidth=1.5, alpha=alpha))
            # Draw axes
            ax.plot([x - 8, x + 8], [y - 5, y - 5], color=self.colors['dim'], linewidth=0.5, alpha=alpha)
            ax.plot([x, x], [y - 5, y + 6], color=self.colors['dim'], linewidth=0.5, alpha=alpha)
            ax.plot([x, x - 6], [y - 5, y - 2], color=self.colors['dim'], linewidth=0.5, alpha=alpha)
            # Points
            points = elem.get('points', [])[:8]
            elev = elem.get('camera_elev', 20)
            azim = elem.get('camera_azim', 45)
            for i, pt in enumerate(points):
                pt_alpha = max(0.0, min(1.0, alpha * (len(points) + 1) - i))
                if pt_alpha <= 0:
                    continue
                # Simple isometric projection
                px = x + pt.get('x', 0) * 2 - pt.get('y', 0) * 0.5
                py = y + pt.get('z', 0) * 2 + pt.get('y', 0) * 0.3
                ax.add_patch(Circle((px, py), 0.8,
                                   facecolor=self.colors['accent'],
                                   edgecolor='white', linewidth=0.3, alpha=pt_alpha))

        elif t == 'vector_3d':
            w, h = 25, 20
            ax.add_patch(FancyBboxPatch(
                (x - w/2, y - h/2), w, h,
                boxstyle="round,pad=0.2", facecolor='#0d0d14',
                edgecolor=self.colors['primary'], linewidth=1.5, alpha=alpha))
            # Draw axes
            ax.plot([x - 8, x + 8], [y - 5, y - 5], color=self.colors['dim'], linewidth=0.5, alpha=alpha)
            ax.plot([x, x], [y - 5, y + 6], color=self.colors['dim'], linewidth=0.5, alpha=alpha)
            # Vectors
            vectors = elem.get('vectors', [])[:5]
            colors_list = ['primary', 'secondary', 'accent', 'warning', 'success']
            for i, vec in enumerate(vectors):
                vec_alpha = max(0.0, min(1.0, alpha * (len(vectors) + 1) - i))
                if vec_alpha <= 0:
                    continue
                vx = vec.get('x', 1) * 3
                vy = vec.get('y', 1) * 1.5
                vz = vec.get('z', 1) * 3
                # Isometric projection
                ex = x + vx - vy * 0.3
                ey = y + vz + vy * 0.2
                vec_color = vec.get('color', colors_list[i % len(colors_list)])
                ax.annotate('', xy=(ex, ey), xytext=(x, y),
                           arrowprops=dict(arrowstyle='->', lw=1.5,
                                          color=self.colors.get(vec_color, vec_color),
                                          alpha=vec_alpha))

        elif t == 'attention_heatmap':
            w, h = elem.get('width', 25), elem.get('height', 25)
            tokens = elem.get('tokens_x', ['A', 'B', 'C'])[:5]
            n = len(tokens)
            cell_size = min(w, h) / (n + 1)
            # Draw grid
            for i in range(n):
                for j in range(n):
                    cell_alpha = max(0.0, min(1.0, alpha * (n * n + 1) - (i * n + j)))
                    if cell_alpha <= 0:
                        continue
                    cx = x - w/2 + (j + 1.5) * cell_size
                    cy = y + h/2 - (i + 1.5) * cell_size
                    # Random weight for demo
                    weight = 0.3 + 0.7 * ((i + j) % 3) / 2
                    ax.add_patch(Rectangle(
                        (cx - cell_size/2, cy - cell_size/2), cell_size * 0.9, cell_size * 0.9,
                        facecolor=self.colors['accent'], alpha=weight * cell_alpha))
            # Labels
            for i, tok in enumerate(tokens):
                ax.text(x - w/2 + cell_size/2, y + h/2 - (i + 1.5) * cell_size,
                       tok[:3], fontsize=6, ha='center', va='center',
                       color=self.colors['text'], alpha=alpha)

        elif t == 'parameter_slider':
            w = elem.get('width', 25)
            label = elem.get('label', 'Param')[:12]
            val = elem.get('current_value', 0.5)
            min_v, max_v = elem.get('min_value', 0), elem.get('max_value', 1)
            ratio = (val - min_v) / (max_v - min_v) if max_v != min_v else 0.5
            # Label
            ax.text(x, y + 5, label, fontsize=10, fontweight='bold',
                   ha='center', va='center', color=self.colors['text'], alpha=alpha)
            # Track
            ax.add_patch(Rectangle((x - w/2, y - 1), w, 2,
                                  facecolor='#333', edgecolor='#555', linewidth=0.5, alpha=alpha))
            # Fill
            ax.add_patch(Rectangle((x - w/2, y - 1), w * ratio * alpha, 2,
                                  facecolor=self.colors['accent'], alpha=alpha))
            # Handle
            handle_x = x - w/2 + w * ratio * alpha
            ax.add_patch(Circle((handle_x, y), 1.5,
                               facecolor='white', edgecolor=self.colors['accent'],
                               linewidth=1.5, alpha=alpha))
            # Value
            ax.text(handle_x, y + 3, f'{val:.1f}', fontsize=8,
                   ha='center', va='bottom', color=self.colors['accent'], alpha=alpha)

        elif t == 'token_flow':
            w, h = elem.get('width', 40), elem.get('height', 20)
            input_text = elem.get('input_text', 'Hello')[:15]
            # Input box
            ax.add_patch(FancyBboxPatch(
                (x - w/2, y + h/4), w * 0.3, h * 0.4,
                boxstyle="round,pad=0.1", facecolor='#1a1a24',
                edgecolor=self.colors['dim'], linewidth=1, alpha=alpha))
            ax.text(x - w/2 + w * 0.15, y + h/4 + h * 0.2, input_text[:8], fontsize=7,
                   ha='center', va='center', color=self.colors['text'], alpha=alpha)
            # Tokens
            tokens = input_text.split()[:3] or ['tok']
            for i, tok in enumerate(tokens):
                tok_alpha = max(0.0, min(1.0, alpha * 3 - i))
                if tok_alpha <= 0:
                    continue
                tx = x - w * 0.1 + i * 8
                ax.add_patch(FancyBboxPatch(
                    (tx - 3, y - 2), 6, 4,
                    boxstyle="round,pad=0.1", facecolor='#1a1a24',
                    edgecolor=self.colors['accent'], linewidth=1, alpha=tok_alpha))
                ax.text(tx, y, tok[:4], fontsize=6, ha='center', va='center',
                       color=self.colors['accent'], alpha=tok_alpha)
            # Arrow
            ax.annotate('', xy=(x - w * 0.15, y + h * 0.1), xytext=(x - w * 0.3, y + h * 0.1),
                       arrowprops=dict(arrowstyle='->', lw=1, color=self.colors['dim']), alpha=alpha)

        else:
            w, h = elem.get('width', 18), elem.get('height', 10)
            ax.add_patch(FancyBboxPatch(
                (x - w/2, y - h/2), w, h,
                boxstyle="round,pad=0.2", facecolor='#1a1a24',
                edgecolor=self.colors['dim'], linewidth=1.5, linestyle='--', alpha=alpha))
            ax.text(x, y, t, fontsize=9, ha='center', va='center',
                   color=self.colors['dim'], alpha=alpha)

    def _draw_preview_controls(self):
        """Draw animation controls in preview window"""
        ax = self.preview_controls_ax
        ax.clear()
        ax.set_facecolor(self.PANEL_HEADER)
        ax.set_xlim(0, 100)
        ax.set_ylim(0, 100)

        # Play/Pause
        play_text = 'II' if self.animation_playing else '>'
        ax.text(5, 50, play_text, fontsize=18, ha='center', va='center',
               color=self.colors['primary'], fontweight='bold', family='monospace')

        # Progress bar
        bar_x, bar_y, bar_w, bar_h = 12, 35, 60, 30
        ax.add_patch(Rectangle((bar_x, bar_y), bar_w, bar_h,
                               facecolor='#1a1a24', edgecolor=self.colors['dim'], linewidth=1))
        ax.add_patch(Rectangle((bar_x, bar_y), bar_w * self.animation_progress, bar_h,
                               facecolor=self.colors['primary'], edgecolor='none'))

        ax.text(bar_x + bar_w / 2, 75, f'{int(self.animation_progress * 100)}%',
               fontsize=10, ha='center', va='center', color=self.colors['text'])

        # Phase indicators
        phases = ['imm', 'early', 'mid', 'late', 'final']
        phase_x = [0.0, 0.2, 0.4, 0.6, 0.8]
        for phase, px in zip(phases, phase_x):
            screen_x = bar_x + bar_w * px
            ax.axvline(screen_x, ymin=0.35, ymax=0.65, color=self.colors['dim'], linewidth=0.5)
            ax.text(screen_x, 20, phase, fontsize=6, ha='center', color=self.colors['dim'])

        # Loop toggle
        loop_color = self.colors['accent'] if self.animation_loop else self.colors['dim']
        ax.text(78, 50, 'LOOP', fontsize=9, ha='center', va='center', color=loop_color, fontweight='bold')

        # Step navigation
        ax.text(88, 50, '<', fontsize=16, ha='center', va='center', color=self.colors['text'])
        ax.text(95, 50, '>', fontsize=16, ha='center', va='center', color=self.colors['text'])

        ax.text(50, 5, 'Space: Play/Pause  |  Arrows: Scrub  |  L: Loop  |  R: Reset  |  Q: Close',
               fontsize=7, ha='center', va='bottom', color=self.colors['dim'])

        ax.axis('off')

        if self.preview_fig:
            self.preview_fig.canvas.draw_idle()

    def _on_preview_key(self, event):
        """Handle key events in preview window"""
        key = event.key
        if key == ' ':
            self.animation_playing = not self.animation_playing
            if self.animation_playing:
                self._start_animation()
            self._draw_preview_controls()
        elif key == 'left':
            self.animation_progress = max(0, self.animation_progress - 0.05)
            self._render_preview_step()
            self._draw_preview_controls()
        elif key == 'right':
            self.animation_progress = min(1, self.animation_progress + 0.05)
            self._render_preview_step()
            self._draw_preview_controls()
        elif key == 'r':
            self.animation_progress = 0
            self.animation_playing = False
            self._render_preview_step()
            self._draw_preview_controls()
        elif key == 'l':
            self.animation_loop = not self.animation_loop
            self._draw_preview_controls()
        elif key == 'q':
            plt.close(self.preview_fig)
            self.preview_fig = None
            self.preview_ax = None

    def _on_preview_click(self, event):
        """Handle click events in preview window"""
        if event.inaxes == self.preview_controls_ax:
            x = event.xdata
            if x is None:
                return

            if x < 10:
                self.animation_playing = not self.animation_playing
                if self.animation_playing:
                    self._start_animation()
                self._draw_preview_controls()

            elif 12 <= x <= 72:
                self.animation_progress = (x - 12) / 60
                self.animation_progress = max(0, min(1, self.animation_progress))
                self._render_preview_step()
                self._draw_preview_controls()

            elif 75 <= x <= 82:
                self.animation_loop = not self.animation_loop
                self._draw_preview_controls()

            elif 85 <= x <= 90:
                self._prev_step()
                self.animation_progress = 0
                self._render_preview_step()
                self._draw_preview_controls()
                if self.preview_fig:
                    self.preview_fig.canvas.manager.set_window_title(f'Preview: Step {self.current_step + 1}')

            elif 92 <= x <= 98:
                self._next_step()
                self.animation_progress = 0
                self._render_preview_step()
                self._draw_preview_controls()
                if self.preview_fig:
                    self.preview_fig.canvas.manager.set_window_title(f'Preview: Step {self.current_step + 1}')

    def _start_animation(self):
        """Start animation playback"""
        def animate():
            try:
                if not self.animation_playing or self.preview_fig is None:
                    return

                # Check if figure still exists and has a valid canvas
                if not plt.fignum_exists(self.preview_fig.number):
                    self.animation_playing = False
                    self.preview_fig = None
                    return

                self.animation_progress += 0.02
                if self.animation_progress >= 1.0:
                    if self.animation_loop:
                        self.animation_progress = 0
                    else:
                        self.animation_progress = 1.0
                        self.animation_playing = False

                self._render_preview_step()
                self._draw_preview_controls()

                if self.animation_playing and self.preview_fig is not None:
                    if self.preview_fig.canvas and self.preview_fig.canvas.manager:
                        self.preview_fig.canvas.draw_idle()
                        self.preview_fig.canvas.flush_events()
                        self.preview_fig.canvas.manager.window.after(33, animate)
            except Exception:
                # Preview window was closed, stop animation
                self.animation_playing = False
                self.preview_fig = None

        if self.preview_fig:
            animate()

    # Element operations
    def _add_element(self, elem_type, x, y):
        step = self._get_current_step()
        if not step:
            return

        elem = {'type': elem_type, 'position': {'x': x, 'y': y}, 'animation_phase': 'early'}

        defaults = {
            'text': {'content': 'New Text'},
            'typewriter_text': {'content': 'Typewriter...', 'show_cursor': True},
            'box': {'width': 25, 'height': 12, 'title': 'Title'},
            'bullet_list': {'items': ['Item 1', 'Item 2', 'Item 3']},
            'comparison': {'width': 50, 'height': 18, 'left_title': 'Before', 'right_title': 'After'},
            'arrow': {'start': {'x': x - 10, 'y': y}, 'end': {'x': x + 10, 'y': y}},
            'arc_arrow': {'start': {'x': x - 10, 'y': y}, 'end': {'x': x + 10, 'y': y}, 'arc_height': 8},
            'flow': {'width': 45, 'steps': [{'title': 'Step 1'}, {'title': 'Step 2'}]},
            'code_block': {'code': 'print("Hello")', 'width': 25, 'height': 10},
            'grid': {'columns': 2, 'rows': 2, 'items': [{'title': 'A'}, {'title': 'B'}, {'title': 'C'}, {'title': 'D'}]},
            'checklist': {'items': ['Task 1', 'Task 2']},
            'particle_flow': {'start': {'x': x - 15, 'y': y}, 'end': {'x': x + 15, 'y': y}, 'num_particles': 15},
            'similarity_meter': {'score': 75, 'radius': 5},
            'progress_bar': {'current': 5, 'total': 10, 'width': 18},
            'neural_network': {'layers': [3, 4, 2], 'width': 35, 'height': 22},
            'scatter_3d': {'points': [{'x': 1, 'y': 2, 'z': 1, 'label': 'A'}], 'width': 30, 'height': 25},
        }

        if elem_type in defaults:
            elem.update(defaults[elem_type])

        step.elements.append(elem)
        self.selected_element = len(step.elements) - 1
        self.unsaved = True

    def _delete_selected(self):
        if self.selected_element is None:
            return
        elements = self._get_current_elements()
        if self.selected_element < len(elements):
            del elements[self.selected_element]
            self.selected_element = None
            self.unsaved = True
            self._refresh_all()

    def _duplicate_selected(self):
        if self.selected_element is None:
            return
        elements = self._get_current_elements()
        if self.selected_element < len(elements):
            new_elem = copy.deepcopy(elements[self.selected_element])
            pos = new_elem.get('position', {'x': 50, 'y': 50})
            new_elem['position'] = {'x': pos['x'] + 5, 'y': pos['y'] - 5}
            elements.append(new_elem)
            self.selected_element = len(elements) - 1
            self.unsaved = True
            self._refresh_all()

    def _edit_selected(self):
        if self.selected_element is None:
            return
        elements = self._get_current_elements()
        if self.selected_element >= len(elements):
            return

        elem = elements[self.selected_element]
        self._show_edit_dialog(elem)

    def _show_edit_dialog(self, elem):
        """Show edit dialog for element"""
        try:
            root = Tk()
            root.withdraw()

            t = elem.get('type', 'unknown')

            if 'content' in elem:
                result = simpledialog.askstring("Edit Content",
                                               f"Content for {t}:",
                                               initialvalue=elem['content'],
                                               parent=root)
                if result is not None:
                    elem['content'] = result
                    self.unsaved = True

            elif 'title' in elem:
                result = simpledialog.askstring("Edit Title",
                                               f"Title for {t}:",
                                               initialvalue=elem['title'],
                                               parent=root)
                if result is not None:
                    elem['title'] = result
                    self.unsaved = True

            elif 'items' in elem:
                items_str = '\n'.join(elem['items'])
                result = simpledialog.askstring("Edit Items",
                                               "Items (one per line):",
                                               initialvalue=items_str,
                                               parent=root)
                if result is not None:
                    elem['items'] = [x.strip() for x in result.split('\n') if x.strip()]
                    self.unsaved = True

            elif 'score' in elem:
                result = simpledialog.askinteger("Edit Score", "Score (0-100):",
                                                initialvalue=elem['score'],
                                                minvalue=0, maxvalue=100,
                                                parent=root)
                if result is not None:
                    elem['score'] = result
                    self.unsaved = True

            root.destroy()
            self._refresh_all()

        except Exception as e:
            print(f"Edit error: {e}")

    def _edit_property(self, prop_name, elem):
        """Edit a specific property - handles all property types"""
        try:
            root = Tk()
            root.withdraw()
            result = None

            # Position properties
            if prop_name in ('x', 'y'):
                pos = elem.get('position', {'x': 50, 'y': 50})
                result = simpledialog.askinteger(f"Edit {prop_name.upper()}",
                                                f"{prop_name} (0-100):",
                                                initialvalue=int(pos[prop_name]),
                                                minvalue=0, maxvalue=100,
                                                parent=root)
                if result is not None:
                    if 'position' not in elem:
                        elem['position'] = {'x': 50, 'y': 50}
                    elem['position'][prop_name] = result
                    self.unsaved = True

            # Start position properties (for arrows, particle_flow)
            elif prop_name == 'start_x':
                start = elem.get('start', {'x': 30, 'y': 50})
                result = simpledialog.askinteger("Edit Start X", "start_x (0-100):",
                                                initialvalue=int(start['x']),
                                                minvalue=0, maxvalue=100, parent=root)
                if result is not None:
                    if 'start' not in elem:
                        elem['start'] = {'x': 30, 'y': 50}
                    elem['start']['x'] = result
                    self.unsaved = True

            elif prop_name == 'start_y':
                start = elem.get('start', {'x': 30, 'y': 50})
                result = simpledialog.askinteger("Edit Start Y", "start_y (0-100):",
                                                initialvalue=int(start['y']),
                                                minvalue=0, maxvalue=100, parent=root)
                if result is not None:
                    if 'start' not in elem:
                        elem['start'] = {'x': 30, 'y': 50}
                    elem['start']['y'] = result
                    self.unsaved = True

            # End position properties
            elif prop_name == 'end_x':
                end = elem.get('end', {'x': 70, 'y': 50})
                result = simpledialog.askinteger("Edit End X", "end_x (0-100):",
                                                initialvalue=int(end['x']),
                                                minvalue=0, maxvalue=100, parent=root)
                if result is not None:
                    if 'end' not in elem:
                        elem['end'] = {'x': 70, 'y': 50}
                    elem['end']['x'] = result
                    self.unsaved = True

            elif prop_name == 'end_y':
                end = elem.get('end', {'x': 70, 'y': 50})
                result = simpledialog.askinteger("Edit End Y", "end_y (0-100):",
                                                initialvalue=int(end['y']),
                                                minvalue=0, maxvalue=100, parent=root)
                if result is not None:
                    if 'end' not in elem:
                        elem['end'] = {'x': 70, 'y': 50}
                    elem['end']['y'] = result
                    self.unsaved = True

            # Size properties
            elif prop_name in ('width', 'height', 'radius'):
                result = simpledialog.askinteger(f"Edit {prop_name}",
                                                f"{prop_name} (1-100):",
                                                initialvalue=int(elem.get(prop_name, 20)),
                                                minvalue=1, maxvalue=100, parent=root)
                if result is not None:
                    elem[prop_name] = result
                    self.unsaved = True

            # String properties
            elif prop_name in ('content', 'title', 'code', 'input_text', 'label', 'output'):
                current = elem.get(prop_name, '')
                result = simpledialog.askstring(f"Edit {prop_name}", f"{prop_name}:",
                                               initialvalue=current, parent=root)
                if result is not None:
                    elem[prop_name] = result
                    self.unsaved = True

            # Numeric properties
            elif prop_name == 'score':
                result = simpledialog.askinteger("Edit Score", "Score (0-100):",
                                                initialvalue=elem.get('score', 75),
                                                minvalue=0, maxvalue=100, parent=root)
                if result is not None:
                    elem['score'] = result
                    self.unsaved = True

            elif prop_name == 'num_particles':
                result = simpledialog.askinteger("Edit Particles", "num_particles (5-100):",
                                                initialvalue=elem.get('num_particles', 15),
                                                minvalue=5, maxvalue=100, parent=root)
                if result is not None:
                    elem['num_particles'] = result
                    self.unsaved = True

            elif prop_name == 'arc_height':
                result = simpledialog.askinteger("Edit Arc Height", "arc_height (1-50):",
                                                initialvalue=elem.get('arc_height', 10),
                                                minvalue=1, maxvalue=50, parent=root)
                if result is not None:
                    elem['arc_height'] = result
                    self.unsaved = True

            elif prop_name in ('current', 'total'):
                result = simpledialog.askinteger(f"Edit {prop_name}", f"{prop_name} (0-1000):",
                                                initialvalue=elem.get(prop_name, 10),
                                                minvalue=0, maxvalue=1000, parent=root)
                if result is not None:
                    elem[prop_name] = result
                    self.unsaved = True

            # Float properties
            elif prop_name in ('current_value', 'min_value', 'max_value', 'spacing',
                               'cursor_blink_rate', 'spread', 'camera_elev', 'camera_azim'):
                result = simpledialog.askfloat(f"Edit {prop_name}", f"{prop_name}:",
                                              initialvalue=elem.get(prop_name, 0.5),
                                              parent=root)
                if result is not None:
                    elem[prop_name] = result
                    self.unsaved = True

            # More integer properties
            elif prop_name in ('columns', 'rows', 'cell_width', 'cell_height',
                               'fontsize', 'base_width', 'box_height', 'particle_size'):
                result = simpledialog.askinteger(f"Edit {prop_name}", f"{prop_name}:",
                                                initialvalue=int(elem.get(prop_name, 10)),
                                                minvalue=1, maxvalue=200, parent=root)
                if result is not None:
                    elem[prop_name] = result
                    self.unsaved = True

            # More string properties
            elif prop_name in ('left_title', 'right_title', 'language', 'bullet_char'):
                result = simpledialog.askstring(f"Edit {prop_name}", f"{prop_name}:",
                                               initialvalue=elem.get(prop_name, ''),
                                               parent=root)
                if result is not None:
                    elem[prop_name] = result
                    self.unsaved = True

            # Boolean properties (toggle)
            elif prop_name in ('show_cursor', 'stagger', 'show_connections', 'show_values',
                               'show_embeddings', 'rotate_camera'):
                current = elem.get(prop_name, True)
                elem[prop_name] = not current
                self.unsaved = True

            # Choice properties (cycle through options)
            elif prop_name == 'orientation':
                current = elem.get('orientation', 'horizontal')
                elem['orientation'] = 'vertical' if current == 'horizontal' else 'horizontal'
                self.unsaved = True

            elif prop_name == 'direction':
                current = elem.get('direction', 'up')
                elem['direction'] = 'down' if current == 'up' else 'up'
                self.unsaved = True

            # List properties - open list editor
            elif prop_name in ('items', 'steps', 'events', 'messages', 'models',
                               'tokens_x', 'before_weights', 'after_weights',
                               'points', 'vectors', 'comparison_rows'):
                self._edit_list_property(elem, prop_name, root)

            # Neural network layers
            elif prop_name == 'layers':
                layers = elem.get('layers', [3, 5, 5, 2])
                layers_str = ','.join(map(str, layers))
                result = simpledialog.askstring("Edit Layers",
                                               "Layer sizes (comma-separated):\ne.g. 3,5,5,2",
                                               initialvalue=layers_str, parent=root)
                if result is not None:
                    try:
                        new_layers = [int(x.strip()) for x in result.split(',') if x.strip()]
                        if new_layers:
                            elem['layers'] = new_layers
                            self.unsaved = True
                    except ValueError:
                        pass

            root.destroy()
            self._refresh_all()

        except Exception as e:
            print(f"Edit error: {e}")

    def _edit_list_property(self, elem, prop_name, root):
        """Edit list-type properties with appropriate dialog"""
        current = elem.get(prop_name, [])

        if prop_name == 'items':
            # Simple string list
            if isinstance(current, list) and all(isinstance(x, str) for x in current):
                items_str = '\n'.join(current)
            else:
                items_str = ''
            result = simpledialog.askstring(f"Edit {prop_name}",
                                           "Items (one per line):",
                                           initialvalue=items_str, parent=root)
            if result is not None:
                elem[prop_name] = [x.strip() for x in result.split('\n') if x.strip()]
                self.unsaved = True

        elif prop_name in ('before_weights', 'after_weights'):
            # Float list
            weights_str = ','.join(map(str, current)) if current else '0.5,0.3,0.8'
            result = simpledialog.askstring(f"Edit {prop_name}",
                                           "Weights (comma-separated, 0-1):",
                                           initialvalue=weights_str, parent=root)
            if result is not None:
                try:
                    elem[prop_name] = [float(x.strip()) for x in result.split(',') if x.strip()]
                    self.unsaved = True
                except ValueError:
                    pass

        elif prop_name == 'tokens_x':
            # Token list
            tokens_str = ','.join(current) if current else 'The,cat,sat'
            result = simpledialog.askstring(f"Edit {prop_name}",
                                           "Tokens (comma-separated):",
                                           initialvalue=tokens_str, parent=root)
            if result is not None:
                elem[prop_name] = [x.strip() for x in result.split(',') if x.strip()]
                # Also update tokens_y to match
                elem['tokens_y'] = elem[prop_name]
                self.unsaved = True

        elif prop_name == 'points':
            # 3D points - show simplified editor
            pts_count = len(current)
            result = simpledialog.askinteger("Edit Points",
                                            f"Currently {pts_count} points.\nHow many points?",
                                            initialvalue=pts_count, minvalue=0, maxvalue=50,
                                            parent=root)
            if result is not None and result != pts_count:
                # Generate sample points
                import numpy as np
                elem[prop_name] = [
                    {'x': np.random.uniform(-3, 3),
                     'y': np.random.uniform(-3, 3),
                     'z': np.random.uniform(-3, 3),
                     'label': f'P{i}'}
                    for i in range(result)
                ]
                self.unsaved = True

        elif prop_name == 'vectors':
            # 3D vectors - show simplified editor
            vecs_count = len(current)
            result = simpledialog.askinteger("Edit Vectors",
                                            f"Currently {vecs_count} vectors.\nHow many vectors?",
                                            initialvalue=vecs_count, minvalue=0, maxvalue=20,
                                            parent=root)
            if result is not None and result != vecs_count:
                import numpy as np
                colors = ['primary', 'secondary', 'accent', 'warning', 'success']
                elem[prop_name] = [
                    {'x': np.random.uniform(-2, 2),
                     'y': np.random.uniform(-2, 2),
                     'z': np.random.uniform(-2, 2),
                     'label': f'V{i}',
                     'color': colors[i % len(colors)]}
                    for i in range(result)
                ]
                self.unsaved = True

        elif prop_name == 'steps':
            # Flow steps
            steps_str = '\n'.join([s.get('label', '') for s in current]) if current else ''
            result = simpledialog.askstring(f"Edit {prop_name}",
                                           "Steps (one per line):",
                                           initialvalue=steps_str, parent=root)
            if result is not None:
                elem[prop_name] = [{'label': x.strip()} for x in result.split('\n') if x.strip()]
                self.unsaved = True

        else:
            # Generic message for complex list types
            messagebox.showinfo("Edit List",
                               f"{prop_name} contains {len(current)} items.\n"
                               "Edit the JSON directly for complex list types.",
                               parent=root)

    def _set_phase(self, phase):
        if self.selected_element is not None:
            elements = self._get_current_elements()
            if self.selected_element < len(elements):
                elements[self.selected_element]['animation_phase'] = phase
                self.unsaved = True
                self._draw_right_panel()
                self.fig.canvas.draw_idle()

    def _set_easing(self, easing):
        if self.selected_element is not None:
            elements = self._get_current_elements()
            if self.selected_element < len(elements):
                elements[self.selected_element]['easing'] = easing
                self.unsaved = True
                self._draw_right_panel()
                self.fig.canvas.draw_idle()

    def _set_effect(self, effect):
        if self.selected_element is not None:
            elements = self._get_current_elements()
            if self.selected_element < len(elements):
                elements[self.selected_element]['continuous_effect'] = effect
                self.unsaved = True
                self._draw_right_panel()
                self.fig.canvas.draw_idle()

    def _set_timing_prop(self, prop_name, value):
        """Set a timing property (duration, delay, speed)"""
        if self.selected_element is not None:
            elements = self._get_current_elements()
            if self.selected_element < len(elements):
                elements[self.selected_element][prop_name] = value
                self.unsaved = True
                self._draw_right_panel()
                self.fig.canvas.draw_idle()

    def _edit_property_by_index(self, prop_name, elem_idx):
        """Edit property using element index for persistence"""
        elements = self._get_current_elements()
        if elem_idx < len(elements):
            elem = elements[elem_idx]
            self._edit_property(prop_name, elem)

    # Step operations
    def _add_step(self):
        idx = len(self.schema.steps) + 1
        self.schema.steps.append(Step(name=f"Step {idx}", title=f"New Step {idx}", elements=[]))
        self.current_step = len(self.schema.steps) - 1
        self.selected_element = None
        self.unsaved = True
        self._refresh_all()

    def _delete_step(self):
        if len(self.schema.steps) <= 1:
            return
        del self.schema.steps[self.current_step]
        if self.current_step >= len(self.schema.steps):
            self.current_step = len(self.schema.steps) - 1
        self.selected_element = None
        self.unsaved = True
        self._refresh_all()

    def _next_step(self):
        if self.current_step < len(self.schema.steps) - 1:
            self.current_step += 1
            self.selected_element = None
            self._refresh_all()

    def _prev_step(self):
        if self.current_step > 0:
            self.current_step -= 1
            self.selected_element = None
            self._refresh_all()

    # File operations
    def _new_file(self):
        self.schema = self._create_empty_schema()
        self.schema_path = "schemas/new_presentation.json"
        self.current_step = 0
        self.selected_element = None
        self.unsaved = False
        self.undo_stack.clear()
        self.redo_stack.clear()
        if not self.schema.steps:
            self.schema.steps.append(Step(name="Step 1", title="New Step", elements=[]))
        self._refresh_all()

    def _open_file(self):
        try:
            root = Tk()
            root.withdraw()
            root.attributes('-topmost', True)

            path = filedialog.askopenfilename(
                title="Open Presentation",
                initialdir="schemas",
                filetypes=[("JSON", "*.json"), ("All", "*.*")]
            )
            root.destroy()

            if path:
                self.schema = PresentationSchema.from_file(path)
                self.schema_path = path
                self.current_step = 0
                self.selected_element = None
                self.unsaved = False
                self.undo_stack.clear()
                self.redo_stack.clear()
                if not self.schema.steps:
                    self.schema.steps.append(Step(name="Step 1", title="New Step", elements=[]))
                self._refresh_all()
        except Exception as e:
            print(f"Open error: {e}")

    def _save(self):
        try:
            Path(self.schema_path).parent.mkdir(exist_ok=True)
            self.schema.to_file(self.schema_path)
            self.unsaved = False
            print(f"Saved: {self.schema_path}")
        except Exception as e:
            print(f"Save error: {e}")

    def _generate(self):
        try:
            self._save()
            from tools.generator import PresentationGenerator
            output = Path('presentations') / f"{self.schema.name}_presentation.py"
            PresentationGenerator(self.schema).to_file(str(output))
            print(f"Generated: {output}")
        except Exception as e:
            print(f"Generate error: {e}")

    def _quit(self):
        if self.unsaved:
            print("Unsaved changes! Press Q again to quit.")
            self.unsaved = False
            return
        if self.preview_fig:
            plt.close(self.preview_fig)
        plt.close(self.fig)

    def show(self):
        plt.show()


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Visual Presentation Designer v7")
    parser.add_argument('schema', nargs='?', help="JSON schema to edit")
    parser.add_argument('--new', '-n', help="Create new with name")
    args = parser.parse_args()

    path = f"schemas/{args.new}.json" if args.new else args.schema
    VisualDesigner(path).show()


if __name__ == "__main__":
    main()
