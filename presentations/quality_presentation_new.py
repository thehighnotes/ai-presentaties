"""
Quality Presentation - Completely Redesigned
Simple, visual, practical - for BiSL advisors

Steps:
1. Landing - Intro
2. De Drie Keuzes - RAG, Finetuning, Hybrid (visual decision)
3. De Belangrijkste Vraag - Stakeholder web (wie betrek je?)
4. Topje van de IJsberg - What you see vs what you need to think about
5. Waar Begin Je? - Practical first steps

~5 minutes, clear, visual, actionable
"""

from core.base_presentation import BasePresentation
from core.styling import PresentationStyle
from matplotlib.patches import FancyBboxPatch, Circle, FancyArrowPatch, Rectangle, Wedge
import matplotlib.pyplot as plt
import numpy as np


class QualityPresentation(BasePresentation):
    """
    Quality Governance Presentation - Redesigned for BiSL advisors
    Focus: Insight, key questions, practical starting points
    """

    def __init__(self):
        """Initialize the quality presentation"""
        step_names = [
            'Landing',
            'De Drie Keuzes',
            'Wanneer Heb Je Embeddings Nodig?',
            'Cloud of Lokaal?',
            'De Belangrijkste Vraag',
            'Topje van de IJsberg'
        ]

        super().__init__("AI Kwaliteit: Praktische Inzichten", step_names)

    def animate_step(self, frame: int):
        """Animate current step"""
        total_frames = self.get_frames_for_step(self.current_step)
        progress = frame / (total_frames - 1) if total_frames > 1 else 1

        self.draw_step(self.current_step, progress)

        if frame >= total_frames - 1:
            self.is_animating = False

    def draw_current_step_static(self):
        """Draw current step without animation"""
        if self.current_step == -1:
            self.draw_landing(1.0)
        else:
            self.draw_step(self.current_step, 1.0)

    def draw_step(self, step: int, progress: float):
        """Draw the current step"""
        if step == 0:
            self.draw_landing(progress)
        elif step == 1:
            self.draw_three_choices(progress)
        elif step == 2:
            self.draw_when_embeddings(progress)
        elif step == 3:
            self.draw_cloud_vs_local(progress)
        elif step == 4:
            self.draw_stakeholder_web(progress)
        elif step == 5:
            self.draw_iceberg(progress)

    def draw_landing(self, progress: float):
        """Landing page - simple and clear"""
        self.fig.clear()
        ax = self.fig.add_subplot(111)
        ax.axis('off')
        ax.set_xlim(0, 100)
        ax.set_ylim(0, 100)

        # Title
        ax.text(50, 70, 'AI Kwaliteit',
                fontsize=60, fontweight='bold', ha='center',
                color=self.colors['highlight'])

        ax.text(50, 62, 'Praktische Inzichten voor BiSL',
                fontsize=30, ha='center',
                color=self.colors['text'], alpha=0.8)

        # Context box
        context_box = FancyBboxPatch(
            (15, 35), 70, 20,
            boxstyle="round,pad=1.2",
            facecolor=self.colors['bg_light'],
            edgecolor=self.colors['accent'],
            linewidth=3,
            alpha=0.95
        )
        ax.add_patch(context_box)

        ax.text(50, 50, 'Je kent nu de techniek:',
                fontsize=24, ha='center', va='center',
                color=self.colors['secondary'], fontweight='bold')

        ax.text(50, 45, 'Vectors • Neural Networks • RAG • Finetuning',
                fontsize=21, ha='center', va='center',
                color=self.colors['text'], alpha=0.9)

        ax.text(50, 40, 'Nu de praktijk: Welke vragen stel je?',
                fontsize=24, ha='center', va='center',
                color=self.colors['highlight'], fontweight='bold')

        # Bottom instruction
        ax.text(50, 18, '6 stappen • 6 minuten • Praktische inzichten',
                fontsize=21, ha='center', va='center',
                color=self.colors['dim'], style='italic')

        ax.text(50, 8, 'SPATIE = Volgende stap',
                fontsize=18, ha='center', va='center',
                color=self.colors['text'], alpha=0.7)

        self.add_status_indicator(progress < 1.0)
        plt.tight_layout()

    def draw_three_choices(self, progress: float):
        """Step 1: The three AI approaches - visual and simple"""
        self.fig.clear()
        ax = self.fig.add_subplot(111)
        ax.axis('off')
        ax.set_xlim(0, 100)
        ax.set_ylim(0, 100)

        # Title
        alpha = min(1.0, progress * 2)
        ax.text(50, 95, 'Stap 1: De Drie Keuzes',
                fontsize=48, fontweight='bold', ha='center',
                color=self.colors['highlight'], alpha=alpha)

        ax.text(50, 89, 'Welke AI-aanpak past bij jouw situatie?',
                fontsize=27, ha='center',
                color=self.colors['text'], alpha=alpha * 0.7, style='italic')

        # Three scenarios in a row
        scenarios = [
            {
                'name': 'RAG',
                'icon': '[<>]',
                'color': self.colors['primary'],
                'x': 17,
                'when': 'Kennis verandert vaak',
                'example': 'Procedures, documentatie',
                'delay': 0.2
            },
            {
                'name': 'Finetuning',
                'icon': '[>>]',
                'color': self.colors['secondary'],
                'x': 50,
                'when': 'Specifieke stijl/taal',
                'example': 'BiSL terminologie',
                'delay': 0.35
            },
            {
                'name': 'Hybrid',
                'icon': '[*]',
                'color': self.colors['purple'],
                'x': 83,
                'when': 'Beide nodig',
                'example': 'Complex domein',
                'delay': 0.5
            }
        ]

        for scenario in scenarios:
            if progress > scenario['delay']:
                box_alpha = min(1.0, (progress - scenario['delay']) / 0.15)

                # Main box
                box = FancyBboxPatch(
                    (scenario['x'] - 12, 60), 24, 22,
                    boxstyle="round,pad=1",
                    facecolor=self.colors['bg_light'],
                    edgecolor=scenario['color'],
                    linewidth=4,
                    alpha=box_alpha * 0.95
                )
                ax.add_patch(box)

                # Icon & name
                ax.text(scenario['x'], 77, scenario['icon'],
                        fontsize=36, ha='center', va='center',
                        color=scenario['color'],
                        fontweight='bold', alpha=box_alpha)

                ax.text(scenario['x'], 71, scenario['name'],
                        fontsize=24, ha='center', va='center',
                        color=scenario['color'],
                        fontweight='bold', alpha=box_alpha)

                # When to use
                ax.text(scenario['x'], 66, 'Wanneer?',
                        fontsize=16, ha='center', va='center',
                        color=self.colors['text'],
                        fontweight='bold', alpha=box_alpha * 0.9)

                ax.text(scenario['x'], 62, scenario['when'],
                        fontsize=15, ha='center', va='center',
                        color=self.colors['text'], alpha=box_alpha * 0.8)

        # Bottom insight
        if progress > 0.7:
            insight_alpha = min(1.0, (progress - 0.7) / 0.2)

            insight_box = FancyBboxPatch(
                (10, 35), 80, 16,
                boxstyle="round,pad=1",
                facecolor=self.colors['bg_light'],
                edgecolor=self.colors['accent'],
                linewidth=3,
                alpha=insight_alpha * 0.9
            )
            ax.add_patch(insight_box)

            ax.text(50, 46, '[!] De keuze bepaalt de kwaliteitsvragen',
                    fontsize=24, ha='center', va='center',
                    color=self.colors['accent'],
                    fontweight='bold', alpha=insight_alpha)

            ax.text(50, 40, 'RAG → Bronkwaliteit & Actualiteit',
                    fontsize=18, ha='center', va='center',
                    color=self.colors['primary'], alpha=insight_alpha * 0.9)

            ax.text(50, 37, 'Finetuning → Trainingsdata & Bias',
                    fontsize=18, ha='center', va='center',
                    color=self.colors['secondary'], alpha=insight_alpha * 0.9)

            ax.text(50, 34, 'Hybrid → Beide + Complexiteit',
                    fontsize=18, ha='center', va='center',
                    color=self.colors['purple'], alpha=insight_alpha * 0.9)

        # Key question at bottom
        if progress > 0.85:
            question_alpha = min(1.0, (progress - 0.85) / 0.15)
            ax.text(50, 18, '[?] Belangrijkste vraag voor élke keuze...',
                    fontsize=24, ha='center', va='center',
                    color=self.colors['highlight'],
                    fontweight='bold', alpha=question_alpha)

            ax.text(50, 13, 'Wie moet je betrekken?',
                    fontsize=27, ha='center', va='center',
                    color=self.colors['text'], alpha=question_alpha * 0.9,
                    style='italic')

        self.add_status_indicator(progress < 1.0)
        plt.tight_layout()

    def draw_when_embeddings(self, progress: float):
        """Step 2.5: When do you need embeddings/semantic search?"""
        self.fig.clear()
        ax = self.fig.add_subplot(111)
        ax.axis('off')
        ax.set_xlim(0, 100)
        ax.set_ylim(0, 100)

        # Title
        ax.text(50, 96, 'Wanneer Heb Je Embeddings Nodig?',
                fontsize=45, fontweight='bold', ha='center', va='top',
                color=self.colors['highlight'])

        ax.text(50, 90, 'Decision-making voor semantisch zoeken',
                fontsize=22, ha='center', va='top',
                color=self.colors['text'], alpha=0.7, style='italic')

        # YES section - when to use embeddings
        if progress > 0.15:
            yes_alpha = min(1.0, (progress - 0.15) / 0.3)

            yes_box = FancyBboxPatch(
                (8, 55), 40, 28,
                boxstyle="round,pad=1.2",
                facecolor=self.colors['bg_light'],
                edgecolor=self.colors['secondary'],
                linewidth=4,
                alpha=0.95 * yes_alpha
            )
            ax.add_patch(yes_box)

            ax.text(28, 80, '✓ JA - Gebruik Embeddings:',
                    fontsize=22, ha='center', va='center',
                    color=self.colors['secondary'], fontweight='bold',
                    alpha=yes_alpha)

            # Use cases
            yes_items = [
                '• Grote kennisbank (100+ docs)',
                '• Synoniemen belangrijk',
                '  "RFC" = "Request for Change"',
                '• Natuurlijke taalvragen',
                '• Conceptueel zoeken',
                '  "problemen" → "issues"'
            ]

            y_start = 72
            for i, item in enumerate(yes_items):
                ax.text(11, y_start - i * 4.5, item,
                        fontsize=15, ha='left', va='center',
                        color=self.colors['text'], alpha=yes_alpha * 0.95)

        # NO section - when NOT to use embeddings
        if progress > 0.48:
            no_alpha = min(1.0, (progress - 0.48) / 0.3)

            no_box = FancyBboxPatch(
                (52, 55), 40, 28,
                boxstyle="round,pad=1.2",
                facecolor=self.colors['bg_light'],
                edgecolor=self.colors['error'],
                linewidth=4,
                alpha=0.95 * no_alpha
            )
            ax.add_patch(no_box)

            ax.text(72, 80, '✗ NEE - Simpeler oplossing:',
                    fontsize=22, ha='center', va='center',
                    color=self.colors['error'], fontweight='bold',
                    alpha=no_alpha)

            # Alternative solutions
            no_items = [
                '• Exact zoeken (product IDs)',
                '  → Database',
                '• Kleine dataset (<20 docs)',
                '  → Keyword search',
                '• Geen budget voor API calls',
                '  → Lokale alternatieven',
                '• Real-time critical (<50ms)',
                '  → Cache + keywords'
            ]

            y_start = 72
            for i, item in enumerate(no_items):
                ax.text(55, y_start - i * 3.3, item,
                        fontsize=14, ha='left', va='center',
                        color=self.colors['text'], alpha=no_alpha * 0.95)

        # Example scenario
        if progress > 0.78:
            example_alpha = min(1.0, (progress - 0.78) / 0.2)

            example_box = FancyBboxPatch(
                (10, 28), 80, 22,
                boxstyle="round,pad=1",
                facecolor=self.colors['bg_light'],
                edgecolor=self.colors['cyan'],
                linewidth=3,
                alpha=0.95 * example_alpha
            )
            ax.add_patch(example_box)

            ax.text(50, 46, 'Praktisch Voorbeeld: BiSL Kennisbank',
                    fontsize=21, ha='center', va='center',
                    color=self.colors['cyan'], fontweight='bold',
                    alpha=example_alpha)

            # Scenario
            ax.text(13, 40, 'Vraag:', fontsize=17, ha='left', va='center',
                    color=self.colors['text'], fontweight='bold', alpha=example_alpha)
            ax.text(26, 40, '"Wat is een RFC in BiSL?"',
                    fontsize=16, ha='left', va='center',
                    color=self.colors['text'], alpha=example_alpha, style='italic')

            ax.text(13, 35.5, '✗ Keywords:', fontsize=15, ha='left', va='center',
                    color=self.colors['error'], alpha=example_alpha)
            ax.text(30, 35.5, 'Vindt alleen exact "RFC"',
                    fontsize=14, ha='left', va='center',
                    color=self.colors['text'], alpha=example_alpha * 0.8)

            ax.text(13, 31, '✓ Embeddings:', fontsize=15, ha='left', va='center',
                    color=self.colors['secondary'], alpha=example_alpha)
            ax.text(32, 31, 'Vindt ook "Request for Change", "wijzigingsaanvraag", RFC uitleg',
                    fontsize=14, ha='left', va='center',
                    color=self.colors['text'], alpha=example_alpha * 0.8)

        # Bottom tip
        if progress > 0.9:
            tip_alpha = min(1.0, (progress - 0.9) / 0.1)

            tip_box = FancyBboxPatch(
                (15, 8), 70, 15,
                boxstyle="round,pad=1",
                facecolor=self.colors['bg_light'],
                edgecolor=self.colors['accent'],
                linewidth=3,
                alpha=0.95 * tip_alpha
            )
            ax.add_patch(tip_box)

            ax.text(50, 18, '💡 Praktische Beslisregel:',
                    fontsize=21, ha='center', va='center',
                    color=self.colors['accent'], fontweight='bold',
                    alpha=tip_alpha)

            ax.text(50, 12, 'Start met keyword search → upgrade naar embeddings als synoniemen/schaal probleem worden',
                    fontsize=15, ha='center', va='center',
                    color=self.colors['text'], alpha=tip_alpha * 0.9)

        self.add_status_indicator(progress < 1.0)

    def draw_cloud_vs_local(self, progress: float):
        """Step 2: Cloud vs Local models - Infrastructure choice"""
        self.fig.clear()
        ax = self.fig.add_subplot(111)
        ax.axis('off')
        ax.set_xlim(0, 100)
        ax.set_ylim(0, 100)

        # Title
        alpha = min(1.0, progress * 2)
        ax.text(50, 95, 'Stap 2: Cloud of Lokaal?',
                fontsize=48, fontweight='bold', ha='center',
                color=self.colors['purple'], alpha=alpha)

        ax.text(50, 89, 'Waar draait je AI-model? De keuze heeft grote gevolgen',
                fontsize=27, ha='center',
                color=self.colors['text'], alpha=alpha * 0.7, style='italic')

        # Two main options side by side
        # CLOUD (left)
        if progress > 0.15:
            cloud_alpha = min(1.0, (progress - 0.15) / 0.2)

            cloud_box = FancyBboxPatch(
                (8, 50), 38, 32,
                boxstyle="round,pad=1.2",
                facecolor=self.colors['bg_light'],
                edgecolor=self.colors['primary'],
                linewidth=4,
                alpha=cloud_alpha * 0.95
            )
            ax.add_patch(cloud_box)

            # Cloud icon & title
            ax.text(27, 78, '[CLOUD]',
                    fontsize=36, ha='center', va='center',
                    color=self.colors['primary'],
                    fontweight='bold', alpha=cloud_alpha)

            ax.text(27, 72, 'Cloud Models',
                    fontsize=27, ha='center', va='center',
                    color=self.colors['primary'],
                    fontweight='bold', alpha=cloud_alpha)

            # Examples
            ax.text(27, 67, 'Voorbeelden:',
                    fontsize=16, ha='center', va='center',
                    color=self.colors['text'],
                    fontweight='bold', alpha=cloud_alpha * 0.9)

            ax.text(27, 63, 'Azure OpenAI\nGoogle Vertex AI\nAWS Bedrock',
                    fontsize=15, ha='center', va='center',
                    color=self.colors['text'],
                    alpha=cloud_alpha * 0.8)

            # Pros
            ax.text(27, 56, '[+] Voordelen:',
                    fontsize=15, ha='center', va='center',
                    color=self.colors['secondary'],
                    fontweight='bold', alpha=cloud_alpha * 0.9)

            ax.text(27, 52.5, '• Snel starten\n• Altijd up-to-date\n• Schaalbaar',
                    fontsize=13, ha='center', va='center',
                    color=self.colors['text'],
                    alpha=cloud_alpha * 0.8)

        # LOCAL (right)
        if progress > 0.3:
            local_alpha = min(1.0, (progress - 0.3) / 0.2)

            local_box = FancyBboxPatch(
                (54, 50), 38, 32,
                boxstyle="round,pad=1.2",
                facecolor=self.colors['bg_light'],
                edgecolor=self.colors['accent'],
                linewidth=4,
                alpha=local_alpha * 0.95
            )
            ax.add_patch(local_box)

            # Local icon & title
            ax.text(73, 78, '[LOCAL]',
                    fontsize=36, ha='center', va='center',
                    color=self.colors['accent'],
                    fontweight='bold', alpha=local_alpha)

            ax.text(73, 72, 'Lokale Models',
                    fontsize=27, ha='center', va='center',
                    color=self.colors['accent'],
                    fontweight='bold', alpha=local_alpha)

            # Examples
            ax.text(73, 67, 'Voorbeelden:',
                    fontsize=16, ha='center', va='center',
                    color=self.colors['text'],
                    fontweight='bold', alpha=local_alpha * 0.9)

            ax.text(73, 63, 'LLaMA 3\nMistral\nPhi-3',
                    fontsize=15, ha='center', va='center',
                    color=self.colors['text'],
                    alpha=local_alpha * 0.8)

            # Pros
            ax.text(73, 56, '[+] Voordelen:',
                    fontsize=15, ha='center', va='center',
                    color=self.colors['secondary'],
                    fontweight='bold', alpha=local_alpha * 0.9)

            ax.text(73, 52.5, '• Data blijft intern\n• Geen API kosten\n• Volledige controle',
                    fontsize=13, ha='center', va='center',
                    color=self.colors['text'],
                    alpha=local_alpha * 0.8)

        # Key questions at bottom
        if progress > 0.55:
            questions_alpha = min(1.0, (progress - 0.55) / 0.2)

            questions_box = FancyBboxPatch(
                (10, 20), 80, 23,
                boxstyle="round,pad=1",
                facecolor=self.colors['bg_light'],
                edgecolor=self.colors['warning'],
                linewidth=3,
                alpha=questions_alpha * 0.9
            )
            ax.add_patch(questions_box)

            ax.text(50, 39, '[?] Belangrijke Vragen',
                    fontsize=24, ha='center', va='center',
                    color=self.colors['warning'],
                    fontweight='bold', alpha=questions_alpha)

            # Questions grid
            questions_left = [
                '• Mag data naar buiten (AVG)?',
                '• Wat zijn de kosten per request?',
                '• Wie beheert de infrastructuur?'
            ]

            questions_right = [
                '• Hoe gevoelig is de data?',
                '• Hebben we de expertise in-house?',
                '• Wat bij vendor lock-in?'
            ]

            y_pos = 33
            for q in questions_left:
                ax.text(15, y_pos, q,
                        fontsize=15, ha='left', va='center',
                        color=self.colors['text'],
                        alpha=questions_alpha * 0.9)
                y_pos -= 4

            y_pos = 33
            for q in questions_right:
                ax.text(52, y_pos, q,
                        fontsize=15, ha='left', va='center',
                        color=self.colors['text'],
                        alpha=questions_alpha * 0.9)
                y_pos -= 4

        # Bottom insight
        if progress > 0.8:
            insight_alpha = min(1.0, (progress - 0.8) / 0.2)

            ax.text(50, 12, '[!] Vaak is een HYBRIDE oplossing het beste',
                    fontsize=24, ha='center', va='center',
                    color=self.colors['highlight'],
                    fontweight='bold', alpha=insight_alpha)

            ax.text(50, 8, 'Prototype in cloud, productie lokaal • Of: niet-gevoelig → cloud, gevoelig → lokaal',
                    fontsize=16, ha='center', va='center',
                    color=self.colors['text'],
                    alpha=insight_alpha * 0.8, style='italic')

        self.add_status_indicator(progress < 1.0)
        plt.tight_layout()

    def draw_stakeholder_web(self, progress: float):
        """Step 3: The stakeholder web - WHO do you involve?"""
        self.fig.clear()
        ax = self.fig.add_subplot(111)
        ax.axis('off')
        ax.set_xlim(0, 100)
        ax.set_ylim(0, 100)

        # Title
        ax.text(50, 96, 'Stap 3: De Belangrijkste Vraag',
                fontsize=48, fontweight='bold', ha='center',
                color=self.colors['secondary'])

        ax.text(50, 90, 'WIE moet je betrekken bij AI-kwaliteit?',
                fontsize=27, ha='center',
                color=self.colors['text'], alpha=0.7, style='italic')

        # Center: AI Quality
        if progress > 0.1:
            center_alpha = min(1.0, (progress - 0.1) / 0.15)
            center_circle = Circle((50, 55), 6,
                                   facecolor=self.colors['highlight'],
                                   edgecolor='white',
                                   linewidth=4,
                                   alpha=center_alpha)
            ax.add_patch(center_circle)

            ax.text(50, 55, 'AI\nKwaliteit',
                    fontsize=16, ha='center', va='center',
                    color='white', fontweight='bold',
                    alpha=center_alpha)

        # Stakeholders around the center
        stakeholders = [
            {'name': 'Informatie-\nmanagement', 'angle': 0, 'color': self.colors['primary'], 'delay': 0.25},
            {'name': 'Data-\ngovernance', 'angle': 45, 'color': self.colors['secondary'], 'delay': 0.3},
            {'name': 'Privacy &\nSecurity', 'angle': 90, 'color': self.colors['accent'], 'delay': 0.35},
            {'name': 'Business\nOwners', 'angle': 135, 'color': self.colors['purple'], 'delay': 0.4},
            {'name': 'ICT /\nDevelopment', 'angle': 180, 'color': self.colors['cyan'], 'delay': 0.45},
            {'name': 'Compliance\n& Audit', 'angle': 225, 'color': self.colors['warning'], 'delay': 0.5},
            {'name': 'Gebruikers\n& Experts', 'angle': 270, 'color': self.colors['primary'], 'delay': 0.55},
            {'name': 'Architectuur', 'angle': 315, 'color': self.colors['secondary'], 'delay': 0.6}
        ]

        for stakeholder in stakeholders:
            if progress > stakeholder['delay']:
                sh_alpha = min(1.0, (progress - stakeholder['delay']) / 0.1)

                # Calculate position
                angle_rad = np.radians(stakeholder['angle'])
                radius = 28
                x = 50 + radius * np.cos(angle_rad)
                y = 55 + radius * np.sin(angle_rad)

                # Connection line
                line_start_x = 50 + 6 * np.cos(angle_rad)
                line_start_y = 55 + 6 * np.sin(angle_rad)
                ax.plot([line_start_x, x], [line_start_y, y],
                        color=stakeholder['color'],
                        linewidth=2, alpha=sh_alpha * 0.5,
                        linestyle='--', zorder=1)

                # Stakeholder circle
                sh_circle = Circle((x, y), 3.5,
                                   facecolor=stakeholder['color'],
                                   edgecolor='white',
                                   linewidth=2,
                                   alpha=sh_alpha * 0.9,
                                   zorder=2)
                ax.add_patch(sh_circle)

                # Label
                ax.text(x, y - 6, stakeholder['name'],
                        fontsize=13, ha='center', va='center',
                        color=self.colors['text'],
                        alpha=sh_alpha * 0.9)

        # Bottom insight
        if progress > 0.75:
            insight_alpha = min(1.0, (progress - 0.75) / 0.2)

            insight_box = FancyBboxPatch(
                (10, 8), 80, 14,
                boxstyle="round,pad=1",
                facecolor=self.colors['bg_light'],
                edgecolor=self.colors['highlight'],
                linewidth=3,
                alpha=insight_alpha * 0.9
            )
            ax.add_patch(insight_box)

            ax.text(50, 18, '[!] Kwaliteit is GEEN solo-opdracht',
                    fontsize=24, ha='center', va='center',
                    color=self.colors['highlight'],
                    fontweight='bold', alpha=insight_alpha)

            ax.text(50, 13, 'Elk van deze partijen heeft eigen vragen en verantwoordelijkheden',
                    fontsize=18, ha='center', va='center',
                    color=self.colors['text'], alpha=insight_alpha * 0.8)

            ax.text(50, 10, 'Als BiSL adviseur ben jij de spin in het web!',
                    fontsize=18, ha='center', va='center',
                    color=self.colors['accent'],
                    fontweight='bold', alpha=insight_alpha * 0.9)

        self.add_status_indicator(progress < 1.0)
        plt.tight_layout()

    def draw_iceberg(self, progress: float):
        """Step 3: Iceberg - what you see vs what you need to think about"""
        self.fig.clear()
        ax = self.fig.add_subplot(111)
        ax.axis('off')
        ax.set_xlim(0, 100)
        ax.set_ylim(0, 100)

        # Title
        ax.text(50, 96, 'Stap 4: Topje van de IJsberg',
                fontsize=48, fontweight='bold', ha='center',
                color=self.colors['accent'])

        ax.text(50, 90, 'Wat je ziet is maar een klein deel van het verhaal',
                fontsize=27, ha='center',
                color=self.colors['text'], alpha=0.7, style='italic')

        # Water line
        if progress > 0.1:
            water_alpha = min(1.0, (progress - 0.1) / 0.15)
            ax.plot([10, 90], [55, 55], color=self.colors['cyan'],
                    linewidth=3, alpha=water_alpha * 0.8,
                    linestyle='--')

            ax.text(12, 57, 'Zichtbaar',
                    fontsize=18, ha='left', va='bottom',
                    color=self.colors['text'], alpha=water_alpha * 0.7,
                    style='italic')

            ax.text(12, 53, 'Onzichtbaar',
                    fontsize=18, ha='left', va='top',
                    color=self.colors['text'], alpha=water_alpha * 0.7,
                    style='italic')

        # Above water (visible) - The TIP
        if progress > 0.25:
            tip_alpha = min(1.0, (progress - 0.25) / 0.15)

            # Small triangle above water
            tip_points = np.array([[50, 80], [40, 55], [60, 55]])
            tip_triangle = plt.Polygon(tip_points,
                                       facecolor=self.colors['secondary'],
                                       edgecolor='white',
                                       linewidth=3,
                                       alpha=tip_alpha * 0.9)
            ax.add_patch(tip_triangle)

            # What you see
            visible_items = [
                '[OK] AI geeft antwoorden',
                '[OK] Snel resultaat',
                '[OK] Lijkt te werken'
            ]

            for i, item in enumerate(visible_items):
                if progress > 0.25 + i * 0.05:
                    item_alpha = min(1.0, (progress - (0.25 + i * 0.05)) / 0.1)
                    ax.text(70, 75 - i * 5, item,
                            fontsize=16, ha='left', va='center',
                            color=self.colors['text'],
                            alpha=item_alpha * 0.9)

        # Below water (invisible) - The BULK
        if progress > 0.5:
            bulk_alpha = min(1.0, (progress - 0.5) / 0.2)

            # Large triangle below water
            bulk_points = np.array([[50, 55], [40, 55], [20, 10], [80, 10], [60, 55]])
            bulk_triangle = plt.Polygon(bulk_points,
                                        facecolor=self.colors['cyan'],
                                        edgecolor='white',
                                        linewidth=3,
                                        alpha=bulk_alpha * 0.7)
            ax.add_patch(bulk_triangle)

            # What you need to think about
            hidden_items = [
                '[?] Wie is eigenaar van data?',
                '[?] Hoe actueel is de bron?',
                '[?] Wie controleert output?',
                '[?] Wat als het fout gaat?',
                '[?] Privacy & AVG compliance?',
                '[?] Bias in trainingsdata?',
                '[?] Wie documenteert beslissingen?',
                '[?] Hoe monitoren we kwaliteit?'
            ]

            for i, item in enumerate(hidden_items):
                if progress > 0.55 + i * 0.04:
                    item_alpha = min(1.0, (progress - (0.55 + i * 0.04)) / 0.05)
                    y_pos = 50 - i * 4.5
                    # Alternate left and right
                    if i % 2 == 0:
                        ax.text(30, y_pos, item,
                                fontsize=14, ha='left', va='center',
                                color=self.colors['text'],
                                alpha=item_alpha * 0.9)
                    else:
                        ax.text(70, y_pos, item,
                                fontsize=14, ha='right', va='center',
                                color=self.colors['text'],
                                alpha=item_alpha * 0.9)

        self.add_status_indicator(progress < 1.0)
        plt.tight_layout()



def main():
    """Main presentation runner"""
    print("\n" + "="*60)
    print("🎯 AI Quality Presentation - Redesigned")
    print("="*60)
    print("\nSteps:")
    print("  1. Landing - Intro")
    print("  2. De Drie Keuzes - RAG/Finetuning/Hybrid")
    print("  3. Wanneer Heb Je Embeddings Nodig?")
    print("  4. Cloud of Lokaal? - Infrastructure choice")
    print("  5. De Belangrijkste Vraag - Stakeholder Web")
    print("  6. Topje van de IJsberg - Visible vs Hidden")
    print("\n[Keys]  SPACE=Next | B=Previous | R=Reset | Q=Quit")
    print("="*60 + "\n")

    presentation = QualityPresentation()
    presentation.run()


if __name__ == "__main__":
    main()
