"""
Presentation Schema Definition
JSON schema for designing matplotlib-based presentations

Element Categories (sorted logically):
1. BASIC TEXT - text, typewriter_text, code_block, code_execution
2. CONTAINERS - box, comparison, conversation
3. LISTS - bullet_list, checklist, timeline
4. LAYOUT - flow, grid, stacked_boxes
5. CONNECTORS - arrow, arc_arrow, particle_flow
6. VISUALIZATIONS - neural_network, attention_heatmap, token_flow
7. METRICS - similarity_meter, progress_bar, weight_comparison, parameter_slider
8. 3D ELEMENTS - scatter_3d, vector_3d
9. COMPARISON - model_comparison
"""

from dataclasses import dataclass, field, asdict
from typing import List, Optional, Dict, Any, Literal, Tuple
from enum import Enum
import json


class AnimationPhase(str, Enum):
    """When element appears during step animation"""
    IMMEDIATE = "immediate"  # 0-20%
    EARLY = "early"          # 20-40%
    MIDDLE = "middle"        # 40-60%
    LATE = "late"            # 60-80%
    FINAL = "final"          # 80-100%


class EasingFunction(str, Enum):
    """Easing functions for smooth animations"""
    LINEAR = "linear"
    EASE_IN = "ease_in"
    EASE_OUT = "ease_out"
    EASE_IN_OUT = "ease_in_out"
    EASE_IN_CUBIC = "ease_in_cubic"
    EASE_OUT_CUBIC = "ease_out_cubic"
    ELASTIC_OUT = "elastic_out"
    BOUNCE_OUT = "bounce_out"


class ContinuousEffect(str, Enum):
    """Continuous animation effects"""
    NONE = "none"
    PULSE = "pulse"
    BREATHING = "breathing"


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
class Point3D:
    """3D point with optional label and color"""
    x: float
    y: float
    z: float
    label: Optional[str] = None
    color: Optional[str] = None


@dataclass
class AnimationTiming:
    """Custom animation timing override"""
    start_percent: float  # 0-100
    end_percent: float    # 0-100
    easing: EasingFunction = EasingFunction.EASE_IN_OUT


@dataclass
class TextStyle:
    """Text styling options"""
    fontsize: Optional[int] = None
    fontweight: Literal["normal", "bold"] = "normal"
    fontstyle: Literal["normal", "italic"] = "normal"
    color: Optional[str] = None
    alpha: float = 1.0
    ha: HAlign = HAlign.CENTER
    va: VAlign = VAlign.CENTER


@dataclass
class BoxStyle:
    """Box/container styling"""
    fill_color: Optional[str] = None
    border_color: Optional[str] = None
    border_width: float = 3.0
    corner_radius: float = 2.0
    alpha: float = 0.95


# ============================================================================
# CATEGORY 1: BASIC TEXT ELEMENTS
# ============================================================================

@dataclass
class TextElement:
    """Simple text element"""
    type: Literal["text"] = "text"
    content: str = ""
    position: Position = field(default_factory=lambda: Position(50, 50))
    style: TextStyle = field(default_factory=TextStyle)
    animation_phase: AnimationPhase = AnimationPhase.IMMEDIATE
    preset: Optional[Literal["title", "subtitle", "body", "caption", "footer"]] = None
    easing: EasingFunction = EasingFunction.EASE_IN_OUT
    continuous_effect: ContinuousEffect = ContinuousEffect.NONE
    effect_frequency: float = 1.0


@dataclass
class TypewriterTextElement:
    """Text with character-by-character reveal and cursor"""
    type: Literal["typewriter_text"] = "typewriter_text"
    content: str = ""
    position: Position = field(default_factory=lambda: Position(50, 50))
    style: TextStyle = field(default_factory=TextStyle)
    animation_phase: AnimationPhase = AnimationPhase.EARLY
    show_cursor: bool = True
    cursor_char: str = "|"
    cursor_blink_rate: float = 2.0
    easing: EasingFunction = EasingFunction.LINEAR
    continuous_effect: ContinuousEffect = ContinuousEffect.NONE
    effect_frequency: float = 1.0


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
class CodeExecutionElement:
    """Code block with execution output shown below"""
    type: Literal["code_execution"] = "code_execution"
    position: Position = field(default_factory=lambda: Position(50, 50))
    code: str = ""
    output: str = ""
    language: str = "python"
    width: float = 70.0
    code_height: float = 20.0
    output_height: float = 12.0
    show_arrow: bool = True  # Arrow between code and output
    animation_phase: AnimationPhase = AnimationPhase.EARLY
    stagger: bool = True  # Code first, then output


# ============================================================================
# CATEGORY 2: CONTAINERS
# ============================================================================

@dataclass
class BoxElement:
    """Box/container with optional content"""
    type: Literal["box"] = "box"
    position: Position = field(default_factory=lambda: Position(50, 50))
    width: float = 60.0
    height: float = 20.0
    style: BoxStyle = field(default_factory=BoxStyle)
    animation_phase: AnimationPhase = AnimationPhase.IMMEDIATE
    title: Optional[str] = None
    title_style: Optional[TextStyle] = None
    content: Optional[str] = None
    content_style: Optional[TextStyle] = None
    icon: Optional[str] = None


@dataclass
class ComparisonElement:
    """Side-by-side comparison (good/bad, before/after)"""
    type: Literal["comparison"] = "comparison"
    position: Position = field(default_factory=lambda: Position(50, 50))
    left_title: str = "Before"
    left_content: str = ""
    left_color: str = "warning"
    right_title: str = "After"
    right_content: str = ""
    right_color: str = "success"
    width: float = 80.0
    height: float = 30.0
    animation_phase: AnimationPhase = AnimationPhase.EARLY


@dataclass
class ConversationElement:
    """Chat-style conversation bubbles"""
    type: Literal["conversation"] = "conversation"
    position: Position = field(default_factory=lambda: Position(50, 50))
    messages: List[Dict[str, Any]] = field(default_factory=list)
    # Each message: {"role": "user"|"assistant"|"system", "content": "...", "name": "User"}
    width: float = 70.0
    bubble_spacing: float = 4.0
    user_color: str = "primary"
    assistant_color: str = "secondary"
    system_color: str = "dim"
    animation_phase: AnimationPhase = AnimationPhase.EARLY
    stagger: bool = True


# ============================================================================
# CATEGORY 3: LISTS
# ============================================================================

@dataclass
class BulletListElement:
    """Bulleted list with sequential reveal"""
    type: Literal["bullet_list"] = "bullet_list"
    position: Position = field(default_factory=lambda: Position(50, 50))
    items: List[str] = field(default_factory=list)
    item_style: TextStyle = field(default_factory=TextStyle)
    bullet_char: str = "*"
    spacing: float = 6.0
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
class TimelineElement:
    """Horizontal or vertical timeline with milestones"""
    type: Literal["timeline"] = "timeline"
    position: Position = field(default_factory=lambda: Position(50, 50))
    events: List[Dict[str, Any]] = field(default_factory=list)
    # Each event: {"date": "2023", "title": "GPT-4", "description": "...", "color": "primary"}
    orientation: Literal["horizontal", "vertical"] = "horizontal"
    width: float = 80.0
    height: float = 25.0
    line_color: str = "dim"
    animation_phase: AnimationPhase = AnimationPhase.EARLY
    stagger: bool = True


# ============================================================================
# CATEGORY 4: LAYOUT ELEMENTS
# ============================================================================

@dataclass
class FlowElement:
    """Horizontal process flow with steps"""
    type: Literal["flow"] = "flow"
    position: Position = field(default_factory=lambda: Position(50, 50))
    steps: List[Dict[str, str]] = field(default_factory=list)
    colors: Optional[List[str]] = None
    width: float = 80.0
    animation_phase: AnimationPhase = AnimationPhase.EARLY
    stagger: bool = True


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
    animation_phase: AnimationPhase = AnimationPhase.EARLY
    stagger: bool = True


@dataclass
class StackedBoxesElement:
    """Vertically stacked boxes with pyramid-like layout"""
    type: Literal["stacked_boxes"] = "stacked_boxes"
    position: Position = field(default_factory=lambda: Position(50, 50))
    items: List[Dict[str, str]] = field(default_factory=list)
    base_width: float = 70.0
    box_height: float = 12.0
    width_decrease: float = 4.0
    spacing: float = 15.0
    animation_phase: AnimationPhase = AnimationPhase.EARLY
    stagger: bool = True


# ============================================================================
# CATEGORY 5: CONNECTORS
# ============================================================================

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
class ArcArrowElement:
    """Curved arrow following parabolic path"""
    type: Literal["arc_arrow"] = "arc_arrow"
    start: Position = field(default_factory=lambda: Position(30, 50))
    end: Position = field(default_factory=lambda: Position(70, 50))
    arc_height: float = 15.0
    direction: Literal["up", "down"] = "up"
    color: str = "primary"
    width: float = 2.0
    animation_phase: AnimationPhase = AnimationPhase.MIDDLE
    custom_timing: Optional[AnimationTiming] = None


@dataclass
class ParticleFlowElement:
    """Animated particles flowing between two points"""
    type: Literal["particle_flow"] = "particle_flow"
    start: Position = field(default_factory=lambda: Position(15, 50))
    end: Position = field(default_factory=lambda: Position(85, 50))
    num_particles: int = 30
    color: str = "accent"
    particle_size: float = 30.0
    spread: float = 0.5
    animation_phase: AnimationPhase = AnimationPhase.MIDDLE
    easing: EasingFunction = EasingFunction.EASE_IN_OUT


# ============================================================================
# CATEGORY 6: AI VISUALIZATIONS
# ============================================================================

@dataclass
class NeuralNetworkElement:
    """Pre-built neural network diagram"""
    type: Literal["neural_network"] = "neural_network"
    position: Position = field(default_factory=lambda: Position(50, 50))
    layers: List[int] = field(default_factory=lambda: [3, 5, 5, 2])
    layer_labels: Optional[List[str]] = None
    width: float = 70.0
    height: float = 50.0
    node_color: str = "primary"
    connection_color: str = "dim"
    active_color: str = "accent"
    animation_phase: AnimationPhase = AnimationPhase.EARLY
    stagger: bool = True
    show_connections: bool = True


@dataclass
class AttentionHeatmapElement:
    """Attention weights visualization as heatmap grid"""
    type: Literal["attention_heatmap"] = "attention_heatmap"
    position: Position = field(default_factory=lambda: Position(50, 50))
    tokens_x: List[str] = field(default_factory=lambda: ["The", "cat", "sat"])
    tokens_y: List[str] = field(default_factory=lambda: ["The", "cat", "sat"])
    weights: Optional[List[List[float]]] = None  # 2D matrix, auto-generated if None
    width: float = 50.0
    height: float = 50.0
    colormap: str = "viridis"  # matplotlib colormap
    show_values: bool = True
    title: str = "Attention Weights"
    animation_phase: AnimationPhase = AnimationPhase.EARLY
    stagger: bool = True  # Reveal row by row


@dataclass
class TokenFlowElement:
    """Tokenization pipeline visualization: text -> tokens -> embeddings"""
    type: Literal["token_flow"] = "token_flow"
    position: Position = field(default_factory=lambda: Position(50, 50))
    input_text: str = "Hello world"
    tokens: Optional[List[str]] = None  # Auto-split if None
    token_ids: Optional[List[int]] = None  # Auto-generate if None
    show_embeddings: bool = True
    embedding_dims_shown: int = 4  # How many embedding values to show
    width: float = 80.0
    height: float = 40.0
    animation_phase: AnimationPhase = AnimationPhase.EARLY
    stagger: bool = True


@dataclass
class ModelComparisonElement:
    """Side-by-side model architecture or capability comparison"""
    type: Literal["model_comparison"] = "model_comparison"
    position: Position = field(default_factory=lambda: Position(50, 50))
    models: List[Dict[str, Any]] = field(default_factory=list)
    # Each model: {"name": "GPT-4", "params": "1.7T", "context": "128K", "features": [...], "color": "primary"}
    comparison_rows: List[str] = field(default_factory=list)
    # Row labels: ["Parameters", "Context Window", "Multimodal", ...]
    width: float = 85.0
    height: float = 50.0
    animation_phase: AnimationPhase = AnimationPhase.EARLY
    stagger: bool = True


# ============================================================================
# CATEGORY 7: METRICS & INDICATORS
# ============================================================================

@dataclass
class SimilarityMeterElement:
    """Gauge widget showing 0-100% score"""
    type: Literal["similarity_meter"] = "similarity_meter"
    position: Position = field(default_factory=lambda: Position(50, 50))
    score: float = 75.0
    radius: float = 8.0
    label: str = "Similarity"
    animation_phase: AnimationPhase = AnimationPhase.MIDDLE
    low_color: str = "warning"
    medium_color: str = "accent"
    high_color: str = "success"


@dataclass
class ProgressBarElement:
    """Visual progress indicator"""
    type: Literal["progress_bar"] = "progress_bar"
    position: Position = field(default_factory=lambda: Position(50, 50))
    current: int = 5
    total: int = 10
    width: float = 30.0
    height: float = 3.0
    label: str = "Progress"
    color: str = "success"
    animation_phase: AnimationPhase = AnimationPhase.MIDDLE


@dataclass
class WeightComparisonElement:
    """Before/after weight bars with delta arrows"""
    type: Literal["weight_comparison"] = "weight_comparison"
    position: Position = field(default_factory=lambda: Position(50, 50))
    before_weights: List[float] = field(default_factory=lambda: [0.5, 0.3, 0.8])
    after_weights: List[float] = field(default_factory=lambda: [0.7, 0.5, 0.6])
    labels: Optional[List[str]] = None
    bar_height: float = 20.0
    animation_phase: AnimationPhase = AnimationPhase.MIDDLE


@dataclass
class ParameterSliderElement:
    """Interactive-looking parameter slider (static representation)"""
    type: Literal["parameter_slider"] = "parameter_slider"
    position: Position = field(default_factory=lambda: Position(50, 50))
    label: str = "Temperature"
    min_value: float = 0.0
    max_value: float = 2.0
    current_value: float = 0.7
    width: float = 40.0
    description: str = ""  # Optional description of what parameter does
    effect_preview: Optional[str] = None  # Text showing effect at current value
    color: str = "accent"
    animation_phase: AnimationPhase = AnimationPhase.MIDDLE


# ============================================================================
# CATEGORY 8: 3D ELEMENTS
# ============================================================================

@dataclass
class Scatter3DElement:
    """3D scatter plot with labels and camera control"""
    type: Literal["scatter_3d"] = "scatter_3d"
    points: List[Dict[str, Any]] = field(default_factory=list)
    xlim: tuple = (-5, 5)
    ylim: tuple = (-5, 5)
    zlim: tuple = (-5, 5)
    camera_elev: float = 20.0
    camera_azim: float = 45.0
    rotate_camera: bool = False
    camera_rotation_speed: float = 90.0
    stagger_points: bool = True
    animation_phase: AnimationPhase = AnimationPhase.EARLY
    show_vectors: bool = True


@dataclass
class Vector3DElement:
    """3D vectors from origin with labels"""
    type: Literal["vector_3d"] = "vector_3d"
    vectors: List[Dict[str, Any]] = field(default_factory=list)
    xlim: tuple = (-5, 5)
    ylim: tuple = (-5, 5)
    zlim: tuple = (-5, 5)
    camera_elev: float = 20.0
    camera_azim: float = 45.0
    rotate_camera: bool = False
    camera_rotation_speed: float = 90.0
    animation_phase: AnimationPhase = AnimationPhase.EARLY
    stagger: bool = True


# ============================================================================
# Element Type Enum and Category Mapping
# ============================================================================

class ElementType(str, Enum):
    """Types of visual elements (categorized)"""
    # Basic Text
    TEXT = "text"
    TYPEWRITER_TEXT = "typewriter_text"
    CODE_BLOCK = "code_block"
    CODE_EXECUTION = "code_execution"
    # Containers
    BOX = "box"
    COMPARISON = "comparison"
    CONVERSATION = "conversation"
    # Lists
    BULLET_LIST = "bullet_list"
    CHECKLIST = "checklist"
    TIMELINE = "timeline"
    # Layout
    FLOW = "flow"
    GRID = "grid"
    STACKED_BOXES = "stacked_boxes"
    # Connectors
    ARROW = "arrow"
    ARC_ARROW = "arc_arrow"
    PARTICLE_FLOW = "particle_flow"
    # AI Visualizations
    NEURAL_NETWORK = "neural_network"
    ATTENTION_HEATMAP = "attention_heatmap"
    TOKEN_FLOW = "token_flow"
    MODEL_COMPARISON = "model_comparison"
    # Metrics
    SIMILARITY_METER = "similarity_meter"
    PROGRESS_BAR = "progress_bar"
    WEIGHT_COMPARISON = "weight_comparison"
    PARAMETER_SLIDER = "parameter_slider"
    # 3D
    SCATTER_3D = "scatter_3d"
    VECTOR_3D = "vector_3d"


# Category definitions for UI organization
ELEMENT_CATEGORIES = {
    "Basic Text": ["text", "typewriter_text", "code_block", "code_execution"],
    "Containers": ["box", "comparison", "conversation"],
    "Lists": ["bullet_list", "checklist", "timeline"],
    "Layout": ["flow", "grid", "stacked_boxes"],
    "Connectors": ["arrow", "arc_arrow", "particle_flow"],
    "AI Visuals": ["neural_network", "attention_heatmap", "token_flow", "model_comparison"],
    "Metrics": ["similarity_meter", "progress_bar", "weight_comparison", "parameter_slider"],
    "3D": ["scatter_3d", "vector_3d"],
}

# Flat sorted list for designer
SORTED_ELEMENTS = [
    # Basic Text (most common first)
    ("text", "Text", "Aa"),
    ("typewriter_text", "Typewriter", "Ty|"),
    ("code_block", "Code", "</>"),
    ("code_execution", "Code+Out", ">>>"),
    # Containers
    ("box", "Box", "[ ]"),
    ("comparison", "Compare", "<>"),
    ("conversation", "Chat", "..."),
    # Lists
    ("bullet_list", "Bullets", "* *"),
    ("checklist", "Checklist", "[x]"),
    ("timeline", "Timeline", "o-o"),
    # Layout
    ("flow", "Flow", ">>>"),
    ("grid", "Grid", "##"),
    ("stacked_boxes", "Stack", "="),
    # Connectors
    ("arrow", "Arrow", "->"),
    ("arc_arrow", "Arc", "~>"),
    ("particle_flow", "Particles", "***"),
    # AI Visualizations
    ("neural_network", "Neural Net", "ooo"),
    ("attention_heatmap", "Attention", "HM"),
    ("token_flow", "Tokens", "T>E"),
    ("model_comparison", "Models", "A|B"),
    # Metrics
    ("similarity_meter", "Meter", "%"),
    ("progress_bar", "Progress", "[=]"),
    ("weight_comparison", "Weights", "W"),
    ("parameter_slider", "Slider", "-o-"),
    # 3D
    ("scatter_3d", "3D Scatter", "3D"),
    ("vector_3d", "3D Vector", "v3"),
]


# Union type for all elements
Element = (TextElement | TypewriterTextElement | BoxElement | BulletListElement |
           ArrowElement | ArcArrowElement | ComparisonElement | FlowElement |
           CodeBlockElement | CodeExecutionElement | GridElement | ChecklistElement |
           StackedBoxesElement | ConversationElement | TimelineElement |
           ParticleFlowElement | SimilarityMeterElement | ProgressBarElement |
           WeightComparisonElement | ParameterSliderElement |
           Scatter3DElement | Vector3DElement | NeuralNetworkElement |
           AttentionHeatmapElement | TokenFlowElement | ModelComparisonElement)


@dataclass
class Step:
    """A single presentation step/slide"""
    name: str
    title: Optional[str] = None
    subtitle: Optional[str] = None
    elements: List[Dict[str, Any]] = field(default_factory=list)
    animation_frames: int = 60
    notes: Optional[str] = None


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
    name: str
    title: str
    description: Optional[str] = None
    author: Optional[str] = None
    language: str = "nl"
    version: str = "1.0"
    landing: LandingPage = field(default_factory=LandingPage)
    steps: List[Step] = field(default_factory=list)
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


# Example schema
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
    ),
    steps=[
        Step(
            name="Introductie",
            title="Wat Gaan We Leren?",
            elements=[
                {
                    "type": "bullet_list",
                    "position": {"x": 50, "y": 55},
                    "items": ["Onderwerp 1", "Onderwerp 2", "Onderwerp 3"],
                    "animation_phase": "early",
                    "stagger": True
                }
            ],
            animation_frames=60,
        ),
    ]
)


def get_example_json() -> str:
    """Get example JSON for reference"""
    return EXAMPLE_SCHEMA.to_json()


if __name__ == "__main__":
    print("=== Presentation Schema ===\n")
    print(f"Total element types: {len(SORTED_ELEMENTS)}")
    print("\nCategories:")
    for cat, elems in ELEMENT_CATEGORIES.items():
        print(f"  {cat}: {', '.join(elems)}")
