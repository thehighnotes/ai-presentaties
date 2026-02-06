"""
Presentation Schema Definition
JSON schema for designing matplotlib-based presentations
"""

from dataclasses import dataclass, field, asdict
from typing import List, Optional, Dict, Any, Literal
from enum import Enum
import json


class ElementType(str, Enum):
    """Types of visual elements"""
    TEXT = "text"
    BOX = "box"
    ARROW = "arrow"
    ICON = "icon"
    DIVIDER = "divider"
    BULLET_LIST = "bullet_list"
    CODE_BLOCK = "code_block"
    COMPARISON = "comparison"  # Before/after, good/bad
    FLOW = "flow"  # Left-to-right process flow
    GRID = "grid"  # 2D grid of cards
    CHECKLIST = "checklist"  # List with checkmarks
    STACKED_BOXES = "stacked_boxes"  # Vertically stacked boxes


class AnimationPhase(str, Enum):
    """When element appears during step animation"""
    IMMEDIATE = "immediate"  # 0-20%
    EARLY = "early"          # 20-40%
    MIDDLE = "middle"        # 40-60%
    LATE = "late"            # 60-80%
    FINAL = "final"          # 80-100%


class HAlign(str, Enum):
    LEFT = "left"
    CENTER = "center"
    RIGHT = "right"


class VAlign(str, Enum):
    TOP = "top"
    CENTER = "center"
    BOTTOM = "bottom"


@dataclass
class Position:
    """Position in 0-100 coordinate space"""
    x: float
    y: float


@dataclass
class TextStyle:
    """Text styling options"""
    fontsize: Optional[int] = None  # None = use default for type
    fontweight: Literal["normal", "bold"] = "normal"
    fontstyle: Literal["normal", "italic"] = "normal"
    color: Optional[str] = None  # Color name from palette or hex
    alpha: float = 1.0
    ha: HAlign = HAlign.CENTER
    va: VAlign = VAlign.CENTER


@dataclass
class BoxStyle:
    """Box/container styling"""
    fill_color: Optional[str] = None  # bg_light default
    border_color: Optional[str] = None  # primary default
    border_width: float = 3.0
    corner_radius: float = 2.0
    alpha: float = 0.95


@dataclass
class TextElement:
    """Simple text element"""
    type: Literal["text"] = "text"
    content: str = ""
    position: Position = field(default_factory=lambda: Position(50, 50))
    style: TextStyle = field(default_factory=TextStyle)
    animation_phase: AnimationPhase = AnimationPhase.IMMEDIATE

    # Convenience for title/subtitle presets
    preset: Optional[Literal["title", "subtitle", "body", "caption", "footer"]] = None


@dataclass
class BoxElement:
    """Box/container with optional content"""
    type: Literal["box"] = "box"
    position: Position = field(default_factory=lambda: Position(50, 50))
    width: float = 60.0
    height: float = 20.0
    style: BoxStyle = field(default_factory=BoxStyle)
    animation_phase: AnimationPhase = AnimationPhase.IMMEDIATE

    # Content inside the box
    title: Optional[str] = None
    title_style: Optional[TextStyle] = None
    content: Optional[str] = None
    content_style: Optional[TextStyle] = None
    icon: Optional[str] = None  # Emoji or icon placeholder


@dataclass
class BulletListElement:
    """Bulleted list with sequential reveal"""
    type: Literal["bullet_list"] = "bullet_list"
    position: Position = field(default_factory=lambda: Position(50, 50))
    items: List[str] = field(default_factory=list)
    item_style: TextStyle = field(default_factory=TextStyle)
    bullet_char: str = "•"
    spacing: float = 6.0  # Vertical spacing between items
    animation_phase: AnimationPhase = AnimationPhase.EARLY
    stagger: bool = True  # Reveal items one by one


@dataclass
class ArrowElement:
    """Arrow between two points"""
    type: Literal["arrow"] = "arrow"
    start: Position = field(default_factory=lambda: Position(30, 50))
    end: Position = field(default_factory=lambda: Position(70, 50))
    color: Optional[str] = None
    width: float = 2.0
    head_size: float = 15.0
    style: Literal["simple", "fancy", "curved"] = "simple"
    animation_phase: AnimationPhase = AnimationPhase.MIDDLE


@dataclass
class ComparisonElement:
    """Side-by-side comparison (good/bad, before/after)"""
    type: Literal["comparison"] = "comparison"
    position: Position = field(default_factory=lambda: Position(50, 50))

    left_title: str = "Before"
    left_content: str = ""
    left_color: str = "warning"  # Red/warning for "bad"

    right_title: str = "After"
    right_content: str = ""
    right_color: str = "success"  # Green/success for "good"

    width: float = 80.0
    height: float = 30.0
    animation_phase: AnimationPhase = AnimationPhase.EARLY


@dataclass
class FlowElement:
    """Horizontal process flow with steps"""
    type: Literal["flow"] = "flow"
    position: Position = field(default_factory=lambda: Position(50, 50))

    steps: List[Dict[str, str]] = field(default_factory=list)
    # Each step: {"icon": "📚", "title": "Input", "subtitle": "Data source"}

    colors: Optional[List[str]] = None  # Per-step colors, or None for auto
    width: float = 80.0
    animation_phase: AnimationPhase = AnimationPhase.EARLY
    stagger: bool = True


@dataclass
class CodeBlockElement:
    """Syntax-highlighted code block"""
    type: Literal["code_block"] = "code_block"
    position: Position = field(default_factory=lambda: Position(50, 50))
    code: str = ""
    language: str = "python"
    width: float = 60.0
    height: float = 25.0
    animation_phase: AnimationPhase = AnimationPhase.MIDDLE


@dataclass
class GridElement:
    """2D grid of cards/items"""
    type: Literal["grid"] = "grid"
    position: Position = field(default_factory=lambda: Position(50, 50))

    columns: int = 2
    rows: int = 2
    cell_width: float = 30.0
    cell_height: float = 18.0

    items: List[Dict[str, str]] = field(default_factory=list)
    # Each item: {"icon": "👨‍🏫", "title": "Expert", "description": "Details", "color": "primary"}

    animation_phase: AnimationPhase = AnimationPhase.EARLY
    stagger: bool = True


@dataclass
class ChecklistElement:
    """List with checkmarks"""
    type: Literal["checklist"] = "checklist"
    position: Position = field(default_factory=lambda: Position(50, 50))

    items: List[str] = field(default_factory=list)
    check_color: str = "secondary"
    text_color: str = "text"
    spacing: float = 6.5
    fontsize: int = 18

    animation_phase: AnimationPhase = AnimationPhase.EARLY
    stagger: bool = True


@dataclass
class StackedBoxesElement:
    """Vertically stacked boxes with pyramid-like layout"""
    type: Literal["stacked_boxes"] = "stacked_boxes"
    position: Position = field(default_factory=lambda: Position(50, 50))

    items: List[Dict[str, str]] = field(default_factory=list)
    # Each item: {"title": "Context", "description": "Background info", "color": "accent"}

    base_width: float = 70.0
    box_height: float = 12.0
    width_decrease: float = 4.0  # Each box gets narrower
    spacing: float = 15.0  # Vertical spacing between boxes

    animation_phase: AnimationPhase = AnimationPhase.EARLY
    stagger: bool = True


# Union type for all elements
Element = (TextElement | BoxElement | BulletListElement | ArrowElement |
           ComparisonElement | FlowElement | CodeBlockElement |
           GridElement | ChecklistElement | StackedBoxesElement)


@dataclass
class Step:
    """A single presentation step/slide"""
    name: str
    title: Optional[str] = None
    subtitle: Optional[str] = None
    elements: List[Dict[str, Any]] = field(default_factory=list)  # Serialized elements
    animation_frames: int = 60  # 60=short, 90=medium, 120=long
    notes: Optional[str] = None  # Speaker notes


@dataclass
class LandingPage:
    """Landing page configuration"""
    title: str = "Presentatie"
    subtitle: Optional[str] = None
    tagline: Optional[str] = None
    welcome_message: Optional[str] = None
    footer: Optional[str] = None
    primary_color: str = "primary"
    icon_left: Optional[str] = None
    icon_right: Optional[str] = None


@dataclass
class PresentationSchema:
    """Complete presentation definition"""
    # Metadata
    name: str
    title: str
    description: Optional[str] = None
    author: Optional[str] = None
    language: str = "nl"  # nl, en
    version: str = "1.0"

    # Landing page
    landing: LandingPage = field(default_factory=LandingPage)

    # Steps (excluding landing which is step -1)
    steps: List[Step] = field(default_factory=list)

    # Styling overrides
    color_overrides: Dict[str, str] = field(default_factory=dict)

    def to_json(self, indent: int = 2) -> str:
        """Serialize to JSON string"""
        return json.dumps(asdict(self), indent=indent, ensure_ascii=False)

    def to_file(self, path: str):
        """Save to JSON file"""
        with open(path, 'w', encoding='utf-8') as f:
            f.write(self.to_json())

    @classmethod
    def from_json(cls, json_str: str) -> 'PresentationSchema':
        """Deserialize from JSON string"""
        data = json.loads(json_str)

        # Reconstruct nested dataclasses
        if 'landing' in data:
            data['landing'] = LandingPage(**data['landing'])

        if 'steps' in data:
            data['steps'] = [Step(**s) for s in data['steps']]

        return cls(**data)

    @classmethod
    def from_file(cls, path: str) -> 'PresentationSchema':
        """Load from JSON file"""
        with open(path, 'r', encoding='utf-8') as f:
            return cls.from_json(f.read())


# Example schema for reference
EXAMPLE_SCHEMA = PresentationSchema(
    name="example_presentation",
    title="Voorbeeld Presentatie",
    description="Een voorbeeldpresentatie om de structuur te demonstreren",
    author="Designer",
    language="nl",
    landing=LandingPage(
        title="Voorbeeld Presentatie",
        subtitle="Een Introductie",
        tagline="Van concept naar uitvoering",
        welcome_message="Welkom! We gaan samen leren.",
        footer="Druk op SPATIE om te beginnen",
        primary_color="primary",
        icon_left="[doc]",
        icon_right="[AI]"
    ),
    steps=[
        Step(
            name="Introductie",
            title="Wat Gaan We Leren?",
            subtitle="Een overzicht van de onderwerpen",
            elements=[
                {
                    "type": "bullet_list",
                    "position": {"x": 50, "y": 55},
                    "items": [
                        "Onderwerp 1: De basis",
                        "Onderwerp 2: Verdieping",
                        "Onderwerp 3: Praktijk"
                    ],
                    "animation_phase": "early",
                    "stagger": True
                }
            ],
            animation_frames=60,
            notes="Start met een overzicht om verwachtingen te scheppen"
        ),
        Step(
            name="Hoofdconcept",
            title="Het Hoofdconcept",
            elements=[
                {
                    "type": "comparison",
                    "position": {"x": 50, "y": 50},
                    "left_title": "Zonder",
                    "left_content": "Verwarrend en chaotisch",
                    "left_color": "warning",
                    "right_title": "Met",
                    "right_content": "Duidelijk en gestructureerd",
                    "right_color": "success",
                    "animation_phase": "early"
                }
            ],
            animation_frames=90
        )
    ]
)


def get_example_json() -> str:
    """Get example JSON for reference"""
    return EXAMPLE_SCHEMA.to_json()


if __name__ == "__main__":
    # Print example schema
    print("=== Presentation Schema Example ===\n")
    print(get_example_json())
