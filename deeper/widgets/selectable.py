import imgui

from deeper.dimgui import Widget

class Selectable(Widget):
    def __init__(self, label, callback, selected=False):
        super().__init__()
        self.label = label
        self.callback = callback
        self.selected = selected

    def draw(self):
        clicked, selected = imgui.selectable(self.label, self.selected)
        if selected:
            self.selected = selected
            self.callback()

class SelectableGroup(Widget):
    def __init__(self, children, callback=lambda: None):
        super().__init__(children)
        self.callback = callback

    def add_child(self, child):
        super().add_child(child)
        child_callback = child.callback
        child.callback = lambda: self.on_child_select(child, child_callback)

    def on_child_select(self, child, child_callback):
        child_callback()
        self.callback()