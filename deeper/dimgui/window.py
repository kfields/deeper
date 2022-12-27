import imgui

from .widget import Widget

class Window(Widget):
    _parent: None
    def __init__(self, title, children=[]):
        super().__init__(children=children)
        self.title = title

    def draw(self):
        imgui.begin(self.title)
        super().draw()
        imgui.end()