"""
Transformers & Attention
Understanding the attention mechanism that powers modern LLMs
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


class TransformersAttentionPresentation(BasePresentation):
    """Transformers & Attention"""

    def __init__(self):
        """Initialize the presentation"""
        step_names = [
            'Landing',
            'what_is_attention',
            'attention_visualization',
            'qkv',
            'multi_head',
            'transformer_architecture',
            'positional_encoding',
            'context_window',
            'summary'
        ]

        super().__init__("Transformers & Attention", step_names)

        self.show_landing_page()

    def get_frames_for_step(self, step: int) -> int:
        """Get animation frame count for each step"""
        if False: pass
        elif step == 1: return 90
        elif step == 2: return 120
        elif step == 3: return 120
        elif step == 4: return 90
        elif step == 5: return 120
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
            edgecolor=self.colors['primary'],
            linewidth=4,
            alpha=0.95
        )
        ax.add_patch(title_box)

        ax.text(50, 72, 'Transformers & Attention',
                fontsize=66, fontweight='bold', ha='center', va='center',
                color=self.colors['primary'])

        ax.text(50, 64, 'The Architecture Behind Modern AI',
                fontsize=30, ha='center', va='center',
                color=self.colors['text'], alpha=0.8, style='italic')

        ax.text(50, 45, 'How language models understand context',
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
            self.draw_what_is_attention(progress)
        elif self.current_step == 2:
            self.draw_attention_visualization(progress)
        elif self.current_step == 3:
            self.draw_qkv(progress)
        elif self.current_step == 4:
            self.draw_multi_head(progress)
        elif self.current_step == 5:
            self.draw_transformer_architecture(progress)
        elif self.current_step == 6:
            self.draw_positional_encoding(progress)
        elif self.current_step == 7:
            self.draw_context_window(progress)
        elif self.current_step == 8:
            self.draw_summary(progress)

        if frame >= total_frames - 1:
            self.is_animating = False

    def draw_current_step_static(self):
        """Draw current step without animation"""
        if self.current_step == -1:
            self.show_landing_page()
        elif self.current_step == 1:
            self.draw_what_is_attention(1.0)
        elif self.current_step == 2:
            self.draw_attention_visualization(1.0)
        elif self.current_step == 3:
            self.draw_qkv(1.0)
        elif self.current_step == 4:
            self.draw_multi_head(1.0)
        elif self.current_step == 5:
            self.draw_transformer_architecture(1.0)
        elif self.current_step == 6:
            self.draw_positional_encoding(1.0)
        elif self.current_step == 7:
            self.draw_context_window(1.0)
        elif self.current_step == 8:
            self.draw_summary(1.0)
        plt.draw()

    def draw_what_is_attention(self, progress: float):
        """Step 1: what_is_attention"""
        self.fig.clear()
        ax = self.fig.add_subplot(111)
        ax.axis('off')
        ax.set_xlim(0, 100)
        ax.set_ylim(0, 100)

        # Title
        title_alpha = min(1.0, progress / 0.2)
        ax.text(50, 95, 'What is Attention?',
                fontsize=45, fontweight='bold', ha='center', va='top',
                color=self.colors['primary'], alpha=title_alpha)

        if progress > 0.0:
            t = min(1.0, (progress - 0.0) / 0.2)
            text_alpha = t * t * (3 - 2 * t)
            effective_fontsize = 20
            ax.text(50, 82, 'The Key Insight: Not all words are equally important',
                    fontsize=effective_fontsize, fontweight='bold',
                    ha='center', va='center',
                    color=self.colors['primary'], alpha=text_alpha)

        # Message 1: user
        if progress > 0.20:
            msg_alpha = min(1.0, (progress - 0.20) / 0.10)

            bubble = FancyBboxPatch(
                (12.5, 57.0),
                35.5, 8,
                boxstyle="round,pad=0.5",
                facecolor=self.colors['bg_light'],
                edgecolor=self.colors['primary'],
                linewidth=2,
                alpha=0.95 * msg_alpha
            )
            ax.add_patch(bubble)

            ax.text(14.5, 63.0, 'Input:',
                   fontsize=10, fontweight='bold', ha='left', va='center',
                   color=self.colors['primary'], alpha=msg_alpha)

            ax.text(14.5, 59.666666666666664, 'The cat sat on the mat because it was tired',
                   fontsize=11, ha='left', va='center',
                   color=self.colors['text'], alpha=msg_alpha)

        # Message 2: assistant
        if progress > 0.30:
            msg_alpha = min(1.0, (progress - 0.30) / 0.10)

            bubble = FancyBboxPatch(
                (50, 45.0),
                35.5, 8,
                boxstyle="round,pad=0.5",
                facecolor=self.colors['bg_light'],
                edgecolor=self.colors['secondary'],
                linewidth=2,
                alpha=0.95 * msg_alpha
            )
            ax.add_patch(bubble)

            ax.text(52, 51.0, 'Model:',
                   fontsize=10, fontweight='bold', ha='left', va='center',
                   color=self.colors['secondary'], alpha=msg_alpha)

            ax.text(52, 47.666666666666664, 'What does \'it\' refer to? The cat!',
                   fontsize=11, ha='left', va='center',
                   color=self.colors['text'], alpha=msg_alpha)

        if progress > 0.40:
            item_alpha = min(1.0, (progress - 0.40) / 0.07)
            ax.text(20, 25, '• Traditional models: process words one by one',
                    fontsize=21, ha='left', va='center',
                    color=self.colors['text'], alpha=item_alpha)

        if progress > 0.47:
            item_alpha = min(1.0, (progress - 0.47) / 0.07)
            ax.text(20, 19, '• Attention: each word \'looks at\' all other words',
                    fontsize=21, ha='left', va='center',
                    color=self.colors['text'], alpha=item_alpha)

        if progress > 0.53:
            item_alpha = min(1.0, (progress - 0.53) / 0.07)
            ax.text(20, 13, '• Learns which relationships matter most',
                    fontsize=21, ha='left', va='center',
                    color=self.colors['text'], alpha=item_alpha)

        self.add_status_indicator(progress < 1.0)

    def draw_attention_visualization(self, progress: float):
        """Step 2: attention_visualization"""
        self.fig.clear()
        ax = self.fig.add_subplot(111)
        ax.axis('off')
        ax.set_xlim(0, 100)
        ax.set_ylim(0, 100)

        # Title
        title_alpha = min(1.0, progress / 0.2)
        ax.text(50, 95, 'Attention in Action',
                fontsize=45, fontweight='bold', ha='center', va='top',
                color=self.colors['primary'], alpha=title_alpha)

        if progress > 0.0:
            t = min(1.0, (progress - 0.0) / 0.2)
            text_alpha = t * t * (3 - 2 * t)
            effective_fontsize = 18
            ax.text(50, 85, 'Self-Attention: Every token attends to every other token',
                    fontsize=effective_fontsize, fontweight='bold',
                    ha='center', va='center',
                    color=self.colors['text'], alpha=text_alpha)

        # Attention heatmap
        if progress > 0.2:
            hm_progress = min(1.0, (progress - 0.2) / 0.2)

            # Title
            ax.text(50, 80.0, 'Attention Weights',
                   fontsize=18, fontweight='bold', ha='center', va='bottom',
                   color=self.colors['text'], alpha=hm_progress)

            # Generate weights if not provided
            np.random.seed(42)
            weights = np.random.rand(5, 5)
            # Make diagonal stronger (self-attention pattern)
            for i in range(min(5, 5)):
                weights[i, i] = 0.7 + np.random.rand() * 0.3

            # Row 0
            if hm_progress > 0.00:
                row_alpha = min(1.0, (hm_progress - 0.00) / 0.20)

                # Row label
                ax.text(23.0, 70.0, 'The',
                       fontsize=12, ha='right', va='center',
                       color=self.colors['text'], alpha=row_alpha)

                # Cell (0, 0)
                w = weights[0, 0]
                cell = FancyBboxPatch(
                    (25.5, 65.5),
                    9.0, 9.0,
                    boxstyle="round,pad=0.1",
                    facecolor=plt.cm.viridis(w),
                    edgecolor='#333',
                    linewidth=0.5,
                    alpha=row_alpha * 0.9
                )
                ax.add_patch(cell)

                ax.text(30.0, 70.0, f'{w:.2f}',
                       fontsize=8, ha='center', va='center',
                       color='white' if w > 0.5 else 'black',
                       alpha=row_alpha)

                # Cell (0, 1)
                w = weights[0, 1]
                cell = FancyBboxPatch(
                    (35.5, 65.5),
                    9.0, 9.0,
                    boxstyle="round,pad=0.1",
                    facecolor=plt.cm.viridis(w),
                    edgecolor='#333',
                    linewidth=0.5,
                    alpha=row_alpha * 0.9
                )
                ax.add_patch(cell)

                ax.text(40.0, 70.0, f'{w:.2f}',
                       fontsize=8, ha='center', va='center',
                       color='white' if w > 0.5 else 'black',
                       alpha=row_alpha)

                # Cell (0, 2)
                w = weights[0, 2]
                cell = FancyBboxPatch(
                    (45.5, 65.5),
                    9.0, 9.0,
                    boxstyle="round,pad=0.1",
                    facecolor=plt.cm.viridis(w),
                    edgecolor='#333',
                    linewidth=0.5,
                    alpha=row_alpha * 0.9
                )
                ax.add_patch(cell)

                ax.text(50.0, 70.0, f'{w:.2f}',
                       fontsize=8, ha='center', va='center',
                       color='white' if w > 0.5 else 'black',
                       alpha=row_alpha)

                # Cell (0, 3)
                w = weights[0, 3]
                cell = FancyBboxPatch(
                    (55.5, 65.5),
                    9.0, 9.0,
                    boxstyle="round,pad=0.1",
                    facecolor=plt.cm.viridis(w),
                    edgecolor='#333',
                    linewidth=0.5,
                    alpha=row_alpha * 0.9
                )
                ax.add_patch(cell)

                ax.text(60.0, 70.0, f'{w:.2f}',
                       fontsize=8, ha='center', va='center',
                       color='white' if w > 0.5 else 'black',
                       alpha=row_alpha)

                # Cell (0, 4)
                w = weights[0, 4]
                cell = FancyBboxPatch(
                    (65.5, 65.5),
                    9.0, 9.0,
                    boxstyle="round,pad=0.1",
                    facecolor=plt.cm.viridis(w),
                    edgecolor='#333',
                    linewidth=0.5,
                    alpha=row_alpha * 0.9
                )
                ax.add_patch(cell)

                ax.text(70.0, 70.0, f'{w:.2f}',
                       fontsize=8, ha='center', va='center',
                       color='white' if w > 0.5 else 'black',
                       alpha=row_alpha)

            # Row 1
            if hm_progress > 0.20:
                row_alpha = min(1.0, (hm_progress - 0.20) / 0.20)

                # Row label
                ax.text(23.0, 60.0, 'cat',
                       fontsize=12, ha='right', va='center',
                       color=self.colors['text'], alpha=row_alpha)

                # Cell (1, 0)
                w = weights[1, 0]
                cell = FancyBboxPatch(
                    (25.5, 55.5),
                    9.0, 9.0,
                    boxstyle="round,pad=0.1",
                    facecolor=plt.cm.viridis(w),
                    edgecolor='#333',
                    linewidth=0.5,
                    alpha=row_alpha * 0.9
                )
                ax.add_patch(cell)

                ax.text(30.0, 60.0, f'{w:.2f}',
                       fontsize=8, ha='center', va='center',
                       color='white' if w > 0.5 else 'black',
                       alpha=row_alpha)

                # Cell (1, 1)
                w = weights[1, 1]
                cell = FancyBboxPatch(
                    (35.5, 55.5),
                    9.0, 9.0,
                    boxstyle="round,pad=0.1",
                    facecolor=plt.cm.viridis(w),
                    edgecolor='#333',
                    linewidth=0.5,
                    alpha=row_alpha * 0.9
                )
                ax.add_patch(cell)

                ax.text(40.0, 60.0, f'{w:.2f}',
                       fontsize=8, ha='center', va='center',
                       color='white' if w > 0.5 else 'black',
                       alpha=row_alpha)

                # Cell (1, 2)
                w = weights[1, 2]
                cell = FancyBboxPatch(
                    (45.5, 55.5),
                    9.0, 9.0,
                    boxstyle="round,pad=0.1",
                    facecolor=plt.cm.viridis(w),
                    edgecolor='#333',
                    linewidth=0.5,
                    alpha=row_alpha * 0.9
                )
                ax.add_patch(cell)

                ax.text(50.0, 60.0, f'{w:.2f}',
                       fontsize=8, ha='center', va='center',
                       color='white' if w > 0.5 else 'black',
                       alpha=row_alpha)

                # Cell (1, 3)
                w = weights[1, 3]
                cell = FancyBboxPatch(
                    (55.5, 55.5),
                    9.0, 9.0,
                    boxstyle="round,pad=0.1",
                    facecolor=plt.cm.viridis(w),
                    edgecolor='#333',
                    linewidth=0.5,
                    alpha=row_alpha * 0.9
                )
                ax.add_patch(cell)

                ax.text(60.0, 60.0, f'{w:.2f}',
                       fontsize=8, ha='center', va='center',
                       color='white' if w > 0.5 else 'black',
                       alpha=row_alpha)

                # Cell (1, 4)
                w = weights[1, 4]
                cell = FancyBboxPatch(
                    (65.5, 55.5),
                    9.0, 9.0,
                    boxstyle="round,pad=0.1",
                    facecolor=plt.cm.viridis(w),
                    edgecolor='#333',
                    linewidth=0.5,
                    alpha=row_alpha * 0.9
                )
                ax.add_patch(cell)

                ax.text(70.0, 60.0, f'{w:.2f}',
                       fontsize=8, ha='center', va='center',
                       color='white' if w > 0.5 else 'black',
                       alpha=row_alpha)

            # Row 2
            if hm_progress > 0.40:
                row_alpha = min(1.0, (hm_progress - 0.40) / 0.20)

                # Row label
                ax.text(23.0, 50.0, 'sat',
                       fontsize=12, ha='right', va='center',
                       color=self.colors['text'], alpha=row_alpha)

                # Cell (2, 0)
                w = weights[2, 0]
                cell = FancyBboxPatch(
                    (25.5, 45.5),
                    9.0, 9.0,
                    boxstyle="round,pad=0.1",
                    facecolor=plt.cm.viridis(w),
                    edgecolor='#333',
                    linewidth=0.5,
                    alpha=row_alpha * 0.9
                )
                ax.add_patch(cell)

                ax.text(30.0, 50.0, f'{w:.2f}',
                       fontsize=8, ha='center', va='center',
                       color='white' if w > 0.5 else 'black',
                       alpha=row_alpha)

                # Cell (2, 1)
                w = weights[2, 1]
                cell = FancyBboxPatch(
                    (35.5, 45.5),
                    9.0, 9.0,
                    boxstyle="round,pad=0.1",
                    facecolor=plt.cm.viridis(w),
                    edgecolor='#333',
                    linewidth=0.5,
                    alpha=row_alpha * 0.9
                )
                ax.add_patch(cell)

                ax.text(40.0, 50.0, f'{w:.2f}',
                       fontsize=8, ha='center', va='center',
                       color='white' if w > 0.5 else 'black',
                       alpha=row_alpha)

                # Cell (2, 2)
                w = weights[2, 2]
                cell = FancyBboxPatch(
                    (45.5, 45.5),
                    9.0, 9.0,
                    boxstyle="round,pad=0.1",
                    facecolor=plt.cm.viridis(w),
                    edgecolor='#333',
                    linewidth=0.5,
                    alpha=row_alpha * 0.9
                )
                ax.add_patch(cell)

                ax.text(50.0, 50.0, f'{w:.2f}',
                       fontsize=8, ha='center', va='center',
                       color='white' if w > 0.5 else 'black',
                       alpha=row_alpha)

                # Cell (2, 3)
                w = weights[2, 3]
                cell = FancyBboxPatch(
                    (55.5, 45.5),
                    9.0, 9.0,
                    boxstyle="round,pad=0.1",
                    facecolor=plt.cm.viridis(w),
                    edgecolor='#333',
                    linewidth=0.5,
                    alpha=row_alpha * 0.9
                )
                ax.add_patch(cell)

                ax.text(60.0, 50.0, f'{w:.2f}',
                       fontsize=8, ha='center', va='center',
                       color='white' if w > 0.5 else 'black',
                       alpha=row_alpha)

                # Cell (2, 4)
                w = weights[2, 4]
                cell = FancyBboxPatch(
                    (65.5, 45.5),
                    9.0, 9.0,
                    boxstyle="round,pad=0.1",
                    facecolor=plt.cm.viridis(w),
                    edgecolor='#333',
                    linewidth=0.5,
                    alpha=row_alpha * 0.9
                )
                ax.add_patch(cell)

                ax.text(70.0, 50.0, f'{w:.2f}',
                       fontsize=8, ha='center', va='center',
                       color='white' if w > 0.5 else 'black',
                       alpha=row_alpha)

            # Row 3
            if hm_progress > 0.60:
                row_alpha = min(1.0, (hm_progress - 0.60) / 0.20)

                # Row label
                ax.text(23.0, 40.0, 'on',
                       fontsize=12, ha='right', va='center',
                       color=self.colors['text'], alpha=row_alpha)

                # Cell (3, 0)
                w = weights[3, 0]
                cell = FancyBboxPatch(
                    (25.5, 35.5),
                    9.0, 9.0,
                    boxstyle="round,pad=0.1",
                    facecolor=plt.cm.viridis(w),
                    edgecolor='#333',
                    linewidth=0.5,
                    alpha=row_alpha * 0.9
                )
                ax.add_patch(cell)

                ax.text(30.0, 40.0, f'{w:.2f}',
                       fontsize=8, ha='center', va='center',
                       color='white' if w > 0.5 else 'black',
                       alpha=row_alpha)

                # Cell (3, 1)
                w = weights[3, 1]
                cell = FancyBboxPatch(
                    (35.5, 35.5),
                    9.0, 9.0,
                    boxstyle="round,pad=0.1",
                    facecolor=plt.cm.viridis(w),
                    edgecolor='#333',
                    linewidth=0.5,
                    alpha=row_alpha * 0.9
                )
                ax.add_patch(cell)

                ax.text(40.0, 40.0, f'{w:.2f}',
                       fontsize=8, ha='center', va='center',
                       color='white' if w > 0.5 else 'black',
                       alpha=row_alpha)

                # Cell (3, 2)
                w = weights[3, 2]
                cell = FancyBboxPatch(
                    (45.5, 35.5),
                    9.0, 9.0,
                    boxstyle="round,pad=0.1",
                    facecolor=plt.cm.viridis(w),
                    edgecolor='#333',
                    linewidth=0.5,
                    alpha=row_alpha * 0.9
                )
                ax.add_patch(cell)

                ax.text(50.0, 40.0, f'{w:.2f}',
                       fontsize=8, ha='center', va='center',
                       color='white' if w > 0.5 else 'black',
                       alpha=row_alpha)

                # Cell (3, 3)
                w = weights[3, 3]
                cell = FancyBboxPatch(
                    (55.5, 35.5),
                    9.0, 9.0,
                    boxstyle="round,pad=0.1",
                    facecolor=plt.cm.viridis(w),
                    edgecolor='#333',
                    linewidth=0.5,
                    alpha=row_alpha * 0.9
                )
                ax.add_patch(cell)

                ax.text(60.0, 40.0, f'{w:.2f}',
                       fontsize=8, ha='center', va='center',
                       color='white' if w > 0.5 else 'black',
                       alpha=row_alpha)

                # Cell (3, 4)
                w = weights[3, 4]
                cell = FancyBboxPatch(
                    (65.5, 35.5),
                    9.0, 9.0,
                    boxstyle="round,pad=0.1",
                    facecolor=plt.cm.viridis(w),
                    edgecolor='#333',
                    linewidth=0.5,
                    alpha=row_alpha * 0.9
                )
                ax.add_patch(cell)

                ax.text(70.0, 40.0, f'{w:.2f}',
                       fontsize=8, ha='center', va='center',
                       color='white' if w > 0.5 else 'black',
                       alpha=row_alpha)

            # Row 4
            if hm_progress > 0.80:
                row_alpha = min(1.0, (hm_progress - 0.80) / 0.20)

                # Row label
                ax.text(23.0, 30.0, 'it',
                       fontsize=12, ha='right', va='center',
                       color=self.colors['text'], alpha=row_alpha)

                # Cell (4, 0)
                w = weights[4, 0]
                cell = FancyBboxPatch(
                    (25.5, 25.5),
                    9.0, 9.0,
                    boxstyle="round,pad=0.1",
                    facecolor=plt.cm.viridis(w),
                    edgecolor='#333',
                    linewidth=0.5,
                    alpha=row_alpha * 0.9
                )
                ax.add_patch(cell)

                ax.text(30.0, 30.0, f'{w:.2f}',
                       fontsize=8, ha='center', va='center',
                       color='white' if w > 0.5 else 'black',
                       alpha=row_alpha)

                # Cell (4, 1)
                w = weights[4, 1]
                cell = FancyBboxPatch(
                    (35.5, 25.5),
                    9.0, 9.0,
                    boxstyle="round,pad=0.1",
                    facecolor=plt.cm.viridis(w),
                    edgecolor='#333',
                    linewidth=0.5,
                    alpha=row_alpha * 0.9
                )
                ax.add_patch(cell)

                ax.text(40.0, 30.0, f'{w:.2f}',
                       fontsize=8, ha='center', va='center',
                       color='white' if w > 0.5 else 'black',
                       alpha=row_alpha)

                # Cell (4, 2)
                w = weights[4, 2]
                cell = FancyBboxPatch(
                    (45.5, 25.5),
                    9.0, 9.0,
                    boxstyle="round,pad=0.1",
                    facecolor=plt.cm.viridis(w),
                    edgecolor='#333',
                    linewidth=0.5,
                    alpha=row_alpha * 0.9
                )
                ax.add_patch(cell)

                ax.text(50.0, 30.0, f'{w:.2f}',
                       fontsize=8, ha='center', va='center',
                       color='white' if w > 0.5 else 'black',
                       alpha=row_alpha)

                # Cell (4, 3)
                w = weights[4, 3]
                cell = FancyBboxPatch(
                    (55.5, 25.5),
                    9.0, 9.0,
                    boxstyle="round,pad=0.1",
                    facecolor=plt.cm.viridis(w),
                    edgecolor='#333',
                    linewidth=0.5,
                    alpha=row_alpha * 0.9
                )
                ax.add_patch(cell)

                ax.text(60.0, 30.0, f'{w:.2f}',
                       fontsize=8, ha='center', va='center',
                       color='white' if w > 0.5 else 'black',
                       alpha=row_alpha)

                # Cell (4, 4)
                w = weights[4, 4]
                cell = FancyBboxPatch(
                    (65.5, 25.5),
                    9.0, 9.0,
                    boxstyle="round,pad=0.1",
                    facecolor=plt.cm.viridis(w),
                    edgecolor='#333',
                    linewidth=0.5,
                    alpha=row_alpha * 0.9
                )
                ax.add_patch(cell)

                ax.text(70.0, 30.0, f'{w:.2f}',
                       fontsize=8, ha='center', va='center',
                       color='white' if w > 0.5 else 'black',
                       alpha=row_alpha)

            ax.text(30.0, 23.0, 'The',
                   fontsize=12, ha='center', va='top',
                   color=self.colors['text'], alpha=hm_progress)

            ax.text(40.0, 23.0, 'cat',
                   fontsize=12, ha='center', va='top',
                   color=self.colors['text'], alpha=hm_progress)

            ax.text(50.0, 23.0, 'sat',
                   fontsize=12, ha='center', va='top',
                   color=self.colors['text'], alpha=hm_progress)

            ax.text(60.0, 23.0, 'on',
                   fontsize=12, ha='center', va='top',
                   color=self.colors['text'], alpha=hm_progress)

            ax.text(70.0, 23.0, 'it',
                   fontsize=12, ha='center', va='top',
                   color=self.colors['text'], alpha=hm_progress)

        if progress > 0.6:
            t = min(1.0, (progress - 0.6) / 0.20000000000000007)
            text_alpha = t * t * (3 - 2 * t)
            effective_fontsize = 14
            ax.text(50, 12, 'Brighter = stronger attention. Notice \'it\' attending to \'cat\'!',
                    fontsize=effective_fontsize, fontweight='normal',
                    ha='center', va='center',
                    color=self.colors['dim'], alpha=text_alpha)

        self.add_status_indicator(progress < 1.0)

    def draw_qkv(self, progress: float):
        """Step 3: qkv"""
        self.fig.clear()
        ax = self.fig.add_subplot(111)
        ax.axis('off')
        ax.set_xlim(0, 100)
        ax.set_ylim(0, 100)

        # Title
        title_alpha = min(1.0, progress / 0.2)
        ax.text(50, 95, 'Query, Key, Value',
                fontsize=45, fontweight='bold', ha='center', va='top',
                color=self.colors['primary'], alpha=title_alpha)

        if progress > 0.0:
            t = min(1.0, (progress - 0.0) / 0.2)
            text_alpha = t * t * (3 - 2 * t)
            effective_fontsize = 22
            ax.text(50, 88, 'The Three Projections',
                    fontsize=effective_fontsize, fontweight='bold',
                    ha='center', va='center',
                    color=self.colors['primary'], alpha=text_alpha)

        # Flow step 1
        if progress > 0.20:
            step_alpha = min(1.0, (progress - 0.20) / 0.07)

            step_box = FancyBboxPatch(
                (9.499999999999998, 53), 24.333333333333332, 24,
                boxstyle="round,pad=0.5",
                facecolor=self.colors['bg_light'],
                edgecolor=self.colors['warning'],
                linewidth=2,
                alpha=0.95 * step_alpha
            )
            ax.add_patch(step_box)

            ax.text(21.666666666666664, 71, '',
                    fontsize=30, ha='center', va='center', alpha=step_alpha)
            ax.text(21.666666666666664, 63, 'Query (Q)',
                    fontsize=18, fontweight='bold', ha='center', va='center',
                    color=self.colors['warning'], alpha=step_alpha)
            ax.text(21.666666666666664, 57, 'What am I looking for?',
                    fontsize=14, ha='center', va='center',
                    color=self.colors['text'], alpha=step_alpha * 0.7)

            if progress > 0.23:
                ax.annotate('', xy=(38.83333333333333, 65), xytext=(34.83333333333333, 65),
                           arrowprops=dict(arrowstyle='->', color=self.colors['dim'],
                                          lw=2), alpha=step_alpha)

        # Flow step 2
        if progress > 0.27:
            step_alpha = min(1.0, (progress - 0.27) / 0.07)

            step_box = FancyBboxPatch(
                (37.833333333333336, 53), 24.333333333333332, 24,
                boxstyle="round,pad=0.5",
                facecolor=self.colors['bg_light'],
                edgecolor=self.colors['primary'],
                linewidth=2,
                alpha=0.95 * step_alpha
            )
            ax.add_patch(step_box)

            ax.text(50.0, 71, '',
                    fontsize=30, ha='center', va='center', alpha=step_alpha)
            ax.text(50.0, 63, 'Key (K)',
                    fontsize=18, fontweight='bold', ha='center', va='center',
                    color=self.colors['primary'], alpha=step_alpha)
            ax.text(50.0, 57, 'What do I contain?',
                    fontsize=14, ha='center', va='center',
                    color=self.colors['text'], alpha=step_alpha * 0.7)

            if progress > 0.30:
                ax.annotate('', xy=(67.16666666666667, 65), xytext=(63.16666666666667, 65),
                           arrowprops=dict(arrowstyle='->', color=self.colors['dim'],
                                          lw=2), alpha=step_alpha)

        # Flow step 3
        if progress > 0.33:
            step_alpha = min(1.0, (progress - 0.33) / 0.07)

            step_box = FancyBboxPatch(
                (66.16666666666666, 53), 24.333333333333332, 24,
                boxstyle="round,pad=0.5",
                facecolor=self.colors['bg_light'],
                edgecolor=self.colors['success'],
                linewidth=2,
                alpha=0.95 * step_alpha
            )
            ax.add_patch(step_box)

            ax.text(78.33333333333333, 71, '',
                    fontsize=30, ha='center', va='center', alpha=step_alpha)
            ax.text(78.33333333333333, 63, 'Value (V)',
                    fontsize=18, fontweight='bold', ha='center', va='center',
                    color=self.colors['success'], alpha=step_alpha)
            ax.text(78.33333333333333, 57, 'What info do I give?',
                    fontsize=14, ha='center', va='center',
                    color=self.colors['text'], alpha=step_alpha * 0.7)

        if progress > 0.4:
            code_alpha = min(1.0, (progress - 0.4) / 0.19999999999999996)

            code_box = FancyBboxPatch(
                (15.0, 33.0), 70, 10,
                boxstyle="round,pad=0.5",
                facecolor='#1a1a2e',
                edgecolor=self.colors['dim'],
                linewidth=2,
                alpha=0.95 * code_alpha
            )
            ax.add_patch(code_box)

            code_text = 'Attention(Q, K, V) = softmax(Q * K^T / sqrt(d)) * V'
            ax.text(50, 38, code_text,
                    fontsize=14, family='monospace', ha='center', va='center',
                    color='#a8ff60', alpha=code_alpha)

        if progress > 0.60:
            item_alpha = min(1.0, (progress - 0.60) / 0.07)
            ax.text(20, 18, '• Q*K = how relevant is each key to my query?',
                    fontsize=21, ha='left', va='center',
                    color=self.colors['text'], alpha=item_alpha)

        if progress > 0.67:
            item_alpha = min(1.0, (progress - 0.67) / 0.07)
            ax.text(20, 12, '• softmax = normalize to probabilities',
                    fontsize=21, ha='left', va='center',
                    color=self.colors['text'], alpha=item_alpha)

        if progress > 0.73:
            item_alpha = min(1.0, (progress - 0.73) / 0.07)
            ax.text(20, 6, '• Multiply by V = weighted sum of values',
                    fontsize=21, ha='left', va='center',
                    color=self.colors['text'], alpha=item_alpha)

        self.add_status_indicator(progress < 1.0)

    def draw_multi_head(self, progress: float):
        """Step 4: multi_head"""
        self.fig.clear()
        ax = self.fig.add_subplot(111)
        ax.axis('off')
        ax.set_xlim(0, 100)
        ax.set_ylim(0, 100)

        # Title
        title_alpha = min(1.0, progress / 0.2)
        ax.text(50, 95, 'Multi-Head Attention',
                fontsize=45, fontweight='bold', ha='center', va='top',
                color=self.colors['primary'], alpha=title_alpha)

        if progress > 0.0:
            t = min(1.0, (progress - 0.0) / 0.2)
            text_alpha = t * t * (3 - 2 * t)
            effective_fontsize = 20
            ax.text(50, 88, 'Multiple Attention Heads = Multiple Perspectives',
                    fontsize=effective_fontsize, fontweight='bold',
                    ha='center', va='center',
                    color=self.colors['primary'], alpha=text_alpha)

        # Grid item 1
        if progress > 0.20:
            item_alpha = min(1.0, (progress - 0.20) / 0.03)

            grid_box = FancyBboxPatch(
                (15.0, 56.0), 16, 13,
                boxstyle="round,pad=0.8",
                facecolor=self.colors['bg_light'],
                edgecolor=self.colors['warning'],
                linewidth=2,
                alpha=0.9 * item_alpha
            )
            ax.add_patch(grid_box)

            ax.text(23.0, 66.25, '',
                    fontsize=30, ha='center', va='center', alpha=item_alpha)
            ax.text(23.0, 62.5, 'Head 1',
                    fontsize=15, fontweight='bold', ha='center', va='center',
                    color=self.colors['warning'], alpha=item_alpha)
            ax.text(23.0, 58.75, 'Syntax',
                    fontsize=11, ha='center', va='center',
                    color=self.colors['text'], alpha=item_alpha * 0.8,
                    linespacing=1.3)

        # Grid item 2
        if progress > 0.23:
            item_alpha = min(1.0, (progress - 0.23) / 0.03)

            grid_box = FancyBboxPatch(
                (33.0, 56.0), 16, 13,
                boxstyle="round,pad=0.8",
                facecolor=self.colors['bg_light'],
                edgecolor=self.colors['warning'],
                linewidth=2,
                alpha=0.9 * item_alpha
            )
            ax.add_patch(grid_box)

            ax.text(41.0, 66.25, '',
                    fontsize=30, ha='center', va='center', alpha=item_alpha)
            ax.text(41.0, 62.5, 'Head 2',
                    fontsize=15, fontweight='bold', ha='center', va='center',
                    color=self.colors['warning'], alpha=item_alpha)
            ax.text(41.0, 58.75, 'Semantics',
                    fontsize=11, ha='center', va='center',
                    color=self.colors['text'], alpha=item_alpha * 0.8,
                    linespacing=1.3)

        # Grid item 3
        if progress > 0.25:
            item_alpha = min(1.0, (progress - 0.25) / 0.03)

            grid_box = FancyBboxPatch(
                (51.0, 56.0), 16, 13,
                boxstyle="round,pad=0.8",
                facecolor=self.colors['bg_light'],
                edgecolor=self.colors['warning'],
                linewidth=2,
                alpha=0.9 * item_alpha
            )
            ax.add_patch(grid_box)

            ax.text(59.0, 66.25, '',
                    fontsize=30, ha='center', va='center', alpha=item_alpha)
            ax.text(59.0, 62.5, 'Head 3',
                    fontsize=15, fontweight='bold', ha='center', va='center',
                    color=self.colors['warning'], alpha=item_alpha)
            ax.text(59.0, 58.75, 'Position',
                    fontsize=11, ha='center', va='center',
                    color=self.colors['text'], alpha=item_alpha * 0.8,
                    linespacing=1.3)

        # Grid item 4
        if progress > 0.28:
            item_alpha = min(1.0, (progress - 0.28) / 0.03)

            grid_box = FancyBboxPatch(
                (69.0, 56.0), 16, 13,
                boxstyle="round,pad=0.8",
                facecolor=self.colors['bg_light'],
                edgecolor=self.colors['warning'],
                linewidth=2,
                alpha=0.9 * item_alpha
            )
            ax.add_patch(grid_box)

            ax.text(77.0, 66.25, '',
                    fontsize=30, ha='center', va='center', alpha=item_alpha)
            ax.text(77.0, 62.5, 'Head 4',
                    fontsize=15, fontweight='bold', ha='center', va='center',
                    color=self.colors['warning'], alpha=item_alpha)
            ax.text(77.0, 58.75, 'Coreference',
                    fontsize=11, ha='center', va='center',
                    color=self.colors['text'], alpha=item_alpha * 0.8,
                    linespacing=1.3)

        # Grid item 5
        if progress > 0.30:
            item_alpha = min(1.0, (progress - 0.30) / 0.03)

            grid_box = FancyBboxPatch(
                (15.0, 41.0), 16, 13,
                boxstyle="round,pad=0.8",
                facecolor=self.colors['bg_light'],
                edgecolor=self.colors['warning'],
                linewidth=2,
                alpha=0.9 * item_alpha
            )
            ax.add_patch(grid_box)

            ax.text(23.0, 51.25, '',
                    fontsize=30, ha='center', va='center', alpha=item_alpha)
            ax.text(23.0, 47.5, 'Head 5',
                    fontsize=15, fontweight='bold', ha='center', va='center',
                    color=self.colors['warning'], alpha=item_alpha)
            ax.text(23.0, 43.75, 'Entities',
                    fontsize=11, ha='center', va='center',
                    color=self.colors['text'], alpha=item_alpha * 0.8,
                    linespacing=1.3)

        # Grid item 6
        if progress > 0.33:
            item_alpha = min(1.0, (progress - 0.33) / 0.03)

            grid_box = FancyBboxPatch(
                (33.0, 41.0), 16, 13,
                boxstyle="round,pad=0.8",
                facecolor=self.colors['bg_light'],
                edgecolor=self.colors['warning'],
                linewidth=2,
                alpha=0.9 * item_alpha
            )
            ax.add_patch(grid_box)

            ax.text(41.0, 51.25, '',
                    fontsize=30, ha='center', va='center', alpha=item_alpha)
            ax.text(41.0, 47.5, 'Head 6',
                    fontsize=15, fontweight='bold', ha='center', va='center',
                    color=self.colors['warning'], alpha=item_alpha)
            ax.text(41.0, 43.75, 'Relations',
                    fontsize=11, ha='center', va='center',
                    color=self.colors['text'], alpha=item_alpha * 0.8,
                    linespacing=1.3)

        # Grid item 7
        if progress > 0.35:
            item_alpha = min(1.0, (progress - 0.35) / 0.03)

            grid_box = FancyBboxPatch(
                (51.0, 41.0), 16, 13,
                boxstyle="round,pad=0.8",
                facecolor=self.colors['bg_light'],
                edgecolor=self.colors['warning'],
                linewidth=2,
                alpha=0.9 * item_alpha
            )
            ax.add_patch(grid_box)

            ax.text(59.0, 51.25, '',
                    fontsize=30, ha='center', va='center', alpha=item_alpha)
            ax.text(59.0, 47.5, 'Head 7',
                    fontsize=15, fontweight='bold', ha='center', va='center',
                    color=self.colors['warning'], alpha=item_alpha)
            ax.text(59.0, 43.75, 'Negation',
                    fontsize=11, ha='center', va='center',
                    color=self.colors['text'], alpha=item_alpha * 0.8,
                    linespacing=1.3)

        # Grid item 8
        if progress > 0.38:
            item_alpha = min(1.0, (progress - 0.38) / 0.03)

            grid_box = FancyBboxPatch(
                (69.0, 41.0), 16, 13,
                boxstyle="round,pad=0.8",
                facecolor=self.colors['bg_light'],
                edgecolor=self.colors['warning'],
                linewidth=2,
                alpha=0.9 * item_alpha
            )
            ax.add_patch(grid_box)

            ax.text(77.0, 51.25, '',
                    fontsize=30, ha='center', va='center', alpha=item_alpha)
            ax.text(77.0, 47.5, 'Head 8',
                    fontsize=15, fontweight='bold', ha='center', va='center',
                    color=self.colors['warning'], alpha=item_alpha)
            ax.text(77.0, 43.75, 'Numbers',
                    fontsize=11, ha='center', va='center',
                    color=self.colors['text'], alpha=item_alpha * 0.8,
                    linespacing=1.3)

        if progress > 0.6:
            t = min(1.0, (progress - 0.6) / 0.20000000000000007)
            text_alpha = t * t * (3 - 2 * t)
            effective_fontsize = 16
            ax.text(50, 20, 'Each head learns to focus on different linguistic features',
                    fontsize=effective_fontsize, fontweight='normal',
                    ha='center', va='center',
                    color=self.colors['text'], alpha=text_alpha)

        self.add_status_indicator(progress < 1.0)

    def draw_transformer_architecture(self, progress: float):
        """Step 5: transformer_architecture"""
        self.fig.clear()
        ax = self.fig.add_subplot(111)
        ax.axis('off')
        ax.set_xlim(0, 100)
        ax.set_ylim(0, 100)

        # Title
        title_alpha = min(1.0, progress / 0.2)
        ax.text(50, 95, 'The Transformer Block',
                fontsize=45, fontweight='bold', ha='center', va='top',
                color=self.colors['primary'], alpha=title_alpha)

        if progress > 0.0:
            t = min(1.0, (progress - 0.0) / 0.2)
            text_alpha = t * t * (3 - 2 * t)
            effective_fontsize = 20
            ax.text(50, 90, 'Stacking Transformer Layers',
                    fontsize=effective_fontsize, fontweight='bold',
                    ha='center', va='center',
                    color=self.colors['primary'], alpha=text_alpha)

        # Stacked box 1
        if progress > 0.20:
            stack_alpha = min(1.0, (progress - 0.20) / 0.04)

            stack_box = FancyBboxPatch(
                (7.5, 81.5), 45, 12,
                boxstyle="round,pad=0.8",
                facecolor=self.colors['bg_light'],
                edgecolor=self.colors['success'],
                linewidth=3,
                alpha=0.95 * stack_alpha
            )
            ax.add_patch(stack_box)

            ax.text(30, 89.5, 'Output',
                    fontsize=21, fontweight='bold', ha='center', va='center',
                    color=self.colors['success'], alpha=stack_alpha)
            ax.text(30, 85.5, 'Final representation',
                    fontsize=14, ha='center', va='center',
                    color=self.colors['text'], alpha=stack_alpha * 0.8)

        # Stacked box 2
        if progress > 0.24:
            stack_alpha = min(1.0, (progress - 0.24) / 0.04)

            stack_box = FancyBboxPatch(
                (9.5, 66.5), 41, 12,
                boxstyle="round,pad=0.8",
                facecolor=self.colors['bg_light'],
                edgecolor=self.colors['accent'],
                linewidth=3,
                alpha=0.95 * stack_alpha
            )
            ax.add_patch(stack_box)

            ax.text(30, 74.5, 'Feed Forward',
                    fontsize=21, fontweight='bold', ha='center', va='center',
                    color=self.colors['accent'], alpha=stack_alpha)
            ax.text(30, 70.5, 'Process each position',
                    fontsize=14, ha='center', va='center',
                    color=self.colors['text'], alpha=stack_alpha * 0.8)

        # Stacked box 3
        if progress > 0.28:
            stack_alpha = min(1.0, (progress - 0.28) / 0.04)

            stack_box = FancyBboxPatch(
                (11.5, 51.5), 37, 12,
                boxstyle="round,pad=0.8",
                facecolor=self.colors['bg_light'],
                edgecolor=self.colors['dim'],
                linewidth=3,
                alpha=0.95 * stack_alpha
            )
            ax.add_patch(stack_box)

            ax.text(30, 59.5, 'Add & Norm',
                    fontsize=21, fontweight='bold', ha='center', va='center',
                    color=self.colors['dim'], alpha=stack_alpha)
            ax.text(30, 55.5, 'Residual connection',
                    fontsize=14, ha='center', va='center',
                    color=self.colors['text'], alpha=stack_alpha * 0.8)

        # Stacked box 4
        if progress > 0.32:
            stack_alpha = min(1.0, (progress - 0.32) / 0.04)

            stack_box = FancyBboxPatch(
                (13.5, 36.5), 33, 12,
                boxstyle="round,pad=0.8",
                facecolor=self.colors['bg_light'],
                edgecolor=self.colors['primary'],
                linewidth=3,
                alpha=0.95 * stack_alpha
            )
            ax.add_patch(stack_box)

            ax.text(30, 44.5, 'Multi-Head Attention',
                    fontsize=21, fontweight='bold', ha='center', va='center',
                    color=self.colors['primary'], alpha=stack_alpha)
            ax.text(30, 40.5, 'Attend to context',
                    fontsize=14, ha='center', va='center',
                    color=self.colors['text'], alpha=stack_alpha * 0.8)

        # Stacked box 5
        if progress > 0.36:
            stack_alpha = min(1.0, (progress - 0.36) / 0.04)

            stack_box = FancyBboxPatch(
                (15.5, 21.5), 29, 12,
                boxstyle="round,pad=0.8",
                facecolor=self.colors['bg_light'],
                edgecolor=self.colors['secondary'],
                linewidth=3,
                alpha=0.95 * stack_alpha
            )
            ax.add_patch(stack_box)

            ax.text(30, 29.5, 'Input Embeddings',
                    fontsize=21, fontweight='bold', ha='center', va='center',
                    color=self.colors['secondary'], alpha=stack_alpha)
            ax.text(30, 25.5, 'Token + Position',
                    fontsize=14, ha='center', va='center',
                    color=self.colors['text'], alpha=stack_alpha * 0.8)

        if progress > 0.40:
            item_alpha = min(1.0, (progress - 0.40) / 0.05)
            ax.text(42, 50, '• GPT-3: 96 layers',
                    fontsize=21, ha='left', va='center',
                    color=self.colors['text'], alpha=item_alpha)

        if progress > 0.45:
            item_alpha = min(1.0, (progress - 0.45) / 0.05)
            ax.text(42, 44, '• GPT-4: ~120 layers',
                    fontsize=21, ha='left', va='center',
                    color=self.colors['text'], alpha=item_alpha)

        if progress > 0.50:
            item_alpha = min(1.0, (progress - 0.50) / 0.05)
            ax.text(42, 38, '• Each layer refines',
                    fontsize=21, ha='left', va='center',
                    color=self.colors['text'], alpha=item_alpha)

        if progress > 0.55:
            item_alpha = min(1.0, (progress - 0.55) / 0.05)
            ax.text(42, 32, '• understanding',
                    fontsize=21, ha='left', va='center',
                    color=self.colors['text'], alpha=item_alpha)

        self.add_status_indicator(progress < 1.0)

    def draw_positional_encoding(self, progress: float):
        """Step 6: positional_encoding"""
        self.fig.clear()
        ax = self.fig.add_subplot(111)
        ax.axis('off')
        ax.set_xlim(0, 100)
        ax.set_ylim(0, 100)

        # Title
        title_alpha = min(1.0, progress / 0.2)
        ax.text(50, 95, 'Positional Encoding',
                fontsize=45, fontweight='bold', ha='center', va='top',
                color=self.colors['primary'], alpha=title_alpha)

        if progress > 0.0:
            t = min(1.0, (progress - 0.0) / 0.2)
            text_alpha = t * t * (3 - 2 * t)
            effective_fontsize = 20
            ax.text(50, 88, 'How does attention know word order?',
                    fontsize=effective_fontsize, fontweight='bold',
                    ha='center', va='center',
                    color=self.colors['primary'], alpha=text_alpha)

        # Comparison: Left (before/bad)
        if progress > 0.2:
            left_alpha = min(1.0, (progress - 0.2) / 0.1)

            left_box = FancyBboxPatch(
                (7.5, 47.5), 37.5, 25,
                boxstyle="round,pad=1",
                facecolor=self.colors['bg_light'],
                edgecolor=self.colors['warning'],
                linewidth=3,
                alpha=0.95 * left_alpha
            )
            ax.add_patch(left_box)

            ax.text(26.25, 66.25, 'Problem',
                    fontsize=24, fontweight='bold', ha='center', va='center',
                    color=self.colors['warning'], alpha=left_alpha)

            ax.text(26.25, 53.75, 'Attention is permutation invariant - word order is lost!',
                    fontsize=18, ha='center', va='center',
                    color=self.colors['text'], alpha=left_alpha * 0.9)

        # Comparison: Right (after/good)
        if progress > 0.30000000000000004:
            right_alpha = min(1.0, (progress - 0.30000000000000004) / 0.1)

            right_box = FancyBboxPatch(
                (55.0, 47.5), 37.5, 25,
                boxstyle="round,pad=1",
                facecolor=self.colors['bg_light'],
                edgecolor=self.colors['success'],
                linewidth=3,
                alpha=0.95 * right_alpha
            )
            ax.add_patch(right_box)

            ax.text(73.75, 66.25, 'Solution',
                    fontsize=24, fontweight='bold', ha='center', va='center',
                    color=self.colors['success'], alpha=right_alpha)

            ax.text(73.75, 53.75, 'Add position info to each embedding',
                    fontsize=18, ha='center', va='center',
                    color=self.colors['text'], alpha=right_alpha * 0.9)

        if progress > 0.4:
            code_alpha = min(1.0, (progress - 0.4) / 0.19999999999999996)

            code_box = FancyBboxPatch(
                (17.5, 24.0), 65, 12,
                boxstyle="round,pad=0.5",
                facecolor='#1a1a2e',
                edgecolor=self.colors['dim'],
                linewidth=2,
                alpha=0.95 * code_alpha
            )
            ax.add_patch(code_box)

            code_text = 'PE(pos, 2i) = sin(pos / 10000^(2i/d))\nPE(pos, 2i+1) = cos(pos / 10000^(2i/d))'
            ax.text(50, 30, code_text,
                    fontsize=14, family='monospace', ha='center', va='center',
                    color='#a8ff60', alpha=code_alpha)

        if progress > 0.6:
            t = min(1.0, (progress - 0.6) / 0.20000000000000007)
            text_alpha = t * t * (3 - 2 * t)
            effective_fontsize = 14
            ax.text(50, 12, 'Unique pattern for each position, learnable relative distances',
                    fontsize=effective_fontsize, fontweight='normal',
                    ha='center', va='center',
                    color=self.colors['dim'], alpha=text_alpha)

        self.add_status_indicator(progress < 1.0)

    def draw_context_window(self, progress: float):
        """Step 7: context_window"""
        self.fig.clear()
        ax = self.fig.add_subplot(111)
        ax.axis('off')
        ax.set_xlim(0, 100)
        ax.set_ylim(0, 100)

        # Title
        title_alpha = min(1.0, progress / 0.2)
        ax.text(50, 95, 'Context Windows',
                fontsize=45, fontweight='bold', ha='center', va='top',
                color=self.colors['primary'], alpha=title_alpha)

        if progress > 0.0:
            t = min(1.0, (progress - 0.0) / 0.2)
            text_alpha = t * t * (3 - 2 * t)
            effective_fontsize = 20
            ax.text(50, 88, 'How Much Can a Model Remember?',
                    fontsize=effective_fontsize, fontweight='bold',
                    ha='center', va='center',
                    color=self.colors['primary'], alpha=text_alpha)

        # Model comparison table
        if progress > 0.2:
            mc_progress = min(1.0, (progress - 0.2) / 0.2)

            # Header row
            for i, model in enumerate(['GPT-3.5', 'GPT-4', 'Claude 3']):
                x = 10.0 + 20.0 * (i + 1.5)
                ax.text(x, 64.5, model,
                       fontsize=14, fontweight='bold', ha='center', va='center',
                       color=self.colors['primary'], alpha=mc_progress)

            # Row: Context
            if mc_progress > 0.33:
                row_alpha = min(1.0, (mc_progress - 0.33) / 0.33)

                ax.text(20.0, 50.0, 'Context',
                       fontsize=11, ha='center', va='center',
                       color=self.colors['dim'], alpha=row_alpha)

                ax.text(40.0, 50.0, '4K',
                       fontsize=11, ha='center', va='center',
                       color=self.colors['dim'], alpha=row_alpha)

                ax.text(60.0, 50.0, '128K',
                       fontsize=11, ha='center', va='center',
                       color=self.colors['primary'], alpha=row_alpha)

                ax.text(80.0, 50.0, '200K',
                       fontsize=11, ha='center', va='center',
                       color=self.colors['secondary'], alpha=row_alpha)

            # Row: Pages
            if mc_progress > 0.67:
                row_alpha = min(1.0, (mc_progress - 0.67) / 0.33)

                ax.text(20.0, 38.333333333333336, 'Pages',
                       fontsize=11, ha='center', va='center',
                       color=self.colors['dim'], alpha=row_alpha)

                ax.text(40.0, 38.333333333333336, '~6',
                       fontsize=11, ha='center', va='center',
                       color=self.colors['dim'], alpha=row_alpha)

                ax.text(60.0, 38.333333333333336, '~200',
                       fontsize=11, ha='center', va='center',
                       color=self.colors['primary'], alpha=row_alpha)

                ax.text(80.0, 38.333333333333336, '~300',
                       fontsize=11, ha='center', va='center',
                       color=self.colors['secondary'], alpha=row_alpha)

        if progress > 0.6:
            t = min(1.0, (progress - 0.6) / 0.20000000000000007)
            text_alpha = t * t * (3 - 2 * t)
            effective_fontsize = 14
            ax.text(50, 15, 'Attention is O(n^2) - longer context = more compute',
                    fontsize=effective_fontsize, fontweight='normal',
                    ha='center', va='center',
                    color=self.colors['warning'], alpha=text_alpha)

        self.add_status_indicator(progress < 1.0)

    def draw_summary(self, progress: float):
        """Step 8: summary"""
        self.fig.clear()
        ax = self.fig.add_subplot(111)
        ax.axis('off')
        ax.set_xlim(0, 100)
        ax.set_ylim(0, 100)

        # Title
        title_alpha = min(1.0, progress / 0.2)
        ax.text(50, 95, 'Key Takeaways',
                fontsize=45, fontweight='bold', ha='center', va='top',
                color=self.colors['primary'], alpha=title_alpha)

        if progress > 0.0:
            t = min(1.0, (progress - 0.0) / 0.2)
            text_alpha = t * t * (3 - 2 * t)
            effective_fontsize = 22
            ax.text(50, 88, 'Transformers: The Building Block of Modern AI',
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

            ax.text(25, 71.25, '\u2611 Attention lets every token see every other token',
                    fontsize=18, ha='left', va='center',
                    color=self.colors['text'], alpha=check_alpha)

        # Checklist item 2
        if progress > 0.24:
            check_alpha = min(1.0, (progress - 0.24) / 0.04)

            ax.text(20, 64.75, '\u2713',
                    fontsize=27, ha='center', va='center',
                    color=self.colors['secondary'], fontweight='bold',
                    alpha=check_alpha)

            ax.text(25, 64.75, '\u2611 Query-Key-Value: the fundamental operation',
                    fontsize=18, ha='left', va='center',
                    color=self.colors['text'], alpha=check_alpha)

        # Checklist item 3
        if progress > 0.28:
            check_alpha = min(1.0, (progress - 0.28) / 0.04)

            ax.text(20, 58.25, '\u2713',
                    fontsize=27, ha='center', va='center',
                    color=self.colors['secondary'], fontweight='bold',
                    alpha=check_alpha)

            ax.text(25, 58.25, '\u2611 Multi-head attention: multiple perspectives',
                    fontsize=18, ha='left', va='center',
                    color=self.colors['text'], alpha=check_alpha)

        # Checklist item 4
        if progress > 0.32:
            check_alpha = min(1.0, (progress - 0.32) / 0.04)

            ax.text(20, 51.75, '\u2713',
                    fontsize=27, ha='center', va='center',
                    color=self.colors['secondary'], fontweight='bold',
                    alpha=check_alpha)

            ax.text(25, 51.75, '\u2611 Positional encoding: preserves word order',
                    fontsize=18, ha='left', va='center',
                    color=self.colors['text'], alpha=check_alpha)

        # Checklist item 5
        if progress > 0.36:
            check_alpha = min(1.0, (progress - 0.36) / 0.04)

            ax.text(20, 45.25, '\u2713',
                    fontsize=27, ha='center', va='center',
                    color=self.colors['secondary'], fontweight='bold',
                    alpha=check_alpha)

            ax.text(25, 45.25, '\u2611 Context window: memory limit of the model',
                    fontsize=18, ha='left', va='center',
                    color=self.colors['text'], alpha=check_alpha)

        if progress > 0.8:
            t = min(1.0, (progress - 0.8) / 0.19999999999999996)
            text_alpha = t * t * (3 - 2 * t)
            effective_fontsize = 16
            ax.text(50, 15, 'This architecture powers GPT, Claude, Llama, and all modern LLMs!',
                    fontsize=effective_fontsize, fontweight='normal',
                    ha='center', va='center',
                    color=self.colors['success'], alpha=text_alpha)

        self.add_status_indicator(progress < 1.0)


def run():
    """Run the presentation"""
    pres = TransformersAttentionPresentation()
    pres.show()


if __name__ == "__main__":
    run()
