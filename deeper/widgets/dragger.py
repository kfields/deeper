import imgui

from deeper.dimgui import Widget

class Dragger(Widget):
    def __init__(self, button, callback):
        super().__init__([button])
        #self.button = button
        self.callback = callback

    def draw(self):
        super().draw()
        if imgui.begin_drag_drop_source():
            self.callback()
            imgui.end_drag_drop_source()
