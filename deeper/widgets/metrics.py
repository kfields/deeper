import imgui

from deeper.dimgui import Widget

class Metrics(Widget):
    def __init__(self, closable=True):
        super().__init__()
        self.closable = closable

    def draw(self):
        super().draw()
        self.visible = imgui.show_metrics_window(self.closable)
