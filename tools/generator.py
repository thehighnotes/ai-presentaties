"""
Presentation Code Generator
Generates Python presentation code from JSON schema
"""

import textwrap
from pathlib import Path
from typing import Dict, Any, List, Optional
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))

from tools.schema import (
    PresentationSchema, Step, LandingPage,
    EasingFunction, ContinuousEffect, AnimationTiming
)


class PresentationGenerator:
    """Generates Python presentation code from schema"""

    def __init__(self, schema: PresentationSchema):
        self.schema = schema
        self.class_name = self._to_class_name(schema.name)

    def _to_class_name(self, name: str) -> str:
        """Convert name to PascalCase class name"""
        words = name.replace('_', ' ').replace('-', ' ').split()
        return ''.join(w.capitalize() for w in words) + 'Presentation'

    def _to_method_name(self, name: str) -> str:
        """Convert step name to snake_case method name"""
        clean = name.lower()
        clean = clean.replace('?', '').replace('!', '').replace('.', '')
        clean = clean.replace('-', ' ').replace(':', ' ')
        words = clean.split()
        return 'draw_' + '_'.join(words)

    def _escape_string(self, s: str) -> str:
        """Escape string for Python code"""
        return s.replace('\\', '\\\\').replace("'", "\\'").replace('\n', '\\n')

    def _format_multiline(self, s: str, indent: int = 8) -> str:
        """Format multiline string for Python"""
        if '\n' not in s and len(s) < 60:
            return f"'{self._escape_string(s)}'"

        lines = s.split('\n')
        ind = ' ' * indent
        formatted = '"""' + lines[0]
        for line in lines[1:]:
            formatted += f'\n{ind}{line}'
        formatted += '"""'
        return formatted

    def generate_imports(self) -> str:
        """Generate import statements"""
        # Check if we need 3D imports
        needs_3d = self._needs_3d_imports()
        needs_visual_effects = self._needs_visual_effects()

        base_imports = '''"""
{title}
{description}
"""

import sys
import os
import numpy as np
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle, Wedge
import matplotlib.pyplot as plt
'''.format(
            title=self.schema.title,
            description=self.schema.description or "Auto-generated presentation"
        )

        if needs_3d:
            base_imports += '''from mpl_toolkits.mplot3d import proj3d, Axes3D
'''

        base_imports += '''
# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core import BasePresentation, PresentationStyle
from core.animations import AnimationHelper
'''

        if needs_visual_effects:
            base_imports += '''from core.visual_effects import (
    ParticleSystem, SimilarityMeter, ProgressIndicator,
    WeightDeltaVisualizer, AnimationHelpers
)
'''

        if needs_3d:
            base_imports += self._generate_arrow3d_class()

        return base_imports

    def _needs_3d_imports(self) -> bool:
        """Check if any step uses 3D elements"""
        for step in self.schema.steps:
            for elem in step.elements:
                if elem.get('type') in ('scatter_3d', 'vector_3d'):
                    return True
        return False

    def _needs_visual_effects(self) -> bool:
        """Check if any step uses visual effect elements"""
        for step in self.schema.steps:
            for elem in step.elements:
                if elem.get('type') in ('particle_flow', 'similarity_meter',
                                        'progress_bar', 'weight_comparison'):
                    return True
        return False

    def _generate_arrow3d_class(self) -> str:
        """Generate the Arrow3D helper class for 3D visualizations"""
        return '''

class Arrow3D(FancyArrowPatch):
    """Custom 3D arrow for visualization"""
    def __init__(self, xs, ys, zs, *args, **kwargs):
        super().__init__((0, 0), (0, 0), *args, **kwargs)
        self._verts3d = xs, ys, zs

    def do_3d_projection(self, renderer=None):
        xs3d, ys3d, zs3d = self._verts3d
        xs, ys, zs = proj3d.proj_transform(xs3d, ys3d, zs3d, self.axes.M)
        self.set_positions((xs[0], ys[0]), (xs[1], ys[1]))
        return np.min(zs)
'''

    def generate_class_header(self) -> str:
        """Generate class definition and __init__"""
        step_names_str = ',\n            '.join(
            f"'{s.name}'" for s in [Step(name='Landing')] + self.schema.steps
        )

        return f'''

class {self.class_name}(BasePresentation):
    """{self.schema.title}"""

    def __init__(self):
        """Initialize the presentation"""
        step_names = [
            {step_names_str}
        ]

        super().__init__("{self.schema.title}", step_names)

        self.show_landing_page()
'''

    def generate_get_frames_for_step(self) -> str:
        """Generate get_frames_for_step method"""
        # Check if any steps have non-default frame counts
        custom_frames = [(i, s.animation_frames) for i, s in enumerate(self.schema.steps)
                         if s.animation_frames != 60]

        if not custom_frames:
            return '''
    def get_frames_for_step(self, step: int) -> int:
        """Get animation frame count for each step"""
        return 60
'''

        cases = '\n        '.join(
            f'elif step == {i + 1}: return {frames}'  # +1 because landing is step 0
            for i, frames in custom_frames
        )

        return f'''
    def get_frames_for_step(self, step: int) -> int:
        """Get animation frame count for each step"""
        if False: pass
        {cases}
        return 60
'''

    def generate_landing_page(self) -> str:
        """Generate show_landing_page method"""
        land = self.schema.landing

        # Build the landing page code
        code = f'''
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
            edgecolor=self.colors['{land.primary_color}'],
            linewidth=4,
            alpha=0.95
        )
        ax.add_patch(title_box)

        ax.text(50, 72, '{self._escape_string(land.title)}',
                fontsize=66, fontweight='bold', ha='center', va='center',
                color=self.colors['{land.primary_color}'])
'''

        if land.subtitle:
            code += f'''
        ax.text(50, 64, '{self._escape_string(land.subtitle)}',
                fontsize=30, ha='center', va='center',
                color=self.colors['text'], alpha=0.8, style='italic')
'''

        if land.icon_left:
            code += f'''
        ax.text(30, 67, '{land.icon_left}', fontsize=75, ha='center', va='center')
'''

        if land.icon_right:
            code += f'''
        ax.text(70, 67, '{land.icon_right}', fontsize=75, ha='center', va='center')
'''

        if land.tagline:
            code += f'''
        ax.text(50, 45, '{self._escape_string(land.tagline)}',
                fontsize=27, ha='center', va='center',
                color=self.colors['accent'], alpha=0.9)
'''

        # Instructions box
        code += '''
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
'''

        if land.footer:
            code += f'''
        ax.text(50, 5, '{self._escape_string(land.footer)}',
                fontsize=21, ha='center', va='center',
                color=self.colors['text'], alpha=0.5)
'''

        code += '''
        plt.tight_layout()
'''
        return code

    def generate_animate_step(self) -> str:
        """Generate animate_step method"""
        # Build dispatch cases
        cases = []
        for i, step in enumerate(self.schema.steps):
            method_name = self._to_method_name(step.name)
            cases.append(f'        elif self.current_step == {i + 1}:\n            self.{method_name}(progress)')

        cases_str = '\n'.join(cases)

        return f'''
    def animate_step(self, frame: int):
        """Animate current step"""
        total_frames = self.get_frames_for_step(self.current_step)
        progress = frame / (total_frames - 1) if total_frames > 1 else 1

        if self.current_step == 0:
            pass  # Landing is static
{cases_str}

        if frame >= total_frames - 1:
            self.is_animating = False
'''

    def generate_draw_current_step_static(self) -> str:
        """Generate draw_current_step_static method"""
        cases = []
        for i, step in enumerate(self.schema.steps):
            method_name = self._to_method_name(step.name)
            cases.append(f'        elif self.current_step == {i + 1}:\n            self.{method_name}(1.0)')

        cases_str = '\n'.join(cases)

        return f'''
    def draw_current_step_static(self):
        """Draw current step without animation"""
        if self.current_step == -1:
            self.show_landing_page()
{cases_str}
        plt.draw()
'''

    def generate_step_method(self, step: Step, step_index: int) -> str:
        """Generate a draw method for a single step"""
        method_name = self._to_method_name(step.name)
        title = step.title or step.name

        code = f'''
    def {method_name}(self, progress: float):
        """Step {step_index + 1}: {step.name}"""
        self.fig.clear()
        ax = self.fig.add_subplot(111)
        ax.axis('off')
        ax.set_xlim(0, 100)
        ax.set_ylim(0, 100)

        # Title
        title_alpha = min(1.0, progress / 0.2)
        ax.text(50, 95, '{self._escape_string(title)}',
                fontsize=45, fontweight='bold', ha='center', va='top',
                color=self.colors['primary'], alpha=title_alpha)
'''

        # Add subtitle if present
        if step.subtitle:
            code += f'''
        if progress > 0.1:
            sub_alpha = min(1.0, (progress - 0.1) / 0.2)
            ax.text(50, 88, '{self._escape_string(step.subtitle)}',
                    fontsize=24, ha='center', va='top',
                    color=self.colors['text'], alpha=sub_alpha * 0.8, style='italic')
'''

        # Process elements
        for elem in step.elements:
            code += self._generate_element_code(elem)

        # Add status indicator
        code += '''
        self.add_status_indicator(progress < 1.0)
'''

        return code

    def _generate_element_code(self, elem: Dict[str, Any]) -> str:
        """Generate code for a single element"""
        elem_type = elem.get('type', 'text')

        # Map animation phase to progress thresholds
        phase_map = {
            'immediate': (0.0, 0.2),
            'early': (0.2, 0.4),
            'middle': (0.4, 0.6),
            'late': (0.6, 0.8),
            'final': (0.8, 1.0)
        }
        phase = elem.get('animation_phase', 'early')
        start, end = phase_map.get(phase, (0.2, 0.4))

        # Apply duration and delay if specified
        duration = elem.get('duration', 1.0)
        delay = elem.get('delay', 0.0)

        # Delay shifts the start point
        start = start + delay * 0.1  # delay of 1.0s = shift by 10%

        # Duration affects how long the element animates
        # Default phase is 20% of total animation (0.2 range)
        # Duration multiplier adjusts this
        phase_duration = (end - start) * duration
        end = min(1.0, start + phase_duration)

        # Check for custom timing override (takes priority)
        custom_timing = elem.get('custom_timing')
        if custom_timing:
            start = custom_timing.get('start_percent', start * 100) / 100
            end = custom_timing.get('end_percent', end * 100) / 100

        # Get easing function
        easing = elem.get('easing', 'ease_in_out')

        if elem_type == 'text':
            return self._generate_text_element(elem, start, end, easing)
        elif elem_type == 'typewriter_text':
            return self._generate_typewriter_text(elem, start, end)
        elif elem_type == 'box':
            return self._generate_box_element(elem, start, end)
        elif elem_type == 'bullet_list':
            return self._generate_bullet_list(elem, start, end)
        elif elem_type == 'comparison':
            return self._generate_comparison(elem, start, end)
        elif elem_type == 'flow':
            return self._generate_flow(elem, start, end)
        elif elem_type == 'arrow':
            return self._generate_arrow(elem, start, end)
        elif elem_type == 'arc_arrow':
            return self._generate_arc_arrow(elem, start, end)
        elif elem_type == 'code_block':
            return self._generate_code_block(elem, start, end)
        elif elem_type == 'grid':
            return self._generate_grid(elem, start, end)
        elif elem_type == 'checklist':
            return self._generate_checklist(elem, start, end)
        elif elem_type == 'stacked_boxes':
            return self._generate_stacked_boxes(elem, start, end)
        elif elem_type == 'particle_flow':
            return self._generate_particle_flow(elem, start, end)
        elif elem_type == 'similarity_meter':
            return self._generate_similarity_meter(elem, start, end)
        elif elem_type == 'progress_bar':
            return self._generate_progress_bar(elem, start, end)
        elif elem_type == 'weight_comparison':
            return self._generate_weight_comparison(elem, start, end)
        elif elem_type == 'scatter_3d':
            return self._generate_scatter_3d(elem, start, end)
        elif elem_type == 'vector_3d':
            return self._generate_vector_3d(elem, start, end)
        elif elem_type == 'neural_network':
            return self._generate_neural_network(elem, start, end)
        elif elem_type == 'code_execution':
            return self._generate_code_execution(elem, start, end)
        elif elem_type == 'conversation':
            return self._generate_conversation(elem, start, end)
        elif elem_type == 'timeline':
            return self._generate_timeline(elem, start, end)
        elif elem_type == 'attention_heatmap':
            return self._generate_attention_heatmap(elem, start, end)
        elif elem_type == 'token_flow':
            return self._generate_token_flow(elem, start, end)
        elif elem_type == 'model_comparison':
            return self._generate_model_comparison(elem, start, end)
        elif elem_type == 'parameter_slider':
            return self._generate_parameter_slider(elem, start, end)

        return f"\n        # TODO: Implement element type '{elem_type}'\n"

    def _get_easing_code(self, easing: str, var_name: str = 't') -> str:
        """Get the easing function code for a given easing type"""
        easing_map = {
            'linear': f'{var_name}',
            'ease_in': f'{var_name} * {var_name}',
            'ease_out': f'1 - (1 - {var_name}) ** 2',
            'ease_in_out': f'{var_name} * {var_name} * (3 - 2 * {var_name})',
            'ease_in_cubic': f'{var_name} ** 3',
            'ease_out_cubic': f'1 - (1 - {var_name}) ** 3',
            'elastic_out': f'(np.power(2, -10 * {var_name}) * np.sin(({var_name} - 0.075) * (2 * np.pi) / 0.3) + 1) if {var_name} > 0 else 0',
            'bounce_out': f'AnimationHelpers.ease_out_bounce({var_name})',
        }
        return easing_map.get(easing, easing_map['ease_in_out'])

    def _generate_text_element(self, elem: Dict, start: float, end: float, easing: str = 'ease_in_out') -> str:
        """Generate text element code"""
        pos = elem.get('position', {'x': 50, 'y': 50})
        content = self._escape_string(elem.get('content', ''))
        style = elem.get('style', {})

        fontsize = style.get('fontsize', 24)
        color = style.get('color', 'text')
        fontweight = style.get('fontweight', 'normal')
        ha = style.get('ha', 'center')
        va = style.get('va', 'center')

        continuous_effect = elem.get('continuous_effect', 'none')
        effect_frequency = elem.get('effect_frequency', 1.0)

        easing_expr = self._get_easing_code(easing, 't')

        code = f'''
        if progress > {start}:
            t = min(1.0, (progress - {start}) / {end - start})
            text_alpha = {easing_expr}
'''

        if continuous_effect == 'pulse':
            code += f'''            scale = 1.0 + 0.1 * np.sin(progress * 2 * np.pi * {effect_frequency})
            effective_fontsize = {fontsize} * scale
'''
        elif continuous_effect == 'breathing':
            code += f'''            scale = 1.0 + 0.05 * np.sin(progress * 2 * np.pi * {effect_frequency})
            effective_fontsize = {fontsize} * scale
'''
        else:
            code += f'''            effective_fontsize = {fontsize}
'''

        code += f'''            ax.text({pos['x']}, {pos['y']}, '{content}',
                    fontsize=effective_fontsize, fontweight='{fontweight}',
                    ha='{ha}', va='{va}',
                    color=self.colors['{color}'], alpha=text_alpha)
'''
        return code

    def _generate_box_element(self, elem: Dict, start: float, end: float) -> str:
        """Generate box element code"""
        pos = elem.get('position', {'x': 50, 'y': 50})
        width = elem.get('width', 60)
        height = elem.get('height', 20)
        style = elem.get('style', {})
        border_color = style.get('border_color', 'primary')

        title = elem.get('title')
        content = elem.get('content')
        icon = elem.get('icon')

        code = f'''
        if progress > {start}:
            box_alpha = min(1.0, (progress - {start}) / {end - start})

            box = FancyBboxPatch(
                ({pos['x'] - width/2}, {pos['y'] - height/2}), {width}, {height},
                boxstyle="round,pad=1",
                facecolor=self.colors['bg_light'],
                edgecolor=self.colors['{border_color}'],
                linewidth=3,
                alpha=0.95 * box_alpha
            )
            ax.add_patch(box)
'''

        if icon:
            code += f'''
            ax.text({pos['x'] - width/2 + 5}, {pos['y']}, '{icon}',
                    fontsize=36, ha='left', va='center', alpha=box_alpha)
'''

        if title:
            title_x = pos['x'] if not icon else pos['x']
            code += f'''
            ax.text({title_x}, {pos['y'] + height/4}, '{self._escape_string(title)}',
                    fontsize=24, fontweight='bold', ha='center', va='center',
                    color=self.colors['{border_color}'], alpha=box_alpha)
'''

        if content:
            code += f'''
            ax.text({pos['x']}, {pos['y'] - height/4}, '{self._escape_string(content)}',
                    fontsize=18, ha='center', va='center',
                    color=self.colors['text'], alpha=box_alpha * 0.9)
'''

        return code

    def _generate_bullet_list(self, elem: Dict, start: float, end: float) -> str:
        """Generate bullet list code"""
        pos = elem.get('position', {'x': 50, 'y': 50})
        items = elem.get('items', [])
        spacing = elem.get('spacing', 6)
        bullet = elem.get('bullet_char', '•')
        stagger = elem.get('stagger', True)

        if not items:
            return ''

        code = ''
        phase_duration = end - start
        item_duration = phase_duration / len(items) if stagger else phase_duration

        for i, item in enumerate(items):
            item_start = start + (i * item_duration) if stagger else start
            y_pos = pos['y'] - (i * spacing)

            code += f'''
        if progress > {item_start:.2f}:
            item_alpha = min(1.0, (progress - {item_start:.2f}) / {item_duration:.2f})
            ax.text({pos['x'] - 30}, {y_pos}, '{bullet} {self._escape_string(item)}',
                    fontsize=21, ha='left', va='center',
                    color=self.colors['text'], alpha=item_alpha)
'''

        return code

    def _generate_comparison(self, elem: Dict, start: float, end: float) -> str:
        """Generate comparison (before/after) element"""
        pos = elem.get('position', {'x': 50, 'y': 50})
        width = elem.get('width', 80)
        height = elem.get('height', 30)

        left_title = self._escape_string(elem.get('left_title', 'Before'))
        left_content = self._escape_string(elem.get('left_content', ''))
        left_color = elem.get('left_color', 'warning')

        right_title = self._escape_string(elem.get('right_title', 'After'))
        right_content = self._escape_string(elem.get('right_content', ''))
        right_color = elem.get('right_color', 'success')

        box_width = width / 2 - 5
        left_x = pos['x'] - width/4 - 2.5
        right_x = pos['x'] + width/4 + 2.5

        return f'''
        # Comparison: Left (before/bad)
        if progress > {start}:
            left_alpha = min(1.0, (progress - {start}) / {(end-start)/2})

            left_box = FancyBboxPatch(
                ({left_x - box_width/2}, {pos['y'] - height/2}), {box_width}, {height},
                boxstyle="round,pad=1",
                facecolor=self.colors['bg_light'],
                edgecolor=self.colors['{left_color}'],
                linewidth=3,
                alpha=0.95 * left_alpha
            )
            ax.add_patch(left_box)

            ax.text({left_x}, {pos['y'] + height/4}, '{left_title}',
                    fontsize=24, fontweight='bold', ha='center', va='center',
                    color=self.colors['{left_color}'], alpha=left_alpha)

            ax.text({left_x}, {pos['y'] - height/4}, '{left_content}',
                    fontsize=18, ha='center', va='center',
                    color=self.colors['text'], alpha=left_alpha * 0.9)

        # Comparison: Right (after/good)
        if progress > {start + (end-start)/2}:
            right_alpha = min(1.0, (progress - {start + (end-start)/2}) / {(end-start)/2})

            right_box = FancyBboxPatch(
                ({right_x - box_width/2}, {pos['y'] - height/2}), {box_width}, {height},
                boxstyle="round,pad=1",
                facecolor=self.colors['bg_light'],
                edgecolor=self.colors['{right_color}'],
                linewidth=3,
                alpha=0.95 * right_alpha
            )
            ax.add_patch(right_box)

            ax.text({right_x}, {pos['y'] + height/4}, '{right_title}',
                    fontsize=24, fontweight='bold', ha='center', va='center',
                    color=self.colors['{right_color}'], alpha=right_alpha)

            ax.text({right_x}, {pos['y'] - height/4}, '{right_content}',
                    fontsize=18, ha='center', va='center',
                    color=self.colors['text'], alpha=right_alpha * 0.9)
'''

    def _generate_flow(self, elem: Dict, start: float, end: float) -> str:
        """Generate horizontal flow element"""
        pos = elem.get('position', {'x': 50, 'y': 50})
        steps = elem.get('steps', [])
        width = elem.get('width', 80)
        stagger = elem.get('stagger', True)

        if not steps:
            return ''

        code = ''
        n_steps = len(steps)
        step_width = width / n_steps
        phase_duration = end - start
        step_duration = phase_duration / n_steps if stagger else phase_duration

        default_colors = ['warning', 'primary', 'success', 'accent']

        for i, step in enumerate(steps):
            step_start = start + (i * step_duration) if stagger else start
            x_pos = pos['x'] - width/2 + step_width/2 + (i * step_width)
            color = step.get('color', default_colors[i % len(default_colors)])
            icon = step.get('icon', '')
            title = self._escape_string(step.get('title', ''))
            subtitle = self._escape_string(step.get('subtitle', ''))

            code += f'''
        # Flow step {i + 1}
        if progress > {step_start:.2f}:
            step_alpha = min(1.0, (progress - {step_start:.2f}) / {step_duration:.2f})

            step_box = FancyBboxPatch(
                ({x_pos - step_width/2 + 2}, {pos['y'] - 12}), {step_width - 4}, 24,
                boxstyle="round,pad=0.5",
                facecolor=self.colors['bg_light'],
                edgecolor=self.colors['{color}'],
                linewidth=2,
                alpha=0.95 * step_alpha
            )
            ax.add_patch(step_box)

            ax.text({x_pos}, {pos['y'] + 6}, '{icon}',
                    fontsize=30, ha='center', va='center', alpha=step_alpha)
            ax.text({x_pos}, {pos['y'] - 2}, '{title}',
                    fontsize=18, fontweight='bold', ha='center', va='center',
                    color=self.colors['{color}'], alpha=step_alpha)
            ax.text({x_pos}, {pos['y'] - 8}, '{subtitle}',
                    fontsize=14, ha='center', va='center',
                    color=self.colors['text'], alpha=step_alpha * 0.7)
'''

            # Add arrow between steps
            if i < n_steps - 1:
                arrow_x = x_pos + step_width/2 - 1
                code += f'''
            if progress > {step_start + step_duration * 0.5:.2f}:
                ax.annotate('', xy=({arrow_x + 4}, {pos['y']}), xytext=({arrow_x}, {pos['y']}),
                           arrowprops=dict(arrowstyle='->', color=self.colors['dim'],
                                          lw=2), alpha=step_alpha)
'''

        return code

    def _generate_arrow(self, elem: Dict, start: float, end: float) -> str:
        """Generate arrow element"""
        s = elem.get('start', {'x': 30, 'y': 50})
        e = elem.get('end', {'x': 70, 'y': 50})
        color = elem.get('color', 'dim')

        return f'''
        if progress > {start}:
            arrow_alpha = min(1.0, (progress - {start}) / {end - start})
            ax.annotate('', xy=({e['x']}, {e['y']}), xytext=({s['x']}, {s['y']}),
                       arrowprops=dict(arrowstyle='->', color=self.colors['{color}'],
                                      lw=2), alpha=arrow_alpha)
'''

    def _generate_code_block(self, elem: Dict, start: float, end: float) -> str:
        """Generate code block element"""
        pos = elem.get('position', {'x': 50, 'y': 50})
        code_content = elem.get('code', '# Code here')
        width = elem.get('width', 60)
        height = elem.get('height', 25)

        # Escape the code for Python string
        escaped_code = code_content.replace('\\', '\\\\').replace("'", "\\'").replace('\n', '\\n')

        return f'''
        if progress > {start}:
            code_alpha = min(1.0, (progress - {start}) / {end - start})

            code_box = FancyBboxPatch(
                ({pos['x'] - width/2}, {pos['y'] - height/2}), {width}, {height},
                boxstyle="round,pad=0.5",
                facecolor='#1a1a2e',
                edgecolor=self.colors['dim'],
                linewidth=2,
                alpha=0.95 * code_alpha
            )
            ax.add_patch(code_box)

            code_text = '{escaped_code}'
            ax.text({pos['x']}, {pos['y']}, code_text,
                    fontsize=14, family='monospace', ha='center', va='center',
                    color='#a8ff60', alpha=code_alpha)
'''

    def _generate_grid(self, elem: Dict, start: float, end: float) -> str:
        """Generate grid of cards element"""
        pos = elem.get('position', {'x': 50, 'y': 50})
        columns = elem.get('columns', 2)
        rows = elem.get('rows', 2)
        cell_width = elem.get('cell_width', 36)
        cell_height = elem.get('cell_height', 14)
        items = elem.get('items', [])
        stagger = elem.get('stagger', True)

        if not items:
            return ''

        code = ''
        total_width = columns * cell_width
        total_height = rows * cell_height
        phase_duration = end - start
        item_duration = phase_duration / len(items) if stagger else phase_duration

        for idx, item in enumerate(items):
            row = idx // columns
            col = idx % columns
            item_start = start + (idx * item_duration) if stagger else start

            # Calculate position
            x_pos = pos['x'] - total_width/2 + cell_width/2 + (col * cell_width)
            y_pos = pos['y'] + total_height/2 - cell_height/2 - (row * cell_height)

            icon = item.get('icon', '')
            title = self._escape_string(item.get('title', ''))
            description = self._escape_string(item.get('description', ''))
            color = item.get('color', 'warning')

            code += f'''
        # Grid item {idx + 1}
        if progress > {item_start:.2f}:
            item_alpha = min(1.0, (progress - {item_start:.2f}) / {item_duration:.2f})

            grid_box = FancyBboxPatch(
                ({x_pos - cell_width/2 + 1}, {y_pos - cell_height/2 + 1}), {cell_width - 2}, {cell_height - 2},
                boxstyle="round,pad=0.8",
                facecolor=self.colors['bg_light'],
                edgecolor=self.colors['{color}'],
                linewidth=2,
                alpha=0.9 * item_alpha
            )
            ax.add_patch(grid_box)

            ax.text({x_pos}, {y_pos + cell_height/4}, '{icon}',
                    fontsize=30, ha='center', va='center', alpha=item_alpha)
            ax.text({x_pos}, {y_pos}, '{title}',
                    fontsize=15, fontweight='bold', ha='center', va='center',
                    color=self.colors['{color}'], alpha=item_alpha)
            ax.text({x_pos}, {y_pos - cell_height/4}, '{description}',
                    fontsize=11, ha='center', va='center',
                    color=self.colors['text'], alpha=item_alpha * 0.8,
                    linespacing=1.3)
'''

        return code

    def _generate_checklist(self, elem: Dict, start: float, end: float) -> str:
        """Generate checklist element"""
        pos = elem.get('position', {'x': 50, 'y': 50})
        items = elem.get('items', [])
        check_color = elem.get('check_color', 'secondary')
        text_color = elem.get('text_color', 'text')
        spacing = elem.get('spacing', 6.5)
        fontsize = elem.get('fontsize', 18)
        stagger = elem.get('stagger', True)

        if not items:
            return ''

        code = ''
        phase_duration = end - start
        item_duration = phase_duration / len(items) if stagger else phase_duration

        for idx, item in enumerate(items):
            item_start = start + (idx * item_duration) if stagger else start
            y_pos = pos['y'] + (len(items) / 2 - idx) * spacing
            escaped_item = self._escape_string(item)

            code += f'''
        # Checklist item {idx + 1}
        if progress > {item_start:.2f}:
            check_alpha = min(1.0, (progress - {item_start:.2f}) / {item_duration:.2f})

            ax.text(20, {y_pos}, '\\u2713',
                    fontsize=27, ha='center', va='center',
                    color=self.colors['{check_color}'], fontweight='bold',
                    alpha=check_alpha)

            ax.text(25, {y_pos}, '\\u2611 {escaped_item}',
                    fontsize={fontsize}, ha='left', va='center',
                    color=self.colors['{text_color}'], alpha=check_alpha)
'''

        return code

    def _generate_stacked_boxes(self, elem: Dict, start: float, end: float) -> str:
        """Generate vertically stacked boxes element"""
        pos = elem.get('position', {'x': 50, 'y': 50})
        items = elem.get('items', [])
        base_width = elem.get('base_width', 70)
        box_height = elem.get('box_height', 12)
        width_decrease = elem.get('width_decrease', 4)
        spacing = elem.get('spacing', 15)
        stagger = elem.get('stagger', True)

        if not items:
            return ''

        code = ''
        phase_duration = end - start
        item_duration = phase_duration / len(items) if stagger else phase_duration

        for idx, item in enumerate(items):
            item_start = start + (idx * item_duration) if stagger else start

            # Calculate dimensions - each box gets smaller
            width = base_width - (idx * width_decrease)
            x_start = pos['x'] - width/2
            y_pos = pos['y'] + (len(items)/2 - idx) * spacing

            title = self._escape_string(item.get('title', ''))
            description = self._escape_string(item.get('description', ''))
            color = item.get('color', 'primary')

            code += f'''
        # Stacked box {idx + 1}
        if progress > {item_start:.2f}:
            stack_alpha = min(1.0, (progress - {item_start:.2f}) / {item_duration:.2f})

            stack_box = FancyBboxPatch(
                ({x_start}, {y_pos - box_height/2}), {width}, {box_height},
                boxstyle="round,pad=0.8",
                facecolor=self.colors['bg_light'],
                edgecolor=self.colors['{color}'],
                linewidth=3,
                alpha=0.95 * stack_alpha
            )
            ax.add_patch(stack_box)

            ax.text({pos['x']}, {y_pos + 2}, '{title}',
                    fontsize=21, fontweight='bold', ha='center', va='center',
                    color=self.colors['{color}'], alpha=stack_alpha)
            ax.text({pos['x']}, {y_pos - 2}, '{description}',
                    fontsize=14, ha='center', va='center',
                    color=self.colors['text'], alpha=stack_alpha * 0.8)
'''

        return code

    # ========================================================================
    # New Element Generators (Phase 1-5)
    # ========================================================================

    def _generate_typewriter_text(self, elem: Dict, start: float, end: float) -> str:
        """Generate typewriter text element with character reveal"""
        pos = elem.get('position', {'x': 50, 'y': 50})
        content = self._escape_string(elem.get('content', ''))
        style = elem.get('style', {})
        show_cursor = elem.get('show_cursor', True)
        cursor_char = elem.get('cursor_char', '▌')
        cursor_blink_rate = elem.get('cursor_blink_rate', 2.0)
        speed = elem.get('speed', 1.0)  # Typing speed multiplier

        fontsize = style.get('fontsize', 24)
        color = style.get('color', 'text')
        fontweight = style.get('fontweight', 'normal')
        ha = style.get('ha', 'center')
        va = style.get('va', 'center')

        if show_cursor:
            return f'''
        # Typewriter text with cursor
        if progress > {start}:
            full_text = '{content}'
            type_progress = min(1.0, (progress - {start}) / {end - start}) * {speed}
            type_progress = min(1.0, type_progress)  # Clamp to 1.0
            num_chars = int(len(full_text) * type_progress)
            visible_text = full_text[:num_chars]

            # Blinking cursor
            show_cursor = num_chars < len(full_text) and int(progress * {cursor_blink_rate * 10}) % 2 == 0
            cursor = '{cursor_char}' if show_cursor else ''

            ax.text({pos['x']}, {pos['y']}, visible_text + cursor,
                    fontsize={fontsize}, fontweight='{fontweight}',
                    ha='{ha}', va='{va}',
                    color=self.colors['{color}'])
'''
        else:
            return f'''
        # Typewriter text
        if progress > {start}:
            full_text = '{content}'
            type_progress = min(1.0, (progress - {start}) / {end - start}) * {speed}
            type_progress = min(1.0, type_progress)  # Clamp to 1.0
            num_chars = int(len(full_text) * type_progress)
            visible_text = full_text[:num_chars]

            ax.text({pos['x']}, {pos['y']}, visible_text,
                    fontsize={fontsize}, fontweight='{fontweight}',
                    ha='{ha}', va='{va}',
                    color=self.colors['{color}'])
'''

    def _generate_particle_flow(self, elem: Dict, start: float, end: float) -> str:
        """Generate particle flow animation"""
        s = elem.get('start', {'x': 15, 'y': 50})
        e = elem.get('end', {'x': 85, 'y': 50})
        num_particles = elem.get('num_particles', 30)
        color = elem.get('color', 'accent')
        particle_size = elem.get('particle_size', 30)
        spread = elem.get('spread', 0.5)
        speed = elem.get('speed', 1.0)  # Speed multiplier

        return f'''
        # Particle flow animation
        if progress > {start}:
            flow_progress = min(1.0, (progress - {start}) / {end - start})
            flow_progress = flow_progress * {speed}  # Apply speed multiplier
            np.random.seed(42)  # Consistent randomness

            for i in range({num_particles}):
                # Stagger particle start times
                phase_offset = np.random.rand() * 0.3
                particle_prog = max(0, min(1, (flow_progress - phase_offset) / (1 - 0.3)))

                if particle_prog > 0:
                    # Interpolate position with random offset
                    offset = np.random.randn(2) * {spread}
                    px = {s['x']} + ({e['x']} - {s['x']}) * particle_prog + offset[0] * (1 - particle_prog)
                    py = {s['y']} + ({e['y']} - {s['y']}) * particle_prog + offset[1] * (1 - particle_prog)

                    # Fade in/out
                    particle_alpha = min(particle_prog * 3, (1 - particle_prog) * 3, 1.0)

                    ax.scatter([px], [py], c=[self.colors['{color}']],
                              s={particle_size}, alpha=particle_alpha,
                              edgecolors='none', zorder=100)
'''

    def _generate_similarity_meter(self, elem: Dict, start: float, end: float) -> str:
        """Generate similarity meter gauge widget"""
        pos = elem.get('position', {'x': 50, 'y': 50})
        score = elem.get('score', 75)
        radius = elem.get('radius', 8)
        label = self._escape_string(elem.get('label', 'Similarity'))
        low_color = elem.get('low_color', 'warning')
        medium_color = elem.get('medium_color', 'accent')
        high_color = elem.get('high_color', 'success')

        return f'''
        # Similarity meter
        if progress > {start}:
            meter_progress = min(1.0, (progress - {start}) / {end - start})
            target_score = {score}
            current_score = target_score * min(1.0, meter_progress * 2)

            # Background arc
            bg_wedge = Wedge(({pos['x']}, {pos['y']}), {radius}, 0, 180,
                            facecolor='#1a1a1a', edgecolor='#404040',
                            linewidth=2, alpha=0.9 * meter_progress)
            ax.add_patch(bg_wedge)

            # Score arc color
            if current_score < 50:
                meter_color = self.colors['{low_color}']
            elif current_score < 75:
                meter_color = self.colors['{medium_color}']
            else:
                meter_color = self.colors['{high_color}']

            angle = 180 * (current_score / 100)
            score_wedge = Wedge(({pos['x']}, {pos['y']}), {radius} * 0.9, 0, angle,
                               facecolor=meter_color, edgecolor='none',
                               alpha=0.8 * meter_progress)
            ax.add_patch(score_wedge)

            # Center circle cutout
            center = Circle(({pos['x']}, {pos['y']}), {radius} * 0.6,
                           facecolor=self.colors['bg'], edgecolor='none', zorder=10)
            ax.add_patch(center)

            # Score text
            ax.text({pos['x']}, {pos['y']}, f'{{int(current_score)}}%',
                   fontsize=28, fontweight='bold', ha='center', va='center',
                   color=meter_color, alpha=meter_progress)

            # Label
            ax.text({pos['x']}, {pos['y'] - radius - 2}, '{label}',
                   fontsize=18, ha='center', va='top',
                   color=self.colors['text'], alpha=meter_progress * 0.7)
'''

    def _generate_progress_bar(self, elem: Dict, start: float, end: float) -> str:
        """Generate progress bar element"""
        pos = elem.get('position', {'x': 50, 'y': 50})
        current = elem.get('current', 5)
        total = elem.get('total', 10)
        width = elem.get('width', 30)
        height = elem.get('height', 3)
        label = self._escape_string(elem.get('label', 'Progress'))
        color = elem.get('color', 'success')

        return f'''
        # Progress bar
        if progress > {start}:
            bar_progress = min(1.0, (progress - {start}) / {end - start})

            # Background
            bg_box = FancyBboxPatch(
                ({pos['x'] - width/2}, {pos['y'] - height/2}),
                {width}, {height},
                boxstyle="round,pad=0.2",
                facecolor='#1a1a1a',
                edgecolor='#404040',
                linewidth=2,
                alpha=0.9 * bar_progress
            )
            ax.add_patch(bg_box)

            # Progress fill
            fill_ratio = {current} / {total}
            fill_width = {width} * fill_ratio * bar_progress
            fill_box = FancyBboxPatch(
                ({pos['x'] - width/2}, {pos['y'] - height/2}),
                fill_width, {height},
                boxstyle="round,pad=0.2",
                facecolor=self.colors['{color}'],
                edgecolor='none',
                alpha=0.8 * bar_progress
            )
            ax.add_patch(fill_box)

            # Counter text
            ax.text({pos['x']}, {pos['y']}, f'{current}/{total}',
                   fontsize=16, fontweight='bold', ha='center', va='center',
                   color='white', zorder=20, alpha=bar_progress)

            # Label
            ax.text({pos['x']}, {pos['y'] + height + 1.5}, '{label}',
                   fontsize=14, ha='center', va='bottom',
                   color=self.colors['text'], alpha=bar_progress * 0.8)
'''

    def _generate_weight_comparison(self, elem: Dict, start: float, end: float) -> str:
        """Generate weight comparison with before/after bars"""
        pos = elem.get('position', {'x': 50, 'y': 50})
        before_weights = elem.get('before_weights', [0.5, 0.3, 0.8])
        after_weights = elem.get('after_weights', [0.7, 0.5, 0.6])
        bar_height = elem.get('bar_height', 20)
        labels = elem.get('labels', None)

        num_weights = len(before_weights)
        bar_spacing = bar_height / num_weights

        code = f'''
        # Weight comparison
        if progress > {start}:
            comp_progress = min(1.0, (progress - {start}) / {end - start})
'''

        for i, (before, after) in enumerate(zip(before_weights, after_weights)):
            y = pos['y'] + bar_height/2 - i * bar_spacing - bar_spacing/2
            delta = after - before
            delta_pct = (delta / abs(before) * 100) if before != 0 else 0

            # Color based on change
            if abs(delta_pct) < 5:
                color = 'dim'
            elif delta > 0:
                color = 'success'
            else:
                color = 'warning'

            label_text = labels[i] if labels and i < len(labels) else f'W{i+1}'

            # Pre-compute arrow direction
            arrow_x_offset = 4 if delta > 0 else -4

            code += f'''
            # Weight {i + 1}
            w{i}_y = {y}
            w{i}_before = {before}
            w{i}_after = {after}
            w{i}_delta_pct = {delta_pct:.1f}

            # Before bar
            if comp_progress > 0.3:
                before_alpha = min(1.0, (comp_progress - 0.3) / 0.2)
                ax.barh(w{i}_y, w{i}_before * 20, {bar_spacing * 0.7},
                       left={pos['x'] - 25}, color='#60A5FA',
                       alpha=0.6 * before_alpha, edgecolor='white', linewidth=0.5)
                ax.text({pos['x'] - 27}, w{i}_y, '{label_text}',
                       fontsize=12, ha='right', va='center',
                       color=self.colors['text'], alpha=before_alpha)

            # After bar
            if comp_progress > 0.5:
                after_alpha = min(1.0, (comp_progress - 0.5) / 0.2)
                ax.barh(w{i}_y, w{i}_after * 20, {bar_spacing * 0.7},
                       left={pos['x'] + 5}, color=self.colors['{color}'],
                       alpha=0.8 * after_alpha, edgecolor='white', linewidth=0.5)

            # Delta arrow
            if comp_progress > 0.7 and abs(w{i}_delta_pct) > 5:
                arrow_alpha = min(1.0, (comp_progress - 0.7) / 0.3)
                ax.annotate('', xy=({pos['x'] + arrow_x_offset}, w{i}_y),
                           xytext=({pos['x']}, w{i}_y),
                           arrowprops=dict(arrowstyle='->', color=self.colors['{color}'],
                                          lw=2), alpha=arrow_alpha)
                ax.text({pos['x'] + 1}, w{i}_y + {bar_spacing * 0.4},
                       f'{{w{i}_delta_pct:+.0f}}%',
                       fontsize=11, ha='center', va='bottom',
                       color=self.colors['{color}'], fontweight='bold',
                       alpha=arrow_alpha)
'''

        return code

    def _generate_scatter_3d(self, elem: Dict, start: float, end: float) -> str:
        """Generate 3D scatter plot"""
        points = elem.get('points', [])
        xlim = elem.get('xlim', (-5, 5))
        ylim = elem.get('ylim', (-5, 5))
        zlim = elem.get('zlim', (-5, 5))
        camera_elev = elem.get('camera_elev', 20)
        camera_azim = elem.get('camera_azim', 45)
        rotate_camera = elem.get('rotate_camera', False)
        camera_rotation_speed = elem.get('camera_rotation_speed', 90)
        stagger_points = elem.get('stagger_points', True)
        show_vectors = elem.get('show_vectors', True)

        if not points:
            return ''

        # This generates 3D subplot code - needs special handling
        code = f'''
        # 3D Scatter plot (requires special subplot handling)
        # Note: This should be the main element when using 3D
        if progress > {start}:
            scatter_progress = min(1.0, (progress - {start}) / {end - start})

            # Remove current axes and create 3D subplot
            self.fig.clear()
            ax3d = self.fig.add_subplot(111, projection='3d')
            ax3d.set_xlim({xlim[0]}, {xlim[1]})
            ax3d.set_ylim({ylim[0]}, {ylim[1]})
            ax3d.set_zlim({zlim[0]}, {zlim[1]})
'''
        if rotate_camera:
            code += f'''
            ax3d.view_init(elev={camera_elev}, azim={camera_azim} + scatter_progress * {camera_rotation_speed})
'''
        else:
            code += f'''
            ax3d.view_init(elev={camera_elev}, azim={camera_azim})
'''

        code += '''
            # Style 3D axes
            ax3d.set_facecolor(self.colors['bg'])
            ax3d.xaxis.pane.fill = True
            ax3d.yaxis.pane.fill = True
            ax3d.zaxis.pane.fill = True
            ax3d.xaxis.pane.set_facecolor((0.05, 0.05, 0.05, 0.3))
            ax3d.yaxis.pane.set_facecolor((0.05, 0.05, 0.05, 0.3))
            ax3d.zaxis.pane.set_facecolor((0.05, 0.05, 0.05, 0.3))
            ax3d.grid(True, alpha=0.2)
            ax3d.tick_params(colors=self.colors['text'], labelsize=10)
'''

        phase_duration = end - start
        point_duration = phase_duration / len(points) if stagger_points else phase_duration

        for i, pt in enumerate(points):
            pt_start = start + (i * point_duration) if stagger_points else start
            x, y, z = pt.get('x', 0), pt.get('y', 0), pt.get('z', 0)
            label = pt.get('label', '')
            color = pt.get('color', 'primary')

            code += f'''
            # Point {i + 1}: {label}
            if scatter_progress > {(pt_start - start) / phase_duration:.2f}:
                pt_alpha = min(1.0, (scatter_progress - {(pt_start - start) / phase_duration:.2f}) / {point_duration / phase_duration:.2f})
'''
            if show_vectors:
                code += f'''
                # Vector line from origin
                ax3d.plot([0, {x}], [0, {y}], [0, {z}],
                         color=self.colors['{color}'], linewidth=1.5,
                         alpha=pt_alpha * 0.6, linestyle='--')
'''
            code += f'''
                # Point
                ax3d.scatter([{x}], [{y}], [{z}], s=400,
                            c=[self.colors['{color}']], edgecolors='white',
                            linewidths=2, alpha=pt_alpha * 0.9, depthshade=True)
'''
            if label:
                code += f'''
                # Label
                ax3d.text({x}, {y}, {z} + 0.5, '{self._escape_string(label)}',
                         fontsize=14, ha='center', color='white',
                         alpha=pt_alpha,
                         bbox=dict(boxstyle='round,pad=0.3',
                                 facecolor=self.colors['{color}'],
                                 edgecolor='white', alpha=0.9))
'''

        return code

    def _generate_vector_3d(self, elem: Dict, start: float, end: float) -> str:
        """Generate 3D vectors from origin"""
        vectors = elem.get('vectors', [])
        xlim = elem.get('xlim', (-5, 5))
        ylim = elem.get('ylim', (-5, 5))
        zlim = elem.get('zlim', (-5, 5))
        camera_elev = elem.get('camera_elev', 20)
        camera_azim = elem.get('camera_azim', 45)
        rotate_camera = elem.get('rotate_camera', False)
        camera_rotation_speed = elem.get('camera_rotation_speed', 90)
        stagger = elem.get('stagger', True)

        if not vectors:
            return ''

        code = f'''
        # 3D Vectors
        if progress > {start}:
            vec_progress = min(1.0, (progress - {start}) / {end - start})

            self.fig.clear()
            ax3d = self.fig.add_subplot(111, projection='3d')
            ax3d.set_xlim({xlim[0]}, {xlim[1]})
            ax3d.set_ylim({ylim[0]}, {ylim[1]})
            ax3d.set_zlim({zlim[0]}, {zlim[1]})
'''
        if rotate_camera:
            code += f'''
            ax3d.view_init(elev={camera_elev}, azim={camera_azim} + vec_progress * {camera_rotation_speed})
'''
        else:
            code += f'''
            ax3d.view_init(elev={camera_elev}, azim={camera_azim})
'''

        code += '''
            ax3d.set_facecolor(self.colors['bg'])
            ax3d.grid(True, alpha=0.2)

            # Origin marker
            ax3d.scatter([0], [0], [0], s=100, c='white', marker='x', linewidths=2)
'''

        phase_duration = end - start
        vec_duration = phase_duration / len(vectors) if stagger else phase_duration

        for i, vec in enumerate(vectors):
            vec_start = start + (i * vec_duration) if stagger else start
            x, y, z = vec.get('x', 0), vec.get('y', 0), vec.get('z', 0)
            label = vec.get('label', f'v{i+1}')
            color = vec.get('color', 'primary')

            code += f'''
            # Vector {i + 1}
            if vec_progress > {(vec_start - start) / phase_duration:.2f}:
                v_alpha = min(1.0, (vec_progress - {(vec_start - start) / phase_duration:.2f}) / {vec_duration / phase_duration:.2f})

                # Arrow
                arrow = Arrow3D([0, {x}], [0, {y}], [0, {z}],
                               mutation_scale=15, lw=2,
                               arrowstyle='-|>', color=self.colors['{color}'],
                               alpha=v_alpha)
                ax3d.add_artist(arrow)

                # Label
                ax3d.text({x * 1.1}, {y * 1.1}, {z * 1.1}, '{self._escape_string(label)}',
                         fontsize=12, color=self.colors['{color}'],
                         fontweight='bold', alpha=v_alpha)
'''

        return code

    def _generate_arc_arrow(self, elem: Dict, start: float, end: float) -> str:
        """Generate curved arc arrow"""
        s = elem.get('start', {'x': 30, 'y': 50})
        e = elem.get('end', {'x': 70, 'y': 50})
        arc_height = elem.get('arc_height', 15)
        direction = elem.get('direction', 'up')
        color = elem.get('color', 'primary')
        width = elem.get('width', 2)

        sign = 1 if direction == 'up' else -1

        return f'''
        # Arc arrow
        if progress > {start}:
            arc_progress = min(1.0, (progress - {start}) / {end - start})

            # Generate arc points using quadratic bezier
            t = np.linspace(0, arc_progress, 50)
            mid_x = ({s['x']} + {e['x']}) / 2
            mid_y = ({s['y']} + {e['y']}) / 2 + {sign * arc_height}

            # Quadratic bezier curve
            arc_x = (1-t)**2 * {s['x']} + 2*(1-t)*t * mid_x + t**2 * {e['x']}
            arc_y = (1-t)**2 * {s['y']} + 2*(1-t)*t * mid_y + t**2 * {e['y']}

            ax.plot(arc_x, arc_y, color=self.colors['{color}'],
                   linewidth={width}, alpha=arc_progress, zorder=50)

            # Arrowhead at the end
            if arc_progress > 0.9:
                arrow_alpha = (arc_progress - 0.9) / 0.1
                # Calculate direction at endpoint
                dx = arc_x[-1] - arc_x[-2] if len(arc_x) > 1 else 1
                dy = arc_y[-1] - arc_y[-2] if len(arc_y) > 1 else 0
                ax.annotate('', xy=({e['x']}, {e['y']}),
                           xytext=(arc_x[-1] - dx*0.5, arc_y[-1] - dy*0.5),
                           arrowprops=dict(arrowstyle='->', color=self.colors['{color}'],
                                          lw={width}), alpha=arrow_alpha)
'''

    def _generate_neural_network(self, elem: Dict, start: float, end: float) -> str:
        """Generate neural network diagram"""
        pos = elem.get('position', {'x': 50, 'y': 50})
        layers = elem.get('layers', [3, 5, 5, 2])
        layer_labels = elem.get('layer_labels', None)
        width = elem.get('width', 70)
        height = elem.get('height', 50)
        node_color = elem.get('node_color', 'primary')
        connection_color = elem.get('connection_color', 'dim')
        stagger = elem.get('stagger', True)
        show_connections = elem.get('show_connections', True)

        num_layers = len(layers)
        layer_spacing = width / (num_layers - 1) if num_layers > 1 else width

        code = f'''
        # Neural network diagram
        if progress > {start}:
            nn_progress = min(1.0, (progress - {start}) / {end - start})
'''

        phase_duration = end - start
        layer_duration = phase_duration / num_layers if stagger else phase_duration

        for layer_idx, num_nodes in enumerate(layers):
            layer_start = start + (layer_idx * layer_duration) if stagger else start
            layer_x = pos['x'] - width/2 + layer_idx * layer_spacing
            max_nodes = max(layers)
            node_spacing = height / (max_nodes + 1)

            # Calculate vertical positions for this layer's nodes
            layer_height = (num_nodes - 1) * node_spacing
            start_y = pos['y'] + layer_height / 2

            code += f'''
            # Layer {layer_idx + 1}
            layer{layer_idx}_x = {layer_x}
            if nn_progress > {(layer_start - start) / phase_duration:.2f}:
                layer_alpha = min(1.0, (nn_progress - {(layer_start - start) / phase_duration:.2f}) / {layer_duration / phase_duration:.2f})
'''

            # Draw connections to previous layer
            if show_connections and layer_idx > 0:
                prev_num_nodes = layers[layer_idx - 1]
                prev_layer_height = (prev_num_nodes - 1) * node_spacing
                prev_start_y = pos['y'] + prev_layer_height / 2
                prev_layer_x = pos['x'] - width/2 + (layer_idx - 1) * layer_spacing

                code += f'''
                # Connections from layer {layer_idx}
                for prev_i in range({prev_num_nodes}):
                    prev_y = {prev_start_y} - prev_i * {node_spacing}
                    for curr_i in range({num_nodes}):
                        curr_y = {start_y} - curr_i * {node_spacing}
                        ax.plot([{prev_layer_x}, layer{layer_idx}_x],
                               [prev_y, curr_y],
                               color=self.colors['{connection_color}'],
                               linewidth=0.5, alpha=layer_alpha * 0.3, zorder=1)
'''

            # Draw nodes
            for node_idx in range(num_nodes):
                node_y = start_y - node_idx * node_spacing
                code += f'''
                # Node {node_idx + 1}
                node{layer_idx}_{node_idx} = Circle((layer{layer_idx}_x, {node_y}), 1.5,
                                                    facecolor=self.colors['{node_color}'],
                                                    edgecolor='white', linewidth=1.5,
                                                    alpha=layer_alpha * 0.9, zorder=10)
                ax.add_patch(node{layer_idx}_{node_idx})
'''

            # Layer label
            if layer_labels and layer_idx < len(layer_labels):
                label = self._escape_string(layer_labels[layer_idx])
                code += f'''
                ax.text(layer{layer_idx}_x, {pos['y'] - height/2 - 3}, '{label}',
                       fontsize=12, ha='center', va='top',
                       color=self.colors['text'], alpha=layer_alpha * 0.8)
'''

        return code

    def _generate_code_execution(self, elem: Dict, start: float, end: float) -> str:
        """Generate code block with execution output"""
        pos = elem.get('position', {'x': 50, 'y': 50})
        code = elem.get('code', '# code')
        output = elem.get('output', '# output')
        width = elem.get('width', 70)
        code_height = elem.get('code_height', 20)
        output_height = elem.get('output_height', 12)
        stagger = elem.get('stagger', True)

        escaped_code = code.replace('\\', '\\\\').replace("'", "\\'").replace('\n', '\\n')
        escaped_output = output.replace('\\', '\\\\').replace("'", "\\'").replace('\n', '\\n')

        return f'''
        # Code execution
        if progress > {start}:
            code_progress = min(1.0, (progress - {start}) / {end - start})

            # Code block
            code_box = FancyBboxPatch(
                ({pos['x'] - width/2}, {pos['y'] + output_height/2 + 2}),
                {width}, {code_height},
                boxstyle="round,pad=0.5",
                facecolor='#1a1a2e',
                edgecolor=self.colors['dim'],
                linewidth=2,
                alpha=0.95 * code_progress
            )
            ax.add_patch(code_box)

            ax.text({pos['x']}, {pos['y'] + output_height/2 + 2 + code_height/2},
                   '{escaped_code}',
                   fontsize=12, family='monospace', ha='center', va='center',
                   color='#a8ff60', alpha=code_progress)

        # Output (staggered)
        output_start = {start + (end - start) * 0.5 if stagger else start}
        if progress > output_start:
            out_progress = min(1.0, (progress - output_start) / ({end} - output_start))

            # Arrow
            ax.annotate('', xy=({pos['x']}, {pos['y'] - output_height/2}),
                       xytext=({pos['x']}, {pos['y'] + output_height/2}),
                       arrowprops=dict(arrowstyle='->', color=self.colors['accent'],
                                      lw=2), alpha=out_progress)

            # Output box
            out_box = FancyBboxPatch(
                ({pos['x'] - width/2}, {pos['y'] - output_height/2 - output_height}),
                {width}, {output_height},
                boxstyle="round,pad=0.5",
                facecolor='#1a2e1a',
                edgecolor=self.colors['success'],
                linewidth=2,
                alpha=0.95 * out_progress
            )
            ax.add_patch(out_box)

            ax.text({pos['x']}, {pos['y'] - output_height/2 - output_height/2},
                   '{escaped_output}',
                   fontsize=12, family='monospace', ha='center', va='center',
                   color='#60ffa8', alpha=out_progress)
'''

    def _generate_conversation(self, elem: Dict, start: float, end: float) -> str:
        """Generate chat-style conversation bubbles"""
        pos = elem.get('position', {'x': 50, 'y': 50})
        messages = elem.get('messages', [])
        width = elem.get('width', 70)
        bubble_spacing = elem.get('bubble_spacing', 4)
        user_color = elem.get('user_color', 'primary')
        assistant_color = elem.get('assistant_color', 'secondary')
        stagger = elem.get('stagger', True)

        if not messages:
            return ''

        code = ''
        phase_duration = end - start
        msg_duration = phase_duration / len(messages) if stagger else phase_duration
        bubble_height = 8

        for i, msg in enumerate(messages):
            msg_start = start + (i * msg_duration) if stagger else start
            role = msg.get('role', 'user')
            content = self._escape_string(msg.get('content', ''))
            name = msg.get('name', role.capitalize())

            is_user = role == 'user'
            color = user_color if is_user else assistant_color
            x_offset = -width/4 if is_user else width/4
            ha = 'left' if is_user else 'right'
            bubble_x = pos['x'] - width/2 if is_user else pos['x']
            y = pos['y'] + (len(messages)/2 - i - 0.5) * (bubble_height + bubble_spacing)

            code += f'''
        # Message {i + 1}: {role}
        if progress > {msg_start:.2f}:
            msg_alpha = min(1.0, (progress - {msg_start:.2f}) / {msg_duration:.2f})

            bubble = FancyBboxPatch(
                ({bubble_x}, {y - bubble_height/2}),
                {width/2 - 2}, {bubble_height},
                boxstyle="round,pad=0.5",
                facecolor=self.colors['bg_light'],
                edgecolor=self.colors['{color}'],
                linewidth=2,
                alpha=0.95 * msg_alpha
            )
            ax.add_patch(bubble)

            ax.text({bubble_x + 2}, {y + bubble_height/4}, '{name}:',
                   fontsize=10, fontweight='bold', ha='left', va='center',
                   color=self.colors['{color}'], alpha=msg_alpha)

            ax.text({bubble_x + 2}, {y - bubble_height/6}, '{content}',
                   fontsize=11, ha='left', va='center',
                   color=self.colors['text'], alpha=msg_alpha)
'''

        return code

    def _generate_timeline(self, elem: Dict, start: float, end: float) -> str:
        """Generate timeline with events"""
        pos = elem.get('position', {'x': 50, 'y': 50})
        events = elem.get('events', [])
        orientation = elem.get('orientation', 'horizontal')
        width = elem.get('width', 80)
        height = elem.get('height', 25)
        line_color = elem.get('line_color', 'dim')
        stagger = elem.get('stagger', True)

        if not events:
            return ''

        n_events = len(events)
        phase_duration = end - start
        event_duration = phase_duration / n_events if stagger else phase_duration

        code = f'''
        # Timeline
        if progress > {start}:
            tl_progress = min(1.0, (progress - {start}) / {end - start})

            # Main line
            ax.plot([{pos['x'] - width/2}, {pos['x'] + width/2}],
                   [{pos['y']}, {pos['y']}],
                   color=self.colors['{line_color}'], linewidth=3,
                   alpha=tl_progress * 0.8)
'''

        event_spacing = width / (n_events - 1) if n_events > 1 else 0

        for i, event in enumerate(events):
            event_start = start + (i * event_duration) if stagger else start
            x = pos['x'] - width/2 + i * event_spacing
            date = self._escape_string(event.get('date', ''))
            title = self._escape_string(event.get('title', ''))
            description = self._escape_string(event.get('description', ''))
            color = event.get('color', 'primary')

            code += f'''
        # Event {i + 1}
        if progress > {event_start:.2f}:
            ev_alpha = min(1.0, (progress - {event_start:.2f}) / {event_duration:.2f})

            # Marker
            marker = Circle(({x}, {pos['y']}), 1.5,
                          facecolor=self.colors['{color}'],
                          edgecolor='white', linewidth=2,
                          alpha=ev_alpha, zorder=10)
            ax.add_patch(marker)

            # Date
            ax.text({x}, {pos['y'] - 4}, '{date}',
                   fontsize=12, fontweight='bold', ha='center', va='top',
                   color=self.colors['{color}'], alpha=ev_alpha)

            # Title
            ax.text({x}, {pos['y'] + 4}, '{title}',
                   fontsize=14, fontweight='bold', ha='center', va='bottom',
                   color=self.colors['text'], alpha=ev_alpha)

            # Description
            ax.text({x}, {pos['y'] + 8}, '{description}',
                   fontsize=10, ha='center', va='bottom',
                   color=self.colors['dim'], alpha=ev_alpha * 0.8)
'''

        return code

    def _generate_attention_heatmap(self, elem: Dict, start: float, end: float) -> str:
        """Generate attention weights heatmap"""
        pos = elem.get('position', {'x': 50, 'y': 50})
        tokens_x = elem.get('tokens_x', ['The', 'cat', 'sat'])
        tokens_y = elem.get('tokens_y', ['The', 'cat', 'sat'])
        weights = elem.get('weights', None)
        width = elem.get('width', 50)
        height = elem.get('height', 50)
        title = self._escape_string(elem.get('title', 'Attention'))
        stagger = elem.get('stagger', True)

        n_x = len(tokens_x)
        n_y = len(tokens_y)
        cell_w = width / n_x
        cell_h = height / n_y

        code = f'''
        # Attention heatmap
        if progress > {start}:
            hm_progress = min(1.0, (progress - {start}) / {end - start})

            # Title
            ax.text({pos['x']}, {pos['y'] + height/2 + 5}, '{title}',
                   fontsize=18, fontweight='bold', ha='center', va='bottom',
                   color=self.colors['text'], alpha=hm_progress)

            # Generate weights if not provided
            np.random.seed(42)
            weights = np.random.rand({n_y}, {n_x})
            # Make diagonal stronger (self-attention pattern)
            for i in range(min({n_x}, {n_y})):
                weights[i, i] = 0.7 + np.random.rand() * 0.3
'''

        phase_duration = end - start
        row_duration = phase_duration / n_y if stagger else phase_duration

        for row in range(n_y):
            row_start = start + (row * row_duration) if stagger else start
            y = pos['y'] + height/2 - row * cell_h - cell_h/2
            token_y = self._escape_string(tokens_y[row])

            code += f'''
            # Row {row}
            if hm_progress > {(row_start - start) / phase_duration:.2f}:
                row_alpha = min(1.0, (hm_progress - {(row_start - start) / phase_duration:.2f}) / {row_duration / phase_duration:.2f})

                # Row label
                ax.text({pos['x'] - width/2 - 2}, {y}, '{token_y}',
                       fontsize=12, ha='right', va='center',
                       color=self.colors['text'], alpha=row_alpha)
'''
            for col in range(n_x):
                x = pos['x'] - width/2 + col * cell_w + cell_w/2

                code += f'''
                # Cell ({row}, {col})
                w = weights[{row}, {col}]
                cell = FancyBboxPatch(
                    ({x - cell_w/2 + 0.5}, {y - cell_h/2 + 0.5}),
                    {cell_w - 1}, {cell_h - 1},
                    boxstyle="round,pad=0.1",
                    facecolor=plt.cm.viridis(w),
                    edgecolor='#333',
                    linewidth=0.5,
                    alpha=row_alpha * 0.9
                )
                ax.add_patch(cell)

                ax.text({x}, {y}, f'{{w:.2f}}',
                       fontsize=8, ha='center', va='center',
                       color='white' if w > 0.5 else 'black',
                       alpha=row_alpha)
'''

        # Column labels
        for col in range(n_x):
            x = pos['x'] - width/2 + col * cell_w + cell_w/2
            token_x = self._escape_string(tokens_x[col])
            code += f'''
            ax.text({x}, {pos['y'] - height/2 - 2}, '{token_x}',
                   fontsize=12, ha='center', va='top',
                   color=self.colors['text'], alpha=hm_progress)
'''

        return code

    def _generate_token_flow(self, elem: Dict, start: float, end: float) -> str:
        """Generate tokenization pipeline visualization"""
        pos = elem.get('position', {'x': 50, 'y': 50})
        input_text = self._escape_string(elem.get('input_text', 'Hello'))
        tokens = elem.get('tokens', None)
        width = elem.get('width', 80)
        stagger = elem.get('stagger', True)

        code = f'''
        # Token flow pipeline
        if progress > {start}:
            tf_progress = min(1.0, (progress - {start}) / {end - start})

            # Stage 1: Input text
            if tf_progress > 0:
                stage1_alpha = min(1.0, tf_progress / 0.25)

                ax.text({pos['x'] - width/2 + 5}, {pos['y'] + 15}, 'Input Text:',
                       fontsize=12, fontweight='bold', ha='left', va='center',
                       color=self.colors['dim'], alpha=stage1_alpha)

                text_box = FancyBboxPatch(
                    ({pos['x'] - width/2}, {pos['y'] + 5}),
                    {width}, 8,
                    boxstyle="round,pad=0.5",
                    facecolor=self.colors['bg_light'],
                    edgecolor=self.colors['primary'],
                    linewidth=2,
                    alpha=0.95 * stage1_alpha
                )
                ax.add_patch(text_box)

                ax.text({pos['x']}, {pos['y'] + 9}, '"{input_text}"',
                       fontsize=14, ha='center', va='center',
                       color=self.colors['text'], alpha=stage1_alpha)

            # Stage 2: Tokens
            if tf_progress > 0.25:
                stage2_alpha = min(1.0, (tf_progress - 0.25) / 0.25)

                # Arrow
                ax.annotate('', xy=({pos['x']}, {pos['y'] - 2}),
                           xytext=({pos['x']}, {pos['y'] + 4}),
                           arrowprops=dict(arrowstyle='->', color=self.colors['accent'],
                                          lw=2), alpha=stage2_alpha)

                ax.text({pos['x'] - width/2 + 5}, {pos['y'] - 5}, 'Tokens:',
                       fontsize=12, fontweight='bold', ha='left', va='center',
                       color=self.colors['dim'], alpha=stage2_alpha)

                # Generate tokens from input
                tokens = '{input_text}'.split()
                token_width = min(12, {width} / (len(tokens) + 1))
                for i, tok in enumerate(tokens):
                    tx = {pos['x'] - width/2} + 10 + i * (token_width + 2)
                    tok_box = FancyBboxPatch(
                        (tx, {pos['y'] - 15}),
                        token_width, 8,
                        boxstyle="round,pad=0.3",
                        facecolor=self.colors['bg_light'],
                        edgecolor=self.colors['secondary'],
                        linewidth=1.5,
                        alpha=0.95 * stage2_alpha
                    )
                    ax.add_patch(tok_box)
                    ax.text(tx + token_width/2, {pos['y'] - 11}, tok,
                           fontsize=10, ha='center', va='center',
                           color=self.colors['text'], alpha=stage2_alpha)

            # Stage 3: Embeddings
            if tf_progress > 0.55:
                stage3_alpha = min(1.0, (tf_progress - 0.55) / 0.25)

                ax.annotate('', xy=({pos['x']}, {pos['y'] - 20}),
                           xytext=({pos['x']}, {pos['y'] - 16}),
                           arrowprops=dict(arrowstyle='->', color=self.colors['accent'],
                                          lw=2), alpha=stage3_alpha)

                ax.text({pos['x'] - width/2 + 5}, {pos['y'] - 23}, 'Embeddings:',
                       fontsize=12, fontweight='bold', ha='left', va='center',
                       color=self.colors['dim'], alpha=stage3_alpha)

                emb_box = FancyBboxPatch(
                    ({pos['x'] - width/2}, {pos['y'] - 35}),
                    {width}, 10,
                    boxstyle="round,pad=0.5",
                    facecolor='#1a2e1a',
                    edgecolor=self.colors['success'],
                    linewidth=2,
                    alpha=0.95 * stage3_alpha
                )
                ax.add_patch(emb_box)

                ax.text({pos['x']}, {pos['y'] - 30}, '[0.23, -0.15, 0.87, ..., 768 dims]',
                       fontsize=11, family='monospace', ha='center', va='center',
                       color='#60ffa8', alpha=stage3_alpha)
'''

        return code

    def _generate_model_comparison(self, elem: Dict, start: float, end: float) -> str:
        """Generate side-by-side model comparison"""
        pos = elem.get('position', {'x': 50, 'y': 50})
        models = elem.get('models', [])
        comparison_rows = elem.get('comparison_rows', [])
        width = elem.get('width', 85)
        height = elem.get('height', 50)
        stagger = elem.get('stagger', True)

        if not models:
            return ''

        n_models = len(models)
        col_width = width / (n_models + 1)  # +1 for label column
        n_rows = len(comparison_rows)
        row_height = height / (n_rows + 1) if n_rows > 0 else height  # +1 for header

        code = f'''
        # Model comparison table
        if progress > {start}:
            mc_progress = min(1.0, (progress - {start}) / {end - start})

            # Header row
            for i, model in enumerate({[m.get('name', f'Model {j+1}') for j, m in enumerate(models)]}):
                x = {pos['x'] - width/2} + {col_width} * (i + 1.5)
                ax.text(x, {pos['y'] + height/2 - 3}, model,
                       fontsize=14, fontweight='bold', ha='center', va='center',
                       color=self.colors['primary'], alpha=mc_progress)
'''

        phase_duration = end - start
        row_duration = phase_duration / (n_rows + 1) if stagger and n_rows > 0 else phase_duration

        for row_idx, row_label in enumerate(comparison_rows):
            row_start = start + ((row_idx + 1) * row_duration) if stagger else start
            y = pos['y'] + height/2 - (row_idx + 1.5) * row_height
            escaped_label = self._escape_string(row_label)

            code += f'''
            # Row: {row_label}
            if mc_progress > {(row_start - start) / phase_duration:.2f}:
                row_alpha = min(1.0, (mc_progress - {(row_start - start) / phase_duration:.2f}) / {row_duration / phase_duration:.2f})

                ax.text({pos['x'] - width/2 + col_width/2}, {y}, '{escaped_label}',
                       fontsize=11, ha='center', va='center',
                       color=self.colors['dim'], alpha=row_alpha)
'''

            for model_idx, model in enumerate(models):
                x = pos['x'] - width/2 + col_width * (model_idx + 1.5)
                # Get value for this row from model data
                value = model.get(row_label.lower().replace(' ', '_'), '-')
                if isinstance(value, list):
                    value = ', '.join(str(v) for v in value[:2]) + ('...' if len(value) > 2 else '')
                escaped_value = self._escape_string(str(value))
                color = model.get('color', 'text')

                code += f'''
                ax.text({x}, {y}, '{escaped_value}',
                       fontsize=11, ha='center', va='center',
                       color=self.colors['{color}'], alpha=row_alpha)
'''

        return code

    def _generate_parameter_slider(self, elem: Dict, start: float, end: float) -> str:
        """Generate parameter slider visualization"""
        pos = elem.get('position', {'x': 50, 'y': 50})
        label = self._escape_string(elem.get('label', 'Parameter'))
        min_val = elem.get('min_value', 0.0)
        max_val = elem.get('max_value', 1.0)
        current = elem.get('current_value', 0.5)
        width = elem.get('width', 40)
        description = self._escape_string(elem.get('description', ''))
        effect_preview = self._escape_string(elem.get('effect_preview', ''))
        color = elem.get('color', 'accent')

        # Calculate slider position
        ratio = (current - min_val) / (max_val - min_val) if max_val != min_val else 0.5

        return f'''
        # Parameter slider
        if progress > {start}:
            sl_progress = min(1.0, (progress - {start}) / {end - start})

            # Label
            ax.text({pos['x']}, {pos['y'] + 8}, '{label}',
                   fontsize=16, fontweight='bold', ha='center', va='bottom',
                   color=self.colors['text'], alpha=sl_progress)

            # Slider track
            track = FancyBboxPatch(
                ({pos['x'] - width/2}, {pos['y'] - 1}),
                {width}, 2,
                boxstyle="round,pad=0.2",
                facecolor='#333',
                edgecolor='#555',
                linewidth=1,
                alpha=sl_progress
            )
            ax.add_patch(track)

            # Filled portion
            fill_width = {width * ratio} * min(1.0, sl_progress * 2)
            fill = FancyBboxPatch(
                ({pos['x'] - width/2}, {pos['y'] - 1}),
                fill_width, 2,
                boxstyle="round,pad=0.2",
                facecolor=self.colors['{color}'],
                edgecolor='none',
                alpha=sl_progress * 0.8
            )
            ax.add_patch(fill)

            # Handle
            handle_x = {pos['x'] - width/2} + fill_width
            handle = Circle((handle_x, {pos['y']}), 1.5,
                           facecolor='white',
                           edgecolor=self.colors['{color}'],
                           linewidth=2, alpha=sl_progress, zorder=10)
            ax.add_patch(handle)

            # Min/Max labels
            ax.text({pos['x'] - width/2}, {pos['y'] - 4}, '{min_val}',
                   fontsize=10, ha='center', va='top',
                   color=self.colors['dim'], alpha=sl_progress)
            ax.text({pos['x'] + width/2}, {pos['y'] - 4}, '{max_val}',
                   fontsize=10, ha='center', va='top',
                   color=self.colors['dim'], alpha=sl_progress)

            # Current value
            ax.text(handle_x, {pos['y'] + 3}, '{current}',
                   fontsize=12, fontweight='bold', ha='center', va='bottom',
                   color=self.colors['{color}'], alpha=sl_progress)
'''

    def generate_main_block(self) -> str:
        """Generate __main__ block"""
        return f'''

def run():
    """Run the presentation"""
    pres = {self.class_name}()
    pres.show()


if __name__ == "__main__":
    run()
'''

    def generate(self) -> str:
        """Generate complete presentation Python code"""
        parts = [
            self.generate_imports(),
            self.generate_class_header(),
            self.generate_get_frames_for_step(),
            self.generate_landing_page(),
            self.generate_animate_step(),
            self.generate_draw_current_step_static(),
        ]

        # Generate step methods
        for i, step in enumerate(self.schema.steps):
            parts.append(self.generate_step_method(step, i))

        parts.append(self.generate_main_block())

        return ''.join(parts)

    def to_file(self, path: str):
        """Generate and save to file"""
        code = self.generate()
        with open(path, 'w', encoding='utf-8') as f:
            f.write(code)
        print(f"Generated: {path}")


def generate_from_json(json_path: str, output_path: Optional[str] = None) -> str:
    """
    Generate Python presentation code from JSON schema file

    Args:
        json_path: Path to JSON schema file
        output_path: Optional output path (defaults to same name with .py)

    Returns:
        Generated Python code
    """
    schema = PresentationSchema.from_file(json_path)
    generator = PresentationGenerator(schema)

    code = generator.generate()

    if output_path is None:
        output_path = str(Path(json_path).with_suffix('.py'))

    generator.to_file(output_path)
    return code


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Generate Python presentation from JSON")
    parser.add_argument('json_file', help="Path to JSON schema file")
    parser.add_argument('-o', '--output', help="Output Python file path")

    args = parser.parse_args()

    generate_from_json(args.json_file, args.output)
