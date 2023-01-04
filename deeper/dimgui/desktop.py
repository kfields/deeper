import imgui

from .widget import Widget

# Note: keep this in case gui per view doesn't pan out

class Desktop(Widget):
    def __init__(self, window, children=[]):
        self.window = window
        super().__init__(children)
        self.default_font = None

    def draw(self):
        if self.default_font:
            imgui.push_font(self.default_font)

        super().draw()

        if self.default_font:
            imgui.pop_font()

        imgui.end()
