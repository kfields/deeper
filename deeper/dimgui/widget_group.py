import imgui

from . import Widget


class WidgetGroup(Widget):
    def __init__(self, children):
        super().__init__(children)
        self.drag_index = -1
        self.dragging = None

    def draw_sortable(self):
        hovered_index = -1
        for i, child in enumerate(self.children):
            self.draw_child(child)
            if imgui.is_item_hovered(imgui.HOVERED_RECT_ONLY):
                hovered_index = i

        if hovered_index > -1 and self.dragging:
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
