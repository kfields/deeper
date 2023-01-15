import imgui

from .widget import Widget

class Window(Widget):
    _parent: None
    def __init__(self, title, children=[], flags=0):
        super().__init__(children=children)
        self.title = title
        self.flags = flags

    def draw(self):
        imgui.begin(self.title, flags=self.flags)
        super().draw()
        imgui.end()