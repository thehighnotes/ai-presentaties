# AI Presentation Suite

A matplotlib-based presentation system with JSON schema design and visual GUI editor.

## Quick Start

```bash
# Qt Designer (recommended GUI)
python -m tools.qt_designer schemas/my_presentation.json

# Or legacy matplotlib designer
python -m tools.visual_designer schemas/my_presentation.json

# Generate Python from JSON (uses centralized rendering)
python -m tools.generator_v2 schemas/my_presentation.json

# Run a presentation
python presentations/my_presentation_presentation.py
```

## Project Structure

```
AI-Presentatie/
├── core/                       # Core framework
│   ├── base.py                # BasePresentation class
│   ├── styling.py             # PresentationStyle colors/fonts
│   ├── animations.py          # AnimationHelper, easing functions
│   ├── element_rendering.py   # Centralized matplotlib rendering (28 types)
│   └── visual_effects.py      # ParticleSystem, SimilarityMeter, etc.
│
├── tools/                      # Design tools
│   ├── schema.py              # JSON schema dataclasses (28 element types)
│   ├── generator_v2.py        # JSON → Python (uses centralized rendering)
│   ├── generator.py           # Legacy generator (inline rendering)
│   ├── designer.py            # CLI tool for schema operations
│   ├── qt_designer/           # Qt/PySide6 GUI designer package
│   │   ├── __init__.py        # Package exports
│   │   ├── __main__.py        # Entry point for python -m
│   │   ├── constants.py       # Colors, elements, defaults
│   │   ├── commands.py        # Undo/redo commands
│   │   ├── canvas.py          # CanvasElement, CanvasView
│   │   ├── palette.py         # Element palette (left sidebar)
│   │   ├── properties.py      # Properties panel (right sidebar)
│   │   ├── navigator.py       # Step navigator (bottom bar)
│   │   ├── preview.py         # Animation preview window
│   │   └── main.py            # PresentationDesigner main window
│   └── visual_designer.py     # Matplotlib GUI designer (legacy)
│
├── schemas/                    # JSON presentation definitions
│   └── *.json
│
└── presentations/              # Generated Python presentations
    └── *_presentation.py
```

---

## Centralized Rendering

The `core/element_rendering.py` module provides a single source of truth for all matplotlib element rendering. Both the Qt designer preview and generated presentations use this module, ensuring **identical visual output**.

```python
from core.element_rendering import ElementRenderer, render_step

# Render a step at 50% progress
render_step(ax, step_data, progress=0.5)

# Or use the renderer directly
renderer = ElementRenderer(ax)
renderer.render(element_data, progress=0.5)
```

---

## Available Presentations

| Presentation | Topics |
|--------------|--------|
| `neural_network` | XOR training, decision boundaries, loss curves |
| `vector` | 2D→3D vectors, semantic space, vector arithmetic |
| `rag` | Chunking, embeddings, vector DB, similarity search |
| `finetuning` | Base model → training → specialist model |
| `prompt_engineering` | Clear instructions, few-shot, chain-of-thought |
| `transformers_attention` | Self-attention, QKV, multi-head, positional encoding |
| `tokenization` | BPE, token flow, special tokens, vocabulary |
| `ai_agents` | Tool use, ReAct, planning, memory, safety |

---

## Qt Designer (Recommended)

Modern PySide6-based GUI editor with full animation preview. Built for speed and reliability.

### Launch
```bash
python -m tools.qt_designer                              # New presentation
python -m tools.qt_designer schemas/existing.json        # Edit existing
```

### Interface Layout

```
┌─────────────────────────────────────────────────────────────────────────┐
│  File   Edit   View                                                     │
├──────────┬───────────────────────────────────────────┬──────────────────┤
│ ELEMENTS │                                           │    PROPERTIES    │
│          │                                           │ ┌──────────────┐ │
│ Aa Text  │              CANVAS                       │ │ ATTENTION_HM │ │
│ Ty| Type │                                           │ └──────────────┘ │
│ </> Code │     (zoomable, pannable, drag elements)   │                  │
│ [ ] Box  │                                           │ [Content][Anim]  │
│ <> Comp  │                                           │                  │
│ ... Chat │                                           │ x: [50]  y: [50] │
│ *** List │                                           │ width:  [30]     │
│ [x] Check│                                           │ tokens_x: [Edit] │
│ o-o Time │                                           │                  │
│ >>> Flow │                                           │ Duration: [1.0]  │
│ ## Grid  │                                           │ Phase: [early ▼] │
│ === Stack│                                           │ Easing: [ease ▼] │
│ -> Arrow │                                           │                  │
│ ~> Arc   │                                           │                  │
│ *** Part │                                           │                  │
│ ooo NN   │                                           │                  │
│ HM Attn  │                                           │                  │
│ ...      │                                           │                  │
├──────────┴───────────────────────────────────────────┴──────────────────┤
│   <  [+] [-]              Step 2/8: Attention in Action              >  │
└─────────────────────────────────────────────────────────────────────────┘
```

### Keyboard Shortcuts

| Key | Action |
|-----|--------|
| **Ctrl+N** | New presentation |
| **Ctrl+O** | Open file |
| **Ctrl+S** | Save |
| **Ctrl+G** | Generate Python code |
| **P** | Preview animation |
| **Ctrl+Z** | Undo |
| **Ctrl+Shift+Z** | Redo |
| **Ctrl+C** | Copy selected element |
| **Ctrl+V** | Paste element |
| **Delete** | Delete selected element |
| **Ctrl+D** | Duplicate selected |
| **Ctrl+Shift+]** | Bring to front |
| **Ctrl+]** | Bring forward |
| **Ctrl+[** | Send backward |
| **Ctrl+Shift+[** | Send to back |
| **Arrow keys** | Nudge element (1 unit) |
| **Shift+Arrow** | Nudge element (5 units) |
| **G** | Toggle snap-to-grid |
| **Ctrl+=** | Zoom in |
| **Ctrl+-** | Zoom out |
| **Ctrl+0** | Reset zoom |

### Mouse Controls

| Action | Result |
|--------|--------|
| Click element in palette | Add to canvas center |
| Click element on canvas | Select it |
| Drag element | Move (with undo support) |
| Scroll wheel | Zoom in/out |
| Middle-click drag | Pan canvas |
| Click property field | Edit value inline |
| Click step name | Rename step |

### Properties Panel

**Content Tab**
- Position (x, y) in 0-100 coordinate space
- Size (width, height) - available for ALL element types
- Type-specific properties (content, items, tokens, etc.)
- List editors for arrays (click "Edit (N items)")
- **Color pickers** with named color dropdown (primary, secondary, accent, etc.)
- **Dropdowns** for style options (arrow style, timeline orientation, arc direction, colormap)

**Animation Tab**
- Duration, Delay, Speed multipliers
- Phase selector (immediate → early → middle → late → final)
- Easing function dropdown (8 options)
- Continuous effect (none, pulse, breathing) - **now fully functional**

### Animation Preview

Press **P** to open the preview window:

```
┌─────────────────────────────────────────────────────────────┐
│                    Preview: Step Name                        │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│                   [Animated Presentation]                   │
│                                                             │
│         Elements appear based on animation phase            │
│         with proper easing and timing                       │
│                                                             │
├─────────────────────────────────────────────────────────────┤
│  [>] [R]  ════════════●═══════════════════  75%   [L]      │
│           imm  early  mid  late  final                      │
└─────────────────────────────────────────────────────────────┘
```

**Preview Controls:**
| Control | Action |
|---------|--------|
| > / \|\| | Play / Pause |
| R | Reset to start |
| Slider | Scrub through animation |
| L | Toggle loop |
| 0.5x / 1x / 2x | Playback speed |
| Space | Play/Pause |
| Esc / Q | Close preview |

### Unsaved Changes

- Window title shows `*` when there are unsaved changes
- Prompts to save when closing with unsaved changes

### Undo/Redo System

All actions are undoable (50 levels):
- Element moves
- Element nudges (arrow keys)
- Add element
- Delete element

---

## Visual Designer (Matplotlib - Legacy)

Original matplotlib-based GUI. Still functional but Qt Designer is recommended.

### Launch
```bash
python -m tools.visual_designer                          # New presentation
python -m tools.visual_designer schemas/existing.json    # Edit existing
python -m tools.visual_designer --new my_presentation    # New with name
```

---

## Element Types (28 total)

### Basic Text
| Type | Icon | Description | Key Properties |
|------|------|-------------|----------------|
| `text` | Aa | Simple text | content, color, fontsize, highlight, underline |
| `typewriter_text` | Ty\| | Character reveal effect | content, show_cursor, cursor_char, reveal (char/word) |
| `counter` | 123 | Animated number counter | value, prefix, suffix, decimals, glow |
| `code_block` | </> | Code display (multi-line) | code, language, width, height |
| `code_execution` | >>> | Code with output below | code, output, stagger |

### Containers
| Type | Icon | Description | Key Properties |
|------|------|-------------|----------------|
| `box` | [ ] | Container with border | width, height, title, content, color, shadow, glow |
| `comparison` | <> | Side-by-side panels | left_title, left_content, right_title, right_content, left_color, right_color |
| `conversation` | ... | Chat-style bubbles | messages[], user_color, assistant_color, system_color, bubble_spacing |

### Media
| Type | Icon | Description | Key Properties |
|------|------|-------------|----------------|
| `image` | IMG | Display image file | src, width, height, border, shadow |

### Lists
| Type | Icon | Description | Key Properties |
|------|------|-------------|----------------|
| `bullet_list` | *** | Bulleted list | items[], bullet_char, text_color, spacing |
| `checklist` | [x] | Checkmark list | items[], check_color, text_color |
| `timeline` | o-o | Timeline (horizontal/vertical) | events[], orientation, line_color |

### Layout
| Type | Icon | Description | Key Properties |
|------|------|-------------|----------------|
| `flow` | >>> | Horizontal process | steps[], colors[], width |
| `grid` | ## | 2D card grid | columns, rows, items[], cell_width, cell_height |
| `stacked_boxes` | === | Vertical stack | items[], base_width, box_height, width_decrease |

### Connectors
| Type | Icon | Description | Key Properties |
|------|------|-------------|----------------|
| `arrow` | -> | Straight arrow | start, end, color, width, head_size, style, head_style, draw_animation, marching_ants |
| `arc_arrow` | ~> | Curved arrow | start, end, arc_height, direction (up/down), color, width, glow, draw_animation |
| `particle_flow` | *** | Animated particles | start, end, num_particles, color, particle_size, spread |

### AI Visualizations
| Type | Icon | Description | Key Properties |
|------|------|-------------|----------------|
| `neural_network` | ooo | Network diagram | layers[], layer_labels[], node_color, connection_color |
| `attention_heatmap` | HM | Attention weights grid | tokens_x[], tokens_y[], weights[][], colormap, title |
| `token_flow` | T>E | Tokenization pipeline | input_text, tokens[], show_embeddings |
| `model_comparison` | A\|B | Side-by-side models | models[], comparison_rows[] |

### Metrics
| Type | Icon | Description | Key Properties |
|------|------|-------------|----------------|
| `similarity_meter` | % | Gauge 0-100% | score, radius, label, glow, show_needle, animate_needle |
| `progress_bar` | [=] | Progress indicator | current, total, width, height, color, label, glow, animate_fill, show_percent |
| `weight_comparison` | W | Before/after bars | before_weights[], after_weights[], labels[], animate_bars |
| `parameter_slider` | -o- | Slider visualization | label, description, min_value, max_value, current_value, color |

### 3D Elements
| Type | Icon | Description | Key Properties |
|------|------|-------------|----------------|
| `scatter_3d` | 3D | 3D scatter plot with camera control | points[{x,y,z,color}], camera_elev, camera_azim, rotate_camera, camera_rotation_speed, show_vectors |
| `vector_3d` | v3 | 3D vectors with labels | vectors[{x,y,z,color,label}], camera_elev, camera_azim, rotate_camera, camera_rotation_speed |

---

## Animation System

### Animation Phases
Elements appear based on `animation_phase`:

| Phase | Progress Range | Use For |
|-------|---------------|---------|
| `immediate` | 0-20% | Titles, backgrounds |
| `early` | 20-40% | Main content |
| `middle` | 40-60% | Supporting details |
| `late` | 60-80% | Additional info |
| `final` | 80-100% | Conclusions |

### Easing Functions
Available via `easing` property:
- `linear` - Constant speed
- `ease_in` - Slow start
- `ease_out` - Slow end
- `ease_in_out` - Smooth both ends
- `ease_in_cubic` - Strong slow start
- `ease_out_cubic` - Strong slow end
- `elastic_out` - Bouncy overshoot
- `bounce_out` - Bounce effect

### Continuous Effects
Via `continuous_effect` property (activates when element is fully visible):
- `none` - Static (default)
- `pulse` - Scale oscillation (±10%) - good for emphasis
- `breathing` - Gentle oscillation (±5%) - subtle attention

Control frequency with `effect_frequency` (default 1.0, higher = faster)

### Timing Properties

**Duration** - Controls how long the fade-in animation takes:
- `duration: 1.0` (default) - Standard timing, 20% of total animation
- `duration: 2.0` - Slower, takes 40% of animation (more gradual reveal)
- `duration: 0.5` - Faster, takes 10% of animation (quick pop-in)

**Delay** - Shifts when the element starts appearing:
- `delay: 0.0` (default) - Starts at phase begin
- `delay: 1.0` - Starts 5% later within the phase

**Speed** - Affects internal animations (typewriter, particles):
- `speed: 1.0` (default) - Normal speed
- `speed: 2.0` - Twice as fast
- `speed: 0.5` - Half speed

**Stagger** - For list/grid elements, controls sequential reveal:
- `stagger: true` (default) - Items appear one by one
- `stagger: false` - All items appear together

### Entry Animations
Elements can fly in from a direction using `entry_animation`:

| Value | Effect |
|-------|--------|
| `none` | No entry animation (default) |
| `left` | Fly in from left |
| `right` | Fly in from right |
| `top` | Fly in from top |
| `bottom` | Fly in from bottom |
| `zoom` | Scale up from small |

Control the distance with `entry_distance` (default: 30 units).

```json
{
  "type": "box",
  "entry_animation": "left",
  "entry_distance": 40
}
```

### Step Transitions
Apply transitions when changing steps using `render_step()`:

| Transition | Effect |
|------------|--------|
| `none` | No transition (default) |
| `fade` | Fade in |
| `slide_left` | Slide in from left |
| `slide_right` | Slide in from right |
| `slide_up` | Slide in from bottom |
| `slide_down` | Slide in from top |
| `zoom` | Zoom in from center |

```python
render_step(ax, step_data, progress, step_transition='slide_right', transition_progress=0.5)
```

---

## Visual Effects

### Shadows
Add depth with drop shadows:
```json
{
  "type": "box",
  "shadow": true,
  "shadow_offset": [2, -2]
}
```

### Glow
Add emphasis with glow effects:
```json
{
  "type": "box",
  "glow": true,
  "glow_color": "accent"
}
```
Works on: `box`, `progress_bar`, `similarity_meter`, `counter`, `arc_arrow`

### Text Highlight
Animated highlight behind text:
```json
{
  "type": "text",
  "highlight": true,
  "highlight_color": "accent"
}
```

### Text Underline
Animated underline that draws in:
```json
{
  "type": "text",
  "underline": true,
  "underline_color": "primary"
}
```

---

## Advanced Element Features

### 3D Elements (scatter_3d, vector_3d)
True 3D rendering with isometric projection and animated camera:
```json
{
  "type": "scatter_3d",
  "position": {"x": 50, "y": 50},
  "points": [
    {"x": 2, "y": 3, "z": 1, "color": "accent"},
    {"x": -1, "y": 2, "z": 4, "color": "primary"}
  ],
  "camera_elev": 20,
  "camera_azim": 45,
  "rotate_camera": true,
  "camera_rotation_speed": 30,
  "show_vectors": false
}
```
- Camera rotates during animation when `rotate_camera: true`
- Points/vectors support per-item colors and labels
- `show_vectors` draws lines from origin to each point

### Attention Heatmap
Visualize attention weights with custom data:
```json
{
  "type": "attention_heatmap",
  "tokens_x": ["The", "cat", "sat"],
  "tokens_y": ["The", "cat", "sat"],
  "weights": [
    [0.9, 0.2, 0.1],
    [0.2, 0.8, 0.3],
    [0.1, 0.3, 0.7]
  ],
  "colormap": "accent",
  "show_values": true,
  "title": "Self-Attention"
}
```
- If `weights` not provided, generates realistic self-attention pattern
- `colormap` uses named colors (accent, primary, warning, etc.)

### Arrow Styling
```json
{
  "type": "arrow",
  "start": {"x": 20, "y": 50},
  "end": {"x": 80, "y": 50},
  "style": "fancy",
  "width": 3,
  "head_size": 20,
  "color": "primary"
}
```
Styles: `simple` (default), `fancy` (thick decorative), `curved` (slight curve)

### Timeline Orientation
```json
{
  "type": "timeline",
  "orientation": "vertical",
  "events": [
    {"date": "2023", "title": "Start"},
    {"date": "2024", "title": "Launch"}
  ],
  "line_color": "dim"
}
```
Orientations: `horizontal` (default), `vertical`

---

## JSON Schema Example

```json
{
  "name": "my_presentation",
  "title": "My Presentation",
  "landing": {
    "title": "Welcome",
    "subtitle": "Introduction",
    "tagline": "Let's learn together"
  },
  "steps": [
    {
      "name": "intro",
      "title": "Introduction",
      "elements": [
        {
          "type": "text",
          "content": "Hello World",
          "position": {"x": 50, "y": 50},
          "animation_phase": "early",
          "easing": "ease_out",
          "continuous_effect": "pulse"
        },
        {
          "type": "attention_heatmap",
          "position": {"x": 50, "y": 30},
          "tokens_x": ["The", "cat", "sat"],
          "tokens_y": ["The", "cat", "sat"],
          "width": 40,
          "height": 40,
          "animation_phase": "middle"
        }
      ],
      "animation_frames": 60
    }
  ]
}
```

---

## CLI Commands

```bash
# Create new schema template
python -m tools.designer new my_presentation --title "My Title"

# Generate Python from JSON (V2 - centralized rendering)
python -m tools.generator_v2 schemas/my_presentation.json

# Generate Python from JSON (legacy - inline rendering)
python -m tools.designer generate schemas/my_presentation.json

# Validate schema
python -m tools.designer validate schemas/my_presentation.json

# List all presentations
python -m tools.designer list
```

---

## Presentation Controls

When running a generated presentation:

| Key | Action |
|-----|--------|
| **Space** | Next step |
| **B** | Previous step |
| **R** | Reset to start |
| **F** | Toggle fullscreen |
| **Q** | Quit |

---

## Color Palette

Available color names for styling:

| Name | Hex | Usage |
|------|-----|-------|
| `primary` | #3B82F6 | Headers, main actions |
| `secondary` | #10B981 | Success, completion |
| `accent` | #F59E0B | Highlights, warnings |
| `highlight` | #EC4899 | Special emphasis |
| `warning` | #EF4444 | Errors, alerts |
| `success` | #10B981 | Positive states |
| `text` | #F0F0F0 | Main text |
| `dim` | #6B7280 | Secondary text |
| `bg_light` | #1a1a1a | Elevated surfaces |

---

## Development

### Adding New Element Types

1. **schema.py**: Add dataclass and add to `SORTED_ELEMENTS` list
   ```python
   @dataclass
   class MyNewElement:
       type: Literal["my_new"] = "my_new"
       position: Position = ...
       # properties

   # Add to SORTED_ELEMENTS with (type, name, icon)
   SORTED_ELEMENTS = [
       ...
       ("my_new", "My New", "MN"),
   ]
   ```

2. **schema.py**: Add to `ElementType` enum and `Element` union

3. **core/element_rendering.py**: Add `_render_my_new()` method to `ElementRenderer`

4. **tools/qt_designer/constants.py**: Add to `ELEMENTS` and `ELEMENT_DEFAULTS`

5. **tools/qt_designer/canvas.py**: Add `_draw_my_new()` method to `CanvasElement`

### Architecture Notes

- **Centralized Rendering**: `core/element_rendering.py` is the single source of truth for matplotlib rendering
- **Qt Designer**: Modular package in `tools/qt_designer/` with separate concerns
- **Generator V2**: Produces compact presentations that import centralized rendering
- **Preview = Final**: Preview window and generated presentations render identically
- **SORTED_ELEMENTS**: Single source of truth for element order and icons
