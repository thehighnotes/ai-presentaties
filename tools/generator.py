"""
Presentation Code Generator
Generates Python presentation code from JSON schema
"""

import textwrap
from pathlib import Path
from typing import Dict, Any, List, Optional
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))

from tools.schema import PresentationSchema, Step, LandingPage


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
        return '''"""
{title}
{description}
"""

import sys
import os
import numpy as np
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle
import matplotlib.pyplot as plt

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core import BasePresentation, PresentationStyle
'''.format(
            title=self.schema.title,
            description=self.schema.description or "Auto-generated presentation"
        )

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

        if elem_type == 'text':
            return self._generate_text_element(elem, start, end)
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
        elif elem_type == 'code_block':
            return self._generate_code_block(elem, start, end)
        elif elem_type == 'grid':
            return self._generate_grid(elem, start, end)
        elif elem_type == 'checklist':
            return self._generate_checklist(elem, start, end)
        elif elem_type == 'stacked_boxes':
            return self._generate_stacked_boxes(elem, start, end)

        return f"\n        # TODO: Implement element type '{elem_type}'\n"

    def _generate_text_element(self, elem: Dict, start: float, end: float) -> str:
        """Generate text element code"""
        pos = elem.get('position', {'x': 50, 'y': 50})
        content = self._escape_string(elem.get('content', ''))
        style = elem.get('style', {})

        fontsize = style.get('fontsize', 24)
        color = style.get('color', 'text')
        fontweight = style.get('fontweight', 'normal')
        ha = style.get('ha', 'center')
        va = style.get('va', 'center')

        return f'''
        if progress > {start}:
            text_alpha = min(1.0, (progress - {start}) / {end - start})
            ax.text({pos['x']}, {pos['y']}, '{content}',
                    fontsize={fontsize}, fontweight='{fontweight}',
                    ha='{ha}', va='{va}',
                    color=self.colors['{color}'], alpha=text_alpha)
'''

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
