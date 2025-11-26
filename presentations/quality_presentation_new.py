"""
AI Quality Presentation - Professional Perspective
Van technische concepten naar strategische vraagstelling

Stappen:
1. Landing - Context
2. Van Techniek naar Betekenis
3. Waar Kwaliteit Bepaald Wordt  
4. De Onzichtbare Laag
5. Welke Vragen Stel Je Nu?
6. Kwaliteitsstandaarden

~6-8 minutes, perspectief-verbredend
"""

from core.base_presentation import BasePresentation
from core.styling import PresentationStyle
from matplotlib.patches import FancyBboxPatch, Circle, FancyArrowPatch, Rectangle, Wedge, Polygon
import matplotlib.pyplot as plt
import numpy as np


class QualityPresentation (BasePresentation):
    """
    AI Quality - Professional Perspective
    Van technische kennis naar strategische vraagstelling
    """

    def __init__(self):
        """Initialize the presentation"""
        step_names = [
            'Landing',
            'Van Techniek naar Betekenis',
            'Waar Kwaliteit Bepaald Wordt',
            'De Onzichtbare Laag',
            'Welke Vragen Stel Je Nu?',
            'Kwaliteitsstandaarden'
        ]

        super().__init__("AI Kwaliteit: Professional Perspective", step_names)

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
            self.draw_tech_to_meaning(progress)
        elif step == 2:
            self.draw_quality_control_points(progress)
        elif step == 3:
            self.draw_invisible_layer(progress)
        elif step == 4:
            self.draw_new_questions(progress)
        elif step == 5:
            self.draw_quality_standards(progress)

    def draw_landing(self, progress: float):
        """Landing page - context setting"""
        self.fig.clear()
        ax = self.fig.add_subplot(111)
        ax.axis('off')
        ax.set_xlim(0, 100)
        ax.set_ylim(0, 100)

        # Title
        ax.text(50, 75, 'AI Kwaliteit',
                fontsize=65, fontweight='bold', ha='center',
                color=self.colors['highlight'])

        ax.text(50, 66, 'Van Techniek naar Vraagstelling',
                fontsize=32, ha='center',
                color=self.colors['text'], alpha=0.85)

        # Context box
        context_box = FancyBboxPatch(
            (12, 38), 76, 20,
            boxstyle="round,pad=1.2",
            facecolor=self.colors['bg_light'],
            edgecolor=self.colors['accent'],
            linewidth=3,
            alpha=0.95
        )
        ax.add_patch(context_box)

        ax.text(50, 53, 'Je kent de techniek:',
                fontsize=24, ha='center', va='center',
                color=self.colors['secondary'], fontweight='bold')

        ax.text(50, 47, 'Vectors • Embeddings • RAG • Finetuning • Neural Networks',
                fontsize=20, ha='center', va='center',
                color=self.colors['text'], alpha=0.9)

        ax.text(50, 42, 'Maar wat betekent dit voor kwaliteit in de praktijk?',
                fontsize=24, ha='center', va='center',
                color=self.colors['highlight'], fontweight='bold')

        # Bottom
        ax.text(50, 22, 'Niet: "Hoe passen we dit toe?"',
                fontsize=21, ha='center', va='center',
                color=self.colors['dim'], style='italic')
        
        ax.text(50, 17, 'Maar: "Welke vragen moeten we stellen?"',
                fontsize=23, ha='center', va='center',
                color=self.colors['accent'], fontweight='bold')

        ax.text(50, 8, 'SPATIE = Volgende',
                fontsize=18, ha='center', va='center',
                color=self.colors['text'], alpha=0.6)

        self.add_status_indicator(progress < 1.0)
        plt.tight_layout()

    def draw_tech_to_meaning(self, progress: float):
        """Step 1: Van techniek naar betekenis"""
        self.fig.clear()
        ax = self.fig.add_subplot(111)
        ax.axis('off')
        ax.set_xlim(0, 100)
        ax.set_ylim(0, 100)

        # Title
        alpha = min(1.0, progress * 2)
        ax.text(50, 95, 'Wat Doen Die Technieken Eigenlijk?',
                fontsize=44, fontweight='bold', ha='center',
                color=self.colors['highlight'], alpha=alpha)

        ax.text(50, 89, 'Van technische term naar betekenis voor informatiestromen',
                fontsize=24, ha='center',
                color=self.colors['text'], alpha=alpha * 0.7, style='italic')

        # Three technique translations
        translations = [
            {
                'tech': 'Embeddings',
                'arrow': '→',
                'meaning': 'Betekenis Vastleggen',
                'detail': 'Hoe leg je vast wat een\ndocument "betekent"?',
                'y': 72,
                'color': self.colors['primary'],
                'delay': 0.2
            },
            {
                'tech': 'RAG',
                'arrow': '→',
                'meaning': 'Context Toevoegen',
                'detail': 'Welke informatie heeft het\nnodig om te antwoorden?',
                'y': 53,
                'color': self.colors['secondary'],
                'delay': 0.35
            },
            {
                'tech': 'Finetuning',
                'arrow': '→',
                'meaning': 'Gedrag Aanpassen',
                'detail': 'Hoe schrijft/redeneert het\nmodel standaard?',
                'y': 34,
                'color': self.colors['purple'],
                'delay': 0.5
            }
        ]

        for trans in translations:
            if progress > trans['delay']:
                t_alpha = min(1.0, (progress - trans['delay']) / 0.15)

                # Tech term (left)
                tech_box = FancyBboxPatch(
                    (8, trans['y'] - 4), 22, 10,
                    boxstyle="round,pad=0.8",
                    facecolor=self.colors['bg_light'],
                    edgecolor=trans['color'],
                    linewidth=3,
                    alpha=t_alpha * 0.9
                )
                ax.add_patch(tech_box)

                ax.text(19, trans['y'] + 1, trans['tech'],
                        fontsize=22, ha='center', va='center',
                        color=trans['color'],
                        fontweight='bold', alpha=t_alpha)

                # Arrow
                arrow = FancyArrowPatch(
                    (32, trans['y'] + 1), (46, trans['y'] + 1),
                    arrowstyle='->', mutation_scale=30,
                    linewidth=3, color=trans['color'],
                    alpha=t_alpha * 0.7
                )
                ax.add_artist(arrow)

                # Meaning (center-right)
                meaning_box = FancyBboxPatch(
                    (48, trans['y'] - 4), 26, 10,
                    boxstyle="round,pad=0.8",
                    facecolor=trans['color'],
                    edgecolor='white',
                    linewidth=2,
                    alpha=t_alpha * 0.85
                )
                ax.add_patch(meaning_box)

                ax.text(61, trans['y'] + 1, trans['meaning'],
                        fontsize=20, ha='center', va='center',
                        color='white',
                        fontweight='bold', alpha=t_alpha)

                # Detail (right)
                ax.text(82, trans['y'] + 1, trans['detail'],
                        fontsize=15, ha='left', va='center',
                        color=self.colors['text'],
                        alpha=t_alpha * 0.85)

        # Bottom insight
        if progress > 0.7:
            insight_alpha = min(1.0, (progress - 0.7) / 0.25)

            insight_box = FancyBboxPatch(
                (10, 10), 80, 16,
                boxstyle="round,pad=1",
                facecolor=self.colors['bg_light'],
                edgecolor=self.colors['highlight'],
                linewidth=3,
                alpha=insight_alpha * 0.9
            )
            ax.add_patch(insight_box)

            ax.text(50, 21, 'Inzicht:',
                    fontsize=20, ha='center', va='center',
                    color=self.colors['highlight'],
                    fontweight='bold', alpha=insight_alpha)

            ax.text(50, 16, 'Elke techniek bepaalt waar kwaliteit geborgd wordt',
                    fontsize=19, ha='center', va='center',
                    color=self.colors['text'], alpha=insight_alpha * 0.9)

            ax.text(50, 12, 'Embeddings = in de data • RAG = in de selectie • Finetuning = in het model',
                    fontsize=16, ha='center', va='center',
                    color=self.colors['dim'], alpha=insight_alpha * 0.8,
                    style='italic')

        self.add_status_indicator(progress < 1.0)
        plt.tight_layout()

    def draw_quality_control_points(self, progress: float):
        """Step 2: Waar kwaliteit bepaald wordt"""
        self.fig.clear()
        ax = self.fig.add_subplot(111)
        ax.axis('off')
        ax.set_xlim(0, 100)
        ax.set_ylim(0, 100)

        # Title
        ax.text(50, 95, 'Waar Wordt Kwaliteit Bepaald?',
                fontsize=48, fontweight='bold', ha='center',
                color=self.colors['accent'])

        ax.text(50, 89, 'Verschillende technieken = verschillende controlepunten',
                fontsize=24, ha='center',
                color=self.colors['text'], alpha=0.7, style='italic')

        # Three scenarios with control points
        scenarios = [
            {
                'name': 'RAG-systeem',
                'control_points': [
                    'Documentkwaliteit',
                    'Chunking-strategie',
                    'Zoek-relevantie',
                    'Context-selectie'
                ],
                'x': 18,
                'color': self.colors['primary'],
                'delay': 0.15
            },
            {
                'name': 'Finetuned Model',
                'control_points': [
                    'Trainingsdata',
                    'Voorbeelden',
                    'Evaluatie-metrics',
                    'Model-gedrag'
                ],
                'x': 50,
                'color': self.colors['secondary'],
                'delay': 0.35
            },
            {
                'name': 'Hybrid Aanpak',
                'control_points': [
                    'Alles hierboven',
                    '+ Interactie',
                    '+ Orchestratie',
                    '+ Fallbacks'
                ],
                'x': 82,
                'color': self.colors['purple'],
                'delay': 0.55
            }
        ]

        for scenario in scenarios:
            if progress > scenario['delay']:
                s_alpha = min(1.0, (progress - scenario['delay']) / 0.15)

                # Scenario name box
                name_box = FancyBboxPatch(
                    (scenario['x'] - 12, 73), 24, 7,
                    boxstyle="round,pad=0.7",
                    facecolor=scenario['color'],
                    edgecolor='white',
                    linewidth=2,
                    alpha=s_alpha * 0.9
                )
                ax.add_patch(name_box)

                ax.text(scenario['x'], 76.5, scenario['name'],
                        fontsize=19, ha='center', va='center',
                        color='white',
                        fontweight='bold', alpha=s_alpha)

                # Control points list
                for i, cp in enumerate(scenario['control_points']):
                    if progress > scenario['delay'] + 0.05 + i * 0.03:
                        cp_alpha = min(1.0, (progress - (scenario['delay'] + 0.05 + i * 0.03)) / 0.05)
                        
                        y_pos = 65 - i * 5.5

                        # Control point box
                        cp_box = FancyBboxPatch(
                            (scenario['x'] - 11, y_pos - 2), 22, 4,
                            boxstyle="round,pad=0.5",
                            facecolor=self.colors['bg_light'],
                            edgecolor=scenario['color'],
                            linewidth=2,
                            alpha=cp_alpha * 0.85
                        )
                        ax.add_patch(cp_box)

                        ax.text(scenario['x'], y_pos, cp,
                                fontsize=14, ha='center', va='center',
                                color=self.colors['text'],
                                alpha=cp_alpha * 0.9)

        # Bottom insight
        if progress > 0.75:
            insight_alpha = min(1.0, (progress - 0.75) / 0.2)

            insight_box = FancyBboxPatch(
                (8, 18), 84, 20,
                boxstyle="round,pad=1",
                facecolor=self.colors['bg_light'],
                edgecolor=self.colors['highlight'],
                linewidth=3,
                alpha=insight_alpha * 0.9
            )
            ax.add_patch(insight_box)

            ax.text(50, 32, 'Cruciaal Inzicht:',
                    fontsize=22, ha='center', va='center',
                    color=self.colors['highlight'],
                    fontweight='bold', alpha=insight_alpha)

            ax.text(50, 27, 'Bij traditionele systemen: kwaliteit in één proces',
                    fontsize=18, ha='center', va='center',
                    color=self.colors['text'], alpha=insight_alpha * 0.8)

            ax.text(50, 23, 'Bij AI-systemen: kwaliteit verspreid over meerdere lagen',
                    fontsize=18, ha='center', va='center',
                    color=self.colors['accent'],
                    fontweight='bold', alpha=insight_alpha * 0.9)

            ax.text(50, 19, 'Vraag dus niet "Is het goed?", maar "Waar borgen we wat?"',
                    fontsize=17, ha='center', va='center',
                    color=self.colors['dim'], alpha=insight_alpha * 0.8,
                    style='italic')

        self.add_status_indicator(progress < 1.0)
        plt.tight_layout()

    def draw_invisible_layer(self, progress: float):
        """Step 3: De onzichtbare laag"""
        self.fig.clear()
        ax = self.fig.add_subplot(111)
        ax.axis('off')
        ax.set_xlim(0, 100)
        ax.set_ylim(0, 100)

        # Title
        ax.text(50, 96, 'De Onzichtbare Laag',
                fontsize=52, fontweight='bold', ha='center',
                color=self.colors['accent'])

        ax.text(50, 90, 'Wat gebeurt er tussen vraag en antwoord?',
                fontsize=27, ha='center',
                color=self.colors['text'], alpha=0.7, style='italic')

        # Visual flow representation
        if progress > 0.15:
            flow_alpha = min(1.0, (progress - 0.15) / 0.15)

            # Input (visible)
            input_box = FancyBboxPatch(
                (8, 73), 18, 8,
                boxstyle="round,pad=0.7",
                facecolor=self.colors['primary'],
                edgecolor='white',
                linewidth=2,
                alpha=flow_alpha * 0.9
            )
            ax.add_patch(input_box)

            ax.text(17, 77, 'Vraag',
                    fontsize=20, ha='center', va='center',
                    color='white',
                    fontweight='bold', alpha=flow_alpha)

            # Output (visible)
            output_box = FancyBboxPatch(
                (74, 73), 18, 8,
                boxstyle="round,pad=0.7",
                facecolor=self.colors['secondary'],
                edgecolor='white',
                linewidth=2,
                alpha=flow_alpha * 0.9
            )
            ax.add_patch(output_box)

            ax.text(83, 77, 'Antwoord',
                    fontsize=20, ha='center', va='center',
                    color='white',
                    fontweight='bold', alpha=flow_alpha)

        # The invisible middle (the black box)
        if progress > 0.3:
            box_alpha = min(1.0, (progress - 0.3) / 0.2)

            # Large mysterious box
            mystery_box = FancyBboxPatch(
                (30, 45), 40, 30,
                boxstyle="round,pad=1.2",
                facecolor='#0a0a0a',
                edgecolor=self.colors['warning'],
                linewidth=4,
                linestyle='--',
                alpha=box_alpha * 0.95
            )
            ax.add_patch(mystery_box)

            ax.text(50, 71, '???',
                    fontsize=60, ha='center', va='center',
                    color=self.colors['warning'],
                    fontweight='bold', alpha=box_alpha)

            # Arrow in
            arrow_in = FancyArrowPatch(
                (26, 77), (32, 65),
                arrowstyle='->', mutation_scale=25,
                linewidth=3, color=self.colors['primary'],
                alpha=box_alpha * 0.7
            )
            ax.add_artist(arrow_in)

            # Arrow out
            arrow_out = FancyArrowPatch(
                (68, 65), (74, 77),
                arrowstyle='->', mutation_scale=25,
                linewidth=3, color=self.colors['secondary'],
                alpha=box_alpha * 0.7
            )
            ax.add_artist(arrow_out)

        # What's actually happening (reveal)
        invisible_steps = [
            {'text': 'Vraag omzetten naar embedding', 'delay': 0.45},
            {'text': 'Zoeken in vectordatabase', 'delay': 0.5},
            {'text': 'Relevante chunks selecteren', 'delay': 0.55},
            {'text': 'Context samenstellen', 'delay': 0.6},
            {'text': 'Prompt construeren', 'delay': 0.65},
            {'text': 'Model inference', 'delay': 0.7},
            {'text': 'Output formatteren', 'delay': 0.75}
        ]

        for i, step in enumerate(invisible_steps):
            if progress > step['delay']:
                step_alpha = min(1.0, (progress - step['delay']) / 0.05)
                y_pos = 65 - i * 3.2

                ax.text(50, y_pos, f"• {step['text']}",
                        fontsize=13, ha='center', va='center',
                        color=self.colors['cyan'],
                        alpha=step_alpha * 0.85)

        # Bottom insight
        if progress > 0.82:
            insight_alpha = min(1.0, (progress - 0.82) / 0.15)

            insight_box = FancyBboxPatch(
                (10, 15), 80, 20,
                boxstyle="round,pad=1",
                facecolor=self.colors['bg_light'],
                edgecolor=self.colors['highlight'],
                linewidth=3,
                alpha=insight_alpha * 0.9
            )
            ax.add_patch(insight_box)

            ax.text(50, 29, 'Elke stap heeft impact op kwaliteit',
                    fontsize=22, ha='center', va='center',
                    color=self.colors['highlight'],
                    fontweight='bold', alpha=insight_alpha)

            ax.text(50, 24, 'Traditioneel: test input → output',
                    fontsize=18, ha='center', va='center',
                    color=self.colors['text'], alpha=insight_alpha * 0.8)

            ax.text(50, 20, 'AI: test elke stap in de keten',
                    fontsize=18, ha='center', va='center',
                    color=self.colors['accent'],
                    fontweight='bold', alpha=insight_alpha * 0.9)

            ax.text(50, 16, 'Zonder inzicht in deze laag: geen kwaliteitsborging mogelijk',
                    fontsize=16, ha='center', va='center',
                    color=self.colors['dim'], alpha=insight_alpha * 0.8,
                    style='italic')

        self.add_status_indicator(progress < 1.0)
        plt.tight_layout()

    def draw_new_questions(self, progress: float):
        """Step 4: Welke vragen stel je nu?"""
        self.fig.clear()
        ax = self.fig.add_subplot(111)
        ax.axis('off')
        ax.set_xlim(0, 100)
        ax.set_ylim(0, 100)

        # Title
        ax.text(50, 95, 'Welke Vragen Stel Je Nu?',
                fontsize=48, fontweight='bold', ha='center',
                color=self.colors['highlight'])

        ax.text(50, 89, 'Van bekende naar nieuwe vraagstukken',
                fontsize=26, ha='center',
                color=self.colors['text'], alpha=0.7, style='italic')

        # Two columns: traditional vs AI-specific questions
        if progress > 0.15:
            col_alpha = min(1.0, (progress - 0.15) / 0.15)

            # Traditional column header
            trad_box = FancyBboxPatch(
                (8, 77), 38, 6,
                boxstyle="round,pad=0.6",
                facecolor=self.colors['secondary'],
                edgecolor='white',
                linewidth=2,
                alpha=col_alpha * 0.85
            )
            ax.add_patch(trad_box)

            ax.text(27, 80, 'Bekende Vragen',
                    fontsize=20, ha='center', va='center',
                    color='white',
                    fontweight='bold', alpha=col_alpha)

            # AI column header
            ai_box = FancyBboxPatch(
                (54, 77), 38, 6,
                boxstyle="round,pad=0.6",
                facecolor=self.colors['purple'],
                edgecolor='white',
                linewidth=2,
                alpha=col_alpha * 0.85
            )
            ax.add_patch(ai_box)

            ax.text(73, 80, 'Nieuwe Vragen (AI-specifiek)',
                    fontsize=20, ha='center', va='center',
                    color='white',
                    fontweight='bold', alpha=col_alpha)

        # Question pairs
        question_pairs = [
            {
                'traditional': 'Wie is eigenaar van\nde data?',
                'ai': 'Wie is eigenaar van\nde embeddings?',
                'delay': 0.3
            },
            {
                'traditional': 'Hoe vaak updaten\nwe informatie?',
                'ai': 'Wanneer verversen we\nde vectordatabase?',
                'delay': 0.4
            },
            {
                'traditional': 'Wie controleert\nde output?',
                'ai': 'Hoe valideren we\nrelevantie van chunks?',
                'delay': 0.5
            },
            {
                'traditional': 'Wat is de bron van\nwaarheid?',
                'ai': 'Hoe combineren we\nbronnen met model-kennis?',
                'delay': 0.6
            },
            {
                'traditional': 'Hoe documenteren\nwe wijzigingen?',
                'ai': 'Hoe traceren we\nprompt-versies?',
                'delay': 0.7
            }
        ]

        y_start = 70
        for i, pair in enumerate(question_pairs):
            if progress > pair['delay']:
                q_alpha = min(1.0, (progress - pair['delay']) / 0.08)
                y_pos = y_start - i * 11

                # Traditional question
                trad_q_box = FancyBboxPatch(
                    (9, y_pos - 4), 36, 7,
                    boxstyle="round,pad=0.5",
                    facecolor=self.colors['bg_light'],
                    edgecolor=self.colors['secondary'],
                    linewidth=2,
                    alpha=q_alpha * 0.8
                )
                ax.add_patch(trad_q_box)

                ax.text(27, y_pos + 0.5, pair['traditional'],
                        fontsize=13, ha='center', va='center',
                        color=self.colors['text'],
                        alpha=q_alpha * 0.9)

                # Arrow between
                arrow = FancyArrowPatch(
                    (47, y_pos + 0.5), (53, y_pos + 0.5),
                    arrowstyle='->', mutation_scale=20,
                    linewidth=2, color=self.colors['accent'],
                    alpha=q_alpha * 0.6
                )
                ax.add_artist(arrow)

                # AI question
                ai_q_box = FancyBboxPatch(
                    (55, y_pos - 4), 36, 7,
                    boxstyle="round,pad=0.5",
                    facecolor=self.colors['bg_light'],
                    edgecolor=self.colors['purple'],
                    linewidth=2,
                    alpha=q_alpha * 0.8
                )
                ax.add_patch(ai_q_box)

                ax.text(73, y_pos + 0.5, pair['ai'],
                        fontsize=13, ha='center', va='center',
                        color=self.colors['text'],
                        alpha=q_alpha * 0.9)

        # Bottom insight
        if progress > 0.82:
            insight_alpha = min(1.0, (progress - 0.82) / 0.15)

            insight_box = FancyBboxPatch(
                (10, 8), 80, 12,
                boxstyle="round,pad=1",
                facecolor=self.colors['bg_light'],
                edgecolor=self.colors['highlight'],
                linewidth=3,
                alpha=insight_alpha * 0.9
            )
            ax.add_patch(insight_box)

            ax.text(50, 16, 'Bekende vragen blijven relevant',
                    fontsize=19, ha='center', va='center',
                    color=self.colors['text'], alpha=insight_alpha * 0.9)

            ax.text(50, 11, 'Maar AI introduceert een hele nieuwe laag van vraagstukken',
                    fontsize=19, ha='center', va='center',
                    color=self.colors['highlight'],
                    fontweight='bold', alpha=insight_alpha)

        self.add_status_indicator(progress < 1.0)
        plt.tight_layout()

    def draw_quality_standards(self, progress: float):
        """Step 5: Kwaliteitsstandaarden bepalen"""
        self.fig.clear()
        ax = self.fig.add_subplot(111)
        ax.axis('off')
        ax.set_xlim(0, 100)
        ax.set_ylim(0, 100)

        # Title
        ax.text(50, 95, 'Kwaliteitsstandaarden in AI-Context',
                fontsize=45, fontweight='bold', ha='center',
                color=self.colors['accent'])

        ax.text(50, 89, 'Hoe bepaal je "goed genoeg" als het systeem leert en verandert?',
                fontsize=23, ha='center',
                color=self.colors['text'], alpha=0.7, style='italic')

        # Framework: traditional metrics vs AI metrics
        if progress > 0.15:
            framework_alpha = min(1.0, (progress - 0.15) / 0.15)

            # Traditional box
            trad_frame = FancyBboxPatch(
                (8, 60), 38, 20,
                boxstyle="round,pad=1",
                facecolor=self.colors['bg_light'],
                edgecolor=self.colors['secondary'],
                linewidth=3,
                alpha=framework_alpha * 0.9
            )
            ax.add_patch(trad_frame)

            ax.text(27, 76, 'Traditionele Metrieken',
                    fontsize=18, ha='center', va='center',
                    color=self.colors['secondary'],
                    fontweight='bold', alpha=framework_alpha)

            trad_metrics = [
                '• Beschikbaarheid',
                '• Response tijd',
                '• Foutmeldingen',
                '• Compliance status'
            ]

            for i, metric in enumerate(trad_metrics):
                ax.text(27, 72 - i * 3.5, metric,
                        fontsize=14, ha='center', va='center',
                        color=self.colors['text'],
                        alpha=framework_alpha * 0.85)

            # AI-specific box
            ai_frame = FancyBboxPatch(
                (54, 60), 38, 20,
                boxstyle="round,pad=1",
                facecolor=self.colors['bg_light'],
                edgecolor=self.colors['purple'],
                linewidth=3,
                alpha=framework_alpha * 0.9
            )
            ax.add_patch(ai_frame)

            ax.text(73, 76, 'AI-Specifieke Metrieken',
                    fontsize=18, ha='center', va='center',
                    color=self.colors['purple'],
                    fontweight='bold', alpha=framework_alpha)

            ai_metrics = [
                '• Retrieval relevantie',
                '• Context kwaliteit',
                '• Output consistentie',
                '• Bias detectie'
            ]

            for i, metric in enumerate(ai_metrics):
                ax.text(73, 72 - i * 3.5, metric,
                        fontsize=14, ha='center', va='center',
                        color=self.colors['text'],
                        alpha=framework_alpha * 0.85)

        # The key questions framework
        if progress > 0.4:
            key_alpha = min(1.0, (progress - 0.4) / 0.15)

            key_box = FancyBboxPatch(
                (10, 35), 80, 18,
                boxstyle="round,pad=1.2",
                facecolor=self.colors['bg_light'],
                edgecolor=self.colors['highlight'],
                linewidth=3,
                alpha=key_alpha * 0.95
            )
            ax.add_patch(key_box)

            ax.text(50, 50, 'Kernvragen voor Kwaliteitsstandaarden:',
                    fontsize=20, ha='center', va='center',
                    color=self.colors['highlight'],
                    fontweight='bold', alpha=key_alpha)

        key_questions = [
            {'q': 'Wat is "juist" als het model interpreteert?', 'delay': 0.5},
            {'q': 'Hoe meet je "relevantie" van geselecteerde context?', 'delay': 0.58},
            {'q': 'Wanneer is een embedding-update een "wijziging"?', 'delay': 0.66},
            {'q': 'Wie bepaalt of een gegenereerd antwoord "goed genoeg" is?', 'delay': 0.74}
        ]

        for i, kq in enumerate(key_questions):
            if progress > kq['delay']:
                kq_alpha = min(1.0, (progress - kq['delay']) / 0.06)
                y_pos = 45 - i * 3.2

                ax.text(50, y_pos, f"→ {kq['q']}",
                        fontsize=15, ha='center', va='center',
                        color=self.colors['text'],
                        alpha=kq_alpha * 0.9)

        # Final takeaway
        if progress > 0.85:
            final_alpha = min(1.0, (progress - 0.85) / 0.12)

            final_box = FancyBboxPatch(
                (8, 10), 84, 18,
                boxstyle="round,pad=1.2",
                facecolor=self.colors['bg_light'],
                edgecolor=self.colors['cyan'],
                linewidth=4,
                alpha=final_alpha * 0.95
            )
            ax.add_patch(final_box)

            ax.text(50, 24, 'Wat Hebben We Eraan?',
                    fontsize=24, ha='center', va='center',
                    color=self.colors['cyan'],
                    fontweight='bold', alpha=final_alpha)

            ax.text(50, 18, 'Inzicht in waar kwaliteit zit → betere afspraken maken',
                    fontsize=17, ha='center', va='center',
                    color=self.colors['text'], alpha=final_alpha * 0.9)

            ax.text(50, 14, 'Nieuwe vragen stellen → risico\'s vroegtijdig signaleren',
                    fontsize=17, ha='center', va='center',
                    color=self.colors['text'], alpha=final_alpha * 0.9)

            ax.text(50, 11, 'Standaarden bepalen → kwaliteit borgen in afspraken',
                    fontsize=17, ha='center', va='center',
                    color=self.colors['text'], alpha=final_alpha * 0.9)

        self.add_status_indicator(progress < 1.0)
        plt.tight_layout()


def main():
    """Main presentation runner"""
    print("\n" + "="*70)
    print(">> AI Quality Presentation - Professional Perspective")
    print("="*70)
    print("\nVan technische kennis naar strategische vraagstelling")
    print("\nStappen:")
    print("  1. Landing - Context")
    print("  2. Van Techniek naar Betekenis")
    print("  3. Waar Kwaliteit Bepaald Wordt")
    print("  4. De Onzichtbare Laag")
    print("  5. Welke Vragen Stel Je Nu?")
    print("  6. Kwaliteitsstandaarden Bepalen")
    print("\n[Keys]  SPACE=Next | B=Previous | R=Reset | Q=Quit")
    print("="*70 + "\n")

    presentation = QualityPresentation()
    presentation.run()


if __name__ == "__main__":
    main()