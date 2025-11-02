"""
Core modules for AI Presentation Suite
Shared functionality across all presentations
"""

from .styling import PresentationStyle
from .controls import ControlHandler
from .base_presentation import BasePresentation
from .animations import AnimationHelper
from .visual_effects import (
    AnimationHelpers,
    ParticleSystem,
    SimilarityMeter,
    Performance3D,
    WeightDeltaVisualizer,
    ProgressIndicator
)

__all__ = [
    'PresentationStyle',
    'ControlHandler',
    'BasePresentation',
    'AnimationHelper',
    'AnimationHelpers',
    'ParticleSystem',
    'SimilarityMeter',
    'Performance3D',
    'WeightDeltaVisualizer',
    'ProgressIndicator'
]
