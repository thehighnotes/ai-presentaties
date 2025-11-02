"""
Animation utilities and helpers
Common animation patterns and easing functions
"""

import numpy as np
from typing import Callable


class AnimationHelper:
    """
    Utility functions for smooth animations
    Easing functions, progress calculation, and animation patterns
    """

    @staticmethod
    def ease_in_out(t: float) -> float:
        """
        Smooth ease-in-out curve (smoothstep)

        Args:
            t: Progress value between 0 and 1

        Returns:
            Eased progress value between 0 and 1
        """
        return t * t * (3 - 2 * t)

    @staticmethod
    def ease_in(t: float) -> float:
        """
        Ease-in curve (accelerate)

        Args:
            t: Progress value between 0 and 1

        Returns:
            Eased progress value
        """
        return t * t

    @staticmethod
    def ease_out(t: float) -> float:
        """
        Ease-out curve (decelerate)

        Args:
            t: Progress value between 0 and 1

        Returns:
            Eased progress value
        """
        return 1 - (1 - t) ** 2

    @staticmethod
    def ease_out_cubic(t: float) -> float:
        """
        Cubic ease-out (stronger deceleration)

        Args:
            t: Progress value between 0 and 1

        Returns:
            Eased progress value
        """
        return 1 - (1 - t) ** 3

    @staticmethod
    def ease_in_cubic(t: float) -> float:
        """
        Cubic ease-in (stronger acceleration)

        Args:
            t: Progress value between 0 and 1

        Returns:
            Eased progress value
        """
        return t ** 3

    @staticmethod
    def elastic_ease_out(t: float) -> float:
        """
        Elastic ease-out (bouncy effect)

        Args:
            t: Progress value between 0 and 1

        Returns:
            Eased progress value
        """
        if t == 0 or t == 1:
            return t

        p = 0.3
        s = p / 4
        return np.power(2, -10 * t) * np.sin((t - s) * (2 * np.pi) / p) + 1

    @staticmethod
    def pulse(t: float, frequency: float = 10) -> float:
        """
        Create a pulsing effect

        Args:
            t: Progress value between 0 and 1
            frequency: Pulse frequency

        Returns:
            Pulse value between -1 and 1
        """
        return np.sin(t * frequency * 2 * np.pi)

    @staticmethod
    def fade_in(progress: float, delay: float = 0, duration: float = 1) -> float:
        """
        Calculate fade-in alpha value

        Args:
            progress: Current animation progress (0 to 1)
            delay: When to start fading (0 to 1)
            duration: How long the fade takes (relative to total)

        Returns:
            Alpha value between 0 and 1
        """
        if progress < delay:
            return 0
        if progress > delay + duration:
            return 1

        t = (progress - delay) / duration
        return AnimationHelper.ease_in_out(t)

    @staticmethod
    def stagger_delay(index: int, total: int, start: float = 0, end: float = 0.5) -> float:
        """
        Calculate staggered animation delay for multiple elements

        Args:
            index: Current element index
            total: Total number of elements
            start: When to start the stagger (0 to 1)
            end: When to finish the stagger (0 to 1)

        Returns:
            Delay value between start and end
        """
        if total <= 1:
            return start

        return start + (end - start) * (index / (total - 1))

    @staticmethod
    def get_phase_progress(progress: float, phase_start: float, phase_end: float) -> float:
        """
        Get normalized progress within a specific phase

        Args:
            progress: Overall progress (0 to 1)
            phase_start: Phase start point (0 to 1)
            phase_end: Phase end point (0 to 1)

        Returns:
            Progress within phase (0 to 1), or 0 if before phase, or 1 if after
        """
        if progress < phase_start:
            return 0
        if progress > phase_end:
            return 1

        return (progress - phase_start) / (phase_end - phase_start)

    @staticmethod
    def lerp(start: float, end: float, t: float) -> float:
        """
        Linear interpolation between two values

        Args:
            start: Start value
            end: End value
            t: Progress (0 to 1)

        Returns:
            Interpolated value
        """
        return start + (end - start) * t

    @staticmethod
    def typewriter_progress(text: str, progress: float) -> tuple[str, bool]:
        """
        Create typewriter effect for text

        Args:
            text: Full text to display
            progress: Animation progress (0 to 1)

        Returns:
            Tuple of (visible_text, show_cursor)
        """
        num_chars = int(len(text) * progress)
        visible_text = text[:num_chars]

        # Blinking cursor when not complete
        show_cursor = num_chars < len(text) and int(progress * 10) % 2 == 0

        return visible_text, show_cursor

    @staticmethod
    def draw_progress_bar(ax, progress: float, x: float, y: float,
                         width: float, height: float, color: str = '#3B82F6'):
        """
        Draw a progress bar on an axis

        Args:
            ax: Matplotlib axis
            progress: Progress value (0 to 1)
            x: X position
            y: Y position
            width: Bar width
            height: Bar height
            color: Fill color
        """
        from matplotlib.patches import Rectangle

        # Background
        bg = Rectangle((x, y), width, height,
                      facecolor='#2a2a2a',
                      edgecolor='#6B7280',
                      linewidth=1)
        ax.add_patch(bg)

        # Progress fill
        if progress > 0:
            fill = Rectangle((x, y), width * progress, height,
                           facecolor=color,
                           edgecolor='none')
            ax.add_patch(fill)

    @staticmethod
    def calculate_arc_points(center_x: float, center_y: float,
                            radius: float, angle_start: float,
                            angle_end: float, num_points: int = 50) -> tuple:
        """
        Calculate points along an arc

        Args:
            center_x: Arc center X
            center_y: Arc center Y
            radius: Arc radius
            angle_start: Start angle in degrees
            angle_end: End angle in degrees
            num_points: Number of points to generate

        Returns:
            Tuple of (x_points, y_points)
        """
        angles = np.linspace(np.radians(angle_start), np.radians(angle_end), num_points)
        x_points = center_x + radius * np.cos(angles)
        y_points = center_y + radius * np.sin(angles)
        return x_points, y_points
