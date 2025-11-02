"""
Unified control handling for all presentations
Keyboard, mouse, and navigation controls
"""

import matplotlib.pyplot as plt
from typing import Callable, Optional


class ControlHandler:
    """
    Centralized keyboard and mouse control handling
    Provides consistent navigation across all presentations
    """

    def __init__(self, presentation):
        """
        Initialize control handler for a presentation

        Args:
            presentation: The presentation instance to control
        """
        self.presentation = presentation
        self.fig = presentation.fig

        # Control key mappings
        self.KEY_NEXT = ' '  # Space
        self.KEY_PREVIOUS = 'b'
        self.KEY_RESET = 'r'
        self.KEY_QUIT = ['q', 'escape']
        self.KEY_FULLSCREEN = 'f'
        self.KEY_HELP = 'h'
        self.KEY_SELECTION = 's'  # Return to presentation selection

        # Mouse state for drawing/interaction
        self.is_drawing = False
        self.drawing_lines = []
        self.current_line = []

    def setup(self):
        """Connect all event handlers to the figure"""
        self.fig.canvas.mpl_connect('key_press_event', self.on_key_press)
        self.fig.canvas.mpl_connect('scroll_event', self.on_scroll)
        self.fig.canvas.mpl_connect('button_press_event', self.on_mouse_press)
        self.fig.canvas.mpl_connect('button_release_event', self.on_mouse_release)
        self.fig.canvas.mpl_connect('motion_notify_event', self.on_mouse_motion)

    def on_key_press(self, event):
        """
        Handle keyboard events

        Args:
            event: Matplotlib key press event
        """
        if not event.key:
            return

        # Don't process during animation unless it's quit
        if hasattr(self.presentation, 'is_animating'):
            if self.presentation.is_animating and event.key not in self.KEY_QUIT:
                return

        # Navigation controls
        if event.key == self.KEY_NEXT:
            self.handle_next()
        elif event.key == self.KEY_PREVIOUS:
            self.handle_previous()
        elif event.key == self.KEY_RESET:
            self.handle_reset()
        elif event.key in self.KEY_QUIT:
            self.handle_quit()
        elif event.key == self.KEY_SELECTION:
            self.handle_selection()
        elif event.key == self.KEY_FULLSCREEN:
            self.handle_fullscreen()
        elif event.key == self.KEY_HELP:
            self.handle_help()
        else:
            # Pass to presentation-specific handler if exists
            if hasattr(self.presentation, 'on_custom_key'):
                self.presentation.on_custom_key(event.key)

    def handle_next(self):
        """Move to next step/slide"""
        if hasattr(self.presentation, 'next_step'):
            self.presentation.next_step()
        elif hasattr(self.presentation, 'start_next_step'):
            self.presentation.start_next_step()

    def handle_previous(self):
        """Move to previous step/slide"""
        if hasattr(self.presentation, 'previous_step'):
            self.presentation.previous_step()

    def handle_reset(self):
        """Reset presentation to beginning"""
        if hasattr(self.presentation, 'reset'):
            self.presentation.reset()

    def handle_quit(self):
        """Quit the presentation"""
        plt.close(self.fig)
        print("\n👋 Presentation closed. Thanks for watching!")

    def handle_selection(self):
        """Return to presentation selection menu"""
        plt.close(self.fig)
        print("\n🔙 Returning to presentation selection menu...")

    def handle_fullscreen(self):
        """Toggle fullscreen mode"""
        try:
            manager = plt.get_current_fig_manager()
            manager.full_screen_toggle()
        except Exception as e:
            print(f"(!)  Fullscreen toggle failed: {e}")

    def handle_help(self):
        """Display help information"""
        help_text = """
        ╔══════════════════════════════════════════════╗
        ║        PRESENTATION CONTROLS HELP            ║
        ╠══════════════════════════════════════════════╣
        ║  SPACE    : Next step/slide                  ║
        ║  B        : Previous step/slide              ║
        ║  R        : Reset to beginning               ║
        ║  S        : Return to selection menu         ║
        ║  F        : Toggle fullscreen                ║
        ║  H        : Show this help                   ║
        ║  Q or ESC : Quit presentation                ║
        ╚══════════════════════════════════════════════╝
        """
        print(help_text)

    def on_scroll(self, event):
        """
        Handle mouse scroll events

        Args:
            event: Matplotlib scroll event
        """
        if hasattr(self.presentation, 'handle_scroll'):
            self.presentation.handle_scroll(event)

    def on_mouse_press(self, event):
        """
        Handle mouse button press

        Args:
            event: Matplotlib mouse press event
        """
        if hasattr(self.presentation, 'handle_mouse_press'):
            self.presentation.handle_mouse_press(event)

    def on_mouse_release(self, event):
        """
        Handle mouse button release

        Args:
            event: Matplotlib mouse release event
        """
        if hasattr(self.presentation, 'handle_mouse_release'):
            self.presentation.handle_mouse_release(event)

    def on_mouse_motion(self, event):
        """
        Handle mouse motion

        Args:
            event: Matplotlib mouse motion event
        """
        if hasattr(self.presentation, 'handle_mouse_motion'):
            self.presentation.handle_mouse_motion(event)

    @staticmethod
    def print_controls_reminder():
        """Print a brief control reminder to console"""
        print("\n[Keys]  Controls: SPACE=Next | B=Previous | R=Reset | S=Menu | F=Fullscreen | H=Help | Q=Quit\n")
