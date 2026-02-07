"""
Training Controller Widget for Qt Designer.

Provides interactive controls for training visualizations:
- Epoch scrubber
- Play/Pause/Step controls
- Speed control
- Interactive parameter sliders
"""

from typing import Optional, Dict, Callable

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QSlider,
    QLabel, QSpinBox, QDoubleSpinBox, QGroupBox, QFormLayout,
    QCheckBox, QFrame
)
from PySide6.QtCore import Qt, Signal, QTimer
from PySide6.QtGui import QFont

from .constants import COLORS
from core.training import TrainingSession, TrainingController, TrainingState


class TrainingControllerWidget(QWidget):
    """
    Interactive training controller UI.

    Provides:
    - Epoch scrubber (slider)
    - Play/Pause/Step buttons
    - Playback speed control
    - Loop toggle
    - Interactive parameter sliders

    Signals:
        state_changed(TrainingState): Emitted when training state changes
        parameter_changed(str, float): Emitted when a parameter is adjusted
    """

    state_changed = Signal(object)  # TrainingState
    parameter_changed = Signal(str, float)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.controller: Optional[TrainingController] = None
        self._timer = QTimer()
        self._timer.timeout.connect(self._tick)
        self._last_tick = 0

        self._setup_ui()

    def _setup_ui(self):
        """Build the UI."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(8)

        # Apply dark styling
        self.setStyleSheet(f"""
            QWidget {{
                background-color: {COLORS['bg']};
                color: {COLORS['text']};
            }}
            QGroupBox {{
                color: {COLORS['secondary']};
                font-weight: bold;
                border: 1px solid {COLORS['dim']};
                border-radius: 4px;
                margin-top: 8px;
                padding-top: 4px;
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                left: 8px;
                padding: 0 4px;
            }}
            QPushButton {{
                background-color: {COLORS['bg_light']};
                border: 1px solid {COLORS['dim']};
                border-radius: 4px;
                padding: 6px 12px;
                color: {COLORS['text']};
            }}
            QPushButton:hover {{
                background-color: {COLORS['primary']};
                border-color: {COLORS['primary']};
            }}
            QPushButton:pressed {{
                background-color: {COLORS['secondary']};
            }}
            QPushButton:checked {{
                background-color: {COLORS['primary']};
                border-color: {COLORS['accent']};
            }}
            QSlider::groove:horizontal {{
                height: 6px;
                background: {COLORS['bg_light']};
                border-radius: 3px;
            }}
            QSlider::handle:horizontal {{
                background: {COLORS['primary']};
                width: 16px;
                margin: -5px 0;
                border-radius: 8px;
            }}
            QSlider::sub-page:horizontal {{
                background: {COLORS['primary']};
                border-radius: 3px;
            }}
        """)

        # Epoch scrubber section
        epoch_group = QGroupBox("Epoch")
        epoch_layout = QVBoxLayout(epoch_group)

        # Epoch slider
        slider_layout = QHBoxLayout()
        self.epoch_label = QLabel("0")
        self.epoch_label.setMinimumWidth(40)
        slider_layout.addWidget(self.epoch_label)

        self.epoch_slider = QSlider(Qt.Horizontal)
        self.epoch_slider.setMinimum(0)
        self.epoch_slider.setMaximum(100)
        self.epoch_slider.valueChanged.connect(self._on_epoch_changed)
        slider_layout.addWidget(self.epoch_slider, 1)

        self.total_epochs_label = QLabel("/ 100")
        slider_layout.addWidget(self.total_epochs_label)

        epoch_layout.addLayout(slider_layout)

        # Transport controls
        transport_layout = QHBoxLayout()
        transport_layout.setSpacing(4)

        self.btn_reset = QPushButton("⏮")
        self.btn_reset.setFixedWidth(36)
        self.btn_reset.setToolTip("Reset to start")
        self.btn_reset.clicked.connect(self._on_reset)
        transport_layout.addWidget(self.btn_reset)

        self.btn_step_back = QPushButton("⏪")
        self.btn_step_back.setFixedWidth(36)
        self.btn_step_back.setToolTip("Step backward")
        self.btn_step_back.clicked.connect(lambda: self._on_step(False))
        transport_layout.addWidget(self.btn_step_back)

        self.btn_play = QPushButton("▶")
        self.btn_play.setCheckable(True)
        self.btn_play.setFixedWidth(50)
        self.btn_play.setToolTip("Play/Pause")
        self.btn_play.clicked.connect(self._on_play_toggle)
        transport_layout.addWidget(self.btn_play)

        self.btn_step_forward = QPushButton("⏩")
        self.btn_step_forward.setFixedWidth(36)
        self.btn_step_forward.setToolTip("Step forward")
        self.btn_step_forward.clicked.connect(lambda: self._on_step(True))
        transport_layout.addWidget(self.btn_step_forward)

        self.btn_loop = QPushButton("🔁")
        self.btn_loop.setCheckable(True)
        self.btn_loop.setFixedWidth(36)
        self.btn_loop.setToolTip("Loop")
        self.btn_loop.clicked.connect(self._on_loop_toggle)
        transport_layout.addWidget(self.btn_loop)

        transport_layout.addStretch()

        # Speed control
        speed_layout = QHBoxLayout()
        speed_layout.addWidget(QLabel("Speed:"))

        for speed in [0.5, 1.0, 2.0, 4.0]:
            btn = QPushButton(f"{speed}x")
            btn.setFixedWidth(40)
            btn.setCheckable(True)
            btn.clicked.connect(lambda checked, s=speed: self._on_speed_changed(s))
            if speed == 1.0:
                btn.setChecked(True)
                self._current_speed_btn = btn
            speed_layout.addWidget(btn)
            setattr(self, f'btn_speed_{str(speed).replace(".", "_")}', btn)

        transport_layout.addLayout(speed_layout)

        epoch_layout.addLayout(transport_layout)
        layout.addWidget(epoch_group)

        # Parameters section
        self.params_group = QGroupBox("Parameters")
        self.params_layout = QFormLayout(self.params_group)
        self.params_layout.setSpacing(6)

        # Default parameters
        self._add_parameter_slider("learning_rate", 0.01, 0.0001, 1.0, 4)
        self._add_parameter_slider("dropout_rate", 0.0, 0.0, 0.9, 2)
        self._add_parameter_slider("batch_size", 32, 1, 256, 0)

        layout.addWidget(self.params_group)

        # Status
        self.status_label = QLabel("No training session loaded")
        self.status_label.setStyleSheet(f"color: {COLORS['dim']}; font-size: 11px;")
        layout.addWidget(self.status_label)

        layout.addStretch()

    def _add_parameter_slider(self, name: str, default: float, min_val: float, max_val: float, decimals: int = 2):
        """Add a parameter slider."""
        container = QWidget()
        h_layout = QHBoxLayout(container)
        h_layout.setContentsMargins(0, 0, 0, 0)

        if decimals == 0:
            slider = QSlider(Qt.Horizontal)
            slider.setMinimum(int(min_val))
            slider.setMaximum(int(max_val))
            slider.setValue(int(default))

            value_label = QLabel(str(int(default)))
            value_label.setMinimumWidth(40)

            def on_change(v, n=name, lbl=value_label):
                lbl.setText(str(v))
                self.parameter_changed.emit(n, float(v))

            slider.valueChanged.connect(on_change)
        else:
            # For float values, use slider with scaling
            slider = QSlider(Qt.Horizontal)
            scale = 10 ** decimals
            slider.setMinimum(int(min_val * scale))
            slider.setMaximum(int(max_val * scale))
            slider.setValue(int(default * scale))

            value_label = QLabel(f"{default:.{decimals}f}")
            value_label.setMinimumWidth(50)

            def on_change(v, n=name, lbl=value_label, s=scale, d=decimals):
                actual = v / s
                lbl.setText(f"{actual:.{d}f}")
                self.parameter_changed.emit(n, actual)

            slider.valueChanged.connect(on_change)

        h_layout.addWidget(slider, 1)
        h_layout.addWidget(value_label)

        self.params_layout.addRow(f"{name}:", container)

    def set_session(self, session: TrainingSession):
        """Set the training session to control."""
        if self.controller is None:
            self.controller = TrainingController()

        self.controller.set_session(session)
        session.on_state_change(self._on_state_update)

        # Update UI
        self.epoch_slider.setMaximum(max(session.total_epochs - 1, 0))
        self.total_epochs_label.setText(f"/ {session.total_epochs}")
        self.status_label.setText(f"Session: {session.name} ({session.total_epochs} epochs)")

        # Emit initial state
        if session.current_state:
            self._on_state_update(session.current_state)

    def _on_epoch_changed(self, value: int):
        """Handle epoch slider change."""
        if self.controller and self.controller.session:
            self.controller.session.go_to_index(value)
        self.epoch_label.setText(str(value))

    def _on_play_toggle(self):
        """Handle play/pause toggle."""
        if self.controller:
            if self.btn_play.isChecked():
                self.controller.play()
                self.btn_play.setText("⏸")
                self._start_playback()
            else:
                self.controller.pause()
                self.btn_play.setText("▶")
                self._stop_playback()

    def _on_reset(self):
        """Handle reset button."""
        if self.controller:
            self.controller.reset()
            self.epoch_slider.setValue(0)

    def _on_step(self, forward: bool):
        """Handle step forward/backward."""
        if self.controller:
            self.controller.step(forward)
            if self.controller.session:
                self.epoch_slider.setValue(self.controller.session._current_index)

    def _on_loop_toggle(self):
        """Handle loop toggle."""
        if self.controller:
            self.controller.loop = self.btn_loop.isChecked()

    def _on_speed_changed(self, speed: float):
        """Handle speed change."""
        if self.controller:
            self.controller.playback_speed = speed

        # Update button states
        for s in [0.5, 1.0, 2.0, 4.0]:
            btn = getattr(self, f'btn_speed_{str(s).replace(".", "_")}', None)
            if btn:
                btn.setChecked(s == speed)

    def _start_playback(self):
        """Start the playback timer."""
        import time
        self._last_tick = time.time()
        self._timer.start(33)  # ~30 FPS

    def _stop_playback(self):
        """Stop the playback timer."""
        self._timer.stop()

    def _tick(self):
        """Timer tick for playback."""
        import time
        now = time.time()
        dt = now - self._last_tick
        self._last_tick = now

        if self.controller:
            if self.controller.tick(dt):
                # State changed
                if self.controller.session:
                    # Update slider without triggering callback
                    self.epoch_slider.blockSignals(True)
                    self.epoch_slider.setValue(self.controller.session._current_index)
                    self.epoch_slider.blockSignals(False)
                    self.epoch_label.setText(str(self.controller.session._current_index))

            # Check if playback stopped
            if not self.controller.is_playing:
                self.btn_play.setChecked(False)
                self.btn_play.setText("▶")
                self._stop_playback()

    def _on_state_update(self, state: TrainingState):
        """Handle training state update."""
        self.state_changed.emit(state)

        # Update epoch display
        self.epoch_label.setText(str(state.epoch))

    def get_current_state(self) -> Optional[TrainingState]:
        """Get the current training state."""
        if self.controller and self.controller.session:
            return self.controller.session.current_state
        return None
