"""
Animation preview window for the Qt Designer.
Uses the centralized element rendering from core/element_rendering.py.

Supports two modes:
1. Standard animation preview (progress 0-1)
2. Training mode (live neural network training with interactive controls)
"""

from typing import Dict, Optional, List

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QSlider, QLabel,
    QTabWidget, QGroupBox, QFormLayout, QDoubleSpinBox, QSpinBox,
    QSplitter, QFrame
)
from PySide6.QtCore import Qt, QTimer, Signal

# Matplotlib with Qt backend
import matplotlib
matplotlib.use('QtAgg')
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from core.element_rendering import render_step, step_needs_3d_axes, COLORS
from core.training import TrainingState, TrainingSession


class PreviewWindow(QWidget):
    """Animation preview window using matplotlib."""

    def __init__(self, step_data: Dict, step_name: str, parent=None):
        super().__init__(parent, Qt.Window)  # Make it a separate window
        self.step_data = step_data
        self.step_name = step_name
        self.progress = 0.0
        self.playing = False
        self.loop = True

        # Training mode
        self.training_mode = False
        self.trainer = None
        self.training_state: Optional[TrainingState] = None

        # Check if we need 3D axes for this step
        self.needs_3d = step_needs_3d_axes(step_data)

        # Check if step contains training elements
        self._check_training_elements()

        self.setWindowTitle(f"Preview: {step_name}")
        self.setMinimumSize(1100, 750)
        self.setStyleSheet(f"background-color: {COLORS['bg']};")

        # Enable keyboard focus
        self.setFocusPolicy(Qt.StrongFocus)

        self._setup_ui()
        self._setup_timer()
        self._render()

    def _check_training_elements(self):
        """Check if step contains training visualization elements."""
        training_types = {'loss_curve', 'decision_boundary_2d', 'xor_problem',
                         'gradient_flow', 'dropout_layer', 'optimizer_paths', 'confusion_matrix'}
        for elem in self.step_data.get('elements', []):
            if elem.get('type') in training_types:
                self.training_mode = True
                break

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Main content area
        if self.training_mode:
            # Use splitter for training mode
            splitter = QSplitter(Qt.Horizontal)

            # Left: Matplotlib canvas
            canvas_widget = QWidget()
            canvas_layout = QVBoxLayout(canvas_widget)
            canvas_layout.setContentsMargins(0, 0, 0, 0)

            self.figure = Figure(figsize=(10, 7), facecolor=COLORS['bg'])
            self.canvas = FigureCanvas(self.figure)

            if self.needs_3d:
                self.ax = self.figure.add_subplot(111, projection='3d')
            else:
                self.ax = self.figure.add_subplot(111)

            canvas_layout.addWidget(self.canvas)
            splitter.addWidget(canvas_widget)

            # Right: Training controls
            self.training_panel = self._create_training_panel()
            splitter.addWidget(self.training_panel)

            splitter.setSizes([800, 300])
            splitter.setStretchFactor(0, 1)
            splitter.setStretchFactor(1, 0)

            layout.addWidget(splitter, stretch=1)
        else:
            # Standard mode - just canvas
            self.figure = Figure(figsize=(10, 7), facecolor=COLORS['bg'])
            self.canvas = FigureCanvas(self.figure)

            if self.needs_3d:
                self.ax = self.figure.add_subplot(111, projection='3d')
            else:
                self.ax = self.figure.add_subplot(111)

            layout.addWidget(self.canvas, stretch=1)

        # Controls bar (standard or training)
        if self.training_mode:
            controls = self._create_training_controls()
        else:
            controls = self._create_standard_controls()

        layout.addWidget(controls)

    def _create_standard_controls(self) -> QWidget:
        """Create standard animation controls."""
        controls = QWidget()
        controls.setFixedHeight(60)
        controls.setStyleSheet(f"background-color: {COLORS.get('panel', '#0d0d14')};")
        ctrl_layout = QHBoxLayout(controls)
        ctrl_layout.setContentsMargins(16, 8, 16, 8)

        btn_style = self._get_button_style()

        # Play/Pause
        self.play_btn = QPushButton(">")
        self.play_btn.setFixedSize(50, 40)
        self.play_btn.setStyleSheet(btn_style)
        self.play_btn.clicked.connect(self._toggle_play)
        ctrl_layout.addWidget(self.play_btn)

        # Reset
        self.reset_btn = QPushButton("R")
        self.reset_btn.setFixedSize(50, 40)
        self.reset_btn.setStyleSheet(btn_style)
        self.reset_btn.clicked.connect(self._reset)
        ctrl_layout.addWidget(self.reset_btn)

        ctrl_layout.addSpacing(16)

        # Progress slider
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(0, 1000)
        self.slider.setValue(0)
        self.slider.setStyleSheet(self._get_slider_style())
        self.slider.valueChanged.connect(self._on_slider_change)
        self.slider.sliderPressed.connect(lambda: setattr(self, 'playing', False))
        ctrl_layout.addWidget(self.slider, stretch=1)

        ctrl_layout.addSpacing(16)

        # Progress label
        self.progress_label = QLabel("0%")
        self.progress_label.setFixedWidth(50)
        self.progress_label.setStyleSheet(f"color: {COLORS['text']}; font-size: 14px; font-weight: bold;")
        ctrl_layout.addWidget(self.progress_label)

        ctrl_layout.addSpacing(16)

        # Loop toggle
        self.loop_btn = QPushButton("L")
        self.loop_btn.setFixedSize(50, 40)
        self.loop_btn.setCheckable(True)
        self.loop_btn.setChecked(True)
        self.loop_btn.setStyleSheet(btn_style)
        self.loop_btn.toggled.connect(lambda v: setattr(self, 'loop', v))
        ctrl_layout.addWidget(self.loop_btn)

        ctrl_layout.addSpacing(16)

        # Speed controls
        self._add_speed_controls(ctrl_layout)

        return controls

    def _create_training_controls(self) -> QWidget:
        """Create training mode controls."""
        controls = QWidget()
        controls.setFixedHeight(70)
        controls.setStyleSheet(f"background-color: {COLORS.get('panel', '#0d0d14')};")
        ctrl_layout = QHBoxLayout(controls)
        ctrl_layout.setContentsMargins(16, 8, 16, 8)

        btn_style = self._get_button_style()

        # Transport controls
        self.btn_reset = QPushButton("⏮")
        self.btn_reset.setFixedSize(45, 40)
        self.btn_reset.setStyleSheet(btn_style)
        self.btn_reset.setToolTip("Reset training")
        self.btn_reset.clicked.connect(self._reset_training)
        ctrl_layout.addWidget(self.btn_reset)

        self.btn_step = QPushButton("⏯")
        self.btn_step.setFixedSize(45, 40)
        self.btn_step.setStyleSheet(btn_style)
        self.btn_step.setToolTip("Step one epoch")
        self.btn_step.clicked.connect(self._step_training)
        ctrl_layout.addWidget(self.btn_step)

        self.play_btn = QPushButton("▶ Train")
        self.play_btn.setFixedSize(80, 40)
        self.play_btn.setStyleSheet(btn_style)
        self.play_btn.clicked.connect(self._toggle_training)
        ctrl_layout.addWidget(self.play_btn)

        ctrl_layout.addSpacing(16)

        # Epoch slider
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(0, 1000)
        self.slider.setValue(0)
        self.slider.setStyleSheet(self._get_slider_style())
        self.slider.setEnabled(False)  # Read-only during training
        ctrl_layout.addWidget(self.slider, stretch=1)

        ctrl_layout.addSpacing(16)

        # Epoch/Loss display
        info_layout = QVBoxLayout()
        info_layout.setSpacing(2)

        self.epoch_label = QLabel("Epoch: 0 / 1000")
        self.epoch_label.setStyleSheet(f"color: {COLORS['text']}; font-size: 12px; font-weight: bold;")
        info_layout.addWidget(self.epoch_label)

        self.loss_label = QLabel("Loss: --")
        self.loss_label.setStyleSheet(f"color: {COLORS['accent']}; font-size: 11px;")
        info_layout.addWidget(self.loss_label)

        self.accuracy_label = QLabel("Accuracy: --")
        self.accuracy_label.setStyleSheet(f"color: {COLORS['success']}; font-size: 11px;")
        info_layout.addWidget(self.accuracy_label)

        ctrl_layout.addLayout(info_layout)

        ctrl_layout.addSpacing(16)

        # Speed controls
        speed_label = QLabel("Speed:")
        speed_label.setStyleSheet(f"color: {COLORS['dim']}; font-size: 11px;")
        ctrl_layout.addWidget(speed_label)

        self.playback_speed = 1.0
        for speed, label in [(0.5, "Slow"), (1.0, "1x"), (2.0, "2x"), (4.0, "Fast")]:
            btn = QPushButton(label)
            btn.setFixedSize(45, 30)
            btn.setCheckable(True)
            btn.setChecked(speed == 1.0)
            btn.setStyleSheet(self._get_speed_btn_style())
            btn.clicked.connect(lambda checked, s=speed: self._set_training_speed(s))
            ctrl_layout.addWidget(btn)
            setattr(self, f'speed_btn_{str(speed).replace(".", "_")}', btn)

        return controls

    def _create_training_panel(self) -> QWidget:
        """Create the training parameters panel."""
        panel = QWidget()
        panel.setFixedWidth(280)
        panel.setStyleSheet(f"""
            QWidget {{
                background-color: {COLORS.get('panel', '#0d0d14')};
                color: {COLORS['text']};
            }}
            QGroupBox {{
                color: {COLORS['secondary']};
                font-weight: bold;
                border: 1px solid {COLORS['dim']};
                border-radius: 4px;
                margin-top: 10px;
                padding-top: 8px;
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                left: 8px;
                padding: 0 4px;
            }}
        """)

        layout = QVBoxLayout(panel)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(12)

        # Title
        title = QLabel("Training Controls")
        title.setStyleSheet(f"color: {COLORS['accent']}; font-size: 14px; font-weight: bold;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # Hyperparameters
        params_group = QGroupBox("Hyperparameters")
        params_layout = QFormLayout(params_group)
        params_layout.setSpacing(8)

        # Learning rate
        self.lr_spin = QDoubleSpinBox()
        self.lr_spin.setRange(0.001, 2.0)
        self.lr_spin.setDecimals(3)
        self.lr_spin.setSingleStep(0.01)
        self.lr_spin.setValue(0.5)
        self.lr_spin.valueChanged.connect(self._on_lr_changed)
        params_layout.addRow("Learning Rate:", self.lr_spin)

        # Momentum
        self.momentum_spin = QDoubleSpinBox()
        self.momentum_spin.setRange(0.0, 0.99)
        self.momentum_spin.setDecimals(2)
        self.momentum_spin.setSingleStep(0.05)
        self.momentum_spin.setValue(0.9)
        self.momentum_spin.valueChanged.connect(self._on_momentum_changed)
        params_layout.addRow("Momentum:", self.momentum_spin)

        # Dropout
        self.dropout_spin = QDoubleSpinBox()
        self.dropout_spin.setRange(0.0, 0.9)
        self.dropout_spin.setDecimals(2)
        self.dropout_spin.setSingleStep(0.05)
        self.dropout_spin.setValue(0.0)
        self.dropout_spin.valueChanged.connect(self._on_dropout_changed)
        params_layout.addRow("Dropout:", self.dropout_spin)

        layout.addWidget(params_group)

        # Network info
        network_group = QGroupBox("Network")
        network_layout = QFormLayout(network_group)

        self.network_label = QLabel("[2, 4, 1]")
        self.network_label.setStyleSheet(f"color: {COLORS['primary']};")
        network_layout.addRow("Architecture:", self.network_label)

        # Hidden size control
        self.hidden_spin = QSpinBox()
        self.hidden_spin.setRange(2, 16)
        self.hidden_spin.setValue(4)
        self.hidden_spin.valueChanged.connect(self._on_hidden_changed)
        network_layout.addRow("Hidden Size:", self.hidden_spin)

        layout.addWidget(network_group)

        # Training config
        config_group = QGroupBox("Training")
        config_layout = QFormLayout(config_group)

        self.epochs_spin = QSpinBox()
        self.epochs_spin.setRange(100, 10000)
        self.epochs_spin.setSingleStep(100)
        self.epochs_spin.setValue(1000)
        config_layout.addRow("Max Epochs:", self.epochs_spin)

        layout.addWidget(config_group)

        # Status
        self.status_label = QLabel("Ready - Click 'Train' or press S to step")
        self.status_label.setWordWrap(True)
        self.status_label.setStyleSheet(f"color: {COLORS['dim']}; font-size: 11px; padding: 8px;")
        layout.addWidget(self.status_label)

        layout.addStretch()

        return panel

    def _get_button_style(self) -> str:
        return f"""
            QPushButton {{
                background-color: {COLORS['bg_light']};
                color: {COLORS['text']};
                border: 1px solid {COLORS['dim']};
                border-radius: 4px;
                font-size: 16px;
                font-weight: bold;
            }}
            QPushButton:hover {{ background-color: {COLORS['primary']}; }}
            QPushButton:checked {{ background-color: {COLORS['accent']}; }}
        """

    def _get_speed_btn_style(self) -> str:
        return f"""
            QPushButton {{
                background-color: {COLORS['bg_light']};
                color: {COLORS['text']};
                border: 1px solid {COLORS['dim']};
                border-radius: 4px;
                font-size: 11px;
            }}
            QPushButton:hover {{ background-color: {COLORS['primary']}; }}
            QPushButton:checked {{ background-color: {COLORS['accent']}; color: white; }}
        """

    def _get_slider_style(self) -> str:
        return f"""
            QSlider::groove:horizontal {{
                background: {COLORS['bg_light']};
                height: 8px;
                border-radius: 4px;
            }}
            QSlider::handle:horizontal {{
                background: {COLORS['primary']};
                width: 18px;
                margin: -5px 0;
                border-radius: 9px;
            }}
            QSlider::sub-page:horizontal {{
                background: {COLORS['primary']};
                border-radius: 4px;
            }}
        """

    def _add_speed_controls(self, layout):
        """Add speed control buttons to layout."""
        self.playback_speed = 1.0
        speed_label = QLabel("Speed:")
        speed_label.setStyleSheet(f"color: {COLORS['dim']}; font-size: 12px;")
        layout.addWidget(speed_label)

        speed_btn_style = self._get_speed_btn_style()

        self.speed_05 = QPushButton("0.5x")
        self.speed_05.setCheckable(True)
        self.speed_05.setStyleSheet(speed_btn_style)
        self.speed_05.clicked.connect(lambda: self._set_speed(0.5))
        layout.addWidget(self.speed_05)

        self.speed_1 = QPushButton("1x")
        self.speed_1.setCheckable(True)
        self.speed_1.setChecked(True)
        self.speed_1.setStyleSheet(speed_btn_style)
        self.speed_1.clicked.connect(lambda: self._set_speed(1.0))
        layout.addWidget(self.speed_1)

        self.speed_2 = QPushButton("2x")
        self.speed_2.setCheckable(True)
        self.speed_2.setStyleSheet(speed_btn_style)
        self.speed_2.clicked.connect(lambda: self._set_speed(2.0))
        layout.addWidget(self.speed_2)

    def _setup_timer(self):
        self.timer = QTimer(self)
        self.timer.timeout.connect(self._tick)
        self.timer.setInterval(33)  # ~30fps

    # Standard animation controls
    def _set_speed(self, speed: float):
        self.playback_speed = speed
        self.speed_05.setChecked(speed == 0.5)
        self.speed_1.setChecked(speed == 1.0)
        self.speed_2.setChecked(speed == 2.0)

    def _toggle_play(self):
        self.playing = not self.playing
        self.play_btn.setText("||" if self.playing else ">")
        if self.playing:
            self.timer.start()
        else:
            self.timer.stop()

    def _reset(self):
        self.progress = 0.0
        self.slider.setValue(0)
        self._render()

    def _on_slider_change(self, value):
        self.progress = value / 1000.0
        self.progress_label.setText(f"{int(self.progress * 100)}%")
        self._render()

    def _tick(self):
        if self.training_mode:
            self._training_tick()
        else:
            self._animation_tick()

    def _animation_tick(self):
        self.progress += 0.015 * self.playback_speed
        if self.progress >= 1.0:
            if self.loop:
                self.progress = 0.0
            else:
                self.progress = 1.0
                self.playing = False
                self.play_btn.setText(">")
                self.timer.stop()

        self.slider.blockSignals(True)
        self.slider.setValue(int(self.progress * 1000))
        self.slider.blockSignals(False)
        self.progress_label.setText(f"{int(self.progress * 100)}%")
        self._render()

    # Training mode controls
    def _init_trainer(self):
        """Initialize the live trainer."""
        from core.live_training import create_xor_trainer

        hidden_size = self.hidden_spin.value() if hasattr(self, 'hidden_spin') else 4
        lr = self.lr_spin.value() if hasattr(self, 'lr_spin') else 0.5

        self.trainer = create_xor_trainer(hidden_size=hidden_size, learning_rate=lr)
        # No callback - we poll the queue instead for thread safety

        # Update network label (simpler architecture now: 2 -> hidden -> 1)
        if hasattr(self, 'network_label'):
            self.network_label.setText(f"[2, {hidden_size}, 1]")

    def _toggle_training(self):
        if self.trainer is None:
            self._init_trainer()

        if self.trainer.is_running and not self.trainer.is_paused:
            # Pause
            self.trainer.pause()
            self.play_btn.setText("▶ Train")
            self.status_label.setText("Paused")
        elif self.trainer.is_running and self.trainer.is_paused:
            # Resume
            self.trainer.resume()
            self.play_btn.setText("⏸ Pause")
            self.status_label.setText("Training...")
        else:
            # Start
            epochs = self.epochs_spin.value() if hasattr(self, 'epochs_spin') else 1000
            speed = 30 * self.playback_speed  # epochs per second
            self.trainer.start(epochs=epochs, epochs_per_second=speed)
            self.play_btn.setText("⏸ Pause")
            self.status_label.setText("Training...")
            self.timer.start()

    def _reset_training(self):
        """Reset training to beginning."""
        if self.trainer:
            self.trainer.reset()
        self._init_trainer()
        self.training_state = None
        self.slider.setValue(0)
        self.epoch_label.setText("Epoch: 0 / 1000")
        self.loss_label.setText("Loss: --")
        self.accuracy_label.setText("Accuracy: --")
        self.status_label.setText("Reset - Click 'Train' to start")
        self.play_btn.setText("▶ Train")
        self._render()

    def _step_training(self):
        """Perform a batch of training steps (like original presentation)."""
        if self.trainer is None:
            self._init_trainer()

        # Train 10 epochs at a time like the original
        state = self.trainer.train_batch(num_epochs=10)
        if state:
            self.training_state = state
            self._update_training_ui(state)
            self._render()

    def _set_training_speed(self, speed: float):
        """Set training speed."""
        self.playback_speed = speed
        for s in [0.5, 1.0, 2.0, 4.0]:
            btn = getattr(self, f'speed_btn_{str(s).replace(".", "_")}', None)
            if btn:
                btn.setChecked(s == speed)

        # Update trainer speed if running
        if self.trainer and self.trainer.is_running:
            # We'd need to restart with new speed
            pass

    def _on_lr_changed(self, value):
        if self.trainer:
            self.trainer.set_hyperparameters(learning_rate=value)

    def _on_momentum_changed(self, value):
        if self.trainer:
            self.trainer.set_hyperparameters(momentum=value)

    def _on_dropout_changed(self, value):
        if self.trainer:
            self.trainer.set_hyperparameters(dropout_rate=value)

    def _on_hidden_changed(self, value):
        """Hidden size changed - need to reset network."""
        if hasattr(self, 'network_label'):
            self.network_label.setText(f"[2, {value}, 1]")
        self.status_label.setText("Hidden size changed - click Reset to apply")

    def _update_training_ui(self, state: TrainingState):
        """Update UI elements with training state."""
        self.slider.blockSignals(True)
        progress = state.epoch / max(state.total_epochs, 1)
        self.slider.setValue(int(progress * 1000))
        self.slider.blockSignals(False)

        self.epoch_label.setText(f"Epoch: {state.epoch} / {state.total_epochs}")
        self.loss_label.setText(f"Loss: {state.loss:.4f}")

        accuracy = state.metrics.get('accuracy', 0)
        self.accuracy_label.setText(f"Accuracy: {accuracy:.1%}")

        # Check if training finished
        if self.trainer and not self.trainer.is_running:
            self.play_btn.setText("▶ Train")
            self.status_label.setText(f"Finished at epoch {state.epoch}")
            if accuracy >= 0.99:
                self.status_label.setText(f"Converged at epoch {state.epoch}!")

    def _training_tick(self):
        """Timer tick for training mode - polls queue for thread-safe updates."""
        if self.trainer:
            # Poll the state queue (thread-safe)
            state = self.trainer.get_latest_state()
            if state:
                self.training_state = state
                self._update_training_ui(state)
                self._render()
            elif self.training_state:
                # No new state but we have old one - just check if finished
                if not self.trainer.is_running:
                    self._update_training_ui(self.training_state)

    def _render(self):
        """Render the current frame using centralized renderer."""
        step_with_title = dict(self.step_data)
        if not step_with_title.get('title'):
            step_with_title['title'] = self.step_name

        # Inject training state into elements if in training mode
        if self.training_mode and self.training_state:
            elements = []
            for elem in step_with_title.get('elements', []):
                elem_copy = dict(elem)
                elem_type = elem_copy.get('type', '')

                # Inject training data
                if elem_type == 'loss_curve':
                    elem_copy['values'] = self.training_state.loss_history
                    if self.training_state.metrics_history.get('accuracy'):
                        elem_copy['val_values'] = []  # Could add validation loss
                elif elem_type in ('decision_boundary_2d', 'xor_problem'):
                    if self.training_state.decision_boundary is not None:
                        elem_copy['decision_boundary'] = self.training_state.decision_boundary
                    elem_copy['epoch'] = self.training_state.epoch
                    elem_copy['total_epochs'] = self.training_state.total_epochs
                elif elem_type == 'gradient_flow':
                    if self.training_state.gradients:
                        grads = list(self.training_state.gradients.values())
                        elem_copy['gradient_magnitudes'] = grads
                elif elem_type == 'dropout_layer':
                    elem_copy['dropout_rate'] = self.training_state.hyperparameters.get('dropout_rate', 0)
                    # Use epoch as seed for different dropout patterns
                    elem_copy['seed'] = self.training_state.epoch

                elements.append(elem_copy)
            step_with_title['elements'] = elements

        # Determine progress
        if self.training_mode and self.training_state:
            progress = self.training_state.epoch / max(self.training_state.total_epochs, 1)
        else:
            progress = self.progress

        render_step(
            self.ax,
            step_with_title,
            progress,
            colors=COLORS,
            show_title=True,
            show_phase_markers=not self.training_mode
        )
        self.canvas.draw_idle()

    def keyPressEvent(self, event):
        """Handle keyboard shortcuts."""
        if event.key() == Qt.Key_Space:
            if self.training_mode:
                self._toggle_training()
            else:
                self._toggle_play()
        elif event.key() == Qt.Key_R:
            if self.training_mode:
                self._reset_training()
            else:
                self._reset()
        elif event.key() == Qt.Key_S:
            if self.training_mode:
                self._step_training()
        elif event.key() in (Qt.Key_Escape, Qt.Key_Q):
            self.close()
        else:
            super().keyPressEvent(event)

    def showEvent(self, event):
        super().showEvent(event)
        self.setFocus()
        self.activateWindow()

    def closeEvent(self, event):
        self.timer.stop()
        if self.trainer:
            self.trainer.stop()
        super().closeEvent(event)
