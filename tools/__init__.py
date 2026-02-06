"""
Presentation Designer Tools
Tools for designing, exporting, and generating matplotlib presentations
"""

from tools.schema import (
    PresentationSchema,
    Step,
    LandingPage,
    TextElement,
    BoxElement,
    BulletListElement,
    ArrowElement,
    ComparisonElement,
    FlowElement,
    CodeBlockElement,
    GridElement,
    ChecklistElement,
    StackedBoxesElement,
    Position,
    TextStyle,
    BoxStyle,
    AnimationPhase,
    get_example_json
)

from tools.generator import (
    PresentationGenerator,
    generate_from_json
)

from tools.exporter import (
    analyze_presentation_file,
    export_presentation,
    export_all_presentations,
    print_analysis
)

__all__ = [
    # Schema classes
    'PresentationSchema',
    'Step',
    'LandingPage',
    'TextElement',
    'BoxElement',
    'BulletListElement',
    'ArrowElement',
    'ComparisonElement',
    'FlowElement',
    'CodeBlockElement',
    'GridElement',
    'ChecklistElement',
    'StackedBoxesElement',
    'Position',
    'TextStyle',
    'BoxStyle',
    'AnimationPhase',
    'get_example_json',

    # Generator
    'PresentationGenerator',
    'generate_from_json',

    # Exporter
    'analyze_presentation_file',
    'export_presentation',
    'export_all_presentations',
    'print_analysis',
]
