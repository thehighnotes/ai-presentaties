"""
Presentation Code Generator V2
Generates Python presentation code from JSON schema using centralized element rendering.

This version produces much smaller presentations by using core/element_rendering.py
instead of inlining all rendering code.
"""

import json
from pathlib import Path
from typing import Dict, Any, List, Optional
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))

from tools.schema import PresentationSchema, Step


class PresentationGeneratorV2:
    """Generates Python presentation code from schema using centralized rendering"""

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

    def _format_dict(self, d: Dict, indent: int = 12) -> str:
        """Format a dict as Python code"""
        # Use json.dumps for clean formatting, then convert to Python syntax
        s = json.dumps(d, indent=4)
        # Indent each line
        lines = s.split('\n')
        ind = ' ' * indent
        return ('\n' + ind).join(lines)

    def generate_imports(self) -> str:
        """Generate import statements"""
        return f'''"""
{self.schema.title}
{self.schema.description or "Auto-generated presentation"}

Generated using centralized element rendering for consistency with designer preview.
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from matplotlib.patches import FancyBboxPatch
import matplotlib.pyplot as plt

from core import BasePresentation, PresentationStyle
from core.element_rendering import ElementRenderer, render_step
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

        # Step data for centralized rendering
        self._step_data = self._init_step_data()

        self.show_landing_page()

    def _init_step_data(self):
        """Initialize step data dictionaries"""
        return {self._generate_step_data()}
'''

    def _generate_step_data(self) -> str:
        """Generate the step data dictionary"""
        steps = {}
        for i, step in enumerate(self.schema.steps):
            step_dict = {
                'title': step.title or step.name,
                'subtitle': step.subtitle or '',
                'elements': step.elements,
                'animation_frames': step.animation_frames
            }
            steps[i + 1] = step_dict  # +1 because landing is step 0

        # Format as Python dict
        lines = ['{']
        for step_idx, step_dict in steps.items():
            lines.append(f'            {step_idx}: {{')
            lines.append(f"                'title': '{self._escape_string(step_dict['title'])}',")
            lines.append(f"                'subtitle': '{self._escape_string(step_dict['subtitle'])}',")
            lines.append(f"                'animation_frames': {step_dict['animation_frames']},")
            lines.append(f"                'elements': {self._format_elements(step_dict['elements'])},")
            lines.append('            },')
        lines.append('        }')
        return '\n'.join(lines)

    def _format_elements(self, elements: List[Dict]) -> str:
        """Format elements list as Python code"""
        if not elements:
            return '[]'

        # Use json for clean formatting
        s = json.dumps(elements, indent=4)
        # Convert JSON booleans to Python booleans
        s = s.replace(': true', ': True').replace(': false', ': False')
        s = s.replace(': null', ': None')
        # Indent for nesting inside the dict
        lines = s.split('\n')
        indented = [lines[0]]
        for line in lines[1:]:
            indented.append('                ' + line)
        return '\n'.join(indented)

    def generate_get_frames_for_step(self) -> str:
        """Generate get_frames_for_step method"""
        return '''
    def get_frames_for_step(self, step: int) -> int:
        """Get animation frame count for each step"""
        if step in self._step_data:
            return self._step_data[step].get('animation_frames', 60)
        return 60
'''

    def generate_landing_page(self) -> str:
        """Generate show_landing_page method"""
        land = self.schema.landing

        return f'''
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
            linewidth=4
        )
        ax.add_patch(title_box)

        # Title
        ax.text(50, 67, '{self._escape_string(land.title)}',
                fontsize=42, fontweight='bold', ha='center', va='center',
                color=self.colors['primary'])

        # Subtitle
        ax.text(50, 48, '{self._escape_string(land.subtitle)}',
                fontsize=24, ha='center', va='top',
                color=self.colors['text'])

        # Tagline
        ax.text(50, 15, '{self._escape_string(land.tagline)}',
                fontsize=18, ha='center', va='center',
                color=self.colors['dim'], style='italic')

        # Navigation hint
        ax.text(50, 5, 'Press SPACE to begin',
                fontsize=12, ha='center', va='center',
                color=self.colors['dim'])
'''

    def generate_animate_step(self) -> str:
        """Generate animate_step method using centralized renderer"""
        return '''
    def animate_step(self, frame: int):
        """Animate current step using centralized renderer"""
        total_frames = self.get_frames_for_step(self.current_step)
        progress = frame / (total_frames - 1) if total_frames > 1 else 1

        if self.current_step == 0:
            pass  # Landing is static
        elif self.current_step in self._step_data:
            self._render_step(self.current_step, progress)

        if frame >= total_frames - 1:
            self.is_animating = False
'''

    def generate_draw_current_step_static(self) -> str:
        """Generate draw_current_step_static method"""
        return '''
    def draw_current_step_static(self):
        """Draw current step without animation"""
        if self.current_step == -1:
            self.show_landing_page()
        elif self.current_step in self._step_data:
            self._render_step(self.current_step, 1.0)
        plt.draw()
'''

    def generate_render_step(self) -> str:
        """Generate the _render_step method that uses centralized rendering"""
        return '''
    def _render_step(self, step_idx: int, progress: float):
        """Render a step using centralized element rendering"""
        step_data = self._step_data.get(step_idx, {})

        self.fig.clear()
        ax = self.fig.add_subplot(111)
        ax.axis('off')
        ax.set_xlim(0, 100)
        ax.set_ylim(0, 100)

        # Use centralized renderer
        render_step(ax, step_data, progress, colors=self.colors, show_title=True)

        # Add status indicator
        self.add_status_indicator(progress < 1.0)
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
            self.generate_render_step(),
            self.generate_main_block(),
        ]

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
        output_path: Optional output path (defaults to presentations/ folder)

    Returns:
        Generated Python code
    """
    schema = PresentationSchema.from_file(json_path)
    generator = PresentationGeneratorV2(schema)

    code = generator.generate()

    if output_path is None:
        # Default to presentations folder
        json_name = Path(json_path).stem
        output_path = str(Path(__file__).parent.parent / 'presentations' / f'{json_name}_presentation.py')

    generator.to_file(output_path)
    return code


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Generate Python presentation from JSON (V2 - centralized rendering)")
    parser.add_argument('json_file', help="Path to JSON schema file")
    parser.add_argument('-o', '--output', help="Output Python file path")

    args = parser.parse_args()

    generate_from_json(args.json_file, args.output)
