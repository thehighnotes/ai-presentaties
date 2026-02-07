"""
Undo/Redo commands for the Qt Designer.
Uses Qt's QUndoCommand system for proper undo stack support.
"""

from PySide6.QtGui import QUndoCommand


class MoveCommand(QUndoCommand):
    """Undo command for element movement."""

    def __init__(self, item, old_pos, new_pos):
        super().__init__("Move Element")
        self.item = item
        self.old_pos = old_pos
        self.new_pos = new_pos

    def redo(self):
        self.item.setPos(self.new_pos)
        self.item._sync_data_from_pos()

    def undo(self):
        self.item.setPos(self.old_pos)
        self.item._sync_data_from_pos()


class AddElementCommand(QUndoCommand):
    """Undo command for adding elements."""

    def __init__(self, scene, step_elements, elem_data, item):
        super().__init__(f"Add {elem_data.get('type', 'element')}")
        self.scene = scene
        self.step_elements = step_elements
        self.elem_data = elem_data
        self.item = item

    def redo(self):
        if self.elem_data not in self.step_elements:
            self.step_elements.append(self.elem_data)
        if self.item not in self.scene.items():
            self.scene.addItem(self.item)

    def undo(self):
        if self.elem_data in self.step_elements:
            self.step_elements.remove(self.elem_data)
        if self.item in self.scene.items():
            self.scene.removeItem(self.item)


class DeleteElementCommand(QUndoCommand):
    """Undo command for deleting elements."""

    def __init__(self, scene, step_elements, elem_data, item):
        super().__init__(f"Delete {elem_data.get('type', 'element')}")
        self.scene = scene
        self.step_elements = step_elements
        self.elem_data = elem_data
        self.item = item

    def redo(self):
        if self.elem_data in self.step_elements:
            self.step_elements.remove(self.elem_data)
        if self.item in self.scene.items():
            self.scene.removeItem(self.item)

    def undo(self):
        if self.elem_data not in self.step_elements:
            self.step_elements.append(self.elem_data)
        if self.item not in self.scene.items():
            self.scene.addItem(self.item)


class NudgeCommand(QUndoCommand):
    """Undo command for arrow key nudging."""

    def __init__(self, item, dx, dy):
        super().__init__("Nudge Element")
        self.item = item
        self.dx = dx
        self.dy = dy

    def redo(self):
        pos = self.item.elem_data.get('position', {'x': 50, 'y': 50})
        pos['x'] = max(0, min(100, pos['x'] + self.dx))
        pos['y'] = max(0, min(100, pos['y'] + self.dy))
        self.item.elem_data['position'] = pos
        self.item._update_visual_position()

    def undo(self):
        pos = self.item.elem_data.get('position', {'x': 50, 'y': 50})
        pos['x'] = max(0, min(100, pos['x'] - self.dx))
        pos['y'] = max(0, min(100, pos['y'] - self.dy))
        self.item.elem_data['position'] = pos
        self.item._update_visual_position()
