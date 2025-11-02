"""
Main Menu Presentation - Visual menu for selecting presentations
Beautiful, interactive menu using matplotlib
"""

import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle
from core.styling import PresentationStyle
import sys


class MainMenu:
    """Visual menu for presentation selection"""

    def __init__(self, presentations):
        """Initialize menu with presentation list"""
        self.presentations = presentations
        self.colors = PresentationStyle.COLORS
        self.selected_index = 0

        # Setup figure
        plt.style.use('dark_background')
        self.fig, self.ax = plt.subplots(figsize=(16, 9))
        self.fig.patch.set_facecolor(self.colors['bg'])
        self.ax.set_facecolor(self.colors['bg'])
        self.ax.axis('off')
        self.ax.set_xlim(0, 100)
        self.ax.set_ylim(0, 100)

        # Key bindings
        self.fig.canvas.mpl_connect('key_press_event', self.on_key_press)

        self.draw_menu()

    def draw_menu(self):
        """Draw the visual menu"""
        self.ax.clear()
        self.ax.axis('off')
        self.ax.set_xlim(0, 100)
        self.ax.set_ylim(0, 100)

        # Title
        title_box = FancyBboxPatch(
            (10, 85), 80, 12,
            boxstyle="round,pad=1.5",
            facecolor=self.colors['bg_light'],
            edgecolor=self.colors['highlight'],
            linewidth=4,
            alpha=0.95
        )
        self.ax.add_patch(title_box)

        self.ax.text(50, 93, 'AI KENNISSESSIE',
                     fontsize=54, fontweight='bold', ha='center',
                     color=self.colors['highlight'])

        self.ax.text(50, 87, 'Kies een presentatie om te starten',
                     fontsize=24, ha='center',
                     color=self.colors['text'], alpha=0.7, style='italic')

        # Presentation cards
        card_height = 11
        card_spacing = 2.5
        start_y = 70

        for idx, pres in enumerate(self.presentations):
            y = start_y - idx * (card_height + card_spacing)
            is_selected = (idx == self.selected_index)

            # Card box
            if is_selected:
                edge_color = self.colors['highlight']
                edge_width = 5
                alpha = 1.0
            else:
                edge_color = self.colors['grid']
                edge_width = 2
                alpha = 0.85

            card = FancyBboxPatch(
                (12, y - card_height + 2), 76, card_height - 2,
                boxstyle="round,pad=1",
                facecolor=self.colors['bg_light'],
                edgecolor=edge_color,
                linewidth=edge_width,
                alpha=alpha
            )
            self.ax.add_patch(card)

            # Number badge
            badge_x = 16
            badge_y = y - card_height/2 + 1

            badge_colors = [
                self.colors['primary'],
                self.colors['secondary'],
                self.colors['accent'],
                self.colors['purple'],
                self.colors['cyan']
            ]
            badge_color = badge_colors[idx % len(badge_colors)]

            badge = FancyBboxPatch(
                (badge_x - 2, badge_y - 2.5), 4, 5,
                boxstyle="round,pad=0.3",
                facecolor=badge_color,
                edgecolor='white',
                linewidth=2,
                alpha=1.0
            )
            self.ax.add_patch(badge)

            self.ax.text(badge_x, badge_y, str(idx + 1),
                         fontsize=27, ha='center', va='center',
                         color='white', fontweight='bold')

            # Icon and title
            icon_x = 24
            title_x = 28
            desc_x = 28
            duration_x = 80

            self.ax.text(icon_x, y - 3, pres['icon'],
                         fontsize=30, ha='center', va='center',
                         color=badge_color)

            title_color = self.colors['highlight'] if is_selected else self.colors['text']
            self.ax.text(title_x, y - 2.5, pres['name'],
                         fontsize=24, ha='left', va='center',
                         color=title_color, fontweight='bold')

            self.ax.text(desc_x, y - 6, pres['description'],
                         fontsize=15, ha='left', va='center',
                         color=self.colors['text'], alpha=0.8)

            self.ax.text(duration_x, y - 6, pres['duration'],
                         fontsize=14, ha='right', va='center',
                         color=self.colors['dim'], style='italic')

        # Controls box at bottom
        controls_box = FancyBboxPatch(
            (10, 2), 80, 8,
            boxstyle="round,pad=0.8",
            facecolor=self.colors['bg_light'],
            edgecolor=self.colors['secondary'],
            linewidth=3,
            alpha=0.9
        )
        self.ax.add_patch(controls_box)

        self.ax.text(50, 7.5, '[Keys]  Controls',
                     fontsize=18, ha='center', va='center',
                     color=self.colors['secondary'], fontweight='bold')

        controls_text = '↑↓ = Selecteer  •  ENTER/SPACE = Start  •  A = Alles afspelen  •  Q = Afsluiten'
        self.ax.text(50, 4.5, controls_text,
                     fontsize=16, ha='center', va='center',
                     color=self.colors['text'], alpha=0.9)

        plt.tight_layout()
        plt.draw()

    def on_key_press(self, event):
        """Handle key presses"""
        if event.key == 'up':
            self.selected_index = (self.selected_index - 1) % len(self.presentations)
            self.draw_menu()

        elif event.key == 'down':
            self.selected_index = (self.selected_index + 1) % len(self.presentations)
            self.draw_menu()

        elif event.key in ['enter', ' ']:
            # Start selected presentation
            plt.close(self.fig)
            self.choice = str(self.selected_index + 1)

        elif event.key == 'a':
            # Play all
            plt.close(self.fig)
            self.choice = 'all'

        elif event.key == 'q':
            # Quit
            plt.close(self.fig)
            self.choice = 'q'

        elif event.key.isdigit() and 1 <= int(event.key) <= len(self.presentations):
            # Direct selection via number
            self.selected_index = int(event.key) - 1
            plt.close(self.fig)
            self.choice = event.key

    def show(self):
        """Show menu and wait for selection"""
        self.choice = None
        plt.show()
        return self.choice if self.choice else 'q'
