"""
Tokenization: Text to Numbers
How LLMs convert text into something they can process
"""

import sys
import os
import numpy as np
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle, Wedge
import matplotlib.pyplot as plt

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core import BasePresentation, PresentationStyle
from core.animations import AnimationHelper


class TokenizationPresentation(BasePresentation):
    """Tokenization: Text to Numbers"""

    def __init__(self):
        """Initialize the presentation"""
        step_names = [
            'Landing',
            'why_tokenize',
            'token_flow_demo',
            'tokenization_types',
            'bpe_explained',
            'token_counts',
            'special_tokens',
            'tokenizer_differences',
            'practical_tips'
        ]

        super().__init__("Tokenization: Text to Numbers", step_names)

        self.show_landing_page()

    def get_frames_for_step(self, step: int) -> int:
        """Get animation frame count for each step"""
        if False: pass
        elif step == 1: return 90
        elif step == 2: return 120
        elif step == 3: return 90
        elif step == 4: return 120
        elif step == 5: return 90
        elif step == 6: return 90
        elif step == 7: return 90
        elif step == 8: return 90
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

        ax.text(50, 72, 'Tokenization',
                fontsize=66, fontweight='bold', ha='center', va='center',
                color=self.colors['secondary'])

        ax.text(50, 64, 'From Text to Numbers',
                fontsize=30, ha='center', va='center',
                color=self.colors['text'], alpha=0.8, style='italic')

        ax.text(50, 45, 'The first step in language understanding',
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

        ax.text(50, 5, 'Press SPACE to begin',
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
            self.draw_why_tokenize(progress)
        elif self.current_step == 2:
            self.draw_token_flow_demo(progress)
        elif self.current_step == 3:
            self.draw_tokenization_types(progress)
        elif self.current_step == 4:
            self.draw_bpe_explained(progress)
        elif self.current_step == 5:
            self.draw_token_counts(progress)
        elif self.current_step == 6:
            self.draw_special_tokens(progress)
        elif self.current_step == 7:
            self.draw_tokenizer_differences(progress)
        elif self.current_step == 8:
            self.draw_practical_tips(progress)

        if frame >= total_frames - 1:
            self.is_animating = False

    def draw_current_step_static(self):
        """Draw current step without animation"""
        if self.current_step == -1:
            self.show_landing_page()
        elif self.current_step == 1:
            self.draw_why_tokenize(1.0)
        elif self.current_step == 2:
            self.draw_token_flow_demo(1.0)
        elif self.current_step == 3:
            self.draw_tokenization_types(1.0)
        elif self.current_step == 4:
            self.draw_bpe_explained(1.0)
        elif self.current_step == 5:
            self.draw_token_counts(1.0)
        elif self.current_step == 6:
            self.draw_special_tokens(1.0)
        elif self.current_step == 7:
            self.draw_tokenizer_differences(1.0)
        elif self.current_step == 8:
            self.draw_practical_tips(1.0)
        plt.draw()

    def draw_why_tokenize(self, progress: float):
        """Step 1: why_tokenize"""
        self.fig.clear()
        ax = self.fig.add_subplot(111)
        ax.axis('off')
        ax.set_xlim(0, 100)
        ax.set_ylim(0, 100)

        # Title
        title_alpha = min(1.0, progress / 0.2)
        ax.text(50, 95, 'Why Tokenization?',
                fontsize=45, fontweight='bold', ha='center', va='top',
                color=self.colors['primary'], alpha=title_alpha)

        if progress > 0.0:
            t = min(1.0, (progress - 0.0) / 0.2)
            text_alpha = t * t * (3 - 2 * t)
            effective_fontsize = 20
            ax.text(50, 85, 'Computers don\'t understand words - only numbers',
                    fontsize=effective_fontsize, fontweight='bold',
                    ha='center', va='center',
                    color=self.colors['primary'], alpha=text_alpha)

        # Comparison: Left (before/bad)
        if progress > 0.2:
            left_alpha = min(1.0, (progress - 0.2) / 0.1)

            left_box = FancyBboxPatch(
                (7.5, 42.5), 37.5, 25,
                boxstyle="round,pad=1",
                facecolor=self.colors['bg_light'],
                edgecolor=self.colors['primary'],
                linewidth=3,
                alpha=0.95 * left_alpha
            )
            ax.add_patch(left_box)

            ax.text(26.25, 61.25, 'What We See',
                    fontsize=24, fontweight='bold', ha='center', va='center',
                    color=self.colors['primary'], alpha=left_alpha)

            ax.text(26.25, 48.75, 'Hello, how are you today?',
                    fontsize=18, ha='center', va='center',
                    color=self.colors['text'], alpha=left_alpha * 0.9)

        # Comparison: Right (after/good)
        if progress > 0.30000000000000004:
            right_alpha = min(1.0, (progress - 0.30000000000000004) / 0.1)

            right_box = FancyBboxPatch(
                (55.0, 42.5), 37.5, 25,
                boxstyle="round,pad=1",
                facecolor=self.colors['bg_light'],
                edgecolor=self.colors['secondary'],
                linewidth=3,
                alpha=0.95 * right_alpha
            )
            ax.add_patch(right_box)

            ax.text(73.75, 61.25, 'What AI Sees',
                    fontsize=24, fontweight='bold', ha='center', va='center',
                    color=self.colors['secondary'], alpha=right_alpha)

            ax.text(73.75, 48.75, '[15496, 11, 703, 527, 499, 3432, 30]',
                    fontsize=18, ha='center', va='center',
                    color=self.colors['text'], alpha=right_alpha * 0.9)

        if progress > 0.40:
            item_alpha = min(1.0, (progress - 0.40) / 0.07)
            ax.text(20, 22, '• Text -> Tokens -> Token IDs -> Embeddings',
                    fontsize=21, ha='left', va='center',
                    color=self.colors['text'], alpha=item_alpha)

        if progress > 0.47:
            item_alpha = min(1.0, (progress - 0.47) / 0.07)
            ax.text(20, 16, '• Each token = a piece of text with a unique ID',
                    fontsize=21, ha='left', va='center',
                    color=self.colors['text'], alpha=item_alpha)

        if progress > 0.53:
            item_alpha = min(1.0, (progress - 0.53) / 0.07)
            ax.text(20, 10, '• Vocabulary: all tokens the model knows',
                    fontsize=21, ha='left', va='center',
                    color=self.colors['text'], alpha=item_alpha)

        self.add_status_indicator(progress < 1.0)

    def draw_token_flow_demo(self, progress: float):
        """Step 2: token_flow_demo"""
        self.fig.clear()
        ax = self.fig.add_subplot(111)
        ax.axis('off')
        ax.set_xlim(0, 100)
        ax.set_ylim(0, 100)

        # Title
        title_alpha = min(1.0, progress / 0.2)
        ax.text(50, 95, 'The Tokenization Pipeline',
                fontsize=45, fontweight='bold', ha='center', va='top',
                color=self.colors['primary'], alpha=title_alpha)

        if progress > 0.0:
            t = min(1.0, (progress - 0.0) / 0.2)
            text_alpha = t * t * (3 - 2 * t)
            effective_fontsize = 20
            ax.text(50, 90, 'From Text to Embeddings',
                    fontsize=effective_fontsize, fontweight='bold',
                    ha='center', va='center',
                    color=self.colors['primary'], alpha=text_alpha)

        # Token flow pipeline
        if progress > 0.2:
            tf_progress = min(1.0, (progress - 0.2) / 0.2)

            # Stage 1: Input text
            if tf_progress > 0:
                stage1_alpha = min(1.0, tf_progress / 0.25)

                ax.text(15.0, 70, 'Input Text:',
                       fontsize=12, fontweight='bold', ha='left', va='center',
                       color=self.colors['dim'], alpha=stage1_alpha)

                text_box = FancyBboxPatch(
                    (10.0, 60),
                    80, 8,
                    boxstyle="round,pad=0.5",
                    facecolor=self.colors['bg_light'],
                    edgecolor=self.colors['primary'],
                    linewidth=2,
                    alpha=0.95 * stage1_alpha
                )
                ax.add_patch(text_box)

                ax.text(50, 64, '"Hello world"',
                       fontsize=14, ha='center', va='center',
                       color=self.colors['text'], alpha=stage1_alpha)

            # Stage 2: Tokens
            if tf_progress > 0.25:
                stage2_alpha = min(1.0, (tf_progress - 0.25) / 0.25)

                # Arrow
                ax.annotate('', xy=(50, 53),
                           xytext=(50, 59),
                           arrowprops=dict(arrowstyle='->', color=self.colors['accent'],
                                          lw=2), alpha=stage2_alpha)

                ax.text(15.0, 50, 'Tokens:',
                       fontsize=12, fontweight='bold', ha='left', va='center',
                       color=self.colors['dim'], alpha=stage2_alpha)

                # Generate tokens from input
                tokens = 'Hello world'.split()
                token_width = min(12, 80 / (len(tokens) + 1))
                for i, tok in enumerate(tokens):
                    tx = 10.0 + 10 + i * (token_width + 2)
                    tok_box = FancyBboxPatch(
                        (tx, 40),
                        token_width, 8,
                        boxstyle="round,pad=0.3",
                        facecolor=self.colors['bg_light'],
                        edgecolor=self.colors['secondary'],
                        linewidth=1.5,
                        alpha=0.95 * stage2_alpha
                    )
                    ax.add_patch(tok_box)
                    ax.text(tx + token_width/2, 44, tok,
                           fontsize=10, ha='center', va='center',
                           color=self.colors['text'], alpha=stage2_alpha)

            # Stage 3: Embeddings
            if tf_progress > 0.55:
                stage3_alpha = min(1.0, (tf_progress - 0.55) / 0.25)

                ax.annotate('', xy=(50, 35),
                           xytext=(50, 39),
                           arrowprops=dict(arrowstyle='->', color=self.colors['accent'],
                                          lw=2), alpha=stage3_alpha)

                ax.text(15.0, 32, 'Embeddings:',
                       fontsize=12, fontweight='bold', ha='left', va='center',
                       color=self.colors['dim'], alpha=stage3_alpha)

                emb_box = FancyBboxPatch(
                    (10.0, 20),
                    80, 10,
                    boxstyle="round,pad=0.5",
                    facecolor='#1a2e1a',
                    edgecolor=self.colors['success'],
                    linewidth=2,
                    alpha=0.95 * stage3_alpha
                )
                ax.add_patch(emb_box)

                ax.text(50, 25, '[0.23, -0.15, 0.87, ..., 768 dims]',
                       fontsize=11, family='monospace', ha='center', va='center',
                       color='#60ffa8', alpha=stage3_alpha)

        if progress > 0.6:
            t = min(1.0, (progress - 0.6) / 0.20000000000000007)
            text_alpha = t * t * (3 - 2 * t)
            effective_fontsize = 14
            ax.text(50, 12, 'Embeddings capture meaning: similar words have similar vectors',
                    fontsize=effective_fontsize, fontweight='normal',
                    ha='center', va='center',
                    color=self.colors['dim'], alpha=text_alpha)

        self.add_status_indicator(progress < 1.0)

    def draw_tokenization_types(self, progress: float):
        """Step 3: tokenization_types"""
        self.fig.clear()
        ax = self.fig.add_subplot(111)
        ax.axis('off')
        ax.set_xlim(0, 100)
        ax.set_ylim(0, 100)

        # Title
        title_alpha = min(1.0, progress / 0.2)
        ax.text(50, 95, 'Types of Tokenization',
                fontsize=45, fontweight='bold', ha='center', va='top',
                color=self.colors['primary'], alpha=title_alpha)

        if progress > 0.0:
            t = min(1.0, (progress - 0.0) / 0.2)
            text_alpha = t * t * (3 - 2 * t)
            effective_fontsize = 20
            ax.text(50, 88, 'Different Approaches to Splitting Text',
                    fontsize=effective_fontsize, fontweight='bold',
                    ha='center', va='center',
                    color=self.colors['primary'], alpha=text_alpha)

        # Grid item 1
        if progress > 0.20:
            item_alpha = min(1.0, (progress - 0.20) / 0.07)

            grid_box = FancyBboxPatch(
                (12.0, 38.5), 24, 33,
                boxstyle="round,pad=0.8",
                facecolor=self.colors['bg_light'],
                edgecolor=self.colors['warning'],
                linewidth=2,
                alpha=0.9 * item_alpha
            )
            ax.add_patch(grid_box)

            ax.text(24.0, 63.75, '',
                    fontsize=30, ha='center', va='center', alpha=item_alpha)
            ax.text(24.0, 55.0, 'Word-level',
                    fontsize=15, fontweight='bold', ha='center', va='center',
                    color=self.colors['warning'], alpha=item_alpha)
            ax.text(24.0, 46.25, 'hello, world, today',
                    fontsize=11, ha='center', va='center',
                    color=self.colors['text'], alpha=item_alpha * 0.8,
                    linespacing=1.3)

        # Grid item 2
        if progress > 0.27:
            item_alpha = min(1.0, (progress - 0.27) / 0.07)

            grid_box = FancyBboxPatch(
                (38.0, 38.5), 24, 33,
                boxstyle="round,pad=0.8",
                facecolor=self.colors['bg_light'],
                edgecolor=self.colors['dim'],
                linewidth=2,
                alpha=0.9 * item_alpha
            )
            ax.add_patch(grid_box)

            ax.text(50.0, 63.75, '',
                    fontsize=30, ha='center', va='center', alpha=item_alpha)
            ax.text(50.0, 55.0, 'Character',
                    fontsize=15, fontweight='bold', ha='center', va='center',
                    color=self.colors['dim'], alpha=item_alpha)
            ax.text(50.0, 46.25, 'h,e,l,l,o',
                    fontsize=11, ha='center', va='center',
                    color=self.colors['text'], alpha=item_alpha * 0.8,
                    linespacing=1.3)

        # Grid item 3
        if progress > 0.33:
            item_alpha = min(1.0, (progress - 0.33) / 0.07)

            grid_box = FancyBboxPatch(
                (64.0, 38.5), 24, 33,
                boxstyle="round,pad=0.8",
                facecolor=self.colors['bg_light'],
                edgecolor=self.colors['success'],
                linewidth=2,
                alpha=0.9 * item_alpha
            )
            ax.add_patch(grid_box)

            ax.text(76.0, 63.75, '',
                    fontsize=30, ha='center', va='center', alpha=item_alpha)
            ax.text(76.0, 55.0, 'Subword (BPE)',
                    fontsize=15, fontweight='bold', ha='center', va='center',
                    color=self.colors['success'], alpha=item_alpha)
            ax.text(76.0, 46.25, 'hel, lo, wor, ld',
                    fontsize=11, ha='center', va='center',
                    color=self.colors['text'], alpha=item_alpha * 0.8,
                    linespacing=1.3)

        if progress > 0.6:
            t = min(1.0, (progress - 0.6) / 0.20000000000000007)
            text_alpha = t * t * (3 - 2 * t)
            effective_fontsize = 16
            ax.text(50, 18, 'BPE: Best of both worlds - handles rare words AND is efficient',
                    fontsize=effective_fontsize, fontweight='normal',
                    ha='center', va='center',
                    color=self.colors['secondary'], alpha=text_alpha)

        self.add_status_indicator(progress < 1.0)

    def draw_bpe_explained(self, progress: float):
        """Step 4: bpe_explained"""
        self.fig.clear()
        ax = self.fig.add_subplot(111)
        ax.axis('off')
        ax.set_xlim(0, 100)
        ax.set_ylim(0, 100)

        # Title
        title_alpha = min(1.0, progress / 0.2)
        ax.text(50, 95, 'Byte Pair Encoding (BPE)',
                fontsize=45, fontweight='bold', ha='center', va='top',
                color=self.colors['primary'], alpha=title_alpha)

        if progress > 0.0:
            t = min(1.0, (progress - 0.0) / 0.2)
            text_alpha = t * t * (3 - 2 * t)
            effective_fontsize = 20
            ax.text(50, 88, 'How BPE Learns Its Vocabulary',
                    fontsize=effective_fontsize, fontweight='bold',
                    ha='center', va='center',
                    color=self.colors['primary'], alpha=text_alpha)

        # Flow step 1
        if progress > 0.20:
            step_alpha = min(1.0, (progress - 0.20) / 0.05)

            step_box = FancyBboxPatch(
                (7.0, 53), 18.5, 24,
                boxstyle="round,pad=0.5",
                facecolor=self.colors['bg_light'],
                edgecolor=self.colors['warning'],
                linewidth=2,
                alpha=0.95 * step_alpha
            )
            ax.add_patch(step_box)

            ax.text(16.25, 71, '',
                    fontsize=30, ha='center', va='center', alpha=step_alpha)
            ax.text(16.25, 63, '1. Start',
                    fontsize=18, fontweight='bold', ha='center', va='center',
                    color=self.colors['warning'], alpha=step_alpha)
            ax.text(16.25, 57, 'All characters',
                    fontsize=14, ha='center', va='center',
                    color=self.colors['text'], alpha=step_alpha * 0.7)

            if progress > 0.23:
                ax.annotate('', xy=(30.5, 65), xytext=(26.5, 65),
                           arrowprops=dict(arrowstyle='->', color=self.colors['dim'],
                                          lw=2), alpha=step_alpha)

        # Flow step 2
        if progress > 0.25:
            step_alpha = min(1.0, (progress - 0.25) / 0.05)

            step_box = FancyBboxPatch(
                (29.5, 53), 18.5, 24,
                boxstyle="round,pad=0.5",
                facecolor=self.colors['bg_light'],
                edgecolor=self.colors['primary'],
                linewidth=2,
                alpha=0.95 * step_alpha
            )
            ax.add_patch(step_box)

            ax.text(38.75, 71, '',
                    fontsize=30, ha='center', va='center', alpha=step_alpha)
            ax.text(38.75, 63, '2. Count',
                    fontsize=18, fontweight='bold', ha='center', va='center',
                    color=self.colors['primary'], alpha=step_alpha)
            ax.text(38.75, 57, 'Find common pairs',
                    fontsize=14, ha='center', va='center',
                    color=self.colors['text'], alpha=step_alpha * 0.7)

            if progress > 0.28:
                ax.annotate('', xy=(53.0, 65), xytext=(49.0, 65),
                           arrowprops=dict(arrowstyle='->', color=self.colors['dim'],
                                          lw=2), alpha=step_alpha)

        # Flow step 3
        if progress > 0.30:
            step_alpha = min(1.0, (progress - 0.30) / 0.05)

            step_box = FancyBboxPatch(
                (52.0, 53), 18.5, 24,
                boxstyle="round,pad=0.5",
                facecolor=self.colors['bg_light'],
                edgecolor=self.colors['success'],
                linewidth=2,
                alpha=0.95 * step_alpha
            )
            ax.add_patch(step_box)

            ax.text(61.25, 71, '',
                    fontsize=30, ha='center', va='center', alpha=step_alpha)
            ax.text(61.25, 63, '3. Merge',
                    fontsize=18, fontweight='bold', ha='center', va='center',
                    color=self.colors['success'], alpha=step_alpha)
            ax.text(61.25, 57, 'Create new token',
                    fontsize=14, ha='center', va='center',
                    color=self.colors['text'], alpha=step_alpha * 0.7)

            if progress > 0.33:
                ax.annotate('', xy=(75.5, 65), xytext=(71.5, 65),
                           arrowprops=dict(arrowstyle='->', color=self.colors['dim'],
                                          lw=2), alpha=step_alpha)

        # Flow step 4
        if progress > 0.35:
            step_alpha = min(1.0, (progress - 0.35) / 0.05)

            step_box = FancyBboxPatch(
                (74.5, 53), 18.5, 24,
                boxstyle="round,pad=0.5",
                facecolor=self.colors['bg_light'],
                edgecolor=self.colors['accent'],
                linewidth=2,
                alpha=0.95 * step_alpha
            )
            ax.add_patch(step_box)

            ax.text(83.75, 71, '',
                    fontsize=30, ha='center', va='center', alpha=step_alpha)
            ax.text(83.75, 63, '4. Repeat',
                    fontsize=18, fontweight='bold', ha='center', va='center',
                    color=self.colors['accent'], alpha=step_alpha)
            ax.text(83.75, 57, 'Until vocab full',
                    fontsize=14, ha='center', va='center',
                    color=self.colors['text'], alpha=step_alpha * 0.7)

        # Code execution
        if progress > 0.4:
            code_progress = min(1.0, (progress - 0.4) / 0.19999999999999996)

            # Code block
            code_box = FancyBboxPatch(
                (15.0, 38.0),
                70, 14,
                boxstyle="round,pad=0.5",
                facecolor='#1a1a2e',
                edgecolor=self.colors['dim'],
                linewidth=2,
                alpha=0.95 * code_progress
            )
            ax.add_patch(code_box)

            ax.text(50, 45.0,
                   'l o w -> (lo) w -> low\nl o w e r -> (lo) w e r -> low e r',
                   fontsize=12, family='monospace', ha='center', va='center',
                   color='#a8ff60', alpha=code_progress)

        # Output (staggered)
        output_start = 0.5
        if progress > output_start:
            out_progress = min(1.0, (progress - output_start) / (0.6 - output_start))

            # Arrow
            ax.annotate('', xy=(50, 28.0),
                       xytext=(50, 36.0),
                       arrowprops=dict(arrowstyle='->', color=self.colors['accent'],
                                      lw=2), alpha=out_progress)

            # Output box
            out_box = FancyBboxPatch(
                (15.0, 20.0),
                70, 8,
                boxstyle="round,pad=0.5",
                facecolor='#1a2e1a',
                edgecolor=self.colors['success'],
                linewidth=2,
                alpha=0.95 * out_progress
            )
            ax.add_patch(out_box)

            ax.text(50, 24.0,
                   'Vocabulary: [l, o, w, e, r, lo, low, ...]',
                   fontsize=12, family='monospace', ha='center', va='center',
                   color='#60ffa8', alpha=out_progress)

        self.add_status_indicator(progress < 1.0)

    def draw_token_counts(self, progress: float):
        """Step 5: token_counts"""
        self.fig.clear()
        ax = self.fig.add_subplot(111)
        ax.axis('off')
        ax.set_xlim(0, 100)
        ax.set_ylim(0, 100)

        # Title
        title_alpha = min(1.0, progress / 0.2)
        ax.text(50, 95, 'Token Counts Matter',
                fontsize=45, fontweight='bold', ha='center', va='top',
                color=self.colors['primary'], alpha=title_alpha)

        if progress > 0.0:
            t = min(1.0, (progress - 0.0) / 0.2)
            text_alpha = t * t * (3 - 2 * t)
            effective_fontsize = 20
            ax.text(50, 88, 'Why Token Count Affects Cost & Speed',
                    fontsize=effective_fontsize, fontweight='bold',
                    ha='center', va='center',
                    color=self.colors['primary'], alpha=text_alpha)

        # Comparison: Left (before/bad)
        if progress > 0.2:
            left_alpha = min(1.0, (progress - 0.2) / 0.1)

            left_box = FancyBboxPatch(
                (12.5, 47.0), 32.5, 22,
                boxstyle="round,pad=1",
                facecolor=self.colors['bg_light'],
                edgecolor=self.colors['success'],
                linewidth=3,
                alpha=0.95 * left_alpha
            )
            ax.add_patch(left_box)

            ax.text(28.75, 63.5, 'Efficient',
                    fontsize=24, fontweight='bold', ha='center', va='center',
                    color=self.colors['success'], alpha=left_alpha)

            ax.text(28.75, 52.5, '\'Hello\' = 1 token',
                    fontsize=18, ha='center', va='center',
                    color=self.colors['text'], alpha=left_alpha * 0.9)

        # Comparison: Right (after/good)
        if progress > 0.30000000000000004:
            right_alpha = min(1.0, (progress - 0.30000000000000004) / 0.1)

            right_box = FancyBboxPatch(
                (55.0, 47.0), 32.5, 22,
                boxstyle="round,pad=1",
                facecolor=self.colors['bg_light'],
                edgecolor=self.colors['warning'],
                linewidth=3,
                alpha=0.95 * right_alpha
            )
            ax.add_patch(right_box)

            ax.text(71.25, 63.5, 'Expensive',
                    fontsize=24, fontweight='bold', ha='center', va='center',
                    color=self.colors['warning'], alpha=right_alpha)

            ax.text(71.25, 52.5, '\'Cryptocurrency\' = 3 tokens',
                    fontsize=18, ha='center', va='center',
                    color=self.colors['text'], alpha=right_alpha * 0.9)

        if progress > 0.40:
            item_alpha = min(1.0, (progress - 0.40) / 0.05)
            ax.text(20, 28, '• Common words = fewer tokens = cheaper',
                    fontsize=21, ha='left', va='center',
                    color=self.colors['text'], alpha=item_alpha)

        if progress > 0.45:
            item_alpha = min(1.0, (progress - 0.45) / 0.05)
            ax.text(20, 22, '• Rare/technical words = more tokens = more expensive',
                    fontsize=21, ha='left', va='center',
                    color=self.colors['text'], alpha=item_alpha)

        if progress > 0.50:
            item_alpha = min(1.0, (progress - 0.50) / 0.05)
            ax.text(20, 16, '• Different languages tokenize differently',
                    fontsize=21, ha='left', va='center',
                    color=self.colors['text'], alpha=item_alpha)

        if progress > 0.55:
            item_alpha = min(1.0, (progress - 0.55) / 0.05)
            ax.text(20, 10, '• Code often uses more tokens than natural language',
                    fontsize=21, ha='left', va='center',
                    color=self.colors['text'], alpha=item_alpha)

        self.add_status_indicator(progress < 1.0)

    def draw_special_tokens(self, progress: float):
        """Step 6: special_tokens"""
        self.fig.clear()
        ax = self.fig.add_subplot(111)
        ax.axis('off')
        ax.set_xlim(0, 100)
        ax.set_ylim(0, 100)

        # Title
        title_alpha = min(1.0, progress / 0.2)
        ax.text(50, 95, 'Special Tokens',
                fontsize=45, fontweight='bold', ha='center', va='top',
                color=self.colors['primary'], alpha=title_alpha)

        if progress > 0.0:
            t = min(1.0, (progress - 0.0) / 0.2)
            text_alpha = t * t * (3 - 2 * t)
            effective_fontsize = 20
            ax.text(50, 88, 'Tokens With Special Meaning',
                    fontsize=effective_fontsize, fontweight='bold',
                    ha='center', va='center',
                    color=self.colors['primary'], alpha=text_alpha)

        # Grid item 1
        if progress > 0.20:
            item_alpha = min(1.0, (progress - 0.20) / 0.03)

            grid_box = FancyBboxPatch(
                (16.0, 58.5), 33, 13,
                boxstyle="round,pad=0.8",
                facecolor=self.colors['bg_light'],
                edgecolor=self.colors['warning'],
                linewidth=2,
                alpha=0.9 * item_alpha
            )
            ax.add_patch(grid_box)

            ax.text(32.5, 68.75, '',
                    fontsize=30, ha='center', va='center', alpha=item_alpha)
            ax.text(32.5, 65.0, '<|endoftext|>',
                    fontsize=15, fontweight='bold', ha='center', va='center',
                    color=self.colors['warning'], alpha=item_alpha)
            ax.text(32.5, 61.25, 'End of document',
                    fontsize=11, ha='center', va='center',
                    color=self.colors['text'], alpha=item_alpha * 0.8,
                    linespacing=1.3)

        # Grid item 2
        if progress > 0.23:
            item_alpha = min(1.0, (progress - 0.23) / 0.03)

            grid_box = FancyBboxPatch(
                (51.0, 58.5), 33, 13,
                boxstyle="round,pad=0.8",
                facecolor=self.colors['bg_light'],
                edgecolor=self.colors['primary'],
                linewidth=2,
                alpha=0.9 * item_alpha
            )
            ax.add_patch(grid_box)

            ax.text(67.5, 68.75, '',
                    fontsize=30, ha='center', va='center', alpha=item_alpha)
            ax.text(67.5, 65.0, '<|im_start|>',
                    fontsize=15, fontweight='bold', ha='center', va='center',
                    color=self.colors['primary'], alpha=item_alpha)
            ax.text(67.5, 61.25, 'Message start',
                    fontsize=11, ha='center', va='center',
                    color=self.colors['text'], alpha=item_alpha * 0.8,
                    linespacing=1.3)

        # Grid item 3
        if progress > 0.27:
            item_alpha = min(1.0, (progress - 0.27) / 0.03)

            grid_box = FancyBboxPatch(
                (16.0, 43.5), 33, 13,
                boxstyle="round,pad=0.8",
                facecolor=self.colors['bg_light'],
                edgecolor=self.colors['primary'],
                linewidth=2,
                alpha=0.9 * item_alpha
            )
            ax.add_patch(grid_box)

            ax.text(32.5, 53.75, '',
                    fontsize=30, ha='center', va='center', alpha=item_alpha)
            ax.text(32.5, 50.0, '<|im_end|>',
                    fontsize=15, fontweight='bold', ha='center', va='center',
                    color=self.colors['primary'], alpha=item_alpha)
            ax.text(32.5, 46.25, 'Message end',
                    fontsize=11, ha='center', va='center',
                    color=self.colors['text'], alpha=item_alpha * 0.8,
                    linespacing=1.3)

        # Grid item 4
        if progress > 0.30:
            item_alpha = min(1.0, (progress - 0.30) / 0.03)

            grid_box = FancyBboxPatch(
                (51.0, 43.5), 33, 13,
                boxstyle="round,pad=0.8",
                facecolor=self.colors['bg_light'],
                edgecolor=self.colors['dim'],
                linewidth=2,
                alpha=0.9 * item_alpha
            )
            ax.add_patch(grid_box)

            ax.text(67.5, 53.75, '',
                    fontsize=30, ha='center', va='center', alpha=item_alpha)
            ax.text(67.5, 50.0, '[PAD]',
                    fontsize=15, fontweight='bold', ha='center', va='center',
                    color=self.colors['dim'], alpha=item_alpha)
            ax.text(67.5, 46.25, 'Padding for batches',
                    fontsize=11, ha='center', va='center',
                    color=self.colors['text'], alpha=item_alpha * 0.8,
                    linespacing=1.3)

        # Grid item 5
        if progress > 0.33:
            item_alpha = min(1.0, (progress - 0.33) / 0.03)

            grid_box = FancyBboxPatch(
                (16.0, 28.5), 33, 13,
                boxstyle="round,pad=0.8",
                facecolor=self.colors['bg_light'],
                edgecolor=self.colors['warning'],
                linewidth=2,
                alpha=0.9 * item_alpha
            )
            ax.add_patch(grid_box)

            ax.text(32.5, 38.75, '',
                    fontsize=30, ha='center', va='center', alpha=item_alpha)
            ax.text(32.5, 35.0, '[UNK]',
                    fontsize=15, fontweight='bold', ha='center', va='center',
                    color=self.colors['warning'], alpha=item_alpha)
            ax.text(32.5, 31.25, 'Unknown token',
                    fontsize=11, ha='center', va='center',
                    color=self.colors['text'], alpha=item_alpha * 0.8,
                    linespacing=1.3)

        # Grid item 6
        if progress > 0.37:
            item_alpha = min(1.0, (progress - 0.37) / 0.03)

            grid_box = FancyBboxPatch(
                (51.0, 28.5), 33, 13,
                boxstyle="round,pad=0.8",
                facecolor=self.colors['bg_light'],
                edgecolor=self.colors['secondary'],
                linewidth=2,
                alpha=0.9 * item_alpha
            )
            ax.add_patch(grid_box)

            ax.text(67.5, 38.75, '',
                    fontsize=30, ha='center', va='center', alpha=item_alpha)
            ax.text(67.5, 35.0, '[MASK]',
                    fontsize=15, fontweight='bold', ha='center', va='center',
                    color=self.colors['secondary'], alpha=item_alpha)
            ax.text(67.5, 31.25, 'For training (BERT)',
                    fontsize=11, ha='center', va='center',
                    color=self.colors['text'], alpha=item_alpha * 0.8,
                    linespacing=1.3)

        self.add_status_indicator(progress < 1.0)

    def draw_tokenizer_differences(self, progress: float):
        """Step 7: tokenizer_differences"""
        self.fig.clear()
        ax = self.fig.add_subplot(111)
        ax.axis('off')
        ax.set_xlim(0, 100)
        ax.set_ylim(0, 100)

        # Title
        title_alpha = min(1.0, progress / 0.2)
        ax.text(50, 95, 'Different Models, Different Tokenizers',
                fontsize=45, fontweight='bold', ha='center', va='top',
                color=self.colors['primary'], alpha=title_alpha)

        if progress > 0.0:
            t = min(1.0, (progress - 0.0) / 0.2)
            text_alpha = t * t * (3 - 2 * t)
            effective_fontsize = 20
            ax.text(50, 88, 'Each Model Family Has Its Own Tokenizer',
                    fontsize=effective_fontsize, fontweight='bold',
                    ha='center', va='center',
                    color=self.colors['primary'], alpha=text_alpha)

        # Model comparison table
        if progress > 0.2:
            mc_progress = min(1.0, (progress - 0.2) / 0.2)

            # Header row
            for i, model in enumerate(['GPT-4', 'Claude', 'Llama']):
                x = 7.5 + 21.25 * (i + 1.5)
                ax.text(x, 67.0, model,
                       fontsize=14, fontweight='bold', ha='center', va='center',
                       color=self.colors['primary'], alpha=mc_progress)

            # Row: Vocabulary
            if mc_progress > 0.33:
                row_alpha = min(1.0, (mc_progress - 0.33) / 0.33)

                ax.text(18.125, 50.0, 'Vocabulary',
                       fontsize=11, ha='center', va='center',
                       color=self.colors['dim'], alpha=row_alpha)

                ax.text(39.375, 50.0, '100K',
                       fontsize=11, ha='center', va='center',
                       color=self.colors['primary'], alpha=row_alpha)

                ax.text(60.625, 50.0, '100K',
                       fontsize=11, ha='center', va='center',
                       color=self.colors['secondary'], alpha=row_alpha)

                ax.text(81.875, 50.0, '32K',
                       fontsize=11, ha='center', va='center',
                       color=self.colors['accent'], alpha=row_alpha)

            # Row: Algorithm
            if mc_progress > 0.67:
                row_alpha = min(1.0, (mc_progress - 0.67) / 0.33)

                ax.text(18.125, 36.666666666666664, 'Algorithm',
                       fontsize=11, ha='center', va='center',
                       color=self.colors['dim'], alpha=row_alpha)

                ax.text(39.375, 36.666666666666664, 'BPE',
                       fontsize=11, ha='center', va='center',
                       color=self.colors['primary'], alpha=row_alpha)

                ax.text(60.625, 36.666666666666664, 'BPE',
                       fontsize=11, ha='center', va='center',
                       color=self.colors['secondary'], alpha=row_alpha)

                ax.text(81.875, 36.666666666666664, 'SentencePiece',
                       fontsize=11, ha='center', va='center',
                       color=self.colors['accent'], alpha=row_alpha)

        if progress > 0.6:
            t = min(1.0, (progress - 0.6) / 0.20000000000000007)
            text_alpha = t * t * (3 - 2 * t)
            effective_fontsize = 14
            ax.text(50, 12, 'Same text = different token counts on different models!',
                    fontsize=effective_fontsize, fontweight='normal',
                    ha='center', va='center',
                    color=self.colors['warning'], alpha=text_alpha)

        self.add_status_indicator(progress < 1.0)

    def draw_practical_tips(self, progress: float):
        """Step 8: practical_tips"""
        self.fig.clear()
        ax = self.fig.add_subplot(111)
        ax.axis('off')
        ax.set_xlim(0, 100)
        ax.set_ylim(0, 100)

        # Title
        title_alpha = min(1.0, progress / 0.2)
        ax.text(50, 95, 'Practical Tips',
                fontsize=45, fontweight='bold', ha='center', va='top',
                color=self.colors['primary'], alpha=title_alpha)

        if progress > 0.0:
            t = min(1.0, (progress - 0.0) / 0.2)
            text_alpha = t * t * (3 - 2 * t)
            effective_fontsize = 22
            ax.text(50, 88, 'Working With Tokens',
                    fontsize=effective_fontsize, fontweight='bold',
                    ha='center', va='center',
                    color=self.colors['primary'], alpha=text_alpha)

        # Checklist item 1
        if progress > 0.20:
            check_alpha = min(1.0, (progress - 0.20) / 0.04)

            ax.text(20, 71.25, '\u2713',
                    fontsize=27, ha='center', va='center',
                    color=self.colors['secondary'], fontweight='bold',
                    alpha=check_alpha)

            ax.text(25, 71.25, '\u2611 Use tiktoken to count tokens before API calls',
                    fontsize=18, ha='left', va='center',
                    color=self.colors['text'], alpha=check_alpha)

        # Checklist item 2
        if progress > 0.24:
            check_alpha = min(1.0, (progress - 0.24) / 0.04)

            ax.text(20, 64.75, '\u2713',
                    fontsize=27, ha='center', va='center',
                    color=self.colors['secondary'], fontweight='bold',
                    alpha=check_alpha)

            ax.text(25, 64.75, '\u2611 Watch for context window limits',
                    fontsize=18, ha='left', va='center',
                    color=self.colors['text'], alpha=check_alpha)

        # Checklist item 3
        if progress > 0.28:
            check_alpha = min(1.0, (progress - 0.28) / 0.04)

            ax.text(20, 58.25, '\u2713',
                    fontsize=27, ha='center', va='center',
                    color=self.colors['secondary'], fontweight='bold',
                    alpha=check_alpha)

            ax.text(25, 58.25, '\u2611 Minimize tokens for cost efficiency',
                    fontsize=18, ha='left', va='center',
                    color=self.colors['text'], alpha=check_alpha)

        # Checklist item 4
        if progress > 0.32:
            check_alpha = min(1.0, (progress - 0.32) / 0.04)

            ax.text(20, 51.75, '\u2713',
                    fontsize=27, ha='center', va='center',
                    color=self.colors['secondary'], fontweight='bold',
                    alpha=check_alpha)

            ax.text(25, 51.75, '\u2611 Be aware: special chars often = extra tokens',
                    fontsize=18, ha='left', va='center',
                    color=self.colors['text'], alpha=check_alpha)

        # Checklist item 5
        if progress > 0.36:
            check_alpha = min(1.0, (progress - 0.36) / 0.04)

            ax.text(20, 45.25, '\u2713',
                    fontsize=27, ha='center', va='center',
                    color=self.colors['secondary'], fontweight='bold',
                    alpha=check_alpha)

            ax.text(25, 45.25, '\u2611 Test tokenization of domain-specific terms',
                    fontsize=18, ha='left', va='center',
                    color=self.colors['text'], alpha=check_alpha)

        if progress > 0.6:
            code_alpha = min(1.0, (progress - 0.6) / 0.20000000000000007)

            code_box = FancyBboxPatch(
                (17.5, 12.0), 65, 12,
                boxstyle="round,pad=0.5",
                facecolor='#1a1a2e',
                edgecolor=self.colors['dim'],
                linewidth=2,
                alpha=0.95 * code_alpha
            )
            ax.add_patch(code_box)

            code_text = 'import tiktoken\nenc = tiktoken.encoding_for_model(\'gpt-4\')\nlen(enc.encode(\'Hello world\'))  # -> 2'
            ax.text(50, 18, code_text,
                    fontsize=14, family='monospace', ha='center', va='center',
                    color='#a8ff60', alpha=code_alpha)

        self.add_status_indicator(progress < 1.0)


def run():
    """Run the presentation"""
    pres = TokenizationPresentation()
    pres.show()


if __name__ == "__main__":
    run()
