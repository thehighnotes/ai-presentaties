"""
AI Quality Governance Presentation
From AI knowledge to quality assurance in practice
Refactored with BasePresentation architecture
"""

import sys
import os
import numpy as np
import textwrap
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle, Arc
import matplotlib.patches as patches

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core import BasePresentation, PresentationStyle


class QualityPresentation(BasePresentation):
    """
    AI Quality Governance - Kennissessie Slotstuk
    Van AI-kennis naar Kwaliteitszorg in de Praktijk
    """

    def __init__(self):
        """Initialize the quality governance presentation"""
        step_names = [
            'Landing',
            'Het Beslismoment',
            'Waar Let Je Op?',
            'Van Data naar Betrouwbare AI',
            'Het Stakeholder Web',
            'Belangrijke Vragen',
            'Veelvoorkomende Valkuilen',
            'De Realiteit van Integratie',
            'Continue Verbetering'
        ]

        super().__init__("AI Kwaliteit in de Praktijk", step_names)

        # AI Scenarios with quality requirements
        self.scenarios = {
            'RAG': {
                'color': self.colors['primary'],
                'icon': '[<>]',
                'name': 'RAG',
                'quality_focus': ['Bronkwaliteit', 'Actualiteit', 'Relevantie', 'Traceerbaarheid']
            },
            'Finetuning': {
                'color': self.colors['secondary'],
                'icon': '>>',
                'name': 'Finetuning',
                'quality_focus': ['Datavolume', 'Representativiteit', 'Labeling', 'Bias']
            },
            'Hybrid': {
                'color': self.colors['purple'],
                'icon': '[*]',
                'name': 'Hybrid',
                'quality_focus': ['Balans', 'Complexiteit', 'Onderhoud', 'Consistentie']
            }
        }

        # Stakeholders - broad spectrum
        self.stakeholders = [
            {'name': 'Informatie-\nmanagement', 'angle': 0, 'color': self.colors['primary'], 'distance': 3},
            {'name': 'Data-\ngovernance', 'angle': 45, 'color': self.colors['secondary'], 'distance': 3.2},
            {'name': 'Privacy &\nSecurity', 'angle': 90, 'color': self.colors['warning'], 'distance': 3},
            {'name': 'Business\nOwners', 'angle': 135, 'color': self.colors['accent'], 'distance': 3.2},
            {'name': 'ICT /\nDevelopment', 'angle': 180, 'color': self.colors['cyan'], 'distance': 3},
            {'name': 'Compliance &\nAudit', 'angle': 225, 'color': self.colors['purple'], 'distance': 3.2},
            {'name': 'Gebruikers &\nExperts', 'angle': 270, 'color': self.colors['highlight'], 'distance': 3},
            {'name': 'Architectuur', 'angle': 315, 'color': '#60A5FA', 'distance': 3.2}
        ]

        # Governance questions per domain
        self.governance_questions = {
            'Data': [
                'Waar komen de data vandaan?',
                'Hoe actueel moeten ze zijn?',
                'Wie is eigenaar van de data?',
                'Wat is de kwaliteit van brondata?'
            ],
            'Model': [
                'Welke AI-aanpak past het beste?',
                'Hoe valideren we output?',
                'Wat zijn acceptabele foutenmarges?',
                'Hoe monitoren we performance?'
            ],
            'Proces': [
                'Wie autoriseert wijzigingen?',
                'Hoe testen we voor productie?',
                'Wat is de rollback strategie?',
                'Hoe documenteren we?'
            ],
            'Mensen': [
                'Wie heeft welke rol?',
                'Wat is ieders verantwoordelijkheid?',
                'Hoe communiceren we?',
                'Wie neemt besluiten?'
            ],
            'Ethics': [
                'Is output eerlijk & onbevooroordeeld?',
                'Kunnen we uitleg geven?',
                'Respecteren we privacy?',
                'Wat zijn de risico\'s?'
            ]
        }

        self.show_landing_page()

    def show_landing_page(self):
        """Display landing page"""
        self.fig.clear()
        ax = self.fig.add_subplot(111)
        ax.axis('off')
        ax.set_xlim(0, 100)
        ax.set_ylim(0, 100)

        # Main title
        title_box = FancyBboxPatch(
            (10, 50), 80, 30,
            boxstyle="round,pad=2",
            facecolor=self.colors['bg_light'],
            edgecolor=self.colors['primary'],
            linewidth=4,
            alpha=0.95
        )
        ax.add_patch(title_box)

        # Gradient effect with multiple texts
        ax.text(50, 70, 'Van AI-kennis',
                fontsize=63, fontweight='bold', ha='center', va='center',
                color=self.colors['primary'])

        ax.text(50, 62, 'naar',
                fontsize=42, ha='center', va='center',
                color=self.colors['text'], alpha=0.6, style='italic')

        ax.text(50, 53, 'Kwaliteitszorg',
                fontsize=63, fontweight='bold', ha='center', va='center',
                color=self.colors['secondary'])

        # Subtitle
        ax.text(50, 40, 'Voor BiSL adviseurs en Functioneel Beheerders',
                fontsize=27, ha='center', va='center',
                color=self.colors['text'], alpha=0.7, style='italic')

        # Key insight box
        insight_box = FancyBboxPatch(
            (12, 18), 76, 16,
            boxstyle="round,pad=1.2",
            facecolor=self.colors['bg_light'],
            edgecolor=self.colors['accent'],
            linewidth=3,
            alpha=0.9
        )
        ax.add_patch(insight_box)

        ax.text(50, 29, '[OK] Je snapt nu de techniek:',
                fontsize=24, ha='center', va='center',
                color=self.colors['secondary'], fontweight='bold', alpha=0.9)

        ax.text(50, 25, 'Vectors • Neural Networks • RAG • Finetuning',
                fontsize=21, ha='center', va='center',
                color=self.colors['text'], alpha=0.8)

        ax.text(50, 21, '[?] Maar... welke vragen stel je in jouw rol?',
                fontsize=24, ha='center', va='center',
                color=self.colors['highlight'], fontweight='bold')

        # Instructions
        ax.text(50, 8, '* Druk op SPATIE om te starten',
                fontsize=24, ha='center', va='center',
                color=self.colors['dim'], alpha=0.8)

        ax.text(50, 4, 'Controls: SPACE=Volgende | B=Vorige | R=Reset | F=Fullscreen | Q=Quit',
                fontsize=16, ha='center', va='center',
                color=self.colors['dim'], alpha=0.6)

        import matplotlib.pyplot as plt
        plt.tight_layout()

    def get_frames_for_step(self, step: int) -> int:
        """Get animation frame count for each step"""
        return 60  # Standard frame count for all steps

    def animate_step(self, frame: int):
        """Animate current step"""
        total_frames = self.get_frames_for_step(self.current_step)
        progress = frame / (total_frames - 1) if total_frames > 1 else 1

        if self.current_step == 0:
            pass  # Landing is static
        elif self.current_step == 1:
            self.draw_decision_moment(progress)
        elif self.current_step == 2:
            self.draw_quality_dimensions(progress)
        elif self.current_step == 3:
            self.draw_data_pipeline(progress)
        elif self.current_step == 4:
            self.draw_stakeholder_web(progress)
        elif self.current_step == 5:
            self.draw_governance_questions(progress)
        elif self.current_step == 6:
            self.draw_risk_patterns(progress)
        elif self.current_step == 7:
            self.draw_integration_reality(progress)
        elif self.current_step == 8:
            self.draw_continuous_loop(progress)

        if frame >= total_frames - 1:
            self.on_animation_complete()

    def draw_current_step_static(self):
        """Draw current step as static image"""
        if self.current_step == -1:
            self.show_landing_page()
        elif self.current_step == 1:
            self.draw_decision_moment(1.0)
        elif self.current_step == 2:
            self.draw_quality_dimensions(1.0)
        elif self.current_step == 3:
            self.draw_data_pipeline(1.0)
        elif self.current_step == 4:
            self.draw_stakeholder_web(1.0)
        elif self.current_step == 5:
            self.draw_governance_questions(1.0)
        elif self.current_step == 6:
            self.draw_risk_patterns(1.0)
        elif self.current_step == 7:
            self.draw_integration_reality(1.0)
        elif self.current_step == 8:
            self.draw_continuous_loop(1.0)
        import matplotlib.pyplot as plt
        plt.draw()

    def draw_decision_moment(self, progress: float):
        """Step 1: The decision moment - which AI approach?"""
        self.fig.clear()
        ax = self.fig.add_subplot(111)
        ax.axis('off')
        ax.set_xlim(0, 100)
        ax.set_ylim(0, 100)

        # Title
        title_alpha = min(1.0, progress * 2)
        ax.text(50, 95, 'Stap 1: Het Beslismoment',
                fontsize=48, fontweight='bold', ha='center', va='top',
                color=self.colors['highlight'], alpha=title_alpha)

        ax.text(50, 89, 'Welke AI-aanpak kies je voor jouw datastroom?',
                fontsize=27, ha='center', va='top',
                color=self.colors['text'], alpha=title_alpha * 0.7, style='italic')

        # Central question circle
        if progress > 0.15:
            q_alpha = min(1.0, (progress - 0.15) / 0.15)

            center_circle = Circle((50, 60), 8,
                                  facecolor=self.colors['bg_light'],
                                  edgecolor=self.colors['highlight'],
                                  linewidth=4, alpha=0.95 * q_alpha)
            ax.add_patch(center_circle)

            ax.text(50, 62, '[?]',
                   fontsize=48, ha='center', va='center',
                   alpha=q_alpha,
                   color=self.colors['highlight'],
                   fontweight='bold')

            ax.text(50, 56, 'Welke\naanpak?',
                   fontsize=18, ha='center', va='center',
                   color=self.colors['text'], alpha=q_alpha,
                   fontweight='bold')

        # Three scenarios - fanning out from center
        scenarios_data = [
            ('RAG', 20, 60, self.colors['primary'], '[<>]'),
            ('Finetuning', 50, 35, self.colors['secondary'], '>>'),
            ('Hybrid', 80, 60, self.colors['purple'], '[*]')
        ]

        for idx, (name, x, y, color, icon) in enumerate(scenarios_data):
            delay = 0.3 + idx * 0.15
            if progress > delay:
                alpha = min(1.0, (progress - delay) / 0.15)

                # Line from center to box - calculate proper angle
                dx = x - 50
                dy = y - 60
                dist = np.sqrt(dx**2 + dy**2)
                # Start from edge of center circle (radius ~8)
                start_x = 50 + (dx / dist) * 8
                start_y = 60 + (dy / dist) * 8

                ax.plot([start_x, x], [start_y, y], color=color, linewidth=2,
                       alpha=alpha * 0.6, linestyle='--', zorder=1)

                # Scenario box
                box = FancyBboxPatch(
                    (x - 10, y - 6), 20, 12,
                    boxstyle="round,pad=0.8",
                    facecolor=self.colors['bg_light'],
                    edgecolor=color,
                    linewidth=3,
                    alpha=0.95 * alpha
                )
                ax.add_patch(box)

                ax.text(x, y + 3, icon,
                       fontsize=36, ha='center', va='center',
                       alpha=alpha)

                ax.text(x, y - 1, name,
                       fontsize=19, ha='center', va='center',
                       color=color, fontweight='bold',
                       alpha=alpha)

        # Key insight at bottom
        if progress > 0.7:
            insight_alpha = min(1.0, (progress - 0.7) / 0.3)

            insight_box = FancyBboxPatch(
                (15, 10), 70, 15,
                boxstyle="round,pad=1",
                facecolor=self.colors['bg_light'],
                edgecolor=self.colors['accent'],
                linewidth=2,
                alpha=0.9 * insight_alpha
            )
            ax.add_patch(insight_box)

            ax.text(50, 20, '[!] Elk scenario heeft eigen kwaliteitseisen',
                   fontsize=24, ha='center', va='center',
                   color=self.colors['accent'], fontweight='bold',
                   alpha=insight_alpha)

            ax.text(50, 15, 'De keuze bepaalt wát je moet controleren en mét wie',
                   fontsize=21, ha='center', va='center',
                   color=self.colors['text'], alpha=insight_alpha * 0.9)

        self.add_status_indicator(progress < 1.0)
        import matplotlib.pyplot as plt
        plt.tight_layout()

    def draw_quality_dimensions(self, progress: float):
        """Step 2: Quality Dimensions Matrix"""
        self.fig.clear()
        ax = self.fig.add_subplot(111)
        ax.axis('off')
        ax.set_xlim(0, 100)
        ax.set_ylim(0, 100)

        # Title
        ax.text(50, 96, 'Stap 2: Waar Let Je Op?',
                fontsize=48, fontweight='bold', ha='center', va='top',
                color=self.colors['secondary'])

        ax.text(50, 91, 'Elk AI-scenario heeft z\'n eigen aandachtspunten',
                fontsize=27, ha='center', va='top',
                color=self.colors['text'], alpha=0.7, style='italic')

        # Matrix grid - 3 scenarios x 5 dimensions
        dimensions = [
            ('[DATA] Data\nKwaliteit', 'Volledigheid, correctheid, actualiteit'),
            ('[LOCK] Privacy &\nSecurity', 'AVG-compliance, toegangscontrole, audit trails'),
            ('[==] Eerlijkheid\n& Bias', 'Eerlijkheid, transparantie, verantwoording'),
            ('[>>] Prestaties &\nNauwkeurigheid', 'Foutenmarges, validatie, monitoring'),
            ('[CFG] Beheer &\nGovernance', 'Eigenaarschap, procedures, documentatie')
        ]

        scenarios = ['RAG', 'Finetuning', 'Hybrid']
        scenario_colors = [self.colors['primary'], self.colors['secondary'], self.colors['purple']]

        # Draw matrix
        start_x = 20
        col_width = 25
        row_height = 15
        start_y = 75

        # Column headers
        if progress > 0.1:
            header_alpha = min(1.0, (progress - 0.1) / 0.15)
            for i, (scenario, color) in enumerate(zip(scenarios, scenario_colors)):
                x = start_x + (i + 1) * col_width

                icon = ['[<>]', '>>', '[*]'][i]
                ax.text(x, start_y + 5, f'{icon} {scenario}',
                       fontsize=16, ha='center', va='center',
                       color=color, fontweight='bold',
                       alpha=header_alpha)

        # Rows with dimensions and checks
        for row_idx, (dim_name, dim_desc) in enumerate(dimensions):
            row_delay = 0.25 + row_idx * 0.12
            if progress > row_delay:
                row_alpha = min(1.0, (progress - row_delay) / 0.12)

                y = start_y - (row_idx + 1) * row_height

                # Dimension name
                ax.text(start_x - 2, y, dim_name,
                       fontsize=13, ha='right', va='center',
                       color=self.colors['text'], alpha=row_alpha,
                       fontweight='bold')

                # Description
                wrapped_desc = textwrap.fill(dim_desc, width=20)
                ax.text(start_x - 2, y - 3.5, wrapped_desc,
                       fontsize=10, ha='right', va='center',
                       color=self.colors['dim'], alpha=row_alpha * 0.7)

                # Relevance matrix
                relevance = [
                    [3, 2, 3],  # Data Quality
                    [2, 1, 2],  # Privacy
                    [1, 3, 2],  # Bias
                    [2, 3, 3],  # Performance
                    [2, 2, 3]   # Governance
                ]

                for col_idx, rel in enumerate(relevance[row_idx]):
                    x = start_x + (col_idx + 1) * col_width

                    if rel == 3:
                        indicator = '●●●'
                        alpha_mult = 1.0
                    elif rel == 2:
                        indicator = '●●○'
                        alpha_mult = 0.7
                    else:
                        indicator = '●○○'
                        alpha_mult = 0.4

                    ax.text(x, y, indicator,
                           fontsize=21, ha='center', va='center',
                           color=scenario_colors[col_idx],
                           alpha=row_alpha * alpha_mult)

        # Legend
        if progress > 0.85:
            legend_alpha = min(1.0, (progress - 0.85) / 0.15)

            ax.text(50, 8, '●●● = Kritisch  |  ●●○ = Belangrijk  |  ●○○ = Relevant',
                   fontsize=15, ha='center', va='center',
                   color=self.colors['dim'], alpha=legend_alpha * 0.8)

        # Insight
        if progress > 0.75:
            insight_alpha = min(1.0, (progress - 0.75) / 0.15)

            ax.text(50, 3, '[i] Geen scenario is "makkelijk" - elk vraagt andere aandacht',
                   fontsize=16, ha='center', va='center',
                   color=self.colors['accent'], fontweight='bold',
                   alpha=insight_alpha)

        self.add_status_indicator(progress < 1.0)
        import matplotlib.pyplot as plt
        plt.tight_layout()

    def draw_data_pipeline(self, progress: float):
        """Step 3: Data Quality Pipeline - where are the checkpoints?"""
        self.fig.clear()
        ax = self.fig.add_subplot(111)
        ax.axis('off')
        ax.set_xlim(0, 100)
        ax.set_ylim(0, 100)

        # Title
        ax.text(50, 96, 'Stap 3: Van Data naar Betrouwbare AI',
                fontsize=48, fontweight='bold', ha='center', va='top',
                color=self.colors['accent'])

        ax.text(50, 91, 'Waar in de keten moet je kwaliteit controleren?',
                fontsize=27, ha='center', va='top',
                color=self.colors['text'], alpha=0.7, style='italic')

        # Pipeline flow (left to right)
        pipeline_stages = [
            {'name': 'Bron\nData', 'x': 10, 'y': 60, 'checks': ['Volledigheid', 'Actualiteit', 'Eigenaarschap'],
             'color': self.colors['warning'], 'icon': '[#]'},
            {'name': 'Data\nPreparatie', 'x': 27, 'y': 60, 'checks': ['Opschoning', 'Transformatie', 'Validatie'],
             'color': self.colors['primary'], 'icon': '🔧'},
            {'name': 'Model\nInput', 'x': 44, 'y': 60, 'checks': ['Format', 'Encoding', 'Bias check'],
             'color': self.colors['secondary'], 'icon': '⚙️'},
            {'name': 'AI\nVerwerking', 'x': 61, 'y': 60, 'checks': ['Monitoring', 'Logging', 'Explainability'],
             'color': self.colors['purple'], 'icon': '🤖'},
            {'name': 'Output\nValidatie', 'x': 78, 'y': 60, 'checks': ['Accuracy', 'Bias', 'Safety'],
             'color': self.colors['highlight'], 'icon': '[OK]'},
        ]

        # Draw pipeline flow
        for idx, stage in enumerate(pipeline_stages):
            delay = 0.15 + idx * 0.15
            if progress > delay:
                alpha = min(1.0, (progress - delay) / 0.15)

                # Stage box
                box = FancyBboxPatch(
                    (stage['x'] - 5, stage['y'] - 5), 10, 10,
                    boxstyle="round,pad=0.5",
                    facecolor=self.colors['bg_light'],
                    edgecolor=stage['color'],
                    linewidth=3,
                    alpha=0.95 * alpha
                )
                ax.add_patch(box)

                # Icon and name
                ax.text(stage['x'], stage['y'] + 1, stage['icon'],
                       fontsize=30, ha='center', va='center',
                       alpha=alpha)

                ax.text(stage['x'], stage['y'] - 3, stage['name'],
                       fontsize=12, ha='center', va='center',
                       color=stage['color'], fontweight='bold',
                       alpha=alpha)

                # Checks below stage
                check_y = stage['y'] - 15
                for check_idx, check in enumerate(stage['checks']):
                    check_alpha = min(1.0, (progress - delay - 0.05 * check_idx) / 0.1)
                    if check_alpha > 0:
                        ax.text(stage['x'], check_y - check_idx * 4, f'• {check}',
                               fontsize=10, ha='center', va='center',
                               color=self.colors['text'], alpha=check_alpha * 0.8)

                # Arrow to next stage
                if idx < len(pipeline_stages) - 1:
                    arrow_alpha = min(1.0, (progress - delay) / 0.1)
                    if arrow_alpha > 0:
                        next_stage = pipeline_stages[idx + 1]
                        arrow = FancyArrowPatch(
                            (stage['x'] + 5, stage['y']),
                            (next_stage['x'] - 5, next_stage['y']),
                            arrowstyle='->,head_width=0.4,head_length=0.8',
                            color=self.colors['dim'],
                            linewidth=2,
                            alpha=arrow_alpha * 0.6
                        )
                        ax.add_patch(arrow)

        # Feedback loop
        if progress > 0.8:
            feedback_alpha = min(1.0, (progress - 0.8) / 0.2)

            arc = Arc((44, 35), 60, 30, angle=0, theta1=180, theta2=360,
                     color=self.colors['secondary'], linewidth=2,
                     linestyle='--', alpha=feedback_alpha * 0.7)
            ax.add_patch(arc)

            ax.text(44, 22, '🔄 Continuous Monitoring & Improvement',
                   fontsize=15, ha='center', va='center',
                   color=self.colors['secondary'], fontweight='bold',
                   alpha=feedback_alpha)

        # Key insight
        if progress > 0.85:
            insight_alpha = min(1.0, (progress - 0.85) / 0.15)

            insight_box = FancyBboxPatch(
                (10, 5), 80, 10,
                boxstyle="round,pad=0.8",
                facecolor=self.colors['bg_light'],
                edgecolor=self.colors['accent'],
                linewidth=2,
                alpha=0.9 * insight_alpha
            )
            ax.add_patch(insight_box)

            ax.text(50, 10, '(!) Elk checkpoint vraagt andere expertise en verantwoordelijkheden',
                   fontsize=18, ha='center', va='center',
                   color=self.colors['accent'], fontweight='bold',
                   alpha=insight_alpha)

            ax.text(50, 7, 'Dit is geen ICT-taak alleen - dit vraagt samenwerking over de hele keten',
                   fontsize=15, ha='center', va='center',
                   color=self.colors['text'], alpha=insight_alpha * 0.8)

        self.add_status_indicator(progress < 1.0)
        import matplotlib.pyplot as plt
        plt.tight_layout()

    def draw_stakeholder_web(self, progress: float):
        """Step 4: Stakeholder Web - who needs to be involved?"""
        self.fig.clear()
        ax = self.fig.add_subplot(111)
        ax.axis('off')
        ax.set_xlim(-10, 110)
        ax.set_ylim(-10, 110)

        # Title
        ax.text(50, 98, 'Stap 4: Het Stakeholder Web',
                fontsize=39, fontweight='bold', ha='center', va='top',
                color=self.colors['text'])

        ax.text(50, 93, 'AI kwaliteit is geen ICT-ding - het vraagt ketenbrede afstemming',
                fontsize=21, ha='center', va='top',
                color=self.colors['accent'], alpha=0.9, fontweight='bold')

        # Center: AI Quality
        if progress > 0.1:
            center_alpha = min(1.0, (progress - 0.1) / 0.15)

            center_circle = Circle((50, 50), 6,
                                  facecolor=self.colors['bg_light'],
                                  edgecolor=self.colors['highlight'],
                                  linewidth=4, alpha=0.95 * center_alpha)
            ax.add_patch(center_circle)

            ax.text(50, 51, 'AI\nQuality',
                   fontsize=16, ha='center', va='center',
                   color=self.colors['highlight'], fontweight='bold',
                   alpha=center_alpha)

        # Stakeholders in circle around center
        for idx, stakeholder in enumerate(self.stakeholders):
            delay = 0.25 + idx * 0.08
            if progress > delay:
                alpha = min(1.0, (progress - delay) / 0.1)

                # Calculate position
                angle_rad = np.radians(stakeholder['angle'])
                distance = stakeholder['distance'] * 12
                x = 50 + distance * np.cos(angle_rad)
                y = 50 + distance * np.sin(angle_rad)

                # Line to center
                line_alpha = min(1.0, (progress - delay) / 0.08)
                if line_alpha > 0:
                    ax.plot([50, x], [50, y],
                           color=stakeholder['color'],
                           linewidth=1.5,
                           alpha=line_alpha * 0.4,
                           linestyle='-')

                # Stakeholder node
                node = Circle((x, y), 4,
                            facecolor=self.colors['bg_light'],
                            edgecolor=stakeholder['color'],
                            linewidth=2.5,
                            alpha=0.95 * alpha)
                ax.add_patch(node)

                # Label
                ax.text(x, y, stakeholder['name'],
                       fontsize=12, ha='center', va='center',
                       color=stakeholder['color'], fontweight='bold',
                       alpha=alpha)

        # Interconnections
        if progress > 0.75:
            connection_alpha = min(1.0, (progress - 0.75) / 0.2)

            key_connections = [
                (0, 1),  # Informatie mgmt <-> Data governance
                (1, 2),  # Data governance <-> Privacy
                (3, 4),  # Business <-> ICT
                (4, 7),  # ICT <-> Architectuur
                (5, 6),  # Compliance <-> Gebruikers
                (0, 3),  # Informatie mgmt <-> Business
            ]

            for conn_idx, (idx1, idx2) in enumerate(key_connections):
                conn_delay = connection_alpha - conn_idx * 0.05
                if conn_delay > 0:
                    s1 = self.stakeholders[idx1]
                    s2 = self.stakeholders[idx2]

                    angle_rad1 = np.radians(s1['angle'])
                    angle_rad2 = np.radians(s2['angle'])
                    x1 = 50 + s1['distance'] * 12 * np.cos(angle_rad1)
                    y1 = 50 + s1['distance'] * 12 * np.sin(angle_rad1)
                    x2 = 50 + s2['distance'] * 12 * np.cos(angle_rad2)
                    y2 = 50 + s2['distance'] * 12 * np.sin(angle_rad2)

                    ax.plot([x1, x2], [y1, y2],
                           color=self.colors['dim'],
                           linewidth=1,
                           alpha=conn_delay * 0.3,
                           linestyle=':')

        # Key insight
        if progress > 0.85:
            insight_alpha = min(1.0, (progress - 0.85) / 0.15)

            insight_box = FancyBboxPatch(
                (10, 3), 80, 10,
                boxstyle="round,pad=0.8",
                facecolor=self.colors['bg_light'],
                edgecolor=self.colors['warning'],
                linewidth=2,
                alpha=0.9 * insight_alpha
            )
            ax.add_patch(insight_box)

            ax.text(50, 9, '⚡ Elk stakeholder heeft eigen perspectief en verantwoordelijkheid',
                   fontsize=16, ha='center', va='center',
                   color=self.colors['warning'], fontweight='bold',
                   alpha=insight_alpha)

            ax.text(50, 5.5, 'Zonder goede afstemming loop je risico\'s - zowel operationeel als compliance',
                   fontsize=15, ha='center', va='center',
                   color=self.colors['text'], alpha=insight_alpha * 0.8)

        self.add_status_indicator(progress < 1.0)
        import matplotlib.pyplot as plt
        plt.tight_layout()

    def draw_governance_questions(self, progress: float):
        """Step 5: Governance Questions - what MUST be asked?"""
        self.fig.clear()
        ax = self.fig.add_subplot(111)
        ax.axis('off')
        ax.set_xlim(0, 100)
        ax.set_ylim(0, 100)

        # Title
        ax.text(50, 96, 'Stap 5: Belangrijke Vragen',
                fontsize=48, fontweight='bold', ha='center', va='top',
                color=self.colors['purple'])

        ax.text(50, 91, 'Wat moet je als BiSL adviseur ALTIJD vragen?',
                fontsize=27, ha='center', va='top',
                color=self.colors['text'], alpha=0.7, style='italic')

        # 5 domains with questions
        domains = ['Data', 'Model', 'Proces', 'Mensen', 'Ethics']
        domain_colors = [
            self.colors['primary'],
            self.colors['secondary'],
            self.colors['accent'],
            self.colors['purple'],
            self.colors['highlight']
        ]

        # Grid layout: 2 rows, first row 3 columns, second row 2 columns
        positions = [
            (18, 65),  # Data
            (50, 65),  # Model
            (82, 65),  # Proces
            (33, 30),  # Mensen
            (67, 30)   # Ethics
        ]

        for idx, (domain, color, pos) in enumerate(zip(domains, domain_colors, positions)):
            delay = 0.15 + idx * 0.15
            if progress > delay:
                alpha = min(1.0, (progress - delay) / 0.15)

                x, y = pos

                # Domain box
                box = FancyBboxPatch(
                    (x - 13, y + 8), 26, 7,
                    boxstyle="round,pad=0.5",
                    facecolor=self.colors['bg_light'],
                    edgecolor=color,
                    linewidth=3,
                    alpha=0.95 * alpha
                )
                ax.add_patch(box)

                ax.text(x, y + 11.5, domain,
                       fontsize=18, ha='center', va='center',
                       color=color, fontweight='bold',
                       alpha=alpha)

                # Questions under domain
                questions = self.governance_questions[domain]
                for q_idx, question in enumerate(questions):
                    q_delay = delay + 0.05 + q_idx * 0.03
                    if progress > q_delay:
                        q_alpha = min(1.0, (progress - q_delay) / 0.08)

                        q_y = y - q_idx * 4.2

                        wrapped_q = textwrap.fill(f'• {question}', width=28)
                        ax.text(x, q_y, wrapped_q,
                               fontsize=10.5, ha='center', va='center',
                               color=self.colors['text'], alpha=q_alpha * 0.85,
                               linespacing=1.4)

        # Key insight
        if progress > 0.85:
            insight_alpha = min(1.0, (progress - 0.85) / 0.15)

            insight_box = FancyBboxPatch(
                (10, 3), 80, 9,
                boxstyle="round,pad=0.8",
                facecolor=self.colors['bg_light'],
                edgecolor=self.colors['accent'],
                linewidth=2,
                alpha=0.9 * insight_alpha
            )
            ax.add_patch(insight_box)

            ax.text(50, 8.5, '[i] Deze vragen MOETEN antwoorden hebben voordat je begint',
                   fontsize=18, ha='center', va='center',
                   color=self.colors['accent'], fontweight='bold',
                   alpha=insight_alpha)

            ax.text(50, 5.5, 'Geen antwoord = risico op kwaliteitsissues, compliance problemen of bias',
                   fontsize=15, ha='center', va='center',
                   color=self.colors['text'], alpha=insight_alpha * 0.8)

        self.add_status_indicator(progress < 1.0)
        import matplotlib.pyplot as plt
        plt.tight_layout()

    def draw_risk_patterns(self, progress: float):
        """Step 6: Risk Patterns - what often goes wrong?"""
        self.fig.clear()
        ax = self.fig.add_subplot(111)
        ax.axis('off')
        ax.set_xlim(0, 100)
        ax.set_ylim(0, 100)

        # Title
        ax.text(50, 96, 'Stap 6: Veelvoorkomende Valkuilen',
                fontsize=48, fontweight='bold', ha='center', va='top',
                color=self.colors['warning'])

        ax.text(50, 91, 'Wat zie je vaak gebeuren in de praktijk?',
                fontsize=27, ha='center', va='top',
                color=self.colors['text'], alpha=0.7, style='italic')

        # Risk patterns in 3x2 grid
        risk_patterns = [
            {
                'name': '[DRIFT] Data Drift',
                'desc': 'Brondata verandert,\nmodel niet geüpdatet',
                'impact': 'Hoog',
                'color': self.colors['warning']
            },
            {
                'name': '[BIAS] Verborgen Bias',
                'desc': 'Bias in trainingsdata\nwordt niet gedetecteerd',
                'impact': 'Hoog',
                'color': self.colors['warning']
            },
            {
                'name': '[WHO] Eigenaarschap',
                'desc': 'Onduidelijk wie\nverantwoordelijk is',
                'impact': 'Medium',
                'color': self.colors['accent']
            },
            {
                'name': '[MON] Geen Monitoring',
                'desc': 'Geen monitoring van\noutput kwaliteit',
                'impact': 'Hoog',
                'color': self.colors['warning']
            },
            {
                'name': '[DOC] Documentatie',
                'desc': 'Besluiten en keuzes\nniet gedocumenteerd',
                'impact': 'Medium',
                'color': self.colors['accent']
            },
            {
                'name': '[SILO] Silo-werking',
                'desc': 'Teams werken langs\nelkaar heen',
                'impact': 'Hoog',
                'color': self.colors['warning']
            }
        ]

        # Grid positions
        cols = 3
        start_x = 15
        start_y = 72
        col_width = 28
        row_height = 30

        for idx, risk in enumerate(risk_patterns):
            delay = 0.15 + idx * 0.12
            if progress > delay:
                alpha = min(1.0, (progress - delay) / 0.12)

                col = idx % cols
                row = idx // cols

                x = start_x + col * col_width
                y = start_y - row * row_height

                # Risk box
                box = FancyBboxPatch(
                    (x, y - 8), 24, 16,
                    boxstyle="round,pad=0.7",
                    facecolor=self.colors['bg_light'],
                    edgecolor=risk['color'],
                    linewidth=2.5,
                    alpha=0.95 * alpha
                )
                ax.add_patch(box)

                # Risk name
                ax.text(x + 12, y + 4, risk['name'],
                       fontsize=15, ha='center', va='center',
                       color=risk['color'], fontweight='bold',
                       alpha=alpha)

                # Description
                ax.text(x + 12, y - 1, risk['desc'],
                       fontsize=12, ha='center', va='center',
                       color=self.colors['text'], alpha=alpha * 0.8,
                       linespacing=1.3)

                # Impact badge
                impact_color = self.colors['warning'] if risk['impact'] == 'Hoog' else self.colors['accent']
                ax.text(x + 12, y - 6.5, f"Impact: {risk['impact']}",
                       fontsize=10, ha='center', va='center',
                       bbox=dict(boxstyle='round,pad=0.3',
                               facecolor=impact_color,
                               alpha=0.3),
                       color=impact_color, fontweight='bold',
                       alpha=alpha)

        # Key insight
        if progress > 0.8:
            insight_alpha = min(1.0, (progress - 0.8) / 0.2)

            insight_box = FancyBboxPatch(
                (10, 4), 80, 10,
                boxstyle="round,pad=0.8",
                facecolor=self.colors['bg_light'],
                edgecolor=self.colors['secondary'],
                linewidth=2,
                alpha=0.9 * insight_alpha
            )
            ax.add_patch(insight_box)

            ax.text(50, 10, '✅ Deze risico\'s zijn te managen met de juiste governance',
                   fontsize=18, ha='center', va='center',
                   color=self.colors['secondary'], fontweight='bold',
                   alpha=insight_alpha)

            ax.text(50, 6.5, 'Maar dan moet je ze wel identificeren én de juiste mensen betrekken',
                   fontsize=15, ha='center', va='center',
                   color=self.colors['text'], alpha=insight_alpha * 0.8)

        self.add_status_indicator(progress < 1.0)
        import matplotlib.pyplot as plt
        plt.tight_layout()

    def draw_integration_reality(self, progress: float):
        """Step 7: Integration Reality - what does this look like in practice?"""
        self.fig.clear()
        ax = self.fig.add_subplot(111)
        ax.axis('off')
        ax.set_xlim(0, 100)
        ax.set_ylim(0, 100)

        # Title
        ax.text(50, 96, 'Stap 7: De Praktijk - Alles Hangt Samen',
                fontsize=39, fontweight='bold', ha='center', va='top',
                color=self.colors['text'])

        ax.text(50, 91, 'AI kwaliteit is geen losse activiteit - het zit in je hele werkwijze',
                fontsize=19, ha='center', va='top',
                color=self.colors['dim'], alpha=0.8, style='italic')

        # Central integration hub
        if progress > 0.1:
            hub_alpha = min(1.0, (progress - 0.1) / 0.15)

            center = Circle((50, 50), 9,
                           facecolor=self.colors['bg_light'],
                           edgecolor=self.colors['highlight'],
                           linewidth=4, alpha=0.95 * hub_alpha)
            ax.add_patch(center)

            ax.text(50, 52, 'AI Quality\nIntegration',
                   fontsize=16, ha='center', va='center',
                   color=self.colors['highlight'], fontweight='bold',
                   alpha=hub_alpha,
                   linespacing=1.3)

        # Integration points around center
        integration_points = [
            {'name': 'BiSL\nProcessen', 'angle': 0, 'icon': '📋', 'color': self.colors['primary']},
            {'name': 'Change\nManagement', 'angle': 45, 'icon': '🔄', 'color': self.colors['secondary']},
            {'name': 'Security &\nPrivacy', 'angle': 90, 'icon': '🔒', 'color': self.colors['warning']},
            {'name': 'Service\nCatalogue', 'angle': 135, 'icon': '📖', 'color': self.colors['accent']},
            {'name': 'Architecture\nGovernance', 'angle': 180, 'icon': '🏛️', 'color': self.colors['cyan']},
            {'name': 'Data\nGovernance', 'angle': 225, 'icon': '[#]', 'color': self.colors['purple']},
            {'name': 'Incident\nManagement', 'angle': 270, 'icon': '🚨', 'color': '#EF4444'},
            {'name': 'Continuous\nImprovement', 'angle': 315, 'icon': '[^]', 'color': '#10B981'}
        ]

        for idx, point in enumerate(integration_points):
            delay = 0.25 + idx * 0.08
            if progress > delay:
                alpha = min(1.0, (progress - delay) / 0.1)

                # Calculate position
                angle_rad = np.radians(point['angle'])
                distance = 32
                x = 50 + distance * np.cos(angle_rad)
                y = 50 + distance * np.sin(angle_rad)

                # Line to center
                ax.plot([50, x], [50, y],
                       color=point['color'],
                       linewidth=2,
                       alpha=alpha * 0.5,
                       linestyle='-')

                # Integration point
                point_circle = Circle((x, y), 6,
                                    facecolor=self.colors['bg_light'],
                                    edgecolor=point['color'],
                                    linewidth=2.5,
                                    alpha=0.95 * alpha)
                ax.add_patch(point_circle)

                # Icon
                ax.text(x, y + 1.5, point['icon'],
                       fontsize=21, ha='center', va='center',
                       alpha=alpha)

                # Label outside circle
                label_distance = 8
                label_x = 50 + (distance + label_distance) * np.cos(angle_rad)
                label_y = 50 + (distance + label_distance) * np.sin(angle_rad)

                ax.text(label_x, label_y, point['name'],
                       fontsize=12, ha='center', va='center',
                       color=point['color'], fontweight='bold',
                       alpha=alpha,
                       linespacing=1.2)

        # Interconnection lines
        if progress > 0.75:
            conn_alpha = min(1.0, (progress - 0.75) / 0.2)

            key_links = [
                (0, 1),  # BiSL <-> Change Mgmt
                (2, 5),  # Security <-> Data Governance
                (4, 5),  # Architecture <-> Data Governance
                (6, 7),  # Incident <-> Continuous Improvement
            ]

            for link_idx, (idx1, idx2) in enumerate(key_links):
                p1 = integration_points[idx1]
                p2 = integration_points[idx2]

                angle_rad1 = np.radians(p1['angle'])
                angle_rad2 = np.radians(p2['angle'])
                x1 = 50 + 32 * np.cos(angle_rad1)
                y1 = 50 + 32 * np.sin(angle_rad1)
                x2 = 50 + 32 * np.cos(angle_rad2)
                y2 = 50 + 32 * np.sin(angle_rad2)

                ax.plot([x1, x2], [y1, y2],
                       color=self.colors['dim'],
                       linewidth=1,
                       alpha=conn_alpha * 0.3,
                       linestyle=':')

        # Key insight
        if progress > 0.85:
            insight_alpha = min(1.0, (progress - 0.85) / 0.15)

            insight_box = FancyBboxPatch(
                (10, 3), 80, 10,
                boxstyle="round,pad=0.8",
                facecolor=self.colors['bg_light'],
                edgecolor=self.colors['highlight'],
                linewidth=2,
                alpha=0.9 * insight_alpha
            )
            ax.add_patch(insight_box)

            ax.text(50, 9, '⚡ AI Quality is geen add-on - het moet geïntegreerd zijn',
                   fontsize=18, ha='center', va='center',
                   color=self.colors['highlight'], fontweight='bold',
                   alpha=insight_alpha)

            ax.text(50, 5.5, 'Gebruik bestaande processen en governance structuren als fundament',
                   fontsize=15, ha='center', va='center',
                   color=self.colors['text'], alpha=insight_alpha * 0.8)

        self.add_status_indicator(progress < 1.0)
        import matplotlib.pyplot as plt
        plt.tight_layout()

    def draw_continuous_loop(self, progress: float):
        """Step 8: Continuous Quality Loop - it never ends!"""
        self.fig.clear()
        ax = self.fig.add_subplot(111)
        ax.axis('off')
        ax.set_xlim(0, 100)
        ax.set_ylim(0, 100)

        # Title
        title_alpha = min(1.0, progress * 2)
        ax.text(50, 96, 'Stap 8: Continue Verbetering',
                fontsize=48, fontweight='bold', ha='center', va='top',
                color=self.colors['highlight'], alpha=title_alpha)

        ax.text(50, 91, 'AI-kwaliteit is een doorlopend proces, geen eenmalige taak',
                fontsize=24, ha='center', va='top',
                color=self.colors['text'], alpha=title_alpha * 0.7, style='italic')

        # Circular process (PDCA-like for AI Quality)
        loop_stages = [
            {'name': 'Plan', 'desc': 'Definieer kwaliteitseisen\nBetrek stakeholders\nStel governance in',
             'angle': 90, 'color': self.colors['primary'], 'icon': '[PLAN]'},
            {'name': 'Build', 'desc': 'Implementeer checkpoints\nValideer datastromen\nTest grondig',
             'angle': 0, 'color': self.colors['secondary'], 'icon': '[BUILD]'},
            {'name': 'Monitor', 'desc': 'Track performance\nDetecteer afwijkingen\nLog beslissingen',
             'angle': 270, 'color': self.colors['accent'], 'icon': '[MON]'},
            {'name': 'Improve', 'desc': 'Analyseer feedback\nOptimaliseer processen\nUpdate documentatie',
             'angle': 180, 'color': self.colors['purple'], 'icon': '[>>]'}
        ]

        # Draw circular process
        radius = 22
        center_x, center_y = 50, 55

        for idx, stage in enumerate(loop_stages):
            delay = 0.15 + idx * 0.15
            if progress > delay:
                alpha = min(1.0, (progress - delay) / 0.15)

                # Calculate position
                angle_rad = np.radians(stage['angle'])
                x = center_x + radius * np.cos(angle_rad)
                y = center_y + radius * np.sin(angle_rad)

                # Stage circle
                stage_circle = Circle((x, y), 8,
                                     facecolor=self.colors['bg_light'],
                                     edgecolor=stage['color'],
                                     linewidth=3,
                                     alpha=0.95 * alpha)
                ax.add_patch(stage_circle)

                # Icon and name
                ax.text(x, y + 2, stage['icon'],
                       fontsize=30, ha='center', va='center',
                       alpha=alpha)

                ax.text(x, y - 2, stage['name'],
                       fontsize=15, ha='center', va='center',
                       color=stage['color'], fontweight='bold',
                       alpha=alpha)

                # Description outside circle
                desc_distance = 15
                desc_x = center_x + (radius + desc_distance) * np.cos(angle_rad)
                desc_y = center_y + (radius + desc_distance) * np.sin(angle_rad)

                wrapped_desc = textwrap.fill(stage['desc'], width=22)
                ax.text(desc_x, desc_y, wrapped_desc,
                       fontsize=12, ha='center', va='center',
                       color=self.colors['text'], alpha=alpha * 0.8,
                       linespacing=1.4)

                # Arrow to next stage
                next_idx = (idx + 1) % len(loop_stages)
                next_angle = np.radians(loop_stages[next_idx]['angle'])

                if progress > delay + 0.1:
                    arrow_alpha = min(1.0, (progress - delay - 0.1) / 0.1)

                    next_x = center_x + radius * np.cos(next_angle)
                    next_y = center_y + radius * np.sin(next_angle)

                    arrow = FancyArrowPatch(
                        (x + 7 * np.cos(angle_rad - np.pi/4), y + 7 * np.sin(angle_rad - np.pi/4)),
                        (next_x - 7 * np.cos(next_angle + np.pi/4), next_y - 7 * np.sin(next_angle + np.pi/4)),
                        arrowstyle='->,head_width=0.6,head_length=1',
                        color=self.colors['highlight'],
                        linewidth=3,
                        alpha=arrow_alpha * 0.7,
                        connectionstyle="arc3,rad=0.3"
                    )
                    ax.add_patch(arrow)

        # Center: Continuous
        if progress > 0.7:
            center_alpha = min(1.0, (progress - 0.7) / 0.2)

            center_circle = Circle((center_x, center_y), 5,
                                  facecolor=self.colors['bg_light'],
                                  edgecolor=self.colors['highlight'],
                                  linewidth=3,
                                  alpha=0.95 * center_alpha)
            ax.add_patch(center_circle)

            ax.text(center_x, center_y, '🔄',
                   fontsize=24, ha='center', va='center',
                   alpha=center_alpha)

        # Final insight
        if progress > 0.85:
            final_alpha = min(1.0, (progress - 0.85) / 0.15)

            final_box = FancyBboxPatch(
                (10, 3), 80, 20,
                boxstyle="round,pad=1",
                facecolor=self.colors['bg_light'],
                edgecolor=self.colors['secondary'],
                linewidth=3,
                alpha=0.95 * final_alpha
            )
            ax.add_patch(final_box)

            ax.text(50, 18, '>> Takeaway: AI Quality is ketenbrede verantwoordelijkheid',
                   fontsize=21, ha='center', va='center',
                   color=self.colors['secondary'], fontweight='bold',
                   alpha=final_alpha)

            key_points = [
                '[OK] Stel de juiste vragen voordat je begint',
                '[OK] Betrek alle stakeholders - niet alleen ICT',
                '[OK] Bouw quality checkpoints in je datastroom',
                '[OK] Monitor continu en verbeter waar nodig'
            ]

            for idx, point in enumerate(key_points):
                ax.text(50, 13 - idx * 3, point,
                       fontsize=15, ha='center', va='center',
                       color=self.colors['text'], alpha=final_alpha * 0.9)

        self.add_status_indicator(progress < 1.0)
        import matplotlib.pyplot as plt
        plt.tight_layout()


def main():
    """Main entry point for standalone execution"""
    print("="*80)
    print("AI QUALITY GOVERNANCE - Kennissessie Slotstuk")
    print("="*80)
    print("\n[#] Overzicht:")
    print("  Dit is het sluitstuk na Vector/RAG/Finetuning presentaties.")
    print("  Focus: Van AI-kennis naar kwaliteitszorg in de praktijk.\n")

    print(">> Stappen:")
    for i, step in enumerate(['Landing', 'Decision Moment', 'Quality Dimensions Matrix',
                             'Data Quality Pipeline', 'Stakeholder Web', 'Governance Questions',
                             'Risk Patterns', 'Integration Reality', 'Continuous Loop'], 1):
        print(f"  {i}. {step}")

    print("\n[Keys]  Controls:")
    print("  SPACE : Volgende stap")
    print("  B     : Vorige stap")
    print("  R     : Reset")
    print("  Q     : Quit")
    print("  F     : Fullscreen")

    print("\n[i] Kernboodschap:")
    print("  AI quality is geen ICT-taak alleen - het vraagt ketenbrede afstemming")
    print("  Visualiseert: stakeholders, quality checkpoints, governance vragen, risico's")

    print("\n" + "="*80 + "\n")

    presentation = QualityPresentation()
    presentation.show()


if __name__ == "__main__":
    main()
