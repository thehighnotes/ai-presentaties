"""
Animation preview window for the Qt Designer.
Uses the centralized element rendering from core/element_rendering.py.
"""

from typing import Dict

from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QSlider, QLabel
from PySide6.QtCore import Qt, QTimer

# Matplotlib with Qt backend
import matplotlib
matplotlib.use('QtAgg')
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from core.element_rendering import render_step, COLORS


class PreviewWindow(QWidget):
    """Animation preview window using matplotlib."""

    def __init__(self, step_data: Dict, step_name: str, parent=None):
        super().__init__(parent, Qt.Window)  # Make it a separate window
        self.step_data = step_data
        self.step_name = step_name
        self.progress = 0.0
        self.playing = False
        self.loop = True

        self.setWindowTitle(f"Preview: {step_name}")
        self.setMinimumSize(900, 700)
        self.setStyleSheet(f"background-color: {COLORS['bg']};")

        # Enable keyboard focus
        self.setFocusPolicy(Qt.StrongFocus)

        self._setup_ui()
        self._setup_timer()
        self._render()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Matplotlib figure
        self.figure = Figure(figsize=(10, 7), facecolor=COLORS['bg'])
        self.canvas = FigureCanvas(self.figure)
        self.ax = self.figure.add_subplot(111)
        layout.addWidget(self.canvas, stretch=1)

        # Controls bar
        controls = QWidget()
        controls.setFixedHeight(60)
        controls.setStyleSheet(f"background-color: {COLORS.get('panel', '#0d0d14')};")
        ctrl_layout = QHBoxLayout(controls)
        ctrl_layout.setContentsMargins(16, 8, 16, 8)

        btn_style = f"""
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
        self.slider.setStyleSheet(f"""
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
        """)
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

        layout.addWidget(controls)

    def _setup_timer(self):
        self.timer = QTimer(self)
        self.timer.timeout.connect(self._tick)
        self.timer.setInterval(33)  # ~30fps

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
        self.progress += 0.015
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

    def _render(self):
        """Render the current frame using centralized renderer."""
        # Use the step name as title if step doesn't have one
        step_with_title = dict(self.step_data)
        if not step_with_title.get('title'):
            step_with_title['title'] = self.step_name

        render_step(
            self.ax,
            step_with_title,
            self.progress,
            colors=COLORS,
            show_title=True,
            show_phase_markers=True
        )
        self.canvas.draw_idle()

    def keyPressEvent(self, event):
        """Handle keyboard shortcuts."""
        if event.key() == Qt.Key_Space:
            self._toggle_play()
        elif event.key() == Qt.Key_R:
            self._reset()
        elif event.key() in (Qt.Key_Escape, Qt.Key_Q):
            self.close()
        else:
            super().keyPressEvent(event)

    def showEvent(self, event):
        """Grab focus when shown."""
        super().showEvent(event)
        self.setFocus()
        self.activateWindow()

    def closeEvent(self, event):
        """Stop timer on close."""
        self.timer.stop()
        super().closeEvent(event)
