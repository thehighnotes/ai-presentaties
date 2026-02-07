"""
AI Agents & Tool Use
How LLMs interact with the real world through tools and planning
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


class AiAgentsPresentation(BasePresentation):
    """AI Agents & Tool Use"""

    def __init__(self):
        """Initialize the presentation"""
        step_names = [
            'Landing',
            'what_is_agent',
            'agent_loop',
            'tools',
            'function_calling',
            'react',
            'planning',
            'memory',
            'safety',
            'examples'
        ]

        super().__init__("AI Agents & Tool Use", step_names)

        self.show_landing_page()

    def get_frames_for_step(self, step: int) -> int:
        """Get animation frame count for each step"""
        if False: pass
        elif step == 1: return 90
        elif step == 2: return 120
        elif step == 3: return 90
        elif step == 4: return 90
        elif step == 5: return 120
        elif step == 6: return 120
        elif step == 7: return 90
        elif step == 8: return 90
        elif step == 9: return 90
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
            edgecolor=self.colors['accent'],
            linewidth=4,
            alpha=0.95
        )
        ax.add_patch(title_box)

        ax.text(50, 72, 'AI Agents',
                fontsize=66, fontweight='bold', ha='center', va='center',
                color=self.colors['accent'])

        ax.text(50, 64, 'From Chat to Action',
                fontsize=30, ha='center', va='center',
                color=self.colors['text'], alpha=0.8, style='italic')

        ax.text(50, 45, 'When AI does more than just talk',
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
            self.draw_what_is_agent(progress)
        elif self.current_step == 2:
            self.draw_agent_loop(progress)
        elif self.current_step == 3:
            self.draw_tools(progress)
        elif self.current_step == 4:
            self.draw_function_calling(progress)
        elif self.current_step == 5:
            self.draw_react(progress)
        elif self.current_step == 6:
            self.draw_planning(progress)
        elif self.current_step == 7:
            self.draw_memory(progress)
        elif self.current_step == 8:
            self.draw_safety(progress)
        elif self.current_step == 9:
            self.draw_examples(progress)

        if frame >= total_frames - 1:
            self.is_animating = False

    def draw_current_step_static(self):
        """Draw current step without animation"""
        if self.current_step == -1:
            self.show_landing_page()
        elif self.current_step == 1:
            self.draw_what_is_agent(1.0)
        elif self.current_step == 2:
            self.draw_agent_loop(1.0)
        elif self.current_step == 3:
            self.draw_tools(1.0)
        elif self.current_step == 4:
            self.draw_function_calling(1.0)
        elif self.current_step == 5:
            self.draw_react(1.0)
        elif self.current_step == 6:
            self.draw_planning(1.0)
        elif self.current_step == 7:
            self.draw_memory(1.0)
        elif self.current_step == 8:
            self.draw_safety(1.0)
        elif self.current_step == 9:
            self.draw_examples(1.0)
        plt.draw()

    def draw_what_is_agent(self, progress: float):
        """Step 1: what_is_agent"""
        self.fig.clear()
        ax = self.fig.add_subplot(111)
        ax.axis('off')
        ax.set_xlim(0, 100)
        ax.set_ylim(0, 100)

        # Title
        title_alpha = min(1.0, progress / 0.2)
        ax.text(50, 95, 'What is an AI Agent?',
                fontsize=45, fontweight='bold', ha='center', va='top',
                color=self.colors['primary'], alpha=title_alpha)

        if progress > 0.0:
            t = min(1.0, (progress - 0.0) / 0.2)
            text_alpha = t * t * (3 - 2 * t)
            effective_fontsize = 22
            ax.text(50, 88, 'More Than Just Conversation',
                    fontsize=effective_fontsize, fontweight='bold',
                    ha='center', va='center',
                    color=self.colors['primary'], alpha=text_alpha)

        # Comparison: Left (before/bad)
        if progress > 0.2:
            left_alpha = min(1.0, (progress - 0.2) / 0.1)

            left_box = FancyBboxPatch(
                (7.5, 46.0), 37.5, 28,
                boxstyle="round,pad=1",
                facecolor=self.colors['bg_light'],
                edgecolor=self.colors['dim'],
                linewidth=3,
                alpha=0.95 * left_alpha
            )
            ax.add_patch(left_box)

            ax.text(26.25, 67.0, 'Chatbot',
                    fontsize=24, fontweight='bold', ha='center', va='center',
                    color=self.colors['dim'], alpha=left_alpha)

            ax.text(26.25, 53.0, 'Answers questions, generates text, stays within the conversation',
                    fontsize=18, ha='center', va='center',
                    color=self.colors['text'], alpha=left_alpha * 0.9)

        # Comparison: Right (after/good)
        if progress > 0.30000000000000004:
            right_alpha = min(1.0, (progress - 0.30000000000000004) / 0.1)

            right_box = FancyBboxPatch(
                (55.0, 46.0), 37.5, 28,
                boxstyle="round,pad=1",
                facecolor=self.colors['bg_light'],
                edgecolor=self.colors['success'],
                linewidth=3,
                alpha=0.95 * right_alpha
            )
            ax.add_patch(right_box)

            ax.text(73.75, 67.0, 'Agent',
                    fontsize=24, fontweight='bold', ha='center', va='center',
                    color=self.colors['success'], alpha=right_alpha)

            ax.text(73.75, 53.0, 'Plans, uses tools, takes actions, accomplishes goals',
                    fontsize=18, ha='center', va='center',
                    color=self.colors['text'], alpha=right_alpha * 0.9)

        if progress > 0.40:
            item_alpha = min(1.0, (progress - 0.40) / 0.07)
            ax.text(20, 25, '• Agents can: search the web, run code, manage files',
                    fontsize=21, ha='left', va='center',
                    color=self.colors['text'], alpha=item_alpha)

        if progress > 0.47:
            item_alpha = min(1.0, (progress - 0.47) / 0.07)
            ax.text(20, 19, '• Agents decide which tools to use and when',
                    fontsize=21, ha='left', va='center',
                    color=self.colors['text'], alpha=item_alpha)

        if progress > 0.53:
            item_alpha = min(1.0, (progress - 0.53) / 0.07)
            ax.text(20, 13, '• Agents iterate until the task is complete',
                    fontsize=21, ha='left', va='center',
                    color=self.colors['text'], alpha=item_alpha)

        self.add_status_indicator(progress < 1.0)

    def draw_agent_loop(self, progress: float):
        """Step 2: agent_loop"""
        self.fig.clear()
        ax = self.fig.add_subplot(111)
        ax.axis('off')
        ax.set_xlim(0, 100)
        ax.set_ylim(0, 100)

        # Title
        title_alpha = min(1.0, progress / 0.2)
        ax.text(50, 95, 'The Agent Loop',
                fontsize=45, fontweight='bold', ha='center', va='top',
                color=self.colors['primary'], alpha=title_alpha)

        if progress > 0.0:
            t = min(1.0, (progress - 0.0) / 0.2)
            text_alpha = t * t * (3 - 2 * t)
            effective_fontsize = 20
            ax.text(50, 88, 'Think -> Act -> Observe -> Repeat',
                    fontsize=effective_fontsize, fontweight='bold',
                    ha='center', va='center',
                    color=self.colors['primary'], alpha=text_alpha)

        # Flow step 1
        if progress > 0.20:
            step_alpha = min(1.0, (progress - 0.20) / 0.05)

            step_box = FancyBboxPatch(
                (7.0, 48), 18.5, 24,
                boxstyle="round,pad=0.5",
                facecolor=self.colors['bg_light'],
                edgecolor=self.colors['warning'],
                linewidth=2,
                alpha=0.95 * step_alpha
            )
            ax.add_patch(step_box)

            ax.text(16.25, 66, '',
                    fontsize=30, ha='center', va='center', alpha=step_alpha)
            ax.text(16.25, 58, 'Think',
                    fontsize=18, fontweight='bold', ha='center', va='center',
                    color=self.colors['warning'], alpha=step_alpha)
            ax.text(16.25, 52, 'Reason about goal',
                    fontsize=14, ha='center', va='center',
                    color=self.colors['text'], alpha=step_alpha * 0.7)

            if progress > 0.23:
                ax.annotate('', xy=(30.5, 60), xytext=(26.5, 60),
                           arrowprops=dict(arrowstyle='->', color=self.colors['dim'],
                                          lw=2), alpha=step_alpha)

        # Flow step 2
        if progress > 0.25:
            step_alpha = min(1.0, (progress - 0.25) / 0.05)

            step_box = FancyBboxPatch(
                (29.5, 48), 18.5, 24,
                boxstyle="round,pad=0.5",
                facecolor=self.colors['bg_light'],
                edgecolor=self.colors['primary'],
                linewidth=2,
                alpha=0.95 * step_alpha
            )
            ax.add_patch(step_box)

            ax.text(38.75, 66, '',
                    fontsize=30, ha='center', va='center', alpha=step_alpha)
            ax.text(38.75, 58, 'Decide',
                    fontsize=18, fontweight='bold', ha='center', va='center',
                    color=self.colors['primary'], alpha=step_alpha)
            ax.text(38.75, 52, 'Choose action',
                    fontsize=14, ha='center', va='center',
                    color=self.colors['text'], alpha=step_alpha * 0.7)

            if progress > 0.28:
                ax.annotate('', xy=(53.0, 60), xytext=(49.0, 60),
                           arrowprops=dict(arrowstyle='->', color=self.colors['dim'],
                                          lw=2), alpha=step_alpha)

        # Flow step 3
        if progress > 0.30:
            step_alpha = min(1.0, (progress - 0.30) / 0.05)

            step_box = FancyBboxPatch(
                (52.0, 48), 18.5, 24,
                boxstyle="round,pad=0.5",
                facecolor=self.colors['bg_light'],
                edgecolor=self.colors['success'],
                linewidth=2,
                alpha=0.95 * step_alpha
            )
            ax.add_patch(step_box)

            ax.text(61.25, 66, '',
                    fontsize=30, ha='center', va='center', alpha=step_alpha)
            ax.text(61.25, 58, 'Act',
                    fontsize=18, fontweight='bold', ha='center', va='center',
                    color=self.colors['success'], alpha=step_alpha)
            ax.text(61.25, 52, 'Execute tool',
                    fontsize=14, ha='center', va='center',
                    color=self.colors['text'], alpha=step_alpha * 0.7)

            if progress > 0.33:
                ax.annotate('', xy=(75.5, 60), xytext=(71.5, 60),
                           arrowprops=dict(arrowstyle='->', color=self.colors['dim'],
                                          lw=2), alpha=step_alpha)

        # Flow step 4
        if progress > 0.35:
            step_alpha = min(1.0, (progress - 0.35) / 0.05)

            step_box = FancyBboxPatch(
                (74.5, 48), 18.5, 24,
                boxstyle="round,pad=0.5",
                facecolor=self.colors['bg_light'],
                edgecolor=self.colors['accent'],
                linewidth=2,
                alpha=0.95 * step_alpha
            )
            ax.add_patch(step_box)

            ax.text(83.75, 66, '',
                    fontsize=30, ha='center', va='center', alpha=step_alpha)
            ax.text(83.75, 58, 'Observe',
                    fontsize=18, fontweight='bold', ha='center', va='center',
                    color=self.colors['accent'], alpha=step_alpha)
            ax.text(83.75, 52, 'See result',
                    fontsize=14, ha='center', va='center',
                    color=self.colors['text'], alpha=step_alpha * 0.7)

        # Arc arrow
        if progress > 0.4:
            arc_progress = min(1.0, (progress - 0.4) / 0.19999999999999996)

            # Generate arc points using quadratic bezier
            t = np.linspace(0, arc_progress, 50)
            mid_x = (85 + 15) / 2
            mid_y = (60 + 60) / 2 + -20

            # Quadratic bezier curve
            arc_x = (1-t)**2 * 85 + 2*(1-t)*t * mid_x + t**2 * 15
            arc_y = (1-t)**2 * 60 + 2*(1-t)*t * mid_y + t**2 * 60

            ax.plot(arc_x, arc_y, color=self.colors['accent'],
                   linewidth=2, alpha=arc_progress, zorder=50)

            # Arrowhead at the end
            if arc_progress > 0.9:
                arrow_alpha = (arc_progress - 0.9) / 0.1
                # Calculate direction at endpoint
                dx = arc_x[-1] - arc_x[-2] if len(arc_x) > 1 else 1
                dy = arc_y[-1] - arc_y[-2] if len(arc_y) > 1 else 0
                ax.annotate('', xy=(15, 60),
                           xytext=(arc_x[-1] - dx*0.5, arc_y[-1] - dy*0.5),
                           arrowprops=dict(arrowstyle='->', color=self.colors['accent'],
                                          lw=2), alpha=arrow_alpha)

        if progress > 0.6:
            t = min(1.0, (progress - 0.6) / 0.20000000000000007)
            text_alpha = t * t * (3 - 2 * t)
            effective_fontsize = 14
            ax.text(50, 25, 'Loop until goal achieved or max iterations reached',
                    fontsize=effective_fontsize, fontweight='normal',
                    ha='center', va='center',
                    color=self.colors['dim'], alpha=text_alpha)

        self.add_status_indicator(progress < 1.0)

    def draw_tools(self, progress: float):
        """Step 3: tools"""
        self.fig.clear()
        ax = self.fig.add_subplot(111)
        ax.axis('off')
        ax.set_xlim(0, 100)
        ax.set_ylim(0, 100)

        # Title
        title_alpha = min(1.0, progress / 0.2)
        ax.text(50, 95, 'Tool Use',
                fontsize=45, fontweight='bold', ha='center', va='top',
                color=self.colors['primary'], alpha=title_alpha)

        if progress > 0.0:
            t = min(1.0, (progress - 0.0) / 0.2)
            text_alpha = t * t * (3 - 2 * t)
            effective_fontsize = 20
            ax.text(50, 90, 'Extending LLM Capabilities',
                    fontsize=effective_fontsize, fontweight='bold',
                    ha='center', va='center',
                    color=self.colors['primary'], alpha=text_alpha)

        # Grid item 1
        if progress > 0.20:
            item_alpha = min(1.0, (progress - 0.20) / 0.03)

            grid_box = FancyBboxPatch(
                (12.0, 56.0), 24, 16,
                boxstyle="round,pad=0.8",
                facecolor=self.colors['bg_light'],
                edgecolor=self.colors['primary'],
                linewidth=2,
                alpha=0.9 * item_alpha
            )
            ax.add_patch(grid_box)

            ax.text(24.0, 68.5, '',
                    fontsize=30, ha='center', va='center', alpha=item_alpha)
            ax.text(24.0, 64.0, 'Web Search',
                    fontsize=15, fontweight='bold', ha='center', va='center',
                    color=self.colors['primary'], alpha=item_alpha)
            ax.text(24.0, 59.5, 'Find information',
                    fontsize=11, ha='center', va='center',
                    color=self.colors['text'], alpha=item_alpha * 0.8,
                    linespacing=1.3)

        # Grid item 2
        if progress > 0.23:
            item_alpha = min(1.0, (progress - 0.23) / 0.03)

            grid_box = FancyBboxPatch(
                (38.0, 56.0), 24, 16,
                boxstyle="round,pad=0.8",
                facecolor=self.colors['bg_light'],
                edgecolor=self.colors['secondary'],
                linewidth=2,
                alpha=0.9 * item_alpha
            )
            ax.add_patch(grid_box)

            ax.text(50.0, 68.5, '',
                    fontsize=30, ha='center', va='center', alpha=item_alpha)
            ax.text(50.0, 64.0, 'Calculator',
                    fontsize=15, fontweight='bold', ha='center', va='center',
                    color=self.colors['secondary'], alpha=item_alpha)
            ax.text(50.0, 59.5, 'Math operations',
                    fontsize=11, ha='center', va='center',
                    color=self.colors['text'], alpha=item_alpha * 0.8,
                    linespacing=1.3)

        # Grid item 3
        if progress > 0.27:
            item_alpha = min(1.0, (progress - 0.27) / 0.03)

            grid_box = FancyBboxPatch(
                (64.0, 56.0), 24, 16,
                boxstyle="round,pad=0.8",
                facecolor=self.colors['bg_light'],
                edgecolor=self.colors['accent'],
                linewidth=2,
                alpha=0.9 * item_alpha
            )
            ax.add_patch(grid_box)

            ax.text(76.0, 68.5, '',
                    fontsize=30, ha='center', va='center', alpha=item_alpha)
            ax.text(76.0, 64.0, 'Code Exec',
                    fontsize=15, fontweight='bold', ha='center', va='center',
                    color=self.colors['accent'], alpha=item_alpha)
            ax.text(76.0, 59.5, 'Run Python/JS',
                    fontsize=11, ha='center', va='center',
                    color=self.colors['text'], alpha=item_alpha * 0.8,
                    linespacing=1.3)

        # Grid item 4
        if progress > 0.30:
            item_alpha = min(1.0, (progress - 0.30) / 0.03)

            grid_box = FancyBboxPatch(
                (12.0, 38.0), 24, 16,
                boxstyle="round,pad=0.8",
                facecolor=self.colors['bg_light'],
                edgecolor=self.colors['warning'],
                linewidth=2,
                alpha=0.9 * item_alpha
            )
            ax.add_patch(grid_box)

            ax.text(24.0, 50.5, '',
                    fontsize=30, ha='center', va='center', alpha=item_alpha)
            ax.text(24.0, 46.0, 'File I/O',
                    fontsize=15, fontweight='bold', ha='center', va='center',
                    color=self.colors['warning'], alpha=item_alpha)
            ax.text(24.0, 41.5, 'Read/write files',
                    fontsize=11, ha='center', va='center',
                    color=self.colors['text'], alpha=item_alpha * 0.8,
                    linespacing=1.3)

        # Grid item 5
        if progress > 0.33:
            item_alpha = min(1.0, (progress - 0.33) / 0.03)

            grid_box = FancyBboxPatch(
                (38.0, 38.0), 24, 16,
                boxstyle="round,pad=0.8",
                facecolor=self.colors['bg_light'],
                edgecolor=self.colors['highlight'],
                linewidth=2,
                alpha=0.9 * item_alpha
            )
            ax.add_patch(grid_box)

            ax.text(50.0, 50.5, '',
                    fontsize=30, ha='center', va='center', alpha=item_alpha)
            ax.text(50.0, 46.0, 'API Calls',
                    fontsize=15, fontweight='bold', ha='center', va='center',
                    color=self.colors['highlight'], alpha=item_alpha)
            ax.text(50.0, 41.5, 'External services',
                    fontsize=11, ha='center', va='center',
                    color=self.colors['text'], alpha=item_alpha * 0.8,
                    linespacing=1.3)

        # Grid item 6
        if progress > 0.37:
            item_alpha = min(1.0, (progress - 0.37) / 0.03)

            grid_box = FancyBboxPatch(
                (64.0, 38.0), 24, 16,
                boxstyle="round,pad=0.8",
                facecolor=self.colors['bg_light'],
                edgecolor=self.colors['success'],
                linewidth=2,
                alpha=0.9 * item_alpha
            )
            ax.add_patch(grid_box)

            ax.text(76.0, 50.5, '',
                    fontsize=30, ha='center', va='center', alpha=item_alpha)
            ax.text(76.0, 46.0, 'Browser',
                    fontsize=15, fontweight='bold', ha='center', va='center',
                    color=self.colors['success'], alpha=item_alpha)
            ax.text(76.0, 41.5, 'Navigate web',
                    fontsize=11, ha='center', va='center',
                    color=self.colors['text'], alpha=item_alpha * 0.8,
                    linespacing=1.3)

        if progress > 0.6:
            t = min(1.0, (progress - 0.6) / 0.20000000000000007)
            text_alpha = t * t * (3 - 2 * t)
            effective_fontsize = 16
            ax.text(50, 15, 'Tools turn language into action',
                    fontsize=effective_fontsize, fontweight='normal',
                    ha='center', va='center',
                    color=self.colors['text'], alpha=text_alpha)

        self.add_status_indicator(progress < 1.0)

    def draw_function_calling(self, progress: float):
        """Step 4: function_calling"""
        self.fig.clear()
        ax = self.fig.add_subplot(111)
        ax.axis('off')
        ax.set_xlim(0, 100)
        ax.set_ylim(0, 100)

        # Title
        title_alpha = min(1.0, progress / 0.2)
        ax.text(50, 95, 'Function Calling',
                fontsize=45, fontweight='bold', ha='center', va='top',
                color=self.colors['primary'], alpha=title_alpha)

        if progress > 0.0:
            t = min(1.0, (progress - 0.0) / 0.2)
            text_alpha = t * t * (3 - 2 * t)
            effective_fontsize = 20
            ax.text(50, 90, 'How the LLM Chooses Tools',
                    fontsize=effective_fontsize, fontweight='bold',
                    ha='center', va='center',
                    color=self.colors['primary'], alpha=text_alpha)

        # Code execution
        if progress > 0.2:
            code_progress = min(1.0, (progress - 0.2) / 0.2)

            # Code block
            code_box = FancyBboxPatch(
                (12.5, 63.0),
                75, 18,
                boxstyle="round,pad=0.5",
                facecolor='#1a1a2e',
                edgecolor=self.colors['dim'],
                linewidth=2,
                alpha=0.95 * code_progress
            )
            ax.add_patch(code_box)

            ax.text(50, 72.0,
                   'User: What\'s the weather in Amsterdam?\n\nLLM chooses: get_weather(city=\'Amsterdam\')',
                   fontsize=12, family='monospace', ha='center', va='center',
                   color='#a8ff60', alpha=code_progress)

        # Output (staggered)
        output_start = 0.30000000000000004
        if progress > output_start:
            out_progress = min(1.0, (progress - output_start) / (0.4 - output_start))

            # Arrow
            ax.annotate('', xy=(50, 49.0),
                       xytext=(50, 61.0),
                       arrowprops=dict(arrowstyle='->', color=self.colors['accent'],
                                      lw=2), alpha=out_progress)

            # Output box
            out_box = FancyBboxPatch(
                (12.5, 37.0),
                75, 12,
                boxstyle="round,pad=0.5",
                facecolor='#1a2e1a',
                edgecolor=self.colors['success'],
                linewidth=2,
                alpha=0.95 * out_progress
            )
            ax.add_patch(out_box)

            ax.text(50, 43.0,
                   '{\n  "temp": 15,\n  "condition": "cloudy"\n}',
                   fontsize=12, family='monospace', ha='center', va='center',
                   color='#60ffa8', alpha=out_progress)

        if progress > 0.6:
            t = min(1.0, (progress - 0.6) / 0.20000000000000007)
            text_alpha = t * t * (3 - 2 * t)
            effective_fontsize = 14
            ax.text(50, 15, 'The model outputs structured JSON that maps to function calls',
                    fontsize=effective_fontsize, fontweight='normal',
                    ha='center', va='center',
                    color=self.colors['dim'], alpha=text_alpha)

        self.add_status_indicator(progress < 1.0)

    def draw_react(self, progress: float):
        """Step 5: react"""
        self.fig.clear()
        ax = self.fig.add_subplot(111)
        ax.axis('off')
        ax.set_xlim(0, 100)
        ax.set_ylim(0, 100)

        # Title
        title_alpha = min(1.0, progress / 0.2)
        ax.text(50, 95, 'ReAct Pattern',
                fontsize=45, fontweight='bold', ha='center', va='top',
                color=self.colors['primary'], alpha=title_alpha)

        if progress > 0.0:
            t = min(1.0, (progress - 0.0) / 0.2)
            text_alpha = t * t * (3 - 2 * t)
            effective_fontsize = 22
            ax.text(50, 90, 'Reasoning + Acting',
                    fontsize=effective_fontsize, fontweight='bold',
                    ha='center', va='center',
                    color=self.colors['primary'], alpha=text_alpha)

        # Message 1: user
        if progress > 0.20:
            msg_alpha = min(1.0, (progress - 0.20) / 0.05)

            bubble = FancyBboxPatch(
                (10.0, 69.0),
                38.0, 8,
                boxstyle="round,pad=0.5",
                facecolor=self.colors['bg_light'],
                edgecolor=self.colors['primary'],
                linewidth=2,
                alpha=0.95 * msg_alpha
            )
            ax.add_patch(bubble)

            ax.text(12.0, 75.0, 'Task:',
                   fontsize=10, fontweight='bold', ha='left', va='center',
                   color=self.colors['primary'], alpha=msg_alpha)

            ax.text(12.0, 71.66666666666667, 'Book a flight to Paris for next Tuesday',
                   fontsize=11, ha='left', va='center',
                   color=self.colors['text'], alpha=msg_alpha)

        # Message 2: assistant
        if progress > 0.25:
            msg_alpha = min(1.0, (progress - 0.25) / 0.05)

            bubble = FancyBboxPatch(
                (50, 57.0),
                38.0, 8,
                boxstyle="round,pad=0.5",
                facecolor=self.colors['bg_light'],
                edgecolor=self.colors['secondary'],
                linewidth=2,
                alpha=0.95 * msg_alpha
            )
            ax.add_patch(bubble)

            ax.text(52, 63.0, 'Thought:',
                   fontsize=10, fontweight='bold', ha='left', va='center',
                   color=self.colors['secondary'], alpha=msg_alpha)

            ax.text(52, 59.666666666666664, 'I need to search for flights first',
                   fontsize=11, ha='left', va='center',
                   color=self.colors['text'], alpha=msg_alpha)

        # Message 3: system
        if progress > 0.30:
            msg_alpha = min(1.0, (progress - 0.30) / 0.05)

            bubble = FancyBboxPatch(
                (50, 45.0),
                38.0, 8,
                boxstyle="round,pad=0.5",
                facecolor=self.colors['bg_light'],
                edgecolor=self.colors['secondary'],
                linewidth=2,
                alpha=0.95 * msg_alpha
            )
            ax.add_patch(bubble)

            ax.text(52, 51.0, 'Action:',
                   fontsize=10, fontweight='bold', ha='left', va='center',
                   color=self.colors['secondary'], alpha=msg_alpha)

            ax.text(52, 47.666666666666664, 'search_flights(dest=\'Paris\', date=\'Tuesday\')',
                   fontsize=11, ha='left', va='center',
                   color=self.colors['text'], alpha=msg_alpha)

        # Message 4: assistant
        if progress > 0.35:
            msg_alpha = min(1.0, (progress - 0.35) / 0.05)

            bubble = FancyBboxPatch(
                (50, 33.0),
                38.0, 8,
                boxstyle="round,pad=0.5",
                facecolor=self.colors['bg_light'],
                edgecolor=self.colors['secondary'],
                linewidth=2,
                alpha=0.95 * msg_alpha
            )
            ax.add_patch(bubble)

            ax.text(52, 39.0, 'Observation:',
                   fontsize=10, fontweight='bold', ha='left', va='center',
                   color=self.colors['secondary'], alpha=msg_alpha)

            ax.text(52, 35.666666666666664, 'Found 3 options: AF123, KL456, BA789',
                   fontsize=11, ha='left', va='center',
                   color=self.colors['text'], alpha=msg_alpha)

        if progress > 0.8:
            t = min(1.0, (progress - 0.8) / 0.19999999999999996)
            text_alpha = t * t * (3 - 2 * t)
            effective_fontsize = 14
            ax.text(50, 12, 'Explicit reasoning traces improve accuracy and debuggability',
                    fontsize=effective_fontsize, fontweight='normal',
                    ha='center', va='center',
                    color=self.colors['secondary'], alpha=text_alpha)

        self.add_status_indicator(progress < 1.0)

    def draw_planning(self, progress: float):
        """Step 6: planning"""
        self.fig.clear()
        ax = self.fig.add_subplot(111)
        ax.axis('off')
        ax.set_xlim(0, 100)
        ax.set_ylim(0, 100)

        # Title
        title_alpha = min(1.0, progress / 0.2)
        ax.text(50, 95, 'Planning & Decomposition',
                fontsize=45, fontweight='bold', ha='center', va='top',
                color=self.colors['primary'], alpha=title_alpha)

        if progress > 0.0:
            t = min(1.0, (progress - 0.0) / 0.2)
            text_alpha = t * t * (3 - 2 * t)
            effective_fontsize = 20
            ax.text(50, 90, 'Breaking Complex Tasks Into Steps',
                    fontsize=effective_fontsize, fontweight='bold',
                    ha='center', va='center',
                    color=self.colors['primary'], alpha=text_alpha)

        # Stacked box 1
        if progress > 0.20:
            stack_alpha = min(1.0, (progress - 0.20) / 0.04)

            stack_box = FancyBboxPatch(
                (15.0, 81.5), 70, 12,
                boxstyle="round,pad=0.8",
                facecolor=self.colors['bg_light'],
                edgecolor=self.colors['primary'],
                linewidth=3,
                alpha=0.95 * stack_alpha
            )
            ax.add_patch(stack_box)

            ax.text(50, 89.5, 'Goal',
                    fontsize=21, fontweight='bold', ha='center', va='center',
                    color=self.colors['primary'], alpha=stack_alpha)
            ax.text(50, 85.5, 'Create a market analysis report',
                    fontsize=14, ha='center', va='center',
                    color=self.colors['text'], alpha=stack_alpha * 0.8)

        # Stacked box 2
        if progress > 0.24:
            stack_alpha = min(1.0, (progress - 0.24) / 0.04)

            stack_box = FancyBboxPatch(
                (17.0, 66.5), 66, 12,
                boxstyle="round,pad=0.8",
                facecolor=self.colors['bg_light'],
                edgecolor=self.colors['secondary'],
                linewidth=3,
                alpha=0.95 * stack_alpha
            )
            ax.add_patch(stack_box)

            ax.text(50, 74.5, 'Step 1',
                    fontsize=21, fontweight='bold', ha='center', va='center',
                    color=self.colors['secondary'], alpha=stack_alpha)
            ax.text(50, 70.5, 'Research competitor data',
                    fontsize=14, ha='center', va='center',
                    color=self.colors['text'], alpha=stack_alpha * 0.8)

        # Stacked box 3
        if progress > 0.28:
            stack_alpha = min(1.0, (progress - 0.28) / 0.04)

            stack_box = FancyBboxPatch(
                (19.0, 51.5), 62, 12,
                boxstyle="round,pad=0.8",
                facecolor=self.colors['bg_light'],
                edgecolor=self.colors['secondary'],
                linewidth=3,
                alpha=0.95 * stack_alpha
            )
            ax.add_patch(stack_box)

            ax.text(50, 59.5, 'Step 2',
                    fontsize=21, fontweight='bold', ha='center', va='center',
                    color=self.colors['secondary'], alpha=stack_alpha)
            ax.text(50, 55.5, 'Analyze market trends',
                    fontsize=14, ha='center', va='center',
                    color=self.colors['text'], alpha=stack_alpha * 0.8)

        # Stacked box 4
        if progress > 0.32:
            stack_alpha = min(1.0, (progress - 0.32) / 0.04)

            stack_box = FancyBboxPatch(
                (21.0, 36.5), 58, 12,
                boxstyle="round,pad=0.8",
                facecolor=self.colors['bg_light'],
                edgecolor=self.colors['secondary'],
                linewidth=3,
                alpha=0.95 * stack_alpha
            )
            ax.add_patch(stack_box)

            ax.text(50, 44.5, 'Step 3',
                    fontsize=21, fontweight='bold', ha='center', va='center',
                    color=self.colors['secondary'], alpha=stack_alpha)
            ax.text(50, 40.5, 'Generate visualizations',
                    fontsize=14, ha='center', va='center',
                    color=self.colors['text'], alpha=stack_alpha * 0.8)

        # Stacked box 5
        if progress > 0.36:
            stack_alpha = min(1.0, (progress - 0.36) / 0.04)

            stack_box = FancyBboxPatch(
                (23.0, 21.5), 54, 12,
                boxstyle="round,pad=0.8",
                facecolor=self.colors['bg_light'],
                edgecolor=self.colors['accent'],
                linewidth=3,
                alpha=0.95 * stack_alpha
            )
            ax.add_patch(stack_box)

            ax.text(50, 29.5, 'Step 4',
                    fontsize=21, fontweight='bold', ha='center', va='center',
                    color=self.colors['accent'], alpha=stack_alpha)
            ax.text(50, 25.5, 'Write executive summary',
                    fontsize=14, ha='center', va='center',
                    color=self.colors['text'], alpha=stack_alpha * 0.8)

        self.add_status_indicator(progress < 1.0)

    def draw_memory(self, progress: float):
        """Step 7: memory"""
        self.fig.clear()
        ax = self.fig.add_subplot(111)
        ax.axis('off')
        ax.set_xlim(0, 100)
        ax.set_ylim(0, 100)

        # Title
        title_alpha = min(1.0, progress / 0.2)
        ax.text(50, 95, 'Agent Memory',
                fontsize=45, fontweight='bold', ha='center', va='top',
                color=self.colors['primary'], alpha=title_alpha)

        if progress > 0.0:
            t = min(1.0, (progress - 0.0) / 0.2)
            text_alpha = t * t * (3 - 2 * t)
            effective_fontsize = 20
            ax.text(50, 90, 'Remembering Across Interactions',
                    fontsize=effective_fontsize, fontweight='bold',
                    ha='center', va='center',
                    color=self.colors['primary'], alpha=text_alpha)

        # Grid item 1
        if progress > 0.20:
            item_alpha = min(1.0, (progress - 0.20) / 0.07)

            grid_box = FancyBboxPatch(
                (12.0, 41.0), 24, 28,
                boxstyle="round,pad=0.8",
                facecolor=self.colors['bg_light'],
                edgecolor=self.colors['warning'],
                linewidth=2,
                alpha=0.9 * item_alpha
            )
            ax.add_patch(grid_box)

            ax.text(24.0, 62.5, '',
                    fontsize=30, ha='center', va='center', alpha=item_alpha)
            ax.text(24.0, 55.0, 'Short-term',
                    fontsize=15, fontweight='bold', ha='center', va='center',
                    color=self.colors['warning'], alpha=item_alpha)
            ax.text(24.0, 47.5, 'Current context window',
                    fontsize=11, ha='center', va='center',
                    color=self.colors['text'], alpha=item_alpha * 0.8,
                    linespacing=1.3)

        # Grid item 2
        if progress > 0.27:
            item_alpha = min(1.0, (progress - 0.27) / 0.07)

            grid_box = FancyBboxPatch(
                (38.0, 41.0), 24, 28,
                boxstyle="round,pad=0.8",
                facecolor=self.colors['bg_light'],
                edgecolor=self.colors['accent'],
                linewidth=2,
                alpha=0.9 * item_alpha
            )
            ax.add_patch(grid_box)

            ax.text(50.0, 62.5, '',
                    fontsize=30, ha='center', va='center', alpha=item_alpha)
            ax.text(50.0, 55.0, 'Working',
                    fontsize=15, fontweight='bold', ha='center', va='center',
                    color=self.colors['accent'], alpha=item_alpha)
            ax.text(50.0, 47.5, 'Scratchpad for task',
                    fontsize=11, ha='center', va='center',
                    color=self.colors['text'], alpha=item_alpha * 0.8,
                    linespacing=1.3)

        # Grid item 3
        if progress > 0.33:
            item_alpha = min(1.0, (progress - 0.33) / 0.07)

            grid_box = FancyBboxPatch(
                (64.0, 41.0), 24, 28,
                boxstyle="round,pad=0.8",
                facecolor=self.colors['bg_light'],
                edgecolor=self.colors['success'],
                linewidth=2,
                alpha=0.9 * item_alpha
            )
            ax.add_patch(grid_box)

            ax.text(76.0, 62.5, '',
                    fontsize=30, ha='center', va='center', alpha=item_alpha)
            ax.text(76.0, 55.0, 'Long-term',
                    fontsize=15, fontweight='bold', ha='center', va='center',
                    color=self.colors['success'], alpha=item_alpha)
            ax.text(76.0, 47.5, 'Vector DB / external storage',
                    fontsize=11, ha='center', va='center',
                    color=self.colors['text'], alpha=item_alpha * 0.8,
                    linespacing=1.3)

        if progress > 0.40:
            item_alpha = min(1.0, (progress - 0.40) / 0.07)
            ax.text(20, 18, '• Persist important information across sessions',
                    fontsize=21, ha='left', va='center',
                    color=self.colors['text'], alpha=item_alpha)

        if progress > 0.47:
            item_alpha = min(1.0, (progress - 0.47) / 0.07)
            ax.text(20, 12, '• Retrieve relevant memories when needed',
                    fontsize=21, ha='left', va='center',
                    color=self.colors['text'], alpha=item_alpha)

        if progress > 0.53:
            item_alpha = min(1.0, (progress - 0.53) / 0.07)
            ax.text(20, 6, '• Learn from past successes and failures',
                    fontsize=21, ha='left', va='center',
                    color=self.colors['text'], alpha=item_alpha)

        self.add_status_indicator(progress < 1.0)

    def draw_safety(self, progress: float):
        """Step 8: safety"""
        self.fig.clear()
        ax = self.fig.add_subplot(111)
        ax.axis('off')
        ax.set_xlim(0, 100)
        ax.set_ylim(0, 100)

        # Title
        title_alpha = min(1.0, progress / 0.2)
        ax.text(50, 95, 'Safety & Control',
                fontsize=45, fontweight='bold', ha='center', va='top',
                color=self.colors['primary'], alpha=title_alpha)

        if progress > 0.0:
            t = min(1.0, (progress - 0.0) / 0.2)
            text_alpha = t * t * (3 - 2 * t)
            effective_fontsize = 22
            ax.text(50, 90, 'Keeping Agents Safe',
                    fontsize=effective_fontsize, fontweight='bold',
                    ha='center', va='center',
                    color=self.colors['warning'], alpha=text_alpha)

        # Checklist item 1
        if progress > 0.20:
            check_alpha = min(1.0, (progress - 0.20) / 0.04)

            ax.text(20, 71.25, '\u2713',
                    fontsize=27, ha='center', va='center',
                    color=self.colors['secondary'], fontweight='bold',
                    alpha=check_alpha)

            ax.text(25, 71.25, '\u2611 Sandbox execution environments',
                    fontsize=18, ha='left', va='center',
                    color=self.colors['text'], alpha=check_alpha)

        # Checklist item 2
        if progress > 0.24:
            check_alpha = min(1.0, (progress - 0.24) / 0.04)

            ax.text(20, 64.75, '\u2713',
                    fontsize=27, ha='center', va='center',
                    color=self.colors['secondary'], fontweight='bold',
                    alpha=check_alpha)

            ax.text(25, 64.75, '\u2611 Require human approval for high-risk actions',
                    fontsize=18, ha='left', va='center',
                    color=self.colors['text'], alpha=check_alpha)

        # Checklist item 3
        if progress > 0.28:
            check_alpha = min(1.0, (progress - 0.28) / 0.04)

            ax.text(20, 58.25, '\u2713',
                    fontsize=27, ha='center', va='center',
                    color=self.colors['secondary'], fontweight='bold',
                    alpha=check_alpha)

            ax.text(25, 58.25, '\u2611 Set clear boundaries on what agent can access',
                    fontsize=18, ha='left', va='center',
                    color=self.colors['text'], alpha=check_alpha)

        # Checklist item 4
        if progress > 0.32:
            check_alpha = min(1.0, (progress - 0.32) / 0.04)

            ax.text(20, 51.75, '\u2713',
                    fontsize=27, ha='center', va='center',
                    color=self.colors['secondary'], fontweight='bold',
                    alpha=check_alpha)

            ax.text(25, 51.75, '\u2611 Log all actions for audit trails',
                    fontsize=18, ha='left', va='center',
                    color=self.colors['text'], alpha=check_alpha)

        # Checklist item 5
        if progress > 0.36:
            check_alpha = min(1.0, (progress - 0.36) / 0.04)

            ax.text(20, 45.25, '\u2713',
                    fontsize=27, ha='center', va='center',
                    color=self.colors['secondary'], fontweight='bold',
                    alpha=check_alpha)

            ax.text(25, 45.25, '\u2611 Implement rate limits and cost controls',
                    fontsize=18, ha='left', va='center',
                    color=self.colors['text'], alpha=check_alpha)

        if progress > 0.6:
            t = min(1.0, (progress - 0.6) / 0.20000000000000007)
            text_alpha = t * t * (3 - 2 * t)
            effective_fontsize = 16
            ax.text(50, 15, 'Agents are powerful - use appropriate guardrails!',
                    fontsize=effective_fontsize, fontweight='normal',
                    ha='center', va='center',
                    color=self.colors['warning'], alpha=text_alpha)

        self.add_status_indicator(progress < 1.0)

    def draw_examples(self, progress: float):
        """Step 9: examples"""
        self.fig.clear()
        ax = self.fig.add_subplot(111)
        ax.axis('off')
        ax.set_xlim(0, 100)
        ax.set_ylim(0, 100)

        # Title
        title_alpha = min(1.0, progress / 0.2)
        ax.text(50, 95, 'Real-World Agents',
                fontsize=45, fontweight='bold', ha='center', va='top',
                color=self.colors['primary'], alpha=title_alpha)

        if progress > 0.0:
            t = min(1.0, (progress - 0.0) / 0.2)
            text_alpha = t * t * (3 - 2 * t)
            effective_fontsize = 22
            ax.text(50, 90, 'Agents in Production',
                    fontsize=effective_fontsize, fontweight='bold',
                    ha='center', va='center',
                    color=self.colors['primary'], alpha=text_alpha)

        # Timeline
        if progress > 0.2:
            tl_progress = min(1.0, (progress - 0.2) / 0.2)

            # Main line
            ax.plot([7.5, 92.5],
                   [55, 55],
                   color=self.colors['dim'], linewidth=3,
                   alpha=tl_progress * 0.8)

        # Event 1
        if progress > 0.20:
            ev_alpha = min(1.0, (progress - 0.20) / 0.05)

            # Marker
            marker = Circle((7.5, 55), 1.5,
                          facecolor=self.colors['dim'],
                          edgecolor='white', linewidth=2,
                          alpha=ev_alpha, zorder=10)
            ax.add_patch(marker)

            # Date
            ax.text(7.5, 51, '2023',
                   fontsize=12, fontweight='bold', ha='center', va='top',
                   color=self.colors['dim'], alpha=ev_alpha)

            # Title
            ax.text(7.5, 59, 'Auto-GPT',
                   fontsize=14, fontweight='bold', ha='center', va='bottom',
                   color=self.colors['text'], alpha=ev_alpha)

            # Description
            ax.text(7.5, 63, 'First viral agent',
                   fontsize=10, ha='center', va='bottom',
                   color=self.colors['dim'], alpha=ev_alpha * 0.8)

        # Event 2
        if progress > 0.25:
            ev_alpha = min(1.0, (progress - 0.25) / 0.05)

            # Marker
            marker = Circle((35.83333333333333, 55), 1.5,
                          facecolor=self.colors['primary'],
                          edgecolor='white', linewidth=2,
                          alpha=ev_alpha, zorder=10)
            ax.add_patch(marker)

            # Date
            ax.text(35.83333333333333, 51, '2024',
                   fontsize=12, fontweight='bold', ha='center', va='top',
                   color=self.colors['primary'], alpha=ev_alpha)

            # Title
            ax.text(35.83333333333333, 59, 'Devin',
                   fontsize=14, fontweight='bold', ha='center', va='bottom',
                   color=self.colors['text'], alpha=ev_alpha)

            # Description
            ax.text(35.83333333333333, 63, 'AI software engineer',
                   fontsize=10, ha='center', va='bottom',
                   color=self.colors['dim'], alpha=ev_alpha * 0.8)

        # Event 3
        if progress > 0.30:
            ev_alpha = min(1.0, (progress - 0.30) / 0.05)

            # Marker
            marker = Circle((64.16666666666666, 55), 1.5,
                          facecolor=self.colors['secondary'],
                          edgecolor='white', linewidth=2,
                          alpha=ev_alpha, zorder=10)
            ax.add_patch(marker)

            # Date
            ax.text(64.16666666666666, 51, '2024',
                   fontsize=12, fontweight='bold', ha='center', va='top',
                   color=self.colors['secondary'], alpha=ev_alpha)

            # Title
            ax.text(64.16666666666666, 59, 'Claude Code',
                   fontsize=14, fontweight='bold', ha='center', va='bottom',
                   color=self.colors['text'], alpha=ev_alpha)

            # Description
            ax.text(64.16666666666666, 63, 'Coding assistant',
                   fontsize=10, ha='center', va='bottom',
                   color=self.colors['dim'], alpha=ev_alpha * 0.8)

        # Event 4
        if progress > 0.35:
            ev_alpha = min(1.0, (progress - 0.35) / 0.05)

            # Marker
            marker = Circle((92.5, 55), 1.5,
                          facecolor=self.colors['accent'],
                          edgecolor='white', linewidth=2,
                          alpha=ev_alpha, zorder=10)
            ax.add_patch(marker)

            # Date
            ax.text(92.5, 51, '2025',
                   fontsize=12, fontweight='bold', ha='center', va='top',
                   color=self.colors['accent'], alpha=ev_alpha)

            # Title
            ax.text(92.5, 59, 'Operator',
                   fontsize=14, fontweight='bold', ha='center', va='bottom',
                   color=self.colors['text'], alpha=ev_alpha)

            # Description
            ax.text(92.5, 63, 'Computer use',
                   fontsize=10, ha='center', va='bottom',
                   color=self.colors['dim'], alpha=ev_alpha * 0.8)

        if progress > 0.8:
            t = min(1.0, (progress - 0.8) / 0.19999999999999996)
            text_alpha = t * t * (3 - 2 * t)
            effective_fontsize = 18
            ax.text(50, 18, 'The agentic era is just beginning!',
                    fontsize=effective_fontsize, fontweight='normal',
                    ha='center', va='center',
                    color=self.colors['success'], alpha=text_alpha)

        self.add_status_indicator(progress < 1.0)


def run():
    """Run the presentation"""
    pres = AiAgentsPresentation()
    pres.show()


if __name__ == "__main__":
    run()
