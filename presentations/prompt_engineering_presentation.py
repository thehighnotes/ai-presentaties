"""
Prompt Engineering
Leer hoe je effectief communiceert met AI systemen
"""

import sys
import os
import numpy as np
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle
import matplotlib.pyplot as plt

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core import BasePresentation, PresentationStyle


class PromptEngineeringPresentation(BasePresentation):
    """Prompt Engineering"""

    def __init__(self):
        """Initialize the presentation"""
        step_names = [
            'Landing',
            'Wat is Prompt Engineering?',
            'Waarom is het Belangrijk?',
            'Anatomie van een Goede Prompt',
            'Techniek 1: Clear Instructions',
            'Techniek 2: Few-Shot Learning',
            'Techniek 3: Chain-of-Thought',
            'Techniek 4: Role Playing',
            'Veelvoorkomende Valkuilen',
            'Best Practices Checklist'
        ]

        super().__init__("Prompt Engineering", step_names)

        self.show_landing_page()

    def get_frames_for_step(self, step: int) -> int:
        """Get animation frame count for each step"""
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
            edgecolor=self.colors['secondary'],
            linewidth=4,
            alpha=0.95
        )
        ax.add_patch(title_box)

        ax.text(50, 72, 'Prompt Engineering',
                fontsize=66, fontweight='bold', ha='center', va='center',
                color=self.colors['secondary'])

        ax.text(50, 64, 'De Kunst van AI Communicatie',
                fontsize=30, ha='center', va='center',
                color=self.colors['text'], alpha=0.8, style='italic')

        ax.text(30, 67, '[chat]', fontsize=75, ha='center', va='center')

        ax.text(70, 67, '[AI]', fontsize=75, ha='center', va='center')

        ax.text(50, 45, 'Leer hoe je betere resultaten krijgt uit AI',
                fontsize=27, ha='center', va='center',
                color=self.colors['accent'], alpha=0.9)

        # Instructions box
        instr_box = FancyBboxPatch(
            (25, 15), 50, 15,
            boxstyle="round,pad=1",
            facecolor=self.colors['bg_light'],
            edgecolor=self.colors['secondary'],
            linewidth=3,
            alpha=0.9
        )
        ax.add_patch(instr_box)

        ax.text(50, 25, '>> Druk op SPATIE om te beginnen <<',
                fontsize=30, ha='center', va='center',
                color=self.colors['secondary'], fontweight='bold')

        ax.text(50, 20, 'SPACE=Volgende | B=Vorige | R=Reset | Q=Afsluiten',
                fontsize=18, ha='center', va='center',
                color=self.colors['dim'], style='italic')

        ax.text(50, 5, 'Van vage vragen naar concrete resultaten',
                fontsize=21, ha='center', va='center',
                color=self.colors['text'], alpha=0.5)

        plt.tight_layout()

    def animate_step(self, frame: int):
        """Animate current step"""
        total_frames = self.get_frames_for_step(self.current_step)
        progress = frame / (total_frames - 1) if total_frames > 1 else 1

        if self.current_step == 0:
            pass  # Landing is static
        elif self.current_step == 1:
            self.draw_wat_is_prompt_engineering(progress)
        elif self.current_step == 2:
            self.draw_waarom_is_het_belangrijk(progress)
        elif self.current_step == 3:
            self.draw_anatomie_van_een_goede_prompt(progress)
        elif self.current_step == 4:
            self.draw_techniek_1_clear_instructions(progress)
        elif self.current_step == 5:
            self.draw_techniek_2_few_shot_learning(progress)
        elif self.current_step == 6:
            self.draw_techniek_3_chain_of_thought(progress)
        elif self.current_step == 7:
            self.draw_techniek_4_role_playing(progress)
        elif self.current_step == 8:
            self.draw_veelvoorkomende_valkuilen(progress)
        elif self.current_step == 9:
            self.draw_best_practices_checklist(progress)

        if frame >= total_frames - 1:
            self.is_animating = False

    def draw_current_step_static(self):
        """Draw current step without animation"""
        if self.current_step == -1:
            self.show_landing_page()
        elif self.current_step == 1:
            self.draw_wat_is_prompt_engineering(1.0)
        elif self.current_step == 2:
            self.draw_waarom_is_het_belangrijk(1.0)
        elif self.current_step == 3:
            self.draw_anatomie_van_een_goede_prompt(1.0)
        elif self.current_step == 4:
            self.draw_techniek_1_clear_instructions(1.0)
        elif self.current_step == 5:
            self.draw_techniek_2_few_shot_learning(1.0)
        elif self.current_step == 6:
            self.draw_techniek_3_chain_of_thought(1.0)
        elif self.current_step == 7:
            self.draw_techniek_4_role_playing(1.0)
        elif self.current_step == 8:
            self.draw_veelvoorkomende_valkuilen(1.0)
        elif self.current_step == 9:
            self.draw_best_practices_checklist(1.0)
        plt.draw()

    def draw_wat_is_prompt_engineering(self, progress: float):
        """Step 1: Wat is Prompt Engineering?"""
        self.fig.clear()
        ax = self.fig.add_subplot(111)
        ax.axis('off')
        ax.set_xlim(0, 100)
        ax.set_ylim(0, 100)

        # Title
        title_alpha = min(1.0, progress / 0.2)
        ax.text(50, 95, 'Wat is Prompt Engineering?',
                fontsize=45, fontweight='bold', ha='center', va='top',
                color=self.colors['primary'], alpha=title_alpha)

        if progress > 0.2:
            box_alpha = min(1.0, (progress - 0.2) / 0.2)

            box = FancyBboxPatch(
                (15.0, 70.0), 70, 15,
                boxstyle="round,pad=1",
                facecolor=self.colors['bg_light'],
                edgecolor=self.colors['primary'],
                linewidth=3,
                alpha=0.95 * box_alpha
            )
            ax.add_patch(box)

            ax.text(50, 73.75, 'Prompt Engineering is de kunst en wetenschap van het formuleren van effectieve instructies voor AI-modellen om optimale resultaten te krijgen.',
                    fontsize=18, ha='center', va='center',
                    color=self.colors['text'], alpha=box_alpha * 0.9)

        # Flow step 1
        if progress > 0.40:
            step_alpha = min(1.0, (progress - 0.40) / 0.07)

            step_box = FancyBboxPatch(
                (17.0, 38), 19.333333333333332, 24,
                boxstyle="round,pad=0.5",
                facecolor=self.colors['bg_light'],
                edgecolor=self.colors['accent'],
                linewidth=2,
                alpha=0.95 * step_alpha
            )
            ax.add_patch(step_box)

            ax.text(26.666666666666664, 56, '📝',
                    fontsize=30, ha='center', va='center', alpha=step_alpha)
            ax.text(26.666666666666664, 48, 'Jouw Prompt',
                    fontsize=18, fontweight='bold', ha='center', va='center',
                    color=self.colors['accent'], alpha=step_alpha)
            ax.text(26.666666666666664, 42, '',
                    fontsize=14, ha='center', va='center',
                    color=self.colors['text'], alpha=step_alpha * 0.7)

            if progress > 0.43:
                ax.annotate('', xy=(41.33333333333333, 50), xytext=(37.33333333333333, 50),
                           arrowprops=dict(arrowstyle='->', color=self.colors['dim'],
                                          lw=2), alpha=step_alpha)

        # Flow step 2
        if progress > 0.47:
            step_alpha = min(1.0, (progress - 0.47) / 0.07)

            step_box = FancyBboxPatch(
                (40.333333333333336, 38), 19.333333333333332, 24,
                boxstyle="round,pad=0.5",
                facecolor=self.colors['bg_light'],
                edgecolor=self.colors['primary'],
                linewidth=2,
                alpha=0.95 * step_alpha
            )
            ax.add_patch(step_box)

            ax.text(50.0, 56, '⚙️',
                    fontsize=30, ha='center', va='center', alpha=step_alpha)
            ax.text(50.0, 48, 'AI Verwerking',
                    fontsize=18, fontweight='bold', ha='center', va='center',
                    color=self.colors['primary'], alpha=step_alpha)
            ax.text(50.0, 42, '',
                    fontsize=14, ha='center', va='center',
                    color=self.colors['text'], alpha=step_alpha * 0.7)

            if progress > 0.50:
                ax.annotate('', xy=(64.66666666666666, 50), xytext=(60.666666666666664, 50),
                           arrowprops=dict(arrowstyle='->', color=self.colors['dim'],
                                          lw=2), alpha=step_alpha)

        # Flow step 3
        if progress > 0.53:
            step_alpha = min(1.0, (progress - 0.53) / 0.07)

            step_box = FancyBboxPatch(
                (63.666666666666664, 38), 19.333333333333332, 24,
                boxstyle="round,pad=0.5",
                facecolor=self.colors['bg_light'],
                edgecolor=self.colors['secondary'],
                linewidth=2,
                alpha=0.95 * step_alpha
            )
            ax.add_patch(step_box)

            ax.text(73.33333333333333, 56, '*',
                    fontsize=30, ha='center', va='center', alpha=step_alpha)
            ax.text(73.33333333333333, 48, 'Resultaat',
                    fontsize=18, fontweight='bold', ha='center', va='center',
                    color=self.colors['secondary'], alpha=step_alpha)
            ax.text(73.33333333333333, 42, '',
                    fontsize=14, ha='center', va='center',
                    color=self.colors['text'], alpha=step_alpha * 0.7)

        if progress > 0.8:
            box_alpha = min(1.0, (progress - 0.8) / 0.19999999999999996)

            box = FancyBboxPatch(
                (15.0, 19.5), 70, 15,
                boxstyle="round,pad=1",
                facecolor=self.colors['bg_light'],
                edgecolor=self.colors['highlight'],
                linewidth=3,
                alpha=0.95 * box_alpha
            )
            ax.add_patch(box)

            ax.text(50, 30.75, '[!] De kwaliteit van je prompt bepaalt de kwaliteit van het resultaat',
                    fontsize=24, fontweight='bold', ha='center', va='center',
                    color=self.colors['highlight'], alpha=box_alpha)

            ax.text(50, 23.25, 'Betere prompts = Betere antwoorden',
                    fontsize=18, ha='center', va='center',
                    color=self.colors['text'], alpha=box_alpha * 0.9)

        self.add_status_indicator(progress < 1.0)

    def draw_waarom_is_het_belangrijk(self, progress: float):
        """Step 2: Waarom is het Belangrijk?"""
        self.fig.clear()
        ax = self.fig.add_subplot(111)
        ax.axis('off')
        ax.set_xlim(0, 100)
        ax.set_ylim(0, 100)

        # Title
        title_alpha = min(1.0, progress / 0.2)
        ax.text(50, 95, 'Waarom is het Belangrijk?',
                fontsize=45, fontweight='bold', ha='center', va='top',
                color=self.colors['primary'], alpha=title_alpha)

        # Comparison: Left (before/bad)
        if progress > 0.2:
            left_alpha = min(1.0, (progress - 0.2) / 0.1)

            left_box = FancyBboxPatch(
                (10.0, 57.5), 35.0, 25,
                boxstyle="round,pad=1",
                facecolor=self.colors['bg_light'],
                edgecolor=self.colors['warning'],
                linewidth=3,
                alpha=0.95 * left_alpha
            )
            ax.add_patch(left_box)

            ax.text(27.5, 76.25, '✗ Vage Prompt',
                    fontsize=24, fontweight='bold', ha='center', va='center',
                    color=self.colors['warning'], alpha=left_alpha)

            ax.text(27.5, 63.75, '"Schrijf iets over AI"\n→ Algemeen\n→ Niet bruikbaar\n→ Frustrerend',
                    fontsize=18, ha='center', va='center',
                    color=self.colors['text'], alpha=left_alpha * 0.9)

        # Comparison: Right (after/good)
        if progress > 0.30000000000000004:
            right_alpha = min(1.0, (progress - 0.30000000000000004) / 0.1)

            right_box = FancyBboxPatch(
                (55.0, 57.5), 35.0, 25,
                boxstyle="round,pad=1",
                facecolor=self.colors['bg_light'],
                edgecolor=self.colors['secondary'],
                linewidth=3,
                alpha=0.95 * right_alpha
            )
            ax.add_patch(right_box)

            ax.text(72.5, 76.25, '✓ Specifieke Prompt',
                    fontsize=24, fontweight='bold', ha='center', va='center',
                    color=self.colors['secondary'], alpha=right_alpha)

            ax.text(72.5, 63.75, '"Leg uit hoe RAG werkt..."\n→ Specifiek\n→ Direct bruikbaar\n→ Efficiënt',
                    fontsize=18, ha='center', va='center',
                    color=self.colors['text'], alpha=right_alpha * 0.9)

        if progress > 0.40:
            item_alpha = min(1.0, (progress - 0.40) / 0.05)
            ax.text(20, 40, '• ⏱️ Bespaart tijd',
                    fontsize=21, ha='left', va='center',
                    color=self.colors['text'], alpha=item_alpha)

        if progress > 0.45:
            item_alpha = min(1.0, (progress - 0.45) / 0.05)
            ax.text(20, 33, '• >> Betere resultaten',
                    fontsize=21, ha='left', va='center',
                    color=self.colors['text'], alpha=item_alpha)

        if progress > 0.50:
            item_alpha = min(1.0, (progress - 0.50) / 0.05)
            ax.text(20, 26, '• 💰 Lagere kosten',
                    fontsize=21, ha='left', va='center',
                    color=self.colors['text'], alpha=item_alpha)

        if progress > 0.55:
            item_alpha = min(1.0, (progress - 0.55) / 0.05)
            ax.text(20, 19, '• [>>] Meer productiviteit',
                    fontsize=21, ha='left', va='center',
                    color=self.colors['text'], alpha=item_alpha)

        if progress > 0.8:
            text_alpha = min(1.0, (progress - 0.8) / 0.19999999999999996)
            ax.text(50, 8, '[i] Goede prompts kunnen het verschil maken tussen nutteloos en onmisbaar',
                    fontsize=18, fontweight='bold',
                    ha='center', va='center',
                    color=self.colors['accent'], alpha=text_alpha)

        self.add_status_indicator(progress < 1.0)

    def draw_anatomie_van_een_goede_prompt(self, progress: float):
        """Step 3: Anatomie van een Goede Prompt"""
        self.fig.clear()
        ax = self.fig.add_subplot(111)
        ax.axis('off')
        ax.set_xlim(0, 100)
        ax.set_ylim(0, 100)

        # Title
        title_alpha = min(1.0, progress / 0.2)
        ax.text(50, 95, 'Anatomie van een Goede Prompt',
                fontsize=45, fontweight='bold', ha='center', va='top',
                color=self.colors['primary'], alpha=title_alpha)

        # Stacked box 1
        if progress > 0.20:
            stack_alpha = min(1.0, (progress - 0.20) / 0.04)

            stack_box = FancyBboxPatch(
                (15.0, 86.5), 70, 12,
                boxstyle="round,pad=0.8",
                facecolor=self.colors['bg_light'],
                edgecolor=self.colors['accent'],
                linewidth=3,
                alpha=0.95 * stack_alpha
            )
            ax.add_patch(stack_box)

            ax.text(50, 94.5, 'Context',
                    fontsize=21, fontweight='bold', ha='center', va='center',
                    color=self.colors['accent'], alpha=stack_alpha)
            ax.text(50, 90.5, 'Achtergrond informatie',
                    fontsize=14, ha='center', va='center',
                    color=self.colors['text'], alpha=stack_alpha * 0.8)

        # Stacked box 2
        if progress > 0.24:
            stack_alpha = min(1.0, (progress - 0.24) / 0.04)

            stack_box = FancyBboxPatch(
                (17.0, 71.5), 66, 12,
                boxstyle="round,pad=0.8",
                facecolor=self.colors['bg_light'],
                edgecolor=self.colors['primary'],
                linewidth=3,
                alpha=0.95 * stack_alpha
            )
            ax.add_patch(stack_box)

            ax.text(50, 79.5, 'Instructie',
                    fontsize=21, fontweight='bold', ha='center', va='center',
                    color=self.colors['primary'], alpha=stack_alpha)
            ax.text(50, 75.5, 'Wat moet er gebeuren',
                    fontsize=14, ha='center', va='center',
                    color=self.colors['text'], alpha=stack_alpha * 0.8)

        # Stacked box 3
        if progress > 0.28:
            stack_alpha = min(1.0, (progress - 0.28) / 0.04)

            stack_box = FancyBboxPatch(
                (19.0, 56.5), 62, 12,
                boxstyle="round,pad=0.8",
                facecolor=self.colors['bg_light'],
                edgecolor=self.colors['secondary'],
                linewidth=3,
                alpha=0.95 * stack_alpha
            )
            ax.add_patch(stack_box)

            ax.text(50, 64.5, 'Format',
                    fontsize=21, fontweight='bold', ha='center', va='center',
                    color=self.colors['secondary'], alpha=stack_alpha)
            ax.text(50, 60.5, 'Gewenste output vorm',
                    fontsize=14, ha='center', va='center',
                    color=self.colors['text'], alpha=stack_alpha * 0.8)

        # Stacked box 4
        if progress > 0.32:
            stack_alpha = min(1.0, (progress - 0.32) / 0.04)

            stack_box = FancyBboxPatch(
                (21.0, 41.5), 58, 12,
                boxstyle="round,pad=0.8",
                facecolor=self.colors['bg_light'],
                edgecolor=self.colors['purple'],
                linewidth=3,
                alpha=0.95 * stack_alpha
            )
            ax.add_patch(stack_box)

            ax.text(50, 49.5, 'Voorbeelden',
                    fontsize=21, fontweight='bold', ha='center', va='center',
                    color=self.colors['purple'], alpha=stack_alpha)
            ax.text(50, 45.5, 'Concrete samples (optioneel)',
                    fontsize=14, ha='center', va='center',
                    color=self.colors['text'], alpha=stack_alpha * 0.8)

        # Stacked box 5
        if progress > 0.36:
            stack_alpha = min(1.0, (progress - 0.36) / 0.04)

            stack_box = FancyBboxPatch(
                (23.0, 26.5), 54, 12,
                boxstyle="round,pad=0.8",
                facecolor=self.colors['bg_light'],
                edgecolor=self.colors['warning'],
                linewidth=3,
                alpha=0.95 * stack_alpha
            )
            ax.add_patch(stack_box)

            ax.text(50, 34.5, 'Beperkingen',
                    fontsize=21, fontweight='bold', ha='center', va='center',
                    color=self.colors['warning'], alpha=stack_alpha)
            ax.text(50, 30.5, 'Wat NIET te doen (optioneel)',
                    fontsize=14, ha='center', va='center',
                    color=self.colors['text'], alpha=stack_alpha * 0.8)

        if progress > 0.8:
            text_alpha = min(1.0, (progress - 0.8) / 0.19999999999999996)
            ax.text(50, 8, '[→] Volgende slides: Deze componenten in actie!',
                    fontsize=18, fontweight='bold',
                    ha='center', va='center',
                    color=self.colors['highlight'], alpha=text_alpha)

        self.add_status_indicator(progress < 1.0)

    def draw_techniek_1_clear_instructions(self, progress: float):
        """Step 4: Techniek 1: Clear Instructions"""
        self.fig.clear()
        ax = self.fig.add_subplot(111)
        ax.axis('off')
        ax.set_xlim(0, 100)
        ax.set_ylim(0, 100)

        # Title
        title_alpha = min(1.0, progress / 0.2)
        ax.text(50, 95, 'Techniek 1: Clear Instructions',
                fontsize=45, fontweight='bold', ha='center', va='top',
                color=self.colors['primary'], alpha=title_alpha)

        if progress > 0.1:
            sub_alpha = min(1.0, (progress - 0.1) / 0.2)
            ax.text(50, 88, 'Wees specifiek, duidelijk, en direct',
                    fontsize=24, ha='center', va='top',
                    color=self.colors['text'], alpha=sub_alpha * 0.8, style='italic')

        # Comparison: Left (before/bad)
        if progress > 0.2:
            left_alpha = min(1.0, (progress - 0.2) / 0.1)

            left_box = FancyBboxPatch(
                (7.5, 53.0), 37.5, 28,
                boxstyle="round,pad=1",
                facecolor=self.colors['bg_light'],
                edgecolor=self.colors['warning'],
                linewidth=3,
                alpha=0.95 * left_alpha
            )
            ax.add_patch(left_box)

            ax.text(26.25, 74.0, '[X] Vaag',
                    fontsize=24, fontweight='bold', ha='center', va='center',
                    color=self.colors['warning'], alpha=left_alpha)

            ax.text(26.25, 60.0, '"Maak een email"',
                    fontsize=18, ha='center', va='center',
                    color=self.colors['text'], alpha=left_alpha * 0.9)

        # Comparison: Right (after/good)
        if progress > 0.30000000000000004:
            right_alpha = min(1.0, (progress - 0.30000000000000004) / 0.1)

            right_box = FancyBboxPatch(
                (55.0, 53.0), 37.5, 28,
                boxstyle="round,pad=1",
                facecolor=self.colors['bg_light'],
                edgecolor=self.colors['secondary'],
                linewidth=3,
                alpha=0.95 * right_alpha
            )
            ax.add_patch(right_box)

            ax.text(73.75, 74.0, '[OK] Specifiek',
                    fontsize=24, fontweight='bold', ha='center', va='center',
                    color=self.colors['secondary'], alpha=right_alpha)

            ax.text(73.75, 60.0, '"Schrijf een professionele email naar een klant om een meeting te verzetten naar volgende week. Wees beleefd, bied excuses aan, en stel 3 alternatieve tijden voor."',
                    fontsize=18, ha='center', va='center',
                    color=self.colors['text'], alpha=right_alpha * 0.9)

        if progress > 0.60:
            item_alpha = min(1.0, (progress - 0.60) / 0.05)
            ax.text(20, 32, '• 1. Specificeer de taak precies',
                    fontsize=21, ha='left', va='center',
                    color=self.colors['text'], alpha=item_alpha)

        if progress > 0.65:
            item_alpha = min(1.0, (progress - 0.65) / 0.05)
            ax.text(20, 26, '• 2. Geef context en doel aan',
                    fontsize=21, ha='left', va='center',
                    color=self.colors['text'], alpha=item_alpha)

        if progress > 0.70:
            item_alpha = min(1.0, (progress - 0.70) / 0.05)
            ax.text(20, 20, '• 3. Definieer gewenste lengte/format',
                    fontsize=21, ha='left', va='center',
                    color=self.colors['text'], alpha=item_alpha)

        if progress > 0.75:
            item_alpha = min(1.0, (progress - 0.75) / 0.05)
            ax.text(20, 14, '• 4. Vermeld toon en stijl',
                    fontsize=21, ha='left', va='center',
                    color=self.colors['text'], alpha=item_alpha)

        if progress > 0.8:
            text_alpha = min(1.0, (progress - 0.8) / 0.19999999999999996)
            ax.text(50, 8, '[[i]] Hoe specifieker, hoe beter het resultaat',
                    fontsize=18, fontweight='bold',
                    ha='center', va='center',
                    color=self.colors['accent'], alpha=text_alpha)

        self.add_status_indicator(progress < 1.0)

    def draw_techniek_2_few_shot_learning(self, progress: float):
        """Step 5: Techniek 2: Few-Shot Learning"""
        self.fig.clear()
        ax = self.fig.add_subplot(111)
        ax.axis('off')
        ax.set_xlim(0, 100)
        ax.set_ylim(0, 100)

        # Title
        title_alpha = min(1.0, progress / 0.2)
        ax.text(50, 95, 'Techniek 2: Few-Shot Learning',
                fontsize=45, fontweight='bold', ha='center', va='top',
                color=self.colors['primary'], alpha=title_alpha)

        if progress > 0.1:
            sub_alpha = min(1.0, (progress - 0.1) / 0.2)
            ax.text(50, 88, 'Geef voorbeelden van wat je wilt',
                    fontsize=24, ha='center', va='top',
                    color=self.colors['text'], alpha=sub_alpha * 0.8, style='italic')

        if progress > 0.2:
            code_alpha = min(1.0, (progress - 0.2) / 0.2)

            code_box = FancyBboxPatch(
                (10.0, 60.0), 80, 22,
                boxstyle="round,pad=0.5",
                facecolor='#1a1a2e',
                edgecolor=self.colors['dim'],
                linewidth=2,
                alpha=0.95 * code_alpha
            )
            ax.add_patch(code_box)

            code_text = 'Vertaal naar beleefd Nederlands:\n\nVoorbeeld 1:\nInput: "give me the report"\nOutput: "Zou je mij het rapport kunnen toesturen?"\n\nVoorbeeld 2:\nInput: "send it now"\nOutput: "Kun je het zo spoedig mogelijk versturen?"\n\nNu jouw beurt:\nInput: "call me back"\nOutput: ?'
            ax.text(50, 71, code_text,
                    fontsize=14, family='monospace', ha='center', va='center',
                    color='#a8ff60', alpha=code_alpha)

        if progress > 0.40:
            item_alpha = min(1.0, (progress - 0.40) / 0.20)
            ax.text(20, 45, '• ✓ Model leert het patroon',
                    fontsize=21, ha='left', va='center',
                    color=self.colors['text'], alpha=item_alpha)

        if progress > 0.40:
            item_alpha = min(1.0, (progress - 0.40) / 0.20)
            ax.text(20, 40, '• ✓ Consistente output',
                    fontsize=21, ha='left', va='center',
                    color=self.colors['text'], alpha=item_alpha)

        if progress > 0.40:
            item_alpha = min(1.0, (progress - 0.40) / 0.20)
            ax.text(20, 35, '• ✓ Minder uitleg nodig',
                    fontsize=21, ha='left', va='center',
                    color=self.colors['text'], alpha=item_alpha)

        if progress > 0.6:
            box_alpha = min(1.0, (progress - 0.6) / 0.20000000000000007)

            box = FancyBboxPatch(
                (15.0, 15.0), 70, 15,
                boxstyle="round,pad=1",
                facecolor=self.colors['bg_light'],
                edgecolor=self.colors['accent'],
                linewidth=3,
                alpha=0.95 * box_alpha
            )
            ax.add_patch(box)

            ax.text(50, 26.25, 'Perfect voor:',
                    fontsize=24, fontweight='bold', ha='center', va='center',
                    color=self.colors['accent'], alpha=box_alpha)

            ax.text(50, 18.75, 'Vertalingen • Classificaties • Format conversies • Data extractie',
                    fontsize=18, ha='center', va='center',
                    color=self.colors['text'], alpha=box_alpha * 0.9)

        self.add_status_indicator(progress < 1.0)

    def draw_techniek_3_chain_of_thought(self, progress: float):
        """Step 6: Techniek 3: Chain-of-Thought"""
        self.fig.clear()
        ax = self.fig.add_subplot(111)
        ax.axis('off')
        ax.set_xlim(0, 100)
        ax.set_ylim(0, 100)

        # Title
        title_alpha = min(1.0, progress / 0.2)
        ax.text(50, 95, 'Techniek 3: Chain-of-Thought',
                fontsize=45, fontweight='bold', ha='center', va='top',
                color=self.colors['primary'], alpha=title_alpha)

        if progress > 0.1:
            sub_alpha = min(1.0, (progress - 0.1) / 0.2)
            ax.text(50, 88, 'Laat AI stap-voor-stap denken',
                    fontsize=24, ha='center', va='top',
                    color=self.colors['text'], alpha=sub_alpha * 0.8, style='italic')

        # Comparison: Left (before/bad)
        if progress > 0.2:
            left_alpha = min(1.0, (progress - 0.2) / 0.1)

            left_box = FancyBboxPatch(
                (7.5, 59.0), 37.5, 22,
                boxstyle="round,pad=1",
                facecolor=self.colors['bg_light'],
                edgecolor=self.colors['warning'],
                linewidth=3,
                alpha=0.95 * left_alpha
            )
            ax.add_patch(left_box)

            ax.text(26.25, 75.5, '[!] Direct',
                    fontsize=24, fontweight='bold', ha='center', va='center',
                    color=self.colors['warning'], alpha=left_alpha)

            ax.text(26.25, 64.5, '"Wat is 37 x 24?"\n→ Vaak fout bij complexe vragen',
                    fontsize=18, ha='center', va='center',
                    color=self.colors['text'], alpha=left_alpha * 0.9)

        # Comparison: Right (after/good)
        if progress > 0.30000000000000004:
            right_alpha = min(1.0, (progress - 0.30000000000000004) / 0.1)

            right_box = FancyBboxPatch(
                (55.0, 59.0), 37.5, 22,
                boxstyle="round,pad=1",
                facecolor=self.colors['bg_light'],
                edgecolor=self.colors['purple'],
                linewidth=3,
                alpha=0.95 * right_alpha
            )
            ax.add_patch(right_box)

            ax.text(73.75, 75.5, '🧠 Chain-of-Thought',
                    fontsize=24, fontweight='bold', ha='center', va='center',
                    color=self.colors['purple'], alpha=right_alpha)

            ax.text(73.75, 64.5, '"Wat is 37 x 24? Laat je redenering zien stap voor stap voordat je het antwoord geeft."\n→ Veel accurater voor complexe taken',
                    fontsize=18, ha='center', va='center',
                    color=self.colors['text'], alpha=right_alpha * 0.9)

        if progress > 0.40:
            item_alpha = min(1.0, (progress - 0.40) / 0.05)
            ax.text(20, 38, '• 🧮 Wiskunde & berekeningen',
                    fontsize=21, ha='left', va='center',
                    color=self.colors['text'], alpha=item_alpha)

        if progress > 0.45:
            item_alpha = min(1.0, (progress - 0.45) / 0.05)
            ax.text(20, 32, '• 🤔 Logische redeneringen',
                    fontsize=21, ha='left', va='center',
                    color=self.colors['text'], alpha=item_alpha)

        if progress > 0.50:
            item_alpha = min(1.0, (progress - 0.50) / 0.05)
            ax.text(20, 26, '• [list] Meerstaps problemen',
                    fontsize=21, ha='left', va='center',
                    color=self.colors['text'], alpha=item_alpha)

        if progress > 0.55:
            item_alpha = min(1.0, (progress - 0.55) / 0.05)
            ax.text(20, 20, '• [search] Analyse taken',
                    fontsize=21, ha='left', va='center',
                    color=self.colors['text'], alpha=item_alpha)

        if progress > 0.8:
            box_alpha = min(1.0, (progress - 0.8) / 0.19999999999999996)

            box = FancyBboxPatch(
                (15.0, 8.0), 70, 10,
                boxstyle="round,pad=1",
                facecolor=self.colors['bg_light'],
                edgecolor=self.colors['highlight'],
                linewidth=3,
                alpha=0.95 * box_alpha
            )
            ax.add_patch(box)

            ax.text(50, 15.5, '* Magic phrase: "Let\'s think step by step"',
                    fontsize=24, fontweight='bold', ha='center', va='center',
                    color=self.colors['highlight'], alpha=box_alpha)

        self.add_status_indicator(progress < 1.0)

    def draw_techniek_4_role_playing(self, progress: float):
        """Step 7: Techniek 4: Role Playing"""
        self.fig.clear()
        ax = self.fig.add_subplot(111)
        ax.axis('off')
        ax.set_xlim(0, 100)
        ax.set_ylim(0, 100)

        # Title
        title_alpha = min(1.0, progress / 0.2)
        ax.text(50, 95, 'Techniek 4: Role Playing',
                fontsize=45, fontweight='bold', ha='center', va='top',
                color=self.colors['primary'], alpha=title_alpha)

        if progress > 0.1:
            sub_alpha = min(1.0, (progress - 0.1) / 0.2)
            ax.text(50, 88, 'Geef AI een specifieke rol of persona',
                    fontsize=24, ha='center', va='top',
                    color=self.colors['text'], alpha=sub_alpha * 0.8, style='italic')

        # Grid item 1
        if progress > 0.20:
            item_alpha = min(1.0, (progress - 0.20) / 0.04)

            grid_box = FancyBboxPatch(
                (-3.0, 61.0), 34, 12,
                boxstyle="round,pad=0.8",
                facecolor=self.colors['bg_light'],
                edgecolor=self.colors['primary'],
                linewidth=2,
                alpha=0.9 * item_alpha
            )
            ax.add_patch(grid_box)

            ax.text(14.0, 70.5, '👨‍🏫',
                    fontsize=30, ha='center', va='center', alpha=item_alpha)
            ax.text(14.0, 67.0, 'Expert Leraar',
                    fontsize=15, fontweight='bold', ha='center', va='center',
                    color=self.colors['primary'], alpha=item_alpha)
            ax.text(14.0, 63.5, 'Leg uit alsof ik 10 jaar oud ben',
                    fontsize=11, ha='center', va='center',
                    color=self.colors['text'], alpha=item_alpha * 0.8,
                    linespacing=1.3)

        # Grid item 2
        if progress > 0.24:
            item_alpha = min(1.0, (progress - 0.24) / 0.04)

            grid_box = FancyBboxPatch(
                (33.0, 61.0), 34, 12,
                boxstyle="round,pad=0.8",
                facecolor=self.colors['bg_light'],
                edgecolor=self.colors['secondary'],
                linewidth=2,
                alpha=0.9 * item_alpha
            )
            ax.add_patch(grid_box)

            ax.text(50.0, 70.5, '[work]',
                    fontsize=30, ha='center', va='center', alpha=item_alpha)
            ax.text(50.0, 67.0, 'Business Consultant',
                    fontsize=15, fontweight='bold', ha='center', va='center',
                    color=self.colors['secondary'], alpha=item_alpha)
            ax.text(50.0, 63.5, 'Analyseer deze data strategisch',
                    fontsize=11, ha='center', va='center',
                    color=self.colors['text'], alpha=item_alpha * 0.8,
                    linespacing=1.3)

        # Grid item 3
        if progress > 0.28:
            item_alpha = min(1.0, (progress - 0.28) / 0.04)

            grid_box = FancyBboxPatch(
                (69.0, 61.0), 34, 12,
                boxstyle="round,pad=0.8",
                facecolor=self.colors['bg_light'],
                edgecolor=self.colors['purple'],
                linewidth=2,
                alpha=0.9 * item_alpha
            )
            ax.add_patch(grid_box)

            ax.text(86.0, 70.5, '👨‍[PC]',
                    fontsize=30, ha='center', va='center', alpha=item_alpha)
            ax.text(86.0, 67.0, 'Senior Developer',
                    fontsize=15, fontweight='bold', ha='center', va='center',
                    color=self.colors['purple'], alpha=item_alpha)
            ax.text(86.0, 63.5, 'Review deze code kritisch',
                    fontsize=11, ha='center', va='center',
                    color=self.colors['text'], alpha=item_alpha * 0.8,
                    linespacing=1.3)

        # Grid item 4
        if progress > 0.32:
            item_alpha = min(1.0, (progress - 0.32) / 0.04)

            grid_box = FancyBboxPatch(
                (-3.0, 47.0), 34, 12,
                boxstyle="round,pad=0.8",
                facecolor=self.colors['bg_light'],
                edgecolor=self.colors['accent'],
                linewidth=2,
                alpha=0.9 * item_alpha
            )
            ax.add_patch(grid_box)

            ax.text(14.0, 56.5, '[edit]',
                    fontsize=30, ha='center', va='center', alpha=item_alpha)
            ax.text(14.0, 53.0, 'Professioneel Schrijver',
                    fontsize=15, fontweight='bold', ha='center', va='center',
                    color=self.colors['accent'], alpha=item_alpha)
            ax.text(14.0, 49.5, 'Schrijf in journalistieke stijl',
                    fontsize=11, ha='center', va='center',
                    color=self.colors['text'], alpha=item_alpha * 0.8,
                    linespacing=1.3)

        # Grid item 5
        if progress > 0.36:
            item_alpha = min(1.0, (progress - 0.36) / 0.04)

            grid_box = FancyBboxPatch(
                (33.0, 47.0), 34, 12,
                boxstyle="round,pad=0.8",
                facecolor=self.colors['bg_light'],
                edgecolor=self.colors['highlight'],
                linewidth=2,
                alpha=0.9 * item_alpha
            )
            ax.add_patch(grid_box)

            ax.text(50.0, 56.5, '🤝',
                    fontsize=30, ha='center', va='center', alpha=item_alpha)
            ax.text(50.0, 53.0, 'Empathische Coach',
                    fontsize=15, fontweight='bold', ha='center', va='center',
                    color=self.colors['highlight'], alpha=item_alpha)
            ax.text(50.0, 49.5, 'Geef constructieve feedback',
                    fontsize=11, ha='center', va='center',
                    color=self.colors['text'], alpha=item_alpha * 0.8,
                    linespacing=1.3)

        if progress > 0.6:
            box_alpha = min(1.0, (progress - 0.6) / 0.20000000000000007)

            box = FancyBboxPatch(
                (10.0, 18.0), 80, 18,
                boxstyle="round,pad=1",
                facecolor=self.colors['bg_light'],
                edgecolor=self.colors['accent'],
                linewidth=3,
                alpha=0.95 * box_alpha
            )
            ax.add_patch(box)

            ax.text(50, 31.5, '📝 Voorbeeld Template:',
                    fontsize=24, fontweight='bold', ha='center', va='center',
                    color=self.colors['accent'], alpha=box_alpha)

            ax.text(50, 22.5, 'Je bent een [ROL] met [X] jaar ervaring. Je specialiteit is [EXPERTISE]. Help me met: [TAAK]',
                    fontsize=18, ha='center', va='center',
                    color=self.colors['text'], alpha=box_alpha * 0.9)

        if progress > 0.8:
            text_alpha = min(1.0, (progress - 0.8) / 0.19999999999999996)
            ax.text(50, 8, '[[i]] Rollen activeren specifieke kennis en stijlen in het model',
                    fontsize=16, fontweight='bold',
                    ha='center', va='center',
                    color=self.colors['highlight'], alpha=text_alpha)

        self.add_status_indicator(progress < 1.0)

    def draw_veelvoorkomende_valkuilen(self, progress: float):
        """Step 8: Veelvoorkomende Valkuilen"""
        self.fig.clear()
        ax = self.fig.add_subplot(111)
        ax.axis('off')
        ax.set_xlim(0, 100)
        ax.set_ylim(0, 100)

        # Title
        title_alpha = min(1.0, progress / 0.2)
        ax.text(50, 95, 'Veelvoorkomende Valkuilen',
                fontsize=45, fontweight='bold', ha='center', va='top',
                color=self.colors['primary'], alpha=title_alpha)

        if progress > 0.1:
            sub_alpha = min(1.0, (progress - 0.1) / 0.2)
            ax.text(50, 88, 'Wat je NIET moet doen',
                    fontsize=24, ha='center', va='top',
                    color=self.colors['text'], alpha=sub_alpha * 0.8, style='italic')

        # Grid item 1
        if progress > 0.20:
            item_alpha = min(1.0, (progress - 0.20) / 0.03)

            grid_box = FancyBboxPatch(
                (15.0, 60.0), 34, 12,
                boxstyle="round,pad=0.8",
                facecolor=self.colors['bg_light'],
                edgecolor=self.colors['warning'],
                linewidth=2,
                alpha=0.9 * item_alpha
            )
            ax.add_patch(grid_box)

            ax.text(32.0, 69.5, '[X]',
                    fontsize=30, ha='center', va='center', alpha=item_alpha)
            ax.text(32.0, 66.0, 'Te Vaag',
                    fontsize=15, fontweight='bold', ha='center', va='center',
                    color=self.colors['warning'], alpha=item_alpha)
            ax.text(32.0, 62.5, 'Te algemene instructies zonder context',
                    fontsize=11, ha='center', va='center',
                    color=self.colors['text'], alpha=item_alpha * 0.8,
                    linespacing=1.3)

        # Grid item 2
        if progress > 0.23:
            item_alpha = min(1.0, (progress - 0.23) / 0.03)

            grid_box = FancyBboxPatch(
                (51.0, 60.0), 34, 12,
                boxstyle="round,pad=0.8",
                facecolor=self.colors['bg_light'],
                edgecolor=self.colors['warning'],
                linewidth=2,
                alpha=0.9 * item_alpha
            )
            ax.add_patch(grid_box)

            ax.text(68.0, 69.5, '[books]',
                    fontsize=30, ha='center', va='center', alpha=item_alpha)
            ax.text(68.0, 66.0, 'Te Lang',
                    fontsize=15, fontweight='bold', ha='center', va='center',
                    color=self.colors['warning'], alpha=item_alpha)
            ax.text(68.0, 62.5, 'Oneindige paragrafen die niemand leest',
                    fontsize=11, ha='center', va='center',
                    color=self.colors['text'], alpha=item_alpha * 0.8,
                    linespacing=1.3)

        # Grid item 3
        if progress > 0.27:
            item_alpha = min(1.0, (progress - 0.27) / 0.03)

            grid_box = FancyBboxPatch(
                (15.0, 46.0), 34, 12,
                boxstyle="round,pad=0.8",
                facecolor=self.colors['bg_light'],
                edgecolor=self.colors['warning'],
                linewidth=2,
                alpha=0.9 * item_alpha
            )
            ax.add_patch(grid_box)

            ax.text(32.0, 55.5, '🤔',
                    fontsize=30, ha='center', va='center', alpha=item_alpha)
            ax.text(32.0, 52.0, 'Aannames',
                    fontsize=15, fontweight='bold', ha='center', va='center',
                    color=self.colors['warning'], alpha=item_alpha)
            ax.text(32.0, 48.5, 'Veronderstellingen zonder uitleg',
                    fontsize=11, ha='center', va='center',
                    color=self.colors['text'], alpha=item_alpha * 0.8,
                    linespacing=1.3)

        # Grid item 4
        if progress > 0.30:
            item_alpha = min(1.0, (progress - 0.30) / 0.03)

            grid_box = FancyBboxPatch(
                (51.0, 46.0), 34, 12,
                boxstyle="round,pad=0.8",
                facecolor=self.colors['bg_light'],
                edgecolor=self.colors['warning'],
                linewidth=2,
                alpha=0.9 * item_alpha
            )
            ax.add_patch(grid_box)

            ax.text(68.0, 55.5, '🎭',
                    fontsize=30, ha='center', va='center', alpha=item_alpha)
            ax.text(68.0, 52.0, 'Tegenstrijdig',
                    fontsize=15, fontweight='bold', ha='center', va='center',
                    color=self.colors['warning'], alpha=item_alpha)
            ax.text(68.0, 48.5, 'Conflicterende instructies in één prompt',
                    fontsize=11, ha='center', va='center',
                    color=self.colors['text'], alpha=item_alpha * 0.8,
                    linespacing=1.3)

        # Grid item 5
        if progress > 0.33:
            item_alpha = min(1.0, (progress - 0.33) / 0.03)

            grid_box = FancyBboxPatch(
                (15.0, 32.0), 34, 12,
                boxstyle="round,pad=0.8",
                facecolor=self.colors['bg_light'],
                edgecolor=self.colors['warning'],
                linewidth=2,
                alpha=0.9 * item_alpha
            )
            ax.add_patch(grid_box)

            ax.text(32.0, 41.5, '[#]',
                    fontsize=30, ha='center', va='center', alpha=item_alpha)
            ax.text(32.0, 38.0, 'Geen Format',
                    fontsize=15, fontweight='bold', ha='center', va='center',
                    color=self.colors['warning'], alpha=item_alpha)
            ax.text(32.0, 34.5, 'Niet specificeren hoe output eruit moet zien',
                    fontsize=11, ha='center', va='center',
                    color=self.colors['text'], alpha=item_alpha * 0.8,
                    linespacing=1.3)

        # Grid item 6
        if progress > 0.37:
            item_alpha = min(1.0, (progress - 0.37) / 0.03)

            grid_box = FancyBboxPatch(
                (51.0, 32.0), 34, 12,
                boxstyle="round,pad=0.8",
                facecolor=self.colors['bg_light'],
                edgecolor=self.colors['warning'],
                linewidth=2,
                alpha=0.9 * item_alpha
            )
            ax.add_patch(grid_box)

            ax.text(68.0, 41.5, '🧪',
                    fontsize=30, ha='center', va='center', alpha=item_alpha)
            ax.text(68.0, 38.0, 'Niet Testen',
                    fontsize=15, fontweight='bold', ha='center', va='center',
                    color=self.colors['warning'], alpha=item_alpha)
            ax.text(68.0, 34.5, 'Geen iteratie op basis van resultaten',
                    fontsize=11, ha='center', va='center',
                    color=self.colors['text'], alpha=item_alpha * 0.8,
                    linespacing=1.3)

        if progress > 0.8:
            box_alpha = min(1.0, (progress - 0.8) / 0.19999999999999996)

            box = FancyBboxPatch(
                (10.0, 8.0), 80, 12,
                boxstyle="round,pad=1",
                facecolor=self.colors['bg_light'],
                edgecolor=self.colors['secondary'],
                linewidth=3,
                alpha=0.95 * box_alpha
            )
            ax.add_patch(box)

            ax.text(50, 17.0, '[OK] De Oplossing: Itereer!',
                    fontsize=24, fontweight='bold', ha='center', va='center',
                    color=self.colors['secondary'], alpha=box_alpha)

            ax.text(50, 11.0, 'Test je prompts, analyseer resultaten, en verfijn stap voor stap',
                    fontsize=18, ha='center', va='center',
                    color=self.colors['text'], alpha=box_alpha * 0.9)

        self.add_status_indicator(progress < 1.0)

    def draw_best_practices_checklist(self, progress: float):
        """Step 9: Best Practices Checklist"""
        self.fig.clear()
        ax = self.fig.add_subplot(111)
        ax.axis('off')
        ax.set_xlim(0, 100)
        ax.set_ylim(0, 100)

        # Title
        title_alpha = min(1.0, progress / 0.2)
        ax.text(50, 95, 'Je Prompt Checklist ✓',
                fontsize=45, fontweight='bold', ha='center', va='top',
                color=self.colors['primary'], alpha=title_alpha)

        # Checklist item 1
        if progress > 0.20:
            check_alpha = min(1.0, (progress - 0.20) / 0.03)

            ax.text(20, 86.0, '\u2713',
                    fontsize=27, ha='center', va='center',
                    color=self.colors['secondary'], fontweight='bold',
                    alpha=check_alpha)

            ax.text(25, 86.0, '\u2611 Duidelijke taak gedefinieerd?',
                    fontsize=18, ha='left', va='center',
                    color=self.colors['text'], alpha=check_alpha)

        # Checklist item 2
        if progress > 0.23:
            check_alpha = min(1.0, (progress - 0.23) / 0.03)

            ax.text(20, 79.5, '\u2713',
                    fontsize=27, ha='center', va='center',
                    color=self.colors['secondary'], fontweight='bold',
                    alpha=check_alpha)

            ax.text(25, 79.5, '\u2611 Context en achtergrond gegeven?',
                    fontsize=18, ha='left', va='center',
                    color=self.colors['text'], alpha=check_alpha)

        # Checklist item 3
        if progress > 0.25:
            check_alpha = min(1.0, (progress - 0.25) / 0.03)

            ax.text(20, 73.0, '\u2713',
                    fontsize=27, ha='center', va='center',
                    color=self.colors['secondary'], fontweight='bold',
                    alpha=check_alpha)

            ax.text(25, 73.0, '\u2611 Gewenst format gespecificeerd?',
                    fontsize=18, ha='left', va='center',
                    color=self.colors['text'], alpha=check_alpha)

        # Checklist item 4
        if progress > 0.28:
            check_alpha = min(1.0, (progress - 0.28) / 0.03)

            ax.text(20, 66.5, '\u2713',
                    fontsize=27, ha='center', va='center',
                    color=self.colors['secondary'], fontweight='bold',
                    alpha=check_alpha)

            ax.text(25, 66.5, '\u2611 Toon en stijl aangegeven?',
                    fontsize=18, ha='left', va='center',
                    color=self.colors['text'], alpha=check_alpha)

        # Checklist item 5
        if progress > 0.30:
            check_alpha = min(1.0, (progress - 0.30) / 0.03)

            ax.text(20, 60.0, '\u2713',
                    fontsize=27, ha='center', va='center',
                    color=self.colors['secondary'], fontweight='bold',
                    alpha=check_alpha)

            ax.text(25, 60.0, '\u2611 Voorbeelden toegevoegd (indien nodig)?',
                    fontsize=18, ha='left', va='center',
                    color=self.colors['text'], alpha=check_alpha)

        # Checklist item 6
        if progress > 0.33:
            check_alpha = min(1.0, (progress - 0.33) / 0.03)

            ax.text(20, 53.5, '\u2713',
                    fontsize=27, ha='center', va='center',
                    color=self.colors['secondary'], fontweight='bold',
                    alpha=check_alpha)

            ax.text(25, 53.5, '\u2611 Beperkingen vermeld?',
                    fontsize=18, ha='left', va='center',
                    color=self.colors['text'], alpha=check_alpha)

        # Checklist item 7
        if progress > 0.35:
            check_alpha = min(1.0, (progress - 0.35) / 0.03)

            ax.text(20, 47.0, '\u2713',
                    fontsize=27, ha='center', va='center',
                    color=self.colors['secondary'], fontweight='bold',
                    alpha=check_alpha)

            ax.text(25, 47.0, '\u2611 Rol/persona toegewezen (indien nuttig)?',
                    fontsize=18, ha='left', va='center',
                    color=self.colors['text'], alpha=check_alpha)

        # Checklist item 8
        if progress > 0.38:
            check_alpha = min(1.0, (progress - 0.38) / 0.03)

            ax.text(20, 40.5, '\u2713',
                    fontsize=27, ha='center', va='center',
                    color=self.colors['secondary'], fontweight='bold',
                    alpha=check_alpha)

            ax.text(25, 40.5, '\u2611 Lengte/omvang aangegeven?',
                    fontsize=18, ha='left', va='center',
                    color=self.colors['text'], alpha=check_alpha)

        if progress > 0.8:
            box_alpha = min(1.0, (progress - 0.8) / 0.19999999999999996)

            box = FancyBboxPatch(
                (10.0, 8.0), 80, 15,
                boxstyle="round,pad=1",
                facecolor=self.colors['bg_light'],
                edgecolor=self.colors['highlight'],
                linewidth=3,
                alpha=0.95 * box_alpha
            )
            ax.add_patch(box)

            ax.text(50, 19.25, '>> Onthoud: Prompt Engineering is een Vaardigheid',
                    fontsize=24, fontweight='bold', ha='center', va='center',
                    color=self.colors['highlight'], alpha=box_alpha)

            ax.text(50, 11.75, 'Hoe meer je oefent, hoe beter je wordt!\nStart simpel → Test → Verfijn → Herhaal',
                    fontsize=18, ha='center', va='center',
                    color=self.colors['text'], alpha=box_alpha * 0.9)

        self.add_status_indicator(progress < 1.0)


def run():
    """Run the presentation"""
    pres = PromptEngineeringPresentation()
    pres.show()


if __name__ == "__main__":
    run()
