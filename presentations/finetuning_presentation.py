"""
Finetuning Journey Visualization
Interactive step-by-step animation: From base model to specialized behavior
Refactored with BasePresentation and proper Unicode encoding
"""

import sys
import os
import numpy as np
import textwrap
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle, Arc
import matplotlib.patches as patches

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core import (BasePresentation, PresentationStyle, WeightDeltaVisualizer,
                  ProgressIndicator, AnimationHelpers)


class FinetuningPresentation(BasePresentation):
    """
    Finetuning Journey Visualization
    Demonstrates how to transform a base model into a domain specialist
    """

    def __init__(self):
        """Initialize the finetuning presentation"""
        step_names = [
            'Landing',
            'Base Model',
            'Training Data',
            'Model Predictions - Het Probleem!',
            'Loss Function',
            'Gradient Updates',
            'Weight Adjustment',
            'Finetuned Model',
            'Comparison',
            'Azure AI / Local Setup'
        ]

        super().__init__("Finetuning Journey", step_names)

        # Training examples (Cooking/Recipe domain)
        self.training_examples = [
            {
                'input': 'Hoe lang moet ik pasta koken?',
                'output': 'Kook pasta al dente in 8-10 minuten in ruim kokend water met zout. Proef regelmatig voor de perfecte beet.',
                'category': 'Kooktechnieken'
            },
            {
                'input': 'Wat is het verschil tussen bakken en braden?',
                'output': 'Bakken gebeurt in een pan met weinig vet op matig vuur. Braden is in de oven bij hoge temperatuur met vocht voor malse garing.',
                'category': 'Bereidingsmethoden'
            },
            {
                'input': 'Hoe maak ik een perfecte jus?',
                'output': 'Gebruik braadvet en aanbaksels, blus met wijn of bouillon, reduceer tot de gewenste dikte. Zeef voor een gladde jus.',
                'category': 'Sauzen & Jus'
            }
        ]

        # Weights (simplified representation for visualization)
        np.random.seed(42)  # For reproducibility
        self.base_weights = np.random.randn(50) * 0.5
        self.finetuned_weights = self.base_weights + np.random.randn(50) * 0.2

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
            (10, 55), 80, 25,
            boxstyle="round,pad=2",
            facecolor=self.colors['bg_light'],
            edgecolor=self.colors['purple'],
            linewidth=4,
            alpha=0.95
        )
        ax.add_patch(title_box)

        ax.text(50, 72, 'Finetuning Journey',
                fontsize=72, fontweight='bold', ha='center', va='center',
                color=self.colors['purple'])

        ax.text(50, 64, 'Van Algemeen Model naar Specialist',
                fontsize=33, ha='center', va='center',
                color=self.colors['text'], alpha=0.8, style='italic')

        # Icons
        ax.text(30, 67, 'AI', fontsize=90, ha='center', va='center',
               fontweight='bold', color=self.colors['primary'])
        ax.text(70, 67, '>>', fontsize=90, ha='center', va='center',
               fontweight='bold', color=self.colors['secondary'])

        # Subtitle
        ax.text(50, 45, 'Leer hoe je AI traint voor specifieke taken',
                fontsize=33, ha='center', va='center',
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

        ax.text(50, 25, '>> Druk op SPATIE om te beginnen <<',
                fontsize=36, ha='center', va='center',
                color=self.colors['secondary'], fontweight='bold')

        ax.text(50, 20, 'B=Terug • R=Reset • Q=Afsluiten • F=Volledig scherm',
                fontsize=24, ha='center', va='center',
                color=self.colors['dim'], style='italic')

        # Footer
        ax.text(50, 5, 'Inclusief Azure AI Studio en Local LLM voorbeelden',
                fontsize=24, ha='center', va='center',
                color=self.colors['text'], alpha=0.5)

        plt.tight_layout()

    def get_frames_for_step(self, step: int) -> int:
        """Get animation frame count for each step"""
        frames_dict = {
            0: 30,   # Landing
            1: 80,   # Base Model
            2: 90,   # Training Data
            3: 100,  # Model Predictions
            4: 100,  # Loss Function
            5: 120,  # Gradient Updates
            6: 100,  # Weight Adjustment
            7: 80,   # Finetuned Model
            8: 100,  # Comparison
            9: 90    # Azure/Local
        }
        return frames_dict.get(step, 60)

    def animate_step(self, frame: int):
        """Animate current step"""
        total_frames = self.get_frames_for_step(self.current_step)
        progress = frame / (total_frames - 1) if total_frames > 1 else 1

        if self.current_step == 0:
            pass  # Landing is static
        elif self.current_step == 1:
            self.draw_base_model(progress)
        elif self.current_step == 2:
            self.draw_training_data(progress)
        elif self.current_step == 3:
            self.draw_model_predictions(progress)
        elif self.current_step == 4:
            self.draw_loss_function(progress)
        elif self.current_step == 5:
            self.draw_gradient_updates(progress)
        elif self.current_step == 6:
            self.draw_weight_adjustment(progress)
        elif self.current_step == 7:
            self.draw_finetuned_model(progress)
        elif self.current_step == 8:
            self.draw_comparison(progress)
        elif self.current_step == 9:
            self.draw_azure_local_setup(progress)

        if frame >= total_frames - 1:
            self.on_animation_complete()

    def draw_current_step_static(self):
        """Draw current step as static image"""
        if self.current_step == -1:
            self.show_landing_page()
        elif self.current_step == 1:
            self.draw_base_model(1.0)
        elif self.current_step == 2:
            self.draw_training_data(1.0)
        elif self.current_step == 3:
            self.draw_model_predictions(1.0)
        elif self.current_step == 4:
            self.draw_loss_function(1.0)
        elif self.current_step == 5:
            self.draw_gradient_updates(1.0)
        elif self.current_step == 6:
            self.draw_weight_adjustment(1.0)
        elif self.current_step == 7:
            self.draw_finetuned_model(1.0)
        elif self.current_step == 8:
            self.draw_comparison(1.0)
        elif self.current_step == 9:
            self.draw_azure_local_setup(1.0)
        import matplotlib.pyplot as plt
        plt.draw()

    def draw_base_model(self, progress: float):
        """Step 1: Show base pre-trained model"""
        self.fig.clear()
        ax = self.fig.add_subplot(111)
        ax.axis('off')
        ax.set_xlim(0, 100)
        ax.set_ylim(0, 100)

        # Title
        title_alpha = min(1.0, progress / 0.15)
        ax.text(50, 97, 'Stap 1: Het Basis Model',
                fontsize=51, fontweight='bold', ha='center', va='top',
                color=self.colors['primary'], alpha=title_alpha)

        ax.text(50, 90, 'Een pre-trained model met algemene kennis',
                fontsize=27, ha='center', va='top',
                color=self.colors['text'], alpha=0.7 * title_alpha, style='italic')

        # Model box (center)
        if progress > 0.2:
            model_alpha = min(1.0, (progress - 0.2) / 0.3)

            # Pulse effect
            pulse = 1 + 0.05 * np.sin(progress * 20) if progress > 0.7 else 1.0

            model_box = FancyBboxPatch(
                (30, 35), 40 * pulse, 30 * pulse,
                boxstyle="round,pad=2",
                facecolor='#1a2a4a',
                edgecolor=self.colors['primary'],
                linewidth=4,
                alpha=0.95 * model_alpha
            )
            ax.add_patch(model_box)

            ax.text(50, 55, 'AI', fontsize=120, ha='center', va='center',
                    alpha=model_alpha)

            ax.text(50, 40, 'GPT / LLaMA / Phi',
                    fontsize=24, ha='center', va='center',
                    color=self.colors['primary'],
                    fontweight='bold',
                    alpha=model_alpha)

        # Knowledge clouds
        knowledge_items = [
            ('[BOOK] Algemene kennis', 15, 70, 0.3),
            ('[GLOBE] Talen & cultuur', 85, 70, 0.35),
            ('[PC] Programmeren', 15, 30, 0.4),
            ('[SCI] Wetenschap', 85, 30, 0.45),
            ('[LIT] Literatuur', 50, 15, 0.5)
        ]

        for text, x, y, delay in knowledge_items:
            if progress > delay:
                item_alpha = min(1.0, (progress - delay) / 0.2)

                bubble = FancyBboxPatch(
                    (x - 10, y - 4), 20, 8,
                    boxstyle="round,pad=0.5",
                    facecolor=self.colors['bg_light'],
                    edgecolor=self.colors['secondary'],
                    linewidth=2,
                    alpha=0.8 * item_alpha
                )
                ax.add_patch(bubble)

                ax.text(x, y, text,
                        fontsize=16, ha='center', va='center',
                        color=self.colors['text'],
                        alpha=item_alpha)

        # Explanation
        if progress > 0.7:
            exp_alpha = min(1.0, (progress - 0.7) / 0.3)

            ax.text(50, 8, '[i] Het model kent veel, maar mist specifieke domeinkennis',
                    fontsize=19, ha='center', va='center',
                    color=self.colors['accent'],
                    alpha=0.8 * exp_alpha,
                    style='italic')

        self.add_status_indicator(progress < 1.0)
        plt.tight_layout()

    def draw_training_data(self, progress: float):
        """Step 2: Show training data examples"""
        self.fig.clear()
        ax = self.fig.add_subplot(111)
        ax.axis('off')
        ax.set_xlim(0, 100)
        ax.set_ylim(0, 100)

        # Title
        ax.text(50, 97, 'Stap 2: Training Data Verzamelen',
                fontsize=51, fontweight='bold', ha='center', va='top',
                color=self.colors['secondary'])

        ax.text(50, 90, 'Voorbeelden van gewenst gedrag in input/output paren',
                fontsize=27, ha='center', va='top',
                color=self.colors['text'], alpha=0.7, style='italic')

        # Training examples appear one by one
        y_positions = [75, 50, 25]

        for i, (example, y_pos) in enumerate(zip(self.training_examples, y_positions)):
            if progress > i * 0.25:
                example_alpha = min(1.0, (progress - i * 0.25) / 0.20)

                # Box for example
                box_width = 80
                box_height = 20
                box_x = 10

                example_box = FancyBboxPatch(
                    (box_x, y_pos - box_height/2), box_width, box_height,
                    boxstyle="round,pad=1",
                    facecolor=self.colors['bg_light'],
                    edgecolor=self.colors['secondary'],
                    linewidth=2,
                    alpha=0.9 * example_alpha
                )
                ax.add_patch(example_box)

                # Category badge
                ax.text(box_x + 2, y_pos + box_height/2 - 2, example['category'],
                        fontsize=13, ha='left', va='top',
                        bbox=dict(boxstyle='round,pad=0.3',
                                facecolor=self.colors['purple'],
                                edgecolor='none',
                                alpha=0.8),
                        color='white',
                        fontweight='bold',
                        alpha=example_alpha)

                # Input
                wrapped_input = textwrap.fill(f"[>>] Input: {example['input']}", width=60)
                ax.text(box_x + box_width/2, y_pos + 4, wrapped_input,
                        fontsize=21, ha='center', va='center',
                        color=self.colors['accent'],
                        alpha=example_alpha,
                        fontweight='bold')

                # Output
                wrapped_output = textwrap.fill(f"[<<] Output: {example['output']}", width=60)
                ax.text(box_x + box_width/2, y_pos - 4, wrapped_output,
                        fontsize=13, ha='center', va='center',
                        color=self.colors['text'],
                        alpha=example_alpha * 0.9)

        # Data count indicator
        if progress > 0.8:
            count_alpha = min(1.0, (progress - 0.8) / 0.2)

            ax.text(50, 8, '[DB] Typisch: 100-10.000+ voorbeelden nodig',
                    fontsize=19, ha='center', va='center',
                    bbox=dict(boxstyle='round,pad=0.5',
                            facecolor=self.colors['bg_light'],
                            edgecolor=self.colors['highlight'],
                            linewidth=2,
                            alpha=0.9),
                    color=self.colors['highlight'],
                    fontweight='bold',
                    alpha=count_alpha)

        self.add_status_indicator(progress < 1.0)
        plt.tight_layout()

    def draw_model_predictions(self, progress: float):
        """Step 3: Show that model makes errors - visualize THE PROBLEM"""
        self.fig.clear()
        ax = self.fig.add_subplot(111)
        ax.axis('off')
        ax.set_xlim(0, 100)
        ax.set_ylim(0, 100)

        # Title
        ax.text(50, 96, 'Stap 3: Het Probleem - Model Maakt Fouten!',
                fontsize=48, fontweight='bold', ha='center', va='top',
                color=self.colors['error'])

        ax.text(50, 90, 'Zonder training geeft het model vaak verkeerde antwoorden',
                fontsize=24, ha='center', va='top',
                color=self.colors['text'], alpha=0.7, style='italic')

        # Input question
        if progress > 0.05:
            input_alpha = min(1.0, (progress - 0.05) / 0.1)

            input_box = FancyBboxPatch(
                (15, 76), 70, 9,
                boxstyle="round,pad=0.8",
                facecolor=self.colors['bg_light'],
                edgecolor=self.colors['accent'],
                linewidth=3,
                alpha=0.95 * input_alpha
            )
            ax.add_patch(input_box)

            ax.text(50, 80.5, '[?] Input: "Hoe maak ik risotto?"',
                   fontsize=27, ha='center', va='center',
                   color=self.colors['accent'],
                   fontweight='bold',
                   alpha=input_alpha)

        # Model (center)
        if progress > 0.15:
            model_alpha = min(1.0, (progress - 0.15) / 0.15)

            model_box = FancyBboxPatch(
                (35, 56), 30, 16,
                boxstyle="round,pad=1",
                facecolor='#1a2a4a',
                edgecolor=self.colors['primary'],
                linewidth=3,
                alpha=0.9 * model_alpha
            )
            ax.add_patch(model_box)

            ax.text(50, 67, 'AI', fontsize=52, ha='center', va='center',
                   color='white', alpha=model_alpha)
            ax.text(50, 59, 'Base Model\n(Niet getraind)', fontsize=16, ha='center', va='center',
                   color=self.colors['primary'], alpha=model_alpha)

            # Arrow from input to model
            arrow = FancyArrowPatch(
                (50, 76), (50, 72),
                arrowstyle='-|>',
                mutation_scale=25,
                linewidth=3,
                color=self.colors['accent'],
                alpha=model_alpha
            )
            ax.add_artist(arrow)

        # Model Output (WRONG - left bottom)
        if progress > 0.3:
            output_alpha = min(1.0, (progress - 0.3) / 0.2)

            # Arrow from model to output
            arrow = FancyArrowPatch(
                (40, 56), (28, 48),
                arrowstyle='-|>',
                mutation_scale=25,
                linewidth=3,
                color=self.colors['error'],
                alpha=output_alpha
            )
            ax.add_artist(arrow)

            output_box = FancyBboxPatch(
                (5, 28), 38, 20,
                boxstyle="round,pad=1",
                facecolor='#3a1a1a',
                edgecolor=self.colors['error'],
                linewidth=3,
                alpha=0.95 * output_alpha
            )
            ax.add_patch(output_box)

            ax.text(24, 44, '[X] Model Output (Fout!)',
                   fontsize=18, ha='center', va='center',
                   color=self.colors['error'],
                   fontweight='bold',
                   alpha=output_alpha)

            wrong_answer = textwrap.fill(
                "Risotto is een Italiaanse rijstschotel. Je maakt het door rijst te koken met bouillon.",
                width=32
            )
            ax.text(24, 35, wrong_answer,
                   fontsize=14, ha='center', va='center',
                   color=self.colors['text'],
                   alpha=output_alpha * 0.9)

        # Desired Output (CORRECT - right bottom)
        if progress > 0.55:
            target_alpha = min(1.0, (progress - 0.55) / 0.2)

            # Arrow from model to desired output
            arrow = FancyArrowPatch(
                (60, 56), (72, 48),
                arrowstyle='-|>',
                mutation_scale=25,
                linewidth=3,
                color=self.colors['secondary'],
                alpha=target_alpha
            )
            ax.add_artist(arrow)

            target_box = FancyBboxPatch(
                (57, 28), 38, 20,
                boxstyle="round,pad=1",
                facecolor='#1a3a1a',
                edgecolor=self.colors['secondary'],
                linewidth=3,
                alpha=0.95 * target_alpha
            )
            ax.add_patch(target_box)

            ax.text(76, 44, '[OK] Gewenst Output (Correct)',
                   fontsize=18, ha='center', va='center',
                   color=self.colors['secondary'],
                   fontweight='bold',
                   alpha=target_alpha)

            correct_answer = textwrap.fill(
                "Voor risotto: fruit ui, bak arborio rijst glazig, voeg lepel voor lepel warme bouillon toe onder constant roeren. Na 18 min is de rijst romig en al dente. Finish met boter en parmezaan.",
                width=32
            )
            ax.text(76, 35, correct_answer,
                   fontsize=14, ha='center', va='center',
                   color=self.colors['text'],
                   alpha=target_alpha * 0.95)

        # Difference indicator
        if progress > 0.78:
            diff_alpha = min(1.0, (progress - 0.78) / 0.15)

            # Large warning symbol between both outputs
            ax.text(50, 25, '✗', fontsize=60, ha='center', va='center',
                   color=self.colors['highlight'], alpha=diff_alpha, fontweight='bold')

            diff_box = FancyBboxPatch(
                (35, 10), 30, 8,
                boxstyle="round,pad=0.6",
                facecolor=self.colors['highlight'],
                edgecolor='white',
                linewidth=3,
                alpha=0.95 * diff_alpha
            )
            ax.add_patch(diff_box)

            ax.text(50, 14, 'Groot Verschil!',
                   fontsize=21, ha='center', va='center',
                   color='white',
                   fontweight='bold',
                   alpha=diff_alpha)

        # Problem statement - only show when difference is fully visible
        if progress > 0.88:
            problem_alpha = min(1.0, (progress - 0.88) / 0.12)

            problem_box = FancyBboxPatch(
                (10, 1), 80, 8,
                boxstyle="round,pad=0.8",
                facecolor=self.colors['bg_light'],
                edgecolor=self.colors['accent'],
                linewidth=4,
                alpha=0.95 * problem_alpha
            )
            ax.add_patch(problem_box)

            ax.text(50, 6.5, '>> Het Doel van Finetuning:',
                   fontsize=21, ha='center', va='center',
                   color=self.colors['accent'],
                   fontweight='bold',
                   alpha=problem_alpha)

            ax.text(50, 3, 'Het verschil tussen Model Output en Gewenst Output MINIMALISEREN',
                   fontsize=16, ha='center', va='center',
                   color=self.colors['text'],
                   alpha=problem_alpha * 0.9)

        self.add_status_indicator(progress < 1.0)
        # Don't use tight_layout for this slide - causes centering/folding issues during animation

    def draw_loss_function(self, progress: float):
        """Step 4: Show loss function concept"""
        self.fig.clear()
        ax = self.fig.add_subplot(111)
        ax.axis('off')
        ax.set_xlim(0, 100)
        ax.set_ylim(0, 100)

        # Title
        ax.text(50, 97, 'Stap 4: Loss Function - Fouten Meten',
                fontsize=51, fontweight='bold', ha='center', va='top',
                color=self.colors['accent'])

        ax.text(50, 90, 'Hoe goed komt het model output overeen met gewenst antwoord?',
                fontsize=27, ha='center', va='top',
                color=self.colors['text'], alpha=0.7, style='italic')

        # Model in center
        if progress > 0.1:
            model_alpha = min(1.0, (progress - 0.1) / 0.15)

            model_box = FancyBboxPatch(
                (35, 45), 30, 20,
                boxstyle="round,pad=1",
                facecolor='#1a2a4a',
                edgecolor=self.colors['primary'],
                linewidth=3,
                alpha=0.9 * model_alpha
            )
            ax.add_patch(model_box)

            ax.text(50, 58, 'AI', fontsize=60, ha='center', va='center',
                    alpha=model_alpha)
            ax.text(50, 48, 'Model', fontsize=18, ha='center', va='center',
                    color=self.colors['primary'], fontweight='bold',
                    alpha=model_alpha)

        # Input (left)
        if progress > 0.25:
            input_alpha = min(1.0, (progress - 0.25) / 0.15)

            input_box = FancyBboxPatch(
                (5, 50), 25, 10,
                boxstyle="round,pad=0.5",
                facecolor=self.colors['bg_light'],
                edgecolor=self.colors['secondary'],
                linewidth=2,
                alpha=0.9 * input_alpha
            )
            ax.add_patch(input_box)

            ax.text(17.5, 55, 'Hoe kook ik pasta?',
                    fontsize=21, ha='center', va='center',
                    color=self.colors['text'],
                    alpha=input_alpha)

            # Arrow to model
            arrow = FancyArrowPatch(
                (30, 55), (35, 55),
                arrowstyle='-|>',
                mutation_scale=20,
                linewidth=2,
                color=self.colors['secondary'],
                alpha=input_alpha
            )
            ax.add_artist(arrow)

        # Model output (right top - wrong)
        if progress > 0.4:
            output_alpha = min(1.0, (progress - 0.4) / 0.15)

            output_box = FancyBboxPatch(
                (70, 60), 25, 12,
                boxstyle="round,pad=0.5",
                facecolor='#3a1a1a',
                edgecolor=self.colors['error'],
                linewidth=2,
                alpha=0.9 * output_alpha
            )
            ax.add_patch(output_box)

            ax.text(82.5, 68, '[X] Model Output',
                    fontsize=13, ha='center', va='center',
                    color=self.colors['error'],
                    fontweight='bold',
                    alpha=output_alpha)

            wrapped_output = textwrap.fill("Kook rijst met water...", width=20)
            ax.text(82.5, 63, wrapped_output,
                    fontsize=12, ha='center', va='center',
                    color=self.colors['text'],
                    alpha=output_alpha * 0.8)

            # Arrow from model
            arrow = FancyArrowPatch(
                (65, 58), (70, 64),
                arrowstyle='-|>',
                mutation_scale=20,
                linewidth=2,
                color=self.colors['error'],
                alpha=output_alpha
            )
            ax.add_artist(arrow)

        # Expected output (right bottom - correct)
        if progress > 0.5:
            expected_alpha = min(1.0, (progress - 0.5) / 0.15)

            expected_box = FancyBboxPatch(
                (70, 42), 25, 12,
                boxstyle="round,pad=0.5",
                facecolor='#1a3a1a',
                edgecolor=self.colors['secondary'],
                linewidth=2,
                alpha=0.9 * expected_alpha
            )
            ax.add_patch(expected_box)

            ax.text(82.5, 50, '[OK] Gewenst Output',
                    fontsize=13, ha='center', va='center',
                    color=self.colors['secondary'],
                    fontweight='bold',
                    alpha=expected_alpha)

            wrapped_expected = textwrap.fill("Kook al dente in 8-10 min...", width=20)
            ax.text(82.5, 45, wrapped_expected,
                    fontsize=12, ha='center', va='center',
                    color=self.colors['text'],
                    alpha=expected_alpha * 0.8)

        # Loss calculation
        if progress > 0.65:
            loss_alpha = min(1.0, (progress - 0.65) / 0.25)

            # Comparison arrow
            arrow1 = FancyArrowPatch(
                (82.5, 60), (82.5, 54),
                arrowstyle='<->',
                mutation_scale=25,
                linewidth=3,
                color=self.colors['accent'],
                alpha=loss_alpha
            )
            ax.add_artist(arrow1)

            # Loss value box
            loss_box = FancyBboxPatch(
                (75, 55), 15, 6,
                boxstyle="round,pad=0.3",
                facecolor=self.colors['accent'],
                edgecolor='white',
                linewidth=2,
                alpha=0.95 * loss_alpha
            )
            ax.add_patch(loss_box)

            ax.text(82.5, 58, '[#] Loss = 0.82',
                    fontsize=16, ha='center', va='center',
                    color='white',
                    fontweight='bold',
                    alpha=loss_alpha)

        # Explanation
        if progress > 0.85:
            exp_alpha = min(1.0, (progress - 0.85) / 0.15)

            explanation = "Lagere loss = betere overeenkomst\nDoel: Loss minimaliseren"
            ax.text(50, 25, explanation,
                    fontsize=19, ha='center', va='center',
                    bbox=dict(boxstyle='round,pad=0.8',
                            facecolor=self.colors['bg_light'],
                            edgecolor=self.colors['accent'],
                            linewidth=2,
                            alpha=0.9),
                    color=self.colors['accent'],
                    alpha=exp_alpha,
                    fontweight='bold')

        # Formula hint
        if progress > 0.9:
            formula_alpha = (progress - 0.9) / 0.1
            ax.text(50, 10, 'Cross-Entropy Loss: ℒ = -Σ y log(ŷ)',
                    fontsize=16, ha='center', va='center',
                    color=self.colors['dim'],
                    alpha=0.7 * formula_alpha,
                    style='italic',
                    family='monospace')

        self.add_status_indicator(progress < 1.0)
        plt.tight_layout()

    def draw_gradient_updates(self, progress: float):
        """Step 5: Show gradient descent process"""
        self.fig.clear()
        ax = self.fig.add_subplot(111)
        ax.axis('off')
        ax.set_xlim(0, 100)
        ax.set_ylim(0, 100)

        # Title
        ax.text(50, 97, 'Stap 5: Gradient Updates - Leren!',
                fontsize=51, fontweight='bold', ha='center', va='top',
                color=self.colors['highlight'])

        ax.text(50, 90, 'Model gewichten aanpassen om loss te verlagen',
                fontsize=27, ha='center', va='top',
                color=self.colors['text'], alpha=0.7, style='italic')

        # Loss landscape (valley shape)
        if progress > 0.1:
            landscape_alpha = min(1.0, (progress - 0.1) / 0.2)

            # Draw loss curve - valley (U-shape)
            x = np.linspace(10, 90, 100)
            y_center = 45
            y_min = 30
            y_max = 70

            # Parabola: high at sides, low in middle
            x_normalized = (x - 50) / 40
            y = y_min + (y_max - y_min) * (x_normalized ** 2)

            ax.plot(x, y, color=self.colors['primary'], linewidth=3,
                   alpha=landscape_alpha, zorder=1)

            # Fill under curve
            ax.fill_between(x, y, 20, color=self.colors['primary'],
                           alpha=0.2 * landscape_alpha, zorder=0)

            # Labels
            ax.text(15, 73, 'Hoge Loss', fontsize=16, ha='left', va='center',
                   color=self.colors['error'], fontweight='bold',
                   alpha=landscape_alpha)
            ax.text(85, 73, 'Hoge Loss', fontsize=16, ha='right', va='center',
                   color=self.colors['error'], fontweight='bold',
                   alpha=landscape_alpha)
            ax.text(50, 23, 'Optimale Weights\n(Lage Loss)',
                   fontsize=16, ha='center', va='top',
                   color=self.colors['secondary'], fontweight='bold',
                   alpha=landscape_alpha)

        # Ball rolling down (gradient descent)
        if progress > 0.3:
            descent_progress = min(1.0, (progress - 0.3) / 0.6)

            # Position along curve
            t_eased = 1 - (1 - descent_progress) ** 3

            # Start left top, end in valley
            current_x = 15 + t_eased * 35  # From 15 to 50
            x_normalized = (current_x - 50) / 40
            current_y = y_min + (y_max - y_min) * (x_normalized ** 2)

            # Ball
            ball_size = 800
            ax.scatter([current_x], [current_y], s=ball_size,
                      c=self.colors['highlight'], edgecolors='white',
                      linewidths=3, zorder=10, alpha=0.9)

            # Trail effect
            if descent_progress > 0.1:
                trail_x = np.linspace(15, current_x, 20)
                trail_x_norm = (trail_x - 50) / 40
                trail_y = y_min + (y_max - y_min) * (trail_x_norm ** 2)
                ax.plot(trail_x, trail_y, color=self.colors['highlight'],
                       linewidth=4, alpha=0.5, zorder=5, linestyle='--')

            # Gradient arrow (points downward towards valley)
            if descent_progress < 0.95:
                arrow_length = 10
                dx = arrow_length * (0.5 if current_x < 50 else -0.5)
                dy = -arrow_length * 0.7

                arrow = FancyArrowPatch(
                    (current_x, current_y),
                    (current_x + dx, current_y + dy),
                    arrowstyle='-|>',
                    mutation_scale=30,
                    linewidth=4,
                    color=self.colors['accent'],
                    alpha=0.8,
                    zorder=9
                )
                ax.add_artist(arrow)

                # Gradient label
                ax.text(current_x + dx + 2, current_y + dy - 2, '∇L',
                       fontsize=24, ha='center', va='center',
                       color=self.colors['accent'],
                       fontweight='bold')

        # Iteration counter
        if progress > 0.4:
            iteration = int((progress - 0.4) * 100)
            iter_alpha = min(1.0, (progress - 0.4) / 0.1)

            ax.text(50, 15, f'Iteratie: {iteration}',
                   fontsize=27, ha='center', va='center',
                   bbox=dict(boxstyle='round,pad=0.5',
                           facecolor=self.colors['bg_light'],
                           edgecolor=self.colors['highlight'],
                           linewidth=2,
                           alpha=0.9),
                   color=self.colors['highlight'],
                   fontweight='bold',
                   alpha=iter_alpha)

        # Learning rate hint
        if progress > 0.9:
            lr_alpha = (progress - 0.9) / 0.1
            ax.text(50, 8, '[CFG] Learning Rate (α): hoe grote stappen we nemen',
                   fontsize=16, ha='center', va='center',
                   color=self.colors['dim'],
                   alpha=0.7 * lr_alpha,
                   style='italic')

        self.add_status_indicator(progress < 1.0)
        plt.tight_layout()

    def draw_weight_adjustment(self, progress: float):
        """Step 6: ENHANCED weight adjustments with delta arrows"""
        self.fig.clear()
        ax = self.fig.add_subplot(111)
        ax.axis('off')
        ax.set_xlim(0, 100)
        ax.set_ylim(0, 100)

        # Title
        ax.text(50, 97, 'Stap 6: Weight Adjustment',
                fontsize=51, fontweight='bold', ha='center', va='top',
                color=self.colors['purple'])

        ax.text(50, 89, 'Honderden miljoenen parameters worden aangepast',
                fontsize=27, ha='center', va='top',
                color=self.colors['text'], alpha=0.7, style='italic')

        # Initialize weight delta visualizer
        visualizer = WeightDeltaVisualizer(colors={
            'increase': self.colors['secondary'],
            'decrease': self.colors['warning'],
            'neutral': self.colors['dim']
        })

        # Sample 30 weights for visualization
        num_weights = 30

        # Draw weight comparison with delta arrows
        visualizer.draw_weight_comparison(
            ax,
            before_weights=self.base_weights[:num_weights],
            after_weights=self.finetuned_weights[:num_weights],
            x_before=8,
            x_after=60,
            y_start=25,
            height=55,
            progress=progress
        )

        # Labels
        if progress > 0.2:
            label_alpha = min(1.0, (progress - 0.2) / 0.2)
            ax.text(20, 82, '[O] Voor Finetuning', fontsize=24, ha='center',
                   color=self.colors['primary'], fontweight='bold',
                   alpha=label_alpha)

        if progress > 0.4:
            label_alpha = min(1.0, (progress - 0.4) / 0.2)
            ax.text(72, 82, '[O] Na Finetuning', fontsize=24, ha='center',
                   color=self.colors['secondary'], fontweight='bold',
                   alpha=label_alpha)

        # Delta explanation box
        if progress > 0.8:
            delta_alpha = min(1.0, (progress - 0.8) / 0.2)

            delta_box = FancyBboxPatch(
                (30, 10), 40, 12,
                boxstyle="round,pad=0.8",
                facecolor=self.colors['bg_light'],
                edgecolor=self.colors['purple'],
                linewidth=3,
                alpha=0.95 * delta_alpha
            )
            ax.add_patch(delta_box)

            # Legend
            legend_y = 16
            ax.text(35, legend_y + 3, 'Weight Veranderingen:', fontsize=18,
                   fontweight='bold', color=self.colors['text'],
                   alpha=delta_alpha)

            # Color legend with icons
            ax.text(35, legend_y, '>> Groener = Groter geworden',
                   fontsize=15, color=self.colors['secondary'],
                   alpha=delta_alpha)
            ax.text(35, legend_y - 3, '>> Roder = Kleiner geworden',
                   fontsize=15, color=self.colors['warning'],
                   alpha=delta_alpha)

        # Stats box
        if progress > 0.9:
            stats_alpha = min(1.0, (progress - 0.9) / 0.1)

            ax.text(50, 5, '[#] 7B model ≈ 7.000.000.000 params | 13B model ≈ 13.000.000.000 params',
                   fontsize=16, ha='center', va='center',
                   color=self.colors['text'],
                   alpha=stats_alpha * 0.7,
                   style='italic')

        # Explanation
        if progress > 0.92:
            exp_alpha = (progress - 0.92) / 0.08
            ax.text(50, 8, '[i] Kleine aanpassingen → Grote impact op gedrag',
                   fontsize=24, ha='center', va='center',
                   color=self.colors['accent'],
                   alpha=0.8 * exp_alpha,
                   style='italic')

        self.add_status_indicator(progress < 1.0)
        plt.tight_layout()

    def draw_finetuned_model(self, progress: float):
        """Step 7: Show finetuned model"""
        self.fig.clear()
        ax = self.fig.add_subplot(111)
        ax.axis('off')
        ax.set_xlim(0, 100)
        ax.set_ylim(0, 100)

        # Title
        ax.text(50, 97, 'Stap 7: Gefinetuned Model! [***]',
                fontsize=51, fontweight='bold', ha='center', va='top',
                color=self.colors['secondary'])

        ax.text(50, 90, 'Het model is nu een kook specialist',
                fontsize=27, ha='center', va='top',
                color=self.colors['text'], alpha=0.7, style='italic')

        # Model with glow effect
        if progress > 0.1:
            model_alpha = min(1.0, (progress - 0.1) / 0.2)

            # Pulse effect
            pulse = 1 + 0.1 * np.sin(progress * 15) if progress > 0.4 else 1.0

            # Glow circles
            for radius in [25, 22, 19]:
                glow_alpha = model_alpha * 0.15 * pulse
                glow = Circle((50, 50), radius,
                            facecolor='none',
                            edgecolor=self.colors['secondary'],
                            linewidth=2,
                            alpha=glow_alpha)
                ax.add_patch(glow)

            model_box = FancyBboxPatch(
                (32, 37), 36 * pulse, 26 * pulse,
                boxstyle="round,pad=1.5",
                facecolor='#1a3a2a',
                edgecolor=self.colors['secondary'],
                linewidth=4,
                alpha=0.95 * model_alpha
            )
            ax.add_patch(model_box)

            ax.text(50, 55, 'AI+', fontsize=90, ha='center', va='center',
                    alpha=model_alpha)

            ax.text(50, 42, 'Kook Expert Model',
                    fontsize=27, ha='center', va='center',
                    color=self.colors['secondary'],
                    fontweight='bold',
                    alpha=model_alpha)

        # Capabilities
        capabilities = [
            ('[OK] Kooktechnieken', 20, 70, 0.3),
            ('[OK] Recepten & timing', 80, 70, 0.35),
            ('[OK] Ingrediënten kennis', 20, 30, 0.4),
            ('[OK] Culinaire tips', 80, 30, 0.45)
        ]

        for text, x, y, delay in capabilities:
            if progress > delay:
                cap_alpha = min(1.0, (progress - delay) / 0.15)

                cap_box = FancyBboxPatch(
                    (x - 12, y - 4), 24, 8,
                    boxstyle="round,pad=0.5",
                    facecolor='#1a3a1a',
                    edgecolor=self.colors['secondary'],
                    linewidth=2,
                    alpha=0.9 * cap_alpha
                )
                ax.add_patch(cap_box)

                ax.text(x, y, text,
                        fontsize=16, ha='center', va='center',
                        color=self.colors['text'],
                        fontweight='bold',
                        alpha=cap_alpha)

        # Performance metrics
        if progress > 0.65:
            metrics_alpha = min(1.0, (progress - 0.65) / 0.25)

            metrics_box = FancyBboxPatch(
                (25, 10), 50, 12,
                boxstyle="round,pad=0.8",
                facecolor=self.colors['bg_light'],
                edgecolor=self.colors['highlight'],
                linewidth=3,
                alpha=0.95 * metrics_alpha
            )
            ax.add_patch(metrics_box)

            ax.text(50, 18, '[^] Performance Verbetering', fontsize=18,
                   ha='center', va='center',
                   color=self.colors['highlight'], fontweight='bold',
                   alpha=metrics_alpha)

            ax.text(50, 14, 'Accuraatheid: 65% → 92% | Relevantie: +40%',
                   fontsize=21, ha='center', va='center',
                   color=self.colors['text'],
                   alpha=metrics_alpha)

        self.add_status_indicator(progress < 1.0)
        plt.tight_layout()

    def draw_comparison(self, progress: float):
        """Step 8: Side-by-side comparison"""
        self.fig.clear()
        ax = self.fig.add_subplot(111)
        ax.axis('off')
        ax.set_xlim(0, 100)
        ax.set_ylim(0, 100)

        # Title
        ax.text(50, 97, 'Stap 8: Voor vs Na Vergelijking',
                fontsize=51, fontweight='bold', ha='center', va='top',
                color=self.colors['highlight'])

        ax.text(50, 90, 'Hetzelfde model, maar met domeinkennis',
                fontsize=27, ha='center', va='top',
                color=self.colors['text'], alpha=0.7, style='italic')

        # Question (top)
        if progress > 0.05:
            q_alpha = min(1.0, (progress - 0.05) / 0.1)

            q_box = FancyBboxPatch(
                (15, 78), 70, 8,
                boxstyle="round,pad=0.5",
                facecolor=self.colors['bg_light'],
                edgecolor=self.colors['accent'],
                linewidth=2,
                alpha=0.9 * q_alpha
            )
            ax.add_patch(q_box)

            ax.text(50, 82, '[?] "Wat is het verschil tussen bakken en braden?"',
                   fontsize=16, ha='center', va='center',
                   color=self.colors['accent'],
                   fontweight='bold',
                   alpha=q_alpha)

        # Base Model response (left)
        if progress > 0.2:
            base_alpha = min(1.0, (progress - 0.2) / 0.2)

            ax.text(25, 70, '[O] Base Model', fontsize=19, ha='center',
                   color=self.colors['error'], fontweight='bold',
                   alpha=base_alpha)

            base_box = FancyBboxPatch(
                (5, 35), 40, 30,
                boxstyle="round,pad=1",
                facecolor='#2a1a1a',
                edgecolor=self.colors['error'],
                linewidth=2,
                alpha=0.9 * base_alpha
            )
            ax.add_patch(base_box)

            base_response = textwrap.fill(
                "Bakken en braden zijn beide warmte bereidingsmethoden. "
                "Bakken doe je meestal voor gebak en brood. "
                "Braden wordt gebruikt voor vlees en groenten.",
                width=35
            )

            ax.text(25, 50, base_response,
                   fontsize=13, ha='center', va='center',
                   color=self.colors['text'],
                   alpha=base_alpha * 0.9)

            # Warning
            if progress > 0.35:
                warn_alpha = min(1.0, (progress - 0.35) / 0.15)
                ax.text(25, 38, '(!) Vaag & onnauwkeurig',
                       fontsize=13, ha='center', va='center',
                       color=self.colors['error'],
                       alpha=warn_alpha * 0.8,
                       style='italic')

        # Finetuned Model response (right)
        if progress > 0.5:
            ft_alpha = min(1.0, (progress - 0.5) / 0.2)

            ax.text(75, 70, '[O] Finetuned Model', fontsize=19, ha='center',
                   color=self.colors['secondary'], fontweight='bold',
                   alpha=ft_alpha)

            ft_box = FancyBboxPatch(
                (55, 35), 40, 30,
                boxstyle="round,pad=1",
                facecolor='#1a3a1a',
                edgecolor=self.colors['secondary'],
                linewidth=3,
                alpha=0.95 * ft_alpha
            )
            ax.add_patch(ft_box)

            ft_response = textwrap.fill(
                "Bakken gebeurt in een pan op het fornuis met weinig vet "
                "op matig vuur voor een krokant resultaat. "
                "Braden is in de oven bij hoge temperatuur (160-220°C) "
                "met vocht erbij voor malse, sappige garing. "
                "Bakken = snel & krokant, Braden = langzaam & mals.",
                width=35
            )

            ax.text(75, 50, ft_response,
                   fontsize=13, ha='center', va='center',
                   color=self.colors['text'],
                   alpha=ft_alpha * 0.95)

            # Check
            if progress > 0.65:
                check_alpha = min(1.0, (progress - 0.65) / 0.15)
                ax.text(75, 38, '[OK] Nauwkeurig & specifiek',
                       fontsize=13, ha='center', va='center',
                       color=self.colors['secondary'],
                       alpha=check_alpha * 0.9,
                       fontweight='bold')

        # Scores
        if progress > 0.8:
            score_alpha = min(1.0, (progress - 0.8) / 0.2)

            # Base score
            ax.text(25, 28, '[#] Score: 4/10', fontsize=16, ha='center',
                   bbox=dict(boxstyle='round,pad=0.4',
                           facecolor=self.colors['error'],
                           alpha=0.3),
                   color=self.colors['error'],
                   fontweight='bold',
                   alpha=score_alpha)

            # Finetuned score
            ax.text(75, 28, '[#] Score: 9.5/10', fontsize=16, ha='center',
                   bbox=dict(boxstyle='round,pad=0.4',
                           facecolor=self.colors['secondary'],
                           alpha=0.3),
                   color=self.colors['secondary'],
                   fontweight='bold',
                   alpha=score_alpha)

        # Key takeaway
        if progress > 0.9:
            takeaway_alpha = (progress - 0.9) / 0.1

            ax.text(50, 15, '[i] Finetuning = Model wordt domeinexpert zonder algemene kennis te verliezen',
                   fontsize=24, ha='center', va='center',
                   bbox=dict(boxstyle='round,pad=0.6',
                           facecolor=self.colors['bg_light'],
                           edgecolor=self.colors['highlight'],
                           linewidth=2,
                           alpha=0.9),
                   color=self.colors['highlight'],
                   alpha=takeaway_alpha,
                   fontweight='bold')

        self.add_status_indicator(progress < 1.0)
        plt.tight_layout()

    def draw_azure_local_setup(self, progress: float):
        """Step 9: Azure AI Studio and Local LLM setup"""
        self.fig.clear()
        ax = self.fig.add_subplot(111)
        ax.axis('off')
        ax.set_xlim(0, 100)
        ax.set_ylim(0, 100)

        # Title
        ax.text(50, 97, 'Stap 9: Finetuning in de Praktijk',
                fontsize=51, fontweight='bold', ha='center', va='top',
                color=self.colors['primary'])

        ax.text(50, 90, 'Azure AI Studio vs Local LLM - Beide kunnen!',
                fontsize=27, ha='center', va='top',
                color=self.colors['text'], alpha=0.7, style='italic')

        # Azure AI Studio (left)
        if progress > 0.1:
            azure_alpha = min(1.0, (progress - 0.1) / 0.2)

            azure_box = FancyBboxPatch(
                (5, 25), 40, 55,
                boxstyle="round,pad=1.5",
                facecolor='#1a2a3a',
                edgecolor=self.colors['primary'],
                linewidth=3,
                alpha=0.95 * azure_alpha
            )
            ax.add_patch(azure_box)

            # Azure logo area
            ax.text(25, 75, '[~]', fontsize=75, ha='center', va='center',
                   alpha=azure_alpha)

            ax.text(25, 68, 'Azure AI Studio', fontsize=21, ha='center',
                   color=self.colors['primary'], fontweight='bold',
                   alpha=azure_alpha)

            # Features
            azure_features = [
                ('[OK] Cloud-based', 60),
                ('[OK] GPU compute', 54),
                ('[OK] Managed service', 48),
                ('[OK] GPT-4, Phi-3', 42),
                ('[OK] Auto-scaling', 36)
            ]

            for feat, y in azure_features:
                if progress > 0.2 + (60 - y) * 0.01:
                    feat_alpha = min(1.0, (progress - (0.2 + (60 - y) * 0.01)) / 0.1)
                    ax.text(25, y, feat, fontsize=15, ha='center',
                           color=self.colors['text'],
                           alpha=feat_alpha * azure_alpha)

        # Local LLM (right)
        if progress > 0.4:
            local_alpha = min(1.0, (progress - 0.4) / 0.2)

            local_box = FancyBboxPatch(
                (55, 25), 40, 55,
                boxstyle="round,pad=1.5",
                facecolor='#2a1a3a',
                edgecolor=self.colors['purple'],
                linewidth=3,
                alpha=0.95 * local_alpha
            )
            ax.add_patch(local_box)

            # Computer icon
            ax.text(75, 75, '[PC]', fontsize=75, ha='center', va='center',
                   alpha=local_alpha)

            ax.text(75, 68, 'Local LLM', fontsize=21, ha='center',
                   color=self.colors['purple'], fontweight='bold',
                   alpha=local_alpha)

            # Features
            local_features = [
                ('[OK] On-premise', 60),
                ('[OK] Privacy control', 54),
                ('[OK] LLaMA, Mistral', 48),
                ('[OK] LoRA, QLoRA', 42),
                ('[OK] Cost efficient', 36)
            ]

            for feat, y in local_features:
                if progress > 0.5 + (60 - y) * 0.01:
                    feat_alpha = min(1.0, (progress - (0.5 + (60 - y) * 0.01)) / 0.1)
                    ax.text(75, y, feat, fontsize=15, ha='center',
                           color=self.colors['text'],
                           alpha=feat_alpha * local_alpha)

        # Workflow (bottom Azure)
        if progress > 0.65:
            workflow_alpha = min(1.0, (progress - 0.65) / 0.2)

            azure_steps = "1. Upload data\n2. Select model\n3. Configure\n4. Deploy"
            ax.text(25, 30, azure_steps, fontsize=13, ha='center', va='center',
                   color=self.colors['dim'],
                   alpha=workflow_alpha * 0.8,
                   style='italic')

        # Workflow (bottom Local)
        if progress > 0.75:
            workflow_alpha = min(1.0, (progress - 0.75) / 0.2)

            local_steps = "1. Setup env\n2. Load model\n3. Train script\n4. Evaluate"
            ax.text(75, 30, local_steps, fontsize=13, ha='center', va='center',
                   color=self.colors['dim'],
                   alpha=workflow_alpha * 0.8,
                   style='italic')

        # Bottom comparison
        if progress > 0.85:
            comp_alpha = min(1.0, (progress - 0.85) / 0.15)

            comp_box = FancyBboxPatch(
                (10, 8), 80, 12,
                boxstyle="round,pad=0.8",
                facecolor=self.colors['bg_light'],
                edgecolor=self.colors['secondary'],
                linewidth=2,
                alpha=0.9 * comp_alpha
            )
            ax.add_patch(comp_box)

            ax.text(50, 16, '[=] Keuze afweging', fontsize=18, ha='center',
                   color=self.colors['secondary'], fontweight='bold',
                   alpha=comp_alpha)

            comparison_text = "Azure: Sneller, minder technisch • Local: Meer controle, privacy"
            ax.text(50, 11, comparison_text, fontsize=15, ha='center',
                   color=self.colors['text'],
                   alpha=comp_alpha * 0.9)

        self.add_status_indicator(progress < 1.0)
        plt.tight_layout()


def main():
    """Main entry point for standalone execution"""
    print("="*80)
    print("FINETUNING JOURNEY VISUALISATIE")
    print("="*80)
    print("\n[grad] Deze presentatie legt uit hoe Finetuning werkt:")
    print("  1. Base Model - Pre-trained algemeen model")
    print("  2. Training Data - Voorbeelden van gewenst gedrag")
    print("  3. Model Predictions - Het probleem: foute antwoorden!")
    print("  4. Loss Function - Hoe goed is de output?")
    print("  5. Gradient Updates - Leerproces visualisatie")
    print("  6. Weight Adjustment - Parameters worden aangepast")
    print("  7. Finetuned Model - Het resultaat!")
    print("  8. Comparison - Voor vs Na vergelijking")
    print("  9. Azure AI / Local Setup - Praktische implementatie")
    print("\n[CFG] Technische Details:")
    print("  • Azure AI Studio: Cloud-based, managed, GPT-4/Phi-3")
    print("  • Local LLM: On-premise, LLaMA/Mistral, LoRA/QLoRA")
    print("  • Training: 100-10.000+ voorbeelden typisch")
    print("  • Models: 7B-70B parameters")
    print("\n[Keys]  Controls:")
    print("  SPACE : Volgende stap")
    print("  B     : Vorige stap")
    print("  R     : Reset")
    print("  Q     : Quit")
    print("  F     : Fullscreen")
    print("\n[i] Voorbeeld Use Case:")
    print("  • Doel: Kook-specialist maken van algemeen model")
    print("  • Data: Kooktechnieken, recepten, bereidingsmethoden")
    print("  • Resultaat: Model dat culinaire vragen gedetailleerd beantwoordt")
    print("\n" + "="*80 + "\n")

    presentation = FinetuningPresentation()
    presentation.show()


if __name__ == "__main__":
    main()
