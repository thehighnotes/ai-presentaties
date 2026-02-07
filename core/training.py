"""
Training visualization system - generic foundations.

Provides:
- TrainingState: Immutable snapshot of training at a point in time
- TrainingSession: Collection of states (recorded or live)
- TrainingRecorder: Records live training for later playback
- TrainingController: Manages playback/scrubbing of training sessions

This is designed to be model-agnostic - works with any training loop
that can provide state snapshots.
"""

import json
import time
from dataclasses import dataclass, field, asdict
from typing import Dict, List, Any, Optional, Callable, Union
from pathlib import Path
import numpy as np


@dataclass
class TrainingState:
    """
    Immutable snapshot of training state at a specific point.

    This is the core data structure that all training visualizations consume.
    It's intentionally generic - specific training scenarios add their own
    data to the `custom` dict.
    """
    # Core training progress
    epoch: int = 0
    total_epochs: int = 100
    batch: int = 0
    total_batches: int = 1

    # Loss tracking
    loss: float = 0.0
    val_loss: Optional[float] = None
    loss_history: List[float] = field(default_factory=list)
    val_loss_history: List[float] = field(default_factory=list)

    # Metrics (accuracy, f1, etc.)
    metrics: Dict[str, float] = field(default_factory=dict)
    metrics_history: Dict[str, List[float]] = field(default_factory=dict)

    # Network state (layer_name -> values)
    weights: Dict[str, Any] = field(default_factory=dict)
    biases: Dict[str, Any] = field(default_factory=dict)
    gradients: Dict[str, Any] = field(default_factory=dict)
    activations: Dict[str, Any] = field(default_factory=dict)

    # Hyperparameters (can change during training)
    hyperparameters: Dict[str, float] = field(default_factory=lambda: {
        'learning_rate': 0.01,
        'batch_size': 32,
        'dropout_rate': 0.0,
        'momentum': 0.0,
        'weight_decay': 0.0,
    })

    # Predictions and data (for visualization)
    predictions: Optional[Any] = None
    decision_boundary: Optional[Any] = None  # For classification viz

    # Custom data for specific visualizations
    custom: Dict[str, Any] = field(default_factory=dict)

    # Timestamp
    timestamp: float = field(default_factory=time.time)

    @property
    def progress(self) -> float:
        """Training progress as 0-1 float."""
        if self.total_epochs == 0:
            return 0.0
        return self.epoch / self.total_epochs

    @property
    def batch_progress(self) -> float:
        """Batch progress within current epoch as 0-1 float."""
        if self.total_batches == 0:
            return 0.0
        return self.batch / self.total_batches

    def to_dict(self) -> Dict:
        """Convert to JSON-serializable dict."""
        d = asdict(self)
        # Convert numpy arrays to lists
        for key in ['weights', 'biases', 'gradients', 'activations']:
            if d[key]:
                d[key] = {k: v.tolist() if hasattr(v, 'tolist') else v
                         for k, v in d[key].items()}
        if d['predictions'] is not None and hasattr(d['predictions'], 'tolist'):
            d['predictions'] = d['predictions'].tolist()
        if d['decision_boundary'] is not None and hasattr(d['decision_boundary'], 'tolist'):
            d['decision_boundary'] = d['decision_boundary'].tolist()
        return d

    @classmethod
    def from_dict(cls, d: Dict) -> 'TrainingState':
        """Create from dict (e.g., loaded from JSON)."""
        # Convert lists back to numpy arrays for known array fields
        for key in ['weights', 'biases', 'gradients', 'activations']:
            if d.get(key):
                d[key] = {k: np.array(v) if isinstance(v, list) else v
                         for k, v in d[key].items()}
        if d.get('predictions') is not None and isinstance(d['predictions'], list):
            d['predictions'] = np.array(d['predictions'])
        if d.get('decision_boundary') is not None and isinstance(d['decision_boundary'], list):
            d['decision_boundary'] = np.array(d['decision_boundary'])
        return cls(**d)


class TrainingSession:
    """
    A collection of training states that can be played back.

    Can be:
    - Pre-recorded (loaded from file)
    - Live (states added during training)

    Supports:
    - Scrubbing to any epoch
    - Interpolation between states
    - Play/pause/step
    """

    def __init__(self, name: str = "session"):
        self.name = name
        self.states: List[TrainingState] = []
        self._current_index: int = 0
        self._is_live: bool = False
        self._on_state_change: Optional[Callable[[TrainingState], None]] = None

    @property
    def current_state(self) -> Optional[TrainingState]:
        """Get the current training state."""
        if not self.states:
            return None
        return self.states[self._current_index]

    @property
    def current_epoch(self) -> int:
        """Get current epoch number."""
        return self.current_state.epoch if self.current_state else 0

    @property
    def total_epochs(self) -> int:
        """Get total number of recorded epochs."""
        return len(self.states)

    @property
    def can_scrub(self) -> bool:
        """Whether scrubbing is supported (not live mode)."""
        return not self._is_live and len(self.states) > 0

    def add_state(self, state: TrainingState):
        """Add a new training state (for recording/live mode)."""
        self.states.append(state)
        if self._is_live:
            self._current_index = len(self.states) - 1
            if self._on_state_change:
                self._on_state_change(state)

    def go_to_epoch(self, epoch: int):
        """Jump to a specific epoch."""
        if not self.states:
            return
        # Find state closest to requested epoch
        for i, state in enumerate(self.states):
            if state.epoch >= epoch:
                self._current_index = i
                break
        else:
            self._current_index = len(self.states) - 1

        if self._on_state_change and self.current_state:
            self._on_state_change(self.current_state)

    def go_to_index(self, index: int):
        """Jump to a specific state index."""
        if not self.states:
            return
        self._current_index = max(0, min(index, len(self.states) - 1))
        if self._on_state_change and self.current_state:
            self._on_state_change(self.current_state)

    def step_forward(self) -> bool:
        """Advance to next state. Returns False if at end."""
        if self._current_index < len(self.states) - 1:
            self._current_index += 1
            if self._on_state_change:
                self._on_state_change(self.current_state)
            return True
        return False

    def step_backward(self) -> bool:
        """Go to previous state. Returns False if at start."""
        if self._current_index > 0:
            self._current_index -= 1
            if self._on_state_change:
                self._on_state_change(self.current_state)
            return True
        return False

    def get_interpolated_state(self, t: float) -> Optional[TrainingState]:
        """
        Get interpolated state at time t (0-1).

        For smooth scrubbing between discrete states.
        """
        if not self.states:
            return None
        if len(self.states) == 1:
            return self.states[0]

        # Find surrounding states
        float_index = t * (len(self.states) - 1)
        lower_idx = int(float_index)
        upper_idx = min(lower_idx + 1, len(self.states) - 1)
        blend = float_index - lower_idx

        if blend < 0.01:
            return self.states[lower_idx]
        if blend > 0.99:
            return self.states[upper_idx]

        # Interpolate between states (for smooth visualization)
        s1, s2 = self.states[lower_idx], self.states[upper_idx]

        # Linear interpolation of numeric values
        return TrainingState(
            epoch=int(s1.epoch + blend * (s2.epoch - s1.epoch)),
            total_epochs=s2.total_epochs,
            batch=int(s1.batch + blend * (s2.batch - s1.batch)),
            total_batches=s2.total_batches,
            loss=s1.loss + blend * (s2.loss - s1.loss),
            val_loss=(s1.val_loss + blend * (s2.val_loss - s1.val_loss))
                     if s1.val_loss and s2.val_loss else None,
            loss_history=s2.loss_history,  # Use later state's history
            val_loss_history=s2.val_loss_history,
            metrics={k: s1.metrics.get(k, 0) + blend * (s2.metrics.get(k, 0) - s1.metrics.get(k, 0))
                    for k in set(s1.metrics) | set(s2.metrics)},
            metrics_history=s2.metrics_history,
            weights=s2.weights,  # Can't easily interpolate weight matrices
            biases=s2.biases,
            gradients=s2.gradients,
            activations=s2.activations,
            hyperparameters=s2.hyperparameters,
            predictions=s2.predictions,
            decision_boundary=s2.decision_boundary,
            custom=s2.custom,
        )

    def on_state_change(self, callback: Callable[[TrainingState], None]):
        """Register callback for state changes."""
        self._on_state_change = callback

    def save(self, path: Union[str, Path]):
        """Save session to JSON file."""
        path = Path(path)
        data = {
            'name': self.name,
            'states': [s.to_dict() for s in self.states]
        }
        with open(path, 'w') as f:
            json.dump(data, f, indent=2)

    @classmethod
    def load(cls, path: Union[str, Path]) -> 'TrainingSession':
        """Load session from JSON file."""
        path = Path(path)
        with open(path) as f:
            data = json.load(f)

        session = cls(name=data.get('name', 'loaded'))
        for state_dict in data.get('states', []):
            session.add_state(TrainingState.from_dict(state_dict))
        return session


class TrainingRecorder:
    """
    Records training states from a live training loop.

    Usage:
        recorder = TrainingRecorder()

        for epoch in range(epochs):
            # ... training code ...
            recorder.record(
                epoch=epoch,
                loss=loss,
                weights={'layer1': w1, 'layer2': w2},
                # ... other state ...
            )

        recorder.save('training_session.json')
    """

    def __init__(self, total_epochs: int = 100, record_every: int = 1):
        self.session = TrainingSession("recording")
        self.total_epochs = total_epochs
        self.record_every = record_every  # Record every N epochs
        self._epoch_counter = 0

    def record(self, epoch: int, loss: float, **kwargs):
        """
        Record a training state.

        Args:
            epoch: Current epoch number
            loss: Current loss value
            **kwargs: Any other TrainingState fields
        """
        if epoch % self.record_every != 0:
            return

        # Build loss history from session
        loss_history = [s.loss for s in self.session.states]
        loss_history.append(loss)

        val_loss = kwargs.pop('val_loss', None)
        val_loss_history = [s.val_loss for s in self.session.states if s.val_loss]
        if val_loss is not None:
            val_loss_history.append(val_loss)

        state = TrainingState(
            epoch=epoch,
            total_epochs=self.total_epochs,
            loss=loss,
            val_loss=val_loss,
            loss_history=loss_history,
            val_loss_history=val_loss_history,
            **kwargs
        )
        self.session.add_state(state)

    def save(self, path: Union[str, Path]):
        """Save recorded session."""
        self.session.save(path)


class InteractiveParameter:
    """
    A parameter that can be adjusted during training/visualization.

    Provides:
    - Current value
    - Min/max range
    - Step size
    - Change callbacks
    """

    def __init__(self, name: str, initial: float, min_val: float, max_val: float,
                 step: float = 0.01, log_scale: bool = False):
        self.name = name
        self._value = initial
        self.min_val = min_val
        self.max_val = max_val
        self.step = step
        self.log_scale = log_scale
        self._callbacks: List[Callable[[float], None]] = []

    @property
    def value(self) -> float:
        return self._value

    @value.setter
    def value(self, new_val: float):
        new_val = max(self.min_val, min(self.max_val, new_val))
        if new_val != self._value:
            self._value = new_val
            for cb in self._callbacks:
                cb(new_val)

    def on_change(self, callback: Callable[[float], None]):
        """Register callback for value changes."""
        self._callbacks.append(callback)

    def to_dict(self) -> Dict:
        return {
            'name': self.name,
            'value': self._value,
            'min': self.min_val,
            'max': self.max_val,
            'step': self.step,
            'log_scale': self.log_scale
        }


class TrainingController:
    """
    Controls playback and interaction with a training session.

    Manages:
    - Play/pause state
    - Playback speed
    - Epoch scrubbing
    - Interactive parameters
    - Callbacks for UI updates
    """

    def __init__(self, session: Optional[TrainingSession] = None):
        self.session = session
        self.is_playing = False
        self.playback_speed = 1.0  # Epochs per second
        self.loop = False

        # Interactive parameters
        self.parameters: Dict[str, InteractiveParameter] = {}

        # Callbacks
        self._on_update: Optional[Callable[[], None]] = None
        self._on_play_state_change: Optional[Callable[[bool], None]] = None

        # Default parameters
        self.add_parameter(InteractiveParameter('learning_rate', 0.01, 0.0001, 1.0, 0.001, log_scale=True))
        self.add_parameter(InteractiveParameter('dropout_rate', 0.0, 0.0, 0.9, 0.05))
        self.add_parameter(InteractiveParameter('batch_size', 32, 1, 256, 1))

    def set_session(self, session: TrainingSession):
        """Set the training session to control."""
        self.session = session

    def add_parameter(self, param: InteractiveParameter):
        """Add an interactive parameter."""
        self.parameters[param.name] = param

    def play(self):
        """Start playback."""
        self.is_playing = True
        if self._on_play_state_change:
            self._on_play_state_change(True)

    def pause(self):
        """Pause playback."""
        self.is_playing = False
        if self._on_play_state_change:
            self._on_play_state_change(False)

    def toggle_play(self):
        """Toggle play/pause."""
        if self.is_playing:
            self.pause()
        else:
            self.play()

    def reset(self):
        """Go to beginning."""
        if self.session:
            self.session.go_to_index(0)

    def step(self, forward: bool = True):
        """Step one epoch forward or backward."""
        if self.session:
            if forward:
                at_end = not self.session.step_forward()
                if at_end and self.loop:
                    self.session.go_to_index(0)
            else:
                self.session.step_backward()

    def scrub_to(self, t: float):
        """
        Scrub to position t (0-1).
        """
        if self.session and self.session.can_scrub:
            index = int(t * (len(self.session.states) - 1))
            self.session.go_to_index(index)

    def tick(self, dt: float):
        """
        Update for animation frame.

        Args:
            dt: Time delta in seconds since last tick

        Returns:
            True if state changed, False otherwise
        """
        if not self.is_playing or not self.session:
            return False

        # Calculate epochs to advance based on speed
        epochs_to_advance = dt * self.playback_speed

        # For now, step if enough time has passed
        if epochs_to_advance >= 1.0:
            at_end = not self.session.step_forward()
            if at_end:
                if self.loop:
                    self.session.go_to_index(0)
                else:
                    self.pause()
            return True

        return False

    def on_update(self, callback: Callable[[], None]):
        """Register callback for any update."""
        self._on_update = callback

    def on_play_state_change(self, callback: Callable[[bool], None]):
        """Register callback for play/pause changes."""
        self._on_play_state_change = callback
