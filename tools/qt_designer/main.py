"""
Main window for the Qt Designer.
PresentationDesigner: The main application window.
"""

import sys
import json
import copy
from pathlib import Path
from typing import Optional, Dict

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QFileDialog, QMessageBox, QStatusBar, QSplitter
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QAction, QKeySequence, QUndoStack

from .constants import COLORS, ELEMENT_DEFAULTS
from .commands import AddElementCommand, DeleteElementCommand
from .canvas import CanvasView, CanvasElement
from .palette import ElementPalette
from .properties import PropertiesPanel
from .navigator import StepNavigator
from .preview import PreviewWindow


class PresentationDesigner(QMainWindow):
    """Main application window."""

    def __init__(self, schema_path: Optional[str] = None):
        super().__init__()
        self.schema_path = schema_path
        self.schema = self._load_or_create_schema(schema_path)
        self.current_step = 0
        self._dirty = False
        self._clipboard = None

        # Undo stack
        self.undo_stack = QUndoStack(self)
        self.undo_stack.setUndoLimit(50)
        self.undo_stack.cleanChanged.connect(self._on_clean_changed)

        self._setup_ui()
        self._setup_menu()
        self._connect_signals()
        self._load_step(0)

    def _load_or_create_schema(self, path: Optional[str]) -> Dict:
        if path and Path(path).exists():
            with open(path) as f:
                return json.load(f)
        return {
            'name': 'new_presentation',
            'title': 'New Presentation',
            'landing': {
                'title': 'New Presentation',
                'subtitle': 'Created with Qt Designer',
                'tagline': 'Press SPACE to begin'
            },
            'steps': [{'name': 'Step 1', 'title': 'Introduction', 'elements': [], 'animation_frames': 60}]
        }

    def _setup_ui(self):
        self._update_title()
        self.setMinimumSize(1280, 800)

        # Dark theme
        self.setStyleSheet(f"""
            QMainWindow, QWidget {{
                background-color: {COLORS['bg']};
                color: {COLORS['text']};
            }}
            QGroupBox {{
                color: {COLORS['secondary']};
                font-weight: bold;
                border: 1px solid {COLORS['dim']};
                border-radius: 4px;
                margin-top: 12px;
                padding-top: 8px;
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
            }}
            QSpinBox, QDoubleSpinBox, QLineEdit, QComboBox, QPlainTextEdit {{
                background-color: {COLORS['bg_light']};
                border: 1px solid {COLORS['dim']};
                border-radius: 4px;
                padding: 4px 8px;
                color: {COLORS['text']};
                min-height: 24px;
            }}
            QSpinBox:focus, QDoubleSpinBox:focus, QLineEdit:focus, QComboBox:focus {{
                border-color: {COLORS['primary']};
            }}
            QComboBox::drop-down {{
                border: none;
                width: 20px;
            }}
            QComboBox::down-arrow {{
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 6px solid {COLORS['text']};
                margin-right: 5px;
            }}
            QScrollBar:vertical {{
                background: {COLORS['bg_light']};
                width: 12px;
                border-radius: 6px;
            }}
            QScrollBar::handle:vertical {{
                background: {COLORS['dim']};
                border-radius: 6px;
                min-height: 20px;
            }}
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
                height: 0;
            }}
            QCheckBox::indicator {{
                width: 18px;
                height: 18px;
                border: 2px solid {COLORS['dim']};
                border-radius: 4px;
                background: {COLORS['bg_light']};
            }}
            QCheckBox::indicator:checked {{
                background: {COLORS['success']};
                border-color: {COLORS['success']};
            }}
        """)

        # Central widget
        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QVBoxLayout(central)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Content area with resizable splitter
        splitter = QSplitter(Qt.Horizontal)
        splitter.setHandleWidth(4)
        splitter.setStyleSheet(f"""
            QSplitter::handle {{
                background-color: {COLORS['dim']};
            }}
            QSplitter::handle:hover {{
                background-color: {COLORS['primary']};
            }}
        """)

        # Left: Element palette
        self.palette = ElementPalette()
        splitter.addWidget(self.palette)

        # Center: Canvas
        self.canvas = CanvasView(self.undo_stack)
        splitter.addWidget(self.canvas)

        # Right: Properties
        self.properties = PropertiesPanel()
        splitter.addWidget(self.properties)

        # Set initial sizes (palette: 120, canvas: stretch, properties: 300)
        splitter.setSizes([120, 800, 300])
        splitter.setStretchFactor(0, 0)  # Palette doesn't stretch
        splitter.setStretchFactor(1, 1)  # Canvas stretches
        splitter.setStretchFactor(2, 0)  # Properties doesn't stretch

        main_layout.addWidget(splitter, stretch=1)

        # Bottom: Step navigator
        self.navigator = StepNavigator()
        self._update_navigator()
        main_layout.addWidget(self.navigator)

        # Status bar
        self.statusBar().showMessage("Ready | Middle-click: pan | Scroll: zoom | Arrow keys: nudge")
        self.statusBar().setStyleSheet(f"color: {COLORS['dim']}; padding: 4px;")

    def _update_title(self):
        """Update window title with dirty indicator."""
        name = self.schema.get('name', 'Untitled')
        dirty = '*' if self._dirty else ''
        self.setWindowTitle(f"Presentation Designer - {name}{dirty}")

    def _mark_dirty(self):
        """Mark the document as dirty (unsaved changes)."""
        if not self._dirty:
            self._dirty = True
            self._update_title()

    def _on_clean_changed(self, clean):
        """Called when undo stack clean state changes."""
        # If undo stack is clean (no undoable changes), mark as clean
        if clean:
            self._dirty = False
            self._update_title()

    def _setup_menu(self):
        menubar = self.menuBar()
        menubar.setStyleSheet(f"""
            QMenuBar {{
                background-color: {COLORS.get('panel', '#0d0d14')};
                color: {COLORS['text']};
                padding: 4px;
            }}
            QMenuBar::item:selected {{
                background-color: {COLORS['primary']};
            }}
            QMenu {{
                background-color: {COLORS['bg_light']};
                color: {COLORS['text']};
                border: 1px solid {COLORS['dim']};
            }}
            QMenu::item:selected {{
                background-color: {COLORS['primary']};
            }}
        """)

        # File menu
        file_menu = menubar.addMenu("&File")

        new_action = QAction("&New", self)
        new_action.setShortcut(QKeySequence.New)
        new_action.triggered.connect(self._new_presentation)
        file_menu.addAction(new_action)

        open_action = QAction("&Open...", self)
        open_action.setShortcut(QKeySequence.Open)
        open_action.triggered.connect(self._open_file)
        file_menu.addAction(open_action)

        save_action = QAction("&Save", self)
        save_action.setShortcut(QKeySequence.Save)
        save_action.triggered.connect(self._save_file)
        file_menu.addAction(save_action)

        file_menu.addSeparator()

        generate_action = QAction("&Generate Python...", self)
        generate_action.setShortcut("Ctrl+G")
        generate_action.triggered.connect(self._generate_python)
        file_menu.addAction(generate_action)

        file_menu.addSeparator()

        quit_action = QAction("&Quit", self)
        quit_action.setShortcut(QKeySequence.Quit)
        quit_action.triggered.connect(self.close)
        file_menu.addAction(quit_action)

        # Edit menu
        edit_menu = menubar.addMenu("&Edit")

        undo_action = QAction("&Undo", self)
        undo_action.setShortcut(QKeySequence.Undo)
        undo_action.triggered.connect(self.undo_stack.undo)
        edit_menu.addAction(undo_action)

        redo_action = QAction("&Redo", self)
        redo_action.setShortcut(QKeySequence.Redo)
        redo_action.triggered.connect(self.undo_stack.redo)
        edit_menu.addAction(redo_action)

        edit_menu.addSeparator()

        copy_action = QAction("&Copy", self)
        copy_action.setShortcut(QKeySequence.Copy)
        copy_action.triggered.connect(self._copy_selected)
        edit_menu.addAction(copy_action)

        paste_action = QAction("&Paste", self)
        paste_action.setShortcut(QKeySequence.Paste)
        paste_action.triggered.connect(self._paste)
        edit_menu.addAction(paste_action)

        edit_menu.addSeparator()

        delete_action = QAction("&Delete Element", self)
        delete_action.setShortcut(QKeySequence.Delete)
        delete_action.triggered.connect(self._delete_selected)
        edit_menu.addAction(delete_action)

        duplicate_action = QAction("D&uplicate", self)
        duplicate_action.setShortcut("Ctrl+D")
        duplicate_action.triggered.connect(self._duplicate_selected)
        edit_menu.addAction(duplicate_action)

        edit_menu.addSeparator()

        # Z-order controls
        bring_front = QAction("Bring to &Front", self)
        bring_front.setShortcut("Ctrl+Shift+]")
        bring_front.triggered.connect(lambda: self._change_z_order('front'))
        edit_menu.addAction(bring_front)

        bring_forward = QAction("Bring For&ward", self)
        bring_forward.setShortcut("Ctrl+]")
        bring_forward.triggered.connect(lambda: self._change_z_order('forward'))
        edit_menu.addAction(bring_forward)

        send_backward = QAction("Send Back&ward", self)
        send_backward.setShortcut("Ctrl+[")
        send_backward.triggered.connect(lambda: self._change_z_order('backward'))
        edit_menu.addAction(send_backward)

        send_back = QAction("Send to &Back", self)
        send_back.setShortcut("Ctrl+Shift+[")
        send_back.triggered.connect(lambda: self._change_z_order('back'))
        edit_menu.addAction(send_back)

        # View menu
        view_menu = menubar.addMenu("&View")

        zoom_in = QAction("Zoom &In", self)
        zoom_in.setShortcut("Ctrl+=")
        zoom_in.triggered.connect(lambda: self.canvas.scale(1.15, 1.15))
        view_menu.addAction(zoom_in)

        zoom_out = QAction("Zoom &Out", self)
        zoom_out.setShortcut("Ctrl+-")
        zoom_out.triggered.connect(lambda: self.canvas.scale(1/1.15, 1/1.15))
        view_menu.addAction(zoom_out)

        zoom_reset = QAction("&Reset Zoom", self)
        zoom_reset.setShortcut("Ctrl+0")
        zoom_reset.triggered.connect(self._reset_zoom)
        view_menu.addAction(zoom_reset)

        view_menu.addSeparator()

        snap_action = QAction("Snap to &Grid", self)
        snap_action.setShortcut("G")
        snap_action.setCheckable(True)
        snap_action.triggered.connect(self._toggle_snap)
        view_menu.addAction(snap_action)
        self._snap_action = snap_action

        view_menu.addSeparator()

        preview_action = QAction("&Preview Animation", self)
        preview_action.setShortcut("P")
        preview_action.triggered.connect(self._show_preview)
        view_menu.addAction(preview_action)

    def _connect_signals(self):
        self.palette.element_clicked.connect(self._add_element)
        self.canvas.element_selected.connect(self.properties.set_element)
        self.canvas.element_deselected.connect(lambda: self.properties.set_element(None))
        self.properties.property_changed.connect(self._on_property_changed)
        self.navigator.step_changed.connect(self._load_step)
        self.navigator.step_added.connect(self._add_step)
        self.navigator.step_removed.connect(self._remove_step)
        self.navigator.step_renamed.connect(self._rename_step)

    def _update_navigator(self):
        names = [s.get('name', f'Step {i+1}') for i, s in enumerate(self.schema['steps'])]
        self.navigator.set_steps(self.current_step, len(self.schema['steps']), names)

    def _load_step(self, step_idx: int):
        self.current_step = step_idx
        self.canvas.clear_elements()

        if 0 <= step_idx < len(self.schema['steps']):
            step = self.schema['steps'][step_idx]
            for elem in step.get('elements', []):
                self.canvas.add_element(elem)
            self._update_navigator()
            self.statusBar().showMessage(f"Loaded: {step.get('name', 'Untitled')}")

    def _add_element(self, elem_type: str):
        defaults = copy.deepcopy(ELEMENT_DEFAULTS.get(elem_type, {}))
        elem_data = {
            'type': elem_type,
            'position': {'x': 50, 'y': 50},
            'animation_phase': 'early',
            **defaults
        }

        step_elements = self.schema['steps'][self.current_step]['elements']
        item = self.canvas.add_element(elem_data)

        # Undo command
        cmd = AddElementCommand(self.canvas.scene_obj, step_elements, elem_data, item)
        self.undo_stack.push(cmd)
        self._mark_dirty()

        item.setSelected(True)
        self.statusBar().showMessage(f"Added {elem_type}")

    def _on_property_changed(self, prop: str, value):
        item = self.canvas.get_selected_item()
        if not item:
            return

        self._mark_dirty()

        if prop in ('x', 'y'):
            if 'position' not in item.elem_data:
                item.elem_data['position'] = {}
            item.elem_data['position'][prop] = value
            item._update_visual_position()
        elif prop in ('start_x', 'start_y'):
            key = 'start'
            if key not in item.elem_data:
                item.elem_data[key] = {'x': 30, 'y': 50}
            item.elem_data[key][prop.split('_')[1]] = value
        elif prop in ('end_x', 'end_y'):
            key = 'end'
            if key not in item.elem_data:
                item.elem_data[key] = {'x': 70, 'y': 50}
            item.elem_data[key][prop.split('_')[1]] = value
        elif prop == 'layers':
            try:
                layers = [int(x.strip()) for x in value.split(',')]
                item.elem_data['layers'] = layers
            except ValueError:
                pass
        else:
            item.elem_data[prop] = value

        item.update()

    def _delete_selected(self):
        item = self.canvas.get_selected_item()
        if item:
            step_elements = self.schema['steps'][self.current_step]['elements']
            cmd = DeleteElementCommand(self.canvas.scene_obj, step_elements, item.elem_data, item)
            self.undo_stack.push(cmd)
            self._mark_dirty()
            self.properties.set_element(None)

    def _copy_selected(self):
        """Copy selected element to clipboard."""
        item = self.canvas.get_selected_item()
        if item:
            self._clipboard = copy.deepcopy(item.elem_data)
            self.statusBar().showMessage("Copied element")

    def _paste(self):
        """Paste element from clipboard."""
        if self._clipboard:
            new_data = copy.deepcopy(self._clipboard)
            # Offset position
            new_data['position']['x'] = min(95, new_data['position']['x'] + 5)
            new_data['position']['y'] = max(5, new_data['position']['y'] - 5)

            step_elements = self.schema['steps'][self.current_step]['elements']
            new_item = self.canvas.add_element(new_data)

            cmd = AddElementCommand(self.canvas.scene_obj, step_elements, new_data, new_item)
            self.undo_stack.push(cmd)
            self._mark_dirty()

            new_item.setSelected(True)
            self.statusBar().showMessage("Pasted element")

    def _duplicate_selected(self):
        item = self.canvas.get_selected_item()
        if item:
            new_data = copy.deepcopy(item.elem_data)
            new_data['position']['x'] = min(95, new_data['position']['x'] + 5)
            new_data['position']['y'] = max(5, new_data['position']['y'] - 5)

            step_elements = self.schema['steps'][self.current_step]['elements']
            new_item = self.canvas.add_element(new_data)

            cmd = AddElementCommand(self.canvas.scene_obj, step_elements, new_data, new_item)
            self.undo_stack.push(cmd)
            self._mark_dirty()

            item.setSelected(False)
            new_item.setSelected(True)

    def _change_z_order(self, direction: str):
        """Change z-order of selected element."""
        item = self.canvas.get_selected_item()
        if not item:
            return

        step_elements = self.schema['steps'][self.current_step]['elements']
        elem_data = item.elem_data

        try:
            idx = step_elements.index(elem_data)
        except ValueError:
            return

        new_idx = idx
        if direction == 'front':
            new_idx = len(step_elements) - 1
        elif direction == 'back':
            new_idx = 0
        elif direction == 'forward' and idx < len(step_elements) - 1:
            new_idx = idx + 1
        elif direction == 'backward' and idx > 0:
            new_idx = idx - 1

        if new_idx != idx:
            # Move element in list
            step_elements.pop(idx)
            step_elements.insert(new_idx, elem_data)

            # Update canvas z-order
            self.canvas.update_z_order()
            self._mark_dirty()
            self.statusBar().showMessage(f"Moved element {direction}")

    def _toggle_snap(self, enabled: bool):
        """Toggle snap-to-grid."""
        self.canvas.set_snap_enabled(enabled)
        state = "enabled" if enabled else "disabled"
        self.statusBar().showMessage(f"Snap to grid {state}")

    def _add_step(self):
        idx = len(self.schema['steps']) + 1
        self.schema['steps'].append({
            'name': f'Step {idx}',
            'title': f'New Step {idx}',
            'elements': [],
            'animation_frames': 60
        })
        self._mark_dirty()
        self._update_navigator()

    def _remove_step(self):
        if len(self.schema['steps']) <= 1:
            QMessageBox.warning(self, "Warning", "Cannot remove the last step.")
            return
        self.schema['steps'].pop(self.current_step)
        self._mark_dirty()
        if self.current_step >= len(self.schema['steps']):
            self.current_step = len(self.schema['steps']) - 1
        self._load_step(self.current_step)

    def _rename_step(self, idx: int, name: str):
        if 0 <= idx < len(self.schema['steps']):
            self.schema['steps'][idx]['name'] = name
            self._mark_dirty()

    def _reset_zoom(self):
        self.canvas.resetTransform()
        self.canvas.zoom_level = 1.0

    def _show_preview(self):
        """Open the animation preview window."""
        if 0 <= self.current_step < len(self.schema['steps']):
            step = self.schema['steps'][self.current_step]
            step_name = step.get('name', f'Step {self.current_step + 1}')
            self.preview_window = PreviewWindow(step, step_name, self)
            self.preview_window.show()

    def _new_presentation(self):
        if self._dirty:
            reply = QMessageBox.question(
                self, "Unsaved Changes",
                "You have unsaved changes. Create new anyway?",
                QMessageBox.Yes | QMessageBox.No
            )
            if reply != QMessageBox.Yes:
                return

        self.schema = {
            'name': 'new_presentation',
            'title': 'New Presentation',
            'landing': {
                'title': 'New Presentation',
                'subtitle': 'Created with Qt Designer',
                'tagline': 'Press SPACE to begin'
            },
            'steps': [{'name': 'Step 1', 'title': 'Introduction', 'elements': [], 'animation_frames': 60}]
        }
        self.schema_path = None
        self.current_step = 0
        self.undo_stack.clear()
        self._dirty = False
        self._load_step(0)
        self._update_title()

    def _open_file(self):
        if self._dirty:
            reply = QMessageBox.question(
                self, "Unsaved Changes",
                "You have unsaved changes. Open anyway?",
                QMessageBox.Yes | QMessageBox.No
            )
            if reply != QMessageBox.Yes:
                return

        path, _ = QFileDialog.getOpenFileName(self, "Open Schema", "schemas/", "JSON Files (*.json)")
        if path:
            with open(path) as f:
                self.schema = json.load(f)
            self.schema_path = path
            self.current_step = 0
            self.undo_stack.clear()
            self._dirty = False
            self._load_step(0)
            self._update_title()

    def _save_file(self):
        if not self.schema_path:
            path, _ = QFileDialog.getSaveFileName(self, "Save Schema", "schemas/", "JSON Files (*.json)")
            if not path:
                return
            if not path.endswith('.json'):
                path += '.json'
            self.schema_path = path

        with open(self.schema_path, 'w') as f:
            json.dump(self.schema, f, indent=2)

        self._dirty = False
        self.undo_stack.setClean()
        self._update_title()
        self.statusBar().showMessage(f"Saved: {self.schema_path}")

    def _generate_python(self):
        if not self.schema_path:
            QMessageBox.warning(self, "Warning", "Save the schema first.")
            return

        try:
            # Use the V2 generator with centralized rendering
            from tools.generator_v2 import generate_from_json
            output_path = generate_from_json(self.schema_path)
            QMessageBox.information(self, "Generated", f"Python file generated:\n{output_path}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Generation failed:\n{e}")

    def closeEvent(self, event):
        """Prompt for save on close if dirty."""
        if self._dirty:
            reply = QMessageBox.question(
                self, "Unsaved Changes",
                "You have unsaved changes. Save before closing?",
                QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel
            )
            if reply == QMessageBox.Save:
                self._save_file()
                event.accept()
            elif reply == QMessageBox.Discard:
                event.accept()
            else:
                event.ignore()
        else:
            event.accept()


def main():
    app = QApplication(sys.argv)

    # Set application-wide font
    font = QFont('sans-serif', 10)
    app.setFont(font)

    schema_path = sys.argv[1] if len(sys.argv) > 1 else None
    window = PresentationDesigner(schema_path)
    window.show()

    sys.exit(app.exec())


if __name__ == '__main__':
    main()
