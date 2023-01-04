import imgui

from deeper.dimgui import Widget

class Button(Widget):
    def __init__(self, text, callback, small=False):
        super().__init__()
        self.text = text
        self.callback = callback
        self.small = small

    def draw(self):
        clicked = imgui.small_button(self.text) if self.small else imgui.button(self.text)
        if clicked:
            self.callback()
