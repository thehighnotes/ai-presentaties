"""
Prompt Engineering Presentatie
Leer hoe je effectief communiceert met AI systemen
"""

import sys
import os
import numpy as np
import textwrap
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle
import matplotlib.pyplot as plt

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core import BasePresentation, PresentationStyle


class PromptEngineeringPresentation(BasePresentation):
    """Prompt Engineering - De kunst van AI communicatie"""

    def __init__(self):
        """Initialize the prompt engineering presentation"""
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

        # Example prompts
        self.bad_prompt = "Schrijf iets over AI"
        self.good_prompt = """Schrijf een informatieve paragraaf van 100 woorden
over de voordelen van AI in de gezondheidszorg.
Richt je op: diagnose nauwkeurigheid, efficiëntie, en patiëntenzorg.
Gebruik een professionele maar toegankelijke toon."""

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

        # Main title
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

        # Icons
        ax.text(30, 67, '💬', fontsize=75, ha='center', va='center')
        ax.text(70, 67, '🤖', fontsize=75, ha='center', va='center')

        # Subtitle
        ax.text(50, 45, 'Leer hoe je betere resultaten krijgt uit AI',
                fontsize=27, ha='center', va='center',
                color=self.colors['accent'], alpha=0.9)

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

        ax.text(50, 25, '>> Druk op SPATIE om te beginnen <<',
                fontsize=30, ha='center', va='center',
                color=self.colors['secondary'], fontweight='bold')

        ax.text(50, 20, 'SPACE=Volgende | B=Vorige | R=Reset | Q=Afsluiten',
                fontsize=18, ha='center', va='center',
                color=self.colors['dim'], style='italic')

        # Footer
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
            self.draw_what_is_prompting(progress)
        elif self.current_step == 2:
            self.draw_why_important(progress)
        elif self.current_step == 3:
            self.draw_anatomy(progress)
        elif self.current_step == 4:
            self.draw_clear_instructions(progress)
        elif self.current_step == 5:
            self.draw_few_shot(progress)
        elif self.current_step == 6:
            self.draw_chain_of_thought(progress)
        elif self.current_step == 7:
            self.draw_role_playing(progress)
        elif self.current_step == 8:
            self.draw_pitfalls(progress)
        elif self.current_step == 9:
            self.draw_checklist(progress)

        if frame >= total_frames - 1:
            self.is_animating = False

    def draw_current_step_static(self):
        """Draw current step without animation"""
        if self.current_step == -1:
            self.show_landing_page()
        elif self.current_step == 1:
            self.draw_what_is_prompting(1.0)
        elif self.current_step == 2:
            self.draw_why_important(1.0)
        elif self.current_step == 3:
            self.draw_anatomy(1.0)
        elif self.current_step == 4:
            self.draw_clear_instructions(1.0)
        elif self.current_step == 5:
            self.draw_few_shot(1.0)
        elif self.current_step == 6:
            self.draw_chain_of_thought(1.0)
        elif self.current_step == 7:
            self.draw_role_playing(1.0)
        elif self.current_step == 8:
            self.draw_pitfalls(1.0)
        elif self.current_step == 9:
            self.draw_checklist(1.0)
        plt.draw()

    def draw_what_is_prompting(self, progress: float):
        """Step 1: What is Prompt Engineering?"""
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

        # Definition
        if progress > 0.2:
            def_alpha = min(1.0, (progress - 0.2) / 0.3)

            def_box = FancyBboxPatch(
                (15, 70), 70, 15,
                boxstyle="round,pad=1.5",
                facecolor=self.colors['bg_light'],
                edgecolor=self.colors['primary'],
                linewidth=3,
                alpha=0.95 * def_alpha
            )
            ax.add_patch(def_box)

            definition = """Prompt Engineering is de kunst en wetenschap van het
formuleren van effectieve instructies voor AI-modellen om
optimale resultaten te krijgen."""

            ax.text(50, 77.5, definition,
                    fontsize=21, ha='center', va='center',
                    color=self.colors['text'],
                    alpha=def_alpha,
                    linespacing=1.5)

        # Visual: Input -> Processing -> Output
        items = [
            ('Jouw\nPrompt', 20, 50, 0.45, self.colors['accent'], '📝'),
            ('AI\nVerwerking', 50, 50, 0.55, self.colors['primary'], '⚙️'),
            ('Resultaat', 80, 50, 0.65, self.colors['secondary'], '✨')
        ]

        for text, x, y, delay, color, icon in items:
            if progress > delay:
                alpha = min(1.0, (progress - delay) / 0.1)

                box = FancyBboxPatch(
                    (x - 10, y - 8), 20, 16,
                    boxstyle="round,pad=1",
                    facecolor=self.colors['bg_light'],
                    edgecolor=color,
                    linewidth=3,
                    alpha=0.95 * alpha
                )
                ax.add_patch(box)

                ax.text(x, y + 4, icon,
                        fontsize=36, ha='center', va='center',
                        alpha=alpha)

                ax.text(x, y - 3, text,
                        fontsize=18, ha='center', va='center',
                        color=color, fontweight='bold',
                        alpha=alpha,
                        linespacing=1.2)

                # Arrow to next
                if x < 80 and progress > delay + 0.05:
                    arrow_alpha = min(1.0, (progress - delay - 0.05) / 0.05)
                    arrow = FancyArrowPatch(
                        (x + 10, y), (x + 20, y),
                        arrowstyle='-|>',
                        mutation_scale=25,
                        linewidth=3,
                        color=self.colors['dim'],
                        alpha=arrow_alpha
                    )
                    ax.add_artist(arrow)

        # Key insight
        if progress > 0.8:
            insight_alpha = min(1.0, (progress - 0.8) / 0.2)

            insight_box = FancyBboxPatch(
                (15, 20), 70, 15,
                boxstyle="round,pad=1",
                facecolor=self.colors['bg_light'],
                edgecolor=self.colors['highlight'],
                linewidth=2,
                alpha=0.9 * insight_alpha
            )
            ax.add_patch(insight_box)

            ax.text(50, 30, '[!] De kwaliteit van je prompt bepaalt de kwaliteit van het resultaat',
                    fontsize=21, ha='center', va='center',
                    color=self.colors['highlight'], fontweight='bold',
                    alpha=insight_alpha)

            ax.text(50, 24, 'Betere prompts = Betere antwoorden',
                    fontsize=18, ha='center', va='center',
                    color=self.colors['text'],
                    alpha=insight_alpha * 0.8)

        self.add_status_indicator(progress < 1.0)
        plt.tight_layout()

    def draw_why_important(self, progress: float):
        """Step 2: Why is it important?"""
        self.fig.clear()
        ax = self.fig.add_subplot(111)
        ax.axis('off')
        ax.set_xlim(0, 100)
        ax.set_ylim(0, 100)

        # Title
        ax.text(50, 95, 'Waarom is het Belangrijk?',
                fontsize=45, fontweight='bold', ha='center', va='top',
                color=self.colors['highlight'])

        # Comparison: Bad vs Good
        if progress > 0.15:
            bad_alpha = min(1.0, (progress - 0.15) / 0.2)

            # Bad prompt
            bad_box = FancyBboxPatch(
                (10, 60), 35, 25,
                boxstyle="round,pad=1",
                facecolor='#2a1a1a',
                edgecolor=self.colors['warning'],
                linewidth=3,
                alpha=0.9 * bad_alpha
            )
            ax.add_patch(bad_box)

            ax.text(27.5, 80, '✗ Vage Prompt', fontsize=21, ha='center',
                    color=self.colors['warning'], fontweight='bold',
                    alpha=bad_alpha)

            ax.text(27.5, 74, '"Schrijf iets\nover AI"',
                    fontsize=18, ha='center', va='center',
                    color=self.colors['text'],
                    alpha=bad_alpha,
                    style='italic',
                    linespacing=1.3)

            ax.text(27.5, 65, '→ Algemeen\n→ Niet bruikbaar\n→ Frustrerend',
                    fontsize=14, ha='center', va='center',
                    color=self.colors['dim'],
                    alpha=bad_alpha,
                    linespacing=1.4)

        # Good prompt
        if progress > 0.4:
            good_alpha = min(1.0, (progress - 0.4) / 0.2)

            good_box = FancyBboxPatch(
                (55, 60), 35, 25,
                boxstyle="round,pad=1",
                facecolor='#1a3a1a',
                edgecolor=self.colors['secondary'],
                linewidth=3,
                alpha=0.95 * good_alpha
            )
            ax.add_patch(good_box)

            ax.text(72.5, 80, '✓ Specifieke Prompt', fontsize=21, ha='center',
                    color=self.colors['secondary'], fontweight='bold',
                    alpha=good_alpha)

            ax.text(72.5, 74, '"Leg uit hoe\nRAG werkt..."',
                    fontsize=18, ha='center', va='center',
                    color=self.colors['text'],
                    alpha=good_alpha,
                    style='italic',
                    linespacing=1.3)

            ax.text(72.5, 65, '→ Specifiek\n→ Direct bruikbaar\n→ Efficiënt',
                    fontsize=14, ha='center', va='center',
                    color=self.colors['secondary'],
                    alpha=good_alpha,
                    linespacing=1.4)

        # Benefits
        benefits = [
            ('⏱️ Bespaart tijd', 45, 0.65),
            ('🎯 Betere resultaten', 38, 0.7),
            ('💰 Lagere kosten', 31, 0.75),
            ('🚀 Meer productiviteit', 24, 0.8)
        ]

        for text, y, delay in benefits:
            if progress > delay:
                alpha = min(1.0, (progress - delay) / 0.1)
                ax.text(50, y, text,
                        fontsize=21, ha='center', va='center',
                        color=self.colors['text'],
                        alpha=alpha,
                        fontweight='bold')

        # Bottom insight
        if progress > 0.9:
            insight_alpha = min(1.0, (progress - 0.9) / 0.1)
            ax.text(50, 8, '[i] Goede prompts kunnen het verschil maken tussen nutteloos en onmisbaar',
                    fontsize=18, ha='center', va='center',
                    color=self.colors['accent'],
                    fontweight='bold',
                    alpha=insight_alpha)

        self.add_status_indicator(progress < 1.0)
        plt.tight_layout()

    def draw_anatomy(self, progress: float):
        """Step 3: Anatomy of a good prompt"""
        self.fig.clear()
        ax = self.fig.add_subplot(111)
        ax.axis('off')
        ax.set_xlim(0, 100)
        ax.set_ylim(0, 100)

        # Title
        ax.text(50, 95, 'Anatomie van een Goede Prompt',
                fontsize=42, fontweight='bold', ha='center', va='top',
                color=self.colors['primary'])

        # Components in layered boxes
        components = [
            ('Context', 'Achtergrond informatie', 80, self.colors['accent'], 0.15),
            ('Instructie', 'Wat moet er gebeuren', 65, self.colors['primary'], 0.3),
            ('Format', 'Gewenste output vorm', 50, self.colors['secondary'], 0.45),
            ('Voorbeelden', 'Concrete samples (optioneel)', 35, self.colors['purple'], 0.6),
            ('Beperkingen', 'Wat NIET te doen (optioneel)', 20, self.colors['warning'], 0.75)
        ]

        for idx, (name, desc, y, color, delay) in enumerate(components):
            if progress > delay:
                alpha = min(1.0, (progress - delay) / 0.15)

                # Width varies for visual hierarchy
                width = 70 - idx * 4
                x_start = 15 + idx * 2

                box = FancyBboxPatch(
                    (x_start, y - 6), width, 12,
                    boxstyle="round,pad=0.8",
                    facecolor=self.colors['bg_light'],
                    edgecolor=color,
                    linewidth=3,
                    alpha=0.95 * alpha
                )
                ax.add_patch(box)

                ax.text(x_start + width/2, y + 2, name,
                        fontsize=21, ha='center', va='center',
                        color=color, fontweight='bold',
                        alpha=alpha)

                ax.text(x_start + width/2, y - 2, desc,
                        fontsize=14, ha='center', va='center',
                        color=self.colors['text'],
                        alpha=alpha * 0.8)

        # Example
        if progress > 0.9:
            ex_alpha = min(1.0, (progress - 0.9) / 0.1)
            ax.text(50, 8, '[→] Volgende slides: Deze componenten in actie!',
                    fontsize=18, ha='center', va='center',
                    color=self.colors['highlight'],
                    fontweight='bold',
                    alpha=ex_alpha)

        self.add_status_indicator(progress < 1.0)
        plt.tight_layout()

    def draw_clear_instructions(self, progress: float):
        """Step 4: Clear Instructions technique"""
        self.fig.clear()
        ax = self.fig.add_subplot(111)
        ax.axis('off')
        ax.set_xlim(0, 100)
        ax.set_ylim(0, 100)

        # Title
        ax.text(50, 95, 'Techniek 1: Clear Instructions',
                fontsize=42, fontweight='bold', ha='center', va='top',
                color=self.colors['primary'])

        ax.text(50, 89, 'Wees specifiek, duidelijk, en direct',
                fontsize=21, ha='center', va='top',
                color=self.colors['text'], alpha=0.7, style='italic')

        # Before/After
        if progress > 0.15:
            before_alpha = min(1.0, (progress - 0.15) / 0.2)

            # Before
            before_box = FancyBboxPatch(
                (5, 55), 40, 25,
                boxstyle="round,pad=1",
                facecolor='#2a1a1a',
                edgecolor=self.colors['warning'],
                linewidth=2,
                alpha=0.9 * before_alpha
            )
            ax.add_patch(before_box)

            ax.text(25, 76, '❌ Vaag', fontsize=18, ha='center',
                    color=self.colors['warning'], fontweight='bold',
                    alpha=before_alpha)

            vague = textwrap.fill('"Maak een email"', width=25)
            ax.text(25, 67, vague,
                    fontsize=16, ha='center', va='center',
                    color=self.colors['text'],
                    alpha=before_alpha,
                    style='italic')

        if progress > 0.4:
            after_alpha = min(1.0, (progress - 0.4) / 0.2)

            # After
            after_box = FancyBboxPatch(
                (55, 50), 40, 35,
                boxstyle="round,pad=1",
                facecolor='#1a3a1a',
                edgecolor=self.colors['secondary'],
                linewidth=3,
                alpha=0.95 * after_alpha
            )
            ax.add_patch(after_box)

            ax.text(75, 81, '✅ Specifiek', fontsize=18, ha='center',
                    color=self.colors['secondary'], fontweight='bold',
                    alpha=after_alpha)

            specific = textwrap.fill('"Schrijf een professionele email naar een klant '
                                   'om een meeting te verzetten naar volgende week. '
                                   'Wees beleefd, bied excuses aan, '
                                   'en stel 3 alternatieve tijden voor."', width=32)
            ax.text(75, 66, specific,
                    fontsize=14, ha='center', va='center',
                    color=self.colors['text'],
                    alpha=after_alpha,
                    linespacing=1.5)

        # Tips
        tips = [
            ('1. Specificeer de taak precies', 38, 0.65),
            ('2. Geef context en doel aan', 32, 0.75),
            ('3. Definieer gewenste lengte/format', 26, 0.8),
            ('4. Vermeld toon en stijl', 20, 0.85)
        ]

        for text, y, delay in tips:
            if progress > delay:
                alpha = min(1.0, (progress - delay) / 0.1)
                ax.text(50, y, text,
                        fontsize=16, ha='center', va='center',
                        color=self.colors['text'],
                        alpha=alpha)

        # Bottom
        if progress > 0.9:
            bottom_alpha = min(1.0, (progress - 0.9) / 0.1)
            ax.text(50, 8, '[💡] Hoe specifieker, hoe beter het resultaat',
                    fontsize=18, ha='center', va='center',
                    color=self.colors['accent'],
                    fontweight='bold',
                    alpha=bottom_alpha)

        self.add_status_indicator(progress < 1.0)
        plt.tight_layout()

    def draw_few_shot(self, progress: float):
        """Step 5: Few-Shot Learning technique"""
        self.fig.clear()
        ax = self.fig.add_subplot(111)
        ax.axis('off')
        ax.set_xlim(0, 100)
        ax.set_ylim(0, 100)

        # Title
        ax.text(50, 95, 'Techniek 2: Few-Shot Learning',
                fontsize=42, fontweight='bold', ha='center', va='top',
                color=self.colors['secondary'])

        ax.text(50, 89, 'Geef voorbeelden van wat je wilt',
                fontsize=21, ha='center', va='top',
                color=self.colors['text'], alpha=0.7, style='italic')

        # Example structure
        if progress > 0.15:
            struct_alpha = min(1.0, (progress - 0.15) / 0.2)

            struct_box = FancyBboxPatch(
                (10, 60), 80, 22,
                boxstyle="round,pad=1.5",
                facecolor=self.colors['bg_light'],
                edgecolor=self.colors['secondary'],
                linewidth=3,
                alpha=0.95 * struct_alpha
            )
            ax.add_patch(struct_box)

            example_text = """Vertaal naar beleefd Nederlands:

Voorbeeld 1:
Input: "give me the report"
Output: "Zou je mij het rapport kunnen toesturen?"

Voorbeeld 2:
Input: "send it now"
Output: "Kun je het zo spoedig mogelijk versturen?"

Nu jouw beurt:
Input: "call me back"
Output: ?"""

            ax.text(50, 71, example_text,
                    fontsize=15, ha='center', va='center',
                    color=self.colors['text'],
                    alpha=struct_alpha,
                    family='monospace',
                    linespacing=1.6)

        # Benefits
        if progress > 0.5:
            benefits_alpha = min(1.0, (progress - 0.5) / 0.3)

            benefits = [
                '✓ Model leert het patroon',
                '✓ Consistente output',
                '✓ Minder uitleg nodig'
            ]

            for idx, benefit in enumerate(benefits):
                ax.text(50, 48 - idx * 5, benefit,
                        fontsize=18, ha='center', va='center',
                        color=self.colors['secondary'],
                        alpha=benefits_alpha,
                        fontweight='bold')

        # Use cases
        if progress > 0.75:
            use_alpha = min(1.0, (progress - 0.75) / 0.25)

            use_box = FancyBboxPatch(
                (15, 15), 70, 15,
                boxstyle="round,pad=1",
                facecolor=self.colors['bg_light'],
                edgecolor=self.colors['accent'],
                linewidth=2,
                alpha=0.9 * use_alpha
            )
            ax.add_patch(use_box)

            ax.text(50, 25, 'Perfect voor:', fontsize=18, ha='center',
                    color=self.colors['accent'], fontweight='bold',
                    alpha=use_alpha)

            ax.text(50, 20, 'Vertalingen • Classificaties • Format conversies • Data extractie',
                    fontsize=15, ha='center', va='center',
                    color=self.colors['text'],
                    alpha=use_alpha)

        self.add_status_indicator(progress < 1.0)
        plt.tight_layout()

    def draw_chain_of_thought(self, progress: float):
        """Step 6: Chain-of-Thought technique"""
        self.fig.clear()
        ax = self.fig.add_subplot(111)
        ax.axis('off')
        ax.set_xlim(0, 100)
        ax.set_ylim(0, 100)

        # Title
        ax.text(50, 95, 'Techniek 3: Chain-of-Thought',
                fontsize=42, fontweight='bold', ha='center', va='top',
                color=self.colors['purple'])

        ax.text(50, 89, 'Laat AI stap-voor-stap denken',
                fontsize=21, ha='center', va='top',
                color=self.colors['text'], alpha=0.7, style='italic')

        # Comparison
        if progress > 0.15:
            direct_alpha = min(1.0, (progress - 0.15) / 0.2)

            # Direct
            direct_box = FancyBboxPatch(
                (5, 60), 40, 20,
                boxstyle="round,pad=1",
                facecolor='#2a2a1a',
                edgecolor=self.colors['warning'],
                linewidth=2,
                alpha=0.9 * direct_alpha
            )
            ax.add_patch(direct_box)

            ax.text(25, 76, '⚡ Direct', fontsize=18, ha='center',
                    color=self.colors['warning'], fontweight='bold',
                    alpha=direct_alpha)

            direct_text = textwrap.fill('"Wat is 37 x 24?"', width=25)
            ax.text(25, 68, direct_text,
                    fontsize=16, ha='center', va='center',
                    color=self.colors['text'],
                    alpha=direct_alpha,
                    style='italic')

            ax.text(25, 63, '→ Vaak fout bij\ncomplexe vragen',
                    fontsize=12, ha='center', va='center',
                    color=self.colors['dim'],
                    alpha=direct_alpha,
                    linespacing=1.4)

        if progress > 0.4:
            cot_alpha = min(1.0, (progress - 0.4) / 0.2)

            # Chain-of-Thought
            cot_box = FancyBboxPatch(
                (55, 55), 40, 30,
                boxstyle="round,pad=1",
                facecolor='#2a1a3a',
                edgecolor=self.colors['purple'],
                linewidth=3,
                alpha=0.95 * cot_alpha
            )
            ax.add_patch(cot_box)

            ax.text(75, 81, '🧠 Chain-of-Thought', fontsize=18, ha='center',
                    color=self.colors['purple'], fontweight='bold',
                    alpha=cot_alpha)

            cot_text = textwrap.fill('"Wat is 37 x 24? '
                                    'Laat je redenering zien '
                                    'stap voor stap voordat '
                                    'je het antwoord geeft."', width=32)
            ax.text(75, 68, cot_text,
                    fontsize=14, ha='center', va='center',
                    color=self.colors['text'],
                    alpha=cot_alpha,
                    linespacing=1.5,
                    style='italic')

            ax.text(75, 58, '→ Veel accurater\nvoor complexe taken',
                    fontsize=12, ha='center', va='center',
                    color=self.colors['purple'],
                    alpha=cot_alpha,
                    linespacing=1.4,
                    fontweight='bold')

        # When to use
        if progress > 0.65:
            when_alpha = min(1.0, (progress - 0.65) / 0.25)

            when_items = [
                ('🧮 Wiskunde & berekeningen', 42),
                ('🤔 Logische redeneringen', 36),
                ('📋 Meerstaps problemen', 30),
                ('🔍 Analyse taken', 24)
            ]

            ax.text(50, 48, 'Wanneer gebruiken:', fontsize=18, ha='center',
                    color=self.colors['accent'], fontweight='bold',
                    alpha=when_alpha)

            for text, y in when_items:
                ax.text(50, y, text,
                        fontsize=16, ha='center', va='center',
                        color=self.colors['text'],
                        alpha=when_alpha)

        # Magic phrase
        if progress > 0.85:
            magic_alpha = min(1.0, (progress - 0.85) / 0.15)

            magic_box = FancyBboxPatch(
                (15, 8), 70, 10,
                boxstyle="round,pad=0.8",
                facecolor=self.colors['bg_light'],
                edgecolor=self.colors['highlight'],
                linewidth=3,
                alpha=0.95 * magic_alpha
            )
            ax.add_patch(magic_box)

            ax.text(50, 13, '✨ Magic phrase: "Let\'s think step by step"',
                    fontsize=19, ha='center', va='center',
                    color=self.colors['highlight'],
                    fontweight='bold',
                    alpha=magic_alpha)

        self.add_status_indicator(progress < 1.0)
        plt.tight_layout()

    def draw_role_playing(self, progress: float):
        """Step 7: Role Playing technique"""
        self.fig.clear()
        ax = self.fig.add_subplot(111)
        ax.axis('off')
        ax.set_xlim(0, 100)
        ax.set_ylim(0, 100)

        # Title
        ax.text(50, 95, 'Techniek 4: Role Playing',
                fontsize=42, fontweight='bold', ha='center', va='top',
                color=self.colors['accent'])

        ax.text(50, 89, 'Geef AI een specifieke rol of persona',
                fontsize=21, ha='center', va='top',
                color=self.colors['text'], alpha=0.7, style='italic')

        # Role examples in grid
        roles = [
            ('👨‍🏫 Expert Leraar', 'Leg uit alsof ik 10 jaar oud ben', 20, 70, 0.2, self.colors['primary']),
            ('💼 Business Consultant', 'Analyseer deze data strategisch', 50, 70, 0.3, self.colors['secondary']),
            ('👨‍💻 Senior Developer', 'Review deze code kritisch', 80, 70, 0.4, self.colors['purple']),
            ('✍️ Professioneel Schrijver', 'Schrijf in journalistieke stijl', 35, 45, 0.5, self.colors['accent']),
            ('🤝 Empathische Coach', 'Geef constructieve feedback', 65, 45, 0.6, self.colors['highlight'])
        ]

        for icon_title, desc, x, y, delay, color in roles:
            if progress > delay:
                alpha = min(1.0, (progress - delay) / 0.15)

                box = FancyBboxPatch(
                    (x - 13, y - 9), 26, 18,
                    boxstyle="round,pad=0.8",
                    facecolor=self.colors['bg_light'],
                    edgecolor=color,
                    linewidth=2,
                    alpha=0.95 * alpha
                )
                ax.add_patch(box)

                ax.text(x, y + 5, icon_title.split()[0],
                        fontsize=33, ha='center', va='center',
                        alpha=alpha)

                ax.text(x, y, icon_title.split(' ', 1)[1] if ' ' in icon_title else '',
                        fontsize=13, ha='center', va='center',
                        color=color, fontweight='bold',
                        alpha=alpha)

                wrapped_desc = textwrap.fill(desc, width=18)
                ax.text(x, y - 5, wrapped_desc,
                        fontsize=10, ha='center', va='center',
                        color=self.colors['text'],
                        alpha=alpha * 0.8,
                        linespacing=1.3)

        # Example prompt
        if progress > 0.75:
            example_alpha = min(1.0, (progress - 0.75) / 0.25)

            example_box = FancyBboxPatch(
                (10, 18), 80, 18,
                boxstyle="round,pad=1.2",
                facecolor=self.colors['bg_light'],
                edgecolor=self.colors['accent'],
                linewidth=3,
                alpha=0.95 * example_alpha
            )
            ax.add_patch(example_box)

            ax.text(50, 31, '📝 Voorbeeld Template:', fontsize=18, ha='center',
                    color=self.colors['accent'], fontweight='bold',
                    alpha=example_alpha)

            template = textwrap.fill('Je bent een [ROL] met [X] jaar ervaring. '
                                    'Je specialiteit is [EXPERTISE]. '
                                    'Help me met: [TAAK]', width=70)
            ax.text(50, 24, template,
                    fontsize=14, ha='center', va='center',
                    color=self.colors['text'],
                    alpha=example_alpha,
                    style='italic',
                    linespacing=1.5)

        # Bottom tip
        if progress > 0.9:
            tip_alpha = min(1.0, (progress - 0.9) / 0.1)
            ax.text(50, 8, '[💡] Rollen activeren specifieke kennis en stijlen in het model',
                    fontsize=16, ha='center', va='center',
                    color=self.colors['highlight'],
                    fontweight='bold',
                    alpha=tip_alpha)

        self.add_status_indicator(progress < 1.0)
        plt.tight_layout()

    def draw_pitfalls(self, progress: float):
        """Step 8: Common pitfalls"""
        self.fig.clear()
        ax = self.fig.add_subplot(111)
        ax.axis('off')
        ax.set_xlim(0, 100)
        ax.set_ylim(0, 100)

        # Title
        ax.text(50, 95, 'Veelvoorkomende Valkuilen',
                fontsize=42, fontweight='bold', ha='center', va='top',
                color=self.colors['warning'])

        ax.text(50, 89, 'Wat je NIET moet doen',
                fontsize=21, ha='center', va='top',
                color=self.colors['text'], alpha=0.7, style='italic')

        # Pitfalls in grid
        pitfalls = [
            {
                'icon': '❌',
                'title': 'Te Vaag',
                'desc': 'Te algemene instructies zonder context',
                'x': 25,
                'y': 70,
                'delay': 0.15
            },
            {
                'icon': '📚',
                'title': 'Te Lang',
                'desc': 'Oneindige paragrafen die niemand leest',
                'x': 75,
                'y': 70,
                'delay': 0.25
            },
            {
                'icon': '🤔',
                'title': 'Aannames',
                'desc': 'Veronderstellingen zonder uitleg',
                'x': 25,
                'y': 50,
                'delay': 0.35
            },
            {
                'icon': '🎭',
                'title': 'Tegenstrijdig',
                'desc': 'Conflicterende instructies in één prompt',
                'x': 75,
                'y': 50,
                'delay': 0.45
            },
            {
                'icon': '🔢',
                'title': 'Geen Format',
                'desc': 'Niet specificeren hoe output eruit moet zien',
                'x': 25,
                'y': 30,
                'delay': 0.55
            },
            {
                'icon': '🧪',
                'title': 'Niet Testen',
                'desc': 'Geen iteratie op basis van resultaten',
                'x': 75,
                'y': 30,
                'delay': 0.65
            }
        ]

        for pitfall in pitfalls:
            if progress > pitfall['delay']:
                alpha = min(1.0, (progress - pitfall['delay']) / 0.12)

                box = FancyBboxPatch(
                    (pitfall['x'] - 18, pitfall['y'] - 7), 36, 14,
                    boxstyle="round,pad=0.8",
                    facecolor=self.colors['bg_light'],
                    edgecolor=self.colors['warning'],
                    linewidth=2,
                    alpha=0.9 * alpha
                )
                ax.add_patch(box)

                ax.text(pitfall['x'], pitfall['y'] + 4, pitfall['icon'],
                        fontsize=30, ha='center', va='center',
                        alpha=alpha)

                ax.text(pitfall['x'], pitfall['y'], pitfall['title'],
                        fontsize=15, ha='center', va='center',
                        color=self.colors['warning'], fontweight='bold',
                        alpha=alpha)

                wrapped_desc = textwrap.fill(pitfall['desc'], width=24)
                ax.text(pitfall['x'], pitfall['y'] - 4, wrapped_desc,
                        fontsize=11, ha='center', va='center',
                        color=self.colors['text'],
                        alpha=alpha * 0.8,
                        linespacing=1.3)

        # Bottom advice
        if progress > 0.85:
            advice_alpha = min(1.0, (progress - 0.85) / 0.15)

            advice_box = FancyBboxPatch(
                (10, 8), 80, 12,
                boxstyle="round,pad=1",
                facecolor=self.colors['bg_light'],
                edgecolor=self.colors['secondary'],
                linewidth=3,
                alpha=0.95 * advice_alpha
            )
            ax.add_patch(advice_box)

            ax.text(50, 16, '✅ De Oplossing: Itereer!',
                    fontsize=21, ha='center', va='center',
                    color=self.colors['secondary'], fontweight='bold',
                    alpha=advice_alpha)

            ax.text(50, 11, 'Test je prompts, analyseer resultaten, en verfijn stap voor stap',
                    fontsize=16, ha='center', va='center',
                    color=self.colors['text'],
                    alpha=advice_alpha)

        self.add_status_indicator(progress < 1.0)
        plt.tight_layout()

    def draw_checklist(self, progress: float):
        """Step 9: Best Practices Checklist"""
        self.fig.clear()
        ax = self.fig.add_subplot(111)
        ax.axis('off')
        ax.set_xlim(0, 100)
        ax.set_ylim(0, 100)

        # Title with animation
        title_alpha = min(1.0, progress / 0.2)

        if progress > 0.5:
            pulse = 1 + 0.03 * np.sin(progress * 20)
            fontsize = 45 * pulse
        else:
            fontsize = 45

        ax.text(50, 95, 'Je Prompt Checklist ✓',
                fontsize=fontsize, fontweight='bold', ha='center', va='top',
                color=self.colors['secondary'], alpha=title_alpha)

        # Checklist items
        checklist = [
            ('☑ Duidelijke taak gedefinieerd?', 78, 0.2),
            ('☑ Context en achtergrond gegeven?', 71, 0.3),
            ('☑ Gewenst format gespecificeerd?', 64, 0.4),
            ('☑ Toon en stijl aangegeven?', 57, 0.5),
            ('☑ Voorbeelden toegevoegd (indien nodig)?', 50, 0.6),
            ('☑ Beperkingen vermeld?', 43, 0.7),
            ('☑ Rol/persona toegewezen (indien nuttig)?', 36, 0.75),
            ('☑ Lengte/omvang aangegeven?', 29, 0.8)
        ]

        for text, y, delay in checklist:
            if progress > delay:
                alpha = min(1.0, (progress - delay) / 0.1)

                # Checkmark appears first
                ax.text(20, y, '✓',
                        fontsize=27, ha='center', va='center',
                        color=self.colors['secondary'],
                        fontweight='bold',
                        alpha=alpha)

                # Then text
                ax.text(50, y, text,
                        fontsize=18, ha='left', va='center',
                        color=self.colors['text'],
                        alpha=alpha)

        # Final message
        if progress > 0.88:
            final_alpha = min(1.0, (progress - 0.88) / 0.12)

            final_box = FancyBboxPatch(
                (10, 8), 80, 15,
                boxstyle="round,pad=1.2",
                facecolor=self.colors['bg_light'],
                edgecolor=self.colors['highlight'],
                linewidth=4,
                alpha=0.95 * final_alpha
            )
            ax.add_patch(final_box)

            ax.text(50, 19, '🎯 Onthoud: Prompt Engineering is een Vaardigheid',
                    fontsize=21, ha='center', va='center',
                    color=self.colors['highlight'], fontweight='bold',
                    alpha=final_alpha)

            ax.text(50, 14, 'Hoe meer je oefent, hoe beter je wordt!',
                    fontsize=18, ha='center', va='center',
                    color=self.colors['text'],
                    alpha=final_alpha)

            ax.text(50, 10, 'Start simpel → Test → Verfijn → Herhaal',
                    fontsize=16, ha='center', va='center',
                    color=self.colors['secondary'],
                    alpha=final_alpha,
                    style='italic')

        self.add_status_indicator(progress < 1.0)
        plt.tight_layout()

    def add_status_indicator(self, is_animating):
        """Add animation indicator"""
        if is_animating:
            self.fig.text(0.95, 0.02, '...', fontsize=24, ha='right', va='bottom',
                         color=self.colors['accent'], fontweight='bold')


def main():
    """Main entry point"""
    print("="*80)
    print("PROMPT ENGINEERING - DE KUNST VAN AI COMMUNICATIE")
    print("="*80)
    print("\n🎨 Deze presentatie leert je:")
    print("  1. Wat is Prompt Engineering?")
    print("  2. Waarom is het belangrijk?")
    print("  3. Anatomie van een goede prompt")
    print("  4. Clear Instructions techniek")
    print("  5. Few-Shot Learning techniek")
    print("  6. Chain-of-Thought techniek")
    print("  7. Role Playing techniek")
    print("  8. Veelvoorkomende valkuilen")
    print("  9. Best Practices Checklist")
    print("\n[Keys]  Controls:")
    print("  SPACE : Volgende stap")
    print("  B     : Vorige stap")
    print("  R     : Reset")
    print("  Q     : Quit")
    print("  F     : Fullscreen")
    print("\n[i] Doel:")
    print("  Leer hoe je effectiever communiceert met AI")
    print("  Van vage vragen naar concrete, bruikbare resultaten")
    print("  Praktische technieken die je meteen kunt toepassen")
    print("\n" + "="*80 + "\n")

    presentation = PromptEngineeringPresentation()
    presentation.show()


if __name__ == "__main__":
    main()
