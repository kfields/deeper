import imgui

from deeper.window import GuiWindow
from deeper.dimgui import Window
from deeper.widgets import Selectable, SelectableGroup

class Sortable(SelectableGroup):
    def __init__(self, children, callback=lambda: None):
        super().__init__(children, callback)
        self.drag_index = -1
        self.dragging = None

    def draw(self):
        hovered_index = -1
        for i, child in enumerate(self.children):
            self.draw_child(child)            
            if imgui.is_item_hovered(imgui.HOVERED_RECT_ONLY):
                hovered_index = i

        if 0 <= hovered_index and self.dragging:
            if imgui.is_mouse_dragging():
                if hovered_index != self.drag_index:
                    self.swap(hovered_index, self.drag_index)
                    self.drag_index = hovered_index

        elif imgui.is_mouse_down(0):
            self.drag_index = hovered_index
            #self.dragging = True
            self.dragging = self.children[i]

        if not imgui.is_mouse_down(0) and self.dragging:
            self.drag_index = -1
            self.dragging = None

    def swap(self, i, j):
        self.children[i], self.children[j] = self.children[j], self.children[i]

cb = lambda: None

sortable = Sortable([
    Selectable('A', cb),
    Selectable('B', cb),
    Selectable('C', cb),
])

win = GuiWindow([Window('Sortable', [sortable])], title="Sortable Test")
win.run()
