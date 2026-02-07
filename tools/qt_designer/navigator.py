"""
Step navigator for the Qt Designer.
Bottom bar for navigating between presentation steps.
"""

from typing import List

from PySide6.QtWidgets import (
    QWidget, QHBoxLayout, QPushButton, QLineEdit, QInputDialog
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont

from .constants import COLORS


class StepNavigator(QWidget):
    """Bottom bar for navigating between steps."""

    step_changed = Signal(int)
    step_added = Signal()
    step_removed = Signal()
    step_renamed = Signal(int, str)

    def __init__(self):
        super().__init__()
        self.setFixedHeight(50)
        self.setStyleSheet(f"background-color: {COLORS['panel']};")
        self.current_step = 0
        self.total_steps = 1
        self.step_names = ['Step 1']

        layout = QHBoxLayout(self)
        layout.setContentsMargins(16, 8, 16, 8)

        btn_style = f"""
            QPushButton {{
                background-color: {COLORS['bg_light']};
                color: {COLORS['text']};
                border: 1px solid {COLORS['dim']};
                border-radius: 4px;
                font-weight: bold;
                font-size: 14px;
            }}
            QPushButton:hover {{
                background-color: {COLORS['primary']};
            }}
        """

        # Previous button
        self.prev_btn = QPushButton("<")
        self.prev_btn.setFixedSize(40, 32)
        self.prev_btn.setStyleSheet(btn_style)
        self.prev_btn.clicked.connect(self._prev_step)
        layout.addWidget(self.prev_btn)

        # Add step
        self.add_btn = QPushButton("+")
        self.add_btn.setFixedSize(40, 32)
        self.add_btn.setStyleSheet(btn_style)
        self.add_btn.clicked.connect(self.step_added.emit)
        layout.addWidget(self.add_btn)

        # Remove step
        self.remove_btn = QPushButton("-")
        self.remove_btn.setFixedSize(40, 32)
        self.remove_btn.setStyleSheet(btn_style)
        self.remove_btn.clicked.connect(self.step_removed.emit)
        layout.addWidget(self.remove_btn)

        layout.addStretch()

        # Step label (clickable to rename)
        self.step_label = QPushButton("Step 1/1")
        self.step_label.setFont(QFont('sans-serif', 12, QFont.Bold))
        self.step_label.setStyleSheet(f"""
            QPushButton {{
                color: {COLORS['primary']};
                background: transparent;
                border: none;
                padding: 4px 12px;
            }}
            QPushButton:hover {{
                background-color: {COLORS['bg_light']};
                border-radius: 4px;
            }}
        """)
        self.step_label.clicked.connect(self._rename_step)
        layout.addWidget(self.step_label)

        layout.addStretch()

        # Next button
        self.next_btn = QPushButton(">")
        self.next_btn.setFixedSize(40, 32)
        self.next_btn.setStyleSheet(btn_style)
        self.next_btn.clicked.connect(self._next_step)
        layout.addWidget(self.next_btn)

    def _prev_step(self):
        if self.current_step > 0:
            self.current_step -= 1
            self.step_changed.emit(self.current_step)
            self._update_label()

    def _next_step(self):
        if self.current_step < self.total_steps - 1:
            self.current_step += 1
            self.step_changed.emit(self.current_step)
            self._update_label()

    def _rename_step(self):
        name, ok = QInputDialog.getText(
            self, "Rename Step", "Step name:",
            QLineEdit.Normal, self.step_names[self.current_step]
        )
        if ok and name:
            self.step_names[self.current_step] = name
            self.step_renamed.emit(self.current_step, name)
            self._update_label()

    def set_steps(self, current: int, total: int, names: List[str]):
        self.current_step = current
        self.total_steps = total
        self.step_names = names
        self._update_label()

    def _update_label(self):
        name = self.step_names[self.current_step] if self.current_step < len(self.step_names) else f'Step {self.current_step + 1}'
        self.step_label.setText(f"{name} ({self.current_step + 1}/{self.total_steps})")
