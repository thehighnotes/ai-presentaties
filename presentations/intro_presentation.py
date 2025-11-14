"""
Introductie Presentatie - AI Concepten Overzicht
Kennissessie opening: wat gaan we leren en waarom?
"""

import sys
import os
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle
import numpy as np

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core import BasePresentation, PresentationStyle


class IntroPresentation(BasePresentation):
    """Introductie presentatie voor de AI Kennissessie"""

    def __init__(self):
        """Initialize intro presentation"""
        step_names = [
            'Landing',
            'Wat is AI/ML?',
            'Waarom Deze Sessie?',
            'De Vier Hoofdonderwerpen',
            'Vectors & Embeddings',
            'Neural Networks',
            'RAG - Retrieval Augmented Generation',
            'Finetuning',
            'Prompt Engineering',
            'De Reis Begint'
        ]

        super().__init__("AI Kennissessie - Introductie", step_names)

        # Topic data
        self.topics = [
            {
                'name': 'Vectors',
                'icon': '[→]',
                'desc': 'Hoe AI betekenis vastlegt',
                'color': self.colors['vector']
            },
            {
                'name': 'Neural Networks',
                'icon': '[◉]',
                'desc': 'Hoe AI leert en beslist',
                'color': self.colors['neuron']
            },
            {
                'name': 'RAG',
                'icon': '[⚡]',
                'desc': 'Kennisbank + AI = Slimme antwoorden',
                'color': self.colors['primary']
            },
            {
                'name': 'Finetuning',
                'icon': '[⚙]',
                'desc': 'AI trainen voor specifieke taken',
                'color': self.colors['purple']
            },
            {
                'name': 'Prompt Engineering',
                'icon': '[✎]',
                'desc': 'Effectief communiceren met AI',
                'color': self.colors['secondary']
            }
        ]

        self.show_landing_page()

    def get_frames_for_step(self, step: int) -> int:
        """Custom frame counts per step"""
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

        ax.text(50, 72, 'AI Kennissessie',
                fontsize=72, fontweight='bold', ha='center', va='center',
                color=self.colors['primary'])

        ax.text(50, 64, 'Van Theorie naar Praktijk',
                fontsize=33, ha='center', va='center',
                color=self.colors['text'], alpha=0.8, style='italic')

        # Subtitle
        ax.text(50, 45, 'Ontdek hoe moderne AI werkt en wat je ermee kunt',
                fontsize=27, ha='center', va='center',
                color=self.colors['secondary'], alpha=0.9)

        # Instructions
        instr_box = FancyBboxPatch(
            (25, 15), 50, 15,
            boxstyle="round,pad=1",
            facecolor=self.colors['bg_light'],
            edgecolor=self.colors['secondary'],
            linewidth=3,
            alpha=0.9
        )
        ax.add_patch(instr_box)

        ax.text(50, 25, '* Druk op SPATIE om te beginnen *',
                fontsize=30, ha='center', va='center',
                color=self.colors['secondary'], fontweight='bold')

        ax.text(50, 20, 'SPACE=Volgende | B=Vorige | R=Reset | Q=Afsluiten',
                fontsize=18, ha='center', va='center',
                color=self.colors['dim'], style='italic')

        ax.text(50, 5, 'Interactieve visualisaties van AI concepten',
                fontsize=18, ha='center', va='center',
                color=self.colors['text'], alpha=0.5)

        plt.tight_layout()

    def animate_step(self, frame: int):
        """Animate current step"""
        total_frames = self.get_frames_for_step(self.current_step)
        progress = frame / (total_frames - 1) if total_frames > 1 else 1

        if self.current_step == 0:
            pass  # Landing is static
        elif self.current_step == 1:
            self.draw_what_is_ai(progress)
        elif self.current_step == 2:
            self.draw_why_this_session(progress)
        elif self.current_step == 3:
            self.draw_four_topics(progress)
        elif self.current_step == 4:
            self.draw_vectors_intro(progress)
        elif self.current_step == 5:
            self.draw_neural_intro(progress)
        elif self.current_step == 6:
            self.draw_rag_intro(progress)
        elif self.current_step == 7:
            self.draw_finetuning_intro(progress)
        elif self.current_step == 8:
            self.draw_prompt_intro(progress)
        elif self.current_step == 9:
            self.draw_journey_begins(progress)

        if frame >= total_frames - 1:
            self.is_animating = False

    def draw_current_step_static(self):
        """Draw current step without animation"""
        if self.current_step == -1:
            self.show_landing_page()
        elif self.current_step == 1:
            self.draw_what_is_ai(1.0)
        elif self.current_step == 2:
            self.draw_why_this_session(1.0)
        elif self.current_step == 3:
            self.draw_four_topics(1.0)
        elif self.current_step == 4:
            self.draw_vectors_intro(1.0)
        elif self.current_step == 5:
            self.draw_neural_intro(1.0)
        elif self.current_step == 6:
            self.draw_rag_intro(1.0)
        elif self.current_step == 7:
            self.draw_finetuning_intro(1.0)
        elif self.current_step == 8:
            self.draw_prompt_intro(1.0)
        elif self.current_step == 9:
            self.draw_journey_begins(1.0)
        plt.draw()

    def draw_what_is_ai(self, progress: float):
        """Step 1: What is AI/ML?"""
        self.fig.clear()
        ax = self.fig.add_subplot(111)
        ax.axis('off')
        ax.set_xlim(0, 100)
        ax.set_ylim(0, 100)

        # Title
        title_alpha = min(1.0, progress / 0.2)
        ax.text(50, 95, 'Wat is Artificiële Intelligentie?',
                fontsize=48, fontweight='bold', ha='center', va='top',
                color=self.colors['primary'], alpha=title_alpha)

        # Central AI icon
        if progress > 0.2:
            icon_alpha = min(1.0, (progress - 0.2) / 0.3)

            icon_box = FancyBboxPatch(
                (35, 50), 30, 25,
                boxstyle="round,pad=1.5",
                facecolor=self.colors['bg_light'],
                edgecolor=self.colors['primary'],
                linewidth=4,
                alpha=0.95 * icon_alpha
            )
            ax.add_patch(icon_box)

            ax.text(50, 67, 'AI', fontsize=90, ha='center', va='center',
                    fontweight='bold', alpha=icon_alpha)

            ax.text(50, 54, 'Machine Learning',
                    fontsize=21, ha='center', va='center',
                    color=self.colors['primary'], fontweight='bold',
                    alpha=icon_alpha)

        # Definitions
        definitions = [
            ('Computers die patronen herkennen', 20, 35, 0.4),
            ('Systemen die leren van data', 80, 35, 0.5),
            ('Algoritmes die zelf beslissen', 20, 20, 0.6),
            ('Modellen die voorspellen', 80, 20, 0.7)
        ]

        for text, x, y, delay in definitions:
            if progress > delay:
                alpha = min(1.0, (progress - delay) / 0.15)

                def_box = FancyBboxPatch(
                    (x - 18, y - 4), 36, 8,
                    boxstyle="round,pad=0.5",
                    facecolor=self.colors['bg_light'],
                    edgecolor=self.colors['secondary'],
                    linewidth=2,
                    alpha=0.9 * alpha
                )
                ax.add_patch(def_box)

                ax.text(x, y, text,
                        fontsize=16, ha='center', va='center',
                        color=self.colors['text'],
                        alpha=alpha)

        # Key insight
        if progress > 0.85:
            insight_alpha = min(1.0, (progress - 0.85) / 0.15)

            ax.text(50, 8, '[i] Deze sessie: Hoe werkt het technisch, en wat kun je ermee?',
                    fontsize=21, ha='center', va='center',
                    bbox=dict(boxstyle='round,pad=0.8',
                            facecolor=self.colors['bg_light'],
                            edgecolor=self.colors['accent'],
                            linewidth=2,
                            alpha=0.9),
                    color=self.colors['accent'],
                    fontweight='bold',
                    alpha=insight_alpha)

        self.add_status_indicator(progress < 1.0)
        plt.tight_layout()

    def draw_why_this_session(self, progress: float):
        """Step 2: Why this session?"""
        self.fig.clear()
        ax = self.fig.add_subplot(111)
        ax.axis('off')
        ax.set_xlim(0, 100)
        ax.set_ylim(0, 100)

        # Title
        ax.text(50, 95, 'Waarom Deze Sessie?',
                fontsize=48, fontweight='bold', ha='center', va='top',
                color=self.colors['highlight'])

        # Problems/Challenges
        challenges = [
            ('AI lijkt magisch...', 'maar het is technologie', 25, 75, 0.15, self.colors['warning']),
            ('Iedereen praat erover...', 'maar weinigen begrijpen het', 75, 75, 0.25, self.colors['warning']),
            ('Veel hype...', 'maar ook echte kansen', 25, 55, 0.35, self.colors['accent']),
            ('Lastige keuzes...', 'zonder technische kennis', 75, 55, 0.45, self.colors['accent'])
        ]

        for title, subtitle, x, y, delay, color in challenges:
            if progress > delay:
                alpha = min(1.0, (progress - delay) / 0.15)

                box = FancyBboxPatch(
                    (x - 20, y - 6), 40, 12,
                    boxstyle="round,pad=0.8",
                    facecolor=self.colors['bg_light'],
                    edgecolor=color,
                    linewidth=2,
                    alpha=0.9 * alpha
                )
                ax.add_patch(box)

                ax.text(x, y + 2, title,
                        fontsize=18, ha='center', va='center',
                        color=color, fontweight='bold',
                        alpha=alpha)

                ax.text(x, y - 2, subtitle,
                        fontsize=14, ha='center', va='center',
                        color=self.colors['text'],
                        alpha=alpha * 0.8)

        # Solution
        if progress > 0.65:
            solution_alpha = min(1.0, (progress - 0.65) / 0.25)

            solution_box = FancyBboxPatch(
                (15, 25), 70, 20,
                boxstyle="round,pad=1.5",
                facecolor=self.colors['bg_light'],
                edgecolor=self.colors['secondary'],
                linewidth=4,
                alpha=0.95 * solution_alpha
            )
            ax.add_patch(solution_box)

            ax.text(50, 38, '>> Deze Sessie Geeft Je:',
                    fontsize=27, ha='center', va='center',
                    color=self.colors['secondary'], fontweight='bold',
                    alpha=solution_alpha)

            benefits = [
                '✓ Technisch begrip van hoe AI werkt',
                '✓ Inzicht in verschillende AI-technieken',
                '✓ Praktische kennis voor betere beslissingen'
            ]

            for i, benefit in enumerate(benefits):
                ax.text(50, 32 - i * 4, benefit,
                        fontsize=16, ha='center', va='center',
                        color=self.colors['text'],
                        alpha=solution_alpha * 0.9)

        # Bottom message
        if progress > 0.9:
            msg_alpha = min(1.0, (progress - 0.9) / 0.1)
            ax.text(50, 8, '[!] Na deze sessie snap je wat er onder de motorkap gebeurt',
                    fontsize=19, ha='center', va='center',
                    color=self.colors['highlight'],
                    fontweight='bold',
                    alpha=msg_alpha)

        self.add_status_indicator(progress < 1.0)
        plt.tight_layout()

    def draw_four_topics(self, progress: float):
        """Step 3: The four main topics"""
        self.fig.clear()
        ax = self.fig.add_subplot(111)
        ax.axis('off')
        ax.set_xlim(0, 100)
        ax.set_ylim(0, 100)

        # Title
        ax.text(50, 95, 'De Vijf Hoofdonderwerpen',
                fontsize=48, fontweight='bold', ha='center', va='top',
                color=self.colors['primary'])

        ax.text(50, 89, 'Een reis door moderne AI-technologie',
                fontsize=24, ha='center', va='top',
                color=self.colors['text'], alpha=0.7, style='italic')

        # Topics in circular layout
        angles = [90, 162, 234, 306, 18]  # Evenly spaced around circle
        radius = 28

        for idx, (topic, angle) in enumerate(zip(self.topics, angles)):
            delay = 0.2 + idx * 0.15
            if progress > delay:
                alpha = min(1.0, (progress - delay) / 0.15)

                # Calculate position
                angle_rad = np.radians(angle)
                x = 50 + radius * np.cos(angle_rad)
                y = 50 + radius * np.sin(angle_rad)

                # Topic box
                box = FancyBboxPatch(
                    (x - 10, y - 6), 20, 12,
                    boxstyle="round,pad=0.8",
                    facecolor=self.colors['bg_light'],
                    edgecolor=topic['color'],
                    linewidth=3,
                    alpha=0.95 * alpha
                )
                ax.add_patch(box)

                # Icon
                ax.text(x, y + 3, topic['icon'],
                        fontsize=36, ha='center', va='center',
                        alpha=alpha)

                # Name
                ax.text(x, y - 1, topic['name'],
                        fontsize=16, ha='center', va='center',
                        color=topic['color'], fontweight='bold',
                        alpha=alpha)

                # Description outside
                desc_x = 50 + (radius + 12) * np.cos(angle_rad)
                desc_y = 50 + (radius + 12) * np.sin(angle_rad)

                ax.text(desc_x, desc_y, topic['desc'],
                        fontsize=12, ha='center', va='center',
                        color=self.colors['text'],
                        alpha=alpha * 0.8)

        # Center
        if progress > 0.15:
            center_alpha = min(1.0, (progress - 0.15) / 0.2)

            center_circle = Circle((50, 50), 8,
                                  facecolor=self.colors['bg_light'],
                                  edgecolor=self.colors['highlight'],
                                  linewidth=4,
                                  alpha=0.95 * center_alpha)
            ax.add_patch(center_circle)

            ax.text(50, 51, 'AI\nKennis',
                    fontsize=16, ha='center', va='center',
                    color=self.colors['highlight'], fontweight='bold',
                    alpha=center_alpha,
                    linespacing=1.2)

        # Bottom insight
        if progress > 0.85:
            insight_alpha = min(1.0, (progress - 0.85) / 0.15)
            ax.text(50, 8, '[→] We beginnen met Vectors en eindigen met Prompt Engineering',
                    fontsize=18, ha='center', va='center',
                    color=self.colors['accent'],
                    fontweight='bold',
                    alpha=insight_alpha)

        self.add_status_indicator(progress < 1.0)
        plt.tight_layout()

    def draw_vectors_intro(self, progress: float):
        """Step 4: Vectors introduction"""
        self.fig.clear()
        ax = self.fig.add_subplot(111)
        ax.axis('off')
        ax.set_xlim(0, 100)
        ax.set_ylim(0, 100)

        # Title
        ax.text(50, 95, 'Onderwerp 1: Vectors & Embeddings',
                fontsize=42, fontweight='bold', ha='center', va='top',
                color=self.colors['vector'])

        # Visual: word to vector
        if progress > 0.15:
            word_alpha = min(1.0, (progress - 0.15) / 0.2)

            # Word box
            word_box = FancyBboxPatch(
                (15, 55), 20, 10,
                boxstyle="round,pad=0.8",
                facecolor=self.colors['bg_light'],
                edgecolor=self.colors['text'],
                linewidth=2,
                alpha=0.9 * word_alpha
            )
            ax.add_patch(word_box)

            ax.text(25, 60, '"Hond"',
                    fontsize=24, ha='center', va='center',
                    color=self.colors['text'],
                    alpha=word_alpha)

        # Arrow
        if progress > 0.35:
            arrow_alpha = min(1.0, (progress - 0.35) / 0.2)
            arrow = FancyArrowPatch(
                (35, 60), (45, 60),
                arrowstyle='-|>',
                mutation_scale=30,
                linewidth=3,
                color=self.colors['vector'],
                alpha=arrow_alpha
            )
            ax.add_artist(arrow)

            ax.text(40, 63, 'Embedding\nModel',
                    fontsize=14, ha='center', va='bottom',
                    color=self.colors['vector'],
                    alpha=arrow_alpha)

        # Vector
        if progress > 0.55:
            vec_alpha = min(1.0, (progress - 0.55) / 0.25)

            vec_box = FancyBboxPatch(
                (55, 55), 30, 10,
                boxstyle="round,pad=0.8",
                facecolor='#1a3a1a',
                edgecolor=self.colors['vector'],
                linewidth=2,
                alpha=0.9 * vec_alpha
            )
            ax.add_patch(vec_box)

            ax.text(70, 60, '[0.34, -0.12, 0.89, ...]',
                    fontsize=16, ha='center', va='center',
                    color=self.colors['vector'],
                    family='monospace',
                    alpha=vec_alpha)

        # Key points
        key_points = [
            ('Hoe AI betekenis vastlegt', 40, 0.7),
            ('Woorden → Getallen (vectoren)', 35, 0.75),
            ('Vergelijkbare betekenis = Dichtbij in ruimte', 30, 0.8),
            ('Basis voor veel AI-toepassingen', 25, 0.85)
        ]

        for text, y, delay in key_points:
            if progress > delay:
                alpha = min(1.0, (progress - delay) / 0.1)
                ax.text(50, y, f'• {text}',
                        fontsize=18, ha='center', va='center',
                        color=self.colors['text'],
                        alpha=alpha)

        # Bottom
        if progress > 0.9:
            bottom_alpha = min(1.0, (progress - 0.9) / 0.1)
            ax.text(50, 8, '[→] Straks: 2D, 3D visualisaties en word arithmetic!',
                    fontsize=18, ha='center', va='center',
                    color=self.colors['secondary'],
                    fontweight='bold',
                    alpha=bottom_alpha)

        self.add_status_indicator(progress < 1.0)
        plt.tight_layout()

    def draw_neural_intro(self, progress: float):
        """Step 5: Neural Networks introduction"""
        self.fig.clear()
        ax = self.fig.add_subplot(111)
        ax.axis('off')
        ax.set_xlim(0, 100)
        ax.set_ylim(0, 100)

        # Title
        ax.text(50, 95, 'Onderwerp 2: Neural Networks',
                fontsize=42, fontweight='bold', ha='center', va='top',
                color=self.colors['neuron'])

        # Simple network visualization
        if progress > 0.15:
            net_alpha = min(1.0, (progress - 0.15) / 0.3)

            # Input nodes
            for i, y in enumerate([65, 55]):
                circle = Circle((25, y), 2,
                               facecolor=self.colors['neuron'],
                               edgecolor='white',
                               linewidth=2,
                               alpha=net_alpha)
                ax.add_patch(circle)

            # Hidden nodes
            for i, y in enumerate([68, 60, 52]):
                circle = Circle((50, y), 2,
                               facecolor=self.colors['neuron'],
                               edgecolor='white',
                               linewidth=2,
                               alpha=net_alpha)
                ax.add_patch(circle)

            # Output node
            circle = Circle((75, 60), 2,
                           facecolor=self.colors['neuron'],
                           edgecolor='white',
                           linewidth=2,
                           alpha=net_alpha)
            ax.add_patch(circle)

            # Connections
            for y1 in [65, 55]:
                for y2 in [68, 60, 52]:
                    ax.plot([25, 50], [y1, y2],
                           color=self.colors['connection'],
                           linewidth=1,
                           alpha=net_alpha * 0.4)

            for y1 in [68, 60, 52]:
                ax.plot([50, 75], [y1, 60],
                       color=self.colors['connection'],
                       linewidth=1,
                       alpha=net_alpha * 0.4)

            # Labels
            ax.text(25, 48, 'Input', fontsize=14, ha='center',
                    color=self.colors['text'], alpha=net_alpha)
            ax.text(50, 45, 'Hidden', fontsize=14, ha='center',
                    color=self.colors['text'], alpha=net_alpha)
            ax.text(75, 48, 'Output', fontsize=14, ha='center',
                    color=self.colors['text'], alpha=net_alpha)

        # Key points
        key_points = [
            ('Geïnspireerd door de hersenen', 38, 0.5),
            ('Netwerk van "neuronen" met gewichten', 33, 0.6),
            ('Leert patronen door training', 28, 0.7),
            ('Kan complexe problemen oplossen', 23, 0.8)
        ]

        for text, y, delay in key_points:
            if progress > delay:
                alpha = min(1.0, (progress - delay) / 0.1)
                ax.text(50, y, f'• {text}',
                        fontsize=18, ha='center', va='center',
                        color=self.colors['text'],
                        alpha=alpha)

        # Bottom
        if progress > 0.9:
            bottom_alpha = min(1.0, (progress - 0.9) / 0.1)
            ax.text(50, 8, '[→] Straks: Live training visualisatie met XOR probleem!',
                    fontsize=18, ha='center', va='center',
                    color=self.colors['secondary'],
                    fontweight='bold',
                    alpha=bottom_alpha)

        self.add_status_indicator(progress < 1.0)
        plt.tight_layout()

    def draw_rag_intro(self, progress: float):
        """Step 6: RAG introduction"""
        self.fig.clear()
        ax = self.fig.add_subplot(111)
        ax.axis('off')
        ax.set_xlim(0, 100)
        ax.set_ylim(0, 100)

        # Title
        ax.text(50, 95, 'Onderwerp 3: RAG',
                fontsize=42, fontweight='bold', ha='center', va='top',
                color=self.colors['primary'])

        ax.text(50, 89, 'Retrieval Augmented Generation',
                fontsize=24, ha='center', va='top',
                color=self.colors['text'], alpha=0.7, style='italic')

        # Visual flow
        flow_items = [
            ('📚\nKennisbank', 15, 60, 0.2, self.colors['accent']),
            ('🔍\nZoeken', 35, 60, 0.35, self.colors['secondary']),
            ('⚡\nAI Model', 55, 60, 0.5, self.colors['primary']),
            ('✓\nAntwoord', 75, 60, 0.65, self.colors['correct'])
        ]

        for text, x, y, delay, color in flow_items:
            if progress > delay:
                alpha = min(1.0, (progress - delay) / 0.15)

                box = FancyBboxPatch(
                    (x - 7, y - 6), 14, 12,
                    boxstyle="round,pad=0.8",
                    facecolor=self.colors['bg_light'],
                    edgecolor=color,
                    linewidth=3,
                    alpha=0.95 * alpha
                )
                ax.add_patch(box)

                ax.text(x, y, text,
                        fontsize=18, ha='center', va='center',
                        color=color,
                        alpha=alpha,
                        linespacing=1.3)

                # Arrow to next
                if x < 75 and progress > delay + 0.1:
                    arrow_alpha = min(1.0, (progress - delay - 0.1) / 0.1)
                    arrow = FancyArrowPatch(
                        (x + 7, y), (x + 13, y),
                        arrowstyle='-|>',
                        mutation_scale=20,
                        linewidth=2,
                        color=self.colors['dim'],
                        alpha=arrow_alpha
                    )
                    ax.add_artist(arrow)

        # Key points
        key_points = [
            ('Combineert kennisbank met AI', 42, 0.75),
            ('Actuele, specifieke informatie', 37, 0.8),
            ('Geen training nodig!', 32, 0.85),
            ('Ideaal voor interne documenten', 27, 0.9)
        ]

        for text, y, delay in key_points:
            if progress > delay:
                alpha = min(1.0, (progress - delay) / 0.1)
                ax.text(50, y, f'• {text}',
                        fontsize=18, ha='center', va='center',
                        color=self.colors['text'],
                        alpha=alpha)

        # Bottom
        if progress > 0.92:
            bottom_alpha = min(1.0, (progress - 0.92) / 0.08)
            ax.text(50, 8, '[→] Straks: Stap-voor-stap door het hele RAG proces!',
                    fontsize=18, ha='center', va='center',
                    color=self.colors['secondary'],
                    fontweight='bold',
                    alpha=bottom_alpha)

        self.add_status_indicator(progress < 1.0)
        plt.tight_layout()

    def draw_finetuning_intro(self, progress: float):
        """Step 7: Finetuning introduction"""
        self.fig.clear()
        ax = self.fig.add_subplot(111)
        ax.axis('off')
        ax.set_xlim(0, 100)
        ax.set_ylim(0, 100)

        # Title
        ax.text(50, 95, 'Onderwerp 4: Finetuning',
                fontsize=42, fontweight='bold', ha='center', va='top',
                color=self.colors['purple'])

        # Before/After visualization
        if progress > 0.15:
            before_alpha = min(1.0, (progress - 0.15) / 0.2)

            # Before
            before_box = FancyBboxPatch(
                (15, 55), 25, 15,
                boxstyle="round,pad=1",
                facecolor='#2a1a1a',
                edgecolor=self.colors['warning'],
                linewidth=2,
                alpha=0.9 * before_alpha
            )
            ax.add_patch(before_box)

            ax.text(27.5, 67, 'Voor', fontsize=18, ha='center',
                    color=self.colors['warning'], fontweight='bold',
                    alpha=before_alpha)

            ax.text(27.5, 62, 'Algemeen\nModel',
                    fontsize=16, ha='center', va='center',
                    color=self.colors['text'],
                    alpha=before_alpha,
                    linespacing=1.3)

        # Training arrow
        if progress > 0.35:
            arrow_alpha = min(1.0, (progress - 0.35) / 0.2)

            arrow = FancyArrowPatch(
                (40, 62), (60, 62),
                arrowstyle='-|>',
                mutation_scale=35,
                linewidth=4,
                color=self.colors['purple'],
                alpha=arrow_alpha
            )
            ax.add_artist(arrow)

            ax.text(50, 67, 'Training',
                    fontsize=16, ha='center',
                    color=self.colors['purple'],
                    fontweight='bold',
                    alpha=arrow_alpha)

        # After
        if progress > 0.55:
            after_alpha = min(1.0, (progress - 0.55) / 0.2)

            after_box = FancyBboxPatch(
                (60, 55), 25, 15,
                boxstyle="round,pad=1",
                facecolor='#1a3a1a',
                edgecolor=self.colors['secondary'],
                linewidth=3,
                alpha=0.95 * after_alpha
            )
            ax.add_patch(after_box)

            ax.text(72.5, 67, 'Na', fontsize=18, ha='center',
                    color=self.colors['secondary'], fontweight='bold',
                    alpha=after_alpha)

            ax.text(72.5, 62, 'Specialist\nModel',
                    fontsize=16, ha='center', va='center',
                    color=self.colors['text'],
                    alpha=after_alpha,
                    linespacing=1.3)

        # Key points
        key_points = [
            ('Trainen van bestaand model', 42, 0.7),
            ('Voor specifieke domein/taak', 37, 0.75),
            ('Verbetert prestaties dramatisch', 32, 0.8),
            ('Vereist training data', 27, 0.85)
        ]

        for text, y, delay in key_points:
            if progress > delay:
                alpha = min(1.0, (progress - delay) / 0.1)
                ax.text(50, y, f'• {text}',
                        fontsize=18, ha='center', va='center',
                        color=self.colors['text'],
                        alpha=alpha)

        # Bottom
        if progress > 0.9:
            bottom_alpha = min(1.0, (progress - 0.9) / 0.1)
            ax.text(50, 8, '[→] Straks: Zie hoe model weights veranderen tijdens training!',
                    fontsize=18, ha='center', va='center',
                    color=self.colors['secondary'],
                    fontweight='bold',
                    alpha=bottom_alpha)

        self.add_status_indicator(progress < 1.0)
        plt.tight_layout()

    def draw_prompt_intro(self, progress: float):
        """Step 8: Prompt Engineering introduction"""
        self.fig.clear()
        ax = self.fig.add_subplot(111)
        ax.axis('off')
        ax.set_xlim(0, 100)
        ax.set_ylim(0, 100)

        # Title
        ax.text(50, 95, 'Onderwerp 5: Prompt Engineering',
                fontsize=42, fontweight='bold', ha='center', va='top',
                color=self.colors['secondary'])

        # Visual: bad vs good prompt
        if progress > 0.15:
            bad_alpha = min(1.0, (progress - 0.15) / 0.2)

            # Bad prompt
            bad_box = FancyBboxPatch(
                (10, 60), 35, 15,
                boxstyle="round,pad=1",
                facecolor='#2a1a1a',
                edgecolor=self.colors['warning'],
                linewidth=2,
                alpha=0.9 * bad_alpha
            )
            ax.add_patch(bad_box)

            ax.text(27.5, 72, '✗ Slechte Prompt', fontsize=16, ha='center',
                    color=self.colors['warning'], fontweight='bold',
                    alpha=bad_alpha)

            ax.text(27.5, 67, '"Schrijf iets"',
                    fontsize=18, ha='center', va='center',
                    color=self.colors['text'],
                    alpha=bad_alpha,
                    style='italic')

            ax.text(27.5, 63, 'Vaag, geen context',
                    fontsize=12, ha='center',
                    color=self.colors['dim'],
                    alpha=bad_alpha)

        # Good prompt
        if progress > 0.4:
            good_alpha = min(1.0, (progress - 0.4) / 0.2)

            good_box = FancyBboxPatch(
                (55, 60), 35, 15,
                boxstyle="round,pad=1",
                facecolor='#1a3a1a',
                edgecolor=self.colors['secondary'],
                linewidth=3,
                alpha=0.95 * good_alpha
            )
            ax.add_patch(good_box)

            ax.text(72.5, 72, '✓ Goede Prompt', fontsize=16, ha='center',
                    color=self.colors['secondary'], fontweight='bold',
                    alpha=good_alpha)

            ax.text(72.5, 67, '"Schrijf email..."',
                    fontsize=18, ha='center', va='center',
                    color=self.colors['text'],
                    alpha=good_alpha,
                    style='italic')

            ax.text(72.5, 63, 'Specifiek, duidelijk',
                    fontsize=12, ha='center',
                    color=self.colors['secondary'],
                    alpha=good_alpha)

        # Key points
        key_points = [
            ('Hoe je effectief communiceert met AI', 45, 0.6),
            ('Technieken voor betere resultaten', 40, 0.7),
            ('Patronen en best practices', 35, 0.8),
            ('Limitaties en valkuilen', 30, 0.85)
        ]

        for text, y, delay in key_points:
            if progress > delay:
                alpha = min(1.0, (progress - delay) / 0.1)
                ax.text(50, y, f'• {text}',
                        fontsize=18, ha='center', va='center',
                        color=self.colors['text'],
                        alpha=alpha)

        # Bottom
        if progress > 0.9:
            bottom_alpha = min(1.0, (progress - 0.9) / 0.1)
            ax.text(50, 8, '[→] Straks: Praktische technieken en voorbeelden!',
                    fontsize=18, ha='center', va='center',
                    color=self.colors['secondary'],
                    fontweight='bold',
                    alpha=bottom_alpha)

        self.add_status_indicator(progress < 1.0)
        plt.tight_layout()

    def draw_journey_begins(self, progress: float):
        """Step 9: The journey begins"""
        self.fig.clear()
        ax = self.fig.add_subplot(111)
        ax.axis('off')
        ax.set_xlim(0, 100)
        ax.set_ylim(0, 100)

        # Title with animation
        title_alpha = min(1.0, progress / 0.2)

        # Pulse effect on title
        if progress > 0.5:
            pulse = 1 + 0.05 * np.sin(progress * 20)
            fontsize = 54 * pulse
        else:
            fontsize = 54

        ax.text(50, 80, 'Klaar Voor De Start?',
                fontsize=fontsize, fontweight='bold', ha='center', va='center',
                color=self.colors['highlight'], alpha=title_alpha)

        # Path visualization
        if progress > 0.2:
            path_alpha = min(1.0, (progress - 0.2) / 0.3)

            path_items = [
                ('1', 'Vectors', 20, self.colors['vector']),
                ('2', 'Neural Nets', 35, self.colors['neuron']),
                ('3', 'RAG', 50, self.colors['primary']),
                ('4', 'Finetuning', 65, self.colors['purple']),
                ('5', 'Prompting', 80, self.colors['secondary'])
            ]

            for num, name, x, color in path_items:
                # Node
                circle = Circle((x, 55), 4,
                               facecolor=self.colors['bg_light'],
                               edgecolor=color,
                               linewidth=3,
                               alpha=0.95 * path_alpha)
                ax.add_patch(circle)

                ax.text(x, 55, num,
                        fontsize=21, ha='center', va='center',
                        color=color, fontweight='bold',
                        alpha=path_alpha)

                ax.text(x, 47, name,
                        fontsize=14, ha='center',
                        color=self.colors['text'],
                        alpha=path_alpha)

                # Line to next
                if x < 80:
                    ax.plot([x + 4, x + 11], [55, 55],
                           color=self.colors['dim'],
                           linewidth=2,
                           alpha=path_alpha * 0.5)

        # Key messages
        messages = [
            ('Na deze sessie begrijp je:', 35, 0.5, self.colors['text'], 21),
            ('• Hoe AI betekenis vastlegt en verwerkt', 28, 0.6, self.colors['text'], 18),
            ('• Verschillende AI-technieken en hun toepassingen', 23, 0.65, self.colors['text'], 18),
            ('• Hoe je zelf effectief met AI kunt werken', 18, 0.7, self.colors['text'], 18)
        ]

        for text, y, delay, color, size in messages:
            if progress > delay:
                alpha = min(1.0, (progress - delay) / 0.1)
                ax.text(50, y, text,
                        fontsize=size, ha='center', va='center',
                        color=color,
                        alpha=alpha)

        # Final CTA
        if progress > 0.8:
            cta_alpha = min(1.0, (progress - 0.8) / 0.2)

            cta_box = FancyBboxPatch(
                (20, 5), 60, 8,
                boxstyle="round,pad=1",
                facecolor=self.colors['bg_light'],
                edgecolor=self.colors['highlight'],
                linewidth=4,
                alpha=0.95 * cta_alpha
            )
            ax.add_patch(cta_box)

            ax.text(50, 9, '>> Druk op SPATIE om te beginnen met Vectors! >>',
                    fontsize=24, ha='center', va='center',
                    color=self.colors['highlight'],
                    fontweight='bold',
                    alpha=cta_alpha)

        self.add_status_indicator(progress < 1.0)
        plt.tight_layout()

    def add_status_indicator(self, is_animating):
        """Add progress indicator"""
        if is_animating:
            self.fig.text(0.95, 0.02, '...', fontsize=24, ha='right', va='bottom',
                         color=self.colors['accent'], fontweight='bold')


def main():
    """Main entry point"""
    print("="*80)
    print("AI KENNISSESSIE - INTRODUCTIE")
    print("="*80)
    print("\n[#] Deze presentatie introduceert:")
    print("  1. Wat is AI/ML?")
    print("  2. Waarom deze sessie?")
    print("  3. De vijf hoofdonderwerpen")
    print("  4-8. Introductie van elk onderwerp")
    print("  9. De reis begint!")
    print("\n[Keys]  Controls: SPACE=Volgende | B=Vorige | R=Reset | Q=Quit")
    print("="*80 + "\n")

    presentation = IntroPresentation()
    presentation.show()


if __name__ == "__main__":
    main()
