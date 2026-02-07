# AI Presentation Suite

A matplotlib-based presentation system with JSON schema design and visual GUI editor.

## Quick Start

```bash
# Qt Designer (recommended GUI)
python -m tools.qt_designer schemas/my_presentation.json

# Or legacy matplotlib designer
python -m tools.visual_designer schemas/my_presentation.json

# Generate Python from JSON
python -m tools.designer generate schemas/my_presentation.json

# Run a presentation
python presentations/my_presentation_presentation.py
```

## Project Structure

```
AI-Presentatie/
├── core/                    # Core framework
│   ├── base.py             # BasePresentation class
│   ├── styling.py          # PresentationStyle colors/fonts
│   ├── animations.py       # AnimationHelper, easing functions
│   └── visual_effects.py   # ParticleSystem, SimilarityMeter, etc.
│
├── tools/                   # Design tools
│   ├── schema.py           # JSON schema dataclasses (26 element types)
│   ├── generator.py        # JSON → Python code generator
│   ├── designer.py         # CLI tool for schema operations
│   ├── qt_designer.py      # Qt/PySide6 GUI designer (recommended)
│   └── visual_designer.py  # Matplotlib GUI designer (legacy)
│
├── schemas/                 # JSON presentation definitions
│   └── *.json
│
└── presentations/           # Generated Python presentations
    └── *_presentation.py
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
│ ••• List │                                           │ width:  [30]     │
│ [x] Check│                                           │ tokens_x: [Edit] │
│ o-o Time │                                           │                  │
│ >>> Flow │                                           │ Duration: [1.0]  │
│ ## Grid  │                                           │ Phase: [early ▼] │
│ ≡ Stack  │                                           │ Easing: [ease ▼] │
│ → Arrow  │                                           │                  │
│ ↷ Arc    │                                           │                  │
│ *** Part │                                           │                  │
│ ooo NN   │                                           │                  │
│ HM Attn  │                                           │                  │
│ ...      │                                           │                  │
├──────────┴───────────────────────────────────────────┴──────────────────┤
│   ◀  [+] [−]              Step 2/8: Attention in Action              ▶  │
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
| **Delete** | Delete selected element |
| **Ctrl+D** | Duplicate selected |
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
- Size (width, height)
- Type-specific properties (content, items, tokens, etc.)
- List editors for arrays (click "Edit (N items)")

**Animation Tab**
- Duration, Delay, Speed multipliers
- Phase selector (immediate → early → middle → late → final)
- Easing function dropdown (8 options)
- Continuous effect (none, pulse, breathing)

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
│  [▶] [⟲]  ═══════════●═══════════════════  75%   [🔁]      │
│           imm  early  mid  late  final                      │
└─────────────────────────────────────────────────────────────┘
```

**Preview Controls:**
| Control | Action |
|---------|--------|
| ▶ / ⏸ | Play / Pause |
| ⟲ | Reset to start |
| Slider | Scrub through animation |
| 🔁 | Toggle loop |
| Space | Play/Pause |
| R | Reset |
| Esc / Q | Close preview |

**Rendered Elements (all 26 types):**
- Text elements with typewriter animation
- Attention heatmaps with animated cell reveal and self-attention patterns
- Flow diagrams with staggered step appearance
- Neural networks with layer-by-layer reveal
- Model comparisons with data tables
- Stacked boxes with progressive sizing
- Particle flows with animated particles
- Progress bars and similarity meters with fill animation
- Conversations with message bubbles
- And more...

### Undo/Redo System

All actions are undoable (50 levels):
- Element moves
- Add element
- Delete element

### Why Qt Designer?

| Feature | Matplotlib (old) | Qt/PySide6 (new) |
|---------|------------------|------------------|
| Drag elements | Manual implementation | Built-in flags |
| Selection | Manual hit testing | Native support |
| Zoom/Pan | Complex, buggy | Scroll + middle-drag |
| Form inputs | Tkinter popups | Native widgets |
| Undo/Redo | Not implemented | QUndoStack |
| Performance | Redraw lag | Hardware accelerated |
| Code size | 2500+ lines | ~2200 lines |

---

## Visual Designer (Matplotlib - Legacy)

Original matplotlib-based GUI. Still functional but Qt Designer is recommended.

### Launch
```bash
python -m tools.visual_designer                          # New presentation
python -m tools.visual_designer schemas/existing.json    # Edit existing
python -m tools.visual_designer --new my_presentation    # New with name
```

### Interface Layout

```
┌─────────────────────────────────────────────────────────────────────┐
│  PRESENTATION DESIGNER    [N]ew [O]pen [S]ave [G]enerate [P]review  │
├──────────┬─────────────────────────────────────────┬────────────────┤
│ ELEMENTS │                                         │   PROPERTIES   │
│          │              CANVAS                     │                │
│  [Text]  │                                         │  Element Type  │
│  [Box]   │         (drag & drop area)              │  x: 50  y: 50  │
│  [...]   │                                         │  width: 25     │
│          │                                         │                │
│          │                                         │  Animation:    │
│          │                                         │  [early] [mid] │
│          ├─────────────────────────────────────────┤                │
│          │   < Step 1/5: Introduction >            │  Current Step  │
└──────────┴─────────────────────────────────────────┴────────────────┘
```

### Keyboard Shortcuts

| Key | Action |
|-----|--------|
| **N** | New presentation |
| **O** | Open file |
| **S** | Save |
| **G** | Generate Python code |
| **P** | Preview presentation |
| **E** | Edit selected element |
| **D** | Duplicate selected |
| **Del** | Delete selected |
| **←/→** | Navigate steps |
| **Esc** | Cancel action / Deselect |
| **Q** | Quit (warns if unsaved) |
| **Scroll** | Scroll element list |

### Mouse Controls

| Action | Result |
|--------|--------|
| Click element button | Select element type to place |
| Click canvas | Place element / Select existing |
| Drag on canvas | Move selected element |
| Click property value | Edit property via dialog |
| Click phase button | Set animation phase |
| Click nav buttons | Navigate steps |

### Panel Details

**Elements Panel (Left)**
- 26 element types available (sorted by category)
- Scroll with mouse wheel
- Click to select, click canvas to place
- Active selection highlighted in orange

**Canvas (Center)**
- 100x100 coordinate system
- Subtle grid for alignment
- Blue border indicates canvas bounds
- Elements rendered with selection highlight

**Properties Panel (Right)**
- Shows selected element properties
- Click values to edit via popup dialog
- Animation phase selector buttons
- Current step info at bottom

**Navigation Bar (Bottom)**
- `<` `>` - Previous/Next step
- `+` `-` - Add/Delete step
- Step indicator shows current position

---

## Element Types (26 total)

### Basic Text
| Type | Icon | Description | Key Properties |
|------|------|-------------|----------------|
| `text` | Aa | Simple text | content, style |
| `typewriter_text` | Ty\| | Character reveal effect | content, show_cursor |
| `code_block` | </> | Syntax-highlighted code | code, language, width |
| `code_execution` | >>> | Code with output below | code, output, stagger |

### Containers
| Type | Icon | Description | Key Properties |
|------|------|-------------|----------------|
| `box` | [ ] | Container with border | width, height, title, content |
| `comparison` | <> | Side-by-side panels | left_title, right_title, width |
| `conversation` | ... | Chat-style bubbles | messages[], user_color |

### Lists
| Type | Icon | Description | Key Properties |
|------|------|-------------|----------------|
| `bullet_list` | * * | Bulleted list | items[], stagger |
| `checklist` | [x] | Checkmark list | items[], check_color |
| `timeline` | o-o | Horizontal timeline | events[], orientation |

### Layout
| Type | Icon | Description | Key Properties |
|------|------|-------------|----------------|
| `flow` | >>> | Horizontal process | steps[], width |
| `grid` | ## | 2D card grid | columns, rows, items[] |
| `stacked_boxes` | = | Vertical stack | items[], base_width |

### Connectors
| Type | Icon | Description | Key Properties |
|------|------|-------------|----------------|
| `arrow` | -> | Straight arrow | start, end |
| `arc_arrow` | ~> | Curved arrow | start, end, arc_height |
| `particle_flow` | *** | Animated particles | start, end, num_particles |

### AI Visualizations
| Type | Icon | Description | Key Properties |
|------|------|-------------|----------------|
| `neural_network` | ooo | Network diagram | layers[], width, height |
| `attention_heatmap` | HM | Attention weights grid | tokens_x[], tokens_y[], weights |
| `token_flow` | T>E | Tokenization pipeline | input_text, show_embeddings |
| `model_comparison` | A\|B | Side-by-side models | models[], comparison_rows[] |

### Metrics
| Type | Icon | Description | Key Properties |
|------|------|-------------|----------------|
| `similarity_meter` | % | Gauge 0-100% | score, radius, label |
| `progress_bar` | [=] | Progress indicator | current, total, width |
| `weight_comparison` | W | Before/after bars | before_weights[], after_weights[] |
| `parameter_slider` | -o- | Slider visualization | label, min_value, max_value, current_value |

### 3D Elements
| Type | Icon | Description | Key Properties |
|------|------|-------------|----------------|
| `scatter_3d` | 3D | 3D scatter plot | points[], rotate_camera |
| `vector_3d` | v3 | 3D vectors | vectors[], camera_elev |

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
Via `continuous_effect` property:
- `none` - Static (default)
- `pulse` - Scale oscillation (±10%)
- `breathing` - Gentle oscillation (±5%)

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

When `stagger: true`, duration affects the entire sequence - longer duration means more time between each item appearing.

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

# Generate Python from JSON
python -m tools.designer generate schemas/my_presentation.json

# Validate schema
python -m tools.designer validate schemas/my_presentation.json

# List all presentations
python -m tools.designer list

# Show example schema
python -m tools.designer example
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

3. **generator.py**: Add `_generate_my_new()` method

4. **generator.py**: Add case in `_generate_element_code()`

5. **visual_designer.py**: Add to `_draw_element()` and `_draw_element_thumbnail()`

### Architecture Notes

- **Generator**: Converts schema to Python code with dynamic imports
- **Visual Designer**: Uses matplotlib with optimized panel rendering
- **Presentations**: Extend `BasePresentation` from core module
- **Blitting**: Canvas uses fast redraw during drag operations
- **SORTED_ELEMENTS**: Single source of truth for element order and icons
