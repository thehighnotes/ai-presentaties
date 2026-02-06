#!/usr/bin/env python3
"""
Presentation Designer CLI
Main tool for designing matplotlib-based presentations

Usage:
    python -m tools.designer new <name>           Create new presentation JSON
    python -m tools.designer generate <json>      Generate Python from JSON
    python -m tools.designer analyze <py>         Analyze existing presentation
    python -m tools.designer export <py>          Export presentation to JSON
    python -m tools.designer validate <json>      Validate JSON schema
    python -m tools.designer example              Show example JSON
"""

import argparse
import json
import sys
from pathlib import Path

# Add parent to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from tools.schema import (
    PresentationSchema, Step, LandingPage,
    get_example_json
)
from tools.generator import PresentationGenerator, generate_from_json
from tools.exporter import (
    analyze_presentation_file, export_presentation,
    export_all_presentations, print_analysis
)


def cmd_new(args):
    """Create a new presentation JSON template"""
    name = args.name.replace(' ', '_').lower()

    # Create schema with template content
    schema = PresentationSchema(
        name=name,
        title=args.title or name.replace('_', ' ').title(),
        description=f"Auto-generated presentation: {name}",
        author=args.author or "Designer",
        language="nl",
        landing=LandingPage(
            title=args.title or name.replace('_', ' ').title(),
            subtitle="Ondertitel hier",
            tagline="Korte beschrijving van het onderwerp",
            footer="Druk op SPATIE om te beginnen",
            primary_color="primary"
        ),
        steps=[
            Step(
                name="Introductie",
                title="Introductie",
                subtitle="Wat gaan we behandelen?",
                elements=[
                    {
                        "type": "bullet_list",
                        "position": {"x": 50, "y": 60},
                        "items": [
                            "Eerste onderwerp",
                            "Tweede onderwerp",
                            "Derde onderwerp"
                        ],
                        "animation_phase": "early",
                        "stagger": True
                    }
                ],
                animation_frames=60,
                notes="Start met een overzicht"
            ),
            Step(
                name="Hoofdconcept",
                title="Het Hoofdconcept",
                elements=[
                    {
                        "type": "box",
                        "position": {"x": 50, "y": 55},
                        "width": 70,
                        "height": 25,
                        "title": "Belangrijk Concept",
                        "content": "Uitleg van het concept komt hier",
                        "style": {"border_color": "primary"},
                        "animation_phase": "early"
                    }
                ],
                animation_frames=60
            ),
            Step(
                name="Vergelijking",
                title="Voor en Na",
                elements=[
                    {
                        "type": "comparison",
                        "position": {"x": 50, "y": 50},
                        "left_title": "Zonder",
                        "left_content": "Oude situatie",
                        "left_color": "warning",
                        "right_title": "Met",
                        "right_content": "Nieuwe situatie",
                        "right_color": "success",
                        "animation_phase": "early"
                    }
                ],
                animation_frames=90
            ),
            Step(
                name="Samenvatting",
                title="Samenvatting",
                subtitle="Wat hebben we geleerd?",
                elements=[
                    {
                        "type": "bullet_list",
                        "position": {"x": 50, "y": 55},
                        "items": [
                            "Punt 1: Belangrijkste inzicht",
                            "Punt 2: Praktische toepassing",
                            "Punt 3: Volgende stappen"
                        ],
                        "animation_phase": "early",
                        "stagger": True
                    }
                ],
                animation_frames=60,
                notes="Eindig met concrete takeaways"
            )
        ]
    )

    # Determine output path
    output_dir = Path(args.output) if args.output else Path.cwd() / 'schemas'
    output_dir.mkdir(exist_ok=True)
    output_path = output_dir / f"{name}.json"

    schema.to_file(str(output_path))
    print(f"\nCreated new presentation template: {output_path}")
    print(f"\nNext steps:")
    print(f"  1. Edit the JSON file to add your content")
    print(f"  2. Generate Python: python -m tools.designer generate {output_path}")


def cmd_generate(args):
    """Generate Python presentation from JSON"""
    json_path = Path(args.json_file)

    if not json_path.exists():
        print(f"Error: File not found: {json_path}")
        sys.exit(1)

    # Determine output path
    if args.output:
        output_path = args.output
    else:
        output_dir = Path(__file__).parent.parent / 'presentations'
        output_path = str(output_dir / f"{json_path.stem}_presentation.py")

    generate_from_json(str(json_path), output_path)
    print(f"\nGenerated: {output_path}")
    print(f"\nTo run: python {output_path}")


def cmd_analyze(args):
    """Analyze an existing presentation file"""
    py_path = Path(args.py_file)

    if not py_path.exists():
        print(f"Error: File not found: {py_path}")
        sys.exit(1)

    print_analysis(str(py_path))


def cmd_export(args):
    """Export existing presentation to JSON"""
    py_path = Path(args.py_file)

    if not py_path.exists():
        print(f"Error: File not found: {py_path}")
        sys.exit(1)

    # Determine output path
    output_dir = Path(__file__).parent.parent / 'schemas'
    output_dir.mkdir(exist_ok=True)

    if args.output:
        output_path = args.output
    else:
        output_path = str(output_dir / f"{py_path.stem}.json")

    export_presentation(str(py_path), output_path)
    print(f"\nNote: The exported JSON is a skeleton. You may need to manually add element details.")


def cmd_validate(args):
    """Validate a JSON schema file"""
    json_path = Path(args.json_file)

    if not json_path.exists():
        print(f"Error: File not found: {json_path}")
        sys.exit(1)

    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Try to parse as schema
        schema = PresentationSchema.from_file(str(json_path))

        print(f"\nValidation: PASSED")
        print(f"\n  Name: {schema.name}")
        print(f"  Title: {schema.title}")
        print(f"  Steps: {len(schema.steps)}")

        # Check for common issues
        warnings = []

        if not schema.landing.title:
            warnings.append("Landing page has no title")

        for i, step in enumerate(schema.steps):
            if not step.name:
                warnings.append(f"Step {i} has no name")
            if not step.elements:
                warnings.append(f"Step '{step.name}' has no elements")

        if warnings:
            print(f"\n  Warnings:")
            for w in warnings:
                print(f"    - {w}")

    except json.JSONDecodeError as e:
        print(f"\nValidation: FAILED - Invalid JSON")
        print(f"  {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\nValidation: FAILED - Schema error")
        print(f"  {e}")
        sys.exit(1)


def cmd_example(args):
    """Show example JSON schema"""
    print("\n=== Example Presentation Schema ===\n")
    print(get_example_json())
    print("\n" + "="*50)
    print("\nElement Types Available:")
    print("  - text: Simple text element")
    print("  - box: Bordered box with optional title/content")
    print("  - bullet_list: List with sequential reveal")
    print("  - comparison: Side-by-side before/after")
    print("  - flow: Horizontal process flow")
    print("  - arrow: Arrow between points")
    print("  - code_block: Syntax-highlighted code")
    print("\nAnimation Phases:")
    print("  - immediate: 0-20% progress")
    print("  - early: 20-40% progress")
    print("  - middle: 40-60% progress")
    print("  - late: 60-80% progress")
    print("  - final: 80-100% progress")
    print("\nColors Available:")
    print("  primary, secondary, accent, highlight")
    print("  success, warning, error")
    print("  text, dim, bg_light")


def cmd_list(args):
    """List all presentations"""
    pres_dir = Path(__file__).parent.parent / 'presentations'
    schemas_dir = Path(__file__).parent.parent / 'schemas'

    print("\n=== Python Presentations ===")
    for f in sorted(pres_dir.glob('*_presentation*.py')):
        if '__pycache__' not in str(f):
            analysis = analyze_presentation_file(str(f))
            print(f"  {f.name}: {analysis['total_steps']} steps - {analysis['title']}")

    if schemas_dir.exists():
        print("\n=== JSON Schemas ===")
        for f in sorted(schemas_dir.glob('*.json')):
            try:
                schema = PresentationSchema.from_file(str(f))
                print(f"  {f.name}: {len(schema.steps)} steps - {schema.title}")
            except:
                print(f"  {f.name}: (invalid)")


def main():
    parser = argparse.ArgumentParser(
        description="Presentation Designer - Create matplotlib presentations from JSON",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s new my_presentation --title "Mijn Presentatie"
  %(prog)s generate schemas/my_presentation.json
  %(prog)s analyze presentations/prompt_engineering_presentation.py
  %(prog)s validate schemas/my_presentation.json
  %(prog)s example
  %(prog)s list
"""
    )

    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # new
    p_new = subparsers.add_parser('new', help='Create new presentation JSON template')
    p_new.add_argument('name', help='Presentation name (used for filename)')
    p_new.add_argument('--title', '-t', help='Presentation title')
    p_new.add_argument('--author', '-a', help='Author name')
    p_new.add_argument('--output', '-o', help='Output directory')
    p_new.set_defaults(func=cmd_new)

    # generate
    p_gen = subparsers.add_parser('generate', help='Generate Python from JSON schema')
    p_gen.add_argument('json_file', help='JSON schema file')
    p_gen.add_argument('--output', '-o', help='Output Python file')
    p_gen.set_defaults(func=cmd_generate)

    # analyze
    p_analyze = subparsers.add_parser('analyze', help='Analyze existing presentation')
    p_analyze.add_argument('py_file', help='Python presentation file')
    p_analyze.set_defaults(func=cmd_analyze)

    # export
    p_export = subparsers.add_parser('export', help='Export presentation to JSON')
    p_export.add_argument('py_file', help='Python presentation file')
    p_export.add_argument('--output', '-o', help='Output JSON file')
    p_export.set_defaults(func=cmd_export)

    # validate
    p_validate = subparsers.add_parser('validate', help='Validate JSON schema')
    p_validate.add_argument('json_file', help='JSON schema file')
    p_validate.set_defaults(func=cmd_validate)

    # example
    p_example = subparsers.add_parser('example', help='Show example JSON schema')
    p_example.set_defaults(func=cmd_example)

    # list
    p_list = subparsers.add_parser('list', help='List all presentations')
    p_list.set_defaults(func=cmd_list)

    args = parser.parse_args()

    if args.command is None:
        parser.print_help()
        sys.exit(1)

    args.func(args)


if __name__ == "__main__":
    main()
