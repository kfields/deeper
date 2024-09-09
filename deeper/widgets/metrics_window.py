from crunge import imgui

from crunge.engine import Renderer
from crunge.engine.imgui.widget import Window

class MetricsWindow(Window):
    def __init__(self, on_close:callable=None):
        super().__init__('Metrics', on_close=on_close)

    def draw(self, renderer: Renderer):
        #super().draw(renderer)
        opened = imgui.show_metrics_window(self.closable)
        if not opened:
            self.on_close()
