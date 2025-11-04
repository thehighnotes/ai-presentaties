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

        # FULLSCREEN - voeg deze regel toe
        manager = plt.get_current_fig_manager()
        manager.full_screen_toggle()  # Voor de meeste backends

        # Key bindings
        self.fig.canvas.mpl_connect('key_press_event', self.on_key_press)

        self.draw_menu()

    def draw_menu(self):
        """Draw the visual menu - VERBETERDE LAYOUT"""
        self.ax.clear()
        self.ax.axis('off')
        self.ax.set_xlim(0, 100)
        self.ax.set_ylim(0, 100)
        
        # === TITLE SECTION - Compacter en eleganter ===
        title_box = FancyBboxPatch(
            (8, 86), 84, 11,
            boxstyle="round,pad=1.2",
            facecolor=self.colors['bg_light'],
            edgecolor=self.colors['highlight'],
            linewidth=3,
            alpha=0.95
        )
        self.ax.add_patch(title_box)
        
        self.ax.text(50, 90.5, 'AI KENNISSESSIE',
                    fontsize=48, fontweight='bold', ha='center',
                    color=self.colors['highlight'], 
                    family='sans-serif')
        
        self.ax.text(50, 86.5, 'Kies een presentatie om te starten',
                    fontsize=20, ha='center',
                    color=self.colors['text'], alpha=0.75, style='italic')
        
        # === PRESENTATION CARDS - Betere spacing en uitlijning ===
        card_height = 10.5  # Iets compacter
        card_spacing = 2.8  # Meer ruimte tussen cards
        start_y = 72        # Start lager voor betere balans
        
        for idx, pres in enumerate(self.presentations):
            y = start_y - idx * (card_height + card_spacing)
            is_selected = (idx == self.selected_index)
            
            # Card box met subtielere styling
            if is_selected:
                edge_color = self.colors['highlight']
                edge_width = 4
                alpha = 1.0
                shadow = True
            else:
                edge_color = self.colors['grid']
                edge_width = 2
                alpha = 0.85
                shadow = False
            
            # Shadow effect voor geselecteerde card
            if shadow:
                shadow_card = FancyBboxPatch(
                    (12.3, y - card_height + 1.7), 76, card_height - 2,
                    boxstyle="round,pad=1",
                    facecolor='black',
                    edgecolor='none',
                    alpha=0.3
                )
                self.ax.add_patch(shadow_card)
            
            card = FancyBboxPatch(
                (12, y - card_height + 2), 76, card_height - 2,
                boxstyle="round,pad=1",
                facecolor=self.colors['bg_light'],
                edgecolor=edge_color,
                linewidth=edge_width,
                alpha=alpha
            )
            self.ax.add_patch(card)
            
            # Number badge - iets groter en duidelijker
            badge_x = 17
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
                (badge_x - 2.2, badge_y - 2.8), 4.4, 5.6,
                boxstyle="round,pad=0.35",
                facecolor=badge_color,
                edgecolor='white',
                linewidth=2.5,
                alpha=1.0
            )
            self.ax.add_patch(badge)
            
            self.ax.text(badge_x, badge_y, str(idx + 1),
                        fontsize=30, ha='center', va='center',
                        color='white', fontweight='bold')
            
            # Content - betere uitlijning en spacing
            icon_x = 26
            title_x = 30
            desc_x = 30
            duration_x = 82
            
            # Icon
            self.ax.text(icon_x, y - 3.2, pres['icon'],
                        fontsize=28, ha='center', va='center',
                        color=badge_color, fontweight='bold')
            
            # Title - groter en prominenter
            title_color = self.colors['highlight'] if is_selected else self.colors['text']
            self.ax.text(title_x, y - 2.5, pres['name'],
                        fontsize=26, ha='left', va='center',
                        color=title_color, fontweight='bold')
            
            # Description - betere leesbaarheid
            self.ax.text(desc_x, y - 6.2, pres['description'],
                        fontsize=16, ha='left', va='center',
                        color=self.colors['text'], alpha=0.85)
            
            # Duration - rechts uitgelijnd
            self.ax.text(duration_x, y - 6.2, pres['duration'],
                        fontsize=15, ha='right', va='center',
                        color=self.colors['dim'], style='italic', alpha=0.9)
        
        # === CONTROLS BOX - Compacter en moderner ===
        controls_box = FancyBboxPatch(
            (8, 2), 84, 7,
            boxstyle="round,pad=0.7",
            facecolor=self.colors['bg_light'],
            edgecolor=self.colors['secondary'],
            linewidth=2.5,
            alpha=0.92
        )
        self.ax.add_patch(controls_box)
        
        # Controls header
        self.ax.text(50, 7, '[Keys]  Controls',
                    fontsize=17, ha='center', va='center',
                    color=self.colors['secondary'], fontweight='bold')
        
        # Controls text - overzichtelijker
        controls_text = '↑↓ = Selecteer  •  ENTER/SPACE = Start  •  A = Alles afspelen  •  Q = Afsluiten'
        self.ax.text(50, 4.2, controls_text,
                    fontsize=15, ha='center', va='center',
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
