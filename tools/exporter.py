"""
Presentation Exporter
Extracts structure and content from existing Python presentations to JSON
"""

import ast
import re
import os
import sys
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple

# Add parent to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from tools.schema import PresentationSchema, Step, LandingPage


class PresentationAnalyzer(ast.NodeVisitor):
    """AST visitor to extract presentation structure"""

    def __init__(self):
        self.class_name: Optional[str] = None
        self.step_names: List[str] = []
        self.title: Optional[str] = None
        self.strings: List[Tuple[int, str]] = []  # (line_no, string)
        self.method_strings: Dict[str, List[str]] = {}  # method -> strings
        self.current_method: Optional[str] = None

    def visit_ClassDef(self, node: ast.ClassDef):
        """Extract class name"""
        if 'Presentation' in node.name:
            self.class_name = node.name
        self.generic_visit(node)

    def visit_FunctionDef(self, node: ast.FunctionDef):
        """Track current method and extract strings"""
        self.current_method = node.name
        if node.name not in self.method_strings:
            self.method_strings[node.name] = []
        self.generic_visit(node)
        self.current_method = None

    def visit_Assign(self, node: ast.Assign):
        """Extract step_names list assignment"""
        for target in node.targets:
            if isinstance(target, ast.Name) and target.id == 'step_names':
                if isinstance(node.value, ast.List):
                    for elt in node.value.elts:
                        if isinstance(elt, ast.Constant) and isinstance(elt.value, str):
                            self.step_names.append(elt.value)
        self.generic_visit(node)

    def visit_Call(self, node: ast.Call):
        """Extract strings from method calls (ax.text, etc.)"""
        # Look for ax.text() calls with string content
        if isinstance(node.func, ast.Attribute):
            if node.func.attr == 'text':
                for arg in node.args:
                    if isinstance(arg, ast.Constant) and isinstance(arg.value, str):
                        self.strings.append((node.lineno, arg.value))
                        if self.current_method:
                            self.method_strings[self.current_method].append(arg.value)

        # Look for super().__init__ with title
        if isinstance(node.func, ast.Attribute):
            if node.func.attr == '__init__':
                if isinstance(node.func.value, ast.Call):
                    if isinstance(node.func.value.func, ast.Name):
                        if node.func.value.func.id == 'super':
                            # First arg after self is usually title
                            for arg in node.args:
                                if isinstance(arg, ast.Constant) and isinstance(arg.value, str):
                                    self.title = arg.value
                                    break

        self.generic_visit(node)


def analyze_presentation_file(filepath: str) -> Dict[str, Any]:
    """
    Analyze a presentation Python file and extract structure

    Returns dict with:
    - class_name: str
    - title: str
    - step_names: List[str]
    - methods: Dict[str, List[str]] - method name -> strings found
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        source = f.read()

    tree = ast.parse(source)
    analyzer = PresentationAnalyzer()
    analyzer.visit(tree)

    return {
        'file': filepath,
        'class_name': analyzer.class_name,
        'title': analyzer.title,
        'step_names': analyzer.step_names,
        'total_steps': len(analyzer.step_names),
        'methods': analyzer.method_strings,
        'all_strings': analyzer.strings
    }


def extract_step_content(source_code: str, step_name: str) -> Dict[str, Any]:
    """
    Extract content for a specific step by analyzing draw_* methods

    This is a heuristic-based extraction - not perfect but helpful
    """
    # Find method name pattern
    method_patterns = [
        f"draw_{step_name.lower().replace(' ', '_').replace('-', '_')}",
        f"draw_step_{step_name.lower().replace(' ', '_')}",
    ]

    content = {
        'texts': [],
        'boxes': [],
        'colors_used': set(),
        'fontsize_values': set()
    }

    # Extract ax.text() calls
    text_pattern = r"ax\.text\s*\(\s*([0-9.]+)\s*,\s*([0-9.]+)\s*,\s*['\"](.+?)['\"]"
    for match in re.finditer(text_pattern, source_code, re.DOTALL):
        x, y, text = match.groups()
        content['texts'].append({
            'x': float(x),
            'y': float(y),
            'text': text.replace('\\n', '\n')
        })

    # Extract color references
    color_pattern = r"self\.colors\['(\w+)'\]"
    for match in re.finditer(color_pattern, source_code):
        content['colors_used'].add(match.group(1))

    # Extract fontsize values
    fontsize_pattern = r"fontsize\s*=\s*(\d+)"
    for match in re.finditer(fontsize_pattern, source_code):
        content['fontsize_values'].add(int(match.group(1)))

    content['colors_used'] = list(content['colors_used'])
    content['fontsize_values'] = sorted(list(content['fontsize_values']))

    return content


def export_presentation(filepath: str, output_path: Optional[str] = None) -> PresentationSchema:
    """
    Export a presentation to JSON schema format

    This creates a skeletal schema that can be manually enriched
    """
    analysis = analyze_presentation_file(filepath)

    # Read source for content extraction
    with open(filepath, 'r', encoding='utf-8') as f:
        source = f.read()

    # Create steps from step_names
    steps = []
    for i, name in enumerate(analysis['step_names']):
        if name == 'Landing':
            continue  # Landing is separate

        # Find the draw method for this step
        method_name = None
        step_strings = []

        # Try to find corresponding method
        for mname, mstrings in analysis['methods'].items():
            if 'draw' in mname.lower():
                # Heuristic: method index might match step index
                step_strings = mstrings

        step = Step(
            name=name,
            title=name,  # Use step name as default title
            elements=[],
            notes=f"Extracted from {analysis['class_name']} step {i}"
        )
        steps.append(step)

    # Create schema
    schema = PresentationSchema(
        name=Path(filepath).stem,
        title=analysis['title'] or "Untitled Presentation",
        description=f"Exported from {Path(filepath).name}",
        landing=LandingPage(
            title=analysis['title'] or "Presentatie",
        ),
        steps=steps
    )

    # Save if output path provided
    if output_path:
        schema.to_file(output_path)
        print(f"Exported to: {output_path}")

    return schema


def export_all_presentations(presentations_dir: str, output_dir: str):
    """Export all presentations in a directory"""
    pres_path = Path(presentations_dir)
    out_path = Path(output_dir)
    out_path.mkdir(exist_ok=True)

    exported = []
    for pyfile in pres_path.glob('*_presentation*.py'):
        if '__pycache__' in str(pyfile):
            continue

        try:
            output_file = out_path / f"{pyfile.stem}.json"
            schema = export_presentation(str(pyfile), str(output_file))
            exported.append({
                'source': str(pyfile),
                'output': str(output_file),
                'steps': len(schema.steps)
            })
            print(f"✓ Exported: {pyfile.name} ({len(schema.steps)} steps)")
        except Exception as e:
            print(f"✗ Failed: {pyfile.name} - {e}")

    return exported


def print_analysis(filepath: str):
    """Print detailed analysis of a presentation file"""
    analysis = analyze_presentation_file(filepath)

    print(f"\n{'='*60}")
    print(f"PRESENTATION ANALYSIS: {Path(filepath).name}")
    print(f"{'='*60}")
    print(f"\nClass: {analysis['class_name']}")
    print(f"Title: {analysis['title']}")
    print(f"Steps: {analysis['total_steps']}")
    print(f"\nStep Names:")
    for i, name in enumerate(analysis['step_names']):
        print(f"  {i}: {name}")

    print(f"\nMethods with text content:")
    for method, strings in sorted(analysis['methods'].items()):
        if strings and 'draw' in method.lower():
            print(f"\n  {method}():")
            for s in strings[:5]:  # First 5 strings
                preview = s[:60].replace('\n', '\\n')
                print(f"    - \"{preview}...\"" if len(s) > 60 else f"    - \"{preview}\"")
            if len(strings) > 5:
                print(f"    ... and {len(strings) - 5} more strings")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Export presentations to JSON")
    parser.add_argument('action', choices=['analyze', 'export', 'export-all'],
                        help="Action to perform")
    parser.add_argument('path', nargs='?', help="File or directory path")
    parser.add_argument('-o', '--output', help="Output path")

    args = parser.parse_args()

    # Default paths
    pres_dir = Path(__file__).parent.parent / 'presentations'
    out_dir = Path(__file__).parent.parent / 'schemas'

    if args.action == 'analyze':
        if args.path:
            print_analysis(args.path)
        else:
            # Analyze all
            for f in pres_dir.glob('*_presentation*.py'):
                print_analysis(str(f))

    elif args.action == 'export':
        if not args.path:
            print("Error: path required for export")
            sys.exit(1)
        output = args.output or str(out_dir / f"{Path(args.path).stem}.json")
        export_presentation(args.path, output)

    elif args.action == 'export-all':
        export_all_presentations(str(pres_dir), str(out_dir))
