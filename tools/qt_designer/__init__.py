"""
Qt Designer Package for Presentation Design

A modular GUI editor for creating animated presentations.
Uses PySide6 for the interface and matplotlib for preview rendering.

Usage:
    python -m tools.qt_designer [schema.json]

Architecture:
    - constants.py: Colors, element definitions, defaults
    - commands.py: Undo/redo commands (QUndoCommand subclasses)
    - canvas.py: CanvasElement, CanvasView (draggable elements, zoom/pan)
    - palette.py: ElementPalette (left sidebar)
    - properties.py: PropertiesPanel (right sidebar, property editing)
    - navigator.py: StepNavigator (bottom bar)
    - preview.py: PreviewWindow (animation preview using core/element_rendering)
    - main.py: PresentationDesigner (main window)

The preview window uses core/element_rendering.py for rendering, ensuring
identical output between preview and generated presentations.
"""

from .main import PresentationDesigner, main
from .canvas import CanvasElement, CanvasView
from .palette import ElementPalette
from .properties import PropertiesPanel
from .navigator import StepNavigator
from .preview import PreviewWindow
from .constants import COLORS, ELEMENTS, ELEMENT_DEFAULTS

__all__ = [
    'PresentationDesigner',
    'main',
    'CanvasElement',
    'CanvasView',
    'ElementPalette',
    'PropertiesPanel',
    'StepNavigator',
    'PreviewWindow',
    'COLORS',
    'ELEMENTS',
    'ELEMENT_DEFAULTS',
]
