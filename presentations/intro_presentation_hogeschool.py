"""
Hogeschool Introduction Presentation
Proper introduction establishing baseline knowledge and setting up the session

Steps:
1. Landing - Welkom
2. Over Mezelf
3. Wat We Al Weten Over AI
4. AI voor Informatieverwerking
5. Waarom Kwaliteit Belangrijk Is
6. Wat Gaan We Bespreken?
7. Waarom Deze Onderwerpen?

~8-10 minutes, accessible for all Hogeschool colleagues
"""

import sys
import os
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle, Rectangle

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core import BasePresentation, PresentationStyle


class IntroHogeschoolPresentation(BasePresentation):
    """
    Introduction presentation for Hogeschool colleagues
    Establishes baseline and sets expectations
    """

    def __init__(self):
        """Initialize the presentation"""
        step_names = [
            'Welkom',
            'Over Mezelf',
            'Wat We Al Weten Over AI',
            'AI voor Informatieverwerking',
            'Waarom Kwaliteit Belangrijk Is',
            'Wat Gaan We Bespreken?',
            'Waarom Deze Onderwerpen?'
        ]

        super().__init__("AI Kennissessie: Introductie", step_names)
        self.show_landing_page()

    def get_frames_for_step(self, step: int) -> int:
        """Get animation frame count for each step"""
        return 60  # Standard 60 frames per step

    def show_landing_page(self):
        """Display welcoming landing page"""
        self.fig.clear()
        ax = self.fig.add_subplot(111)
        ax.axis('off')
        ax.set_xlim(0, 100)
        ax.set_ylim(0, 100)

        # Main title box
        title_box = FancyBboxPatch(
            (10, 60), 80, 28,
            boxstyle="round,pad=2",
            facecolor=self.colors['bg_light'],
            edgecolor=self.colors['highlight'],
            linewidth=4,
            alpha=0.95
        )
        ax.add_patch(title_box)

        # Title
        ax.text(50, 78, 'AI Kennissessie',
                fontsize=62, fontweight='bold', ha='center', va='center',
                color=self.colors['highlight'])

        ax.text(50, 70, 'Voor Hogeschool Professionals',
                fontsize=28, ha='center', va='center',
                color=self.colors['text'], alpha=0.85, style='italic')

        ax.text(50, 65, 'Van Basis naar Praktijk',
                fontsize=24, ha='center', va='center',
                color=self.colors['secondary'], alpha=0.8)

        # Welcoming message
        welcome_box = FancyBboxPatch(
            (15, 35), 70, 18,
            boxstyle="round,pad=1.5",
            facecolor=self.colors['bg_light'],
            edgecolor=self.colors['secondary'],
            linewidth=3,
            alpha=0.9
        )
        ax.add_patch(welcome_box)

        ax.text(50, 48, 'Welkom!',
                fontsize=30, fontweight='bold', ha='center', va='center',
                color=self.colors['secondary'])

        ax.text(50, 42, 'We gaan samen verkennen hoe AI werkt en hoe we',
                fontsize=19, ha='center', va='center',
                color=self.colors['text'], alpha=0.9)

        ax.text(50, 38, 'kwaliteit kunnen borgen in AI-toepassingen',
                fontsize=19, ha='center', va='center',
                color=self.colors['text'], alpha=0.9)

        # Instructions
        instr_box = FancyBboxPatch(
            (25, 15), 50, 13,
            boxstyle="round,pad=1",
            facecolor=self.colors['bg_light'],
            edgecolor=self.colors['accent'],
            linewidth=2,
            alpha=0.85
        )
        ax.add_patch(instr_box)

        ax.text(50, 24, '>> Druk op SPATIE om te beginnen <<',
                fontsize=20, ha='center', va='center',
                color=self.colors['accent'], fontweight='bold')

        ax.text(50, 19, 'SPACE=Volgende | B=Vorige | R=Reset | Q=Afsluiten',
                fontsize=14, ha='center', va='center',
                color=self.colors['dim'], alpha=0.8)

        # Footer
        ax.text(50, 6, 'Geen technische achtergrond nodig - we beginnen bij het begin',
                fontsize=18, ha='center', va='center',
                color=self.colors['text'], alpha=0.6, style='italic')

        plt.tight_layout()

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
            self.show_landing_page()
        else:
            self.draw_step(self.current_step, 1.0)
        plt.draw()

    def draw_step(self, step: int, progress: float):
        """Draw the current step"""
        if step == 0:
            self.draw_about_me(progress)
        elif step == 1:
            self.draw_what_we_know(progress)
        elif step == 2:
            self.draw_ai_information_processing(progress)
        elif step == 3:
            self.draw_why_quality_matters(progress)
        elif step == 4:
            self.draw_topics_overview(progress)
        elif step == 5:
            self.draw_why_these_topics(progress)

    def draw_about_me(self, progress: float):
        """Step 1: Over mezelf"""
        self.fig.clear()
        ax = self.fig.add_subplot(111)
        ax.axis('off')
        ax.set_xlim(0, 100)
        ax.set_ylim(0, 100)

        # Title
        alpha = min(1.0, progress * 2)
        ax.text(50, 95, 'Over Mezelf',
                fontsize=50, fontweight='bold', ha='center',
                color=self.colors['primary'], alpha=alpha)

        # Profile section
        if progress > 0.2:
            profile_alpha = min(1.0, (progress - 0.2) / 0.3)

            # Profile box
            profile_box = FancyBboxPatch(
                (15, 60), 70, 25,
                boxstyle="round,pad=1.5",
                facecolor=self.colors['bg_light'],
                edgecolor=self.colors['primary'],
                linewidth=3,
                alpha=profile_alpha * 0.95
            )
            ax.add_patch(profile_box)

            # Icon/Avatar placeholder
            circle = Circle((30, 72.5), 8,
                          facecolor=self.colors['primary'],
                          edgecolor='white',
                          linewidth=3,
                          alpha=profile_alpha)
            ax.add_patch(circle)

            ax.text(30, 72.5, '[user]',
                    fontsize=60, ha='center', va='center',
                    alpha=profile_alpha)

            # Text content - AANPASBAAR
            ax.text(45, 80, '[Jouw Naam]',
                    fontsize=28, ha='left', va='center',
                    color=self.colors['text'],
                    fontweight='bold', alpha=profile_alpha)

            ax.text(45, 75, '[Jouw Rol/Functie]',
                    fontsize=20, ha='left', va='center',
                    color=self.colors['secondary'],
                    alpha=profile_alpha * 0.9)

            ax.text(45, 70, '[Jouw Afdeling/Team]',
                    fontsize=18, ha='left', va='center',
                    color=self.colors['text'],
                    alpha=profile_alpha * 0.85)

            ax.text(45, 65, '[Korte relevante ervaring met AI/topic]',
                    fontsize=17, ha='left', va='center',
                    color=self.colors['text'],
                    alpha=profile_alpha * 0.8,
                    style='italic')

        # Why this session
        if progress > 0.55:
            why_alpha = min(1.0, (progress - 0.55) / 0.3)

            why_box = FancyBboxPatch(
                (10, 30), 80, 22,
                boxstyle="round,pad=1.2",
                facecolor=self.colors['bg_light'],
                edgecolor=self.colors['accent'],
                linewidth=3,
                alpha=why_alpha * 0.95
            )
            ax.add_patch(why_box)

            ax.text(50, 47, 'Waarom Deze Sessie?',
                    fontsize=24, ha='center', va='center',
                    color=self.colors['accent'],
                    fontweight='bold', alpha=why_alpha)

            reasons = [
                'AI wordt steeds belangrijker in ons werk',
                'We moeten weten hoe we kwaliteit kunnen borgen',
                'Iedereen kan meedenken, ongeacht technische achtergrond'
            ]

            for i, reason in enumerate(reasons):
                y_pos = 40 - i * 5
                ax.text(50, y_pos, f'• {reason}',
                        fontsize=17, ha='center', va='center',
                        color=self.colors['text'],
                        alpha=why_alpha * 0.9)

        # Bottom note
        if progress > 0.85:
            note_alpha = min(1.0, (progress - 0.85) / 0.15)
            ax.text(50, 15, 'Vragen? Stel ze gerust tussendoor!',
                    fontsize=20, ha='center', va='center',
                    color=self.colors['secondary'],
                    fontweight='bold', alpha=note_alpha)

        self.add_status_indicator(progress < 1.0)
        plt.tight_layout()

    def draw_what_we_know(self, progress: float):
        """Step 2: Wat we al weten over AI"""
        self.fig.clear()
        ax = self.fig.add_subplot(111)
        ax.axis('off')
        ax.set_xlim(0, 100)
        ax.set_ylim(0, 100)

        # Title
        ax.text(50, 95, 'Wat We Al Weten Over AI',
                fontsize=48, fontweight='bold', ha='center',
                color=self.colors['highlight'])

        ax.text(50, 89, 'Onze gezamenlijke baseline',
                fontsize=24, ha='center',
                color=self.colors['text'], alpha=0.7, style='italic')

        # Common experiences with AI
        experiences = [
            {
                'icon': '[chat]',
                'title': 'We kunnen chatten met AI',
                'examples': 'ChatGPT, Copilot, Claude...',
                'y': 75,
                'delay': 0.15
            },
            {
                'icon': '[doc]',
                'title': 'We kunnen documenten uploaden',
                'examples': 'PDFs, Word bestanden analyseren',
                'y': 60,
                'delay': 0.3
            },
            {
                'icon': '[edit]',
                'title': 'AI kan teksten schrijven',
                'examples': 'E-mails, samenvattingen, rapporten',
                'y': 45,
                'delay': 0.45
            },
            {
                'icon': '[search]',
                'title': 'AI kan zoeken en analyseren',
                'examples': 'Informatie vinden, patronen herkennen',
                'y': 30,
                'delay': 0.6
            }
        ]

        for exp in experiences:
            if progress > exp['delay']:
                exp_alpha = min(1.0, (progress - exp['delay']) / 0.12)

                # Experience box
                exp_box = FancyBboxPatch(
                    (12, exp['y'] - 5), 76, 10,
                    boxstyle="round,pad=1",
                    facecolor=self.colors['bg_light'],
                    edgecolor=self.colors['secondary'],
                    linewidth=2,
                    alpha=exp_alpha * 0.9
                )
                ax.add_patch(exp_box)

                # Icon
                ax.text(18, exp['y'], exp['icon'],
                        fontsize=36, ha='center', va='center',
                        alpha=exp_alpha)

                # Title
                ax.text(30, exp['y'] + 1.5, exp['title'],
                        fontsize=20, ha='left', va='center',
                        color=self.colors['text'],
                        fontweight='bold', alpha=exp_alpha)

                # Examples
                ax.text(30, exp['y'] - 2, exp['examples'],
                        fontsize=15, ha='left', va='center',
                        color=self.colors['dim'],
                        alpha=exp_alpha * 0.85, style='italic')

        # Bottom message
        if progress > 0.8:
            bottom_alpha = min(1.0, (progress - 0.8) / 0.2)

            bottom_box = FancyBboxPatch(
                (10, 8), 80, 12,
                boxstyle="round,pad=1",
                facecolor=self.colors['bg_light'],
                edgecolor=self.colors['highlight'],
                linewidth=3,
                alpha=bottom_alpha * 0.95
            )
            ax.add_patch(bottom_box)

            ax.text(50, 16, '✓ Dit is onze gezamenlijke startpositie',
                    fontsize=22, ha='center', va='center',
                    color=self.colors['highlight'],
                    fontweight='bold', alpha=bottom_alpha)

            ax.text(50, 11, 'Nu gaan we een laag dieper: hóe werkt dit eigenlijk?',
                    fontsize=18, ha='center', va='center',
                    color=self.colors['text'],
                    alpha=bottom_alpha * 0.9)

        self.add_status_indicator(progress < 1.0)
        plt.tight_layout()

    def draw_ai_information_processing(self, progress: float):
        """Step 3: AI voor informatieverwerking"""
        self.fig.clear()
        ax = self.fig.add_subplot(111)
        ax.axis('off')
        ax.set_xlim(0, 100)
        ax.set_ylim(0, 100)

        # Title
        ax.text(50, 95, 'AI voor Informatieverwerking',
                fontsize=46, fontweight='bold', ha='center',
                color=self.colors['primary'])

        ax.text(50, 89, 'Hoe AI ons helpt informatie te verwerken',
                fontsize=23, ha='center',
                color=self.colors['text'], alpha=0.7, style='italic')

        # Visual flow: Problem → AI → Solution
        if progress > 0.15:
            flow_alpha = min(1.0, (progress - 0.15) / 0.2)

            # Problem box
            problem_box = FancyBboxPatch(
                (8, 65), 25, 15,
                boxstyle="round,pad=1",
                facecolor=self.colors['bg_light'],
                edgecolor=self.colors['warning'],
                linewidth=3,
                alpha=flow_alpha * 0.9
            )
            ax.add_patch(problem_box)

            ax.text(20.5, 76, '[books]',
                    fontsize=36, ha='center', va='center',
                    alpha=flow_alpha)

            ax.text(20.5, 71, 'Teveel\nInformatie',
                    fontsize=18, ha='center', va='center',
                    color=self.colors['warning'],
                    fontweight='bold', alpha=flow_alpha)

            ax.text(20.5, 67.5, 'Te veel documenten\nom door te lezen',
                    fontsize=12, ha='center', va='center',
                    color=self.colors['text'],
                    alpha=flow_alpha * 0.8)

        if progress > 0.35:
            ai_alpha = min(1.0, (progress - 0.35) / 0.2)

            # Arrow to AI
            arrow1 = FancyArrowPatch(
                (34, 72.5), (43, 72.5),
                arrowstyle='->', mutation_scale=30,
                linewidth=3, color=self.colors['accent'],
                alpha=ai_alpha * 0.7
            )
            ax.add_artist(arrow1)

            # AI processing box
            ai_box = FancyBboxPatch(
                (43, 65), 25, 15,
                boxstyle="round,pad=1",
                facecolor=self.colors['primary'],
                edgecolor='white',
                linewidth=3,
                alpha=ai_alpha * 0.95
            )
            ax.add_patch(ai_box)

            ax.text(55.5, 76, '[AI]',
                    fontsize=36, ha='center', va='center',
                    alpha=ai_alpha)

            ax.text(55.5, 71, 'AI Verwerkt',
                    fontsize=18, ha='center', va='center',
                    color='white',
                    fontweight='bold', alpha=ai_alpha)

            ax.text(55.5, 67.5, 'Leest, begrijpt\nen selecteert',
                    fontsize=12, ha='center', va='center',
                    color='white',
                    alpha=ai_alpha * 0.9)

        if progress > 0.55:
            solution_alpha = min(1.0, (progress - 0.55) / 0.2)

            # Arrow to solution
            arrow2 = FancyArrowPatch(
                (69, 72.5), (78, 72.5),
                arrowstyle='->', mutation_scale=30,
                linewidth=3, color=self.colors['accent'],
                alpha=solution_alpha * 0.7
            )
            ax.add_artist(arrow2)

            # Solution box
            solution_box = FancyBboxPatch(
                (67, 65), 25, 15,
                boxstyle="round,pad=1",
                facecolor=self.colors['bg_light'],
                edgecolor=self.colors['secondary'],
                linewidth=3,
                alpha=solution_alpha * 0.9
            )
            ax.add_patch(solution_box)

            ax.text(79.5, 76, '*',
                    fontsize=36, ha='center', va='center',
                    alpha=solution_alpha)

            ax.text(79.5, 71, 'Bruikbaar\nAntwoord',
                    fontsize=18, ha='center', va='center',
                    color=self.colors['secondary'],
                    fontweight='bold', alpha=solution_alpha)

            ax.text(79.5, 67.5, 'Precies wat je\nnodig had',
                    fontsize=12, ha='center', va='center',
                    color=self.colors['text'],
                    alpha=solution_alpha * 0.8)

        # Use cases
        if progress > 0.75:
            cases_alpha = min(1.0, (progress - 0.75) / 0.25)

            cases_box = FancyBboxPatch(
                (10, 25), 80, 30,
                boxstyle="round,pad=1.5",
                facecolor=self.colors['bg_light'],
                edgecolor=self.colors['accent'],
                linewidth=3,
                alpha=cases_alpha * 0.95
            )
            ax.add_patch(cases_box)

            ax.text(50, 51, 'Praktijkvoorbeelden:',
                    fontsize=22, ha='center', va='center',
                    color=self.colors['accent'],
                    fontweight='bold', alpha=cases_alpha)

            examples = [
                '[list] Studenten kunnen vragen stellen over hun cursusmateriaal',
                '[search] Docenten kunnen snel relevante bronnen vinden',
                '[#] Onderzoekers kunnen grote hoeveelheden data analyseren',
                '[work] Medewerkers kunnen beleidsdocumenten doorzoeken'
            ]

            for i, example in enumerate(examples):
                y_pos = 45 - i * 5
                ax.text(50, y_pos, example,
                        fontsize=16, ha='center', va='center',
                        color=self.colors['text'],
                        alpha=cases_alpha * 0.9)

            ax.text(50, 27, '→ AI maakt informatie toegankelijk',
                    fontsize=19, ha='center', va='center',
                    color=self.colors['secondary'],
                    fontweight='bold', alpha=cases_alpha,
                    style='italic')

        self.add_status_indicator(progress < 1.0)
        plt.tight_layout()

    def draw_why_quality_matters(self, progress: float):
        """Step 4: Waarom kwaliteit belangrijk is"""
        self.fig.clear()
        ax = self.fig.add_subplot(111)
        ax.axis('off')
        ax.set_xlim(0, 100)
        ax.set_ylim(0, 100)

        # Title
        ax.text(50, 95, 'Waarom Kwaliteit Belangrijk Is',
                fontsize=46, fontweight='bold', ha='center',
                color=self.colors['warning'])

        # The stakes
        if progress > 0.15:
            stakes_alpha = min(1.0, (progress - 0.15) / 0.2)

            stakes_box = FancyBboxPatch(
                (12, 72), 76, 15,
                boxstyle="round,pad=1.2",
                facecolor=self.colors['bg_light'],
                edgecolor=self.colors['warning'],
                linewidth=3,
                alpha=stakes_alpha * 0.95
            )
            ax.add_patch(stakes_box)

            ax.text(50, 83, 'We vertrouwen erop dat AI:',
                    fontsize=24, ha='center', va='center',
                    color=self.colors['warning'],
                    fontweight='bold', alpha=stakes_alpha)

            stakes = [
                'Juiste informatie geeft (geen verzinsels)',
                'Relevante antwoorden vindt (geen ruis)',
                'Consistent is (niet random)'
            ]

            for i, stake in enumerate(stakes):
                y_pos = 77 - i * 4.5
                ax.text(50, y_pos, f'✓ {stake}',
                        fontsize=17, ha='center', va='center',
                        color=self.colors['text'],
                        alpha=stakes_alpha * 0.9)

        # Consequences of poor quality
        if progress > 0.4:
            bad_alpha = min(1.0, (progress - 0.4) / 0.25)

            ax.text(50, 60, 'Wat Gebeurt Er Bij Slechte Kwaliteit?',
                    fontsize=24, ha='center', va='center',
                    color=self.colors['secondary'],
                    fontweight='bold', alpha=bad_alpha)

            consequences = [
                {
                    'icon': '[X]',
                    'text': 'Verkeerde beslissingen',
                    'example': 'Gebaseerd op onjuiste informatie',
                    'x': 25,
                    'y': 48
                },
                {
                    'icon': '[time]',
                    'text': 'Tijdverlies',
                    'example': 'Antwoorden controleren en herdoen',
                    'x': 75,
                    'y': 48
                },
                {
                    'icon': '[?]',
                    'text': 'Verlies van vertrouwen',
                    'example': 'AI wordt niet meer gebruikt',
                    'x': 25,
                    'y': 35
                },
                {
                    'icon': '(!)',
                    'text': 'Risico\'s',
                    'example': 'Fouten in kritieke processen',
                    'x': 75,
                    'y': 35
                }
            ]

            for cons in consequences:
                cons_box = FancyBboxPatch(
                    (cons['x'] - 12, cons['y'] - 5), 24, 10,
                    boxstyle="round,pad=0.8",
                    facecolor=self.colors['bg_light'],
                    edgecolor=self.colors['warning'],
                    linewidth=2,
                    alpha=bad_alpha * 0.85
                )
                ax.add_patch(cons_box)

                ax.text(cons['x'], cons['y'] + 2.5, cons['icon'],
                        fontsize=28, ha='center', va='center',
                        alpha=bad_alpha)

                ax.text(cons['x'], cons['y'], cons['text'],
                        fontsize=15, ha='center', va='center',
                        color=self.colors['text'],
                        fontweight='bold', alpha=bad_alpha)

                ax.text(cons['x'], cons['y'] - 3, cons['example'],
                        fontsize=11, ha='center', va='center',
                        color=self.colors['dim'],
                        alpha=bad_alpha * 0.8, style='italic')

        # The solution
        if progress > 0.75:
            solution_alpha = min(1.0, (progress - 0.75) / 0.25)

            solution_box = FancyBboxPatch(
                (10, 8), 80, 18,
                boxstyle="round,pad=1.5",
                facecolor=self.colors['bg_light'],
                edgecolor=self.colors['highlight'],
                linewidth=4,
                alpha=solution_alpha * 0.95
            )
            ax.add_patch(solution_box)

            ax.text(50, 22, '[i] Daarom Deze Sessie',
                    fontsize=26, ha='center', va='center',
                    color=self.colors['highlight'],
                    fontweight='bold', alpha=solution_alpha)

            ax.text(50, 16, 'We gaan leren hoe AI werkt, waar risico\'s zitten,',
                    fontsize=18, ha='center', va='center',
                    color=self.colors['text'],
                    alpha=solution_alpha * 0.9)

            ax.text(50, 11, 'en hoe we kwaliteit kunnen borgen in onze AI-toepassingen',
                    fontsize=18, ha='center', va='center',
                    color=self.colors['text'],
                    alpha=solution_alpha * 0.9)

        self.add_status_indicator(progress < 1.0)
        plt.tight_layout()

    def draw_topics_overview(self, progress: float):
        """Step 5: Wat gaan we bespreken?"""
        self.fig.clear()
        ax = self.fig.add_subplot(111)
        ax.axis('off')
        ax.set_xlim(0, 100)
        ax.set_ylim(0, 100)

        # Title
        ax.text(50, 95, 'Wat Gaan We Bespreken?',
                fontsize=48, fontweight='bold', ha='center',
                color=self.colors['highlight'])

        ax.text(50, 89, 'Onze roadmap voor vandaag',
                fontsize=23, ha='center',
                color=self.colors['text'], alpha=0.7, style='italic')

        # Topics in cards
        topics = [
            {
                'number': '1',
                'icon': '[#]',
                'title': 'Vectors & Embeddings',
                'description': 'Hoe AI "begrijpt" wat tekst betekent',
                'color': self.colors['primary'],
                'y': 75,
                'delay': 0.15
            },
            {
                'number': '2',
                'icon': '[search]',
                'title': 'RAG (Retrieval)',
                'description': 'Hoe AI de juiste informatie vindt',
                'color': self.colors['secondary'],
                'y': 60,
                'delay': 0.3
            },
            {
                'number': '3',
                'icon': '[grad]',
                'title': 'Finetuning',
                'description': 'Hoe AI leert van specifieke voorbeelden',
                'color': self.colors['purple'],
                'y': 45,
                'delay': 0.45
            },
            {
                'number': '4',
                'icon': '[OK]',
                'title': 'Kwaliteitsborging',
                'description': 'Hoe we ervoor zorgen dat AI betrouwbaar is',
                'color': self.colors['accent'],
                'y': 30,
                'delay': 0.6
            },
            {
                'number': '5',
                'icon': '[chat]',
                'title': 'Prompt Engineering',
                'description': 'Hoe we effectief communiceren met AI',
                'color': self.colors['cyan'],
                'y': 15,
                'delay': 0.75
            }
        ]

        for topic in topics:
            if progress > topic['delay']:
                topic_alpha = min(1.0, (progress - topic['delay']) / 0.12)

                # Topic card
                topic_box = FancyBboxPatch(
                    (12, topic['y'] - 5), 76, 10,
                    boxstyle="round,pad=1",
                    facecolor=self.colors['bg_light'],
                    edgecolor=topic['color'],
                    linewidth=3,
                    alpha=topic_alpha * 0.95
                )
                ax.add_patch(topic_box)

                # Number badge
                badge = Circle((18, topic['y']), 2.5,
                             facecolor=topic['color'],
                             edgecolor='white',
                             linewidth=2,
                             alpha=topic_alpha)
                ax.add_patch(badge)

                ax.text(18, topic['y'], topic['number'],
                        fontsize=22, ha='center', va='center',
                        color='white',
                        fontweight='bold', alpha=topic_alpha)

                # Icon
                ax.text(27, topic['y'], topic['icon'],
                        fontsize=32, ha='center', va='center',
                        alpha=topic_alpha)

                # Title
                ax.text(35, topic['y'] + 1.5, topic['title'],
                        fontsize=20, ha='left', va='center',
                        color=topic['color'],
                        fontweight='bold', alpha=topic_alpha)

                # Description
                ax.text(35, topic['y'] - 2, topic['description'],
                        fontsize=15, ha='left', va='center',
                        color=self.colors['text'],
                        alpha=topic_alpha * 0.85)

        self.add_status_indicator(progress < 1.0)
        plt.tight_layout()

    def draw_why_these_topics(self, progress: float):
        """Step 6: Waarom deze onderwerpen?"""
        self.fig.clear()
        ax = self.fig.add_subplot(111)
        ax.axis('off')
        ax.set_xlim(0, 100)
        ax.set_ylim(0, 100)

        # Title
        ax.text(50, 95, 'Waarom Deze Onderwerpen?',
                fontsize=48, fontweight='bold', ha='center',
                color=self.colors['secondary'])

        # The journey metaphor
        if progress > 0.15:
            journey_alpha = min(1.0, (progress - 0.15) / 0.2)

            journey_box = FancyBboxPatch(
                (10, 70), 80, 18,
                boxstyle="round,pad=1.5",
                facecolor=self.colors['bg_light'],
                edgecolor=self.colors['accent'],
                linewidth=3,
                alpha=journey_alpha * 0.95
            )
            ax.add_patch(journey_box)

            ax.text(50, 83, 'De Reis van Vraag naar Antwoord',
                    fontsize=26, ha='center', va='center',
                    color=self.colors['accent'],
                    fontweight='bold', alpha=journey_alpha)

            # Journey steps
            journey_steps = [
                ('Vectors', 'Begrijpen wat woorden betekenen'),
                ('RAG', 'Juiste info vinden'),
                ('Finetuning', 'Gedrag aanpassen'),
                ('Kwaliteit', 'Betrouwbaarheid borgen'),
                ('Prompts', 'Effectief communiceren')
            ]

            x_positions = [15, 27, 42, 61, 78]
            for i, (step, desc) in enumerate(journey_steps):
                x = x_positions[i]

                # Step box
                step_box = FancyBboxPatch(
                    (x - 5, 75), 10, 5,
                    boxstyle="round,pad=0.5",
                    facecolor=self.colors['primary'],
                    edgecolor='white',
                    linewidth=2,
                    alpha=journey_alpha * 0.9
                )
                ax.add_patch(step_box)

                ax.text(x, 77.5, step,
                        fontsize=13, ha='center', va='center',
                        color='white',
                        fontweight='bold', alpha=journey_alpha)

                # Arrow (except for last)
                if i < len(journey_steps) - 1:
                    arrow = FancyArrowPatch(
                        (x + 5.5, 77.5), (x_positions[i+1] - 5.5, 77.5),
                        arrowstyle='->', mutation_scale=15,
                        linewidth=2, color=self.colors['dim'],
                        alpha=journey_alpha * 0.6
                    )
                    ax.add_artist(arrow)

        # Why it matters
        if progress > 0.4:
            matters_alpha = min(1.0, (progress - 0.4) / 0.3)

            reasons = [
                {
                    'icon': '>>',
                    'title': 'Praktisch Toepasbaar',
                    'desc': 'Alles wat we bespreken kun je direct gebruiken',
                    'y': 58
                },
                {
                    'icon': '[search]',
                    'title': 'Begrijp de Werking',
                    'desc': 'Weet hoe AI beslissingen maakt',
                    'y': 46
                },
                {
                    'icon': '[!]',
                    'title': 'Beter Resultaat',
                    'desc': 'Krijg betrouwbaardere antwoorden uit AI',
                    'y': 34
                },
                {
                    'icon': '[shield]',
                    'title': 'Risico\'s Herkennen',
                    'desc': 'Weet waar dingen mis kunnen gaan',
                    'y': 22
                }
            ]

            for reason in reasons:
                reason_box = FancyBboxPatch(
                    (12, reason['y'] - 4), 76, 9,
                    boxstyle="round,pad=1",
                    facecolor=self.colors['bg_light'],
                    edgecolor=self.colors['secondary'],
                    linewidth=2,
                    alpha=matters_alpha * 0.9
                )
                ax.add_patch(reason_box)

                ax.text(18, reason['y'], reason['icon'],
                        fontsize=32, ha='center', va='center',
                        alpha=matters_alpha)

                ax.text(28, reason['y'] + 1, reason['title'],
                        fontsize=19, ha='left', va='center',
                        color=self.colors['secondary'],
                        fontweight='bold', alpha=matters_alpha)

                ax.text(28, reason['y'] - 2, reason['desc'],
                        fontsize=15, ha='left', va='center',
                        color=self.colors['text'],
                        alpha=matters_alpha * 0.85)

        # Final message
        if progress > 0.85:
            final_alpha = min(1.0, (progress - 0.85) / 0.15)

            final_box = FancyBboxPatch(
                (10, 5), 80, 10,
                boxstyle="round,pad=1",
                facecolor=self.colors['highlight'],
                edgecolor='white',
                linewidth=3,
                alpha=final_alpha * 0.95
            )
            ax.add_patch(final_box)

            ax.text(50, 10, '[>>] Laten we beginnen!',
                    fontsize=28, ha='center', va='center',
                    color='white',
                    fontweight='bold', alpha=final_alpha)

        self.add_status_indicator(progress < 1.0)
        plt.tight_layout()


def main():
    """Main presentation runner"""
    print("\n" + "="*70)
    print("[grad] AI KENNISSESSIE - INTRODUCTIE")
    print("="*70)
    print("\nVoor Hogeschool Professionals")
    print("\nStappen:")
    print("  1. Welkom")
    print("  2. Over Mezelf")
    print("  3. Wat We Al Weten Over AI")
    print("  4. AI voor Informatieverwerking")
    print("  5. Waarom Kwaliteit Belangrijk Is")
    print("  6. Wat Gaan We Bespreken?")
    print("  7. Waarom Deze Onderwerpen?")
    print("\n[Keys]  SPACE=Next | B=Previous | R=Reset | Q=Quit")
    print("="*70 + "\n")

    presentation = IntroHogeschoolPresentation()
    presentation.show()


if __name__ == "__main__":
    main()
