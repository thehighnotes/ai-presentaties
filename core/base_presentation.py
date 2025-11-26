"""
Base presentation class
All specific presentations inherit from this
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.animation import FuncAnimation
from typing import List, Optional
from .styling import PresentationStyle
from .controls import ControlHandler
from .animations import AnimationHelper


class BasePresentation:
    """
    Base class for all AI presentations
    Provides common functionality for navigation, animation, and UI
    """

    def __init__(self, title: str, step_names: List[str]):
        """
        Initialize base presentation

        Args:
            title: Presentation title
            step_names: List of step names (including 'Landing' as first step)
        """
        # Apply dark mode styling globally
        PresentationStyle.apply_dark_mode()

        # Create figure
        self.fig = PresentationStyle.create_figure()
        self.title = title
        self.step_names = step_names

        # Animation state
        self.current_step = -1  # Start at landing page
        self.is_animating = False
        self.animation = None
        self.animation_frame = 0

        # Styling
        self.style = PresentationStyle
        self.colors = PresentationStyle.COLORS
        self.anim_helper = AnimationHelper

        # Setup resize handler to maintain aspect ratio
        self.fig.canvas.mpl_connect('resize_event', self._on_resize)

        # Setup controls
        self.control_handler = ControlHandler(self)
        self.control_handler.setup()

    def _on_resize(self, event):
        """Handle window resize to maintain proper aspect ratio and alignment"""
        if event is None or event.width is None or event.height is None:
            return

        # Target aspect ratio (16:9)
        target_aspect = 16 / 9

        # Calculate current aspect ratio
        current_aspect = event.width / event.height if event.height > 0 else target_aspect

        # If aspect ratio changed significantly, redraw to maintain layout
        if abs(current_aspect - target_aspect) > 0.01:
            # Force matplotlib to maintain the aspect ratio
            for ax in self.fig.get_axes():
                ax.set_aspect('equal', adjustable='box')

            # Redraw current content
            self.fig.canvas.draw_idle()

    def show_landing_page(self):
        """
        Display landing page - must be implemented by subclass

        Raises:
            NotImplementedError: If subclass doesn't implement
        """
        raise NotImplementedError("Subclass must implement show_landing_page()")

    def start_next_step(self):
        """Move to and animate next step"""
        if self.current_step < len(self.step_names) - 1:
            self.current_step += 1
            print(f"\n→ Stap {self.current_step + 1}/{len(self.step_names)}: "
                  f"{self.step_names[self.current_step]}")
            self.start_step_animation()
        else:
            print("[OK] Laatste stap bereikt!")

    def previous_step(self):
        """Move back to previous step"""
        if not self.is_animating:
            if self.current_step > -1:
                self.current_step -= 1
                print(f"← Stap {self.current_step + 1}/{len(self.step_names)}: "
                      f"{self.step_names[self.current_step]}")

                if self.current_step == -1:
                    self.show_landing_page()
                else:
                    self.draw_current_step_static()
                plt.draw()
            else:
                print("[OK] Al bij eerste stap!")

    def reset(self):
        """Reset presentation to beginning"""
        self.current_step = -1
        self.is_animating = False
        if self.animation is not None:
            try:
                self.animation.event_source.stop()
            except:
                pass
            self.animation = None
        self.show_landing_page()
        plt.draw()
        print("\n🔄 Presentatie gereset naar begin")

    def next_step(self):
        """Alias for start_next_step (for control compatibility)"""
        self.start_next_step()

    def start_step_animation(self):
        """
        Start animation for current step
        Subclasses can override to customize animation timing
        """
        self.is_animating = True
        self.animation_frame = 0

        # Get frame count for this step
        total_frames = self.get_frames_for_step(self.current_step)

        self.animation = FuncAnimation(
            self.fig,
            self.animate_step,
            frames=total_frames,
            interval=PresentationStyle.ANIMATION_INTERVAL,
            blit=False,
            repeat=False
        )

        plt.draw()

    def get_frames_for_step(self, step: int) -> int:
        """
        Get number of animation frames for a step
        Override in subclass to customize per step

        Args:
            step: Step index

        Returns:
            Number of frames (default 60)
        """
        return PresentationStyle.ANIMATION_FRAMES_SHORT

    def animate_step(self, frame: int):
        """
        Animate current step - must be implemented by subclass

        Args:
            frame: Current frame number

        Raises:
            NotImplementedError: If subclass doesn't implement
        """
        raise NotImplementedError("Subclass must implement animate_step()")

    def draw_current_step_static(self):
        """
        Draw current step as static image (paused state)
        Must be implemented by subclass

        Raises:
            NotImplementedError: If subclass doesn't implement
        """
        raise NotImplementedError("Subclass must implement draw_current_step_static()")

    def add_status_indicator(self, is_animating: bool = True):
        """
        Add standard status indicator at top-left of screen

        Args:
            is_animating: Whether animation is currently running
        """
        if is_animating:
            status_text = "ANIMEREN..."
            status_color = self.colors['accent']
        else:
            status_text = "GEPAUZEERD - SPATIE = volgende"
            status_color = self.colors['secondary']

        # Top-left status indicator (smaller)
        self.fig.text(0.02, 0.98, status_text,
                     fontsize=12,  # Smaller font
                     ha='left', va='top',
                     bbox=dict(boxstyle='round,pad=0.3',
                              facecolor=self.colors['bg_light'],
                              edgecolor=status_color,
                              linewidth=1.5,
                              alpha=0.85),
                     color=status_color,
                     fontweight='bold')

        # Progress bar at bottom
        self._add_progress_bar()

        # Step counter at bottom center
        step_num = max(0, self.current_step)
        total_steps = len(self.step_names) - 1
        self.fig.text(0.5, 0.015, f'Stap {step_num + 1} / {total_steps + 1}',
                     fontsize=20, ha='center', va='center',
                     color=self.colors['text'],
                     alpha=0.7)

    def _add_progress_bar(self):
        """Add progress bar visualization"""
        # Current step: -1 = landing (not started), 0 = first step, etc.
        # For progress: landing = 0%, first step = 1/total, last step = 100%
        step_num = max(0, self.current_step + 1)  # +1 to account for landing at -1
        total_steps = len(self.step_names)  # Total including landing
        progress_pct = step_num / total_steps if total_steps > 0 else 0

        bar_width = self.style.PROGRESS_BAR_WIDTH
        bar_height = self.style.PROGRESS_BAR_HEIGHT
        bar_x = (1 - bar_width) / 2
        bar_y = 0.01

        # Background
        bar_bg = patches.Rectangle(
            (bar_x, bar_y), bar_width, bar_height,
            transform=self.fig.transFigure,
            facecolor='#2a2a2a',
            edgecolor=self.colors['dim'],
            linewidth=1
        )
        self.fig.patches.append(bar_bg)

        # Progress fill
        if progress_pct > 0:
            status_color = self.colors['accent'] if self.is_animating else self.colors['secondary']
            bar_fg = patches.Rectangle(
                (bar_x, bar_y), bar_width * progress_pct, bar_height,
                transform=self.fig.transFigure,
                facecolor=status_color,
                edgecolor='none'
            )
            self.fig.patches.append(bar_fg)

    def show(self):
        """Show the presentation in maximized window"""
        manager = plt.get_current_fig_manager()

        # Try to maximize window
        try:
            manager.window.state('zoomed')  # Windows/Linux
        except:
            try:
                manager.window.showMaximized()  # Qt backend
            except:
                pass  # Fallback - show normal size

        # Print controls reminder
        self.control_handler.print_controls_reminder()

        # Show
        plt.show()

    def create_title_box(self, ax, x: float, y: float, text: str,
                         color: str = None, fontsize: int = None):
        """
        Create a styled title box

        Args:
            ax: Matplotlib axis
            x: X position
            y: Y position
            text: Title text
            color: Border color (default primary)
            fontsize: Font size (default title size)
        """
        if color is None:
            color = self.colors['primary']
        if fontsize is None:
            fontsize = self.style.FONT_SIZE_TITLE

        from matplotlib.patches import FancyBboxPatch

        box = FancyBboxPatch(
            (x - 40, y - 10), 80, 20,
            boxstyle="round,pad=2",
            facecolor=self.colors['bg_light'],
            edgecolor=color,
            linewidth=4,
            alpha=0.95
        )
        ax.add_patch(box)

        ax.text(x, y, text,
               fontsize=fontsize,
               fontweight='bold',
               ha='center',
               va='center',
               color=color)

    def on_animation_complete(self):
        """
        Called when animation completes
        Can be overridden by subclass for custom behavior
        """
        self.is_animating = False
        print(f"  [OK] Stap {self.current_step + 1} compleet. SPATIE = volgende stap")
