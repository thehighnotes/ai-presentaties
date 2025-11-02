# AI Presentation Suite

Geünificeerde presentatie suite voor AI kennissessie met interactieve animaties over vectors, neural networks, RAG, finetuning en quality governance.

## 🏗️ Architecture

```
AI-Presentatie/
├── presentation.py           # Main controller - start hier!
├── core/                     # Gedeelde functionaliteit
│   ├── __init__.py
│   ├── base_presentation.py  # BasePresentation class
│   ├── styling.py           # Dark mode styling & colors
│   ├── controls.py          # Keyboard/mouse handling
│   └── animations.py        # Animation utilities
├── presentations/           # Individuele presentaties
│   ├── __init__.py
│   ├── vector_presentation.py           # [TODO]
│   ├── neural_network_presentation.py   # ✅ COMPLEET - Interactive matplotlib
│   ├── manim_neural_network.py          # Standalone Manim script (optioneel)
│   ├── rag_presentation.py              # [TODO]
│   ├── finetuning_presentation.py       # [TODO]
│   └── quality_presentation.py          # [TODO]
├── config/                  # Data configuratie
│   └── data.json            # [TODO] Externalized data
└── [Legacy files]           # Original .py files (voor referentie)
    ├── Vector.py
    ├── Neural Network.py
    ├── Text-processing.py
    ├── finetuning.py
    └── quality.py
```

## 🚀 Quick Start

### Alle presentaties:
```bash
python presentation.py
```

### Specifieke presentatie:
```bash
python presentation.py neural     # Neural Network
python presentation.py vector     # Vector & Embeddings
python presentation.py rag        # RAG Journey
python presentation.py finetuning # Finetuning
python presentation.py quality    # Quality Governance
```

### Auto-play alle presentaties:
```bash
python presentation.py all
```

## ⌨️ Controls (Uniform voor alle presentaties)

| Toets | Actie |
|-------|-------|
| `SPACE` | Volgende stap |
| `B` | Vorige stap |
| `R` | Reset naar begin |
| `F` | Toggle fullscreen |
| `H` | Help weergeven |
| `Q` of `ESC` | Afsluiten |

### Presentatie-specifieke controls:
- **Neural Network**: `T` = Train 100 epochs, `N`/`P` = Wissel view
- **Vector**: (coming soon)
- **RAG**: (coming soon)

## 🎨 Features

### ✅ Geïmplementeerd
- **Unified Dark Mode**: Consistente styling across alle presentaties
- **Base Presentation Class**: Geen code duplicatie meer
- **Centralized Controls**: Eén plek voor keyboard/mouse handling
- **Animation Helpers**: Easing functions, fade-in/out, etc.
- **Main Controller**: Navigatie tussen presentaties
- **Neural Network Presentation**: Volledig gerefactored met dark mode

### 🚧 In Progress
- Vector Presentation refactoring
- RAG Presentation refactoring
- Finetuning Presentation (+ fix encoding issues)
- Quality Presentation refactoring
- Config data externalization

## 📝 Voor Developers

### Een nieuwe presentatie maken

```python
from core import BasePresentation

class MyPresentation(BasePresentation):
    def __init__(self):
        step_names = ['Landing', 'Step 1', 'Step 2', ...]
        super().__init__("My Title", step_names)
        self.show_landing_page()

    def show_landing_page(self):
        self.fig.clear()
        ax = self.fig.add_subplot(111)
        # ... jouw landing page code

    def animate_step(self, frame: int):
        progress = frame / self.get_frames_for_step(self.current_step)
        # ... jouw animatie code

    def draw_current_step_static(self):
        if self.current_step == -1:
            self.show_landing_page()
        # ... handle andere stappen
```

### Kleuren gebruiken

```python
# Via self.colors dict (beschikbaar in alle BasePresentation subclasses)
self.colors['primary']      # Blue
self.colors['secondary']    # Green
self.colors['accent']       # Orange
self.colors['highlight']    # Pink
self.colors['warning']      # Red
self.colors['text']         # Light gray
self.colors['bg']           # Near black
self.colors['bg_light']     # Dark gray

# Of direct via PresentationStyle
from core import PresentationStyle
color = PresentationStyle.get_color('primary')
```

### Animation easing

```python
from core import AnimationHelper

# Smooth ease in/out
smooth_progress = AnimationHelper.ease_in_out(progress)

# Fade in with delay
alpha = AnimationHelper.fade_in(progress, delay=0.2, duration=0.3)

# Staggered animation
for i, item in enumerate(items):
    delay = AnimationHelper.stagger_delay(i, len(items), 0.1, 0.5)
    if progress > delay:
        # Draw item
```

## 🐛 Known Issues

1. **Character Encoding**: Original `finetuning.py` heeft corrupted unicode - moet gefixed worden
2. **Legacy Files**: Original .py files zijn nog aanwezig voor referentie
3. **Incomplete Refactoring**: Nog niet alle presentaties gerefactored

## 📊 Progress Status

- [x] Core modules (styling, controls, animations, base)
- [x] Main controller (presentation.py)
- [x] Neural Network presentation (COMPLEET)
- [ ] Vector presentation (in progress)
- [ ] RAG presentation (TODO)
- [ ] Finetuning presentation (TODO - fix encoding)
- [ ] Quality presentation (TODO)
- [ ] Config data files (TODO)
- [ ] End-to-end testing (TODO)

## 🎯 Next Steps

1. Finish refactoring remaining presentations
2. Fix encoding issues in finetuning
3. Externalize hardcoded data to config files
4. Add comprehensive error handling
5. Test complete flow
6. Remove legacy files

## 📄 License

Internal use - AI Kennissessie

## 👥 Contact

Voor vragen over deze presentatie suite, neem contact op met het team.
