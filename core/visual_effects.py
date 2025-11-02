"""
Visual Effects and Performance Utilities
Shared animation helpers and 3D optimization tools
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyBboxPatch, Wedge
from typing import Tuple, List


class AnimationHelpers:
    """Helper functions for smooth animations"""

    @staticmethod
    def lerp(start: float, end: float, t: float) -> float:
        """Linear interpolation"""
        return start + (end - start) * t

    @staticmethod
    def ease_in_out(t: float) -> float:
        """Smooth ease in/out curve (cubic)"""
        if t < 0.5:
            return 4 * t * t * t
        else:
            return 1 - pow(-2 * t + 2, 3) / 2

    @staticmethod
    def ease_out_bounce(t: float) -> float:
        """Bouncy ease out"""
        n1 = 7.5625
        d1 = 2.75

        if t < 1 / d1:
            return n1 * t * t
        elif t < 2 / d1:
            t -= 1.5 / d1
            return n1 * t * t + 0.75
        elif t < 2.5 / d1:
            t -= 2.25 / d1
            return n1 * t * t + 0.9375
        else:
            t -= 2.625 / d1
            return n1 * t * t + 0.984375

    @staticmethod
    def pulse(t: float, frequency: float = 1.0) -> float:
        """Pulsing effect (0.9 to 1.1 range)"""
        return 1.0 + 0.1 * np.sin(t * 2 * np.pi * frequency)

    @staticmethod
    def breathing(t: float, frequency: float = 0.5) -> float:
        """Gentle breathing effect (0.95 to 1.05)"""
        return 1.0 + 0.05 * np.sin(t * 2 * np.pi * frequency)


class ParticleSystem:
    """Optimized particle system for data flow animations"""

    def __init__(self, num_particles: int, start_pos: Tuple[float, float],
                 end_pos: Tuple[float, float], color: str = '#06B6D4'):
        self.num_particles = num_particles
        self.start_pos = np.array(start_pos)
        self.end_pos = np.array(end_pos)
        self.color = color

        # Pre-calculate particle paths with randomized offsets
        self.offsets = np.random.randn(num_particles, 2) * 0.5
        self.phase_offsets = np.random.rand(num_particles) * 0.3

    def draw(self, ax, progress: float, alpha: float = 1.0):
        """Draw particles with optimized batch rendering"""
        if progress < 0.01:
            return

        # Batch calculate all particle positions
        positions = []
        alphas = []

        for i in range(self.num_particles):
            # Stagger particle start times
            particle_progress = max(0, min(1, (progress - self.phase_offsets[i]) / (1 - 0.3)))

            if particle_progress > 0:
                # Interpolate position with offset
                pos = (
                    AnimationHelpers.lerp(self.start_pos[0], self.end_pos[0], particle_progress) + self.offsets[i, 0] * (1 - particle_progress),
                    AnimationHelpers.lerp(self.start_pos[1], self.end_pos[1], particle_progress) + self.offsets[i, 1] * (1 - particle_progress)
                )
                positions.append(pos)

                # Fade in/out
                particle_alpha = min(particle_progress * 3, (1 - particle_progress) * 3, 1.0) * alpha
                alphas.append(particle_alpha)

        # Batch render all particles
        if positions:
            positions = np.array(positions)
            ax.scatter(positions[:, 0], positions[:, 1],
                      c=self.color, s=30, alpha=alphas,
                      edgecolors='none', zorder=100)


class SimilarityMeter:
    """Gauge/meter for showing similarity scores"""

    def __init__(self, x: float, y: float, radius: float = 8,
                 colors: dict = None):
        self.x = x
        self.y = y
        self.radius = radius
        self.colors = colors or {
            'low': '#EF4444',     # Red
            'medium': '#F59E0B',  # Orange
            'high': '#10B981'     # Green
        }

    def draw(self, ax, score: float, progress: float):
        """Draw similarity score meter (0-100%)"""
        if progress < 0.01:
            return

        # Animate score from 0 to target
        current_score = score * min(1.0, progress * 2)

        # Background arc (gray)
        bg_wedge = Wedge((self.x, self.y), self.radius, 0, 180,
                        facecolor='#1a1a1a', edgecolor='#404040',
                        linewidth=2, alpha=0.9 * progress)
        ax.add_patch(bg_wedge)

        # Score arc (colored based on value)
        if current_score < 50:
            color = self.colors['low']
        elif current_score < 75:
            color = self.colors['medium']
        else:
            color = self.colors['high']

        angle = 180 * (current_score / 100)
        score_wedge = Wedge((self.x, self.y), self.radius * 0.9, 0, angle,
                           facecolor=color, edgecolor='none',
                           alpha=0.8 * progress)
        ax.add_patch(score_wedge)

        # Center circle (cutout)
        center = Circle((self.x, self.y), self.radius * 0.6,
                       facecolor='#0a0a0a', edgecolor='none',
                       zorder=10)
        ax.add_patch(center)

        # Score text
        ax.text(self.x, self.y, f'{int(current_score)}%',
               fontsize=32, fontweight='bold',
               ha='center', va='center',
               color=color, alpha=progress)

        # Label
        ax.text(self.x, self.y - self.radius - 2, 'Similarity',
               fontsize=20, ha='center', va='top',
               color='#F0F0F0', alpha=progress * 0.7)


class Performance3D:
    """3D Performance optimization utilities"""

    @staticmethod
    def create_optimized_scatter(ax, positions: np.ndarray, color: str,
                                size: float = 100, alpha: float = 1.0,
                                add_shadow: bool = True):
        """Create optimized 3D scatter with optional shadows"""
        # Main points
        scatter = ax.scatter(positions[:, 0], positions[:, 1], positions[:, 2],
                            c=color, s=size, alpha=alpha,
                            edgecolors='white', linewidths=1.5,
                            depthshade=True)

        # Optional ground shadows for depth perception
        if add_shadow and len(positions) < 20:  # Only for small datasets
            shadow_positions = positions.copy()
            shadow_positions[:, 2] = 0  # Project to ground
            ax.scatter(shadow_positions[:, 0], shadow_positions[:, 1], shadow_positions[:, 2],
                      c='black', s=size * 0.5, alpha=0.2 * alpha,
                      edgecolors='none', depthshade=False)

        return scatter

    @staticmethod
    def create_depth_lines(ax, start_points: np.ndarray, end_points: np.ndarray,
                          color: str = '#6B7280', alpha: float = 0.3,
                          linestyle: str = ':'):
        """Create depth indicator lines (optimized batch rendering)"""
        # Batch render vertical lines for depth
        for start, end in zip(start_points, end_points):
            ax.plot([start[0], end[0]], [start[1], end[1]], [start[2], end[2]],
                   color=color, linestyle=linestyle, linewidth=1,
                   alpha=alpha, zorder=1)

    @staticmethod
    def optimize_3d_view(ax, reduce_ticks: bool = True):
        """Apply 3D performance optimizations"""
        # Reduce tick density
        if reduce_ticks:
            ax.locator_params(nbins=5)

        # Disable expensive features
        ax.xaxis.pane.fill = False
        ax.yaxis.pane.fill = False
        ax.zaxis.pane.fill = False

        # Simplify grid
        ax.grid(True, alpha=0.2, linestyle='--')

        return ax


class WeightDeltaVisualizer:
    """Visualize weight changes with arrows and colors"""

    def __init__(self, colors: dict = None):
        self.colors = colors or {
            'increase': '#10B981',  # Green
            'decrease': '#EF4444',  # Red
            'neutral': '#6B7280'    # Gray
        }

    def draw_weight_comparison(self, ax, before_weights: np.ndarray,
                              after_weights: np.ndarray,
                              x_before: float, x_after: float,
                              y_start: float, height: float,
                              progress: float):
        """Draw before/after weight bars with delta arrows"""
        num_weights = len(before_weights)
        bar_height = height / num_weights

        for i in range(num_weights):
            y = y_start + i * bar_height

            # Calculate delta
            delta = after_weights[i] - before_weights[i]
            delta_pct = (delta / abs(before_weights[i]) * 100) if before_weights[i] != 0 else 0

            # Color based on change
            if abs(delta_pct) < 5:
                color = self.colors['neutral']
            elif delta > 0:
                color = self.colors['increase']
            else:
                color = self.colors['decrease']

            # Before bar (animate)
            if progress > 0.3:
                before_alpha = min(1.0, (progress - 0.3) / 0.2)
                before_width = abs(before_weights[i]) * 3
                ax.barh(y, before_width, bar_height * 0.8,
                       left=x_before, color='#60A5FA',
                       alpha=0.6 * before_alpha, edgecolor='white', linewidth=0.5)

            # After bar (animate)
            if progress > 0.5:
                after_alpha = min(1.0, (progress - 0.5) / 0.2)
                after_width = abs(after_weights[i]) * 3
                ax.barh(y, after_width, bar_height * 0.8,
                       left=x_after, color=color,
                       alpha=0.8 * after_alpha, edgecolor='white', linewidth=0.5)

            # Delta arrow (animate)
            if progress > 0.7 and abs(delta_pct) > 5:
                arrow_alpha = min(1.0, (progress - 0.7) / 0.3)
                mid_x = (x_before + abs(before_weights[i]) * 3 + x_after) / 2

                # Arrow
                arrow_dir = 0.5 if delta > 0 else -0.5
                ax.arrow(mid_x, y, arrow_dir, 0,
                        head_width=bar_height * 0.4, head_length=0.3,
                        fc=color, ec=color, alpha=arrow_alpha,
                        linewidth=2, zorder=10)

                # Delta label
                ax.text(mid_x, y + bar_height * 0.5,
                       f'{delta_pct:+.0f}%',
                       fontsize=14, ha='center', va='bottom',
                       color=color, fontweight='bold',
                       alpha=arrow_alpha)


class ProgressIndicator:
    """Visual progress indicator for iterative processes"""

    def __init__(self, x: float, y: float, width: float = 30,
                 height: float = 3, color: str = '#10B981'):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color

    def draw(self, ax, progress: float, current: int, total: int,
            label: str = "Progress"):
        """Draw progress bar with epoch counter"""
        # Background
        bg_box = FancyBboxPatch(
            (self.x - self.width/2, self.y - self.height/2),
            self.width, self.height,
            boxstyle="round,pad=0.2",
            facecolor='#1a1a1a',
            edgecolor='#404040',
            linewidth=2,
            alpha=0.9
        )
        ax.add_patch(bg_box)

        # Progress fill
        fill_width = self.width * progress
        fill_box = FancyBboxPatch(
            (self.x - self.width/2, self.y - self.height/2),
            fill_width, self.height,
            boxstyle="round,pad=0.2",
            facecolor=self.color,
            edgecolor='none',
            alpha=0.8
        )
        ax.add_patch(fill_box)

        # Text
        ax.text(self.x, self.y, f'{current}/{total}',
               fontsize=18, fontweight='bold',
               ha='center', va='center',
               color='white', zorder=20)

        # Label
        ax.text(self.x, self.y + self.height + 1.5, label,
               fontsize=16, ha='center', va='bottom',
               color='#F0F0F0', alpha=0.8)
