"""
Element palette for the Qt Designer.
Left sidebar with clickable element types.
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QScrollArea, QLabel, QPushButton
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont

from .constants import COLORS, ELEMENTS


class ElementPalette(QWidget):
    """Left panel with clickable element types."""

    element_clicked = Signal(str)

    def __init__(self):
        super().__init__()
        self.setFixedWidth(160)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(4)

        # Header
        header = QLabel("ELEMENTS")
        header.setFont(QFont('sans-serif', 11, QFont.Bold))
        header.setStyleSheet(f"color: {COLORS['accent']};")
        header.setAlignment(Qt.AlignCenter)
        layout.addWidget(header)

        # Scrollable element list
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setStyleSheet("QScrollArea { border: none; background: transparent; }")

        container = QWidget()
        container_layout = QVBoxLayout(container)
        container_layout.setSpacing(3)

        for elem_type, name, icon in ELEMENTS:
            btn = QPushButton(f" {icon}  {name}")
            btn.setFixedHeight(32)
            btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: {COLORS['bg_light']};
                    color: {COLORS['text']};
                    border: 1px solid {COLORS['dim']};
                    border-radius: 4px;
                    text-align: left;
                    padding-left: 8px;
                    font-size: 11px;
                }}
                QPushButton:hover {{
                    background-color: {COLORS['primary']};
                    border-color: {COLORS['primary']};
                }}
            """)
            btn.clicked.connect(lambda checked, t=elem_type: self.element_clicked.emit(t))
            container_layout.addWidget(btn)

        container_layout.addStretch()
        scroll.setWidget(container)
        layout.addWidget(scroll)
