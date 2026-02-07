"""
Advanced Features Test
Test presentation for all new element types
"""

import sys
import os
import numpy as np
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle, Wedge
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import proj3d, Axes3D

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core import BasePresentation, PresentationStyle
from core.animations import AnimationHelper
from core.visual_effects import (
    ParticleSystem, SimilarityMeter, ProgressIndicator,
    WeightDeltaVisualizer, AnimationHelpers
)


class Arrow3D(FancyArrowPatch):
    """Custom 3D arrow for visualization"""
    def __init__(self, xs, ys, zs, *args, **kwargs):
        super().__init__((0, 0), (0, 0), *args, **kwargs)
        self._verts3d = xs, ys, zs

    def do_3d_projection(self, renderer=None):
        xs3d, ys3d, zs3d = self._verts3d
        xs, ys, zs = proj3d.proj_transform(xs3d, ys3d, zs3d, self.axes.M)
        self.set_positions((xs[0], ys[0]), (xs[1], ys[1]))
        return np.min(zs)


class TestAdvancedPresentation(BasePresentation):
    """Advanced Features Test"""

    def __init__(self):
        """Initialize the presentation"""
        step_names = [
            'Landing',
            'Typewriter Demo',
            'Visual Widgets',
            'Weight Comparison',
            'Neural Network',
            'Arc Arrow',
            '3D Scatter',
            'Step 7',
            'Step 8'
        ]

        super().__init__("Advanced Features Test", step_names)

        self.show_landing_page()

    def get_frames_for_step(self, step: int) -> int:
        """Get animation frame count for each step"""
        if False: pass
        elif step == 1: return 90
        elif step == 2: return 90
        elif step == 3: return 120
        elif step == 4: return 120
        elif step == 5: return 90
        elif step == 6: return 120
        return 60

    def show_landing_page(self):
        """Display landing page"""
        self.fig.clear()
        ax = self.fig.add_subplot(111)
        ax.axis('off')
        ax.set_xlim(0, 100)
        ax.set_ylim(0, 100)

        # Main title box
        title_box = FancyBboxPatch(
            (10, 55), 80, 25,
            boxstyle="round,pad=2",
            facecolor=self.colors['bg_light'],
            edgecolor=self.colors['primary'],
            linewidth=4,
            alpha=0.95
        )
        ax.add_patch(title_box)

        ax.text(50, 72, 'Advanced Features',
                fontsize=66, fontweight='bold', ha='center', va='center',
                color=self.colors['primary'])

        ax.text(50, 64, 'Testing New Capabilities',
                fontsize=30, ha='center', va='center',
                color=self.colors['text'], alpha=0.8, style='italic')

        ax.text(50, 45, 'All element types in action',
                fontsize=27, ha='center', va='center',
                color=self.colors['accent'], alpha=0.9)

        # Instructions box
        instr_box = FancyBboxPatch(
            (25, 15), 50, 15,
            boxstyle="round,pad=1",
            facecolor=self.colors['bg_light'],
            edgecolor=self.colors['secondary'],
            linewidth=3,
            alpha=0.9
        )
        ax.add_patch(instr_box)

        ax.text(50, 25, '>> Druk op SPATIE om te beginnen <<',
                fontsize=30, ha='center', va='center',
                color=self.colors['secondary'], fontweight='bold')

        ax.text(50, 20, 'SPACE=Volgende | B=Vorige | R=Reset | Q=Afsluiten',
                fontsize=18, ha='center', va='center',
                color=self.colors['dim'], style='italic')

        ax.text(50, 5, 'Press SPACE to start',
                fontsize=21, ha='center', va='center',
                color=self.colors['text'], alpha=0.5)

        plt.tight_layout()

    def animate_step(self, frame: int):
        """Animate current step"""
        total_frames = self.get_frames_for_step(self.current_step)
        progress = frame / (total_frames - 1) if total_frames > 1 else 1

        if self.current_step == 0:
            pass  # Landing is static
        elif self.current_step == 1:
            self.draw_typewriter_demo(progress)
        elif self.current_step == 2:
            self.draw_visual_widgets(progress)
        elif self.current_step == 3:
            self.draw_weight_comparison(progress)
        elif self.current_step == 4:
            self.draw_neural_network(progress)
        elif self.current_step == 5:
            self.draw_arc_arrow(progress)
        elif self.current_step == 6:
            self.draw_3d_scatter(progress)
        elif self.current_step == 7:
            self.draw_step_7(progress)
        elif self.current_step == 8:
            self.draw_step_8(progress)

        if frame >= total_frames - 1:
            self.is_animating = False

    def draw_current_step_static(self):
        """Draw current step without animation"""
        if self.current_step == -1:
            self.show_landing_page()
        elif self.current_step == 1:
            self.draw_typewriter_demo(1.0)
        elif self.current_step == 2:
            self.draw_visual_widgets(1.0)
        elif self.current_step == 3:
            self.draw_weight_comparison(1.0)
        elif self.current_step == 4:
            self.draw_neural_network(1.0)
        elif self.current_step == 5:
            self.draw_arc_arrow(1.0)
        elif self.current_step == 6:
            self.draw_3d_scatter(1.0)
        elif self.current_step == 7:
            self.draw_step_7(1.0)
        elif self.current_step == 8:
            self.draw_step_8(1.0)
        plt.draw()

    def draw_typewriter_demo(self, progress: float):
        """Step 1: Typewriter Demo"""
        self.fig.clear()
        ax = self.fig.add_subplot(111)
        ax.axis('off')
        ax.set_xlim(0, 100)
        ax.set_ylim(0, 100)

        # Title
        title_alpha = min(1.0, progress / 0.2)
        ax.text(50, 95, 'Typewriter Effect',
                fontsize=45, fontweight='bold', ha='center', va='top',
                color=self.colors['primary'], alpha=title_alpha)

        # Typewriter text with cursor
        if progress > 0.2:
            full_text = 'This text appears character by character...'
            type_progress = min(1.0, (progress - 0.2) / 0.2)
            num_chars = int(len(full_text) * type_progress)
            visible_text = full_text[:num_chars]

            # Blinking cursor
            show_cursor = num_chars < len(full_text) and int(progress * 20.0) % 2 == 0
            cursor = '▌' if show_cursor else ''

            ax.text(50, 50, visible_text + cursor,
                    fontsize=28, fontweight='normal',
                    ha='center', va='center',
                    color=self.colors['text'])

        if progress > 0.6:
            t = min(1.0, (progress - 0.6) / 0.20000000000000007)
            text_alpha = t * t * (3 - 2 * t)
            scale = 1.0 + 0.1 * np.sin(progress * 2 * np.pi * 2.0)
            effective_fontsize = 24 * scale
            ax.text(50, 30, 'With pulse effect',
                    fontsize=effective_fontsize, fontweight='normal',
                    ha='center', va='center',
                    color=self.colors['accent'], alpha=text_alpha)

        if progress > 0.2:
            t = min(1.0, (progress - 0.2) / 0.2)
            text_alpha = t * t * (3 - 2 * t)
            effective_fontsize = 24
            ax.text(16.170987702729516, 73.05610281886553, 'New Text',
                    fontsize=effective_fontsize, fontweight='normal',
                    ha='center', va='center',
                    color=self.colors['text'], alpha=text_alpha)

        if progress > 0.2:
            t = min(1.0, (progress - 0.2) / 0.2)
            text_alpha = t * t * (3 - 2 * t)
            effective_fontsize = 24
            ax.text(24.762407602956703, 25.831314688394627, 'test',
                    fontsize=effective_fontsize, fontweight='normal',
                    ha='center', va='center',
                    color=self.colors['text'], alpha=text_alpha)

        self.add_status_indicator(progress < 1.0)

    def draw_visual_widgets(self, progress: float):
        """Step 2: Visual Widgets"""
        self.fig.clear()
        ax = self.fig.add_subplot(111)
        ax.axis('off')
        ax.set_xlim(0, 100)
        ax.set_ylim(0, 100)

        # Title
        title_alpha = min(1.0, progress / 0.2)
        ax.text(50, 95, 'Visual Effect Widgets',
                fontsize=45, fontweight='bold', ha='center', va='top',
                color=self.colors['primary'], alpha=title_alpha)

        # Similarity meter
        if progress > 0.2:
            meter_progress = min(1.0, (progress - 0.2) / 0.2)
            target_score = 85
            current_score = target_score * min(1.0, meter_progress * 2)

            # Background arc
            bg_wedge = Wedge((25, 60), 10, 0, 180,
                            facecolor='#1a1a1a', edgecolor='#404040',
                            linewidth=2, alpha=0.9 * meter_progress)
            ax.add_patch(bg_wedge)

            # Score arc color
            if current_score < 50:
                meter_color = self.colors['warning']
            elif current_score < 75:
                meter_color = self.colors['accent']
            else:
                meter_color = self.colors['success']

            angle = 180 * (current_score / 100)
            score_wedge = Wedge((25, 60), 10 * 0.9, 0, angle,
                               facecolor=meter_color, edgecolor='none',
                               alpha=0.8 * meter_progress)
            ax.add_patch(score_wedge)

            # Center circle cutout
            center = Circle((25, 60), 10 * 0.6,
                           facecolor=self.colors['bg'], edgecolor='none', zorder=10)
            ax.add_patch(center)

            # Score text
            ax.text(25, 60, f'{int(current_score)}%',
                   fontsize=28, fontweight='bold', ha='center', va='center',
                   color=meter_color, alpha=meter_progress)

            # Label
            ax.text(25, 48, 'Accuracy',
                   fontsize=18, ha='center', va='top',
                   color=self.colors['text'], alpha=meter_progress * 0.7)

        # Progress bar
        if progress > 0.2:
            bar_progress = min(1.0, (progress - 0.2) / 0.2)

            # Background
            bg_box = FancyBboxPatch(
                (62.5, 58.0),
                25, 4,
                boxstyle="round,pad=0.2",
                facecolor='#1a1a1a',
                edgecolor='#404040',
                linewidth=2,
                alpha=0.9 * bar_progress
            )
            ax.add_patch(bg_box)

            # Progress fill
            fill_ratio = 7 / 10
            fill_width = 25 * fill_ratio * bar_progress
            fill_box = FancyBboxPatch(
                (62.5, 58.0),
                fill_width, 4,
                boxstyle="round,pad=0.2",
                facecolor=self.colors['success'],
                edgecolor='none',
                alpha=0.8 * bar_progress
            )
            ax.add_patch(fill_box)

            # Counter text
            ax.text(75, 60, f'7/10',
                   fontsize=16, fontweight='bold', ha='center', va='center',
                   color='white', zorder=20, alpha=bar_progress)

            # Label
            ax.text(75, 65.5, 'Training Epochs',
                   fontsize=14, ha='center', va='bottom',
                   color=self.colors['text'], alpha=bar_progress * 0.8)

        # Particle flow animation
        if progress > 0.4:
            flow_progress = min(1.0, (progress - 0.4) / 0.19999999999999996)
            np.random.seed(42)  # Consistent randomness

            for i in range(25):
                # Stagger particle start times
                phase_offset = np.random.rand() * 0.3
                particle_prog = max(0, min(1, (flow_progress - phase_offset) / (1 - 0.3)))

                if particle_prog > 0:
                    # Interpolate position with random offset
                    offset = np.random.randn(2) * 0.5
                    px = 10 + (90 - 10) * particle_prog + offset[0] * (1 - particle_prog)
                    py = 35 + (35 - 35) * particle_prog + offset[1] * (1 - particle_prog)

                    # Fade in/out
                    particle_alpha = min(particle_prog * 3, (1 - particle_prog) * 3, 1.0)

                    ax.scatter([px], [py], c=[self.colors['accent']],
                              s=30, alpha=particle_alpha,
                              edgecolors='none', zorder=100)

        self.add_status_indicator(progress < 1.0)

    def draw_weight_comparison(self, progress: float):
        """Step 3: Weight Comparison"""
        self.fig.clear()
        ax = self.fig.add_subplot(111)
        ax.axis('off')
        ax.set_xlim(0, 100)
        ax.set_ylim(0, 100)

        # Title
        title_alpha = min(1.0, progress / 0.2)
        ax.text(50, 95, 'Weight Delta Visualization',
                fontsize=45, fontweight='bold', ha='center', va='top',
                color=self.colors['primary'], alpha=title_alpha)

        # Weight comparison
        if progress > 0.2:
            comp_progress = min(1.0, (progress - 0.2) / 0.2)

            # Weight 1
            w0_y = 64.375
            w0_before = 0.5
            w0_after = 0.7
            w0_delta_pct = 40.0

            # Before bar
            if comp_progress > 0.3:
                before_alpha = min(1.0, (comp_progress - 0.3) / 0.2)
                ax.barh(w0_y, w0_before * 20, 4.375,
                       left=25, color='#60A5FA',
                       alpha=0.6 * before_alpha, edgecolor='white', linewidth=0.5)
                ax.text(23, w0_y, 'W1',
                       fontsize=12, ha='right', va='center',
                       color=self.colors['text'], alpha=before_alpha)

            # After bar
            if comp_progress > 0.5:
                after_alpha = min(1.0, (comp_progress - 0.5) / 0.2)
                ax.barh(w0_y, w0_after * 20, 4.375,
                       left=55, color=self.colors['success'],
                       alpha=0.8 * after_alpha, edgecolor='white', linewidth=0.5)

            # Delta arrow
            if comp_progress > 0.7 and abs(w0_delta_pct) > 5:
                arrow_alpha = min(1.0, (comp_progress - 0.7) / 0.3)
                ax.annotate('', xy=(54, w0_y),
                           xytext=(50, w0_y),
                           arrowprops=dict(arrowstyle='->', color=self.colors['success'],
                                          lw=2), alpha=arrow_alpha)
                ax.text(51, w0_y + 2.5,
                       f'{w0_delta_pct:+.0f}%',
                       fontsize=11, ha='center', va='bottom',
                       color=self.colors['success'], fontweight='bold',
                       alpha=arrow_alpha)

            # Weight 2
            w1_y = 58.125
            w1_before = 0.3
            w1_after = 0.5
            w1_delta_pct = 66.7

            # Before bar
            if comp_progress > 0.3:
                before_alpha = min(1.0, (comp_progress - 0.3) / 0.2)
                ax.barh(w1_y, w1_before * 20, 4.375,
                       left=25, color='#60A5FA',
                       alpha=0.6 * before_alpha, edgecolor='white', linewidth=0.5)
                ax.text(23, w1_y, 'W2',
                       fontsize=12, ha='right', va='center',
                       color=self.colors['text'], alpha=before_alpha)

            # After bar
            if comp_progress > 0.5:
                after_alpha = min(1.0, (comp_progress - 0.5) / 0.2)
                ax.barh(w1_y, w1_after * 20, 4.375,
                       left=55, color=self.colors['success'],
                       alpha=0.8 * after_alpha, edgecolor='white', linewidth=0.5)

            # Delta arrow
            if comp_progress > 0.7 and abs(w1_delta_pct) > 5:
                arrow_alpha = min(1.0, (comp_progress - 0.7) / 0.3)
                ax.annotate('', xy=(54, w1_y),
                           xytext=(50, w1_y),
                           arrowprops=dict(arrowstyle='->', color=self.colors['success'],
                                          lw=2), alpha=arrow_alpha)
                ax.text(51, w1_y + 2.5,
                       f'{w1_delta_pct:+.0f}%',
                       fontsize=11, ha='center', va='bottom',
                       color=self.colors['success'], fontweight='bold',
                       alpha=arrow_alpha)

            # Weight 3
            w2_y = 51.875
            w2_before = 0.8
            w2_after = 0.6
            w2_delta_pct = -25.0

            # Before bar
            if comp_progress > 0.3:
                before_alpha = min(1.0, (comp_progress - 0.3) / 0.2)
                ax.barh(w2_y, w2_before * 20, 4.375,
                       left=25, color='#60A5FA',
                       alpha=0.6 * before_alpha, edgecolor='white', linewidth=0.5)
                ax.text(23, w2_y, 'W3',
                       fontsize=12, ha='right', va='center',
                       color=self.colors['text'], alpha=before_alpha)

            # After bar
            if comp_progress > 0.5:
                after_alpha = min(1.0, (comp_progress - 0.5) / 0.2)
                ax.barh(w2_y, w2_after * 20, 4.375,
                       left=55, color=self.colors['warning'],
                       alpha=0.8 * after_alpha, edgecolor='white', linewidth=0.5)

            # Delta arrow
            if comp_progress > 0.7 and abs(w2_delta_pct) > 5:
                arrow_alpha = min(1.0, (comp_progress - 0.7) / 0.3)
                ax.annotate('', xy=(46, w2_y),
                           xytext=(50, w2_y),
                           arrowprops=dict(arrowstyle='->', color=self.colors['warning'],
                                          lw=2), alpha=arrow_alpha)
                ax.text(51, w2_y + 2.5,
                       f'{w2_delta_pct:+.0f}%',
                       fontsize=11, ha='center', va='bottom',
                       color=self.colors['warning'], fontweight='bold',
                       alpha=arrow_alpha)

            # Weight 4
            w3_y = 45.625
            w3_before = 0.2
            w3_after = 0.4
            w3_delta_pct = 100.0

            # Before bar
            if comp_progress > 0.3:
                before_alpha = min(1.0, (comp_progress - 0.3) / 0.2)
                ax.barh(w3_y, w3_before * 20, 4.375,
                       left=25, color='#60A5FA',
                       alpha=0.6 * before_alpha, edgecolor='white', linewidth=0.5)
                ax.text(23, w3_y, 'W4',
                       fontsize=12, ha='right', va='center',
                       color=self.colors['text'], alpha=before_alpha)

            # After bar
            if comp_progress > 0.5:
                after_alpha = min(1.0, (comp_progress - 0.5) / 0.2)
                ax.barh(w3_y, w3_after * 20, 4.375,
                       left=55, color=self.colors['success'],
                       alpha=0.8 * after_alpha, edgecolor='white', linewidth=0.5)

            # Delta arrow
            if comp_progress > 0.7 and abs(w3_delta_pct) > 5:
                arrow_alpha = min(1.0, (comp_progress - 0.7) / 0.3)
                ax.annotate('', xy=(54, w3_y),
                           xytext=(50, w3_y),
                           arrowprops=dict(arrowstyle='->', color=self.colors['success'],
                                          lw=2), alpha=arrow_alpha)
                ax.text(51, w3_y + 2.5,
                       f'{w3_delta_pct:+.0f}%',
                       fontsize=11, ha='center', va='bottom',
                       color=self.colors['success'], fontweight='bold',
                       alpha=arrow_alpha)

        if progress > 0.0:
            t = min(1.0, (progress - 0.0) / 0.2)
            text_alpha = t * t * (3 - 2 * t)
            effective_fontsize = 20
            ax.text(50, 80, 'Before → After',
                    fontsize=effective_fontsize, fontweight='normal',
                    ha='center', va='center',
                    color=self.colors['dim'], alpha=text_alpha)

        self.add_status_indicator(progress < 1.0)

    def draw_neural_network(self, progress: float):
        """Step 4: Neural Network"""
        self.fig.clear()
        ax = self.fig.add_subplot(111)
        ax.axis('off')
        ax.set_xlim(0, 100)
        ax.set_ylim(0, 100)

        # Title
        title_alpha = min(1.0, progress / 0.2)
        ax.text(50, 95, 'Neural Network Diagram',
                fontsize=45, fontweight='bold', ha='center', va='top',
                color=self.colors['primary'], alpha=title_alpha)

        # Neural network diagram
        if progress > 0.2:
            nn_progress = min(1.0, (progress - 0.2) / 0.2)

            # Layer 1
            layer0_x = 20.0
            if nn_progress > 0.00:
                layer_alpha = min(1.0, (nn_progress - 0.00) / 0.25)

                # Node 1
                node0_0 = Circle((layer0_x, 56.666666666666664), 1.5,
                                                    facecolor=self.colors['primary'],
                                                    edgecolor='white', linewidth=1.5,
                                                    alpha=layer_alpha * 0.9, zorder=10)
                ax.add_patch(node0_0)

                # Node 2
                node0_1 = Circle((layer0_x, 50.0), 1.5,
                                                    facecolor=self.colors['primary'],
                                                    edgecolor='white', linewidth=1.5,
                                                    alpha=layer_alpha * 0.9, zorder=10)
                ax.add_patch(node0_1)

                # Node 3
                node0_2 = Circle((layer0_x, 43.33333333333333), 1.5,
                                                    facecolor=self.colors['primary'],
                                                    edgecolor='white', linewidth=1.5,
                                                    alpha=layer_alpha * 0.9, zorder=10)
                ax.add_patch(node0_2)

                ax.text(layer0_x, 27.0, 'Input',
                       fontsize=12, ha='center', va='top',
                       color=self.colors['text'], alpha=layer_alpha * 0.8)

            # Layer 2
            layer1_x = 40.0
            if nn_progress > 0.25:
                layer_alpha = min(1.0, (nn_progress - 0.25) / 0.25)

                # Connections from layer 1
                for prev_i in range(3):
                    prev_y = 56.666666666666664 - prev_i * 6.666666666666667
                    for curr_i in range(5):
                        curr_y = 63.333333333333336 - curr_i * 6.666666666666667
                        ax.plot([20.0, layer1_x],
                               [prev_y, curr_y],
                               color=self.colors['dim'],
                               linewidth=0.5, alpha=layer_alpha * 0.3, zorder=1)

                # Node 1
                node1_0 = Circle((layer1_x, 63.333333333333336), 1.5,
                                                    facecolor=self.colors['primary'],
                                                    edgecolor='white', linewidth=1.5,
                                                    alpha=layer_alpha * 0.9, zorder=10)
                ax.add_patch(node1_0)

                # Node 2
                node1_1 = Circle((layer1_x, 56.66666666666667), 1.5,
                                                    facecolor=self.colors['primary'],
                                                    edgecolor='white', linewidth=1.5,
                                                    alpha=layer_alpha * 0.9, zorder=10)
                ax.add_patch(node1_1)

                # Node 3
                node1_2 = Circle((layer1_x, 50.0), 1.5,
                                                    facecolor=self.colors['primary'],
                                                    edgecolor='white', linewidth=1.5,
                                                    alpha=layer_alpha * 0.9, zorder=10)
                ax.add_patch(node1_2)

                # Node 4
                node1_3 = Circle((layer1_x, 43.333333333333336), 1.5,
                                                    facecolor=self.colors['primary'],
                                                    edgecolor='white', linewidth=1.5,
                                                    alpha=layer_alpha * 0.9, zorder=10)
                ax.add_patch(node1_3)

                # Node 5
                node1_4 = Circle((layer1_x, 36.66666666666667), 1.5,
                                                    facecolor=self.colors['primary'],
                                                    edgecolor='white', linewidth=1.5,
                                                    alpha=layer_alpha * 0.9, zorder=10)
                ax.add_patch(node1_4)

                ax.text(layer1_x, 27.0, 'Hidden 1',
                       fontsize=12, ha='center', va='top',
                       color=self.colors['text'], alpha=layer_alpha * 0.8)

            # Layer 3
            layer2_x = 60.0
            if nn_progress > 0.50:
                layer_alpha = min(1.0, (nn_progress - 0.50) / 0.25)

                # Connections from layer 2
                for prev_i in range(5):
                    prev_y = 63.333333333333336 - prev_i * 6.666666666666667
                    for curr_i in range(5):
                        curr_y = 63.333333333333336 - curr_i * 6.666666666666667
                        ax.plot([40.0, layer2_x],
                               [prev_y, curr_y],
                               color=self.colors['dim'],
                               linewidth=0.5, alpha=layer_alpha * 0.3, zorder=1)

                # Node 1
                node2_0 = Circle((layer2_x, 63.333333333333336), 1.5,
                                                    facecolor=self.colors['primary'],
                                                    edgecolor='white', linewidth=1.5,
                                                    alpha=layer_alpha * 0.9, zorder=10)
                ax.add_patch(node2_0)

                # Node 2
                node2_1 = Circle((layer2_x, 56.66666666666667), 1.5,
                                                    facecolor=self.colors['primary'],
                                                    edgecolor='white', linewidth=1.5,
                                                    alpha=layer_alpha * 0.9, zorder=10)
                ax.add_patch(node2_1)

                # Node 3
                node2_2 = Circle((layer2_x, 50.0), 1.5,
                                                    facecolor=self.colors['primary'],
                                                    edgecolor='white', linewidth=1.5,
                                                    alpha=layer_alpha * 0.9, zorder=10)
                ax.add_patch(node2_2)

                # Node 4
                node2_3 = Circle((layer2_x, 43.333333333333336), 1.5,
                                                    facecolor=self.colors['primary'],
                                                    edgecolor='white', linewidth=1.5,
                                                    alpha=layer_alpha * 0.9, zorder=10)
                ax.add_patch(node2_3)

                # Node 5
                node2_4 = Circle((layer2_x, 36.66666666666667), 1.5,
                                                    facecolor=self.colors['primary'],
                                                    edgecolor='white', linewidth=1.5,
                                                    alpha=layer_alpha * 0.9, zorder=10)
                ax.add_patch(node2_4)

                ax.text(layer2_x, 27.0, 'Hidden 2',
                       fontsize=12, ha='center', va='top',
                       color=self.colors['text'], alpha=layer_alpha * 0.8)

            # Layer 4
            layer3_x = 80.0
            if nn_progress > 0.75:
                layer_alpha = min(1.0, (nn_progress - 0.75) / 0.25)

                # Connections from layer 3
                for prev_i in range(5):
                    prev_y = 63.333333333333336 - prev_i * 6.666666666666667
                    for curr_i in range(2):
                        curr_y = 53.333333333333336 - curr_i * 6.666666666666667
                        ax.plot([60.0, layer3_x],
                               [prev_y, curr_y],
                               color=self.colors['dim'],
                               linewidth=0.5, alpha=layer_alpha * 0.3, zorder=1)

                # Node 1
                node3_0 = Circle((layer3_x, 53.333333333333336), 1.5,
                                                    facecolor=self.colors['primary'],
                                                    edgecolor='white', linewidth=1.5,
                                                    alpha=layer_alpha * 0.9, zorder=10)
                ax.add_patch(node3_0)

                # Node 2
                node3_1 = Circle((layer3_x, 46.66666666666667), 1.5,
                                                    facecolor=self.colors['primary'],
                                                    edgecolor='white', linewidth=1.5,
                                                    alpha=layer_alpha * 0.9, zorder=10)
                ax.add_patch(node3_1)

                ax.text(layer3_x, 27.0, 'Output',
                       fontsize=12, ha='center', va='top',
                       color=self.colors['text'], alpha=layer_alpha * 0.8)

        self.add_status_indicator(progress < 1.0)

    def draw_arc_arrow(self, progress: float):
        """Step 5: Arc Arrow"""
        self.fig.clear()
        ax = self.fig.add_subplot(111)
        ax.axis('off')
        ax.set_xlim(0, 100)
        ax.set_ylim(0, 100)

        # Title
        title_alpha = min(1.0, progress / 0.2)
        ax.text(50, 95, 'Arc Arrow Animation',
                fontsize=45, fontweight='bold', ha='center', va='top',
                color=self.colors['primary'], alpha=title_alpha)

        if progress > 0.0:
            box_alpha = min(1.0, (progress - 0.0) / 0.2)

            box = FancyBboxPatch(
                (15.0, 42.5), 20, 15,
                boxstyle="round,pad=1",
                facecolor=self.colors['bg_light'],
                edgecolor=self.colors['primary'],
                linewidth=3,
                alpha=0.95 * box_alpha
            )
            ax.add_patch(box)

            ax.text(25, 53.75, 'Source',
                    fontsize=24, fontweight='bold', ha='center', va='center',
                    color=self.colors['primary'], alpha=box_alpha)

        if progress > 0.0:
            box_alpha = min(1.0, (progress - 0.0) / 0.2)

            box = FancyBboxPatch(
                (65.0, 42.5), 20, 15,
                boxstyle="round,pad=1",
                facecolor=self.colors['bg_light'],
                edgecolor=self.colors['primary'],
                linewidth=3,
                alpha=0.95 * box_alpha
            )
            ax.add_patch(box)

            ax.text(75, 53.75, 'Target',
                    fontsize=24, fontweight='bold', ha='center', va='center',
                    color=self.colors['primary'], alpha=box_alpha)

        # Arc arrow
        if progress > 0.4:
            arc_progress = min(1.0, (progress - 0.4) / 0.19999999999999996)

            # Generate arc points using quadratic bezier
            t = np.linspace(0, arc_progress, 50)
            mid_x = (35 + 65) / 2
            mid_y = (50 + 50) / 2 + 20

            # Quadratic bezier curve
            arc_x = (1-t)**2 * 35 + 2*(1-t)*t * mid_x + t**2 * 65
            arc_y = (1-t)**2 * 50 + 2*(1-t)*t * mid_y + t**2 * 50

            ax.plot(arc_x, arc_y, color=self.colors['accent'],
                   linewidth=3, alpha=arc_progress, zorder=50)

            # Arrowhead at the end
            if arc_progress > 0.9:
                arrow_alpha = (arc_progress - 0.9) / 0.1
                # Calculate direction at endpoint
                dx = arc_x[-1] - arc_x[-2] if len(arc_x) > 1 else 1
                dy = arc_y[-1] - arc_y[-2] if len(arc_y) > 1 else 0
                ax.annotate('', xy=(65, 50),
                           xytext=(arc_x[-1] - dx*0.5, arc_y[-1] - dy*0.5),
                           arrowprops=dict(arrowstyle='->', color=self.colors['accent'],
                                          lw=3), alpha=arrow_alpha)

        self.add_status_indicator(progress < 1.0)

    def draw_3d_scatter(self, progress: float):
        """Step 6: 3D Scatter"""
        self.fig.clear()
        ax = self.fig.add_subplot(111)
        ax.axis('off')
        ax.set_xlim(0, 100)
        ax.set_ylim(0, 100)

        # Title
        title_alpha = min(1.0, progress / 0.2)
        ax.text(50, 95, '3D Vector Space',
                fontsize=45, fontweight='bold', ha='center', va='top',
                color=self.colors['primary'], alpha=title_alpha)

        # 3D Scatter plot (requires special subplot handling)
        # Note: This should be the main element when using 3D
        if progress > 0.2:
            scatter_progress = min(1.0, (progress - 0.2) / 0.2)

            # Remove current axes and create 3D subplot
            self.fig.clear()
            ax3d = self.fig.add_subplot(111, projection='3d')
            ax3d.set_xlim(-5, 5)
            ax3d.set_ylim(-5, 5)
            ax3d.set_zlim(-5, 5)

            ax3d.view_init(elev=20, azim=45 + scatter_progress * 90)

            # Style 3D axes
            ax3d.set_facecolor(self.colors['bg'])
            ax3d.xaxis.pane.fill = True
            ax3d.yaxis.pane.fill = True
            ax3d.zaxis.pane.fill = True
            ax3d.xaxis.pane.set_facecolor((0.05, 0.05, 0.05, 0.3))
            ax3d.yaxis.pane.set_facecolor((0.05, 0.05, 0.05, 0.3))
            ax3d.zaxis.pane.set_facecolor((0.05, 0.05, 0.05, 0.3))
            ax3d.grid(True, alpha=0.2)
            ax3d.tick_params(colors=self.colors['text'], labelsize=10)

            # Point 1: Dog
            if scatter_progress > 0.00:
                pt_alpha = min(1.0, (scatter_progress - 0.00) / 0.25)

                # Vector line from origin
                ax3d.plot([0, 2], [0, 3], [0, 1.5],
                         color=self.colors['secondary'], linewidth=1.5,
                         alpha=pt_alpha * 0.6, linestyle='--')

                # Point
                ax3d.scatter([2], [3], [1.5], s=400,
                            c=[self.colors['secondary']], edgecolors='white',
                            linewidths=2, alpha=pt_alpha * 0.9, depthshade=True)

                # Label
                ax3d.text(2, 3, 1.5 + 0.5, 'Dog',
                         fontsize=14, ha='center', color='white',
                         alpha=pt_alpha,
                         bbox=dict(boxstyle='round,pad=0.3',
                                 facecolor=self.colors['secondary'],
                                 edgecolor='white', alpha=0.9))

            # Point 2: Cat
            if scatter_progress > 0.25:
                pt_alpha = min(1.0, (scatter_progress - 0.25) / 0.25)

                # Vector line from origin
                ax3d.plot([0, 2.5], [0, 2.8], [0, 1.8],
                         color=self.colors['secondary'], linewidth=1.5,
                         alpha=pt_alpha * 0.6, linestyle='--')

                # Point
                ax3d.scatter([2.5], [2.8], [1.8], s=400,
                            c=[self.colors['secondary']], edgecolors='white',
                            linewidths=2, alpha=pt_alpha * 0.9, depthshade=True)

                # Label
                ax3d.text(2.5, 2.8, 1.8 + 0.5, 'Cat',
                         fontsize=14, ha='center', color='white',
                         alpha=pt_alpha,
                         bbox=dict(boxstyle='round,pad=0.3',
                                 facecolor=self.colors['secondary'],
                                 edgecolor='white', alpha=0.9))

            # Point 3: Car
            if scatter_progress > 0.50:
                pt_alpha = min(1.0, (scatter_progress - 0.50) / 0.25)

                # Vector line from origin
                ax3d.plot([0, -2], [0, 1], [0, 3],
                         color=self.colors['accent'], linewidth=1.5,
                         alpha=pt_alpha * 0.6, linestyle='--')

                # Point
                ax3d.scatter([-2], [1], [3], s=400,
                            c=[self.colors['accent']], edgecolors='white',
                            linewidths=2, alpha=pt_alpha * 0.9, depthshade=True)

                # Label
                ax3d.text(-2, 1, 3 + 0.5, 'Car',
                         fontsize=14, ha='center', color='white',
                         alpha=pt_alpha,
                         bbox=dict(boxstyle='round,pad=0.3',
                                 facecolor=self.colors['accent'],
                                 edgecolor='white', alpha=0.9))

            # Point 4: Bike
            if scatter_progress > 0.75:
                pt_alpha = min(1.0, (scatter_progress - 0.75) / 0.25)

                # Vector line from origin
                ax3d.plot([0, -1.5], [0, 0.5], [0, 2.5],
                         color=self.colors['accent'], linewidth=1.5,
                         alpha=pt_alpha * 0.6, linestyle='--')

                # Point
                ax3d.scatter([-1.5], [0.5], [2.5], s=400,
                            c=[self.colors['accent']], edgecolors='white',
                            linewidths=2, alpha=pt_alpha * 0.9, depthshade=True)

                # Label
                ax3d.text(-1.5, 0.5, 2.5 + 0.5, 'Bike',
                         fontsize=14, ha='center', color='white',
                         alpha=pt_alpha,
                         bbox=dict(boxstyle='round,pad=0.3',
                                 facecolor=self.colors['accent'],
                                 edgecolor='white', alpha=0.9))

        self.add_status_indicator(progress < 1.0)

    def draw_step_7(self, progress: float):
        """Step 7: Step 7"""
        self.fig.clear()
        ax = self.fig.add_subplot(111)
        ax.axis('off')
        ax.set_xlim(0, 100)
        ax.set_ylim(0, 100)

        # Title
        title_alpha = min(1.0, progress / 0.2)
        ax.text(50, 95, 'New Step 7',
                fontsize=45, fontweight='bold', ha='center', va='top',
                color=self.colors['primary'], alpha=title_alpha)

        self.add_status_indicator(progress < 1.0)

    def draw_step_8(self, progress: float):
        """Step 8: Step 8"""
        self.fig.clear()
        ax = self.fig.add_subplot(111)
        ax.axis('off')
        ax.set_xlim(0, 100)
        ax.set_ylim(0, 100)

        # Title
        title_alpha = min(1.0, progress / 0.2)
        ax.text(50, 95, 'New Step 8',
                fontsize=45, fontweight='bold', ha='center', va='top',
                color=self.colors['primary'], alpha=title_alpha)

        if progress > 0.2:
            t = min(1.0, (progress - 0.2) / 0.2)
            text_alpha = t * t * (3 - 2 * t)
            effective_fontsize = 24
            ax.text(31.315526102192596, 43.18032331015792, 'New Text',
                    fontsize=effective_fontsize, fontweight='normal',
                    ha='center', va='center',
                    color=self.colors['text'], alpha=text_alpha)

        self.add_status_indicator(progress < 1.0)


def run():
    """Run the presentation"""
    pres = TestAdvancedPresentation()
    pres.show()


if __name__ == "__main__":
    run()
